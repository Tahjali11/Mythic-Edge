from __future__ import annotations

import copy
import json

import pytest

from mythic_edge_parser.app import field_recovery_matrix, parser_owned_fact_tracker


def _fact_by_id(matrix: dict, fact_id: str) -> dict:
    for fact in matrix["facts"]:
        if fact["fact_id"] == fact_id:
            return fact
    raise AssertionError(f"missing fact row: {fact_id}")


def _session(
    *,
    session_id: str,
    platform: str,
    source_kind: str,
    fact_id: str,
    from_status: str,
    to_status: str,
    candidate_summary_refs: list[str] | None = None,
    review_packet_refs: list[str] | None = None,
    reviewer_decision_refs: list[str] | None = None,
    promotion_proof_refs: list[str] | None = None,
    fixture_draft_refs: list[str] | None = None,
    promoted_fixture_refs: list[str] | None = None,
    source_window_ref: str = "synthetic.window.1",
) -> dict:
    return {
        "session_id": session_id,
        "platform": platform,
        "source_kind": source_kind,
        "scope": "competitive_current",
        "format_family": "standard",
        "queue_family": "traditional_bo3",
        "match_type": "traditional_bo3",
        "capture_started_at_utc": "2026-06-22T00:00:00Z",
        "capture_finished_at_utc": "2026-06-22T00:01:00Z",
        "source_window_ref": source_window_ref,
        "candidate_summary_refs": candidate_summary_refs or [],
        "review_packet_refs": review_packet_refs or [],
        "reviewer_decision_refs": reviewer_decision_refs or [],
        "promotion_proof_refs": promotion_proof_refs or [],
        "fixture_draft_refs": fixture_draft_refs or [],
        "promoted_fixture_refs": promoted_fixture_refs or [],
        "fact_deltas": [
            {
                "fact_id": fact_id,
                "from_status": from_status,
                "to_status": to_status,
                "evidence_ref": f"{session_id}.{fact_id.replace('.', '_')}",
                "rationale": "synthetic_metadata_only",
            }
        ],
        "privacy_scan": {
            "raw_private_values_included": False,
            "private_paths_included": False,
            "secret_values_included": False,
            "findings": [],
        },
        "environment_summary": {"platform": f"synthetic_{platform}"},
        "remaining_targets": [],
        "authorization_flags": {
            field: False for field in parser_owned_fact_tracker.AUTHORIZATION_FLAG_FIELDS
        },
        "non_claims": list(parser_owned_fact_tracker.REQUIRED_NON_CLAIMS),
    }


def test_default_target_matrix_builds_from_field_recovery_rows() -> None:
    matrix = parser_owned_fact_tracker.build_default_fact_target_matrix()

    assert matrix["object"] == parser_owned_fact_tracker.FACT_TARGET_MATRIX_OBJECT
    assert matrix["schema_version"] == (
        parser_owned_fact_tracker.FACT_TARGET_MATRIX_SCHEMA_VERSION
    )
    assert matrix["source_issue"] == parser_owned_fact_tracker.SOURCE_ISSUE
    assert matrix["pipeline_tracker"] == parser_owned_fact_tracker.PIPELINE_TRACKER
    assert matrix["parent_private_evidence_issue"] == (
        parser_owned_fact_tracker.PARENT_PRIVATE_EVIDENCE_ISSUE
    )
    assert matrix["target_matrix_status"] == "seed_matrix_ready"
    assert matrix["readiness_flags"] == {
        field: False for field in parser_owned_fact_tracker.READINESS_FLAG_FIELDS
    }
    assert matrix["authorization_flags"] == {
        field: False for field in parser_owned_fact_tracker.AUTHORIZATION_FLAG_FIELDS
    }
    assert matrix["non_claims"] == list(parser_owned_fact_tracker.REQUIRED_NON_CLAIMS)
    assert len(matrix["facts"]) == len(list(field_recovery_matrix.iter_field_recovery_rows()))
    assert matrix["summary"]["fact_count"] == len(matrix["facts"])
    assert matrix["summary"]["summary_is_readiness_metric"] is False
    assert parser_owned_fact_tracker.validate_fact_target_matrix(matrix) == []


