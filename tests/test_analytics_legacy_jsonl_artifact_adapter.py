from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

import pytest

from mythic_edge_parser.app import state
from mythic_edge_parser.app.analytics_ingest import (
    ingest_parser_normalized_replay,
    normalize_parser_normalized_replay,
)
from mythic_edge_parser.app.analytics_legacy_jsonl_adapter import (
    ANALYTICS_LEGACY_JSONL_ADAPTER_SCHEMA_VERSION,
    ANALYTICS_LEGACY_JSONL_BATCH_IMPORT_SCHEMA_VERSION,
    ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_OBJECT,
    ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION,
    BROWSER_JSONL_UPLOAD_SOURCE_MODE,
    LegacyJsonlAdapterError,
    LegacyJsonlUploadSource,
    adapt_legacy_jsonl_artifacts,
    adapt_legacy_jsonl_file_batch,
    adapt_legacy_jsonl_upload_batch,
)


def _write_jsonl(path: Path, records: list[dict[str, Any] | str | list[Any]]) -> None:
    lines = [record if isinstance(record, str) else json.dumps(record, ensure_ascii=False) for record in records]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _jsonl_bytes(records: list[dict[str, Any] | str | list[Any]]) -> bytes:
    lines = [record if isinstance(record, str) else json.dumps(record, ensure_ascii=False) for record in records]
    return ("\n".join(lines) + "\n").encode("utf-8")


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
    assert ANALYTICS_LEGACY_JSONL_BATCH_IMPORT_SCHEMA_VERSION == "analytics_legacy_jsonl_batch_import.v1"
    assert (
        ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION
        == "analytics_legacy_jsonl_import_quality_breakdown.v1"
    )


