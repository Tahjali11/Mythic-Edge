from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from mythic_edge_parser.app import corpus_parity_report as corpus

MANIFEST_PATH = Path("tests/fixtures/parser_corpus/corpus_manifest.v1.json")
SESSION_LEDGER_PATH = Path("tests/fixtures/parser_corpus/session_ledger.v1.json")


def _manifest_payload() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _session_ledger_payload() -> dict:
    return json.loads(SESSION_LEDGER_PATH.read_text(encoding="utf-8"))


def _write_json(tmp_path: Path, name: str, payload: dict) -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")
    return path


def _matrix_row(report: dict, scenario_family: str) -> dict:
    return next(row for row in report["coverage_matrix"] if row["scenario_family"] == scenario_family)


def _manifest_entry(manifest: dict, entry_id: str) -> dict:
    return next(entry for entry in manifest["entries"] if entry["entry_id"] == entry_id)


def _session_entry(session_ledger: dict, session_id: str) -> dict:
    return next(session for session in session_ledger["sessions"] if session["session_id"] == session_id)


def test_committed_manifest_and_session_ledger_validate_cleanly() -> None:
    manifest = corpus.load_corpus_manifest(MANIFEST_PATH)
    session_ledger = corpus.load_session_ledger(SESSION_LEDGER_PATH)

    assert corpus.validate_corpus_manifest(manifest) == []
    assert corpus.validate_session_ledger(session_ledger) == []
    assert [family["family_id"] for family in manifest["taxonomy"]["families"]] == list(corpus.SCENARIO_FAMILIES)
    assert _manifest_entry(manifest, "gsm_truncation_marker_synthetic_v1")["coverage_status"] == "covered_synthetic"
    sealed_entry = _manifest_entry(manifest, "sealed_entry_lifecycle_synthetic_v1")
    assert sealed_entry["coverage_status"] == "covered_synthetic"
    assert sealed_entry["scenario_families"] == ["core_gameplay.sealed_entry"]
    assert sealed_entry["parser_event_families"] == ["MatchState", "EventLifecycle"]
    assert sealed_entry["parser_claim_families"] == ["sealed_event_identity", "event_lifecycle"]
    assert sealed_entry["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "sealed deckbuild and sealed matches remain missing" in sealed_entry["review_notes"][0]
    sealed_match = _manifest_entry(manifest, "sealed_match_synthetic_v1")
    assert sealed_match["coverage_status"] == "covered_synthetic"
    assert sealed_match["scenario_families"] == ["core_gameplay.sealed_matches"]
    assert sealed_match["parser_event_families"] == ["MatchState", "GameState", "GameResult"]
    assert sealed_match["parser_claim_families"] == [
        "sealed_event_identity",
        "sealed_match_state",
        "sealed_game_state",
        "sealed_game_result",
        "match_summary",
    ]
    assert sealed_match["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "sealed deckbuild remains missing" in sealed_match["review_notes"][0]
    sealed_deckbuild = _manifest_entry(manifest, "sealed_deckbuild_synthetic_v1")
    assert sealed_deckbuild["coverage_status"] == "covered_synthetic"
    assert sealed_deckbuild["scenario_families"] == ["core_gameplay.sealed_deckbuild"]
    assert sealed_deckbuild["parser_event_families"] == ["MatchState", "ClientAction"]
    assert sealed_deckbuild["parser_claim_families"] == [
        "sealed_event_identity",
        "sealed_submit_deck_signal",
        "bounded_submit_deck_shape",
        "deckbuild_privacy_boundary",
    ]
    assert sealed_deckbuild["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "submitted card lists" in sealed_deckbuild["review_notes"][0]
    assert "sealed pool contents" in sealed_deckbuild["review_notes"][0]
    connection_error = _manifest_entry(manifest, "connection_error_payload_synthetic_v1")
    assert connection_error["coverage_status"] == "covered_synthetic"
    assert connection_error["scenario_families"] == ["connection.connection_error_payload"]
    assert connection_error["parser_event_families"] == ["ConnectionError"]
    assert connection_error["parser_claim_families"] == [
        "connection_error_event",
        "connection_error_type_discriminator",
        "connection_error_payload_preservation",
        "connection_error_privacy_boundary",
    ]
    assert connection_error["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "does not prove reconnect" in connection_error["review_notes"][0]
    assert "release readiness" in connection_error["review_notes"][0]
    connection_disconnect = _manifest_entry(manifest, "connection_disconnect_synthetic_v1")
    assert connection_disconnect["coverage_status"] == "covered_synthetic"
    assert connection_disconnect["scenario_families"] == ["connection.disconnect"]
    assert connection_disconnect["parser_event_families"] == [
        "MatchConnectionState",
        "TcpConnectionClose",
        "WebSocketClosed",
    ]
    assert connection_disconnect["parser_claim_families"] == [
        "connection_state_transition",
        "tcp_connection_close_payload",
        "websocket_closed_payload",
        "disconnect_privacy_boundary",
    ]
    assert connection_disconnect["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "does not prove reconnect" in connection_disconnect["review_notes"][0]
    assert "firewall/drop behavior" in connection_disconnect["review_notes"][0]
    detailed_logs_disabled = _manifest_entry(manifest, "detailed_logs_disabled_synthetic_v1")
    assert detailed_logs_disabled["coverage_status"] == "covered_synthetic"
    assert detailed_logs_disabled["scenario_families"] == ["log_runtime.detailed_logs_disabled"]
    assert detailed_logs_disabled["parser_event_families"] == ["DetailedLoggingStatus"]
    assert detailed_logs_disabled["parser_claim_families"] == [
        "detailed_logging_status_event",
        "detailed_logs_disabled_marker",
        "detailed_logging_metadata_parser",
        "detailed_logging_privacy_boundary",
    ]
    assert detailed_logs_disabled["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "does not prove live MTGA settings" in detailed_logs_disabled["review_notes"][0]
    assert "unknown-entry routing" in detailed_logs_disabled["review_notes"][0]
    timestamp_anomaly = _manifest_entry(manifest, "timestamp_anomaly_synthetic_v1")
    assert timestamp_anomaly["coverage_status"] == "covered_synthetic"
    assert timestamp_anomaly["scenario_families"] == ["log_runtime.timestamp_anomaly"]
    assert timestamp_anomaly["parser_event_families"] == []
    assert timestamp_anomaly["parser_claim_families"] == [
        "router_timestamp_missing_stat",
        "router_timestamp_parse_failure_stat",
        "router_timestamp_anomalies_aggregate",
        "timestamp_anomaly_privacy_boundary",
    ]
    assert timestamp_anomaly["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "router-owned timestamp_missing" in timestamp_anomaly["review_notes"][0]
    assert "malformed/headerless log handling" in timestamp_anomaly["review_notes"][0]
    assert "unknown-entry routing" in timestamp_anomaly["review_notes"][0]
    assert "real local Player.log timestamp drift" in timestamp_anomaly["review_notes"][0]
    malformed_headerless = _manifest_entry(manifest, "malformed_headerless_synthetic_v1")
    assert malformed_headerless["coverage_status"] == "covered_synthetic"
    assert malformed_headerless["scenario_families"] == ["log_runtime.malformed_or_headerless"]
    assert malformed_headerless["parser_event_families"] == []
    assert malformed_headerless["parser_claim_families"] == [
        "line_buffer_header_classification",
        "line_buffer_headerless_orphan_noise_ignored",
        "line_buffer_unknown_header_boundary",
        "line_buffer_partial_line_boundary",
        "line_buffer_multiline_boundary",
        "malformed_headerless_privacy_boundary",
    ]
    assert malformed_headerless["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "line-buffer and header-boundary metadata only" in malformed_headerless["review_notes"][0]
    assert "unknown-entry routing" in malformed_headerless["review_notes"][0]
    assert "semantic recovery from arbitrary malformed Player.log payloads" in malformed_headerless["review_notes"][0]
    active_player_timer = _manifest_entry(manifest, "active_player_timer_synthetic_v1")
    assert active_player_timer["coverage_status"] == "covered_synthetic"
    assert active_player_timer["scenario_families"] == ["timer.active_player_timer"]
    assert active_player_timer["parser_event_families"] == ["GameState"]
    assert active_player_timer["parser_claim_families"] == [
        "gre_timer_normalization",
        "active_player_timer_record",
        "active_player_timer_direct_seat_evidence",
        "timer_turn_info_context_boundary",
        "timer_time_unit_boundary",
        "timer_privacy_boundary",
    ]
    assert active_player_timer["coverage_basis"] == ["fixture_metadata_only", "parser_behavior_verified"]
    assert "normalized_timers GameState metadata" in active_player_timer["review_notes"][0]
    assert "does not infer timer ownership from turn_info context" in active_player_timer["review_notes"][0]
    assert "inactivity-timeout" in active_player_timer["review_notes"][0]
    assert "clock-pressure" in active_player_timer["review_notes"][0]
    assert "gameplay-advice" in active_player_timer["review_notes"][0]
    unknown_entry = _manifest_entry(manifest, "unknown_entry_drift_report_reference_v1")
    assert unknown_entry["coverage_status"] == "covered_report_only"
    assert unknown_entry["scenario_families"] == ["log_runtime.unknown_entry"]
    assert unknown_entry["parser_event_families"] == []
    assert unknown_entry["parser_claim_families"] == [
        "router_unknown_entry_count",
        "drift_unknown_signature_review_samples",
        "drift_unmatched_api_name_review_samples",
        "diagnostics_unknown_entries_review_status",
        "evidence_ledger_unknown_entry_count_boundary",
        "unknown_entry_privacy_boundary",
    ]
    assert unknown_entry["coverage_basis"] == [
        "diagnostics_only",
        "fixture_metadata_only",
        "evidence_ledger_only",
    ]
    assert unknown_entry["paths"]["normalized_drift_report_reference"] == (
        "tests/fixtures/player_log_drift_flush_timing_expected.json"
    )
    assert "flush_timing_corpus_slice.log" not in unknown_entry["paths"].values()
    assert "unknown counts and review samples" in unknown_entry["review_notes"][0]
    assert "does not mean the parser understood the unknown entries" in unknown_entry["review_notes"][0]
    assert "parser support for unknown semantic content" in unknown_entry["known_gaps"][0]
    assert "live private Player.log drift health" in unknown_entry["known_gaps"][0]
    assert _session_entry(session_ledger, "gsm_truncation_marker_synthetic_v1")["parser_coverage"] == {
        "event_families": {"Truncation": 1},
        "unknown_entries": 0,
        "truncation_count": 1,
    }
    sealed_session = _session_entry(session_ledger, "sealed_entry_lifecycle_synthetic_v1")
    assert sealed_session["format_family"] == "limited_sealed"
    assert sealed_session["match_shape"] == "sealed_entry_only"
    assert sealed_session["parser_coverage"] == {
        "event_families": {"MatchState": 1, "EventLifecycle": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
    }
    assert sealed_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    connection_disconnect_session = _session_entry(session_ledger, "connection_disconnect_synthetic_v1")
    assert connection_disconnect_session["format_family"] == "connection_runtime"
    assert connection_disconnect_session["match_shape"] == "connection_disconnect_signal_only"
    assert connection_disconnect_session["parser_coverage"] == {
        "event_families": {"MatchConnectionState": 1, "TcpConnectionClose": 1, "WebSocketClosed": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
    }
    assert connection_disconnect_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert connection_disconnect_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    detailed_logs_disabled_session = _session_entry(session_ledger, "detailed_logs_disabled_synthetic_v1")
    assert detailed_logs_disabled_session["format_family"] == "log_runtime"
    assert detailed_logs_disabled_session["match_shape"] == "detailed_logging_status_signal_only"
    assert detailed_logs_disabled_session["parser_coverage"] == {
        "event_families": {"DetailedLoggingStatus": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
    }
    assert detailed_logs_disabled_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert detailed_logs_disabled_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    timestamp_anomaly_session = _session_entry(session_ledger, "timestamp_anomaly_synthetic_v1")
    assert timestamp_anomaly_session["format_family"] == "log_runtime"
    assert timestamp_anomaly_session["match_shape"] == "timestamp_anomaly_signal_only"
    assert timestamp_anomaly_session["record_summary"] == "synthetic_router_stats_summary_only"
    assert timestamp_anomaly_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "timestamp_missing": 1,
        "timestamp_parse_failure": 1,
        "timestamp_anomalies": 2,
    }
    assert timestamp_anomaly_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert timestamp_anomaly_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    malformed_headerless_session = _session_entry(session_ledger, "malformed_headerless_synthetic_v1")
    assert malformed_headerless_session["format_family"] == "log_runtime"
    assert malformed_headerless_session["match_shape"] == "line_buffer_boundary_signal_only"
    assert malformed_headerless_session["record_summary"] == "synthetic_line_buffer_summary_only"
    assert malformed_headerless_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 0,
        "truncation_count": 0,
        "line_buffer_headerless_orphan_lines_ignored": 1,
        "line_buffer_unknown_header_entries": 1,
        "line_buffer_partial_fragments_joined": 1,
        "line_buffer_multiline_entries_finalized": 1,
        "line_buffer_single_line_headers_emitted": 1,
    }
    assert malformed_headerless_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert malformed_headerless_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    active_player_timer_session = _session_entry(session_ledger, "active_player_timer_synthetic_v1")
    assert active_player_timer_session["format_family"] == "timer_runtime"
    assert active_player_timer_session["match_shape"] == "active_player_timer_signal_only"
    assert active_player_timer_session["record_summary"] == "synthetic_timer_normalization_summary_only"
    assert active_player_timer_session["parser_coverage"] == {
        "event_families": {"GameState": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
        "normalized_timer_records": 1,
        "active_player_timer_records": 1,
        "timer_records_with_direct_seat_evidence": 1,
        "timer_records_with_contextual_active_player": 1,
        "timer_records_with_seconds_values": 1,
        "timer_records_with_milliseconds_values": 1,
        "timer_degraded_records": 0,
    }
    assert active_player_timer_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert active_player_timer_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    unknown_entry_session = _session_entry(session_ledger, "unknown_entry_drift_report_reference_v1")
    assert unknown_entry_session["format_family"] == "log_runtime"
    assert unknown_entry_session["match_shape"] == "unknown_entry_drift_report_reference_only"
    assert unknown_entry_session["record_summary"] == "normalized_drift_report_reference_only"
    assert unknown_entry_session["parser_coverage"] == {
        "event_families": {},
        "unknown_entries": 7,
        "truncation_count": 0,
        "drift_report_status": "review",
        "unknown_signatures": 4,
        "unmatched_api_names": 3,
        "unmatched_request_api_names": 3,
        "routed_event_families": 0,
    }
    assert unknown_entry_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert unknown_entry_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    sealed_match_session = _session_entry(session_ledger, "sealed_match_synthetic_v1")
    assert sealed_match_session["format_family"] == "limited_sealed"
    assert sealed_match_session["match_shape"] == "sealed_match_single_game"
    assert sealed_match_session["parser_coverage"] == {
        "event_families": {"MatchState": 1, "GameState": 1, "GameResult": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
    }
    assert sealed_match_session["game_rows"] == {"count": 1, "result_shape": "single_game_result"}
    assert sealed_match_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    sealed_deckbuild_session = _session_entry(session_ledger, "sealed_deckbuild_synthetic_v1")
    assert sealed_deckbuild_session["format_family"] == "limited_sealed"
    assert sealed_deckbuild_session["match_shape"] == "sealed_deckbuild_submit_deck_signal_only"
    assert sealed_deckbuild_session["parser_coverage"] == {
        "event_families": {"MatchState": 1, "ClientAction": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
    }
    assert sealed_deckbuild_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert sealed_deckbuild_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }
    connection_error_session = _session_entry(session_ledger, "connection_error_payload_synthetic_v1")
    assert connection_error_session["format_family"] == "connection_runtime"
    assert connection_error_session["match_shape"] == "connection_error_payload_signal_only"
    assert connection_error_session["parser_coverage"] == {
        "event_families": {"ConnectionError": 1},
        "unknown_entries": 0,
        "truncation_count": 0,
    }
    assert connection_error_session["game_rows"] == {"count": 0, "result_shape": "not_applicable"}
    assert connection_error_session["report_only_redactions"] == {
        "raw_log_lines_included": False,
        "private_paths_included": False,
        "raw_payloads_included": False,
        "external_logs_included": False,
        "decklists_included": False,
    }


def test_build_report_maps_corpus_coverage_without_parser_truth_claims() -> None:
    report = corpus.build_corpus_parity_report(MANIFEST_PATH, session_ledger_path=SESSION_LEDGER_PATH)

    assert report["object"] == corpus.REPORT_OBJECT
    assert report["schema_version"] == corpus.REPORT_SCHEMA_VERSION
    assert report["status"] == "partial_coverage_map_ready"
    assert report["inputs"]["corpus_manifest_path"] == "tests/fixtures/parser_corpus/corpus_manifest.v1.json"
    assert report["inputs"]["session_ledger_path"] == "tests/fixtures/parser_corpus/session_ledger.v1.json"
    assert report["summary"] == {
        "total_scenario_families": len(corpus.SCENARIO_FAMILIES),
        "covered_committed": 6,
        "covered_synthetic": 11,
        "covered_report_only": 1,
        "partial": 3,
        "missing": len(corpus.SCENARIO_FAMILIES) - 27,
        "deferred": 0,
        "blocked_private_evidence": 0,
        "blocked_external_boundary": 6,
        "not_applicable": 0,
    }
    assert _matrix_row(report, "core_gameplay.standard_bo1") == {
        "scenario_family": "core_gameplay.standard_bo1",
        "coverage_status": "covered_committed",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["bo1_match_win_basic"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [],
    }
    assert _matrix_row(report, "core_gameplay.draft_only")["coverage_status"] == "covered_synthetic"
    gsm_row = _matrix_row(report, "drift_debug.gsm_truncation")
    assert gsm_row["coverage_status"] == "covered_synthetic"
    assert gsm_row["coverage_status"] != "covered_committed"
    assert gsm_row["coverage_basis"] == [
        "count_ratchet_only",
        "diagnostics_only",
        "fixture_metadata_only",
        "parser_behavior_verified",
    ]
    assert gsm_row["mythic_edge_entries"] == [
        "feature_equity_corpus_baseline_v1",
        "gsm_truncation_marker_synthetic_v1",
    ]
    assert "GSM truncation is parser-owned data-loss evidence, not recovered GameState truth." in gsm_row["notes"]
    assert _matrix_row(report, "core_gameplay.sealed_entry") == {
        "scenario_family": "core_gameplay.sealed_entry",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["sealed_entry_lifecycle_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic sealed entry coverage proves sealed context plus event-entry lifecycle metadata only; "
            "sealed deckbuild and sealed matches remain missing."
        ],
    }
    assert _matrix_row(report, "core_gameplay.sealed_deckbuild") == {
        "scenario_family": "core_gameplay.sealed_deckbuild",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["sealed_deckbuild_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic sealed deckbuild coverage proves sealed context plus bounded submit-deck signal metadata "
            "only; it does not include submitted card lists, sealed pool contents, deck names, card choices, "
            "analytics truth, AI truth, or coaching truth."
        ],
    }
    assert _matrix_row(report, "core_gameplay.sealed_matches") == {
        "scenario_family": "core_gameplay.sealed_matches",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["sealed_match_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic sealed match coverage proves sealed context plus parser-owned match/game result summary "
            "metadata only; sealed deckbuild remains missing."
        ],
    }
    assert _matrix_row(report, "log_runtime.detailed_logs_disabled") == {
        "scenario_family": "log_runtime.detailed_logs_disabled",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["detailed_logs_disabled_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic detailed logs disabled coverage proves parser-owned DetailedLoggingStatus metadata only; "
            "it does not prove live MTGA settings, log rotation, malformed/headerless log handling, timestamp "
            "anomaly handling, unknown-entry routing, private smoke, release readiness, analytics truth, "
            "AI truth, coaching truth, or production behavior."
        ],
    }
    assert _matrix_row(report, "log_runtime.rotation")["coverage_status"] == "blocked_external_boundary"
    assert _matrix_row(report, "log_runtime.malformed_or_headerless") == {
        "scenario_family": "log_runtime.malformed_or_headerless",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["malformed_headerless_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic malformed/headerless coverage proves line-buffer and header-boundary metadata only; "
            "it does not prove unknown-entry routing, log drift detection, log rotation, semantic recovery "
            "from arbitrary malformed Player.log payloads, private smoke, release readiness, analytics truth, "
            "AI truth, coaching truth, or production behavior."
        ],
    }
    assert _matrix_row(report, "log_runtime.timestamp_anomaly") == {
        "scenario_family": "log_runtime.timestamp_anomaly",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["timestamp_anomaly_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic timestamp anomaly coverage proves router-owned timestamp_missing, "
            "timestamp_parse_failure, and timestamp_anomalies stats only; it does not prove "
            "malformed/headerless log handling, unknown-entry routing, log rotation, real local "
            "Player.log timestamp drift, private smoke, release readiness, analytics truth, AI truth, "
            "coaching truth, or production behavior."
        ],
    }
    assert _matrix_row(report, "log_runtime.unknown_entry") == {
        "scenario_family": "log_runtime.unknown_entry",
        "coverage_status": "covered_report_only",
        "coverage_basis": ["diagnostics_only", "evidence_ledger_only", "fixture_metadata_only"],
        "mythic_edge_entries": ["unknown_entry_drift_report_reference_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Unknown-entry coverage proves that existing drift/diagnostics reports can surface unknown counts "
            "and review samples from a committed normalized report reference; it does not mean the parser "
            "understood the unknown entries."
        ],
    }
    assert _matrix_row(report, "mythic_edge.private_log_report_only_drift") == {
        "scenario_family": "mythic_edge.private_log_report_only_drift",
        "coverage_status": "missing",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": [],
        "external_reference_status": "reference_category_not_checked",
        "notes": [],
    }
    assert _matrix_row(report, "connection.connection_error_payload") == {
        "scenario_family": "connection.connection_error_payload",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["connection_error_payload_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic connection error payload coverage proves parser-owned ConnectionError payload metadata "
            "only; it does not prove reconnect, disconnect, network reliability, private smoke, release "
            "readiness, analytics truth, AI truth, or production behavior."
        ],
    }
    assert _matrix_row(report, "connection.reconnect")["coverage_status"] == "blocked_external_boundary"
    assert _matrix_row(report, "connection.disconnect") == {
        "scenario_family": "connection.disconnect",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["connection_disconnect_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic connection disconnect coverage proves parser-owned MatchConnectionState, "
            "TcpConnectionClose, and WebSocketClosed metadata only; it does not prove reconnect, "
            "firewall/drop behavior, network reliability, private smoke, release readiness, analytics truth, "
            "AI truth, coaching truth, or production behavior."
        ],
    }
    assert _matrix_row(report, "connection.firewall_or_network_drop") == {
        "scenario_family": "connection.firewall_or_network_drop",
        "coverage_status": "missing",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": [],
        "external_reference_status": "reference_category_not_checked",
        "notes": [],
    }
    assert _matrix_row(report, "timer.active_player_timer") == {
        "scenario_family": "timer.active_player_timer",
        "coverage_status": "covered_synthetic",
        "coverage_basis": ["fixture_metadata_only", "parser_behavior_verified"],
        "mythic_edge_entries": ["active_player_timer_synthetic_v1"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Synthetic active player timer coverage proves parser-owned normalized_timers GameState metadata "
            "only; it does not infer timer ownership from turn_info context or claim clock-pressure, rope, "
            "inactivity-timeout, gameplay-advice, analytics, AI, coaching, release, or production truth."
        ],
    }
    assert _matrix_row(report, "timer.inactivity_timeout") == {
        "scenario_family": "timer.inactivity_timeout",
        "coverage_status": "blocked_external_boundary",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": ["external_reference_category_boundary"],
        "external_reference_status": "reference_category_not_checked",
        "notes": [
            "Reference categories require future Mythic Edge fixtures or report-only evidence before support claims."
        ],
    }
    assert _matrix_row(report, "timer.pre_match_idle") == {
        "scenario_family": "timer.pre_match_idle",
        "coverage_status": "missing",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": [],
        "external_reference_status": "reference_category_not_checked",
        "notes": [],
    }
    assert report["privacy"] == {
        "raw_private_log_committed": False,
        "external_logs_committed": False,
        "raw_log_lines_in_report": False,
        "local_absolute_paths_redacted": True,
        "forbidden_content_findings": [],
    }
    assert all(value is False for value in report["protected_surfaces"].values())
    assert any("Reports do not decide merge readiness" in item for item in report["limitations"])


def test_private_manifest_metadata_blocks_without_echoing_sensitive_path(tmp_path: Path) -> None:
    manifest = _manifest_payload()
    private_path = "/" + "Users/example/private/session-data.txt"
    manifest["source_privacy"]["raw_private_log_committed"] = True
    manifest["entries"][0]["review_notes"] = [f"{private_path} should stay out of reports"]
    manifest_path = _write_json(tmp_path, "private-manifest.json", manifest)

    report = corpus.build_corpus_parity_report(manifest_path, session_ledger_path=SESSION_LEDGER_PATH)
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "blocked_private_artifact_risk"
    assert "source_privacy_not_false:raw_private_log_committed" in report["status_reasons"]
    assert "forbidden_content:local_absolute_path" in report["status_reasons"]
    assert private_path not in encoded
    assert "<redacted-local-path>" in encoded


def test_external_artifact_paths_are_blocked_as_reference_boundaries(tmp_path: Path) -> None:
    manifest = _manifest_payload()
    manifest["entries"][0] = deepcopy(manifest["entries"][0])
    manifest["entries"][0]["paths"]["external_log"] = "external/manasight/session.log.gz"
    manifest_path = _write_json(tmp_path, "external-manifest.json", manifest)

    report = corpus.build_corpus_parity_report(manifest_path)

    assert report["status"] == "blocked_external_boundary"
    assert "external_artifact_path:bo1_match_win_basic:external_log" in report["status_reasons"]
    assert "forbidden_artifact_path:bo1_match_win_basic:external_log" in report["status_reasons"]


def test_session_ledger_rejects_non_redacted_report_only_flags(tmp_path: Path) -> None:
    ledger = _session_ledger_payload()
    ledger["sessions"][0]["report_only_redactions"]["private_paths_included"] = True
    ledger_path = _write_json(tmp_path, "session-ledger.json", ledger)

    errors = corpus.validate_session_ledger(corpus.load_session_ledger(ledger_path))

    assert errors == [
        "session_redaction_flag_not_false:standard_bo1_match_win_basic_v1:private_paths_included"
    ]


def test_cli_writes_report_only_when_output_is_explicit(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    output_path = tmp_path / "corpus-parity-report.json"

    exit_code = corpus.main(
        [str(MANIFEST_PATH), "--session-ledger", str(SESSION_LEDGER_PATH), "--out", str(output_path)]
    )

    captured = capsys.readouterr()
    written_report = json.loads(output_path.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert "Corpus parity report: partial_coverage_map_ready" in captured.out
    assert "Report written: <outside_repo>" in captured.out
    assert written_report["status"] == "partial_coverage_map_ready"
    assert written_report["inputs"]["explicit_inputs_required"] is True


def test_cli_requires_manifest_path() -> None:
    with pytest.raises(SystemExit) as exc_info:
        corpus.main([])

    assert exc_info.value.code == 2
