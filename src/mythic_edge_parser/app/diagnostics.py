from __future__ import annotations

import json
import logging
import re
import sys
import traceback
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .config import ACTIVE_SUBMITTED_DECK_PATH, BAD_EVENTS_ROOT, FAILED_POSTS_ROOT, RUNTIME_LOGS_ROOT, STATUS_ROOT

_LOGGER_NAME = "manasight"
_LOGGER_CONFIGURED = False
_RUNTIME_LOG_PATH: Path | None = None
_STATUS_PATH: Path | None = None
_STATUS_STATE: dict[str, Any] = {}
_URL_PATTERN = re.compile(r"https?://[^\s)>\]}\"]+")


def reset_diagnostics_runtime_state() -> None:
    global _LOGGER_CONFIGURED, _RUNTIME_LOG_PATH, _STATUS_PATH

    _close_logger_handlers(logging.getLogger(_LOGGER_NAME))
    _LOGGER_CONFIGURED = False
    _RUNTIME_LOG_PATH = None
    _STATUS_PATH = None
    _STATUS_STATE.clear()


def setup_runtime_logging() -> logging.Logger:
    global _LOGGER_CONFIGURED, _RUNTIME_LOG_PATH, _STATUS_PATH

    logger = logging.getLogger(_LOGGER_NAME)
    if _LOGGER_CONFIGURED:
        return logger

    runtime_dt = datetime.now()
    _RUNTIME_LOG_PATH = _runtime_log_path(runtime_dt)
    _STATUS_PATH = _ensure_status_path()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(_RUNTIME_LOG_PATH, encoding="utf-8")
    file_handler.setFormatter(formatter)

    _close_logger_handlers(logger)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    _LOGGER_CONFIGURED = True
    _initialize_runtime_status(runtime_dt)
    logger.info("Runtime logging ready: %s", _RUNTIME_LOG_PATH)
    return logger


def _initialize_runtime_status(runtime_dt: datetime) -> None:
    update_runtime_status(
        started_at=runtime_dt.astimezone(UTC).isoformat(),
        runtime_log_path=str(_RUNTIME_LOG_PATH),
        status="starting",
        webhook_successes=0,
        webhook_failures=0,
        event_failures=0,
        router_failures=0,
    )


def _runtime_log_path(runtime_dt: datetime) -> Path:
    folder = RUNTIME_LOGS_ROOT / _daily_folder_name(runtime_dt)
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "manasight_runtime.log"


def _ensure_status_path() -> Path:
    global _STATUS_PATH

    if _STATUS_PATH is None:
        STATUS_ROOT.mkdir(parents=True, exist_ok=True)
        _STATUS_PATH = STATUS_ROOT / "manasight_status_latest.json"
    return _STATUS_PATH


def _close_logger_handlers(logger: logging.Logger) -> None:
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


def get_logger(name: str | None = None) -> logging.Logger:
    setup_runtime_logging()
    if not name:
        return logging.getLogger(_LOGGER_NAME)
    return logging.getLogger(f"{_LOGGER_NAME}.{name}")


def current_runtime_log_path() -> Path | None:
    return _RUNTIME_LOG_PATH


def current_status_path() -> Path | None:
    return _STATUS_PATH


def current_active_submitted_deck_path() -> Path:
    return ACTIVE_SUBMITTED_DECK_PATH


def redact_url(url: str | None) -> str:
    target = str(url or "").strip()
    if not target:
        return "[NOT SET]"

    parsed = urlparse(target)
    if not parsed.scheme or not parsed.netloc:
        return "[INVALID URL]"

    tail = parsed.path.rsplit("/", 1)[-1] if parsed.path else ""
    if tail:
        return f"{parsed.scheme}://{parsed.netloc}/.../{tail}"
    return f"{parsed.scheme}://{parsed.netloc}"


def sanitize_sensitive_text(value: Any) -> str:
    text = str(value or "")
    if not text:
        return text
    return _URL_PATTERN.sub(lambda match: redact_url(match.group(0)), text)


