from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

LOCAL_APP_SCHEMA_VERSION = "analytics_app_backend_setup_status.v1"
LOCAL_APP_OBJECT_PREFIX = "mythic_edge_local_app"
LOCAL_APP_DIR_NAME = "MythicEdgeDev"
REQUIRED_APP_SUBDIRS = ("config", "db", "logs", "imports", "jobs", "diagnostics")
DEFAULT_ANALYTICS_DB_FILENAME = "mythic_edge.sqlite3"
DEFAULT_MATCH_JOURNAL_DB_FILENAME = "match_journal.sqlite3"
DEFAULT_BACKEND_HOST = "127.0.0.1"

_DISPLAY_ROOT = "<app_data>"


@dataclass(frozen=True, slots=True)
class LocalAppPaths:
    app_data_root: Path | None
    config_dir: Path | None
    db_dir: Path | None
    logs_dir: Path | None
    imports_dir: Path | None
    jobs_dir: Path | None
    diagnostics_dir: Path | None
    config_file: Path | None
    analytics_database: Path | None
    match_journal_database: Path | None


def build_local_app_paths(app_data_root: Path | None = None) -> LocalAppPaths:
    root = Path(app_data_root) if app_data_root is not None else _default_app_data_root()
    if root is None:
        return LocalAppPaths(
            app_data_root=None,
            config_dir=None,
            db_dir=None,
            logs_dir=None,
            imports_dir=None,
            jobs_dir=None,
            diagnostics_dir=None,
            config_file=None,
            analytics_database=None,
            match_journal_database=None,
        )

    config_dir = root / "config"
    db_dir = root / "db"
    return LocalAppPaths(
        app_data_root=root,
        config_dir=config_dir,
        db_dir=db_dir,
        logs_dir=root / "logs",
        imports_dir=root / "imports",
        jobs_dir=root / "jobs",
        diagnostics_dir=root / "diagnostics",
        config_file=config_dir / "app_config.json",
        analytics_database=db_dir / DEFAULT_ANALYTICS_DB_FILENAME,
        match_journal_database=db_dir / DEFAULT_MATCH_JOURNAL_DB_FILENAME,
    )


def build_path_status(paths: LocalAppPaths) -> dict[str, object]:
    if paths.app_data_root is None:
        return {
            "object": f"{LOCAL_APP_OBJECT_PREFIX}_paths_status",
            "schema_version": LOCAL_APP_SCHEMA_VERSION,
            "status": "unavailable",
            "app_data_root": {
                "key": "app_data_root",
                "display_path": rf"%LOCALAPPDATA%\{LOCAL_APP_DIR_NAME}",
                "exists": False,
                "kind": "unknown",
                "required": True,
                "status": "unavailable",
            },
            "subfolders": [],
            "redaction_policy": "symbolic_app_data_paths_only",
        }

    subfolders = [
        _path_status("config", paths.config_dir, required=True),
        _path_status("db", paths.db_dir, required=True),
        _path_status("logs", paths.logs_dir, required=True),
        _path_status("imports", paths.imports_dir, required=True),
        _path_status("jobs", paths.jobs_dir, required=True),
        _path_status("diagnostics", paths.diagnostics_dir, required=True),
    ]
    return {
        "object": f"{LOCAL_APP_OBJECT_PREFIX}_paths_status",
        "schema_version": LOCAL_APP_SCHEMA_VERSION,
        "status": "ok" if all(folder["exists"] for folder in subfolders) else "degraded",
        "app_data_root": {
            "key": "app_data_root",
            "display_path": _DISPLAY_ROOT,
            "exists": paths.app_data_root.exists(),
            "kind": _path_kind(paths.app_data_root),
            "required": True,
            "status": _status_for_path(paths.app_data_root, required=True),
        },
        "subfolders": subfolders,
        "redaction_policy": "symbolic_app_data_paths_only",
    }


def display_app_path(*parts: str) -> str:
    if not parts:
        return _DISPLAY_ROOT
    return "\\".join((_DISPLAY_ROOT, *parts))


def _default_app_data_root() -> Path | None:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        return None
    return Path(local_app_data) / LOCAL_APP_DIR_NAME


def _path_status(key: str, path: Path | None, *, required: bool) -> dict[str, object]:
    return {
        "key": key,
        "display_path": display_app_path(key),
        "exists": path.exists() if path is not None else False,
        "kind": _path_kind(path),
        "required": required,
        "status": _status_for_path(path, required=required),
    }


def _path_kind(path: Path | None) -> str:
    if path is None or not path.exists():
        return "unknown"
    if path.is_dir():
        return "directory"
    if path.is_file():
        return "file"
    return "unknown"


def _status_for_path(path: Path | None, *, required: bool) -> str:
    if path is None:
        return "unavailable"
    if path.exists():
        return "ok"
    return "missing" if required else "ok"
