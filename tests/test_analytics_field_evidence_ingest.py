from __future__ import annotations

import json
import sqlite3

import pytest

from mythic_edge_parser.app import evidence_ledger
from mythic_edge_parser.app.analytics_ingest import (
    AnalyticsReplayIngestError,
    ingest_parser_normalized_replay,
)


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    return connection


def _base_replay() -> dict[str, object]:
    return {
        "source_kind": "sanitized_golden_replay",
        "source_artifact_label": "field_evidence_ingest_v1",
        "parser_commit": "test-parser-commit",
        "parser_version": "test-parser-version",
        "generated_at": "2026-05-29T12:00:00+00:00",
        "match_log_rows": [
            {
                "match_id": "match:test:field-evidence",
                "timestamp": "2026-05-29T12:30:00+00:00",
                "MTGA Match ID": "match:test:field-evidence",
                "Match Win?": "W",
                "Match Win Flag": 1,
                "Games Won": 1,
                "Games Lost": 0,
                "Total Games": 1,
                "Game Win %": 1.0,
                "MTGA Format": "Constructed",
                "MTGA Event ID": "Play_BestOf1",
                "MTGA Queue Type": "Best of 1",
                "MGTA Start Time": "2026-05-29T12:00:00+00:00",
                "MTGA End Time": "2026-05-29T12:30:00+00:00",
                "MTGA Sync Status": "Final",
            },
        ],
        "game_log_rows": [
            {
                "match_id": "match:test:field-evidence",
                "timestamp": "2026-05-29T12:30:00+00:00",
                "MTGA Match ID": "match:test:field-evidence",
                "Game Number": 1,
                "Pre / Postboard": "Preboard",
                "Play / Draw": "Play",
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


def _field_evidence(**overrides: object) -> dict[str, object]:
    entry: dict[str, object] = {
        "object": evidence_ledger.FIELD_EVIDENCE_OBJECT,
        "schema_version": evidence_ledger.FIELD_EVIDENCE_SCHEMA_VERSION,
        "ledger_version": evidence_ledger.LEDGER_VERSION,
        "entry_id": "tier1.match_identity.match_id",
        "output_family": "match_identity_and_lifecycle",
        "output_field": "match_id",
        "value_source": "observed",
        "confidence": "high",
        "finality": "reconciled",
        "source_event_kind": "MatchState",
        "source_event_type": "match_started",
        "source_payload_paths": ["/match_log_rows/0/match_id"],
        "source_event_timestamp": "2026-05-29T12:00:00+00:00",
        "drift_flags": [],
        "invariant_status": "passed",
        "degraded_reason": "",
        "review_required": False,
        "fact_table": "matches",
        "fact_id": "match:test:field-evidence",
        "fact_field": "match_id",
        "source_parser_surface": "MatchSummary.to_match_log_row",
        "source_fact_key": "match_id",
    }
    entry.update(overrides)
    return entry


def _with_field_evidence(*entries: dict[str, object]) -> dict[str, object]:
    replay = _base_replay()
    replay["field_evidence_entries"] = list(entries)
    return replay


def _count(connection: sqlite3.Connection, table_name: str) -> int:
    return int(connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0])


def _field_evidence_rows(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    return connection.execute(
        """
        SELECT *
        FROM fact_provenance
        WHERE fact_provenance_id LIKE 'field_evidence:%'
        ORDER BY ledger_entry_id, source_payload_paths
        """
    ).fetchall()


def _assert_no_partial_fact_rows(connection: sqlite3.Connection) -> None:
    assert _count(connection, "ingest_runs") == 0
    assert _count(connection, "matches") == 0
    assert _count(connection, "games") == 0
    assert _count(connection, "fact_provenance") == 0


def test_valid_field_evidence_writes_multiple_safe_provenance_rows() -> None:
    connection = _connect()
    second_entry = _field_evidence(
        entry_id="tier1.match_identity.match_id_fallback",
        source_event_type="match_id_fallback",
        source_payload_paths=["payload.match_id"],
        drift_flags=["fallback_used"],
        invariant_status="not_checked",
        degraded_reason="fallback_used",
    )

    result = ingest_parser_normalized_replay(
        connection,
        _with_field_evidence(_field_evidence(), second_entry),
        started_at="2026-05-29T12:00:00+00:00",
        finished_at="2026-05-29T12:31:00+00:00",
    )

    assert result.warnings == []
    assert result.skipped == {}
    assert result.row_counts["fact_provenance"] == 6
    run = connection.execute("SELECT row_counts_json FROM ingest_runs").fetchone()
    assert json.loads(run["row_counts_json"])["fact_provenance"] == 6

    rows = _field_evidence_rows(connection)
    assert len(rows) == 2
    assert {row["fact_table"] for row in rows} == {"matches"}
    assert {row["fact_id"] for row in rows} == {"match:test:field-evidence"}
    assert {row["fact_field"] for row in rows} == {"match_id"}
    assert {row["ledger_entry_id"] for row in rows} == {
        "tier1.match_identity.match_id",
        "tier1.match_identity.match_id_fallback",
    }
    assert {row["source_parser_surface"] for row in rows} == {"MatchSummary.to_match_log_row"}
    assert {row["source_fact_key"] for row in rows} == {"match_id"}
    assert {row["source_event_kind"] for row in rows} == {"MatchState"}
    assert {row["source_event_type"] for row in rows} == {"match_started", "match_id_fallback"}
    assert {row["source_event_timestamp"] for row in rows} == {"2026-05-29T12:00:00+00:00"}
    assert {row["value_source"] for row in rows} == {"observed"}
    assert {row["confidence"] for row in rows} == {"high"}
    assert {row["finality"] for row in rows} == {"reconciled"}
    assert {row["invariant_status"] for row in rows} == {"passed", "not_checked"}
    assert {row["review_required"] for row in rows} == {0}
    assert {row["degraded_reason"] for row in rows} == {None, "fallback_used"}
    assert {tuple(json.loads(row["source_payload_paths"])) for row in rows} == {
        ("/match_log_rows/0/match_id",),
        ("payload.match_id",),
    }
    assert {tuple(json.loads(row["drift_flags"])) for row in rows} == {(), ("fallback_used",)}
    assert all(row["fact_provenance_id"].startswith("field_evidence:") for row in rows)

    automatic_rows = connection.execute(
        "SELECT COUNT(*) AS count FROM fact_provenance WHERE fact_provenance_id NOT LIKE 'field_evidence:%'"
    ).fetchone()
    assert automatic_rows["count"] == 4
    match_row = connection.execute("SELECT source_parser_surface, source_fact_key FROM matches").fetchone()
    assert dict(match_row) == {
        "source_parser_surface": "MatchSummary.to_match_log_row",
        "source_fact_key": "match_id",
    }


def test_replaying_same_field_evidence_input_is_idempotent() -> None:
    connection = _connect()
    replay = _with_field_evidence(_field_evidence(), _field_evidence(entry_id="tier1.match_identity.match_id_alt"))

    first = ingest_parser_normalized_replay(connection, replay, started_at="first", finished_at="first-done")
    second = ingest_parser_normalized_replay(connection, replay, started_at="second", finished_at="second-done")

    assert second.ingest_run_id == first.ingest_run_id
    assert second.row_counts == first.row_counts
    assert len(_field_evidence_rows(connection)) == 2
    assert _count(connection, "matches") == 1
    assert _count(connection, "games") == 1


def test_review_required_field_evidence_preserves_policy_labels() -> None:
    connection = _connect()
    entry = _field_evidence(
        value_source="conflict",
        confidence="low",
        finality="final",
        drift_flags=["conflicting_evidence"],
        invariant_status="failed",
        degraded_reason="conflicting evidence",
        review_required=True,
    )

    ingest_parser_normalized_replay(connection, _with_field_evidence(entry), started_at="now", finished_at="done")

    row = _field_evidence_rows(connection)[0]
    assert row["value_source"] == "conflict"
    assert row["confidence"] == "low"
    assert row["finality"] == "final"
    assert json.loads(row["drift_flags"]) == ["conflicting_evidence"]
    assert row["invariant_status"] == "failed"
    assert row["degraded_reason"] == "conflicting evidence"
    assert row["review_required"] == 1


@pytest.mark.parametrize(
    ("field_name", "bad_value", "error_match"),
    [
        ("object", "wrong", "invalid_object"),
        ("schema_version", "wrong", "invalid_schema_version"),
        ("ledger_version", "wrong", "invalid_ledger_version"),
        ("value_source", "guessed", "value_source"),
        ("confidence", "certain", "confidence"),
        ("finality", "done", "finality"),
        ("drift_flags", ["mystery_drift"], "drift_flags"),
        ("invariant_status", "mystery", "invariant_status"),
        ("review_required", True, "invalid_review_required"),
    ],
)
def test_malformed_canonical_field_evidence_fails_without_partial_rows(
    field_name: str,
    bad_value: object,
    error_match: str,
) -> None:
    connection = _connect()

    with pytest.raises(AnalyticsReplayIngestError, match=error_match):
        ingest_parser_normalized_replay(
            connection,
            _with_field_evidence(_field_evidence(**{field_name: bad_value})),
            started_at="now",
            finished_at="done",
        )

    _assert_no_partial_fact_rows(connection)


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("fact_table", "fact_provenance"),
        ("fact_table", "schema_migrations"),
        ("fact_id", ""),
        ("fact_field", ""),
        ("source_parser_surface", "C:" + "\\Users\\private\\parser.py"),
        ("source_fact_key", ""),
        ("source_payload_paths", "payload.match_id"),
        ("source_payload_paths", ["C:" + "\\Users\\private\\Player.log"]),
        ("source_payload_paths", ["/" + "Users/private/Player.log"]),
        ("source_payload_paths", ["/tmp"]),
        ("source_payload_paths", ["/Users"]),
        ("source_payload_paths", ["/private"]),
        ("source_payload_paths", ["/var"]),
        ("source_payload_paths", ["/" + "C:" + "/blocked"]),
        ("source_payload_paths", ["https://hooks.example.invalid/secret"]),
        ("drift_flags", "fallback_used"),
    ],
)
def test_malformed_attachment_fields_fail_without_partial_rows(field_name: str, bad_value: object) -> None:
    connection = _connect()

    with pytest.raises(AnalyticsReplayIngestError, match=field_name):
        ingest_parser_normalized_replay(
            connection,
            _with_field_evidence(_field_evidence(**{field_name: bad_value})),
            started_at="now",
            finished_at="done",
        )

    _assert_no_partial_fact_rows(connection)


def test_missing_target_fact_row_fails_without_partial_rows() -> None:
    connection = _connect()

    with pytest.raises(AnalyticsReplayIngestError, match="missing target fact row"):
        ingest_parser_normalized_replay(
            connection,
            _with_field_evidence(_field_evidence(fact_id="match:test:missing")),
            started_at="now",
            finished_at="done",
        )

    _assert_no_partial_fact_rows(connection)
