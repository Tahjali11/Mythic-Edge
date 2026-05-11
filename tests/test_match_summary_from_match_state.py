from datetime import UTC, datetime

from mythic_edge_parser.app import state
from mythic_edge_parser.events import ClientActionEvent, EventMetadata, GameResultEvent, GameStateEvent, MatchStateEvent


def test_match_state_final_results_populate_match_summary() -> None:
    state._MATCH_SUMMARIES.clear()
    state._CONTEXT["current_match_id"] = ""
    state._CONTEXT["current_game_number"] = ""
    state._CONTEXT["current_player_team"] = ""

    event = MatchStateEvent(
        EventMetadata(datetime(2026, 4, 17, 23, 33, 48, tzinfo=UTC), b"raw"),
        {
            "type": "match_completed",
            "match_id": "m1",
            "state_type": "MatchGameRoomStateType_MatchCompleted",
            "players": [
                {"player_name": "P1", "team_id": 1},
                {"player_name": "P2", "team_id": 2},
            ],
            "game_results": [
                {
                    "scope": "MatchScope_Game",
                    "result": "ResultType_WinLoss",
                    "winning_team_id": 1,
                    "reason": "ResultReason_Game",
                },
                {
                    "scope": "MatchScope_Game",
                    "result": "ResultType_WinLoss",
                    "winning_team_id": 2,
                    "reason": "ResultReason_Concede",
                },
                {
                    "scope": "MatchScope_Game",
                    "result": "ResultType_WinLoss",
                    "winning_team_id": 2,
                    "reason": "ResultReason_Concede",
                },
                {
                    "scope": "MatchScope_Match",
                    "result": "ResultType_WinLoss",
                    "winning_team_id": 2,
                    "reason": "ResultReason_Concede",
                },
            ],
        },
    )

    state._update_match_summary(event)
    summary = state._MATCH_SUMMARIES["m1"]

    assert summary.games[1].winner_team == 1
    assert summary.games[2].winner_team == 2
    assert summary.games[3].winner_team == 2
    assert summary.match_winner_team == 2
    assert summary.match_wl == "L"


def test_local_team_is_corrected_from_client_action_when_match_player_order_is_reversed() -> None:
    state._MATCH_SUMMARIES.clear()
    state._MULLIGAN_COUNTS.clear()
    state._LAST_POSTED_MATCH_LOG_ROWS.clear()
    state._CONTEXT["current_match_id"] = ""
    state._CONTEXT["current_game_number"] = ""
    state._CONTEXT["current_player_team"] = ""

    started = MatchStateEvent(
        EventMetadata(datetime(2026, 4, 18, 19, 12, 6, tzinfo=UTC), b"raw"),
        {
            "type": "match_started",
            "match_id": "m2",
            "state_type": "MatchGameRoomStateType_Playing",
            "players": [
                {"player_name": "OpponentFirst", "team_id": 1, "system_seat_id": 1},
                {"player_name": "LocalSecond", "team_id": 2, "system_seat_id": 2},
            ],
        },
    )
    state._update_match_summary(started)

    choose_start = ClientActionEvent(
        EventMetadata(datetime(2026, 4, 18, 19, 12, 18, tzinfo=UTC), b"raw"),
        {
            "type": "generic_client_action",
            "message_type": "ClientMessageType_ChooseStartingPlayerResp",
            "raw_client_action": {
                "payload": {
                    "type": "ClientMessageType_ChooseStartingPlayerResp",
                    "gameStateId": 1,
                    "respId": 5,
                    "chooseStartingPlayerResp": {
                        "systemSeatId": 2,
                        "teamId": 2,
                    },
                }
            },
        },
    )
    state._update_match_summary(choose_start)

    game_one = GameResultEvent(
        EventMetadata(datetime(2026, 4, 18, 19, 17, 29, tzinfo=UTC), b"raw"),
        {
            "type": "game_result",
            "winning_team_id": 2,
            "result_type": "ResultType_WinLoss",
            "reason": "ResultReason_Concede",
            "game_info": {"matchID": "m2", "gameNumber": 1},
        },
    )
    state._update_match_summary(game_one)

    game_two_and_match = GameResultEvent(
        EventMetadata(datetime(2026, 4, 18, 19, 25, 35, tzinfo=UTC), b"raw"),
        {
            "type": "game_result",
            "winning_team_id": 2,
            "result_type": "ResultType_WinLoss",
            "reason": "ResultReason_Game",
            "match_state": "MatchState_MatchComplete",
            "results": [
                {
                    "scope": "MatchScope_Game",
                    "winningTeamId": 2,
                    "result": "ResultType_WinLoss",
                    "reason": "ResultReason_Concede",
                },
                {
                    "scope": "MatchScope_Game",
                    "winningTeamId": 2,
                    "result": "ResultType_WinLoss",
                    "reason": "ResultReason_Game",
                },
                {
                    "scope": "MatchScope_Match",
                    "winningTeamId": 2,
                    "result": "ResultType_WinLoss",
                    "reason": "ResultReason_Game",
                },
            ],
            "game_info": {"matchID": "m2", "gameNumber": 2},
        },
    )
    state._update_match_summary(game_two_and_match)

    row = state.build_match_log_row("m2")
    assert row is not None
    assert row["G1 Play / Draw"] == "Play"
    assert row["Game 1 Result"] == "W"
    assert row["Game 2 Result"] == "W"
    assert row["Games Won"] == 2
    assert row["Games Lost"] == 0
    assert row["Match Win?"] == "W"


