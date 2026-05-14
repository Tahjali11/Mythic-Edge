from datetime import UTC, datetime

from mythic_edge_parser.events import PerformanceClass
from mythic_edge_parser.log.entry import EntryHeader, LogEntry
from mythic_edge_parser.parsers import client_actions, gre, match_state, metadata

TS = datetime(2026, 2, 25, 12, 0, 0, tzinfo=UTC)


def test_metadata_parse() -> None:
    entry = LogEntry(EntryHeader.METADATA, "DETAILED LOGS: ENABLED")
    event = metadata.try_parse(entry, None)
    assert event is not None
    assert event.payload["enabled"] is True


def test_match_state_parse() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]matchGameRoomStateChangedEvent\n"
        '{"matchGameRoomStateChangedEvent":{"gameRoomInfo":{"stateType":"MatchGameRoomStateType_Playing","gameRoomConfig":{"matchId":"m1","eventId":"Ladder","reservedPlayers":[{"userId":"u1","playerName":"P1","systemSeatId":1,"teamId":1},{"userId":"u2","playerName":"P2","systemSeatId":2,"teamId":2}]}}}}',
    )
    event = match_state.try_parse(entry, TS)
    assert event is not None
    assert event.payload["type"] == "match_started"
    assert event.payload["match_id"] == "m1"
    assert len(event.payload["players"]) == 2


def test_client_submit_deck_parse() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]ClientToGREMessage\n"
        '{"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientToGREMessage","payload":{"type":"ClientMessageType_SubmitDeckResp","gameStateId":5,"respId":1,"submitDeckResp":{"deckCards":[1,2,3],"sideboardCards":[4,5]}}}',
    )
    event = client_actions.try_parse(entry, TS)
    assert event is not None
    assert event.payload["type"] == "submit_deck_resp"
    assert event.payload["deck_cards"] == [1, 2, 3]
    assert event.payload["sideboard_cards"] == [4, 5]


def test_client_submit_deck_parse_nested_deck_shape() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]ClientToGREMessage\n"
        '{"clientToMatchServiceMessageType":"ClientToMatchServiceMessageType_ClientToGREMessage","payload":{"type":"ClientMessageType_SubmitDeckResp","gameStateId":5,"respId":1,"submitDeckResp":{"deck":{"deckCards":[11,12,13],"sideboardCards":[21,22]}}}}',
    )
    event = client_actions.try_parse(entry, TS)
    assert event is not None
    assert event.payload["type"] == "submit_deck_resp"
    assert event.payload["deck_cards"] == [11, 12, 13]
    assert event.payload["sideboard_cards"] == [21, 22]


def test_gre_game_over_emits_game_state_and_game_result() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]greToClientEvent\n"
        '{"greToClientEvent":{"greToClientMessages":[{"type":"GREMessageType_GameStateMessage","msgId":1,"gameStateMessage":{"gameInfo":{"stage":"GameStage_GameOver","matchState":"MatchState_GameComplete","results":[{"scope":"MatchScope_Game","winningTeamId":1,"result":"ResultType_WinLoss","reason":"ResultReason_Game"}]}}}]}}',
    )
    events = gre.try_parse(entry, TS)
    assert len(events) == 2
    assert events[0].kind == "GameState"
    assert events[1].kind == "GameResult"
    assert events[1].payload["winning_team_id"] == 1


def test_gre_game_over_uses_latest_game_scope_result_when_results_are_cumulative() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]greToClientEvent\n"
        '{"greToClientEvent":{"greToClientMessages":[{"type":"GREMessageType_GameStateMessage","msgId":1,"gameStateMessage":{"gameInfo":{"stage":"GameStage_GameOver","matchState":"MatchState_MatchComplete","results":[{"scope":"MatchScope_Game","winningTeamId":2,"result":"ResultType_WinLoss","reason":"ResultReason_Concede"},{"scope":"MatchScope_Game","winningTeamId":1,"result":"ResultType_WinLoss","reason":"ResultReason_Game"},{"scope":"MatchScope_Match","winningTeamId":1,"result":"ResultType_WinLoss","reason":"ResultReason_Game"}]}}}]}}',
    )

    events = gre.try_parse(entry, TS)

    assert len(events) == 2
    assert events[1].kind == "GameResult"
    assert events[1].payload["winning_team_id"] == 1
    assert events[1].payload["reason"] == "ResultReason_Game"


def test_gre_game_state_payload_is_enriched() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]greToClientEvent\n"
        '{"greToClientEvent":{"greToClientMessages":[{"type":"GREMessageType_GameStateMessage","msgId":7,"gameStateId":42,"systemSeatIds":[1],"gameStateMessage":{"gameInfo":{"matchID":"match-42","gameNumber":2,"stage":"GameStage_Play","matchState":"MatchState_GameInProgress"},"turnInfo":{"turnNumber":3,"activePlayer":2,"phase":"Phase_Main1","step":"Step_PreCombatMain"},"zones":[{"zoneId":31,"type":"ZoneType_Hand","visibility":"Visibility_Private","ownerSeatId":1,"objectInstanceIds":[101,102]}],"gameObjects":[{"instanceId":101,"grpId":91829},{"instanceId":102,"overlayGrpId":93940}],"players":[{"systemSeatNumber":1,"teamId":1},{"systemSeatNumber":2,"teamId":2}],"actions":[{"seatId":1,"action":{"actionType":"ActionType_Play","instanceId":101}}]}}]}}',
    )

    events = gre.try_parse(entry, TS)

    assert len(events) == 1
    payload = events[0].payload
    assert payload["game_state_id"] == 42
    assert payload["system_seat_ids"] == [1]
    assert payload["identity"]["match_id"] == "match-42"
    assert payload["identity"]["game_number"] == 2
    assert payload["turn_info"]["turn_number"] == 3
    assert payload["turn_info"]["active_player_seat_id"] == 2
    assert len(payload["zones"]) == 1
    assert len(payload["game_objects"]) == 2
    assert len(payload["players"]) == 2
    assert len(payload["actions"]) == 1


