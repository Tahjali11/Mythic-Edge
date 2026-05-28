from __future__ import annotations

import copy
import json

import pytest

from mythic_edge_parser.app import evidence_ledger
from mythic_edge_parser.app import runtime_field_evidence as runtime_evidence
from mythic_edge_parser.app.models import GameSummary, MatchSummary


def _ledger() -> dict:
    return evidence_ledger.build_player_log_evidence_ledger()


def _match_id_ref(**overrides: object) -> dict:
    field_ref = {
        "surface": "local_review_sidecar",
        "output_family": "match_identity_and_lifecycle",
        "output_field": "match_id",
        "entry_id": "tier1.match_identity.match_id",
        "entity_ref": {
            "entity_type": "match",
            "stable_ref": "synthetic-match-1",
            "game_number": "",
            "action_index": "",
        },
        "source_event_kind": "MatchState",
        "source_event_type": "match_started",
        "source_payload_paths": ["payload.match_id"],
        "source_event_timestamp": "",
        "value_source": "observed",
        "confidence": "high",
        "finality": "live",
        "drift_flags": [],
        "invariant_status": "not_checked",
        "degraded_reason": "",
    }
    field_ref.update(overrides)
    return field_ref


def _attachment(report: dict) -> dict:
    return report["attachments"][0]


def test_current_ledger_and_sanitized_field_refs_produce_pass_report() -> None:
    report = runtime_evidence.build_runtime_field_evidence_report([_match_id_ref()])

    assert report["object"] == runtime_evidence.RUNTIME_FIELD_EVIDENCE_REPORT_OBJECT
    assert report["schema_version"] == runtime_evidence.RUNTIME_FIELD_EVIDENCE_REPORT_VERSION
    assert report["status"] == "pass"
    assert report["review_required"] is False
    assert report["summary"]["field_ref_count"] == 1
    assert report["summary"]["attachment_count"] == 1
    assert report["summary"]["valid_field_evidence_count"] == 1
    assert report["missing_mappings"] == []
    assert report["ambiguous_mappings"] == []
    assert all(value is False for value in report["protected_surface_assertions"].values())


def test_report_shape_and_constants_match_contract() -> None:
    report = runtime_evidence.build_runtime_field_evidence_report([_match_id_ref()])

    assert runtime_evidence.RUNTIME_FIELD_EVIDENCE_REPORT_STATUSES == ("pass", "review", "fail")
    assert runtime_evidence.RUNTIME_FIELD_EVIDENCE_ATTACHMENT_SURFACES == (
        "local_review_sidecar",
        "synthetic_test_reference",
    )
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
        "attachments",
        "missing_mappings",
        "ambiguous_mappings",
        "validation_errors",
        "affected",
        "review_guidance",
        "drift_flags",
        "privacy",
        "protected_surface_assertions",
        "limitations",
    }
    assert _attachment(report)["object"] == runtime_evidence.RUNTIME_FIELD_EVIDENCE_ATTACHMENT_OBJECT


def test_attachment_field_evidence_records_validate_with_ledger_validator() -> None:
    report = runtime_evidence.build_runtime_field_evidence_report([_match_id_ref()])
    field_evidence = _attachment(report)["field_evidence"]

    assert evidence_ledger.validate_field_evidence(field_evidence) == []
    assert field_evidence["object"] == evidence_ledger.FIELD_EVIDENCE_OBJECT
    assert field_evidence["schema_version"] == evidence_ledger.FIELD_EVIDENCE_SCHEMA_VERSION
    assert field_evidence["ledger_version"] == evidence_ledger.LEDGER_VERSION


def test_exact_entry_id_mapping_wins_over_conflicting_field_names() -> None:
    report = runtime_evidence.build_runtime_field_evidence_report(
        [
            _match_id_ref(
                output_family="game_level_facts",
                output_field="game_number",
                display_name="Game Number",
            ),
        ],
    )

    attachment = _attachment(report)
    assert report["status"] == "pass"
    assert attachment["entry_id"] == "tier1.match_identity.match_id"
    assert attachment["output_family"] == "match_identity_and_lifecycle"
    assert attachment["review_notes"] == ["mapped_by:entry_id"]


