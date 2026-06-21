from __future__ import annotations

import copy
import json

from mythic_edge_parser.app import evidence_ledger, field_recovery_matrix


def _row_by_id(field_id: str) -> dict:
    for row in field_recovery_matrix.iter_field_recovery_rows():
        if row["field_id"] == field_id:
            return row
    raise AssertionError(f"missing recovery row: {field_id}")


def test_build_field_recovery_matrix_shape_and_false_flags() -> None:
    matrix = field_recovery_matrix.build_field_recovery_matrix()

    assert matrix["object"] == field_recovery_matrix.FIELD_RECOVERY_MATRIX_OBJECT
    assert matrix["schema_version"] == field_recovery_matrix.FIELD_RECOVERY_MATRIX_SCHEMA_VERSION
    assert matrix["source_issue"] == field_recovery_matrix.SOURCE_ISSUE
    assert matrix["pipeline_tracker"] == field_recovery_matrix.PIPELINE_TRACKER
    assert matrix["parent_private_evidence_issue"] == (
        field_recovery_matrix.PARENT_PRIVATE_EVIDENCE_ISSUE
    )
    assert matrix["status"] == "planning_matrix_ready"
    for flag in field_recovery_matrix.FALSE_READINESS_FLAGS:
        assert matrix[flag] is False
    assert matrix["non_claims"] == list(field_recovery_matrix.REQUIRED_NON_CLAIMS)
    assert field_recovery_matrix.validate_field_recovery_matrix(matrix) == []


def test_representative_rows_cover_recovery_categories_and_vocabularies() -> None:
    matrix = field_recovery_matrix.build_field_recovery_matrix()
    rows = matrix["rows"]

    assert {row["recovery_category"] for row in rows} == set(
        field_recovery_matrix.RECOVERY_CATEGORIES
    )
    assert {row["minimum_confidence"] for row in rows} <= set(
        evidence_ledger.CONFIDENCE_LEVELS
    )
    for row in rows:
        assert set(row["allowed_finality"]) <= set(evidence_ledger.FINALITY_LABELS)
        assert set(row["degradation_flags"]) <= set(evidence_ledger.DRIFT_FLAGS)
        assert row["non_claims"] == list(field_recovery_matrix.REQUIRED_NON_CLAIMS)
        assert field_recovery_matrix.validate_field_recovery_row(row) == []


def test_matrix_summary_is_deterministic_and_not_readiness_metric() -> None:
    first = field_recovery_matrix.build_field_recovery_matrix()
    second = field_recovery_matrix.build_field_recovery_matrix()

    assert first == second
    assert first["matrix_summary"]["row_count"] == len(first["rows"])
    assert first["matrix_summary"]["summary_is_readiness_metric"] is False
    encoded = json.dumps(first, indent=2, sort_keys=True, ensure_ascii=False)
    assert json.loads(encoded) == first


def test_iter_rows_is_copy_safe() -> None:
    first_row = next(iter(field_recovery_matrix.iter_field_recovery_rows()))
    first_row["field_id"] = "mutated.field"
    first_row["restoration_requirements"].append("mutated")

    fresh_row = next(iter(field_recovery_matrix.iter_field_recovery_rows()))

    assert fresh_row["field_id"] == "match.match_id"
    assert "mutated" not in fresh_row["restoration_requirements"]


def test_approximate_and_blocked_rows_cannot_restore_parser_output() -> None:
    approximate = _row_by_id("analytics.card_performance")
    approximate["parser_output_policy"] = "preserve_existing_parser_behavior"
    approximate["minimum_confidence"] = "high"

    approximate_errors = field_recovery_matrix.validate_field_recovery_row(approximate)

    assert (
        "row:blocked_truth_boundary_violation:non_direct_preserves_parser_behavior"
        in approximate_errors
    )
    assert (
        "row:approximate_analytics_only_cannot_restore_parser_output"
        in approximate_errors
    )
    assert "row:approximate_analytics_only_confidence_too_high" in approximate_errors

    blocked_private = _row_by_id("runtime_health.private_log_drift_window")
    blocked_private["parser_output_policy"] = "blank_or_unknown_until_recovered"
    blocked_private["minimum_confidence"] = "medium"

    blocked_errors = field_recovery_matrix.validate_field_recovery_row(blocked_private)

    assert "row:blocked_private_evidence_requires_private_review_policy" in blocked_errors
    assert "row:blocked_private_evidence_confidence_too_high" in blocked_errors


