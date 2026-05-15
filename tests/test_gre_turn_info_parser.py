from copy import deepcopy

import pytest

from mythic_edge_parser.parsers.gre import game_state
from mythic_edge_parser.parsers.gre.turn_info import build_turn_info


def test_build_turn_info_returns_empty_for_missing_turn_info_dict() -> None:
    assert build_turn_info({}) == {}
    assert build_turn_info({"turnInfo": "bad"}) == {}
    assert build_turn_info({"turnInfo": {}}) == {}


def test_build_turn_info_normalizes_expected_fields() -> None:
    payload = build_turn_info(
        {
            "turnInfo": {
                "turnNumber": "3",
                "phase": "Phase_Main1",
                "step": "Step_PreCombatMain",
                "activePlayer": "2",
                "activePlayerSeatId": "1",
                "decisionPlayer": "1",
                "priorityPlayer": "2",
                "nextPhase": "Phase_Combat",
                "nextStep": "Step_BeginCombat",
                "futureField": "ignored",
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


@pytest.mark.parametrize(
    ("active_player", "active_player_seat_id", "expected"),
    [
        ("", "1", 1),
        (None, "1", 1),
        (0, "1", 0),
        (False, "1", 0),
        ("bad", "1", None),
        ([], "1", None),
        ({}, "1", None),
    ],
)
def test_build_turn_info_active_player_precedence(
    active_player: object,
    active_player_seat_id: object,
    expected: int | None,
) -> None:
    payload = build_turn_info(
        {
            "turnInfo": {
                "activePlayer": active_player,
                "activePlayerSeatId": active_player_seat_id,
            }
        }
    )

    assert payload["active_player_seat_id"] == expected


def test_build_turn_info_locks_integer_conversion_boundaries() -> None:
    payload = build_turn_info(
        {
            "turnInfo": {
                "turnNumber": " 3 ",
                "activePlayer": "-2",
                "decisionPlayer": True,
                "priorityPlayer": 4.9,
            }
        }
    )

    assert payload["turn_number"] == 3
    assert payload["active_player_seat_id"] == -2
    assert payload["decision_player_seat_id"] == 1
    assert payload["priority_player_seat_id"] == 4

    malformed = build_turn_info(
        {
            "turnInfo": {
                "turnNumber": "1.5",
                "activePlayer": None,
                "activePlayerSeatId": "bad",
                "decisionPlayer": object(),
                "priorityPlayer": "bad",
            }
        }
    )

    assert malformed["turn_number"] is None
    assert malformed["active_player_seat_id"] is None
    assert malformed["decision_player_seat_id"] is None
    assert malformed["priority_player_seat_id"] is None


def test_build_turn_info_locks_string_conversion_boundaries() -> None:
    falsey_payload = build_turn_info(
        {
            "turnInfo": {
                "phase": 0,
                "step": False,
                "nextPhase": [],
                "nextStep": {},
            }
        }
    )

    assert falsey_payload["phase"] == ""
    assert falsey_payload["step"] == ""
    assert falsey_payload["next_phase"] == ""
    assert falsey_payload["next_step"] == ""

    truthy_payload = build_turn_info(
        {
            "turnInfo": {
                "phase": ["Phase_Main1"],
                "step": {"step": "Step_PreCombatMain"},
            }
        }
    )

    assert truthy_payload["phase"] == "['Phase_Main1']"
    assert truthy_payload["step"] == "{'step': 'Step_PreCombatMain'}"


def test_build_turn_info_does_not_mutate_input() -> None:
    gsm = {
        "turnInfo": {
            "turnNumber": "1",
            "phase": "Phase_Main1",
            "extra": {"nested": "value"},
        },
        "gameInfo": {"matchID": "match-1"},
    }
    before = deepcopy(gsm)

    payload = build_turn_info(gsm)
    payload["turn_number"] = 99
    payload["phase"] = "Changed"

    assert gsm == before


def test_game_state_payload_carries_turn_info_output(monkeypatch: pytest.MonkeyPatch) -> None:
    expected_turn_info = {
        "turn_number": 4,
        "phase": "Phase_Main1",
        "step": "Step_PreCombatMain",
        "active_player_seat_id": 2,
        "decision_player_seat_id": 1,
        "priority_player_seat_id": 2,
        "next_phase": "Phase_Combat",
        "next_step": "Step_BeginCombat",
    }
    calls: list[dict[str, object]] = []

    def fake_build_turn_info(gsm: dict[str, object]) -> dict[str, object]:
        calls.append(gsm)
        return expected_turn_info

    monkeypatch.setattr(game_state, "build_turn_info", fake_build_turn_info)
    gsm = {
        "gameInfo": {
            "matchID": "match-1",
            "gameNumber": 1,
            "stage": "GameStage_Play",
        }
    }

    payload = game_state.build_game_state_payload({"type": "GREMessageType_GameStateMessage"}, gsm)

    assert calls == [gsm]
    assert payload["turn_info"] is expected_turn_info
    assert payload["turn_number"] == 4
    assert payload["active_player_seat_id"] == 2
    assert payload["identity"]["turn_number"] == 4
    assert payload["identity"]["active_player_seat_id"] == 2
    assert payload["identity"]["phase"] == "Phase_Main1"
    assert payload["identity"]["step"] == "Step_PreCombatMain"


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
