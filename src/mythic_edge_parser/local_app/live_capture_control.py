from __future__ import annotations

import asyncio
import json
import os
import secrets
import sqlite3
import threading
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
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

from .live_capture_control_payload_helpers import (
    LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION as LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION,
)
from .live_capture_control_payload_helpers import (
    LIVE_CAPTURE_HEARTBEAT_STALE_SECONDS as LIVE_CAPTURE_HEARTBEAT_STALE_SECONDS,
)
from .live_capture_control_payload_helpers import (
    LIVE_CAPTURE_STATE_STALE_SECONDS as LIVE_CAPTURE_STATE_STALE_SECONDS,
)
from .live_capture_control_payload_helpers import (
    _append_event_kind,
    _default_progress,
    _errors_for_status,
    _first_blocking_precondition,
    _heartbeat_state,
    _heartbeat_status_from_progress,
    _iso_datetime,
    _merge_safe_codes,
    _now_iso,
    _parse_iso_datetime,
    _parser_status_blurb,
    _precondition,
    _progress_with_reason,
    _row_count_total,
    _safe_completed_match_result,
    _safe_error_list,
    _safe_event_kind_label,
    _safe_heartbeat,
    _safe_iso_or_none,
    _safe_last_result,
    _safe_optional_non_negative_int,
    _safe_progress,
    _safe_state_label,
    _safe_state_summary,
    _safe_warning_list,
    _state_is_stale,
    _warnings_for_status,
)
from .mtga_process_lifecycle import (
    MTGA_PROCESS_SCHEMA_VERSION,
    MTGA_RECONNECT_WINDOW_SECONDS,
    build_automation_readiness,
    build_mtga_process_status,
)
from .paths import LocalAppPaths, display_app_path
from .setup_status import build_analytics_database_status, build_live_player_log_status

