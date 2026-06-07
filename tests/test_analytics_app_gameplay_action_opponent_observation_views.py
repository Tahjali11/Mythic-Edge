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


def test_action_review_routes_report_missing_database_without_creating_artifacts(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    client = _client(app_root)

    actions_payload = client.get("/api/analytics/gameplay-actions").json()
    observations_payload = client.get("/api/analytics/opponent-card-observations").json()
    encoded = json.dumps({"actions": actions_payload, "observations": observations_payload}, sort_keys=True)

    assert actions_payload["object"] == "mythic_edge_local_app_gameplay_action_review"
    assert observations_payload["object"] == "mythic_edge_local_app_opponent_card_observation_review"
    assert actions_payload["schema_version"] == "analytics_app_gameplay_action_opponent_observation_views.v1"
    assert observations_payload["schema_version"] == "analytics_app_gameplay_action_opponent_observation_views.v1"
    assert actions_payload["status"] == "missing"
    assert observations_payload["status"] == "missing"
    assert actions_payload["summary"]["card_row_count"] == 0
    assert observations_payload["summary"]["card_row_count"] == 0
    assert actions_payload["summary"]["review_required_row_count"] == 0
    assert observations_payload["summary"]["review_required_row_count"] == 0
    assert actions_payload["rows"] == []
    assert observations_payload["rows"] == []
    assert actions_payload["database"]["display_path"] == "<app_data>\\db\\mythic_edge.sqlite3"
    assert str(app_root) not in encoded
    assert not app_root.exists()


@pytest.mark.parametrize("endpoint", ["/api/analytics/gameplay-actions", "/api/analytics/opponent-card-observations"])
def test_action_review_routes_report_empty_current_database(endpoint: str, tmp_path: Path) -> None:
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
        "review_required_row_count": 0,
    }
    assert payload["rows"] == []


