from __future__ import annotations

import inspect
import json

from mythic_edge_parser.app import field_evidence_comparison_report as comparison
from mythic_edge_parser.app import field_recovery_matrix
from mythic_edge_parser.app import local_watcher_offset_window_monitor as monitor
from mythic_edge_parser.app import recovery_candidate_packet_generator as packets


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


def test_candidate_report_shape_false_flags_and_deterministic_serialization() -> None:
    report = packets.build_recovery_candidate_packet_report(
        reduced_evidence_summaries=[
            _current(
                "match.match_id",
                ledger_ids=["tier1.match_identity.match_id"],
                signals=["match_state.match_id"],
            )
        ]
    )

    assert report["object"] == packets.RECOVERY_CANDIDATE_PACKET_REPORT_OBJECT
    assert report["schema_version"] == packets.RECOVERY_CANDIDATE_PACKET_SCHEMA_VERSION
    assert report["source_issue"] == packets.SOURCE_ISSUE
    assert report["pipeline_tracker"] == packets.PIPELINE_TRACKER
    assert report["parent_private_evidence_issue"] == packets.PARENT_PRIVATE_EVIDENCE_ISSUE
    for flag in packets.FALSE_READINESS_FLAGS:
        assert report[flag] is False
    assert report["summary"]["summary_is_readiness_metric"] is False
    assert report["non_claims"] == list(packets.REQUIRED_NON_CLAIMS)
    assert packets.validate_recovery_candidate_packet_report(report) == []
    encoded = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False)
    assert json.loads(encoded) == report


def test_direct_packet_is_review_only_and_preserves_existing_parser_boundary() -> None:
    comparison_row = comparison.compare_field_evidence(
        _matrix_row("match.match_id"),
        _current(
            "match.match_id",
            ledger_ids=["tier1.match_identity.match_id"],
            signals=["match_state.match_id"],
        ),
    )

    packet = packets.build_recovery_candidate_packet(
        comparison_row,
        field_recovery_matrix.build_field_recovery_matrix(),
    )

    assert packet["candidate_status"] == "candidate_ready_for_review"
    assert packet["candidate_category"] == "direct_preservation_candidate"
    assert packet["review_required"] is False
    assert packet["next_role_hint"] == "review_only"
    assert packet["reviewer_decision"]["decision"] == "undecided"
    assert packet["reviewer_decision"]["allowed_next_step"] == "review_only"
    assert packet["reviewer_decision"]["requires_parser_contract"] is False
    assert "not_parser_truth" in packet["non_claims"]
    assert packets.validate_recovery_candidate_packet(packet) == []


def test_direct_packet_builder_fail_closes_forbidden_comparison_row_keys() -> None:
    comparison_row = comparison.compare_field_evidence(
        _matrix_row("match.match_id"),
        _current(
            "match.match_id",
            ledger_ids=["tier1.match_identity.match_id"],
            signals=["match_state.match_id"],
        ),
    )
    comparison_row["raw_payload"] = {"public": "caller_supplied_raw_packet_value"}
    comparison_row["current_evidence"]["raw_hash"] = "caller_supplied_raw_hash_value"

    packet = packets.build_recovery_candidate_packet(
        comparison_row,
        field_recovery_matrix.build_field_recovery_matrix(),
    )
    encoded = json.dumps(packet, sort_keys=True)

    assert packet["candidate_status"] == "blocked_privacy"
    assert packet["candidate_category"] == "unsupported_claim_blocked"
    assert packet["privacy_status"] == "blocked_local_artifact"
    assert packet["review_required"] is True
    assert packet["next_role_hint"] == "blocked"
    assert "privacy_or_forbidden_marker" in packet["stop_reasons"]
    assert "caller_supplied_raw_packet_value" not in encoded
    assert "caller_supplied_raw_hash_value" not in encoded
    assert packets.validate_recovery_candidate_packet(packet) == []


