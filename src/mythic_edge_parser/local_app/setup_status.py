from __future__ import annotations

import sqlite3
import stat
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from mythic_edge_parser.app.analytics_migration_loader import AnalyticsMigrationError, iter_analytics_migrations
from mythic_edge_parser.app.config import DEFAULT_MTGA_PLAYER_LOG

from .config import read_local_app_config
from .match_journal_runtime import (
    MATCH_JOURNAL_WRITE_CONTROLS_CAPABILITY,
    build_match_journal_write_status,
)
from .paths import (
    DEFAULT_BACKEND_HOST,
    LOCAL_APP_OBJECT_PREFIX,
    LOCAL_APP_SCHEMA_VERSION,
    LocalAppPaths,
    build_path_status,
    display_app_path,
)

LIVE_STATUS_SCHEMA_VERSION = "live_app_player_log_path_watcher_status.v1"
LIVE_SQLITE_CAPTURE_SCHEMA_VERSION = "live_app_parser_owned_fact_capture_sqlite.v1"
LIVE_PLAYER_LOG_STATUS_OBJECT = "mythic_edge_local_app_live_player_log_status"
LIVE_WATCHER_STATUS_OBJECT = "mythic_edge_local_app_live_watcher_status"
LIVE_SQLITE_CAPTURE_STATUS_OBJECT = "mythic_edge_local_app_live_parser_sqlite_capture_status"
PLAYER_LOG_RECENT_ACTIVITY_SECONDS = 24 * 60 * 60


@dataclass(frozen=True, slots=True)
class _PlayerLogCandidate:
    path: Path | None
    source: str
    display_path: str
    status_prefix: str


@dataclass(frozen=True, slots=True)
class _PlayerLogMetadata:
    exists: bool
    path_kind: str
    metadata_access: str
    size_bytes: int | None
    last_modified_at: str | None
    last_modified_age_seconds: float | None
    activity_hint: str
    diagnostics: tuple[str, ...]
    warnings: tuple[str, ...]
    errors: tuple[str, ...]


