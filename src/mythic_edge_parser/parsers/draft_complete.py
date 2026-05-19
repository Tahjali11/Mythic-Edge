from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..events import DraftCompleteEvent, EventMetadata, GameEvent
from ..log.entry import LogEntry
from . import api_common

DRAFT_COMPLETE_DRAFT_MARKER = "DraftCompleteDraft"

_API_MARKER_RE = re.compile(
    rf"(?P<prefix>==>|<==)\s*(?P<method>{re.escape(DRAFT_COMPLETE_DRAFT_MARKER)})(?![A-Za-z0-9_.])"
)

_DRAFT_ID_ALIASES = ("draftId", "DraftId", "draftID")
_EVENT_ID_ALIASES = ("eventId", "EventId", "eventID", "eventName", "EventName")
_QUEUE_ID_ALIASES = ("queueId", "QueueId", "queueID", "queueName", "QueueName", "eventQueueId", "EventQueueId")
_DRAFT_STATUS_ALIASES = ("draftStatus", "DraftStatus", "status", "state")
_COMPLETION_STATUS_ALIASES = (
    "completionStatus",
    "CompletionStatus",
    "completeStatus",
    "CompleteStatus",
    "result",
    "Result",
    "reason",
    "Reason",
)
_DRAFT_TYPE_ALIASES = ("draftType", "DraftType", "draftCategory", "DraftCategory", "type", "Type")
_DRAFT_MODE_ALIASES = ("draftMode", "DraftMode", "mode", "Mode", "draftKind", "DraftKind")
_COMPLETION_SOURCE_ALIASES = ("completionSource", "CompletionSource", "source", "Source")
_IS_BOT_DRAFT_ALIASES = ("isBotDraft", "IsBotDraft", "botDraft", "BotDraft")
_IS_HUMAN_DRAFT_ALIASES = ("isHumanDraft", "IsHumanDraft", "humanDraft", "HumanDraft")


@dataclass(frozen=True, slots=True)
class _MatchedMarker:
    method: str
    api_direction: str


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    marker = _first_draft_complete_marker(entry.body)
    if marker is None:
        return None

    parsed = api_common.parse_json_from_body(entry.body, marker.method)
    if parsed is None:
        return None

    source = _normalization_source(parsed, marker.method)
    return DraftCompleteEvent(
        EventMetadata(timestamp, entry.body.encode()),
        _build_payload(marker, parsed, source),
    )


def _first_draft_complete_marker(body: str) -> _MatchedMarker | None:
    match = _API_MARKER_RE.search(body)
    if match is None:
        return None
    prefix = match.group("prefix")
    return _MatchedMarker(
        method=match.group("method"),
        api_direction="request" if prefix == "==>" else "response",
    )


def _normalization_source(parsed: dict[str, Any], method: str) -> dict[str, Any]:
    nested = parsed.get(method)
    if isinstance(nested, dict):
        return nested
    return parsed


def _build_payload(
    marker: _MatchedMarker,
    parsed: dict[str, Any],
    source: dict[str, Any],
) -> dict[str, Any]:
    return {
        "type": "draft_complete_draft",
        "source_method": marker.method,
        "api_direction": marker.api_direction,
        "draft_id": _text_field(source, _DRAFT_ID_ALIASES),
        "event_id": _text_field(source, _EVENT_ID_ALIASES),
        "queue_id": _text_field(source, _QUEUE_ID_ALIASES),
        "draft_status": _text_field(source, _DRAFT_STATUS_ALIASES),
        "completion_status": _text_field(source, _COMPLETION_STATUS_ALIASES),
        "draft_type": _text_field(source, _DRAFT_TYPE_ALIASES),
        "draft_mode": _text_field(source, _DRAFT_MODE_ALIASES),
        "completion_source": _completion_source(source),
        "is_bot_draft": _bool_field(source, _IS_BOT_DRAFT_ALIASES),
        "is_human_draft": _bool_field(source, _IS_HUMAN_DRAFT_ALIASES),
        "raw_draft_complete": parsed,
    }


def _first_alias_value(source: dict[str, Any], aliases: tuple[str, ...]) -> tuple[Any, bool]:
    for alias in aliases:
        if alias in source:
            return source[alias], True
    return None, False


def _text_field(source: dict[str, Any], aliases: tuple[str, ...]) -> str:
    value, _ = _first_alias_value(source, aliases)
    if isinstance(value, str):
        return value.strip()
    return ""


def _completion_source(source: dict[str, Any]) -> str:
    value = _text_field(source, _COMPLETION_SOURCE_ALIASES)
    return value or DRAFT_COMPLETE_DRAFT_MARKER


def _bool_field(source: dict[str, Any], aliases: tuple[str, ...]) -> bool | None:
    value, _ = _first_alias_value(source, aliases)
    if isinstance(value, bool):
        return value
    return None
