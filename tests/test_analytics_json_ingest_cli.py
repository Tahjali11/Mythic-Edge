from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from mythic_edge_parser.app import analytics_json_ingest as cli


def _base_replay(label: str = "analytics_json_ingest_cli_v1", match_id: str = "match:cli:001") -> dict[str, object]:
    return {
        "source_kind": "sanitized_golden_replay",
        "source_artifact_label": label,
        "parser_commit": "test-parser-commit",
        "parser_version": "test-parser-version",
        "generated_at": "2026-05-29T15:00:00+00:00",
        "match_log_rows": [
            {
                "event_family": "MatchLogRow",
                "event_type": "match_log_row",
                "scope": "Match",
                "match_id": match_id,
                "timestamp": "2026-05-29T15:30:00+00:00",
                "MTGA Match ID": match_id,
                "Match Win?": "W",
                "Match Win Flag": 1,
                "Games Won": 1,
                "Games Lost": 0,
                "Total Games": 1,
                "Game Win %": 1.0,
                "MTGA Format": "Constructed",
                "MTGA Event ID": "CLI_Event",
                "MTGA Queue Type": "Best of 1",
                "MGTA Start Time": "2026-05-29T15:00:00+00:00",
                "MTGA End Time": "2026-05-29T15:30:00+00:00",
                "MTGA Sync Status": "Final",
            },
        ],
        "game_log_rows": [
            {
                "event_family": "GameLogRow",
                "event_type": "game_log_row",
                "scope": "Game",
                "match_id": match_id,
                "timestamp": "2026-05-29T15:30:00+00:00",
                "MTGA Match ID": match_id,
                "Game Number": 1,
                "Pre / Postboard": "Preboard",
                "Play / Draw": "Play",
                "Mulligans": 0,
                "Opening Hand Size": 7,
                "Opening Hand": "Forest; Island",
                "Mulliganed Away": "",
                "Game Result": "W",
                "Turn Count": 6,
                "Game Duration": 900,
                "MTGA Format": "Constructed",
                "MTGA Event ID": "CLI_Event",
                "MTGA Queue Type": "Best of 1",
            },
        ],
    }


def _write_json(path: Path, payload: object) -> Path:
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    return path


def _summary(stdout: str) -> dict[str, object]:
    return json.loads(stdout)


def _count(database_path: Path, table_name: str) -> int:
    connection = sqlite3.connect(database_path)
    try:
        return int(connection.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0])
    finally:
        connection.close()


def test_cli_constants_and_arg_parser_are_public() -> None:
    parser = cli.build_arg_parser()

    args = parser.parse_args(["--input", "replay.json", "--database", "analytics.sqlite3", "--print-summary"])

    assert cli.ANALYTICS_JSON_INGEST_CLI_SCHEMA_VERSION == "analytics_json_ingest_cli.v1"
    assert cli.ANALYTICS_JSON_INGEST_MAX_BYTES == 10_485_760
    assert cli.SUPPORTED_ANALYTICS_JSON_SHAPES == ("parser_normalized_replay",)
    assert "v_opening_hand_cards" in cli.REQUIRED_ANALYTICS_VIEWS
    assert args.input == ["replay.json"]
    assert args.database == "analytics.sqlite3"
    assert args.print_summary is True


