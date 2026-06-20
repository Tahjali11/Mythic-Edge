import pytest

from mythic_edge_parser.app.local_harvest_candidate_reports import (
    HARVEST_CANDIDATE_SUMMARY_OBJECT,
    HARVEST_CANDIDATE_SUMMARY_SCHEMA_VERSION,
    UTC_LOG_SOURCE_ADAPTER_VERSION,
    HarvestCandidateReportError,
    build_harvest_candidate_report,
    parser_evidence_from_utc_log_normalization,
)
from mythic_edge_parser.app.utc_log_source_adapter import normalize_utc_log_text


def test_builds_deterministic_synthetic_player_log_summary_report() -> None:
    parser_evidence = {
        "event_counts": {"GameResult": 1, "GameState": 2},
        "event_kinds": ["GameState", "GameResult"],
        "raw_log_lines_included": False,
        "raw_payloads_included": False,
        "private_paths_included": False,
    }

    report = build_harvest_candidate_report(
        source_label="synthetic.player_log.case1",
        source_kind="synthetic_player_log",
        privacy_class="synthetic",
        parser_evidence=parser_evidence,
        scenario_family_hints=["core_gameplay.synthetic_case"],
        related_contracts=["docs/contracts/parser_evidence_local_harvest_candidate_reports.md"],
    )
    repeated = build_harvest_candidate_report(
        source_label="synthetic.player_log.case1",
        source_kind="synthetic_player_log",
        privacy_class="synthetic",
        parser_evidence=parser_evidence,
        scenario_family_hints=["core_gameplay.synthetic_case"],
        related_contracts=["docs/contracts/parser_evidence_local_harvest_candidate_reports.md"],
    )

    assert report == repeated
    assert report["object"] == HARVEST_CANDIDATE_SUMMARY_OBJECT
    assert report["schema_version"] == HARVEST_CANDIDATE_SUMMARY_SCHEMA_VERSION
    assert report["source"] == {
        "source_label": "synthetic.player_log.case1",
        "source_kind": "synthetic_player_log",
        "privacy_class": "synthetic",
        "source_adapter": "none",
        "raw_source_committed": False,
        "raw_path_included": False,
        "raw_hash_included": False,
        "raw_content_included": False,
    }
    assert report["authorization"]["authorization_status"] == "not_required_synthetic"
    assert report["authorization"]["private_harvest_authorized"] is False
    assert report["authorization"]["fixture_promotion_authorized"] is False
    assert report["summary"] == {
        "candidate_count": 1,
        "blocked_candidate_count": 0,
        "duplicate_likely_count": 0,
        "highest_privacy_risk": "none",
        "highest_coverage_value": "medium",
    }
    assert report["parser_fact_preview"]["preview_status"] == "available"
    assert report["parser_fact_preview"]["event_counts"] == {"GameResult": 1, "GameState": 2}
    assert report["parser_fact_preview"]["event_kinds"] == ["GameResult", "GameState"]
    assert report["non_claims"] == {
        "parser_behavior_verified": False,
        "corpus_status_change_authorized": False,
        "fixture_promotion_authorized": False,
        "private_harvest_authorized": False,
        "pipeline_activation_ready_for_issue_388": False,
    }
    [window] = report["candidate_windows"]
    [candidate] = window["scenario_family_candidates"]
    assert window["source_window_kind"] == "synthetic_event_range"
    assert window["public_location_included"] is True
    assert window["local_pointer_ref"] is None
    assert candidate["family_id"] == "core_gameplay.synthetic_case"
    assert candidate["candidate_status"] == "candidate"
    assert candidate["evidence_status"] == "observed"
    assert candidate["parser_behavior_verified"] is False
    assert candidate["related_contracts"] == ["docs/contracts/parser_evidence_local_harvest_candidate_reports.md"]


def test_supports_synthetic_utc_log_normalization_metadata_without_raw_text() -> None:
    normalization = normalize_utc_log_text(
        "[1] synthetic event one\n[2] synthetic event two\n",
        source_label="synthetic.utc.harvest",
    )
    parser_evidence = parser_evidence_from_utc_log_normalization(normalization)

    report = build_harvest_candidate_report(
        source_label=normalization.source_label,
        source_kind="synthetic_normalized_utc_log",
        privacy_class="synthetic",
        parser_evidence=parser_evidence,
        scenario_family_hints=["log_runtime.utc_source_adapter"],
    )

    assert report["source"]["source_adapter"] == UTC_LOG_SOURCE_ADAPTER_VERSION
    assert report["parser_fact_preview"]["event_counts"] == {"normalized_line": 2}
    assert report["parser_fact_preview"]["event_kinds"] == []
    assert report["candidate_windows"][0]["source_window_kind"] == "synthetic_line_range"
    assert report["candidate_windows"][0]["scenario_family_candidates"][0]["candidate_status"] == "candidate"
    assert normalization.text not in str(report)
    assert "synthetic event one" not in str(report)


