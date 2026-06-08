from __future__ import annotations

import asyncio
import json
import os
import secrets
import sqlite3
import threading
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

from mythic_edge_parser.app.analytics_ingest import (
    AnalyticsReplayIngestError,
    ingest_live_parser_owned_facts,
)
from mythic_edge_parser.app.analytics_migration_loader import apply_analytics_migrations
from mythic_edge_parser.app.state import (
    _update_match_summary,
    build_game_summary_rows,
    build_match_log_row,
    get_context_snapshot,
    reset_runtime_state,
)
from mythic_edge_parser.stream import MtgaEventStream, StreamError

from .paths import LocalAppPaths, display_app_path
from .setup_status import build_analytics_database_status, build_live_player_log_status

LIVE_CAPTURE_STATUS_OBJECT = "mythic_edge_local_app_live_capture_status"
LIVE_CAPTURE_START_RESULT_OBJECT = "mythic_edge_local_app_live_capture_start_result"
LIVE_CAPTURE_STOP_RESULT_OBJECT = "mythic_edge_local_app_live_capture_stop_result"
LIVE_CAPTURE_SCHEMA_VERSION = "live_app_explicit_start_capture_control.v1"
LIVE_CAPTURE_STATE_FILENAME = "live_capture_state.json"
LIVE_CAPTURE_LOCK_FILENAME = "live_capture_lock.json"
LIVE_CAPTURE_STATE_STALE_SECONDS = 15 * 60
LIVE_CAPTURE_SOURCE_KIND = "live_parser"
LIVE_CAPTURE_SUPERVISOR_KIND = "local_app_capture_supervisor"
_SAFE_STATE_LABEL_MAX_LENGTH = 80
_SAFE_STATE_LABEL_CHARS = frozenset("abcdefghijklmnopqrstuvwxyz0123456789_")

_REGISTRY_LOCK = threading.RLock()
_SUPERVISORS: dict[str, "_LiveCaptureSupervisorProtocol"] = {}


class _LiveCaptureSupervisorProtocol(Protocol):
    ownership_id: str

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...

    def is_running(self) -> bool:
        ...


@dataclass(frozen=True, slots=True)
class _PlayerLogReady:
    status: str
    reason: str | None
    safe_label: str


def build_live_capture_status(paths: LocalAppPaths) -> dict[str, object]:
    state = _read_capture_state(paths)
    supervisor = _registered_supervisor(paths)
    player_log_ready = _player_log_ready(paths)
    preconditions = _build_preconditions(paths, player_log_ready, write_check=False)
    status, reason = _status_from_state(
        state=state,
        supervisor=supervisor,
        player_log_ready=player_log_ready,
        preconditions=preconditions,
    )
    capture = _capture_summary(status=status, state=state, supervisor=supervisor, reason=reason)
    return _status_payload(
        status=status,
        capture=capture,
        preconditions=preconditions,
        state=state,
        last_result=_safe_last_result(state.get("last_result")),
        warnings=_warnings_for_status(status, state),
        errors=_errors_for_status(status, reason, state),
    )


