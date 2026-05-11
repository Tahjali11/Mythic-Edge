import asyncio
from pathlib import Path

import pytest

from mythic_edge_parser.log.tailer import FileTailer


@pytest.mark.performance
def test_open_from_end_only_feeds_new_append_not_large_existing_history(tmp_path: Path) -> None:
    log_path = tmp_path / "Player.log"
    old_line = "[UnityCrossThreadLogger]old entry\n"
    appended_line = "[UnityCrossThreadLogger]new entry\n"
    log_path.write_text(old_line * 20000, encoding="utf-8")

    async def run() -> None:
        tailer = await FileTailer.open_from_end(log_path, poll_interval_seconds=0)
        feed_inputs: list[str] = []
        original_feed = tailer._buffer.feed

        def recording_feed(text: str):
            feed_inputs.append(text)
            return original_feed(text)

        tailer._buffer.feed = recording_feed

        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(appended_line)

        batch = await tailer.poll_once()
        assert len(batch.entries) == 1
        assert [text.replace("\r\n", "\n") for text in feed_inputs] == [appended_line]

    asyncio.run(run())


@pytest.mark.performance
def test_poll_once_with_no_new_bytes_skips_buffer_feed_work(tmp_path: Path) -> None:
    log_path = tmp_path / "Player.log"
    log_path.write_text("[UnityCrossThreadLogger]old entry\n" * 20000, encoding="utf-8")

    async def run() -> None:
        tailer = await FileTailer.open_from_end(log_path, poll_interval_seconds=0)
        feed_calls = 0
        original_feed = tailer._buffer.feed

        def recording_feed(text: str):
            nonlocal feed_calls
            feed_calls += 1
            return original_feed(text)

        tailer._buffer.feed = recording_feed

        batch = await tailer.poll_once()
        assert batch.entries == []
        assert feed_calls == 0

    asyncio.run(run())