def build_capabilities(*, match_journal_write_controls: str = "enabled") -> dict[str, str]:
    return {
        "setup_status": "enabled",
        "config_write": "disabled",
        "database_init": "disabled",
        "manual_import": "enabled",
        MATCH_JOURNAL_WRITE_CONTROLS_CAPABILITY: match_journal_write_controls,
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
    live_status = build_live_player_log_status(paths)
    return {
        "object": f"{LOCAL_APP_OBJECT_PREFIX}_player_log_status",
        "schema_version": LOCAL_APP_SCHEMA_VERSION,
        "status": live_status["status"],
        "player_log": live_status["player_log"],
        "diagnostics": live_status["diagnostics"],
        "warnings": live_status["warnings"],
        "errors": live_status["errors"],
    }


def build_live_player_log_status(paths: LocalAppPaths) -> dict[str, object]:
    config_read = read_local_app_config(paths)
    if paths.app_data_root is None:
        player_log_status = "unavailable"
        candidate = _PlayerLogCandidate(
            path=None,
            source="unavailable",
            display_path="<player_log_unavailable>",
            status_prefix="unavailable",
        )
        metadata = _unavailable_player_log_metadata()
    elif config_read.status in {"invalid_json", "invalid_shape", "unreadable"}:
        player_log_status = "invalid_config"
        candidate = _PlayerLogCandidate(
            path=None,
            source="configured",
            display_path="<configured_player_log>",
            status_prefix="configured",
        )
        metadata = _invalid_config_player_log_metadata()
    elif "player_log_path" in config_read.values:
        player_log_value = config_read.values["player_log_path"]
        if not isinstance(player_log_value, str) or not player_log_value.strip():
            player_log_status = "invalid_config"
            candidate = _PlayerLogCandidate(
                path=None,
                source="configured",
                display_path="<configured_player_log>",
                status_prefix="configured",
            )
            metadata = _invalid_config_player_log_metadata()
        else:
            candidate = _PlayerLogCandidate(
                path=Path(player_log_value),
                source="configured",
                display_path="<configured_player_log>",
                status_prefix="configured",
            )
            metadata = _metadata_for_player_log(candidate.path)
            player_log_status = _player_log_status_for_metadata(candidate, metadata)
    else:
        candidate = _PlayerLogCandidate(
            path=DEFAULT_MTGA_PLAYER_LOG,
            source="detected_default",
            display_path="<detected_mtga_player_log>",
            status_prefix="detected",
        )
        metadata = _metadata_for_player_log(candidate.path)
        player_log_status = _player_log_status_for_metadata(candidate, metadata)

    return {
        "object": LIVE_PLAYER_LOG_STATUS_OBJECT,
        "schema_version": LIVE_STATUS_SCHEMA_VERSION,
        "status": _top_level_status(player_log_status),
        "player_log": {
            "status": player_log_status,
            "source": candidate.source,
            "display_path": candidate.display_path,
            "path_kind": metadata.path_kind,
            "metadata_access": metadata.metadata_access,
            "exists": metadata.exists,
            "contents_read": False,
            "tailing_started": False,
            "size_bytes": metadata.size_bytes,
            "last_modified_at": metadata.last_modified_at,
            "last_modified_age_seconds": metadata.last_modified_age_seconds,
            "activity_hint": metadata.activity_hint,
        },
        "diagnostics": list(metadata.diagnostics),
        "warnings": list(metadata.warnings),
        "errors": list(metadata.errors),
    }


def build_live_watcher_status(paths: LocalAppPaths) -> dict[str, object]:
    player_log_status = build_live_player_log_status(paths)
    player_log = player_log_status["player_log"]
    if not isinstance(player_log, dict):
        player_log = {}
    watcher_status, reason = _watcher_status_for_player_log(str(player_log.get("status", "unavailable")))
    warnings_value = player_log_status.get("warnings", [])
    errors_value = player_log_status.get("errors", [])
    warnings = list(warnings_value) if isinstance(warnings_value, list) else []
    errors = list(errors_value) if isinstance(errors_value, list) else []

    return {
        "object": LIVE_WATCHER_STATUS_OBJECT,
        "schema_version": LIVE_STATUS_SCHEMA_VERSION,
        "status": watcher_status,
        "watcher": {
            "status": watcher_status,
            "mode": "readiness_only",
            "running": False,
            "start_allowed": False,
            "stop_allowed": False,
            "parser_runner_started": False,
            "tailing_started": False,
            "sqlite_live_writes_enabled": False,
            "reason": reason,
        },
        "player_log": {
            "status": player_log.get("status", "unavailable"),
            "source": player_log.get("source", "unavailable"),
            "display_path": player_log.get("display_path", "<player_log_unavailable>"),
            "path_kind": player_log.get("path_kind", "unavailable"),
            "metadata_access": player_log.get("metadata_access", "unavailable"),
            "exists": bool(player_log.get("exists", False)),
            "contents_read": False,
            "tailing_started": False,
        },
        "warnings": warnings,
        "errors": errors,
    }


def build_live_sqlite_capture_status(paths: LocalAppPaths) -> dict[str, object]:
    database_configured = paths.analytics_database is not None
    return {
        "object": LIVE_SQLITE_CAPTURE_STATUS_OBJECT,
        "schema_version": LIVE_SQLITE_CAPTURE_SCHEMA_VERSION,
        "status": "disabled",
        "mode": "status_only",
        "source_kind": "live_parser",
        "database": {
            "configured": database_configured,
            "display_path": display_app_path("db", "mythic_edge.sqlite3")
            if database_configured
            else "<app_data_unavailable>",
        },
        "capabilities": {
            "live_sqlite_capture_contract_present": True,
            "final_match_game_fact_capture_supported": True,
            "provisional_fact_capture_supported": False,
            "gameplay_action_live_capture_supported": False,
            "opponent_observation_live_capture_supported": False,
            "field_evidence_live_capture_supported": False,
            "raw_player_log_storage_supported": False,
            "external_transport_allowed": False,
            "watcher_start_stop_allowed": False,
        },
        "process_control": {
            "parser_runner_started": False,
            "tailing_started": False,
            "sqlite_live_writes_enabled": False,
        },
        "last_result": None,
        "warnings": [] if database_configured else ["app_data_root_unavailable"],
        "errors": [] if database_configured else ["app_data_root_unavailable"],
    }


def _metadata_for_player_log(path: Path | None) -> _PlayerLogMetadata:
    if path is None:
        return _unavailable_player_log_metadata()
    try:
        path_stat = path.stat()
    except FileNotFoundError:
        return _PlayerLogMetadata(
            exists=False,
            path_kind="missing",
            metadata_access="accessible",
            size_bytes=None,
            last_modified_at=None,
            last_modified_age_seconds=None,
            activity_hint="not_applicable",
            diagnostics=("readability_not_probed", "rotation_detection_deferred", "truncation_detection_deferred"),
            warnings=("player_log_missing",),
            errors=(),
        )
    except PermissionError:
        return _PlayerLogMetadata(
            exists=False,
            path_kind="unknown",
            metadata_access="denied",
            size_bytes=None,
            last_modified_at=None,
            last_modified_age_seconds=None,
            activity_hint="unknown",
            diagnostics=("permission_denied", "readability_not_probed"),
            warnings=("player_log_unreadable",),
            errors=("player_log_metadata_denied",),
        )
    except OSError:
        return _PlayerLogMetadata(
            exists=False,
            path_kind="unknown",
            metadata_access="unavailable",
            size_bytes=None,
            last_modified_at=None,
            last_modified_age_seconds=None,
            activity_hint="unknown",
            diagnostics=("metadata_unavailable", "readability_not_probed"),
            warnings=("player_log_unreadable",),
            errors=("player_log_metadata_unavailable",),
        )

    path_kind = _path_kind_from_mode(path_stat.st_mode)
    last_modified = datetime.fromtimestamp(path_stat.st_mtime, tz=UTC)
    age_seconds = max(0.0, (datetime.now(UTC) - last_modified).total_seconds())
    activity_hint = "recent" if age_seconds <= PLAYER_LOG_RECENT_ACTIVITY_SECONDS else "stale"
    diagnostics = ["readability_not_probed", "rotation_detection_deferred", "truncation_detection_deferred"]
    warnings: list[str] = []
    errors: list[str] = []
    if path_kind != "file":
        diagnostics.append("not_file")
        warnings.append("player_log_not_file")
    if activity_hint == "stale":
        diagnostics.append("stale")
        warnings.append("player_log_stale")

    return _PlayerLogMetadata(
        exists=True,
        path_kind=path_kind,
        metadata_access="accessible",
        size_bytes=max(0, int(path_stat.st_size)),
        last_modified_at=last_modified.isoformat().replace("+00:00", "Z"),
        last_modified_age_seconds=age_seconds,
        activity_hint=activity_hint,
        diagnostics=tuple(diagnostics),
        warnings=tuple(warnings),
        errors=tuple(errors),
    )


def _invalid_config_player_log_metadata() -> _PlayerLogMetadata:
    return _PlayerLogMetadata(
        exists=False,
        path_kind="unknown",
        metadata_access="not_checked",
        size_bytes=None,
        last_modified_at=None,
        last_modified_age_seconds=None,
        activity_hint="unknown",
        diagnostics=("metadata_unavailable", "readability_not_probed"),
        warnings=("player_log_config_invalid",),
        errors=("player_log_config_invalid",),
    )


def _unavailable_player_log_metadata() -> _PlayerLogMetadata:
    return _PlayerLogMetadata(
        exists=False,
        path_kind="unavailable",
        metadata_access="unavailable",
        size_bytes=None,
        last_modified_at=None,
        last_modified_age_seconds=None,
        activity_hint="unknown",
        diagnostics=("metadata_unavailable", "readability_not_probed"),
        warnings=("player_log_unavailable",),
        errors=("app_data_root_unavailable",),
    )


def _path_kind_from_mode(mode: int) -> str:
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    return "unknown"


def _player_log_status_for_metadata(candidate: _PlayerLogCandidate, metadata: _PlayerLogMetadata) -> str:
    if metadata.metadata_access in {"denied", "unavailable"}:
        return "unreadable"
    if metadata.path_kind == "file":
        return f"{candidate.status_prefix}_exists"
    if metadata.path_kind == "missing":
        return f"{candidate.status_prefix}_missing"
    if metadata.path_kind == "directory":
        return "configured_not_file" if candidate.source == "configured" else "not_file"
    return "not_file"


def _watcher_status_for_player_log(player_log_status: str) -> tuple[str, str | None]:
    if player_log_status in {"configured_exists", "detected_exists"}:
        return "ready", None
    if player_log_status in {"configured_missing", "detected_missing"}:
        return "blocked_missing_log", "player_log_missing"
    if player_log_status == "missing":
        return "not_configured", "player_log_not_configured"
    if player_log_status == "invalid_config":
        return "blocked_invalid_config", "player_log_config_invalid"
    if player_log_status == "unreadable":
        return "blocked_unreadable_log", "player_log_unreadable"
    if player_log_status in {"configured_not_file", "not_file"}:
        return "degraded", "player_log_not_file"
    if player_log_status == "unavailable":
        return "unavailable", "player_log_unavailable"
    return "deferred", "live_watcher_deferred"


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
        "manual_import": {"status": "enabled"},
        "legacy_status_api": {"status": "separate_reference_surface"},
    }


