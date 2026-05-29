from __future__ import annotations

import os
import sqlite3
from collections import Counter
from pathlib import Path

import pytest

from mythic_edge_parser.app.match_journal_repository import MatchJournalRepository, ensure_match_journal_schema
from mythic_edge_parser.app.match_journal_service import (
    MATCH_JOURNAL_SERVICE_VERSION,
    MatchJournalService,
    MatchJournalServiceConflictError,
    MatchJournalServiceNotFoundError,
    MatchJournalServiceValidationError,
)

APPLIED_AT = "2026-05-29T00:00:00+00:00"
JOURNAL_DATA_TABLES = (
    "journal_matches",
    "journal_games",
    "journal_notes",
    "journal_labels",
    "journal_review_flags",
    "journal_reference_values",
    "journal_field_overrides",
)


class SequenceClock:
    def __init__(self) -> None:
        self.index = 0

    def __call__(self) -> str:
        self.index += 1
        return f"2026-05-29T00:01:{self.index:02d}+00:00"


class CountingIds:
    def __init__(self) -> None:
        self.counts: Counter[str] = Counter()

    def __call__(self, prefix: str) -> str:
        self.counts[prefix] += 1
        return f"{prefix}:service:{self.counts[prefix]}"


def _connect(*, with_schema: bool = True) -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    if with_schema:
        ensure_match_journal_schema(connection, applied_at=APPLIED_AT)
    return connection


def _repo(connection: sqlite3.Connection) -> MatchJournalRepository:
    return MatchJournalRepository(connection, id_factory=CountingIds(), clock=SequenceClock())


def _service() -> tuple[sqlite3.Connection, MatchJournalService]:
    connection = _connect()
    return connection, MatchJournalService(_repo(connection))


def _count(connection: sqlite3.Connection, table_name: str) -> int:
    row = connection.execute(f"SELECT COUNT(*) AS count FROM {table_name}").fetchone()
    return int(row["count"])


def _journal_row_counts(connection: sqlite3.Connection) -> dict[str, int]:
    return {table_name: _count(connection, table_name) for table_name in JOURNAL_DATA_TABLES}


def _table_names(connection: sqlite3.Connection) -> set[str]:
    rows = connection.execute("SELECT name FROM sqlite_schema WHERE type = 'table'").fetchall()
    return {str(row["name"]) for row in rows}


def test_service_version_and_construction_from_repository() -> None:
    _connection, service = _service()

    assert MATCH_JOURNAL_SERVICE_VERSION == "match_journal_service.v1"
    assert isinstance(service, MatchJournalService)


