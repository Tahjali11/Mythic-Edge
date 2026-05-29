from __future__ import annotations

import sqlite3
from collections import Counter

import pytest

from mythic_edge_parser.app.match_journal_repository import (
    MATCH_JOURNAL_REPOSITORY_VERSION,
    MatchJournalConflictError,
    MatchJournalNotFoundError,
    MatchJournalRepository,
    MatchJournalValidationError,
    ensure_match_journal_schema,
)

APPLIED_AT = "2026-05-29T00:00:00+00:00"


class SequenceClock:
    def __init__(self) -> None:
        self.index = 0

    def __call__(self) -> str:
        self.index += 1
        return f"2026-05-29T00:00:{self.index:02d}+00:00"


class CountingIds:
    def __init__(self) -> None:
        self.counts: Counter[str] = Counter()

    def __call__(self, prefix: str) -> str:
        self.counts[prefix] += 1
        return f"{prefix}:generated:{self.counts[prefix]}"


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    ensure_match_journal_schema(connection, applied_at=APPLIED_AT)
    return connection


def _repo() -> tuple[sqlite3.Connection, MatchJournalRepository]:
    connection = _connect()
    return connection, MatchJournalRepository(connection, id_factory=CountingIds(), clock=SequenceClock())


def _count(connection: sqlite3.Connection, table_name: str) -> int:
    row = connection.execute(f"SELECT COUNT(*) AS count FROM {table_name}").fetchone()
    return int(row["count"])


def _names(connection: sqlite3.Connection) -> set[str]:
    rows = connection.execute("SELECT name FROM sqlite_schema WHERE type = 'table'").fetchall()
    return {str(row["name"]) for row in rows}


def test_repository_version_and_schema_helper_apply_existing_migrations() -> None:
    connection = _connect()

    assert MATCH_JOURNAL_REPOSITORY_VERSION == "match_journal_repository.v1"
    assert "journal_matches" in _names(connection)
    assert "journal_sheet_sync_queue" not in _names(connection)


@pytest.mark.parametrize(
    ("method_name", "missing_id"),
    [
        ("get_match", "missing-match"),
        ("get_game", "missing-game"),
        ("get_note", "missing-note"),
        ("get_label", "missing-label"),
        ("get_review_flag", "missing-flag"),
        ("get_reference_value", "missing-reference"),
        ("get_field_override", "missing-override"),
    ],
)
def test_missing_public_get_operations_return_none(method_name: str, missing_id: str) -> None:
    _connection, repo = _repo()

    assert getattr(repo, method_name)(missing_id) is None


def test_create_get_list_update_match_and_attachment_without_inventing_parser_ids() -> None:
    _connection, repo = _repo()

    match = repo.create_match({"title": "Synthetic review", "source_surface": "test_fixture"})

    assert match["journal_match_id"] == "journal_match:generated:1"
    assert match["parser_match_id"] is None
    assert match["attachment_status"] == "unattached"
    assert match["review_status"] == "not_reviewed"
    assert match["author_label"] == "local_user"
    assert match["privacy_label"] == "local_private"
    assert repo.get_match(match["journal_match_id"]) == match
    assert repo.list_matches({"attachment_status": "unattached"}) == (match,)

    updated = repo.update_match(
        match["journal_match_id"],
        {"review_status": "needs_review", "title": "Synthetic review pass"},
    )
    assert updated["title"] == "Synthetic review pass"
    assert updated["review_status"] == "needs_review"

    attached = repo.update_match_attachment(
        match["journal_match_id"],
        {"attachment_status": "attached", "parser_match_id": "parser-match-1"},
    )
    assert attached["attachment_status"] == "attached"
    assert attached["parser_match_id"] == "parser-match-1"

    with pytest.raises(MatchJournalValidationError):
        repo.create_match({"attachment_status": "attached"})


