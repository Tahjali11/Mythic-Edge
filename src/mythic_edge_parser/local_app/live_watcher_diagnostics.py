from __future__ import annotations

from collections.abc import Mapping, Sequence

from .live_watcher_process import build_live_watcher_process_status
from .paths import LocalAppPaths
from .setup_status import (
    build_live_player_log_status,
    build_live_sqlite_capture_status,
    build_live_watcher_status,
)

LIVE_WATCHER_DIAGNOSTICS_OBJECT = "mythic_edge_local_app_live_watcher_diagnostics"
LIVE_WATCHER_DIAGNOSTICS_SCHEMA_VERSION = "live_app_watcher_diagnostics.v1"

_DIAGNOSTIC_SEVERITIES = ("info", "warning", "degraded", "error", "blocked")
_SEVERITY_RANK = {"info": 0, "warning": 1, "degraded": 2, "error": 3, "blocked": 4}
_PRIVACY_FLAGS = (
    "raw_player_log_content_included",
    "raw_player_log_path_included",
    "raw_hashes_included",
    "raw_sql_included",
    "stack_traces_included",
    "secrets_or_environment_values_included",
)


def build_live_watcher_diagnostics_status(paths: LocalAppPaths) -> dict[str, object]:
    player_log_status = build_live_player_log_status(paths)
    watcher_status = build_live_watcher_status(paths)
    watcher_process_status = build_live_watcher_process_status(paths)
    live_ingest_status = build_live_sqlite_capture_status(paths)

    diagnostics: list[dict[str, object]] = []
    _extend_player_log_diagnostics(diagnostics, player_log_status)
    _extend_watcher_readiness_diagnostics(diagnostics, watcher_status)
    _extend_watcher_process_diagnostics(diagnostics, watcher_process_status)
    _extend_live_capture_diagnostics(diagnostics, live_ingest_status)
    _extend_tailer_event_bridge_diagnostics(diagnostics)
    _extend_parser_evidence_diagnostics(diagnostics)
    _extend_privacy_boundary_diagnostics(diagnostics)

    summary = _diagnostics_summary(diagnostics)
    privacy = {flag: False for flag in _PRIVACY_FLAGS}
    capabilities = {
        "read_only": True,
        "starts_watcher": False,
        "stops_watcher": False,
        "tails_player_log": False,
        "writes_sqlite": False,
        "writes_diagnostics_files": False,
        "external_transport_allowed": False,
    }
    return {
        "object": LIVE_WATCHER_DIAGNOSTICS_OBJECT,
        "schema_version": LIVE_WATCHER_DIAGNOSTICS_SCHEMA_VERSION,
        "status": _top_level_status(summary),
        "mode": "read_only_composition",
        "summary": summary,
        "diagnostics": diagnostics,
        "sources": {
            "player_log_status": _source_summary(
                player_log_status,
                evidence_availability="metadata_only",
                limitations=["contents_not_read"],
            ),
            "watcher_status": _source_summary(
                watcher_status,
                evidence_availability="metadata_only",
                limitations=["readiness_only"],
            ),
            "watcher_process_status": _source_summary(
                watcher_process_status,
                evidence_availability="metadata_only",
                limitations=["pid_not_exposed", "process_image_name_only", "raw_detector_output_excluded"],
            ),
            "live_ingest_status": _source_summary(
                live_ingest_status,
                evidence_availability="metadata_only",
                limitations=["status_only", "sqlite_not_written"],
            ),
            "tailer_event_bridge": _missing_source_summary(
                status="deferred",
                evidence_availability="deferred",
                limitations=["tailer_not_called"],
            ),
            "parser_diagnostics": _missing_source_summary(
                status="expected_but_unavailable",
                evidence_availability="expected_but_unavailable",
                limitations=["raw_log_report_generation_not_called"],
            ),
            "evidence_runtime_health": _missing_source_summary(
                status="expected_but_unavailable",
                evidence_availability="expected_but_unavailable",
                limitations=["sanitized_health_source_not_supplied"],
            ),
        },
        "privacy": privacy,
        "capabilities": capabilities,
        "warnings": _collect_codes(
            player_log_status.get("warnings"),
            watcher_status.get("warnings"),
            watcher_process_status.get("warnings"),
        ),
        "errors": _collect_codes(
            player_log_status.get("errors"),
            watcher_status.get("errors"),
            watcher_process_status.get("errors"),
        ),
    }


