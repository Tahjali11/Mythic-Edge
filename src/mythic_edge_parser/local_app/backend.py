from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI

from .config import load_local_app_config_status
from .paths import build_local_app_paths
from .setup_status import (
    build_analytics_database_status,
    build_health_status,
    build_runtime_state,
    build_setup_status,
)


def create_app(*, app_data_root: Path | None = None) -> FastAPI:
    app = FastAPI(
        title="Mythic Edge Local App Backend",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
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

    return app
