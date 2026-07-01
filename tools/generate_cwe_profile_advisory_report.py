"""Generate the advisory CWE-mapped local validation profile report."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import check_cwe_mapped_local_validation_profile as profile_checker  # noqa: E402

REPORT_SCHEMA_VERSION = "security_cwe_mapped_local_validation_profile_advisory_report.v1"
REPOSITORY = "Tahjali11/Mythic-Edge"
REPOSITORY_URL = "https://github.com/Tahjali11/Mythic-Edge"
CONTRACT_REF = "docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md"
SOURCE_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/603"
PARENT_ISSUE = "https://github.com/Tahjali11/Mythic-Edge/issues/330"
SOURCE_PROFILE_CONTRACT = "docs/contracts/security_cwe_mapped_local_validation_profile.md"
SOURCE_PROFILE_MANIFEST = "docs/security/cwe_mapped_local_validation_profile.v1.json"
SOURCE_VALIDATOR = "tools/check_cwe_mapped_local_validation_profile.py"
REPORT_HELPER = "tools/generate_cwe_profile_advisory_report.py"
REPORT_DIR = Path("docs/quality_reports/security/cwe_mapped_local_validation_profile")
DEFAULT_NEXT_ROLE = "Codex E: Module Reviewer / contract-test thread"

ALLOWED_RUN_MODES = {"manifest_validator_advisory", "contract_review_only", "unsupported_input_blocked"}
SUPPORTED_RUN_MODES = {"manifest_validator_advisory"}

NON_CLAIMS = (
    "This report is advisory local validation evidence only.",
    "This report does not mutate, dismiss, reopen, or close CodeQL alerts.",
    "This report does not prove that CodeQL has zero open alerts.",
    "This report is not formal CWE compliance.",
    "This report is not security assurance.",
    "This report is not privacy assurance.",
    "This report is not release readiness.",
    "This report is not deploy readiness.",
    "This report is not CI enforcement.",
    "This report is not parser truth, analytics truth, AI truth, or coaching truth.",
    (
        "This report does not authorize production, workbook, webhook, Apps Script, Google Sheets, "
        "OpenAI, model-provider, Line Tracer, or coaching behavior changes."
    ),
)

BLOCKED_ITEMS = (
    "local_scanner_outputs",
    "raw_sarif_files",
    "codeql_api_responses",
    "private_evidence_packets",
    "raw_logs",
    "local_app_data",
    "sqlite_contents",
    "secrets_or_credentials",
    "endpoint_values",
    "workbook_exports",
    "transport_failure_artifacts",
    "runtime_logs",
    "private_decklists",
    "arbitrary_user_files",
)

VALIDATION_COMMANDS = (
    r"py -m pytest -q tests\test_cwe_mapped_local_validation_profile.py",
    r"py -m pytest -q tests\test_cwe_profile_advisory_report.py",
    r"py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json",
    (
        r"py tools\check_cwe_mapped_local_validation_profile.py "
        r"docs\security\cwe_mapped_local_validation_profile.v1.json"
    ),
    (
        r"py tools\generate_cwe_profile_advisory_report.py "
        r"--write-report --report-date 2026-07-01"
    ),
    r"py -m json.tool docs\quality_reports\security\cwe_mapped_local_validation_profile\<report>.json",
    r"py -m ruff check tools\generate_cwe_profile_advisory_report.py tests\test_cwe_profile_advisory_report.py",
    r"git diff --check",
    r"py tools\check_agent_docs.py",
)

UNSAFE_TEXT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("local_windows_absolute_path", re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/]+", re.IGNORECASE)),
    ("local_unix_user_path", re.compile(r"/(?:Users|home)/[^\s\"'<>]+", re.IGNORECASE)),
    ("live_google_script_url", re.compile(r"https://script\.google\.com/macros/s/", re.IGNORECASE)),
    ("private_key_marker", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----")),
    ("credential_assignment", re.compile(r"(?i)\b(api[_-]?key|token|password|secret)\b\s*[:=]\s*[^<\s][^\s,;]{7,}")),
)


@dataclass(frozen=True)
class RepoMetadata:
    measured_ref: str
    measured_commit: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _git_value(repo_root: Path, args: list[str], fallback: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return fallback
    value = completed.stdout.strip()
    return value or fallback


def read_repo_metadata(repo_root: Path | None = None) -> RepoMetadata:
    root = repo_root or _repo_root()
    return RepoMetadata(
        measured_ref=_git_value(root, ["branch", "--show-current"], "unknown"),
        measured_commit=_git_value(root, ["rev-parse", "HEAD"], "unknown"),
    )


def _contains_unsafe_text(text: str) -> bool:
    return any(pattern.search(text) for _, pattern in UNSAFE_TEXT_PATTERNS)


def _safe_text(text: Any) -> str:
    if not isinstance(text, str):
        return "<redacted>"
    if _contains_unsafe_text(text):
        return "<redacted>"
    return text


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [_safe_text(item) for item in value if isinstance(item, str)]


def _issue_to_dict(issue: profile_checker.ProfileIssue) -> dict[str, str]:
    return {
        "code": _safe_text(issue.code),
        "location": _safe_text(issue.location),
        "message": _safe_text(issue.message),
    }


def _validator_status(result: profile_checker.ValidationResult) -> str:
    return "passed" if result.passed else "failed"


def _overall_status(result: profile_checker.ValidationResult) -> str:
    if result.errors:
        return "failed_advisory"
    if result.warnings:
        return "warning_advisory"
    return "passed_advisory"


def _family_report(family: dict[str, Any]) -> dict[str, Any]:
    return {
        "family_id": _safe_text(family.get("family_id")),
        "primary_cwe_id": _safe_text(family.get("primary_cwe_id")),
        "primary_cwe_title": _safe_text(family.get("primary_cwe_title")),
        "mapping_review_status": _safe_text(family.get("mapping_review_status")),
        "rollout_status": _safe_text(family.get("rollout_status")),
        "codeql_rule_ids": _safe_string_list(family.get("codeql_rule_ids")),
        "local_detector_ids": _safe_string_list(family.get("local_detector_ids")),
        "reporting_policy": _safe_text(family.get("reporting_policy")),
        "non_claims": _safe_string_list(family.get("non_claims")),
    }


def _empty_blocked_validator() -> dict[str, Any]:
    return {
        "tool": SOURCE_VALIDATOR,
        "result": "blocked",
        "exit_code": 2,
        "errors_count": 0,
        "warnings_count": 0,
        "errors": [],
        "warnings": [],
    }


def _blocked_report(
    *,
    run_mode: str,
    overall_status: str,
    measured_ref: str,
    measured_commit: str,
) -> dict[str, Any]:
    safe_run_mode = run_mode if run_mode in ALLOWED_RUN_MODES else "unsupported_input_blocked"
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_id": f"cwe-profile-advisory-report:{_safe_text(measured_commit)[:7]}:{safe_run_mode}",
        "repository": REPOSITORY,
        "repository_url": REPOSITORY_URL,
        "contract_ref": CONTRACT_REF,
        "source_issue": SOURCE_ISSUE,
        "parent_issue": PARENT_ISSUE,
        "source_profile_contract": SOURCE_PROFILE_CONTRACT,
        "source_profile_manifest": SOURCE_PROFILE_MANIFEST,
        "source_validator": SOURCE_VALIDATOR,
        "measured_ref": _safe_text(measured_ref),
        "measured_commit": _safe_text(measured_commit),
        "generated_at_policy": "manual_or_test_only",
        "run_mode": safe_run_mode,
        "overall_status": overall_status,
        "profile_status": "unknown",
        "profile_family_count": 0,
        "families": [],
        "validator": _empty_blocked_validator(),
        "blocked_items": list(BLOCKED_ITEMS),
        "non_claims": list(NON_CLAIMS),
        "privacy_redaction": {
            "policy": "repo_relative_and_symbolic_only",
            "redacted_placeholder": "<redacted>",
            "unsafe_input_echoed": False,
            "raw_private_values_included": False,
        },
        "advisory_only": True,
        "enforcement_authorized": False,
        "ci_change_authorized": False,
        "codeql_alert_mutation_authorized": False,
        "security_assurance_claimed": False,
        "privacy_assurance_claimed": False,
        "validation_commands": list(VALIDATION_COMMANDS),
        "next_recommended_role": DEFAULT_NEXT_ROLE,
    }


def build_report(
    profile: dict[str, Any],
    validation_result: profile_checker.ValidationResult,
    *,
    measured_ref: str,
    measured_commit: str,
    run_mode: str = "manifest_validator_advisory",
) -> dict[str, Any]:
    if run_mode not in SUPPORTED_RUN_MODES:
        return _blocked_report(
            run_mode=run_mode,
            overall_status="blocked_unsupported_mode",
            measured_ref=measured_ref,
            measured_commit=measured_commit,
        )

    families = profile.get("families")
    family_reports = [_family_report(family) for family in families] if isinstance(families, list) else []

    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_id": f"cwe-profile-advisory-report:{_safe_text(measured_commit)[:7]}:{run_mode}",
        "repository": REPOSITORY,
        "repository_url": REPOSITORY_URL,
        "contract_ref": CONTRACT_REF,
        "source_issue": SOURCE_ISSUE,
        "parent_issue": PARENT_ISSUE,
        "source_profile_contract": SOURCE_PROFILE_CONTRACT,
        "source_profile_manifest": SOURCE_PROFILE_MANIFEST,
        "source_validator": SOURCE_VALIDATOR,
        "measured_ref": _safe_text(measured_ref),
        "measured_commit": _safe_text(measured_commit),
        "generated_at_policy": "manual_or_test_only",
        "run_mode": run_mode,
        "overall_status": _overall_status(validation_result),
        "profile_status": _safe_text(profile.get("profile_status")),
        "profile_family_count": validation_result.family_count,
        "families": family_reports,
        "validator": {
            "tool": SOURCE_VALIDATOR,
            "result": _validator_status(validation_result),
            "exit_code": validation_result.exit_code,
            "errors_count": len(validation_result.errors),
            "warnings_count": len(validation_result.warnings),
            "errors": [_issue_to_dict(issue) for issue in validation_result.errors],
            "warnings": [_issue_to_dict(issue) for issue in validation_result.warnings],
        },
        "blocked_items": list(BLOCKED_ITEMS),
        "non_claims": list(NON_CLAIMS),
        "privacy_redaction": {
            "policy": "repo_relative_and_symbolic_only",
            "redacted_placeholder": "<redacted>",
            "unsafe_input_echoed": False,
            "raw_private_values_included": False,
        },
        "advisory_only": True,
        "enforcement_authorized": False,
        "ci_change_authorized": False,
        "codeql_alert_mutation_authorized": False,
        "security_assurance_claimed": False,
        "privacy_assurance_claimed": False,
        "validation_commands": list(VALIDATION_COMMANDS),
        "next_recommended_role": DEFAULT_NEXT_ROLE,
    }


def default_report_path(report_date: str, measured_commit: str) -> Path:
    short_commit = _safe_text(measured_commit)[:7] or "unknown"
    return REPORT_DIR / f"{report_date}-{short_commit}-cwe-profile-advisory-report.json"


def _json_text(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True) + "\n"


def _is_default_profile_path(profile_path: Path, repo_root: Path) -> bool:
    try:
        return profile_path.resolve() == (repo_root / SOURCE_PROFILE_MANIFEST).resolve()
    except OSError:
        return False


def generate_report(
    *,
    profile_path: Path | None = None,
    run_mode: str = "manifest_validator_advisory",
    repo_root: Path | None = None,
) -> dict[str, Any]:
    root = repo_root or _repo_root()
    metadata = read_repo_metadata(root)
    candidate_profile = profile_path or (root / SOURCE_PROFILE_MANIFEST)

    if not _is_default_profile_path(candidate_profile, root):
        return _blocked_report(
            run_mode="unsupported_input_blocked",
            overall_status="blocked_unsafe_input",
            measured_ref=metadata.measured_ref,
            measured_commit=metadata.measured_commit,
        )
    if run_mode not in SUPPORTED_RUN_MODES:
        return _blocked_report(
            run_mode=run_mode,
            overall_status="blocked_unsupported_mode",
            measured_ref=metadata.measured_ref,
            measured_commit=metadata.measured_commit,
        )

    try:
        profile = profile_checker.load_profile(candidate_profile)
    except (OSError, ValueError, json.JSONDecodeError):
        return _blocked_report(
            run_mode=run_mode,
            overall_status="blocked_validator_unavailable",
            measured_ref=metadata.measured_ref,
            measured_commit=metadata.measured_commit,
        )

    validation_result = profile_checker.validate_profile(profile, profile_path=SOURCE_PROFILE_MANIFEST)
    return build_report(
        profile,
        validation_result,
        measured_ref=metadata.measured_ref,
        measured_commit=metadata.measured_commit,
        run_mode=run_mode,
    )


def write_default_report(report: dict[str, Any], *, report_date: str, repo_root: Path | None = None) -> Path:
    root = repo_root or _repo_root()
    output_path = root / default_report_path(report_date, str(report.get("measured_commit", "unknown")))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_json_text(report), encoding="utf-8")
    return output_path.relative_to(root)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        type=Path,
        default=None,
        help="Profile manifest path; only the default repo profile is supported.",
    )
    parser.add_argument("--mode", default="manifest_validator_advisory", help="Report run mode.")
    parser.add_argument("--write-report", action="store_true", help="Write the deterministic default report artifact.")
    parser.add_argument(
        "--report-date",
        default=datetime.now(UTC).date().isoformat(),
        help="Report artifact date in YYYY-MM-DD format.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    report = generate_report(profile_path=args.profile, run_mode=args.mode)
    if args.write_report:
        output_path = write_default_report(report, report_date=args.report_date)
        print(output_path.as_posix())
    else:
        print(_json_text(report), end="")
    return 0 if report["overall_status"] in {"passed_advisory", "warning_advisory"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
