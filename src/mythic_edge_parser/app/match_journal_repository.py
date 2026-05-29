from __future__ import annotations

import sqlite3
import uuid
from collections.abc import Callable, Iterable, Mapping
from datetime import UTC, datetime
from typing import Any

from mythic_edge_parser.app.match_journal_migration_loader import apply_match_journal_migrations

MATCH_JOURNAL_REPOSITORY_VERSION = "match_journal_repository.v1"

DEFAULT_AUTHOR_LABEL = "local_user"
DEFAULT_SOURCE_SURFACE = "manual"
DEFAULT_PRIVACY_LABEL = "local_private"
DEFAULT_REVIEW_STATUS = "not_reviewed"
DEFAULT_ATTACHMENT_STATUS = "unattached"
DEFAULT_NOTE_FORMAT = "plain_text"
DEFAULT_PRIORITY_LABEL = "normal"
DEFAULT_FLAG_STATUS = "open"
DEFAULT_FIELD_OVERRIDE_STATUS = "proposed"
JOURNAL_DISPLAY_ONLY = "journal_display_only"

SOURCE_SURFACES = frozenset({"manual", "imported_review", "local_tool", "test_fixture"})
PRIVACY_LABELS = frozenset({"local_private", "sanitized_fixture", "shareable_summary"})
ATTACHMENT_STATUSES = frozenset({"attached", "unattached", "pending", "ambiguous", "detached"})
REVIEW_STATUSES = frozenset({"not_reviewed", "needs_review", "reviewing", "reviewed", "archived"})
NOTE_SCOPES = frozenset({"match", "game", "sideboarding", "turn", "action", "general", "unattached"})
NOTE_FORMATS = frozenset({"plain_text", "markdown"})
LABEL_SCOPES = frozenset({"match", "game", "sideboarding", "review", "experiment", "opponent", "unattached"})
LABEL_TYPES = frozenset(
    {
        "matchup_label",
        "opponent_archetype",
        "opponent_archetype_tier",
        "experiment_id",
        "pilot_error",
        "pilot_error_reason",
        "review_status",
        "sideboarding_label",
        "custom",
    }
)
PILOT_ERROR_VALUES = frozenset({"yes", "no", "unknown", "not_reviewed"})
FLAG_TYPES = frozenset(
    {
        "needs_review",
        "interesting_match",
        "suspected_parser_gap",
        "sideboarding_review",
        "pilot_error_review",
        "custom",
    }
)
FLAG_STATUSES = frozenset({"open", "in_progress", "resolved", "dismissed", "archived"})
REFERENCE_TYPES = frozenset(
    {
        "review_status",
        "pilot_error_reason",
        "opponent_archetype_tier",
        "sideboarding_label",
        "experiment_id",
        "custom_label",
    }
)
TARGET_SURFACES = frozenset({"match_log_row", "game_log_row", "action_log_row", "analytics_view", "journal_display"})
FIELD_OVERRIDE_STATUSES = frozenset(
    {"proposed", "accepted_for_journal_display", "rejected", "superseded", "archived"}
)

MATCH_COLUMNS = frozenset(
    {
        "journal_match_id",
        "parser_match_id",
        "attachment_status",
        "title",
        "experiment_id",
        "review_status",
        "created_at",
        "updated_at",
        "author_label",
        "source_surface",
        "privacy_label",
    }
)
GAME_COLUMNS = frozenset(
    {
        "journal_game_id",
        "journal_match_id",
        "parser_match_id",
        "parser_game_id",
        "game_number",
        "attachment_status",
        "review_status",
        "created_at",
        "updated_at",
        "author_label",
        "source_surface",
        "privacy_label",
    }
)
NOTE_COLUMNS = frozenset(
    {
        "journal_note_id",
        "journal_match_id",
        "journal_game_id",
        "parser_match_id",
        "parser_game_id",
        "note_scope",
        "note_text",
        "note_format",
        "author_label",
        "source_surface",
        "privacy_label",
        "is_current",
        "supersedes_note_id",
        "valid_from",
        "valid_to",
        "created_at",
        "updated_at",
    }
)
LABEL_COLUMNS = frozenset(
    {
        "journal_label_id",
        "journal_match_id",
        "journal_game_id",
        "parser_match_id",
        "parser_game_id",
        "label_scope",
        "label_type",
        "label_value",
        "reference_id",
        "author_label",
        "source_surface",
        "privacy_label",
        "is_current",
        "valid_from",
        "valid_to",
        "created_at",
        "updated_at",
    }
)
REVIEW_FLAG_COLUMNS = frozenset(
    {
        "journal_review_flag_id",
        "journal_match_id",
        "journal_game_id",
        "parser_match_id",
        "parser_game_id",
        "flag_type",
        "flag_status",
        "priority_label",
        "reason",
        "author_label",
        "source_surface",
        "privacy_label",
        "created_at",
        "updated_at",
    }
)
REFERENCE_COLUMNS = frozenset(
    {"reference_id", "reference_type", "label", "description", "sort_order", "is_active", "created_at", "updated_at"}
)
FIELD_OVERRIDE_COLUMNS = frozenset(
    {
        "journal_field_override_id",
        "journal_match_id",
        "journal_game_id",
        "parser_match_id",
        "parser_game_id",
        "target_surface",
        "target_field",
        "original_value_label",
        "proposed_value_label",
        "override_reason",
        "override_status",
        "effect_scope",
        "author_label",
        "source_surface",
        "privacy_label",
        "created_at",
        "updated_at",
    }
)

