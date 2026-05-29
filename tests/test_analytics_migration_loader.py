from __future__ import annotations

import os
import re
import sqlite3
import tomllib
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

import pytest

from mythic_edge_parser.app import analytics_migration_loader as loader
from mythic_edge_parser.app.analytics_migration_loader import (
    ANALYTICS_MIGRATIONS_PACKAGE,
    ANALYTICS_SCHEMA_VERSION,
    AnalyticsMigrationError,
    apply_analytics_migrations,
    iter_analytics_migrations,
    load_analytics_migration,
    load_analytics_migration_sql,
)

FIRST_MIGRATION_FILENAME = "0001_initial_analytics_schema.sql"
FIRST_MIGRATION_ID = "0001_initial_analytics_schema"


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
    return connection


def _names(connection: sqlite3.Connection, object_type: str) -> set[str]:
    rows = connection.execute("SELECT name FROM sqlite_schema WHERE type = ?", (object_type,)).fetchall()
    return {str(row["name"]) for row in rows if not str(row["name"]).startswith("sqlite_")}


def test_migration_package_resource_can_be_loaded() -> None:
    migration_path = resources.files(ANALYTICS_MIGRATIONS_PACKAGE).joinpath(FIRST_MIGRATION_FILENAME)

    assert migration_path.is_file()
    assert "CREATE TABLE schema_migrations" in migration_path.read_text(encoding="utf-8")


def test_pyproject_includes_analytics_sql_package_data() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    package_data = pyproject["tool"]["setuptools"]["package-data"]
    assert package_data[ANALYTICS_MIGRATIONS_PACKAGE] == ["*.sql"]


def test_iter_analytics_migrations_returns_first_migration_in_deterministic_order() -> None:
    migrations = iter_analytics_migrations()

    assert [migration.filename for migration in migrations] == [FIRST_MIGRATION_FILENAME]
    assert migrations[0].migration_id == FIRST_MIGRATION_ID
    assert migrations[0].schema_version_after == ANALYTICS_SCHEMA_VERSION
    assert re.fullmatch(r"[0-9a-f]{64}", migrations[0].checksum_sha256)


def test_load_analytics_migration_sql_reads_package_resource_from_any_cwd(tmp_path: Path) -> None:
    original_cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        sql = load_analytics_migration_sql(FIRST_MIGRATION_FILENAME)
    finally:
        os.chdir(original_cwd)

    assert "CREATE TABLE schema_migrations" in sql
    assert str(tmp_path) not in sql


def test_load_analytics_migration_returns_exact_checksum_and_sql() -> None:
    migration = load_analytics_migration(FIRST_MIGRATION_ID)
    sql = load_analytics_migration_sql(FIRST_MIGRATION_FILENAME)

    assert migration.sql == sql
    assert migration.checksum_sha256 == iter_analytics_migrations()[0].checksum_sha256


def test_apply_analytics_migrations_creates_schema_and_records_history() -> None:
    connection = _connect()
    migrations = apply_analytics_migrations(connection, applied_at="2026-05-28T00:00:00Z")

    assert [migration.migration_id for migration in migrations] == [FIRST_MIGRATION_ID]
    assert {"schema_migrations", "matches", "games", "fact_provenance"} <= _names(connection, "table")
    assert {"v_opening_hand_cards", "v_play_draw_splits"} <= _names(connection, "view")

    row = connection.execute("SELECT * FROM schema_migrations WHERE migration_id = ?", (FIRST_MIGRATION_ID,)).fetchone()
    assert row["migration_filename"] == FIRST_MIGRATION_FILENAME
    assert row["checksum_sha256"] == migrations[0].checksum_sha256
    assert row["applied_at"] == "2026-05-28T00:00:00Z"
    assert row["schema_version_after"] == ANALYTICS_SCHEMA_VERSION


def test_apply_analytics_migrations_is_idempotent_on_same_connection() -> None:
    connection = _connect()

    first = apply_analytics_migrations(connection, applied_at="first")
    second = apply_analytics_migrations(connection, applied_at="second")

    rows = connection.execute("SELECT * FROM schema_migrations").fetchall()
    assert len(rows) == 1
    assert rows[0]["checksum_sha256"] == first[0].checksum_sha256
    assert rows[0]["applied_at"] == "first"
    assert second == first


def test_preexisting_same_checksum_is_accepted() -> None:
    connection = _connect()

    first = apply_analytics_migrations(connection, applied_at="first")
    second = apply_analytics_migrations(connection, applied_at="already-present")

    assert second[0].checksum_sha256 == first[0].checksum_sha256
    assert connection.execute("SELECT COUNT(*) AS count FROM schema_migrations").fetchone()["count"] == 1


def test_preexisting_different_checksum_is_rejected_without_overwrite() -> None:
    connection = _connect()
    apply_analytics_migrations(connection, applied_at="first")
    connection.execute(
        "UPDATE schema_migrations SET checksum_sha256 = ? WHERE migration_id = ?",
        ("0" * 64, FIRST_MIGRATION_ID),
    )
    connection.commit()

    with pytest.raises(AnalyticsMigrationError, match="Checksum mismatch"):
        apply_analytics_migrations(connection, applied_at="second")

    row = connection.execute("SELECT checksum_sha256 FROM schema_migrations").fetchone()
    assert row["checksum_sha256"] == "0" * 64


def test_missing_package_fails_clearly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(loader, "ANALYTICS_MIGRATIONS_PACKAGE", "mythic_edge_parser.app.not_a_package")

    with pytest.raises(AnalyticsMigrationError, match="Unable to load analytics migrations package"):
        iter_analytics_migrations()


def test_missing_first_migration_fails_clearly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(loader, "_migration_resources", lambda: ())

    with pytest.raises(AnalyticsMigrationError, match=FIRST_MIGRATION_FILENAME):
        iter_analytics_migrations()


def test_invalid_migration_filename_fails_clearly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(loader, "_migration_resources", lambda: (FakeResource("not_a_migration.sql", "SELECT 1;"),))

    with pytest.raises(AnalyticsMigrationError, match="Invalid analytics migration filename"):
        iter_analytics_migrations()


def test_duplicate_migration_ids_fail_clearly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        loader,
        "_migration_resources",
        lambda: (
            FakeResource(FIRST_MIGRATION_FILENAME, "SELECT 1;"),
            FakeResource(FIRST_MIGRATION_FILENAME, "SELECT 2;"),
        ),
    )

    with pytest.raises(AnalyticsMigrationError, match="Duplicate analytics migration id"):
        iter_analytics_migrations()


def test_open_caller_transaction_is_rejected() -> None:
    connection = _connect()
    connection.execute("BEGIN")

    with pytest.raises(AnalyticsMigrationError, match="open transaction"):
        apply_analytics_migrations(connection)


def test_incomplete_migration_sql_rolls_back_without_history(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        loader,
        "_migration_resources",
        lambda: (FakeResource(FIRST_MIGRATION_FILENAME, "CREATE TABLE broken ("),),
    )
    connection = _connect()

    with pytest.raises(AnalyticsMigrationError, match="incomplete statement"):
        apply_analytics_migrations(connection)

    assert not connection.in_transaction
    row = connection.execute(
        "SELECT 1 FROM sqlite_schema WHERE type = 'table' AND name = 'schema_migrations'",
    ).fetchone()
    assert row is None
