from mythic_edge_parser.log.entry import (
    EntryHeader,
    LineBuffer,
    classify_line_header,
    is_single_line_header,
)


def test_classify_line_header_handles_utc_log_prefix() -> None:
    buffer = LineBuffer()
    entries = buffer.feed("[85] [UnityCrossThreadLogger]hello\n[0] DETAILED LOGS: ENABLED\n")
    entries.extend(buffer.flush())

    assert entries[0].header == EntryHeader.UNITY_CROSS_THREAD_LOGGER
    assert entries[0].body == "[UnityCrossThreadLogger]hello"
    assert entries[1].header == EntryHeader.METADATA
    assert entries[1].body == "DETAILED LOGS: ENABLED"
    assert classify_line_header("[UnityCrossThreadLogger]hello") == EntryHeader.UNITY_CROSS_THREAD_LOGGER
    assert classify_line_header("DETAILED LOGS: ENABLED") == EntryHeader.METADATA


def test_single_line_headers_emit_immediately_and_ignore_orphan_noise() -> None:
    buffer = LineBuffer()
    entries = buffer.feed(
        "[UnityCrossThreadLogger]Client.SceneChange {\"fromSceneName\":\"None\"}\n"
        "PreviousPlayBladeVisualState is being set to the same value as previously: Events\n"
        "[ConnectionManager] Reconnect result : Error\n"
        "Matchmaking: GRE connection lost, attempting reconnect\n"
    )
    entries.extend(buffer.flush())

    assert [entry.header for entry in entries] == [
        EntryHeader.UNITY_CROSS_THREAD_LOGGER,
        EntryHeader.CONNECTION_MANAGER,
        EntryHeader.MATCHMAKING,
    ]
    assert entries[0].body == '[UnityCrossThreadLogger]Client.SceneChange {"fromSceneName":"None"}'
    assert entries[1].body == "[ConnectionManager] Reconnect result : Error"
    assert entries[2].body == "Matchmaking: GRE connection lost, attempting reconnect"


def test_header_classification_knows_connection_manager_and_matchmaking() -> None:
    assert classify_line_header("[ConnectionManager] Reconnect result : Connected") == EntryHeader.CONNECTION_MANAGER
    assert classify_line_header("Matchmaking: GRE connection lost") == EntryHeader.MATCHMAKING
    assert is_single_line_header("[ConnectionManager] Reconnect result : Connected") is True
    assert is_single_line_header("Matchmaking: GRE connection lost") is True
    assert is_single_line_header("[UnityCrossThreadLogger]Client.SceneChange {}") is True
    assert is_single_line_header("[UnityCrossThreadLogger]3/11/2026 6:08:26 PM") is False


def test_truncation_marker_header_is_multiline_and_exact() -> None:
    marker_line = "[Message summarized - GREMessageType_GameStateMessage payload omitted]"

    assert classify_line_header(marker_line) == EntryHeader.TRUNCATION_MARKER
    assert classify_line_header(f"[85] {marker_line}") == EntryHeader.TRUNCATION_MARKER
    assert is_single_line_header(marker_line) is False
    assert classify_line_header("GameObject Count: 2") is None
    assert classify_line_header("This summary mentions GameObject Count: 2") is None
    assert classify_line_header("[Summary] GameObject Count: 2") == EntryHeader.UNKNOWN
