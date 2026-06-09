from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from mythic_edge_parser.app import state
from mythic_edge_parser.app.models import MatchSummary
from mythic_edge_parser.events import (
    ClientActionEvent,
    EventMetadata,
    GameResultEvent,
    GameStateEvent,
    MatchStateEvent,
    RankEvent,
)


class UnknownEvent:
    kind = "UnknownKind"

    def __init__(self) -> None:
        self.metadata = EventMetadata(datetime(2026, 5, 12, 12, 0, 0, tzinfo=UTC), b"raw")
        self.payload = {"match_id": "unknown-match"}


def test_reset_runtime_state_restores_default_shared_state() -> None:
    state._MATCH_SUMMARIES["m1"] = cast(Any, object())
    state._MULLIGAN_COUNTS[("m1", 1)] = 2
    state._LAST_POSTED_MATCH_LOG_ROWS["m1"] = {"Match Win?": "W"}
    state._LAST_POSTED_GAME_LOG_ROWS[("m1", 1)] = {"Game Result": "W"}
    state._GAME_INSTANCE_GRP_IDS[("m1", 1)] = {1: 1001}
    state._HAND_SNAPSHOT_HISTORY[("m1", 1)] = [["Card A"]]
    state._LATEST_HAND_SNAPSHOT[("m1", 1)] = ["Card A"]
    state._BOTTOMED_CARDS_CAPTURED.add(("m1", 1))
    state._CONTEXT["current_match_id"] = "m1"
    state._CONTEXT["current_game_number"] = 2
    state._CONTEXT["current_player_team"] = 1
    state._ARENA_CARD_LOOKUP = {"1001": {"name": "Card A"}}
    state._ARENA_CARD_LOOKUP_READY = True
    state._GAMEPLAY_CARD_LOOKUP_READY = True
    state.set_last_posted_rank("Diamond 4")

    state.reset_runtime_state()

    assert state._MATCH_SUMMARIES == {}
    assert state._MULLIGAN_COUNTS == {}
    assert state._LAST_POSTED_MATCH_LOG_ROWS == {}
    assert state._LAST_POSTED_GAME_LOG_ROWS == {}
    assert state._GAME_INSTANCE_GRP_IDS == {}
    assert state._HAND_SNAPSHOT_HISTORY == {}
    assert state._LATEST_HAND_SNAPSHOT == {}
    assert state._BOTTOMED_CARDS_CAPTURED == set()
    assert state._CONTEXT == {
        "current_match_id": "",
        "current_game_number": "",
        "current_player_team": "",
    }
    assert state._ARENA_CARD_LOOKUP is None
    assert state._ARENA_CARD_LOOKUP_READY is False
    assert state._GAMEPLAY_CARD_LOOKUP_READY is False
    assert state.get_last_posted_rank() == ""


