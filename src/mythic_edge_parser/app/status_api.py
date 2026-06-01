from __future__ import annotations

import json
import threading
from collections.abc import Callable, Mapping
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
from .match_journal_service import (
    MatchJournalService,
    MatchJournalServiceConflictError,
    MatchJournalServiceError,
    MatchJournalServiceNotFoundError,
    MatchJournalServiceValidationError,
)
from .runtime_surfaces import filter_match_history_payload, load_active_timeline_payload, load_match_history_payload

_SERVER: ThreadingHTTPServer | None = None
_THREAD: threading.Thread | None = None
_MATCH_JOURNAL_SERVICE_FACTORY: Callable[[], Any | None] | None = None
_TRANSPORT_FAILURE_COUNT_FIELD = "webhook_" + "failures"
_LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})
_JOURNAL_GET_ROUTES = frozenset({"/journal"})
_JOURNAL_POST_ROUTES = frozenset(
    {
        "/journal/notes",
        "/journal/pilot-error",
        "/journal/opponent-labels",
        "/journal/review-flags",
        "/journal/display-corrections",
    }
)
_JOURNAL_ROUTES = _JOURNAL_GET_ROUTES | _JOURNAL_POST_ROUTES
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
    "/journal",
    "/journal/notes",
    "/journal/pilot-error",
    "/journal/opponent-labels",
    "/journal/review-flags",
    "/journal/display-corrections",
]
_JOURNAL_QUERY_FIELDS = frozenset(
    {
        "journal_match_id",
        "journal_game_id",
        "parser_match_id",
        "parser_game_id",
        "game_number",
    }
)
_JOURNAL_CONTEXT_FIELDS = _JOURNAL_QUERY_FIELDS
_COMMON_SERVICE_OPTIONS = frozenset(
    {
        "author_label",
        "source_surface",
        "privacy_label",
        "note_format",
        "priority_label",
        "reference_id",
        "created_at",
        "updated_at",
        "valid_from",
    }
)
_PILOT_ERROR_STATUSES = frozenset({"yes", "no", "unknown", "not_reviewed"})
_NOTE_SCOPES = frozenset({"match", "game", "sideboarding", "unattached"})
_DISPLAY_CORRECTION_FIELDS = frozenset(
    {
        "target_surface",
        "target_field",
        "original_value_label",
        "proposed_value_label",
        "override_reason",
        "override_status",
        "effect_scope",
        "author_label",
        "source_surface",
        "privacy_label",
        "created_at",
        "updated_at",
    }
)


def configure_match_journal_service_factory(
    factory: Callable[[], Any | None] | None,
) -> None:
    """Configure an explicit Match Journal service factory for local API routes."""
    global _MATCH_JOURNAL_SERVICE_FACTORY

    _MATCH_JOURNAL_SERVICE_FACTORY = factory


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
        _TRANSPORT_FAILURE_COUNT_FIELD: status_payload.get(_TRANSPORT_FAILURE_COUNT_FIELD, 0),
        "event_failures": status_payload.get("event_failures", 0),
        "router_failures": status_payload.get("router_failures", 0),
    }


def _actions_payload(*, match_id: str) -> dict[str, Any]:
    payload = _load_json_file(ACTIVE_MATCH_ACTIONS_PATH) if not match_id else None
    if payload is None:
        payload = load_active_match_actions_payload(match_id=match_id)
    return payload


def _loopback_status_api_host() -> bool:
    return STATUS_API_HOST in _LOOPBACK_HOSTS


def _journal_response(result: Mapping[str, Any], warnings: list[Any] | None = None) -> dict[str, Any]:
    return {
        "object": "match_journal_api_response",
        "ok": True,
        "result": _json_safe(result),
        "warnings": _json_safe(warnings or []),
    }


def _journal_error(status_code: int, code: str, message: str) -> tuple[int, dict[str, Any]]:
    return status_code, {
        "object": "match_journal_api_response",
        "ok": False,
        "error": {"code": code, "message": message},
        "warnings": [],
    }


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_json_safe(item) for item in value]
    if hasattr(value, "keys"):
        return {str(key): _json_safe(value[key]) for key in value.keys()}
    return value


def _match_journal_service() -> Any | None:
    if _MATCH_JOURNAL_SERVICE_FACTORY is None:
        return None
    return _MATCH_JOURNAL_SERVICE_FACTORY()


