from __future__ import annotations

import json
import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from fastapi.testclient import TestClient

from mythic_edge_parser.app.analytics_migration_loader import (
    ANALYTICS_SCHEMA_VERSION,
    apply_analytics_migrations,
)
from mythic_edge_parser.local_app.backend import create_app


def _client(app_data_root: Path | None, *, env: dict[str, str] | None = None) -> TestClient:
    return TestClient(create_app(app_data_root=app_data_root, env=dict(os.environ) if env is None else env))


def test_refresh_state_reports_missing_database_without_creating_artifacts(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"

    response = _client(app_root).get("/api/analytics/refresh-state")
    payload = response.json()
    encoded = json.dumps(payload, sort_keys=True)

    assert response.status_code == 200
    assert payload["object"] == "mythic_edge_local_app_analytics_refresh_state"
    assert payload["schema_version"] == "analytics_auto_refresh_after_match_completion.v1"
    assert payload["status"] == "missing"
    assert payload["analytics_revision"] is None
    assert payload["latest_completed_match_result_available"] is False
    assert payload["latest_completed_match_seen_at"] is None
    assert payload["latest_completed_ingest_finished_at"] is None
    assert payload["row_counts"] == {
        "ingest_runs": 0,
        "matches": 0,
        "games": 0,
        "match_results": 0,
        "game_results": 0,
    }
    assert str(app_root) not in encoded
    assert "SELECT" not in encoded.upper()
    assert not app_root.exists()


def test_refresh_state_reports_empty_current_database_with_stable_revision(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()

    first_payload = _client(app_root).get("/api/analytics/refresh-state").json()
    second_payload = _client(app_root).get("/api/analytics/refresh-state").json()

    assert first_payload["status"] == "empty"
    assert first_payload["analytics_revision"].startswith("analytics-refresh-v1:")
    assert first_payload["analytics_revision"] == second_payload["analytics_revision"]
    assert first_payload["latest_completed_match_result_available"] is False
    assert first_payload["latest_completed_ingest_finished_at"] == "2026-06-08T00:00:01Z"
    assert first_payload["row_counts"] == {
        "ingest_runs": 1,
        "matches": 0,
        "games": 0,
        "match_results": 0,
        "game_results": 0,
    }
    assert _sqlite_sidecars(app_root) == []


def test_refresh_state_changes_revision_after_completed_match_result_metadata_changes(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()

    before_payload = _client(app_root).get("/api/analytics/refresh-state").json()
    with _current_database(app_root) as connection:
        _insert_match_result(connection, "match:refresh:1", updated_at="2026-06-08T00:10:00Z")
        _insert_game_result(connection, "match:refresh:1", 1, updated_at="2026-06-08T00:10:01Z")
        connection.commit()

    after_payload = _client(app_root).get("/api/analytics/refresh-state").json()
    encoded = json.dumps(after_payload, sort_keys=True)

    assert after_payload["status"] == "ok"
    assert after_payload["analytics_revision"] != before_payload["analytics_revision"]
    assert after_payload["latest_completed_match_result_available"] is True
    assert after_payload["latest_completed_match_seen_at"] == "2026-06-08T00:10:00Z"
    assert after_payload["row_counts"] == {
        "ingest_runs": 1,
        "matches": 1,
        "games": 1,
        "match_results": 1,
        "game_results": 1,
    }
    assert "match:refresh:1" not in encoded
    assert "win" not in encoded.lower()
    assert "SELECT" not in encoded.upper()
    assert str(app_root) not in encoded
    assert _sqlite_sidecars(app_root) == []


def test_refresh_state_drops_unsafe_persisted_timestamp_metadata(tmp_path: Path) -> None:
    first_payload = _refresh_state_with_unsafe_timestamps(
        tmp_path / "first",
        match_seen_at=r"C:\operator\AppData\Local\MythicEdge\Player.log",
        ingest_finished_at="https://example.invalid/private/mythic_edge.sqlite3",
    )
    second_payload = _refresh_state_with_unsafe_timestamps(
        tmp_path / "second",
        match_seen_at=r"D:\other\private\Player.log",
        ingest_finished_at="file:///private/generated/mythic_edge.sqlite3",
    )
    encoded = json.dumps({"first": first_payload, "second": second_payload}, sort_keys=True)

    assert first_payload["status"] == "ok"
    assert first_payload["latest_completed_match_result_available"] is True
    assert first_payload["latest_completed_match_seen_at"] is None
    assert first_payload["latest_completed_ingest_finished_at"] is None
    assert first_payload["analytics_revision"] == second_payload["analytics_revision"]
    assert "AppData" not in encoded
    assert "Player.log" not in encoded
    assert "example.invalid" not in encoded
    assert "file:///" not in encoded


def test_refresh_state_rejects_unapproved_query_parameters_without_echo(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()

    response = _client(app_root).get("/api/analytics/refresh-state?match_id=private")
    encoded = json.dumps(response.json(), sort_keys=True)

    assert response.status_code == 422
    assert "analytics_refresh_state_query_parameter_not_allowed" in encoded
    assert "private" not in encoded


def test_refresh_state_returns_safe_error_for_invalid_database(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    database_path = app_root / "db" / "mythic_edge.sqlite3"
    database_path.parent.mkdir(parents=True)
    database_path.write_text("not sqlite", encoding="utf-8")

    payload = _client(app_root).get("/api/analytics/refresh-state").json()
    encoded = json.dumps(payload, sort_keys=True)

    assert payload["status"] == "error"
    assert payload["errors"] == ["database_invalid_sqlite"]
    assert payload["analytics_revision"] is None
    assert str(app_root) not in encoded
    assert "not sqlite" not in encoded
    assert "SELECT" not in encoded.upper()


def _refresh_state_with_unsafe_timestamps(
    app_root: Path,
    *,
    match_seen_at: str,
    ingest_finished_at: str,
) -> dict[str, object]:
    with _current_database(app_root) as connection:
        connection.execute(
            """
            UPDATE ingest_runs
            SET finished_at = ?, updated_at = ?
            WHERE ingest_run_id = ?
            """,
            (ingest_finished_at, ingest_finished_at, "ingest:auto-refresh:test"),
        )
        _insert_match_result(connection, "match:refresh:unsafe", updated_at=match_seen_at)
        connection.commit()
    return _client(app_root).get("/api/analytics/refresh-state").json()


@contextmanager
def _current_database(app_root: Path) -> Iterator[sqlite3.Connection]:
    database_path = app_root / "db" / "mythic_edge.sqlite3"
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    try:
        apply_analytics_migrations(connection, applied_at="test-applied")
        _insert_seed_run(connection)
        yield connection
    finally:
        connection.close()


def _insert_seed_run(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        INSERT OR IGNORE INTO ingest_runs (
            ingest_run_id,
            source_kind,
            source_artifact_label,
            started_at,
            finished_at,
            status,
            parser_commit,
            parser_version,
            schema_version,
            row_counts_json,
            created_at,
            updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "ingest:auto-refresh:test",
            "sanitized_golden_replay",
            "analytics_auto_refresh_v1",
            "2026-06-08T00:00:00Z",
            "2026-06-08T00:00:01Z",
            "completed",
            "test",
            "test",
            ANALYTICS_SCHEMA_VERSION,
            "{}",
            "2026-06-08T00:00:00Z",
            "2026-06-08T00:00:01Z",
        ),
    )


def _core(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "value_source": "observed",
        "confidence": "high",
        "finality": "final",
        "drift_status": "none",
        "parser_schema_version": ANALYTICS_SCHEMA_VERSION,
        "ingest_run_id": "ingest:auto-refresh:test",
        "source_parser_surface": "synthetic_auto_refresh_test",
        "source_fact_key": "synthetic_fact",
        "availability_status": "available",
        "created_at": "2026-06-08T00:00:00Z",
        "updated_at": "2026-06-08T00:00:00Z",
    }
    values.update(overrides)
    return values


def _insert_with_core(
    connection: sqlite3.Connection,
    table_name: str,
    row: dict[str, object],
    **core_overrides: object,
) -> None:
    values = {**row, **_core(**core_overrides)}
    columns = ", ".join(values)
    placeholders = ", ".join("?" for _ in values)
    connection.execute(
        f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
        tuple(values.values()),
    )


def _insert_with_core_or_ignore(
    connection: sqlite3.Connection,
    table_name: str,
    row: dict[str, object],
    **core_overrides: object,
) -> None:
    values = {**row, **_core(**core_overrides)}
    columns = ", ".join(values)
    placeholders = ", ".join("?" for _ in values)
    connection.execute(
        f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})",
        tuple(values.values()),
    )


def _insert_match(connection: sqlite3.Connection, match_id: str, *, updated_at: str) -> None:
    _insert_with_core_or_ignore(
        connection,
        "matches",
        {
            "match_id": match_id,
            "session_id": None,
            "parser_match_key": match_id,
            "match_started_at": "2026-06-08T00:00:00Z",
            "match_completed_at": updated_at,
        },
        updated_at=updated_at,
    )


def _insert_game(connection: sqlite3.Connection, match_id: str, game_number: int, *, updated_at: str) -> str:
    game_id = f"{match_id}:g{game_number}"
    _insert_with_core_or_ignore(
        connection,
        "games",
        {
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "game_started_at": "2026-06-08T00:00:00Z",
            "game_completed_at": updated_at,
        },
        updated_at=updated_at,
    )
    return game_id


def _insert_match_result(connection: sqlite3.Connection, match_id: str, *, updated_at: str) -> None:
    _insert_match(connection, match_id, updated_at=updated_at)
    _insert_with_core(
        connection,
        "match_results",
        {
            "match_result_id": f"{match_id}:match_result",
            "match_id": match_id,
            "match_result": "W",
            "winner_team_id": 1,
            "games_won": 2,
            "games_lost": 1,
            "total_games": 3,
            "match_win": 1,
            "game_win_rate": 0.667,
        },
        updated_at=updated_at,
    )


def _insert_game_result(connection: sqlite3.Connection, match_id: str, game_number: int, *, updated_at: str) -> None:
    game_id = _insert_game(connection, match_id, game_number, updated_at=updated_at)
    _insert_with_core(
        connection,
        "game_results",
        {
            "game_result_id": f"{game_id}:game_result",
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "winner_team_id": 1,
            "local_result": "win",
            "pre_postboard_label": "game1",
            "play_draw": "play",
            "turn_count": 8,
            "game_started_at": "2026-06-08T00:00:00Z",
            "game_completed_at": updated_at,
            "game_duration_seconds": 900.0,
        },
        updated_at=updated_at,
    )


def _sqlite_sidecars(app_root: Path) -> list[Path]:
    database_path = app_root / "db" / "mythic_edge.sqlite3"
    return [
        path
        for path in (
            database_path.with_suffix(".sqlite3-wal"),
            database_path.with_suffix(".sqlite3-shm"),
            database_path.with_suffix(".sqlite3-journal"),
        )
        if path.exists()
    ]