Row = dict[str, Any]
IdFactory = Callable[[str], str]
Clock = Callable[[], str]


class MatchJournalRepositoryError(ValueError):
    """Base error for Match Journal repository validation and write failures."""


class MatchJournalValidationError(MatchJournalRepositoryError):
    """Raised when repository input violates the local Match Journal contract."""


class MatchJournalNotFoundError(MatchJournalRepositoryError):
    """Raised when a requested local Match Journal record does not exist."""


class MatchJournalConflictError(MatchJournalRepositoryError):
    """Raised when the caller-owned SQLite connection is not safe for a write."""


def ensure_match_journal_schema(connection: sqlite3.Connection, *, applied_at: str | None = None) -> None:
    """Apply the packaged Match Journal schema migrations to a caller-owned connection."""

    apply_match_journal_migrations(connection, applied_at=applied_at)


class MatchJournalRepository:
    """Small repository for local Match Journal rows.

    The repository owns no database path. Callers provide the SQLite connection,
    schema lifecycle, clock seam, and id seam explicitly.
    """

    def __init__(
        self,
        connection: sqlite3.Connection,
        *,
        id_factory: IdFactory | None = None,
        clock: Clock | None = None,
    ) -> None:
        self.connection = connection
        self.id_factory = id_factory or _default_id_factory
        self.clock = clock or _default_clock
        self.connection.execute("PRAGMA foreign_keys = ON")

    def create_match(self, values: Mapping[str, object] | None = None) -> Row:
        data = dict(values or {})
        timestamp = self._timestamp(data)
        row = {
            "journal_match_id": _optional_text(data, "journal_match_id") or self._new_id("journal_match"),
            "parser_match_id": _optional_text(data, "parser_match_id"),
            "attachment_status": _enum(
                data,
                "attachment_status",
                ATTACHMENT_STATUSES,
                default=DEFAULT_ATTACHMENT_STATUS,
            ),
            "title": _optional_text(data, "title"),
            "experiment_id": _optional_text(data, "experiment_id"),
            "review_status": _enum(data, "review_status", REVIEW_STATUSES, default=DEFAULT_REVIEW_STATUS),
            "created_at": _optional_text(data, "created_at") or timestamp,
            "updated_at": _optional_text(data, "updated_at") or timestamp,
            "author_label": _optional_text(data, "author_label") or DEFAULT_AUTHOR_LABEL,
            "source_surface": _enum(data, "source_surface", SOURCE_SURFACES, default=DEFAULT_SOURCE_SURFACE),
            "privacy_label": _enum(data, "privacy_label", PRIVACY_LABELS, default=DEFAULT_PRIVACY_LABEL),
        }
        _validate_attachment("match", row["attachment_status"], row["parser_match_id"])
        return self._write(lambda: self._insert_and_get("journal_matches", row, "journal_match_id"))

    def get_match(self, journal_match_id: str) -> Row | None:
        return self._fetch_by_id("journal_matches", "journal_match_id", journal_match_id)

    def list_matches(self, filters: Mapping[str, object] | None = None) -> tuple[Row, ...]:
        return self._list_rows(
            "journal_matches",
            MATCH_COLUMNS,
            filters,
            order_by=("created_at", "journal_match_id"),
        )

    def update_match(self, journal_match_id: str, values: Mapping[str, object]) -> Row:
        data = dict(values)
        updates = _pick_optional_text(data, ("parser_match_id", "title", "experiment_id", "author_label"))
        if "attachment_status" in data:
            updates["attachment_status"] = _enum(data, "attachment_status", ATTACHMENT_STATUSES)
        if "review_status" in data:
            updates["review_status"] = _enum(data, "review_status", REVIEW_STATUSES)
        if "source_surface" in data:
            updates["source_surface"] = _enum(data, "source_surface", SOURCE_SURFACES)
        if "privacy_label" in data:
            updates["privacy_label"] = _enum(data, "privacy_label", PRIVACY_LABELS)
        updates["updated_at"] = _optional_text(data, "updated_at") or self._now()

        existing = self._get_by_id("journal_matches", "journal_match_id", journal_match_id)
        next_attachment = updates.get("attachment_status", existing["attachment_status"])
        next_parser_id = updates.get("parser_match_id", existing["parser_match_id"])
        _validate_attachment("match", next_attachment, next_parser_id)
        return self._write(
            lambda: self._update_and_get("journal_matches", "journal_match_id", journal_match_id, updates)
        )

    def update_match_attachment(self, journal_match_id: str, values: Mapping[str, object]) -> Row:
        data = dict(values)
        updates = {
            "parser_match_id": _optional_text(data, "parser_match_id"),
            "attachment_status": _enum(data, "attachment_status", ATTACHMENT_STATUSES),
            "updated_at": _optional_text(data, "updated_at") or self._now(),
        }
        _validate_attachment("match", updates["attachment_status"], updates["parser_match_id"])
        return self._write(
            lambda: self._update_and_get("journal_matches", "journal_match_id", journal_match_id, updates)
        )

    def create_game(self, values: Mapping[str, object] | None = None) -> Row:
        data = dict(values or {})
        timestamp = self._timestamp(data)
        row = {
            "journal_game_id": _optional_text(data, "journal_game_id") or self._new_id("journal_game"),
            "journal_match_id": _optional_text(data, "journal_match_id"),
            "parser_match_id": _optional_text(data, "parser_match_id"),
            "parser_game_id": _optional_text(data, "parser_game_id"),
            "game_number": _optional_positive_int(data, "game_number"),
            "attachment_status": _enum(
                data,
                "attachment_status",
                ATTACHMENT_STATUSES,
                default=DEFAULT_ATTACHMENT_STATUS,
            ),
            "review_status": _enum(data, "review_status", REVIEW_STATUSES, default=DEFAULT_REVIEW_STATUS),
            "created_at": _optional_text(data, "created_at") or timestamp,
            "updated_at": _optional_text(data, "updated_at") or timestamp,
            "author_label": _optional_text(data, "author_label") or DEFAULT_AUTHOR_LABEL,
            "source_surface": _enum(data, "source_surface", SOURCE_SURFACES, default=DEFAULT_SOURCE_SURFACE),
            "privacy_label": _enum(data, "privacy_label", PRIVACY_LABELS, default=DEFAULT_PRIVACY_LABEL),
        }
        _validate_attachment("game", row["attachment_status"], row["parser_game_id"])
        return self._write(lambda: self._insert_and_get("journal_games", row, "journal_game_id"))

    def get_game(self, journal_game_id: str) -> Row | None:
        return self._fetch_by_id("journal_games", "journal_game_id", journal_game_id)

    def list_games(self, filters: Mapping[str, object] | None = None) -> tuple[Row, ...]:
        return self._list_rows("journal_games", GAME_COLUMNS, filters, order_by=("created_at", "journal_game_id"))

    def update_game(self, journal_game_id: str, values: Mapping[str, object]) -> Row:
        data = dict(values)
        updates = _pick_optional_text(
            data,
            ("journal_match_id", "parser_match_id", "parser_game_id", "author_label"),
        )
        if "game_number" in data:
            updates["game_number"] = _optional_positive_int(data, "game_number")
        if "attachment_status" in data:
            updates["attachment_status"] = _enum(data, "attachment_status", ATTACHMENT_STATUSES)
        if "review_status" in data:
            updates["review_status"] = _enum(data, "review_status", REVIEW_STATUSES)
        if "source_surface" in data:
            updates["source_surface"] = _enum(data, "source_surface", SOURCE_SURFACES)
        if "privacy_label" in data:
            updates["privacy_label"] = _enum(data, "privacy_label", PRIVACY_LABELS)
        updates["updated_at"] = _optional_text(data, "updated_at") or self._now()

        existing = self._get_by_id("journal_games", "journal_game_id", journal_game_id)
        next_attachment = updates.get("attachment_status", existing["attachment_status"])
        next_parser_id = updates.get("parser_game_id", existing["parser_game_id"])
        _validate_attachment("game", next_attachment, next_parser_id)
        return self._write(lambda: self._update_and_get("journal_games", "journal_game_id", journal_game_id, updates))

    def update_game_attachment(self, journal_game_id: str, values: Mapping[str, object]) -> Row:
        data = dict(values)
        updates = {
            "parser_match_id": _optional_text(data, "parser_match_id"),
            "parser_game_id": _optional_text(data, "parser_game_id"),
            "attachment_status": _enum(data, "attachment_status", ATTACHMENT_STATUSES),
            "updated_at": _optional_text(data, "updated_at") or self._now(),
        }
        _validate_attachment("game", updates["attachment_status"], updates["parser_game_id"])
        return self._write(lambda: self._update_and_get("journal_games", "journal_game_id", journal_game_id, updates))

    def create_note(self, values: Mapping[str, object]) -> Row:
        data = dict(values)
        timestamp = self._timestamp(data)
        row = {
            "journal_note_id": _optional_text(data, "journal_note_id") or self._new_id("journal_note"),
            "journal_match_id": _optional_text(data, "journal_match_id"),
            "journal_game_id": _optional_text(data, "journal_game_id"),
            "parser_match_id": _optional_text(data, "parser_match_id"),
            "parser_game_id": _optional_text(data, "parser_game_id"),
            "note_scope": _enum(data, "note_scope", NOTE_SCOPES),
            "note_text": _required_text(data, "note_text"),
            "note_format": _enum(data, "note_format", NOTE_FORMATS, default=DEFAULT_NOTE_FORMAT),
            "author_label": _optional_text(data, "author_label") or DEFAULT_AUTHOR_LABEL,
            "source_surface": _enum(data, "source_surface", SOURCE_SURFACES, default=DEFAULT_SOURCE_SURFACE),
            "privacy_label": _enum(data, "privacy_label", PRIVACY_LABELS, default=DEFAULT_PRIVACY_LABEL),
            "is_current": _optional_bool_int(data, "is_current", default=1),
            "supersedes_note_id": _optional_text(data, "supersedes_note_id"),
            "valid_from": _optional_text(data, "valid_from") or timestamp,
            "valid_to": _optional_text(data, "valid_to"),
            "created_at": _optional_text(data, "created_at") or timestamp,
            "updated_at": _optional_text(data, "updated_at") or timestamp,
        }
        return self._write(lambda: self._insert_and_get("journal_notes", row, "journal_note_id"))

    def get_note(self, journal_note_id: str) -> Row | None:
        return self._fetch_by_id("journal_notes", "journal_note_id", journal_note_id)

    def list_notes(self, filters: Mapping[str, object] | None = None) -> tuple[Row, ...]:
        return self._list_rows("journal_notes", NOTE_COLUMNS, filters, order_by=("created_at", "journal_note_id"))

    def supersede_note(self, journal_note_id: str, values: Mapping[str, object]) -> Row:
        existing = self._get_by_id("journal_notes", "journal_note_id", journal_note_id)
        data = dict(values)
        timestamp = self._timestamp(data)
        new_row = {
            "journal_note_id": _optional_text(data, "journal_note_id") or self._new_id("journal_note"),
            "journal_match_id": _optional_text(data, "journal_match_id")
            if "journal_match_id" in data
            else existing["journal_match_id"],
            "journal_game_id": _optional_text(data, "journal_game_id")
            if "journal_game_id" in data
            else existing["journal_game_id"],
            "parser_match_id": _optional_text(data, "parser_match_id")
            if "parser_match_id" in data
            else existing["parser_match_id"],
            "parser_game_id": _optional_text(data, "parser_game_id")
            if "parser_game_id" in data
            else existing["parser_game_id"],
            "note_scope": _enum(data, "note_scope", NOTE_SCOPES)
            if "note_scope" in data
            else existing["note_scope"],
            "note_text": _required_text(data, "note_text"),
            "note_format": _enum(data, "note_format", NOTE_FORMATS)
            if "note_format" in data
            else existing["note_format"],
            "author_label": _optional_text(data, "author_label") or existing["author_label"],
            "source_surface": _enum(data, "source_surface", SOURCE_SURFACES)
            if "source_surface" in data
            else existing["source_surface"],
            "privacy_label": _enum(data, "privacy_label", PRIVACY_LABELS)
            if "privacy_label" in data
            else existing["privacy_label"],
            "is_current": 1,
            "supersedes_note_id": existing["journal_note_id"],
            "valid_from": _optional_text(data, "valid_from") or timestamp,
            "valid_to": _optional_text(data, "valid_to"),
            "created_at": _optional_text(data, "created_at") or timestamp,
            "updated_at": _optional_text(data, "updated_at") or timestamp,
        }
        old_updates = {
            "is_current": 0,
            "valid_to": _optional_text(data, "old_valid_to") or new_row["valid_from"],
            "updated_at": _optional_text(data, "old_updated_at") or timestamp,
        }

        def write() -> Row:
            self._update_raw("journal_notes", "journal_note_id", journal_note_id, old_updates)
            return self._insert_and_get("journal_notes", new_row, "journal_note_id")

        return self._write(write)

    def set_current_label(self, values: Mapping[str, object]) -> Row:
        data = dict(values)
        timestamp = self._timestamp(data)
        label_type = _enum(data, "label_type", LABEL_TYPES)
        label_value = _required_text(data, "label_value")
        if label_type == "pilot_error" and label_value not in PILOT_ERROR_VALUES:
            raise MatchJournalValidationError("label_value is invalid for pilot_error")
        row = {
            "journal_label_id": _optional_text(data, "journal_label_id") or self._new_id("journal_label"),
            "journal_match_id": _optional_text(data, "journal_match_id"),
            "journal_game_id": _optional_text(data, "journal_game_id"),
            "parser_match_id": _optional_text(data, "parser_match_id"),
            "parser_game_id": _optional_text(data, "parser_game_id"),
            "label_scope": _enum(data, "label_scope", LABEL_SCOPES),
            "label_type": label_type,
            "label_value": label_value,
            "reference_id": _optional_text(data, "reference_id"),
            "author_label": _optional_text(data, "author_label") or DEFAULT_AUTHOR_LABEL,
            "source_surface": _enum(data, "source_surface", SOURCE_SURFACES, default=DEFAULT_SOURCE_SURFACE),
            "privacy_label": _enum(data, "privacy_label", PRIVACY_LABELS, default=DEFAULT_PRIVACY_LABEL),
            "is_current": 1,
            "valid_from": _optional_text(data, "valid_from") or timestamp,
            "valid_to": _optional_text(data, "valid_to"),
            "created_at": _optional_text(data, "created_at") or timestamp,
            "updated_at": _optional_text(data, "updated_at") or timestamp,
        }

        def write() -> Row:
            self.connection.execute(
                """
                UPDATE journal_labels
                   SET is_current = 0,
                       valid_to = ?,
                       updated_at = ?
                 WHERE is_current = 1
                   AND label_scope IS ?
                   AND label_type IS ?
                   AND journal_match_id IS ?
                   AND journal_game_id IS ?
                   AND parser_match_id IS ?
                   AND parser_game_id IS ?
                """,
                (
                    row["valid_from"],
                    row["updated_at"],
                    row["label_scope"],
                    row["label_type"],
                    row["journal_match_id"],
                    row["journal_game_id"],
                    row["parser_match_id"],
                    row["parser_game_id"],
                ),
            )
            return self._insert_and_get("journal_labels", row, "journal_label_id")

        return self._write(write)

    def get_label(self, journal_label_id: str) -> Row | None:
        return self._fetch_by_id("journal_labels", "journal_label_id", journal_label_id)

    def list_labels(self, filters: Mapping[str, object] | None = None) -> tuple[Row, ...]:
        return self._list_rows("journal_labels", LABEL_COLUMNS, filters, order_by=("created_at", "journal_label_id"))

    def create_review_flag(self, values: Mapping[str, object]) -> Row:
        data = dict(values)
        timestamp = self._timestamp(data)
        row = {
            "journal_review_flag_id": _optional_text(data, "journal_review_flag_id")
            or self._new_id("journal_review_flag"),
            "journal_match_id": _optional_text(data, "journal_match_id"),
            "journal_game_id": _optional_text(data, "journal_game_id"),
            "parser_match_id": _optional_text(data, "parser_match_id"),
            "parser_game_id": _optional_text(data, "parser_game_id"),
            "flag_type": _enum(data, "flag_type", FLAG_TYPES),
            "flag_status": _enum(data, "flag_status", FLAG_STATUSES, default=DEFAULT_FLAG_STATUS),
            "priority_label": _optional_text(data, "priority_label") or DEFAULT_PRIORITY_LABEL,
            "reason": _optional_text(data, "reason"),
            "author_label": _optional_text(data, "author_label") or DEFAULT_AUTHOR_LABEL,
            "source_surface": _enum(data, "source_surface", SOURCE_SURFACES, default=DEFAULT_SOURCE_SURFACE),
            "privacy_label": _enum(data, "privacy_label", PRIVACY_LABELS, default=DEFAULT_PRIVACY_LABEL),
            "created_at": _optional_text(data, "created_at") or timestamp,
            "updated_at": _optional_text(data, "updated_at") or timestamp,
        }
        return self._write(lambda: self._insert_and_get("journal_review_flags", row, "journal_review_flag_id"))

    def get_review_flag(self, journal_review_flag_id: str) -> Row | None:
        return self._fetch_by_id("journal_review_flags", "journal_review_flag_id", journal_review_flag_id)

    def list_review_flags(self, filters: Mapping[str, object] | None = None) -> tuple[Row, ...]:
        return self._list_rows(
            "journal_review_flags",
            REVIEW_FLAG_COLUMNS,
            filters,
            order_by=("created_at", "journal_review_flag_id"),
        )

    def update_review_flag(self, journal_review_flag_id: str, values: Mapping[str, object]) -> Row:
        data = dict(values)
        updates = _pick_optional_text(
            data,
            (
                "journal_match_id",
                "journal_game_id",
                "parser_match_id",
                "parser_game_id",
                "priority_label",
                "reason",
                "author_label",
            ),
        )
        if "flag_type" in data:
            updates["flag_type"] = _enum(data, "flag_type", FLAG_TYPES)
        if "flag_status" in data:
            updates["flag_status"] = _enum(data, "flag_status", FLAG_STATUSES)
        if "source_surface" in data:
            updates["source_surface"] = _enum(data, "source_surface", SOURCE_SURFACES)
        if "privacy_label" in data:
            updates["privacy_label"] = _enum(data, "privacy_label", PRIVACY_LABELS)
        updates["updated_at"] = _optional_text(data, "updated_at") or self._now()
        return self._write(
            lambda: self._update_and_get(
                "journal_review_flags",
                "journal_review_flag_id",
                journal_review_flag_id,
                updates,
            )
        )

    def upsert_reference_value(self, values: Mapping[str, object]) -> Row:
        data = dict(values)
        timestamp = self._timestamp(data)
        reference_id = _optional_text(data, "reference_id") or self._new_id("journal_reference")
        row = {
            "reference_id": reference_id,
            "reference_type": _enum(data, "reference_type", REFERENCE_TYPES),
            "label": _required_text(data, "label"),
            "description": _optional_text(data, "description"),
            "sort_order": _optional_int(data, "sort_order", default=0),
            "is_active": _optional_bool_int(data, "is_active", default=1),
            "created_at": _optional_text(data, "created_at") or timestamp,
            "updated_at": _optional_text(data, "updated_at") or timestamp,
        }

        def write() -> Row:
            existing = self._fetch_by_id("journal_reference_values", "reference_id", reference_id)
            if existing is None:
                return self._insert_and_get("journal_reference_values", row, "reference_id")
            updates = dict(row)
            updates.pop("reference_id")
            updates.pop("created_at")
            self._update_raw("journal_reference_values", "reference_id", reference_id, updates)
            return self._get_by_id("journal_reference_values", "reference_id", reference_id)

        return self._write(write)

    def get_reference_value(self, reference_id: str) -> Row | None:
        return self._fetch_by_id("journal_reference_values", "reference_id", reference_id)

    def list_reference_values(self, filters: Mapping[str, object] | None = None) -> tuple[Row, ...]:
        return self._list_rows(
            "journal_reference_values",
            REFERENCE_COLUMNS,
            filters,
            order_by=("sort_order", "label", "reference_id"),
        )

    def set_reference_value_active(self, reference_id: str, is_active: bool) -> Row:
        updates = {"is_active": 1 if is_active else 0, "updated_at": self._now()}
        return self._write(
            lambda: self._update_and_get("journal_reference_values", "reference_id", reference_id, updates)
        )

    def propose_field_override(self, values: Mapping[str, object]) -> Row:
        data = dict(values)
        timestamp = self._timestamp(data)
        effect_scope = _optional_text(data, "effect_scope") or JOURNAL_DISPLAY_ONLY
        _validate_effect_scope(effect_scope)
        row = {
            "journal_field_override_id": _optional_text(data, "journal_field_override_id")
            or self._new_id("journal_field_override"),
            "journal_match_id": _optional_text(data, "journal_match_id"),
            "journal_game_id": _optional_text(data, "journal_game_id"),
            "parser_match_id": _optional_text(data, "parser_match_id"),
            "parser_game_id": _optional_text(data, "parser_game_id"),
            "target_surface": _enum(data, "target_surface", TARGET_SURFACES),
            "target_field": _required_text(data, "target_field"),
            "original_value_label": _optional_text(data, "original_value_label"),
            "proposed_value_label": _required_text(data, "proposed_value_label"),
            "override_reason": _optional_text(data, "override_reason"),
            "override_status": _enum(
                data,
                "override_status",
                FIELD_OVERRIDE_STATUSES,
                default=DEFAULT_FIELD_OVERRIDE_STATUS,
            ),
            "effect_scope": effect_scope,
            "author_label": _optional_text(data, "author_label") or DEFAULT_AUTHOR_LABEL,
            "source_surface": _enum(data, "source_surface", SOURCE_SURFACES, default=DEFAULT_SOURCE_SURFACE),
            "privacy_label": _enum(data, "privacy_label", PRIVACY_LABELS, default=DEFAULT_PRIVACY_LABEL),
            "created_at": _optional_text(data, "created_at") or timestamp,
            "updated_at": _optional_text(data, "updated_at") or timestamp,
        }
        return self._write(
            lambda: self._insert_and_get("journal_field_overrides", row, "journal_field_override_id")
        )

    def get_field_override(self, journal_field_override_id: str) -> Row | None:
        return self._fetch_by_id("journal_field_overrides", "journal_field_override_id", journal_field_override_id)

    def list_field_overrides(self, filters: Mapping[str, object] | None = None) -> tuple[Row, ...]:
        return self._list_rows(
            "journal_field_overrides",
            FIELD_OVERRIDE_COLUMNS,
            filters,
            order_by=("created_at", "journal_field_override_id"),
        )

    def update_field_override_status(
        self,
        journal_field_override_id: str,
        values: Mapping[str, object] | str,
    ) -> Row:
        data: Mapping[str, object]
        if isinstance(values, str):
            data = {"override_status": values}
        else:
            data = values
        if "effect_scope" in data:
            _validate_effect_scope(_required_text(data, "effect_scope"))
        updates = {
            "override_status": _enum(data, "override_status", FIELD_OVERRIDE_STATUSES),
            "updated_at": _optional_text(data, "updated_at") or self._now(),
        }
        return self._write(
            lambda: self._update_and_get(
                "journal_field_overrides",
                "journal_field_override_id",
                journal_field_override_id,
                updates,
            )
        )

    def _timestamp(self, data: Mapping[str, object]) -> str:
        return _optional_text(data, "timestamp") or self._now()

    def _now(self) -> str:
        value = self.clock()
        if not isinstance(value, str) or not value.strip():
            raise MatchJournalValidationError("clock must return a non-empty string timestamp")
        return value

    def _new_id(self, prefix: str) -> str:
        value = self.id_factory(prefix)
        if not isinstance(value, str) or not value.strip():
            raise MatchJournalValidationError("id_factory must return a non-empty string id")
        return value

    def _write(self, operation: Callable[[], Row]) -> Row:
        if self.connection.in_transaction:
            raise MatchJournalConflictError(
                "Match Journal repository writes require a caller-owned connection without an open transaction"
            )
        try:
            self.connection.execute("BEGIN")
            row = operation()
            self.connection.commit()
            return row
        except MatchJournalRepositoryError:
            self.connection.rollback()
            raise
        except sqlite3.IntegrityError as exc:
            self.connection.rollback()
            raise MatchJournalRepositoryError("Match Journal write failed schema integrity checks") from exc
        except sqlite3.Error as exc:
            self.connection.rollback()
            raise MatchJournalRepositoryError("Match Journal write failed") from exc

    def _insert_and_get(self, table_name: str, row: Mapping[str, object], primary_key: str) -> Row:
        columns = tuple(row)
        placeholders = ", ".join("?" for _ in columns)
        column_sql = ", ".join(columns)
        self.connection.execute(
            f"INSERT INTO {table_name} ({column_sql}) VALUES ({placeholders})",
            tuple(row[column] for column in columns),
        )
        primary_value = _required_text(row, primary_key)
        return self._get_by_id(table_name, primary_key, primary_value)

    def _update_and_get(
        self,
        table_name: str,
        primary_key: str,
        primary_value: str,
        updates: Mapping[str, object],
    ) -> Row:
        self._update_raw(table_name, primary_key, primary_value, updates)
        return self._get_by_id(table_name, primary_key, primary_value)

    def _update_raw(
        self,
        table_name: str,
        primary_key: str,
        primary_value: str,
        updates: Mapping[str, object],
    ) -> None:
        normalized_id = _required_value(primary_key, primary_value)
        if not updates:
            raise MatchJournalValidationError("at least one update field is required")
        assignments = ", ".join(f"{column} = ?" for column in updates)
        cursor = self.connection.execute(
            f"UPDATE {table_name} SET {assignments} WHERE {primary_key} = ?",
            tuple(updates.values()) + (normalized_id,),
        )
        if cursor.rowcount == 0:
            raise MatchJournalNotFoundError(f"Match Journal row was not found in {table_name}")

    def _get_by_id(self, table_name: str, primary_key: str, primary_value: str) -> Row:
        row = self._fetch_by_id(table_name, primary_key, primary_value)
        if row is None:
            raise MatchJournalNotFoundError(f"Match Journal row was not found in {table_name}")
        return row

    def _fetch_by_id(self, table_name: str, primary_key: str, primary_value: str) -> Row | None:
        normalized_id = _required_value(primary_key, primary_value)
        cursor = self.connection.execute(f"SELECT * FROM {table_name} WHERE {primary_key} = ?", (normalized_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return _row_to_dict(cursor, row)

    def _list_rows(
        self,
        table_name: str,
        allowed_filters: frozenset[str],
        filters: Mapping[str, object] | None,
        *,
        order_by: Iterable[str],
    ) -> tuple[Row, ...]:
        where_sql, params = _where_clause(filters or {}, allowed_filters)
        order_sql = ", ".join(order_by)
        cursor = self.connection.execute(f"SELECT * FROM {table_name}{where_sql} ORDER BY {order_sql}", params)
        return tuple(_row_to_dict(cursor, row) for row in cursor.fetchall())


def _default_id_factory(prefix: str) -> str:
    return f"{prefix}:{uuid.uuid4().hex}"


def _default_clock() -> str:
    return datetime.now(UTC).isoformat()


def _required_value(name: str, value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MatchJournalValidationError(f"{name} is required")
    return value


def _required_text(values: Mapping[str, object], name: str) -> str:
    return _required_value(name, values.get(name))


def _optional_text(values: Mapping[str, object], name: str) -> str | None:
    if name not in values or values[name] is None:
        return None
    value = values[name]
    if not isinstance(value, str):
        raise MatchJournalValidationError(f"{name} must be a string")
    normalized = value.strip()
    if not normalized:
        return None
    return value


def _enum(
    values: Mapping[str, object],
    name: str,
    allowed: frozenset[str],
    *,
    default: str | None = None,
) -> str:
    value = _optional_text(values, name) if name in values else default
    if value is None:
        raise MatchJournalValidationError(f"{name} is required")
    if value not in allowed:
        raise MatchJournalValidationError(f"{name} is not an allowed Match Journal value")
    return value


def _optional_bool_int(values: Mapping[str, object], name: str, *, default: int | None = None) -> int | None:
    if name not in values or values[name] is None:
        return default
    value = values[name]
    if isinstance(value, bool):
        return 1 if value else 0
    if value in (0, 1):
        return int(value)
    raise MatchJournalValidationError(f"{name} must be a boolean or 0/1 integer")


def _optional_int(values: Mapping[str, object], name: str, *, default: int | None = None) -> int | None:
    if name not in values or values[name] is None:
        return default
    value = values[name]
    if isinstance(value, bool) or not isinstance(value, int):
        raise MatchJournalValidationError(f"{name} must be an integer")
    return value


def _optional_positive_int(values: Mapping[str, object], name: str) -> int | None:
    value = _optional_int(values, name)
    if value is None:
        return None
    if value <= 0:
        raise MatchJournalValidationError(f"{name} must be positive")
    return value


def _pick_optional_text(values: Mapping[str, object], names: Iterable[str]) -> dict[str, str | None]:
    return {name: _optional_text(values, name) for name in names if name in values}


def _validate_attachment(entity: str, attachment_status: object, parser_id: object) -> None:
    if attachment_status == "attached" and not parser_id:
        raise MatchJournalValidationError(f"attached {entity} rows require a parser id")


def _validate_effect_scope(effect_scope: str) -> None:
    if effect_scope != JOURNAL_DISPLAY_ONLY:
        raise MatchJournalValidationError("field overrides are limited to journal_display_only effect_scope")


def _where_clause(filters: Mapping[str, object], allowed_columns: frozenset[str]) -> tuple[str, tuple[object, ...]]:
    clauses: list[str] = []
    params: list[object] = []
    for column, value in filters.items():
        if column not in allowed_columns:
            raise MatchJournalValidationError(f"unsupported filter field: {column}")
        normalized_value = _normalize_filter_value(value)
        clauses.append(f"{column} IS ?")
        params.append(normalized_value)
    if not clauses:
        return "", ()
    return " WHERE " + " AND ".join(clauses), tuple(params)


def _normalize_filter_value(value: object) -> object:
    if isinstance(value, bool):
        return 1 if value else 0
    return value


def _row_to_dict(cursor: sqlite3.Cursor, row: object) -> Row:
    if isinstance(row, sqlite3.Row):
        return {key: row[key] for key in row.keys()}
    column_names = tuple(description[0] for description in cursor.description or ())
    return dict(zip(column_names, row, strict=True))
