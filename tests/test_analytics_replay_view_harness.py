from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from mythic_edge_parser.app import evidence_ledger
from mythic_edge_parser.app.analytics_ingest import ingest_parser_normalized_replay
from mythic_edge_parser.app.opponent_card_observations import (
    OPPONENT_CARD_OBSERVATION_OBJECT,
)
from mythic_edge_parser.app.opponent_card_observations import (
    SCHEMA_VERSION as OPPONENT_CARD_OBSERVATION_SCHEMA_VERSION,
)

MATCH_ID = "match:analytics:harness"


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    return connection


def _representative_replay() -> dict[str, object]:
    return {
        "source_kind": "sanitized_golden_replay",
        "source_artifact_label": "analytics_replay_view_harness_v1",
        "parser_commit": "test-parser-commit",
        "parser_version": "test-parser-version",
        "generated_at": "2026-05-29T14:00:00+00:00",
        "match_log_rows": [
            {
                "event_family": "MatchLogRow",
                "event_type": "match_log_row",
                "scope": "Match",
                "match_id": MATCH_ID,
                "timestamp": "2026-05-29T14:30:00+00:00",
                "MTGA Match ID": MATCH_ID,
                "Match Win?": "W",
                "Match Win Flag": 1,
                "Games Won": 1,
                "Games Lost": 1,
                "Total Games": 2,
                "Game Win %": 0.5,
                "MTGA Format": "Constructed",
                "MTGA Event ID": "AnalyticsHarness_Event",
                "MTGA Queue Type": "Best of 3",
                "MTGA Rank Raw": "Synthetic_Tier1",
                "My Rank": "Synthetic",
                "MGTA Start Time": "2026-05-29T14:00:00+00:00",
                "MTGA End Time": "2026-05-29T14:30:00+00:00",
                "MTGA Sync Status": "Final",
            },
        ],
        "game_log_rows": [
            {
                "event_family": "GameLogRow",
                "event_type": "game_log_row",
                "scope": "Game",
                "match_id": MATCH_ID,
                "timestamp": "2026-05-29T14:12:00+00:00",
                "MTGA Match ID": MATCH_ID,
                "Game Number": 1,
                "Pre / Postboard": "Preboard",
                "Play / Draw": "Play",
                "Mulligans": 1,
                "Opening Hand Size": 7,
                "Opening Hand": "Forest; Island; Harness Scout",
                "Mulliganed Away": "Practice Card",
                "Game Result": "W",
                "Turn Count": 6,
                "Game Duration": 720,
                "MTGA Format": "Constructed",
                "MTGA Event ID": "AnalyticsHarness_Event",
                "MTGA Queue Type": "Best of 3",
            },
            {
                "event_family": "GameLogRow",
                "event_type": "game_log_row",
                "scope": "Game",
                "match_id": MATCH_ID,
                "timestamp": "2026-05-29T14:29:00+00:00",
                "MTGA Match ID": MATCH_ID,
                "Game Number": 2,
                "Pre / Postboard": "Postboard",
                "Play / Draw": "Draw",
                "Mulligans": 0,
                "Opening Hand Size": 7,
                "Opening Hand": "Mountain; Plains; Harness Mage",
                "Mulliganed Away": "",
                "Game Result": "L",
                "Turn Count": 10,
                "Game Duration": 1020,
                "MTGA Format": "Constructed",
                "MTGA Event ID": "AnalyticsHarness_Event",
                "MTGA Queue Type": "Best of 3",
            },
        ],
        "gameplay_action_entries": [
            _action_entry(
                timestamp="2026-05-29T14:03:00+00:00",
                game_number=1,
                game_state_id=101,
                turn_number=2,
                instance_id=5001,
                grp_id=7001,
                observed_grp_id=7001,
                overlay_grp_id=7001,
                object_source_grp_id=7001,
                parent_id=4001,
                card_name="Harness Visible Spell",
                display_name="Harness Visible Spell",
            ),
            _action_entry(
                timestamp="2026-05-29T14:20:00+00:00",
                game_number=2,
                game_state_id=202,
                turn_number=5,
                action_type="activated_ability",
                instance_id=5002,
                grp_id=7002,
                observed_grp_id=7002,
                overlay_grp_id=7002,
                object_source_grp_id=7002,
                parent_id=4002,
                card_name="Harness Later Spell",
                display_name="Harness Later Spell",
            ),
        ],
        "opponent_card_observations": [
            _opponent_observation(
                timestamp="2026-05-29T14:03:00+00:00",
                game_number=1,
                game_state_id=101,
                turn_number=2,
                instance_id=5001,
                grp_id=7001,
                observed_grp_id=7001,
                overlay_grp_id=7001,
                object_source_grp_id=7001,
                parent_id=4001,
                card_name="Harness Visible Spell",
                display_name="Harness Visible Spell",
            ),
        ],
        "field_evidence_entries": [
            {
                "object": evidence_ledger.FIELD_EVIDENCE_OBJECT,
                "schema_version": evidence_ledger.FIELD_EVIDENCE_SCHEMA_VERSION,
                "ledger_version": evidence_ledger.LEDGER_VERSION,
                "entry_id": "tier1.match_identity.match_id",
                "output_family": "match_identity_and_lifecycle",
                "output_field": "match_id",
                "value_source": "conflict",
                "confidence": "low",
                "finality": "final",
                "source_event_kind": "MatchState",
                "source_event_type": "match_started",
                "source_payload_paths": ["/match_log_rows/0/match_id"],
                "source_event_timestamp": "2026-05-29T14:00:00+00:00",
                "drift_flags": ["conflicting_evidence"],
                "invariant_status": "failed",
                "degraded_reason": "conflicting evidence",
                "review_required": True,
                "fact_table": "matches",
                "fact_id": MATCH_ID,
                "fact_field": "match_id",
                "source_parser_surface": "MatchSummary.to_match_log_row",
                "source_fact_key": "match_id",
            },
        ],
    }


