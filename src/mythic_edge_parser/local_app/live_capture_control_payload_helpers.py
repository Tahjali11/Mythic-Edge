from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime

LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION = "live_app_capture_heartbeat_no_row_diagnostics.v1"
LIVE_CAPTURE_STATE_STALE_SECONDS = 15 * 60
LIVE_CAPTURE_HEARTBEAT_STALE_SECONDS = 30
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


def _precondition(key: str, status: str, reason: str | None) -> dict[str, str | None]:
    return {"key": key, "status": status, "reason": reason}


def _first_blocking_precondition(preconditions: list[dict[str, str | None]]) -> str | None:
    for entry in preconditions:
        if entry["status"] == "fail":
            return entry["reason"] or str(entry["key"])
    return None


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
    return _iso_datetime(datetime.now(UTC))


def _iso_datetime(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


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


def _merge_safe_codes(*values: list[str]) -> list[str]:
    codes: list[str] = []
    for value in values:
        for entry in value:
            if entry not in codes:
                codes.append(entry)
    return codes


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