def test_exact_output_family_and_output_field_mapping_works_without_entry_id() -> None:
    ref = _match_id_ref(entry_id="")

    report = runtime_evidence.build_runtime_field_evidence_report([ref])

    assert report["status"] == "pass"
    assert _attachment(report)["entry_id"] == "tier1.match_identity.match_id"
    assert _attachment(report)["review_notes"] == ["mapped_by:output_family_output_field"]


def test_display_name_mapping_works_only_when_unambiguous() -> None:
    ref = _match_id_ref(entry_id="", output_field="", display_name="MTGA Match ID")

    report = runtime_evidence.build_runtime_field_evidence_report([ref])

    assert report["status"] == "pass"
    assert _attachment(report)["entry_id"] == "tier1.match_identity.match_id"
    assert _attachment(report)["review_notes"] == ["mapped_by:output_family_display_name"]


def test_missing_mapping_produces_review_without_field_evidence_record() -> None:
    ref = _match_id_ref(entry_id="", output_field="missing_parser_field", display_name="")

    report = runtime_evidence.build_runtime_field_evidence_report([ref])

    assert report["status"] == "review"
    assert report["attachments"] == []
    assert report["summary"]["missing_mapping_count"] == 1
    assert report["missing_mappings"][0]["reason"] == "no_exact_mapping"


def test_ambiguous_display_name_mapping_does_not_choose_candidate() -> None:
    ledger = _ledger()
    duplicate = copy.deepcopy(ledger["entries"][0])
    duplicate["entry_id"] = "tier1.match_identity.match_id_duplicate"
    duplicate["output_field"] = "match_id_duplicate"
    ledger["entries"].append(duplicate)
    ref = _match_id_ref(entry_id="", output_field="", display_name="MTGA Match ID")

    report = runtime_evidence.build_runtime_field_evidence_report([ref], ledger=ledger)

    assert report["status"] == "review"
    assert report["attachments"] == []
    assert report["summary"]["ambiguous_mapping_count"] == 1
    assert report["ambiguous_mappings"][0]["candidate_entry_ids"] == [
        "tier1.match_identity.match_id",
        "tier1.match_identity.match_id_duplicate",
    ]


def test_unknown_vocabulary_label_fails_validation() -> None:
    report = runtime_evidence.build_runtime_field_evidence_report([_match_id_ref(value_source="not_a_source")])

    assert report["status"] == "fail"
    assert report["summary"]["failed_validation_count"] > 0
    assert any("field_evidence:value_source:unknown:not_a_source" in error for error in report["validation_errors"])


def test_unknown_drift_flag_fails_validation() -> None:
    report = runtime_evidence.build_runtime_field_evidence_report([_match_id_ref(drift_flags=["not_a_drift_flag"])])

    assert report["status"] == "fail"
    assert any("field_evidence:drift_flags:unknown:not_a_drift_flag" in error for error in report["validation_errors"])


def test_conflict_and_low_confidence_final_field_evidence_require_review() -> None:
    conflict_report = runtime_evidence.build_runtime_field_evidence_report([_match_id_ref(value_source="conflict")])
    low_final_report = runtime_evidence.build_runtime_field_evidence_report(
        [_match_id_ref(confidence="low", finality="final")],
    )

    assert conflict_report["status"] == "review"
    assert _attachment(conflict_report)["field_evidence"]["review_required"] is True
    assert "field_evidence_requires_review" in conflict_report["status_reasons"]
    assert low_final_report["status"] == "review"
    assert _attachment(low_final_report)["field_evidence"]["review_required"] is True


def test_failed_invariant_status_fails_report() -> None:
    report = runtime_evidence.build_runtime_field_evidence_report([_match_id_ref(invariant_status="failed")])

    assert report["status"] == "fail"
    assert _attachment(report)["field_evidence"]["review_required"] is True
    assert "field_invariant_failed" in report["status_reasons"]


