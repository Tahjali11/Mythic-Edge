from __future__ import annotations

import json
import re
from typing import Any

_API_REQ_RE = re.compile(r"==>\s*(?P<name>[A-Za-z0-9_]+)")
_API_RESP_RE = re.compile(r"<==\s*(?P<name>[A-Za-z0-9_]+)")
_JSON_DECODER = json.JSONDecoder()


def _json_candidate_offsets(text: str) -> list[int]:
    return [idx for idx, ch in enumerate(text) if ch in "[{"]


def _api_name_match(body: str, pattern: re.Pattern[str], expected_name: str) -> bool:
    match = pattern.search(body)
    return bool(match and match.group("name") == expected_name)


def _normalized_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.isdigit():
            return int(stripped)
    return None


def find_json_value(text: str) -> Any | None:
    for idx in _json_candidate_offsets(text):
        try:
            value, _ = _JSON_DECODER.raw_decode(text[idx:])
            return value
        except json.JSONDecodeError:
            continue
    return None


def parse_json_from_body(body: str, context: str = "") -> dict[str, Any] | None:
    value = find_json_value(body)
    if value is None or not isinstance(value, dict):
        return None
    return value


def is_api_request(body: str, name: str) -> bool:
    return _api_name_match(body, _API_REQ_RE, name)


def is_api_response(body: str, name: str) -> bool:
    return _api_name_match(body, _API_RESP_RE, name)


def normalize_int_list(value: Any) -> list[int]:
    if not isinstance(value, list):
        return []
    out: list[int] = []
    for item in value:
        normalized = _normalized_int(item)
        if normalized is not None:
            out.append(normalized)
    return out