def test_live_match_log_update_only_advances_when_summary_changes() -> None:
    state._MATCH_SUMMARIES.clear()
    state._MULLIGAN_COUNTS.clear()
    state._LAST_POSTED_MATCH_LOG_ROWS.clear()
    state._CONTEXT["current_match_id"] = ""
    state._CONTEXT["current_game_number"] = ""
    state._CONTEXT["current_player_team"] = ""

    started = MatchStateEvent(
        EventMetadata(datetime(2026, 4, 18, 22, 25, 55, tzinfo=UTC), b"raw"),
        {
            "type": "match_started",
            "match_id": "m_live",
            "state_type": "MatchGameRoomStateType_Playing",
            "players": [
                {"player_name": "LocalFirst", "team_id": 1, "system_seat_id": 1},
                {"player_name": "OpponentSecond", "team_id": 2, "system_seat_id": 2},
            ],
        },
    )
    state._update_match_summary(started)

    live_row, changed_fields, is_final = state.build_match_log_update("m_live")
    assert live_row is not None
    assert is_final is False
    assert live_row["MTGA Sync Status"] == "Live"
    assert "MTGA Match ID" in changed_fields

    state.mark_match_log_posted("m_live", live_row)
    repeated_row, repeated_changes, repeated_final = state.build_match_log_update("m_live")
    assert repeated_row is None
    assert repeated_changes == []
    assert repeated_final is False

    game_one = GameResultEvent(
        EventMetadata(datetime(2026, 4, 18, 22, 35, 40, tzinfo=UTC), b"raw"),
        {
            "type": "game_result",
            "winning_team_id": 1,
            "result_type": "ResultType_WinLoss",
            "reason": "ResultReason_Concede",
            "game_info": {"matchID": "m_live", "gameNumber": 1},
        },
    )
    state._update_match_summary(game_one)

    progressed_row, progressed_changes, progressed_final = state.build_match_log_update("m_live")
    assert progressed_row is not None
    assert progressed_final is False
    assert progressed_row["Game 1 Result"] == "W"
    assert "Game 1 Result" in progressed_changes

    state.mark_match_log_posted("m_live", progressed_row)

    match_result = GameResultEvent(
        EventMetadata(datetime(2026, 4, 18, 22, 40, 0, tzinfo=UTC), b"raw"),
        {
            "type": "game_result",
            "winning_team_id": 1,
            "result_type": "ResultType_WinLoss",
            "reason": "ResultReason_Game",
            "match_state": "MatchState_MatchComplete",
            "results": [
                {
                    "scope": "MatchScope_Game",
                    "winningTeamId": 1,
                    "result": "ResultType_WinLoss",
                    "reason": "ResultReason_Concede",
                },
                {
                    "scope": "MatchScope_Match",
                    "winningTeamId": 1,
                    "result": "ResultType_WinLoss",
                    "reason": "ResultReason_Game",
                },
            ],
            "game_info": {"matchID": "m_live", "gameNumber": 1},
        },
    )
    state._update_match_summary(match_result)

    final_row, final_changes, final_is_final = state.build_match_log_update("m_live")
    assert final_row is not None
    assert final_is_final is True
    assert final_row["MTGA Sync Status"] == "Final"
    assert final_row["Match Win?"] == "W"
    assert "MTGA End Time" in final_changes


