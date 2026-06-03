from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sqlite3
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from mythic_edge_parser.app.analytics_migration_loader import (
    AnalyticsMigrationError,
    apply_analytics_migrations,
    iter_analytics_migrations,
)

SCHEMA_VERSION = "private_local_v1_clean_checkout_install_launch.v1"
INSTALL_MANIFEST_OBJECT = "mythic_edge_private_local_v1_install_manifest"
SETUP_REPORT_OBJECT = "mythic_edge_private_local_v1_setup_report"
DEFAULT_INSTALL_DIR_NAME = "MythicEdge"
APP_DIR_NAME = "app"
DATA_DIR_NAME = "data"
ANALYTICS_DATABASE_NAME = "mythic_edge.sqlite3"
REQUIRED_DATA_SUBDIRS = (
    "config",
    "db",
    "logs",
    "imports",
    "jobs",
    "diagnostics",
    "exports",
    "ai_review",
    "ai_review/sources",
    "ai_review/packets",
    "ai_review/reports",
)
REQUIRED_REPO_MARKERS = (
    "AGENTS.md",
    "pyproject.toml",
    "frontend/package.json",
    "frontend/package-lock.json",
    "src/mythic_edge_parser/local_app/backend.py",
)


class PrivateLocalV1SetupError(RuntimeError):
    """Raised when private-local-v1 setup cannot proceed safely."""


@dataclass(frozen=True, slots=True)
class PrivateLocalV1Paths:
    install_root: Path
    app_checkout_root: Path
    data_root: Path
    config_dir: Path
    db_dir: Path
    logs_dir: Path
    imports_dir: Path
    jobs_dir: Path
    diagnostics_dir: Path
    exports_dir: Path
    ai_review_root: Path
    ai_review_sources_dir: Path
    ai_review_packets_dir: Path
    ai_review_reports_dir: Path
    analytics_database: Path
    install_manifest: Path
    setup_report: Path


@dataclass(frozen=True, slots=True)
class PrivateLocalV1Config:
    install_root: Path
    source_checkout: Path
    mode: str
    initialize_sqlite: bool = False


def default_install_root(env: Mapping[str, str] = os.environ) -> Path | None:
    local_app_data = env.get("LOCALAPPDATA")
    if not local_app_data:
        return None
    return Path(local_app_data) / DEFAULT_INSTALL_DIR_NAME


def build_private_local_v1_paths(install_root: Path) -> PrivateLocalV1Paths:
    root = install_root
    app_root = root / APP_DIR_NAME
    data_root = root / DATA_DIR_NAME
    config_dir = data_root / "config"
    db_dir = data_root / "db"
    diagnostics_dir = data_root / "diagnostics"
    return PrivateLocalV1Paths(
        install_root=root,
        app_checkout_root=app_root,
        data_root=data_root,
        config_dir=config_dir,
        db_dir=db_dir,
        logs_dir=data_root / "logs",
        imports_dir=data_root / "imports",
        jobs_dir=data_root / "jobs",
        diagnostics_dir=diagnostics_dir,
        exports_dir=data_root / "exports",
        ai_review_root=data_root / "ai_review",
        ai_review_sources_dir=data_root / "ai_review" / "sources",
        ai_review_packets_dir=data_root / "ai_review" / "packets",
        ai_review_reports_dir=data_root / "ai_review" / "reports",
        analytics_database=db_dir / ANALYTICS_DATABASE_NAME,
        install_manifest=config_dir / "install_manifest.json",
        setup_report=diagnostics_dir / "setup_report.json",
    )