def _extend_player_log_diagnostics(
    diagnostics: list[dict[str, object]],
    player_log_status: Mapping[str, object],
) -> None:
    player_log = player_log_status.get("player_log")
    player_log_state = str(player_log.get("status", "unknown")) if isinstance(player_log, Mapping) else "unknown"
    for label in _string_sequence(player_log_status.get("diagnostics")):
        label = _canonical_player_log_label(label)
        evidence = "deferred" if label.endswith("_deferred") or label == "readability_not_probed" else "metadata_only"
        severity = "info" if evidence == "deferred" else "degraded"
        if label in {"player_log_not_file", "player_log_stale"}:
            severity = "warning"
        _add_diagnostic(
            diagnostics,
            category="player_log_metadata",
            key=label,
            severity=severity,
            status=label,
            evidence_availability=evidence,
            source="player_log_status",
            message=_message_for_label(label),
            review_required=severity in {"degraded", "warning", "blocked", "error"},
        )
    for label in _string_sequence(player_log_status.get("warnings")):
        label = _canonical_player_log_label(label)
        severity = "warning"
        if label in {"player_log_missing", "player_log_unreadable", "player_log_config_invalid"}:
            severity = "blocked"
        _add_diagnostic(
            diagnostics,
            category="player_log_metadata",
            key=label,
            severity=severity,
            status=label,
            evidence_availability="metadata_only",
            source="player_log_status",
            message=_message_for_label(label),
            review_required=True,
        )
    for label in _string_sequence(player_log_status.get("errors")):
        label = _canonical_player_log_label(label)
        _add_diagnostic(
            diagnostics,
            category="player_log_metadata",
            key=label,
            severity="blocked",
            status=label,
            evidence_availability="metadata_only",
            source="player_log_status",
            message=_message_for_label(label),
            review_required=True,
        )
    if player_log_state in {"configured_exists", "detected_exists"}:
        _add_diagnostic(
            diagnostics,
            category="player_log_metadata",
            key="player_log_metadata_available",
            severity="info",
            status=player_log_state,
            evidence_availability="metadata_only",
            source="player_log_status",
            message="Player.log metadata is available without reading log contents.",
            review_required=False,
        )


def _extend_watcher_readiness_diagnostics(
    diagnostics: list[dict[str, object]],
    watcher_status: Mapping[str, object],
) -> None:
    watcher = watcher_status.get("watcher")
    state = str(watcher.get("status", "unknown")) if isinstance(watcher, Mapping) else "unknown"
    label_by_state = {
        "ready": "watcher_ready",
        "not_configured": "watcher_not_configured",
        "blocked_missing_log": "watcher_blocked_missing_log",
        "blocked_unreadable_log": "watcher_blocked_unreadable_log",
        "blocked_invalid_config": "watcher_blocked_invalid_config",
        "unavailable": "watcher_unavailable",
        "deferred": "watcher_deferred",
        "degraded": "watcher_deferred",
    }
    label = label_by_state.get(state, "watcher_deferred")
    severity = "info" if label == "watcher_ready" else "degraded"
    if label.startswith("watcher_blocked") or label in {"watcher_not_configured", "watcher_unavailable"}:
        severity = "blocked"
    _add_diagnostic(
        diagnostics,
        category="watcher_readiness",
        key=label,
        severity=severity,
        status=label,
        evidence_availability="metadata_only",
        source="watcher_status",
        message=_message_for_label(label),
        review_required=severity != "info",
    )


