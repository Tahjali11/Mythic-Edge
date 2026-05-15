from collections.abc import Sequence
from datetime import UTC, datetime

from mythic_edge_parser.events import BaseEvent
from mythic_edge_parser.log.entry import EntryHeader, LogEntry
from mythic_edge_parser.parsers import collection

TS = datetime(2026, 5, 5, 12, 0, 0, tzinfo=UTC)


def _expect_one_event(value: BaseEvent | Sequence[BaseEvent] | None) -> BaseEvent:
    assert value is not None
    if isinstance(value, Sequence):
        assert len(value) == 1
        return value[0]
    return value


def test_collection_parse_player_cards_only() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]2/22/2026 11:59:51 AM\n<== StartHook(deck-uuid)\n{"PlayerCards":{"123":4}}',
    )
    event = _expect_one_event(collection.try_parse(entry, TS))
    assert event.kind == "Collection"
    assert event.payload["type"] == "collection_snapshot"
    assert event.payload["player_cards"] == {"123": 4}


def test_collection_parse_emits_player_cards_and_deck_collection() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]2/22/2026 11:59:51 AM\n'
        '<== StartHook(deck-uuid)\n'
        '{"PlayerCards":{"123":4},'
        '"DeckSummaries":[{"DeckId":"deck-1","Name":"Reanimator"}],'
        '"Decks":{"deck-1":{"MainDeck":[{"cardId":1,"quantity":4}]}}}',
    )
    events = collection.try_parse(entry, TS)
    assert isinstance(events, list)
    assert [event.kind for event in events] == ["Collection", "DeckCollection"]
    assert events[1].payload["type"] == "deck_collection_snapshot"
    assert events[1].payload["decks"]["deck-1"]["Name"] == "Reanimator"
    assert events[1].payload["decks"]["deck-1"]["list"]["MainDeck"][0]["cardId"] == 1


def test_collection_parse_skips_orphaned_deck_summaries() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]2/22/2026 11:59:51 AM\n'
        '<== StartHook(deck-uuid)\n'
        '{"DeckSummaries":[{"DeckId":"deck-1","Name":"Missing"},{"DeckId":"deck-2","Name":"Present"}],'
        '"Decks":{"deck-2":{"MainDeck":[{"cardId":2,"quantity":3}]}}}',
    )
    event = _expect_one_event(collection.try_parse(entry, TS))
    assert event.kind == "DeckCollection"
    assert "deck-1" not in event.payload["decks"]
    assert event.payload["decks"]["deck-2"]["list"]["MainDeck"][0]["quantity"] == 3


def test_collection_parse_real_start_hook_shape_emits_deck_collection() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]5/7/2026 11:45:35 PM\n'
        '<== StartHook(real-start-hook)\n'
        '{"InventoryInfo":{"Gold":12750},'
        '"DeckSummaries":[{"DeckId":"deck-1","Name":"Orzhov Skeletons",'
        '"Attributes":[{"name":"Format","value":"Standard"}]}],'
        '"Decks":{"deck-1":{"MainDeck":[{"cardId":1001,"quantity":2}],"Sideboard":[],"Companions":[]}}}',
    )

    event = _expect_one_event(collection.try_parse(entry, TS))
    assert event.kind == "DeckCollection"
    assert event.payload["decks"]["deck-1"]["Name"] == "Orzhov Skeletons"
    assert event.payload["decks"]["deck-1"]["list"]["MainDeck"][0]["cardId"] == 1001


def test_collection_parse_requires_mapping_player_cards() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]2/22/2026 11:59:51 AM\n<== StartHook(collection-shape)\n{"PlayerCards":[1,2,3]}',
    )

    event = collection.try_parse(entry, TS)

    assert event is None


def test_collection_parse_skips_empty_correlated_decks() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]2/22/2026 11:59:51 AM\n'
        '<== StartHook(deck-uuid)\n'
        '{"DeckSummaries":[{"DeckId":"deck-1","Name":"Missing"}],"Decks":{"deck-2":{"MainDeck":[{"cardId":2,"quantity":3}]}}}',
    )

    event = collection.try_parse(entry, TS)

    assert event is None


def test_collection_parse_skips_malformed_deck_summary_entries() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]2/22/2026 11:59:51 AM\n'
        '<== StartHook(deck-uuid)\n'
        '{"DeckSummaries":["bad",{"DeckId":9},{"DeckId":"deck-1","Name":"Playable"}],'
        '"Decks":{"deck-1":{"MainDeck":[{"cardId":7,"quantity":2}]},"deck-2":"bad"}}',
    )

    event = _expect_one_event(collection.try_parse(entry, TS))
    assert event.kind == "DeckCollection"
    assert list(event.payload["decks"]) == ["deck-1"]
    assert event.payload["decks"]["deck-1"]["Name"] == "Playable"
