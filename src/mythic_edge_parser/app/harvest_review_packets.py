"""Synthetic-only harvest review packet builder."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any, Literal
from urllib.parse import unquote

from mythic_edge_parser.app.local_harvest_candidate_reports import (
    DEFAULT_CREATED_AT_UTC,
    HARVEST_CANDIDATE_SUMMARY_OBJECT,
    HARVEST_CANDIDATE_SUMMARY_SCHEMA_VERSION,
    PARSER_FACT_PREVIEW_OBJECT,
    PARSER_FACT_PREVIEW_SCHEMA_VERSION,
)

HARVEST_REVIEW_PACKET_OBJECT = "mythic_edge_harvest_review_packet"
HARVEST_REVIEW_PACKET_SCHEMA_VERSION = "parser_evidence_harvest_review_packet.v1"
HARVEST_REVIEW_PRIVACY_REPORT_OBJECT = "mythic_edge_harvest_review_privacy_report"
HARVEST_REVIEW_PRIVACY_REPORT_SCHEMA_VERSION = "parser_evidence_harvest_review_privacy_report.v1"
HARVEST_REVIEWER_DECISION_OBJECT = "mythic_edge_harvest_reviewer_decision"
HARVEST_REVIEWER_DECISION_SCHEMA_VERSION = "parser_evidence_harvest_reviewer_decision.v1"

PacketStatus = Literal[
    "draft",
    "review_required",
    "blocked_privacy",
    "blocked_authorization",
    "reviewed_followup_candidate",
    "reviewed_rejected",
    "reviewed_deferred",
]
PrivacyStatus = Literal["pass", "warn", "block", "unavailable"]
DecisionStatus = Literal[
    "approve_for_followup",
    "reject",
    "defer",
    "needs_private_authorization",
    "needs_contract_update",
    "blocked_privacy",
]
ReviewerRole = Literal["human", "codex_e", "codex_a", "codex_b"]
AllowedNextRoute = Literal["codex_a_problem_representation", "codex_b_contract", "codex_e_review", "none"]

PACKET_STATUSES = frozenset(PacketStatus.__args__)
PRIVACY_STATUSES = frozenset(PrivacyStatus.__args__)
DECISION_STATUSES = frozenset(DecisionStatus.__args__)
REVIEWER_ROLES = frozenset(ReviewerRole.__args__)
ALLOWED_NEXT_ROUTES = frozenset(AllowedNextRoute.__args__)

PRIVACY_CLASSES = frozenset({"public_fixture", "synthetic", "private_local", "local_only_redacted"})
PRIVATE_PRIVACY_CLASSES = frozenset({"private_local", "local_only_redacted"})
SOURCE_KINDS_REQUIRING_PRIVATE_AUTHORIZATION = frozenset(
    {
        "user_selected_player_log",
        "user_selected_normalized_utc_log",
    },
)
DEFAULT_BLOCKED_ROUTES = (
    "fixture_promotion",
    "private_harvest_execution",
    "corpus_status_change",
)

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


class HarvestReviewPacketError(ValueError):
    """Raised when review packet inputs are outside the in-memory safety boundary."""


def build_harvest_review_packet(
    *,
    candidate_summary: Mapping[str, Any],
    reviewer_context: Mapping[str, Any] | None = None,
    reviewer_decision: Mapping[str, Any] | None = None,
    created_at_utc: str = DEFAULT_CREATED_AT_UTC,
    packet_id: str | None = None,
) -> dict[str, Any]:
    """Build a deterministic advisory review packet from a supplied #382 summary."""

    if not isinstance(candidate_summary, Mapping):
        raise HarvestReviewPacketError("candidate_summary must be a mapping")

    schema_issue = _candidate_schema_issue(candidate_summary)
    source = _packet_source(candidate_summary, schema_issue=schema_issue)
    normalized_packet_id = _packet_id(packet_id, source["candidate_report_id"])
    normalized_created_at = _public_safe_string(created_at_utc, "created_at_utc")

    candidate_privacy_findings = _candidate_summary_privacy_findings(candidate_summary)
    context_payload, context_findings = _sanitize_optional_public_mapping(
        reviewer_context,
        label="reviewer_context",
    )
    decision_payload, decision_findings = _reviewer_decision_payload(
        reviewer_decision,
        candidate_report_id=source["candidate_report_id"],
        packet_id=normalized_packet_id,
    )
    privacy_findings = _dedupe([*candidate_privacy_findings, *context_findings, *decision_findings])
    authorization_blocked = _private_authorization_missing(candidate_summary, source)
    privacy_report = _privacy_report(
        privacy_findings=privacy_findings,
        authorization_blocked=authorization_blocked,
        candidate_summary_valid=schema_issue is None,
    )
    parser_fact_preview = _parser_fact_preview(candidate_summary, blocked=bool(privacy_findings))
    packet_status = _packet_status(
        schema_issue=schema_issue,
        privacy_findings=privacy_findings,
        authorization_blocked=authorization_blocked,
        reviewer_decision=decision_payload,
    )

    authorization = {
        "private_harvest_authorized": False,
        "file_writing_authorized": False,
        "fixture_promotion_authorized": False,
        "corpus_status_change_authorized": False,
    }
    non_claims = _non_claims()
    packet = {
        "object": HARVEST_REVIEW_PACKET_OBJECT,
        "schema_version": HARVEST_REVIEW_PACKET_SCHEMA_VERSION,
        "packet_id": normalized_packet_id,
        "created_at_utc": normalized_created_at,
        "source": source,
        "authorization": authorization,
        "packet_status": packet_status,
        "reviewer_context": context_payload,
        "artifacts": {
            "candidate_summary_markdown": _candidate_summary_markdown(candidate_summary, source),
            "redacted_context_markdown": _redacted_context_markdown(
                candidate_summary,
                source=source,
                authorization_blocked=authorization_blocked,
            ),
            "parser_fact_preview_json": parser_fact_preview,
            "privacy_report_json": privacy_report,
            "reviewer_decision_json": decision_payload,
        },
        "validation": {
            "candidate_summary_valid": schema_issue is None,
            "schema_issue": schema_issue,
            "status_reasons": _status_reasons(
                schema_issue=schema_issue,
                privacy_findings=privacy_findings,
                authorization_blocked=authorization_blocked,
                reviewer_decision=decision_payload,
            ),
        },
        "non_claims": non_claims,
    }
    return packet


