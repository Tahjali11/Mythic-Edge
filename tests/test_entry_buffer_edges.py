from mythic_edge_parser.log.entry import EntryHeader, LineBuffer


def test_partial_single_line_header_waits_for_newline_before_emitting() -> None:
    buffer = LineBuffer()

    first = buffer.feed("[ConnectionManager] Reconnect result")
    second = buffer.feed(" : Connected\n")

    assert first == []
    assert len(second) == 1
    assert second[0].header == EntryHeader.CONNECTION_MANAGER
    assert second[0].body == "[ConnectionManager] Reconnect result : Connected"


def test_flush_finalizes_partial_single_line_header_at_end_of_stream() -> None:
    buffer = LineBuffer()

    first = buffer.feed("DETAILED LOGS: ENABLE")
    second = buffer.flush()

    assert first == []
    assert len(second) == 1
    assert second[0].header == EntryHeader.METADATA
    assert second[0].body == "DETAILED LOGS: ENABLE"


def test_unknown_header_collects_continuations_until_next_header() -> None:
    buffer = LineBuffer()

    entries = buffer.feed(
        "[SomeHeader] started\n"
        "continuation line\n"
        "[ConnectionManager] Reconnect result : Connected\n"
    )

    assert [entry.header for entry in entries] == [
        EntryHeader.UNKNOWN,
        EntryHeader.CONNECTION_MANAGER,
    ]
    assert entries[0].body == "[SomeHeader] started\ncontinuation line"
    assert entries[1].body == "[ConnectionManager] Reconnect result : Connected"


def test_new_header_flushes_buffered_multiline_entry_before_immediate_header() -> None:
    buffer = LineBuffer()

    entries = buffer.feed(
        "[Client GRE] first line\n"
        " continuation line\n"
        "[ConnectionManager] Reconnect result : Connected\n"
    )

    assert [entry.header for entry in entries] == [
        EntryHeader.CLIENT_GRE,
        EntryHeader.CONNECTION_MANAGER,
    ]
    assert entries[0].body == "[Client GRE] first line\n continuation line"
    assert entries[1].body == "[ConnectionManager] Reconnect result : Connected"


def test_orphan_partial_noise_is_ignored_after_flush() -> None:
    buffer = LineBuffer()

    first = buffer.feed("PreviousPlayBladeVisualState")
    second = buffer.flush()

    assert first == []
    assert second == []
