from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from mythic_edge_parser.app.corpus_metadata_diff_generator import (
    CORPUS_METADATA_DIFF_OBJECT,
    CORPUS_METADATA_DIFF_SCHEMA_VERSION,
    build_corpus_metadata_diff,
)
from mythic_edge_parser.app.fixture_promotion_proof import build_fixture_promotion_proof
from mythic_edge_parser.app.harvest_review_packets import build_harvest_review_packet
from mythic_edge_parser.app.local_harvest_candidate_reports import build_harvest_candidate_report

MANIFEST_PATH = Path("tests/fixtures/parser_corpus/corpus_manifest.v1.json")
SESSION_LEDGER_PATH = Path("tests/fixtures/parser_corpus/session_ledger.v1.json")
PRIVATE_POSIX_PATH = "/" + "Users/example/private/Player.log"


def _corpus_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text())


def _session_ledger() -> dict:
    return json.loads(SESSION_LEDGER_PATH.read_text())


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


def _ready_proof(family: str = "core_gameplay.draft_with_games") -> dict:
    candidate = build_harvest_candidate_report(
        source_label="synthetic.diff.case1",
        source_kind="synthetic_player_log",
        privacy_class="synthetic",
        parser_evidence={
            "event_counts": {"DraftComplete": 1, "GameState": 2, "GameResult": 1},
            "event_kinds": ["DraftComplete", "GameState", "GameResult"],
            "raw_log_lines_included": False,
            "raw_payloads_included": False,
            "private_paths_included": False,
        },
        scenario_family_hints=[family],
        related_contracts=["docs/contracts/parser_evidence_corpus_metadata_diff_generator.md"],
    )
    packet = build_harvest_review_packet(
        candidate_summary=candidate,
        reviewer_decision={
            "decision_id": "codex-e.corpus-metadata-diff.decision",
            "reviewer_role": "codex_e",
            "decision_status": "approve_for_followup",
            "rationale": ["synthetic metadata diff candidate may be reviewed"],
            "allowed_next_route": "codex_a_problem_representation",
        },
    )
    return build_fixture_promotion_proof(
        review_packet=packet,
        coverage_before={"family": family, "status": "covered_report_only"},
        proposed_coverage_after={"family": family, "status": "covered_synthetic"},
        check_refs=_passing_check_refs(),
    )


def _proposed_manifest_entry(**overrides: object) -> dict:
    entry = {
        "entry_id": "draft_with_games_metadata_diff_candidate_v1",
        "entry_type": "golden_replay_manifest",
        "source_kind": "synthetic_committed_fixture",
        "commit_status": "committed",
        "privacy_class": "synthetic_committable",
        "sanitization_status": "synthetic",
        "linked_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/386",
        "authorized_by_contract": "docs/contracts/parser_evidence_corpus_metadata_diff_generator.md",
        "paths": {
            "golden_replay_manifest": "tests/fixtures/golden_replay/draft_with_games_synthetic.manifest.json",
            "corpus_parity_test": "tests/test_corpus_parity_report.py",
        },
        "scenario_families": ["core_gameplay.draft_with_games"],
        "parser_event_families": ["DraftComplete", "GameState", "GameResult"],
        "parser_claim_families": ["limited_draft_flow"],
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only"],
        "known_gaps": [
            "synthetic metadata diff only; no corpus status change is authorized",
            "does not prove private smoke success or release readiness",
        ],
        "review_notes": [
            "review-only diff candidate; fixture promotion remains unauthorized",
        ],
    }
    entry.update(overrides)
    return entry


def _proposed_session_entry(**overrides: object) -> dict:
    entry = {
        "session_id": "draft_with_games_metadata_diff_candidate_v1",
        "title": "Draft with games metadata diff candidate",
        "source_kind": "synthetic_committed_fixture",
        "commit_status": "committed",
        "privacy_class": "synthetic_committable",
        "scenario_families": ["core_gameplay.draft_with_games"],
        "format_family": "limited_draft",
        "match_shape": "draft_with_games",
        "record_summary": "synthetic_metadata_diff_candidate",
        "parser_coverage": {
            "coverage_status": "covered_synthetic",
            "event_families": {"DraftComplete": 1, "GameState": 2, "GameResult": 1},
            "unknown_entries": 0,
            "truncation_count": 0,
        },
        "game_rows": {"count": 1, "result_shape": "limited_game_result"},
        "known_gaps": [
            "synthetic metadata diff only; no fixture writing is authorized",
        ],
        "report_only_redactions": {
            "raw_log_lines_included": False,
            "private_paths_included": False,
            "raw_payloads_included": False,
            "local_private_artifacts_included": False,
            "generated_private_artifacts_included": False,
        },
    }
    entry.update(overrides)
    return entry


