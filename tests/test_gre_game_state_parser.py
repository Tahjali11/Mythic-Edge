from mythic_edge_parser.parsers.gre.game_state import (
    QUEUED_GAME_STATE_MESSAGE_TYPE,
    build_game_state_payload,
)


def test_build_game_state_payload_happy_path_fields() -> None:
    message = {
        "type": "GREMessageType_GameStateMessage",
        "msgId": 7,
        "gameStateId": 42,
        "systemSeatIds": [1, "2"],
    }
    gsm = {
        "gameInfo": {
            "matchID": " match-42 ",
            "gameNumber": "2",
            "stage": "GameStage_Play",
            "matchState": "MatchState_GameInProgress",
        },
        "turnInfo": {
            "turnNumber": "3",
            "activePlayer": "2",
            "phase": "Phase_Main1",
            "step": "Step_PreCombatMain",
        },
        "players": [{"systemSeatNumber": 1}, {"systemSeatNumber": 2}],
        "zones": [{"zoneId": 31}],
        "gameObjects": [{"instanceId": 101}],
        "annotations": [{"id": 5}],
        "persistentAnnotations": [{"id": 6}],
        "timers": [{"timerId": 9}],
        "actions": [{"seatId": 1}],
        "update": "full",
        "pendingMessageCount": "4",
        "prevGameStateId": "41",
        "diffDeletedInstanceIds": [10, "11"],
        "diffDeletedPersistentAnnotationIds": [20, "21"],
    }

    payload = build_game_state_payload(message, gsm)
    normalized_annotations = payload.pop("normalized_annotations")
    normalized_timers = payload.pop("normalized_timers")
    game_state_diff_mechanics = payload.pop("game_state_diff_mechanics")

    assert normalized_annotations["object"] == "mythic_edge_gre_annotations"
    assert normalized_annotations["schema_version"] == "parser_gre_annotations.v1"
    assert normalized_annotations["total_records"] == 2
    assert normalized_annotations["degraded_records"] == 2
    assert normalized_annotations["review_required"] is True
    assert normalized_annotations["source_arrays"] == {"annotations": 1, "persistent_annotations": 1}
    assert normalized_annotations["diff_deleted_persistent_annotation_ids"] == [20, 21]
    assert normalized_annotations["records"][0]["source_array"] == "annotations"
    assert normalized_annotations["records"][1]["source_array"] == "persistent_annotations"
    assert normalized_timers["object"] == "mythic_edge_gre_timers"
    assert normalized_timers["schema_version"] == "parser_gre_timers.v1"
    assert normalized_timers["total_records"] == 1
    assert normalized_timers["degraded_records"] == 0
    assert normalized_timers["review_required"] is False
    assert normalized_timers["timer_ids"] == [9]
    assert normalized_timers["contextual_turn_info"] == {
        "turn_number": 3,
        "active_player_seat_id": 2,
        "decision_player_seat_id": "",
        "priority_player_seat_id": "",
    }
    assert game_state_diff_mechanics["object"] == "mythic_edge_gre_game_state_diff_mechanics"
    assert game_state_diff_mechanics["schema_version"] == "parser_gre_game_state_diff_mechanics.v1"
    assert game_state_diff_mechanics["source_payload_type"] == "game_state_message"
    assert game_state_diff_mechanics["queued"] is False
    assert game_state_diff_mechanics["game_state_id"] == 42
    assert game_state_diff_mechanics["game_state_id_normalized"] == 42
    assert game_state_diff_mechanics["msg_id"] == 7
    assert game_state_diff_mechanics["update_raw"] == "full"
    assert game_state_diff_mechanics["update_kind"] == "full"
    assert game_state_diff_mechanics["state_completeness"] == "complete_snapshot"
    assert game_state_diff_mechanics["is_complete_snapshot"] is True
    assert game_state_diff_mechanics["pending_message_count"] == 4
    assert game_state_diff_mechanics["prev_game_state_id"] == 41
    assert game_state_diff_mechanics["prev_game_state_id_status"] == "linked"
    assert game_state_diff_mechanics["diff_deleted_instance_ids"] == [10, 11]
    assert game_state_diff_mechanics["diff_deleted_persistent_annotation_ids"] == [20, 21]
    assert game_state_diff_mechanics["deletion_counts"] == {"instance_ids": 2, "persistent_annotation_ids": 2}
    assert game_state_diff_mechanics["deletion_evidence_present"] is True
    assert game_state_diff_mechanics["section_counts"]["timers"] == 1
    assert game_state_diff_mechanics["evidence_status"] == "observed"
    assert payload["annotations"] == [{"id": 5}]
    assert payload["persistent_annotations"] == [{"id": 6}]
    assert payload["timers"] == [{"timerId": 9}]
    assert payload == {
        "type": "game_state_message",
        "message_type": "GREMessageType_GameStateMessage",
        "msg_id": 7,
        "game_state_id": 42,
        "system_seat_ids": [1, 2],
        "stage": "GameStage_Play",
        "match_state": "MatchState_GameInProgress",
        "turn_number": 3,
        "active_player_seat_id": 2,
        "game_info": {
            "matchID": " match-42 ",
            "gameNumber": "2",
            "stage": "GameStage_Play",
            "matchState": "MatchState_GameInProgress",
        },
        "turn_info": {
            "turn_number": 3,
            "phase": "Phase_Main1",
            "step": "Step_PreCombatMain",
            "active_player_seat_id": 2,
            "decision_player_seat_id": None,
            "priority_player_seat_id": None,
            "next_phase": "",
            "next_step": "",
        },
        "identity": {
            "match_id": "match-42",
            "game_number": 2,
            "turn_number": 3,
            "active_player_seat_id": 2,
            "phase": "Phase_Main1",
            "step": "Step_PreCombatMain",
            "stage": "GameStage_Play",
        },
        "players": [{"systemSeatNumber": 1}, {"systemSeatNumber": 2}],
        "zones": [{"zoneId": 31}],
        "game_objects": [{"instanceId": 101}],
        "annotations": [{"id": 5}],
        "persistent_annotations": [{"id": 6}],
        "timers": [{"timerId": 9}],
        "actions": [{"seatId": 1}],
        "update": "full",
        "pending_message_count": 4,
        "prev_game_state_id": 41,
        "diff_deleted_instance_ids": [10, 11],
        "diff_deleted_persistent_annotation_ids": [20, 21],
        "raw_game_state": message,
    }
    assert payload["raw_game_state"] is message