def test_optional_missing_invariant_report_does_not_fail_by_default() -> None:
    report = runtime_evidence.build_runtime_field_evidence_report([_match_id_ref()])

    assert report["status"] == "pass"
    assert report["input_refs"]["invariant_execution_report"]["supplied"] is False
    assert report["input_refs"]["invariant_execution_report"]["required"] is False


def test_required_missing_invariant_report_fails() -> None:
    report = runtime_evidence.build_runtime_field_evidence_report(
        [_match_id_ref()],
        require_invariant_execution_report=True,
    )

    assert report["status"] == "fail"
    assert "invariant_execution_report_failed_or_missing" in report["status_reasons"]


def test_invariant_execution_report_review_degrades_report() -> None:
    invariant_report = {
        "object": "mythic_edge_player_log_evidence_invariant_execution_report",
        "schema_version": "player_log_evidence_invariant_execution.v1",
        "status": "review",
    }

    report = runtime_evidence.build_runtime_field_evidence_report(
        [_match_id_ref()],
        invariant_execution_report=invariant_report,
    )

    assert report["status"] == "review"
    assert "invariant_execution_report_requires_review" in report["status_reasons"]


def test_invariant_execution_report_fail_fails_report() -> None:
    invariant_report = {
        "object": "mythic_edge_player_log_evidence_invariant_execution_report",
        "schema_version": "player_log_evidence_invariant_execution.v1",
        "status": "fail",
    }

    report = runtime_evidence.build_runtime_field_evidence_report(
        [_match_id_ref()],
        invariant_execution_report=invariant_report,
    )

    assert report["status"] == "fail"
    assert "invariant_execution_report_failed_or_missing" in report["status_reasons"]


def test_privacy_findings_are_path_only_and_do_not_echo_raw_values() -> None:
    private_path = "/Users/example/private/Player.log"
    ref = _match_id_ref(
        entity_ref={
            "entity_type": "match",
            "stable_ref": private_path,
            "game_number": "",
            "action_index": "",
        },
    )

    report = runtime_evidence.build_runtime_field_evidence_report([ref])
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail"
    assert "field_refs[0].entity_ref.stable_ref" in report["privacy"]["local_absolute_paths_found"]
    assert private_path not in encoded
    assert _attachment(report)["entity_ref"]["stable_ref"] == ""


def test_malformed_surface_privacy_finding_does_not_echo_raw_value() -> None:
    private_path = "/Users/example/private/Player.log"

    report = runtime_evidence.build_runtime_field_evidence_report([_match_id_ref(surface=private_path)])
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail"
    assert "field_refs[0].surface" in report["privacy"]["local_absolute_paths_found"]
    assert "field_refs[0]:surface:unknown" in report["validation_errors"]
    assert private_path not in encoded


@pytest.mark.parametrize(
    ("overrides", "privacy_path", "record_key"),
    [
        (
            {"entry_id": "", "output_field": "/Users/example/private/Player.log", "display_name": ""},
            "field_refs[0].output_field",
            "output_field",
        ),
        (
            {"entry_id": "", "output_field": "", "display_name": "/Users/example/private/Player.log"},
            "field_refs[0].display_name",
            "display_name",
        ),
        (
            {
                "entry_id": "",
                "output_family": "/Users/example/private/Player.log",
                "output_field": "missing_parser_field",
                "display_name": "",
            },
            "field_refs[0].output_family",
            "output_family",
        ),
    ],
)
def test_missing_mapping_records_redact_private_field_reference_metadata(
    overrides: dict[str, object],
    privacy_path: str,
    record_key: str,
) -> None:
    private_path = "/Users/example/private/Player.log"

    report = runtime_evidence.build_runtime_field_evidence_report([_match_id_ref(**overrides)])
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail"
    assert privacy_path in report["privacy"]["local_absolute_paths_found"]
    assert report["summary"]["missing_mapping_count"] == 1
    assert report["missing_mappings"][0][record_key] == ""
    assert private_path not in encoded