def test_create_get_list_update_game_and_attachment() -> None:
    _connection, repo = _repo()
    match = repo.create_match({"journal_match_id": "journal-match-1"})

    game = repo.create_game(
        {
            "journal_match_id": match["journal_match_id"],
            "game_number": 1,
            "source_surface": "local_tool",
        }
    )

    assert game["journal_game_id"] == "journal_game:generated:1"
    assert game["parser_game_id"] is None
    assert game["attachment_status"] == "unattached"
    assert repo.get_game(game["journal_game_id"]) == game
    assert repo.list_games({"journal_match_id": match["journal_match_id"]}) == (game,)

    updated = repo.update_game(game["journal_game_id"], {"game_number": 2, "review_status": "reviewing"})
    assert updated["game_number"] == 2
    assert updated["review_status"] == "reviewing"

    attached = repo.update_game_attachment(
        game["journal_game_id"],
        {
            "attachment_status": "attached",
            "parser_match_id": "parser-match-1",
            "parser_game_id": "parser-game-1",
        },
    )
    assert attached["attachment_status"] == "attached"
    assert attached["parser_game_id"] == "parser-game-1"

    with pytest.raises(MatchJournalValidationError):
        repo.update_game_attachment(game["journal_game_id"], {"attachment_status": "attached"})


def test_unattached_notes_are_preserved_and_can_be_superseded() -> None:
    _connection, repo = _repo()

    note = repo.create_note({"note_scope": "unattached", "note_text": "Review this synthetic note."})

    assert note["journal_note_id"] == "journal_note:generated:1"
    assert note["journal_match_id"] is None
    assert note["parser_match_id"] is None
    assert note["is_current"] == 1
    assert repo.list_notes({"note_scope": "unattached", "is_current": True}) == (note,)

    replacement = repo.supersede_note(note["journal_note_id"], {"note_text": "Updated synthetic note."})
    old_note = repo.get_note(note["journal_note_id"])

    assert old_note["is_current"] == 0
    assert old_note["valid_to"] == replacement["valid_from"]
    assert replacement["supersedes_note_id"] == note["journal_note_id"]
    assert replacement["is_current"] == 1
    assert replacement["note_text"] == "Updated synthetic note."

    with pytest.raises(MatchJournalNotFoundError):
        repo.supersede_note("missing-note", {"note_text": "No row."})


def test_set_current_label_expires_same_identity_without_merging_pilot_error_reason() -> None:
    _connection, repo = _repo()
    match = repo.create_match({"journal_match_id": "journal-match-1"})

    first = repo.set_current_label(
        {
            "journal_match_id": match["journal_match_id"],
            "label_scope": "match",
            "label_type": "matchup_label",
            "label_value": "synthetic-midrange",
        }
    )
    second = repo.set_current_label(
        {
            "journal_match_id": match["journal_match_id"],
            "label_scope": "match",
            "label_type": "matchup_label",
            "label_value": "synthetic-control",
        }
    )

    assert repo.get_label(first["journal_label_id"])["is_current"] == 0
    assert repo.get_label(second["journal_label_id"])["is_current"] == 1

    pilot_error = repo.set_current_label(
        {
            "journal_match_id": match["journal_match_id"],
            "label_scope": "review",
            "label_type": "pilot_error",
            "label_value": "yes",
        }
    )
    reason = repo.set_current_label(
        {
            "journal_match_id": match["journal_match_id"],
            "label_scope": "review",
            "label_type": "pilot_error_reason",
            "label_value": "synthetic sequencing note",
        }
    )
    assert repo.get_label(pilot_error["journal_label_id"])["is_current"] == 1
    assert repo.get_label(reason["journal_label_id"])["is_current"] == 1

    with pytest.raises(MatchJournalValidationError):
        repo.set_current_label(
            {
                "journal_match_id": match["journal_match_id"],
                "label_scope": "review",
                "label_type": "pilot_error",
                "label_value": "maybe",
            }
        )


