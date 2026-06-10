from __future__ import annotations

import json
from pathlib import Path

from mythic_edge_parser.app import diagnostics, evidence_runtime_status, evidence_validation_report_wiring

PRIVATE_POSIX_PATH = "/" + "Users/example/private/" + "Player.log"
PRIVATE_POSIX_PREFIX = "/" + "Users/example"
PRIVATE_POSIX_MIDDLE = "example/" + "private"
PRIVATE_LOG_BASENAME = "Player" + ".log"
STATUS_UPDATE_ATTR = "update_" + "runtime_" + "status"


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
            "missing_mapping_count": 1,
            "ambiguous_mapping_count": 0,
            "review_required_count": 1 if status != "pass" else 0,
            "conflict_count": 0,
            "degraded_count": 0,
            "not_checked_count": 0,
            "drift_flag_count": 1,
        },
        "attachments": [{"field_evidence": {"entry_id": "tier1.match_identity.match_id"}}],
        "affected": {
            "output_families": ["match_summary"],
            "entries": ["tier1.match_identity.match_id"],
            "evidence_signals": ["match_identity"],
        },
        "review_guidance": {
            "recommended_review_modules": ["runtime_field_evidence"],
            "recommended_tests": ["tests/test_runtime_field_evidence.py"],
            "review_notes": ["Runtime field-evidence remained sidecar-only."],
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
            "entry_changes": 1 if status == "fail" else 0,
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
            "executable_invariant_count": 2,
            "declared_invariant_total_count": 2,
            "declared_invariant_unique_count": 2,
            "passed_count": 1 if status == "fail" else 2,
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
        "diff": {"changed_entries": ["must not be copied"]},
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


def _review_section(status: str = "pass") -> dict:
    return evidence_validation_report_wiring.build_evidence_ledger_review_section(
        report_context="synthetic_test_reference",
        runtime_field_evidence_report=_runtime_report(status="review" if status == "review" else "pass"),
        schema_snapshot_comparison=_snapshot_comparison(status="diff" if status == "diff" else "pass"),
    )


def test_builder_returns_unavailable_without_sources() -> None:
    health = evidence_runtime_status.build_evidence_ledger_health_status()

    assert health["object"] == evidence_runtime_status.EVIDENCE_LEDGER_HEALTH_OBJECT
    assert health["schema_version"] == evidence_runtime_status.EVIDENCE_LEDGER_HEALTH_SCHEMA_VERSION
    assert health["status"] == "unavailable"
    assert health["review_required"] is False
    assert health["status_affects_runtime_" "status"] is False
    assert health["summary"]["supplied_source_count"] == 0
    assert health["summary"]["unavailable_count"] == 5
    assert set(health["source_refs"]) == set(evidence_runtime_status.EVIDENCE_LEDGER_HEALTH_SOURCE_KEYS)
    assert "No evidence-ledger health inputs were supplied." in health["limitations"]


def test_existing_review_section_is_preferred_over_individual_sources() -> None:
    health = evidence_runtime_status.build_evidence_ledger_health_status(
        evidence_ledger_review=_review_section(status="pass"),
        invariant_execution_report=_invariant_report(status="fail"),
    )

    assert health["status"] == "pass"
    assert health["source_refs"]["evidence_ledger_review"]["supplied"] is True
    assert health["source_refs"]["invariant_execution_report"]["supplied"] is False
    assert health["summary"]["supplied_source_count"] == 1
    assert (
        "Existing evidence_ledger_review input was preferred over individual source summaries."
        in health["limitations"]
    )


def test_review_not_supplied_maps_to_unavailable() -> None:
    review = evidence_validation_report_wiring.build_evidence_ledger_review_section(
        report_context="synthetic_test_reference",
    )

    health = evidence_runtime_status.build_evidence_ledger_health_status(evidence_ledger_review=review)

    assert health["status"] == "unavailable"
    assert health["source_refs"]["evidence_ledger_review"]["status"] == "unavailable"


def test_runtime_review_maps_to_health_review() -> None:
    health = evidence_runtime_status.build_evidence_ledger_health_status(
        runtime_field_evidence_report=_runtime_report(status="review"),
    )

    assert health["status"] == "review"
    assert health["review_required"] is True
    assert health["summary"]["review_count"] == 1
    assert health["summary"]["runtime_field_evidence_review_required_count"] == 1


def test_snapshot_diff_maps_to_health_diff() -> None:
    health = evidence_runtime_status.build_evidence_ledger_health_status(
        schema_snapshot_comparison=_snapshot_comparison(status="diff"),
    )
    encoded = json.dumps(health, sort_keys=True)

    assert health["status"] == "diff"
    assert health["summary"]["diff_count"] == 1
    assert health["summary"]["schema_drift_changed_entry_count"] == 2
    assert health["summary"]["schema_drift_changed_signal_count"] == 1
    assert "changed_entries" not in encoded
    assert "must not be copied" not in encoded


def test_invariant_and_schema_drift_failures_fail_health() -> None:
    invariant_health = evidence_runtime_status.build_evidence_ledger_health_status(
        invariant_execution_report=_invariant_report(status="fail"),
    )
    drift_health = evidence_runtime_status.build_evidence_ledger_health_status(
        schema_drift_report=_schema_drift_report(status="fail"),
    )

    assert invariant_health["status"] == "fail"
    assert invariant_health["summary"]["invariant_failed_count"] == 1
    assert drift_health["status"] == "fail"
    assert drift_health["summary"]["schema_drift_changed_entry_count"] == 1


def test_unknown_source_object_schema_or_status_fails_health() -> None:
    bad_object = {**_runtime_report(), "object": "wrong_object"}
    bad_schema = {**_runtime_report(), "schema_version": "wrong.v1"}
    bad_status = {**_runtime_report(), "status": "unknown"}

    for source in (bad_object, bad_schema, bad_status):
        health = evidence_runtime_status.build_evidence_ledger_health_status(
            runtime_field_evidence_report=source,
        )

        assert health["status"] == "fail"


def test_malformed_non_mapping_source_fails_health() -> None:
    health = evidence_runtime_status.build_evidence_ledger_health_status(
        runtime_field_evidence_report="not a report",  # type: ignore[arg-type]
    )

    assert health["status"] == "fail"
    assert "runtime_field_evidence_report:malformed_source_report" in health["status_reasons"]


def test_full_runtime_details_are_not_copied_to_health() -> None:
    health = evidence_runtime_status.build_evidence_ledger_health_status(
        runtime_field_evidence_report=_runtime_report(status="pass"),
    )
    encoded = json.dumps(health, sort_keys=True)

    assert health["status"] == "pass"
    assert '"attachments"' not in encoded
    assert '"field_evidence"' not in encoded
    assert health["privacy"]["full_field_evidence_attachments_included"] is False


def test_privacy_findings_are_path_only_and_do_not_echo_raw_values() -> None:
    report = _runtime_report()
    report["privacy"]["forbidden_content_findings"] = [
        "https://script.google.com" + "/macros/s/" + "AKfycb-" + "secret-token-value" + "/exec"
    ]
    report["status_reasons"] = [f"raw local marker {PRIVATE_POSIX_PATH}"]

    health = evidence_runtime_status.build_evidence_ledger_health_status(
        runtime_field_evidence_report=report,
    )
    encoded = json.dumps(health, sort_keys=True)

    assert health["status"] == "fail"
    assert "runtime_field_evidence_report.privacy.forbidden_content_findings" in (
        health["privacy"]["forbidden_content_findings"]
    )
    assert "AKfycb-secret-token-value" not in encoded
    assert PRIVATE_POSIX_PREFIX not in encoded
    assert f"{PRIVATE_POSIX_MIDDLE}/{PRIVATE_LOG_BASENAME}" not in encoded
    assert PRIVATE_LOG_BASENAME not in encoded


def test_runtime_artifact_url_detection_uses_exact_hosts_without_substring_trust() -> None:
    trusted_report = _runtime_report()
    trusted_report["status_reasons"] = ["runtime endpoint https://script.google.com/macros/s/synthetic-token/exec"]
    trusted_health = evidence_runtime_status.build_evidence_ledger_health_status(
        runtime_field_evidence_report=trusted_report,
    )
    trusted_encoded = json.dumps(trusted_health, sort_keys=True)

    assert trusted_health["privacy"]["runtime_artifacts_included"] is True
    assert "synthetic-token" not in trusted_encoded

    adversarial_report = _runtime_report()
    adversarial_report["status_reasons"] = ["lookalike https://script.google.com.evil.example/macros/s/token/exec"]
    adversarial_health = evidence_runtime_status.build_evidence_ledger_health_status(
        runtime_field_evidence_report=adversarial_report,
    )
    adversarial_encoded = json.dumps(adversarial_health, sort_keys=True)

    assert "runtime_field_evidence_report.status_reasons[0]" in (
        adversarial_health["privacy"]["forbidden_content_findings"]
    )
    assert adversarial_health["privacy"]["runtime_artifacts_included"] is False
    assert "evil.example" not in adversarial_encoded


def test_complete_local_paths_are_redacted_from_copied_status_strings() -> None:
    posix_path = PRIVATE_POSIX_PATH
    windows_path = "C:" + "\\Users\\Jane Doe\\AppData\\Local\\" + "Player.log"
    report = _runtime_report(status="review")
    report["status_reasons"] = [
        f"raw local marker {posix_path}",
        f"windows local marker {windows_path}",
    ]
    report["affected"]["entries"] = [posix_path, windows_path]
    report["review_guidance"]["review_notes"] = [
        f"inspect {posix_path}",
        f"inspect {windows_path}",
    ]
    report["drift_flags"] = [posix_path, windows_path]

    health = evidence_runtime_status.build_evidence_ledger_health_status(
        runtime_field_evidence_report=report,
    )
    encoded = json.dumps(health, sort_keys=True)

    assert health["status"] == "fail"
    assert "[redacted-path]" in encoded
    for forbidden in (
        "/" + "Users",
        PRIVATE_POSIX_MIDDLE,
        PRIVATE_LOG_BASENAME,
        r"C:\Users",
        "Jane Doe",
        "AppData",
    ):
        assert forbidden not in encoded


def test_protected_surface_assertion_true_fails_health() -> None:
    report = _runtime_report()
    report["protected_surface_assertions"]["workbook_schema_changed"] = True

    health = evidence_runtime_status.build_evidence_ledger_health_status(
        runtime_field_evidence_report=report,
    )

    assert health["status"] == "fail"
    assert health["summary"]["protected_surface_violation_count"] == 1
    assert "protected_surface_assertion_true" in health["status_reasons"]


def test_update_helper_writes_only_evidence_ledger_health(monkeypatch) -> None:
    calls: list[dict] = []

    def fake_status_update(**fields):
        calls.append(fields)
        return Path("unused")

    monkeypatch.setattr(evidence_runtime_status.diagnostics, STATUS_UPDATE_ATTR, fake_status_update)

    health = evidence_runtime_status.update_evidence_ledger_health_status(
        runtime_field_evidence_report=_runtime_report(status="review"),
    )

    assert health["status"] == "review"
    assert calls == [{"evidence_ledger_health": health}]


def test_diagnostics_status_update_writes_health_without_status_promotion(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(diagnostics, "STATUS_ROOT", tmp_path / "status")
    diagnostics.reset_diagnostics_runtime_state()
    diagnostics.update_runtime_status(status="running", webhook_failures=0)
    health = evidence_runtime_status.build_evidence_ledger_health_status(
        runtime_field_evidence_report=_runtime_report(status="review"),
    )

    diagnostics.update_runtime_status(evidence_ledger_health=health)

    status_path = tmp_path / "status" / "manasight_status_latest.json"
    payload = json.loads(status_path.read_text(encoding="utf-8"))
    assert payload["status"] == "running"
    assert payload["webhook_failures"] == 0
    assert payload["evidence_ledger_health"]["status"] == "review"
