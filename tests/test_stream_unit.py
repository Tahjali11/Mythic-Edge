import asyncio
import logging
from pathlib import Path

from mythic_edge_parser.event_bus import EventBus
from mythic_edge_parser.events import EventMetadata, SessionEvent
from mythic_edge_parser.log.entry import EntryHeader, LogEntry
from mythic_edge_parser.log.tailer import TailBatch
from mythic_edge_parser.stream import MtgaEventStream


class _FakeTailer:
    def __init__(
        self,
        batch: TailBatch,
        *,
        poll_interval_seconds: float = 0,
        seconds_without_structured_headers: float = 0.0,
    ) -> None:
        self._batch = batch
        self.poll_interval_seconds = poll_interval_seconds
        self.seconds_without_structured_headers = seconds_without_structured_headers

    async def poll_once(self) -> TailBatch:
        return self._batch


class _FakeRouter:
    def __init__(self, events: list[SessionEvent]) -> None:
        self._events = events
        self.entries: list[LogEntry] = []

    def route(self, entry: LogEntry) -> list[SessionEvent]:
        self.entries.append(entry)
        return list(self._events)


def test_run_pipeline_iteration_routes_entries_without_nested_pipeline_closure() -> None:
    entry = LogEntry(EntryHeader.UNITY_CROSS_THREAD_LOGGER, "[UnityCrossThreadLogger]session")
    routed_event = SessionEvent(EventMetadata.empty(), {"type": "session_logout"})
    tailer = _FakeTailer(TailBatch([entry], rotated=False, structured_headers_seen=False))
    router = _FakeRouter([routed_event])
    bus = EventBus.with_default_capacity()
    subscriber = bus.subscribe()
    stream = MtgaEventStream(
        _shutdown_event=asyncio.Event(),
        _pipeline_task=None,
        _bus=bus,
        _tailer=tailer,
        _router=router,
        _logger=logging.getLogger("test-stream"),
        _log_path=Path("Player.log"),
        _detailed_logging_known=True,
    )

    async def run() -> None:
        await stream._run_pipeline_iteration()
        event = await asyncio.wait_for(subscriber.recv(), timeout=1)
        assert event is not None
        assert event.kind == "Session"
        assert event.payload["type"] == "session_logout"
        assert router.entries == [entry]
        await bus.close()

    asyncio.run(run())
