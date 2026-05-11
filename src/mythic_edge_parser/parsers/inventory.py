from __future__ import annotations

from datetime import datetime
from typing import Any

from ..events import EventMetadata, GameEvent, InventoryEvent
from ..log.entry import LogEntry
from . import api_common

METHOD = "StartHook"
FIELD = "InventoryInfo"


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    body = entry.body
    parsed = _start_hook_payload(body)
    if parsed is None:
        return None
    payload = _build_inventory_payload(parsed)
    if payload is None:
        return None
    return InventoryEvent(EventMetadata(timestamp, body.encode()), payload)


def _start_hook_payload(body: str) -> dict[str, Any] | None:
    if not api_common.is_api_response(body, METHOD):
        return None
    return api_common.parse_json_from_body(body, "StartHook inventory")


def _build_inventory_payload(parsed: dict[str, Any]) -> dict[str, Any] | None:
    inventory = parsed.get(FIELD)
    if not isinstance(inventory, dict):
        return None
    return {
        "type": "inventory_snapshot",
        "inventory": inventory,
        "raw_start_hook": parsed,
    }