def test_representative_fact_rows_keep_scope_boundaries() -> None:
    matrix = parser_owned_fact_tracker.build_default_fact_target_matrix()

    direct = _fact_by_id(matrix, "match.match_id")
    analytics = _fact_by_id(matrix, "analytics.card_performance")
    deck_state = _fact_by_id(matrix, "deck_state.game1_deck_state")
    private = _fact_by_id(matrix, "runtime_health.private_log_drift_window")
    external = _fact_by_id(matrix, "runtime_health.firewall_network_drop")

    assert direct["competitive_scope"] == "competitive_current"
    assert direct["current_lifecycle_status"] == "not_captured"
    assert direct["platform_status"]["windows"] == "not_captured"
    assert analytics["competitive_scope"] == "support_only"
    assert analytics["deferred_reason"] == "analytics_only_support"
    assert analytics["current_lifecycle_status"] == "out_of_scope_now"
    assert deck_state["competitive_scope"] == "deferred_feature_expansion"
    assert deck_state["current_lifecycle_status"] == "deferred_feature_expansion"
    assert private["current_lifecycle_status"] == "blocked_private_evidence"
    assert private["deferred_reason"] == "requires_private_evidence_approval"
    assert external["current_lifecycle_status"] == "blocked_external_boundary"
    assert external["deferred_reason"] == "requires_external_boundary_resolution"


def test_matrix_validator_rejects_true_flags_and_private_markers_without_echo() -> None:
    matrix = parser_owned_fact_tracker.build_default_fact_target_matrix()
    marker = "/" + "Users" + "/example/private/session"
    matrix["readiness_flags"]["parser_behavior_ready"] = True
    matrix["facts"][0]["parser_owner"] = marker

    errors = parser_owned_fact_tracker.validate_fact_target_matrix(matrix)

    assert "matrix:readiness_flags:parser_behavior_ready_must_remain_false" in errors
    assert "matrix:facts[0]:privacy:forbidden_text:fact.parser_owner" in errors
    assert marker not in json.dumps(errors)


def test_record_capture_session_appends_sanitized_private_capture() -> None:
    matrix = parser_owned_fact_tracker.build_default_fact_target_matrix()
    ledger = parser_owned_fact_tracker.build_empty_session_capture_ledger()
    session = _session(
        session_id="session.win.match-id.1",
        platform="windows",
        source_kind="user_selected_player_log",
        fact_id="match.match_id",
        from_status="not_captured",
        to_status="captured_private",
        source_window_ref="private.window.match-id.1",
    )

    updated = parser_owned_fact_tracker.record_capture_session(matrix, ledger, session)

    assert updated["summary"]["session_count"] == 1
    assert updated["summary"]["fact_delta_count"] == 1
    assert updated["privacy"]["raw_private_values_included"] is False
    assert updated["authorization_flags"] == {
        field: False for field in parser_owned_fact_tracker.AUTHORIZATION_FLAG_FIELDS
    }
    assert parser_owned_fact_tracker.validate_session_capture_ledger(updated) == []


def test_record_capture_session_rejects_forbidden_lifecycle_skip() -> None:
    matrix = parser_owned_fact_tracker.build_default_fact_target_matrix()
    ledger = parser_owned_fact_tracker.build_empty_session_capture_ledger()
    session = _session(
        session_id="session.win.skip.1",
        platform="windows",
        source_kind="synthetic_player_log",
        fact_id="match.match_id",
        from_status="not_captured",
        to_status="promoted_golden_fixture",
    )

    with pytest.raises(parser_owned_fact_tracker.ParserOwnedFactTrackerError) as exc_info:
        parser_owned_fact_tracker.record_capture_session(matrix, ledger, session)

    assert "delta:forbidden_lifecycle_transition" in str(exc_info.value)


