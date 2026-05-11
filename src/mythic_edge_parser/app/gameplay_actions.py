from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import state
from .config import (
    ACTIVE_DECK_PROFILE_PATH,
    ACTIVE_MATCH_ACTION_LOG_PATH,
    ACTIVE_MATCH_ACTIONS_PATH,
    GRP_ID_CATALOG_PATH,
    STATUS_ACTIONS_ROOT,
)
from .diagnostics import update_runtime_status
from .extractors import (
    _game_state_actions,
    _game_state_annotations,
    _game_state_objects,
    _game_state_system_seat_ids,
    _game_state_zones,
    _hydrate_game_state_identity,
)
from .grp_id_catalog import (
    bootstrap_grp_id_catalog,
    observe_gameplay_objects,
    resolve_grp_id_entry,
)


@dataclass(slots=True)
class GameplayGameState:
    match_id: str
    game_number: int
    local_seat_id: int | None = None
    last_turn_number: int | None = None
    last_active_player_seat_id: int | None = None
    zones_by_id: dict[int, dict[str, Any]] = field(default_factory=dict)
    objects_by_instance: dict[int, dict[str, Any]] = field(default_factory=dict)


@dataclass(slots=True)
class GameplayActionStore:
    game_states: dict[tuple[str, int], GameplayGameState] = field(default_factory=dict)
    match_actions: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    match_action_keys: dict[str, set[str]] = field(default_factory=dict)
    dirty_match_ids: set[str] = field(default_factory=set)


@dataclass(slots=True)
class ActiveDeckIdentityIndex:
    cache_key: tuple[str, int | None]
    payload: dict[str, Any]
    exact_names_by_arena_id: dict[int, str]
    all_names: set[str]


@dataclass(slots=True)
class GameplayEventContext:
    match_id: str
    game_number: int
    game_state_id: int | None
    timestamp: str
    turn_number: int | None
    annotation_types: list[str]
    action_types_by_instance: dict[int, list[str]]
    annotation_categories_by_instance: dict[int, list[str]]
    replacement_instance_ids: dict[int, int]
    replacement_source_ids: dict[int, int]


ACTION_STORE = GameplayActionStore()
_GAME_STATES = ACTION_STORE.game_states
_MATCH_ACTIONS = ACTION_STORE.match_actions
_MATCH_ACTION_KEYS = ACTION_STORE.match_action_keys
_DIRTY_MATCH_IDS = ACTION_STORE.dirty_match_ids
_JSON_DICT_CACHE: dict[tuple[str, int | None], dict[str, Any]] = {}
_ACTIVE_DECK_INDEX: ActiveDeckIdentityIndex | None = None


def bootstrap_gameplay_actions() -> None:
    STATUS_ACTIONS_ROOT.mkdir(parents=True, exist_ok=True)
    bootstrap_grp_id_catalog()
    update_runtime_status(
        grp_id_catalog_path=str(GRP_ID_CATALOG_PATH),
        active_match_actions_path=str(ACTIVE_MATCH_ACTIONS_PATH),
        active_match_action_log_path=str(ACTIVE_MATCH_ACTION_LOG_PATH),
    )


def reset_gameplay_actions_state() -> None:
    global _ACTIVE_DECK_INDEX

    _GAME_STATES.clear()
    _MATCH_ACTIONS.clear()
    _MATCH_ACTION_KEYS.clear()
    _DIRTY_MATCH_IDS.clear()
    _JSON_DICT_CACHE.clear()
    _ACTIVE_DECK_INDEX = None


def observe_event(event: Any) -> None:
    if getattr(event, "kind", "") != "GameState":
        return
    _observe_game_state(event)


def load_active_match_actions_payload(match_id: str = "") -> dict[str, Any]:
    normalized_match_id = str(match_id or "").strip()
    if normalized_match_id:
        payload_path = STATUS_ACTIONS_ROOT / f"{normalized_match_id}.json"
        if payload_path.exists():
            payload = _load_json_dict(payload_path)
            if isinstance(payload, dict):
                return payload

    if ACTIVE_MATCH_ACTIONS_PATH.exists():
        payload = _load_json_dict(ACTIVE_MATCH_ACTIONS_PATH)
        if isinstance(payload, dict):
            return payload

    return {
        "object": "manasight_match_actions",
        "generated_at": datetime.now(UTC).isoformat(),
        "match_id": normalized_match_id,
        "entries": [],
        "total_entries": 0,
    }


def _safe_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _clean_string_list(raw_values: Any) -> list[str]:
    values = raw_values if isinstance(raw_values, list) else [raw_values]
    found: list[str] = []
    for raw_value in values:
        text = str(raw_value or "").strip()
        if text:
            found.append(text)
    return found


def _extend_unique_strings(target: list[str], values: list[str]) -> None:
    for value in values:
        if value not in target:
            target.append(value)


def _event_timestamp(event: Any) -> str:
    metadata = getattr(event, "metadata", None)
    if metadata is not None and getattr(metadata, "timestamp", None) is not None:
        return metadata.timestamp.isoformat()
    return datetime.now(UTC).isoformat()


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


def _prime_json_dict_cache(path: Path, payload: dict[str, Any]) -> None:
    cache_key = _path_cache_key(path)
    _drop_cached_path(path)
    _JSON_DICT_CACHE[cache_key] = payload


def _game_state_id(payload: dict[str, Any]) -> int | None:
    return _safe_int(payload.get("game_state_id") or payload.get("msg_id"))


def _normalize_zone(zone: dict[str, Any]) -> dict[str, Any] | None:
    zone_id = _safe_int(zone.get("zoneId") or zone.get("zone_id"))
    if zone_id is None:
        return None
    return {
        "zone_id": zone_id,
        "zone_type": str(zone.get("type") or zone.get("zone_type") or "").strip(),
        "visibility": str(zone.get("visibility") or "").strip(),
        "owner_seat_id": _safe_int(zone.get("ownerSeatId") or zone.get("owner_seat_id")),
        "object_instance_ids": [
            instance_id
            for raw_instance_id in (zone.get("objectInstanceIds") or zone.get("object_instance_ids") or [])
            if (instance_id := _safe_int(raw_instance_id)) is not None
        ],
    }