def _journal_route_service() -> tuple[int, dict[str, Any]] | Any:
    if not _loopback_status_api_host():
        return _journal_error(HTTPStatus.SERVICE_UNAVAILABLE, "service_unavailable", "journal service unavailable")
    try:
        service = _match_journal_service()
    except Exception:
        return _journal_error(HTTPStatus.SERVICE_UNAVAILABLE, "service_unavailable", "journal service unavailable")
    if service is None:
        return _journal_error(HTTPStatus.SERVICE_UNAVAILABLE, "service_unavailable", "journal service unavailable")
    return service


def _journal_context(value: object) -> tuple[dict[str, Any] | None, tuple[int, dict[str, Any]] | None]:
    if value is None:
        return None, None
    if not isinstance(value, dict):
        return None, _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    unsupported = sorted(set(value) - _JOURNAL_CONTEXT_FIELDS)
    if unsupported:
        return None, _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    context = dict(value)
    if "game_number" in context:
        game_number, error = _positive_int("game_number", context["game_number"])
        if error is not None:
            return None, error
        context["game_number"] = game_number
    return context, None


def _positive_int(name: str, value: object) -> tuple[int | None, tuple[int, dict[str, Any]] | None]:
    if isinstance(value, bool):
        return None, _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    if isinstance(value, int):
        number = value
    elif isinstance(value, str) and value.strip().isdigit():
        number = int(value)
    else:
        return None, _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    if number <= 0:
        return None, _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    return number, None


def _required_text(body: Mapping[str, Any], name: str) -> tuple[str | None, tuple[int, dict[str, Any]] | None]:
    value = body.get(name)
    if not isinstance(value, str) or not value.strip():
        return None, _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    return value, None


def _optional_text(body: Mapping[str, Any], name: str) -> tuple[str | None, tuple[int, dict[str, Any]] | None]:
    if name not in body or body[name] is None:
        return None, None
    value = body[name]
    if not isinstance(value, str) or not value.strip():
        return None, _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    return value, None


def _reject_unsupported_fields(body: Mapping[str, Any], allowed: frozenset[str]) -> tuple[int, dict[str, Any]] | None:
    unsupported = sorted(set(body) - allowed)
    if unsupported:
        return _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    return None


def _common_options(body: Mapping[str, Any], extra_excluded: frozenset[str]) -> dict[str, Any]:
    return {key: body[key] for key in _COMMON_SERVICE_OPTIONS if key in body and key not in extra_excluded}


def _journal_success_from_service(result: Mapping[str, Any]) -> tuple[int, dict[str, Any]]:
    warnings = result.get("warnings", [])
    response_warnings = list(warnings) if isinstance(warnings, list) else []
    return HTTPStatus.OK, _journal_response({"service_result": dict(result)}, response_warnings)


def _handle_service_error(exc: Exception) -> tuple[int, dict[str, Any]]:
    if isinstance(exc, MatchJournalServiceValidationError):
        return _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    if isinstance(exc, MatchJournalServiceNotFoundError):
        return _journal_error(HTTPStatus.NOT_FOUND, "not_found", "journal record not found")
    if isinstance(exc, MatchJournalServiceConflictError):
        return _journal_error(HTTPStatus.CONFLICT, "conflict", "journal context conflict")
    if isinstance(exc, MatchJournalServiceError):
        return _journal_error(HTTPStatus.INTERNAL_SERVER_ERROR, "internal_error", "journal service operation failed")
    return _journal_error(HTTPStatus.INTERNAL_SERVER_ERROR, "internal_error", "internal error")


def _parse_journal_json_body(body: bytes | str | None) -> dict[str, Any] | tuple[int, dict[str, Any]]:
    if body is None:
        return _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    try:
        raw = body.decode("utf-8") if isinstance(body, bytes) else body
        payload = json.loads(raw)
    except Exception:
        return _journal_error(HTTPStatus.BAD_REQUEST, "malformed_json", "request body is not valid JSON")
    if not isinstance(payload, dict):
        return _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    return payload


