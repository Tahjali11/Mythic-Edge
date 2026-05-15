from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import state
from .card_catalog import load_combined_card_lookup
from .config import (
    ACTIVE_DECK_PROFILE_PATH,
    ACTIVE_MATCH_SNAPSHOT_PATH,
    ACTIVE_MATCH_TIMELINE_PATH,
    ACTIVE_SUBMITTED_DECK_PATH,
    COLLECTION_PROFILE_PATH,
    MATCH_HISTORY_PATH,
    STATUS_TIMELINES_ROOT,
)
from .diagnostics import submitted_deck_signature, update_runtime_status
from .extractors import (
    _extract_game_result_identity,
    _extract_local_private_hand_instance_ids,
    _extract_turn_info,
)
from .transforms import summarize

_CARD_LOOKUP_CACHE: dict[str, dict[str, Any]] | None = None


@dataclass(slots=True)
class RuntimeSurfaceState:
    active_deck_state: dict[str, Any] = field(default_factory=dict)
    match_deck_contexts: dict[str, dict[str, Any]] = field(default_factory=dict)
    deck_collections: dict[str, Any] = field(default_factory=dict)
    player_card_counts: dict[str, int] = field(default_factory=dict)
    inventory_snapshot: dict[str, Any] = field(default_factory=dict)
    match_timelines: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    match_timeline_keys: dict[str, set[str]] = field(default_factory=dict)
    match_history: dict[str, dict[str, Any]] = field(default_factory=dict)


SURFACE_STATE = RuntimeSurfaceState()
_ACTIVE_DECK_STATE = SURFACE_STATE.active_deck_state
_MATCH_DECK_CONTEXTS = SURFACE_STATE.match_deck_contexts
_DECK_COLLECTIONS = SURFACE_STATE.deck_collections
_PLAYER_CARD_COUNTS = SURFACE_STATE.player_card_counts
_INVENTORY_SNAPSHOT = SURFACE_STATE.inventory_snapshot
_MATCH_TIMELINES = SURFACE_STATE.match_timelines
_MATCH_TIMELINE_KEYS = SURFACE_STATE.match_timeline_keys
_MATCH_HISTORY = SURFACE_STATE.match_history
_WRITE_FINGERPRINTS: dict[str, str] = {}


def reset_runtime_surface_state() -> None:
    global _CARD_LOOKUP_CACHE

    _CARD_LOOKUP_CACHE = None
    _WRITE_FINGERPRINTS.clear()
    _ACTIVE_DECK_STATE.clear()
    _MATCH_DECK_CONTEXTS.clear()
    _DECK_COLLECTIONS.clear()
    _PLAYER_CARD_COUNTS.clear()
    _INVENTORY_SNAPSHOT.clear()
    _MATCH_TIMELINES.clear()
    _MATCH_TIMELINE_KEYS.clear()
    _MATCH_HISTORY.clear()


