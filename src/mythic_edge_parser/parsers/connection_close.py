from __future__ import annotations

from datetime import datetime
from typing import Any, Callable

from ..events import EventMetadata, GameEvent, TcpConnectionCloseEvent, WebSocketClosedEvent
from ..log.entry import EntryHeader, LogEntry
from . import api_common

_TCP_CONNECTION_CLOSE_MARKER = "Client.TcpConnection.Close"
_WEBSOCKET_CLOSED_MARKER = "GREConnection.HandleWebSocketClosed"
CloseEventFactory = Callable[[EventMetadata, dict[str, Any]], GameEvent]
_CLOSE_EVENT_RULES: tuple[tuple[str, CloseEventFactory], ...] = (
    (_TCP_CONNECTION_CLOSE_MARKER, TcpConnectionCloseEvent),
    (_WEBSOCKET_CLOSED_MARKER, WebSocketClosedEvent),
)


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    body = _unity_body(entry)
    if body is None:
        return None

    return _parse_connection_close_event(body, timestamp)


def _parse_connection_close_event(
    body: str,
    timestamp: datetime | None,
) -> GameEvent | None:
    for marker, event_factory in _CLOSE_EVENT_RULES:
        if marker not in body:
            continue
        return _build_close_event(body, timestamp, marker, event_factory)
    return None


def _unity_body(entry: LogEntry) -> str | None:
    if entry.header != EntryHeader.UNITY_CROSS_THREAD_LOGGER:
        return None
    return entry.body


def _build_close_event(
    body: str,
    timestamp: datetime | None,
    marker: str,
    event_factory: CloseEventFactory,
) -> GameEvent | None:
    payload = api_common.parse_json_from_body(body, marker)
    if payload is None:
        return None
    return event_factory(EventMetadata(timestamp, body.encode()), payload)
