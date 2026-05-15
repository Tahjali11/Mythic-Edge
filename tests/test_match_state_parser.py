from datetime import UTC, datetime

from mythic_edge_parser.events import PerformanceClass
from mythic_edge_parser.log.entry import EntryHeader, LogEntry
from mythic_edge_parser.parsers import match_state

TS = datetime(2026, 5, 8, 12, 0, 0, tzinfo=UTC)


def _entry(body: str) -> LogEntry:
    return LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, body)


def test_match_state_parse_playing_state_from_wrapped_payload() -> None:
    entry = _entry(
        '[UnityCrossThreadLogger]matchGameRoomStateChangedEvent\n'
        '{"matchGameRoomStateChangedEvent":{"gameRoomInfo":{"stateType":"MatchGameRoomStateType_Playing",'
        '"gameRoomConfig":{"matchId":"m1","eventId":"Traditional_Ladder","reservedPlayers":['
        '{"userId":"u1","playerName":"P1","systemSeatId":1,"teamId":1},'
        '{"userId":"u2","playerName":"P2","systemSeatId":2,"teamId":2}]}}}}',
    )

    event = match_state.try_parse(entry, TS)

    assert event is not None
    assert event.kind == "MatchState"
    assert event.performance_class == PerformanceClass.INTERACTIVE_DISPATCH
    assert event.metadata.timestamp == TS
    assert event.metadata.raw_bytes == entry.body.encode()
    assert event.payload["type"] == "match_started"
    assert event.payload["match_id"] == "m1"
    assert event.payload["event_id"] == "Traditional_Ladder"
    assert event.payload["players"] == [
        {"user_id": "u1", "player_name": "P1", "system_seat_id": 1, "team_id": 1},
        {"user_id": "u2", "player_name": "P2", "system_seat_id": 2, "team_id": 2},
    ]
    assert event.payload["raw_match_state"]["gameRoomInfo"]["gameRoomConfig"]["matchId"] == "m1"


