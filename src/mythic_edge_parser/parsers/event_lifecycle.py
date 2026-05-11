from __future__ import annotations

import re
from datetime import datetime

from ..events import EventLifecycleEvent, EventMetadata, GameEvent
from ..log.entry import LogEntry

_EVENT_LIFECYCLE_PATTERNS = (
    ("event_join", re.compile(r"==>\s*EventJoin")),
    ("event_claim_prize", re.compile(r"==>\s*EventClaimPrize")),
    ("event_enter_pairing", re.compile(r"==>\s*EventEnterPairing")),
)


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    body = entry.body
    event_type = _matched_event_lifecycle_type(body)
    if event_type is not None:
        return _event_lifecycle_event(timestamp, body, event_type)
    return None


def _matched_event_lifecycle_type(body: str) -> str | None:
    for event_type, pattern in _EVENT_LIFECYCLE_PATTERNS:
        if pattern.search(body):
            return event_type
    return None


def _event_lifecycle_event(timestamp: datetime | None, body: str, event_type: str) -> EventLifecycleEvent:
    return EventLifecycleEvent(
        EventMetadata(timestamp, body.encode()),
        {
            "type": event_type,
            "raw_event_lifecycle": body,
        },
    )
