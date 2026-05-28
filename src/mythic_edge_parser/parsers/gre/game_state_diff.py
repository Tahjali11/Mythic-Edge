from __future__ import annotations

from collections.abc import Mapping

GAME_STATE_DIFF_MECHANICS_OBJECT = "mythic_edge_gre_game_state_diff_mechanics"
SCHEMA_VERSION = "parser_gre_game_state_diff_mechanics.v1"

_SECTION_KEYS = (
    ("players", "players"),
    ("zones", "zones"),
    ("game_objects", "gameObjects"),
    ("annotations", "annotations"),
    ("persistent_annotations", "persistentAnnotations"),
    ("timers", "timers"),
    ("actions", "actions"),
)


def build_game_state_diff_mechanics(
    *,
    message: Mapping[str, object],
    gsm: Mapping[str, object],
    payload_type: str,
    game_state_id: object,
    update: str,
    pending_message_count: int | None,
    prev_game_state_id: int | None,
    diff_deleted_instance_ids: list[int],
    diff_deleted_persistent_annotation_ids: list[int],
) -> dict[str, object]:
    source_fields_used = _source_fields_used(message, gsm)
    update_raw = _update_raw(gsm.get("update"), source_fields_used["update"])
    update_kind = _update_kind(update_raw)
    degradation_flags = _degradation_flags_for_update(update_kind, update_raw, source_fields_used["update"])
    state_completeness, is_complete_snapshot = _state_completeness(update_kind)
    raw_game_state_id = gsm.get("gameStateId") if "gameStateId" in gsm else message.get("gameStateId")
    game_state_id_normalized = _strict_id(raw_game_state_id)
    if source_fields_used["gameStateId"] and game_state_id_normalized == "":
        _append_flag(degradation_flags, "malformed_game_state_id")

    normalized_prev_game_state_id = prev_game_state_id if prev_game_state_id is not None else ""
    if source_fields_used["prevGameStateId"] and prev_game_state_id is None:
        _append_flag(degradation_flags, "malformed_prev_game_state_id")
    prev_status = _linkage_status(
        update_kind=update_kind,
        game_state_id_normalized=game_state_id_normalized,
        prev_game_state_id=prev_game_state_id,
        prev_present=source_fields_used["prevGameStateId"],
        prev_malformed="malformed_prev_game_state_id" in degradation_flags,
    )
    _add_linkage_flags(degradation_flags, prev_status)
    if source_fields_used["pendingMessageCount"] and pending_message_count is None:
        _append_flag(degradation_flags, "malformed_pending_message_count")
    if pending_message_count is not None and pending_message_count < 0:
        _append_flag(degradation_flags, "negative_pending_message_count")
    if source_fields_used["diffDeletedInstanceIds"] and not isinstance(gsm.get("diffDeletedInstanceIds"), list):
        _append_flag(degradation_flags, "malformed_diff_deleted_instance_ids")
    if source_fields_used["diffDeletedPersistentAnnotationIds"] and not isinstance(
        gsm.get("diffDeletedPersistentAnnotationIds"), list
    ):
        _append_flag(degradation_flags, "malformed_diff_deleted_persistent_annotation_ids")
    if bool(gsm.get("truncation_or_data_loss_evidence")):
        _append_flag(degradation_flags, "truncation_or_data_loss_evidence")

    evidence_status = _evidence_status(degradation_flags, update_kind)
    value_source = _value_source(evidence_status, update_kind)
    deletion_counts = {
        "instance_ids": len(diff_deleted_instance_ids),
        "persistent_annotation_ids": len(diff_deleted_persistent_annotation_ids),
    }
    return {
        "object": GAME_STATE_DIFF_MECHANICS_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "source_payload_type": payload_type,
        "message_type": str(message.get("type") or ""),
        "queued": payload_type == "queued_game_state_message",
        "game_state_id": game_state_id,
        "game_state_id_normalized": game_state_id_normalized,
        "msg_id": message.get("msgId", ""),
        "update_raw": update_raw,
        "update_kind": update_kind,
        "state_completeness": state_completeness,
        "is_complete_snapshot": is_complete_snapshot,
        "pending_message_count": pending_message_count if pending_message_count is not None else "",
        "prev_game_state_id": normalized_prev_game_state_id,
        "prev_game_state_id_status": prev_status,
        "linkage_status": prev_status,
        "deletion_evidence_present": bool(diff_deleted_instance_ids or diff_deleted_persistent_annotation_ids),
        "diff_deleted_instance_ids": list(diff_deleted_instance_ids),
        "diff_deleted_persistent_annotation_ids": list(diff_deleted_persistent_annotation_ids),
        "deletion_counts": deletion_counts,
        "section_counts": _section_counts(gsm),
        "source_fields_used": source_fields_used,
        "evidence_status": evidence_status,
        "value_source": value_source,
        "confidence": _confidence(evidence_status),
        "degradation_flags": degradation_flags,
        "review_required": bool(degradation_flags) or evidence_status in {"degraded", "unknown", "conflict"},
    }


