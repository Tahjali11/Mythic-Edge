import json
from datetime import UTC, datetime
from pathlib import Path

from mythic_edge_parser.app.saved_event_replay import (
    event_from_saved_record,
    latest_jsonl_files,
    replay_latest_saved_events,
)


def test_latest_jsonl_files_selects_highest_version_per_day(tmp_path: Path) -> None:
    day_one = tmp_path / "2026_05_09"
    day_two = tmp_path / "2026_05_10"
    day_one.mkdir()
    day_two.mkdir()

    older = day_one / "match-events_v1_sample.jsonl"
    newer = day_one / "match-events_v2_sample.jsonl"
    other = day_two / "match-events_v1_other.jsonl"
    older.write_text("", encoding="utf-8")
    newer.write_text("", encoding="utf-8")
    other.write_text("", encoding="utf-8")

    assert latest_jsonl_files(tmp_path) == [newer, other]


def test_replay_latest_saved_events_dedupes_raw_hashes_and_reconstructs_events(tmp_path: Path) -> None:
    day_dir = tmp_path / "2026_05_10"
    day_dir.mkdir()
    jsonl_path = day_dir / "match-events_v3_sample.jsonl"
    records = [
        {
            "kind": "Rank",
            "timestamp": "2026-05-10T17:00:00+00:00",
            "raw_bytes_hash": "same-hash",
            "payload": {
                "constructed_class": "Diamond",
                "constructed_level": 2,
                "constructed_percentile": "",
            },
        },
        {
            "kind": "Rank",
            "timestamp": "2026-05-10T17:00:00+00:00",
            "raw_bytes_hash": "same-hash",
            "payload": {
                "constructed_class": "Diamond",
                "constructed_level": 2,
                "constructed_percentile": "",
            },
        },
        {
            "kind": "MatchState",
            "timestamp": "2026-05-10T17:01:00+00:00",
            "raw_bytes_hash": "other-hash",
            "payload": {
                "type": "match_started",
                "match_id": "match-replay-1",
                "state_type": "MatchGameRoomStateType_Playing",
                "players": [
                    {"player_name": "Local", "team_id": 1, "system_seat_id": 1},
                    {"player_name": "Opponent", "team_id": 2, "system_seat_id": 2},
                ],
            },
        },
    ]
    jsonl_path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )

    seen: list[tuple[str, datetime | None]] = []
    stats = replay_latest_saved_events(
        tmp_path,
        lambda event: seen.append((getattr(event, "kind", ""), getattr(event.metadata, "timestamp", None))),
    )

    assert stats.files_processed == 1
    assert stats.events_processed == 2
    assert stats.events_skipped == 1
    assert [kind for kind, _timestamp in seen] == ["Rank", "MatchState"]
    assert seen[0][1] == datetime(2026, 5, 10, 17, 0, 0, tzinfo=UTC)


def test_event_lifecycle_saved_record_reconstructs_event() -> None:
    record = {
        "kind": "EventLifecycle",
        "timestamp": "2026-05-10T17:02:00+00:00",
        "payload": {
            "type": "event_join",
            "raw_event_lifecycle": "==> EventJoin",
        },
    }
    raw_line = json.dumps(record)

    event = event_from_saved_record(raw_line, record)

    assert event is not None
    assert event.kind == "EventLifecycle"
    assert event.metadata.timestamp == datetime(2026, 5, 10, 17, 2, 0, tzinfo=UTC)
    assert event.metadata.raw_bytes == raw_line.encode()
    assert event.payload == {
        "type": "event_join",
        "raw_event_lifecycle": "==> EventJoin",
    }
