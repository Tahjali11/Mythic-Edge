from datetime import UTC, datetime
from types import SimpleNamespace

from mythic_edge_parser.app import extractors
from mythic_edge_parser.app.extractors import (
    _event_datetime,
    _extract_game_result_identity,
    _extract_instance_grp_lookup,
    _extract_local_private_hand_instance_ids,
    _extract_local_team_from_client_action,
    _extract_local_team_from_game_state,
    _extract_starting_player_from_client_action,
    _extract_starting_player_from_game_state,
    _extract_turn_info,
    _first_present,
    _game_state_actions,
    _game_state_annotations,
    _has_match_scope_result,
    _hydrate_game_state_identity,
    _maybe_int,
    _safe_dict,
    _safe_iso,
    _safe_list,
    _safe_local_player,
)


def test_safe_local_player_uses_configured_index_and_falls_back_to_first_player(monkeypatch) -> None:
    players = [{"teamId": 1}, {"teamId": 2}]

    monkeypatch.setattr(extractors, "LOCAL_PLAYER_INDEX", 1)
    assert _safe_local_player(players) == {"teamId": 2}

    monkeypatch.setattr(extractors, "LOCAL_PLAYER_INDEX", 99)
    assert _safe_local_player(players) == {"teamId": 1}


def test_safe_local_player_returns_empty_dict_for_malformed_inputs(monkeypatch) -> None:
    monkeypatch.setattr(extractors, "LOCAL_PLAYER_INDEX", 0)

    assert _safe_local_player("bad") == {}
    assert _safe_local_player({"teamId": 1}) == {}
    assert _safe_local_player(["bad"]) == {}
    assert _safe_local_player([None]) == {}


def test_safe_primitive_helpers_edge_cases() -> None:
    assert _first_present(None, "", 0, "later") == 0
    assert _first_present(None, "", False, "later") is False
    assert _first_present(None, "", {}, "later") == {}
    assert _first_present(None, "", [], "later") == []
    assert _first_present(None, "") is None

    assert _maybe_int("2") == 2
    assert _maybe_int("not-an-int") is None
    assert _maybe_int(None) is None

    assert _safe_dict({"ok": True}) == {"ok": True}
    assert _safe_dict([("ok", True)]) == {}
    assert _safe_list([1, 2]) == [1, 2]
    assert _safe_list(("not", "a", "list")) == []


def test_maybe_int_bool_and_float_behavior_is_currently_python_int_behavior() -> None:
    assert _maybe_int(True) == 1
    assert _maybe_int(False) == 0
    assert _maybe_int(1.5) == 1
    assert _maybe_int("1.5") is None


def test_extract_game_result_identity_uses_neutral_fallbacks_for_malformed_game_info_and_context() -> None:
    payload = {
        "identity": {"match_id": "", "game_number": None},
        "game_info": "not-a-dict",
    }

    assert _extract_game_result_identity(payload, {}) == ("", None, "", "", "")


def test_extract_game_result_identity_prefers_payload_values_when_context_keys_are_missing() -> None:
    payload = {
        "identity": {"match_id": "payload-match", "game_number": 2},
        "game_info": "not-a-dict",
        "winning_team_id": 1,
        "result_type": "ResultType_WinLoss",
        "reason": "ResultReason_Game",
    }

    assert _extract_game_result_identity(payload, {}) == (
        "payload-match",
        2,
        1,
        "ResultType_WinLoss",
        "ResultReason_Game",
    )


def test_has_match_scope_result_ignores_non_dictionary_results() -> None:
    payload = {
        "results": [
            "bad",
            None,
            {"scope": "MatchScope_Game", "winningTeamId": 1},
            {"scope": "MatchScope_Match", "winningTeamId": 2},
        ]
    }

    assert _has_match_scope_result(payload) is True


def test_has_match_scope_result_returns_false_for_only_malformed_results() -> None:
    assert _has_match_scope_result({"results": ["bad", None, 3]}) is False


def test_extract_starting_player_from_nested_raw_client_action() -> None:
    payload = {
        "type": "generic_client_action",
        "message_type": "ClientMessageType_ChooseStartingPlayerResp",
        "raw_client_action": {
            "payload": {
                "type": "ClientMessageType_ChooseStartingPlayerResp",
                "systemSeatId": 2,
            }
        },
    }

    assert _extract_starting_player_from_client_action(payload) == 2


def test_extract_starting_player_from_client_action_returns_raw_value_shape() -> None:
    assert _extract_starting_player_from_client_action({"systemSeatId": "2"}) == "2"


def test_extract_local_team_from_nested_raw_client_action() -> None:
    payload = {
        "type": "generic_client_action",
        "message_type": "ClientMessageType_ChooseStartingPlayerResp",
        "raw_client_action": {
            "payload": {
                "type": "ClientMessageType_ChooseStartingPlayerResp",
                "chooseStartingPlayerResp": {
                    "teamId": 2,
                    "systemSeatId": 2,
                },
            }
        },
    }

    assert _extract_local_team_from_client_action(payload) == 2


