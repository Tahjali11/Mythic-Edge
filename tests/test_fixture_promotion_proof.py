from __future__ import annotations

from copy import deepcopy

from mythic_edge_parser.app.fixture_promotion_proof import (
    FIXTURE_PROMOTION_PROOF_OBJECT,
    FIXTURE_PROMOTION_PROOF_SCHEMA_VERSION,
    build_fixture_promotion_proof,
)
from mythic_edge_parser.app.harvest_review_packets import build_harvest_review_packet
from mythic_edge_parser.app.local_harvest_candidate_reports import build_harvest_candidate_report

PRIVATE_POSIX_PATH = "/" + "Users/example/private/Player.log"


def _candidate_summary(**overrides: object) -> dict:
    report = build_harvest_candidate_report(
        source_label="synthetic.fixture.case1",
        source_kind="synthetic_player_log",
        privacy_class="synthetic",
        parser_evidence={
            "event_counts": {"GameState": 2, "GameResult": 1},
            "event_kinds": ["GameState", "GameResult"],
            "raw_log_lines_included": False,
            "raw_payloads_included": False,
            "private_paths_included": False,
        },
        scenario_family_hints=["core_gameplay.fixture_candidate"],
        related_contracts=["docs/contracts/parser_evidence_local_harvest_candidate_reports.md"],
    )
    report.update(overrides)
    return report


def _review_packet(**overrides: object) -> dict:
    packet = build_harvest_review_packet(candidate_summary=_candidate_summary(), **overrides)
    return packet


def _passing_check_refs() -> dict:
    return {
        "golden_replay": {
            "status": "pass",
            "refs": ["docs/contract_test_reports/synthetic_golden_replay.md"],
        },
        "corpus_parity": {
            "status": "pass",
            "refs": ["docs/contract_test_reports/synthetic_corpus_parity.md"],
        },
        "feature_equity": {
            "status": "pass",
            "refs": ["docs/contract_test_reports/synthetic_feature_equity.md"],
        },
        "privacy": {
            "status": "pass",
            "refs": ["docs/contract_test_reports/synthetic_privacy.md"],
        },
        "protected_surface": {
            "status": "pass",
            "refs": ["docs/contract_test_reports/synthetic_protected_surface.md"],
        },
    }


def test_builds_deterministic_draft_proof_from_valid_review_packet() -> None:
    packet = _review_packet()
    coverage_before = {
        "family": "core_gameplay.fixture_candidate",
        "status": "covered_report_only",
    }

    proof = build_fixture_promotion_proof(
        review_packet=packet,
        coverage_before=coverage_before,
    )
    repeated = build_fixture_promotion_proof(
        review_packet=packet,
        coverage_before=coverage_before,
    )

    assert proof == repeated
    assert proof["object"] == FIXTURE_PROMOTION_PROOF_OBJECT
    assert proof["schema_version"] == FIXTURE_PROMOTION_PROOF_SCHEMA_VERSION
    assert proof["proof_status"] == "draft"
    assert proof["source"] == {
        "review_packet_schema_version": "parser_evidence_harvest_review_packet.v1",
        "review_packet_id": "synthetic.fixture.case1:candidate-summary:review-packet",
        "candidate_report_id": "synthetic.fixture.case1:candidate-summary",
        "reviewer_decision_id": None,
    }
    assert proof["authorization"] == {
        "parser_behavior_ready": False,
        "pipeline_activation_ready_for_issue_388": False,
        "private_harvest_authorized": False,
        "fixture_promotion_authorized": False,
        "file_writing_authorized": False,
        "corpus_status_change_authorized": False,
    }
    assert proof["coverage_comparison"] == {
        "family": "core_gameplay.fixture_candidate",
        "before_status": "covered_report_only",
        "proposed_after_status": None,
        "status_change_kind": "no_change",
        "metadata_mutation_authorized": False,
    }
    assert proof["parser_fact_scope"]["parser_behavior_verified"] is False
    assert proof["parser_fact_scope"]["facts_proposed"] == []
    assert proof["evidence_checks"]["golden_replay"] == {"status": "not_run", "refs": []}
    assert "not_fixture_promotion_authority" in proof["non_claims"]


