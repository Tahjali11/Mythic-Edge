import json
from pathlib import Path

from mythic_edge_parser.app import card_catalog_refresh as refresh_module
from mythic_edge_parser.app.arena_id_validation import GrpIdOverrideRefreshResult
from mythic_edge_parser.app.card_catalog import write_sync_state


class _DummySession:
    def __init__(self) -> None:
        self.headers: dict[str, str] = {}

    def close(self) -> None:
        return None


def test_refresh_pipeline_keeps_last_successful_manual_sync_when_no_sync_occurs(
    tmp_path: Path,
    monkeypatch,
) -> None:
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    status_path = tmp_path / "status" / "card_catalog_refresh_status_latest.json"
    status_path.parent.mkdir()

    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps({"cards_by_arena_id": {}}),
        encoding="utf-8",
    )
    write_sync_state(
        {
            "last_synced_source_stamp": "20260508090243",
            "last_successful_sync_at": "2026-03-01T12:00:00+00:00",
            "last_successful_manual_sync_at": "2026-03-01T12:00:00+00:00",
        },
        output_dir=output_dir,
        format_key="arena",
        bulk_type="default_cards",
    )

    monkeypatch.setattr(refresh_module.requests, "Session", _DummySession)
    monkeypatch.setattr(
        refresh_module,
        "get_bulk_item",
        lambda session, bulk_type: {
            "type": "default_cards",
            "updated_at": "2026-05-08T09:02:43.122+00:00",
            "download_uri": "https://data.scryfall.io/default-cards/default-cards-20260508090243.json",
        },
    )
    monkeypatch.setattr(
        refresh_module,
        "build_grp_id_candidate_report",
        lambda **kwargs: (_ for _ in ()).throw(FileNotFoundError("No submitted deck yet")),
    )

    result = refresh_module.run_card_catalog_refresh_pipeline(
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        status_path=status_path,
    )

    status_payload = json.loads(status_path.read_text(encoding="utf-8"))
    assert result.sync_performed is False
    assert status_payload["last_successful_manual_refresh_at"] == "2026-03-01T12:00:00+00:00"


def test_refresh_pipeline_discovers_new_unresolved_grp_ids_for_replay(
    tmp_path: Path,
    monkeypatch,
) -> None:
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    status_path = tmp_path / "status" / "card_catalog_refresh_status_latest.json"
    status_path.parent.mkdir()

    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps({"cards_by_arena_id": {}}),
        encoding="utf-8",
    )
    write_sync_state(
        {
            "last_synced_source_stamp": "20260508090243",
            "last_successful_sync_at": "2026-03-01T12:00:00+00:00",
            "last_successful_manual_sync_at": "2026-03-01T12:00:00+00:00",
        },
        output_dir=output_dir,
        format_key="arena",
        bulk_type="default_cards",
    )

    monkeypatch.setattr(refresh_module.requests, "Session", _DummySession)
    monkeypatch.setattr(
        refresh_module,
        "get_bulk_item",
        lambda session, bulk_type: {
            "type": "default_cards",
            "updated_at": "2026-05-08T09:02:43.122+00:00",
            "download_uri": "https://data.scryfall.io/default-cards/default-cards-20260508090243.json",
        },
    )
    monkeypatch.setattr(refresh_module, "grp_ids_requiring_evidence_refresh", lambda cards_by_grp_id: set())
    monkeypatch.setattr(
        refresh_module,
        "discover_unresolved_grp_ids_from_saved_logs",
        lambda **kwargs: {99999},
    )
    captured: dict[str, set[int]] = {}

    def _fake_refresh_grp_id_overrides_from_logs(**kwargs) -> GrpIdOverrideRefreshResult:
        captured["target_grp_ids"] = set(kwargs["target_grp_ids"])
        return GrpIdOverrideRefreshResult(
            generated_at="2026-05-08T12:00:00+00:00",
            format_key="arena",
            override_file_path=output_dir / "mtga-grp-id-overrides-latest.json",
            total_override_entries=1,
            added_stub_count=1,
            unresolved_distinct_arena_ids=1,
        )

    monkeypatch.setattr(refresh_module, "refresh_grp_id_overrides_from_logs", _fake_refresh_grp_id_overrides_from_logs)
    monkeypatch.setattr(
        refresh_module,
        "build_grp_id_candidate_report",
        lambda **kwargs: (_ for _ in ()).throw(FileNotFoundError("No submitted deck yet")),
    )

    result = refresh_module.run_card_catalog_refresh_pipeline(
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        status_path=status_path,
    )

    assert captured["target_grp_ids"] == {99999}
    assert result.unresolved_target_grp_ids == 1