def test_utc_log_normalization_warnings_degrade_candidate_without_verifying_behavior() -> None:
    normalization = normalize_utc_log_text(
        "[1] synthetic event without final newline",
        source_label="synthetic.utc.review",
    )

    report = build_harvest_candidate_report(
        source_label=normalization.source_label,
        source_kind="synthetic_normalized_utc_log",
        privacy_class="synthetic",
        parser_evidence=parser_evidence_from_utc_log_normalization(normalization),
        scenario_family_hints=["log_runtime.utc_source_adapter"],
    )

    candidate = report["candidate_windows"][0]["scenario_family_candidates"][0]
    assert report["parser_fact_preview"]["preview_status"] == "degraded"
    assert candidate["candidate_status"] == "review"
    assert candidate["evidence_status"] == "degraded"
    assert candidate["parser_behavior_verified"] is False
    assert "parser_evidence_has_warnings" in candidate["reasons"]


def test_private_source_class_is_blocked_without_authorization() -> None:
    report = build_harvest_candidate_report(
        source_label="operator.selected.source",
        source_kind="user_selected_player_log",
        privacy_class="private_local",
        parser_evidence={"event_counts": {"UnknownEntry": 1}},
        scenario_family_hints=["private_evidence.local_review"],
    )

    assert report["authorization"]["authorization_status"] == "missing_required"
    assert report["authorization"]["private_harvest_authorized"] is False
    assert report["candidate_windows"][0]["source_window_kind"] == "unavailable"
    assert report["candidate_windows"][0]["public_location_included"] is False
    candidate = report["candidate_windows"][0]["scenario_family_candidates"][0]
    assert candidate["candidate_status"] == "blocked_private_evidence"
    assert candidate["privacy_risk"] == "blocked"
    assert candidate["blocking_conditions"] == ["missing_private_harvest_authorization"]
    assert report["non_claims"]["pipeline_activation_ready_for_issue_388"] is False


def test_forbidden_raw_summary_content_is_rejected_without_echoing_content() -> None:
    forbidden_value = "[" + "Client " + "GRE" + "] secret-ish payload"

    report = build_harvest_candidate_report(
        source_label="synthetic.rejected.case1",
        source_kind="synthetic_player_log",
        privacy_class="synthetic",
        parser_evidence={
            "raw_text": forbidden_value,
            "event_counts": {"GameState": 1},
        },
        scenario_family_hints=["drift_debug.raw_payload_boundary"],
    )

    candidate = report["candidate_windows"][0]["scenario_family_candidates"][0]
    assert candidate["candidate_status"] == "rejected"
    assert candidate["privacy_risk"] == "blocked"
    assert candidate["blocking_conditions"] == ["forbidden_or_private_content_detected"]
    assert forbidden_value not in str(report)
    assert report["privacy"]["privacy_findings"] == ["parser_evidence:forbidden_key"]


def test_source_label_must_be_symbolic_and_error_does_not_leak_path() -> None:
    private_label = "/" + "Users/example/Library/Logs/Player.log"

    with pytest.raises(HarvestCandidateReportError) as excinfo:
        build_harvest_candidate_report(
            source_label=private_label,
            source_kind="synthetic_player_log",
            privacy_class="synthetic",
            parser_evidence={"event_counts": {"GameState": 1}},
            scenario_family_hints=["private_evidence.bad_label"],
        )

    message = str(excinfo.value)
    assert "source_label must be symbolic and public-safe" == message
    assert private_label not in message


def test_missing_parser_evidence_stays_insufficient_and_non_promotional() -> None:
    report = build_harvest_candidate_report(
        source_label="synthetic.empty.case1",
        source_kind="synthetic_player_log",
        privacy_class="synthetic",
        parser_evidence={},
        scenario_family_hints=["core_gameplay.empty_case"],
    )

    candidate = report["candidate_windows"][0]["scenario_family_candidates"][0]
    assert report["summary"]["highest_coverage_value"] == "none"
    assert report["parser_fact_preview"]["preview_status"] == "unavailable"
    assert candidate["candidate_status"] == "insufficient_evidence"
    assert candidate["blocking_conditions"] == ["insufficient_parser_evidence"]
    assert report["non_claims"]["corpus_status_change_authorized"] is False
    assert report["non_claims"]["fixture_promotion_authorized"] is False
