"""Synthetic-only local harvest candidate report builder."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any, Literal

from mythic_edge_parser.app.utc_log_source_adapter import UtcLogNormalizationResult

HARVEST_CANDIDATE_SUMMARY_OBJECT = "mythic_edge_harvest_candidate_summary"
HARVEST_CANDIDATE_SUMMARY_SCHEMA_VERSION = "parser_evidence_harvest_candidate_summary.v1"
PARSER_FACT_PREVIEW_OBJECT = "mythic_edge_parser_fact_preview"
PARSER_FACT_PREVIEW_SCHEMA_VERSION = "parser_evidence_parser_fact_preview.v1"
UTC_LOG_SOURCE_ADAPTER_VERSION = "utc_log_source_adapter.v1"
DEFAULT_CREATED_AT_UTC = "1970-01-01T00:00:00Z"

SourceKind = Literal[
    "synthetic_player_log",
    "synthetic_utc_log",
    "synthetic_normalized_utc_log",
    "user_selected_player_log",
    "user_selected_normalized_utc_log",
]
PrivacyClass = Literal["public_fixture", "synthetic", "private_local", "local_only_redacted"]
CandidateStatus = Literal[
    "candidate",
    "review",
    "blocked_private_evidence",
    "blocked_external_boundary",
    "duplicate_likely",
    "insufficient_evidence",
    "rejected",
]
EvidenceStatus = Literal["observed", "derived", "degraded", "unknown", "blocked"]
CoverageValue = Literal["none", "low", "medium", "high", "critical_gap_candidate"]
Confidence = Literal["unknown", "low", "medium", "high"]
RiskValue = Literal["none", "low", "medium", "high", "blocked"]

SOURCE_KINDS = frozenset(SourceKind.__args__)
PRIVACY_CLASSES = frozenset(PrivacyClass.__args__)
CANDIDATE_STATUSES = frozenset(CandidateStatus.__args__)
EVIDENCE_STATUSES = frozenset(EvidenceStatus.__args__)
COVERAGE_VALUES = frozenset(CoverageValue.__args__)
CONFIDENCE_VALUES = frozenset(Confidence.__args__)
RISK_VALUES = frozenset(RiskValue.__args__)

_SYNTHETIC_SOURCE_KINDS = frozenset(
    {
        "synthetic_player_log",
        "synthetic_utc_log",
        "synthetic_normalized_utc_log",
    },
)
_PRIVATE_SOURCE_KINDS = frozenset(
    {
        "user_selected_player_log",
        "user_selected_normalized_utc_log",
    },
)
_SYMBOLIC_TEXT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_SCENARIO_FAMILY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
_SAFE_CONTRACT_RE = re.compile(r"^docs/contracts/[A-Za-z0-9_.-]+\.md$")
_RAW_OR_PRIVATE_KEY_RE = re.compile(
    r"(^|_)(raw|payload|payloads|content|text|line|lines|path|paths|hash|offset|offsets|bytes|byte_range)($|_)",
    re.IGNORECASE,
)
_SAFE_SUMMARY_KEY_ALLOWLIST = frozenset(
    {
        "event_counts",
        "event_kinds",
        "total_event_count",
        "unknown_entry_count",
        "truncation_count",
        "warning_count",
        "degradation_status",
        "normalization",
        "source_adapter",
        "diagnostics_status",
        "drift_status",
        "raw_log_lines_included",
        "raw_payloads_included",
        "private_paths_included",
        "input_line_count",
        "output_line_count",
        "utc_frame_prefix_lines",
        "unchanged_lines",
        "dropped_lines",
        "replacement_character_count",
    },
)
_FORBIDDEN_TEXT_RE = re.compile(
    r"(\[UnityCrossThreadLogger\]|\[Client GRE\]|DETAILED LOGS:|"
    r"https?://script\.google\.com|https?://hooks\.|"
    r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}|"
    r"\b(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{8,}|"
    r"(?:^|\s)(?:/(?:Applications|Users|Volumes|etc|home|opt|private|tmp|var)\b|\b[A-Za-z]:[\\/]|\\\\))",
    re.IGNORECASE,
)
_COVERAGE_RANK = {
    value: index
    for index, value in enumerate(("none", "low", "medium", "high", "critical_gap_candidate"))
}
_RISK_RANK = {value: index for index, value in enumerate(("none", "low", "medium", "high", "blocked"))}


class HarvestCandidateReportError(ValueError):
    """Raised when a report input is outside the synthetic/in-memory boundary."""


def parser_evidence_from_utc_log_normalization(
    normalization: UtcLogNormalizationResult,
) -> dict[str, Any]:
    """Build sanitized parser-evidence metadata from a #381 UTC_Log normalization result."""

    stats = normalization.stats
    return {
        "source_adapter": UTC_LOG_SOURCE_ADAPTER_VERSION,
        "event_counts": {
            "normalized_line": stats.output_line_count,
        },
        "event_kinds": [],
        "normalization": {
            "input_line_count": stats.input_line_count,
            "output_line_count": stats.output_line_count,
            "utc_frame_prefix_lines": stats.utc_frame_prefix_lines,
            "unchanged_lines": stats.unchanged_lines,
            "dropped_lines": stats.dropped_lines,
            "replacement_character_count": stats.replacement_character_count,
            "degradation_status": stats.degradation_status,
            "warning_count": len(normalization.warnings),
        },
        "warning_count": len(normalization.warnings),
        "degradation_status": stats.degradation_status,
        "raw_log_lines_included": False,
        "raw_payloads_included": False,
        "private_paths_included": False,
    }


