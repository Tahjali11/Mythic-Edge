from __future__ import annotations

from typing import Any

from .. import api_common
from .annotations import normalize_annotation_arrays
from .game_state_diff import build_game_state_diff_mechanics
from .timers import normalize_timer_array
from .turn_info import build_turn_info

QUEUED_GAME_STATE_MESSAGE_TYPE = "GREMessageType_QueuedGameStateMessage"


def build_game_state_payload(message: dict[str, Any], gsm: dict[str, Any]) -> dict[str, Any]:
    game_info = _game_info_payload(gsm)
    turn_info = build_turn_info(gsm)
    identity = _build_identity_payload(game_info, turn_info)
    payload_type = _payload_type(message)
    annotations = _safe_list_copy(gsm.get("annotations"))
    persistent_annotations = _safe_list_copy(gsm.get("persistentAnnotations"))
    timers = _safe_list_copy(gsm.get("timers"))
    update = str(gsm.get("update") or "")
    pending_message_count = _maybe_int(gsm.get("pendingMessageCount"))
    prev_game_state_id = _maybe_int(gsm.get("prevGameStateId"))
    diff_deleted_instance_ids = api_common.normalize_int_list(gsm.get("diffDeletedInstanceIds"))
    diff_deleted_persistent_annotation_ids = api_common.normalize_int_list(
        gsm.get("diffDeletedPersistentAnnotationIds")
    )

    return {
        "type": payload_type,
        "message_type": message.get("type", "GREMessageType_GameStateMessage"),
        "msg_id": message.get("msgId", 0),
        "game_state_id": message.get("gameStateId", 0),
        "system_seat_ids": api_common.normalize_int_list(message.get("systemSeatIds")),
        "stage": identity["stage"],
        "match_state": str(game_info.get("matchState") or ""),
        "turn_number": turn_info.get("turn_number"),
        "active_player_seat_id": turn_info.get("active_player_seat_id"),
        "game_info": game_info,
        "turn_info": turn_info,
        "identity": identity,
        "players": _safe_list_copy(gsm.get("players")),
        "zones": _safe_list_copy(gsm.get("zones")),
        "game_objects": _safe_list_copy(gsm.get("gameObjects")),
        "annotations": annotations,
        "persistent_annotations": persistent_annotations,
        "normalized_annotations": normalize_annotation_arrays(
            annotations=gsm.get("annotations"),
            persistent_annotations=gsm.get("persistentAnnotations"),
            diff_deleted_persistent_annotation_ids=gsm.get("diffDeletedPersistentAnnotationIds"),
        ),
        "timers": timers,
        "normalized_timers": normalize_timer_array(gsm.get("timers"), turn_info=turn_info),
        "actions": _safe_list_copy(gsm.get("actions")),
        "update": update,
        "pending_message_count": pending_message_count,
        "prev_game_state_id": prev_game_state_id,
        "diff_deleted_instance_ids": diff_deleted_instance_ids,
        "diff_deleted_persistent_annotation_ids": diff_deleted_persistent_annotation_ids,
        "game_state_diff_mechanics": build_game_state_diff_mechanics(
            message=message,
            gsm=gsm,
            payload_type=payload_type,
            game_state_id=message.get("gameStateId", 0),
            update=update,
            pending_message_count=pending_message_count,
            prev_game_state_id=prev_game_state_id,
            diff_deleted_instance_ids=diff_deleted_instance_ids,
            diff_deleted_persistent_annotation_ids=diff_deleted_persistent_annotation_ids,
        ),
        "raw_game_state": message,
    }


def _game_info_payload(gsm: dict[str, Any]) -> dict[str, Any]:
    game_info = gsm.get("gameInfo")
    if not isinstance(game_info, dict):
        return {}
    return dict(game_info)


def _build_identity_payload(game_info: dict[str, Any], turn_info: dict[str, Any]) -> dict[str, Any]:
    return {
        "match_id": str(game_info.get("matchID") or "").strip(),
        "game_number": _maybe_int(game_info.get("gameNumber")),
        "turn_number": turn_info.get("turn_number"),
        "active_player_seat_id": turn_info.get("active_player_seat_id"),
        "phase": turn_info.get("phase", ""),
        "step": turn_info.get("step", ""),
        "stage": str(game_info.get("stage") or ""),
    }


def _payload_type(message: dict[str, Any]) -> str:
    if message.get("type") == QUEUED_GAME_STATE_MESSAGE_TYPE:
        return "queued_game_state_message"
    return "game_state_message"


def _safe_list_copy(value: Any) -> list[Any]:
    if isinstance(value, list):
        return list(value)
    return []


def _maybe_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
