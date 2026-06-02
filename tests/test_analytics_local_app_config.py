from __future__ import annotations

import json
import sqlite3

from mythic_edge_parser.app.analytics_migration_loader import apply_analytics_migrations
from mythic_edge_parser.app.match_journal_migration_loader import apply_match_journal_migrations
from mythic_edge_parser.local_app.config import _is_safe_unexpected_field_name, load_local_app_config_status
from mythic_edge_parser.local_app.paths import build_local_app_paths, build_path_status
from mythic_edge_parser.local_app.setup_status import (
    build_analytics_database_status,
    build_match_journal_write_status,
    build_migration_loader_status,
    build_player_log_path_status,
)


def test_build_local_app_paths_uses_temp_override_without_creating_folders(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    paths = build_local_app_paths(app_root)

    assert paths.app_data_root == app_root
    assert paths.config_file == app_root / "config" / "app_config.json"
    assert paths.analytics_database == app_root / "db" / "mythic_edge.sqlite3"
    assert paths.match_journal_database == app_root / "db" / "match_journal.sqlite3"
    assert not app_root.exists()

    status = build_path_status(paths)
    encoded = json.dumps(status, sort_keys=True)

    assert status["status"] == "degraded"
    assert status["app_data_root"]["display_path"] == "<app_data>"
    assert status["subfolders"][0]["display_path"] == "<app_data>\\config"
    assert str(app_root) not in encoded


def test_config_status_reports_missing_and_invalid_json_without_echoing_content(tmp_path) -> None:
    paths = build_local_app_paths(tmp_path / "app-data")

    missing = load_local_app_config_status(paths)

    assert missing["status"] == "missing"
    assert missing["config_file"]["status"] == "missing"
    assert not paths.config_file.exists()

    paths.config_file.parent.mkdir(parents=True)
    paths.config_file.write_text('{"player_log_path": ', encoding="utf-8")

    invalid = load_local_app_config_status(paths)
    encoded = json.dumps(invalid, sort_keys=True)

    assert invalid["status"] == "error"
    assert invalid["config_file"]["status"] == "invalid_json"
    assert '{"player_log_path": ' not in encoded
    assert str(paths.config_file.parent) not in encoded


def test_config_status_reports_safe_field_names_and_redacts_secret_like_fields(tmp_path) -> None:
    paths = build_local_app_paths(tmp_path / "app-data")
    paths.config_file.parent.mkdir(parents=True)
    paths.config_file.write_text(
        json.dumps(
            {
                "player_log_path": str(tmp_path / "Player.log"),
                "analytics_database_path": str(tmp_path / "private.sqlite3"),
                "backend_host": "127.0.0.1",
                "safe_extra": "visible-name-only",
                "webhook_url": "https://example.invalid/hook",
                "api_key": "not-returned",
            }
        ),
        encoding="utf-8",
    )

    status = load_local_app_config_status(paths)
    encoded = json.dumps(status, sort_keys=True)

    assert status["status"] == "ok"
    assert status["config_file"]["status"] == "present"
    assert status["loaded_fields"] == ["player_log_path", "analytics_database_path", "backend_host"]
    assert status["unexpected_fields"] == ["safe_extra"]
    assert status["secret_like_field_count"] == 2
    assert "visible-name-only" not in encoded
    assert "https://example.invalid/hook" not in encoded
    assert "not-returned" not in encoded
    assert str(tmp_path) not in encoded


def test_unexpected_field_safe_label_helper_rejects_non_string_and_unsafe_names(tmp_path) -> None:
    unsafe_url_key = "https://" + "example.invalid/config-key"
    unsafe_path_key = str(tmp_path / "private_config_key")

    assert _is_safe_unexpected_field_name("safe_extra") is True

    for field_name in (
        unsafe_url_key,
        unsafe_path_key,
        "webhook_url",
        "unsafe field with spaces",
        17,
        None,
    ):
        assert _is_safe_unexpected_field_name(field_name) is False


def test_config_status_redacts_unsafe_unexpected_field_names(tmp_path) -> None:
    paths = build_local_app_paths(tmp_path / "app-data")
    unsafe_url_key = "https://" + "example.invalid/config-key"
    unsafe_path_key = str(tmp_path / "private_config_key")
    paths.config_file.parent.mkdir(parents=True)
    paths.config_file.write_text(
        json.dumps(
            {
                "backend_host": "127.0.0.1",
                "safe_extra": "visible-name-only",
                unsafe_url_key: "url-key-value",
                unsafe_path_key: "path-key-value",
                "unsafe field with spaces": "unsafe-field-value",
                "webhook_url": "secret-like-value",
            }
        ),
        encoding="utf-8",
    )

    status = load_local_app_config_status(paths)
    encoded = json.dumps(status, sort_keys=True)

    assert status["status"] == "ok"
    assert status["unexpected_fields"] == ["safe_extra"]
    assert status["secret_like_field_count"] == 4
    assert unsafe_url_key not in encoded
    assert unsafe_path_key not in encoded
    assert "unsafe field with spaces" not in encoded
    assert "webhook_url" not in encoded
    assert "url-key-value" not in encoded
    assert "path-key-value" not in encoded
    assert "unsafe-field-value" not in encoded
    assert "secret-like-value" not in encoded


def test_config_status_rejects_non_loopback_backend_and_wildcard_frontend_origin(tmp_path) -> None:
    paths = build_local_app_paths(tmp_path / "app-data")
    paths.config_file.parent.mkdir(parents=True)
    paths.config_file.write_text(
        json.dumps(
            {
                "backend_host": "0.0.0.0",
                "backend_port": 0,
                "frontend_origin": "*",
            }
        ),
        encoding="utf-8",
    )

    status = load_local_app_config_status(paths)
    encoded = json.dumps(status, sort_keys=True)

    assert status["status"] == "error"
    assert status["config_file"]["status"] == "invalid_shape"
    assert status["errors"] == [
        "backend_host_must_be_loopback",
        "backend_port_invalid",
        "frontend_origin_must_be_local",
    ]
    assert "0.0.0.0" not in encoded
    assert '"*"' not in encoded


def test_player_log_status_uses_configured_path_without_reading_or_returning_it(tmp_path) -> None:
    paths = build_local_app_paths(tmp_path / "app-data")
    player_log_path = tmp_path / "Player.log"
    player_log_path.write_text("private log body must not be read", encoding="utf-8")
    paths.config_file.parent.mkdir(parents=True)
    paths.config_file.write_text(json.dumps({"player_log_path": str(player_log_path)}), encoding="utf-8")

    status = build_player_log_path_status(paths)
    encoded = json.dumps(status, sort_keys=True)

    assert status["status"] == "ok"
    assert status["player_log"]["status"] == "configured_exists"
    assert status["player_log"]["display_path"] == "<configured_player_log>"
    assert status["player_log"]["contents_read"] is False
    assert str(player_log_path) not in encoded
    assert "private log body" not in encoded


def test_database_status_reports_missing_without_creating_sqlite_files(tmp_path) -> None:
    paths = build_local_app_paths(tmp_path / "app-data")

    status = build_analytics_database_status(paths)

    assert status["status"] == "missing"
    assert status["database"]["schema_status"] == "missing"
    assert status["database"]["display_path"] == "<app_data>\\db\\mythic_edge.sqlite3"
    assert not paths.analytics_database.exists()
    assert not paths.analytics_database.parent.exists()


def test_database_status_reads_schema_metadata_read_only(tmp_path) -> None:
    paths = build_local_app_paths(tmp_path / "app-data")
    paths.analytics_database.parent.mkdir(parents=True)
    connection = sqlite3.connect(paths.analytics_database)
    try:
        migrations = apply_analytics_migrations(connection, applied_at="2026-05-29T00:00:00Z")
    finally:
        connection.close()

    before_size = paths.analytics_database.stat().st_size
    status = build_analytics_database_status(paths)
    encoded = json.dumps(status, sort_keys=True)

    assert status["status"] == "ok"
    assert status["database"]["schema_status"] == "schema_current"
    assert status["database"]["applied_migration_ids"] == [migrations[0].migration_id]
    assert paths.analytics_database.stat().st_size == before_size
    assert not paths.analytics_database.with_suffix(".sqlite3-wal").exists()
    assert str(paths.analytics_database) not in encoded


def test_match_journal_status_reports_not_initialized_without_creating_sqlite_files(tmp_path) -> None:
    paths = build_local_app_paths(tmp_path / "app-data")
    assert paths.match_journal_database is not None

    status = build_match_journal_write_status(paths)
    encoded = json.dumps(status, sort_keys=True)

    assert status["status"] == "not_initialized"
    assert status["database"]["schema_status"] == "not_initialized"
    assert status["database"]["display_path"] == "<app_data>\\db\\match_journal.sqlite3"
    assert status["database"]["path_ownership"] == "app_owned"
    assert status["write_controls"]["status"] == "enabled_on_first_write"
    assert not paths.match_journal_database.exists()
    assert not paths.match_journal_database.parent.exists()
    assert str(paths.match_journal_database) not in encoded


def test_match_journal_status_reads_schema_metadata_read_only(tmp_path) -> None:
    paths = build_local_app_paths(tmp_path / "app-data")
    assert paths.match_journal_database is not None
    paths.match_journal_database.parent.mkdir(parents=True)
    connection = sqlite3.connect(paths.match_journal_database)
    try:
        migrations = apply_match_journal_migrations(connection, applied_at="2026-06-01T00:00:00Z")
    finally:
        connection.close()

    before_size = paths.match_journal_database.stat().st_size
    status = build_match_journal_write_status(paths)
    encoded = json.dumps(status, sort_keys=True)

    assert status["status"] == "ready"
    assert status["database"]["schema_status"] == "schema_current"
    assert status["database"]["applied_migration_ids"] == [migrations[0].migration_id]
    assert paths.match_journal_database.stat().st_size == before_size
    assert not paths.match_journal_database.with_suffix(".sqlite3-wal").exists()
    assert str(paths.match_journal_database) not in encoded


def test_migration_loader_status_reports_available_without_sql_or_paths() -> None:
    status = build_migration_loader_status()
    encoded = json.dumps(status, sort_keys=True)

    assert status["status"] == "ok"
    assert status["migration_status"] == "available"
    assert status["migrations"]
    assert status["migrations"][0]["checksum_present"] is True
    assert "CREATE TABLE" not in encoded
    assert "src/mythic_edge_parser" not in encoded
