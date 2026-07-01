from __future__ import annotations

import asyncio
import json
import sqlite3
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from mythic_edge_parser.local_app import import_jobs
from mythic_edge_parser.local_app.backend import (
    _BrowserJsonlUploadReadError,
    _build_browser_jsonl_upload_files,
    create_app,
)
from mythic_edge_parser.local_app.import_jobs import (
    BROWSER_JSONL_UPLOAD_SOURCE_MODE,
    MANUAL_JSONL_IMPORT_SCHEMA_VERSION,
    clear_import_jobs_for_tests,
)
from tests.local_app_request_guard_helpers import guarded_client


@pytest.fixture(autouse=True)
def _clear_jobs() -> None:
    clear_import_jobs_for_tests()


def _client(app_data_root: Path) -> TestClient:
    return guarded_client(create_app(app_data_root=app_data_root))


def _jsonl_bytes(records: list[dict[str, Any] | str]) -> bytes:
    lines = [record if isinstance(record, str) else json.dumps(record, ensure_ascii=False) for record in records]
    return ("\n".join(lines) + "\n").encode("utf-8")


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


def _upload_files(
    first_bytes: bytes,
    second_bytes: bytes,
    *,
    first_name: str = "b_events.jsonl",
    second_name: str = "a_events.jsonl",
) -> list[tuple[str, tuple[str, bytes, str]]]:
    return [
        ("files", (first_name, first_bytes, "application/jsonl")),
        ("files", (second_name, second_bytes, "application/jsonl")),
    ]