def test_equivalent_derived_and_approximate_packets_remain_review_metadata() -> None:
    equivalent = packets.build_recovery_candidate_packet(
        comparison.compare_field_evidence(
            _matrix_row("match.event_id"),
            _current(
                "match.event_id",
                ledger_ids=["tier2.queue_format_rank_event_context.event_id"],
                signals=["match_state.event_id.player_fallback"],
                finality="live",
            ),
        )
    )
    derived = packets.build_recovery_candidate_packet(
        comparison.compare_field_evidence(
            _matrix_row("game.game1_result"),
            _current(
                "game.game1_result",
                ledger_ids=["tier3.game_results.game1_result"],
                signals=["game_result.game1.result", "participant.player_team_mapping"],
                finality="reconciled",
            ),
        )
    )
    approximate = packets.build_recovery_candidate_packet(
        comparison.compare_field_evidence(
            _matrix_row("analytics.card_performance"),
            _current(
                "analytics.card_performance",
                ledger_ids=["tier7.derived_analytics_outputs.card_performance"],
                signals=["parser_owned_game_and_card_identity_summaries"],
                confidence="high",
                finality="provisional",
            ),
        )
    )

    assert equivalent["candidate_status"] == "review_required"
    assert equivalent["candidate_category"] == "equivalent_mapping_candidate"
    assert equivalent["reviewer_decision"]["allowed_next_step"] == "parser_contract"
    assert derived["candidate_status"] == "review_required"
    assert derived["candidate_category"] == "derived_bounded_candidate"
    assert derived["reviewer_decision"]["allowed_next_step"] == "parser_contract"
    assert approximate["candidate_status"] == "review_required"
    assert approximate["candidate_category"] == "analytics_display_only_candidate"
    assert approximate["reviewer_decision"]["allowed_next_step"] == "no_action"
    for packet in (equivalent, derived, approximate):
        assert packet["review_required"] is True
        assert "not_parser_truth" in packet["non_claims"]
        assert packets.validate_recovery_candidate_packet(packet) == []


def test_unavailable_and_blocked_packets_do_not_authorize_recovery() -> None:
    unavailable = packets.build_recovery_candidate_packet(
        comparison.compare_field_evidence(_matrix_row("deck_state.game1_deck_state"))
    )
    private = packets.build_recovery_candidate_packet(
        comparison.compare_field_evidence(_matrix_row("runtime_health.private_log_drift_window"))
    )
    external = packets.build_recovery_candidate_packet(
        comparison.compare_field_evidence(_matrix_row("runtime_health.firewall_network_drop"))
    )

    assert unavailable["candidate_status"] == "not_a_candidate"
    assert unavailable["candidate_category"] == "unavailable_no_candidate"
    assert unavailable["next_role_hint"] == "no_action"
    assert private["candidate_status"] == "blocked_private_evidence"
    assert private["candidate_category"] == "blocked_private_candidate"
    assert private["reviewer_decision"]["requires_private_evidence_approval"] is True
    assert external["candidate_status"] == "blocked_external_boundary"
    assert external["candidate_category"] == "blocked_external_candidate"
    assert external["reviewer_decision"]["allowed_next_step"] == "external_boundary_issue"
    for packet in (unavailable, private, external):
        assert packet["review_required"] is True
        assert packets.validate_recovery_candidate_packet(packet) == []


def test_stale_degraded_and_conflict_packets_route_to_review() -> None:
    stale = packets.build_recovery_candidate_packet(
        comparison.compare_field_evidence(
            _matrix_row("match.match_id"),
            _current(
                "match.match_id",
                ledger_ids=["tier1.match_identity.match_id"],
                signals=["match_state.match_id"],
                source_window_refs=["window_a"],
            ),
            watcher_context=_watcher_report("window_stale"),
        )
    )
    degraded = packets.build_recovery_candidate_packet(
        comparison.compare_field_evidence(
            _matrix_row("match.match_id"),
            _current(
                "match.match_id",
                ledger_ids=["tier1.match_identity.match_id"],
                signals=["match_state.match_id"],
                degradation_flags=["fallback_used"],
            ),
        )
    )
    conflict = packets.build_recovery_candidate_packet(
        comparison.compare_field_evidence(
            _matrix_row("match.match_id"),
            _current(
                "match.match_id",
                ledger_ids=["tier1.match_identity.match_id"],
                signals=["match_state.match_id"],
                invariant_status="failed",
            ),
        )
    )

    assert stale["candidate_status"] == "stale_input"
    assert stale["candidate_category"] == "stale_evidence_review_candidate"
    assert stale["offset_window_refs"] == ["window_a"]
    assert degraded["candidate_status"] == "review_required"
    assert degraded["candidate_category"] == "conflict_review_candidate"
    assert conflict["candidate_status"] == "conflict"
    assert conflict["candidate_category"] == "conflict_review_candidate"
    for packet in (stale, degraded, conflict):
        assert packet["review_required"] is True
        assert packets.validate_recovery_candidate_packet(packet) == []