def _update_raw(value: object, present: bool) -> str:
    if not present or value is None or not value:
        return ""
    text = str(value).strip()
    return text


def _update_kind(update_raw: str) -> str:
    if not update_raw:
        return "unknown"
    lowered = update_raw.lower()
    if lowered == "full":
        return "full"
    if lowered == "diff":
        return "diff"
    return "degraded"


def _degradation_flags_for_update(update_kind: str, update_raw: str, update_present: bool) -> list[str]:
    if update_kind == "degraded":
        return ["unknown_update_kind"]
    if update_kind == "unknown" and (not update_present or not update_raw):
        return ["missing_update_kind"]
    return []


def _state_completeness(update_kind: str) -> tuple[str, bool]:
    if update_kind == "full":
        return "complete_snapshot", True
    if update_kind == "diff":
        return "partial_update", False
    if update_kind == "degraded":
        return "degraded", False
    return "unknown", False


def _linkage_status(
    *,
    update_kind: str,
    game_state_id_normalized: int | str,
    prev_game_state_id: int | None,
    prev_present: bool,
    prev_malformed: bool,
) -> str:
    if prev_malformed:
        return "malformed"
    if prev_game_state_id is None:
        if update_kind == "full":
            return "not_applicable"
        if update_kind == "diff":
            return "missing"
        return "unknown"
    if not isinstance(game_state_id_normalized, int):
        return "present_unverified"
    if prev_game_state_id == game_state_id_normalized:
        return "self_reference"
    if prev_game_state_id > game_state_id_normalized:
        return "future_reference"
    if prev_present:
        return "linked"
    return "unknown"


def _add_linkage_flags(degradation_flags: list[str], status: str) -> None:
    if status == "missing":
        _append_flag(degradation_flags, "missing_prev_game_state_id")
    elif status == "self_reference":
        _append_flag(degradation_flags, "self_referential_prev_game_state_id")
    elif status == "future_reference":
        _append_flag(degradation_flags, "future_prev_game_state_id")


def _evidence_status(degradation_flags: list[str], update_kind: str) -> str:
    if "conflicting_update_and_linkage_evidence" in degradation_flags:
        return "conflict"
    if degradation_flags == ["missing_update_kind"] and update_kind == "unknown":
        return "unknown"
    if degradation_flags:
        return "degraded"
    if update_kind == "unknown":
        return "unknown"
    return "observed"


def _value_source(evidence_status: str, update_kind: str) -> str:
    if evidence_status == "conflict":
        return "conflict"
    if evidence_status == "unknown" or update_kind == "unknown":
        return "unknown"
    return "observed"


def _confidence(evidence_status: str) -> str:
    if evidence_status == "observed":
        return "high"
    if evidence_status == "unknown":
        return "unknown"
    return "low"


def _source_fields_used(message: Mapping[str, object], gsm: Mapping[str, object]) -> dict[str, bool]:
    return {
        "update": "update" in gsm,
        "pendingMessageCount": "pendingMessageCount" in gsm,
        "prevGameStateId": "prevGameStateId" in gsm,
        "diffDeletedInstanceIds": "diffDeletedInstanceIds" in gsm,
        "diffDeletedPersistentAnnotationIds": "diffDeletedPersistentAnnotationIds" in gsm,
        "gameStateId": "gameStateId" in message or "gameStateId" in gsm,
        "msgId": "msgId" in message or "msgId" in gsm,
        "type": "type" in message or "type" in gsm,
    }


def _section_counts(gsm: Mapping[str, object]) -> dict[str, int]:
    return {
        normalized_key: len(value) if isinstance(value := gsm.get(raw_key), list) else 0
        for normalized_key, raw_key in _SECTION_KEYS
    }


def _strict_id(value: object) -> int | str:
    if isinstance(value, bool):
        return ""
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.isdigit():
            return int(stripped)
    return ""


def _append_flag(target: list[str], flag: str) -> None:
    if flag not in target:
        target.append(flag)
