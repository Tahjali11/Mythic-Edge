from datetime import UTC, datetime

from mythic_edge_parser.log.entry import EntryHeader, LogEntry
from mythic_edge_parser.parsers import match_state

TS = datetime(2026, 5, 8, 12, 0, 0, tzinfo=UTC)


def test_match_state_parse_playing_state_from_wrapped_payload() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]matchGameRoomStateChangedEvent\n'
        '{"matchGameRoomStateChangedEvent":{"gameRoomInfo":{"stateType":"MatchGameRoomStateType_Playing",'
        '"gameRoomConfig":{"matchId":"m1","eventId":"Traditional_Ladder","reservedPlayers":['
        '{"userId":"u1","playerName":"P1","systemSeatId":1,"teamId":1},'
        '{"userId":"u2","playerName":"P2","systemSeatId":2,"teamId":2}]}}}}',
    )

    event = match_state.try_parse(entry, TS)

    assert event is not None
    assert event.kind == "MatchState"
    assert event.payload["type"] == "match_started"
    assert event.payload["match_id"] == "m1"
    assert event.payload["event_id"] == "Traditional_Ladder"
    assert event.payload["players"] == [
        {"user_id": "u1", "player_name": "P1", "system_seat_id": 1, "team_id": 1},
        {"user_id": "u2", "player_name": "P2", "system_seat_id": 2, "team_id": 2},
    ]


def test_match_state_parse_bare_payload_shape() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]matchGameRoomStateChangedEvent\n'
        '{"gameRoomInfo":{"stateType":"MatchGameRoomStateType_Playing","gameRoomConfig":{"matchId":"m2",'
        '"eventId":"Constructed_BestOf3","reservedPlayers":[{"userId":"u1","playerName":"P1",'
        '"systemSeatId":1,"teamId":1}]}}}',
    )

    event = match_state.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "match_started"
    assert event.payload["match_id"] == "m2"
    assert event.payload["event_id"] == "Constructed_BestOf3"


def test_match_state_parse_completed_state_with_final_results() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]matchGameRoomStateChangedEvent\n'
        '{"matchGameRoomStateChangedEvent":{"gameRoomInfo":{"stateType":"MatchGameRoomStateType_MatchCompleted",'
        '"gameRoomConfig":{"matchId":"m3","eventId":"Traditional_Ladder","reservedPlayers":['
        '{"userId":"u1","playerName":"P1","systemSeatId":1,"teamId":1},'
        '{"userId":"u2","playerName":"P2","systemSeatId":2,"teamId":2}]},'
        '"finalMatchResult":{"matchCompletedReason":"MatchCompletedReasonType_Success","resultList":['
        '{"scope":"MatchScope_Game","result":"ResultType_WinLoss","winningTeamId":1,"reason":"ResultReason_Game"},'
        '{"scope":"MatchScope_Match","result":"ResultType_WinLoss","winningTeamId":1,"reason":"ResultReason_Game"}]}}}}',
    )

    event = match_state.try_parse(entry, TS)

    assert event is not None
    assert event.payload["type"] == "match_completed"
    assert event.payload["match_completed_reason"] == "MatchCompletedReasonType_Success"
    assert event.payload["game_results"] == [
        {
            "scope": "MatchScope_Game",
            "result": "ResultType_WinLoss",
            "winning_team_id": 1,
            "reason": "ResultReason_Game",
        },
        {
            "scope": "MatchScope_Match",
            "result": "ResultType_WinLoss",
            "winning_team_id": 1,
            "reason": "ResultReason_Game",
        },
    ]


def test_match_state_uses_player_event_id_fallback_when_config_event_id_is_missing() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]matchGameRoomStateChangedEvent\n'
        '{"matchGameRoomStateChangedEvent":{"gameRoomInfo":{"stateType":"MatchGameRoomStateType_Playing",'
        '"gameRoomConfig":{"matchId":"m4","reservedPlayers":['
        '{"userId":"u1","playerName":"P1","systemSeatId":1,"teamId":1,"eventId":"Fallback_Event"}]}}}}',
    )

    event = match_state.try_parse(entry, TS)

    assert event is not None
    assert event.payload["event_id"] == "Fallback_Event"


def test_match_state_falls_back_to_game_room_players_when_reserved_players_missing() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]matchGameRoomStateChangedEvent\n'
        '{"matchGameRoomStateChangedEvent":{"gameRoomInfo":{"stateType":"MatchGameRoomStateType_Playing",'
        '"gameRoomConfig":{"matchId":"m5","eventId":"Traditional_Ladder"},'
        '"players":[{"userId":"u1","playerName":"P1","systemSeatId":1,"teamId":1},'
        '{"userId":"u2","playerName":"P2","systemSeatId":2,"teamId":2}]}}}',
    )

    event = match_state.try_parse(entry, TS)

    assert event is not None
    assert event.payload["players"] == [
        {"user_id": "u1", "player_name": "P1", "system_seat_id": 1, "team_id": 1},
        {"user_id": "u2", "player_name": "P2", "system_seat_id": 2, "team_id": 2},
    ]


def test_match_state_build_payload_tolerates_malformed_nested_payload_shapes() -> None:
    payload = match_state.build_payload(
        {
            "gameRoomInfo": {
                "stateType": "MatchGameRoomStateType_Playing",
                "gameRoomConfig": "not-a-dict",
                "finalMatchResult": "not-a-dict",
            }
        }
    )

    assert payload["type"] == "match_started"
    assert payload["match_id"] == ""
    assert payload["event_id"] == ""
    assert payload["players"] == []
    assert "match_completed_reason" not in payload
    assert "game_results" not in payload
