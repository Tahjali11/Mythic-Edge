from __future__ import annotations

import json
from pathlib import Path

import pytest

from mythic_edge_parser.app import feature_equity_corpus_ratchet as ratchet

FIXTURE_DIR = Path("tests/fixtures/golden_replay")
BASELINE_PATH = Path("tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json")
BO1_MANIFEST = FIXTURE_DIR / "bo1_match_win_basic.manifest.json"


def _baseline_payload() -> dict:
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def _manifest_payload() -> dict:
    return json.loads(BO1_MANIFEST.read_text(encoding="utf-8"))


def _write_json(tmp_path: Path, name: str, payload: dict) -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")
    return path


def test_committed_corpus_matches_initial_count_only_baseline() -> None:
    report = ratchet.build_feature_equity_corpus_report([FIXTURE_DIR], baseline_path=BASELINE_PATH)

    assert report["object"] == ratchet.FEATURE_EQUITY_CORPUS_REPORT_OBJECT
    assert report["schema_version"] == ratchet.FEATURE_EQUITY_CORPUS_REPORT_SCHEMA_VERSION
    assert report["status"] == "ok"
    assert report["status_reasons"] == []
    assert report["inputs"] == {
        "manifest_paths": [
            "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json",
            "tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json",
        ],
        "manifest_count": 2,
        "source_file_count": 2,
        "source_file_paths": [
            "tests/fixtures/parser_regression_bo3_slice.log",
            "tests/fixtures/parser_regression_match_slice.log",
        ],
        "input_kind": "golden_replay_manifest",
        "expanded_from_directories": ["tests/fixtures/golden_replay"],
        "ordering": "sorted_repo_relative_path",
    }
    assert report["baseline"]["loaded"] is True
    assert report["comparison"]["count_diffs"] == []
    assert set(report["comparison"]["matching_sections"]) == set(ratchet.COUNT_SECTIONS)
    assert report["observed"]["router_stats"] == {
        "routed": 13,
        "unknown": 0,
        "timestamp_missing": 0,
        "timestamp_parse_failure": 0,
    }
    assert report["observed"]["event_family_counts"]["GameState"] == 6
    assert report["observed"]["event_family_counts"]["Truncation"] == 0
    assert report["observed"]["payload_type_counts"]["GameState:game_state_message"] == 6
    assert report["observed"]["game_state_evidence_counts"]["diff_review_required"] == 6
    assert report["privacy"] == {
        "forbidden_content_findings": [],
        "local_absolute_paths_redacted": True,
        "privacy_class": "committed_count_only",
        "raw_log_lines_in_report": False,
        "raw_private_log_committed": False,
    }
    assert all(value is False for value in report["protected_surfaces"].values())


def test_missing_baseline_is_review_not_ok() -> None:
    report = ratchet.build_feature_equity_corpus_report([BO1_MANIFEST])

    assert report["status"] == "review"
    assert "baseline_missing" in report["status_reasons"]
    assert report["baseline"] == {
        "path": "",
        "present": False,
        "object": "",
        "schema_version": "",
        "baseline_id": "",
        "loaded": False,
        "validation_errors": [],
    }
    assert report["comparison"]["baseline_present"] is False


def test_baseline_count_mismatch_is_report_only_diff(tmp_path: Path, capsys) -> None:
    baseline = _baseline_payload()
    baseline["expected"]["router_stats"]["routed"] += 1
    baseline_path = _write_json(tmp_path, "baseline.v1.json", baseline)

    report = ratchet.build_feature_equity_corpus_report([FIXTURE_DIR], baseline_path=baseline_path)
    exit_code = ratchet.main([str(FIXTURE_DIR), "--baseline", str(baseline_path)])

    captured = capsys.readouterr()
    assert report["status"] == "diff"
    assert {
        "section": "router_stats",
        "key": "routed",
        "expected": 14,
        "observed": 13,
        "delta": -1,
        "policy": "exact",
    } in report["comparison"]["count_diffs"]
    assert exit_code == 0
    assert "Feature-equity corpus ratchet: diff" in captured.out


def test_private_manifest_is_failed_without_copying_raw_fixture_content(tmp_path: Path) -> None:
    payload = _manifest_payload()
    payload["source"]["raw_private_log_committed"] = True
    manifest_path = _write_json(tmp_path, "private.manifest.json", payload)

    report = ratchet.build_feature_equity_corpus_report([manifest_path])
    encoded = json.dumps(report, sort_keys=True)

    assert report["status"] == "fail"
    assert report["privacy"]["raw_private_log_committed"] is True
    assert report["observed"]["input_counts"]["fixtures_private_rejected"] == 1
    assert "raw_private_log_committed" in " ".join(report["status_reasons"])
    assert "opening_hand" not in encoded
    assert "raw_game_state" not in encoded


def test_malformed_baseline_schema_is_failed(tmp_path: Path) -> None:
    baseline = _baseline_payload()
    baseline["object"] = "wrong_object"
    baseline_path = _write_json(tmp_path, "bad-baseline.json", baseline)

    report = ratchet.build_feature_equity_corpus_report([FIXTURE_DIR], baseline_path=baseline_path)

    assert report["status"] == "fail"
    assert report["baseline"]["loaded"] is False
    assert report["baseline"]["validation_errors"] == ["invalid_baseline_object"]


def test_write_report_writes_only_when_explicitly_requested(tmp_path: Path) -> None:
    unwritten = tmp_path / "not-written.json"
    written = tmp_path / "report.json"

    report_without_output = ratchet.write_feature_equity_corpus_report(
        [FIXTURE_DIR],
        baseline_path=BASELINE_PATH,
        report_path=None,
    )
    report_with_output = ratchet.write_feature_equity_corpus_report(
        [FIXTURE_DIR],
        baseline_path=BASELINE_PATH,
        report_path=written,
    )

    assert not unwritten.exists()
    assert written.exists()
    assert json.loads(written.read_text(encoding="utf-8")) == report_with_output
    assert report_without_output["status"] == "ok"


def test_no_auto_update_baseline_cli_option_exists() -> None:
    with pytest.raises(SystemExit) as exc_info:
        ratchet.main([str(FIXTURE_DIR), "--update-baseline"])

    assert exc_info.value.code == 2