def test_match_state_parse_bare_payload_shape() -> None:
    entry = _entry(
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
    entry = _entry(
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
    entry = _entry(
        '[UnityCrossThreadLogger]matchGameRoomStateChangedEvent\n'
        '{"matchGameRoomStateChangedEvent":{"gameRoomInfo":{"stateType":"MatchGameRoomStateType_Playing",'
        '"gameRoomConfig":{"matchId":"m4","reservedPlayers":['
        '{"userId":"u1","playerName":"P1","systemSeatId":1,"teamId":1,"eventId":"Fallback_Event"}]}}}}',
    )

    event = match_state.try_parse(entry, TS)

    assert event is not None
    assert event.payload["event_id"] == "Fallback_Event"


def test_match_state_falls_back_to_game_room_players_when_reserved_players_missing() -> None:
    entry = _entry(
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


def test_match_state_ignores_non_candidate_or_unparseable_bodies() -> None:
    assert match_state.try_parse(_entry('{"gameRoomInfo":{}}'), TS) is None
    assert match_state.try_parse(_entry("[UnityCrossThreadLogger]matchGameRoomStateChangedEvent\n{bad"), TS) is None
    assert (
        match_state.try_parse(
            _entry('[UnityCrossThreadLogger]matchGameRoomStateChangedEvent\n{"notMatchState":true}'),
            TS,
        )
        is None
    )
    assert (
        match_state.try_parse(
            _entry(
                '[UnityCrossThreadLogger]matchGameRoomStateChangedEvent\n'
                '{"matchGameRoomStateChangedEvent":"not-a-dict"}'
            ),
            TS,
        )
        is None
    )


def test_match_state_accepts_bare_payload_when_wrapper_value_is_not_a_dict() -> None:
    event = match_state.try_parse(
        _entry(
            '[UnityCrossThreadLogger]matchGameRoomStateChangedEvent\n'
            '{"matchGameRoomStateChangedEvent":"not-a-dict",'
            '"gameRoomInfo":{"stateType":"MatchGameRoomStateType_Playing",'
            '"gameRoomConfig":{"matchId":"m6","eventId":"Fallback_Bare"}}}'
        ),
        TS,
    )

    assert event is not None
    assert event.payload["type"] == "match_started"
    assert event.payload["match_id"] == "m6"
    assert event.payload["event_id"] == "Fallback_Bare"


def test_match_state_unknown_state_type_degrades_to_state_changed() -> None:
    payload = match_state.build_payload(
        {
            "gameRoomInfo": {
                "stateType": "MatchGameRoomStateType_NewFutureState",
                "gameRoomConfig": {"matchId": "m7"},
            }
        }
    )

    assert payload["type"] == "state_changed"
    assert payload["state_type"] == "MatchGameRoomStateType_NewFutureState"
    assert payload["match_id"] == "m7"


def test_match_state_player_source_precedence_filtering_and_defaults() -> None:
    payload = match_state.build_payload(
        {
            "gameRoomInfo": {
                "stateType": "MatchGameRoomStateType_Playing",
                "gameRoomConfig": {
                    "matchId": "m8",
                    "eventId": "  ",
                    "reservedPlayers": [
                        "bad-player",
                        {"userId": "u1", "eventId": " Player_Event ", "teamId": 1},
                        {"playerName": "P2", "systemSeatId": 2},
                    ],
                },
                "players": [
                    {"userId": "ignored", "playerName": "Ignored", "systemSeatId": 9, "teamId": 9}
                ],
            }
        }
    )

    assert payload["event_id"] == "Player_Event"
    assert payload["players"] == [
        {"user_id": "u1", "player_name": "", "system_seat_id": 0, "team_id": 1},
        {"user_id": "", "player_name": "P2", "system_seat_id": 2, "team_id": 0},
    ]


def test_match_state_config_event_id_precedes_player_event_id() -> None:
    payload = match_state.build_payload(
        {
            "gameRoomInfo": {
                "stateType": "MatchGameRoomStateType_Playing",
                "gameRoomConfig": {
                    "matchId": "m9",
                    "eventId": " Config_Event ",
                    "reservedPlayers": [{"eventId": "Player_Event"}],
                },
            }
        }
    )

    assert payload["event_id"] == "Config_Event"


def test_match_state_empty_reserved_players_falls_back_to_game_room_players() -> None:
    payload = match_state.build_payload(
        {
            "gameRoomInfo": {
                "stateType": "MatchGameRoomStateType_Playing",
                "gameRoomConfig": {
                    "matchId": "m10",
                    "reservedPlayers": [],
                },
                "players": [{"userId": "u-fallback", "playerName": "Fallback", "teamId": 2}],
            }
        }
    )

    assert payload["players"] == [
        {"user_id": "u-fallback", "player_name": "Fallback", "system_seat_id": 0, "team_id": 2}
    ]


def test_match_state_final_result_normalizes_malformed_and_partial_result_lists() -> None:
    non_list_payload = match_state.build_payload(
        {
            "gameRoomInfo": {
                "stateType": "MatchGameRoomStateType_MatchCompleted",
                "finalMatchResult": {"matchCompletedReason": "Done", "resultList": "not-a-list"},
            }
        }
    )

    assert non_list_payload["match_completed_reason"] == "Done"
    assert non_list_payload["game_results"] == []

    mixed_payload = match_state.build_payload(
        {
            "gameRoomInfo": {
                "stateType": "MatchGameRoomStateType_MatchCompleted",
                "finalMatchResult": {
                    "resultList": [
                        "bad-result",
                        {"scope": "MatchScope_Game", "winningTeamId": 2, "result": "R1"},
                        {"scope": "MatchScope_Match", "reason": "R2"},
                    ]
                },
            }
        }
    )

    assert mixed_payload["game_results"] == [
        {
            "scope": "MatchScope_Game",
            "result": "R1",
            "winning_team_id": 2,
            "reason": "",
        },
        {
            "scope": "MatchScope_Match",
            "result": "",
            "winning_team_id": 0,
            "reason": "R2",
        },
    ]
