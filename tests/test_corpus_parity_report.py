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
        "covered_synthetic": 8,
        "covered_report_only": 0,
        "partial": 3,
        "missing": len(corpus.SCENARIO_FAMILIES) - 23,
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
        "coverage_status": "missing",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": [],
        "external_reference_status": "reference_category_not_checked",
        "notes": [],
    }
    assert _matrix_row(report, "log_runtime.timestamp_anomaly") == {
        "scenario_family": "log_runtime.timestamp_anomaly",
        "coverage_status": "missing",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": [],
        "external_reference_status": "reference_category_not_checked",
        "notes": [],
    }
    assert _matrix_row(report, "log_runtime.unknown_entry") == {
        "scenario_family": "log_runtime.unknown_entry",
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
