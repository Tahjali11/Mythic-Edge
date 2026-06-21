from __future__ import annotations

import copy
import re
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

LOCAL_WATCHER_OFFSET_WINDOW_OBJECT = "mythic_edge_local_watcher_offset_window_monitor"
LOCAL_WATCHER_OFFSET_WINDOW_SCHEMA_VERSION = (
    "parser_recovery_local_watcher_offset_window_monitor.v1"
)
LOCAL_WATCHER_SOURCE_OBJECT = "mythic_edge_local_watcher_source_selection"
LOCAL_WATCHER_WINDOW_OBJECT = "mythic_edge_local_watcher_offset_window"
LOCAL_WATCHER_EVENT_OBJECT = "mythic_edge_local_watcher_update_buffer"

SOURCE_CLASSES = (
    "player_log",
    "normalized_utc_log",
    "synthetic_player_log",
    "synthetic_utc_log",
)
PRIVACY_CLASSES = ("synthetic", "public_fixture", "private_local", "local_only_redacted")
SELECTION_MODES = (
    "synthetic_test",
    "operator_selected_local",
    "approved_private_window",
    "blocked_missing_approval",
)
WINDOW_MODES = (
    "read_from_start",
    "tail_from_now",
    "offset_bounded",
    "metadata_only",
    "blocked",
)
SOURCE_GENERATION_STATUSES = (
    "new_source_generation",
    "same_source_generation",
    "rotated_generation",
    "truncated_generation",
    "recreated_generation",
    "archived_generation",
    "deleted_or_unavailable",
    "unknown_generation",
)
WINDOW_STATUSES = (
    "window_ready",
    "window_in_progress",
    "window_closed",
    "window_unavailable",
    "window_stale",
    "window_degraded",
    "window_blocked_missing_approval",
    "window_manual_review_required",
)
OFFSET_RANGE_STATUSES = (
    "offset_range_valid",
    "offset_range_empty",
    "offset_range_unavailable",
    "offset_range_reversed",
    "offset_range_crosses_generation",
    "offset_range_manual_review_required",
)
FILE_TRANSITION_STATUSES = (
    "file_unchanged",
    "file_appended",
    "file_size_decreased",
    "file_recreated",
    "file_rotated_or_archived",
    "file_deleted",
    "file_metadata_unavailable",
)
WATCHER_UPDATE_STATUSES = (
    "update_observed",
    "update_coalesced",
    "update_dropped_due_to_backpressure",
    "update_skipped_stale_window",
    "update_blocked_missing_approval",
    "update_manual_review_required",
)
BACKPRESSURE_STATUSES = (
    "buffer_ok",
    "buffer_near_limit",
    "buffer_over_limit_degraded",
    "buffer_dropped_updates",
    "buffer_unknown",
)
ERROR_STATUSES = (
    "no_error",
    "non_blocking_error",
    "permission_denied",
    "source_disappeared",
    "metadata_unavailable",
    "event_stream_unavailable_polling",
    "polling_unavailable",
    "manual_review_required",
)
REQUIRED_NON_CLAIMS = (
    "not_parser_truth",
    "not_private_harvest_authorization",
    "not_fixture_promotion",
    "not_corpus_status_change",
    "not_parser_behavior_readiness",
    "not_pipeline_activation_readiness",
    "not_field_recovery_readiness",
    "not_watcher_correctness",
    "not_private_smoke_success",
    "not_release_readiness",
    "not_production_behavior",
    "not_analytics_truth",
    "not_ai_truth",
    "not_coaching_truth",
)
FALSE_READINESS_FLAGS = (
    "parser_behavior_ready",
    "pipeline_activation_ready_for_issue_388",
    "private_harvest_authorized",
    "fixture_promotion_authorized",
    "corpus_status_change_authorized",
)

