from mythic_edge_parser.parsers.gre.game_state import (
    QUEUED_GAME_STATE_MESSAGE_TYPE,
    build_game_state_payload,
)


def test_build_game_state_payload_shallow_copies_normalized_fields() -> None:
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
            "players": [{"systemSeatNumber": 1}, {"systemSeatNumber": 2}],
            "zones": [{"zoneId": 31}],
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

    raw_gsm = message["gameStateMessage"]
    assert raw_gsm["gameInfo"]["stage"] == "GameStage_Play"
    assert len(raw_gsm["players"]) == 2
    assert len(raw_gsm["zones"]) == 1
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
    assert payload["timers"] == [{"timerId": 1}]
    assert payload["actions"] == []
    assert payload["pending_message_count"] == 4
    assert payload["prev_game_state_id"] == 3
    assert payload["diff_deleted_instance_ids"] == [11, 12]
    assert payload["diff_deleted_persistent_annotation_ids"] == [21, 22]
