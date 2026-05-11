import json

from mythic_edge_parser.app import grp_id_catalog


def test_safe_int_ignores_bool_values() -> None:
    assert grp_id_catalog._safe_int(True) is None
    assert grp_id_catalog._safe_int(False) is None


def test_grp_id_catalog_demotes_contradicted_land_promotion(tmp_path, monkeypatch) -> None:
    catalog_path = tmp_path / "mtga-grp-id-catalog-latest.json"
    override_path = tmp_path / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "97547": {
                        "name": "Mosswood Dreadknight // Dread Whispers",
                        "name_source": "auto_promoted_singleton_candidate",
                        "fingerprint": {
                            "card_types_seen": [{"card_type": "CardType_Land", "count": 23}],
                            "action_types_seen": [
                                {"action_type": "ActionType_Play", "count": 5},
                                {"action_type": "ActionType_Activate_Mana", "count": 18},
                            ],
                        },
                    }
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        grp_id_catalog,
        "load_arena_lookup",
        lambda **_kwargs: {
            "86952": {
                "name": "Mosswood Dreadknight // Dread Whispers",
                "layout": "adventure",
                "type_line": "Creature — Human Knight // Sorcery — Adventure",
                "card_faces": [
                    {"name": "Mosswood Dreadknight", "type_line": "Creature — Human Knight"},
                    {"name": "Dread Whispers", "type_line": "Sorcery — Adventure"},
                ],
            }
        },
    )

    grp_id_catalog._CATALOG_PAYLOAD = None
    grp_id_catalog._CATALOG_LOOKUP = {}
    grp_id_catalog.refresh_grp_id_catalog(
        path=catalog_path,
        grp_id_override_path=override_path,
        candidate_report_path=tmp_path / "missing-report.json",
        output_dir=tmp_path,
    )

    entry = grp_id_catalog.resolve_grp_id_entry(97547, path=catalog_path)
    assert entry["resolved_name"] == ""
    assert entry["demoted_resolved_name"] == "Mosswood Dreadknight // Dread Whispers"
    assert entry["resolution_status"] == "contradicted"
    assert entry["blocked_auto_promotion"] is True
    assert "observed_land_but_resolved_card_not_land" in entry["contradiction_flags"]
    assert grp_id_catalog.is_grp_id_promotable(entry) is False


def test_grp_id_catalog_keeps_demoted_override_blocked_without_live_name(tmp_path, monkeypatch) -> None:
    catalog_path = tmp_path / "mtga-grp-id-catalog-latest.json"
    override_path = tmp_path / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "97547": {
                        "name": "",
                        "demoted_name": "Mosswood Dreadknight // Dread Whispers",
                        "demoted_primary_source": "auto_promoted_singleton_candidate",
                        "blocked_auto_promotion": True,
                        "fingerprint": {
                            "card_types_seen": [{"card_type": "CardType_Land", "count": 23}],
                            "action_types_seen": [
                                {"action_type": "ActionType_Play", "count": 5},
                                {"action_type": "ActionType_Activate_Mana", "count": 18},
                            ],
                        },
                    }
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        grp_id_catalog,
        "load_arena_lookup",
        lambda **_kwargs: {
            "86952": {
                "name": "Mosswood Dreadknight // Dread Whispers",
                "layout": "adventure",
                "type_line": "Creature â€” Human Knight // Sorcery â€” Adventure",
                "card_faces": [
                    {"name": "Mosswood Dreadknight", "type_line": "Creature â€” Human Knight"},
                    {"name": "Dread Whispers", "type_line": "Sorcery â€” Adventure"},
                ],
            }
        },
    )

    grp_id_catalog._CATALOG_PAYLOAD = None
    grp_id_catalog._CATALOG_LOOKUP = {}
    grp_id_catalog.refresh_grp_id_catalog(
        path=catalog_path,
        grp_id_override_path=override_path,
        candidate_report_path=tmp_path / "missing-report.json",
        output_dir=tmp_path,
    )

    entry = grp_id_catalog.resolve_grp_id_entry(97547, path=catalog_path)
    assert entry["resolved_name"] == ""
    assert entry["demoted_resolved_name"] == "Mosswood Dreadknight // Dread Whispers"
    assert entry["resolution_status"] == "contradicted"
    assert entry["blocked_auto_promotion"] is True
    assert grp_id_catalog.is_grp_id_promotable(entry) is False