def _load_json_dict(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _replace_mapping_contents(target: dict[Any, Any], values: dict[Any, Any]) -> None:
    target.clear()
    target.update(values)


def _restore_active_deck_state() -> None:
    loaded = _load_json_dict(ACTIVE_SUBMITTED_DECK_PATH)
    if not loaded:
        _ACTIVE_DECK_STATE.clear()
        return
    normalized = _normalize_active_deck_payload(loaded)
    _replace_mapping_contents(_ACTIVE_DECK_STATE, normalized)
    match_id = str(_ACTIVE_DECK_STATE.get("match_id", "")).strip()
    if match_id:
        _MATCH_DECK_CONTEXTS[match_id] = dict(_ACTIVE_DECK_STATE)


def _restore_match_history_state() -> None:
    loaded_history = _load_json_dict(MATCH_HISTORY_PATH)
    matches = loaded_history.get("matches") if isinstance(loaded_history, dict) else None
    if not isinstance(matches, list):
        _MATCH_HISTORY.clear()
        return
    restored = {
        str(item.get("match_id", "")).strip(): item
        for item in matches
        if isinstance(item, dict) and str(item.get("match_id", "")).strip()
    }
    _replace_mapping_contents(_MATCH_HISTORY, restored)


def bootstrap_runtime_surfaces() -> None:
    STATUS_TIMELINES_ROOT.mkdir(parents=True, exist_ok=True)
    _restore_active_deck_state()
    _restore_match_history_state()

    _write_deck_profile()
    _write_collection_profile()
    _write_match_history()
    _write_active_match_snapshot()


def _observe_deck_collection_payload(payload: dict[str, Any]) -> bool:
    decks = payload.get("decks") or {}
    if not isinstance(decks, dict):
        return False
    _DECK_COLLECTIONS.clear()
    _DECK_COLLECTIONS.update(decks)
    _write_deck_profile()
    _write_collection_profile()
    # Completed matches can gain deck metadata only after the collection
    # snapshot arrives, so refresh history when deck correlation changes.
    return True


def _observe_collection_payload(payload: dict[str, Any]) -> None:
    player_cards = payload.get("player_cards") or {}
    if not isinstance(player_cards, dict):
        return
    _PLAYER_CARD_COUNTS.clear()
    _PLAYER_CARD_COUNTS.update(_normalize_card_counts_map(player_cards))
    _write_collection_profile()
    _write_deck_profile()


def _observe_inventory_payload(payload: dict[str, Any]) -> None:
    inventory = payload.get("inventory") or {}
    if not isinstance(inventory, dict):
        return
    _INVENTORY_SNAPSHOT.clear()
    _INVENTORY_SNAPSHOT.update(inventory)
    _write_collection_profile()


def _observe_submit_deck_payload(event: Any, payload: dict[str, Any]) -> bool:
    active_deck = _normalize_active_deck_payload(
        {
            "submitted_at": _event_timestamp(event),
            "match_id": _event_match_id(event),
            "game_number": _event_game_number(event),
            "deck_cards": payload.get("deck_cards") or [],
            "sideboard_cards": payload.get("sideboard_cards") or [],
            "game_state_id": payload.get("game_state_id"),
            "resp_id": payload.get("resp_id"),
            "request_id": payload.get("request_id"),
        }
    )
    _ACTIVE_DECK_STATE.clear()
    _ACTIVE_DECK_STATE.update(active_deck)
    match_id = str(active_deck.get("match_id", "")).strip()
    if match_id:
        _MATCH_DECK_CONTEXTS[match_id] = dict(active_deck)
    _write_deck_profile()
    _write_collection_profile()
    return True


def _observe_runtime_surface_payload(event: Any) -> bool:
    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}

    if kind == "DeckCollection":
        return _observe_deck_collection_payload(payload)
    if kind == "Collection":
        _observe_collection_payload(payload)
        return False
    if kind == "Inventory":
        _observe_inventory_payload(payload)
        return False
    if kind == "Rank":
        # Rank snapshots often arrive after match completion, so completed history
        # rows need one more write to capture the enriched rank fields.
        return True
    if kind == "ClientAction" and payload.get("type") == "submit_deck_resp":
        return _observe_submit_deck_payload(event, payload)
    return False


def observe_event(event: Any, *, include_in_timeline: bool) -> None:
    kind = getattr(event, "kind", "")
    should_refresh_match_history = _observe_runtime_surface_payload(event)

    if include_in_timeline:
        timeline_entry = _build_timeline_entry(event)
        if timeline_entry is not None:
            _append_timeline_entry(timeline_entry)

    if kind in {"GameResult", "MatchState"}:
        should_refresh_match_history = True

    _write_active_match_snapshot()
    if should_refresh_match_history:
        _write_match_history()


def load_match_history_payload() -> dict[str, Any]:
    if MATCH_HISTORY_PATH.exists():
        try:
            payload = json.loads(MATCH_HISTORY_PATH.read_text(encoding="utf-8"))
        except Exception:
            payload = {}
        if isinstance(payload, dict):
            return payload
    return _build_match_history_payload()


def refresh_match_history_snapshot() -> dict[str, Any]:
    _write_match_history()
    return load_match_history_payload()


def load_active_timeline_payload(match_id: str = "") -> dict[str, Any]:
    normalized_match_id = str(match_id or "").strip()
    if normalized_match_id:
        timeline_path = STATUS_TIMELINES_ROOT / f"{normalized_match_id}.json"
        if timeline_path.exists():
            try:
                payload = json.loads(timeline_path.read_text(encoding="utf-8"))
            except Exception:
                payload = {}
            if isinstance(payload, dict):
                return payload

    if ACTIVE_MATCH_TIMELINE_PATH.exists():
        try:
            payload = json.loads(ACTIVE_MATCH_TIMELINE_PATH.read_text(encoding="utf-8"))
        except Exception:
            payload = {}
        if isinstance(payload, dict):
            return payload

    return {
        "object": "manasight_match_timeline",
        "generated_at": datetime.now(UTC).isoformat(),
        "match_id": normalized_match_id,
        "entries": [],
        "total_entries": 0,
    }