def test_build_game_state_payload_shallow_copies_normalized_fields() -> None:
    player = {"systemSeatNumber": 1}
    zone = {"zoneId": 31}
    message = {
        "type": "GREMessageType_GameStateMessage",
        "msgId": 7,
        "gameStateId": 42,
        "systemSeatIds": [1],
        "gameStateMessage": {
            "gameInfo": {
                "matchID": "match-42",
                "gameNumber": 2,
                "stage": "GameStage_Play",
                "matchState": "MatchState_GameInProgress",
            },
            "turnInfo": {
                "turnNumber": 3,
                "activePlayer": 2,
                "phase": "Phase_Main1",
                "step": "Step_PreCombatMain",
            },
            "players": [player, "non-dict-player"],
            "zones": [zone],
            "gameObjects": [{"instanceId": 101}],
            "annotations": [{"id": 5}],
            "persistentAnnotations": [{"id": 6}],
            "timers": [{"timerId": 9}],
            "actions": [{"seatId": 1}],
        },
    }

    payload = build_game_state_payload(message, message["gameStateMessage"])

    payload["game_info"]["stage"] = "Changed"
    payload["players"].append({"systemSeatNumber": 9})
    payload["zones"].append({"zoneId": 99})
    payload["players"][0]["teamId"] = 1

    raw_gsm = message["gameStateMessage"]
    assert raw_gsm["gameInfo"]["stage"] == "GameStage_Play"
    assert len(raw_gsm["players"]) == 2
    assert len(raw_gsm["zones"]) == 1
    assert raw_gsm["players"][0]["teamId"] == 1
    assert payload["players"][:2] == [player, "non-dict-player"]
    assert payload["raw_game_state"] is message


