from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from mythic_edge_parser.app import evidence_validation_report_wiring as wiring
from mythic_edge_parser.app import feature_equity_corpus_ratchet, golden_replay, parser_diagnostics

FIXTURE_DIR = Path("tests/fixtures/golden_replay")
BASELINE_PATH = Path("tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json")
BO1_MANIFEST = FIXTURE_DIR / "bo1_match_win_basic.manifest.json"


def _runtime_report(status: str = "pass") -> dict:
    return {
        "object": "mythic_edge_player_log_runtime_field_evidence_report",
        "schema_version": "player_log_runtime_field_evidence_report.v1",
        "status": status,
        "review_required": status != "pass",
        "status_reasons": [],
        "summary": {
            "attachment_count": 2,
            "valid_field_evidence_count": 2,
            "missing_mapping_count": 0,
            "ambiguous_mapping_count": 0,
            "review_required_count": 1 if status != "pass" else 0,
            "conflict_count": 0,
            "degraded_count": 0,
            "not_checked_count": 0,
            "drift_flag_count": 1,
        },
        "attachments": [
            {
                "field_ref": {"output_family": "match_summary", "output_field": "match_id"},
                "field_evidence": {"entry_id": "tier1.match_lifecycle.match_id"},
            }
        ],
        "affected": {
            "output_families": ["match_summary"],
            "entries": ["tier1.match_lifecycle.match_id"],
            "evidence_signals": ["match_identity"],
        },
        "review_guidance": {
            "recommended_review_modules": ["runtime_field_evidence"],
            "recommended_tests": ["tests/test_runtime_field_evidence.py"],
            "review_notes": ["Runtime field-evidence review stayed sidecar-only."],
        },
        "drift_flags": ["runtime_field_evidence_review_required"],
        "privacy": {
            "forbidden_content_findings": [],
            "local_absolute_paths_found": [],
            "raw_private_logs_included": False,
            "raw_payload_values_included": False,
            "runtime_artifacts_included": False,
            "generated_data_included": False,
        },
        "protected_surface_assertions": {"parser_behavior_changed": False},
    }


def _schema_drift_report(status: str = "pass") -> dict:
    return {
        "object": "mythic_edge_player_log_evidence_schema_drift_report",
        "schema_version": "player_log_evidence_schema_drift_report.v1",
        "status": status,
        "review_required": status != "pass",
        "status_reasons": [],
        "summary": {
            "output_family_changes": 0,
            "entry_changes": 1 if status == "review" else 0,
            "evidence_signal_changes": 0,
            "vocabulary_changes": 0,
            "policy_changes": 0,
            "privacy_findings": 0,
        },
        "affected": {"output_families": [], "entries": [], "evidence_signals": []},
        "review_guidance": {"recommended_review_modules": [], "recommended_tests": [], "review_notes": []},
        "drift_flags": [],
        "privacy": {
            "forbidden_content_findings": [],
            "local_absolute_paths_found": [],
            "raw_private_logs_included": False,
            "raw_payload_values_included": False,
            "runtime_artifacts_included": False,
            "generated_data_included": False,
        },
        "protected_surface_assertions": {"parser_behavior_changed": False},
    }


def _invariant_report(status: str = "pass") -> dict:
    return {
        "object": "mythic_edge_player_log_evidence_invariant_execution_report",
        "schema_version": "player_log_evidence_invariant_execution.v1",
        "status": status,
        "review_required": status != "pass",
        "status_reasons": [],
        "summary": {
            "executable_invariant_count": 3,
            "declared_invariant_total_count": 3,
            "declared_invariant_unique_count": 3,
            "passed_count": 2 if status == "fail" else 3,
            "failed_count": 1 if status == "fail" else 0,
            "degraded_count": 0,
            "not_applicable_count": 0,
            "not_checked_count": 0,
            "affected_entry_count": 0,
            "affected_output_family_count": 0,
            "drift_flag_count": 0,
        },
        "affected": {"output_families": [], "entries": [], "evidence_signals": []},
        "review_guidance": {"recommended_review_modules": [], "recommended_tests": [], "review_notes": []},
        "drift_flags": [],
        "privacy": {
            "forbidden_content_findings": [],
            "local_absolute_paths_found": [],
            "raw_private_logs_included": False,
            "raw_payload_values_included": False,
            "runtime_artifacts_included": False,
            "generated_data_included": False,
        },
        "protected_surface_assertions": {"parser_behavior_changed": False},
    }


