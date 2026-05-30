from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from pathlib import Path
from urllib.parse import urlparse

from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import load_local_app_config_status
from .import_jobs import get_import_job, run_manual_jsonl_import
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


def create_app(
    *,
    app_data_root: Path | None = None,
    frontend_origins: Sequence[str] | None = None,
    env: Mapping[str, str] = os.environ,
) -> FastAPI:
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
        return build_setup_status(build_local_app_paths(app_data_root))

    @app.get("/api/app/config")
    def app_config() -> dict[str, object]:
        return load_local_app_config_status(build_local_app_paths(app_data_root))

    @app.get("/api/app/paths")
    def app_paths() -> dict[str, object]:
        from .paths import build_path_status

        return build_path_status(build_local_app_paths(app_data_root))

    @app.get("/api/analytics/database/status")
    def analytics_database_status() -> dict[str, object]:
        return build_analytics_database_status(build_local_app_paths(app_data_root))

    @app.get("/api/runtime/status")
    def runtime_state() -> dict[str, object]:
        return build_runtime_state()

    @app.post("/api/imports/jsonl")
    def import_jsonl(request: object = Body(...)) -> dict[str, object]:
        return run_manual_jsonl_import(request, app_data_root=app_data_root)

    @app.get("/api/imports/jobs/{job_id}")
    def import_job(job_id: str) -> dict[str, object]:
        job = get_import_job(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail={"error": "not_found"})
        return job

    return app


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
