from __future__ import annotations

import http.client
import json
import sqlite3
from typing import Any

import pytest

from mythic_edge_parser.app import status_api
from mythic_edge_parser.app.match_journal_service import (
    MatchJournalService,
    MatchJournalServiceConflictError,
    MatchJournalServiceNotFoundError,
    MatchJournalServiceValidationError,
)


class RecordingJournalService:
    def __init__(self, *, error: Exception | None = None, bundle: dict[str, Any] | None = None) -> None:
        self.calls: list[tuple[str, tuple[Any, ...], dict[str, Any]]] = []
        self.error = error
        self.bundle = bundle or {"match": {"parser_match_id": "parser-match-1"}, "warnings": []}

    def _record(self, name: str, *args: Any, **kwargs: Any) -> dict[str, Any]:
        self.calls.append((name, args, kwargs))
        if self.error is not None:
            raise self.error
        return {
            "action": name,
            "status": "completed",
            "primary_record_type": "synthetic",
            "primary_record_id": f"{name}:1",
            "records": {"synthetic": {"method": name}},
            "warnings": [],
        }

    def get_journal_bundle(self, context: dict[str, Any]) -> dict[str, Any] | None:
        self.calls.append(("get_journal_bundle", (context,), {}))
        if self.error is not None:
            raise self.error
        return self.bundle

    def record_match_note(self, context: dict[str, Any], note_text: str, **options: Any) -> dict[str, Any]:
        return self._record("record_match_note", context, note_text, **options)

    def record_game_note(self, context: dict[str, Any], note_text: str, **options: Any) -> dict[str, Any]:
        return self._record("record_game_note", context, note_text, **options)

    def record_sideboarding_note(self, context: dict[str, Any], note_text: str, **options: Any) -> dict[str, Any]:
        return self._record("record_sideboarding_note", context, note_text, **options)

    def record_unattached_note(self, note_text: str, **options: Any) -> dict[str, Any]:
        return self._record("record_unattached_note", note_text, **options)

    def set_pilot_error_status(self, context: dict[str, Any], status: str, **options: Any) -> dict[str, Any]:
        return self._record("set_pilot_error_status", context, status, **options)

    def record_pilot_error_review(
        self,
        context: dict[str, Any],
        *,
        status: str,
        reason: str | None = None,
        note_text: str | None = None,
        **options: Any,
    ) -> dict[str, Any]:
        return self._record(
            "record_pilot_error_review",
            context,
            status=status,
            reason=reason,
            note_text=note_text,
            **options,
        )

    def set_opponent_labels(
        self,
        context: dict[str, Any],
        *,
        archetype: str | None = None,
        tier: str | None = None,
        **options: Any,
    ) -> dict[str, Any]:
        return self._record("set_opponent_labels", context, archetype=archetype, tier=tier, **options)

    def flag_for_review(self, context: dict[str, Any], flag_type: str, **options: Any) -> dict[str, Any]:
        return self._record("flag_for_review", context, flag_type, **options)

    def propose_display_correction(self, context: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
        return self._record("propose_display_correction", context, request)


@pytest.fixture(autouse=True)
def reset_match_journal_service(monkeypatch: pytest.MonkeyPatch) -> None:
    status_api.configure_match_journal_service_factory(None)
    monkeypatch.setattr(status_api, "STATUS_API_HOST", "127.0.0.1")
    yield
    status_api.configure_match_journal_service_factory(None)


def _set_service(service: RecordingJournalService | MatchJournalService) -> None:
    status_api.configure_match_journal_service_factory(lambda: service)


def _post(route: str, body: dict[str, Any] | str) -> tuple[int, dict[str, Any]]:
    encoded = json.dumps(body) if isinstance(body, dict) else body
    return status_api._journal_api_payload_for_request("POST", route, {}, encoded)


def test_root_route_inventory_includes_journal_routes_without_removing_existing_routes() -> None:
    status_code, payload = status_api._api_payload_for_request("/", {})

    assert status_code == 200
    routes = set(payload["routes"])
    assert {
        "/health",
        "/status",
        "/active-match",
        "/timeline",
        "/actions",
        "/active-deck",
        "/match-history",
        "/collection",
        "/card-performance",
    } <= routes
    assert {
        "/journal",
        "/journal/notes",
        "/journal/pilot-error",
        "/journal/opponent-labels",
        "/journal/review-flags",
        "/journal/display-corrections",
    } <= routes


def test_journal_routes_reject_unsupported_methods() -> None:
    get_status, get_payload = status_api._journal_api_payload_for_request("GET", "/journal/notes", {})
    post_status, post_payload = status_api._journal_api_payload_for_request("POST", "/journal", {}, "{}")

    assert get_status == 405
    assert get_payload["error"]["code"] == "method_not_allowed"
    assert post_status == 405
    assert post_payload["error"]["code"] == "method_not_allowed"


def test_http_handler_returns_json_405_for_unsupported_journal_method(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(status_api, "ENABLE_STATUS_API", True)
    monkeypatch.setattr(status_api, "STATUS_API_HOST", "127.0.0.1")
    monkeypatch.setattr(status_api, "STATUS_API_PORT", 0)
    status_api.reset_status_api_runtime_state()
    try:
        server_info = status_api.start_status_api_server()
        assert server_info is not None
        connection = http.client.HTTPConnection(server_info["host"], server_info["port"], timeout=5)
        try:
            connection.request("PUT", "/journal/notes")
            response = connection.getresponse()
            response_body = response.read().decode("utf-8")
        finally:
            connection.close()
    finally:
        status_api.stop_status_api_server()

    assert response.status == 405
    assert response.getheader("Content-Type") == "application/json; charset=utf-8"
    payload = json.loads(response_body)
    assert payload["object"] == "match_journal_api_response"
    assert payload["error"]["code"] == "method_not_allowed"


def test_malformed_json_returns_400_without_calling_service() -> None:
    service = RecordingJournalService()
    _set_service(service)

    status_code, payload = _post("/journal/notes", "{not json")

    assert status_code == 400
    assert payload["error"]["code"] == "malformed_json"
    assert service.calls == []


def test_missing_service_wiring_returns_503_after_request_validation() -> None:
    status_code, payload = _post(
        "/journal/notes",
        {
            "note_scope": "unattached",
            "note_text": "Synthetic local note.",
        },
    )

    assert status_code == 503
    assert payload["error"]["code"] == "service_unavailable"


def test_journal_write_routes_fail_closed_when_status_api_host_is_not_loopback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = RecordingJournalService()
    _set_service(service)
    monkeypatch.setattr(status_api, "STATUS_API_HOST", "0.0.0.0")

    status_code, payload = _post(
        "/journal/notes",
        {
            "note_scope": "unattached",
            "note_text": "Synthetic local note.",
        },
    )

    assert status_code == 503
    assert payload["error"]["code"] == "service_unavailable"
    assert service.calls == []


def test_get_journal_maps_query_context_to_service_bundle() -> None:
    service = RecordingJournalService(
        bundle={"match": {"parser_match_id": "parser-match-1"}, "warnings": ["synthetic"]}
    )
    _set_service(service)

    status_code, payload = status_api._journal_api_payload_for_request(
        "GET",
        "/journal",
        {"parser_match_id": "parser-match-1", "game_number": "2"},
    )

    assert status_code == 200
    assert payload["result"]["bundle"]["match"]["parser_match_id"] == "parser-match-1"
    assert payload["warnings"] == ["synthetic"]
    assert service.calls == [("get_journal_bundle", ({"parser_match_id": "parser-match-1", "game_number": 2},), {})]


@pytest.mark.parametrize(
    ("note_scope", "expected_method"),
    (
        ("match", "record_match_note"),
        ("game", "record_game_note"),
        ("sideboarding", "record_sideboarding_note"),
        ("unattached", "record_unattached_note"),
    ),
)
def test_note_scopes_dispatch_to_expected_service_methods(note_scope: str, expected_method: str) -> None:
    service = RecordingJournalService()
    _set_service(service)
    body: dict[str, Any] = {
        "note_scope": note_scope,
        "note_text": "Synthetic local note.",
        "source_surface": "status_api",
    }
    if note_scope != "unattached":
        body["context"] = {"parser_match_id": "parser-match-1", "game_number": 1}

    status_code, payload = _post("/journal/notes", body)

    assert status_code == 200
    assert payload["result"]["service_result"]["action"] == expected_method
    assert service.calls[0][0] == expected_method


def test_attached_note_scopes_require_context_and_do_not_become_unattached() -> None:
    service = RecordingJournalService()
    _set_service(service)

    status_code, payload = _post(
        "/journal/notes",
        {
            "note_scope": "match",
            "note_text": "Synthetic local note.",
        },
    )

    assert status_code == 400
    assert payload["error"]["code"] == "validation_error"
    assert service.calls == []


def test_pilot_error_route_preserves_status_and_reason_paths() -> None:
    service = RecordingJournalService()
    _set_service(service)

    status_only_code, _status_only_payload = _post(
        "/journal/pilot-error",
        {"context": {"parser_match_id": "parser-match-1"}, "status": "yes"},
    )
    review_code, _review_payload = _post(
        "/journal/pilot-error",
        {
            "context": {"parser_match_id": "parser-match-1"},
            "status": "unknown",
            "reason": "Synthetic review reason.",
            "note_text": "Synthetic review note.",
        },
    )

    assert status_only_code == 200
    assert review_code == 200
    assert service.calls[0][0] == "set_pilot_error_status"
    assert service.calls[1][0] == "record_pilot_error_review"
    assert service.calls[1][2]["reason"] == "Synthetic review reason."
    assert service.calls[1][2]["note_text"] == "Synthetic review note."


def test_label_flag_and_display_correction_routes_are_manual_journal_service_calls() -> None:
    service = RecordingJournalService()
    _set_service(service)

    labels_code, _labels_payload = _post(
        "/journal/opponent-labels",
        {
            "context": {"parser_match_id": "parser-match-1"},
            "archetype": "Manual Synthetic Archetype",
            "tier": "Manual Tier 2",
        },
    )
    flag_code, _flag_payload = _post(
        "/journal/review-flags",
        {
            "context": {"parser_match_id": "parser-match-1"},
            "flag_type": "suspected_parser_gap",
            "priority_label": "high",
        },
    )
    correction_code, _correction_payload = _post(
        "/journal/display-corrections",
        {
            "context": {"parser_match_id": "parser-match-1"},
            "target_surface": "journal_display",
            "target_field": "review_summary",
            "proposed_value_label": "Synthetic display label.",
        },
    )

    assert labels_code == 200
    assert flag_code == 200
    assert correction_code == 200
    assert [call[0] for call in service.calls] == [
        "set_opponent_labels",
        "flag_for_review",
        "propose_display_correction",
    ]
    assert service.calls[2][1][1]["effect_scope"] == "journal_display_only"


@pytest.mark.parametrize(
    ("error", "expected_status", "expected_code"),
    (
        (MatchJournalServiceValidationError("synthetic exception detail"), 400, "validation_error"),
        (MatchJournalServiceNotFoundError("synthetic exception detail"), 404, "not_found"),
        (MatchJournalServiceConflictError("synthetic exception detail"), 409, "conflict"),
        (RuntimeError("synthetic exception detail"), 500, "internal_error"),
    ),
)
def test_service_errors_map_to_safe_envelopes(
    error: Exception,
    expected_status: int,
    expected_code: str,
) -> None:
    _set_service(RecordingJournalService(error=error))

    status_code, payload = _post(
        "/journal/notes",
        {
            "note_scope": "unattached",
            "note_text": "Synthetic local note.",
        },
    )
    serialized = json.dumps(payload)

    assert status_code == expected_status
    assert payload["object"] == "match_journal_api_response"
    assert payload["ok"] is False
    assert payload["error"]["code"] == expected_code
    assert "Synthetic local note" not in serialized
    assert "synthetic exception detail" not in serialized


def test_in_memory_match_journal_service_results_are_json_safe() -> None:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    service = MatchJournalService.from_connection(
        connection,
        id_factory=lambda prefix: f"{prefix}:status-api-test",
        clock=lambda: "2026-06-01T00:00:00+00:00",
        ensure_schema=True,
        applied_at="2026-06-01T00:00:00+00:00",
    )
    _set_service(service)

    status_code, payload = _post(
        "/journal/notes",
        {
            "note_scope": "match",
            "note_text": "Synthetic local note.",
            "context": {"parser_match_id": "parser-match-1"},
        },
    )

    assert status_code == 200
    json.dumps(payload)
    note = payload["result"]["service_result"]["records"]["note"]
    assert note["note_scope"] == "match"
    assert note["parser_match_id"] == "parser-match-1"


def test_get_journal_with_parser_game_id_uses_real_service_bundle() -> None:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    service = MatchJournalService.from_connection(
        connection,
        id_factory=lambda prefix: f"{prefix}:status-api-test",
        clock=lambda: "2026-06-01T00:00:00+00:00",
        ensure_schema=True,
        applied_at="2026-06-01T00:00:00+00:00",
    )
    service.record_game_note(
        {"parser_match_id": "parser-match-1", "parser_game_id": "parser-game-1", "game_number": 1},
        "Synthetic game note.",
    )
    _set_service(service)

    status_code, payload = status_api._journal_api_payload_for_request(
        "GET",
        "/journal",
        {"parser_game_id": "parser-game-1"},
    )

    assert status_code == 200
    bundle = payload["result"]["bundle"]
    assert bundle["match"]["parser_match_id"] == "parser-match-1"
    assert bundle["games"][0]["parser_game_id"] == "parser-game-1"
    assert bundle["notes"][0]["parser_game_id"] == "parser-game-1"