def test_bootstrap_grp_id_catalog_uses_existing_catalog_file(tmp_path, monkeypatch) -> None:
    catalog_path = tmp_path / "mtga-grp-id-catalog-latest.json"
    catalog_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_catalog",
                "generated_at": "2026-05-06T00:00:00+00:00",
                "updated_at": "2026-05-06T00:00:00+00:00",
                "cards_by_grp_id": {
                    "12345": {
                        "grp_id": 12345,
                        "resolved_name": "Test Card",
                        "display_name": "Test Card",
                        "resolution_status": "confirmed",
                        "primary_source": "grp_id_override",
                    }
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    grp_id_catalog._CATALOG_PAYLOAD = None
    grp_id_catalog._CATALOG_LOOKUP = {}

    def _unexpected_refresh(**_kwargs) -> None:
        raise AssertionError("bootstrap should load the existing catalog file instead of rebuilding it")

    monkeypatch.setattr(grp_id_catalog, "refresh_grp_id_catalog", _unexpected_refresh)

    grp_id_catalog.bootstrap_grp_id_catalog(path=catalog_path)

    entry = grp_id_catalog.resolve_grp_id_entry(12345, path=catalog_path)
    assert entry["resolved_name"] == "Test Card"
    assert entry["display_name"] == "Test Card"


def test_grp_id_catalog_prefers_exact_numeric_arena_lookup_for_readable_name(tmp_path, monkeypatch) -> None:
    catalog_path = tmp_path / "mtga-grp-id-catalog-latest.json"
    override_path = tmp_path / "mtga-grp-id-overrides-latest.json"
    report_path = tmp_path / "grp-id-candidate-report-latest.json"

    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "97547": {
                        "name": "",
                        "fingerprint": {
                            "card_types_seen": [{"card_type": "CardType_Creature", "count": 3}],
                        },
                    }
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    report_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_candidate_report",
                "unresolved_mainboard_grp_ids": [
                    {
                        "grp_id": 97547,
                        "section": "mainboard",
                        "submitted_count": 2,
                        "heuristic_role": "opening_hand_relevant",
                        "ranked_candidates": [
                            {"name": "Wrong Candidate", "score": 20},
                        ],
                        "auto_suggestion": "Wrong Candidate",
                    }
                ],
                "unresolved_sideboard_grp_ids": [],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        grp_id_catalog,
        "load_arena_lookup",
        lambda **_kwargs: {
            "97547": {
                "name": "Exact Lookup Card",
                "layout": "normal",
                "type_line": "Creature - Elf",
                "card_faces": [],
            }
        },
    )

    grp_id_catalog._CATALOG_PAYLOAD = None
    grp_id_catalog._CATALOG_LOOKUP = {}
    grp_id_catalog.refresh_grp_id_catalog(
        path=catalog_path,
        grp_id_override_path=override_path,
        candidate_report_path=report_path,
        output_dir=tmp_path,
    )

    entry = grp_id_catalog.resolve_grp_id_entry(97547, path=catalog_path)
    assert entry["resolved_name"] == "Exact Lookup Card"
    assert entry["display_name"] == "Exact Lookup Card"
    assert entry["primary_source"] == "exact_numeric_arena_lookup"
    assert entry["arena_lookup_name"] == "Exact Lookup Card"
    assert entry["candidate_names"][0]["name"] == "Wrong Candidate"
    assert grp_id_catalog.resolve_grp_id_name(97547, path=catalog_path) == "Exact Lookup Card"


def test_grp_id_catalog_marks_confirmed_inferred_override_as_inferred_confirmed(tmp_path, monkeypatch) -> None:
    catalog_path = tmp_path / "mtga-grp-id-catalog-latest.json"
    override_path = tmp_path / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_overrides",
                "cards_by_grp_id": {
                    "99991": {
                        "name": "Mosswood Dreadknight // Dread Whispers",
                        "name_source": "confirmed_inferred_candidate",
                    }
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(grp_id_catalog, "load_arena_lookup", lambda **_kwargs: {})

    grp_id_catalog._CATALOG_PAYLOAD = None
    grp_id_catalog._CATALOG_LOOKUP = {}
    grp_id_catalog.refresh_grp_id_catalog(
        path=catalog_path,
        grp_id_override_path=override_path,
        candidate_report_path=tmp_path / "missing-report.json",
        output_dir=tmp_path,
    )

    entry = grp_id_catalog.resolve_grp_id_entry(99991, path=catalog_path)
    assert entry["resolved_name"] == "Mosswood Dreadknight // Dread Whispers"
    assert entry["resolution_status"] == "inferred_confirmed"
    assert entry["primary_source"] == "confirmed_inferred_candidate"


def test_bootstrap_grp_id_catalog_respects_new_catalog_path_without_manual_reset(tmp_path) -> None:
    first_path = tmp_path / "first-catalog.json"
    second_path = tmp_path / "second-catalog.json"
    first_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_catalog",
                "generated_at": "2026-05-06T00:00:00+00:00",
                "updated_at": "2026-05-06T00:00:00+00:00",
                "cards_by_grp_id": {
                    "111": {
                        "grp_id": 111,
                        "resolved_name": "First Card",
                        "display_name": "First Card",
                        "resolution_status": "confirmed",
                        "primary_source": "grp_id_override",
                    }
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    second_path.write_text(
        json.dumps(
            {
                "object": "manasight_grp_id_catalog",
                "generated_at": "2026-05-06T00:00:00+00:00",
                "updated_at": "2026-05-06T00:00:00+00:00",
                "cards_by_grp_id": {
                    "222": {
                        "grp_id": 222,
                        "resolved_name": "Second Card",
                        "display_name": "Second Card",
                        "resolution_status": "confirmed",
                        "primary_source": "grp_id_override",
                    }
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    grp_id_catalog.reset_grp_id_catalog_runtime_state()
    grp_id_catalog.bootstrap_grp_id_catalog(path=first_path)
    first_entry = grp_id_catalog.resolve_grp_id_entry(111, path=first_path)
    second_entry = grp_id_catalog.resolve_grp_id_entry(222, path=second_path)

    assert first_entry["resolved_name"] == "First Card"
    assert second_entry["resolved_name"] == "Second Card"
