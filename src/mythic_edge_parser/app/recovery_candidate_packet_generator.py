from __future__ import annotations

import copy
import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any

from mythic_edge_parser.app import field_evidence_comparison_report as comparison
from mythic_edge_parser.app import field_recovery_matrix

RECOVERY_CANDIDATE_PACKET_REPORT_OBJECT = (
    "mythic_edge_parser_recovery_candidate_packet_report"
)
RECOVERY_CANDIDATE_PACKET_SCHEMA_VERSION = (
    "parser_recovery_candidate_packet_generator.v1"
)
RECOVERY_CANDIDATE_PACKET_OBJECT = (
    "mythic_edge_parser_recovery_candidate_packet"
)
RECOVERY_CANDIDATE_REVIEW_DECISION_OBJECT = (
    "mythic_edge_parser_recovery_candidate_review_decision"
)

SOURCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/454"
PIPELINE_TRACKER = "https://github.com/Tahjali11/Mythic-Edge/issues/388"
PARENT_PRIVATE_EVIDENCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/434"

REPORT_STATUSES = (
    "candidate_packets_ready",
    "empty",
    "review_required",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "invalid_input",
    "fail_closed",
)
CANDIDATE_STATUSES = (
    "candidate_ready_for_review",
    "review_required",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "blocked_unsupported_claim",
    "blocked_privacy",
    "blocked_authorization",
    "not_a_candidate",
    "stale_input",
    "conflict",
    "invalid_input",
)
CANDIDATE_CATEGORIES = (
    "direct_preservation_candidate",
    "equivalent_mapping_candidate",
    "derived_bounded_candidate",
    "approximate_review_candidate",
    "analytics_display_only_candidate",
    "blocked_private_candidate",
    "blocked_external_candidate",
    "unavailable_no_candidate",
    "conflict_review_candidate",
    "stale_evidence_review_candidate",
    "unsupported_claim_blocked",
)
REVIEW_DECISIONS = (
    "undecided",
    "accept_for_later_problem_representation",
    "reject_no_recovery_path",
    "needs_private_evidence_approval",
    "needs_external_boundary_issue",
    "needs_matrix_update_contract",
    "needs_parser_contract",
    "needs_fixture_promotion_contract",
    "needs_corpus_status_contract",
    "defer",
    "blocked",
)
ALLOWED_NEXT_STEPS = (
    "review_only",
    "codex_a_problem_representation",
    "private_evidence_approval",
    "external_boundary_issue",
    "matrix_update_contract",
    "parser_contract",
    "fixture_promotion_contract",
    "corpus_status_contract",
    "no_action",
    "blocked",
)
PRIVACY_STATUSES = (
    "public_safe",
    "symbolic_only",
    "redacted",
    "review_required",
    "blocked_private_marker",
    "blocked_exact_path",
    "blocked_exact_offset",
    "blocked_exact_size",
    "blocked_exact_timestamp",
    "blocked_raw_hash",
    "blocked_raw_payload",
    "blocked_secret_marker",
    "blocked_local_artifact",
)
REQUIRED_NON_CLAIMS = (
    "not_parser_truth",
    "not_field_recovery_readiness",
    "not_private_harvest_authorization",
    "not_fixture_promotion",
    "not_corpus_status_change",
    "not_parser_behavior_readiness",
    "not_pipeline_activation_readiness",
    "not_file_writing_authorization",
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
    "file_writing_authorized",
    "private_harvest_authorized",
    "fixture_promotion_authorized",
    "corpus_status_change_authorized",
    "field_recovery_ready",
)
PROTECTED_SURFACE_FLAGS = (
    "parser_behavior_changed",
    "parser_event_classes_changed",
    "parser_state_final_reconciliation_changed",
    "router_semantics_changed",
    "match_game_identity_or_deduplication_changed",
    "status_artifact_schema_changed",
    "diagnostics_or_drift_integration_changed",
    "workbook_or_webhook_surface_changed",
    "corpus_metadata_changed",
    "fixture_or_golden_replay_changed",
    "analytics_ai_or_coaching_truth_changed",
)
PRIVACY_FALSE_FLAGS = (
    "contents_read",
    "raw_path_included",
    "raw_hash_included",
    "raw_payload_values_included",
    "private_excerpt_included",
    "local_state_written",
    "packet_file_written",
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
    "field_evidence_comparison_schema_version",
    "watcher_context_schema_version",
    "parser_behavior_ready",
    "pipeline_activation_ready_for_issue_388",
    "file_writing_authorized",
    "private_harvest_authorized",
    "fixture_promotion_authorized",
    "corpus_status_change_authorized",
    "field_recovery_ready",
    "packets",
    "summary",
    "privacy",
    "protected_surface_assertions",
    "limitations",
    "non_claims",
)
REQUIRED_PACKET_FIELDS = (
    "object",
    "schema_version",
    "packet_id",
    "field_id",
    "display_name",
    "field_family",
    "candidate_status",
    "candidate_category",
    "candidate_summary",
    "field_recovery_matrix_ref",
    "comparison_row_ref",
    "expected_evidence_summary",
    "current_evidence_summary",
    "evidence_delta",
    "source_evidence_refs",
    "offset_window_refs",
    "confidence",
    "finality",
    "degradation_flags",
    "comparison_status",
    "candidate_recovery_hints",
    "stop_reasons",
    "privacy_status",
    "reviewer_decision",
    "review_required",
    "next_role_hint",
    "non_claims",
)
REQUIRED_REVIEW_DECISION_FIELDS = (
    "object",
    "decision",
    "decision_reason",
    "allowed_next_step",
    "requires_new_issue",
    "requires_private_evidence_approval",
    "requires_parser_contract",
    "requires_fixture_promotion_contract",
    "requires_corpus_status_contract",
    "non_claims",
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
    "strategy_notes",
}
CLAIM_KEYS = {re.sub(r"[^a-z0-9]", "", key.lower()) for key in FALSE_READINESS_FLAGS} | {
    "parserbehaviorready",
    "pipelineactivationreadyforissue388",
    "filewritingauthorized",
    "privateharvestauthorized",
    "fixturepromotionauthorized",
    "corpusstatuschangeauthorized",
    "fieldrecoveryready",
}
PROTECTED_ASSERTION_KEYS = {
    re.sub(r"[^a-z0-9]", "", key.lower()) for key in PROTECTED_SURFACE_FLAGS
}


