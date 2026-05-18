from datetime import UTC, datetime

from mythic_edge_parser import router
from mythic_edge_parser.events import BaseEvent, CollectionEvent, DetailedLoggingStatusEvent, EventMetadata
from mythic_edge_parser.log.entry import EntryHeader, LogEntry

DISPATCH_MODULE_NAMES = (
    "metadata",
    "gre",
    "truncation",
    "client_actions",
    "match_state",
    "session",
    "event_lifecycle",
    "draft_bot",
    "draft_human",
    "rank",
    "collection",
    "inventory",
    "connection_state",
    "connection_close",
    "connection_error",
)


def _make_entry(body: str, header: EntryHeader = EntryHeader.UNKNOWN) -> LogEntry:
    return LogEntry(header=header, body=body)


def _make_event(event_cls: type[BaseEvent] = DetailedLoggingStatusEvent) -> BaseEvent:
    return event_cls(
        metadata=EventMetadata(timestamp=None, raw_bytes=b"router-test"),
        payload={},
    )


def test_extract_timestamp_returns_utc_datetime_from_first_line() -> None:
    body = "[UnityCrossThreadLogger]5/8/2026 1:02:03 pm Some event\nSecond line"

    result = router.extract_timestamp(body)

    assert result == datetime(2026, 5, 8, 13, 2, 3, tzinfo=UTC)


def test_extract_timestamp_ignores_second_line_when_first_line_has_no_timestamp() -> None:
    body = "No timestamp here\n[UnityCrossThreadLogger]5/8/2026 1:02:03 PM Hidden timestamp"

    result = router.extract_timestamp(body)

    assert result is None


def test_extract_timestamp_returns_none_for_invalid_timestamp_values() -> None:
    body = "[UnityCrossThreadLogger]13/40/2026 25:99:99 PM Broken timestamp"

    result = router.extract_timestamp(body)

    assert result is None


def test_route_updates_routed_stats_for_successful_dispatch(monkeypatch) -> None:
    expected_event = _make_event()
    test_router = router.Router()

    monkeypatch.setattr(router, "dispatch_to_parsers", lambda entry, timestamp: [expected_event])

    result = test_router.route(_make_entry("[UnityCrossThreadLogger]5/8/2026 1:02:03 PM Event"))

    stats = test_router.stats
    assert result == [expected_event]
    assert stats.routed == 1
    assert stats.unknown == 0
    assert stats.timestamp_missing == 0
    assert stats.timestamp_parse_failure == 0
    assert stats.timestamp_anomalies == 0


def test_route_updates_unknown_and_timestamp_missing_for_unrouted_entry(monkeypatch) -> None:
    test_router = router.Router()

    monkeypatch.setattr(router, "dispatch_to_parsers", lambda entry, timestamp: [])

    result = test_router.route(_make_entry("No timestamp and no parser match"))

    stats = test_router.stats
    assert result == []
    assert stats.routed == 0
    assert stats.unknown == 1
    assert stats.timestamp_missing == 1
    assert stats.timestamp_parse_failure == 0
    assert stats.timestamp_anomalies == 1


def test_route_updates_timestamp_parse_failure_for_invalid_timestamp(monkeypatch) -> None:
    expected_event = _make_event()
    test_router = router.Router()

    monkeypatch.setattr(router, "dispatch_to_parsers", lambda entry, timestamp: [expected_event])

    result = test_router.route(_make_entry("[UnityCrossThreadLogger]13/40/2026 25:99:99 PM Broken timestamp"))

    stats = test_router.stats
    assert result == [expected_event]
    assert stats.routed == 1
    assert stats.unknown == 0
    assert stats.timestamp_missing == 0
    assert stats.timestamp_parse_failure == 1
    assert stats.timestamp_anomalies == 1


