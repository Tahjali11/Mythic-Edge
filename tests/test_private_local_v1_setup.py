from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from tools.dev_app import private_local_v1_setup as setup


def test_check_mode_reports_without_creating_v1_folders_or_database(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "install"

    result = setup.run_private_local_v1_setup(
        setup.PrivateLocalV1Config(
            install_root=install_root,
            source_checkout=source_checkout,
            mode="check",
        )
    )

    assert result["status"] == "passed"
    assert result["mode"] == "check"
    assert not install_root.exists()
    report = result["report"]
    assert report["folder_creation"]["status"] == "missing"
    assert report["sqlite_initialization"]["status"] == "not_run"
    assert report["backend_startup"] == "not_run"
    assert report["frontend_startup"] == "not_run"
    assert report["browser_open"] == "not_run"
    assert report["privacy"]["raw_paths_included"] is False
    assert str(install_root) not in json.dumps(result, sort_keys=True)


def test_app_data_root_inside_git_checkout_is_blocked(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = source_checkout / "nested-install"

    result = setup.run_private_local_v1_setup(
        setup.PrivateLocalV1Config(
            install_root=install_root,
            source_checkout=source_checkout,
            mode="install",
            initialize_sqlite=True,
        )
    )

    assert result["status"] == "blocked"
    assert result["errors"] == ["app_data_root_inside_source_checkout"]
    assert not (install_root / "data").exists()
    assert result["report"]["status"] == "blocked"
    assert str(source_checkout) not in json.dumps(result, sort_keys=True)


def test_install_mode_creates_reserved_tree_manifest_report_and_empty_migrated_database(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"

    result = setup.run_private_local_v1_setup(
        setup.PrivateLocalV1Config(
            install_root=install_root,
            source_checkout=source_checkout,
            mode="install",
            initialize_sqlite=True,
        )
    )

    paths = setup.build_private_local_v1_paths(install_root)
    assert result["status"] == "passed"
    assert {path.relative_to(paths.data_root).as_posix() for path in paths.data_root.rglob("*") if path.is_dir()} >= {
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
    }
    assert paths.install_manifest.is_file()
    assert paths.setup_report.is_file()
    assert paths.analytics_database.is_file()

    manifest = json.loads(paths.install_manifest.read_text(encoding="utf-8"))
    report = json.loads(paths.setup_report.read_text(encoding="utf-8"))
    assert manifest["object"] == setup.INSTALL_MANIFEST_OBJECT
    assert report["object"] == setup.SETUP_REPORT_OBJECT
    assert manifest["schema_version"] == setup.SCHEMA_VERSION
    assert report["schema_version"] == setup.SCHEMA_VERSION
    assert manifest["ai_review"]["ai_runtime_enabled"] is False
    assert manifest["ai_review"]["external_send_allowed"] is False
    assert manifest["privacy"]["external_sends_performed"] is False
    assert report["sqlite_initialization"]["schema_status"] == "schema_current"
    assert "0001_initial_analytics_schema" in report["sqlite_initialization"]["applied_migration_ids"]
    assert _table_count(paths.analytics_database, "matches") == 0
    assert _table_count(paths.analytics_database, "games") == 0
    assert str(install_root) not in json.dumps(manifest, sort_keys=True)
    assert str(install_root) not in json.dumps(report, sort_keys=True)


def test_install_mode_blocks_existing_manifest_and_report_without_overwriting_metadata(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    paths = setup.build_private_local_v1_paths(install_root)
    paths.config_dir.mkdir(parents=True)
    paths.diagnostics_dir.mkdir(parents=True)
    prior_manifest = '{"sentinel":"keep-manifest"}\n'
    prior_report = '{"sentinel":"keep-report"}\n'
    paths.install_manifest.write_text(prior_manifest, encoding="utf-8")
    paths.setup_report.write_text(prior_report, encoding="utf-8")

    result = setup.run_private_local_v1_setup(
        setup.PrivateLocalV1Config(
            install_root=install_root,
            source_checkout=source_checkout,
            mode="install",
            initialize_sqlite=True,
        )
    )

    assert result["status"] == "blocked"
    assert result["errors"] == ["existing_install_detected"]
    assert paths.install_manifest.read_text(encoding="utf-8") == prior_manifest
    assert paths.setup_report.read_text(encoding="utf-8") == prior_report
    assert not paths.analytics_database.exists()
    assert not paths.app_checkout_root.exists()
    assert result["report"]["existing_install_handling"]["status"] == "blocked"
    assert set(result["report"]["existing_install_handling"]["detected"]) == {
        "install_manifest",
        "setup_report",
    }
    assert str(install_root) not in json.dumps(result, sort_keys=True)


def test_install_mode_blocks_existing_database_without_migrating_or_writing_metadata(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    paths = setup.build_private_local_v1_paths(install_root)
    paths.db_dir.mkdir(parents=True)
    connection = sqlite3.connect(paths.analytics_database)
    try:
        connection.execute("CREATE TABLE sentinel_existing_install (id INTEGER PRIMARY KEY)")
        connection.commit()
    finally:
        connection.close()

    result = setup.run_private_local_v1_setup(
        setup.PrivateLocalV1Config(
            install_root=install_root,
            source_checkout=source_checkout,
            mode="install",
            initialize_sqlite=True,
        )
    )

    assert result["status"] == "blocked"
    assert result["errors"] == ["existing_install_detected"]
    assert not paths.install_manifest.exists()
    assert not paths.setup_report.exists()
    assert _table_exists(paths.analytics_database, "sentinel_existing_install")
    assert not _table_exists(paths.analytics_database, "schema_migrations")
    assert result["report"]["existing_install_handling"]["status"] == "blocked"
    assert result["report"]["existing_install_handling"]["detected"] == ["analytics_database"]
    assert result["report"]["sqlite_initialization"]["status"] == "not_run"
    assert result["report"]["sqlite_initialization"]["exists"] is True
    assert str(install_root) not in json.dumps(result, sort_keys=True)


def test_powershell_wrapper_routes_to_private_local_v1_helper_without_destructive_commands() -> None:
    wrapper = Path("tools/dev_app/setup_private_local_v1.ps1").read_text(encoding="utf-8")
    wrapper_lower = wrapper.lower()

    assert "private_local_v1_setup.py" in wrapper
    assert "-Check" in wrapper
    assert "-Install" in wrapper
    assert "git clone" not in wrapper_lower
    assert "npm ci" not in wrapper_lower
    assert "pip install" not in wrapper_lower
    assert "remove-item" not in wrapper_lower
    assert "rmdir" not in wrapper_lower
    assert "del " not in wrapper_lower


def _table_count(database_path: Path, table_name: str) -> int:
    connection = sqlite3.connect(database_path)
    try:
        row = connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
        return int(row[0])
    finally:
        connection.close()


def _table_exists(database_path: Path, table_name: str) -> bool:
    connection = sqlite3.connect(database_path)
    try:
        row = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
            (table_name,),
        ).fetchone()
        return row is not None
    finally:
        connection.close()


def _make_source_checkout(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    (repo_root / ".git").mkdir(parents=True)
    (repo_root / "frontend").mkdir()
    (repo_root / "src" / "mythic_edge_parser" / "local_app").mkdir(parents=True)
    (repo_root / "AGENTS.md").write_text("agent rules\n", encoding="utf-8")
    (repo_root / "pyproject.toml").write_text("[project]\nname = 'test'\n", encoding="utf-8")
    (repo_root / "frontend" / "package.json").write_text("{}\n", encoding="utf-8")
    (repo_root / "frontend" / "package-lock.json").write_text("{}\n", encoding="utf-8")
    (repo_root / "src" / "mythic_edge_parser" / "local_app" / "backend.py").write_text("", encoding="utf-8")
    return repo_root
