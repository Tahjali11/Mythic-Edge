import pytest

from mythic_edge_parser.parsers.gre.game_result import (
    build_game_result_payload,
    is_game_over,
)


def test_is_game_over_uses_game_info_then_top_level_stage() -> None:
    assert is_game_over({"game_info": {"stage": "GameStage_GameOver"}}) is True
    assert is_game_over({"stage": "GameStage_GameOver"}) is True
    assert is_game_over({"game_info": {"stage": "GameStage_Play"}}) is False


def test_is_game_over_does_not_infer_from_match_state_or_results() -> None:
    assert (
        is_game_over(
            {
                "game_info": {
                    "matchState": "MatchState_GameComplete",
                    "results": [{"scope": "MatchScope_Game", "winningTeamId": 1}],
                },
            }
        )
        is False
    )


def test_is_game_over_handles_malformed_game_info_safely() -> None:
    assert is_game_over({"game_info": "bad", "stage": "GameStage_Play"}) is False


def test_build_game_result_payload_happy_path_fields() -> None:
    game_state_payload = {
        "game_info": {
            "stage": "GameStage_GameOver",
            "matchState": "MatchState_GameComplete",
            "results": [
                {
                    "scope": "MatchScope_Game",
                    "winningTeamId": 2,
                    "result": "ResultType_WinLoss",
                    "reason": "ResultReason_Game",
                }
            ],
        },
        "identity": {"match_id": "match-1", "game_number": 3},
        "game_state_id": "state-7",
        "message_type": "GREMessageType_GameStateMessage",
    }

    payload = build_game_result_payload(game_state_payload)

    assert payload["type"] == "game_result"
    assert payload["source"] == "gre_game_state"
    assert payload["stage"] == "GameStage_GameOver"
    assert payload["match_state"] == "MatchState_GameComplete"
    assert payload["winning_team_id"] == 2
    assert payload["result_type"] == "ResultType_WinLoss"
    assert payload["reason"] == "ResultReason_Game"
    assert payload["identity"] == {"match_id": "match-1", "game_number": 3}
    assert payload["game_state_id"] == "state-7"
    assert payload["message_type"] == "GREMessageType_GameStateMessage"


def test_build_game_result_payload_shallow_copies_output_views() -> None:
    game_state_payload = {
        "game_info": {
            "stage": "GameStage_GameOver",
            "matchState": "MatchState_GameComplete",
            "results": [
                {
                    "scope": "MatchScope_Game",
                    "winningTeamId": 1,
                    "result": "ResultType_WinLoss",
                    "reason": "ResultReason_Game",
                }
            ],
        },
        "identity": {"match_id": "match-1", "game_number": 1},
        "game_state_id": 7,
        "message_type": "GREMessageType_GameStateMessage",
    }

    payload = build_game_result_payload(game_state_payload)

    payload["game_info"]["stage"] = "Changed"
    payload["identity"]["match_id"] = "changed"
    payload["results"].append({"scope": "MatchScope_Match"})

    assert game_state_payload["game_info"]["stage"] == "GameStage_GameOver"
    assert game_state_payload["identity"]["match_id"] == "match-1"
    assert len(game_state_payload["game_info"]["results"]) == 1


def test_build_game_result_payload_keeps_nested_output_views_shallow() -> None:
    result = {
        "scope": "MatchScope_Game",
        "winningTeamId": 1,
        "result": "ResultType_WinLoss",
        "reason": "ResultReason_Game",
    }
    game_state_payload = {
        "game_info": {
            "stage": "GameStage_GameOver",
            "results": [result],
        },
        "identity": {"nested": {"value": "original"}},
    }

    payload = build_game_result_payload(game_state_payload)

    assert payload["game_info"] is not game_state_payload["game_info"]
    assert payload["identity"] is not game_state_payload["identity"]
    assert payload["results"] is not game_state_payload["game_info"]["results"]
    assert payload["results"][0] is result
    assert payload["identity"]["nested"] is game_state_payload["identity"]["nested"]


def test_build_game_result_payload_handles_missing_and_malformed_sections() -> None:
    payload = build_game_result_payload(
        {
            "game_info": "bad",
            "identity": "bad",
            "game_state_id": 11,
        }
    )

    assert payload == {
        "type": "game_result",
        "source": "gre_game_state",
        "stage": "",
        "match_state": "",
        "winning_team_id": 0,
        "result_type": "",
        "reason": "",
        "results": [],
        "game_info": {},
        "identity": {},
        "game_state_id": 11,
        "message_type": "",
    }


def test_build_game_result_payload_non_list_results_yields_empty_results() -> None:
    payload = build_game_result_payload(
        {
            "game_info": {
                "stage": "GameStage_GameOver",
                "results": {"scope": "MatchScope_Game", "winningTeamId": 1},
            }
        }
    )

    assert payload["results"] == []
    assert payload["winning_team_id"] == 0
    assert payload["result_type"] == ""
    assert payload["reason"] == ""


def test_build_game_result_payload_missing_selected_result_fields_use_defaults() -> None:
    payload = build_game_result_payload(
        {
            "game_info": {
                "stage": "GameStage_GameOver",
                "results": [{"scope": "MatchScope_Game", "winningTeamId": 1}],
            }
        }
    )

    assert payload["winning_team_id"] == 1
    assert payload["result_type"] == ""
    assert payload["reason"] == ""


