from __future__ import annotations

import json

from fastapi.testclient import TestClient

from mythic_edge_parser.local_app.backend import create_app

EXPECTED_PROCESS_PRECONDITION_KEYS = [
    "player_log_ready",
    "app_data_root_available",
    "state_directory_available",
    "single_instance_guard_available",
    "supervisor_target_defined",
    "external_transport_disabled",
    "live_sqlite_ingest_contract_present",
    "frontend_controls_authorized",
]


def _client(app_data_root) -> TestClient:
    return TestClient(create_app(app_data_root=app_data_root))


def _preconditions_by_key(payload: dict[str, object]) -> dict[str, dict[str, object]]:
    preconditions = payload["preconditions"]
    assert isinstance(preconditions, list)
    assert [entry["key"] for entry in preconditions] == EXPECTED_PROCESS_PRECONDITION_KEYS
    for entry in preconditions:
        assert set(entry) >= {"key", "status", "reason"}
    return {str(entry["key"]): entry for entry in preconditions}


def test_health_endpoint_reports_setup_status_only_capabilities(tmp_path) -> None:
    client = _client(tmp_path / "app-data")

    response = client.get("/api/health")
    payload = response.json()

    assert response.status_code == 200
    assert payload == {
        "object": "mythic_edge_local_app_health",
        "schema_version": "analytics_app_backend_setup_status.v1",
        "status": "ok",
        "mode": "setup_status_only",
        "capabilities": {
            "setup_status": "enabled",
            "config_write": "disabled",
            "database_init": "disabled",
            "manual_import": "enabled",
            "match_journal_write_controls": "enabled",
            "live_watcher": "disabled",
            "parser_runner_control": "disabled",
            "frontend": "deferred",
        },
    }


def test_read_only_endpoint_inventory_and_no_wildcard_cors(tmp_path) -> None:
    client = _client(tmp_path / "app-data")
    expected_routes = {
        "/api/health",
        "/api/app/setup-status",
        "/api/app/config",
        "/api/app/paths",
        "/api/analytics/database/status",
        "/api/live/player-log/status",
        "/api/live/watcher/status",
        "/api/live/watcher/process",
        "/api/analytics/matches",
        "/api/analytics/games",
        "/api/analytics/opening-hands",
        "/api/analytics/mulligans",
        "/api/analytics/gameplay-actions",
        "/api/analytics/opponent-card-observations",
        "/api/analytics/play-draw-splits",
        "/api/analytics/game1-postboard-splits",
        "/api/runtime/status",
        "/api/imports/jsonl",
        "/api/imports/jsonl/upload",
        "/api/imports/jobs/{job_id}",
    }
    route_paths = {route.path for route in client.app.routes}

    assert expected_routes <= route_paths
    assert all("DELETE" not in route.methods for route in client.app.routes)
    assert client.post("/api/health").status_code == 405

    response = client.get("/api/health", headers={"Origin": "http://example.invalid"})
    assert response.headers.get("access-control-allow-origin") != "*"


