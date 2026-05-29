from __future__ import annotations

import hashlib
import re
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib import resources
from importlib.resources.abc import Traversable

MATCH_JOURNAL_SCHEMA_VERSION = "match_journal_local_sqlite_schema.v1"
MATCH_JOURNAL_MIGRATIONS_PACKAGE = "mythic_edge_parser.app.match_journal_migrations"
DEFAULT_MATCH_JOURNAL_DATABASE_PATH = "data/match_journal/mythic_edge_journal.sqlite3"

_MIGRATION_FILENAME_RE = re.compile(r"^(?P<prefix>\d{4})_[a-z0-9_]+\.sql$")
_SCHEMA_VERSION_BY_MIGRATION_ID = {
    "0001_initial_match_journal_schema": MATCH_JOURNAL_SCHEMA_VERSION,
}


class MatchJournalMigrationError(RuntimeError):
    """Raised when Match Journal migration discovery or application fails."""


@dataclass(frozen=True, slots=True)
class MatchJournalMigration:
    migration_id: str
    filename: str
    schema_version_after: str
    checksum_sha256: str
    sql: str


def iter_match_journal_migrations() -> tuple[MatchJournalMigration, ...]:
    resources_by_id: dict[str, Traversable] = {}
    for migration_resource in _migration_resources():
        migration_id = _migration_id_from_filename(migration_resource.name)
        if migration_id in resources_by_id:
            raise MatchJournalMigrationError(f"Duplicate Match Journal migration id: {migration_id}")
        resources_by_id[migration_id] = migration_resource

    if "0001_initial_match_journal_schema" not in resources_by_id:
        raise MatchJournalMigrationError(
            "Missing required Match Journal migration: 0001_initial_match_journal_schema.sql"
        )

    migrations = tuple(_load_migration_from_resource(resources_by_id[migration_id]) for migration_id in resources_by_id)
    return tuple(sorted(migrations, key=lambda migration: migration.filename[:4]))


def load_match_journal_migration(migration_id: str) -> MatchJournalMigration:
    normalized_id = str(migration_id or "").strip()
    for migration in iter_match_journal_migrations():
        if migration.migration_id == normalized_id:
            return migration
    raise MatchJournalMigrationError(f"Unknown Match Journal migration id: {normalized_id}")


def load_match_journal_migration_sql(migration_id: str) -> str:
    normalized_id = _migration_id_from_identifier(migration_id)
    filename = f"{normalized_id}.sql"
    for migration_resource in _migration_resources():
        if migration_resource.name == filename:
            return _read_resource_text(migration_resource)
    raise MatchJournalMigrationError(f"Missing Match Journal migration resource: {filename}")


def apply_match_journal_migrations(
    connection: sqlite3.Connection,
    *,
    applied_at: str | None = None,
) -> tuple[MatchJournalMigration, ...]:
    if connection.in_transaction:
        raise MatchJournalMigrationError(
            "Cannot apply Match Journal migrations while the SQLite connection already has an open transaction"
        )

    migrations = iter_match_journal_migrations()
    applied_timestamp = applied_at or datetime.now(UTC).isoformat()
    connection.execute("PRAGMA foreign_keys = ON")

    applied: list[MatchJournalMigration] = []
    for migration in migrations:
        existing_checksum = _existing_migration_checksum(connection, migration.migration_id)
        if existing_checksum is not None:
            if existing_checksum != migration.checksum_sha256:
                raise MatchJournalMigrationError(
                    f"Checksum mismatch for Match Journal migration {migration.migration_id}: "
                    f"recorded {existing_checksum}, expected {migration.checksum_sha256}"
                )
            applied.append(migration)
            continue

        _apply_one_migration(connection, migration, applied_timestamp)
        applied.append(migration)

    return tuple(applied)


def _migration_resources() -> tuple[Traversable, ...]:
    try:
        migration_root = resources.files(MATCH_JOURNAL_MIGRATIONS_PACKAGE)
    except (ModuleNotFoundError, FileNotFoundError) as exc:
        raise MatchJournalMigrationError(
            f"Unable to load Match Journal migrations package: {MATCH_JOURNAL_MIGRATIONS_PACKAGE}"
        ) from exc

    candidates: list[Traversable] = []
    for child in migration_root.iterdir():
        if child.name.endswith(".sql"):
            _migration_id_from_filename(child.name)
            candidates.append(child)
    return tuple(sorted(candidates, key=lambda child: child.name))


def _migration_id_from_identifier(identifier: str) -> str:
    normalized = str(identifier or "").strip()
    if not normalized:
        raise MatchJournalMigrationError("Match Journal migration id is required")
    if normalized.endswith(".sql"):
        return _migration_id_from_filename(normalized)
    if normalized not in _SCHEMA_VERSION_BY_MIGRATION_ID:
        raise MatchJournalMigrationError(f"Unsupported Match Journal migration id: {normalized}")
    return normalized


def _migration_id_from_filename(filename: str) -> str:
    if _MIGRATION_FILENAME_RE.fullmatch(filename) is None:
        raise MatchJournalMigrationError(f"Invalid Match Journal migration filename: {filename}")
    migration_id = filename.removesuffix(".sql")
    if migration_id not in _SCHEMA_VERSION_BY_MIGRATION_ID:
        raise MatchJournalMigrationError(f"Unsupported Match Journal migration id: {migration_id}")
    return migration_id


def _load_migration_from_resource(migration_resource: Traversable) -> MatchJournalMigration:
    migration_id = _migration_id_from_filename(migration_resource.name)
    sql = _read_resource_text(migration_resource)
    checksum = hashlib.sha256(sql.encode("utf-8")).hexdigest()
    return MatchJournalMigration(
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
        raise MatchJournalMigrationError(
            f"Missing Match Journal migration resource: {migration_resource.name}"
        ) from exc
    if not sql.strip():
        raise MatchJournalMigrationError(f"Match Journal migration resource is empty: {migration_resource.name}")
    return sql


def _existing_migration_checksum(connection: sqlite3.Connection, migration_id: str) -> str | None:
    if not _journal_schema_migrations_table_exists(connection):
        return None
    row = connection.execute(
        "SELECT checksum_sha256 FROM journal_schema_migrations WHERE migration_id = ?",
        (migration_id,),
    ).fetchone()
    if row is None:
        return None
    return str(row[0])


def _journal_schema_migrations_table_exists(connection: sqlite3.Connection) -> bool:
    row = connection.execute(
        "SELECT 1 FROM sqlite_schema WHERE type = 'table' AND name = 'journal_schema_migrations'",
    ).fetchone()
    return row is not None


def _apply_one_migration(
    connection: sqlite3.Connection,
    migration: MatchJournalMigration,
    applied_at: str,
) -> None:
    try:
        connection.execute("BEGIN")
        for statement in _sql_statements(migration.sql):
            connection.execute(statement)
        connection.execute(
            """
            INSERT INTO journal_schema_migrations (
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
    except MatchJournalMigrationError:
        connection.rollback()
        raise
    except sqlite3.Error as exc:
        connection.rollback()
        raise MatchJournalMigrationError(
            f"Failed to apply Match Journal migration {migration.filename}: {exc}"
        ) from exc


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
        raise MatchJournalMigrationError("Match Journal migration SQL ended with an incomplete statement")
    return tuple(statements)
