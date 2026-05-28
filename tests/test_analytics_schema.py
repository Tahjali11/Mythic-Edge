from __future__ import annotations

import hashlib
import re
import sqlite3
from pathlib import Path

import pytest

SCHEMA_VERSION = "analytics_local_sqlite_schema.v1"
MIGRATION_PATH = Path("src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql")
DATABASE_IGNORE_PATH = "data/analytics/"

REQUIRED_TABLES = {
    "schema_migrations",
    "ingest_runs",
    "parser_schema_versions",
    "matches",
    "games",
    "game_players",
    "sessions",
    "deck_labels",
    "match_results",
    "game_results",
    "match_context",
    "rank_snapshots",
    "opening_hands",
    "opening_hand_cards",
    "mulligan_events",
    "mulligan_bottomed_or_discarded_cards",
    "sideboarding_states",
    "submitted_deck_snapshots",
    "submitted_deck_cards",
    "turns",
    "gameplay_actions",
    "gameplay_action_cards",
    "card_movements",
    "life_totals",
    "public_zone_observations",
    "opponent_card_observations",
    "opponent_card_observation_cards",
    "matchup_labels",
    "archetype_labels",
    "game_notes",
    "fact_provenance",
}
METADATA_TABLES = {"schema_migrations", "ingest_runs", "parser_schema_versions"}
FACT_TABLES = REQUIRED_TABLES - METADATA_TABLES - {"fact_provenance"}
ANNOTATION_TABLES = {"matchup_labels", "archetype_labels", "game_notes"}
PARSER_FACT_TABLES = FACT_TABLES - ANNOTATION_TABLES
CORE_PROVENANCE_COLUMNS = {
    "value_source",
    "confidence",
    "finality",
    "drift_status",
    "parser_schema_version",
    "ingest_run_id",
    "source_parser_surface",
    "source_fact_key",
    "availability_status",
    "created_at",
    "updated_at",
}
REQUIRED_VIEWS = {
    "v_opening_hand_cards",
    "v_opening_lines",
    "v_mulligan_outcomes",
    "v_game1_vs_postboard",
    "v_play_draw_splits",
    "v_sample_size_warnings",
    "v_matchup_label_performance",
}
VALUE_SOURCE_LABELS = {
    "observed",
    "derived",
    "inferred",
    "unknown",
    "conflict",
    "legacy_enriched",
    "human_annotation",
}
CONFIDENCE_LABELS = {"high", "medium", "low", "unknown", "human"}
FINALITY_LABELS = {"live", "provisional", "final", "reconciled", "annotation_current", "annotation_historical"}
DRIFT_STATUS_LABELS = {"none", "not_checked", "degraded", "conflict", "missing_expected_evidence", "redacted"}
AVAILABILITY_LABELS = {
    "available",
    "expected_unavailable",
    "not_applicable",
    "not_observed",
    "withheld_private",
    "not_yet_supported",
}


def _connect_schema() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    _apply_migration(connection)
    return connection


def _apply_migration(connection: sqlite3.Connection) -> str:
    sql = MIGRATION_PATH.read_text(encoding="utf-8")
    connection.executescript(sql)
    checksum = hashlib.sha256(sql.encode("utf-8")).hexdigest()
    connection.execute(
        """
        INSERT INTO schema_migrations (
            migration_id,
            migration_filename,
            checksum_sha256,
            applied_at,
            schema_version_after
        ) VALUES (?, ?, ?, ?, ?)
        """,
        ("0001_initial_analytics_schema", MIGRATION_PATH.name, checksum, "test-applied", SCHEMA_VERSION),
    )
    return checksum


def _names(connection: sqlite3.Connection, object_type: str) -> set[str]:
    rows = connection.execute("SELECT name FROM sqlite_schema WHERE type = ?", (object_type,)).fetchall()
    return {str(row["name"]) for row in rows if not str(row["name"]).startswith("sqlite_")}


def _columns(connection: sqlite3.Connection, table_name: str) -> set[str]:
    rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {str(row["name"]) for row in rows}


def _table_sql(connection: sqlite3.Connection, table_name: str) -> str:
    row = connection.execute(
        "SELECT sql FROM sqlite_schema WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    assert row is not None
    return str(row["sql"])


def _core_values(**overrides: str) -> dict[str, str]:
    values = {
        "value_source": "observed",
        "confidence": "high",
        "finality": "final",
        "drift_status": "none",
        "parser_schema_version": SCHEMA_VERSION,
        "ingest_run_id": "ingest:test",
        "source_parser_surface": "GameSummary.to_game_log_row",
        "source_fact_key": "test_fact",
        "availability_status": "available",
        "created_at": "2026-05-28T00:00:00Z",
        "updated_at": "2026-05-28T00:00:00Z",
    }
    values.update(overrides)
    return values


def _insert_with_core(
    connection: sqlite3.Connection,
    table_name: str,
    row: dict[str, object],
    *,
    on_conflict: str = "",
    **core_overrides: str,
) -> None:
    values = {**row, **_core_values(**core_overrides)}
    columns = ", ".join(values)
    placeholders = ", ".join("?" for _ in values)
    connection.execute(
        f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) {on_conflict}",
        tuple(values.values()),
    )