def _normalize_game_object(game_object: dict[str, Any]) -> dict[str, Any] | None:
    instance_id = _safe_int(game_object.get("instanceId") or game_object.get("instance_id"))
    if instance_id is None:
        return None

    grp_id = _safe_int(game_object.get("grpId") or game_object.get("grp_id"))
    overlay_grp_id = _safe_int(game_object.get("overlayGrpId") or game_object.get("overlay_grp_id"))
    object_source_grp_id = _safe_int(game_object.get("objectSourceGrpId") or game_object.get("object_source_grp_id"))
    primary_grp_id = grp_id or overlay_grp_id or object_source_grp_id

    return {
        "instance_id": instance_id,
        "grp_id": primary_grp_id,
        "raw_grp_id": grp_id,
        "overlay_grp_id": overlay_grp_id,
        "object_source_grp_id": object_source_grp_id,
        "parent_id": _safe_int(game_object.get("parentId") or game_object.get("parent_id")),
        "zone_id": _safe_int(game_object.get("zoneId") or game_object.get("zone_id")),
        "owner_seat_id": _safe_int(game_object.get("ownerSeatId") or game_object.get("owner_seat_id")),
        "controller_seat_id": _safe_int(game_object.get("controllerSeatId") or game_object.get("controller_seat_id")),
        "object_type": str(game_object.get("type") or game_object.get("object_type") or "").strip(),
        "visibility": str(game_object.get("visibility") or "").strip(),
        "name_key": str(game_object.get("name") or "").strip(),
        "object_types": _clean_string_list([game_object.get("type") or game_object.get("object_type") or ""]),
        "card_types": _clean_string_list(game_object.get("cardTypes") or game_object.get("card_types") or []),
        "super_types": _clean_string_list(game_object.get("superTypes") or game_object.get("super_types") or []),
        "subtypes": _clean_string_list(game_object.get("subtypes") or []),
        "colors": _clean_string_list(game_object.get("color") or game_object.get("colors") or []),
        "power": str(game_object.get("power") or "").strip(),
        "toughness": str(game_object.get("toughness") or "").strip(),
    }


def _chain_grp_id_candidates(game_object: dict[str, Any]) -> list[int]:
    candidates: list[int] = []
    for raw_candidate in (
        game_object.get("object_source_grp_id"),
        game_object.get("raw_grp_id"),
        game_object.get("overlay_grp_id"),
        game_object.get("grp_id"),
    ):
        candidate = _safe_int(raw_candidate)
        if candidate is not None and candidate not in candidates:
            candidates.append(candidate)
    return candidates


def _resolve_canonical_grp_id(
    gameplay_state: GameplayGameState,
    objects_by_instance: dict[int, dict[str, Any]],
    game_object: dict[str, Any],
    *,
    replacement_source_id: int | None = None,
) -> tuple[int | None, str]:
    object_source_grp_id = _safe_int(game_object.get("object_source_grp_id"))
    if object_source_grp_id is not None:
        return object_source_grp_id, "object_source_grp_id"

    parent_id = _safe_int(game_object.get("parent_id"))
    if parent_id is not None:
        parent_object = objects_by_instance.get(parent_id) or gameplay_state.objects_by_instance.get(parent_id)
        if isinstance(parent_object, dict):
            for candidate in _chain_grp_id_candidates(parent_object):
                return candidate, "parent_chain"

    instance_id = _safe_int(game_object.get("instance_id"))
    if instance_id is not None:
        prior_object = gameplay_state.objects_by_instance.get(instance_id)
        if isinstance(prior_object, dict):
            prior_canonical_grp_id = _safe_int(prior_object.get("grp_id"))
            prior_raw_grp_id = _safe_int(prior_object.get("raw_grp_id"))
            current_raw_grp_id = _safe_int(game_object.get("raw_grp_id"))
            if prior_canonical_grp_id is not None and prior_canonical_grp_id != (
                current_raw_grp_id or prior_raw_grp_id
            ):
                return prior_canonical_grp_id, "prior_instance"

    if replacement_source_id is not None:
        source_object = gameplay_state.objects_by_instance.get(replacement_source_id)
        if isinstance(source_object, dict):
            source_canonical_grp_id = _safe_int(source_object.get("grp_id"))
            if source_canonical_grp_id is not None:
                return source_canonical_grp_id, "replacement_chain"

    for candidate in _chain_grp_id_candidates(game_object):
        return candidate, "direct_grp_id"
    return None, "missing"


def _normalize_action_instance_map(payload: dict[str, Any]) -> dict[int, list[str]]:
    actions_by_instance: dict[int, list[str]] = {}
    for outer_action in _game_state_actions(payload):
        seat_id = _safe_int(outer_action.get("seatId") or outer_action.get("seat_id"))
        inner = outer_action.get("action") or {}
        if not isinstance(inner, dict):
            continue
        action_type = str(inner.get("actionType") or inner.get("action_type") or "").strip()
        instance_id = _safe_int(inner.get("instanceId") or inner.get("instance_id"))
        if not action_type or instance_id is None:
            continue
        rows = actions_by_instance.setdefault(instance_id, [])
        label = action_type if seat_id is None else f"{action_type}@seat{seat_id}"
        if label not in rows:
            rows.append(label)
    return actions_by_instance


def _annotation_types(payload: dict[str, Any]) -> list[str]:
    found: list[str] = []
    for annotation in _game_state_annotations(payload):
        _extend_unique_strings(found, _clean_string_list(annotation.get("type") or []))
    return found


def _annotation_int_detail_values(annotation: dict[str, Any], key: str) -> list[int]:
    values: list[int] = []
    for detail in annotation.get("details") or []:
        if not isinstance(detail, dict):
            continue
        if str(detail.get("key") or "").strip() != key:
            continue
        for raw_value in detail.get("valueInt32") or []:
            value = _safe_int(raw_value)
            if value is not None:
                values.append(value)
    return values


def _annotation_string_detail_values(annotation: dict[str, Any], key: str) -> list[str]:
    values: list[str] = []
    for detail in annotation.get("details") or []:
        if not isinstance(detail, dict):
            continue
        if str(detail.get("key") or "").strip() != key:
            continue
        _extend_unique_strings(values, _clean_string_list(detail.get("valueString") or []))
    return values