def test_reset_runtime_state_preserves_alias_identity_and_resets_scalars() -> None:
    runtime_state = state.RUNTIME_STATE
    posting_state = runtime_state.posting
    alias_objects = {
        "context": state._CONTEXT,
        "summaries": state._MATCH_SUMMARIES,
        "posted_submit_deck_keys": state._POSTED_SUBMIT_DECK_KEYS,
        "posted_sideboard_keys": state._POSTED_SIDEBOARD_KEYS,
        "game_rows_posted": state._GAME_ROWS_POSTED,
        "match_rows_posted": state._MATCH_ROWS_POSTED,
        "posted_match_summaries": state._POSTED_MATCH_SUMMARIES,
        "posted_match_log_rows": state._POSTED_MATCH_LOG_ROWS,
        "posted_match_rows": state._LAST_POSTED_MATCH_LOG_ROWS,
        "posted_game_rows": state._LAST_POSTED_GAME_LOG_ROWS,
        "mulligan_counts": state._MULLIGAN_COUNTS,
        "game_instance_grp_ids": state._GAME_INSTANCE_GRP_IDS,
        "hand_snapshot_history": state._HAND_SNAPSHOT_HISTORY,
        "latest_hand_snapshot": state._LATEST_HAND_SNAPSHOT,
        "bottomed_cards_captured": state._BOTTOMED_CARDS_CAPTURED,
    }

    state.RUNTIME_STATE.current_log_date = "2026-05-12"
    state.RUNTIME_STATE.current_log_path = Path("/tmp/Player.log")
    state.RUNTIME_STATE.latest_rank_text = "Diamond 1"
    state.RUNTIME_STATE.latest_rank_class = "Diamond"
    state.RUNTIME_STATE.latest_rank_level = 1
    state.RUNTIME_STATE.latest_rank_percentile = 98.6
    state.RUNTIME_STATE.arena_card_lookup = {"1": {"name": "Card A"}}
    state.RUNTIME_STATE.arena_card_lookup_ready = True
    state.RUNTIME_STATE.gameplay_card_lookup_ready = True
    state._CURRENT_LOG_DATE = "2026-05-12"
    state._CURRENT_LOG_PATH = Path("/tmp/Player.log")
    state._LATEST_RANK_TEXT = "Diamond 1"
    state._LATEST_RANK_CLASS = "Diamond"
    state._LATEST_RANK_LEVEL = 1
    state._LATEST_RANK_PERCENTILE = 98.6
    state._ARENA_CARD_LOOKUP = {"1": {"name": "Card A"}}
    state._ARENA_CARD_LOOKUP_READY = True
    state._GAMEPLAY_CARD_LOOKUP_READY = True

    state.reset_runtime_state()

    assert state.RUNTIME_STATE is runtime_state
    assert state.RUNTIME_STATE.posting is posting_state
    assert state._CONTEXT is alias_objects["context"]
    assert state._MATCH_SUMMARIES is alias_objects["summaries"]
    assert state._POSTED_SUBMIT_DECK_KEYS is alias_objects["posted_submit_deck_keys"]
    assert state._POSTED_SIDEBOARD_KEYS is alias_objects["posted_sideboard_keys"]
    assert state._GAME_ROWS_POSTED is alias_objects["game_rows_posted"]
    assert state._MATCH_ROWS_POSTED is alias_objects["match_rows_posted"]
    assert state._POSTED_MATCH_SUMMARIES is alias_objects["posted_match_summaries"]
    assert state._POSTED_MATCH_LOG_ROWS is alias_objects["posted_match_log_rows"]
    assert state._LAST_POSTED_MATCH_LOG_ROWS is alias_objects["posted_match_rows"]
    assert state._LAST_POSTED_GAME_LOG_ROWS is alias_objects["posted_game_rows"]
    assert state._MULLIGAN_COUNTS is alias_objects["mulligan_counts"]
    assert state._GAME_INSTANCE_GRP_IDS is alias_objects["game_instance_grp_ids"]
    assert state._HAND_SNAPSHOT_HISTORY is alias_objects["hand_snapshot_history"]
    assert state._LATEST_HAND_SNAPSHOT is alias_objects["latest_hand_snapshot"]
    assert state._BOTTOMED_CARDS_CAPTURED is alias_objects["bottomed_cards_captured"]
    assert state.RUNTIME_STATE.current_log_date == ""
    assert state.RUNTIME_STATE.current_log_path is None
    assert state.RUNTIME_STATE.latest_rank_text == ""
    assert state.RUNTIME_STATE.latest_rank_class == ""
    assert state.RUNTIME_STATE.latest_rank_level == ""
    assert state.RUNTIME_STATE.latest_rank_percentile is None
    assert state.RUNTIME_STATE.arena_card_lookup is None
    assert state.RUNTIME_STATE.arena_card_lookup_ready is False
    assert state.RUNTIME_STATE.gameplay_card_lookup_ready is False
    assert state._CURRENT_LOG_DATE == ""
    assert state._CURRENT_LOG_PATH is None
    assert state._LATEST_RANK_TEXT == ""
    assert state._LATEST_RANK_CLASS == ""
    assert state._LATEST_RANK_LEVEL == ""
    assert state._LATEST_RANK_PERCENTILE is None
    assert state._ARENA_CARD_LOOKUP is None
    assert state._ARENA_CARD_LOOKUP_READY is False
    assert state._GAMEPLAY_CARD_LOOKUP_READY is False


