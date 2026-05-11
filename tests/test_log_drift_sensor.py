from __future__ import annotations

import json
from pathlib import Path

from mythic_edge_parser.app import log_drift_sensor


def _fixture_log_text() -> str:
    fixture_path = Path(__file__).resolve().parent / "fixtures" / "flush_timing_corpus_slice.log"
    lines = fixture_path.read_text(encoding="utf-8").splitlines()
    return "\n".join(line for line in lines if not line.startswith("#")) + "\n"


def test_build_player_log_drift_report_surfaces_unmatched_api_names(tmp_path: Path) -> None:
    source_log = tmp_path / "Player.log"
    source_log.write_text(_fixture_log_text(), encoding="utf-8")

    report = log_drift_sensor.build_player_log_drift_report(source_log)

    api_names = {item["api_name"] for item in report["top_unmatched_api_names"]}
    request_api_names = {item["api_name"] for item in report["top_unmatched_request_api_names"]}
    assert report["status"] == "review"
    assert report["entry_counts"]["unknown"] > 0
    assert "Client.SceneChange" in api_names
    assert "QuestGetQuests" in api_names
    assert "PeriodicRewardsGetStatus" in api_names
    assert "EventGetCoursesV2" in request_api_names


def test_write_player_log_drift_report_flags_new_unknown_families_against_baseline(tmp_path: Path) -> None:
    source_log = tmp_path / "Player.log"
    source_log.write_text(_fixture_log_text(), encoding="utf-8")
    baseline_path = tmp_path / "baseline.json"
    baseline_path.write_text(
        json.dumps(
            {
                "top_unknown_signatures": [{"signature": "QuestGetQuests", "count": 1}],
                "top_unmatched_api_names": [{"api_name": "QuestGetQuests", "count": 1}],
                "top_unmatched_request_api_names": [],
            }
        ),
        encoding="utf-8",
    )

    result = log_drift_sensor.write_player_log_drift_report(
        source_path=source_log,
        report_path=tmp_path / "report.json",
        baseline_path=baseline_path,
    )

    new_api_names = set(result.report["baseline_delta"]["new_unmatched_api_names"])
    new_request_api_names = set(result.report["baseline_delta"]["new_unmatched_request_api_names"])
    assert "Client.SceneChange" in new_api_names
    assert "PeriodicRewardsGetStatus" in new_api_names
    assert "EventGetCoursesV2" in new_request_api_names


def test_entry_signature_prefers_prefix_label_for_privacy() -> None:
    entry = log_drift_sensor.LogEntry(
        header="Unknown",  # type: ignore[arg-type]
        body="AuthPatch: Identity cached: PiercingSerenity#1234 (4QL72N6FVNAGXELJ7NPAKFJZGI)",
    )

    assert log_drift_sensor._entry_signature(entry) == "AuthPatch"
