from __future__ import annotations

import copy
import json

import pytest

from mythic_edge_parser.app import evidence_schema_drift_report as drift_report
from mythic_edge_parser.app import evidence_schema_snapshot as snapshot_builder


def _pass_payloads() -> tuple[dict, dict, dict]:
    current = snapshot_builder.build_evidence_schema_snapshot()
    expected = copy.deepcopy(current)
    comparison = snapshot_builder.compare_evidence_schema_snapshot(current, expected)
    return comparison, current, expected


def test_pass_comparison_produces_pass_report() -> None:
    comparison, current, expected = _pass_payloads()

    report = drift_report.build_evidence_schema_drift_report(
        comparison,
        current_snapshot=current,
        expected_snapshot=expected,
    )

    assert report["object"] == drift_report.EVIDENCE_SCHEMA_DRIFT_REPORT_OBJECT
    assert report["schema_version"] == drift_report.EVIDENCE_SCHEMA_DRIFT_REPORT_VERSION
    assert report["status"] == "pass"
    assert report["review_required"] is False
    assert report["status_reasons"] == []
    assert report["summary"]["entry_changes"] == 0
    assert report["summary"]["recommended_review_module_count"] == 0
    assert report["affected"] == {
        "output_families": [],
        "entries": [],
        "evidence_signals": [],
    }
    assert all(value is False for value in report["protected_surface_assertions"].values())


def test_diff_comparison_produces_review_report_with_affected_surfaces_and_entry_guidance() -> None:
    current = snapshot_builder.build_evidence_schema_snapshot()
    expected = copy.deepcopy(current)
    expected["output_families"][0]["status"] = "registered_future"
    expected["entries"][0]["output_field"] = "old_match_id"
    expected["entries"][1]["value_source_policy"]["direct"] = "synthetic_old_source"
    expected["evidence_signals"][0]["normalized_payload_path"] = "payload.old_match_id"
    comparison = snapshot_builder.compare_evidence_schema_snapshot(current, expected)

    report = drift_report.build_evidence_schema_drift_report(
        comparison,
        current_snapshot=current,
        expected_snapshot=expected,
    )

    assert report["status"] == "review"
    assert report["review_required"] is True
    assert report["status_reasons"] == ["snapshot_comparison_diff"]
    assert report["drift"]["changed_output_families"] == comparison["diff"]["changed_output_families"]
    assert report["drift"]["changed_entries"] == comparison["diff"]["changed_entries"]
    assert report["drift"]["changed_evidence_signals"] == comparison["diff"]["changed_evidence_signals"]
    assert report["drift"]["changed_policies"] == comparison["diff"]["changed_policies"]
    assert current["entries"][0]["entry_id"] in report["affected"]["entries"]
    assert current["entries"][1]["entry_id"] in report["affected"]["entries"]
    assert current["output_families"][0]["output_family"] in report["affected"]["output_families"]
    assert current["entries"][0]["recommended_review_modules"][0] in report["review_guidance"][
        "recommended_review_modules"
    ]
    assert current["entries"][0]["tests"][0] in report["review_guidance"]["recommended_tests"]
    assert "changed_signal_type" in report["drift_flags"]


def test_fail_comparison_produces_fail_report() -> None:
    comparison, _current, _expected = _pass_payloads()
    comparison["status"] = "fail"
    comparison["limitations"] = ["expected snapshot could not be read: OSError"]
    comparison["drift_flags"] = ["schema_snapshot_missing"]

    report = drift_report.build_evidence_schema_drift_report(comparison)

    assert report["status"] == "fail"
    assert report["review_required"] is True
    assert report["status_reasons"] == ["snapshot_comparison_fail"]
    assert "schema_snapshot_missing" in report["drift_flags"]


def test_malformed_comparison_input_produces_fail_report_without_uncaught_exception() -> None:
    report = drift_report.build_evidence_schema_drift_report({"status": "pass"})

    assert report["status"] == "fail"
    assert "malformed_comparison" in report["status_reasons"]
    assert report["limitations"] == ["comparison input is malformed"]


def test_unknown_comparison_status_produces_fail_report() -> None:
    comparison, _current, _expected = _pass_payloads()
    comparison["status"] = "surprise"

    report = drift_report.build_evidence_schema_drift_report(comparison)

    assert report["status"] == "fail"
    assert "unknown_comparison_status" in report["status_reasons"]


def test_report_derives_affected_entries_from_evidence_signal_and_policy_keys() -> None:
    comparison, _current, _expected = _pass_payloads()
    comparison["status"] = "diff"
    comparison["diff"]["changed_evidence_signals"] = [
        "tier1.match_identity.match_id:direct:match_state.match_id",
    ]
    comparison["diff"]["changed_policies"] = [
        "tier1.match_result.match_result.value_source_policy",
    ]

    report = drift_report.build_evidence_schema_drift_report(comparison)

    assert report["affected"]["entries"] == [
        "tier1.match_identity.match_id",
        "tier1.match_result.match_result",
    ]
    assert report["affected"]["evidence_signals"] == [
        "tier1.match_identity.match_id:direct:match_state.match_id",
    ]


