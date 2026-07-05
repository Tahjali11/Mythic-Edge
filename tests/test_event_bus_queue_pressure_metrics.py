import asyncio
from dataclasses import asdict

import pytest

from mythic_edge_parser.event_bus import EventBus
from mythic_edge_parser.events import EventMetadata, SessionEvent


class _FakeClock:
    def __init__(self, value: float = 100.0) -> None:
        self.value = value

    def __call__(self) -> float:
        return self.value

    def advance(self, seconds: float) -> None:
        self.value += seconds


def _event(label: str, *, payload_marker: str | None = None) -> SessionEvent:
    payload = {"type": label}
    if payload_marker is not None:
        payload["marker"] = payload_marker
    return SessionEvent(EventMetadata.empty(), payload)


async def _assert_publish_blocks(task: asyncio.Task[None]) -> None:
    with pytest.raises(TimeoutError):
        await asyncio.wait_for(asyncio.shield(task), timeout=0.01)


def test_queue_pressure_metrics_start_empty_and_public_safe() -> None:
    clock = _FakeClock()
    bus = EventBus(capacity=2, time_source=clock)

    snapshot = bus.queue_pressure_snapshot()

    assert snapshot.schema_version == "event_bus_queue_pressure_metrics.v1"
    assert snapshot.metrics_status == "metrics_available_in_memory"
    assert snapshot.subscriber_count == 0
    assert snapshot.queue_capacity == 2
    assert snapshot.total_publish_calls == 0
    assert snapshot.publish_wait_count == 0
    assert snapshot.current_total_queue_depth == 0
    assert snapshot.max_total_queue_depth == 0
    assert snapshot.subscriber_pressure == ()
    assert snapshot.consumer_classification_source == "event_bus_consumer_delivery_classification.v1"
    assert snapshot.classification_status == "classified"
    assert snapshot.event_rate_summary.window_publish_calls == 0
    assert snapshot.event_rate_summary.events_per_second_bucket == "rate_not_observed"
    assert snapshot.publish_wait_summary.wait_observed is False
    assert snapshot.publish_wait_summary.wait_bucket == "wait_none"
    assert "not_parser_truth" in snapshot.non_claims
    assert "not_delivery_policy_authorization" in snapshot.non_claims


def test_queue_pressure_metrics_track_depths_and_consumer_classification() -> None:
    async def run() -> None:
        clock = _FakeClock()
        bus = EventBus(capacity=2, time_source=clock)
        subscriber = bus.subscribe(consumer_id="parser_runner_main_loop")

        await bus.publish(_event("first"))
        clock.advance(2.0)
        snapshot = bus.queue_pressure_snapshot()

        assert snapshot.total_publish_calls == 1
        assert snapshot.current_total_queue_depth == 1
        assert snapshot.max_total_queue_depth == 1
        assert snapshot.current_max_subscriber_depth == 1
        assert snapshot.max_subscriber_depth == 1
        assert snapshot.classification_status == "classified"
        assert snapshot.event_rate_summary.events_per_second_bucket == "rate_low"

        subscriber_pressure = snapshot.subscriber_pressure[0]
        assert subscriber_pressure.subscriber_ref == "subscriber_1"
        assert subscriber_pressure.consumer_id == "parser_runner_main_loop"
        assert subscriber_pressure.consumer_class == "truth_critical"
        assert subscriber_pressure.classification_status == "classified"
        assert subscriber_pressure.current_queue_depth == 1
        assert subscriber_pressure.max_queue_depth == 1
        assert subscriber_pressure.pressure_status == "pressure_observed"

        assert await asyncio.wait_for(subscriber.recv(), timeout=1) is not None
        after_recv = bus.queue_pressure_snapshot()
        assert after_recv.current_total_queue_depth == 0
        assert after_recv.max_total_queue_depth == 1
        assert after_recv.subscriber_pressure[0].current_queue_depth == 0
        assert after_recv.subscriber_pressure[0].max_queue_depth == 1

        await bus.close()

    asyncio.run(run())


