from datetime import UTC, datetime

from mythic_edge_parser.events import ClientActionEvent, EventMetadata


def test_event_metadata_empty_uses_empty_raw_bytes() -> None:
    timestamp = datetime(2026, 5, 8, 12, 0, 0, tzinfo=UTC)

    metadata = EventMetadata.empty(timestamp=timestamp)

    assert metadata.timestamp == timestamp
    assert metadata.raw_bytes == b""
    assert metadata.raw_bytes_hash


def test_event_payload_is_snapshotted_at_creation() -> None:
    source_payload = {"type": "submit_deck_resp", "deck_cards": [1, 2, 3]}

    event = ClientActionEvent(EventMetadata.empty(), source_payload)
    source_payload["type"] = "mutated_after_event_creation"

    assert event.payload["type"] == "submit_deck_resp"
    assert event.payload_copy() == {"type": "submit_deck_resp", "deck_cards": [1, 2, 3]}
