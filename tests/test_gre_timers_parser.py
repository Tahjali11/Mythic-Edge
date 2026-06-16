from __future__ import annotations

import json
from copy import deepcopy

from mythic_edge_parser.parsers.gre.timers import (
    SCHEMA_VERSION,
    TIMER_COLLECTION_OBJECT,
    TIMER_RECORD_OBJECT,
    normalize_timer_array,
    normalize_timer_record,
    timer_records_by_direct_seat,
)


def test_normalize_timer_array_builds_collection_summaries_without_mutation() -> None:
    timers = [
        {
            "timerId": "9",
            "timerType": "TimerType_GameClock",
            "timerName": "GameClock",
            "timerState": "running",
            "playerSeatId": "1",
            "running": True,
            "durationMs": 30000,
            "remainingSeconds": "20",
            "elapsedTime": "1.5",
            "priorityCount": 2,
            "customLabel": " side clock ",
        }
    ]
    original_timers = deepcopy(timers)

    normalized = normalize_timer_array(
        timers,
        turn_info={
            "turn_number": 3,
            "active_player_seat_id": 1,
            "decision_player_seat_id": None,
            "priority_player_seat_id": 2,
        },
    )

    assert json.loads(json.dumps(normalized)) == normalized
    assert timers == original_timers
    assert normalized["object"] == TIMER_COLLECTION_OBJECT
    assert normalized["schema_version"] == SCHEMA_VERSION
    assert normalized["total_records"] == 1
    assert normalized["degraded_records"] == 1
    assert normalized["review_required"] is True
    assert normalized["source_array"] == "timers"
    assert normalized["timer_ids"] == [9]
    assert normalized["timer_types"] == ["TimerType_GameClock"]
    assert normalized["direct_seat_ids"] == [1]
    assert normalized["time_units_seen"] == {"seconds": 1, "milliseconds": 1, "unknown": 1}
    assert normalized["contextual_turn_info"] == {
        "turn_number": 3,
        "active_player_seat_id": 1,
        "decision_player_seat_id": "",
        "priority_player_seat_id": 2,
    }

    record = normalized["records"][0]
    assert record["object"] == TIMER_RECORD_OBJECT
    assert record["timer_id"] == 9
    assert record["timer_type"] == "TimerType_GameClock"
    assert record["timer_name"] == "GameClock"
    assert record["timer_state"] == "running"
    assert record["seat_fields"]["player_seat_id"] == 1
    assert record["direct_seat_ids"] == [1]
    assert record["time_values"] == {
        "seconds": [{"key": "remainingSeconds", "value": 20, "seconds_value": 20}],
        "milliseconds": [{"key": "durationMs", "value": 30000, "seconds_value": 30.0}],
        "unknown_unit": [{"key": "elapsedTime", "value": 1.5}],
    }
    assert "unknown_timer_time_unit" in record["degradation_flags"]
    assert record["confidence"] == "low"
    assert timer_records_by_direct_seat(normalized) == {1: [record]}


def test_normalize_timer_array_covers_clean_active_player_timer_evidence() -> None:
    normalized = normalize_timer_array(
        [
            {
                "timerId": 12,
                "timerType": "TimerType_ActivePlayer",
                "timerName": "ActivePlayerTimer",
                "timerState": "running",
                "playerSeatId": 1,
                "running": True,
                "remainingSeconds": 24,
                "durationMs": 30000,
            }
        ],
        turn_info={
            "turn_number": 4,
            "active_player_seat_id": 1,
            "decision_player_seat_id": "",
            "priority_player_seat_id": "",
        },
    )

    assert normalized["object"] == TIMER_COLLECTION_OBJECT
    assert normalized["schema_version"] == SCHEMA_VERSION
    assert normalized["total_records"] == 1
    assert normalized["degraded_records"] == 0
    assert normalized["review_required"] is False
    assert normalized["timer_ids"] == [12]
    assert normalized["timer_types"] == ["TimerType_ActivePlayer"]
    assert normalized["direct_seat_ids"] == [1]
    assert normalized["time_units_seen"] == {"seconds": 1, "milliseconds": 1, "unknown": 0}
    assert normalized["contextual_turn_info"] == {
        "turn_number": 4,
        "active_player_seat_id": 1,
        "decision_player_seat_id": "",
        "priority_player_seat_id": "",
    }

    record = normalized["records"][0]
    assert record["object"] == TIMER_RECORD_OBJECT
    assert record["timer_id"] == 12
    assert record["timer_type"] == "TimerType_ActivePlayer"
    assert record["timer_name"] == "ActivePlayerTimer"
    assert record["timer_state"] == "running"
    assert record["seat_fields"]["player_seat_id"] == 1
    assert record["direct_seat_ids"] == [1]
    assert record["boolean_fields"] == [{"key": "running", "normalized_key": "running", "value": True}]
    assert record["time_values"] == {
        "seconds": [{"key": "remainingSeconds", "value": 24, "seconds_value": 24}],
        "milliseconds": [{"key": "durationMs", "value": 30000, "seconds_value": 30.0}],
        "unknown_unit": [],
    }
    assert record["evidence_status"] == "observed"
    assert record["value_source"] == "derived"
    assert record["confidence"] == "high"
    assert record["degradation_flags"] == []
    assert timer_records_by_direct_seat(normalized) == {1: [record]}


