from __future__ import annotations

import copy
import re
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from mythic_edge_parser.app import (
    evidence_ledger,
    field_recovery_matrix,
)
from mythic_edge_parser.app import (
    local_watcher_offset_window_monitor as offset_monitor,
)

FIELD_EVIDENCE_COMPARISON_REPORT_OBJECT = (
    "mythic_edge_parser_field_evidence_comparison_report"
)
FIELD_EVIDENCE_COMPARISON_SCHEMA_VERSION = (
    "parser_recovery_field_evidence_comparison_report.v1"
)
FIELD_EVIDENCE_COMPARISON_ROW_OBJECT = (
    "mythic_edge_parser_field_evidence_comparison_row"
)
FIELD_EVIDENCE_EXPECTED_OBJECT = "mythic_edge_parser_expected_field_evidence"
FIELD_EVIDENCE_CURRENT_OBJECT = "mythic_edge_parser_current_field_evidence_summary"

SOURCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/453"
PIPELINE_TRACKER = "https://github.com/Tahjali11/Mythic-Edge/issues/388"
PARENT_PRIVATE_EVIDENCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/434"

REPORT_STATUSES = (
    "comparison_ready",
    "review_required",
    "invalid_input",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "fail_closed",
)
COMPARISON_STATUSES = (
    "direct",
    "equivalent",
    "derived_bounded",
    "approximate_analytics_only",
    "unavailable",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "degraded",
    "stale",
    "conflict",
    "review_required",
    "invalid_input",
)
CANDIDATE_RECOVERY_HINTS = (
    "no_recovery_authorized",
    "existing_parser_behavior_sufficient",
    "needs_parser_contract",
    "needs_fixture_review",
    "needs_private_evidence_gate",
    "needs_external_boundary_issue",
    "needs_stale_source_refresh",
    "needs_field_matrix_update",
    "needs_manual_review",
    "needs_runtime_field_evidence_mapping",
    "needs_watcher_context_review",
    "analytics_display_only",
    "blocked_by_policy",
)
STALE_SOURCE_STATUSES = (
    "fresh",
    "stale",
    "unknown",
    "not_applicable",
    "unavailable",
    "blocked",
    "degraded",
    "manual_review_required",
)
WATCHER_WINDOW_STATUSES = ("not_applicable",) + offset_monitor.WINDOW_STATUSES
FIELD_FAMILIES = field_recovery_matrix.FIELD_FAMILIES + ("unknown",)

REQUIRED_NON_CLAIMS = (
    "not_parser_truth",
    "not_field_recovery_readiness",
    "not_private_harvest_authorization",
    "not_fixture_promotion",
    "not_corpus_status_change",
    "not_parser_behavior_readiness",
    "not_pipeline_activation_readiness",
    "not_watcher_correctness",
    "not_private_smoke_success",
    "not_merge_readiness",
    "not_deploy_readiness",
    "not_release_readiness",
    "not_production_behavior",
    "not_analytics_truth",
    "not_ai_truth",
    "not_coaching_truth",
)
FALSE_READINESS_FLAGS = (
    "parser_behavior_ready",
    "pipeline_activation_ready_for_issue_388",
    "private_harvest_authorized",
    "fixture_promotion_authorized",
    "corpus_status_change_authorized",
    "field_recovery_ready",
)
CURRENT_FALSE_FLAGS = (
    "contents_read",
    "raw_path_included",
    "raw_hash_included",
    "raw_payload_values_included",
    "private_excerpt_included",
)
PROTECTED_SURFACE_FLAGS = (
    "parser_behavior_changed",
    "parser_event_classes_changed",
    "parser_state_final_reconciliation_changed",
    "router_semantics_changed",
    "status_artifact_schema_changed",
    "diagnostics_or_drift_integration_changed",
    "workbook_or_webhook_surface_changed",
    "corpus_metadata_changed",
    "fixture_or_golden_replay_changed",
    "analytics_ai_or_coaching_truth_changed",
)

REQUIRED_REPORT_FIELDS = (
    "object",
    "schema_version",
    "source_issue",
    "pipeline_tracker",
    "parent_private_evidence_issue",
    "status",
    "status_reasons",
    "field_recovery_matrix_schema_version",
    "current_evidence_schema_version",
    "watcher_context_schema_version",
    "parser_behavior_ready",
    "pipeline_activation_ready_for_issue_388",
    "private_harvest_authorized",
    "fixture_promotion_authorized",
    "corpus_status_change_authorized",
    "field_recovery_ready",
    "summary",
    "rows",
    "privacy",
    "protected_surface_assertions",
    "limitations",
    "non_claims",
)
REQUIRED_ROW_FIELDS = (
    "object",
    "field_id",
    "display_name",
    "field_family",
    "expected_evidence",
    "current_evidence",
    "recovery_category",
    "parser_output_policy",
    "analytics_output_policy",
    "comparison_status",
    "confidence",
    "finality",
    "degradation_flags",
    "stale_source_status",
    "watcher_window_status",
    "candidate_recovery_hints",
    "review_required",
    "stop_reasons",
    "non_claims",
)
REQUIRED_EXPECTED_FIELDS = (
    "object",
    "field_id",
    "evidence_ledger_entry_ids",
    "required_direct_evidence",
    "allowed_fallback_evidence",
    "forbidden_fallback_evidence",
    "expected_recovery_category",
    "minimum_confidence",
    "allowed_finality",
    "expected_degradation_flags",
    "stale_source_behavior",
    "review_required_by_matrix",
)
REQUIRED_CURRENT_FIELDS = (
    "object",
    "schema_version",
    "field_id",
    "evidence_ledger_entry_ids",
    "observed_signal_ids",
    "source_event_families",
    "source_event_kinds",
    "value_source",
    "confidence",
    "finality",
    "degradation_flags",
    "invariant_status",
    "stale_source_status",
    "source_window_refs",
    "review_required",
    "contents_read",
    "raw_path_included",
    "raw_hash_included",
    "raw_payload_values_included",
    "private_excerpt_included",
)

