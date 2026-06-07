from __future__ import annotations

import sqlite3
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from mythic_edge_parser.app.match_journal_migration_loader import (
    MatchJournalMigrationError,
    iter_match_journal_migrations,
)
from mythic_edge_parser.app.match_journal_service import MatchJournalService

from .paths import LOCAL_APP_OBJECT_PREFIX, LOCAL_APP_SCHEMA_VERSION, LocalAppPaths, display_app_path

MATCH_JOURNAL_WRITE_CONTROLS_CAPABILITY = "match_journal_write_controls"
MATCH_JOURNAL_DATABASE_DISPLAY_PATH = display_app_path("db", "match_journal.sqlite3")


class LocalAppMatchJournalService:
    """Per-operation adapter over the app-owned local Match Journal database."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def get_journal_bundle(self, context: Mapping[str, object]) -> Mapping[str, object] | None:
        if not self._database_path.exists() or not self._database_path.is_file():
            return None
        return self._with_read_service(lambda service: service.get_journal_bundle(context))

    def get_unattached_note_summary(
        self,
        journal_note_id: str,
        *,
        smoke_marker_prefix: str,
    ) -> Mapping[str, object] | None:
        if not self._database_path.exists() or not self._database_path.is_file():
            return None

        def operation(service: MatchJournalService) -> Mapping[str, object] | None:
            note = service.repository.get_note(journal_note_id)
            if note is None or not _is_unattached_note(note):
                return None
            note_text = note.get("note_text")
            return {
                "journal_note_id": note["journal_note_id"],
                "note_scope": "unattached",
                "author_label": note["author_label"],
                "source_surface": note["source_surface"],
                "privacy_label": note["privacy_label"],
                "created_at": note["created_at"],
                "updated_at": note["updated_at"],
                "smoke_marker_present": isinstance(note_text, str) and note_text.startswith(smoke_marker_prefix),
                "attachment_status": "unattached",
            }

        return self._with_read_service(operation)

    def record_match_note(
        self,
        context: Mapping[str, object] | None,
        note_text: str,
        **options: object,
    ) -> Mapping[str, object]:
        return self._with_write_service(lambda service: service.record_match_note(context, note_text, **options))

    def record_game_note(
        self,
        context: Mapping[str, object] | None,
        note_text: str,
        **options: object,
    ) -> Mapping[str, object]:
        return self._with_write_service(lambda service: service.record_game_note(context, note_text, **options))

    def record_sideboarding_note(
        self,
        context: Mapping[str, object] | None,
        note_text: str,
        **options: object,
    ) -> Mapping[str, object]:
        return self._with_write_service(
            lambda service: service.record_sideboarding_note(context, note_text, **options)
        )

    def record_unattached_note(self, note_text: str, **options: object) -> Mapping[str, object]:
        return self._with_write_service(lambda service: service.record_unattached_note(note_text, **options))

    def set_opponent_labels(
        self,
        context: Mapping[str, object] | None,
        *,
        archetype: str | None = None,
        tier: str | None = None,
        **options: object,
    ) -> Mapping[str, object]:
        return self._with_write_service(
            lambda service: service.set_opponent_labels(context, archetype=archetype, tier=tier, **options)
        )

    def flag_for_review(
        self,
        context: Mapping[str, object] | None,
        flag_type: str,
        **options: object,
    ) -> Mapping[str, object]:
        return self._with_write_service(lambda service: service.flag_for_review(context, flag_type, **options))

    def set_experiment_label(
        self,
        context: Mapping[str, object] | None,
        experiment_id: str,
        **options: object,
    ) -> Mapping[str, object]:
        return self._with_write_service(
            lambda service: service.set_experiment_label(context, experiment_id, **options)
        )

    def propose_display_correction(
        self,
        context: Mapping[str, object] | None,
        request: Mapping[str, object],
    ) -> Mapping[str, object]:
        return self._with_write_service(lambda service: service.propose_display_correction(context, request))

    def _with_read_service(self, operation: Callable[[MatchJournalService], Any]) -> Any:
        uri = f"file:{self._database_path.resolve().as_posix()}?mode=ro"
        connection = sqlite3.connect(uri, uri=True, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        try:
            service = MatchJournalService.from_connection(connection)
            return operation(service)
        finally:
            connection.close()

    def _with_write_service(self, operation: Callable[[MatchJournalService], Any]) -> Any:
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self._database_path, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        try:
            service = MatchJournalService.from_connection(connection, ensure_schema=True)
            return operation(service)
        finally:
            connection.close()


def build_match_journal_service_factory(paths: LocalAppPaths) -> Callable[[], LocalAppMatchJournalService | None]:
    def factory() -> LocalAppMatchJournalService | None:
        if paths.match_journal_database is None:
            return None
        return LocalAppMatchJournalService(paths.match_journal_database)

    return factory


def _is_unattached_note(note: Mapping[str, object]) -> bool:
    return (
        note.get("note_scope") == "unattached"
        and note.get("journal_match_id") is None
        and note.get("journal_game_id") is None
        and note.get("parser_match_id") is None
        and note.get("parser_game_id") is None
    )


def build_match_journal_write_status(paths: LocalAppPaths) -> dict[str, object]:
    database_path = paths.match_journal_database
    if paths.app_data_root is None or database_path is None:
        return _status_payload(
            status="unavailable",
            app_data_root_status="unavailable",
            exists=False,
            kind="unknown",
            schema_status="unavailable",
            write_controls_status="unavailable",
            errors=["app_data_root_unavailable"],
        )
    if not database_path.exists():
        return _status_payload(
            status="not_initialized",
            app_data_root_status="available" if paths.app_data_root.exists() else "not_initialized",
            exists=False,
            kind="unknown",
            schema_status="not_initialized",
            write_controls_status="enabled_on_first_write",
            errors=[],
        )
    if not database_path.is_file():
        return _status_payload(
            status="error",
            app_data_root_status="available" if paths.app_data_root.exists() else "not_initialized",
            exists=True,
            kind="directory",
            schema_status="invalid_sqlite",
            write_controls_status="error",
            errors=["database_path_is_not_file"],
        )

    try:
        applied_migrations = _read_applied_journal_migrations(database_path)
        schema_status = _journal_schema_status(applied_migrations)
    except sqlite3.DatabaseError:
        return _status_payload(
            status="error",
            app_data_root_status="available" if paths.app_data_root.exists() else "not_initialized",
            exists=True,
            kind="file",
            schema_status="invalid_sqlite",
            write_controls_status="error",
            errors=["database_invalid_sqlite"],
        )
    except OSError:
        return _status_payload(
            status="error",
            app_data_root_status="available" if paths.app_data_root.exists() else "not_initialized",
            exists=True,
            kind="file",
            schema_status="unreadable",
            write_controls_status="error",
            errors=["database_unreadable"],
        )
    except MatchJournalMigrationError:
        return _status_payload(
            status="error",
            app_data_root_status="available" if paths.app_data_root.exists() else "not_initialized",
            exists=True,
            kind="file",
            schema_status="migration_error",
            write_controls_status="error",
            errors=["migration_discovery_error"],
        )

    return _status_payload(
        status="ready" if schema_status == "schema_current" else "degraded",
        app_data_root_status="available" if paths.app_data_root.exists() else "not_initialized",
        exists=True,
        kind="file",
        schema_status=schema_status,
        write_controls_status="enabled" if schema_status == "schema_current" else "degraded",
        errors=[],
        applied_migration_ids=[row["migration_id"] for row in applied_migrations],
    )


def _status_payload(
    *,
    status: str,
    app_data_root_status: str,
    exists: bool,
    kind: str,
    schema_status: str,
    write_controls_status: str,
    errors: list[str],
    applied_migration_ids: list[str] | None = None,
) -> dict[str, object]:
    return {
        "object": f"{LOCAL_APP_OBJECT_PREFIX}_match_journal_write_status",
        "schema_version": LOCAL_APP_SCHEMA_VERSION,
        "status": status,
        "app_data_root": {
            "display_path": display_app_path(),
            "status": app_data_root_status,
            "available": app_data_root_status == "available",
        },
        "database": {
            "display_path": MATCH_JOURNAL_DATABASE_DISPLAY_PATH,
            "exists": exists,
            "kind": kind,
            "path_ownership": "app_owned" if schema_status != "unavailable" else "unavailable",
            "schema_status": schema_status,
            "applied_migration_ids": list(applied_migration_ids or []),
        },
        "write_controls": {
            "status": write_controls_status,
            "browser_facade": "/api/journal/...",
            "direct_status_api": "forbidden",
        },
        "redaction_policy": "symbolic_app_data_paths_only",
        "errors": errors,
    }


def _read_applied_journal_migrations(database_path: Path) -> list[dict[str, str]]:
    uri = f"file:{database_path.resolve().as_posix()}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    try:
        table_exists = connection.execute(
            "SELECT 1 FROM sqlite_schema WHERE type = 'table' AND name = 'journal_schema_migrations'",
        ).fetchone()
        if table_exists is None:
            return []
        rows = connection.execute(
            "SELECT migration_id, checksum_sha256 FROM journal_schema_migrations ORDER BY migration_id",
        ).fetchall()
        return [
            {
                "migration_id": str(row["migration_id"]),
                "checksum_sha256": str(row["checksum_sha256"]),
            }
            for row in rows
        ]
    finally:
        connection.close()


def _journal_schema_status(applied_migrations: list[dict[str, str]]) -> str:
    if not applied_migrations:
        return "schema_unknown"
    expected = {migration.migration_id: migration.checksum_sha256 for migration in iter_match_journal_migrations()}
    applied = {row["migration_id"]: row["checksum_sha256"] for row in applied_migrations}
    if applied == expected:
        return "schema_current"
    return "schema_outdated"
