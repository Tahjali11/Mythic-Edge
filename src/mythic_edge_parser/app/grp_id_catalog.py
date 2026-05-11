from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .card_catalog import DEFAULT_BULK_TYPE, load_arena_lookup
from .config import GRP_ID_CATALOG_PATH, GRP_ID_OVERRIDES_PATH, ORACLE_DATA_ROOT

DEFAULT_CANDIDATE_REPORT_PATH = ORACLE_DATA_ROOT / "grp-id-candidate-report-latest.json"

_CATALOG_PAYLOAD: dict[str, Any] | None = None
_CATALOG_LOOKUP: dict[str, dict[str, Any]] = {}
_CATALOG_SOURCE_PATH: Path | None = None


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _load_json_dict(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return payload


def _safe_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _safe_string_list(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    normalized: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if text and text not in normalized:
            normalized.append(text)
    return normalized


def _empty_catalog_payload() -> dict[str, Any]:
    now = _now_iso()
    return {
        "object": "manasight_grp_id_catalog",
        "generated_at": now,
        "updated_at": now,
        "cards_by_grp_id": {},
    }


def reset_grp_id_catalog_runtime_state() -> None:
    global _CATALOG_PAYLOAD, _CATALOG_LOOKUP, _CATALOG_SOURCE_PATH

    _CATALOG_PAYLOAD = None
    _CATALOG_LOOKUP = {}
    _CATALOG_SOURCE_PATH = None


def _catalog_target_path(path: Path | None) -> Path:
    return (path or GRP_ID_CATALOG_PATH).resolve(strict=False)


def _blank_entry(grp_id: int) -> dict[str, Any]:
    return {
        "grp_id": grp_id,
        "resolved_name": "",
        "display_name": f"[grpId {grp_id}]",
        "resolution_status": "unresolved",
        "primary_source": "unknown",
        "arena_lookup_name": "",
        "candidate_names": [],
        "submitted_mainboard_count": 0,
        "submitted_sideboard_count": 0,
        "heuristic_role": "",
        "manual_confirmation_hits": 0,
        "exact_manual_confirmation_hits": 0,
        "opening_hand_observations": 0,
        "local_private_hand_observations": 0,
        "top_opening_hand_cooccurrences": [],
        "observation_count": 0,
        "last_seen_at": "",
        "last_seen_match_id": "",
        "last_seen_game_number": "",
        "last_seen_zone_type": "",
        "overlay_grp_ids": [],
        "object_source_grp_ids": [],
        "observed_name_keys": [],
        "observed_action_types": [],
        "observed_object_types": [],
        "observed_card_types": [],
        "observed_super_types": [],
        "observed_subtypes": [],
        "observed_colors": [],
        "resolved_layout": "",
        "resolved_card_faces": [],
        "resolved_type_lines": [],
        "contradiction_flags": [],
        "contradiction_score": 0,
        "blocked_auto_promotion": False,
        "demoted_resolved_name": "",
        "demoted_primary_source": "",
    }


def _normalize_candidate_rows(rows: Any) -> list[dict[str, Any]]:
    if not isinstance(rows, list):
        return []
    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str, int, str]] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        name = str(row.get("name", "")).strip()
        if not name:
            continue
        score = _safe_int(row.get("score")) or 0
        source = str(row.get("source", "candidate_report")).strip() or "candidate_report"
        key = (name, score, source)
        if key in seen:
            continue
        seen.add(key)
        normalized.append(
            {
                "name": name,
                "score": score,
                "source": source,
            }
        )
    normalized.sort(key=lambda item: (-int(item.get("score", 0)), str(item.get("name", ""))))
    return normalized[:10]


def _ensure_entry(cards_by_grp_id: dict[str, dict[str, Any]], grp_id: int) -> dict[str, Any]:
    key = str(grp_id)
    existing = cards_by_grp_id.get(key)
    if not isinstance(existing, dict):
        existing = _blank_entry(grp_id)
        cards_by_grp_id[key] = existing
    existing["grp_id"] = grp_id
    return existing