def test_unresolved_affected_entries_use_generic_review_targets() -> None:
    comparison, _current, _expected = _pass_payloads()
    comparison["status"] = "diff"
    comparison["diff"]["changed_entries"] = ["tier9.unknown_surface.unknown_field"]

    report = drift_report.build_evidence_schema_drift_report(comparison)

    assert report["review_guidance"]["recommended_review_modules"] == [
        "src/mythic_edge_parser/app/evidence_ledger.py",
        "src/mythic_edge_parser/app/evidence_schema_snapshot.py",
    ]
    assert report["review_guidance"]["recommended_tests"] == [
        "tests/test_evidence_ledger.py",
        "tests/test_evidence_schema_snapshot.py",
    ]


def test_vocabulary_and_output_family_changes_add_contract_review_targets() -> None:
    comparison, _current, _expected = _pass_payloads()
    comparison["status"] = "diff"
    comparison["diff"]["changed_output_families"] = ["match_identity_and_lifecycle"]
    comparison["diff"]["changed_vocabulary"] = ["value_sources"]

    report = drift_report.build_evidence_schema_drift_report(comparison)

    assert "docs/contracts/player_log_evidence_ledger.md" in report["review_guidance"]["recommended_review_modules"]
    assert (
        "docs/contracts/player_log_evidence_ledger_schema.md"
        in report["review_guidance"]["recommended_review_modules"]
    )


def test_privacy_findings_are_path_only_and_do_not_echo_private_values() -> None:
    current = snapshot_builder.build_evidence_schema_snapshot()
    expected = copy.deepcopy(current)
    private_path = "/Users/example/private.py"
    expected["entries"][0]["parser_owner"] = private_path
    comparison = snapshot_builder.compare_evidence_schema_snapshot(current, expected)

    report = drift_report.build_evidence_schema_drift_report(
        comparison,
        current_snapshot=current,
        expected_snapshot=expected,
    )
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail"
    assert "privacy_findings" in report["status_reasons"]
    assert "expected.entries[0].parser_owner" in report["privacy"]["local_absolute_paths_found"]
    assert "expected_snapshot.entries[0].parser_owner" in report["privacy"]["local_absolute_paths_found"]
    assert private_path not in encoded


def test_malformed_private_caller_values_are_not_echoed() -> None:
    comparison, _current, _expected = _pass_payloads()
    private_value = "secret=/Users/example/private-token"
    comparison["status"] = "diff"
    comparison["diff"]["added_entries"] = [private_value]
    comparison["drift_flags"] = [private_value]
    comparison["limitations"] = [private_value]

    report = drift_report.build_evidence_schema_drift_report(comparison)
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail"
    assert "privacy_findings" in report["status_reasons"]
    assert private_value not in encoded


def test_write_report_rejects_forbidden_private_snippets(tmp_path) -> None:
    comparison, current, expected = _pass_payloads()
    report = drift_report.build_evidence_schema_drift_report(
        comparison,
        current_snapshot=current,
        expected_snapshot=expected,
    )
    report["review_guidance"]["review_notes"].append("inspect /Users/example/private.log")
    output_path = tmp_path / "report.json"

    with pytest.raises(ValueError, match="forbidden evidence schema drift report content"):
        drift_report.write_evidence_schema_drift_report(output_path, report)

    assert not output_path.exists()


def test_cli_check_returns_zero_for_pass(capsys: pytest.CaptureFixture[str]) -> None:
    assert drift_report.main(["--check"]) == 0
    captured = capsys.readouterr()

    assert '"status": "pass"' in captured.out
    assert captured.err == ""


def test_cli_check_returns_zero_for_review_and_does_not_update_snapshot(
    tmp_path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    expected = snapshot_builder.build_evidence_schema_snapshot()
    expected["summary"]["entry_count"] += 1
    expected_path = tmp_path / "expected.json"
    snapshot_builder.write_evidence_schema_snapshot(expected_path, expected)
    before = snapshot_builder.load_expected_evidence_schema_snapshot(expected_path)

    assert drift_report.main(["--check", "--expected", str(expected_path)]) == 0
    captured = capsys.readouterr()

    assert '"status": "review"' in captured.out
    assert snapshot_builder.load_expected_evidence_schema_snapshot(expected_path) == before


def test_cli_check_returns_nonzero_for_fail(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    missing_path = tmp_path / "missing.json"

    assert drift_report.main(["--check", "--expected", str(missing_path)]) == 1
    captured = capsys.readouterr()

    assert '"status": "fail"' in captured.out
    assert not missing_path.exists()


def test_cli_out_writes_explicit_json_path(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    output_path = tmp_path / "reports" / "drift.json"

    assert drift_report.main(["--check", "--out", str(output_path)]) == 0
    captured = capsys.readouterr()

    assert '"status": "pass"' in captured.out
    assert json.loads(output_path.read_text(encoding="utf-8"))["object"] == (
        drift_report.EVIDENCE_SCHEMA_DRIFT_REPORT_OBJECT
    )


def test_cli_comparison_mode_uses_existing_comparison_json(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    comparison, _current, _expected = _pass_payloads()
    comparison["status"] = "diff"
    comparison["diff"]["added_entries"] = ["tier9.synthetic.synthetic_field"]
    comparison_path = tmp_path / "comparison.json"
    comparison_path.write_text(json.dumps(comparison), encoding="utf-8")

    assert drift_report.main(["--comparison", str(comparison_path)]) == 0
    captured = capsys.readouterr()

    assert '"status": "review"' in captured.out
    assert "tier9.synthetic.synthetic_field" in captured.out
