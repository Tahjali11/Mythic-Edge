from __future__ import annotations

import json
import sqlite3

import pytest

from mythic_edge_parser.app.analytics_ingest import (
    AnalyticsReplayIngestError,
    ingest_parser_normalized_replay,
)
from mythic_edge_parser.app.analytics_migration_loader import ANALYTICS_SCHEMA_VERSION


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    return connection


def _base_replay() -> dict[str, object]:
    return {
        "source_kind": "sanitized_golden_replay",
        "source_artifact_label": "gameplay_action_ingest_v1",
        "parser_commit": "test-parser-commit",
        "parser_version": "test-parser-version",
        "generated_at": "2026-05-28T12:00:00+00:00",
        "match_log_rows": [
            {
                "match_id": "match:test:gameplay",
                "timestamp": "2026-05-28T12:30:00+00:00",
                "MTGA Match ID": "match:test:gameplay",
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
                "match_id": "match:test:gameplay",
                "timestamp": "2026-05-28T12:30:00+00:00",
                "MTGA Match ID": "match:test:gameplay",
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
        "match_id": "match:test:gameplay",
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
        "card_name": "Test Spell",
        "display_name": "Test Spell",
        "resolution_status": "resolved",
    }
    entry.update(overrides)
    return entry


def _with_actions(*actions: dict[str, object]) -> dict[str, object]:
    replay = _base_replay()
    replay["gameplay_action_entries"] = list(actions)
    return replay


def _count(connection: sqlite3.Connection, table_name: str) -> int:
    return int(connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0])


def _gameplay_provenance_rows(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    return connection.execute(
        """
        SELECT *
        FROM fact_provenance
        WHERE fact_table IN ('gameplay_actions', 'gameplay_action_cards')
        ORDER BY fact_table, fact_field
        """
    ).fetchall()


def _assert_no_partial_fact_rows(connection: sqlite3.Connection) -> None:
    assert _count(connection, "matches") == 0
    assert _count(connection, "games") == 0
    assert _count(connection, "gameplay_actions") == 0
    assert _count(connection, "gameplay_action_cards") == 0
    assert len(_gameplay_provenance_rows(connection)) == 0


def test_gameplay_action_ingest_writes_action_card_counts_and_safe_provenance() -> None:
    connection = _connect()

    result = ingest_parser_normalized_replay(
        connection,
        _with_actions(_action_entry()),
        started_at="2026-05-28T12:00:00+00:00",
        finished_at="2026-05-28T12:31:00+00:00",
    )

    assert result.warnings == []
    assert result.skipped == {}
    assert result.row_counts["gameplay_actions"] == 1
    assert result.row_counts["gameplay_action_cards"] == 1
    run = connection.execute("SELECT row_counts_json FROM ingest_runs").fetchone()
    assert json.loads(run["row_counts_json"])["gameplay_actions"] == 1
    assert json.loads(run["row_counts_json"])["gameplay_action_cards"] == 1

    action = connection.execute("SELECT * FROM gameplay_actions").fetchone()
    assert action["game_id"] == "match:test:gameplay:g1"
    assert action["match_id"] == "match:test:gameplay"
    assert action["game_number"] == 1
    assert action["timestamp"] == "2026-05-28T12:05:00+00:00"
    assert action["game_state_id"] == 42
    assert action["turn_number"] == 3
    assert action["action_type"] == "spell_cast"
    assert action["actor_relation"] == "opponent"
    assert action["from_zone_type"] == "ZoneType_Hand"
    assert action["to_zone_type"] == "ZoneType_Stack"
    assert action["source_status"] == "parser_normalized"
    assert action["annotation_context_label"] == "CastSpell"
    assert json.loads(action["raw_action_type_labels"]) == ["ActionType_Cast"]
    assert json.loads(action["annotation_type_labels"]) == ["AnnotationType_ObjectIdChanged"]
    assert action["visible_in_log"] == 1
    assert action["value_source"] == "derived"
    assert action["confidence"] == "unknown"
    assert action["finality"] == "reconciled"
    assert action["drift_status"] == "not_checked"
    assert action["parser_schema_version"] == ANALYTICS_SCHEMA_VERSION
    assert action["source_parser_surface"] == "gameplay_actions.py"
    assert action["availability_status"] == "available"

    card = connection.execute("SELECT * FROM gameplay_action_cards").fetchone()
    assert card["gameplay_action_id"] == action["gameplay_action_id"]
    assert card["game_id"] == action["game_id"]
    assert card["card_ordinal"] == 1
    assert card["instance_id"] == 1001
    assert card["grp_id"] == 2002
    assert card["observed_grp_id"] == 2002
    assert card["overlay_grp_id"] == 2002
    assert card["object_source_grp_id"] == 2002
    assert card["identity_hint_source"] == "direct_grp_id"
    assert card["card_name"] == "Test Spell"
    assert card["display_name"] == "Test Spell"
    assert card["name_resolution_status"] == "resolved"
    assert card["enrichment_status"] == "parser_rendered"

    provenance = _gameplay_provenance_rows(connection)
    assert {(row["fact_table"], row["fact_field"]) for row in provenance} == {
        ("gameplay_actions", "action_type"),
        ("gameplay_actions", "actor_relation"),
        ("gameplay_actions", "from_zone_type"),
        ("gameplay_actions", "to_zone_type"),
        ("gameplay_action_cards", "grp_id"),
    }
    for row in provenance:
        paths = json.loads(row["source_payload_paths"])
        assert row["ledger_entry_id"] == "tier5.gameplay_action.gameplay_action"
        assert row["source_parser_surface"] == "gameplay_actions.py"
        assert row["source_event_kind"] == "GameState"
        assert row["source_event_type"] is None
        assert row["source_event_timestamp"] == "2026-05-28T12:05:00+00:00"
        assert row["value_source"] == "derived"
        assert row["confidence"] == "unknown"
        assert row["finality"] == "reconciled"
        assert all(path.startswith("/gameplay_action_entries/0/") for path in paths)
        assert "Player.log" not in row["source_payload_paths"]
        assert "http" not in row["source_payload_paths"]
        assert ":\\" not in row["source_payload_paths"]


def test_replaying_same_gameplay_action_input_is_idempotent() -> None:
    connection = _connect()
    replay = _with_actions(_action_entry())

    first = ingest_parser_normalized_replay(connection, replay, started_at="first", finished_at="first-done")
    second = ingest_parser_normalized_replay(connection, replay, started_at="second", finished_at="second-done")

    assert second.ingest_run_id == first.ingest_run_id
    assert second.row_counts == first.row_counts
    assert _count(connection, "gameplay_actions") == 1
    assert _count(connection, "gameplay_action_cards") == 1
    assert len(_gameplay_provenance_rows(connection)) == 5


def test_action_without_card_identity_writes_parent_only() -> None:
    connection = _connect()
    action = _action_entry(
        instance_id=None,
        grp_id=None,
        observed_grp_id=None,
        overlay_grp_id=None,
        object_source_grp_id=None,
        card_name=None,
        display_name=None,
        resolution_status=None,
    )

    ingest_parser_normalized_replay(connection, _with_actions(action), started_at="now", finished_at="done")

    assert _count(connection, "gameplay_actions") == 1
    assert _count(connection, "gameplay_action_cards") == 0
    assert {
        row["fact_field"]
        for row in connection.execute("SELECT fact_field FROM fact_provenance WHERE fact_table = 'gameplay_actions'")
    } == {"action_type", "actor_relation", "from_zone_type", "to_zone_type"}


@pytest.mark.parametrize("actor_relation", ["local", "opponent", "unknown", ""])
def test_actor_relation_allowed_values(actor_relation: str) -> None:
    connection = _connect()

    ingest_parser_normalized_replay(
        connection,
        _with_actions(_action_entry(actor_relation=actor_relation, game_state_id=50)),
        started_at="now",
        finished_at="done",
    )

    row = connection.execute("SELECT actor_relation FROM gameplay_actions").fetchone()
    assert row["actor_relation"] == actor_relation


def test_invalid_actor_relation_fails_without_partial_fact_rows() -> None:
    connection = _connect()

    with pytest.raises(AnalyticsReplayIngestError, match="actor_relation"):
        ingest_parser_normalized_replay(
            connection,
            _with_actions(_action_entry(actor_relation="teammate")),
            started_at="now",
            finished_at="done",
        )

    _assert_no_partial_fact_rows(connection)


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("game_number", 0),
        ("game_state_id", True),
        ("turn_number", 1.5),
        ("instance_id", -1),
        ("grp_id", "not-an-int"),
        ("observed_grp_id", 2.5),
        ("overlay_grp_id", False),
        ("object_source_grp_id", -1),
    ],
)
def test_malformed_numeric_action_fields_fail_without_partial_fact_rows(field_name: str, bad_value: object) -> None:
    connection = _connect()

    with pytest.raises(AnalyticsReplayIngestError, match=field_name):
        ingest_parser_normalized_replay(
            connection,
            _with_actions(_action_entry(**{field_name: bad_value})),
            started_at="now",
            finished_at="done",
        )

    _assert_no_partial_fact_rows(connection)


