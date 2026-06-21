from __future__ import annotations

import copy
import json

from mythic_edge_parser.app import (
    field_evidence_comparison_report as comparison,
)
from mythic_edge_parser.app import (
    field_recovery_matrix,
)
from mythic_edge_parser.app import (
    local_watcher_offset_window_monitor as monitor,
)


def _matrix_row(field_id: str) -> dict:
    for row in field_recovery_matrix.iter_field_recovery_rows():
        if row["field_id"] == field_id:
            return row
    raise AssertionError(f"missing matrix row: {field_id}")


def _current(
    field_id: str,
    *,
    ledger_ids: list[str] | None = None,
    signals: list[str] | None = None,
    value_source: str = "observed",
    confidence: str = "high",
    finality: str = "final",
    degradation_flags: list[str] | None = None,
    invariant_status: str = "passed",
    stale_source_status: str = "fresh",
    review_required: bool = False,
    source_window_refs: list[str] | None = None,
) -> dict:
    return {
        "object": comparison.FIELD_EVIDENCE_CURRENT_OBJECT,
        "schema_version": comparison.FIELD_EVIDENCE_COMPARISON_SCHEMA_VERSION,
        "field_id": field_id,
        "evidence_ledger_entry_ids": ledger_ids or [],
        "observed_signal_ids": signals or [],
        "source_event_families": ["synthetic_public_fixture"],
        "source_event_kinds": ["synthetic_event"],
        "value_source": value_source,
        "confidence": confidence,
        "finality": finality,
        "degradation_flags": degradation_flags or [],
        "invariant_status": invariant_status,
        "stale_source_status": stale_source_status,
        "source_window_refs": source_window_refs or [],
        "review_required": review_required,
        "contents_read": False,
        "raw_path_included": False,
        "raw_hash_included": False,
        "raw_payload_values_included": False,
        "private_excerpt_included": False,
    }


def _watcher_report(window_status: str) -> dict:
    source = monitor.describe_source_selection(
        source_label="synthetic_player_log",
        source_class="synthetic_player_log",
    )
    window = monitor.start_offset_window(
        source_selection=source,
        start_metadata={
            "source_label": "synthetic_player_log",
            "source_generation": "generation_a",
            "size_bytes": 1,
            "exists": True,
        },
        window_id="window_a",
    )
    window["window_status"] = window_status
    window["stale_window_status"] = window_status
    window["review_required"] = window_status not in {"window_ready", "window_closed"}
    return monitor.build_offset_window_monitor_report(
        source_selection=source,
        windows=[window],
    )


def test_report_shape_false_flags_and_deterministic_serialization() -> None:
    report = comparison.build_field_evidence_comparison_report()

    assert report["object"] == comparison.FIELD_EVIDENCE_COMPARISON_REPORT_OBJECT
    assert report["schema_version"] == comparison.FIELD_EVIDENCE_COMPARISON_SCHEMA_VERSION
    assert report["source_issue"] == comparison.SOURCE_ISSUE
    assert report["pipeline_tracker"] == comparison.PIPELINE_TRACKER
    assert report["parent_private_evidence_issue"] == comparison.PARENT_PRIVATE_EVIDENCE_ISSUE
    for flag in comparison.FALSE_READINESS_FLAGS:
        assert report[flag] is False
    assert report["summary"]["summary_is_readiness_metric"] is False
    assert report["non_claims"] == list(comparison.REQUIRED_NON_CLAIMS)
    assert comparison.validate_field_evidence_comparison_report(report) == []
    encoded = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False)
    assert json.loads(encoded) == report


def test_direct_comparison_success_preserves_existing_parser_policy() -> None:
    row = comparison.compare_field_evidence(
        _matrix_row("match.match_id"),
        _current(
            "match.match_id",
            ledger_ids=["tier1.match_identity.match_id"],
            signals=["match_state.match_id"],
        ),
    )

    assert row["object"] == comparison.FIELD_EVIDENCE_COMPARISON_ROW_OBJECT
    assert row["comparison_status"] == "direct"
    assert row["confidence"] == "high"
    assert row["review_required"] is False
    assert row["parser_output_policy"] == "preserve_existing_parser_behavior"
    assert "existing_parser_behavior_sufficient" in row["candidate_recovery_hints"]
    assert comparison.validate_field_evidence_comparison_row(row) == []


