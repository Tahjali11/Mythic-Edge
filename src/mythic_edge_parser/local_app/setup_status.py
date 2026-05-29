from __future__ import annotations

import sqlite3
from pathlib import Path

from mythic_edge_parser.app.analytics_migration_loader import AnalyticsMigrationError, iter_analytics_migrations
from mythic_edge_parser.app.config import DEFAULT_MTGA_PLAYER_LOG

from .config import read_local_app_config
from .paths import (
    DEFAULT_BACKEND_HOST,
    LOCAL_APP_OBJECT_PREFIX,
    LOCAL_APP_SCHEMA_VERSION,
    LocalAppPaths,
    build_path_status,
    display_app_path,
)


def build_capabilities() -> dict[str, str]:
    return {
        "setup_status": "enabled",
        "config_write": "disabled",
        "database_init": "disabled",
        "manual_import": "disabled",
        "live_watcher": "disabled",
        "parser_runner_control": "disabled",
        "frontend": "deferred",
    }


def build_health_status() -> dict[str, object]:
    return {
        "object": f"{LOCAL_APP_OBJECT_PREFIX}_health",
        "schema_version": LOCAL_APP_SCHEMA_VERSION,
        "status": "ok",
        "mode": "setup_status_only",
        "capabilities": build_capabilities(),
    }


def build_player_log_path_status(paths: LocalAppPaths) -> dict[str, object]:
    config_read = read_local_app_config(paths)
    if config_read.status in {"invalid_json", "invalid_shape", "unreadable"}:
        player_log_status = "invalid_config"
        display_path = "<configured_player_log>"
    elif "player_log_path" in config_read.values:
        configured_path = Path(str(config_read.values["player_log_path"]))
        player_log_status = (
            "configured_exists" if configured_path.exists() and configured_path.is_file() else "configured_missing"
        )
        display_path = "<configured_player_log>"
    elif DEFAULT_MTGA_PLAYER_LOG.exists() and DEFAULT_MTGA_PLAYER_LOG.is_file():
        player_log_status = "detected_exists"
        display_path = "<detected_mtga_player_log>"
    elif paths.app_data_root is None:
        player_log_status = "unavailable"
        display_path = "<detected_mtga_player_log>"
    else:
        player_log_status = "missing"
        display_path = "<detected_mtga_player_log>"

    return {
        "object": f"{LOCAL_APP_OBJECT_PREFIX}_player_log_status",
        "schema_version": LOCAL_APP_SCHEMA_VERSION,
        "status": _top_level_status(player_log_status),
        "player_log": {
            "status": player_log_status,
            "display_path": display_path,
            "contents_read": False,
        },
        "errors": [] if player_log_status != "invalid_config" else ["player_log_config_invalid"],
    }


def build_analytics_database_status(paths: LocalAppPaths) -> dict[str, object]:
    database_path = paths.analytics_database
    if database_path is None:
        return _database_status_payload(
            status="unavailable",
            schema_status="unavailable",
            exists=False,
            kind="unknown",
            applied_migration_ids=[],
            errors=["app_data_root_unavailable"],
        )
    if not database_path.exists():
        return _database_status_payload(
            status="missing",
            schema_status="missing",
            exists=False,
            kind="unknown",
            applied_migration_ids=[],
            errors=[],
        )
    if not database_path.is_file():
        return _database_status_payload(
            status="error",
            schema_status="invalid_sqlite",
            exists=True,
            kind="directory",
            applied_migration_ids=[],
            errors=["database_path_is_not_file"],
        )

    try:
        applied_migrations = _read_applied_migrations(database_path)
        schema_status = _schema_status(applied_migrations)
    except sqlite3.DatabaseError:
        return _database_status_payload(
            status="error",
            schema_status="invalid_sqlite",
            exists=True,
            kind="file",
            applied_migration_ids=[],
            errors=["database_invalid_sqlite"],
        )
    except OSError:
        return _database_status_payload(
            status="error",
            schema_status="unreadable",
            exists=True,
            kind="file",
            applied_migration_ids=[],
            errors=["database_unreadable"],
        )
    except AnalyticsMigrationError:
        return _database_status_payload(
            status="error",
            schema_status="migration_error",
            exists=True,
            kind="file",
            applied_migration_ids=[],
            errors=["migration_discovery_error"],
        )

    return _database_status_payload(
        status="ok" if schema_status == "schema_current" else "degraded",
        schema_status=schema_status,
        exists=True,
        kind="file",
        applied_migration_ids=[row["migration_id"] for row in applied_migrations],
        errors=[],
    )


