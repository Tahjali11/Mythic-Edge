"""Metadata-only parser-owned fact capture tracker.

This module is a scoreboard for parser-owned fact capture progress. It builds
and validates public-safe target matrices, local session ledgers, and coverage
progress reports from supplied synthetic or already-sanitized metadata. It is
not a raw-log reader, fixture promoter, corpus mutator, parser behavior layer,
or readiness gate.
"""

from __future__ import annotations

import copy
import re
from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any

from mythic_edge_parser.app import field_recovery_matrix
from mythic_edge_parser.app.parser_owned_fact_tracker_schema import (
    AUTHORIZATION_FLAG_FIELDS,
    COMPETITIVE_SCOPES,
    COVERAGE_PROGRESS_REPORT_OBJECT,
    COVERAGE_PROGRESS_REPORT_SCHEMA_VERSION,
    DEFAULT_CREATED_AT_UTC,
    DEFAULT_LEDGER_ID,
    DEFAULT_MATRIX_ID,
    DEFAULT_REPORT_ID,
    DEFAULT_SCOPE,
    DEFERRED_REASONS,
    FACT_FAMILIES,
    FACT_REQUIRED_FIELDS,
    FACT_TARGET_MATRIX_OBJECT,
    FACT_TARGET_MATRIX_SCHEMA_VERSION,
    FORMAT_FAMILIES,
    LEDGER_REQUIRED_FIELDS,
    LIFECYCLE_STATUSES,
    MATCH_TYPES,
    MATRIX_REQUIRED_FIELDS,
    PARENT_PRIVATE_EVIDENCE_ISSUE,
    PIPELINE_TRACKER,
    PLATFORM_KEYS,
    PLATFORM_STATUSES,
    PRIORITIES,
    PRIVATE_SOURCE_KINDS,
    QUEUE_FAMILIES,
    READINESS_FLAG_FIELDS,
    REPORT_REQUIRED_FIELDS,
    REQUIRED_NON_CLAIMS,
    SESSION_CAPTURE_LEDGER_OBJECT,
    SESSION_CAPTURE_LEDGER_SCHEMA_VERSION,
    SESSION_REQUIRED_FIELDS,
    SOURCE_ISSUE,
    SOURCE_KINDS,
    TARGET_MATRIX_STATUSES,
)
from mythic_edge_parser.app.parser_owned_fact_tracker_schema import (
    CONTRACT_PATH as CONTRACT_PATH,
)
from mythic_edge_parser.app.parser_owned_fact_tracker_schema import (
    FALSE_FLAG_FIELDS as FALSE_FLAG_FIELDS,
)
from mythic_edge_parser.app.parser_owned_fact_tracker_schema import (
    SYNTHETIC_SOURCE_KINDS as SYNTHETIC_SOURCE_KINDS,
)

FACT_STATUS_REQUIRED_REF_FIELDS = {
    "candidate_generated": ("candidate_ids",),
    "review_packet_created": ("review_packet_ids",),
    "human_approved": ("review_packet_ids",),
    "promotion_proof_ready": ("promotion_proof_ids",),
    "fixture_manifest_draft_ready": ("fixture_draft_ids",),
    "promoted_golden_fixture": ("promoted_fixture_ids",),
    "confirmed_windows": ("promoted_fixture_ids",),
    "confirmed_macos": ("promoted_fixture_ids",),
    "confirmed_cross_platform": ("promoted_fixture_ids",),
}
ALLOWED_TRANSITIONS = {
    "not_captured": {
        "captured_private",
        "blocked_private_evidence",
        "blocked_external_boundary",
        "deferred_feature_expansion",
        "review_required",
    },
    "captured_private": {"candidate_generated", "review_required"},
    "candidate_generated": {"review_packet_created", "rejected_or_noisy", "review_required"},
    "review_packet_created": {"human_approved", "rejected_or_noisy", "review_required"},
    "human_approved": {"promotion_proof_ready", "review_required"},
    "promotion_proof_ready": {"fixture_manifest_draft_ready", "review_required"},
    "fixture_manifest_draft_ready": {"promoted_golden_fixture", "review_required"},
    "promoted_golden_fixture": {"confirmed_windows", "confirmed_macos", "review_required"},
    "confirmed_windows": {"confirmed_cross_platform", "review_required"},
    "confirmed_macos": {"confirmed_cross_platform", "review_required"},
    "confirmed_cross_platform": {"review_required"},
    "out_of_scope_now": {"review_required"},
    "deferred_feature_expansion": {"review_required"},
    "blocked_private_evidence": {"review_required"},
    "blocked_external_boundary": {"review_required"},
    "rejected_or_noisy": {"review_required"},
    "review_required": {"review_required", "invalid"},
    "invalid": set(),
}
SIDE_TRANSITIONS = {"review_required"}

SESSION_STATUS_REQUIRED_REF_FIELDS = {
    "candidate_generated": ("candidate_summary_refs",),
    "review_packet_created": ("review_packet_refs",),
    "human_approved": ("reviewer_decision_refs",),
    "promotion_proof_ready": ("promotion_proof_refs",),
    "fixture_manifest_draft_ready": ("fixture_draft_refs",),
    "promoted_golden_fixture": ("promoted_fixture_refs",),
    "confirmed_windows": ("promoted_fixture_refs",),
    "confirmed_macos": ("promoted_fixture_refs",),
    "confirmed_cross_platform": ("promoted_fixture_refs",),
}
SYMBOLIC_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
FACT_ID_RE = re.compile(r"^[a-z0-9_]+(?:\.[a-z0-9_]+)+$")
LOCAL_OR_PRIVATE_TEXT_RE = re.compile(
    r"(\[UnityCrossThreadLogger\]|\[Client GRE\]|DETAILED LOGS:|"
    r"\bPlayer\.log\b|\bUTC_Log\b|"
    r"https?://script\.google\.com|https?://hooks\.|"
    r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}|"
    r"\b(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{8,}|"
    r"(?:^|[^\w:/])(?:/(?:Applications|Users|Volumes|etc|home|opt|private|tmp|var)\b|"
    r"\b[A-Za-z]:[\\/]|\\\\))",
    re.IGNORECASE,
)
FORBIDDEN_KEY_RE = re.compile(
    r"(^|_)(raw|payload|payloads|content|text|line|lines|path|paths|hash|offset|offsets|bytes|"
    r"byte_range|file_size|timestamp_window|screenshot|workbook_export|sqlite|secret|token|api_key|"
    r"webhook_url)($|_)",
    re.IGNORECASE,
)
SAFE_KEY_ALLOWLIST = frozenset(
    {
        "source_issue",
        "source_kind",
        "source_window_ref",
        "source_matrix_refs",
        "source_field_recovery_matrix_row_ids",
        "parser_owner",
        "pipeline_tracker",
        "privacy",
        "privacy_scan",
        "privacy_status",
        "raw_private_values_included",
        "private_paths_included",
        "raw_log_excerpt_included",
        "secret_values_included",
        "privacy_scan_count",
        "privacy_finding_count",
        "private_harvest_authorized",
        "private_harvest_authorization",
        "parent_private_evidence_issue",
        "file_writing_authorized",
        "parser_behavior_ready",
        "pipeline_activation_ready_for_issue_388",
    }
)


