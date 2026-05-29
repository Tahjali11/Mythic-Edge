from __future__ import annotations

import sqlite3

import pytest

from mythic_edge_parser.app.analytics_migration_loader import (
    ANALYTICS_SCHEMA_VERSION,
    apply_analytics_migrations,
)

REQUIRED_DERIVED_VIEWS = {
    "v_opening_hand_cards",
    "v_opening_lines",
    "v_gameplay_action_review",
    "v_mulligan_outcomes",
    "v_game1_vs_postboard",
    "v_play_draw_splits",
    "v_sample_size_warnings",
    "v_matchup_label_performance",
    "v_opponent_card_observation_review",
}


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    apply_analytics_migrations(connection, applied_at="test-applied")
    _insert_seed_run(connection)
    return connection


def _names(connection: sqlite3.Connection, object_type: str) -> set[str]:
    rows = connection.execute("SELECT name FROM sqlite_schema WHERE type = ?", (object_type,)).fetchall()
    return {str(row["name"]) for row in rows if not str(row["name"]).startswith("sqlite_")}


def _core(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "value_source": "observed",
        "confidence": "high",
        "finality": "final",
        "drift_status": "none",
        "parser_schema_version": ANALYTICS_SCHEMA_VERSION,
        "ingest_run_id": "ingest:test",
        "source_parser_surface": "synthetic_analytics_view_test",
        "source_fact_key": "synthetic_fact",
        "availability_status": "available",
        "created_at": "2026-05-29T00:00:00Z",
        "updated_at": "2026-05-29T00:00:00Z",
    }
    values.update(overrides)
    return values


def _insert_seed_run(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        INSERT INTO ingest_runs (
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
            "ingest:test",
            "sanitized_golden_replay",
            "analytics_derived_views_v1",
            "2026-05-29T00:00:00Z",
            "2026-05-29T00:00:01Z",
            "completed",
            "test",
            "test",
            ANALYTICS_SCHEMA_VERSION,
            "{}",
            "2026-05-29T00:00:00Z",
            "2026-05-29T00:00:00Z",
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


def _insert_match(connection: sqlite3.Connection, match_id: str, **core_overrides: object) -> None:
    _insert_with_core(
        connection,
        "matches",
        {
            "match_id": match_id,
            "session_id": None,
            "parser_match_key": match_id,
            "match_started_at": "2026-05-29T00:00:00Z",
            "match_completed_at": "2026-05-29T00:30:00Z",
        },
        **core_overrides,
    )


def _insert_game(
    connection: sqlite3.Connection,
    match_id: str,
    game_number: int,
    **core_overrides: object,
) -> str:
    game_id = f"{match_id}:g{game_number}"
    _insert_with_core(
        connection,
        "games",
        {
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "game_started_at": "2026-05-29T00:00:00Z",
            "game_completed_at": "2026-05-29T00:10:00Z",
        },
        **core_overrides,
    )
    return game_id


def _insert_match_and_game(
    connection: sqlite3.Connection,
    match_id: str,
    game_number: int = 1,
    **core_overrides: object,
) -> str:
    _insert_match(connection, match_id, **core_overrides)
    return _insert_game(connection, match_id, game_number, **core_overrides)


def _insert_game_result(
    connection: sqlite3.Connection,
    match_id: str,
    game_number: int,
    *,
    local_result: str | None,
    play_draw: str | None,
    pre_postboard_label: str | None = "preboard",
    turn_count: int | None = 5,
    game_duration_seconds: float | None = 900.0,
    **core_overrides: object,
) -> str:
    game_id = f"{match_id}:g{game_number}"
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
            "game_started_at": "2026-05-29T00:00:00Z",
            "game_completed_at": "2026-05-29T00:10:00Z",
            "game_duration_seconds": game_duration_seconds,
        },
        **core_overrides,
    )
    return game_id