def test_posting_state_bridge_aliases_point_to_nested_state() -> None:
    state.reset_runtime_state()

    posting = state.RUNTIME_STATE.posting

    assert state.RUNTIME_STATE.posted_submit_deck_keys is posting.posted_submit_deck_keys
    assert state.RUNTIME_STATE.posted_sideboard_keys is posting.posted_sideboard_keys
    assert state.RUNTIME_STATE.game_rows_posted is posting.game_rows_posted
    assert state.RUNTIME_STATE.match_rows_posted is posting.match_rows_posted
    assert state.RUNTIME_STATE.posted_match_summaries is posting.posted_match_summaries
    assert state.RUNTIME_STATE.posted_match_log_rows is posting.posted_match_log_rows
    assert state.RUNTIME_STATE.last_posted_match_log_rows is posting.last_posted_match_log_rows
    assert state.RUNTIME_STATE.last_posted_game_log_rows is posting.last_posted_game_log_rows
    assert state._POSTED_SUBMIT_DECK_KEYS is posting.posted_submit_deck_keys
    assert state._POSTED_SIDEBOARD_KEYS is posting.posted_sideboard_keys
    assert state._GAME_ROWS_POSTED is posting.game_rows_posted
    assert state._MATCH_ROWS_POSTED is posting.match_rows_posted
    assert state._POSTED_MATCH_SUMMARIES is posting.posted_match_summaries
    assert state._POSTED_MATCH_LOG_ROWS is posting.posted_match_log_rows
    assert state._LAST_POSTED_MATCH_LOG_ROWS is posting.last_posted_match_log_rows
    assert state._LAST_POSTED_GAME_LOG_ROWS is posting.last_posted_game_log_rows


def test_unknown_event_kind_is_complete_noop() -> None:
    state.reset_runtime_state()

    state._update_match_summary(UnknownEvent())

    assert state._MATCH_SUMMARIES == {}
    assert state._CONTEXT == {
        "current_match_id": "",
        "current_game_number": "",
        "current_player_team": "",
    }


def test_missing_identity_events_do_not_create_anonymous_summaries() -> None:
    state.reset_runtime_state()
    metadata = EventMetadata(datetime(2026, 5, 12, 12, 0, 0, tzinfo=UTC), b"raw")
    events = [
        MatchStateEvent(metadata, {"type": "match_started"}),
        GameStateEvent(metadata, {"type": "game_state_message"}),
        ClientActionEvent(metadata, {"type": "mulligan_resp", "decision": "mulligan"}),
        GameResultEvent(metadata, {"type": "game_result", "winning_team_id": 1}),
    ]

    for event in events:
        state._update_match_summary(event)

    assert state._MATCH_SUMMARIES == {}
    assert state._CONTEXT == {
        "current_match_id": "",
        "current_game_number": "",
        "current_player_team": "",
    }


def test_mark_posted_rows_store_copies() -> None:
    state.reset_runtime_state()
    match_row = {"MTGA Match ID": "match-copy", "Match Win?": "W"}
    game_row = {"MTGA Match ID": "match-copy", "Game Number": 1, "Game Result": "W"}

    state.mark_match_log_posted("match-copy", match_row)
    state.mark_game_log_posted("match-copy", 1, game_row)
    match_row["MTGA Match ID"] = "mutated"
    game_row["Game Result"] = "mutated"

    assert state._LAST_POSTED_MATCH_LOG_ROWS["match-copy"]["MTGA Match ID"] == "match-copy"
    assert state._LAST_POSTED_GAME_LOG_ROWS[("match-copy", 1)]["Game Result"] == "W"