def test_route_counts_truncation_marker_as_routed_with_valid_timestamp() -> None:
    test_router = router.Router()

    result = test_router.route(
        _make_entry(
            "[Message summarized]5/8/2026 1:02:03 PM GREMessageType_GameStateMessage payload omitted\n"
            "GameObject Count: 1",
            header=EntryHeader.TRUNCATION_MARKER,
        )
    )

    stats = test_router.stats
    assert [event.kind for event in result] == ["Truncation"]
    assert result[0].metadata.timestamp == datetime(2026, 5, 8, 13, 2, 3, tzinfo=UTC)
    assert stats.routed == 1
    assert stats.unknown == 0
    assert stats.timestamp_missing == 0
    assert stats.timestamp_parse_failure == 0


def test_route_counts_truncation_marker_timestamp_anomalies_without_unknown() -> None:
    missing_timestamp_router = router.Router()
    malformed_timestamp_router = router.Router()

    missing_timestamp_router.route(
        _make_entry(
            "[Message summarized - GREMessageType_GameStateMessage payload omitted]",
            header=EntryHeader.TRUNCATION_MARKER,
        )
    )
    malformed_timestamp_router.route(
        _make_entry(
            "[Message summarized]13/40/2026 25:99:99 PM GREMessageType_GameStateMessage payload omitted",
            header=EntryHeader.TRUNCATION_MARKER,
        )
    )

    missing_stats = missing_timestamp_router.stats
    malformed_stats = malformed_timestamp_router.stats
    assert missing_stats.routed == 1
    assert missing_stats.unknown == 0
    assert missing_stats.timestamp_missing == 1
    assert malformed_stats.routed == 1
    assert malformed_stats.unknown == 0
    assert malformed_stats.timestamp_parse_failure == 1


def test_stats_property_returns_snapshot_copy() -> None:
    test_router = router.Router()

    stats_snapshot = test_router.stats
    stats_snapshot.routed = 999

    assert test_router.stats.routed == 0


def test_dispatch_to_parsers_uses_metadata_bucket_only(monkeypatch) -> None:
    call_order: list[str] = []
    expected_event = _make_event()

    for module_name in DISPATCH_MODULE_NAMES:
        parser_module = getattr(router.parsers, module_name)

        def _make_parser(name: str):
            def _parser(entry, timestamp):
                call_order.append(name)
                if name == "metadata":
                    return expected_event
                return None

            return _parser

        monkeypatch.setattr(parser_module, "try_parse", _make_parser(module_name))

    result = router.dispatch_to_parsers(_make_entry("body", header=EntryHeader.METADATA), None)

    assert result == [expected_event]
    assert call_order == ["metadata"]


def test_dispatch_to_parsers_uses_truncation_bucket_only(monkeypatch) -> None:
    call_order: list[str] = []
    expected_event = _make_event()

    for module_name in DISPATCH_MODULE_NAMES:
        parser_module = getattr(router.parsers, module_name)

        def _make_parser(name: str):
            def _parser(entry, timestamp):
                call_order.append(name)
                if name == "truncation":
                    return expected_event
                return None

            return _parser

        monkeypatch.setattr(parser_module, "try_parse", _make_parser(module_name))

    result = router.dispatch_to_parsers(_make_entry("body", header=EntryHeader.TRUNCATION_MARKER), None)

    assert result == [expected_event]
    assert call_order == ["truncation"]


def test_dispatch_to_parsers_uses_unknown_header_fallback_order(monkeypatch) -> None:
    call_order: list[str] = []
    expected_event = _make_event()

    for module_name in DISPATCH_MODULE_NAMES:
        parser_module = getattr(router.parsers, module_name)

        def _make_parser(name: str):
            def _parser(entry, timestamp):
                call_order.append(name)
                if name == "client_actions":
                    return expected_event
                return None

            return _parser

        monkeypatch.setattr(parser_module, "try_parse", _make_parser(module_name))

    result = router.dispatch_to_parsers(_make_entry("body"), None)

    assert result == [expected_event]
    assert call_order == ["gre", "client_actions"]


