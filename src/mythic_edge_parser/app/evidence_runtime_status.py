"""Optional summary-only runtime status exposure for evidence-ledger health."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

from . import diagnostics

EVIDENCE_LEDGER_HEALTH_OBJECT = "mythic_edge_player_log_evidence_ledger_runtime_health"
EVIDENCE_LEDGER_HEALTH_SCHEMA_VERSION = "player_log_evidence_ledger_runtime_health.v1"
EVIDENCE_LEDGER_HEALTH_STATUSES = (
    "unavailable",
    "pass",
    "degraded",
    "review",
    "diff",
    "fail",
)
EVIDENCE_LEDGER_HEALTH_SOURCE_KEYS = (
    "evidence_ledger_review",
    "runtime_field_evidence_report",
    "schema_drift_report",
    "invariant_execution_report",
    "schema_snapshot_comparison",
)

STATUS_UNAVAILABLE = "unavailable"
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
    STATUS_UNAVAILABLE,
)

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "evidence_ledger_review": {
        "object": "mythic_edge_player_log_evidence_ledger_validation_review",
        "schema_version": "player_log_evidence_ledger_validation_review.v1",
        "statuses": ("not_supplied", STATUS_PASS, STATUS_DEGRADED, STATUS_REVIEW, STATUS_DIFF, STATUS_FAIL),
        "summary_fields": (
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
        ),
    },
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

PROTECTED_SURFACE_ASSERTIONS = {
    "parser_behavior_changed": False,
    "parser_state_final_reconciliation_changed": False,
    "parser_event_classes_changed": False,
    "router_semantics_changed": False,
    "diagnostics_report_shape_changed": False,
    "validation_report_status_semantics_changed": False,
    "runtime_status_top_level_status_changed": False,
    "status_api_routes_changed": False,
    "health_endpoint_changed": False,
    "workbook_schema_changed": False,
    "webhook_payload_shape_changed": False,
    "apps_script_behavior_changed": False,
    "output_transport_changed": False,
    "action_log_row_shape_changed": False,
    "match_journal_behavior_changed": False,
    "overlay_behavior_changed": False,
    "sqlite_behavior_changed": False,
    "google_sheets_sync_behavior_changed": False,
    "analytics_or_ai_truth_changed": False,
    "ci_merge_deploy_policy_changed": False,
}

ABSOLUTE_PATH_RE = re.compile(
    r"(?:"
    r"/(?:Applications|Users|Volumes|etc|home|opt|private|tmp|var)"
    r"(?:/[^\r\n\"'<>\(\)\[\]\{\}\|]+)*"
    r"|[A-Za-z]:[\\/][^\r\n\"'<>\(\)\[\]\{\}\|]+"
    r"|\\\\[^\r\n\"'<>\(\)\[\]\{\}\|]+"
    r"|\[redacted-path\](?:[\\/][^\s\"'<>\(\)\[\]\{\}\|]+)+"
    r")",
    re.IGNORECASE,
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


def build_evidence_ledger_health_status(
    *,
    evidence_ledger_review: Mapping[str, Any] | None = None,
    runtime_field_evidence_report: Mapping[str, Any] | None = None,
    schema_drift_report: Mapping[str, Any] | None = None,
    invariant_execution_report: Mapping[str, Any] | None = None,
    schema_snapshot_comparison: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a summary-only evidence-ledger health object for runtime status."""

    raw_sources: dict[str, Any] = {
        "evidence_ledger_review": evidence_ledger_review,
        "runtime_field_evidence_report": runtime_field_evidence_report,
        "schema_drift_report": schema_drift_report,
        "invariant_execution_report": invariant_execution_report,
        "schema_snapshot_comparison": schema_snapshot_comparison,
    }
    if evidence_ledger_review is not None:
        raw_sources = {key: None for key in EVIDENCE_LEDGER_HEALTH_SOURCE_KEYS}
        raw_sources["evidence_ledger_review"] = evidence_ledger_review

    source_refs: dict[str, dict[str, Any]] = {}
    contexts: list[dict[str, Any]] = []
    for source_key in EVIDENCE_LEDGER_HEALTH_SOURCE_KEYS:
        source_ref, context = _source_ref(source_key, raw_sources[source_key])
        source_refs[source_key] = source_ref
        contexts.append(context)

    privacy = _merged_privacy(context["privacy"] for context in contexts)
    protected_violation_count = sum(context["protected_violation_count"] for context in contexts)
    affected = _merged_named_lists(context["affected"] for context in contexts)
    review_guidance = _merged_named_lists(context["review_guidance"] for context in contexts)
    drift_flags = _safe_string_list(flag for context in contexts for flag in context["drift_flags"])
    status_reasons = _safe_string_list(
        f"{source_key}:{reason}"
        for source_key, source_ref in source_refs.items()
        if source_ref["supplied"]
        for reason in source_ref["status_reasons"]
    )

    supplied_source_count = sum(1 for source_ref in source_refs.values() if source_ref["supplied"])
    limitations = [
        "Evidence ledger health is advisory runtime review metadata and does not affect runtime status.",
    ]
    if supplied_source_count == 0:
        limitations.append("No evidence-ledger health inputs were supplied.")
    if evidence_ledger_review is not None:
        limitations.append("Existing evidence_ledger_review input was preferred over individual source summaries.")

    status = _highest_status([source_ref["status"] for source_ref in source_refs.values()])
    if _has_privacy_findings(privacy):
        status = STATUS_FAIL
        status_reasons.append("privacy_findings")
    if protected_violation_count:
        status = STATUS_FAIL
        status_reasons.append("protected_surface_assertion_true")

    return {
        "object": EVIDENCE_LEDGER_HEALTH_OBJECT,
        "schema_version": EVIDENCE_LEDGER_HEALTH_SCHEMA_VERSION,
        "status": status,
        "review_required": status in {STATUS_DEGRADED, STATUS_REVIEW, STATUS_DIFF, STATUS_FAIL},
        "status_affects_runtime_status": False,
        "status_affects_parser": False,
        "status_affects_transport": False,
        "status_affects_workbook": False,
        "status_affects_overlay": False,
        "status_affects_ci_merge_deploy": False,
        "status_reasons": _safe_string_list(status_reasons),
        "source_refs": source_refs,
        "summary": _summary(
            source_refs,
            drift_flag_count=len(drift_flags),
            protected_violation_count=protected_violation_count,
            privacy_finding_count=_privacy_finding_count(privacy),
        ),
        "drift_flags": drift_flags,
        "affected": affected,
        "review_guidance": review_guidance,
        "privacy": privacy,
        "protected_surface_assertions": dict(PROTECTED_SURFACE_ASSERTIONS),
        "limitations": _safe_string_list(limitations),
    }


