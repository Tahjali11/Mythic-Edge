from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .config import CARD_PERFORMANCE_MARKDOWN_PATH, CARD_PERFORMANCE_PATH, MATCH_HISTORY_PATH, STATUS_ACTIONS_ROOT
from .grp_id_catalog import load_grp_id_catalog_lookup

_JSON_DICT_CACHE: dict[tuple[str, int | None], dict[str, Any]] = {}


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _safe_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _safe_rate(numerator: int, denominator: int) -> float | str:
    if denominator <= 0:
        return ""
    return numerator / denominator


def _load_json_dict(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    cache_key = _path_cache_key(path)
    cached_payload = _JSON_DICT_CACHE.get(cache_key)
    if cached_payload is not None:
        return cached_payload
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    normalized_payload = payload if isinstance(payload, dict) else {}
    _drop_cached_path(path)
    _JSON_DICT_CACHE[cache_key] = normalized_payload
    return normalized_payload


def _path_cache_key(path: Path) -> tuple[str, int | None]:
    try:
        stat = path.stat()
    except OSError:
        return (str(path), None)
    return (str(path), stat.st_mtime_ns)


def _drop_cached_path(path: Path) -> None:
    normalized_path = str(path)
    stale_keys = [cache_key for cache_key in _JSON_DICT_CACHE if cache_key[0] == normalized_path]
    for stale_key in stale_keys:
        _JSON_DICT_CACHE.pop(stale_key, None)


def _catalog_name_lookup(catalog_lookup: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_name: dict[str, dict[str, Any]] = {}
    for raw_grp_id, entry in catalog_lookup.items():
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("resolved_name", "")).strip()
        if not name:
            continue
        if name in by_name:
            by_name.pop(name, None)
            continue
        candidate = dict(entry)
        candidate["grp_id"] = _safe_int(raw_grp_id)
        by_name[name] = candidate
    return by_name


def _card_key_from_action(entry: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    grp_id = _safe_int(entry.get("grp_id"))
    if grp_id is not None:
        return (
            f"grp:{grp_id}",
            {
                "grp_id": grp_id,
                "card_name": str(entry.get("card_name", "")).strip(),
                "display_name": str(entry.get("display_name", "")).strip() or f"[grpId {grp_id}]",
                "resolution_status": str(entry.get("resolution_status", "")).strip(),
                "layout": str(entry.get("layout", "")).strip(),
                "card_faces": list(entry.get("card_faces") or []),
            },
        )
    display_name = str(entry.get("display_name", "")).strip()
    return (
        f"display:{display_name.lower()}",
        {
            "grp_id": "",
            "card_name": "",
            "display_name": display_name,
            "resolution_status": "unresolved",
            "layout": "",
            "card_faces": [],
        },
    )


def _card_key_from_name(name: str, by_name: dict[str, dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    normalized_name = str(name or "").strip()
    if not normalized_name:
        return ("", {})
    catalog_entry = by_name.get(normalized_name)
    if isinstance(catalog_entry, dict):
        grp_id = _safe_int(catalog_entry.get("grp_id"))
        if grp_id is not None:
            return (
                f"grp:{grp_id}",
                {
                    "grp_id": grp_id,
                    "card_name": normalized_name,
                    "display_name": normalized_name,
                    "resolution_status": str(catalog_entry.get("resolution_status", "")).strip(),
                    "layout": str(catalog_entry.get("resolved_layout", "")).strip(),
                    "card_faces": list(catalog_entry.get("resolved_card_faces") or []),
                },
            )
    return (
        f"name:{normalized_name.lower()}",
        {
            "grp_id": "",
            "card_name": normalized_name,
            "display_name": normalized_name,
            "resolution_status": "name_only",
            "layout": "",
            "card_faces": [],
        },
    )


def _iter_action_payloads(actions_root: Path) -> list[dict[str, Any]]:
    if not actions_root.exists():
        return []
    payloads: list[dict[str, Any]] = []
    for path in sorted(actions_root.glob("*.json")):
        payload = _load_json_dict(path)
        if payload:
            payloads.append(payload)
    return payloads


def _actions_by_game(actions_root: Path) -> dict[tuple[str, int], list[dict[str, Any]]]:
    by_game: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for payload in _iter_action_payloads(actions_root):
        match_id = str(payload.get("match_id", "")).strip()
        for entry in payload.get("entries") or []:
            if not isinstance(entry, dict):
                continue
            game_number = _safe_int(entry.get("game_number"))
            if not match_id or game_number is None:
                continue
            if str(entry.get("actor_relation", "")).strip() not in {"", "local"}:
                continue
            by_game[(match_id, game_number)].append(entry)
    return by_game


def _blank_card_stats(meta: dict[str, Any]) -> dict[str, Any]:
    return {
        "meta": dict(meta),
        "games_seen": set(),
        "games_won": set(),
        "opening_hand_games": set(),
        "opening_hand_wins": set(),
        "cast_games": set(),
        "cast_wins": set(),
        "postboard_cast_games": set(),
        "postboard_cast_wins": set(),
        "mulliganed_away_games": set(),
        "mulliganed_away_wins": set(),
        "seen_in_game_games": set(),
        "seen_in_game_wins": set(),
        "packages": Counter(),
        "package_wins": Counter(),
        "matchups": Counter(),
        "matchup_wins": Counter(),
    }


def _ensure_card_stats(stats_by_key: dict[str, dict[str, Any]], key: str, meta: dict[str, Any]) -> dict[str, Any]:
    existing = stats_by_key.get(key)
    if isinstance(existing, dict):
        if not existing["meta"].get("card_name") and meta.get("card_name"):
            existing["meta"].update(meta)
        return existing
    created = _blank_card_stats(meta)
    stats_by_key[key] = created
    return created


def _game_lookup(payload: dict[str, Any], match_id: str, game_number: int) -> dict[str, Any]:
    for game in payload.get("games") or []:
        if not isinstance(game, dict):
            continue
        if _safe_int(game.get("game_number")) == game_number:
            return game
    return {}


def _aggregate_card_performance(
    *,
    history_payload: dict[str, Any],
    actions_root: Path,
    catalog_lookup: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    matches = history_payload.get("matches") or []
    if not isinstance(matches, list):
        matches = []
    by_name = _catalog_name_lookup(catalog_lookup)
    actions_by_game = _actions_by_game(actions_root)
    stats_by_key: dict[str, dict[str, Any]] = {}
    total_games = 0
    total_game_wins = 0

    for match in matches:
        if not isinstance(match, dict):
            continue
        match_id = str(match.get("match_id", "")).strip()
        opponent_bucket = str(match.get("opponent_archetype") or match.get("opponent_variant") or "").strip()
        for game in match.get("games") or []:
            if not isinstance(game, dict):
                continue
            game_number = _safe_int(game.get("game_number"))
            if game_number is None or not match_id:
                continue
            game_key = (match_id, game_number)
            total_games += 1
            game_result = str(game.get("result", "")).strip()
            won_game = game_result == "W"
            if won_game:
                total_game_wins += 1

            opening_keys: set[str] = set()
            for card_name in game.get("opening_hand") or []:
                key, meta = _card_key_from_name(str(card_name or ""), by_name)
                if not key:
                    continue
                stats = _ensure_card_stats(stats_by_key, key, meta)
                stats["games_seen"].add(game_key)
                stats["opening_hand_games"].add(game_key)
                if won_game:
                    stats["games_won"].add(game_key)
                    stats["opening_hand_wins"].add(game_key)
                opening_keys.add(key)

            mulliganed_keys: set[str] = set()
            for card_name in game.get("mulliganed_away") or []:
                key, meta = _card_key_from_name(str(card_name or ""), by_name)
                if not key:
                    continue
                stats = _ensure_card_stats(stats_by_key, key, meta)
                stats["games_seen"].add(game_key)
                stats["mulliganed_away_games"].add(game_key)
                if won_game:
                    stats["games_won"].add(game_key)
                    stats["mulliganed_away_wins"].add(game_key)
                mulliganed_keys.add(key)

            seen_keys: set[str] = set()
            cast_keys: set[str] = set()
            postboard_cast_keys: set[str] = set()
            for action in actions_by_game.get(game_key, []):
                if not isinstance(action, dict):
                    continue
                key, meta = _card_key_from_action(action)
                stats = _ensure_card_stats(stats_by_key, key, meta)
                stats["games_seen"].add(game_key)
                stats["seen_in_game_games"].add(game_key)
                if won_game:
                    stats["games_won"].add(game_key)
                    stats["seen_in_game_wins"].add(game_key)
                seen_keys.add(key)
                if str(action.get("action_type", "")).strip() == "spell_cast":
                    stats["cast_games"].add(game_key)
                    if game_number > 1:
                        stats["postboard_cast_games"].add(game_key)
                        postboard_cast_keys.add(key)
                    if won_game:
                        stats["cast_wins"].add(game_key)
                        if game_number > 1:
                            stats["postboard_cast_wins"].add(game_key)
                    cast_keys.add(key)

            package_keys = opening_keys | seen_keys
            for key in package_keys:
                stats = stats_by_key[key]
                for other_key in package_keys:
                    if other_key == key:
                        continue
                    stats["packages"][other_key] += 1
                    if won_game:
                        stats["package_wins"][other_key] += 1
                if opponent_bucket:
                    stats["matchups"][opponent_bucket] += 1
                    if won_game:
                        stats["matchup_wins"][opponent_bucket] += 1

    baseline_game_win_rate = _safe_rate(total_game_wins, total_games)
    cards: list[dict[str, Any]] = []
    for key, stats in sorted(
        stats_by_key.items(),
        key=lambda item: (
            -len(item[1]["seen_in_game_games"]),
            -len(item[1]["opening_hand_games"]),
            item[1]["meta"].get("display_name", ""),
        ),
    ):
        meta = stats["meta"]
        top_matchups = []
        for matchup, count in stats["matchups"].most_common(5):
            wins = stats["matchup_wins"][matchup]
            top_matchups.append(
                {
                    "label": matchup,
                    "games": count,
                    "win_rate": _safe_rate(wins, count),
                }
            )
        top_packages = []
        for other_key, count in stats["packages"].most_common(5):
            other_meta = stats_by_key.get(other_key, {}).get("meta", {})
            wins = stats["package_wins"][other_key]
            top_packages.append(
                {
                    "card_key": other_key,
                    "display_name": str(other_meta.get("display_name", other_key)).strip(),
                    "games": count,
                    "win_rate": _safe_rate(wins, count),
                }
            )

        mulligan_rate = _safe_rate(len(stats["mulliganed_away_wins"]), len(stats["mulliganed_away_games"]))
        mulligan_tax: float | str = ""
        if isinstance(mulligan_rate, float) and isinstance(baseline_game_win_rate, float):
            mulligan_tax = baseline_game_win_rate - mulligan_rate

        cards.append(
            {
                "card_key": key,
                "grp_id": meta.get("grp_id", ""),
                "card_name": meta.get("card_name", ""),
                "display_name": meta.get("display_name", ""),
                "resolution_status": meta.get("resolution_status", ""),
                "layout": meta.get("layout", ""),
                "card_faces": list(meta.get("card_faces") or []),
                "games_seen": len(stats["games_seen"]),
                "seen_in_game_games": len(stats["seen_in_game_games"]),
                "seen_in_game_win_rate": _safe_rate(
                    len(stats["seen_in_game_wins"]),
                    len(stats["seen_in_game_games"]),
                ),
                "opening_hand_games": len(stats["opening_hand_games"]),
                "opening_hand_win_rate": _safe_rate(
                    len(stats["opening_hand_wins"]),
                    len(stats["opening_hand_games"]),
                ),
                "cast_games": len(stats["cast_games"]),
                "cast_win_rate": _safe_rate(len(stats["cast_wins"]), len(stats["cast_games"])),
                "postboard_cast_games": len(stats["postboard_cast_games"]),
                "postboard_cast_win_rate": _safe_rate(
                    len(stats["postboard_cast_wins"]),
                    len(stats["postboard_cast_games"]),
                ),
                "mulliganed_away_games": len(stats["mulliganed_away_games"]),
                "mulliganed_away_win_rate": mulligan_rate,
                "mulligan_tax": mulligan_tax,
                "top_matchups": top_matchups,
                "top_packages": top_packages,
            }
        )

    return {
        "object": "manasight_card_performance",
        "generated_at": _now_iso(),
        "total_cards": len(cards),
        "total_games": total_games,
        "baseline_game_win_rate": baseline_game_win_rate,
        "cards": cards,
    }


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Card Performance",
        "",
        f"- Generated at: `{payload.get('generated_at', '')}`",
        f"- Total cards: `{payload.get('total_cards', 0)}`",
        f"- Total games: `{payload.get('total_games', 0)}`",
        f"- Baseline game win rate: `{payload.get('baseline_game_win_rate', '')}`",
        "",
        (
            "| Card | Seen Games | Seen Win % | Opening Games | Opening Win % | "
            "Cast Games | Cast Win % | Postboard Cast Games | Mulliganed Away Games |"
        ),
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for card in (payload.get("cards") or [])[:50]:
        if not isinstance(card, dict):
            continue
        card_row = (
            "| {card} | {seen_games} | {seen_rate} | {opening_games} | {opening_rate} | "
            "{cast_games} | {cast_rate} | {postboard_cast_games} | {mulliganed} |"
        )
        lines.append(
            card_row.format(
                card=str(card.get("display_name", "")).replace("|", "/"),
                seen_games=card.get("seen_in_game_games", 0),
                seen_rate=card.get("seen_in_game_win_rate", ""),
                opening_games=card.get("opening_hand_games", 0),
                opening_rate=card.get("opening_hand_win_rate", ""),
                cast_games=card.get("cast_games", 0),
                cast_rate=card.get("cast_win_rate", ""),
                postboard_cast_games=card.get("postboard_cast_games", 0),
                mulliganed=card.get("mulliganed_away_games", 0),
            )
        )
    return "\n".join(lines) + "\n"


def write_card_performance_payload(payload: dict[str, Any]) -> tuple[Path, Path]:
    CARD_PERFORMANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CARD_PERFORMANCE_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    CARD_PERFORMANCE_MARKDOWN_PATH.write_text(_render_markdown(payload), encoding="utf-8")
    _drop_cached_path(CARD_PERFORMANCE_PATH)
    _JSON_DICT_CACHE[_path_cache_key(CARD_PERFORMANCE_PATH)] = payload
    return CARD_PERFORMANCE_PATH, CARD_PERFORMANCE_MARKDOWN_PATH


def refresh_card_performance_artifacts(
    *,
    history_path: Path = MATCH_HISTORY_PATH,
    actions_root: Path = STATUS_ACTIONS_ROOT,
) -> dict[str, Any]:
    payload = _aggregate_card_performance(
        history_payload=_load_json_dict(history_path),
        actions_root=actions_root,
        catalog_lookup=load_grp_id_catalog_lookup(),
    )
    write_card_performance_payload(payload)
    return payload


def load_card_performance_payload(*, path: Path = CARD_PERFORMANCE_PATH) -> dict[str, Any]:
    payload = _load_json_dict(path)
    if payload:
        return payload
    return {
        "object": "manasight_card_performance",
        "generated_at": _now_iso(),
        "total_cards": 0,
        "total_games": 0,
        "baseline_game_win_rate": "",
        "cards": [],
    }