def _action_entry(**overrides: object) -> dict[str, object]:
    entry: dict[str, object] = {
        "timestamp": "2026-05-29T14:03:00+00:00",
        "match_id": MATCH_ID,
        "game_number": 1,
        "game_state_id": 101,
        "turn_number": 2,
        "action_type": "spell_cast",
        "cast_mode": "main_face",
        "instance_id": 5001,
        "grp_id": 7001,
        "observed_grp_id": 7001,
        "overlay_grp_id": 7001,
        "object_source_grp_id": 7001,
        "parent_id": 4001,
        "identity_hint_source": "direct_grp_id",
        "actor_relation": "opponent",
        "from_zone_type": "ZoneType_Hand",
        "to_zone_type": "ZoneType_Stack",
        "raw_action_types": ["ActionType_Cast"],
        "annotation_types": ["AnnotationType_ObjectIdChanged"],
        "annotation_categories": ["CastSpell"],
        "visible_in_log": True,
        "card_name": "Harness Visible Spell",
        "display_name": "Harness Visible Spell",
        "resolution_status": "resolved",
    }
    entry.update(overrides)
    return entry


def _opponent_observation(**overrides: object) -> dict[str, object]:
    observation = {
        **_action_entry(),
        "object": OPPONENT_CARD_OBSERVATION_OBJECT,
        "schema_version": OPPONENT_CARD_OBSERVATION_SCHEMA_VERSION,
        "actor_seat_id": 2,
        "local_seat_id": 1,
        "name_resolution_source": "grp_id_catalog",
        "source_evidence": "action_array",
        "evidence_status": "degraded",
        "value_source": "observed",
        "confidence": "low",
        "visibility": "action_visible",
        "degradation_flags": ["ambiguous_zone_transition"],
        "review_required": True,
    }
    observation.update(overrides)
    return observation


def _count(connection: sqlite3.Connection, table_name: str) -> int:
    return int(connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0])


def _rows(connection: sqlite3.Connection, query: str) -> list[dict[str, object]]:
    return [dict(row) for row in connection.execute(query).fetchall()]


def _sqlite_artifacts() -> set[str]:
    root = Path("data/analytics")
    if not root.exists():
        return set()
    patterns = ("*.db", "*.sqlite", "*.sqlite3", "*.db-journal", "*.db-wal", "*.db-shm")
    found: set[str] = set()
    for pattern in patterns:
        found.update(str(path) for path in root.glob(pattern))
    return found


