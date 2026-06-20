"""Synthetic-only corpus metadata diff object builder."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any, Literal
from urllib.parse import unquote

from mythic_edge_parser.app.fixture_promotion_proof import (
    FIXTURE_PROMOTION_PROOF_OBJECT,
    FIXTURE_PROMOTION_PROOF_SCHEMA_VERSION,
)
from mythic_edge_parser.app.local_harvest_candidate_reports import DEFAULT_CREATED_AT_UTC

CORPUS_METADATA_DIFF_OBJECT = "mythic_edge_corpus_metadata_diff"
CORPUS_METADATA_DIFF_SCHEMA_VERSION = "parser_evidence_corpus_metadata_diff.v1"
CORPUS_MANIFEST_OBJECT = "mythic_edge_parser_corpus_manifest"
CORPUS_MANIFEST_SCHEMA_VERSION = "parser_corpus_manifest.v1"
SESSION_LEDGER_OBJECT = "mythic_edge_parser_corpus_session_ledger"
SESSION_LEDGER_SCHEMA_VERSION = "parser_corpus_session_ledger.v1"

DEFAULT_CORPUS_MANIFEST_TARGET = "tests/fixtures/parser_corpus/corpus_manifest.v1.json"
DEFAULT_SESSION_LEDGER_TARGET = "tests/fixtures/parser_corpus/session_ledger.v1.json"

DiffStatus = Literal[
    "draft",
    "blocked_privacy",
    "blocked_authorization",
    "insufficient_proof",
    "no_metadata_change",
    "diff_ready_for_review",
    "diff_rejected",
    "blocked_overclaim",
    "needs_contract_update",
]
ProposedChangeType = Literal[
    "no_change",
    "add_manifest_entry",
    "add_session_entry",
    "update_existing_manifest_entry",
    "update_existing_session_entry",
    "status_promotion_candidate",
    "status_correction_candidate",
    "known_gap_update_candidate",
    "review_note_update_candidate",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "needs_contract_update",
    "unknown",
]
CoverageTransitionKind = Literal[
    "no_change",
    "report_only_to_synthetic_candidate",
    "report_only_to_committed_candidate",
    "partial_to_synthetic_candidate",
    "partial_to_committed_candidate",
    "missing_to_report_only_candidate",
    "missing_to_synthetic_candidate",
    "blocked_private_evidence_no_change",
    "blocked_external_boundary_no_change",
    "status_correction_candidate",
    "unknown",
]

DIFF_STATUSES = frozenset(DiffStatus.__args__)
PROPOSED_CHANGE_TYPES = frozenset(ProposedChangeType.__args__)
COVERAGE_TRANSITION_KINDS = frozenset(CoverageTransitionKind.__args__)

MANIFEST_ENTRY_TYPES = frozenset(
    {
        "diagnostics_report",
        "external_reference_category",
        "feature_equity_report",
        "golden_replay_manifest",
        "local_private_report_summary",
        "session_ledger_entry",
    },
)
SOURCE_KINDS = frozenset(
    {
        "committed_count_only_report",
        "external_reference_only",
        "local_private_report_only",
        "sanitized_committed_fixture",
        "synthetic_committed_fixture",
    },
)
MANIFEST_COMMIT_STATUSES = frozenset({"committed", "external_reference_only", "local_report_only"})
SESSION_COMMIT_STATUSES = frozenset({"committed"})
PRIVACY_CLASSES = frozenset(
    {
        "committed_count_only",
        "external_reference_metadata_only",
        "local_private_not_committed",
        "sanitized_committable",
        "synthetic_committable",
    },
)
PRIVATE_PRIVACY_CLASSES = frozenset({"local_private_not_committed"})
SANITIZATION_STATUSES = frozenset(
    {
        "not_applicable_count_only",
        "not_applicable_external_reference",
        "requires_review",
        "sanitized",
        "synthetic",
    },
)
COVERAGE_STATUSES = frozenset(
    {
        "blocked_external_boundary",
        "blocked_private_evidence",
        "covered_committed",
        "covered_report_only",
        "covered_synthetic",
        "partial",
    },
)
COVERAGE_BASIS_VALUES = frozenset(
    {
        "count_ratchet_only",
        "diagnostics_only",
        "evidence_ledger_only",
        "external_reference_only",
        "fixture_metadata_only",
        "local_report_only",
        "parser_behavior_verified",
    },
)
SESSION_REDACTION_FLAGS = frozenset(
    {
        "raw_log_lines_included",
        "private_paths_included",
        "raw_payloads_included",
        "local_private_artifacts_included",
        "generated_private_artifacts_included",
    },
)

_SYMBOLIC_TEXT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_FIELD_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_SENSITIVE_KEY_RE = re.compile(
    r"(^|_)(raw|payload|payloads|content|text|line|lines|hash|hashes|offset|offsets|bytes|byte_range|"
    r"file_size|timestamp_window|secret|token|api_key|credential|webhook)($|_)",
    re.IGNORECASE,
)
_SAFE_FALSE_FLAG_KEYS = frozenset(
    {
        "raw_source_committed",
        "raw_path_included",
        "raw_hash_included",
        "raw_content_included",
        "raw_log_lines_included",
        "raw_payloads_included",
        "raw_private_logs_included",
        "raw_payload_values_included",
        "private_paths_included",
        "raw_hashes_included",
        "exact_offsets_included",
        "exact_file_sizes_included",
        "local_private_artifacts_included",
        "generated_artifacts_written",
        "generated_private_artifacts_included",
        "secrets_or_credentials_included",
    },
)
_FORBIDDEN_TEXT_RE = re.compile(
    r"(\[UnityCrossThreadLogger\]|\[Client GRE\]|DETAILED LOGS:|"
    r"https?://script\.google\.com|https?://hooks\.|"
    r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}|"
    r"\b(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{8,}|"
    r"(?:^|[^\w:/])(?:/(?:Applications|Users|Volumes|etc|home|opt|private|tmp|var)\b|\b[A-Za-z]:[\\/]|\\\\))",
    re.IGNORECASE,
)
_FORBIDDEN_LABELED_PATH_RE = re.compile(
    r"\b(?!(?:https?|git|ssh):)[A-Za-z_][A-Za-z0-9_-]{0,40}:"
    r"(?:/{1,3}(?:[A-Za-z]:[\\/])?(?:Applications|Users|Volumes|etc|home|opt|private|tmp|var)\b|"
    r"[A-Za-z]:[\\/]|\\\\)",
    re.IGNORECASE,
)
_FORBIDDEN_URI_LOCAL_PATH_RE = re.compile(
    r"\b(?!(?:https?|git|ssh):)[A-Za-z][A-Za-z0-9+.-]*:/{2,}"
    r"(?:(?:localhost|file|\.|127\.0\.0\.1)/)?"
    r"(?:[A-Za-z]:[\\/])?(?:Applications|Users|Volumes|etc|home|opt|private|tmp|var)\b",
    re.IGNORECASE,
)
_FORBIDDEN_PATH_EXTENSIONS = (".db", ".gz", ".log", ".sqlite", ".sqlite3", "." "xls", "." "xlsx")
_FORBIDDEN_PATH_SEGMENTS = frozenset(
    {
        "app-data",
        "failed_posts",
        "generated",
        "private",
        "runtime",
        "sqlite",
        "workbook" "_exports",
    },
)
_OVERCLAIM_TRUTH_RE = re.compile(
    r"(release readiness|production behavior|production readiness|analytics truth|ai truth|"
    r"coaching truth|private smoke success|full parser regression parity|tracker completion)",
    re.IGNORECASE,
)


def build_corpus_metadata_diff(
    *,
    promotion_proof: Mapping[str, Any],
    corpus_manifest: Mapping[str, Any],
    session_ledger: Mapping[str, Any],
    proposed_manifest_entry: Mapping[str, Any] | None = None,
    proposed_session_entry: Mapping[str, Any] | None = None,
    diff_context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic, review-only corpus metadata diff object."""

    source, proof_issue = _proof_source(promotion_proof)
    context_payload, context_findings = _diff_context(diff_context)
    diff_id = _diff_id(context_payload, source["proof_id"])
    created_at_utc = _public_safe_string_or_default(
        context_payload.get("created_at_utc") if isinstance(context_payload, Mapping) else None,
        DEFAULT_CREATED_AT_UTC,
    )

    manifest_schema_issue = _manifest_schema_issue(corpus_manifest)
    session_schema_issue = _session_schema_issue(session_ledger)
    taxonomy_families = _taxonomy_families(corpus_manifest)
    manifest_index = _manifest_entry_index(corpus_manifest)
    session_index = _session_entry_index(session_ledger)
    proof_families = _proof_families(promotion_proof)
    proof_before_status = _proof_before_status(promotion_proof)

    manifest_summaries, manifest_findings, manifest_issues = _manifest_entry_summaries(
        proposed_manifest_entry,
        current_entries=manifest_index,
        taxonomy_families=taxonomy_families,
        proof_before_status=proof_before_status,
    )
    session_summaries, session_findings, session_issues = _session_entry_summaries(
        proposed_session_entry,
        current_entries=session_index,
        taxonomy_families=taxonomy_families,
    )
    proposed_entries: list[Mapping[str, Any]] = []
    if proposed_manifest_entry is not None:
        proposed_entries.append(proposed_manifest_entry)
    if proposed_session_entry is not None:
        proposed_entries.append(proposed_session_entry)
    proposed_findings = [
        *_privacy_findings(proposed_manifest_entry, "proposed_manifest_entry"),
        *_privacy_findings(proposed_session_entry, "proposed_session_entry"),
        *_path_privacy_findings(proposed_manifest_entry, "proposed_manifest_entry"),
        *_path_privacy_findings(proposed_session_entry, "proposed_session_entry"),
    ]
    proof_findings = _privacy_findings(promotion_proof, "promotion_proof")
    upstream_findings = _upstream_privacy_findings(promotion_proof)
    privacy_findings = _dedupe(
        [
            *context_findings,
            *manifest_findings,
            *session_findings,
            *proposed_findings,
            *proof_findings,
            *upstream_findings,
        ],
    )
    change_types = _change_types(manifest_summaries, session_summaries)
    families = _transition_families(manifest_summaries, session_summaries)
    consistency_checks = _consistency_checks(
        manifest_schema_issue=manifest_schema_issue,
        session_schema_issue=session_schema_issue,
        proposed_entries=proposed_entries,
        proposed_families=families,
        proof_families=proof_families,
    )
    overclaim_reasons = _overclaim_reasons(
        promotion_proof=promotion_proof,
        proposed_entries=proposed_entries,
        proof_families=proof_families,
        proposed_families=families,
        manifest_summaries=manifest_summaries,
        session_summaries=session_summaries,
        current_manifest_entries=manifest_index,
    )
    authorization_reasons = _authorization_block_reasons(overclaim_reasons)
    status_reasons = _status_reasons(
        proof_issue=proof_issue,
        proof_status=source["proof_status"],
        manifest_schema_issue=manifest_schema_issue,
        session_schema_issue=session_schema_issue,
        manifest_issues=manifest_issues,
        session_issues=session_issues,
        privacy_findings=privacy_findings,
        overclaim_reasons=overclaim_reasons,
        authorization_reasons=authorization_reasons,
        has_proposed_changes=bool(change_types - {"no_change"}),
    )
    diff_status = _diff_status(
        proof_issue=proof_issue,
        proof_status=source["proof_status"],
        manifest_schema_issue=manifest_schema_issue,
        session_schema_issue=session_schema_issue,
        metadata_issues=[*manifest_issues, *session_issues],
        privacy_findings=privacy_findings,
        overclaim_reasons=overclaim_reasons,
        authorization_reasons=authorization_reasons,
        has_proposed_changes=bool(change_types - {"no_change"}),
    )
    blocked_for_privacy = diff_status == "blocked_privacy"

    return {
        "object": CORPUS_METADATA_DIFF_OBJECT,
        "schema_version": CORPUS_METADATA_DIFF_SCHEMA_VERSION,
        "diff_id": diff_id,
        "created_at_utc": created_at_utc,
        "source": source,
        "authorization": _authorization_flags(),
        "diff_status": diff_status,
        "metadata_targets": {
            "corpus_manifest": DEFAULT_CORPUS_MANIFEST_TARGET,
            "session_ledger": DEFAULT_SESSION_LEDGER_TARGET,
        },
        "proposed_changes": {
            "change_types": sorted(change_types),
            "manifest_entries": [] if blocked_for_privacy else manifest_summaries,
            "session_entries": [] if blocked_for_privacy else session_summaries,
        },
        "coverage_transition": {
            "families": [] if blocked_for_privacy else families,
            "transition_kind": _coverage_transition_kind(
                before_status=proof_before_status,
                manifest_summaries=manifest_summaries,
                session_summaries=session_summaries,
            ),
        },
        "consistency_checks": consistency_checks,
        "anti_overclaim": {
            "blocked": bool(overclaim_reasons),
            "reasons": [_safe_field_name(reason) for reason in overclaim_reasons],
        },
        "validation": {
            "proof_valid": proof_issue is None,
            "proof_issue": proof_issue,
            "manifest_schema_issue": manifest_schema_issue,
            "session_ledger_schema_issue": session_schema_issue,
            "metadata_entry_issues": _dedupe([*manifest_issues, *session_issues]),
            "status_reasons": status_reasons,
            "authorization_reasons": [_safe_field_name(reason) for reason in authorization_reasons],
            "privacy_finding_count": len(privacy_findings),
            "privacy_findings": _privacy_finding_records(privacy_findings),
        },
        "diff_context": context_payload,
        "non_claims": _non_claims(),
    }


