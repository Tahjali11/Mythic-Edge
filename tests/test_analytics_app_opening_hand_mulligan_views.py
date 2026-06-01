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


def test_early_game_routes_report_missing_database_without_creating_artifacts(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)

    opening_payload = client.get("/api/analytics/opening-hands").json()
    mulligan_payload = client.get("/api/analytics/mulligans").json()
    encoded = json.dumps({"opening": opening_payload, "mulligans": mulligan_payload}, sort_keys=True)

    assert opening_payload["object"] == "mythic_edge_local_app_opening_hand_history"
    assert mulligan_payload["object"] == "mythic_edge_local_app_mulligan_history"
    assert opening_payload["schema_version"] == "analytics_app_opening_hand_mulligan_views.v1"
    assert mulligan_payload["schema_version"] == "analytics_app_opening_hand_mulligan_views.v1"
    assert opening_payload["status"] == "missing"
    assert mulligan_payload["status"] == "missing"
    assert opening_payload["summary"]["card_row_count"] == 0
    assert mulligan_payload["summary"]["card_row_count"] == 0
    assert opening_payload["rows"] == []
    assert mulligan_payload["rows"] == []
    assert opening_payload["database"]["display_path"] == "<app_data>\\db\\mythic_edge.sqlite3"
    assert str(app_root) not in encoded
    assert not app_root.exists()