def _candidate_schema_issue(candidate_summary: Mapping[str, Any]) -> str | None:
    if candidate_summary.get("object") != HARVEST_CANDIDATE_SUMMARY_OBJECT:
        return "unsupported_candidate_summary_object"
    if candidate_summary.get("schema_version") != HARVEST_CANDIDATE_SUMMARY_SCHEMA_VERSION:
        return "unsupported_candidate_summary_schema"
    return None


def _packet_source(candidate_summary: Mapping[str, Any], *, schema_issue: str | None) -> dict[str, Any]:
    if schema_issue:
        return {
            "candidate_report_object": "unsupported",
            "candidate_report_schema_version": "unsupported",
            "candidate_report_id": "unavailable",
            "source_label": "unavailable",
            "privacy_class": "local_only_redacted",
            "raw_source_committed": False,
            "raw_path_included": False,
            "raw_hash_included": False,
            "raw_content_included": False,
        }

    source = candidate_summary.get("source")
    if not isinstance(source, Mapping):
        source = {}
    return {
        "candidate_report_object": HARVEST_CANDIDATE_SUMMARY_OBJECT,
        "candidate_report_schema_version": HARVEST_CANDIDATE_SUMMARY_SCHEMA_VERSION,
        "candidate_report_id": _symbolic_or_default(candidate_summary.get("report_id"), "candidate-summary"),
        "source_label": _symbolic_or_default(source.get("source_label"), "unavailable"),
        "privacy_class": _privacy_class(source.get("privacy_class")),
        "raw_source_committed": False,
        "raw_path_included": False,
        "raw_hash_included": False,
        "raw_content_included": False,
    }


def _packet_id(packet_id: str | None, candidate_report_id: str) -> str:
    if packet_id is not None:
        return _symbolic_text(packet_id, "packet_id")
    if candidate_report_id == "unavailable":
        return "harvest-review-packet"
    return _symbolic_text(f"{candidate_report_id}:review-packet", "packet_id")