def _annotation_instance_hints(payload: dict[str, Any]) -> tuple[dict[int, list[str]], dict[int, int]]:
    categories_by_instance: dict[int, list[str]] = {}
    replacement_instance_ids: dict[int, int] = {}

    for annotation in _game_state_annotations(payload):
        annotation_types = set(_clean_string_list(annotation.get("type") or []))
        affected_ids = [
            affected_id
            for raw_affected_id in (annotation.get("affectedIds") or [])
            if (affected_id := _safe_int(raw_affected_id)) is not None
        ]

        if "AnnotationType_ZoneTransfer" in annotation_types:
            categories = _annotation_string_detail_values(annotation, "category")
            if categories:
                for affected_id in affected_ids:
                    rows = categories_by_instance.setdefault(affected_id, [])
                    for category in categories:
                        if category not in rows:
                            rows.append(category)

        if "AnnotationType_ObjectIdChanged" in annotation_types:
            original_ids = _annotation_int_detail_values(annotation, "orig_id")
            new_ids = _annotation_int_detail_values(annotation, "new_id")
            if original_ids and new_ids:
                replacement_instance_ids[original_ids[0]] = new_ids[0]

    return categories_by_instance, replacement_instance_ids


def _has_spell_like_annotation(annotation_categories: list[str]) -> bool:
    return any(str(category or "").strip().startswith("Cast") for category in annotation_categories)


def _has_resolution_annotation(annotation_types: list[str], annotation_categories: list[str]) -> bool:
    resolution_types = {
        "AnnotationType_ResolutionStart",
        "AnnotationType_ResolutionComplete",
    }
    return any(annotation_type in resolution_types for annotation_type in annotation_types) or (
        "Resolve" in annotation_categories
    )


def _zone_label(game_state: GameplayGameState, zone_id: int | None) -> str:
    if zone_id is None:
        return ""
    zone = game_state.zones_by_id.get(zone_id) or {}
    return str(zone.get("zone_type", "")).strip()


def _actor_relation(game_state: GameplayGameState, game_object: dict[str, Any]) -> str:
    local_seat_id = game_state.local_seat_id
    controller_seat_id = _safe_int(game_object.get("controller_seat_id"))
    owner_seat_id = _safe_int(game_object.get("owner_seat_id"))
    actor_seat_id = controller_seat_id if controller_seat_id is not None else owner_seat_id
    if local_seat_id is None or actor_seat_id is None:
        return "unknown"
    return "local" if local_seat_id == actor_seat_id else "opponent"


def _classify_zone_transition(
    *,
    previous_zone_type: str,
    current_zone_type: str,
    card_types: list[str],
) -> str:
    if previous_zone_type == "ZoneType_Hand" and current_zone_type == "ZoneType_Stack":
        return "spell_cast"
    if previous_zone_type == "ZoneType_Hand" and current_zone_type == "ZoneType_Battlefield":
        if "CardType_Land" in card_types:
            return "land_played"
        return "put_onto_battlefield_from_hand"
    if previous_zone_type == "ZoneType_Stack" and current_zone_type == "ZoneType_Battlefield":
        return "permanent_resolved"
    if previous_zone_type == "ZoneType_Library" and current_zone_type == "ZoneType_Hand":
        return "card_drawn"
    if previous_zone_type == "ZoneType_Battlefield" and current_zone_type == "ZoneType_Limbo":
        return "permanent_left_battlefield"
    if previous_zone_type == "ZoneType_Battlefield" and current_zone_type == "ZoneType_Graveyard":
        return "permanent_died"
    if previous_zone_type == "ZoneType_Hand" and current_zone_type == "ZoneType_Graveyard":
        return "card_discarded"
    if previous_zone_type == "ZoneType_Stack" and current_zone_type == "ZoneType_Graveyard":
        return "spell_resolved_to_graveyard"
    if current_zone_type == "ZoneType_Exile":
        return "card_exiled"
    return "zone_change"


def _action_type_present(action_types: list[str], prefix: str) -> bool:
    return any(str(action_type or "").startswith(prefix) for action_type in action_types)


def _infer_action_from_partial_diff(
    *,
    previous_zone_type: str,
    current_zone_type: str,
    card_types: list[str],
    raw_action_types: list[str],
    annotation_categories: list[str],
    annotation_types: list[str],
) -> tuple[str, str]:
    inferred_target_zone = current_zone_type
    has_cast = _action_type_present(raw_action_types, "ActionType_Cast")
    has_play = _action_type_present(raw_action_types, "ActionType_Play")
    is_from_hand = previous_zone_type in ("", "ZoneType_Hand")
    spell_like_annotation = _has_spell_like_annotation(annotation_categories)

    if has_cast and is_from_hand and current_zone_type in ("ZoneType_Limbo", "ZoneType_Stack"):
        if current_zone_type == "ZoneType_Limbo":
            inferred_target_zone = "ZoneType_Stack"
        return "spell_cast", inferred_target_zone

    if (
        spell_like_annotation
        and previous_zone_type in ("ZoneType_Hand", "ZoneType_Exile", "ZoneType_Graveyard")
        and current_zone_type == "ZoneType_Limbo"
    ):
        return "spell_cast", "ZoneType_Stack"

    if (
        previous_zone_type == "ZoneType_Stack"
        and current_zone_type == "ZoneType_Limbo"
        and _has_resolution_annotation(annotation_types, annotation_categories)
    ):
        return "spell_finished", current_zone_type

    if (
        has_play
        and "CardType_Land" in card_types
        and is_from_hand
        and current_zone_type in ("ZoneType_Limbo", "ZoneType_Battlefield")
    ):
        if current_zone_type == "ZoneType_Limbo":
            inferred_target_zone = "ZoneType_Battlefield"
        return "land_played", inferred_target_zone

    if (
        "PlayLand" in annotation_categories
        and "CardType_Land" in card_types
        and previous_zone_type == "ZoneType_Hand"
        and current_zone_type == "ZoneType_Limbo"
    ):
        return "land_played", "ZoneType_Battlefield"

    return "", current_zone_type


def _same_canonical_grp_id(left_object: dict[str, Any] | None, right_object: dict[str, Any] | None) -> bool:
    if not isinstance(left_object, dict) or not isinstance(right_object, dict):
        return False
    return _safe_int(left_object.get("grp_id")) is not None and _safe_int(left_object.get("grp_id")) == _safe_int(
        right_object.get("grp_id")
    )