def _insert_game_with_result(
    connection: sqlite3.Connection,
    match_id: str,
    game_number: int,
    **result_values: object,
) -> str:
    game_id = _insert_match_and_game(connection, match_id, game_number)
    _insert_game_result(connection, match_id, game_number, **result_values)
    return game_id


def _insert_action(
    connection: sqlite3.Connection,
    game_id: str,
    match_id: str,
    game_number: int,
    action_id: str,
    *,
    turn_number: int | None,
    action_type: str = "spell_cast",
    actor_relation: str = "opponent",
    **core_overrides: object,
) -> None:
    _insert_with_core(
        connection,
        "gameplay_actions",
        {
            "gameplay_action_id": action_id,
            "game_id": game_id,
            "match_id": match_id,
            "game_number": game_number,
            "timestamp": "2026-05-29T00:03:00Z",
            "game_state_id": 42,
            "turn_number": turn_number,
            "action_type": action_type,
            "actor_relation": actor_relation,
            "from_zone_type": "ZoneType_Hand",
            "to_zone_type": "ZoneType_Stack",
            "source_status": "parser_normalized",
            "annotation_context_label": "CastSpell",
            "raw_action_type_labels": '["ActionType_Cast"]',
            "annotation_type_labels": '["AnnotationType_ObjectIdChanged"]',
            "visible_in_log": 1,
        },
        **core_overrides,
    )


def _insert_action_card(
    connection: sqlite3.Connection,
    action_id: str,
    game_id: str,
    card_id: str,
    *,
    card_ordinal: int = 1,
    grp_id: int | None = 1001,
) -> None:
    _insert_with_core(
        connection,
        "gameplay_action_cards",
        {
            "gameplay_action_card_id": card_id,
            "gameplay_action_id": action_id,
            "game_id": game_id,
            "card_ordinal": card_ordinal,
            "instance_id": 5001,
            "grp_id": grp_id,
            "observed_grp_id": grp_id,
            "overlay_grp_id": grp_id,
            "object_source_grp_id": grp_id,
            "identity_hint_source": "direct_grp_id",
            "card_name": "Visible Spell",
            "display_name": "Visible Spell",
            "name_resolution_status": "resolved",
            "enrichment_status": "parser_rendered",
        },
    )


def test_all_approved_views_exist_after_migration() -> None:
    connection = _connect()

    assert REQUIRED_DERIVED_VIEWS <= _names(connection, "view")


def test_opening_hand_card_view_preserves_row_identity_and_provenance() -> None:
    connection = _connect()
    match_id = "match:views:opening"
    game_id = _insert_match_and_game(connection, match_id)
    opening_hand_id = f"{game_id}:opening_hand"
    _insert_with_core(
        connection,
        "opening_hands",
        {
            "opening_hand_id": opening_hand_id,
            "game_id": game_id,
            "match_id": match_id,
            "game_number": 1,
            "hand_size": 7,
            "exact_card_count": 2,
        },
        source_fact_key="opening_hand",
    )
    for position, card_name in ((1, "Forest"), (2, "Swamp")):
        _insert_with_core(
            connection,
            "opening_hand_cards",
            {
                "opening_hand_card_id": f"{opening_hand_id}:slot{position}",
                "opening_hand_id": opening_hand_id,
                "game_id": game_id,
                "card_position": position,
                "grp_id": None,
                "card_name": card_name,
                "identity_hint_source": "name_only",
                "name_resolution_status": "name_unresolved",
            },
            source_fact_key=f"opening_hand_card_{position}",
        )

    rows = connection.execute(
        "SELECT * FROM v_opening_hand_cards ORDER BY card_position",
    ).fetchall()

    assert [row["opening_hand_card_id"] for row in rows] == [
        f"{opening_hand_id}:slot1",
        f"{opening_hand_id}:slot2",
    ]
    assert [row["card_name"] for row in rows] == ["Forest", "Swamp"]
    assert {row["hand_size"] for row in rows} == {7}
    assert {row["exact_card_count"] for row in rows} == {2}
    assert {row["finality"] for row in rows} == {"final"}
    assert {row["drift_status"] for row in rows} == {"none"}
    assert {row["source_parser_surface"] for row in rows} == {"synthetic_analytics_view_test"}