def _insert_seed_run(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        INSERT INTO ingest_runs (
            ingest_run_id,
            source_kind,
            source_artifact_label,
            started_at,
            finished_at,
            status,
            parser_commit,
            parser_version,
            schema_version,
            row_counts_json,
            created_at,
            updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "ingest:test",
            "sanitized_golden_replay",
            "parser_regression_match_bo1_v1",
            "2026-05-28T00:00:00Z",
            "2026-05-28T00:00:01Z",
            "completed",
            "test",
            "test",
            SCHEMA_VERSION,
            "{}",
            "2026-05-28T00:00:00Z",
            "2026-05-28T00:00:00Z",
        ),
    )


def _insert_seed_match_and_game(connection: sqlite3.Connection) -> None:
    _insert_seed_run(connection)
    _insert_with_core(
        connection,
        "matches",
        {
            "match_id": "match:test",
            "session_id": None,
            "parser_match_key": "match:test",
            "match_started_at": "2026-05-28T00:00:00Z",
            "match_completed_at": "2026-05-28T00:30:00Z",
        },
    )
    _insert_with_core(
        connection,
        "games",
        {
            "game_id": "match:test:g1",
            "match_id": "match:test",
            "game_number": 1,
            "game_started_at": "2026-05-28T00:00:00Z",
            "game_completed_at": "2026-05-28T00:15:00Z",
        },
    )


def test_migration_applies_and_records_schema_identity() -> None:
    connection = _connect_schema()

    migration = connection.execute("SELECT * FROM schema_migrations").fetchone()
    parser_version = connection.execute("SELECT * FROM parser_schema_versions").fetchone()

    assert migration["migration_id"] == "0001_initial_analytics_schema"
    assert migration["migration_filename"] == MIGRATION_PATH.name
    assert re.fullmatch(r"[0-9a-f]{64}", migration["checksum_sha256"])
    assert migration["schema_version_after"] == SCHEMA_VERSION
    assert parser_version["parser_schema_version_id"] == SCHEMA_VERSION
    assert "MatchLogRow" in parser_version["source_surfaces"]
    assert "opponent_card_observation" in parser_version["source_surfaces"]


def test_generated_database_path_is_ignored() -> None:
    gitignore_lines = Path(".gitignore").read_text(encoding="utf-8").splitlines()

    assert DATABASE_IGNORE_PATH in gitignore_lines


def test_required_tables_views_and_indexes_exist() -> None:
    connection = _connect_schema()

    assert REQUIRED_TABLES <= _names(connection, "table")
    assert REQUIRED_VIEWS <= _names(connection, "view")

    index_names = _names(connection, "index")
    assert "idx_games_match_id" in index_names
    assert "idx_gameplay_actions_match_game" in index_names
    assert "idx_fact_provenance_fact" in index_names


def test_fact_tables_include_core_provenance_columns() -> None:
    connection = _connect_schema()

    for table_name in FACT_TABLES:
        assert CORE_PROVENANCE_COLUMNS <= _columns(connection, table_name), table_name


def test_schema_constrains_required_status_vocabularies() -> None:
    sql = MIGRATION_PATH.read_text(encoding="utf-8")

    for label in VALUE_SOURCE_LABELS | CONFIDENCE_LABELS | FINALITY_LABELS | DRIFT_STATUS_LABELS:
        assert f"'{label}'" in sql
    for label in AVAILABILITY_LABELS:
        assert f"'{label}'" in sql

    connection = _connect_schema()
    _insert_seed_run(connection)
    try:
        _insert_with_core(
            connection,
            "matches",
            {
                "match_id": "match:bad-label",
                "session_id": None,
                "parser_match_key": "match:bad-label",
                "match_started_at": None,
                "match_completed_at": None,
            },
        )
    except sqlite3.IntegrityError:
        raise AssertionError("valid core vocabulary labels should insert cleanly") from None

    bad_values = {
        **_core_values(value_source="not_a_source"),
        "match_id": "match:invalid",
        "session_id": None,
        "parser_match_key": "match:invalid",
        "match_started_at": None,
        "match_completed_at": None,
    }
    columns = ", ".join(bad_values)
    placeholders = ", ".join("?" for _ in bad_values)
    try:
        connection.execute(f"INSERT INTO matches ({columns}) VALUES ({placeholders})", tuple(bad_values.values()))
    except sqlite3.IntegrityError:
        return
    raise AssertionError("invalid value_source label should be rejected")


