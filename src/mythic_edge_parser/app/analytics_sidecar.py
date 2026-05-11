from __future__ import annotations

import threading
from dataclasses import dataclass
from queue import Queue
from typing import Any

from .card_catalog import maybe_sync_card_catalog
from .card_performance import (
    CARD_PERFORMANCE_MARKDOWN_PATH,
    CARD_PERFORMANCE_PATH,
    refresh_card_performance_artifacts,
)
from .config import (
    POST_ACTION_LOG_ROWS,
    POST_CARD_PERFORMANCE_ROWS,
    POST_COLLECTION_SNAPSHOT_ROWS,
    POST_DECK_SNAPSHOT_ROWS,
    POST_PARSER_STATUS_ROWS,
    SYNC_CARD_CATALOG,
    SYNC_TIER_BUCKETS,
)
from .diagnostics import get_logger, update_runtime_status
from .outputs import submit_row_to_google_sheets
from .runtime_surfaces import bootstrap_runtime_surfaces
from .runtime_surfaces import observe_event as observe_runtime_surface_event
from .sheet_exports import collect_runtime_sheet_rows
from .tier_sync import sync_tier_sources


@dataclass(slots=True)
class AnalyticsSidecarJob:
    kind: str
    event: Any | None = None
    include_in_timeline: bool = False


_JOB_QUEUE: Queue[AnalyticsSidecarJob | None] = Queue()
_THREAD: threading.Thread | None = None
_LOCK = threading.Lock()


def analytics_sidecar_enabled() -> bool:
    return True


def start_analytics_sidecar() -> bool:
    global _THREAD

    if not analytics_sidecar_enabled():
        update_runtime_status(analytics_sidecar_active=False, analytics_sidecar_enabled=False)
        return False

    with _LOCK:
        if _THREAD is not None and _THREAD.is_alive():
            return True
        _THREAD = threading.Thread(
            target=_analytics_loop,
            name="manasight-analytics-sidecar",
            daemon=True,
        )
        _THREAD.start()
    update_runtime_status(analytics_sidecar_active=True, analytics_sidecar_enabled=True)
    return True


def submit_analytics_event(event: Any, *, include_in_timeline: bool) -> bool:
    if not analytics_sidecar_enabled():
        return False
    _JOB_QUEUE.put(AnalyticsSidecarJob(kind="event", event=event, include_in_timeline=include_in_timeline))
    return True


def stop_analytics_sidecar(*, wait_for_queue: bool = False) -> None:
    global _THREAD

    thread = _THREAD
    if thread is None:
        return
    if wait_for_queue:
        _JOB_QUEUE.join()
    _JOB_QUEUE.put(None)
    thread.join(timeout=2)
    _THREAD = None
    update_runtime_status(analytics_sidecar_active=False)


def _analytics_loop() -> None:
    logger = get_logger("analytics-sidecar")
    try:
        bootstrap_runtime_surfaces()
    except Exception:
        logger.exception("Analytics sidecar bootstrap failed")

    _run_startup_syncs(logger)

    while True:
        job = _JOB_QUEUE.get()
        try:
            if job is None:
                return
            if job.kind == "event" and job.event is not None:
                _process_event_job(job, logger)
        except Exception:
            logger.exception("Analytics sidecar job failed")
        finally:
            _JOB_QUEUE.task_done()


def _run_startup_syncs(logger: Any) -> None:
    if SYNC_TIER_BUCKETS:
        try:
            result = sync_tier_sources(post_to_webhook=True)
            logger.info(result.summary_line())
        except Exception:
            logger.exception("Background tier sync failed")

    if SYNC_CARD_CATALOG:
        try:
            decision = maybe_sync_card_catalog(format_key="standard")
            logger.info(decision.summary_line())
            if decision.sync_result is not None:
                logger.info("Card catalog Arena lookup: %s", decision.sync_result.arena_lookup_json_path)
        except Exception:
            logger.exception("Background card catalog sync check failed")


def _should_refresh_card_performance(event: object) -> bool:
    kind = str(getattr(event, "kind", "")).strip()
    if kind != "MatchState":
        return False
    payload = getattr(event, "payload", {}) or {}
    match_type = str(payload.get("type", "")).strip()
    match_state = str(payload.get("match_state", "")).strip()
    return match_type == "match_completed" or match_state == "MatchState_MatchComplete"


def _should_post_action_rows(event: object) -> bool:
    if not POST_ACTION_LOG_ROWS:
        return False
    kind = str(getattr(event, "kind", "")).strip()
    if kind == "GameResult":
        return True
    return _should_refresh_card_performance(event)


def _should_post_parser_status_rows(event: object) -> bool:
    if not POST_PARSER_STATUS_ROWS:
        return False

    kind = str(getattr(event, "kind", "")).strip()
    payload = getattr(event, "payload", {}) or {}

    if kind == "MatchState":
        match_type = str(payload.get("type", "")).strip()
        match_state = str(payload.get("match_state", "")).strip()
        return match_type in {"match_started", "match_completed"} or match_state == "MatchState_MatchComplete"

    if kind == "GameResult":
        return True

    if kind == "ClientAction":
        return str(payload.get("type", "")).strip() == "submit_deck_resp"

    return kind in {
        "Rank",
        "ConnectionError",
        "TcpConnectionClose",
        "WebSocketClosed",
        "MatchConnectionState",
        "DetailedLoggingStatus",
    }


def _runtime_export_flags(event: object, *, card_performance_ready: bool) -> dict[str, bool]:
    kind = str(getattr(event, "kind", "")).strip()
    payload = getattr(event, "payload", {}) or {}
    is_submit_deck = kind == "ClientAction" and str(payload.get("type", "")).strip() == "submit_deck_resp"
    is_collection_event = kind in {"DeckCollection", "Collection", "Inventory"}
    is_final_match_checkpoint = _should_refresh_card_performance(event)

    return {
        "post_action_rows": _should_post_action_rows(event),
        "post_deck_snapshot_rows": POST_DECK_SNAPSHOT_ROWS and (is_submit_deck or is_final_match_checkpoint),
        "post_collection_snapshot_rows": POST_COLLECTION_SNAPSHOT_ROWS and is_collection_event,
        "post_parser_status_rows": _should_post_parser_status_rows(event),
        "post_card_performance_rows": POST_CARD_PERFORMANCE_ROWS and card_performance_ready,
    }


def _process_event_job(job: AnalyticsSidecarJob, logger: Any) -> None:
    event = job.event
    if event is None:
        return

    observe_runtime_surface_event(event, include_in_timeline=job.include_in_timeline)

    card_performance_payload: dict[str, Any] | None = None
    if _should_refresh_card_performance(event):
        try:
            card_performance_payload = refresh_card_performance_artifacts()
            update_runtime_status(
                card_performance_path=str(CARD_PERFORMANCE_PATH),
                card_performance_markdown_path=str(CARD_PERFORMANCE_MARKDOWN_PATH),
                card_performance_total_cards=card_performance_payload.get("total_cards", 0),
                card_performance_total_games=card_performance_payload.get("total_games", 0),
            )
        except Exception:
            logger.exception("Card performance refresh failed")

    export_flags = _runtime_export_flags(event, card_performance_ready=card_performance_payload is not None)
    if not any(export_flags.values()):
        return

    for artifact_row in collect_runtime_sheet_rows(
        card_performance_payload=card_performance_payload,
        **export_flags,
    ):
        submit_row_to_google_sheets(artifact_row)