def build_harvest_candidate_report(
    *,
    source_label: str,
    source_kind: SourceKind,
    privacy_class: PrivacyClass,
    parser_evidence: Mapping[str, Any],
    diagnostics_summary: Mapping[str, Any] | None = None,
    drift_summary: Mapping[str, Any] | None = None,
    scenario_family_hints: Sequence[str] = (),
    created_at_utc: str = DEFAULT_CREATED_AT_UTC,
    report_id: str | None = None,
    related_contracts: Sequence[str] = (),
) -> dict[str, Any]:
    """Build a deterministic advisory candidate summary from supplied synthetic inputs."""

    normalized_source_label = _validate_symbolic_text(source_label, "source_label")
    normalized_source_kind = _validate_member(source_kind, SOURCE_KINDS, "source_kind")
    normalized_privacy_class = _validate_member(privacy_class, PRIVACY_CLASSES, "privacy_class")
    normalized_report_id = _validate_symbolic_text(
        report_id or f"{normalized_source_label}:candidate-summary",
        "report_id",
    )
    normalized_created_at = _validate_public_safe_string(created_at_utc, "created_at_utc")
    normalized_contracts = _validate_contracts(related_contracts)
    normalized_families = _validate_scenario_family_hints(scenario_family_hints)
    parser_context = _summary_context(parser_evidence, summary_name="parser_evidence")
    diagnostics_context = _summary_context(
        diagnostics_summary or {"diagnostics_status": "unavailable"},
        summary_name="diagnostics_summary",
    )
    drift_context = _summary_context(
        drift_summary or {"drift_status": "unavailable"},
        summary_name="drift_summary",
    )
    privacy_findings = _dedupe(
        [
            *parser_context["privacy_findings"],
            *diagnostics_context["privacy_findings"],
            *drift_context["privacy_findings"],
        ],
    )
    is_private_source = normalized_source_kind in _PRIVATE_SOURCE_KINDS or normalized_privacy_class in {
        "private_local",
        "local_only_redacted",
    }
    authorization_status = "missing_required" if is_private_source else "not_required_synthetic"

    candidates = [
        _scenario_candidate(
            family_id,
            parser_context=parser_context,
            diagnostics_context=diagnostics_context,
            drift_context=drift_context,
            privacy_findings=privacy_findings,
            authorization_status=authorization_status,
            related_contracts=normalized_contracts,
        )
        for family_id in normalized_families
    ]
    candidate_windows = [
        {
            "window_id": _window_id(normalized_source_label),
            "window_label": f"{normalized_source_label}:synthetic-window",
            "source_window_kind": (
                "unavailable" if is_private_source else _source_window_kind(normalized_source_kind)
            ),
            "public_location_included": not is_private_source,
            "local_pointer_ref": None,
            "scenario_family_candidates": candidates,
        },
    ]
    source_adapter = _source_adapter(normalized_source_kind, parser_context)
    report = {
        "object": HARVEST_CANDIDATE_SUMMARY_OBJECT,
        "schema_version": HARVEST_CANDIDATE_SUMMARY_SCHEMA_VERSION,
        "report_id": normalized_report_id,
        "created_at_utc": normalized_created_at,
        "source": {
            "source_label": normalized_source_label,
            "source_kind": normalized_source_kind,
            "privacy_class": normalized_privacy_class,
            "source_adapter": source_adapter,
            "raw_source_committed": False,
            "raw_path_included": False,
            "raw_hash_included": False,
            "raw_content_included": False,
        },
        "authorization": {
            "authorization_status": authorization_status,
            "authorization_issue": None,
            "private_harvest_authorized": False,
            "fixture_promotion_authorized": False,
        },
        "summary": _report_summary(candidates),
        "parser_fact_preview": _parser_fact_preview(
            source_label=normalized_source_label,
            privacy_class=normalized_privacy_class,
            parser_context=parser_context,
            diagnostics_context=diagnostics_context,
            drift_context=drift_context,
            privacy_findings=privacy_findings,
        ),
        "candidate_windows": candidate_windows,
        "privacy": {
            "privacy_findings": privacy_findings,
            "raw_private_logs_included": False,
            "raw_payload_values_included": False,
            "private_paths_included": False,
            "raw_hashes_included": False,
            "exact_offsets_included": False,
            "generated_artifacts_written": False,
        },
        "non_claims": {
            "parser_behavior_verified": False,
            "corpus_status_change_authorized": False,
            "fixture_promotion_authorized": False,
            "private_harvest_authorized": False,
            "pipeline_activation_ready_for_issue_388": False,
        },
    }
    return report


