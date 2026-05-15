import json
import logging
import queue
from datetime import UTC, datetime

import pytest
import requests

from mythic_edge_parser.app import diagnostics, outputs, state


class _FakeHttpFailureResponse:
    def __init__(self, status_code: int = 403, text: str = "Forbidden") -> None:
        self.status_code = status_code
        self.text = text

    def raise_for_status(self) -> None:
        raise requests.HTTPError("403 Client Error", response=self)


class _FakeSuccessResponse:
    status_code = 200
    text = "OK"

    def raise_for_status(self) -> None:
        return None


def _configure_diagnostics_tmp(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(diagnostics, "FAILED_POSTS_ROOT", tmp_path / "failed_posts")
    monkeypatch.setattr(diagnostics, "RUNTIME_LOGS_ROOT", tmp_path / "runtime_logs")
    monkeypatch.setattr(diagnostics, "STATUS_ROOT", tmp_path / "status")
    diagnostics.reset_diagnostics_runtime_state()
    logging.getLogger("manasight").handlers.clear()


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

    attempts = {"count": 0}

    def _fake_post(*_args, **_kwargs):
        attempts["count"] += 1
        return _FakeHttpFailureResponse()

    monkeypatch.setattr(outputs.requests, "post", _fake_post)

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
    assert attempts["count"] == 1

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


def test_missing_webhook_url_skips_without_failed_post(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(outputs, "WEBHOOK_URL", "")
    _configure_diagnostics_tmp(tmp_path, monkeypatch)

    ok = outputs.post_row_to_google_sheets(
        {
            "event_family": "MatchLogRow",
            "event_type": "match_log_row",
            "scope": "Match",
            "match_id": "no-webhook",
        }
    )

    assert ok is False
    assert list((tmp_path / "failed_posts").rglob("failed_posts_*.jsonl")) == []

    status_payload = json.loads((tmp_path / "status" / "manasight_status_latest.json").read_text(encoding="utf-8"))
    assert status_payload["webhook_failures"] == 0
    assert "last_webhook_error_type" not in status_payload


def test_successful_webhook_post_marks_attempt_count(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(outputs, "WEBHOOK_URL", "https://example.invalid/exec")
    _configure_diagnostics_tmp(tmp_path, monkeypatch)

    attempts = {"count": 0}

    def _fake_post(*_args, **_kwargs):
        attempts["count"] += 1
        return _FakeSuccessResponse()

    monkeypatch.setattr(outputs.requests, "post", _fake_post)

    ok = outputs.post_row_to_google_sheets(
        {
            "event_family": "MatchSummaryRow",
            "event_type": "match_summary",
            "scope": "Match",
            "match_id": "success-123",
        }
    )

    assert ok is True
    assert attempts["count"] == 1

    status_payload = json.loads((tmp_path / "status" / "manasight_status_latest.json").read_text(encoding="utf-8"))
    assert status_payload["webhook_successes"] == 1
    assert status_payload["last_webhook_attempts"] == 1
    assert status_payload["last_webhook_match_id"] == "success-123"


def test_retryable_http_errors_eventually_succeed(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(outputs, "WEBHOOK_URL", "https://example.invalid/exec")
    monkeypatch.setattr(outputs.time, "sleep", lambda *_args, **_kwargs: None)
    _configure_diagnostics_tmp(tmp_path, monkeypatch)

    attempts = {"count": 0}

    def _fake_post(*_args, **_kwargs):
        attempts["count"] += 1
        if attempts["count"] < 3:
            return _FakeHttpFailureResponse(status_code=503, text="try again")
        return _FakeSuccessResponse()

    monkeypatch.setattr(outputs.requests, "post", _fake_post)

    ok = outputs.post_row_to_google_sheets(
        {
            "event_family": "GameLogRow",
            "event_type": "game_log_row",
            "scope": "Game",
            "match_id": "retry-http-123",
        }
    )

    assert ok is True
    assert attempts["count"] == 3
    assert list((tmp_path / "failed_posts").rglob("failed_posts_*.jsonl")) == []

    status_payload = json.loads((tmp_path / "status" / "manasight_status_latest.json").read_text(encoding="utf-8"))
    assert status_payload["webhook_successes"] == 1
    assert status_payload["last_webhook_attempts"] == 3
    assert status_payload["last_webhook_match_id"] == "retry-http-123"


def test_terminal_retryable_http_failure_truncates_response_text(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(outputs, "WEBHOOK_URL", "https://example.invalid/exec")
    monkeypatch.setattr(outputs.time, "sleep", lambda *_args, **_kwargs: None)
    _configure_diagnostics_tmp(tmp_path, monkeypatch)

    attempts = {"count": 0}
    response_text = "x" * 600

    def _fake_post(*_args, **_kwargs):
        attempts["count"] += 1
        return _FakeHttpFailureResponse(status_code=503, text=response_text)

    monkeypatch.setattr(outputs.requests, "post", _fake_post)

    ok = outputs.post_row_to_google_sheets(
        {
            "event_family": "GameLogRow",
            "event_type": "game_log_row",
            "scope": "Game",
            "match_id": "terminal-http-123",
        }
    )

    assert ok is False
    assert attempts["count"] == 3

    failed_post_files = list((tmp_path / "failed_posts").rglob("failed_posts_*.jsonl"))
    assert len(failed_post_files) == 1
    record = json.loads(failed_post_files[0].read_text(encoding="utf-8").splitlines()[0])
    assert record["response_text"] == response_text[:500]

    status_payload = json.loads((tmp_path / "status" / "manasight_status_latest.json").read_text(encoding="utf-8"))
    assert status_payload["webhook_failures"] == 1
    assert status_payload["last_webhook_attempts"] == 3


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


def test_webhook_target_display_redacts_configured_url(monkeypatch) -> None:
    monkeypatch.setattr(outputs, "WEBHOOK_URL", "https://script.google.com/macros/s/AKfycb-configured-secret/exec")

    assert outputs.webhook_target_display() == "https://script.google.com/.../exec"


def test_async_submit_dedupes_reordered_dict_keys_and_keeps_first_callbacks(monkeypatch) -> None:
    monkeypatch.setattr(outputs, "update_runtime_status", lambda **_fields: None)
    outputs.reset_outputs_runtime_state()
    callbacks: list[str] = []

    def first_callback() -> None:
        callbacks.append("first")

    def duplicate_callback() -> None:
        callbacks.append("duplicate")

    row = {"event_type": "match_log_row", "match_id": "dedupe", "game_number": 1}
    reordered_row = {"game_number": 1, "match_id": "dedupe", "event_type": "match_log_row"}

    try:
        assert outputs.submit_row_to_google_sheets(row, on_success=first_callback) is True
        assert outputs.submit_row_to_google_sheets(reordered_row, on_success=duplicate_callback) is False

        job = outputs._DISPATCH_QUEUE.get_nowait()
        try:
            assert job is not None
            assert job.row == row
            assert job.row is not row
            assert job.on_success is first_callback
            assert job.on_success is not duplicate_callback
            assert callbacks == []
        finally:
            outputs._DISPATCH_QUEUE.task_done()
    finally:
        outputs.reset_outputs_runtime_state()


def test_async_submit_shallow_copies_top_level_only(monkeypatch) -> None:
    monkeypatch.setattr(outputs, "update_runtime_status", lambda **_fields: None)
    outputs.reset_outputs_runtime_state()
    row = {
        "event_type": "match_log_row",
        "match_id": "original-match",
        "nested": {"winner": "1"},
    }

    try:
        assert outputs.submit_row_to_google_sheets(row) is True
        row["match_id"] = "changed-match"
        row["nested"]["winner"] = "2"

        job = outputs._DISPATCH_QUEUE.get_nowait()
        try:
            assert job is not None
            assert job.row["match_id"] == "original-match"
            assert job.row["nested"]["winner"] == "2"
        finally:
            outputs._DISPATCH_QUEUE.task_done()
    finally:
        outputs.reset_outputs_runtime_state()


def test_drain_webhook_results_invokes_matching_callbacks_and_clears_pending(monkeypatch) -> None:
    monkeypatch.setattr(outputs, "update_runtime_status", lambda **_fields: None)
    outputs.reset_outputs_runtime_state()
    callbacks: list[str] = []

    success_job = outputs.WebhookDispatchJob(
        row={"match_id": "success"},
        row_key="success-key",
        on_success=lambda: callbacks.append("success"),
        on_failure=lambda: callbacks.append("unexpected-success-failure"),
    )
    failure_job = outputs.WebhookDispatchJob(
        row={"match_id": "failure"},
        row_key="failure-key",
        on_success=lambda: callbacks.append("unexpected-failure-success"),
        on_failure=lambda: callbacks.append("failure"),
    )
    outputs._PENDING_ROW_KEYS.update({success_job.row_key, failure_job.row_key})
    outputs._DISPATCH_RESULTS.put(outputs.WebhookDispatchResult(job=success_job, success=True))
    outputs._DISPATCH_RESULTS.put(outputs.WebhookDispatchResult(job=failure_job, success=False))

    try:
        assert outputs.drain_webhook_results(max_items=2) == 2
        assert callbacks == ["success", "failure"]
        assert outputs._PENDING_ROW_KEYS == set()
    finally:
        outputs.reset_outputs_runtime_state()


def test_drain_webhook_results_propagates_callback_exceptions(monkeypatch) -> None:
    monkeypatch.setattr(outputs, "update_runtime_status", lambda **_fields: None)
    outputs.reset_outputs_runtime_state()

    def fail_callback() -> None:
        raise RuntimeError("callback failed")

    job = outputs.WebhookDispatchJob(
        row={"match_id": "callback-failure"},
        row_key="callback-failure-key",
        on_success=fail_callback,
    )
    outputs._PENDING_ROW_KEYS.add(job.row_key)
    outputs._DISPATCH_RESULTS.put(outputs.WebhookDispatchResult(job=job, success=True))

    try:
        with pytest.raises(RuntimeError, match="callback failed"):
            outputs.drain_webhook_results()
        assert job.row_key not in outputs._PENDING_ROW_KEYS
    finally:
        outputs.reset_outputs_runtime_state()


def test_dispatch_callbacks_wait_for_result_drain_not_worker_thread(monkeypatch) -> None:
    monkeypatch.setattr(outputs, "update_runtime_status", lambda **_fields: None)
    monkeypatch.setattr(outputs, "WEBHOOK_URL", "https://example.invalid/exec")
    monkeypatch.setattr(outputs, "post_row_to_google_sheets", lambda _row: True)
    outputs.reset_outputs_runtime_state()
    callbacks: list[str] = []

    try:
        outputs.start_webhook_dispatcher()
        assert outputs.submit_row_to_google_sheets(
            {"match_id": "worker-callback"},
            on_success=lambda: callbacks.append("success"),
        )

        outputs._DISPATCH_QUEUE.join()
        assert callbacks == []

        assert outputs.drain_webhook_results() == 1
        assert callbacks == ["success"]
    finally:
        outputs.stop_webhook_dispatcher(wait_for_queue=False)
        outputs.reset_outputs_runtime_state()


def test_dispatcher_status_flags_update_on_start_stop_and_reset(monkeypatch) -> None:
    status_updates: list[dict[str, bool]] = []
    monkeypatch.setattr(outputs, "update_runtime_status", lambda **fields: status_updates.append(fields))
    outputs.reset_outputs_runtime_state()

    outputs.start_webhook_dispatcher()
    outputs.stop_webhook_dispatcher(wait_for_queue=True)
    outputs.reset_outputs_runtime_state()

    assert {"webhook_dispatcher_active": True} in status_updates
    assert {"webhook_dispatcher_active": False} in status_updates


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


def test_reset_outputs_runtime_state_clears_pending_runtime_queues_without_callbacks(monkeypatch) -> None:
    callbacks: list[str] = []
    monkeypatch.setattr(outputs, "update_runtime_status", lambda **_fields: None)
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
            job=outputs.WebhookDispatchJob(
                row=row,
                row_key=row_key,
                on_success=lambda: callbacks.append("success"),
                on_failure=lambda: callbacks.append("failure"),
            ),
            success=False,
        )
    )

    outputs.reset_outputs_runtime_state()

    assert outputs._PENDING_ROW_KEYS == set()
    assert callbacks == []
    with pytest.raises(queue.Empty):
        outputs._DISPATCH_QUEUE.get_nowait()
    with pytest.raises(queue.Empty):
        outputs._DISPATCH_RESULTS.get_nowait()


def test_reset_live_dispatcher_discards_completed_results_without_callbacks(monkeypatch) -> None:
    callbacks: list[str] = []
    monkeypatch.setattr(outputs, "update_runtime_status", lambda **_fields: None)
    monkeypatch.setattr(outputs, "WEBHOOK_URL", "https://example.invalid/exec")
    monkeypatch.setattr(outputs, "post_row_to_google_sheets", lambda _row: True)
    outputs.reset_outputs_runtime_state()

    outputs.start_webhook_dispatcher()
    assert outputs.submit_row_to_google_sheets(
        {"match_id": "reset-live"},
        on_success=lambda: callbacks.append("success"),
    )
    outputs._DISPATCH_QUEUE.join()

    outputs.reset_outputs_runtime_state()

    assert callbacks == []
    assert outputs._PENDING_ROW_KEYS == set()


def test_append_local_jsonl_preserves_serialized_rows_and_rolls_daily_paths(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(outputs, "MATCH_LOGS_ROOT", tmp_path / "match_logs")
    monkeypatch.setattr(outputs, "OUT_FILENAME_PREFIX", "events")
    state.reset_runtime_state()

    first_day = datetime(2026, 5, 14, 22, 30, tzinfo=UTC)
    second_day = datetime(2026, 5, 15, 0, 5, tzinfo=UTC)

    try:
        outputs.append_local_jsonl('{"id":"one","name":"Jace"}', first_day)
        first_path = state.get_runtime_state().current_log_path
        assert first_path == tmp_path / "match_logs" / "05_14_26" / "events_05_14_26.jsonl"
        assert first_path.read_text(encoding="utf-8").splitlines() == ['{"id":"one","name":"Jace"}']

        outputs.append_local_jsonl({"id": "two", "name": "Chandra"}, first_day)
        assert state.get_runtime_state().current_log_path == first_path
        assert first_path.read_text(encoding="utf-8").splitlines() == [
            '{"id":"one","name":"Jace"}',
            '{"id": "two", "name": "Chandra"}',
        ]

        outputs.append_local_jsonl('{"id":"three"}', second_day)
        second_path = state.get_runtime_state().current_log_path
        assert second_path == tmp_path / "match_logs" / "05_15_26" / "events_05_15_26.jsonl"
        assert second_path.read_text(encoding="utf-8").splitlines() == ['{"id":"three"}']
    finally:
        state.reset_runtime_state()