def run_private_local_v1_setup(config: PrivateLocalV1Config) -> dict[str, object]:
    paths = build_private_local_v1_paths(config.install_root)
    started_at = datetime.now(UTC)
    warnings: list[str] = []
    errors: list[str] = []

    source_status = _source_checkout_status(config.source_checkout)
    if source_status["status"] != "ok":
        errors.append("source_checkout_invalid")

    app_data_policy = validate_app_data_root(paths.data_root, source_checkout=config.source_checkout)
    if app_data_policy["status"] != "ok":
        errors.append(str(app_data_policy["reason"]))

    existing_install_handling = _existing_install_handling_status(paths)
    if config.mode == "install" and existing_install_handling["status"] == "blocked":
        errors.append("existing_install_detected")

    migration_inventory = _migration_inventory()
    if migration_inventory["status"] != "ok":
        errors.append("migration_inventory_unavailable")

    folder_creation = _folder_status(paths)
    sqlite_initialization = _sqlite_status_not_run(paths)
    if config.mode == "install" and not errors:
        folder_creation = create_v1_folder_tree(paths)
        if config.initialize_sqlite:
            sqlite_initialization = initialize_analytics_sqlite(paths)
        else:
            sqlite_initialization = _sqlite_status_not_run(paths)
            warnings.append("sqlite_initialization_not_requested")

    dependency_install = {
        "status": "not_run",
        "python": "not_installed_by_this_foundation",
        "frontend": "not_installed_by_this_foundation",
    }
    launch_status = {
        "backend_startup": "not_run",
        "frontend_startup": "not_run",
        "browser_open": "not_run",
        "status_panel_verification": "not_run",
    }
    privacy = _privacy_flags()
    manifest = _build_install_manifest(
        config=config,
        paths=paths,
        source_status=source_status,
        app_data_policy=app_data_policy,
        migration_inventory=migration_inventory,
        sqlite_initialization=sqlite_initialization,
        dependency_install=dependency_install,
        privacy=privacy,
        warnings=warnings,
        errors=errors,
    )
    report = _build_setup_report(
        started_at=started_at,
        config=config,
        source_status=source_status,
        app_data_policy=app_data_policy,
        folder_creation=folder_creation,
        migration_inventory=migration_inventory,
        sqlite_initialization=sqlite_initialization,
        dependency_install=dependency_install,
        launch_status=launch_status,
        existing_install_handling=existing_install_handling,
        privacy=privacy,
        warnings=warnings,
        errors=errors,
    )

    if config.mode == "install" and not errors:
        _write_json(paths.install_manifest, manifest)
        _write_json(paths.setup_report, report)

    return {
        "object": SETUP_REPORT_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "status": report["status"],
        "mode": config.mode,
        "install_root": "<install_root>",
        "data_root": "<install_root>\\data",
        "manifest": manifest,
        "report": report,
        "warnings": warnings,
        "errors": errors,
    }


def validate_app_data_root(app_data_root: Path, *, source_checkout: Path) -> dict[str, object]:
    normalized_app_data = _resolve_for_policy(app_data_root)
    normalized_source = _resolve_for_policy(source_checkout)
    if _is_relative_to(normalized_app_data, normalized_source):
        return {
            "status": "blocked",
            "reason": "app_data_root_inside_source_checkout",
            "message": _git_checkout_refusal_message(),
        }
    git_root = nearest_git_metadata_root(app_data_root)
    if git_root is not None:
        return {
            "status": "blocked",
            "reason": "app_data_root_inside_git_checkout",
            "message": _git_checkout_refusal_message(),
        }
    return {"status": "ok", "reason": None, "message": "app-data root accepted"}


def nearest_git_metadata_root(path: Path) -> Path | None:
    candidates = _existing_path_and_parents(path)
    for candidate in candidates:
        if (candidate / ".git").exists():
            return candidate
    return None


def create_v1_folder_tree(paths: PrivateLocalV1Paths) -> dict[str, object]:
    created: list[str] = []
    existing: list[str] = []
    for subdir in REQUIRED_DATA_SUBDIRS:
        folder = paths.data_root / Path(subdir)
        if folder.exists():
            existing.append(_symbolic_data_path(subdir))
            continue
        folder.mkdir(parents=True, exist_ok=True)
        created.append(_symbolic_data_path(subdir))
    paths.app_checkout_root.mkdir(parents=True, exist_ok=True)
    return {
        "status": "ok",
        "created": created,
        "existing": existing,
        "app_checkout_root": "<install_root>\\app",
        "data_root": "<install_root>\\data",
    }


def initialize_analytics_sqlite(paths: PrivateLocalV1Paths) -> dict[str, object]:
    paths.db_dir.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(paths.analytics_database)
    try:
        migrations = apply_analytics_migrations(connection)
    finally:
        connection.close()
    return {
        "status": "ok",
        "database": "<install_root>\\data\\db\\mythic_edge.sqlite3",
        "schema_status": "schema_current",
        "applied_migration_ids": [migration.migration_id for migration in migrations],
        "raw_sql_included": False,
        "parser_rows_inserted": False,
    }


def _existing_install_handling_status(paths: PrivateLocalV1Paths) -> dict[str, object]:
    detected = _existing_install_indicators(paths)
    if detected:
        return {
            "status": "blocked",
            "reason": "existing_install_choices_not_implemented",
            "detected": detected,
            "message": "Existing private-local-v1 install state was detected; choose a backup/reset path later.",
        }
    return {
        "status": "not_detected",
        "reason": None,
        "detected": [],
        "message": "No existing private-local-v1 install state detected.",
    }


