from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, ClassVar


class PerformanceClass(str, Enum):
    INTERACTIVE_DISPATCH = "InteractiveDispatch"
    DURABLE_PER_EVENT = "DurablePerEvent"
    POST_GAME_BATCH = "PostGameBatch"


@dataclass(slots=True)
class EventMetadata:
    timestamp: datetime | None
    raw_bytes: bytes
    raw_bytes_hash: str = field(init=False)

    @classmethod
    def empty(cls, timestamp: datetime | None = None) -> "EventMetadata":
        return cls(timestamp=timestamp, raw_bytes=b"")

    def __post_init__(self) -> None:
        self.raw_bytes_hash = hashlib.sha256(self.raw_bytes).hexdigest()


EventPayload = dict[str, Any]


@dataclass(slots=True)
class BaseEvent:
    metadata: EventMetadata
    payload: EventPayload
    performance_class: ClassVar[PerformanceClass]
    kind: ClassVar[str]

    def __post_init__(self) -> None:
        self.payload = _copy_payload_mapping(self.payload)

    def payload_copy(self) -> EventPayload:
        return dict(self.payload)


def _copy_payload_mapping(payload: Mapping[str, Any]) -> EventPayload:
    return dict(payload)


@dataclass(slots=True)
class GameStateEvent(BaseEvent):
    kind: ClassVar[str] = "GameState"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.INTERACTIVE_DISPATCH


@dataclass(slots=True)
class ClientActionEvent(BaseEvent):
    kind: ClassVar[str] = "ClientAction"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.INTERACTIVE_DISPATCH


@dataclass(slots=True)
class MatchStateEvent(BaseEvent):
    kind: ClassVar[str] = "MatchState"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.INTERACTIVE_DISPATCH


@dataclass(slots=True)
class DraftBotEvent(BaseEvent):
    kind: ClassVar[str] = "DraftBot"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.DURABLE_PER_EVENT


@dataclass(slots=True)
class DraftHumanEvent(BaseEvent):
    kind: ClassVar[str] = "DraftHuman"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.DURABLE_PER_EVENT


@dataclass(slots=True)
class DraftCompleteEvent(BaseEvent):
    kind: ClassVar[str] = "DraftComplete"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.DURABLE_PER_EVENT


@dataclass(slots=True)
class EventLifecycleEvent(BaseEvent):
    kind: ClassVar[str] = "EventLifecycle"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.DURABLE_PER_EVENT


@dataclass(slots=True)
class SessionEvent(BaseEvent):
    kind: ClassVar[str] = "Session"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.DURABLE_PER_EVENT


@dataclass(slots=True)
class RankEvent(BaseEvent):
    kind: ClassVar[str] = "Rank"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.DURABLE_PER_EVENT


@dataclass(slots=True)
class CollectionEvent(BaseEvent):
    kind: ClassVar[str] = "Collection"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.DURABLE_PER_EVENT


@dataclass(slots=True)
class DeckCollectionEvent(BaseEvent):
    kind: ClassVar[str] = "DeckCollection"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.DURABLE_PER_EVENT


@dataclass(slots=True)
class InventoryEvent(BaseEvent):
    kind: ClassVar[str] = "Inventory"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.DURABLE_PER_EVENT


@dataclass(slots=True)
class GameResultEvent(BaseEvent):
    kind: ClassVar[str] = "GameResult"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.POST_GAME_BATCH


@dataclass(slots=True)
class LogFileRotatedEvent(BaseEvent):
    kind: ClassVar[str] = "LogFileRotated"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.INTERACTIVE_DISPATCH


@dataclass(slots=True)
class DetailedLoggingStatusEvent(BaseEvent):
    kind: ClassVar[str] = "DetailedLoggingStatus"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.INTERACTIVE_DISPATCH


@dataclass(slots=True)
class MatchConnectionStateEvent(BaseEvent):
    kind: ClassVar[str] = "MatchConnectionState"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.INTERACTIVE_DISPATCH


@dataclass(slots=True)
class TcpConnectionCloseEvent(BaseEvent):
    kind: ClassVar[str] = "TcpConnectionClose"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.INTERACTIVE_DISPATCH


@dataclass(slots=True)
class WebSocketClosedEvent(BaseEvent):
    kind: ClassVar[str] = "WebSocketClosed"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.INTERACTIVE_DISPATCH


@dataclass(slots=True)
class ConnectionErrorEvent(BaseEvent):
    kind: ClassVar[str] = "ConnectionError"
    performance_class: ClassVar[PerformanceClass] = PerformanceClass.INTERACTIVE_DISPATCH


GameEvent = (
    GameStateEvent
    | ClientActionEvent
    | MatchStateEvent
    | DraftBotEvent
    | DraftHumanEvent
    | DraftCompleteEvent
    | EventLifecycleEvent
    | SessionEvent
    | RankEvent
    | CollectionEvent
    | DeckCollectionEvent
    | InventoryEvent
    | GameResultEvent
    | LogFileRotatedEvent
    | DetailedLoggingStatusEvent
    | MatchConnectionStateEvent
    | TcpConnectionCloseEvent
    | WebSocketClosedEvent
    | ConnectionErrorEvent
)
