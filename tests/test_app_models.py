from mythic_edge_parser.app.models import MatchSummary
from mythic_edge_parser.app.sheet_schema import GAME_LOG_SYNC_FIELDS, MATCH_LOG_SYNC_FIELDS


def test_match_log_row_contains_every_python_sync_field() -> None:
    summary = MatchSummary(match_id="m_contract")

    row = summary.to_match_log_row()

    missing_fields = set(MATCH_LOG_SYNC_FIELDS) - set(row)
    assert missing_fields == set()


def test_game_log_row_contains_every_python_sync_field() -> None:
    summary = MatchSummary(match_id="m_game_contract")
    summary.touch_game(1, "2026-04-17T19:12:00-04:00")

    rows = summary.to_game_sheet_rows()

    assert len(rows) == 1
    missing_fields = set(GAME_LOG_SYNC_FIELDS) - set(rows[0])
    assert missing_fields == set()


def test_match_summary_touch_ignores_blank_timestamp_after_existing_timestamp() -> None:
    summary = MatchSummary(match_id="m_touch")
    summary.touch("2026-04-17T19:11:42-04:00")

    summary.touch("")

    assert summary.first_event_time == "2026-04-17T19:11:42-04:00"
    assert summary.last_event_time == "2026-04-17T19:11:42-04:00"


def test_set_game_mulligans_ignores_non_integer_values() -> None:
    summary = MatchSummary(match_id="m_mulligans")
    summary.set_game_mulligans(1, 2)

    for invalid_value in ("not-a-number", -1, True, 1.5, object()):
        summary.set_game_mulligans(1, invalid_value)

        assert summary.games[1].mulligans == 2
        assert summary.total_mulligans == 2


def test_set_game_mulligans_ignores_non_finite_numeric_values() -> None:
    summary = MatchSummary(match_id="m_non_finite_mulligans")
    summary.set_game_mulligans(1, 2)

    for invalid_value in (float("inf"), float("-inf"), float("nan")):
        summary.set_game_mulligans(1, invalid_value)

        assert summary.games[1].mulligans == 2
        assert summary.total_mulligans == 2


def test_set_game_mulligans_accepts_integer_like_string_value() -> None:
    summary = MatchSummary(match_id="m_string_mulligans")

    summary.set_game_mulligans(1, "2")

    assert summary.games[1].mulligans == 2
    assert summary.total_mulligans == 2


def test_match_summary_sheet_row_matches_workbook_shape() -> None:
    summary = MatchSummary(match_id="m1")
    summary.first_event_time = "2026-04-17T19:11:42-04:00"
    summary.last_event_time = "2026-04-17T19:33:48-04:00"
    summary.player_team = 1
    summary.match_winner_team = 2
    summary.match_result_type = "ResultType_WinLoss"
    summary.match_result_reason = "ResultReason_Concede"
    summary.constructed_rank = "Mythic 98.6"
    summary.constructed_class = "Mythic"
    summary.constructed_percentile = 98.6
    summary.sideboarding_entered = True
    summary.submit_deck_seen = True
    summary.set_game_winner(1, 1)
    summary.set_game_winner(2, 2)
    summary.set_game_winner(3, 2)
    summary.set_game_starting_player(1, 2)
    summary.set_game_starting_player(2, 1)
    summary.set_game_mulligans(1, 1)
    summary.set_game_mulligans(2, 2)

    row = summary.to_sheet_row()

    assert row["match_id"] == "m1"
    assert row["first_event_time"] == "2026-04-17T19:11:42-04:00"
    assert row["last_event_time"] == "2026-04-17T19:33:48-04:00"
    assert row["match_wl"] == "L"
    assert row["game_wins"] == 1
    assert row["game_losses"] == 2
    assert row["g1_play_draw"] == "Draw"
    assert row["g2_play_draw"] == "Play"
    assert row["g3_play_draw"] == "Play"
    assert row["g1_result"] == "W"
    assert row["g2_result"] == "L"
    assert row["g3_result"] == "L"
    assert row["total_mulligans"] == 3
    assert row["constructed_rank"] == "Mythic 98.6"
    assert row["my_rank"] == "Mythic %"