def test_malformed_card_ordinal_fails_without_partial_fact_rows() -> None:
    connection = _connect()
    action = _action_entry(
        instance_id=None,
        grp_id=None,
        observed_grp_id=None,
        overlay_grp_id=None,
        object_source_grp_id=None,
        card_name=None,
        display_name=None,
        associated_cards=[
            {
                "card_ordinal": 0,
                "grp_id": 2002,
            },
        ],
    )

    with pytest.raises(AnalyticsReplayIngestError, match="card_ordinal"):
        ingest_parser_normalized_replay(connection, _with_actions(action), started_at="now", finished_at="done")

    _assert_no_partial_fact_rows(connection)


def test_missing_parent_game_identity_fails_without_orphan_action_rows() -> None:
    connection = _connect()

    with pytest.raises(AnalyticsReplayIngestError, match="unknown game parent"):
        ingest_parser_normalized_replay(
            connection,
            _with_actions(_action_entry(game_number=2)),
            started_at="now",
            finished_at="done",
        )

    _assert_no_partial_fact_rows(connection)


def test_gameplay_action_ingest_has_no_optional_deferred_warning() -> None:
    connection = _connect()
    replay = _with_actions(_action_entry())

    result = ingest_parser_normalized_replay(connection, replay, started_at="now", finished_at="done")

    assert result.skipped == {}
    assert result.warnings == []
    assert _count(connection, "gameplay_actions") == 1
    assert _count(connection, "opponent_card_observations") == 0
