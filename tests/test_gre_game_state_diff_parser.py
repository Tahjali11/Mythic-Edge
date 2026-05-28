from __future__ import annotations

import json
from copy import deepcopy

from mythic_edge_parser.parsers.gre.game_state_diff import (
    GAME_STATE_DIFF_MECHANICS_OBJECT,
    SCHEMA_VERSION,
    build_game_state_diff_mechanics,
)


def _build_mechanics(
    *,
    message: dict[str, object] | None = None,
    gsm: dict[str, object] | None = None,
    payload_type: str = "game_state_message",
    pending_message_count: int | None = None,
    prev_game_state_id: int | None = None,
    diff_deleted_instance_ids: list[int] | None = None,
    diff_deleted_persistent_annotation_ids: list[int] | None = None,
) -> dict[str, object]:
    message = {"type": "GREMessageType_GameStateMessage", "msgId": 7, "gameStateId": 42} | (message or {})
    gsm = gsm or {}
    return build_game_state_diff_mechanics(
        message=message,
        gsm=gsm,
        payload_type=payload_type,
        game_state_id=message.get("gameStateId", 0),
        update=str(gsm.get("update") or ""),
        pending_message_count=pending_message_count,
        prev_game_state_id=prev_game_state_id,
        diff_deleted_instance_ids=diff_deleted_instance_ids or [],
        diff_deleted_persistent_annotation_ids=diff_deleted_persistent_annotation_ids or [],
    )


def test_full_update_maps_to_complete_snapshot_without_reconstruction_or_mutation() -> None:
    message = {"type": "GREMessageType_GameStateMessage", "msgId": 7, "gameStateId": "42"}
    gsm = {
        "update": " Full ",
        "players": [{"systemSeatNumber": 1}, {"systemSeatNumber": 2}],
        "zones": [{"zoneId": 1}],
        "gameObjects": [{"instanceId": 1}, {"instanceId": 2}],
        "annotations": [{"id": 1}],
        "persistentAnnotations": [],
        "timers": [{"timerId": 1}],
        "actions": [{"seatId": 1}],
    }
    original_message = deepcopy(message)
    original_gsm = deepcopy(gsm)

    mechanics = _build_mechanics(message=message, gsm=gsm)

    assert json.loads(json.dumps(mechanics)) == mechanics
    assert message == original_message
    assert gsm == original_gsm
    assert mechanics["object"] == GAME_STATE_DIFF_MECHANICS_OBJECT
    assert mechanics["schema_version"] == SCHEMA_VERSION
    assert mechanics["source_payload_type"] == "game_state_message"
    assert mechanics["message_type"] == "GREMessageType_GameStateMessage"
    assert mechanics["queued"] is False
    assert mechanics["game_state_id"] == "42"
    assert mechanics["game_state_id_normalized"] == 42
    assert mechanics["msg_id"] == 7
    assert mechanics["update_raw"] == "Full"
    assert mechanics["update_kind"] == "full"
    assert mechanics["state_completeness"] == "complete_snapshot"
    assert mechanics["is_complete_snapshot"] is True
    assert mechanics["prev_game_state_id"] == ""
    assert mechanics["prev_game_state_id_status"] == "not_applicable"
    assert mechanics["linkage_status"] == "not_applicable"
    assert mechanics["deletion_evidence_present"] is False
    assert mechanics["section_counts"] == {
        "players": 2,
        "zones": 1,
        "game_objects": 2,
        "annotations": 1,
        "persistent_annotations": 0,
        "timers": 1,
        "actions": 1,
    }
    assert mechanics["source_fields_used"] == {
        "update": True,
        "pendingMessageCount": False,
        "prevGameStateId": False,
        "diffDeletedInstanceIds": False,
        "diffDeletedPersistentAnnotationIds": False,
        "gameStateId": True,
        "msgId": True,
        "type": True,
    }
    assert mechanics["evidence_status"] == "observed"
    assert mechanics["value_source"] == "observed"
    assert mechanics["confidence"] == "high"
    assert mechanics["degradation_flags"] == []
    assert mechanics["review_required"] is False


def test_diff_update_maps_to_partial_update_with_linked_deletion_evidence() -> None:
    mechanics = _build_mechanics(
        gsm={
            "update": "diff",
            "pendingMessageCount": "4",
            "prevGameStateId": "41",
            "diffDeletedInstanceIds": [10, "11"],
            "diffDeletedPersistentAnnotationIds": [20, "21"],
        },
        pending_message_count=4,
        prev_game_state_id=41,
        diff_deleted_instance_ids=[10, 11],
        diff_deleted_persistent_annotation_ids=[20, 21],
    )

    assert mechanics["update_kind"] == "diff"
    assert mechanics["state_completeness"] == "partial_update"
    assert mechanics["is_complete_snapshot"] is False
    assert mechanics["pending_message_count"] == 4
    assert mechanics["prev_game_state_id"] == 41
    assert mechanics["prev_game_state_id_status"] == "linked"
    assert mechanics["linkage_status"] == "linked"
    assert mechanics["deletion_evidence_present"] is True
    assert mechanics["diff_deleted_instance_ids"] == [10, 11]
    assert mechanics["diff_deleted_persistent_annotation_ids"] == [20, 21]
    assert mechanics["deletion_counts"] == {"instance_ids": 2, "persistent_annotation_ids": 2}
    assert mechanics["evidence_status"] == "observed"
    assert mechanics["review_required"] is False


