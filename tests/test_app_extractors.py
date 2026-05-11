from mythic_edge_parser.app.extractors import (
    _extract_instance_grp_lookup,
    _extract_local_private_hand_instance_ids,
    _extract_local_team_from_client_action,
    _extract_local_team_from_game_state,
    _extract_starting_player_from_client_action,
    _extract_starting_player_from_game_state,
    _extract_turn_info,
    _hydrate_game_state_identity,
)


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