def test_direct_comparator_claim_bypass_inputs_are_invalid() -> None:
    cases = []

    current_claim = _current(
        "match.match_id",
        ledger_ids=["tier1.match_identity.match_id"],
        signals=["match_state.match_id"],
    )
    current_claim["parserBehaviorReady"] = True
    cases.append((_matrix_row("match.match_id"), current_claim, None))

    current_protected_claim = _current(
        "match.match_id",
        ledger_ids=["tier1.match_identity.match_id"],
        signals=["match_state.match_id"],
    )
    current_protected_claim["protectedSurfaceAssertions"] = {
        "parserBehaviorChanged": True,
    }
    cases.append((_matrix_row("match.match_id"), current_protected_claim, None))

    matrix_claim = _matrix_row("match.match_id")
    matrix_claim["private_harvest_authorized"] = True
    cases.append(
        (
            matrix_claim,
            _current(
                "match.match_id",
                ledger_ids=["tier1.match_identity.match_id"],
                signals=["match_state.match_id"],
            ),
            None,
        )
    )

    watcher_claim = {
        "protected_surface_assertions": {
            "parser_behavior_changed": True,
        }
    }
    cases.append(
        (
            _matrix_row("match.match_id"),
            _current(
                "match.match_id",
                ledger_ids=["tier1.match_identity.match_id"],
                signals=["match_state.match_id"],
            ),
            watcher_claim,
        )
    )

    for matrix_row, current, watcher_context in cases:
        row = comparison.compare_field_evidence(
            matrix_row,
            current,
            watcher_context=watcher_context,
        )

        assert row["comparison_status"] == "invalid_input"
        assert row["review_required"] is True
        assert "privacy_or_forbidden_marker" in row["stop_reasons"]
        assert "blocked_by_policy" in row["candidate_recovery_hints"]
        assert comparison.validate_field_evidence_comparison_row(row) == []


def test_equivalent_and_derived_comparisons_are_capped_and_review_required() -> None:
    equivalent = comparison.compare_field_evidence(
        _matrix_row("match.event_id"),
        _current(
            "match.event_id",
            ledger_ids=["tier2.queue_format_rank_event_context.event_id"],
            signals=["match_state.event_id.player_fallback"],
            finality="live",
        ),
    )
    derived = comparison.compare_field_evidence(
        _matrix_row("game.game1_result"),
        _current(
            "game.game1_result",
            ledger_ids=["tier3.game_results.game1_result"],
            signals=["game_result.game1.result", "participant.player_team_mapping"],
            finality="reconciled",
        ),
    )

    assert equivalent["comparison_status"] == "equivalent"
    assert equivalent["confidence"] == "medium"
    assert equivalent["review_required"] is True
    assert "needs_parser_contract" in equivalent["candidate_recovery_hints"]
    assert derived["comparison_status"] == "derived_bounded"
    assert derived["confidence"] == "medium"
    assert derived["review_required"] is True
    assert comparison.validate_field_evidence_comparison_row(equivalent) == []
    assert comparison.validate_field_evidence_comparison_row(derived) == []


def test_approximate_analytics_only_never_restores_parser_output() -> None:
    row = comparison.compare_field_evidence(
        _matrix_row("analytics.card_performance"),
        _current(
            "analytics.card_performance",
            ledger_ids=["tier7.derived_analytics_outputs.card_performance"],
            signals=["parser_owned_game_and_card_identity_summaries"],
            confidence="high",
            finality="provisional",
        ),
    )

    assert row["comparison_status"] == "approximate_analytics_only"
    assert row["confidence"] == "low"
    assert row["parser_output_policy"] == "never_parser_truth_analytics_only"
    assert "analytics_display_only" in row["candidate_recovery_hints"]
    assert row["review_required"] is True