def test_changed_fields_ignore_non_sync_changes_and_float_rounding_noise() -> None:
    previous_row = {
        "MTGA Match ID": "match-sync",
        "Game Win %": 0.333333333333,
        "not_a_sync_field": "old",
    }
    current_row = {
        "MTGA Match ID": "match-sync",
        "Game Win %": 0.333333333334,
        "not_a_sync_field": "new",
    }

    changed_fields = state._changed_fields(
        previous_row,
        current_row,
        ("MTGA Match ID", "Game Win %"),
    )

    assert changed_fields == []


def test_invalid_game_log_keys_are_skipped() -> None:
    class InvalidGameRows:
        def to_game_sheet_rows(self) -> list[dict[str, object]]:
            return [
                {"MTGA Match ID": "", "Game Number": 1, "Game Result": "W"},
                {"MTGA Match ID": "match-invalid-game", "Game Number": "not-a-game", "Game Result": "W"},
            ]

    state.reset_runtime_state()

    state.mark_game_log_posted("", 1, {"MTGA Match ID": "", "Game Number": 1})
    state.mark_game_log_posted("match-invalid-game", "", {"MTGA Match ID": "match-invalid-game", "Game Number": ""})
    state._MATCH_SUMMARIES["match-invalid-game"] = cast(Any, InvalidGameRows())

    assert state._LAST_POSTED_GAME_LOG_ROWS == {}
    assert state.build_game_log_updates("match-invalid-game") == []


def test_match_row_builders_respect_live_and_final_readiness() -> None:
    state.reset_runtime_state()
    summary = MatchSummary(match_id="match-builders")
    state._MATCH_SUMMARIES["match-builders"] = summary

    live_row = state.build_live_match_log_row("match-builders")

    assert live_row is not None
    assert live_row["MTGA Sync Status"] == "Live"
    assert state.build_match_summary_row("match-builders") is None
    assert state.build_match_log_row("match-builders") is None

    summary.player_team = 1
    summary.match_winner_team = 1

    final_summary_row = state.build_match_summary_row("match-builders")
    final_match_log_row = state.build_match_log_row("match-builders")
    assert final_summary_row is not None
    assert final_summary_row["event_family"] == "MatchSummary"
    assert final_match_log_row is not None
    assert final_match_log_row["MTGA Sync Status"] == "Final"


def test_observation_apis_return_snapshots_and_runtime_singleton() -> None:
    state.reset_runtime_state()
    summary_one = MatchSummary(match_id="match-one")
    summary_two = MatchSummary(match_id="match-two")
    state._MATCH_SUMMARIES["match-one"] = summary_one
    state._CONTEXT["current_match_id"] = "match-one"

    summaries_snapshot = state.iter_match_summaries()
    context_snapshot = state.get_context_snapshot()
    state._MATCH_SUMMARIES["match-two"] = summary_two
    context_snapshot["current_match_id"] = "mutated"

    assert summaries_snapshot == [summary_one]
    assert state.iter_match_summaries() == [summary_one, summary_two]
    assert state.get_context_snapshot()["current_match_id"] == "match-one"
    assert state.get_runtime_state() is state.RUNTIME_STATE