def _snapshot_comparison(status: str = "pass") -> dict:
    return {
        "object": "mythic_edge_player_log_evidence_schema_snapshot_comparison",
        "schema_version": "player_log_evidence_schema_snapshot_comparison.v1",
        "status": status,
        "review_required": status != "pass",
        "status_reasons": [],
        "summary": {
            "output_family_changes": 0,
            "entry_changes": 2 if status == "diff" else 0,
            "evidence_signal_changes": 1 if status == "diff" else 0,
            "vocabulary_changes": 0,
            "policy_changes": 0,
            "privacy_findings": 0,
        },
        "diff": {"changed_entries": ["not copied into integrated report"]},
        "affected": {"output_families": [], "entries": [], "evidence_signals": []},
        "review_guidance": {"recommended_review_modules": [], "recommended_tests": [], "review_notes": []},
        "drift_flags": [],
        "privacy": {
            "forbidden_content_findings": [],
            "local_absolute_paths_found": [],
            "raw_private_logs_included": False,
            "raw_payload_values_included": False,
            "runtime_artifacts_included": False,
            "generated_data_included": False,
        },
        "protected_surface_assertions": {"parser_behavior_changed": False},
    }


def _prebuilt_review_section_with_private_details() -> dict:
    return {
        "object": wiring.EVIDENCE_LEDGER_REVIEW_OBJECT,
        "schema_version": wiring.EVIDENCE_LEDGER_REVIEW_SCHEMA_VERSION,
        "report_context": "synthetic_test_reference",
        "status": "pass",
        "review_required": False,
        "status_affects_parent": False,
        "status_reasons": [],
        "summary": {},
        "sources": {},
        "attachments": [
            {"field_evidence": {"raw": "/" + "Users/example/private/" + "Player.log"}},
        ],
        "invariant_results": [
            {"raw_payload": "DETAILED " + "LOGS:" + " private raw payload"},
        ],
        "privacy": {"forbidden_content_findings": [], "local_absolute_paths_found": []},
    }


def _write_log(tmp_path: Path) -> Path:
    payload = {
        "greToClientEvent": {
            "greToClientMessages": [
                {
                    "type": "GREMessageType" + "_GameStateMessage",
                    "msgId": 1,
                    "gameStateMessage": {
                        "gameInfo": {
                            "stage": "GameStage_GameOver",
                            "matchState": "MatchState_GameComplete",
                            "results": [{"scope": "MatchScope_Game", "winningTeamId": 1}],
                        }
                    },
                }
            ]
        }
    }
    path = tmp_path / "Player.log"
    raw_log_marker = "[Unity" + "CrossThreadLogger]"
    path.write_text(f"{raw_log_marker}5/8/2026 1:02:03 PM greToClientEvent\n{json.dumps(payload)}\n")
    return path


def test_not_supplied_section_has_stable_shape() -> None:
    section = wiring.build_evidence_ledger_review_section(report_context="synthetic_test_reference")

    assert section["object"] == wiring.EVIDENCE_LEDGER_REVIEW_OBJECT
    assert section["schema_version"] == wiring.EVIDENCE_LEDGER_REVIEW_SCHEMA_VERSION
    assert section["status"] == "not_supplied"
    assert section["review_required"] is False
    assert section["status_affects_parent"] is False
    assert section["summary"]["source_report_count"] == 0
    assert section["summary"]["supplied_source_report_count"] == 0
    assert set(section["sources"]) == set(wiring.EVIDENCE_LEDGER_REVIEW_SOURCE_KEYS)
    assert "No evidence-ledger review source reports were supplied." in section["limitations"]


def test_pass_source_reports_summarize_without_copying_full_records() -> None:
    section = wiring.build_evidence_ledger_review_section(
        report_context="synthetic_test_reference",
        runtime_field_evidence_report=_runtime_report(),
        schema_drift_report=_schema_drift_report(),
        invariant_execution_report=_invariant_report(),
        schema_snapshot_comparison=_snapshot_comparison(),
    )
    encoded = json.dumps(section, sort_keys=True)

    assert section["status"] == "pass"
    assert section["summary"]["source_report_count"] == 4
    assert section["summary"]["pass_count"] == 4
    assert section["summary"]["runtime_field_evidence_attachment_count"] == 2
    assert section["summary"]["runtime_field_evidence_review_required_count"] == 0
    assert section["affected"]["entries"] == ["tier1.match_lifecycle.match_id"]
    assert '"attachments"' not in encoded
    assert '"field_evidence"' not in encoded
    assert '"diff"' not in encoded