def test_turn_one_game_state_populates_game_one_play_draw_without_choose_starting_player_resp() -> None:
    state._MATCH_SUMMARIES.clear()
    state._MULLIGAN_COUNTS.clear()
    state._LAST_POSTED_MATCH_LOG_ROWS.clear()
    state._LAST_POSTED_GAME_LOG_ROWS.clear()
    state._CONTEXT["current_match_id"] = ""
    state._CONTEXT["current_game_number"] = ""
    state._CONTEXT["current_player_team"] = ""

    started = MatchStateEvent(
        EventMetadata(datetime(2026, 4, 19, 0, 56, 45, tzinfo=UTC), b"raw"),
        {
            "type": "match_started",
            "match_id": "m_turn1",
            "state_type": "MatchGameRoomStateType_Playing",
            "players": [
                {"player_name": "LocalFirst", "team_id": 1, "system_seat_id": 1},
                {"player_name": "OpponentSecond", "team_id": 2, "system_seat_id": 2},
            ],
        },
    )
    state._update_match_summary(started)

    turn_one = GameStateEvent(
        EventMetadata(datetime(2026, 4, 19, 0, 57, 4, tzinfo=UTC), b"raw"),
        {
            "type": "game_state_message",
            "game_info": {"matchID": "m_turn1", "gameNumber": 1},
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
            },
        },
    )
    state._update_match_summary(turn_one)

    completed = MatchStateEvent(
        EventMetadata(datetime(2026, 4, 19, 1, 17, 5, tzinfo=UTC), b"raw"),
        {
            "type": "match_completed",
            "match_id": "m_turn1",
            "state_type": "MatchGameRoomStateType_MatchCompleted",
            "players": [
                {"player_name": "LocalFirst", "team_id": 1, "system_seat_id": 1},
                {"player_name": "OpponentSecond", "team_id": 2, "system_seat_id": 2},
            ],
            "game_results": [
                {
                    "scope": "MatchScope_Game",
                    "result": "ResultType_WinLoss",
                    "winning_team_id": 1,
                    "reason": "ResultReason_Concede",
                },
                {
                    "scope": "MatchScope_Match",
                    "result": "ResultType_WinLoss",
                    "winning_team_id": 1,
                    "reason": "ResultReason_Game",
                },
            ],
        },
    )
    state._update_match_summary(completed)

    row = state.build_match_log_row("m_turn1")
    assert row is not None
    assert row["G1 Play / Draw"] == "Draw"


