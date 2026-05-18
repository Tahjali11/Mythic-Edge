import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from mythic_edge_parser.app.saved_event_replay import (
    EVENT_CLASS_BY_KIND,
    event_from_saved_record,
    latest_jsonl_files,
    replay_latest_saved_events,
)

SUPPORTED_REPLAY_KINDS = {
    "ClientAction",
    "DetailedLoggingStatus",
    "EventLifecycle",
    "GameResult",
    "GameState",
    "MatchState",
    "Rank",
    "Truncation",
}


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


def test_latest_jsonl_files_treats_unversioned_files_as_lower_than_versioned(tmp_path: Path) -> None:
    day_one = tmp_path / "2026_05_09"
    day_two = tmp_path / "2026_05_10"
    day_one.mkdir()
    day_two.mkdir()

    unversioned = day_one / "match-events_sample.jsonl"
    versioned = day_one / "match-events_v0_sample.jsonl"
    only_unversioned = day_two / "match-events_sample.jsonl"
    unversioned.write_text("", encoding="utf-8")
    versioned.write_text("", encoding="utf-8")
    only_unversioned.write_text("", encoding="utf-8")

    assert latest_jsonl_files(tmp_path) == [versioned, only_unversioned]


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


def test_replay_latest_saved_events_dedupes_raw_hashes_across_selected_files(tmp_path: Path) -> None:
    day_one = tmp_path / "2026_05_10"
    day_two = tmp_path / "2026_05_11"
    day_one.mkdir()
    day_two.mkdir()
    (day_one / "match-events_v1_a.jsonl").write_text(
        json.dumps(
            {
                "kind": "Rank",
                "timestamp": "2026-05-10T17:00:00+00:00",
                "raw_bytes_hash": "global-hash",
                "payload": {},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (day_two / "match-events_v1_b.jsonl").write_text(
        "\n".join(
            json.dumps(record)
            for record in [
                {
                    "kind": "MatchState",
                    "timestamp": "2026-05-11T17:00:00+00:00",
                    "raw_bytes_hash": "global-hash",
                    "payload": {},
                },
                {
                    "kind": "DetailedLoggingStatus",
                    "timestamp": "2026-05-11T17:01:00+00:00",
                    "raw_bytes_hash": "   ",
                    "payload": {},
                },
                {
                    "kind": "EventLifecycle",
                    "timestamp": "2026-05-11T17:02:00+00:00",
                    "payload": {},
                },
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    seen: list[str] = []
    stats = replay_latest_saved_events(tmp_path, lambda event: seen.append(event.kind))

    assert stats.files_processed == 2
    assert stats.events_processed == 3
    assert stats.events_skipped == 1
    assert seen == ["Rank", "DetailedLoggingStatus", "EventLifecycle"]


def test_replay_latest_saved_events_skips_unknown_kind_and_ignores_blank_lines(tmp_path: Path) -> None:
    day_dir = tmp_path / "2026_05_10"
    day_dir.mkdir()
    jsonl_path = day_dir / "match-events_v1_sample.jsonl"
    jsonl_path.write_text(
        "\n"
        + json.dumps({"kind": "Collection", "timestamp": "2026-05-10T17:00:00+00:00", "payload": {}})
        + "\n\n"
        + json.dumps({"kind": "Rank", "timestamp": "2026-05-10T17:01:00+00:00", "payload": {}})
        + "\n",
        encoding="utf-8",
    )

    seen: list[str] = []
    stats = replay_latest_saved_events(tmp_path, lambda event: seen.append(event.kind))

    assert stats.files_processed == 1
    assert stats.events_processed == 1
    assert stats.events_skipped == 1
    assert seen == ["Rank"]


def test_replay_latest_saved_events_consumes_hash_before_unknown_kind_skip(tmp_path: Path) -> None:
    day_dir = tmp_path / "2026_05_10"
    day_dir.mkdir()
    jsonl_path = day_dir / "match-events_v1_sample.jsonl"
    records = [
        {
            "kind": "Collection",
            "timestamp": "2026-05-10T17:00:00+00:00",
            "raw_bytes_hash": "consumed-hash",
            "payload": {},
        },
        {
            "kind": "Rank",
            "timestamp": "2026-05-10T17:01:00+00:00",
            "raw_bytes_hash": "consumed-hash",
            "payload": {},
        },
    ]
    jsonl_path.write_text(
        "\n".join(json.dumps(record) for record in records) + "\n",
        encoding="utf-8",
    )

    seen: list[str] = []
    stats = replay_latest_saved_events(tmp_path, lambda event: seen.append(event.kind))

    assert stats.events_processed == 0
    assert stats.events_skipped == 2
    assert seen == []


def test_replay_latest_saved_events_propagates_callback_exceptions(tmp_path: Path) -> None:
    day_dir = tmp_path / "2026_05_10"
    day_dir.mkdir()
    jsonl_path = day_dir / "match-events_v1_sample.jsonl"
    jsonl_path.write_text(
        json.dumps({"kind": "Rank", "timestamp": "2026-05-10T17:00:00+00:00", "payload": {}})
        + "\n",
        encoding="utf-8",
    )

    def failing_callback(event) -> None:
        assert event.kind == "Rank"
        raise RuntimeError("callback failed")

    with pytest.raises(RuntimeError, match="callback failed"):
        replay_latest_saved_events(tmp_path, failing_callback)


def test_replay_latest_saved_events_invalid_json_fails_fast(tmp_path: Path) -> None:
    day_dir = tmp_path / "2026_05_10"
    day_dir.mkdir()
    jsonl_path = day_dir / "match-events_v1_sample.jsonl"
    jsonl_path.write_text("{not-json}\n", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        replay_latest_saved_events(tmp_path, lambda _event: None)


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
    assert event.metadata.raw_bytes_hash == hashlib.sha256(raw_line.encode()).hexdigest()
    assert event.payload == {
        "type": "event_join",
        "raw_event_lifecycle": "==> EventJoin",
    }


def test_truncation_saved_record_reconstructs_event() -> None:
    record = {
        "kind": "Truncation",
        "timestamp": "2026-05-10T17:02:00+00:00",
        "payload": {
            "type": "game_state_message_truncation",
            "data_loss": True,
            "recoverable": False,
        },
    }
    raw_line = json.dumps(record)

    event = event_from_saved_record(raw_line, record)

    assert event is not None
    assert event.kind == "Truncation"
    assert event.metadata.timestamp == datetime(2026, 5, 10, 17, 2, 0, tzinfo=UTC)
    assert event.metadata.raw_bytes_hash == hashlib.sha256(raw_line.encode()).hexdigest()
    assert event.payload["type"] == "game_state_message_truncation"


def test_replay_event_kind_mapping_contains_exact_supported_kinds() -> None:
    assert set(EVENT_CLASS_BY_KIND) == SUPPORTED_REPLAY_KINDS

    for unsupported_kind in ("rank", " Rank", "Rank ", "Collection", "Inventory", "", None):
        record = {"kind": unsupported_kind, "timestamp": "2026-05-10T17:00:00+00:00", "payload": {}}

        assert event_from_saved_record(json.dumps(record), record) is None


@pytest.mark.parametrize("kind", sorted(SUPPORTED_REPLAY_KINDS))
def test_supported_saved_record_kinds_reconstruct_events(kind: str) -> None:
    record = {
        "kind": kind,
        "timestamp": "",
        "payload": {},
    }
    raw_line = json.dumps(record)

    event = event_from_saved_record(raw_line, record)

    assert event is not None
    assert event.kind == kind
    assert event.metadata.timestamp is None
    assert event.metadata.raw_bytes == raw_line.encode()
    assert event.payload == {}


def test_missing_saved_record_payload_defaults_to_empty_payload() -> None:
    record = {
        "kind": "Rank",
        "timestamp": "2026-05-10T17:00:00+00:00",
    }

    event = event_from_saved_record(json.dumps(record), record)

    assert event is not None
    assert event.payload == {}


def test_present_malformed_saved_record_payload_fails_fast() -> None:
    record = {
        "kind": "Rank",
        "timestamp": "2026-05-10T17:00:00+00:00",
        "payload": "not-a-mapping",
    }

    with pytest.raises(ValueError):
        event_from_saved_record(json.dumps(record), record)


@pytest.mark.parametrize("timestamp", [None, "", "   ", 0])
def test_saved_record_falsey_or_blank_timestamp_reconstructs_as_none(timestamp) -> None:
    record = {
        "kind": "Rank",
        "timestamp": timestamp,
        "payload": {},
    }

    event = event_from_saved_record(json.dumps(record), record)

    assert event is not None
    assert event.metadata.timestamp is None


def test_saved_record_invalid_nonblank_timestamp_fails_fast() -> None:
    record = {
        "kind": "Rank",
        "timestamp": "not-a-timestamp",
        "payload": {},
    }

    with pytest.raises(ValueError):
        event_from_saved_record(json.dumps(record), record)
