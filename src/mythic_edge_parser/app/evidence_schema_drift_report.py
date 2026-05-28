"""Review-only evidence-ledger schema drift report builder."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from mythic_edge_parser.app import evidence_schema_snapshot

EVIDENCE_SCHEMA_DRIFT_REPORT_OBJECT = "mythic_edge_player_log_evidence_schema_drift_report"
EVIDENCE_SCHEMA_DRIFT_REPORT_VERSION = "player_log_evidence_schema_drift_report.v1"
EVIDENCE_SCHEMA_DRIFT_REPORT_STATUSES = ("pass", "review", "fail")

SOURCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/177"
PARENT_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/11"

DIFF_KEYS = (
    "added_output_families",
    "removed_output_families",
    "changed_output_families",
    "added_entries",
    "removed_entries",
    "changed_entries",
    "added_evidence_signals",
    "removed_evidence_signals",
    "changed_evidence_signals",
    "changed_vocabulary",
    "changed_policies",
)
OUTPUT_FAMILY_DIFF_KEYS = ("added_output_families", "removed_output_families", "changed_output_families")
ENTRY_DIFF_KEYS = ("added_entries", "removed_entries", "changed_entries")
EVIDENCE_SIGNAL_DIFF_KEYS = ("added_evidence_signals", "removed_evidence_signals", "changed_evidence_signals")
ENTRY_POLICY_SUFFIXES = (".value_source_policy", ".confidence_policy", ".finality_policy")

GENERIC_REVIEW_MODULES = (
    "src/mythic_edge_parser/app/evidence_ledger.py",
    "src/mythic_edge_parser/app/evidence_schema_snapshot.py",
)
GENERIC_REVIEW_TESTS = (
    "tests/test_evidence_ledger.py",
    "tests/test_evidence_schema_snapshot.py",
)

PROTECTED_SURFACE_ASSERTIONS = {
    "parser_behavior_changed": False,
    "parser_state_final_reconciliation_changed": False,
    "parser_event_classes_changed": False,
    "runtime_status_schema_changed": False,
    "diagnostics_report_shape_changed": False,
    "golden_replay_behavior_changed": False,
    "feature_equity_behavior_changed": False,
    "workbook_schema_changed": False,
    "webhook_payload_shape_changed": False,
    "apps_script_behavior_changed": False,
    "output_transport_changed": False,
    "analytics_or_ai_truth_changed": False,
}


def build_evidence_schema_drift_report(
    comparison: Mapping[str, Any],
    *,
    current_snapshot: Mapping[str, Any] | None = None,
    expected_snapshot: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build deterministic review guidance from an evidence schema snapshot comparison."""

    comparison_is_mapping = isinstance(comparison, Mapping)
    comparison_payload = comparison if comparison_is_mapping else {}
    input_privacy = _combined_privacy_findings(
        (
            ("comparison", comparison),
            ("current_snapshot", current_snapshot),
            ("expected_snapshot", expected_snapshot),
        ),
    )
    malformed = not comparison_is_mapping or not _has_required_comparison_shape(comparison_payload)
    comparison_status = _safe_text(comparison_payload.get("status"))
    diff = _normal_diff(comparison_payload.get("diff"), privacy_blocked=_has_privacy_findings(input_privacy))
    comparison_privacy = _normal_privacy(comparison_payload.get("privacy"))
    privacy = _merge_privacy_findings(comparison_privacy, input_privacy)
    limitations = _safe_string_list(
        comparison_payload.get("limitations"),
        drop_sensitive=_has_privacy_findings(input_privacy),
    )

    status, status_reasons = _report_status(comparison_status, malformed, privacy, limitations)
    if malformed and "comparison input is malformed" not in limitations:
        limitations = [*limitations, "comparison input is malformed"]

    affected = _affected_surfaces(diff, current_snapshot=current_snapshot, expected_snapshot=expected_snapshot)
    review_guidance = _review_guidance(
        diff,
        affected,
        privacy,
        current_snapshot=current_snapshot,
        expected_snapshot=expected_snapshot,
        status=status,
    )
    drift_flags = _drift_flags(
        comparison_payload,
        diff=diff,
        malformed=malformed,
        privacy=privacy,
        limitations=limitations,
    )
    summary = _summary(diff, privacy, affected, review_guidance, limitations)

    report = {
        "object": EVIDENCE_SCHEMA_DRIFT_REPORT_OBJECT,
        "schema_version": EVIDENCE_SCHEMA_DRIFT_REPORT_VERSION,
        "source_issue": SOURCE_ISSUE,
        "parent_issue": PARENT_ISSUE,
        "status": status,
        "review_required": status != "pass",
        "status_reasons": status_reasons,
        "comparison": {
            "object": _safe_text(comparison_payload.get("object")),
            "schema_version": _safe_text(comparison_payload.get("schema_version")),
            "status": comparison_status,
            "expected_snapshot_id": _safe_text(comparison_payload.get("expected_snapshot_id")),
            "current_snapshot_id": _safe_text(comparison_payload.get("current_snapshot_id")),
        },
        "summary": summary,
        "drift": diff,
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
        report["drift_flags"] = _dedupe([*report["drift_flags"], "sensitive_evidence_redacted"])
        report["summary"] = _summary(diff, report["privacy"], affected, review_guidance, limitations)
    return report


def build_current_evidence_schema_drift_report(
    *,
    expected_snapshot_path: Path | None = None,
) -> dict[str, Any]:
    """Build a drift report for the current evidence-ledger schema snapshot."""

    expected_path = expected_snapshot_path or evidence_schema_snapshot.EXPECTED_EVIDENCE_SCHEMA_SNAPSHOT_PATH
    try:
        current = evidence_schema_snapshot.build_evidence_schema_snapshot()
    except (TypeError, ValueError) as exc:
        return build_evidence_schema_drift_report(
            _failure_comparison(f"current snapshot could not be built: {exc.__class__.__name__}"),
        )

    try:
        expected = evidence_schema_snapshot.load_expected_evidence_schema_snapshot(expected_path)
    except OSError as exc:
        return build_evidence_schema_drift_report(
            _failure_comparison(f"expected snapshot could not be read: {exc.__class__.__name__}", current=current),
            current_snapshot=current,
        )
    except json.JSONDecodeError:
        return build_evidence_schema_drift_report(
            _failure_comparison("expected snapshot is malformed JSON", current=current),
            current_snapshot=current,
        )

    comparison = evidence_schema_snapshot.compare_evidence_schema_snapshot(current, expected)
    return build_evidence_schema_drift_report(
        comparison,
        current_snapshot=current,
        expected_snapshot=expected,
    )


def write_evidence_schema_drift_report(
    path: Path,
    report: Mapping[str, Any],
) -> None:
    """Write a drift report to an explicit local path after privacy scanning."""

    findings = _privacy_findings(report, "report")
    combined = findings["forbidden_content_findings"] + findings["local_absolute_paths_found"]
    if combined:
        raise ValueError(f"forbidden evidence schema drift report content: {', '.join(combined)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_encode_report(report), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a Player.log evidence-ledger schema drift report.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Build a report from the current evidence schema snapshot.")
    mode.add_argument("--comparison", type=Path, help="Build a report from an existing snapshot comparison JSON file.")
    parser.add_argument("--expected", type=Path, help="Expected snapshot path for --check mode.")
    parser.add_argument("--out", type=Path, help="Write JSON report to an explicit path.")
    parser.add_argument("--markdown-out", type=Path, help="Write a sanitized Markdown summary to an explicit path.")
    args = parser.parse_args(argv)

    if args.comparison is not None:
        report = _report_from_comparison_path(args.comparison)
    else:
        report = build_current_evidence_schema_drift_report(expected_snapshot_path=args.expected)

    if args.out is not None:
        try:
            write_evidence_schema_drift_report(args.out, report)
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


def _report_from_comparison_path(path: Path) -> dict[str, Any]:
    try:
        comparison = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return build_evidence_schema_drift_report(
            _failure_comparison(f"comparison could not be read: {exc.__class__.__name__}"),
        )
    except json.JSONDecodeError:
        return build_evidence_schema_drift_report(_failure_comparison("comparison is malformed JSON"))
    return build_evidence_schema_drift_report(comparison)


def _failure_comparison(reason: str, *, current: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "object": evidence_schema_snapshot.EVIDENCE_SCHEMA_SNAPSHOT_COMPARISON_OBJECT,
        "schema_version": evidence_schema_snapshot.EVIDENCE_SCHEMA_SNAPSHOT_COMPARISON_VERSION,
        "status": "fail",
        "expected_snapshot_id": "",
        "current_snapshot_id": _safe_text((current or {}).get("snapshot_id")),
        "summary": {
            "output_family_changes": 0,
            "entry_changes": 0,
            "evidence_signal_changes": 0,
            "vocabulary_changes": 0,
            "policy_changes": 0,
            "privacy_findings": 0,
            "forbidden_content_findings": 0,
        },
        "diff": {key: [] for key in DIFF_KEYS},
        "privacy": {
            "forbidden_content_findings": [],
            "local_absolute_paths_found": [],
        },
        "drift_flags": ["schema_snapshot_missing"],
        "review_required": True,
        "limitations": [reason],
    }


def _report_status(
    comparison_status: str,
    malformed: bool,
    privacy: Mapping[str, list[str]],
    limitations: Sequence[str],
) -> tuple[str, list[str]]:
    status_reasons: list[str] = []
    if malformed:
        status_reasons.append("malformed_comparison")
    if comparison_status not in {"pass", "diff", "fail"} and comparison_status:
        status_reasons.append("unknown_comparison_status")
    if _has_privacy_findings(privacy):
        status_reasons.append("privacy_findings")
    if limitations and comparison_status == "pass":
        status_reasons.append("comparison_limitations")

    if status_reasons:
        return "fail", status_reasons
    if comparison_status == "pass":
        return "pass", []
    if comparison_status == "diff":
        return "review", ["snapshot_comparison_diff"]
    if comparison_status == "fail":
        return "fail", ["snapshot_comparison_fail"]
    return "fail", ["unknown_comparison_status"]


def _has_required_comparison_shape(comparison: Mapping[str, Any]) -> bool:
    return (
        isinstance(comparison.get("status"), str)
        and isinstance(comparison.get("diff"), Mapping)
        and isinstance(comparison.get("privacy"), Mapping)
        and isinstance(comparison.get("limitations"), list)
    )


def _normal_diff(value: Any, *, privacy_blocked: bool) -> dict[str, list[str]]:
    diff = value if isinstance(value, Mapping) else {}
    return {key: _safe_string_list(diff.get(key), drop_sensitive=privacy_blocked) for key in DIFF_KEYS}


def _normal_privacy(value: Any) -> dict[str, list[str]]:
    privacy = value if isinstance(value, Mapping) else {}
    return {
        "forbidden_content_findings": _safe_string_list(privacy.get("forbidden_content_findings")),
        "local_absolute_paths_found": _safe_string_list(privacy.get("local_absolute_paths_found")),
    }


def _summary(
    diff: Mapping[str, Sequence[str]],
    privacy: Mapping[str, Sequence[str]],
    affected: Mapping[str, Sequence[str]],
    review_guidance: Mapping[str, Sequence[str]],
    limitations: Sequence[str],
) -> dict[str, int]:
    forbidden_count = len(privacy.get("forbidden_content_findings", ()))
    local_path_count = len(privacy.get("local_absolute_paths_found", ()))
    return {
        "output_family_changes": sum(len(diff[key]) for key in OUTPUT_FAMILY_DIFF_KEYS),
        "entry_changes": sum(len(diff[key]) for key in ENTRY_DIFF_KEYS),
        "evidence_signal_changes": sum(len(diff[key]) for key in EVIDENCE_SIGNAL_DIFF_KEYS),
        "vocabulary_changes": len(diff["changed_vocabulary"]),
        "policy_changes": len(diff["changed_policies"]),
        "privacy_findings": forbidden_count + local_path_count,
        "forbidden_content_findings": forbidden_count,
        "limitation_count": len(limitations),
        "affected_output_family_count": len(affected.get("output_families", ())),
        "affected_entry_count": len(affected.get("entries", ())),
        "affected_evidence_signal_count": len(affected.get("evidence_signals", ())),
        "recommended_review_module_count": len(review_guidance.get("recommended_review_modules", ())),
        "recommended_test_count": len(review_guidance.get("recommended_tests", ())),
    }


def _affected_surfaces(
    diff: Mapping[str, Sequence[str]],
    *,
    current_snapshot: Mapping[str, Any] | None,
    expected_snapshot: Mapping[str, Any] | None,
) -> dict[str, list[str]]:
    entries = set().union(*(set(diff[key]) for key in ENTRY_DIFF_KEYS))
    evidence_signals = set().union(*(set(diff[key]) for key in EVIDENCE_SIGNAL_DIFF_KEYS))
    entries.update(_entry_id_from_signal_key(signal_key) for signal_key in evidence_signals)
    entries.update(_entry_id_from_policy_key(policy_key) for policy_key in diff["changed_policies"])
    entries.discard("")

    entry_records = _entry_records(current_snapshot, expected_snapshot)
    output_families = set().union(*(set(diff[key]) for key in OUTPUT_FAMILY_DIFF_KEYS))
    for entry_id in entries:
        entry = entry_records.get(entry_id)
        if entry is not None:
            output_family = _safe_text(entry.get("output_family"))
            if output_family:
                output_families.add(output_family)

    return {
        "output_families": sorted(output_families),
        "entries": sorted(entries),
        "evidence_signals": sorted(evidence_signals),
    }


def _review_guidance(
    diff: Mapping[str, Sequence[str]],
    affected: Mapping[str, Sequence[str]],
    privacy: Mapping[str, Sequence[str]],
    *,
    current_snapshot: Mapping[str, Any] | None,
    expected_snapshot: Mapping[str, Any] | None,
    status: str,
) -> dict[str, list[str]]:
    entry_records = _entry_records(current_snapshot, expected_snapshot)
    modules: list[str] = []
    tests: list[str] = []
    unresolved_entries: list[str] = []
    for entry_id in affected["entries"]:
        entry = entry_records.get(entry_id)
        if entry is None:
            unresolved_entries.append(entry_id)
            continue
        modules.extend(_safe_string_list(entry.get("recommended_review_modules")))
        tests.extend(_safe_string_list(entry.get("tests")))

    has_diff = any(diff[key] for key in DIFF_KEYS)
    if unresolved_entries or (has_diff and not modules and not tests):
        modules.extend(GENERIC_REVIEW_MODULES)
        tests.extend(GENERIC_REVIEW_TESTS)
    if diff["changed_vocabulary"]:
        modules.append("docs/contracts/player_log_evidence_ledger_schema.md")
    if any(diff[key] for key in OUTPUT_FAMILY_DIFF_KEYS):
        modules.append("docs/contracts/player_log_evidence_ledger.md")
    if _has_privacy_findings(privacy):
        modules.append("src/mythic_edge_parser/app/evidence_schema_snapshot.py")
        tests.append("tests/test_evidence_schema_snapshot.py")

    review_notes: list[str] = []
    if status == "review":
        review_notes.extend(
            [
                "Snapshot comparison reported schema drift; human review is required before any snapshot update.",
                "This report is review evidence only, not merge readiness, deploy readiness, or tracker completion.",
            ],
        )
    elif status == "fail":
        review_notes.append(
            "Schema drift report input could not be trusted; inspect status_reasons and privacy findings.",
        )
    if unresolved_entries:
        review_notes.append(
            "Some affected entries were not present in supplied snapshots; generic review targets were used.",
        )

    return {
        "recommended_review_modules": sorted(set(modules)),
        "recommended_tests": sorted(set(tests)),
        "review_notes": review_notes,
    }


def _drift_flags(
    comparison: Mapping[str, Any],
    *,
    diff: Mapping[str, Sequence[str]],
    malformed: bool,
    privacy: Mapping[str, Sequence[str]],
    limitations: Sequence[str],
) -> list[str]:
    flags = _safe_string_list(comparison.get("drift_flags"), drop_sensitive=_has_privacy_findings(privacy))
    if any(diff[key] for key in DIFF_KEYS):
        flags.append("changed_signal_type")
    if malformed or limitations:
        flags.append("schema_snapshot_missing")
    if _has_privacy_findings(privacy):
        flags.append("sensitive_evidence_redacted")
    if diff["removed_entries"] or diff["removed_evidence_signals"]:
        flags.append("missing_expected_payload_path")
    if diff["added_entries"] or diff["added_evidence_signals"]:
        flags.append("new_unknown_payload_path")
    return _dedupe(flags)


def _entry_records(*snapshots: Mapping[str, Any] | None) -> dict[str, Mapping[str, Any]]:
    records: dict[str, Mapping[str, Any]] = {}
    for snapshot in snapshots:
        if not isinstance(snapshot, Mapping):
            continue
        entries = snapshot.get("entries")
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, Mapping):
                continue
            entry_id = _safe_text(entry.get("entry_id"))
            if entry_id:
                records.setdefault(entry_id, entry)
    return records