def test_turn_one_game_state_captures_opening_hand_when_arena_lookup_resolves_cards() -> None:
    state._MATCH_SUMMARIES.clear()
    state._MULLIGAN_COUNTS.clear()
    state._GAME_INSTANCE_GRP_IDS.clear()
    state._HAND_SNAPSHOT_HISTORY.clear()
    state._LATEST_HAND_SNAPSHOT.clear()
    state._BOTTOMED_CARDS_CAPTURED.clear()
    state._ARENA_CARD_LOOKUP = {
        "91829": {"name": "Forest"},
        "93940": {"name": "Llanowar Elves"},
        "98436": {"name": "Cut Down"},
        "72579": {"name": "Swamp"},
        "86752": {"name": "Obyra's Attendants // Desperate Parry"},
        "90452": {"name": "Go for the Throat"},
        "87235": {"name": "Faerie Dreamthief"},
    }
    state._ARENA_CARD_LOOKUP_READY = True
    state._CONTEXT["current_match_id"] = ""
    state._CONTEXT["current_game_number"] = ""
    state._CONTEXT["current_player_team"] = ""
    try:
        started = MatchStateEvent(
            EventMetadata(datetime(2026, 4, 20, 21, 14, 0, tzinfo=UTC), b"raw"),
            {
                "type": "match_started",
                "match_id": "m_hand",
                "state_type": "MatchGameRoomStateType_Playing",
                "players": [
                    {"player_name": "LocalPlayer", "team_id": 1, "system_seat_id": 1},
                    {"player_name": "Opponent", "team_id": 2, "system_seat_id": 2},
                ],
            },
        )
        state._update_match_summary(started)

        opening_state = GameStateEvent(
            EventMetadata(datetime(2026, 4, 20, 21, 14, 12, tzinfo=UTC), b"raw"),
            {
                "type": "game_state_message",
                "game_info": {"matchID": "m_hand", "gameNumber": 1},
                "raw_game_state": {
                    "systemSeatIds": [1],
                    "gameStateMessage": {
                        "gameInfo": {"matchID": "m_hand", "gameNumber": 1},
                        "players": [
                            {"systemSeatNumber": 1, "teamId": 1},
                            {"systemSeatNumber": 2, "teamId": 2},
                        ],
                        "turnInfo": {"turnNumber": 1, "activePlayer": 1},
                        "zones": [
                            {
                                "type": "ZoneType_Hand",
                                "visibility": "Visibility_Private",
                                "ownerSeatId": 1,
                                "objectInstanceIds": [101, 102, 103, 104, 105, 106, 107],
                            }
                        ],
                        "gameObjects": [
                            {"instanceId": 101, "grpId": 91829},
                            {"instanceId": 102, "grpId": 93940},
                            {"instanceId": 103, "grpId": 98436},
                            {"instanceId": 104, "grpId": 72579},
                            {"instanceId": 105, "grpId": 86752},
                            {"instanceId": 106, "grpId": 90452},
                            {"instanceId": 107, "grpId": 87235},
                        ],
                    },
                },
            },
        )
        state._update_match_summary(opening_state)

        summary = state._MATCH_SUMMARIES["m_hand"]
        assert summary.games[1].opening_hand == [
            "Forest",
            "Llanowar Elves",
            "Cut Down",
            "Swamp",
            "Obyra's Attendants // Desperate Parry",
            "Go for the Throat",
            "Faerie Dreamthief",
        ]
    finally:
        state._ARENA_CARD_LOOKUP = None
        state._ARENA_CARD_LOOKUP_READY = False


