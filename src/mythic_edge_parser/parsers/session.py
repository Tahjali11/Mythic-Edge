from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from ..events import EventMetadata, GameEvent, SessionEvent
from ..log.entry import LogEntry
from . import api_common

_UPDATED_ACCOUNT_RE = re.compile(
    r"Updated account\.\s*DisplayName:(?P<display>[^,]*)(?:,\s*AccountID:\s*(?P<account>[^\s,]+))?"
)
_AUTHENTICATE_RESPONSE_NAMES = ("AuthenticateResponse", "authenticateResponse")
_LOGOUT_RE = re.compile(r"\blogout\b", re.IGNORECASE)


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    body = entry.body
    event = _try_parse_account_update(body, timestamp)
    if event is not None:
        return event
    event = _try_parse_authenticate_response(body, timestamp)
    if event is not None:
        return event
    return _try_parse_logout(body, timestamp)


def _try_parse_account_update(body: str, timestamp: datetime | None) -> GameEvent | None:
    account_match = _UPDATED_ACCOUNT_RE.search(body)
    if account_match is None:
        return None
    return _session_event(
        timestamp,
        body,
        {
            "type": "session_account_update",
            "display_name": (account_match.group("display") or "").strip(),
            "account_id": (account_match.group("account") or "").strip(),
            "raw_session": body,
        },
    )


def _try_parse_authenticate_response(body: str, timestamp: datetime | None) -> GameEvent | None:
    parsed = _authenticate_response_payload(body)
    if parsed is None:
        return None
    return _session_event(
        timestamp,
        body,
        {
            "type": "session_authenticated",
            "display_name": _text_value(parsed.get("displayName")),
            "account_id": _text_value(parsed.get("accountId")),
            "screen_name": _text_value(parsed.get("screenName")),
            "raw_session": parsed,
        },
    )


def _try_parse_logout(body: str, timestamp: datetime | None) -> GameEvent | None:
    if _LOGOUT_RE.search(body) is None:
        return None
    return _session_event(timestamp, body, {"type": "session_logout", "raw_session": body})


def _authenticate_response_payload(body: str) -> dict[str, Any] | None:
    if not any(api_common.is_api_response(body, name) for name in _AUTHENTICATE_RESPONSE_NAMES):
        return None
    return api_common.parse_json_from_body(body, "AuthenticateResponse")


def _text_value(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    return ""


def _session_event(timestamp: datetime | None, body: str, payload: dict[str, Any]) -> SessionEvent:
    return SessionEvent(EventMetadata(timestamp, body.encode()), payload)
