from datetime import UTC, datetime

import pytest

from mythic_edge_parser.log.entry import EntryHeader, LogEntry
from mythic_edge_parser.parsers import (
    event_lifecycle,
    inventory,
    metadata,
    rank,
    session,
)

TS = datetime(2026, 5, 8, 12, 0, 0, tzinfo=UTC)


def test_metadata_parse_disabled_status() -> None:
    entry = LogEntry(EntryHeader.METADATA, "DETAILED LOGS: DISABLED")

    event = metadata.try_parse(entry, TS)

    assert event is not None
    assert event.kind == "DetailedLoggingStatus"
    assert event.payload == {"enabled": False}


def test_metadata_parse_enabled_status_with_whitespace() -> None:
    entry = LogEntry(EntryHeader.METADATA, "  DETAILED LOGS: ENABLED  ")

    event = metadata.try_parse(entry, TS)

    assert event is not None
    assert event.kind == "DetailedLoggingStatus"
    assert event.payload == {"enabled": True}


@pytest.mark.parametrize(
    ("body", "expected_type"),
    [
        ("[UnityCrossThreadLogger]==> EventJoin {\"id\":\"e1\"}", "event_join"),
        ("[UnityCrossThreadLogger]==> EventEnterPairing {\"id\":\"e2\"}", "event_enter_pairing"),
        ("[UnityCrossThreadLogger]==> EventClaimPrize {\"id\":\"e3\"}", "event_claim_prize"),
    ],
)
def test_event_lifecycle_parse_known_markers(body: str, expected_type: str) -> None:
    entry = LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, body)

    event = event_lifecycle.try_parse(entry, TS)

    assert event is not None
    assert event.kind == "EventLifecycle"
    assert event.payload["type"] == expected_type
    assert event.payload["raw_event_lifecycle"] == body


def test_event_lifecycle_parse_unknown_marker_returns_none() -> None:
    entry = LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, "[UnityCrossThreadLogger]==> EventSomethingElse")

    event = event_lifecycle.try_parse(entry, TS)

    assert event is None


def test_rank_parse_snapshot_payload() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]3/1/2026 9:00:00 AM\n'
        '<== RankGetCombinedRankInfo\n'
        '{"constructedClass":"Mythic","constructedLevel":1,"limitedClass":"Gold","limitedLevel":4,'
        '"constructedPercentile":99.1,"limitedPercentile":75.5}',
    )

    event = rank.try_parse(entry, TS)

    assert event is not None
    assert event.kind == "Rank"
    assert event.payload["type"] == "rank_snapshot"
    assert event.payload["constructed_class"] == "Mythic"
    assert event.payload["limited_class"] == "Gold"
    assert event.payload["constructed_percentile"] == 99.1
    assert event.payload["limited_percentile"] == 75.5


def test_rank_parse_sanitizes_container_fields_to_defaults() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]3/1/2026 9:00:00 AM\n'
        '<== RankGetCombinedRankInfo\n'
        '{"constructedClass":{"bad":1},"constructedLevel":[1],"limitedClass":"Gold","limitedLevel":{"bad":1},'
        '"constructedPercentile":{"bad":1},"limitedPercentile":[1]}',
    )

    event = rank.try_parse(entry, TS)

    assert event is not None
    assert event.payload["constructed_class"] == ""
    assert event.payload["constructed_level"] == ""
    assert event.payload["limited_class"] == "Gold"
    assert event.payload["limited_level"] == ""
    assert event.payload["constructed_percentile"] is None
    assert event.payload["limited_percentile"] is None


def test_rank_parse_non_matching_response_returns_none() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]3/1/2026 9:00:00 AM\n<== SomeOtherMethod\n{"constructedClass":"Mythic"}',
    )

    event = rank.try_parse(entry, TS)

    assert event is None


def test_inventory_parse_snapshot_payload() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]3/1/2026 9:00:00 AM\n'
        '<== StartHook(deck-uuid)\n'
        '{"InventoryInfo":{"Gold":1234,"Gems":55}}',
    )

    event = inventory.try_parse(entry, TS)

    assert event is not None
    assert event.kind == "Inventory"
    assert event.payload["type"] == "inventory_snapshot"
    assert event.payload["inventory"] == {"Gold": 1234, "Gems": 55}


def test_inventory_parse_missing_inventory_info_returns_none() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]3/1/2026 9:00:00 AM\n<== StartHook(deck-uuid)\n{"PlayerCards":{"123":4}}',
    )

    event = inventory.try_parse(entry, TS)

    assert event is None


def test_inventory_parse_requires_mapping_inventory_info() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]3/1/2026 9:00:00 AM\n<== StartHook(deck-uuid)\n{"InventoryInfo":["bad"]}',
    )

    event = inventory.try_parse(entry, TS)

    assert event is None


def test_session_parse_account_update() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]Updated account. DisplayName:Tahj, AccountID:abc-123",
    )

    event = session.try_parse(entry, TS)

    assert event is not None
    assert event.kind == "Session"
    assert event.payload == {
        "type": "session_account_update",
        "display_name": "Tahj",
        "account_id": "abc-123",
        "raw_session": entry.body,
    }


def test_session_parse_authenticate_response_lowercase_variant() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]3/1/2026 9:00:00 AM\n'
        '<== authenticateResponse\n'
        '{"displayName":"Tahj","accountId":"abc-123","screenName":"TahjScreen"}',
    )

    event = session.try_parse(entry, TS)

    assert event is not None
    assert event.kind == "Session"
    assert event.payload["type"] == "session_authenticated"
    assert event.payload["display_name"] == "Tahj"
    assert event.payload["account_id"] == "abc-123"
    assert event.payload["screen_name"] == "TahjScreen"


def test_session_parse_authenticate_response_sanitizes_non_string_fields() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        '[UnityCrossThreadLogger]3/1/2026 9:00:00 AM\n'
        '<== AuthenticateResponse\n'
        '{"displayName":{"bad":1},"accountId":["bad"],"screenName":" TahjScreen "}',
    )

    event = session.try_parse(entry, TS)

    assert event is not None
    assert event.payload["display_name"] == ""
    assert event.payload["account_id"] == ""
    assert event.payload["screen_name"] == "TahjScreen"


def test_session_parse_logout_word_boundary() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]User requested logout from the profile menu",
    )

    event = session.try_parse(entry, TS)

    assert event is not None
    assert event.kind == "Session"
    assert event.payload == {
        "type": "session_logout",
        "raw_session": entry.body,
    }


def test_session_parse_does_not_match_logout_substring() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]Received logoutToken refresh payload",
    )

    event = session.try_parse(entry, TS)

    assert event is None


def test_session_parse_account_update_trims_fields() -> None:
    entry = LogEntry(
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        "[UnityCrossThreadLogger]Updated account. DisplayName: Tahj , AccountID: abc-123 ",
    )

    event = session.try_parse(entry, TS)

    assert event is not None
    assert event.payload["display_name"] == "Tahj"
    assert event.payload["account_id"] == "abc-123"