def test_unavailable_and_blocked_rows_remain_non_claims() -> None:
    unavailable = comparison.compare_field_evidence(_matrix_row("deck_state.game1_deck_state"))
    private = comparison.compare_field_evidence(
        _matrix_row("runtime_health.private_log_drift_window")
    )
    external = comparison.compare_field_evidence(
        _matrix_row("runtime_health.firewall_network_drop")
    )

    assert unavailable["comparison_status"] == "unavailable"
    assert private["comparison_status"] == "blocked_private_evidence"
    assert external["comparison_status"] == "blocked_external_boundary"
    for row in (unavailable, private, external):
        assert row["review_required"] is True
        assert "no_recovery_authorized" in row["candidate_recovery_hints"]


def test_watcher_stale_context_routes_affected_field_to_stale() -> None:
    row = comparison.compare_field_evidence(
        _matrix_row("match.match_id"),
        _current(
            "match.match_id",
            ledger_ids=["tier1.match_identity.match_id"],
            signals=["match_state.match_id"],
            source_window_refs=["window_a"],
        ),
        watcher_context=_watcher_report("window_stale"),
    )

    assert row["comparison_status"] == "stale"
    assert row["stale_source_status"] == "stale"
    assert row["watcher_window_status"] == "window_stale"
    assert "needs_stale_source_refresh" in row["candidate_recovery_hints"]


def test_degraded_and_conflicting_current_evidence_route_to_review() -> None:
    degraded = comparison.compare_field_evidence(
        _matrix_row("match.match_id"),
        _current(
            "match.match_id",
            ledger_ids=["tier1.match_identity.match_id"],
            signals=["match_state.match_id"],
            degradation_flags=["fallback_used"],
        ),
    )
    conflict = comparison.compare_field_evidence(
        _matrix_row("match.match_id"),
        _current(
            "match.match_id",
            ledger_ids=["tier1.match_identity.match_id"],
            signals=["match_state.match_id"],
            value_source="conflict",
            invariant_status="failed",
        ),
    )

    assert degraded["comparison_status"] == "degraded"
    assert degraded["review_required"] is True
    assert conflict["comparison_status"] == "conflict"
    assert conflict["review_required"] is True


def test_unknown_field_ids_and_unknown_ledger_ids_require_review() -> None:
    report = comparison.build_field_evidence_comparison_report(
        field_recovery_matrix_report={
            **field_recovery_matrix.build_field_recovery_matrix(),
            "rows": [_matrix_row("match.match_id")],
            "matrix_summary": {
                "row_count": 1,
                "recovery_category_counts": {
                    value: int(value == "direct")
                    for value in field_recovery_matrix.RECOVERY_CATEGORIES
                },
                "parser_output_policy_counts": {
                    value: int(value == "preserve_existing_parser_behavior")
                    for value in field_recovery_matrix.PARSER_OUTPUT_POLICIES
                },
                "review_required_count": 0,
                "summary_is_readiness_metric": False,
            },
        },
        current_field_evidence=[
            _current(
                "match.match_id",
                ledger_ids=["tier9.unknown.field"],
                signals=["match_state.match_id"],
            ),
            _current("unknown.field", signals=["unknown.signal"]),
        ],
    )

    by_field = {row["field_id"]: row for row in report["rows"]}

    assert by_field["match.match_id"]["comparison_status"] == "review_required"
    assert "unknown_evidence_ledger_entry" in by_field["match.match_id"]["stop_reasons"]
    assert by_field["unknown.field"]["comparison_status"] == "review_required"
    assert "needs_field_matrix_update" in by_field["unknown.field"]["candidate_recovery_hints"]
    assert comparison.validate_field_evidence_comparison_report(report) == []