def _raw_jsonl_artifacts(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.jsonl"))


class _RecordingUpload:
    def __init__(self, content: bytes, *, filename: str = "events.jsonl") -> None:
        self._content = content
        self._offset = 0
        self.filename = filename
        self.content_type = "application/jsonl"
        self.read_sizes: list[int] = []
        self.bytes_served = 0

    async def read(self, size: int = -1) -> bytes:
        self.read_sizes.append(size)
        if size < 0:
            size = len(self._content) - self._offset
        chunk = self._content[self._offset : self._offset + size]
        self._offset += len(chunk)
        self.bytes_served += len(chunk)
        return chunk


def test_upload_builder_rejects_too_many_files_before_content_reads(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(import_jobs, "MAX_BROWSER_JSONL_UPLOAD_FILES", 1)
    first = _RecordingUpload(b'{"kind": "Rank"}\n')
    second = _RecordingUpload(b'{"kind": "Rank"}\n')

    with pytest.raises(_BrowserJsonlUploadReadError) as exc_info:
        asyncio.run(_build_browser_jsonl_upload_files([first, second]))

    assert exc_info.value.error_code == "upload_files_too_many"
    assert first.read_sizes == []
    assert second.read_sizes == []


def test_upload_builder_stops_single_oversized_file_before_full_read(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(import_jobs, "MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES", 8)
    monkeypatch.setattr(import_jobs, "MAX_BROWSER_JSONL_UPLOAD_TOTAL_BYTES", 1024)
    upload = _RecordingUpload(b"x" * 100)

    with pytest.raises(_BrowserJsonlUploadReadError) as exc_info:
        asyncio.run(_build_browser_jsonl_upload_files([upload]))

    assert exc_info.value.error_code == "upload_file_too_large"
    assert upload.bytes_served == 9
    assert upload.bytes_served < len(upload._content)
    assert upload.read_sizes == [9]


def test_upload_builder_stops_aggregate_oversized_batch_before_remaining_reads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(import_jobs, "MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES", 1024)
    monkeypatch.setattr(import_jobs, "MAX_BROWSER_JSONL_UPLOAD_TOTAL_BYTES", 20)
    first = _RecordingUpload(b"a" * 15, filename="a_events.jsonl")
    second = _RecordingUpload(b"b" * 15, filename="b_events.jsonl")
    third = _RecordingUpload(b"c" * 15, filename="c_events.jsonl")

    with pytest.raises(_BrowserJsonlUploadReadError) as exc_info:
        asyncio.run(_build_browser_jsonl_upload_files([first, second, third]))

    assert exc_info.value.error_code == "upload_total_size_too_large"
    assert first.bytes_served == 15
    assert second.bytes_served == 6
    assert second.bytes_served < len(second._content)
    assert third.read_sizes == []


def test_browser_jsonl_upload_imports_multiple_files_as_one_sanitized_job(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)
    match_id = "match:upload:batch"
    first_bytes = _jsonl_bytes([_match_finished(match_id)])
    second_bytes = _jsonl_bytes([_match_started(match_id), _turn_one(match_id)])

    response = client.post(
        "/api/imports/jsonl/upload",
        files=_upload_files(first_bytes, second_bytes),
        data={"source_artifact_label": "legacy_jsonl_uploaded_batch_v1"},
    )
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["object"] == "mythic_edge_local_app_manual_jsonl_import_job"
    assert payload["schema_version"] == MANUAL_JSONL_IMPORT_SCHEMA_VERSION
    assert payload["status"] == "succeeded"
    assert payload["source"]["source_mode"] == BROWSER_JSONL_UPLOAD_SOURCE_MODE
    assert payload["source"]["source_display_label"] == "2 uploaded JSONL files"
    assert payload["source"]["path_echoed"] is False
    assert payload["source"]["files_selected"] == 2
    assert payload["source"]["files_accepted"] == 2
    assert payload["source"]["files_rejected"] == 0
    assert payload["adapter"]["source_mode"] == BROWSER_JSONL_UPLOAD_SOURCE_MODE
    assert payload["adapter"]["events_processed"] == 3
    assert payload["adapter"]["quality"]["quality_status"] == "complete"
    assert [artifact["source_display_label"] for artifact in payload["adapter"]["source_artifacts"]] == [
        "a_events.jsonl",
        "b_events.jsonl",
    ]
    assert payload["source"]["source_artifacts"] == payload["adapter"]["source_artifacts"]
    assert payload["ingest"]["row_counts"]["matches"] == 1
    assert payload["ingest"]["row_counts"]["games"] == 1
    assert "fakepath" not in encoded.lower()
    assert "raw_bytes_hash" not in encoded
    assert _raw_jsonl_artifacts(app_root) == []

    second_response = client.post(
        "/api/imports/jsonl/upload",
        files=_upload_files(first_bytes, second_bytes),
        data={"source_artifact_label": "legacy_jsonl_uploaded_batch_v1"},
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


def test_browser_jsonl_upload_counts_cross_file_duplicates_without_exposing_hashes_or_payloads(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)
    match_id = "match:upload:degraded"
    first_bytes = _jsonl_bytes(
        [
            _match_started(match_id),
            _turn_one(match_id),
            _match_finished(match_id, raw_hash="upload-final-hash"),
            {
                "kind": "ConnectionError",
                "timestamp": "2026-05-29T18:00:30+00:00",
                "raw_bytes_hash": "upload-shared-unsupported-hash",
                "payload": {"type": "connection_error", "private": "not emitted"},
            },
        ]
    )
    second_bytes = _jsonl_bytes(
        [
            "",
            {
                "kind": "Rank",
                "timestamp": "2026-05-29T18:00:45+00:00",
                "raw_bytes_hash": "upload-shared-unsupported-hash",
                "payload": {"constructed_class": "Mythic", "constructed_percentile": 99},
            },
            _match_finished(match_id, raw_hash="upload-final-hash"),
        ]
    )

    response = client.post("/api/imports/jsonl/upload", files=_upload_files(second_bytes, first_bytes))
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["status"] == "degraded"
    assert payload["adapter"]["quality"]["skipped_reason_counts"] == {
        "blank_line": 1,
        "duplicate_raw_hash": 2,
        "unsupported_kind": 1,
    }
    assert payload["adapter"]["quality"]["duplicate_raw_hash_count"] == 2
    assert payload["adapter"]["quality"]["unsupported_kind_skip_count"] == 1
    assert payload["adapter"]["source_artifacts"][0]["source_display_label"] == "a_events.jsonl"
    assert payload["adapter"]["source_artifacts"][1]["events_skipped"] == 3
    assert "upload-final-hash" not in encoded
    assert "upload-shared-unsupported-hash" not in encoded
    assert "not emitted" not in encoded
    assert _raw_jsonl_artifacts(app_root) == []


@pytest.mark.parametrize(
    ("files", "data", "expected_error"),
    (
        ([], {}, "upload_files_required"),
        ([("files", (" ", b"{}", "application/jsonl"))], {}, "upload_filename_required"),
        ([("files", ("empty.jsonl", b"", "application/jsonl"))], {}, "upload_file_empty"),
        ([("files", ("events.txt", b"{}", "text/plain"))], {}, "upload_file_extension_not_allowed"),
        (
            [("files", ("events.jsonl", b"{}", "application/jsonl"))],
            {"source_artifact_label": "C:\\secret\\Player.log"},
            "source_artifact_label_invalid",
        ),
    ),
)
def test_invalid_browser_upload_requests_reject_before_database_creation(
    tmp_path: Path,
    files: list[tuple[str, tuple[str, bytes, str]]],
    data: dict[str, str],
    expected_error: str,
) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)

    response = client.post("/api/imports/jsonl/upload", files=files, data=data)
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["status"] == "rejected"
    assert payload["errors"] == [expected_error]
    assert "C:\\secret" not in encoded
    assert not app_root.exists()


def test_non_file_multipart_files_field_rejects_without_echoing_submitted_input(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)
    submitted_value = "C:\\private\\secret_token_dump.jsonl"

    response = client.post(
        "/api/imports/jsonl/upload",
        files=[("files", (None, submitted_value))],
    )
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["status"] == "rejected"
    assert payload["source"]["source_mode"] == BROWSER_JSONL_UPLOAD_SOURCE_MODE
    assert payload["source"]["files_selected"] == 1
    assert payload["errors"] == ["upload_file_invalid"]
    assert submitted_value not in encoded
    assert "secret_token_dump" not in encoded
    assert "Expected UploadFile" not in encoded
    assert not app_root.exists()


def test_browser_upload_file_count_and_size_limits_reject_before_database_creation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)
    valid_bytes = b'{"kind": "Rank"}\n'

    monkeypatch.setattr(import_jobs, "MAX_BROWSER_JSONL_UPLOAD_FILES", 1)
    response = client.post(
        "/api/imports/jsonl/upload",
        files=[
            ("files", ("a_events.jsonl", valid_bytes, "application/jsonl")),
            ("files", ("b_events.jsonl", valid_bytes, "application/jsonl")),
        ],
    )
    assert response.json()["errors"] == ["upload_files_too_many"]
    assert not app_root.exists()

    monkeypatch.setattr(import_jobs, "MAX_BROWSER_JSONL_UPLOAD_FILES", 100)
    monkeypatch.setattr(import_jobs, "MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES", 8)
    response = client.post(
        "/api/imports/jsonl/upload",
        files=[("files", ("events.jsonl", valid_bytes, "application/jsonl"))],
    )
    assert response.json()["errors"] == ["upload_file_too_large"]
    assert not app_root.exists()

    monkeypatch.setattr(import_jobs, "MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES", 1024)
    monkeypatch.setattr(import_jobs, "MAX_BROWSER_JSONL_UPLOAD_TOTAL_BYTES", 20)
    response = client.post(
        "/api/imports/jsonl/upload",
        files=[
            ("files", ("a_events.jsonl", valid_bytes, "application/jsonl")),
            ("files", ("b_events.jsonl", valid_bytes, "application/jsonl")),
        ],
    )
    assert response.json()["errors"] == ["upload_total_size_too_large"]
    assert not app_root.exists()


def test_malformed_browser_upload_fails_without_raw_line_hash_path_or_temp_artifact(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)
    raw_hash = "uploaded-private-raw-hash"
    bad_line = f'{{"kind": "GameState", "raw_bytes_hash": "{raw_hash}", "payload": '

    response = client.post(
        "/api/imports/jsonl/upload",
        files=[("files", ("C:\\fakepath\\malformed_events.jsonl", (bad_line + "\n").encode(), "application/jsonl"))],
    )
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["status"] == "failed"
    assert payload["errors"] == ["invalid_jsonl"]
    assert payload["adapter"]["quality"]["quality_status"] == "failed"
    assert bad_line not in encoded
    assert raw_hash not in encoded
    assert '"payload": ' not in encoded
    assert "fakepath" not in encoded.lower()
    assert "<tmp" not in encoded.lower()
    assert not app_root.exists()


def test_browser_upload_does_not_add_destructive_routes(tmp_path: Path) -> None:
    client = _client(tmp_path / "app-data")

    assert client.delete("/api/imports/jsonl/upload").status_code == 405
    assert client.delete("/api/imports/jobs/not-a-real-job").status_code == 405
    assert all("DELETE" not in route.methods for route in client.app.routes)
