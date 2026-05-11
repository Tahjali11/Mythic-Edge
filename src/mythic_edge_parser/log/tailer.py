from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from pathlib import Path

from .entry import EntryHeader, LineBuffer, LogEntry

DEFAULT_POLL_INTERVAL_SECONDS = 0.25
_STRUCTURED_HEADERS = {
    EntryHeader.UNITY_CROSS_THREAD_LOGGER,
    EntryHeader.CLIENT_GRE,
}


def _monotonic_now() -> float:
    return time.monotonic()


class TailerError(Exception):
    pass


@dataclass(slots=True)
class TailBatch:
    entries: list[LogEntry]
    rotated: bool = False
    structured_headers_seen: bool = False


class FileTailer:
    def __init__(self, path: Path, *, poll_interval_seconds: float = DEFAULT_POLL_INTERVAL_SECONDS) -> None:
        self.path = path
        self._buffer = LineBuffer()
        self._offset = 0
        self._poll_interval_seconds = poll_interval_seconds
        self._seconds_without_structured_headers = 0.0
        self._last_poll_monotonic = _monotonic_now()

    @property
    def seconds_without_structured_headers(self) -> float:
        return self._seconds_without_structured_headers

    @property
    def poll_interval_seconds(self) -> float:
        return self._poll_interval_seconds

    @classmethod
    async def open_from_start(
        cls,
        path: Path,
        *,
        poll_interval_seconds: float = DEFAULT_POLL_INTERVAL_SECONDS,
    ) -> "FileTailer":
        await asyncio.to_thread(cls._ensure_log_exists, path)
        tailer = cls(path, poll_interval_seconds=poll_interval_seconds)
        tailer._offset = 0
        return tailer

    @classmethod
    async def open_from_end(
        cls,
        path: Path,
        *,
        poll_interval_seconds: float = DEFAULT_POLL_INTERVAL_SECONDS,
    ) -> "FileTailer":
        tailer = cls(path, poll_interval_seconds=poll_interval_seconds)
        tailer._offset = await asyncio.to_thread(cls._existing_size, path)
        return tailer

    async def poll(self) -> TailBatch:
        await asyncio.sleep(self._poll_interval_seconds)
        return await self.poll_once()

    async def poll_once(self) -> TailBatch:
        elapsed_seconds = self._advance_elapsed_seconds()
        rotated, chunk, next_offset = await asyncio.to_thread(
            self._read_poll_snapshot,
            self.path,
            self._offset,
        )

        if rotated:
            self._buffer = LineBuffer()
        self._offset = next_offset

        if not chunk:
            self._record_unstructured_poll(elapsed_seconds)
            return TailBatch([], rotated=rotated, structured_headers_seen=False)

        entries = self._parse_entries(chunk)
        structured_headers_seen = self._contains_structured_headers(entries)
        self._update_structured_header_health(elapsed_seconds, structured_headers_seen)
        return TailBatch(
            entries,
            rotated=rotated,
            structured_headers_seen=structured_headers_seen,
        )

    @staticmethod
    def _ensure_log_exists(path: Path) -> None:
        if not path.exists():
            raise TailerError(f"Log file does not exist: {FileTailer._display_path(path)}")

    @staticmethod
    def _display_path(path: Path) -> str:
        return path.name or "[log file]"

    @staticmethod
    def _existing_size(path: Path) -> int:
        try:
            return path.stat().st_size
        except FileNotFoundError as exc:
            raise TailerError(f"Log file disappeared: {FileTailer._display_path(path)}") from exc

    @staticmethod
    def _read_poll_snapshot(path: Path, offset: int) -> tuple[bool, bytes, int]:
        try:
            with path.open("rb") as handle:
                handle.seek(0, 2)
                size = handle.tell()
                rotated = size < offset
                handle.seek(0 if rotated else offset)
                chunk = handle.read()
                next_offset = handle.tell()
        except FileNotFoundError as exc:
            raise TailerError(f"Log file disappeared: {FileTailer._display_path(path)}") from exc
        return rotated, chunk, next_offset

    def _parse_entries(self, chunk: bytes) -> list[LogEntry]:
        entries = self._buffer.feed(chunk.decode("utf-8", errors="replace"))
        if chunk.endswith(b"\n"):
            entries.extend(self._buffer.flush())
        return entries

    def _advance_elapsed_seconds(self) -> float:
        now = _monotonic_now()
        elapsed_seconds = max(0.0, now - self._last_poll_monotonic)
        self._last_poll_monotonic = now
        return elapsed_seconds

    def _record_unstructured_poll(self, elapsed_seconds: float) -> None:
        self._seconds_without_structured_headers += elapsed_seconds

    @staticmethod
    def _contains_structured_headers(entries: list[LogEntry]) -> bool:
        return any(entry.header in _STRUCTURED_HEADERS for entry in entries)

    def _update_structured_header_health(
        self,
        elapsed_seconds: float,
        structured_headers_seen: bool,
    ) -> None:
        if structured_headers_seen:
            self._seconds_without_structured_headers = 0
            return
        self._seconds_without_structured_headers += elapsed_seconds
