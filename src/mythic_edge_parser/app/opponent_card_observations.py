from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any

OPPONENT_CARD_OBSERVATION_OBJECT = "mythic_edge_opponent_card_observation"
OPPONENT_CARD_OBSERVATIONS_OBJECT = "mythic_edge_opponent_card_observations"
SCHEMA_VERSION = "parser_opponent_card_observations.v1"

ALLOWED_ACTION_TYPES = {
    "spell_cast",
    "land_played",
    "put_onto_battlefield_from_hand",
    "permanent_resolved",
    "permanent_left_battlefield",
    "permanent_died",
    "card_discarded",
    "spell_resolved_to_graveyard",
    "card_exiled",
    "zone_change",
    "object_revealed",
    "public_zone_presence",
    "unknown",
}
PUBLIC_ZONE_TYPES = {
    "ZoneType_Battlefield",
    "ZoneType_Command",
    "ZoneType_Exile",
    "ZoneType_Graveyard",
    "ZoneType_Limbo",
    "ZoneType_Revealed",
    "ZoneType_Stack",
}
ACTION_VISIBLE_TYPES = {
    "spell_cast",
    "land_played",
    "put_onto_battlefield_from_hand",
    "card_discarded",
    "object_revealed",
}
RESOLUTION_STATUS_MAP = {
    "": "unresolved",
    "exact_numeric_match": "resolved",
    "inferred_confirmed": "confirmed",
    "legacy_auto_promoted": "candidate",
    "confirmed": "confirmed",
    "resolved": "resolved",
    "candidate": "candidate",
    "unresolved": "unresolved",
    "contradicted": "contradicted",
    "ambiguous": "ambiguous",
    "name_only": "name_only",
}
_ACTION_SEAT_RE = re.compile(r"@seat(?P<seat_id>-?\d+)\b")


def build_opponent_card_observation(action_entry: Mapping[str, Any]) -> dict[str, Any] | None:
    if not isinstance(action_entry, Mapping):
        return None

    entry = dict(action_entry)
    if str(entry.get("actor_relation", "")).strip() != "opponent":
        return None

    local_seat_id = _safe_int(entry.get("local_seat_id"))
    actor_seat_id = _safe_int(entry.get("actor_seat_id"))
    action_seat_id = _action_seat_id(entry.get("raw_action_types"))
    if actor_seat_id is None:
        actor_seat_id = action_seat_id

    action_type = _normalized_action_type(entry.get("action_type"))
    if action_type is None:
        return None

    raw_action_types = _string_list(entry.get("raw_action_types"))
    annotation_types = _string_list(entry.get("annotation_types"))
    annotation_categories = _string_list(entry.get("annotation_categories"))
    from_zone_type = str(entry.get("from_zone_type") or "").strip()
    to_zone_type = str(entry.get("to_zone_type") or "").strip()
    visibility = _visibility(
        action_type=action_type,
        from_zone_type=from_zone_type,
        to_zone_type=to_zone_type,
        annotation_types=annotation_types,
        annotation_categories=annotation_categories,
    )

    if visibility == "hidden_not_recorded":
        return None

    observed_grp_id = _safe_int(entry.get("observed_grp_id"))
    overlay_grp_id = _safe_int(entry.get("overlay_grp_id"))
    object_source_grp_id = _safe_int(entry.get("object_source_grp_id"))
    parent_id = _safe_int(entry.get("parent_id"))
    grp_id = _safe_int(entry.get("grp_id"))
    if grp_id is None:
        grp_id = _first_int(object_source_grp_id, observed_grp_id, overlay_grp_id)

    identity_hint_source = str(entry.get("identity_hint_source") or "").strip()
    if not identity_hint_source:
        identity_hint_source = _identity_hint_source(
            grp_id=grp_id,
            observed_grp_id=observed_grp_id,
            overlay_grp_id=overlay_grp_id,
            object_source_grp_id=object_source_grp_id,
            parent_id=parent_id,
        )

    raw_resolution_status = str(entry.get("resolution_status") or "").strip()
    resolution_status = RESOLUTION_STATUS_MAP.get(raw_resolution_status, raw_resolution_status)
    if resolution_status not in set(RESOLUTION_STATUS_MAP.values()):
        resolution_status = "unresolved"

    card_name = str(entry.get("card_name") or "").strip()
    display_name = str(entry.get("display_name") or "").strip()
    if not display_name and grp_id is not None:
        display_name = f"[grpId {grp_id}]"

    degradation_flags = _degradation_flags(
        action_entry=entry,
        action_seat_id=action_seat_id,
        actor_seat_id=actor_seat_id,
        local_seat_id=local_seat_id,
        grp_id=grp_id,
        observed_grp_id=observed_grp_id,
        resolution_status=resolution_status,
        visibility=visibility,
    )
    evidence_status = _evidence_status(degradation_flags, resolution_status)
    value_source = _value_source(
        evidence_status,
        grp_id=grp_id,
        visibility=visibility,
        degradation_flags=degradation_flags,
    )
    confidence = _confidence(
        evidence_status=evidence_status,
        resolution_status=resolution_status,
        grp_id=grp_id,
        visibility=visibility,
        degradation_flags=degradation_flags,
    )

    return {
        "object": OPPONENT_CARD_OBSERVATION_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "match_id": str(entry.get("match_id") or "").strip(),
        "game_number": _safe_json_int(entry.get("game_number")),
        "game_state_id": _safe_json_int(entry.get("game_state_id")),
        "timestamp": str(entry.get("timestamp") or "").strip(),
        "turn_number": _safe_json_int(entry.get("turn_number")),
        "actor_relation": "opponent",
        "actor_seat_id": _safe_json_int(actor_seat_id),
        "local_seat_id": _safe_json_int(local_seat_id),
        "instance_id": _safe_json_int(entry.get("instance_id")),
        "grp_id": _safe_json_int(grp_id),
        "observed_grp_id": _safe_json_int(observed_grp_id),
        "overlay_grp_id": _safe_json_int(overlay_grp_id),
        "object_source_grp_id": _safe_json_int(object_source_grp_id),
        "parent_id": _safe_json_int(parent_id),
        "identity_hint_source": identity_hint_source,
        "card_name": card_name if resolution_status in {"resolved", "confirmed", "name_only"} else "",
        "display_name": display_name,
        "resolution_status": resolution_status,
        "name_resolution_source": _name_resolution_source(entry, raw_resolution_status),
        "layout": str(entry.get("layout") or "").strip(),
        "card_faces": _card_faces(entry.get("card_faces")),
        "action_type": action_type,
        "cast_mode": str(entry.get("cast_mode") or "").strip(),
        "source_evidence": _source_evidence(
            entry,
            raw_action_types=raw_action_types,
            annotation_types=annotation_types,
            annotation_categories=annotation_categories,
            visibility=visibility,
        ),
        "evidence_status": evidence_status,
        "value_source": value_source,
        "confidence": confidence,
        "visibility": visibility,
        "from_zone_type": from_zone_type,
        "to_zone_type": to_zone_type,
        "raw_action_types": raw_action_types,
        "annotation_types": annotation_types,
        "annotation_categories": annotation_categories,
        "degradation_flags": degradation_flags,
        "review_required": bool(degradation_flags or evidence_status in {"conflict", "degraded"}),
    }


