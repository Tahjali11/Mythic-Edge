import asyncio

import pytest

from mythic_edge_parser.event_bus import EventBus
from mythic_edge_parser.events import EventMetadata, SessionEvent


def _event(label: str) -> SessionEvent:
    return SessionEvent(EventMetadata.empty(), {"type": label})


async def _assert_publish_blocks(task: asyncio.Task[None]) -> None:
    with pytest.raises(TimeoutError):
        await asyncio.wait_for(asyncio.shield(task), timeout=0.01)


def test_publish_waits_for_full_subscriber_queue_and_preserves_order() -> None:
    async def run() -> None:
        bus = EventBus(capacity=1)
        subscriber = bus.subscribe()
        first = _event("first")
        second = _event("second")

        await bus.publish(first)
        blocked_publish = asyncio.create_task(bus.publish(second))

        await _assert_publish_blocks(blocked_publish)
        assert await asyncio.wait_for(subscriber.recv(), timeout=1) == first
        await asyncio.wait_for(blocked_publish, timeout=1)
        assert await asyncio.wait_for(subscriber.recv(), timeout=1) == second

        await bus.close()

    asyncio.run(run())


def test_full_queue_does_not_remove_slow_subscriber_as_dead() -> None:
    async def run() -> None:
        bus = EventBus(capacity=1)
        subscriber = bus.subscribe()
        first = _event("first")
        second = _event("second")
        third = _event("third")

        await bus.publish(first)
        blocked_publish = asyncio.create_task(bus.publish(second))

        await _assert_publish_blocks(blocked_publish)
        assert await asyncio.wait_for(subscriber.recv(), timeout=1) == first
        await asyncio.wait_for(blocked_publish, timeout=1)
        assert await asyncio.wait_for(subscriber.recv(), timeout=1) == second

        await bus.publish(third)
        assert await asyncio.wait_for(subscriber.recv(), timeout=1) == third

        await bus.close()

    asyncio.run(run())


def test_close_still_delivers_close_signal_to_subscriber() -> None:
    async def run() -> None:
        bus = EventBus(capacity=1)
        subscriber = bus.subscribe()

        await bus.close()

        assert await asyncio.wait_for(subscriber.recv(), timeout=1) is None

    asyncio.run(run())


def test_close_returns_when_subscriber_queue_is_full() -> None:
    async def run() -> None:
        bus = EventBus(capacity=1)
        subscriber = bus.subscribe()
        queued = _event("queued")

        await bus.publish(queued)
        await asyncio.wait_for(bus.close(), timeout=1)

        assert await asyncio.wait_for(subscriber.recv(), timeout=1) == queued
        assert await asyncio.wait_for(subscriber.recv(), timeout=1) is None

    asyncio.run(run())


def test_publish_after_close_does_not_deliver_new_events() -> None:
    async def run() -> None:
        bus = EventBus(capacity=1)
        subscriber = bus.subscribe()

        await bus.close()
        await bus.publish(_event("after_close"))

        assert await asyncio.wait_for(subscriber.recv(), timeout=1) is None

    asyncio.run(run())


def test_close_unblocks_publish_waiting_on_full_queue() -> None:
    async def run() -> None:
        bus = EventBus(capacity=1)
        subscriber = bus.subscribe()
        first = _event("first")
        second = _event("second")

        await bus.publish(first)
        blocked_publish = asyncio.create_task(bus.publish(second))
        await _assert_publish_blocks(blocked_publish)

        close_task = asyncio.create_task(bus.close())
        await asyncio.sleep(0)
        assert await asyncio.wait_for(subscriber.recv(), timeout=1) == first

        await asyncio.wait_for(blocked_publish, timeout=1)
        await asyncio.wait_for(close_task, timeout=1)
        assert await asyncio.wait_for(subscriber.recv(), timeout=1) is None

    asyncio.run(run())