def _candidate_summary_privacy_findings(candidate_summary: Mapping[str, Any]) -> list[str]:
    findings = _privacy_findings(candidate_summary, "candidate_summary")
    source = candidate_summary.get("source")
    if isinstance(source, Mapping):
        for key in ("raw_source_committed", "raw_path_included", "raw_hash_included", "raw_content_included"):
            if source.get(key) is not False:
                findings.append(f"candidate_summary.source.{key}:forbidden_true")
    privacy = candidate_summary.get("privacy")
    if isinstance(privacy, Mapping):
        for key in (
            "raw_private_logs_included",
            "raw_payload_values_included",
            "private_paths_included",
            "raw_hashes_included",
            "exact_offsets_included",
            "generated_artifacts_written",
        ):
            if privacy.get(key) is not False:
                findings.append(f"candidate_summary.privacy.{key}:forbidden_true")
        if privacy.get("privacy_findings"):
            findings.append("candidate_summary.privacy.privacy_findings:upstream_privacy_finding")
    return _dedupe(findings)


def _sanitize_optional_public_mapping(
    value: Mapping[str, Any] | None,
    *,
    label: str,
) -> tuple[dict[str, Any] | None, list[str]]:
    if value is None:
        return None, []
    if not isinstance(value, Mapping):
        return {"status": "blocked"}, [f"{label}:not_mapping"]
    findings = _privacy_findings(value, label)
    if findings:
        return {"status": "blocked", "finding_count": len(findings)}, findings
    return _sanitize_mapping(value), []


def _reviewer_decision_payload(
    value: Mapping[str, Any] | None,
    *,
    candidate_report_id: str,
    packet_id: str,
) -> tuple[dict[str, Any] | None, list[str]]:
    if value is None:
        return None, []
    if not isinstance(value, Mapping):
        return _needs_contract_update_decision(candidate_report_id, packet_id), []
    findings = _privacy_findings(value, "reviewer_decision")
    if findings:
        decision = _base_reviewer_decision(
            candidate_report_id=candidate_report_id,
            packet_id=packet_id,
            decision_id=f"{packet_id}:blocked-privacy",
            reviewer_role="codex_e",
            decision_status="blocked_privacy",
            rationale=["reviewer_decision_failed_privacy_check"],
            allowed_next_route="none",
        )
        return decision, findings

    if value.get("object", HARVEST_REVIEWER_DECISION_OBJECT) != HARVEST_REVIEWER_DECISION_OBJECT:
        return _needs_contract_update_decision(candidate_report_id, packet_id), []
    if (
        value.get("schema_version", HARVEST_REVIEWER_DECISION_SCHEMA_VERSION)
        != HARVEST_REVIEWER_DECISION_SCHEMA_VERSION
    ):
        return _needs_contract_update_decision(candidate_report_id, packet_id), []

    decision_status = value.get("decision_status", "defer")
    reviewer_role = value.get("reviewer_role", "codex_e")
    allowed_next_route = value.get("allowed_next_route", _route_for_decision_status(str(decision_status)))
    rationale = _safe_public_reason_list(value.get("rationale", ["reviewer_decision_supplied"]))
    decision = _base_reviewer_decision(
        candidate_report_id=candidate_report_id,
        packet_id=packet_id,
        decision_id=_symbolic_or_default(value.get("decision_id"), f"{packet_id}:reviewer-decision"),
        reviewer_role=_member_or_default(reviewer_role, REVIEWER_ROLES, "codex_e"),
        decision_status=_member_or_default(decision_status, DECISION_STATUSES, "needs_contract_update"),
        rationale=rationale,
        allowed_next_route=_member_or_default(allowed_next_route, ALLOWED_NEXT_ROUTES, "none"),
    )
    return decision, []


def _needs_contract_update_decision(candidate_report_id: str, packet_id: str) -> dict[str, Any]:
    return _base_reviewer_decision(
        candidate_report_id=candidate_report_id,
        packet_id=packet_id,
        decision_id=f"{packet_id}:needs-contract-update",
        reviewer_role="codex_e",
        decision_status="needs_contract_update",
        rationale=["reviewer_decision_or_candidate_summary_needs_contract_update"],
        allowed_next_route="codex_b_contract",
    )


def _base_reviewer_decision(
    *,
    candidate_report_id: str,
    packet_id: str,
    decision_id: str,
    reviewer_role: str,
    decision_status: str,
    rationale: Sequence[str],
    allowed_next_route: str,
) -> dict[str, Any]:
    return {
        "object": HARVEST_REVIEWER_DECISION_OBJECT,
        "schema_version": HARVEST_REVIEWER_DECISION_SCHEMA_VERSION,
        "decision_id": _symbolic_text(decision_id, "decision_id"),
        "reviewer_role": reviewer_role,
        "decision_status": decision_status,
        "candidate_report_id": candidate_report_id,
        "packet_id": packet_id,
        "rationale": list(rationale),
        "allowed_next_route": allowed_next_route,
        "blocked_routes": list(DEFAULT_BLOCKED_ROUTES),
        "non_claims": {
            "parser_truth_decided": False,
            "fixture_promotion_authorized": False,
            "private_harvest_authorized": False,
            "corpus_status_change_authorized": False,
            "parser_behavior_verified": False,
            "pipeline_activation_ready_for_issue_388": False,
        },
    }