def start_live_capture(paths: LocalAppPaths) -> dict[str, object]:
    with _REGISTRY_LOCK:
        existing = _registered_supervisor_unlocked(paths)
        if existing is not None and existing.is_running():
            capture_status = build_live_capture_status(paths)
            return _start_result("already_running", accepted=False, capture_status=capture_status)

        player_log_ready = _player_log_ready(paths)
        preconditions = _build_preconditions(paths, player_log_ready, write_check=True)
        blocking_reason = _first_blocking_precondition(preconditions)
        state = _read_capture_state(paths)
        state_blocker = _state_start_blocker(state)
        if blocking_reason is not None or state_blocker is not None:
            reason = blocking_reason or state_blocker or "start_blocked"
            capture_status = _blocked_status_payload(paths, reason)
            return _start_result("blocked", accepted=False, capture_status=capture_status, errors=[reason])

        supervisor_id = secrets.token_urlsafe(18)
        _ensure_control_dirs(paths)
        if not _ensure_database_ready(paths):
            capture_status = _blocked_status_payload(paths, "analytics_database_unavailable")
            return _start_result(
                "blocked",
                accepted=False,
                capture_status=capture_status,
                errors=["analytics_database_unavailable"],
            )
        supervisor = _build_supervisor(paths, ownership_id=supervisor_id)
        _SUPERVISORS[_registry_key(paths)] = supervisor
        _write_capture_state(
            paths,
            {
                "status": "starting",
                "supervisor_token": supervisor_id,
                "pid": os.getpid(),
                "supervisor_kind": LIVE_CAPTURE_SUPERVISOR_KIND,
                "source_kind": LIVE_CAPTURE_SOURCE_KIND,
                "started_at": _now_iso(),
                "updated_at": _now_iso(),
                "parser_runner_started": True,
                "tailing_started": False,
                "sqlite_live_writes_enabled": False,
                "external_transport_allowed": False,
                "raw_player_log_storage_enabled": False,
                "last_result": None,
                "warnings": [],
                "errors": [],
            },
        )
        try:
            supervisor.start()
        except Exception:
            _SUPERVISORS.pop(_registry_key(paths), None)
            _write_capture_state(
                paths,
                {
                    "status": "failed",
                    "supervisor_token": supervisor_id,
                    "pid": os.getpid(),
                    "supervisor_kind": LIVE_CAPTURE_SUPERVISOR_KIND,
                    "source_kind": LIVE_CAPTURE_SOURCE_KIND,
                    "started_at": _now_iso(),
                    "updated_at": _now_iso(),
                    "parser_runner_started": False,
                    "tailing_started": False,
                    "sqlite_live_writes_enabled": False,
                    "external_transport_allowed": False,
                    "raw_player_log_storage_enabled": False,
                    "last_result": None,
                    "warnings": [],
                    "errors": ["supervisor_start_failed"],
                },
            )
            capture_status = build_live_capture_status(paths)
            return _start_result(
                "failed",
                accepted=False,
                capture_status=capture_status,
                errors=["supervisor_start_failed"],
            )

    capture_status = build_live_capture_status(paths)
    status = "capturing" if str(capture_status.get("status")) == "capturing" else "starting"
    return _start_result(status, accepted=True, capture_status=capture_status)


def stop_live_capture(paths: LocalAppPaths) -> dict[str, object]:
    with _REGISTRY_LOCK:
        supervisor = _registered_supervisor_unlocked(paths)
        state = _read_capture_state(paths)
        if supervisor is None:
            state_status = str(state.get("status", "not_initialized"))
            if state_status in {"not_initialized", "stopped"}:
                capture_status = build_live_capture_status(paths)
                return _stop_result("not_running", accepted=False, capture_status=capture_status)
            capture_status = _blocked_status_payload(paths, "supervisor_ownership_unverified")
            return _stop_result(
                "blocked",
                accepted=False,
                capture_status=capture_status,
                errors=["supervisor_ownership_unverified"],
            )

        state_token = str(state.get("supervisor_token", "") or "")
        if state_token != supervisor.ownership_id:
            capture_status = _blocked_status_payload(paths, "supervisor_ownership_unverified")
            return _stop_result(
                "blocked",
                accepted=False,
                capture_status=capture_status,
                errors=["supervisor_ownership_unverified"],
            )

        _write_capture_state(paths, {**state, "status": "stopping", "updated_at": _now_iso()})
        try:
            supervisor.stop()
        except Exception:
            capture_status = _blocked_status_payload(paths, "supervisor_stop_failed")
            return _stop_result(
                "failed",
                accepted=False,
                capture_status=capture_status,
                errors=["supervisor_stop_failed"],
            )
        _SUPERVISORS.pop(_registry_key(paths), None)
        _write_capture_state(
            paths,
            {
                **state,
                "status": "stopped",
                "updated_at": _now_iso(),
                "parser_runner_started": False,
                "tailing_started": False,
                "sqlite_live_writes_enabled": False,
                "last_result": _safe_last_result(state.get("last_result")),
            },
        )

    capture_status = build_live_capture_status(paths)
    return _stop_result("stopped", accepted=True, capture_status=capture_status)


