from __future__ import annotations

import copy
import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any

from mythic_edge_parser.app import field_recovery_matrix
from mythic_edge_parser.app import recovery_candidate_packet_generator as candidates

RECOVERY_ISSUE_FIXTURE_DRAFT_REPORT_OBJECT = (
    "mythic_edge_parser_recovery_issue_fixture_draft_report"
)
RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION = (
    "parser_recovery_issue_fixture_draft_generator.v1"
)
RECOVERY_ISSUE_DRAFT_OBJECT = "mythic_edge_parser_recovery_issue_draft"
RECOVERY_FIXTURE_DRAFT_SUMMARY_OBJECT = (
    "mythic_edge_parser_recovery_fixture_draft_summary"
)
RECOVERY_MANIFEST_DRAFT_SUMMARY_OBJECT = (
    "mythic_edge_parser_recovery_manifest_draft_summary"
)
RECOVERY_DRAFT_REVIEW_CHECKLIST_OBJECT = (
    "mythic_edge_parser_recovery_draft_review_checklist"
)

SOURCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/455"
PIPELINE_TRACKER = "https://github.com/Tahjali11/Mythic-Edge/issues/388"
PARENT_PRIVATE_EVIDENCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/434"
PREVIOUS_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/454"
PREVIOUS_PR = "https://github.com/Tahjali11/Mythic-Edge/pull/546"

REPORT_STATUSES = (
    "drafts_ready_for_review",
    "empty",
    "review_required",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "invalid_input",
    "fail_closed",
)
DRAFT_STATUSES = (
    "draft_ready_for_review",
    "review_required",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "blocked_authorization",
    "blocked_privacy",
    "blocked_overclaim",
    "not_a_draft_candidate",
    "insufficient_packet_review",
    "insufficient_fixture_basis",
    "insufficient_manifest_basis",
    "conflict",
    "invalid_input",
)
DRAFT_TYPES = (
    "issue_only_review_draft",
    "issue_plus_fixture_summary_draft",
    "issue_plus_manifest_summary_draft",
    "issue_fixture_manifest_review_draft",
    "blocked_private_evidence_summary",
    "blocked_external_boundary_summary",
    "no_action_summary",
    "review_required_summary",
)
FIXTURE_EVIDENCE_CLASSES = (
    "synthetic_only_candidate",
    "committed_sanitized_candidate",
    "metadata_only_candidate",
    "private_gated_candidate",
    "external_gated_candidate",
    "blocked_no_fixture_candidate",
    "review_required_candidate",
)
EXPECTED_SECTIONS = (
    "router_stats",
    "event_family_counts",
    "event_kind_sequence",
    "diagnostics_summary",
    "truncation_and_data_loss",
    "unknowns_and_degradation",
    "parser_state",
    "final_reconciliation",
    "parser_owned_rows",
)
NEXT_ROLE_HINTS = (
    "codex_a_problem_representation",
    "codex_b_contract",
    "review_only",
    "blocked",
    "no_action",
)
REQUIRED_NON_CLAIMS = (
    "not_parser_truth",
    "not_issue_creation_authority",
    "not_pr_creation_authority",
    "not_file_writing_authorization",
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
READINESS_FLAGS = (
    "parser_behavior_ready",
    "pipeline_activation_ready_for_issue_388",
    "field_recovery_ready",
)
AUTHORIZATION_FLAGS = (
    "file_writing_authorized",
    "private_harvest_authorized",
    "fixture_promotion_authorized",
    "corpus_status_change_authorized",
    "implementation_authorized",
    "issue_creation_authorized",
    "pr_creation_authorized",
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
    "github_issue_or_pr_lifecycle_changed",
)
PRIVACY_FALSE_FLAGS = (
    "contents_read",
    "raw_path_included",
    "raw_hash_included",
    "raw_payload_values_included",
    "private_excerpt_included",
    "local_state_written",
    "draft_file_written",
    "github_issue_created",
    "github_pr_created",
)

REQUIRED_REPORT_FIELDS = (
    "object",
    "schema_version",
    "source_issue",
    "pipeline_tracker",
    "parent_private_evidence_issue",
    "previous_issue",
    "previous_pr",
    "status",
    "status_reasons",
    "source_packet_report_ref",
    "drafts",
    "summary",
    "privacy",
    "protected_surface_assertions",
    "readiness_flags",
    "authorization_flags",
    "limitations",
    "non_claims",
)
REQUIRED_DRAFT_GROUP_FIELDS = (
    "draft_group_id",
    "source_packet_id",
    "field_id",
    "field_family",
    "draft_status",
    "draft_type",
    "issue_draft",
    "fixture_draft_summary",
    "manifest_draft_summary",
    "review_checklist",
    "stop_reasons",
    "next_role_hint",
    "non_claims",
)
REQUIRED_ISSUE_DRAFT_FIELDS = (
    "object",
    "schema_version",
    "draft_id",
    "draft_status",
    "title",
    "body_sections",
    "refs",
    "suggested_labels",
    "suggested_tracker_update",
    "lifecycle_wording_status",
    "forbidden_lifecycle_terms_found",
    "privacy_status",
    "protected_surface_assertions",
    "readiness_flags",
    "authorization_flags",
    "non_claims",
)
REQUIRED_FIXTURE_SUMMARY_FIELDS = (
    "object",
    "schema_version",
    "draft_id",
    "draft_status",
    "source_packet_id",
    "confidence",
    "finality",
    "degradation_flags",
    "candidate_status",
    "fixture_evidence_class",
    "scenario_family",
    "event_family_scope",
    "expected_parser_fact_scope",
    "minimal_window_summary",
    "proposed_fixture_path",
    "file_writing_authorized",
    "fixture_promotion_authorized",
    "forbidden_content_summary",
    "review_gates",
    "non_claims",
)
REQUIRED_MANIFEST_SUMMARY_FIELDS = (
    "object",
    "schema_version",
    "draft_id",
    "draft_status",
    "source_packet_id",
    "confidence",
    "finality",
    "degradation_flags",
    "candidate_status",
    "proposed_manifest_path",
    "manifest_object",
    "manifest_schema_version",
    "expected_sections",
    "corpus_manifest_change",
    "session_ledger_change",
    "file_writing_authorized",
    "corpus_status_change_authorized",
    "review_gates",
    "non_claims",
)
REQUIRED_CHECKLIST_FIELDS = (
    "object",
    "schema_version",
    "checklist_id",
    "source_packet_id",
    "required_human_checks",
    "required_codex_checks",
    "blocking_questions",
    "privacy_checks",
    "protected_surface_checks",
    "next_role_hint",
    "non_claims",
)

FIELD_ID_RE = re.compile(r"^[a-z0-9_]+(?:\.[a-z0-9_]+)+$")
KNOWN_FIELD_IDS = frozenset(row["field_id"] for row in field_recovery_matrix.iter_field_recovery_rows())
SYMBOLIC_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_.:-]{0,191}$")
ERROR_PATH_COMPONENT_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,160}$")
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
EXACT_PRIVATE_METADATA_VALUE_RE = re.compile(
    r"\b(?:"
    r"offset|start[_-]?offset|end[_-]?offset|"
    r"exact[_-]?(?:offset|start[_-]?offset|end[_-]?offset|"
    r"file[_-]?size(?:[_-]?bytes)?|timestamp)|"
    r"file[_-]?size(?:[_-]?bytes)?|timestamp|"
    r"raw[_-]?hash|content[_-]?hash|hash|sha1|sha256|md5|"
    r"filesystem[_-]?id|inode|archive[_-]?name|source[_-]?generation[_-]?id"
    r")\b\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=:-]{3,}"
    r"|\b\d{4}-\d{2}-\d{2}[tT]\d{2}:\d{2}:\d{2}"
    r"(?:\.\d+)?(?:[zZ]|[+-]\d{2}:?\d{2})?\b",
    re.IGNORECASE,
)
CLOSING_KEYWORD_RE = re.compile(
    r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?|closed by|done by)\s+#?\d+",
    re.IGNORECASE,
)
SOURCE_ACTION_INSTRUCTION_RE = re.compile(
    r"\b(?:open|create|file|submit|stage|commit|push|merge|deploy|release)\s+"
    r"(?:a\s+|an\s+|the\s+)?(?:github\s+)?"
    r"(?:issue|pr|pull\s+request|branch|commit|files?|tracker|release|"
    r"deployment|production|main)\b"
    r"|\b(?:merge|deploy|release)\s+(?:after|when|now|ready)\b",
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
    "file_size",
    "file_size_bytes",
    "filesystem_id",
    "filesystem_ids",
    "hash",
    "hashes",
    "inode",
    "inodes",
    "archive_name",
    "archive_names",
    "source_generation_id",
    "source_generation_ids",
    "private_report_path",
    "local_absolute_path",
    "decklist",
    "card_choices",
    "strategy_notes",
    "close",
    "closes",
    "closed_by",
    "fix",
    "fixes",
    "resolve",
    "resolves",
    "done_by",
}
FORBIDDEN_KEY_NORMALIZATIONS = {
    re.sub(r"[^a-z0-9]", "", key.lower()) for key in FORBIDDEN_KEYS
}
CLAIM_KEYS = {
    re.sub(r"[^a-z0-9]", "", key.lower())
    for key in READINESS_FLAGS + AUTHORIZATION_FLAGS
} | {
    "parserbehaviorready",
    "pipelineactivationreadyforissue388",
    "filewritingauthorized",
    "privateharvestauthorized",
    "fixturepromotionauthorized",
    "corpusstatuschangeauthorized",
    "issuecreationauthorized",
    "prcreationauthorized",
}
SOURCE_ACTION_CLAIM_KEYS = {
    "branch",
    "branchname",
    "commit",
    "commitmessage",
    "commitsha",
    "createbranch",
    "createdraftissue",
    "creategithubissue",
    "creategithubpr",
    "createissue",
    "createpr",
    "createpullrequest",
    "deploy",
    "deployready",
    "deploymentready",
    "fileissue",
    "githubissuecreated",
    "githubprcreated",
    "githubpullrequestcreated",
    "merge",
    "mergeready",
    "openissue",
    "openpr",
    "openpullrequest",
    "production",
    "productionready",
    "push",
    "release",
    "releaseready",
    "sourceissueorprcreated",
    "sourceprcreated",
    "sourcepullrequestcreated",
    "stage",
    "stagefiles",
    "staging",
    "stagingrequested",
    "tracker",
    "trackerupdate",
    "updatetracker",
}
PROTECTED_ASSERTION_KEYS = {
    re.sub(r"[^a-z0-9]", "", key.lower()) for key in PROTECTED_SURFACE_FLAGS
}


