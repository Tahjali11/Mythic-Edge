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


def test_split_review_routes_report_missing_database_without_creating_artifacts(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)

    play_draw_payload = client.get("/api/analytics/play-draw-splits").json()
    postboard_payload = client.get("/api/analytics/game1-postboard-splits").json()
    encoded = json.dumps({"play_draw": play_draw_payload, "postboard": postboard_payload}, sort_keys=True)

    assert play_draw_payload["object"] == "mythic_edge_local_app_play_draw_split_review"
    assert postboard_payload["object"] == "mythic_edge_local_app_game1_postboard_split_review"
    assert play_draw_payload["schema_version"] == "analytics_app_play_draw_postboard_split_views.v1"
    assert postboard_payload["schema_version"] == "analytics_app_play_draw_postboard_split_views.v1"
    assert play_draw_payload["status"] == "missing"
    assert postboard_payload["status"] == "missing"
    assert play_draw_payload["rows"] == []
    assert postboard_payload["rows"] == []
    assert play_draw_payload["summary"] == _empty_play_draw_summary()
    assert postboard_payload["summary"] == _empty_game1_postboard_summary()
    assert play_draw_payload["database"]["display_path"] == "<app_data>\\db\\mythic_edge.sqlite3"
    assert str(app_root) not in encoded
    assert not app_root.exists()