def test_refresh_pipeline_writes_global_inferred_review_even_without_current_submit_deck(
    tmp_path: Path,
    monkeypatch,
) -> None:
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    status_path = tmp_path / "status" / "card_catalog_refresh_status_latest.json"
    status_path.parent.mkdir()

    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps(
            {
                "cards_by_arena_id": {
                    "1001": {
                        "name": "Old Name",
                        "type_line": "Creature - Merfolk",
                        "colors": ["U"],
                        "mana_cost": "{3}{U}",
                    },
                    "1002": {
                        "name": "New Name",
                        "type_line": "Enchantment",
                        "colors": ["G"],
                        "mana_cost": "{2}{G}",
                    },
                }
            }
        ),
        encoding="utf-8",
    )
    (output_dir / "mtga-grp-id-overrides-latest.json").write_text(
        json.dumps(
            {
                "cards_by_grp_id": {
                    "99991": {
                        "name": "Old Name",
                        "name_source": "confirmed_inferred_candidate",
                        "heuristic_role": "opening_hand_relevant",
                        "opening_hand_observations": 2,
                        "local_private_hand_observations": 3,
                        "top_opening_hand_cooccurrences": [{"name": "New Name", "count": 3}],
                        "fingerprint": {
                            "card_types_seen": [{"card_type": "CardType_Enchantment", "count": 8}],
                            "colors_seen": [{"color": "CardColor_Green", "count": 8}],
                            "mana_cost_signatures_seen": [
                                {"mana_cost_signature": "1xGreen + 2xColorless", "count": 5}
                            ],
                        },
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    write_sync_state(
        {
            "last_synced_source_stamp": "20260508090243",
            "last_successful_sync_at": "2026-03-01T12:00:00+00:00",
            "last_successful_manual_sync_at": "2026-03-01T12:00:00+00:00",
        },
        output_dir=output_dir,
        format_key="arena",
        bulk_type="default_cards",
    )

    monkeypatch.setattr(refresh_module.requests, "Session", _DummySession)
    monkeypatch.setattr(
        refresh_module,
        "get_bulk_item",
        lambda session, bulk_type: {
            "type": "default_cards",
            "updated_at": "2026-05-08T09:02:43.122+00:00",
            "download_uri": "https://data.scryfall.io/default-cards/default-cards-20260508090243.json",
        },
    )
    monkeypatch.setattr(refresh_module, "grp_ids_requiring_evidence_refresh", lambda cards_by_grp_id: set())
    monkeypatch.setattr(
        refresh_module,
        "discover_unresolved_grp_ids_from_saved_logs",
        lambda **kwargs: set(),
    )
    monkeypatch.setattr(
        refresh_module,
        "build_grp_id_candidate_report",
        lambda **kwargs: (_ for _ in ()).throw(FileNotFoundError("No submitted deck yet")),
    )

    result = refresh_module.run_card_catalog_refresh_pipeline(
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        status_path=status_path,
    )

    status_payload = json.loads(status_path.read_text(encoding="utf-8"))
    review_payload = json.loads(result.inferred_review_json_path.read_text(encoding="utf-8"))
    assert result.candidate_report is None
    assert result.candidate_report_error == "No submitted deck yet"
    assert result.inferred_review_entry_count == 1
    assert review_payload["entry_count"] == 1
    assert review_payload["entries"][0]["current_name"] == "Old Name"
    assert status_payload["review_suggestions_pending"] is True