def filter_match_history_payload(payload: dict[str, Any], query: dict[str, str]) -> dict[str, Any]:
    matches = payload.get("matches") or []
    if not isinstance(matches, list):
        matches = []

    filtered = []
    for match in matches:
        if not isinstance(match, dict):
            continue
        if not _history_item_matches_query(match, query):
            continue
        filtered.append(match)

    limit_raw = query.get("limit", "")
    try:
        limit = max(int(limit_raw), 0) if limit_raw else 0
    except ValueError:
        limit = 0
    if limit:
        filtered = filtered[:limit]

    return {
        "object": "manasight_match_history",
        "generated_at": datetime.now(UTC).isoformat(),
        "filters_applied": {key: value for key, value in query.items() if value not in ("", None)},
        "total_matches": len(filtered),
        "matches": filtered,
        "available_filters": _build_history_filters(filtered),
    }


def _history_item_matches_query(item: dict[str, Any], query: dict[str, str]) -> bool:
    comparable_fields = {
        "match_id": str(item.get("match_id", "")),
        "deck_signature": str(item.get("deck", {}).get("signature", "")),
        "deck_name": str(item.get("deck", {}).get("name", "")),
        "format": str(item.get("mtga_format", "")),
        "queue_type": str(item.get("mtga_queue_type", "")),
        "result": str(item.get("result", "")),
        "event_id": str(item.get("event_id", "")),
        "rank_match_type": str(item.get("rank_match_type", "")),
        "play_mode_family": str(item.get("play_mode_family", "")),
        "event_family": str(item.get("event_family", "")),
        "queue_subtype": str(item.get("queue_subtype", "")),
        "date": str(item.get("date", "")),
    }
    for key, actual in comparable_fields.items():
        expected = str(query.get(key, "")).strip()
        if expected and actual != expected:
            return False
    return True


def _normalize_active_deck_payload(payload: dict[str, Any]) -> dict[str, Any]:
    deck_cards = _normalize_int_list(payload.get("deck_cards") or [])
    sideboard_cards = _normalize_int_list(payload.get("sideboard_cards") or [])
    return {
        "submitted_at": str(payload.get("submitted_at") or payload.get("updated_at") or "").strip(),
        "match_id": str(payload.get("match_id", "")).strip(),
        "game_number": payload.get("game_number", ""),
        "game_state_id": payload.get("game_state_id"),
        "resp_id": payload.get("resp_id"),
        "request_id": payload.get("request_id"),
        "deck_cards": deck_cards,
        "sideboard_cards": sideboard_cards,
        "mainboard_count": len(deck_cards),
        "sideboard_count": len(sideboard_cards),
        "signature": str(payload.get("signature") or submitted_deck_signature(deck_cards, sideboard_cards)),
    }


def _normalize_int_list(values: list[Any]) -> list[int]:
    normalized: list[int] = []
    for value in values:
        try:
            normalized.append(int(value))
        except (TypeError, ValueError):
            continue
    return normalized


def _normalize_card_counts_map(raw_counts: dict[Any, Any]) -> dict[str, int]:
    normalized: dict[str, int] = {}
    for raw_id, raw_count in raw_counts.items():
        try:
            card_id = str(int(raw_id))
            count = int(raw_count)
        except (TypeError, ValueError):
            continue
        if count <= 0:
            continue
        normalized[card_id] = count
    return normalized


def _card_lookup() -> dict[str, dict[str, Any]]:
    global _CARD_LOOKUP_CACHE
    if _CARD_LOOKUP_CACHE is not None:
        return _CARD_LOOKUP_CACHE
    try:
        _CARD_LOOKUP_CACHE = load_combined_card_lookup(format_key="arena")
    except Exception:
        _CARD_LOOKUP_CACHE = {}
    return _CARD_LOOKUP_CACHE


def _event_timestamp(event: Any) -> str:
    metadata = getattr(event, "metadata", None)
    if metadata is not None and getattr(metadata, "timestamp", None) is not None:
        return metadata.timestamp.isoformat()
    return ""