def _journal_get_payload(query: Mapping[str, str]) -> tuple[int, dict[str, Any]]:
    unsupported = sorted(set(query) - _JOURNAL_QUERY_FIELDS)
    if unsupported or not query:
        return _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    context: dict[str, Any] = dict(query)
    if "game_number" in context:
        game_number, error = _positive_int("game_number", context["game_number"])
        if error is not None:
            return error
        context["game_number"] = game_number
    service_or_error = _journal_route_service()
    if isinstance(service_or_error, tuple):
        return service_or_error
    try:
        bundle = service_or_error.get_journal_bundle(context)
    except Exception as exc:
        return _handle_service_error(exc)
    if bundle is None:
        return _journal_error(HTTPStatus.NOT_FOUND, "not_found", "journal bundle not found")
    warnings = bundle.get("warnings", []) if isinstance(bundle, dict) else []
    return HTTPStatus.OK, _journal_response({"bundle": bundle}, list(warnings) if isinstance(warnings, list) else [])


def _journal_post_payload(route: str, body: bytes | str | None) -> tuple[int, dict[str, Any]]:
    payload = _parse_journal_json_body(body)
    if isinstance(payload, tuple):
        return payload
    service_or_error = _journal_route_service()
    if isinstance(service_or_error, tuple):
        return service_or_error
    try:
        if route == "/journal/notes":
            return _journal_notes_payload(service_or_error, payload)
        if route == "/journal/pilot-error":
            return _journal_pilot_error_payload(service_or_error, payload)
        if route == "/journal/opponent-labels":
            return _journal_opponent_labels_payload(service_or_error, payload)
        if route == "/journal/review-flags":
            return _journal_review_flags_payload(service_or_error, payload)
        if route == "/journal/display-corrections":
            return _journal_display_corrections_payload(service_or_error, payload)
    except Exception as exc:
        return _handle_service_error(exc)
    return _journal_error(HTTPStatus.NOT_FOUND, "not_found_route", "route not found")


def _journal_notes_payload(service: MatchJournalService, body: Mapping[str, Any]) -> tuple[int, dict[str, Any]]:
    allowed = frozenset({"note_text", "note_scope", "context"}) | _COMMON_SERVICE_OPTIONS
    if error := _reject_unsupported_fields(body, allowed):
        return error
    note_text, error = _required_text(body, "note_text")
    if error is not None:
        return error
    note_scope, error = _required_text(body, "note_scope")
    if error is not None:
        return error
    if note_scope not in _NOTE_SCOPES:
        return _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    context, error = _journal_context(body.get("context"))
    if error is not None:
        return error
    options = _common_options(body, frozenset({"context", "note_text", "note_scope"}))
    if note_scope == "unattached":
        return _journal_success_from_service(service.record_unattached_note(note_text, **options))
    if context is None:
        return _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    if note_scope == "match":
        return _journal_success_from_service(service.record_match_note(context, note_text, **options))
    if note_scope == "game":
        return _journal_success_from_service(service.record_game_note(context, note_text, **options))
    return _journal_success_from_service(service.record_sideboarding_note(context, note_text, **options))


def _journal_pilot_error_payload(service: MatchJournalService, body: Mapping[str, Any]) -> tuple[int, dict[str, Any]]:
    allowed = frozenset({"context", "status", "reason", "note_text"}) | _COMMON_SERVICE_OPTIONS
    if error := _reject_unsupported_fields(body, allowed):
        return error
    context, error = _journal_context(body.get("context"))
    if error is not None or context is None:
        return error or _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    status, error = _required_text(body, "status")
    if error is not None:
        return error
    if status not in _PILOT_ERROR_STATUSES:
        return _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    reason, error = _optional_text(body, "reason")
    if error is not None:
        return error
    note_text, error = _optional_text(body, "note_text")
    if error is not None:
        return error
    options = _common_options(body, frozenset({"context", "status", "reason", "note_text"}))
    if reason is not None or note_text is not None:
        return _journal_success_from_service(
            service.record_pilot_error_review(context, status=status, reason=reason, note_text=note_text, **options)
        )
    return _journal_success_from_service(service.set_pilot_error_status(context, status, **options))


def _journal_opponent_labels_payload(
    service: MatchJournalService,
    body: Mapping[str, Any],
) -> tuple[int, dict[str, Any]]:
    allowed = frozenset({"context", "archetype", "tier"}) | _COMMON_SERVICE_OPTIONS
    if error := _reject_unsupported_fields(body, allowed):
        return error
    context, error = _journal_context(body.get("context"))
    if error is not None or context is None:
        return error or _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    archetype, error = _optional_text(body, "archetype")
    if error is not None:
        return error
    tier, error = _optional_text(body, "tier")
    if error is not None:
        return error
    if archetype is None and tier is None:
        return _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    options = _common_options(body, frozenset({"context", "archetype", "tier"}))
    result = service.set_opponent_labels(context, archetype=archetype, tier=tier, **options)
    return _journal_success_from_service(result)