def test_build_game_state_payload_handles_missing_and_malformed_sections() -> None:
    message = {
        "type": QUEUED_GAME_STATE_MESSAGE_TYPE,
        "msgId": "8",
        "gameStateId": "17",
        "systemSeatIds": ["1", "2", "x"],
    }
    gsm = {
        "gameInfo": "not-a-dict",
        "turnInfo": {
            "activePlayerSeatId": "2",
            "nextPhase": "Phase_End",
            "nextStep": "Step_End",
        },
        "players": "not-a-list",
        "zones": None,
        "gameObjects": [{"instanceId": 101}],
        "annotations": "bad",
        "persistentAnnotations": None,
        "timers": [{"timerId": 1}],
        "actions": "bad",
        "pendingMessageCount": "4",
        "prevGameStateId": "3",
        "diffDeletedInstanceIds": ["11", 12, "x"],
        "diffDeletedPersistentAnnotationIds": ["21", 22, "x"],
    }

    payload = build_game_state_payload(message, gsm)

    assert payload["type"] == "queued_game_state_message"
    assert payload["message_type"] == QUEUED_GAME_STATE_MESSAGE_TYPE
    assert payload["msg_id"] == "8"
    assert payload["game_state_id"] == "17"
    assert payload["system_seat_ids"] == [1, 2]
    assert payload["game_info"] == {}
    assert payload["stage"] == ""
    assert payload["match_state"] == ""
    assert payload["identity"] == {
        "match_id": "",
        "game_number": None,
        "turn_number": None,
        "active_player_seat_id": 2,
        "phase": "",
        "step": "",
        "stage": "",
    }
    assert payload["players"] == []
    assert payload["zones"] == []
    assert payload["game_objects"] == [{"instanceId": 101}]
    assert payload["annotations"] == []
    assert payload["persistent_annotations"] == []
    assert payload["normalized_annotations"]["total_records"] == 0
    assert payload["normalized_annotations"]["degradation_flags"] == ["malformed_annotations_section"]
    assert payload["normalized_annotations"]["review_required"] is True
    assert payload["timers"] == [{"timerId": 1}]
    assert payload["normalized_timers"]["total_records"] == 1
    assert payload["normalized_timers"]["degraded_records"] == 0
    assert payload["normalized_timers"]["timer_ids"] == [1]
    assert payload["normalized_timers"]["contextual_turn_info"]["active_player_seat_id"] == 2
    assert payload["game_state_diff_mechanics"]["source_payload_type"] == "queued_game_state_message"
    assert payload["game_state_diff_mechanics"]["queued"] is True
    assert payload["game_state_diff_mechanics"]["game_state_id_normalized"] == 17
    assert payload["game_state_diff_mechanics"]["update_kind"] == "unknown"
    assert payload["game_state_diff_mechanics"]["evidence_status"] == "unknown"
    assert payload["game_state_diff_mechanics"]["review_required"] is True
    assert payload["actions"] == []
    assert payload["pending_message_count"] == 4
    assert payload["prev_game_state_id"] == 3
    assert payload["diff_deleted_instance_ids"] == [11, 12]
    assert payload["diff_deleted_persistent_annotation_ids"] == [21, 22]