def _extend_watcher_process_diagnostics(
    diagnostics: list[dict[str, object]],
    watcher_process_status: Mapping[str, object],
) -> None:
    state = watcher_process_status.get("state")
    process_control = watcher_process_status.get("process_control")
    state_status = str(state.get("status", "unknown")) if isinstance(state, Mapping) else "unknown"
    reason = str(process_control.get("reason", "")) if isinstance(process_control, Mapping) else ""
    labels: list[str] = []
    if reason in {"watcher_state_missing", "watcher_state_malformed", "watcher_state_stale"}:
        labels.append(reason)
    elif state_status == "not_initialized":
        labels.append("watcher_state_missing")
    elif state_status == "stale":
        labels.append("watcher_state_stale")
    elif state_status == "unknown":
        labels.append("watcher_state_malformed")

    preconditions = watcher_process_status.get("preconditions")
    if isinstance(preconditions, Sequence) and not isinstance(preconditions, (str, bytes)):
        for entry in preconditions:
            if not isinstance(entry, Mapping):
                continue
            key = str(entry.get("key", ""))
            status = str(entry.get("status", ""))
            reason_value = entry.get("reason")
            if status == "deferred" and isinstance(reason_value, str):
                labels.append(reason_value)
            elif key == "single_instance_guard_available" and status == "deferred":
                labels.append("single_instance_guard_deferred")
            elif key == "supervisor_target_defined" and status == "deferred":
                labels.append("supervisor_target_deferred")

    for label in _dedupe(labels):
        severity = "warning"
        if label == "watcher_state_malformed":
            severity = "blocked"
        elif label == "watcher_state_stale":
            severity = "degraded"
        _add_diagnostic(
            diagnostics,
            category="watcher_process",
            key=label,
            severity=severity,
            status=label,
            evidence_availability="metadata_only",
            source="watcher_process_status",
            message=_message_for_label(label),
            review_required=severity != "info",
        )

    mtga_process = watcher_process_status.get("mtga_process")
    mtga_status = str(mtga_process.get("status", "unknown")) if isinstance(mtga_process, Mapping) else "unknown"
    mtga_label_by_status = {
        "detected": "mtga_process_detected",
        "not_detected": "mtga_process_not_detected",
        "unsupported_platform": "mtga_process_detection_unsupported",
        "detector_unavailable": "mtga_detector_unavailable",
    }
    mtga_label = mtga_label_by_status.get(mtga_status, "mtga_process_unknown")
    mtga_severity = "info" if mtga_label == "mtga_process_detected" else "degraded"
    if mtga_label == "mtga_detector_unavailable":
        mtga_severity = "warning"
    _add_diagnostic(
        diagnostics,
        category="mtga_process",
        key=mtga_label,
        severity=mtga_severity,
        status=mtga_status,
        evidence_availability="metadata_only" if mtga_status != "unsupported_platform" else "not_checked",
        source="watcher_process_status",
        message=_message_for_label(mtga_label),
        review_required=mtga_severity != "info",
    )

    automation_readiness = watcher_process_status.get("automation_readiness")
    readiness_status = (
        str(automation_readiness.get("status", "blocked")) if isinstance(automation_readiness, Mapping) else "blocked"
    )
    _add_diagnostic(
        diagnostics,
        category="automation_readiness",
        key="automatic_start_blocked",
        severity="info",
        status=readiness_status,
        evidence_availability="metadata_only",
        source="watcher_process_status",
        message=_message_for_label("automatic_start_blocked"),
        review_required=False,
    )


def _extend_live_capture_diagnostics(
    diagnostics: list[dict[str, object]],
    live_ingest_status: Mapping[str, object],
) -> None:
    _add_diagnostic(
        diagnostics,
        category="live_capture",
        key="live_sqlite_capture_status_only",
        severity="info",
        status=str(live_ingest_status.get("status", "unknown")),
        evidence_availability="metadata_only",
        source="live_ingest_status",
        message="Live SQLite capture is represented as status metadata only.",
        review_required=False,
    )
    capabilities = live_ingest_status.get("capabilities")
    if isinstance(capabilities, Mapping):
        if capabilities.get("final_match_game_fact_capture_supported") is True:
            _add_diagnostic(
                diagnostics,
                category="live_capture",
                key="final_match_game_fact_capture_supported",
                severity="info",
                status="supported",
                evidence_availability="metadata_only",
                source="live_ingest_status",
                message="Final and reconciled match/game fact capture is supported by the live adapter.",
                review_required=False,
            )
        for key, capability_name in (
            ("provisional_fact_capture_supported", "provisional_fact_capture_unsupported"),
            ("gameplay_action_live_capture_supported", "gameplay_action_live_capture_deferred"),
            ("opponent_observation_live_capture_supported", "opponent_observation_live_capture_deferred"),
            ("field_evidence_live_capture_supported", "field_evidence_live_capture_deferred"),
        ):
            if capabilities.get(key) is False:
                _add_diagnostic(
                    diagnostics,
                    category="live_capture",
                    key=capability_name,
                    severity="info",
                    status=capability_name,
                    evidence_availability="deferred",
                    source="live_ingest_status",
                    message=_message_for_label(capability_name),
                    review_required=False,
                )