def _entry_id_from_signal_key(signal_key: str) -> str:
    return signal_key.split(":", 1)[0] if ":" in signal_key else ""


def _entry_id_from_policy_key(policy_key: str) -> str:
    for suffix in ENTRY_POLICY_SUFFIXES:
        if policy_key.endswith(suffix):
            return policy_key[: -len(suffix)]
    return ""


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


def _merge_privacy_findings(
    comparison_privacy: Mapping[str, Sequence[str]],
    input_privacy: Mapping[str, Sequence[str]],
) -> dict[str, list[str]]:
    return {
        "forbidden_content_findings": _dedupe(
            [
                *comparison_privacy.get("forbidden_content_findings", ()),
                *input_privacy.get("forbidden_content_findings", ()),
            ],
        ),
        "local_absolute_paths_found": _dedupe(
            [
                *comparison_privacy.get("local_absolute_paths_found", ()),
                *input_privacy.get("local_absolute_paths_found", ()),
            ],
        ),
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


def _safe_text(value: Any) -> str:
    text = str(value or "")
    if _contains_forbidden_content(text):
        return ""
    return text


def _safe_string_list(value: Any, *, drop_sensitive: bool = False) -> list[str]:
    if not isinstance(value, list | tuple):
        return []
    result: list[str] = []
    for item in value:
        text = str(item)
        if drop_sensitive and _contains_forbidden_content(text):
            continue
        result.append(_safe_text(text))
    return sorted(text for text in _dedupe(result) if text)


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list | tuple):
        return []
    return [str(item) for item in value]


