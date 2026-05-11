from datetime import UTC, datetime

from mythic_edge_parser.log.entry import EntryHeader, LogEntry
from mythic_edge_parser.parsers import connection_close, connection_error, connection_state

TS = datetime(2026, 5, 5, 12, 0, 0, tzinfo=UTC)


def test_connection_state_parse() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]STATE CHANGED {"old":"Playing","new":"Disconnected"}',
    )
    event = connection_state.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "MatchConnectionState"
    assert event.payload == {"old": "Playing", "new": "Disconnected"}


def test_connection_state_rejects_non_unity_header() -> None:
    entry = LogEntry(
        EntryHeader.CONNECTION_MANAGER,
        '[UnityCrossThreadLogger]STATE CHANGED {"old":"Playing","new":"Disconnected"}',
    )
    assert connection_state.try_parse(entry, TS) is None


def test_connection_state_rejects_malformed_json() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]STATE CHANGED {"old":"Playing","new"',
    )
    assert connection_state.try_parse(entry, TS) is None


def test_connection_state_rejects_non_string_transition_values() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]STATE CHANGED {"old":"Playing","new":7}',
    )
    assert connection_state.try_parse(entry, TS) is None


def test_connection_state_rejects_non_mapping_json_payload() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]STATE CHANGED ["Playing","Disconnected"]',
    )
    assert connection_state.try_parse(entry, TS) is None


def test_tcp_connection_close_parse() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]Client.TcpConnection.Close {"status":7,"reason":"Closed by remote end"}',
    )
    event = connection_close.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "TcpConnectionClose"
    assert event.payload["status"] == 7
    assert event.payload["reason"] == "Closed by remote end"


def test_tcp_connection_close_preserves_richer_payload() -> None:
    body = (
        "[UnityCrossThreadLogger]Client.TcpConnection.Close "
        '{"status":2,"reason":"MatchManager.Reset","host":"matchdoor.example","port":30003,'
        '"lastLocalActivity":[{"type":"Close","status":2}]}'
    )
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        body,
    )
    event = connection_close.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "TcpConnectionClose"
    assert event.payload["host"] == "matchdoor.example"
    assert event.payload["port"] == 30003
    assert event.payload["lastLocalActivity"][0]["type"] == "Close"


def test_websocket_closed_parse() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]GREConnection.HandleWebSocketClosed {"closeType":1,"reason":"network"}',
    )
    event = connection_close.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "WebSocketClosed"
    assert event.payload["closeType"] == 1


def test_websocket_closed_preserves_nested_tcp_payload() -> None:
    body = (
        "[UnityCrossThreadLogger]GREConnection.HandleWebSocketClosed "
        '{"closeType":7,"reason":"Closed by remote end","tcpConn":{"host":"matchdoor.example","port":30003}}'
    )
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        body,
    )
    event = connection_close.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "WebSocketClosed"
    assert event.payload["tcpConn"]["host"] == "matchdoor.example"
    assert event.payload["tcpConn"]["port"] == 30003


def test_connection_close_rejects_non_unity_header() -> None:
    entry = LogEntry(
        EntryHeader.CONNECTION_MANAGER,
        '[UnityCrossThreadLogger]Client.TcpConnection.Close {"status":7,"reason":"Closed by remote end"}',
    )
    assert connection_close.try_parse(entry, TS) is None


def test_connection_close_rejects_malformed_json() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]GREConnection.HandleWebSocketClosed {"closeType":7',
    )
    assert connection_close.try_parse(entry, TS) is None


def test_connection_close_rejects_non_mapping_json_payload() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]GREConnection.HandleWebSocketClosed ["bad"]',
    )
    assert connection_close.try_parse(entry, TS) is None


def test_connection_close_ignores_unrelated_unity_line() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]SomeOtherCloseEvent {}",
    )
    assert connection_close.try_parse(entry, TS) is None


