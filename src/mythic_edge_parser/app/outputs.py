# Imports
import json
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from queue import Empty, Queue
from typing import Any, Callable

import requests

from . import state
from .config import MATCH_LOGS_ROOT, OUT_FILENAME_PREFIX, WEBHOOK_URL
from .diagnostics import (
    get_logger,
    mark_webhook_failure,
    mark_webhook_success,
    record_failed_post,
    redact_url,
    update_runtime_status,
)

_WEBHOOK_MAX_ATTEMPTS = 3
_WEBHOOK_RETRYABLE_STATUS_CODES = {408, 425, 429, 500, 502, 503, 504}
_WEBHOOK_BACKOFF_SECONDS = (0.5, 1.5)
_QUIET_SUCCESS_EVENT_FAMILIES = {
    "ActionLogRow",
    "ParserStatusRow",
    "DeckSnapshotRow",
    "CollectionSnapshotRow",
    "CardPerformanceRow",
}


@dataclass(slots=True)
class WebhookDispatchJob:
    row: dict[str, Any]
    row_key: str
    on_success: Callable[[], None] | None = None
    on_failure: Callable[[], None] | None = None


@dataclass(slots=True)
class WebhookDispatchResult:
    job: WebhookDispatchJob
    success: bool


_DISPATCH_QUEUE: Queue[WebhookDispatchJob | None] = Queue()
_DISPATCH_RESULTS: Queue[WebhookDispatchResult] = Queue()
_DISPATCH_THREAD: threading.Thread | None = None
_DISPATCH_LOCK = threading.Lock()
_PENDING_ROW_KEYS: set[str] = set()


def reset_outputs_runtime_state() -> None:
    global _DISPATCH_THREAD

    stop_webhook_dispatcher(wait_for_queue=False)
    _drain_queue_without_processing()
    _drain_results_without_callbacks()
    with _DISPATCH_LOCK:
        _PENDING_ROW_KEYS.clear()
    _DISPATCH_THREAD = None
    update_runtime_status(webhook_dispatcher_active=False)


def webhook_target_display(url: str | None = None) -> str:
    return redact_url(url if url is not None else WEBHOOK_URL or "")


# Send one row to Google Sheets through the webhook.
def post_row_to_google_sheets(row: dict[str, Any]) -> bool:
    logger = get_logger("webhook")

    if not WEBHOOK_URL:
        logger.warning("POST skipped: webhook URL not set")
        return False

    last_error: Exception | None = None
    for attempt in range(1, _WEBHOOK_MAX_ATTEMPTS + 1):
        try:
            response = requests.post(WEBHOOK_URL, json=row, timeout=10)
            response.raise_for_status()
            mark_webhook_success(row, attempts=attempt)
            log_success = logger.debug if row.get("event_family") in _QUIET_SUCCESS_EVENT_FAMILIES else logger.info
            log_success(
                "POST ok (attempt %s/%s): %s | %s | %s | %s | %s",
                attempt,
                _WEBHOOK_MAX_ATTEMPTS,
                row.get("event_family"),
                row.get("event_type"),
                row.get("scope"),
                row.get("match_id"),
                row.get("game_number", ""),
            )
            return True
        except requests.HTTPError as exc:
            last_error = exc
            status_code = exc.response.status_code if exc.response is not None else None
            if status_code in _WEBHOOK_RETRYABLE_STATUS_CODES and attempt < _WEBHOOK_MAX_ATTEMPTS:
                delay = _WEBHOOK_BACKOFF_SECONDS[min(attempt - 1, len(_WEBHOOK_BACKOFF_SECONDS) - 1)]
                logger.warning(
                    "POST retry %s/%s after HTTP %s for %s/%s",
                    attempt + 1,
                    _WEBHOOK_MAX_ATTEMPTS,
                    status_code,
                    row.get("event_family"),
                    row.get("event_type"),
                )
                time.sleep(delay)
                continue

            response_text = exc.response.text[:500] if exc.response is not None and exc.response.text else ""
            out_path = record_failed_post(row, exc, response_text=response_text)
            mark_webhook_failure(row, exc, attempts=attempt)
            logger.error(
                "POST failed with HTTP %s for %s/%s after %s attempt(s); saved row to %s",
                status_code if status_code is not None else "unknown",
                row.get("event_family"),
                row.get("event_type"),
                attempt,
                out_path,
            )
            return False
        except requests.RequestException as exc:
            last_error = exc
            if attempt < _WEBHOOK_MAX_ATTEMPTS:
                delay = _WEBHOOK_BACKOFF_SECONDS[min(attempt - 1, len(_WEBHOOK_BACKOFF_SECONDS) - 1)]
                logger.warning(
                    "POST retry %s/%s after network error for %s/%s: %s",
                    attempt + 1,
                    _WEBHOOK_MAX_ATTEMPTS,
                    row.get("event_family"),
                    row.get("event_type"),
                    exc,
                )
                time.sleep(delay)
                continue

            out_path = record_failed_post(row, exc)
            mark_webhook_failure(row, exc, attempts=attempt)
            logger.error(
                "POST failed for %s/%s after %s attempt(s): %s; saved row to %s",
                row.get("event_family"),
                row.get("event_type"),
                attempt,
                exc,
                out_path,
            )
            return False

    if last_error is not None:
        out_path = record_failed_post(row, last_error)
        mark_webhook_failure(row, last_error, attempts=_WEBHOOK_MAX_ATTEMPTS)
        logger.error(
            "POST exhausted retries for %s/%s; saved row to %s",
            row.get("event_family"),
            row.get("event_type"),
            out_path,
        )
    return False