@pytest.mark.parametrize("endpoint", ["/api/analytics/play-draw-splits", "/api/analytics/game1-postboard-splits"])
def test_split_review_routes_report_empty_current_database(endpoint: str, tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()
    client = _client(app_root)

    payload = client.get(endpoint).json()

    assert payload["status"] == "empty"
    assert payload["pagination"] == {"limit": 50, "offset": 0, "returned": 0}
    assert payload["rows"] == []
    if endpoint.endswith("play-draw-splits"):
        assert payload["summary"] == _empty_play_draw_summary()
    else:
        assert payload["summary"] == _empty_game1_postboard_summary()


def test_play_draw_split_review_uses_sample_warnings_and_keeps_unknown_counts(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        for index in range(10):
            _insert_game_result(
                connection,
                f"match:play:{index}",
                1,
                local_result="win" if index < 6 else "loss",
                play_draw="play",
                pre_postboard_label="game1",
            )
        _insert_game_result(
            connection,
            "match:draw:win",
            1,
            local_result="win",
            play_draw="draw",
            pre_postboard_label="game1",
        )
        _insert_game_result(
            connection,
            "match:draw:unknown",
            1,
            local_result=None,
            play_draw="draw",
            pre_postboard_label="game1",
            availability_status="expected_unavailable",
        )
        _insert_game_result(
            connection,
            "match:unknown:pending",
            1,
            local_result="pending",
            play_draw=None,
            pre_postboard_label="unknown",
            value_source="conflict",
            drift_status="conflict",
        )
        connection.commit()

    payload = _client(app_root).get("/api/analytics/play-draw-splits").json()

    assert payload["status"] == "ok"
    assert payload["summary"] == {
        "row_count": 3,
        "total_game_count": 13,
        "known_result_count": 11,
        "wins": 7,
        "losses": 4,
        "unknown_result_count": 2,
        "unavailable_result_count": 1,
        "degraded_result_count": 1,
        "small_sample_group_count": 2,
    }
    assert [row["play_draw"] for row in payload["rows"]] == ["play", "draw", "unknown"]

    play_row, draw_row, unknown_row = payload["rows"]
    assert play_row["game_count"] == 10
    assert play_row["known_result_count"] == 10
    assert play_row["wins"] == 6
    assert play_row["losses"] == 4
    assert play_row["win_rate"] == 0.6
    assert play_row["sample_size_warning"] == "ok"

    assert draw_row["game_count"] == 2
    assert draw_row["known_result_count"] == 1
    assert draw_row["unknown_result_count"] == 1
    assert draw_row["unavailable_result_count"] == 1
    assert draw_row["win_rate"] == 1.0
    assert draw_row["sample_size_warning"] == "small_sample"

    assert unknown_row["play_draw"] == "unknown"
    assert unknown_row["known_result_count"] == 0
    assert unknown_row["unknown_result_count"] == 1
    assert unknown_row["degraded_result_count"] == 1
    assert unknown_row["win_rate"] is None
    assert unknown_row["sample_size_warning"] == "small_sample"


def test_game1_postboard_split_review_preserves_status_and_nonstandard_results(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        _insert_game_result(
            connection,
            "match:split:z",
            1,
            local_result="win",
            play_draw="play",
            pre_postboard_label="preboard",
            turn_count=6,
            game_duration_seconds=601.5,
        )
        _insert_game_result(
            connection,
            "match:split:z",
            2,
            local_result="loss",
            play_draw="draw",
            pre_postboard_label="postboard",
            turn_count=9,
            game_duration_seconds=None,
            availability_status="expected_unavailable",
        )
        _insert_game_result(
            connection,
            "match:split:z",
            3,
            local_result="pending",
            play_draw="unknown",
            pre_postboard_label="postboard",
            turn_count=None,
            game_duration_seconds=1200.0,
            value_source="conflict",
            drift_status="conflict",
        )
        connection.commit()

    payload = _client(app_root).get("/api/analytics/game1-postboard-splits").json()

    assert payload["status"] == "ok"
    assert payload["summary"] == {
        "row_count": 3,
        "game1_row_count": 1,
        "postboard_row_count": 2,
        "known_result_count": 2,
        "unknown_result_count": 1,
        "degraded_row_count": 1,
        "unavailable_row_count": 1,
        "conflict_row_count": 1,
    }
    assert [row["game_number"] for row in payload["rows"]] == [1, 2, 3]

    game1_row = payload["rows"][0]
    assert game1_row["game_result_id"] == "match:split:z:g1:game_result"
    assert game1_row["pre_postboard_label"] == "preboard"
    assert game1_row["local_result"] == "win"
    assert game1_row["play_draw"] == "play"
    assert game1_row["turn_count"] == 6
    assert game1_row["game_duration_seconds"] == 601.5
    assert game1_row["game_result_status"]["source_parser_surface"] == "synthetic_split_review_test"

    unavailable_row = payload["rows"][1]
    assert unavailable_row["local_result"] == "loss"
    assert unavailable_row["game_duration_seconds"] is None
    assert unavailable_row["game_result_status"]["availability_status"] == "expected_unavailable"

    conflict_row = payload["rows"][2]
    assert conflict_row["local_result"] == "pending"
    assert conflict_row["turn_count"] is None
    assert conflict_row["game_result_status"]["value_source"] == "conflict"
    assert conflict_row["game_result_status"]["drift_status"] == "conflict"


def test_split_review_routes_degrade_unknown_schema_without_querying_rows(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    database_path = app_root / "db" / "mythic_edge.sqlite3"
    database_path.parent.mkdir(parents=True)
    connection = sqlite3.connect(database_path)
    try:
        connection.execute("CREATE TABLE game_results (game_result_id TEXT PRIMARY KEY)")
        connection.commit()
    finally:
        connection.close()

    payload = _client(app_root).get("/api/analytics/play-draw-splits").json()

    assert payload["status"] == "degraded"
    assert payload["rows"] == []
    assert payload["summary"] == _empty_play_draw_summary()
    assert payload["warnings"] == ["analytics_schema_not_current"]
    assert payload["errors"] == []


@pytest.mark.parametrize("endpoint", ["/api/analytics/play-draw-splits", "/api/analytics/game1-postboard-splits"])
def test_split_review_routes_return_safe_error_for_invalid_or_broken_database(endpoint: str, tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    database_path = app_root / "db" / "mythic_edge.sqlite3"
    database_path.parent.mkdir(parents=True)
    database_path.write_text("not sqlite", encoding="utf-8")

    invalid_payload = _client(app_root).get(endpoint).json()

    assert invalid_payload["status"] == "error"
    assert invalid_payload["errors"] == ["database_invalid_sqlite"]
    assert str(app_root) not in json.dumps(invalid_payload, sort_keys=True)

    with _current_database(app_root, reset=True) as connection:
        connection.execute("DROP TABLE game_results")
        connection.commit()

    broken_payload = _client(app_root).get(endpoint).json()

    assert broken_payload["status"] == "error"
    assert broken_payload["errors"] == ["analytics_history_query_failed"]
    encoded = json.dumps(broken_payload, sort_keys=True).upper()
    assert "SELECT" not in encoded
    assert "V_PLAY_DRAW_SPLITS" not in encoded
    assert "V_GAME1_VS_POSTBOARD" not in encoded


@pytest.mark.parametrize("endpoint", ["/api/analytics/play-draw-splits", "/api/analytics/game1-postboard-splits"])
def test_split_review_routes_reject_unapproved_query_parameters(endpoint: str, tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()

    response = _client(app_root).get(f"{endpoint}?table=v_play_draw_splits")

    assert response.status_code == 422
    encoded = json.dumps(response.json(), sort_keys=True)
    assert "analytics_history_query_parameter_not_allowed" in encoded
    assert "v_play_draw_splits" not in encoded


@pytest.mark.parametrize("endpoint", ["/api/analytics/play-draw-splits", "/api/analytics/game1-postboard-splits"])
@pytest.mark.parametrize("query_key", ["limit", "offset"])
def test_split_review_routes_reject_malformed_pagination_without_echo(
    endpoint: str,
    query_key: str,
    tmp_path: Path,
) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()

    response = _client(app_root).get(f"{endpoint}?{query_key}=C:%5Csecret%5CPlayer.log")

    assert response.status_code == 422
    encoded = json.dumps(response.json(), sort_keys=True)
    assert "analytics_history_query_parameter_invalid" in encoded
    assert "Player.log" not in encoded
    assert "C:" not in encoded
    assert "secret" not in encoded


@pytest.mark.parametrize("endpoint", ["/api/analytics/play-draw-splits", "/api/analytics/game1-postboard-splits"])
@pytest.mark.parametrize("query", ["limit=0", "limit=101", "offset=-1", "limit=5&limit=6"])
def test_split_review_routes_reject_out_of_bounds_or_duplicate_pagination(
    endpoint: str,
    query: str,
    tmp_path: Path,
) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()

    response = _client(app_root).get(f"{endpoint}?{query}")

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


def _empty_play_draw_summary() -> dict[str, int]:
    return {
        "row_count": 0,
        "total_game_count": 0,
        "known_result_count": 0,
        "wins": 0,
        "losses": 0,
        "unknown_result_count": 0,
        "unavailable_result_count": 0,
        "degraded_result_count": 0,
        "small_sample_group_count": 0,
    }


def _empty_game1_postboard_summary() -> dict[str, int]:
    return {
        "row_count": 0,
        "game1_row_count": 0,
        "postboard_row_count": 0,
        "known_result_count": 0,
        "unknown_result_count": 0,
        "degraded_row_count": 0,
        "unavailable_row_count": 0,
        "conflict_row_count": 0,
    }


def _core(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "value_source": "observed",
        "confidence": "high",
        "finality": "final",
        "drift_status": "none",
        "parser_schema_version": ANALYTICS_SCHEMA_VERSION,
        "ingest_run_id": "ingest:split-review:test",
        "source_parser_surface": "synthetic_split_review_test",
        "source_fact_key": "synthetic_fact",
        "availability_status": "available",
        "created_at": "2026-06-01T00:00:00Z",
        "updated_at": "2026-06-01T00:00:00Z",
    }
    values.update(overrides)
    return values


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
            "ingest:split-review:test",
            "sanitized_golden_replay",
            "analytics_app_split_review_v1",
            "2026-06-01T00:00:00Z",
            "2026-06-01T00:00:01Z",
            "completed",
            "test",
            "test",
            ANALYTICS_SCHEMA_VERSION,
            "{}",
            "2026-06-01T00:00:00Z",
            "2026-06-01T00:00:00Z",
        ),
    )


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


def _insert_match(connection: sqlite3.Connection, match_id: str) -> None:
    _insert_with_core_or_ignore(
        connection,
        "matches",
        {
            "match_id": match_id,
            "session_id": None,
            "parser_match_key": match_id,
            "match_started_at": "2026-06-01T00:00:00Z",
            "match_completed_at": "2026-06-01T00:30:00Z",
        },
    )


def _insert_game(connection: sqlite3.Connection, match_id: str, game_number: int) -> str:
    game_id = f"{match_id}:g{game_number}"
    _insert_with_core_or_ignore(
        connection,
        "games",
        {
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "game_started_at": "2026-06-01T00:00:00Z",
            "game_completed_at": "2026-06-01T00:10:00Z",
        },
    )
    return game_id


def _insert_game_result(
    connection: sqlite3.Connection,
    match_id: str,
    game_number: int,
    *,
    local_result: str | None,
    play_draw: str | None,
    pre_postboard_label: str | None,
    turn_count: int | None = 5,
    game_duration_seconds: float | None = 900.0,
    **core_overrides: object,
) -> str:
    _insert_match(connection, match_id)
    game_id = _insert_game(connection, match_id, game_number)
    _insert_with_core(
        connection,
        "game_results",
        {
            "game_result_id": f"{game_id}:game_result",
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "winner_team_id": None,
            "local_result": local_result,
            "pre_postboard_label": pre_postboard_label,
            "play_draw": play_draw,
            "turn_count": turn_count,
            "game_started_at": "2026-06-01T00:00:00Z",
            "game_completed_at": "2026-06-01T00:10:00Z",
            "game_duration_seconds": game_duration_seconds,
        },
        **core_overrides,
    )
    return game_id