def _scenario_candidate(
    family_id: str,
    *,
    parser_context: Mapping[str, Any],
    diagnostics_context: Mapping[str, Any],
    drift_context: Mapping[str, Any],
    privacy_findings: Sequence[str],
    authorization_status: str,
    related_contracts: tuple[str, ...],
) -> dict[str, Any]:
    malformed = parser_context["malformed"] or diagnostics_context["malformed"] or drift_context["malformed"]
    has_evidence = parser_context["has_parser_evidence"]
    degradation = parser_context["degradation_status"]
    if privacy_findings:
        candidate_status: CandidateStatus = "rejected"
        evidence_status: EvidenceStatus = "blocked"
        coverage_value: CoverageValue = "none"
        confidence: Confidence = "unknown"
        privacy_risk: RiskValue = "blocked"
        reasons = ["privacy_boundary_blocked"]
        blocking_conditions = ["forbidden_or_private_content_detected"]
    elif authorization_status == "missing_required":
        candidate_status = "blocked_private_evidence"
        evidence_status = "blocked"
        coverage_value = "none"
        confidence = "unknown"
        privacy_risk = "blocked"
        reasons = ["private_source_requires_separate_approval"]
        blocking_conditions = ["missing_private_harvest_authorization"]
    elif malformed:
        candidate_status = "rejected"
        evidence_status = "unknown"
        coverage_value = "none"
        confidence = "unknown"
        privacy_risk = "low"
        reasons = ["malformed_summary_input"]
        blocking_conditions = ["summary_shape_not_accepted"]
    elif not has_evidence:
        candidate_status = "insufficient_evidence"
        evidence_status = "unknown"
        coverage_value = "none"
        confidence = "unknown"
        privacy_risk = "none"
        reasons = ["parser_evidence_missing_or_empty"]
        blocking_conditions = ["insufficient_parser_evidence"]
    else:
        evidence_status = "degraded" if degradation in {"review", "degraded", "failed"} else "observed"
        candidate_status = "review" if evidence_status == "degraded" else "candidate"
        coverage_value = "medium"
        confidence = "medium"
        privacy_risk = "none"
        reasons = ["synthetic_in_memory_parser_evidence_supplied"]
        blocking_conditions: list[str] = []

    if parser_context["warning_count"]:
        reasons.append("parser_evidence_has_warnings")
    if diagnostics_context["status"] not in {"", "unknown", "unavailable", "pass"}:
        reasons.append(f"diagnostics_status_{diagnostics_context['status']}")
    if drift_context["status"] not in {"", "unknown", "unavailable"}:
        reasons.append(f"drift_status_{drift_context['status']}")

    return {
        "family_id": family_id,
        "candidate_status": candidate_status,
        "evidence_status": evidence_status,
        "coverage_value": coverage_value,
        "confidence": confidence,
        "duplication_risk": "unknown",
        "privacy_risk": privacy_risk,
        "parser_behavior_applicable": True,
        "parser_behavior_verified": False,
        "reasons": _dedupe(reasons),
        "blocking_conditions": _dedupe(blocking_conditions),
        "related_contracts": list(related_contracts),
    }