def update_runtime_status(**fields: Any) -> Path | None:
    status_path = _ensure_status_path()
    normalized_fields = _normalized_status_fields(fields)
    _STATUS_STATE.update(normalized_fields)
    _STATUS_STATE["updated_at"] = datetime.now(UTC).isoformat()

    status_path.write_text(
        json.dumps(_STATUS_STATE, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return status_path


def _normalized_status_fields(fields: dict[str, Any]) -> dict[str, Any]:
    return {
        key: _safe_json_value(value)
        for key, value in fields.items()
        if value is not None
    }


def record_submitted_deck(
    submit_payload: dict[str, Any],
    *,
    match_id: Any = "",
    game_number: Any = "",
    event_timestamp: Any = None,
) -> Path | None:
    payload = _submitted_deck_payload(
        submit_payload,
        match_id=match_id,
        game_number=game_number,
        event_timestamp=event_timestamp,
    )
    if payload is None:
        return None

    path = current_active_submitted_deck_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    update_runtime_status(
        active_submitted_deck_path=str(path),
        active_submitted_deck_updated_at=payload["updated_at"],
        active_submitted_deck_submitted_at=payload["submitted_at"],
        active_submitted_deck_signature=payload["signature"],
        active_submitted_deck_mainboard_count=payload["mainboard_count"],
        active_submitted_deck_sideboard_count=payload["sideboard_count"],
    )
    return path


def _submitted_deck_payload(
    submit_payload: dict[str, Any],
    *,
    match_id: Any,
    game_number: Any,
    event_timestamp: Any,
) -> dict[str, Any] | None:
    deck_cards = normalize_int_list(submit_payload.get("deck_cards") or [])
    sideboard_cards = normalize_int_list(submit_payload.get("sideboard_cards") or [])
    if not deck_cards and not sideboard_cards:
        return None

    submitted_at = _safe_json_value(event_timestamp) or datetime.now(UTC).isoformat()
    signature = submitted_deck_signature(deck_cards, sideboard_cards)
    return {
        "object": "manasight_active_submitted_deck",
        "updated_at": datetime.now(UTC).isoformat(),
        "submitted_at": submitted_at,
        "signature": signature,
        "match_id": str(match_id or "").strip(),
        "game_number": _safe_json_value(game_number),
        "game_state_id": _safe_json_value(submit_payload.get("game_state_id")),
        "resp_id": _safe_json_value(submit_payload.get("resp_id")),
        "request_id": _safe_json_value(submit_payload.get("request_id")),
        "mainboard_count": len(deck_cards),
        "sideboard_count": len(sideboard_cards),
        "deck_cards": deck_cards,
        "sideboard_cards": sideboard_cards,
    }


def mark_event_seen(event: Any, *, match_id: Any = "", game_number: Any = "", player_team: Any = "") -> Path | None:
    metadata = getattr(event, "metadata", None)
    return update_runtime_status(
        status="running",
        last_event_kind=getattr(event, "kind", ""),
        last_event_at=_safe_json_value(getattr(metadata, "timestamp", None)),
        current_match_id=match_id,
        current_game_number=game_number,
        current_player_team=player_team,
    )


def mark_webhook_success(row: dict[str, Any], *, attempts: int) -> Path | None:
    return update_runtime_status(
        webhook_successes=_incremented_status_counter("webhook_successes"),
        last_webhook_ok_at=datetime.now(UTC).isoformat(),
        last_webhook_attempts=attempts,
        last_webhook_event_family=row.get("event_family", ""),
        last_webhook_event_type=row.get("event_type", ""),
        last_webhook_match_id=row.get("match_id", row.get("MTGA Match ID", "")),
    )


def mark_webhook_failure(row: dict[str, Any], exc: Exception, *, attempts: int) -> Path | None:
    return _record_error_status(
        counter_key="webhook_failures",
        error_key_base="last_webhook_error",
        exc=exc,
        last_webhook_event_family=row.get("event_family", ""),
        last_webhook_event_type=row.get("event_type", ""),
        last_webhook_match_id=row.get("match_id", row.get("MTGA Match ID", "")),
        last_webhook_attempts=attempts,
    )


def record_failed_post(row: dict[str, Any], exc: Exception, *, response_text: str = "") -> Path:
    record = {
        "captured_at": datetime.now(UTC).isoformat(),
        "error_type": type(exc).__name__,
        "error": sanitize_sensitive_text(exc),
        "response_text": response_text,
        "row": _safe_json_value(row),
        "traceback": traceback.format_exc(),
    }
    return _append_jsonl_record(FAILED_POSTS_ROOT, "failed_posts", record)


def record_event_failure(event: Any, exc: Exception, *, stage: str) -> Path:
    metadata = getattr(event, "metadata", None)
    record = {
        "captured_at": datetime.now(UTC).isoformat(),
        "stage": stage,
        "error_type": type(exc).__name__,
        "error": sanitize_sensitive_text(exc),
        "event_kind": getattr(event, "kind", ""),
        "event_payload": _safe_json_value(getattr(event, "payload", {})),
        "event_timestamp": _safe_json_value(getattr(metadata, "timestamp", None)),
        "raw_bytes_hash": getattr(metadata, "raw_bytes_hash", ""),
        "traceback": traceback.format_exc(),
    }
    _record_error_status(
        counter_key="event_failures",
        error_key_base="last_event_error",
        exc=exc,
        status="running_with_errors",
        last_event_error_stage=stage,
        last_event_error_kind=getattr(event, "kind", ""),
    )
    return _append_jsonl_record(BAD_EVENTS_ROOT, "bad_events", record)


def record_router_failure(entry: Any, exc: Exception) -> Path:
    record = {
        "captured_at": datetime.now(UTC).isoformat(),
        "stage": "router",
        "error_type": type(exc).__name__,
        "error": sanitize_sensitive_text(exc),
        "entry_header": str(getattr(getattr(entry, "header", None), "value", getattr(entry, "header", ""))),
        "entry_body": _safe_json_value(getattr(entry, "body", "")),
        "traceback": traceback.format_exc(),
    }
    _record_error_status(
        counter_key="router_failures",
        error_key_base="last_router_error",
        exc=exc,
        status="running_with_errors",
    )
    return _append_jsonl_record(BAD_EVENTS_ROOT, "bad_entries", record)


def _record_error_status(
    *,
    counter_key: str,
    error_key_base: str,
    exc: Exception,
    status: str = "running",
    **fields: Any,
) -> Path | None:
    return update_runtime_status(
        **fields,
        **{
            counter_key: _incremented_status_counter(counter_key),
            "status": status,
            f"{error_key_base}_at": datetime.now(UTC).isoformat(),
            f"{error_key_base}_type": type(exc).__name__,
            error_key_base: sanitize_sensitive_text(exc),
        },
    )


def _incremented_status_counter(counter_key: str) -> int:
    return _status_int_value(counter_key) + 1


def _status_int_value(counter_key: str) -> int:
    try:
        value = _STATUS_STATE.get(counter_key, 0)
        if isinstance(value, bool):
            return int(value)
        return int(value)
    except (TypeError, ValueError):
        return 0


def _append_jsonl_record(root: Path, prefix: str, record: dict[str, Any]) -> Path:
    now = datetime.now()
    folder = root / _daily_folder_name(now)
    folder.mkdir(parents=True, exist_ok=True)
    out_path = folder / f"{prefix}_{_daily_folder_name(now)}.jsonl"
    with out_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        handle.flush()
    return out_path


def _daily_folder_name(dt: datetime) -> str:
    return dt.strftime("%m_%d_%y")


def _safe_json_value(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, bytes):
        return {"type": "bytes", "length": len(value)}
    if isinstance(value, dict):
        return {str(key): _safe_json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_safe_json_value(item) for item in value]
    return str(value)


def normalize_int_list(values: list[Any]) -> list[int]:
    normalized: list[int] = []
    for value in values:
        if isinstance(value, bool):
            continue
        try:
            normalized.append(int(value))
        except (TypeError, ValueError):
            continue
    return normalized


def submitted_deck_signature(deck_cards: list[int], sideboard_cards: list[int]) -> str:
    payload = json.dumps(
        {"deck_cards": deck_cards, "sideboard_cards": sideboard_cards},
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(payload).hexdigest()[:16]