def _should_skip_replacement_followup(
    *,
    gameplay_state: GameplayGameState,
    normalized_by_instance: dict[int, dict[str, Any]],
    normalized_object: dict[str, Any],
    replacement_source_id: int | None,
    previous_object: dict[str, Any] | None,
    current_zone_type: str,
) -> bool:
    if previous_object is not None or replacement_source_id is None:
        return False
    source_current_object = normalized_by_instance.get(replacement_source_id)
    source_previous_object = gameplay_state.objects_by_instance.get(replacement_source_id)
    if not _same_canonical_grp_id(normalized_object, source_current_object):
        return False
    source_current_zone_type = _zone_label(gameplay_state, _safe_int((source_current_object or {}).get("zone_id")))
    source_previous_zone_type = _zone_label(gameplay_state, _safe_int((source_previous_object or {}).get("zone_id")))
    if source_current_zone_type != "ZoneType_Limbo":
        return False
    if current_zone_type == "ZoneType_Battlefield" and source_previous_zone_type == "ZoneType_Hand":
        return True
    if current_zone_type == "ZoneType_Stack" and source_previous_zone_type in (
        "ZoneType_Hand",
        "ZoneType_Exile",
        "ZoneType_Graveyard",
    ):
        return True
    return False


def _should_skip_shadow_child_transition(
    *,
    normalized_by_instance: dict[int, dict[str, Any]],
    normalized_object: dict[str, Any],
    current_zone_id: int | None,
) -> bool:
    parent_id = _safe_int(normalized_object.get("parent_id"))
    if parent_id is None or current_zone_id is None:
        return False
    parent_object = normalized_by_instance.get(parent_id)
    if not _same_canonical_grp_id(normalized_object, parent_object):
        return False
    return _safe_int((parent_object or {}).get("zone_id")) == current_zone_id


def _should_skip_reveal_cleanup_transition(
    *,
    previous_zone_type: str,
    current_zone_type: str,
    annotation_types: list[str],
    annotation_categories: list[str],
    raw_action_types: list[str],
) -> bool:
    return (
        previous_zone_type == "ZoneType_Hand"
        and current_zone_type == "ZoneType_Limbo"
        and "AnnotationType_RevealedCardDeleted" in annotation_types
        and not raw_action_types
        and not _has_spell_like_annotation(annotation_categories)
    )


def _should_skip_support_object_transition(
    *,
    normalized_object: dict[str, Any],
    previous_zone_type: str,
    current_zone_type: str,
    raw_action_types: list[str],
) -> bool:
    return (
        previous_zone_type == "ZoneType_Pending"
        and current_zone_type == "ZoneType_Stack"
        and not raw_action_types
        and (
            _safe_int(normalized_object.get("object_source_grp_id")) is not None
            or _safe_int(normalized_object.get("parent_id")) is not None
        )
    )


def _action_key(entry: dict[str, Any]) -> str:
    return json.dumps(
        {
            "game_state_id": entry.get("game_state_id"),
            "game_number": entry.get("game_number"),
            "turn_number": entry.get("turn_number"),
            "action_type": entry.get("action_type"),
            "instance_id": entry.get("instance_id"),
            "grp_id": entry.get("grp_id"),
            "from_zone_type": entry.get("from_zone_type"),
            "to_zone_type": entry.get("to_zone_type"),
        },
        sort_keys=True,
        ensure_ascii=False,
    )


def _append_match_action(entry: dict[str, Any]) -> None:
    match_id = str(entry.get("match_id", "")).strip()
    if not match_id:
        return
    key = _action_key(entry)
    seen_keys = _MATCH_ACTION_KEYS.setdefault(match_id, set())
    if key in seen_keys:
        return
    seen_keys.add(key)
    _MATCH_ACTIONS.setdefault(match_id, []).append(dict(entry))
    _DIRTY_MATCH_IDS.add(match_id)


def _summary_for_entry(entry: dict[str, Any], display_name: str) -> str:
    actor = {
        "local": "You",
        "opponent": "Opponent",
    }.get(str(entry.get("actor_relation", "")).strip(), "A player")
    action_type = str(entry.get("action_type", "")).strip()
    cast_mode = str(entry.get("cast_mode", "")).strip().replace("_", " ")
    if cast_mode:
        display_name = f"{display_name} ({cast_mode})"

    from_zone_type = str(entry.get("from_zone_type", "")).strip()
    from_zone_label = {
        "ZoneType_Hand": "hand",
        "ZoneType_Exile": "exile",
        "ZoneType_Graveyard": "graveyard",
        "ZoneType_Library": "library",
    }.get(from_zone_type, "")

    if action_type == "turn_started":
        turn_number = entry.get("turn_number")
        if turn_number not in (None, ""):
            return f"Turn {turn_number} started"
        return "A new turn started"
    if action_type == "spell_cast":
        if from_zone_label:
            return f"{actor} cast {display_name} from {from_zone_label} to stack"
        return f"{actor} cast {display_name} to stack"
    if action_type == "spell_finished":
        return f"{display_name} finished resolving and left the stack"
    if action_type == "land_played":
        return f"{actor} played {display_name} from hand to battlefield"
    if action_type == "put_onto_battlefield_from_hand":
        return f"{actor} moved {display_name} from hand to battlefield"
    if action_type == "permanent_resolved":
        return f"{display_name} resolved onto the battlefield"
    if action_type == "permanent_left_battlefield":
        return f"{display_name} left the battlefield"
    if action_type == "card_drawn":
        return f"{actor} drew {display_name}"
    if action_type == "permanent_died":
        return f"{display_name} moved from battlefield to graveyard"
    if action_type == "card_discarded":
        return f"{actor} discarded {display_name}"
    if action_type == "spell_resolved_to_graveyard":
        return f"{display_name} moved from stack to graveyard"
    if action_type == "card_exiled":
        return f"{display_name} moved to exile"
    return (
        f"{display_name} moved from {entry.get('from_zone_type', '') or 'unknown'} "
        f"to {entry.get('to_zone_type', '') or 'unknown'}"
    )


