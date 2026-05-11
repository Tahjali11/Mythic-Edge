from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from mythic_edge_parser.app import state  # noqa: E402
from mythic_edge_parser.app.config import MATCH_LOGS_ROOT, WEBHOOK_URL  # noqa: E402
from mythic_edge_parser.app.saved_event_replay import replay_latest_saved_events  # noqa: E402


@dataclass(slots=True)
class BackfillStats:
    files_processed: int = 0
    events_processed: int = 0
    events_skipped: int = 0
    game_rows_posted: int = 0
    game_rows_failed: int = 0


def _ingest_latest_logs(root: Path, stats: BackfillStats) -> None:
    replay_stats = replay_latest_saved_events(root, state._update_match_summary)
    stats.files_processed = replay_stats.files_processed
    stats.events_processed = replay_stats.events_processed
    stats.events_skipped = replay_stats.events_skipped


def _game_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for match_id in sorted(state._MATCH_SUMMARIES):
        summary = state._MATCH_SUMMARIES[match_id]
        for row in summary.to_game_sheet_rows():
            if str(row.get("Game Result", "")).strip() == "":
                continue
            rows.append(row)
    rows.sort(
        key=lambda row: (
            str(row.get("Date", "")),
            str(row.get("MTGA Match ID", "")),
            int(row.get("Game Number", 0)),
        )
    )
    return rows


def _launcher_webhook(project_root: Path) -> str:
    settings_paths = (
        Path.home() / ".mythic_edge_launcher_settings.json",
        Path.home() / ".manasight_launcher_settings.json",
    )
    for settings_path in settings_paths:
        if not settings_path.exists():
            continue
        try:
            payload = json.loads(settings_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        return str(payload.get("webhook_url") or WEBHOOK_URL)
    return WEBHOOK_URL


def _post_rows(rows: list[dict[str, Any]], webhook_url: str, stats: BackfillStats) -> None:
    session = requests.Session()
    for row in rows:
        match_id = row.get("MTGA Match ID")
        game_number = row.get("Game Number")
        response = None
        error_message = ""

        for attempt in range(1, 4):
            try:
                response = session.post(webhook_url, json=row, timeout=30)
                if response.ok:
                    stats.game_rows_posted += 1
                    break

                error_message = f"{response.status_code} {response.text[:200]}"
            except requests.RequestException as exc:
                error_message = str(exc)

            if attempt < 3:
                wait_seconds = attempt
                print(
                    f"Retrying POST for match={match_id} game={game_number} after attempt {attempt} failed: "
                    f"{error_message}"
                )
                time.sleep(wait_seconds)

        else:
            stats.game_rows_failed += 1
            print(f"POST failed for match={match_id} game={game_number}: {error_message}")

        time.sleep(0.1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill MTGA Game Log rows from saved match_logs JSONL files.")
    parser.add_argument("--dry-run", action="store_true", help="Parse logs and print summary without posting rows.")
    parser.add_argument("--webhook", default="", help="Override the Google Apps Script webhook URL.")
    args = parser.parse_args()

    stats = BackfillStats()
    state.reset_runtime_state()
    _ingest_latest_logs(MATCH_LOGS_ROOT, stats)
    rows = _game_rows()

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Match logs root: {MATCH_LOGS_ROOT}")
    print(f"Latest daily files processed: {stats.files_processed}")
    print(f"Unique events processed: {stats.events_processed}")
    print(f"Skipped events: {stats.events_skipped}")
    print(f"Completed game rows reconstructed: {len(rows)}")

    if rows:
        print("Sample rows:")
        for row in rows[:5]:
            print(
                json.dumps(
                    {
                        "match_id": row.get("MTGA Match ID"),
                        "game_number": row.get("Game Number"),
                        "play_draw": row.get("Play / Draw"),
                        "mulligans": row.get("Mulligans"),
                        "result": row.get("Game Result"),
                        "turn_count": row.get("Turn Count"),
                        "format": row.get("MTGA Format"),
                        "event_id": row.get("MTGA Event ID"),
                        "queue_type": row.get("MTGA Queue Type"),
                    },
                    ensure_ascii=False,
                )
            )

    if args.dry_run:
        return

    webhook_url = args.webhook.strip() or _launcher_webhook(PROJECT_ROOT)
    if not webhook_url:
        raise SystemExit("No webhook URL available. Pass --webhook or configure the launcher webhook.")

    print(f"Posting {len(rows)} GameLogRow payloads to {webhook_url}")
    _post_rows(rows, webhook_url, stats)
    print(f"Posted rows: {stats.game_rows_posted}")
    print(f"Failed rows: {stats.game_rows_failed}")


if __name__ == "__main__":
    main()
