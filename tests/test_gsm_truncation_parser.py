from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import get_args

from mythic_edge_parser.app.transforms import include_event, summarize, to_sheet_rows
from mythic_edge_parser.events import GameEvent, PerformanceClass, TruncationEvent
from mythic_edge_parser.log.entry import EntryHeader, LogEntry
from mythic_edge_parser.parsers import gre, truncation

TS = datetime(2026, 5, 18, 12, 0, 0, tzinfo=UTC)
MARKER_LINE = "[Message summarized - GREMessageType_GameStateMessage payload omitted]"


def _entry(body: str, header: EntryHeader = EntryHeader.TRUNCATION_MARKER) -> LogEntry:
    return LogEntry(header, body)


def test_truncation_event_is_first_class_interactive_dispatch_event() -> None:
    assert TruncationEvent.kind == "Truncation"
    assert TruncationEvent.performance_class == PerformanceClass.INTERACTIVE_DISPATCH
    assert TruncationEvent in get_args(GameEvent)


def test_try_parse_emits_data_loss_event_for_sanitized_gsm_marker_block() -> None:
    body = f"{MARKER_LINE}\nGameObject Count: 12\nAnnotation Count: 3"

    event = truncation.try_parse(_entry(body), TS)

    assert isinstance(event, TruncationEvent)
    assert event.kind == "Truncation"
    assert event.metadata.timestamp == TS
    assert event.metadata.raw_bytes == body.encode()
    assert event.metadata.raw_bytes_hash == hashlib.sha256(body.encode()).hexdigest()
    assert event.payload == {
        "type": "game_state_message_truncation",
        "marker_family": "game_state_message_truncation",
        "affected_event_family": "GameState",
        "affected_message_type": "GREMessageType_GameStateMessage",
        "data_loss": True,
        "recoverable": False,
        "parser_confidence": "explicit_marker",
        "value_source": "observed",
        "confidence": "high",
        "finality": "live",
        "drift_flag": "missing_expected_payload_path",
        "source_header": "TruncationMarker",
        "game_object_count": 12,
        "annotation_count": 3,
        "raw_marker_summary": "game_state_message_truncation; game_object_count=12; annotation_count=3",
    }
    assert "game_objects" not in event.payload
    assert "annotations" not in event.payload
    assert "raw_game_state" not in event.payload


def test_try_parse_keeps_missing_zero_and_malformed_counts_as_evidence_only() -> None:
    missing = truncation.try_parse(_entry(MARKER_LINE), TS)
    zero = truncation.try_parse(_entry(f"{MARKER_LINE}\nGameObject Count: 0\nAnnotation Count: 0"), TS)
    malformed = truncation.try_parse(
        _entry(f"{MARKER_LINE}\nGameObject Count: -1\nAnnotation Count: many"),
        TS,
    )
    first_safe = truncation.try_parse(
        _entry(f"{MARKER_LINE}\nGameObject Count: -2\nGameObject Count: 5"),
        TS,
    )

    assert missing is not None
    assert missing.payload["game_object_count"] is None
    assert missing.payload["annotation_count"] is None
    assert zero is not None
    assert zero.payload["game_object_count"] == 0
    assert zero.payload["annotation_count"] == 0
    assert malformed is not None
    assert malformed.payload["game_object_count"] is None
    assert malformed.payload["annotation_count"] is None
    assert first_safe is not None
    assert first_safe.payload["game_object_count"] == 5


def test_try_parse_rejects_count_only_and_nearby_non_marker_text() -> None:
    assert truncation.try_parse(_entry("GameObject Count: 2\nAnnotation Count: 1"), TS) is None
    assert truncation.try_parse(_entry("summary GameObject Count: 2"), TS) is None
    assert truncation.try_parse(_entry("[Summary] GameObject Count: 2", EntryHeader.UNKNOWN), TS) is None


def test_try_parse_handles_non_string_body_without_raising() -> None:
    assert truncation.try_parse(LogEntry(EntryHeader.TRUNCATION_MARKER, None), TS) is None  # type: ignore[arg-type]


def test_truncation_marker_is_not_gre_game_state_or_result() -> None:
    body = f"{MARKER_LINE}\nGameObject Count: 4\nAnnotation Count: 2"

    assert gre.try_parse(_entry(body), TS) == []
    event = truncation.try_parse(_entry(body), TS)

    assert isinstance(event, TruncationEvent)
    assert event.kind != "GameState"
    assert event.kind != "GameResult"


def test_transforms_keep_truncation_event_without_workbook_rows() -> None:
    event = truncation.try_parse(_entry(f"{MARKER_LINE}\nGameObject Count: 4"), TS)

    assert event is not None
    assert include_event(event) is True
    assert to_sheet_rows(event) == []
    assert summarize(event) == (
        "Truncation affected=GREMessageType_GameStateMessage data_loss=True recoverable=False "
        "game_object_count=4 annotation_count=None"
    )
