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
LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION = "live_app_capture_heartbeat_no_row_diagnostics.v1"
LIVE_CAPTURE_STATE_FILENAME = "live_capture_state.json"
LIVE_CAPTURE_LOCK_FILENAME = "live_capture_lock.json"
LIVE_CAPTURE_STATE_STALE_SECONDS = 15 * 60
LIVE_CAPTURE_HEARTBEAT_STALE_SECONDS = 30
LIVE_CAPTURE_HEARTBEAT_UPDATE_SECONDS = 10
LIVE_CAPTURE_SOURCE_KIND = "live_parser"
LIVE_CAPTURE_SUPERVISOR_KIND = "local_app_capture_supervisor"
_SAFE_STATE_LABEL_MAX_LENGTH = 80
_SAFE_STATE_LABEL_CHARS = frozenset("abcdefghijklmnopqrstuvwxyz0123456789_")
_NO_WRITE_REASONS = frozenset(
    {
        "not_started",
        "no_log_bytes_seen",
        "no_log_chunks_seen",
        "no_structured_entries_seen",
        "no_parser_events_routed",
        "no_match_id_seen",
        "no_completed_game_rows",
        "match_row_not_ready",
        "sqlite_ingest_not_attempted",
        "sqlite_write_failed",
        "capture_stopped_before_completion",
        "capture_state_stale",
        "rows_written",
        "unknown",
    }
)
_HEARTBEAT_STATUSES = frozenset(
    {
        "not_started",
        "starting",
        "waiting",
        "progress",
        "rows_written",
        "blocked",
        "failed",
        "stale",
        "unknown",
    }
)

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
        started_at = _now_iso()
        _write_capture_state(
            paths,
            {
                "status": "starting",
                "supervisor_token": supervisor_id,
                "pid": os.getpid(),
                "supervisor_kind": LIVE_CAPTURE_SUPERVISOR_KIND,
                "source_kind": LIVE_CAPTURE_SOURCE_KIND,
                "started_at": started_at,
                "updated_at": started_at,
                "parser_runner_started": True,
                "tailing_started": False,
                "sqlite_live_writes_enabled": False,
                "external_transport_allowed": False,
                "raw_player_log_storage_enabled": False,
                "last_result": None,
                "heartbeat": _heartbeat_state("starting", started_at=started_at, heartbeat_updated_at=started_at),
                "progress": _default_progress("no_parser_events_routed"),
                "warnings": [],
                "errors": [],
            },
        )
        try:
            supervisor.start()
        except Exception:
            _SUPERVISORS.pop(_registry_key(paths), None)
            failed_at = _now_iso()
            _write_capture_state(
                paths,
                {
                    "status": "failed",
                    "supervisor_token": supervisor_id,
                    "pid": os.getpid(),
                    "supervisor_kind": LIVE_CAPTURE_SUPERVISOR_KIND,
                    "source_kind": LIVE_CAPTURE_SOURCE_KIND,
                    "started_at": started_at,
                    "updated_at": failed_at,
                    "parser_runner_started": False,
                    "tailing_started": False,
                    "sqlite_live_writes_enabled": False,
                    "external_transport_allowed": False,
                    "raw_player_log_storage_enabled": False,
                    "last_result": None,
                    "heartbeat": _heartbeat_state("failed", started_at=started_at, heartbeat_updated_at=failed_at),
                    "progress": _default_progress("no_parser_events_routed"),
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

        stopping_at = _now_iso()
        _write_capture_state(
            paths,
            {
                **state,
                "status": "stopping",
                "updated_at": stopping_at,
                "heartbeat": _heartbeat_state(
                    "waiting",
                    started_at=state.get("started_at"),
                    heartbeat_updated_at=stopping_at,
                ),
                "progress": _progress_with_reason(state.get("progress"), "capture_stopped_before_completion"),
            },
        )
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
        stopped_at = _now_iso()
        _write_capture_state(
            paths,
            {
                **state,
                "status": "stopped",
                "updated_at": stopped_at,
                "parser_runner_started": False,
                "tailing_started": False,
                "sqlite_live_writes_enabled": False,
                "last_result": _safe_last_result(state.get("last_result")),
                "heartbeat": _heartbeat_state(
                    "not_started",
                    started_at=state.get("started_at"),
                    heartbeat_updated_at=stopped_at,
                ),
                "progress": _progress_with_reason(state.get("progress"), "capture_stopped_before_completion"),
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
            crashed_at = _now_iso()
            state = _read_capture_state(self.paths)
            _write_capture_state(
                self.paths,
                {
                    **state,
                    "status": "failed",
                    "updated_at": crashed_at,
                    "parser_runner_started": False,
                    "tailing_started": False,
                    "sqlite_live_writes_enabled": False,
                    "heartbeat": _heartbeat_state(
                        "failed",
                        started_at=state.get("started_at"),
                        heartbeat_updated_at=crashed_at,
                    ),
                    "progress": _progress_with_reason(state.get("progress"), "unknown"),
                    "errors": ["supervisor_crashed"],
                },
            )

    async def _run_async(self) -> None:
        player_log_path = _configured_player_log_path(self.paths)
        if player_log_path is None:
            blocked_at = _now_iso()
            state = _read_capture_state(self.paths)
            _write_capture_state(
                self.paths,
                {
                    **state,
                    "status": "blocked",
                    "updated_at": blocked_at,
                    "heartbeat": _heartbeat_state(
                        "blocked",
                        started_at=state.get("started_at"),
                        heartbeat_updated_at=blocked_at,
                    ),
                    "progress": _progress_with_reason(state.get("progress"), "not_started"),
                    "errors": ["player_log_not_ready"],
                },
            )
            return

        reset_runtime_state()
        try:
            stream, subscriber = await MtgaEventStream.start(player_log_path)
        except StreamError:
            failed_at = _now_iso()
            state = _read_capture_state(self.paths)
            _write_capture_state(
                self.paths,
                {
                    **state,
                    "status": "failed",
                    "updated_at": failed_at,
                    "parser_runner_started": False,
                    "tailing_started": False,
                    "sqlite_live_writes_enabled": False,
                    "heartbeat": _heartbeat_state(
                        "failed",
                        started_at=state.get("started_at"),
                        heartbeat_updated_at=failed_at,
                    ),
                    "progress": _progress_with_reason(state.get("progress"), "no_log_chunks_seen"),
                    "errors": ["tailer_start_failed"],
                },
            )
            return

        progress = _default_progress("no_parser_events_routed")
        heartbeat_at = _now_iso()
        _write_capture_state(
            self.paths,
            {
                **_read_capture_state(self.paths),
                "status": "capturing",
                "updated_at": heartbeat_at,
                "parser_runner_started": True,
                "tailing_started": True,
                "sqlite_live_writes_enabled": True,
                "heartbeat": _heartbeat_state(
                    "waiting",
                    started_at=_read_capture_state(self.paths).get("started_at"),
                    heartbeat_updated_at=heartbeat_at,
                ),
                "progress": progress,
                "warnings": ["waiting_for_events"],
                "errors": [],
            },
        )
        written_matches: set[str] = set()
        seen_match_ids: set[str] = set()
        last_heartbeat_write = datetime.now(UTC)
        try:
            while not self._stop_event.is_set():
                try:
                    event = await asyncio.wait_for(subscriber.recv(), timeout=0.25)
                except TimeoutError:
                    progress["log_poll_count"] = int(progress["log_poll_count"]) + 1
                    heartbeat_due = (
                        datetime.now(UTC) - last_heartbeat_write
                    ).total_seconds() >= LIVE_CAPTURE_HEARTBEAT_UPDATE_SECONDS
                    if heartbeat_due:
                        _write_capture_state(
                            self.paths,
                            {
                                **_read_capture_state(self.paths),
                                "status": "capturing",
                                "updated_at": _now_iso(),
                                "heartbeat": _heartbeat_state(
                                    _heartbeat_status_from_progress(progress),
                                    started_at=_read_capture_state(self.paths).get("started_at"),
                                    heartbeat_updated_at=_now_iso(),
                                ),
                                "progress": progress,
                                "warnings": ["waiting_for_events"],
                                "errors": [],
                            },
                        )
                        last_heartbeat_write = datetime.now(UTC)
                    continue
                if event is None:
                    break
                event_seen_at = _now_iso()
                progress["structured_entry_count"] = int(progress["structured_entry_count"]) + 1
                progress["parser_event_count"] = int(progress["parser_event_count"]) + 1
                progress["last_event_seen_at"] = event_seen_at
                progress["last_no_write_reason"] = "no_match_id_seen"
                _append_event_kind(progress, _safe_event_kind_label(event))
                _update_match_summary(event)
                match_id = str(get_context_snapshot().get("current_match_id", "") or "")
                if match_id:
                    seen_match_ids.add(match_id)
                    progress["match_ids_seen_count"] = len(seen_match_ids)
                    progress["current_match_detected"] = True
                if not match_id:
                    _write_capture_state(
                        self.paths,
                        {
                            **_read_capture_state(self.paths),
                            "status": "capturing",
                            "updated_at": event_seen_at,
                            "heartbeat": _heartbeat_state(
                                "progress",
                                started_at=_read_capture_state(self.paths).get("started_at"),
                                heartbeat_updated_at=event_seen_at,
                            ),
                            "progress": progress,
                            "warnings": ["waiting_for_events"],
                            "errors": [],
                        },
                    )
                    last_heartbeat_write = datetime.now(UTC)
                    continue
                if match_id in written_matches:
                    continue
                match_row = build_match_log_row(match_id)
                game_rows = [
                    row
                    for row in build_game_summary_rows(match_id)
                    if str(row.get("Game Result", "") or "").strip()
                ]
                progress["completed_game_rows_seen"] = len(game_rows)
                if match_row is None:
                    progress["last_no_write_reason"] = "match_row_not_ready"
                    _write_capture_state(
                        self.paths,
                        {
                            **_read_capture_state(self.paths),
                            "status": "capturing",
                            "updated_at": event_seen_at,
                            "heartbeat": _heartbeat_state(
                                "progress",
                                started_at=_read_capture_state(self.paths).get("started_at"),
                                heartbeat_updated_at=event_seen_at,
                            ),
                            "progress": progress,
                            "warnings": ["waiting_for_events"],
                            "errors": [],
                        },
                    )
                    last_heartbeat_write = datetime.now(UTC)
                    continue
                if not game_rows:
                    progress["last_no_write_reason"] = "no_completed_game_rows"
                    _write_capture_state(
                        self.paths,
                        {
                            **_read_capture_state(self.paths),
                            "status": "capturing",
                            "updated_at": event_seen_at,
                            "heartbeat": _heartbeat_state(
                                "progress",
                                started_at=_read_capture_state(self.paths).get("started_at"),
                                heartbeat_updated_at=event_seen_at,
                            ),
                            "progress": progress,
                            "warnings": ["waiting_for_events"],
                            "errors": [],
                        },
                    )
                    last_heartbeat_write = datetime.now(UTC)
                    continue
                progress["sqlite_write_attempt_count"] = int(progress["sqlite_write_attempt_count"]) + 1
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
                written_at = _now_iso()
                progress["sqlite_rows_written"] = int(progress["sqlite_rows_written"]) + _row_count_total(
                    result.row_counts
                )
                progress["last_no_write_reason"] = "rows_written"
                progress["last_sqlite_write_at"] = written_at
                progress["last_completed_match_result"] = _safe_completed_match_result(match_row)
                _write_capture_state(
                    self.paths,
                    {
                        **_read_capture_state(self.paths),
                        "status": "capturing",
                        "updated_at": written_at,
                        "sqlite_live_writes_enabled": True,
                        "heartbeat": _heartbeat_state(
                            "rows_written",
                            started_at=_read_capture_state(self.paths).get("started_at"),
                            heartbeat_updated_at=written_at,
                        ),
                        "progress": progress,
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
                last_heartbeat_write = datetime.now(UTC)
        except (AnalyticsReplayIngestError, sqlite3.DatabaseError, OSError):
            failed_at = _now_iso()
            progress["last_no_write_reason"] = "sqlite_write_failed"
            _write_capture_state(
                self.paths,
                {
                    **_read_capture_state(self.paths),
                    "status": "failed",
                    "updated_at": failed_at,
                    "sqlite_live_writes_enabled": False,
                    "heartbeat": _heartbeat_state(
                        "failed",
                        started_at=_read_capture_state(self.paths).get("started_at"),
                        heartbeat_updated_at=failed_at,
                    ),
                    "progress": progress,
                    "errors": ["sqlite_write_failed"],
                },
            )
        finally:
            await stream.shutdown()
            if self._stop_event.is_set():
                stopped_at = _now_iso()
                _write_capture_state(
                    self.paths,
                    {
                        **_read_capture_state(self.paths),
                        "status": "stopped",
                        "updated_at": stopped_at,
                        "parser_runner_started": False,
                        "tailing_started": False,
                        "sqlite_live_writes_enabled": False,
                        "heartbeat": _heartbeat_state(
                            "not_started",
                            started_at=_read_capture_state(self.paths).get("started_at"),
                            heartbeat_updated_at=stopped_at,
                        ),
                        "progress": _progress_with_reason(progress, "capture_stopped_before_completion"),
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
    heartbeat = _safe_heartbeat(state.get("heartbeat"), status=status, state=state)
    progress = _safe_progress(state.get("progress"), status=status, last_result=last_result)
    return {
        "object": LIVE_CAPTURE_STATUS_OBJECT,
        "schema_version": LIVE_CAPTURE_SCHEMA_VERSION,
        "status": status,
        "mode": "explicit_operator_control",
        "capture": capture,
        "preconditions": preconditions,
        "state": _safe_state_summary(state),
        "last_result": last_result,
        "heartbeat": heartbeat,
        "progress": progress,
        "parser_status_blurb": _parser_status_blurb(
            status=status,
            reason=str(capture.get("reason") or ""),
            progress=progress,
        ),
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
        "heartbeat": _safe_heartbeat(payload.get("heartbeat"), status=status, state=payload),
        "progress": _safe_progress(payload.get("progress"), status=status, last_result=payload.get("last_result")),
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
        "heartbeat": _safe_heartbeat(None, status=status, state={}),
        "progress": _safe_progress(None, status=status, last_result=None),
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
        "heartbeat": _safe_heartbeat(
            payload.get("heartbeat"),
            status=str(payload.get("status", "unknown") or "unknown"),
            state=payload,
        ),
        "progress": _safe_progress(
            payload.get("progress"),
            status=str(payload.get("status", "unknown") or "unknown"),
            last_result=payload.get("last_result"),
        ),
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


def _heartbeat_state(
    status: str,
    *,
    started_at: object,
    heartbeat_updated_at: object,
) -> dict[str, object]:
    return {
        "schema_version": LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION,
        "status": status if status in _HEARTBEAT_STATUSES else "unknown",
        "heartbeat_updated_at": _safe_iso_or_none(heartbeat_updated_at),
        "capture_duration_seconds": _capture_duration_seconds(
            _safe_iso_or_none(started_at),
            _safe_iso_or_none(heartbeat_updated_at),
        ),
        "heartbeat_age_seconds": _heartbeat_age_seconds(_safe_iso_or_none(heartbeat_updated_at)),
        "stale_after_seconds": LIVE_CAPTURE_HEARTBEAT_STALE_SECONDS,
    }


def _safe_heartbeat(value: object, *, status: str, state: Mapping[str, object]) -> dict[str, object]:
    heartbeat = value if isinstance(value, Mapping) else {}
    started_at = _safe_iso_or_none(state.get("started_at"))
    heartbeat_updated_at = _safe_iso_or_none(heartbeat.get("heartbeat_updated_at")) or _safe_iso_or_none(
        state.get("updated_at")
    )
    heartbeat_status = _safe_state_label(heartbeat.get("status")) if heartbeat else None
    if heartbeat_status not in _HEARTBEAT_STATUSES:
        heartbeat_status = _default_heartbeat_status(status)
    age_seconds = _heartbeat_age_seconds(heartbeat_updated_at)
    if status in {"starting", "capturing", "stopping"} and age_seconds is not None:
        if age_seconds > LIVE_CAPTURE_HEARTBEAT_STALE_SECONDS:
            heartbeat_status = "stale"
    if status in {"blocked", "failed", "stale"}:
        heartbeat_status = _default_heartbeat_status(status)
    return {
        "schema_version": LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION,
        "status": heartbeat_status,
        "heartbeat_updated_at": heartbeat_updated_at,
        "capture_duration_seconds": _capture_duration_seconds(started_at, heartbeat_updated_at),
        "heartbeat_age_seconds": age_seconds,
        "stale_after_seconds": LIVE_CAPTURE_HEARTBEAT_STALE_SECONDS,
    }


def _default_heartbeat_status(status: str) -> str:
    if status == "starting":
        return "starting"
    if status == "capturing":
        return "waiting"
    if status == "blocked":
        return "blocked"
    if status == "failed":
        return "failed"
    if status == "stale":
        return "stale"
    if status in {"ready_to_start", "stopped", "not_initialized"}:
        return "not_started"
    return "unknown"


def _default_progress(reason: str) -> dict[str, object]:
    return {
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
        "last_no_write_reason": reason if reason in _NO_WRITE_REASONS else "unknown",
        "last_event_seen_at": None,
        "last_sqlite_write_at": None,
    }


def _safe_progress(value: object, *, status: str, last_result: object) -> dict[str, object]:
    progress = _default_progress(_default_no_write_reason(status=status, last_result=last_result))
    if not isinstance(value, Mapping):
        return progress
    for key in (
        "log_poll_count",
        "log_chunks_seen",
        "structured_entry_count",
        "parser_event_count",
        "match_ids_seen_count",
        "completed_game_rows_seen",
        "sqlite_write_attempt_count",
        "sqlite_rows_written",
    ):
        progress[key] = _safe_non_negative_int(value.get(key))
    progress["parser_event_kinds_seen"] = _safe_progress_label_list(value.get("parser_event_kinds_seen"))
    progress["current_match_detected"] = bool(value.get("current_match_detected", False))
    progress["current_match_game_wins"] = _safe_optional_non_negative_int(value.get("current_match_game_wins"))
    progress["current_match_game_losses"] = _safe_optional_non_negative_int(value.get("current_match_game_losses"))
    progress["last_completed_match_result"] = _safe_state_label(value.get("last_completed_match_result"))
    progress["last_completed_match_game_wins"] = _safe_optional_non_negative_int(
        value.get("last_completed_match_game_wins")
    )
    progress["last_completed_match_game_losses"] = _safe_optional_non_negative_int(
        value.get("last_completed_match_game_losses")
    )
    reason = _safe_state_label(value.get("last_no_write_reason"))
    if reason in _NO_WRITE_REASONS:
        progress["last_no_write_reason"] = reason
    if int(progress["sqlite_rows_written"]) > 0:
        progress["last_no_write_reason"] = "rows_written"
    if status == "stale":
        progress["last_no_write_reason"] = "capture_state_stale"
    progress["last_event_seen_at"] = _safe_iso_or_none(value.get("last_event_seen_at"))
    progress["last_sqlite_write_at"] = _safe_iso_or_none(value.get("last_sqlite_write_at"))
    return progress


def _progress_with_reason(value: object, reason: str) -> dict[str, object]:
    progress = _safe_progress(value, status="capturing", last_result=None)
    if int(progress["sqlite_rows_written"]) > 0 and reason == "capture_stopped_before_completion":
        progress["last_no_write_reason"] = "rows_written"
    else:
        progress["last_no_write_reason"] = reason if reason in _NO_WRITE_REASONS else "unknown"
    return progress


def _default_no_write_reason(*, status: str, last_result: object) -> str:
    safe_last_result = _safe_last_result(last_result)
    row_counts = safe_last_result.get("row_counts") if isinstance(safe_last_result, Mapping) else {}
    if _row_count_total(row_counts) > 0:
        return "rows_written"
    if status == "stale":
        return "capture_state_stale"
    if status in {"ready_to_start", "blocked", "not_initialized"}:
        return "not_started"
    if status == "stopped":
        return "capture_stopped_before_completion"
    if status == "failed":
        return "unknown"
    return "no_parser_events_routed"


def _heartbeat_status_from_progress(progress: Mapping[str, object]) -> str:
    if _safe_non_negative_int(progress.get("sqlite_rows_written")) > 0:
        return "rows_written"
    if _safe_non_negative_int(progress.get("parser_event_count")) > 0 or bool(progress.get("current_match_detected")):
        return "progress"
    return "waiting"


def _parser_status_blurb(*, status: str, reason: str, progress: Mapping[str, object]) -> dict[str, str]:
    last_no_write_reason = str(progress.get("last_no_write_reason", "unknown") or "unknown")
    if status == "blocked" and reason.startswith("player_log"):
        return _blurb("not_configured", "Configure Player.log to start capture.", "warning")
    if status == "ready_to_start":
        return _blurb("ready_to_start", "Ready to start capture.", "neutral")
    if status == "starting":
        return _blurb("starting", "Starting live capture.", "waiting")
    if status == "stale" or last_no_write_reason == "capture_state_stale":
        return _blurb("capture_state_stale", "Capture heartbeat stopped. Restart capture.", "warning")
    if status == "failed" or last_no_write_reason == "sqlite_write_failed":
        return _blurb("sqlite_write_failed", "SQLite write failed. Review diagnostics.", "error")
    if status == "stopped":
        return _blurb("stopped", "Capture stopped.", "neutral")
    if status == "capturing":
        if _safe_non_negative_int(progress.get("sqlite_rows_written")) > 0:
            return _blurb("most_recent_match_completed", "Most recent completed match was recorded.", "ok")
        if bool(progress.get("current_match_detected")):
            return _blurb("waiting_for_completed_facts", "Capturing; waiting for completed match facts.", "waiting")
        if _safe_non_negative_int(progress.get("parser_event_count")) > 0:
            return _blurb("waiting_for_next_match", "Waiting for next match.", "waiting")
        return _blurb("listening_for_events", "Listening for Player.log events.", "waiting")
    return _blurb("unknown", "Live capture status is unavailable.", "warning")


def _blurb(code: str, text: str, tone: str) -> dict[str, str]:
    return {"code": code, "text": text, "tone": tone}


def _append_event_kind(progress: dict[str, object], label: str) -> None:
    labels = _safe_progress_label_list(progress.get("parser_event_kinds_seen"))
    if label not in labels:
        labels.append(label)
    progress["parser_event_kinds_seen"] = labels


def _safe_event_kind_label(event: object) -> str:
    raw_kind = getattr(event, "kind", None)
    if not isinstance(raw_kind, str) or not raw_kind.strip():
        raw_kind = type(event).__name__
    label_chars: list[str] = []
    previous_was_separator = False
    for character in raw_kind.strip():
        if character.isupper() and label_chars and not previous_was_separator:
            label_chars.append("_")
        if character.isalnum():
            label_chars.append(character.lower())
            previous_was_separator = False
        elif not previous_was_separator:
            label_chars.append("_")
            previous_was_separator = True
    label = "".join(label_chars).strip("_")
    return _safe_state_label(label) or "unknown"


def _safe_completed_match_result(match_row: Mapping[str, object]) -> str | None:
    result = str(match_row.get("Match Result", "") or "").strip().lower().replace(" ", "_")
    return _safe_state_label(result)


def _safe_progress_label_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    labels: list[str] = []
    for entry in value:
        label = _safe_state_label(entry)
        if label is not None and label not in labels:
            labels.append(label)
    return labels


def _safe_non_negative_int(value: object) -> int:
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return value
    return 0


def _safe_optional_non_negative_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return value
    return None


def _row_count_total(row_counts: object) -> int:
    if not isinstance(row_counts, Mapping):
        return 0
    total = 0
    for count in row_counts.values():
        if isinstance(count, int) and not isinstance(count, bool) and count > 0:
            total += count
    return total


def _heartbeat_age_seconds(value: str | None) -> int | None:
    if value is None:
        return None
    parsed = _parse_iso_datetime(value)
    if parsed is None:
        return None
    age = int((datetime.now(UTC) - parsed).total_seconds())
    return age if age >= 0 else None


def _capture_duration_seconds(started_at: str | None, heartbeat_updated_at: str | None) -> int:
    started = _parse_iso_datetime(started_at)
    if started is None:
        return 0
    ended = _parse_iso_datetime(heartbeat_updated_at) or datetime.now(UTC)
    duration = int((ended - started).total_seconds())
    return max(0, duration)


def _parse_iso_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


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
