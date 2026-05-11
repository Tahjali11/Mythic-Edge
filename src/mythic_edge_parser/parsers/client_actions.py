from __future__ import annotations

from datetime import datetime
from typing import Any, Callable

from ..events import ClientActionEvent, EventMetadata, GameEvent
from ..log.entry import LogEntry
from . import api_common

CLIENT_TO_GRE_MARKER = "ClientToGREMessage"
CLIENT_TO_GRE_UI_MARKER = "ClientToGREUIMessage"
ClientActionPayloadBuilder = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]
MULLIGAN_DECISION_MAP = {
    "MulliganOption_Mulligan": "mulligan",
    "MulliganOption_AcceptHand": "keep",
}


def try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None:
    body = entry.body
    message_channel = _classify_message_channel(body)
    if message_channel is None:
        return None
    parsed = api_common.parse_json_from_body(body, "ClientToGREMessage")
    if parsed is None:
        return None
    if message_channel == "ui":
        return ClientActionEvent(
            EventMetadata(timestamp, body.encode()),
            {
                "type": "client_ui_message",
                "raw_client_action": parsed,
            },
        )
    inner = _extract_inner_payload(parsed)
    if inner is None:
        return None
    payload = _build_client_action_payload(inner, parsed)
    return ClientActionEvent(EventMetadata(timestamp, body.encode()), payload)


def _classify_message_channel(body: str) -> str | None:
    if CLIENT_TO_GRE_UI_MARKER in body:
        return "ui"
    if CLIENT_TO_GRE_MARKER in body:
        return "gre"
    return None


def _extract_inner_payload(parsed: dict[str, Any]) -> dict[str, Any] | None:
    payload = parsed.get("payload")
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        value = api_common.find_json_value(payload)
        if isinstance(value, dict):
            return value
    return None


def _dict_payload(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _request_context(inner: dict[str, Any], envelope: dict[str, Any]) -> dict[str, Any]:
    return {
        "game_state_id": inner.get("gameStateId", 0),
        "resp_id": inner.get("respId", 0),
        "request_id": envelope.get("requestId", 0),
        "raw_client_action": envelope,
    }


def _normalized_message_type(inner: dict[str, Any]) -> str:
    return str(inner.get("type", "") or "").strip()


def _build_client_action_payload(inner: dict[str, Any], envelope: dict[str, Any]) -> dict[str, Any]:
    message_type = _normalized_message_type(inner)
    builder = _CLIENT_ACTION_PAYLOAD_BUILDERS.get(message_type)
    if builder is None:
        return _build_generic_client_action(message_type, envelope)
    return builder(inner, envelope)


def _build_generic_client_action(message_type: str, envelope: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "generic_client_action",
        "message_type": message_type,
        "raw_client_action": envelope,
    }


def _build_mulligan(inner: dict[str, Any], envelope: dict[str, Any]) -> dict[str, Any]:
    mulligan_payload = _dict_payload(inner.get("mulliganResp"))
    decision_raw = mulligan_payload.get("decision") or ""
    payload = {
        "type": "mulligan_resp",
        "decision": MULLIGAN_DECISION_MAP.get(decision_raw, decision_raw),
    }
    payload.update(_request_context(inner, envelope))
    return payload


def _build_select_n(inner: dict[str, Any], envelope: dict[str, Any]) -> dict[str, Any]:
    select_payload = _dict_payload(inner.get("selectNResp"))
    payload = {
        "type": "select_n_resp",
        "selected_option_ids": api_common.normalize_int_list(select_payload.get("selectedOptionIds")),
        "selected_object_ids": api_common.normalize_int_list(select_payload.get("selectedObjectIds")),
    }
    payload.update(_request_context(inner, envelope))
    return payload


def _submit_deck_lists(submit_payload: dict[str, Any]) -> tuple[list[int], list[int]]:
    nested_deck = _dict_payload(submit_payload.get("deck"))
    deck_cards = api_common.normalize_int_list(
        submit_payload.get("deckCards") or nested_deck.get("deckCards") or submit_payload.get("deck") or []
    )
    sideboard_cards = api_common.normalize_int_list(
        submit_payload.get("sideboardCards")
        or nested_deck.get("sideboardCards")
        or submit_payload.get("sideboard")
        or []
    )
    return deck_cards, sideboard_cards


def _build_submit_deck(inner: dict[str, Any], envelope: dict[str, Any]) -> dict[str, Any]:
    submit_payload = _dict_payload(inner.get("submitDeckResp"))
    deck_cards, sideboard_cards = _submit_deck_lists(submit_payload)
    payload = {
        "type": "submit_deck_resp",
        "deck_cards": deck_cards,
        "sideboard_cards": sideboard_cards,
    }
    payload.update(_request_context(inner, envelope))
    return payload


_CLIENT_ACTION_PAYLOAD_BUILDERS: dict[str, ClientActionPayloadBuilder] = {
    "ClientMessageType_MulliganResp": _build_mulligan,
    "ClientMessageType_SelectNResp": _build_select_n,
    "ClientMessageType_SubmitDeckResp": _build_submit_deck,
}