def _extend_tailer_event_bridge_diagnostics(diagnostics: list[dict[str, object]]) -> None:
    for label in (
        "rotation_detection_deferred",
        "truncation_detection_deferred",
        "duplication_detection_deferred",
    ):
        _add_diagnostic(
            diagnostics,
            category="tailer_event_bridge",
            key=label,
            severity="info",
            status=label,
            evidence_availability="deferred",
            source="tailer_event_bridge",
            message=_message_for_label(label),
            review_required=False,
        )


def _extend_parser_evidence_diagnostics(diagnostics: list[dict[str, object]]) -> None:
    for label, source in (
        ("parser_diagnostics_unavailable", "parser_diagnostics"),
        ("evidence_ledger_health_unavailable", "evidence_runtime_health"),
    ):
        _add_diagnostic(
            diagnostics,
            category="parser_evidence",
            key=label,
            severity="info",
            status=label,
            evidence_availability="expected_but_unavailable",
            source=source,
            message=_message_for_label(label),
            review_required=False,
        )


def _extend_privacy_boundary_diagnostics(diagnostics: list[dict[str, object]]) -> None:
    for label in (
        "raw_player_log_content_excluded",
        "raw_player_log_path_excluded",
        "raw_hashes_excluded",
        "external_transport_disabled",
        "destructive_controls_absent",
    ):
        _add_diagnostic(
            diagnostics,
            category="privacy_boundary",
            key=label,
            severity="info",
            status=label,
            evidence_availability="observed",
            source="privacy_boundary",
            message=_message_for_label(label),
            review_required=False,
        )


def _add_diagnostic(
    diagnostics: list[dict[str, object]],
    *,
    category: str,
    key: str,
    severity: str,
    status: str,
    evidence_availability: str,
    source: str,
    message: str,
    review_required: bool,
    count: int | None = None,
) -> None:
    for existing in diagnostics:
        if existing.get("category") == category and existing.get("key") == key and existing.get("source") == source:
            if _SEVERITY_RANK.get(severity, -1) > _SEVERITY_RANK.get(str(existing.get("severity")), -1):
                existing["severity"] = severity
                existing["status"] = status
                existing["evidence_availability"] = evidence_availability
                existing["message"] = message
                existing["review_required"] = review_required
                existing["count"] = count
            return
    diagnostics.append(
        {
            "category": category,
            "key": key,
            "severity": severity,
            "status": status,
            "evidence_availability": evidence_availability,
            "source": source,
            "message": message,
            "count": count,
            "review_required": review_required,
        }
    )


def _diagnostics_summary(diagnostics: Sequence[Mapping[str, object]]) -> dict[str, int]:
    summary = {f"{severity}_count": 0 for severity in _DIAGNOSTIC_SEVERITIES}
    summary["unknown_count"] = 0
    for diagnostic in diagnostics:
        severity = str(diagnostic.get("severity", "unknown"))
        key = f"{severity}_count"
        if key in summary:
            summary[key] += 1
        else:
            summary["unknown_count"] += 1
    return summary


def _top_level_status(summary: Mapping[str, int]) -> str:
    if summary.get("blocked_count", 0) or summary.get("error_count", 0):
        return "blocked"
    if summary.get("warning_count", 0) or summary.get("degraded_count", 0):
        return "degraded"
    if summary.get("unknown_count", 0):
        return "unknown"
    return "ok"


def _source_summary(
    payload: Mapping[str, object],
    *,
    evidence_availability: str,
    limitations: list[str],
) -> dict[str, object]:
    return {
        "supplied": True,
        "status": str(payload.get("status", "unknown")),
        "schema_version": payload.get("schema_version") if isinstance(payload.get("schema_version"), str) else None,
        "evidence_availability": evidence_availability,
        "limitations": limitations,
    }


def _missing_source_summary(
    *,
    status: str,
    evidence_availability: str,
    limitations: list[str],
) -> dict[str, object]:
    return {
        "supplied": False,
        "status": status,
        "schema_version": None,
        "evidence_availability": evidence_availability,
        "limitations": limitations,
    }


def _collect_codes(*values: object) -> list[str]:
    codes: list[str] = []
    for value in values:
        for entry in _string_sequence(value):
            if entry not in codes:
                codes.append(entry)
    return codes