def _event_match_id(event: Any) -> str:
    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}

    if kind == "MatchState":
        return str(payload.get("match_id") or state._CONTEXT.get("current_match_id", "")).strip()
    if kind == "GameState":
        match_id, _, _, _, _, _, _ = _extract_turn_info(payload, state._CONTEXT)
        return str(match_id or state._CONTEXT.get("current_match_id", "")).strip()
    if kind == "GameResult":
        match_id, _, _, _, _ = _extract_game_result_identity(payload, state._CONTEXT)
        return str(match_id or state._CONTEXT.get("current_match_id", "")).strip()
    return str(state._CONTEXT.get("current_match_id", "")).strip()


def _event_game_number(event: Any) -> Any:
    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}

    if kind == "GameState":
        _, game_number, _, _, _, _, _ = _extract_turn_info(payload, state._CONTEXT)
        return game_number or state._CONTEXT.get("current_game_number", "")
    if kind == "GameResult":
        _, game_number, _, _, _ = _extract_game_result_identity(payload, state._CONTEXT)
        return game_number or state._CONTEXT.get("current_game_number", "")
    return state._CONTEXT.get("current_game_number", "")


def _build_timeline_entry(event: Any) -> dict[str, Any] | None:
    kind = getattr(event, "kind", "")
    payload = getattr(event, "payload", {}) or {}
    match_id = _event_match_id(event)
    if not match_id and kind not in {
        "ConnectionError",
        "TcpConnectionClose",
        "WebSocketClosed",
        "MatchConnectionState",
        "DetailedLoggingStatus",
    }:
        return None

    timestamp = _event_timestamp(event) or datetime.now(UTC).isoformat()
    entry: dict[str, Any] = {
        "timestamp": timestamp,
        "match_id": match_id,
        "game_number": _event_game_number(event),
        "event_kind": kind,
        "event_type": str(payload.get("type", "")),
        "summary": summarize(event),
    }

    if kind == "GameState":
        _, _, turn_number, active_player, phase, step, stage = _extract_turn_info(payload, state._CONTEXT)
        hand_instance_ids = _extract_local_private_hand_instance_ids(payload)
        entry.update(
            {
                "turn_number": turn_number,
                "active_player_seat_id": active_player,
                "phase": phase,
                "step": step,
                "stage": stage,
                "local_private_hand_size": len(hand_instance_ids) if hand_instance_ids else 0,
            }
        )
    elif kind == "GameResult":
        _, _, winner_team, result_type, reason = _extract_game_result_identity(payload, state._CONTEXT)
        entry.update(
            {
                "winner_team": winner_team,
                "result_type": result_type,
                "reason": reason,
            }
        )
    elif kind == "ClientAction":
        entry["message_type"] = str(payload.get("message_type", ""))
    elif kind == "MatchState":
        entry["state_type"] = str(payload.get("state_type", ""))
    elif kind == "Rank":
        entry["rank"] = str(payload.get("constructed_class", ""))

    return entry


def _append_timeline_entry(entry: dict[str, Any]) -> None:
    match_id = str(entry.get("match_id", "")).strip() or "session"
    key = json.dumps(
        {
            "timestamp": entry.get("timestamp"),
            "event_kind": entry.get("event_kind"),
            "summary": entry.get("summary"),
            "game_number": entry.get("game_number"),
            "turn_number": entry.get("turn_number"),
        },
        sort_keys=True,
        ensure_ascii=False,
    )

    seen_keys = _MATCH_TIMELINE_KEYS.setdefault(match_id, set())
    if key in seen_keys:
        return
    seen_keys.add(key)
    _MATCH_TIMELINES.setdefault(match_id, []).append(dict(entry))
    _write_timeline_payload(match_id)


def _write_timeline_payload(match_id: str) -> None:
    entries = _MATCH_TIMELINES.get(match_id, [])
    payload = {
        "object": "manasight_match_timeline",
        "generated_at": datetime.now(UTC).isoformat(),
        "match_id": match_id,
        "total_entries": len(entries),
        "entries": entries,
    }
    timeline_path = STATUS_TIMELINES_ROOT / f"{match_id}.json"
    _write_json(timeline_path, payload)

    current_match_id = str(state._CONTEXT.get("current_match_id", "")).strip()
    if current_match_id == match_id:
        _write_json(ACTIVE_MATCH_TIMELINE_PATH, payload)
        update_runtime_status(
            active_match_timeline_path=str(ACTIVE_MATCH_TIMELINE_PATH),
            active_match_timeline_entries=len(entries),
        )


