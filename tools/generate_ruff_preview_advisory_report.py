"""Build a sanitized advisory summary from Ruff preview-mode JSON output."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import generate_ruff_advisory_report as stable_reporter

REPORT_OBJECT = "mythic_edge_quality_ruff_preview_advisory_report"
REPORT_SCHEMA_VERSION = "quality_ruff_preview_advisory_report.v1"
DEFAULT_COMMAND = (
    "py -m ruff check src tests tools --preview --select ALL --exit-zero "
    "--output-format json --output-file <local-only-raw-json>"
)

PREVIEW_CLASSIFICATIONS = {
    "candidate_exact_code",
    "watch_list",
    "style_only",
    "too_noisy",
    "protected_surface_review_required",
    "defer_until_stable",
    "not_recommended",
}
STYLE_FAMILIES = {"D", "ANN", "COM", "CPY", "E", "I", "ISC", "Q", "W"}
NOISY_FINDING_THRESHOLD = 100
NON_CLAIMS = (
    "not CI readiness",
    "not blocking-promotion readiness",
    "not parser behavior readiness",
    "not parser truth",
    "not fixture promotion readiness",
    "not corpus readiness",
    "not security assurance",
    "not privacy assurance",
    "not release readiness",
    "not deploy readiness",
    "not production readiness",
    "not analytics truth",
    "not AI truth",
    "not coaching truth",
    "not preview-mode adoption approval",
)


class RuffPreviewAdvisoryError(ValueError):
    """Raised when preview advisory input must fail closed."""


def load_rule_metadata(text: str) -> dict[str, dict[str, Any]]:
    """Load public Ruff rule metadata keyed by exact rule code."""
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuffPreviewAdvisoryError("measurement_blocked_malformed_rule_metadata") from exc
    if not isinstance(payload, list):
        raise RuffPreviewAdvisoryError("measurement_blocked_malformed_rule_metadata")

    metadata: dict[str, dict[str, Any]] = {}
    for item in payload:
        if not isinstance(item, dict):
            raise RuffPreviewAdvisoryError("measurement_blocked_malformed_rule_metadata")
        raw_code = item.get("code")
        if not isinstance(raw_code, str):
            raise RuffPreviewAdvisoryError("measurement_blocked_malformed_rule_metadata")
        code = raw_code.strip().upper()
        if not stable_reporter.is_exact_rule_code(code):
            raise RuffPreviewAdvisoryError("measurement_blocked_malformed_rule_metadata")
        metadata[code] = item
    return metadata


def build_preview_report(
    ruff_records: list[dict[str, Any]],
    *,
    rule_metadata: dict[str, dict[str, Any]],
    metadata: stable_reporter.ReportMetadata | None = None,
    measured_checkout_root: str | Path | None = None,
) -> dict[str, Any]:
    """Build a preview-specific public report from local-only Ruff output."""
    preview_rule_codes = tuple(sorted(code for code, item in rule_metadata.items() if item.get("preview") is True))
    report_metadata = metadata or stable_reporter.ReportMetadata(commands=(DEFAULT_COMMAND,))
    stable_report = stable_reporter.build_report(
        ruff_records,
        metadata=report_metadata,
        candidate_rule_codes=preview_rule_codes,
        measured_checkout_root=measured_checkout_root,
    )

    rule_summaries = [
        _preview_rule_summary(summary, rule_metadata=rule_metadata)
        for summary in stable_report["rule_summaries"]
    ]
    classification_summary = Counter(item["primary_classification"] for item in rule_summaries)
    triggered_preview_codes = [
        item["rule_code"]
        for item in rule_summaries
        if item["preview_only_rule"] and item["count"] > 0
    ]
    zero_preview_codes = [
        item["rule_code"]
        for item in rule_summaries
        if item["preview_only_rule"] and item["count"] == 0
    ]

    return {
        "object": REPORT_OBJECT,
        "schema_version": REPORT_SCHEMA_VERSION,
        "repository": stable_report["repository"],
        "repository_url": stable_report["repository_url"],
        "branch_or_ref": stable_report["branch_or_ref"],
        "commit": stable_report["commit"],
        "ruff_version": stable_report["ruff_version"],
        "scan_scope": stable_report["scan_scope"],
        "commands": stable_report["commands"],
        "exit_behavior": stable_report["exit_behavior"],
        "preview_enabled_for_measurement": True,
        "preview_enabled_in_pyproject": False,
        "preview_enabled_in_ci": False,
        "blocking_promotion_authorized": False,
        "autofix_authorized": False,
        "unsafe_fix_authorized": False,
        "totals": {
            "findings": stable_report["totals"]["findings"],
            "triggered_rule_codes": stable_report["totals"]["triggered_rule_codes"],
            "preview_only_rule_codes": len(preview_rule_codes),
            "triggered_preview_only_rule_codes": len(triggered_preview_codes),
            "zero_baseline_preview_rule_codes": len(zero_preview_codes),
        },
        "rule_summaries": rule_summaries,
        "classification_summary": dict(sorted(classification_summary.items())),
        "log004_classification": _classification_for_code(rule_summaries, "LOG004"),
        "non_claims": list(NON_CLAIMS),
    }


def _preview_rule_summary(
    stable_summary: dict[str, Any],
    *,
    rule_metadata: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    code = stable_summary["rule_code"]
    preview_only = rule_metadata.get(code, {}).get("preview") is True
    classification = _classify_preview_rule(stable_summary, preview_only=preview_only)
    secondary_labels = _secondary_labels(stable_summary, preview_only=preview_only)
    summary = {
        "rule_code": code,
        "rule_family": stable_summary["rule_family"],
        "count": stable_summary["count"],
        "affected_file_count": stable_summary["affected_file_count"],
        "affected_path_families": _affected_path_families(stable_summary),
        "autofix_available": stable_summary["autofix_available"],
        "unsafe_fix_available": stable_summary["unsafe_fix_available"],
        "protected_surface_impact": stable_summary["protected_surface_impact"],
        "preview_only_rule": preview_only,
        "preview_rule_status": "preview" if preview_only else "stable_or_non_preview",
        "primary_classification": classification,
        "secondary_labels": secondary_labels,
        "reason": _reason_for(classification, preview_only=preview_only, count=stable_summary["count"]),
    }
    if stable_summary.get("omitted_affected_path_count"):
        summary["omitted_affected_path_count"] = stable_summary["omitted_affected_path_count"]
        summary["path_handling_policy"] = stable_summary["path_handling_policy"]
        summary["path_omission_reason"] = stable_summary["path_omission_reason"]
        summary["path_scope_buckets"] = stable_summary["path_scope_buckets"]
    return summary


def _classify_preview_rule(stable_summary: dict[str, Any], *, preview_only: bool) -> str:
    count = stable_summary["count"]
    if stable_summary["protected_surface_impact"] != "none":
        return "protected_surface_review_required"
    if preview_only and count == 0:
        return "defer_until_stable"
    if count > NOISY_FINDING_THRESHOLD:
        return "too_noisy"
    if stable_summary["rule_family"] in STYLE_FAMILIES:
        return "style_only"
    if preview_only:
        return "watch_list"
    if count == 0:
        return "candidate_exact_code"
    return "watch_list"


def _affected_path_families(stable_summary: dict[str, Any]) -> list[str]:
    families = {path.split("/", 1)[0] for path in stable_summary.get("affected_paths", [])}
    families.update(stable_summary.get("path_scope_buckets", []))
    return sorted(families)


def _secondary_labels(stable_summary: dict[str, Any], *, preview_only: bool) -> list[str]:
    labels: set[str] = set()
    family = stable_summary["rule_family"]
    protected_surface = stable_summary["protected_surface_impact"]
    if preview_only:
        labels.add("preview_only")
    if family in {"LOG", "G"}:
        labels.add("logging_visibility")
    if family in {"S"}:
        labels.add("security_adjacent")
    if family in {"B", "BLE", "DTZ", "PERF", "PL", "TRY", "RUF"}:
        labels.add("runtime_safety")
    if family in STYLE_FAMILIES:
        labels.add("style_or_documentation")
    if protected_surface != "none":
        labels.add(protected_surface)
    if stable_summary["count"] > NOISY_FINDING_THRESHOLD:
        labels.add("high_volume")
    return sorted(labels)


def _reason_for(classification: str, *, preview_only: bool, count: int) -> str:
    if classification == "protected_surface_review_required":
        return "Findings touch protected surfaces and need a dedicated contract before cleanup or promotion."
    if classification == "defer_until_stable":
        return "Preview-only rule is measured for awareness but deferred until Ruff stabilizes the rule."
    if classification == "too_noisy":
        return "Finding volume is too high for a preview-mode promotion slice."
    if classification == "style_only":
        return "Rule is mainly style or documentation oriented and is lower priority for current hardening."
    if classification == "candidate_exact_code":
        return "Stable exact code has zero findings in this report and may be considered by a later contract."
    if classification == "watch_list" and preview_only:
        return "Preview-only rule is worth monitoring but is not stable blocking-ready."
    if classification == "watch_list" and count:
        return "Rule has advisory findings and must not block without cleanup and review."
    if classification == "not_recommended":
        return "Rule is not aligned with current Mythic Edge conventions."
    raise RuffPreviewAdvisoryError("unsupported_preview_classification")


def _classification_for_code(rule_summaries: list[dict[str, Any]], code: str) -> dict[str, Any]:
    for summary in rule_summaries:
        if summary["rule_code"] == code:
            return {
                "rule_code": code,
                "count": summary["count"],
                "primary_classification": summary["primary_classification"],
                "preview_only_rule": summary["preview_only_rule"],
                "reason": summary["reason"],
            }
    return {
        "rule_code": code,
        "count": 0,
        "primary_classification": "defer_until_stable",
        "preview_only_rule": True,
        "reason": "Preview-only rule was not present in Ruff metadata output for this measurement.",
    }


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True) + "\n"


def _read_text(path_text: str) -> str:
    if path_text == "-":
        return sys.stdin.read()
    try:
        return Path(path_text).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise RuffPreviewAdvisoryError("measurement_blocked_input_unreadable") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a sanitized Ruff preview advisory summary.")
    parser.add_argument("--input", default="-", help="Path to Ruff preview JSON output, or '-' for stdin.")
    parser.add_argument("--rule-metadata-input", required=True, help="Path to `ruff rule --all --output-format json`.")
    parser.add_argument("--repository", default=stable_reporter.DEFAULT_REPOSITORY)
    parser.add_argument("--repository-url", default=stable_reporter.DEFAULT_REPOSITORY_URL)
    parser.add_argument("--branch-or-ref", default="unknown")
    parser.add_argument("--commit", default="unknown")
    parser.add_argument("--ruff-version", default="unknown")
    parser.add_argument("--scan-scope", nargs="+", default=list(stable_reporter.DEFAULT_SCAN_SCOPE))
    parser.add_argument("--command", action="append", help="Advisory Ruff command that produced the input.")
    parser.add_argument(
        "--measured-checkout-root",
        type=Path,
        default=None,
        help="Measured checkout root used only to normalize Ruff diagnostic filenames.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        metadata = stable_reporter.ReportMetadata(
            repository=args.repository,
            repository_url=args.repository_url,
            branch_or_ref=args.branch_or_ref,
            commit=args.commit,
            ruff_version=args.ruff_version,
            scan_scope=tuple(args.scan_scope),
            commands=tuple(args.command or ()) or (DEFAULT_COMMAND,),
        )
        records = stable_reporter.load_ruff_json(_read_text(args.input))
        rule_metadata = load_rule_metadata(_read_text(args.rule_metadata_input))
        report = build_preview_report(
            records,
            rule_metadata=rule_metadata,
            metadata=metadata,
            measured_checkout_root=args.measured_checkout_root,
        )
    except (
        OSError,
        json.JSONDecodeError,
        stable_reporter.RuffAdvisoryError,
        RuffPreviewAdvisoryError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(render_json(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
