from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from .paths import LocalAppPaths, display_app_path
from .setup_status import LIVE_PLAYER_LOG_STATUS_OBJECT, build_live_player_log_status, build_live_watcher_status

LIVE_WATCHER_PROCESS_OBJECT = "mythic_edge_local_app_live_watcher_process_status"
LIVE_WATCHER_PROCESS_SCHEMA_VERSION = "live_app_player_log_watcher_process_control_safeguards.v1"
LIVE_WATCHER_PROCESS_STATE_FILENAME = "live_watcher_state.json"
LIVE_WATCHER_PROCESS_STATE_STALE_SECONDS = 15 * 60

_PROCESS_CONTROL_FALSE_FLAGS = (
    "start_allowed",
    "stop_allowed",
    "start_route_enabled",
    "stop_route_enabled",
    "ui_controls_allowed",
    "automatic_start_enabled",
    "parser_runner_started",
    "tailing_started",
    "sqlite_live_writes_enabled",
    "external_transport_allowed",
)


def build_live_watcher_process_status(paths: LocalAppPaths) -> dict[str, object]:
    player_log_status = build_live_player_log_status(paths)
    watcher_status = build_live_watcher_status(paths)
    state = _read_watcher_state(paths)
    preconditions = _build_preconditions(paths, watcher_status)
    status, reason = _process_status(state, preconditions)
    warnings = _merge_codes(player_log_status.get("warnings"), watcher_status.get("warnings"), state["warnings"])
    errors = _merge_codes(player_log_status.get("errors"), watcher_status.get("errors"), state["errors"])
    if reason and status in {"blocked", "unknown"} and reason not in errors:
        errors.append(reason)

    return {
        "object": LIVE_WATCHER_PROCESS_OBJECT,
        "schema_version": LIVE_WATCHER_PROCESS_SCHEMA_VERSION,
        "status": status,
        "process_control": {
            "mode": "safeguards_only",
            "implementation_status": "state_only" if state["exists"] else "not_implemented",
            **{flag: False for flag in _PROCESS_CONTROL_FALSE_FLAGS},
            "reason": reason,
        },
        "watcher": {
            "status": status,
            "running": False,
            "pid_verified": False,
            "single_instance_guard": _single_instance_guard_status(state),
            "supervisor_boundary": "local_app_supervisor_deferred",
        },
        "player_log": _sanitized_player_log_summary(player_log_status),
        "preconditions": preconditions,
        "state": {
            "source": state["source"],
            "exists": state["exists"],
            "status": state["status"],
            "stale": state["stale"],
            "pid_present": state["pid_present"],
            "pid_verified": False,
            "supervisor_token_present": state["supervisor_token_present"],
            "display_path": state["display_path"],
            "raw_path_exposed": False,
        },
        "warnings": warnings,
        "errors": errors,
    }


def _read_watcher_state(paths: LocalAppPaths) -> dict[str, object]:
    display_path = display_app_path("jobs", LIVE_WATCHER_PROCESS_STATE_FILENAME) if paths.jobs_dir is not None else None
    if paths.app_data_root is None or paths.jobs_dir is None:
        return _state_payload(
            source="unavailable",
            exists=False,
            status="not_configured",
            display_path=display_path,
            errors=["app_data_root_unavailable"],
        )

    state_path = paths.jobs_dir / LIVE_WATCHER_PROCESS_STATE_FILENAME
    if not state_path.exists():
        return _state_payload(source="none", exists=False, status="not_initialized", display_path=display_path)
    if not state_path.is_file():
        return _state_payload(
            source="app_data_state_file",
            exists=True,
            status="unknown",
            display_path=display_path,
            errors=["watcher_state_not_file"],
        )

    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return _state_payload(
            source="app_data_state_file",
            exists=True,
            status="unknown",
            display_path=display_path,
            errors=["watcher_state_malformed"],
        )

    if not isinstance(payload, dict):
        return _state_payload(
            source="app_data_state_file",
            exists=True,
            status="unknown",
            display_path=display_path,
            errors=["watcher_state_malformed"],
        )

    pid_present = _safe_positive_int(payload.get("pid"))
    supervisor_token_present = isinstance(payload.get("supervisor_token"), str) and bool(
        str(payload.get("supervisor_token")).strip()
    )
    updated_at = payload.get("updated_at")
    stale = _state_is_stale(updated_at)
    source = "synthetic_test_state" if payload.get("source") == "synthetic_test_state" else "app_data_state_file"
    status = "stale" if stale else "deferred"
    warnings = ["watcher_state_stale"] if stale else []
    return _state_payload(
        source=source,
        exists=True,
        status=status,
        stale=stale,
        pid_present=pid_present,
        supervisor_token_present=supervisor_token_present,
        display_path=display_path,
        warnings=warnings,
    )