def test_representative_replay_ingests_and_surfaces_required_view_rows() -> None:
    before_artifacts = _sqlite_artifacts()
    connection = _connect()

    result = ingest_parser_normalized_replay(
        connection,
        _representative_replay(),
        started_at="2026-05-29T14:00:00+00:00",
        finished_at="2026-05-29T14:31:00+00:00",
    )

    assert result.warnings == []
    assert result.skipped == {}
    assert result.source_kind == "sanitized_golden_replay"
    assert result.source_artifact_label == "analytics_replay_view_harness_v1"
    assert result.row_counts["games"] == 2
    assert result.row_counts["gameplay_actions"] == 2
    assert result.row_counts["opponent_card_observations"] == 1

    opening_rows = _rows(
        connection,
        """
        SELECT *
        FROM v_opening_hand_cards
        ORDER BY game_number, card_position
        """,
    )
    assert len(opening_rows) == 6
    assert opening_rows[0]["match_id"] == MATCH_ID
    assert opening_rows[0]["game_id"] == f"{MATCH_ID}:g1"
    assert opening_rows[0]["opening_hand_id"] == f"{MATCH_ID}:g1:opening_hand"
    assert opening_rows[0]["opening_hand_card_id"] == f"{MATCH_ID}:g1:opening_hand:slot1"
    assert opening_rows[0]["card_position"] == 1
    assert opening_rows[0]["card_name"] == "Forest"
    assert opening_rows[0]["hand_size"] == 7
    assert opening_rows[0]["source_parser_surface"] == "GameSummary.to_game_log_row"
    assert opening_rows[0]["finality"] == "final"
    assert opening_rows[0]["drift_status"] == "not_checked"
    assert opening_rows[0]["ingest_run_id"] == result.ingest_run_id
    assert opening_rows[0]["availability_status"] == "available"

    mulligan_rows = _rows(
        connection,
        """
        SELECT *
        FROM v_mulligan_outcomes
        ORDER BY game_number
        """,
    )
    assert [(row["game_number"], row["mulligan_count"]) for row in mulligan_rows] == [(1, 1), (2, 0)]
    assert [row["availability_status"] for row in mulligan_rows] == ["available", "not_observed"]
    assert [row["local_result"] for row in mulligan_rows] == ["win", "loss"]

    opening_line_rows = _rows(
        connection,
        """
        SELECT *
        FROM v_opening_lines
        ORDER BY turn_number
        """,
    )
    review_action_rows = _rows(
        connection,
        """
        SELECT *
        FROM v_gameplay_action_review
        ORDER BY game_number, turn_number
        """,
    )
    assert len(opening_line_rows) == 1
    assert opening_line_rows[0]["turn_number"] == 2
    assert opening_line_rows[0]["card_count"] == 1
    assert opening_line_rows[0]["grp_ids"] == "7001"
    assert opening_line_rows[0]["source_parser_surface"] == "gameplay_actions.py"
    assert [row["turn_number"] for row in review_action_rows] == [2, 5]
    assert review_action_rows[1]["gameplay_action_id"] not in {
        row["gameplay_action_id"] for row in opening_line_rows
    }

    game_rows = _rows(
        connection,
        """
        SELECT *
        FROM v_game1_vs_postboard
        ORDER BY game_number
        """,
    )
    assert [(row["pre_postboard_label"], row["play_draw"], row["local_result"]) for row in game_rows] == [
        ("preboard", "play", "win"),
        ("postboard", "draw", "loss"),
    ]
    assert [row["turn_count"] for row in game_rows] == [6, 10]
    assert [row["game_duration_seconds"] for row in game_rows] == [720.0, 1020.0]

    split_rows = {
        row["play_draw"]: row
        for row in _rows(
            connection,
            """
            SELECT *
            FROM v_play_draw_splits
            ORDER BY play_draw
            """,
        )
    }
    assert split_rows["play"]["wins"] == 1
    assert split_rows["play"]["losses"] == 0
    assert split_rows["play"]["win_rate"] == pytest.approx(1.0)
    assert split_rows["draw"]["wins"] == 0
    assert split_rows["draw"]["losses"] == 1
    assert split_rows["draw"]["win_rate"] == pytest.approx(0.0)
    assert split_rows["draw"]["unknown_result_count"] == 0

    warning_rows = {
        row["play_draw"]: row["sample_size_warning"]
        for row in _rows(
            connection,
            """
            SELECT *
            FROM v_sample_size_warnings
            ORDER BY play_draw
            """,
        )
    }
    assert warning_rows == {"draw": "small_sample", "play": "small_sample"}

    observation_rows = _rows(connection, "SELECT * FROM v_opponent_card_observation_review")
    assert len(observation_rows) == 1
    observation = observation_rows[0]
    assert observation["match_id"] == MATCH_ID
    assert observation["game_id"] == f"{MATCH_ID}:g1"
    assert observation["gameplay_action_id"] == opening_line_rows[0]["gameplay_action_id"]
    assert observation["actor_relation"] == "opponent"
    assert observation["evidence_status"] == "degraded"
    assert observation["confidence"] == "low"
    assert observation["drift_status"] == "degraded"
    assert observation["review_required"] == 1
    assert json.loads(str(observation["degradation_flags"])) == ["ambiguous_zone_transition"]
    assert observation["card_grp_id"] == 7001
    assert observation["source_parser_surface"] == "opponent_card_observations.py"

    target_fact = connection.execute("SELECT match_id FROM matches WHERE match_id = ?", (MATCH_ID,)).fetchone()
    assert target_fact["match_id"] == MATCH_ID
    field_evidence = _rows(
        connection,
        """
        SELECT *
        FROM fact_provenance
        WHERE fact_provenance_id LIKE 'field_evidence:%'
        """,
    )
    assert len(field_evidence) == 1
    field = field_evidence[0]
    assert field["ledger_entry_id"] == "tier1.match_identity.match_id"
    assert field["fact_table"] == "matches"
    assert field["fact_id"] == MATCH_ID
    assert field["fact_field"] == "match_id"
    assert field["source_parser_surface"] == "MatchSummary.to_match_log_row"
    assert field["source_fact_key"] == "match_id"
    assert field["value_source"] == "conflict"
    assert field["confidence"] == "low"
    assert field["finality"] == "final"
    assert json.loads(str(field["drift_flags"])) == ["conflicting_evidence"]
    assert field["invariant_status"] == "failed"
    assert field["degraded_reason"] == "conflicting evidence"
    assert field["review_required"] == 1
    assert json.loads(str(field["source_payload_paths"])) == ["/match_log_rows/0/match_id"]
    assert "Player.log" not in str(field["source_payload_paths"])
    assert "http" not in str(field["source_payload_paths"])
    assert ":\\" not in str(field["source_payload_paths"])

    assert _sqlite_artifacts() == before_artifacts


