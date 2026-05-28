"""Local review-only runtime field-evidence report builder."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from mythic_edge_parser.app import evidence_invariant_execution, evidence_ledger

RUNTIME_FIELD_EVIDENCE_REPORT_OBJECT = "mythic_edge_player_log_runtime_field_evidence_report"
RUNTIME_FIELD_EVIDENCE_REPORT_VERSION = "player_log_runtime_field_evidence_report.v1"
RUNTIME_FIELD_EVIDENCE_ATTACHMENT_OBJECT = "mythic_edge_player_log_runtime_field_evidence_attachment"
RUNTIME_FIELD_EVIDENCE_REPORT_STATUSES = ("pass", "review", "fail")
RUNTIME_FIELD_EVIDENCE_ATTACHMENT_SURFACES = (
    "local_review_sidecar",
    "synthetic_test_reference",
)

SOURCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/181"
PARENT_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/11"

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
SAFE_ID_RE = re.compile(r"[^A-Za-z0-9_.-]+")

PROTECTED_SURFACE_ASSERTIONS = {
    "parser_behavior_changed": False,
    "parser_state_final_reconciliation_changed": False,
    "parser_event_classes_changed": False,
    "workbook_schema_changed": False,
    "webhook_payload_shape_changed": False,
    "apps_script_behavior_changed": False,
    "output_transport_changed": False,
    "action_log_row_shape_changed": False,
    "runtime_status_schema_changed": False,
    "diagnostics_report_shape_changed": False,
    "golden_replay_behavior_changed": False,
    "feature_equity_behavior_changed": False,
    "match_journal_behavior_changed": False,
    "overlay_behavior_changed": False,
    "sqlite_behavior_changed": False,
    "google_sheets_sync_behavior_changed": False,
    "analytics_or_ai_truth_changed": False,
}


def build_runtime_field_evidence_report(
    field_refs: Sequence[Mapping[str, Any]],
    *,
    ledger: Mapping[str, Any] | None = None,
    invariant_execution_report: Mapping[str, Any] | None = None,
    require_invariant_execution_report: bool = False,
) -> dict[str, Any]:
    """Build deterministic review-only field evidence for sanitized field references."""

    source_ledger: Any = evidence_ledger.build_player_log_evidence_ledger() if ledger is None else ledger
    ledger_is_mapping = isinstance(source_ledger, Mapping)
    ledger_payload: Mapping[str, Any] = source_ledger if ledger_is_mapping else {}
    invariant_supplied = invariant_execution_report is not None
    invariant_is_mapping = isinstance(invariant_execution_report, Mapping)
    invariant_payload: Mapping[str, Any] = invariant_execution_report if invariant_is_mapping else {}

    field_refs_valid, field_ref_errors = _validate_field_refs_container(field_refs)
    field_ref_items: Sequence[Any] = field_refs if field_refs_valid else ()
    privacy = _combined_privacy_findings(
        (
            ("ledger", source_ledger),
            ("field_refs", field_ref_items),
            ("invariant_execution_report", invariant_execution_report),
        ),
    )
    field_value_paths = _field_value_paths(field_ref_items)
    privacy["forbidden_content_findings"].extend(field_value_paths)
    privacy["field_values_included"] = bool(field_value_paths)
    privacy_blocked = _has_privacy_findings(privacy)

    ledger_validation_errors = (
        evidence_ledger.validate_player_log_evidence_ledger(ledger_payload)
        if ledger_is_mapping
        else ["ledger:not_mapping"]
    )
    indexes = _entry_indexes(ledger_payload) if not ledger_validation_errors else _empty_indexes()

    attachments: list[dict[str, Any]] = []
    missing_mappings: list[dict[str, Any]] = []
    ambiguous_mappings: list[dict[str, Any]] = []
    validation_errors: list[str] = list(field_ref_errors)

    for index, raw_ref in enumerate(field_ref_items):
        if not isinstance(raw_ref, Mapping):
            validation_errors.append(f"field_refs[{index}]:not_mapping")
            continue
        ref_errors = _validate_field_ref(raw_ref, index)
        validation_errors.extend(ref_errors)
        if ref_errors:
            continue

        resolution = _resolve_entry(raw_ref, indexes)
        if resolution["status"] == "missing":
            missing_mappings.append(_mapping_record(raw_ref, index, reason=resolution["reason"]))
            continue
        if resolution["status"] == "ambiguous":
            ambiguous_mappings.append(
                _mapping_record(
                    raw_ref,
                    index,
                    reason=resolution["reason"],
                    candidate_entry_ids=resolution["candidate_entry_ids"],
                ),
            )
            continue

        entry = resolution["entry"]
        attachment = _build_attachment(
            raw_ref,
            entry,
            index=index,
            mapping_method=resolution["method"],
            privacy_blocked=privacy_blocked,
        )
        validation_errors.extend(
            f"attachments[{len(attachments)}].field_evidence:{error}"
            for error in attachment["validation_errors"]
        )
        attachments.append(attachment)

    invariant_dependency = _invariant_dependency(
        invariant_payload,
        supplied=invariant_supplied,
        is_mapping=invariant_is_mapping,
        required=require_invariant_execution_report,
    )
    affected = _affected(attachments, missing_mappings, ambiguous_mappings)
    review_guidance = _review_guidance(
        attachments,
        missing_mappings,
        ambiguous_mappings,
        invariant_dependency=invariant_dependency,
        ledger_validation_errors=ledger_validation_errors,
        validation_errors=validation_errors,
    )
    drift_flags = _report_drift_flags(attachments, invariant_dependency, privacy_blocked)
    protected_violation_count = sum(1 for value in PROTECTED_SURFACE_ASSERTIONS.values() if value is not False)
    status = _report_status(
        ledger_validation_errors=ledger_validation_errors,
        validation_errors=validation_errors,
        attachments=attachments,
        missing_mappings=missing_mappings,
        ambiguous_mappings=ambiguous_mappings,
        invariant_dependency=invariant_dependency,
        privacy=privacy,
        protected_violation_count=protected_violation_count,
    )
    status_reasons = _status_reasons(
        status,
        ledger_validation_errors=ledger_validation_errors,
        validation_errors=validation_errors,
        attachments=attachments,
        missing_mappings=missing_mappings,
        ambiguous_mappings=ambiguous_mappings,
        invariant_dependency=invariant_dependency,
        privacy=privacy,
        protected_violation_count=protected_violation_count,
    )

    report = {
        "object": RUNTIME_FIELD_EVIDENCE_REPORT_OBJECT,
        "schema_version": RUNTIME_FIELD_EVIDENCE_REPORT_VERSION,
        "source_issue": SOURCE_ISSUE,
        "parent_issue": PARENT_ISSUE,
        "status": status,
        "review_required": status != "pass",
        "status_reasons": status_reasons,
        "input_refs": {
            "ledger": _ledger_input_ref(ledger_payload),
            "invariant_execution_report": {
                "supplied": invariant_supplied,
                "required": require_invariant_execution_report,
                "status": invariant_dependency["status"],
                "schema_version": invariant_dependency["schema_version"],
            },
        },
        "summary": _summary(
            field_ref_count=len(field_ref_items) if field_refs_valid else 0,
            attachments=attachments,
            missing_mappings=missing_mappings,
            ambiguous_mappings=ambiguous_mappings,
            validation_errors=validation_errors,
            drift_flags=drift_flags,
            protected_violation_count=protected_violation_count,
        ),
        "attachments": attachments,
        "missing_mappings": missing_mappings,
        "ambiguous_mappings": ambiguous_mappings,
        "validation_errors": _safe_string_list([*ledger_validation_errors, *validation_errors]),
        "affected": affected,
        "review_guidance": review_guidance,
        "drift_flags": drift_flags,
        "privacy": {
            "forbidden_content_findings": _dedupe(privacy["forbidden_content_findings"]),
            "local_absolute_paths_found": _dedupe(privacy["local_absolute_paths_found"]),
            "raw_private_logs_included": False,
            "raw_payload_values_included": False,
            "runtime_artifacts_included": False,
            "generated_data_included": False,
            "field_values_included": bool(privacy.get("field_values_included")),
        },
        "protected_surface_assertions": dict(PROTECTED_SURFACE_ASSERTIONS),
        "limitations": _limitations(
            field_refs_valid=field_refs_valid,
            ledger_validation_errors=ledger_validation_errors,
            invariant_dependency=invariant_dependency,
        ),
    }

    report = _redact_sensitive_report_values(report)
    report_privacy = _privacy_findings(report, "report")
    if _has_privacy_findings(report_privacy):
        report["status"] = "fail"
        report["review_required"] = True
        report["status_reasons"] = _dedupe([*report["status_reasons"], "report_privacy_findings"])
        report["privacy"]["forbidden_content_findings"] = _dedupe(
            [*report["privacy"]["forbidden_content_findings"], *report_privacy["forbidden_content_findings"]],
        )
        report["privacy"]["local_absolute_paths_found"] = _dedupe(
            [*report["privacy"]["local_absolute_paths_found"], *report_privacy["local_absolute_paths_found"]],
        )
        report["drift_flags"] = _dedupe_allowed_flags([*report["drift_flags"], "sensitive_evidence_redacted"])
        report["summary"] = _summary(
            field_ref_count=len(field_ref_items) if field_refs_valid else 0,
            attachments=attachments,
            missing_mappings=missing_mappings,
            ambiguous_mappings=ambiguous_mappings,
            validation_errors=validation_errors,
            drift_flags=report["drift_flags"],
            protected_violation_count=protected_violation_count,
        )
    return report


def build_current_runtime_field_evidence_report(
    field_refs: Sequence[Mapping[str, Any]],
    *,
    require_invariant_execution_report: bool = False,
) -> dict[str, Any]:
    """Build a report against the current evidence ledger."""

    invariant_report = (
        evidence_invariant_execution.build_current_evidence_invariant_execution_report()
        if require_invariant_execution_report
        else None
    )
    return build_runtime_field_evidence_report(
        field_refs,
        invariant_execution_report=invariant_report,
        require_invariant_execution_report=require_invariant_execution_report,
    )


def write_runtime_field_evidence_report(path: Path, report: Mapping[str, Any]) -> None:
    """Write a runtime field-evidence report to an explicit path after privacy scanning."""

    findings = _privacy_findings(report, "report")
    combined = findings["forbidden_content_findings"] + findings["local_absolute_paths_found"]
    if combined:
        raise ValueError(f"forbidden runtime field-evidence report content: {', '.join(combined)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_encode_report(report), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a local runtime field-evidence sidecar report.")
    parser.add_argument("--check", action="store_true", help="Build a report and print JSON.")
    parser.add_argument("--field-refs", type=Path, help="Explicit sanitized field-reference JSON payload.")
    parser.add_argument("--ledger", type=Path, help="Explicit synthetic JSON ledger payload.")
    parser.add_argument("--invariant-report", type=Path, help="Explicit invariant execution report JSON payload.")
    parser.add_argument(
        "--require-invariant-report",
        action="store_true",
        help="Fail when invariant execution review evidence is missing or failed.",
    )
    parser.add_argument("--out", type=Path, help="Write JSON report to an explicit path.")
    parser.add_argument("--markdown-out", type=Path, help="Write a sanitized Markdown summary to an explicit path.")
    args = parser.parse_args(argv)

    field_refs, field_ref_limitations = _load_field_refs(args.field_refs) if args.field_refs else ([], [])
    ledger_payload, ledger_limitations = _load_json_mapping(args.ledger, "ledger") if args.ledger else (None, [])
    invariant_report, invariant_limitations = (
        _load_json_mapping(args.invariant_report, "invariant execution report")
        if args.invariant_report
        else (None, [])
    )
    report = build_runtime_field_evidence_report(
        field_refs,
        ledger=ledger_payload,
        invariant_execution_report=invariant_report,
        require_invariant_execution_report=args.require_invariant_report,
    )
    _add_cli_limitations(report, [*field_ref_limitations, *ledger_limitations, *invariant_limitations])

    if args.out is not None:
        try:
            write_runtime_field_evidence_report(args.out, report)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
    if args.markdown_out is not None:
        try:
            _write_markdown_report(args.markdown_out, report)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1

    print(_encode_report(report), end="")
    return 1 if report["status"] == "fail" else 0


def _validate_field_refs_container(field_refs: Any) -> tuple[bool, list[str]]:
    if isinstance(field_refs, Mapping | str | bytes) or not isinstance(field_refs, Sequence):
        return False, ["field_refs:not_sequence"]
    return True, []


def _empty_indexes() -> dict[str, Any]:
    return {
        "by_entry_id": {},
        "by_family_field": defaultdict(list),
        "by_family_display": defaultdict(list),
    }


def _entry_indexes(ledger: Mapping[str, Any]) -> dict[str, Any]:
    indexes = _empty_indexes()
    entries = ledger.get("entries")
    if not isinstance(entries, list):
        return indexes
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        entry_id = _safe_text(entry.get("entry_id"))
        output_family = _safe_text(entry.get("output_family"))
        output_field = _safe_text(entry.get("output_field"))
        display_name = _safe_text(entry.get("display_name"))
        if entry_id:
            indexes["by_entry_id"][entry_id] = entry
        if output_family and output_field:
            indexes["by_family_field"][(output_family, output_field)].append(entry)
        if output_family and display_name:
            indexes["by_family_display"][(output_family, display_name)].append(entry)
    return indexes


def _resolve_entry(field_ref: Mapping[str, Any], indexes: Mapping[str, Any]) -> dict[str, Any]:
    entry_id = _safe_text(field_ref.get("entry_id"))
    output_family = _safe_text(field_ref.get("output_family"))
    output_field = _safe_text(field_ref.get("output_field"))
    display_name = _safe_text(field_ref.get("display_name"))
    if entry_id:
        entry = indexes["by_entry_id"].get(entry_id)
        if isinstance(entry, Mapping):
            return {"status": "mapped", "entry": entry, "method": "entry_id"}
        return {"status": "missing", "reason": "entry_id_not_found"}

    candidates = indexes["by_family_field"].get((output_family, output_field), [])
    if len(candidates) == 1:
        return {"status": "mapped", "entry": candidates[0], "method": "output_family_output_field"}
    if len(candidates) > 1:
        return {
            "status": "ambiguous",
            "reason": "output_family_output_field_ambiguous",
            "candidate_entry_ids": _candidate_ids(candidates),
        }

    display_candidates = indexes["by_family_display"].get((output_family, display_name), []) if display_name else []
    if len(display_candidates) == 1:
        return {"status": "mapped", "entry": display_candidates[0], "method": "output_family_display_name"}
    if len(display_candidates) > 1:
        return {
            "status": "ambiguous",
            "reason": "output_family_display_name_ambiguous",
            "candidate_entry_ids": _candidate_ids(display_candidates),
        }
    return {"status": "missing", "reason": "no_exact_mapping"}


def _validate_field_ref(field_ref: Mapping[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    surface = field_ref.get("surface")
    if surface not in RUNTIME_FIELD_EVIDENCE_ATTACHMENT_SURFACES:
        errors.append(f"field_refs[{index}]:surface:unknown")
    entity_ref = field_ref.get("entity_ref")
    if not isinstance(entity_ref, Mapping):
        errors.append(f"field_refs[{index}]:entity_ref:not_mapping")
    source_payload_paths = field_ref.get("source_payload_paths", [])
    if not isinstance(source_payload_paths, list) or any(not isinstance(path, str) for path in source_payload_paths):
        errors.append(f"field_refs[{index}]:source_payload_paths:not_string_list")
    if "value" in field_ref:
        errors.append(f"field_refs[{index}]:value_key_forbidden")
    return errors


def _build_attachment(
    field_ref: Mapping[str, Any],
    entry: Mapping[str, Any],
    *,
    index: int,
    mapping_method: str,
    privacy_blocked: bool,
) -> dict[str, Any]:
    field_evidence = _field_evidence(field_ref, entry, privacy_blocked=privacy_blocked)
    validation_errors = evidence_ledger.validate_field_evidence(field_evidence)
    review_notes = _attachment_review_notes(field_evidence, validation_errors, mapping_method)
    entity_ref = _entity_ref(field_ref.get("entity_ref"))
    return {
        "object": RUNTIME_FIELD_EVIDENCE_ATTACHMENT_OBJECT,
        "attachment_id": _attachment_id(entry, entity_ref, index),
        "surface": _safe_text(field_ref.get("surface")),
        "entity_ref": entity_ref,
        "entry_id": _safe_text(entry.get("entry_id")),
        "output_family": _safe_text(entry.get("output_family")),
        "output_field": _safe_text(entry.get("output_field")),
        "display_name": _safe_text(entry.get("display_name")),
        "parser_owner": _safe_text(entry.get("parser_owner"), drop_sensitive=privacy_blocked),
        "model_surface": _safe_text(entry.get("model_surface"), drop_sensitive=privacy_blocked),
        "field_evidence": field_evidence,
        "validation_errors": validation_errors,
        "review_notes": review_notes,
    }


def _field_evidence(
    field_ref: Mapping[str, Any],
    entry: Mapping[str, Any],
    *,
    privacy_blocked: bool,
) -> dict[str, Any]:
    drift_flags = field_ref.get("drift_flags", [])
    if not isinstance(drift_flags, list):
        drift_flags = ["changed_signal_type"]
    source_payload_paths = field_ref.get("source_payload_paths", [])
    if not isinstance(source_payload_paths, list):
        source_payload_paths = []
    payload = {
        "object": evidence_ledger.FIELD_EVIDENCE_OBJECT,
        "schema_version": evidence_ledger.FIELD_EVIDENCE_SCHEMA_VERSION,
        "ledger_version": evidence_ledger.LEDGER_VERSION,
        "entry_id": _safe_text(entry.get("entry_id")),
        "output_family": _safe_text(entry.get("output_family")),
        "output_field": _safe_text(entry.get("output_field")),
        "value_source": _safe_text(field_ref.get("value_source"), drop_sensitive=True) or "unknown",
        "confidence": _safe_text(field_ref.get("confidence"), drop_sensitive=True) or "unknown",
        "finality": _safe_text(field_ref.get("finality"), drop_sensitive=True) or "provisional",
        "source_event_kind": _safe_text(field_ref.get("source_event_kind"), drop_sensitive=True),
        "source_event_type": _safe_text(field_ref.get("source_event_type"), drop_sensitive=True),
        "source_payload_paths": _safe_string_list(source_payload_paths, drop_sensitive=privacy_blocked),
        "source_event_timestamp": _safe_text(field_ref.get("source_event_timestamp"), drop_sensitive=privacy_blocked),
        "drift_flags": _safe_string_list(drift_flags, drop_sensitive=privacy_blocked),
        "invariant_status": _safe_text(field_ref.get("invariant_status"), drop_sensitive=True) or "not_checked",
        "degraded_reason": _safe_text(field_ref.get("degraded_reason"), drop_sensitive=privacy_blocked),
        "review_required": False,
    }
    payload["review_required"] = _field_evidence_review_required(payload)
    return payload


def _field_evidence_review_required(payload: Mapping[str, Any]) -> bool:
    return bool(
        payload.get("invariant_status") == "failed"
        or payload.get("value_source") == "conflict"
        or (payload.get("confidence") == "low" and payload.get("finality") in {"final", "reconciled"})
    )


def _attachment_review_notes(
    field_evidence: Mapping[str, Any],
    validation_errors: Sequence[str],
    mapping_method: str,
) -> list[str]:
    notes: list[str] = [f"mapped_by:{mapping_method}"]
    if validation_errors:
        notes.append("field_evidence_validation_failed")
    if field_evidence.get("review_required") is True:
        notes.append("field_evidence_requires_review")
    if field_evidence.get("invariant_status") == "degraded":
        notes.append("invariant_dependency_degraded")
    return notes


def _mapping_record(
    field_ref: Mapping[str, Any],
    index: int,
    *,
    reason: str,
    candidate_entry_ids: Sequence[str] = (),
) -> dict[str, Any]:
    return {
        "field_ref_index": index,
        "surface": _safe_text(field_ref.get("surface"), drop_sensitive=True),
        "entry_id": _safe_text(field_ref.get("entry_id"), drop_sensitive=True),
        "output_family": _safe_text(field_ref.get("output_family"), drop_sensitive=True),
        "output_field": _safe_text(field_ref.get("output_field"), drop_sensitive=True),
        "display_name": _safe_text(field_ref.get("display_name"), drop_sensitive=True),
        "entity_ref": _entity_ref(field_ref.get("entity_ref")),
        "reason": _safe_text(reason),
        "candidate_entry_ids": _safe_string_list(candidate_entry_ids),
    }


def _invariant_dependency(
    report: Mapping[str, Any],
    *,
    supplied: bool,
    is_mapping: bool,
    required: bool,
) -> dict[str, Any]:
    if not supplied:
        return {
            "supplied": False,
            "required": required,
            "status": "missing",
            "schema_version": "",
            "outcome": "fail" if required else "pass",
            "reason": "required invariant execution report missing" if required else "",
        }
    if not is_mapping:
        return {
            "supplied": True,
            "required": required,
            "status": "malformed",
            "schema_version": "",
            "outcome": "fail" if required else "review",
            "reason": "invariant execution report is not a mapping",
        }
    status = _safe_text(report.get("status"))
    schema_version = _safe_text(report.get("schema_version"))
    if status == "pass":
        outcome = "pass"
    elif status == "review":
        outcome = "review"
    else:
        outcome = "fail" if required or status == "fail" else "review"
    return {
        "supplied": True,
        "required": required,
        "status": status or "unknown",
        "schema_version": schema_version,
        "outcome": outcome,
        "reason": "" if outcome == "pass" else f"invariant execution report status is {status or 'unknown'}",
    }


def _report_status(
    *,
    ledger_validation_errors: Sequence[str],
    validation_errors: Sequence[str],
    attachments: Sequence[Mapping[str, Any]],
    missing_mappings: Sequence[Mapping[str, Any]],
    ambiguous_mappings: Sequence[Mapping[str, Any]],
    invariant_dependency: Mapping[str, Any],
    privacy: Mapping[str, Any],
    protected_violation_count: int,
) -> str:
    hard_fail = bool(
        ledger_validation_errors
        or validation_errors
        or _has_privacy_findings(privacy)
        or protected_violation_count
        or invariant_dependency.get("outcome") == "fail"
        or any(item.get("field_evidence", {}).get("invariant_status") == "failed" for item in attachments)
    )
    if hard_fail:
        return "fail"
    needs_review = bool(
        missing_mappings
        or ambiguous_mappings
        or invariant_dependency.get("outcome") == "review"
        or any(item.get("field_evidence", {}).get("review_required") is True for item in attachments)
        or any(item.get("field_evidence", {}).get("invariant_status") == "degraded" for item in attachments)
    )
    return "review" if needs_review else "pass"


def _status_reasons(
    status: str,
    *,
    ledger_validation_errors: Sequence[str],
    validation_errors: Sequence[str],
    attachments: Sequence[Mapping[str, Any]],
    missing_mappings: Sequence[Mapping[str, Any]],
    ambiguous_mappings: Sequence[Mapping[str, Any]],
    invariant_dependency: Mapping[str, Any],
    privacy: Mapping[str, Any],
    protected_violation_count: int,
) -> list[str]:
    reasons: list[str] = []
    if ledger_validation_errors:
        reasons.append("ledger_validation_failed")
    if validation_errors:
        reasons.append("field_ref_or_field_evidence_validation_failed")
    if _has_privacy_findings(privacy):
        reasons.append("privacy_findings")
    if protected_violation_count:
        reasons.append("protected_surface_assertion_true")
    if missing_mappings:
        reasons.append("missing_mappings")
    if ambiguous_mappings:
        reasons.append("ambiguous_mappings")
    if invariant_dependency.get("outcome") == "fail":
        reasons.append("invariant_execution_report_failed_or_missing")
    elif invariant_dependency.get("outcome") == "review":
        reasons.append("invariant_execution_report_requires_review")
    if any(item.get("field_evidence", {}).get("invariant_status") == "failed" for item in attachments):
        reasons.append("field_invariant_failed")
    if any(item.get("field_evidence", {}).get("review_required") is True for item in attachments):
        reasons.append("field_evidence_requires_review")
    if any(item.get("field_evidence", {}).get("invariant_status") == "degraded" for item in attachments):
        reasons.append("field_invariant_degraded")
    if status == "pass":
        return []
    return _dedupe(reasons)


def _summary(
    *,
    field_ref_count: int,
    attachments: Sequence[Mapping[str, Any]],
    missing_mappings: Sequence[Mapping[str, Any]],
    ambiguous_mappings: Sequence[Mapping[str, Any]],
    validation_errors: Sequence[str],
    drift_flags: Sequence[str],
    protected_violation_count: int,
) -> dict[str, int]:
    field_evidence_records = [item.get("field_evidence", {}) for item in attachments]
    valid_field_evidence_count = sum(1 for item in attachments if not item.get("validation_errors"))
    return {
        "field_ref_count": field_ref_count,
        "attachment_count": len(attachments),
        "valid_field_evidence_count": valid_field_evidence_count,
        "missing_mapping_count": len(missing_mappings),
        "ambiguous_mapping_count": len(ambiguous_mappings),
        "failed_validation_count": len(validation_errors),
        "review_required_count": sum(1 for item in field_evidence_records if item.get("review_required") is True),
        "conflict_count": sum(1 for item in field_evidence_records if item.get("value_source") == "conflict"),
        "degraded_count": sum(1 for item in field_evidence_records if item.get("invariant_status") == "degraded"),
        "not_checked_count": sum(1 for item in field_evidence_records if item.get("invariant_status") == "not_checked"),
        "drift_flag_count": len(_dedupe_allowed_flags(drift_flags)),
        "protected_surface_violation_count": protected_violation_count,
    }


def _affected(
    attachments: Sequence[Mapping[str, Any]],
    missing_mappings: Sequence[Mapping[str, Any]],
    ambiguous_mappings: Sequence[Mapping[str, Any]],
) -> dict[str, list[str]]:
    families: list[str] = []
    entries: list[str] = []
    for item in [*attachments, *missing_mappings, *ambiguous_mappings]:
        family = _safe_text(item.get("output_family"))
        entry_id = _safe_text(item.get("entry_id"))
        if family:
            families.append(family)
        if entry_id:
            entries.append(entry_id)
    return {
        "output_families": sorted(_dedupe(families)),
        "entries": sorted(_dedupe(entries)),
    }


def _review_guidance(
    attachments: Sequence[Mapping[str, Any]],
    missing_mappings: Sequence[Mapping[str, Any]],
    ambiguous_mappings: Sequence[Mapping[str, Any]],
    *,
    invariant_dependency: Mapping[str, Any],
    ledger_validation_errors: Sequence[str],
    validation_errors: Sequence[str],
) -> dict[str, list[str]]:
    modules: list[str] = []
    tests: list[str] = ["tests/test_runtime_field_evidence.py"]
    notes: list[str] = []
    for attachment in attachments:
        entry = _safe_text(attachment.get("entry_id"))
        if entry:
            notes.append(f"review mapped field evidence for {entry}")
        field_evidence = attachment.get("field_evidence", {})
        if isinstance(field_evidence, Mapping) and field_evidence.get("review_required") is True:
            notes.append(f"{entry} requires field-evidence review")
    if missing_mappings:
        modules.append("src/mythic_edge_parser/app/evidence_ledger.py")
        notes.append(f"{len(missing_mappings)} field reference(s) did not map to a ledger entry")
    if ambiguous_mappings:
        modules.append("src/mythic_edge_parser/app/evidence_ledger.py")
        notes.append(f"{len(ambiguous_mappings)} field reference(s) had ambiguous ledger mappings")
    if ledger_validation_errors:
        modules.append("src/mythic_edge_parser/app/evidence_ledger.py")
        tests.append("tests/test_evidence_ledger.py")
        notes.append("ledger validation failed before runtime field evidence could be trusted")
    if validation_errors:
        notes.append("field reference or field-evidence validation failed")
    if invariant_dependency.get("outcome") in {"review", "fail"}:
        modules.append("src/mythic_edge_parser/app/evidence_invariant_execution.py")
        tests.append("tests/test_evidence_invariant_execution.py")
        reason = _safe_text(invariant_dependency.get("reason"))
        if reason:
            notes.append(reason)
    return {
        "recommended_review_modules": sorted(_dedupe(modules)),
        "recommended_tests": sorted(_dedupe(tests)),
        "review_notes": _dedupe(notes),
    }


def _report_drift_flags(
    attachments: Sequence[Mapping[str, Any]],
    invariant_dependency: Mapping[str, Any],
    privacy_blocked: bool,
) -> list[str]:
    flags: list[str] = []
    for attachment in attachments:
        field_evidence = attachment.get("field_evidence", {})
        if isinstance(field_evidence, Mapping):
            flags.extend(_safe_string_list(field_evidence.get("drift_flags", [])))
            if field_evidence.get("invariant_status") == "failed":
                flags.append("invariant_failed")
            if field_evidence.get("value_source") == "conflict":
                flags.append("conflicting_evidence")
    if invariant_dependency.get("outcome") == "fail":
        flags.append("invariant_failed")
    if invariant_dependency.get("status") == "missing" and invariant_dependency.get("required"):
        flags.append("schema_snapshot_missing")
    if privacy_blocked:
        flags.append("sensitive_evidence_redacted")
    return _dedupe_allowed_flags(flags)


def _limitations(
    *,
    field_refs_valid: bool,
    ledger_validation_errors: Sequence[str],
    invariant_dependency: Mapping[str, Any],
) -> list[str]:
    limitations: list[str] = [
        "Runtime field evidence is a local review sidecar only and does not change parser output values.",
        "No field values are serialized in V1 runtime field-evidence reports.",
    ]
    if not field_refs_valid:
        limitations.append("Field references input was malformed.")
    if ledger_validation_errors:
        limitations.append(f"Ledger validation returned {len(ledger_validation_errors)} error(s).")
    if invariant_dependency.get("status") == "missing":
        limitations.append("Invariant execution report was not supplied.")
    return limitations


def _ledger_input_ref(ledger: Mapping[str, Any]) -> dict[str, str]:
    return {
        "object": _safe_text(ledger.get("object")),
        "schema_version": _safe_text(ledger.get("schema_version")),
        "ledger_version": _safe_text(ledger.get("ledger_version")),
    }


def _entity_ref(value: Any) -> dict[str, Any]:
    source = value if isinstance(value, Mapping) else {}
    return {
        "entity_type": _safe_text(source.get("entity_type"), drop_sensitive=True),
        "stable_ref": _safe_text(source.get("stable_ref"), drop_sensitive=True),
        "game_number": _safe_text(source.get("game_number"), drop_sensitive=True),
        "action_index": _safe_text(source.get("action_index"), drop_sensitive=True),
    }


def _attachment_id(entry: Mapping[str, Any], entity_ref: Mapping[str, Any], index: int) -> str:
    parts = [
        _safe_text(entry.get("output_family")),
        _safe_text(entry.get("output_field")),
        _safe_text(entity_ref.get("stable_ref")) or f"field-ref-{index}",
    ]
    return ".".join(_slug(part) for part in parts if part)


def _slug(value: str) -> str:
    return SAFE_ID_RE.sub("_", value).strip("._") or "unknown"


def _candidate_ids(candidates: Sequence[Mapping[str, Any]]) -> list[str]:
    return _safe_string_list([candidate.get("entry_id", "") for candidate in candidates])


def _load_field_refs(path: Path) -> tuple[list[Any], list[str]]:
    payload, limitations = _load_json_any(path, "field references")
    if limitations:
        return [], limitations
    if isinstance(payload, list):
        return payload, []
    if isinstance(payload, Mapping) and isinstance(payload.get("field_refs"), list):
        return list(payload["field_refs"]), []
    return [], ["field references payload must be a list or mapping with field_refs"]


def _load_json_mapping(path: Path, label: str) -> tuple[Mapping[str, Any] | None, list[str]]:
    payload, limitations = _load_json_any(path, label)
    if limitations:
        return {}, limitations
    if not isinstance(payload, Mapping):
        return {}, [f"{label} is not a mapping"]
    return payload, []


def _load_json_any(path: Path, label: str) -> tuple[Any, list[str]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return None, [f"{label} could not be read: {exc.__class__.__name__}"]
    except json.JSONDecodeError:
        return None, [f"{label} is malformed JSON"]
    return payload, []


def _add_cli_limitations(report: dict[str, Any], limitations: Sequence[str]) -> None:
    safe_limitations = _safe_string_list(limitations, drop_sensitive=True)
    if not safe_limitations:
        return
    report["limitations"] = _dedupe([*report["limitations"], *safe_limitations])
    report["status"] = "fail"
    report["review_required"] = True
    report["status_reasons"] = _dedupe([*report["status_reasons"], "cli_input_error"])
    report["summary"]["failed_validation_count"] += len(safe_limitations)


def _write_markdown_report(path: Path, report: Mapping[str, Any]) -> None:
    findings = _privacy_findings(report, "report")
    combined = findings["forbidden_content_findings"] + findings["local_absolute_paths_found"]
    if combined:
        raise ValueError(f"forbidden runtime field-evidence markdown content: {', '.join(combined)}")
    summary = report.get("summary", {}) if isinstance(report.get("summary"), Mapping) else {}
    lines = [
        "# Runtime Field Evidence Report",
        "",
        f"- status: {_safe_text(report.get('status'))}",
        f"- field_ref_count: {summary.get('field_ref_count', 0)}",
        f"- attachment_count: {summary.get('attachment_count', 0)}",
        f"- missing_mapping_count: {summary.get('missing_mapping_count', 0)}",
        f"- ambiguous_mapping_count: {summary.get('ambiguous_mapping_count', 0)}",
        f"- failed_validation_count: {summary.get('failed_validation_count', 0)}",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _encode_report(report: Mapping[str, Any]) -> str:
    return json.dumps(report, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def _redact_sensitive_report_values(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _redact_sensitive_report_values(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact_sensitive_report_values(item) for item in value]
    if isinstance(value, tuple):
        return [_redact_sensitive_report_values(item) for item in value]
    if isinstance(value, str) and _string_is_sensitive(value):
        return ""
    return value


def _combined_privacy_findings(items: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    combined = {
        "forbidden_content_findings": [],
        "local_absolute_paths_found": [],
        "field_values_included": False,
    }
    for label, value in items:
        findings = _privacy_findings(value, label)
        combined["forbidden_content_findings"].extend(findings["forbidden_content_findings"])
        combined["local_absolute_paths_found"].extend(findings["local_absolute_paths_found"])
    combined["forbidden_content_findings"] = _dedupe(combined["forbidden_content_findings"])
    combined["local_absolute_paths_found"] = _dedupe(combined["local_absolute_paths_found"])
    return combined


def _privacy_findings(value: Any, path: str) -> dict[str, list[str]]:
    findings = {
        "forbidden_content_findings": [],
        "local_absolute_paths_found": [],
    }
    _collect_privacy_findings(value, path, findings)
    findings["forbidden_content_findings"] = _dedupe(findings["forbidden_content_findings"])
    findings["local_absolute_paths_found"] = _dedupe(findings["local_absolute_paths_found"])
    return findings


def _collect_privacy_findings(value: Any, path: str, findings: dict[str, list[str]]) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            _collect_privacy_findings(item, f"{path}.{key}", findings)
        return
    if isinstance(value, list | tuple):
        for index, item in enumerate(value):
            _collect_privacy_findings(item, f"{path}[{index}]", findings)
        return
    if not isinstance(value, str):
        return
    if ABSOLUTE_PATH_RE.search(value):
        findings["local_absolute_paths_found"].append(path)
    if FORBIDDEN_TEXT_RE.search(value):
        findings["forbidden_content_findings"].append(path)


def _field_value_paths(field_refs: Sequence[Any]) -> list[str]:
    paths: list[str] = []
    for index, item in enumerate(field_refs):
        if isinstance(item, Mapping) and "value" in item:
            paths.append(f"field_refs[{index}].value")
    return paths


def _has_privacy_findings(privacy: Mapping[str, Any]) -> bool:
    return bool(
        privacy.get("forbidden_content_findings")
        or privacy.get("local_absolute_paths_found")
        or privacy.get("field_values_included")
    )


def _safe_text(value: Any, *, drop_sensitive: bool = False) -> str:
    if value is None:
        return ""
    text = str(value)
    if drop_sensitive and _string_is_sensitive(text):
        return ""
    return text


def _safe_string_list(value: Any, *, drop_sensitive: bool = False) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, str | bytes):
        return []
    items: list[str] = []
    for item in value:
        text = _safe_text(item, drop_sensitive=drop_sensitive)
        if text:
            items.append(text)
    return items


def _string_is_sensitive(value: str) -> bool:
    return bool(ABSOLUTE_PATH_RE.search(value) or FORBIDDEN_TEXT_RE.search(value))


def _dedupe(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _dedupe_allowed_flags(values: Sequence[str]) -> list[str]:
    return [item for item in _dedupe(list(values)) if item in evidence_ledger.DRIFT_FLAGS]


if __name__ == "__main__":
    raise SystemExit(main())
