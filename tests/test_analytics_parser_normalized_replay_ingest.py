from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from mythic_edge_parser.app.analytics_ingest import (
    ANALYTICS_REPLAY_INGEST_SCHEMA_VERSION,
    AnalyticsReplayIngestError,
    deterministic_ingest_run_id,
    ingest_parser_normalized_replay,
    normalize_parser_normalized_replay,
)
from mythic_edge_parser.app.analytics_migration_loader import ANALYTICS_SCHEMA_VERSION


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    return connection


def _base_replay() -> dict[str, object]:
    return {
        "source_kind": "sanitized_golden_replay",
        "source_artifact_label": "parser_regression_match_bo1_v1",
        "parser_commit": "test-parser-commit",
        "parser_version": "test-parser-version",
        "generated_at": "2026-05-28T12:00:00+00:00",
        "match_log_rows": [
            {
                "event_family": "MatchLogRow",
                "event_type": "match_log_row",
                "scope": "Match",
                "match_id": "match:test:001",
                "timestamp": "2026-05-28T12:30:00+00:00",
                "MTGA Match ID": "match:test:001",
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
                "MGTA Start Time": "2026-05-28T12:00:00+00:00",
                "MTGA End Time": "2026-05-28T12:30:00+00:00",
                "MTGA Sync Status": "Final",
                "MTGA Sideboard Entered": "No",
                "MTGA Submit Deck Seen": "No",
                "G1 Mulligans": 1,
                "G1 Play / Draw": "Play",
                "G1 Turn Count": 8,
                "Game 1 Result": "W",
            },
        ],
        "game_log_rows": [
            {
                "event_family": "GameLogRow",
                "event_type": "game_log_row",
                "scope": "Game",
                "match_id": "match:test:001",
                "timestamp": "2026-05-28T12:30:00+00:00",
                "MTGA Match ID": "match:test:001",
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
            },
        ],
    }


def _count(connection: sqlite3.Connection, table_name: str) -> int:
    return int(connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0])


def _sqlite_artifacts() -> set[str]:
    root = Path("data/analytics")
    if not root.exists():
        return set()
    patterns = ("*.db", "*.sqlite", "*.sqlite3", "*.db-journal", "*.db-wal", "*.db-shm")
    found: set[str] = set()
    for pattern in patterns:
        found.update(str(path) for path in root.glob(pattern))
    return found


def _assert_ingest_error_without_partial_fact_rows(replay: dict[str, object], match: str) -> None:
    connection = _connect()

    with pytest.raises(AnalyticsReplayIngestError, match=match):
        ingest_parser_normalized_replay(connection, replay, started_at="now", finished_at="done")

    assert _count(connection, "ingest_runs") == 0
    assert _count(connection, "matches") == 0
    assert _count(connection, "games") == 0


def test_schema_version_constant_is_public() -> None:
    assert ANALYTICS_REPLAY_INGEST_SCHEMA_VERSION == "analytics_parser_normalized_replay_ingest.v1"


def test_ingest_migrates_empty_memory_database_and_writes_core_facts() -> None:
    connection = _connect()

    result = ingest_parser_normalized_replay(
        connection,
        _base_replay(),
        started_at="2026-05-28T12:00:00+00:00",
        finished_at="2026-05-28T12:31:00+00:00",
    )

    assert result.status == "completed"
    assert result.source_kind == "sanitized_golden_replay"
    assert result.source_artifact_label == "parser_regression_match_bo1_v1"
    assert result.warnings == []
    assert result.skipped == {}
    assert _count(connection, "schema_migrations") == 1
    assert _count(connection, "ingest_runs") == 1
    assert _count(connection, "matches") == 1
    assert _count(connection, "games") == 1
    assert _count(connection, "match_results") == 1
    assert _count(connection, "game_results") == 1
    assert _count(connection, "match_context") == 1
    assert _count(connection, "rank_snapshots") == 1
    assert _count(connection, "opening_hands") == 1
    assert _count(connection, "opening_hand_cards") == 3
    assert _count(connection, "mulligan_events") == 1
    assert _count(connection, "mulligan_bottomed_or_discarded_cards") == 1

    run = connection.execute("SELECT * FROM ingest_runs").fetchone()
    assert run["ingest_run_id"] == result.ingest_run_id
    assert run["status"] == "completed"
    assert run["schema_version"] == ANALYTICS_SCHEMA_VERSION
    assert json.loads(run["row_counts_json"]) == result.row_counts


