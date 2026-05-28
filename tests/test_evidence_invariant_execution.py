from __future__ import annotations

import json

import pytest

from mythic_edge_parser.app import evidence_invariant_execution as invariants
from mythic_edge_parser.app import evidence_ledger, evidence_schema_drift_report


def _ledger() -> dict:
    return evidence_ledger.build_player_log_evidence_ledger()


def _schema_report() -> dict:
    return evidence_schema_drift_report.build_current_evidence_schema_drift_report()


def _result(report: dict, invariant_id: str) -> dict:
    return next(result for result in report["invariant_results"] if result["invariant_id"] == invariant_id)


def test_current_ledger_and_schema_drift_report_produce_pass_report() -> None:
    report = invariants.build_current_evidence_invariant_execution_report()

    assert report["object"] == invariants.EVIDENCE_INVARIANT_EXECUTION_REPORT_OBJECT
    assert report["schema_version"] == invariants.EVIDENCE_INVARIANT_EXECUTION_REPORT_VERSION
    assert report["status"] == "pass"
    assert report["review_required"] is False
    assert report["status_reasons"] == []
    assert report["summary"]["executable_invariant_count"] == len(invariants.EXECUTABLE_INVARIANT_IDS)
    assert report["summary"]["failed_count"] == 0
    assert report["summary"]["degraded_count"] == 0
    assert report["summary"]["not_checked_count"] == 0
    assert [result["status"] for result in report["invariant_results"]].count("passed") == (
        len(invariants.EXECUTABLE_INVARIANT_IDS)
    )


def test_report_shape_uses_ledger_invariant_status_vocabulary_and_protected_surface_assertions() -> None:
    report = invariants.build_current_evidence_invariant_execution_report()

    assert invariants.EVIDENCE_INVARIANT_EXECUTION_REPORT_STATUSES == ("pass", "review", "fail")
    assert set(report) == {
        "object",
        "schema_version",
        "source_issue",
        "parent_issue",
        "status",
        "review_required",
        "status_reasons",
        "input_refs",
        "summary",
        "declared_invariants",
        "invariant_results",
        "affected",
        "review_guidance",
        "drift_flags",
        "privacy",
        "protected_surface_assertions",
        "limitations",
    }
    assert all(result["status"] in evidence_ledger.INVARIANT_STATUSES for result in report["invariant_results"])
    assert all(value is False for value in report["protected_surface_assertions"].values())


def test_declared_invariant_inventory_counts_current_ledger() -> None:
    report = invariants.build_current_evidence_invariant_execution_report()

    assert report["declared_invariants"]["total_count"] == 425
    assert report["declared_invariants"]["unique_count"] == 394
    assert report["declared_invariants"]["shared_name_count"] > 0
    assert report["declared_invariants"]["entries_without_invariants"] == []
    assert report["declared_invariants"]["duplicate_names_within_entries"] == []
    assert report["declared_invariants"]["invalid_names"] == []
    assert "match_identity_and_lifecycle" in report["declared_invariants"]["by_output_family"]


def test_non_mapping_ledger_input_fails_without_uncaught_exception() -> None:
    report = invariants.build_evidence_invariant_execution_report("not a ledger")  # type: ignore[arg-type]

    assert report["status"] == "fail"
    assert _result(report, "ledger_validates_cleanly")["status"] == "failed"
    assert "invariant_failed" in report["drift_flags"]


def test_ledger_validation_errors_fail_ledger_validator_invariant() -> None:
    ledger = _ledger()
    ledger["object"] = "wrong_object"

    report = invariants.build_evidence_invariant_execution_report(
        ledger,
        schema_drift_report=_schema_report(),
        require_schema_drift_report=True,
    )

    assert report["status"] == "fail"
    assert _result(report, "ledger_validates_cleanly")["status"] == "failed"
    assert "ledger validation returned" in report["limitations"][0]


def test_missing_or_empty_invariant_lists_fail() -> None:
    ledger = _ledger()
    ledger["entries"][0]["invariant_checks"] = []

    report = invariants.build_evidence_invariant_execution_report(ledger, require_schema_drift_report=False)

    assert report["status"] == "fail"
    assert _result(report, "entries_declare_invariant_checks")["status"] == "failed"
    assert ledger["entries"][0]["entry_id"] in report["affected"]["entries"]


