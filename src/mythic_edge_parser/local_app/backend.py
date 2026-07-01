from __future__ import annotations

import hmac
import os
import secrets
from collections.abc import Mapping, Sequence
from pathlib import Path
from urllib.parse import urlparse

from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.datastructures import UploadFile

from . import import_jobs
from .analytics_dashboard import build_analytics_dashboard_modules
from .analytics_history import (
    build_game1_postboard_split_review,
    build_game_history,
    build_gameplay_action_review,
    build_match_history,
    build_mulligan_history,
    build_opening_hand_history,
    build_opponent_card_observation_review,
    build_play_draw_split_review,
)
from .analytics_refresh_state import build_analytics_refresh_state
from .config import load_local_app_config_status
from .error_reports import GitHubIssueSubmitter, build_error_report_preview, build_error_report_submission
from .import_jobs import (
    BrowserJsonlUploadFile,
    get_import_job,
    reject_browser_jsonl_upload_import,
    run_browser_jsonl_upload_import,
    run_manual_jsonl_import,
)
from .live_capture_control import build_live_capture_status, start_live_capture, stop_live_capture
from .live_watcher_diagnostics import build_live_watcher_diagnostics_status
from .live_watcher_process import build_live_watcher_process_status
from .match_journal_cockpit import (
    JournalServiceFactory,
    match_journal_get_response,
    match_journal_note_readback_response,
    match_journal_post_response,
)
from .match_journal_runtime import build_match_journal_service_factory
from .paths import build_local_app_paths
from .setup_status import (
    build_analytics_database_status,
    build_health_status,
    build_live_player_log_status,
    build_live_sqlite_capture_status,
    build_live_watcher_status,
    build_runtime_state,
    build_setup_status,
)

FRONTEND_ORIGIN_ENV = "MYTHIC_EDGE_LOCAL_APP_FRONTEND_ORIGIN"
DEFAULT_FRONTEND_ORIGINS = ("http://127.0.0.1:5173", "http://localhost:5173")
LOOPBACK_HOSTS = {"127.0.0.1", "localhost"}
LOCAL_REQUEST_GUARD_HEADER = "X-Mythic-Edge-Local-Request-Guard"
LOCAL_REQUEST_GUARD_OBJECT = "mythic_edge_local_request_guard"
LOCAL_REQUEST_GUARD_SCHEMA_VERSION = 1
GUARDED_MUTATING_API_ROUTES = frozenset(
    {
        "/api/live/capture/start",
        "/api/live/capture/stop",
        "/api/feedback/error-report/preview",
        "/api/feedback/error-report/submit",
        "/api/journal/notes",
        "/api/journal/opponent-labels",
        "/api/journal/review-flags",
        "/api/journal/experiment-label",
        "/api/journal/display-corrections",
        "/api/imports/jsonl",
        "/api/imports/jsonl/upload",
    }
)
HISTORY_QUERY_PARAM_INVALID = "analytics_history_query_parameter_invalid"
HISTORY_QUERY_PARAM_NOT_ALLOWED = "analytics_history_query_parameter_not_allowed"
DASHBOARD_QUERY_PARAM_NOT_ALLOWED = "analytics_dashboard_query_parameter_not_allowed"
REFRESH_STATE_QUERY_PARAM_NOT_ALLOWED = "analytics_refresh_state_query_parameter_not_allowed"
_BROWSER_JSONL_UPLOAD_READ_CHUNK_BYTES = 64 * 1024


class _BrowserJsonlUploadReadError(ValueError):
    def __init__(self, error_code: str) -> None:
        super().__init__(error_code)
        self.error_code = error_code


