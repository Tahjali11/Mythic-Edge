from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

TOOLS_DIR = Path(__file__).resolve().parents[1] / "tools"
MODULE_PATH = TOOLS_DIR / "generate_security_quality_summary.py"
SPEC = importlib.util.spec_from_file_location("generate_security_quality_summary", MODULE_PATH)
assert SPEC is not None
reporter = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reporter
assert SPEC.loader is not None
SPEC.loader.exec_module(reporter)

CURRENT_REF = "codex/security-summary-aggregation-330"
CURRENT_COMMIT = "503239c593dc935e7864bf15df94dae70760ff7f"
STALE_COMMIT = "024eda7000000000000000000000000000000000"


def _metadata() -> reporter.RepoMetadata:
    return reporter.RepoMetadata(measured_ref=CURRENT_REF, measured_commit=CURRENT_COMMIT)


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _cwe_report_payload(*, measured_commit: str = STALE_COMMIT) -> dict:
    return {
        "schema_version": "security_cwe_mapped_local_validation_profile_advisory_report.v1",
        "report_id": "cwe-profile-advisory-report:test",
        "repository": "Tahjali11/Mythic-Edge",
        "repository_url": "https://github.com/Tahjali11/Mythic-Edge",
        "contract_ref": "docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md",
        "source_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/603",
        "parent_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/330",
        "source_profile_contract": "docs/contracts/security_cwe_mapped_local_validation_profile.md",
        "source_profile_manifest": "docs/security/cwe_mapped_local_validation_profile.v1.json",
        "source_validator": "tools/check_cwe_mapped_local_validation_profile.py",
        "measured_ref": "codex/cwe-profile-advisory-report-603",
        "measured_commit": measured_commit,
        "generated_at_policy": "manual_or_test_only",
        "run_mode": "manifest_validator_advisory",
        "overall_status": "passed_advisory",
        "profile_status": "advisory_profile",
        "profile_family_count": 7,
        "families": [
            {
                "family_id": "local_path_traversal",
                "primary_cwe_id": "CWE-22",
            },
        ],
        "validator": {
            "tool": "tools/check_cwe_mapped_local_validation_profile.py",
            "result": "passed",
            "exit_code": 0,
            "errors_count": 0,
            "warnings_count": 0,
        },
        "blocked_items": ["raw_sarif_files", "codeql_api_responses"],
        "non_claims": ["This report is not security assurance."],
        "privacy_redaction": {
            "unsafe_input_echoed": False,
            "raw_private_values_included": False,
        },
        "advisory_only": True,
        "enforcement_authorized": False,
        "ci_change_authorized": False,
        "codeql_alert_mutation_authorized": False,
        "security_assurance_claimed": False,
        "privacy_assurance_claimed": False,
        "validation_commands": [],
        "next_recommended_role": "Codex E: Module Reviewer / contract-test thread",
    }


def _generate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    cwe_payload: dict | None = None,
    **kwargs: object,
) -> dict:
    monkeypatch.setattr(reporter, "read_repo_metadata", lambda repo_root=None: _metadata())
    cwe_path = _write_json(tmp_path / "cwe-report.json", cwe_payload or _cwe_report_payload())
    return reporter.generate_report(
        cwe_report_path=cwe_path,
        report_date="2026-07-01",
        repo_root=tmp_path,
        **kwargs,
    )


def test_default_report_keeps_sources_separate_and_marks_missing_inputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report = _generate(tmp_path, monkeypatch)

    assert report["schema_version"] == "security_quality_scanner_summary_aggregation.v1"
    assert report["repository"] == "Tahjali11/Mythic-Edge"
    assert report["source_issue"] == "https://github.com/Tahjali11/Mythic-Edge/issues/610"
    assert report["overall_status"] == "advisory_warnings"
    assert report["freshness_status"] == "mixed"
    assert report["advisory_only"] is True
    assert report["enforcement_authorized"] is False
    assert report["ci_change_authorized"] is False
    assert report["codeql_alert_mutation_authorized"] is False
    assert report["security_assurance_claimed"] is False
    assert report["privacy_assurance_claimed"] is False

    source_statuses = {source["source_id"]: source["status"] for source in report["sources"]}
    assert source_statuses == {
        "codeql": "not_collected",
        "cwe_profile_report": "stale",
        "protected_surface_scan": "not_collected",
        "secret_private_marker_scan": "not_collected",
        "ci_or_repo_check_status": "not_collected",
    }
    assert report["codeql"]["source_state"] == "not_collected"
    assert report["cwe_profile_report"]["freshness_status"] == "stale"
    assert report["protected_surface_scan"]["source_state"] == "not_collected"
    assert report["secret_private_marker_scan"]["source_state"] == "not_collected"