def test_non_direct_rows_require_review_and_cannot_claim_existing_parser_behavior() -> None:
    equivalent = _row_by_id("match.event_id")
    equivalent["review_required"] = False
    equivalent["parser_output_policy"] = "preserve_existing_parser_behavior"

    errors = field_recovery_matrix.validate_field_recovery_row(equivalent)

    assert "row:blocked_truth_boundary_violation:non_direct_preserves_parser_behavior" in errors
    assert "row:equivalent_requires_parser_contract_and_fixture_review" in errors
    assert "row:equivalent_requires_review" in errors
    assert "row:non_direct_or_blocked_category_requires_review" in errors


def test_unknown_ledger_entry_requires_review_and_is_reported() -> None:
    direct = _row_by_id("match.match_id")
    direct["evidence_ledger_entry_ids"].append("tier9.unknown.field")

    errors = field_recovery_matrix.validate_field_recovery_row(direct)

    assert "row:evidence_ledger_entry_ids:unknown:tier9.unknown.field" in errors
    assert "row:evidence_ledger_entry_ids:unknown_requires_review_required" in errors

    review_row = copy.deepcopy(direct)
    review_row["review_required"] = True
    review_errors = field_recovery_matrix.validate_field_recovery_row(review_row)

    assert "row:evidence_ledger_entry_ids:unknown:tier9.unknown.field" in review_errors
    assert (
        "row:evidence_ledger_entry_ids:unknown_requires_review_required"
        not in review_errors
    )


def test_matrix_validator_rejects_true_readiness_flags() -> None:
    matrix = field_recovery_matrix.build_field_recovery_matrix()
    matrix["parser_behavior_ready"] = True
    matrix["pipeline_activation_ready_for_issue_388"] = True

    errors = field_recovery_matrix.validate_field_recovery_matrix(matrix)

    assert "matrix:parser_behavior_ready_must_remain_false" in errors
    assert "matrix:pipeline_activation_ready_for_issue_388_must_remain_false" in errors


def test_validator_rejects_private_markers_absolute_paths_and_non_claim_drift() -> None:
    row = _row_by_id("match.match_id")
    row["parser_owner"] = "/" + "Users" + "/example/state.py"
    row["required_direct_evidence"].append("[" + "UnityCrossThreadLogger" + "] private")
    row["non_claims"].remove("not_parser_truth")

    errors = field_recovery_matrix.validate_field_recovery_row(row)

    assert "privacy:absolute_path:row.parser_owner" in errors
    assert "privacy:forbidden_text:row.required_direct_evidence[1]" in errors
    assert "row:non_claims:mismatch" in errors


def test_validator_rejects_embedded_local_paths_without_echoing_values() -> None:
    row = _row_by_id("match.match_id")
    unix_path = "/" + "Users" + "/example/private/session"
    windows_path = "C:" + "\\Users\\example\\private\\session"
    colon_path = "local_path:" + "/" + "Users" + "/example/private/session"
    file_uri = "file://" + "/" + "Users" + "/example/private/session"
    row["restoration_requirements"].append(f"review evidence stored at {unix_path}")
    row["restoration_requirements"].append(f"review evidence stored at {colon_path}")
    row["restoration_requirements"].append(f"review evidence stored at {file_uri}")
    row["forbidden_fallback_evidence"].append(f"local artifact {windows_path}")

    errors = field_recovery_matrix.validate_field_recovery_row(row)

    assert "privacy:absolute_path:row.restoration_requirements[2]" in errors
    assert "privacy:absolute_path:row.restoration_requirements[3]" in errors
    assert "privacy:absolute_path:row.restoration_requirements[4]" in errors
    assert "privacy:absolute_path:row.forbidden_fallback_evidence[4]" in errors
    assert unix_path not in json.dumps(errors)
    assert windows_path not in json.dumps(errors)
    assert colon_path not in json.dumps(errors)
    assert file_uri not in json.dumps(errors)


def test_matrix_validator_reports_duplicate_field_ids() -> None:
    matrix = field_recovery_matrix.build_field_recovery_matrix()
    matrix["rows"].append(copy.deepcopy(matrix["rows"][0]))
    matrix["matrix_summary"] = {
        **matrix["matrix_summary"],
        "row_count": len(matrix["rows"]),
    }

    errors = field_recovery_matrix.validate_field_recovery_matrix(matrix)

    assert "duplicate_field_id:match.match_id" in errors