def test_queued_game_state_uses_same_shape_without_degrading_queue_status() -> None:
    mechanics = _build_mechanics(
        message={"type": "GREMessageType_QueuedGameStateMessage", "msgId": 8, "gameStateId": 43},
        gsm={"update": "full"},
        payload_type="queued_game_state_message",
    )

    assert mechanics["source_payload_type"] == "queued_game_state_message"
    assert mechanics["queued"] is True
    assert mechanics["update_kind"] == "full"
    assert mechanics["evidence_status"] == "observed"
    assert mechanics["degradation_flags"] == []


def test_missing_and_unknown_update_kind_are_reviewable_without_crashing() -> None:
    missing = _build_mechanics(gsm={})
    assert missing["update_raw"] == ""
    assert missing["update_kind"] == "unknown"
    assert missing["state_completeness"] == "unknown"
    assert missing["is_complete_snapshot"] is False
    assert missing["prev_game_state_id_status"] == "unknown"
    assert missing["evidence_status"] == "unknown"
    assert missing["value_source"] == "unknown"
    assert missing["confidence"] == "unknown"
    assert missing["degradation_flags"] == ["missing_update_kind"]
    assert missing["review_required"] is True

    unknown = _build_mechanics(gsm={"update": "incremental"})
    assert unknown["update_raw"] == "incremental"
    assert unknown["update_kind"] == "degraded"
    assert unknown["state_completeness"] == "degraded"
    assert unknown["evidence_status"] == "degraded"
    assert unknown["confidence"] == "low"
    assert unknown["degradation_flags"] == ["unknown_update_kind"]
    assert unknown["review_required"] is True


def test_linkage_degradation_boundaries_are_explicit() -> None:
    missing_prev = _build_mechanics(gsm={"update": "diff"})
    assert missing_prev["prev_game_state_id_status"] == "missing"
    assert missing_prev["degradation_flags"] == ["missing_prev_game_state_id"]

    malformed_prev = _build_mechanics(gsm={"update": "diff", "prevGameStateId": "bad"})
    assert malformed_prev["prev_game_state_id_status"] == "malformed"
    assert malformed_prev["degradation_flags"] == ["malformed_prev_game_state_id"]

    self_reference = _build_mechanics(gsm={"update": "diff", "prevGameStateId": "42"}, prev_game_state_id=42)
    assert self_reference["prev_game_state_id_status"] == "self_reference"
    assert self_reference["degradation_flags"] == ["self_referential_prev_game_state_id"]

    future_reference = _build_mechanics(gsm={"update": "diff", "prevGameStateId": "43"}, prev_game_state_id=43)
    assert future_reference["prev_game_state_id_status"] == "future_reference"
    assert future_reference["degradation_flags"] == ["future_prev_game_state_id"]

    unverified = _build_mechanics(
        message={"gameStateId": "bad"},
        gsm={"update": "diff", "prevGameStateId": "41"},
        prev_game_state_id=41,
    )
    assert unverified["game_state_id_normalized"] == ""
    assert unverified["prev_game_state_id_status"] == "present_unverified"
    assert unverified["degradation_flags"] == ["malformed_game_state_id"]


def test_malformed_counts_and_deletion_source_shapes_are_degraded_without_losing_normalized_ids() -> None:
    mechanics = _build_mechanics(
        gsm={
            "update": "diff",
            "prevGameStateId": "41",
            "pendingMessageCount": "bad",
            "diffDeletedInstanceIds": "bad",
            "diffDeletedPersistentAnnotationIds": {"bad": "shape"},
        },
        prev_game_state_id=41,
        diff_deleted_instance_ids=[10],
        diff_deleted_persistent_annotation_ids=[20],
    )

    assert mechanics["pending_message_count"] == ""
    assert mechanics["diff_deleted_instance_ids"] == [10]
    assert mechanics["diff_deleted_persistent_annotation_ids"] == [20]
    assert mechanics["deletion_counts"] == {"instance_ids": 1, "persistent_annotation_ids": 1}
    assert mechanics["deletion_evidence_present"] is True
    assert set(mechanics["degradation_flags"]) == {
        "malformed_pending_message_count",
        "malformed_diff_deleted_instance_ids",
        "malformed_diff_deleted_persistent_annotation_ids",
    }
    assert mechanics["evidence_status"] == "degraded"
    assert mechanics["review_required"] is True

    negative_count = _build_mechanics(gsm={"update": "full", "pendingMessageCount": "-1"}, pending_message_count=-1)
    assert negative_count["pending_message_count"] == -1
    assert negative_count["degradation_flags"] == ["negative_pending_message_count"]


def test_full_update_with_deletion_markers_does_not_become_inferred_diff() -> None:
    mechanics = _build_mechanics(
        gsm={"update": "full", "diffDeletedInstanceIds": [1]},
        diff_deleted_instance_ids=[1],
    )

    assert mechanics["update_kind"] == "full"
    assert mechanics["state_completeness"] == "complete_snapshot"
    assert mechanics["is_complete_snapshot"] is True
    assert mechanics["deletion_evidence_present"] is True
    assert mechanics["deletion_counts"] == {"instance_ids": 1, "persistent_annotation_ids": 0}
    assert mechanics["degradation_flags"] == []