def create_app(
    *,
    app_data_root: Path | None = None,
    frontend_origins: Sequence[str] | None = None,
    env: Mapping[str, str] = os.environ,
    match_journal_service_factory: JournalServiceFactory | None = None,
    error_report_submitter: GitHubIssueSubmitter | None = None,
) -> FastAPI:
    local_app_paths = build_local_app_paths(app_data_root, env=env)
    resolved_app_data_root = local_app_paths.app_data_root
    journal_service_factory = match_journal_service_factory or build_match_journal_service_factory(local_app_paths)
    app = FastAPI(
        title="Mythic Edge Local App Backend",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    allowed_origins = resolve_frontend_origins(frontend_origins=frontend_origins, env=env)
    app.state.local_request_guard_token = secrets.token_urlsafe(32)
    app.state.local_request_guard_allowed_origins = allowed_origins
    guarded_mutation_dependencies = [Depends(require_local_request_guard)]
    if allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=list(allowed_origins),
            allow_methods=["GET", "POST"],
            allow_headers=["Accept", "Content-Type", LOCAL_REQUEST_GUARD_HEADER],
        )

    @app.get("/api/health")
    def health() -> dict[str, object]:
        return build_health_status()

    @app.get("/api/app/setup-status")
    def setup_status() -> dict[str, object]:
        return build_setup_status(local_app_paths)

    @app.get("/api/app/config")
    def app_config() -> dict[str, object]:
        return load_local_app_config_status(local_app_paths)

    @app.get("/api/app/paths")
    def app_paths() -> dict[str, object]:
        from .paths import build_path_status

        return build_path_status(local_app_paths)

    @app.get("/api/app/request-guard")
    def app_request_guard(request: Request) -> dict[str, object]:
        _validate_local_request_origin_and_host(request)
        guard_value = _get_local_request_guard_token(request)
        payload: dict[str, object] = {
            "object": LOCAL_REQUEST_GUARD_OBJECT,
            "schema_version": LOCAL_REQUEST_GUARD_SCHEMA_VERSION,
            "status": "available",
            "header_name": LOCAL_REQUEST_GUARD_HEADER,
            "expires_on_backend_restart": True,
            "warnings": [],
            "errors": [],
        }
        payload["token"] = guard_value
        return payload

    @app.get("/api/analytics/database/status")
    def analytics_database_status() -> dict[str, object]:
        return build_analytics_database_status(local_app_paths)

    @app.get("/api/live/player-log/status")
    def live_player_log_status() -> dict[str, object]:
        return build_live_player_log_status(local_app_paths)

    @app.get("/api/live/watcher/status")
    def live_watcher_status() -> dict[str, object]:
        return build_live_watcher_status(local_app_paths)

    @app.get("/api/live/watcher/process")
    def live_watcher_process_status() -> dict[str, object]:
        return build_live_watcher_process_status(local_app_paths)

    @app.get("/api/live/watcher/diagnostics")
    def live_watcher_diagnostics_status() -> dict[str, object]:
        return build_live_watcher_diagnostics_status(local_app_paths)

    @app.get("/api/live/ingest/status")
    def live_ingest_status() -> dict[str, object]:
        return build_live_sqlite_capture_status(local_app_paths)

    @app.get("/api/live/capture/status")
    def live_capture_status() -> dict[str, object]:
        return build_live_capture_status(local_app_paths)

    @app.post("/api/live/capture/start", dependencies=guarded_mutation_dependencies)
    def live_capture_start() -> dict[str, object]:
        return start_live_capture(local_app_paths)

    @app.post("/api/live/capture/stop", dependencies=guarded_mutation_dependencies)
    def live_capture_stop() -> dict[str, object]:
        return stop_live_capture(local_app_paths)

    @app.get("/api/analytics/matches")
    def analytics_match_history(request: Request) -> dict[str, object]:
        limit, offset = _history_pagination(request)
        return build_match_history(local_app_paths, limit=limit, offset=offset)

    @app.get("/api/analytics/games")
    def analytics_game_history(request: Request) -> dict[str, object]:
        limit, offset = _history_pagination(request)
        return build_game_history(local_app_paths, limit=limit, offset=offset)

    @app.get("/api/analytics/opening-hands")
    def analytics_opening_hand_history(request: Request) -> dict[str, object]:
        limit, offset = _history_pagination(request)
        return build_opening_hand_history(local_app_paths, limit=limit, offset=offset)

    @app.get("/api/analytics/mulligans")
    def analytics_mulligan_history(request: Request) -> dict[str, object]:
        limit, offset = _history_pagination(request)
        return build_mulligan_history(local_app_paths, limit=limit, offset=offset)

    @app.get("/api/analytics/gameplay-actions")
    def analytics_gameplay_action_review(request: Request) -> dict[str, object]:
        limit, offset = _history_pagination(request)
        return build_gameplay_action_review(local_app_paths, limit=limit, offset=offset)

    @app.get("/api/analytics/opponent-card-observations")
    def analytics_opponent_card_observation_review(request: Request) -> dict[str, object]:
        limit, offset = _history_pagination(request)
        return build_opponent_card_observation_review(local_app_paths, limit=limit, offset=offset)

    @app.get("/api/analytics/play-draw-splits")
    def analytics_play_draw_split_review(request: Request) -> dict[str, object]:
        limit, offset = _history_pagination(request)
        return build_play_draw_split_review(local_app_paths, limit=limit, offset=offset)

    @app.get("/api/analytics/game1-postboard-splits")
    def analytics_game1_postboard_split_review(request: Request) -> dict[str, object]:
        limit, offset = _history_pagination(request)
        return build_game1_postboard_split_review(local_app_paths, limit=limit, offset=offset)

    @app.get("/api/analytics/dashboard/modules")
    def analytics_dashboard_modules(request: Request) -> dict[str, object]:
        _reject_dashboard_query_params(request)
        return build_analytics_dashboard_modules(local_app_paths)

    @app.get("/api/analytics/refresh-state")
    def analytics_refresh_state(request: Request) -> dict[str, object]:
        _reject_refresh_state_query_params(request)
        return build_analytics_refresh_state(local_app_paths)

    @app.get("/api/runtime/status")
    def runtime_state() -> dict[str, object]:
        return build_runtime_state()

    @app.post("/api/feedback/error-report/preview", dependencies=guarded_mutation_dependencies)
    def error_report_preview(request: object = Body(...)) -> dict[str, object]:
        return build_error_report_preview(request, local_app_paths)

    @app.post("/api/feedback/error-report/submit", dependencies=guarded_mutation_dependencies)
    def error_report_submit(request: object = Body(...)) -> dict[str, object]:
        return build_error_report_submission(request, local_app_paths, submitter=error_report_submitter)

    @app.get("/api/journal")
    async def match_journal(request: Request) -> object:
        return await match_journal_get_response(request, journal_service_factory)

    @app.post("/api/journal/notes", dependencies=guarded_mutation_dependencies)
    async def match_journal_notes(request: Request) -> object:
        return await match_journal_post_response("notes", request, journal_service_factory)

    @app.get("/api/journal/notes")
    async def match_journal_note_readback(request: Request) -> object:
        return await match_journal_note_readback_response(request, journal_service_factory)

    @app.post("/api/journal/opponent-labels", dependencies=guarded_mutation_dependencies)
    async def match_journal_opponent_labels(request: Request) -> object:
        return await match_journal_post_response("opponent-labels", request, journal_service_factory)

    @app.post("/api/journal/review-flags", dependencies=guarded_mutation_dependencies)
    async def match_journal_review_flags(request: Request) -> object:
        return await match_journal_post_response("review-flags", request, journal_service_factory)

    @app.post("/api/journal/experiment-label", dependencies=guarded_mutation_dependencies)
    async def match_journal_experiment_label(request: Request) -> object:
        return await match_journal_post_response("experiment-label", request, journal_service_factory)

    @app.post("/api/journal/display-corrections", dependencies=guarded_mutation_dependencies)
    async def match_journal_display_corrections(request: Request) -> object:
        return await match_journal_post_response("display-corrections", request, journal_service_factory)

    @app.post("/api/imports/jsonl", dependencies=guarded_mutation_dependencies)
    def import_jsonl(request: object = Body(...)) -> dict[str, object]:
        return run_manual_jsonl_import(request, app_data_root=resolved_app_data_root)

    @app.post("/api/imports/jsonl/upload", dependencies=guarded_mutation_dependencies)
    async def import_jsonl_upload(request: Request) -> dict[str, object]:
        form = await request.form()
        upload_files: list[UploadFile] = []
        try:
            form_files = list(form.getlist("files"))
            raw_source_artifact_labels = form.getlist("source_artifact_label")
            raw_source_artifact_label = raw_source_artifact_labels[-1] if raw_source_artifact_labels else None
            source_artifact_label = raw_source_artifact_label if isinstance(raw_source_artifact_label, str) else None

            for value in form_files:
                if not isinstance(value, UploadFile):
                    return reject_browser_jsonl_upload_import(
                        "upload_file_invalid",
                        files_selected=len(form_files),
                        app_data_root=resolved_app_data_root,
                    )
                upload_files.append(value)

            if raw_source_artifact_label is not None and not isinstance(raw_source_artifact_label, str):
                return reject_browser_jsonl_upload_import(
                    "source_artifact_label_invalid",
                    files_selected=len(form_files),
                    app_data_root=resolved_app_data_root,
                )

            try:
                uploads = await _build_browser_jsonl_upload_files(upload_files)
            except _BrowserJsonlUploadReadError as exc:
                return reject_browser_jsonl_upload_import(
                    exc.error_code,
                    files_selected=len(form_files),
                    app_data_root=resolved_app_data_root,
                )
        finally:
            for upload_file in upload_files:
                await upload_file.close()
            await form.close()

        return run_browser_jsonl_upload_import(
            uploads,
            source_artifact_label=source_artifact_label,
            app_data_root=resolved_app_data_root,
        )

    @app.get("/api/imports/jobs/{job_id}")
    def import_job(job_id: str) -> dict[str, object]:
        job = get_import_job(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail={"error": "not_found"})
        return job

    return app


