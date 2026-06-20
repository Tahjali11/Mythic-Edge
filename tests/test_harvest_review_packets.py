import dataclasses

import pytest

from mythic_edge_parser.app.harvest_review_packets import (
    HARVEST_REVIEW_PACKET_OBJECT,
    HARVEST_REVIEW_PACKET_SCHEMA_VERSION,
    HARVEST_REVIEW_PRIVACY_REPORT_OBJECT,
    HARVEST_REVIEW_PRIVACY_REPORT_SCHEMA_VERSION,
    HARVEST_REVIEWER_DECISION_OBJECT,
    HARVEST_REVIEWER_DECISION_SCHEMA_VERSION,
    HarvestReviewPacketError,
    build_harvest_review_packet,
)
from mythic_edge_parser.app.local_harvest_candidate_reports import build_harvest_candidate_report

PRIVATE_POSIX_PATH = "/" + "Users/example/private/Player.log"
PRIVATE_WINDOWS_PATH = "C:" + "\\Users\\Example\\private\\Player.log"
PRIVATE_WINDOWS_MARKER = "\\Users" + "\\Example\\private"
PRIVATE_POSIX_PATH_ENCODED = "%2F" + "Users%2Fexample%2Fprivate%2FPlayer.log"
PRIVATE_FILE_URI_ENCODED = "file%3A%2F%2F%2F" + "Users%2Fexample%2Fprivate%2FPlayer.log"
PRIVATE_FILE_LOCALHOST_URI_ENCODED = "file%3A%2F%2Flocalhost%2F" + "Users%2Fexample%2Fprivate%2FPlayer.log"


def _candidate_summary(**overrides: object) -> dict:
    report = build_harvest_candidate_report(
        source_label="synthetic.harvest.case1",
        source_kind="synthetic_player_log",
        privacy_class="synthetic",
        parser_evidence={
            "event_counts": {"GameState": 2, "GameResult": 1},
            "event_kinds": ["GameState", "GameResult"],
            "raw_log_lines_included": False,
            "raw_payloads_included": False,
            "private_paths_included": False,
        },
        scenario_family_hints=["core_gameplay.synthetic_review"],
        related_contracts=["docs/contracts/parser_evidence_local_harvest_candidate_reports.md"],
    )
    report.update(overrides)
    return report


def test_builds_deterministic_in_memory_review_packet_from_candidate_summary() -> None:
    candidate = _candidate_summary()

    packet = build_harvest_review_packet(candidate_summary=candidate)
    repeated = build_harvest_review_packet(candidate_summary=candidate)

    assert packet == repeated
    assert packet["object"] == HARVEST_REVIEW_PACKET_OBJECT
    assert packet["schema_version"] == HARVEST_REVIEW_PACKET_SCHEMA_VERSION
    assert packet["packet_status"] == "review_required"
    assert packet["source"] == {
        "candidate_report_object": "mythic_edge_harvest_candidate_summary",
        "candidate_report_schema_version": "parser_evidence_harvest_candidate_summary.v1",
        "candidate_report_id": "synthetic.harvest.case1:candidate-summary",
        "source_label": "synthetic.harvest.case1",
        "privacy_class": "synthetic",
        "raw_source_committed": False,
        "raw_path_included": False,
        "raw_hash_included": False,
        "raw_content_included": False,
    }
    assert packet["authorization"] == {
        "private_harvest_authorized": False,
        "file_writing_authorized": False,
        "fixture_promotion_authorized": False,
        "corpus_status_change_authorized": False,
    }
    assert all(value is False for value in packet["non_claims"].values())
    assert packet["artifacts"]["reviewer_decision_json"] is None
    assert packet["artifacts"]["privacy_report_json"]["status"] == "pass"
    assert packet["artifacts"]["parser_fact_preview_json"]["event_counts"] == {
        "GameResult": 1,
        "GameState": 2,
    }
    assert "core_gameplay.synthetic_review" in packet["artifacts"]["candidate_summary_markdown"]
    assert "Raw logs included: `false`" in packet["artifacts"]["redacted_context_markdown"]