def test_queue_pressure_metrics_record_backpressure_wait_without_changing_delivery() -> None:
    async def run() -> None:
        clock = _FakeClock()
        bus = EventBus(capacity=1, time_source=clock)
        subscriber = bus.subscribe(consumer_id="event_bus_test_subscriber")
        first = _event("first")
        second = _event("second")

        await bus.publish(first)
        blocked_publish = asyncio.create_task(bus.publish(second))

        await _assert_publish_blocks(blocked_publish)
        waiting_snapshot = bus.queue_pressure_snapshot()
        assert waiting_snapshot.subscriber_pressure[0].pressure_status == "pressure_waiting"

        clock.advance(0.25)
        assert await asyncio.wait_for(subscriber.recv(), timeout=1) == first
        await asyncio.wait_for(blocked_publish, timeout=1)
        assert await asyncio.wait_for(subscriber.recv(), timeout=1) == second

        snapshot = bus.queue_pressure_snapshot()
        assert snapshot.total_publish_calls == 2
        assert snapshot.publish_wait_count == 1
        assert snapshot.publish_wait_summary.wait_observed is True
        assert snapshot.publish_wait_summary.publish_wait_count == 1
        assert snapshot.publish_wait_summary.total_wait_seconds == pytest.approx(0.25)
        assert snapshot.publish_wait_summary.max_wait_seconds == pytest.approx(0.25)
        assert snapshot.publish_wait_summary.wait_bucket == "wait_observed_moderate"
        assert snapshot.subscriber_pressure[0].publish_wait_count == 1
        assert snapshot.subscriber_pressure[0].consumer_class == "test_fixture_only"
        assert snapshot.subscriber_pressure[0].classification_status == "test_fixture_only"

        await bus.close()

    asyncio.run(run())


def test_queue_pressure_metrics_fail_closed_for_unknown_consumer_without_echoing_input() -> None:
    unsafe_consumer_id = "unsafe_consumer_id_with_sensitive_marker"
    bus = EventBus(capacity=1)

    bus.subscribe(consumer_id=unsafe_consumer_id)
    snapshot = bus.queue_pressure_snapshot()

    assert snapshot.classification_status == "classification_unknown_fail_closed"
    assert snapshot.subscriber_pressure[0].consumer_id == "unknown_subscriber"
    assert snapshot.subscriber_pressure[0].consumer_class == "unknown"
    assert snapshot.subscriber_pressure[0].classification_status == "classification_unknown_fail_closed"
    assert unsafe_consumer_id not in repr(asdict(snapshot))


def test_queue_pressure_metrics_do_not_expose_event_payload_or_event_kind() -> None:
    async def run() -> None:
        bus = EventBus(capacity=2)
        bus.subscribe(consumer_id="event_bus_test_subscriber")
        private_marker = "synthetic_local_path_marker_hidden_inside_event_payload"

        await bus.publish(_event("secret_event_type", payload_marker=private_marker))
        snapshot_text = repr(asdict(bus.queue_pressure_snapshot()))

        assert private_marker not in snapshot_text
        assert "secret_event_type" not in snapshot_text
        assert "Session" not in snapshot_text
        assert "raw_bytes" not in snapshot_text
        assert "raw_bytes_hash" not in snapshot_text

        await bus.close()

    asyncio.run(run())


def test_queue_pressure_metrics_reset_does_not_clear_queues_or_change_delivery() -> None:
    async def run() -> None:
        bus = EventBus(capacity=2)
        subscriber = bus.subscribe(consumer_id="event_bus_test_subscriber")
        queued = _event("queued")

        await bus.publish(queued)
        bus.reset_queue_pressure_metrics()

        snapshot = bus.queue_pressure_snapshot()
        assert snapshot.metrics_status == "metrics_reset"
        assert snapshot.total_publish_calls == 0
        assert snapshot.publish_wait_count == 0
        assert snapshot.current_total_queue_depth == 1
        assert snapshot.max_total_queue_depth == 1
        assert snapshot.subscriber_pressure[0].current_queue_depth == 1
        assert snapshot.subscriber_pressure[0].max_queue_depth == 1

        assert await asyncio.wait_for(subscriber.recv(), timeout=1) == queued
        after_recv = bus.queue_pressure_snapshot()
        assert after_recv.current_total_queue_depth == 0

        await bus.close()

    asyncio.run(run())


def test_queue_pressure_metrics_closed_bus_drops_subscriber_summaries() -> None:
    async def run() -> None:
        bus = EventBus(capacity=1)
        subscriber = bus.subscribe(consumer_id="event_bus_test_subscriber")

        await bus.publish(_event("queued"))
        await bus.close()
        snapshot = bus.queue_pressure_snapshot()

        assert snapshot.metrics_status == "metrics_unavailable_closed_bus"
        assert snapshot.subscriber_count == 0
        assert snapshot.subscriber_pressure == ()
        assert snapshot.max_total_queue_depth == 1
        assert await asyncio.wait_for(subscriber.recv(), timeout=1) is not None
        assert await asyncio.wait_for(subscriber.recv(), timeout=1) is None

    asyncio.run(run())
