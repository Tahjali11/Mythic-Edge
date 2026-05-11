from __future__ import annotations

from datetime import datetime
from typing import Callable

from ..events import ConnectionErrorEvent, EventMetadata, GameEvent
from ..log.entry import EntryHeader, LogEntry
from . import api_common

_PROCESS_READ_EXCEPTION_MARKER = "TcpConnection.ProcessRead.Exception"
_PROCESS_FAILURE_MARKER = "Client.TcpConnection.ProcessFailure"
_MATCH_DOOR_ERROR_MARKER = "GREConnection.MatchDoorConnectionError"
_CLOSE_EXCEPTION_MARKER = "TcpConnection.Close.Exception"

_ERROR_TYPE_PROCESS_READ = "tcp_process_read_exception"
_ERROR_TYPE_PROCESS_FAILURE = "tcp_process_failure_socket_error"
_ERROR_TYPE_MATCH_DOOR = "gre_match_door_connection_error"
_ERROR_TYPE_CLOSE_EXCEPTION = "tcp_close_exception"

_UNITY_ERROR_MARKERS: tuple[tuple[str, str], ...] = (
    (_PROCESS_READ_EXCEPTION_MARKER, _ERROR_TYPE_PROCESS_READ),
    (_PROCESS_FAILURE_MARKER, _ERROR_TYPE_PROCESS_FAILURE),
    (_MATCH_DOOR_ERROR_MARKER, _ERROR_TYPE_MATCH_DOOR),
    (_CLOSE_EXCEPTION_MARKER, _ERROR_TYPE_CLOSE_EXCEPTION),
)

_RECONNECT_RESULT_VALUES = {"Connected", "Error", "None"}
ConnectionManagerParser = Callable[[str], dict[str, object] | None]


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    payload = _parse_connection_error_payload(entry)

    if payload is None:
        return None

    return ConnectionErrorEvent(EventMetadata(timestamp, entry.body.encode()), payload)


def _parse_connection_error_payload(entry: LogEntry) -> dict[str, object] | None:
    unity_body = _unity_body(entry)
    if unity_body is not None:
        return _try_unity_error(unity_body)

    connection_manager_content = _connection_manager_content(entry)
    if connection_manager_content is not None:
        return _try_connection_manager(connection_manager_content)

    matchmaking_body = _matchmaking_body(entry)
    if matchmaking_body is not None:
        return _try_matchmaking(matchmaking_body)
    return None


def _try_unity_error(body: str) -> dict[str, object] | None:
    for marker, error_type in _UNITY_ERROR_MARKERS:
        if marker in body:
            return _try_exception_marker(body, marker, error_type)
    return None


def _try_exception_marker(body: str, marker: str, error_type: str) -> dict[str, object] | None:
    parsed = api_common.parse_json_from_body(body, marker)
    if parsed is None:
        return None
    return {"error_type": error_type, "payload": parsed}


def _try_connection_manager(content: str) -> dict[str, object] | None:
    for parser in _CONNECTION_MANAGER_PARSERS:
        payload = parser(content)
        if payload is not None:
            return payload
    return None


def _try_matchmaking(body: str) -> dict[str, object] | None:
    if body.startswith("Matchmaking: GRE connection lost"):
        return {"error_type": "gre_connection_lost"}
    return None


def _parse_reconnect_result(content: str) -> dict[str, object] | None:
    prefix = "Reconnect result : "
    if not content.startswith(prefix):
        return None
    result = content.removeprefix(prefix).strip()
    if result not in _RECONNECT_RESULT_VALUES:
        return None
    return {"error_type": "reconnect_result", "result": result}


def _parse_reconnect_succeeded(content: str) -> dict[str, object] | None:
    prefix = "Reconnect succeeded after "
    if not content.startswith(prefix):
        return None
    attempts = _leading_int_token(content.removeprefix(prefix))
    return {
        "error_type": "reconnect_outcome",
        "outcome": "succeeded",
        "attempts": attempts,
    }


def _parse_reconnect_failed(content: str) -> dict[str, object] | None:
    if not content.startswith("Reconnect failed"):
        return None
    return {
        "error_type": "reconnect_outcome",
        "outcome": "failed",
        "attempts": None,
    }


def _parse_reconnect_timed_out(content: str) -> dict[str, object] | None:
    if not content.startswith("Reconnect timed out"):
        return None
    return {
        "error_type": "reconnect_outcome",
        "outcome": "timed_out",
        "attempts": None,
    }


_CONNECTION_MANAGER_PARSERS: tuple[ConnectionManagerParser, ...] = (
    _parse_reconnect_result,
    _parse_reconnect_succeeded,
    _parse_reconnect_failed,
    _parse_reconnect_timed_out,
)


def _unity_body(entry: LogEntry) -> str | None:
    if entry.header == EntryHeader.UNITY_CROSS_THREAD_LOGGER:
        return entry.body
    return None


def _connection_manager_content(entry: LogEntry) -> str | None:
    if entry.header != EntryHeader.CONNECTION_MANAGER:
        return None
    content = entry.body.strip()
    if content.startswith("[ConnectionManager]"):
        content = content.removeprefix("[ConnectionManager]").strip()
    return content or None


def _matchmaking_body(entry: LogEntry) -> str | None:
    if entry.header == EntryHeader.MATCHMAKING:
        return entry.body
    return None


def _leading_int_token(text: str) -> int | None:
    token = text.split(maxsplit=1)[0]
    if token.isdigit():
        return int(token)
    return None