def _infer_cast_mode(
    *,
    grp_id: Any,
    action_type: str,
    card_types: list[str],
    to_zone_type: str,
    raw_action_types: list[str],
    object_type: str,
    subtypes: list[str],
) -> str:
    if action_type != "spell_cast":
        return ""
    if _action_type_present(raw_action_types, "ActionType_CastAdventure"):
        return "adventure_face"
    if str(object_type or "").strip() == "GameObjectType_Adventure":
        return "adventure_face"
    if "SubType_Adventure" in subtypes:
        return "adventure_face"
    catalog_entry = resolve_grp_id_entry(grp_id) if grp_id not in (None, "") else {}
    if str(catalog_entry.get("resolved_layout", "")).strip() != "adventure":
        return ""
    if "CardType_Creature" in card_types or to_zone_type == "ZoneType_Battlefield":
        return "main_face"
    if "CardType_Sorcery" in card_types or "CardType_Instant" in card_types or to_zone_type == "ZoneType_Stack":
        return "adventure_face"
    return ""


def _build_active_deck_identity_index(payload: dict[str, Any]) -> ActiveDeckIdentityIndex:
    exact_names_by_arena_id: dict[int, str] = {}
    all_names: set[str] = set()
    for row in _active_deck_rows(payload):
        arena_id = _safe_int(row.get("arena_id"))
        name = str(row.get("name", "")).strip()
        if arena_id is not None and name and arena_id not in exact_names_by_arena_id:
            exact_names_by_arena_id[arena_id] = name
        all_names.update(_card_name_aliases(name))
    return ActiveDeckIdentityIndex(
        cache_key=_path_cache_key(ACTIVE_DECK_PROFILE_PATH),
        payload=payload,
        exact_names_by_arena_id=exact_names_by_arena_id,
        all_names=all_names,
    )


def _active_deck_identity_index() -> ActiveDeckIdentityIndex:
    global _ACTIVE_DECK_INDEX

    cache_key = _path_cache_key(ACTIVE_DECK_PROFILE_PATH)
    if _ACTIVE_DECK_INDEX is not None and _ACTIVE_DECK_INDEX.cache_key == cache_key:
        return _ACTIVE_DECK_INDEX

    payload = _load_json_dict(ACTIVE_DECK_PROFILE_PATH)
    _ACTIVE_DECK_INDEX = _build_active_deck_identity_index(payload)
    return _ACTIVE_DECK_INDEX


def _card_name_aliases(name: str) -> set[str]:
    normalized = str(name or "").strip()
    aliases: set[str] = set()
    if not normalized:
        return aliases
    aliases.add(normalized)
    for part in normalized.split("//"):
        alias = part.strip()
        if alias:
            aliases.add(alias)
    return aliases


def _active_deck_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in ("mainboard", "sideboard"):
        raw_rows = payload.get(key) or []
        if not isinstance(raw_rows, list):
            continue
        for row in raw_rows:
            if isinstance(row, dict):
                rows.append(row)
    return rows


def _best_grp_id_from_entry(entry: dict[str, Any]) -> int | None:
    for raw_value in (
        entry.get("grp_id"),
        entry.get("object_source_grp_id"),
        entry.get("observed_grp_id"),
    ):
        grp_id = _safe_int(raw_value)
        if grp_id is not None:
            return grp_id
    return None


def _resolved_identity_for_entry(
    entry: dict[str, Any],
    *,
    deck_index: ActiveDeckIdentityIndex | None = None,
) -> tuple[int | None, dict[str, Any], str, str]:
    grp_id = _best_grp_id_from_entry(entry)
    catalog_entry = resolve_grp_id_entry(grp_id) if grp_id is not None else {}
    actor_relation = str(entry.get("actor_relation", "")).strip()
    local_deck_index = deck_index if actor_relation == "local" else None
    if local_deck_index is None and actor_relation == "local":
        local_deck_index = _active_deck_identity_index()
    deck_name = (
        local_deck_index.exact_names_by_arena_id.get(grp_id, "")
        if local_deck_index is not None and grp_id is not None
        else ""
    )
    deck_names = local_deck_index.all_names if local_deck_index is not None else set()

    resolved_name = str(catalog_entry.get("resolved_name", "")).strip() if catalog_entry else ""
    display_name = str(catalog_entry.get("display_name", "")).strip() if catalog_entry else ""
    candidate_name = ""
    candidate_rows = catalog_entry.get("candidate_names") or []
    if isinstance(candidate_rows, list) and candidate_rows:
        first = candidate_rows[0]
        if isinstance(first, dict):
            candidate_name = str(first.get("name", "")).strip()

    if deck_name:
        return grp_id, catalog_entry, deck_name, resolved_name or deck_name

    if resolved_name:
        return grp_id, catalog_entry, resolved_name, resolved_name

    if candidate_name:
        if actor_relation != "local" or not deck_names or candidate_name in deck_names:
            return grp_id, catalog_entry, f"{candidate_name}? [grpId {grp_id}]", ""
        display_name = ""

    if not display_name and grp_id is not None:
        display_name = f"[grpId {grp_id}]"
    return grp_id, catalog_entry, display_name, resolved_name


def _is_visible_in_action_log(entry: dict[str, Any]) -> bool:
    action_type = str(entry.get("action_type", "")).strip()
    if action_type == "turn_started":
        return True
    if _best_grp_id_from_entry(entry) is not None:
        return True
    display_name = str(entry.get("display_name", "")).strip()
    return bool(display_name)