def build_recovery_candidate_packet_report(
    *,
    field_recovery_matrix_report: Mapping[str, Any] | None = None,
    field_evidence_comparison_report: Mapping[str, Any] | None = None,
    reduced_evidence_summaries: Sequence[Mapping[str, Any]] | None = None,
    offset_window_metadata: Mapping[str, Any] | None = None,
    context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic, public-safe, in-memory recovery candidate report."""

    matrix = (
        field_recovery_matrix.build_field_recovery_matrix()
        if field_recovery_matrix_report is None
        else copy.deepcopy(dict(field_recovery_matrix_report))
    )
    context_payload = copy.deepcopy(dict(context or {}))
    comparison_report = (
        comparison.build_field_evidence_comparison_report(
            field_recovery_matrix_report=matrix,
            current_field_evidence=reduced_evidence_summaries,
            watcher_context=offset_window_metadata,
            context=context_payload,
        )
        if field_evidence_comparison_report is None
        else copy.deepcopy(dict(field_evidence_comparison_report))
    )
    input_errors = _input_errors(
        context_payload,
        matrix,
        comparison_report,
        reduced_evidence_summaries,
        offset_window_metadata,
    )
    matrix_errors = field_recovery_matrix.validate_field_recovery_matrix(matrix)
    comparison_errors = comparison.validate_field_evidence_comparison_report(comparison_report)

    fatal_errors = _fatal_error_codes(input_errors)
    valid_inputs = not matrix_errors and not comparison_errors and not fatal_errors
    packets = (
        [
            build_recovery_candidate_packet(row, matrix)
            for row in comparison_report.get("rows", [])
            if isinstance(row, Mapping)
        ]
        if valid_inputs
        else []
    )
    packet_errors = _packet_validation_errors(packets) if valid_inputs else []
    if packet_errors:
        packets = []

    status = _report_status(packets)
    status_reasons = _status_reasons(packets)
    if matrix_errors or comparison_errors or packet_errors:
        status = "invalid_input"
        status_reasons = _dedupe_errors(
            ["invalid_input"]
            + [f"matrix:{error}" for error in matrix_errors]
            + [f"comparison:{error}" for error in comparison_errors]
            + packet_errors
        )
    if fatal_errors:
        status = "fail_closed"
        status_reasons = ["privacy_or_protected_surface_violation"]

    report = {
        "object": RECOVERY_CANDIDATE_PACKET_REPORT_OBJECT,
        "schema_version": RECOVERY_CANDIDATE_PACKET_SCHEMA_VERSION,
        "source_issue": SOURCE_ISSUE,
        "pipeline_tracker": PIPELINE_TRACKER,
        "parent_private_evidence_issue": PARENT_PRIVATE_EVIDENCE_ISSUE,
        "status": status,
        "status_reasons": status_reasons,
        "field_recovery_matrix_schema_version": matrix.get("schema_version"),
        "field_evidence_comparison_schema_version": comparison_report.get("schema_version"),
        "watcher_context_schema_version": _watcher_schema_version(offset_window_metadata),
        "parser_behavior_ready": False,
        "pipeline_activation_ready_for_issue_388": False,
        "file_writing_authorized": False,
        "private_harvest_authorized": False,
        "fixture_promotion_authorized": False,
        "corpus_status_change_authorized": False,
        "field_recovery_ready": False,
        "packets": packets,
        "summary": _summary(packets),
        "privacy": _privacy_summary(),
        "protected_surface_assertions": _protected_surface_assertions(),
        "limitations": [
            "in_memory_review_metadata_only",
            "no_file_writing_authorization",
            "no_parser_behavior_changes",
            "no_private_harvest_authorization",
            "no_fixture_or_corpus_status_promotion",
            "no_pipeline_activation_readiness",
        ],
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }
    report_errors = (
        _privacy_errors(report, "report")
        + _forbidden_key_errors(report, "report")
        + _claim_errors(report, "report")
    )
    if report_errors and report["status"] != "fail_closed":
        report["status"] = "fail_closed"
        report["status_reasons"] = ["privacy_or_protected_surface_violation"]
        report["packets"] = []
        report["summary"] = _summary([])
    return report


def build_recovery_candidate_packet(
    comparison_row: Mapping[str, Any],
    field_recovery_matrix_report: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one recovery candidate packet from a validated comparison row."""

    row = copy.deepcopy(dict(comparison_row))
    row_errors = _safety_errors(row, "row")
    status = _candidate_status(row)
    category = _candidate_category(row)
    packet = {
        "object": RECOVERY_CANDIDATE_PACKET_OBJECT,
        "schema_version": RECOVERY_CANDIDATE_PACKET_SCHEMA_VERSION,
        "packet_id": _packet_id(row, status, category),
        "field_id": _safe_text(row.get("field_id", "unknown.field")),
        "display_name": _safe_text(row.get("display_name", "Unknown Field")),
        "field_family": _safe_text(row.get("field_family", "unknown")),
        "candidate_status": status,
        "candidate_category": category,
        "candidate_summary": _candidate_summary(row, status, category),
        "field_recovery_matrix_ref": _matrix_ref(row, field_recovery_matrix_report),
        "comparison_row_ref": _comparison_ref(row),
        "expected_evidence_summary": _expected_summary(row.get("expected_evidence")),
        "current_evidence_summary": _current_summary(row.get("current_evidence")),
        "evidence_delta": _evidence_delta(row),
        "source_evidence_refs": _source_evidence_refs(row),
        "offset_window_refs": _offset_window_refs(row),
        "confidence": _safe_text(row.get("confidence", "unknown")),
        "finality": _safe_text(row.get("finality", "provisional")),
        "degradation_flags": _safe_string_list(row.get("degradation_flags")),
        "comparison_status": _safe_text(row.get("comparison_status", "review_required")),
        "candidate_recovery_hints": _safe_string_list(row.get("candidate_recovery_hints")),
        "stop_reasons": _packet_stop_reasons(row, status, category),
        "privacy_status": _privacy_status(row, status),
        "reviewer_decision": _reviewer_decision(status, category, row),
        "review_required": _packet_review_required(status, row),
        "next_role_hint": _next_role_hint(status, category),
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }
    if row_errors or _safety_errors(packet, "packet"):
        packet["candidate_status"] = "blocked_privacy"
        packet["candidate_category"] = "unsupported_claim_blocked"
        packet["privacy_status"] = "blocked_local_artifact"
        packet["review_required"] = True
        packet["next_role_hint"] = "blocked"
        packet["stop_reasons"] = _dedupe_errors(
            _safe_string_list(packet.get("stop_reasons")) + ["privacy_or_forbidden_marker"]
        )
    return packet


def validate_recovery_candidate_packet_report(report: Mapping[str, Any]) -> list[str]:
    if not isinstance(report, Mapping):
        return ["report:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(report, REQUIRED_REPORT_FIELDS, "report"))
    if report.get("object") != RECOVERY_CANDIDATE_PACKET_REPORT_OBJECT:
        errors.append("report:invalid_object")
    if report.get("schema_version") != RECOVERY_CANDIDATE_PACKET_SCHEMA_VERSION:
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
    errors.extend(_validate_false_mapping(report.get("privacy"), "report:privacy"))
    errors.extend(
        _validate_false_mapping(
            report.get("protected_surface_assertions"),
            "report:protected_surface_assertions",
        )
    )
    errors.extend(_validate_summary(report.get("summary"), report.get("packets")))
    _validate_string_list(report.get("status_reasons"), "report:status_reasons", errors)
    _validate_string_list(report.get("limitations"), "report:limitations", errors)
    errors.extend(_validate_non_claims(report.get("non_claims"), "report:non_claims"))
    packets = report.get("packets")
    if not isinstance(packets, list):
        errors.append("report:packets_not_list")
    else:
        packet_ids: set[str] = set()
        for index, packet in enumerate(packets):
            packet_errors = validate_recovery_candidate_packet(
                packet if isinstance(packet, Mapping) else {}
            )
            errors.extend(f"report:packets[{index}]:{error}" for error in packet_errors)
            packet_id = packet.get("packet_id") if isinstance(packet, Mapping) else None
            if isinstance(packet_id, str):
                if packet_id in packet_ids:
                    errors.append(f"report:duplicate_packet_id:{packet_id}")
                packet_ids.add(packet_id)
    errors.extend(_privacy_errors(report, "report"))
    errors.extend(_forbidden_key_errors(report, "report"))
    errors.extend(_claim_errors(report, "report"))
    return _dedupe_errors(errors)


def validate_recovery_candidate_packet(packet: Mapping[str, Any]) -> list[str]:
    if not isinstance(packet, Mapping):
        return ["packet:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(packet, REQUIRED_PACKET_FIELDS, "packet"))
    if packet.get("object") != RECOVERY_CANDIDATE_PACKET_OBJECT:
        errors.append("packet:invalid_object")
    if packet.get("schema_version") != RECOVERY_CANDIDATE_PACKET_SCHEMA_VERSION:
        errors.append("packet:invalid_schema_version")
    _validate_field_id(packet.get("field_id"), "packet:field_id", errors)
    _validate_scalar(
        packet.get("candidate_status"),
        CANDIDATE_STATUSES,
        "packet:candidate_status",
        errors,
    )
    _validate_scalar(
        packet.get("candidate_category"),
        CANDIDATE_CATEGORIES,
        "packet:candidate_category",
        errors,
    )
    _validate_scalar(
        packet.get("privacy_status"),
        PRIVACY_STATUSES,
        "packet:privacy_status",
        errors,
    )
    _validate_scalar(
        packet.get("comparison_status"),
        comparison.COMPARISON_STATUSES,
        "packet:comparison_status",
        errors,
    )
    _validate_string_list(packet.get("source_evidence_refs"), "packet:source_evidence_refs", errors)
    _validate_string_list(packet.get("offset_window_refs"), "packet:offset_window_refs", errors)
    for ref_index, ref in enumerate(_as_string_list(packet.get("offset_window_refs"))):
        if not SYMBOLIC_ID_RE.fullmatch(ref):
            errors.append(f"packet:offset_window_refs[{ref_index}]:not_symbolic")
    _validate_string_list(packet.get("degradation_flags"), "packet:degradation_flags", errors)
    _validate_string_list(
        packet.get("candidate_recovery_hints"),
        "packet:candidate_recovery_hints",
        errors,
    )
    _validate_string_list(packet.get("stop_reasons"), "packet:stop_reasons", errors)
    if not isinstance(packet.get("review_required"), bool):
        errors.append("packet:review_required_not_bool")
    errors.extend(validate_recovery_candidate_review_decision(packet.get("reviewer_decision")))
    errors.extend(_validate_non_claims(packet.get("non_claims"), "packet:non_claims"))
    errors.extend(_privacy_errors(packet, "packet"))
    errors.extend(_forbidden_key_errors(packet, "packet"))
    errors.extend(_claim_errors(packet, "packet"))
    return _dedupe_errors(errors)


def validate_recovery_candidate_review_decision(decision: Any) -> list[str]:
    if not isinstance(decision, Mapping):
        return ["review_decision:not_mapping"]
    errors: list[str] = []
    errors.extend(
        _missing_required_fields(decision, REQUIRED_REVIEW_DECISION_FIELDS, "review_decision")
    )
    if decision.get("object") != RECOVERY_CANDIDATE_REVIEW_DECISION_OBJECT:
        errors.append("review_decision:invalid_object")
    _validate_scalar(
        decision.get("decision"),
        REVIEW_DECISIONS,
        "review_decision:decision",
        errors,
    )
    _validate_scalar(
        decision.get("allowed_next_step"),
        ALLOWED_NEXT_STEPS,
        "review_decision:allowed_next_step",
        errors,
    )
    for key in (
        "requires_new_issue",
        "requires_private_evidence_approval",
        "requires_parser_contract",
        "requires_fixture_promotion_contract",
        "requires_corpus_status_contract",
    ):
        if not isinstance(decision.get(key), bool):
            errors.append(f"review_decision:{key}_not_bool")
    errors.extend(_validate_non_claims(decision.get("non_claims"), "review_decision:non_claims"))
    errors.extend(_privacy_errors(decision, "review_decision"))
    errors.extend(_forbidden_key_errors(decision, "review_decision"))
    errors.extend(_claim_errors(decision, "review_decision"))
    return _dedupe_errors(errors)


def _candidate_status(row: Mapping[str, Any]) -> str:
    status = str(row.get("comparison_status") or "review_required")
    parser_policy = str(row.get("parser_output_policy") or "")
    if _safety_errors(row, "row"):
        return "blocked_privacy"
    if status == "direct":
        if (
            parser_policy == "preserve_existing_parser_behavior"
            and row.get("review_required") is not True
            and not _as_string_list(row.get("degradation_flags"))
            and str(row.get("stale_source_status") or "fresh") in {"fresh", "not_applicable"}
        ):
            return "candidate_ready_for_review"
        return "review_required"
    if status in {"equivalent", "derived_bounded", "degraded", "review_required"}:
        return "review_required"
    if status == "approximate_analytics_only":
        return "review_required"
    if status == "unavailable":
        return "not_a_candidate"
    if status == "blocked_private_evidence":
        return "blocked_private_evidence"
    if status == "blocked_external_boundary":
        return "blocked_external_boundary"
    if status == "stale":
        return "stale_input"
    if status == "conflict":
        return "conflict"
    if status == "invalid_input":
        return "invalid_input"
    return "review_required"


def _candidate_category(row: Mapping[str, Any]) -> str:
    status = str(row.get("comparison_status") or "review_required")
    if _safety_errors(row, "row"):
        return "unsupported_claim_blocked"
    if status == "direct":
        return "direct_preservation_candidate"
    if status == "equivalent":
        return "equivalent_mapping_candidate"
    if status == "derived_bounded":
        return "derived_bounded_candidate"
    if status == "approximate_analytics_only":
        return (
            "analytics_display_only_candidate"
            if "analytics_display_only" in _as_string_list(row.get("candidate_recovery_hints"))
            else "approximate_review_candidate"
        )
    if status == "unavailable":
        return "unavailable_no_candidate"
    if status == "blocked_private_evidence":
        return "blocked_private_candidate"
    if status == "blocked_external_boundary":
        return "blocked_external_candidate"
    if status == "stale":
        return "stale_evidence_review_candidate"
    if status in {"conflict", "degraded", "review_required"}:
        return "conflict_review_candidate"
    return "unsupported_claim_blocked"


def _candidate_summary(row: Mapping[str, Any], status: str, category: str) -> str:
    field_id = _safe_text(row.get("field_id", "unknown.field"))
    comparison_status = _safe_text(row.get("comparison_status", "review_required"))
    if status == "candidate_ready_for_review":
        return f"{field_id}: existing parser behavior has direct public-safe evidence for review."
    if category == "blocked_private_candidate":
        return f"{field_id}: recovery evidence remains blocked behind private-evidence approval."
    if category == "blocked_external_candidate":
        return f"{field_id}: recovery evidence remains blocked behind an external-boundary issue."
    if category == "analytics_display_only_candidate":
        return f"{field_id}: approximate evidence is display-only and not parser restoration."
    if status == "not_a_candidate":
        return f"{field_id}: no parser recovery candidate is available from current evidence."
    return f"{field_id}: {comparison_status} evidence requires review before any later action."


def _packet_id(row: Mapping[str, Any], status: str, category: str) -> str:
    payload = {
        "schema_version": RECOVERY_CANDIDATE_PACKET_SCHEMA_VERSION,
        "field_id": _safe_text(row.get("field_id", "unknown.field")),
        "comparison_status": _safe_text(row.get("comparison_status", "review_required")),
        "candidate_status": status,
        "candidate_category": category,
        "source_window_refs": _as_string_list(
            _mapping(row.get("current_evidence")).get("source_window_refs")
        ),
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    return f"recovery_candidate:{payload['field_id']}:{digest}"


def _matrix_ref(
    row: Mapping[str, Any],
    matrix: Mapping[str, Any] | None,
) -> dict[str, Any]:
    return {
        "object": field_recovery_matrix.FIELD_RECOVERY_MATRIX_ROW_OBJECT,
        "schema_version": (
            matrix.get("schema_version") if isinstance(matrix, Mapping) else None
        )
        or field_recovery_matrix.FIELD_RECOVERY_MATRIX_SCHEMA_VERSION,
        "field_id": _safe_text(row.get("field_id", "unknown.field")),
        "recovery_category": _safe_text(row.get("recovery_category", "review_required")),
        "parser_output_policy": _safe_text(row.get("parser_output_policy", "manual_review_required")),
        "analytics_output_policy": _safe_text(
            row.get("analytics_output_policy", "must_not_display_as_fact")
        ),
    }


def _comparison_ref(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "object": comparison.FIELD_EVIDENCE_COMPARISON_ROW_OBJECT,
        "schema_version": comparison.FIELD_EVIDENCE_COMPARISON_SCHEMA_VERSION,
        "field_id": _safe_text(row.get("field_id", "unknown.field")),
        "comparison_status": _safe_text(row.get("comparison_status", "review_required")),
        "watcher_window_status": _safe_text(row.get("watcher_window_status", "not_applicable")),
    }


def _expected_summary(value: Any) -> dict[str, Any]:
    expected = _mapping(value)
    return {
        "field_id": _safe_text(expected.get("field_id", "unknown.field")),
        "evidence_ledger_entry_ids": _safe_string_list(expected.get("evidence_ledger_entry_ids")),
        "required_direct_evidence": _safe_string_list(expected.get("required_direct_evidence")),
        "allowed_fallback_evidence": _safe_string_list(expected.get("allowed_fallback_evidence")),
        "forbidden_fallback_evidence": _safe_string_list(
            expected.get("forbidden_fallback_evidence")
        ),
        "expected_recovery_category": _safe_text(
            expected.get("expected_recovery_category", "review_required")
        ),
        "review_required_by_matrix": expected.get("review_required_by_matrix") is True,
    }


def _current_summary(value: Any) -> dict[str, Any]:
    current = _mapping(value)
    return {
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
        "review_required": current.get("review_required") is True,
    }


def _evidence_delta(row: Mapping[str, Any]) -> dict[str, Any]:
    expected = _mapping(row.get("expected_evidence"))
    current = _mapping(row.get("current_evidence"))
    expected_entries = set(_as_string_list(expected.get("evidence_ledger_entry_ids")))
    current_entries = set(_as_string_list(current.get("evidence_ledger_entry_ids")))
    return {
        "comparison_status": _safe_text(row.get("comparison_status", "review_required")),
        "missing_evidence_ledger_entry_ids": sorted(expected_entries - current_entries),
        "extra_evidence_ledger_entry_ids": sorted(current_entries - expected_entries),
        "degradation_flags": _safe_string_list(row.get("degradation_flags")),
        "stop_reasons": _safe_string_list(row.get("stop_reasons")),
    }


def _source_evidence_refs(row: Mapping[str, Any]) -> list[str]:
    current = _mapping(row.get("current_evidence"))
    refs = (
        _safe_string_list(current.get("observed_signal_ids"))
        + _safe_string_list(current.get("source_event_families"))
        + _safe_string_list(current.get("source_event_kinds"))
    )
    return _dedupe_errors(refs)


def _offset_window_refs(row: Mapping[str, Any]) -> list[str]:
    current = _mapping(row.get("current_evidence"))
    return _dedupe_errors(_safe_string_list(current.get("source_window_refs")))


def _packet_stop_reasons(row: Mapping[str, Any], status: str, category: str) -> list[str]:
    reasons = _safe_string_list(row.get("stop_reasons"))
    if status != "candidate_ready_for_review":
        reasons.append(status)
    if category in {"blocked_private_candidate", "blocked_external_candidate"}:
        reasons.append(category)
    return _dedupe_errors(reasons or ["review_packet_created"])


def _privacy_status(row: Mapping[str, Any], status: str) -> str:
    if status == "blocked_privacy":
        return "blocked_local_artifact"
    if _safety_errors(row, "row"):
        return "blocked_local_artifact"
    if status in {"blocked_private_evidence", "blocked_external_boundary"}:
        return "redacted"
    refs = _offset_window_refs(row)
    return "symbolic_only" if refs else "public_safe"


def _reviewer_decision(status: str, category: str, row: Mapping[str, Any]) -> dict[str, Any]:
    next_step = _allowed_next_step(status, category, row)
    return {
        "object": RECOVERY_CANDIDATE_REVIEW_DECISION_OBJECT,
        "decision": "undecided",
        "decision_reason": "not_reviewed",
        "allowed_next_step": next_step,
        "requires_new_issue": next_step in {
            "codex_a_problem_representation",
            "external_boundary_issue",
            "matrix_update_contract",
            "parser_contract",
            "fixture_promotion_contract",
            "corpus_status_contract",
        },
        "requires_private_evidence_approval": status == "blocked_private_evidence",
        "requires_parser_contract": next_step == "parser_contract",
        "requires_fixture_promotion_contract": next_step == "fixture_promotion_contract",
        "requires_corpus_status_contract": next_step == "corpus_status_contract",
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }


def _allowed_next_step(status: str, category: str, row: Mapping[str, Any]) -> str:
    hints = set(_as_string_list(row.get("candidate_recovery_hints")))
    if status == "candidate_ready_for_review":
        return "review_only"
    if status == "blocked_private_evidence":
        return "private_evidence_approval"
    if status == "blocked_external_boundary":
        return "external_boundary_issue"
    if "needs_field_matrix_update" in hints:
        return "matrix_update_contract"
    if "needs_parser_contract" in hints:
        return "parser_contract"
    if "needs_fixture_review" in hints:
        return "fixture_promotion_contract"
    if category == "analytics_display_only_candidate":
        return "no_action"
    if status in {"not_a_candidate", "blocked_privacy", "invalid_input"}:
        return "blocked"
    if category == "unavailable_no_candidate":
        return "no_action"
    return "codex_a_problem_representation"


def _packet_review_required(status: str, row: Mapping[str, Any]) -> bool:
    return status != "candidate_ready_for_review" or row.get("review_required") is True


def _next_role_hint(status: str, category: str) -> str:
    if status == "candidate_ready_for_review":
        return "review_only"
    if status in {
        "blocked_private_evidence",
        "blocked_external_boundary",
        "blocked_privacy",
        "blocked_authorization",
        "blocked_unsupported_claim",
        "invalid_input",
    }:
        return "blocked"
    if category == "unavailable_no_candidate":
        return "no_action"
    return "codex_a_problem_representation"


def _report_status(packets: Sequence[Mapping[str, Any]]) -> str:
    if not packets:
        return "empty"
    statuses = {packet.get("candidate_status") for packet in packets}
    if statuses == {"blocked_private_evidence"}:
        return "blocked_private_evidence"
    if statuses == {"blocked_external_boundary"}:
        return "blocked_external_boundary"
    if statuses <= {"candidate_ready_for_review"}:
        return "candidate_packets_ready"
    return "review_required"


def _status_reasons(packets: Sequence[Mapping[str, Any]]) -> list[str]:
    if not packets:
        return ["no_candidate_packets"]
    reasons = [str(packet.get("candidate_status")) for packet in packets]
    return _dedupe_errors(reasons)


def _summary(packets: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "packet_count": len(packets),
        "candidate_status_counts": _count_values(packets, "candidate_status", CANDIDATE_STATUSES),
        "candidate_category_counts": _count_values(
            packets,
            "candidate_category",
            CANDIDATE_CATEGORIES,
        ),
        "review_required_count": sum(1 for packet in packets if packet.get("review_required") is True),
        "summary_is_readiness_metric": False,
    }


def _privacy_summary() -> dict[str, bool]:
    return {flag: False for flag in PRIVACY_FALSE_FLAGS}


def _protected_surface_assertions() -> dict[str, bool]:
    return {flag: False for flag in PROTECTED_SURFACE_FLAGS}


def _watcher_schema_version(value: Any) -> str:
    if isinstance(value, Mapping):
        return str(value.get("schema_version") or "unknown")
    return "not_applicable"


def _input_errors(*values: Any) -> list[str]:
    errors: list[str] = []
    for index, value in enumerate(values):
        label = f"input[{index}]"
        errors.extend(_safety_errors(value, label))
    return _dedupe_errors(errors)


def _safety_errors(value: Any, path: str) -> list[str]:
    return _dedupe_errors(
        _privacy_errors(value, path)
        + _forbidden_key_errors(value, path)
        + _claim_errors(value, path)
    )


def _packet_validation_errors(packets: Sequence[Mapping[str, Any]]) -> list[str]:
    errors: list[str] = []
    for index, packet in enumerate(packets):
        errors.extend(
            f"packet[{index}]:{error}" for error in validate_recovery_candidate_packet(packet)
        )
    return _dedupe_errors(errors)


def _fatal_error_codes(errors: Sequence[str]) -> list[str]:
    fatal_prefixes = (
        "privacy:",
        "forbidden_key:",
        "claim:",
        "protected_surface:",
    )
    return [error for error in errors if error.startswith(fatal_prefixes)]


def _privacy_errors(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_path = f"{path}.{key}"
            errors.extend(_privacy_errors(item, key_path))
    elif isinstance(value, list | tuple | set):
        for index, item in enumerate(value):
            errors.extend(_privacy_errors(item, f"{path}[{index}]"))
    elif isinstance(value, str):
        if LOCAL_ABSOLUTE_PATH_RE.search(value):
            errors.append(f"privacy:absolute_path:{path}")
        if FORBIDDEN_TEXT_RE.search(value):
            errors.append(f"privacy:forbidden_text:{path}")
    return errors


def _forbidden_key_errors(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            key_path = f"{path}.{key_text}"
            if key_text in FORBIDDEN_KEYS:
                errors.append(f"forbidden_key:{key_path}")
            errors.extend(_forbidden_key_errors(item, key_path))
    elif isinstance(value, list | tuple | set):
        for index, item in enumerate(value):
            errors.extend(_forbidden_key_errors(item, f"{path}[{index}]"))
    return errors


def _claim_errors(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            normalized = _claim_key(key_text)
            key_path = f"{path}.{key_text}"
            if normalized in CLAIM_KEYS and item is not False:
                errors.append(f"claim:{key_path}:must_remain_false")
            if normalized == "protectedsurfaceassertions":
                if not isinstance(item, Mapping):
                    errors.append(f"protected_surface:{key_path}:not_mapping")
                else:
                    for protected_key, protected_value in item.items():
                        protected_path = f"{key_path}.{protected_key}"
                        if protected_value is not False:
                            errors.append(f"protected_surface:{protected_path}:must_remain_false")
                        if _claim_key(str(protected_key)) not in PROTECTED_ASSERTION_KEYS:
                            errors.append(f"protected_surface:{protected_path}:unknown")
            errors.extend(_claim_errors(item, key_path))
    elif isinstance(value, list | tuple | set):
        for index, item in enumerate(value):
            errors.extend(_claim_errors(item, f"{path}[{index}]"))
    return errors


def _claim_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


def _validate_summary(value: Any, packets: Any) -> list[str]:
    if not isinstance(value, Mapping):
        return ["report:summary_not_mapping"]
    packet_list = packets if isinstance(packets, list) else []
    expected = _summary(packet_list)
    errors: list[str] = []
    if value.get("packet_count") != expected["packet_count"]:
        errors.append("report:summary:packet_count_mismatch")
    if value.get("candidate_status_counts") != expected["candidate_status_counts"]:
        errors.append("report:summary:candidate_status_counts_mismatch")
    if value.get("candidate_category_counts") != expected["candidate_category_counts"]:
        errors.append("report:summary:candidate_category_counts_mismatch")
    if value.get("review_required_count") != expected["review_required_count"]:
        errors.append("report:summary:review_required_count_mismatch")
    if value.get("summary_is_readiness_metric") is not False:
        errors.append("report:summary:summary_is_readiness_metric_must_be_false")
    return errors


def _count_values(
    rows: Sequence[Mapping[str, Any]],
    key: str,
    allowed_values: Sequence[str],
) -> dict[str, int]:
    return {value: sum(1 for row in rows if row.get(key) == value) for value in allowed_values}


def _validate_false_mapping(value: Any, label: str) -> list[str]:
    if not isinstance(value, Mapping):
        return [f"{label}_not_mapping"]
    errors: list[str] = []
    for key, item in value.items():
        if item is not False:
            errors.append(f"{label}:{key}_must_remain_false")
    return errors


def _validate_non_claims(value: Any, label: str) -> list[str]:
    if list(_as_string_list(value)) != list(REQUIRED_NON_CLAIMS):
        return [f"{label}:mismatch"]
    return []


def _validate_scalar(value: Any, allowed: Sequence[str], label: str, errors: list[str]) -> None:
    if value not in allowed:
        errors.append(f"{label}:unknown:{value}")


def _validate_field_id(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not FIELD_ID_RE.fullmatch(value):
        errors.append(f"{label}:invalid")


def _validate_string_list(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        errors.append(f"{label}_not_string_list")


def _missing_required_fields(value: Mapping[str, Any], required: Sequence[str], label: str) -> list[str]:
    return [f"{label}:missing:{field}" for field in required if field not in value]


def _safe_text(value: Any) -> str:
    return str(value) if isinstance(value, str) else ""


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list | tuple | set):
        return []
    return [_safe_text(item) for item in value if isinstance(item, str)]


def _as_string_list(value: Any) -> list[str]:
    if isinstance(value, list | tuple | set):
        return [str(item) for item in value if isinstance(item, str)]
    return []


def _mapping(value: Any) -> dict[str, Any]:
    return copy.deepcopy(dict(value)) if isinstance(value, Mapping) else {}


def _dedupe_errors(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