def test_game_state_and_game_result_use_context_fallback_identity() -> None:
    state.reset_runtime_state()
    state._CONTEXT["current_match_id"] = "match-context"
    state._CONTEXT["current_game_number"] = 2
    state._CONTEXT["current_player_team"] = 1

    game_state = GameStateEvent(
        EventMetadata(datetime(2026, 5, 12, 12, 1, 0, tzinfo=UTC), b"raw"),
        {
            "type": "game_state_message",
            "turn_info": {"turnNumber": 3, "activePlayer": 1},
            "players": [
                {"systemSeatNumber": 1, "teamId": 1},
                {"systemSeatNumber": 2, "teamId": 2},
            ],
        },
    )
    state._update_match_summary(game_state)

    game_result = GameResultEvent(
        EventMetadata(datetime(2026, 5, 12, 12, 5, 0, tzinfo=UTC), b"raw"),
        {
            "type": "game_result",
            "winning_team_id": 2,
            "result_type": "ResultType_WinLoss",
            "reason": "ResultReason_Game",
        },
    )
    state._update_match_summary(game_result)

    summary = state.get_match_summary("match-context")
    assert summary is not None
    assert summary.player_team == 1
    assert summary.games[2].turn_count == 3
    assert summary.games[2].winner_team == 2


def test_game_result_uses_nested_game_and_match_scope_winners() -> None:
    state.reset_runtime_state()
    state._CONTEXT["current_player_team"] = 1

    event = GameResultEvent(
        EventMetadata(datetime(2026, 5, 12, 12, 10, 0, tzinfo=UTC), b"raw"),
        {
            "type": "game_result",
            "winning_team_id": 9,
            "result_type": "ResultType_TopLevel",
            "reason": "ResultReason_TopLevel",
            "match_state": "MatchState_GameComplete",
            "identity": {"match_id": "match-nested", "game_number": 2},
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
                    "result": "ResultType_MatchWinLoss",
                    "reason": "ResultReason_MatchNested",
                },
                {
                    "scope": "MatchScope_Game",
                    "winningTeamId": 2,
                    "result": "ResultType_WinLoss",
                    "reason": "ResultReason_LatestGame",
                },
            ],
        },
    )

    state._update_match_summary(event)

    summary = state.get_match_summary("match-nested")
    assert summary is not None
    assert summary.games[2].winner_team == 2
    assert summary.match_winner_team == 3
    assert summary.match_result_type == "ResultType_MatchWinLoss"
    assert summary.match_result_reason == "ResultReason_MatchNested"


def test_game_result_nested_match_winner_beats_conflicting_top_level_winner() -> None:
    state.reset_runtime_state()
    state._CONTEXT["current_player_team"] = 1

    event = GameResultEvent(
        EventMetadata(datetime(2026, 5, 12, 12, 12, 0, tzinfo=UTC), b"raw"),
        {
            "type": "game_result",
            "winning_team_id": 1,
            "result_type": "ResultType_TopLevel",
            "reason": "ResultReason_TopLevel",
            "match_state": "MatchState_MatchComplete",
            "identity": {"match_id": "match-conflict", "game_number": 1},
            "results": [
                {
                    "scope": "MatchScope_Game",
                    "winningTeamId": 1,
                    "result": "ResultType_WinLoss",
                    "reason": "ResultReason_Game",
                },
                {
                    "scope": "MatchScope_Match",
                    "winningTeamId": 2,
                    "result": "ResultType_NestedMatch",
                    "reason": "ResultReason_NestedMatch",
                },
            ],
        },
    )

    state._update_match_summary(event)

    summary = state.get_match_summary("match-conflict")
    assert summary is not None
    assert summary.games[1].winner_team == 1
    assert summary.match_winner_team == 2
    assert summary.match_result_type == "ResultType_NestedMatch"
    assert summary.match_result_reason == "ResultReason_NestedMatch"