def _write_active_match_snapshot() -> None:
    context = state.get_context_snapshot()
    current_match_id = str(context.get("current_match_id", "")).strip()
    summary = state.get_match_summary(current_match_id) if current_match_id else None
    deck_context = _MATCH_DECK_CONTEXTS.get(current_match_id) or _ACTIVE_DECK_STATE
    timeline_entries = _MATCH_TIMELINES.get(current_match_id, [])

    payload = {
        "object": "manasight_active_match_snapshot",
        "generated_at": datetime.now(UTC).isoformat(),
        "match_id": current_match_id,
        "current_game_number": context.get("current_game_number", ""),
        "current_player_team": context.get("current_player_team", ""),
        "summary": summary.to_debug_dict() if summary is not None else {},
        "deck": _deck_snapshot_brief(deck_context),
        "timeline_path": str(ACTIVE_MATCH_TIMELINE_PATH),
        "timeline_entries": len(timeline_entries),
    }
    _write_json(ACTIVE_MATCH_SNAPSHOT_PATH, payload)
    update_runtime_status(
        active_match_snapshot_path=str(ACTIVE_MATCH_SNAPSHOT_PATH),
        active_match_id=current_match_id,
        active_match_timeline_path=str(ACTIVE_MATCH_TIMELINE_PATH),
    )


def _build_match_history_payload() -> dict[str, Any]:
    matches = sorted(
        _MATCH_HISTORY.values(),
        key=lambda item: str(item.get("finished_at") or item.get("started_at") or ""),
        reverse=True,
    )
    return {
        "object": "manasight_match_history",
        "generated_at": datetime.now(UTC).isoformat(),
        "total_matches": len(matches),
        "matches": matches,
        "available_filters": _build_history_filters(matches),
    }


def _build_history_filters(matches: list[dict[str, Any]]) -> dict[str, list[str]]:
    def _values(path: tuple[str, ...]) -> list[str]:
        found = set()
        for item in matches:
            value: Any = item
            for key in path:
                if not isinstance(value, dict):
                    value = ""
                    break
                value = value.get(key, "")
            text = str(value or "").strip()
            if text:
                found.add(text)
        return sorted(found)

    return {
        "deck_names": _values(("deck", "name")),
        "deck_signatures": _values(("deck", "signature")),
        "formats": _values(("mtga_format",)),
        "queue_types": _values(("mtga_queue_type",)),
        "rank_match_types": _values(("rank_match_type",)),
        "play_mode_families": _values(("play_mode_family",)),
        "event_families": _values(("event_family",)),
        "queue_subtypes": _values(("queue_subtype",)),
        "results": _values(("result",)),
        "event_ids": _values(("event_id",)),
        "dates": _values(("date",)),
    }


def _write_match_history() -> None:
    for summary in state.iter_match_summaries():
        if not summary.is_ready():
            continue
        history_item = summary.to_history_item()
        deck_context = _MATCH_DECK_CONTEXTS.get(summary.match_id)
        history_item["deck"] = _deck_snapshot_brief(deck_context or {})
        history_item["timeline_path"] = str(STATUS_TIMELINES_ROOT / f"{summary.match_id}.json")
        _MATCH_HISTORY[summary.match_id] = history_item

    payload = _build_match_history_payload()
    _write_json(MATCH_HISTORY_PATH, payload)
    update_runtime_status(
        match_history_path=str(MATCH_HISTORY_PATH),
        match_history_total_matches=payload["total_matches"],
    )


def _deck_snapshot_brief(deck_context: dict[str, Any]) -> dict[str, Any]:
    if not deck_context:
        return {}
    matched = _match_active_deck_to_collection(deck_context)
    primary_match = matched[0] if matched else {}
    return {
        "signature": str(deck_context.get("signature", "")),
        "submitted_at": str(deck_context.get("submitted_at", "")),
        "mainboard_count": int(deck_context.get("mainboard_count", 0) or 0),
        "sideboard_count": int(deck_context.get("sideboard_count", 0) or 0),
        "name": primary_match.get("name", ""),
        "deck_id": primary_match.get("deck_id", ""),
        "format": primary_match.get("format", ""),
        "match_mode": primary_match.get("match_mode", ""),
    }


