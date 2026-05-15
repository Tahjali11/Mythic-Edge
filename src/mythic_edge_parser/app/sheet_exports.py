from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .card_performance import load_card_performance_payload
from .config import (
    ACTIVE_DECK_PROFILE_PATH,
    COLLECTION_PROFILE_PATH,
    STATUS_ROOT,
)
from .gameplay_actions import load_active_match_actions_payload
from .sheet_schema import (
    ACTION_LOG_FAMILY,
    CARD_PERFORMANCE_FAMILY,
    COLLECTION_SNAPSHOT_FAMILY,
    DECK_SNAPSHOT_FAMILY,
    PARSER_STATUS_FAMILY,
    runtime_sheet_spec,
)

_JSON_DICT_CACHE: dict[tuple[str, int | None], dict[str, Any]] = {}


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


def _safe_int(value: Any) -> int | str:
    if isinstance(value, bool):
        return ""
    try:
        return int(value)
    except (TypeError, ValueError):
        return ""


def _stable_fingerprint(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha1(encoded.encode("utf-8")).hexdigest()


def _without_keys(payload: dict[str, Any], keys_to_remove: set[str]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key not in keys_to_remove}


def _base_runtime_row(event_family: str, **fields: Any) -> dict[str, Any]:
    spec = runtime_sheet_spec(event_family)
    return {
        "event_family": spec.family,
        "event_type": spec.event_type,
        "scope": spec.scope,
        **fields,
    }


def _status_snapshot_path() -> Path:
    return STATUS_ROOT / "manasight_status_latest.json"


def _rows_fingerprint(rows: list[dict[str, Any]], *, transient_keys: set[str]) -> str:
    return _stable_fingerprint([_without_keys(row, transient_keys) for row in rows])


def _row_fingerprint(row: dict[str, Any], *, transient_keys: set[str]) -> str:
    return _stable_fingerprint(_without_keys(row, transient_keys))


def _snapshot_rows_if_changed(
    rows: list[dict[str, Any]],
    *,
    transient_keys: set[str],
    last_fingerprint_attr: str,
) -> list[dict[str, Any]]:
    if not rows:
        return []

    fingerprint = _rows_fingerprint(rows, transient_keys=transient_keys)
    if fingerprint == getattr(EXPORT_STATE, last_fingerprint_attr):
        return []
    setattr(EXPORT_STATE, last_fingerprint_attr, fingerprint)
    return rows


def _snapshot_row_if_changed(
    row: dict[str, Any],
    *,
    transient_keys: set[str],
    last_fingerprint_attr: str,
) -> list[dict[str, Any]]:
    if not row:
        return []

    fingerprint = _row_fingerprint(row, transient_keys=transient_keys)
    if fingerprint == getattr(EXPORT_STATE, last_fingerprint_attr):
        return []
    setattr(EXPORT_STATE, last_fingerprint_attr, fingerprint)
    return [row]


@dataclass(slots=True)
class SheetExportState:
    posted_action_keys: set[str] = field(default_factory=set)
    last_deck_snapshot_fingerprint: str = ""
    last_collection_snapshot_fingerprint: str = ""
    last_parser_status_fingerprint: str = ""
    last_card_performance_fingerprint: str = ""


EXPORT_STATE = SheetExportState()


def reset_sheet_export_state() -> None:
    EXPORT_STATE.posted_action_keys.clear()
    EXPORT_STATE.last_deck_snapshot_fingerprint = ""
    EXPORT_STATE.last_collection_snapshot_fingerprint = ""
    EXPORT_STATE.last_parser_status_fingerprint = ""
    EXPORT_STATE.last_card_performance_fingerprint = ""
    _JSON_DICT_CACHE.clear()


def _action_row(entry: dict[str, Any], *, generated_at: str) -> dict[str, Any]:
    return _base_runtime_row(
        ACTION_LOG_FAMILY,
        generated_at=generated_at,
        match_id=str(entry.get("match_id", "")).strip(),
        game_number=_safe_int(entry.get("game_number")),
        turn_number=_safe_int(entry.get("turn_number")),
        timestamp=str(entry.get("timestamp", "")).strip(),
        action_type=str(entry.get("action_type", "")).strip(),
        cast_mode=str(entry.get("cast_mode", "")).strip(),
        grp_id=_safe_int(entry.get("grp_id")),
        card_name=str(entry.get("card_name", "")).strip(),
        display_name=str(entry.get("display_name", "")).strip(),
        resolution_status=str(entry.get("resolution_status", "")).strip(),
        actor_relation=str(entry.get("actor_relation", "")).strip(),
        from_zone_type=str(entry.get("from_zone_type", "")).strip(),
        to_zone_type=str(entry.get("to_zone_type", "")).strip(),
        summary=str(entry.get("summary", "")).strip(),
    )


def _action_row_key(row: dict[str, Any]) -> str:
    return "||".join(
        [
            str(row.get("match_id", "")),
            str(row.get("game_number", "")),
            str(row.get("timestamp", "")),
            str(row.get("action_type", "")),
            str(row.get("grp_id", "")),
            str(row.get("from_zone_type", "")),
            str(row.get("to_zone_type", "")),
        ]
    )


def _deck_snapshot_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    generated_at = str(payload.get("generated_at", "")).strip()
    submitted_at = str(payload.get("submitted_at", "")).strip()
    match_id = str(payload.get("match_id", "")).strip()
    signature = str(payload.get("signature", "")).strip()
    matched_deck = {}
    matched_decks = payload.get("matched_decks") or []
    if isinstance(matched_decks, list) and matched_decks:
        first = matched_decks[0]
        if isinstance(first, dict):
            matched_deck = first
    deck_name = str(matched_deck.get("name", "")).strip()
    deck_match_mode = str(matched_deck.get("match_mode", "")).strip()
    deck_format = str(matched_deck.get("format", "")).strip()

    rows: list[dict[str, Any]] = []
    for section_name in ("mainboard", "sideboard"):
        section_cards = payload.get(section_name) or []
        if not isinstance(section_cards, list):
            continue
        for card in section_cards:
            if not isinstance(card, dict):
                continue
            rows.append(
                _base_runtime_row(
                    DECK_SNAPSHOT_FAMILY,
                    generated_at=generated_at,
                    submitted_at=submitted_at,
                    match_id=match_id,
                    deck_signature=signature,
                    deck_name=deck_name,
                    deck_match_mode=deck_match_mode,
                    deck_format=deck_format,
                    section=str(card.get("section", section_name)).strip(),
                    arena_id=_safe_int(card.get("arena_id")),
                    count=_safe_int(card.get("count")),
                    card_name=str(card.get("name", "")).strip(),
                    rarity=str(card.get("rarity", "")).strip(),
                    set=str(card.get("set", "")).strip(),
                    type_line=str(card.get("type_line", "")).strip(),
                    colors=list(card.get("colors") or []),
                    owned_copies=_safe_int(card.get("owned_copies")),
                    missing_copies=_safe_int(card.get("missing_copies")),
                )
            )
    return rows


def _collection_snapshot_row(payload: dict[str, Any]) -> dict[str, Any]:
    inventory = payload.get("inventory") or {}
    completion = payload.get("active_deck_completion") or {}
    raw_wildcards = inventory.get("wildcards") or {}
    wildcards = raw_wildcards if isinstance(raw_wildcards, dict) else {}
    return _base_runtime_row(
        COLLECTION_SNAPSHOT_FAMILY,
        generated_at=str(payload.get("generated_at", "")).strip(),
        collection_available=bool(payload.get("collection_available")),
        inventory_available=bool(payload.get("inventory_available")),
        owned_unique_cards=_safe_int(payload.get("owned_unique_cards")),
        owned_total_card_copies=_safe_int(payload.get("owned_total_card_copies")),
        owned_by_rarity=payload.get("owned_by_rarity") or {},
        inventory_gold=_safe_int(inventory.get("gold")),
        inventory_gems=_safe_int(inventory.get("gems")),
        wildcards_common=_safe_int(inventory.get("wildcards_common", wildcards.get("common"))),
        wildcards_uncommon=_safe_int(inventory.get("wildcards_uncommon", wildcards.get("uncommon"))),
        wildcards_rare=_safe_int(inventory.get("wildcards_rare", wildcards.get("rare"))),
        wildcards_mythic=_safe_int(inventory.get("wildcards_mythic", wildcards.get("mythic"))),
        active_deck_missing_by_rarity=payload.get("active_deck_missing_by_rarity") or {},
        active_deck_completion_rate=completion.get("completion_rate", ""),
        wanted_cards=payload.get("wanted_cards") or [],
    )


def _parser_status_row(payload: dict[str, Any]) -> dict[str, Any]:
    return _base_runtime_row(
        PARSER_STATUS_FAMILY,
        updated_at=str(payload.get("updated_at", "")).strip(),
        status=str(payload.get("status", "")).strip(),
        current_match_id=str(payload.get("current_match_id", "")).strip(),
        current_game_number=_safe_int(payload.get("current_game_number")),
        current_player_team=str(payload.get("current_player_team", "")).strip(),
        last_event_kind=str(payload.get("last_event_kind", "")).strip(),
        last_event_at=str(payload.get("last_event_at", "")).strip(),
        webhook_successes=_safe_int(payload.get("webhook_successes")),
        webhook_failures=_safe_int(payload.get("webhook_failures")),
        event_failures=_safe_int(payload.get("event_failures")),
        router_failures=_safe_int(payload.get("router_failures")),
        active_deck_signature=str(payload.get("active_deck_signature", "")).strip(),
        active_deck_name=str(payload.get("active_deck_name", "")).strip(),
        active_match_action_count=_safe_int(payload.get("active_match_action_count")),
    )


def _card_performance_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    generated_at = str(payload.get("generated_at", "")).strip()
    rows: list[dict[str, Any]] = []
    for card in payload.get("cards") or []:
        if not isinstance(card, dict):
            continue
        rows.append(
            _base_runtime_row(
                CARD_PERFORMANCE_FAMILY,
                generated_at=generated_at,
                card_key=str(card.get("card_key", "")).strip(),
                grp_id=_safe_int(card.get("grp_id")),
                card_name=str(card.get("card_name", "")).strip(),
                display_name=str(card.get("display_name", "")).strip(),
                resolution_status=str(card.get("resolution_status", "")).strip(),
                layout=str(card.get("layout", "")).strip(),
                card_faces=list(card.get("card_faces") or []),
                games_seen=_safe_int(card.get("games_seen")),
                seen_in_game_games=_safe_int(card.get("seen_in_game_games")),
                seen_in_game_win_rate=card.get("seen_in_game_win_rate", ""),
                opening_hand_games=_safe_int(card.get("opening_hand_games")),
                opening_hand_win_rate=card.get("opening_hand_win_rate", ""),
                cast_games=_safe_int(card.get("cast_games")),
                cast_win_rate=card.get("cast_win_rate", ""),
                postboard_cast_games=_safe_int(card.get("postboard_cast_games")),
                postboard_cast_win_rate=card.get("postboard_cast_win_rate", ""),
                mulliganed_away_games=_safe_int(card.get("mulliganed_away_games")),
                mulligan_tax=card.get("mulligan_tax", ""),
                top_matchups=list(card.get("top_matchups") or []),
                top_packages=list(card.get("top_packages") or []),
            )
        )
    return rows


def collect_runtime_sheet_rows(
    *,
    action_payload: dict[str, Any] | None = None,
    deck_payload: dict[str, Any] | None = None,
    collection_payload: dict[str, Any] | None = None,
    status_payload: dict[str, Any] | None = None,
    card_performance_payload: dict[str, Any] | None = None,
    post_action_rows: bool = True,
    post_deck_snapshot_rows: bool = True,
    post_collection_snapshot_rows: bool = True,
    post_parser_status_rows: bool = True,
    post_card_performance_rows: bool = True,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    if post_action_rows:
        payload = action_payload if action_payload is not None else load_active_match_actions_payload()
        generated_at = str(payload.get("generated_at", "")).strip()
        for entry in payload.get("entries") or []:
            if not isinstance(entry, dict):
                continue
            row = _action_row(entry, generated_at=generated_at)
            key = _action_row_key(row)
            if not key.strip() or key in EXPORT_STATE.posted_action_keys:
                continue
            EXPORT_STATE.posted_action_keys.add(key)
            rows.append(row)

    if post_deck_snapshot_rows:
        payload = deck_payload if deck_payload is not None else _load_json_dict(ACTIVE_DECK_PROFILE_PATH)
        deck_rows = _deck_snapshot_rows(payload) if payload else []
        rows.extend(
            _snapshot_rows_if_changed(
                deck_rows,
                transient_keys={"generated_at"},
                last_fingerprint_attr="last_deck_snapshot_fingerprint",
            )
        )

    if post_collection_snapshot_rows:
        payload = collection_payload if collection_payload is not None else _load_json_dict(COLLECTION_PROFILE_PATH)
        collection_row = _collection_snapshot_row(payload) if payload else {}
        rows.extend(
            _snapshot_row_if_changed(
                collection_row,
                transient_keys={"generated_at"},
                last_fingerprint_attr="last_collection_snapshot_fingerprint",
            )
        )

    if post_parser_status_rows:
        payload = status_payload if status_payload is not None else _load_json_dict(_status_snapshot_path())
        status_row = _parser_status_row(payload) if payload else {}
        rows.extend(
            _snapshot_row_if_changed(
                status_row,
                transient_keys={
                    "updated_at",
                    "last_event_at",
                    "webhook_successes",
                    "webhook_failures",
                    "active_match_action_count",
                },
                last_fingerprint_attr="last_parser_status_fingerprint",
            )
        )

    if post_card_performance_rows:
        payload = card_performance_payload if card_performance_payload is not None else load_card_performance_payload()
        performance_rows = _card_performance_rows(payload) if payload else []
        rows.extend(
            _snapshot_rows_if_changed(
                performance_rows,
                transient_keys={"generated_at"},
                last_fingerprint_attr="last_card_performance_fingerprint",
            )
        )

    return rows