def test_ready_proof_with_no_proposed_entries_returns_no_metadata_change() -> None:
    diff = build_corpus_metadata_diff(
        promotion_proof=_ready_proof(),
        corpus_manifest=_corpus_manifest(),
        session_ledger=_session_ledger(),
    )

    assert diff["object"] == CORPUS_METADATA_DIFF_OBJECT
    assert diff["schema_version"] == CORPUS_METADATA_DIFF_SCHEMA_VERSION
    assert diff["diff_status"] == "no_metadata_change"
    assert diff["proposed_changes"] == {
        "change_types": ["no_change"],
        "manifest_entries": [],
        "session_entries": [],
    }
    assert diff["coverage_transition"] == {"families": [], "transition_kind": "no_change"}
    assert diff["consistency_checks"]["no_metadata_mutation_performed"] is True
    assert all(value is False for value in diff["authorization"].values())
    assert "not_readiness" in diff["non_claims"]


def test_ready_proof_with_public_safe_entries_is_review_only_diff_ready() -> None:
    manifest = _corpus_manifest()
    ledger = _session_ledger()
    manifest_before = deepcopy(manifest)
    ledger_before = deepcopy(ledger)

    diff = build_corpus_metadata_diff(
        promotion_proof=_ready_proof(),
        corpus_manifest=manifest,
        session_ledger=ledger,
        proposed_manifest_entry=_proposed_manifest_entry(),
        proposed_session_entry=_proposed_session_entry(),
    )

    assert diff["diff_status"] == "diff_ready_for_review"
    assert diff["coverage_transition"] == {
        "families": ["core_gameplay.draft_with_games"],
        "transition_kind": "report_only_to_synthetic_candidate",
    }
    assert set(diff["proposed_changes"]["change_types"]) == {
        "add_manifest_entry",
        "add_session_entry",
        "status_promotion_candidate",
    }
    assert diff["proposed_changes"]["manifest_entries"][0]["entry_id"] == (
        "draft_with_games_metadata_diff_candidate_v1"
    )
    assert diff["proposed_changes"]["session_entries"][0]["session_id"] == (
        "draft_with_games_metadata_diff_candidate_v1"
    )
    assert diff["consistency_checks"] == {
        "manifest_schema_valid": True,
        "session_ledger_schema_valid": True,
        "family_scope_limited": True,
        "known_gaps_preserved": True,
        "privacy_flags_preserved": True,
        "no_metadata_mutation_performed": True,
    }
    assert all(value is False for value in diff["authorization"].values())
    assert manifest == manifest_before
    assert ledger == ledger_before


def test_missing_proof_fails_closed_to_insufficient_proof() -> None:
    diff = build_corpus_metadata_diff(
        promotion_proof=None,  # type: ignore[arg-type]
        corpus_manifest=_corpus_manifest(),
        session_ledger=_session_ledger(),
    )

    assert diff["diff_status"] == "insufficient_proof"
    assert diff["source"]["proof_id"] == "unavailable"
    assert diff["authorization"]["fixture_promotion_authorized"] is False


def test_malformed_proof_routes_to_contract_update() -> None:
    proof = _ready_proof()
    proof["schema_version"] = "future.schema"

    diff = build_corpus_metadata_diff(
        promotion_proof=proof,
        corpus_manifest=_corpus_manifest(),
        session_ledger=_session_ledger(),
    )

    assert diff["diff_status"] == "needs_contract_update"
    assert diff["validation"]["proof_issue"] == "unsupported_proof_schema"
    assert "future.schema" not in str(diff)


def test_non_ready_proof_is_insufficient() -> None:
    proof = _ready_proof()
    proof["proof_status"] = "draft"

    diff = build_corpus_metadata_diff(
        promotion_proof=proof,
        corpus_manifest=_corpus_manifest(),
        session_ledger=_session_ledger(),
        proposed_manifest_entry=_proposed_manifest_entry(),
    )

    assert diff["diff_status"] == "insufficient_proof"
    assert "proof_status_draft" in diff["validation"]["status_reasons"]


def test_forbidden_private_values_block_without_echoing_value() -> None:
    forbidden_value = "[" + "Client " + "GRE" + "] private payload " + PRIVATE_POSIX_PATH
    entry = _proposed_manifest_entry(raw_payload=forbidden_value)

    diff = build_corpus_metadata_diff(
        promotion_proof=_ready_proof(),
        corpus_manifest=_corpus_manifest(),
        session_ledger=_session_ledger(),
        proposed_manifest_entry=entry,
    )

    assert diff["diff_status"] == "blocked_privacy"
    assert diff["proposed_changes"]["manifest_entries"] == []
    assert diff["validation"]["privacy_finding_count"] > 0
    assert forbidden_value not in str(diff)
    assert PRIVATE_POSIX_PATH not in str(diff)


