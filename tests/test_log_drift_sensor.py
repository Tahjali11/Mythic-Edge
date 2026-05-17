from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mythic_edge_parser.app import log_drift_sensor

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
REPO_ROOT = Path(__file__).resolve().parents[1]
DRIFT_FIXTURE_ID = "player_log_drift_flush_timing_v1"
NORMALIZED_REPORT_FIELDS = [
    "object",
    "status",
    "entry_counts",
    "headers",
    "routed_event_kinds",
    "top_unknown_signatures",
    "top_unmatched_api_names",
    "top_unmatched_request_api_names",
    "baseline_delta",
]
FORBIDDEN_REFERENCE_KEYS = {
    "analyzed_at",
    "source_path",
    "report_path",
    "baseline_path",
}
REQUIRED_DRIFT_NOT_APPLICABLE_KEYS = {
    "raw_log_source_path",
    "source_log_session_id",
    "source_schema_snapshot_id",
    "sanitizer_tool_version",
    "evidence_ledger_fixture_id",
    "runtime_drift_report_path",
    "runtime_drift_baseline_path",
    "committed_drift_baseline_path",
    "refresh_baseline_command",
    "live_workbook_id",
    "deployed_apps_script_version",
    "webhook_url",
    "generated_card_data_version",
    "external_api_source",
    "runtime_status_artifact",
    "failed_post_artifact",
    "workbook_export_artifact",
}


def _fixture_log_text(fixture_path: Path | None = None) -> str:
    fixture_path = fixture_path or FIXTURE_DIR / "flush_timing_corpus_slice.log"
    lines = fixture_path.read_text(encoding="utf-8").splitlines()
    return "\n".join(line for line in lines if not line.startswith("#")) + "\n"


def _load_manifest_fixture(fixture_id: str) -> dict[str, Any]:
    manifest_path = FIXTURE_DIR / "golden_fixture_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    fixtures = manifest["fixtures"]
    matches = [entry for entry in fixtures if entry["fixture_id"] == fixture_id]
    assert len(matches) == 1
    return matches[0]


def _normalize_drift_report(report: dict[str, Any]) -> dict[str, Any]:
    return {field: report[field] for field in NORMALIZED_REPORT_FIELDS}


def _assert_forbidden_reference_keys_absent(payload: Any) -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            assert key not in FORBIDDEN_REFERENCE_KEYS
            _assert_forbidden_reference_keys_absent(value)
    elif isinstance(payload, list):
        for item in payload:
            _assert_forbidden_reference_keys_absent(item)


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


def test_drift_report_reference_matches_manifest_fixture(tmp_path: Path) -> None:
    fixture = _load_manifest_fixture(DRIFT_FIXTURE_ID)
    assert fixture["fixture_classes"] == [
        "sanitized_player_log_excerpt",
        "drift_report_expected_output",
        "report_only_reference",
    ]
    assert fixture["input_path"] == "tests/fixtures/flush_timing_corpus_slice.log"
    assert (
        fixture["expected_output_path"]
        == "tests/fixtures/player_log_drift_flush_timing_expected.json"
    )
    assert fixture["expected_output_kind"] == "normalized_drift_report_reference"
    assert fixture["input_transform"] == "strip_fixture_comment_lines_for_existing_test_compatibility"
    assert fixture["baseline_mode"] == "empty_in_memory_baseline"
    assert fixture["update_approval_required"] is True
    assert set(fixture["expected_output_fields"]) == set(NORMALIZED_REPORT_FIELDS)
    assert set(fixture["not_applicable"]) == REQUIRED_DRIFT_NOT_APPLICABLE_KEYS
    assert all(fixture["not_applicable"].values())

    input_path = REPO_ROOT / fixture["input_path"]
    expected_path = REPO_ROOT / fixture["expected_output_path"]
    expected_reference = json.loads(expected_path.read_text(encoding="utf-8"))

    source_log = tmp_path / "Player.log"
    source_log.write_text(_fixture_log_text(input_path), encoding="utf-8")
    actual_report = log_drift_sensor.build_player_log_drift_report(
        source_log,
        baseline_payload={},
    )
    actual_reference = {
        "object": "mythic_edge_player_log_drift_report_reference",
        "schema_version": 1,
        "fixture_id": DRIFT_FIXTURE_ID,
        "input_path": fixture["input_path"],
        "input_transform": fixture["input_transform"],
        "report_builder": "src.mythic_edge_parser.app.log_drift_sensor.build_player_log_drift_report",
        "baseline_mode": fixture["baseline_mode"],
        "normalized_report": _normalize_drift_report(actual_report),
    }

    _assert_forbidden_reference_keys_absent(expected_reference)
    expected_text = json.dumps(expected_reference, sort_keys=True)
    assert "C:\\" not in expected_text
    assert "\\Users\\" not in expected_text
    assert "Player.log" not in expected_text
    assert actual_reference == expected_reference


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