def _append_unique(entry: dict[str, Any], field: str, value: Any) -> None:
    text = str(value or "").strip()
    if not text:
        return
    values = _safe_string_list(entry.get(field))
    if text not in values:
        values.append(text)
        entry[field] = values


def _candidate_name_from_entry(entry: dict[str, Any]) -> str:
    candidate_names = entry.get("candidate_names") or []
    if not isinstance(candidate_names, list) or not candidate_names:
        return ""
    first = candidate_names[0]
    if not isinstance(first, dict):
        return ""
    return str(first.get("name", "")).strip()


def _cards_by_name(arena_lookup: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for card in arena_lookup.values():
        if not isinstance(card, dict):
            continue
        name = str(card.get("name", "")).strip()
        if name and name not in lookup:
            lookup[name] = card
    return lookup


def _card_face_names(card: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for face in card.get("card_faces") or []:
        if not isinstance(face, dict):
            continue
        name = str(face.get("name", "")).strip()
        if name and name not in names:
            names.append(name)
    return names


def _card_type_lines(card: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    type_line = str(card.get("type_line", "")).strip()
    if type_line:
        lines.append(type_line)
    for face in card.get("card_faces") or []:
        if not isinstance(face, dict):
            continue
        face_type_line = str(face.get("type_line", "")).strip()
        if face_type_line:
            lines.append(face_type_line)
    return lines


def _reference_card_looks_like_land(entry: dict[str, Any]) -> bool:
    for type_line in _safe_string_list(entry.get("resolved_type_lines")):
        if "Land" in type_line:
            return True
    return False


def _entry_looks_like_land(entry: dict[str, Any]) -> bool:
    observed_card_types = set(_safe_string_list(entry.get("observed_card_types")))
    if "CardType_Land" in observed_card_types:
        non_land_types = {card_type for card_type in observed_card_types if card_type != "CardType_Land"}
        if not non_land_types:
            return True

    observed_action_types = _safe_string_list(entry.get("observed_action_types"))
    has_play = any("ActionType_Play" in action_type for action_type in observed_action_types)
    has_mana = any("ActionType_Activate_Mana" in action_type for action_type in observed_action_types)
    return has_play and has_mana


def _refresh_reference_metadata(entry: dict[str, Any], cards_by_name: dict[str, dict[str, Any]]) -> None:
    reference_name = (
        str(entry.get("resolved_name", "")).strip()
        or str(entry.get("demoted_resolved_name", "")).strip()
        or str(entry.get("arena_lookup_name", "")).strip()
    )
    if not reference_name:
        entry["resolved_layout"] = ""
        entry["resolved_card_faces"] = []
        entry["resolved_type_lines"] = []
        return
    card = cards_by_name.get(reference_name)
    if not isinstance(card, dict):
        return
    entry["resolved_layout"] = str(card.get("layout", "")).strip()
    entry["resolved_card_faces"] = _card_face_names(card)
    entry["resolved_type_lines"] = _card_type_lines(card)


def _evaluate_contradictions(entry: dict[str, Any]) -> None:
    flags: list[str] = []
    reference_name = str(entry.get("resolved_name", "")).strip() or str(
        entry.get("demoted_resolved_name", "")
    ).strip()
    has_reference_types = bool(_safe_string_list(entry.get("resolved_type_lines")))
    if (
        reference_name
        and has_reference_types
        and _entry_looks_like_land(entry)
        and not _reference_card_looks_like_land(entry)
    ):
        flags.append("observed_land_but_resolved_card_not_land")

    entry["contradiction_flags"] = flags
    entry["contradiction_score"] = len(flags)
    entry["blocked_auto_promotion"] = bool(flags)

    if flags and str(entry.get("resolved_name", "")).strip():
        entry["demoted_resolved_name"] = str(entry.get("resolved_name", "")).strip()
        entry["demoted_primary_source"] = str(entry.get("primary_source", "")).strip()
        entry["resolved_name"] = ""
        entry["resolution_status"] = "contradicted"
        entry["primary_source"] = "contradicted_gameplay_observation"


def is_grp_id_promotable(grp_id_or_entry: int | str | dict[str, Any], *, path: Path | None = None) -> bool:
    if isinstance(grp_id_or_entry, dict):
        entry = grp_id_or_entry
    else:
        entry = resolve_grp_id_entry(grp_id_or_entry, path=path)
    return not bool(entry.get("blocked_auto_promotion")) and not bool(entry.get("contradiction_flags"))


def _finalize_entry(entry: dict[str, Any]) -> None:
    grp_id = _safe_int(entry.get("grp_id")) or 0
    resolved_name = str(entry.get("resolved_name", "")).strip()
    candidate_rows = _normalize_candidate_rows(entry.get("candidate_names"))
    entry["candidate_names"] = candidate_rows

    if resolved_name:
        entry["display_name"] = resolved_name
        return

    if entry.get("contradiction_flags"):
        entry["resolution_status"] = "contradicted"
        entry["display_name"] = f"[grpId {grp_id}]"
        return

    candidate_name = _candidate_name_from_entry(entry)
    if candidate_name:
        entry["resolution_status"] = "candidate"
        entry["display_name"] = f"{candidate_name}? [grpId {grp_id}]"
        if not str(entry.get("primary_source", "")).strip():
            entry["primary_source"] = "candidate_report"
        return

    entry["resolution_status"] = "unresolved"
    entry["display_name"] = f"[grpId {grp_id}]"
    if not str(entry.get("primary_source", "")).strip():
        entry["primary_source"] = "unknown"


def _merge_resolved_name(entry: dict[str, Any], *, name: str, source: str, status: str) -> None:
    normalized_name = str(name or "").strip()
    if not normalized_name:
        return
    existing_name = str(entry.get("resolved_name", "")).strip()
    if existing_name and existing_name != normalized_name and source != "grp_id_override":
        return
    entry["resolved_name"] = normalized_name
    entry["resolution_status"] = status
    entry["primary_source"] = source


def _merge_candidate(entry: dict[str, Any], *, name: str, score: int, source: str) -> None:
    normalized_name = str(name or "").strip()
    if not normalized_name:
        return
    candidate_rows = _normalize_candidate_rows(entry.get("candidate_names"))
    candidate_rows.append({"name": normalized_name, "score": int(score), "source": source})
    entry["candidate_names"] = _normalize_candidate_rows(candidate_rows)


def _candidate_report_rows(report: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in ("unresolved_mainboard_grp_ids", "unresolved_sideboard_grp_ids"):
        raw_rows = report.get(key) or []
        if not isinstance(raw_rows, list):
            continue
        for row in raw_rows:
            if isinstance(row, dict):
                rows.append(row)
    return rows


def _override_resolution_status(raw_entry: dict[str, Any]) -> str:
    source = str(raw_entry.get("name_source", "")).strip()
    if source == "confirmed_inferred_candidate":
        return "inferred_confirmed"
    if source == "auto_promoted_singleton_candidate":
        return "legacy_auto_promoted"
    return "confirmed"


def _apply_override_entries(
    cards_by_grp_id: dict[str, dict[str, Any]],
    *,
    override_payload: dict[str, Any],
) -> None:
    for raw_grp_id, raw_entry in (override_payload.get("cards_by_grp_id") or {}).items():
        grp_id = _safe_int(raw_grp_id)
        if grp_id is None or not isinstance(raw_entry, dict):
            continue
        entry = _ensure_entry(cards_by_grp_id, grp_id)
        name = str(raw_entry.get("name", "")).strip()
        if name:
            _merge_resolved_name(
                entry,
                name=name,
                source=str(raw_entry.get("name_source", "")).strip() or "grp_id_override",
                status=_override_resolution_status(raw_entry),
            )
        demoted_name = str(raw_entry.get("demoted_resolved_name", "") or raw_entry.get("demoted_name", "")).strip()
        if demoted_name:
            entry["demoted_resolved_name"] = demoted_name
        demoted_source = str(raw_entry.get("demoted_primary_source", "")).strip()
        if demoted_source:
            entry["demoted_primary_source"] = demoted_source
        if raw_entry.get("contradiction_flags") not in (None, ""):
            entry["contradiction_flags"] = _safe_string_list(raw_entry.get("contradiction_flags"))
        if raw_entry.get("blocked_auto_promotion") is not None:
            entry["blocked_auto_promotion"] = bool(raw_entry.get("blocked_auto_promotion"))
        for field in (
            "heuristic_role",
            "opening_hand_observations",
            "local_private_hand_observations",
            "top_opening_hand_cooccurrences",
            "promotion_score",
            "promotion_reasons",
        ):
            if field in raw_entry and raw_entry[field] not in (None, "", [], {}):
                entry[field] = raw_entry[field]
        fingerprint = raw_entry.get("fingerprint") or {}
        if isinstance(fingerprint, dict):
            for row in fingerprint.get("card_types_seen") or []:
                if isinstance(row, dict):
                    _append_unique(entry, "observed_card_types", row.get("card_type"))
            for row in fingerprint.get("action_types_seen") or []:
                if isinstance(row, dict):
                    _append_unique(entry, "observed_action_types", row.get("action_type"))
            for row in fingerprint.get("observed_name_keys") or []:
                if isinstance(row, dict):
                    _append_unique(entry, "observed_name_keys", row.get("name_key"))


def _apply_exact_numeric_arena_lookup(
    cards_by_grp_id: dict[str, dict[str, Any]],
    *,
    arena_lookup: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    cards_by_name = _cards_by_name(arena_lookup)
    for raw_arena_id, raw_card in arena_lookup.items():
        grp_id = _safe_int(raw_arena_id)
        if grp_id is None or not isinstance(raw_card, dict):
            continue
        entry = _ensure_entry(cards_by_grp_id, grp_id)
        arena_name = str(raw_card.get("name", "")).strip()
        if arena_name:
            entry["arena_lookup_name"] = arena_name
            if not str(entry.get("resolved_name", "")).strip():
                _merge_resolved_name(
                    entry,
                    name=arena_name,
                    source="exact_numeric_arena_lookup",
                    status="exact_numeric_match",
                )
    return cards_by_name


def _apply_candidate_report_entries(
    cards_by_grp_id: dict[str, dict[str, Any]],
    *,
    report: dict[str, Any],
) -> None:
    for row in _candidate_report_rows(report):
        grp_id = _safe_int(row.get("grp_id"))
        if grp_id is None:
            continue
        entry = _ensure_entry(cards_by_grp_id, grp_id)
        section = str(row.get("section", "")).strip()
        submitted_count = _safe_int(row.get("submitted_count")) or 0
        if section == "mainboard":
            entry["submitted_mainboard_count"] = submitted_count
        elif section == "sideboard":
            entry["submitted_sideboard_count"] = submitted_count
        entry["heuristic_role"] = str(row.get("heuristic_role", "")).strip()
        entry["manual_confirmation_hits"] = _safe_int(row.get("manual_confirmation_hits")) or 0
        entry["exact_manual_confirmation_hits"] = _safe_int(row.get("exact_manual_confirmation_hits")) or 0
        entry["opening_hand_observations"] = _safe_int(row.get("opening_hand_observations")) or 0
        entry["local_private_hand_observations"] = _safe_int(row.get("local_private_hand_observations")) or 0
        entry["top_opening_hand_cooccurrences"] = list(row.get("top_opening_hand_cooccurrences") or [])

        for candidate in list(row.get("ranked_candidates") or [])[:5]:
            if not isinstance(candidate, dict):
                continue
            _merge_candidate(
                entry,
                name=str(candidate.get("name", "")).strip(),
                score=_safe_int(candidate.get("score")) or 0,
                source="candidate_report",
            )
        auto_suggestion = str(row.get("auto_suggestion", "")).strip()
        if auto_suggestion:
            _merge_candidate(
                entry,
                name=auto_suggestion,
                score=999,
                source="candidate_report_auto_suggestion",
            )


def _finalize_catalog_entries(
    cards_by_grp_id: dict[str, dict[str, Any]],
    *,
    cards_by_name: dict[str, dict[str, Any]],
) -> None:
    for entry in cards_by_grp_id.values():
        if not isinstance(entry, dict):
            continue
        _refresh_reference_metadata(entry, cards_by_name)
        _evaluate_contradictions(entry)
        _finalize_entry(entry)


def _rebuild_catalog_payload(
    *,
    path: Path,
    grp_id_override_path: Path | None,
    candidate_report_path: Path | None,
    format_key: str,
    bulk_type: str,
    output_dir: Path,
) -> dict[str, Any]:
    previous = _empty_catalog_payload()
    if path.exists():
        try:
            previous = _load_json_dict(path)
        except Exception:
            previous = _empty_catalog_payload()

    cards_by_grp_id = previous.get("cards_by_grp_id")
    if not isinstance(cards_by_grp_id, dict):
        cards_by_grp_id = {}

    try:
        override_payload = _load_json_dict(grp_id_override_path or GRP_ID_OVERRIDES_PATH)
    except Exception:
        override_payload = {"cards_by_grp_id": {}}
    _apply_override_entries(cards_by_grp_id, override_payload=override_payload)

    try:
        arena_lookup = load_arena_lookup(
            format_key=format_key,
            bulk_type=bulk_type,
            output_dir=output_dir,
        )
    except Exception:
        arena_lookup = {}
    cards_by_name = _apply_exact_numeric_arena_lookup(cards_by_grp_id, arena_lookup=arena_lookup)

    report_path = candidate_report_path or DEFAULT_CANDIDATE_REPORT_PATH
    if report_path.exists():
        try:
            report = _load_json_dict(report_path)
        except Exception:
            report = {}
        _apply_candidate_report_entries(cards_by_grp_id, report=report)

    _finalize_catalog_entries(cards_by_grp_id, cards_by_name=cards_by_name)

    payload = {
        "object": "manasight_grp_id_catalog",
        "generated_at": str(previous.get("generated_at", "")).strip() or _now_iso(),
        "updated_at": _now_iso(),
        "cards_by_grp_id": dict(sorted(cards_by_grp_id.items(), key=lambda item: int(item[0]))),
    }
    return payload


def write_grp_id_catalog_payload(payload: dict[str, Any], *, path: Path | None = None) -> Path:
    target_path = _catalog_target_path(path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return target_path


def _set_catalog_runtime_cache(payload: dict[str, Any], *, path: Path) -> None:
    global _CATALOG_PAYLOAD, _CATALOG_LOOKUP, _CATALOG_SOURCE_PATH

    _CATALOG_PAYLOAD = payload
    cards_by_grp_id = payload.get("cards_by_grp_id")
    _CATALOG_LOOKUP = cards_by_grp_id if isinstance(cards_by_grp_id, dict) else {}
    _CATALOG_SOURCE_PATH = path


def refresh_grp_id_catalog(
    *,
    path: Path | None = None,
    grp_id_override_path: Path | None = None,
    candidate_report_path: Path | None = None,
    format_key: str = "arena",
    bulk_type: str = DEFAULT_BULK_TYPE,
    output_dir: Path = ORACLE_DATA_ROOT,
) -> Path:
    target_path = _catalog_target_path(path)
    payload = _rebuild_catalog_payload(
        path=target_path,
        grp_id_override_path=grp_id_override_path,
        candidate_report_path=candidate_report_path,
        format_key=format_key,
        bulk_type=bulk_type,
        output_dir=output_dir,
    )
    write_grp_id_catalog_payload(payload, path=target_path)
    _set_catalog_runtime_cache(payload, path=target_path)
    return target_path


def _prime_catalog_from_disk(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        payload = _load_json_dict(path)
    except Exception:
        return False
    cards_by_grp_id = payload.get("cards_by_grp_id")
    if not isinstance(cards_by_grp_id, dict):
        return False
    _set_catalog_runtime_cache(payload, path=path)
    return True


def bootstrap_grp_id_catalog(
    *,
    path: Path | None = None,
    grp_id_override_path: Path | None = None,
    candidate_report_path: Path | None = None,
    format_key: str = "arena",
    bulk_type: str = DEFAULT_BULK_TYPE,
    output_dir: Path = ORACLE_DATA_ROOT,
) -> None:
    target_path = _catalog_target_path(path)
    if _CATALOG_PAYLOAD is not None and _CATALOG_SOURCE_PATH == target_path:
        return
    if _prime_catalog_from_disk(target_path):
        return
    refresh_grp_id_catalog(
        path=target_path,
        grp_id_override_path=grp_id_override_path,
        candidate_report_path=candidate_report_path,
        format_key=format_key,
        bulk_type=bulk_type,
        output_dir=output_dir,
    )


def load_grp_id_catalog_payload(*, path: Path | None = None) -> dict[str, Any]:
    bootstrap_grp_id_catalog(path=path)
    return dict(_CATALOG_PAYLOAD or _empty_catalog_payload())


def load_grp_id_catalog_lookup(*, path: Path | None = None) -> dict[str, dict[str, Any]]:
    bootstrap_grp_id_catalog(path=path)
    return _CATALOG_LOOKUP


def resolve_grp_id_entry(grp_id: int | str, *, path: Path | None = None) -> dict[str, Any]:
    bootstrap_grp_id_catalog(path=path)
    return dict(_CATALOG_LOOKUP.get(str(grp_id), _blank_entry(_safe_int(grp_id) or 0)))


def resolve_grp_id_name(
    grp_id: int | str,
    *,
    include_candidates: bool = True,
    path: Path | None = None,
) -> str:
    entry = resolve_grp_id_entry(grp_id, path=path)
    resolved_name = str(entry.get("resolved_name", "")).strip()
    if resolved_name:
        return resolved_name
    if include_candidates:
        return str(entry.get("display_name", "")).strip() or f"[grpId {grp_id}]"
    return f"[grpId {grp_id}]"


def observe_gameplay_objects(
    observations: list[dict[str, Any]],
    *,
    timestamp: str,
    match_id: str,
    game_number: int | None,
    path: Path | None = None,
) -> Path | None:
    target_path = _catalog_target_path(path)
    bootstrap_grp_id_catalog(path=target_path)
    if _CATALOG_PAYLOAD is None:
        return None

    cards_by_grp_id = _CATALOG_PAYLOAD.get("cards_by_grp_id")
    if not isinstance(cards_by_grp_id, dict):
        cards_by_grp_id = {}
        _CATALOG_PAYLOAD["cards_by_grp_id"] = cards_by_grp_id

    changed = False
    for observation in observations:
        if not isinstance(observation, dict):
            continue
        grp_id = _safe_int(observation.get("grp_id"))
        if grp_id is None:
            continue
        entry = _ensure_entry(cards_by_grp_id, grp_id)
        entry["observation_count"] = (_safe_int(entry.get("observation_count")) or 0) + 1
        entry["last_seen_at"] = timestamp
        entry["last_seen_match_id"] = match_id
        entry["last_seen_game_number"] = game_number if game_number is not None else ""
        entry["last_seen_zone_type"] = str(observation.get("zone_type", "")).strip()
        for list_field in (
            ("overlay_grp_ids", observation.get("overlay_grp_id")),
            ("object_source_grp_ids", observation.get("object_source_grp_id")),
            ("observed_name_keys", observation.get("name_key")),
        ):
            _append_unique(entry, list_field[0], list_field[1])
        for field, values in (
            ("observed_action_types", observation.get("action_types")),
            ("observed_object_types", observation.get("object_types")),
            ("observed_card_types", observation.get("card_types")),
            ("observed_super_types", observation.get("super_types")),
            ("observed_subtypes", observation.get("subtypes")),
            ("observed_colors", observation.get("colors")),
        ):
            for value in values or []:
                _append_unique(entry, field, value)
        if entry.get("primary_source") in ("", "unknown"):
            entry["primary_source"] = "gameplay_observation"
        _evaluate_contradictions(entry)
        _finalize_entry(entry)
        changed = True

    if not changed:
        return None

    _CATALOG_PAYLOAD["updated_at"] = _now_iso()
    _set_catalog_runtime_cache(_CATALOG_PAYLOAD, path=target_path)
    return write_grp_id_catalog_payload(_CATALOG_PAYLOAD, path=target_path)