async def _build_browser_jsonl_upload_files(upload_files: Sequence[UploadFile]) -> list[BrowserJsonlUploadFile]:
    if not upload_files:
        raise _BrowserJsonlUploadReadError("upload_files_required")
    if len(upload_files) > import_jobs.MAX_BROWSER_JSONL_UPLOAD_FILES:
        raise _BrowserJsonlUploadReadError("upload_files_too_many")

    uploads: list[BrowserJsonlUploadFile] = []
    total_size = 0
    for upload_file in upload_files:
        content_bytes = await _read_browser_jsonl_upload_file(upload_file, accepted_total_bytes=total_size)
        total_size += len(content_bytes)
        uploads.append(
            BrowserJsonlUploadFile(
                filename=upload_file.filename or "",
                content_bytes=content_bytes,
                content_type=upload_file.content_type or "",
            )
        )
    return uploads


async def _read_browser_jsonl_upload_file(upload_file: UploadFile, *, accepted_total_bytes: int) -> bytes:
    chunks: list[bytes] = []
    file_size = 0
    while True:
        file_budget_remaining = import_jobs.MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES - file_size
        total_budget_remaining = import_jobs.MAX_BROWSER_JSONL_UPLOAD_TOTAL_BYTES - accepted_total_bytes - file_size
        read_size = min(
            _BROWSER_JSONL_UPLOAD_READ_CHUNK_BYTES,
            max(1, file_budget_remaining + 1),
            max(1, total_budget_remaining + 1),
        )
        chunk = await upload_file.read(read_size)
        if not chunk:
            return b"".join(chunks)

        next_file_size = file_size + len(chunk)
        next_total_size = accepted_total_bytes + next_file_size
        if next_file_size > import_jobs.MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES:
            raise _BrowserJsonlUploadReadError("upload_file_too_large")
        if next_total_size > import_jobs.MAX_BROWSER_JSONL_UPLOAD_TOTAL_BYTES:
            raise _BrowserJsonlUploadReadError("upload_total_size_too_large")

        chunks.append(chunk)
        file_size = next_file_size


