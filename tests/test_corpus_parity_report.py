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
        "covered_synthetic": 4,
        "covered_report_only": 0,
        "partial": 3,
        "missing": len(corpus.SCENARIO_FAMILIES) - 19,
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
        "coverage_status": "missing",
        "coverage_basis": ["external_reference_only"],
        "mythic_edge_entries": [],
        "external_reference_status": "reference_category_not_checked",
        "notes": [],
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
    assert _matrix_row(report, "connection.reconnect")["coverage_status"] == "blocked_external_boundary"
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