def _render_entry(
    entry: dict[str, Any],
    *,
    deck_index: ActiveDeckIdentityIndex | None = None,
) -> dict[str, Any]:
    grp_id, catalog_entry, display_name, resolved_name = _resolved_identity_for_entry(
        entry,
        deck_index=deck_index,
    )
    if not display_name:
        display_name = f"[grpId {grp_id}]" if grp_id is not None else ""

    rendered = dict(entry)
    rendered["grp_id"] = grp_id if grp_id is not None else rendered.get("grp_id", "")
    rendered["card_name"] = resolved_name
    rendered["display_name"] = display_name
    rendered["resolution_status"] = str(catalog_entry.get("resolution_status", "")).strip() if catalog_entry else ""
    rendered["layout"] = str(catalog_entry.get("resolved_layout", "")).strip() if catalog_entry else ""
    rendered["card_faces"] = list(catalog_entry.get("resolved_card_faces") or []) if catalog_entry else []
    rendered["visible_in_log"] = _is_visible_in_action_log(rendered)
    rendered["summary"] = _summary_for_entry(entry, display_name)
    return rendered


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Gameplay Action Log",
        "",
        f"- Match ID: `{payload.get('match_id', '')}`",
        f"- Generated at: `{payload.get('generated_at', '')}`",
        f"- Total entries: `{payload.get('total_entries', 0)}`",
        "",
        "| Time | Game | Turn | Action | Card | From | To | Summary |",
        "|---|---:|---:|---|---|---|---|---|",
    ]
    entries = payload.get("entries") or []
    if not isinstance(entries, list) or not entries:
        lines.append("|  |  |  |  |  |  |  | No gameplay actions recorded yet. |")
        return "\n".join(lines) + "\n"

    visible_entries = [
        entry for entry in entries if isinstance(entry, dict) and bool(entry.get("visible_in_log", True))
    ]
    if not visible_entries:
        lines.append("|  |  |  |  |  |  |  | No visible gameplay actions recorded yet. |")
        return "\n".join(lines) + "\n"

    for entry in visible_entries:
        if not isinstance(entry, dict):
            continue
        lines.append(
            (
                "| {timestamp} | {game_number} | {turn_number} | {action_type} | "
                "{display_name} | {from_zone} | {to_zone} | {summary} |"
            ).format(
                timestamp=str(entry.get("timestamp", "")).replace("|", "/"),
                game_number=entry.get("game_number", ""),
                turn_number=entry.get("turn_number", ""),
                action_type=str(entry.get("action_type", "")).replace("|", "/"),
                display_name=str(entry.get("display_name", "")).replace("|", "/"),
                from_zone=str(entry.get("from_zone_type", "")).replace("|", "/"),
                to_zone=str(entry.get("to_zone_type", "")).replace("|", "/"),
                summary=str(entry.get("summary", "")).replace("|", "/"),
            )
        )
    return "\n".join(lines) + "\n"


def _write_match_actions(match_id: str) -> None:
    raw_entries = _MATCH_ACTIONS.get(match_id, [])
    deck_index = _active_deck_identity_index()
    rendered_entries = [_render_entry(entry, deck_index=deck_index) for entry in raw_entries]
    payload = {
        "object": "manasight_match_actions",
        "generated_at": datetime.now(UTC).isoformat(),
        "match_id": match_id,
        "total_entries": len(rendered_entries),
        "visible_entry_count": sum(1 for entry in rendered_entries if entry.get("visible_in_log", True)),
        "entries": rendered_entries,
    }
    STATUS_ACTIONS_ROOT.mkdir(parents=True, exist_ok=True)
    json_path = STATUS_ACTIONS_ROOT / f"{match_id}.json"
    markdown_path = STATUS_ACTIONS_ROOT / f"{match_id}.md"
    json_text = json.dumps(payload, indent=2, ensure_ascii=False)
    markdown_text = _render_markdown(payload)
    json_path.write_text(json_text, encoding="utf-8")
    markdown_path.write_text(markdown_text, encoding="utf-8")
    _prime_json_dict_cache(json_path, payload)

    current_match_id = str(state._CONTEXT.get("current_match_id", "")).strip()
    if current_match_id == match_id:
        ACTIVE_MATCH_ACTIONS_PATH.write_text(json_text, encoding="utf-8")
        ACTIVE_MATCH_ACTION_LOG_PATH.write_text(markdown_text, encoding="utf-8")
        _prime_json_dict_cache(ACTIVE_MATCH_ACTIONS_PATH, payload)
        update_runtime_status(
            active_match_actions_path=str(ACTIVE_MATCH_ACTIONS_PATH),
            active_match_action_log_path=str(ACTIVE_MATCH_ACTION_LOG_PATH),
            active_match_action_count=len(rendered_entries),
        )


def _flush_match_actions(match_id: str) -> None:
    if match_id not in _DIRTY_MATCH_IDS:
        return
    _write_match_actions(match_id)
    _DIRTY_MATCH_IDS.discard(match_id)


def _maybe_emit_turn_started(
    *,
    match_id: str,
    game_number: int,
    game_state_id: int | None,
    timestamp: str,
    turn_number: int | None,
    annotation_types: list[str],
) -> None:
    if "AnnotationType_NewTurnStarted" not in annotation_types:
        return
    _append_match_action(
        {
            "timestamp": timestamp,
            "match_id": match_id,
            "game_number": game_number,
            "game_state_id": game_state_id,
            "turn_number": turn_number,
            "action_type": "turn_started",
            "instance_id": "",
            "grp_id": "",
            "actor_relation": "",
            "from_zone_type": "",
            "to_zone_type": "",
            "raw_action_types": [],
            "annotation_types": annotation_types,
        }
    )


def _ensure_gameplay_state(match_id: str, game_number: int) -> GameplayGameState:
    game_key = (match_id, game_number)
    return _GAME_STATES.setdefault(
        game_key,
        GameplayGameState(match_id=match_id, game_number=game_number),
    )


def _update_known_zones(gameplay_state: GameplayGameState, payload: dict[str, Any]) -> None:
    for raw_zone in _game_state_zones(payload):
        zone = _normalize_zone(raw_zone)
        if zone is None:
            continue
        gameplay_state.zones_by_id[zone["zone_id"]] = zone


def _update_turn_tracking(gameplay_state: GameplayGameState, identity: dict[str, Any]) -> int | None:
    turn_number = _safe_int(identity.get("turn_number"))
    if turn_number is None:
        return gameplay_state.last_turn_number
    gameplay_state.last_turn_number = turn_number
    return turn_number


def _update_active_player_tracking(gameplay_state: GameplayGameState, identity: dict[str, Any]) -> None:
    active_player_seat_id = _safe_int(identity.get("active_player_seat_id"))
    if active_player_seat_id is not None:
        gameplay_state.last_active_player_seat_id = active_player_seat_id


def _build_gameplay_event_context(
    event: Any,
    payload: dict[str, Any],
    identity: dict[str, Any],
    gameplay_state: GameplayGameState,
    *,
    match_id: str,
    game_number: int,
) -> GameplayEventContext:
    annotation_categories_by_instance, replacement_instance_ids = _annotation_instance_hints(payload)
    return GameplayEventContext(
        match_id=match_id,
        game_number=game_number,
        game_state_id=_game_state_id(payload),
        timestamp=_event_timestamp(event),
        turn_number=_update_turn_tracking(gameplay_state, identity),
        annotation_types=_annotation_types(payload),
        action_types_by_instance=_normalize_action_instance_map(payload),
        annotation_categories_by_instance=annotation_categories_by_instance,
        replacement_instance_ids=replacement_instance_ids,
        replacement_source_ids={new_id: original_id for original_id, new_id in replacement_instance_ids.items()},
    )


