from pathlib import Path

from mythic_edge_parser.log.entry import (
    EntryHeader,
    LineBuffer,
    LogEntry,
    is_single_line_header,
)

FIXTURE = (
    Path(__file__).resolve().parent / "fixtures" / "flush_timing_corpus_slice.log"
)


def _fixture_lines() -> list[str]:
    return [
        line.rstrip("\r\n")
        for line in FIXTURE.read_text(encoding="utf-8").splitlines()
        if not line.startswith("#")
    ]


def test_single_line_headers_flush_in_same_call() -> None:
    buffer = LineBuffer()
    for idx, line in enumerate(_fixture_lines()):
        entries = buffer.feed(f"{line}\n")
        if is_single_line_header(line):
            assert entries, f"single-line header at line {idx} produced no entries: {line!r}"
            assert entries[-1].body == line


def test_single_line_entry_bodies_stay_clean() -> None:
    buffer = LineBuffer()
    all_entries: list[LogEntry] = []
    for line in _fixture_lines():
        all_entries.extend(buffer.feed(f"{line}\n"))
    all_entries.extend(buffer.flush())

    noise_markers = [
        "PreviousPlayBladeVisualState",
        "BEGIN home page notification flow",
        "Beacon does not have identifier",
        "END home page notification flow",
    ]
    for entry in all_entries:
        if "\n" not in entry.body:
            for noise in noise_markers:
                assert noise not in entry.body


def test_replay_produces_one_entry_per_header_line() -> None:
    lines = _fixture_lines()
    expected_headers = [
        line
        for line in lines
        if line.startswith("[UnityCrossThreadLogger]")
        or line.startswith("[ConnectionManager]")
        or line.startswith("Matchmaking: ")
        or line.startswith("[Client GRE]")
        or line.startswith("DETAILED LOGS:")
    ]

    buffer = LineBuffer()
    all_entries: list[LogEntry] = []
    for line in lines:
        all_entries.extend(buffer.feed(f"{line}\n"))
    all_entries.extend(buffer.flush())

    assert len(all_entries) == len(expected_headers)
    for entry, header_line in zip(all_entries, expected_headers, strict=True):
        assert entry.body.splitlines()[0] == header_line
    assert any(entry.header == EntryHeader.UNITY_CROSS_THREAD_LOGGER for entry in all_entries)
