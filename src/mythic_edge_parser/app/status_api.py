from __future__ import annotations

import json
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .card_performance import load_card_performance_payload
from .config import (
    ACTIVE_DECK_PROFILE_PATH,
    ACTIVE_MATCH_ACTIONS_PATH,
    ACTIVE_MATCH_SNAPSHOT_PATH,
    CARD_PERFORMANCE_PATH,
    COLLECTION_PROFILE_PATH,
    ENABLE_STATUS_API,
    STATUS_API_HOST,
    STATUS_API_PORT,
    STATUS_ROOT,
)
from .gameplay_actions import load_active_match_actions_payload
from .runtime_surfaces import filter_match_history_payload, load_active_timeline_payload, load_match_history_payload

_SERVER: ThreadingHTTPServer | None = None
_THREAD: threading.Thread | None = None
_ROUTES = [
    "/health",
    "/status",
    "/active-match",
    "/timeline",
    "/actions",
    "/active-deck",
    "/match-history",
    "/collection",
    "/card-performance",
]


def start_status_api_server() -> dict[str, Any] | None:
    global _SERVER, _THREAD

    if not ENABLE_STATUS_API:
        return None
    if _SERVER is not None:
        return _server_info(_SERVER)

    server = ThreadingHTTPServer((STATUS_API_HOST, STATUS_API_PORT), _StatusApiHandler)
    server.daemon_threads = True
    thread = threading.Thread(
        target=server.serve_forever,
        name="manasight-status-api",
        daemon=True,
    )
    thread.start()
    _SERVER = server
    _THREAD = thread
    return _server_info(server)


def stop_status_api_server() -> None:
    global _SERVER, _THREAD

    if _SERVER is None:
        return
    _SERVER.shutdown()
    _SERVER.server_close()
    if _THREAD is not None:
        _THREAD.join(timeout=2)
    _SERVER = None
    _THREAD = None


def reset_status_api_runtime_state() -> None:
    stop_status_api_server()


def _server_info(server: ThreadingHTTPServer) -> dict[str, Any]:
    host, port = server.server_address[:2]
    return {
        "host": str(host),
        "port": int(port),
        "base_url": f"http://{host}:{port}",
    }


def _load_json_file(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if isinstance(payload, dict):
        return payload
    return None


def _status_snapshot_path() -> Path:
    return STATUS_ROOT / "manasight_status_latest.json"


def _not_found_payload(message: str) -> dict[str, Any]:
    return {"ok": False, "msg": message}


def _artifact_response(path: Path, *, missing_message: str) -> tuple[int, dict[str, Any]]:
    payload = _load_json_file(path)
    if payload is None:
        return HTTPStatus.NOT_FOUND, _not_found_payload(missing_message)
    return HTTPStatus.OK, payload


def _health_payload() -> dict[str, Any]:
    status_payload = _load_json_file(_status_snapshot_path()) or {}
    return {
        "object": "manasight_health",
        "status": status_payload.get("status", "unknown"),
        "updated_at": status_payload.get("updated_at", ""),
        "current_match_id": status_payload.get("current_match_id", ""),
        "webhook_failures": status_payload.get("webhook_failures", 0),
        "event_failures": status_payload.get("event_failures", 0),
        "router_failures": status_payload.get("router_failures", 0),
    }


def _actions_payload(*, match_id: str) -> dict[str, Any]:
    payload = _load_json_file(ACTIVE_MATCH_ACTIONS_PATH) if not match_id else None
    if payload is None:
        payload = load_active_match_actions_payload(match_id=match_id)
    return payload


def _api_payload_for_request(route: str, query: dict[str, str]) -> tuple[int, dict[str, Any]]:
    if route in {"", "/"}:
        return HTTPStatus.OK, {
            "object": "manasight_status_api",
            "routes": list(_ROUTES),
        }

    if route == "/health":
        return HTTPStatus.OK, _health_payload()

    if route == "/status":
        return _artifact_response(_status_snapshot_path(), missing_message="status file not found")

    if route == "/active-match":
        return _artifact_response(
            ACTIVE_MATCH_SNAPSHOT_PATH,
            missing_message="active match snapshot not found",
        )

    if route == "/timeline":
        match_id = query.get("match_id", "")
        payload = load_active_timeline_payload(match_id=match_id)
        return HTTPStatus.OK, payload

    if route == "/actions":
        return HTTPStatus.OK, _actions_payload(match_id=query.get("match_id", ""))

    if route == "/active-deck":
        return _artifact_response(
            ACTIVE_DECK_PROFILE_PATH,
            missing_message="active deck profile not found",
        )

    if route == "/match-history":
        payload = filter_match_history_payload(load_match_history_payload(), query)
        return HTTPStatus.OK, payload

    if route == "/collection":
        return _artifact_response(
            COLLECTION_PROFILE_PATH,
            missing_message="collection profile not found",
        )

    if route == "/card-performance":
        payload = _load_json_file(CARD_PERFORMANCE_PATH)
        if payload is None:
            payload = load_card_performance_payload()
        return HTTPStatus.OK, payload

    return HTTPStatus.NOT_FOUND, _not_found_payload("not found")


def _request_query(parsed_path: str) -> tuple[str, dict[str, str]]:
    parsed = urlparse(parsed_path)
    route = parsed.path.rstrip("/")
    query = {
        key: values[0]
        for key, values in parse_qs(parsed.query, keep_blank_values=True).items()
        if values
    }
    return route, query


class _StatusApiHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        route, query = _request_query(self.path)
        status_code, payload = _api_payload_for_request(route, query)
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return
