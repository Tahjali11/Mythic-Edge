from __future__ import annotations

from typing import Any

from .. import api_common


def build_connect_resp_payload(message: dict[str, Any]) -> dict[str, Any]:
    connect_resp = _connect_resp_payload(message)
    deck_message = _deck_message_payload(connect_resp)

    return {
        "type": "connect_resp",
        "message_type": message.get("type", "GREMessageType_ConnectResp"),
        "msg_id": message.get("msgId", 0),
        "game_state_id": message.get("gameStateId", 0),
        "system_seat_ids": api_common.normalize_int_list(message.get("systemSeatIds")),
        "deck_cards": api_common.normalize_int_list(deck_message.get("deckCards")),
        "sideboard_cards": api_common.normalize_int_list(deck_message.get("sideboardCards")),
        "settings": _settings_payload(connect_resp),
        "raw_connect_resp": message,
    }


def _connect_resp_payload(message: dict[str, Any]) -> dict[str, Any]:
    connect_resp = message.get("connectResp")
    if isinstance(connect_resp, dict):
        return connect_resp
    return {}


def _deck_message_payload(connect_resp: dict[str, Any]) -> dict[str, Any]:
    deck_message = connect_resp.get("deckMessage")
    if isinstance(deck_message, dict):
        return deck_message
    return {}


def _settings_payload(connect_resp: dict[str, Any]) -> dict[str, Any]:
    settings = connect_resp.get("settings")
    if isinstance(settings, dict):
        return dict(settings)
    return {}