LIVE_CAPTURE_STATUS_OBJECT = "mythic_edge_local_app_live_capture_status"
LIVE_CAPTURE_START_RESULT_OBJECT = "mythic_edge_local_app_live_capture_start_result"
LIVE_CAPTURE_STOP_RESULT_OBJECT = "mythic_edge_local_app_live_capture_stop_result"
LIVE_CAPTURE_SCHEMA_VERSION = "live_app_explicit_start_capture_control.v1"
LIVE_CAPTURE_STATE_FILENAME = "live_capture_state.json"
LIVE_CAPTURE_LOCK_FILENAME = "live_capture_lock.json"
LIVE_CAPTURE_HEARTBEAT_UPDATE_SECONDS = 10
MTGA_PROCESS_SUPERVISOR_CHECK_SECONDS = 1
LIVE_CAPTURE_SOURCE_KIND = "live_parser"
LIVE_CAPTURE_SUPERVISOR_KIND = "local_app_capture_supervisor"
_MTGA_LIFECYCLE_STATUSES = frozenset(
    {
        "ready_to_start",
        "starting",
        "capturing",
        "mtga_unavailable",
        "reconnect_window",
        "shutting_down",
        "stopped",
        "blocked",
        "failed",
        "unknown",
    }
)
_MTGA_SHUTDOWN_REASONS = frozenset(
    {
        "mtga_unavailable_timeout",
        "operator_stop_requested",
        "supervisor_stop_requested",
        "supervisor_error",
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
    mtga_process = build_mtga_process_status()
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
        mtga_process=mtga_process,
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
                "mtga_lifecycle": _mtga_lifecycle_state(
                    status="shutting_down",
                    mtga_process_status=str(
                        _safe_mtga_lifecycle_state(state.get("mtga_lifecycle")).get("mtga_process_status")
                        or "unknown"
                    ),
                    checked_at=stopping_at,
                    shutdown_reason="operator_stop_requested",
                    last_detected_at=_safe_mtga_lifecycle_state(state.get("mtga_lifecycle")).get("last_detected_at"),
                    warnings=["capture_shutdown_started"],
                ),
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
                "mtga_lifecycle": _mtga_lifecycle_state(
                    status="stopped",
                    mtga_process_status=str(
                        _safe_mtga_lifecycle_state(state.get("mtga_lifecycle")).get("mtga_process_status")
                        or "unknown"
                    ),
                    checked_at=stopped_at,
                    shutdown_reason="operator_stop_requested",
                    last_detected_at=_safe_mtga_lifecycle_state(state.get("mtga_lifecycle")).get("last_detected_at"),
                    warnings=["capture_shutdown_completed"],
                ),
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
        last_mtga_process_check = datetime.min.replace(tzinfo=UTC)
        try:
            while not self._stop_event.is_set():
                try:
                    event = await asyncio.wait_for(subscriber.recv(), timeout=0.25)
                except TimeoutError:
                    progress["log_poll_count"] = int(progress["log_poll_count"]) + 1
                    now = datetime.now(UTC)
                    process_check_due = (
                        now - last_mtga_process_check
                    ).total_seconds() >= MTGA_PROCESS_SUPERVISOR_CHECK_SECONDS
                    if process_check_due:
                        last_mtga_process_check = now
                        if self._tick_mtga_lifecycle(progress, now=now):
                            break
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
                state = _read_capture_state(self.paths)
                _write_capture_state(
                    self.paths,
                    {
                        **state,
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
                        "mtga_lifecycle": _stopped_mtga_lifecycle_state(state, stopped_at=stopped_at),
                    },
                )

    def _tick_mtga_lifecycle(self, progress: Mapping[str, object], *, now: datetime) -> bool:
        checked_at = _iso_datetime(now)
        mtga_process = build_mtga_process_status(checked_at=now)
        process_status = _safe_state_label(mtga_process.get("status")) or "unknown"
        state = _read_capture_state(self.paths)
        lifecycle = _safe_mtga_lifecycle_state(state.get("mtga_lifecycle"))

        if process_status == "detected":
            warnings = ["waiting_for_events"]
            if lifecycle.get("status") == "reconnect_window":
                warnings.append("mtga_reconnected")
            _write_capture_state(
                self.paths,
                {
                    **state,
                    "status": "capturing",
                    "updated_at": checked_at,
                    "heartbeat": _heartbeat_state(
                        _heartbeat_status_from_progress(progress),
                        started_at=state.get("started_at"),
                        heartbeat_updated_at=checked_at,
                    ),
                    "progress": progress,
                    "mtga_lifecycle": _mtga_lifecycle_state(
                        status="capturing",
                        mtga_process_status=process_status,
                        checked_at=checked_at,
                        last_detected_at=checked_at,
                        warnings=warnings[1:],
                    ),
                    "warnings": warnings,
                    "errors": [],
                },
            )
            return False

        if process_status == "not_detected":
            reconnect_started_at = _safe_iso_or_none(lifecycle.get("reconnect_started_at")) or checked_at
            started = _parse_iso_datetime(reconnect_started_at) or now
            deadline = started + timedelta(seconds=MTGA_RECONNECT_WINDOW_SECONDS)
            deadline_at = _iso_datetime(deadline)
            if now >= deadline:
                _write_capture_state(
                    self.paths,
                    {
                        **state,
                        "status": "stopping",
                        "updated_at": checked_at,
                        "heartbeat": _heartbeat_state(
                            "waiting",
                            started_at=state.get("started_at"),
                            heartbeat_updated_at=checked_at,
                        ),
                        "progress": _progress_with_reason(progress, "capture_stopped_before_completion"),
                        "mtga_lifecycle": _mtga_lifecycle_state(
                            status="shutting_down",
                            mtga_process_status=process_status,
                            checked_at=checked_at,
                            reconnect_started_at=reconnect_started_at,
                            reconnect_deadline_at=deadline_at,
                            shutdown_reason="mtga_unavailable_timeout",
                            last_detected_at=lifecycle.get("last_detected_at"),
                            warnings=[
                                "mtga_not_detected",
                                "mtga_unavailable_timeout",
                                "capture_shutdown_started",
                            ],
                        ),
                        "warnings": [
                            "waiting_for_events",
                            "mtga_not_detected",
                            "mtga_unavailable_timeout",
                            "capture_shutdown_started",
                        ],
                        "errors": [],
                    },
                )
                self._stop_event.set()
                return True

            _write_capture_state(
                self.paths,
                {
                    **state,
                    "status": "capturing",
                    "updated_at": checked_at,
                    "heartbeat": _heartbeat_state(
                        _heartbeat_status_from_progress(progress),
                        started_at=state.get("started_at"),
                        heartbeat_updated_at=checked_at,
                    ),
                    "progress": progress,
                    "mtga_lifecycle": _mtga_lifecycle_state(
                        status="reconnect_window",
                        mtga_process_status=process_status,
                        checked_at=checked_at,
                        reconnect_started_at=reconnect_started_at,
                        reconnect_deadline_at=deadline_at,
                        last_detected_at=lifecycle.get("last_detected_at"),
                        warnings=["mtga_not_detected", "mtga_reconnect_window_active"],
                    ),
                    "warnings": [
                        "waiting_for_events",
                        "mtga_not_detected",
                        "mtga_reconnect_window_active",
                    ],
                    "errors": [],
                },
            )
            return False

        warning_codes = _safe_warning_list(mtga_process.get("warnings"))
        error_codes = _safe_error_list(mtga_process.get("errors"))
        _write_capture_state(
            self.paths,
            {
                **state,
                "status": "capturing",
                "updated_at": checked_at,
                "heartbeat": _heartbeat_state(
                    _heartbeat_status_from_progress(progress),
                    started_at=state.get("started_at"),
                    heartbeat_updated_at=checked_at,
                ),
                "progress": progress,
                "mtga_lifecycle": _mtga_lifecycle_state(
                    status="capturing",
                    mtga_process_status=process_status,
                    checked_at=checked_at,
                    last_detected_at=lifecycle.get("last_detected_at"),
                    warnings=warning_codes,
                    errors=error_codes,
                ),
                "warnings": ["waiting_for_events", *warning_codes],
                "errors": [],
            },
        )
        return False


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
    mtga_process: Mapping[str, object],
    last_result: object,
    warnings: list[str],
    errors: list[str],
) -> dict[str, object]:
    heartbeat = _safe_heartbeat(state.get("heartbeat"), status=status, state=state)
    progress = _safe_progress(state.get("progress"), status=status, last_result=last_result)
    mtga_lifecycle = _mtga_lifecycle_for_status(status=status, state=state, mtga_process=mtga_process)
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
        "mtga_lifecycle": mtga_lifecycle,
        "parser_status_blurb": _parser_status_blurb(
            status=status,
            reason=str(capture.get("reason") or ""),
            progress=progress,
        ),
        "warnings": warnings,
        "errors": errors,
    }