class ParserOwnedFactTrackerError(ValueError):
    """Raised when tracker builders receive unsafe or invalid inputs."""


def build_default_fact_target_matrix(
    *,
    matrix_id: str = DEFAULT_MATRIX_ID,
    scope: str = DEFAULT_SCOPE,
    created_at_utc: str = DEFAULT_CREATED_AT_UTC,
) -> dict[str, Any]:
    """Build the seed target matrix from the reviewed field recovery matrix rows."""

    rows = [fact_row_from_recovery_row(row) for row in field_recovery_matrix.iter_field_recovery_rows()]
    matrix = {
        "object": FACT_TARGET_MATRIX_OBJECT,
        "schema_version": FACT_TARGET_MATRIX_SCHEMA_VERSION,
        "matrix_id": _symbolic_text(matrix_id, "matrix_id"),
        "scope": _member(scope, COMPETITIVE_SCOPES, "scope"),
        "target_matrix_status": "seed_matrix_ready",
        "created_at_utc": _utc_text(created_at_utc, "created_at_utc"),
        "source_issue": SOURCE_ISSUE,
        "pipeline_tracker": PIPELINE_TRACKER,
        "parent_private_evidence_issue": PARENT_PRIVATE_EVIDENCE_ISSUE,
        "source_matrix_refs": [
            {
                "ref_id": "field_recovery_matrix.default.v1",
                "object": field_recovery_matrix.FIELD_RECOVERY_MATRIX_OBJECT,
                "schema_version": field_recovery_matrix.FIELD_RECOVERY_MATRIX_SCHEMA_VERSION,
                "contract": "docs/contracts/parser_recovery_field_recovery_matrix.md",
                "status": "seed_rows_only",
            }
        ],
        "readiness_flags": _false_flags(READINESS_FLAG_FIELDS),
        "authorization_flags": _false_flags(AUTHORIZATION_FLAG_FIELDS),
        "facts": rows,
        "summary": _matrix_summary(rows),
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }
    errors = validate_fact_target_matrix(matrix)
    if errors:
        raise ParserOwnedFactTrackerError(f"default target matrix is invalid: {errors[0]}")
    return matrix


def fact_row_from_recovery_row(row: Mapping[str, Any]) -> dict[str, Any]:
    """Convert one field-recovery row into a parser-owned fact target row."""

    if not isinstance(row, Mapping):
        raise ParserOwnedFactTrackerError("recovery row must be a mapping")
    fact_id = _fact_id(str(row.get("field_id") or ""), "field_id")
    family = _member(str(row.get("field_family") or ""), FACT_FAMILIES, "field_family")
    competitive_scope, deferred_reason, lifecycle_status, platform_status = _scope_defaults(row)
    priority = _priority_for(row, competitive_scope, lifecycle_status)
    platform_requirements = _platform_requirements_for(competitive_scope)
    known_gaps = _known_gaps_for(row, competitive_scope, lifecycle_status)
    return {
        "fact_id": fact_id,
        "display_name": _public_text(str(row.get("display_name") or fact_id), "display_name"),
        "fact_family": family,
        "competitive_scope": competitive_scope,
        "deferred_reason": deferred_reason,
        "priority": priority,
        "parser_owner": _public_text(str(row.get("parser_owner") or "unknown"), "parser_owner"),
        "source_field_recovery_matrix_row_ids": [fact_id],
        "evidence_ledger_entry_ids": _symbolic_list(row.get("evidence_ledger_entry_ids"), "evidence_ledger_entry_ids"),
        "required_capture_evidence": _required_capture_evidence(row),
        "allowed_capture_sources": _allowed_capture_sources_for(competitive_scope, lifecycle_status),
        "forbidden_capture_sources": [
            "raw_private_log_content",
            "unapproved_private_source",
            "live_mtga_capture",
            "network_packet_capture",
            "workbook_export",
            "model_provider_output",
        ],
        "expected_outputs": _public_string_list(row.get("output_surfaces"), "expected_outputs"),
        "platform_requirements": platform_requirements,
        "current_lifecycle_status": lifecycle_status,
        "platform_status": platform_status,
        "candidate_ids": [],
        "review_packet_ids": [],
        "promotion_proof_ids": [],
        "fixture_draft_ids": [],
        "promoted_fixture_ids": [],
        "corpus_entry_ids": [],
        "known_gaps": known_gaps,
        "next_capture_target": _next_capture_target_for(fact_id, competitive_scope, lifecycle_status),
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }


def build_empty_session_capture_ledger(
    *,
    target_matrix_ref: str = DEFAULT_MATRIX_ID,
    ledger_id: str = DEFAULT_LEDGER_ID,
    scope: str = DEFAULT_SCOPE,
    updated_at_utc: str = DEFAULT_CREATED_AT_UTC,
) -> dict[str, Any]:
    """Build an empty public-safe session capture ledger."""

    ledger = {
        "object": SESSION_CAPTURE_LEDGER_OBJECT,
        "schema_version": SESSION_CAPTURE_LEDGER_SCHEMA_VERSION,
        "ledger_id": _symbolic_text(ledger_id, "ledger_id"),
        "scope": _member(scope, COMPETITIVE_SCOPES, "scope"),
        "updated_at_utc": _utc_text(updated_at_utc, "updated_at_utc"),
        "source_issue": SOURCE_ISSUE,
        "pipeline_tracker": PIPELINE_TRACKER,
        "parent_private_evidence_issue": PARENT_PRIVATE_EVIDENCE_ISSUE,
        "target_matrix_ref": _symbolic_text(target_matrix_ref, "target_matrix_ref"),
        "sessions": [],
        "summary": _ledger_summary([]),
        "privacy": _privacy_summary(),
        "readiness_flags": _false_flags(READINESS_FLAG_FIELDS),
        "authorization_flags": _false_flags(AUTHORIZATION_FLAG_FIELDS),
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }
    errors = validate_session_capture_ledger(ledger)
    if errors:
        raise ParserOwnedFactTrackerError(f"empty session ledger is invalid: {errors[0]}")
    return ledger


def record_capture_session(
    matrix: Mapping[str, Any],
    ledger: Mapping[str, Any],
    session_record: Mapping[str, Any],
) -> dict[str, Any]:
    """Append or replace one supplied session entry in a session capture ledger."""

    _raise_if_errors(validate_fact_target_matrix(matrix), "matrix")
    _raise_if_errors(validate_session_capture_ledger(ledger), "ledger")
    session_errors = validate_session_entry(session_record, matrix=matrix, ledger=ledger)
    if session_errors:
        raise ParserOwnedFactTrackerError(f"session record is invalid: {session_errors[0]}")
    session = copy.deepcopy(dict(session_record))
    sessions = [
        copy.deepcopy(existing)
        for existing in _as_sequence(ledger.get("sessions"))
        if isinstance(existing, Mapping) and existing.get("session_id") != session["session_id"]
    ]
    sessions.append(session)
    updated = copy.deepcopy(dict(ledger))
    updated["sessions"] = sessions
    updated["updated_at_utc"] = session["capture_finished_at_utc"] or session["capture_started_at_utc"] or (
        ledger.get("updated_at_utc") or DEFAULT_CREATED_AT_UTC
    )
    updated["summary"] = _ledger_summary(sessions)
    updated["privacy"] = _privacy_summary(sessions)
    errors = validate_session_capture_ledger(updated)
    if errors:
        raise ParserOwnedFactTrackerError(f"updated session ledger is invalid: {errors[0]}")
    return updated