def test_extract_local_team_from_game_state_system_seat_ids() -> None:
    payload = {
        "raw_game_state": {
            "systemSeatIds": [2],
            "gameStateMessage": {
                "players": [
                    {"systemSeatNumber": 1, "teamId": 1},
                    {"systemSeatNumber": 2, "teamId": 2},
                ]
            },
        }
    }

    assert _extract_local_team_from_game_state(payload) == 2


def test_extract_starting_player_from_turn_one_game_state() -> None:
    payload = {
        "raw_game_state": {
            "gameStateMessage": {
                "players": [
                    {"systemSeatNumber": 1, "teamId": 1},
                    {"systemSeatNumber": 2, "teamId": 2},
                ],
                "turnInfo": {
                    "turnNumber": 1,
                    "activePlayer": 2,
                },
            }
        }
    }

    assert _extract_starting_player_from_game_state(payload) == 2


def test_extract_starting_player_from_game_state_returns_team_id_when_player_mapping_exists() -> None:
    payload = {
        "turn_info": {"turnNumber": 1, "activePlayer": 2},
        "players": [
            {"systemSeatNumber": 2, "teamId": 9},
        ],
    }

    assert _extract_starting_player_from_game_state(payload) == 9


def test_extract_starting_player_from_game_state_returns_active_seat_when_mapping_is_missing() -> None:
    payload = {
        "turn_info": {"turnNumber": 1, "activePlayer": 2},
        "players": [
            {"systemSeatNumber": 1, "teamId": 7},
        ],
    }

    assert _extract_starting_player_from_game_state(payload) == 2


def test_extract_local_private_hand_instance_ids_prefers_local_private_zone() -> None:
    payload = {
        "raw_game_state": {
            "systemSeatIds": [2],
            "gameStateMessage": {
                "zones": [
                    {
                        "type": "ZoneType_Hand",
                        "visibility": "Visibility_Private",
                        "ownerSeatId": 1,
                        "objectInstanceIds": [11, 12],
                    },
                    {
                        "type": "ZoneType_Hand",
                        "visibility": "Visibility_Private",
                        "ownerSeatId": 2,
                        "objectInstanceIds": [21, 22, 23],
                    },
                ]
            },
        }
    }

    assert _extract_local_private_hand_instance_ids(payload) == [21, 22, 23]


def test_extract_local_private_hand_instance_ids_accepts_malformed_owner_seat_as_local() -> None:
    payload = {
        "system_seat_ids": [2],
        "zones": [
            {
                "type": "ZoneType_Hand",
                "visibility": "Visibility_Private",
                "ownerSeatId": "not-a-seat",
                "objectInstanceIds": [11, "12", "bad"],
            },
            {
                "type": "ZoneType_Hand",
                "visibility": "Visibility_Private",
                "ownerSeatId": 2,
                "objectInstanceIds": [21],
            },
        ],
    }

    assert _extract_local_private_hand_instance_ids(payload) == [11, 12]


def test_extract_local_private_hand_instance_ids_returns_first_matching_private_hand_zone() -> None:
    payload = {
        "system_seat_ids": [2],
        "zones": [
            {
                "type": "ZoneType_Hand",
                "visibility": "Visibility_Private",
                "ownerSeatId": 2,
                "objectInstanceIds": [21],
            },
            {
                "type": "ZoneType_Hand",
                "visibility": "Visibility_Private",
                "ownerSeatId": 2,
                "objectInstanceIds": [22],
            },
        ],
    }

    assert _extract_local_private_hand_instance_ids(payload) == [21]


def test_extract_instance_grp_lookup_normalizes_game_objects() -> None:
    payload = {
        "raw_game_state": {
            "gameStateMessage": {
                "gameObjects": [
                    {"instanceId": 101, "grpId": 91829},
                    {"instanceId": "102", "overlayGrpId": "93940"},
                    {"instanceId": None, "grpId": 12345},
                ]
            }
        }
    }

    assert _extract_instance_grp_lookup(payload) == {
        101: 91829,
        102: 93940,
    }


def test_game_state_actions_prefers_top_level_then_current_raw_then_queued_raw() -> None:
    assert _game_state_actions(
        {
            "actions": [{"id": "top"}, "bad"],
            "raw_game_state": {"gameStateMessage": {"actions": [{"id": "raw"}]}},
        }
    ) == [{"id": "top"}]

    assert _game_state_actions({"raw_game_state": {"gameStateMessage": {"actions": [{"id": "raw"}, None]}}}) == [
        {"id": "raw"}
    ]

    assert _game_state_actions(
        {
            "raw_game_state": {
                "gameStateMessage": {},
                "queuedGameStateMessage": {"gameStateMessage": {"actions": [{"id": "queued"}, 3]}},
            }
        }
    ) == [{"id": "queued"}]


