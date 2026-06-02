from __future__ import annotations

from collections.abc import Callable, Mapping
from http import HTTPStatus
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse

from mythic_edge_parser.app.match_journal_service import (
    MatchJournalServiceConflictError,
    MatchJournalServiceError,
    MatchJournalServiceNotFoundError,
    MatchJournalServiceValidationError,
)

MATCH_JOURNAL_COCKPIT_OBJECT = "mythic_edge_local_app_match_journal"
MATCH_JOURNAL_COCKPIT_SCHEMA_VERSION = "match_journal_cockpit_ui.v1"
UNATTACHED_SMOKE_NOTE_PREFIX = "MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW"

JournalServiceFactory = Callable[[], Any | None]

_JOURNAL_CONTEXT_FIELDS = frozenset(
    {
        "journal_match_id",
        "journal_game_id",
        "parser_match_id",
        "parser_game_id",
        "game_number",
        "attachment_status",
    }
)
_JOURNAL_QUERY_FIELDS = _JOURNAL_CONTEXT_FIELDS
_UNATTACHED_NOTE_READBACK_QUERY_FIELDS = frozenset({"journal_note_id", "note_scope"})
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
_JOURNAL_DISPLAY_ONLY = "journal_display_only"
_SERVICE_RESULT_SUMMARY_FIELDS = ("action", "status", "primary_record_type", "primary_record_id")
_UNSAFE_SERVICE_RESULT_MARKERS = (
    "player.log",
    "script.google.com",
    "webhook",
    "api_key",
    "apikey",
    "access_token",
    "bearer ",
    "secret",
    "password",
    "token",
)


async def match_journal_get_response(
    request: Request,
    service_factory: JournalServiceFactory | None,
) -> JSONResponse:
    unsupported = sorted(set(request.query_params.keys()) - _JOURNAL_QUERY_FIELDS)
    if unsupported or not request.query_params:
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")

    context: dict[str, Any] = dict(request.query_params)
    if not _has_attachment_reference(context):
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    if "game_number" in context:
        game_number, error = _positive_int(context["game_number"])
        if error is not None:
            return error
        context["game_number"] = game_number

    service_or_error = _service_or_error(service_factory)
    if isinstance(service_or_error, JSONResponse):
        return service_or_error

    try:
        bundle = service_or_error.get_journal_bundle(context)
    except Exception as exc:
        return _service_error_response(exc)
    if bundle is None:
        return _error_response(HTTPStatus.NOT_FOUND, "missing", "not_found")

    warnings = bundle.get("warnings", []) if isinstance(bundle, Mapping) else []
    return _response(
        HTTPStatus.OK,
        "ok",
        {"bundle": _json_safe(bundle)},
        warnings=list(warnings) if isinstance(warnings, list) else [],
    )


async def match_journal_note_readback_response(
    request: Request,
    service_factory: JournalServiceFactory | None,
) -> JSONResponse:
    unsupported = sorted(set(request.query_params.keys()) - _UNATTACHED_NOTE_READBACK_QUERY_FIELDS)
    if unsupported:
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    if any(len(request.query_params.getlist(key)) != 1 for key in _UNATTACHED_NOTE_READBACK_QUERY_FIELDS):
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    if request.query_params.get("note_scope") != "unattached":
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")

    journal_note_id, error = _journal_note_id(request.query_params.get("journal_note_id"))
    if error is not None:
        return error

    service_or_error = _service_or_error(service_factory)
    if isinstance(service_or_error, JSONResponse):
        return service_or_error
    readback = getattr(service_or_error, "get_unattached_note_summary", None)
    if not callable(readback):
        return _error_response(HTTPStatus.SERVICE_UNAVAILABLE, "unavailable", "service_unavailable")

    try:
        note = readback(journal_note_id, smoke_marker_prefix=UNATTACHED_SMOKE_NOTE_PREFIX)
    except Exception as exc:
        return _service_error_response(exc)
    if note is None:
        return _error_response(HTTPStatus.NOT_FOUND, "missing", "not_found")
    return _response(HTTPStatus.OK, "ok", {"note": _json_safe(note)})


async def match_journal_post_response(
    route_name: str,
    request: Request,
    service_factory: JournalServiceFactory | None,
) -> JSONResponse:
    payload = await _request_json(request)
    if isinstance(payload, JSONResponse):
        return payload

    service_or_error = _service_or_error(service_factory)
    if isinstance(service_or_error, JSONResponse):
        return service_or_error

    try:
        if route_name == "notes":
            return _notes_response(service_or_error, payload)
        if route_name == "opponent-labels":
            return _opponent_labels_response(service_or_error, payload)
        if route_name == "review-flags":
            return _review_flags_response(service_or_error, payload)
        if route_name == "experiment-label":
            return _experiment_label_response(service_or_error, payload)
        if route_name == "display-corrections":
            return _display_corrections_response(service_or_error, payload)
    except Exception as exc:
        return _service_error_response(exc)
    return _error_response(HTTPStatus.NOT_FOUND, "missing", "not_found")


