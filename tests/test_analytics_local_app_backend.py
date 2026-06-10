from __future__ import annotations

import inspect
import json
import os
import subprocess
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from mythic_edge_parser.local_app import live_watcher_diagnostics
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


class _FakeErrorReportSubmitter:
    def __init__(
        self,
        *,
        labels: set[str] | None = None,
        issue_url: str = "https://github.com/Tahjali11/Mythic-Edge/issues/999",
        raise_status: str | None = None,
        create_raise_status: str | None = None,
    ) -> None:
        self.labels = labels or {"bug", "enhancement", "question", "workflow:problem", "layer:dashboard"}
        self.issue_url = issue_url
        self.raise_status = raise_status
        self.create_raise_status = create_raise_status
        self.created: list[dict[str, object]] = []

    def available_labels(self) -> set[str]:
        if self.raise_status:
            from mythic_edge_parser.local_app.error_reports import GitHubSubmitterError

            raise GitHubSubmitterError(self.raise_status)
        return set(self.labels)

    def create_issue(self, *, title: str, body: str, labels: list[str]) -> tuple[str | None, int | None]:
        if self.create_raise_status:
            from mythic_edge_parser.local_app.error_reports import GitHubSubmitterError

            raise GitHubSubmitterError(self.create_raise_status)
        self.created.append({"title": title, "body": body, "labels": labels})
        return self.issue_url, 999


def _client_with_error_report_submitter(app_data_root, submitter: _FakeErrorReportSubmitter) -> TestClient:
    return TestClient(create_app(app_data_root=app_data_root, error_report_submitter=submitter))


def _preconditions_by_key(payload: dict[str, object]) -> dict[str, dict[str, object]]:
    preconditions = payload["preconditions"]
    assert isinstance(preconditions, list)
    assert [entry["key"] for entry in preconditions] == EXPECTED_PROCESS_PRECONDITION_KEYS
    for entry in preconditions:
        assert set(entry) >= {"key", "status", "reason"}
    return {str(entry["key"]): entry for entry in preconditions}


def _valid_error_report_request(**overrides: object) -> dict[str, object]:
    request = {
        "summary": "Dashboard status did not refresh",
        "report_type": "bug",
        "expected_behavior": "The local app should show the latest safe status labels.",
        "actual_behavior": "The dashboard kept the previous labels after I refreshed the page.",
        "reproduction_steps": "1. Open the local app.\n2. Refresh the dashboard.\n3. Compare the status labels.",
        "affected_area": "local_app_ui",
        "severity": "degraded",
        "current_frontend_surface": "dashboard",
    }
    request.update(overrides)
    return request


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
        "/api/analytics/dashboard/modules",
        "/api/analytics/refresh-state",
        "/api/runtime/status",
        "/api/feedback/error-report/preview",
        "/api/feedback/error-report/submit",
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
        "/api/live/watcher/diagnostics",
        "/api/live/ingest/status",
        "/api/runtime/status",
    ):
        response = client.get(route)
        assert response.status_code == 200

    assert not app_root.exists()
    assert list(tmp_path.rglob("*")) == []