def test_gre_connect_resp_emits_game_state_event() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]greToClientEvent\n"
        '{"greToClientEvent":{"greToClientMessages":[{"type":"GREMessageType_ConnectResp","msgId":1,"gameStateId":4,"systemSeatIds":[1,2],"connectResp":{"deckMessage":{"deckCards":[11,12],"sideboardCards":[21]},"settings":{"matchClockSec":1800}}}]}}',
    )

    events = gre.try_parse(entry, TS)

    assert len(events) == 1
    assert events[0].kind == "GameState"
    assert events[0].payload["type"] == "connect_resp"
    assert events[0].payload["deck_cards"] == [11, 12]
    assert events[0].payload["sideboard_cards"] == [21]


def test_gre_direct_connect_resp_emits_game_state_event_with_metadata() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]GREMessageType_ConnectResp\n"
        '{"type":"GREMessageType_ConnectResp","msgId":1,"gameStateId":4,"systemSeatIds":[1],'
        '"connectResp":{"deckMessage":{"deckCards":[11],"sideboardCards":[21]},"settings":{"matchClockSec":1800}}}',
    )

    events = gre.try_parse(entry, TS)

    assert len(events) == 1
    assert events[0].kind == "GameState"
    assert events[0].performance_class == PerformanceClass.INTERACTIVE_DISPATCH
    assert events[0].metadata.timestamp is TS
    assert events[0].metadata.raw_bytes == entry.body.encode()
    assert events[0].payload["type"] == "connect_resp"
    assert events[0].payload["system_seat_ids"] == [1]


def test_gre_connect_resp_requires_dict_connect_resp_for_dispatch_event() -> None:
    missing_connect_resp = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]GREMessageType_ConnectResp\n"
        '{"type":"GREMessageType_ConnectResp","msgId":1,"gameStateId":4}',
    )
    malformed_connect_resp = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]GREMessageType_ConnectResp\n"
        '{"type":"GREMessageType_ConnectResp","msgId":1,"gameStateId":4,"connectResp":"bad"}',
    )

    assert gre.try_parse(missing_connect_resp, TS) == []
    assert gre.try_parse(malformed_connect_resp, TS) == []


def test_gre_game_state_payload_takes_precedence_over_connect_resp_on_same_message() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]greToClientEvent\n"
        '{"greToClientEvent":{"greToClientMessages":[{"type":"GREMessageType_ConnectResp",'
        '"msgId":1,"gameStateId":4,"systemSeatIds":[1],"connectResp":{"deckMessage":{"deckCards":[11]}},'
        '"gameStateMessage":{"gameInfo":{"matchID":"match-gsm","gameNumber":1,'
        '"stage":"GameStage_Play","matchState":"MatchState_GameInProgress"}}}]}}',
    )

    events = gre.try_parse(entry, TS)

    assert len(events) == 1
    assert events[0].kind == "GameState"
    assert events[0].payload["type"] == "game_state_message"
    assert events[0].payload["identity"]["match_id"] == "match-gsm"


def test_gre_queued_game_state_message_emits_queued_payload_type() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]greToClientEvent\n"
        '{"greToClientEvent":{"greToClientMessages":[{"type":"GREMessageType_QueuedGameStateMessage","msgId":5,"gameStateId":9,"queuedGameStateMessage":{"gameStateMessage":{"gameInfo":{"matchID":"queued-1","gameNumber":1,"stage":"GameStage_Play","matchState":"MatchState_GameInProgress"}}}}]}}',
    )

    events = gre.try_parse(entry, TS)

    assert len(events) == 1
    assert events[0].kind == "GameState"
    assert events[0].payload["type"] == "queued_game_state_message"
    assert events[0].payload["identity"]["match_id"] == "queued-1"


def test_gre_ignores_non_dict_messages_inside_batch() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]greToClientEvent\n"
        '{"greToClientEvent":{"greToClientMessages":["bad",{"type":"GREMessageType_ConnectResp","msgId":1,"gameStateId":4,"systemSeatIds":[1],"connectResp":{"deckMessage":{"deckCards":[11]}}}]}}',
    )

    events = gre.try_parse(entry, TS)

    assert len(events) == 1
    assert events[0].kind == "GameState"
    assert events[0].payload["type"] == "connect_resp"


def test_gre_returns_empty_when_message_list_shape_is_invalid() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]greToClientEvent\n"
        '{"greToClientEvent":{"greToClientMessages":{"not":"a list"}}}',
    )

    assert gre.try_parse(entry, TS) == []