async def _request_json(request: Request) -> dict[str, Any] | JSONResponse:
    try:
        payload = await request.json()
    except Exception:
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "malformed_json")
    if not isinstance(payload, dict):
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    return payload


def _service_or_error(service_factory: JournalServiceFactory | None) -> Any | JSONResponse:
    if service_factory is None:
        return _error_response(HTTPStatus.SERVICE_UNAVAILABLE, "unavailable", "service_unavailable")
    try:
        service = service_factory()
    except Exception:
        return _error_response(HTTPStatus.SERVICE_UNAVAILABLE, "unavailable", "service_unavailable")
    if service is None:
        return _error_response(HTTPStatus.SERVICE_UNAVAILABLE, "unavailable", "service_unavailable")
    return service


def _notes_response(service: Any, body: Mapping[str, Any]) -> JSONResponse:
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
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")

    context, error = _journal_context(body.get("context"))
    if error is not None:
        return error
    options = _common_options(body, frozenset({"context", "note_text", "note_scope"}))

    if note_scope == "unattached":
        if context:
            return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
        return _success_from_service(service.record_unattached_note(note_text, **options))

    if context is None or not _has_attachment_reference(context):
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    if note_scope == "match":
        return _success_from_service(service.record_match_note(context, note_text, **options))
    if note_scope == "game":
        return _success_from_service(service.record_game_note(context, note_text, **options))
    return _success_from_service(service.record_sideboarding_note(context, note_text, **options))


def _opponent_labels_response(service: Any, body: Mapping[str, Any]) -> JSONResponse:
    allowed = frozenset({"context", "archetype", "tier"}) | _COMMON_SERVICE_OPTIONS
    if error := _reject_unsupported_fields(body, allowed):
        return error
    context, error = _required_context(body)
    if error is not None:
        return error
    archetype, error = _optional_text(body, "archetype")
    if error is not None:
        return error
    tier, error = _optional_text(body, "tier")
    if error is not None:
        return error
    if archetype is None and tier is None:
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    result = service.set_opponent_labels(
        context,
        archetype=archetype,
        tier=tier,
        **_common_options(body, frozenset({"context", "archetype", "tier"})),
    )
    return _success_from_service(result)


def _review_flags_response(service: Any, body: Mapping[str, Any]) -> JSONResponse:
    allowed = frozenset({"context", "flag_type", "flag_status", "reason"}) | _COMMON_SERVICE_OPTIONS
    if error := _reject_unsupported_fields(body, allowed):
        return error
    context, error = _required_context(body)
    if error is not None:
        return error
    flag_type, error = _required_text(body, "flag_type")
    if error is not None:
        return error
    options = _common_options(body, frozenset({"context", "flag_type"}))
    for name in ("flag_status", "reason"):
        if name in body:
            options[name] = body[name]
    return _success_from_service(service.flag_for_review(context, flag_type, **options))


def _experiment_label_response(service: Any, body: Mapping[str, Any]) -> JSONResponse:
    allowed = frozenset({"context", "experiment_label", "experiment_id"}) | _COMMON_SERVICE_OPTIONS
    if error := _reject_unsupported_fields(body, allowed):
        return error
    context, error = _required_context(body)
    if error is not None:
        return error
    experiment_label = body.get("experiment_label")
    experiment_id = body.get("experiment_id")
    if experiment_label is not None and experiment_id is not None:
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    raw_value = experiment_label if experiment_label is not None else experiment_id
    if not isinstance(raw_value, str) or not raw_value.strip():
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    options = _common_options(body, frozenset({"context", "experiment_label", "experiment_id"}))
    return _success_from_service(service.set_experiment_label(context, raw_value, **options))


def _display_corrections_response(service: Any, body: Mapping[str, Any]) -> JSONResponse:
    allowed = frozenset({"context"}) | _DISPLAY_CORRECTION_FIELDS
    if error := _reject_unsupported_fields(body, allowed):
        return error
    context, error = _required_context(body)
    if error is not None:
        return error
    request = {key: body[key] for key in _DISPLAY_CORRECTION_FIELDS if key in body}
    if request.get("effect_scope", _JOURNAL_DISPLAY_ONLY) != _JOURNAL_DISPLAY_ONLY:
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    request.setdefault("effect_scope", _JOURNAL_DISPLAY_ONLY)
    return _success_from_service(service.propose_display_correction(context, request))


def _required_context(body: Mapping[str, Any]) -> tuple[dict[str, Any], JSONResponse | None]:
    context, error = _journal_context(body.get("context"))
    if error is not None:
        return {}, error
    if context is None or not _has_attachment_reference(context):
        return {}, _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    return context, None


def _journal_context(value: object) -> tuple[dict[str, Any] | None, JSONResponse | None]:
    if value is None:
        return None, None
    if not isinstance(value, dict):
        return None, _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    if error := _reject_unsupported_fields(value, _JOURNAL_CONTEXT_FIELDS):
        return None, error
    context = dict(value)
    if "game_number" in context:
        game_number, error = _positive_int(context["game_number"])
        if error is not None:
            return None, error
        context["game_number"] = game_number
    return context, None


