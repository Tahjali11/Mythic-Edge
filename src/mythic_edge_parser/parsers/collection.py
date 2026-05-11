from __future__ import annotations

from datetime import datetime
from typing import Any

from ..events import CollectionEvent, DeckCollectionEvent, EventMetadata, GameEvent
from ..log.entry import LogEntry
from . import api_common

METHOD = "StartHook"
PLAYER_CARDS_FIELD = "PlayerCards"
DECK_SUMMARIES_FIELD = "DeckSummaries"
DECKS_FIELD = "Decks"


def try_parse(entry: LogEntry, timestamp: datetime | None) -> list[GameEvent] | GameEvent | None:
    body = entry.body
    parsed = _start_hook_payload(body)
    if parsed is None:
        return None

    events: list[GameEvent] = []
    collection_payload = _build_collection_payload(parsed)
    if collection_payload is not None:
        events.append(CollectionEvent(EventMetadata(timestamp, body.encode()), collection_payload))

    deck_payload = _build_deck_collection_payload(parsed)
    if deck_payload is not None:
        events.append(DeckCollectionEvent(EventMetadata(timestamp, body.encode()), deck_payload))

    if not events:
        return None
    if len(events) == 1:
        return events[0]
    return events


def _start_hook_payload(body: str) -> dict[str, Any] | None:
    if not api_common.is_api_response(body, METHOD):
        return None
    return api_common.parse_json_from_body(body, "StartHook collection")


def _mapping_field(parsed: dict[str, Any], field: str) -> dict[str, Any] | None:
    value = parsed.get(field)
    if isinstance(value, dict):
        return value
    return None


def _list_field(parsed: dict[str, Any], field: str) -> list[Any] | None:
    value = parsed.get(field)
    if isinstance(value, list):
        return value
    return None


def _build_collection_payload(parsed: dict[str, Any]) -> dict[str, Any] | None:
    player_cards = _mapping_field(parsed, PLAYER_CARDS_FIELD)
    if player_cards is None:
        return None
    return {
        "type": "collection_snapshot",
        "player_cards": player_cards,
        "raw_start_hook": parsed,
    }


def _build_deck_collection_payload(parsed: dict[str, Any]) -> dict[str, Any] | None:
    deck_summaries = _list_field(parsed, DECK_SUMMARIES_FIELD)
    deck_map = _mapping_field(parsed, DECKS_FIELD)
    if deck_summaries is None or deck_map is None:
        return None
    correlated_decks = _correlate_decks(deck_summaries, deck_map)
    if not correlated_decks:
        return None
    return {
        "type": "deck_collection_snapshot",
        "decks": correlated_decks,
        "raw_start_hook": parsed,
    }


def _correlate_decks(deck_summaries: list[Any], deck_map: dict[str, Any]) -> dict[str, Any]:
    correlated: dict[str, Any] = {}
    for summary in deck_summaries:
        deck_entry = _correlated_deck_payload(summary, deck_map)
        if deck_entry is None:
            continue
        deck_id, enriched = deck_entry
        correlated[deck_id] = enriched
    return correlated


def _correlated_deck_payload(
    summary: Any,
    deck_map: dict[str, Any],
) -> tuple[str, dict[str, Any]] | None:
    if not isinstance(summary, dict):
        return None
    deck_id = summary.get("DeckId")
    if not isinstance(deck_id, str):
        return None
    deck_payload = deck_map.get(deck_id)
    if not isinstance(deck_payload, dict):
        return None
    enriched = dict(summary)
    enriched["list"] = deck_payload
    return deck_id, enriched