def test_build_game_result_payload_top_level_stage_fallback_is_detection_only() -> None:
    game_state_payload = {"stage": "GameStage_GameOver", "game_info": {}}

    assert is_game_over(game_state_payload) is True
    assert build_game_result_payload(game_state_payload)["stage"] == ""


def test_build_game_result_payload_uses_latest_game_scope_result_for_top_level_winner() -> None:
    payload = build_game_result_payload(
        {
            "game_info": {
                "stage": "GameStage_GameOver",
                "results": [
                    {
                        "scope": "MatchScope_Game",
                        "winningTeamId": 1,
                        "result": "ResultType_WinLoss",
                        "reason": "ResultReason_FirstGame",
                    },
                    {
                        "scope": "MatchScope_Match",
                        "winningTeamId": 3,
                        "result": "ResultType_WinLoss",
                        "reason": "ResultReason_Match",
                    },
                    {
                        "scope": "MatchScope_Game",
                        "winningTeamId": 2,
                        "result": "ResultType_WinLoss",
                        "reason": "ResultReason_LatestGame",
                    },
                ],
            }
        }
    )

    assert payload["winning_team_id"] == 2
    assert payload["result_type"] == "ResultType_WinLoss"
    assert payload["reason"] == "ResultReason_LatestGame"


@pytest.mark.parametrize("unknown_winner", [None, "", 0, 0.0, "0", " 0 ", False, True])
def test_build_game_result_payload_ignores_unknown_game_scope_winners(unknown_winner) -> None:
    payload = build_game_result_payload(
        {
            "game_info": {
                "stage": "GameStage_GameOver",
                "results": [
                    {
                        "scope": "MatchScope_Game",
                        "winningTeamId": unknown_winner,
                        "result": "ResultType_WinLoss",
                        "reason": "ResultReason_Game",
                    },
                    {
                        "scope": "MatchScope_Match",
                        "winningTeamId": 2,
                        "result": "ResultType_WinLoss",
                        "reason": "ResultReason_Match",
                    },
                ],
            }
        }
    )

    assert payload["winning_team_id"] == 0
    assert payload["result_type"] == ""
    assert payload["reason"] == ""


def test_build_game_result_payload_keeps_earlier_known_game_winner_when_later_game_winner_unknown() -> None:
    payload = build_game_result_payload(
        {
            "game_info": {
                "stage": "GameStage_GameOver",
                "results": [
                    {
                        "scope": "MatchScope_Game",
                        "winningTeamId": 2,
                        "result": "ResultType_WinLoss",
                        "reason": "ResultReason_Known",
                    },
                    {
                        "scope": "MatchScope_Game",
                        "winningTeamId": "0",
                        "result": "ResultType_WinLoss",
                        "reason": "ResultReason_Unknown",
                    },
                ],
            }
        }
    )

    assert payload["winning_team_id"] == 2
    assert payload["reason"] == "ResultReason_Known"


def test_build_game_result_payload_accepts_exact_game_scope_alias_and_preserves_non_dict_results() -> None:
    malformed_result = "bad"
    payload = build_game_result_payload(
        {
            "game_info": {
                "stage": "GameStage_GameOver",
                "results": [
                    malformed_result,
                    {
                        "scope": "UnknownScope",
                        "winningTeamId": 9,
                        "result": "ResultType_Unknown",
                        "reason": "ResultReason_Unknown",
                    },
                    {
                        "scope": "Match",
                        "winningTeamId": 3,
                        "result": "ResultType_Match",
                        "reason": "ResultReason_Match",
                    },
                    {
                        "scope": "Game",
                        "winningTeamId": "4",
                        "result": "ResultType_Game",
                        "reason": "ResultReason_GameAlias",
                    },
                ],
            }
        }
    )

    assert payload["results"][0] is malformed_result
    assert payload["winning_team_id"] == "4"
    assert payload["result_type"] == "ResultType_Game"
    assert payload["reason"] == "ResultReason_GameAlias"


def test_build_game_result_payload_ignores_snake_case_winner_for_parser_top_level_selection() -> None:
    payload = build_game_result_payload(
        {
            "game_info": {
                "stage": "GameStage_GameOver",
                "results": [
                    {
                        "scope": "MatchScope_Game",
                        "winning_team_id": 2,
                        "result_type": "ResultType_Snake",
                        "reason": "ResultReason_Snake",
                    },
                ],
            }
        }
    )

    assert payload["winning_team_id"] == 0
    assert payload["result_type"] == ""
    assert payload["reason"] == ""


def test_build_game_result_payload_does_not_promote_match_scope_result_to_game_winner() -> None:
    payload = build_game_result_payload(
        {
            "game_info": {
                "stage": "GameStage_GameOver",
                "results": [
                    "bad",
                    {
                        "scope": "MatchScope_Match",
                        "winningTeamId": 2,
                        "result": "ResultType_WinLoss",
                        "reason": "ResultReason_Concede",
                    },
                ],
            }
        }
    )

    assert payload["winning_team_id"] == 0
    assert payload["result_type"] == ""
    assert payload["reason"] == ""