def _parser_fact_preview(
    *,
    source_label: str,
    privacy_class: str,
    parser_context: Mapping[str, Any],
    diagnostics_context: Mapping[str, Any],
    drift_context: Mapping[str, Any],
    privacy_findings: Sequence[str],
) -> dict[str, Any]:
    if privacy_findings:
        preview_status = "blocked"
    elif parser_context["malformed"]:
        preview_status = "degraded"
    elif parser_context["has_parser_evidence"]:
        preview_status = (
            "degraded"
            if parser_context["degradation_status"] in {"review", "degraded", "failed"}
            else "available"
        )
    else:
        preview_status = "unavailable"
    return {
        "object": PARSER_FACT_PREVIEW_OBJECT,
        "schema_version": PARSER_FACT_PREVIEW_SCHEMA_VERSION,
        "source_label": source_label,
        "privacy_class": privacy_class,
        "preview_status": preview_status,
        "raw_log_lines_included": False,
        "raw_payloads_included": False,
        "private_paths_included": False,
        "event_counts": parser_context["event_counts"],
        "event_kinds": parser_context["event_kinds"],
        "diagnostics_summary": {
            "status": diagnostics_context["status"],
        },
        "drift_summary": {
            "status": drift_context["status"],
        },
        "state_summary": {
            "included": False,
            "reason": "not_in_scope_for_v1",
        },
    }


def _report_summary(candidates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "candidate_count": len(candidates),
        "blocked_candidate_count": sum(
            1
            for candidate in candidates
            if candidate["candidate_status"] in {"blocked_private_evidence", "blocked_external_boundary", "rejected"}
        ),
        "duplicate_likely_count": sum(
            1 for candidate in candidates if candidate["candidate_status"] == "duplicate_likely"
        ),
        "highest_privacy_risk": _highest_risk(candidate["privacy_risk"] for candidate in candidates),
        "highest_coverage_value": _highest_coverage(candidate["coverage_value"] for candidate in candidates),
    }


def _summary_context(summary: Mapping[str, Any], *, summary_name: str) -> dict[str, Any]:
    if not isinstance(summary, Mapping):
        return _malformed_context(summary_name, "summary_not_mapping")
    privacy_findings = _privacy_findings(summary, summary_name)
    malformed = False
    if privacy_findings:
        return _context_from_summary(summary, malformed=False, privacy_findings=privacy_findings)
    for key in summary:
        if not isinstance(key, str):
            malformed = True
            continue
        if _RAW_OR_PRIVATE_KEY_RE.search(key) and key not in _SAFE_SUMMARY_KEY_ALLOWLIST:
            privacy_findings.append(f"{summary_name}:forbidden_key")
    return _context_from_summary(summary, malformed=malformed, privacy_findings=_dedupe(privacy_findings))


def _context_from_summary(
    summary: Mapping[str, Any],
    *,
    malformed: bool,
    privacy_findings: Sequence[str],
) -> dict[str, Any]:
    event_counts = _safe_event_counts(summary.get("event_counts"))
    total_event_count = _safe_int(summary.get("total_event_count"), default=sum(event_counts.values()))
    if total_event_count and not event_counts:
        event_counts = {"total": total_event_count}
    event_kinds = _safe_event_kinds(summary.get("event_kinds"))
    status = _safe_status(
        summary.get("diagnostics_status", summary.get("drift_status", summary.get("status", "unknown"))),
    )
    warning_count = _safe_int(summary.get("warning_count"), default=0)
    degradation_status = _safe_status(summary.get("degradation_status", "ok"))
    has_parser_evidence = bool(event_counts or event_kinds or total_event_count)
    return {
        "malformed": malformed,
        "privacy_findings": list(privacy_findings),
        "event_counts": event_counts,
        "event_kinds": event_kinds,
        "status": status,
        "warning_count": warning_count,
        "degradation_status": degradation_status,
        "source_adapter": _safe_status(summary.get("source_adapter", "none")),
        "has_parser_evidence": has_parser_evidence,
    }


def _malformed_context(summary_name: str, reason: str) -> dict[str, Any]:
    return {
        "malformed": True,
        "privacy_findings": [],
        "event_counts": {},
        "event_kinds": [],
        "status": "unknown",
        "warning_count": 0,
        "degradation_status": "failed",
        "source_adapter": "none",
        "has_parser_evidence": False,
    }


def _source_adapter(source_kind: str, parser_context: Mapping[str, Any]) -> str:
    if source_kind in {"synthetic_utc_log", "synthetic_normalized_utc_log", "user_selected_normalized_utc_log"}:
        return UTC_LOG_SOURCE_ADAPTER_VERSION
    adapter = parser_context.get("source_adapter")
    return adapter if adapter in {"none", UTC_LOG_SOURCE_ADAPTER_VERSION} else "none"