def test_dispatch_to_parsers_uses_unknown_header_lifecycle_position(monkeypatch) -> None:
    call_order: list[str] = []
    expected_event = _make_event()

    for module_name in DISPATCH_MODULE_NAMES:
        parser_module = getattr(router.parsers, module_name)

        def _make_parser(name: str):
            def _parser(entry, timestamp):
                call_order.append(name)
                if name == "rank":
                    return expected_event
                return None

            return _parser

        monkeypatch.setattr(parser_module, "try_parse", _make_parser(module_name))

    result = router.dispatch_to_parsers(_make_entry("body", header=EntryHeader.UNKNOWN), None)

    assert result == [expected_event]
    assert call_order == [
        "gre",
        "client_actions",
        "match_state",
        "session",
        "event_lifecycle",
        "draft_bot",
        "draft_human",
        "rank",
    ]


def test_dispatch_to_parsers_uses_unity_bucket_order(monkeypatch) -> None:
    call_order: list[str] = []
    expected_event = _make_event()

    for module_name in DISPATCH_MODULE_NAMES:
        parser_module = getattr(router.parsers, module_name)

        def _make_parser(name: str):
            def _parser(entry, timestamp):
                call_order.append(name)
                if name == "connection_error":
                    return expected_event
                return None

            return _parser

        monkeypatch.setattr(parser_module, "try_parse", _make_parser(module_name))

    result = router.dispatch_to_parsers(
        _make_entry("body", header=EntryHeader.UNITY_CROSS_THREAD_LOGGER),
        None,
    )

    assert result == [expected_event]
    assert call_order == [
        "gre",
        "client_actions",
        "match_state",
        "session",
        "event_lifecycle",
        "draft_bot",
        "draft_human",
        "rank",
        "collection",
        "inventory",
        "connection_state",
        "connection_close",
        "connection_error",
    ]


def test_dispatch_to_parsers_stops_after_lifecycle_event(monkeypatch) -> None:
    call_order: list[str] = []
    expected_event = _make_event()

    for module_name in DISPATCH_MODULE_NAMES:
        parser_module = getattr(router.parsers, module_name)

        def _make_parser(name: str):
            def _parser(entry, timestamp):
                call_order.append(name)
                if name == "event_lifecycle":
                    return expected_event
                return None

            return _parser

        monkeypatch.setattr(parser_module, "try_parse", _make_parser(module_name))

    result = router.dispatch_to_parsers(
        _make_entry("body", header=EntryHeader.UNITY_CROSS_THREAD_LOGGER),
        None,
    )

    assert result == [expected_event]
    assert call_order == [
        "gre",
        "client_actions",
        "match_state",
        "session",
        "event_lifecycle",
    ]


def test_dispatch_to_parsers_uses_unity_bucket_gre_before_connection_parsers(monkeypatch) -> None:
    call_order: list[str] = []
    expected_event = _make_event()

    for module_name in DISPATCH_MODULE_NAMES:
        parser_module = getattr(router.parsers, module_name)

        def _make_parser(name: str):
            def _parser(entry, timestamp):
                call_order.append(name)
                if name == "gre":
                    return expected_event
                return None

            return _parser

        monkeypatch.setattr(parser_module, "try_parse", _make_parser(module_name))

    result = router.dispatch_to_parsers(
        _make_entry("body", header=EntryHeader.UNITY_CROSS_THREAD_LOGGER),
        None,
    )

    assert result == [expected_event]
    assert call_order == ["gre"]


def test_dispatch_to_parsers_preserves_list_results_inside_unknown_bucket(monkeypatch) -> None:
    expected_events = [_make_event(), _make_event(CollectionEvent)]
    call_order: list[str] = []

    for module_name in DISPATCH_MODULE_NAMES:
        parser_module = getattr(router.parsers, module_name)

        def _make_parser(name: str):
            def _parser(entry, timestamp):
                call_order.append(name)
                if name == "gre":
                    return expected_events
                return None

            return _parser

        monkeypatch.setattr(parser_module, "try_parse", _make_parser(module_name))

    result = router.dispatch_to_parsers(_make_entry("body", header=EntryHeader.UNKNOWN), None)

    assert result is expected_events
    assert call_order == ["gre"]