def test_opening_lines_filter_known_first_three_turns_without_widening_review_view() -> None:
    connection = _connect()
    match_id = "match:views:actions"
    game_id = _insert_match_and_game(connection, match_id)
    _insert_action(connection, game_id, match_id, 1, "action:t2", turn_number=2)
    _insert_action(connection, game_id, match_id, 1, "action:t4", turn_number=4, action_type="attack")
    _insert_action(connection, game_id, match_id, 1, "action:unknown", turn_number=None, actor_relation="unknown")
    _insert_action_card(connection, "action:t2", game_id, "action:t2:card1", grp_id=2002)

    opening_rows = connection.execute(
        "SELECT * FROM v_opening_lines ORDER BY gameplay_action_id",
    ).fetchall()
    review_rows = connection.execute(
        "SELECT * FROM v_gameplay_action_review ORDER BY gameplay_action_id",
    ).fetchall()

    assert [row["gameplay_action_id"] for row in opening_rows] == ["action:t2"]
    assert opening_rows[0]["turn_number"] == 2
    assert opening_rows[0]["card_count"] == 1
    assert opening_rows[0]["grp_ids"] == "2002"
    assert [row["gameplay_action_id"] for row in review_rows] == [
        "action:t2",
        "action:t4",
        "action:unknown",
    ]


def test_mulligan_and_game_review_views_preserve_unknown_and_postboard_context() -> None:
    connection = _connect()
    match_id = "match:views:mulligans"
    game_id = _insert_match_and_game(connection, match_id)
    _insert_game_result(
        connection,
        match_id,
        1,
        local_result="loss",
        play_draw="draw",
        pre_postboard_label="postboard",
        turn_count=8,
        game_duration_seconds=1234.0,
    )
    _insert_with_core(
        connection,
        "mulligan_events",
        {
            "mulligan_event_id": f"{game_id}:mulligan:0",
            "game_id": game_id,
            "match_id": match_id,
            "game_number": 1,
            "ordinal_or_count": "0",
            "mulligan_count": 0,
            "decision_detail": "kept_initial_hand",
        },
        availability_status="not_observed",
        source_fact_key="mulligan_zero",
    )
    _insert_with_core(
        connection,
        "mulligan_events",
        {
            "mulligan_event_id": f"{game_id}:mulligan:unknown",
            "game_id": game_id,
            "match_id": match_id,
            "game_number": 1,
            "ordinal_or_count": "unknown",
            "mulligan_count": None,
            "decision_detail": "mulligan_detail_unavailable",
        },
        availability_status="expected_unavailable",
        source_fact_key="mulligan_unknown",
    )

    mulligan_rows = connection.execute(
        "SELECT * FROM v_mulligan_outcomes ORDER BY ordinal_or_count",
    ).fetchall()
    game_row = connection.execute("SELECT * FROM v_game1_vs_postboard").fetchone()

    assert [row["mulligan_count"] for row in mulligan_rows] == [0, None]
    assert [row["availability_status"] for row in mulligan_rows] == [
        "not_observed",
        "expected_unavailable",
    ]
    assert {row["local_result"] for row in mulligan_rows} == {"loss"}
    assert game_row["pre_postboard_label"] == "postboard"
    assert game_row["game_duration_seconds"] == 1234.0
    assert game_row["source_parser_surface"] == "synthetic_analytics_view_test"


