from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from mythic_edge_parser.app.analytics_migration_loader import (
    ANALYTICS_SCHEMA_VERSION,
    apply_analytics_migrations,
)
from mythic_edge_parser.local_app.backend import create_app


def _client(app_data_root: Path) -> TestClient:
    return TestClient(create_app(app_data_root=app_data_root))


def test_history_routes_report_missing_database_without_creating_artifacts(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)

    matches_payload = client.get("/api/analytics/matches").json()
    games_payload = client.get("/api/analytics/games").json()
    encoded = json.dumps({"matches": matches_payload, "games": games_payload}, sort_keys=True)

    assert matches_payload["object"] == "mythic_edge_local_app_match_history"
    assert games_payload["object"] == "mythic_edge_local_app_game_history"
    assert matches_payload["status"] == "missing"
    assert games_payload["status"] == "missing"
    assert matches_payload["rows"] == []
    assert games_payload["rows"] == []
    assert matches_payload["database"]["display_path"] == "<app_data>\\db\\mythic_edge.sqlite3"
    assert str(app_root) not in encoded
    assert not app_root.exists()


def test_history_routes_report_empty_current_database(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()
    client = _client(app_root)

    payload = client.get("/api/analytics/matches").json()

    assert payload["status"] == "empty"
    assert payload["database"] == {
        "display_path": "<app_data>\\db\\mythic_edge.sqlite3",
        "exists": True,
        "schema_status": "schema_current",
        "status": "ok",
    }
    assert payload["pagination"] == {"limit": 50, "offset": 0, "returned": 0}
    assert payload["summary"] == {
        "row_count": 0,
        "degraded_row_count": 0,
        "unavailable_row_count": 0,
        "conflict_row_count": 0,
    }
    assert payload["rows"] == []


def test_match_history_uses_fixed_projection_order_and_status_summary(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        _insert_match_with_optional_rows(
            connection,
            "match:history:old",
            completed_at="2026-05-30T00:30:00Z",
            match_result="L",
            match_win=0,
            queue_name="Ranked",
            result_core={"confidence": "low", "drift_status": "degraded"},
            context_core={"availability_status": "not_observed"},
        )
        _insert_match_with_optional_rows(
            connection,
            "match:history:new",
            completed_at="2026-05-30T01:30:00Z",
            match_result="W",
            match_win=1,
            queue_name="Play",
            result_core={"value_source": "conflict", "drift_status": "conflict"},
        )
        connection.commit()
    client = _client(app_root)

    first_page = client.get("/api/analytics/matches?limit=1").json()
    second_page = client.get("/api/analytics/matches?limit=1&offset=1").json()

    assert first_page["status"] == "ok"
    assert first_page["pagination"] == {"limit": 1, "offset": 0, "returned": 1}
    assert first_page["summary"] == {
        "row_count": 1,
        "degraded_row_count": 1,
        "unavailable_row_count": 0,
        "conflict_row_count": 1,
    }
    row = first_page["rows"][0]
    assert row["match_id"] == "match:history:new"
    assert row["match_result"] == "W"
    assert row["match_win"] == 1
    assert row["games_won"] == 2
    assert row["games_lost"] == 1
    assert row["total_games"] == 3
    assert row["game_win_rate"] == 2 / 3
    assert row["queue_name"] == "Play"
    assert row["match_status"]["source_parser_surface"] == "synthetic_history_test"
    assert row["result_status"]["value_source"] == "conflict"
    assert row["context_status"]["availability_status"] == "available"
    assert second_page["rows"][0]["match_id"] == "match:history:old"
    assert second_page["summary"]["degraded_row_count"] == 1
    assert second_page["summary"]["unavailable_row_count"] == 1


def test_game_history_uses_fixed_projection_and_optional_join_nulls(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        _insert_match_with_optional_rows(
            connection,
            "match:games",
            completed_at="2026-05-30T00:30:00Z",
            match_result="W",
            match_win=1,
            queue_name="Traditional Ranked",
        )
        _insert_game(
            connection,
            "match:games",
            1,
            completed_at="2026-05-30T00:10:00Z",
            include_result=True,
            result_core={"confidence": "unknown"},
        )
        _insert_game(
            connection,
            "match:games",
            2,
            completed_at="2026-05-30T00:20:00Z",
            include_result=False,
        )
        connection.commit()
    client = _client(app_root)

    payload = client.get("/api/analytics/games").json()

    assert payload["status"] == "ok"
    assert payload["summary"] == {
        "row_count": 2,
        "degraded_row_count": 1,
        "unavailable_row_count": 0,
        "conflict_row_count": 0,
    }
    assert [row["game_number"] for row in payload["rows"]] == [2, 1]
    latest = payload["rows"][0]
    assert latest["game_id"] == "match:games:g2"
    assert latest["result_status"] is None
    assert latest["local_result"] is None
    assert latest["queue_name"] == "Traditional Ranked"
    first = payload["rows"][1]
    assert first["local_result"] == "win"
    assert first["play_draw"] == "play"
    assert first["turn_count"] == 8
    assert first["result_status"]["confidence"] == "unknown"


def test_history_routes_degrade_unknown_schema_without_querying_rows(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    database_path = app_root / "db" / "mythic_edge.sqlite3"
    database_path.parent.mkdir(parents=True)
    connection = sqlite3.connect(database_path)
    try:
        connection.execute("CREATE TABLE matches (match_id TEXT PRIMARY KEY)")
        connection.commit()
    finally:
        connection.close()
    client = _client(app_root)

    payload = client.get("/api/analytics/matches").json()

    assert payload["status"] == "degraded"
    assert payload["rows"] == []
    assert payload["warnings"] == ["analytics_schema_not_current"]
    assert payload["errors"] == []


def test_history_routes_return_safe_error_for_invalid_or_broken_database(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    database_path = app_root / "db" / "mythic_edge.sqlite3"
    database_path.parent.mkdir(parents=True)
    database_path.write_text("not sqlite", encoding="utf-8")
    client = _client(app_root)

    invalid_payload = client.get("/api/analytics/matches").json()

    assert invalid_payload["status"] == "error"
    assert invalid_payload["errors"] == ["database_invalid_sqlite"]
    assert str(app_root) not in json.dumps(invalid_payload, sort_keys=True)

    with _current_database(app_root, reset=True) as connection:
        connection.execute("DROP TABLE game_results")
        connection.commit()

    broken_payload = client.get("/api/analytics/games").json()

    assert broken_payload["status"] == "error"
    assert broken_payload["errors"] == ["analytics_history_query_failed"]
    assert "SELECT" not in json.dumps(broken_payload, sort_keys=True).upper()


def test_history_routes_reject_unapproved_query_parameters(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()
    client = _client(app_root)

    response = client.get("/api/analytics/matches?table=matches")

    assert response.status_code == 422
    encoded = json.dumps(response.json(), sort_keys=True)
    assert "analytics_history_query_parameter_not_allowed" in encoded
    assert "matches" not in encoded


@pytest.mark.parametrize("endpoint", ["/api/analytics/matches", "/api/analytics/games"])
@pytest.mark.parametrize("query_key", ["limit", "offset"])
def test_history_routes_reject_malformed_pagination_without_echo(endpoint: str, query_key: str, tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()
    client = _client(app_root)

    response = client.get(f"{endpoint}?{query_key}=C:%5Csecret%5CPlayer.log")

    assert response.status_code == 422
    encoded = json.dumps(response.json(), sort_keys=True)
    assert "analytics_history_query_parameter_invalid" in encoded
    assert "Player.log" not in encoded
    assert "C:" not in encoded
    assert "secret" not in encoded


@pytest.mark.parametrize("query", ["limit=0", "limit=101", "offset=-1", "limit=5&limit=6"])
def test_history_routes_reject_out_of_bounds_or_duplicate_pagination(query: str, tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()
    client = _client(app_root)

    response = client.get(f"/api/analytics/matches?{query}")

    assert response.status_code == 422
    encoded = json.dumps(response.json(), sort_keys=True)
    assert "analytics_history_query_parameter_invalid" in encoded


@contextmanager
def _current_database(app_root: Path, *, reset: bool = False) -> Iterator[sqlite3.Connection]:
    database_path = app_root / "db" / "mythic_edge.sqlite3"
    database_path.parent.mkdir(parents=True, exist_ok=True)
    if reset and database_path.exists():
        database_path.unlink()
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
            "ingest:history:test",
            "sanitized_golden_replay",
            "analytics_history_views_v1",
            "2026-05-30T00:00:00Z",
            "2026-05-30T00:00:01Z",
            "completed",
            "test",
            "test",
            ANALYTICS_SCHEMA_VERSION,
            "{}",
            "2026-05-30T00:00:00Z",
            "2026-05-30T00:00:00Z",
        ),
    )


def _core(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "value_source": "observed",
        "confidence": "high",
        "finality": "final",
        "drift_status": "none",
        "parser_schema_version": ANALYTICS_SCHEMA_VERSION,
        "ingest_run_id": "ingest:history:test",
        "source_parser_surface": "synthetic_history_test",
        "source_fact_key": "synthetic_fact",
        "availability_status": "available",
        "created_at": "2026-05-30T00:00:00Z",
        "updated_at": "2026-05-30T00:00:00Z",
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


def _insert_match_with_optional_rows(
    connection: sqlite3.Connection,
    match_id: str,
    *,
    completed_at: str,
    match_result: str,
    match_win: int,
    queue_name: str,
    result_core: dict[str, object] | None = None,
    context_core: dict[str, object] | None = None,
) -> None:
    _insert_with_core(
        connection,
        "matches",
        {
            "match_id": match_id,
            "session_id": None,
            "parser_match_key": match_id,
            "match_started_at": "2026-05-30T00:00:00Z",
            "match_completed_at": completed_at,
        },
        source_fact_key="match_id",
    )
    _insert_with_core(
        connection,
        "match_results",
        {
            "match_result_id": f"{match_id}:match_result",
            "match_id": match_id,
            "match_result": match_result,
            "winner_team_id": None,
            "games_won": 2,
            "games_lost": 1,
            "total_games": 3,
            "match_win": match_win,
            "game_win_rate": 2 / 3,
        },
        source_fact_key="match_result",
        **(result_core or {}),
    )
    _insert_with_core(
        connection,
        "match_context",
        {
            "match_context_id": f"{match_id}:match_context",
            "match_id": match_id,
            "queue_name": queue_name,
            "format_name": "Standard",
            "event_id": "PremierDraft",
            "match_win_condition": None,
            "event_type": None,
            "event_scope": None,
            "event_source": None,
        },
        source_fact_key="match_context",
        **(context_core or {}),
    )


def _insert_game(
    connection: sqlite3.Connection,
    match_id: str,
    game_number: int,
    *,
    completed_at: str,
    include_result: bool,
    result_core: dict[str, object] | None = None,
) -> None:
    game_id = f"{match_id}:g{game_number}"
    _insert_with_core(
        connection,
        "games",
        {
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "game_started_at": "2026-05-30T00:00:00Z",
            "game_completed_at": completed_at,
        },
        source_fact_key="game_id",
    )
    if not include_result:
        return
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
            "game_started_at": "2026-05-30T00:00:00Z",
            "game_completed_at": completed_at,
            "game_duration_seconds": 900.0,
        },
        source_fact_key="game_result",
        **(result_core or {}),
    )
