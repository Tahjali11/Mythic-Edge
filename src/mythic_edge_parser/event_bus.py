from __future__ import annotations

import asyncio
from dataclasses import dataclass
from time import monotonic
from typing import Callable, Generic, TypeVar

from .events import GameEvent

T = TypeVar("T")
_SENTINEL = object()
_SCHEMA_VERSION = "event_bus_queue_pressure_metrics.v1"
_CONSUMER_CLASSIFICATION_SOURCE = "event_bus_consumer_delivery_classification.v1"
_NON_CLAIMS = (
    "not_runtime_reliability_readiness",
    "not_release_readiness",
    "not_deploy_readiness",
    "not_production_readiness",
    "not_parser_truth",
    "not_delivery_policy_authorization",
    "not_consumer_classification_change",
    "not_workbook_truth",
    "not_webhook_truth",
    "not_api_contract",
    "not_ci_gate",
    "not_security_assurance",
    "not_privacy_assurance",
    "not_analytics_truth",
    "not_ai_truth",
    "not_coaching_truth",
)
_CONSUMER_CLASSIFICATIONS = {
    "parser_runner_main_loop": ("truth_critical", "classified"),
    "local_app_live_capture_supervisor": ("mixed", "classified"),
    "mtga_event_stream_start": ("publisher_or_factory", "publisher_or_factory"),
    "event_bus_test_subscriber": ("test_fixture_only", "test_fixture_only"),
    "unknown_subscriber": ("unknown", "classification_required"),
}


@dataclass(frozen=True, slots=True)
class EventBusPublishWaitSummary:
    wait_observed: bool
    publish_wait_count: int
    total_wait_seconds: float
    max_wait_seconds: float
    wait_bucket: str


@dataclass(frozen=True, slots=True)
class EventBusEventRateSummary:
    window_publish_calls: int
    window_elapsed_seconds: float
    events_per_second_bucket: str


@dataclass(frozen=True, slots=True)
class EventBusSubscriberPressure:
    subscriber_ref: str
    consumer_id: str
    consumer_class: str
    classification_status: str
    current_queue_depth: int
    max_queue_depth: int
    queue_capacity: int
    pressure_status: str
    publish_wait_count: int


@dataclass(frozen=True, slots=True)
class EventBusQueuePressureSnapshot:
    schema_version: str
    metrics_status: str
    subscriber_count: int
    queue_capacity: int
    total_publish_calls: int
    publish_wait_count: int
    current_total_queue_depth: int
    max_total_queue_depth: int
    current_max_subscriber_depth: int
    max_subscriber_depth: int
    subscriber_pressure: tuple[EventBusSubscriberPressure, ...]
    consumer_classification_source: str
    classification_status: str
    event_rate_summary: EventBusEventRateSummary
    publish_wait_summary: EventBusPublishWaitSummary
    non_claims: tuple[str, ...]


@dataclass(slots=True)
class _SubscriberMetrics:
    subscriber_ref: str
    consumer_id: str
    consumer_class: str
    classification_status: str
    max_queue_depth: int = 0
    publish_wait_count: int = 0


