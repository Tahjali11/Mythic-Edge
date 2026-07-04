from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Generic, TypeVar

from .events import GameEvent

T = TypeVar("T")
_SENTINEL = object()


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
    def __init__(self, capacity: int = 1024) -> None:
        self._capacity = capacity
        self._queues: list[asyncio.Queue[object]] = []
        self._closed = False
        self._closed_event = asyncio.Event()
        self._space_available = asyncio.Condition()

    @classmethod
    def with_default_capacity(cls) -> "EventBus":
        return cls(capacity=1024)

    def subscribe(self) -> Subscriber[GameEvent]:
        q: asyncio.Queue[object] = asyncio.Queue(maxsize=self._capacity)
        self._queues.append(q)
        return Subscriber(q, self._closed_event, self._space_available)

    async def publish(self, event: GameEvent) -> None:
        if self._closed:
            return
        for q in list(self._queues):
            accepted = await self._put_unless_closed(q, event)
            if not accepted:
                return

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

    async def _put_unless_closed(self, q: asyncio.Queue[object], item: object) -> bool:
        async with self._space_available:
            while q.full() and not self._closed:
                await self._space_available.wait()
            if self._closed:
                return False
            q.put_nowait(item)
            return True
