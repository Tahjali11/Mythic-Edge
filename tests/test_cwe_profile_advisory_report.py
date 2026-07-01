from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest

TOOLS_DIR = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

MODULE_PATH = TOOLS_DIR / "generate_cwe_profile_advisory_report.py"
SPEC = importlib.util.spec_from_file_location("generate_cwe_profile_advisory_report", MODULE_PATH)
assert SPEC is not None
reporter = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reporter
assert SPEC.loader is not None
SPEC.loader.exec_module(reporter)

PROFILE_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "security"
    / "cwe_mapped_local_validation_profile.v1.json"
)


def _load_profile() -> dict:
    return reporter.profile_checker.load_profile(PROFILE_PATH)


def _validated_report(profile: dict | None = None) -> dict:
    profile_data = profile or _load_profile()
    result = reporter.profile_checker.validate_profile(profile_data, profile_path=reporter.SOURCE_PROFILE_MANIFEST)
    return reporter.build_report(
        profile_data,
        result,
        measured_ref="codex/cwe-profile-advisory-report-603",
        measured_commit="3948e5204ae3372b6418c456297467fa8ca788bf",
    )


def test_success_report_matches_contract_schema_and_flags() -> None:
    report = _validated_report()

    assert report["schema_version"] == "security_cwe_mapped_local_validation_profile_advisory_report.v1"
    assert report["repository"] == "Tahjali11/Mythic-Edge"
    assert report["repository_url"] == "https://github.com/Tahjali11/Mythic-Edge"
    assert report["contract_ref"] == "docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md"
    assert report["source_issue"] == "https://github.com/Tahjali11/Mythic-Edge/issues/603"
    assert report["parent_issue"] == "https://github.com/Tahjali11/Mythic-Edge/issues/330"
    assert report["run_mode"] == "manifest_validator_advisory"
    assert report["overall_status"] == "passed_advisory"
    assert report["profile_status"] == "advisory_profile"
    assert report["profile_family_count"] == 7
    assert report["validator"]["result"] == "passed"
    assert report["validator"]["exit_code"] == 0
    assert report["validator"]["errors_count"] == 0
    assert report["validator"]["warnings_count"] == 0
    assert report["advisory_only"] is True
    assert report["enforcement_authorized"] is False
    assert report["ci_change_authorized"] is False
    assert report["codeql_alert_mutation_authorized"] is False
    assert report["security_assurance_claimed"] is False
    assert report["privacy_assurance_claimed"] is False
    assert "This report is not formal CWE compliance." in report["non_claims"]
    assert "raw_sarif_files" in report["blocked_items"]
    assert "codeql_api_responses" in report["blocked_items"]


def test_family_entries_are_symbolic_and_public_safe() -> None:
    report = _validated_report()
    family = next(item for item in report["families"] if item["family_id"] == "url_host_validation")

    assert set(family) == {
        "family_id",
        "primary_cwe_id",
        "primary_cwe_title",
        "mapping_review_status",
        "rollout_status",
        "codeql_rule_ids",
        "local_detector_ids",
        "reporting_policy",
        "non_claims",
    }
    assert family["primary_cwe_id"] == "CWE-187"
    assert family["codeql_rule_ids"] == ["py/incomplete-url-substring-sanitization"]

    encoded = json.dumps(report, sort_keys=True)
    assert "C:\\Users\\" not in encoded
    assert "https://script.google.com/macros/s/" not in encoded


def test_validator_errors_are_preserved_symbolically_without_raw_private_values() -> None:
    profile = _load_profile()
    raw_private_path = "\\".join(["C:", "Users", "Local Operator", "AppData", "Local", "private.json"])
    profile["families"][0]["allowed_evidence"].append(raw_private_path)

    report = _validated_report(profile)
    encoded = json.dumps(report, sort_keys=True)

    assert report["overall_status"] == "failed_advisory"
    assert report["validator"]["result"] == "failed"
    assert report["validator"]["errors_count"] >= 1
    assert any(issue["code"] == "unsafe_report_output" for issue in report["validator"]["errors"])
    assert raw_private_path not in encoded
    assert "Local Operator" not in encoded


def test_validator_warnings_are_preserved_symbolically() -> None:
    profile = _load_profile()
    result = reporter.profile_checker.ValidationResult(
        profile_path=reporter.SOURCE_PROFILE_MANIFEST,
        family_count=7,
        errors=(),
        warnings=(
            reporter.profile_checker.ProfileIssue(
                code="symbolic_warning",
                location="$.families[0]",
                message="symbolic advisory warning",
            ),
        ),
    )

    report = reporter.build_report(
        profile,
        result,
        measured_ref="codex/cwe-profile-advisory-report-603",
        measured_commit="3948e5204ae3372b6418c456297467fa8ca788bf",
    )

    assert report["overall_status"] == "warning_advisory"
    assert report["validator"]["result"] == "passed"
    assert report["validator"]["warnings_count"] == 1
    assert report["validator"]["warnings"][0] == {
        "code": "symbolic_warning",
        "location": "$.families[0]",
        "message": "symbolic advisory warning",
    }


def test_unsupported_mode_is_blocked_without_security_claims() -> None:
    profile = _load_profile()
    result = reporter.profile_checker.validate_profile(profile, profile_path=reporter.SOURCE_PROFILE_MANIFEST)

    report = reporter.build_report(
        profile,
        result,
        measured_ref="codex/cwe-profile-advisory-report-603",
        measured_commit="3948e5204ae3372b6418c456297467fa8ca788bf",
        run_mode="local_all_repo_advisory",
    )

    assert report["run_mode"] == "unsupported_input_blocked"
    assert report["overall_status"] == "blocked_unsupported_mode"
    assert report["validator"]["result"] == "blocked"
    assert report["advisory_only"] is True
    assert report["security_assurance_claimed"] is False
    assert report["privacy_assurance_claimed"] is False


def test_non_default_profile_path_is_blocked_without_echoing_raw_path(capsys: pytest.CaptureFixture[str]) -> None:
    raw_private_path = "\\".join(["C:", "Users", "Local Operator", "AppData", "Local", "profile.json"])

    exit_code = reporter.main(["--profile", raw_private_path])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert raw_private_path not in captured.out
    assert "Local Operator" not in captured.out
    payload = json.loads(captured.out)
    assert payload["overall_status"] == "blocked_unsafe_input"
    assert payload["run_mode"] == "unsupported_input_blocked"


def test_default_report_path_uses_date_and_short_commit() -> None:
    path = reporter.default_report_path("2026-07-01", "3948e5204ae3372b6418c456297467fa8ca788bf")

    assert path.as_posix() == (
        "docs/quality_reports/security/cwe_mapped_local_validation_profile/"
        "2026-07-01-3948e52-cwe-profile-advisory-report.json"
    )


def test_build_report_does_not_mutate_profile() -> None:
    profile = _load_profile()
    original = copy.deepcopy(profile)

    _validated_report(profile)

    assert profile == original