def test_backend_allows_only_explicit_loopback_frontend_cors(tmp_path) -> None:
    client = _client(tmp_path / "app-data")

    allowed = client.get("/api/health", headers={"Origin": "http://127.0.0.1:5173"})
    preflight = client.options(
        "/api/imports/jsonl",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    disallowed = client.get("/api/health", headers={"Origin": "http://example.invalid"})

    assert allowed.headers.get("access-control-allow-origin") == "http://127.0.0.1:5173"
    assert preflight.headers.get("access-control-allow-origin") == "http://127.0.0.1:5173"
    assert "POST" in preflight.headers.get("access-control-allow-methods", "")
    assert disallowed.headers.get("access-control-allow-origin") is None


def test_backend_cors_uses_local_frontend_origin_from_launcher_env(tmp_path) -> None:
    client = TestClient(
        create_app(
            app_data_root=tmp_path / "app-data",
            env={"MYTHIC_EDGE_LOCAL_APP_FRONTEND_ORIGIN": "http://127.0.0.1:5180"},
        ),
    )

    response = client.get("/api/health", headers={"Origin": "http://127.0.0.1:5180"})

    assert response.headers.get("access-control-allow-origin") == "http://127.0.0.1:5180"


def test_backend_ignores_non_loopback_frontend_origin_env(tmp_path) -> None:
    client = TestClient(
        create_app(
            app_data_root=tmp_path / "app-data",
            env={"MYTHIC_EDGE_LOCAL_APP_FRONTEND_ORIGIN": "https://example.invalid"},
        ),
    )

    response = client.get("/api/health", headers={"Origin": "https://example.invalid"})

    assert response.headers.get("access-control-allow-origin") is None


def test_backend_uses_launcher_app_data_root_env_for_status_and_writes(tmp_path) -> None:
    launcher_root = tmp_path / "launcher-app-data"
    local_app_data = tmp_path / "local-app-data"
    default_root = local_app_data / "MythicEdgeDev"
    client = TestClient(
        create_app(
            env={
                "LOCALAPPDATA": str(local_app_data),
                "MYTHIC_EDGE_LOCAL_APP_DATA_ROOT": str(launcher_root),
            },
        ),
    )

    setup_payload = client.get("/api/app/setup-status").json()
    encoded_setup = json.dumps(setup_payload, sort_keys=True)

    assert setup_payload["match_journal"]["database"]["display_path"] == "<app_data>\\db\\match_journal.sqlite3"
    assert str(launcher_root) not in encoded_setup
    assert str(default_root) not in encoded_setup
    assert not launcher_root.exists()
    assert not default_root.exists()

    write_response = client.post(
        "/api/journal/notes",
        json={"note_scope": "unattached", "note_text": "Synthetic local note."},
    )

    assert write_response.status_code == 200
    assert (launcher_root / "db" / "match_journal.sqlite3").is_file()
    assert not (launcher_root / "db" / "mythic_edge.sqlite3").exists()
    assert not default_root.exists()


def test_setup_status_combines_sections_without_exposing_temp_paths_or_writing(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)

    response = client.get("/api/app/setup-status")
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["object"] == "mythic_edge_local_app_setup_status"
    assert payload["status"] == "degraded"
    assert {
        "paths",
        "config",
        "player_log",
        "analytics_database",
        "match_journal",
        "migrations",
        "runtime",
        "capabilities",
    } <= set(payload)
    assert payload["config"]["status"] == "missing"
    assert payload["analytics_database"]["status"] == "missing"
    assert payload["match_journal"]["status"] == "not_initialized"
    assert payload["match_journal"]["database"]["display_path"] == "<app_data>\\db\\match_journal.sqlite3"
    assert payload["capabilities"]["match_journal_write_controls"] == "enabled_on_first_write"
    assert payload["runtime"]["parser_runner"]["status"] == "deferred"
    assert str(app_root) not in encoded
    assert not app_root.exists()


def test_config_and_paths_routes_hide_temp_roots_and_raw_config_values(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    config_file = app_root / "config" / "app_config.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text(
        json.dumps(
            {
                "player_log_path": str(tmp_path / "Player.log"),
                "webhook_url": "https://example.invalid/hook",
            }
        ),
        encoding="utf-8",
    )
    client = _client(app_root)

    config_payload = client.get("/api/app/config").json()
    paths_payload = client.get("/api/app/paths").json()
    encoded = json.dumps({"config": config_payload, "paths": paths_payload}, sort_keys=True)

    assert config_payload["status"] == "ok"
    assert config_payload["loaded_fields"] == ["player_log_path"]
    assert config_payload["secret_like_field_count"] == 1
    assert paths_payload["app_data_root"]["display_path"] == "<app_data>"
    assert str(app_root) not in encoded
    assert "https://example.invalid/hook" not in encoded


def test_config_route_redacts_unsafe_unexpected_field_names(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    config_file = app_root / "config" / "app_config.json"
    unsafe_url_key = "https://" + "example.invalid/config-key"
    unsafe_path_key = str(tmp_path / "private_config_key")
    config_file.parent.mkdir(parents=True)
    config_file.write_text(
        json.dumps(
            {
                "backend_host": "127.0.0.1",
                "safe_extra": "visible-name-only",
                unsafe_url_key: "url-key-value",
                unsafe_path_key: "path-key-value",
                "webhook_url": "secret-like-value",
            }
        ),
        encoding="utf-8",
    )
    client = _client(app_root)

    payload = client.get("/api/app/config").json()
    encoded = json.dumps(payload, sort_keys=True)

    assert payload["status"] == "ok"
    assert payload["unexpected_fields"] == ["safe_extra"]
    assert payload["secret_like_field_count"] == 3
    assert unsafe_url_key not in encoded
    assert unsafe_path_key not in encoded
    assert "webhook_url" not in encoded
    assert "url-key-value" not in encoded
    assert "path-key-value" not in encoded
    assert "secret-like-value" not in encoded


def test_setup_status_get_routes_do_not_create_local_app_artifacts(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)

    for route in (
        "/api/health",
        "/api/app/setup-status",
        "/api/app/config",
        "/api/app/paths",
        "/api/analytics/database/status",
        "/api/live/player-log/status",
        "/api/live/watcher/status",
        "/api/live/watcher/process",
        "/api/live/ingest/status",
        "/api/runtime/status",
    ):
        response = client.get(route)
        assert response.status_code == 200

    assert not app_root.exists()
    assert list(tmp_path.rglob("*")) == []


def test_live_status_routes_report_symbolic_metadata_and_readiness_only(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    player_log_path = tmp_path / "Player.log"
    player_log_path.write_text("private log body must not be returned", encoding="utf-8")
    config_file = app_root / "config" / "app_config.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text(json.dumps({"player_log_path": str(player_log_path)}), encoding="utf-8")
    client = _client(app_root)

    player_log_payload = client.get("/api/live/player-log/status").json()
    watcher_payload = client.get("/api/live/watcher/status").json()
    process_payload = client.get("/api/live/watcher/process").json()
    ingest_payload = client.get("/api/live/ingest/status").json()
    encoded = json.dumps(
        {
            "player_log": player_log_payload,
            "watcher": watcher_payload,
            "process": process_payload,
            "ingest": ingest_payload,
        },
        sort_keys=True,
    )

    assert player_log_payload["object"] == "mythic_edge_local_app_live_player_log_status"
    assert player_log_payload["schema_version"] == "live_app_player_log_path_watcher_status.v1"
    assert player_log_payload["player_log"]["status"] == "configured_exists"
    assert player_log_payload["player_log"]["display_path"] == "<configured_player_log>"
    assert player_log_payload["player_log"]["contents_read"] is False
    assert player_log_payload["player_log"]["tailing_started"] is False
    assert watcher_payload["object"] == "mythic_edge_local_app_live_watcher_status"
    assert watcher_payload["watcher"]["status"] == "ready"
    assert watcher_payload["watcher"]["mode"] == "readiness_only"
    assert watcher_payload["watcher"]["running"] is False
    assert watcher_payload["watcher"]["start_allowed"] is False
    assert watcher_payload["watcher"]["stop_allowed"] is False
    assert watcher_payload["watcher"]["parser_runner_started"] is False
    assert watcher_payload["watcher"]["tailing_started"] is False
    assert watcher_payload["watcher"]["sqlite_live_writes_enabled"] is False
    assert process_payload["object"] == "mythic_edge_local_app_live_watcher_process_status"
    assert process_payload["schema_version"] == "live_app_player_log_watcher_process_control_safeguards.v1"
    assert process_payload["status"] == "not_initialized"
    assert process_payload["process_control"]["mode"] == "safeguards_only"
    assert process_payload["process_control"]["start_allowed"] is False
    assert process_payload["process_control"]["stop_allowed"] is False
    assert process_payload["process_control"]["start_route_enabled"] is False
    assert process_payload["process_control"]["stop_route_enabled"] is False
    assert process_payload["process_control"]["ui_controls_allowed"] is False
    assert process_payload["process_control"]["automatic_start_enabled"] is False
    assert process_payload["process_control"]["parser_runner_started"] is False
    assert process_payload["process_control"]["tailing_started"] is False
    assert process_payload["process_control"]["sqlite_live_writes_enabled"] is False
    assert process_payload["process_control"]["external_transport_allowed"] is False
    assert process_payload["watcher"]["running"] is False
    assert process_payload["watcher"]["pid_verified"] is False
    assert process_payload["state"]["raw_path_exposed"] is False
    assert _preconditions_by_key(process_payload)["player_log_ready"]["status"] == "pass"
    assert _preconditions_by_key(process_payload)["live_sqlite_ingest_contract_present"]["status"] == "pass"
    assert ingest_payload["object"] == "mythic_edge_local_app_live_parser_sqlite_capture_status"
    assert ingest_payload["schema_version"] == "live_app_parser_owned_fact_capture_sqlite.v1"
    assert ingest_payload["status"] == "disabled"
    assert ingest_payload["mode"] == "status_only"
    assert ingest_payload["source_kind"] == "live_parser"
    assert ingest_payload["database"] == {
        "configured": True,
        "display_path": "<app_data>\\db\\mythic_edge.sqlite3",
    }
    assert ingest_payload["capabilities"]["live_sqlite_capture_contract_present"] is True
    assert ingest_payload["capabilities"]["final_match_game_fact_capture_supported"] is True
    assert ingest_payload["capabilities"]["provisional_fact_capture_supported"] is False
    assert ingest_payload["capabilities"]["gameplay_action_live_capture_supported"] is False
    assert ingest_payload["capabilities"]["opponent_observation_live_capture_supported"] is False
    assert ingest_payload["capabilities"]["field_evidence_live_capture_supported"] is False
    assert ingest_payload["capabilities"]["raw_player_log_storage_supported"] is False
    assert ingest_payload["capabilities"]["external_transport_allowed"] is False
    assert ingest_payload["process_control"]["parser_runner_started"] is False
    assert ingest_payload["process_control"]["tailing_started"] is False
    assert ingest_payload["process_control"]["sqlite_live_writes_enabled"] is False
    assert ingest_payload["last_result"] is None
    assert str(player_log_path) not in encoded
    assert "private log body" not in encoded


def test_live_watcher_process_routes_do_not_expose_start_stop_controls(tmp_path) -> None:
    client = _client(tmp_path / "app-data")

    for route in (
        "/api/live/watcher/process",
        "/api/live/watcher/start",
        "/api/live/watcher/stop",
        "/api/live/watcher/restart",
    ):
        response = client.post(route)
        assert response.status_code in {404, 405}


def test_live_watcher_blocks_configured_missing_player_log(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    missing_player_log = tmp_path / "missing" / "Player.log"
    config_file = app_root / "config" / "app_config.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text(json.dumps({"player_log_path": str(missing_player_log)}), encoding="utf-8")
    client = _client(app_root)

    watcher_payload = client.get("/api/live/watcher/status").json()
    process_payload = client.get("/api/live/watcher/process").json()
    encoded = json.dumps({"watcher": watcher_payload, "process": process_payload}, sort_keys=True)

    assert watcher_payload["watcher"]["status"] == "blocked_missing_log"
    assert watcher_payload["watcher"]["reason"] == "player_log_missing"
    assert watcher_payload["watcher"]["start_allowed"] is False
    assert watcher_payload["watcher"]["tailing_started"] is False
    assert process_payload["status"] == "blocked_missing_log"
    assert process_payload["process_control"]["reason"] == "player_log_missing"
    assert process_payload["watcher"]["running"] is False
    assert str(missing_player_log) not in encoded


def test_database_status_route_reports_missing_without_creating_database(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    database_path = app_root / "db" / "mythic_edge.sqlite3"
    client = _client(app_root)

    payload = client.get("/api/analytics/database/status").json()

    assert payload["object"] == "mythic_edge_local_app_analytics_database_status"
    assert payload["status"] == "missing"
    assert payload["database"]["schema_status"] == "missing"
    assert not database_path.exists()
    assert not database_path.parent.exists()


def test_runtime_state_route_is_explicitly_non_controlling(tmp_path) -> None:
    client = _client(tmp_path / "app-data")

    payload = client.get("/api/runtime/status").json()

    assert payload == {
        "object": "mythic_edge_local_app_runtime" + "_status",
        "schema_version": "analytics_app_backend_setup_status.v1",
        "status": "ok",
        "backend": {"status": "running", "host": "127.0.0.1"},
        "parser_runner": {"status": "deferred"},
        "live_watcher": {"status": "deferred"},
        "manual_import": {"status": "enabled"},
        "legacy_status_api": {"status": "separate_reference_surface"},
    }