def test_invalid_input_and_privacy_markers_fail_closed_without_value_echo() -> None:
    private_path = "/" + "Users" + "/example/private/" + "Player" + ".log"
    bad_current = _current(
        "match.match_id",
        ledger_ids=["tier1.match_identity.match_id"],
        signals=["match_state.match_id"],
        source_window_refs=[private_path],
    )
    bad_current["raw_hash"] = "private-content-hash"

    report = comparison.build_field_evidence_comparison_report(
        current_field_evidence=[bad_current]
    )
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail_closed"
    assert private_path not in encoded
    assert "private-content-hash" not in encoded
    assert any(
        reason == "privacy_or_protected_surface_violation"
        for reason in report["status_reasons"]
    )


def test_context_readiness_and_authorization_claims_fail_closed() -> None:
    flags = tuple(comparison.FALSE_READINESS_FLAGS) + ("parserBehaviorReady",)
    for flag in flags:
        report = comparison.build_field_evidence_comparison_report(
            context={"validation_context": {flag: True}}
        )

        assert report["status"] == "fail_closed"
        if flag in comparison.FALSE_READINESS_FLAGS:
            assert report[flag] is False
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        assert comparison.validate_field_evidence_comparison_report(report) == []


def test_context_protected_surface_claims_fail_closed() -> None:
    contexts = (
        {
            "protected_surface_assertions": {
                "parser_behavior_changed": True,
                "future_surface_changed": True,
            }
        },
        {
            "validation_context": {
                "workbook_or_webhook_surface_changed": True,
                "parserBehaviorChanged": True,
            },
        },
    )

    for context in contexts:
        report = comparison.build_field_evidence_comparison_report(context=context)

        assert report["status"] == "fail_closed"
        assert all(
            value is False
            for value in report["protected_surface_assertions"].values()
        )
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        assert comparison.validate_field_evidence_comparison_report(report) == []


def test_current_evidence_claims_fail_closed_before_normalization() -> None:
    cases = (
        {"parser_behavior_ready": True},
        {"private_harvest_authorized": True},
        {"parserBehaviorReady": True},
        {"protected_surface_assertions": {"parser_behavior_changed": True}},
        {"protected_surface_assertions": True},
        {"protectedSurfaceAssertions": {"future_surface_changed": True}},
    )

    for claim in cases:
        current = _current(
            "match.match_id",
            ledger_ids=["tier1.match_identity.match_id"],
            signals=["match_state.match_id"],
        )
        current.update(claim)

        report = comparison.build_field_evidence_comparison_report(
            current_field_evidence=[current]
        )

        assert report["status"] == "fail_closed"
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        assert comparison.validate_field_evidence_comparison_report(report) == []


def test_matrix_and_watcher_claims_fail_closed() -> None:
    matrix = field_recovery_matrix.build_field_recovery_matrix()
    matrix["parser_behavior_ready"] = True
    matrix_report = comparison.build_field_evidence_comparison_report(
        field_recovery_matrix_report=matrix
    )

    watcher_report = comparison.build_field_evidence_comparison_report(
        watcher_context={
            "protected_surface_assertions": {
                "parser_behavior_changed": True,
            }
        }
    )

    for report in (matrix_report, watcher_report):
        assert report["status"] == "fail_closed"
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        assert comparison.validate_field_evidence_comparison_report(report) == []


def test_inputs_are_copy_safe() -> None:
    current = _current(
        "match.match_id",
        ledger_ids=["tier1.match_identity.match_id"],
        signals=["match_state.match_id"],
    )
    matrix_row = _matrix_row("match.match_id")
    current_before = copy.deepcopy(current)
    matrix_before = copy.deepcopy(matrix_row)

    row = comparison.compare_field_evidence(matrix_row, current)
    row["current_evidence"]["observed_signal_ids"].append("mutated")
    row["expected_evidence"]["required_direct_evidence"].append("mutated")

    assert current == current_before
    assert matrix_row == matrix_before


def test_no_parser_runtime_imports_are_used() -> None:
    imported = set(comparison.__dict__)

    assert "router" not in imported
    assert "state" not in imported
    assert "FileTailer" not in imported
