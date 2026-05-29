from __future__ import annotations

import os
import re
import sqlite3
import tomllib
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

import pytest

from mythic_edge_parser.app import match_journal_migration_loader as loader
from mythic_edge_parser.app.analytics_migration_loader import apply_analytics_migrations
from mythic_edge_parser.app.match_journal_migration_loader import (
    DEFAULT_MATCH_JOURNAL_DATABASE_PATH,
    MATCH_JOURNAL_MIGRATIONS_PACKAGE,
    MATCH_JOURNAL_SCHEMA_VERSION,
    MatchJournalMigrationError,
    apply_match_journal_migrations,
    iter_match_journal_migrations,
    load_match_journal_migration,
    load_match_journal_migration_sql,
)

FIRST_MIGRATION_FILENAME = "0001_initial_match_journal_schema.sql"
FIRST_MIGRATION_ID = "0001_initial_match_journal_schema"
DATABASE_IGNORE_PATH = "data/match_journal/"
NOW = "2026-05-29T00:00:00+00:00"

REQUIRED_TABLES = {
    "journal_schema_migrations",
    "journal_schema_versions",
    "journal_matches",
    "journal_games",
    "journal_notes",
    "journal_labels",
    "journal_review_flags",
    "journal_reference_values",
    "journal_field_overrides",
}
DEFERRED_TABLES = {"journal_sheet_sync_queue"}


@dataclass(frozen=True, slots=True)
class FakeResource:
    name: str
    sql: str

    def read_text(self, encoding: str = "utf-8") -> str:
        assert encoding == "utf-8"
        return self.sql


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def _connect_schema() -> sqlite3.Connection:
    connection = _connect()
    apply_match_journal_migrations(connection, applied_at=NOW)
    return connection


def _names(connection: sqlite3.Connection, object_type: str) -> set[str]:
    rows = connection.execute("SELECT name FROM sqlite_schema WHERE type = ?", (object_type,)).fetchall()
    return {str(row["name"]) for row in rows if not str(row["name"]).startswith("sqlite_")}


def _columns(connection: sqlite3.Connection, table_name: str) -> set[str]:
    rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {str(row["name"]) for row in rows}


def _insert_journal_match(connection: sqlite3.Connection, **overrides: object) -> None:
    values = {
        "journal_match_id": "journal:match:1",
        "parser_match_id": "parser:match:1",
        "attachment_status": "attached",
        "title": "Synthetic match",
        "experiment_id": "experiment:fixture",
        "review_status": "needs_review",
        "created_at": NOW,
        "updated_at": NOW,
        "author_label": "tester",
        "source_surface": "test_fixture",
        "privacy_label": "sanitized_fixture",
    }
    values.update(overrides)
    _insert_row(connection, "journal_matches", values)


def _insert_journal_game(connection: sqlite3.Connection, **overrides: object) -> None:
    values = {
        "journal_game_id": "journal:game:1",
        "journal_match_id": "journal:match:1",
        "parser_match_id": "parser:match:1",
        "parser_game_id": "parser:match:1:g1",
        "game_number": 1,
        "attachment_status": "attached",
        "review_status": "not_reviewed",
        "created_at": NOW,
        "updated_at": NOW,
        "author_label": "tester",
        "source_surface": "test_fixture",
        "privacy_label": "sanitized_fixture",
    }
    values.update(overrides)
    _insert_row(connection, "journal_games", values)


def _insert_row(connection: sqlite3.Connection, table_name: str, values: dict[str, object]) -> None:
    columns = ", ".join(values)
    placeholders = ", ".join("?" for _ in values)
    connection.execute(
        f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
        tuple(values.values()),
    )


def test_migration_package_resource_can_be_loaded() -> None:
    migration_path = resources.files(MATCH_JOURNAL_MIGRATIONS_PACKAGE).joinpath(FIRST_MIGRATION_FILENAME)

    assert migration_path.is_file()
    assert "CREATE TABLE journal_matches" in migration_path.read_text(encoding="utf-8")


def test_pyproject_includes_match_journal_sql_package_data() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    package_data = pyproject["tool"]["setuptools"]["package-data"]
    assert package_data[MATCH_JOURNAL_MIGRATIONS_PACKAGE] == ["*.sql"]


def test_iter_match_journal_migrations_returns_first_migration_in_deterministic_order() -> None:
    migrations = iter_match_journal_migrations()

    assert [migration.filename for migration in migrations] == [FIRST_MIGRATION_FILENAME]
    assert migrations[0].migration_id == FIRST_MIGRATION_ID
    assert migrations[0].schema_version_after == MATCH_JOURNAL_SCHEMA_VERSION
    assert re.fullmatch(r"[0-9a-f]{64}", migrations[0].checksum_sha256)


