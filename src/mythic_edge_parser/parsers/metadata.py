from __future__ import annotations

from datetime import datetime

from ..events import DetailedLoggingStatusEvent, EventMetadata, GameEvent
from ..log.entry import EntryHeader, LogEntry

_DETAILED_LOGGING_STATUS_BY_BODY = {
    "DETAILED LOGS: ENABLED": True,
    "DETAILED LOGS: DISABLED": False,
}


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    enabled = _logging_enabled_value(entry)
    if enabled is None:
        return None
    return DetailedLoggingStatusEvent(EventMetadata(timestamp, entry.body.encode()), {"enabled": enabled})


def _logging_enabled_value(entry: LogEntry) -> bool | None:
    if entry.header != EntryHeader.METADATA:
        return None
    return _DETAILED_LOGGING_STATUS_BY_BODY.get(entry.body.strip())