def _observed_card_payload(
    gameplay_state: GameplayGameState,
    normalized_object: dict[str, Any],
) -> dict[str, Any]:
    return {
        "grp_id": _safe_int(normalized_object.get("grp_id")),
        "observed_grp_id": normalized_object.get("observed_grp_id"),
        "overlay_grp_id": normalized_object.get("overlay_grp_id"),
        "object_source_grp_id": normalized_object.get("object_source_grp_id"),
        "zone_type": _zone_label(gameplay_state, normalized_object.get("zone_id")),
        "name_key": normalized_object.get("name_key"),
        "object_types": list(normalized_object.get("object_types") or []),
        "card_types": list(normalized_object.get("card_types") or []),
        "super_types": list(normalized_object.get("super_types") or []),
        "subtypes": list(normalized_object.get("subtypes") or []),
        "colors": list(normalized_object.get("colors") or []),
        "action_types": [],
    }


def _normalize_payload_objects(
    gameplay_state: GameplayGameState,
    payload: dict[str, Any],
    replacement_source_ids: dict[int, int],
) -> tuple[list[dict[str, Any]], dict[int, dict[str, Any]], list[dict[str, Any]]]:
    normalized_objects: list[dict[str, Any]] = []
    for raw_object in _game_state_objects(payload):
        normalized_object = _normalize_game_object(raw_object)
        if normalized_object is not None:
            normalized_objects.append(normalized_object)

    normalized_by_instance = {
        instance_id: normalized_object
        for normalized_object in normalized_objects
        if (instance_id := _safe_int(normalized_object.get("instance_id"))) is not None
    }

    observed_cards: list[dict[str, Any]] = []
    seen_grp_ids: set[int] = set()
    for normalized_object in normalized_objects:
        instance_id = _safe_int(normalized_object.get("instance_id"))
        canonical_grp_id, identity_source = _resolve_canonical_grp_id(
            gameplay_state,
            normalized_by_instance,
            normalized_object,
            replacement_source_id=replacement_source_ids.get(instance_id or -1),
        )
        normalized_object["observed_grp_id"] = normalized_object.get("grp_id")
        normalized_object["grp_id"] = canonical_grp_id
        normalized_object["identity_hint_source"] = identity_source

        grp_id = _safe_int(normalized_object.get("grp_id"))
        if grp_id is None or grp_id in seen_grp_ids:
            continue
        seen_grp_ids.add(grp_id)
        observed_cards.append(_observed_card_payload(gameplay_state, normalized_object))

    return normalized_objects, normalized_by_instance, observed_cards


def _record_observed_action_types(
    observed_cards: list[dict[str, Any]],
    normalized_object: dict[str, Any],
    raw_action_types: list[str],
) -> None:
    grp_id = _safe_int(normalized_object.get("grp_id"))
    if grp_id is None:
        return
    for observed_card in observed_cards:
        if _safe_int(observed_card.get("grp_id")) != grp_id:
            continue
        _extend_unique_strings(observed_card["action_types"], raw_action_types)
        return


def _annotation_categories_for_instance(
    instance_id: int,
    event_context: GameplayEventContext,
) -> list[str]:
    categories = list(event_context.annotation_categories_by_instance.get(instance_id, []))
    replacement_instance_id = event_context.replacement_instance_ids.get(instance_id)
    if replacement_instance_id is not None:
        _extend_unique_strings(
            categories,
            list(event_context.annotation_categories_by_instance.get(replacement_instance_id, [])),
        )
    return categories


def _build_object_action_entry(
    *,
    event_context: GameplayEventContext,
    gameplay_state: GameplayGameState,
    normalized_object: dict[str, Any],
    instance_id: int,
    action_type: str,
    from_zone_type: str,
    to_zone_type: str,
    raw_action_types: list[str],
) -> dict[str, Any]:
    return {
        "timestamp": event_context.timestamp,
        "match_id": event_context.match_id,
        "game_number": event_context.game_number,
        "game_state_id": event_context.game_state_id,
        "turn_number": event_context.turn_number,
        "action_type": action_type,
        "cast_mode": _infer_cast_mode(
            grp_id=normalized_object.get("grp_id"),
            action_type=action_type,
            card_types=list(normalized_object.get("card_types") or []),
            to_zone_type=to_zone_type,
            raw_action_types=raw_action_types,
            object_type=str(normalized_object.get("object_type", "")).strip(),
            subtypes=list(normalized_object.get("subtypes") or []),
        ),
        "instance_id": instance_id,
        "grp_id": normalized_object.get("grp_id"),
        "observed_grp_id": normalized_object.get("observed_grp_id"),
        "object_source_grp_id": normalized_object.get("object_source_grp_id"),
        "parent_id": normalized_object.get("parent_id"),
        "identity_hint_source": normalized_object.get("identity_hint_source"),
        "actor_relation": _actor_relation(gameplay_state, normalized_object),
        "from_zone_type": from_zone_type,
        "to_zone_type": to_zone_type,
        "raw_action_types": raw_action_types,
        "annotation_types": event_context.annotation_types,
    }


def _observe_new_object_transition(
    *,
    event_context: GameplayEventContext,
    gameplay_state: GameplayGameState,
    normalized_by_instance: dict[int, dict[str, Any]],
    normalized_object: dict[str, Any],
    instance_id: int,
    replacement_source_id: int | None,
    current_zone_type: str,
    raw_action_types: list[str],
    annotation_categories: list[str],
) -> None:
    if _should_skip_replacement_followup(
        gameplay_state=gameplay_state,
        normalized_by_instance=normalized_by_instance,
        normalized_object=normalized_object,
        replacement_source_id=replacement_source_id,
        previous_object=None,
        current_zone_type=current_zone_type,
    ):
        return

    inferred_action_type, inferred_zone_type = _infer_action_from_partial_diff(
        previous_zone_type="",
        current_zone_type=current_zone_type,
        card_types=list(normalized_object.get("card_types") or []),
        raw_action_types=raw_action_types,
        annotation_categories=annotation_categories,
        annotation_types=event_context.annotation_types,
    )
    if not inferred_action_type:
        return

    _append_match_action(
        _build_object_action_entry(
            event_context=event_context,
            gameplay_state=gameplay_state,
            normalized_object=normalized_object,
            instance_id=instance_id,
            action_type=inferred_action_type,
            from_zone_type="",
            to_zone_type=inferred_zone_type,
            raw_action_types=raw_action_types,
        )
    )


