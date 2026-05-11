from __future__ import annotations

import json
import logging
from types import SimpleNamespace

from mythic_edge_parser.app import diagnostics


def test_normalize_int_list_ignores_bools_and_bad_values() -> None:
    assert diagnostics.normalize_int_list([1, "2", " 3 ", True, False, "x", None, 4]) == [1, 2, 3, 4]


def test_reset_diagnostics_runtime_state_clears_paths_handlers_and_status(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(diagnostics, "RUNTIME_LOGS_ROOT", tmp_path / "runtime_logs")
    monkeypatch.setattr(diagnostics, "STATUS_ROOT", tmp_path / "status")

    diagnostics.reset_diagnostics_runtime_state()
    logger = diagnostics.setup_runtime_logging()
    diagnostics.update_runtime_status(example="value")

    assert diagnostics.current_runtime_log_path() is not None
    assert diagnostics.current_status_path() is not None
    assert logger.handlers
    assert diagnostics._STATUS_STATE["example"] == "value"

    diagnostics.reset_diagnostics_runtime_state()

    assert diagnostics.current_runtime_log_path() is None
    assert diagnostics.current_status_path() is None
    assert diagnostics._STATUS_STATE == {}
    assert logging.getLogger("manasight").handlers == []


def test_record_router_failure_updates_status_and_writes_entry(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(diagnostics, "BAD_EVENTS_ROOT", tmp_path / "bad_events")
    monkeypatch.setattr(diagnostics, "STATUS_ROOT", tmp_path / "status")

    diagnostics.reset_diagnostics_runtime_state()
    entry = SimpleNamespace(
        header=SimpleNamespace(value="[UnityCrossThreadLogger]"),
        body={"message": "router payload"},
    )

    try:
        raise RuntimeError("router blew up")
    except RuntimeError as exc:
        out_path = diagnostics.record_router_failure(entry, exc)

    assert out_path.exists()

    record = json.loads(out_path.read_text(encoding="utf-8").splitlines()[0])
    assert record["stage"] == "router"
    assert record["error_type"] == "RuntimeError"
    assert record["entry_body"] == {"message": "router payload"}

    status_path = tmp_path / "status" / "manasight_status_latest.json"
    status_payload = json.loads(status_path.read_text(encoding="utf-8"))
    assert status_payload["router_failures"] == 1
    assert status_payload["last_router_error_type"] == "RuntimeError"
    assert status_payload["status"] == "running_with_errors"


def test_mark_webhook_failure_redacts_secret_webhook_url_in_status(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(diagnostics, "STATUS_ROOT", tmp_path / "status")

    diagnostics.reset_diagnostics_runtime_state()
    row = {"event_family": "TierSourceSnapshot", "event_type": "tier_source_snapshot"}
    exc = RuntimeError(
        "404 Client Error: Not Found for url: "
        "https://script.google.com/macros/s/AKfycb-secret-value/exec?user=tahj"
    )

    diagnostics.mark_webhook_failure(row, exc, attempts=1)

    status_path = tmp_path / "status" / "manasight_status_latest.json"
    status_payload = json.loads(status_path.read_text(encoding="utf-8"))
    assert status_payload["last_webhook_error"] == (
        "404 Client Error: Not Found for url: https://script.google.com/.../exec"
    )