def _mtga_lifecycle_for_status(
    *,
    status: str,
    state: Mapping[str, object],
    mtga_process: Mapping[str, object],
) -> dict[str, object]:
    lifecycle = _safe_mtga_lifecycle_state(state.get("mtga_lifecycle"))
    process_status = _safe_state_label(mtga_process.get("status")) or "unknown"
    checked_at = _safe_iso_or_none(mtga_process.get("checked_at")) or _now_iso()
    lifecycle_status = _derived_mtga_lifecycle_status(status=status, lifecycle=lifecycle, process_status=process_status)
    reconnect_deadline_at = lifecycle.get("reconnect_deadline_at")
    warnings = _safe_warning_list(lifecycle.get("warnings")) + [
        warning
        for warning in _safe_warning_list(mtga_process.get("warnings"))
        if warning not in _safe_warning_list(lifecycle.get("warnings"))
    ]
    if lifecycle_status == "reconnect_window" and "mtga_reconnect_window_active" not in warnings:
        warnings.append("mtga_reconnect_window_active")
    if lifecycle_status == "mtga_unavailable" and "mtga_not_detected" not in warnings:
        warnings.append("mtga_not_detected")
    if process_status == "unsupported_platform" and "mtga_process_detection_unsupported" not in warnings:
        warnings.append("mtga_process_detection_unsupported")

    return {
        "schema_version": MTGA_PROCESS_SCHEMA_VERSION,
        "status": lifecycle_status,
        "mtga_process_status": process_status,
        "reconnect_window_seconds": MTGA_RECONNECT_WINDOW_SECONDS,
        "reconnect_started_at": lifecycle.get("reconnect_started_at"),
        "reconnect_deadline_at": reconnect_deadline_at,
        "seconds_remaining": _seconds_until(reconnect_deadline_at) if lifecycle_status == "reconnect_window" else None,
        "shutdown_reason": lifecycle.get("shutdown_reason"),
        "last_detected_at": checked_at if process_status == "detected" else lifecycle.get("last_detected_at"),
        "last_checked_at": checked_at,
        "automation_start_allowed": False,
        "automation_readiness": build_automation_readiness(mtga_process),
        "warnings": warnings,
        "errors": _merge_safe_codes(
            _safe_error_list(lifecycle.get("errors")),
            _safe_error_list(mtga_process.get("errors")),
        ),
    }


def _derived_mtga_lifecycle_status(
    *,
    status: str,
    lifecycle: Mapping[str, object],
    process_status: str,
) -> str:
    stored_status = _safe_state_label(lifecycle.get("status"))
    if stored_status in {"reconnect_window", "shutting_down"}:
        return stored_status
    if status == "ready_to_start":
        return "mtga_unavailable" if process_status == "not_detected" else "ready_to_start"
    if status == "capturing":
        return "mtga_unavailable" if process_status == "not_detected" else "capturing"
    if status in _MTGA_LIFECYCLE_STATUSES:
        return status
    return "unknown"