def test_gameplay_action_review_groups_card_rows_and_keeps_zero_card_groups(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        _insert_match(connection, "match:actions:cards", completed_at="2026-05-30T01:30:00Z")
        _insert_game(connection, "match:actions:cards", 1, completed_at="2026-05-30T01:10:00Z")
        _insert_game_result(connection, "match:actions:cards", 1, local_result="win", play_draw="play")
        _insert_match_result(connection, "match:actions:cards", match_result="W", match_win=1)
        _insert_match_context(connection, "match:actions:cards", queue_name="Ranked")
        action_id = _insert_gameplay_action(
            connection,
            "match:actions:cards",
            1,
            timestamp="2026-05-30T01:05:00Z",
            action_type="cast",
            turn_number=2,
        )
        _insert_gameplay_action_card(connection, action_id, 1, grp_id=1001, card_name="Forest")
        _insert_gameplay_action_card(
            connection,
            action_id,
            2,
            grp_id=1002,
            card_name="Swamp",
            confidence="low",
        )

        _insert_match(connection, "match:actions:empty", completed_at="2026-05-30T02:30:00Z")
        _insert_game(connection, "match:actions:empty", 1, completed_at="2026-05-30T02:10:00Z")
        _insert_gameplay_action(
            connection,
            "match:actions:empty",
            1,
            timestamp="2026-05-30T02:05:00Z",
            action_type="pass_priority",
            turn_number=None,
        )
        connection.commit()

    payload = _client(app_root).get("/api/analytics/gameplay-actions").json()

    assert payload["status"] == "ok"
    assert payload["summary"] == {
        "row_count": 2,
        "card_row_count": 2,
        "degraded_row_count": 1,
        "unavailable_row_count": 0,
        "conflict_row_count": 0,
        "review_required_row_count": 0,
    }
    assert [row["match_id"] for row in payload["rows"]] == ["match:actions:empty", "match:actions:cards"]

    empty_row = payload["rows"][0]
    assert empty_row["cards"] == []
    assert empty_row["card_count"] == 0
    assert empty_row["turn_number"] is None
    assert empty_row["game_result_status"] is None
    assert empty_row["match_result_status"] is None
    assert empty_row["context_status"] is None

    card_row = payload["rows"][1]
    assert card_row["gameplay_action_id"] == "match:actions:cards:g1:action:cast"
    assert card_row["visible_in_log"] is True
    assert card_row["grp_ids"] == [1001, 1002]
    assert card_row["local_result"] == "win"
    assert card_row["play_draw"] == "play"
    assert card_row["match_result"] == "W"
    assert card_row["queue_name"] == "Ranked"
    assert [card["card_ordinal"] for card in card_row["cards"]] == [1, 2]
    assert [card["display_name"] for card in card_row["cards"]] == ["Forest", "Swamp"]
    assert card_row["cards"][1]["card_status"]["confidence"] == "low"


def test_opponent_observation_review_groups_cards_linked_actions_and_review_labels(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        _insert_match(connection, "match:observations:1", completed_at="2026-05-30T03:30:00Z")
        _insert_game(connection, "match:observations:1", 1, completed_at="2026-05-30T03:10:00Z")
        _insert_game_result(connection, "match:observations:1", 1, local_result="loss", play_draw="draw")
        _insert_match_result(connection, "match:observations:1", match_result="L", match_win=0)
        _insert_match_context(connection, "match:observations:1", queue_name="Traditional Ranked")
        linked_action_id = _insert_gameplay_action(
            connection,
            "match:observations:1",
            1,
            timestamp="2026-05-30T03:03:00Z",
            action_type="cast",
            turn_number=3,
        )
        observation_id = _insert_opponent_observation(
            connection,
            "match:observations:1",
            1,
            gameplay_action_id=linked_action_id,
            timestamp="2026-05-30T03:04:00Z",
            turn_number=3,
            degradation_flags=["missing_expected_evidence"],
            review_required=1,
            drift_status="degraded",
        )
        _insert_opponent_observation_card(connection, observation_id, 1, grp_id=2001, card_name="Island")
        _insert_opponent_observation_card(
            connection,
            observation_id,
            2,
            grp_id=2002,
            card_name="Mountain",
            availability_status="expected_unavailable",
        )

        _insert_opponent_observation(
            connection,
            "match:observations:1",
            1,
            gameplay_action_id=None,
            timestamp="2026-05-30T03:02:00Z",
            turn_number=2,
            card_name="Visible Zero Card",
            review_required=0,
        )
        connection.commit()

    payload = _client(app_root).get("/api/analytics/opponent-card-observations").json()

    assert payload["status"] == "ok"
    assert payload["summary"] == {
        "row_count": 2,
        "card_row_count": 2,
        "degraded_row_count": 1,
        "unavailable_row_count": 1,
        "conflict_row_count": 0,
        "review_required_row_count": 1,
    }
    row = payload["rows"][0]
    assert row["opponent_card_observation_id"] == "match:observations:1:g1:observation:3"
    assert row["degradation_flags"] == ["missing_expected_evidence"]
    assert row["review_required"] is True
    assert row["linked_gameplay_action"] == {
        "gameplay_action_id": linked_action_id,
        "turn_number": 3,
        "action_type": "cast",
        "actor_relation": "opponent",
        "from_zone_type": "hand",
        "to_zone_type": "stack",
        "visible_in_log": True,
    }
    assert row["linked_gameplay_action_status"]["source_parser_surface"] == "synthetic_action_review_test"
    assert [card["card_ordinal"] for card in row["cards"]] == [1, 2]
    assert row["cards"][1]["card_status"]["availability_status"] == "expected_unavailable"

    zero_child_row = payload["rows"][1]
    assert zero_child_row["cards"] == []
    assert zero_child_row["linked_gameplay_action"] is None
    assert zero_child_row["linked_gameplay_action_status"] is None


def test_opponent_observation_review_hides_malformed_degradation_flag_values(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    raw_private_marker = "C:\\secret\\Player.log"
    with _current_database(app_root) as connection:
        _insert_match(connection, "match:observations:malformed", completed_at="2026-05-30T04:30:00Z")
        _insert_game(connection, "match:observations:malformed", 1, completed_at="2026-05-30T04:10:00Z")
        _insert_opponent_observation(
            connection,
            "match:observations:malformed",
            1,
            gameplay_action_id=None,
            timestamp="2026-05-30T04:05:00Z",
            turn_number=1,
            degradation_flags=raw_private_marker,
            review_required=0,
        )
        connection.commit()

    payload = _client(app_root).get("/api/analytics/opponent-card-observations").json()
    encoded = json.dumps(payload, sort_keys=True)

    assert payload["status"] == "ok"
    assert payload["warnings"] == ["opponent_observation_degradation_flags_malformed"]
    assert payload["rows"][0]["degradation_flags"] == []
    assert payload["summary"]["review_required_row_count"] == 0
    assert "Player.log" not in encoded
    assert "C:" not in encoded
    assert "secret" not in encoded


def test_opponent_observation_review_redacts_valid_degradation_flag_private_markers(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    raw_private_path_flag = "C:\\secret\\Player.log"
    raw_private_url_flag = "https://example.invalid/local-artifact"
    with _current_database(app_root) as connection:
        _insert_match(connection, "match:observations:redacted", completed_at="2026-05-30T04:50:00Z")
        _insert_game(connection, "match:observations:redacted", 1, completed_at="2026-05-30T04:40:00Z")
        _insert_opponent_observation(
            connection,
            "match:observations:redacted",
            1,
            gameplay_action_id=None,
            timestamp="2026-05-30T04:35:00Z",
            turn_number=1,
            degradation_flags=["missing_expected_evidence", raw_private_path_flag, raw_private_url_flag],
            review_required=0,
        )
        connection.commit()

    payload = _client(app_root).get("/api/analytics/opponent-card-observations").json()
    encoded = json.dumps(payload, sort_keys=True)

    assert payload["status"] == "ok"
    assert payload["warnings"] == []
    assert payload["rows"][0]["degradation_flags"] == [
        "missing_expected_evidence",
        "opponent_observation_degradation_flag_redacted",
    ]
    assert payload["summary"]["review_required_row_count"] == 1
    assert "Player.log" not in encoded
    assert "C:" not in encoded
    assert "secret" not in encoded
    assert "https://" not in encoded
    assert "local-artifact" not in encoded


def test_action_review_routes_degrade_unknown_schema_without_querying_rows(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    database_path = app_root / "db" / "mythic_edge.sqlite3"
    database_path.parent.mkdir(parents=True)
    connection = sqlite3.connect(database_path)
    try:
        connection.execute("CREATE TABLE gameplay_actions (gameplay_action_id TEXT PRIMARY KEY)")
        connection.commit()
    finally:
        connection.close()
    client = _client(app_root)

    payload = client.get("/api/analytics/gameplay-actions").json()

    assert payload["status"] == "degraded"
    assert payload["rows"] == []
    assert payload["summary"]["card_row_count"] == 0
    assert payload["summary"]["review_required_row_count"] == 0
    assert payload["warnings"] == ["analytics_schema_not_current"]
    assert payload["errors"] == []


def test_action_review_routes_return_safe_error_for_fixed_query_failure(tmp_path: Path) -> None:
    app_root = tmp_path / "app-data"
    with _current_database(app_root) as connection:
        _insert_match(connection, "match:actions:broken", completed_at="2026-05-30T05:30:00Z")
        _insert_game(connection, "match:actions:broken", 1, completed_at="2026-05-30T05:10:00Z")
        _insert_gameplay_action(connection, "match:actions:broken", 1, timestamp="2026-05-30T05:05:00Z")
        connection.execute("DROP TABLE gameplay_action_cards")
        connection.commit()
    client = _client(app_root)

    payload = client.get("/api/analytics/gameplay-actions").json()

    assert payload["status"] == "error"
    assert payload["errors"] == ["analytics_history_query_failed"]
    assert payload["summary"]["card_row_count"] == 0
    assert payload["summary"]["review_required_row_count"] == 0
    assert "SELECT" not in json.dumps(payload, sort_keys=True).upper()
    assert str(app_root) not in json.dumps(payload, sort_keys=True)


@pytest.mark.parametrize("endpoint", ["/api/analytics/gameplay-actions", "/api/analytics/opponent-card-observations"])
@pytest.mark.parametrize(
    "query",
    [
        "table=gameplay_actions",
        "limit=C:%5Csecret%5CPlayer.log",
        "offset=C:%5Csecret%5CPlayer.log",
        "limit=0",
        "limit=101",
        "offset=-1",
        "limit=5&limit=6",
    ],
)
def test_action_review_routes_reject_malformed_query_params_without_echo(
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
    assert "gameplay_actions" not in encoded
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
            "ingest:action-review:test",
            "sanitized_golden_replay",
            "analytics_action_review_views_v1",
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
        "ingest_run_id": "ingest:action-review:test",
        "source_parser_surface": "synthetic_action_review_test",
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


def _insert_gameplay_action(
    connection: sqlite3.Connection,
    match_id: str,
    game_number: int,
    *,
    timestamp: str,
    action_type: str = "cast",
    turn_number: int | None = 1,
    **core_overrides: object,
) -> str:
    game_id = f"{match_id}:g{game_number}"
    action_id = f"{game_id}:action:{action_type}"
    _insert_with_core(
        connection,
        "gameplay_actions",
        {
            "gameplay_action_id": action_id,
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "timestamp": timestamp,
            "game_state_id": 123,
            "turn_number": turn_number,
            "action_type": action_type,
            "actor_relation": "opponent",
            "from_zone_type": "hand",
            "to_zone_type": "stack",
            "source_status": "observed",
            "annotation_context_label": "gameplay_action",
            "raw_action_type_labels": "cast",
            "annotation_type_labels": "spell",
            "visible_in_log": 1,
        },
        source_fact_key=f"gameplay_action_{action_type}",
        **core_overrides,
    )
    return action_id


def _insert_gameplay_action_card(
    connection: sqlite3.Connection,
    gameplay_action_id: str,
    card_ordinal: int,
    *,
    grp_id: int,
    card_name: str,
    **core_overrides: object,
) -> None:
    game_id = gameplay_action_id.split(":action:", maxsplit=1)[0]
    _insert_with_core(
        connection,
        "gameplay_action_cards",
        {
            "gameplay_action_card_id": f"{gameplay_action_id}:card{card_ordinal}",
            "gameplay_action_id": gameplay_action_id,
            "game_id": game_id,
            "card_ordinal": card_ordinal,
            "instance_id": 10000 + card_ordinal,
            "grp_id": grp_id,
            "observed_grp_id": grp_id,
            "overlay_grp_id": None,
            "object_source_grp_id": grp_id,
            "identity_hint_source": "direct_grp_id",
            "card_name": card_name,
            "display_name": card_name,
            "name_resolution_status": "resolved",
            "enrichment_status": "not_needed",
        },
        source_fact_key=f"gameplay_action_card_{card_ordinal}",
        **core_overrides,
    )


def _insert_opponent_observation(
    connection: sqlite3.Connection,
    match_id: str,
    game_number: int,
    *,
    gameplay_action_id: str | None,
    timestamp: str,
    turn_number: int,
    card_name: str = "Visible Opponent Card",
    degradation_flags: object = None,
    review_required: int = 0,
    **core_overrides: object,
) -> str:
    game_id = f"{match_id}:g{game_number}"
    observation_id = f"{game_id}:observation:{turn_number}"
    if isinstance(degradation_flags, list):
        stored_degradation_flags = json.dumps(degradation_flags)
    else:
        stored_degradation_flags = degradation_flags
    _insert_with_core(
        connection,
        "opponent_card_observations",
        {
            "opponent_card_observation_id": observation_id,
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "gameplay_action_id": gameplay_action_id,
            "timestamp": timestamp,
            "game_state_id": 456,
            "turn_number": turn_number,
            "actor_relation": "opponent",
            "actor_seat_id": 2,
            "local_seat_id": 1,
            "instance_id": 22000 + turn_number,
            "grp_id": 3000 + turn_number,
            "observed_grp_id": 3000 + turn_number,
            "overlay_grp_id": None,
            "object_source_grp_id": 3000 + turn_number,
            "parent_id": None,
            "identity_hint_source": "visible_object",
            "card_name": card_name,
            "display_name": card_name,
            "resolution_status": "resolved",
            "name_resolution_source": "local_catalog",
            "action_type": "cast",
            "cast_mode": "normal",
            "source_evidence": "gameplay_action",
            "evidence_status": "visible",
            "visibility": "public",
            "from_zone_type": "hand",
            "to_zone_type": "stack",
            "degradation_flags": stored_degradation_flags,
            "review_required": review_required,
        },
        source_parser_surface="opponent_card_observations.py",
        source_fact_key=f"opponent_observation_{turn_number}",
        **core_overrides,
    )
    return observation_id


def _insert_opponent_observation_card(
    connection: sqlite3.Connection,
    opponent_card_observation_id: str,
    card_ordinal: int,
    *,
    grp_id: int,
    card_name: str,
    **core_overrides: object,
) -> None:
    game_id = opponent_card_observation_id.split(":observation:", maxsplit=1)[0]
    _insert_with_core(
        connection,
        "opponent_card_observation_cards",
        {
            "opponent_card_observation_card_id": f"{opponent_card_observation_id}:card{card_ordinal}",
            "opponent_card_observation_id": opponent_card_observation_id,
            "game_id": game_id,
            "card_ordinal": card_ordinal,
            "grp_id": grp_id,
            "observed_grp_id": grp_id,
            "overlay_grp_id": None,
            "object_source_grp_id": grp_id,
            "identity_hint_source": "visible_object",
            "card_name": card_name,
            "resolution_status": "resolved",
            "visibility": "public",
        },
        source_parser_surface="opponent_card_observations.py",
        source_fact_key=f"opponent_observation_card_{card_ordinal}",
        **core_overrides,
    )