def test_build_game_state_payload_defaults_for_missing_message_fields_and_sections() -> None:
    payload = build_game_state_payload(
        {},
        {
            "gameInfo": {"matchID": 0, "gameNumber": "bad", "stage": 0, "matchState": False},
            "turnInfo": "not-a-dict",
            "players": (),
            "zones": {"bad": "shape"},
            "gameObjects": None,
            "annotations": "bad",
            "persistentAnnotations": None,
            "timers": object(),
            "actions": "bad",
            "update": 0,
            "pendingMessageCount": "bad",
            "prevGameStateId": None,
            "diffDeletedInstanceIds": "not-a-list",
            "diffDeletedPersistentAnnotationIds": None,
        },
    )

    assert payload["type"] == "game_state_message"
    assert payload["message_type"] == "GREMessageType_GameStateMessage"
    assert payload["msg_id"] == 0
    assert payload["game_state_id"] == 0
    assert payload["system_seat_ids"] == []
    assert payload["stage"] == ""
    assert payload["match_state"] == ""
    assert payload["turn_info"] == {}
    assert payload["turn_number"] is None
    assert payload["active_player_seat_id"] is None
    assert payload["identity"] == {
        "match_id": "",
        "game_number": None,
        "turn_number": None,
        "active_player_seat_id": None,
        "phase": "",
        "step": "",
        "stage": "",
    }
    assert payload["players"] == []
    assert payload["zones"] == []
    assert payload["game_objects"] == []
    assert payload["annotations"] == []
    assert payload["persistent_annotations"] == []
    assert payload["normalized_annotations"]["total_records"] == 0
    assert payload["normalized_annotations"]["degradation_flags"] == ["malformed_annotations_section"]
    assert payload["normalized_annotations"]["review_required"] is True
    assert payload["timers"] == []
    assert payload["normalized_timers"]["total_records"] == 0
    assert payload["normalized_timers"]["degradation_flags"] == ["malformed_timers_section"]
    assert payload["normalized_timers"]["review_required"] is True
    assert payload["game_state_diff_mechanics"]["game_state_id"] == 0
    assert payload["game_state_diff_mechanics"]["game_state_id_normalized"] == ""
    assert payload["game_state_diff_mechanics"]["update_kind"] == "unknown"
    assert payload["game_state_diff_mechanics"]["pending_message_count"] == ""
    assert payload["game_state_diff_mechanics"]["prev_game_state_id"] == ""
    assert payload["game_state_diff_mechanics"]["diff_deleted_instance_ids"] == []
    assert payload["game_state_diff_mechanics"]["degradation_flags"] == [
        "missing_update_kind",
        "malformed_prev_game_state_id",
        "malformed_pending_message_count",
        "malformed_diff_deleted_instance_ids",
        "malformed_diff_deleted_persistent_annotation_ids",
    ]
    assert payload["actions"] == []
    assert payload["update"] == ""
    assert payload["pending_message_count"] is None
    assert payload["prev_game_state_id"] is None
    assert payload["diff_deleted_instance_ids"] == []
    assert payload["diff_deleted_persistent_annotation_ids"] == []


def test_build_game_state_payload_locks_integer_normalization_boundaries() -> None:
    message = {
        "systemSeatIds": [1, "2", " 3 ", True, False, 4.5, "-5", "bad", None, 2],
    }
    gsm = {
        "gameInfo": {
            "matchID": "match-int",
            "gameNumber": False,
            "stage": "GameStage_Play",
        },
        "turnInfo": {
            "turnNumber": " -2 ",
            "activePlayer": True,
        },
        "pendingMessageCount": True,
        "prevGameStateId": 4.9,
        "diffDeletedInstanceIds": [7, "8", True, False, 9.1, "-10", "bad", None],
        "diffDeletedPersistentAnnotationIds": ["11", 12, " 13 ", True, 14.2],
    }

    payload = build_game_state_payload(message, gsm)

    assert payload["system_seat_ids"] == [1, 2, 3, 2]
    assert payload["diff_deleted_instance_ids"] == [7, 8]
    assert payload["diff_deleted_persistent_annotation_ids"] == [11, 12, 13]
    assert payload["identity"]["game_number"] == 0
    assert payload["turn_info"]["turn_number"] == -2
    assert payload["turn_info"]["active_player_seat_id"] == 1
    assert payload["pending_message_count"] == 1
    assert payload["prev_game_state_id"] == 4