def _proof_source(promotion_proof: Mapping[str, Any] | None) -> tuple[dict[str, Any], str | None]:
    if promotion_proof is None or not isinstance(promotion_proof, Mapping):
        return _unsupported_source("proof_missing"), "proof_missing"
    if promotion_proof.get("object") != FIXTURE_PROMOTION_PROOF_OBJECT:
        return _unsupported_source("unsupported_proof_object"), "unsupported_proof_object"
    if promotion_proof.get("schema_version") != FIXTURE_PROMOTION_PROOF_SCHEMA_VERSION:
        return _unsupported_source("unsupported_proof_schema"), "unsupported_proof_schema"
    source = promotion_proof.get("source")
    if not isinstance(source, Mapping):
        return _unsupported_source("proof_source_missing"), "proof_source_missing"
    return (
        {
            "promotion_proof_schema_version": FIXTURE_PROMOTION_PROOF_SCHEMA_VERSION,
            "proof_id": _symbolic_or_default(promotion_proof.get("proof_id"), "fixture-promotion-proof"),
            "proof_status": _safe_field_name(str(promotion_proof.get("proof_status", "unknown"))),
            "review_packet_id": _symbolic_or_default(source.get("review_packet_id"), "unavailable"),
            "candidate_report_id": _symbolic_or_default(source.get("candidate_report_id"), "unavailable"),
        },
        None,
    )