def test_supports_public_safe_reviewer_context_and_decision_metadata() -> None:
    packet = build_harvest_review_packet(
        candidate_summary=_candidate_summary(),
        reviewer_context={
            "context_id": "codex-e.synthetic-review",
            "notes": ["public safe reduced packet review"],
        },
        reviewer_decision={
            "decision_id": "codex-e.synthetic-review.decision",
            "reviewer_role": "codex_e",
            "decision_status": "approve_for_followup",
            "rationale": ["candidate merits a future scoped followup"],
            "allowed_next_route": "codex_a_problem_representation",
        },
    )

    assert packet["packet_status"] == "reviewed_followup_candidate"
    assert packet["reviewer_context"] == {
        "context_id": "codex-e.synthetic-review",
        "notes": ["public safe reduced packet review"],
    }
    decision = packet["artifacts"]["reviewer_decision_json"]
    assert decision["object"] == HARVEST_REVIEWER_DECISION_OBJECT
    assert decision["schema_version"] == HARVEST_REVIEWER_DECISION_SCHEMA_VERSION
    assert decision["decision_status"] == "approve_for_followup"
    assert decision["blocked_routes"] == [
        "fixture_promotion",
        "private_harvest_execution",
        "corpus_status_change",
    ]
    assert all(value is False for value in decision["non_claims"].values())
    assert packet["non_claims"]["pipeline_activation_ready_for_issue_388"] is False


def test_private_source_candidate_summary_is_blocked_without_promotion_claims() -> None:
    candidate = build_harvest_candidate_report(
        source_label="operator.selected.source",
        source_kind="user_selected_player_log",
        privacy_class="private_local",
        parser_evidence={"event_counts": {"UnknownEntry": 1}},
        scenario_family_hints=["private_evidence.local_review"],
    )

    packet = build_harvest_review_packet(candidate_summary=candidate)

    assert packet["packet_status"] == "blocked_authorization"
    assert packet["source"]["privacy_class"] == "private_local"
    assert packet["artifacts"]["privacy_report_json"]["status"] == "block"
    assert "private source review requires a separate approval" in packet["artifacts"]["redacted_context_markdown"]
    assert packet["non_claims"]["private_harvest_authorized"] is False
    assert packet["non_claims"]["fixture_promotion_authorized"] is False
    assert packet["non_claims"]["pipeline_activation_ready_for_issue_388"] is False


def test_forbidden_raw_fields_block_privacy_without_echoing_values() -> None:
    forbidden_value = "[" + "Client " + "GRE" + "] secret-ish payload"
    candidate = _candidate_summary()
    candidate["unsafe"] = {"raw_text": forbidden_value}

    packet = build_harvest_review_packet(candidate_summary=candidate)

    assert packet["packet_status"] == "blocked_privacy"
    privacy_report = packet["artifacts"]["privacy_report_json"]
    assert privacy_report["object"] == HARVEST_REVIEW_PRIVACY_REPORT_OBJECT
    assert privacy_report["schema_version"] == HARVEST_REVIEW_PRIVACY_REPORT_SCHEMA_VERSION
    assert privacy_report["status"] == "block"
    assert privacy_report["findings"][0]["field"] == "candidate_summary.unsafe.raw_text"
    assert privacy_report["findings"][0]["reason"] == "forbidden_key"
    assert forbidden_value not in str(packet)


def test_upstream_privacy_findings_block_even_when_values_were_already_redacted() -> None:
    candidate = build_harvest_candidate_report(
        source_label="synthetic.rejected.case1",
        source_kind="synthetic_player_log",
        privacy_class="synthetic",
        parser_evidence={
            "raw_text": "[" + "Client " + "GRE" + "] secret-ish payload",
            "event_counts": {"GameState": 1},
        },
        scenario_family_hints=["drift_debug.raw_payload_boundary"],
    )

    packet = build_harvest_review_packet(candidate_summary=candidate)

    assert packet["packet_status"] == "blocked_privacy"
    assert packet["artifacts"]["parser_fact_preview_json"]["preview_status"] == "blocked"
    assert any(
        finding["reason"] == "upstream_privacy_finding"
        for finding in packet["artifacts"]["privacy_report_json"]["findings"]
    )
    assert packet["non_claims"]["parser_behavior_verified"] is False


def test_unsupported_candidate_summary_schema_routes_to_contract_update_without_echo() -> None:
    candidate = _candidate_summary(schema_version="future.private.schema")

    packet = build_harvest_review_packet(candidate_summary=candidate)

    assert packet["packet_status"] == "reviewed_deferred"
    assert packet["source"]["candidate_report_schema_version"] == "unsupported"
    assert packet["validation"]["schema_issue"] == "unsupported_candidate_summary_schema"
    assert packet["validation"]["status_reasons"] == [
        "unsupported_candidate_summary_schema",
        "reviewer_decision_not_supplied",
    ]
    assert packet["source"]["privacy_class"] == "local_only_redacted"
    assert "future.private.schema" not in str(packet)
    assert packet["non_claims"]["full_parser_regression_parity"] is False