def _row_dispatch_key(row: dict[str, Any]) -> str:
    return json.dumps(row, sort_keys=True, ensure_ascii=False, default=str)


def _dispatch_loop() -> None:
    while True:
        job = _DISPATCH_QUEUE.get()
        try:
            if job is None:
                return
            success = post_row_to_google_sheets(job.row)
            _DISPATCH_RESULTS.put(WebhookDispatchResult(job=job, success=success))
        finally:
            _DISPATCH_QUEUE.task_done()


def start_webhook_dispatcher() -> None:
    global _DISPATCH_THREAD

    with _DISPATCH_LOCK:
        if _DISPATCH_THREAD is not None and _DISPATCH_THREAD.is_alive():
            return
        _DISPATCH_THREAD = threading.Thread(
            target=_dispatch_loop,
            name="manasight-webhook-dispatcher",
            daemon=True,
        )
        _DISPATCH_THREAD.start()
    update_runtime_status(webhook_dispatcher_active=True)


def submit_row_to_google_sheets(
    row: dict[str, Any],
    *,
    on_success: Callable[[], None] | None = None,
    on_failure: Callable[[], None] | None = None,
) -> bool:
    row_key = _row_dispatch_key(row)
    with _DISPATCH_LOCK:
        if row_key in _PENDING_ROW_KEYS:
            return False
        _PENDING_ROW_KEYS.add(row_key)
    _DISPATCH_QUEUE.put(
        WebhookDispatchJob(
            row=dict(row),
            row_key=row_key,
            on_success=on_success,
            on_failure=on_failure,
        )
    )
    return True


def drain_webhook_results(*, max_items: int = 200) -> int:
    processed = 0
    while processed < max_items:
        try:
            result = _DISPATCH_RESULTS.get_nowait()
        except Empty:
            break
        with _DISPATCH_LOCK:
            _PENDING_ROW_KEYS.discard(result.job.row_key)
        if result.success:
            if result.job.on_success is not None:
                result.job.on_success()
        elif result.job.on_failure is not None:
            result.job.on_failure()
        processed += 1
    return processed


def _drain_all_webhook_results() -> int:
    processed = 0
    while True:
        batch = drain_webhook_results(max_items=5000)
        processed += batch
        if batch == 0:
            return processed


def _drain_queue_without_processing() -> int:
    drained = 0
    while True:
        try:
            job = _DISPATCH_QUEUE.get_nowait()
        except Empty:
            return drained
        try:
            if job is not None:
                with _DISPATCH_LOCK:
                    _PENDING_ROW_KEYS.discard(job.row_key)
            drained += 1
        finally:
            _DISPATCH_QUEUE.task_done()


def _drain_results_without_callbacks() -> int:
    drained = 0
    while True:
        try:
            result = _DISPATCH_RESULTS.get_nowait()
        except Empty:
            return drained
        with _DISPATCH_LOCK:
            _PENDING_ROW_KEYS.discard(result.job.row_key)
        drained += 1


def stop_webhook_dispatcher(*, wait_for_queue: bool = True) -> None:
    global _DISPATCH_THREAD

    thread = _DISPATCH_THREAD
    if thread is None:
        _drain_all_webhook_results()
        update_runtime_status(webhook_dispatcher_active=False)
        return
    if wait_for_queue:
        _DISPATCH_QUEUE.join()
    _DISPATCH_QUEUE.put(None)
    thread.join(timeout=5)
    if thread.is_alive():
        get_logger("webhook").warning("Webhook dispatcher thread did not stop cleanly within timeout")
        update_runtime_status(webhook_dispatcher_active=True)
        return
    _DISPATCH_THREAD = None
    _drain_all_webhook_results()
    update_runtime_status(webhook_dispatcher_active=False)


# Build the daily folder name like 04_17_26.
def daily_log_label(event_dt: datetime) -> str:
    return event_dt.strftime("%m_%d_%y")


_daily_folder_name = daily_log_label


# Get or create the JSONL path for that day.
def _ensure_daily_log_path(event_dt: datetime) -> Path:
    folder_name = daily_log_label(event_dt)
    runtime_state = state.get_runtime_state()

    if runtime_state.current_log_date == folder_name and runtime_state.current_log_path is not None:
        return runtime_state.current_log_path

    day_folder = MATCH_LOGS_ROOT / folder_name
    day_folder.mkdir(parents=True, exist_ok=True)

    file_name = f"{OUT_FILENAME_PREFIX}_{folder_name}.jsonl"
    runtime_state.current_log_date = folder_name
    runtime_state.current_log_path = day_folder / file_name
    return runtime_state.current_log_path


# Append one already-serialized row to the local JSONL log.
def append_local_jsonl(local_row: dict[str, Any], event_dt: datetime) -> None:
    out_path = _ensure_daily_log_path(event_dt)
    with out_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(local_row, ensure_ascii=False) + "\n")
        f.flush()
