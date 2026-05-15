import json
from pathlib import Path, PureWindowsPath
from typing import Any, Callable
from urllib.parse import urlparse

from ..stream import MtgaEventStream
from .analytics_sidecar import (
    start_analytics_sidecar,
    stop_analytics_sidecar,
    submit_analytics_event,
)
from .config import (
    LOG_PATH,
    MATCH_LOGS_ROOT,
    POST_ACTION_LOG_ROWS,
    POST_CARD_PERFORMANCE_ROWS,
    POST_COLLECTION_SNAPSHOT_ROWS,
    POST_DECK_SNAPSHOT_ROWS,
    POST_GAME_LOG_ROWS,
    POST_GAMESTATE_ROWS,
    POST_MATCH_LOG_ROWS,
    POST_MATCH_SUMMARY_ROWS,
    POST_PARSER_STATUS_ROWS,
    POST_RAW_EVENT_ROWS,
    PROJECT_ROOT,
    SYNC_TIER_BUCKETS,
    TIER_NORMALIZATION_PATH,
    WEBHOOK_URL,
)
from .diagnostics import (
    current_runtime_log_path,
    current_status_path,
    get_logger,
    mark_event_seen,
    record_event_failure,
    record_submitted_deck,
    setup_runtime_logging,
    update_runtime_status,
)
from .extractors import _event_datetime
from .gameplay_actions import (
    bootstrap_gameplay_actions,
)
from .gameplay_actions import (
    observe_event as observe_gameplay_event,
)
from .outputs import (
    append_local_jsonl,
    daily_log_label,
    drain_webhook_results,
    start_webhook_dispatcher,
    stop_webhook_dispatcher,
    submit_row_to_google_sheets,
    webhook_target_display,
)
from .state import (
    _CONTEXT,
    _POSTED_MATCH_SUMMARIES,
    _update_match_summary,
    build_game_log_updates,
    build_match_log_update,
    build_match_summary_row,
    mark_game_log_posted,
    mark_match_log_posted,
)
from .status_api import start_status_api_server, stop_status_api_server
from .transforms import include_event, summarize, to_serializable, to_sheet_rows


def _display_path(path: Path | None) -> str:
    if path is None:
        return ""
    path_text = str(path)
    windows_path = PureWindowsPath(path_text)
    windows_name = windows_path.name
    if "\\" in path_text and windows_name and not path.is_absolute() and (windows_path.drive or windows_path.root):
        return windows_name
    try:
        return str(path.resolve(strict=False).relative_to(PROJECT_ROOT.resolve(strict=False)))
    except Exception:
        if "\\" in path_text and windows_name:
            return windows_name
        return path.name or windows_name or path_text


def _sheet_posting_enabled() -> bool:
    return any(
        (
            POST_RAW_EVENT_ROWS,
            POST_GAMESTATE_ROWS,
            POST_GAME_LOG_ROWS,
            POST_MATCH_SUMMARY_ROWS,
            POST_MATCH_LOG_ROWS,
            POST_ACTION_LOG_ROWS,
            POST_DECK_SNAPSHOT_ROWS,
            POST_COLLECTION_SNAPSHOT_ROWS,
            POST_PARSER_STATUS_ROWS,
            POST_CARD_PERFORMANCE_ROWS,
        )
    )


def _startup_status_fields() -> dict[str, object]:
    return {
        "status": "starting",
        "log_path": _display_path(LOG_PATH),
        "match_logs_root": _display_path(MATCH_LOGS_ROOT),
        "webhook_enabled": bool(WEBHOOK_URL),
        "webhook_target": webhook_target_display(WEBHOOK_URL),
        "post_match_log_rows": POST_MATCH_LOG_ROWS,
        "post_game_log_rows": POST_GAME_LOG_ROWS,
        "post_match_summaries": POST_MATCH_SUMMARY_ROWS,
        "post_raw_event_rows": POST_RAW_EVENT_ROWS,
        "post_gamestate_rows": POST_GAMESTATE_ROWS,
        "post_action_log_rows": POST_ACTION_LOG_ROWS,
        "post_deck_snapshot_rows": POST_DECK_SNAPSHOT_ROWS,
        "post_collection_snapshot_rows": POST_COLLECTION_SNAPSHOT_ROWS,
        "post_parser_status_rows": POST_PARSER_STATUS_ROWS,
        "post_card_performance_rows": POST_CARD_PERFORMANCE_ROWS,
        "status_file_path": _display_path(current_status_path()),
    }


def _should_post_sheet_debug_rows(event: object) -> bool:
    if POST_RAW_EVENT_ROWS:
        return True
    return POST_GAMESTATE_ROWS and str(getattr(event, "kind", "")).strip() == "GameState"


def _post_sheet_debug_rows(event: object) -> int:
    if not _should_post_sheet_debug_rows(event):
        return 0

    posted = 0
    for sheet_row in to_sheet_rows(event):
        submit_row_to_google_sheets(sheet_row)
        posted += 1
    return posted