class LocalAppLiveCaptureSupervisor:
    def __init__(self, paths: LocalAppPaths, *, ownership_id: str) -> None:
        self.paths = paths
        self.ownership_id = ownership_id
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run_thread, name="mythic-edge-live-capture", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=2)

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def _run_thread(self) -> None:
        try:
            asyncio.run(self._run_async())
        except Exception:
            _write_capture_state(
                self.paths,
                {
                    **_read_capture_state(self.paths),
                    "status": "failed",
                    "updated_at": _now_iso(),
                    "parser_runner_started": False,
                    "tailing_started": False,
                    "sqlite_live_writes_enabled": False,
                    "errors": ["supervisor_crashed"],
                },
            )

    async def _run_async(self) -> None:
        player_log_path = _configured_player_log_path(self.paths)
        if player_log_path is None:
            _write_capture_state(
                self.paths,
                {
                    **_read_capture_state(self.paths),
                    "status": "blocked",
                    "updated_at": _now_iso(),
                    "errors": ["player_log_not_ready"],
                },
            )
            return

        reset_runtime_state()
        try:
            stream, subscriber = await MtgaEventStream.start(player_log_path)
        except StreamError:
            _write_capture_state(
                self.paths,
                {
                    **_read_capture_state(self.paths),
                    "status": "failed",
                    "updated_at": _now_iso(),
                    "parser_runner_started": False,
                    "tailing_started": False,
                    "sqlite_live_writes_enabled": False,
                    "errors": ["tailer_start_failed"],
                },
            )
            return

        _write_capture_state(
            self.paths,
            {
                **_read_capture_state(self.paths),
                "status": "capturing",
                "updated_at": _now_iso(),
                "parser_runner_started": True,
                "tailing_started": True,
                "sqlite_live_writes_enabled": True,
                "warnings": ["waiting_for_events"],
                "errors": [],
            },
        )
        written_matches: set[str] = set()
        try:
            while not self._stop_event.is_set():
                try:
                    event = await asyncio.wait_for(subscriber.recv(), timeout=0.25)
                except TimeoutError:
                    continue
                if event is None:
                    break
                _update_match_summary(event)
                match_id = str(get_context_snapshot().get("current_match_id", "") or "")
                if not match_id or match_id in written_matches:
                    continue
                match_row = build_match_log_row(match_id)
                game_rows = [
                    row
                    for row in build_game_summary_rows(match_id)
                    if str(row.get("Game Result", "") or "").strip()
                ]
                if match_row is None or not game_rows:
                    continue
                result = _write_live_facts(
                    self.paths,
                    {
                        "source_kind": LIVE_CAPTURE_SOURCE_KIND,
                        "source_artifact_label": "live_parser_session",
                        "session_id": f"live_capture_{self.ownership_id[:8]}",
                        "parser_version": LIVE_CAPTURE_SCHEMA_VERSION,
                        "capture_started_at": str(_read_capture_state(self.paths).get("started_at", "")),
                        "capture_finished_at": _now_iso(),
                        "match_log_rows": [match_row],
                        "game_log_rows": game_rows,
                    },
                )
                written_matches.add(match_id)
                _write_capture_state(
                    self.paths,
                    {
                        **_read_capture_state(self.paths),
                        "status": "capturing",
                        "updated_at": _now_iso(),
                        "sqlite_live_writes_enabled": True,
                        "last_result": {
                            "status": result.status,
                            "row_counts": result.row_counts,
                            "warnings": result.warnings,
                            "skipped": result.skipped,
                        },
                        "warnings": result.warnings,
                        "errors": [],
                    },
                )
        except (AnalyticsReplayIngestError, sqlite3.DatabaseError, OSError):
            _write_capture_state(
                self.paths,
                {
                    **_read_capture_state(self.paths),
                    "status": "failed",
                    "updated_at": _now_iso(),
                    "sqlite_live_writes_enabled": False,
                    "errors": ["sqlite_write_failed"],
                },
            )
        finally:
            await stream.shutdown()
            if self._stop_event.is_set():
                _write_capture_state(
                    self.paths,
                    {
                        **_read_capture_state(self.paths),
                        "status": "stopped",
                        "updated_at": _now_iso(),
                        "parser_runner_started": False,
                        "tailing_started": False,
                        "sqlite_live_writes_enabled": False,
                    },
                )


def _write_live_facts(paths: LocalAppPaths, payload: Mapping[str, object]):
    if paths.analytics_database is None:
        raise sqlite3.DatabaseError("analytics_database_unavailable")
    paths.analytics_database.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(paths.analytics_database)
    try:
        return ingest_live_parser_owned_facts(connection, payload)
    finally:
        connection.close()


def _ensure_database_ready(paths: LocalAppPaths) -> bool:
    if paths.analytics_database is None:
        return False
    try:
        paths.analytics_database.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(paths.analytics_database)
        try:
            apply_analytics_migrations(connection)
        finally:
            connection.close()
    except (OSError, sqlite3.DatabaseError):
        return False
    return True