def test_codeql_summary_stays_lifecycle_evidence_not_local_scanner_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    codeql_summary = _write_json(
        tmp_path / "codeql-summary.json",
        {
            "source": "github_code_scanning",
            "repository": "Tahjali11/Mythic-Edge",
            "repository_url": "https://github.com/Tahjali11/Mythic-Edge",
            "ref": "refs/heads/main",
            "analysis_commit": CURRENT_COMMIT,
            "provided_at_policy": "codex_g_public_safe_summary",
            "state_counts": {"open": 0, "fixed": 16, "dismissed": 0},
            "severity_counts": {"critical": 0, "high": 0},
            "rule_id_counts": {"py/path-injection": 0},
            "tool_name": "CodeQL",
            "source_url": "https://github.com/Tahjali11/Mythic-Edge/security/code-scanning",
            "freshness_status": "current",
        },
    )

    report = _generate(
        tmp_path,
        monkeypatch,
        cwe_payload=_cwe_report_payload(measured_commit=CURRENT_COMMIT),
        codeql_state_source="summary-file",
        codeql_summary_path=codeql_summary,
    )

    assert report["codeql"]["source_state"] == "provided_by_codex_g"
    assert report["codeql"]["open_count"] == 0
    assert report["codeql"]["codeql_alert_mutation_authorized"] is False
    assert report["protected_surface_scan"]["source_state"] == "not_collected"
    assert report["secret_private_marker_scan"]["source_state"] == "not_collected"
    assert "security assurance" in " ".join(report["non_claims"]).lower()


def test_raw_codeql_payload_fields_are_blocked_without_echoing_private_values(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    private_path = "\\".join(["C:", "Users", "Local Operator", "AppData", "Local", "secret.txt"])
    unsafe_summary = _write_json(
        tmp_path / "unsafe-codeql.json",
        {
            "source": "github_code_scanning",
            "repository": "Tahjali11/Mythic-Edge",
            "alerts": [{"message": "raw alert", "location": private_path}],
        },
    )

    report = _generate(
        tmp_path,
        monkeypatch,
        codeql_state_source="summary-file",
        codeql_summary_path=unsafe_summary,
    )
    encoded = json.dumps(report, sort_keys=True)

    assert report["overall_status"] == "blocked_unsafe_input"
    assert report["blocked_inputs"] == [{"source_id": "codeql", "reason": "blocked_unsafe_input"}]
    assert private_path not in encoded
    assert "Local Operator" not in encoded
    assert "raw alert" not in encoded


def test_raw_sarif_like_input_is_blocked(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    unsafe_summary = _write_json(
        tmp_path / "unsafe-sarif.json",
        {
            "source": "github_code_scanning",
            "repository": "Tahjali11/Mythic-Edge",
            "raw_sarif": {"runs": []},
        },
    )

    report = _generate(
        tmp_path,
        monkeypatch,
        codeql_state_source="summary-file",
        codeql_summary_path=unsafe_summary,
    )

    assert report["overall_status"] == "blocked_unsafe_input"
    assert report["blocked_inputs"][0]["reason"] == "blocked_unsafe_input"


def test_secret_like_field_is_blocked_without_echo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    unsafe_summary = _write_json(
        tmp_path / "unsafe-secret.json",
        {
            "tool": "tools/check_secret_patterns.py",
            "mode": "changed-path",
            "base": "origin/main",
            "head": CURRENT_COMMIT,
            "scanned_paths": 1,
            "forbidden": 0,
            "warnings": 0,
            "result": "passed",
            "freshness_status": "current",
            "symbolic_category_counts": {"token": 1},
        },
    )

    report = _generate(
        tmp_path,
        monkeypatch,
        secret_private_summary_path=unsafe_summary,
    )
    encoded = json.dumps(report, sort_keys=True)

    assert report["overall_status"] == "blocked_unsafe_input"
    assert report["blocked_inputs"] == [
        {"source_id": "secret_private_marker_scan", "reason": "blocked_unsafe_input"},
    ]
    assert "unsafe-secret.json" not in encoded


def test_stale_cwe_evidence_is_labeled_stale(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    report = _generate(tmp_path, monkeypatch)

    assert report["cwe_profile_report"]["measured_commit"] == STALE_COMMIT
    assert report["cwe_profile_report"]["freshness_status"] == "stale"
    assert any(
        source["source_id"] == "cwe_profile_report" and source["status"] == "stale"
        for source in report["sources"]
    )


def test_default_report_path_uses_date_and_short_commit() -> None:
    path = reporter.default_report_path("2026-07-01", CURRENT_COMMIT)

    assert path.as_posix() == (
        "docs/quality_reports/security/security_quality_summary/"
        "2026-07-01-503239c-security-quality-summary.json"
    )