def test_fact_lifecycle_statuses_require_matching_reference_ids() -> None:
    matrix = parser_owned_fact_tracker.build_default_fact_target_matrix()
    base_fact = _fact_by_id(matrix, "match.match_id")
    cases = [
        ("candidate_generated", "candidate_ids", "candidate.match-id.1"),
        ("review_packet_created", "review_packet_ids", "review.match-id.1"),
        ("human_approved", "review_packet_ids", "review.match-id.1"),
        ("promotion_proof_ready", "promotion_proof_ids", "proof.match-id.1"),
        ("fixture_manifest_draft_ready", "fixture_draft_ids", "draft.match-id.1"),
        ("promoted_golden_fixture", "promoted_fixture_ids", "fixture.match-id.1"),
        ("confirmed_windows", "promoted_fixture_ids", "fixture.match-id.1"),
        ("confirmed_macos", "promoted_fixture_ids", "fixture.match-id.1"),
        ("confirmed_cross_platform", "promoted_fixture_ids", "fixture.match-id.1"),
    ]

    for status, ref_field, ref_value in cases:
        fact = copy.deepcopy(base_fact)
        fact["current_lifecycle_status"] = status
        if status == "confirmed_cross_platform":
            fact["platform_status"] = {
                "windows": "confirmed",
                "macos": "confirmed",
                "cross_platform": "confirmed",
            }

        errors = parser_owned_fact_tracker.validate_fact_row(fact)

        expected = f"fact:lifecycle_status:{status}_requires_{ref_field}"
        assert expected in errors
        fact[ref_field] = [ref_value]
        assert expected not in parser_owned_fact_tracker.validate_fact_row(fact)


def test_session_lifecycle_deltas_require_matching_refs() -> None:
    matrix = parser_owned_fact_tracker.build_default_fact_target_matrix()
    ledger = parser_owned_fact_tracker.build_empty_session_capture_ledger()
    fact = _fact_by_id(matrix, "match.match_id")
    cases = [
        (
            "not_captured",
            "candidate_generated",
            "candidate_summary_refs",
            "candidate.match-id.1",
        ),
        (
            "candidate_generated",
            "review_packet_created",
            "review_packet_refs",
            "review.match-id.1",
        ),
        (
            "review_packet_created",
            "human_approved",
            "reviewer_decision_refs",
            "decision.match-id.1",
        ),
        (
            "human_approved",
            "promotion_proof_ready",
            "promotion_proof_refs",
            "proof.match-id.1",
        ),
        (
            "promotion_proof_ready",
            "fixture_manifest_draft_ready",
            "fixture_draft_refs",
            "draft.match-id.1",
        ),
        (
            "fixture_manifest_draft_ready",
            "promoted_golden_fixture",
            "promoted_fixture_refs",
            "fixture.match-id.1",
        ),
        (
            "promoted_golden_fixture",
            "confirmed_windows",
            "promoted_fixture_refs",
            "fixture.match-id.1",
        ),
        (
            "confirmed_windows",
            "confirmed_cross_platform",
            "promoted_fixture_refs",
            "fixture.match-id.1",
        ),
    ]

    for from_status, to_status, ref_field, ref_value in cases:
        fact["current_lifecycle_status"] = from_status
        session = _session(
            session_id=f"session.win.{to_status.replace('_', '-')}.1",
            platform="windows",
            source_kind="synthetic_fixture",
            fact_id="match.match_id",
            from_status=from_status,
            to_status=to_status,
        )

        errors = parser_owned_fact_tracker.validate_session_entry(
            session,
            matrix=matrix,
            ledger=ledger,
        )

        expected = f"session:fact_deltas[0]:delta:{to_status}_requires_{ref_field}"
        assert expected in errors
        session[ref_field] = [ref_value]
        assert expected not in parser_owned_fact_tracker.validate_session_entry(
            session,
            matrix=matrix,
            ledger=ledger,
        )


def test_private_source_kind_requires_private_or_blocked_delta() -> None:
    matrix = parser_owned_fact_tracker.build_default_fact_target_matrix()
    ledger = parser_owned_fact_tracker.build_empty_session_capture_ledger()
    session = _session(
        session_id="session.win.private.invalid.1",
        platform="windows",
        source_kind="user_selected_player_log",
        fact_id="match.match_id",
        from_status="not_captured",
        to_status="review_required",
        source_window_ref="private.window.invalid.1",
    )

    errors = parser_owned_fact_tracker.validate_session_entry(
        session,
        matrix=matrix,
        ledger=ledger,
    )

    assert "session:private_source_kind_requires_private_or_blocked_delta" in errors


