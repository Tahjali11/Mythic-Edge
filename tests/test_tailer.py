import asyncio
from pathlib import Path

import pytest

from mythic_edge_parser.log.tailer import FileTailer, TailerError


def test_open_from_end_skips_existing_log_history(tmp_path: Path) -> None:
    log_path = tmp_path / "Player.log"
    log_path.write_text("[UnityCrossThreadLogger]old entry\n", encoding="utf-8")

    async def run() -> None:
        tailer = await FileTailer.open_from_end(log_path, poll_interval_seconds=0)

        first = await tailer.poll()
        assert first.entries == []
        assert first.rotated is False

        with log_path.open("a", encoding="utf-8") as handle:
            handle.write("[UnityCrossThreadLogger]new entry\n")

        second = await tailer.poll()
        assert len(second.entries) == 1
        assert "new entry" in second.entries[0].body

    asyncio.run(run())


def test_open_from_start_replays_existing_log_history(tmp_path: Path) -> None:
    log_path = tmp_path / "Player.log"
    log_path.write_text("[UnityCrossThreadLogger]old entry\n", encoding="utf-8")

    async def run() -> None:
        tailer = await FileTailer.open_from_start(log_path, poll_interval_seconds=0)

        first = await tailer.poll()
        assert len(first.entries) == 1
        assert "old entry" in first.entries[0].body
        assert first.rotated is False

    asyncio.run(run())


def test_poll_reports_rotation_and_reads_replacement_content(tmp_path: Path) -> None:
    log_path = tmp_path / "Player.log"
    log_path.write_text("[UnityCrossThreadLogger]very old entry that is longer\n", encoding="utf-8")

    async def run() -> None:
        tailer = await FileTailer.open_from_end(log_path, poll_interval_seconds=0)
        first = await tailer.poll()
        assert first.entries == []

        log_path.write_text("[UnityCrossThreadLogger]new entry\n", encoding="utf-8")

        second = await tailer.poll()
        assert second.rotated is True
        assert len(second.entries) == 1
        assert "new entry" in second.entries[0].body

    asyncio.run(run())


def test_partial_entry_is_buffered_until_newline(tmp_path: Path) -> None:
    log_path = tmp_path / "Player.log"
    log_path.write_text("", encoding="utf-8")

    async def run() -> None:
        tailer = await FileTailer.open_from_end(log_path, poll_interval_seconds=0)

        with log_path.open("a", encoding="utf-8") as handle:
            handle.write("[Client GRE]partial")

        first = await tailer.poll()
        assert first.entries == []

        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(" entry\n")

        second = await tailer.poll()
        assert len(second.entries) == 1
        assert second.entries[0].body == "[Client GRE]partial entry"

    asyncio.run(run())


def test_poll_once_tracks_real_elapsed_seconds(monkeypatch, tmp_path: Path) -> None:
    log_path = tmp_path / "Player.log"
    log_path.write_text("", encoding="utf-8")
    monotonic_values = iter([100.0, 103.5, 107.0])

    monkeypatch.setattr(
        "mythic_edge_parser.log.tailer._monotonic_now",
        lambda: next(monotonic_values),
    )

    async def run() -> None:
        tailer = await FileTailer.open_from_end(log_path, poll_interval_seconds=0)

        first = await tailer.poll_once()
        assert first.entries == []
        assert first.structured_headers_seen is False
        assert tailer.seconds_without_structured_headers == 3.5

        with log_path.open("a", encoding="utf-8") as handle:
            handle.write("[UnityCrossThreadLogger]new entry\n")

        second = await tailer.poll_once()
        assert len(second.entries) == 1
        assert second.structured_headers_seen is True
        assert tailer.seconds_without_structured_headers == 0

    asyncio.run(run())


def test_invalid_utf8_bytes_are_replaced_not_dropped(tmp_path: Path) -> None:
    log_path = tmp_path / "Player.log"
    log_path.write_bytes(b"[UnityCrossThreadLogger]bad\xffentry\n")

    async def run() -> None:
        tailer = await FileTailer.open_from_start(log_path, poll_interval_seconds=0)

        batch = await tailer.poll_once()
        assert len(batch.entries) == 1
        assert "bad\ufffdentry" in batch.entries[0].body

    asyncio.run(run())


def test_missing_file_errors_use_sanitized_filename(tmp_path: Path) -> None:
    missing_path = tmp_path / "nested" / "Player.log"

    async def run() -> None:
        with pytest.raises(TailerError) as exc_info:
            await FileTailer.open_from_end(missing_path, poll_interval_seconds=0)

        message = str(exc_info.value)
        assert "Player.log" in message
        assert str(missing_path) not in message

    asyncio.run(run())


def test_file_checks_are_offloaded_with_to_thread(monkeypatch, tmp_path: Path) -> None:
    log_path = tmp_path / "Player.log"
    log_path.write_text("[UnityCrossThreadLogger]entry\n", encoding="utf-8")
    to_thread_calls: list[str] = []

    original_to_thread = asyncio.to_thread

    async def recording_to_thread(func, /, *args, **kwargs):
        to_thread_calls.append(func.__name__)
        return await original_to_thread(func, *args, **kwargs)

    monkeypatch.setattr("mythic_edge_parser.log.tailer.asyncio.to_thread", recording_to_thread)

    async def run() -> None:
        tailer = await FileTailer.open_from_end(log_path, poll_interval_seconds=0)
        await tailer.poll_once()

    asyncio.run(run())

    assert "_existing_size" in to_thread_calls
    assert "_read_poll_snapshot" in to_thread_calls