def test_ambiguous_mapping_records_redact_private_field_reference_metadata() -> None:
    private_path = "/Users/example/private/Player.log"
    ledger = _ledger()
    duplicate = copy.deepcopy(ledger["entries"][0])
    duplicate["entry_id"] = "tier1.match_identity.match_id_duplicate"
    ledger["entries"].append(duplicate)
    ref = _match_id_ref(entry_id="", display_name=private_path)

    report = runtime_evidence.build_runtime_field_evidence_report([ref], ledger=ledger)
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail"
    assert "field_refs[0].display_name" in report["privacy"]["local_absolute_paths_found"]
    assert report["summary"]["ambiguous_mapping_count"] == 1
    assert report["ambiguous_mappings"][0]["display_name"] == ""
    assert private_path not in encoded


def test_field_value_key_is_forbidden_and_not_serialized() -> None:
    ref = _match_id_ref(value="raw-runtime-value")

    report = runtime_evidence.build_runtime_field_evidence_report([ref])
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail"
    assert report["privacy"]["field_values_included"] is True
    assert "field_refs[0].value" in report["privacy"]["forbidden_content_findings"]
    assert "raw-runtime-value" not in encoded


def test_write_report_rejects_forbidden_private_snippets(tmp_path) -> None:
    report = runtime_evidence.build_runtime_field_evidence_report([_match_id_ref()])
    report["review_guidance"]["review_notes"].append("inspect /Users/example/private.log")
    output_path = tmp_path / "field_evidence.json"

    with pytest.raises(ValueError, match="forbidden runtime field-evidence report content"):
        runtime_evidence.write_runtime_field_evidence_report(output_path, report)

    assert not output_path.exists()


def test_cli_returns_zero_for_pass_and_writes_explicit_outputs(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    refs_path = tmp_path / "field_refs.json"
    out_path = tmp_path / "reports" / "runtime_field_evidence.json"
    markdown_path = tmp_path / "reports" / "runtime_field_evidence.md"
    refs_path.write_text(json.dumps([_match_id_ref()]), encoding="utf-8")

    assert runtime_evidence.main(
        ["--check", "--field-refs", str(refs_path), "--out", str(out_path), "--markdown-out", str(markdown_path)],
    ) == 0
    captured = capsys.readouterr()

    assert '"status": "pass"' in captured.out
    assert json.loads(out_path.read_text(encoding="utf-8"))["object"] == (
        runtime_evidence.RUNTIME_FIELD_EVIDENCE_REPORT_OBJECT
    )
    assert "Runtime Field Evidence Report" in markdown_path.read_text(encoding="utf-8")


def test_cli_returns_zero_for_review_and_nonzero_for_fail(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    review_refs_path = tmp_path / "review_refs.json"
    fail_refs_path = tmp_path / "fail_refs.json"
    review_refs_path.write_text(
        json.dumps([_match_id_ref(entry_id="", output_field="missing_parser_field", display_name="")]),
        encoding="utf-8",
    )
    fail_refs_path.write_text(json.dumps([_match_id_ref(value_source="not_a_source")]), encoding="utf-8")

    assert runtime_evidence.main(["--check", "--field-refs", str(review_refs_path)]) == 0
    review_output = capsys.readouterr().out
    assert '"status": "review"' in review_output

    assert runtime_evidence.main(["--check", "--field-refs", str(fail_refs_path)]) == 1
    fail_output = capsys.readouterr().out
    assert '"status": "fail"' in fail_output


def test_existing_model_rows_do_not_gain_field_evidence_shape() -> None:
    match = MatchSummary("synthetic-match-1")
    game = GameSummary(1)
    match_row = match.to_match_log_row()
    game_row = game.to_game_log_row(match)

    assert "field_evidence" not in match_row
    assert "field_evidence" not in game_row
    assert "runtime_field_evidence" not in match_row
    assert "runtime_field_evidence" not in game_row
