from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from mythic_edge_parser.app.analytics_legacy_jsonl_adapter import (
    ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_OBJECT,
    ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION,
)
from mythic_edge_parser.local_app.backend import create_app
from mythic_edge_parser.local_app.import_jobs import (
    MANUAL_JSONL_IMPORT_SCHEMA_VERSION,
    MAX_LEGACY_JSONL_BATCH_FILES,
    clear_import_jobs_for_tests,
)


@pytest.fixture(autouse=True)
def _clear_jobs() -> None:
    clear_import_jobs_for_tests()


def _client(app_data_root: Path) -> TestClient:
    return TestClient(create_app(app_data_root=app_data_root))


def _write_jsonl(path: Path, records: list[dict[str, Any] | str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [record if isinstance(record, str) else json.dumps(record, ensure_ascii=False) for record in records]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _match_started(match_id: str, raw_hash: str = "match-started-hash") -> dict[str, Any]:
    return {
        "kind": "MatchState",
        "timestamp": "2026-05-29T18:00:00+00:00",
        "raw_bytes_hash": raw_hash,
        "payload": {
            "type": "match_started",
            "match_id": match_id,
            "event_id": "Constructed_BestOf1",
            "state_type": "MatchGameRoomStateType_Playing",
            "players": [
                {"player_name": "Local", "team_id": 1, "system_seat_id": 1},
                {"player_name": "Opponent", "team_id": 2, "system_seat_id": 2},
            ],
        },
    }


def _turn_one(match_id: str, raw_hash: str = "turn-one-hash") -> dict[str, Any]:
    return {
        "kind": "GameState",
        "timestamp": "2026-05-29T18:01:00+00:00",
        "raw_bytes_hash": raw_hash,
        "payload": {
            "type": "game_state_message",
            "game_info": {
                "matchID": match_id,
                "gameNumber": 1,
                "superFormat": "SuperFormat_Constructed",
                "matchWinCondition": "MatchWinCondition_SingleGame",
            },
            "raw_game_state": {
                "systemSeatIds": [1],
                "gameStateMessage": {
                    "players": [
                        {"systemSeatNumber": 1, "teamId": 1},
                        {"systemSeatNumber": 2, "teamId": 2},
                    ],
                    "turnInfo": {"turnNumber": 1, "activePlayer": 1},
                },
            },
        },
    }


def _match_finished(match_id: str, raw_hash: str = "match-finished-hash") -> dict[str, Any]:
    return {
        "kind": "GameResult",
        "timestamp": "2026-05-29T18:08:00+00:00",
        "raw_bytes_hash": raw_hash,
        "payload": {
            "type": "game_result",
            "winning_team_id": 1,
            "result_type": "ResultType_WinLoss",
            "reason": "ResultReason_Game",
            "match_state": "MatchState_MatchComplete",
            "results": [
                {
                    "scope": "MatchScope_Game",
                    "winningTeamId": 1,
                    "result": "ResultType_WinLoss",
                    "reason": "ResultReason_Game",
                },
                {
                    "scope": "MatchScope_Match",
                    "winningTeamId": 1,
                    "result": "ResultType_WinLoss",
                    "reason": "ResultReason_Game",
                },
            ],
            "game_info": {
                "matchID": match_id,
                "gameNumber": 1,
                "superFormat": "SuperFormat_Constructed",
                "matchWinCondition": "MatchWinCondition_SingleGame",
            },
        },
    }


def _supported_records(match_id: str = "match:manual:import") -> list[dict[str, Any]]:
    return [_match_started(match_id), _turn_one(match_id), _match_finished(match_id)]


def _repo_sqlite_artifacts() -> set[str]:
    root = Path("data/analytics")
    if not root.exists():
        return set()
    patterns = ("*.db", "*.sqlite", "*.sqlite3", "*.db-journal", "*.db-wal", "*.db-shm")
    found: set[str] = set()
    for pattern in patterns:
        found.update(str(path) for path in root.rglob(pattern))
    return found


def test_valid_synthetic_jsonl_imports_into_app_owned_sqlite_and_job_status(tmp_path: Path) -> None:
    before_repo_artifacts = _repo_sqlite_artifacts()
    app_root = tmp_path / "app-data"
    jsonl_path = tmp_path / "selected" / "events_v1_synthetic.jsonl"
    _write_jsonl(jsonl_path, _supported_records())
    client = _client(app_root)

    response = client.post(
        "/api/imports/jsonl",
        json={
            "source_path": str(jsonl_path),
            "source_artifact_label": "legacy_jsonl_saved_event_replay_v1",
        },
    )
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["object"] == "mythic_edge_local_app_manual_jsonl_import_job"
    assert payload["schema_version"] == MANUAL_JSONL_IMPORT_SCHEMA_VERSION
    assert payload["status"] == "succeeded"
    assert payload["phase"] == "completed"
    assert payload["source"]["source_kind"] == "saved_event_replay"
    assert payload["source"]["source_file_extension"] == ".jsonl"
    assert payload["source"]["path_echoed"] is False
    assert payload["adapter"]["files_processed"] == 1
    assert payload["adapter"]["events_processed"] == 3
    assert payload["adapter"]["quality"]["quality_status"] == "complete"
    assert payload["adapter"]["quality"]["object"] == ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_OBJECT
    assert payload["adapter"]["quality"]["schema_version"] == ANALYTICS_LEGACY_JSONL_IMPORT_QUALITY_SCHEMA_VERSION
    assert payload["adapter"]["quality"]["processed_kind_counts"] == {
        "GameResult": 1,
        "GameState": 1,
        "MatchState": 1,
    }
    assert payload["ingest"]["status"] == "succeeded"
    assert payload["ingest"]["row_counts"]["matches"] == 1
    assert payload["ingest"]["row_counts"]["games"] == 1
    assert payload["database"] == {
        "status": "ok",
        "display_path": "<app_data>\\db\\mythic_edge.sqlite3",
        "created": True,
    }
    assert str(jsonl_path) not in encoded
    assert jsonl_path.as_posix() not in encoded

    job_response = client.get(f"/api/imports/jobs/{payload['job_id']}")
    assert job_response.status_code == 200
    assert job_response.json() == payload

    database_path = app_root / "db" / "mythic_edge.sqlite3"
    assert database_path.exists()
    connection = sqlite3.connect(database_path)
    try:
        assert connection.execute("SELECT COUNT(*) FROM matches").fetchone()[0] == 1
    finally:
        connection.close()
    assert _repo_sqlite_artifacts() == before_repo_artifacts


def test_explicit_batch_jsonl_imports_in_one_job_and_is_idempotent(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    first_path = tmp_path / "selected" / "a_events.jsonl"
    second_path = tmp_path / "selected" / "b_events.jsonl"
    match_id = "match:manual:batch"
    _write_jsonl(first_path, [_match_started(match_id), _turn_one(match_id)])
    _write_jsonl(second_path, [_match_finished(match_id)])
    client = _client(app_root)

    response = client.post(
        "/api/imports/jsonl",
        json={
            "source_paths": [str(second_path), str(first_path)],
            "source_artifact_label": "legacy_jsonl_explicit_batch_v1",
        },
    )
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["status"] == "succeeded"
    assert payload["source"]["source_mode"] == "explicit_file_batch"
    assert payload["source"]["files_selected"] == 2
    assert payload["source"]["files_accepted"] == 2
    assert payload["source"]["files_rejected"] == 0
    assert payload["source"]["source_group_label"] == "legacy_jsonl_explicit_batch_v1"
    assert payload["adapter"]["source_mode"] == "explicit_file_batch"
    assert payload["adapter"]["files_selected"] == 2
    assert payload["adapter"]["files_accepted"] == 2
    assert payload["adapter"]["files_rejected"] == 0
    assert payload["adapter"]["events_processed"] == 3
    assert payload["adapter"]["events_skipped"] == 0
    assert payload["adapter"]["quality"]["quality_status"] == "complete"
    assert [artifact["source_display_label"] for artifact in payload["adapter"]["source_artifacts"]] == [
        "a_events.jsonl",
        "b_events.jsonl",
    ]
    assert payload["source"]["source_artifacts"] == payload["adapter"]["source_artifacts"]
    assert payload["ingest"]["row_counts"]["matches"] == 1
    assert payload["ingest"]["row_counts"]["games"] == 1
    assert str(first_path) not in encoded
    assert str(second_path) not in encoded

    second_response = client.post(
        "/api/imports/jsonl",
        json={
            "source_paths": [str(first_path), str(second_path)],
            "source_artifact_label": "legacy_jsonl_explicit_batch_v1",
        },
    )
    assert second_response.status_code == 200
    assert second_response.json()["status"] == "succeeded"

    database_path = app_root / "db" / "mythic_edge.sqlite3"
    connection = sqlite3.connect(database_path)
    try:
        assert connection.execute("SELECT COUNT(*) FROM matches").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM games").fetchone()[0] == 1
    finally:
        connection.close()


def test_quoted_windows_copy_as_path_style_jsonl_path_is_accepted(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    jsonl_path = tmp_path / "selected path with spaces" / "events_v1_synthetic.jsonl"
    _write_jsonl(jsonl_path, _supported_records("match:manual:quoted-path"))
    client = _client(app_root)

    response = client.post("/api/imports/jsonl", json={"source_path": f'"{jsonl_path}"'})
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["status"] == "succeeded"
    assert payload["source"]["source_display_label"] == "events_v1_synthetic.jsonl"
    assert str(jsonl_path) not in encoded


def test_invalid_batch_source_shapes_reject_before_database_creation(tmp_path: Path) -> None:
    valid_path = tmp_path / "selected" / "events.jsonl"
    _write_jsonl(valid_path, _supported_records("match:manual:batch-validation"))
    text_path = tmp_path / "selected" / "events.txt"
    text_path.write_text("not-jsonl", encoding="utf-8")
    directory_path = tmp_path / "selected" / "folder.jsonl"
    directory_path.mkdir()
    missing_path = tmp_path / "selected" / "missing.jsonl"

    cases: list[tuple[object, str]] = [
        ({"source_path": str(valid_path), "source_paths": [str(valid_path)]}, "source_path_and_source_paths_conflict"),
        ({"source_paths": "not-a-list"}, "source_paths_required"),
        ({"source_paths": []}, "source_paths_empty"),
        (
            {"source_paths": [str(valid_path)] * (MAX_LEGACY_JSONL_BATCH_FILES + 1)},
            "source_paths_too_many",
        ),
        ({"source_paths": [str(valid_path), ""]}, "source_path_invalid"),
        ({"source_paths": [str(valid_path), 7]}, "source_path_invalid"),
        ({"source_paths": [str(valid_path), {"source_path": str(valid_path)}]}, "source_path_invalid"),
        ({"source_paths": [str(valid_path), f'"{valid_path}"']}, "source_path_duplicate"),
        ({"source_paths": ["https://example.invalid/events.jsonl"]}, "source_path_url_not_allowed"),
        ({"source_paths": ["\\\\server\\share\\events.jsonl"]}, "source_path_unc_not_allowed"),
        ({"source_paths": [str(missing_path)]}, "source_path_missing"),
        ({"source_paths": [str(directory_path)]}, "source_path_directory_not_allowed"),
        ({"source_paths": [str(text_path)]}, "source_path_extension_not_allowed"),
    ]

    for index, (body, expected_error) in enumerate(cases):
        app_root = tmp_path / f"app-data-batch-invalid-{index}"
        client = _client(app_root)

        response = client.post("/api/imports/jsonl", json=body)
        payload = response.json()
        encoded = json.dumps(payload, sort_keys=True)

        assert response.status_code == 200
        assert payload["status"] == "rejected"
        assert payload["errors"] == [expected_error]
        assert str(valid_path) not in encoded
        assert str(text_path) not in encoded
        assert str(directory_path) not in encoded
        assert str(missing_path) not in encoded
        assert not app_root.exists()


@pytest.mark.parametrize(
    ("source_path_value", "expected_error"),
    (
        ("", "source_path_required"),
        ("https://example.invalid/events.jsonl", "source_path_url_not_allowed"),
        ("\\\\server\\share\\events.jsonl", "source_path_unc_not_allowed"),
    ),
)
def test_invalid_source_shape_rejects_before_database_creation(
    tmp_path: Path,
    source_path_value: str,
    expected_error: str,
) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)

    response = client.post("/api/imports/jsonl", json={"source_path": source_path_value})
    payload = response.json()

    assert response.status_code == 200
    assert payload["status"] == "rejected"
    assert payload["errors"] == [expected_error]
    assert not app_root.exists()


@pytest.mark.parametrize("body_kind", ("scalar_path", "list_path", "number"))
def test_non_object_import_requests_are_sanitized_before_database_creation(
    tmp_path: Path,
    body_kind: str,
) -> None:
    app_root = tmp_path / "app-data"
    raw_submitted_path = str(tmp_path / "selected" / "private_events.jsonl")
    request_body: object
    if body_kind == "scalar_path":
        request_body = raw_submitted_path
    elif body_kind == "list_path":
        request_body = [raw_submitted_path]
    else:
        request_body = 7
    client = _client(app_root)

    response = client.post("/api/imports/jsonl", json=request_body)
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["status"] == "rejected"
    assert payload["errors"] == ["source_request_invalid"]
    assert raw_submitted_path not in encoded
    assert Path(raw_submitted_path).as_posix() not in encoded
    assert not app_root.exists()


def test_missing_non_jsonl_and_directory_sources_reject_before_database_creation(tmp_path: Path) -> None:
    cases: list[tuple[str, str]] = []
    missing_path = tmp_path / "missing" / "events.jsonl"
    cases.append((str(missing_path), "source_path_missing"))
    text_path = tmp_path / "selected" / "events.txt"
    text_path.parent.mkdir(parents=True)
    text_path.write_text("not-jsonl", encoding="utf-8")
    cases.append((str(text_path), "source_path_extension_not_allowed"))
    directory_path = tmp_path / "selected" / "folder.jsonl"
    directory_path.mkdir()
    cases.append((str(directory_path), "source_path_directory_not_allowed"))

    for index, (source_path, expected_error) in enumerate(cases):
        app_root = tmp_path / f"app-data-{index}"
        client = _client(app_root)

        response = client.post("/api/imports/jsonl", json={"source_path": source_path})
        payload = response.json()

        assert response.status_code == 200
        assert payload["status"] == "rejected"
        assert payload["errors"] == [expected_error]
        assert not app_root.exists()


def test_malformed_jsonl_fails_without_raw_line_path_or_database_creation(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    bad_line = '{"kind": "Rank", "payload": '
    jsonl_path = tmp_path / "selected" / "malformed_events.jsonl"
    _write_jsonl(jsonl_path, [bad_line])
    client = _client(app_root)

    response = client.post("/api/imports/jsonl", json={"source_path": str(jsonl_path)})
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["status"] == "failed"
    assert payload["errors"] == ["invalid_jsonl"]
    assert payload["adapter"]["quality"]["quality_status"] == "failed"
    assert payload["adapter"]["quality"]["adapter_warning_codes"] == ["invalid_jsonl"]
    assert payload["adapter"]["quality"]["routing_hints"] == [
        {
            "category": "source_artifact_problem",
            "code": "invalid_jsonl",
            "count": 1,
            "severity": "action_needed",
        }
    ]
    assert bad_line not in encoded
    assert '"payload":' not in encoded
    assert str(jsonl_path) not in encoded
    assert not app_root.exists()


def test_unsupported_kinds_and_duplicate_hashes_are_safe_degraded_counts(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    jsonl_path = tmp_path / "selected" / "events_with_skips.jsonl"
    match_id = "match:manual:degraded"
    _write_jsonl(
        jsonl_path,
        [
            _match_started(match_id),
            "",
            {
                "kind": "ConnectionError",
                "timestamp": "2026-05-29T18:00:30+00:00",
                "raw_bytes_hash": "unsupported-consumed-hash",
                "payload": {"type": "connection_error", "private": "not emitted"},
            },
            {
                "kind": "Rank",
                "timestamp": "2026-05-29T18:00:45+00:00",
                "raw_bytes_hash": "unsupported-consumed-hash",
                "payload": {"constructed_class": "Mythic", "constructed_percentile": 99},
            },
            _turn_one(match_id),
            _match_finished(match_id, raw_hash="final-hash"),
            _match_finished(match_id, raw_hash="final-hash"),
        ],
    )
    client = _client(app_root)

    response = client.post("/api/imports/jsonl", json={"source_path": str(jsonl_path)})
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["status"] == "degraded"
    assert payload["adapter"]["unsupported_kind_counts"] == {"ConnectionError": 1}
    assert payload["adapter"]["events_skipped"] == 4
    assert payload["adapter"]["quality"]["quality_status"] == "degraded"
    assert payload["adapter"]["quality"]["records_seen"] == 6
    assert payload["adapter"]["quality"]["events_processed"] == 3
    assert payload["adapter"]["quality"]["events_skipped"] == 4
    assert payload["adapter"]["quality"]["processed_kind_counts"] == {
        "GameResult": 1,
        "GameState": 1,
        "MatchState": 1,
    }
    assert payload["adapter"]["quality"]["skipped_reason_counts"] == {
        "blank_line": 1,
        "duplicate_raw_hash": 2,
        "unsupported_kind": 1,
    }
    assert payload["adapter"]["quality"]["duplicate_raw_hash_count"] == 2
    assert payload["adapter"]["quality"]["unsupported_kind_skip_count"] == 1
    assert payload["adapter"]["quality"]["adapter_warning_codes"] == [
        "events_skipped",
        "unsupported_event_kinds",
    ]
    assert payload["adapter"]["quality"]["routing_hints"] == [
        {
            "category": "harmless_expected_skip",
            "code": "blank_lines",
            "count": 1,
            "severity": "info",
        },
        {
            "category": "harmless_or_repeated_export",
            "code": "duplicate_raw_hashes",
            "count": 2,
            "severity": "info",
        },
        {
            "category": "parser_or_adapter_backlog",
            "code": "unsupported_event_kinds",
            "count": 1,
            "severity": "warning",
        },
    ]
    assert payload["adapter"]["quality"]["privacy"] == {
        "has_private_path_echo": False,
        "raw_hash_exposed": False,
        "raw_payload_exposed": False,
    }
    assert payload["warnings"] == ["unsupported_event_kinds", "events_skipped"]
    assert "unsupported-consumed-hash" not in encoded
    assert "final-hash" not in encoded
    assert "not emitted" not in encoded


def test_unknown_jobs_and_destructive_routes_are_absent(tmp_path: Path) -> None:
    client = _client(tmp_path / "app-data")

    assert client.get("/api/imports/jobs/not-a-real-job").status_code == 404
    assert client.delete("/api/imports/jobs/not-a-real-job").status_code == 405
    assert client.delete("/api/imports/jsonl").status_code == 405
    assert all("DELETE" not in route.methods for route in client.app.routes)