def _match_active_deck_to_collection(deck_context: dict[str, Any]) -> list[dict[str, Any]]:
    if not deck_context or not _DECK_COLLECTIONS:
        return []

    active_main = Counter(str(card_id) for card_id in deck_context.get("deck_cards") or [])
    active_side = Counter(str(card_id) for card_id in deck_context.get("sideboard_cards") or [])
    active_pool = active_main + active_side
    candidates: list[dict[str, Any]] = []

    for deck_id, deck_payload in _DECK_COLLECTIONS.items():
        if not isinstance(deck_payload, dict):
            continue
        main_counts = _deck_section_counts(deck_payload.get("list"), "MainDeck")
        side_counts = _deck_section_counts(deck_payload.get("list"), "Sideboard")
        if main_counts + side_counts != active_pool:
            continue
        match_mode = (
            "exact_mainboard" if main_counts == active_main and side_counts == active_side else "same_pool_sideboarded"
        )
        candidates.append(
            {
                "deck_id": str(deck_id),
                "name": str(deck_payload.get("Name", "")),
                "format": _deck_attribute(deck_payload, "Format"),
                "last_played": _deck_attribute(deck_payload, "LastPlayed"),
                "last_updated": _deck_attribute(deck_payload, "LastUpdated"),
                "is_favorite": _deck_attribute(deck_payload, "IsFavorite"),
                "match_mode": match_mode,
            }
        )

    candidates.sort(
        key=lambda item: (
            0 if item.get("match_mode") == "exact_mainboard" else 1,
            str(item.get("name", "")),
        )
    )
    return candidates


def _deck_attribute(deck_payload: dict[str, Any], name: str) -> str:
    for attribute in deck_payload.get("Attributes") or []:
        if not isinstance(attribute, dict):
            continue
        if attribute.get("name") == name:
            return str(attribute.get("value", ""))
    return ""


def _safe_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _deck_section_counts(deck_sections: Any, section_name: str) -> Counter[str]:
    if not isinstance(deck_sections, dict):
        return Counter()
    cards = deck_sections.get(section_name) or []
    counts: Counter[str] = Counter()
    if not isinstance(cards, list):
        return counts
    for card in cards:
        if not isinstance(card, dict):
            continue
        card_id_int = _safe_int(card.get("cardId"))
        quantity = _safe_int(card.get("quantity", 0))
        if card_id_int is None or quantity is None:
            continue
        card_id = str(card_id_int)
        if quantity > 0:
            counts[card_id] += quantity
    return counts


def _build_card_entry(card_id: str, count: int, *, section: str) -> dict[str, Any]:
    card = _card_lookup().get(card_id, {})
    colors = card.get("color_identity") or card.get("colors") or []
    type_line = str(card.get("type_line", "")).strip()
    return {
        "arena_id": int(card_id),
        "count": count,
        "section": section,
        "name": str(card.get("name", "")).strip(),
        "resolved": bool(str(card.get("name", "")).strip()),
        "rarity": str(card.get("rarity", "")).strip(),
        "set": str(card.get("set", "")).strip(),
        "set_name": str(card.get("set_name", "")).strip(),
        "mana_cost": str(card.get("mana_cost", "")).strip(),
        "cmc": card.get("cmc"),
        "type_line": type_line,
        "colors": list(colors) if isinstance(colors, list) else [],
    }


def _build_deck_profile() -> dict[str, Any]:
    deck_context = dict(_ACTIVE_DECK_STATE)
    mainboard_counts = Counter(str(card_id) for card_id in deck_context.get("deck_cards") or [])
    sideboard_counts = Counter(str(card_id) for card_id in deck_context.get("sideboard_cards") or [])
    mainboard = [
        _build_card_entry(card_id, count, section="mainboard") for card_id, count in sorted(mainboard_counts.items())
    ]
    sideboard = [
        _build_card_entry(card_id, count, section="sideboard") for card_id, count in sorted(sideboard_counts.items())
    ]
    matched_decks = _match_active_deck_to_collection(deck_context)
    missing_report = _build_missing_card_report(deck_context)

    return {
        "object": "manasight_active_deck_profile",
        "generated_at": datetime.now(UTC).isoformat(),
        "submitted_at": deck_context.get("submitted_at", ""),
        "match_id": deck_context.get("match_id", ""),
        "game_number": deck_context.get("game_number", ""),
        "signature": deck_context.get("signature", ""),
        "matched_decks": matched_decks,
        "stats": {
            "mainboard_count": sum(mainboard_counts.values()),
            "sideboard_count": sum(sideboard_counts.values()),
            "resolved_mainboard_cards": sum(1 for card in mainboard if card["resolved"]),
            "unresolved_mainboard_cards": sum(1 for card in mainboard if not card["resolved"]),
            "mana_curve": _mana_curve(mainboard),
            "type_counts": _type_counts(mainboard),
            "color_counts": _color_counts(mainboard),
            "rarity_counts": _rarity_counts(mainboard),
        },
        "mainboard": mainboard,
        "sideboard": sideboard,
        "collection_status": missing_report,
    }