def test_normalize_timer_array_handles_missing_malformed_and_placeholder_records() -> None:
    missing = normalize_timer_array(None)
    assert missing["records"] == []
    assert missing["total_records"] == 0
    assert missing["degradation_flags"] == []
    assert missing["review_required"] is False

    malformed = normalize_timer_array("not-a-list")
    assert malformed["records"] == []
    assert malformed["degradation_flags"] == ["malformed_timers_section"]
    assert malformed["review_required"] is True

    with_placeholder = normalize_timer_array([None])
    record = with_placeholder["records"][0]
    assert record["object"] == TIMER_RECORD_OBJECT
    assert record["source_array"] == "timers"
    assert record["source_index"] == 0
    assert record["degradation_flags"] == ["malformed_timer_record"]
    assert record["evidence_status"] == "degraded"
    assert record["confidence"] == "low"
    assert record["review_required"] is True


def test_normalize_timer_record_locks_identifier_string_boolean_and_seat_boundaries() -> None:
    record = normalize_timer_record(
        {
            "timerId": True,
            "timerType": 99,
            "running": "true",
            "ownerSeatId": True,
            "playerSeatId": "2",
            "seatId": "3",
            "systemSeatId": 4.5,
            "teamId": "5",
            "playerId": "6",
        },
        source_index=0,
    )

    assert record["timer_id"] == ""
    assert record["timer_type"] == ""
    assert record["boolean_fields"] == []
    assert record["seat_fields"] == {
        "owner_seat_id": "",
        "controller_seat_id": "",
        "player_seat_id": 2,
        "system_seat_id": "",
        "team_id": 5,
        "player_id": 6,
    }
    assert record["direct_seat_ids"] == [2]
    assert record["evidence_status"] == "conflict"
    assert record["value_source"] == "conflict"
    assert set(record["degradation_flags"]) == {
        "malformed_timer_id",
        "malformed_timer_string_field",
        "malformed_timer_boolean_field",
        "malformed_timer_seat_field",
        "conflicting_timer_seat_fields",
    }


def test_normalize_timer_record_normalizes_numeric_time_and_unsupported_fields() -> None:
    record = normalize_timer_record(
        {
            "type": "TimerType_Test",
            "durationMs": "-1500.5",
            "remainingSeconds": " 2.25 ",
            "elapsedTime": "3.5",
            "priorityCount": "7",
            "deadlineTime": "not-numeric",
            "metadata": {"kept": False},
            "timerPayload": [],
            "truncation_or_data_loss_evidence": True,
        },
        source_index=4,
    )

    assert record["numeric_fields"] == [
        {
            "key": "durationMs",
            "normalized_key": "duration_ms",
            "value": -1500.5,
            "unit": "milliseconds",
            "seconds_value": -1.5005,
        },
        {
            "key": "remainingSeconds",
            "normalized_key": "remaining_seconds",
            "value": 2.25,
            "unit": "seconds",
            "seconds_value": 2.25,
        },
        {"key": "elapsedTime", "normalized_key": "elapsed_time", "value": 3.5, "unit": "unknown"},
        {"key": "priorityCount", "normalized_key": "priority_count", "value": 7, "unit": ""},
    ]
    assert record["time_values"] == {
        "seconds": [{"key": "remainingSeconds", "value": 2.25, "seconds_value": 2.25}],
        "milliseconds": [{"key": "durationMs", "value": -1500.5, "seconds_value": -1.5005}],
        "unknown_unit": [{"key": "elapsedTime", "value": 3.5}],
    }
    assert record["unsupported_field_names"] == ["metadata", "timerPayload"]
    assert set(record["degradation_flags"]) == {
        "negative_timer_value",
        "unknown_timer_time_unit",
        "malformed_timer_numeric_field",
        "unsupported_timer_field_shape",
        "truncation_or_data_loss_evidence",
    }


def test_normalize_timer_record_preserves_booleans_without_numeric_coercion() -> None:
    record = normalize_timer_record(
        {
            "timerId": "1",
            "running": True,
            "paused": False,
            "hasPriority": True,
            "active": 1,
            "customFlag": False,
            "durationMs": True,
        },
        source_index=0,
    )

    assert record["timer_id"] == 1
    assert record["boolean_fields"] == [
        {"key": "running", "normalized_key": "running", "value": True},
        {"key": "paused", "normalized_key": "paused", "value": False},
        {"key": "hasPriority", "normalized_key": "has_priority", "value": True},
        {"key": "customFlag", "normalized_key": "custom_flag", "value": False},
    ]
    assert record["numeric_fields"] == []
    assert set(record["degradation_flags"]) == {
        "malformed_timer_boolean_field",
        "malformed_timer_numeric_field",
    }


def test_turn_info_context_does_not_assign_timer_ownership() -> None:
    normalized = normalize_timer_array(
        [{"timerId": 9}],
        turn_info={
            "turn_number": "3",
            "active_player_seat_id": "1",
            "decision_player_seat_id": "2",
            "priority_player_seat_id": "3",
        },
    )

    assert normalized["direct_seat_ids"] == []
    assert normalized["records"][0]["seat_fields"] == {
        "owner_seat_id": "",
        "controller_seat_id": "",
        "player_seat_id": "",
        "system_seat_id": "",
        "team_id": "",
        "player_id": "",
    }
    assert normalized["contextual_turn_info"] == {
        "turn_number": 3,
        "active_player_seat_id": 1,
        "decision_player_seat_id": 2,
        "priority_player_seat_id": 3,
    }
