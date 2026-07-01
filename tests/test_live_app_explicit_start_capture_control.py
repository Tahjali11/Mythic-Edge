from __future__ import annotations

import asyncio
import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

from fastapi.testclient import TestClient

from mythic_edge_parser.app import config as app_config
from mythic_edge_parser.local_app import live_capture_control, setup_status
from mythic_edge_parser.local_app.backend import create_app
from mythic_edge_parser.local_app.live_capture_control import (
    LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION,
    LIVE_CAPTURE_SCHEMA_VERSION,
    LIVE_CAPTURE_STATE_FILENAME,
)
from mythic_edge_parser.local_app.paths import build_local_app_paths
from tests.local_app_request_guard_helpers import guarded_client


class _FakeSupervisor:
    def __init__(self, paths, *, ownership_id: str) -> None:
        self.paths = paths
        self.ownership_id = ownership_id
        self.running = False

    def start(self) -> None:
        self.running = True
        state = self.paths.jobs_dir / LIVE_CAPTURE_STATE_FILENAME
        payload = json.loads(state.read_text(encoding="utf-8"))
        payload.update(
            {
                "status": "capturing",
                "tailing_started": True,
                "sqlite_live_writes_enabled": True,
                "updated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                "heartbeat": {
                    "schema_version": LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION,
                    "status": "waiting",
                    "heartbeat_updated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                    "capture_duration_seconds": 0,
                    "heartbeat_age_seconds": 0,
                    "stale_after_seconds": 30,
                },
                "progress": {
                    "schema_version": LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION,
                    "log_poll_count": 0,
                    "log_chunks_seen": 0,
                    "structured_entry_count": 0,
                    "parser_event_count": 0,
                    "parser_event_kinds_seen": [],
                    "match_ids_seen_count": 0,
                    "current_match_detected": False,
                    "current_match_game_wins": None,
                    "current_match_game_losses": None,
                    "last_completed_match_result": None,
                    "last_completed_match_game_wins": None,
                    "last_completed_match_game_losses": None,
                    "completed_game_rows_seen": 0,
                    "sqlite_write_attempt_count": 0,
                    "sqlite_rows_written": 0,
                    "last_no_write_reason": "no_parser_events_routed",
                    "last_event_seen_at": None,
                    "last_sqlite_write_at": None,
                },
                "warnings": ["waiting_for_events"],
                "errors": [],
            },
        )
        state.write_text(json.dumps(payload), encoding="utf-8")

    def stop(self) -> None:
        self.running = False

    def is_running(self) -> bool:
        return self.running


class _FakeStream:
    def __init__(self) -> None:
        self.shutdown_called = False

    async def shutdown(self) -> None:
        self.shutdown_called = True


class _FakeSubscriber:
    def __init__(self, event: object) -> None:
        self._event = event
        self._sent = False

    async def recv(self) -> object | None:
        if self._sent:
            return None
        self._sent = True
        return self._event


def _client(app_data_root: Path) -> TestClient:
    return guarded_client(create_app(app_data_root=app_data_root))


def _configure_player_log(app_root: Path, player_log_path: Path) -> None:
    player_log_path.write_text("private log body must never be returned", encoding="utf-8")
    config_file = app_root / "config" / "app_config.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text(json.dumps({"player_log_path": str(player_log_path)}), encoding="utf-8")


def _fake_supervisor_factory(paths, *, ownership_id: str) -> _FakeSupervisor:
    return _FakeSupervisor(paths, ownership_id=ownership_id)


