from types import SimpleNamespace

from mythic_edge_parser.app import analytics_sidecar
from mythic_edge_parser.app.analytics_sidecar import _runtime_export_flags, _should_refresh_card_performance


def test_should_refresh_card_performance_only_for_completed_match_states() -> None:
    started_event = SimpleNamespace(kind="MatchState", payload={"type": "match_started"})
    completed_event = SimpleNamespace(kind="MatchState", payload={"type": "match_completed"})

    assert _should_refresh_card_performance(started_event) is False
    assert _should_refresh_card_performance(completed_event) is True


def test_runtime_export_flags_reduce_optional_work_for_game_state() -> None:
    event = SimpleNamespace(kind="GameState", payload={})
    flags = _runtime_export_flags(event, card_performance_ready=False)
    assert flags["post_action_rows"] is False
    assert flags["post_deck_snapshot_rows"] is False
    assert flags["post_collection_snapshot_rows"] is False
    assert flags["post_parser_status_rows"] is False
    assert flags["post_card_performance_rows"] is False


def test_runtime_export_flags_enable_card_performance_only_after_match_completion(monkeypatch) -> None:
    monkeypatch.setattr(analytics_sidecar, "POST_PARSER_STATUS_ROWS", True)
    event = SimpleNamespace(kind="MatchState", payload={"type": "match_completed"})
    flags = _runtime_export_flags(event, card_performance_ready=True)
    assert flags["post_action_rows"] is True
    assert flags["post_parser_status_rows"] is True
    assert flags["post_card_performance_rows"] is True


def test_runtime_export_flags_post_action_rows_on_game_result(monkeypatch) -> None:
    monkeypatch.setattr(analytics_sidecar, "POST_PARSER_STATUS_ROWS", True)
    event = SimpleNamespace(kind="GameResult", payload={})
    flags = _runtime_export_flags(event, card_performance_ready=False)
    assert flags["post_action_rows"] is True
    assert flags["post_parser_status_rows"] is True


def test_runtime_export_flags_post_deck_snapshot_on_submit_deck_but_not_collection_events() -> None:
    submit_event = SimpleNamespace(kind="ClientAction", payload={"type": "submit_deck_resp"})
    collection_event = SimpleNamespace(kind="Collection", payload={})

    submit_flags = _runtime_export_flags(submit_event, card_performance_ready=False)
    collection_flags = _runtime_export_flags(collection_event, card_performance_ready=False)

    assert submit_flags["post_deck_snapshot_rows"] is True
    assert collection_flags["post_deck_snapshot_rows"] is False
