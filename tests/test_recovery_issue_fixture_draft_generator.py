from __future__ import annotations

import inspect
import json

from mythic_edge_parser.app import field_evidence_comparison_report as comparison
from mythic_edge_parser.app import field_recovery_matrix
from mythic_edge_parser.app import recovery_candidate_packet_generator as candidates
from mythic_edge_parser.app import recovery_issue_fixture_draft_generator as drafts


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


def _direct_candidate_packet_report() -> dict:
    return candidates.build_recovery_candidate_packet_report(
        reduced_evidence_summaries=[
            _current(
                "match.match_id",
                ledger_ids=["tier1.match_identity.match_id"],
                signals=["match_state.match_id"],
            )
        ]
    )


def _direct_candidate_packet() -> dict:
    return candidates.build_recovery_candidate_packet(
        comparison.compare_field_evidence(
            _matrix_row("match.match_id"),
            _current(
                "match.match_id",
                ledger_ids=["tier1.match_identity.match_id"],
                signals=["match_state.match_id"],
            ),
        )
    )


def _packet_for(field_id: str) -> dict:
    return candidates.build_recovery_candidate_packet(
        comparison.compare_field_evidence(_matrix_row(field_id))
    )


def test_draft_report_shape_false_flags_and_deterministic_serialization() -> None:
    report = drafts.build_recovery_issue_fixture_draft_report(
        recovery_candidate_packets=[_direct_candidate_packet()],
    )

    assert report["object"] == drafts.RECOVERY_ISSUE_FIXTURE_DRAFT_REPORT_OBJECT
    assert report["schema_version"] == drafts.RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION
    assert report["source_issue"] == drafts.SOURCE_ISSUE
    assert report["status"] == "drafts_ready_for_review"
    assert report["drafts"][0]["draft_status"] == "draft_ready_for_review"
    assert report["drafts"][0]["draft_type"] == "issue_fixture_manifest_review_draft"
    for flag in drafts.READINESS_FLAGS:
        assert report["readiness_flags"][flag] is False
    for flag in drafts.AUTHORIZATION_FLAGS:
        assert report["authorization_flags"][flag] is False
    assert report["summary"]["summary_is_readiness_metric"] is False
    assert report["non_claims"] == list(drafts.REQUIRED_NON_CLAIMS)
    assert drafts.validate_recovery_issue_fixture_draft_report(report) == []
    encoded = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False)
    assert json.loads(encoded) == report


def test_issue_draft_uses_refs_only_lifecycle_wording() -> None:
    report = drafts.build_recovery_issue_fixture_draft_report(
        recovery_candidate_packets=[_direct_candidate_packet()],
    )
    issue_draft = report["drafts"][0]["issue_draft"]
    encoded = json.dumps(issue_draft, sort_keys=True)

    assert issue_draft["lifecycle_wording_status"] == "refs_only"
    assert issue_draft["forbidden_lifecycle_terms_found"] is False
    assert "Refs #455" in encoded
    assert "Closes #" not in encoded
    assert "Fixes #" not in encoded
    assert "Resolves #" not in encoded
    assert issue_draft["authorization_flags"]["issue_creation_authorized"] is False
    assert issue_draft["authorization_flags"]["pr_creation_authorized"] is False
    assert drafts.validate_recovery_issue_draft(issue_draft) == []


def test_fixture_and_manifest_summaries_remain_review_only() -> None:
    report = drafts.build_recovery_issue_fixture_draft_report(
        recovery_candidate_packets=[_direct_candidate_packet()],
    )
    group = report["drafts"][0]
    fixture_summary = group["fixture_draft_summary"]
    manifest_summary = group["manifest_draft_summary"]

    assert fixture_summary["object"] == drafts.RECOVERY_FIXTURE_DRAFT_SUMMARY_OBJECT
    assert fixture_summary["file_writing_authorized"] is False
    assert fixture_summary["fixture_promotion_authorized"] is False
    assert fixture_summary["proposed_fixture_path"] == "not_applicable"
    assert fixture_summary["minimal_window_summary"]["raw_lines_included"] is False
    assert manifest_summary["object"] == drafts.RECOVERY_MANIFEST_DRAFT_SUMMARY_OBJECT
    assert manifest_summary["file_writing_authorized"] is False
    assert manifest_summary["corpus_status_change_authorized"] is False
    assert manifest_summary["corpus_manifest_change"] == "not_authorized"
    assert manifest_summary["session_ledger_change"] == "not_authorized"
    assert manifest_summary["expected_sections"] == [
        "parser_state",
        "final_reconciliation",
        "parser_owned_rows",
    ]
    assert drafts.validate_recovery_fixture_draft_summary(fixture_summary) == []
    assert drafts.validate_recovery_manifest_draft_summary(manifest_summary) == []


