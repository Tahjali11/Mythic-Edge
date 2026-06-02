from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from mythic_edge_parser.app.analytics_ingest import (
    LIVE_PARSER_OWNED_FACT_CAPTURE_SCHEMA_VERSION,
    AnalyticsReplayIngestError,
    ingest_live_parser_owned_facts,
    ingest_parser_normalized_replay,
    normalize_parser_normalized_replay,
)


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    return connection


def _match_row(*, match_id: str = "match:live:001", sync_status: str = "Final") -> dict[str, object]:
    return {
        "event_family": "MatchLogRow",
        "event_type": "match_log_row",
        "scope": "Match",
        "match_id": match_id,
        "timestamp": "2026-06-02T12:30:00+00:00",
        "MTGA Match ID": match_id,
        "Match Win?": "W",
        "Match Win Flag": 1,
        "Games Won": 1,
        "Games Lost": 0,
        "Total Games": 1,
        "Game Win %": 1.0,
        "MTGA Format": "Constructed",
        "MTGA Event ID": "Play_BestOf1",
        "MTGA Queue Type": "Best of 1",
        "MTGA Rank Raw": "Gold_Tier2",
        "My Rank": "Gold",
        "MGTA Start Time": "2026-06-02T12:00:00+00:00",
        "MTGA End Time": "2026-06-02T12:30:00+00:00",
        "MTGA Sync Status": sync_status,
        "MTGA Sideboard Entered": "No",
        "MTGA Submit Deck Seen": "No",
        "G1 Mulligans": 1,
        "G1 Play / Draw": "Play",
        "G1 Turn Count": 8,
        "Game 1 Result": "W",
    }


def _game_row(*, match_id: str = "match:live:001") -> dict[str, object]:
    return {
        "event_family": "GameLogRow",
        "event_type": "game_log_row",
        "scope": "Game",
        "match_id": match_id,
        "timestamp": "2026-06-02T12:30:00+00:00",
        "MTGA Match ID": match_id,
        "Game Number": 1,
        "Pre / Postboard": "Preboard",
        "Play / Draw": "Play",
        "Mulligans": 1,
        "Opening Hand Size": 7,
        "Opening Hand": "Forest; Swamp; Mosswood Dreadknight",
        "Mulliganed Away": "Llanowar Elves",
        "Game Result": "W",
        "Turn Count": 8,
        "Game Duration": 1800,
        "MTGA Format": "Constructed",
        "MTGA Event ID": "Play_BestOf1",
        "MTGA Queue Type": "Best of 1",
    }


def _live_payload(*, match_id: str = "match:live:001", sync_status: str = "Final") -> dict[str, object]:
    return {
        "source_kind": "live_parser",
        "source_artifact_label": "live_parser_session",
        "session_id": "live-session-001",
        "parser_version": "test-parser-version",
        "capture_started_at": "2026-06-02T12:00:00+00:00",
        "capture_finished_at": "2026-06-02T12:31:00+00:00",
        "match_log_rows": [_match_row(match_id=match_id, sync_status=sync_status)],
        "game_log_rows": [_game_row(match_id=match_id)],
    }


def _replay_payload(match_id: str = "match:live:001") -> dict[str, object]:
    payload = _live_payload(match_id=match_id)
    payload["source_kind"] = "sanitized_golden_replay"
    payload["source_artifact_label"] = "parser_regression_match_bo1_v1"
    payload.pop("session_id")
    payload.pop("capture_started_at")
    payload.pop("capture_finished_at")
    payload["generated_at"] = "2026-06-02T12:31:00+00:00"
    return payload


def _count(connection: sqlite3.Connection, table_name: str) -> int:
    return int(connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0])


def _count_if_table_exists(connection: sqlite3.Connection, table_name: str) -> int:
    row = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    if row is None:
        return 0
    return _count(connection, table_name)


def _assert_live_ingest_error_without_partial_fact_rows(payload: dict[str, object], match: str) -> None:
    connection = _connect()

    with pytest.raises(AnalyticsReplayIngestError, match=match):
        ingest_live_parser_owned_facts(connection, payload)

    assert _count_if_table_exists(connection, "ingest_runs") == 0
    assert _count_if_table_exists(connection, "matches") == 0
    assert _count_if_table_exists(connection, "games") == 0


def _sqlite_artifacts() -> set[str]:
    root = Path("data/analytics")
    if not root.exists():
        return set()
    patterns = ("*.db", "*.sqlite", "*.sqlite3", "*.db-journal", "*.db-wal", "*.db-shm")
    found: set[str] = set()
    for pattern in patterns:
        found.update(str(path) for path in root.glob(pattern))
    return found


def test_live_schema_version_constant_is_public() -> None:
    assert LIVE_PARSER_OWNED_FACT_CAPTURE_SCHEMA_VERSION == "live_app_parser_owned_fact_capture_sqlite.v1"


def test_live_parser_source_kind_is_accepted_only_by_live_adapter() -> None:
    replay_shape = _live_payload()

    with pytest.raises(AnalyticsReplayIngestError, match="Unsupported"):
        normalize_parser_normalized_replay(replay_shape)

    connection = _connect()
    result = ingest_live_parser_owned_facts(connection, replay_shape)

    assert result.status == "completed"
    assert result.source_kind == "live_parser"
    assert result.source_artifact_label == "live_parser_session"
    assert _count(connection, "ingest_runs") == 1