def _has_attachment_reference(context: Mapping[str, Any]) -> bool:
    return bool(
        context.get("journal_match_id")
        or context.get("journal_game_id")
        or context.get("parser_match_id")
        or context.get("parser_game_id")
    )


def _positive_int(value: object) -> tuple[int | None, JSONResponse | None]:
    if isinstance(value, bool):
        return None, _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    if isinstance(value, int):
        number = value
    elif isinstance(value, str) and value.strip().isdigit():
        number = int(value)
    else:
        return None, _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    if number <= 0:
        return None, _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    return number, None


def _journal_note_id(value: object) -> tuple[str | None, JSONResponse | None]:
    if not isinstance(value, str):
        return None, _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    text = value.strip()
    if _safe_service_summary_value(text) != text:
        return None, _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    return text, None


def _required_text(body: Mapping[str, Any], name: str) -> tuple[str | None, JSONResponse | None]:
    value = body.get(name)
    if not isinstance(value, str) or not value.strip():
        return None, _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    return value, None


def _optional_text(body: Mapping[str, Any], name: str) -> tuple[str | None, JSONResponse | None]:
    if name not in body or body[name] is None:
        return None, None
    value = body[name]
    if not isinstance(value, str) or not value.strip():
        return None, _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    return value, None


def _reject_unsupported_fields(body: Mapping[str, Any], allowed: frozenset[str]) -> JSONResponse | None:
    unsupported = sorted(set(body) - allowed)
    if unsupported:
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    return None


def _common_options(body: Mapping[str, Any], excluded: frozenset[str]) -> dict[str, Any]:
    return {key: body[key] for key in _COMMON_SERVICE_OPTIONS if key in body and key not in excluded}


def _success_from_service(result: Mapping[str, Any]) -> JSONResponse:
    warnings = result.get("warnings", [])
    response_warnings = list(warnings) if isinstance(warnings, list) else []
    return _response(
        HTTPStatus.OK,
        "ok",
        {"service_result": _service_result_summary(result)},
        warnings=response_warnings,
    )


def _service_result_summary(result: Mapping[str, Any]) -> dict[str, Any]:
    summary = {field: _safe_service_summary_value(result.get(field)) for field in _SERVICE_RESULT_SUMMARY_FIELDS}
    summary["record_counts"] = _service_record_counts(result.get("records"))
    return summary


def _safe_service_summary_value(value: object) -> object:
    if value is None or isinstance(value, int | float | bool):
        return value
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text or len(text) > 160:
        return "redacted"
    lower_text = text.lower()
    if any(marker in lower_text for marker in _UNSAFE_SERVICE_RESULT_MARKERS):
        return "redacted"
    if "://" in text or "\\" in text or "/" in text:
        return "redacted"
    if not all(char.isalnum() or char in "_.:-" for char in text):
        return "redacted"
    return text


def _service_record_counts(records: object) -> dict[str, int]:
    if not isinstance(records, Mapping):
        return {}
    counts: dict[str, int] = {}
    for raw_name, record in records.items():
        name = _safe_service_summary_value(raw_name)
        if not isinstance(name, str) or name == "redacted":
            continue
        counts[name] = _service_record_count(record)
    return counts


def _service_record_count(record: object) -> int:
    if isinstance(record, list | tuple):
        return len(record)
    return 1


def _service_error_response(exc: Exception) -> JSONResponse:
    if isinstance(exc, MatchJournalServiceValidationError):
        return _error_response(HTTPStatus.BAD_REQUEST, "error", "validation_error")
    if isinstance(exc, MatchJournalServiceNotFoundError):
        return _error_response(HTTPStatus.NOT_FOUND, "missing", "not_found")
    if isinstance(exc, MatchJournalServiceConflictError):
        return _error_response(HTTPStatus.CONFLICT, "error", "conflict")
    if isinstance(exc, MatchJournalServiceError):
        return _error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "error", "internal_error")
    return _error_response(HTTPStatus.INTERNAL_SERVER_ERROR, "error", "internal_error")


def _error_response(status_code: int, status: str, code: str) -> JSONResponse:
    return _response(status_code, status, {}, errors=[code])


def _response(
    status_code: int,
    status: str,
    result: Mapping[str, Any],
    *,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=int(status_code),
        content={
            "object": MATCH_JOURNAL_COCKPIT_OBJECT,
            "schema_version": MATCH_JOURNAL_COCKPIT_SCHEMA_VERSION,
            "status": status,
            "result": _json_safe(dict(result)),
            "warnings": list(warnings or []),
            "errors": list(errors or []),
        },
    )


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, Mapping):
        return {str(key): _json_safe(nested) for key, nested in value.items()}
    if isinstance(value, list | tuple):
        return [_json_safe(nested) for nested in value]
    return None
