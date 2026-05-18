from __future__ import annotations

import json
from pathlib import Path

from mythic_edge_parser.app import parser_diagnostics


def _write_log(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "Player.log"
    path.write_text(text, encoding="utf-8")
    return path


def _game_over_log() -> str:
    payload = {
        "greToClientEvent": {
            "greToClientMessages": [
                {
                    "type": "GREMessageType_GameStateMessage",
                    "msgId": 1,
                    "gameStateMessage": {
                        "gameInfo": {
                            "stage": "GameStage_GameOver",
                            "matchState": "MatchState_GameComplete",
                            "results": [
                                {
                                    "scope": "MatchScope_Game",
                                    "winningTeamId": 1,
                                    "result": "ResultType_WinLoss",
                                    "reason": "ResultReason_Game",
                                }
                            ],
                        }
                    },
                }
            ]
        }
    }
    return f"[UnityCrossThreadLogger]5/8/2026 1:02:03 PM greToClientEvent\n{json.dumps(payload)}\n"


def test_healthy_completed_game_fixture_report_returns_pass(tmp_path: Path) -> None:
    report = parser_diagnostics.build_parser_diagnostics_report(
        _write_log(tmp_path, _game_over_log()),
        profile="fixture",
    )

    assert report["object"] == "mythic_edge_parser_diagnostics_report"
    assert report["schema_version"] == "parser_diagnostics.v1"
    assert report["overall_status"] == "pass"
    assert report["summary"]["parser_status"] == "pass"
    assert report["summary"]["routed_entries"] == 1
    assert report["summary"]["unknown_entries"] == 0
    assert report["event_family_coverage"]["counts_by_kind"]["GameState"] == 1
    assert report["event_family_coverage"]["counts_by_kind"]["GameResult"] == 1
    assert report["final_reconciliation"]["status"] == "pass"
    assert report["transport_health"]["status"] == "unknown"


def test_unknown_signatures_produce_review_and_are_sanitized(tmp_path: Path) -> None:
    source_log = _write_log(
        tmp_path,
        _game_over_log()
        + "[MysteryHeader] https://script.google.com/macros/s/AKfycb-secret-token-value/exec?user=local\n",
    )

    report = parser_diagnostics.build_parser_diagnostics_report(source_log, profile="fixture")
    encoded = json.dumps(report, sort_keys=True)

    assert report["overall_status"] == "review"
    assert report["parser_health"]["status"] == "review"
    assert report["unknowns_and_degradation"]["status"] == "review"
    assert report["summary"]["unknown_entries"] == 1
    assert "AKfycb-secret-token-value" not in encoded
    assert "script.google.com" not in encoded


def test_truncation_events_produce_data_loss_review(tmp_path: Path) -> None:
    source_log = _write_log(
        tmp_path,
        "[Message summarized - GREMessageType_GameStateMessage payload omitted]\n"
        "GameObject Count: 4\n"
        "Annotation Count: 2\n",
    )

    report = parser_diagnostics.build_parser_diagnostics_report(source_log, profile="fixture")

    assert report["overall_status"] == "review"
    assert report["summary"]["truncation_events"] == 1
    assert report["truncation_and_data_loss"]["status"] == "review"
    assert report["truncation_and_data_loss"]["data_loss_events"] == [
        {
            "event_kind": "Truncation",
            "type": "game_state_message_truncation",
            "data_loss": True,
            "recoverable": False,
            "affected_event_family": "GameState",
            "affected_message_type": "GREMessageType_GameStateMessage",
            "game_object_count": 4,
            "annotation_count": 2,
            "drift_flag": "missing_expected_payload_path",
            "value_source": "observed",
            "confidence": "high",
            "finality": "live",
            "raw_bytes_hash": report["truncation_and_data_loss"]["data_loss_events"][0]["raw_bytes_hash"],
        }
    ]
    assert "missing_expected_payload_path" in report["unknowns_and_degradation"]["drift_flags"]


def test_unreadable_source_log_produces_fail(tmp_path: Path) -> None:
    report = parser_diagnostics.build_parser_diagnostics_report(tmp_path / "missing.log", profile="fixture")

    assert report["overall_status"] == "fail"
    assert report["parser_health"]["status"] == "fail"
    assert report["parser_health"]["reasons"] == ["source_log_unreadable"]
    assert report["source"]["source_path_redacted"] == "missing.log"


def test_webhook_failure_is_transport_review_not_parser_failure(tmp_path: Path) -> None:
    report = parser_diagnostics.build_parser_diagnostics_report(
        _write_log(tmp_path, _game_over_log()),
        profile="fixture",
        runtime_status={
            "webhook_successes": 1,
            "webhook_failures": 2,
            "last_webhook_error": "POST failed for https://script.google.com/macros/s/AKfycb-secret/exec",
        },
    )
    encoded = json.dumps(report, sort_keys=True)

    assert report["overall_status"] == "review"
    assert report["parser_health"]["status"] == "pass"
    assert report["transport_health"]["status"] == "review"
    assert report["transport_health"]["webhook_successes"] == 1
    assert report["transport_health"]["webhook_failures"] == 2
    assert "AKfycb-secret" not in encoded
    assert "https://script.google.com/.../exec" in encoded


def test_missing_optional_runtime_status_is_unknown_not_parser_failure(tmp_path: Path) -> None:
    report = parser_diagnostics.build_parser_diagnostics_report(
        _write_log(tmp_path, _game_over_log()),
        profile="fixture",
    )

    assert report["overall_status"] == "pass"
    assert report["parser_health"]["status"] == "pass"
    assert report["transport_health"]["status"] == "unknown"
    assert report["transport_health"]["notes"] == ["Optional runtime status was not supplied."]


def test_report_redacts_local_paths_and_excludes_raw_log_lines(tmp_path: Path) -> None:
    source_log = _write_log(tmp_path, _game_over_log())

    report = parser_diagnostics.build_parser_diagnostics_report(source_log, profile="fixture")
    encoded = json.dumps(report, sort_keys=True)

    assert str(tmp_path) not in encoded
    assert report["source"]["log_display_name"] == "Player.log"
    assert report["privacy"] == {
        "redaction_applied": True,
        "raw_log_lines_included": False,
        "raw_payloads_included": False,
        "webhook_urls_included": False,
    }
    assert "greToClientEvent" not in encoded
    assert "winningTeamId" not in encoded


def test_report_schema_has_stable_v1_top_level_keys(tmp_path: Path) -> None:
    report = parser_diagnostics.build_parser_diagnostics_report(
        _write_log(tmp_path, _game_over_log()),
        profile="fixture",
    )

    assert list(report) == [
        "object",
        "schema_version",
        "generated_at",
        "profile",
        "overall_status",
        "summary",
        "source",
        "privacy",
        "parser_health",
        "event_family_coverage",
        "truncation_and_data_loss",
        "unknowns_and_degradation",
        "final_reconciliation",
        "transport_health",
        "workbook_and_appscript",
        "manual_checklist",
        "validation_evidence",
    ]


def test_write_report_handles_malformed_baseline_as_review(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    baseline_path.write_text("{not-json}", encoding="utf-8")
    out_path = tmp_path / "parser_diagnostics_latest.json"

    result = parser_diagnostics.write_parser_diagnostics_report(
        source_log=_write_log(tmp_path, _game_over_log()),
        report_path=out_path,
        profile="fixture",
        drift_baseline_path=baseline_path,
    )

    assert result.report_path == out_path
    assert out_path.exists()
    assert result.report["overall_status"] == "review"
    assert "malformed_drift_baseline_json" in result.report["unknowns_and_degradation"]["drift_flags"]


def test_cli_writes_local_report_and_prints_sanitized_summary(tmp_path: Path, capsys) -> None:
    out_path = tmp_path / "status" / "parser_diagnostics_latest.json"

    exit_code = parser_diagnostics.main(
        [
            str(_write_log(tmp_path, _game_over_log())),
            "--profile",
            "fixture",
            "--out",
            str(out_path),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert out_path.exists()
    assert "Parser diagnostics: pass (1 routed / 0 unknown, 0 truncation)" in captured.out
    assert str(tmp_path) not in captured.out