def test_game_summary_rows_exist_for_future_exports() -> None:
    summary = MatchSummary(match_id="m2")
    summary.player_team = 1
    summary.constructed_rank = "Diamond 1"
    summary.constructed_class = "Diamond"
    summary.event_id = "Constructed_BestOf3"
    summary.super_format = "SuperFormat_Constructed"
    summary.match_win_condition = "MatchWinCondition_Best2of3"
    summary.first_event_time = "2026-04-17T19:11:42-04:00"
    summary.last_event_time = "2026-04-17T19:33:48-04:00"
    summary.touch_game(1, "2026-04-17T19:12:00-04:00")
    summary.touch_game(1, "2026-04-17T19:18:00-04:00")
    summary.set_game_winner(1, 1)
    summary.set_game_starting_player(1, 1)
    summary.set_game_mulligans(1, 2)
    summary.set_game_opening_hand(1, ["Forest", "Llanowar Elves", "Cut Down", "Swamp", "Go for the Throat"])
    summary.add_game_mulliganed_away(1, ["Duress", "Blooming Marsh"])
    summary.set_game_turn_count(1, 9)

    rows = summary.to_game_sheet_rows()

    assert len(rows) == 1
    assert rows[0]["event_family"] == "GameLogRow"
    assert rows[0]["MTGA Match ID"] == "m2"
    assert rows[0]["Game Number"] == 1
    assert rows[0]["Play / Draw"] == "Play"
    assert rows[0]["Mulligans"] == 2
    assert rows[0]["Opening Hand Size"] == 5
    assert rows[0]["Opening Hand"] == "Forest; Llanowar Elves; Cut Down; Swamp; Go for the Throat"
    assert rows[0]["Mulliganed Away"] == "Duress; Blooming Marsh"
    assert rows[0]["Game Result"] == "W"
    assert rows[0]["Turn Count"] == 9
    assert rows[0]["Game Duration"] == 360
    assert rows[0]["MTGA Format"] == "Constructed"
    assert rows[0]["MTGA Event ID"] == "Constructed_BestOf3"
    assert rows[0]["MTGA Queue Type"] == "Best of 3"


def test_match_log_row_matches_first_phase_workbook_shape() -> None:
    summary = MatchSummary(match_id="m3")
    summary.first_event_time = "2026-04-17T19:11:42-04:00"
    summary.last_event_time = "2026-04-17T19:33:48-04:00"
    summary.player_team = 1
    summary.match_winner_team = 1
    summary.constructed_rank = "Mythic 98.6295678174752"
    summary.constructed_class = "Mythic"
    summary.constructed_percentile = 98.6295678174752
    summary.event_id = "Traditional_Ladder"
    summary.super_format = "SuperFormat_Constructed"
    summary.match_win_condition = "MatchWinCondition_Best2of3"
    summary.sideboarding_entered = True
    summary.submit_deck_seen = True
    summary.set_game_starting_player(1, 2)
    summary.set_game_starting_player(2, 1)
    summary.set_game_starting_player(3, 2)
    summary.set_game_winner(1, 2)
    summary.set_game_winner(2, 1)
    summary.set_game_winner(3, 1)
    summary.touch_game(1, "2026-04-17T19:12:00-04:00")
    summary.touch_game(2, "2026-04-17T19:20:00-04:00")
    summary.touch_game(3, "2026-04-17T19:28:00-04:00")
    summary.set_game_mulligans(1, 1)
    summary.set_game_mulligans(2, 0)
    summary.set_game_mulligans(3, 0)
    summary.set_game_turn_count(1, 7)
    summary.set_game_turn_count(2, 9)
    summary.set_game_turn_count(3, 11)

    row = summary.to_match_log_row()

    assert row["event_family"] == "MatchLogRow"
    assert row["event_type"] == "match_log_row"
    assert row["scope"] == "Match"
    assert row["match_id"] == "m3"
    assert row["Date"] == "2026-04-17"
    assert row["My Rank"] == "Mythic %"
    assert row["G1 Play / Draw"] == "Draw"
    assert row["Game 1 Result"] == "L"
    assert row["G2 Play / Draw"] == "Play"
    assert row["Game 2 Result"] == "W"
    assert row["G3 Play / Draw"] == "Draw"
    assert row["Game 3 Result"] == "W"
    assert row["Games Won"] == 2
    assert row["Games Lost"] == 1
    assert row["Match Win?"] == "W"
    assert row["Total Games"] == 3
    assert row["Match Win Flag"] == 1
    assert row["MTGA Match ID"] == "m3"
    assert row["MTGA Format"] == "Constructed"
    assert row["MTGA Event ID"] == "Traditional_Ladder"
    assert row["MTGA Queue Type"] == "Best of 3"
    assert row["G1 Mulligans"] == 1
    assert row["G2 Mulligans"] == 0
    assert row["G3 Mulligans"] == 0
    assert row["G1 Turn Count"] == 7
    assert row["G2 Turn Count"] == 9
    assert row["G3 Turn Count"] == 11
    assert row["MTGA Rank Raw"] == "Mythic 98.6295678174752"
    assert row["MTGA Mulligans"] == 1
    assert row["MTGA Sideboard Entered"] == "Yes"
    assert row["MTGA Submit Deck Seen"] == "Yes"