def test_game_state_annotations_prefers_top_level_then_current_raw_then_queued_raw() -> None:
    assert _game_state_annotations(
        {
            "annotations": [{"id": "top"}, "bad"],
            "raw_game_state": {"gameStateMessage": {"annotations": [{"id": "raw"}]}},
        }
    ) == [{"id": "top"}]

    assert _game_state_annotations(
        {"raw_game_state": {"gameStateMessage": {"annotations": [{"id": "raw"}, None]}}}
    ) == [{"id": "raw"}]

    assert _game_state_annotations(
        {
            "raw_game_state": {
                "gameStateMessage": {},
                "queuedGameStateMessage": {"gameStateMessage": {"annotations": [{"id": "queued"}, 3]}},
            }
        }
    ) == [{"id": "queued"}]


def test_event_datetime_and_safe_iso_use_valid_metadata_timestamp() -> None:
    timestamp = datetime(2026, 5, 12, 9, 30, 15, tzinfo=UTC)
    event = SimpleNamespace(metadata=SimpleNamespace(timestamp=timestamp))

    assert _event_datetime(event) is timestamp
    assert _safe_iso(event) == timestamp.isoformat()


def test_event_datetime_and_safe_iso_fall_back_when_timestamp_is_missing() -> None:
    before = datetime.now()
    result = _event_datetime(object())
    after = datetime.now()

    assert before <= result <= after
    assert isinstance(datetime.fromisoformat(_safe_iso(object())), datetime)


def test_hydrate_game_state_identity_uses_payload_then_context() -> None:
    payload = {
        "identity": {
            "match_id": "",
            "game_number": None,
            "turn_number": 2,
            "active_player_seat_id": 1,
            "phase": "Phase_Main1",
            "step": "Step_None",
            "stage": "",
        }
    }
    context = {
        "current_match_id": "match-context",
        "current_game_number": 3,
    }

    identity = _hydrate_game_state_identity(payload, context)

    assert identity["match_id"] == "match-context"
    assert identity["game_number"] == 3
    assert identity["turn_number"] == 2
    assert identity["identity_source"] == "context"


def test_extract_turn_info_reads_enriched_identity_payload() -> None:
    payload = {
        "identity": {
            "match_id": "match-enriched",
            "game_number": 2,
            "turn_number": 4,
            "active_player_seat_id": 1,
            "phase": "Phase_Combat",
            "step": "Step_DeclareAttack",
            "stage": "GameStage_Play",
        }
    }

    assert _extract_turn_info(payload) == (
        "match-enriched",
        2,
        4,
        1,
        "Phase_Combat",
        "Step_DeclareAttack",
        "GameStage_Play",
    )


def test_extract_turn_info_falls_back_to_queued_message_when_current_message_is_partial() -> None:
    payload = {
        "raw_game_state": {
            "gameStateMessage": {
                "gameInfo": {
                    "matchID": "match-current",
                    "gameNumber": 1,
                }
            },
            "queuedGameStateMessage": {
                "gameStateMessage": {
                    "turnInfo": {
                        "turnNumber": 3,
                        "activePlayer": 2,
                        "phase": "Phase_Main1",
                        "step": "Step_None",
                    }
                }
            },
        }
    }

    assert _extract_turn_info(payload) == (
        "match-current",
        1,
        3,
        2,
        "Phase_Main1",
        "Step_None",
        "",
    )


def test_extract_local_private_hand_instance_ids_falls_back_to_queued_zones() -> None:
    payload = {
        "raw_game_state": {
            "systemSeatIds": [2],
            "gameStateMessage": {
                "players": [
                    {"systemSeatNumber": 1, "teamId": 1},
                    {"systemSeatNumber": 2, "teamId": 2},
                ]
            },
            "queuedGameStateMessage": {
                "gameStateMessage": {
                    "zones": [
                        {
                            "type": "ZoneType_Hand",
                            "visibility": "Visibility_Private",
                            "ownerSeatId": 2,
                            "objectInstanceIds": [21, 22, 23],
                        }
                    ]
                }
            },
        }
    }

    assert _extract_local_private_hand_instance_ids(payload) == [21, 22, 23]


def test_extract_instance_grp_lookup_falls_back_to_queued_game_objects() -> None:
    payload = {
        "raw_game_state": {
            "gameStateMessage": {
                "turnInfo": {"turnNumber": 1}
            },
            "queuedGameStateMessage": {
                "gameStateMessage": {
                    "gameObjects": [
                        {"instanceId": 101, "grpId": 91829},
                        {"instanceId": "102", "overlayGrpId": "93940"},
                    ]
                }
            },
        }
    }

    assert _extract_instance_grp_lookup(payload) == {
        101: 91829,
        102: 93940,
    }
