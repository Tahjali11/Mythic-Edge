from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import shutil
import sqlite3
import subprocess
import sys
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from mythic_edge_parser.app.analytics_migration_loader import (
    AnalyticsMigrationError,
    apply_analytics_migrations,
    iter_analytics_migrations,
)

try:
    from tools.dev_app import dev_app_launcher as launcher
except ModuleNotFoundError:  # pragma: no cover - direct script execution path
    import dev_app_launcher as launcher

SCHEMA_VERSION = "private_local_v1_clean_checkout_install_launch.v1"
INSTALL_MANIFEST_OBJECT = "mythic_edge_private_local_v1_install_manifest"
SETUP_REPORT_OBJECT = "mythic_edge_private_local_v1_setup_report"
PROOF_REPORT_OBJECT = "mythic_edge_private_local_v1_setup_proof_report"
DEFAULT_INSTALL_DIR_NAME = "MythicEdge"
APP_DIR_NAME = "app"
DATA_DIR_NAME = "data"
ANALYTICS_DATABASE_NAME = "mythic_edge.sqlite3"
DEFAULT_REPO_URL = "https://github.com/Tahjali11/Mythic-Edge.git"
DEFAULT_RELEASE_REF = "codex/analytics-foundation"
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
    managed_app_checkout: bool = False


@dataclass(frozen=True, slots=True)
class PrivateLocalV1ProofConfig:
    install_root: Path
    source_checkout: Path
    repo_url: str = DEFAULT_REPO_URL
    release_ref: str = DEFAULT_RELEASE_REF
    existing_checkout: bool = True
    initialize_sqlite: bool = True
    no_open: bool = True
    leave_running: bool = False
    stop_after_verify: bool = True
    backend_port: int = launcher.BACKEND_PORT
    frontend_port: int = launcher.FRONTEND_PORT


@dataclass(frozen=True, slots=True)
class CommandOutcome:
    status: str
    returncode: int
    summary: str


CommandRunner = Callable[[Sequence[str], Path], CommandOutcome]
HttpVerifier = Callable[[str], dict[str, object]]


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

    existing_install_handling = _existing_install_handling_status(paths, config=config)
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


