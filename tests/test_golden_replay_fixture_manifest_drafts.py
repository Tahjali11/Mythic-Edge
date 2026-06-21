from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from mythic_edge_parser.app.corpus_metadata_diff_generator import build_corpus_metadata_diff
from mythic_edge_parser.app.fixture_promotion_proof import build_fixture_promotion_proof
from mythic_edge_parser.app.golden_replay_fixture_manifest_drafts import (
    GOLDEN_REPLAY_DRAFT_PACKET_OBJECT,
    GOLDEN_REPLAY_DRAFT_PACKET_SCHEMA_VERSION,
    GOLDEN_REPLAY_FIXTURE_DRAFT_OBJECT,
    GOLDEN_REPLAY_MANIFEST_DRAFT_OBJECT,
    build_golden_replay_fixture_manifest_draft_packet,
)
from mythic_edge_parser.app.harvest_review_packets import build_harvest_review_packet
from mythic_edge_parser.app.local_harvest_candidate_reports import build_harvest_candidate_report

MANIFEST_PATH = Path("tests/fixtures/parser_corpus/corpus_manifest.v1.json")
SESSION_LEDGER_PATH = Path("tests/fixtures/parser_corpus/session_ledger.v1.json")
PRIVATE_POSIX_PATH = "/" + "Users/example/private/Player.log"
PRIVATE_REPO_SOURCE_PATH = "pri" + "vate/" + "Player" + ".log"
UNSAFE_DRAFT_PATH = "run" + "time/status.json"
UNSAFE_QUEUE_PATH = "failed_" + "posts/golden-replay-draft.json"
SEMANTIC_PRIVATE_VALUE = "example-user-" + "private-value"
SCENARIO_FAMILY = "core_gameplay.draft_with_games"


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


def _review_packet() -> dict:
    candidate = build_harvest_candidate_report(
        source_label="synthetic.golden.draft.case1",
        source_kind="synthetic_player_log",
        privacy_class="synthetic",
        parser_evidence={
            "event_counts": {"DraftComplete": 1, "GameState": 2, "GameResult": 1},
            "event_kinds": ["DraftComplete", "GameState", "GameResult"],
            "raw_log_lines_included": False,
            "raw_payloads_included": False,
            "private_paths_included": False,
        },
        scenario_family_hints=[SCENARIO_FAMILY],
        related_contracts=["docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md"],
    )
    return build_harvest_review_packet(
        candidate_summary=candidate,
        reviewer_decision={
            "decision_id": "codex-e.golden-draft.decision",
            "reviewer_role": "codex_e",
            "decision_status": "approve_for_followup",
            "rationale": ["synthetic draft can proceed to packet construction"],
            "allowed_next_route": "codex_a_problem_representation",
        },
    )


def _ready_proof() -> dict:
    return build_fixture_promotion_proof(
        review_packet=_review_packet(),
        coverage_before={"family": SCENARIO_FAMILY, "status": "covered_report_only"},
        proposed_coverage_after={"family": SCENARIO_FAMILY, "status": "covered_synthetic"},
        check_refs=_passing_check_refs(),
    )


def _proposed_manifest_entry() -> dict:
    return {
        "entry_id": "draft_with_games_golden_draft_candidate_v1",
        "entry_type": "golden_replay_manifest",
        "source_kind": "synthetic_committed_fixture",
        "commit_status": "committed",
        "privacy_class": "synthetic_committable",
        "sanitization_status": "synthetic",
        "linked_issue": "https://github.com/Tahjali11/Mythic-Edge/issues/385",
        "authorized_by_contract": "docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md",
        "paths": {
            "golden_replay_manifest": "tests/fixtures/golden_replay/draft_candidate.manifest.json",
            "corpus_parity_test": "tests/test_corpus_parity_report.py",
        },
        "scenario_families": [SCENARIO_FAMILY],
        "parser_event_families": ["DraftComplete", "GameState", "GameResult"],
        "parser_claim_families": ["limited_draft_flow"],
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only"],
        "known_gaps": ["draft object only; no corpus status change authorized"],
        "review_notes": ["fixture and manifest draft remain review-only"],
    }


