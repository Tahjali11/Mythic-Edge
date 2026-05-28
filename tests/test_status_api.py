import json

from mythic_edge_parser.app import evidence_runtime_status, status_api


def test_start_and_stop_status_api_server_reuses_server_info(monkeypatch) -> None:
    monkeypatch.setattr(status_api, "ENABLE_STATUS_API", True)
    monkeypatch.setattr(status_api, "STATUS_API_HOST", "127.0.0.1")
    monkeypatch.setattr(status_api, "STATUS_API_PORT", 0)

    status_api.reset_status_api_runtime_state()
    try:
        first = status_api.start_status_api_server()
        second = status_api.start_status_api_server()

        assert first is not None
        assert second == first
        assert first["host"] == "127.0.0.1"
        assert first["port"] > 0
        assert first["base_url"] == f"http://127.0.0.1:{first['port']}"
    finally:
        status_api.stop_status_api_server()

    assert status_api._SERVER is None
    assert status_api._THREAD is None


def test_api_payload_for_status_and_filtered_match_history(tmp_path, monkeypatch) -> None:
    status_root = tmp_path / "status"
    status_root.mkdir(parents=True, exist_ok=True)
    (status_root / "manasight_status_latest.json").write_text(
        json.dumps({"status": "running", "current_match_id": "match-1"}),
        encoding="utf-8",
    )

    monkeypatch.setattr(status_api, "STATUS_ROOT", status_root)
    monkeypatch.setattr(status_api, "ACTIVE_MATCH_ACTIONS_PATH", status_root / "missing_active_match_actions.json")
    monkeypatch.setattr(
        status_api,
        "load_match_history_payload",
        lambda: {
            "matches": [
                {
                    "match_id": "m1",
                    "result": "W",
                    "mtga_format": "Standard",
                    "mtga_queue_type": "Best of 3",
                    "event_id": "Play",
                    "date": "2026-05-05",
                    "deck": {"name": "Deck A", "signature": "aaa"},
                },
                {
                    "match_id": "m2",
                    "result": "L",
                    "mtga_format": "Standard",
                    "mtga_queue_type": "Best of 1",
                    "event_id": "Play",
                    "date": "2026-05-05",
                    "deck": {"name": "Deck B", "signature": "bbb"},
                },
            ]
        },
    )
    monkeypatch.setattr(
        status_api,
        "load_active_match_actions_payload",
        lambda match_id="": {
            "match_id": match_id or "match-1",
            "total_entries": 2,
            "entries": [{"action_type": "spell_cast"}],
        },
    )

    status_code, status_payload = status_api._api_payload_for_request("/status", {})
    assert status_code == 200
    assert status_payload["current_match_id"] == "match-1"

    status_code, history_payload = status_api._api_payload_for_request(
        "/match-history",
        {"deck_name": "Deck A", "result": "W"},
    )
    assert status_code == 200
    assert history_payload["total_matches"] == 1
    assert history_payload["matches"][0]["match_id"] == "m1"

    status_code, actions_payload = status_api._api_payload_for_request("/actions", {})
    assert status_code == 200
    assert actions_payload["total_entries"] == 2


def test_request_query_normalizes_root_and_query_values() -> None:
    route, query = status_api._request_query("/match-history/?deck_name=Deck+A&result=W")

    assert route == "/match-history"
    assert query == {"deck_name": "Deck A", "result": "W"}


def test_status_exposes_evidence_ledger_health_but_health_shape_is_unchanged(tmp_path, monkeypatch) -> None:
    status_root = tmp_path / "status"
    status_root.mkdir(parents=True, exist_ok=True)
    health = evidence_runtime_status.build_evidence_ledger_health_status()
    (status_root / "manasight_status_latest.json").write_text(
        json.dumps(
            {
                "status": "running",
                "updated_at": "2026-05-28T00:00:00+00:00",
                "current_match_id": "match-1",
                "webhook_failures": 0,
                "event_failures": 0,
                "router_failures": 0,
                "evidence_ledger_health": health,
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(status_api, "STATUS_ROOT", status_root)

    status_code, status_payload = status_api._api_payload_for_request("/status", {})
    health_code, health_payload = status_api._api_payload_for_request("/health", {})

    assert status_code == 200
    assert status_payload["evidence_ledger_health"]["status"] == "unavailable"
    assert health_code == 200
    assert health_payload == {
        "object": "manasight_health",
        "status": "running",
        "updated_at": "2026-05-28T00:00:00+00:00",
        "current_match_id": "match-1",
        "webhook_failures": 0,
        "event_failures": 0,
        "router_failures": 0,
    }
    assert "evidence_ledger_health" not in health_payload