def build_opponent_card_observations_payload(
    action_entries: Iterable[Mapping[str, Any]],
    *,
    match_id: str = "",
) -> dict[str, Any]:
    observations: list[dict[str, Any]] = []
    for action_entry in action_entries:
        observation = build_opponent_card_observation(action_entry)
        if observation is not None:
            observations.append(observation)

    normalized_match_id = str(match_id or "").strip()
    if not normalized_match_id and observations:
        normalized_match_id = str(observations[0].get("match_id") or "").strip()

    return {
        "object": OPPONENT_CARD_OBSERVATIONS_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "match_id": normalized_match_id,
        "total_observations": len(observations),
        "degraded_observations": sum(1 for observation in observations if observation.get("degradation_flags")),
        "review_required": any(bool(observation.get("review_required")) for observation in observations),
        "observations": observations,
    }


def _safe_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _safe_json_int(value: Any) -> int | str:
    normalized = _safe_int(value)
    return normalized if normalized is not None else ""


def _first_int(*values: int | None) -> int | None:
    for value in values:
        if value is not None:
            return value
    return None


def _string_list(value: Any) -> list[str]:
    raw_values = value if isinstance(value, list) else [value]
    normalized: list[str] = []
    for raw_value in raw_values:
        text = str(raw_value or "").strip()
        if text and text not in normalized:
            normalized.append(text)
    return normalized


