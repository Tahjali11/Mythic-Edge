from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from ..events import (
    BaseEvent,
    ClientActionEvent,
    ConnectionErrorEvent,
    DeckCollectionEvent,
    DetailedLoggingStatusEvent,
    EventLifecycleEvent,
    EventMetadata,
    GameResultEvent,
    GameStateEvent,
    MatchConnectionStateEvent,
    MatchStateEvent,
    RankEvent,
    TcpConnectionCloseEvent,
    WebSocketClosedEvent,
)

_LATEST_JSONL_RE = re.compile(r"_v(?P<version>\d+)_")

EVENT_CLASS_BY_KIND: dict[str, type[BaseEvent]] = {
    "ClientAction": ClientActionEvent,
    "DetailedLoggingStatus": DetailedLoggingStatusEvent,
    "EventLifecycle": EventLifecycleEvent,
    "GameResult": GameResultEvent,
    "GameState": GameStateEvent,
    "MatchConnectionState": MatchConnectionStateEvent,
    "MatchState": MatchStateEvent,
    "Rank": RankEvent,
    "TcpConnectionClose": TcpConnectionCloseEvent,
    "DeckCollection": DeckCollectionEvent,
    "WebSocketClosed": WebSocketClosedEvent,
    "ConnectionError": ConnectionErrorEvent,
}


@dataclass(slots=True)
class ReplayStats:
    files_processed: int = 0
    events_processed: int = 0
    events_skipped: int = 0


def latest_jsonl_files(root: Path) -> list[Path]:
    by_day: dict[Path, tuple[int, Path]] = {}
    for path in root.rglob("*.jsonl"):
        match = _LATEST_JSONL_RE.search(path.name)
        version = int(match.group("version")) if match else -1
        day_dir = path.parent
        current = by_day.get(day_dir)
        if current is None or version > current[0]:
            by_day[day_dir] = (version, path)
    return [entry[1] for entry in sorted(by_day.values(), key=lambda item: item[1].parent.name)]


def _parse_timestamp(value: Any) -> datetime | None:
    if not value:
        return None
    text = str(value).strip()
    if not text:
        return None
    return datetime.fromisoformat(text)


def event_from_saved_record(raw_line: str, payload: dict[str, Any]) -> Any | None:
    kind = payload.get("kind")
    if not isinstance(kind, str):
        return None
    event_class = EVENT_CLASS_BY_KIND.get(kind)
    if event_class is None:
        return None
    event_payload = payload.get("payload", {})
    metadata = EventMetadata(
        timestamp=_parse_timestamp(payload.get("timestamp")),
        raw_bytes=raw_line.encode("utf-8", errors="ignore"),
    )
    return event_class(metadata, event_payload)


def replay_latest_saved_events(root: Path, on_event: Callable[[Any], None]) -> ReplayStats:
    stats = ReplayStats()
    seen_raw_hashes: set[str] = set()

    for path in latest_jsonl_files(root):
        stats.files_processed += 1
        with path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line:
                    continue
                record = json.loads(line)
                raw_hash = str(record.get("raw_bytes_hash") or "").strip()
                if raw_hash and raw_hash in seen_raw_hashes:
                    stats.events_skipped += 1
                    continue
                if raw_hash:
                    seen_raw_hashes.add(raw_hash)

                event = event_from_saved_record(line, record)
                if event is None:
                    stats.events_skipped += 1
                    continue

                on_event(event)
                stats.events_processed += 1

    return stats