def run_private_local_v1_proof(
    config: PrivateLocalV1ProofConfig,
    *,
    command_runner: CommandRunner | None = None,
    http_verifier: HttpVerifier | None = None,
    tool_resolver: launcher.ToolResolver = shutil.which,
    module_finder: launcher.ModuleFinder = importlib.util.find_spec,
    port_checker: launcher.PortChecker | None = None,
    process_launcher: launcher.ProcessLauncher | None = None,
    browser_opener: launcher.BrowserOpener | None = None,
    platform_name: str | None = None,
    settle_seconds: float = 1.0,
) -> dict[str, object]:
    command_runner = command_runner or run_command
    http_verifier = http_verifier or verify_http_url
    browser_opener = browser_opener or launcher.webbrowser.open
    started_at = datetime.now(UTC)
    paths = build_private_local_v1_paths(config.install_root)
    warnings: list[str] = []
    errors: list[str] = []
    steps: list[dict[str, object]] = []
    children: tuple[launcher.ManagedChild, ...] = ()

    if config.leave_running and config.stop_after_verify:
        errors.append("leave_running_conflicts_with_stop_after_verify")

    app_data_policy = validate_app_data_root(paths.data_root, source_checkout=config.source_checkout)
    if app_data_policy["status"] != "ok":
        errors.append(str(app_data_policy["reason"]))

    proof_source = config.source_checkout
    clone_status: dict[str, object] = {
        "status": "skipped_existing_checkout",
        "display_path": "<source_checkout>",
        "repo_url": "<repo_url>",
        "release_ref": config.release_ref,
        "clone_from_github_performed": False,
    }
    if not config.existing_checkout and not errors:
        existing_install = _existing_install_handling_status(
            paths,
            config=PrivateLocalV1Config(
                install_root=config.install_root,
                source_checkout=paths.app_checkout_root,
                mode="install",
                initialize_sqlite=config.initialize_sqlite,
            ),
        )
        if existing_install["status"] == "blocked":
            errors.append("existing_install_detected")
        else:
            paths.install_root.mkdir(parents=True, exist_ok=True)
            clone_command = [
                "git",
                "clone",
                "--branch",
                config.release_ref,
                "--single-branch",
                config.repo_url,
                str(paths.app_checkout_root),
            ]
            clone_outcome = command_runner(clone_command, paths.install_root)
            clone_status = _command_step(
                "git_clone_to_app_root",
                clone_outcome,
                cwd="<install_root>",
                command_shape="git clone --branch <release_ref> --single-branch <repo_url> <install_root>\\app",
            )
            steps.append(clone_status)
            if clone_outcome.status != "passed":
                errors.append("git_clone_failed")
            proof_source = paths.app_checkout_root

    source_status = _source_checkout_status(proof_source)
    if source_status["status"] != "ok":
        errors.append("source_checkout_invalid")

    setup_result: dict[str, object] | None = None
    if not errors:
        setup_result = run_private_local_v1_setup(
            PrivateLocalV1Config(
                install_root=config.install_root,
                source_checkout=proof_source,
                mode="install",
                initialize_sqlite=config.initialize_sqlite,
                managed_app_checkout=not config.existing_checkout,
            )
        )
        steps.append(
            {
                "name": "private_local_v1_setup_install",
                "status": setup_result["status"],
                "cwd": "<proof_source_checkout>",
                "command_shape": (
                    "py tools\\dev_app\\private_local_v1_setup.py --install "
                    "--source-checkout <proof_source_checkout> --install-root <install_root> "
                    "--initialize-sqlite --json-report"
                ),
            }
        )
        if setup_result["status"] not in {"passed", "degraded"}:
            errors.append("setup_install_failed")

    proof_python = _proof_python_path(proof_source)
    command_plan = [
        (
            "python_virtualenv",
            [sys.executable, "-m", "venv", str(proof_source / ".venv")],
            proof_source,
            "<active_python> -m venv <proof_source_checkout>\\.venv",
        ),
        (
            "python_dependency_install",
            [str(proof_python), "-m", "pip", "install", "-e", ".[dev,app]"],
            proof_source,
            '<venv_python> -m pip install -e ".[dev,app]"',
        ),
        (
            "python_dependency_import_check",
            [str(proof_python), "-c", "import mythic_edge_parser, fastapi, uvicorn"],
            proof_source,
            '<venv_python> -c "import mythic_edge_parser, fastapi, uvicorn"',
        ),
        (
            "frontend_dependency_install",
            [_npm_command(), "--prefix", "frontend", "ci"],
            proof_source,
            "npm --prefix frontend ci",
        ),
    ]
    if not errors:
        for name, command, cwd, command_shape in command_plan:
            outcome = command_runner(command, cwd)
            step = _command_step(name, outcome, cwd="<proof_source_checkout>", command_shape=command_shape)
            steps.append(step)
            if outcome.status != "passed":
                errors.append(f"{name}_failed")
                break

    launch_status: dict[str, object] = {
        "backend_startup": "not_run",
        "frontend_startup": "not_run",
        "browser_open": "not_run",
        "status_panel_verification": "not_run",
        "http_checks": [],
        "process_cleanup": "not_run",
    }
    if not errors:
        launch_config = launcher.build_config(
            repo_root=proof_source,
            app_data_root=paths.data_root,
            backend_port=config.backend_port,
            frontend_port=config.frontend_port,
            backend_python=str(proof_python),
            no_open=True,
        )
        start_result = launcher.start_dev_app(
            launch_config,
            tool_resolver=tool_resolver,
            module_finder=module_finder,
            platform_name=platform_name,
            port_checker=port_checker,
            process_launcher=process_launcher,
            browser_opener=lambda _url: False,
            run_id="private-local-v1-proof",
            wait_for_exit=False,
            settle_seconds=settle_seconds,
        )
        children = start_result.children
        launch_status["backend_startup"] = "passed" if start_result.status == "running" else "failed"
        launch_status["frontend_startup"] = "passed" if start_result.status == "running" else "failed"
        if start_result.status != "running":
            errors.append("backend_frontend_startup_failed")
        else:
            http_checks = [
                http_verifier(f"http://127.0.0.1:{config.backend_port}/api/health"),
                http_verifier(f"http://127.0.0.1:{config.backend_port}/api/app/setup-status"),
                http_verifier(f"http://127.0.0.1:{config.backend_port}/api/analytics/database/status"),
                http_verifier(f"http://127.0.0.1:{config.frontend_port}/"),
            ]
            launch_status["http_checks"] = http_checks
            if any(check["status"] != "passed" for check in http_checks):
                errors.append("status_http_verification_failed")
            else:
                launch_status["status_panel_verification"] = "http_only"
                warnings.append("status_panel_verification_http_only")
            if config.no_open:
                launch_status["browser_open"] = "skipped_no_open"
            else:
                try:
                    opened = bool(browser_opener(f"http://127.0.0.1:{config.frontend_port}"))
                except Exception:
                    opened = False
                launch_status["browser_open"] = "passed" if opened else "degraded"
                if not opened:
                    warnings.append("browser_open_failed")

    if children and config.stop_after_verify:
        launcher.cleanup_children(children)
        launch_status["process_cleanup"] = "stopped_proof_started_processes"
    elif children and config.leave_running:
        launch_status["process_cleanup"] = "left_running_by_request"

    dependency_install = _proof_dependency_install_status(steps)
    status = "failed" if errors else ("degraded" if warnings else "passed")
    proof_report = {
        "object": PROOF_REPORT_OBJECT,
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "mode": "proof",
        "duration_seconds": round(max(0.0, (datetime.now(UTC) - started_at).total_seconds()), 3),
        "install_root": "<install_root>",
        "app_checkout_root": "<install_root>\\app",
        "data_root": "<install_root>\\data",
        "source_checkout": {
            **source_status,
            "clone_from_github_performed": not config.existing_checkout and "git_clone_failed" not in errors,
        },
        "clone": clone_status,
        "dependency_install": dependency_install,
        "setup_install": None if setup_result is None else setup_result["report"],
        "launch": launch_status,
        "steps": steps,
        "privacy": _privacy_flags(),
        "warnings": warnings,
        "errors": errors,
        "next_steps": _proof_next_steps(status),
    }
    if setup_result is not None and setup_result["status"] in {"passed", "degraded"}:
        _write_final_proof_artifacts(paths, setup_result, proof_report, dependency_install, launch_status)
    return proof_report


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