def test_forbidden_private_values_inside_promotion_proof_block_without_echoing_value() -> None:
    forbidden_value = "[" + "Client " + "GRE" + "] proof raw payload " + PRIVATE_POSIX_PATH
    proof = _ready_proof()
    proof["promotion_proof_raw_payload"] = forbidden_value

    diff = build_corpus_metadata_diff(
        promotion_proof=proof,
        corpus_manifest=_corpus_manifest(),
        session_ledger=_session_ledger(),
        proposed_manifest_entry=_proposed_manifest_entry(),
    )

    assert diff["diff_status"] == "blocked_privacy"
    assert diff["proposed_changes"]["manifest_entries"] == []
    assert diff["validation"]["privacy_finding_count"] > 0
    assert {
        "finding_id": "corpus-metadata-diff-privacy-finding-1",
        "field": "promotion_proof.promotion_proof_raw_payload",
        "reason": "forbidden_key",
    } in diff["validation"]["privacy_findings"]
    assert forbidden_value not in str(diff)
    assert PRIVATE_POSIX_PATH not in str(diff)


def test_non_repo_relative_proposed_paths_block_privacy_without_echo() -> None:
    private_path = "/" + "Users/example/private/corpus_metadata_diff.json"
    entry = _proposed_manifest_entry(paths={"local_artifact": private_path})

    diff = build_corpus_metadata_diff(
        promotion_proof=_ready_proof(),
        corpus_manifest=_corpus_manifest(),
        session_ledger=_session_ledger(),
        proposed_manifest_entry=entry,
    )

    assert diff["diff_status"] == "blocked_privacy"
    assert private_path not in str(diff)


@pytest.mark.parametrize(
    ("before_status", "reason"),
    (
        (
            "blocked_private_evidence",
            "blocked_private_evidence:promotion_requires_separate_authority",
        ),
        (
            "blocked_external_boundary",
            "blocked_external_boundary:promotion_requires_separate_authority",
        ),
    ),
)
def test_blocked_private_or_external_promotion_requires_authorization(
    before_status: str,
    reason: str,
) -> None:
    proof = _ready_proof()
    proof["coverage_comparison"]["before_status"] = before_status

    diff = build_corpus_metadata_diff(
        promotion_proof=proof,
        corpus_manifest=_corpus_manifest(),
        session_ledger=_session_ledger(),
        proposed_manifest_entry=_proposed_manifest_entry(),
    )

    assert diff["diff_status"] == "blocked_authorization"
    assert reason in diff["anti_overclaim"]["reasons"]
    assert reason in diff["validation"]["authorization_reasons"]
    assert "authorization_boundary_blocked" in diff["validation"]["status_reasons"]


def test_premature_parser_behavior_verified_blocks_as_overclaim() -> None:
    entry = _proposed_manifest_entry(coverage_basis=["fixture_metadata_only", "parser_behavior_verified"])

    diff = build_corpus_metadata_diff(
        promotion_proof=_ready_proof(),
        corpus_manifest=_corpus_manifest(),
        session_ledger=_session_ledger(),
        proposed_manifest_entry=entry,
    )

    assert diff["diff_status"] == "blocked_overclaim"
    assert "parser_behavior_verified:premature_claim" in diff["anti_overclaim"]["reasons"]
    assert diff["authorization"]["pipeline_activation_ready_for_issue_388"] is False


def test_unrelated_family_promotion_blocks_as_overclaim() -> None:
    entry = _proposed_manifest_entry(scenario_families=["core_gameplay.standard_bo1"])

    diff = build_corpus_metadata_diff(
        promotion_proof=_ready_proof("core_gameplay.draft_with_games"),
        corpus_manifest=_corpus_manifest(),
        session_ledger=_session_ledger(),
        proposed_manifest_entry=entry,
    )

    assert diff["diff_status"] == "blocked_overclaim"
    assert "proposed_families:outside_proof_scope" in diff["anti_overclaim"]["reasons"]
    assert diff["consistency_checks"]["family_scope_limited"] is False


def test_invalid_manifest_or_session_schema_routes_to_contract_update() -> None:
    manifest = _corpus_manifest()
    ledger = _session_ledger()
    manifest["schema_version"] = "future.schema"
    ledger["object"] = "future_ledger"

    diff = build_corpus_metadata_diff(
        promotion_proof=_ready_proof(),
        corpus_manifest=manifest,
        session_ledger=ledger,
        proposed_manifest_entry=_proposed_manifest_entry(),
    )

    assert diff["diff_status"] == "needs_contract_update"
    assert diff["validation"]["manifest_schema_issue"] == "manifest:unsupported_schema"
    assert diff["validation"]["session_ledger_schema_issue"] == "session_ledger:unsupported_object"


def test_existing_entry_known_gap_deletion_blocks_as_overclaim() -> None:
    manifest = _corpus_manifest()
    existing_entry = next(
        entry for entry in manifest["entries"] if entry["entry_id"] == "draft_with_games_boundary_report_v1"
    )
    proposed = deepcopy(existing_entry)
    proposed["coverage_status"] = "covered_synthetic"
    proposed["known_gaps"] = []

    diff = build_corpus_metadata_diff(
        promotion_proof=_ready_proof("core_gameplay.draft_with_games"),
        corpus_manifest=manifest,
        session_ledger=_session_ledger(),
        proposed_manifest_entry=proposed,
    )

    assert diff["diff_status"] == "blocked_overclaim"
    assert "known_gaps:removed_without_replacement" in diff["anti_overclaim"]["reasons"]