@dataclass(slots=True)
class Subscriber(Generic[T]):
    _queue: asyncio.Queue[object]
    _closed_event: asyncio.Event
    _space_available: asyncio.Condition

    async def recv(self) -> T | None:
        try:
            item = self._queue.get_nowait()
        except asyncio.QueueEmpty:
            if self._closed_event.is_set():
                return None
        else:
            await self._notify_space_available()
            if item is _SENTINEL:
                return None
            return item  # type: ignore[return-value]

        get_task = asyncio.create_task(self._queue.get())
        close_task = asyncio.create_task(self._closed_event.wait())
        done, pending = await asyncio.wait(
            {get_task, close_task},
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
        if get_task in done:
            item = await get_task
            await self._notify_space_available()
            if item is _SENTINEL:
                return None
            return item  # type: ignore[return-value]
        try:
            item = self._queue.get_nowait()
        except asyncio.QueueEmpty:
            return None
        await self._notify_space_available()
        if item is _SENTINEL:
            return None
        return item  # type: ignore[return-value]

    async def _notify_space_available(self) -> None:
        async with self._space_available:
            self._space_available.notify_all()


class EventBus:
    def __init__(self, capacity: int = 1024, *, time_source: Callable[[], float] | None = None) -> None:
        self._capacity = capacity
        self._queues: list[asyncio.Queue[object]] = []
        self._closed = False
        self._closed_event = asyncio.Event()
        self._space_available = asyncio.Condition()
        self._time_source = time_source or monotonic
        self._subscriber_sequence = 0
        self._subscriber_metrics: dict[asyncio.Queue[object], _SubscriberMetrics] = {}
        self._active_waiters: dict[asyncio.Queue[object], int] = {}
        self._total_publish_calls = 0
        self._publish_wait_count = 0
        self._total_wait_seconds = 0.0
        self._max_wait_seconds = 0.0
        self._max_total_queue_depth = 0
        self._max_subscriber_depth = 0
        self._metrics_window_start = self._now()
        self._metrics_reset = False

    @classmethod
    def with_default_capacity(cls) -> "EventBus":
        return cls(capacity=1024)

    def subscribe(self, *, consumer_id: str = "unknown_subscriber") -> Subscriber[GameEvent]:
        q: asyncio.Queue[object] = asyncio.Queue(maxsize=self._capacity)
        self._queues.append(q)
        self._subscriber_sequence += 1
        normalized_id, consumer_class, classification_status = _consumer_metadata(consumer_id)
        self._subscriber_metrics[q] = _SubscriberMetrics(
            subscriber_ref=f"subscriber_{self._subscriber_sequence}",
            consumer_id=normalized_id,
            consumer_class=consumer_class,
            classification_status=classification_status,
        )
        return Subscriber(q, self._closed_event, self._space_available)

    async def publish(self, event: GameEvent) -> None:
        if self._closed:
            return
        publish_waited = False
        publish_wait_seconds = 0.0
        for q in list(self._queues):
            accepted, waited, wait_seconds = await self._put_unless_closed(q, event)
            if not accepted:
                return
            if waited:
                publish_waited = True
                publish_wait_seconds += wait_seconds
                subscriber_metrics = self._subscriber_metrics.get(q)
                if subscriber_metrics is not None:
                    subscriber_metrics.publish_wait_count += 1
        self._total_publish_calls += 1
        if publish_waited:
            self._publish_wait_count += 1
            self._total_wait_seconds += publish_wait_seconds
            self._max_wait_seconds = max(self._max_wait_seconds, publish_wait_seconds)
        self._metrics_reset = False
        self._record_depths()

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._closed_event.set()
        for q in list(self._queues):
            try:
                q.put_nowait(_SENTINEL)
            except asyncio.QueueFull:
                pass
        async with self._space_available:
            self._space_available.notify_all()
        self._queues.clear()
        self._subscriber_metrics.clear()
        self._active_waiters.clear()

    def queue_pressure_snapshot(self) -> EventBusQueuePressureSnapshot:
        current_depths = [q.qsize() for q in self._queues]
        current_total_queue_depth = sum(current_depths)
        current_max_subscriber_depth = max(current_depths, default=0)
        return EventBusQueuePressureSnapshot(
            schema_version=_SCHEMA_VERSION,
            metrics_status=self._metrics_status(),
            subscriber_count=len(self._queues),
            queue_capacity=self._capacity,
            total_publish_calls=self._total_publish_calls,
            publish_wait_count=self._publish_wait_count,
            current_total_queue_depth=current_total_queue_depth,
            max_total_queue_depth=self._max_total_queue_depth,
            current_max_subscriber_depth=current_max_subscriber_depth,
            max_subscriber_depth=self._max_subscriber_depth,
            subscriber_pressure=tuple(self._subscriber_pressure(q) for q in self._queues),
            consumer_classification_source=_CONSUMER_CLASSIFICATION_SOURCE,
            classification_status=self._classification_status(),
            event_rate_summary=self._event_rate_summary(),
            publish_wait_summary=self._publish_wait_summary(),
            non_claims=_NON_CLAIMS,
        )

    def reset_queue_pressure_metrics(self) -> None:
        self._total_publish_calls = 0
        self._publish_wait_count = 0
        self._total_wait_seconds = 0.0
        self._max_wait_seconds = 0.0
        self._metrics_window_start = self._now()
        self._metrics_reset = True
        current_total_queue_depth = 0
        current_max_subscriber_depth = 0
        for q in self._queues:
            depth = q.qsize()
            current_total_queue_depth += depth
            current_max_subscriber_depth = max(current_max_subscriber_depth, depth)
            subscriber_metrics = self._subscriber_metrics.get(q)
            if subscriber_metrics is not None:
                subscriber_metrics.max_queue_depth = depth
                subscriber_metrics.publish_wait_count = 0
        self._max_total_queue_depth = current_total_queue_depth
        self._max_subscriber_depth = current_max_subscriber_depth

    async def _put_unless_closed(self, q: asyncio.Queue[object], item: object) -> tuple[bool, bool, float]:
        wait_started_at: float | None = None
        async with self._space_available:
            try:
                while q.full() and not self._closed:
                    if wait_started_at is None:
                        wait_started_at = self._now()
                        self._active_waiters[q] = self._active_waiters.get(q, 0) + 1
                    await self._space_available.wait()
                wait_seconds = max(0.0, self._now() - wait_started_at) if wait_started_at is not None else 0.0
                if self._closed:
                    return False, wait_started_at is not None, wait_seconds
                q.put_nowait(item)
                return True, wait_started_at is not None, wait_seconds
            finally:
                if wait_started_at is not None:
                    self._decrement_waiter(q)

    def _decrement_waiter(self, q: asyncio.Queue[object]) -> None:
        current = self._active_waiters.get(q, 0)
        if current <= 1:
            self._active_waiters.pop(q, None)
            return
        self._active_waiters[q] = current - 1

    def _record_depths(self) -> None:
        current_total_queue_depth = 0
        current_max_subscriber_depth = 0
        for q in self._queues:
            depth = q.qsize()
            current_total_queue_depth += depth
            current_max_subscriber_depth = max(current_max_subscriber_depth, depth)
            subscriber_metrics = self._subscriber_metrics.get(q)
            if subscriber_metrics is not None:
                subscriber_metrics.max_queue_depth = max(subscriber_metrics.max_queue_depth, depth)
        self._max_total_queue_depth = max(self._max_total_queue_depth, current_total_queue_depth)
        self._max_subscriber_depth = max(self._max_subscriber_depth, current_max_subscriber_depth)

    def _subscriber_pressure(self, q: asyncio.Queue[object]) -> EventBusSubscriberPressure:
        subscriber_metrics = self._subscriber_metrics[q]
        current_depth = q.qsize()
        return EventBusSubscriberPressure(
            subscriber_ref=subscriber_metrics.subscriber_ref,
            consumer_id=subscriber_metrics.consumer_id,
            consumer_class=subscriber_metrics.consumer_class,
            classification_status=subscriber_metrics.classification_status,
            current_queue_depth=current_depth,
            max_queue_depth=subscriber_metrics.max_queue_depth,
            queue_capacity=self._capacity,
            pressure_status=self._pressure_status(q, subscriber_metrics, current_depth),
            publish_wait_count=subscriber_metrics.publish_wait_count,
        )

    def _pressure_status(
        self,
        q: asyncio.Queue[object],
        subscriber_metrics: _SubscriberMetrics,
        current_depth: int,
    ) -> str:
        if self._closed:
            return "pressure_closed"
        if self._active_waiters.get(q, 0) > 0:
            return "pressure_waiting"
        if self._capacity > 0 and current_depth >= self._capacity:
            return "pressure_near_capacity"
        if subscriber_metrics.publish_wait_count > 0 or subscriber_metrics.max_queue_depth > 0:
            return "pressure_observed"
        return "pressure_ok"

    def _metrics_status(self) -> str:
        if self._closed:
            return "metrics_unavailable_closed_bus"
        if self._metrics_reset:
            return "metrics_reset"
        return "metrics_available_in_memory"

    def _classification_status(self) -> str:
        statuses = {self._subscriber_metrics[q].classification_status for q in self._queues}
        if "classification_unknown_fail_closed" in statuses:
            return "classification_unknown_fail_closed"
        if "classification_review_required" in statuses:
            return "classification_review_required"
        if "classification_required" in statuses:
            return "classification_required"
        if statuses == {"test_fixture_only"}:
            return "test_fixture_only"
        if statuses == {"publisher_or_factory"}:
            return "publisher_or_factory"
        return "classified"

    def _event_rate_summary(self) -> EventBusEventRateSummary:
        elapsed = max(0.0, self._now() - self._metrics_window_start)
        return EventBusEventRateSummary(
            window_publish_calls=self._total_publish_calls,
            window_elapsed_seconds=elapsed,
            events_per_second_bucket=_event_rate_bucket(self._total_publish_calls, elapsed),
        )

    def _publish_wait_summary(self) -> EventBusPublishWaitSummary:
        return EventBusPublishWaitSummary(
            wait_observed=self._publish_wait_count > 0,
            publish_wait_count=self._publish_wait_count,
            total_wait_seconds=self._total_wait_seconds,
            max_wait_seconds=self._max_wait_seconds,
            wait_bucket=_wait_bucket(self._publish_wait_count, self._max_wait_seconds),
        )

    def _now(self) -> float:
        return self._time_source()


def _consumer_metadata(consumer_id: str) -> tuple[str, str, str]:
    if not isinstance(consumer_id, str):
        return "unknown_subscriber", "unknown", "classification_unknown_fail_closed"
    metadata = _CONSUMER_CLASSIFICATIONS.get(consumer_id)
    if metadata is None:
        return "unknown_subscriber", "unknown", "classification_unknown_fail_closed"
    consumer_class, classification_status = metadata
    return consumer_id, consumer_class, classification_status


def _wait_bucket(publish_wait_count: int, max_wait_seconds: float) -> str:
    if publish_wait_count <= 0:
        return "wait_none"
    if max_wait_seconds <= 0.05:
        return "wait_observed_short"
    if max_wait_seconds <= 1.0:
        return "wait_observed_moderate"
    return "wait_observed_long"


def _event_rate_bucket(publish_calls: int, elapsed_seconds: float) -> str:
    if publish_calls <= 0:
        return "rate_not_observed"
    if elapsed_seconds <= 0:
        return "rate_unknown"
    events_per_second = publish_calls / elapsed_seconds
    if events_per_second < 1:
        return "rate_low"
    if events_per_second < 10:
        return "rate_moderate"
    if events_per_second < 100:
        return "rate_high"
    return "rate_burst"