_SOURCE_REQUIRED_FIELDS = (
    "object",
    "schema_version",
    "source_label",
    "source_class",
    "privacy_class",
    "selection_mode",
    "approval_issue",
    "selection_status",
    "contents_read",
    "raw_path_included",
    "raw_hash_included",
)
_WINDOW_REQUIRED_FIELDS = (
    "object",
    "schema_version",
    "window_id",
    "source_label",
    "source_class",
    "privacy_class",
    "source_generation",
    "window_mode",
    "window_status",
    "start_marker_status",
    "end_marker_status",
    "offset_range_status",
    "source_transition_status",
    "source_generation_status",
    "stale_window_status",
    "buffer_status",
    "backpressure_status",
    "error_status",
    "contents_read",
    "local_state_written",
    "raw_path_included",
    "raw_hash_included",
    "synthetic_start_offset",
    "synthetic_end_offset",
    "synthetic_start_size_bytes",
    "synthetic_end_size_bytes",
    "review_required",
    "non_claims",
)
_BUFFER_REQUIRED_FIELDS = (
    "object",
    "schema_version",
    "buffer_capacity",
    "queued_update_count",
    "dropped_update_count",
    "coalesced_update_count",
    "backpressure_status",
    "oldest_update_status",
    "newest_update_status",
    "review_required",
)
_REPORT_REQUIRED_FIELDS = (
    "object",
    "schema_version",
    "source_selection",
    "windows",
    "buffer_summary",
    "parser_behavior_ready",
    "pipeline_activation_ready_for_issue_388",
    "private_harvest_authorized",
    "fixture_promotion_authorized",
    "corpus_status_change_authorized",
    "non_claims",
)

_SYMBOLIC_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]{1,63}$")
_ABSOLUTE_PATH_RE = re.compile(
    r"(?:^|[\s\"':=])/"
    r"|(?:^|[\s\"':=])[A-Za-z]:[\\/]"
    r"|(?:^|[\s\"':=])\\\\"
    r"|file://",
    re.IGNORECASE,
)
_FORBIDDEN_TEXT_RE = re.compile(
    r"(\[UnityCrossThreadLogger\]|\[Client GRE\]|DETAILED LOGS:|"
    r"\bPlayer[.]log\b|\bUTC[_]Log\b|https?://hooks[.]|"
    r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}|"
    r"\b(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{8,})",
    re.IGNORECASE,
)


class OffsetWindowMonitorError(ValueError):
    def __init__(self, status: str, reason: str) -> None:
        super().__init__(reason)
        self.status = status
        self.reason = reason


def describe_source_selection(
    *,
    source_label: str,
    source_class: str,
    privacy_class: str = "synthetic",
    selection_mode: str = "synthetic_test",
    approval_issue: str | None = None,
) -> dict[str, Any]:
    """Describe an explicit symbolic source without touching source contents."""

    _require_symbolic_id(source_label, "source_label")
    _validate_choice(source_class, SOURCE_CLASSES, "source_class")
    _validate_choice(privacy_class, PRIVACY_CLASSES, "privacy_class")
    _validate_choice(selection_mode, SELECTION_MODES, "selection_mode")
    status = (
        "window_blocked_missing_approval"
        if _requires_approval(privacy_class, selection_mode) and not approval_issue
        else "source_selection_ready"
    )
    if status == "window_blocked_missing_approval":
        selection_mode = "blocked_missing_approval"

    return {
        "object": LOCAL_WATCHER_SOURCE_OBJECT,
        "schema_version": LOCAL_WATCHER_OFFSET_WINDOW_SCHEMA_VERSION,
        "source_label": source_label,
        "source_class": source_class,
        "privacy_class": privacy_class,
        "selection_mode": selection_mode,
        "approval_issue": approval_issue,
        "selection_status": status,
        "contents_read": False,
        "raw_path_included": False,
        "raw_hash_included": False,
    }


def capture_synthetic_file_metadata(
    *,
    source_label: str,
    path: Path,
    source_generation: str,
    modified_time_label: str = "synthetic_mtime",
    synthetic_file_token: str | None = None,
    archived: bool = False,
) -> dict[str, Any]:
    """Capture metadata for a synthetic temp file without returning its path."""

    _require_symbolic_id(source_label, "source_label")
    _require_symbolic_id(source_generation, "source_generation")
    _require_symbolic_id(modified_time_label, "modified_time_label")
    if synthetic_file_token is not None:
        _require_symbolic_id(synthetic_file_token, "synthetic_file_token")

    exists = path.exists()
    return {
        "source_label": source_label,
        "source_generation": source_generation,
        "synthetic_file_token": synthetic_file_token or source_generation,
        "size_bytes": path.stat().st_size if exists else None,
        "modified_time_label": modified_time_label,
        "exists": exists,
        "archived": archived,
        "path_included": False,
        "contents_read": False,
    }