def _write_deck_profile() -> None:
    payload = _build_deck_profile()
    _write_json(ACTIVE_DECK_PROFILE_PATH, payload)
    update_runtime_status(
        active_deck_profile_path=str(ACTIVE_DECK_PROFILE_PATH),
        active_deck_signature=payload.get("signature", ""),
        active_deck_name=(payload.get("matched_decks") or [{}])[0].get("name", ""),
    )


def _build_collection_profile() -> dict[str, Any]:
    inventory = _normalized_inventory(_INVENTORY_SNAPSHOT)
    missing_report = _build_missing_card_report(_ACTIVE_DECK_STATE)
    return {
        "object": "manasight_collection_profile",
        "generated_at": datetime.now(UTC).isoformat(),
        "collection_available": bool(_PLAYER_CARD_COUNTS),
        "inventory_available": bool(_INVENTORY_SNAPSHOT),
        "owned_unique_cards": len(_PLAYER_CARD_COUNTS),
        "owned_total_card_copies": sum(_PLAYER_CARD_COUNTS.values()),
        "owned_by_rarity": _owned_by_rarity(),
        "owned_by_set": _owned_by_set(),
        "inventory": inventory,
        "active_deck_missing_cards": missing_report["missing_cards"],
        "active_deck_missing_by_rarity": missing_report["missing_by_rarity"],
        "active_deck_completion": missing_report["completion"],
        "wanted_cards": missing_report["missing_cards"],
    }


def _write_collection_profile() -> None:
    payload = _build_collection_profile()
    _write_json(COLLECTION_PROFILE_PATH, payload)
    update_runtime_status(
        collection_profile_path=str(COLLECTION_PROFILE_PATH),
        collection_available=payload["collection_available"],
        inventory_available=payload["inventory_available"],
        collection_missing_active_deck_cards=len(payload["active_deck_missing_cards"]),
    )


def _build_missing_card_report(deck_context: dict[str, Any]) -> dict[str, Any]:
    required_counts = Counter(str(card_id) for card_id in deck_context.get("deck_cards") or [])
    required_counts.update(str(card_id) for card_id in deck_context.get("sideboard_cards") or [])
    total_required = sum(required_counts.values())
    if not required_counts:
        return {
            "missing_cards": [],
            "missing_by_rarity": {},
            "completion": {
                "owned_required_copies": 0,
                "total_required_copies": 0,
                "completion_rate": "",
            },
        }
    if not _PLAYER_CARD_COUNTS:
        return {
            "missing_cards": [],
            "missing_by_rarity": {},
            "completion": {
                "owned_required_copies": "",
                "total_required_copies": total_required,
                "completion_rate": "",
            },
        }

    missing_cards: list[dict[str, Any]] = []
    missing_by_rarity: dict[str, int] = defaultdict(int)
    owned_required_copies = 0

    for card_id, required_count in sorted(required_counts.items()):
        owned_count = int(_PLAYER_CARD_COUNTS.get(card_id, 0))
        owned_required_copies += min(owned_count, required_count)
        missing_count = max(required_count - owned_count, 0)
        if missing_count <= 0:
            continue
        card = _card_lookup().get(card_id, {})
        rarity = str(card.get("rarity", "")).strip() or "unknown"
        missing_by_rarity[rarity] += missing_count
        missing_cards.append(
            {
                "arena_id": int(card_id),
                "name": str(card.get("name", "")).strip(),
                "rarity": rarity,
                "required_count": required_count,
                "owned_count": owned_count,
                "missing_count": missing_count,
                "set": str(card.get("set", "")).strip(),
                "set_name": str(card.get("set_name", "")).strip(),
            }
        )

    completion_rate: float | str = ""
    if total_required > 0:
        completion_rate = owned_required_copies / total_required

    return {
        "missing_cards": missing_cards,
        "missing_by_rarity": dict(sorted(missing_by_rarity.items())),
        "completion": {
            "owned_required_copies": owned_required_copies,
            "total_required_copies": total_required,
            "completion_rate": completion_rate,
        },
    }


