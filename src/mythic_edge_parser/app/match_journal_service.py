from __future__ import annotations

import sqlite3
from collections.abc import Callable, Mapping
from typing import Any

from mythic_edge_parser.app.match_journal_repository import (
    FIELD_OVERRIDE_STATUSES,
    FLAG_STATUSES,
    NOTE_FORMATS,
    PRIVACY_LABELS,
    SOURCE_SURFACES,
    TARGET_SURFACES,
    MatchJournalConflictError,
    MatchJournalNotFoundError,
    MatchJournalRepository,
    MatchJournalRepositoryError,
    MatchJournalValidationError,
    ensure_match_journal_schema,
)

MATCH_JOURNAL_SERVICE_VERSION = "match_journal_service.v1"

ATTACHMENT_STATUSES = frozenset({"attached", "unattached", "pending", "ambiguous", "detached"})
COMMON_OPTION_FIELDS = frozenset(
    {
        "author_label",
        "source_surface",
        "privacy_label",
        "note_format",
        "priority_label",
        "reference_id",
        "created_at",
        "updated_at",
        "valid_from",
    }
)
CONTEXT_FIELDS = frozenset(
    {
        "journal_match_id",
        "journal_game_id",
        "parser_match_id",
        "parser_game_id",
        "game_number",
        "attachment_status",
    }
)
PILOT_ERROR_STATUSES = frozenset({"yes", "no", "unknown", "not_reviewed"})
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
JOURNAL_DISPLAY_ONLY = "journal_display_only"
DISPLAY_CORRECTION_FIELDS = frozenset(
    {
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
Result = dict[str, Any]


class MatchJournalServiceError(ValueError):
    """Base error for Match Journal service failures."""


class MatchJournalServiceValidationError(MatchJournalServiceError):
    """Raised when a service command is invalid."""


class MatchJournalServiceNotFoundError(MatchJournalServiceError):
    """Raised when caller-supplied journal IDs do not resolve."""


class MatchJournalServiceConflictError(MatchJournalServiceError):
    """Raised when caller-supplied context cannot be resolved unambiguously."""


class MatchJournalService:
    """Human-intent service boundary over the local Match Journal repository."""

    def __init__(self, repository: MatchJournalRepository) -> None:
        self.repository = repository

    @classmethod
    def from_connection(
        cls,
        connection: sqlite3.Connection,
        *,
        id_factory: Callable[[str], str] | None = None,
        clock: Callable[[], str] | None = None,
        ensure_schema: bool = False,
        applied_at: str | None = None,
    ) -> MatchJournalService:
        if ensure_schema:
            ensure_match_journal_schema(connection, applied_at=applied_at)
        return cls(MatchJournalRepository(connection, id_factory=id_factory, clock=clock))

    def record_match_note(
        self,
        context: Mapping[str, object] | None,
        note_text: str,
        **options: object,
    ) -> Result:
        note_text = _required_text_value("note_text", note_text)
        _validate_common_options(options)
        resolved = self._resolve_attachment_context(context, allow_create=True, prefer_game=False)
        note = self._create_note("match", note_text, resolved, options)
        return _completed(
            "record_match_note",
            "note",
            note["journal_note_id"],
            {"note": note, **resolved.records},
            resolved.warnings,
        )

    def record_game_note(
        self,
        context: Mapping[str, object] | None,
        note_text: str,
        **options: object,
    ) -> Result:
        note_text = _required_text_value("note_text", note_text)
        _validate_common_options(options)
        resolved = self._resolve_attachment_context(context, allow_create=True, prefer_game=True)
        note = self._create_note("game", note_text, resolved, options)
        return _completed(
            "record_game_note",
            "note",
            note["journal_note_id"],
            {"note": note, **resolved.records},
            resolved.warnings,
        )

    def record_sideboarding_note(
        self,
        context: Mapping[str, object] | None,
        note_text: str,
        **options: object,
    ) -> Result:
        note_text = _required_text_value("note_text", note_text)
        _validate_common_options(options)
        resolved = self._resolve_attachment_context(context, allow_create=True, prefer_game=True)
        note = self._create_note("sideboarding", note_text, resolved, options)
        return _completed(
            "record_sideboarding_note",
            "note",
            note["journal_note_id"],
            {"note": note, **resolved.records},
            resolved.warnings,
        )

    def record_unattached_note(self, note_text: str, **options: object) -> Result:
        note_text = _required_text_value("note_text", note_text)
        _validate_common_options(options)
        note = self._create_note("unattached", note_text, _ResolvedContext(), options)
        return _completed("record_unattached_note", "note", note["journal_note_id"], {"note": note}, ())

    def set_experiment_label(
        self,
        context: Mapping[str, object] | None,
        experiment_id: str,
        **options: object,
    ) -> Result:
        experiment_id = _required_text_value("experiment_id", experiment_id)
        _validate_common_options(options, include_note_format=False)
        resolved = self._resolve_attachment_context(context, allow_create=True, prefer_game=False)
        label = self._set_label("experiment", "experiment_id", experiment_id, resolved, options)
        records = {"experiment_label": label, **resolved.records}
        if resolved.journal_match_id:
            match = self._call_repo(
                lambda: self.repository.update_match(
                    resolved.journal_match_id,
                    {"experiment_id": experiment_id, **_common_row_options(options, include_note_format=False)},
                )
            )
            records["match"] = match
        return _completed(
            "set_experiment_label",
            "label",
            label["journal_label_id"],
            records,
            resolved.warnings,
        )

    def set_pilot_error_status(
        self,
        context: Mapping[str, object] | None,
        status: str,
        **options: object,
    ) -> Result:
        status = _required_text_value("status", status)
        if status not in PILOT_ERROR_STATUSES:
            raise MatchJournalServiceValidationError("status is not an allowed pilot-error value")
        _validate_common_options(options, include_note_format=False)
        resolved = self._resolve_attachment_context(context, allow_create=True, prefer_game=False)
        label = self._set_label("review", "pilot_error", status, resolved, options)
        return _completed(
            "set_pilot_error_status",
            "label",
            label["journal_label_id"],
            {"pilot_error_label": label, **resolved.records},
            resolved.warnings,
        )

    def set_pilot_error_reason(
        self,
        context: Mapping[str, object] | None,
        reason: str,
        **options: object,
    ) -> Result:
        reason = _required_text_value("reason", reason)
        _validate_common_options(options, include_note_format=False)
        resolved = self._resolve_attachment_context(context, allow_create=True, prefer_game=False)
        label = self._set_label("review", "pilot_error_reason", reason, resolved, options)
        return _completed(
            "set_pilot_error_reason",
            "label",
            label["journal_label_id"],
            {"pilot_error_reason_label": label, **resolved.records},
            resolved.warnings,
        )

    def set_opponent_labels(
        self,
        context: Mapping[str, object] | None,
        *,
        archetype: str | None = None,
        tier: str | None = None,
        **options: object,
    ) -> Result:
        archetype = _optional_non_empty_text("archetype", archetype)
        tier = _optional_non_empty_text("tier", tier)
        if archetype is None and tier is None:
            raise MatchJournalServiceValidationError("archetype or tier is required")
        _validate_common_options(options, include_note_format=False)
        resolved = self._resolve_attachment_context(context, allow_create=True, prefer_game=False)

        records: dict[str, Row] = dict(resolved.records)
        primary_id: str | None = None
        if archetype is not None:
            label = self._set_label("opponent", "opponent_archetype", archetype, resolved, options)
            records["opponent_archetype_label"] = label
            primary_id = primary_id or label["journal_label_id"]
        if tier is not None:
            label = self._set_label("opponent", "opponent_archetype_tier", tier, resolved, options)
            records["opponent_archetype_tier_label"] = label
            primary_id = primary_id or label["journal_label_id"]
        return _completed("set_opponent_labels", "label", primary_id, records, resolved.warnings)

    def record_pilot_error_review(
        self,
        context: Mapping[str, object] | None,
        *,
        status: str,
        reason: str | None = None,
        note_text: str | None = None,
        **options: object,
    ) -> Result:
        status = _required_text_value("status", status)
        if status not in PILOT_ERROR_STATUSES:
            raise MatchJournalServiceValidationError("status is not an allowed pilot-error value")
        reason = _optional_non_empty_text("reason", reason)
        note_text = _optional_non_empty_text("note_text", note_text)
        _validate_common_options(options, include_note_format=note_text is not None)
        resolved = self._resolve_attachment_context(context, allow_create=True, prefer_game=False)

        records: dict[str, Row] = dict(resolved.records)
        status_label = self._set_label("review", "pilot_error", status, resolved, options)
        records["pilot_error_label"] = status_label
        primary_type = "label"
        primary_id: str | None = status_label["journal_label_id"]

        if reason is not None:
            reason_label = self._set_label("review", "pilot_error_reason", reason, resolved, options)
            records["pilot_error_reason_label"] = reason_label
        if note_text is not None:
            note_scope = (
                "game"
                if resolved.journal_game_id
                else "match"
                if resolved.has_match_reference
                else "unattached"
            )
            note = self._create_note(note_scope, note_text, resolved, options)
            records["note"] = note
        return _completed("record_pilot_error_review", primary_type, primary_id, records, resolved.warnings)

    def flag_for_review(
        self,
        context: Mapping[str, object] | None,
        flag_type: str,
        **options: object,
    ) -> Result:
        flag_type = _required_text_value("flag_type", flag_type)
        if flag_type not in FLAG_TYPES:
            raise MatchJournalServiceValidationError("flag_type is not allowed")
        _validate_common_options(
            options,
            include_note_format=False,
            extra_allowed_fields=frozenset({"flag_status", "reason"}),
        )
        if "flag_status" in options:
            _validate_allowed_value("flag_status", options["flag_status"], FLAG_STATUSES)
        if "reason" in options:
            _optional_non_empty_text("reason", options["reason"])
        resolved = self._resolve_attachment_context(context, allow_create=True, prefer_game=True)
        request: dict[str, object] = {
            **resolved.attachment_fields,
            "flag_type": flag_type,
            **_common_row_options(options, include_note_format=False),
        }
        if "flag_status" in options:
            request["flag_status"] = options["flag_status"]
        if "priority_label" in options:
            request["priority_label"] = options["priority_label"]
        if "reason" in options:
            request["reason"] = options["reason"]
        flag = self._call_repo(lambda: self.repository.create_review_flag(request))
        return _completed(
            "flag_for_review",
            "review_flag",
            flag["journal_review_flag_id"],
            {"review_flag": flag, **resolved.records},
            resolved.warnings,
        )

    def propose_display_correction(
        self,
        context: Mapping[str, object] | None,
        request: Mapping[str, object],
    ) -> Result:
        data = dict(request)
        _validate_display_correction_request(data)
        resolved = self._resolve_attachment_context(context, allow_create=True, prefer_game=True)
        override_request = {**resolved.attachment_fields, **data, "effect_scope": JOURNAL_DISPLAY_ONLY}
        override = self._call_repo(lambda: self.repository.propose_field_override(override_request))
        return _completed(
            "propose_display_correction",
            "field_override",
            override["journal_field_override_id"],
            {"field_override": override, **resolved.records},
            resolved.warnings,
        )

    def get_journal_bundle(self, context: Mapping[str, object]) -> Mapping[str, object] | None:
        resolved = self._resolve_attachment_context(context, allow_create=False, prefer_game=True)
        filters = self._journal_bundle_filters(resolved)
        if filters is None:
            return None
        match = self._journal_bundle_match(resolved)
        return {
            "match": match,
            "games": self._call_repo(lambda: self.repository.list_games(filters)),
            "notes": self._call_repo(lambda: self.repository.list_notes(filters)),
            "labels": self._call_repo(lambda: self.repository.list_labels(filters)),
            "review_flags": self._call_repo(lambda: self.repository.list_review_flags(filters)),
            "field_overrides": self._call_repo(lambda: self.repository.list_field_overrides(filters)),
            "warnings": list(resolved.warnings),
        }

    def _journal_bundle_filters(self, resolved: _ResolvedContext) -> dict[str, object] | None:
        if resolved.journal_game_id:
            return {"journal_game_id": resolved.journal_game_id}
        if resolved.parser_game_id:
            return {"parser_game_id": resolved.parser_game_id}
        if resolved.journal_match_id:
            return {"journal_match_id": resolved.journal_match_id}
        if resolved.parser_match_id:
            return {"parser_match_id": resolved.parser_match_id}
        return None

    def _journal_bundle_match(self, resolved: _ResolvedContext) -> Row | None:
        if resolved.journal_match_id:
            return self._call_repo(lambda: self.repository.get_match(resolved.journal_match_id))
        if not resolved.parser_match_id:
            return None
        matches = self._call_repo(lambda: self.repository.list_matches({"parser_match_id": resolved.parser_match_id}))
        if len(matches) > 1:
            raise MatchJournalServiceConflictError("parser_match_id maps to multiple journal matches")
        if len(matches) == 1:
            return matches[0]
        return None

    def _resolve_attachment_context(
        self,
        context: Mapping[str, object] | None,
        *,
        allow_create: bool,
        prefer_game: bool,
    ) -> _ResolvedContext:
        if context is None:
            return _ResolvedContext(warnings=("no_attachment_context",))
        data = dict(context)
        _validate_options(data, CONTEXT_FIELDS)
        attachment_status = _attachment_status(data)
        resolved = _ResolvedContext(
            journal_match_id=_optional_non_empty_text("journal_match_id", data.get("journal_match_id")),
            journal_game_id=_optional_non_empty_text("journal_game_id", data.get("journal_game_id")),
            parser_match_id=_optional_non_empty_text("parser_match_id", data.get("parser_match_id")),
            parser_game_id=_optional_non_empty_text("parser_game_id", data.get("parser_game_id")),
            game_number=_optional_positive_int(data.get("game_number")),
        )

        if resolved.journal_match_id:
            match = self._require_match(resolved.journal_match_id)
            _ensure_parser_id_consistent("parser_match_id", resolved.parser_match_id, match.get("parser_match_id"))
            resolved = resolved.with_record("match", match).with_match(match)

        if resolved.journal_game_id:
            game = self._require_game(resolved.journal_game_id)
            _ensure_parser_id_consistent("parser_match_id", resolved.parser_match_id, game.get("parser_match_id"))
            _ensure_parser_id_consistent("parser_game_id", resolved.parser_game_id, game.get("parser_game_id"))
            resolved = resolved.with_record("game", game).with_game(game)
            if game.get("journal_match_id") and not resolved.journal_match_id:
                match = self._require_match(str(game["journal_match_id"]))
                resolved = resolved.with_record("match", match).with_match(match)

        if resolved.parser_match_id and not resolved.journal_match_id:
            match = self._resolve_match_by_parser_id(
                resolved.parser_match_id,
                allow_create=allow_create,
                attachment_status=attachment_status or "attached",
            )
            if match is not None:
                resolved = resolved.with_record("match", match).with_match(match)

        if prefer_game and resolved.parser_game_id and not resolved.journal_game_id:
            game = self._resolve_game_by_parser_id(
                resolved,
                allow_create=allow_create,
                attachment_status=attachment_status or "attached",
            )
            if game is not None:
                resolved = resolved.with_record("game", game).with_game(game)

        if attachment_status == "attached" and not (resolved.parser_match_id or resolved.parser_game_id):
            raise MatchJournalServiceValidationError("attached context requires a parser match or game id")
        return resolved

    def _resolve_match_by_parser_id(
        self,
        parser_match_id: str,
        *,
        allow_create: bool,
        attachment_status: str,
    ) -> Row | None:
        matches = self._call_repo(lambda: self.repository.list_matches({"parser_match_id": parser_match_id}))
        if len(matches) > 1:
            raise MatchJournalServiceConflictError("parser_match_id maps to multiple journal matches")
        if len(matches) == 1:
            return matches[0]
        if not allow_create:
            return None
        return self._call_repo(
            lambda: self.repository.create_match(
                {"parser_match_id": parser_match_id, "attachment_status": attachment_status}
            )
        )

    def _resolve_game_by_parser_id(
        self,
        resolved: _ResolvedContext,
        *,
        allow_create: bool,
        attachment_status: str,
    ) -> Row | None:
        if not resolved.parser_game_id:
            return None
        games = self._call_repo(lambda: self.repository.list_games({"parser_game_id": resolved.parser_game_id}))
        if len(games) > 1:
            raise MatchJournalServiceConflictError("parser_game_id maps to multiple journal games")
        if len(games) == 1:
            return games[0]
        if not allow_create:
            return None
        return self._call_repo(
            lambda: self.repository.create_game(
                {
                    "journal_match_id": resolved.journal_match_id,
                    "parser_match_id": resolved.parser_match_id,
                    "parser_game_id": resolved.parser_game_id,
                    "game_number": resolved.game_number,
                    "attachment_status": attachment_status,
                }
            )
        )

    def _require_match(self, journal_match_id: str) -> Row:
        match = self._call_repo(lambda: self.repository.get_match(journal_match_id))
        if match is None:
            raise MatchJournalServiceNotFoundError("journal_match_id was not found")
        return match

    def _require_game(self, journal_game_id: str) -> Row:
        game = self._call_repo(lambda: self.repository.get_game(journal_game_id))
        if game is None:
            raise MatchJournalServiceNotFoundError("journal_game_id was not found")
        return game

    def _create_note(
        self,
        note_scope: str,
        note_text: str,
        resolved: _ResolvedContext,
        options: Mapping[str, object],
    ) -> Row:
        request = {
            **resolved.attachment_fields,
            "note_scope": note_scope,
            "note_text": note_text,
            **_common_row_options(options),
        }
        return self._call_repo(lambda: self.repository.create_note(request))

    def _set_label(
        self,
        label_scope: str,
        label_type: str,
        label_value: str,
        resolved: _ResolvedContext,
        options: Mapping[str, object],
    ) -> Row:
        request = {
            **resolved.attachment_fields,
            "label_scope": label_scope,
            "label_type": label_type,
            "label_value": label_value,
            **_common_row_options(options, include_note_format=False),
        }
        if "reference_id" in options:
            request["reference_id"] = options["reference_id"]
        return self._call_repo(lambda: self.repository.set_current_label(request))

    def _call_repo(self, operation: Callable[[], Row | tuple[Row, ...] | None]) -> Any:
        try:
            return operation()
        except MatchJournalValidationError as exc:
            raise MatchJournalServiceValidationError(_safe_error_message(exc)) from exc
        except MatchJournalNotFoundError as exc:
            raise MatchJournalServiceNotFoundError(_safe_error_message(exc)) from exc
        except MatchJournalConflictError as exc:
            raise MatchJournalServiceConflictError(_safe_error_message(exc)) from exc
        except MatchJournalRepositoryError as exc:
            raise MatchJournalServiceError(_safe_error_message(exc)) from exc


class _ResolvedContext:
    def __init__(
        self,
        *,
        journal_match_id: str | None = None,
        journal_game_id: str | None = None,
        parser_match_id: str | None = None,
        parser_game_id: str | None = None,
        game_number: int | None = None,
        records: Mapping[str, Row] | None = None,
        warnings: tuple[str, ...] = (),
    ) -> None:
        self.journal_match_id = journal_match_id
        self.journal_game_id = journal_game_id
        self.parser_match_id = parser_match_id
        self.parser_game_id = parser_game_id
        self.game_number = game_number
        self.records = dict(records or {})
        self.warnings = warnings

    @property
    def has_match_reference(self) -> bool:
        return bool(self.journal_match_id or self.parser_match_id)

    @property
    def attachment_fields(self) -> dict[str, object]:
        fields: dict[str, object] = {}
        for name in ("journal_match_id", "journal_game_id", "parser_match_id", "parser_game_id"):
            value = getattr(self, name)
            if value:
                fields[name] = value
        return fields

    def with_record(self, name: str, row: Row) -> _ResolvedContext:
        return _ResolvedContext(
            journal_match_id=self.journal_match_id,
            journal_game_id=self.journal_game_id,
            parser_match_id=self.parser_match_id,
            parser_game_id=self.parser_game_id,
            game_number=self.game_number,
            records={**self.records, name: row},
            warnings=self.warnings,
        )

    def with_match(self, match: Mapping[str, object]) -> _ResolvedContext:
        return _ResolvedContext(
            journal_match_id=str(match["journal_match_id"]),
            journal_game_id=self.journal_game_id,
            parser_match_id=_coalesce_text(self.parser_match_id, match.get("parser_match_id")),
            parser_game_id=self.parser_game_id,
            game_number=self.game_number,
            records=self.records,
            warnings=self.warnings,
        )

    def with_game(self, game: Mapping[str, object]) -> _ResolvedContext:
        return _ResolvedContext(
            journal_match_id=_coalesce_text(self.journal_match_id, game.get("journal_match_id")),
            journal_game_id=str(game["journal_game_id"]),
            parser_match_id=_coalesce_text(self.parser_match_id, game.get("parser_match_id")),
            parser_game_id=_coalesce_text(self.parser_game_id, game.get("parser_game_id")),
            game_number=(
                self.game_number if self.game_number is not None else _optional_positive_int(game.get("game_number"))
            ),
            records=self.records,
            warnings=self.warnings,
        )


def _completed(
    action: str,
    primary_record_type: str,
    primary_record_id: object,
    records: Mapping[str, object],
    warnings: tuple[str, ...],
) -> Result:
    return {
        "action": action,
        "status": "completed",
        "primary_record_type": primary_record_type,
        "primary_record_id": primary_record_id,
        "records": dict(records),
        "warnings": list(warnings),
    }


def _common_row_options(
    options: Mapping[str, object],
    *,
    include_note_format: bool = True,
) -> dict[str, object]:
    names = {
        "author_label",
        "source_surface",
        "privacy_label",
        "created_at",
        "updated_at",
        "valid_from",
    }
    if include_note_format:
        names.add("note_format")
    return {name: options[name] for name in names if name in options}


def _attachment_status(data: Mapping[str, object]) -> str | None:
    if "attachment_status" not in data or data["attachment_status"] is None:
        return None
    status = _required_text_value("attachment_status", data["attachment_status"])
    if status not in ATTACHMENT_STATUSES:
        raise MatchJournalServiceValidationError("attachment_status is not allowed")
    return status


def _validate_common_options(
    values: Mapping[str, object],
    *,
    include_note_format: bool = True,
    extra_allowed_fields: frozenset[str] = frozenset(),
) -> None:
    _validate_options(values, COMMON_OPTION_FIELDS | extra_allowed_fields)
    _validate_common_option_values(values, include_note_format=include_note_format)


def _validate_common_option_values(
    values: Mapping[str, object],
    *,
    include_note_format: bool = True,
) -> None:
    for name in ("author_label", "priority_label", "reference_id", "created_at", "updated_at", "valid_from"):
        if name in values:
            _optional_non_empty_text(name, values[name])
    if "source_surface" in values:
        _validate_allowed_value("source_surface", values["source_surface"], SOURCE_SURFACES)
    if "privacy_label" in values:
        _validate_allowed_value("privacy_label", values["privacy_label"], PRIVACY_LABELS)
    if include_note_format and "note_format" in values:
        _validate_allowed_value("note_format", values["note_format"], NOTE_FORMATS)


def _validate_display_correction_request(values: Mapping[str, object]) -> None:
    _validate_options(values, DISPLAY_CORRECTION_FIELDS)
    _validate_allowed_value("target_surface", values.get("target_surface"), TARGET_SURFACES)
    _required_text_value("target_field", values.get("target_field"))
    if "original_value_label" in values:
        _optional_non_empty_text("original_value_label", values["original_value_label"])
    _required_text_value("proposed_value_label", values.get("proposed_value_label"))
    if "override_reason" in values:
        _optional_non_empty_text("override_reason", values["override_reason"])
    if "override_status" in values:
        _validate_allowed_value("override_status", values["override_status"], FIELD_OVERRIDE_STATUSES)
    if values.get("effect_scope", JOURNAL_DISPLAY_ONLY) != JOURNAL_DISPLAY_ONLY:
        raise MatchJournalServiceValidationError("display corrections are limited to journal_display_only")
    _validate_common_option_values(values, include_note_format=False)


def _validate_allowed_value(name: str, value: object, allowed_values: frozenset[str]) -> str:
    normalized = _required_text_value(name, value)
    if normalized not in allowed_values:
        raise MatchJournalServiceValidationError(f"{name} is not allowed")
    return normalized


def _validate_options(values: Mapping[str, object], allowed_fields: frozenset[str]) -> None:
    unsupported = sorted(set(values) - allowed_fields)
    if unsupported:
        raise MatchJournalServiceValidationError("unsupported service field")


def _ensure_parser_id_consistent(name: str, requested: object, existing: object) -> None:
    requested_text = _optional_non_empty_text(name, requested)
    existing_text = _optional_non_empty_text(name, existing)
    if requested_text and existing_text and requested_text != existing_text:
        raise MatchJournalServiceConflictError(f"{name} conflicts with the existing journal record")


def _required_text_value(name: str, value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MatchJournalServiceValidationError(f"{name} is required")
    return value


def _optional_non_empty_text(name: str, value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise MatchJournalServiceValidationError(f"{name} must be a string")
    if not value.strip():
        return None
    return value


def _optional_positive_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise MatchJournalServiceValidationError("game_number must be an integer")
    if value <= 0:
        raise MatchJournalServiceValidationError("game_number must be positive")
    return value


def _coalesce_text(primary: object, fallback: object) -> str | None:
    return _optional_non_empty_text("attachment_context_value", primary) or _optional_non_empty_text(
        "attachment_context_value",
        fallback,
    )


def _safe_error_message(exc: Exception) -> str:
    message = str(exc)
    if not message:
        return "Match Journal service operation failed"
    return message.splitlines()[0][:160]
