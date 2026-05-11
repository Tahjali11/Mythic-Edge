import json
import logging
import queue

import pytest
import requests

from mythic_edge_parser.app import diagnostics, outputs


class _FakeHttpFailureResponse:
    status_code = 403
    text = "Forbidden"

    def raise_for_status(self) -> None:
        raise requests.HTTPError("403 Client Error", response=self)


class _FakeSuccessResponse:
    status_code = 200
    text = "OK"

    def raise_for_status(self) -> None:
        return None


def test_failed_webhook_posts_are_saved_locally(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(outputs, "WEBHOOK_URL", "https://example.invalid/exec")
    monkeypatch.setattr(diagnostics, "FAILED_POSTS_ROOT", tmp_path / "failed_posts")
    monkeypatch.setattr(diagnostics, "RUNTIME_LOGS_ROOT", tmp_path / "runtime_logs")
    monkeypatch.setattr(diagnostics, "STATUS_ROOT", tmp_path / "status")
    monkeypatch.setattr(diagnostics, "_LOGGER_CONFIGURED", False)
    monkeypatch.setattr(diagnostics, "_RUNTIME_LOG_PATH", None)
    monkeypatch.setattr(diagnostics, "_STATUS_PATH", None)
    monkeypatch.setattr(diagnostics, "_STATUS_STATE", {})

    logging.getLogger("manasight").handlers.clear()

    monkeypatch.setattr(outputs.requests, "post", lambda *args, **kwargs: _FakeHttpFailureResponse())

    ok = outputs.post_row_to_google_sheets(
        {
            "event_family": "MatchLogRow",
            "event_type": "match_log_row",
            "scope": "Match",
            "match_id": "abc-123",
            "game_number": 3,
        }
    )

    assert ok is False

    failed_post_files = list((tmp_path / "failed_posts").rglob("failed_posts_*.jsonl"))
    assert len(failed_post_files) == 1

    record = json.loads(failed_post_files[0].read_text(encoding="utf-8").splitlines()[0])
    assert record["error_type"] == "HTTPError"
    assert record["response_text"] == "Forbidden"
    assert record["row"]["match_id"] == "abc-123"

    runtime_log_files = list((tmp_path / "runtime_logs").rglob("manasight_runtime.log"))
    assert len(runtime_log_files) == 1

    status_path = tmp_path / "status" / "manasight_status_latest.json"
    assert status_path.exists()
    status_payload = json.loads(status_path.read_text(encoding="utf-8"))
    assert status_payload["webhook_failures"] == 1
    assert status_payload["last_webhook_error_type"] == "HTTPError"


def test_retryable_webhook_errors_eventually_succeed(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(outputs, "WEBHOOK_URL", "https://example.invalid/exec")
    monkeypatch.setattr(diagnostics, "FAILED_POSTS_ROOT", tmp_path / "failed_posts")
    monkeypatch.setattr(diagnostics, "RUNTIME_LOGS_ROOT", tmp_path / "runtime_logs")
    monkeypatch.setattr(diagnostics, "STATUS_ROOT", tmp_path / "status")
    monkeypatch.setattr(diagnostics, "_LOGGER_CONFIGURED", False)
    monkeypatch.setattr(diagnostics, "_RUNTIME_LOG_PATH", None)
    monkeypatch.setattr(diagnostics, "_STATUS_PATH", None)
    monkeypatch.setattr(diagnostics, "_STATUS_STATE", {})
    monkeypatch.setattr(outputs.time, "sleep", lambda *_args, **_kwargs: None)

    logging.getLogger("manasight").handlers.clear()

    attempts = {"count": 0}

    def _fake_post(*_args, **_kwargs):
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise requests.ConnectionError("temporary network issue")
        return _FakeSuccessResponse()

    monkeypatch.setattr(outputs.requests, "post", _fake_post)

    ok = outputs.post_row_to_google_sheets(
        {
            "event_family": "GameLogRow",
            "event_type": "game_log_row",
            "scope": "Game",
            "match_id": "retry-123",
            "game_number": 1,
        }
    )

    assert ok is True
    assert attempts["count"] == 3

    status_path = tmp_path / "status" / "manasight_status_latest.json"
    assert status_path.exists()
    status_payload = json.loads(status_path.read_text(encoding="utf-8"))
    assert status_payload["webhook_successes"] == 1
    assert status_payload["last_webhook_attempts"] == 3
    assert status_payload["last_webhook_match_id"] == "retry-123"


def test_record_submitted_deck_writes_active_artifact_and_updates_status(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(diagnostics, "STATUS_ROOT", tmp_path / "status")
    monkeypatch.setattr(
        diagnostics,
        "ACTIVE_SUBMITTED_DECK_PATH",
        tmp_path / "status" / "active_submitted_deck_latest.json",
    )
    monkeypatch.setattr(diagnostics, "_STATUS_PATH", None)
    monkeypatch.setattr(diagnostics, "_STATUS_STATE", {})

    out_path = diagnostics.record_submitted_deck(
        {
            "deck_cards": [1001, 1001, 2002],
            "sideboard_cards": [3003],
            "game_state_id": 77,
            "resp_id": 88,
            "request_id": 99,
        },
        match_id="match-abc",
        game_number=1,
        event_timestamp="2026-05-05T22:30:00+00:00",
    )

    assert out_path is not None
    assert out_path.exists()

    artifact_payload = json.loads(out_path.read_text(encoding="utf-8"))
    assert artifact_payload["object"] == "manasight_active_submitted_deck"
    assert artifact_payload["match_id"] == "match-abc"
    assert artifact_payload["game_number"] == 1
    assert artifact_payload["mainboard_count"] == 3
    assert artifact_payload["sideboard_count"] == 1
    assert artifact_payload["signature"]

    status_path = tmp_path / "status" / "manasight_status_latest.json"
    status_payload = json.loads(status_path.read_text(encoding="utf-8"))
    assert status_payload["active_submitted_deck_path"] == str(out_path)
    assert status_payload["active_submitted_deck_signature"] == artifact_payload["signature"]
    assert status_payload["active_submitted_deck_mainboard_count"] == 3
    assert status_payload["active_submitted_deck_sideboard_count"] == 1


def test_webhook_target_display_redacts_secret_path_segments() -> None:
    display = outputs.webhook_target_display(
        "https://script.google.com/macros/s/AKfycb-example-secret-value/exec?user=tahj"
    )

    assert display == "https://script.google.com/.../exec"


def test_stop_webhook_dispatcher_drains_results_and_allows_requeue(monkeypatch) -> None:
    outputs.reset_outputs_runtime_state()
    monkeypatch.setattr(outputs, "WEBHOOK_URL", "https://example.invalid/exec")
    monkeypatch.setattr(outputs, "post_row_to_google_sheets", lambda _row: True)

    callbacks: list[str] = []
    row = {
        "event_family": "MatchLogRow",
        "event_type": "match_log_row",
        "scope": "Match",
        "match_id": "match-1",
    }

    outputs.start_webhook_dispatcher()
    assert outputs.submit_row_to_google_sheets(row, on_success=lambda: callbacks.append("ok")) is True
    outputs.stop_webhook_dispatcher(wait_for_queue=True)

    assert callbacks == ["ok"]
    assert outputs._PENDING_ROW_KEYS == set()

    outputs.start_webhook_dispatcher()
    assert outputs.submit_row_to_google_sheets(row) is True
    outputs.stop_webhook_dispatcher(wait_for_queue=True)

    outputs.reset_outputs_runtime_state()


def test_reset_outputs_runtime_state_clears_pending_runtime_queues() -> None:
    outputs.reset_outputs_runtime_state()

    row = {
        "event_family": "MatchLogRow",
        "event_type": "match_log_row",
        "scope": "Match",
        "match_id": "pending-match",
    }
    row_key = outputs._row_dispatch_key(row)
    outputs._PENDING_ROW_KEYS.add(row_key)
    outputs._DISPATCH_QUEUE.put(outputs.WebhookDispatchJob(row=row, row_key=row_key))
    outputs._DISPATCH_RESULTS.put(
        outputs.WebhookDispatchResult(
            job=outputs.WebhookDispatchJob(row=row, row_key=row_key),
            success=False,
        )
    )

    outputs.reset_outputs_runtime_state()

    assert outputs._PENDING_ROW_KEYS == set()
    with pytest.raises(queue.Empty):
        outputs._DISPATCH_QUEUE.get_nowait()
    with pytest.raises(queue.Empty):
        outputs._DISPATCH_RESULTS.get_nowait()