def _proposed_session_entry() -> dict:
    return {
        "session_id": "draft_with_games_golden_draft_candidate_v1",
        "title": "Draft with games golden draft candidate",
        "source_kind": "synthetic_committed_fixture",
        "commit_status": "committed",
        "privacy_class": "synthetic_committable",
        "scenario_families": [SCENARIO_FAMILY],
        "format_family": "limited_draft",
        "match_shape": "draft_with_games",
        "record_summary": "synthetic_golden_replay_draft_candidate",
        "parser_coverage": {
            "coverage_status": "covered_synthetic",
            "event_families": {"DraftComplete": 1, "GameState": 2, "GameResult": 1},
            "unknown_entries": 0,
            "truncation_count": 0,
        },
        "game_rows": {"count": 1, "result_shape": "limited_game_result"},
        "known_gaps": ["draft object only; no fixture writing authorized"],
        "report_only_redactions": {
            "raw_log_lines_included": False,
            "private_paths_included": False,
            "raw_payloads_included": False,
            "local_private_artifacts_included": False,
            "generated_private_artifacts_included": False,
        },
    }


def _metadata_diff() -> dict:
    return build_corpus_metadata_diff(
        promotion_proof=_ready_proof(),
        corpus_manifest=_corpus_manifest(),
        session_ledger=_session_ledger(),
        proposed_manifest_entry=_proposed_manifest_entry(),
        proposed_session_entry=_proposed_session_entry(),
    )


def _parser_preview(**overrides: object) -> dict:
    preview = {
        "source_refs": [
            "synthetic.golden.draft.case1:candidate-summary:review-packet",
            "synthetic.golden.draft.case1:candidate-summary:review-packet:fixture-promotion-proof",
            "synthetic.golden.draft.case1:candidate-summary:review-packet:fixture-promotion-proof:"
            "corpus-metadata-diff",
        ],
        "scenario_families": [SCENARIO_FAMILY],
        "parser_event_families": ["DraftComplete", "GameState", "GameResult"],
        "expected_sections": {
            "event_family_counts": {"DraftComplete": 1, "GameState": 2, "GameResult": 1},
            "event_kind_sequence": ["DraftComplete", "GameState", "GameResult"],
            "diagnostics_summary": {"status": "pass"},
            "truncation_and_data_loss": {"truncation_count": 0},
        },
        "expected_degradation": [],
    }
    preview.update(overrides)
    return preview


def _ready_packet(**overrides: object) -> dict:
    kwargs = {
        "harvest_review_packet": _review_packet(),
        "promotion_proof": _ready_proof(),
        "metadata_diff": _metadata_diff(),
        "corpus_manifest": _corpus_manifest(),
        "session_ledger": _session_ledger(),
        "parser_expected_fact_preview": _parser_preview(),
        "draft_context": {
            "packet_id": "draft-with-games-golden-replay-draft-packet-v1",
            "fixture_draft_id": "draft-with-games-fixture-draft-v1",
            "manifest_draft_id": "draft-with-games-manifest-draft-v1",
            "fixture_window_summary": {
                "line_count": 42,
                "event_count": 4,
                "ordering_required": True,
            },
            "known_gaps": ["draft remains review-only and does not write files"],
        },
    }
    kwargs.update(overrides)
    return build_golden_replay_fixture_manifest_draft_packet(**kwargs)