def _observe_zone_transition(
    *,
    event_context: GameplayEventContext,
    gameplay_state: GameplayGameState,
    normalized_by_instance: dict[int, dict[str, Any]],
    normalized_object: dict[str, Any],
    previous_object: dict[str, Any],
    instance_id: int,
    current_zone_id: int | None,
    current_zone_type: str,
    raw_action_types: list[str],
    annotation_categories: list[str],
) -> None:
    previous_zone_id = _safe_int(previous_object.get("zone_id"))
    if current_zone_id == previous_zone_id:
        return

    previous_zone_type = _zone_label(gameplay_state, previous_zone_id)
    if _should_skip_shadow_child_transition(
        normalized_by_instance=normalized_by_instance,
        normalized_object=normalized_object,
        current_zone_id=current_zone_id,
    ):
        return
    if _should_skip_reveal_cleanup_transition(
        previous_zone_type=previous_zone_type,
        current_zone_type=current_zone_type,
        annotation_types=event_context.annotation_types,
        annotation_categories=annotation_categories,
        raw_action_types=raw_action_types,
    ):
        return
    if _should_skip_support_object_transition(
        normalized_object=normalized_object,
        previous_zone_type=previous_zone_type,
        current_zone_type=current_zone_type,
        raw_action_types=raw_action_types,
    ):
        return

    inferred_action_type, inferred_zone_type = _infer_action_from_partial_diff(
        previous_zone_type=previous_zone_type,
        current_zone_type=current_zone_type,
        card_types=list(normalized_object.get("card_types") or []),
        raw_action_types=raw_action_types,
        annotation_categories=annotation_categories,
        annotation_types=event_context.annotation_types,
    )
    action_type = inferred_action_type or _classify_zone_transition(
        previous_zone_type=previous_zone_type,
        current_zone_type=current_zone_type,
        card_types=list(normalized_object.get("card_types") or []),
    )
    to_zone_type = inferred_zone_type if inferred_action_type else current_zone_type
    _append_match_action(
        _build_object_action_entry(
            event_context=event_context,
            gameplay_state=gameplay_state,
            normalized_object=normalized_object,
            instance_id=instance_id,
            action_type=action_type,
            from_zone_type=previous_zone_type,
            to_zone_type=to_zone_type,
            raw_action_types=raw_action_types,
        )
    )


def _observe_normalized_object(
    *,
    gameplay_state: GameplayGameState,
    event_context: GameplayEventContext,
    normalized_by_instance: dict[int, dict[str, Any]],
    normalized_object: dict[str, Any],
    observed_cards: list[dict[str, Any]],
) -> None:
    instance_id = _safe_int(normalized_object.get("instance_id"))
    if instance_id is None:
        return

    raw_action_types = event_context.action_types_by_instance.get(instance_id, [])
    _record_observed_action_types(observed_cards, normalized_object, raw_action_types)

    annotation_categories = _annotation_categories_for_instance(instance_id, event_context)
    replacement_source_id = event_context.replacement_source_ids.get(instance_id)
    previous_object = gameplay_state.objects_by_instance.get(instance_id)
    gameplay_state.objects_by_instance[instance_id] = dict(previous_object or {}, **normalized_object)

    current_zone_id = _safe_int(normalized_object.get("zone_id"))
    current_zone_type = _zone_label(gameplay_state, current_zone_id)
    if previous_object is None:
        _observe_new_object_transition(
            event_context=event_context,
            gameplay_state=gameplay_state,
            normalized_by_instance=normalized_by_instance,
            normalized_object=normalized_object,
            instance_id=instance_id,
            replacement_source_id=replacement_source_id,
            current_zone_type=current_zone_type,
            raw_action_types=raw_action_types,
            annotation_categories=annotation_categories,
        )
        return

    _observe_zone_transition(
        event_context=event_context,
        gameplay_state=gameplay_state,
        normalized_by_instance=normalized_by_instance,
        normalized_object=normalized_object,
        previous_object=previous_object,
        instance_id=instance_id,
        current_zone_id=current_zone_id,
        current_zone_type=current_zone_type,
        raw_action_types=raw_action_types,
        annotation_categories=annotation_categories,
    )


def _observe_game_state(event: Any) -> None:
    payload = getattr(event, "payload", {}) or {}
    identity = _hydrate_game_state_identity(payload, state._CONTEXT)
    match_id = str(identity.get("match_id") or "").strip()
    game_number = _safe_int(identity.get("game_number"))
    if not match_id or game_number is None:
        return

    gameplay_state = _ensure_gameplay_state(match_id, game_number)

    system_seat_ids = _game_state_system_seat_ids(payload)
    if system_seat_ids:
        gameplay_state.local_seat_id = system_seat_ids[0]
    _update_known_zones(gameplay_state, payload)

    _update_active_player_tracking(gameplay_state, identity)
    event_context = _build_gameplay_event_context(
        event,
        payload,
        identity,
        gameplay_state,
        match_id=match_id,
        game_number=game_number,
    )

    _maybe_emit_turn_started(
        match_id=event_context.match_id,
        game_number=event_context.game_number,
        game_state_id=event_context.game_state_id,
        timestamp=event_context.timestamp,
        turn_number=event_context.turn_number,
        annotation_types=event_context.annotation_types,
    )

    normalized_objects, normalized_by_instance, observed_cards = _normalize_payload_objects(
        gameplay_state,
        payload,
        event_context.replacement_source_ids,
    )

    for normalized_object in normalized_objects:
        _observe_normalized_object(
            gameplay_state=gameplay_state,
            event_context=event_context,
            normalized_by_instance=normalized_by_instance,
            normalized_object=normalized_object,
            observed_cards=observed_cards,
        )
    observe_gameplay_objects(
        observed_cards,
        timestamp=event_context.timestamp,
        match_id=event_context.match_id,
        game_number=event_context.game_number,
    )
    _flush_match_actions(event_context.match_id)