def test_turn_one_game_state_keeps_partial_opening_hand_when_lookup_is_incomplete() -> None:
    state._MATCH_SUMMARIES.clear()
    state._MULLIGAN_COUNTS.clear()
    state._GAME_INSTANCE_GRP_IDS.clear()
    state._HAND_SNAPSHOT_HISTORY.clear()
    state._LATEST_HAND_SNAPSHOT.clear()
    state._BOTTOMED_CARDS_CAPTURED.clear()
    state._ARENA_CARD_LOOKUP = {
        "91829": {"name": "Forest"},
    }
    state._ARENA_CARD_LOOKUP_READY = True
    state._CONTEXT["current_match_id"] = ""
    state._CONTEXT["current_game_number"] = ""
    state._CONTEXT["current_player_team"] = ""
    try:
        started = MatchStateEvent(
            EventMetadata(datetime(2026, 4, 20, 21, 30, 0, tzinfo=UTC), b"raw"),
            {
                "type": "match_started",
                "match_id": "m_partial_hand",
                "state_type": "MatchGameRoomStateType_Playing",
                "players": [
                    {"player_name": "LocalPlayer", "team_id": 1, "system_seat_id": 1},
                    {"player_name": "Opponent", "team_id": 2, "system_seat_id": 2},
                ],
            },
        )
        state._update_match_summary(started)

        opening_state = GameStateEvent(
            EventMetadata(datetime(2026, 4, 20, 21, 30, 12, tzinfo=UTC), b"raw"),
            {
                "type": "game_state_message",
                "game_info": {"matchID": "m_partial_hand", "gameNumber": 1},
                "raw_game_state": {
                    "systemSeatIds": [1],
                    "gameStateMessage": {
                        "gameInfo": {"matchID": "m_partial_hand", "gameNumber": 1},
                        "players": [
                            {"systemSeatNumber": 1, "teamId": 1},
                            {"systemSeatNumber": 2, "teamId": 2},
                        ],
                        "turnInfo": {"turnNumber": 1, "activePlayer": 1},
                        "zones": [
                            {
                                "type": "ZoneType_Hand",
                                "visibility": "Visibility_Private",
                                "ownerSeatId": 1,
                                "objectInstanceIds": [101, 102, 103, 104, 105, 106, 107],
                            }
                        ],
                        "gameObjects": [
                            {"instanceId": 101, "grpId": 91829},
                            {"instanceId": 102, "grpId": 99999},
                            {"instanceId": 103, "grpId": 91829},
                            {"instanceId": 104, "grpId": 99998},
                            {"instanceId": 105, "grpId": 91829},
                            {"instanceId": 106, "grpId": 99997},
                            {"instanceId": 107, "grpId": 91829},
                        ],
                    },
                },
            },
        )
        state._update_match_summary(opening_state)

        summary = state._MATCH_SUMMARIES["m_partial_hand"]
        assert summary.games[1].opening_hand == [
            "Forest",
            "[Arena ID 99999]",
            "Forest",
            "[Arena ID 99998]",
            "Forest",
            "[Arena ID 99997]",
            "Forest",
        ]
    finally:
        state._ARENA_CARD_LOOKUP = None
        state._ARENA_CARD_LOOKUP_READY = False


