from mythic_edge_parser.parsers.gre.game_result import (
    build_game_result_payload,
    is_game_over,
)


def test_is_game_over_uses_game_info_then_top_level_stage() -> None:
    assert is_game_over({"game_info": {"stage": "GameStage_GameOver"}}) is True
    assert is_game_over({"stage": "GameStage_GameOver"}) is True
    assert is_game_over({"game_info": {"stage": "GameStage_Play"}}) is False


def test_is_game_over_handles_malformed_game_info_safely() -> None:
    assert is_game_over({"game_info": "bad", "stage": "GameStage_Play"}) is False


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