def test_capture_status_get_is_read_only_and_ready_to_start_when_preconditions_pass(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    player_log_path = tmp_path / "Player.log"
    _configure_player_log(app_root, player_log_path)
    client = _client(app_root)

    response = client.get("/api/live/capture/status")
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["object"] == "mythic_edge_local_app_live_capture_status"
    assert payload["schema_version"] == LIVE_CAPTURE_SCHEMA_VERSION
    assert payload["status"] == "ready_to_start"
    assert payload["mode"] == "explicit_operator_control"
    assert payload["capture"]["start_allowed"] is True
    assert payload["capture"]["stop_allowed"] is False
    assert payload["capture"]["external_transport_allowed"] is False
    assert payload["capture"]["raw_player_log_storage_enabled"] is False
    assert payload["state"]["display_path"] == "<app_data>\\jobs\\live_capture_state.json"
    assert payload["state"]["raw_path_exposed"] is False
    assert payload["heartbeat"]["schema_version"] == LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION
    assert payload["heartbeat"]["status"] == "not_started"
    assert payload["heartbeat"]["heartbeat_updated_at"] is None
    assert payload["progress"]["schema_version"] == LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION
    assert payload["progress"]["log_chunks_seen"] == 0
    assert payload["progress"]["last_no_write_reason"] == "not_started"
    assert payload["parser_status_blurb"] == {
        "code": "ready_to_start",
        "text": "Ready to start capture.",
        "tone": "neutral",
    }
    assert not (app_root / "jobs").exists()
    assert not (app_root / "db" / "mythic_edge.sqlite3").exists()
    assert str(player_log_path) not in encoded
    assert "private log body" not in encoded


def test_capture_status_redacts_unsafe_state_warning_error_and_result_text(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    player_log_path = tmp_path / "Player.log"
    _configure_player_log(app_root, player_log_path)
    unsafe_path = r"C:\operator\logs\Player.log"
    unsafe_url = "https://example.invalid/local/capture"
    now = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    state_file = app_root / "jobs" / LIVE_CAPTURE_STATE_FILENAME
    state_file.parent.mkdir(parents=True)
    state_file.write_text(
        json.dumps(
            {
                "status": "failed",
                "supervisor_token": "state-token",
                "pid": 12345,
                "started_at": now,
                "updated_at": now,
                "parser_runner_started": True,
                "tailing_started": True,
                "sqlite_live_writes_enabled": False,
                "last_result": {
                    "status": "ok",
                    "raw_path": unsafe_path,
                    "row_counts": {"match_rows": 1},
                    "warnings": ["sqlite_write_failed", unsafe_url],
                },
                "warnings": ["waiting_for_events", unsafe_path],
                "errors": ["sqlite_write_failed", unsafe_url],
            },
        ),
        encoding="utf-8",
    )
    client = _client(app_root)

    status_payload = client.get("/api/live/capture/status").json()
    start_payload = client.post("/api/live/capture/start").json()
    stop_payload = client.post("/api/live/capture/stop").json()
    encoded = json.dumps(
        {"status": status_payload, "start": start_payload, "stop": stop_payload},
        sort_keys=True,
    )

    assert status_payload["status"] == "failed"
    assert start_payload["accepted"] is False
    assert stop_payload["accepted"] is False
    assert "waiting_for_events" in status_payload["warnings"]
    assert "unsafe_state_warning_redacted" in status_payload["warnings"]
    assert "sqlite_write_failed" in status_payload["errors"]
    assert "unsafe_state_error_redacted" in status_payload["errors"]
    assert "raw_path" not in status_payload["last_result"]
    assert unsafe_path not in encoded
    assert unsafe_url not in encoded


def test_capture_status_sanitizes_heartbeat_progress_and_blurb_boundaries(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    player_log_path = tmp_path / "Player.log"
    _configure_player_log(app_root, player_log_path)
    unsafe_path = r"C:\operator\AppData\Local\MythicEdge\Player.log"
    unsafe_url = "https://example.invalid/private/path"
    now = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    state_file = app_root / "jobs" / LIVE_CAPTURE_STATE_FILENAME
    state_file.parent.mkdir(parents=True)
    state_file.write_text(
        json.dumps(
            {
                "status": "failed",
                "supervisor_token": "state-token",
                "pid": 12345,
                "started_at": now,
                "updated_at": now,
                "parser_runner_started": True,
                "tailing_started": True,
                "sqlite_live_writes_enabled": False,
                "heartbeat": {
                    "schema_version": LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION,
                    "status": "waiting",
                    "heartbeat_updated_at": unsafe_path,
                    "capture_duration_seconds": -12,
                    "heartbeat_age_seconds": -1,
                    "stale_after_seconds": 30,
                },
                "progress": {
                    "schema_version": LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION,
                    "log_poll_count": 2,
                    "log_chunks_seen": -1,
                    "structured_entry_count": 1,
                    "parser_event_count": 1,
                    "parser_event_kinds_seen": ["game_state", unsafe_path, "GameStateEvent"],
                    "match_ids_seen_count": 1,
                    "current_match_detected": True,
                    "current_match_game_wins": None,
                    "current_match_game_losses": None,
                    "last_completed_match_result": unsafe_url,
                    "last_completed_match_game_wins": None,
                    "last_completed_match_game_losses": None,
                    "completed_game_rows_seen": 0,
                    "sqlite_write_attempt_count": 1,
                    "sqlite_rows_written": 0,
                    "last_no_write_reason": "sqlite_write_failed",
                    "last_event_seen_at": unsafe_path,
                    "last_sqlite_write_at": unsafe_url,
                },
                "warnings": ["waiting_for_events", unsafe_path],
                "errors": ["sqlite_write_failed", unsafe_url],
            },
        ),
        encoding="utf-8",
    )
    client = _client(app_root)

    payload = client.get("/api/live/capture/status").json()
    encoded = json.dumps(payload, sort_keys=True)

    assert payload["status"] == "failed"
    assert payload["heartbeat"]["schema_version"] == LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION
    assert payload["heartbeat"]["heartbeat_updated_at"] == now
    assert payload["heartbeat"]["heartbeat_age_seconds"] is not None
    assert payload["progress"]["schema_version"] == LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION
    assert payload["progress"]["log_chunks_seen"] == 0
    assert payload["progress"]["parser_event_kinds_seen"] == ["game_state"]
    assert payload["progress"]["last_completed_match_result"] is None
    assert payload["progress"]["last_event_seen_at"] is None
    assert payload["progress"]["last_sqlite_write_at"] is None
    assert payload["progress"]["last_no_write_reason"] == "sqlite_write_failed"
    assert payload["parser_status_blurb"] == {
        "code": "sqlite_write_failed",
        "text": "SQLite write failed. Review diagnostics.",
        "tone": "error",
    }
    assert unsafe_path not in encoded
    assert unsafe_url not in encoded


def test_capture_status_redacts_unsafe_state_timestamp_fields(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    player_log_path = tmp_path / "Player.log"
    _configure_player_log(app_root, player_log_path)
    unsafe_started_at = r"C:\operator\AppData\Local\MythicEdge\live_capture_state.json"
    unsafe_updated_at = "https://example.invalid/local/live_capture_state.json"
    state_file = app_root / "jobs" / LIVE_CAPTURE_STATE_FILENAME
    state_file.parent.mkdir(parents=True)
    state_file.write_text(
        json.dumps(
            {
                "status": "capturing",
                "supervisor_token": "state-token",
                "pid": 12345,
                "started_at": unsafe_started_at,
                "updated_at": unsafe_updated_at,
                "parser_runner_started": True,
                "tailing_started": True,
                "sqlite_live_writes_enabled": True,
                "warnings": ["waiting_for_events"],
                "errors": [],
            },
        ),
        encoding="utf-8",
    )
    client = _client(app_root)

    payload = client.get("/api/live/capture/status").json()
    encoded = json.dumps(payload, sort_keys=True)

    assert payload["status"] == "stale"
    assert payload["state"]["started_at"] is None
    assert payload["state"]["updated_at"] is None
    assert unsafe_started_at not in encoded
    assert unsafe_updated_at not in encoded


def test_start_capture_is_explicit_local_only_and_duplicate_safe(tmp_path, monkeypatch) -> None:
    app_root = tmp_path / "app-data"
    player_log_path = tmp_path / "Player.log"
    _configure_player_log(app_root, player_log_path)
    monkeypatch.setattr(live_capture_control, "_build_supervisor", _fake_supervisor_factory)
    client = _client(app_root)

    start_response = client.post("/api/live/capture/start")
    start_payload = start_response.json()
    duplicate_payload = client.post("/api/live/capture/start").json()
    status_payload = client.get("/api/live/capture/status").json()
    encoded = json.dumps(
        {"start": start_payload, "duplicate": duplicate_payload, "status": status_payload},
        sort_keys=True,
    )

    assert start_response.status_code == 200
    assert start_payload["object"] == "mythic_edge_local_app_live_capture_start_result"
    assert start_payload["schema_version"] == LIVE_CAPTURE_SCHEMA_VERSION
    assert start_payload["accepted"] is True
    assert start_payload["status"] == "capturing"
    assert duplicate_payload["accepted"] is False
    assert duplicate_payload["status"] == "already_running"
    assert status_payload["status"] == "capturing"
    assert status_payload["capture"]["running"] is True
    assert status_payload["capture"]["stop_allowed"] is True
    assert status_payload["capture"]["parser_runner_started"] is True
    assert status_payload["capture"]["tailing_started"] is True
    assert status_payload["capture"]["sqlite_live_writes_enabled"] is True
    assert status_payload["capture"]["external_transport_allowed"] is False
    assert status_payload["heartbeat"]["schema_version"] == LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION
    assert status_payload["heartbeat"]["status"] == "waiting"
    assert status_payload["heartbeat"]["heartbeat_age_seconds"] is not None
    assert status_payload["heartbeat"]["heartbeat_age_seconds"] <= 30
    assert status_payload["progress"]["schema_version"] == LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION
    assert status_payload["progress"]["last_no_write_reason"] == "no_parser_events_routed"
    assert status_payload["parser_status_blurb"] == {
        "code": "listening_for_events",
        "text": "Listening for Player.log events.",
        "tone": "waiting",
    }
    assert (app_root / "jobs" / "live_capture_state.json").is_file()
    assert (app_root / "jobs" / "live_capture_lock.json").is_file()
    assert (app_root / "db" / "mythic_edge.sqlite3").is_file()
    assert str(player_log_path) not in encoded
    assert "private log body" not in encoded


def test_capture_status_marks_stale_heartbeat_without_changing_capture_ownership(tmp_path, monkeypatch) -> None:
    app_root = tmp_path / "app-data"
    player_log_path = tmp_path / "Player.log"
    _configure_player_log(app_root, player_log_path)
    monkeypatch.setattr(live_capture_control, "_build_supervisor", _fake_supervisor_factory)
    client = _client(app_root)

    client.post("/api/live/capture/start")
    state_file = app_root / "jobs" / LIVE_CAPTURE_STATE_FILENAME
    payload = json.loads(state_file.read_text(encoding="utf-8"))
    stale_heartbeat = (datetime.now(UTC) - timedelta(seconds=45)).isoformat().replace("+00:00", "Z")
    payload["updated_at"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    payload["heartbeat"]["heartbeat_updated_at"] = stale_heartbeat
    state_file.write_text(json.dumps(payload), encoding="utf-8")

    status_payload = client.get("/api/live/capture/status").json()

    assert status_payload["status"] == "capturing"
    assert status_payload["heartbeat"]["status"] == "stale"
    assert status_payload["heartbeat"]["heartbeat_age_seconds"] >= 30
    assert status_payload["progress"]["last_no_write_reason"] == "no_parser_events_routed"


def test_failed_live_ingest_counts_one_sqlite_write_attempt_without_leaking_error_text(tmp_path, monkeypatch) -> None:
    app_root = tmp_path / "app-data"
    player_log_path = tmp_path / "Player.log"
    _configure_player_log(app_root, player_log_path)
    paths = build_local_app_paths(app_root)
    event = object()
    fake_stream = _FakeStream()
    unsafe_error = r"C:\operator\AppData\Local\MythicEdge\mythic_edge.sqlite3"

    async def _fake_stream_start(_player_log_path: Path):
        return fake_stream, _FakeSubscriber(event)

    def _failing_write_live_facts(_paths, _payload):
        raise sqlite3.DatabaseError(unsafe_error)

    monkeypatch.setattr(live_capture_control.MtgaEventStream, "start", _fake_stream_start)
    monkeypatch.setattr(live_capture_control, "_update_match_summary", lambda _event: None)
    monkeypatch.setattr(
        live_capture_control,
        "get_context_snapshot",
        lambda: {"current_match_id": "match:ingest-fail"},
    )
    monkeypatch.setattr(
        live_capture_control,
        "build_match_log_row",
        lambda _match_id: {"Match Result": "W"},
    )
    monkeypatch.setattr(
        live_capture_control,
        "build_game_summary_rows",
        lambda _match_id: [{"Game Result": "Win"}],
    )
    monkeypatch.setattr(live_capture_control, "_write_live_facts", _failing_write_live_facts)

    supervisor = live_capture_control.LocalAppLiveCaptureSupervisor(paths, ownership_id="test-owner")
    asyncio.run(supervisor._run_async())

    payload = _client(app_root).get("/api/live/capture/status").json()
    encoded = json.dumps(payload, sort_keys=True)

    assert fake_stream.shutdown_called is True
    assert payload["status"] == "failed"
    assert payload["progress"]["sqlite_write_attempt_count"] == 1
    assert payload["progress"]["sqlite_rows_written"] == 0
    assert payload["progress"]["last_no_write_reason"] == "sqlite_write_failed"
    assert payload["parser_status_blurb"] == {
        "code": "sqlite_write_failed",
        "text": "SQLite write failed. Review diagnostics.",
        "tone": "error",
    }
    assert payload["errors"] == ["sqlite_write_failed"]
    assert unsafe_error not in encoded
    assert "DatabaseError" not in encoded
    assert "SELECT" not in encoded.upper()


def test_stop_capture_stops_only_registered_app_owned_supervisor(tmp_path, monkeypatch) -> None:
    app_root = tmp_path / "app-data"
    player_log_path = tmp_path / "Player.log"
    _configure_player_log(app_root, player_log_path)
    monkeypatch.setattr(live_capture_control, "_build_supervisor", _fake_supervisor_factory)
    client = _client(app_root)

    client.post("/api/live/capture/start")
    stop_payload = client.post("/api/live/capture/stop").json()
    second_stop_payload = client.post("/api/live/capture/stop").json()

    assert stop_payload["object"] == "mythic_edge_local_app_live_capture_stop_result"
    assert stop_payload["accepted"] is True
    assert stop_payload["status"] == "stopped"
    assert stop_payload["capture_status"]["status"] == "stopped"
    assert stop_payload["capture_status"]["capture"]["running"] is False
    assert second_stop_payload["accepted"] is False
    assert second_stop_payload["status"] == "not_running"


def test_start_capture_blocks_missing_player_log_without_creating_state(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    missing_player_log = tmp_path / "missing" / "Player.log"
    config_file = app_root / "config" / "app_config.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text(json.dumps({"player_log_path": str(missing_player_log)}), encoding="utf-8")
    client = _client(app_root)

    payload = client.post("/api/live/capture/start").json()
    encoded = json.dumps(payload, sort_keys=True)

    assert payload["accepted"] is False
    assert payload["status"] == "blocked"
    assert "player_log_missing" in payload["errors"]
    assert not (app_root / "jobs" / "live_capture_state.json").exists()
    assert str(missing_player_log) not in encoded


def test_start_capture_requires_configured_player_log_not_detected_default(tmp_path, monkeypatch) -> None:
    app_root = tmp_path / "app-data"
    detected_default = tmp_path / "detected" / "Player.log"
    detected_default.parent.mkdir()
    detected_default.write_text("detected log body must never be returned", encoding="utf-8")
    monkeypatch.setattr(app_config, "DEFAULT_MTGA_PLAYER_LOG", detected_default)
    monkeypatch.setattr(setup_status, "DEFAULT_MTGA_PLAYER_LOG", detected_default)
    monkeypatch.setattr(live_capture_control, "_build_supervisor", _fake_supervisor_factory)
    client = _client(app_root)

    monitor_payload = client.get("/api/live/player-log/status").json()
    status_payload = client.get("/api/live/capture/status").json()
    start_payload = client.post("/api/live/capture/start").json()
    encoded = json.dumps(
        {"monitor": monitor_payload, "status": status_payload, "start": start_payload},
        sort_keys=True,
    )

    assert monitor_payload["player_log"]["status"] == "detected_exists"
    assert status_payload["status"] == "blocked"
    assert status_payload["capture"]["start_allowed"] is False
    assert "player_log_not_configured" in status_payload["errors"]
    assert start_payload["accepted"] is False
    assert start_payload["status"] == "blocked"
    assert "player_log_not_configured" in start_payload["errors"]
    assert not (app_root / "jobs" / LIVE_CAPTURE_STATE_FILENAME).exists()
    assert str(detected_default) not in encoded
    assert "detected log body" not in encoded


def test_stale_capture_state_blocks_start_and_stop_without_cleanup(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    player_log_path = tmp_path / "Player.log"
    _configure_player_log(app_root, player_log_path)
    stale_time = (datetime.now(UTC) - timedelta(hours=2)).isoformat().replace("+00:00", "Z")
    state_file = app_root / "jobs" / "live_capture_state.json"
    state_file.parent.mkdir(parents=True)
    state_file.write_text(
        json.dumps(
            {
                "status": "capturing",
                "supervisor_token": "stale-token",
                "pid": 12345,
                "started_at": stale_time,
                "updated_at": stale_time,
                "parser_runner_started": True,
                "tailing_started": True,
                "sqlite_live_writes_enabled": True,
                "warnings": [],
                "errors": [],
            },
        ),
        encoding="utf-8",
    )
    client = _client(app_root)

    status_payload = client.get("/api/live/capture/status").json()
    start_payload = client.post("/api/live/capture/start").json()
    stop_payload = client.post("/api/live/capture/stop").json()

    assert status_payload["status"] == "stale"
    assert start_payload["accepted"] is False
    assert start_payload["status"] == "blocked"
    assert "capture_state_stale" in start_payload["errors"]
    assert stop_payload["accepted"] is False
    assert stop_payload["status"] == "blocked"
    assert "supervisor_ownership_unverified" in stop_payload["errors"]
    assert state_file.is_file()


def test_capture_routes_do_not_add_destructive_controls(tmp_path) -> None:
    client = _client(tmp_path / "app-data")

    for route in (
        "/api/live/capture/restart",
        "/api/live/capture/reset",
        "/api/live/capture/kill",
        "/api/live/capture/delete",
        "/api/live/capture/cleanup",
    ):
        assert client.post(route).status_code == 404