def _route_for_decision_status(status: str) -> str:
    if status == "approve_for_followup":
        return "codex_a_problem_representation"
    if status == "needs_contract_update":
        return "codex_b_contract"
    if status in {"reject", "blocked_privacy"}:
        return "none"
    return "codex_e_review"


def _privacy_report(
    *,
    privacy_findings: Sequence[str],
    authorization_blocked: bool,
    candidate_summary_valid: bool,
) -> dict[str, Any]:
    findings = [
        {
            "finding_id": f"privacy-finding-{index}",
            "severity": "block",
            "field": _safe_field_name(finding.split(":", 1)[0]),
            "reason": _safe_field_name(finding.split(":", 1)[-1]),
        }
        for index, finding in enumerate(privacy_findings, start=1)
    ]
    if authorization_blocked:
        findings.append(
            {
                "finding_id": "authorization-missing",
                "severity": "block",
                "field": "source",
                "reason": "private_harvest_authorization_missing",
            },
        )
    if privacy_findings or authorization_blocked:
        status: PrivacyStatus = "block"
    elif not candidate_summary_valid:
        status = "warn"
    else:
        status = "pass"
    return {
        "object": HARVEST_REVIEW_PRIVACY_REPORT_OBJECT,
        "schema_version": HARVEST_REVIEW_PRIVACY_REPORT_SCHEMA_VERSION,
        "status": status,
        "checks": {
            "raw_log_lines_included": False,
            "raw_payloads_included": False,
            "private_paths_included": False,
            "raw_hashes_included": False,
            "exact_offsets_included": False,
            "exact_file_sizes_included": False,
            "generated_private_artifacts_included": False,
            "secrets_or_credentials_included": False,
        },
        "findings": findings,
        "non_claims": {
            "privacy_assurance": False,
            "private_harvest_authorized": False,
        },
    }


def _parser_fact_preview(candidate_summary: Mapping[str, Any], *, blocked: bool) -> dict[str, Any] | None:
    value = candidate_summary.get("parser_fact_preview")
    if not isinstance(value, Mapping):
        return None
    if blocked:
        return {
            "object": PARSER_FACT_PREVIEW_OBJECT,
            "schema_version": PARSER_FACT_PREVIEW_SCHEMA_VERSION,
            "preview_status": "blocked",
            "raw_log_lines_included": False,
            "raw_payloads_included": False,
            "private_paths_included": False,
            "event_counts": {},
            "event_kinds": [],
            "diagnostics_summary": {"status": "unknown"},
            "drift_summary": {"status": "unknown"},
        }
    return {
        "object": PARSER_FACT_PREVIEW_OBJECT,
        "schema_version": PARSER_FACT_PREVIEW_SCHEMA_VERSION,
        "preview_status": _safe_status(value.get("preview_status", "unavailable")),
        "raw_log_lines_included": False,
        "raw_payloads_included": False,
        "private_paths_included": False,
        "event_counts": _safe_event_counts(value.get("event_counts")),
        "event_kinds": _safe_symbolic_list(value.get("event_kinds")),
        "diagnostics_summary": {"status": _nested_status(value, "diagnostics_summary")},
        "drift_summary": {"status": _nested_status(value, "drift_summary")},
    }


