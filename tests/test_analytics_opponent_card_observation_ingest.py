from __future__ import annotations

import json
import sqlite3

import pytest

from mythic_edge_parser.app.analytics_ingest import (
    AnalyticsReplayIngestError,
    ingest_parser_normalized_replay,
)
from mythic_edge_parser.app.analytics_migration_loader import ANALYTICS_SCHEMA_VERSION
from mythic_edge_parser.app.opponent_card_observations import (
    OPPONENT_CARD_OBSERVATION_OBJECT,
)
from mythic_edge_parser.app.opponent_card_observations import (
    SCHEMA_VERSION as OPPONENT_CARD_OBSERVATION_SCHEMA_VERSION,
)


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    return connection


def _base_replay() -> dict[str, object]:
    return {
        "source_kind": "sanitized_golden_replay",
        "source_artifact_label": "opponent_card_observation_ingest_v1",
        "parser_commit": "test-parser-commit",
        "parser_version": "test-parser-version",
        "generated_at": "2026-05-28T12:00:00+00:00",
        "match_log_rows": [
            {
                "match_id": "match:test:opponent-observation",
                "timestamp": "2026-05-28T12:30:00+00:00",
                "MTGA Match ID": "match:test:opponent-observation",
                "Match Win?": "W",
                "Match Win Flag": 1,
                "Games Won": 1,
                "Games Lost": 0,
                "Total Games": 1,
                "Game Win %": 1.0,
                "MTGA Format": "Constructed",
                "MTGA Event ID": "Play_BestOf1",
                "MTGA Queue Type": "Best of 1",
                "MGTA Start Time": "2026-05-28T12:00:00+00:00",
                "MTGA End Time": "2026-05-28T12:30:00+00:00",
                "MTGA Sync Status": "Final",
            },
        ],
        "game_log_rows": [
            {
                "match_id": "match:test:opponent-observation",
                "timestamp": "2026-05-28T12:30:00+00:00",
                "MTGA Match ID": "match:test:opponent-observation",
                "Game Number": 1,
                "Pre / Postboard": "Preboard",
                "Play / Draw": "Draw",
                "Mulligans": 0,
                "Opening Hand Size": "",
                "Opening Hand": "",
                "Mulliganed Away": "",
                "Game Result": "W",
                "Turn Count": 5,
                "Game Duration": 900,
                "MTGA Format": "Constructed",
                "MTGA Event ID": "Play_BestOf1",
                "MTGA Queue Type": "Best of 1",
            },
        ],
    }


def _action_entry(**overrides: object) -> dict[str, object]:
    entry: dict[str, object] = {
        "timestamp": "2026-05-28T12:05:00+00:00",
        "match_id": "match:test:opponent-observation",
        "game_number": 1,
        "game_state_id": 42,
        "turn_number": 3,
        "action_type": "spell_cast",
        "cast_mode": "main_face",
        "instance_id": 1001,
        "grp_id": 2002,
        "observed_grp_id": 2002,
        "overlay_grp_id": 2002,
        "object_source_grp_id": 2002,
        "parent_id": 1000,
        "identity_hint_source": "direct_grp_id",
        "actor_relation": "opponent",
        "from_zone_type": "ZoneType_Hand",
        "to_zone_type": "ZoneType_Stack",
        "raw_action_types": ["ActionType_Cast"],
        "annotation_types": ["AnnotationType_ObjectIdChanged"],
        "annotation_categories": ["CastSpell"],
        "visible_in_log": True,
        "card_name": "Visible Spell",
        "display_name": "Visible Spell",
        "resolution_status": "resolved",
    }
    entry.update(overrides)
    return entry


def _observation(**overrides: object) -> dict[str, object]:
    observation: dict[str, object] = {
        "object": OPPONENT_CARD_OBSERVATION_OBJECT,
        "schema_version": OPPONENT_CARD_OBSERVATION_SCHEMA_VERSION,
        "timestamp": "2026-05-28T12:05:00+00:00",
        "match_id": "match:test:opponent-observation",
        "game_number": 1,
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
        "evidence_status": "observed",
        "value_source": "observed",
        "confidence": "high",
        "visibility": "action_visible",
        "from_zone_type": "ZoneType_Hand",
        "to_zone_type": "ZoneType_Stack",
        "raw_action_types": ["ActionType_Cast"],
        "annotation_types": ["AnnotationType_ObjectIdChanged"],
        "annotation_categories": ["CastSpell"],
        "degradation_flags": [],
        "review_required": False,
    }
    observation.update(overrides)
    return observation