def test_load_match_journal_migration_sql_reads_package_resource_from_any_cwd(tmp_path: Path) -> None:
    original_cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        sql_by_id = load_match_journal_migration_sql(FIRST_MIGRATION_ID)
        sql_by_filename = load_match_journal_migration_sql(FIRST_MIGRATION_FILENAME)
    finally:
        os.chdir(original_cwd)

    assert sql_by_id == sql_by_filename
    assert "CREATE TABLE journal_notes" in sql_by_id
    assert str(tmp_path) not in sql_by_id


def test_load_match_journal_migration_returns_exact_checksum_and_sql() -> None:
    migration = load_match_journal_migration(FIRST_MIGRATION_ID)
    sql = load_match_journal_migration_sql(FIRST_MIGRATION_ID)

    assert migration.sql == sql
    assert migration.checksum_sha256 == iter_match_journal_migrations()[0].checksum_sha256


def test_default_generated_database_path_is_private_and_ignored() -> None:
    gitignore_lines = Path(".gitignore").read_text(encoding="utf-8").splitlines()

    assert DEFAULT_MATCH_JOURNAL_DATABASE_PATH == "data/match_journal/mythic_edge_journal.sqlite3"
    assert DATABASE_IGNORE_PATH in gitignore_lines


def test_apply_match_journal_migrations_creates_schema_and_records_history() -> None:
    connection = _connect_schema()

    assert REQUIRED_TABLES <= _names(connection, "table")
    assert DEFERRED_TABLES.isdisjoint(_names(connection, "table"))
    assert {"idx_journal_matches_parser_match_id", "idx_journal_labels_match_type"} <= _names(
        connection,
        "index",
    )

    migration = connection.execute(
        "SELECT * FROM journal_schema_migrations WHERE migration_id = ?",
        (FIRST_MIGRATION_ID,),
    ).fetchone()
    schema_version = connection.execute("SELECT * FROM journal_schema_versions").fetchone()
    assert migration["migration_filename"] == FIRST_MIGRATION_FILENAME
    assert migration["applied_at"] == NOW
    assert migration["schema_version_after"] == MATCH_JOURNAL_SCHEMA_VERSION
    assert schema_version["schema_version_id"] == MATCH_JOURNAL_SCHEMA_VERSION


def test_required_columns_exist_on_journal_tables() -> None:
    connection = _connect_schema()

    assert {
        "journal_match_id",
        "parser_match_id",
        "attachment_status",
        "title",
        "experiment_id",
        "review_status",
        "created_at",
        "updated_at",
        "author_label",
        "source_surface",
        "privacy_label",
    } <= _columns(connection, "journal_matches")
    assert {
        "journal_note_id",
        "journal_match_id",
        "journal_game_id",
        "parser_match_id",
        "parser_game_id",
        "note_scope",
        "note_text",
        "note_format",
        "author_label",
        "source_surface",
        "privacy_label",
        "is_current",
        "supersedes_note_id",
        "valid_from",
        "valid_to",
        "created_at",
        "updated_at",
    } <= _columns(connection, "journal_notes")
    assert {
        "journal_field_override_id",
        "target_surface",
        "target_field",
        "original_value_label",
        "proposed_value_label",
        "override_reason",
        "override_status",
        "effect_scope",
    } <= _columns(connection, "journal_field_overrides")


def test_apply_match_journal_migrations_is_idempotent_on_same_connection() -> None:
    connection = _connect()

    first = apply_match_journal_migrations(connection, applied_at="first")
    second = apply_match_journal_migrations(connection, applied_at="second")

    rows = connection.execute("SELECT * FROM journal_schema_migrations").fetchall()
    assert len(rows) == 1
    assert rows[0]["checksum_sha256"] == first[0].checksum_sha256
    assert rows[0]["applied_at"] == "first"
    assert second == first


def test_preexisting_different_checksum_is_rejected_without_overwrite() -> None:
    connection = _connect()
    apply_match_journal_migrations(connection, applied_at="first")
    connection.execute(
        "UPDATE journal_schema_migrations SET checksum_sha256 = ? WHERE migration_id = ?",
        ("0" * 64, FIRST_MIGRATION_ID),
    )
    connection.commit()

    with pytest.raises(MatchJournalMigrationError, match="Checksum mismatch"):
        apply_match_journal_migrations(connection, applied_at="second")

    row = connection.execute("SELECT checksum_sha256 FROM journal_schema_migrations").fetchone()
    assert row["checksum_sha256"] == "0" * 64


