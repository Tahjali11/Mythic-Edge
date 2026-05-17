from __future__ import annotations

import logging
from typing import Any

from mythic_edge_parser.app import diagnostics, outputs


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


def test_webhook_post_sends_row_dict_as_top_level_json_payload(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(outputs, "WEBHOOK_URL", "https://example.invalid/exec")
    _configure_diagnostics_tmp(tmp_path, monkeypatch)
    row = {
        "event_family": "MatchLogRow",
        "event_type": "match_log_row",
        "scope": "Match",
        "match_id": "schema-payload",
        "game_number": 1,
    }
    captured: dict[str, Any] = {}

    def _fake_post(url: str, **kwargs: Any) -> _FakeSuccessResponse:
        captured["url"] = url
        captured["kwargs"] = kwargs
        return _FakeSuccessResponse()

    monkeypatch.setattr(outputs.requests, "post", _fake_post)

    assert outputs.post_row_to_google_sheets(row) is True
    assert captured["url"] == "https://example.invalid/exec"
    assert captured["kwargs"] == {"json": row, "timeout": 10}