def build_setup_status(paths: LocalAppPaths) -> dict[str, object]:
    path_status = build_path_status(paths)
    from .config import load_local_app_config_status

    config_status = load_local_app_config_status(paths)
    player_log_status = build_player_log_path_status(paths)
    live_player_log_status = build_live_player_log_status(paths)
    live_watcher_status = build_live_watcher_status(paths)
    from .live_watcher_process import build_live_watcher_process_status

    live_watcher_process_status = build_live_watcher_process_status(paths)
    live_sqlite_capture_status = build_live_sqlite_capture_status(paths)
    database_status = build_analytics_database_status(paths)
    migration_status = build_migration_loader_status()
    match_journal_status = build_match_journal_write_status(paths)
    match_journal_write_controls = match_journal_status.get("write_controls", {})
    match_journal_write_status = "unavailable"
    if isinstance(match_journal_write_controls, dict):
        match_journal_write_status = str(match_journal_write_controls.get("status", "unavailable"))
    runtime_section = build_runtime_state()
    sections = {
        "paths": path_status,
        "config": config_status,
        "player_log": player_log_status,
        "live_player_log": live_player_log_status,
        "live_watcher": live_watcher_status,
        "live_watcher_process": live_watcher_process_status,
        "live_sqlite_capture": live_sqlite_capture_status,
        "analytics_database": database_status,
        "match_journal": match_journal_status,
        "migrations": migration_status,
        "runtime": runtime_section,
    }
    return {
        "object": f"{LOCAL_APP_OBJECT_PREFIX}_setup_status",
        "schema_version": LOCAL_APP_SCHEMA_VERSION,
        "status": _combined_status(sections),
        **sections,
        "capabilities": build_capabilities(match_journal_write_controls=match_journal_write_status),
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
    if statuses == {"ok"} or statuses == {"ok", "ready"}:
        return "ok"
    return "degraded"
