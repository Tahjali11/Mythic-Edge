from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

import pytest

from mythic_edge_parser.app.analytics_ingest import (
    ingest_parser_normalized_replay,
    normalize_parser_normalized_replay,
)
from mythic_edge_parser.app.analytics_legacy_jsonl_adapter import (
    ANALYTICS_LEGACY_JSONL_ADAPTER_SCHEMA_VERSION,
    LegacyJsonlAdapterError,
    adapt_legacy_jsonl_artifacts,
)


def _write_jsonl(path: Path, records: list[dict[str, Any] | str | list[Any]]) -> None:
    lines = [record if isinstance(record, str) else json.dumps(record, ensure_ascii=False) for record in records]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _match_started(match_id: str, raw_hash: str = "match-started-hash") -> dict[str, Any]:
    return {
        "kind": "MatchState",
        "timestamp": "2026-05-29T18:00:00+00:00",
        "raw_bytes_hash": raw_hash,
        "payload": {
            "type": "match_started",
            "match_id": match_id,
            "event_id": "Constructed_BestOf1",
            "state_type": "MatchGameRoomStateType_Playing",
            "players": [
                {"player_name": "Local", "team_id": 1, "system_seat_id": 1},
                {"player_name": "Opponent", "team_id": 2, "system_seat_id": 2},
            ],
        },
        "derived": {"match_id": "legacy_derived_wrong"},
    }


def _turn_one(match_id: str, raw_hash: str = "turn-one-hash") -> dict[str, Any]:
    return {
        "kind": "GameState",
        "timestamp": "2026-05-29T18:01:00+00:00",
        "raw_bytes_hash": raw_hash,
        "payload": {
            "type": "game_state_message",
            "game_info": {
                "matchID": match_id,
                "gameNumber": 1,
                "superFormat": "SuperFormat_Constructed",
                "matchWinCondition": "MatchWinCondition_SingleGame",
            },
            "raw_game_state": {
                "systemSeatIds": [1],
                "gameStateMessage": {
                    "players": [
                        {"systemSeatNumber": 1, "teamId": 1},
                        {"systemSeatNumber": 2, "teamId": 2},
                    ],
                    "turnInfo": {
                        "turnNumber": 1,
                        "activePlayer": 1,
                    },
                },
            },
        },
    }


def _match_finished(
    match_id: str,
    *,
    winning_team_id: int = 1,
    raw_hash: str = "match-finished-hash",
) -> dict[str, Any]:
    return {
        "kind": "GameResult",
        "timestamp": "2026-05-29T18:08:00+00:00",
        "raw_bytes_hash": raw_hash,
        "payload": {
            "type": "game_result",
            "winning_team_id": winning_team_id,
            "result_type": "ResultType_WinLoss",
            "reason": "ResultReason_Game",
            "match_state": "MatchState_MatchComplete",
            "results": [
                {
                    "scope": "MatchScope_Game",
                    "winningTeamId": winning_team_id,
                    "result": "ResultType_WinLoss",
                    "reason": "ResultReason_Game",
                },
                {
                    "scope": "MatchScope_Match",
                    "winningTeamId": winning_team_id,
                    "result": "ResultType_WinLoss",
                    "reason": "ResultReason_Game",
                },
            ],
            "game_info": {
                "matchID": match_id,
                "gameNumber": 1,
                "superFormat": "SuperFormat_Constructed",
                "matchWinCondition": "MatchWinCondition_SingleGame",
            },
        },
    }


def _synthetic_supported_records(match_id: str = "match:legacy:adapter") -> list[dict[str, Any]]:
    return [
        _match_started(match_id),
        _turn_one(match_id),
        _match_finished(match_id),
    ]


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    return connection


def _local_generated_artifacts() -> set[str]:
    roots_and_patterns = {
        Path("data/analytics"): ("*.db", "*.sqlite", "*.sqlite3", "*.db-journal", "*.db-wal", "*.db-shm"),
        Path("data") / "status": ("*.json",),
        Path("data") / "runtime_logs": ("*.json", "*.jsonl"),
        Path("data") / ("failed_" + "posts"): ("*.json", "*.jsonl"),
    }
    found: set[str] = set()
    for root, patterns in roots_and_patterns.items():
        if not root.exists():
            continue
        for pattern in patterns:
            found.update(str(path) for path in root.rglob(pattern))
    return found


def test_schema_version_constant_is_public() -> None:
    assert ANALYTICS_LEGACY_JSONL_ADAPTER_SCHEMA_VERSION == "analytics_legacy_jsonl_artifact_adapter.v1"


