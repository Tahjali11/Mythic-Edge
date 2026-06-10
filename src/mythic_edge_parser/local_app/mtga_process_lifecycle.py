from __future__ import annotations

import platform
import subprocess
from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from typing import Any

MTGA_PROCESS_STATUS_OBJECT = "mythic_edge_local_app_mtga_process_status"
MTGA_PROCESS_SCHEMA_VERSION = "live_app_mtga_process_detection_shutdown_readiness_gate.v1"
MTGA_PROCESS_NAME = "MTGA.exe"
MTGA_PROCESS_DETECTOR = "windows_tasklist_image_name"
MTGA_RECONNECT_WINDOW_SECONDS = 45
MTGA_PROCESS_DETECTOR_TIMEOUT_SECONDS = 2

_AUTOMATION_READINESS_KEYS = (
    "manual_start_dashboard",
    "manual_stop_dashboard",
    "starting_cannot_dead_end",
    "capturing_persistent_stop_action",
    "stale_capture_recovery_actionable",
    "analytics_refresh_after_completed_match",
    "mtga_process_detected",
    "mtga_disappearance_detected",
    "reconnect_window_verified",
    "shutdown_returns_ready_to_start",
    "shutdown_preserves_completed_facts",
    "shutdown_privacy_boundary_verified",
    "readiness_recorded_in_contract_or_report",
)


def build_mtga_process_status(
    *,
    runner: Callable[..., Any] | None = None,
    platform_system: Callable[[], str] | None = None,
    checked_at: datetime | None = None,
) -> dict[str, object]:
    system = (platform_system or platform.system)().strip().lower()
    now = _iso_datetime(checked_at or datetime.now(UTC))
    if system != "windows":
        return _process_status(
            status="unsupported_platform",
            detected=False,
            platform_label="non_windows",
            evidence="not_checked",
            checked_at=now,
            warnings=["mtga_process_detection_unsupported"],
        )

    command = ["tasklist", "/FI", f"IMAGENAME eq {MTGA_PROCESS_NAME}", "/NH"]
    run = runner or subprocess.run
    run_kwargs: dict[str, object] = {
        "capture_output": True,
        "text": True,
        "timeout": MTGA_PROCESS_DETECTOR_TIMEOUT_SECONDS,
        "shell": False,
    }
    creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", None)
    if creation_flags is not None:
        run_kwargs["creationflags"] = creation_flags

    try:
        result = run(command, **run_kwargs)
    except (FileNotFoundError, OSError, subprocess.SubprocessError, subprocess.TimeoutExpired):
        return _process_status(
            status="detector_unavailable",
            detected=False,
            platform_label="windows",
            evidence="detector_error",
            checked_at=now,
            errors=["mtga_detector_unavailable"],
        )

    return_code = getattr(result, "returncode", 0)
    if not isinstance(return_code, int) or return_code != 0:
        return _process_status(
            status="detector_unavailable",
            detected=False,
            platform_label="windows",
            evidence="detector_error",
            checked_at=now,
            errors=["mtga_detector_unavailable"],
        )

    detected = _tasklist_output_has_mtga(str(getattr(result, "stdout", "") or ""))
    return _process_status(
        status="detected" if detected else "not_detected",
        detected=detected,
        platform_label="windows",
        evidence="image_name_match" if detected else "image_name_absent",
        checked_at=now,
        warnings=[] if detected else ["mtga_not_detected"],
    )


def build_automation_readiness(mtga_process: Mapping[str, object] | None = None) -> dict[str, object]:
    process_status = str(mtga_process.get("status", "unknown") if isinstance(mtga_process, Mapping) else "unknown")
    detected_status = "pass" if process_status == "detected" else "not_proven"
    item_statuses = {
        "manual_start_dashboard": "pass",
        "manual_stop_dashboard": "pass",
        "starting_cannot_dead_end": "pass",
        "capturing_persistent_stop_action": "pass",
        "stale_capture_recovery_actionable": "pass",
        "analytics_refresh_after_completed_match": "pass",
        "mtga_process_detected": detected_status,
        "readiness_recorded_in_contract_or_report": "pass",
    }
    return {
        "schema_version": MTGA_PROCESS_SCHEMA_VERSION,
        "status": "blocked",
        "automatic_start_allowed": False,
        "items": [
            {"key": key, "status": item_statuses.get(key, "not_proven")} for key in _AUTOMATION_READINESS_KEYS
        ],
    }


def _process_status(
    *,
    status: str,
    detected: bool,
    platform_label: str,
    evidence: str,
    checked_at: str,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> dict[str, object]:
    return {
        "object": MTGA_PROCESS_STATUS_OBJECT,
        "schema_version": MTGA_PROCESS_SCHEMA_VERSION,
        "status": status,
        "detected": detected,
        "platform": platform_label,
        "process_name": MTGA_PROCESS_NAME,
        "evidence": evidence,
        "checked_at": checked_at,
        "detector": MTGA_PROCESS_DETECTOR,
        "warnings": warnings or [],
        "errors": errors or [],
        "privacy": {
            "pid_exposed": False,
            "command_line_exposed": False,
            "environment_exposed": False,
            "raw_detector_output_exposed": False,
        },
    }


def _tasklist_output_has_mtga(output: str) -> bool:
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped or stripped.upper().startswith("INFO:"):
            continue
        first_column = stripped.split(maxsplit=1)[0].strip('"')
        if first_column.casefold() == MTGA_PROCESS_NAME.casefold():
            return True
    return False


def _iso_datetime(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
