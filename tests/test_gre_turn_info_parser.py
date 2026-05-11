from mythic_edge_parser.parsers.gre.turn_info import build_turn_info


def test_build_turn_info_returns_empty_for_missing_turn_info_dict() -> None:
    assert build_turn_info({}) == {}
    assert build_turn_info({"turnInfo": "bad"}) == {}


def test_build_turn_info_normalizes_expected_fields() -> None:
    payload = build_turn_info(
        {
            "turnInfo": {
                "turnNumber": "3",
                "phase": "Phase_Main1",
                "step": "Step_PreCombatMain",
                "activePlayer": "2",
                "decisionPlayer": "1",
                "priorityPlayer": "2",
                "nextPhase": "Phase_Combat",
                "nextStep": "Step_BeginCombat",
            }
        }
    )

    assert payload == {
        "turn_number": 3,
        "phase": "Phase_Main1",
        "step": "Step_PreCombatMain",
        "active_player_seat_id": 2,
        "decision_player_seat_id": 1,
        "priority_player_seat_id": 2,
        "next_phase": "Phase_Combat",
        "next_step": "Step_BeginCombat",
    }


def test_build_turn_info_falls_back_to_active_player_seat_id() -> None:
    payload = build_turn_info(
        {
            "turnInfo": {
                "activePlayerSeatId": "2",
                "decisionPlayer": None,
            }
        }
    )

    assert payload["active_player_seat_id"] == 2
    assert payload["decision_player_seat_id"] is None


def test_build_turn_info_handles_malformed_values_safely() -> None:
    payload = build_turn_info(
        {
            "turnInfo": {
                "turnNumber": "bad",
                "phase": None,
                "step": None,
                "activePlayer": "",
                "activePlayerSeatId": "bad",
                "priorityPlayer": "bad",
                "nextPhase": None,
                "nextStep": None,
            }
        }
    )

    assert payload == {
        "turn_number": None,
        "phase": "",
        "step": "",
        "active_player_seat_id": None,
        "decision_player_seat_id": None,
        "priority_player_seat_id": None,
        "next_phase": "",
        "next_step": "",
    }