def test_match_summary_history_item_includes_normalized_event_identity() -> None:
    summary = MatchSummary(match_id="m_history")
    summary.first_event_time = "2026-04-17T19:11:42-04:00"
    summary.last_event_time = "2026-04-17T19:33:48-04:00"
    summary.player_team = 1
    summary.match_winner_team = 1
    summary.event_id = "Traditional_Ladder"
    summary.super_format = "SuperFormat_Constructed"
    summary.match_win_condition = "MatchWinCondition_Best2of3"
    summary.set_game_winner(1, 1)

    payload = summary.to_history_item()

    assert payload["rank_match_type"] == "ranked"
    assert payload["play_mode_family"] == "constructed"
    assert payload["event_family"] == "ladder"
    assert payload["queue_subtype"] == "traditional_ranked_ladder"
    assert payload["rank_eligible"] is True
    assert payload["is_ranked_match"] is True
    assert payload["is_unranked_match"] is False
    assert payload["is_constructed_match"] is True
    assert payload["is_limited_match"] is False
    assert payload["is_draft_match"] is False
    assert payload["is_sealed_match"] is False
    assert payload["is_ladder_match"] is True
    assert payload["is_special_event_match"] is False
    assert payload["is_event_match"] is False


def test_game_summary_opening_hand_size_falls_back_to_seven_minus_mulligans() -> None:
    summary = MatchSummary(match_id="m_open")
    summary.player_team = 1
    summary.first_event_time = "2026-04-21T19:11:42-04:00"
    summary.last_event_time = "2026-04-21T19:18:42-04:00"
    summary.touch_game(1, "2026-04-21T19:12:00-04:00")
    summary.set_game_mulligans(1, 1)

    row = summary.to_game_sheet_rows()[0]

    assert row["Opening Hand Size"] == 6
    assert row["Opening Hand"] == ""
    assert row["Mulliganed Away"] == ""


def test_game_log_row_hides_partial_card_lists_with_unresolved_arena_ids() -> None:
    summary = MatchSummary(match_id="m_partial")
    summary.player_team = 1
    summary.first_event_time = "2026-04-21T19:11:42-04:00"
    summary.last_event_time = "2026-04-21T19:18:42-04:00"
    summary.touch_game(1, "2026-04-21T19:12:00-04:00")
    summary.set_game_mulligans(1, 1)
    summary.set_game_opening_hand(
        1,
        [
            "Blooming Marsh",
            "[Arena ID 96185]",
            "Wastewood Verge",
            "Duress",
            "Sentinel of the Nameless City",
            "[Arena ID 100574]",
        ],
    )
    summary.add_game_mulliganed_away(
        1,
        [
            "[Arena ID 102778]",
            "Duress",
            "[Arena ID 102703]",
            "Archdruid's Charm",
        ],
    )

    row = summary.to_game_sheet_rows()[0]

    assert row["Opening Hand Size"] == 6
    assert row["Opening Hand"] == ""
    assert row["Mulliganed Away"] == ""


def test_live_match_log_row_is_provisional() -> None:
    summary = MatchSummary(match_id="m_live")
    summary.first_event_time = "2026-04-18T19:11:42-04:00"
    summary.last_event_time = "2026-04-18T19:12:10-04:00"
    summary.player_team = 1
    summary.set_game_winner(1, 1)

    row = summary.to_match_log_row(final=False)

    assert row["MTGA Sync Status"] == "Live"
    assert row["MTGA End Time"] == ""
    assert row["Games Won"] == 1
    assert row["Games Lost"] == 0
    assert row["Match Win?"] == ""
    assert row["MTGA Sideboard Entered"] == ""
    assert row["MTGA Submit Deck Seen"] == ""
    assert row["MTGA Mulligans"] == ""


def test_missing_later_game_starting_player_is_inferred_from_previous_game_result() -> None:
    summary = MatchSummary(match_id="m4")
    summary.player_team = 1
    summary.match_winner_team = 2
    summary.set_game_starting_player(1, 1)
    summary.set_game_winner(1, 1)
    summary.set_game_winner(2, 2)
    summary.set_game_winner(3, 2)

    row = summary.to_match_log_row()

    assert row["G1 Play / Draw"] == "Play"
    assert row["G2 Play / Draw"] == "Draw"
    assert row["G3 Play / Draw"] == "Play"


def test_explicit_starting_player_beats_inferred_starting_player() -> None:
    summary = MatchSummary(match_id="m5")
    summary.player_team = 1
    summary.match_winner_team = 1
    summary.set_game_winner(1, 1)
    summary.set_game_winner(2, 1)
    summary.set_game_starting_player(2, 1)

    row = summary.to_match_log_row()

    assert row["G2 Play / Draw"] == "Play"


def test_unused_game_slot_stays_blank_in_two_zero_match() -> None:
    summary = MatchSummary(match_id="m6")
    summary.player_team = 2
    summary.match_winner_team = 2
    summary.set_game_starting_player(1, 2)
    summary.set_game_winner(1, 2)
    summary.set_game_winner(2, 2)

    row = summary.to_match_log_row()

    assert row["G1 Play / Draw"] == "Play"
    assert row["G2 Play / Draw"] == "Draw"
    assert row["G3 Play / Draw"] == ""
    assert row["Game 3 Result"] == ""