def test_connection_error_json_marker_parse() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]GREConnection.MatchDoorConnectionError {"reason":"Connection lost","code":500}',
    )
    event = connection_error.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "ConnectionError"
    assert event.payload["error_type"] == "gre_match_door_connection_error"
    assert event.payload["payload"]["reason"] == "Connection lost"


def test_connection_error_process_read_exception_parse() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]TcpConnection.ProcessRead.Exception {"message":"socket read failed","code":10054}',
    )
    event = connection_error.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "ConnectionError"
    assert event.payload["error_type"] == "tcp_process_read_exception"
    assert event.payload["payload"]["code"] == 10054


def test_connection_error_process_failure_parse() -> None:
    body = (
        "[UnityCrossThreadLogger]Client.TcpConnection.ProcessFailure "
        '{"message":"socket failure","socketError":"ConnectionReset"}'
    )
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        body,
    )
    event = connection_error.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "ConnectionError"
    assert event.payload["error_type"] == "tcp_process_failure_socket_error"
    assert event.payload["payload"]["socketError"] == "ConnectionReset"


def test_connection_error_close_exception_parse() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]TcpConnection.Close.Exception {"message":"close failed"}',
    )
    event = connection_error.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "ConnectionError"
    assert event.payload["error_type"] == "tcp_close_exception"
    assert event.payload["payload"]["message"] == "close failed"


def test_connection_error_connection_manager_parse() -> None:
    entry = LogEntry(
        EntryHeader.CONNECTION_MANAGER,
        "[ConnectionManager] Reconnect succeeded after 3 attempts",
    )
    event = connection_error.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "ConnectionError"
    assert event.payload == {
        "error_type": "reconnect_outcome",
        "outcome": "succeeded",
        "attempts": 3,
    }


def test_connection_error_connection_manager_result_parse() -> None:
    entry = LogEntry(
        EntryHeader.CONNECTION_MANAGER,
        "[ConnectionManager] Reconnect result : Error",
    )
    event = connection_error.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "ConnectionError"
    assert event.payload == {
        "error_type": "reconnect_result",
        "result": "Error",
    }


def test_connection_error_connection_manager_without_literal_prefix_still_parses() -> None:
    entry = LogEntry(
        EntryHeader.CONNECTION_MANAGER,
        "Reconnect failed",
    )
    event = connection_error.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "ConnectionError"
    assert event.payload == {
        "error_type": "reconnect_outcome",
        "outcome": "failed",
        "attempts": None,
    }


def test_connection_error_connection_manager_failed_parse() -> None:
    entry = LogEntry(
        EntryHeader.CONNECTION_MANAGER,
        "[ConnectionManager] Reconnect failed",
    )
    event = connection_error.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "ConnectionError"
    assert event.payload == {
        "error_type": "reconnect_outcome",
        "outcome": "failed",
        "attempts": None,
    }


def test_connection_error_connection_manager_timed_out_parse() -> None:
    entry = LogEntry(
        EntryHeader.CONNECTION_MANAGER,
        "[ConnectionManager] Reconnect timed out",
    )
    event = connection_error.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "ConnectionError"
    assert event.payload == {
        "error_type": "reconnect_outcome",
        "outcome": "timed_out",
        "attempts": None,
    }


def test_connection_error_connection_manager_rejects_unknown_result() -> None:
    entry = LogEntry(
        EntryHeader.CONNECTION_MANAGER,
        "[ConnectionManager] Reconnect result : WeirdValue",
    )
    assert connection_error.try_parse(entry, TS) is None


def test_connection_error_matchmaking_parse() -> None:
    entry = LogEntry(
        EntryHeader.MATCHMAKING,
        "Matchmaking: GRE connection lost, attempting reconnect",
    )
    event = connection_error.try_parse(entry, TS)
    assert event is not None
    assert event.kind == "ConnectionError"
    assert event.payload["error_type"] == "gre_connection_lost"


def test_connection_error_ignores_non_matching_entries() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]TotallyDifferentMarker {}",
    )
    assert connection_error.try_parse(entry, TS) is None