def test_ready_public_safe_inputs_build_deterministic_review_only_packet() -> None:
    review_packet = _review_packet()
    proof = _ready_proof()
    diff = _metadata_diff()
    manifest = _corpus_manifest()
    ledger = _session_ledger()
    preview = _parser_preview()
    before = deepcopy((review_packet, proof, diff, manifest, ledger, preview))

    packet = build_golden_replay_fixture_manifest_draft_packet(
        harvest_review_packet=review_packet,
        promotion_proof=proof,
        metadata_diff=diff,
        corpus_manifest=manifest,
        session_ledger=ledger,
        parser_expected_fact_preview=preview,
        draft_context={"packet_id": "draft-with-games-golden-replay-draft-packet-v1"},
    )
    repeated = build_golden_replay_fixture_manifest_draft_packet(
        harvest_review_packet=review_packet,
        promotion_proof=proof,
        metadata_diff=diff,
        corpus_manifest=manifest,
        session_ledger=ledger,
        parser_expected_fact_preview=preview,
        draft_context={"packet_id": "draft-with-games-golden-replay-draft-packet-v1"},
    )

    assert packet == repeated
    assert packet["object"] == GOLDEN_REPLAY_DRAFT_PACKET_OBJECT
    assert packet["schema_version"] == GOLDEN_REPLAY_DRAFT_PACKET_SCHEMA_VERSION
    assert packet["draft_status"] == "draft_ready_for_review"
    assert packet["fixture_draft"]["object"] == GOLDEN_REPLAY_FIXTURE_DRAFT_OBJECT
    assert packet["manifest_draft"]["object"] == GOLDEN_REPLAY_MANIFEST_DRAFT_OBJECT
    assert packet["fixture_draft"]["scenario_families"] == [SCENARIO_FAMILY]
    assert packet["manifest_draft"]["parser_owned_expected_sections"] == [
        "diagnostics_summary",
        "event_family_counts",
        "event_kind_sequence",
        "truncation_and_data_loss",
    ]
    assert packet["readiness_flags"] == {
        "parser_behavior_ready": False,
        "pipeline_activation_ready_for_issue_388": False,
    }
    assert all(value is False for value in packet["authorization_flags"].values())
    assert "not_file_writing_authority" in packet["non_claims"]
    assert (review_packet, proof, diff, manifest, ledger, preview) == before


def test_missing_review_packet_fails_closed_to_insufficient_review() -> None:
    packet = _ready_packet(harvest_review_packet=None)

    assert packet["draft_status"] == "insufficient_review"
    assert packet["source_artifacts"]["harvest_review_packet_id"] == "unavailable"
    assert packet["authorization_flags"]["fixture_promotion_authorized"] is False


def test_non_ready_proof_fails_closed_to_insufficient_proof() -> None:
    proof = _ready_proof()
    proof["proof_status"] = "draft"

    packet = _ready_packet(promotion_proof=proof)

    assert packet["draft_status"] == "insufficient_proof"
    assert "proof_status_draft" in packet["validation"]["status_reasons"]


def test_missing_metadata_diff_is_insufficient_metadata_diff() -> None:
    packet = _ready_packet(metadata_diff=None)

    assert packet["draft_status"] == "insufficient_metadata_diff"
    assert packet["source_artifacts"]["metadata_diff_id"] is None


def test_missing_or_unsourced_parser_preview_is_insufficient_preview() -> None:
    missing = _ready_packet(parser_expected_fact_preview=None)
    unsourced = _ready_packet(parser_expected_fact_preview=_parser_preview(source_refs=[]))

    assert missing["draft_status"] == "insufficient_parser_preview"
    assert unsourced["draft_status"] == "insufficient_parser_preview"
    assert "parser_preview_source_refs_missing" in unsourced["validation"]["status_reasons"]


def test_forbidden_private_values_block_without_echoing_value() -> None:
    forbidden_value = "[" + "Client " + "GRE" + "] private payload " + PRIVATE_POSIX_PATH
    preview = _parser_preview(
        expected_sections={
            "diagnostics_summary": {"note": forbidden_value},
        },
    )

    packet = _ready_packet(parser_expected_fact_preview=preview)

    assert packet["draft_status"] == "blocked_privacy"
    assert packet["privacy"]["privacy_finding_count"] > 0
    assert packet["manifest_draft"]["expected_draft"] == {}
    assert forbidden_value not in str(packet)
    assert PRIVATE_POSIX_PATH not in str(packet)