def _with_observations(*observations: dict[str, object]) -> dict[str, object]:
    replay = _base_replay()
    replay["opponent_card_observations"] = list(observations)
    return replay


def _with_actions_and_observations(
    actions: list[dict[str, object]],
    observations: list[dict[str, object]],
) -> dict[str, object]:
    replay = _base_replay()
    replay["gameplay_action_entries"] = actions
    replay["opponent_card_observations"] = observations
    return replay


def _count(connection: sqlite3.Connection, table_name: str) -> int:
    return int(connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0])


def _opponent_provenance_rows(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    return connection.execute(
        """
        SELECT *
        FROM fact_provenance
        WHERE fact_table IN ('opponent_card_observations', 'opponent_card_observation_cards')
        ORDER BY fact_table, fact_field
        """
    ).fetchall()


def _assert_no_partial_fact_rows(connection: sqlite3.Connection) -> None:
    assert _count(connection, "matches") == 0
    assert _count(connection, "games") == 0
    assert _count(connection, "opponent_card_observations") == 0
    assert _count(connection, "opponent_card_observation_cards") == 0
    assert len(_opponent_provenance_rows(connection)) == 0


def test_opponent_observation_ingest_writes_rows_counts_link_and_safe_provenance() -> None:
    connection = _connect()

    result = ingest_parser_normalized_replay(
        connection,
        _with_actions_and_observations([_action_entry()], [_observation()]),
        started_at="2026-05-28T12:00:00+00:00",
        finished_at="2026-05-28T12:31:00+00:00",
    )

    assert result.warnings == []
    assert result.skipped == {}
    assert result.row_counts["opponent_card_observations"] == 1
    assert result.row_counts["opponent_card_observation_cards"] == 1
    run = connection.execute("SELECT row_counts_json FROM ingest_runs").fetchone()
    row_counts = json.loads(run["row_counts_json"])
    assert row_counts["opponent_card_observations"] == 1
    assert row_counts["opponent_card_observation_cards"] == 1

    action = connection.execute("SELECT * FROM gameplay_actions").fetchone()
    observation = connection.execute("SELECT * FROM opponent_card_observations").fetchone()
    assert observation["game_id"] == "match:test:opponent-observation:g1"
    assert observation["match_id"] == "match:test:opponent-observation"
    assert observation["gameplay_action_id"] == action["gameplay_action_id"]
    assert observation["timestamp"] == "2026-05-28T12:05:00+00:00"
    assert observation["game_state_id"] == 42
    assert observation["turn_number"] == 3
    assert observation["actor_relation"] == "opponent"
    assert observation["actor_seat_id"] == 2
    assert observation["local_seat_id"] == 1
    assert observation["instance_id"] == 1001
    assert observation["grp_id"] == 2002
    assert observation["observed_grp_id"] == 2002
    assert observation["overlay_grp_id"] == 2002
    assert observation["object_source_grp_id"] == 2002
    assert observation["parent_id"] == 1000
    assert observation["identity_hint_source"] == "direct_grp_id"
    assert observation["card_name"] == "Visible Spell"
    assert observation["display_name"] == "Visible Spell"
    assert observation["resolution_status"] == "resolved"
    assert observation["name_resolution_source"] == "grp_id_catalog"
    assert observation["action_type"] == "spell_cast"
    assert observation["cast_mode"] == "main_face"
    assert observation["source_evidence"] == "action_array"
    assert observation["evidence_status"] == "observed"
    assert observation["visibility"] == "action_visible"
    assert json.loads(observation["degradation_flags"]) == []
    assert observation["review_required"] == 0
    assert observation["value_source"] == "observed"
    assert observation["confidence"] == "high"
    assert observation["finality"] == "reconciled"
    assert observation["drift_status"] == "not_checked"
    assert observation["parser_schema_version"] == ANALYTICS_SCHEMA_VERSION
    assert observation["source_parser_surface"] == "opponent_card_observations.py"
    assert observation["availability_status"] == "available"

    card = connection.execute("SELECT * FROM opponent_card_observation_cards").fetchone()
    assert card["opponent_card_observation_id"] == observation["opponent_card_observation_id"]
    assert card["game_id"] == observation["game_id"]
    assert card["card_ordinal"] == 1
    assert card["grp_id"] == 2002
    assert card["observed_grp_id"] == 2002
    assert card["overlay_grp_id"] == 2002
    assert card["object_source_grp_id"] == 2002
    assert card["identity_hint_source"] == "direct_grp_id"
    assert card["card_name"] == "Visible Spell"
    assert card["resolution_status"] == "resolved"
    assert card["visibility"] == "action_visible"
    assert card["value_source"] == "observed"
    assert card["confidence"] == "high"

    provenance = _opponent_provenance_rows(connection)
    assert {(row["fact_table"], row["fact_field"]) for row in provenance} == {
        ("opponent_card_observations", "visibility"),
        ("opponent_card_observations", "evidence_status"),
        ("opponent_card_observations", "value_source"),
        ("opponent_card_observations", "confidence"),
        ("opponent_card_observations", "review_required"),
        ("opponent_card_observations", "degradation_flags"),
        ("opponent_card_observations", "action_type"),
        ("opponent_card_observation_cards", "grp_id"),
    }
    for row in provenance:
        paths = json.loads(row["source_payload_paths"])
        assert row["ledger_entry_id"] == "tier5.opponent_card_observation.opponent_card_observation"
        assert row["source_parser_surface"] == "opponent_card_observations.py"
        assert row["source_event_kind"] == "GameState"
        assert row["source_event_type"] is None
        assert row["source_event_timestamp"] == "2026-05-28T12:05:00+00:00"
        assert row["value_source"] == "observed"
        assert row["confidence"] == "high"
        assert row["finality"] == "reconciled"
        assert json.loads(row["drift_flags"]) == []
        assert row["review_required"] == 0
        assert all(path.startswith("/opponent_card_observations/0/") for path in paths)
        assert "Player.log" not in row["source_payload_paths"]
        assert "http" not in row["source_payload_paths"]
        assert ":\\" not in row["source_payload_paths"]


def test_replaying_same_opponent_observation_input_is_idempotent() -> None:
    connection = _connect()
    replay = _with_actions_and_observations([_action_entry()], [_observation()])

    first = ingest_parser_normalized_replay(connection, replay, started_at="first", finished_at="first-done")
    second = ingest_parser_normalized_replay(connection, replay, started_at="second", finished_at="second-done")

    assert second.ingest_run_id == first.ingest_run_id
    assert second.row_counts == first.row_counts
    assert _count(connection, "opponent_card_observations") == 1
    assert _count(connection, "opponent_card_observation_cards") == 1
    assert len(_opponent_provenance_rows(connection)) == 8


def test_observation_without_matching_gameplay_action_stores_null_link() -> None:
    connection = _connect()

    result = ingest_parser_normalized_replay(
        connection,
        _with_observations(_observation()),
        started_at="now",
        finished_at="done",
    )

    row = connection.execute("SELECT gameplay_action_id FROM opponent_card_observations").fetchone()
    assert result.skipped == {}
    assert result.warnings == []
    assert row["gameplay_action_id"] is None
    assert _count(connection, "gameplay_actions") == 0
    assert _count(connection, "opponent_card_observations") == 1


def test_explicit_unknown_gameplay_action_id_warns_and_uses_null_link() -> None:
    connection = _connect()

    result = ingest_parser_normalized_replay(
        connection,
        _with_observations(_observation(gameplay_action_id="gameplay_action:missing")),
        started_at="now",
        finished_at="done",
    )

    row = connection.execute("SELECT gameplay_action_id FROM opponent_card_observations").fetchone()
    assert row["gameplay_action_id"] is None
    assert result.warnings == ["opponent_card_observations[0] gameplay_action_id did not match an ingested action"]
    assert result.skipped == {}


def test_degraded_missing_identity_observation_writes_parent_without_fabricated_card() -> None:
    connection = _connect()
    observation = _observation(
        instance_id="",
        grp_id="",
        observed_grp_id="",
        overlay_grp_id="",
        object_source_grp_id="",
        identity_hint_source="",
        card_name="",
        display_name="",
        resolution_status="unresolved",
        evidence_status="degraded",
        value_source="unknown",
        confidence="low",
        visibility="ambiguous",
        degradation_flags=["missing_card_identity", "name_resolution_unresolved"],
        review_required=True,
    )

    ingest_parser_normalized_replay(connection, _with_observations(observation), started_at="now", finished_at="done")

    parent = connection.execute("SELECT * FROM opponent_card_observations").fetchone()
    assert parent["gameplay_action_id"] is None
    assert parent["grp_id"] is None
    assert parent["card_name"] is None
    assert json.loads(parent["degradation_flags"]) == ["missing_card_identity", "name_resolution_unresolved"]
    assert parent["review_required"] == 1
    assert parent["value_source"] == "unknown"
    assert parent["confidence"] == "low"
    assert parent["finality"] == "reconciled"
    assert parent["drift_status"] == "degraded"
    assert _count(connection, "opponent_card_observation_cards") == 0
    provenance = _opponent_provenance_rows(connection)
    assert {row["degraded_reason"] for row in provenance} == {
        "missing_card_identity;name_resolution_unresolved"
    }
    assert {row["review_required"] for row in provenance} == {1}


def test_unsafe_degradation_flags_fail_without_persisting_private_text() -> None:
    unsafe_flags = [
        "C:" + "\\private\\Player.log",
        "https://" + "example.com/private-artifact",
        "[" + "Client GRE" + "] raw payload marker",
        "api_" + "key=" + "not-a-real-value",
        "failed_" + "posts payload marker",
    ]

    for unsafe_flag in unsafe_flags:
        connection = _connect()

        with pytest.raises(AnalyticsReplayIngestError, match="degradation_flags"):
            ingest_parser_normalized_replay(
                connection,
                _with_observations(
                    _observation(
                        evidence_status="degraded",
                        confidence="low",
                        visibility="ambiguous",
                        degradation_flags=["missing_card_identity", unsafe_flag],
                        review_required=True,
                    )
                ),
                started_at="now",
                finished_at="done",
            )

        _assert_no_partial_fact_rows(connection)


def test_observation_ingest_has_no_optional_deferred_warning() -> None:
    connection = _connect()
    replay = _with_observations(_observation())

    result = ingest_parser_normalized_replay(connection, replay, started_at="now", finished_at="done")

    assert result.skipped == {}
    assert result.warnings == []
    assert _count(connection, "opponent_card_observations") == 1


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("object", "wrong_object"),
        ("schema_version", "wrong_schema"),
        ("actor_relation", "local"),
        ("value_source", "degraded"),
        ("confidence", "certain"),
        ("evidence_status", "clean"),
        ("visibility", "private_hand"),
        ("degradation_flags", "missing_card_identity"),
        ("degradation_flags", ("missing_card_identity",)),
        ("review_required", "sometimes"),
        ("game_number", 0),
        ("game_state_id", True),
        ("turn_number", 1.5),
        ("actor_seat_id", -1),
        ("local_seat_id", False),
        ("instance_id", "not-an-int"),
        ("grp_id", 2.5),
        ("observed_grp_id", -1),
        ("overlay_grp_id", True),
        ("object_source_grp_id", -1),
        ("parent_id", 2.25),
    ],
)
def test_malformed_observation_inputs_fail_without_partial_fact_rows(field_name: str, bad_value: object) -> None:
    connection = _connect()

    with pytest.raises(AnalyticsReplayIngestError, match=field_name):
        ingest_parser_normalized_replay(
            connection,
            _with_observations(_observation(**{field_name: bad_value})),
            started_at="now",
            finished_at="done",
        )

    _assert_no_partial_fact_rows(connection)


def test_missing_parent_game_identity_fails_without_orphan_observation_rows() -> None:
    connection = _connect()

    with pytest.raises(AnalyticsReplayIngestError, match="unknown game parent"):
        ingest_parser_normalized_replay(
            connection,
            _with_observations(_observation(game_number=2)),
            started_at="now",
            finished_at="done",
        )

    _assert_no_partial_fact_rows(connection)