def test_approved_review_packet_with_public_safe_checks_is_ready_for_review_only() -> None:
    packet = _review_packet(
        reviewer_decision={
            "decision_id": "codex-e.fixture-proof.decision",
            "reviewer_role": "codex_e",
            "decision_status": "approve_for_followup",
            "rationale": ["candidate merits proof review"],
            "allowed_next_route": "codex_a_problem_representation",
        },
    )

    proof = build_fixture_promotion_proof(
        review_packet=packet,
        coverage_before={
            "family": "core_gameplay.fixture_candidate",
            "status": "covered_report_only",
        },
        proposed_coverage_after={
            "family": "core_gameplay.fixture_candidate",
            "status": "covered_synthetic",
        },
        check_refs=_passing_check_refs(),
    )

    assert proof["proof_status"] == "proof_ready_for_review"
    assert proof["source"]["reviewer_decision_id"] == "codex-e.fixture-proof.decision"
    assert proof["coverage_comparison"]["status_change_kind"] == "status_promotion_candidate"
    assert proof["coverage_comparison"]["metadata_mutation_authorized"] is False
    assert proof["authorization"]["fixture_promotion_authorized"] is False
    assert proof["authorization"]["corpus_status_change_authorized"] is False
    assert proof["authorization"]["pipeline_activation_ready_for_issue_388"] is False
    assert "not_readiness" in proof["non_claims"]


def test_missing_review_packet_fails_closed_to_insufficient_review() -> None:
    proof = build_fixture_promotion_proof(
        review_packet=None,
        coverage_before={"family": "core_gameplay.fixture_candidate", "status": "covered_report_only"},
    )

    assert proof["proof_status"] == "insufficient_review"
    assert proof["source"]["review_packet_id"] == "unavailable"
    assert proof["validation"]["schema_issue"] == "review_packet_missing"
    assert proof["authorization"]["fixture_promotion_authorized"] is False


def test_privacy_blocked_packet_blocks_proof_without_echoing_values() -> None:
    forbidden_value = "[" + "Client " + "GRE" + "] private-ish payload"
    candidate = _candidate_summary()
    candidate["unsafe"] = {"raw_text": forbidden_value}
    packet = build_harvest_review_packet(candidate_summary=candidate)

    proof = build_fixture_promotion_proof(
        review_packet=packet,
        coverage_before={"family": "drift_debug.raw_payload_boundary", "status": "covered_report_only"},
    )

    assert proof["proof_status"] == "blocked_privacy"
    assert proof["validation"]["privacy_finding_count"] > 0
    assert forbidden_value not in str(proof)
    assert proof["authorization"]["private_harvest_authorized"] is False


def test_private_source_packet_blocks_authorization_and_keeps_flags_false() -> None:
    private_candidate = build_harvest_candidate_report(
        source_label="operator.selected.source",
        source_kind="user_selected_player_log",
        privacy_class="private_local",
        parser_evidence={"event_counts": {"UnknownEntry": 1}},
        scenario_family_hints=["private_evidence.local_review"],
    )
    packet = build_harvest_review_packet(candidate_summary=private_candidate)

    proof = build_fixture_promotion_proof(
        review_packet=packet,
        coverage_before={
            "family": "private_evidence.local_review",
            "status": "blocked_private_evidence",
        },
    )

    assert proof["proof_status"] == "blocked_authorization"
    assert proof["coverage_comparison"]["status_change_kind"] == "blocked_private_evidence"
    assert all(value is False for value in proof["authorization"].values())