def _build_supervisor(paths: LocalAppPaths, *, ownership_id: str) -> _LiveCaptureSupervisorProtocol:
    return LocalAppLiveCaptureSupervisor(paths, ownership_id=ownership_id)


def _status_payload(
    *,
    status: str,
    capture: dict[str, object],
    preconditions: list[dict[str, str | None]],
    state: dict[str, object],
    last_result: object,
    warnings: list[str],
    errors: list[str],
) -> dict[str, object]:
    return {
        "object": LIVE_CAPTURE_STATUS_OBJECT,
        "schema_version": LIVE_CAPTURE_SCHEMA_VERSION,
        "status": status,
        "mode": "explicit_operator_control",
        "capture": capture,
        "preconditions": preconditions,
        "state": _safe_state_summary(state),
        "last_result": last_result,
        "warnings": warnings,
        "errors": errors,
    }


def _start_result(
    status: str,
    *,
    accepted: bool,
    capture_status: Mapping[str, object],
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> dict[str, object]:
    return {
        "object": LIVE_CAPTURE_START_RESULT_OBJECT,
        "schema_version": LIVE_CAPTURE_SCHEMA_VERSION,
        "status": status,
        "accepted": accepted,
        "capture_status": dict(capture_status),
        "warnings": warnings or [],
        "errors": errors or [],
    }


def _stop_result(
    status: str,
    *,
    accepted: bool,
    capture_status: Mapping[str, object],
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> dict[str, object]:
    return {
        "object": LIVE_CAPTURE_STOP_RESULT_OBJECT,
        "schema_version": LIVE_CAPTURE_SCHEMA_VERSION,
        "status": status,
        "accepted": accepted,
        "capture_status": dict(capture_status),
        "warnings": warnings or [],
        "errors": errors or [],
    }


def _capture_summary(
    *,
    status: str,
    state: Mapping[str, object],
    supervisor: _LiveCaptureSupervisorProtocol | None,
    reason: str | None,
) -> dict[str, object]:
    running = status == "capturing" and supervisor is not None and supervisor.is_running()
    return {
        "running": running,
        "start_allowed": status in {"ready_to_start", "stopped"},
        "stop_allowed": running,
        "parser_runner_started": running,
        "tailing_started": running and bool(state.get("tailing_started")),
        "sqlite_live_writes_enabled": running and bool(state.get("sqlite_live_writes_enabled")),
        "external_transport_allowed": False,
        "raw_player_log_storage_enabled": False,
        "supervisor_kind": LIVE_CAPTURE_SUPERVISOR_KIND,
        "source_kind": LIVE_CAPTURE_SOURCE_KIND,
        "reason": reason,
    }


def _read_capture_state(paths: LocalAppPaths) -> dict[str, object]:
    display_path = display_app_path("jobs", LIVE_CAPTURE_STATE_FILENAME) if paths.jobs_dir is not None else None
    if paths.jobs_dir is None:
        return _default_state(status="unavailable", display_path=display_path, errors=["app_data_root_unavailable"])
    state_path = paths.jobs_dir / LIVE_CAPTURE_STATE_FILENAME
    if not state_path.exists():
        return _default_state(status="not_initialized", display_path=display_path)
    if not state_path.is_file():
        return _default_state(status="unknown", display_path=display_path, errors=["capture_state_not_file"])
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return _default_state(status="unknown", display_path=display_path, errors=["capture_state_malformed"])
    if not isinstance(payload, dict):
        return _default_state(status="unknown", display_path=display_path, errors=["capture_state_malformed"])
    status = str(payload.get("status", "unknown") or "unknown")
    stale = _state_is_stale(payload.get("updated_at")) if status in {"starting", "capturing", "stopping"} else False
    if stale:
        status = "stale"
    return {
        "source": "app_data_state_file",
        "exists": True,
        "status": status,
        "stale": stale,
        "pid_present": isinstance(payload.get("pid"), int) and not isinstance(payload.get("pid"), bool),
        "pid_verified": False,
        "supervisor_token_present": bool(str(payload.get("supervisor_token", "") or "").strip()),
        "supervisor_token": str(payload.get("supervisor_token", "") or ""),
        "display_path": display_path,
        "raw_path_exposed": False,
        "started_at": _safe_iso_or_none(payload.get("started_at")),
        "updated_at": _safe_iso_or_none(payload.get("updated_at")),
        "parser_runner_started": bool(payload.get("parser_runner_started", False)),
        "tailing_started": bool(payload.get("tailing_started", False)),
        "sqlite_live_writes_enabled": bool(payload.get("sqlite_live_writes_enabled", False)),
        "last_result": _safe_last_result(payload.get("last_result")),
        "warnings": _safe_warning_list(payload.get("warnings")),
        "errors": _safe_error_list(payload.get("errors")),
    }


def _default_state(
    *,
    status: str,
    display_path: str | None,
    errors: list[str] | None = None,
) -> dict[str, object]:
    return {
        "source": "none" if status == "not_initialized" else "unavailable",
        "exists": False,
        "status": status,
        "stale": False,
        "pid_present": False,
        "pid_verified": False,
        "supervisor_token_present": False,
        "supervisor_token": "",
        "display_path": display_path,
        "raw_path_exposed": False,
        "started_at": None,
        "updated_at": None,
        "parser_runner_started": False,
        "tailing_started": False,
        "sqlite_live_writes_enabled": False,
        "last_result": None,
        "warnings": [],
        "errors": errors or [],
    }


def _write_capture_state(paths: LocalAppPaths, payload: Mapping[str, object]) -> None:
    if paths.jobs_dir is None:
        return
    paths.jobs_dir.mkdir(parents=True, exist_ok=True)
    state_path = paths.jobs_dir / LIVE_CAPTURE_STATE_FILENAME
    lock_path = paths.jobs_dir / LIVE_CAPTURE_LOCK_FILENAME
    safe_payload = {
        "status": str(payload.get("status", "unknown") or "unknown"),
        "supervisor_token": str(payload.get("supervisor_token", "") or ""),
        "pid": payload.get("pid") if isinstance(payload.get("pid"), int) else os.getpid(),
        "supervisor_kind": LIVE_CAPTURE_SUPERVISOR_KIND,
        "source_kind": LIVE_CAPTURE_SOURCE_KIND,
        "started_at": _safe_iso_or_none(payload.get("started_at")),
        "updated_at": _safe_iso_or_none(payload.get("updated_at")) or _now_iso(),
        "parser_runner_started": bool(payload.get("parser_runner_started", False)),
        "tailing_started": bool(payload.get("tailing_started", False)),
        "sqlite_live_writes_enabled": bool(payload.get("sqlite_live_writes_enabled", False)),
        "external_transport_allowed": False,
        "raw_player_log_storage_enabled": False,
        "last_result": _safe_last_result(payload.get("last_result")),
        "warnings": _safe_warning_list(payload.get("warnings")),
        "errors": _safe_error_list(payload.get("errors")),
    }
    state_path.write_text(json.dumps(safe_payload, sort_keys=True, indent=2), encoding="utf-8")
    lock_path.write_text(
        json.dumps(
            {
                "supervisor_token_present": bool(safe_payload["supervisor_token"]),
                "pid_present": True,
                "updated_at": safe_payload["updated_at"],
            },
            sort_keys=True,
            indent=2,
        ),
        encoding="utf-8",
    )


def _safe_state_summary(state: Mapping[str, object]) -> dict[str, object]:
    return {
        "source": state.get("source", "unknown"),
        "exists": bool(state.get("exists", False)),
        "status": state.get("status", "unknown"),
        "stale": bool(state.get("stale", False)),
        "pid_present": bool(state.get("pid_present", False)),
        "pid_verified": False,
        "supervisor_token_present": bool(state.get("supervisor_token_present", False)),
        "display_path": state.get("display_path"),
        "raw_path_exposed": False,
        "started_at": state.get("started_at"),
        "updated_at": state.get("updated_at"),
    }


def _player_log_ready(paths: LocalAppPaths) -> _PlayerLogReady:
    payload = build_live_player_log_status(paths)
    player_log = payload.get("player_log")
    status = str(player_log.get("status", "unavailable") if isinstance(player_log, Mapping) else "unavailable")
    if status == "configured_exists":
        return _PlayerLogReady("pass", None, status)
    reason = _player_log_blocker(status)
    return _PlayerLogReady("fail", reason, status)


def _player_log_blocker(status: str) -> str:
    return {
        "configured_missing": "player_log_missing",
        "detected_exists": "player_log_not_configured",
        "detected_missing": "player_log_not_configured",
        "invalid_config": "player_log_config_invalid",
        "unreadable": "player_log_unreadable",
        "configured_not_file": "player_log_not_file",
        "not_file": "player_log_not_file",
        "unavailable": "player_log_unavailable",
    }.get(status, "player_log_not_ready")


def _build_preconditions(
    paths: LocalAppPaths,
    player_log_ready: _PlayerLogReady,
    *,
    write_check: bool,
) -> list[dict[str, str | None]]:
    database_status = build_analytics_database_status(paths)
    schema_status = "unavailable"
    database = database_status.get("database")
    if isinstance(database, Mapping):
        schema_status = str(database.get("schema_status", "unavailable"))
    database_ready = schema_status in {"schema_current", "missing", "schema_unknown"}
    return [
        _precondition("player_log_ready", player_log_ready.status, player_log_ready.reason),
        _precondition(
            "app_data_root_available",
            "pass" if paths.app_data_root is not None else "fail",
            None if paths.app_data_root is not None else "app_data_root_unavailable",
        ),
        _precondition(
            "state_directory_available",
            "pass" if paths.jobs_dir is not None and (paths.jobs_dir.is_dir() or write_check) else "deferred",
            (
                None
                if paths.jobs_dir is not None and (paths.jobs_dir.is_dir() or write_check)
                else "state_directory_create_requires_post"
            ),
        ),
        _precondition("single_instance_guard_available", "pass", None),
        _precondition("supervisor_target_defined", "pass", None),
        _precondition("external_transport_disabled", "pass", None),
        _precondition("live_sqlite_ingest_contract_present", "pass", None),
        _precondition(
            "analytics_database_available",
            "pass" if database_ready else "fail",
            None if database_ready else "analytics_database_unavailable",
        ),
        _precondition("frontend_controls_authorized", "pass", None),
    ]


def _precondition(key: str, status: str, reason: str | None) -> dict[str, str | None]:
    return {"key": key, "status": status, "reason": reason}


def _first_blocking_precondition(preconditions: list[dict[str, str | None]]) -> str | None:
    for entry in preconditions:
        if entry["status"] == "fail":
            return entry["reason"] or str(entry["key"])
    return None


def _status_from_state(
    *,
    state: Mapping[str, object],
    supervisor: _LiveCaptureSupervisorProtocol | None,
    player_log_ready: _PlayerLogReady,
    preconditions: list[dict[str, str | None]],
) -> tuple[str, str | None]:
    reason = _first_blocking_precondition(preconditions)
    if reason is not None:
        return "blocked", reason
    state_errors = _safe_error_list(state.get("errors"))
    if state_errors:
        return "failed", state_errors[0]
    state_status = str(state.get("status", "unknown"))
    if state_status == "stale":
        return "stale", "capture_state_stale"
    if supervisor is not None and supervisor.is_running():
        if bool(state.get("tailing_started")) and bool(state.get("sqlite_live_writes_enabled")):
            return "capturing", None
        return "starting", None
    if state_status in {"starting", "capturing", "stopping"} and supervisor is None:
        return "stale", "supervisor_ownership_unverified"
    if state_status == "stopped":
        return "stopped", None
    if player_log_ready.status == "pass":
        return "ready_to_start", None
    return "unknown", None


def _state_start_blocker(state: Mapping[str, object]) -> str | None:
    status = str(state.get("status", "unknown"))
    if status in {"stale", "starting", "capturing", "stopping"}:
        return "capture_state_stale" if status == "stale" else "supervisor_ownership_unverified"
    state_errors = _safe_error_list(state.get("errors"))
    if state_errors:
        return state_errors[0]
    return None


def _blocked_status_payload(paths: LocalAppPaths, reason: str) -> dict[str, object]:
    state = _read_capture_state(paths)
    player_log_ready = _player_log_ready(paths)
    preconditions = _build_preconditions(paths, player_log_ready, write_check=False)
    return _status_payload(
        status="blocked",
        capture=_capture_summary(status="blocked", state=state, supervisor=None, reason=reason),
        preconditions=preconditions,
        state=state,
        last_result=_safe_last_result(state.get("last_result")),
        warnings=_warnings_for_status("blocked", state),
        errors=[reason],
    )


def _warnings_for_status(status: str, state: Mapping[str, object]) -> list[str]:
    warnings = _safe_warning_list(state.get("warnings"))
    if status == "capturing" and not state.get("last_result") and "waiting_for_events" not in warnings:
        warnings.append("waiting_for_events")
    if status == "stale" and "capture_state_stale" not in warnings:
        warnings.append("capture_state_stale")
    return warnings


def _errors_for_status(status: str, reason: str | None, state: Mapping[str, object]) -> list[str]:
    errors = _safe_error_list(state.get("errors"))
    if status in {"blocked", "failed", "stale"} and reason and reason not in errors:
        errors.append(reason)
    return errors


def _ensure_control_dirs(paths: LocalAppPaths) -> None:
    if paths.jobs_dir is not None:
        paths.jobs_dir.mkdir(parents=True, exist_ok=True)
    if paths.diagnostics_dir is not None:
        paths.diagnostics_dir.mkdir(parents=True, exist_ok=True)
    if paths.db_dir is not None:
        paths.db_dir.mkdir(parents=True, exist_ok=True)


def _configured_player_log_path(paths: LocalAppPaths) -> Path | None:
    from .config import read_local_app_config

    config = read_local_app_config(paths)
    if isinstance(config.values.get("player_log_path"), str) and config.values["player_log_path"].strip():
        candidate = Path(config.values["player_log_path"])
    else:
        return None
    try:
        if candidate.is_file():
            return candidate
    except OSError:
        return None
    return None


def _registered_supervisor(paths: LocalAppPaths) -> _LiveCaptureSupervisorProtocol | None:
    with _REGISTRY_LOCK:
        return _registered_supervisor_unlocked(paths)


def _registered_supervisor_unlocked(paths: LocalAppPaths) -> _LiveCaptureSupervisorProtocol | None:
    supervisor = _SUPERVISORS.get(_registry_key(paths))
    if supervisor is not None and supervisor.is_running():
        return supervisor
    if supervisor is not None:
        _SUPERVISORS.pop(_registry_key(paths), None)
    return None


def _registry_key(paths: LocalAppPaths) -> str:
    if paths.app_data_root is None:
        return "<app_data_unavailable>"
    return str(paths.app_data_root.resolve(strict=False))


def _state_is_stale(value: object) -> bool:
    if not isinstance(value, str):
        return True
    try:
        updated_at = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return True
    if updated_at.tzinfo is None:
        updated_at = updated_at.replace(tzinfo=UTC)
    age_seconds = (datetime.now(UTC) - updated_at.astimezone(UTC)).total_seconds()
    return age_seconds < 0 or age_seconds > LIVE_CAPTURE_STATE_STALE_SECONDS


def _now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _safe_iso_or_none(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text:
        return None
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    return text


def _safe_warning_list(value: object) -> list[str]:
    return _safe_state_label_list(value, redacted_code="unsafe_state_warning_redacted")


def _safe_error_list(value: object) -> list[str]:
    return _safe_state_label_list(value, redacted_code="unsafe_state_error_redacted")


def _safe_state_label_list(value: object, *, redacted_code: str) -> list[str]:
    if not isinstance(value, list):
        return []
    labels: list[str] = []
    unsafe_seen = False
    for entry in value:
        label = _safe_state_label(entry)
        if label is None:
            if isinstance(entry, str):
                unsafe_seen = True
            continue
        if label not in labels:
            labels.append(label)
    if unsafe_seen and redacted_code not in labels:
        labels.append(redacted_code)
    return labels


def _safe_state_label(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    label = value.strip()
    if (
        not label
        or len(label) > _SAFE_STATE_LABEL_MAX_LENGTH
        or not label[0].isalpha()
        or label.lower() != label
        or any(character not in _SAFE_STATE_LABEL_CHARS for character in label)
    ):
        return None
    return label


def _safe_last_result(value: object) -> dict[str, object] | None:
    if not isinstance(value, Mapping):
        return None
    result: dict[str, object] = {}
    status = _safe_state_label(value.get("status"))
    if status is not None:
        result["status"] = status
    row_counts = _safe_int_mapping(value.get("row_counts"))
    if row_counts:
        result["row_counts"] = row_counts
    skipped = _safe_int_mapping(value.get("skipped"))
    if skipped:
        result["skipped"] = skipped
    warnings = _safe_warning_list(value.get("warnings"))
    if warnings:
        result["warnings"] = warnings
    return result or None


def _safe_int_mapping(value: object) -> dict[str, int]:
    if not isinstance(value, Mapping):
        return {}
    result: dict[str, int] = {}
    for key, count in value.items():
        safe_key = _safe_state_label(key)
        if safe_key is None or not isinstance(count, int) or isinstance(count, bool) or count < 0:
            continue
        result[safe_key] = count
    return result