def test_runtime_review_maps_section_to_review() -> None:
    section = wiring.build_evidence_ledger_review_section(
        report_context="synthetic_test_reference",
        runtime_field_evidence_report=_runtime_report(status="review"),
    )

    assert section["status"] == "review"
    assert section["review_required"] is True
    assert section["summary"]["review_count"] == 1
    assert section["summary"]["runtime_field_evidence_review_required_count"] == 1


def test_ok_status_maps_to_pass_only_for_feature_equity_context() -> None:
    report = _runtime_report(status="ok")

    feature_section = wiring.build_evidence_ledger_review_section(
        report_context="feature_equity_corpus_ratchet",
        runtime_field_evidence_report=report,
    )
    diagnostics_section = wiring.build_evidence_ledger_review_section(
        report_context="parser_diagnostics",
        runtime_field_evidence_report=report,
    )

    assert feature_section["status"] == "pass"
    assert diagnostics_section["status"] == "fail"


def test_schema_snapshot_diff_maps_section_to_diff() -> None:
    section = wiring.build_evidence_ledger_review_section(
        report_context="synthetic_test_reference",
        schema_snapshot_comparison=_snapshot_comparison(status="diff"),
    )

    assert section["status"] == "diff"
    assert section["summary"]["diff_count"] == 1
    assert section["summary"]["schema_drift_changed_entry_count"] == 2
    assert section["summary"]["schema_drift_changed_signal_count"] == 1


@pytest.mark.parametrize(
    ("source_report", "reason"),
    [
        ({**_runtime_report(), "object": "wrong_object"}, "unknown_source_object"),
        ({**_runtime_report(), "schema_version": "wrong.v1"}, "unknown_source_schema_version"),
        ({**_runtime_report(), "status": "unknown"}, "unknown_source_status"),
        (_schema_drift_report(status="fail"), "schema_drift_report:"),
        (_invariant_report(status="fail"), "invariant_execution_report:"),
    ],
)
def test_invalid_or_failing_source_reports_fail_section(source_report: dict, reason: str) -> None:
    section = wiring.build_evidence_ledger_review_section(
        report_context="synthetic_test_reference",
        runtime_field_evidence_report=source_report
        if source_report.get("object") == "mythic_edge_player_log_runtime_field_evidence_report"
        or source_report.get("object") == "wrong_object"
        else None,
        schema_drift_report=source_report
        if source_report.get("object") == "mythic_edge_player_log_evidence_schema_drift_report"
        else None,
        invariant_execution_report=source_report
        if source_report.get("object") == "mythic_edge_player_log_evidence_invariant_execution_report"
        else None,
    )

    assert section["status"] == "fail"
    assert section["review_required"] is True
    assert any(reason in item for item in section["status_reasons"])


def test_privacy_findings_are_path_only_and_do_not_echo_raw_values() -> None:
    report = _runtime_report()
    report["privacy"]["forbidden_content_findings"] = [
        "https://script.google.com" + "/macros/s/" + "AKfycb-" + "secret-token-value" + "/exec"
    ]
    report["status_reasons"] = ["raw local marker /Users/example/private/Player.log"]

    section = wiring.build_evidence_ledger_review_section(
        report_context="synthetic_test_reference",
        runtime_field_evidence_report=report,
    )
    encoded = json.dumps(section, sort_keys=True)

    assert section["status"] == "fail"
    assert "runtime_field_evidence_report.privacy.forbidden_content_findings" in (
        section["privacy"]["forbidden_content_findings"]
    )
    assert "AKfycb-secret-token-value" not in encoded
    assert "/Users/example" not in encoded


def test_runtime_artifact_url_detection_uses_exact_hosts_without_substring_trust() -> None:
    trusted_report = _runtime_report()
    trusted_report["status_reasons"] = ["runtime endpoint https://hooks.example.invalid/services/synthetic-token"]
    trusted_section = wiring.build_evidence_ledger_review_section(
        report_context="synthetic_test_reference",
        runtime_field_evidence_report=trusted_report,
    )
    trusted_encoded = json.dumps(trusted_section, sort_keys=True)

    assert trusted_section["privacy"]["runtime_artifacts_included"] is True
    assert "synthetic-token" not in trusted_encoded

    adversarial_report = _runtime_report()
    adversarial_report["status_reasons"] = ["lookalike https://script.google.com.evil.example/macros/s/token/exec"]
    adversarial_section = wiring.build_evidence_ledger_review_section(
        report_context="synthetic_test_reference",
        runtime_field_evidence_report=adversarial_report,
    )
    adversarial_encoded = json.dumps(adversarial_section, sort_keys=True)

    assert "runtime_field_evidence_report.status_reasons[0]" in (
        adversarial_section["privacy"]["forbidden_content_findings"]
    )
    assert adversarial_section["privacy"]["runtime_artifacts_included"] is False
    assert "evil.example" not in adversarial_encoded


