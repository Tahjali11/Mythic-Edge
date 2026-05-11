from __future__ import annotations

from datetime import datetime
from typing import Any

from ..events import EventMetadata, GameEvent, RankEvent
from ..log.entry import LogEntry
from . import api_common

METHOD = "RankGetCombinedRankInfo"
_TEXT_DEFAULT = ""


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    body = entry.body
    parsed = _rank_response_payload(body)
    if parsed is None:
        return None
    payload = _build_rank_payload(parsed)
    return RankEvent(EventMetadata(timestamp, body.encode()), payload)


def _rank_response_payload(body: str) -> dict[str, Any] | None:
    if not api_common.is_api_response(body, METHOD):
        return None
    return api_common.parse_json_from_body(body, METHOD)


def _scalar_field(parsed: dict[str, Any], field: str, default: Any = None) -> Any:
    value = parsed.get(field, default)
    if isinstance(value, (dict, list, tuple, set)):
        return default
    return value


def _build_rank_payload(parsed: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "rank_snapshot",
        "constructed_class": _scalar_field(parsed, "constructedClass", _TEXT_DEFAULT),
        "constructed_level": _scalar_field(parsed, "constructedLevel", _TEXT_DEFAULT),
        "limited_class": _scalar_field(parsed, "limitedClass", _TEXT_DEFAULT),
        "limited_level": _scalar_field(parsed, "limitedLevel", _TEXT_DEFAULT),
        "constructed_percentile": _scalar_field(parsed, "constructedPercentile"),
        "limited_percentile": _scalar_field(parsed, "limitedPercentile"),
        "raw_rank": parsed,
    }