def test_mulliganed_away_cards_include_discarded_hands_and_bottomed_cards() -> None:
    state._MATCH_SUMMARIES.clear()
    state._MULLIGAN_COUNTS.clear()
    state._GAME_INSTANCE_GRP_IDS.clear()
    state._HAND_SNAPSHOT_HISTORY.clear()
    state._LATEST_HAND_SNAPSHOT.clear()
    state._BOTTOMED_CARDS_CAPTURED.clear()
    state._ARENA_CARD_LOOKUP = {
        "1": {"name": "A"},
        "2": {"name": "B"},
        "3": {"name": "C"},
        "4": {"name": "D"},
        "5": {"name": "E"},
        "6": {"name": "F"},
        "7": {"name": "G"},
        "8": {"name": "H"},
        "9": {"name": "I"},
        "10": {"name": "J"},
        "11": {"name": "K"},
        "12": {"name": "L"},
        "13": {"name": "M"},
        "14": {"name": "N"},
    }
    state._ARENA_CARD_LOOKUP_READY = True
    state._CONTEXT["current_match_id"] = ""
    state._CONTEXT["current_game_number"] = ""
    state._CONTEXT["current_player_team"] = ""
    try:
        started = MatchStateEvent(
            EventMetadata(datetime(2026, 4, 20, 21, 45, 0, tzinfo=UTC), b"raw"),
            {
                "type": "match_started",
                "match_id": "m_mulliganed_away",
                "state_type": "MatchGameRoomStateType_Playing",
                "players": [
                    {"player_name": "LocalPlayer", "team_id": 1, "system_seat_id": 1},
                    {"player_name": "Opponent", "team_id": 2, "system_seat_id": 2},
                ],
            },
        )
        state._update_match_summary(started)

        first_offer = GameStateEvent(
            EventMetadata(datetime(2026, 4, 20, 21, 45, 8, tzinfo=UTC), b"raw"),
            {
                "type": "game_state_message",
                "game_info": {"matchID": "m_mulliganed_away", "gameNumber": 1},
                "raw_game_state": {
                    "systemSeatIds": [1],
                    "gameStateMessage": {
                        "gameInfo": {"matchID": "m_mulliganed_away", "gameNumber": 1},
                        "zones": [
                            {
                                "type": "ZoneType_Hand",
                                "visibility": "Visibility_Private",
                                "ownerSeatId": 1,
                                "objectInstanceIds": [101, 102, 103, 104, 105, 106, 107],
                            }
                        ],
                        "gameObjects": [
                            {"instanceId": 101, "grpId": 1},
                            {"instanceId": 102, "grpId": 2},
                            {"instanceId": 103, "grpId": 3},
                            {"instanceId": 104, "grpId": 4},
                            {"instanceId": 105, "grpId": 5},
                            {"instanceId": 106, "grpId": 6},
                            {"instanceId": 107, "grpId": 7},
                        ],
                    },
                },
            },
        )
        state._update_match_summary(first_offer)

        mulligan = ClientActionEvent(
            EventMetadata(datetime(2026, 4, 20, 21, 45, 12, tzinfo=UTC), b"raw"),
            {
                "type": "mulligan_resp",
                "decision": "mulligan",
            },
        )
        state._update_match_summary(mulligan)

        second_offer = GameStateEvent(
            EventMetadata(datetime(2026, 4, 20, 21, 45, 18, tzinfo=UTC), b"raw"),
            {
                "type": "game_state_message",
                "game_info": {"matchID": "m_mulliganed_away", "gameNumber": 1},
                "raw_game_state": {
                    "systemSeatIds": [1],
                    "gameStateMessage": {
                        "gameInfo": {"matchID": "m_mulliganed_away", "gameNumber": 1},
                        "zones": [
                            {
                                "type": "ZoneType_Hand",
                                "visibility": "Visibility_Private",
                                "ownerSeatId": 1,
                                "objectInstanceIds": [201, 202, 203, 204, 205, 206, 207],
                            }
                        ],
                        "gameObjects": [
                            {"instanceId": 201, "grpId": 8},
                            {"instanceId": 202, "grpId": 9},
                            {"instanceId": 203, "grpId": 10},
                            {"instanceId": 204, "grpId": 11},
                            {"instanceId": 205, "grpId": 12},
                            {"instanceId": 206, "grpId": 13},
                            {"instanceId": 207, "grpId": 14},
                        ],
                    },
                },
            },
        )
        state._update_match_summary(second_offer)

        kept_hand = GameStateEvent(
            EventMetadata(datetime(2026, 4, 20, 21, 45, 25, tzinfo=UTC), b"raw"),
            {
                "type": "game_state_message",
                "game_info": {"matchID": "m_mulliganed_away", "gameNumber": 1},
                "raw_game_state": {
                    "systemSeatIds": [1],
                    "gameStateMessage": {
                        "gameInfo": {"matchID": "m_mulliganed_away", "gameNumber": 1},
                        "players": [
                            {"systemSeatNumber": 1, "teamId": 1},
                            {"systemSeatNumber": 2, "teamId": 2},
                        ],
                        "turnInfo": {"turnNumber": 1, "activePlayer": 1},
                        "zones": [
                            {
                                "type": "ZoneType_Hand",
                                "visibility": "Visibility_Private",
                                "ownerSeatId": 1,
                                "objectInstanceIds": [201, 202, 203, 204, 205, 206],
                            }
                        ],
                        "gameObjects": [
                            {"instanceId": 201, "grpId": 8},
                            {"instanceId": 202, "grpId": 9},
                            {"instanceId": 203, "grpId": 10},
                            {"instanceId": 204, "grpId": 11},
                            {"instanceId": 205, "grpId": 12},
                            {"instanceId": 206, "grpId": 13},
                            {"instanceId": 207, "grpId": 14},
                        ],
                    },
                },
            },
        )
        state._update_match_summary(kept_hand)

        summary = state._MATCH_SUMMARIES["m_mulliganed_away"]
        assert summary.games[1].opening_hand == ["H", "I", "J", "K", "L", "M"]
        assert summary.games[1].mulliganed_away == ["A", "B", "C", "D", "E", "F", "G", "N"]

        row = summary.to_game_sheet_rows()[0]
        assert row["Opening Hand"] == "H; I; J; K; L; M"
        assert row["Mulliganed Away"] == "A; B; C; D; E; F; G; N"
    finally:
        state._ARENA_CARD_LOOKUP = None
        state._ARENA_CARD_LOOKUP_READY = False