def test_ingest_run_id_is_deterministic_for_same_normalized_input() -> None:
    replay = normalize_parser_normalized_replay(_base_replay())

    assert deterministic_ingest_run_id(replay) == deterministic_ingest_run_id(replay)


def test_replaying_same_normalized_input_is_idempotent() -> None:
    connection = _connect()
    replay = _base_replay()

    first = ingest_parser_normalized_replay(connection, replay, started_at="first", finished_at="first-done")
    second = ingest_parser_normalized_replay(connection, replay, started_at="second", finished_at="second-done")

    assert second.ingest_run_id == first.ingest_run_id
    assert second.row_counts == first.row_counts
    assert _count(connection, "ingest_runs") == 1
    assert _count(connection, "matches") == 1
    assert _count(connection, "games") == 1
    assert _count(connection, "opening_hand_cards") == 3
    assert _count(connection, "fact_provenance") == 5


def test_core_provenance_columns_use_safe_default_labels() -> None:
    connection = _connect()
    result = ingest_parser_normalized_replay(connection, _base_replay(), started_at="now", finished_at="done")

    rows = [
        connection.execute("SELECT * FROM matches").fetchone(),
        connection.execute("SELECT * FROM game_results").fetchone(),
        connection.execute("SELECT * FROM opening_hands").fetchone(),
        connection.execute("SELECT * FROM mulligan_events").fetchone(),
    ]

    assert rows[0]["finality"] == "reconciled"
    for row in rows:
        assert row["value_source"] == "derived"
        assert row["confidence"] == "unknown"
        assert row["drift_status"] == "not_checked"
        assert row["parser_schema_version"] == ANALYTICS_SCHEMA_VERSION
        assert row["ingest_run_id"] == result.ingest_run_id
        assert row["availability_status"] in {"available", "not_observed"}
        assert row["source_parser_surface"] in {
            "MatchSummary.to_match_log_row",
            "GameSummary.to_game_log_row",
        }


def test_fact_provenance_rows_use_labels_not_raw_payloads() -> None:
    connection = _connect()
    result = ingest_parser_normalized_replay(connection, _base_replay(), started_at="now", finished_at="done")

    rows = connection.execute(
        "SELECT fact_table, fact_field, source_payload_paths, ingest_run_id FROM fact_provenance"
    ).fetchall()

    assert {(row["fact_table"], row["fact_field"]) for row in rows} == {
        ("matches", "match_id"),
        ("match_results", "match_result"),
        ("game_results", "local_result"),
        ("opening_hands", "hand_size"),
        ("mulligan_events", "mulligan_count"),
    }
    for row in rows:
        paths = json.loads(row["source_payload_paths"])
        assert row["ingest_run_id"] == result.ingest_run_id
        assert all(path.startswith("/") for path in paths)
        assert "Player.log" not in row["source_payload_paths"]
        assert ":\\" not in row["source_payload_paths"]
        assert "http" not in row["source_payload_paths"]


def test_empty_optional_decision_fields_are_not_coerced_to_zero_or_false() -> None:
    replay = _base_replay()
    game_row = dict(replay["game_log_rows"][0])  # type: ignore[index]
    game_row.update(
        {
            "Mulligans": "",
            "Opening Hand Size": "",
            "Opening Hand": "",
            "Mulliganed Away": "",
        }
    )
    replay["game_log_rows"] = [game_row]
    connection = _connect()

    ingest_parser_normalized_replay(connection, replay, started_at="now", finished_at="done")

    assert _count(connection, "games") == 1
    assert _count(connection, "opening_hands") == 0
    assert _count(connection, "opening_hand_cards") == 0
    assert _count(connection, "mulligan_events") == 0
    assert _count(connection, "mulligan_bottomed_or_discarded_cards") == 0