def test_fixture_and_manifest_summaries_preserve_source_packet_review_metadata() -> None:
    packet = candidates.build_recovery_candidate_packet(
        comparison.compare_field_evidence(
            _matrix_row("match.match_id"),
            _current(
                "match.match_id",
                ledger_ids=["tier1.match_identity.match_id"],
                signals=["match_state.match_id"],
                confidence="medium",
                finality="provisional",
                degradation_flags=["fallback_used"],
            ),
        )
    )

    group = drafts.build_recovery_issue_fixture_draft_group(packet)

    assert packet["candidate_status"] == "review_required"
    assert group["draft_status"] == "review_required"
    for summary in (group["fixture_draft_summary"], group["manifest_draft_summary"]):
        assert summary["confidence"] == packet["confidence"]
        assert summary["finality"] == packet["finality"]
        assert summary["degradation_flags"] == packet["degradation_flags"]
        assert summary["candidate_status"] == packet["candidate_status"]
    assert drafts.validate_recovery_issue_fixture_draft_group(group) == []


def test_direct_group_invalid_or_unknown_field_id_routes_review_required() -> None:
    cases = (
        ("not_a_field", "unknown.field"),
        ("unknown.field", "unknown.field"),
    )
    for supplied_field_id, expected_field_id in cases:
        packet = _direct_candidate_packet()
        packet["field_id"] = supplied_field_id

        group = drafts.build_recovery_issue_fixture_draft_group(packet)

        assert packet["candidate_status"] == "candidate_ready_for_review"
        assert group["field_id"] == expected_field_id
        assert group["draft_status"] == "review_required"
        assert group["draft_type"] == "review_required_summary"
        assert group["next_role_hint"] == "codex_a_problem_representation"
        assert group["fixture_draft_summary"]["draft_status"] == "review_required"
        assert group["manifest_draft_summary"]["draft_status"] == "review_required"
        assert drafts.validate_recovery_issue_fixture_draft_group(group) == []