def test_parser_fact_tables_exclude_human_annotation_labels() -> None:
    connection = _connect_schema()

    for table_name in PARSER_FACT_TABLES:
        table_sql = _table_sql(connection, table_name)
        assert "'human_annotation'" not in table_sql, table_name
        assert "'human'" not in table_sql, table_name

    for table_name in ANNOTATION_TABLES:
        table_sql = _table_sql(connection, table_name)
        assert "value_source = 'human_annotation'" in table_sql, table_name
        assert "confidence = 'human'" in table_sql, table_name


def test_parser_fact_rows_reject_human_only_labels() -> None:
    connection = _connect_schema()
    _insert_seed_run(connection)
    base_match = {
        "match_id": "match:human-label",
        "session_id": None,
        "parser_match_key": "match:human-label",
        "match_started_at": None,
        "match_completed_at": None,
    }

    with pytest.raises(sqlite3.IntegrityError):
        _insert_with_core(connection, "matches", base_match, value_source="human_annotation")

    with pytest.raises(sqlite3.IntegrityError):
        _insert_with_core(
            connection,
            "matches",
            {**base_match, "match_id": "match:human-confidence", "parser_match_key": "match:human-confidence"},
            confidence="human",
        )


def test_annotation_tables_accept_human_annotation_labels() -> None:
    connection = _connect_schema()
    _insert_seed_match_and_game(connection)
    annotation_core = _core_values(
        value_source="human_annotation",
        confidence="human",
        finality="annotation_current",
        source_parser_surface="human_annotation",
        source_fact_key="human_annotation",
    )

    connection.execute(
        f"""
        INSERT INTO matchup_labels (
            matchup_label_id,
            match_id,
            label_value,
            label_source,
            author_label,
            valid_from,
            valid_to,
            is_current,
            {", ".join(annotation_core)}
        ) VALUES ({", ".join("?" for _ in range(8 + len(annotation_core)))})
        """,
        (
            "matchup:test",
            "match:test",
            "mirror",
            "manual",
            "local",
            "2026-05-28T00:00:00Z",
            None,
            1,
            *annotation_core.values(),
        ),
    )
    connection.execute(
        f"""
        INSERT INTO archetype_labels (
            archetype_label_id,
            match_id,
            label_value,
            label_source,
            author_label,
            valid_from,
            valid_to,
            is_current,
            {", ".join(annotation_core)}
        ) VALUES ({", ".join("?" for _ in range(8 + len(annotation_core)))})
        """,
        (
            "archetype:test",
            "match:test",
            "golgari_midrange",
            "manual",
            "local",
            "2026-05-28T00:00:00Z",
            None,
            1,
            *annotation_core.values(),
        ),
    )
    connection.execute(
        f"""
        INSERT INTO game_notes (
            game_note_id,
            game_id,
            match_id,
            note_text,
            note_source,
            author_label,
            valid_from,
            valid_to,
            is_current,
            {", ".join(annotation_core)}
        ) VALUES ({", ".join("?" for _ in range(9 + len(annotation_core)))})
        """,
        (
            "note:test",
            "match:test:g1",
            "match:test",
            "Kept a risky seven.",
            "manual",
            "local",
            "2026-05-28T00:00:00Z",
            None,
            1,
            *annotation_core.values(),
        ),
    )

    assert connection.execute("SELECT COUNT(*) AS count FROM matchup_labels").fetchone()["count"] == 1
    assert connection.execute("SELECT COUNT(*) AS count FROM archetype_labels").fetchone()["count"] == 1
    assert connection.execute("SELECT COUNT(*) AS count FROM game_notes").fetchone()["count"] == 1