def update_evidence_ledger_health_status(
    *,
    evidence_ledger_review: Mapping[str, Any] | None = None,
    runtime_field_evidence_report: Mapping[str, Any] | None = None,
    schema_drift_report: Mapping[str, Any] | None = None,
    invariant_execution_report: Mapping[str, Any] | None = None,
    schema_snapshot_comparison: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build and write evidence-ledger health through the existing status writer."""

    health = build_evidence_ledger_health_status(
        evidence_ledger_review=evidence_ledger_review,
        runtime_field_evidence_report=runtime_field_evidence_report,
        schema_drift_report=schema_drift_report,
        invariant_execution_report=invariant_execution_report,
        schema_snapshot_comparison=schema_snapshot_comparison,
    )
    diagnostics.update_runtime_status(evidence_ledger_health=health)
    return health


def _source_ref(source_key: str, source: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    if source is None:
        return _empty_source_ref(), _empty_context()

    context = _empty_context()
    if not isinstance(source, Mapping):
        return (
            _supplied_source_ref(
                object_value="",
                schema_version="",
                status=STATUS_FAIL,
                review_required=True,
                status_reasons=["malformed_source_report"],
                summary={},
            ),
            context,
        )

    spec = SOURCE_SPECS[source_key]
    object_value = _safe_text(source.get("object"))
    schema_version = _safe_text(source.get("schema_version"))
    raw_status = _safe_text(source.get("status"))
    normalized_status = _normalized_source_status(source_key, raw_status)
    status_reasons: list[str] = []

    if object_value != spec["object"]:
        normalized_status = STATUS_FAIL
        status_reasons.append("unknown_source_object")
    if schema_version != spec["schema_version"]:
        normalized_status = STATUS_FAIL
        status_reasons.append("unknown_source_schema_version")
    if raw_status not in spec["statuses"] and not (source_key == "evidence_ledger_review" and raw_status == "ok"):
        normalized_status = STATUS_FAIL
        status_reasons.append("unknown_source_status")
    elif normalized_status not in {STATUS_PASS, STATUS_UNAVAILABLE}:
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

    status_reasons.extend(_safe_string_list(source.get("status_reasons")))
    context["affected"] = _source_named_lists(
        source.get("affected"),
        ("output_families", "entries", "evidence_signals"),
    )
    context["review_guidance"] = _source_named_lists(
        source.get("review_guidance"),
        ("recommended_review_modules", "recommended_tests", "review_notes"),
    )
    context["drift_flags"] = set(_safe_string_list(source.get("drift_flags")))
    return (
        _supplied_source_ref(
            object_value=object_value,
            schema_version=schema_version,
            status=normalized_status if normalized_status in EVIDENCE_LEDGER_HEALTH_STATUSES else STATUS_FAIL,
            review_required=bool(source.get("review_required"))
            or normalized_status in {STATUS_DEGRADED, STATUS_REVIEW, STATUS_DIFF, STATUS_FAIL},
            status_reasons=status_reasons,
            summary=_source_summary(source.get("summary"), spec["summary_fields"]),
        ),
        context,
    )


def _empty_source_ref() -> dict[str, Any]:
    return {
        "supplied": False,
        "object": "",
        "schema_version": "",
        "status": STATUS_UNAVAILABLE,
        "review_required": False,
        "status_reasons": [],
        "summary": {},
    }


def _supplied_source_ref(
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


def _empty_context() -> dict[str, Any]:
    return {
        "privacy": _empty_privacy(),
        "protected_violation_count": 0,
        "affected": {"output_families": set[str](), "entries": set[str](), "evidence_signals": set[str]()},
        "review_guidance": {
            "recommended_review_modules": set[str](),
            "recommended_tests": set[str](),
            "review_notes": set[str](),
        },
        "drift_flags": set[str](),
    }


def _normalized_source_status(source_key: str, status: str) -> str:
    if status in {STATUS_UNAVAILABLE, "not_supplied"}:
        return STATUS_UNAVAILABLE
    if source_key == "evidence_ledger_review" and status == "ok":
        return STATUS_PASS
    return status


def _summary(
    source_refs: Mapping[str, Mapping[str, Any]],
    *,
    drift_flag_count: int,
    protected_violation_count: int,
    privacy_finding_count: int,
) -> dict[str, int]:
    status_counts = {status: 0 for status in EVIDENCE_LEDGER_HEALTH_STATUSES}
    for source_ref in source_refs.values():
        status_counts[str(source_ref.get("status") or STATUS_UNAVAILABLE)] += 1

    review_summary = _source_summary_for(source_refs, "evidence_ledger_review")
    runtime_summary = _source_summary_for(source_refs, "runtime_field_evidence_report")
    drift_summary = _source_summary_for(source_refs, "schema_drift_report")
    invariant_summary = _source_summary_for(source_refs, "invariant_execution_report")
    snapshot_summary = _source_summary_for(source_refs, "schema_snapshot_comparison")
    return {
        "supplied_source_count": sum(1 for source_ref in source_refs.values() if source_ref.get("supplied")),
        "pass_count": status_counts[STATUS_PASS],
        "degraded_count": status_counts[STATUS_DEGRADED],
        "review_count": status_counts[STATUS_REVIEW],
        "diff_count": status_counts[STATUS_DIFF],
        "fail_count": status_counts[STATUS_FAIL],
        "unavailable_count": status_counts[STATUS_UNAVAILABLE],
        "runtime_field_evidence_attachment_count": _safe_int(
            review_summary.get("runtime_field_evidence_attachment_count", runtime_summary.get("attachment_count"))
        ),
        "runtime_field_evidence_review_required_count": _safe_int(
            review_summary.get(
                "runtime_field_evidence_review_required_count",
                runtime_summary.get("review_required_count"),
            )
        ),
        "runtime_field_evidence_missing_mapping_count": _safe_int(
            review_summary.get(
                "runtime_field_evidence_missing_mapping_count",
                runtime_summary.get("missing_mapping_count"),
            )
        ),
        "schema_drift_changed_entry_count": _safe_int(
            review_summary.get(
                "schema_drift_changed_entry_count",
                _safe_int(drift_summary.get("entry_changes")) + _safe_int(snapshot_summary.get("entry_changes")),
            )
        ),
        "schema_drift_changed_signal_count": _safe_int(
            review_summary.get(
                "schema_drift_changed_signal_count",
                _safe_int(drift_summary.get("evidence_signal_changes"))
                + _safe_int(snapshot_summary.get("evidence_signal_changes")),
            )
        ),
        "invariant_failed_count": _safe_int(
            review_summary.get("invariant_failed_count", invariant_summary.get("failed_count"))
        ),
        "invariant_degraded_count": _safe_int(
            review_summary.get("invariant_degraded_count", invariant_summary.get("degraded_count"))
        ),
        "invariant_not_checked_count": _safe_int(
            review_summary.get("invariant_not_checked_count", invariant_summary.get("not_checked_count"))
        ),
        "drift_flag_count": drift_flag_count or _safe_int(review_summary.get("drift_flag_count")),
        "protected_surface_violation_count": protected_violation_count
        or _safe_int(review_summary.get("protected_surface_violation_count")),
        "privacy_finding_count": privacy_finding_count,
    }


def _source_summary_for(source_refs: Mapping[str, Mapping[str, Any]], source_key: str) -> Mapping[str, Any]:
    source_ref = source_refs.get(source_key, {})
    summary = source_ref.get("summary") if isinstance(source_ref, Mapping) else {}
    return summary if isinstance(summary, Mapping) else {}


def _source_summary(summary: Any, allowed_fields: Sequence[str]) -> dict[str, Any]:
    if not isinstance(summary, Mapping):
        return {}
    return {
        field: _safe_json_scalar(summary.get(field))
        for field in allowed_fields
        if field in summary
    }


def _source_named_lists(raw: Any, keys: Sequence[str]) -> dict[str, set[str]]:
    source = raw if isinstance(raw, Mapping) else {}
    return {key: set(_safe_string_list(source.get(key))) for key in keys}


def _merged_named_lists(sources: Sequence[Mapping[str, set[str]]]) -> dict[str, list[str]]:
    keys: set[str] = set()
    for source in sources:
        keys.update(source)
    return {key: _safe_string_list(value for source in sources for value in source.get(key, set())) for key in keys}


def _source_privacy_findings(source: Mapping[str, Any], source_key: str) -> dict[str, Any]:
    findings = _privacy_findings(source, source_key)
    privacy = source.get("privacy")
    if isinstance(privacy, Mapping):
        for key in ("forbidden_content_findings", "local_absolute_paths_found"):
            if _has_items(privacy.get(key)):
                findings[key].append(f"{source_key}.privacy.{key}")
        for key in _empty_privacy():
            if key in {"forbidden_content_findings", "local_absolute_paths_found"}:
                continue
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
        if "script.google.com" in payload or "hooks." in payload:
            findings["runtime_artifacts_included"] = True
        if re.search(r"(?i)\b(api[_-]?key|secret|token)\s*[:=]", payload):
            findings["secrets_or_credentials_included"] = True
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
        "runtime_status_contents_included": False,
        "failed_posts_included": False,
        "workbook_exports_included": False,
        "secrets_or_credentials_included": False,
        "full_field_evidence_attachments_included": False,
        "full_schema_snapshots_included": False,
        "ai_or_model_provider_output_included": False,
    }


def _merged_privacy(sources: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    privacy = _empty_privacy()
    for source in sources:
        for key in ("forbidden_content_findings", "local_absolute_paths_found"):
            privacy[key] = _safe_string_list([*privacy[key], *list(source.get(key, []))])
        for key in privacy:
            if key in {"forbidden_content_findings", "local_absolute_paths_found"}:
                continue
            privacy[key] = bool(privacy[key]) or bool(source.get(key))
    return privacy


def _sorted_privacy(privacy: Mapping[str, Any]) -> dict[str, Any]:
    clean = _empty_privacy()
    for key in ("forbidden_content_findings", "local_absolute_paths_found"):
        clean[key] = _safe_string_list(privacy.get(key))
    for key in clean:
        if key in {"forbidden_content_findings", "local_absolute_paths_found"}:
            continue
        clean[key] = bool(privacy.get(key))
    return clean


def _has_privacy_findings(privacy: Mapping[str, Any]) -> bool:
    if privacy.get("forbidden_content_findings") or privacy.get("local_absolute_paths_found"):
        return True
    return any(
        bool(privacy.get(key))
        for key in privacy
        if key not in {"forbidden_content_findings", "local_absolute_paths_found"}
    )


def _privacy_finding_count(privacy: Mapping[str, Any]) -> int:
    count = len(privacy.get("forbidden_content_findings", [])) + len(privacy.get("local_absolute_paths_found", []))
    count += sum(
        1
        for key, value in privacy.items()
        if key not in {"forbidden_content_findings", "local_absolute_paths_found"} and value is True
    )
    return count


def _protected_violations(source: Mapping[str, Any], source_key: str) -> list[str]:
    assertions = source.get("protected_surface_assertions")
    if not isinstance(assertions, Mapping):
        return []
    return _safe_string_list(
        f"{source_key}.protected_surface_assertions.{key}"
        for key, value in assertions.items()
        if value is not False
    )


def _highest_status(statuses: Sequence[str]) -> str:
    normalized = [status if status in EVIDENCE_LEDGER_HEALTH_STATUSES else STATUS_FAIL for status in statuses]
    for status in STATUS_PRECEDENCE:
        if status in normalized:
            return status
    return STATUS_UNAVAILABLE


def _safe_json_scalar(value: Any) -> Any:
    if isinstance(value, bool | int | float) or value is None:
        return value
    return _safe_text(value)


def _safe_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _safe_text(value: Any) -> str:
    text = str(value or "")
    text = URL_RE.sub("[redacted-url]", text)
    text = ABSOLUTE_PATH_RE.sub("[redacted-path]", text)
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


def _safe_path_segment(value: Any) -> str:
    text = str(value or "")
    text = SAFE_PATH_RE.sub("_", text).strip("_")
    return text or "value"
