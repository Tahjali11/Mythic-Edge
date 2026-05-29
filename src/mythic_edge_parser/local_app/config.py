from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from .paths import LOCAL_APP_OBJECT_PREFIX, LOCAL_APP_SCHEMA_VERSION, LocalAppPaths, display_app_path

ALLOWED_CONFIG_FIELDS = (
    "player_log_path",
    "analytics_database_path",
    "backend_host",
    "backend_port",
    "frontend_origin",
)

_SECRET_FIELD_RE = re.compile(r"(api[_-]?key|secret|token|credential|oauth|webhook)", re.IGNORECASE)
_SAFE_UNEXPECTED_FIELD_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_-]{0,63}")


@dataclass(frozen=True, slots=True)
class LocalAppConfigRead:
    status: str
    values: dict[str, Any]
    loaded_fields: tuple[str, ...]
    unexpected_fields: tuple[str, ...]
    secret_like_field_count: int
    errors: tuple[str, ...]


def load_local_app_config_status(paths: LocalAppPaths) -> dict[str, object]:
    config_read = read_local_app_config(paths)
    return {
        "object": f"{LOCAL_APP_OBJECT_PREFIX}_config_status",
        "schema_version": LOCAL_APP_SCHEMA_VERSION,
        "status": _top_level_config_status(config_read.status),
        "config_file": {
            "display_path": display_app_path("config", "app_config.json"),
            "exists": paths.config_file.exists() if paths.config_file is not None else False,
            "status": config_read.status,
        },
        "allowed_fields": list(ALLOWED_CONFIG_FIELDS),
        "loaded_fields": list(config_read.loaded_fields),
        "unexpected_fields": list(config_read.unexpected_fields),
        "secret_like_field_count": config_read.secret_like_field_count,
        "errors": list(config_read.errors),
    }


def read_local_app_config(paths: LocalAppPaths) -> LocalAppConfigRead:
    config_file = paths.config_file
    if config_file is None:
        return LocalAppConfigRead(
            status="unavailable",
            values={},
            loaded_fields=(),
            unexpected_fields=(),
            secret_like_field_count=0,
            errors=("app_data_root_unavailable",),
        )
    if not config_file.exists():
        return LocalAppConfigRead(
            status="missing",
            values={},
            loaded_fields=(),
            unexpected_fields=(),
            secret_like_field_count=0,
            errors=(),
        )
    if not config_file.is_file():
        return LocalAppConfigRead(
            status="invalid_shape",
            values={},
            loaded_fields=(),
            unexpected_fields=(),
            secret_like_field_count=0,
            errors=("config_path_is_not_file",),
        )

    try:
        payload = json.loads(config_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return LocalAppConfigRead(
            status="invalid_json",
            values={},
            loaded_fields=(),
            unexpected_fields=(),
            secret_like_field_count=0,
            errors=("config_invalid_json",),
        )
    except OSError:
        return LocalAppConfigRead(
            status="unreadable",
            values={},
            loaded_fields=(),
            unexpected_fields=(),
            secret_like_field_count=0,
            errors=("config_unreadable",),
        )

    if not isinstance(payload, dict):
        return LocalAppConfigRead(
            status="invalid_shape",
            values={},
            loaded_fields=(),
            unexpected_fields=(),
            secret_like_field_count=0,
            errors=("config_not_object",),
        )

    allowed = set(ALLOWED_CONFIG_FIELDS)
    values = {key: payload[key] for key in ALLOWED_CONFIG_FIELDS if key in payload}
    loaded_fields = tuple(key for key in ALLOWED_CONFIG_FIELDS if key in payload)
    unexpected_safe_fields = tuple(
        sorted(key for key in payload if key not in allowed and _is_safe_unexpected_field_name(key))
    )
    secret_like_field_count = sum(
        1 for key in payload if key not in allowed and not _is_safe_unexpected_field_name(key)
    )

    errors = _config_shape_errors(values)

    return LocalAppConfigRead(
        status="invalid_shape" if errors else "present",
        values=values,
        loaded_fields=loaded_fields,
        unexpected_fields=unexpected_safe_fields,
        secret_like_field_count=secret_like_field_count,
        errors=tuple(errors),
    )


def _top_level_config_status(config_status: str) -> str:
    if config_status == "present":
        return "ok"
    if config_status == "missing":
        return "missing"
    if config_status == "unavailable":
        return "unavailable"
    return "error"


def _is_secret_field(field_name: str) -> bool:
    return _SECRET_FIELD_RE.search(field_name) is not None


def _is_safe_unexpected_field_name(field_name: object) -> bool:
    if not isinstance(field_name, str):
        return False
    return _SAFE_UNEXPECTED_FIELD_RE.fullmatch(field_name) is not None and not _is_secret_field(field_name)


def _config_shape_errors(values: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    backend_host = values.get("backend_host")
    if backend_host is not None and backend_host not in {"127.0.0.1", "localhost"}:
        errors.append("backend_host_must_be_loopback")

    backend_port = values.get("backend_port")
    if backend_port is not None and (
        not isinstance(backend_port, int) or isinstance(backend_port, bool) or not 1 <= backend_port <= 65535
    ):
        errors.append("backend_port_invalid")

    frontend_origin = values.get("frontend_origin")
    if frontend_origin is not None and not _is_local_frontend_origin(frontend_origin):
        errors.append("frontend_origin_must_be_local")

    return errors


def _is_local_frontend_origin(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return value.startswith("http://127.0.0.1:") or value.startswith("http://localhost:")