def build_recovery_issue_fixture_draft_report(
    *,
    recovery_candidate_packet_report: Mapping[str, Any] | None = None,
    recovery_candidate_packets: Sequence[Mapping[str, Any]] | None = None,
    context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic, public-safe, in-memory issue/fixture draft report."""

    context_payload = copy.deepcopy(dict(context or {}))
    packet_override = recovery_candidate_packets is not None
    packet_report = (
        candidates.build_recovery_candidate_packet_report()
        if recovery_candidate_packet_report is None
        else copy.deepcopy(dict(recovery_candidate_packet_report))
    )
    if packet_override:
        packet_report["packets"] = [copy.deepcopy(dict(packet)) for packet in recovery_candidate_packets]
    input_errors = _safety_errors(context_payload, "context") + _safety_errors(
        packet_report,
        "packet_report",
    )
    packet_report_errors = (
        _packet_override_errors(packet_report.get("packets"))
        if packet_override
        else candidates.validate_recovery_candidate_packet_report(packet_report)
    )
    fatal_errors = _fatal_error_codes(input_errors)
    valid_inputs = not packet_report_errors and not fatal_errors
    drafts = (
        [build_recovery_issue_fixture_draft_group(packet) for packet in packet_report["packets"]]
        if valid_inputs
        else []
    )
    draft_errors = _draft_validation_errors(drafts) if valid_inputs else []
    if draft_errors:
        drafts = []

    status = _report_status(drafts)
    status_reasons = _status_reasons(drafts)
    if packet_report_errors or draft_errors:
        status = "invalid_input"
        status_reasons = _dedupe(
            ["invalid_input"]
            + [f"packet_report:{error}" for error in packet_report_errors]
            + draft_errors
        )
    if fatal_errors:
        status = "fail_closed"
        status_reasons = ["privacy_or_protected_surface_violation"]

    report = {
        "object": RECOVERY_ISSUE_FIXTURE_DRAFT_REPORT_OBJECT,
        "schema_version": RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION,
        "source_issue": SOURCE_ISSUE,
        "pipeline_tracker": PIPELINE_TRACKER,
        "parent_private_evidence_issue": PARENT_PRIVATE_EVIDENCE_ISSUE,
        "previous_issue": PREVIOUS_ISSUE,
        "previous_pr": PREVIOUS_PR,
        "status": status,
        "status_reasons": status_reasons,
        "source_packet_report_ref": _packet_report_ref(packet_report),
        "drafts": drafts,
        "summary": _summary(drafts),
        "privacy": _privacy_summary(),
        "protected_surface_assertions": _protected_surface_assertions(),
        "readiness_flags": _readiness_flags(),
        "authorization_flags": _authorization_flags(),
        "limitations": [
            "in_memory_review_metadata_only",
            "refs_only_lifecycle_wording",
            "no_issue_creation_authorization",
            "no_pr_creation_authorization",
            "no_file_writing_authorization",
            "no_fixture_or_corpus_status_promotion",
            "no_parser_behavior_changes",
            "no_pipeline_activation_readiness",
        ],
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }
    report_errors = _safety_errors(report, "report")
    if report_errors and report["status"] != "fail_closed":
        report["status"] = "fail_closed"
        report["status_reasons"] = ["privacy_or_protected_surface_violation"]
        report["drafts"] = []
        report["summary"] = _summary([])
    return report


def build_recovery_issue_fixture_draft_group(packet: Mapping[str, Any]) -> dict[str, Any]:
    """Build one review-only draft group from a validated recovery candidate packet."""

    packet_copy = copy.deepcopy(dict(packet))
    safety_errors = _safety_errors(packet_copy, "packet")
    draft_status = _draft_status(packet_copy)
    draft_type = _draft_type(packet_copy, draft_status)
    source_packet_id = _safe_symbolic_text(packet_copy.get("packet_id"), "unknown_packet")
    field_id = _safe_field_id(packet_copy.get("field_id"))
    field_family = _safe_symbolic_text(packet_copy.get("field_family"), "unknown")
    group_id = _draft_group_id(packet_copy, draft_status, draft_type)
    issue_draft = build_recovery_issue_draft(packet_copy, draft_status, draft_type, group_id)
    fixture_summary = build_recovery_fixture_draft_summary(
        packet_copy,
        draft_status,
        group_id,
    )
    manifest_summary = build_recovery_manifest_draft_summary(
        packet_copy,
        draft_status,
        group_id,
    )
    checklist = build_recovery_draft_review_checklist(packet_copy, draft_status, group_id)
    group = {
        "draft_group_id": group_id,
        "source_packet_id": source_packet_id,
        "field_id": field_id,
        "field_family": field_family,
        "draft_status": draft_status,
        "draft_type": draft_type,
        "issue_draft": issue_draft,
        "fixture_draft_summary": fixture_summary,
        "manifest_draft_summary": manifest_summary,
        "review_checklist": checklist,
        "stop_reasons": _draft_stop_reasons(packet_copy, draft_status),
        "next_role_hint": _next_role_hint(packet_copy, draft_status),
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }
    if safety_errors or _safety_errors(group, "draft_group"):
        group["draft_status"] = "blocked_privacy"
        group["draft_type"] = "review_required_summary"
        group["next_role_hint"] = "blocked"
        group["stop_reasons"] = _dedupe(group["stop_reasons"] + ["privacy_or_forbidden_marker"])
        group["issue_draft"]["draft_status"] = "blocked_privacy"
        group["fixture_draft_summary"]["draft_status"] = "blocked_privacy"
        group["manifest_draft_summary"]["draft_status"] = "blocked_privacy"
    return group


def build_recovery_issue_draft(
    packet: Mapping[str, Any],
    draft_status: str,
    draft_type: str,
    group_id: str,
) -> dict[str, Any]:
    draft_status = _safe_draft_status(draft_status)
    draft_type = _safe_draft_type(draft_type)
    group_id = _safe_symbolic_text(group_id, "recovery_draft:unknown.field")
    field_id = _safe_field_id(packet.get("field_id"))
    title = f"[parser-recovery] Review recovery candidate for {field_id}"
    body_sections = _issue_body_sections(packet, draft_status, draft_type)
    forbidden_lifecycle_terms_found = _contains_closing_keyword(body_sections)
    return {
        "object": RECOVERY_ISSUE_DRAFT_OBJECT,
        "schema_version": RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION,
        "draft_id": f"issue_draft:{group_id}",
        "draft_status": "blocked_authorization" if forbidden_lifecycle_terms_found else draft_status,
        "title": title,
        "body_sections": body_sections,
        "refs": [
            SOURCE_ISSUE,
            PIPELINE_TRACKER,
            PARENT_PRIVATE_EVIDENCE_ISSUE,
            PREVIOUS_ISSUE,
            PREVIOUS_PR,
        ],
        "suggested_labels": ["parser-recovery", "review-required"],
        "suggested_tracker_update": "review_suggestion_only_refs_no_close",
        "lifecycle_wording_status": "blocked_closing_keyword" if forbidden_lifecycle_terms_found else "refs_only",
        "forbidden_lifecycle_terms_found": forbidden_lifecycle_terms_found,
        "privacy_status": _draft_privacy_status(packet, draft_status),
        "protected_surface_assertions": _protected_surface_assertions(),
        "readiness_flags": _readiness_flags(),
        "authorization_flags": _authorization_flags(),
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }


def build_recovery_fixture_draft_summary(
    packet: Mapping[str, Any],
    draft_status: str,
    group_id: str,
) -> dict[str, Any]:
    draft_status = _safe_draft_status(draft_status)
    group_id = _safe_symbolic_text(group_id, "recovery_draft:unknown.field")
    evidence_class = _fixture_evidence_class(packet, draft_status)
    return {
        "object": RECOVERY_FIXTURE_DRAFT_SUMMARY_OBJECT,
        "schema_version": RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION,
        "draft_id": f"fixture_summary:{group_id}",
        "draft_status": draft_status,
        "source_packet_id": _safe_symbolic_text(packet.get("packet_id"), "unknown_packet"),
        **_source_packet_review_metadata(packet),
        "fixture_evidence_class": evidence_class,
        "scenario_family": _scenario_family(packet, draft_status),
        "event_family_scope": _event_family_scope(packet),
        "expected_parser_fact_scope": _expected_parser_fact_scope(packet),
        "minimal_window_summary": _minimal_window_summary(packet, evidence_class),
        "proposed_fixture_path": "not_applicable",
        "file_writing_authorized": False,
        "fixture_promotion_authorized": False,
        "forbidden_content_summary": _forbidden_content_summary(),
        "review_gates": _review_gates(packet, draft_status),
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }


def build_recovery_manifest_draft_summary(
    packet: Mapping[str, Any],
    draft_status: str,
    group_id: str,
) -> dict[str, Any]:
    draft_status = _safe_draft_status(draft_status)
    group_id = _safe_symbolic_text(group_id, "recovery_draft:unknown.field")
    return {
        "object": RECOVERY_MANIFEST_DRAFT_SUMMARY_OBJECT,
        "schema_version": RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION,
        "draft_id": f"manifest_summary:{group_id}",
        "draft_status": draft_status,
        "source_packet_id": _safe_symbolic_text(packet.get("packet_id"), "unknown_packet"),
        **_source_packet_review_metadata(packet),
        "proposed_manifest_path": "not_applicable",
        "manifest_object": "not_applicable",
        "manifest_schema_version": "not_applicable",
        "expected_sections": _expected_parser_fact_scope(packet),
        "corpus_manifest_change": "not_authorized",
        "session_ledger_change": "not_authorized",
        "file_writing_authorized": False,
        "corpus_status_change_authorized": False,
        "review_gates": _review_gates(packet, draft_status),
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }


def build_recovery_draft_review_checklist(
    packet: Mapping[str, Any],
    draft_status: str,
    group_id: str,
) -> dict[str, Any]:
    draft_status = _safe_draft_status(draft_status)
    group_id = _safe_symbolic_text(group_id, "recovery_draft:unknown.field")
    return {
        "object": RECOVERY_DRAFT_REVIEW_CHECKLIST_OBJECT,
        "schema_version": RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION,
        "checklist_id": f"review_checklist:{group_id}",
        "source_packet_id": _safe_symbolic_text(packet.get("packet_id"), "unknown_packet"),
        "required_human_checks": [
            "confirm_issue_scope_is_one_recovery_candidate",
            "confirm_refs_only_lifecycle_wording",
            "confirm_no_private_or_raw_evidence",
            "confirm_no_fixture_or_corpus_status_claim",
        ],
        "required_codex_checks": [
            "validate_packet_schema",
            "scan_for_private_markers",
            "scan_for_github_closing_keywords",
            "preserve_false_readiness_flags",
        ],
        "blocking_questions": _blocking_questions(packet, draft_status),
        "privacy_checks": [
            "no_raw_player_log",
            "no_raw_utc_log",
            "no_local_absolute_path",
            "no_exact_offsets_sizes_timestamps_or_hashes",
            "no_secrets_or_webhook_urls",
        ],
        "protected_surface_checks": list(PROTECTED_SURFACE_FLAGS),
        "next_role_hint": _next_role_hint(packet, draft_status),
        "non_claims": list(REQUIRED_NON_CLAIMS),
    }


def validate_recovery_issue_fixture_draft_report(report: Mapping[str, Any]) -> list[str]:
    if not isinstance(report, Mapping):
        return ["report:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(report, REQUIRED_REPORT_FIELDS, "report"))
    if report.get("object") != RECOVERY_ISSUE_FIXTURE_DRAFT_REPORT_OBJECT:
        errors.append("report:invalid_object")
    if report.get("schema_version") != RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION:
        errors.append("report:invalid_schema_version")
    if report.get("source_issue") != SOURCE_ISSUE:
        errors.append("report:invalid_source_issue")
    if report.get("pipeline_tracker") != PIPELINE_TRACKER:
        errors.append("report:invalid_pipeline_tracker")
    if report.get("parent_private_evidence_issue") != PARENT_PRIVATE_EVIDENCE_ISSUE:
        errors.append("report:invalid_parent_private_evidence_issue")
    if report.get("previous_issue") != PREVIOUS_ISSUE:
        errors.append("report:invalid_previous_issue")
    if report.get("previous_pr") != PREVIOUS_PR:
        errors.append("report:invalid_previous_pr")
    _validate_scalar(report.get("status"), REPORT_STATUSES, "report:status", errors)
    errors.extend(_validate_false_mapping(report.get("readiness_flags"), READINESS_FLAGS, "report:readiness_flags"))
    errors.extend(
        _validate_false_mapping(
            report.get("authorization_flags"),
            AUTHORIZATION_FLAGS,
            "report:authorization_flags",
        )
    )
    errors.extend(_validate_false_mapping(report.get("privacy"), PRIVACY_FALSE_FLAGS, "report:privacy"))
    errors.extend(
        _validate_false_mapping(
            report.get("protected_surface_assertions"),
            PROTECTED_SURFACE_FLAGS,
            "report:protected_surface_assertions",
        )
    )
    _validate_string_list(report.get("status_reasons"), "report:status_reasons", errors)
    _validate_string_list(report.get("limitations"), "report:limitations", errors)
    errors.extend(_validate_non_claims(report.get("non_claims"), "report:non_claims"))
    drafts = report.get("drafts")
    if not isinstance(drafts, list):
        errors.append("report:drafts_not_list")
    else:
        draft_ids: set[str] = set()
        for index, draft in enumerate(drafts):
            draft_errors = validate_recovery_issue_fixture_draft_group(
                draft if isinstance(draft, Mapping) else {}
            )
            errors.extend(f"report:drafts[{index}]:{error}" for error in draft_errors)
            draft_id = draft.get("draft_group_id") if isinstance(draft, Mapping) else None
            if isinstance(draft_id, str):
                if draft_id in draft_ids:
                    errors.append("report:duplicate_draft_group_id")
                draft_ids.add(draft_id)
    errors.extend(_validate_summary(report.get("summary"), report.get("drafts")))
    errors.extend(_safety_errors(report, "report"))
    return _dedupe(errors)


def validate_recovery_issue_fixture_draft_group(group: Mapping[str, Any]) -> list[str]:
    if not isinstance(group, Mapping):
        return ["draft_group:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(group, REQUIRED_DRAFT_GROUP_FIELDS, "draft_group"))
    _validate_field_id(group.get("field_id"), "draft_group:field_id", errors)
    _validate_scalar(group.get("draft_status"), DRAFT_STATUSES, "draft_group:draft_status", errors)
    _validate_scalar(group.get("draft_type"), DRAFT_TYPES, "draft_group:draft_type", errors)
    _validate_scalar(
        group.get("next_role_hint"),
        NEXT_ROLE_HINTS,
        "draft_group:next_role_hint",
        errors,
    )
    _validate_string_list(group.get("stop_reasons"), "draft_group:stop_reasons", errors)
    errors.extend(validate_recovery_issue_draft(group.get("issue_draft")))
    errors.extend(validate_recovery_fixture_draft_summary(group.get("fixture_draft_summary")))
    errors.extend(validate_recovery_manifest_draft_summary(group.get("manifest_draft_summary")))
    errors.extend(validate_recovery_draft_review_checklist(group.get("review_checklist")))
    errors.extend(_validate_non_claims(group.get("non_claims"), "draft_group:non_claims"))
    errors.extend(_safety_errors(group, "draft_group"))
    return _dedupe(errors)


def validate_recovery_issue_draft(draft: Any) -> list[str]:
    if not isinstance(draft, Mapping):
        return ["issue_draft:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(draft, REQUIRED_ISSUE_DRAFT_FIELDS, "issue_draft"))
    if draft.get("object") != RECOVERY_ISSUE_DRAFT_OBJECT:
        errors.append("issue_draft:invalid_object")
    if draft.get("schema_version") != RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION:
        errors.append("issue_draft:invalid_schema_version")
    _validate_scalar(draft.get("draft_status"), DRAFT_STATUSES, "issue_draft:draft_status", errors)
    if draft.get("lifecycle_wording_status") not in {"refs_only", "blocked_closing_keyword"}:
        errors.append("issue_draft:lifecycle_wording_status_unknown")
    if not isinstance(draft.get("forbidden_lifecycle_terms_found"), bool):
        errors.append("issue_draft:forbidden_lifecycle_terms_found_not_bool")
    if draft.get("forbidden_lifecycle_terms_found") is False:
        if draft.get("lifecycle_wording_status") != "refs_only":
            errors.append("issue_draft:lifecycle_wording_not_refs_only")
    if _contains_closing_keyword(draft):
        errors.append("issue_draft:closing_keyword_found")
    if not isinstance(draft.get("body_sections"), list):
        errors.append("issue_draft:body_sections_not_list")
    _validate_string_list(draft.get("refs"), "issue_draft:refs", errors)
    _validate_string_list(draft.get("suggested_labels"), "issue_draft:suggested_labels", errors)
    errors.extend(
        _validate_false_mapping(
            draft.get("protected_surface_assertions"),
            PROTECTED_SURFACE_FLAGS,
            "issue_draft:protected_surface_assertions",
        )
    )
    errors.extend(
        _validate_false_mapping(draft.get("readiness_flags"), READINESS_FLAGS, "issue_draft:readiness_flags")
    )
    errors.extend(
        _validate_false_mapping(
            draft.get("authorization_flags"),
            AUTHORIZATION_FLAGS,
            "issue_draft:authorization_flags",
        )
    )
    errors.extend(_validate_non_claims(draft.get("non_claims"), "issue_draft:non_claims"))
    errors.extend(_safety_errors(draft, "issue_draft"))
    return _dedupe(errors)


def validate_recovery_fixture_draft_summary(summary: Any) -> list[str]:
    if not isinstance(summary, Mapping):
        return ["fixture_summary:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(summary, REQUIRED_FIXTURE_SUMMARY_FIELDS, "fixture_summary"))
    if summary.get("object") != RECOVERY_FIXTURE_DRAFT_SUMMARY_OBJECT:
        errors.append("fixture_summary:invalid_object")
    if summary.get("schema_version") != RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION:
        errors.append("fixture_summary:invalid_schema_version")
    _validate_scalar(
        summary.get("draft_status"),
        DRAFT_STATUSES,
        "fixture_summary:draft_status",
        errors,
    )
    _validate_scalar(
        summary.get("fixture_evidence_class"),
        FIXTURE_EVIDENCE_CLASSES,
        "fixture_summary:fixture_evidence_class",
        errors,
    )
    _validate_string_list(summary.get("event_family_scope"), "fixture_summary:event_family_scope", errors)
    _validate_string_list(
        summary.get("expected_parser_fact_scope"),
        "fixture_summary:expected_parser_fact_scope",
        errors,
    )
    _validate_source_packet_review_metadata(summary, "fixture_summary", errors)
    if summary.get("file_writing_authorized") is not False:
        errors.append("fixture_summary:file_writing_authorized_must_remain_false")
    if summary.get("fixture_promotion_authorized") is not False:
        errors.append("fixture_summary:fixture_promotion_authorized_must_remain_false")
    errors.extend(_validate_non_claims(summary.get("non_claims"), "fixture_summary:non_claims"))
    errors.extend(_safety_errors(summary, "fixture_summary"))
    return _dedupe(errors)


def validate_recovery_manifest_draft_summary(summary: Any) -> list[str]:
    if not isinstance(summary, Mapping):
        return ["manifest_summary:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(summary, REQUIRED_MANIFEST_SUMMARY_FIELDS, "manifest_summary"))
    if summary.get("object") != RECOVERY_MANIFEST_DRAFT_SUMMARY_OBJECT:
        errors.append("manifest_summary:invalid_object")
    if summary.get("schema_version") != RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION:
        errors.append("manifest_summary:invalid_schema_version")
    _validate_scalar(
        summary.get("draft_status"),
        DRAFT_STATUSES,
        "manifest_summary:draft_status",
        errors,
    )
    expected_sections = summary.get("expected_sections")
    _validate_string_list(expected_sections, "manifest_summary:expected_sections", errors)
    for index, section in enumerate(_as_string_list(expected_sections)):
        if section not in EXPECTED_SECTIONS:
            errors.append(f"manifest_summary:expected_sections[{index}]:unknown")
    _validate_source_packet_review_metadata(summary, "manifest_summary", errors)
    if summary.get("corpus_manifest_change") != "not_authorized":
        errors.append("manifest_summary:corpus_manifest_change_must_be_not_authorized")
    if summary.get("session_ledger_change") != "not_authorized":
        errors.append("manifest_summary:session_ledger_change_must_be_not_authorized")
    if summary.get("file_writing_authorized") is not False:
        errors.append("manifest_summary:file_writing_authorized_must_remain_false")
    if summary.get("corpus_status_change_authorized") is not False:
        errors.append("manifest_summary:corpus_status_change_authorized_must_remain_false")
    errors.extend(_validate_non_claims(summary.get("non_claims"), "manifest_summary:non_claims"))
    errors.extend(_safety_errors(summary, "manifest_summary"))
    return _dedupe(errors)


def validate_recovery_draft_review_checklist(checklist: Any) -> list[str]:
    if not isinstance(checklist, Mapping):
        return ["review_checklist:not_mapping"]
    errors: list[str] = []
    errors.extend(_missing_required_fields(checklist, REQUIRED_CHECKLIST_FIELDS, "review_checklist"))
    if checklist.get("object") != RECOVERY_DRAFT_REVIEW_CHECKLIST_OBJECT:
        errors.append("review_checklist:invalid_object")
    if checklist.get("schema_version") != RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION:
        errors.append("review_checklist:invalid_schema_version")
    for field in (
        "required_human_checks",
        "required_codex_checks",
        "blocking_questions",
        "privacy_checks",
        "protected_surface_checks",
    ):
        _validate_string_list(checklist.get(field), f"review_checklist:{field}", errors)
    _validate_scalar(
        checklist.get("next_role_hint"),
        NEXT_ROLE_HINTS,
        "review_checklist:next_role_hint",
        errors,
    )
    errors.extend(_validate_non_claims(checklist.get("non_claims"), "review_checklist:non_claims"))
    errors.extend(_safety_errors(checklist, "review_checklist"))
    return _dedupe(errors)


def _draft_status(packet: Mapping[str, Any]) -> str:
    candidate_status = str(packet.get("candidate_status") or "invalid_input")
    category = str(packet.get("candidate_category") or "")
    if _safety_errors(packet, "packet"):
        return "blocked_privacy"
    if not _is_known_field_id(packet.get("field_id")):
        return "review_required"
    if candidate_status == "candidate_ready_for_review":
        return "draft_ready_for_review"
    if candidate_status == "review_required":
        return "review_required"
    if candidate_status == "blocked_private_evidence":
        return "blocked_private_evidence"
    if candidate_status == "blocked_external_boundary":
        return "blocked_external_boundary"
    if candidate_status == "blocked_privacy":
        return "blocked_privacy"
    if candidate_status in {"blocked_authorization", "blocked_unsupported_claim"}:
        return "blocked_overclaim" if category == "unsupported_claim_blocked" else "blocked_authorization"
    if candidate_status == "not_a_candidate":
        return "not_a_draft_candidate"
    if candidate_status == "stale_input":
        return "review_required"
    if candidate_status == "conflict":
        return "conflict"
    if candidate_status == "invalid_input":
        return "invalid_input"
    return "review_required"


def _draft_type(packet: Mapping[str, Any], draft_status: str) -> str:
    if draft_status == "blocked_private_evidence":
        return "blocked_private_evidence_summary"
    if draft_status == "blocked_external_boundary":
        return "blocked_external_boundary_summary"
    if draft_status == "not_a_draft_candidate":
        return "no_action_summary"
    if draft_status in {"review_required", "conflict", "invalid_input"}:
        return "review_required_summary"
    if draft_status.startswith("blocked_"):
        return "review_required_summary"
    if packet.get("candidate_status") == "candidate_ready_for_review":
        return "issue_fixture_manifest_review_draft"
    return "issue_only_review_draft"


def _issue_body_sections(
    packet: Mapping[str, Any],
    draft_status: str,
    draft_type: str,
) -> list[dict[str, str]]:
    field_id = _safe_field_id(packet.get("field_id"))
    packet_id = _safe_symbolic_text(packet.get("packet_id"), "unknown_packet")
    candidate_status = _safe_symbolic_text(packet.get("candidate_status"), "unknown")
    return [
        {
            "section": "problem",
            "body": f"Refs #455, #388, #434, and #454. Review parser recovery candidate {field_id}.",
        },
        {
            "section": "source_packet_summary",
            "body": (
                f"Source packet {packet_id} "
                f"has candidate status {candidate_status} "
                f"and draft status {draft_status}."
            ),
        },
        {
            "section": "evidence_basis",
            "body": "Use public-safe symbolic packet evidence only; do not include raw log lines or private paths.",
        },
        {
            "section": "proposed_scope",
            "body": f"Draft type {draft_type}; review-only and not parser behavior authority.",
        },
        {
            "section": "proposed_fixture_summary",
            "body": "Fixture summary is in-memory review metadata only; no fixture file is authorized.",
        },
        {
            "section": "proposed_manifest_summary",
            "body": "Manifest summary is in-memory review metadata only; no manifest write is authorized.",
        },
        {
            "section": "required_review_questions",
            "body": "Confirm privacy, scope, parser-truth boundary, and whether a later Codex A issue is needed.",
        },
        {
            "section": "protected_boundaries",
            "body": (
                "No private harvest, file writing, fixture promotion, corpus status change, "
                "issue creation, or PR creation."
            ),
        },
        {
            "section": "validation_expectations",
            "body": "Future implementation must run focused draft-generator tests and adjacent recovery tests.",
        },
        {
            "section": "non_claims",
            "body": (
                "This draft is not parser truth, readiness, fixture promotion, corpus status, "
                "analytics truth, AI truth, or coaching truth."
            ),
        },
        {
            "section": "workflow_handoff_stub",
            "body": "Next role is Codex A or Codex B unless a later issue explicitly authorizes implementation.",
        },
    ]


def _fixture_evidence_class(packet: Mapping[str, Any], draft_status: str) -> str:
    if draft_status == "blocked_private_evidence":
        return "private_gated_candidate"
    if draft_status == "blocked_external_boundary":
        return "external_gated_candidate"
    if draft_status in {
        "blocked_authorization",
        "blocked_privacy",
        "blocked_overclaim",
        "not_a_draft_candidate",
        "invalid_input",
    }:
        return "blocked_no_fixture_candidate"
    refs = _safe_symbolic_list(packet.get("source_evidence_refs"))
    if any("synthetic" in ref for ref in refs):
        return "synthetic_only_candidate"
    if draft_status == "draft_ready_for_review":
        return "metadata_only_candidate"
    return "review_required_candidate"


def _source_packet_review_metadata(packet: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "confidence": _safe_symbolic_text(packet.get("confidence"), "unknown"),
        "finality": _safe_symbolic_text(packet.get("finality"), "unknown"),
        "degradation_flags": _safe_symbolic_list(packet.get("degradation_flags")),
        "candidate_status": _safe_symbolic_text(packet.get("candidate_status"), "unknown"),
    }


def _scenario_family(packet: Mapping[str, Any], draft_status: str) -> str:
    if draft_status.startswith("blocked_"):
        return "review_required"
    return _safe_symbolic_text(packet.get("field_family"), "review_required")


def _event_family_scope(packet: Mapping[str, Any]) -> list[str]:
    refs = _safe_symbolic_list(packet.get("source_evidence_refs"))
    families = [ref for ref in refs if "." not in ref or ref.startswith("synthetic")]
    return _dedupe(families) or ["review_required"]


def _expected_parser_fact_scope(packet: Mapping[str, Any]) -> list[str]:
    field_id = _safe_field_id(packet.get("field_id"))
    if field_id.startswith("runtime_health."):
        return ["diagnostics_summary", "unknowns_and_degradation"]
    if field_id.startswith(("match.", "game.")):
        return ["parser_state", "final_reconciliation", "parser_owned_rows"]
    return ["parser_owned_rows"]


def _minimal_window_summary(packet: Mapping[str, Any], evidence_class: str) -> dict[str, Any]:
    return {
        "summary_kind": "symbolic_count_only",
        "source_packet_id": _safe_symbolic_text(packet.get("packet_id"), "unknown_packet"),
        "offset_window_refs": _safe_symbolic_list(packet.get("offset_window_refs")),
        "fixture_evidence_class": evidence_class,
        "raw_lines_included": False,
        "private_paths_included": False,
        "exact_offsets_sizes_timestamps_or_hashes_included": False,
    }


def _forbidden_content_summary() -> dict[str, bool]:
    return {
        "raw_player_log_included": False,
        "raw_utc_log_included": False,
        "local_absolute_path_included": False,
        "raw_payload_included": False,
        "secret_included": False,
        "github_closing_keyword_included": False,
    }


def _review_gates(packet: Mapping[str, Any], draft_status: str) -> list[str]:
    gates = [
        "human_review_required",
        "privacy_scan_required",
        "protected_surface_review_required",
        "refs_only_lifecycle_review_required",
    ]
    if draft_status != "draft_ready_for_review":
        gates.append("scope_or_evidence_review_required")
    if packet.get("candidate_status") == "blocked_private_evidence":
        gates.append("private_evidence_approval_required")
    if packet.get("candidate_status") == "blocked_external_boundary":
        gates.append("external_boundary_issue_required")
    return gates


def _blocking_questions(packet: Mapping[str, Any], draft_status: str) -> list[str]:
    questions = [
        "Does this draft preserve parser truth ownership?",
        "Does this draft avoid issue or PR lifecycle side effects?",
        "Does this draft avoid private/raw evidence?",
    ]
    if draft_status != "draft_ready_for_review":
        questions.append("What additional contract or review is required before action?")
    if packet.get("candidate_status") == "blocked_private_evidence":
        questions.append("Has parent private-evidence issue #434 authorized the exact source and window?")
    return questions


def _draft_stop_reasons(packet: Mapping[str, Any], draft_status: str) -> list[str]:
    reasons = _safe_symbolic_list(packet.get("stop_reasons"))
    if draft_status != "draft_ready_for_review":
        reasons.append(draft_status)
    return _dedupe(reasons or ["draft_created_for_review"])


def _next_role_hint(packet: Mapping[str, Any], draft_status: str) -> str:
    if draft_status == "draft_ready_for_review":
        return "review_only"
    if draft_status in {"blocked_private_evidence", "blocked_external_boundary"}:
        return "codex_a_problem_representation"
    if draft_status in {"not_a_draft_candidate"}:
        return "no_action"
    if draft_status.startswith("blocked_") or draft_status == "invalid_input":
        return "blocked"
    if packet.get("next_role_hint") == "blocked":
        return "blocked"
    return "codex_a_problem_representation"


def _draft_privacy_status(packet: Mapping[str, Any], draft_status: str) -> str:
    if draft_status == "blocked_privacy":
        return "blocked_privacy"
    if draft_status == "blocked_private_evidence":
        return "redacted"
    if packet.get("privacy_status") == "symbolic_only":
        return "symbolic_only"
    return "public_safe"


def _packet_report_ref(packet_report: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "object": candidates.RECOVERY_CANDIDATE_PACKET_REPORT_OBJECT,
        "schema_version": packet_report.get("schema_version")
        or candidates.RECOVERY_CANDIDATE_PACKET_SCHEMA_VERSION,
        "status": _safe_symbolic_text(packet_report.get("status"), "unknown"),
        "packet_count": len(packet_report.get("packets", []))
        if isinstance(packet_report.get("packets"), list)
        else 0,
    }


def _draft_group_id(packet: Mapping[str, Any], draft_status: str, draft_type: str) -> str:
    payload = {
        "schema_version": RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION,
        "packet_id": _safe_symbolic_text(packet.get("packet_id"), "unknown_packet"),
        "field_id": _safe_field_id(packet.get("field_id")),
        "field_family": _safe_symbolic_text(packet.get("field_family"), "unknown"),
        "draft_status": draft_status,
        "draft_type": draft_type,
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    return f"recovery_draft:{payload['field_id']}:{digest}"


def _report_status(drafts: Sequence[Mapping[str, Any]]) -> str:
    if not drafts:
        return "empty"
    statuses = {draft.get("draft_status") for draft in drafts}
    if any(status in {"blocked_privacy", "blocked_authorization", "blocked_overclaim"} for status in statuses):
        return "fail_closed"
    if statuses == {"blocked_private_evidence"}:
        return "blocked_private_evidence"
    if statuses == {"blocked_external_boundary"}:
        return "blocked_external_boundary"
    if statuses <= {"draft_ready_for_review"}:
        return "drafts_ready_for_review"
    return "review_required"


def _status_reasons(drafts: Sequence[Mapping[str, Any]]) -> list[str]:
    if not drafts:
        return ["no_drafts"]
    return _dedupe([str(draft.get("draft_status")) for draft in drafts])


def _summary(drafts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "draft_count": len(drafts),
        "draft_status_counts": _count_values(drafts, "draft_status", DRAFT_STATUSES),
        "draft_type_counts": _count_values(drafts, "draft_type", DRAFT_TYPES),
        "review_required_count": sum(
            1 for draft in drafts if draft.get("draft_status") == "review_required"
        ),
        "summary_is_readiness_metric": False,
    }


def _privacy_summary() -> dict[str, bool]:
    return {flag: False for flag in PRIVACY_FALSE_FLAGS}


def _protected_surface_assertions() -> dict[str, bool]:
    return {flag: False for flag in PROTECTED_SURFACE_FLAGS}


def _readiness_flags() -> dict[str, bool]:
    return {flag: False for flag in READINESS_FLAGS}


def _authorization_flags() -> dict[str, bool]:
    return {flag: False for flag in AUTHORIZATION_FLAGS}


def _draft_validation_errors(drafts: Sequence[Mapping[str, Any]]) -> list[str]:
    errors: list[str] = []
    for index, draft in enumerate(drafts):
        errors.extend(
            f"draft[{index}]:{error}"
            for error in validate_recovery_issue_fixture_draft_group(draft)
        )
    return _dedupe(errors)


def _packet_override_errors(value: Any) -> list[str]:
    if not isinstance(value, list):
        return ["packets:not_list"]
    errors: list[str] = []
    packet_ids: set[str] = set()
    for index, packet in enumerate(value):
        if not isinstance(packet, Mapping):
            errors.append(f"packets[{index}]:not_mapping")
            continue
        errors.extend(
            f"packets[{index}]:{error}"
            for error in candidates.validate_recovery_candidate_packet(packet)
        )
        packet_id = packet.get("packet_id")
        if isinstance(packet_id, str):
            if packet_id in packet_ids:
                errors.append("packets:duplicate_packet_id")
            packet_ids.add(packet_id)
    return _dedupe(errors)


def _fatal_error_codes(errors: Sequence[str]) -> list[str]:
    fatal_prefixes = (
        "privacy:",
        "forbidden_key:",
        "claim:",
        "protected_surface:",
        "lifecycle:",
        "source_action:",
    )
    return [error for error in errors if error.startswith(fatal_prefixes)]


def _safety_errors(value: Any, path: str) -> list[str]:
    return _dedupe(
        _privacy_errors(value, path)
        + _forbidden_key_errors(value, path)
        + _claim_errors(value, path)
        + _source_action_errors(value, path)
        + _lifecycle_errors(value, path)
    )


def _privacy_errors(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            key_label = _safe_error_path_component(key_text)
            key_path = f"{path}.{key_label}"
            if _unsafe_text(key_text):
                errors.append(f"privacy:unsafe_key:{key_path}")
            errors.extend(_privacy_errors(item, key_path))
    elif isinstance(value, list | tuple | set):
        for index, item in enumerate(value):
            errors.extend(_privacy_errors(item, f"{path}[{index}]"))
    elif isinstance(value, str):
        if LOCAL_ABSOLUTE_PATH_RE.search(value):
            errors.append(f"privacy:absolute_path:{path}")
        if FORBIDDEN_TEXT_RE.search(value):
            errors.append(f"privacy:forbidden_text:{path}")
        if EXACT_PRIVATE_METADATA_VALUE_RE.search(value):
            errors.append(f"privacy:exact_private_metadata:{path}")
    return errors


def _forbidden_key_errors(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            key_path = f"{path}.{_safe_error_path_component(key_text)}"
            if (
                key_text in FORBIDDEN_KEYS
                or _claim_key(key_text) in FORBIDDEN_KEY_NORMALIZATIONS
            ):
                errors.append(f"forbidden_key:{key_path}")
            errors.extend(_forbidden_key_errors(item, key_path))
    elif isinstance(value, list | tuple | set):
        for index, item in enumerate(value):
            errors.extend(_forbidden_key_errors(item, f"{path}[{index}]"))
    return errors


def _source_action_errors(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            normalized = _claim_key(key_text)
            key_path = f"{path}.{_safe_error_path_component(key_text)}"
            if normalized in SOURCE_ACTION_CLAIM_KEYS and item is not False:
                errors.append(f"source_action:{key_path}:must_remain_false")
            errors.extend(_source_action_errors(item, key_path))
    elif isinstance(value, list | tuple | set):
        for index, item in enumerate(value):
            errors.extend(_source_action_errors(item, f"{path}[{index}]"))
    elif isinstance(value, str) and SOURCE_ACTION_INSTRUCTION_RE.search(value):
        errors.append(f"source_action:instruction:{path}")
    return errors


def _claim_errors(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            normalized = _claim_key(key_text)
            key_path = f"{path}.{_safe_error_path_component(key_text)}"
            if normalized in CLAIM_KEYS and item is not False:
                errors.append(f"claim:{key_path}:must_remain_false")
            if normalized in PROTECTED_ASSERTION_KEYS and item is not False:
                errors.append(f"protected_surface:{key_path}:must_remain_false")
            if normalized == "protectedsurfaceassertions":
                if not isinstance(item, Mapping):
                    errors.append(f"protected_surface:{key_path}:not_mapping")
                else:
                    for protected_key, protected_value in item.items():
                        protected_path = (
                            f"{key_path}.{_safe_error_path_component(str(protected_key))}"
                        )
                        if protected_value is not False:
                            errors.append(f"protected_surface:{protected_path}:must_remain_false")
                        if _claim_key(str(protected_key)) not in PROTECTED_ASSERTION_KEYS:
                            errors.append(f"protected_surface:{protected_path}:unknown")
            errors.extend(_claim_errors(item, key_path))
    elif isinstance(value, list | tuple | set):
        for index, item in enumerate(value):
            errors.extend(_claim_errors(item, f"{path}[{index}]"))
    return errors


def _lifecycle_errors(value: Any, path: str) -> list[str]:
    errors: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            key_path = f"{path}.{_safe_error_path_component(key_text)}"
            if CLOSING_KEYWORD_RE.search(key_text):
                errors.append(f"lifecycle:closing_keyword:{key_path}")
            errors.extend(_lifecycle_errors(item, key_path))
    elif isinstance(value, list | tuple | set):
        for index, item in enumerate(value):
            errors.extend(_lifecycle_errors(item, f"{path}[{index}]"))
    elif isinstance(value, str) and CLOSING_KEYWORD_RE.search(value):
        errors.append(f"lifecycle:closing_keyword:{path}")
    return errors


def _contains_closing_keyword(value: Any) -> bool:
    return bool(_lifecycle_errors(value, "value"))


def _validate_summary(value: Any, drafts: Any) -> list[str]:
    if not isinstance(value, Mapping):
        return ["report:summary_not_mapping"]
    draft_list = drafts if isinstance(drafts, list) else []
    expected = _summary(draft_list)
    errors: list[str] = []
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            errors.append(f"report:summary:{key}_mismatch")
    if value.get("summary_is_readiness_metric") is not False:
        errors.append("report:summary:summary_is_readiness_metric_must_be_false")
    return errors


def _validate_false_mapping(
    value: Any,
    expected_keys: Sequence[str],
    label: str,
) -> list[str]:
    if not isinstance(value, Mapping):
        return [f"{label}_not_mapping"]
    errors: list[str] = []
    for key in expected_keys:
        if value.get(key) is not False:
            errors.append(f"{label}:{key}_must_remain_false")
    for key in value:
        if key not in expected_keys:
            errors.append(f"{label}:unknown_key")
    return errors


def _validate_non_claims(value: Any, label: str) -> list[str]:
    if list(_as_string_list(value)) != list(REQUIRED_NON_CLAIMS):
        return [f"{label}:mismatch"]
    return []


def _validate_scalar(value: Any, allowed: Sequence[str], label: str, errors: list[str]) -> None:
    if value not in allowed:
        errors.append(f"{label}:unknown")


def _validate_source_packet_review_metadata(
    summary: Mapping[str, Any],
    label: str,
    errors: list[str],
) -> None:
    for field in ("confidence", "finality"):
        if not isinstance(summary.get(field), str) or not SYMBOLIC_ID_RE.fullmatch(summary[field]):
            errors.append(f"{label}:{field}:invalid")
    _validate_scalar(
        summary.get("candidate_status"),
        (*candidates.CANDIDATE_STATUSES, "unknown"),
        f"{label}:candidate_status",
        errors,
    )
    _validate_string_list(summary.get("degradation_flags"), f"{label}:degradation_flags", errors)
    for index, flag in enumerate(_as_string_list(summary.get("degradation_flags"))):
        if not SYMBOLIC_ID_RE.fullmatch(flag):
            errors.append(f"{label}:degradation_flags[{index}]:invalid")


def _validate_field_id(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not FIELD_ID_RE.fullmatch(value):
        errors.append(f"{label}:invalid")


def _is_known_field_id(value: Any) -> bool:
    return isinstance(value, str) and FIELD_ID_RE.fullmatch(value) is not None and value in KNOWN_FIELD_IDS


def _validate_string_list(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        errors.append(f"{label}_not_string_list")


def _missing_required_fields(value: Mapping[str, Any], required: Sequence[str], label: str) -> list[str]:
    return [f"{label}:missing:{field}" for field in required if field not in value]


def _count_values(
    rows: Sequence[Mapping[str, Any]],
    key: str,
    allowed_values: Sequence[str],
) -> dict[str, int]:
    return {value: sum(1 for row in rows if row.get(key) == value) for value in allowed_values}


def _claim_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


def _safe_text(value: Any, fallback: str = "") -> str:
    if not isinstance(value, str):
        return fallback
    if _unsafe_text(value):
        return fallback
    return value


def _safe_symbolic_text(value: Any, fallback: str) -> str:
    text = _safe_text(value, fallback)
    if not SYMBOLIC_ID_RE.fullmatch(text):
        return fallback
    return text


def _safe_field_id(value: Any) -> str:
    text = _safe_text(value, "unknown.field")
    if not FIELD_ID_RE.fullmatch(text):
        return "unknown.field"
    return text


def _safe_draft_status(value: Any) -> str:
    return value if isinstance(value, str) and value in DRAFT_STATUSES else "invalid_input"


def _safe_draft_type(value: Any) -> str:
    return value if isinstance(value, str) and value in DRAFT_TYPES else "review_required_summary"


def _safe_symbolic_list(value: Any) -> list[str]:
    return [
        text
        for text in (_safe_symbolic_text(item, "") for item in _as_string_list(value))
        if text
    ]


def _unsafe_text(value: str) -> bool:
    return bool(
        LOCAL_ABSOLUTE_PATH_RE.search(value)
        or FORBIDDEN_TEXT_RE.search(value)
        or EXACT_PRIVATE_METADATA_VALUE_RE.search(value)
        or CLOSING_KEYWORD_RE.search(value)
    )


def _safe_error_path_component(value: str) -> str:
    if _unsafe_text(value) or not ERROR_PATH_COMPONENT_RE.fullmatch(value):
        return "redacted_key"
    return value


def _as_string_list(value: Any) -> list[str]:
    if isinstance(value, list | tuple | set):
        return [str(item) for item in value if isinstance(item, str)]
    return []


def _dedupe(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result