FIELD_ID_RE = re.compile(r"^[a-z0-9_]+(?:\.[a-z0-9_]+)+$")
SYMBOLIC_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_.:-]{0,127}$")
LOCAL_ABSOLUTE_PATH_RE = re.compile(
    r"(?:file:(?://)?/(?!/)|(^|[\s\"'`(:=\[])/(?!/)|"
    r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]|\\\\)"
)
FORBIDDEN_TEXT_RE = re.compile(
    r"(\[UnityCrossThreadLogger\]|\[Client GRE\]|DETAILED LOGS:|"
    r"\bPlayer\.log\b|\bUTC_Log\b|https?://hooks\.|"
    r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}|"
    r"\b(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{8,})",
    re.IGNORECASE,
)
FORBIDDEN_KEYS = {
    "value",
    "field_value",
    "parser_value",
    "raw_payload",
    "raw_payload_value",
    "raw_payload_values",
    "raw_private_line",
    "raw_private_lines",
    "raw_line",
    "raw_lines",
    "raw_hash",
    "content_hash",
    "exact_offset",
    "exact_start_offset",
    "exact_end_offset",
    "exact_file_size",
    "exact_file_size_bytes",
    "exact_timestamp",
    "private_report_path",
    "local_absolute_path",
    "decklist",
    "card_choices",
}

CONFIDENCE_ORDER = {"unknown": 0, "low": 1, "medium": 2, "high": 3}
CONFIDENCE_BY_SCORE = {value: key for key, value in CONFIDENCE_ORDER.items()}
CATEGORY_CONFIDENCE_CAPS = {
    "direct": "high",
    "equivalent": "medium",
    "derived_bounded": "medium",
    "approximate_analytics_only": "low",
    "unavailable": "unknown",
    "blocked_private_evidence": "unknown",
    "blocked_external_boundary": "unknown",
    "review_required": "low",
}