def test_name_only_opening_hand_cards_do_not_claim_grp_id() -> None:
    connection = _connect()

    ingest_parser_normalized_replay(connection, _base_replay(), started_at="now", finished_at="done")

    rows = connection.execute(
        """
        SELECT grp_id, card_name, identity_hint_source, name_resolution_status
        FROM opening_hand_cards
        ORDER BY card_position
        """
    ).fetchall()
    assert [row["card_name"] for row in rows] == ["Forest", "Swamp", "Mosswood Dreadknight"]
    assert {row["grp_id"] for row in rows} == {None}
    assert {row["identity_hint_source"] for row in rows} == {"name_only_from_parser_row"}
    assert {row["name_resolution_status"] for row in rows} == {"name_only"}


def test_missing_match_id_fails_without_partial_fact_rows() -> None:
    replay = _base_replay()
    match_row = dict(replay["match_log_rows"][0])  # type: ignore[index]
    match_row["match_id"] = ""
    match_row["MTGA Match ID"] = ""
    replay["match_log_rows"] = [match_row]
    connection = _connect()

    with pytest.raises(AnalyticsReplayIngestError, match="match_log_rows\\[0\\].*match_id"):
        ingest_parser_normalized_replay(connection, replay, started_at="now", finished_at="done")

    assert _count(connection, "ingest_runs") == 0
    assert _count(connection, "matches") == 0
    assert _count(connection, "games") == 0


def test_malformed_game_number_fails_without_partial_fact_rows() -> None:
    replay = _base_replay()
    game_row = dict(replay["game_log_rows"][0])  # type: ignore[index]
    game_row["Game Number"] = "not-a-number"
    replay["game_log_rows"] = [game_row]
    connection = _connect()

    with pytest.raises(AnalyticsReplayIngestError, match="Game Number"):
        ingest_parser_normalized_replay(connection, replay, started_at="now", finished_at="done")

    assert _count(connection, "ingest_runs") == 0
    assert _count(connection, "matches") == 0
    assert _count(connection, "games") == 0


@pytest.mark.parametrize(
    ("row_group", "field_name"),
    (
        ("game_log_rows", "Game Number"),
        ("game_log_rows", "Mulligans"),
        ("game_log_rows", "Opening Hand Size"),
        ("game_log_rows", "Turn Count"),
        ("match_log_rows", "Games Won"),
        ("match_log_rows", "Total Games"),
    ),
)
def test_fractional_parser_owned_integer_fields_fail_without_partial_fact_rows(
    row_group: str,
    field_name: str,
) -> None:
    replay = _base_replay()
    row = dict(replay[row_group][0])  # type: ignore[index]
    row[field_name] = 1.5
    replay[row_group] = [row]

    _assert_ingest_error_without_partial_fact_rows(replay, field_name)


@pytest.mark.parametrize(
    ("row_group", "field_name"),
    (
        ("game_log_rows", "Mulligans"),
        ("game_log_rows", "Opening Hand Size"),
        ("game_log_rows", "Turn Count"),
        ("match_log_rows", "Games Won"),
        ("match_log_rows", "Total Games"),
    ),
)
def test_negative_parser_owned_counts_fail_without_partial_fact_rows(row_group: str, field_name: str) -> None:
    replay = _base_replay()
    row = dict(replay[row_group][0])  # type: ignore[index]
    row[field_name] = -1
    replay[row_group] = [row]

    _assert_ingest_error_without_partial_fact_rows(replay, field_name)


def test_unsupported_source_kind_and_unsafe_label_fail_clearly() -> None:
    replay = _base_replay()
    replay["source_kind"] = "live_parser"

    with pytest.raises(AnalyticsReplayIngestError, match="Unsupported"):
        normalize_parser_normalized_replay(replay)

    replay = _base_replay()
    replay["source_artifact_label"] = "Z:" + "\\private\\Player.log"

    with pytest.raises(AnalyticsReplayIngestError, match="safe label"):
        normalize_parser_normalized_replay(replay)


def test_no_optional_payloads_are_reported_as_deferred_after_accepted_slices() -> None:
    replay = _base_replay()
    connection = _connect()

    result = ingest_parser_normalized_replay(connection, replay, started_at="now", finished_at="done")

    assert result.skipped == {}
    assert result.warnings == []


def test_ingest_does_not_create_generated_sqlite_files() -> None:
    before = _sqlite_artifacts()
    connection = _connect()

    ingest_parser_normalized_replay(connection, _base_replay(), started_at="now", finished_at="done")

    assert _sqlite_artifacts() == before
