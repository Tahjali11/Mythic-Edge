# ruff: noqa: I001
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from mythic_edge_parser.app import state  # noqa: E402
from mythic_edge_parser.app.config import MATCH_HISTORY_PATH, MATCH_LOGS_ROOT  # noqa: E402
from mythic_edge_parser.app.runtime_surfaces import (  # noqa: E402
    observe_event as observe_runtime_surface_event,
    refresh_match_history_snapshot,
    reset_runtime_surface_state,
)
from mythic_edge_parser.app.saved_event_replay import replay_latest_saved_events  # noqa: E402


@dataclass(slots=True)
class HistoryRefreshStats:
    files_processed: int = 0
    events_processed: int = 0
    events_skipped: int = 0
    matches_written: int = 0


def _reset_replay_state() -> None:
    state.reset_runtime_state()
    reset_runtime_surface_state()


def _observe_replayed_event(event: object) -> None:
    state._update_match_summary(event)
    observe_runtime_surface_event(event, include_in_timeline=False)


def refresh_history_from_saved_match_logs(match_logs_root: Path) -> tuple[dict[str, object], HistoryRefreshStats]:
    _reset_replay_state()
    replay_stats = replay_latest_saved_events(match_logs_root, _observe_replayed_event)
    payload = refresh_match_history_snapshot()
    return (
        payload,
        HistoryRefreshStats(
            files_processed=replay_stats.files_processed,
            events_processed=replay_stats.events_processed,
            events_skipped=replay_stats.events_skipped,
            matches_written=int(payload.get("total_matches", 0) or 0),
        ),
    )


def main() -> None:
    payload, stats = refresh_history_from_saved_match_logs(MATCH_LOGS_ROOT)

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Match logs root: {MATCH_LOGS_ROOT}")
    print(f"Match history path: {MATCH_HISTORY_PATH}")
    print(f"Latest daily files processed: {stats.files_processed}")
    print(f"Unique events processed: {stats.events_processed}")
    print(f"Skipped events: {stats.events_skipped}")
    print(f"Matches written: {stats.matches_written}")

    matches = payload.get("matches") or []
    if isinstance(matches, list) and matches:
        print("Newest reconstructed matches:")
        for item in matches[:5]:
            if not isinstance(item, dict):
                continue
            print(
                json.dumps(
                    {
                        "match_id": item.get("match_id"),
                        "date": item.get("date"),
                        "event_id": item.get("event_id"),
                        "queue_type": item.get("mtga_queue_type"),
                        "rank_match_type": item.get("rank_match_type"),
                        "play_mode_family": item.get("play_mode_family"),
                        "event_family": item.get("event_family"),
                        "queue_subtype": item.get("queue_subtype"),
                    },
                    ensure_ascii=False,
                )
            )


if __name__ == "__main__":
    main()