def test_review_required_and_blocked_packets_do_not_become_action_ready() -> None:
    review_packet = candidates.build_recovery_candidate_packet(
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
    private_packet = _packet_for("runtime_health.private_log_drift_window")
    external_packet = _packet_for("runtime_health.firewall_network_drop")

    review_group = drafts.build_recovery_issue_fixture_draft_group(review_packet)
    private_group = drafts.build_recovery_issue_fixture_draft_group(private_packet)
    external_group = drafts.build_recovery_issue_fixture_draft_group(external_packet)

    assert review_group["draft_status"] == "review_required"
    assert review_group["next_role_hint"] == "codex_a_problem_representation"
    assert private_group["draft_status"] == "blocked_private_evidence"
    assert private_group["fixture_draft_summary"]["fixture_evidence_class"] == "private_gated_candidate"
    assert private_group["next_role_hint"] == "codex_a_problem_representation"
    assert external_group["draft_status"] == "blocked_external_boundary"
    assert external_group["fixture_draft_summary"]["fixture_evidence_class"] == "external_gated_candidate"
    for group in (review_group, private_group, external_group):
        assert drafts.validate_recovery_issue_fixture_draft_group(group) == []


def test_context_readiness_claims_fail_closed_without_value_echo() -> None:
    for context in (
        {"parser_behavior_ready": True},
        {"fileWritingAuthorized": True},
        {"issue_creation_authorized": True},
        {"prCreationAuthorized": True},
        {"protected_surface_assertions": {"parser_behavior_changed": True}},
    ):
        report = drafts.build_recovery_issue_fixture_draft_report(
            recovery_candidate_packets=[_direct_candidate_packet()],
            context=context,
        )

        assert report["status"] == "fail_closed"
        assert report["drafts"] == []
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        for flag in drafts.READINESS_FLAGS:
            assert report["readiness_flags"][flag] is False
        for flag in drafts.AUTHORIZATION_FLAGS:
            assert report["authorization_flags"][flag] is False
        assert drafts.validate_recovery_issue_fixture_draft_report(report) == []


def test_context_forbidden_keys_fail_closed_without_key_echo() -> None:
    private_key = "/" + "Users" + "/example/private/" + "Player" + ".log"
    closing_key = "Closes #455"

    for context, forbidden_text in (
        ({private_key: "symbolic"}, private_key),
        ({closing_key: "symbolic"}, closing_key),
    ):
        report = drafts.build_recovery_issue_fixture_draft_report(
            recovery_candidate_packets=[_direct_candidate_packet()],
            context=context,
        )
        encoded = json.dumps(report, sort_keys=True)

        assert report["status"] == "fail_closed"
        assert report["drafts"] == []
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        assert forbidden_text not in encoded
        assert drafts.validate_recovery_issue_fixture_draft_report(report) == []


def test_lifecycle_action_keys_fail_closed_without_value_echo() -> None:
    for context in (
        {"closes": "#455"},
        {"fixes": "#388"},
        {"closedBy": "#434"},
    ):
        report = drafts.build_recovery_issue_fixture_draft_report(
            recovery_candidate_packets=[_direct_candidate_packet()],
            context=context,
        )
        encoded = json.dumps(report, sort_keys=True)

        assert report["status"] == "fail_closed"
        assert report["drafts"] == []
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        assert "#455" not in encoded
        assert "#388" not in encoded
        assert "#434" not in encoded
        assert drafts.validate_recovery_issue_fixture_draft_report(report) == []


def test_direct_protected_surface_claim_keys_fail_closed() -> None:
    for context in (
        {"parser_behavior_changed": True},
        {"parserBehaviorChanged": True},
        {"github_issue_or_pr_lifecycle_changed": True},
    ):
        report = drafts.build_recovery_issue_fixture_draft_report(
            recovery_candidate_packets=[_direct_candidate_packet()],
            context=context,
        )

        assert report["status"] == "fail_closed"
        assert report["drafts"] == []
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        assert drafts.validate_recovery_issue_fixture_draft_report(report) == []


def test_private_markers_fail_closed_without_echoing_values() -> None:
    private_path = "/" + "Users" + "/example/private/" + "Player" + ".log"
    packet = _direct_candidate_packet()
    packet["offset_window_refs"] = [private_path]
    packet["raw_hash"] = "private-content-hash"

    report = drafts.build_recovery_issue_fixture_draft_report(
        recovery_candidate_packets=[packet],
    )
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail_closed"
    assert report["drafts"] == []
    assert private_path not in encoded
    assert "private-content-hash" not in encoded
    assert drafts.validate_recovery_issue_fixture_draft_report(report) == []


def test_exact_private_metadata_values_fail_closed_without_echo() -> None:
    cases = (
        ("offset_window_refs", "offset:123456"),
        ("source_evidence_refs", "exact_file_size_bytes:123456"),
        ("source_evidence_refs", "2026-06-22t00:00:00z"),
        ("source_evidence_refs", "sha256:abcdef1234567890abcdef1234567890"),
        ("source_evidence_refs", "source_generation_id:private-123"),
        ("source_evidence_refs", "inode:12345"),
        ("source_evidence_refs", "archive_name:private-session.zip"),
    )
    for field, forbidden_value in cases:
        packet = _direct_candidate_packet()
        packet[field] = [forbidden_value]

        report = drafts.build_recovery_issue_fixture_draft_report(
            recovery_candidate_packets=[packet],
        )
        encoded = json.dumps(report, sort_keys=True)

        assert report["status"] == "fail_closed"
        assert report["drafts"] == []
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        assert forbidden_value not in encoded
        assert drafts.validate_recovery_issue_fixture_draft_report(report) == []


def test_direct_private_metadata_keys_fail_closed() -> None:
    for key in (
        "sourceGenerationId",
        "filesystemId",
        "inode",
        "archiveName",
        "fileSizeBytes",
    ):
        report = drafts.build_recovery_issue_fixture_draft_report(
            recovery_candidate_packets=[_direct_candidate_packet()],
            context={key: "symbolic"},
        )

        assert report["status"] == "fail_closed"
        assert report["drafts"] == []
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        assert drafts.validate_recovery_issue_fixture_draft_report(report) == []


def test_source_repo_action_claim_keys_fail_closed_without_echo() -> None:
    cases = (
        {"open_pr": True},
        {"createPullRequest": True},
        {"branch_name": "codex/private"},
        {"commit_sha": "a" * 40},
        {"stage_files": True},
        {"trackerUpdate": "complete"},
        {"merge_ready": True},
        {"deployReady": True},
        {"releaseReady": True},
        {"production_ready": True},
        {"github_issue_created": True},
        {"githubPrCreated": True},
    )
    for context in cases:
        report = drafts.build_recovery_issue_fixture_draft_report(
            recovery_candidate_packets=[_direct_candidate_packet()],
            context=context,
        )
        encoded = json.dumps(report, sort_keys=True)

        assert report["status"] == "fail_closed"
        assert report["drafts"] == []
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        assert "codex/private" not in encoded
        assert "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" not in encoded
        assert "complete" not in encoded
        assert drafts.validate_recovery_issue_fixture_draft_report(report) == []


def test_source_repo_action_instruction_values_fail_closed_without_echo() -> None:
    for instruction in (
        "open PR after review",
        "create branch codex/example",
        "merge after tests",
        "deploy now",
        "release after review",
    ):
        report = drafts.build_recovery_issue_fixture_draft_report(
            recovery_candidate_packets=[_direct_candidate_packet()],
            context={"context_note": instruction},
        )
        encoded = json.dumps(report, sort_keys=True)

        assert report["status"] == "fail_closed"
        assert report["drafts"] == []
        assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
        assert instruction not in encoded
        assert drafts.validate_recovery_issue_fixture_draft_report(report) == []


def test_packet_report_ref_sanitizes_unsafe_status_without_echo() -> None:
    closing_phrase = "Closes #455"
    packet_report = _direct_candidate_packet_report()
    packet_report["status"] = closing_phrase

    report = drafts.build_recovery_issue_fixture_draft_report(
        recovery_candidate_packet_report=packet_report,
    )
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail_closed"
    assert report["status_reasons"] == ["privacy_or_protected_surface_violation"]
    assert report["source_packet_report_ref"]["status"] == "unknown"
    assert closing_phrase not in encoded
    assert drafts.validate_recovery_issue_fixture_draft_report(report) == []


def test_direct_group_builder_sanitizes_unsafe_packet_text_without_echo() -> None:
    private_path = "/" + "Users" + "/example/private/" + "Player" + ".log"
    closing_phrase = "Closes #455"
    packet = _direct_candidate_packet()
    packet["field_id"] = private_path
    packet["packet_id"] = closing_phrase
    packet["source_evidence_refs"] = [private_path, closing_phrase]
    packet["offset_window_refs"] = [private_path, closing_phrase]
    packet["stop_reasons"] = [closing_phrase]

    group = drafts.build_recovery_issue_fixture_draft_group(packet)
    encoded = json.dumps(group, sort_keys=True)

    assert group["draft_status"] == "blocked_privacy"
    assert group["field_id"] == "unknown.field"
    assert group["source_packet_id"] == "unknown_packet"
    assert private_path not in encoded
    assert closing_phrase not in encoded
    assert drafts.validate_recovery_issue_fixture_draft_group(group) == []


def test_closing_keywords_are_rejected_by_issue_draft_validator() -> None:
    report = drafts.build_recovery_issue_fixture_draft_report(
        recovery_candidate_packets=[_direct_candidate_packet()],
    )
    issue_draft = json.loads(json.dumps(report["drafts"][0]["issue_draft"], sort_keys=True))
    issue_draft["body_sections"][0]["body"] = "Closes #455"

    errors = drafts.validate_recovery_issue_draft(issue_draft)

    assert "issue_draft:closing_keyword_found" in errors


def test_direct_draft_validation_rejects_forbidden_keys_without_value_echo() -> None:
    report = drafts.build_recovery_issue_fixture_draft_report(
        recovery_candidate_packets=[_direct_candidate_packet()],
    )
    group = json.loads(json.dumps(report["drafts"][0], sort_keys=True))
    group["raw_payload"] = {"public": "caller_supplied_raw_packet_value"}
    group["closes"] = "#455"
    group["issue_draft"]["exact_offset"] = 123
    group["issue_draft"]["fixes"] = "#388"

    errors = drafts.validate_recovery_issue_fixture_draft_group(group)

    assert "forbidden_key:draft_group.raw_payload" in errors
    assert "forbidden_key:draft_group.closes" in errors
    assert "forbidden_key:draft_group.issue_draft.exact_offset" in errors
    assert "forbidden_key:draft_group.issue_draft.fixes" in errors
    assert "caller_supplied_raw_packet_value" not in json.dumps(errors, sort_keys=True)
    assert "#455" not in json.dumps(errors, sort_keys=True)
    assert "#388" not in json.dumps(errors, sort_keys=True)


def test_validation_unknown_values_do_not_echo_forbidden_values() -> None:
    private_path = "/" + "Users" + "/example/private/" + "Player" + ".log"
    closing_phrase = "Closes #455"
    report = drafts.build_recovery_issue_fixture_draft_report(
        recovery_candidate_packets=[_direct_candidate_packet()],
    )
    group = json.loads(json.dumps(report["drafts"][0], sort_keys=True))
    group["draft_status"] = closing_phrase
    group["manifest_draft_summary"]["expected_sections"] = [private_path]

    errors = drafts.validate_recovery_issue_fixture_draft_group(group)
    encoded_errors = json.dumps(errors, sort_keys=True)

    assert "draft_group:draft_status:unknown" in errors
    assert "manifest_summary:expected_sections[0]:unknown" in errors
    assert private_path not in encoded_errors
    assert closing_phrase not in encoded_errors


def test_validation_unknown_keys_do_not_echo_forbidden_key_names() -> None:
    private_key = "/" + "Users" + "/example/private/" + "Player" + ".log"
    report = drafts.build_recovery_issue_fixture_draft_report(
        recovery_candidate_packets=[_direct_candidate_packet()],
    )
    issue_draft = json.loads(json.dumps(report["drafts"][0]["issue_draft"], sort_keys=True))
    issue_draft["readiness_flags"][private_key] = False
    issue_draft[private_key] = "symbolic"

    errors = drafts.validate_recovery_issue_draft(issue_draft)
    encoded_errors = json.dumps(errors, sort_keys=True)

    assert "issue_draft:readiness_flags:unknown_key" in errors
    assert "privacy:unsafe_key:issue_draft.redacted_key" in errors
    assert "privacy:unsafe_key:issue_draft.readiness_flags.redacted_key" in errors
    assert private_key not in encoded_errors


def test_inputs_are_copy_safe() -> None:
    packet_report = _direct_candidate_packet_report()
    before = json.loads(json.dumps(packet_report, sort_keys=True))

    drafts.build_recovery_issue_fixture_draft_report(
        recovery_candidate_packet_report=packet_report,
    )

    assert packet_report == before


def test_no_parser_runtime_file_writer_or_github_imports_are_used() -> None:
    imported = inspect.getsource(drafts)

    assert "from mythic_edge_parser import router" not in imported
    assert "from mythic_edge_parser.app import state" not in imported
    assert "from mythic_edge_parser.log.tailer import FileTailer" not in imported
    assert "from github" not in imported.lower()
    assert "import github" not in imported.lower()
    assert "subprocess" not in imported
    assert "open(" not in imported
    assert "Path(" not in imported