def test_fact_provenance_supports_multiple_field_level_entries() -> None:
    connection = _connect_schema()
    _insert_seed_run(connection)

    common = {
        "fact_table": "opening_hands",
        "fact_id": "match:test:g1:opening_hand",
        "fact_field": "hand_size",
        "source_parser_surface": "GameSummary.to_game_log_row",
        "source_fact_key": "opening_hand_size",
        "source_event_kind": "GameState",
        "source_event_type": "opening_hand_snapshot",
        "source_payload_paths": '["GameSummary.opening_hand"]',
        "source_event_timestamp": "2026-05-28T00:00:00Z",
        "value_source": "observed",
        "confidence": "high",
        "finality": "final",
        "drift_flags": "[]",
        "invariant_status": "passed",
        "degraded_reason": "",
        "review_required": 0,
        "ingest_run_id": "ingest:test",
        "created_at": "2026-05-28T00:00:00Z",
    }
    connection.execute(
        f"INSERT INTO fact_provenance ({', '.join(['fact_provenance_id', *common])}) "
        f"VALUES ({', '.join('?' for _ in range(len(common) + 1))})",
        ("prov:1", *common.values()),
    )
    connection.execute(
        f"INSERT INTO fact_provenance ({', '.join(['fact_provenance_id', *common])}) "
        f"VALUES ({', '.join('?' for _ in range(len(common) + 1))})",
        ("prov:2", *common.values()),
    )

    count = connection.execute(
        """
        SELECT COUNT(*) AS count
        FROM fact_provenance
        WHERE fact_table = ? AND fact_id = ? AND fact_field = ?
        """,
        ("opening_hands", "match:test:g1:opening_hand", "hand_size"),
    ).fetchone()["count"]

    assert count == 2


def test_card_lists_are_normalized_into_child_rows() -> None:
    connection = _connect_schema()

    assert "opening_hand" not in _columns(connection, "opening_hands")
    assert {"opening_hand_id", "card_position", "grp_id", "card_name"} <= _columns(
        connection,
        "opening_hand_cards",
    )
    assert {"submitted_deck_snapshot_id", "section", "grp_id", "quantity"} <= _columns(
        connection,
        "submitted_deck_cards",
    )


def test_expected_unavailable_is_distinct_from_not_observed() -> None:
    connection = _connect_schema()
    _insert_seed_match_and_game(connection)

    _insert_with_core(
        connection,
        "mulligan_events",
        {
            "mulligan_event_id": "match:test:g1:mulligan:unknown_detail",
            "game_id": "match:test:g1",
            "match_id": "match:test",
            "game_number": 1,
            "ordinal_or_count": "unknown_detail",
            "mulligan_count": None,
            "decision_detail": None,
        },
    )
    _insert_with_core(
        connection,
        "mulligan_events",
        {
            "mulligan_event_id": "match:test:g1:mulligan:0",
            "game_id": "match:test:g1",
            "match_id": "match:test",
            "game_number": 1,
            "ordinal_or_count": "0",
            "mulligan_count": 0,
            "decision_detail": "kept_initial_hand",
        },
        on_conflict="",
    )
    connection.execute(
        """
        UPDATE mulligan_events
        SET availability_status = 'expected_unavailable'
        WHERE mulligan_event_id = 'match:test:g1:mulligan:unknown_detail'
        """
    )
    connection.execute(
        """
        UPDATE mulligan_events
        SET availability_status = 'not_observed'
        WHERE mulligan_event_id = 'match:test:g1:mulligan:0'
        """
    )

    statuses = {
        row["mulligan_event_id"]: row["availability_status"]
        for row in connection.execute("SELECT mulligan_event_id, availability_status FROM mulligan_events")
    }

    assert statuses["match:test:g1:mulligan:unknown_detail"] == "expected_unavailable"
    assert statuses["match:test:g1:mulligan:0"] == "not_observed"


def test_repeated_normalized_fact_insert_is_idempotent_by_deterministic_ids() -> None:
    connection = _connect_schema()
    _insert_seed_match_and_game(connection)
    opening_hand = {
        "opening_hand_id": "match:test:g1:opening_hand",
        "game_id": "match:test:g1",
        "match_id": "match:test",
        "game_number": 1,
        "hand_size": 7,
        "exact_card_count": 1,
    }
    opening_hand_card = {
        "opening_hand_card_id": "match:test:g1:opening_hand:slot1",
        "opening_hand_id": "match:test:g1:opening_hand",
        "game_id": "match:test:g1",
        "card_position": 1,
        "grp_id": 12345,
        "card_name": "Test Card",
        "identity_hint_source": "direct_grp_id",
        "name_resolution_status": "resolved",
    }

    for _ in range(2):
        _insert_with_core(
            connection,
            "opening_hands",
            opening_hand,
            on_conflict="ON CONFLICT(opening_hand_id) DO UPDATE SET updated_at = excluded.updated_at",
        )
        _insert_with_core(
            connection,
            "opening_hand_cards",
            opening_hand_card,
            on_conflict="ON CONFLICT(opening_hand_card_id) DO UPDATE SET updated_at = excluded.updated_at",
        )

    opening_hand_count = connection.execute("SELECT COUNT(*) AS count FROM opening_hands").fetchone()["count"]
    opening_card_count = connection.execute("SELECT COUNT(*) AS count FROM opening_hand_cards").fetchone()["count"]

    assert opening_hand_count == 1
    assert opening_card_count == 1