def _owned_by_rarity() -> dict[str, dict[str, int]]:
    buckets: dict[str, dict[str, int]] = defaultdict(lambda: {"unique_cards": 0, "copies": 0})
    for card_id, owned_count in _PLAYER_CARD_COUNTS.items():
        card = _card_lookup().get(card_id, {})
        rarity = str(card.get("rarity", "")).strip() or "unknown"
        buckets[rarity]["unique_cards"] += 1
        buckets[rarity]["copies"] += int(owned_count)
    return dict(sorted(buckets.items()))


def _owned_by_set() -> dict[str, dict[str, int]]:
    buckets: dict[str, dict[str, int]] = defaultdict(lambda: {"unique_cards": 0, "copies": 0})
    for card_id, owned_count in _PLAYER_CARD_COUNTS.items():
        card = _card_lookup().get(card_id, {})
        set_name = str(card.get("set_name", "")).strip() or str(card.get("set", "")).strip() or "unknown"
        buckets[set_name]["unique_cards"] += 1
        buckets[set_name]["copies"] += int(owned_count)
    return dict(sorted(buckets.items()))


def _normalized_inventory(inventory: dict[str, Any]) -> dict[str, Any]:
    return {
        "gold": _first_inventory_number(inventory, "gold", "Gold", "coins"),
        "gems": _first_inventory_number(inventory, "gems", "Gems", "crystals"),
        "wildcards_common": _first_inventory_number(
            inventory,
            "wcCommon",
            "wildCardCommons",
            "wildcardsCommon",
        ),
        "wildcards_uncommon": _first_inventory_number(
            inventory,
            "wcUncommon",
            "wildCardUnCommons",
            "wildcardsUncommon",
        ),
        "wildcards_rare": _first_inventory_number(
            inventory,
            "wcRare",
            "wildCardRares",
            "wildcardsRare",
        ),
        "wildcards_mythic": _first_inventory_number(
            inventory,
            "wcMythic",
            "wildCardMythics",
            "wildcardsMythic",
        ),
        "vault_progress": _first_inventory_number(inventory, "vaultProgress", "VaultProgress"),
        "raw_inventory": inventory,
    }


def _first_inventory_number(inventory: dict[str, Any], *keys: str) -> int | str:
    for key in keys:
        value = inventory.get(key)
        if value in (None, ""):
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return ""


def _mana_curve(cards: list[dict[str, Any]]) -> dict[str, int]:
    curve: Counter[str] = Counter()
    for card in cards:
        type_line = str(card.get("type_line", ""))
        if "Land" in type_line:
            continue
        count = int(card.get("count", 0) or 0)
        cmc = card.get("cmc")
        if cmc in (None, ""):
            curve["unknown"] += count
            continue
        try:
            cmc_label = str(int(float(cmc)))
        except (TypeError, ValueError):
            cmc_label = str(cmc)
        curve[cmc_label] += count
    return dict(sorted(curve.items(), key=lambda item: item[0]))


def _type_counts(cards: list[dict[str, Any]]) -> dict[str, int]:
    supported_types = (
        "Creature",
        "Land",
        "Instant",
        "Sorcery",
        "Artifact",
        "Enchantment",
        "Planeswalker",
        "Battle",
    )
    counts: Counter[str] = Counter()
    for card in cards:
        type_line = str(card.get("type_line", ""))
        card_count = int(card.get("count", 0) or 0)
        for type_name in supported_types:
            if type_name in type_line:
                counts[type_name] += card_count
    return dict(sorted(counts.items()))


def _color_counts(cards: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for card in cards:
        card_count = int(card.get("count", 0) or 0)
        colors = card.get("colors") or []
        if not isinstance(colors, list) or not colors:
            counts["Colorless"] += card_count
            continue
        for color in colors:
            counts[str(color)] += card_count
    return dict(sorted(counts.items()))


def _rarity_counts(cards: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for card in cards:
        rarity = str(card.get("rarity", "")).strip() or "unknown"
        counts[rarity] += int(card.get("count", 0) or 0)
    return dict(sorted(counts.items()))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    normalized_payload = _without_volatile_fields(payload)
    fingerprint = hashlib.sha1(
        json.dumps(normalized_payload, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    ).hexdigest()
    path_key = str(path)
    if _WRITE_FINGERPRINTS.get(path_key) == fingerprint and path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    _WRITE_FINGERPRINTS[path_key] = fingerprint


def _without_volatile_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_volatile_fields(item)
            for key, item in value.items()
            if key not in {"generated_at", "updated_at"}
        }
    if isinstance(value, list):
        return [_without_volatile_fields(item) for item in value]
    return value