def _unsupported_source(reason: str) -> dict[str, Any]:
    return {
        "promotion_proof_schema_version": "unsupported",
        "proof_id": "unavailable",
        "proof_status": "unavailable",
        "review_packet_id": "unavailable",
        "candidate_report_id": "unavailable",
        "unavailable_reason": reason,
    }


def _diff_context(value: Mapping[str, Any] | None) -> tuple[dict[str, Any], list[str]]:
    if value is None:
        return {"created_at_utc": DEFAULT_CREATED_AT_UTC}, []
    if not isinstance(value, Mapping):
        return {"status": "blocked", "created_at_utc": DEFAULT_CREATED_AT_UTC}, ["diff_context:not_mapping"]
    findings = _privacy_findings(value, "diff_context")
    if findings:
        return {"status": "blocked", "created_at_utc": DEFAULT_CREATED_AT_UTC}, findings
    payload = _sanitize_mapping(value)
    payload.setdefault("created_at_utc", DEFAULT_CREATED_AT_UTC)
    return payload, []


def _diff_id(context_payload: Mapping[str, Any], proof_id: str) -> str:
    context_diff_id = context_payload.get("diff_id")
    if isinstance(context_diff_id, str):
        return _symbolic_or_default(context_diff_id, "corpus-metadata-diff")
    if proof_id != "unavailable":
        return _symbolic_or_default(f"{proof_id}:corpus-metadata-diff", "corpus-metadata-diff")
    return "corpus-metadata-diff"