def build_coverage_progress_report(
    matrix: Mapping[str, Any],
    ledger: Mapping[str, Any],
    *,
    previous_report: Mapping[str, Any] | None = None,
    report_id: str = DEFAULT_REPORT_ID,
    generated_at_utc: str = DEFAULT_CREATED_AT_UTC,
) -> dict[str, Any]:
    """Build a deterministic coverage progress report from a matrix and ledger."""

    _raise_if_errors(validate_fact_target_matrix(matrix), "matrix")
    _raise_if_errors(validate_session_capture_ledger(ledger), "ledger")
    if previous_report is not None:
        _raise_if_errors(validate_coverage_progress_report(previous_report), "previous_report")

    facts_by_id = _facts_by_id(matrix)
    latest_status = _latest_fact_statuses(matrix, ledger)
    platform_status = _latest_platform_statuses(matrix, ledger)
    sessions = [session for session in _as_sequence(ledger.get("sessions")) if isinstance(session, Mapping)]
    report = {
        "object": COVERAGE_PROGRESS_REPORT_OBJECT,
        "schema_version": COVERAGE_PROGRESS_REPORT_SCHEMA_VERSION,
        "report_id": _symbolic_text(report_id, "report_id"),
        "scope": matrix["scope"],
        "generated_at_utc": _utc_text(generated_at_utc, "generated_at_utc"),
        "target_matrix_ref": _symbolic_text(str(matrix.get("matrix_id") or DEFAULT_MATRIX_ID), "target_matrix_ref"),
        "session_capture_ledger_ref": _symbolic_text(str(ledger.get("ledger_id") or DEFAULT_LEDGER_ID), "ledger_ref"),
        "previous_report_ref": (
            _symbolic_text(str(previous_report.get("report_id")), "previous_report_ref") if previous_report else None
        ),
        "summary_counts": _report_summary_counts(matrix, latest_status, platform_status),
        "new_private_captures": _new_private_captures(sessions),
        "new_candidates_generated": _refs_for_status(sessions, "candidate_generated", "candidate_summary_refs"),
        "reviewer_decisions": _reviewer_decisions(sessions),
        "promotion_progress": _promotion_progress(sessions),
        "windows_only_confirmations": _platform_only_confirmations(platform_status, "windows"),
        "macos_only_confirmations": _platform_only_confirmations(platform_status, "macos"),
        "cross_platform_confirmations": sorted(
            fact_id for fact_id, status in latest_status.items() if status == "confirmed_cross_platform"
        ),
        "current_competitive_scope_gaps": _current_gaps(matrix, latest_status),
        "deferred_feature_expansion_facts": _deferred_facts(matrix),
        "next_recommended_capture_targets": _next_targets(matrix, latest_status, facts_by_id),
        "blocked_or_review_required": _blocked_or_review_required(matrix, latest_status),
        "privacy": _privacy_summary(sessions),
        "validation": {
            "matrix_valid": True,
            "ledger_valid": True,
            "previous_report_valid": previous_report is None or not validate_coverage_progress_report(previous_report),
            "raw_private_values_included": False,
            "parser_behavior_changed": False,
        },
        "readiness_flags": _false_flags(READINESS_FLAG_FIELDS),
        "authorization_flags": _false_flags(AUTHORIZATION_FLAG_FIELDS),
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }
    errors = validate_coverage_progress_report(report)
    if errors:
        raise ParserOwnedFactTrackerError(f"coverage report is invalid: {errors[0]}")
    return report