def classify_source_transition(
    previous_metadata: Mapping[str, Any] | None,
    current_metadata: Mapping[str, Any] | None,
) -> dict[str, str]:
    """Classify a synthetic metadata-only source transition."""

    if not isinstance(current_metadata, Mapping) or current_metadata.get("exists") is not True:
        return _transition("file_deleted", "deleted_or_unavailable", "source_disappeared")
    if not isinstance(previous_metadata, Mapping) or previous_metadata.get("exists") is not True:
        return _transition("file_metadata_unavailable", "new_source_generation", "no_error")
    if current_metadata.get("archived") is True:
        return _transition("file_rotated_or_archived", "archived_generation", "no_error")
    if previous_metadata.get("source_generation") != current_metadata.get("source_generation"):
        return _transition("file_rotated_or_archived", "rotated_generation", "no_error")
    if previous_metadata.get("synthetic_file_token") != current_metadata.get("synthetic_file_token"):
        return _transition("file_recreated", "recreated_generation", "no_error")

    previous_size = previous_metadata.get("size_bytes")
    current_size = current_metadata.get("size_bytes")
    if not isinstance(previous_size, int) or not isinstance(current_size, int):
        return _transition("file_metadata_unavailable", "unknown_generation", "metadata_unavailable")
    if current_size < previous_size:
        return _transition("file_size_decreased", "truncated_generation", "no_error")
    if current_size > previous_size:
        return _transition("file_appended", "same_source_generation", "no_error")
    return _transition("file_unchanged", "same_source_generation", "no_error")


def start_offset_window(
    *,
    source_selection: Mapping[str, Any],
    start_metadata: Mapping[str, Any] | None,
    window_id: str,
    window_mode: str = "metadata_only",
) -> dict[str, Any]:
    """Start a synthetic metadata-only offset window."""

    source = dict(source_selection)
    _require_symbolic_id(window_id, "window_id")
    _validate_choice(window_mode, WINDOW_MODES, "window_mode")
    errors = validate_source_selection(source)
    if errors:
        return _blocked_window(source, window_id, window_mode, "window_manual_review_required")
    if source.get("selection_status") == "window_blocked_missing_approval":
        return _blocked_window(source, window_id, "blocked", "window_blocked_missing_approval")
    if source.get("privacy_class") not in {"synthetic", "public_fixture"}:
        return _blocked_window(source, window_id, "blocked", "window_manual_review_required")

    metadata = start_metadata if isinstance(start_metadata, Mapping) else {}
    size = metadata.get("size_bytes") if isinstance(metadata.get("size_bytes"), int) else None
    generation = str(metadata.get("source_generation") or "unknown_generation")
    start_offset = 0 if window_mode == "read_from_start" else size
    if window_mode in {"offset_bounded", "metadata_only"}:
        start_offset = size
    return {
        **_base_window(source, window_id, window_mode, generation),
        "window_status": "window_in_progress",
        "start_marker_status": "window_ready" if size is not None else "window_unavailable",
        "end_marker_status": "window_in_progress",
        "offset_range_status": "offset_range_unavailable",
        "source_transition_status": "file_metadata_unavailable",
        "source_generation_status": (
            "new_source_generation" if generation != "unknown_generation" else "unknown_generation"
        ),
        "synthetic_start_offset": start_offset,
        "synthetic_end_offset": None,
        "synthetic_start_size_bytes": size,
        "synthetic_end_size_bytes": None,
        "review_required": size is None,
    }


