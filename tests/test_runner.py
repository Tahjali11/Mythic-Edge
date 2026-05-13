from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from mythic_edge_parser.app import runner


def test_display_path_returns_empty_for_none() -> None:
    assert runner._display_path(None) == ""


def test_display_path_preserves_project_relative_paths(monkeypatch, tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_path = project_root / "data" / "status" / "manasight_status_latest.json"
    monkeypatch.setattr(runner, "PROJECT_ROOT", project_root)

    assert runner._display_path(project_path) == str(Path("data") / "status" / "manasight_status_latest.json")


def test_display_path_uses_basename_for_non_project_posix_paths(monkeypatch, tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    outside_path = tmp_path / "outside" / "Player.log"
    monkeypatch.setattr(runner, "PROJECT_ROOT", project_root)

    assert runner._display_path(outside_path) == "Player.log"


def test_display_path_uses_basename_for_windows_style_paths_on_posix(monkeypatch, tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    windows_path = Path(r"C:\Users\Tahj Blow\AppData\LocalLow\Wizards Of The Coast\MTGA\Player.log")
    monkeypatch.setattr(runner, "PROJECT_ROOT", project_root)

    assert runner._display_path(windows_path) == "Player.log"


def test_display_path_does_not_treat_windows_drive_path_as_project_relative(monkeypatch) -> None:
    windows_path = Path(r"C:\Users\Tahj Blow\AppData\LocalLow\Wizards Of The Coast\MTGA\Player.log")
    monkeypatch.setattr(runner, "PROJECT_ROOT", Path.cwd())

    assert runner._display_path(windows_path) == "Player.log"


def test_startup_status_fields_sanitize_paths_and_webhook(monkeypatch, tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    status_path = project_root / "data" / "status" / "manasight_status_latest.json"
    match_logs_root = project_root / "data" / "match_logs"

    monkeypatch.setattr(runner, "PROJECT_ROOT", project_root)
    monkeypatch.setattr(
        runner,
        "LOG_PATH",
        Path(r"C:\Users\Tahj Blow\AppData\LocalLow\Wizards Of The Coast\MTGA\Player.log"),
    )
    monkeypatch.setattr(runner, "MATCH_LOGS_ROOT", match_logs_root)
    monkeypatch.setattr(
        runner,
        "WEBHOOK_URL",
        "https://script.google.com/macros/s/AKfycb-secret-value/exec?user=tahj",
    )
    monkeypatch.setattr(runner, "current_status_path", lambda: status_path)

    payload = runner._startup_status_fields()

    assert payload["log_path"] == "Player.log"
    assert payload["match_logs_root"] == str(Path("data") / "match_logs")
    assert payload["status_file_path"] == str(Path("data") / "status" / "manasight_status_latest.json")
    assert payload["webhook_target"] == "https://script.google.com/.../exec"


def test_sheet_posting_enabled_treats_gamestate_flag_as_transport_output(monkeypatch) -> None:
    monkeypatch.setattr(runner, "POST_RAW_EVENT_ROWS", False)
    monkeypatch.setattr(runner, "POST_GAMESTATE_ROWS", True)
    monkeypatch.setattr(runner, "POST_GAME_LOG_ROWS", False)
    monkeypatch.setattr(runner, "POST_MATCH_SUMMARY_ROWS", False)
    monkeypatch.setattr(runner, "POST_MATCH_LOG_ROWS", False)
    monkeypatch.setattr(runner, "POST_ACTION_LOG_ROWS", False)
    monkeypatch.setattr(runner, "POST_DECK_SNAPSHOT_ROWS", False)
    monkeypatch.setattr(runner, "POST_COLLECTION_SNAPSHOT_ROWS", False)
    monkeypatch.setattr(runner, "POST_PARSER_STATUS_ROWS", False)
    monkeypatch.setattr(runner, "POST_CARD_PERFORMANCE_ROWS", False)

    assert runner._sheet_posting_enabled() is True


def test_post_sheet_debug_rows_allows_gamestate_only_transport(monkeypatch) -> None:
    submitted_rows: list[dict[str, object]] = []
    event = SimpleNamespace(kind="GameState", payload={})
    game_state_row = {"event_family": "GameState", "scope": "Turn", "turn_number": 2}

    monkeypatch.setattr(runner, "POST_RAW_EVENT_ROWS", False)
    monkeypatch.setattr(runner, "POST_GAMESTATE_ROWS", True)
    monkeypatch.setattr(runner, "to_sheet_rows", lambda _event: [game_state_row])
    monkeypatch.setattr(
        runner,
        "submit_row_to_google_sheets",
        lambda row, **_kwargs: submitted_rows.append(dict(row)) or True,
    )

    posted = runner._post_sheet_debug_rows(event)

    assert posted == 1
    assert submitted_rows == [game_state_row]


def test_post_sheet_debug_rows_skips_non_gamestate_when_only_gamestate_flag_is_enabled(monkeypatch) -> None:
    submitted_rows: list[dict[str, object]] = []
    event = SimpleNamespace(kind="MatchState", payload={"type": "match_started"})

    monkeypatch.setattr(runner, "POST_RAW_EVENT_ROWS", False)
    monkeypatch.setattr(runner, "POST_GAMESTATE_ROWS", True)
    monkeypatch.setattr(runner, "to_sheet_rows", lambda _event: [{"event_family": "MatchState"}])
    monkeypatch.setattr(
        runner,
        "submit_row_to_google_sheets",
        lambda row, **_kwargs: submitted_rows.append(dict(row)) or True,
    )

    posted = runner._post_sheet_debug_rows(event)

    assert posted == 0
    assert submitted_rows == []