def test_prebuilt_review_section_is_rebuilt_summary_only_and_redacted() -> None:
    section = wiring.evidence_review_section_from_inputs(
        _prebuilt_review_section_with_private_details(),
        report_context="parser_diagnostics",
    )
    encoded = json.dumps(section, sort_keys=True)

    assert section["status"] == "fail"
    assert section["report_context"] == "parser_diagnostics"
    assert section["status_affects_parent"] is False
    assert "forbidden_full_detail_keys" in section["status_reasons"]
    assert "integrated_report_privacy_findings" in section["status_reasons"]
    assert "attachments" not in section
    assert "invariant_results" not in section
    assert '"field_evidence"' not in encoded
    assert "/Users/example/private/Player.log" not in encoded
    assert "DETAILED LOGS:" not in encoded
    assert "evidence_ledger_review.attachments" in section["privacy"]["forbidden_content_findings"]
    assert "evidence_ledger_review.attachments[0].field_evidence.raw" in (
        section["privacy"]["local_absolute_paths_found"]
    )
    assert section["privacy"]["full_field_evidence_attachments_included"] is True


def test_parent_report_with_prebuilt_review_section_is_summary_only_and_redacted(tmp_path: Path) -> None:
    report = parser_diagnostics.build_parser_diagnostics_report(
        _write_log(tmp_path),
        profile="fixture",
        evidence_ledger_review=_prebuilt_review_section_with_private_details(),
    )
    encoded = json.dumps(report, sort_keys=True)

    assert report["overall_status"] == "pass"
    assert report["evidence_ledger_review"]["status"] == "fail"
    assert report["evidence_ledger_review"]["status_affects_parent"] is False
    assert "attachments" not in report["evidence_ledger_review"]
    assert "/Users/example/private/Player.log" not in encoded
    assert "DETAILED LOGS:" not in encoded


def test_protected_surface_assertion_true_fails_section() -> None:
    report = _runtime_report()
    report["protected_surface_assertions"]["workbook_schema_changed"] = True

    section = wiring.build_evidence_ledger_review_section(
        report_context="synthetic_test_reference",
        runtime_field_evidence_report=report,
    )

    assert section["status"] == "fail"
    assert section["summary"]["protected_surface_violation_count"] == 1
    assert "protected_surface_assertion_true" in section["status_reasons"]


def test_cli_inputs_are_explicit_and_optional(tmp_path: Path) -> None:
    report_path = tmp_path / "runtime-review.json"
    report_path.write_text(json.dumps(_runtime_report(status="review")), encoding="utf-8")
    parser = argparse.ArgumentParser()
    wiring.evidence_review_cli_arguments(parser)

    empty_args = parser.parse_args([])
    supplied_args = parser.parse_args(["--evidence-runtime-field-report", str(report_path)])

    assert wiring.evidence_review_inputs_from_args(empty_args) == {}
    assert wiring.evidence_review_inputs_from_args(supplied_args)["runtime_field_evidence_report"]["status"] == "review"


def test_diagnostics_integration_does_not_change_parent_status(tmp_path: Path) -> None:
    report = parser_diagnostics.build_parser_diagnostics_report(
        _write_log(tmp_path),
        profile="fixture",
        evidence_ledger_review={"runtime_field_evidence_report": _runtime_report(status="review")},
    )

    assert report["overall_status"] == "pass"
    assert report["parser_health"]["status"] == "pass"
    assert report["evidence_ledger_review"]["status"] == "review"
    assert report["evidence_ledger_review"]["status_affects_parent"] is False


def test_golden_replay_integration_does_not_change_suite_status() -> None:
    report = golden_replay.build_golden_replay_report(
        [BO1_MANIFEST],
        evidence_ledger_review={"schema_snapshot_comparison": _snapshot_comparison(status="diff")},
    )

    assert report["suite_status"] == "pass"
    assert report["evidence_ledger_review"]["status"] == "diff"
    assert golden_replay.REQUIRED_EXPECTED_SECTIONS[-1] == "parser_owned_rows"


def test_feature_equity_integration_does_not_change_count_baseline_status() -> None:
    report = feature_equity_corpus_ratchet.build_feature_equity_corpus_report(
        [FIXTURE_DIR],
        baseline_path=BASELINE_PATH,
        evidence_ledger_review={"invariant_execution_report": _invariant_report(status="fail")},
    )

    assert report["status"] == "ok"
    assert report["comparison"]["baseline_present"] is True
    assert report["evidence_ledger_review"]["status"] == "fail"