def test_progress_report_summarizes_candidates_and_remaining_gaps() -> None:
    matrix = parser_owned_fact_tracker.build_default_fact_target_matrix()
    ledger = parser_owned_fact_tracker.build_empty_session_capture_ledger()
    ledger = parser_owned_fact_tracker.record_capture_session(
        matrix,
        ledger,
        _session(
            session_id="session.win.match-id.1",
            platform="windows",
            source_kind="user_selected_player_log",
            fact_id="match.match_id",
            from_status="not_captured",
            to_status="captured_private",
            source_window_ref="private.window.match-id.1",
        ),
    )
    ledger = parser_owned_fact_tracker.record_capture_session(
        matrix,
        ledger,
        _session(
            session_id="session.win.match-id.2",
            platform="windows",
            source_kind="local_harvest_candidate_summary",
            fact_id="match.match_id",
            from_status="captured_private",
            to_status="candidate_generated",
            candidate_summary_refs=["candidate.match-id.1"],
        ),
    )

    report = parser_owned_fact_tracker.build_coverage_progress_report(matrix, ledger)

    assert report["summary_counts"]["fact_count"] == len(matrix["facts"])
    assert report["summary_counts"]["parser_behavior_ready_fact_count"] == 0
    assert report["summary_counts"]["pipeline_activation_ready_fact_count"] == 0
    assert report["new_private_captures"] == ["session.win.match-id.1:match.match_id"]
    assert report["new_candidates_generated"] == ["candidate.match-id.1"]
    assert "match.match_id" in report["current_competitive_scope_gaps"]
    assert "deck_state.game1_deck_state" in report["deferred_feature_expansion_facts"]
    assert "runtime_health.private_log_drift_window" in report["blocked_or_review_required"]
    assert report["privacy"]["raw_private_values_included"] is False
    assert parser_owned_fact_tracker.validate_coverage_progress_report(report) == []


def test_cross_platform_confirmation_requires_both_platforms() -> None:
    matrix = parser_owned_fact_tracker.build_default_fact_target_matrix()
    fact = _fact_by_id(matrix, "match.match_id")
    fact["current_lifecycle_status"] = "confirmed_cross_platform"
    fact["platform_status"] = {
        "windows": "confirmed",
        "macos": "not_captured",
        "cross_platform": "confirmed",
    }
    matrix["summary"] = {
        **matrix["summary"],
        "lifecycle_counts": {
            **matrix["summary"]["lifecycle_counts"],
            "confirmed_cross_platform": 1,
        },
    }

    errors = parser_owned_fact_tracker.validate_fact_row(fact)

    assert "fact:cross_platform_requires_windows_and_macos_confirmation" in errors


def test_report_validator_rejects_readiness_and_parser_behavior_overclaims() -> None:
    matrix = parser_owned_fact_tracker.build_default_fact_target_matrix()
    ledger = parser_owned_fact_tracker.build_empty_session_capture_ledger()
    report = parser_owned_fact_tracker.build_coverage_progress_report(matrix, ledger)
    report["validation"]["parser_behavior_changed"] = True
    report["authorization_flags"]["fixture_promotion_authorized"] = True

    errors = parser_owned_fact_tracker.validate_coverage_progress_report(report)

    assert "report:validation:parser_behavior_changed_must_remain_false" in errors
    assert (
        "report:authorization_flags:fixture_promotion_authorized_must_remain_false"
        in errors
    )


def test_iterated_objects_are_copy_safe() -> None:
    matrix = parser_owned_fact_tracker.build_default_fact_target_matrix()
    mutated = copy.deepcopy(matrix)
    mutated["facts"][0]["fact_id"] = "mutated.fact"

    fresh = parser_owned_fact_tracker.build_default_fact_target_matrix()

    assert fresh["facts"][0]["fact_id"] == "match.match_id"