def build_migration_loader_status() -> dict[str, object]:
    try:
        migrations = iter_analytics_migrations()
    except AnalyticsMigrationError:
        return {
            "object": f"{LOCAL_APP_OBJECT_PREFIX}_migration_loader_status",
            "schema_version": LOCAL_APP_SCHEMA_VERSION,
            "status": "error",
            "migration_status": "error",
            "migrations": [],
            "errors": ["migration_discovery_error"],
        }

    return {
        "object": f"{LOCAL_APP_OBJECT_PREFIX}_migration_loader_status",
        "schema_version": LOCAL_APP_SCHEMA_VERSION,
        "status": "ok" if migrations else "missing",
        "migration_status": "available" if migrations else "missing",
        "migrations": [
            {
                "migration_id": migration.migration_id,
                "filename": migration.filename,
                "schema_version_after": migration.schema_version_after,
                "checksum_present": bool(migration.checksum_sha256),
            }
            for migration in migrations
        ],
        "errors": [],
    }


def build_runtime_state() -> dict[str, object]:
    return {
        "object": f"{LOCAL_APP_OBJECT_PREFIX}_runtime" + "_status",
        "schema_version": LOCAL_APP_SCHEMA_VERSION,
        "status": "ok",
        "backend": {"status": "running", "host": DEFAULT_BACKEND_HOST},
        "parser_runner": {"status": "deferred"},
        "live_watcher": {"status": "deferred"},
        "manual_import": {"status": "deferred"},
        "legacy_status_api": {"status": "separate_reference_surface"},
    }


def build_setup_status(paths: LocalAppPaths) -> dict[str, object]:
    path_status = build_path_status(paths)
    from .config import load_local_app_config_status

    config_status = load_local_app_config_status(paths)
    player_log_status = build_player_log_path_status(paths)
    database_status = build_analytics_database_status(paths)
    migration_status = build_migration_loader_status()
    runtime_section = build_runtime_state()
    sections = {
        "paths": path_status,
        "config": config_status,
        "player_log": player_log_status,
        "analytics_database": database_status,
        "migrations": migration_status,
        "runtime": runtime_section,
    }
    return {
        "object": f"{LOCAL_APP_OBJECT_PREFIX}_setup_status",
        "schema_version": LOCAL_APP_SCHEMA_VERSION,
        "status": _combined_status(sections),
        **sections,
        "capabilities": build_capabilities(),
    }


def _read_applied_migrations(database_path: Path) -> list[dict[str, str]]:
    uri = f"file:{database_path.resolve().as_posix()}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    try:
        table_exists = connection.execute(
            "SELECT 1 FROM sqlite_schema WHERE type = 'table' AND name = 'schema_migrations'",
        ).fetchone()
        if table_exists is None:
            return []
        rows = connection.execute(
            "SELECT migration_id, checksum_sha256 FROM schema_migrations ORDER BY migration_id",
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


def _schema_status(applied_migrations: list[dict[str, str]]) -> str:
    if not applied_migrations:
        return "schema_unknown"
    expected = {migration.migration_id: migration.checksum_sha256 for migration in iter_analytics_migrations()}
    applied = {row["migration_id"]: row["checksum_sha256"] for row in applied_migrations}
    if applied == expected:
        return "schema_current"
    return "schema_outdated"


def _database_status_payload(
    *,
    status: str,
    schema_status: str,
    exists: bool,
    kind: str,
    applied_migration_ids: list[str],
    errors: list[str],
) -> dict[str, object]:
    return {
        "object": f"{LOCAL_APP_OBJECT_PREFIX}_analytics_database_status",
        "schema_version": LOCAL_APP_SCHEMA_VERSION,
        "status": status,
        "database": {
            "display_path": display_app_path("db", "mythic_edge.sqlite3"),
            "exists": exists,
            "kind": kind,
            "schema_status": schema_status,
            "applied_migration_ids": applied_migration_ids,
        },
        "migrations": build_migration_loader_status(),
        "errors": errors,
    }


def _top_level_status(section_status: str) -> str:
    if section_status.endswith("_exists"):
        return "ok"
    if section_status in {"missing", "configured_missing", "detected_missing"}:
        return "missing"
    if section_status == "unavailable":
        return "unavailable"
    return "error"


def _combined_status(sections: dict[str, dict[str, object]]) -> str:
    statuses = {str(section.get("status")) for section in sections.values()}
    if "unavailable" in statuses:
        return "unavailable"
    if "error" in statuses:
        return "error"
    if statuses == {"ok"}:
        return "ok"
    return "degraded"