def test_live_game_log_update_only_advances_when_game_summary_changes() -> None:
    state._MATCH_SUMMARIES.clear()
    state._MULLIGAN_COUNTS.clear()
    state._LAST_POSTED_MATCH_LOG_ROWS.clear()
    state._LAST_POSTED_GAME_LOG_ROWS.clear()
    state._CONTEXT["current_match_id"] = ""
    state._CONTEXT["current_game_number"] = ""
    state._CONTEXT["current_player_team"] = ""

    started = MatchStateEvent(
        EventMetadata(datetime(2026, 4, 20, 1, 0, 0, tzinfo=UTC), b"raw"),
        {
            "type": "match_started",
            "match_id": "m_game_log",
            "state_type": "MatchGameRoomStateType_Playing",
            "event_id": "Constructed_BestOf3",
            "players": [
                {"player_name": "LocalFirst", "team_id": 1, "system_seat_id": 1},
                {"player_name": "OpponentSecond", "team_id": 2, "system_seat_id": 2},
            ],
        },
    )
    state._update_match_summary(started)

    turn_one = GameStateEvent(
        EventMetadata(datetime(2026, 4, 20, 1, 0, 30, tzinfo=UTC), b"raw"),
        {
            "type": "game_state_message",
            "game_info": {
                "matchID": "m_game_log",
                "gameNumber": 1,
                "superFormat": "SuperFormat_Constructed",
                "matchWinCondition": "MatchWinCondition_Best2of3",
            },
            "raw_game_state": {
                "systemSeatIds": [1],
                "gameStateMessage": {
                    "players": [
                        {"systemSeatNumber": 1, "teamId": 1},
                        {"systemSeatNumber": 2, "teamId": 2},
                    ],
                    "turnInfo": {
                        "turnNumber": 1,
                        "activePlayer": 2,
                    },
                },
            },
        },
    )
    state._update_match_summary(turn_one)

    updates = state.build_game_log_updates("m_game_log")
    assert len(updates) == 1
    row, changed_fields, is_final = updates[0]
    assert is_final is False
    assert row["MTGA Match ID"] == "m_game_log"
    assert row["Game Number"] == 1
    assert row["Play / Draw"] == "Draw"
    assert row["Pre / Postboard"] == "Preboard"
    assert row["MTGA Event ID"] == "Constructed_BestOf3"
    assert row["MTGA Format"] == "Constructed"
    assert row["MTGA Queue Type"] == "Best of 3"
    assert "Play / Draw" in changed_fields

    state.mark_game_log_posted("m_game_log", 1, row)
    repeated_updates = state.build_game_log_updates("m_game_log")
    assert repeated_updates == []

    finished = GameResultEvent(
        EventMetadata(datetime(2026, 4, 20, 1, 8, 0, tzinfo=UTC), b"raw"),
        {
            "type": "game_result",
            "winning_team_id": 1,
            "result_type": "ResultType_WinLoss",
            "reason": "ResultReason_Game",
            "game_info": {
                "matchID": "m_game_log",
                "gameNumber": 1,
                "superFormat": "SuperFormat_Constructed",
                "matchWinCondition": "MatchWinCondition_Best2of3",
            },
        },
    )
    state._update_match_summary(finished)

    final_updates = state.build_game_log_updates("m_game_log")
    assert len(final_updates) == 1
    final_row, final_changes, final_is_final = final_updates[0]
    assert final_is_final is True
    assert final_row["Game Result"] == "W"
    assert final_row["Turn Count"] == 1
    assert final_row["Game Duration"] == 450
    assert "Game Result" in final_changes