def _safe_mtga_lifecycle_state(value: object) -> dict[str, object]:
    lifecycle = value if isinstance(value, Mapping) else {}
    status = _safe_state_label(lifecycle.get("status")) if lifecycle else None
    if status not in _MTGA_LIFECYCLE_STATUSES:
        status = "unknown"
    process_status = _safe_state_label(lifecycle.get("mtga_process_status")) if lifecycle else None
    if process_status not in {"detected", "not_detected", "unsupported_platform", "detector_unavailable", "unknown"}:
        process_status = "unknown"
    shutdown_reason = _safe_state_label(lifecycle.get("shutdown_reason")) if lifecycle else None
    if shutdown_reason not in _MTGA_SHUTDOWN_REASONS:
        shutdown_reason = None
    return {
        "schema_version": MTGA_PROCESS_SCHEMA_VERSION,
        "status": status,
        "mtga_process_status": process_status,
        "reconnect_window_seconds": MTGA_RECONNECT_WINDOW_SECONDS,
        "reconnect_started_at": _safe_iso_or_none(lifecycle.get("reconnect_started_at")) if lifecycle else None,
        "reconnect_deadline_at": _safe_iso_or_none(lifecycle.get("reconnect_deadline_at")) if lifecycle else None,
        "seconds_remaining": _safe_optional_non_negative_int(lifecycle.get("seconds_remaining")) if lifecycle else None,
        "shutdown_reason": shutdown_reason,
        "last_detected_at": _safe_iso_or_none(lifecycle.get("last_detected_at")) if lifecycle else None,
        "last_checked_at": _safe_iso_or_none(lifecycle.get("last_checked_at")) if lifecycle else None,
        "warnings": _safe_warning_list(lifecycle.get("warnings")) if lifecycle else [],
        "errors": _safe_error_list(lifecycle.get("errors")) if lifecycle else [],
    }


def _seconds_until(deadline_at: object) -> int | None:
    deadline = _parse_iso_datetime(_safe_iso_or_none(deadline_at))
    if deadline is None:
        return None
    return max(0, int((deadline - datetime.now(UTC)).total_seconds()))


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
        "mtga_lifecycle": _safe_mtga_lifecycle_state(payload.get("mtga_lifecycle")),
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
        "mtga_lifecycle": _safe_mtga_lifecycle_state(None),
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
        "mtga_lifecycle": _safe_mtga_lifecycle_state(payload.get("mtga_lifecycle")),
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
    mtga_process = build_mtga_process_status()
    player_log_ready = _player_log_ready(paths)
    preconditions = _build_preconditions(paths, player_log_ready, write_check=False)
    return _status_payload(
        status="blocked",
        capture=_capture_summary(status="blocked", state=state, supervisor=None, reason=reason),
        preconditions=preconditions,
        state=state,
        mtga_process=mtga_process,
        last_result=_safe_last_result(state.get("last_result")),
        warnings=_warnings_for_status("blocked", state),
        errors=[reason],
    )


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


def _mtga_lifecycle_state(
    *,
    status: str,
    mtga_process_status: str,
    checked_at: object,
    reconnect_started_at: object | None = None,
    reconnect_deadline_at: object | None = None,
    shutdown_reason: str | None = None,
    last_detected_at: object | None = None,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> dict[str, object]:
    reconnect_deadline = _safe_iso_or_none(reconnect_deadline_at)
    lifecycle = {
        "schema_version": MTGA_PROCESS_SCHEMA_VERSION,
        "status": status,
        "mtga_process_status": mtga_process_status,
        "reconnect_window_seconds": MTGA_RECONNECT_WINDOW_SECONDS,
        "reconnect_started_at": _safe_iso_or_none(reconnect_started_at),
        "reconnect_deadline_at": reconnect_deadline,
        "seconds_remaining": _seconds_until(reconnect_deadline) if status == "reconnect_window" else None,
        "shutdown_reason": shutdown_reason,
        "last_detected_at": _safe_iso_or_none(last_detected_at),
        "last_checked_at": _safe_iso_or_none(checked_at),
        "warnings": warnings or [],
        "errors": errors or [],
    }
    return _safe_mtga_lifecycle_state(lifecycle)


def _stopped_mtga_lifecycle_state(state: Mapping[str, object], *, stopped_at: str) -> dict[str, object]:
    lifecycle = _safe_mtga_lifecycle_state(state.get("mtga_lifecycle"))
    shutdown_reason = _safe_state_label(lifecycle.get("shutdown_reason")) or "supervisor_stop_requested"
    warnings = _safe_warning_list(lifecycle.get("warnings"))
    if shutdown_reason == "mtga_unavailable_timeout" and "capture_shutdown_completed" not in warnings:
        warnings.append("capture_shutdown_completed")
    return _mtga_lifecycle_state(
        status="stopped",
        mtga_process_status=str(lifecycle.get("mtga_process_status") or "unknown"),
        checked_at=lifecycle.get("last_checked_at") or stopped_at,
        reconnect_started_at=lifecycle.get("reconnect_started_at"),
        reconnect_deadline_at=lifecycle.get("reconnect_deadline_at"),
        shutdown_reason=shutdown_reason,
        last_detected_at=lifecycle.get("last_detected_at"),
        warnings=warnings,
        errors=_safe_error_list(lifecycle.get("errors")),
    )