def _string_sequence(value: object) -> list[str]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [entry for entry in value if isinstance(entry, str)]
    return []


def _dedupe(values: Sequence[str]) -> list[str]:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
    return seen


def _canonical_player_log_label(label: str) -> str:
    labels = {
        "metadata_unavailable": "player_log_metadata_unavailable",
        "not_file": "player_log_not_file",
        "permission_denied": "player_log_metadata_denied",
        "stale": "player_log_stale",
    }
    return labels.get(label, label)


def _message_for_label(label: str) -> str:
    messages = {
        "readability_not_probed": "Readability was not checked because diagnostics do not read Player.log contents.",
        "rotation_detection_deferred": (
            "Rotation detection is deferred until an authorized watcher surface supplies it."
        ),
        "truncation_detection_deferred": (
            "Truncation detection is deferred until an authorized watcher surface supplies it."
        ),
        "duplication_detection_deferred": (
            "Duplicate-line detection is deferred until an authorized watcher surface supplies it."
        ),
        "not_file": "The configured Player.log target is not a file.",
        "stale": "Player.log metadata appears stale.",
        "player_log_missing": "Player.log metadata indicates the file is missing.",
        "player_log_stale": "Player.log metadata indicates stale activity.",
        "player_log_not_file": "Player.log metadata indicates the target is not a file.",
        "player_log_unreadable": "Player.log metadata cannot be read safely.",
        "player_log_metadata_unavailable": "Player.log metadata is unavailable.",
        "player_log_metadata_denied": "Player.log metadata access was denied.",
        "player_log_config_invalid": "Player.log configuration is invalid.",
        "app_data_root_unavailable": "The local app-data root is unavailable.",
        "watcher_ready": "Watcher readiness metadata is ready; capture is not running.",
        "watcher_not_configured": "Watcher readiness is not configured.",
        "watcher_blocked_missing_log": "Watcher readiness is blocked because Player.log is missing.",
        "watcher_blocked_unreadable_log": "Watcher readiness is blocked because Player.log metadata is unreadable.",
        "watcher_blocked_invalid_config": "Watcher readiness is blocked by invalid configuration.",
        "watcher_deferred": "Watcher readiness remains deferred.",
        "watcher_unavailable": "Watcher readiness is unavailable.",
        "watcher_state_missing": "Watcher process state is missing and was not created by diagnostics.",
        "watcher_state_malformed": "Watcher process state is malformed and was not repaired.",
        "watcher_state_stale": "Watcher process state is stale and was not cleaned.",
        "watcher_state_not_file": "Watcher process state is not a file.",
        "single_instance_guard_deferred": "Single-instance guard ownership is deferred.",
        "supervisor_target_deferred": "Supervisor target ownership is deferred.",
        "frontend_controls_not_authorized": "Frontend process controls are not authorized.",
        "watcher_process_control_deferred": "Watcher process control remains deferred.",
        "mtga_process_detected": "MTGA process metadata indicates MTGA.exe is running.",
        "mtga_process_not_detected": "MTGA process metadata does not currently detect MTGA.exe.",
        "mtga_process_detection_unsupported": "MTGA process detection is supported only on Windows in this slice.",
        "mtga_detector_unavailable": "MTGA process detection is unavailable; no raw detector output was included.",
        "mtga_process_unknown": "MTGA process metadata is unavailable.",
        "automatic_start_blocked": "Automatic capture startup remains blocked pending a future contract.",
        "provisional_fact_capture_unsupported": "Provisional live fact capture is unsupported in this slice.",
        "gameplay_action_live_capture_deferred": "Gameplay-action live capture is deferred.",
        "opponent_observation_live_capture_deferred": "Opponent-observation live capture is deferred.",
        "field_evidence_live_capture_deferred": "Field-evidence live capture is deferred.",
        "parser_diagnostics_unavailable": "Parser diagnostics were not generated by this read-only route.",
        "evidence_ledger_health_unavailable": "Evidence runtime health was not supplied to this route.",
        "raw_player_log_content_excluded": "Raw Player.log content is excluded.",
        "raw_player_log_path_excluded": "Raw Player.log paths are excluded.",
        "raw_hashes_excluded": "Raw hashes are excluded.",
        "external_transport_disabled": "External transport is disabled.",
        "destructive_controls_absent": "Destructive controls are absent.",
    }
    return messages.get(label, label.replace("_", " "))