def _maybe_record_submitted_deck(event: object, logger: Any) -> None:
    if getattr(event, "kind", "") != "ClientAction":
        return

    payload = getattr(event, "payload", {}) or {}
    if payload.get("type") != "submit_deck_resp":
        return

    submitted_deck_path = record_submitted_deck(
        payload,
        match_id=_CONTEXT.get("current_match_id", ""),
        game_number=_CONTEXT.get("current_game_number", ""),
        event_timestamp=getattr(getattr(event, "metadata", None), "timestamp", None),
    )
    if submitted_deck_path is not None:
        logger.info("Active submitted deck updated: %s", _display_path(submitted_deck_path))


def _post_game_log_rows(logger: Any) -> None:
    if not POST_GAME_LOG_ROWS:
        return

    match_id = _CONTEXT.get("current_match_id")
    if not match_id:
        return

    for game_row, changed_fields, is_final in build_game_log_updates(match_id):
        sync_phase = "final" if is_final else "live"
        submit_row_to_google_sheets(
            game_row,
            on_success=_game_log_success_callback(
                logger,
                match_id=match_id,
                game_row=game_row,
                changed_fields=changed_fields,
                sync_phase=sync_phase,
            ),
        )


def _post_match_summary_row() -> None:
    if not POST_MATCH_SUMMARY_ROWS:
        return

    match_id = _CONTEXT.get("current_match_id")
    if not match_id or match_id in _POSTED_MATCH_SUMMARIES:
        return

    summary_row = build_match_summary_row(match_id)
    if summary_row is None:
        return

    submit_row_to_google_sheets(
        summary_row,
        on_success=lambda match_id=match_id: _POSTED_MATCH_SUMMARIES.add(match_id),
    )


def _post_match_log_row(logger: Any) -> None:
    if not POST_MATCH_LOG_ROWS:
        return

    match_id = _CONTEXT.get("current_match_id")
    if not match_id:
        return

    match_log_row, changed_fields, is_final = build_match_log_update(match_id)
    if match_log_row is None:
        return

    sync_phase = "final" if is_final else "live"
    submit_row_to_google_sheets(
        match_log_row,
        on_success=_match_log_success_callback(
            logger,
            match_id=match_id,
            match_log_row=match_log_row,
            changed_fields=changed_fields,
            sync_phase=sync_phase,
        ),
    )


def _game_log_success_callback(
    logger: Any,
    *,
    match_id: str,
    game_row: dict[str, object],
    changed_fields: list[str],
    sync_phase: str,
) -> Callable[[], None]:
    game_row_snapshot = dict(game_row)
    changed_fields_snapshot = list(changed_fields)

    def _callback() -> None:
        mark_game_log_posted(
            match_id,
            game_row_snapshot.get("Game Number"),
            game_row_snapshot,
        )
        logger.info(
            "GameLog %s sync match=%s game=%s changed=%s",
            sync_phase,
            match_id,
            game_row_snapshot.get("Game Number", ""),
            ",".join(changed_fields_snapshot),
        )

    return _callback


def _match_log_success_callback(
    logger: Any,
    *,
    match_id: str,
    match_log_row: dict[str, object],
    changed_fields: list[str],
    sync_phase: str,
) -> Callable[[], None]:
    match_log_snapshot = dict(match_log_row)
    changed_fields_snapshot = list(changed_fields)

    def _callback() -> None:
        mark_match_log_posted(match_id, match_log_snapshot)
        logger.info(
            "MatchLog %s sync match=%s changed=%s",
            sync_phase,
            match_id,
            ",".join(changed_fields_snapshot),
        )

    return _callback


def _startup_issues() -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    errors: list[str] = []

    if not LOG_PATH.exists():
        errors.append(f"MTGA Player.log was not found at {LOG_PATH}")

    if any(
        (
            POST_RAW_EVENT_ROWS,
            POST_MATCH_SUMMARY_ROWS,
            POST_MATCH_LOG_ROWS,
            POST_GAME_LOG_ROWS,
            POST_GAMESTATE_ROWS,
            POST_ACTION_LOG_ROWS,
            POST_DECK_SNAPSHOT_ROWS,
            POST_COLLECTION_SNAPSHOT_ROWS,
            POST_PARSER_STATUS_ROWS,
            POST_CARD_PERFORMANCE_ROWS,
        )
    ):
        if not WEBHOOK_URL:
            warnings.append("Sheet posting is enabled, but the webhook URL is blank")
        else:
            parsed = urlparse(WEBHOOK_URL)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                errors.append("Webhook URL does not look valid")

    if SYNC_TIER_BUCKETS:
        if not TIER_NORMALIZATION_PATH.exists():
            warnings.append(f"Tier normalization file is missing: {TIER_NORMALIZATION_PATH}")
        else:
            try:
                json.loads(TIER_NORMALIZATION_PATH.read_text(encoding="utf-8"))
            except Exception as exc:
                warnings.append(f"Tier normalization JSON could not be read: {exc}")

    return warnings, errors