def _authorization_flags() -> dict[str, bool]:
    return {
        "parser_behavior_ready": False,
        "pipeline_activation_ready_for_issue_388": False,
        "file_writing_authorized": False,
        "private_harvest_authorized": False,
        "fixture_promotion_authorized": False,
        "corpus_status_change_authorized": False,
    }


def _manifest_schema_issue(corpus_manifest: Mapping[str, Any]) -> str | None:
    if not isinstance(corpus_manifest, Mapping):
        return "manifest:not_mapping"
    if corpus_manifest.get("object") != CORPUS_MANIFEST_OBJECT:
        return "manifest:unsupported_object"
    if corpus_manifest.get("schema_version") != CORPUS_MANIFEST_SCHEMA_VERSION:
        return "manifest:unsupported_schema"
    if not isinstance(corpus_manifest.get("entries"), Sequence) or isinstance(corpus_manifest.get("entries"), str):
        return "manifest:entries_not_sequence"
    if not isinstance(corpus_manifest.get("taxonomy"), Mapping):
        return "manifest:taxonomy_missing"
    return None


def _session_schema_issue(session_ledger: Mapping[str, Any]) -> str | None:
    if not isinstance(session_ledger, Mapping):
        return "session_ledger:not_mapping"
    if session_ledger.get("object") != SESSION_LEDGER_OBJECT:
        return "session_ledger:unsupported_object"
    if session_ledger.get("schema_version") != SESSION_LEDGER_SCHEMA_VERSION:
        return "session_ledger:unsupported_schema"
    if not isinstance(session_ledger.get("sessions"), Sequence) or isinstance(session_ledger.get("sessions"), str):
        return "session_ledger:sessions_not_sequence"
    return None


def _taxonomy_families(corpus_manifest: Mapping[str, Any]) -> set[str]:
    taxonomy = corpus_manifest.get("taxonomy") if isinstance(corpus_manifest, Mapping) else None
    families = taxonomy.get("families") if isinstance(taxonomy, Mapping) else None
    if not isinstance(families, Sequence) or isinstance(families, str):
        return set()
    output = set()
    for family in families:
        if isinstance(family, Mapping):
            family_id = family.get("family_id")
            if isinstance(family_id, str):
                output.add(family_id)
    return output


