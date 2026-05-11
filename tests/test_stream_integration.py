import asyncio
import itertools
from pathlib import Path

import pytest

from mythic_edge_parser import stream as stream_module
from mythic_edge_parser.events import DetailedLoggingStatusEvent, LogFileRotatedEvent
from mythic_edge_parser.log.tailer import TailBatch
from mythic_edge_parser.stream import MtgaEventStream


@pytest.mark.integration
def test_stream_replays_appended_metadata_line_into_typed_event(
    monkeypatch,
    tmp_path: Path,
) -> None:
    log_path = tmp_path / "Player.log"
    log_path.write_text("", encoding="utf-8")
    original_open_from_end = stream_module.FileTailer.open_from_end

    async def open_from_end_zero(_cls, path: Path):
        return await original_open_from_end(path, poll_interval_seconds=0)

    monkeypatch.setattr(
        stream_module.FileTailer,
        "open_from_end",
        classmethod(open_from_end_zero),
    )

    async def run() -> None:
        stream, subscriber = await MtgaEventStream.start(log_path)
        try:
            with log_path.open("a", encoding="utf-8") as handle:
                handle.write("DETAILED LOGS: ENABLED\n")

            event = await asyncio.wait_for(subscriber.recv(), timeout=1)
            assert isinstance(event, DetailedLoggingStatusEvent)
            assert event.payload == {"enabled": True}
        finally:
            await stream.shutdown()

    asyncio.run(run())


@pytest.mark.integration
def test_stream_emits_disabled_status_after_30_seconds_without_structured_headers(
    monkeypatch,
    tmp_path: Path,
) -> None:
    log_path = tmp_path / "Player.log"
    log_path.write_text("", encoding="utf-8")
    original_open_from_end = stream_module.FileTailer.open_from_end

    async def open_from_end_zero(_cls, path: Path):
        return await original_open_from_end(path, poll_interval_seconds=0)

    monkeypatch.setattr(
        stream_module.FileTailer,
        "open_from_end",
        classmethod(open_from_end_zero),
    )
    monotonic_values = itertools.chain([100.0, 131.0], itertools.repeat(131.0))
    monkeypatch.setattr(
        "mythic_edge_parser.log.tailer._monotonic_now",
        lambda: next(monotonic_values),
    )

    async def run() -> None:
        stream, subscriber = await MtgaEventStream.start(log_path)
        try:
            event = await asyncio.wait_for(subscriber.recv(), timeout=1)
            assert isinstance(event, DetailedLoggingStatusEvent)
            assert event.payload == {"enabled": False}
        finally:
            await stream.shutdown()

    asyncio.run(run())


@pytest.mark.integration
def test_stream_emits_rotated_event_with_sanitized_log_path(
    monkeypatch,
    tmp_path: Path,
) -> None:
    class _FakeTailer:
        poll_interval_seconds = 0
        seconds_without_structured_headers = 0.0

        def __init__(self) -> None:
            self._batches = [
                TailBatch([], rotated=True, structured_headers_seen=False),
                TailBatch([], rotated=False, structured_headers_seen=False),
            ]

        async def poll_once(self) -> TailBatch:
            if self._batches:
                return self._batches.pop(0)
            return TailBatch([], rotated=False, structured_headers_seen=False)

    async def open_from_end_fake(_cls, _path: Path):
        return _FakeTailer()

    monkeypatch.setattr(
        stream_module.FileTailer,
        "open_from_end",
        classmethod(open_from_end_fake),
    )

    async def run() -> None:
        log_path = tmp_path / "secret-user-folder" / "Player.log"
        stream, subscriber = await MtgaEventStream.start(log_path)
        try:
            event = await asyncio.wait_for(subscriber.recv(), timeout=1)
            assert isinstance(event, LogFileRotatedEvent)
            assert event.payload == {"type": "log_file_rotated", "path": "Player.log"}
            assert event.metadata.raw_bytes == b""
        finally:
            await stream.shutdown()

    asyncio.run(run())
