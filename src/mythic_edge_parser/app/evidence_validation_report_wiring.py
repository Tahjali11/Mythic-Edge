"""Summary-only evidence-ledger review wiring for validation reports."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .privacy_url_detection import contains_runtime_artifact_url

EVIDENCE_LEDGER_REVIEW_OBJECT = "mythic_edge_player_log_evidence_ledger_validation_review"
EVIDENCE_LEDGER_REVIEW_SCHEMA_VERSION = "player_log_evidence_ledger_validation_review.v1"
EVIDENCE_LEDGER_REVIEW_STATUSES = (
    "not_supplied",
    "pass",
    "degraded",
    "review",
    "diff",
    "fail",
)
EVIDENCE_LEDGER_REVIEW_SOURCE_KEYS = (
    "runtime_field_evidence_report",
    "schema_drift_report",
    "invariant_execution_report",
    "schema_snapshot_comparison",
)

REPORT_CONTEXTS = (
    "parser_diagnostics",
    "golden_replay",
    "feature_equity_corpus_ratchet",
    "synthetic_test_reference",
)

STATUS_NOT_SUPPLIED = "not_supplied"
STATUS_PASS = "pass"
STATUS_DEGRADED = "degraded"
STATUS_REVIEW = "review"
STATUS_DIFF = "diff"
STATUS_FAIL = "fail"
STATUS_PRECEDENCE = (
    STATUS_FAIL,
    STATUS_DIFF,
    STATUS_REVIEW,
    STATUS_DEGRADED,
    STATUS_PASS,
    STATUS_NOT_SUPPLIED,
)

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "runtime_field_evidence_report": {
        "object": "mythic_edge_player_log_runtime_field_evidence_report",
        "schema_version": "player_log_runtime_field_evidence_report.v1",
        "statuses": (STATUS_PASS, STATUS_REVIEW, STATUS_FAIL),
        "summary_fields": (
            "attachment_count",
            "valid_field_evidence_count",
            "missing_mapping_count",
            "ambiguous_mapping_count",
            "review_required_count",
            "conflict_count",
            "degraded_count",
            "not_checked_count",
            "drift_flag_count",
        ),
    },
    "schema_drift_report": {
        "object": "mythic_edge_player_log_evidence_schema_drift_report",
        "schema_version": "player_log_evidence_schema_drift_report.v1",
        "statuses": (STATUS_PASS, STATUS_REVIEW, STATUS_FAIL),
        "summary_fields": (
            "output_family_changes",
            "entry_changes",
            "evidence_signal_changes",
            "vocabulary_changes",
            "policy_changes",
            "privacy_findings",
        ),
    },
    "invariant_execution_report": {
        "object": "mythic_edge_player_log_evidence_invariant_execution_report",
        "schema_version": "player_log_evidence_invariant_execution.v1",
        "statuses": (STATUS_PASS, STATUS_REVIEW, STATUS_FAIL),
        "summary_fields": (
            "executable_invariant_count",
            "declared_invariant_total_count",
            "declared_invariant_unique_count",
            "passed_count",
            "failed_count",
            "degraded_count",
            "not_applicable_count",
            "not_checked_count",
            "affected_entry_count",
            "affected_output_family_count",
            "drift_flag_count",
        ),
    },
    "schema_snapshot_comparison": {
        "object": "mythic_edge_player_log_evidence_schema_snapshot_comparison",
        "schema_version": "player_log_evidence_schema_snapshot_comparison.v1",
        "statuses": (STATUS_PASS, STATUS_DIFF, STATUS_FAIL),
        "summary_fields": (
            "output_family_changes",
            "entry_changes",
            "evidence_signal_changes",
            "vocabulary_changes",
            "policy_changes",
            "privacy_findings",
        ),
    },
}

SUMMARY_FIELDS = (
    "source_report_count",
    "supplied_source_report_count",
    "pass_count",
    "degraded_count",
    "review_count",
    "diff_count",
    "fail_count",
    "runtime_field_evidence_attachment_count",
    "runtime_field_evidence_review_required_count",
    "runtime_field_evidence_missing_mapping_count",
    "schema_drift_changed_entry_count",
    "schema_drift_changed_signal_count",
    "invariant_failed_count",
    "invariant_degraded_count",
    "invariant_not_checked_count",
    "drift_flag_count",
    "protected_surface_violation_count",
)

FORBIDDEN_REVIEW_DETAIL_KEYS = {
    "attachments",
    "field_evidence",
    "invariant_results",
    "snapshot",
    "snapshots",
    "schema_snapshot",
    "schema_snapshots",
    "diff",
    "drift_diff",
}

PROTECTED_SURFACE_ASSERTIONS = {
    "parser_behavior_changed": False,
    "parser_state_final_reconciliation_changed": False,
    "parser_event_classes_changed": False,
    "router_semantics_changed": False,
    "diagnostics_report_semantics_changed": False,
    "golden_replay_expected_fixture_truth_changed": False,
    "feature_equity_baseline_update_policy_changed": False,
    "workbook_schema_changed": False,
    "webhook_payload_shape_changed": False,
    "apps_script_behavior_changed": False,
    "output_transport_changed": False,
    "runtime_status_schema_changed": False,
    "match_journal_behavior_changed": False,
    "overlay_behavior_changed": False,
    "sqlite_behavior_changed": False,
    "google_sheets_sync_behavior_changed": False,
    "analytics_or_ai_truth_changed": False,
    "ci_merge_deploy_policy_changed": False,
}

ABSOLUTE_PATH_RE = re.compile(
    r"(?:^|\s)(?:/(?:Applications|Users|Volumes|etc|home|opt|private|tmp|var)\b|\b[A-Za-z]:[\\/]|\\\\)",
)
FORBIDDEN_TEXT_RE = re.compile(
    r"(\[UnityCrossThreadLogger\]|\[Client GRE\]|DETAILED LOGS:|"
    r"https?://script\.google\.com|https?://hooks\.|"
    r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}|"
    r"\b(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{8,})",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https?://[^\s)>\]}\"]+")
SAFE_PATH_RE = re.compile(r"[^A-Za-z0-9_.-]+")


def build_evidence_ledger_review_section(
    *,
    runtime_field_evidence_report: Mapping[str, Any] | None = None,
    schema_drift_report: Mapping[str, Any] | None = None,
    invariant_execution_report: Mapping[str, Any] | None = None,
    schema_snapshot_comparison: Mapping[str, Any] | None = None,
    report_context: str,
) -> dict[str, Any]:
    """Build a summary-only evidence-ledger review section."""

    raw_sources = {
        "runtime_field_evidence_report": runtime_field_evidence_report,
        "schema_drift_report": schema_drift_report,
        "invariant_execution_report": invariant_execution_report,
        "schema_snapshot_comparison": schema_snapshot_comparison,
    }
    sources: dict[str, dict[str, Any]] = {}
    statuses: list[str] = []
    status_reasons: list[str] = []
    privacy = _empty_privacy()
    protected_violation_count = 0
    affected = {
        "output_families": set[str](),
        "entries": set[str](),
        "evidence_signals": set[str](),
    }
    review_guidance = {
        "recommended_review_modules": set[str](),
        "recommended_tests": set[str](),
        "review_notes": set[str](),
    }
    drift_flags: set[str] = set()

    normalized_context = _safe_text(report_context)
    if normalized_context not in REPORT_CONTEXTS:
        normalized_context = str(report_context or "").strip() or "unknown"
        statuses.append(STATUS_FAIL)
        status_reasons.append("unknown_report_context")

    supplied_source_count = 0
    for source_key in EVIDENCE_LEDGER_REVIEW_SOURCE_KEYS:
        source = raw_sources[source_key]
        source_section, source_context = _source_section(
            source_key,
            source,
            report_context=normalized_context,
        )
        sources[source_key] = source_section
        if source_section["supplied"]:
            supplied_source_count += 1
            statuses.append(source_section["status"])
            status_reasons.extend(f"{source_key}:{reason}" for reason in source_section["status_reasons"])
            _merge_privacy(privacy, source_context["privacy"])
            protected_violation_count += source_context["protected_violation_count"]
            for key in affected:
                affected[key].update(source_context["affected"][key])
            for key in review_guidance:
                review_guidance[key].update(source_context["review_guidance"][key])
            drift_flags.update(source_context["drift_flags"])

    limitations: list[str] = [
        "Evidence ledger review is summary-only and does not affect parent report status.",
    ]
    if supplied_source_count == 0:
        statuses.append(STATUS_NOT_SUPPLIED)
        limitations.append("No evidence-ledger review source reports were supplied.")

    status = _highest_status(statuses)
    if _has_privacy_findings(privacy):
        status = STATUS_FAIL
        status_reasons.append("privacy_findings")
    if protected_violation_count:
        status = STATUS_FAIL
        status_reasons.append("protected_surface_assertion_true")

    summary = _summary(
        supplied_source_count=supplied_source_count,
        sources=sources,
        drift_flag_count=len(drift_flags),
        protected_violation_count=protected_violation_count,
    )
    section = {
        "object": EVIDENCE_LEDGER_REVIEW_OBJECT,
        "schema_version": EVIDENCE_LEDGER_REVIEW_SCHEMA_VERSION,
        "report_context": normalized_context,
        "status": status,
        "review_required": status in {STATUS_DEGRADED, STATUS_REVIEW, STATUS_DIFF, STATUS_FAIL},
        "status_affects_parent": False,
        "status_reasons": _safe_string_list(status_reasons),
        "summary": summary,
        "sources": sources,
        "drift_flags": _safe_string_list(drift_flags),
        "affected": {key: _safe_string_list(values) for key, values in affected.items()},
        "review_guidance": {key: _safe_string_list(values) for key, values in review_guidance.items()},
        "privacy": _sorted_privacy(privacy),
        "protected_surface_assertions": dict(PROTECTED_SURFACE_ASSERTIONS),
        "limitations": _safe_string_list(limitations),
    }

    section_privacy = _privacy_findings(section, "evidence_ledger_review")
    if _has_privacy_findings(section_privacy):
        section["status"] = STATUS_FAIL
        section["review_required"] = True
        section["status_reasons"] = _safe_string_list(
            [*section["status_reasons"], "integrated_report_privacy_findings"],
        )
        _merge_privacy(section["privacy"], section_privacy)
    return section


def load_evidence_review_json(path: Path) -> dict[str, Any]:
    """Load an explicit evidence review JSON report without raising."""

    safe_path = _safe_path_label(path)
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        return _malformed_loaded_report(safe_path, f"json_load_error:{exc.__class__.__name__}")
    if not isinstance(payload, Mapping):
        return _malformed_loaded_report(safe_path, "json_payload_not_mapping")
    return dict(payload)


def evidence_review_cli_arguments(parser: Any) -> None:
    """Add optional explicit evidence review source report arguments."""

    parser.add_argument(
        "--evidence-runtime-field-report",
        dest="evidence_runtime_field_report",
        default="",
        help="Optional explicit runtime field-evidence report JSON path.",
    )
    parser.add_argument(
        "--evidence-schema-drift-report",
        dest="evidence_schema_drift_report",
        default="",
        help="Optional explicit evidence schema drift report JSON path.",
    )
    parser.add_argument(
        "--evidence-invariant-report",
        dest="evidence_invariant_report",
        default="",
        help="Optional explicit evidence invariant execution report JSON path.",
    )
    parser.add_argument(
        "--evidence-schema-snapshot-comparison",
        dest="evidence_schema_snapshot_comparison",
        default="",
        help="Optional explicit evidence schema snapshot comparison JSON path.",
    )


def evidence_review_inputs_from_args(args: Any) -> dict[str, Any]:
    """Return source report inputs from explicit CLI arguments only."""

    inputs: dict[str, Any] = {}
    arg_map = {
        "runtime_field_evidence_report": "evidence_runtime_field_report",
        "schema_drift_report": "evidence_schema_drift_report",
        "invariant_execution_report": "evidence_invariant_report",
        "schema_snapshot_comparison": "evidence_schema_snapshot_comparison",
    }
    for source_key, attr_name in arg_map.items():
        raw_path = str(getattr(args, attr_name, "") or "").strip()
        if raw_path:
            inputs[source_key] = load_evidence_review_json(Path(raw_path))
    return inputs


def evidence_review_section_from_inputs(
    evidence_ledger_review: Mapping[str, Any] | None,
    *,
    report_context: str,
) -> dict[str, Any]:
    """Build a review section from optional caller-provided source inputs."""

    if isinstance(evidence_ledger_review, Mapping):
        if evidence_ledger_review.get("object") == EVIDENCE_LEDGER_REVIEW_OBJECT:
            return _sanitize_existing_section(evidence_ledger_review, report_context=report_context)
        inputs = {
            key: evidence_ledger_review.get(key)
            for key in EVIDENCE_LEDGER_REVIEW_SOURCE_KEYS
            if key in evidence_ledger_review
        }
    else:
        inputs = {}
    return build_evidence_ledger_review_section(report_context=report_context, **inputs)


def _source_section(
    source_key: str,
    source: Any,
    *,
    report_context: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if source is None:
        return _empty_source_section(), _empty_source_context()

    context = _empty_source_context()
    if not isinstance(source, Mapping):
        section = _supplied_source_section(
            object_value="",
            schema_version="",
            status=STATUS_FAIL,
            review_required=True,
            status_reasons=["malformed_source_report"],
            summary={},
        )
        return section, context

    spec = SOURCE_SPECS[source_key]
    object_value = _safe_text(source.get("object"))
    schema_version = _safe_text(source.get("schema_version"))
    raw_status = _safe_text(source.get("status"))
    status_reasons: list[str] = []
    normalized_status = (
        STATUS_PASS
        if raw_status == "ok" and report_context == "feature_equity_corpus_ratchet"
        else raw_status
    )

    if object_value != spec["object"]:
        normalized_status = STATUS_FAIL
        status_reasons.append("unknown_source_object")
    if schema_version != spec["schema_version"]:
        normalized_status = STATUS_FAIL
        status_reasons.append("unknown_source_schema_version")
    if raw_status not in spec["statuses"] and not (
        raw_status == "ok" and report_context == "feature_equity_corpus_ratchet"
    ):
        normalized_status = STATUS_FAIL
        status_reasons.append("unknown_source_status")
    elif normalized_status != STATUS_PASS:
        status_reasons.append(f"source_status_{normalized_status}")

    source_privacy = _source_privacy_findings(source, source_key)
    context["privacy"] = source_privacy
    if _has_privacy_findings(source_privacy):
        normalized_status = STATUS_FAIL
        status_reasons.append("privacy_findings")

    protected_violations = _protected_violations(source, source_key)
    context["protected_violation_count"] = len(protected_violations)
    if protected_violations:
        normalized_status = STATUS_FAIL
        status_reasons.append("protected_surface_assertion_true")

    status_reasons.extend(_safe_string_list(source.get("status_reasons") if isinstance(source, Mapping) else []))
    summary = _source_summary(source.get("summary"), spec["summary_fields"])
    context["drift_flags"].update(_safe_string_list(source.get("drift_flags")))
    context["affected"] = _source_affected(source.get("affected"))
    context["review_guidance"] = _source_review_guidance(source.get("review_guidance"))
    section = _supplied_source_section(
        object_value=object_value,
        schema_version=schema_version,
        status=normalized_status if normalized_status in EVIDENCE_LEDGER_REVIEW_STATUSES else STATUS_FAIL,
        review_required=bool(source.get("review_required")) or normalized_status != STATUS_PASS,
        status_reasons=status_reasons,
        summary=summary,
    )
    return section, context


def _empty_source_section() -> dict[str, Any]:
    return {
        "supplied": False,
        "object": "",
        "schema_version": "",
        "status": STATUS_NOT_SUPPLIED,
        "review_required": False,
        "status_reasons": [],
        "summary": {},
    }


def _supplied_source_section(
    *,
    object_value: str,
    schema_version: str,
    status: str,
    review_required: bool,
    status_reasons: Sequence[str],
    summary: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "supplied": True,
        "object": object_value,
        "schema_version": schema_version,
        "status": status,
        "review_required": bool(review_required),
        "status_reasons": _safe_string_list(status_reasons),
        "summary": dict(summary),
    }


def _empty_source_context() -> dict[str, Any]:
    return {
        "privacy": _empty_privacy(),
        "protected_violation_count": 0,
        "affected": {
            "output_families": set[str](),
            "entries": set[str](),
            "evidence_signals": set[str](),
        },
        "review_guidance": {
            "recommended_review_modules": set[str](),
            "recommended_tests": set[str](),
            "review_notes": set[str](),
        },
        "drift_flags": set[str](),
    }


def _summary(
    *,
    supplied_source_count: int,
    sources: Mapping[str, Mapping[str, Any]],
    drift_flag_count: int,
    protected_violation_count: int,
) -> dict[str, int]:
    status_counts = {status: 0 for status in EVIDENCE_LEDGER_REVIEW_STATUSES}
    for source in sources.values():
        if source.get("supplied"):
            status_counts[str(source.get("status") or STATUS_FAIL)] = (
                status_counts.get(str(source.get("status") or STATUS_FAIL), 0) + 1
            )
    runtime_summary = _source_summary_for(sources, "runtime_field_evidence_report")
    drift_summary = _source_summary_for(sources, "schema_drift_report")
    invariant_summary = _source_summary_for(sources, "invariant_execution_report")
    snapshot_summary = _source_summary_for(sources, "schema_snapshot_comparison")
    return {
        "source_report_count": supplied_source_count,
        "supplied_source_report_count": supplied_source_count,
        "pass_count": status_counts[STATUS_PASS],
        "degraded_count": status_counts[STATUS_DEGRADED],
        "review_count": status_counts[STATUS_REVIEW],
        "diff_count": status_counts[STATUS_DIFF],
        "fail_count": status_counts[STATUS_FAIL],
        "runtime_field_evidence_attachment_count": _safe_int(runtime_summary.get("attachment_count")),
        "runtime_field_evidence_review_required_count": _safe_int(runtime_summary.get("review_required_count")),
        "runtime_field_evidence_missing_mapping_count": _safe_int(runtime_summary.get("missing_mapping_count")),
        "schema_drift_changed_entry_count": _safe_int(drift_summary.get("entry_changes"))
        + _safe_int(snapshot_summary.get("entry_changes")),
        "schema_drift_changed_signal_count": _safe_int(drift_summary.get("evidence_signal_changes"))
        + _safe_int(snapshot_summary.get("evidence_signal_changes")),
        "invariant_failed_count": _safe_int(invariant_summary.get("failed_count")),
        "invariant_degraded_count": _safe_int(invariant_summary.get("degraded_count")),
        "invariant_not_checked_count": _safe_int(invariant_summary.get("not_checked_count")),
        "drift_flag_count": drift_flag_count,
        "protected_surface_violation_count": protected_violation_count,
    }


def _source_summary_for(sources: Mapping[str, Mapping[str, Any]], source_key: str) -> Mapping[str, Any]:
    source = sources.get(source_key, {})
    summary = source.get("summary") if isinstance(source, Mapping) else {}
    return summary if isinstance(summary, Mapping) else {}


def _source_summary(summary: Any, allowed_fields: Sequence[str]) -> dict[str, Any]:
    if not isinstance(summary, Mapping):
        return {}
    return {
        field: _safe_json_scalar(summary.get(field))
        for field in allowed_fields
        if field in summary
    }


def _source_affected(raw: Any) -> dict[str, set[str]]:
    if not isinstance(raw, Mapping):
        return {
            "output_families": set(),
            "entries": set(),
            "evidence_signals": set(),
        }
    return {
        "output_families": set(_safe_string_list(raw.get("output_families"))),
        "entries": set(_safe_string_list(raw.get("entries"))),
        "evidence_signals": set(_safe_string_list(raw.get("evidence_signals"))),
    }


def _source_review_guidance(raw: Any) -> dict[str, set[str]]:
    if not isinstance(raw, Mapping):
        return {
            "recommended_review_modules": set(),
            "recommended_tests": set(),
            "review_notes": set(),
        }
    return {
        "recommended_review_modules": set(_safe_string_list(raw.get("recommended_review_modules"))),
        "recommended_tests": set(_safe_string_list(raw.get("recommended_tests"))),
        "review_notes": set(_safe_string_list(raw.get("review_notes"))),
    }


def _source_privacy_findings(source: Mapping[str, Any], source_key: str) -> dict[str, list[str]]:
    findings = _privacy_findings(source, source_key)
    privacy = source.get("privacy")
    if isinstance(privacy, Mapping):
        for key in (
            "forbidden_content_findings",
            "local_absolute_paths_found",
        ):
            if _has_items(privacy.get(key)):
                findings[key].append(f"{source_key}.privacy.{key}")
        for key in (
            "raw_private_logs_included",
            "raw_payload_values_included",
            "runtime_artifacts_included",
            "generated_data_included",
        ):
            if privacy.get(key) is True:
                findings[key] = True
    return _sorted_privacy(findings)


def _privacy_findings(payload: Any, path: str) -> dict[str, Any]:
    findings = _empty_privacy()
    _collect_privacy_findings(payload, path, findings)
    return _sorted_privacy(findings)


def _collect_privacy_findings(payload: Any, path: str, findings: dict[str, Any]) -> None:
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            _collect_privacy_findings(value, f"{path}.{_safe_path_segment(key)}", findings)
        return
    if isinstance(payload, Sequence) and not isinstance(payload, str | bytes | bytearray):
        for index, value in enumerate(payload):
            _collect_privacy_findings(value, f"{path}[{index}]", findings)
        return
    if not isinstance(payload, str):
        return

    if FORBIDDEN_TEXT_RE.search(payload):
        findings["forbidden_content_findings"].append(path)
        if "[UnityCrossThreadLogger]" in payload or "[Client GRE]" in payload or "DETAILED LOGS:" in payload:
            findings["raw_private_logs_included"] = True
        if contains_runtime_artifact_url(payload):
            findings["runtime_artifacts_included"] = True
    if ABSOLUTE_PATH_RE.search(payload):
        findings["local_absolute_paths_found"].append(path)


def _empty_privacy() -> dict[str, Any]:
    return {
        "forbidden_content_findings": [],
        "local_absolute_paths_found": [],
        "raw_private_logs_included": False,
        "raw_payload_values_included": False,
        "runtime_artifacts_included": False,
        "generated_data_included": False,
        "full_field_evidence_attachments_included": False,
        "full_schema_snapshots_included": False,
    }


def _merge_privacy(target: dict[str, Any], source: Mapping[str, Any]) -> None:
    for key in ("forbidden_content_findings", "local_absolute_paths_found"):
        target[key] = _safe_string_list([*target.get(key, []), *list(source.get(key, []))])
    for key in (
        "raw_private_logs_included",
        "raw_payload_values_included",
        "runtime_artifacts_included",
        "generated_data_included",
        "full_field_evidence_attachments_included",
        "full_schema_snapshots_included",
    ):
        target[key] = bool(target.get(key)) or bool(source.get(key))


def _sorted_privacy(privacy: Mapping[str, Any]) -> dict[str, Any]:
    clean = _empty_privacy()
    for key in ("forbidden_content_findings", "local_absolute_paths_found"):
        clean[key] = _safe_string_list(privacy.get(key))
    for key in (
        "raw_private_logs_included",
        "raw_payload_values_included",
        "runtime_artifacts_included",
        "generated_data_included",
        "full_field_evidence_attachments_included",
        "full_schema_snapshots_included",
    ):
        clean[key] = bool(privacy.get(key))
    return clean


def _has_privacy_findings(privacy: Mapping[str, Any]) -> bool:
    return bool(privacy.get("forbidden_content_findings")) or bool(privacy.get("local_absolute_paths_found")) or any(
        bool(privacy.get(key))
        for key in (
            "raw_private_logs_included",
            "raw_payload_values_included",
            "runtime_artifacts_included",
            "generated_data_included",
        )
    )


def _protected_violations(source: Mapping[str, Any], source_key: str) -> list[str]:
    assertions = source.get("protected_surface_assertions")
    if not isinstance(assertions, Mapping):
        return []
    return _safe_string_list(
        f"{source_key}.protected_surface_assertions.{key}"
        for key, value in assertions.items()
        if value is not False
    )


def _sanitize_existing_section(section: Mapping[str, Any], *, report_context: str) -> dict[str, Any]:
    payload = json.loads(json.dumps(section, default=str))
    if not isinstance(payload, dict):
        return build_evidence_ledger_review_section(report_context=report_context)
    normalized_context = (
        report_context
        if report_context in REPORT_CONTEXTS
        else _safe_text(payload.get("report_context"))
    )
    if normalized_context not in REPORT_CONTEXTS:
        normalized_context = "unknown"
    status_reasons = _safe_string_list(payload.get("status_reasons"))
    status = _safe_text(payload.get("status"))
    if status not in EVIDENCE_LEDGER_REVIEW_STATUSES:
        status = STATUS_FAIL
        status_reasons.append("unknown_review_section_status")
    if payload.get("schema_version") != EVIDENCE_LEDGER_REVIEW_SCHEMA_VERSION:
        status = STATUS_FAIL
        status_reasons.append("unknown_review_section_schema_version")

    privacy = _sorted_privacy(payload.get("privacy") if isinstance(payload.get("privacy"), Mapping) else {})
    payload_privacy = _privacy_findings(payload, "evidence_ledger_review")
    detail_findings = _forbidden_review_detail_findings(payload, "evidence_ledger_review")
    if detail_findings["paths"]:
        status = STATUS_FAIL
        status_reasons.append("forbidden_full_detail_keys")
        privacy["forbidden_content_findings"] = _safe_string_list(
            [*privacy["forbidden_content_findings"], *detail_findings["paths"]]
        )
        privacy["full_field_evidence_attachments_included"] = bool(
            privacy["full_field_evidence_attachments_included"]
            or detail_findings["field_evidence_attachments"]
        )
        privacy["full_schema_snapshots_included"] = bool(
            privacy["full_schema_snapshots_included"] or detail_findings["schema_snapshots"]
        )
    if _has_privacy_findings(payload_privacy):
        status = STATUS_FAIL
        status_reasons.append("integrated_report_privacy_findings")
        _merge_privacy(privacy, payload_privacy)

    protected_assertions = dict(PROTECTED_SURFACE_ASSERTIONS)
    supplied_assertions = payload.get("protected_surface_assertions")
    protected_violation_count = 0
    if isinstance(supplied_assertions, Mapping):
        protected_violation_count = sum(1 for value in supplied_assertions.values() if value is not False)
        if protected_violation_count:
            status = STATUS_FAIL
            status_reasons.append("protected_surface_assertion_true")

    return {
        "object": EVIDENCE_LEDGER_REVIEW_OBJECT,
        "schema_version": EVIDENCE_LEDGER_REVIEW_SCHEMA_VERSION,
        "report_context": normalized_context,
        "status": status,
        "review_required": bool(payload.get("review_required"))
        or status in {STATUS_DEGRADED, STATUS_REVIEW, STATUS_DIFF, STATUS_FAIL},
        "status_affects_parent": False,
        "status_reasons": _safe_string_list(status_reasons),
        "summary": _sanitize_existing_summary(payload.get("summary"), protected_violation_count),
        "sources": _sanitize_existing_sources(payload.get("sources")),
        "drift_flags": _safe_string_list(payload.get("drift_flags")),
        "affected": _sanitize_existing_affected(payload.get("affected")),
        "review_guidance": _sanitize_existing_review_guidance(payload.get("review_guidance")),
        "privacy": _sorted_privacy(privacy),
        "protected_surface_assertions": protected_assertions,
        "limitations": _safe_string_list(payload.get("limitations")),
    }


def _sanitize_existing_summary(raw: Any, protected_violation_count: int) -> dict[str, int]:
    source = raw if isinstance(raw, Mapping) else {}
    summary = {field: _safe_int(source.get(field)) for field in SUMMARY_FIELDS}
    if protected_violation_count:
        summary["protected_surface_violation_count"] = protected_violation_count
    return summary


def _sanitize_existing_sources(raw: Any) -> dict[str, dict[str, Any]]:
    source_sections = raw if isinstance(raw, Mapping) else {}
    sources: dict[str, dict[str, Any]] = {}
    for source_key in EVIDENCE_LEDGER_REVIEW_SOURCE_KEYS:
        source = source_sections.get(source_key) if isinstance(source_sections, Mapping) else None
        if not isinstance(source, Mapping):
            sources[source_key] = _empty_source_section()
            continue
        status = _safe_text(source.get("status"))
        if status not in EVIDENCE_LEDGER_REVIEW_STATUSES:
            status = STATUS_FAIL
        sources[source_key] = _supplied_source_section(
            object_value=_safe_text(source.get("object")),
            schema_version=_safe_text(source.get("schema_version")),
            status=status,
            review_required=bool(source.get("review_required"))
            or status in {STATUS_DEGRADED, STATUS_REVIEW, STATUS_DIFF, STATUS_FAIL},
            status_reasons=_safe_string_list(source.get("status_reasons")),
            summary=_source_summary(
                source.get("summary"),
                SOURCE_SPECS[source_key]["summary_fields"],
            ),
        )
    return sources


def _sanitize_existing_affected(raw: Any) -> dict[str, list[str]]:
    source = raw if isinstance(raw, Mapping) else {}
    return {
        "output_families": _safe_string_list(source.get("output_families")),
        "entries": _safe_string_list(source.get("entries")),
        "evidence_signals": _safe_string_list(source.get("evidence_signals")),
    }


def _sanitize_existing_review_guidance(raw: Any) -> dict[str, list[str]]:
    source = raw if isinstance(raw, Mapping) else {}
    return {
        "recommended_review_modules": _safe_string_list(source.get("recommended_review_modules")),
        "recommended_tests": _safe_string_list(source.get("recommended_tests")),
        "review_notes": _safe_string_list(source.get("review_notes")),
    }


def _forbidden_review_detail_findings(payload: Any, path: str) -> dict[str, Any]:
    findings = {
        "paths": [],
        "field_evidence_attachments": False,
        "schema_snapshots": False,
    }
    _collect_forbidden_review_detail_findings(payload, path, findings)
    findings["paths"] = _safe_string_list(findings["paths"])
    return findings


def _collect_forbidden_review_detail_findings(payload: Any, path: str, findings: dict[str, Any]) -> None:
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            key_text = str(key)
            child_path = f"{path}.{_safe_path_segment(key)}"
            if key_text in FORBIDDEN_REVIEW_DETAIL_KEYS:
                findings["paths"].append(child_path)
                if key_text in {"attachments", "field_evidence"}:
                    findings["field_evidence_attachments"] = True
                if "snapshot" in key_text:
                    findings["schema_snapshots"] = True
                continue
            _collect_forbidden_review_detail_findings(value, child_path, findings)
        return
    if isinstance(payload, Sequence) and not isinstance(payload, str | bytes | bytearray):
        for index, value in enumerate(payload):
            _collect_forbidden_review_detail_findings(value, f"{path}[{index}]", findings)


def _malformed_loaded_report(safe_path: str, reason: str) -> dict[str, Any]:
    return {
        "object": "",
        "schema_version": "",
        "status": STATUS_FAIL,
        "review_required": True,
        "status_reasons": [reason],
        "summary": {},
        "affected": {"output_families": [], "entries": [], "evidence_signals": []},
        "review_guidance": {
            "recommended_review_modules": [],
            "recommended_tests": [],
            "review_notes": [f"Could not load explicit evidence review input {safe_path}."],
        },
        "drift_flags": [],
        "privacy": _empty_privacy(),
        "protected_surface_assertions": {},
    }


def _highest_status(statuses: Sequence[str]) -> str:
    normalized = [status if status in EVIDENCE_LEDGER_REVIEW_STATUSES else STATUS_FAIL for status in statuses]
    for status in STATUS_PRECEDENCE:
        if status in normalized:
            return status
    return STATUS_NOT_SUPPLIED


def _safe_json_scalar(value: Any) -> Any:
    if isinstance(value, bool | int | float) or value is None:
        return value
    if isinstance(value, str):
        return _safe_text(value)
    return _safe_text(value)


def _safe_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _safe_text(value: Any) -> str:
    text = str(value or "")
    text = URL_RE.sub("[redacted-url]", text)
    text = ABSOLUTE_PATH_RE.sub(" [redacted-path]", text)
    text = FORBIDDEN_TEXT_RE.sub("[redacted-sensitive]", text)
    return text.strip()


def _safe_string_list(values: Any) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        iterable: Sequence[Any] = (values,)
    elif isinstance(values, Sequence):
        iterable = values
    else:
        try:
            iterable = tuple(values)
        except TypeError:
            iterable = (values,)
    seen: set[str] = set()
    result: list[str] = []
    for value in iterable:
        text = _safe_text(value)
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return sorted(result)


def _has_items(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value)
    if isinstance(value, Sequence):
        return bool(value)
    return bool(value)


def _safe_path_label(path: Path) -> str:
    name = Path(path).name or "[redacted-path]"
    return _safe_path_segment(name)


def _safe_path_segment(value: Any) -> str:
    text = str(value or "")
    text = SAFE_PATH_RE.sub("_", text).strip("_")
    return text or "value"