def _existing_install_indicators(paths: PrivateLocalV1Paths) -> list[str]:
    indicators: list[str] = []
    if paths.install_manifest.exists():
        indicators.append("install_manifest")
    if paths.setup_report.exists():
        indicators.append("setup_report")
    if paths.analytics_database.exists():
        indicators.append("analytics_database")
    if paths.app_checkout_root.exists():
        indicators.append("app_checkout_root")
    if _has_existing_generated_data(paths):
        indicators.append("generated_data")
    return indicators


def _has_existing_generated_data(paths: PrivateLocalV1Paths) -> bool:
    if not paths.data_root.exists():
        return False
    expected_artifact_paths = {
        paths.install_manifest.resolve(),
        paths.setup_report.resolve(),
        paths.analytics_database.resolve(),
    }
    allowed_empty_dirs = {
        paths.config_dir.resolve(),
        paths.db_dir.resolve(),
        paths.diagnostics_dir.resolve(),
    }
    for child in paths.data_root.rglob("*"):
        try:
            resolved_child = child.resolve()
        except OSError:
            return True
        if resolved_child in expected_artifact_paths:
            continue
        if child.is_dir() and resolved_child in allowed_empty_dirs:
            continue
        if child.is_dir() and not any(child.iterdir()):
            continue
        if child.is_file() or child.is_dir():
            return True
    return False


def _build_install_manifest(
    *,
    config: PrivateLocalV1Config,
    paths: PrivateLocalV1Paths,
    source_status: dict[str, object],
    app_data_policy: dict[str, object],
    migration_inventory: dict[str, object],
    sqlite_initialization: dict[str, object],
    dependency_install: dict[str, object],
    privacy: dict[str, bool],
    warnings: list[str],
    errors: list[str],
) -> dict[str, object]:
    return {
        "object": INSTALL_MANIFEST_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "install_profile": "private_local_v1",
        "mode": config.mode,
        "install_root": "<install_root>",
        "app_checkout_root": "<install_root>\\app",
        "data_root": "<install_root>\\data",
        "source_checkout": source_status,
        "app_data_policy": app_data_policy,
        "toolchain": _toolchain_status(),
        "dependency_install": dependency_install,
        "node": _node_status(),
        "git": _git_status(config.source_checkout),
        "migrations": migration_inventory,
        "sqlite_initialization": sqlite_initialization,
        "ai_review": {
            "status": "reserved_only",
            "folders": [
                "<install_root>\\data\\ai_review\\sources",
                "<install_root>\\data\\ai_review\\packets",
                "<install_root>\\data\\ai_review\\reports",
            ],
            "ai_runtime_enabled": False,
            "external_send_allowed": False,
        },
        "privacy": privacy,
        "warnings": warnings,
        "errors": errors,
    }


def _build_setup_report(
    *,
    started_at: datetime,
    config: PrivateLocalV1Config,
    source_status: dict[str, object],
    app_data_policy: dict[str, object],
    folder_creation: dict[str, object],
    migration_inventory: dict[str, object],
    sqlite_initialization: dict[str, object],
    dependency_install: dict[str, object],
    launch_status: dict[str, str],
    existing_install_handling: dict[str, object],
    privacy: dict[str, bool],
    warnings: list[str],
    errors: list[str],
) -> dict[str, object]:
    duration = max(0.0, (datetime.now(UTC) - started_at).total_seconds())
    status = "blocked" if errors else ("degraded" if warnings else "passed")
    return {
        "object": SETUP_REPORT_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "mode": config.mode,
        "duration_seconds": round(duration, 3),
        "toolchain": _toolchain_status(),
        "dependency_install": dependency_install,
        "folder_creation": folder_creation,
        "git_checkout": source_status,
        "existing_install_handling": existing_install_handling,
        "sqlite_initialization": sqlite_initialization,
        "migration_status": migration_inventory,
        **launch_status,
        "git_artifact_safety": {
            "status": "not_run",
            "tracked_generated_artifacts_detected": False,
        },
        "privacy": privacy,
        "warnings": warnings,
        "errors": errors,
        "next_steps": _next_steps(status),
    }


def _source_checkout_status(source_checkout: Path) -> dict[str, object]:
    missing = [marker for marker in REQUIRED_REPO_MARKERS if not (source_checkout / marker).exists()]
    return {
        "status": "ok" if not missing else "blocked",
        "display_path": "<source_checkout>",
        "controlled_existing_checkout": True,
        "clone_from_github_performed": False,
        "missing_markers": missing,
    }


