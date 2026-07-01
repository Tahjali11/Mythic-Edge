from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "tools" / "check_cwe_mapped_local_validation_profile.py"
)
SPEC = importlib.util.spec_from_file_location("check_cwe_mapped_local_validation_profile", MODULE_PATH)
assert SPEC is not None
profile_checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = profile_checker
assert SPEC.loader is not None
SPEC.loader.exec_module(profile_checker)

PROFILE_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "security"
    / "cwe_mapped_local_validation_profile.v1.json"
)


def _load_profile() -> dict:
    return profile_checker.load_profile(PROFILE_PATH)


def _family(profile: dict, family_id: str) -> dict:
    for item in profile["families"]:
        if item["family_id"] == family_id:
            return item
    raise AssertionError(f"missing family {family_id}")


def _validate(profile: dict) -> profile_checker.ValidationResult:
    return profile_checker.validate_profile(profile, profile_path=str(PROFILE_PATH))


def test_manifest_validates_with_exact_v1_family_set() -> None:
    profile = _load_profile()

    result = _validate(profile)

    assert result.passed
    assert result.family_count == 7
    assert {family["family_id"] for family in profile["families"]} == set(
        profile_checker.EXPECTED_PRIMARY_CWES,
    )


def test_cli_reports_public_safe_success(capsys: pytest.CaptureFixture[str]) -> None:
    assert profile_checker.main([str(PROFILE_PATH)]) == 0

    captured = capsys.readouterr()
    assert "CWE-Mapped Local Validation Profile" in captured.out
    assert "families: 7" in captured.out
    assert "result: passed" in captured.out
    assert "C:\\Users\\" not in captured.out


def test_rejects_missing_family() -> None:
    profile = _load_profile()
    profile["families"] = profile["families"][:-1]

    result = _validate(profile)

    assert not result.passed
    assert any(issue.code == "cwe_mapping_missing" for issue in result.errors)


@pytest.mark.parametrize(
    "field",
    [
        "ci_change_authorized",
        "enforcement_authorized",
        "codeql_alert_mutation_authorized",
        "parser_behavior_change_authorized",
        "security_assurance_claimed",
        "privacy_assurance_claimed",
    ],
)
def test_rejects_authorized_or_assurance_flags(field: str) -> None:
    profile = _load_profile()
    profile[field] = True

    result = _validate(profile)

    assert not result.passed
    assert any(
        issue.code
        in {
            "enforcement_not_authorized",
            "codeql_alert_mutation_not_authorized",
            "security_assurance_not_authorized",
        }
        for issue in result.errors
    )


@pytest.mark.parametrize("status", ["blocking_candidate", "blocking_enabled"])
def test_rejects_blocking_profile_status(status: str) -> None:
    profile = _load_profile()
    profile["profile_status"] = status

    result = _validate(profile)

    assert not result.passed
    assert any(issue.code == "enforcement_not_authorized" for issue in result.errors)


def test_rejects_blocking_family_rollout_status() -> None:
    profile = _load_profile()
    _family(profile, "local_path_traversal")["rollout_status"] = "blocking_enabled"

    result = _validate(profile)

    assert not result.passed
    assert any(issue.code == "enforcement_not_authorized" for issue in result.errors)


@pytest.mark.parametrize(
    ("family_id", "primary_cwe_id"),
    [
        ("url_host_validation", "CWE-20"),
        ("secret_private_artifact_exposure", "CWE-200"),
        ("workflow_permission_scope", "CWE-275"),
    ],
)
def test_rejects_broad_or_prohibited_primary_cwe(family_id: str, primary_cwe_id: str) -> None:
    profile = _load_profile()
    _family(profile, family_id)["primary_cwe_id"] = primary_cwe_id

    result = _validate(profile)

    assert not result.passed
    assert any(issue.code == "cwe_mapping_prohibited" for issue in result.errors)


@pytest.mark.parametrize(
    ("family_id", "expected_provenance"),
    [
        ("url_host_validation", "CWE-20"),
        ("secret_private_artifact_exposure", "CWE-200"),
        ("workflow_permission_scope", "CWE-275"),
    ],
)
def test_requires_discouraged_scanner_provenance_to_stay_separate(
    family_id: str,
    expected_provenance: str,
) -> None:
    profile = _load_profile()
    family = _family(profile, family_id)
    assert expected_provenance in family["scanner_cwe_provenance"]
    family["discouraged_or_prohibited_cwe_provenance"] = []

    result = _validate(profile)

    assert not result.passed
    assert any(issue.code == "cwe_mapping_discouraged_provenance_missing" for issue in result.errors)


def test_rejects_placeholder_or_invented_mapping_status() -> None:
    profile = _load_profile()
    _family(profile, "temporary_file_handling")["mapping_review_status"] = (
        "rejected_placeholder_or_invented"
    )

    result = _validate(profile)

    assert not result.passed
    assert any(issue.code == "cwe_mapping_prohibited" for issue in result.errors)


def test_rejects_local_absolute_paths_without_echoing_private_value() -> None:
    profile = _load_profile()
    raw_private_path = "\\".join(
        ["C:", "Users", "Local Operator", "AppData", "Local", "MythicEdge", "private.json"],
    )
    _family(profile, "secret_private_artifact_exposure")["allowed_evidence"].append(raw_private_path)

    result = _validate(profile)
    report = profile_checker.render_report(result)

    assert not result.passed
    assert any(issue.code == "unsafe_report_output" for issue in result.errors)
    assert raw_private_path not in report
    assert "Local Operator" not in report


@pytest.mark.parametrize(
    "raw_private_path",
    [
        "\\".join(["D:", "scanner", "evidence", "profile.json"]),
        "/".join(["E:", "advisory", "manifest", "profile.json"]),
    ],
)
def test_rejects_non_user_windows_absolute_paths_without_echoing_value(
    raw_private_path: str,
) -> None:
    profile = _load_profile()
    _family(profile, "local_path_traversal")["forbidden_evidence"].append(raw_private_path)

    result = _validate(profile)
    report = profile_checker.render_report(result)

    assert not result.passed
    assert any(issue.code == "unsafe_report_output" for issue in result.errors)
    assert raw_private_path not in report


def test_rejects_live_webhook_url_without_echoing_value() -> None:
    profile = _load_profile()
    raw_url = (
        "https://script.google.com/"
        + "macros/s/"
        + "AKfycbexampleexampleexampleexampleexample"
        + "/exec"
    )
    _family(profile, "url_host_validation")["forbidden_evidence"].append(raw_url)

    result = _validate(profile)
    report = profile_checker.render_report(result)

    assert not result.passed
    assert any(issue.code == "unsafe_report_output" for issue in result.errors)
    assert raw_url not in report


def test_profile_fixture_mutation_does_not_modify_loaded_manifest() -> None:
    profile = _load_profile()
    mutated = copy.deepcopy(profile)
    mutated["families"][0]["family_id"] = "unknown_family"

    assert not _validate(mutated).passed
    assert _validate(profile).passed
