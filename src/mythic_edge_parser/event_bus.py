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

    async def recv(self) -> T | None:
        item = await self._queue.get()
        if item is _SENTINEL:
            return None
        return item  # type: ignore[return-value]


class EventBus:
    def __init__(self, capacity: int = 1024) -> None:
        self._capacity = capacity
        self._queues: list[asyncio.Queue[object]] = []
        self._closed = False

    @classmethod
    def with_default_capacity(cls) -> "EventBus":
        return cls(capacity=1024)

    def subscribe(self) -> Subscriber[GameEvent]:
        q: asyncio.Queue[object] = asyncio.Queue(maxsize=self._capacity)
        self._queues.append(q)
        return Subscriber(q)

    async def publish(self, event: GameEvent) -> None:
        if self._closed:
            return
        dead: list[asyncio.Queue[object]] = []
        for q in self._queues:
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                try:
                    _ = q.get_nowait()
                    q.put_nowait(event)
                except Exception:
                    dead.append(q)
        for q in dead:
            if q in self._queues:
                self._queues.remove(q)

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        for q in list(self._queues):
            await q.put(_SENTINEL)
        self._queues.clear()