# Main async function to process the MTGA event stream.
async def main() -> None:
    setup_runtime_logging()
    logger = get_logger("runner")

    MATCH_LOGS_ROOT.mkdir(parents=True, exist_ok=True)
    logger.info("Startup: runtime log file is %s", _display_path(current_runtime_log_path()))
    update_runtime_status(**_startup_status_fields())

    warnings, errors = _startup_issues()
    for message in warnings:
        logger.warning("Startup warning: %s", message)
    for message in errors:
        logger.error("Startup error: %s", message)
    if errors:
        raise RuntimeError("Startup checks failed. See runtime log for details.")

    bootstrap_gameplay_actions()

    try:
        stream, subscriber = await MtgaEventStream.start(LOG_PATH)
    except Exception as exc:
        logger.exception("Could not start MTGA event stream: %s", exc)
        raise

    logger.info("Watching: %s", _display_path(LOG_PATH))
    logger.info("Writing daily match logs under: %s", _display_path(MATCH_LOGS_ROOT))
    logger.info("Posting raw archive rows to Sheets: %s", POST_RAW_EVENT_ROWS)
    logger.info("Posting full GameState rows to Sheets: %s", POST_GAMESTATE_ROWS)
    logger.info("Posting Game Log rows to Sheets: %s", POST_GAME_LOG_ROWS)
    logger.info("Posting MatchSummary rows to Sheets: %s", POST_MATCH_SUMMARY_ROWS)
    logger.info("Posting Match Log rows to Sheets: %s", POST_MATCH_LOG_ROWS)
    logger.info("Posting Action Log rows to Sheets: %s", POST_ACTION_LOG_ROWS)
    logger.info("Posting Deck Snapshot rows to Sheets: %s", POST_DECK_SNAPSHOT_ROWS)
    logger.info("Posting Collection Snapshot rows to Sheets: %s", POST_COLLECTION_SNAPSHOT_ROWS)
    logger.info("Posting Parser Status rows to Sheets: %s", POST_PARSER_STATUS_ROWS)
    logger.info("Posting Card Performance rows to Sheets: %s", POST_CARD_PERFORMANCE_ROWS)
    logger.info("Webhook target: %s", webhook_target_display())
    update_runtime_status(status="running")

    if _sheet_posting_enabled():
        start_webhook_dispatcher()
    start_analytics_sidecar()

    try:
        api_info = start_status_api_server()
        if api_info is not None:
            logger.info("Local status API: %s", api_info["base_url"])
            update_runtime_status(
                local_status_api_url=api_info["base_url"],
                local_status_api_host=api_info["host"],
                local_status_api_port=api_info["port"],
                local_status_api_enabled=True,
            )
    except Exception as exc:
        logger.warning("Local status API could not start: %s", exc)
        update_runtime_status(
            local_status_api_enabled=False,
            local_status_api_error=str(exc),
        )

    try:
        while True:
            drain_webhook_results()
            event = await subscriber.recv()
            if event is None:
                break

            try:
                # Let the in-memory match summary see every event, even if we later
                # choose not to archive or sheet-post that event verbatim.
                _update_match_summary(event)
                mark_event_seen(
                    event,
                    match_id=_CONTEXT.get("current_match_id", ""),
                    game_number=_CONTEXT.get("current_game_number", ""),
                    player_team=_CONTEXT.get("current_player_team", ""),
                )
                observe_gameplay_event(event)
                keep_event = include_event(event)
                submit_analytics_event(event, include_in_timeline=keep_event)

                if not keep_event:
                    continue

                # 1) Write the local JSONL log.
                local_row = to_serializable(event)
                event_dt = _event_datetime(event)
                append_local_jsonl(local_row, event_dt)
                _maybe_record_submitted_deck(event, logger)

                # 2) Post raw event rows only when debug/archive output is enabled.
                _post_sheet_debug_rows(event)

                # 3) Post one normalized Game Log row per tracked game when it changes.
                _post_game_log_rows(logger)

                # 4) Post one normalized MatchSummary row when ready.
                _post_match_summary_row()

                # 5) Post one first-phase Match Log row when ready.
                _post_match_log_row(logger)

                # 6) Console output.
                summary_text = summarize(event)
                if getattr(event, "kind", "") == "GameState":
                    logger.debug("[%s] %s", daily_log_label(event_dt), summary_text)
                else:
                    logger.info("[%s] %s", daily_log_label(event_dt), summary_text)
            except Exception as exc:
                out_path = record_event_failure(event, exc, stage="runner")
                logger.exception(
                    "Event processing failed for %s; saved failure record to %s",
                    getattr(event, "kind", ""),
                    out_path,
                )

    finally:
        drain_webhook_results(max_items=5000)
        stop_webhook_dispatcher(wait_for_queue=True)
        drain_webhook_results(max_items=5000)
        stop_analytics_sidecar(wait_for_queue=False)
        update_runtime_status(status="stopped")
        stop_status_api_server()
        await stream.shutdown()