def _reject_unknown_history_query_params(request: Request) -> None:
    allowed = {"limit", "offset"}
    if any(key not in allowed for key in request.query_params.keys()):
        raise HTTPException(status_code=422, detail={"error": HISTORY_QUERY_PARAM_NOT_ALLOWED})


def _reject_dashboard_query_params(request: Request) -> None:
    if request.query_params:
        raise HTTPException(status_code=422, detail={"error": DASHBOARD_QUERY_PARAM_NOT_ALLOWED})


def _reject_refresh_state_query_params(request: Request) -> None:
    if request.query_params:
        raise HTTPException(status_code=422, detail={"error": REFRESH_STATE_QUERY_PARAM_NOT_ALLOWED})


def _history_pagination(request: Request) -> tuple[int, int]:
    _reject_unknown_history_query_params(request)
    limit = _history_query_int(request, "limit", default=50, minimum=1, maximum=100)
    offset = _history_query_int(request, "offset", default=0, minimum=0)
    return limit, offset


def _history_query_int(
    request: Request,
    key: str,
    *,
    default: int,
    minimum: int,
    maximum: int | None = None,
) -> int:
    values = request.query_params.getlist(key)
    if not values:
        return default
    if len(values) != 1:
        raise HTTPException(status_code=422, detail={"error": HISTORY_QUERY_PARAM_INVALID})

    raw_value = values[0]
    if not raw_value.isdecimal():
        raise HTTPException(status_code=422, detail={"error": HISTORY_QUERY_PARAM_INVALID})

    value = int(raw_value)
    if value < minimum or (maximum is not None and value > maximum):
        raise HTTPException(status_code=422, detail={"error": HISTORY_QUERY_PARAM_INVALID})
    return value