def test_review_flags_are_local_review_metadata() -> None:
    _connection, repo = _repo()

    flag = repo.create_review_flag(
        {
            "parser_match_id": "parser-match-1",
            "flag_type": "suspected_parser_gap",
            "reason": "Synthetic review marker.",
        }
    )

    assert flag["journal_review_flag_id"] == "journal_review_flag:generated:1"
    assert flag["flag_status"] == "open"
    assert repo.list_review_flags({"flag_type": "suspected_parser_gap"}) == (flag,)

    updated = repo.update_review_flag(flag["journal_review_flag_id"], {"flag_status": "resolved"})
    assert updated["flag_status"] == "resolved"


def test_reference_values_upsert_and_active_filtering() -> None:
    _connection, repo = _repo()

    reference = repo.upsert_reference_value(
        {"reference_id": "ref:review:1", "reference_type": "review_status", "label": "Ready", "sort_order": 2}
    )
    assert reference["is_active"] == 1

    changed = repo.upsert_reference_value(
        {
            "reference_id": "ref:review:1",
            "reference_type": "review_status",
            "label": "Reviewed",
            "description": "Synthetic description.",
            "sort_order": 1,
        }
    )
    assert changed["label"] == "Reviewed"
    assert changed["created_at"] == reference["created_at"]

    inactive = repo.set_reference_value_active("ref:review:1", False)
    assert inactive["is_active"] == 0
    assert repo.list_reference_values({"is_active": False}) == (inactive,)
    assert repo.list_reference_values({"is_active": True}) == ()


def test_field_overrides_are_journal_display_only() -> None:
    connection, repo = _repo()

    override = repo.propose_field_override(
        {
            "target_surface": "journal_display",
            "target_field": "review_label",
            "proposed_value_label": "Synthetic journal label",
            "override_reason": "Local review only.",
        }
    )

    assert override["journal_field_override_id"] == "journal_field_override:generated:1"
    assert override["effect_scope"] == "journal_display_only"

    accepted = repo.update_field_override_status(
        override["journal_field_override_id"],
        {"override_status": "accepted_for_journal_display"},
    )
    assert accepted["override_status"] == "accepted_for_journal_display"

    with pytest.raises(MatchJournalValidationError):
        repo.propose_field_override(
            {
                "target_surface": "journal_display",
                "target_field": "review_label",
                "proposed_value_label": "Rejected boundary",
                "effect_scope": "parser_truth",
            }
        )
    assert _count(connection, "journal_field_overrides") == 1


def test_validation_failures_leave_no_partial_rows() -> None:
    connection, repo = _repo()

    with pytest.raises(MatchJournalValidationError):
        repo.create_note({"note_scope": "unattached"})
    with pytest.raises(MatchJournalValidationError):
        repo.create_match({"review_status": "ready_to_merge"})
    with pytest.raises(MatchJournalValidationError):
        repo.create_game({"game_number": 0})

    assert _count(connection, "journal_notes") == 0
    assert _count(connection, "journal_matches") == 0
    assert _count(connection, "journal_games") == 0


def test_missing_updates_and_unsupported_filters_raise_contract_errors() -> None:
    _connection, repo = _repo()

    with pytest.raises(MatchJournalNotFoundError):
        repo.update_match("missing-match", {"review_status": "reviewed"})
    with pytest.raises(MatchJournalNotFoundError):
        repo.update_game("missing-game", {"review_status": "reviewed"})
    with pytest.raises(MatchJournalNotFoundError):
        repo.update_review_flag("missing-flag", {"flag_status": "resolved"})
    with pytest.raises(MatchJournalNotFoundError):
        repo.set_reference_value_active("missing-reference", True)
    with pytest.raises(MatchJournalNotFoundError):
        repo.update_field_override_status("missing-override", "rejected")
    with pytest.raises(MatchJournalValidationError):
        repo.list_matches({"raw_payload": "not-supported"})


def test_write_operations_reject_caller_open_transactions() -> None:
    connection, repo = _repo()
    connection.execute("BEGIN")
    try:
        with pytest.raises(MatchJournalConflictError):
            repo.create_match({"title": "Open transaction should block writes."})
    finally:
        connection.rollback()

    assert _count(connection, "journal_matches") == 0
