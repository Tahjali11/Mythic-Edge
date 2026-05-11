from __future__ import annotations

import re
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from threading import Lock

from . import parsers
from .events import GameEvent
from .log.entry import EntryHeader, LogEntry

_TIMESTAMP_RE = re.compile(
    r"\](?P<date>\d{1,2}/\d{1,2}/\d{4})\s+(?P<time>\d{1,2}:\d{2}:\d{2})\s+(?P<ampm>AM|PM)",
    re.IGNORECASE,
)
HEADER_PARSER_DISPATCH_ORDER = {
    EntryHeader.METADATA: (
        parsers.metadata,
    ),
    EntryHeader.CLIENT_GRE: (
        parsers.gre,
    ),
    EntryHeader.CONNECTION_MANAGER: (
        parsers.connection_error,
    ),
    EntryHeader.MATCHMAKING: (
        parsers.connection_error,
    ),
    EntryHeader.UNITY_CROSS_THREAD_LOGGER: (
        parsers.gre,
        parsers.client_actions,
        parsers.match_state,
        parsers.session,
        parsers.event_lifecycle,
        parsers.rank,
        parsers.collection,
        parsers.inventory,
        parsers.connection_state,
        parsers.connection_close,
        parsers.connection_error,
    ),
    EntryHeader.UNKNOWN: (
        parsers.gre,
        parsers.client_actions,
        parsers.match_state,
        parsers.session,
        parsers.event_lifecycle,
        parsers.rank,
        parsers.collection,
        parsers.inventory,
    ),
}


@dataclass(slots=True)
class RouterStats:
    routed: int = 0
    unknown: int = 0
    timestamp_missing: int = 0
    timestamp_parse_failure: int = 0

    @property
    def timestamp_anomalies(self) -> int:
        return self.timestamp_missing + self.timestamp_parse_failure


class Router:
    def __init__(self) -> None:
        self._stats = RouterStats()
        self._lock = Lock()

    @property
    def stats(self) -> RouterStats:
        with self._lock:
            return replace(self._stats)

    def reset(self) -> None:
        with self._lock:
            self._stats = RouterStats()

    def route(self, entry: LogEntry) -> list[GameEvent]:
        timestamp, timestamp_state = _extract_timestamp_state(entry.body)
        if timestamp_state == "missing":
            with self._lock:
                self._stats.timestamp_missing += 1
        elif timestamp_state == "parse_failure":
            with self._lock:
                self._stats.timestamp_parse_failure += 1
        events = dispatch_to_parsers(entry, timestamp)
        with self._lock:
            if events:
                self._stats.routed += 1
            else:
                self._stats.unknown += 1
        return events


def extract_timestamp(body: str) -> datetime | None:
    timestamp, _ = _extract_timestamp_state(body)
    return timestamp


def _extract_timestamp_state(body: str) -> tuple[datetime | None, str]:
    first_line = body.splitlines()[0] if body else ""
    match = _TIMESTAMP_RE.search(first_line)
    if not match:
        return None, "missing"
    try:
        ts = datetime.strptime(
            f"{match.group('date')} {match.group('time')} {match.group('ampm').upper()}",
            "%m/%d/%Y %I:%M:%S %p",
        )
    except ValueError:
        return None, "parse_failure"
    return ts.replace(tzinfo=UTC), "valid"


def dispatch_to_parsers(entry: LogEntry, timestamp: datetime | None) -> list[GameEvent]:
    for parser_module in _dispatch_order_for_header(entry.header):
        result = parser_module.try_parse(entry, timestamp)
        if not result:
            continue
        if isinstance(result, list):
            return result
        return [result]
    return []


def _dispatch_order_for_header(header: EntryHeader) -> tuple[object, ...]:
    return HEADER_PARSER_DISPATCH_ORDER.get(header, HEADER_PARSER_DISPATCH_ORDER[EntryHeader.UNKNOWN])
