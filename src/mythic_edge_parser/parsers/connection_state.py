from __future__ import annotations

from datetime import datetime
from typing import Any

from ..events import EventMetadata, GameEvent, MatchConnectionStateEvent
from ..log.entry import EntryHeader, LogEntry
from . import api_common

_STATE_CHANGED_MARKER = "STATE CHANGED "


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    body = _state_change_body(entry)
    if body is None:
        return None

    payload = _parse_state_change_payload(body)
    if payload is None:
        return None

    return MatchConnectionStateEvent(
        EventMetadata(timestamp, body.encode()),
        payload,
    )


def _state_change_body(entry: LogEntry) -> str | None:
    if entry.header != EntryHeader.UNITY_CROSS_THREAD_LOGGER:
        return None
    if _STATE_CHANGED_MARKER not in entry.body:
        return None
    return entry.body


def _parse_state_change_payload(body: str) -> dict[str, str] | None:
    parsed = api_common.parse_json_from_body(body, "STATE CHANGED")
    if parsed is None:
        return None
    return _extract_state_transition(parsed)


def _extract_state_transition(parsed: dict[str, Any]) -> dict[str, str] | None:
    old_state = _state_value(parsed, "old")
    new_state = _state_value(parsed, "new")
    if old_state is None or new_state is None:
        return None
    return {"old": old_state, "new": new_state}


def _state_value(parsed: dict[str, Any], field: str) -> str | None:
    value = parsed.get(field)
    if isinstance(value, str):
        return value
    return None