def _candidate_summary_markdown(candidate_summary: Mapping[str, Any], source: Mapping[str, Any]) -> str:
    rows = _candidate_rows(candidate_summary)
    lines = [
        "# Harvest Review Packet Candidate Summary",
        "",
        f"- Candidate report id: `{source['candidate_report_id']}`",
        f"- Source label: `{source['source_label']}`",
        f"- Privacy class: `{source['privacy_class']}`",
        "- Parser behavior verified: `false`",
        "- Fixture promotion authorized: `false`",
        "- Private harvest authorized: `false`",
        "",
        "| Family | Candidate status | Coverage | Confidence | Evidence | Privacy risk |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    if not rows:
        lines.append("| unavailable | unavailable | none | unknown | unknown | unknown |")
    else:
        for row in rows:
            lines.append(
                "| "
                + " | ".join(
                    [
                        row["family_id"],
                        row["candidate_status"],
                        row["coverage_value"],
                        row["confidence"],
                        row["evidence_status"],
                        row["privacy_risk"],
                    ],
                )
                + " |",
            )
    lines.extend(
        [
            "",
            "This packet is a routing/review artifact only. It does not decide parser truth, fixture promotion, "
            "private harvest authorization, corpus status changes, or pipeline activation.",
        ],
    )
    return "\n".join(lines)


def _redacted_context_markdown(
    candidate_summary: Mapping[str, Any],
    *,
    source: Mapping[str, Any],
    authorization_blocked: bool,
) -> str:
    if authorization_blocked or source["privacy_class"] in PRIVATE_PRIVACY_CLASSES:
        return (
            "Redacted context unavailable: private source review requires a separate "
            "approval under issue #434."
        )
    preview = _parser_fact_preview(candidate_summary, blocked=False) or {}
    event_counts = preview.get("event_counts", {})
    event_kinds = preview.get("event_kinds", [])
    lines = [
        "# Redacted Context",
        "",
        f"- Source label: `{source['source_label']}`",
        f"- Event counts: `{_compact_public_mapping(event_counts)}`",
        f"- Event kinds: `{', '.join(event_kinds) if event_kinds else 'none'}`",
        "- Raw logs included: `false`",
        "- Raw payloads included: `false`",
        "- Private paths included: `false`",
    ]
    return "\n".join(lines)


def _packet_status(
    *,
    schema_issue: str | None,
    privacy_findings: Sequence[str],
    authorization_blocked: bool,
    reviewer_decision: Mapping[str, Any] | None,
) -> str:
    if privacy_findings:
        return "blocked_privacy"
    if schema_issue:
        return "reviewed_deferred"
    if authorization_blocked:
        return "blocked_authorization"
    if reviewer_decision is None:
        return "review_required"
    status = reviewer_decision.get("decision_status")
    if status == "approve_for_followup":
        return "reviewed_followup_candidate"
    if status == "reject":
        return "reviewed_rejected"
    if status == "needs_private_authorization":
        return "blocked_authorization"
    if status == "blocked_privacy":
        return "blocked_privacy"
    return "reviewed_deferred"


def _status_reasons(
    *,
    schema_issue: str | None,
    privacy_findings: Sequence[str],
    authorization_blocked: bool,
    reviewer_decision: Mapping[str, Any] | None,
) -> list[str]:
    reasons: list[str] = []
    if schema_issue:
        reasons.append(schema_issue)
    if privacy_findings:
        reasons.append("privacy_boundary_blocked")
    if authorization_blocked:
        reasons.append("private_harvest_authorization_missing")
    if reviewer_decision is None:
        reasons.append("reviewer_decision_not_supplied")
    else:
        reasons.append(f"reviewer_decision_{reviewer_decision['decision_status']}")
    return _dedupe(reasons)


def _private_authorization_missing(candidate_summary: Mapping[str, Any], source: Mapping[str, Any]) -> bool:
    if source["candidate_report_object"] == "unsupported":
        return False
    if source["privacy_class"] in PRIVATE_PRIVACY_CLASSES:
        return True
    candidate_source = candidate_summary.get("source")
    if (
        isinstance(candidate_source, Mapping)
        and candidate_source.get("source_kind") in SOURCE_KINDS_REQUIRING_PRIVATE_AUTHORIZATION
    ):
        return True
    authorization = candidate_summary.get("authorization")
    if isinstance(authorization, Mapping) and authorization.get("authorization_status") == "missing_required":
        return True
    return False


def _candidate_rows(candidate_summary: Mapping[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    candidate_windows = candidate_summary.get("candidate_windows")
    if not isinstance(candidate_windows, Sequence) or isinstance(candidate_windows, str):
        return rows
    for window in candidate_windows:
        if not isinstance(window, Mapping):
            continue
        candidates = window.get("scenario_family_candidates")
        if not isinstance(candidates, Sequence) or isinstance(candidates, str):
            continue
        for candidate in candidates:
            if not isinstance(candidate, Mapping):
                continue
            rows.append(
                {
                    "family_id": _safe_field_name(candidate.get("family_id", "unknown")),
                    "candidate_status": _safe_field_name(candidate.get("candidate_status", "unknown")),
                    "coverage_value": _safe_field_name(candidate.get("coverage_value", "none")),
                    "confidence": _safe_field_name(candidate.get("confidence", "unknown")),
                    "evidence_status": _safe_field_name(candidate.get("evidence_status", "unknown")),
                    "privacy_risk": _safe_field_name(candidate.get("privacy_risk", "unknown")),
                },
            )
    return rows


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
        return _public_safe_string(value, "public_value")
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, int | float):
        return value
    return str(value)


def _non_claims() -> dict[str, bool]:
    return {
        "parser_behavior_verified": False,
        "parser_truth_decided": False,
        "corpus_status_change_authorized": False,
        "fixture_promotion_authorized": False,
        "private_harvest_authorized": False,
        "pipeline_activation_ready_for_issue_388": False,
        "fixture_promotion_ready": False,
        "release_readiness": False,
        "analytics_truth": False,
        "ai_truth": False,
        "coaching_truth": False,
        "full_parser_regression_parity": False,
    }


def _privacy_class(value: Any) -> str:
    if isinstance(value, str) and value in PRIVACY_CLASSES:
        return value
    return "local_only_redacted"


def _safe_public_reason_list(value: Any) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        value = [value]
    reasons = []
    for item in value:
        if not isinstance(item, str):
            continue
        reasons.append(_public_safe_string(item, "rationale"))
    return reasons or ["reviewer_decision_supplied"]


def _safe_event_counts(value: Any) -> dict[str, int]:
    if not isinstance(value, Mapping):
        return {}
    counts: dict[str, int] = {}
    for key, count in sorted(value.items(), key=lambda item: str(item[0])):
        safe_key = _safe_field_name(str(key))
        if isinstance(count, bool):
            continue
        if isinstance(count, int) and count >= 0:
            counts[safe_key] = count
    return counts


def _safe_symbolic_list(value: Any) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        return []
    return sorted(_dedupe([_safe_field_name(str(item)) for item in value]))


def _nested_status(value: Mapping[str, Any], key: str) -> str:
    nested = value.get(key)
    if not isinstance(nested, Mapping):
        return "unknown"
    return _safe_status(nested.get("status", "unknown"))


def _safe_status(value: Any) -> str:
    if not isinstance(value, str):
        return "unknown"
    value = value.strip()
    if not value or _contains_forbidden_text(value):
        return "unknown"
    return _safe_field_name(value)


def _compact_public_mapping(value: Any) -> str:
    if not isinstance(value, Mapping) or not value:
        return "none"
    parts = [f"{_safe_field_name(key)}={count}" for key, count in sorted(value.items(), key=lambda item: str(item[0]))]
    return ", ".join(parts)


def _member_or_default(value: Any, accepted: frozenset[str], default: str) -> str:
    if isinstance(value, str) and value in accepted:
        return value
    return default


def _symbolic_or_default(value: Any, default: str) -> str:
    if isinstance(value, str) and _SYMBOLIC_TEXT_RE.match(value) and not _contains_forbidden_text(value):
        return value
    return default


def _symbolic_text(value: str, name: str) -> str:
    if not isinstance(value, str) or not _SYMBOLIC_TEXT_RE.match(value) or _contains_forbidden_text(value):
        raise HarvestReviewPacketError(f"{name} must be symbolic and public-safe")
    return value


def _public_safe_string(value: str, name: str) -> str:
    if not isinstance(value, str) or _contains_forbidden_text(value):
        raise HarvestReviewPacketError(f"{name} must be public-safe")
    return value


def _safe_field_name(value: Any) -> str:
    if not isinstance(value, str):
        return "unknown"
    value = value.strip()
    if not value or _contains_forbidden_text(value):
        return "unknown"
    cleaned = re.sub(r"[^A-Za-z0-9._:-]+", "_", value)
    if not _FIELD_NAME_RE.match(cleaned):
        return "unknown"
    return cleaned[:120]


def _contains_forbidden_text(value: str) -> bool:
    candidates = [value]
    decoded = unquote(value)
    if decoded != value:
        candidates.append(decoded)
    return any(
        _FORBIDDEN_TEXT_RE.search(candidate)
        or _FORBIDDEN_LABELED_PATH_RE.search(candidate)
        or _FORBIDDEN_URI_LOCAL_PATH_RE.search(candidate)
        for candidate in candidates
    )


def _dedupe(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output