def test_live_adapter_writes_final_match_and_game_facts_to_existing_tables() -> None:
    connection = _connect()

    result = ingest_live_parser_owned_facts(connection, _live_payload())

    run = connection.execute("SELECT source_kind, source_artifact_label FROM ingest_runs").fetchone()
    match = connection.execute("SELECT session_id, finality FROM matches").fetchone()
    game = connection.execute("SELECT finality FROM games").fetchone()
    encoded_provenance = json.dumps(
        [dict(row) for row in connection.execute("SELECT source_payload_paths FROM fact_provenance").fetchall()],
        sort_keys=True,
    )

    assert run["source_kind"] == "live_parser"
    assert run["source_artifact_label"] == "live_parser_session"
    assert match["session_id"] is None
    assert match["finality"] == "reconciled"
    assert game["finality"] == "final"
    assert _count(connection, "matches") == 1
    assert _count(connection, "games") == 1
    assert _count(connection, "match_results") == 1
    assert _count(connection, "game_results") == 1
    assert _count(connection, "opening_hands") == 1
    assert _count(connection, "mulligan_events") == 1
    assert _count(connection, "gameplay_actions") == 0
    assert _count(connection, "opponent_card_observations") == 0
    assert result.warnings == []
    assert "Player.log" not in encoded_provenance
    assert ":\\" not in encoded_provenance
    assert "http" not in encoded_provenance


def test_live_adapter_is_idempotent_and_does_not_duplicate_replay_facts() -> None:
    connection = _connect()
    payload = _live_payload()

    first = ingest_live_parser_owned_facts(connection, payload)
    second = ingest_live_parser_owned_facts(connection, payload)

    assert second.ingest_run_id == first.ingest_run_id
    assert _count(connection, "ingest_runs") == 1
    assert _count(connection, "matches") == 1
    assert _count(connection, "games") == 1
    assert _count(connection, "fact_provenance") == 5

    ingest_parser_normalized_replay(connection, _replay_payload())

    assert _count(connection, "ingest_runs") == 2
    assert _count(connection, "matches") == 1
    assert _count(connection, "games") == 1
    assert _count(connection, "fact_provenance") == 5


def test_live_adapter_rejects_unsafe_labels_and_forbidden_raw_payload_fields() -> None:
    connection = _connect()
    unsafe_label_payload = _live_payload()
    unsafe_label_payload["session_id"] = "C:\\private\\Player.log"

    with pytest.raises(AnalyticsReplayIngestError, match="session_id"):
        ingest_live_parser_owned_facts(connection, unsafe_label_payload)

    forbidden_payload = _live_payload()
    forbidden_payload["player_log_path"] = "C:\\private\\Player.log"

    with pytest.raises(AnalyticsReplayIngestError, match="player_log_path"):
        ingest_live_parser_owned_facts(connection, forbidden_payload)


def test_live_adapter_rejects_raw_artifact_source_label_without_partial_writes() -> None:
    payload = _live_payload()
    payload["source_artifact_label"] = "Player.log"

    _assert_live_ingest_error_without_partial_fact_rows(payload, "source_artifact_label")


def test_live_adapter_rejects_forbidden_raw_fields_inside_rows_without_partial_writes() -> None:
    payload = _live_payload()
    match_row = dict(payload["match_log_rows"][0])  # type: ignore[index]
    match_row["player_log_path"] = "local-profile\\Player.log"
    payload["match_log_rows"] = [match_row]

    _assert_live_ingest_error_without_partial_fact_rows(payload, "match_log_rows\\[0\\].player_log_path")


def test_live_adapter_rejects_unsafe_private_row_values_without_partial_writes() -> None:
    payload = _live_payload()
    game_row = dict(payload["game_log_rows"][0])  # type: ignore[index]
    game_row["debug_note"] = "local-profile\\Player.log"
    payload["game_log_rows"] = [game_row]

    _assert_live_ingest_error_without_partial_fact_rows(payload, "game_log_rows\\[0\\].debug_note")


def test_live_adapter_rejects_provisional_rows_without_overwriting_final_facts() -> None:
    connection = _connect()
    ingest_live_parser_owned_facts(connection, _live_payload())
    before = connection.execute("SELECT finality, ingest_run_id FROM matches").fetchone()

    with pytest.raises(AnalyticsReplayIngestError, match="finality"):
        ingest_live_parser_owned_facts(connection, _live_payload(sync_status="Live"))

    after = connection.execute("SELECT finality, ingest_run_id FROM matches").fetchone()
    assert dict(after) == dict(before)
    assert _count(connection, "matches") == 1
    assert _count(connection, "games") == 1


def test_live_adapter_skips_deferred_fact_families_with_warnings() -> None:
    connection = _connect()
    payload = _live_payload()
    payload["gameplay_action_entries"] = [{"match_id": "match:live:001"}]
    payload["opponent_card_observations"] = [{"match_id": "match:live:001"}]
    payload["field_evidence_entries"] = [{"fact_table": "matches"}]

    result = ingest_live_parser_owned_facts(connection, payload)

    assert result.warnings == [
        "live_gameplay_action_capture_deferred",
        "live_opponent_observation_capture_deferred",
        "live_field_evidence_capture_deferred",
    ]
    assert result.skipped == {
        "gameplay_action_entries": 1,
        "opponent_card_observations": 1,
        "field_evidence_entries": 1,
    }
    assert _count(connection, "gameplay_actions") == 0
    assert _count(connection, "opponent_card_observations") == 0


def test_live_adapter_does_not_create_generated_sqlite_files() -> None:
    before = _sqlite_artifacts()
    connection = _connect()

    ingest_live_parser_owned_facts(connection, _live_payload())

    assert _sqlite_artifacts() == before
