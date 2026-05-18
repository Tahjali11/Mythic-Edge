from __future__ import annotations

import json
from pathlib import Path

import pytest

from mythic_edge_parser.app import golden_replay

FIXTURE_DIR = Path("tests/fixtures/golden_replay")
BO1_MANIFEST = FIXTURE_DIR / "bo1_match_win_basic.manifest.json"
BO3_MANIFEST = FIXTURE_DIR / "bo3_sideboard_match_loss.manifest.json"


def _manifest_payload(path: Path = BO1_MANIFEST) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_manifest(tmp_path: Path, payload: dict) -> Path:
    manifest_path = tmp_path / "fixture.manifest.json"
    manifest_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest_path


def test_committed_golden_manifests_pass_through_normal_parser_path() -> None:
    report = golden_replay.build_golden_replay_report([BO1_MANIFEST, BO3_MANIFEST])

    assert report["object"] == "mythic_edge_golden_replay_report"
    assert report["schema_version"] == "parser_golden_replay_report.v1"
    assert report["suite_status"] == "pass"
    assert report["summary"] == {
        "manifests_total": 2,
        "pass": 2,
        "degraded": 0,
        "review": 0,
        "diff": 0,
        "fail": 0,
        "fixtures_with_truncation": 0,
        "fixtures_with_data_loss": 0,
    }
    assert [result["fixture_id"] for result in report["results"]] == [
        "bo1_match_win_basic",
        "bo3_sideboard_match_loss",
    ]
    assert report["metadata"]["normal_parser_path"] == [
        "LineBuffer",
        "Router",
        "parser modules",
        "transforms",
        "parser state",
    ]


def test_run_golden_replay_reports_reduced_expected_manifest_diffs(tmp_path: Path) -> None:
    payload = _manifest_payload()
    payload["expected"]["final_reconciliation"]["match_winner_team"] = 2

    result = golden_replay.run_golden_replay(_write_manifest(tmp_path, payload))

    assert result.status == "diff"
    assert result.comparisons["final_reconciliation"] == "diff"
    assert result.diffs == [
        {
            "manifest_path": "fixture.manifest.json",
            "fixture_id": "bo1_match_win_basic",
            "section": "final_reconciliation",
            "json_pointer": "/expected/final_reconciliation/match_winner_team",
            "expected": 2,
            "observed": 1,
            "truth_layer": "parser_owned_truth",
        }
    ]


def test_expected_degradation_is_reported_and_cli_exits_zero(tmp_path: Path, capsys) -> None:
    payload = _manifest_payload()
    payload["coverage"]["known_gaps"] = ["fixture_gap_for_future_parser_evidence"]
    manifest_path = _write_manifest(tmp_path, payload)

    result = golden_replay.run_golden_replay(manifest_path)
    report = golden_replay.build_golden_replay_report([manifest_path])
    exit_code = golden_replay.main([str(manifest_path)])

    captured = capsys.readouterr()
    assert result.status == "degraded"
    assert result.degradation == ["known_gaps:fixture_gap_for_future_parser_evidence"]
    assert report["suite_status"] == "degraded"
    assert report["metadata"]["degraded_cli_exit_code"] == 0
    assert exit_code == 0
    assert "Golden replay: degraded" in captured.out


def test_manifest_privacy_fields_are_required_before_replay(tmp_path: Path) -> None:
    payload = _manifest_payload()
    payload["source"]["raw_private_log_committed"] = True

    result = golden_replay.run_golden_replay(_write_manifest(tmp_path, payload))

    assert result.status == "fail"
    assert "raw_private_log_committed_must_be_false" in result.failures
    assert result.privacy["raw_private_log_committed"] is True


def test_absolute_or_private_fixture_paths_are_rejected(tmp_path: Path) -> None:
    payload = _manifest_payload()
    payload["source"]["log_path"] = "/Users/example/private/Player.log"

    result = golden_replay.run_golden_replay(_write_manifest(tmp_path, payload))

    assert result.status == "fail"
    assert "missing_or_invalid_fixture_path" in result.failures
    assert result.fixture_path is None


def test_legacy_unclassified_manifest_replays_but_requires_review(tmp_path: Path) -> None:
    payload = _manifest_payload()
    payload["source"]["sanitization_status"] = "legacy_unclassified"

    result = golden_replay.run_golden_replay(_write_manifest(tmp_path, payload))

    assert result.status == "review"
    assert result.review_notes == ["legacy_unclassified_fixture_metadata"]
    assert result.privacy["review_required"] is True
    assert result.diffs == []


def test_forbidden_fixture_content_fails_without_printing_raw_secret(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(golden_replay, "PROJECT_ROOT", tmp_path)
    fixture_path = Path("fixtures/private_marker_slice.log")
    full_fixture_path = tmp_path / fixture_path
    full_fixture_path.parent.mkdir()
    full_fixture_path.write_text("token = placeholder-value\n", encoding="utf-8")
    payload = _manifest_payload()
    payload["fixture_id"] = "private_marker_fixture"
    payload["source"]["log_path"] = str(fixture_path)

    result = golden_replay.run_golden_replay(_write_manifest(tmp_path, payload))

    encoded = json.dumps(result.to_report_result(), sort_keys=True)
    assert result.status == "fail"
    assert result.failures == ["forbidden_fixture_content:api_key_assignment"]
    assert "placeholder-value" not in encoded


def test_cli_accepts_manifest_directory_and_writes_explicit_local_report(tmp_path: Path, capsys) -> None:
    out_path = tmp_path / "golden_replay_report.json"

    exit_code = golden_replay.main([str(FIXTURE_DIR), "--out", str(out_path)])

    captured = capsys.readouterr()
    report = json.loads(out_path.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert "Golden replay: pass (2 manifests, 2 pass, 0 degraded, 0 review, 0 diff, 0 fail)" in captured.out
    assert report["suite_status"] == "pass"
    assert report["summary"]["manifests_total"] == 2


def test_cli_returns_nonzero_for_review_status(tmp_path: Path, capsys) -> None:
    payload = _manifest_payload()
    payload["source"]["sanitization_status"] = "legacy_unclassified"

    exit_code = golden_replay.main([str(_write_manifest(tmp_path, payload))])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Golden replay: review" in captured.out


def test_cli_returns_nonzero_for_diff_status(tmp_path: Path, capsys) -> None:
    payload = _manifest_payload()
    payload["expected"]["final_reconciliation"]["match_winner_team"] = 2

    exit_code = golden_replay.main([str(_write_manifest(tmp_path, payload))])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Golden replay: diff" in captured.out


def test_cli_returns_nonzero_for_fail_status(tmp_path: Path, capsys) -> None:
    payload = _manifest_payload()
    payload["source"]["raw_private_log_committed"] = True

    exit_code = golden_replay.main([str(_write_manifest(tmp_path, payload))])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Golden replay: fail" in captured.out


def test_cli_requires_explicit_manifest_inputs() -> None:
    with pytest.raises(SystemExit) as exc_info:
        golden_replay.main([])

    assert exc_info.value.code == 2
