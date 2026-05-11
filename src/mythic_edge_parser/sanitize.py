from __future__ import annotations

import re
from typing import Callable

_PATTERNS: list[tuple[re.Pattern[str], str | Callable[[re.Match[str]], str]]] = [
    (re.compile(r"Token:\s*\S+"), "Token: <REDACTED>"),
    (re.compile(r"(?i)authorization:\s*bearer\s+[A-Za-z0-9._\-+/=]+"), "Authorization: Bearer <REDACTED>"),
    (re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._\-+/=]+"), "Bearer <REDACTED>"),
    (
        re.compile(r'(?i)(access[_ -]?token|refresh[_ -]?token|id[_ -]?token)"?\s*[:=]\s*"[^"]+"'),
        r'\1:"<REDACTED>"',
    ),
    (
        re.compile(r'(?i)"(?P<key>token|sessionId|screenName|playerName|clientId|userId|accountId)"\s*:\s*"[^"]+"'),
        lambda m: f'"{m.group("key")}": "<REDACTED>"',
    ),
    (
        re.compile(r'(?i)(AccountID|accountId|userId|playerId|clientId)"?\s*[:=]\s*"?[A-Za-z0-9\-]{6,}"?'),
        lambda m: f'{m.group(1)}:"<REDACTED>"',
    ),
    (re.compile(r'([A-Za-z]:\\Users\\)[^\\\r\n]+'), r'\1<REDACTED>'),
    (re.compile(r'(/Users/)[^/\r\n]+'), r'\1<REDACTED>'),
    (re.compile(r'(/home/)[^/\r\n]+'), r'\1<REDACTED>'),
    (
        re.compile(r'(?i)(DisplayName|playerName)"?\s*[:=]\s*"[^"]*"'),
        r'\1:"<REDACTED>"',
    ),
]


def scrub_raw_log(text: str) -> str:
    cleaned = text
    for pattern, replacement in _PATTERNS:
        cleaned = pattern.sub(replacement, cleaned)
    return cleaned