def _manifest_entry_index(corpus_manifest: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    entries = corpus_manifest.get("entries") if isinstance(corpus_manifest, Mapping) else None
    output: dict[str, Mapping[str, Any]] = {}
    if not isinstance(entries, Sequence) or isinstance(entries, str):
        return output
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        entry_id = entry.get("entry_id")
        if isinstance(entry_id, str):
            output[entry_id] = entry
    return output


def _session_entry_index(session_ledger: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    sessions = session_ledger.get("sessions") if isinstance(session_ledger, Mapping) else None
    output: dict[str, Mapping[str, Any]] = {}
    if not isinstance(sessions, Sequence) or isinstance(sessions, str):
        return output
    for session in sessions:
        if not isinstance(session, Mapping):
            continue
        session_id = session.get("session_id")
        if isinstance(session_id, str):
            output[session_id] = session
    return output


def _manifest_entry_summaries(
    proposed_manifest_entry: Mapping[str, Any] | None,
    *,
    current_entries: Mapping[str, Mapping[str, Any]],
    taxonomy_families: set[str],
    proof_before_status: str,
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    if proposed_manifest_entry is None:
        return [], [], []
    if not isinstance(proposed_manifest_entry, Mapping):
        return [], ["proposed_manifest_entry:not_mapping"], ["proposed_manifest_entry:not_mapping"]

    findings = _privacy_findings(proposed_manifest_entry, "proposed_manifest_entry")
    issues = _manifest_entry_issues(proposed_manifest_entry, taxonomy_families=taxonomy_families)
    if findings:
        return [], findings, issues

    entry_id = _symbolic_or_default(proposed_manifest_entry.get("entry_id"), "unavailable")
    current_entry = current_entries.get(entry_id)
    current_status = (
        _safe_field_name(str(current_entry.get("coverage_status")))
        if isinstance(current_entry, Mapping)
        else proof_before_status
    )
    proposed_status = _safe_field_name(str(proposed_manifest_entry.get("coverage_status", "unknown")))
    change_type = "update_existing_manifest_entry" if entry_id in current_entries else "add_manifest_entry"
    summary = {
        "change_type": change_type,
        "entry_id": entry_id,
        "scenario_families": _scenario_families(proposed_manifest_entry),
        "before_status": current_status,
        "proposed_status": proposed_status,
        "coverage_basis": _string_list(proposed_manifest_entry.get("coverage_basis")),
        "known_gaps": _string_list(proposed_manifest_entry.get("known_gaps")),
        "review_notes": _string_list(proposed_manifest_entry.get("review_notes")),
    }
    return [summary], [], issues


def _session_entry_summaries(
    proposed_session_entry: Mapping[str, Any] | None,
    *,
    current_entries: Mapping[str, Mapping[str, Any]],
    taxonomy_families: set[str],
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    if proposed_session_entry is None:
        return [], [], []
    if not isinstance(proposed_session_entry, Mapping):
        return [], ["proposed_session_entry:not_mapping"], ["proposed_session_entry:not_mapping"]

    findings = _privacy_findings(proposed_session_entry, "proposed_session_entry")
    issues = _session_entry_issues(proposed_session_entry, taxonomy_families=taxonomy_families)
    if findings:
        return [], findings, issues

    session_id = _symbolic_or_default(proposed_session_entry.get("session_id"), "unavailable")
    change_type = "update_existing_session_entry" if session_id in current_entries else "add_session_entry"
    parser_coverage = proposed_session_entry.get("parser_coverage")
    coverage_status = "unknown"
    if isinstance(parser_coverage, Mapping):
        coverage_status = _safe_field_name(str(parser_coverage.get("coverage_status", "unknown")))
    summary = {
        "change_type": change_type,
        "session_id": session_id,
        "scenario_families": _scenario_families(proposed_session_entry),
        "proposed_status": coverage_status,
        "known_gaps": _string_list(proposed_session_entry.get("known_gaps")),
        "report_only_redactions": _redaction_flags(proposed_session_entry.get("report_only_redactions")),
    }
    return [summary], [], issues


def _manifest_entry_issues(entry: Mapping[str, Any], *, taxonomy_families: set[str]) -> list[str]:
    issues = []
    entry_id = _symbolic_or_default(entry.get("entry_id"), "unavailable")
    if entry_id == "unavailable":
        issues.append("manifest_entry:entry_id_missing")
    for key, accepted in (
        ("entry_type", MANIFEST_ENTRY_TYPES),
        ("source_kind", SOURCE_KINDS),
        ("commit_status", MANIFEST_COMMIT_STATUSES),
        ("privacy_class", PRIVACY_CLASSES),
        ("sanitization_status", SANITIZATION_STATUSES),
        ("coverage_status", COVERAGE_STATUSES),
    ):
        if entry.get(key) not in accepted:
            issues.append(f"manifest_entry:{key}_unsupported")
    if entry.get("privacy_class") in PRIVATE_PRIVACY_CLASSES:
        issues.append("manifest_entry:private_privacy_class")
    coverage_basis = _string_list(entry.get("coverage_basis"))
    if not coverage_basis:
        issues.append("manifest_entry:coverage_basis_missing")
    elif any(value not in COVERAGE_BASIS_VALUES for value in coverage_basis):
        issues.append("manifest_entry:coverage_basis_unsupported")
    families = _scenario_families(entry)
    if not families:
        issues.append("manifest_entry:scenario_families_missing")
    elif any(family not in taxonomy_families for family in families):
        issues.append("manifest_entry:scenario_family_not_in_taxonomy")
    if not _public_safe_string_or_default(entry.get("linked_issue"), ""):
        issues.append("manifest_entry:linked_issue_missing")
    if not _public_safe_string_or_default(entry.get("authorized_by_contract"), ""):
        issues.append("manifest_entry:authorized_by_contract_missing")
    if not _string_list(entry.get("known_gaps")):
        issues.append("manifest_entry:known_gaps_missing")
    if not _string_list(entry.get("review_notes")):
        issues.append("manifest_entry:review_notes_missing")
    return issues


def _session_entry_issues(entry: Mapping[str, Any], *, taxonomy_families: set[str]) -> list[str]:
    issues = []
    session_id = _symbolic_or_default(entry.get("session_id"), "unavailable")
    if session_id == "unavailable":
        issues.append("session_entry:session_id_missing")
    for key, accepted in (
        ("source_kind", SOURCE_KINDS),
        ("commit_status", SESSION_COMMIT_STATUSES),
        ("privacy_class", PRIVACY_CLASSES),
    ):
        if entry.get(key) not in accepted:
            issues.append(f"session_entry:{key}_unsupported")
    if entry.get("privacy_class") in PRIVATE_PRIVACY_CLASSES:
        issues.append("session_entry:private_privacy_class")
    families = _scenario_families(entry)
    if not families:
        issues.append("session_entry:scenario_families_missing")
    elif any(family not in taxonomy_families for family in families):
        issues.append("session_entry:scenario_family_not_in_taxonomy")
    if not isinstance(entry.get("parser_coverage"), Mapping):
        issues.append("session_entry:parser_coverage_missing")
    if not isinstance(entry.get("game_rows"), Mapping):
        issues.append("session_entry:game_rows_missing")
    if not _string_list(entry.get("known_gaps")):
        issues.append("session_entry:known_gaps_missing")
    redactions = entry.get("report_only_redactions")
    if not isinstance(redactions, Mapping):
        issues.append("session_entry:report_only_redactions_missing")
    elif any(redactions.get(key, False) is not False for key in SESSION_REDACTION_FLAGS):
        issues.append("session_entry:report_only_redactions_not_false")
    return issues


def _change_types(
    manifest_summaries: Sequence[Mapping[str, Any]],
    session_summaries: Sequence[Mapping[str, Any]],
) -> set[str]:
    change_types = {
        *(_safe_field_name(str(summary.get("change_type"))) for summary in manifest_summaries),
        *(_safe_field_name(str(summary.get("change_type"))) for summary in session_summaries),
    }
    for summary in manifest_summaries:
        before_status = summary.get("before_status")
        proposed_status = summary.get("proposed_status")
        if before_status != proposed_status:
            change_types.add(_status_change_type(str(before_status), str(proposed_status)))
    if not change_types:
        return {"no_change"}
    return {change_type for change_type in change_types if change_type in PROPOSED_CHANGE_TYPES} or {"unknown"}


def _status_change_type(before_status: str, proposed_status: str) -> str:
    if before_status == proposed_status:
        return "no_change"
    if before_status in {"blocked_private_evidence", "blocked_external_boundary"}:
        return before_status
    if proposed_status in {"blocked_private_evidence", "blocked_external_boundary"}:
        return proposed_status
    if proposed_status in {"covered_report_only", "covered_synthetic", "covered_committed"}:
        return "status_promotion_candidate"
    return "status_correction_candidate"


def _transition_families(
    manifest_summaries: Sequence[Mapping[str, Any]],
    session_summaries: Sequence[Mapping[str, Any]],
) -> list[str]:
    families: set[str] = set()
    for summary in (*manifest_summaries, *session_summaries):
        families.update(_string_list(summary.get("scenario_families")))
    return sorted(families)


def _coverage_transition_kind(
    *,
    before_status: str,
    manifest_summaries: Sequence[Mapping[str, Any]],
    session_summaries: Sequence[Mapping[str, Any]],
) -> str:
    statuses = [
        _safe_field_name(str(summary.get("proposed_status", "unknown")))
        for summary in (*manifest_summaries, *session_summaries)
    ]
    statuses = [status for status in statuses if status != "unknown"]
    if not statuses:
        return "no_change"
    proposed_status = _strongest_status(statuses)
    if before_status == "covered_report_only" and proposed_status == "covered_synthetic":
        return "report_only_to_synthetic_candidate"
    if before_status == "covered_report_only" and proposed_status == "covered_committed":
        return "report_only_to_committed_candidate"
    if before_status == "partial" and proposed_status == "covered_synthetic":
        return "partial_to_synthetic_candidate"
    if before_status == "partial" and proposed_status == "covered_committed":
        return "partial_to_committed_candidate"
    if before_status in {"missing", "unknown"} and proposed_status == "covered_report_only":
        return "missing_to_report_only_candidate"
    if before_status in {"missing", "unknown"} and proposed_status == "covered_synthetic":
        return "missing_to_synthetic_candidate"
    if before_status == "blocked_private_evidence":
        return "blocked_private_evidence_no_change"
    if before_status == "blocked_external_boundary":
        return "blocked_external_boundary_no_change"
    if before_status != proposed_status:
        return "status_correction_candidate"
    return "no_change"


def _strongest_status(statuses: Sequence[str]) -> str:
    rank = {
        "blocked_external_boundary": 0,
        "blocked_private_evidence": 0,
        "covered_report_only": 1,
        "partial": 2,
        "covered_synthetic": 3,
        "covered_committed": 4,
    }
    return max(statuses, key=lambda status: rank.get(status, -1), default="unknown")


def _consistency_checks(
    *,
    manifest_schema_issue: str | None,
    session_schema_issue: str | None,
    proposed_entries: Sequence[Mapping[str, Any]],
    proposed_families: Sequence[str],
    proof_families: Sequence[str],
) -> dict[str, bool]:
    family_scope_limited = set(proposed_families).issubset(set(proof_families)) if proposed_families else True
    return {
        "manifest_schema_valid": manifest_schema_issue is None,
        "session_ledger_schema_valid": session_schema_issue is None,
        "family_scope_limited": family_scope_limited,
        "known_gaps_preserved": all(_string_list(entry.get("known_gaps")) for entry in proposed_entries)
        if proposed_entries
        else True,
        "privacy_flags_preserved": all(_privacy_flags_preserved(entry) for entry in proposed_entries)
        if proposed_entries
        else True,
        "no_metadata_mutation_performed": True,
    }


def _overclaim_reasons(
    *,
    promotion_proof: Mapping[str, Any],
    proposed_entries: Sequence[Mapping[str, Any]],
    proof_families: Sequence[str],
    proposed_families: Sequence[str],
    manifest_summaries: Sequence[Mapping[str, Any]],
    session_summaries: Sequence[Mapping[str, Any]],
    current_manifest_entries: Mapping[str, Mapping[str, Any]],
) -> list[str]:
    reasons: list[str] = []
    authorization = promotion_proof.get("authorization") if isinstance(promotion_proof, Mapping) else None
    if isinstance(authorization, Mapping):
        for key in (
            "parser_behavior_ready",
            "pipeline_activation_ready_for_issue_388",
            "fixture_promotion_authorized",
            "corpus_status_change_authorized",
            "file_writing_authorized",
            "private_harvest_authorized",
        ):
            if authorization.get(key) is True:
                reasons.append(f"proof.authorization.{key}:forbidden_true")
    if proposed_families and not set(proposed_families).issubset(set(proof_families)):
        reasons.append("proposed_families:outside_proof_scope")
    for entry in proposed_entries:
        reasons.extend(_entry_overclaims(entry))
    for summary in (*manifest_summaries, *session_summaries):
        before_status = summary.get("before_status")
        proposed_status = summary.get("proposed_status")
        if before_status == "blocked_private_evidence" and proposed_status != "blocked_private_evidence":
            reasons.append("blocked_private_evidence:promotion_requires_separate_authority")
        if before_status == "blocked_external_boundary" and proposed_status != "blocked_external_boundary":
            reasons.append("blocked_external_boundary:promotion_requires_separate_authority")
    for summary in manifest_summaries:
        entry_id = summary.get("entry_id")
        current_entry = current_manifest_entries.get(str(entry_id))
        if isinstance(current_entry, Mapping) and _string_list(current_entry.get("known_gaps")):
            if not _string_list(summary.get("known_gaps")):
                reasons.append("known_gaps:removed_without_replacement")
    return _dedupe(reasons)


def _authorization_block_reasons(overclaim_reasons: Sequence[str]) -> list[str]:
    authorization_reasons = {
        "blocked_private_evidence:promotion_requires_separate_authority",
        "blocked_external_boundary:promotion_requires_separate_authority",
    }
    return [reason for reason in overclaim_reasons if reason in authorization_reasons]


def _entry_overclaims(entry: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    for key, value in _walk_mapping(entry):
        key_name = _safe_field_name(str(key))
        if key_name in {
            "parser_behavior_ready",
            "pipeline_activation_ready_for_issue_388",
            "fixture_promotion_authorized",
            "corpus_status_change_authorized",
            "file_writing_authorized",
            "private_harvest_authorized",
        } and value is True:
            reasons.append(f"{key_name}:forbidden_true")
        if key_name == "parser_behavior_verified":
            if value is True or value == "parser_behavior_verified":
                reasons.append("parser_behavior_verified:premature_claim")
        if isinstance(value, str):
            if value == "parser_behavior_verified":
                reasons.append("parser_behavior_verified:premature_claim")
            if _is_forbidden_truth_claim(value):
                reasons.append(f"{key_name}:forbidden_truth_claim")
    return reasons


def _is_forbidden_truth_claim(value: str) -> bool:
    if not _OVERCLAIM_TRUTH_RE.search(value):
        return False
    lower_value = value.lower()
    return not any(
        marker in lower_value
        for marker in (
            "does not",
            "do not",
            "not ",
            "not_",
            "non-claim",
            "nonclaim",
            "no ",
            "without ",
        )
    )


def _walk_mapping(value: Any) -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            items.append((str(key), item))
            items.extend(_walk_mapping(item))
    elif isinstance(value, Sequence) and not isinstance(value, str):
        for item in value:
            if isinstance(item, Mapping) or (isinstance(item, Sequence) and not isinstance(item, str)):
                items.extend(_walk_mapping(item))
            else:
                items.append(("", item))
    return items


def _status_reasons(
    *,
    proof_issue: str | None,
    proof_status: str,
    manifest_schema_issue: str | None,
    session_schema_issue: str | None,
    manifest_issues: Sequence[str],
    session_issues: Sequence[str],
    privacy_findings: Sequence[str],
    overclaim_reasons: Sequence[str],
    authorization_reasons: Sequence[str],
    has_proposed_changes: bool,
) -> list[str]:
    reasons = []
    if proof_issue:
        reasons.append(proof_issue)
    elif proof_status != "proof_ready_for_review":
        reasons.append(f"proof_status_{proof_status}")
    if manifest_schema_issue:
        reasons.append(manifest_schema_issue)
    if session_schema_issue:
        reasons.append(session_schema_issue)
    reasons.extend(manifest_issues)
    reasons.extend(session_issues)
    if privacy_findings:
        reasons.append("privacy_boundary_blocked")
    if authorization_reasons:
        reasons.append("authorization_boundary_blocked")
    reasons.extend(overclaim_reasons)
    if not has_proposed_changes:
        reasons.append("no_metadata_change")
    return [_safe_field_name(reason) for reason in _dedupe(reasons)]


def _diff_status(
    *,
    proof_issue: str | None,
    proof_status: str,
    manifest_schema_issue: str | None,
    session_schema_issue: str | None,
    metadata_issues: Sequence[str],
    privacy_findings: Sequence[str],
    overclaim_reasons: Sequence[str],
    authorization_reasons: Sequence[str],
    has_proposed_changes: bool,
) -> str:
    if privacy_findings:
        return "blocked_privacy"
    if proof_issue in {"proof_missing", "proof_source_missing"}:
        return "insufficient_proof"
    if proof_issue:
        return "needs_contract_update"
    if proof_status in {"blocked_privacy"}:
        return "blocked_privacy"
    if proof_status in {"blocked_authorization"}:
        return "blocked_authorization"
    if proof_status in {"proof_rejected"}:
        return "diff_rejected"
    if proof_status in {"needs_contract_update"}:
        return "needs_contract_update"
    if proof_status != "proof_ready_for_review":
        return "insufficient_proof"
    if authorization_reasons:
        return "blocked_authorization"
    if overclaim_reasons:
        return "blocked_overclaim"
    if manifest_schema_issue or session_schema_issue or metadata_issues:
        return "needs_contract_update"
    if not has_proposed_changes:
        return "no_metadata_change"
    return "diff_ready_for_review"


def _proof_families(promotion_proof: Mapping[str, Any]) -> list[str]:
    if not isinstance(promotion_proof, Mapping):
        return []
    comparison = promotion_proof.get("coverage_comparison")
    if not isinstance(comparison, Mapping):
        return []
    family = comparison.get("family")
    if isinstance(family, str) and _FIELD_NAME_RE.match(family):
        return [family]
    return []


def _proof_before_status(promotion_proof: Mapping[str, Any]) -> str:
    if not isinstance(promotion_proof, Mapping):
        return "unknown"
    comparison = promotion_proof.get("coverage_comparison")
    if not isinstance(comparison, Mapping):
        return "unknown"
    status = comparison.get("before_status")
    if isinstance(status, str):
        return _safe_field_name(status)
    return "unknown"


def _upstream_privacy_findings(promotion_proof: Mapping[str, Any]) -> list[str]:
    if not isinstance(promotion_proof, Mapping):
        return []
    validation = promotion_proof.get("validation")
    if isinstance(validation, Mapping) and validation.get("privacy_finding_count", 0):
        return ["promotion_proof.validation:upstream_privacy_finding"]
    return []


def _privacy_findings(value: Any, label: str) -> list[str]:
    findings: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_label = _safe_field_name(str(key))
            if isinstance(key, str) and key in _SAFE_FALSE_FLAG_KEYS:
                if item is not False:
                    findings.append(f"{label}.{key_label}:forbidden_true")
                continue
            if isinstance(key, str) and _SENSITIVE_KEY_RE.search(key):
                findings.append(f"{label}.{key_label}:forbidden_key")
                continue
            findings.extend(_privacy_findings(item, f"{label}.{key_label}"))
    elif isinstance(value, Sequence) and not isinstance(value, str):
        for index, item in enumerate(value):
            findings.extend(_privacy_findings(item, f"{label}.{index}"))
    elif isinstance(value, str) and _contains_forbidden_text(value):
        findings.append(f"{label}:forbidden_text")
    return _dedupe(findings)


def _path_privacy_findings(value: Any, label: str) -> list[str]:
    if not isinstance(value, Mapping):
        return []
    findings: list[str] = []
    paths = value.get("paths")
    if paths is not None:
        findings.extend(_paths_privacy_findings(paths, f"{label}.paths"))
    return _dedupe(findings)


def _paths_privacy_findings(value: Any, label: str) -> list[str]:
    findings: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            findings.extend(_paths_privacy_findings(item, f"{label}.{_safe_field_name(str(key))}"))
    elif isinstance(value, Sequence) and not isinstance(value, str):
        for index, item in enumerate(value):
            findings.extend(_paths_privacy_findings(item, f"{label}.{index}"))
    elif isinstance(value, str) and not _is_public_repo_relative_path(value):
        findings.append(f"{label}:forbidden_path")
    return _dedupe(findings)


def _is_public_repo_relative_path(value: str) -> bool:
    path = value.strip()
    if not path or _contains_forbidden_text(path):
        return False
    if path.startswith(("/", "\\", "~")) or "://" in path:
        return False
    path_parts = [part for part in path.replace("\\", "/").split("/") if part]
    if any(part == ".." for part in path_parts):
        return False
    lower_parts = {part.lower() for part in path_parts}
    if lower_parts & _FORBIDDEN_PATH_SEGMENTS:
        return False
    return not path.lower().endswith(_FORBIDDEN_PATH_EXTENSIONS)


def _privacy_flags_preserved(entry: Mapping[str, Any]) -> bool:
    for key, value in _walk_mapping(entry):
        if key in _SAFE_FALSE_FLAG_KEYS and value is not False:
            return False
    if entry.get("privacy_class") in PRIVATE_PRIVACY_CLASSES:
        return False
    redactions = entry.get("report_only_redactions")
    if isinstance(redactions, Mapping):
        for key in SESSION_REDACTION_FLAGS:
            if redactions.get(key, False) is not False:
                return False
    return True


def _redaction_flags(value: Any) -> dict[str, bool]:
    if not isinstance(value, Mapping):
        return {}
    flags = {}
    for key in sorted(SESSION_REDACTION_FLAGS):
        if key in value:
            flags[key] = value.get(key) is True
    return flags


def _scenario_families(entry: Mapping[str, Any]) -> list[str]:
    return _string_list(entry.get("scenario_families"))


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        return []
    output = []
    for item in value:
        if not isinstance(item, str):
            continue
        safe_item = _public_safe_string_or_default(item, "")
        if safe_item:
            output.append(safe_item)
    return _dedupe(output)


def _safe_field_name(value: Any) -> str:
    if not isinstance(value, str):
        return "unknown"
    value = value.strip()
    if not value or _contains_forbidden_text(value):
        return "unknown"
    normalized = re.sub(r"[^A-Za-z0-9._:-]+", "_", value).strip("_")
    if not normalized or not _FIELD_NAME_RE.match(normalized):
        return "unknown"
    return normalized


def _symbolic_or_default(value: Any, default: str) -> str:
    if isinstance(value, str) and _SYMBOLIC_TEXT_RE.match(value) and not _contains_forbidden_text(value):
        return value
    return default


def _public_safe_string_or_default(value: Any, default: str) -> str:
    if not isinstance(value, str) or _contains_forbidden_text(value):
        return default
    return value


def _sanitize_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, item in sorted(value.items(), key=lambda item: str(item[0])):
        output[_safe_field_name(str(key))] = _sanitize_value(item)
    return output


def _sanitize_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return _sanitize_mapping(value)
    if isinstance(value, Sequence) and not isinstance(value, str):
        return [_sanitize_value(item) for item in value]
    if isinstance(value, str):
        return _public_safe_string_or_default(value, "unavailable")
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int | float):
        return value
    return str(value)


def _privacy_finding_records(findings: Sequence[str]) -> list[dict[str, str]]:
    records = []
    for index, finding in enumerate(findings, start=1):
        field, _, reason = finding.partition(":")
        records.append(
            {
                "finding_id": f"corpus-metadata-diff-privacy-finding-{index}",
                "field": _safe_field_name(field),
                "reason": _safe_field_name(reason or "forbidden"),
            },
        )
    return records


def _contains_forbidden_text(value: str) -> bool:
    decoded = value
    for _ in range(2):
        decoded = unquote(decoded)
    return any(
        pattern.search(decoded)
        for pattern in (
            _FORBIDDEN_TEXT_RE,
            _FORBIDDEN_LABELED_PATH_RE,
            _FORBIDDEN_URI_LOCAL_PATH_RE,
        )
    )


def _dedupe(values: Sequence[str] | Any) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


def _non_claims() -> list[str]:
    return [
        "not_corpus_status_authority",
        "not_fixture_promotion_authority",
        "not_parser_truth",
        "not_readiness",
        "not_private_evidence_authorization",
        "not_parser_behavior_ready",
        "not_pipeline_activation_ready_for_issue_388",
        "not_file_writing_authority",
        "not_release_readiness",
        "not_production_readiness",
        "not_analytics_truth",
        "not_ai_truth",
        "not_coaching_truth",
        "not_full_parser_regression_parity",
    ]