def validate_fact_target_matrix(matrix: Mapping[str, Any] | None) -> list[str]:
    """Return sanitized validation errors for a target matrix."""

    if not isinstance(matrix, Mapping):
        return ["matrix:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_fields(matrix, MATRIX_REQUIRED_FIELDS, "matrix"))
    errors.extend(_privacy_errors(matrix, "matrix"))
    if matrix.get("object") != FACT_TARGET_MATRIX_OBJECT:
        errors.append("matrix:invalid_object")
    if matrix.get("schema_version") != FACT_TARGET_MATRIX_SCHEMA_VERSION:
        errors.append("matrix:invalid_schema_version")
    if matrix.get("source_issue") != SOURCE_ISSUE:
        errors.append("matrix:invalid_source_issue")
    if matrix.get("pipeline_tracker") != PIPELINE_TRACKER:
        errors.append("matrix:invalid_pipeline_tracker")
    if matrix.get("parent_private_evidence_issue") != PARENT_PRIVATE_EVIDENCE_ISSUE:
        errors.append("matrix:invalid_parent_private_evidence_issue")
    _validate_member_field(matrix, "scope", COMPETITIVE_SCOPES, "matrix", errors)
    _validate_member_field(matrix, "target_matrix_status", TARGET_MATRIX_STATUSES, "matrix", errors)
    _validate_false_flag_group(matrix.get("readiness_flags"), READINESS_FLAG_FIELDS, "matrix:readiness_flags", errors)
    _validate_false_flag_group(
        matrix.get("authorization_flags"),
        AUTHORIZATION_FLAG_FIELDS,
        "matrix:authorization_flags",
        errors,
    )
    errors.extend(_validate_non_claims(matrix.get("non_claims"), "matrix:non_claims"))
    facts = matrix.get("facts")
    if not isinstance(facts, list):
        errors.append("matrix:facts_not_list")
    else:
        fact_ids: list[str] = []
        for index, fact in enumerate(facts):
            fact_errors = validate_fact_row(fact if isinstance(fact, Mapping) else {})
            errors.extend(f"matrix:facts[{index}]:{error}" for error in fact_errors)
            if isinstance(fact, Mapping) and isinstance(fact.get("fact_id"), str):
                fact_ids.append(fact["fact_id"])
        errors.extend(_duplicate_errors(fact_ids, "fact_id"))
        errors.extend(_validate_matrix_summary(matrix.get("summary"), facts))
    return _dedupe(errors)


def validate_fact_row(row: Mapping[str, Any]) -> list[str]:
    """Return sanitized validation errors for one fact target row."""

    if not isinstance(row, Mapping):
        return ["fact:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_fields(row, FACT_REQUIRED_FIELDS, "fact"))
    errors.extend(_privacy_errors(row, "fact"))
    fact_id = row.get("fact_id")
    if not isinstance(fact_id, str) or not FACT_ID_RE.fullmatch(fact_id):
        errors.append("fact:invalid_fact_id")
    _validate_member_field(row, "fact_family", FACT_FAMILIES, "fact", errors)
    _validate_member_field(row, "competitive_scope", COMPETITIVE_SCOPES, "fact", errors)
    _validate_member_field(row, "priority", PRIORITIES, "fact", errors)
    _validate_member_field(row, "current_lifecycle_status", LIFECYCLE_STATUSES, "fact", errors)
    if row.get("deferred_reason") is not None:
        _validate_member_field(row, "deferred_reason", DEFERRED_REASONS, "fact", errors)
    _validate_platform_map(row.get("platform_status"), "fact:platform_status", errors)
    _validate_platform_requirements(row.get("platform_requirements"), errors)
    for key in (
        "source_field_recovery_matrix_row_ids",
        "evidence_ledger_entry_ids",
        "required_capture_evidence",
        "allowed_capture_sources",
        "forbidden_capture_sources",
        "expected_outputs",
        "candidate_ids",
        "review_packet_ids",
        "promotion_proof_ids",
        "fixture_draft_ids",
        "promoted_fixture_ids",
        "corpus_entry_ids",
        "known_gaps",
    ):
        _validate_public_string_list(row.get(key), f"fact:{key}", errors)
    _validate_fact_status_refs(row, errors)
    for source_kind in _as_string_list(row.get("allowed_capture_sources")):
        if source_kind not in SOURCE_KINDS:
            errors.append(f"fact:allowed_capture_sources:unknown:{source_kind}")
    if row.get("competitive_scope") == "deferred_feature_expansion" and row.get("deferred_reason") in {
        None,
        "not_applicable",
    }:
        errors.append("fact:deferred_scope_requires_deferred_reason")
    if row.get("competitive_scope") == "competitive_current" and row.get("deferred_reason") not in {
        "not_applicable",
        "requires_private_evidence_approval",
        "requires_external_boundary_resolution",
    }:
        errors.append("fact:competitive_current_requires_not_applicable_deferred_reason")
    if row.get("current_lifecycle_status") == "confirmed_cross_platform":
        platform = row.get("platform_status")
        if (
            not isinstance(platform, Mapping)
            or platform.get("windows") != "confirmed"
            or platform.get("macos") != "confirmed"
        ):
            errors.append("fact:cross_platform_requires_windows_and_macos_confirmation")
    errors.extend(_validate_non_claims(row.get("non_claims"), "fact:non_claims"))
    return _dedupe(errors)


def validate_session_capture_ledger(ledger: Mapping[str, Any] | None) -> list[str]:
    """Return sanitized validation errors for a session capture ledger."""

    if not isinstance(ledger, Mapping):
        return ["ledger:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_fields(ledger, LEDGER_REQUIRED_FIELDS, "ledger"))
    errors.extend(_privacy_errors(ledger, "ledger"))
    if ledger.get("object") != SESSION_CAPTURE_LEDGER_OBJECT:
        errors.append("ledger:invalid_object")
    if ledger.get("schema_version") != SESSION_CAPTURE_LEDGER_SCHEMA_VERSION:
        errors.append("ledger:invalid_schema_version")
    if ledger.get("source_issue") != SOURCE_ISSUE:
        errors.append("ledger:invalid_source_issue")
    if ledger.get("pipeline_tracker") != PIPELINE_TRACKER:
        errors.append("ledger:invalid_pipeline_tracker")
    if ledger.get("parent_private_evidence_issue") != PARENT_PRIVATE_EVIDENCE_ISSUE:
        errors.append("ledger:invalid_parent_private_evidence_issue")
    _validate_member_field(ledger, "scope", COMPETITIVE_SCOPES, "ledger", errors)
    _validate_false_flag_group(ledger.get("readiness_flags"), READINESS_FLAG_FIELDS, "ledger:readiness_flags", errors)
    _validate_false_flag_group(
        ledger.get("authorization_flags"),
        AUTHORIZATION_FLAG_FIELDS,
        "ledger:authorization_flags",
        errors,
    )
    errors.extend(_validate_non_claims(ledger.get("non_claims"), "ledger:non_claims"))
    sessions = ledger.get("sessions")
    if not isinstance(sessions, list):
        errors.append("ledger:sessions_not_list")
    else:
        session_ids: list[str] = []
        for index, session in enumerate(sessions):
            session_errors = validate_session_entry(session if isinstance(session, Mapping) else {})
            errors.extend(f"ledger:sessions[{index}]:{error}" for error in session_errors)
            if isinstance(session, Mapping) and isinstance(session.get("session_id"), str):
                session_ids.append(session["session_id"])
        errors.extend(_duplicate_errors(session_ids, "session_id"))
        if ledger.get("summary") != _ledger_summary(sessions):
            errors.append("ledger:summary_mismatch")
        if ledger.get("privacy") != _privacy_summary(sessions):
            errors.append("ledger:privacy_summary_mismatch")
    return _dedupe(errors)


def validate_session_entry(
    session: Mapping[str, Any],
    *,
    matrix: Mapping[str, Any] | None = None,
    ledger: Mapping[str, Any] | None = None,
) -> list[str]:
    """Return sanitized validation errors for one session entry."""

    if not isinstance(session, Mapping):
        return ["session:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_fields(session, SESSION_REQUIRED_FIELDS, "session"))
    errors.extend(_privacy_errors(session, "session"))
    _validate_symbolic_field(session, "session_id", "session", errors)
    _validate_member_field(session, "platform", ("windows", "macos", "unknown"), "session", errors)
    _validate_member_field(session, "source_kind", SOURCE_KINDS, "session", errors)
    _validate_member_field(session, "scope", COMPETITIVE_SCOPES, "session", errors)
    _validate_member_field(session, "format_family", FORMAT_FAMILIES, "session", errors)
    _validate_member_field(session, "queue_family", QUEUE_FAMILIES, "session", errors)
    _validate_member_field(session, "match_type", MATCH_TYPES, "session", errors)
    for key in ("capture_started_at_utc", "capture_finished_at_utc"):
        if session.get(key) is not None and not _is_utc_text(session.get(key)):
            errors.append(f"session:{key}_not_utc")
    for key in (
        "candidate_summary_refs",
        "review_packet_refs",
        "reviewer_decision_refs",
        "promotion_proof_refs",
        "fixture_draft_refs",
        "promoted_fixture_refs",
        "remaining_targets",
    ):
        _validate_public_string_list(session.get(key), f"session:{key}", errors)
    if session.get("source_window_ref") is not None:
        _validate_symbolic_value(session.get("source_window_ref"), "session:source_window_ref", errors)
    _validate_false_flag_group(
        session.get("authorization_flags"),
        AUTHORIZATION_FLAG_FIELDS,
        "session:authorization_flags",
        errors,
    )
    errors.extend(_validate_non_claims(session.get("non_claims"), "session:non_claims"))
    _validate_session_privacy(session, errors)
    fact_ids = set(_facts_by_id(matrix or {}).keys()) if matrix else set()
    current_status = _latest_fact_statuses(matrix or {}, ledger or {}) if matrix else {}
    deltas = session.get("fact_deltas")
    if not isinstance(deltas, list):
        errors.append("session:fact_deltas_not_list")
    else:
        seen_delta_ids: set[str] = set()
        for index, delta in enumerate(deltas):
            delta_errors = _validate_fact_delta(
                delta if isinstance(delta, Mapping) else {},
                fact_ids=fact_ids,
                current_status=current_status,
            )
            if isinstance(delta, Mapping):
                delta_errors.extend(_validate_session_delta_refs(session, delta))
            errors.extend(f"session:fact_deltas[{index}]:{error}" for error in delta_errors)
            if isinstance(delta, Mapping) and isinstance(delta.get("fact_id"), str):
                seen_delta_ids.add(delta["fact_id"])
    if session.get("source_kind") in PRIVATE_SOURCE_KINDS:
        deltas_for_private = session.get("fact_deltas") if isinstance(session.get("fact_deltas"), list) else []
        if not any(
            isinstance(delta, Mapping)
            and delta.get("to_status") in {"captured_private", "blocked_private_evidence"}
            for delta in deltas_for_private
        ):
            errors.append("session:private_source_kind_requires_private_or_blocked_delta")
    return _dedupe(errors)


def validate_coverage_progress_report(report: Mapping[str, Any] | None) -> list[str]:
    """Return sanitized validation errors for a coverage progress report."""

    if not isinstance(report, Mapping):
        return ["report:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_fields(report, REPORT_REQUIRED_FIELDS, "report"))
    errors.extend(_privacy_errors(report, "report"))
    if report.get("object") != COVERAGE_PROGRESS_REPORT_OBJECT:
        errors.append("report:invalid_object")
    if report.get("schema_version") != COVERAGE_PROGRESS_REPORT_SCHEMA_VERSION:
        errors.append("report:invalid_schema_version")
    _validate_member_field(report, "scope", COMPETITIVE_SCOPES, "report", errors)
    _validate_false_flag_group(report.get("readiness_flags"), READINESS_FLAG_FIELDS, "report:readiness_flags", errors)
    _validate_false_flag_group(
        report.get("authorization_flags"),
        AUTHORIZATION_FLAG_FIELDS,
        "report:authorization_flags",
        errors,
    )
    errors.extend(_validate_non_claims(report.get("non_claims"), "report:non_claims"))
    for key in (
        "new_private_captures",
        "new_candidates_generated",
        "windows_only_confirmations",
        "macos_only_confirmations",
        "cross_platform_confirmations",
        "current_competitive_scope_gaps",
        "deferred_feature_expansion_facts",
        "next_recommended_capture_targets",
        "blocked_or_review_required",
    ):
        _validate_public_string_list(report.get(key), f"report:{key}", errors)
    if not isinstance(report.get("summary_counts"), Mapping):
        errors.append("report:summary_counts_not_mapping")
    if not isinstance(report.get("reviewer_decisions"), Mapping):
        errors.append("report:reviewer_decisions_not_mapping")
    if not isinstance(report.get("promotion_progress"), Mapping):
        errors.append("report:promotion_progress_not_mapping")
    validation = report.get("validation")
    if not isinstance(validation, Mapping):
        errors.append("report:validation_not_mapping")
    else:
        for key in ("raw_private_values_included", "parser_behavior_changed"):
            if validation.get(key) is not False:
                errors.append(f"report:validation:{key}_must_remain_false")
    return _dedupe(errors)


def _scope_defaults(row: Mapping[str, Any]) -> tuple[str, str, str, dict[str, str]]:
    category = str(row.get("recovery_category") or "")
    family = str(row.get("field_family") or "")
    if category == "approximate_analytics_only" or family == "analytics":
        return "support_only", "analytics_only_support", "out_of_scope_now", _not_required_platforms()
    if category == "unavailable" or family == "deck_state":
        return (
            "deferred_feature_expansion",
            "requires_future_contract",
            "deferred_feature_expansion",
            _not_required_platforms(),
        )
    if category == "blocked_private_evidence":
        return "competitive_current", "requires_private_evidence_approval", "blocked_private_evidence", {
            "windows": "blocked_private_evidence",
            "macos": "blocked_private_evidence",
            "cross_platform": "blocked_private_evidence",
        }
    if category == "blocked_external_boundary":
        return "competitive_current", "requires_external_boundary_resolution", "blocked_external_boundary", {
            "windows": "blocked_external_boundary",
            "macos": "blocked_external_boundary",
            "cross_platform": "blocked_external_boundary",
        }
    if category == "review_required":
        return "competitive_current", "not_applicable", "review_required", _not_captured_platforms()
    return "competitive_current", "not_applicable", "not_captured", _not_captured_platforms()


def _priority_for(row: Mapping[str, Any], scope: str, status: str) -> str:
    if scope == "deferred_feature_expansion":
        return "deferred"
    if status in {"blocked_private_evidence", "blocked_external_boundary", "review_required"}:
        return "medium"
    if row.get("field_family") in {"match", "game", "queue"}:
        return "critical"
    if row.get("field_family") in {"gameplay_action", "runtime_health"}:
        return "high"
    return "medium"


def _platform_requirements_for(scope: str) -> dict[str, str]:
    if scope == "competitive_current":
        return {"windows": "required", "macos": "required", "cross_platform": "required"}
    return {"windows": "not_required", "macos": "not_required", "cross_platform": "not_required"}


def _not_required_platforms() -> dict[str, str]:
    return {"windows": "not_required", "macos": "not_required", "cross_platform": "not_required"}


def _not_captured_platforms() -> dict[str, str]:
    return {"windows": "not_captured", "macos": "not_captured", "cross_platform": "not_captured"}


def _required_capture_evidence(row: Mapping[str, Any]) -> list[str]:
    direct = _as_string_list(row.get("required_direct_evidence"))
    if direct:
        return direct
    fallback = _as_string_list(row.get("allowed_fallback_evidence"))
    return fallback or ["reviewed_public_safe_metadata"]


def _allowed_capture_sources_for(scope: str, status: str) -> list[str]:
    if scope in {"support_only", "out_of_scope_now", "deferred_feature_expansion"}:
        return ["synthetic_fixture"]
    if status in {"blocked_private_evidence", "blocked_external_boundary"}:
        return ["synthetic_fixture", "local_harvest_candidate_summary", "harvest_review_packet"]
    return [
        "synthetic_fixture",
        "synthetic_player_log",
        "synthetic_utc_log",
        "local_harvest_candidate_summary",
        "harvest_review_packet",
        "fixture_promotion_proof",
        "golden_replay_fixture_manifest_draft",
        "corpus_metadata_diff",
    ]


def _known_gaps_for(row: Mapping[str, Any], scope: str, status: str) -> list[str]:
    if scope == "support_only":
        return ["analytics_support_not_parser_truth"]
    if scope == "deferred_feature_expansion":
        return ["future_contract_required"]
    if status == "blocked_private_evidence":
        return ["private_evidence_approval_required"]
    if status == "blocked_external_boundary":
        return ["external_boundary_resolution_required"]
    if status == "review_required":
        return ["review_required_before_capture_campaign"]
    return ["synthetic_or_private_capture_missing"]


def _next_capture_target_for(fact_id: str, scope: str, status: str) -> str:
    if scope == "deferred_feature_expansion":
        return f"{fact_id}:deferred"
    if status.startswith("blocked_"):
        return f"{fact_id}:{status}"
    if status == "review_required":
        return f"{fact_id}:review-required"
    return f"{fact_id}:next-synthetic-or-private-candidate"


def _matrix_summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "fact_count": len(rows),
        "scope_counts": _counter_by(rows, "competitive_scope"),
        "family_counts": _counter_by(rows, "fact_family"),
        "lifecycle_counts": _counter_by(rows, "current_lifecycle_status"),
        "platform_counts": {
            platform: _counter(row.get("platform_status", {}).get(platform) for row in rows)
            for platform in PLATFORM_KEYS
        },
        "summary_is_readiness_metric": False,
    }


def _ledger_summary(sessions: Sequence[Any]) -> dict[str, Any]:
    valid_sessions = [session for session in sessions if isinstance(session, Mapping)]
    deltas = [
        delta
        for session in valid_sessions
        for delta in _as_sequence(session.get("fact_deltas"))
        if isinstance(delta, Mapping)
    ]
    return {
        "session_count": len(valid_sessions),
        "fact_delta_count": len(deltas),
        "source_kind_counts": _counter(session.get("source_kind") for session in valid_sessions),
        "platform_counts": _counter(session.get("platform") for session in valid_sessions),
        "lifecycle_to_status_counts": _counter(delta.get("to_status") for delta in deltas),
        "summary_is_readiness_metric": False,
    }


def _privacy_summary(sessions: Sequence[Any] | None = None) -> dict[str, Any]:
    scan_count = 0
    finding_count = 0
    for session in sessions or ():
        if not isinstance(session, Mapping):
            continue
        scan = session.get("privacy_scan")
        if isinstance(scan, Mapping):
            scan_count += 1
            findings = scan.get("findings")
            if isinstance(findings, list):
                finding_count += len(findings)
    return {
        "raw_private_values_included": False,
        "private_paths_included": False,
        "raw_log_excerpt_included": False,
        "secret_values_included": False,
        "privacy_scan_count": scan_count,
        "privacy_finding_count": finding_count,
    }


def _report_summary_counts(
    matrix: Mapping[str, Any],
    latest_status: Mapping[str, str],
    platform_status: Mapping[str, Mapping[str, str]],
) -> dict[str, Any]:
    facts = [fact for fact in _as_sequence(matrix.get("facts")) if isinstance(fact, Mapping)]
    competitive = [fact for fact in facts if fact.get("competitive_scope") == "competitive_current"]
    ready_statuses = {"promoted_golden_fixture", "confirmed_windows", "confirmed_macos", "confirmed_cross_platform"}
    return {
        "fact_count": len(facts),
        "competitive_current_fact_count": len(competitive),
        "deferred_feature_expansion_fact_count": sum(
            1 for fact in facts if fact.get("competitive_scope") == "deferred_feature_expansion"
        ),
        "support_only_fact_count": sum(1 for fact in facts if fact.get("competitive_scope") == "support_only"),
        "not_captured_fact_count": sum(1 for status in latest_status.values() if status == "not_captured"),
        "blocked_private_evidence_fact_count": sum(
            1 for status in latest_status.values() if status == "blocked_private_evidence"
        ),
        "blocked_external_boundary_fact_count": sum(
            1 for status in latest_status.values() if status == "blocked_external_boundary"
        ),
        "review_required_fact_count": sum(1 for status in latest_status.values() if status == "review_required"),
        "synthetic_or_private_progress_fact_count": sum(
            1
            for status in latest_status.values()
            if status in {"captured_private", "candidate_generated", "review_packet_created", "human_approved"}
        ),
        "promotion_progress_fact_count": sum(
            1
            for status in latest_status.values()
            if status in {"promotion_proof_ready", "fixture_manifest_draft_ready", "promoted_golden_fixture"}
        ),
        "parser_behavior_ready_fact_count": 0,
        "pipeline_activation_ready_fact_count": 0,
        "covered_or_confirmed_fact_count": sum(1 for status in latest_status.values() if status in ready_statuses),
        "windows_confirmed_fact_count": sum(
            1 for status_by_platform in platform_status.values() if status_by_platform.get("windows") == "confirmed"
        ),
        "macos_confirmed_fact_count": sum(
            1 for status_by_platform in platform_status.values() if status_by_platform.get("macos") == "confirmed"
        ),
        "cross_platform_confirmed_fact_count": sum(
            1
            for fact_id, status in latest_status.items()
            if status == "confirmed_cross_platform"
            or platform_status.get(fact_id, {}).get("cross_platform") == "confirmed"
        ),
        "summary_is_readiness_metric": False,
    }


def _new_private_captures(sessions: Sequence[Mapping[str, Any]]) -> list[str]:
    refs: list[str] = []
    for session in sessions:
        if not isinstance(session, Mapping):
            continue
        for delta in _as_sequence(session.get("fact_deltas")):
            if isinstance(delta, Mapping) and delta.get("to_status") == "captured_private":
                refs.append(f"{session.get('session_id')}:{delta.get('fact_id')}")
    return sorted(_dedupe(refs))


def _refs_for_status(
    sessions: Sequence[Mapping[str, Any]],
    status: str,
    refs_key: str,
) -> list[str]:
    refs: list[str] = []
    for session in sessions:
        if not isinstance(session, Mapping):
            continue
        if any(
            isinstance(delta, Mapping) and delta.get("to_status") == status
            for delta in _as_sequence(session.get("fact_deltas"))
        ):
            refs.extend(_as_string_list(session.get(refs_key)))
    return sorted(_dedupe(refs))


def _reviewer_decisions(sessions: Sequence[Mapping[str, Any]]) -> dict[str, list[str]]:
    decisions: dict[str, list[str]] = {"approved": [], "rejected_or_noisy": [], "review_required": []}
    for session in sessions:
        if not isinstance(session, Mapping):
            continue
        refs = _as_string_list(session.get("reviewer_decision_refs"))
        for delta in _as_sequence(session.get("fact_deltas")):
            if not isinstance(delta, Mapping):
                continue
            status = str(delta.get("to_status") or "")
            if status == "human_approved":
                decisions["approved"].extend(refs or [f"{session.get('session_id')}:{delta.get('fact_id')}"])
            elif status == "rejected_or_noisy":
                decisions["rejected_or_noisy"].extend(refs or [f"{session.get('session_id')}:{delta.get('fact_id')}"])
            elif status == "review_required":
                decisions["review_required"].extend(refs or [f"{session.get('session_id')}:{delta.get('fact_id')}"])
    return {key: sorted(_dedupe(value)) for key, value in decisions.items()}


def _promotion_progress(sessions: Sequence[Mapping[str, Any]]) -> dict[str, list[str]]:
    progress = {
        "promotion_proof_ready": [],
        "fixture_manifest_draft_ready": [],
        "promoted_golden_fixture": [],
    }
    ref_keys = {
        "promotion_proof_ready": "promotion_proof_refs",
        "fixture_manifest_draft_ready": "fixture_draft_refs",
        "promoted_golden_fixture": "promoted_fixture_refs",
    }
    for session in sessions:
        if not isinstance(session, Mapping):
            continue
        for delta in _as_sequence(session.get("fact_deltas")):
            if not isinstance(delta, Mapping):
                continue
            status = str(delta.get("to_status") or "")
            if status in progress:
                refs = _as_string_list(session.get(ref_keys[status]))
                progress[status].extend(refs or [f"{session.get('session_id')}:{delta.get('fact_id')}"])
    return {key: sorted(_dedupe(value)) for key, value in progress.items()}


def _platform_only_confirmations(
    platform_status: Mapping[str, Mapping[str, str]],
    platform: str,
) -> list[str]:
    other = "macos" if platform == "windows" else "windows"
    return sorted(
        fact_id
        for fact_id, status_by_platform in platform_status.items()
        if status_by_platform.get(platform) == "confirmed"
        and status_by_platform.get(other) != "confirmed"
        and status_by_platform.get("cross_platform") != "confirmed"
    )


def _current_gaps(matrix: Mapping[str, Any], latest_status: Mapping[str, str]) -> list[str]:
    gaps: list[str] = []
    for fact in _as_sequence(matrix.get("facts")):
        if not isinstance(fact, Mapping):
            continue
        fact_id = str(fact.get("fact_id") or "")
        if fact.get("competitive_scope") != "competitive_current":
            continue
        if latest_status.get(fact_id) in {"not_captured", "captured_private", "candidate_generated"}:
            gaps.append(fact_id)
    return sorted(gaps)


def _deferred_facts(matrix: Mapping[str, Any]) -> list[str]:
    return sorted(
        str(fact.get("fact_id"))
        for fact in _as_sequence(matrix.get("facts"))
        if isinstance(fact, Mapping) and fact.get("competitive_scope") == "deferred_feature_expansion"
    )


def _next_targets(
    matrix: Mapping[str, Any],
    latest_status: Mapping[str, str],
    facts_by_id: Mapping[str, Mapping[str, Any]],
) -> list[str]:
    targets: list[str] = []
    for fact_id, fact in facts_by_id.items():
        if fact.get("competitive_scope") != "competitive_current":
            continue
        if latest_status.get(fact_id) in {
            "not_captured",
            "captured_private",
            "candidate_generated",
            "review_packet_created",
            "human_approved",
            "promotion_proof_ready",
            "fixture_manifest_draft_ready",
        }:
            targets.append(str(fact.get("next_capture_target") or f"{fact_id}:next"))
    if not targets:
        targets = [
            str(fact.get("next_capture_target") or f"{fact.get('fact_id')}:next")
            for fact in _as_sequence(matrix.get("facts"))
            if isinstance(fact, Mapping) and fact.get("competitive_scope") == "competitive_current"
        ][:5]
    return sorted(_dedupe(targets))


def _blocked_or_review_required(matrix: Mapping[str, Any], latest_status: Mapping[str, str]) -> list[str]:
    return sorted(
        fact_id
        for fact_id in _facts_by_id(matrix)
        if latest_status.get(fact_id)
        in {"blocked_private_evidence", "blocked_external_boundary", "review_required", "invalid"}
    )


def _latest_fact_statuses(
    matrix: Mapping[str, Any],
    ledger: Mapping[str, Any] | None = None,
) -> dict[str, str]:
    status = {
        str(fact.get("fact_id")): str(fact.get("current_lifecycle_status"))
        for fact in _as_sequence(matrix.get("facts"))
        if isinstance(fact, Mapping) and isinstance(fact.get("fact_id"), str)
    }
    for session in _as_sequence((ledger or {}).get("sessions")):
        if not isinstance(session, Mapping):
            continue
        for delta in _as_sequence(session.get("fact_deltas")):
            if isinstance(delta, Mapping) and isinstance(delta.get("fact_id"), str):
                status[delta["fact_id"]] = str(delta.get("to_status") or status.get(delta["fact_id"]))
    return status


def _latest_platform_statuses(
    matrix: Mapping[str, Any],
    ledger: Mapping[str, Any] | None = None,
) -> dict[str, dict[str, str]]:
    statuses = {
        str(fact.get("fact_id")): dict(fact.get("platform_status") or {})
        for fact in _as_sequence(matrix.get("facts"))
        if isinstance(fact, Mapping) and isinstance(fact.get("fact_id"), str)
    }
    for session in _as_sequence((ledger or {}).get("sessions")):
        if not isinstance(session, Mapping):
            continue
        platform = str(session.get("platform") or "")
        for delta in _as_sequence(session.get("fact_deltas")):
            if not isinstance(delta, Mapping) or not isinstance(delta.get("fact_id"), str):
                continue
            fact_platform = statuses.setdefault(delta["fact_id"], _not_captured_platforms())
            to_status = str(delta.get("to_status") or "")
            if platform in {"windows", "macos"} and to_status in {
                "captured_private",
                "candidate_generated",
                "review_packet_created",
                "human_approved",
                "promoted_golden_fixture",
                "confirmed_windows",
                "confirmed_macos",
                "confirmed_cross_platform",
            }:
                fact_platform[platform] = "confirmed" if to_status.startswith("confirmed_") else to_status
            if to_status == "confirmed_cross_platform":
                fact_platform["windows"] = "confirmed"
                fact_platform["macos"] = "confirmed"
                fact_platform["cross_platform"] = "confirmed"
    return statuses


def _validate_matrix_summary(summary: Any, facts: Sequence[Any]) -> list[str]:
    if not isinstance(summary, Mapping):
        return ["matrix:summary_not_mapping"]
    expected = _matrix_summary([fact for fact in facts if isinstance(fact, Mapping)])
    if summary != expected:
        return ["matrix:summary_mismatch"]
    return []


def _validate_platform_map(value: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(value, Mapping):
        errors.append(f"{prefix}_not_mapping")
        return
    for platform in PLATFORM_KEYS:
        status = value.get(platform)
        if status not in PLATFORM_STATUSES:
            errors.append(f"{prefix}:{platform}_invalid")


def _validate_platform_requirements(value: Any, errors: list[str]) -> None:
    if not isinstance(value, Mapping):
        errors.append("fact:platform_requirements_not_mapping")
        return
    for platform in PLATFORM_KEYS:
        if value.get(platform) not in {"required", "not_required"}:
            errors.append(f"fact:platform_requirements:{platform}_invalid")


def _validate_fact_delta(
    delta: Mapping[str, Any],
    *,
    fact_ids: set[str],
    current_status: Mapping[str, str],
) -> list[str]:
    errors: list[str] = []
    errors.extend(_privacy_errors(delta, "delta"))
    for key in ("fact_id", "from_status", "to_status", "evidence_ref", "rationale"):
        if key not in delta:
            errors.append(f"delta:missing_{key}")
    fact_id = delta.get("fact_id")
    if not isinstance(fact_id, str) or not FACT_ID_RE.fullmatch(fact_id):
        errors.append("delta:invalid_fact_id")
    elif fact_ids and fact_id not in fact_ids:
        errors.append("delta:unknown_fact_id")
    from_status = delta.get("from_status")
    to_status = delta.get("to_status")
    if from_status not in LIFECYCLE_STATUSES:
        errors.append("delta:invalid_from_status")
    if to_status not in LIFECYCLE_STATUSES:
        errors.append("delta:invalid_to_status")
    if fact_id in current_status and from_status != current_status[fact_id]:
        errors.append("delta:from_status_does_not_match_current_status")
    if isinstance(from_status, str) and isinstance(to_status, str) and not _transition_allowed(from_status, to_status):
        errors.append("delta:forbidden_lifecycle_transition")
    for key in ("evidence_ref", "rationale"):
        if key in delta and delta[key] is not None:
            _validate_symbolic_value(delta[key], f"delta:{key}", errors)
    return _dedupe(errors)


def _validate_fact_status_refs(row: Mapping[str, Any], errors: list[str]) -> None:
    status = row.get("current_lifecycle_status")
    for ref_field in FACT_STATUS_REQUIRED_REF_FIELDS.get(status, ()):
        refs = row.get(ref_field)
        if not isinstance(refs, list) or not refs:
            errors.append(f"fact:lifecycle_status:{status}_requires_{ref_field}")


def _validate_session_delta_refs(
    session: Mapping[str, Any],
    delta: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    status = delta.get("to_status")
    for ref_field in SESSION_STATUS_REQUIRED_REF_FIELDS.get(status, ()):
        refs = session.get(ref_field)
        if not isinstance(refs, list) or not refs:
            errors.append(f"delta:{status}_requires_{ref_field}")
    return errors


def _transition_allowed(from_status: str, to_status: str) -> bool:
    if from_status == to_status:
        return True
    return to_status in ALLOWED_TRANSITIONS.get(from_status, set()) or to_status in SIDE_TRANSITIONS


def _validate_session_privacy(session: Mapping[str, Any], errors: list[str]) -> None:
    scan = session.get("privacy_scan")
    if not isinstance(scan, Mapping):
        errors.append("session:privacy_scan_not_mapping")
        return
    if scan.get("raw_private_values_included") is not False:
        errors.append("session:privacy_scan:raw_private_values_included_must_remain_false")
    if scan.get("private_paths_included") is not False:
        errors.append("session:privacy_scan:private_paths_included_must_remain_false")
    if scan.get("secret_values_included") is not False:
        errors.append("session:privacy_scan:secret_values_included_must_remain_false")
    findings = scan.get("findings", [])
    if not isinstance(findings, list):
        errors.append("session:privacy_scan:findings_not_list")
    else:
        _validate_public_string_list(findings, "session:privacy_scan:findings", errors)
        if findings:
            errors.append("session:privacy_scan:findings_present")


def _validate_false_flag_group(
    value: Any,
    expected_fields: Sequence[str],
    prefix: str,
    errors: list[str],
) -> None:
    if not isinstance(value, Mapping):
        errors.append(f"{prefix}_not_mapping")
        return
    for flag in expected_fields:
        if flag not in value:
            errors.append(f"{prefix}:{flag}_missing")
        elif value.get(flag) is not False:
            errors.append(f"{prefix}:{flag}_must_remain_false")


def _validate_non_claims(value: Any, prefix: str) -> list[str]:
    if not isinstance(value, list):
        return [f"{prefix}_not_list"]
    if value != list(REQUIRED_NON_CLAIMS):
        return [f"{prefix}:mismatch"]
    return []


def _validate_public_string_list(value: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{prefix}_not_list")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str):
            errors.append(f"{prefix}[{index}]_not_string")
        elif LOCAL_OR_PRIVATE_TEXT_RE.search(item):
            errors.append(f"privacy:forbidden_text:{prefix}[{index}]")


def _validate_symbolic_field(mapping: Mapping[str, Any], key: str, prefix: str, errors: list[str]) -> None:
    if key not in mapping:
        return
    _validate_symbolic_value(mapping.get(key), f"{prefix}:{key}", errors)


def _validate_symbolic_value(value: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{prefix}_not_string")
    elif not SYMBOLIC_ID_RE.fullmatch(value):
        errors.append(f"{prefix}_not_symbolic")


def _validate_member_field(
    mapping: Mapping[str, Any],
    key: str,
    allowed: Sequence[str],
    prefix: str,
    errors: list[str],
) -> None:
    if key not in mapping:
        return
    if mapping.get(key) not in allowed:
        errors.append(f"{prefix}:invalid_{key}")


def _privacy_errors(value: Any, prefix: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            item_prefix = f"{prefix}.{key_text}"
            if FORBIDDEN_KEY_RE.search(key_text) and key_text not in SAFE_KEY_ALLOWLIST:
                errors.append(f"privacy:forbidden_key:{item_prefix}")
            errors.extend(_privacy_errors(item, item_prefix))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(_privacy_errors(item, f"{prefix}[{index}]"))
    elif isinstance(value, str) and LOCAL_OR_PRIVATE_TEXT_RE.search(value):
        errors.append(f"privacy:forbidden_text:{prefix}")
    return errors


def _missing_fields(mapping: Mapping[str, Any], fields: Sequence[str], prefix: str) -> list[str]:
    return [f"{prefix}:missing_{field}" for field in fields if field not in mapping]


def _duplicate_errors(values: Sequence[str], label: str) -> list[str]:
    counts = Counter(values)
    return [f"duplicate_{label}:{value}" for value, count in sorted(counts.items()) if count > 1]


def _facts_by_id(matrix: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(fact.get("fact_id")): fact
        for fact in _as_sequence(matrix.get("facts"))
        if isinstance(fact, Mapping) and isinstance(fact.get("fact_id"), str)
    }


def _counter_by(rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, int]:
    return _counter(row.get(key) for row in rows)


def _counter(values: Any) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values if value is not None).items()))


def _false_flags(fields: Sequence[str]) -> dict[str, bool]:
    return {field: False for field in fields}


def _public_string_list(value: Any, field: str) -> list[str]:
    items = _as_string_list(value)
    for item in items:
        if LOCAL_OR_PRIVATE_TEXT_RE.search(item):
            raise ParserOwnedFactTrackerError(f"{field} contains forbidden private text")
    return items


def _symbolic_list(value: Any, field: str) -> list[str]:
    items = _as_string_list(value)
    for item in items:
        if not SYMBOLIC_ID_RE.fullmatch(item):
            raise ParserOwnedFactTrackerError(f"{field} contains non-symbolic value")
    return items


def _as_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if not isinstance(value, Sequence) or isinstance(value, (bytes, bytearray)):
        return []
    return [item for item in value if isinstance(item, str)]


def _as_sequence(value: Any) -> Sequence[Any]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return value
    return []


def _member(value: str, allowed: Sequence[str], field: str) -> str:
    if value not in allowed:
        raise ParserOwnedFactTrackerError(f"{field} must be one of {', '.join(allowed)}")
    return value


def _symbolic_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not SYMBOLIC_ID_RE.fullmatch(value):
        raise ParserOwnedFactTrackerError(f"{field} must be a symbolic identifier")
    return value


def _fact_id(value: str, field: str) -> str:
    if not isinstance(value, str) or not FACT_ID_RE.fullmatch(value):
        raise ParserOwnedFactTrackerError(f"{field} must be a dotted fact id")
    return value


def _public_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ParserOwnedFactTrackerError(f"{field} must be non-empty public text")
    if LOCAL_OR_PRIVATE_TEXT_RE.search(value):
        raise ParserOwnedFactTrackerError(f"{field} contains forbidden private text")
    return value


def _utc_text(value: str, field: str) -> str:
    if not _is_utc_text(value):
        raise ParserOwnedFactTrackerError(f"{field} must be a UTC timestamp ending in Z")
    return value


def _is_utc_text(value: Any) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value))


def _dedupe(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _raise_if_errors(errors: Sequence[str], label: str) -> None:
    if errors:
        raise ParserOwnedFactTrackerError(f"{label} is invalid: {errors[0]}")