def resolve_frontend_origins(
    *,
    frontend_origins: Sequence[str] | None = None,
    env: Mapping[str, str] = os.environ,
) -> tuple[str, ...]:
    candidates = list(frontend_origins if frontend_origins is not None else DEFAULT_FRONTEND_ORIGINS)
    env_origin = env.get(FRONTEND_ORIGIN_ENV)
    if env_origin:
        candidates.append(env_origin)

    origins: list[str] = []
    for candidate in candidates:
        origin = _local_http_origin(candidate)
        if origin and origin not in origins:
            origins.append(origin)
    return tuple(origins)


def _local_http_origin(value: str) -> str | None:
    try:
        parsed = urlparse(value.strip())
        port = parsed.port
    except ValueError:
        return None

    if parsed.scheme != "http" or parsed.hostname not in LOOPBACK_HOSTS:
        return None
    if port is None or not 1 <= port <= 65535:
        return None
    if parsed.path not in {"", "/"} or parsed.params or parsed.query or parsed.fragment:
        return None
    return f"http://{parsed.hostname}:{port}"


def require_local_request_guard(request: Request) -> None:
    _validate_local_request_origin_and_host(request)
    expected_token = _get_local_request_guard_token(request)
    received_token = request.headers.get(LOCAL_REQUEST_GUARD_HEADER)
    if received_token is None or not received_token.strip():
        raise _local_request_guard_error(401, "local_request_guard_missing")
    if not hmac.compare_digest(received_token, expected_token):
        raise _local_request_guard_error(403, "local_request_guard_invalid")


def _validate_local_request_origin_and_host(request: Request) -> None:
    origin = request.headers.get("origin")
    allowed_origins = set(getattr(request.app.state, "local_request_guard_allowed_origins", ()))
    if origin is not None and origin not in allowed_origins:
        raise _local_request_guard_error(403, "local_request_origin_not_allowed")

    host = request.headers.get("host")
    if host and not _is_loopback_host_header(host):
        raise _local_request_guard_error(403, "local_request_host_not_allowed")


def _get_local_request_guard_token(request: Request) -> str:
    guard_value = getattr(request.app.state, "local_request_guard_token", None)
    if not isinstance(guard_value, str) or not guard_value:
        raise _local_request_guard_error(503, "local_request_guard_unavailable")
    return guard_value


def _local_request_guard_error(status_code: int, error_code: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"error": error_code})


def _is_loopback_host_header(value: str) -> bool:
    try:
        parsed = urlparse(f"http://{value.strip()}")
        port = parsed.port
    except ValueError:
        return False
    return parsed.hostname in LOOPBACK_HOSTS and (port is None or 1 <= port <= 65535)