def build_field_evidence_comparison_report(
    *,
    field_recovery_matrix_report: Mapping[str, Any] | None = None,
    current_field_evidence: Sequence[Mapping[str, Any]] | None = None,
    watcher_context: Mapping[str, Any] | None = None,
    context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    matrix = (
        field_recovery_matrix.build_field_recovery_matrix()
        if field_recovery_matrix_report is None
        else copy.deepcopy(dict(field_recovery_matrix_report))
    )
    context_payload = copy.deepcopy(dict(context or {}))
    privacy_errors = _privacy_errors(context_payload, "context")
    input_claim_errors = (
        _input_claim_errors(context_payload, "context")
        + _input_claim_errors(matrix, "field_recovery_matrix_report")
        + _input_claim_errors(current_field_evidence, "current_evidence")
        + _input_claim_errors(watcher_context, "watcher_context")
    )
    matrix_errors = field_recovery_matrix.validate_field_recovery_matrix(matrix)
    current_errors = _validate_current_sequence(current_field_evidence)
    watcher_errors = _validate_watcher_context(watcher_context)

    if matrix_errors:
        rows: list[dict[str, Any]] = []
        status = "invalid_input"
        status_reasons = ["matrix_validation_failed"]
    else:
        rows = _build_rows(matrix, current_field_evidence or (), watcher_context)
        status = _report_status(rows)
        status_reasons = _status_reasons(rows)

    fatal_errors = (
        privacy_errors
        + _fatal_error_codes(input_claim_errors + current_errors + watcher_errors)
    )
    if fatal_errors:
        status = "fail_closed"
        status_reasons = _dedupe_errors(["privacy_or_protected_surface_violation"])
    elif current_errors or watcher_errors:
        status = "invalid_input" if status != "fail_closed" else status
        status_reasons = _dedupe_errors(status_reasons + current_errors + watcher_errors)

    report = {
        "object": FIELD_EVIDENCE_COMPARISON_REPORT_OBJECT,
        "schema_version": FIELD_EVIDENCE_COMPARISON_SCHEMA_VERSION,
        "source_issue": context_payload.get("source_issue", SOURCE_ISSUE),
        "pipeline_tracker": context_payload.get("pipeline_tracker", PIPELINE_TRACKER),
        "parent_private_evidence_issue": context_payload.get(
            "parent_private_evidence_issue",
            PARENT_PRIVATE_EVIDENCE_ISSUE,
        ),
        "status": status,
        "status_reasons": status_reasons or ["comparison_ready"],
        "field_recovery_matrix_schema_version": matrix.get("schema_version"),
        "current_evidence_schema_version": FIELD_EVIDENCE_COMPARISON_SCHEMA_VERSION,
        "watcher_context_schema_version": _watcher_schema_version(watcher_context),
        "parser_behavior_ready": False,
        "pipeline_activation_ready_for_issue_388": False,
        "private_harvest_authorized": False,
        "fixture_promotion_authorized": False,
        "corpus_status_change_authorized": False,
        "field_recovery_ready": False,
        "summary": _build_summary(rows),
        "rows": rows,
        "privacy": _privacy_summary(),
        "protected_surface_assertions": _protected_surface_assertions(),
        "limitations": [
            "report_only_review_metadata",
            "no_parser_behavior_changes",
            "no_private_harvest_authorization",
            "no_fixture_or_corpus_status_promotion",
            "no_pipeline_activation_readiness",
        ],
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }
    report_privacy_errors = _privacy_errors(report, "report")
    if report_privacy_errors and report["status"] != "fail_closed":
        report["status"] = "fail_closed"
        report["status_reasons"] = ["privacy_or_protected_surface_violation"]
    return report


def compare_field_evidence(
    matrix_row: Mapping[str, Any],
    current_evidence: Mapping[str, Any] | None = None,
    *,
    watcher_context: Mapping[str, Any] | None = None,
    duplicate_current: bool = False,
) -> dict[str, Any]:
    row = copy.deepcopy(dict(matrix_row))
    expected = _expected_from_matrix_row(row)
    raw_current = copy.deepcopy(dict(current_evidence or {}))
    current = (
        _empty_current_summary(str(row.get("field_id") or "unknown.field"))
        if current_evidence is None
        else _normal_current_summary(current_evidence)
    )
    matrix_errors = field_recovery_matrix.validate_field_recovery_row(row)
    current_errors = validate_current_field_evidence_summary(current)
    privacy_errors = (
        _privacy_errors(raw_current, "current_evidence")
        + _forbidden_key_errors(raw_current, "current_evidence")
        + _input_claim_errors(row, "matrix_row")
        + _input_claim_errors(raw_current, "current_evidence")
        + _input_claim_errors(watcher_context, "watcher_context")
    )
    unknown_ledger = _unknown_ledger_entry_ids(current.get("evidence_ledger_entry_ids"))
    watcher_status = _watcher_status(current.get("source_window_refs"), watcher_context)
    status = _comparison_status(
        row,
        current,
        matrix_errors=matrix_errors,
        current_errors=current_errors,
        privacy_errors=privacy_errors,
        duplicate_current=duplicate_current,
        unknown_ledger=unknown_ledger,
        watcher_status=watcher_status,
    )
    confidence = _comparison_confidence(row, current, status)
    finality = (
        str(current.get("finality"))
        if current.get("finality") in evidence_ledger.FINALITY_LABELS
        else "provisional"
    )
    degradation_flags = _dedupe_errors(
        _as_string_list(current.get("degradation_flags"))
        + _status_degradation_flags(status)
    )
    stop_reasons = _stop_reasons(
        row,
        current,
        status=status,
        matrix_errors=matrix_errors,
        current_errors=current_errors,
        privacy_errors=privacy_errors,
        duplicate_current=duplicate_current,
        unknown_ledger=unknown_ledger,
        watcher_status=watcher_status,
    )
    return {
        "object": FIELD_EVIDENCE_COMPARISON_ROW_OBJECT,
        "field_id": str(row.get("field_id") or current.get("field_id") or "unknown.field"),
        "display_name": str(row.get("display_name") or "Unknown Field"),
        "field_family": str(row.get("field_family") or "unknown"),
        "expected_evidence": expected,
        "current_evidence": current,
        "recovery_category": str(row.get("recovery_category") or "review_required"),
        "parser_output_policy": str(row.get("parser_output_policy") or "manual_review_required"),
        "analytics_output_policy": str(
            row.get("analytics_output_policy") or "must_not_display_as_fact"
        ),
        "comparison_status": status,
        "confidence": confidence,
        "finality": finality,
        "degradation_flags": degradation_flags,
        "stale_source_status": _current_stale_status(current, status),
        "watcher_window_status": watcher_status,
        "candidate_recovery_hints": _candidate_recovery_hints(status, row),
        "review_required": _row_review_required(status, row, current, current_errors),
        "stop_reasons": stop_reasons,
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }


def validate_field_evidence_comparison_report(report: Mapping[str, Any]) -> list[str]:
    if not isinstance(report, Mapping):
        return ["report:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(report, REQUIRED_REPORT_FIELDS, "report"))
    if report.get("object") != FIELD_EVIDENCE_COMPARISON_REPORT_OBJECT:
        errors.append("report:invalid_object")
    if report.get("schema_version") != FIELD_EVIDENCE_COMPARISON_SCHEMA_VERSION:
        errors.append("report:invalid_schema_version")
    if report.get("source_issue") != SOURCE_ISSUE:
        errors.append("report:invalid_source_issue")
    if report.get("pipeline_tracker") != PIPELINE_TRACKER:
        errors.append("report:invalid_pipeline_tracker")
    if report.get("parent_private_evidence_issue") != PARENT_PRIVATE_EVIDENCE_ISSUE:
        errors.append("report:invalid_parent_private_evidence_issue")
    _validate_scalar(report.get("status"), REPORT_STATUSES, "report:status", errors)
    for flag in FALSE_READINESS_FLAGS:
        if report.get(flag) is not False:
            errors.append(f"report:{flag}_must_remain_false")
    _validate_string_list(report.get("status_reasons"), "report:status_reasons", errors)
    errors.extend(_validate_summary(report.get("summary"), report.get("rows")))
    errors.extend(_validate_false_mapping(report.get("privacy"), "report:privacy"))
    errors.extend(
        _validate_false_mapping(
            report.get("protected_surface_assertions"),
            "report:protected_surface_assertions",
        )
    )
    _validate_string_list(report.get("limitations"), "report:limitations", errors)
    errors.extend(_validate_non_claims(report.get("non_claims"), "report:non_claims"))
    rows = report.get("rows")
    if not isinstance(rows, list):
        errors.append("report:rows_not_list")
    else:
        for index, row in enumerate(rows):
            row_errors = validate_field_evidence_comparison_row(
                row if isinstance(row, Mapping) else {}
            )
            errors.extend(f"report:rows[{index}]:{error}" for error in row_errors)
    errors.extend(_privacy_errors(report, "report"))
    errors.extend(_forbidden_key_errors(report, "report"))
    return _dedupe_errors(errors)


def validate_field_evidence_comparison_row(row: Mapping[str, Any]) -> list[str]:
    if not isinstance(row, Mapping):
        return ["row:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(row, REQUIRED_ROW_FIELDS, "row"))
    if row.get("object") != FIELD_EVIDENCE_COMPARISON_ROW_OBJECT:
        errors.append("row:invalid_object")
    _validate_field_id(row.get("field_id"), "row:field_id", errors)
    _validate_scalar(row.get("field_family"), FIELD_FAMILIES, "row:field_family", errors)
    _validate_scalar(
        row.get("recovery_category"),
        field_recovery_matrix.RECOVERY_CATEGORIES,
        "row:recovery_category",
        errors,
    )
    _validate_scalar(
        row.get("parser_output_policy"),
        field_recovery_matrix.PARSER_OUTPUT_POLICIES,
        "row:parser_output_policy",
        errors,
    )
    _validate_scalar(
        row.get("analytics_output_policy"),
        field_recovery_matrix.ANALYTICS_OUTPUT_POLICIES,
        "row:analytics_output_policy",
        errors,
    )
    _validate_scalar(
        row.get("comparison_status"),
        COMPARISON_STATUSES,
        "row:comparison_status",
        errors,
    )
    _validate_scalar(
        row.get("confidence"),
        evidence_ledger.CONFIDENCE_LEVELS,
        "row:confidence",
        errors,
    )
    _validate_scalar(
        row.get("finality"),
        evidence_ledger.FINALITY_LABELS,
        "row:finality",
        errors,
    )
    _validate_scalar(
        row.get("stale_source_status"),
        STALE_SOURCE_STATUSES,
        "row:stale_source_status",
        errors,
    )
    _validate_scalar(
        row.get("watcher_window_status"),
        WATCHER_WINDOW_STATUSES,
        "row:watcher_window_status",
        errors,
    )
    _validate_string_list(row.get("degradation_flags"), "row:degradation_flags", errors)
    for flag in _as_string_list(row.get("degradation_flags")):
        if flag not in evidence_ledger.DRIFT_FLAGS:
            errors.append(f"row:degradation_flags:unknown:{flag}")
    _validate_string_list(
        row.get("candidate_recovery_hints"),
        "row:candidate_recovery_hints",
        errors,
    )
    for hint in _as_string_list(row.get("candidate_recovery_hints")):
        if hint not in CANDIDATE_RECOVERY_HINTS:
            errors.append(f"row:candidate_recovery_hints:unknown:{hint}")
    _validate_string_list(row.get("stop_reasons"), "row:stop_reasons", errors)
    if not isinstance(row.get("review_required"), bool):
        errors.append("row:review_required_not_bool")
    errors.extend(validate_expected_field_evidence(row.get("expected_evidence")))
    errors.extend(validate_current_field_evidence_summary(row.get("current_evidence")))
    errors.extend(_validate_non_claims(row.get("non_claims"), "row:non_claims"))
    errors.extend(_privacy_errors(row, "row"))
    errors.extend(_forbidden_key_errors(row, "row"))
    return _dedupe_errors(errors)


def validate_expected_field_evidence(expected: Any) -> list[str]:
    if not isinstance(expected, Mapping):
        return ["expected:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(expected, REQUIRED_EXPECTED_FIELDS, "expected"))
    if expected.get("object") != FIELD_EVIDENCE_EXPECTED_OBJECT:
        errors.append("expected:invalid_object")
    _validate_field_id(expected.get("field_id"), "expected:field_id", errors)
    for key in (
        "evidence_ledger_entry_ids",
        "required_direct_evidence",
        "allowed_fallback_evidence",
        "forbidden_fallback_evidence",
        "allowed_finality",
        "expected_degradation_flags",
    ):
        _validate_string_list(expected.get(key), f"expected:{key}", errors)
    _validate_scalar(
        expected.get("expected_recovery_category"),
        field_recovery_matrix.RECOVERY_CATEGORIES,
        "expected:expected_recovery_category",
        errors,
    )
    _validate_scalar(
        expected.get("minimum_confidence"),
        evidence_ledger.CONFIDENCE_LEVELS,
        "expected:minimum_confidence",
        errors,
    )
    _validate_scalar(
        expected.get("stale_source_behavior"),
        field_recovery_matrix.STALE_SOURCE_BEHAVIORS,
        "expected:stale_source_behavior",
        errors,
    )
    for finality in _as_string_list(expected.get("allowed_finality")):
        if finality not in evidence_ledger.FINALITY_LABELS:
            errors.append(f"expected:allowed_finality:unknown:{finality}")
    for flag in _as_string_list(expected.get("expected_degradation_flags")):
        if flag not in evidence_ledger.DRIFT_FLAGS:
            errors.append(f"expected:expected_degradation_flags:unknown:{flag}")
    if not isinstance(expected.get("review_required_by_matrix"), bool):
        errors.append("expected:review_required_by_matrix_not_bool")
    errors.extend(_privacy_errors(expected, "expected"))
    errors.extend(_forbidden_key_errors(expected, "expected"))
    return _dedupe_errors(errors)


def validate_current_field_evidence_summary(current: Any) -> list[str]:
    if not isinstance(current, Mapping):
        return ["current:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(current, REQUIRED_CURRENT_FIELDS, "current"))
    if current.get("object") != FIELD_EVIDENCE_CURRENT_OBJECT:
        errors.append("current:invalid_object")
    if current.get("schema_version") != FIELD_EVIDENCE_COMPARISON_SCHEMA_VERSION:
        errors.append("current:invalid_schema_version")
    _validate_field_id(current.get("field_id"), "current:field_id", errors)
    for key in (
        "evidence_ledger_entry_ids",
        "observed_signal_ids",
        "source_event_families",
        "source_event_kinds",
        "degradation_flags",
        "source_window_refs",
    ):
        _validate_string_list(current.get(key), f"current:{key}", errors)
    for ref_index, ref in enumerate(_as_string_list(current.get("source_window_refs"))):
        if not SYMBOLIC_ID_RE.fullmatch(ref):
            errors.append(f"current:source_window_refs[{ref_index}]:not_symbolic")
    _validate_scalar(
        current.get("value_source"),
        evidence_ledger.VALUE_SOURCES,
        "current:value_source",
        errors,
    )
    _validate_scalar(
        current.get("confidence"),
        evidence_ledger.CONFIDENCE_LEVELS,
        "current:confidence",
        errors,
    )
    _validate_scalar(
        current.get("finality"),
        evidence_ledger.FINALITY_LABELS,
        "current:finality",
        errors,
    )
    _validate_scalar(
        current.get("invariant_status"),
        evidence_ledger.INVARIANT_STATUSES,
        "current:invariant_status",
        errors,
    )
    _validate_scalar(
        current.get("stale_source_status"),
        STALE_SOURCE_STATUSES,
        "current:stale_source_status",
        errors,
    )
    for flag in _as_string_list(current.get("degradation_flags")):
        if flag not in evidence_ledger.DRIFT_FLAGS:
            errors.append(f"current:degradation_flags:unknown:{flag}")
    if not isinstance(current.get("review_required"), bool):
        errors.append("current:review_required_not_bool")
    for flag in CURRENT_FALSE_FLAGS:
        if current.get(flag) is not False:
            errors.append(f"current:{flag}_must_remain_false")
    errors.extend(_privacy_errors(current, "current"))
    errors.extend(_forbidden_key_errors(current, "current"))
    return _dedupe_errors(errors)


def _build_rows(
    matrix: Mapping[str, Any],
    current_field_evidence: Sequence[Mapping[str, Any]],
    watcher_context: Mapping[str, Any] | None,
) -> list[dict[str, Any]]:
    current_by_field: dict[str, list[Mapping[str, Any]]] = {}
    for summary in current_field_evidence:
        if not isinstance(summary, Mapping):
            continue
        field_id = str(summary.get("field_id") or "")
        current_by_field.setdefault(field_id, []).append(summary)

    rows: list[dict[str, Any]] = []
    known_fields: set[str] = set()
    for matrix_row in matrix.get("rows", []):
        if not isinstance(matrix_row, Mapping):
            continue
        field_id = str(matrix_row.get("field_id") or "")
        known_fields.add(field_id)
        summaries = current_by_field.get(field_id, [])
        rows.append(
            compare_field_evidence(
                matrix_row,
                summaries[0] if summaries else None,
                watcher_context=watcher_context,
                duplicate_current=len(summaries) > 1,
            )
        )

    for field_id in sorted(set(current_by_field) - known_fields):
        summaries = current_by_field[field_id]
        rows.append(
            compare_field_evidence(
                _unknown_matrix_row(field_id),
                summaries[0],
                watcher_context=watcher_context,
                duplicate_current=len(summaries) > 1,
            )
        )
    return rows


def _expected_from_matrix_row(row: Mapping[str, Any]) -> dict[str, Any]:
    field_id = str(row.get("field_id") or "unknown.field")
    return {
        "object": FIELD_EVIDENCE_EXPECTED_OBJECT,
        "field_id": field_id,
        "evidence_ledger_entry_ids": _as_string_list(row.get("evidence_ledger_entry_ids")),
        "required_direct_evidence": _as_string_list(row.get("required_direct_evidence")),
        "allowed_fallback_evidence": _as_string_list(row.get("allowed_fallback_evidence")),
        "forbidden_fallback_evidence": _as_string_list(row.get("forbidden_fallback_evidence")),
        "expected_recovery_category": str(row.get("recovery_category") or "review_required"),
        "minimum_confidence": str(row.get("minimum_confidence") or "unknown"),
        "allowed_finality": _as_string_list(row.get("allowed_finality")),
        "expected_degradation_flags": _as_string_list(row.get("degradation_flags")),
        "stale_source_behavior": str(row.get("stale_source_behavior") or "not_applicable"),
        "review_required_by_matrix": row.get("review_required") is True,
    }


def _normal_current_summary(current: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "object": _safe_text(current.get("object", FIELD_EVIDENCE_CURRENT_OBJECT)),
        "schema_version": _safe_text(current.get(
            "schema_version",
            FIELD_EVIDENCE_COMPARISON_SCHEMA_VERSION,
        )),
        "field_id": _safe_text(current.get("field_id", "unknown.field")),
        "evidence_ledger_entry_ids": _safe_string_list(current.get("evidence_ledger_entry_ids")),
        "observed_signal_ids": _safe_string_list(current.get("observed_signal_ids")),
        "source_event_families": _safe_string_list(current.get("source_event_families")),
        "source_event_kinds": _safe_string_list(current.get("source_event_kinds")),
        "value_source": _safe_text(current.get("value_source", "unknown")),
        "confidence": _safe_text(current.get("confidence", "unknown")),
        "finality": _safe_text(current.get("finality", "provisional")),
        "degradation_flags": _safe_string_list(current.get("degradation_flags")),
        "invariant_status": _safe_text(current.get("invariant_status", "not_checked")),
        "stale_source_status": _safe_text(current.get("stale_source_status", "unknown")),
        "source_window_refs": _safe_string_list(current.get("source_window_refs")),
        "review_required": current.get("review_required", True),
        "contents_read": current.get("contents_read", False),
        "raw_path_included": current.get("raw_path_included", False),
        "raw_hash_included": current.get("raw_hash_included", False),
        "raw_payload_values_included": current.get("raw_payload_values_included", False),
        "private_excerpt_included": current.get("private_excerpt_included", False),
    }


def _empty_current_summary(field_id: str) -> dict[str, Any]:
    return {
        "object": FIELD_EVIDENCE_CURRENT_OBJECT,
        "schema_version": FIELD_EVIDENCE_COMPARISON_SCHEMA_VERSION,
        "field_id": field_id,
        "evidence_ledger_entry_ids": [],
        "observed_signal_ids": [],
        "source_event_families": [],
        "source_event_kinds": [],
        "value_source": "unknown",
        "confidence": "unknown",
        "finality": "provisional",
        "degradation_flags": [],
        "invariant_status": "not_checked",
        "stale_source_status": "unknown",
        "source_window_refs": [],
        "review_required": True,
        "contents_read": False,
        "raw_path_included": False,
        "raw_hash_included": False,
        "raw_payload_values_included": False,
        "private_excerpt_included": False,
    }


def _unknown_matrix_row(field_id: str) -> dict[str, Any]:
    return {
        "object": field_recovery_matrix.FIELD_RECOVERY_MATRIX_ROW_OBJECT,
        "field_id": field_id,
        "display_name": "Unknown Field",
        "field_family": "unknown",
        "parser_owner": "unknown",
        "output_surfaces": [],
        "evidence_ledger_entry_ids": [],
        "required_direct_evidence": [],
        "allowed_fallback_evidence": [],
        "forbidden_fallback_evidence": [],
        "recovery_category": "review_required",
        "parser_output_policy": "manual_review_required",
        "analytics_output_policy": "must_not_display_as_fact",
        "minimum_confidence": "unknown",
        "allowed_finality": ["provisional"],
        "degradation_flags": ["fixture_gap"],
        "stale_source_behavior": "route_to_review_required",
        "review_required": True,
        "restoration_requirements": ["needs_field_matrix_update"],
        "non_claims": list(field_recovery_matrix.REQUIRED_NON_CLAIMS),
    }


def _comparison_status(
    row: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    matrix_errors: Sequence[str],
    current_errors: Sequence[str],
    privacy_errors: Sequence[str],
    duplicate_current: bool,
    unknown_ledger: Sequence[str],
    watcher_status: str,
) -> str:
    category = str(row.get("recovery_category") or "review_required")
    if privacy_errors or _fatal_error_codes(current_errors) or _fatal_error_codes(matrix_errors):
        return "invalid_input"
    if matrix_errors:
        return "review_required"
    if duplicate_current:
        return "conflict"
    if category == "blocked_private_evidence":
        return "blocked_private_evidence"
    if category == "blocked_external_boundary":
        return "blocked_external_boundary"
    if not _has_current_evidence(current):
        return "unavailable"
    if _field_has_forbidden_signal(row, current):
        return "invalid_input"
    if unknown_ledger:
        return "review_required"
    if current.get("value_source") == "conflict" or current.get("invariant_status") == "failed":
        return "conflict"
    if "conflicting_evidence" in _as_string_list(current.get("degradation_flags")):
        return "conflict"
    watcher_routed = _status_from_watcher(watcher_status)
    if watcher_routed is not None:
        return watcher_routed
    stale_routed = _status_from_stale_source(str(current.get("stale_source_status") or "unknown"))
    if stale_routed is not None:
        return stale_routed
    if current.get("invariant_status") == "degraded":
        return "degraded"
    if _as_string_list(current.get("degradation_flags")):
        return "degraded"
    if _low_confidence_final_requires_review(current):
        return "review_required"
    if category == "direct":
        if _direct_requirements_met(row, current):
            return "direct"
        return "review_required"
    if category == "equivalent":
        return "equivalent"
    if category == "derived_bounded":
        return "derived_bounded"
    if category == "approximate_analytics_only":
        return "approximate_analytics_only"
    if category == "unavailable":
        return "unavailable"
    return "review_required"


def _comparison_confidence(
    row: Mapping[str, Any],
    current: Mapping[str, Any],
    status: str,
) -> str:
    if status in {
        "invalid_input",
        "unavailable",
        "blocked_private_evidence",
        "blocked_external_boundary",
        "conflict",
    }:
        return "unknown"
    current_confidence = str(current.get("confidence") or "unknown")
    if current_confidence not in CONFIDENCE_ORDER:
        current_confidence = "unknown"
    category = str(row.get("recovery_category") or "review_required")
    cap = CATEGORY_CONFIDENCE_CAPS.get(category, "low")
    if status in {"degraded", "stale", "review_required"}:
        cap = _minimum_confidence(cap, "low")
    return _minimum_confidence(current_confidence, cap)


def _direct_requirements_met(row: Mapping[str, Any], current: Mapping[str, Any]) -> bool:
    direct_signals = set(_as_string_list(row.get("required_direct_evidence")))
    observed_signals = set(_as_string_list(current.get("observed_signal_ids")))
    if direct_signals and direct_signals.isdisjoint(observed_signals):
        return False
    if not _confidence_at_least(
        str(current.get("confidence") or "unknown"),
        str(row.get("minimum_confidence") or "unknown"),
    ):
        return False
    if current.get("finality") not in _as_string_list(row.get("allowed_finality")):
        return False
    if current.get("review_required") is True:
        return False
    return True


def _has_current_evidence(current: Mapping[str, Any]) -> bool:
    return bool(
        _as_string_list(current.get("evidence_ledger_entry_ids"))
        or _as_string_list(current.get("observed_signal_ids"))
        or _as_string_list(current.get("source_event_families"))
        or _as_string_list(current.get("source_event_kinds"))
    )


def _field_has_forbidden_signal(row: Mapping[str, Any], current: Mapping[str, Any]) -> bool:
    forbidden = set(_as_string_list(row.get("forbidden_fallback_evidence")))
    observed = set(_as_string_list(current.get("observed_signal_ids")))
    ledger_ids = set(_as_string_list(current.get("evidence_ledger_entry_ids")))
    return bool(forbidden & (observed | ledger_ids))


def _watcher_status(refs: Any, watcher_context: Mapping[str, Any] | None) -> str:
    refs_set = set(_as_string_list(refs))
    if not refs_set or not isinstance(watcher_context, Mapping):
        return "not_applicable"
    windows = watcher_context.get("windows")
    if not isinstance(windows, list):
        return "window_manual_review_required"
    matching_statuses = [
        window.get("window_status")
        for window in windows
        if isinstance(window, Mapping) and window.get("window_id") in refs_set
    ]
    if not matching_statuses:
        return "window_unavailable"
    priority = (
        "window_blocked_missing_approval",
        "window_stale",
        "window_degraded",
        "window_unavailable",
        "window_manual_review_required",
        "window_in_progress",
        "window_closed",
        "window_ready",
    )
    for status in priority:
        if status in matching_statuses:
            return status
    return "window_manual_review_required"


def _status_from_watcher(watcher_status: str) -> str | None:
    if watcher_status == "not_applicable":
        return None
    if watcher_status == "window_blocked_missing_approval":
        return "blocked_private_evidence"
    if watcher_status == "window_stale":
        return "stale"
    if watcher_status == "window_degraded":
        return "degraded"
    if watcher_status == "window_unavailable":
        return "unavailable"
    if watcher_status in {"window_manual_review_required", "window_in_progress"}:
        return "review_required"
    return None


def _status_from_stale_source(stale_source_status: str) -> str | None:
    if stale_source_status == "stale":
        return "stale"
    if stale_source_status == "blocked":
        return "blocked_private_evidence"
    if stale_source_status == "unavailable":
        return "unavailable"
    if stale_source_status == "degraded":
        return "degraded"
    if stale_source_status == "manual_review_required":
        return "review_required"
    return None


def _candidate_recovery_hints(status: str, row: Mapping[str, Any]) -> list[str]:
    hints = ["no_recovery_authorized"]
    if status == "direct":
        hints.append("existing_parser_behavior_sufficient")
    elif status == "equivalent":
        hints.extend(["needs_parser_contract", "needs_fixture_review"])
    elif status == "derived_bounded":
        hints.extend(["needs_parser_contract", "needs_fixture_review"])
    elif status == "approximate_analytics_only":
        hints.extend(["analytics_display_only", "blocked_by_policy"])
    elif status == "unavailable":
        hints.extend(["needs_runtime_field_evidence_mapping", "needs_manual_review"])
    elif status == "blocked_private_evidence":
        hints.extend(["needs_private_evidence_gate", "blocked_by_policy"])
    elif status == "blocked_external_boundary":
        hints.extend(["needs_external_boundary_issue", "blocked_by_policy"])
    elif status == "stale":
        hints.extend(["needs_stale_source_refresh", "needs_watcher_context_review"])
    elif status == "degraded":
        hints.extend(["needs_manual_review", "needs_runtime_field_evidence_mapping"])
    elif status == "conflict":
        hints.append("needs_manual_review")
    elif status == "invalid_input":
        hints.extend(["needs_manual_review", "blocked_by_policy"])
    else:
        hints.append("needs_manual_review")
    if row.get("field_family") == "unknown":
        hints.append("needs_field_matrix_update")
    return _dedupe_errors(hints)


def _row_review_required(
    status: str,
    row: Mapping[str, Any],
    current: Mapping[str, Any],
    current_errors: Sequence[str],
) -> bool:
    return bool(
        status != "direct"
        or row.get("review_required") is True
        or current.get("review_required") is True
        or current_errors
    )


def _stop_reasons(
    row: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    status: str,
    matrix_errors: Sequence[str],
    current_errors: Sequence[str],
    privacy_errors: Sequence[str],
    duplicate_current: bool,
    unknown_ledger: Sequence[str],
    watcher_status: str,
) -> list[str]:
    reasons = [f"comparison_status:{status}"]
    if matrix_errors:
        reasons.append("matrix_row_validation_failed")
    if current_errors:
        reasons.append("current_evidence_validation_failed")
    if privacy_errors:
        reasons.append("privacy_or_forbidden_marker")
    if duplicate_current:
        reasons.append("duplicate_current_evidence")
    if unknown_ledger:
        reasons.append("unknown_evidence_ledger_entry")
    if watcher_status != "not_applicable":
        reasons.append(f"watcher_window_status:{watcher_status}")
    if row.get("review_required") is True:
        reasons.append("matrix_row_requires_review")
    if current.get("review_required") is True:
        reasons.append("current_evidence_requires_review")
    return _dedupe_errors(reasons)


def _status_degradation_flags(status: str) -> list[str]:
    if status == "conflict":
        return ["conflicting_evidence", "invariant_failed"]
    if status == "degraded":
        return ["fixture_gap"]
    if status == "stale":
        return ["fixture_gap"]
    if status == "invalid_input":
        return ["new_unknown_payload_path"]
    return []


def _current_stale_status(current: Mapping[str, Any], status: str) -> str:
    if status == "stale":
        return "stale"
    stale_status = str(current.get("stale_source_status") or "unknown")
    return stale_status if stale_status in STALE_SOURCE_STATUSES else "unknown"


def _report_status(rows: Sequence[Mapping[str, Any]]) -> str:
    statuses = {row.get("comparison_status") for row in rows}
    if "invalid_input" in statuses:
        return "invalid_input"
    if "blocked_private_evidence" in statuses:
        return "blocked_private_evidence"
    if "blocked_external_boundary" in statuses:
        return "blocked_external_boundary"
    if statuses - {"direct"}:
        return "review_required"
    return "comparison_ready"


def _status_reasons(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    statuses = _count_values(rows, "comparison_status", COMPARISON_STATUSES)
    return [f"{status}:{count}" for status, count in statuses.items() if count]


def _build_summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "comparison_status_counts": _count_values(rows, "comparison_status", COMPARISON_STATUSES),
        "recovery_category_counts": _count_values(
            rows,
            "recovery_category",
            field_recovery_matrix.RECOVERY_CATEGORIES,
        ),
        "review_required_count": sum(1 for row in rows if row.get("review_required") is True),
        "summary_is_readiness_metric": False,
    }


def _privacy_summary() -> dict[str, bool]:
    return {
        "raw_private_logs_included": False,
        "raw_payload_values_included": False,
        "raw_paths_included": False,
        "raw_hashes_included": False,
        "private_excerpts_included": False,
        "local_artifacts_included": False,
    }


def _protected_surface_assertions() -> dict[str, bool]:
    return {
        "parser_behavior_changed": False,
        "parser_event_classes_changed": False,
        "parser_state_final_reconciliation_changed": False,
        "router_semantics_changed": False,
        "status_artifact_schema_changed": False,
        "diagnostics_or_drift_integration_changed": False,
        "workbook_or_webhook_surface_changed": False,
        "corpus_metadata_changed": False,
        "fixture_or_golden_replay_changed": False,
        "analytics_ai_or_coaching_truth_changed": False,
    }


def _validate_summary(summary: Any, rows: Any) -> list[str]:
    if not isinstance(summary, Mapping):
        return ["report:summary_not_mapping"]
    if not isinstance(rows, list):
        return []
    expected = _build_summary(rows)
    errors: list[str] = []
    for key, expected_value in expected.items():
        if summary.get(key) != expected_value:
            errors.append(f"report:summary:{key}_mismatch")
    return errors


def _validate_current_sequence(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (str, bytes)) or isinstance(value, Mapping):
        return ["current_evidence:not_sequence"]
    if not isinstance(value, Sequence):
        return ["current_evidence:not_sequence"]
    errors: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            errors.append(f"current_evidence[{index}]:not_mapping")
            continue
        errors.extend(
            f"current_evidence[{index}]:{error}"
            for error in _privacy_errors(item, "current")
        )
        errors.extend(
            f"current_evidence[{index}]:{error}"
            for error in _forbidden_key_errors(item, "current")
        )
        item_errors = validate_current_field_evidence_summary(_normal_current_summary(item))
        errors.extend(f"current_evidence[{index}]:{error}" for error in item_errors)
    return _dedupe_errors(errors)


def _validate_watcher_context(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, Mapping):
        return ["watcher_context:not_mapping"]
    if value.get("schema_version") != offset_monitor.LOCAL_WATCHER_OFFSET_WINDOW_SCHEMA_VERSION:
        return ["watcher_context:invalid_schema_version"]
    errors = offset_monitor.validate_offset_window_monitor_report(value)
    return [f"watcher_context:{error}" for error in errors]


def _watcher_schema_version(watcher_context: Mapping[str, Any] | None) -> str | None:
    if not isinstance(watcher_context, Mapping):
        return None
    schema = watcher_context.get("schema_version")
    return schema if isinstance(schema, str) else None


def _unknown_ledger_entry_ids(value: Any) -> list[str]:
    known = {entry["entry_id"] for entry in evidence_ledger.iter_ledger_entries()}
    return [entry_id for entry_id in _as_string_list(value) if entry_id not in known]


def _low_confidence_final_requires_review(current: Mapping[str, Any]) -> bool:
    return current.get("confidence") == "low" and current.get("finality") in {
        "final",
        "reconciled",
    }


def _confidence_at_least(actual: str, minimum: str) -> bool:
    return CONFIDENCE_ORDER.get(actual, 0) >= CONFIDENCE_ORDER.get(minimum, 0)


def _minimum_confidence(left: str, right: str) -> str:
    score = min(CONFIDENCE_ORDER.get(left, 0), CONFIDENCE_ORDER.get(right, 0))
    return CONFIDENCE_BY_SCORE[score]


def _fatal_error_codes(errors: Sequence[str]) -> list[str]:
    return [
        error
        for error in errors
        if "privacy:" in error
        or "forbidden_key" in error
        or "_must_remain_false" in error
        or "raw_" in error
        or "private_excerpt" in error
    ]


def _missing_required_fields(value: Mapping[str, Any], fields: Sequence[str], label: str) -> list[str]:
    return [f"{label}:missing:{field}" for field in fields if field not in value]


def _validate_scalar(
    value: Any,
    allowed: Sequence[str],
    label: str,
    errors: list[str],
) -> None:
    if value not in allowed:
        errors.append(f"{label}:unknown:{value}")


def _validate_field_id(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or FIELD_ID_RE.fullmatch(value) is None:
        errors.append(f"{label}:invalid")


def _validate_string_list(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{label}_not_list")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str):
            errors.append(f"{label}[{index}]_not_string")


def _normalize_field_name(value: str) -> str:
    separated = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", value)
    separated = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", separated)
    return re.sub(r"[^a-zA-Z0-9]+", "_", separated).lower().strip("_")


def _validate_false_mapping(value: Any, label: str) -> list[str]:
    if not isinstance(value, Mapping):
        return [f"{label}_not_mapping"]
    return [
        f"{label}:{key}_must_remain_false"
        for key, item in value.items()
        if item is not False
    ]


def _input_claim_errors(value: Any, label: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            child_label = f"{label}.{key}"
            key_name = str(key)
            normalized_key = _normalize_field_name(key_name)
            if normalized_key in FALSE_READINESS_FLAGS and item is not False:
                errors.append(f"{child_label}_must_remain_false")
            if normalized_key == "protected_surface_assertions":
                if isinstance(item, Mapping):
                    errors.extend(_validate_false_mapping(item, child_label))
                else:
                    errors.append(f"{child_label}_must_remain_false")
            if normalized_key in PROTECTED_SURFACE_FLAGS and item is not False:
                errors.append(f"{child_label}_must_remain_false")
            errors.extend(_input_claim_errors(item, child_label))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(_input_claim_errors(item, f"{label}[{index}]"))
    return _dedupe_errors(errors)


def _validate_non_claims(value: Any, label: str) -> list[str]:
    errors: list[str] = []
    _validate_string_list(value, label, errors)
    if isinstance(value, list) and tuple(value) != REQUIRED_NON_CLAIMS:
        errors.append(f"{label}:mismatch")
    return errors


def _privacy_errors(value: Any, label: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            errors.extend(_privacy_errors(item, f"{label}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(_privacy_errors(item, f"{label}[{index}]"))
    elif isinstance(value, str):
        if LOCAL_ABSOLUTE_PATH_RE.search(value):
            errors.append(f"privacy:absolute_path:{label}")
        if FORBIDDEN_TEXT_RE.search(value):
            errors.append(f"privacy:forbidden_text:{label}")
    return errors


def _safe_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    if LOCAL_ABSOLUTE_PATH_RE.search(value) or FORBIDDEN_TEXT_RE.search(value):
        return "redacted_forbidden_value"
    return value


def _safe_string_list(value: Any) -> list[str]:
    return [_safe_text(item) for item in _as_string_list(value)]


def _forbidden_key_errors(value: Any, label: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            child_label = f"{label}.{key}"
            if key in FORBIDDEN_KEYS:
                errors.append(f"privacy:forbidden_key:{child_label}")
            errors.extend(_forbidden_key_errors(item, child_label))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(_forbidden_key_errors(item, f"{label}[{index}]"))
    return errors


def _count_values(
    rows: Sequence[Mapping[str, Any]],
    key: str,
    allowed_values: Sequence[str],
) -> dict[str, int]:
    return {
        value: sum(1 for row in rows if row.get(key) == value)
        for value in allowed_values
    }


def _as_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _dedupe_errors(errors: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(errors))