def _contains_forbidden_content(text: str) -> bool:
    return bool(
        evidence_schema_snapshot.LOCAL_ABSOLUTE_PATH_RE.search(text)
        or evidence_schema_snapshot.FORBIDDEN_VALUE_RE.search(text)
        or any(snippet in text for snippet in evidence_schema_snapshot.FORBIDDEN_VALUE_SNIPPETS)
    )


def _encode_report(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _write_markdown_report(path: Path, report: Mapping[str, Any]) -> None:
    findings = _privacy_findings(report, "report")
    combined = findings["forbidden_content_findings"] + findings["local_absolute_paths_found"]
    if combined:
        raise ValueError(f"forbidden evidence schema drift report content: {', '.join(combined)}")
    lines = [
        "# Player.log Evidence Ledger Schema Drift Report",
        "",
        f"- status: {report.get('status', '')}",
        f"- review_required: {str(report.get('review_required', False)).lower()}",
        f"- affected_entries: {len((report.get('affected') or {}).get('entries', []))}",
        f"- affected_output_families: {len((report.get('affected') or {}).get('output_families', []))}",
        "",
        (
            "This report is review evidence only. It does not decide merge readiness, deploy readiness, "
            "or tracker closure."
        ),
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _dedupe(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


if __name__ == "__main__":
    raise SystemExit(main())
