from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..events import DraftBotEvent, EventMetadata, GameEvent
from ..log.entry import LogEntry
from . import api_common

BOT_DRAFT_STATUS_MARKER = "BotDraftDraftStatus"
BOT_DRAFT_PICK_MARKER = "BotDraftDraftPick"

_API_MARKER_RE = re.compile(
    rf"(?P<prefix>==>|<==)\s*(?P<method>{BOT_DRAFT_STATUS_MARKER}|{BOT_DRAFT_PICK_MARKER})\b"
)
_PAYLOAD_TYPE_BY_METHOD = {
    BOT_DRAFT_STATUS_MARKER: "bot_draft_status",
    BOT_DRAFT_PICK_MARKER: "bot_draft_pick",
}

_DRAFT_ID_ALIASES = ("draftId", "DraftId", "draftID")
_EVENT_ID_ALIASES = ("eventId", "EventId", "eventID", "eventName", "EventName")
_DRAFT_STATUS_ALIASES = ("draftStatus", "DraftStatus", "status", "state")
_PACK_NUMBER_ALIASES = ("packNumber", "PackNumber", "pack", "Pack")
_PICK_NUMBER_ALIASES = ("pickNumber", "PickNumber", "pick", "Pick")
_PACK_CARD_IDS_ALIASES = ("packCardIds", "packCards", "PackCards", "cards", "Cards", "draftPack", "DraftPack")
_PICKED_CARD_ID_ALIASES = ("pickedCardId", "PickedCardId", "pickGrpId", "PickGrpId", "cardId", "grpId")
_PICKED_CARD_IDS_ALIASES = ("pickedCardIds", "pickedCards", "pickedGrpIds", "PickedGrpIds")


@dataclass(frozen=True, slots=True)
class _MatchedMarker:
    method: str
    api_direction: str


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    marker = _first_bot_draft_marker(entry.body)
    if marker is None:
        return None

    parsed = api_common.parse_json_from_body(entry.body, marker.method)
    if parsed is None:
        return None

    source = _normalization_source(parsed, marker.method)
    return DraftBotEvent(
        EventMetadata(timestamp, entry.body.encode()),
        _build_payload(marker, parsed, source),
    )


def _first_bot_draft_marker(body: str) -> _MatchedMarker | None:
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
    picked_card_ids = _nonnegative_int_list_field(source, _PICKED_CARD_IDS_ALIASES)
    picked_card_id = _picked_card_id(source, picked_card_ids)
    return {
        "type": _PAYLOAD_TYPE_BY_METHOD[marker.method],
        "source_method": marker.method,
        "api_direction": marker.api_direction,
        "draft_id": _text_field(source, _DRAFT_ID_ALIASES),
        "event_id": _text_field(source, _EVENT_ID_ALIASES),
        "draft_status": _text_field(source, _DRAFT_STATUS_ALIASES),
        "pack_number": _nonnegative_int_field(source, _PACK_NUMBER_ALIASES),
        "pick_number": _nonnegative_int_field(source, _PICK_NUMBER_ALIASES),
        "pack_card_ids": _nonnegative_int_list_field(source, _PACK_CARD_IDS_ALIASES),
        "picked_card_id": picked_card_id,
        "picked_card_ids": picked_card_ids,
        "raw_draft_bot": parsed,
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


def _nonnegative_int_field(source: dict[str, Any], aliases: tuple[str, ...]) -> int | None:
    value, _ = _first_alias_value(source, aliases)
    return _nonnegative_int(value)


def _nonnegative_int_list_field(source: dict[str, Any], aliases: tuple[str, ...]) -> list[int]:
    value, _ = _first_alias_value(source, aliases)
    if not isinstance(value, list):
        return []
    normalized: list[int] = []
    for item in value:
        integer = _nonnegative_int(item)
        if integer is not None:
            normalized.append(integer)
    return normalized


def _picked_card_id(source: dict[str, Any], picked_card_ids: list[int]) -> int | None:
    value, present = _first_alias_value(source, _PICKED_CARD_ID_ALIASES)
    if present:
        return _nonnegative_int(value)
    if picked_card_ids:
        return picked_card_ids[0]
    return None


def _nonnegative_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        if value >= 0:
            return value
        return None
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.isdigit():
            return int(stripped)
    return None