def test_play_draw_splits_and_sample_warnings_do_not_treat_unknowns_as_losses() -> None:
    connection = _connect()
    result_specs = [
        ("match:views:play:win", "win", "play", {}),
        ("match:views:play:loss", "loss", "play", {}),
        ("match:views:play:unknown", None, "play", {"availability_status": "not_observed"}),
        ("match:views:play:nonstandard", "drawn", "play", {}),
        ("match:views:play:degraded-loss", "loss", "play", {"drift_status": "degraded"}),
    ]
    for match_id, local_result, play_draw, core_overrides in result_specs:
        _insert_game_with_result(
            connection,
            match_id,
            1,
            local_result=local_result,
            play_draw=play_draw,
            **core_overrides,
        )
    for index in range(10):
        _insert_game_with_result(
            connection,
            f"match:views:draw:{index}",
            1,
            local_result="win",
            play_draw="draw",
        )

    play = connection.execute("SELECT * FROM v_play_draw_splits WHERE play_draw = 'play'").fetchone()
    draw_warning = connection.execute(
        "SELECT sample_size_warning FROM v_sample_size_warnings WHERE play_draw = 'draw'",
    ).fetchone()
    play_warning = connection.execute(
        "SELECT sample_size_warning FROM v_sample_size_warnings WHERE play_draw = 'play'",
    ).fetchone()

    assert play["game_count"] == 5
    assert play["known_result_count"] == 3
    assert play["wins"] == 1
    assert play["losses"] == 2
    assert play["unknown_result_count"] == 2
    assert play["unavailable_result_count"] == 1
    assert play["degraded_result_count"] == 1
    assert play["win_rate"] == pytest.approx(1 / 3)
    assert play_warning["sample_size_warning"] == "small_sample"
    assert draw_warning["sample_size_warning"] == "ok"


def test_matchup_label_performance_uses_current_human_labels_and_preserves_unknown_results() -> None:
    connection = _connect()
    for match_id, match_win in (
        ("match:views:label:win", 1),
        ("match:views:label:unknown", None),
        ("match:views:label:historical", 0),
    ):
        _insert_match(connection, match_id)
        _insert_with_core(
            connection,
            "match_results",
            {
                "match_result_id": f"{match_id}:match_result",
                "match_id": match_id,
                "match_result": "W" if match_win == 1 else None,
                "winner_team_id": None,
                "games_won": None,
                "games_lost": None,
                "total_games": None,
                "match_win": match_win,
                "game_win_rate": None,
            },
        )

    annotation_core = _core(
        value_source="human_annotation",
        confidence="human",
        finality="annotation_current",
        source_parser_surface="human_annotation",
        source_fact_key="human_matchup_label",
    )
    labels = [
        ("label:win", "match:views:label:win", 1),
        ("label:unknown", "match:views:label:unknown", 1),
        ("label:historical", "match:views:label:historical", 0),
    ]
    for label_id, match_id, is_current in labels:
        values = {
            "matchup_label_id": label_id,
            "match_id": match_id,
            "label_value": "mirror",
            "label_source": "manual",
            "author_label": "local",
            "valid_from": "2026-05-29T00:00:00Z",
            "valid_to": None,
            "is_current": is_current,
            **annotation_core,
        }
        columns = ", ".join(values)
        placeholders = ", ".join("?" for _ in values)
        connection.execute(
            f"INSERT INTO matchup_labels ({columns}) VALUES ({placeholders})",
            tuple(values.values()),
        )

    row = connection.execute("SELECT * FROM v_matchup_label_performance").fetchone()

    assert row["matchup_label"] == "mirror"
    assert row["match_count"] == 2
    assert row["known_match_result_count"] == 1
    assert row["match_wins"] == 1
    assert row["match_losses"] == 0
    assert row["unknown_match_result_count"] == 1
    assert row["match_win_rate"] == pytest.approx(1.0)


