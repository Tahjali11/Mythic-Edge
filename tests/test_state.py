from datetime import UTC, datetime

from mythic_edge_parser.app import state
from mythic_edge_parser.events import EventMetadata, MatchStateEvent, RankEvent


def test_reset_runtime_state_restores_default_shared_state() -> None:
    state._MATCH_SUMMARIES["m1"] = object()
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