@pytest.mark.parametrize("endpoint", ["/api/analytics/opening-hands", "/api/analytics/mulligans"])
def test_early_game_routes_report_empty_current_database(endpoint: str, tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()
    client = _client(app_root)

    payload = client.get(endpoint).json()

    assert payload["status"] == "empty"
    assert payload["pagination"] == {"limit": 50, "offset": 0, "returned": 0}
    assert payload["summary"] == {
        "row_count": 0,
        "card_row_count": 0,
        "degraded_row_count": 0,
        "unavailable_row_count": 0,
        "conflict_row_count": 0,
    }
    assert payload["rows"] == []


def test_opening_hand_history_groups_card_rows_and_keeps_zero_card_groups(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        _insert_match(connection, "match:opening:cards", completed_at="2026-05-30T01:30:00Z")
        _insert_game(connection, "match:opening:cards", 1, completed_at="2026-05-30T01:10:00Z")
        _insert_game_result(connection, "match:opening:cards", 1, local_result="win", play_draw="play")
        _insert_match_result(connection, "match:opening:cards", match_result="W", match_win=1)
        _insert_match_context(connection, "match:opening:cards", queue_name="Ranked")
        cards_opening_id = _insert_opening_hand(connection, "match:opening:cards", 1, hand_size=7, exact_card_count=2)
        _insert_opening_hand_card(connection, cards_opening_id, 1, grp_id=1001, card_name="Forest")
        _insert_opening_hand_card(
            connection,
            cards_opening_id,
            2,
            grp_id=1002,
            card_name="Swamp",
            confidence="low",
        )

        _insert_match(connection, "match:opening:empty", completed_at="2026-05-30T02:30:00Z")
        _insert_game(connection, "match:opening:empty", 1, completed_at="2026-05-30T02:10:00Z")
        _insert_opening_hand(connection, "match:opening:empty", 1, hand_size=7, exact_card_count=0)
        connection.commit()

    payload = _client(app_root).get("/api/analytics/opening-hands").json()

    assert payload["status"] == "ok"
    assert payload["summary"] == {
        "row_count": 2,
        "card_row_count": 2,
        "degraded_row_count": 1,
        "unavailable_row_count": 0,
        "conflict_row_count": 0,
    }
    assert [row["match_id"] for row in payload["rows"]] == ["match:opening:empty", "match:opening:cards"]

    empty_row = payload["rows"][0]
    assert empty_row["cards"] == []
    assert empty_row["game_result_status"] is None
    assert empty_row["match_result_status"] is None
    assert empty_row["context_status"] is None

    card_row = payload["rows"][1]
    assert card_row["opening_hand_id"] == "match:opening:cards:g1:opening_hand"
    assert card_row["local_result"] == "win"
    assert card_row["play_draw"] == "play"
    assert card_row["match_result"] == "W"
    assert card_row["queue_name"] == "Ranked"
    assert [card["card_position"] for card in card_row["cards"]] == [1, 2]
    assert [card["card_name"] for card in card_row["cards"]] == ["Forest", "Swamp"]
    assert card_row["cards"][1]["card_status"]["confidence"] == "low"


def test_mulligan_history_groups_cards_and_child_availability_summary(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        _insert_match(connection, "match:mulligans:1", completed_at="2026-05-30T03:30:00Z")
        _insert_game(connection, "match:mulligans:1", 1, completed_at="2026-05-30T03:10:00Z")
        _insert_game_result(connection, "match:mulligans:1", 1, local_result="loss", play_draw="draw")
        _insert_match_result(connection, "match:mulligans:1", match_result="L", match_win=0)
        _insert_match_context(connection, "match:mulligans:1", queue_name="Traditional Ranked")
        _insert_mulligan_event(
            connection,
            "match:mulligans:1",
            1,
            ordinal_or_count="0",
            mulligan_count=0,
            decision_detail="kept_initial_hand",
        )
        mulligan_event_id = _insert_mulligan_event(
            connection,
            "match:mulligans:1",
            1,
            ordinal_or_count="1",
            mulligan_count=1,
            decision_detail="mulliganed_to_six",
        )
        _insert_mulligan_card(connection, mulligan_event_id, 1, card_action="bottomed", grp_id=2001, card_name="Island")
        _insert_mulligan_card(
            connection,
            mulligan_event_id,
            2,
            card_action="discarded",
            grp_id=2002,
            card_name="Mountain",
            availability_status="expected_unavailable",
        )
        connection.commit()

    payload = _client(app_root).get("/api/analytics/mulligans").json()

    assert payload["status"] == "ok"
    assert payload["summary"] == {
        "row_count": 2,
        "card_row_count": 2,
        "degraded_row_count": 0,
        "unavailable_row_count": 1,
        "conflict_row_count": 0,
    }
    assert [row["ordinal_or_count"] for row in payload["rows"]] == ["0", "1"]
    assert payload["rows"][0]["cards"] == []
    row = payload["rows"][1]
    assert row["mulligan_count"] == 1
    assert row["decision_detail"] == "mulliganed_to_six"
    assert row["local_result"] == "loss"
    assert row["play_draw"] == "draw"
    assert row["match_result"] == "L"
    assert row["queue_name"] == "Traditional Ranked"
    assert [card["card_action"] for card in row["cards"]] == ["bottomed", "discarded"]
    assert row["cards"][1]["card_status"]["availability_status"] == "expected_unavailable"


def test_early_game_routes_degrade_unknown_schema_without_querying_rows(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    database_path = app_root / "db" / "mythic_edge.sqlite3"
    database_path.parent.mkdir(parents=True)
    connection = sqlite3.connect(database_path)
    try:
        connection.execute("CREATE TABLE opening_hands (opening_hand_id TEXT PRIMARY KEY)")
        connection.commit()
    finally:
        connection.close()
    client = _client(app_root)

    payload = client.get("/api/analytics/opening-hands").json()

    assert payload["status"] == "degraded"
    assert payload["rows"] == []
    assert payload["summary"]["card_row_count"] == 0
    assert payload["warnings"] == ["analytics_schema_not_current"]
    assert payload["errors"] == []


def test_early_game_routes_return_safe_error_for_fixed_query_failure(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        _insert_match(connection, "match:mulligans:broken", completed_at="2026-05-30T04:30:00Z")
        _insert_game(connection, "match:mulligans:broken", 1, completed_at="2026-05-30T04:10:00Z")
        _insert_mulligan_event(
            connection,
            "match:mulligans:broken",
            1,
            ordinal_or_count="1",
            mulligan_count=1,
            decision_detail="mulliganed_to_six",
        )
        connection.execute("DROP TABLE mulligan_bottomed_or_discarded_cards")
        connection.commit()
    client = _client(app_root)

    payload = client.get("/api/analytics/mulligans").json()

    assert payload["status"] == "error"
    assert payload["errors"] == ["analytics_history_query_failed"]
    assert payload["summary"]["card_row_count"] == 0
    assert "SELECT" not in json.dumps(payload, sort_keys=True).upper()
    assert str(app_root) not in json.dumps(payload, sort_keys=True)


@pytest.mark.parametrize("endpoint", ["/api/analytics/opening-hands", "/api/analytics/mulligans"])
@pytest.mark.parametrize(
    "query",
    [
        "table=opening_hands",
        "limit=C:%5Csecret%5CPlayer.log",
        "offset=C:%5Csecret%5CPlayer.log",
        "limit=0",
        "limit=101",
        "offset=-1",
        "limit=5&limit=6",
    ],
)
def test_early_game_routes_reject_malformed_query_params_without_echo(
    endpoint: str,
    query: str,
    tmp_path: Path,
) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        connection.commit()
    client = _client(app_root)

    response = client.get(f"{endpoint}?{query}")

    assert response.status_code == 422
    encoded = json.dumps(response.json(), sort_keys=True)
    assert "analytics_history_query_parameter_" in encoded
    assert "opening_hands" not in encoded
    assert "Player.log" not in encoded
    assert "C:" not in encoded
    assert "secret" not in encoded


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
            "ingest:early-game:test",
            "sanitized_golden_replay",
            "analytics_opening_hand_mulligan_views_v1",
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
        "ingest_run_id": "ingest:early-game:test",
        "source_parser_surface": "synthetic_early_game_history_test",
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


def _insert_match(connection: sqlite3.Connection, match_id: str, *, completed_at: str) -> None:
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


def _insert_game(connection: sqlite3.Connection, match_id: str, game_number: int, *, completed_at: str) -> str:
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
    return game_id


def _insert_game_result(
    connection: sqlite3.Connection,
    match_id: str,
    game_number: int,
    *,
    local_result: str,
    play_draw: str,
) -> None:
    game_id = f"{match_id}:g{game_number}"
    _insert_with_core(
        connection,
        "game_results",
        {
            "game_result_id": f"{game_id}:game_result",
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "winner_team_id": 1 if local_result == "win" else 2,
            "local_result": local_result,
            "pre_postboard_label": "game1",
            "play_draw": play_draw,
            "turn_count": 8,
            "game_started_at": "2026-05-30T00:00:00Z",
            "game_completed_at": "2026-05-30T00:10:00Z",
            "game_duration_seconds": 900.0,
        },
        source_fact_key="game_result",
    )


def _insert_match_result(connection: sqlite3.Connection, match_id: str, *, match_result: str, match_win: int) -> None:
    _insert_with_core(
        connection,
        "match_results",
        {
            "match_result_id": f"{match_id}:match_result",
            "match_id": match_id,
            "match_result": match_result,
            "winner_team_id": 1 if match_win else 2,
            "games_won": 2 if match_win else 1,
            "games_lost": 1 if match_win else 2,
            "total_games": 3,
            "match_win": match_win,
            "game_win_rate": 2 / 3 if match_win else 1 / 3,
        },
        source_fact_key="match_result",
    )


def _insert_match_context(connection: sqlite3.Connection, match_id: str, *, queue_name: str) -> None:
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
    )


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
        source_fact_key="opening_hand",
    )
    return opening_hand_id


def _insert_opening_hand_card(
    connection: sqlite3.Connection,
    opening_hand_id: str,
    card_position: int,
    *,
    grp_id: int,
    card_name: str,
    **core_overrides: object,
) -> None:
    _insert_with_core(
        connection,
        "opening_hand_cards",
        {
            "opening_hand_card_id": f"{opening_hand_id}:slot{card_position}",
            "opening_hand_id": opening_hand_id,
            "game_id": opening_hand_id.removesuffix(":opening_hand"),
            "card_position": card_position,
            "grp_id": grp_id,
            "card_name": card_name,
            "identity_hint_source": "direct_grp_id",
            "name_resolution_status": "resolved",
        },
        source_fact_key=f"opening_hand_card_{card_position}",
        **core_overrides,
    )


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
        source_fact_key=f"mulligan_{ordinal_or_count}",
    )
    return mulligan_event_id


def _insert_mulligan_card(
    connection: sqlite3.Connection,
    mulligan_event_id: str,
    card_position: int,
    *,
    card_action: str,
    grp_id: int,
    card_name: str,
    **core_overrides: object,
) -> None:
    game_id = mulligan_event_id.split(":mulligan:", maxsplit=1)[0]
    _insert_with_core(
        connection,
        "mulligan_bottomed_or_discarded_cards",
        {
            "mulligan_card_id": f"{mulligan_event_id}:card{card_position}",
            "mulligan_event_id": mulligan_event_id,
            "game_id": game_id,
            "card_position": card_position,
            "card_action": card_action,
            "grp_id": grp_id,
            "card_name": card_name,
            "identity_hint_source": "direct_grp_id",
        },
        source_fact_key=f"mulligan_card_{card_position}",
        **core_overrides,
    )