def finish_offset_window(
    *,
    window: Mapping[str, Any],
    end_metadata: Mapping[str, Any] | None,
    transition: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Finish a synthetic metadata-only offset window."""

    result = copy.deepcopy(dict(window))
    end_size = end_metadata.get("size_bytes") if isinstance(end_metadata, Mapping) else None
    if not isinstance(end_size, int):
        result.update(
            {
                "window_status": "window_degraded",
                "end_marker_status": "window_unavailable",
                "offset_range_status": "offset_range_unavailable",
                "error_status": "metadata_unavailable",
                "review_required": True,
            }
        )
        return result

    transition_result = transition or classify_source_transition(
        {
            "source_generation": result.get("source_generation"),
            "synthetic_file_token": result.get("source_generation"),
            "size_bytes": result.get("synthetic_start_size_bytes"),
            "exists": True,
        },
        end_metadata,
    )
    result["synthetic_end_offset"] = end_size
    result["synthetic_end_size_bytes"] = end_size
    result["end_marker_status"] = "window_ready"
    result["source_transition_status"] = transition_result["source_transition_status"]
    result["source_generation_status"] = transition_result["source_generation_status"]
    result["error_status"] = transition_result["error_status"]

    start_offset = result.get("synthetic_start_offset")
    if result["source_generation_status"] not in {
        "same_source_generation",
        "new_source_generation",
    }:
        result["offset_range_status"] = "offset_range_crosses_generation"
        result["window_status"] = "window_manual_review_required"
        result["review_required"] = True
    elif not isinstance(start_offset, int):
        result["offset_range_status"] = "offset_range_unavailable"
        result["window_status"] = "window_degraded"
        result["review_required"] = True
    elif end_size < start_offset:
        result["offset_range_status"] = "offset_range_reversed"
        result["window_status"] = "window_manual_review_required"
        result["review_required"] = True
    elif end_size == start_offset:
        result["offset_range_status"] = "offset_range_empty"
        result["window_status"] = "window_closed"
        result["review_required"] = False
    else:
        result["offset_range_status"] = "offset_range_valid"
        result["window_status"] = "window_closed"
        result["review_required"] = False
    return result


def summarize_update_buffer(
    *,
    buffer_capacity: int,
    queued_update_count: int,
    dropped_update_count: int = 0,
    coalesced_update_count: int = 0,
) -> dict[str, Any]:
    """Summarize bounded update metadata without processing source contents."""

    counts = [buffer_capacity, queued_update_count, dropped_update_count, coalesced_update_count]
    if any(isinstance(count, bool) or not isinstance(count, int) or count < 0 for count in counts):
        status = "buffer_unknown"
        review_required = True
    elif buffer_capacity == 0:
        status = "buffer_unknown"
        review_required = True
    elif dropped_update_count > 0:
        status = "buffer_dropped_updates"
        review_required = True
    elif queued_update_count > buffer_capacity:
        status = "buffer_over_limit_degraded"
        review_required = True
    elif queued_update_count >= max(1, int(buffer_capacity * 0.8)):
        status = "buffer_near_limit"
        review_required = False
    else:
        status = "buffer_ok"
        review_required = False
    update_status = (
        "update_dropped_due_to_backpressure"
        if dropped_update_count > 0
        else "update_coalesced"
        if coalesced_update_count > 0
        else "update_observed"
    )
    return {
        "object": LOCAL_WATCHER_EVENT_OBJECT,
        "schema_version": LOCAL_WATCHER_OFFSET_WINDOW_SCHEMA_VERSION,
        "buffer_capacity": buffer_capacity,
        "queued_update_count": queued_update_count,
        "dropped_update_count": dropped_update_count,
        "coalesced_update_count": coalesced_update_count,
        "backpressure_status": status,
        "oldest_update_status": update_status,
        "newest_update_status": update_status,
        "review_required": review_required,
    }


def build_offset_window_monitor_report(
    *,
    source_selection: Mapping[str, Any],
    windows: Sequence[Mapping[str, Any]],
    buffer_summary: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "object": LOCAL_WATCHER_OFFSET_WINDOW_OBJECT,
        "schema_version": LOCAL_WATCHER_OFFSET_WINDOW_SCHEMA_VERSION,
        "source_selection": copy.deepcopy(dict(source_selection)),
        "windows": [copy.deepcopy(dict(window)) for window in windows],
        "buffer_summary": copy.deepcopy(
            dict(buffer_summary or summarize_update_buffer(buffer_capacity=1, queued_update_count=0))
        ),
        "parser_behavior_ready": False,
        "pipeline_activation_ready_for_issue_388": False,
        "private_harvest_authorized": False,
        "fixture_promotion_authorized": False,
        "corpus_status_change_authorized": False,
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }


def validate_offset_window_monitor_report(report: Mapping[str, Any]) -> list[str]:
    if not isinstance(report, Mapping):
        return ["report:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(report, _REPORT_REQUIRED_FIELDS, "report"))
    if report.get("object") != LOCAL_WATCHER_OFFSET_WINDOW_OBJECT:
        errors.append("report:invalid_object")
    if report.get("schema_version") != LOCAL_WATCHER_OFFSET_WINDOW_SCHEMA_VERSION:
        errors.append("report:invalid_schema_version")
    for flag in FALSE_READINESS_FLAGS:
        if report.get(flag) is not False:
            errors.append(f"report:{flag}_must_remain_false")
    errors.extend(_validate_non_claims(report.get("non_claims"), "report:non_claims"))
    errors.extend(
        f"report:source_selection:{error}"
        for error in validate_source_selection(report.get("source_selection"))
    )
    windows = report.get("windows")
    if not isinstance(windows, list):
        errors.append("report:windows_not_list")
    else:
        for index, window in enumerate(windows):
            errors.extend(
                f"report:windows[{index}]:{error}"
                for error in validate_offset_window(window if isinstance(window, Mapping) else {})
            )
    errors.extend(
        f"report:buffer_summary:{error}"
        for error in validate_update_buffer_summary(report.get("buffer_summary"))
    )
    errors.extend(_privacy_errors(report, "report"))
    return _dedupe_errors(errors)


def validate_source_selection(source_selection: Any) -> list[str]:
    if not isinstance(source_selection, Mapping):
        return ["source:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(source_selection, _SOURCE_REQUIRED_FIELDS, "source"))
    if source_selection.get("object") != LOCAL_WATCHER_SOURCE_OBJECT:
        errors.append("source:invalid_object")
    if source_selection.get("schema_version") != LOCAL_WATCHER_OFFSET_WINDOW_SCHEMA_VERSION:
        errors.append("source:invalid_schema_version")
    _validate_symbolic_value(source_selection.get("source_label"), "source:source_label", errors)
    _validate_choice_error(source_selection.get("source_class"), SOURCE_CLASSES, "source:source_class", errors)
    _validate_choice_error(source_selection.get("privacy_class"), PRIVACY_CLASSES, "source:privacy_class", errors)
    _validate_choice_error(
        source_selection.get("selection_mode"),
        SELECTION_MODES,
        "source:selection_mode",
        errors,
    )
    for flag in ("contents_read", "raw_path_included", "raw_hash_included"):
        if source_selection.get(flag) is not False:
            errors.append(f"source:{flag}_must_remain_false")
    if _requires_approval(
        str(source_selection.get("privacy_class")),
        str(source_selection.get("selection_mode")),
    ) and not source_selection.get("approval_issue"):
        errors.append("source:missing_approval_issue")
    errors.extend(_privacy_errors(source_selection, "source"))
    return _dedupe_errors(errors)


def validate_offset_window(window: Any) -> list[str]:
    if not isinstance(window, Mapping):
        return ["window:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(window, _WINDOW_REQUIRED_FIELDS, "window"))
    if window.get("object") != LOCAL_WATCHER_WINDOW_OBJECT:
        errors.append("window:invalid_object")
    if window.get("schema_version") != LOCAL_WATCHER_OFFSET_WINDOW_SCHEMA_VERSION:
        errors.append("window:invalid_schema_version")
    _validate_symbolic_value(window.get("window_id"), "window:window_id", errors)
    _validate_symbolic_value(window.get("source_label"), "window:source_label", errors)
    _validate_symbolic_value(
        window.get("source_generation"),
        "window:source_generation",
        errors,
    )
    _validate_choice_error(window.get("source_class"), SOURCE_CLASSES, "window:source_class", errors)
    _validate_choice_error(window.get("privacy_class"), PRIVACY_CLASSES, "window:privacy_class", errors)
    _validate_choice_error(window.get("window_mode"), WINDOW_MODES, "window:window_mode", errors)
    _validate_choice_error(window.get("window_status"), WINDOW_STATUSES, "window:window_status", errors)
    _validate_choice_error(
        window.get("start_marker_status"),
        WINDOW_STATUSES,
        "window:start_marker_status",
        errors,
    )
    _validate_choice_error(
        window.get("end_marker_status"),
        WINDOW_STATUSES,
        "window:end_marker_status",
        errors,
    )
    _validate_choice_error(
        window.get("offset_range_status"),
        OFFSET_RANGE_STATUSES,
        "window:offset_range_status",
        errors,
    )
    _validate_choice_error(
        window.get("source_transition_status"),
        FILE_TRANSITION_STATUSES,
        "window:source_transition_status",
        errors,
    )
    _validate_choice_error(
        window.get("source_generation_status"),
        SOURCE_GENERATION_STATUSES,
        "window:source_generation_status",
        errors,
    )
    _validate_choice_error(
        window.get("stale_window_status"),
        WINDOW_STATUSES,
        "window:stale_window_status",
        errors,
    )
    _validate_choice_error(
        window.get("buffer_status"),
        BACKPRESSURE_STATUSES,
        "window:buffer_status",
        errors,
    )
    _validate_choice_error(
        window.get("backpressure_status"),
        BACKPRESSURE_STATUSES,
        "window:backpressure_status",
        errors,
    )
    _validate_choice_error(window.get("error_status"), ERROR_STATUSES, "window:error_status", errors)
    for flag in ("contents_read", "local_state_written", "raw_path_included", "raw_hash_included"):
        if window.get(flag) is not False:
            errors.append(f"window:{flag}_must_remain_false")
    if not isinstance(window.get("review_required"), bool):
        errors.append("window:review_required_not_bool")
    errors.extend(_validate_non_claims(window.get("non_claims"), "window:non_claims"))
    if window.get("privacy_class") not in {"synthetic", "public_fixture"}:
        for field in (
            "synthetic_start_offset",
            "synthetic_end_offset",
            "synthetic_start_size_bytes",
            "synthetic_end_size_bytes",
        ):
            if window.get(field) is not None:
                errors.append(f"window:{field}_must_be_redacted_for_non_synthetic")
    errors.extend(_privacy_errors(window, "window"))
    return _dedupe_errors(errors)


def validate_update_buffer_summary(buffer_summary: Any) -> list[str]:
    if not isinstance(buffer_summary, Mapping):
        return ["buffer:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(buffer_summary, _BUFFER_REQUIRED_FIELDS, "buffer"))
    if buffer_summary.get("object") != LOCAL_WATCHER_EVENT_OBJECT:
        errors.append("buffer:invalid_object")
    if buffer_summary.get("schema_version") != LOCAL_WATCHER_OFFSET_WINDOW_SCHEMA_VERSION:
        errors.append("buffer:invalid_schema_version")
    _validate_choice_error(
        buffer_summary.get("backpressure_status"),
        BACKPRESSURE_STATUSES,
        "buffer:backpressure_status",
        errors,
    )
    _validate_choice_error(
        buffer_summary.get("oldest_update_status"),
        WATCHER_UPDATE_STATUSES,
        "buffer:oldest_update_status",
        errors,
    )
    _validate_choice_error(
        buffer_summary.get("newest_update_status"),
        WATCHER_UPDATE_STATUSES,
        "buffer:newest_update_status",
        errors,
    )
    for field in (
        "buffer_capacity",
        "queued_update_count",
        "dropped_update_count",
        "coalesced_update_count",
    ):
        if (
            isinstance(buffer_summary.get(field), bool)
            or not isinstance(buffer_summary.get(field), int)
            or buffer_summary.get(field) < 0
        ):
            errors.append(f"buffer:{field}_invalid")
    if not isinstance(buffer_summary.get("review_required"), bool):
        errors.append("buffer:review_required_not_bool")
    errors.extend(_privacy_errors(buffer_summary, "buffer"))
    return _dedupe_errors(errors)


def _base_window(
    source: Mapping[str, Any], window_id: str, window_mode: str, source_generation: str
) -> dict[str, Any]:
    return {
        "object": LOCAL_WATCHER_WINDOW_OBJECT,
        "schema_version": LOCAL_WATCHER_OFFSET_WINDOW_SCHEMA_VERSION,
        "window_id": window_id,
        "source_label": source.get("source_label"),
        "source_class": source.get("source_class"),
        "privacy_class": source.get("privacy_class"),
        "source_generation": source_generation,
        "window_mode": window_mode,
        "window_status": "window_in_progress",
        "start_marker_status": "window_unavailable",
        "end_marker_status": "window_unavailable",
        "offset_range_status": "offset_range_unavailable",
        "source_transition_status": "file_metadata_unavailable",
        "source_generation_status": "unknown_generation",
        "stale_window_status": "window_in_progress",
        "buffer_status": "buffer_ok",
        "backpressure_status": "buffer_ok",
        "error_status": "no_error",
        "contents_read": False,
        "local_state_written": False,
        "raw_path_included": False,
        "raw_hash_included": False,
        "synthetic_start_offset": None,
        "synthetic_end_offset": None,
        "synthetic_start_size_bytes": None,
        "synthetic_end_size_bytes": None,
        "review_required": False,
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }


def _blocked_window(
    source: Mapping[str, Any], window_id: str, window_mode: str, window_status: str
) -> dict[str, Any]:
    return {
        **_base_window(source, window_id, window_mode, "unknown_generation"),
        "window_status": window_status,
        "start_marker_status": window_status,
        "end_marker_status": window_status,
        "offset_range_status": "offset_range_unavailable",
        "error_status": "manual_review_required",
        "review_required": True,
    }


def _transition(
    source_transition_status: str, source_generation_status: str, error_status: str
) -> dict[str, str]:
    return {
        "source_transition_status": source_transition_status,
        "source_generation_status": source_generation_status,
        "error_status": error_status,
    }


def _requires_approval(privacy_class: str, selection_mode: str) -> bool:
    return privacy_class in {"private_local", "local_only_redacted"} and selection_mode not in {
        "approved_private_window",
        "blocked_missing_approval",
    }


def _require_symbolic_id(value: str, label: str) -> None:
    if not isinstance(value, str) or _SYMBOLIC_ID_RE.fullmatch(value) is None:
        raise OffsetWindowMonitorError("blocked_forbidden_artifact", f"{label} must be symbolic")
    if _ABSOLUTE_PATH_RE.search(value) or _FORBIDDEN_TEXT_RE.search(value):
        raise OffsetWindowMonitorError("blocked_forbidden_artifact", f"{label} must be symbolic")


def _validate_symbolic_value(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or _SYMBOLIC_ID_RE.fullmatch(value) is None:
        errors.append(f"{label}:invalid_symbolic_value")
        return
    if _ABSOLUTE_PATH_RE.search(value) or _FORBIDDEN_TEXT_RE.search(value):
        errors.append(f"{label}:invalid_symbolic_value")


def _validate_choice(value: str, choices: Sequence[str], label: str) -> None:
    if value not in choices:
        raise OffsetWindowMonitorError("manual_review_required", f"{label} outside vocabulary")


def _validate_choice_error(
    value: Any, choices: Sequence[str], label: str, errors: list[str]
) -> None:
    if value not in choices:
        errors.append(f"{label}:unknown_value")


def _missing_required_fields(value: Mapping[str, Any], fields: Sequence[str], label: str) -> list[str]:
    return [f"{label}:missing:{field}" for field in fields if field not in value]


def _validate_non_claims(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        return [f"{label}_not_list"]
    if tuple(value) != REQUIRED_NON_CLAIMS:
        return [f"{label}:mismatch"]
    return []


def _privacy_errors(value: Any, label: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            errors.extend(_privacy_errors(item, f"{label}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(_privacy_errors(item, f"{label}[{index}]"))
    elif isinstance(value, str):
        if _ABSOLUTE_PATH_RE.search(value):
            errors.append(f"privacy:absolute_path:{label}")
        if _FORBIDDEN_TEXT_RE.search(value):
            errors.append(f"privacy:forbidden_text:{label}")
    return errors


def _dedupe_errors(errors: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(errors))