def test_main_returns_usage_code_for_argparse_errors(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = cli.main([])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "usage:" in captured.err


def test_single_parser_normalized_replay_file_ingests_and_prints_summary(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_path = _write_json(tmp_path / "supported.json", _base_replay())
    database_path = tmp_path / "analytics.sqlite3"

    exit_code = cli.main(["--input", str(input_path), "--database", str(database_path), "--print-summary"])

    captured = capsys.readouterr()
    summary = _summary(captured.out)
    assert exit_code == 0
    assert captured.err == ""
    assert summary["ok"] is True
    assert summary["object"] == "mythic_edge_analytics_json_ingest_summary"
    assert summary["schema_version"] == "analytics_json_ingest_cli.v1"
    assert summary["database_label"] == "analytics.sqlite3"
    assert summary["files_seen"] == 1
    assert summary["files_supported"] == 1
    assert summary["files_ingested"] == 1
    assert summary["files_unsupported"] == 0
    assert summary["unsupported_files"] == []
    assert summary["row_counts"]["matches"] == 1
    assert summary["row_counts"]["games"] == 1
    assert summary["row_counts"]["opening_hand_cards"] == 2
    assert summary["warnings"] == []
    assert summary["skipped"] == {}
    assert set(summary["view_readiness"]) == set(cli.REQUIRED_ANALYTICS_VIEWS)
    assert summary["view_readiness"]["v_opening_hand_cards"]["status"] == "queryable"
    assert "/Users/" not in captured.out
    assert str(tmp_path) not in captured.out
    assert database_path.exists()


def test_directory_and_repeated_inputs_ingest_in_deterministic_order_with_duplicate_warning(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_dir = tmp_path / "json"
    input_dir.mkdir()
    first = _write_json(input_dir / "a.json", _base_replay("cli_dir_a", "match:cli:a"))
    _write_json(input_dir / "b.json", _base_replay("cli_dir_b", "match:cli:b"))
    database_path = tmp_path / "analytics.sqlite3"

    exit_code = cli.main(
        [
            "--input",
            str(input_dir),
            "--input",
            str(first),
            "--database",
            str(database_path),
            "--print-summary",
        ]
    )

    captured = capsys.readouterr()
    summary = _summary(captured.out)
    assert exit_code == 0
    assert summary["files_seen"] == 2
    assert summary["files_ingested"] == 2
    assert [run["file_label"] for run in summary["ingest_runs"]] == ["a.json", "b.json"]
    assert summary["row_counts"]["matches"] == 2
    assert summary["warnings"] == ["duplicate input skipped: a.json"]


def test_repeat_ingest_is_idempotent(tmp_path: Path) -> None:
    input_path = _write_json(tmp_path / "supported.json", _base_replay())
    database_path = tmp_path / "analytics.sqlite3"
    args = ["--input", str(input_path), "--database", str(database_path), "--print-summary"]

    first = cli.main(args)
    second = cli.main(args)

    assert first == 0
    assert second == 0
    assert _count(database_path, "ingest_runs") == 1
    assert _count(database_path, "matches") == 1
    assert _count(database_path, "games") == 1


def test_unsupported_json_shape_exits_failure_and_creates_no_database(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_path = _write_json(tmp_path / "unsupported.json", {"match_log_row": {}, "game_log_rows": []})
    database_path = tmp_path / "analytics.sqlite3"

    exit_code = cli.main(["--input", str(input_path), "--database", str(database_path), "--print-summary"])

    captured = capsys.readouterr()
    summary = _summary(captured.out)
    assert exit_code == 1
    assert "unsupported.json" in captured.err
    assert str(tmp_path) not in captured.err
    assert summary["ok"] is False
    assert summary["database_label"] == "analytics.sqlite3"
    assert summary["files_seen"] == 1
    assert summary["files_unsupported"] == 1
    assert summary["unsupported_files"][0]["file_label"] == "unsupported.json"
    assert not database_path.exists()


def test_unsafe_source_artifact_label_exits_failure_without_database(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    replay = _base_replay()
    replay["source_artifact_label"] = "Z:" + "\\private\\Player.log"
    input_path = _write_json(tmp_path / "unsafe.json", replay)
    database_path = tmp_path / "analytics.sqlite3"

    exit_code = cli.main(["--input", str(input_path), "--database", str(database_path), "--print-summary"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "unsafe.json" in captured.err
    assert "Player.log" not in captured.out
    assert "Z:" not in captured.out
    assert not database_path.exists()


def test_invalid_json_and_top_level_arrays_are_rejected(tmp_path: Path) -> None:
    invalid_json = tmp_path / "invalid.json"
    invalid_json.write_text("{not json", encoding="utf-8")
    array_json = _write_json(tmp_path / "array.json", [])
    database_path = tmp_path / "analytics.sqlite3"

    assert cli.main(["--input", str(invalid_json), "--database", str(database_path)]) == 1
    assert cli.main(["--input", str(array_json), "--database", str(database_path)]) == 1
    assert not database_path.exists()


def test_oversize_file_is_rejected_without_echoing_payload(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli, "ANALYTICS_JSON_INGEST_MAX_BYTES", 8)
    oversize = tmp_path / "oversize.json"
    oversize.write_text('{"secret":"do-not-echo"}', encoding="utf-8")
    database_path = tmp_path / "analytics.sqlite3"

    assert cli.main(["--input", str(oversize), "--database", str(database_path), "--print-summary"]) == 1
    assert not database_path.exists()


def test_jsonl_and_player_log_style_inputs_are_rejected(tmp_path: Path) -> None:
    jsonl = tmp_path / "events.jsonl"
    jsonl.write_text('{"source_kind":"saved_event_replay"}\n', encoding="utf-8")
    player_log = tmp_path / "Player.log"
    player_log.write_text("sanitized non-json local log placeholder", encoding="utf-8")
    database_path = tmp_path / "analytics.sqlite3"

    assert cli.main(["--input", str(jsonl), "--database", str(database_path)]) == 1
    assert cli.main(["--input", str(player_log), "--database", str(database_path)]) == 1
    assert not database_path.exists()


def test_database_path_pointing_to_directory_is_rejected_after_preflight(tmp_path: Path) -> None:
    input_path = _write_json(tmp_path / "supported.json", _base_replay())

    assert cli.main(["--input", str(input_path), "--database", str(tmp_path)]) == 1


def test_fail_on_warning_converts_duplicate_warning_to_exit_one(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    input_path = _write_json(tmp_path / "supported.json", _base_replay())
    database_path = tmp_path / "analytics.sqlite3"

    exit_code = cli.main(
        [
            "--input",
            str(input_path),
            "--input",
            str(input_path),
            "--database",
            str(database_path),
            "--print-summary",
            "--fail-on-warning",
        ]
    )

    summary = _summary(capsys.readouterr().out)
    assert exit_code == 1
    assert summary["ok"] is False
    assert summary["status"] == "warning"
    assert summary["warnings"] == ["duplicate input skipped: supported.json"]
    assert database_path.exists()


def test_no_view_check_marks_required_views_not_checked(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    input_path = _write_json(tmp_path / "supported.json", _base_replay())
    database_path = tmp_path / "analytics.sqlite3"

    exit_code = cli.main(
        [
            "--input",
            str(input_path),
            "--database",
            str(database_path),
            "--print-summary",
            "--no-check-views",
        ]
    )

    summary = _summary(capsys.readouterr().out)
    assert exit_code == 0
    assert {view["status"] for view in summary["view_readiness"].values()} == {"not_checked"}