def _state_payload(
    *,
    source: str,
    exists: bool,
    status: str,
    display_path: str | None,
    stale: bool = False,
    pid_present: bool = False,
    supervisor_token_present: bool = False,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> dict[str, object]:
    return {
        "source": source,
        "exists": exists,
        "status": status,
        "stale": stale,
        "pid_present": pid_present,
        "supervisor_token_present": supervisor_token_present,
        "display_path": display_path,
        "warnings": warnings or [],
        "errors": errors or [],
    }


def _state_is_stale(value: object) -> bool:
    if not isinstance(value, str):
        return True
    normalized = value.replace("Z", "+00:00")
    try:
        updated_at = datetime.fromisoformat(normalized)
    except ValueError:
        return True
    if updated_at.tzinfo is None:
        updated_at = updated_at.replace(tzinfo=UTC)
    age_seconds = (datetime.now(UTC) - updated_at.astimezone(UTC)).total_seconds()
    return age_seconds < 0 or age_seconds > LIVE_WATCHER_PROCESS_STATE_STALE_SECONDS


def _safe_positive_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _build_preconditions(paths: LocalAppPaths, watcher_status: dict[str, object]) -> list[dict[str, str | None]]:
    watcher = watcher_status.get("watcher", {})
    watcher_reason = None
    watcher_state = "unavailable"
    if isinstance(watcher, dict):
        watcher_reason = watcher.get("reason") if isinstance(watcher.get("reason"), str) else None
        watcher_state = str(watcher.get("status", "unavailable"))

    return [
        _precondition(
            "player_log_ready",
            "pass" if watcher_state == "ready" else "fail",
            None if watcher_state == "ready" else watcher_reason or watcher_state,
        ),
        _precondition(
            "app_data_root_available",
            "pass" if paths.app_data_root is not None else "fail",
            None if paths.app_data_root is not None else "app_data_root_unavailable",
        ),
        _precondition(
            "state_directory_available",
            "pass" if paths.jobs_dir is not None and paths.jobs_dir.is_dir() else "deferred",
            None if paths.jobs_dir is not None and paths.jobs_dir.is_dir() else "state_directory_not_created_by_get",
        ),
        _precondition("single_instance_guard_available", "deferred", "single_instance_guard_deferred"),
        _precondition("supervisor_target_defined", "deferred", "supervisor_target_deferred"),
        _precondition("external_transport_disabled", "pass", None),
        _precondition("live_sqlite_ingest_contract_present", "pass", None),
        _precondition("frontend_controls_authorized", "deferred", "frontend_controls_not_authorized"),
    ]


def _precondition(key: str, status: str, reason: str | None) -> dict[str, str | None]:
    return {"key": key, "status": status, "reason": reason}


def _process_status(
    state: dict[str, object],
    preconditions: list[dict[str, str | None]],
) -> tuple[str, str | None]:
    state_errors = state.get("errors")
    if isinstance(state_errors, list) and state_errors:
        reason = str(state_errors[0])
        return ("blocked" if reason != "app_data_root_unavailable" else "not_configured", reason)
    if state.get("status") == "stale":
        return "stale", "watcher_state_stale"

    preconditions_by_key = {str(entry.get("key")): entry for entry in preconditions}
    player_log_ready = preconditions_by_key["player_log_ready"]
    if player_log_ready["status"] == "fail":
        reason = player_log_ready["reason"] or "player_log_not_ready"
        if reason in {"player_log_missing", "blocked_missing_log"}:
            return "blocked_missing_log", "player_log_missing"
        if reason in {"player_log_config_invalid", "blocked_invalid_config"}:
            return "blocked_invalid_config", "player_log_config_invalid"
        if reason in {"player_log_unreadable", "blocked_unreadable_log"}:
            return "blocked_unreadable_log", "player_log_unreadable"
        if reason in {"player_log_unavailable", "unavailable"}:
            return "not_configured", "player_log_unavailable"
        return "blocked", reason

    if not state.get("exists"):
        return "not_initialized", "watcher_state_missing"
    return "deferred", "watcher_process_control_deferred"


def _single_instance_guard_status(state: dict[str, object]) -> str:
    if state.get("status") == "stale":
        return "stale"
    if state.get("errors"):
        return "unknown"
    if not state.get("exists"):
        return "not_initialized"
    return "deferred"


def _sanitized_player_log_summary(player_log_status: dict[str, object]) -> dict[str, object]:
    player_log = player_log_status.get("player_log", {})
    if not isinstance(player_log, dict):
        player_log = {}
    return {
        "object": LIVE_PLAYER_LOG_STATUS_OBJECT,
        "status": player_log.get("status", "unavailable"),
        "source": player_log.get("source", "unavailable"),
        "display_path": player_log.get("display_path", "<player_log_unavailable>"),
        "path_kind": player_log.get("path_kind", "unavailable"),
        "metadata_access": player_log.get("metadata_access", "unavailable"),
        "exists": bool(player_log.get("exists", False)),
        "contents_read": False,
        "tailing_started": False,
    }


def _merge_codes(*values: Any) -> list[str]:
    codes: list[str] = []
    for value in values:
        if not isinstance(value, list):
            continue
        for entry in value:
            if isinstance(entry, str) and entry not in codes:
                codes.append(entry)
    return codes
