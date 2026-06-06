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


def test_dashboard_modules_report_missing_database_without_creating_artifacts(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"

    payload = _client(app_root).get("/api/analytics/dashboard/modules").json()
    encoded = json.dumps(payload, sort_keys=True)

    assert payload["object"] == "mythic_edge_local_app_analytics_dashboard_modules"
    assert payload["schema_version"] == "analytics_dynamic_decision_support_dashboard.v1"
    assert payload["status"] == "missing"
    assert payload["database"]["display_path"] == "<app_data>\\db\\mythic_edge.sqlite3"
    assert [module["module_id"] for module in payload["modules"]] == [
        "play_draw_win_rate",
        "game1_postboard",
        "mulligan_opening_hand_outcomes",
    ]
    assert all(module["rows"] == [] for module in payload["modules"])
    assert payload["custom_explorer"]["builder_ui_enabled"] is False
    assert payload["custom_explorer"]["query_execution_enabled"] is False
    assert str(app_root) not in encoded
    assert "SELECT" not in encoded.upper()
    assert not app_root.exists()


def test_dashboard_modules_report_unavailable_app_data_without_creating_artifacts() -> None:
    payload = _client(None, env={}).get("/api/analytics/dashboard/modules").json()

    assert payload["status"] == "unavailable"
    assert payload["database"]["display_path"] == "<app_data>\\db\\mythic_edge.sqlite3"
    assert all(module["status"] == "unavailable" for module in payload["modules"])


def test_dashboard_modules_report_empty_current_database(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()

    payload = _client(app_root).get("/api/analytics/dashboard/modules").json()

    assert payload["status"] == "empty"
    assert len(payload["modules"]) == 3
    assert all(module["status"] == "empty" for module in payload["modules"])
    assert all(module["data_quality"]["sample_size_status"] == "empty" for module in payload["modules"])
    assert all(module["rows"] == [] for module in payload["modules"])
    assert _sqlite_sidecars(app_root) == []


def test_dashboard_modules_return_three_stock_modules_from_safe_analytics_sources(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        for index in range(10):
            _insert_game_result(
                connection,
                f"match:dash:play:{index}",
                1,
                local_result="win" if index < 6 else "loss",
                play_draw="play",
                pre_postboard_label="game1",
            )
        _insert_game_result(
            connection,
            "match:dash:draw",
            2,
            local_result="loss",
            play_draw="draw",
            pre_postboard_label="postboard",
        )
        _insert_game_result(
            connection,
            "match:dash:unknown",
            2,
            local_result=None,
            play_draw=None,
            pre_postboard_label="unknown",
            availability_status="expected_unavailable",
            drift_status="degraded",
        )
        _insert_opening_hand(connection, "match:dash:play:0", 1, hand_size=7, exact_card_count=7)
        _insert_mulligan_event(
            connection,
            "match:dash:play:0",
            1,
            ordinal_or_count="0",
            mulligan_count=0,
            decision_detail="kept_initial_hand",
        )
        _insert_opening_hand(connection, "match:dash:draw", 2, hand_size=6, exact_card_count=6)
        _insert_mulligan_event(
            connection,
            "match:dash:draw",
            2,
            ordinal_or_count="1",
            mulligan_count=1,
            decision_detail="mulliganed_to_six",
        )
        connection.commit()

    payload = _client(app_root).get("/api/analytics/dashboard/modules").json()
    encoded = json.dumps(payload, sort_keys=True)

    assert payload["status"] == "ok"
    assert [module["module_id"] for module in payload["modules"]] == [
        "play_draw_win_rate",
        "game1_postboard",
        "mulligan_opening_hand_outcomes",
    ]

    play_draw, game1_postboard, mulligan_opening = payload["modules"]
    assert play_draw["title"] == "Win Rate By Play/Draw"
    assert play_draw["default_view"] == "bar"
    assert [row["dimension_values"]["play_draw"] for row in play_draw["rows"]] == ["play", "draw", "unknown"]
    assert play_draw["rows"][0]["metrics"][4]["display"] == "60 percent"
    assert "small_sample" in play_draw["rows"][1]["warnings"]
    assert "unknown_or_degraded_results_present" in play_draw["rows"][2]["warnings"]

    assert game1_postboard["title"] == "Game 1 / Postboard"
    assert game1_postboard["source_metadata"]["source_tables_or_views"] == ["v_game1_vs_postboard"]
    assert [row["dimension_values"]["game1_postboard"] for row in game1_postboard["rows"]] == [
        "game1",
        "postboard",
        "unknown",
    ]
    assert game1_postboard["rows"][0]["metrics"][0]["display"] == "10 games"

    assert mulligan_opening["title"] == "Mulligan / Opening Hand Outcomes"
    assert mulligan_opening["default_view"] == "table"
    assert {
        row["dimension_values"]["mulligan_bucket"] for row in mulligan_opening["rows"]
    } == {"kept_initial_hand", "mulligan_1"}
    assert mulligan_opening["data_quality"]["finality"] == "analytics_projection"

    assert payload["custom_explorer"]["status"] == "deferred"
    journal_dimensions = [
        dimension
        for dimension in payload["custom_explorer"]["dimensions"]
        if dimension["value_source"] == "journal_annotation"
    ]
    assert journal_dimensions
    assert all(dimension["annotation_boundary"] == "Journal annotation" for dimension in journal_dimensions)
    assert str(app_root) not in encoded
    assert "SELECT" not in encoded.upper()
    assert "Player.log" not in encoded
    assert _sqlite_sidecars(app_root) == []


def test_dashboard_modules_degrade_unknown_schema_without_querying_rows(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    database_path = app_root / "db" / "mythic_edge.sqlite3"
    database_path.parent.mkdir(parents=True)
    connection = sqlite3.connect(database_path)
    try:
        connection.execute("CREATE TABLE game_results (game_result_id TEXT PRIMARY KEY)")
        connection.commit()
    finally:
        connection.close()

    payload = _client(app_root).get("/api/analytics/dashboard/modules").json()

    assert payload["status"] == "degraded"
    assert payload["warnings"] == ["analytics_schema_not_current"]
    assert all(module["warnings"] == ["analytics_schema_not_current"] for module in payload["modules"])
    assert all(module["rows"] == [] for module in payload["modules"])


def test_dashboard_modules_return_safe_error_for_invalid_or_broken_database(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    database_path = app_root / "db" / "mythic_edge.sqlite3"
    database_path.parent.mkdir(parents=True)
    database_path.write_text("not sqlite", encoding="utf-8")

    invalid_payload = _client(app_root).get("/api/analytics/dashboard/modules").json()

    assert invalid_payload["status"] == "error"
    assert invalid_payload["errors"] == ["database_invalid_sqlite"]
    assert str(app_root) not in json.dumps(invalid_payload, sort_keys=True)

    with _current_database(app_root, reset=True) as connection:
        connection.execute("DROP VIEW v_play_draw_splits")
        connection.commit()

    broken_payload = _client(app_root).get("/api/analytics/dashboard/modules").json()
    encoded = json.dumps(broken_payload, sort_keys=True)

    assert broken_payload["status"] == "error"
    assert broken_payload["errors"] == ["analytics_dashboard_query_failed"]
    assert "SELECT" not in encoded.upper()
    assert "NO SUCH" not in encoded.upper()
    assert str(app_root) not in encoded


def test_dashboard_modules_reject_unapproved_query_parameters_without_echo(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()

    response = _client(app_root).get("/api/analytics/dashboard/modules?table=v_play_draw_splits")
    encoded = json.dumps(response.json(), sort_keys=True)

    assert response.status_code == 422
    assert "analytics_dashboard_query_parameter_not_allowed" in encoded
    assert "v_play_draw_splits" not in encoded


def test_dashboard_modules_do_not_add_charting_dependency() -> None:
    package_json = json.loads(Path("frontend/package.json").read_text(encoding="utf-8"))
    dependencies = {
        **package_json.get("dependencies", {}),
        **package_json.get("devDependencies", {}),
    }

    assert not {"chart.js", "recharts", "d3", "victory", "nivo", "echarts"} & set(dependencies)


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
            "ingest:dashboard:test",
            "sanitized_golden_replay",
            "analytics_dynamic_dashboard_v1",
            "2026-06-04T00:00:00Z",
            "2026-06-04T00:00:01Z",
            "completed",
            "test",
            "test",
            ANALYTICS_SCHEMA_VERSION,
            "{}",
            "2026-06-04T00:00:00Z",
            "2026-06-04T00:00:00Z",
        ),
    )


def _core(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "value_source": "observed",
        "confidence": "high",
        "finality": "final",
        "drift_status": "none",
        "parser_schema_version": ANALYTICS_SCHEMA_VERSION,
        "ingest_run_id": "ingest:dashboard:test",
        "source_parser_surface": "synthetic_dashboard_test",
        "source_fact_key": "synthetic_fact",
        "availability_status": "available",
        "created_at": "2026-06-04T00:00:00Z",
        "updated_at": "2026-06-04T00:00:00Z",
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


def _insert_match(connection: sqlite3.Connection, match_id: str) -> None:
    _insert_with_core_or_ignore(
        connection,
        "matches",
        {
            "match_id": match_id,
            "session_id": None,
            "parser_match_key": match_id,
            "match_started_at": "2026-06-04T00:00:00Z",
            "match_completed_at": "2026-06-04T00:30:00Z",
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
            "game_started_at": "2026-06-04T00:00:00Z",
            "game_completed_at": "2026-06-04T00:10:00Z",
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
            "game_started_at": "2026-06-04T00:00:00Z",
            "game_completed_at": "2026-06-04T00:10:00Z",
            "game_duration_seconds": game_duration_seconds,
        },
        **core_overrides,
    )
    return game_id


def _insert_opening_hand(
    connection: sqlite3.Connection,
    match_id: str,
    game_number: int,
    *,
    hand_size: int,
    exact_card_count: int,
) -> str:
    game_id = f"{match_id}:g{game_number}"
    opening_hand_id = f"{game_id}:opening_hand"
    _insert_with_core(
        connection,
        "opening_hands",
        {
            "opening_hand_id": opening_hand_id,
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "hand_size": hand_size,
            "exact_card_count": exact_card_count,
        },
    )
    return opening_hand_id


def _insert_mulligan_event(
    connection: sqlite3.Connection,
    match_id: str,
    game_number: int,
    *,
    ordinal_or_count: str,
    mulligan_count: int,
    decision_detail: str,
) -> str:
    game_id = f"{match_id}:g{game_number}"
    mulligan_event_id = f"{game_id}:mulligan:{ordinal_or_count}"
    _insert_with_core(
        connection,
        "mulligan_events",
        {
            "mulligan_event_id": mulligan_event_id,
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "ordinal_or_count": ordinal_or_count,
            "mulligan_count": mulligan_count,
            "decision_detail": decision_detail,
        },
    )
    return mulligan_event_id


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