def _migration_inventory() -> dict[str, object]:
    try:
        migrations = iter_analytics_migrations()
    except AnalyticsMigrationError:
        return {"status": "error", "applied_migration_ids": [], "errors": ["migration_inventory_unavailable"]}
    return {
        "status": "ok",
        "available_migration_ids": [migration.migration_id for migration in migrations],
        "errors": [],
    }


def _folder_status(paths: PrivateLocalV1Paths) -> dict[str, object]:
    missing = [
        _symbolic_data_path(subdir)
        for subdir in REQUIRED_DATA_SUBDIRS
        if not (paths.data_root / Path(subdir)).exists()
    ]
    return {
        "status": "missing" if missing else "ok",
        "missing": missing,
        "created": [],
        "app_checkout_root": "<install_root>\\app",
        "data_root": "<install_root>\\data",
    }


def _sqlite_status_not_run(paths: PrivateLocalV1Paths) -> dict[str, object]:
    return {
        "status": "not_run",
        "database": "<install_root>\\data\\db\\mythic_edge.sqlite3",
        "schema_status": "not_checked",
        "exists": paths.analytics_database.exists(),
        "applied_migration_ids": [],
        "raw_sql_included": False,
        "parser_rows_inserted": False,
    }


def _toolchain_status() -> dict[str, object]:
    return {
        "status": "metadata_only",
        "platform": platform.system(),
        "python": {
            "executable_kind": "active_interpreter",
            "version": platform.python_version(),
            "virtualenv_display_path": "<not_created_by_this_foundation>",
            "install_status": "not_run",
        },
    }


def _node_status() -> dict[str, object]:
    return {
        "node_available": shutil.which("node") is not None,
        "npm_available": shutil.which("npm") is not None or shutil.which("npm.cmd") is not None,
        "install_status": "not_run",
    }


def _git_status(source_checkout: Path) -> dict[str, object]:
    return {
        "git_available": shutil.which("git") is not None,
        "checkout_status": "controlled_existing_checkout" if (source_checkout / ".git").exists() else "metadata_only",
        "release_ref_status": "deferred_until_v1_ref_exists",
    }


def _privacy_flags() -> dict[str, bool]:
    return {
        "raw_paths_included": False,
        "raw_logs_read": False,
        "private_jsonl_payloads_read": False,
        "secrets_or_environment_values_read": False,
        "ai_provider_keys_read": False,
        "raw_sql_included": False,
        "stack_traces_included": False,
        "external_sends_performed": False,
    }


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _next_steps(status: str) -> list[str]:
    if status == "blocked":
        return ["Resolve blockers and rerun setup."]
    return [
        "Run dependency installation and launch proof in a later authorized slice.",
        "Run contract-test review before claiming private_local_v1 install readiness.",
    ]


def _git_checkout_refusal_message() -> str:
    return (
        "Mythic Edge cannot use a Git checkout folder, or any folder inside a Git checkout, "
        "as its app-data folder. Please choose a folder outside the repo. "
        "Recommended: %LOCALAPPDATA%\\MythicEdge\\data\\"
    )


def _symbolic_data_path(subdir: str) -> str:
    return "<install_root>\\data\\" + subdir.replace("/", "\\")


def _existing_path_and_parents(path: Path) -> tuple[Path, ...]:
    current = _resolve_for_policy(path if path.exists() else _nearest_existing_parent(path))
    return (current, *current.parents)


def _nearest_existing_parent(path: Path) -> Path:
    current = path
    while not current.exists() and current.parent != current:
        current = current.parent
    return current


def _resolve_for_policy(path: Path) -> Path:
    try:
        return path.resolve()
    except OSError:
        return path.absolute()


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mythic Edge private-local-v1 setup foundation")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Report readiness without creating folders or databases.")
    mode.add_argument("--install", action="store_true", help="Create v1 folders and generated setup artifacts.")
    parser.add_argument("--existing-checkout", action="store_true", help="Use the current checkout as source input.")
    parser.add_argument("--source-checkout", type=Path, default=Path.cwd())
    parser.add_argument("--install-root", type=Path)
    parser.add_argument("--initialize-sqlite", action="store_true")
    parser.add_argument("--json-report", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    install_root = args.install_root or default_install_root()
    if install_root is None:
        print("LOCALAPPDATA is unavailable; pass --install-root for tests or controlled setup.")
        return 2
    mode = "install" if args.install else "check"
    config = PrivateLocalV1Config(
        install_root=install_root,
        source_checkout=args.source_checkout,
        mode=mode,
        initialize_sqlite=args.initialize_sqlite,
    )
    result = run_private_local_v1_setup(config)
    if args.json_report:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"private-local-v1 setup {result['status']} ({mode})")
    return 0 if result["status"] in {"passed", "degraded"} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
