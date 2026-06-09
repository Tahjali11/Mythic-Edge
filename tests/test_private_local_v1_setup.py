from __future__ import annotations

import io
import json
import sqlite3
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import IO

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
    _assert_package_readiness_metadata(result, release_ref=setup.DEFAULT_RELEASE_REF)
    report = result["report"]
    _assert_package_readiness_metadata(result["manifest"], release_ref=setup.DEFAULT_RELEASE_REF)
    _assert_package_readiness_metadata(report, release_ref=setup.DEFAULT_RELEASE_REF)
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
    _assert_package_readiness_metadata(manifest, release_ref=setup.DEFAULT_RELEASE_REF)
    _assert_package_readiness_metadata(report, release_ref=setup.DEFAULT_RELEASE_REF)
    assert manifest["ai_review"]["ai_runtime_enabled"] is False
    assert manifest["ai_review"]["external_send_allowed"] is False
    assert manifest["privacy"]["external_sends_performed"] is False
    assert report["sqlite_initialization"]["schema_status"] == "schema_current"
    assert "0001_initial_analytics_schema" in report["sqlite_initialization"]["applied_migration_ids"]
    assert _table_count(paths.analytics_database, "matches") == 0
    assert _table_count(paths.analytics_database, "games") == 0
    assert str(install_root) not in json.dumps(manifest, sort_keys=True)
    assert str(install_root) not in json.dumps(report, sort_keys=True)


