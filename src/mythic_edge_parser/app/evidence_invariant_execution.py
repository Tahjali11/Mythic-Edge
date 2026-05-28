"""Local review-only evidence-ledger invariant execution report builder."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from mythic_edge_parser.app import evidence_ledger, evidence_schema_drift_report, evidence_schema_snapshot

EVIDENCE_INVARIANT_EXECUTION_REPORT_OBJECT = "mythic_edge_player_log_evidence_invariant_execution_report"
EVIDENCE_INVARIANT_EXECUTION_REPORT_VERSION = "player_log_evidence_invariant_execution.v1"
EVIDENCE_INVARIANT_EXECUTION_REPORT_STATUSES = ("pass", "review", "fail")
EXECUTABLE_INVARIANT_IDS = (
    "ledger_validates_cleanly",
    "ledger_privacy_contract_holds",
    "invariant_status_vocabulary_matches_ledger",
    "entries_declare_invariant_checks",
    "entry_invariant_names_are_stable",
    "entry_invariant_names_are_unique_within_entry",
    "entries_with_invariants_have_review_modules",
    "entries_with_invariants_have_tests",
    "declared_invariant_inventory_is_deterministic",
    "schema_drift_report_is_usable_review_evidence",
    "schema_drift_report_protected_surface_assertions_hold",
)

SOURCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/179"
PARENT_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/11"
INVARIANT_NAME_RE = re.compile(r"^[a-z0-9_]+$")

GENERIC_LEDGER_REVIEW_MODULES = ("src/mythic_edge_parser/app/evidence_ledger.py",)
GENERIC_LEDGER_TESTS = ("tests/test_evidence_ledger.py",)
GENERIC_SCHEMA_DRIFT_REVIEW_MODULES = (
    "src/mythic_edge_parser/app/evidence_ledger.py",
    "src/mythic_edge_parser/app/evidence_schema_drift_report.py",
)
GENERIC_SCHEMA_DRIFT_TESTS = (
    "tests/test_evidence_ledger.py",
    "tests/test_evidence_schema_drift_report.py",
)
PRIVACY_FLAGS = ("sensitive_evidence_redacted", "invariant_failed")
PROTECTED_SURFACE_ASSERTIONS = {
    "parser_behavior_changed": False,
    "parser_state_final_reconciliation_changed": False,
    "parser_event_classes_changed": False,
    "router_semantics_changed": False,
    "diagnostics_report_shape_changed": False,
    "runtime_status_schema_changed": False,
    "log_drift_report_behavior_changed": False,
    "schema_snapshot_update_policy_changed": False,
    "schema_drift_report_behavior_changed": False,
    "golden_replay_behavior_changed": False,
    "feature_equity_behavior_changed": False,
    "workbook_schema_changed": False,
    "webhook_payload_shape_changed": False,
    "apps_script_behavior_changed": False,
    "output_transport_changed": False,
    "analytics_or_ai_truth_changed": False,
}


def build_evidence_invariant_execution_report(
    ledger: Mapping[str, Any] | None = None,
    *,
    schema_drift_report: Mapping[str, Any] | None = None,
    require_schema_drift_report: bool = False,
) -> dict[str, Any]:
    """Build deterministic metadata invariant review evidence."""

    source_ledger: Any = evidence_ledger.build_player_log_evidence_ledger() if ledger is None else ledger
    ledger_is_mapping = isinstance(source_ledger, Mapping)
    ledger_payload: Mapping[str, Any] = source_ledger if ledger_is_mapping else {}
    schema_report_supplied = schema_drift_report is not None
    schema_report_is_mapping = isinstance(schema_drift_report, Mapping)
    schema_report_payload: Mapping[str, Any] = schema_drift_report if schema_report_is_mapping else {}
    privacy = _combined_privacy_findings(
        (
            ("ledger", source_ledger),
            ("schema_drift_report", schema_drift_report),
        ),
    )
    privacy_blocked = _has_privacy_findings(privacy)

    validation_errors = (
        evidence_ledger.validate_player_log_evidence_ledger(ledger_payload)
        if ledger_is_mapping
        else ["ledger:not_mapping"]
    )
    entries = _entry_records(ledger_payload, privacy_blocked=privacy_blocked)
    output_family_by_entry = {entry["entry_id"]: entry["output_family"] for entry in entries if entry["entry_id"]}
    inventory = _declared_invariant_inventory(entries, privacy_blocked=privacy_blocked)

    results = [
        _ledger_validation_result(validation_errors),
        _privacy_result(privacy),
        _invariant_status_vocabulary_result(ledger_payload),
        _entries_declare_invariant_checks_result(inventory),
        _entry_invariant_names_are_stable_result(inventory),
        _entry_invariant_names_are_unique_within_entry_result(inventory),
        _entries_with_invariants_have_review_modules_result(entries),
        _entries_with_invariants_have_tests_result(entries),
        _declared_inventory_result(entries),
        _schema_drift_report_result(
            schema_report_payload,
            supplied=schema_report_supplied,
            is_mapping=schema_report_is_mapping,
            required=require_schema_drift_report,
            privacy_blocked=privacy_blocked,
        ),
        _schema_drift_protected_surface_result(
            schema_report_payload,
            supplied=schema_report_supplied,
            is_mapping=schema_report_is_mapping,
            required=require_schema_drift_report,
        ),
    ]
    affected = _affected_surfaces(results, inventory, output_family_by_entry)
    review_guidance = _review_guidance(
        results,
        affected,
        entries=entries,
        schema_drift_report=schema_report_payload if schema_report_is_mapping else {},
        privacy_blocked=privacy_blocked,
    )
    drift_flags = _report_drift_flags(
        results,
        schema_drift_report=schema_report_payload if schema_report_is_mapping else {},
    )
    if privacy_blocked:
        drift_flags.extend(PRIVACY_FLAGS)
    drift_flags = _dedupe_allowed_flags(drift_flags)

    status = _report_status(results, privacy, require_schema_drift_report)
    status_reasons = _status_reasons(results, privacy)
    limitations = _limitations(validation_errors, results)
    report = {
        "object": EVIDENCE_INVARIANT_EXECUTION_REPORT_OBJECT,
        "schema_version": EVIDENCE_INVARIANT_EXECUTION_REPORT_VERSION,
        "source_issue": SOURCE_ISSUE,
        "parent_issue": PARENT_ISSUE,
        "status": status,
        "review_required": status != "pass",
        "status_reasons": status_reasons,
        "input_refs": {
            "ledger": _ledger_input_ref(ledger_payload),
            "schema_drift_report": _schema_drift_report_input_ref(
                schema_report_payload,
                supplied=schema_report_supplied,
            ),
        },
        "summary": _summary(results, inventory, affected, drift_flags),
        "declared_invariants": {
            "total_count": inventory["total_count"],
            "unique_count": inventory["unique_count"],
            "shared_name_count": inventory["shared_name_count"],
            "entries_without_invariants": inventory["entries_without_invariants"],
            "duplicate_names_within_entries": inventory["duplicate_names_within_entries"],
            "invalid_names": inventory["invalid_names"],
            "by_output_family": inventory["by_output_family"],
        },
        "invariant_results": results,
        "affected": affected,
        "review_guidance": review_guidance,
        "drift_flags": drift_flags,
        "privacy": {
            "forbidden_content_findings": privacy["forbidden_content_findings"],
            "local_absolute_paths_found": privacy["local_absolute_paths_found"],
            "raw_private_logs_included": False,
            "raw_payload_values_included": False,
            "local_absolute_paths_included": False,
            "runtime_artifacts_included": False,
            "generated_data_included": False,
        },
        "protected_surface_assertions": dict(PROTECTED_SURFACE_ASSERTIONS),
        "limitations": limitations,
    }
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
        report["drift_flags"] = _dedupe_allowed_flags([*report["drift_flags"], *PRIVACY_FLAGS])
        report["summary"] = _summary(results, inventory, affected, report["drift_flags"])
    return report


def build_current_evidence_invariant_execution_report(
    *,
    expected_snapshot_path: Path | None = None,
    require_schema_drift_report: bool = True,
) -> dict[str, Any]:
    """Build a report for the current ledger and current schema drift report."""

    schema_report = (
        evidence_schema_drift_report.build_current_evidence_schema_drift_report(
            expected_snapshot_path=expected_snapshot_path,
        )
        if require_schema_drift_report
        else None
    )
    return build_evidence_invariant_execution_report(
        schema_drift_report=schema_report,
        require_schema_drift_report=require_schema_drift_report,
    )


def write_evidence_invariant_execution_report(path: Path, report: Mapping[str, Any]) -> None:
    """Write an invariant execution report to an explicit path after privacy scanning."""

    findings = _privacy_findings(report, "report")
    combined = findings["forbidden_content_findings"] + findings["local_absolute_paths_found"]
    if combined:
        raise ValueError(f"forbidden evidence invariant execution report content: {', '.join(combined)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_encode_report(report), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local Player.log evidence-ledger metadata invariants.")
    parser.add_argument("--check", action="store_true", help="Run invariant checks and print JSON.")
    parser.add_argument("--ledger", type=Path, help="Run against an explicit synthetic JSON ledger payload.")
    parser.add_argument("--schema-drift-report", type=Path, help="Use an explicit schema drift report JSON payload.")
    parser.add_argument(
        "--expected",
        type=Path,
        help="Expected schema snapshot path passed to schema drift report builder.",
    )
    parser.add_argument(
        "--no-schema-drift-report",
        action="store_true",
        help="Run ledger-only checks and mark schema drift dependency not_checked.",
    )
    parser.add_argument("--out", type=Path, help="Write JSON report to an explicit path.")
    parser.add_argument("--markdown-out", type=Path, help="Write a sanitized Markdown summary to an explicit path.")
    args = parser.parse_args(argv)

    ledger_payload, ledger_limitations = _load_json_mapping(args.ledger, "ledger") if args.ledger else (None, [])
    schema_report, schema_limitations = _schema_drift_report_for_cli(args)
    require_schema = not args.no_schema_drift_report
    report = build_evidence_invariant_execution_report(
        ledger_payload,
        schema_drift_report=schema_report,
        require_schema_drift_report=require_schema,
    )
    if ledger_limitations or schema_limitations:
        _add_cli_limitations(report, [*ledger_limitations, *schema_limitations])

    if args.out is not None:
        try:
            write_evidence_invariant_execution_report(args.out, report)
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


def _schema_drift_report_for_cli(args: argparse.Namespace) -> tuple[Mapping[str, Any] | None, list[str]]:
    if args.no_schema_drift_report:
        return None, []
    if args.schema_drift_report:
        return _load_json_mapping(args.schema_drift_report, "schema drift report")
    return (
        evidence_schema_drift_report.build_current_evidence_schema_drift_report(
            expected_snapshot_path=args.expected,
        ),
        [],
    )


def _load_json_mapping(path: Path, label: str) -> tuple[Mapping[str, Any], list[str]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return {}, [f"{label} could not be read: {exc.__class__.__name__}"]
    except json.JSONDecodeError:
        return {}, [f"{label} is malformed JSON"]
    if not isinstance(payload, Mapping):
        return {}, [f"{label} is not a mapping"]
    return payload, []


def _add_cli_limitations(report: dict[str, Any], limitations: Sequence[str]) -> None:
    safe_limitations = _safe_string_list(limitations, drop_sensitive=True)
    if not safe_limitations:
        return
    report["limitations"] = _dedupe([*report["limitations"], *safe_limitations])
    report["status"] = "fail"
    report["review_required"] = True
    report["status_reasons"] = _dedupe([*report["status_reasons"], "cli_input_error"])
    report["summary"]["failed_count"] += 1


def _ledger_validation_result(validation_errors: Sequence[str]) -> dict[str, Any]:
    if validation_errors:
        return _result(
            "ledger_validates_cleanly",
            "failed",
            "ledger",
            reason=f"ledger validator returned {len(validation_errors)} error(s)",
            drift_flags=["invariant_failed"],
            evidence_refs=["evidence_ledger.validate_player_log_evidence_ledger"],
            modules=GENERIC_LEDGER_REVIEW_MODULES,
            tests=GENERIC_LEDGER_TESTS,
        )
    return _result(
        "ledger_validates_cleanly",
        "passed",
        "ledger",
        evidence_refs=["evidence_ledger.validate_player_log_evidence_ledger"],
        modules=GENERIC_LEDGER_REVIEW_MODULES,
        tests=GENERIC_LEDGER_TESTS,
    )


def _privacy_result(privacy: Mapping[str, Sequence[str]]) -> dict[str, Any]:
    if _has_privacy_findings(privacy):
        return _result(
            "ledger_privacy_contract_holds",
            "failed",
            "ledger",
            reason="privacy findings detected",
            drift_flags=list(PRIVACY_FLAGS),
            evidence_refs=["privacy_scan"],
            modules=GENERIC_LEDGER_REVIEW_MODULES,
            tests=GENERIC_LEDGER_TESTS,
        )
    return _result(
        "ledger_privacy_contract_holds",
        "passed",
        "ledger",
        evidence_refs=["privacy_scan"],
        modules=GENERIC_LEDGER_REVIEW_MODULES,
        tests=GENERIC_LEDGER_TESTS,
    )


def _invariant_status_vocabulary_result(ledger: Mapping[str, Any]) -> dict[str, Any]:
    vocabulary = ledger.get("vocabulary") if isinstance(ledger.get("vocabulary"), Mapping) else {}
    if vocabulary.get("invariant_statuses") != list(evidence_ledger.INVARIANT_STATUSES):
        return _result(
            "invariant_status_vocabulary_matches_ledger",
            "failed",
            "ledger",
            reason="invariant status vocabulary mismatch",
            drift_flags=["changed_signal_type", "invariant_failed"],
            evidence_refs=["evidence_ledger.INVARIANT_STATUSES"],
            modules=GENERIC_LEDGER_REVIEW_MODULES,
            tests=GENERIC_LEDGER_TESTS,
        )
    return _result(
        "invariant_status_vocabulary_matches_ledger",
        "passed",
        "ledger",
        evidence_refs=["evidence_ledger.INVARIANT_STATUSES"],
        modules=GENERIC_LEDGER_REVIEW_MODULES,
        tests=GENERIC_LEDGER_TESTS,
    )


def _entries_declare_invariant_checks_result(inventory: Mapping[str, Any]) -> dict[str, Any]:
    affected = inventory["entries_without_invariants"]
    if affected:
        return _result(
            "entries_declare_invariant_checks",
            "failed",
            "entry",
            reason=f"{len(affected)} entry or entries lack invariant declarations",
            drift_flags=["invariant_failed"],
            affected_entries=affected,
            evidence_refs=["entry.invariant_checks"],
            modules=GENERIC_LEDGER_REVIEW_MODULES,
            tests=GENERIC_LEDGER_TESTS,
        )
    return _result(
        "entries_declare_invariant_checks",
        "passed",
        "entry",
        evidence_refs=["entry.invariant_checks"],
        modules=GENERIC_LEDGER_REVIEW_MODULES,
        tests=GENERIC_LEDGER_TESTS,
    )


def _entry_invariant_names_are_stable_result(inventory: Mapping[str, Any]) -> dict[str, Any]:
    invalid_names = inventory["invalid_names"]
    if invalid_names:
        return _result(
            "entry_invariant_names_are_stable",
            "failed",
            "entry",
            reason=f"{len(invalid_names)} invalid invariant name reference(s)",
            drift_flags=["invariant_failed"],
            affected_entries=_entry_ids_from_paths(invalid_names),
            evidence_refs=["entry.invariant_checks"],
            modules=GENERIC_LEDGER_REVIEW_MODULES,
            tests=GENERIC_LEDGER_TESTS,
        )
    return _result(
        "entry_invariant_names_are_stable",
        "passed",
        "entry",
        evidence_refs=["entry.invariant_checks"],
        modules=GENERIC_LEDGER_REVIEW_MODULES,
        tests=GENERIC_LEDGER_TESTS,
    )


def _entry_invariant_names_are_unique_within_entry_result(inventory: Mapping[str, Any]) -> dict[str, Any]:
    affected = inventory["duplicate_names_within_entries"]
    if affected:
        return _result(
            "entry_invariant_names_are_unique_within_entry",
            "failed",
            "entry",
            reason=f"{len(affected)} entry or entries repeat invariant names",
            drift_flags=["invariant_failed"],
            affected_entries=affected,
            evidence_refs=["entry.invariant_checks"],
            modules=GENERIC_LEDGER_REVIEW_MODULES,
            tests=GENERIC_LEDGER_TESTS,
        )
    return _result(
        "entry_invariant_names_are_unique_within_entry",
        "passed",
        "entry",
        evidence_refs=["entry.invariant_checks"],
        modules=GENERIC_LEDGER_REVIEW_MODULES,
        tests=GENERIC_LEDGER_TESTS,
    )


def _entries_with_invariants_have_review_modules_result(entries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    malformed, missing = _entries_missing_list_values(entries, "recommended_review_modules")
    if malformed:
        return _result(
            "entries_with_invariants_have_review_modules",
            "failed",
            "entry",
            reason=f"{len(malformed)} entry or entries have malformed review module lists",
            drift_flags=["invariant_failed"],
            affected_entries=malformed,
            evidence_refs=["entry.recommended_review_modules"],
            modules=GENERIC_LEDGER_REVIEW_MODULES,
            tests=GENERIC_LEDGER_TESTS,
        )
    if missing:
        return _result(
            "entries_with_invariants_have_review_modules",
            "degraded",
            "entry",
            reason=f"{len(missing)} entry or entries lack review module references",
            affected_entries=missing,
            evidence_refs=["entry.recommended_review_modules"],
            modules=GENERIC_LEDGER_REVIEW_MODULES,
            tests=GENERIC_LEDGER_TESTS,
        )
    return _result(
        "entries_with_invariants_have_review_modules",
        "passed",
        "entry",
        evidence_refs=["entry.recommended_review_modules"],
        modules=GENERIC_LEDGER_REVIEW_MODULES,
        tests=GENERIC_LEDGER_TESTS,
    )


def _entries_with_invariants_have_tests_result(entries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    malformed, missing = _entries_missing_list_values(entries, "tests")
    if malformed:
        return _result(
            "entries_with_invariants_have_tests",
            "failed",
            "entry",
            reason=f"{len(malformed)} entry or entries have malformed test lists",
            drift_flags=["invariant_failed"],
            affected_entries=malformed,
            evidence_refs=["entry.tests"],
            modules=GENERIC_LEDGER_REVIEW_MODULES,
            tests=GENERIC_LEDGER_TESTS,
        )
    if missing:
        return _result(
            "entries_with_invariants_have_tests",
            "degraded",
            "entry",
            reason=f"{len(missing)} entry or entries lack focused test references",
            affected_entries=missing,
            evidence_refs=["entry.tests"],
            modules=GENERIC_LEDGER_REVIEW_MODULES,
            tests=GENERIC_LEDGER_TESTS,
        )
    return _result(
        "entries_with_invariants_have_tests",
        "passed",
        "entry",
        evidence_refs=["entry.tests"],
        modules=GENERIC_LEDGER_REVIEW_MODULES,
        tests=GENERIC_LEDGER_TESTS,
    )


def _declared_inventory_result(entries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if any(not entry.get("entry_id") for entry in entries):
        return _result(
            "declared_invariant_inventory_is_deterministic",
            "failed",
            "ledger",
            reason="inventory could not resolve all entry IDs",
            drift_flags=["invariant_failed"],
            evidence_refs=["entry.entry_id", "entry.invariant_checks"],
            modules=GENERIC_LEDGER_REVIEW_MODULES,
            tests=GENERIC_LEDGER_TESTS,
        )
    return _result(
        "declared_invariant_inventory_is_deterministic",
        "passed",
        "ledger",
        evidence_refs=["entry.entry_id", "entry.invariant_checks"],
        modules=GENERIC_LEDGER_REVIEW_MODULES,
        tests=GENERIC_LEDGER_TESTS,
    )


def _schema_drift_report_result(
    schema_report: Mapping[str, Any],
    *,
    supplied: bool,
    is_mapping: bool,
    required: bool,
    privacy_blocked: bool,
) -> dict[str, Any]:
    if not supplied:
        if required:
            return _result(
                "schema_drift_report_is_usable_review_evidence",
                "failed",
                "schema_drift_report",
                reason="required schema drift report was not supplied",
                drift_flags=["schema_snapshot_missing", "invariant_failed"],
                evidence_refs=["evidence_schema_drift_report.build_current_evidence_schema_drift_report"],
                modules=GENERIC_SCHEMA_DRIFT_REVIEW_MODULES,
                tests=GENERIC_SCHEMA_DRIFT_TESTS,
            )
        return _result(
            "schema_drift_report_is_usable_review_evidence",
            "not_checked",
            "schema_drift_report",
            reason="schema drift report was not supplied and not required",
            evidence_refs=["evidence_schema_drift_report.build_current_evidence_schema_drift_report"],
            modules=GENERIC_SCHEMA_DRIFT_REVIEW_MODULES,
            tests=GENERIC_SCHEMA_DRIFT_TESTS,
        )
    if not is_mapping:
        return _result(
            "schema_drift_report_is_usable_review_evidence",
            "failed",
            "schema_drift_report",
            reason="schema drift report is malformed",
            drift_flags=["schema_snapshot_missing", "invariant_failed"],
            evidence_refs=["schema_drift_report.status"],
            modules=GENERIC_SCHEMA_DRIFT_REVIEW_MODULES,
            tests=GENERIC_SCHEMA_DRIFT_TESTS,
        )

    status = _safe_text(schema_report.get("status")) if not privacy_blocked else ""
    if status == "pass":
        return _result(
            "schema_drift_report_is_usable_review_evidence",
            "passed",
            "schema_drift_report",
            evidence_refs=["schema_drift_report.status"],
            modules=GENERIC_SCHEMA_DRIFT_REVIEW_MODULES,
            tests=GENERIC_SCHEMA_DRIFT_TESTS,
        )
    if status == "review":
        return _result(
            "schema_drift_report_is_usable_review_evidence",
            "degraded",
            "schema_drift_report",
            reason="schema drift review is required before approving any snapshot update",
            drift_flags=_allowed_drift_flags(schema_report.get("drift_flags")),
            evidence_refs=["schema_drift_report.status"],
            modules=GENERIC_SCHEMA_DRIFT_REVIEW_MODULES,
            tests=GENERIC_SCHEMA_DRIFT_TESTS,
        )
    return _result(
        "schema_drift_report_is_usable_review_evidence",
        "failed",
        "schema_drift_report",
        reason="schema drift report status is fail, unknown, or malformed",
        drift_flags=[*_allowed_drift_flags(schema_report.get("drift_flags")), "invariant_failed"],
        evidence_refs=["schema_drift_report.status"],
        modules=GENERIC_SCHEMA_DRIFT_REVIEW_MODULES,
        tests=GENERIC_SCHEMA_DRIFT_TESTS,
    )


def _schema_drift_protected_surface_result(
    schema_report: Mapping[str, Any],
    *,
    supplied: bool,
    is_mapping: bool,
    required: bool,
) -> dict[str, Any]:
    if not supplied:
        status = "failed" if required else "not_checked"
        return _result(
            "schema_drift_report_protected_surface_assertions_hold",
            status,
            "schema_drift_report",
            reason="schema drift report was not supplied",
            drift_flags=["invariant_failed"] if required else [],
            evidence_refs=["schema_drift_report.protected_surface_assertions"],
            modules=GENERIC_SCHEMA_DRIFT_REVIEW_MODULES,
            tests=GENERIC_SCHEMA_DRIFT_TESTS,
        )
    assertions = schema_report.get("protected_surface_assertions") if is_mapping else None
    if not isinstance(assertions, Mapping) or any(value is not False for value in assertions.values()):
        return _result(
            "schema_drift_report_protected_surface_assertions_hold",
            "failed",
            "schema_drift_report",
            reason="schema drift report protected surface assertions are missing or non-false",
            drift_flags=["invariant_failed"],
            evidence_refs=["schema_drift_report.protected_surface_assertions"],
            modules=GENERIC_SCHEMA_DRIFT_REVIEW_MODULES,
            tests=GENERIC_SCHEMA_DRIFT_TESTS,
        )
    return _result(
        "schema_drift_report_protected_surface_assertions_hold",
        "passed",
        "schema_drift_report",
        evidence_refs=["schema_drift_report.protected_surface_assertions"],
        modules=GENERIC_SCHEMA_DRIFT_REVIEW_MODULES,
        tests=GENERIC_SCHEMA_DRIFT_TESTS,
    )


def _result(
    invariant_id: str,
    status: str,
    scope: str,
    *,
    entry_id: str = "",
    output_family: str = "",
    reason: str = "",
    drift_flags: Sequence[str] = (),
    evidence_refs: Sequence[str] = (),
    modules: Sequence[str] = (),
    tests: Sequence[str] = (),
    affected_entries: Sequence[str] = (),
) -> dict[str, Any]:
    if status not in evidence_ledger.INVARIANT_STATUSES:
        status = "failed"
    return {
        "invariant_id": invariant_id,
        "status": status,
        "scope": scope,
        "entry_id": entry_id,
        "output_family": output_family,
        "review_required": status in {"failed", "degraded"},
        "drift_flags": _dedupe_allowed_flags(drift_flags),
        "reason": _safe_text(reason),
        "evidence_refs": _safe_string_list(evidence_refs),
        "recommended_review_modules": _safe_string_list(modules),
        "recommended_tests": _safe_string_list(tests),
        "affected_entries": _safe_string_list(affected_entries),
    }


def _entry_records(ledger: Mapping[str, Any], *, privacy_blocked: bool) -> list[dict[str, Any]]:
    entries = ledger.get("entries")
    if not isinstance(entries, list):
        return []
    records: list[dict[str, Any]] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, Mapping):
            records.append(
                {
                    "entry_id": f"ledger.entries[{index}]",
                    "output_family": "",
                    "invariant_checks": [],
                    "recommended_review_modules": [],
                    "tests": [],
                    "malformed": True,
                },
            )
            continue
        records.append(
            {
                "entry_id": _safe_text(entry.get("entry_id")) or f"ledger.entries[{index}]",
                "output_family": _safe_text(entry.get("output_family")),
                "invariant_checks": _safe_list(entry.get("invariant_checks"), drop_sensitive=False),
                "recommended_review_modules": _safe_list(
                    entry.get("recommended_review_modules"),
                    drop_sensitive=privacy_blocked,
                ),
                "tests": _safe_list(entry.get("tests"), drop_sensitive=privacy_blocked),
                "malformed": False,
                "raw_invariant_checks_is_list": isinstance(entry.get("invariant_checks"), list),
                "raw_review_modules_is_list": isinstance(entry.get("recommended_review_modules"), list),
                "raw_tests_is_list": isinstance(entry.get("tests"), list),
            },
        )
    return records


def _declared_invariant_inventory(entries: Sequence[Mapping[str, Any]], *, privacy_blocked: bool) -> dict[str, Any]:
    total_count = 0
    name_counts: Counter[str] = Counter()
    by_output_family: dict[str, list[str]] = defaultdict(list)
    entries_without_invariants: list[str] = []
    duplicate_names_within_entries: list[str] = []
    invalid_names: list[str] = []

    for entry_index, entry in enumerate(entries):
        entry_id = str(entry.get("entry_id") or f"ledger.entries[{entry_index}]")
        output_family = str(entry.get("output_family") or "")
        checks = entry.get("invariant_checks") if isinstance(entry.get("invariant_checks"), list) else []
        if not checks:
            entries_without_invariants.append(entry_id)
        total_count += len(checks)
        per_entry_valid_names: list[str] = []
        per_entry_counts: Counter[str] = Counter()
        for check_index, check in enumerate(checks):
            path = f"{entry_id}.invariant_checks[{check_index}]"
            if not isinstance(check, str) or not _valid_invariant_name(check):
                invalid_names.append(path)
                continue
            per_entry_valid_names.append(check)
            per_entry_counts[check] += 1
            name_counts[check] += 1
        if any(count > 1 for count in per_entry_counts.values()):
            duplicate_names_within_entries.append(entry_id)
        by_output_family[output_family].extend(per_entry_valid_names)

    return {
        "total_count": total_count,
        "unique_count": len(name_counts),
        "shared_name_count": sum(1 for count in name_counts.values() if count > 1),
        "entries_without_invariants": sorted(set(entries_without_invariants)),
        "duplicate_names_within_entries": sorted(set(duplicate_names_within_entries)),
        "invalid_names": sorted(set(invalid_names)),
        "by_output_family": {family: sorted(set(names)) for family, names in sorted(by_output_family.items())},
    }


def _entries_missing_list_values(entries: Sequence[Mapping[str, Any]], key: str) -> tuple[list[str], list[str]]:
    list_marker = f"raw_{'review_modules' if key == 'recommended_review_modules' else key}_is_list"
    malformed: list[str] = []
    missing: list[str] = []
    for entry in entries:
        entry_id = str(entry.get("entry_id") or "")
        checks = entry.get("invariant_checks") if isinstance(entry.get("invariant_checks"), list) else []
        if not checks:
            continue
        if entry.get(list_marker) is False:
            malformed.append(entry_id)
            continue
        values = entry.get(key) if isinstance(entry.get(key), list) else []
        if not values:
            missing.append(entry_id)
    return sorted(set(malformed)), sorted(set(missing))


def _affected_surfaces(
    results: Sequence[Mapping[str, Any]],
    inventory: Mapping[str, Any],
    output_family_by_entry: Mapping[str, str],
) -> dict[str, list[str]]:
    entries: set[str] = set()
    output_families: set[str] = set()
    for result in results:
        if result.get("status") not in {"failed", "degraded"}:
            continue
        entries.update(_safe_string_list(result.get("affected_entries")))
        entry_id = _safe_text(result.get("entry_id"))
        if entry_id:
            entries.add(entry_id)
        output_family = _safe_text(result.get("output_family"))
        if output_family:
            output_families.add(output_family)
    entries.update(_entry_ids_from_paths(inventory["invalid_names"]))
    for entry_id in entries:
        output_family = output_family_by_entry.get(entry_id)
        if output_family:
            output_families.add(output_family)
    return {
        "output_families": sorted(output_families),
        "entries": sorted(entries),
    }


def _review_guidance(
    results: Sequence[Mapping[str, Any]],
    affected: Mapping[str, Sequence[str]],
    *,
    entries: Sequence[Mapping[str, Any]],
    schema_drift_report: Mapping[str, Any],
    privacy_blocked: bool,
) -> dict[str, list[str]]:
    modules: list[str] = []
    tests: list[str] = []
    notes: list[str] = []
    entry_by_id = {str(entry.get("entry_id") or ""): entry for entry in entries}
    for result in results:
        if result.get("status") not in {"failed", "degraded"}:
            continue
        modules.extend(_safe_string_list(result.get("recommended_review_modules")))
        tests.extend(_safe_string_list(result.get("recommended_tests")))
        reason = _safe_text(result.get("reason"))
        if reason:
            notes.append(reason)
    for entry_id in affected["entries"]:
        entry = entry_by_id.get(entry_id)
        if entry is None:
            modules.extend(GENERIC_SCHEMA_DRIFT_REVIEW_MODULES)
            tests.extend(GENERIC_SCHEMA_DRIFT_TESTS)
            continue
        modules.extend(_safe_list(entry.get("recommended_review_modules"), drop_sensitive=privacy_blocked))
        tests.extend(_safe_list(entry.get("tests"), drop_sensitive=privacy_blocked))
    if schema_drift_report:
        guidance = schema_drift_report.get("review_guidance")
        if isinstance(guidance, Mapping):
            modules.extend(
                _safe_string_list(guidance.get("recommended_review_modules"), drop_sensitive=privacy_blocked),
            )
            tests.extend(_safe_string_list(guidance.get("recommended_tests"), drop_sensitive=privacy_blocked))
    if any(result.get("status") == "degraded" for result in results):
        notes.append("Invariant execution is review evidence only and does not approve snapshot or parser changes.")
    if any(result.get("status") == "failed" for result in results):
        notes.append("One or more metadata invariants failed; inspect affected entries and review targets.")
    return {
        "recommended_review_modules": sorted(set(modules)),
        "recommended_tests": sorted(set(tests)),
        "review_notes": _dedupe(notes),
    }


def _report_drift_flags(results: Sequence[Mapping[str, Any]], *, schema_drift_report: Mapping[str, Any]) -> list[str]:
    flags: list[str] = []
    for result in results:
        flags.extend(_safe_string_list(result.get("drift_flags")))
    if schema_drift_report:
        flags.extend(_allowed_drift_flags(schema_drift_report.get("drift_flags")))
    return _dedupe_allowed_flags(flags)


def _report_status(
    results: Sequence[Mapping[str, Any]],
    privacy: Mapping[str, Sequence[str]],
    require_schema_drift_report: bool,
) -> str:
    if _has_privacy_findings(privacy):
        return "fail"
    if any(result["status"] == "failed" for result in results):
        return "fail"
    if any(result["status"] == "degraded" for result in results):
        return "review"
    if require_schema_drift_report and any(result["status"] == "not_checked" for result in results):
        return "review"
    return "pass"


def _status_reasons(results: Sequence[Mapping[str, Any]], privacy: Mapping[str, Sequence[str]]) -> list[str]:
    reasons: list[str] = []
    if _has_privacy_findings(privacy):
        reasons.append("privacy_findings")
    if any(result["status"] == "failed" for result in results):
        reasons.append("invariant_failed")
    if any(result["status"] == "degraded" for result in results):
        reasons.append("invariant_degraded")
    return reasons


def _summary(
    results: Sequence[Mapping[str, Any]],
    inventory: Mapping[str, Any],
    affected: Mapping[str, Sequence[str]],
    drift_flags: Sequence[str],
) -> dict[str, int]:
    status_counts = Counter(result["status"] for result in results)
    return {
        "executable_invariant_count": len(EXECUTABLE_INVARIANT_IDS),
        "declared_invariant_total_count": int(inventory["total_count"]),
        "declared_invariant_unique_count": int(inventory["unique_count"]),
        "passed_count": status_counts["passed"],
        "failed_count": status_counts["failed"],
        "degraded_count": status_counts["degraded"],
        "not_applicable_count": status_counts["not_applicable"],
        "not_checked_count": status_counts["not_checked"],
        "affected_entry_count": len(affected["entries"]),
        "affected_output_family_count": len(affected["output_families"]),
        "drift_flag_count": len(drift_flags),
    }


def _limitations(validation_errors: Sequence[str], results: Sequence[Mapping[str, Any]]) -> list[str]:
    limitations: list[str] = []
    if validation_errors:
        limitations.append(f"ledger validation returned {len(validation_errors)} error(s)")
    if any(result["status"] == "not_checked" for result in results):
        limitations.append("optional schema drift report check was not run")
    return limitations


def _ledger_input_ref(ledger: Mapping[str, Any]) -> dict[str, str]:
    return {
        "object": _safe_text(ledger.get("object")),
        "schema_version": _safe_text(ledger.get("schema_version")),
        "ledger_version": _safe_text(ledger.get("ledger_version")),
        "source_issue": _safe_text(ledger.get("source_issue")),
        "parent_issue": _safe_text(ledger.get("parent_issue")),
    }


def _schema_drift_report_input_ref(schema_report: Mapping[str, Any], *, supplied: bool) -> dict[str, Any]:
    comparison = schema_report.get("comparison") if isinstance(schema_report.get("comparison"), Mapping) else {}
    return {
        "supplied": supplied,
        "status": _safe_text(schema_report.get("status")),
        "schema_version": _safe_text(schema_report.get("schema_version")),
        "expected_snapshot_id": _safe_text(comparison.get("expected_snapshot_id")),
        "current_snapshot_id": _safe_text(comparison.get("current_snapshot_id")),
    }


def _combined_privacy_findings(inputs: Sequence[tuple[str, Any]]) -> dict[str, list[str]]:
    findings = {
        "forbidden_content_findings": [],
        "local_absolute_paths_found": [],
    }
    for label, payload in inputs:
        if payload is None:
            continue
        payload_findings = _privacy_findings(payload, label)
        findings["forbidden_content_findings"].extend(payload_findings["forbidden_content_findings"])
        findings["local_absolute_paths_found"].extend(payload_findings["local_absolute_paths_found"])
    return {
        "forbidden_content_findings": _dedupe(findings["forbidden_content_findings"]),
        "local_absolute_paths_found": _dedupe(findings["local_absolute_paths_found"]),
    }


def _privacy_findings(payload: Any, path: str) -> dict[str, list[str]]:
    findings = {
        "forbidden_content_findings": [],
        "local_absolute_paths_found": [],
    }
    _collect_privacy_findings(payload, path, findings)
    return {
        "forbidden_content_findings": _dedupe(findings["forbidden_content_findings"]),
        "local_absolute_paths_found": _dedupe(findings["local_absolute_paths_found"]),
    }


def _collect_privacy_findings(payload: Any, path: str, findings: dict[str, list[str]]) -> None:
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            _collect_privacy_findings(value, f"{path}.{key}", findings)
        return
    if isinstance(payload, list | tuple):
        for index, value in enumerate(payload):
            _collect_privacy_findings(value, f"{path}[{index}]", findings)
        return
    if not isinstance(payload, str):
        return

    if evidence_schema_snapshot.LOCAL_ABSOLUTE_PATH_RE.search(payload):
        findings["local_absolute_paths_found"].append(path)
    if evidence_schema_snapshot.FORBIDDEN_VALUE_RE.search(payload) or any(
        snippet in payload for snippet in evidence_schema_snapshot.FORBIDDEN_VALUE_SNIPPETS
    ):
        findings["forbidden_content_findings"].append(path)


def _has_privacy_findings(privacy: Mapping[str, Sequence[str]]) -> bool:
    return bool(privacy.get("forbidden_content_findings") or privacy.get("local_absolute_paths_found"))


def _valid_invariant_name(value: str) -> bool:
    return bool(
        value
        and INVARIANT_NAME_RE.fullmatch(value)
        and not _contains_forbidden_content(value)
        and "/" not in value
        and "\\" not in value
    )


def _contains_forbidden_content(text: str) -> bool:
    return bool(
        evidence_schema_snapshot.LOCAL_ABSOLUTE_PATH_RE.search(text)
        or evidence_schema_snapshot.FORBIDDEN_VALUE_RE.search(text)
        or any(snippet in text for snippet in evidence_schema_snapshot.FORBIDDEN_VALUE_SNIPPETS)
    )


def _entry_ids_from_paths(paths: Sequence[str]) -> list[str]:
    entries: list[str] = []
    for path in paths:
        if ".invariant_checks[" in path:
            entries.append(path.split(".invariant_checks[", 1)[0])
    return sorted(set(entries))


def _safe_text(value: Any) -> str:
    text = str(value or "")
    if _contains_forbidden_content(text):
        return ""
    return text


def _safe_list(value: Any, *, drop_sensitive: bool = False) -> list[Any]:
    if not isinstance(value, list | tuple):
        return []
    result: list[Any] = []
    for item in value:
        if isinstance(item, str):
            if drop_sensitive and _contains_forbidden_content(item):
                continue
            result.append(_safe_text(item))
        else:
            result.append(item)
    return result


def _safe_string_list(value: Any, *, drop_sensitive: bool = False) -> list[str]:
    if not isinstance(value, list | tuple):
        return []
    result: list[str] = []
    for item in value:
        text = str(item)
        if drop_sensitive and _contains_forbidden_content(text):
            continue
        safe = _safe_text(text)
        if safe:
            result.append(safe)
    return sorted(_dedupe(result))


def _allowed_drift_flags(value: Any) -> list[str]:
    return [flag for flag in _safe_string_list(value, drop_sensitive=True) if flag in evidence_ledger.DRIFT_FLAGS]


def _dedupe_allowed_flags(values: Sequence[str]) -> list[str]:
    return [flag for flag in _dedupe([str(value) for value in values]) if flag in evidence_ledger.DRIFT_FLAGS]


def _encode_report(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _write_markdown_report(path: Path, report: Mapping[str, Any]) -> None:
    findings = _privacy_findings(report, "report")
    combined = findings["forbidden_content_findings"] + findings["local_absolute_paths_found"]
    if combined:
        raise ValueError(f"forbidden evidence invariant execution report content: {', '.join(combined)}")
    lines = [
        "# Player.log Evidence Ledger Invariant Execution Report",
        "",
        f"- status: {report.get('status', '')}",
        f"- review_required: {str(report.get('review_required', False)).lower()}",
        f"- executable_invariants: {(report.get('summary') or {}).get('executable_invariant_count', 0)}",
        f"- affected_entries: {len((report.get('affected') or {}).get('entries', []))}",
        "",
        "This report is local review evidence only. It does not decide parser correctness or merge readiness.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _dedupe(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


if __name__ == "__main__":
    raise SystemExit(main())