def test_game_result_top_level_match_winner_fallback_requires_match_complete() -> None:
    state.reset_runtime_state()
    state._CONTEXT["current_player_team"] = 1

    not_complete = GameResultEvent(
        EventMetadata(datetime(2026, 5, 12, 12, 14, 0, tzinfo=UTC), b"raw"),
        {
            "type": "game_result",
            "winning_team_id": 2,
            "result_type": "ResultType_TopLevel",
            "reason": "ResultReason_TopLevel",
            "match_state": "MatchState_GameComplete",
            "identity": {"match_id": "match-fallback", "game_number": 1},
        },
    )
    state._update_match_summary(not_complete)
    summary = state.get_match_summary("match-fallback")
    assert summary is not None
    assert summary.games[1].winner_team == 2
    assert summary.match_winner_team == ""

    complete = GameResultEvent(
        EventMetadata(datetime(2026, 5, 12, 12, 16, 0, tzinfo=UTC), b"raw"),
        {
            "type": "game_result",
            "winning_team_id": 2,
            "result_type": "ResultType_TopLevelComplete",
            "reason": "ResultReason_TopLevelComplete",
            "match_state": "MatchState_MatchComplete",
            "identity": {"match_id": "match-fallback", "game_number": 1},
        },
    )
    state._update_match_summary(complete)

    assert summary.match_winner_team == 2
    assert summary.match_result_type == "ResultType_TopLevelComplete"
    assert summary.match_result_reason == "ResultReason_TopLevelComplete"


def test_game_result_unknown_winners_do_not_overwrite_existing_winners() -> None:
    for unknown_winner in (0, "0", None, ""):
        state.reset_runtime_state()
        summary = MatchSummary(match_id=f"match-unknown-{unknown_winner!r}")
        summary.set_game_winner(1, 7)
        summary.match_winner_team = 8
        summary.match_result_type = "ResultType_Existing"
        summary.match_result_reason = "ResultReason_Existing"
        state._MATCH_SUMMARIES[summary.match_id] = summary

        event = GameResultEvent(
            EventMetadata(datetime(2026, 5, 12, 12, 18, 0, tzinfo=UTC), b"raw"),
            {
                "type": "game_result",
                "winning_team_id": unknown_winner,
                "result_type": "ResultType_TopLevel",
                "reason": "ResultReason_TopLevel",
                "match_state": "MatchState_MatchComplete",
                "identity": {"match_id": summary.match_id, "game_number": 1},
                "results": [
                    {
                        "scope": "MatchScope_Game",
                        "winningTeamId": unknown_winner,
                        "result": "ResultType_Game",
                        "reason": "ResultReason_Game",
                    },
                    {
                        "scope": "MatchScope_Match",
                        "winningTeamId": unknown_winner,
                        "result": "ResultType_Match",
                        "reason": "ResultReason_Match",
                    },
                ],
            },
        )

        state._update_match_summary(event)

        assert summary.games[1].winner_team == 7
        assert summary.match_winner_team == 8
        assert summary.match_result_type == "ResultType_Existing"
        assert summary.match_result_reason == "ResultReason_Existing"


def test_hand_snapshot_duplicate_suppression_and_once_only_bottomed_capture() -> None:
    state.reset_runtime_state()
    summary = MatchSummary(match_id="match-hand")
    summary.set_game_mulligans(1, 1)
    key = ("match-hand", 1)

    state._record_hand_snapshot(key, ["A", "B", "C"])
    state._record_hand_snapshot(key, ["A", "B", "C"])
    state._record_hand_snapshot(key, ["A", "B"])
    state._capture_bottomed_cards(summary, 1, ["A", "B"])
    state._capture_bottomed_cards(summary, 1, ["A", "B"])

    assert state._HAND_SNAPSHOT_HISTORY[key] == [["A", "B", "C"], ["A", "B"]]
    assert summary.games[1].mulliganed_away == ["C"]
    assert state._BOTTOMED_CARDS_CAPTURED == {key}


def test_update_match_summary_rank_event_updates_shared_rank_alias() -> None:
    state.reset_runtime_state()

    event = RankEvent(
        EventMetadata(datetime(2026, 5, 8, 12, 0, 0, tzinfo=UTC), b"raw"),
        {
            "constructed_class": "Diamond",
            "constructed_level": 4,
            "constructed_percentile": "",
        },
    )

    state._update_match_summary(event)

    assert state.get_last_posted_rank() == "Diamond 4"
    assert state.get_runtime_state().last_posted_rank == "Diamond 4"