def _journal_review_flags_payload(service: MatchJournalService, body: Mapping[str, Any]) -> tuple[int, dict[str, Any]]:
    allowed = frozenset({"context", "flag_type", "flag_status", "reason"}) | _COMMON_SERVICE_OPTIONS
    if error := _reject_unsupported_fields(body, allowed):
        return error
    context, error = _journal_context(body.get("context"))
    if error is not None or context is None:
        return error or _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    flag_type, error = _required_text(body, "flag_type")
    if error is not None:
        return error
    options = _common_options(body, frozenset({"context", "flag_type"}))
    for name in ("flag_status", "reason"):
        if name in body:
            options[name] = body[name]
    return _journal_success_from_service(service.flag_for_review(context, flag_type, **options))


def _journal_display_corrections_payload(
    service: MatchJournalService,
    body: Mapping[str, Any],
) -> tuple[int, dict[str, Any]]:
    allowed = frozenset({"context"}) | _DISPLAY_CORRECTION_FIELDS
    if error := _reject_unsupported_fields(body, allowed):
        return error
    context, error = _journal_context(body.get("context"))
    if error is not None or context is None:
        return error or _journal_error(HTTPStatus.BAD_REQUEST, "validation_error", "request validation failed")
    request = {key: body[key] for key in _DISPLAY_CORRECTION_FIELDS if key in body}
    request.setdefault("effect_scope", "journal_display_only")
    return _journal_success_from_service(service.propose_display_correction(context, request))


def _journal_api_payload_for_request(
    method: str,
    route: str,
    query: Mapping[str, str],
    body: bytes | str | None = None,
) -> tuple[int, dict[str, Any]]:
    if route not in _JOURNAL_ROUTES:
        return _journal_error(HTTPStatus.NOT_FOUND, "not_found_route", "route not found")
    if method == "GET" and route in _JOURNAL_POST_ROUTES:
        return _journal_error(HTTPStatus.METHOD_NOT_ALLOWED, "method_not_allowed", "method not allowed")
    if method == "POST" and route in _JOURNAL_GET_ROUTES:
        return _journal_error(HTTPStatus.METHOD_NOT_ALLOWED, "method_not_allowed", "method not allowed")
    if method == "GET":
        return _journal_get_payload(query)
    if method == "POST":
        return _journal_post_payload(route, body)
    return _journal_error(HTTPStatus.METHOD_NOT_ALLOWED, "method_not_allowed", "method not allowed")


def _api_payload_for_request(route: str, query: dict[str, str]) -> tuple[int, dict[str, Any]]:
    if route in {"", "/"}:
        return HTTPStatus.OK, {
            "object": "manasight_status_api",
            "routes": list(_ROUTES),
        }

    if route in _JOURNAL_ROUTES:
        return _journal_api_payload_for_request("GET", route, query)

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
        self._send_json_response(status_code, payload)

    def do_POST(self) -> None:  # noqa: N802
        route, query = _request_query(self.path)
        content_length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(content_length) if content_length > 0 else b""
        if route in _JOURNAL_ROUTES:
            status_code, payload = _journal_api_payload_for_request("POST", route, query, body)
        elif route in _ROUTES:
            status_code, payload = _journal_error(
                HTTPStatus.METHOD_NOT_ALLOWED,
                "method_not_allowed",
                "method not allowed",
            )
        else:
            status_code, payload = _journal_error(HTTPStatus.NOT_FOUND, "not_found_route", "route not found")
        self._send_json_response(status_code, payload)

    def do_PUT(self) -> None:  # noqa: N802
        self._handle_unsupported_method("PUT")

    def do_PATCH(self) -> None:  # noqa: N802
        self._handle_unsupported_method("PATCH")

    def do_DELETE(self) -> None:  # noqa: N802
        self._handle_unsupported_method("DELETE")

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._handle_unsupported_method("OPTIONS")

    def _handle_unsupported_method(self, method: str) -> None:
        route, query = _request_query(self.path)
        if route in _JOURNAL_ROUTES:
            status_code, payload = _journal_api_payload_for_request(method, route, query)
            self._send_json_response(status_code, payload)
            return
        self.send_error(HTTPStatus.NOT_IMPLEMENTED, f"Unsupported method ({method})")

    def _send_json_response(self, status_code: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return
