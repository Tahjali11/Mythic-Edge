from __future__ import annotations

from datetime import datetime
from typing import Any

from ...events import EventMetadata, GameEvent, GameResultEvent, GameStateEvent
from ...log.entry import LogEntry
from .. import api_common
from .connect_resp import build_connect_resp_payload
from .game_result import build_game_result_payload, is_game_over
from .game_state import build_game_state_payload

_MARKERS = (
    "greToClientEvent",
    "queuedGameStateMessage",
    "GREMessageType_GameStateMessage",
    "GREMessageType_ConnectResp",
    "GameStage_GameOver",
)


def try_parse(entry: LogEntry, timestamp: datetime | None) -> list[GameEvent]:
    body = entry.body
    if not any(marker in body for marker in _MARKERS):
        return []

    parsed = api_common.parse_json_from_body(body, "gre")
    if parsed is None:
        return []

    messages = _extract_gre_messages(parsed)
    if not messages:
        return []

    output: list[GameEvent] = []
    for message in messages:
        output.extend(_emit_message_events(message, body, timestamp))
    return output


def _extract_gre_messages(parsed: dict[str, Any]) -> list[dict[str, Any]]:
    event_root = parsed.get("greToClientEvent", parsed)
    messages = event_root.get("greToClientMessages") if isinstance(event_root, dict) else None
    if isinstance(messages, list):
        return [message for message in messages if isinstance(message, dict)]
    return [parsed]


def _emit_message_events(message: dict[str, Any], body: str, timestamp: datetime | None) -> list[GameEvent]:
    metadata = EventMetadata(timestamp, body.encode())
    events = _build_game_state_events(message, metadata)
    if events:
        return events

    connect_resp_event = _build_connect_resp_event(message, metadata)
    if connect_resp_event is None:
        return []
    return [connect_resp_event]


def _build_game_state_events(
    message: dict[str, Any],
    metadata: EventMetadata,
) -> list[GameEvent]:
    gsm = _message_game_state(message)
    if not isinstance(gsm, dict):
        return []

    game_state_payload = build_game_state_payload(message, gsm)
    events: list[GameEvent] = [GameStateEvent(metadata, game_state_payload)]
    if is_game_over(game_state_payload):
        events.append(GameResultEvent(metadata, build_game_result_payload(game_state_payload)))
    return events


def _build_connect_resp_event(
    message: dict[str, Any],
    metadata: EventMetadata,
) -> GameEvent | None:
    if not isinstance(message.get("connectResp"), dict):
        return None
    return GameStateEvent(metadata, build_connect_resp_payload(message))


def _message_game_state(message: dict[str, Any]) -> dict[str, Any] | None:
    gsm = message.get("gameStateMessage")
    if isinstance(gsm, dict):
        return gsm

    queued = message.get("queuedGameStateMessage")
    if isinstance(queued, dict):
        queued_gsm = queued.get("gameStateMessage")
        if isinstance(queued_gsm, dict):
            return queued_gsm
    return None