def test_forbidden_reference_paths_block_without_echoing_value() -> None:
    proposed = _ready_packet(
        draft_context={
            "packet_id": "draft-with-games-golden-replay-draft-packet-v1",
            "fixture_draft_id": "draft-with-games-fixture-draft-v1",
            "manifest_draft_id": "draft-with-games-manifest-draft-v1",
            "fixture_window_summary": {"line_count": 42, "event_count": 4},
            "proposed_fixture_path": UNSAFE_DRAFT_PATH,
            "proposed_manifest_path": UNSAFE_QUEUE_PATH,
        },
    )
    referenced = _ready_packet(
        parser_expected_fact_preview=_parser_preview(source_refs=[PRIVATE_REPO_SOURCE_PATH]),
    )

    assert proposed["draft_status"] == "blocked_privacy"
    assert referenced["draft_status"] == "blocked_privacy"
    assert any(
        reason.startswith("privacy:draft_context.proposed_fixture_path:forbidden_path")
        for reason in proposed["validation"]["status_reasons"]
    )
    assert any(
        reason.startswith("privacy:parser_expected_fact_preview.source_refs.0:forbidden_path")
        for reason in referenced["validation"]["status_reasons"]
    )
    assert UNSAFE_DRAFT_PATH not in str(proposed)
    assert UNSAFE_QUEUE_PATH not in str(proposed)
    assert PRIVATE_REPO_SOURCE_PATH not in str(referenced)
    assert referenced["fixture_draft"]["parser_fact_preview_refs"] == []
    assert referenced["manifest_draft"]["expected_draft"] == {}


def test_semantic_private_fields_block_without_echoing_value() -> None:
    preview = _parser_preview(
        expected_sections={
            "diagnostics_summary": {
                "account_id": SEMANTIC_PRIVATE_VALUE,
                "display_name": SEMANTIC_PRIVATE_VALUE,
                "opponent_identifier": SEMANTIC_PRIVATE_VALUE,
                "machine_name": SEMANTIC_PRIVATE_VALUE,
                "local_user_name": SEMANTIC_PRIVATE_VALUE,
                "source_path": "Users/example/" + "pri" + "vate/" + "Player" + ".log",
                "deck_name": SEMANTIC_PRIVATE_VALUE,
                "strategy_note": SEMANTIC_PRIVATE_VALUE,
                "sideboarding_notes": SEMANTIC_PRIVATE_VALUE,
                "card_choices": SEMANTIC_PRIVATE_VALUE,
            },
        },
    )

    packet = _ready_packet(parser_expected_fact_preview=preview)

    assert packet["draft_status"] == "blocked_privacy"
    assert any(
        reason.startswith(
            "privacy:parser_expected_fact_preview.expected_sections."
            "diagnostics_summary.account_id:forbidden_semantic_key",
        )
        for reason in packet["validation"]["status_reasons"]
    )
    assert any(
        reason.startswith(
            "privacy:parser_expected_fact_preview.expected_sections."
            "diagnostics_summary.strategy_note:forbidden_semantic_key",
        )
        for reason in packet["validation"]["status_reasons"]
    )
    assert packet["fixture_draft"]["parser_fact_preview_refs"] == []
    assert packet["manifest_draft"]["expected_draft"] == {}
    assert SEMANTIC_PRIVATE_VALUE not in str(packet)