def test_install_mode_writes_user_confirmed_player_log_config_without_leaking_paths(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    player_log_path = tmp_path / "Arena" / "Player.log"
    player_log_path.parent.mkdir()
    player_log_path.write_text("private log body must not be read", encoding="utf-8")

    result = setup.run_private_local_v1_setup(
        setup.PrivateLocalV1Config(
            install_root=install_root,
            source_checkout=source_checkout,
            mode="install",
            initialize_sqlite=True,
            player_log_path=player_log_path,
        )
    )

    paths = setup.build_private_local_v1_paths(install_root)
    config_file = paths.config_dir / "app_config.json"
    manifest = json.loads(paths.install_manifest.read_text(encoding="utf-8"))
    report = json.loads(paths.setup_report.read_text(encoding="utf-8"))
    config_payload = json.loads(config_file.read_text(encoding="utf-8"))
    encoded_result = json.dumps(result, sort_keys=True)
    encoded_manifest = json.dumps(manifest, sort_keys=True)
    encoded_report = json.dumps(report, sort_keys=True)

    assert result["status"] == "passed"
    assert config_file.read_bytes()[:3] != b"\xef\xbb\xbf"
    assert config_payload == {
        "analytics_database_path": str(paths.analytics_database),
        "player_log_path": str(player_log_path),
    }
    assert result["player_log_configuration"]["status"] == "accepted"
    assert result["player_log_configuration"]["display_path"] == "<selected_player_log>"
    assert result["player_log_configuration"]["contents_read"] is False
    assert result["player_log_configuration"]["tailing_started"] is False
    assert result["config_write"]["status"] == "ok"
    assert result["config_write"]["written_fields"] == ["player_log_path", "analytics_database_path"]
    assert manifest["player_log_configuration"]["status"] == "accepted"
    assert manifest["config_write"]["status"] == "ok"
    assert report["player_log_configuration"]["display_path"] == "<selected_player_log>"
    assert report["config_write"]["raw_values_included"] is False
    assert str(player_log_path) not in encoded_result
    assert str(player_log_path) not in encoded_manifest
    assert str(player_log_path) not in encoded_report
    assert str(paths.analytics_database) not in encoded_result
    assert "private log body" not in encoded_result


def test_check_mode_validates_player_log_metadata_without_writing_config(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    player_log_path = tmp_path / "Player.log"
    player_log_path.write_text("private log body must not be read", encoding="utf-8")

    result = setup.run_private_local_v1_setup(
        setup.PrivateLocalV1Config(
            install_root=install_root,
            source_checkout=source_checkout,
            mode="check",
            player_log_path=player_log_path,
        )
    )

    paths = setup.build_private_local_v1_paths(install_root)
    encoded = json.dumps(result, sort_keys=True)

    assert result["status"] == "passed"
    assert result["player_log_configuration"]["status"] == "accepted"
    assert result["config_write"]["status"] == "not_run"
    assert result["config_write"]["reason"] == "check_mode_non_mutating"
    assert not paths.config_dir.exists()
    assert str(player_log_path) not in encoded
    assert "private log body" not in encoded


def test_install_mode_blocks_missing_player_log_without_writing_config(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    player_log_path = tmp_path / "missing" / "Player.log"

    result = setup.run_private_local_v1_setup(
        setup.PrivateLocalV1Config(
            install_root=install_root,
            source_checkout=source_checkout,
            mode="install",
            initialize_sqlite=True,
            player_log_path=player_log_path,
        )
    )

    paths = setup.build_private_local_v1_paths(install_root)
    encoded = json.dumps(result, sort_keys=True)

    assert result["status"] == "blocked"
    assert result["errors"] == ["player_log_missing"]
    assert result["player_log_configuration"]["status"] == "missing"
    assert result["config_write"]["status"] == "not_run"
    assert result["config_write"]["reason"] == "blocked_before_config_write"
    assert not (paths.config_dir / "app_config.json").exists()
    assert not paths.analytics_database.exists()
    assert str(player_log_path) not in encoded


def test_install_mode_blocks_player_log_directory_without_writing_config(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    player_log_path = tmp_path / "Player.log"
    player_log_path.mkdir()

    result = setup.run_private_local_v1_setup(
        setup.PrivateLocalV1Config(
            install_root=install_root,
            source_checkout=source_checkout,
            mode="install",
            initialize_sqlite=True,
            player_log_path=player_log_path,
        )
    )

    paths = setup.build_private_local_v1_paths(install_root)
    encoded = json.dumps(result, sort_keys=True)

    assert result["status"] == "blocked"
    assert result["errors"] == ["player_log_not_file"]
    assert result["player_log_configuration"]["status"] == "not_file"
    assert result["player_log_configuration"]["path_kind"] == "directory"
    assert result["player_log_configuration"]["display_path"] == "<selected_player_log>"
    assert result["player_log_configuration"]["contents_read"] is False
    assert result["player_log_configuration"]["tailing_started"] is False
    assert result["config_write"]["status"] == "not_run"
    assert result["config_write"]["reason"] == "blocked_before_config_write"
    assert not (paths.config_dir / "app_config.json").exists()
    assert not paths.analytics_database.exists()
    assert str(player_log_path) not in encoded


def test_install_mode_blocks_unreadable_player_log_metadata_without_writing_config(tmp_path: Path, monkeypatch) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    player_log_path = tmp_path / "Player.log"
    player_log_path.write_text("private log body must not be read", encoding="utf-8")
    original_stat = type(player_log_path).stat

    def stat_with_denial(self: Path, *args: object, **kwargs: object) -> object:
        if self == player_log_path:
            raise PermissionError("metadata denied")
        return original_stat(self, *args, **kwargs)

    monkeypatch.setattr(type(player_log_path), "stat", stat_with_denial)

    result = setup.run_private_local_v1_setup(
        setup.PrivateLocalV1Config(
            install_root=install_root,
            source_checkout=source_checkout,
            mode="install",
            initialize_sqlite=True,
            player_log_path=player_log_path,
        )
    )

    paths = setup.build_private_local_v1_paths(install_root)
    encoded = json.dumps(result, sort_keys=True)

    assert result["status"] == "blocked"
    assert result["errors"] == ["player_log_metadata_denied"]
    assert result["player_log_configuration"]["status"] == "unreadable"
    assert result["player_log_configuration"]["metadata_access"] == "denied"
    assert result["player_log_configuration"]["warnings"] == ["player_log_unreadable"]
    assert result["player_log_configuration"]["display_path"] == "<selected_player_log>"
    assert result["player_log_configuration"]["contents_read"] is False
    assert result["player_log_configuration"]["tailing_started"] is False
    assert result["config_write"]["status"] == "not_run"
    assert result["config_write"]["reason"] == "blocked_before_config_write"
    assert not (paths.config_dir / "app_config.json").exists()
    assert not paths.analytics_database.exists()
    assert str(player_log_path) not in encoded
    assert "private log body" not in encoded


def test_check_mode_records_configured_release_ref_in_metadata(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "install"

    result = setup.run_private_local_v1_setup(
        setup.PrivateLocalV1Config(
            install_root=install_root,
            source_checkout=source_checkout,
            mode="check",
            release_ref="release/test-ref",
        )
    )

    assert result["status"] == "passed"
    _assert_package_readiness_metadata(result, release_ref="release/test-ref")
    _assert_package_readiness_metadata(result["manifest"], release_ref="release/test-ref")
    _assert_package_readiness_metadata(result["report"], release_ref="release/test-ref")
    assert not install_root.exists()


def test_check_mode_cli_records_configured_release_ref_in_json_report(capsys, tmp_path: Path) -> None:
    install_root = tmp_path / "install"

    exit_code = setup.main(
        [
            "--check",
            "--install-root",
            str(install_root),
            "--release-ref",
            "release/test-ref",
            "--json-report",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert exit_code == 0
    _assert_package_readiness_metadata(payload, release_ref="release/test-ref")
    _assert_package_readiness_metadata(payload["manifest"], release_ref="release/test-ref")
    _assert_package_readiness_metadata(payload["report"], release_ref="release/test-ref")
    assert not install_root.exists()


def test_wizard_detects_default_windows_player_log_metadata_without_reading_contents(tmp_path: Path) -> None:
    user_profile = tmp_path / "profile"
    default_log = user_profile.joinpath(*setup.DEFAULT_WINDOWS_PLAYER_LOG_RELATIVE_PATH)
    default_log.parent.mkdir(parents=True)
    default_log.write_text("private default body must not be read", encoding="utf-8")

    status = setup.detect_default_windows_player_log_candidate({"USERPROFILE": str(user_profile)})
    encoded = json.dumps(status, sort_keys=True)

    assert status["status"] == "accepted"
    assert status["source"] == "detected_default"
    assert status["display_path"] == "<detected_mtga_player_log>"
    assert status["path_kind"] == "file"
    assert status["metadata_access"] == "accessible"
    assert status["contents_read"] is False
    assert status["tailing_started"] is False
    assert status["activity_hint"] in {"recent", "stale"}
    assert str(default_log) not in encoded
    assert "private default body" not in encoded


def test_wizard_accepts_detected_default_after_confirmation_without_leaking_paths(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    user_profile = tmp_path / "profile"
    default_log = user_profile.joinpath(*setup.DEFAULT_WINDOWS_PLAYER_LOG_RELATIVE_PATH)
    default_log.parent.mkdir(parents=True)
    default_log.write_text("private default body must not be read", encoding="utf-8")

    result = setup.run_private_local_v1_setup_wizard(
        setup.PrivateLocalV1WizardConfig(
            install_root=install_root,
            source_checkout=source_checkout,
        ),
        prompt_reader=_prompt_answers(["", "", "y"]),
        output_writer=lambda _message: None,
        env={"USERPROFILE": str(user_profile)},
    )

    paths = setup.build_private_local_v1_paths(install_root)
    manifest = json.loads(paths.install_manifest.read_text(encoding="utf-8"))
    report = json.loads(paths.setup_report.read_text(encoding="utf-8"))
    config_payload = json.loads((paths.config_dir / "app_config.json").read_text(encoding="utf-8"))
    encoded = json.dumps(result, sort_keys=True)

    assert result["status"] == "healthy"
    assert result["player_log_selection"]["source"] == "detected_default"
    assert result["player_log_selection"]["display_path"] == "<detected_mtga_player_log>"
    assert manifest["player_log_configuration"]["source"] == "detected_default"
    assert manifest["player_log_configuration"]["display_path"] == "<detected_mtga_player_log>"
    assert report["player_log_configuration"]["contents_read"] is False
    assert config_payload["player_log_path"] == str(default_log)
    assert config_payload["analytics_database_path"] == str(paths.analytics_database)
    assert str(default_log) not in encoded
    assert str(paths.analytics_database) not in encoded
    assert "private default body" not in encoded


def test_wizard_accepts_manual_player_log_after_default_missing(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    user_profile = tmp_path / "profile"
    manual_log = tmp_path / "manual" / "Player.log"
    manual_log.parent.mkdir()
    manual_log.write_text("private manual body must not be read", encoding="utf-8")

    result = setup.run_private_local_v1_setup_wizard(
        setup.PrivateLocalV1WizardConfig(
            install_root=install_root,
            source_checkout=source_checkout,
        ),
        prompt_reader=_prompt_answers(["", str(manual_log), "y"]),
        output_writer=lambda _message: None,
        env={"USERPROFILE": str(user_profile)},
    )

    paths = setup.build_private_local_v1_paths(install_root)
    manifest = json.loads(paths.install_manifest.read_text(encoding="utf-8"))
    encoded = json.dumps(result, sort_keys=True)

    assert result["status"] == "healthy"
    assert result["player_log_selection"]["source"] == "manual_selection"
    assert result["player_log_selection"]["display_path"] == "<selected_player_log>"
    assert manifest["player_log_configuration"]["source"] == "manual_selection"
    assert manifest["player_log_configuration"]["display_path"] == "<selected_player_log>"
    assert json.loads((paths.config_dir / "app_config.json").read_text(encoding="utf-8"))["player_log_path"] == str(
        manual_log
    )
    assert str(manual_log) not in encoded
    assert "private manual body" not in encoded


def test_wizard_skip_player_log_completes_degraded_without_config_write(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    user_profile = tmp_path / "profile"

    result = setup.run_private_local_v1_setup_wizard(
        setup.PrivateLocalV1WizardConfig(
            install_root=install_root,
            source_checkout=source_checkout,
        ),
        prompt_reader=_prompt_answers(["", "skip", "y"]),
        output_writer=lambda _message: None,
        env={"USERPROFILE": str(user_profile)},
    )

    paths = setup.build_private_local_v1_paths(install_root)
    report = json.loads(paths.setup_report.read_text(encoding="utf-8"))

    assert result["status"] == "degraded"
    assert result["player_log_selection"]["status"] == "skipped"
    assert result["player_log_selection"]["display_path"] == "<player_log_not_configured>"
    assert "player_log_not_configured" in result["warnings"]
    assert report["status"] == "degraded"
    assert report["config_write"]["status"] == "not_run"
    assert report["config_write"]["reason"] == "player_log_path_not_provided"
    assert not (paths.config_dir / "app_config.json").exists()
    assert paths.analytics_database.is_file()


def test_wizard_cli_json_report_keeps_stdout_parseable(capsys, monkeypatch, tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    user_profile = tmp_path / "profile"
    monkeypatch.setenv("USERPROFILE", str(user_profile))
    monkeypatch.setattr(sys, "stdin", io.StringIO("\nskip\ny\n"))

    exit_code = setup.main(
        [
            "--wizard",
            "--install-root",
            str(install_root),
            "--source-checkout",
            str(source_checkout),
            "--json-report",
        ]
    )

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["status"] == "degraded"
    assert payload["mode"] == "wizard"
    assert payload["player_log_selection"]["display_path"] == "<player_log_not_configured>"
    assert "Mythic Edge private-local-v1 setup wizard" in captured.err
    assert str(install_root) not in captured.out


def test_wizard_missing_manual_path_can_cancel_without_writing(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    user_profile = tmp_path / "profile"
    missing_log = tmp_path / "missing" / "Player.log"

    result = setup.run_private_local_v1_setup_wizard(
        setup.PrivateLocalV1WizardConfig(
            install_root=install_root,
            source_checkout=source_checkout,
        ),
        prompt_reader=_prompt_answers(["", str(missing_log), "cancel"]),
        output_writer=lambda _message: None,
        env={"USERPROFILE": str(user_profile)},
    )

    assert result["status"] == "blocked"
    assert result["errors"] == ["wizard_cancelled"]
    assert result["setup_result"] is None
    assert not install_root.exists()
    assert str(missing_log) not in json.dumps(result, sort_keys=True)


def test_wizard_manual_player_log_directory_can_cancel_without_writing(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    user_profile = tmp_path / "profile"
    player_log_path = tmp_path / "Player.log"
    player_log_path.mkdir()
    messages: list[str] = []

    result = setup.run_private_local_v1_setup_wizard(
        setup.PrivateLocalV1WizardConfig(
            install_root=install_root,
            source_checkout=source_checkout,
        ),
        prompt_reader=_prompt_answers(["", str(player_log_path), "cancel"]),
        output_writer=messages.append,
        env={"USERPROFILE": str(user_profile)},
    )

    encoded = json.dumps(result, sort_keys=True)
    rendered_messages = "\n".join(messages)

    assert result["status"] == "blocked"
    assert result["errors"] == ["wizard_cancelled"]
    assert result["setup_result"] is None
    assert result["player_log_selection"]["status"] == "cancelled"
    assert "Selected Player.log could not be accepted from metadata" in rendered_messages
    assert not install_root.exists()
    assert str(player_log_path) not in encoded
    assert str(player_log_path) not in rendered_messages


def test_wizard_manual_player_log_metadata_denied_can_cancel_without_writing(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    user_profile = tmp_path / "profile"
    player_log_path = tmp_path / "Player.log"
    player_log_path.write_text("private log body must not be read", encoding="utf-8")
    original_stat = type(player_log_path).stat
    messages: list[str] = []

    def stat_with_denial(self: Path, *args: object, **kwargs: object) -> object:
        if self == player_log_path:
            raise PermissionError("metadata denied")
        return original_stat(self, *args, **kwargs)

    monkeypatch.setattr(type(player_log_path), "stat", stat_with_denial)

    result = setup.run_private_local_v1_setup_wizard(
        setup.PrivateLocalV1WizardConfig(
            install_root=install_root,
            source_checkout=source_checkout,
        ),
        prompt_reader=_prompt_answers(["", str(player_log_path), "cancel"]),
        output_writer=messages.append,
        env={"USERPROFILE": str(user_profile)},
    )

    encoded = json.dumps(result, sort_keys=True)
    rendered_messages = "\n".join(messages)

    assert result["status"] == "blocked"
    assert result["errors"] == ["wizard_cancelled"]
    assert result["setup_result"] is None
    assert result["player_log_selection"]["status"] == "cancelled"
    assert "Selected Player.log could not be accepted from metadata" in rendered_messages
    assert not install_root.exists()
    assert str(player_log_path) not in encoded
    assert str(player_log_path) not in rendered_messages
    assert "private log body" not in encoded


def test_parse_args_and_powershell_wrapper_expose_wizard_mode() -> None:
    args = setup._parse_args(["--wizard"])
    wrapper = Path("tools/dev_app/setup_private_local_v1.ps1").read_text(encoding="utf-8")

    assert args.wizard is True
    assert "[switch]$Wizard" in wrapper
    assert '$argsList += "--wizard"' in wrapper


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


def test_install_mode_blocks_existing_app_config_without_overwriting_it(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    paths = setup.build_private_local_v1_paths(install_root)
    paths.config_dir.mkdir(parents=True)
    prior_config = '{"sentinel":"keep-config"}\n'
    paths.config_dir.joinpath("app_config.json").write_text(prior_config, encoding="utf-8")
    player_log_path = tmp_path / "Player.log"
    player_log_path.write_text("private log body must not be read", encoding="utf-8")

    result = setup.run_private_local_v1_setup(
        setup.PrivateLocalV1Config(
            install_root=install_root,
            source_checkout=source_checkout,
            mode="install",
            initialize_sqlite=True,
            player_log_path=player_log_path,
        )
    )

    assert result["status"] == "blocked"
    assert result["errors"] == ["existing_install_detected"]
    assert paths.config_dir.joinpath("app_config.json").read_text(encoding="utf-8") == prior_config
    assert result["report"]["existing_install_handling"]["status"] == "blocked"
    assert result["report"]["existing_install_handling"]["detected"] == ["app_config"]
    assert str(player_log_path) not in json.dumps(result, sort_keys=True)


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


def test_proof_mode_orchestrates_existing_checkout_without_real_side_effects(tmp_path: Path) -> None:
    source_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    commands = ProofCommandRecorder()
    processes = ProofProcessRecorder()

    result = setup.run_private_local_v1_proof(
        setup.PrivateLocalV1ProofConfig(
            install_root=install_root,
            source_checkout=source_checkout,
            existing_checkout=True,
            no_open=True,
            stop_after_verify=True,
        ),
        command_runner=commands.run,
        http_verifier=_passing_http_verifier,
        tool_resolver=_tool_resolver,
        module_finder=_module_finder,
        port_checker=lambda _host, _port: True,
        process_launcher=processes.launch,
        browser_opener=lambda _url: False,
        platform_name="Windows",
        settle_seconds=0,
    )

    paths = setup.build_private_local_v1_paths(install_root)
    proof_report = json.loads((paths.diagnostics_dir / "setup_proof_report.json").read_text(encoding="utf-8"))
    setup_report = json.loads(paths.setup_report.read_text(encoding="utf-8"))

    assert result["status"] == "degraded"
    assert result["source_checkout"]["clone_from_github_performed"] is False
    assert [call.command_shape for call in commands.calls] == [
        "<active_python> -m venv <proof_source_checkout>\\.venv",
        '<venv_python> -m pip install -e ".[dev,app]"',
        '<venv_python> -c "import mythic_edge_parser, fastapi, uvicorn"',
        "npm --prefix frontend ci",
    ]
    assert [call.name for call in processes.calls] == ["backend", "frontend"]
    backend_call = processes.calls[0]
    assert backend_call.command[:3] == [str(setup._proof_python_path(source_checkout)), "-m", "uvicorn"]
    assert all(process.terminated for process in processes.processes)
    assert proof_report["launch"]["status_panel_verification"] == "http_only"
    assert proof_report["launch"]["browser_open"] == "skipped_no_open"
    assert "status_panel_verification_http_only" in proof_report["warnings"]
    assert setup_report["dependency_install"]["status"] == "passed"
    assert setup_report["backend_startup"] == "passed"
    assert setup_report["frontend_startup"] == "passed"
    assert setup_report["status_panel_verification"] == "http_only"
    assert str(install_root) not in json.dumps(proof_report, sort_keys=True)
    assert str(source_checkout) not in json.dumps(proof_report, sort_keys=True)


def test_proof_mode_can_clone_into_v1_app_root_with_fake_repo(tmp_path: Path) -> None:
    seed_checkout = _make_source_checkout(tmp_path)
    install_root = tmp_path / "private-local-v1"
    commands = ProofCommandRecorder(clone_source=seed_checkout)
    processes = ProofProcessRecorder()

    result = setup.run_private_local_v1_proof(
        setup.PrivateLocalV1ProofConfig(
            install_root=install_root,
            source_checkout=seed_checkout,
            repo_url="https://example.invalid/Mythic-Edge.git",
            release_ref="v1-test",
            existing_checkout=False,
            no_open=True,
            stop_after_verify=True,
        ),
        command_runner=commands.run,
        http_verifier=_passing_http_verifier,
        tool_resolver=_tool_resolver,
        module_finder=_module_finder,
        port_checker=lambda _host, _port: True,
        process_launcher=processes.launch,
        platform_name="Windows",
        settle_seconds=0,
    )

    paths = setup.build_private_local_v1_paths(install_root)
    proof_report = json.loads((paths.diagnostics_dir / "setup_proof_report.json").read_text(encoding="utf-8"))

    assert result["status"] == "degraded"
    assert result["source_checkout"]["clone_from_github_performed"] is True
    assert commands.calls[0].name == "git_clone_to_app_root"
    assert commands.calls[0].command_shape == (
        "git clone --branch <release_ref> --single-branch <repo_url> <install_root>\\app"
    )
    backend_call = processes.calls[0]
    assert backend_call.command[:3] == [str(setup._proof_python_path(paths.app_checkout_root)), "-m", "uvicorn"]
    assert (paths.app_checkout_root / "AGENTS.md").is_file()
    assert proof_report["clone"]["status"] == "passed"
    assert proof_report["launch"]["status_panel_verification"] == "http_only"
    assert str(paths.app_checkout_root) not in json.dumps(proof_report, sort_keys=True)


def test_powershell_wrapper_routes_to_private_local_v1_helper_without_destructive_commands() -> None:
    wrapper = Path("tools/dev_app/setup_private_local_v1.ps1").read_text(encoding="utf-8")
    wrapper_lower = wrapper.lower()

    assert "private_local_v1_setup.py" in wrapper
    assert "-Check" in wrapper
    assert "-Install" in wrapper
    assert "-Proof" in wrapper
    assert "--repo-url" in wrapper
    assert "--release-ref" in wrapper
    assert "--player-log-path" in wrapper
    assert "--no-open" in wrapper
    assert "--stop-after-verify" in wrapper
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


def _assert_package_readiness_metadata(payload: Mapping[str, object], *, release_ref: str) -> None:
    assert payload["release_profile"] == "private_local_v1"
    assert payload["package_mode"] == "managed_full_checkout"
    assert payload["release_ref"] == release_ref
    assert payload["public_release_ready"] is False
    assert payload["production_ready"] is False


@dataclass(frozen=True, slots=True)
class ProofCommandCall:
    name: str
    command_shape: str
    cwd: Path


class ProofCommandRecorder:
    def __init__(self, *, clone_source: Path | None = None) -> None:
        self.clone_source = clone_source
        self.calls: list[ProofCommandCall] = []

    def run(self, command: Sequence[str], cwd: Path) -> setup.CommandOutcome:
        command_shape = _command_shape(command)
        name = _command_name(command)
        self.calls.append(ProofCommandCall(name, command_shape, cwd))
        if name == "git_clone_to_app_root" and self.clone_source is not None:
            _copy_fake_checkout(self.clone_source, Path(command[-1]))
        return setup.CommandOutcome("passed", 0, "fake_passed")


@dataclass(frozen=True, slots=True)
class ProofProcessCall:
    name: str
    command: list[str]
    cwd: Path
    env: Mapping[str, str]


class ProofProcessRecorder:
    def __init__(self) -> None:
        self.calls: list[ProofProcessCall] = []
        self.processes: list[ProofProcess] = []

    def launch(
        self,
        command: Sequence[str],
        cwd: Path,
        env: Mapping[str, str],
        log_handle: IO[bytes],
    ) -> "ProofProcess":
        name = "backend" if "uvicorn" in command else "frontend"
        log_handle.write(f"{name} started\n".encode())
        process = ProofProcess()
        self.calls.append(ProofProcessCall(name, list(command), cwd, dict(env)))
        self.processes.append(process)
        return process


class ProofProcess:
    def __init__(self) -> None:
        self.terminated = False
        self.killed = False

    def poll(self) -> int | None:
        return 0 if self.terminated or self.killed else None

    def terminate(self) -> None:
        self.terminated = True

    def wait(self, timeout: float | None = None) -> int:
        self.terminated = True
        return 0

    def kill(self) -> None:
        self.killed = True


def _passing_http_verifier(url: str) -> dict[str, object]:
    return {"status": "passed", "url": url.replace("8765", "<backend_port>").replace("5173", "<frontend_port>")}


def _tool_resolver(name: str) -> str | None:
    tools = {
        "py": "py",
        "node": "node",
        "npm": "npm",
        "npm.cmd": "npm.cmd",
        "git": "git",
    }
    return tools.get(name)


def _module_finder(name: str) -> object | None:
    return object() if name in {"mythic_edge_parser", "fastapi", "uvicorn"} else None


def _command_name(command: Sequence[str]) -> str:
    if command[:2] == ["git", "clone"]:
        return "git_clone_to_app_root"
    if len(command) >= 3 and command[1:3] == ["-m", "venv"]:
        return "python_virtualenv"
    if len(command) >= 4 and command[1:4] == ["-m", "pip", "install"]:
        return "python_dependency_install"
    if len(command) >= 3 and command[1] == "-c":
        return "python_dependency_import_check"
    return "frontend_dependency_install"


def _command_shape(command: Sequence[str]) -> str:
    name = _command_name(command)
    if name == "git_clone_to_app_root":
        return "git clone --branch <release_ref> --single-branch <repo_url> <install_root>\\app"
    if name == "python_virtualenv":
        return "<active_python> -m venv <proof_source_checkout>\\.venv"
    if name == "python_dependency_install":
        return '<venv_python> -m pip install -e ".[dev,app]"'
    if name == "python_dependency_import_check":
        return '<venv_python> -c "import mythic_edge_parser, fastapi, uvicorn"'
    return "npm --prefix frontend ci"


def _copy_fake_checkout(source: Path, destination: Path) -> None:
    for marker in setup.REQUIRED_REPO_MARKERS:
        source_path = source / marker
        target_path = destination / marker
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")
    (destination / ".git").mkdir(exist_ok=True)


def _prompt_answers(answers: Sequence[str]) -> Callable[[str], str]:
    iterator = iter(answers)

    def read_prompt(_prompt: str) -> str:
        return next(iterator)

    return read_prompt