def test_open_caller_transaction_is_rejected() -> None:
    connection = _connect()
    connection.execute("BEGIN")

    with pytest.raises(MatchJournalMigrationError, match="open transaction"):
        apply_match_journal_migrations(connection)


def test_invalid_migration_resource_fails_clearly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(loader, "_migration_resources", lambda: (FakeResource("not_a_migration.sql", "SELECT 1;"),))

    with pytest.raises(MatchJournalMigrationError, match="Invalid Match Journal migration filename"):
        iter_match_journal_migrations()


def test_unattached_note_is_preserved_without_parser_identity() -> None:
    connection = _connect_schema()

    _insert_row(
        connection,
        "journal_notes",
        {
            "journal_note_id": "journal:note:unattached",
            "journal_match_id": None,
            "journal_game_id": None,
            "parser_match_id": None,
            "parser_game_id": None,
            "note_scope": "unattached",
            "note_text": "Synthetic unattached note for review.",
            "note_format": "plain_text",
            "author_label": "tester",
            "source_surface": "test_fixture",
            "privacy_label": "sanitized_fixture",
            "is_current": 1,
            "supersedes_note_id": None,
            "valid_from": NOW,
            "valid_to": None,
            "created_at": NOW,
            "updated_at": NOW,
        },
    )

    row = connection.execute(
        "SELECT * FROM journal_notes WHERE journal_note_id = ?",
        ("journal:note:unattached",),
    ).fetchone()
    assert row["parser_match_id"] is None
    assert row["parser_game_id"] is None
    assert row["note_scope"] == "unattached"
    assert row["note_text"] == "Synthetic unattached note for review."


def test_attached_journal_rows_reference_parser_ids_without_parser_tables() -> None:
    connection = _connect_schema()
    _insert_journal_match(connection)
    _insert_journal_game(connection)

    match = connection.execute("SELECT * FROM journal_matches").fetchone()
    game = connection.execute("SELECT * FROM journal_games").fetchone()
    assert match["journal_match_id"] == "journal:match:1"
    assert match["parser_match_id"] == "parser:match:1"
    assert game["journal_game_id"] == "journal:game:1"
    assert game["parser_game_id"] == "parser:match:1:g1"


def test_structured_labels_reference_values_and_pilot_error_vocabulary() -> None:
    connection = _connect_schema()
    _insert_journal_match(connection)
    _insert_row(
        connection,
        "journal_reference_values",
        {
            "reference_id": "ref:pilot:error:sequencing",
            "reference_type": "pilot_error_reason",
            "label": "sequencing",
            "description": "Synthetic sequencing review reason.",
            "sort_order": 10,
            "is_active": 1,
            "created_at": NOW,
            "updated_at": NOW,
        },
    )
    _insert_row(
        connection,
        "journal_labels",
        {
            "journal_label_id": "journal:label:pilot-error",
            "journal_match_id": "journal:match:1",
            "journal_game_id": None,
            "parser_match_id": "parser:match:1",
            "parser_game_id": None,
            "label_scope": "review",
            "label_type": "pilot_error",
            "label_value": "yes",
            "reference_id": "ref:pilot:error:sequencing",
            "author_label": "tester",
            "source_surface": "test_fixture",
            "privacy_label": "sanitized_fixture",
            "is_current": 1,
            "valid_from": NOW,
            "valid_to": None,
            "created_at": NOW,
            "updated_at": NOW,
        },
    )

    row = connection.execute("SELECT * FROM journal_labels").fetchone()
    assert row["label_type"] == "pilot_error"
    assert row["label_value"] == "yes"
    assert row["reference_id"] == "ref:pilot:error:sequencing"


def test_review_flags_store_review_tasks_not_parser_truth() -> None:
    connection = _connect_schema()
    _insert_journal_match(connection)
    _insert_row(
        connection,
        "journal_review_flags",
        {
            "journal_review_flag_id": "journal:flag:parser-gap",
            "journal_match_id": "journal:match:1",
            "journal_game_id": None,
            "parser_match_id": "parser:match:1",
            "parser_game_id": None,
            "flag_type": "suspected_parser_gap",
            "flag_status": "open",
            "priority_label": "high",
            "reason": "Synthetic review-only parser gap flag.",
            "author_label": "tester",
            "source_surface": "test_fixture",
            "privacy_label": "sanitized_fixture",
            "created_at": NOW,
            "updated_at": NOW,
        },
    )

    row = connection.execute("SELECT * FROM journal_review_flags").fetchone()
    assert row["flag_type"] == "suspected_parser_gap"
    assert row["flag_status"] == "open"