def test_error_report_preview_returns_sanitized_markdown_without_writes(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    private_log_path = tmp_path / "Private Logs" / "Player.log"
    client = _client(app_root)

    response = client.post(
        "/api/feedback/error-report/preview",
        json=_valid_error_report_request(
            actual_behavior=f"The dashboard mentioned {private_log_path} while showing stale labels.",
        ),
    )
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["schema"] == "quality_app_submit_error_report_codex_triage.v1"
    assert payload["status"] == "preview_ready"
    assert payload["issue_title"].startswith("[error-report] [bug] [local_app_ui]")
    assert payload["external_submission_enabled"] is True
    assert "backend_health" in payload["included_diagnostic_categories"]
    assert "privacy_boundary" in payload["included_diagnostic_categories"]
    assert "raw Player.log contents or raw log lines" in payload["excluded_private_data"]
    assert "<redacted_local_path>" in payload["issue_body_markdown"]
    assert "Pasteable Codex Triage Prompt" in payload["issue_body_markdown"]
    assert str(private_log_path) not in encoded
    assert str(tmp_path) not in encoded
    assert not app_root.exists()


def test_error_report_preview_redacts_macos_private_temp_path_shape(tmp_path) -> None:
    private_log_path = "/private/var/folders/zz/test-safe/Private Logs/Player.log"
    client = _client(tmp_path / "app-data")

    response = client.post(
        "/api/feedback/error-report/preview",
        json=_valid_error_report_request(
            reproduction_steps=f"1. Open the dashboard.\n2. Notice the message mentioning {private_log_path}.",
        ),
    )
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["status"] == "preview_ready"
    assert "<redacted_local_path>" in payload["issue_body_markdown"]
    assert private_log_path not in encoded


def test_error_report_preview_blocks_endpoint_like_user_text_without_echoing_value(tmp_path) -> None:
    endpoint_value = "https://" + "example.invalid/hook"
    client = _client(tmp_path / "app-data")

    response = client.post(
        "/api/feedback/error-report/preview",
        json=_valid_error_report_request(actual_behavior=f"The report form displayed endpoint {endpoint_value}."),
    )
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["status"] == "blocked_privacy_guard"
    assert payload["issue_title"] == ""
    assert payload["issue_body_markdown"] == ""
    assert payload["external_submission_enabled"] is False
    assert "privacy_guard_blocked:actual_behavior" in payload["warnings"]
    assert endpoint_value not in encoded


def test_error_report_preview_rejects_invalid_request(tmp_path) -> None:
    client = _client(tmp_path / "app-data")

    invalid_response = client.post(
        "/api/feedback/error-report/preview",
        json=_valid_error_report_request(affected_area="workbook", summary=""),
    )

    assert invalid_response.status_code == 200
    assert invalid_response.json()["status"] == "invalid_request"


def test_error_report_submit_rebuilds_preview_and_uses_mocked_github_cli_boundary(tmp_path) -> None:
    submitter = _FakeErrorReportSubmitter()
    client = _client_with_error_report_submitter(tmp_path / "app-data", submitter)

    response = client.post("/api/feedback/error-report/submit", json=_valid_error_report_request())
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["object"] == "mythic_edge_local_app_error_report_submission"
    assert payload["schema_version"] == "quality_app_error_report_github_submission.v1"
    assert payload["status"] == "submitted"
    assert payload["submitted"] is True
    assert payload["issue_url"] == "https://github.com/Tahjali11/Mythic-Edge/issues/999"
    assert payload["issue_number"] == 999
    assert payload["fallback_available"] is True
    assert payload["labels"] == ["bug", "layer:dashboard", "workflow:problem"]
    assert submitter.created == [
        {
            "title": payload["issue_title"],
            "body": payload["issue_body_markdown"],
            "labels": ["bug", "layer:dashboard", "workflow:problem"],
        }
    ]
    assert "secret-like-value" not in encoded
    assert str(tmp_path) not in encoded


def test_error_report_submit_blocks_privacy_guard_without_calling_github(tmp_path) -> None:
    submitter = _FakeErrorReportSubmitter()
    client = _client_with_error_report_submitter(tmp_path / "app-data", submitter)
    endpoint_value = "https://" + "example.invalid/hook"

    response = client.post(
        "/api/feedback/error-report/submit",
        json=_valid_error_report_request(actual_behavior=f"The report form displayed endpoint {endpoint_value}."),
    )
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["status"] == "blocked_privacy_guard"
    assert payload["submitted"] is False
    assert payload["fallback_available"] is False
    assert submitter.created == []
    assert endpoint_value not in encoded


def test_error_report_submit_degrades_to_fallback_labels_for_feedback_and_features(tmp_path) -> None:
    submitter = _FakeErrorReportSubmitter()
    client = _client_with_error_report_submitter(tmp_path / "app-data", submitter)

    feedback = client.post(
        "/api/feedback/error-report/submit",
        json={
            "summary": "Status copy is confusing",
            "report_type": "feedback",
            "feedback": "The live capture status should explain ready versus active.",
            "affected_area": "local_app_ui",
            "severity": "question",
            "current_frontend_surface": "feedback",
        },
    ).json()
    feature = client.post(
        "/api/feedback/error-report/submit",
        json={
            "summary": "Add a report queue",
            "report_type": "feature_request",
            "feature_goal": "Track submitted local-app reports.",
            "feature_location": "Feedback route.",
            "feature_success": "Show the last submitted issue URL for the current session.",
            "affected_area": "local_app_ui",
            "severity": "question",
            "current_frontend_surface": "feedback",
        },
    ).json()

    assert feedback["status"] == "submitted"
    assert feedback["labels"] == ["layer:dashboard", "question", "workflow:problem"]
    assert feature["status"] == "submitted"
    assert feature["labels"] == ["enhancement", "layer:dashboard", "workflow:problem"]


def test_error_report_submit_returns_safe_fallback_for_github_tool_failures(tmp_path) -> None:
    missing_gh_client = _client_with_error_report_submitter(
        tmp_path / "app-data",
        _FakeErrorReportSubmitter(raise_status="blocked_missing_gh"),
    )
    unauthenticated_client = _client_with_error_report_submitter(
        tmp_path / "app-data-unauthenticated",
        _FakeErrorReportSubmitter(raise_status="blocked_gh_unauthenticated"),
    )
    wrong_repo_client = _client_with_error_report_submitter(
        tmp_path / "app-data-wrong-repo",
        _FakeErrorReportSubmitter(issue_url="https://github.com/Other/Repo/issues/999"),
    )
    failed_client = _client_with_error_report_submitter(
        tmp_path / "app-data-failed",
        _FakeErrorReportSubmitter(create_raise_status="submission_failed"),
    )
    missing_label_client = _client_with_error_report_submitter(
        tmp_path / "app-data-labels",
        _FakeErrorReportSubmitter(labels={"bug"}),
    )

    missing_gh = missing_gh_client.post("/api/feedback/error-report/submit", json=_valid_error_report_request()).json()
    unauthenticated = unauthenticated_client.post(
        "/api/feedback/error-report/submit",
        json=_valid_error_report_request(),
    ).json()
    wrong_repo = wrong_repo_client.post("/api/feedback/error-report/submit", json=_valid_error_report_request()).json()
    failed = failed_client.post("/api/feedback/error-report/submit", json=_valid_error_report_request()).json()
    missing_labels = missing_label_client.post(
        "/api/feedback/error-report/submit",
        json=_valid_error_report_request(),
    ).json()

    assert missing_gh["status"] == "blocked_missing_gh"
    assert missing_gh["submitted"] is False
    assert missing_gh["fallback_available"] is True
    assert missing_gh["issue_body_markdown"].startswith("# [error-report]")
    assert unauthenticated["status"] == "blocked_gh_unauthenticated"
    assert unauthenticated["submitted"] is False
    assert unauthenticated["fallback_available"] is True
    assert wrong_repo["status"] == "blocked_wrong_repo"
    assert wrong_repo["issue_url"] is None
    assert wrong_repo["errors"] == ["unexpected_issue_url"]
    assert failed["status"] == "submission_failed"
    assert failed["errors"] == ["submission_failed"]
    assert missing_labels["status"] == "blocked_label_unavailable"
    assert missing_labels["submitted"] is False
    assert missing_labels["fallback_available"] is True


def test_real_gh_cli_submitter_checks_auth_and_labels_with_argument_lists(monkeypatch) -> None:
    from mythic_edge_parser.local_app import error_reports

    gh_path = "C:\\Tools\\gh.exe"
    commands: list[list[str]] = []

    def fake_which(name: str) -> str | None:
        return gh_path if name == "gh" else None

    def fake_run(command: list[str], *, capture_output: bool, shell: bool, text: bool, timeout: int):
        commands.append(command)
        assert capture_output is True
        assert shell is False
        assert text is True
        assert timeout == 3
        if command[1:4] == ["auth", "status", "--hostname"]:
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
        if command[1:3] == ["label", "list"]:
            stdout = "bug\tBug\nworkflow:problem\tProblem\nlayer:dashboard\tDashboard\n"
            return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")
        raise AssertionError(f"Unexpected gh command: {command!r}")

    monkeypatch.setattr(error_reports.shutil, "which", fake_which)
    monkeypatch.setattr(error_reports.subprocess, "run", fake_run)

    labels = error_reports.GhCliIssueSubmitter(timeout_seconds=3).available_labels()

    assert labels == {"bug", "workflow:problem", "layer:dashboard"}
    assert commands == [
        [gh_path, "auth", "status", "--hostname", "github.com"],
        [gh_path, "label", "list", "--repo", "Tahjali11/Mythic-Edge", "--limit", "100"],
    ]


def test_real_gh_cli_submitter_creates_issue_with_argument_list_and_temp_body_cleanup(monkeypatch) -> None:
    from mythic_edge_parser.local_app import error_reports

    gh_path = "C:\\Tools\\gh.exe"
    body = "# Synthetic sanitized report\n\nNo private artifacts."
    captured_body_path: Path | None = None
    captured_command: list[str] | None = None

    def fake_which(name: str) -> str | None:
        return gh_path if name == "gh" else None

    def fake_run(command: list[str], *, capture_output: bool, shell: bool, text: bool, timeout: int):
        nonlocal captured_body_path, captured_command
        assert capture_output is True
        assert shell is False
        assert text is True
        assert timeout == 3
        captured_command = command
        body_path = Path(command[command.index("--body-file") + 1])
        captured_body_path = body_path
        assert body_path.name == "issue-body.md"
        assert body_path.exists()
        assert body_path.read_text(encoding="utf-8") == body
        return subprocess.CompletedProcess(
            command,
            0,
            stdout="https://github.com/Tahjali11/Mythic-Edge/issues/1000\n",
            stderr="raw tool output must not be returned",
        )

    monkeypatch.setattr(error_reports.shutil, "which", fake_which)
    monkeypatch.setattr(error_reports.subprocess, "run", fake_run)

    issue_url, issue_number = error_reports.GhCliIssueSubmitter(timeout_seconds=3).create_issue(
        title="[error-report] Synthetic",
        body=body,
        labels=["bug", "layer:dashboard", "workflow:problem"],
    )

    assert issue_url == "https://github.com/Tahjali11/Mythic-Edge/issues/1000"
    assert issue_number == 1000
    assert captured_command == [
        gh_path,
        "issue",
        "create",
        "--repo",
        "Tahjali11/Mythic-Edge",
        "--title",
        "[error-report] Synthetic",
        "--body-file",
        str(captured_body_path),
        "--label",
        "bug",
        "--label",
        "layer:dashboard",
        "--label",
        "workflow:problem",
    ]
    assert captured_body_path is not None
    assert not captured_body_path.exists()


def test_real_gh_cli_submitter_maps_tool_failures_and_cleans_temp_body(monkeypatch) -> None:
    from mythic_edge_parser.local_app import error_reports

    gh_path = "C:\\Tools\\gh.exe"
    captured_failure_body_path: Path | None = None

    monkeypatch.setattr(error_reports.shutil, "which", lambda name: None)
    with pytest.raises(error_reports.GitHubSubmitterError) as missing_gh:
        error_reports.GhCliIssueSubmitter(timeout_seconds=3).available_labels()
    assert missing_gh.value.status == "blocked_missing_gh"

    monkeypatch.setattr(error_reports.shutil, "which", lambda name: gh_path if name == "gh" else None)

    def fake_unauthenticated_run(command: list[str], **_kwargs: object):
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="do not echo auth output")

    monkeypatch.setattr(error_reports.subprocess, "run", fake_unauthenticated_run)
    with pytest.raises(error_reports.GitHubSubmitterError) as unauthenticated:
        error_reports.GhCliIssueSubmitter(timeout_seconds=3).available_labels()
    assert unauthenticated.value.status == "blocked_gh_unauthenticated"

    def fake_wrong_repo_run(command: list[str], **_kwargs: object):
        if command[1:3] == ["auth", "status"]:
            return subprocess.CompletedProcess(command, 0, stdout="", stderr="")
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="do not echo repo output")

    monkeypatch.setattr(error_reports.subprocess, "run", fake_wrong_repo_run)
    with pytest.raises(error_reports.GitHubSubmitterError) as wrong_repo:
        error_reports.GhCliIssueSubmitter(timeout_seconds=3).available_labels()
    assert wrong_repo.value.status == "blocked_wrong_repo"

    def fake_submission_failed_run(command: list[str], **_kwargs: object):
        nonlocal captured_failure_body_path
        body_path = Path(command[command.index("--body-file") + 1])
        captured_failure_body_path = body_path
        assert body_path.exists()
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="do not echo failure output")

    monkeypatch.setattr(error_reports.subprocess, "run", fake_submission_failed_run)
    with pytest.raises(error_reports.GitHubSubmitterError) as submission_failed:
        error_reports.GhCliIssueSubmitter(timeout_seconds=3).create_issue(
            title="[error-report] Synthetic failure",
            body="Sanitized fallback body",
            labels=["bug"],
        )
    assert submission_failed.value.status == "submission_failed"
    assert captured_failure_body_path is not None
    assert not captured_failure_body_path.exists()


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
    diagnostics_payload = client.get("/api/live/watcher/diagnostics").json()
    ingest_payload = client.get("/api/live/ingest/status").json()
    encoded = json.dumps(
        {
            "player_log": player_log_payload,
            "watcher": watcher_payload,
            "process": process_payload,
            "diagnostics": diagnostics_payload,
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
    assert diagnostics_payload["object"] == "mythic_edge_local_app_live_watcher_diagnostics"
    assert diagnostics_payload["schema_version"] == "live_app_watcher_diagnostics.v1"
    assert diagnostics_payload["mode"] == "read_only_composition"
    assert diagnostics_payload["privacy"] == {
        "raw_player_log_content_included": False,
        "raw_player_log_path_included": False,
        "raw_hashes_included": False,
        "raw_sql_included": False,
        "stack_traces_included": False,
        "secrets_or_environment_values_included": False,
    }
    assert diagnostics_payload["capabilities"] == {
        "read_only": True,
        "starts_watcher": False,
        "stops_watcher": False,
        "tails_player_log": False,
        "writes_sqlite": False,
        "writes_diagnostics_files": False,
        "external_transport_allowed": False,
    }
    assert diagnostics_payload["sources"]["player_log_status"]["supplied"] is True
    assert diagnostics_payload["sources"]["watcher_status"]["supplied"] is True
    assert diagnostics_payload["sources"]["watcher_process_status"]["supplied"] is True
    assert diagnostics_payload["sources"]["live_ingest_status"]["supplied"] is True
    assert diagnostics_payload["sources"]["tailer_event_bridge"]["supplied"] is False
    diagnostic_keys = {entry["key"] for entry in diagnostics_payload["diagnostics"]}
    assert "readability_not_probed" in diagnostic_keys
    assert "rotation_detection_deferred" in diagnostic_keys
    assert "truncation_detection_deferred" in diagnostic_keys
    assert "duplication_detection_deferred" in diagnostic_keys
    assert "raw_player_log_content_excluded" in diagnostic_keys
    assert "destructive_controls_absent" in diagnostic_keys
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
        "/api/live/watcher/diagnostics",
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


def test_live_watcher_diagnostics_reports_stale_metadata_without_reading_contents(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    player_log_path = tmp_path / "Player.log"
    player_log_path.write_text("private stale log body must not be returned", encoding="utf-8")
    old_timestamp = time.time() - (48 * 60 * 60)
    os.utime(player_log_path, (old_timestamp, old_timestamp))
    config_file = app_root / "config" / "app_config.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text(json.dumps({"player_log_path": str(player_log_path)}), encoding="utf-8")
    client = _client(app_root)

    payload = client.get("/api/live/watcher/diagnostics").json()
    encoded = json.dumps(payload, sort_keys=True)
    diagnostic_by_key = {entry["key"]: entry for entry in payload["diagnostics"]}

    assert payload["status"] == "degraded"
    assert diagnostic_by_key["player_log_stale"]["severity"] == "warning"
    assert diagnostic_by_key["player_log_stale"]["evidence_availability"] == "metadata_only"
    assert str(player_log_path) not in encoded
    assert "private stale log body" not in encoded


def test_live_watcher_diagnostics_reports_malformed_state_without_repairing_it(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    player_log_path = tmp_path / "Player.log"
    player_log_path.write_text("private log body must not be returned", encoding="utf-8")
    config_file = app_root / "config" / "app_config.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text(json.dumps({"player_log_path": str(player_log_path)}), encoding="utf-8")
    state_file = app_root / "jobs" / "live_watcher_state.json"
    state_file.parent.mkdir(parents=True)
    state_file.write_text("{", encoding="utf-8")
    client = _client(app_root)

    payload = client.get("/api/live/watcher/diagnostics").json()
    encoded = json.dumps(payload, sort_keys=True)
    diagnostic_by_key = {entry["key"]: entry for entry in payload["diagnostics"]}

    assert payload["status"] == "blocked"
    assert diagnostic_by_key["watcher_state_malformed"]["severity"] == "blocked"
    assert state_file.read_text(encoding="utf-8") == "{"
    assert str(state_file) not in encoded
    assert str(player_log_path) not in encoded


def test_live_watcher_diagnostics_does_not_call_runner_tailer_or_report_builders() -> None:
    source = inspect.getsource(live_watcher_diagnostics)

    for forbidden in (
        "runner.main",
        "MtgaEventStream.start",
        "FileTailer.open_from_start",
        "FileTailer.open_from_end",
        "FileTailer.poll",
        "FileTailer.poll_once",
        "build_parser_diagnostics_report",
        "write_parser_diagnostics_report",
        "build_player_log_drift_report",
        "write_player_log_drift_report",
    ):
        assert forbidden not in source


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
