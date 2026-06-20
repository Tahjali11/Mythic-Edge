"""Synthetic-only fixture promotion proof builder."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any, Literal
from urllib.parse import unquote

from mythic_edge_parser.app.harvest_review_packets import (
    HARVEST_REVIEW_PACKET_OBJECT,
    HARVEST_REVIEW_PACKET_SCHEMA_VERSION,
    HARVEST_REVIEWER_DECISION_SCHEMA_VERSION,
)
from mythic_edge_parser.app.local_harvest_candidate_reports import DEFAULT_CREATED_AT_UTC

FIXTURE_PROMOTION_PROOF_OBJECT = "mythic_edge_fixture_promotion_proof"
FIXTURE_PROMOTION_PROOF_SCHEMA_VERSION = "parser_evidence_fixture_promotion_proof.v1"

ProofStatus = Literal[
    "draft",
    "blocked_privacy",
    "blocked_authorization",
    "insufficient_review",
    "proof_ready_for_review",
    "proof_rejected",
    "needs_contract_update",
]
CoverageStatusChangeKind = Literal[
    "no_change",
    "stronger_evidence_candidate",
    "status_promotion_candidate",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "needs_contract_update",
    "unknown",
]
EvidenceCheckStatus = Literal["not_run", "pass", "warn", "review", "diff", "fail", "blocked", "unavailable"]

PROOF_STATUSES = frozenset(ProofStatus.__args__)
COVERAGE_STATUS_CHANGE_KINDS = frozenset(CoverageStatusChangeKind.__args__)
EVIDENCE_CHECK_STATUSES = frozenset(EvidenceCheckStatus.__args__)
EVIDENCE_CHECK_NAMES = ("golden_replay", "corpus_parity", "feature_equity", "privacy", "protected_surface")

_SYMBOLIC_TEXT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_FIELD_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_RAW_OR_PRIVATE_KEY_RE = re.compile(
    r"(^|_)(raw|payload|payloads|content|text|line|lines|path|paths|hash|offset|offsets|bytes|byte_range|"
    r"file_size|timestamp_window)($|_)",
    re.IGNORECASE,
)
_SAFE_RAW_FLAG_KEYS = frozenset(
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


def build_fixture_promotion_proof(
    *,
    review_packet: Mapping[str, Any] | None,
    coverage_before: Mapping[str, Any],
    proposed_coverage_after: Mapping[str, Any] | None = None,
    check_refs: Mapping[str, Any] | None = None,
    proof_context: Mapping[str, Any] | None = None,
    created_at_utc: str = DEFAULT_CREATED_AT_UTC,
    proof_id: str | None = None,
) -> dict[str, Any]:
    """Build a deterministic review-only fixture promotion proof object."""

    source, schema_issue = _proof_source(review_packet)
    normalized_proof_id = _proof_id(proof_id, source["review_packet_id"])
    normalized_created_at = _public_safe_string_or_default(created_at_utc, DEFAULT_CREATED_AT_UTC)

    packet_privacy_findings = _dedupe(
        [
            *_privacy_findings(review_packet, "review_packet"),
            *_upstream_packet_privacy_findings(review_packet),
        ],
    )
    before_payload, before_findings = _coverage_input(coverage_before, "coverage_before")
    after_payload, after_findings = _coverage_input(proposed_coverage_after, "proposed_coverage_after")
    evidence_checks, check_findings = _evidence_checks(check_refs)
    context_payload, context_findings = _proof_context(proof_context)
    reviewer_decision = _reviewer_decision(review_packet, source)

    privacy_findings = _dedupe(
        [
            *packet_privacy_findings,
            *before_findings,
            *after_findings,
            *check_findings,
            *context_findings,
        ],
    )
    coverage_comparison = _coverage_comparison(
        before_payload=before_payload,
        after_payload=after_payload,
        review_packet=review_packet,
        packet_status=_packet_status(review_packet),
    )
    parser_fact_scope = _parser_fact_scope(review_packet, source)
    status_reasons = _status_reasons(
        schema_issue=schema_issue,
        privacy_findings=privacy_findings,
        packet_status=_packet_status(review_packet),
        reviewer_decision=reviewer_decision,
        coverage_comparison=coverage_comparison,
        evidence_checks=evidence_checks,
    )
    proof_status = _proof_status(
        schema_issue=schema_issue,
        privacy_findings=privacy_findings,
        packet_status=_packet_status(review_packet),
        reviewer_decision=reviewer_decision,
        coverage_comparison=coverage_comparison,
        evidence_checks=evidence_checks,
    )

    return {
        "object": FIXTURE_PROMOTION_PROOF_OBJECT,
        "schema_version": FIXTURE_PROMOTION_PROOF_SCHEMA_VERSION,
        "proof_id": normalized_proof_id,
        "created_at_utc": normalized_created_at,
        "source": source,
        "authorization": _authorization_flags(),
        "proof_status": proof_status,
        "coverage_comparison": coverage_comparison,
        "parser_fact_scope": parser_fact_scope,
        "evidence_checks": evidence_checks,
        "proof_context": context_payload,
        "validation": {
            "review_packet_valid": schema_issue is None,
            "schema_issue": schema_issue,
            "status_reasons": status_reasons,
            "privacy_finding_count": len(privacy_findings),
            "privacy_findings": _privacy_finding_records(privacy_findings),
        },
        "non_claims": _non_claims(),
    }


def _proof_source(review_packet: Mapping[str, Any] | None) -> tuple[dict[str, Any], str | None]:
    if review_packet is None or not isinstance(review_packet, Mapping):
        return _unsupported_source("review_packet_missing"), "review_packet_missing"
    if review_packet.get("object") != HARVEST_REVIEW_PACKET_OBJECT:
        return _unsupported_source("unsupported_review_packet_object"), "unsupported_review_packet_object"
    if review_packet.get("schema_version") != HARVEST_REVIEW_PACKET_SCHEMA_VERSION:
        return _unsupported_source("unsupported_review_packet_schema"), "unsupported_review_packet_schema"

    source = review_packet.get("source")
    if not isinstance(source, Mapping):
        return _unsupported_source("review_packet_source_missing"), "review_packet_source_missing"
    reviewer_decision = _reviewer_decision(review_packet, None)
    return (
        {
            "review_packet_schema_version": HARVEST_REVIEW_PACKET_SCHEMA_VERSION,
            "review_packet_id": _symbolic_or_default(review_packet.get("packet_id"), "harvest-review-packet"),
            "candidate_report_id": _symbolic_or_default(source.get("candidate_report_id"), "candidate-summary"),
            "reviewer_decision_id": (
                reviewer_decision["decision_id"] if reviewer_decision is not None else None
            ),
        },
        None,
    )


def _unsupported_source(reason: str) -> dict[str, Any]:
    return {
        "review_packet_schema_version": "unsupported",
        "review_packet_id": "unavailable",
        "candidate_report_id": "unavailable",
        "reviewer_decision_id": None,
        "unavailable_reason": reason,
    }


def _proof_id(proof_id: str | None, review_packet_id: str) -> str:
    if proof_id is not None:
        return _symbolic_or_default(proof_id, "fixture-promotion-proof")
    if review_packet_id == "unavailable":
        return "fixture-promotion-proof"
    return _symbolic_or_default(f"{review_packet_id}:fixture-promotion-proof", "fixture-promotion-proof")


def _authorization_flags() -> dict[str, bool]:
    return {
        "parser_behavior_ready": False,
        "pipeline_activation_ready_for_issue_388": False,
        "private_harvest_authorized": False,
        "fixture_promotion_authorized": False,
        "file_writing_authorized": False,
        "corpus_status_change_authorized": False,
    }


def _coverage_input(value: Mapping[str, Any] | None, label: str) -> tuple[dict[str, Any], list[str]]:
    if value is None:
        return {"family": "unknown", "status": None, "status_change_kind": "unknown"}, []
    if not isinstance(value, Mapping):
        return {"family": "unknown", "status": None, "status_change_kind": "unknown"}, [f"{label}:not_mapping"]
    findings = _privacy_findings(value, label)
    family = _safe_field_name(value.get("family", value.get("scenario_family", "unknown")))
    status = _safe_status(value.get("status", value.get("current_status", value.get("before_status"))))
    payload = {
        "family": family,
        "status": status,
        "requires_private_evidence": value.get("requires_private_evidence") is True,
        "external_boundary": value.get("external_boundary") is True,
        "needs_contract_update": value.get("needs_contract_update") is True,
        "evidence_strength": _safe_status(value.get("evidence_strength")),
    }
    return payload, findings


def _coverage_comparison(
    *,
    before_payload: Mapping[str, Any],
    after_payload: Mapping[str, Any],
    review_packet: Mapping[str, Any] | None,
    packet_status: str,
) -> dict[str, Any]:
    family = _coverage_family(before_payload, review_packet)
    before_status = before_payload.get("status") or "unknown"
    proposed_after_status = after_payload.get("status")
    if packet_status == "blocked_authorization" or before_payload.get("requires_private_evidence"):
        status_change_kind: CoverageStatusChangeKind = "blocked_private_evidence"
    elif before_payload.get("external_boundary") or after_payload.get("external_boundary"):
        status_change_kind = "blocked_external_boundary"
    elif before_payload.get("needs_contract_update") or after_payload.get("needs_contract_update"):
        status_change_kind = "needs_contract_update"
    elif proposed_after_status is None or proposed_after_status == before_status:
        status_change_kind = (
            "stronger_evidence_candidate"
            if after_payload.get("evidence_strength") not in {None, "", "unknown"}
            else "no_change"
        )
    elif proposed_after_status == "unknown" or before_status == "unknown":
        status_change_kind = "unknown"
    else:
        status_change_kind = "status_promotion_candidate"
    return {
        "family": family,
        "before_status": before_status,
        "proposed_after_status": proposed_after_status,
        "status_change_kind": status_change_kind,
        "metadata_mutation_authorized": False,
    }


def _coverage_family(before_payload: Mapping[str, Any], review_packet: Mapping[str, Any] | None) -> str:
    family = before_payload.get("family")
    if isinstance(family, str) and family != "unknown":
        return family
    if not isinstance(review_packet, Mapping):
        return "unknown"
    artifacts = review_packet.get("artifacts")
    if not isinstance(artifacts, Mapping):
        return "unknown"
    preview = artifacts.get("parser_fact_preview_json")
    if not isinstance(preview, Mapping):
        return "unknown"
    event_kinds = preview.get("event_kinds")
    if isinstance(event_kinds, Sequence) and not isinstance(event_kinds, str) and event_kinds:
        return _safe_field_name(str(event_kinds[0]))
    return "unknown"


def _evidence_checks(value: Mapping[str, Any] | None) -> tuple[dict[str, Any], list[str]]:
    findings = _privacy_findings(value, "check_refs") if isinstance(value, Mapping) else []
    checks: dict[str, Any] = {}
    for check_name in EVIDENCE_CHECK_NAMES:
        check_value = value.get(check_name) if isinstance(value, Mapping) else None
        if not isinstance(check_value, Mapping):
            checks[check_name] = {"status": "not_run", "refs": []}
            continue
        checks[check_name] = {
            "status": _member_or_default(check_value.get("status"), EVIDENCE_CHECK_STATUSES, "unavailable"),
            "refs": _safe_refs(check_value.get("refs")),
        }
    return checks, findings


def _reviewer_decision(
    review_packet: Mapping[str, Any] | None,
    source: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    if not isinstance(review_packet, Mapping):
        return None
    artifacts = review_packet.get("artifacts")
    if not isinstance(artifacts, Mapping):
        return None
    decision = artifacts.get("reviewer_decision_json")
    if decision is None:
        return None
    if not isinstance(decision, Mapping):
        return {
            "decision_status": "needs_contract_update",
            "decision_id": "reviewer-decision:needs-contract-update",
            "identity_matches": False,
            "decision_fresh": False,
        }
    decision_status = _safe_status(decision.get("decision_status")) or "needs_contract_update"
    decision_id = _symbolic_or_default(decision.get("decision_id"), "reviewer-decision")
    identity_matches = True
    if source is not None:
        identity_matches = (
            decision.get("candidate_report_id") == source.get("candidate_report_id")
            and decision.get("packet_id") == source.get("review_packet_id")
        )
    decision_fresh = decision.get("stale") is not True and decision.get("decision_fresh", True) is not False
    if (
        decision.get("schema_version", HARVEST_REVIEWER_DECISION_SCHEMA_VERSION)
        != HARVEST_REVIEWER_DECISION_SCHEMA_VERSION
    ):
        decision_status = "needs_contract_update"
    return {
        "decision_status": decision_status,
        "decision_id": decision_id,
        "identity_matches": identity_matches,
        "decision_fresh": decision_fresh,
    }


def _parser_fact_scope(review_packet: Mapping[str, Any] | None, source: Mapping[str, Any]) -> dict[str, Any]:
    preview_present = False
    if isinstance(review_packet, Mapping):
        artifacts = review_packet.get("artifacts")
        preview_present = isinstance(artifacts, Mapping) and isinstance(
            artifacts.get("parser_fact_preview_json"),
            Mapping,
        )
    fact_preview_ref = None
    if preview_present and source["review_packet_id"] != "unavailable":
        fact_preview_ref = f"{source['review_packet_id']}:parser_fact_preview"
    return {
        "parser_behavior_verified": False,
        "facts_proposed": [],
        "fact_preview_ref": fact_preview_ref,
    }


def _proof_context(value: Mapping[str, Any] | None) -> tuple[dict[str, Any] | None, list[str]]:
    if value is None:
        return None, []
    if not isinstance(value, Mapping):
        return {"status": "blocked"}, ["proof_context:not_mapping"]
    findings = _privacy_findings(value, "proof_context")
    if findings:
        return {"status": "blocked", "finding_count": len(findings)}, findings
    return _sanitize_mapping(value), []


def _proof_status(
    *,
    schema_issue: str | None,
    privacy_findings: Sequence[str],
    packet_status: str,
    reviewer_decision: Mapping[str, Any] | None,
    coverage_comparison: Mapping[str, Any],
    evidence_checks: Mapping[str, Any],
) -> str:
    if privacy_findings or packet_status == "blocked_privacy":
        return "blocked_privacy"
    if schema_issue == "review_packet_missing" or schema_issue == "review_packet_source_missing":
        return "insufficient_review"
    if schema_issue:
        return "needs_contract_update"
    if packet_status == "blocked_authorization":
        return "blocked_authorization"
    if coverage_comparison["status_change_kind"] == "blocked_private_evidence":
        return "blocked_authorization"
    if coverage_comparison["status_change_kind"] == "blocked_external_boundary":
        return "proof_rejected"
    if coverage_comparison["status_change_kind"] == "needs_contract_update":
        return "needs_contract_update"
    check_blocking_status = _blocking_check_status(evidence_checks)
    if check_blocking_status == "privacy":
        return "blocked_privacy"
    if check_blocking_status == "reject":
        return "proof_rejected"

    if reviewer_decision is None:
        return "draft"
    decision_status = reviewer_decision["decision_status"]
    if not reviewer_decision["identity_matches"] or not reviewer_decision["decision_fresh"]:
        return "insufficient_review"
    if decision_status == "approve_for_followup":
        return "proof_ready_for_review" if _all_checks_pass(evidence_checks) else "insufficient_review"
    if decision_status == "reject":
        return "proof_rejected"
    if decision_status == "needs_private_authorization":
        return "blocked_authorization"
    if decision_status == "blocked_privacy":
        return "blocked_privacy"
    if decision_status == "needs_contract_update":
        return "needs_contract_update"
    return "insufficient_review"


def _blocking_check_status(evidence_checks: Mapping[str, Any]) -> str | None:
    for check_name, check in evidence_checks.items():
        status = check.get("status")
        if check_name == "privacy" and status in {"fail", "blocked", "unavailable", "diff"}:
            return "privacy"
        if status in {"fail", "blocked", "unavailable", "diff"}:
            return "reject"
    return None


def _all_checks_pass(evidence_checks: Mapping[str, Any]) -> bool:
    return all(isinstance(check, Mapping) and check.get("status") == "pass" for check in evidence_checks.values())


def _status_reasons(
    *,
    schema_issue: str | None,
    privacy_findings: Sequence[str],
    packet_status: str,
    reviewer_decision: Mapping[str, Any] | None,
    coverage_comparison: Mapping[str, Any],
    evidence_checks: Mapping[str, Any],
) -> list[str]:
    reasons: list[str] = []
    if schema_issue:
        reasons.append(schema_issue)
    if privacy_findings:
        reasons.append("privacy_boundary_blocked")
    if packet_status != "reviewed_followup_candidate":
        reasons.append(f"review_packet_status_{packet_status}")
    if reviewer_decision is None:
        reasons.append("reviewer_decision_not_supplied")
    else:
        reasons.append(f"reviewer_decision_{reviewer_decision['decision_status']}")
        if not reviewer_decision["identity_matches"]:
            reasons.append("reviewer_decision_identity_mismatch")
        if not reviewer_decision["decision_fresh"]:
            reasons.append("reviewer_decision_stale")
    status_change_kind = coverage_comparison["status_change_kind"]
    if status_change_kind != "no_change":
        reasons.append(f"coverage_{status_change_kind}")
    non_pass_checks = [
        f"{name}_{check['status']}"
        for name, check in sorted(evidence_checks.items())
        if isinstance(check, Mapping) and check.get("status") != "pass"
    ]
    reasons.extend(non_pass_checks)
    return _dedupe(reasons)


def _packet_status(review_packet: Mapping[str, Any] | None) -> str:
    if not isinstance(review_packet, Mapping):
        return "missing"
    status = review_packet.get("packet_status")
    return _safe_status(status) or "unknown"


def _privacy_finding_records(findings: Sequence[str]) -> list[dict[str, str]]:
    records = []
    for index, finding in enumerate(findings, start=1):
        field, _, reason = finding.partition(":")
        records.append(
            {
                "finding_id": f"fixture-proof-privacy-finding-{index}",
                "field": _safe_field_name(field),
                "reason": _safe_field_name(reason or "forbidden"),
            },
        )
    return records


def _upstream_packet_privacy_findings(review_packet: Mapping[str, Any] | None) -> list[str]:
    if not isinstance(review_packet, Mapping):
        return []
    artifacts = review_packet.get("artifacts")
    if not isinstance(artifacts, Mapping):
        return []
    privacy_report = artifacts.get("privacy_report_json")
    if not isinstance(privacy_report, Mapping):
        return []
    findings = []
    report_findings = privacy_report.get("findings")
    report_reasons = []
    if isinstance(report_findings, Sequence) and not isinstance(report_findings, str):
        for index, finding in enumerate(report_findings):
            if isinstance(finding, Mapping):
                reason = _safe_field_name(finding.get("reason", "upstream_privacy_finding"))
                report_reasons.append(reason)
                if reason == "private_harvest_authorization_missing":
                    continue
                findings.append(f"review_packet.privacy_report_json.findings.{index}:{reason}")
    if privacy_report.get("status") == "block" and not findings and not report_reasons:
        findings.append("review_packet.privacy_report_json:upstream_privacy_block")
    return _dedupe(findings)


def _non_claims() -> list[str]:
    return [
        "not_fixture_promotion_authority",
        "not_parser_truth",
        "not_private_evidence_authorization",
        "not_readiness",
        "not_parser_behavior_ready",
        "not_pipeline_activation_ready_for_issue_388",
        "not_corpus_status_change_authority",
        "not_file_writing_authority",
        "not_release_readiness",
        "not_production_readiness",
        "not_analytics_truth",
        "not_ai_truth",
        "not_coaching_truth",
        "not_full_parser_regression_parity",
    ]


def _privacy_findings(value: Any, label: str) -> list[str]:
    findings: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_label = _safe_field_name(str(key))
            if isinstance(key, str) and _RAW_OR_PRIVATE_KEY_RE.search(key) and key not in _SAFE_RAW_FLAG_KEYS:
                findings.append(f"{label}.{key_label}:forbidden_key")
                continue
            findings.extend(_privacy_findings(item, f"{label}.{key_label}"))
    elif isinstance(value, Sequence) and not isinstance(value, str):
        for index, item in enumerate(value):
            findings.extend(_privacy_findings(item, f"{label}.{index}"))
    elif isinstance(value, str) and _contains_forbidden_text(value):
        findings.append(f"{label}:forbidden_text")
    return _dedupe(findings)


def _sanitize_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, item in sorted(value.items(), key=lambda item: str(item[0])):
        safe_key = _safe_field_name(str(key))
        output[safe_key] = _sanitize_value(item)
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


def _safe_refs(value: Any) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        return []
    refs = []
    for ref in value:
        if not isinstance(ref, str):
            continue
        safe_ref = _public_safe_string_or_default(ref, "unavailable")
        if safe_ref != "unavailable":
            refs.append(safe_ref)
    return _dedupe(sorted(refs))


def _safe_status(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip()
    if not value or _contains_forbidden_text(value):
        return None
    return _safe_field_name(value)


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


def _member_or_default(value: Any, accepted: frozenset[str], default: str) -> str:
    if isinstance(value, str) and value in accepted:
        return value
    return default


def _public_safe_string_or_default(value: Any, default: str) -> str:
    if not isinstance(value, str) or _contains_forbidden_text(value):
        return default
    return value


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