def _card_faces(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    faces: list[str] = []
    for raw_face in value:
        if isinstance(raw_face, str):
            text = raw_face.strip()
        elif isinstance(raw_face, Mapping):
            text = str(raw_face.get("name") or "").strip()
        else:
            text = ""
        if text and text not in faces:
            faces.append(text)
    return faces


def _action_seat_id(raw_action_types: Any) -> int | None:
    for action_type in _string_list(raw_action_types):
        match = _ACTION_SEAT_RE.search(action_type)
        if match:
            return _safe_int(match.group("seat_id"))
    return None


def _normalized_action_type(value: Any) -> str | None:
    action_type = str(value or "").strip()
    if action_type in ALLOWED_ACTION_TYPES:
        return action_type
    if not action_type:
        return "unknown"
    return None


def _visibility(
    *,
    action_type: str,
    from_zone_type: str,
    to_zone_type: str,
    annotation_types: list[str],
    annotation_categories: list[str],
) -> str:
    if action_type == "card_drawn":
        if _has_reveal_evidence(annotation_types, annotation_categories) or to_zone_type in PUBLIC_ZONE_TYPES:
            return "revealed"
        return "hidden_not_recorded"
    if action_type == "object_revealed" or _has_reveal_evidence(annotation_types, annotation_categories):
        return "revealed"
    if action_type in ACTION_VISIBLE_TYPES:
        return "action_visible"
    if action_type == "public_zone_presence" or to_zone_type in PUBLIC_ZONE_TYPES:
        return "public_zone"
    if from_zone_type in PUBLIC_ZONE_TYPES or to_zone_type in PUBLIC_ZONE_TYPES:
        return "derived_zone_transition"
    return "ambiguous"


def _has_reveal_evidence(annotation_types: list[str], annotation_categories: list[str]) -> bool:
    return any("Reveal" in value or "Revealed" in value for value in (*annotation_types, *annotation_categories))


def _identity_hint_source(
    *,
    grp_id: int | None,
    observed_grp_id: int | None,
    overlay_grp_id: int | None,
    object_source_grp_id: int | None,
    parent_id: int | None,
) -> str:
    if object_source_grp_id is not None and grp_id == object_source_grp_id:
        return "object_source_grp_id"
    if parent_id is not None and grp_id is not None:
        return "parent_chain"
    if observed_grp_id is not None and grp_id == observed_grp_id:
        return "direct_grp_id"
    if overlay_grp_id is not None and grp_id == overlay_grp_id:
        return "overlay_grp_id"
    return "missing"


def _degradation_flags(
    *,
    action_entry: dict[str, Any],
    action_seat_id: int | None,
    actor_seat_id: int | None,
    local_seat_id: int | None,
    grp_id: int | None,
    observed_grp_id: int | None,
    resolution_status: str,
    visibility: str,
) -> list[str]:
    flags: list[str] = []
    if actor_seat_id is None or local_seat_id is None:
        flags.append("missing_seat_mapping")
    elif actor_seat_id == local_seat_id:
        flags.append("actor_relation_conflict")
    if action_seat_id is not None and action_seat_id != actor_seat_id:
        flags.append("action_seat_conflict")
    if grp_id is None and observed_grp_id is None:
        flags.append("missing_card_identity")
    if resolution_status in {"candidate", "ambiguous", "contradicted", "name_only"}:
        flags.append(f"name_resolution_{resolution_status}")
    if resolution_status == "unresolved" and grp_id is None and observed_grp_id is None:
        flags.append("name_resolution_unresolved")
    if visibility == "ambiguous":
        flags.append("ambiguous_visibility")
    if bool(action_entry.get("data_loss")) or bool(action_entry.get("truncated")):
        flags.append("data_loss_evidence")
    return sorted(dict.fromkeys(flags))


def _evidence_status(degradation_flags: list[str], resolution_status: str) -> str:
    if any(flag.endswith("_conflict") or "contradicted" in flag for flag in degradation_flags):
        return "conflict"
    if any(
        flag in degradation_flags
        for flag in ("data_loss_evidence", "missing_card_identity", "missing_seat_mapping")
    ):
        return "degraded"
    if resolution_status in {"candidate", "ambiguous", "name_only"}:
        return "observed"
    return "observed"


def _value_source(
    evidence_status: str,
    *,
    grp_id: int | None,
    visibility: str,
    degradation_flags: list[str],
) -> str:
    if evidence_status == "conflict":
        return "conflict"
    if evidence_status == "degraded":
        if "missing_seat_mapping" in degradation_flags:
            return "unknown"
        return "unknown" if grp_id is None else "derived"
    if visibility == "derived_zone_transition":
        return "derived"
    return "observed"


def _confidence(
    *,
    evidence_status: str,
    resolution_status: str,
    grp_id: int | None,
    visibility: str,
    degradation_flags: list[str],
) -> str:
    if evidence_status == "conflict":
        return "low"
    if "missing_seat_mapping" in degradation_flags:
        return "low"
    if "missing_card_identity" in degradation_flags:
        return "low"
    if visibility == "ambiguous":
        return "low"
    if resolution_status in {"contradicted", "ambiguous", "name_only"}:
        return "low"
    if resolution_status == "candidate":
        return "medium"
    if grp_id is not None and evidence_status == "observed":
        return "high"
    return "unknown"


def _name_resolution_source(entry: dict[str, Any], raw_resolution_status: str) -> str:
    explicit = str(entry.get("name_resolution_source") or "").strip()
    if explicit:
        return explicit
    if raw_resolution_status:
        return f"gameplay_action_entry:{raw_resolution_status}"
    if entry.get("display_name") or entry.get("card_name"):
        return "gameplay_action_entry"
    return "unknown"


def _source_evidence(
    entry: dict[str, Any],
    *,
    raw_action_types: list[str],
    annotation_types: list[str],
    annotation_categories: list[str],
    visibility: str,
) -> str:
    explicit = str(entry.get("source_evidence") or "").strip()
    if explicit:
        return explicit
    sources: list[str] = []
    if raw_action_types:
        sources.append("action_array")
    if annotation_types or annotation_categories:
        sources.append("annotation")
    if visibility == "derived_zone_transition":
        sources.append("zone_transition")
    if visibility == "public_zone":
        sources.append("object_presence_public_zone")
    if not sources:
        sources.append("gameplay_action_entry")
    unique_sources = sorted(dict.fromkeys(sources))
    return unique_sources[0] if len(unique_sources) == 1 else "mixed"
