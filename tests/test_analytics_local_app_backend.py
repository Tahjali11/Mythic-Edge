from __future__ import annotations

import json

from fastapi.testclient import TestClient

from mythic_edge_parser.local_app.backend import create_app


def _client(app_data_root) -> TestClient:
    return TestClient(create_app(app_data_root=app_data_root))


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


def test_setup_status_combines_sections_without_exposing_temp_paths_or_writing(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)

    response = client.get("/api/app/setup-status")
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["object"] == "mythic_edge_local_app_setup_status"
    assert payload["status"] == "degraded"
    assert {"paths", "config", "player_log", "analytics_database", "migrations", "runtime", "capabilities"} <= set(
        payload
    )
    assert payload["config"]["status"] == "missing"
    assert payload["analytics_database"]["status"] == "missing"
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
        "/api/runtime/status",
    ):
        response = client.get(route)
        assert response.status_code == 200

    assert not app_root.exists()
    assert list(tmp_path.rglob("*")) == []


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
