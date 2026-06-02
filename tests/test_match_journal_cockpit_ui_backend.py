from __future__ import annotations

import json
import sqlite3
from typing import Any

from fastapi.testclient import TestClient

from mythic_edge_parser.app.match_journal_service import (
    MatchJournalService,
    MatchJournalServiceConflictError,
    MatchJournalServiceNotFoundError,
    MatchJournalServiceValidationError,
)
from mythic_edge_parser.local_app.backend import create_app


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

    def set_experiment_label(self, context: dict[str, Any], experiment_id: str, **options: Any) -> dict[str, Any]:
        return self._record("set_experiment_label", context, experiment_id, **options)

    def propose_display_correction(self, context: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
        return self._record("propose_display_correction", context, request)


def _client(tmp_path, service: Any | None = None) -> TestClient:
    factory = (lambda: service) if service is not None else None
    return TestClient(create_app(app_data_root=tmp_path / "app-data", match_journal_service_factory=factory))


def _real_journal_service() -> MatchJournalService:
    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.row_factory = sqlite3.Row
    counters: dict[str, int] = {}

    def id_factory(prefix: str) -> str:
        counters[prefix] = counters.get(prefix, 0) + 1
        return f"{prefix}:cockpit-test:{counters[prefix]}"

    return MatchJournalService.from_connection(
        connection,
        id_factory=id_factory,
        clock=lambda: "2026-06-01T00:00:00Z",
        ensure_schema=True,
        applied_at="2026-06-01T00:00:00Z",
    )


def test_journal_route_inventory_has_browser_facade_routes_without_pilot_error_or_delete(tmp_path) -> None:
    client = _client(tmp_path, RecordingJournalService())
    route_paths = {route.path for route in client.app.routes}

    assert {
        "/api/journal",
        "/api/journal/notes",
        "/api/journal/opponent-labels",
        "/api/journal/review-flags",
        "/api/journal/experiment-label",
        "/api/journal/display-corrections",
    } <= route_paths
    assert "/api/journal/pilot-error" not in route_paths
    assert all("DELETE" not in route.methods for route in client.app.routes)


def test_journal_facade_preserves_local_cors_and_rejects_non_loopback_origins(tmp_path) -> None:
    client = _client(tmp_path, RecordingJournalService())

    allowed = client.get("/api/journal?parser_match_id=parser-match-1", headers={"Origin": "http://127.0.0.1:5173"})
    disallowed = client.get("/api/journal?parser_match_id=parser-match-1", headers={"Origin": "http://example.invalid"})

    assert allowed.headers.get("access-control-allow-origin") == "http://127.0.0.1:5173"
    assert disallowed.headers.get("access-control-allow-origin") is None
    assert disallowed.headers.get("access-control-allow-origin") != "*"


def test_journal_facade_fails_closed_when_service_is_not_explicitly_wired(tmp_path) -> None:
    client = _client(tmp_path)

    get_response = client.get("/api/journal?parser_match_id=parser-match-1")
    post_response = client.post(
        "/api/journal/notes",
        json={"note_scope": "unattached", "note_text": "Synthetic local note."},
    )

    assert get_response.status_code == 503
    assert get_response.json()["errors"] == ["service_unavailable"]
    assert post_response.status_code == 503
    assert post_response.json()["errors"] == ["service_unavailable"]


def test_malformed_and_invalid_journal_requests_do_not_call_service(tmp_path) -> None:
    service = RecordingJournalService()
    client = _client(tmp_path, service)

    malformed = client.post(
        "/api/journal/notes",
        content="{not json",
        headers={"Content-Type": "application/json"},
    )
    invalid = client.post(
        "/api/journal/notes",
        json={"note_scope": "match", "note_text": "Synthetic local note."},
    )
    unattached_with_context = client.post(
        "/api/journal/notes",
        json={
            "note_scope": "unattached",
            "note_text": "Synthetic local note.",
            "context": {"parser_match_id": "parser-match-1"},
        },
    )

    assert malformed.status_code == 400
    assert malformed.json()["errors"] == ["malformed_json"]
    assert invalid.status_code == 400
    assert invalid.json()["errors"] == ["validation_error"]
    assert unattached_with_context.status_code == 400
    assert unattached_with_context.json()["errors"] == ["validation_error"]
    assert service.calls == []


def test_journal_get_reads_bundle_without_creating_app_data_artifacts(tmp_path) -> None:
    app_root = tmp_path / "app-data"
    service = RecordingJournalService(
        bundle={"match": {"parser_match_id": "parser-match-1"}, "warnings": ["synthetic"]}
    )
    client = TestClient(create_app(app_data_root=app_root, match_journal_service_factory=lambda: service))

    response = client.get("/api/journal?parser_match_id=parser-match-1&game_number=2")
    payload = response.json()

    assert response.status_code == 200
    assert payload["object"] == "mythic_edge_local_app_match_journal"
    assert payload["schema_version"] == "match_journal_cockpit_ui.v1"
    assert payload["result"]["bundle"]["match"]["parser_match_id"] == "parser-match-1"
    assert payload["warnings"] == ["synthetic"]
    assert service.calls == [("get_journal_bundle", ({"parser_match_id": "parser-match-1", "game_number": 2},), {})]
    assert not app_root.exists()
    assert list(tmp_path.rglob("*")) == []


def test_journal_write_routes_dispatch_to_expected_service_methods(tmp_path) -> None:
    service = RecordingJournalService()
    client = _client(tmp_path, service)
    context = {"parser_match_id": "parser-match-1", "parser_game_id": "parser-game-1", "game_number": 1}

    note = client.post(
        "/api/journal/notes",
        json={"context": context, "note_scope": "game", "note_text": "Synthetic local note."},
    )
    labels = client.post(
        "/api/journal/opponent-labels",
        json={"context": context, "archetype": "Manual Synthetic Archetype", "tier": "Manual Tier 2"},
    )
    flag = client.post(
        "/api/journal/review-flags",
        json={"context": context, "flag_type": "suspected_parser_gap", "priority_label": "high"},
    )
    experiment = client.post(
        "/api/journal/experiment-label",
        json={"context": context, "experiment_label": "ladder-test"},
    )
    correction = client.post(
        "/api/journal/display-corrections",
        json={
            "context": context,
            "target_surface": "journal_display",
            "target_field": "review_summary",
            "proposed_value_label": "Synthetic display label.",
        },
    )

    status_codes = [response.status_code for response in (note, labels, flag, experiment, correction)]
    assert status_codes == [200, 200, 200, 200, 200]
    assert [call[0] for call in service.calls] == [
        "record_game_note",
        "set_opponent_labels",
        "flag_for_review",
        "set_experiment_label",
        "propose_display_correction",
    ]
    assert service.calls[-1][1][1]["effect_scope"] == "journal_display_only"


def test_successful_journal_write_response_summarizes_service_result_without_echoing_record_values(tmp_path) -> None:
    service = _real_journal_service()
    client = _client(tmp_path, service)
    unsafe_note_text = "local-profile\\Player.log https://script.google.com/macros/s/private-deploy/exec"

    response = client.post(
        "/api/journal/notes",
        json={"note_scope": "unattached", "note_text": unsafe_note_text},
    )
    payload = response.json()
    serialized = json.dumps(payload, sort_keys=True)
    service_result = payload["result"]["service_result"]

    assert response.status_code == 200
    assert service_result == {
        "action": "record_unattached_note",
        "status": "completed",
        "primary_record_type": "note",
        "primary_record_id": "journal_note:cockpit-test:1",
        "record_counts": {"note": 1},
    }
    assert "records" not in service_result
    assert "note_text" not in serialized
    assert "Player.log" not in serialized
    assert "script.google.com" not in serialized
    assert unsafe_note_text not in serialized


def test_journal_display_correction_rejects_non_display_only_scope(tmp_path) -> None:
    service = RecordingJournalService()
    client = _client(tmp_path, service)

    response = client.post(
        "/api/journal/display-corrections",
        json={
            "context": {"parser_match_id": "parser-match-1"},
            "target_surface": "journal_display",
            "target_field": "review_summary",
            "proposed_value_label": "Synthetic display label.",
            "effect_scope": "parser_truth",
        },
    )

    assert response.status_code == 400
    assert response.json()["errors"] == ["validation_error"]
    assert service.calls == []


def test_journal_service_errors_map_to_safe_envelopes_without_raw_details(tmp_path) -> None:
    for error, expected_status, expected_code in (
        (MatchJournalServiceValidationError("synthetic exception detail"), 400, "validation_error"),
        (MatchJournalServiceNotFoundError("synthetic exception detail"), 404, "not_found"),
        (MatchJournalServiceConflictError("synthetic exception detail"), 409, "conflict"),
        (RuntimeError("synthetic exception detail"), 500, "internal_error"),
    ):
        service = RecordingJournalService(error=error)
        client = _client(tmp_path, service)

        response = client.post(
            "/api/journal/notes",
            json={"note_scope": "unattached", "note_text": "Synthetic local note."},
        )
        serialized = json.dumps(response.json())

        assert response.status_code == expected_status
        assert response.json()["errors"] == [expected_code]
        assert "Synthetic local note" not in serialized
        assert "synthetic exception detail" not in serialized