def test_field_overrides_are_display_only_proposals() -> None:
    connection = _connect_schema()
    _insert_journal_match(connection)
    _insert_row(
        connection,
        "journal_field_overrides",
        {
            "journal_field_override_id": "journal:override:1",
            "journal_match_id": "journal:match:1",
            "journal_game_id": None,
            "parser_match_id": "parser:match:1",
            "parser_game_id": None,
            "target_surface": "game_log_row",
            "target_field": "game_result",
            "original_value_label": "loss",
            "proposed_value_label": "win",
            "override_reason": "Synthetic display-only correction proposal.",
            "override_status": "proposed",
            "effect_scope": "journal_display_only",
            "author_label": "tester",
            "source_surface": "test_fixture",
            "privacy_label": "sanitized_fixture",
            "created_at": NOW,
            "updated_at": NOW,
        },
    )

    row = connection.execute("SELECT * FROM journal_field_overrides").fetchone()
    assert row["effect_scope"] == "journal_display_only"
    assert row["target_surface"] == "game_log_row"


@pytest.mark.parametrize(
    ("table_name", "values", "error_match"),
    [
        (
            "journal_matches",
            {
                "journal_match_id": "journal:match:bad",
                "attachment_status": "parser_truth",
                "created_at": NOW,
                "updated_at": NOW,
                "author_label": "tester",
                "source_surface": "test_fixture",
                "privacy_label": "sanitized_fixture",
            },
            "CHECK constraint failed",
        ),
        (
            "journal_matches",
            {
                "journal_match_id": "journal:match:bad",
                "attachment_status": "attached",
                "created_at": NOW,
                "updated_at": NOW,
                "author_label": "tester",
                "source_surface": "test_fixture",
                "privacy_label": "sanitized_fixture",
            },
            "CHECK constraint failed",
        ),
        (
            "journal_notes",
            {
                "journal_note_id": "journal:note:bad",
                "note_scope": "parser_fact",
                "note_text": "bad",
                "note_format": "plain_text",
                "author_label": "tester",
                "source_surface": "test_fixture",
                "privacy_label": "sanitized_fixture",
                "valid_from": NOW,
                "created_at": NOW,
                "updated_at": NOW,
            },
            "CHECK constraint failed",
        ),
        (
            "journal_labels",
            {
                "journal_label_id": "journal:label:bad",
                "label_scope": "review",
                "label_type": "pilot_error",
                "label_value": "misplay_truth",
                "author_label": "tester",
                "source_surface": "test_fixture",
                "privacy_label": "sanitized_fixture",
                "valid_from": NOW,
                "created_at": NOW,
                "updated_at": NOW,
            },
            "CHECK constraint failed",
        ),
        (
            "journal_field_overrides",
            {
                "journal_field_override_id": "journal:override:bad",
                "target_surface": "game_log_row",
                "target_field": "game_result",
                "proposed_value_label": "win",
                "effect_scope": "parser_fact_update",
                "author_label": "tester",
                "source_surface": "test_fixture",
                "privacy_label": "sanitized_fixture",
                "created_at": NOW,
                "updated_at": NOW,
            },
            "CHECK constraint failed",
        ),
    ],
)
def test_bounded_vocabularies_are_enforced(
    table_name: str,
    values: dict[str, object],
    error_match: str,
) -> None:
    connection = _connect_schema()

    with pytest.raises(sqlite3.IntegrityError, match=error_match):
        _insert_row(connection, table_name, values)


def test_match_journal_schema_can_share_memory_connection_with_analytics_schema() -> None:
    connection = _connect()

    apply_analytics_migrations(connection, applied_at="analytics")
    apply_match_journal_migrations(connection, applied_at="journal")

    table_names = _names(connection, "table")
    view_names = _names(connection, "view")
    assert {"matches", "games", "schema_migrations"} <= table_names
    assert REQUIRED_TABLES <= table_names
    assert {"v_opening_hand_cards", "v_play_draw_splits"} <= view_names
    assert connection.execute("SELECT COUNT(*) FROM journal_schema_migrations").fetchone()[0] == 1
    assert connection.execute("SELECT COUNT(*) FROM schema_migrations").fetchone()[0] == 1