def test_supported_generated_jsonl_adapts_to_saved_event_replay_input_and_sqlite(tmp_path: Path) -> None:
    before_artifacts = _local_generated_artifacts()
    jsonl_path = tmp_path / "events_v1_synthetic.jsonl"
    match_id = "match:legacy:adapter"
    records = [
        _match_started(match_id),
        "",
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
    assert result.events_skipped == 4
    assert result.unsupported_kind_counts == {"ConnectionError": 1}
    assert result.warnings == ["derived_match_id_mismatch:legacy_derived_wrong"]
    assert result.quality == {
        "object": ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_OBJECT,
        "schema_version": ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION,
        "quality_status": "degraded",
        "records_seen": 6,
        "events_processed": 3,
        "events_skipped": 4,
        "processed_kind_counts": {"GameResult": 1, "GameState": 1, "MatchState": 1},
        "unsupported_kind_counts": {"ConnectionError": 1},
        "skipped_reason_counts": {
            "blank_line": 1,
            "duplicate_raw_hash": 2,
            "unsupported_kind": 1,
        },
        "blank_line_count": 1,
        "duplicate_raw_hash_count": 2,
        "unsupported_kind_skip_count": 1,
        "output_gap_counts": {
            "incomplete_game_summary": 0,
            "incomplete_match_summary": 0,
            "incomplete_summary_unclassified": 0,
        },
        "adapter_warning_counts": {
            "derived_match_id_mismatch": 1,
            "events_skipped": 1,
            "unsupported_event_kinds": 1,
        },
        "adapter_warning_codes": [
            "derived_match_id_mismatch",
            "events_skipped",
            "unsupported_event_kinds",
        ],
        "ingest_warning_codes": [],
        "routing_hints": [
            {
                "category": "harmless_expected_skip",
                "code": "blank_lines",
                "count": 1,
                "severity": "info",
            },
            {
                "category": "harmless_or_repeated_export",
                "code": "duplicate_raw_hashes",
                "count": 2,
                "severity": "info",
            },
            {
                "category": "parser_or_adapter_backlog",
                "code": "unsupported_event_kinds",
                "count": 1,
                "severity": "warning",
            },
        ],
        "privacy": {
            "has_private_path_echo": False,
            "raw_hash_exposed": False,
            "raw_payload_exposed": False,
        },
    }
    assert "unsupported-consumed-hash" not in json.dumps(result.quality, sort_keys=True)
    assert "final-hash" not in json.dumps(result.quality, sort_keys=True)
    assert "legacy_derived_wrong" not in json.dumps(result.quality, sort_keys=True)

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


def test_explicit_file_batch_sorts_inputs_and_reconstructs_one_replay(tmp_path: Path) -> None:
    first_path = tmp_path / "a_events.jsonl"
    second_path = tmp_path / "b_events.jsonl"
    match_id = "match:legacy:batch"
    _write_jsonl(first_path, [_match_started(match_id), _turn_one(match_id)])
    _write_jsonl(second_path, [_match_finished(match_id)])

    result = adapt_legacy_jsonl_file_batch(
        [second_path, first_path],
        source_artifact_label="legacy_jsonl_explicit_batch_v1",
    )

    assert result.source_mode == "explicit_file_batch"
    assert result.source_artifact_label == "legacy_jsonl_explicit_batch_v1"
    assert result.files_processed == 2
    assert result.files_selected == 2
    assert result.files_accepted == 2
    assert result.files_rejected == 0
    assert result.events_processed == 3
    assert result.events_skipped == 0
    assert result.source_artifacts == [
        {
            "batch_index": 0,
            "source_artifact_label": result.source_artifacts[0]["source_artifact_label"],
            "source_display_label": "a_events.jsonl",
            "status": "processed",
            "records_seen": 2,
            "events_processed": 2,
            "events_skipped": 0,
            "processed_kind_counts": {"GameState": 1, "MatchState": 1},
            "unsupported_kind_counts": {},
            "skipped_reason_counts": {"blank_line": 0, "duplicate_raw_hash": 0, "unsupported_kind": 0},
            "adapter_warning_codes": [],
        },
        {
            "batch_index": 1,
            "source_artifact_label": result.source_artifacts[1]["source_artifact_label"],
            "source_display_label": "b_events.jsonl",
            "status": "processed",
            "records_seen": 1,
            "events_processed": 1,
            "events_skipped": 0,
            "processed_kind_counts": {"GameResult": 1},
            "unsupported_kind_counts": {},
            "skipped_reason_counts": {"blank_line": 0, "duplicate_raw_hash": 0, "unsupported_kind": 0},
            "adapter_warning_codes": [],
        },
    ]
    assert all(
        str(artifact["source_artifact_label"]).startswith("legacy_jsonl_file:")
        for artifact in result.source_artifacts
    )
    assert result.replay["match_log_rows"][0]["match_id"] == match_id  # type: ignore[index]
    assert result.replay["game_log_rows"][0]["match_id"] == match_id  # type: ignore[index]


def test_explicit_file_batch_aggregates_cross_file_duplicate_hashes_without_exposing_raw_hashes(
    tmp_path: Path,
) -> None:
    first_path = tmp_path / "a_events.jsonl"
    second_path = tmp_path / "b_events.jsonl"
    match_id = "match:legacy:batch-degraded"
    _write_jsonl(
        first_path,
        [
            _match_started(match_id),
            _turn_one(match_id),
            _match_finished(match_id, raw_hash="duplicate-final-hash"),
            {
                "kind": "ConnectionError",
                "timestamp": "2026-05-29T18:00:30+00:00",
                "raw_bytes_hash": "unsupported-shared-hash",
                "payload": {"type": "connection_error", "private": "not emitted"},
            },
        ],
    )
    _write_jsonl(
        second_path,
        [
            "",
            {
                "kind": "Rank",
                "timestamp": "2026-05-29T18:00:45+00:00",
                "raw_bytes_hash": "unsupported-shared-hash",
                "payload": {"constructed_class": "Mythic", "constructed_percentile": 99},
            },
            _match_finished(match_id, raw_hash="duplicate-final-hash"),
        ],
    )

    result = adapt_legacy_jsonl_file_batch([second_path, first_path])
    encoded = json.dumps(result.quality | {"source_artifacts": result.source_artifacts}, sort_keys=True)

    assert result.source_mode == "explicit_file_batch"
    assert result.source_artifact_label.startswith("legacy_jsonl_explicit_batch:2:")
    assert result.files_selected == 2
    assert result.records_seen == 6
    assert result.events_processed == 3
    assert result.events_skipped == 4
    assert result.unsupported_kind_counts == {"ConnectionError": 1}
    assert result.quality["skipped_reason_counts"] == {
        "blank_line": 1,
        "duplicate_raw_hash": 2,
        "unsupported_kind": 1,
    }
    assert result.source_artifacts[0]["source_display_label"] == "a_events.jsonl"
    assert result.source_artifacts[0]["status"] == "processed_with_skips"
    assert result.source_artifacts[0]["unsupported_kind_counts"] == {"ConnectionError": 1}
    assert result.source_artifacts[1]["source_display_label"] == "b_events.jsonl"
    assert result.source_artifacts[1]["events_skipped"] == 3
    assert result.source_artifacts[1]["skipped_reason_counts"] == {
        "blank_line": 1,
        "duplicate_raw_hash": 2,
        "unsupported_kind": 0,
    }
    assert "duplicate-final-hash" not in encoded
    assert "unsupported-shared-hash" not in encoded
    assert "not emitted" not in encoded


def test_uploaded_file_batch_sorts_inputs_and_uses_safe_uploaded_source_mode() -> None:
    match_id = "match:legacy:upload"
    first_bytes = _jsonl_bytes([_match_started(match_id), _turn_one(match_id)])
    second_bytes = _jsonl_bytes([_match_finished(match_id)])
    result = adapt_legacy_jsonl_upload_batch(
        [
            LegacyJsonlUploadSource(
                display_name="C:\\fakepath\\b_events.jsonl",
                content_bytes=second_bytes,
                size_bytes=len(second_bytes),
                original_index=0,
            ),
            LegacyJsonlUploadSource(
                display_name="C:\\fakepath\\a_events.jsonl",
                content_bytes=first_bytes,
                size_bytes=len(first_bytes),
                original_index=1,
            ),
        ],
        source_artifact_label="legacy_jsonl_uploaded_batch_v1",
    )
    encoded = json.dumps(result.quality | {"source_artifacts": result.source_artifacts}, sort_keys=True)

    assert result.source_mode == BROWSER_JSONL_UPLOAD_SOURCE_MODE
    assert result.source_artifact_label == "legacy_jsonl_uploaded_batch_v1"
    assert result.files_processed == 2
    assert result.files_selected == 2
    assert result.files_accepted == 2
    assert result.files_rejected == 0
    assert result.events_processed == 3
    assert [artifact["source_display_label"] for artifact in result.source_artifacts] == [
        "a_events.jsonl",
        "b_events.jsonl",
    ]
    assert all(
        str(artifact["source_artifact_label"]).startswith("legacy_jsonl_uploaded_file:")
        for artifact in result.source_artifacts
    )
    assert result.replay["match_log_rows"][0]["match_id"] == match_id  # type: ignore[index]
    assert "fakepath" not in encoded.lower()


def test_uploaded_file_batch_dedupes_cross_file_hashes_without_exposing_hash_or_payload() -> None:
    match_id = "match:legacy:upload-degraded"
    first_bytes = _jsonl_bytes(
        [
            _match_started(match_id),
            _turn_one(match_id),
            _match_finished(match_id, raw_hash="uploaded-duplicate-final-hash"),
            {
                "kind": "ConnectionError",
                "timestamp": "2026-05-29T18:00:30+00:00",
                "raw_bytes_hash": "uploaded-unsupported-shared-hash",
                "payload": {"type": "connection_error", "private": "not emitted"},
            },
        ]
    )
    second_bytes = _jsonl_bytes(
        [
            "",
            {
                "kind": "Rank",
                "timestamp": "2026-05-29T18:00:45+00:00",
                "raw_bytes_hash": "uploaded-unsupported-shared-hash",
                "payload": {"constructed_class": "Mythic", "constructed_percentile": 99},
            },
            _match_finished(match_id, raw_hash="uploaded-duplicate-final-hash"),
        ]
    )

    result = adapt_legacy_jsonl_upload_batch(
        [
            LegacyJsonlUploadSource("b_events.jsonl", second_bytes, len(second_bytes), 0),
            LegacyJsonlUploadSource("a_events.jsonl", first_bytes, len(first_bytes), 1),
        ],
    )
    encoded = json.dumps(result.quality | {"source_artifacts": result.source_artifacts}, sort_keys=True)

    assert result.source_mode == BROWSER_JSONL_UPLOAD_SOURCE_MODE
    assert result.source_artifact_label.startswith("legacy_jsonl_uploaded_batch:2:")
    assert result.records_seen == 6
    assert result.events_processed == 3
    assert result.events_skipped == 4
    assert result.quality["skipped_reason_counts"] == {
        "blank_line": 1,
        "duplicate_raw_hash": 2,
        "unsupported_kind": 1,
    }
    assert result.source_artifacts[0]["source_display_label"] == "a_events.jsonl"
    assert result.source_artifacts[1]["source_display_label"] == "b_events.jsonl"
    assert "uploaded-duplicate-final-hash" not in encoded
    assert "uploaded-unsupported-shared-hash" not in encoded
    assert "not emitted" not in encoded


def test_uploaded_file_batch_malformed_json_fails_without_payload_hash_or_path_echo() -> None:
    raw_hash = "uploaded-private-raw-hash"
    bad_line = f'{{"kind": "GameState", "raw_bytes_hash": "{raw_hash}", "payload": '
    with pytest.raises(LegacyJsonlAdapterError) as exc_info:
        adapt_legacy_jsonl_upload_batch(
            [
                LegacyJsonlUploadSource(
                    display_name="C:\\fakepath\\malformed_events.jsonl",
                    content_bytes=_jsonl_bytes([bad_line]),
                    size_bytes=len(_jsonl_bytes([bad_line])),
                    original_index=0,
                )
            ]
        )

    message = str(exc_info.value)
    assert "Invalid JSON" in message
    assert "malformed_events.jsonl" in message
    assert "fakepath" not in message.lower()
    assert bad_line not in message
    assert "payload" not in message
    assert raw_hash not in message


def test_explicit_file_batch_malformed_selected_file_fails_without_replay_or_private_echo(
    tmp_path: Path,
) -> None:
    first_path = tmp_path / "a_events.jsonl"
    malformed_path = tmp_path / "b_malformed_events.jsonl"
    match_id = "match:legacy:batch-malformed"
    raw_hash = "batch-private-raw-hash"
    bad_line = f'{{"kind": "GameState", "raw_bytes_hash": "{raw_hash}", "payload": '
    _write_jsonl(first_path, [_match_started(match_id), _turn_one(match_id)])
    _write_jsonl(malformed_path, [bad_line])

    with pytest.raises(LegacyJsonlAdapterError) as exc_info:
        adapt_legacy_jsonl_file_batch([first_path, malformed_path])

    message = str(exc_info.value)
    assert "Invalid JSON" in message
    assert state.iter_match_summaries() == []
    assert bad_line not in message
    assert "payload" not in message
    assert raw_hash not in message
    assert str(malformed_path) not in message
    assert malformed_path.as_posix() not in message


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


def test_quality_counts_incomplete_summary_output_gaps_without_inventing_match_game_split(tmp_path: Path) -> None:
    jsonl_path = tmp_path / "events_v1_synthetic.jsonl"
    complete_records = _synthetic_supported_records("match:legacy:complete")
    for record in complete_records:
        record.pop("derived", None)
    incomplete_record = _match_started("match:legacy:incomplete", raw_hash="incomplete-match-started-hash")
    incomplete_record.pop("derived", None)
    _write_jsonl(jsonl_path, [*complete_records, incomplete_record])

    result = adapt_legacy_jsonl_artifacts(jsonl_path)

    assert result.events_processed == 4
    assert result.events_skipped == 0
    assert result.warnings == ["incomplete_match_summaries_skipped:1"]
    assert result.quality["quality_status"] == "degraded"
    assert result.quality["output_gap_counts"] == {
        "incomplete_game_summary": 0,
        "incomplete_match_summary": 0,
        "incomplete_summary_unclassified": 1,
    }
    assert result.quality["adapter_warning_codes"] == ["incomplete_match_summaries_skipped"]
    assert result.quality["routing_hints"] == [
        {
            "category": "analytics_ingest_backlog",
            "code": "incomplete_summaries",
            "count": 1,
            "severity": "warning",
        }
    ]


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
