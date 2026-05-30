from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from mythic_edge_parser.local_app.backend import create_app
from mythic_edge_parser.local_app.import_jobs import (
    MANUAL_JSONL_IMPORT_SCHEMA_VERSION,
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
    assert bad_line not in encoded
    assert "payload" not in encoded
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
    assert payload["adapter"]["events_skipped"] == 3
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