def test_matchup_label_performance_counts_current_label_without_match_result_row() -> None:
    connection = _connect()
    match_id = "match:views:label:missing-result"
    _insert_match(connection, match_id)
    annotation_core = _core(
        value_source="human_annotation",
        confidence="human",
        finality="annotation_current",
        source_parser_surface="human_annotation",
        source_fact_key="human_matchup_label",
    )
    values = {
        "matchup_label_id": "label:missing-result",
        "match_id": match_id,
        "label_value": "missing_result_label",
        "label_source": "manual",
        "author_label": "local",
        "valid_from": "2026-05-29T00:00:00Z",
        "valid_to": None,
        "is_current": 1,
        **annotation_core,
    }
    columns = ", ".join(values)
    placeholders = ", ".join("?" for _ in values)
    connection.execute(
        f"INSERT INTO matchup_labels ({columns}) VALUES ({placeholders})",
        tuple(values.values()),
    )

    row = connection.execute("SELECT * FROM v_matchup_label_performance").fetchone()

    assert row["matchup_label"] == "missing_result_label"
    assert row["match_count"] == 1
    assert row["known_match_result_count"] == 0
    assert row["match_wins"] == 0
    assert row["match_losses"] == 0
    assert row["unknown_match_result_count"] == 1
    assert row["match_win_rate"] is None


def test_opponent_observation_review_preserves_child_card_and_degradation_context() -> None:
    connection = _connect()
    match_id = "match:views:opponent"
    game_id = _insert_match_and_game(connection, match_id)
    _insert_action(connection, game_id, match_id, 1, "action:opponent", turn_number=3)
    _insert_with_core(
        connection,
        "opponent_card_observations",
        {
            "opponent_card_observation_id": "observation:1",
            "game_id": game_id,
            "match_id": match_id,
            "game_number": 1,
            "gameplay_action_id": "action:opponent",
            "timestamp": "2026-05-29T00:03:00Z",
            "game_state_id": 42,
            "turn_number": 3,
            "actor_relation": "opponent",
            "actor_seat_id": 2,
            "local_seat_id": 1,
            "instance_id": 1001,
            "grp_id": 2002,
            "observed_grp_id": 2002,
            "overlay_grp_id": 2002,
            "object_source_grp_id": 2002,
            "parent_id": 1000,
            "identity_hint_source": "direct_grp_id",
            "card_name": "Visible Spell",
            "display_name": "Visible Spell",
            "resolution_status": "resolved",
            "name_resolution_source": "grp_id_catalog",
            "action_type": "spell_cast",
            "cast_mode": "main_face",
            "source_evidence": "action_array",
            "evidence_status": "degraded",
            "visibility": "action_visible",
            "from_zone_type": "ZoneType_Hand",
            "to_zone_type": "ZoneType_Stack",
            "degradation_flags": '["ambiguous_zone_transition"]',
            "review_required": 1,
        },
        confidence="low",
        drift_status="degraded",
        source_parser_surface="opponent_card_observations.py",
        source_fact_key="opponent_card_observation",
    )
    _insert_with_core(
        connection,
        "opponent_card_observation_cards",
        {
            "opponent_card_observation_card_id": "observation:1:card1",
            "opponent_card_observation_id": "observation:1",
            "game_id": game_id,
            "card_ordinal": 1,
            "grp_id": 2002,
            "observed_grp_id": 2002,
            "overlay_grp_id": 2002,
            "object_source_grp_id": 2002,
            "identity_hint_source": "direct_grp_id",
            "card_name": "Visible Spell",
            "resolution_status": "resolved",
            "visibility": "action_visible",
        },
    )

    row = connection.execute("SELECT * FROM v_opponent_card_observation_review").fetchone()

    assert row["opponent_card_observation_id"] == "observation:1"
    assert row["gameplay_action_id"] == "action:opponent"
    assert row["actor_relation"] == "opponent"
    assert row["evidence_status"] == "degraded"
    assert row["degradation_flags"] == '["ambiguous_zone_transition"]'
    assert row["review_required"] == 1
    assert row["opponent_card_observation_card_id"] == "observation:1:card1"
    assert row["card_grp_id"] == 2002
    assert row["confidence"] == "low"
    assert row["drift_status"] == "degraded"
    assert row["source_parser_surface"] == "opponent_card_observations.py"