@pytest.mark.parametrize(
    "bad_name",
    [
        123,
        "",
        "UppercaseName",
        "has punctuation!",
        "path/like",
        "/Users/example/private_invariant",
    ],
)
def test_invalid_invariant_names_fail_without_echoing_private_values(bad_name: object) -> None:
    ledger = _ledger()
    ledger["entries"][0]["invariant_checks"] = [bad_name]

    report = invariants.build_evidence_invariant_execution_report(ledger, require_schema_drift_report=False)
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail"
    assert _result(report, "entry_invariant_names_are_stable")["status"] == "failed"
    assert report["declared_invariants"]["invalid_names"] == [
        f"{ledger['entries'][0]['entry_id']}.invariant_checks[0]",
    ]
    if isinstance(bad_name, str) and "/Users/" in bad_name:
        assert bad_name not in encoded


def test_duplicate_invariant_names_within_entry_fail() -> None:
    ledger = _ledger()
    ledger["entries"][0]["invariant_checks"] = ["same_name", "same_name"]

    report = invariants.build_evidence_invariant_execution_report(ledger, require_schema_drift_report=False)

    assert report["status"] == "fail"
    assert _result(report, "entry_invariant_names_are_unique_within_entry")["status"] == "failed"
    assert report["declared_invariants"]["duplicate_names_within_entries"] == [ledger["entries"][0]["entry_id"]]


def test_duplicate_invariant_names_across_entries_are_allowed_and_counted() -> None:
    ledger = _ledger()
    ledger["entries"][0]["invariant_checks"] = ["shared_invariant"]
    ledger["entries"][1]["invariant_checks"] = ["shared_invariant"]

    report = invariants.build_evidence_invariant_execution_report(ledger, require_schema_drift_report=False)

    assert _result(report, "entry_invariant_names_are_unique_within_entry")["status"] == "passed"
    assert report["declared_invariants"]["shared_name_count"] >= 1


def test_missing_review_modules_degrades_report() -> None:
    ledger = _ledger()
    ledger["entries"][0]["recommended_review_modules"] = []

    report = invariants.build_evidence_invariant_execution_report(ledger, require_schema_drift_report=False)

    assert report["status"] == "review"
    assert _result(report, "entries_with_invariants_have_review_modules")["status"] == "degraded"
    assert ledger["entries"][0]["entry_id"] in report["affected"]["entries"]


def test_missing_tests_degrades_report() -> None:
    ledger = _ledger()
    ledger["entries"][0]["tests"] = []

    report = invariants.build_evidence_invariant_execution_report(ledger, require_schema_drift_report=False)

    assert report["status"] == "review"
    assert _result(report, "entries_with_invariants_have_tests")["status"] == "degraded"
    assert ledger["entries"][0]["entry_id"] in report["affected"]["entries"]


def test_schema_drift_report_review_degrades_invariant_execution() -> None:
    schema_report = _schema_report()
    schema_report["status"] = "review"
    schema_report["drift_flags"] = ["changed_signal_type"]
    schema_report["review_guidance"]["recommended_tests"] = ["tests/test_evidence_schema_drift_report.py"]

    report = invariants.build_evidence_invariant_execution_report(
        _ledger(),
        schema_drift_report=schema_report,
        require_schema_drift_report=True,
    )

    assert report["status"] == "review"
    assert _result(report, "schema_drift_report_is_usable_review_evidence")["status"] == "degraded"
    assert "changed_signal_type" in report["drift_flags"]
    assert "tests/test_evidence_schema_drift_report.py" in report["review_guidance"]["recommended_tests"]


def test_schema_drift_report_fail_fails_invariant_execution() -> None:
    schema_report = _schema_report()
    schema_report["status"] = "fail"

    report = invariants.build_evidence_invariant_execution_report(
        _ledger(),
        schema_drift_report=schema_report,
        require_schema_drift_report=True,
    )

    assert report["status"] == "fail"
    assert _result(report, "schema_drift_report_is_usable_review_evidence")["status"] == "failed"


