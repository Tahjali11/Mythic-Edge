from __future__ import annotations

import re
from datetime import datetime

from ..events import EventMetadata, GameEvent, TruncationEvent
from ..log.entry import TRUNCATION_MARKER_PREFIX, LogEntry

_GAME_OBJECT_COUNT_RE = re.compile(r"^\s*GameObject Count\s*[:=]\s*(?P<value>[+-]?\d+)\s*$")
_ANNOTATION_COUNT_RE = re.compile(r"^\s*Annotation Count\s*[:=]\s*(?P<value>[+-]?\d+)\s*$")


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    body = entry.body if isinstance(entry.body, str) else ""
    if not _is_explicit_marker_body(body):
        return None

    game_object_count = _first_nonnegative_int(body, _GAME_OBJECT_COUNT_RE)
    annotation_count = _first_nonnegative_int(body, _ANNOTATION_COUNT_RE)
    payload = {
        "type": "game_state_message_truncation",
        "marker_family": "game_state_message_truncation",
        "affected_event_family": "GameState",
        "affected_message_type": "GREMessageType_GameStateMessage",
        "data_loss": True,
        "recoverable": False,
        "parser_confidence": "explicit_marker",
        "value_source": "observed",
        "confidence": "high",
        "finality": "live",
        "drift_flag": "missing_expected_payload_path",
        "source_header": _source_header_value(entry),
        "game_object_count": game_object_count,
        "annotation_count": annotation_count,
        "raw_marker_summary": _summary(game_object_count, annotation_count),
    }
    return TruncationEvent(EventMetadata(timestamp, body.encode()), payload)


def _is_explicit_marker_body(body: str) -> bool:
    for line in body.splitlines() or [body]:
        if not line.strip():
            continue
        return line.lstrip().startswith(TRUNCATION_MARKER_PREFIX)
    return False


def _first_nonnegative_int(body: str, pattern: re.Pattern[str]) -> int | None:
    for line in body.splitlines():
        match = pattern.match(line)
        if not match:
            continue
        value = _nonnegative_int(match.group("value"))
        if value is not None:
            return value
    return None


def _nonnegative_int(value: str) -> int | None:
    try:
        parsed = int(value)
    except ValueError:
        return None
    if parsed < 0:
        return None
    return parsed


def _source_header_value(entry: LogEntry) -> str:
    header = getattr(entry, "header", "")
    value = getattr(header, "value", header)
    return str(value)


def _summary(game_object_count: int | None, annotation_count: int | None) -> str:
    fields: list[str] = ["game_state_message_truncation"]
    if game_object_count is not None:
        fields.append(f"game_object_count={game_object_count}")
    if annotation_count is not None:
        fields.append(f"annotation_count={annotation_count}")
    return "; ".join(fields)