def test_review_packet_schema_mismatch_routes_to_contract_update_without_echo() -> None:
    packet = _review_packet()
    packet["schema_version"] = "future.private.schema"

    proof = build_fixture_promotion_proof(
        review_packet=packet,
        coverage_before={"family": "core_gameplay.fixture_candidate", "status": "covered_report_only"},
    )

    assert proof["proof_status"] == "needs_contract_update"
    assert proof["source"]["review_packet_schema_version"] == "unsupported"
    assert proof["validation"]["schema_issue"] == "unsupported_review_packet_schema"
    assert "future.private.schema" not in str(proof)


def test_rejected_reviewer_decision_rejects_proof() -> None:
    packet = _review_packet(
        reviewer_decision={
            "decision_id": "codex-e.fixture-proof.reject",
            "reviewer_role": "codex_e",
            "decision_status": "reject",
            "rationale": ["not enough evidence for followup"],
            "allowed_next_route": "none",
        },
    )

    proof = build_fixture_promotion_proof(
        review_packet=packet,
        coverage_before={"family": "core_gameplay.fixture_candidate", "status": "covered_report_only"},
        check_refs=_passing_check_refs(),
    )

    assert proof["proof_status"] == "proof_rejected"
    assert "reviewer_decision_reject" in proof["validation"]["status_reasons"]
    assert proof["authorization"]["fixture_promotion_authorized"] is False


def test_evidence_check_failure_prevents_ready_state() -> None:
    packet = _review_packet(
        reviewer_decision={
            "decision_id": "codex-e.fixture-proof.decision",
            "reviewer_role": "codex_e",
            "decision_status": "approve_for_followup",
            "rationale": ["candidate merits proof review"],
            "allowed_next_route": "codex_a_problem_representation",
        },
    )
    checks = _passing_check_refs()
    checks["protected_surface"] = {
        "status": "diff",
        "refs": ["docs/contract_test_reports/synthetic_protected_surface.md"],
    }

    proof = build_fixture_promotion_proof(
        review_packet=packet,
        coverage_before={"family": "core_gameplay.fixture_candidate", "status": "covered_report_only"},
        proposed_coverage_after={"family": "core_gameplay.fixture_candidate", "status": "covered_synthetic"},
        check_refs=checks,
    )

    assert proof["proof_status"] == "proof_rejected"
    assert "protected_surface_diff" in proof["validation"]["status_reasons"]
    assert proof["authorization"]["corpus_status_change_authorized"] is False


def test_proof_context_forbidden_content_blocks_without_echoing_value() -> None:
    proof = build_fixture_promotion_proof(
        review_packet=_review_packet(),
        coverage_before={"family": "core_gameplay.fixture_candidate", "status": "covered_report_only"},
        proof_context={"note": f"looked at {PRIVATE_POSIX_PATH}"},
    )

    assert proof["proof_status"] == "blocked_privacy"
    assert proof["proof_context"] == {"status": "blocked", "finding_count": 1}
    assert PRIVATE_POSIX_PATH not in str(proof)


def test_coverage_inputs_are_not_mutated_and_do_not_authorize_metadata_change() -> None:
    packet = _review_packet()
    coverage_before = {
        "family": "core_gameplay.fixture_candidate",
        "status": "covered_report_only",
        "evidence_strength": "review",
    }
    proposed_after = {
        "family": "core_gameplay.fixture_candidate",
        "status": "covered_report_only",
        "evidence_strength": "stronger",
    }
    before_copy = deepcopy(coverage_before)
    after_copy = deepcopy(proposed_after)

    proof = build_fixture_promotion_proof(
        review_packet=packet,
        coverage_before=coverage_before,
        proposed_coverage_after=proposed_after,
    )

    assert coverage_before == before_copy
    assert proposed_after == after_copy
    assert proof["coverage_comparison"]["status_change_kind"] == "stronger_evidence_candidate"
    assert proof["coverage_comparison"]["metadata_mutation_authorized"] is False
    assert proof["authorization"]["corpus_status_change_authorized"] is False