def test_supported_generated_jsonl_adapts_to_saved_event_replay_input_and_sqlite(tmp_path: Path) -> None:
    before_artifacts = _local_generated_artifacts()
    jsonl_path = tmp_path / "events_v1_synthetic.jsonl"
    match_id = "match:legacy:adapter"
    records = [
        _match_started(match_id),
        {
            "kind": "ConnectionError",
            "timestamp": "2026-05-29T18:00:30+00:00",
            "raw_bytes_hash": "unsupported-consumed-hash",
            "payload": {"type": "connection_error", "private": "not emitted"},
        },
        {
            "kind": "Rank",
            "timestamp": "2026-05-29T18:00:45+00:00",
            "raw_bytes_hash": "unsupported-consumed-hash",
            "payload": {"constructed_class": "Mythic", "constructed_percentile": 99},
        },
        _turn_one(match_id),
        _match_finished(match_id, winning_team_id=1, raw_hash="final-hash"),
        _match_finished(match_id, winning_team_id=2, raw_hash="final-hash"),
    ]
    _write_jsonl(jsonl_path, records)

    result = adapt_legacy_jsonl_artifacts(
        jsonl_path,
        source_artifact_label="legacy_jsonl_saved_event_replay_v1",
    )

    assert result.source_kind == "saved_event_replay"
    assert result.source_artifact_label == "legacy_jsonl_saved_event_replay_v1"
    assert result.files_processed == 1
    assert result.records_seen == 6
    assert result.events_processed == 3
    assert result.events_skipped == 3
    assert result.unsupported_kind_counts == {"ConnectionError": 1}
    assert result.warnings == ["derived_match_id_mismatch:legacy_derived_wrong"]

    replay = result.replay
    normalized = normalize_parser_normalized_replay(replay)
    assert normalized.source_kind == "saved_event_replay"
    assert normalized.source_artifact_label == "legacy_jsonl_saved_event_replay_v1"
    assert normalized.gameplay_action_entries == ()
    assert normalized.opponent_card_observations == ()
    assert normalized.field_evidence_entries == ()

    assert len(normalized.match_log_rows) == 1
    assert len(normalized.game_log_rows) == 1
    match_row = normalized.match_log_rows[0]
    game_row = normalized.game_log_rows[0]
    assert match_row["match_id"] == match_id
    assert match_row["MTGA Match ID"] == match_id
    assert match_row["Match Win?"] == "W"
    assert match_row["MTGA Format"] == "Constructed"
    assert match_row["MTGA Queue Type"] == "Best of 1"
    assert "legacy_derived_wrong" not in json.dumps(replay, sort_keys=True)
    assert game_row["match_id"] == match_id
    assert game_row["Game Number"] == 1
    assert game_row["Game Result"] == "W"
    assert game_row["Play / Draw"] == "Play"

    ingest_result = ingest_parser_normalized_replay(
        _connect(),
        replay,
        started_at="2026-05-29T18:00:00+00:00",
        finished_at="2026-05-29T18:09:00+00:00",
    )
    assert ingest_result.status == "completed"
    assert ingest_result.source_kind == "saved_event_replay"
    assert ingest_result.row_counts["matches"] == 1
    assert ingest_result.row_counts["games"] == 1
    assert _local_generated_artifacts() == before_artifacts


def test_directory_input_uses_latest_saved_event_selection_semantics(tmp_path: Path) -> None:
    match_id = "match:legacy:folder"
    day_dir = tmp_path / "2026_05_29"
    day_dir.mkdir()
    _write_jsonl(day_dir / "match-events_v1_old.jsonl", ["{not-json}"])
    _write_jsonl(day_dir / "match-events_v2_new.jsonl", _synthetic_supported_records(match_id))

    result = adapt_legacy_jsonl_artifacts(tmp_path)

    assert result.files_processed == 1
    assert result.source_artifact_label.startswith("legacy_jsonl_bundle:")
    assert result.replay["match_log_rows"][0]["match_id"] == match_id  # type: ignore[index]


def test_unsafe_source_artifact_label_fails(tmp_path: Path) -> None:
    jsonl_path = tmp_path / "events_v1_synthetic.jsonl"
    _write_jsonl(jsonl_path, _synthetic_supported_records())
    private_label = "C:" + "\\Users\\private\\" + "Player" + ".log"

    with pytest.raises(LegacyJsonlAdapterError, match="safe label"):
        adapt_legacy_jsonl_artifacts(jsonl_path, source_artifact_label=private_label)


def test_invalid_json_fails_without_echoing_raw_line(tmp_path: Path) -> None:
    jsonl_path = tmp_path / "events_v1_synthetic.jsonl"
    bad_line = '{"kind": "Rank", "payload": '
    _write_jsonl(jsonl_path, [bad_line])

    with pytest.raises(LegacyJsonlAdapterError) as exc_info:
        adapt_legacy_jsonl_artifacts(jsonl_path)

    message = str(exc_info.value)
    assert "Invalid JSON" in message
    assert bad_line not in message
    assert "payload" not in message


def test_non_object_jsonl_record_fails_clearly(tmp_path: Path) -> None:
    jsonl_path = tmp_path / "events_v1_synthetic.jsonl"
    _write_jsonl(jsonl_path, [["not", "an", "object"]])

    with pytest.raises(LegacyJsonlAdapterError, match="must be an object"):
        adapt_legacy_jsonl_artifacts(jsonl_path)


def test_malformed_supported_event_record_fails_clearly_without_payload_dump(tmp_path: Path) -> None:
    jsonl_path = tmp_path / "events_v1_synthetic.jsonl"
    _write_jsonl(
        jsonl_path,
        [
            {
                "kind": "Rank",
                "timestamp": "2026-05-29T18:00:00+00:00",
                "raw_bytes_hash": "bad-rank-hash",
                "payload": "not-a-mapping",
            }
        ],
    )

    with pytest.raises(LegacyJsonlAdapterError) as exc_info:
        adapt_legacy_jsonl_artifacts(jsonl_path)

    message = str(exc_info.value)
    assert "Malformed saved event record for kind Rank" in message
    assert "not-a-mapping" not in message


def test_no_ingestable_rows_fails_clearly(tmp_path: Path) -> None:
    jsonl_path = tmp_path / "events_v1_synthetic.jsonl"
    _write_jsonl(
        jsonl_path,
        [
            {
                "kind": "Rank",
                "timestamp": "2026-05-29T18:00:00+00:00",
                "raw_bytes_hash": "rank-only-hash",
                "payload": {"constructed_class": "Diamond", "constructed_level": 2},
            }
        ],
    )

    with pytest.raises(LegacyJsonlAdapterError, match="no ingestable parser-normalized match/game rows"):
        adapt_legacy_jsonl_artifacts(jsonl_path)