def test_schema_drift_report_protected_surface_assertion_true_fails() -> None:
    schema_report = _schema_report()
    schema_report["protected_surface_assertions"]["parser_behavior_changed"] = True

    report = invariants.build_evidence_invariant_execution_report(
        _ledger(),
        schema_drift_report=schema_report,
        require_schema_drift_report=True,
    )

    assert report["status"] == "fail"
    assert _result(report, "schema_drift_report_protected_surface_assertions_hold")["status"] == "failed"


def test_optional_missing_schema_drift_report_is_not_checked() -> None:
    report = invariants.build_evidence_invariant_execution_report(_ledger(), require_schema_drift_report=False)

    assert report["status"] == "pass"
    assert _result(report, "schema_drift_report_is_usable_review_evidence")["status"] == "not_checked"
    assert _result(report, "schema_drift_report_protected_surface_assertions_hold")["status"] == "not_checked"


def test_required_missing_schema_drift_report_fails() -> None:
    report = invariants.build_evidence_invariant_execution_report(_ledger(), require_schema_drift_report=True)

    assert report["status"] == "fail"
    assert _result(report, "schema_drift_report_is_usable_review_evidence")["status"] == "failed"
    assert "schema_snapshot_missing" in report["drift_flags"]


def test_privacy_findings_are_path_only_and_never_echo_private_values() -> None:
    ledger = _ledger()
    private_value = "/Users/example/private.py"
    ledger["entries"][0]["parser_owner"] = private_value

    report = invariants.build_evidence_invariant_execution_report(ledger, require_schema_drift_report=False)
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail"
    assert "privacy_findings" in report["status_reasons"]
    assert "ledger.entries[0].parser_owner" in report["privacy"]["local_absolute_paths_found"]
    assert private_value not in encoded


def test_write_report_rejects_forbidden_private_snippets(tmp_path) -> None:
    report = invariants.build_current_evidence_invariant_execution_report()
    report["review_guidance"]["review_notes"].append("inspect /Users/example/private.log")
    output_path = tmp_path / "report.json"

    with pytest.raises(ValueError, match="forbidden evidence invariant execution report content"):
        invariants.write_evidence_invariant_execution_report(output_path, report)

    assert not output_path.exists()


def test_cli_check_returns_zero_for_pass(capsys: pytest.CaptureFixture[str]) -> None:
    assert invariants.main(["--check"]) == 0
    captured = capsys.readouterr()

    assert '"status": "pass"' in captured.out
    assert captured.err == ""


def test_cli_check_returns_zero_for_review(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    schema_report = _schema_report()
    schema_report["status"] = "review"
    schema_path = tmp_path / "schema_drift_report.json"
    schema_path.write_text(json.dumps(schema_report), encoding="utf-8")

    assert invariants.main(["--check", "--schema-drift-report", str(schema_path)]) == 0
    captured = capsys.readouterr()

    assert '"status": "review"' in captured.out


def test_cli_check_returns_nonzero_for_fail(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    missing_path = tmp_path / "missing.json"

    assert invariants.main(["--check", "--ledger", str(missing_path), "--no-schema-drift-report"]) == 1
    captured = capsys.readouterr()

    assert '"status": "fail"' in captured.out


def test_cli_out_writes_only_to_explicit_path(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    output_path = tmp_path / "reports" / "invariants.json"

    assert invariants.main(["--check", "--out", str(output_path)]) == 0
    captured = capsys.readouterr()

    assert '"status": "pass"' in captured.out
    assert json.loads(output_path.read_text(encoding="utf-8"))["object"] == (
        invariants.EVIDENCE_INVARIANT_EXECUTION_REPORT_OBJECT
    )


def test_cli_does_not_update_expected_snapshot_or_require_update_env(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    expected_path = tmp_path / "expected.json"
    expected_path.write_text("{not json", encoding="utf-8")
    before = expected_path.read_text(encoding="utf-8")
    monkeypatch.delenv("MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT", raising=False)

    assert invariants.main(["--check", "--expected", str(expected_path)]) == 1

    assert expected_path.read_text(encoding="utf-8") == before