def run_command(command: Sequence[str], cwd: Path) -> CommandOutcome:
    try:
        completed = subprocess.run(  # noqa: S603 - command vectors are contract-owned setup steps.
            list(command),
            cwd=cwd,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return CommandOutcome("failed", 1, "command_unavailable_or_failed_to_start")
    return CommandOutcome(
        "passed" if completed.returncode == 0 else "failed",
        completed.returncode,
        "command_completed" if completed.returncode == 0 else "command_failed",
    )


def verify_http_url(url: str, *, timeout_seconds: float = 20.0) -> dict[str, object]:
    try:
        with urllib.request.urlopen(url, timeout=timeout_seconds) as response:  # noqa: S310 - loopback proof URL only.
            status_code = response.getcode()
    except (OSError, urllib.error.URLError):
        return {"status": "failed", "url": _symbolic_url(url), "status_code": None}
    return {
        "status": "passed" if 200 <= status_code < 300 else "failed",
        "url": _symbolic_url(url),
        "status_code": status_code,
    }


def _existing_install_handling_status(paths: PrivateLocalV1Paths, *, config: PrivateLocalV1Config) -> dict[str, object]:
    detected = _existing_install_indicators(paths, config=config)
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


def _existing_install_indicators(paths: PrivateLocalV1Paths, *, config: PrivateLocalV1Config) -> list[str]:
    indicators: list[str] = []
    if paths.install_manifest.exists():
        indicators.append("install_manifest")
    if paths.setup_report.exists():
        indicators.append("setup_report")
    if paths.analytics_database.exists():
        indicators.append("analytics_database")
    if paths.app_checkout_root.exists() and not _is_managed_app_checkout(paths, config):
        indicators.append("app_checkout_root")
    if _has_existing_generated_data(paths):
        indicators.append("generated_data")
    return indicators


def _is_managed_app_checkout(paths: PrivateLocalV1Paths, config: PrivateLocalV1Config) -> bool:
    if not config.managed_app_checkout:
        return False
    if _resolve_for_policy(config.source_checkout) != _resolve_for_policy(paths.app_checkout_root):
        return False
    return _source_checkout_status(paths.app_checkout_root)["status"] == "ok"


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


def _proof_python_path(proof_source: Path) -> Path:
    if platform.system() == "Windows":
        return proof_source / ".venv" / "Scripts" / "python.exe"
    return proof_source / ".venv" / "bin" / "python"


def _npm_command() -> str:
    return shutil.which("npm.cmd") or shutil.which("npm") or "npm"


def _command_step(
    name: str,
    outcome: CommandOutcome,
    *,
    cwd: str,
    command_shape: str,
) -> dict[str, object]:
    return {
        "name": name,
        "status": outcome.status,
        "returncode": outcome.returncode,
        "cwd": cwd,
        "command_shape": command_shape,
        "summary": outcome.summary,
    }


def _proof_dependency_install_status(steps: Sequence[dict[str, object]]) -> dict[str, object]:
    by_name = {str(step["name"]): step for step in steps}
    return {
        "status": _combined_step_status(
            by_name,
            (
                "python_virtualenv",
                "python_dependency_install",
                "python_dependency_import_check",
                "frontend_dependency_install",
            ),
        ),
        "python_virtualenv": by_name.get("python_virtualenv", {"status": "not_run"})["status"],
        "python": by_name.get("python_dependency_install", {"status": "not_run"})["status"],
        "python_import_check": by_name.get("python_dependency_import_check", {"status": "not_run"})["status"],
        "frontend": by_name.get("frontend_dependency_install", {"status": "not_run"})["status"],
        "raw_command_output_included": False,
    }


def _combined_step_status(by_name: Mapping[str, dict[str, object]], names: Sequence[str]) -> str:
    statuses = [by_name.get(name, {"status": "not_run"})["status"] for name in names]
    if any(status == "failed" for status in statuses):
        return "failed"
    if any(status == "not_run" for status in statuses):
        return "not_run"
    return "passed"


def _write_final_proof_artifacts(
    paths: PrivateLocalV1Paths,
    setup_result: dict[str, object],
    proof_report: dict[str, object],
    dependency_install: dict[str, object],
    launch_status: dict[str, object],
) -> None:
    manifest = dict(setup_result["manifest"])  # type: ignore[arg-type]
    setup_report = dict(setup_result["report"])  # type: ignore[arg-type]
    manifest["dependency_install"] = dependency_install
    setup_report["dependency_install"] = dependency_install
    setup_report["backend_startup"] = launch_status["backend_startup"]
    setup_report["frontend_startup"] = launch_status["frontend_startup"]
    setup_report["browser_open"] = launch_status["browser_open"]
    setup_report["status_panel_verification"] = launch_status["status_panel_verification"]
    setup_report["git_artifact_safety"] = {
        "status": "not_run",
        "tracked_generated_artifacts_detected": False,
    }
    setup_report["proof_report_object"] = PROOF_REPORT_OBJECT
    setup_report["status"] = proof_report["status"]
    setup_report["warnings"] = proof_report["warnings"]
    setup_report["errors"] = proof_report["errors"]
    _write_json(paths.install_manifest, manifest)
    _write_json(paths.setup_report, setup_report)
    _write_json(paths.diagnostics_dir / "setup_proof_report.json", proof_report)


def _proof_next_steps(status: str) -> list[str]:
    if status == "passed":
        return ["Route to Codex E for live controlled clean-install proof review."]
    if status == "degraded":
        return ["Review degraded proof warnings before claiming private_local_v1 readiness."]
    return ["Resolve setup proof blockers and rerun the proof flow."]


def _symbolic_url(url: str) -> str:
    if "/api/health" in url:
        return "http://127.0.0.1:<backend_port>/api/health"
    if "/api/app/setup-status" in url:
        return "http://127.0.0.1:<backend_port>/api/app/setup-status"
    if "/api/analytics/database/status" in url:
        return "http://127.0.0.1:<backend_port>/api/analytics/database/status"
    return "http://127.0.0.1:<frontend_port>/"


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
    mode.add_argument("--proof", action="store_true", help="Run the private-local-v1 setup proof orchestration.")
    parser.add_argument("--existing-checkout", action="store_true", help="Use the current checkout as source input.")
    parser.add_argument("--source-checkout", type=Path, default=Path.cwd())
    parser.add_argument("--install-root", type=Path)
    parser.add_argument("--initialize-sqlite", action="store_true")
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL)
    parser.add_argument("--release-ref", default=DEFAULT_RELEASE_REF)
    parser.add_argument("--no-open", action="store_true")
    parser.add_argument("--leave-running", action="store_true")
    parser.add_argument("--stop-after-verify", action="store_true")
    parser.add_argument("--backend-port", type=int, default=launcher.BACKEND_PORT)
    parser.add_argument("--frontend-port", type=int, default=launcher.FRONTEND_PORT)
    parser.add_argument("--json-report", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    install_root = args.install_root or default_install_root()
    if install_root is None:
        print("LOCALAPPDATA is unavailable; pass --install-root for tests or controlled setup.")
        return 2
    if args.proof:
        result = run_private_local_v1_proof(
            PrivateLocalV1ProofConfig(
                install_root=install_root,
                source_checkout=args.source_checkout,
                repo_url=args.repo_url,
                release_ref=args.release_ref,
                existing_checkout=args.existing_checkout,
                initialize_sqlite=True,
                no_open=args.no_open,
                leave_running=args.leave_running,
                stop_after_verify=args.stop_after_verify or not args.leave_running,
                backend_port=args.backend_port,
                frontend_port=args.frontend_port,
            )
        )
        if args.json_report:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print(f"private-local-v1 setup proof {result['status']}")
        return 0 if result["status"] in {"passed", "degraded"} else 1

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
