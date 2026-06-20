from pathlib import Path

import pytest

from mythic_edge_parser.app.utc_log_source_adapter import (
    UtcLogNormalizationResult,
    UtcLogSourceAccessError,
    describe_user_selected_utc_log_candidate,
    normalize_utc_log_text,
)
from mythic_edge_parser.log.entry import EntryHeader, LineBuffer

UNITY_HEADER = "[" + "Unity" + "Cross" + "Thread" + "Logger]"
CLIENT_GRE_HEADER = "[" + "Client " + "GRE]"
CONNECTION_HEADER = "[" + "Connection" + "Manager]"
DETAILED_LOGS = "DETAILED" + " LOGS:"
MATCHMAKING = "Match" + "making:"


def test_normalize_utc_log_text_strips_frame_prefixes_and_line_endings() -> None:
    result = normalize_utc_log_text(
        f"[85] {UNITY_HEADER}hello\r\n"
        "plain continuation\r"
        f"[0] {DETAILED_LOGS} ENABLED\n",
        source_label="synthetic.utc-log.case-1",
    )

    assert isinstance(result, UtcLogNormalizationResult)
    assert result.text == (
        f"{UNITY_HEADER}hello\n"
        "plain continuation\n"
        f"{DETAILED_LOGS} ENABLED\n"
    )
    assert result.source_label == "synthetic.utc-log.case-1"
    assert result.source_kind == "synthetic"
    assert result.warnings == ()
    assert result.stats.input_line_count == 3
    assert result.stats.output_line_count == 3
    assert result.stats.utc_frame_prefix_lines == 2
    assert result.stats.unchanged_lines == 1
    assert result.stats.dropped_lines == 0
    assert result.stats.degradation_status == "ok"


def test_normalize_utc_log_text_preserves_non_prefixed_content_order() -> None:
    source = (
        f"{CLIENT_GRE_HEADER} first line\n"
        "  [85] continuation is content, not a frame prefix\n"
        f"[1] {CONNECTION_HEADER} Reconnect result : Connected"
    )

    result = normalize_utc_log_text(source, source_label="synthetic.order")

    assert result.text == (
        f"{CLIENT_GRE_HEADER} first line\n"
        "  [85] continuation is content, not a frame prefix\n"
        f"{CONNECTION_HEADER} Reconnect result : Connected"
    )
    assert result.stats.input_line_count == 3
    assert result.stats.utc_frame_prefix_lines == 1
    assert result.stats.unchanged_lines == 2
    assert result.stats.dropped_lines == 0
    assert result.warnings == ("input_has_no_line_ending",)
    assert result.stats.degradation_status == "review"


def test_normalized_text_feeds_existing_line_buffer_path() -> None:
    result = normalize_utc_log_text(
        f"[44] {UNITY_HEADER}Client.SceneChange {{}}\n"
        f"[45] {CONNECTION_HEADER} Reconnect result : Connected\n",
        source_label="synthetic.line-buffer",
    )
    buffer = LineBuffer()

    entries = buffer.feed(result.text)
    entries.extend(buffer.flush())

    assert [entry.header for entry in entries] == [
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        EntryHeader.CONNECTION_MANAGER,
    ]
    assert entries[0].body == f"{UNITY_HEADER}Client.SceneChange {{}}"
    assert entries[1].body == f"{CONNECTION_HEADER} Reconnect result : Connected"


def test_adapter_returns_text_not_parser_events() -> None:
    result = normalize_utc_log_text(
        f"[1] {MATCHMAKING} GRE connection lost, attempting reconnect\n",
        source_label="synthetic.text-only",
    )

    assert result.text == f"{MATCHMAKING} GRE connection lost, attempting reconnect\n"
    assert not hasattr(result, "events")
    assert not hasattr(result, "entries")


def test_malformed_synthetic_input_warns_without_dropping_content() -> None:
    result = normalize_utc_log_text(
        "[1] [SomeHeader] bad\ufffdvalue\x00\n",
        source_label="synthetic.malformed",
    )

    assert result.text == "[SomeHeader] bad\ufffdvalue\x00\n"
    assert result.warnings == (
        "replacement_characters_present",
        "nul_characters_present",
    )
    assert result.stats.replacement_character_count == 1
    assert result.stats.degradation_status == "degraded"
    assert result.stats.dropped_lines == 0


def test_empty_synthetic_input_is_review_not_failure() -> None:
    result = normalize_utc_log_text("", source_label="synthetic.empty")

    assert result.text == ""
    assert result.stats.input_line_count == 0
    assert result.stats.output_line_count == 0
    assert result.stats.degradation_status == "review"
    assert result.warnings == ("empty_input",)


def test_user_selected_local_normalization_fails_closed_without_path_leak() -> None:
    private_label = "/" + "Users/example/Library/Logs/UTC_Log.txt"

    with pytest.raises(UtcLogSourceAccessError) as excinfo:
        normalize_utc_log_text(
            f"[1] {DETAILED_LOGS} ENABLED\n",
            source_label=private_label,
            source_kind="user_selected_local",
        )

    message = str(excinfo.value)
    assert "not authorized" not in message
    assert private_label not in message
    assert "source_label must be symbolic" in message


def test_user_selected_candidate_discovery_fails_closed_without_path_leak() -> None:
    private_path = Path("/" + "Users/example/Library/Logs/UTC_Log.txt")

    with pytest.raises(UtcLogSourceAccessError) as excinfo:
        describe_user_selected_utc_log_candidate(private_path)

    message = str(excinfo.value)
    assert "private/local UTC_Log candidate inspection is not authorized" == message
    assert str(private_path) not in message
