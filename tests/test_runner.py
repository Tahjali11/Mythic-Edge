from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

from mythic_edge_parser.app import runner


def _synthetic_windows_player_log() -> Path:
    return Path(
        "C:"
        + "\\"
        + "Users"
        + "\\"
        + "Arena Player"
        + r"\AppData\LocalLow\Wizards Of The Coast\MTGA\Player.log"
    )


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
    windows_path = _synthetic_windows_player_log()
    monkeypatch.setattr(runner, "PROJECT_ROOT", project_root)

    assert runner._display_path(windows_path) == "Player.log"


def test_display_path_does_not_treat_windows_drive_path_as_project_relative(monkeypatch) -> None:
    windows_path = _synthetic_windows_player_log()
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
        _synthetic_windows_player_log(),
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


class _FakeLogger:
    def __init__(self, calls: list[str] | None = None) -> None:
        self.calls = calls if calls is not None else []

    def info(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("logger.info")

    def debug(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("logger.debug")

    def warning(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("logger.warning")

    def error(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("logger.error")

    def exception(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("logger.exception")


class _FakeSubscriber:
    def __init__(self, events: list[object | None]) -> None:
        self._events = iter(events)

    async def recv(self) -> object | None:
        return next(self._events)


class _FakeStream:
    def __init__(self, calls: list[str]) -> None:
        self.calls = calls

    async def shutdown(self) -> None:
        self.calls.append("stream.shutdown")


def _event(kind: str = "MatchState", payload: dict[str, object] | None = None) -> SimpleNamespace:
    return SimpleNamespace(
        kind=kind,
        payload=payload or {},
        metadata=SimpleNamespace(timestamp=datetime(2026, 5, 14, tzinfo=UTC), raw_bytes_hash="hash"),
    )


def _patch_main_harness(
    monkeypatch,
    tmp_path: Path,
    events: list[object | None],
    calls: list[str],
) -> None:
    log_path = tmp_path / "Player.log"
    log_path.write_text("", encoding="utf-8")

    monkeypatch.setattr(runner, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(runner, "LOG_PATH", log_path)
    monkeypatch.setattr(runner, "MATCH_LOGS_ROOT", tmp_path / "match_logs")
    monkeypatch.setattr(runner, "WEBHOOK_URL", "")
    monkeypatch.setattr(runner, "current_runtime_log_path", lambda: tmp_path / "runtime.log")
    monkeypatch.setattr(runner, "current_status_path", lambda: tmp_path / "status.json")
    monkeypatch.setattr(runner, "setup_runtime_logging", lambda: calls.append("setup_runtime_logging"))
    monkeypatch.setattr(runner, "get_logger", lambda _name: _FakeLogger(calls))
    monkeypatch.setattr(
        runner,
        "update_runtime_status",
        lambda **kwargs: calls.append(f"status:{kwargs.get('status', '')}"),
    )
    monkeypatch.setattr(runner, "_startup_issues", lambda: ([], []))
    monkeypatch.setattr(runner, "bootstrap_gameplay_actions", lambda: calls.append("bootstrap_gameplay_actions"))
    monkeypatch.setattr(runner, "_sheet_posting_enabled", lambda: False)
    monkeypatch.setattr(runner, "start_webhook_dispatcher", lambda: calls.append("start_webhook_dispatcher"))
    monkeypatch.setattr(runner, "start_analytics_sidecar", lambda: calls.append("start_analytics_sidecar"))
    monkeypatch.setattr(runner, "start_status_api_server", lambda: None)
    monkeypatch.setattr(runner, "daily_log_label", lambda _event_dt: "2026-05-14")

    async def fake_start(_path: Path) -> tuple[_FakeStream, _FakeSubscriber]:
        calls.append("stream.start")
        return _FakeStream(calls), _FakeSubscriber(events)

    monkeypatch.setattr(runner, "MtgaEventStream", SimpleNamespace(start=fake_start))


def _patch_shutdown_hooks(monkeypatch, calls: list[str]) -> None:
    def drain_webhook_results(*, max_items: int = 200) -> None:
        calls.append(f"drain:{max_items}")

    monkeypatch.setattr(runner, "drain_webhook_results", drain_webhook_results)
    monkeypatch.setattr(
        runner,
        "stop_webhook_dispatcher",
        lambda *, wait_for_queue=True: calls.append(f"stop_webhook:{wait_for_queue}"),
    )
    monkeypatch.setattr(
        runner,
        "stop_analytics_sidecar",
        lambda *, wait_for_queue=True: calls.append(f"stop_analytics:{wait_for_queue}"),
    )
    monkeypatch.setattr(runner, "stop_status_api_server", lambda: calls.append("stop_status_api"))


def test_main_loop_preserves_kept_event_side_effect_order(monkeypatch, tmp_path: Path) -> None:
    calls: list[str] = []
    event = _event()

    _patch_main_harness(monkeypatch, tmp_path, [event, None], calls)
    _patch_shutdown_hooks(monkeypatch, calls)
    monkeypatch.setattr(runner, "_CONTEXT", {"current_match_id": "match-1", "current_game_number": 1})
    monkeypatch.setattr(runner, "_update_match_summary", lambda _event: calls.append("state"))
    monkeypatch.setattr(runner, "mark_event_seen", lambda *_args, **_kwargs: calls.append("diagnostics"))
    monkeypatch.setattr(runner, "observe_gameplay_event", lambda _event: calls.append("gameplay"))
    monkeypatch.setattr(runner, "include_event", lambda _event: calls.append("include") or True)
    monkeypatch.setattr(
        runner,
        "submit_analytics_event",
        lambda _event, *, include_in_timeline: calls.append(f"analytics:{include_in_timeline}"),
    )
    monkeypatch.setattr(
        runner,
        "to_serializable",
        lambda _event: calls.append("serializable") or {"kind": "MatchState"},
    )
    monkeypatch.setattr(
        runner,
        "_event_datetime",
        lambda _event: calls.append("event_datetime") or datetime(2026, 5, 14, tzinfo=UTC),
    )
    monkeypatch.setattr(runner, "append_local_jsonl", lambda *_args: calls.append("archive"))
    monkeypatch.setattr(runner, "_maybe_record_submitted_deck", lambda *_args: calls.append("submitted_deck"))
    monkeypatch.setattr(runner, "_post_sheet_debug_rows", lambda _event: calls.append("debug_rows") or 0)
    monkeypatch.setattr(runner, "_post_game_log_rows", lambda _logger: calls.append("game_log_rows"))
    monkeypatch.setattr(runner, "_post_match_summary_row", lambda: calls.append("match_summary_row"))
    monkeypatch.setattr(runner, "_post_match_log_row", lambda _logger: calls.append("match_log_row"))
    monkeypatch.setattr(runner, "summarize", lambda _event: calls.append("summarize") or "summary")

    asyncio.run(runner.main())

    expected_order = [
        "state",
        "diagnostics",
        "gameplay",
        "include",
        "analytics:True",
        "serializable",
        "event_datetime",
        "archive",
        "submitted_deck",
        "debug_rows",
        "game_log_rows",
        "match_summary_row",
        "match_log_row",
        "summarize",
    ]
    positions = [calls.index(item) for item in expected_order]
    assert positions == sorted(positions)


def test_main_loop_dropped_event_updates_all_event_surfaces_only(monkeypatch, tmp_path: Path) -> None:
    calls: list[str] = []
    event = _event()

    _patch_main_harness(monkeypatch, tmp_path, [event, None], calls)
    _patch_shutdown_hooks(monkeypatch, calls)
    monkeypatch.setattr(runner, "_CONTEXT", {"current_match_id": "match-1", "current_game_number": 1})
    monkeypatch.setattr(runner, "_update_match_summary", lambda _event: calls.append("state"))
    monkeypatch.setattr(runner, "mark_event_seen", lambda *_args, **_kwargs: calls.append("diagnostics"))
    monkeypatch.setattr(runner, "observe_gameplay_event", lambda _event: calls.append("gameplay"))
    monkeypatch.setattr(runner, "include_event", lambda _event: calls.append("include") or False)
    monkeypatch.setattr(
        runner,
        "submit_analytics_event",
        lambda _event, *, include_in_timeline: calls.append(f"analytics:{include_in_timeline}"),
    )
    monkeypatch.setattr(runner, "append_local_jsonl", lambda *_args: calls.append("archive"))
    monkeypatch.setattr(runner, "_post_sheet_debug_rows", lambda _event: calls.append("debug_rows") or 0)
    monkeypatch.setattr(runner, "_post_game_log_rows", lambda _logger: calls.append("game_log_rows"))
    monkeypatch.setattr(runner, "_post_match_summary_row", lambda: calls.append("match_summary_row"))
    monkeypatch.setattr(runner, "_post_match_log_row", lambda _logger: calls.append("match_log_row"))

    asyncio.run(runner.main())

    assert "state" in calls
    assert "diagnostics" in calls
    assert "gameplay" in calls
    assert "include" in calls
    assert "analytics:False" in calls
    assert "archive" not in calls
    assert "debug_rows" not in calls
    assert "game_log_rows" not in calls
    assert "match_summary_row" not in calls
    assert "match_log_row" not in calls


def test_main_loop_records_runner_failure_and_continues(monkeypatch, tmp_path: Path) -> None:
    calls: list[str] = []
    bad_event = _event("MatchState", {"id": "bad"})
    good_event = _event("MatchState", {"id": "good"})

    _patch_main_harness(monkeypatch, tmp_path, [bad_event, good_event, None], calls)
    _patch_shutdown_hooks(monkeypatch, calls)
    monkeypatch.setattr(runner, "_CONTEXT", {"current_match_id": "match-1", "current_game_number": 1})
    monkeypatch.setattr(runner, "_update_match_summary", lambda event: calls.append(f"state:{event.payload['id']}"))
    monkeypatch.setattr(runner, "mark_event_seen", lambda *_args, **_kwargs: calls.append("diagnostics"))
    monkeypatch.setattr(runner, "observe_gameplay_event", lambda _event: calls.append("gameplay"))
    monkeypatch.setattr(runner, "include_event", lambda _event: True)
    monkeypatch.setattr(runner, "submit_analytics_event", lambda *_args, **_kwargs: calls.append("analytics"))

    def to_serializable(event: object) -> dict[str, object]:
        if getattr(event, "payload", {}).get("id") == "bad":
            raise ValueError("bad event")
        return {"id": "good"}

    failures: list[tuple[object, str, str]] = []
    monkeypatch.setattr(runner, "to_serializable", to_serializable)
    monkeypatch.setattr(runner, "_event_datetime", lambda _event: datetime(2026, 5, 14, tzinfo=UTC))
    monkeypatch.setattr(runner, "append_local_jsonl", lambda row, _event_dt: calls.append(f"archive:{row['id']}"))
    monkeypatch.setattr(runner, "_maybe_record_submitted_deck", lambda *_args: None)
    monkeypatch.setattr(runner, "_post_sheet_debug_rows", lambda _event: 0)
    monkeypatch.setattr(runner, "_post_game_log_rows", lambda _logger: None)
    monkeypatch.setattr(runner, "_post_match_summary_row", lambda: None)
    monkeypatch.setattr(runner, "_post_match_log_row", lambda _logger: None)
    monkeypatch.setattr(runner, "summarize", lambda _event: "summary")
    monkeypatch.setattr(
        runner,
        "record_event_failure",
        lambda event, exc, *, stage: failures.append((event, str(exc), stage)) or tmp_path / "failure.jsonl",
    )

    asyncio.run(runner.main())

    assert failures == [(bad_event, "bad event", "runner")]
    assert "state:good" in calls
    assert "archive:good" in calls


def test_main_shutdown_order_after_stream_exists(monkeypatch, tmp_path: Path) -> None:
    calls: list[str] = []

    _patch_main_harness(monkeypatch, tmp_path, [None], calls)
    _patch_shutdown_hooks(monkeypatch, calls)

    asyncio.run(runner.main())

    assert calls[-7:] == [
        "drain:5000",
        "stop_webhook:True",
        "drain:5000",
        "stop_analytics:False",
        "status:stopped",
        "stop_status_api",
        "stream.shutdown",
    ]
    assert calls[-8] == "drain:200"
    assert calls.index("stop_status_api") < calls.index("stream.shutdown")


def test_main_records_status_api_success_fields(monkeypatch, tmp_path: Path) -> None:
    status_updates: list[dict[str, object]] = []
    calls: list[str] = []

    _patch_main_harness(monkeypatch, tmp_path, [None], calls)
    _patch_shutdown_hooks(monkeypatch, calls)
    monkeypatch.setattr(runner, "update_runtime_status", lambda **kwargs: status_updates.append(dict(kwargs)))
    monkeypatch.setattr(
        runner,
        "start_status_api_server",
        lambda: {"base_url": "http://127.0.0.1:1234", "host": "127.0.0.1", "port": 1234},
    )

    asyncio.run(runner.main())

    assert {
        "local_status_api_url": "http://127.0.0.1:1234",
        "local_status_api_host": "127.0.0.1",
        "local_status_api_port": 1234,
        "local_status_api_enabled": True,
    } in status_updates


def test_main_records_status_api_startup_failure(monkeypatch, tmp_path: Path) -> None:
    status_updates: list[dict[str, object]] = []
    calls: list[str] = []

    _patch_main_harness(monkeypatch, tmp_path, [None], calls)
    _patch_shutdown_hooks(monkeypatch, calls)
    monkeypatch.setattr(runner, "update_runtime_status", lambda **kwargs: status_updates.append(dict(kwargs)))

    def fail_status_api() -> None:
        raise RuntimeError("port unavailable")

    monkeypatch.setattr(runner, "start_status_api_server", fail_status_api)

    asyncio.run(runner.main())

    assert {"local_status_api_enabled": False, "local_status_api_error": "port unavailable"} in status_updates


def test_startup_issues_classifies_log_webhook_and_tier_conditions(monkeypatch, tmp_path: Path) -> None:
    missing_log = tmp_path / "missing" / "Player.log"
    tier_path = tmp_path / "missing-tier.json"

    monkeypatch.setattr(runner, "LOG_PATH", missing_log)
    monkeypatch.setattr(runner, "WEBHOOK_URL", "")
    monkeypatch.setattr(runner, "SYNC_TIER_BUCKETS", True)
    monkeypatch.setattr(runner, "TIER_NORMALIZATION_PATH", tier_path)
    monkeypatch.setattr(runner, "POST_RAW_EVENT_ROWS", False)
    monkeypatch.setattr(runner, "POST_GAMESTATE_ROWS", False)
    monkeypatch.setattr(runner, "POST_GAME_LOG_ROWS", True)
    monkeypatch.setattr(runner, "POST_MATCH_SUMMARY_ROWS", False)
    monkeypatch.setattr(runner, "POST_MATCH_LOG_ROWS", False)
    monkeypatch.setattr(runner, "POST_ACTION_LOG_ROWS", False)
    monkeypatch.setattr(runner, "POST_DECK_SNAPSHOT_ROWS", False)
    monkeypatch.setattr(runner, "POST_COLLECTION_SNAPSHOT_ROWS", False)
    monkeypatch.setattr(runner, "POST_PARSER_STATUS_ROWS", False)
    monkeypatch.setattr(runner, "POST_CARD_PERFORMANCE_ROWS", False)

    warnings, errors = runner._startup_issues()

    assert any("webhook URL is blank" in warning for warning in warnings)
    assert any("Tier normalization file is missing" in warning for warning in warnings)
    assert any("Player.log was not found" in error for error in errors)

    log_path = tmp_path / "Player.log"
    log_path.write_text("", encoding="utf-8")
    monkeypatch.setattr(runner, "LOG_PATH", log_path)
    monkeypatch.setattr(runner, "WEBHOOK_URL", "not-a-url")

    warnings, errors = runner._startup_issues()

    assert "Webhook URL does not look valid" in errors

    tier_path.write_text("{not json", encoding="utf-8")
    monkeypatch.setattr(runner, "WEBHOOK_URL", "https://example.invalid/exec")

    warnings, errors = runner._startup_issues()

    assert errors == []
    assert any("Tier normalization JSON could not be read" in warning for warning in warnings)

    tier_path.write_text(json.dumps({"ok": True}), encoding="utf-8")

    warnings, errors = runner._startup_issues()

    assert warnings == []
    assert errors == []


def test_game_log_success_callback_snapshots_row_and_changed_fields(monkeypatch) -> None:
    logger = _FakeLogger()
    row = {"Game Number": 1, "Result": "Win"}
    changed_fields = ["Result"]
    posted: list[tuple[str, object, dict[str, object]]] = []

    monkeypatch.setattr(
        runner,
        "mark_game_log_posted",
        lambda match_id, game_number, posted_row: posted.append((match_id, game_number, dict(posted_row))),
    )

    callback = runner._game_log_success_callback(
        logger,
        match_id="match-1",
        game_row=row,
        changed_fields=changed_fields,
        sync_phase="live",
    )
    row["Game Number"] = 2
    row["Result"] = "Loss"
    changed_fields.append("Other")

    callback()

    assert posted == [("match-1", 1, {"Game Number": 1, "Result": "Win"})]


def test_match_log_success_callback_snapshots_row_and_changed_fields(monkeypatch) -> None:
    logger = _FakeLogger()
    row: dict[str, object] = {"Match ID": "match-1", "Result": "Win"}
    changed_fields = ["Result"]
    posted: list[tuple[str, dict[str, object]]] = []

    monkeypatch.setattr(
        runner,
        "mark_match_log_posted",
        lambda match_id, posted_row: posted.append((match_id, dict(posted_row))),
    )

    callback = runner._match_log_success_callback(
        logger,
        match_id="match-1",
        match_log_row=row,
        changed_fields=changed_fields,
        sync_phase="final",
    )
    row["Result"] = "Loss"
    changed_fields.append("Other")

    callback()

    assert posted == [("match-1", {"Match ID": "match-1", "Result": "Win"})]
