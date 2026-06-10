from __future__ import annotations

import asyncio
import json
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

from fastapi.testclient import TestClient

from mythic_edge_parser.local_app import live_capture_control, live_watcher_process
from mythic_edge_parser.local_app.backend import create_app
from mythic_edge_parser.local_app.live_capture_control import LIVE_CAPTURE_STATE_FILENAME
from mythic_edge_parser.local_app.mtga_process_lifecycle import (
    MTGA_PROCESS_SCHEMA_VERSION,
    build_mtga_process_status,
)
from mythic_edge_parser.local_app.paths import build_local_app_paths


def _iso(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _mtga_status(status: str, *, checked_at: str = "2026-06-10T12:00:00Z") -> dict[str, object]:
    detected = status == "detected"
    evidence = "image_name_match" if detected else "image_name_absent"
    warnings = [] if detected else ["mtga_not_detected"]
    errors: list[str] = []
    if status == "detector_unavailable":
        evidence = "detector_error"
        warnings = []
        errors = ["mtga_detector_unavailable"]
    if status == "unsupported_platform":
        evidence = "not_checked"
        warnings = ["mtga_process_detection_unsupported"]
    return {
        "object": "mythic_edge_local_app_mtga_process_status",
        "schema_version": MTGA_PROCESS_SCHEMA_VERSION,
        "status": status,
        "detected": detected,
        "platform": "windows" if status != "unsupported_platform" else "non_windows",
        "process_name": "MTGA.exe",
        "evidence": evidence,
        "checked_at": checked_at,
        "detector": "windows_tasklist_image_name",
        "warnings": warnings,
        "errors": errors,
        "privacy": {
            "pid_exposed": False,
            "command_line_exposed": False,
            "environment_exposed": False,
            "raw_detector_output_exposed": False,
        },
    }


def _configure_player_log(app_root: Path, player_log_path: Path) -> None:
    player_log_path.write_text("synthetic log body must never be returned", encoding="utf-8")
    config_file = app_root / "config" / "app_config.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text(json.dumps({"player_log_path": str(player_log_path)}), encoding="utf-8")


def _seed_capturing_state(app_root: Path, *, started_at: str = "2026-06-10T12:00:00Z") -> None:
    paths = build_local_app_paths(app_root)
    live_capture_control._write_capture_state(
        paths,
        {
            "status": "capturing",
            "supervisor_token": "synthetic-owner",
            "started_at": started_at,
            "updated_at": started_at,
            "parser_runner_started": True,
            "tailing_started": True,
            "sqlite_live_writes_enabled": True,
            "last_result": {"status": "ok", "row_counts": {"matches": 1, "games": 2}},
            "heartbeat": live_capture_control._heartbeat_state(
                "waiting",
                started_at=started_at,
                heartbeat_updated_at=started_at,
            ),
            "progress": live_capture_control._default_progress("rows_written"),
            "warnings": ["waiting_for_events"],
            "errors": [],
        },
    )


def test_windows_mtga_process_detector_uses_fixed_tasklist_vector_without_raw_output() -> None:
    captured: dict[str, object] = {}

    def _runner(command, **kwargs):
        captured["command"] = command
        captured["shell"] = kwargs.get("shell")
        captured["timeout"] = kwargs.get("timeout")
        return subprocess.CompletedProcess(command, 0, stdout="MTGA.exe 123 Console 1 256 K", stderr="secret stderr")

    payload = build_mtga_process_status(runner=_runner, platform_system=lambda: "Windows")
    encoded = json.dumps(payload, sort_keys=True)

    assert captured["command"] == ["tasklist", "/FI", "IMAGENAME eq MTGA.exe", "/NH"]
    assert captured["shell"] is False
    assert captured["timeout"] == 2
    assert payload["status"] == "detected"
    assert payload["detected"] is True
    assert payload["privacy"] == {
        "pid_exposed": False,
        "command_line_exposed": False,
        "environment_exposed": False,
        "raw_detector_output_exposed": False,
    }
    assert "123" not in encoded
    assert "secret stderr" not in encoded


def test_windows_mtga_process_detector_reports_not_detected_unavailable_and_unsupported_safely() -> None:
    not_detected = build_mtga_process_status(
        runner=lambda command, **kwargs: subprocess.CompletedProcess(command, 0, stdout="INFO: No tasks are running"),
        platform_system=lambda: "Windows",
    )
    unavailable = build_mtga_process_status(
        runner=lambda command, **kwargs: (_ for _ in ()).throw(FileNotFoundError("tasklist missing")),
        platform_system=lambda: "Windows",
    )
    unsupported = build_mtga_process_status(platform_system=lambda: "Linux")

    assert not_detected["status"] == "not_detected"
    assert not_detected["detected"] is False
    assert unavailable["status"] == "detector_unavailable"
    assert unavailable["errors"] == ["mtga_detector_unavailable"]
    assert unsupported["status"] == "unsupported_platform"
    assert unsupported["evidence"] == "not_checked"


def test_watcher_process_and_diagnostics_include_sanitized_mtga_process_status(tmp_path, monkeypatch) -> None:
    app_root = tmp_path / "app-data"
    _configure_player_log(app_root, tmp_path / "Player.log")
    monkeypatch.setattr(live_watcher_process, "build_mtga_process_status", lambda: _mtga_status("not_detected"))
    client = TestClient(create_app(app_data_root=app_root))

    process_payload = client.get("/api/live/watcher/process").json()
    diagnostics_payload = client.get("/api/live/watcher/diagnostics").json()
    encoded = json.dumps({"process": process_payload, "diagnostics": diagnostics_payload}, sort_keys=True)
    diagnostic_keys = {entry["key"] for entry in diagnostics_payload["diagnostics"]}

    assert process_payload["mtga_process"]["status"] == "not_detected"
    assert process_payload["mtga_process"]["privacy"]["pid_exposed"] is False
    assert process_payload["automation_readiness"]["automatic_start_allowed"] is False
    assert "mtga_process_not_detected" in diagnostic_keys
    assert "automatic_start_blocked" in diagnostic_keys
    assert "raw_stdout" not in encoded
    assert "pid" not in json.dumps(process_payload["mtga_process"], sort_keys=True).replace("pid_exposed", "")


def test_capture_status_adds_mtga_lifecycle_without_mutating_get_state(tmp_path, monkeypatch) -> None:
    app_root = tmp_path / "app-data"
    _configure_player_log(app_root, tmp_path / "Player.log")
    monkeypatch.setattr(live_capture_control, "build_mtga_process_status", lambda: _mtga_status("not_detected"))
    client = TestClient(create_app(app_data_root=app_root))

    payload = client.get("/api/live/capture/status").json()
    encoded = json.dumps(payload, sort_keys=True)

    assert payload["status"] == "ready_to_start"
    assert payload["mtga_lifecycle"]["status"] == "mtga_unavailable"
    assert payload["mtga_lifecycle"]["automation_start_allowed"] is False
    assert payload["mtga_lifecycle"]["automation_readiness"]["automatic_start_allowed"] is False
    assert not (app_root / "jobs").exists()
    assert "synthetic log body" not in encoded


def test_mtga_disappearance_enters_reconnect_and_reconnect_continues_capture(tmp_path, monkeypatch) -> None:
    app_root = tmp_path / "app-data"
    _seed_capturing_state(app_root)
    paths = build_local_app_paths(app_root)
    now = datetime(2026, 6, 10, 12, 0, 0, tzinfo=UTC)
    statuses = [
        _mtga_status("not_detected", checked_at=_iso(now)),
        _mtga_status("detected", checked_at=_iso(now + timedelta(seconds=10))),
    ]

    def _detector(*, checked_at=None):
        return statuses.pop(0)

    monkeypatch.setattr(live_capture_control, "build_mtga_process_status", _detector)
    supervisor = live_capture_control.LocalAppLiveCaptureSupervisor(paths, ownership_id="synthetic-owner")
    progress = live_capture_control._default_progress("no_parser_events_routed")

    assert supervisor._tick_mtga_lifecycle(progress, now=now) is False
    reconnect_state = json.loads((app_root / "jobs" / LIVE_CAPTURE_STATE_FILENAME).read_text(encoding="utf-8"))
    assert reconnect_state["status"] == "capturing"
    assert reconnect_state["mtga_lifecycle"]["status"] == "reconnect_window"
    assert reconnect_state["mtga_lifecycle"]["shutdown_reason"] is None
    assert supervisor._stop_event.is_set() is False

    assert supervisor._tick_mtga_lifecycle(progress, now=now + timedelta(seconds=10)) is False
    reconnected_state = json.loads((app_root / "jobs" / LIVE_CAPTURE_STATE_FILENAME).read_text(encoding="utf-8"))
    assert reconnected_state["status"] == "capturing"
    assert reconnected_state["mtga_lifecycle"]["status"] == "capturing"
    assert "mtga_reconnected" in reconnected_state["mtga_lifecycle"]["warnings"]
    assert supervisor._stop_event.is_set() is False


def test_mtga_absence_after_reconnect_window_stops_app_owned_capture_without_erasing_completed_rows(
    tmp_path,
    monkeypatch,
) -> None:
    app_root = tmp_path / "app-data"
    _seed_capturing_state(app_root)
    paths = build_local_app_paths(app_root)
    now = datetime(2026, 6, 10, 12, 1, 0, tzinfo=UTC)
    previous_started = _iso(now - timedelta(seconds=46))
    state_path = app_root / "jobs" / LIVE_CAPTURE_STATE_FILENAME
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["mtga_lifecycle"] = {
        "schema_version": MTGA_PROCESS_SCHEMA_VERSION,
        "status": "reconnect_window",
        "mtga_process_status": "not_detected",
        "reconnect_window_seconds": 45,
        "reconnect_started_at": previous_started,
        "reconnect_deadline_at": _iso(now - timedelta(seconds=1)),
        "seconds_remaining": 0,
        "shutdown_reason": None,
        "last_detected_at": _iso(now - timedelta(seconds=60)),
        "last_checked_at": previous_started,
        "warnings": ["mtga_reconnect_window_active"],
        "errors": [],
    }
    state_path.write_text(json.dumps(state), encoding="utf-8")
    monkeypatch.setattr(
        live_capture_control,
        "build_mtga_process_status",
        lambda *, checked_at=None: _mtga_status("not_detected", checked_at=_iso(now)),
    )
    supervisor = live_capture_control.LocalAppLiveCaptureSupervisor(paths, ownership_id="synthetic-owner")
    progress = live_capture_control._default_progress("rows_written")

    assert supervisor._tick_mtga_lifecycle(progress, now=now) is True
    payload = json.loads(state_path.read_text(encoding="utf-8"))

    assert payload["status"] == "stopping"
    assert payload["last_result"]["row_counts"] == {"matches": 1, "games": 2}
    assert payload["mtga_lifecycle"]["status"] == "shutting_down"
    assert payload["mtga_lifecycle"]["shutdown_reason"] == "mtga_unavailable_timeout"
    assert "capture_shutdown_started" in payload["mtga_lifecycle"]["warnings"]
    assert supervisor._stop_event.is_set() is True


class _FakeStream:
    def __init__(self) -> None:
        self.shutdown_called = False

    async def shutdown(self) -> None:
        self.shutdown_called = True


class _TimeoutSubscriber:
    async def recv(self) -> None:
        await asyncio.sleep(10)


def test_mtga_timeout_shutdown_returns_stopped_state_through_supervisor_loop(tmp_path, monkeypatch) -> None:
    app_root = tmp_path / "app-data"
    _configure_player_log(app_root, tmp_path / "Player.log")
    paths = build_local_app_paths(app_root)
    fake_stream = _FakeStream()

    async def _fake_stream_start(_player_log_path: Path):
        return fake_stream, _TimeoutSubscriber()

    monkeypatch.setattr(live_capture_control.MtgaEventStream, "start", _fake_stream_start)
    monkeypatch.setattr(
        live_capture_control,
        "build_mtga_process_status",
        lambda *, checked_at=None: _mtga_status("not_detected"),
    )
    monkeypatch.setattr(live_capture_control, "MTGA_RECONNECT_WINDOW_SECONDS", 0)
    monkeypatch.setattr(live_capture_control, "MTGA_PROCESS_SUPERVISOR_CHECK_SECONDS", 0)

    supervisor = live_capture_control.LocalAppLiveCaptureSupervisor(paths, ownership_id="synthetic-owner")
    asyncio.run(supervisor._run_async())
    payload = json.loads((app_root / "jobs" / LIVE_CAPTURE_STATE_FILENAME).read_text(encoding="utf-8"))

    assert fake_stream.shutdown_called is True
    assert payload["status"] == "stopped"
    assert payload["parser_runner_started"] is False
    assert payload["tailing_started"] is False
    assert payload["sqlite_live_writes_enabled"] is False
    assert payload["mtga_lifecycle"]["status"] == "stopped"
    assert payload["mtga_lifecycle"]["shutdown_reason"] == "mtga_unavailable_timeout"
    assert "capture_shutdown_completed" in payload["mtga_lifecycle"]["warnings"]