def _source_window_kind(source_kind: str) -> str:
    if source_kind in {"synthetic_utc_log", "synthetic_normalized_utc_log"}:
        return "synthetic_line_range"
    return "synthetic_event_range"


def _window_id(source_label: str) -> str:
    return f"{source_label}:window-1"


def _safe_event_counts(value: Any) -> dict[str, int]:
    if not isinstance(value, Mapping):
        return {}
    counts: dict[str, int] = {}
    for key, count in sorted(value.items(), key=lambda item: str(item[0])):
        if not isinstance(key, str) or not _SCENARIO_FAMILY_RE.match(key):
            continue
        safe_count = _safe_int(count, default=0)
        if safe_count > 0:
            counts[key] = safe_count
    return counts


def _safe_event_kinds(value: Any) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str):
        return []
    return sorted(_dedupe(_validate_symbolic_text(str(item), "event_kind") for item in value))


def _safe_int(value: Any, *, default: int) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int) and value >= 0:
        return value
    return default


def _safe_status(value: Any) -> str:
    if not isinstance(value, str):
        return "unknown"
    value = value.strip()
    if not value:
        return "unknown"
    if _FORBIDDEN_TEXT_RE.search(value):
        return "unknown"
    return value


def _validate_member(value: str, accepted: frozenset[str], name: str) -> str:
    if value not in accepted:
        raise HarvestCandidateReportError(f"unknown {name}")
    return value


def _validate_symbolic_text(value: str, name: str) -> str:
    if not isinstance(value, str) or not _SYMBOLIC_TEXT_RE.match(value):
        raise HarvestCandidateReportError(f"{name} must be symbolic and public-safe")
    if _FORBIDDEN_TEXT_RE.search(value):
        raise HarvestCandidateReportError(f"{name} must be symbolic and public-safe")
    return value


def _validate_public_safe_string(value: str, name: str) -> str:
    if not isinstance(value, str) or _FORBIDDEN_TEXT_RE.search(value):
        raise HarvestCandidateReportError(f"{name} must be public-safe")
    return value


def _validate_scenario_family_hints(values: Sequence[str]) -> tuple[str, ...]:
    if isinstance(values, str):
        raise HarvestCandidateReportError("scenario_family_hints must be a sequence")
    families = []
    for value in values:
        if not isinstance(value, str) or not _SCENARIO_FAMILY_RE.match(value):
            raise HarvestCandidateReportError("scenario_family_hints must be public-safe")
        if _FORBIDDEN_TEXT_RE.search(value):
            raise HarvestCandidateReportError("scenario_family_hints must be public-safe")
        families.append(value)
    return tuple(_dedupe(families))


def _validate_contracts(values: Sequence[str]) -> tuple[str, ...]:
    if isinstance(values, str):
        raise HarvestCandidateReportError("related_contracts must be a sequence")
    contracts = []
    for value in values:
        if not isinstance(value, str) or not _SAFE_CONTRACT_RE.match(value):
            raise HarvestCandidateReportError("related_contracts must be repo-relative contract paths")
        contracts.append(value)
    return tuple(_dedupe(contracts))


def _privacy_findings(value: Any, label: str) -> list[str]:
    findings: list[str] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_label = str(key)
            event_count_key = label.endswith(".event_counts")
            if (
                isinstance(key, str)
                and not event_count_key
                and _RAW_OR_PRIVATE_KEY_RE.search(key)
                and key not in _SAFE_SUMMARY_KEY_ALLOWLIST
            ):
                findings.append(f"{label}:forbidden_key")
                continue
            findings.extend(_privacy_findings(item, f"{label}.{key_label}"))
    elif isinstance(value, Sequence) and not isinstance(value, str):
        for index, item in enumerate(value):
            findings.extend(_privacy_findings(item, f"{label}[{index}]"))
    elif isinstance(value, str) and _FORBIDDEN_TEXT_RE.search(value):
        findings.append(f"{label}:forbidden_text")
    return _dedupe(findings)


def _highest_coverage(values: Sequence[Any]) -> str:
    highest = "none"
    for value in values:
        if isinstance(value, str) and value in _COVERAGE_RANK and _COVERAGE_RANK[value] > _COVERAGE_RANK[highest]:
            highest = value
    return highest


def _highest_risk(values: Sequence[Any]) -> str:
    highest = "none"
    for value in values:
        if isinstance(value, str) and value in _RISK_RANK and _RISK_RANK[value] > _RISK_RANK[highest]:
            highest = value
    return highest


def _dedupe(values: Sequence[str] | Any) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output