def test_generic_note_privacy_fields_block_without_echoing_value() -> None:
    generic_note_value = "card choice: preserve synthetic choice summary"
    generic_notes_value = "card choices: preserve synthetic choice summary"
    generic_comment_value = "card-choice: preserve synthetic choice summary"
    generic_annotation_value = "pri" + "vate strategy note: sideboard plan keeps card choices"
    public_note = "fixture and manifest draft remain review-only"
    public_nonclaim_note = (
        "Synthetic metadata does not include deck names, card choices, analytics truth, "
        "AI truth, or coaching truth."
    )
    public_packet = _ready_packet(
        parser_expected_fact_preview=_parser_preview(
            expected_sections={
                "diagnostics_summary": {
                    "note": public_note,
                    "review_notes": [public_note, public_nonclaim_note],
                },
            },
        ),
    )
    blocked_packet = _ready_packet(
        parser_expected_fact_preview=_parser_preview(
            expected_sections={
                "diagnostics_summary": {
                    "note": generic_note_value,
                    "notes": [generic_notes_value],
                    "comment": generic_comment_value,
                    "annotation": generic_annotation_value,
                },
            },
        ),
    )

    assert public_packet["draft_status"] == "draft_ready_for_review"
    assert blocked_packet["draft_status"] == "blocked_privacy"
    assert any(
        reason.startswith(
            "privacy:parser_expected_fact_preview.expected_sections."
            "diagnostics_summary.note:forbidden_semantic_note",
        )
        for reason in blocked_packet["validation"]["status_reasons"]
    )
    assert any(
        reason.startswith(
            "privacy:parser_expected_fact_preview.expected_sections."
            "diagnostics_summary.notes:forbidden_semantic_note",
        )
        for reason in blocked_packet["validation"]["status_reasons"]
    )
    assert any(
        reason.startswith(
            "privacy:parser_expected_fact_preview.expected_sections."
            "diagnostics_summary.comment:forbidden_semantic_note",
        )
        for reason in blocked_packet["validation"]["status_reasons"]
    )
    assert any(
        reason.startswith(
            "privacy:parser_expected_fact_preview.expected_sections."
            "diagnostics_summary.annotation:forbidden_semantic_note",
        )
        for reason in blocked_packet["validation"]["status_reasons"]
    )
    assert blocked_packet["fixture_draft"]["parser_fact_preview_refs"] == []
    assert blocked_packet["manifest_draft"]["expected_draft"] == {}
    assert generic_note_value not in str(blocked_packet)
    assert generic_notes_value not in str(blocked_packet)
    assert generic_comment_value not in str(blocked_packet)
    assert generic_annotation_value not in str(blocked_packet)


def test_blocked_private_source_class_blocks_authorization() -> None:
    packet = _ready_packet(
        draft_context={
            "source_privacy_class": "blocked_private_evidence",
            "fixture_window_summary": {"line_count": 5},
        },
    )

    assert packet["draft_status"] == "blocked_authorization"
    assert packet["fixture_draft"]["source_privacy_class"] == "blocked_private_evidence"
    assert "authorization:source_privacy_class_blocked_private_evidence" in (
        packet["validation"]["status_reasons"]
    )


def test_overclaim_flags_and_forbidden_expected_sections_are_blocked() -> None:
    flagged = _ready_packet(draft_context={"file_writing_authorized": True})
    forbidden_preview = _parser_preview(
        expected_sections={
            "event_family_counts": {"GameState": 1},
            "analytics_aggregates": {"win_rate": 1},
        },
    )
    forbidden = _ready_packet(parser_expected_fact_preview=forbidden_preview)

    assert flagged["draft_status"] == "blocked_overclaim"
    assert "overclaim:input.file_writing_authorized_true" in flagged["validation"]["status_reasons"]
    assert forbidden["draft_status"] == "blocked_overclaim"
    assert "overclaim:forbidden_expected_section_analytics_aggregates" in (
        forbidden["validation"]["status_reasons"]
    )


def test_fixture_window_refusal_statuses_are_preserved() -> None:
    oversized = _ready_packet(
        draft_context={
            "fixture_window_summary": {"line_count": 201},
            "max_fixture_line_count": 200,
        },
    )
    ambiguous = _ready_packet(
        draft_context={
            "fixture_window_summary": {"line_count": 4, "ambiguous_window": True},
        },
    )
    multi_family = _ready_packet(
        parser_expected_fact_preview=_parser_preview(
            scenario_families=[SCENARIO_FAMILY, "drift_debug.missing_message_type"],
        ),
    )

    assert oversized["draft_status"] == "refused_oversized_window"
    assert ambiguous["draft_status"] == "refused_ambiguous_window"
    assert multi_family["draft_status"] == "refused_multi_family_window"
