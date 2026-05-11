from __future__ import annotations

import asyncio
from dataclasses import dataclass
from logging import Logger
from pathlib import Path

from .app.diagnostics import get_logger, record_router_failure
from .event_bus import EventBus, Subscriber
from .events import DetailedLoggingStatusEvent, EventMetadata, GameEvent, LogFileRotatedEvent
from .log.entry import LogEntry
from .log.tailer import FileTailer, TailBatch, TailerError
from .router import Router


class StreamError(Exception):
    pass


@dataclass(slots=True)
class MtgaEventStream:
    _shutdown_event: asyncio.Event
    _pipeline_task: asyncio.Task[None] | None
    _bus: EventBus
    _tailer: FileTailer
    _router: Router
    _logger: Logger
    _log_path: Path
    _detailed_logging_known: bool = False

    @classmethod
    async def start(cls, log_path: Path) -> tuple["MtgaEventStream", Subscriber[GameEvent]]:
        logger = get_logger("stream")
        try:
            # Default to live tailing so launcher startup does not replay stale
            # matches from previous MTGA sessions into the sheet.
            tailer = await FileTailer.open_from_end(log_path)
        except TailerError as exc:
            raise StreamError(str(exc)) from exc
        bus = EventBus.with_default_capacity()
        subscriber = bus.subscribe()
        router = Router()
        shutdown_event = asyncio.Event()
        stream = cls(
            _shutdown_event=shutdown_event,
            _pipeline_task=None,
            _bus=bus,
            _tailer=tailer,
            _router=router,
            _logger=logger,
            _log_path=log_path,
        )
        task = asyncio.create_task(stream._run_pipeline(), name="manasight-parser-py-pipeline")
        stream._pipeline_task = task
        return stream, subscriber

    async def shutdown(self) -> None:
        self._shutdown_event.set()
        if self._pipeline_task is not None:
            await self._pipeline_task

    async def _run_pipeline(self) -> None:
        try:
            while not self._shutdown_event.is_set():
                await self._run_pipeline_iteration()
                await asyncio.sleep(self._tailer.poll_interval_seconds)
        finally:
            await self._bus.close()

    async def _run_pipeline_iteration(self) -> None:
        batch = await self._poll_batch()
        await self._publish_rotation_event_if_needed(batch)
        if batch.entries:
            await self._handle_entry_batch(batch)
            return
        await self._maybe_publish_inferred_detailed_logging_status()

    async def _poll_batch(self) -> TailBatch:
        try:
            return await self._tailer.poll_once()
        except Exception as exc:
            self._logger.exception("Tailer polling failed for %s: %s", self._log_path, exc)
            raise

    async def _publish_rotation_event_if_needed(self, batch: TailBatch) -> None:
        if not batch.rotated:
            return
        event = LogFileRotatedEvent(
            EventMetadata.empty(),
            {"type": "log_file_rotated", "path": _display_log_path(self._log_path)},
        )
        await self._bus.publish(event)

    async def _handle_entry_batch(self, batch: TailBatch) -> None:
        if batch.structured_headers_seen and not self._detailed_logging_known:
            await self._publish_detailed_logging_status(enabled=True)
        for entry in batch.entries:
            await self._route_and_publish_entry(entry)

    async def _route_and_publish_entry(self, entry: LogEntry) -> None:
        try:
            routed_events = self._router.route(entry)
        except Exception as exc:
            out_path = record_router_failure(entry, exc)
            self._logger.exception(
                "Router failed for %s entry; saved failure record to %s",
                entry.header.value,
                out_path,
            )
            return
        for event in routed_events:
            await self._bus.publish(event)

    async def _maybe_publish_inferred_detailed_logging_status(self) -> None:
        if self._tailer.seconds_without_structured_headers < 30 or self._detailed_logging_known:
            return
        await self._publish_detailed_logging_status(enabled=False)

    async def _publish_detailed_logging_status(self, *, enabled: bool) -> None:
        self._detailed_logging_known = True
        await self._bus.publish(
            DetailedLoggingStatusEvent(EventMetadata.empty(), {"enabled": enabled})
        )


def _display_log_path(log_path: Path) -> str:
    return log_path.name or "[log file]"