def test_pre_match_rank_is_carried_into_next_match_summary() -> None:
    state.reset_runtime_state()

    rank_event = RankEvent(
        EventMetadata(datetime(2026, 5, 8, 11, 59, 0, tzinfo=UTC), b"raw"),
        {
            "constructed_class": "Diamond",
            "constructed_level": 2,
            "constructed_percentile": "",
        },
    )
    state._update_match_summary(rank_event)

    match_started = MatchStateEvent(
        EventMetadata(datetime(2026, 5, 8, 12, 0, 0, tzinfo=UTC), b"raw"),
        {
            "type": "match_started",
            "match_id": "match-rank-carry",
            "state_type": "MatchGameRoomStateType_Playing",
            "players": [
                {"player_name": "Local", "team_id": 1, "system_seat_id": 1},
                {"player_name": "Opponent", "team_id": 2, "system_seat_id": 2},
            ],
        },
    )
    state._update_match_summary(match_started)

    summary = state.get_match_summary("match-rank-carry")
    assert summary is not None
    assert summary.constructed_rank == "Diamond 2"
    assert summary.constructed_class == "Diamond"
    assert summary.constructed_level == 2
    assert summary.constructed_rank_source == "carried_forward_pre_match"


def test_post_match_rank_updates_next_match_not_completed_match() -> None:
    state.reset_runtime_state()

    started = MatchStateEvent(
        EventMetadata(datetime(2026, 5, 8, 12, 0, 0, tzinfo=UTC), b"raw"),
        {
            "type": "match_started",
            "match_id": "match-old",
            "state_type": "MatchGameRoomStateType_Playing",
            "players": [
                {"player_name": "Local", "team_id": 1, "system_seat_id": 1},
                {"player_name": "Opponent", "team_id": 2, "system_seat_id": 2},
            ],
        },
    )
    completed = MatchStateEvent(
        EventMetadata(datetime(2026, 5, 8, 12, 10, 0, tzinfo=UTC), b"raw"),
        {
            "type": "match_completed",
            "match_id": "match-old",
            "state_type": "MatchGameRoomStateType_MatchCompleted",
            "players": [
                {"player_name": "Local", "team_id": 1, "system_seat_id": 1},
                {"player_name": "Opponent", "team_id": 2, "system_seat_id": 2},
            ],
            "game_results": [
                {
                    "scope": "MatchScope_Game",
                    "result": "ResultType_WinLoss",
                    "winning_team_id": 2,
                    "reason": "ResultReason_Normal",
                },
                {
                    "scope": "MatchScope_Match",
                    "result": "ResultType_WinLoss",
                    "winning_team_id": 2,
                    "reason": "ResultReason_Normal",
                },
            ],
        },
    )
    rank_event = RankEvent(
        EventMetadata(datetime(2026, 5, 8, 12, 11, 0, tzinfo=UTC), b"raw"),
        {
            "constructed_class": "Platinum",
            "constructed_level": 4,
            "constructed_percentile": "",
        },
    )
    next_match_started = MatchStateEvent(
        EventMetadata(datetime(2026, 5, 8, 12, 20, 0, tzinfo=UTC), b"raw"),
        {
            "type": "match_started",
            "match_id": "match-new",
            "state_type": "MatchGameRoomStateType_Playing",
            "players": [
                {"player_name": "Local", "team_id": 1, "system_seat_id": 1},
                {"player_name": "Opponent", "team_id": 2, "system_seat_id": 2},
            ],
        },
    )

    state._update_match_summary(started)
    state._update_match_summary(completed)
    state._update_match_summary(rank_event)
    state._update_match_summary(next_match_started)

    old_summary = state.get_match_summary("match-old")
    new_summary = state.get_match_summary("match-new")
    assert old_summary is not None
    assert new_summary is not None
    assert old_summary.constructed_rank == ""
    assert new_summary.constructed_rank == "Platinum 4"
    assert new_summary.constructed_rank_source == "carried_forward_pre_match"
