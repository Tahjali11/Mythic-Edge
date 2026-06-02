from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from pathlib import Path
from urllib.parse import urlparse

from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.datastructures import UploadFile

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
from .config import load_local_app_config_status
from .import_jobs import (
    BrowserJsonlUploadFile,
    get_import_job,
    reject_browser_jsonl_upload_import,
    run_browser_jsonl_upload_import,
    run_manual_jsonl_import,
)
from .match_journal_cockpit import (
    JournalServiceFactory,
    match_journal_get_response,
    match_journal_post_response,
)
from .match_journal_runtime import build_match_journal_service_factory
from .paths import build_local_app_paths
from .setup_status import (
    build_analytics_database_status,
    build_health_status,
    build_runtime_state,
    build_setup_status,
)

FRONTEND_ORIGIN_ENV = "MYTHIC_EDGE_LOCAL_APP_FRONTEND_ORIGIN"
DEFAULT_FRONTEND_ORIGINS = ("http://127.0.0.1:5173", "http://localhost:5173")
LOOPBACK_HOSTS = {"127.0.0.1", "localhost"}
HISTORY_QUERY_PARAM_INVALID = "analytics_history_query_parameter_invalid"
HISTORY_QUERY_PARAM_NOT_ALLOWED = "analytics_history_query_parameter_not_allowed"


def create_app(
    *,
    app_data_root: Path | None = None,
    frontend_origins: Sequence[str] | None = None,
    env: Mapping[str, str] = os.environ,
    match_journal_service_factory: JournalServiceFactory | None = None,
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
    if allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=list(allowed_origins),
            allow_methods=["GET", "POST"],
            allow_headers=["Accept", "Content-Type"],
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

    @app.get("/api/analytics/database/status")
    def analytics_database_status() -> dict[str, object]:
        return build_analytics_database_status(local_app_paths)

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

    @app.get("/api/runtime/status")
    def runtime_state() -> dict[str, object]:
        return build_runtime_state()

    @app.get("/api/journal")
    async def match_journal(request: Request) -> object:
        return await match_journal_get_response(request, journal_service_factory)

    @app.post("/api/journal/notes")
    async def match_journal_notes(request: Request) -> object:
        return await match_journal_post_response("notes", request, journal_service_factory)

    @app.post("/api/journal/opponent-labels")
    async def match_journal_opponent_labels(request: Request) -> object:
        return await match_journal_post_response("opponent-labels", request, journal_service_factory)

    @app.post("/api/journal/review-flags")
    async def match_journal_review_flags(request: Request) -> object:
        return await match_journal_post_response("review-flags", request, journal_service_factory)

    @app.post("/api/journal/experiment-label")
    async def match_journal_experiment_label(request: Request) -> object:
        return await match_journal_post_response("experiment-label", request, journal_service_factory)

    @app.post("/api/journal/display-corrections")
    async def match_journal_display_corrections(request: Request) -> object:
        return await match_journal_post_response("display-corrections", request, journal_service_factory)

    @app.post("/api/imports/jsonl")
    def import_jsonl(request: object = Body(...)) -> dict[str, object]:
        return run_manual_jsonl_import(request, app_data_root=resolved_app_data_root)

    @app.post("/api/imports/jsonl/upload")
    async def import_jsonl_upload(request: Request) -> dict[str, object]:
        form = await request.form()
        form_files = list(form.getlist("files"))
        raw_source_artifact_labels = form.getlist("source_artifact_label")
        raw_source_artifact_label = raw_source_artifact_labels[-1] if raw_source_artifact_labels else None
        source_artifact_label = raw_source_artifact_label if isinstance(raw_source_artifact_label, str) else None

        upload_files: list[UploadFile] = []
        for value in form_files:
            if not isinstance(value, UploadFile):
                for upload_file in upload_files:
                    await upload_file.close()
                await form.close()
                return reject_browser_jsonl_upload_import(
                    "upload_file_invalid",
                    files_selected=len(form_files),
                    app_data_root=resolved_app_data_root,
                )
            upload_files.append(value)

        if raw_source_artifact_label is not None and not isinstance(raw_source_artifact_label, str):
            for upload_file in upload_files:
                await upload_file.close()
            await form.close()
            return reject_browser_jsonl_upload_import(
                "source_artifact_label_invalid",
                files_selected=len(form_files),
                app_data_root=resolved_app_data_root,
            )

        uploads: list[BrowserJsonlUploadFile] = []
        try:
            for upload_file in upload_files:
                uploads.append(
                    BrowserJsonlUploadFile(
                        filename=upload_file.filename or "",
                        content_bytes=await upload_file.read(),
                        content_type=upload_file.content_type or "",
                    )
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


def _reject_unknown_history_query_params(request: Request) -> None:
    allowed = {"limit", "offset"}
    if any(key not in allowed for key in request.query_params.keys()):
        raise HTTPException(status_code=422, detail={"error": HISTORY_QUERY_PARAM_NOT_ALLOWED})


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