def test_malformed_reviewer_decision_routes_to_contract_update() -> None:
    packet = build_harvest_review_packet(
        candidate_summary=_candidate_summary(),
        reviewer_decision={
            "object": "mythic_edge_unknown_reviewer_decision",
            "decision_status": "approve_for_followup",
        },
    )

    assert packet["packet_status"] == "reviewed_deferred"
    decision = packet["artifacts"]["reviewer_decision_json"]
    assert decision["decision_status"] == "needs_contract_update"
    assert decision["allowed_next_route"] == "codex_b_contract"
    assert packet["non_claims"]["corpus_status_change_authorized"] is False


def test_reviewer_context_forbidden_content_blocks_without_echoing_value() -> None:
    private_path = PRIVATE_POSIX_PATH

    packet = build_harvest_review_packet(
        candidate_summary=_candidate_summary(),
        reviewer_context={"note": f"looked at {private_path}"},
    )

    assert packet["packet_status"] == "blocked_privacy"
    assert packet["reviewer_context"] == {"status": "blocked", "finding_count": 1}
    assert private_path not in str(packet)
    assert packet["artifacts"]["privacy_report_json"]["findings"][0]["field"] == "reviewer_context.note"


def test_reviewer_context_assignment_prefixed_private_path_blocks_without_echo() -> None:
    private_path = PRIVATE_POSIX_PATH

    packet = build_harvest_review_packet(
        candidate_summary=_candidate_summary(),
        reviewer_context={"note": f"file={private_path}"},
    )

    assert packet["packet_status"] == "blocked_privacy"
    assert packet["reviewer_context"] == {"status": "blocked", "finding_count": 1}
    assert private_path not in str(packet)
    assert packet["artifacts"]["privacy_report_json"]["findings"][0]["reason"] == "forbidden_text"


@pytest.mark.parametrize(
    "note,private_marker",
    [
        ("uri=file:" + "//" + PRIVATE_POSIX_PATH, PRIVATE_POSIX_PATH),
        ("uri=file://localhost" + PRIVATE_POSIX_PATH, PRIVATE_POSIX_PATH),
        ("uri:file://localhost" + PRIVATE_POSIX_PATH, PRIVATE_POSIX_PATH),
        ("vscode://file" + PRIVATE_POSIX_PATH, PRIVATE_POSIX_PATH),
        ("source_path:" + PRIVATE_POSIX_PATH, PRIVATE_POSIX_PATH),
        ("windows_path:" + PRIVATE_WINDOWS_PATH, PRIVATE_WINDOWS_MARKER),
        ("encoded=" + PRIVATE_POSIX_PATH_ENCODED, PRIVATE_POSIX_PATH),
        (
            "encoded=" + PRIVATE_FILE_URI_ENCODED,
            PRIVATE_POSIX_PATH,
        ),
        (
            "encoded=" + PRIVATE_FILE_LOCALHOST_URI_ENCODED,
            PRIVATE_POSIX_PATH,
        ),
    ],
)
def test_reviewer_context_labeled_or_encoded_private_paths_block_without_echo(
    note: str,
    private_marker: str,
) -> None:
    packet = build_harvest_review_packet(
        candidate_summary=_candidate_summary(),
        reviewer_context={"note": note},
    )

    packet_text = str(packet)
    assert packet["packet_status"] == "blocked_privacy"
    assert packet["reviewer_context"] == {"status": "blocked", "finding_count": 1}
    assert note not in packet_text
    assert private_marker not in packet_text
    assert packet["artifacts"]["privacy_report_json"]["findings"][0]["reason"] == "forbidden_text"


def test_reviewer_context_public_https_url_remains_public_safe() -> None:
    note = "repo=https://github.com/Tahjali11/Mythic-Edge/issues/383"

    packet = build_harvest_review_packet(
        candidate_summary=_candidate_summary(),
        reviewer_context={"note": note},
    )

    assert packet["packet_status"] == "review_required"
    assert packet["reviewer_context"] == {"note": note}
    assert packet["artifacts"]["privacy_report_json"]["status"] == "pass"


def test_non_mapping_candidate_summary_fails_closed_without_value_echo() -> None:
    bad_value = dataclasses.make_dataclass("BadCandidate", [("raw_text", str)])("private-ish")

    with pytest.raises(HarvestReviewPacketError) as excinfo:
        build_harvest_review_packet(candidate_summary=bad_value)  # type: ignore[arg-type]

    assert str(excinfo.value) == "candidate_summary must be a mapping"
    assert "private-ish" not in str(excinfo.value)