def test_report_fail_closes_on_private_markers_without_echoing_values() -> None:
    private_path = "/" + "Users" + "/example/private/" + "Player" + ".log"
    current = _current(
        "match.match_id",
        ledger_ids=["tier1.match_identity.match_id"],
        signals=["match_state.match_id"],
        source_window_refs=[private_path],
    )
    current["raw_hash"] = "private-content-hash"

    report = packets.build_recovery_candidate_packet_report(
        reduced_evidence_summaries=[current],
    )
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail_closed"
    assert report["packets"] == []
    assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
    assert private_path not in encoded
    assert "private-content-hash" not in encoded
    assert packets.validate_recovery_candidate_packet_report(report) == []


def test_context_readiness_and_protected_surface_claims_fail_closed() -> None:
    for context in (
        {"parser_behavior_ready": True},
        {"fileWritingAuthorized": True},
        {"protected_surface_assertions": {"parser_behavior_changed": True}},
        {"protectedSurfaceAssertions": {"parserBehaviorChanged": True}},
    ):
        report = packets.build_recovery_candidate_packet_report(context=context)

        assert report["status"] == "fail_closed"
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        for flag in packets.FALSE_READINESS_FLAGS:
            assert report[flag] is False
        assert all(value is False for value in report["protected_surface_assertions"].values())
        assert packets.validate_recovery_candidate_packet_report(report) == []


def test_context_identity_values_fail_closed_without_value_echo() -> None:
    private_path = "/" + "Users" + "/example/private/" + "Player" + ".log"
    for field, expected in (
        ("source_issue", packets.SOURCE_ISSUE),
        ("pipeline_tracker", packets.PIPELINE_TRACKER),
        ("parent_private_evidence_issue", packets.PARENT_PRIVATE_EVIDENCE_ISSUE),
    ):
        report = packets.build_recovery_candidate_packet_report(
            context={field: private_path}
        )
        encoded = json.dumps(report, sort_keys=True)

        assert report["status"] == "fail_closed"
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        assert report[field] == expected
        assert private_path not in encoded
        assert packets.validate_recovery_candidate_packet_report(report) == []


def test_packet_validator_rejects_reviewer_decision_drift_and_summary_readiness() -> None:
    report = packets.build_recovery_candidate_packet_report()
    report["summary"]["summary_is_readiness_metric"] = True
    report["packets"][0]["reviewer_decision"]["decision"] = "auto_promote_fixture"

    errors = packets.validate_recovery_candidate_packet_report(report)

    assert "report:summary:summary_is_readiness_metric_must_be_false" in errors
    assert any(
        "review_decision:decision:unknown:auto_promote_fixture" in error for error in errors
    )


def test_direct_packet_and_report_validation_reject_forbidden_keys() -> None:
    report = packets.build_recovery_candidate_packet_report()
    base_packet = report["packets"][0]

    for key, value in (
        ("raw_payload", {"public": "synthetic"}),
        ("raw_hash", "synthetic_hash"),
        ("exact_offset", 123),
        ("decklist", ["synthetic_card"]),
    ):
        packet = json.loads(json.dumps(base_packet, sort_keys=True))
        packet[key] = value

        errors = packets.validate_recovery_candidate_packet(packet)

        assert f"forbidden_key:packet.{key}" in errors
        assert str(value) not in json.dumps(errors, sort_keys=True)

    report["packets"][0]["raw_payload"] = {"public": "synthetic"}

    report_errors = packets.validate_recovery_candidate_packet_report(report)

    assert "forbidden_key:report.packets[0].raw_payload" in report_errors


def test_inputs_are_copy_safe() -> None:
    matrix = field_recovery_matrix.build_field_recovery_matrix()
    comparison_report = comparison.build_field_evidence_comparison_report()
    matrix_before = json.loads(json.dumps(matrix, sort_keys=True))
    comparison_before = json.loads(json.dumps(comparison_report, sort_keys=True))

    packets.build_recovery_candidate_packet_report(
        field_recovery_matrix_report=matrix,
        field_evidence_comparison_report=comparison_report,
    )

    assert matrix == matrix_before
    assert comparison_report == comparison_before


def test_no_parser_runtime_or_file_writer_imports_are_used() -> None:
    imported = inspect.getsource(packets)

    assert "from mythic_edge_parser import router" not in imported
    assert "from mythic_edge_parser.app import state" not in imported
    assert "from mythic_edge_parser.log.tailer import FileTailer" not in imported
    assert "open(" not in imported
    assert "Path(" not in imported