def test_from_connection_can_explicitly_ensure_schema_without_default_database(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MATCH_JOURNAL_DATABASE_PATH", "/tmp/should-not-be-read.sqlite3")
    connection = _connect(with_schema=False)

    service = MatchJournalService.from_connection(
        connection,
        id_factory=CountingIds(),
        clock=SequenceClock(),
        ensure_schema=True,
        applied_at=APPLIED_AT,
    )
    result = service.record_unattached_note("Synthetic local note.", source_surface="test_fixture")

    assert result["status"] == "completed"
    assert "journal_matches" in _table_names(connection)
    assert not Path("/tmp/should-not-be-read.sqlite3").exists()
    assert os.environ["MATCH_JOURNAL_DATABASE_PATH"] == "/tmp/should-not-be-read.sqlite3"


def test_match_note_with_parser_context_creates_one_match_container_and_note() -> None:
    _connection, service = _service()

    result = service.record_match_note(
        {"parser_match_id": "parser-match-1"},
        "Synthetic match review note.",
        source_surface="test_fixture",
        privacy_label="sanitized_fixture",
    )

    assert result["action"] == "record_match_note"
    assert result["status"] == "completed"
    assert result["primary_record_type"] == "note"
    match = result["records"]["match"]
    note = result["records"]["note"]
    assert match["parser_match_id"] == "parser-match-1"
    assert match["attachment_status"] == "attached"
    assert note["note_scope"] == "match"
    assert note["journal_match_id"] == match["journal_match_id"]
    assert note["parser_match_id"] == "parser-match-1"
    assert "parser-game-" not in str(result)


def test_game_note_with_parser_context_creates_match_and_game_containers() -> None:
    _connection, service = _service()

    result = service.record_game_note(
        {"parser_match_id": "parser-match-1", "parser_game_id": "parser-game-1", "game_number": 1},
        "Synthetic game note.",
    )

    game = result["records"]["game"]
    note = result["records"]["note"]
    assert game["parser_match_id"] == "parser-match-1"
    assert game["parser_game_id"] == "parser-game-1"
    assert game["game_number"] == 1
    assert note["note_scope"] == "game"
    assert note["journal_game_id"] == game["journal_game_id"]
    assert note["parser_game_id"] == "parser-game-1"


def test_sideboarding_note_uses_existing_game_context() -> None:
    _connection, service = _service()
    game_result = service.record_game_note(
        {"parser_match_id": "parser-match-1", "parser_game_id": "parser-game-1"},
        "Create context.",
    )

    result = service.record_sideboarding_note(
        {"journal_game_id": game_result["records"]["game"]["journal_game_id"]},
        "Synthetic sideboard note.",
    )

    note = result["records"]["note"]
    assert note["note_scope"] == "sideboarding"
    assert note["journal_game_id"] == game_result["records"]["game"]["journal_game_id"]
    assert note["parser_game_id"] == "parser-game-1"


def test_unattached_note_is_preserved_without_parser_or_journal_context() -> None:
    _connection, service = _service()

    result = service.record_unattached_note("Synthetic unattached note.", note_format="markdown")
    note = result["records"]["note"]

    assert result["warnings"] == []
    assert note["note_scope"] == "unattached"
    assert note["journal_match_id"] is None
    assert note["journal_game_id"] is None
    assert note["parser_match_id"] is None
    assert note["parser_game_id"] is None


def test_missing_explicit_journal_context_raises_service_not_found() -> None:
    _connection, service = _service()

    with pytest.raises(MatchJournalServiceNotFoundError):
        service.record_match_note({"journal_match_id": "missing-match"}, "No row.")
    with pytest.raises(MatchJournalServiceNotFoundError):
        service.record_game_note({"journal_game_id": "missing-game"}, "No row.")


def test_duplicate_parser_match_context_raises_service_conflict() -> None:
    connection, service = _service()
    repository = service.repository
    repository.create_match({"journal_match_id": "journal-match-1", "parser_match_id": "parser-match-1"})
    repository.create_match({"journal_match_id": "journal-match-2", "parser_match_id": "parser-match-1"})

    with pytest.raises(MatchJournalServiceConflictError):
        service.record_match_note({"parser_match_id": "parser-match-1"}, "Ambiguous.")

    assert _count(connection, "journal_notes") == 0


def test_experiment_label_writes_label_and_match_metadata() -> None:
    _connection, service = _service()
    match_note = service.record_match_note({"parser_match_id": "parser-match-1"}, "Create match.")

    result = service.set_experiment_label(
        {"journal_match_id": match_note["records"]["match"]["journal_match_id"]},
        "experiment-alpha",
    )

    assert result["records"]["experiment_label"]["label_type"] == "experiment_id"
    assert result["records"]["experiment_label"]["label_value"] == "experiment-alpha"
    assert result["records"]["match"]["experiment_id"] == "experiment-alpha"


def test_pilot_error_status_and_reason_remain_separately_queryable() -> None:
    _connection, service = _service()
    context = {"parser_match_id": "parser-match-1"}

    status = service.set_pilot_error_status(context, "yes")
    reason = service.set_pilot_error_reason(context, "synthetic sequencing reason")

    assert status["records"]["pilot_error_label"]["label_type"] == "pilot_error"
    assert status["records"]["pilot_error_label"]["label_value"] == "yes"
    assert reason["records"]["pilot_error_reason_label"]["label_type"] == "pilot_error_reason"
    assert reason["records"]["pilot_error_reason_label"]["label_value"] == "synthetic sequencing reason"

    labels = service.get_journal_bundle(context)["labels"]
    current_labels = {(label["label_type"], label["label_value"]) for label in labels if label["is_current"]}
    assert ("pilot_error", "yes") in current_labels
    assert ("pilot_error_reason", "synthetic sequencing reason") in current_labels


def test_pilot_error_review_prevalidates_and_creates_distinguishable_rows() -> None:
    connection, service = _service()

    with pytest.raises(MatchJournalServiceValidationError):
        service.record_pilot_error_review({"parser_match_id": "parser-match-1"}, status="maybe", note_text="Nope.")
    assert _count(connection, "journal_labels") == 0
    assert _count(connection, "journal_notes") == 0

    result = service.record_pilot_error_review(
        {"parser_match_id": "parser-match-1"},
        status="unknown",
        reason="synthetic uncertainty",
        note_text="Synthetic review note.",
    )

    assert result["records"]["pilot_error_label"]["label_type"] == "pilot_error"
    assert result["records"]["pilot_error_reason_label"]["label_type"] == "pilot_error_reason"
    assert result["records"]["note"]["note_scope"] == "match"


def test_opponent_labels_are_manual_and_non_inferred() -> None:
    _connection, service = _service()

    result = service.set_opponent_labels(
        {"parser_match_id": "parser-match-1"},
        archetype="Manual Synthetic Archetype",
        tier="Manual Tier 2",
    )

    assert result["records"]["opponent_archetype_label"]["label_type"] == "opponent_archetype"
    assert result["records"]["opponent_archetype_label"]["label_value"] == "Manual Synthetic Archetype"
    assert result["records"]["opponent_archetype_tier_label"]["label_type"] == "opponent_archetype_tier"
    assert result["records"]["opponent_archetype_tier_label"]["label_value"] == "Manual Tier 2"

    with pytest.raises(MatchJournalServiceValidationError):
        service.set_opponent_labels({"parser_match_id": "parser-match-1"})


def test_review_flags_are_local_review_metadata_only() -> None:
    _connection, service = _service()

    result = service.flag_for_review(
        {"parser_match_id": "parser-match-1"},
        "suspected_parser_gap",
        priority_label="high",
    )

    flag = result["records"]["review_flag"]
    assert flag["flag_type"] == "suspected_parser_gap"
    assert flag["flag_status"] == "open"
    assert flag["priority_label"] == "high"


def test_display_corrections_remain_journal_display_only() -> None:
    connection, service = _service()

    result = service.propose_display_correction(
        {"parser_match_id": "parser-match-1"},
        {
            "target_surface": "journal_display",
            "target_field": "review_summary",
            "original_value_label": "Parser display unchanged",
            "proposed_value_label": "Synthetic journal-only display",
            "override_reason": "Local review note.",
        },
    )

    override = result["records"]["field_override"]
    assert override["effect_scope"] == "journal_display_only"
    assert override["target_surface"] == "journal_display"

    with pytest.raises(MatchJournalServiceValidationError):
        service.propose_display_correction(
            {"parser_match_id": "parser-match-1"},
            {
                "target_surface": "journal_display",
                "target_field": "review_summary",
                "proposed_value_label": "Not allowed",
                "effect_scope": "parser_truth",
            },
        )
    assert _count(connection, "journal_field_overrides") == 1


def test_journal_bundle_reads_local_repository_data_only() -> None:
    _connection, service = _service()
    context = {"parser_match_id": "parser-match-1", "parser_game_id": "parser-game-1", "game_number": 1}
    service.record_game_note(context, "Synthetic game note.")
    service.set_pilot_error_status({"parser_match_id": "parser-match-1"}, "not_reviewed")
    service.flag_for_review({"parser_match_id": "parser-match-1"}, "needs_review")
    service.propose_display_correction(
        {"parser_match_id": "parser-match-1"},
        {
            "target_surface": "journal_display",
            "target_field": "review_summary",
            "proposed_value_label": "Synthetic display value",
        },
    )

    bundle = service.get_journal_bundle({"parser_match_id": "parser-match-1"})

    assert bundle is not None
    assert set(bundle) == {"match", "games", "notes", "labels", "review_flags", "field_overrides", "warnings"}
    assert bundle["match"]["parser_match_id"] == "parser-match-1"
    assert len(bundle["games"]) == 1
    assert len(bundle["notes"]) == 1
    assert len(bundle["labels"]) == 1
    assert len(bundle["review_flags"]) == 1
    assert len(bundle["field_overrides"]) == 1
    assert "analytics" not in bundle
    assert "openai" not in bundle
    assert service.get_journal_bundle({"parser_match_id": "missing-parser-match"}) is not None


def test_service_validation_failures_do_not_create_partial_rows() -> None:
    connection, service = _service()
    before = _journal_row_counts(connection)

    with pytest.raises(MatchJournalServiceValidationError):
        service.record_match_note({"parser_match_id": "parser-match-1", "raw_payload": "nope"}, "Nope.")
    with pytest.raises(MatchJournalServiceValidationError):
        service.record_unattached_note("   ")
    with pytest.raises(MatchJournalServiceValidationError):
        service.flag_for_review({"parser_match_id": "parser-match-1"}, "not_a_flag_type")
    with pytest.raises(MatchJournalServiceValidationError):
        service.flag_for_review({"parser_match_id": "parser-match-1"}, "needs_review", flag_status="not_allowed")
    with pytest.raises(MatchJournalServiceValidationError):
        service.set_experiment_label(
            {"parser_match_id": "parser-match-1"},
            "experiment-alpha",
            source_surface="not_allowed",
        )

    assert _journal_row_counts(connection) == before
    assert "journal_sheet_sync_queue" not in _table_names(connection)


def test_invalid_note_format_with_parser_context_does_not_create_partial_rows() -> None:
    connection, service = _service()
    before = _journal_row_counts(connection)

    with pytest.raises(MatchJournalServiceValidationError):
        service.record_match_note(
            {"parser_match_id": "parser-match-note"},
            "Synthetic note.",
            note_format="not_allowed",
        )

    assert _journal_row_counts(connection) == before


@pytest.mark.parametrize(
    "correction_request",
    (
        {
            "target_surface": "not_allowed",
            "target_field": "review_summary",
            "proposed_value_label": "Synthetic display value",
        },
        {
            "target_surface": "journal_display",
            "proposed_value_label": "Synthetic display value",
        },
        {
            "target_surface": "journal_display",
            "target_field": "review_summary",
        },
        {
            "target_surface": "journal_display",
            "target_field": "review_summary",
            "proposed_value_label": "Synthetic display value",
            "override_status": "not_allowed",
        },
    ),
)
def test_invalid_display_correction_with_parser_context_does_not_create_partial_rows(
    correction_request: dict[str, str],
) -> None:
    connection, service = _service()
    before = _journal_row_counts(connection)

    with pytest.raises(MatchJournalServiceValidationError):
        service.propose_display_correction({"parser_match_id": "parser-match-override"}, correction_request)

    assert _journal_row_counts(connection) == before