def test_reingesting_same_replay_keeps_fact_counts_and_view_rows_stable() -> None:
    connection = _connect()
    replay = _representative_replay()
    tracked_tables = (
        "ingest_runs",
        "matches",
        "games",
        "match_results",
        "game_results",
        "opening_hands",
        "opening_hand_cards",
        "mulligan_events",
        "gameplay_actions",
        "gameplay_action_cards",
        "opponent_card_observations",
        "opponent_card_observation_cards",
        "fact_provenance",
    )

    first = ingest_parser_normalized_replay(connection, replay, started_at="first", finished_at="first-done")
    first_counts = {table: _count(connection, table) for table in tracked_tables}
    first_view_rows = _stable_view_snapshot(connection)

    second = ingest_parser_normalized_replay(connection, replay, started_at="second", finished_at="second-done")
    second_counts = {table: _count(connection, table) for table in tracked_tables}
    second_view_rows = _stable_view_snapshot(connection)

    assert second.ingest_run_id == first.ingest_run_id
    assert second.row_counts == first.row_counts
    assert second_counts == first_counts
    assert second_view_rows == first_view_rows
    assert _count(connection, "fact_provenance") == first_counts["fact_provenance"]
    assert _count(connection, "ingest_runs") == 1


def _stable_view_snapshot(connection: sqlite3.Connection) -> dict[str, list[dict[str, object]]]:
    return {
        "v_opening_hand_cards": _rows(
            connection,
            """
            SELECT match_id, game_id, opening_hand_card_id, card_position, card_name, ingest_run_id
            FROM v_opening_hand_cards
            ORDER BY game_id, card_position
            """,
        ),
        "v_opening_lines": _rows(
            connection,
            """
            SELECT gameplay_action_id, match_id, game_id, turn_number, action_type, card_count, grp_ids
            FROM v_opening_lines
            ORDER BY gameplay_action_id
            """,
        ),
        "v_gameplay_action_review": _rows(
            connection,
            """
            SELECT gameplay_action_id, match_id, game_id, turn_number, action_type, card_count, grp_ids
            FROM v_gameplay_action_review
            ORDER BY gameplay_action_id
            """,
        ),
        "v_mulligan_outcomes": _rows(
            connection,
            """
            SELECT mulligan_event_id, match_id, game_id, mulligan_count, availability_status
            FROM v_mulligan_outcomes
            ORDER BY mulligan_event_id
            """,
        ),
        "v_game1_vs_postboard": _rows(
            connection,
            """
            SELECT game_result_id, match_id, game_id, pre_postboard_label, play_draw, local_result
            FROM v_game1_vs_postboard
            ORDER BY game_result_id
            """,
        ),
        "v_play_draw_splits": _rows(
            connection,
            """
            SELECT play_draw, game_count, known_result_count, wins, losses, unknown_result_count, win_rate
            FROM v_play_draw_splits
            ORDER BY play_draw
            """,
        ),
        "v_sample_size_warnings": _rows(
            connection,
            """
            SELECT play_draw, game_count, sample_size_warning
            FROM v_sample_size_warnings
            ORDER BY play_draw
            """,
        ),
        "v_opponent_card_observation_review": _rows(
            connection,
            """
            SELECT
                opponent_card_observation_id,
                gameplay_action_id,
                match_id,
                game_id,
                evidence_status,
                confidence,
                review_required,
                card_grp_id
            FROM v_opponent_card_observation_review
            ORDER BY opponent_card_observation_id
            """,
        ),
        "field_evidence": _rows(
            connection,
            """
            SELECT
                fact_provenance_id,
                ledger_entry_id,
                fact_table,
                fact_id,
                fact_field,
                value_source,
                confidence,
                invariant_status,
                review_required
            FROM fact_provenance
            WHERE fact_provenance_id LIKE 'field_evidence:%'
            ORDER BY fact_provenance_id
            """,
        ),
    }
