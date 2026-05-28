from __future__ import annotations

import hashlib
import re
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib import resources
from importlib.resources.abc import Traversable

ANALYTICS_SCHEMA_VERSION = "analytics_local_sqlite_schema.v1"
ANALYTICS_MIGRATIONS_PACKAGE = "mythic_edge_parser.app.analytics_migrations"

_MIGRATION_FILENAME_RE = re.compile(r"^(?P<prefix>\d{4})_[a-z0-9_]+\.sql$")
_SCHEMA_VERSION_BY_MIGRATION_ID = {
    "0001_initial_analytics_schema": ANALYTICS_SCHEMA_VERSION,
}


class AnalyticsMigrationError(RuntimeError):
    """Raised when analytics migration discovery or application fails."""


@dataclass(frozen=True, slots=True)
class AnalyticsMigration:
    migration_id: str
    filename: str
    schema_version_after: str
    checksum_sha256: str
    sql: str


def iter_analytics_migrations() -> tuple[AnalyticsMigration, ...]:
    resources_by_id: dict[str, Traversable] = {}
    for migration_resource in _migration_resources():
        migration_id = _migration_id_from_filename(migration_resource.name)
        if migration_id in resources_by_id:
            raise AnalyticsMigrationError(f"Duplicate analytics migration id: {migration_id}")
        resources_by_id[migration_id] = migration_resource

    if "0001_initial_analytics_schema" not in resources_by_id:
        raise AnalyticsMigrationError("Missing required analytics migration: 0001_initial_analytics_schema.sql")

    migrations = tuple(_load_migration_from_resource(resources_by_id[migration_id]) for migration_id in resources_by_id)
    return tuple(sorted(migrations, key=lambda migration: migration.filename[:4]))


def load_analytics_migration(migration_id: str) -> AnalyticsMigration:
    normalized_id = str(migration_id or "").strip()
    for migration in iter_analytics_migrations():
        if migration.migration_id == normalized_id:
            return migration
    raise AnalyticsMigrationError(f"Unknown analytics migration id: {normalized_id}")


def load_analytics_migration_sql(filename: str) -> str:
    normalized_filename = str(filename or "").strip()
    if not normalized_filename:
        raise AnalyticsMigrationError("Analytics migration filename is required")
    _migration_id_from_filename(normalized_filename)
    for migration_resource in _migration_resources():
        if migration_resource.name == normalized_filename:
            return _read_resource_text(migration_resource)
    raise AnalyticsMigrationError(f"Missing analytics migration resource: {normalized_filename}")


def apply_analytics_migrations(
    connection: sqlite3.Connection,
    *,
    applied_at: str | None = None,
) -> tuple[AnalyticsMigration, ...]:
    if connection.in_transaction:
        raise AnalyticsMigrationError(
            "Cannot apply analytics migrations while the SQLite connection already has an open transaction"
        )

    migrations = iter_analytics_migrations()
    applied_timestamp = applied_at or datetime.now(UTC).isoformat()
    connection.execute("PRAGMA foreign_keys = ON")

    applied: list[AnalyticsMigration] = []
    for migration in migrations:
        existing_checksum = _existing_migration_checksum(connection, migration.migration_id)
        if existing_checksum is not None:
            if existing_checksum != migration.checksum_sha256:
                raise AnalyticsMigrationError(
                    f"Checksum mismatch for analytics migration {migration.migration_id}: "
                    f"recorded {existing_checksum}, expected {migration.checksum_sha256}"
                )
            applied.append(migration)
            continue

        _apply_one_migration(connection, migration, applied_timestamp)
        applied.append(migration)

    return tuple(applied)


def _migration_resources() -> tuple[Traversable, ...]:
    try:
        migration_root = resources.files(ANALYTICS_MIGRATIONS_PACKAGE)
    except (ModuleNotFoundError, FileNotFoundError) as exc:
        raise AnalyticsMigrationError(
            f"Unable to load analytics migrations package: {ANALYTICS_MIGRATIONS_PACKAGE}"
        ) from exc

    candidates: list[Traversable] = []
    for child in migration_root.iterdir():
        if child.name.endswith(".sql"):
            _migration_id_from_filename(child.name)
            candidates.append(child)
    return tuple(sorted(candidates, key=lambda child: child.name))


def _migration_id_from_filename(filename: str) -> str:
    if _MIGRATION_FILENAME_RE.fullmatch(filename) is None:
        raise AnalyticsMigrationError(f"Invalid analytics migration filename: {filename}")
    migration_id = filename.removesuffix(".sql")
    if migration_id not in _SCHEMA_VERSION_BY_MIGRATION_ID:
        raise AnalyticsMigrationError(f"Unsupported analytics migration id: {migration_id}")
    return migration_id


def _load_migration_from_resource(migration_resource: Traversable) -> AnalyticsMigration:
    migration_id = _migration_id_from_filename(migration_resource.name)
    sql = _read_resource_text(migration_resource)
    checksum = hashlib.sha256(sql.encode("utf-8")).hexdigest()
    return AnalyticsMigration(
        migration_id=migration_id,
        filename=migration_resource.name,
        schema_version_after=_SCHEMA_VERSION_BY_MIGRATION_ID[migration_id],
        checksum_sha256=checksum,
        sql=sql,
    )


def _read_resource_text(migration_resource: Traversable) -> str:
    try:
        sql = migration_resource.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise AnalyticsMigrationError(f"Missing analytics migration resource: {migration_resource.name}") from exc
    if not sql.strip():
        raise AnalyticsMigrationError(f"Analytics migration resource is empty: {migration_resource.name}")
    return sql


def _existing_migration_checksum(connection: sqlite3.Connection, migration_id: str) -> str | None:
    if not _schema_migrations_table_exists(connection):
        return None
    row = connection.execute(
        "SELECT checksum_sha256 FROM schema_migrations WHERE migration_id = ?",
        (migration_id,),
    ).fetchone()
    if row is None:
        return None
    return str(row[0])


def _schema_migrations_table_exists(connection: sqlite3.Connection) -> bool:
    row = connection.execute(
        "SELECT 1 FROM sqlite_schema WHERE type = 'table' AND name = 'schema_migrations'",
    ).fetchone()
    return row is not None


def _apply_one_migration(
    connection: sqlite3.Connection,
    migration: AnalyticsMigration,
    applied_at: str,
) -> None:
    try:
        connection.execute("BEGIN")
        for statement in _sql_statements(migration.sql):
            connection.execute(statement)
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
            (
                migration.migration_id,
                migration.filename,
                migration.checksum_sha256,
                applied_at,
                migration.schema_version_after,
            ),
        )
        connection.commit()
    except AnalyticsMigrationError:
        connection.rollback()
        raise
    except sqlite3.Error as exc:
        connection.rollback()
        raise AnalyticsMigrationError(f"Failed to apply analytics migration {migration.filename}: {exc}") from exc


def _sql_statements(sql: str) -> tuple[str, ...]:
    statements: list[str] = []
    pending_lines: list[str] = []
    for line in sql.splitlines():
        pending_lines.append(line)
        pending_sql = "\n".join(pending_lines).strip()
        if pending_sql and sqlite3.complete_statement(pending_sql):
            statements.append(pending_sql)
            pending_lines.clear()

    remainder = "\n".join(pending_lines).strip()
    if remainder:
        raise AnalyticsMigrationError("Analytics migration SQL ended with an incomplete statement")
    return tuple(statements)
