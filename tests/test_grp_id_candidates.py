import json

import pytest

from mythic_edge_parser.app.decklists import parse_arena_decklist_text, save_current_decklist
from mythic_edge_parser.app.grp_id_candidates import (
    build_grp_id_candidate_report,
    build_inferred_review_report,
    confirm_candidate_suggestion,
    defer_candidate_suggestion,
    load_grp_id_candidate_report,
    promote_auto_suggestions,
    promote_auto_suggestions_with_details,
    write_inferred_review_reports,
)


def test_build_grp_id_candidate_report_uses_current_decklist_and_submit_deck_counts(tmp_path) -> None:
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    decklists_root = tmp_path / "decklists"
    decklists_root.mkdir()

    lookup_payload = {
        "cards_by_arena_id": {
            "1001": {"name": "Forest", "set": "fdn", "collector_number": "281"},
            "2002": {"name": "Llanowar Elves", "set": "fdn", "collector_number": "227"},
        }
    }
    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps(lookup_payload),
        encoding="utf-8",
    )

    override_payload = {
        "cards_by_grp_id": {
            "99991": {
                "name": "",
                "heuristic_role": "opening_hand_relevant",
                "opening_hand_observations": 2,
                "local_private_hand_observations": 4,
                "top_opening_hand_cooccurrences": [{"name": "Llanowar Elves", "count": 2}],
            },
            "99992": {
                "name": "",
                "heuristic_role": "private_zone_relevant",
                "opening_hand_observations": 0,
                "local_private_hand_observations": 0,
                "top_opening_hand_cooccurrences": [],
            },
        }
    }
    (output_dir / "mtga-grp-id-overrides-latest.json").write_text(json.dumps(override_payload), encoding="utf-8")

    decklist = parse_arena_decklist_text(
        """
Deck
4 Forest
4 Llanowar Elves
3 Mosswood Dreadknight // Dread Whispers

Sideboard
2 Duress
""",
        label="Current Golgari",
        source_path="current.txt",
    )
    decklist_path = decklists_root / "current_deck_latest.json"
    save_current_decklist(decklist, path=decklist_path)

    submit_row = {
        "kind": "ClientAction",
        "timestamp": "2026-04-27T12:00:00+00:00",
        "payload": {
            "type": "submit_deck_resp",
            "raw_client_action": {
                "payload": {
                    "submitDeckResp": {
                        "deck": {
                            "deckCards": [1001, 1001, 1001, 1001, 2002, 2002, 2002, 2002, 99991, 99991, 99991],
                            "sideboardCards": [99992, 99992],
                        }
                    }
                }
            },
        },
    }
    (match_logs_root / "sample.jsonl").write_text(json.dumps(submit_row) + "\n", encoding="utf-8")

    report = build_grp_id_candidate_report(
        decklist_path=decklist_path,
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="arena",
    )

    assert report.deck_label == "Current Golgari"
    assert report.decklist_alignment == "aligned"
    assert report.decklist_alignment_notes == []
    assert report.remaining_mainboard_names == {"Mosswood Dreadknight // Dread Whispers": 3}
    assert report.remaining_sideboard_names == {"Duress": 2}
    assert report.unresolved_mainboard_grp_ids[0].grp_id == 99991
    assert report.unresolved_mainboard_grp_ids[0].auto_suggestion == "Mosswood Dreadknight // Dread Whispers"
    assert report.unresolved_sideboard_grp_ids[0].grp_id == 99992
    assert report.unresolved_sideboard_grp_ids[0].auto_suggestion == "Duress"
    assert report.report_path is not None
    assert report.report_path.exists()
    assert report.markdown_report_path is not None
    assert report.markdown_report_path.exists()

    report_payload = json.loads(report.report_path.read_text(encoding="utf-8"))
    assert report_payload["markdown_report_path"].endswith("grp-id-candidate-report-latest.md")
    assert report_payload["decklist_alignment"] == "aligned"


def test_promote_auto_suggestions_does_not_confirm_weak_singleton_guess(tmp_path) -> None:
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    decklists_root = tmp_path / "decklists"
    decklists_root.mkdir()

    lookup_payload = {
        "cards_by_arena_id": {
            "1001": {"name": "Forest", "set": "fdn", "collector_number": "281"},
        }
    }
    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps(lookup_payload),
        encoding="utf-8",
    )

    override_path = output_dir / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "cards_by_grp_id": {
                    "99991": {
                        "name": "",
                        "heuristic_role": "private_zone_relevant",
                        "opening_hand_observations": 0,
                        "local_private_hand_observations": 4,
                        "top_opening_hand_cooccurrences": [],
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    decklist = parse_arena_decklist_text(
        """
Deck
4 Forest
3 Mosswood Dreadknight // Dread Whispers
""",
        label="Current Golgari",
        source_path="current.txt",
    )
    decklist_path = decklists_root / "current_deck_latest.json"
    save_current_decklist(decklist, path=decklist_path)

    submit_row = {
        "kind": "ClientAction",
        "timestamp": "2026-04-27T12:00:00+00:00",
        "payload": {
            "type": "submit_deck_resp",
            "raw_client_action": {
                "payload": {
                    "submitDeckResp": {
                        "deck": {
                            "deckCards": [1001, 1001, 1001, 1001, 99991, 99991, 99991],
                            "sideboardCards": [],
                        }
                    }
                }
            },
        },
    }
    (match_logs_root / "sample.jsonl").write_text(json.dumps(submit_row) + "\n", encoding="utf-8")

    report = build_grp_id_candidate_report(
        decklist_path=decklist_path,
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="arena",
    )

    promoted_details = promote_auto_suggestions_with_details(
        report,
        output_dir=output_dir,
        override_path=override_path,
    )
    row = report.unresolved_mainboard_grp_ids[0]
    assert row.auto_suggestion == "Mosswood Dreadknight // Dread Whispers"
    assert row.confirmation_status == "candidate_only"
    assert row.confidence_percent < 80
    assert promoted_details == []
    assert report.promoted_override_count == 0

    override_payload = json.loads(override_path.read_text(encoding="utf-8"))
    assert override_payload["cards_by_grp_id"]["99991"]["name"] == ""

    assert report.report_path is not None
    report_payload = json.loads(report.report_path.read_text(encoding="utf-8"))
    assert report_payload["promoted_override_count"] == 0
    assert report_payload["markdown_report_path"].endswith("grp-id-candidate-report-latest.md")

    promoted = promote_auto_suggestions(report, output_dir=output_dir, override_path=override_path)
    assert promoted == 0


def test_manual_candidate_review_can_defer_then_confirm_candidate(tmp_path) -> None:
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    decklists_root = tmp_path / "decklists"
    decklists_root.mkdir()

    lookup_payload = {
        "cards_by_arena_id": {
            "1001": {"name": "Forest", "set": "fdn", "collector_number": "281"},
        }
    }
    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps(lookup_payload),
        encoding="utf-8",
    )

    override_path = output_dir / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "cards_by_grp_id": {
                    "99991": {
                        "name": "",
                        "heuristic_role": "private_zone_relevant",
                        "opening_hand_observations": 0,
                        "local_private_hand_observations": 4,
                        "top_opening_hand_cooccurrences": [],
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    decklist = parse_arena_decklist_text(
        """
Deck
4 Forest
3 Mosswood Dreadknight // Dread Whispers
""",
        label="Current Golgari",
        source_path="current.txt",
    )
    decklist_path = decklists_root / "current_deck_latest.json"
    save_current_decklist(decklist, path=decklist_path)

    submit_row = {
        "kind": "ClientAction",
        "timestamp": "2026-04-27T12:00:00+00:00",
        "payload": {
            "type": "submit_deck_resp",
            "raw_client_action": {
                "payload": {
                    "submitDeckResp": {
                        "deck": {
                            "deckCards": [1001, 1001, 1001, 1001, 99991, 99991, 99991],
                            "sideboardCards": [],
                        }
                    }
                }
            },
        },
    }
    (match_logs_root / "sample.jsonl").write_text(json.dumps(submit_row) + "\n", encoding="utf-8")

    report = build_grp_id_candidate_report(
        decklist_path=decklist_path,
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="arena",
    )

    deferred = defer_candidate_suggestion(report, grp_id=99991, output_dir=output_dir, override_path=override_path)
    assert deferred.grp_id == 99991
    override_payload = json.loads(override_path.read_text(encoding="utf-8"))
    assert override_payload["cards_by_grp_id"]["99991"]["candidate_review"]["status"] == "deferred"

    confirmed = confirm_candidate_suggestion(report, grp_id=99991, output_dir=output_dir, override_path=override_path)
    assert confirmed.grp_id == 99991
    assert confirmed.name == "Mosswood Dreadknight // Dread Whispers"
    override_payload = json.loads(override_path.read_text(encoding="utf-8"))
    assert override_payload["cards_by_grp_id"]["99991"]["name"] == "Mosswood Dreadknight // Dread Whispers"
    assert override_payload["cards_by_grp_id"]["99991"]["name_source"] == "manual_review_confirmed_candidate"
    assert "candidate_review" not in override_payload["cards_by_grp_id"]["99991"]


def test_saved_candidate_report_can_drive_manual_review_without_rescoring(tmp_path) -> None:
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    decklists_root = tmp_path / "decklists"
    decklists_root.mkdir()

    lookup_payload = {
        "cards_by_arena_id": {
            "1001": {"name": "Forest", "set": "fdn", "collector_number": "281"},
        }
    }
    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps(lookup_payload),
        encoding="utf-8",
    )

    override_path = output_dir / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "cards_by_grp_id": {
                    "99991": {
                        "name": "",
                        "heuristic_role": "private_zone_relevant",
                        "opening_hand_observations": 0,
                        "local_private_hand_observations": 4,
                        "top_opening_hand_cooccurrences": [],
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    decklist = parse_arena_decklist_text(
        """
Deck
4 Forest
3 Mosswood Dreadknight // Dread Whispers
""",
        label="Current Golgari",
        source_path="current.txt",
    )
    decklist_path = decklists_root / "current_deck_latest.json"
    save_current_decklist(decklist, path=decklist_path)

    submit_row = {
        "kind": "ClientAction",
        "timestamp": "2026-04-27T12:00:00+00:00",
        "payload": {
            "type": "submit_deck_resp",
            "raw_client_action": {
                "payload": {
                    "submitDeckResp": {
                        "deck": {
                            "deckCards": [1001, 1001, 1001, 1001, 99991, 99991, 99991],
                            "sideboardCards": [],
                        }
                    }
                }
            },
        },
    }
    (match_logs_root / "sample.jsonl").write_text(json.dumps(submit_row) + "\n", encoding="utf-8")

    built_report = build_grp_id_candidate_report(
        decklist_path=decklist_path,
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="arena",
    )
    assert built_report.report_path is not None

    saved_report = load_grp_id_candidate_report(built_report.report_path)
    deferred = defer_candidate_suggestion(
        saved_report,
        grp_id=99991,
        output_dir=output_dir,
        override_path=override_path,
    )
    assert deferred.grp_id == 99991

    saved_report = load_grp_id_candidate_report(built_report.report_path)
    confirmed = confirm_candidate_suggestion(
        saved_report,
        grp_id=99991,
        output_dir=output_dir,
        override_path=override_path,
    )
    assert confirmed.grp_id == 99991
    override_payload = json.loads(override_path.read_text(encoding="utf-8"))
    assert override_payload["cards_by_grp_id"]["99991"]["name"] == "Mosswood Dreadknight // Dread Whispers"


def test_load_grp_id_candidate_report_fails_on_malformed_runner_up_gap(tmp_path) -> None:
    report_path = tmp_path / "grp-id-candidate-report-latest.json"
    report_path.write_text(
        json.dumps(
            {
                "generated_at": "2026-05-15T00:00:00+00:00",
                "deck_label": "Malformed Runner Gap",
                "submit_deck_timestamp": "",
                "submit_deck_source_file": "",
                "unresolved_mainboard_grp_ids": [
                    {
                        "grp_id": 99991,
                        "section": "mainboard",
                        "runner_up_gap": "not-an-int",
                    }
                ],
                "unresolved_sideboard_grp_ids": [],
                "remaining_mainboard_names": {},
                "remaining_sideboard_names": {},
                "decklist_alignment": "aligned",
                "decklist_alignment_notes": [],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        load_grp_id_candidate_report(report_path)


def test_promote_auto_suggestions_confirms_strong_fingerprint_backed_candidate(tmp_path) -> None:
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    decklists_root = tmp_path / "decklists"
    decklists_root.mkdir()

    lookup_payload = {
        "cards_by_arena_id": {
            "1001": {"name": "Forest", "set": "fdn", "collector_number": "281"},
            "2002": {
                "name": "Mosswood Dreadknight // Dread Whispers",
                "set": "woe",
                "collector_number": "231",
                "type_line": "Creature - Human Knight",
                "colors": ["B", "G"],
                "mana_cost": "{B}{G}",
            },
        }
    }
    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps(lookup_payload),
        encoding="utf-8",
    )

    override_path = output_dir / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps(
            {
                "cards_by_grp_id": {
                    "99991": {
                        "name": "",
                        "heuristic_role": "opening_hand_relevant",
                        "opening_hand_observations": 2,
                        "local_private_hand_observations": 4,
                        "top_opening_hand_cooccurrences": [],
                        "fingerprint": {
                            "card_types_seen": [{"card_type": "CardType_Creature", "count": 6}],
                            "colors_seen": [
                                {"color": "CardColor_Black", "count": 6},
                                {"color": "CardColor_Green", "count": 6},
                            ],
                            "mana_cost_signatures_seen": [{"mana_cost_signature": "1xBlack + 1xGreen", "count": 4}],
                        },
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    decklist = parse_arena_decklist_text(
        """
Deck
4 Forest
3 Mosswood Dreadknight // Dread Whispers
""",
        label="Current Golgari",
        source_path="current.txt",
    )
    decklist_path = decklists_root / "current_deck_latest.json"
    save_current_decklist(decklist, path=decklist_path)

    submit_row = {
        "kind": "ClientAction",
        "timestamp": "2026-04-27T12:00:00+00:00",
        "payload": {
            "type": "submit_deck_resp",
            "raw_client_action": {
                "payload": {
                    "submitDeckResp": {
                        "deck": {
                            "deckCards": [1001, 1001, 1001, 1001, 99991, 99991, 99991],
                            "sideboardCards": [],
                        }
                    }
                }
            },
        },
    }
    (match_logs_root / "sample.jsonl").write_text(json.dumps(submit_row) + "\n", encoding="utf-8")

    report = build_grp_id_candidate_report(
        decklist_path=decklist_path,
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="arena",
    )

    row = report.unresolved_mainboard_grp_ids[0]
    assert row.auto_suggestion == "Mosswood Dreadknight // Dread Whispers"
    assert row.confirmation_status == "ready"
    assert row.confidence_percent >= 80

    promoted_details = promote_auto_suggestions_with_details(
        report,
        output_dir=output_dir,
        override_path=override_path,
    )
    assert len(promoted_details) == 1
    assert promoted_details[0].grp_id == 99991
    assert promoted_details[0].name == "Mosswood Dreadknight // Dread Whispers"
    assert report.promoted_override_count == 1

    override_payload = json.loads(override_path.read_text(encoding="utf-8"))
    assert override_payload["cards_by_grp_id"]["99991"]["name"] == "Mosswood Dreadknight // Dread Whispers"
    assert override_payload["cards_by_grp_id"]["99991"]["name_source"] == "confirmed_inferred_candidate"
    assert override_payload["cards_by_grp_id"]["99991"]["promotion_confirmation_status"] == "ready"


def test_build_inferred_review_report_flags_changed_inferred_match_globally(tmp_path) -> None:
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
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
                            "mana_cost_signatures_seen": [{"mana_cost_signature": "1xGreen + 2xColorless", "count": 5}],
                        },
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    report = build_inferred_review_report(
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="arena",
    )

    assert report.reviewed_inferred_match_count == 1
    assert len(report.entries) == 1
    assert report.entries[0].grp_id == 99991
    assert report.entries[0].current_name == "Old Name"
    assert report.entries[0].proposed_name == "New Name"
    assert "prefers a different card identity" in report.entries[0].review_reason

    json_path, markdown_path = write_inferred_review_reports(report, output_dir=output_dir)
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["entry_count"] == 1
    assert payload["reviewed_inferred_match_count"] == 1
    assert payload["entries"][0]["current_name"] == "Old Name"
    assert markdown_path.exists()


def test_build_grp_id_candidate_report_uses_fingerprint_tiebreakers_for_ambiguous_four_ofs(tmp_path) -> None:
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    decklists_root = tmp_path / "decklists"
    decklists_root.mkdir()

    lookup_payload = {
        "cards_by_arena_id": {
            "1001": {"name": "Swamp", "type_line": "Basic Land — Swamp", "colors": [], "mana_cost": ""},
            "1002": {
                "name": "Overgrown Tomb",
                "type_line": "Land — Swamp Forest",
                "colors": [],
                "mana_cost": "",
            },
            "1003": {
                "name": "Badgermole Cub",
                "type_line": "Creature — Badger Mole",
                "colors": ["G"],
                "mana_cost": "{1}{G}",
            },
        }
    }
    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps(lookup_payload),
        encoding="utf-8",
    )

    override_payload = {
        "cards_by_grp_id": {
            "99991": {
                "name": "",
                "heuristic_role": "opening_hand_relevant",
                "opening_hand_observations": 1,
                "local_private_hand_observations": 5,
                "top_opening_hand_cooccurrences": [],
                "fingerprint": {
                    "card_types_seen": [{"card_type": "CardType_Land", "count": 20}],
                    "super_types_seen": [{"super_type": "SuperType_Basic", "count": 20}],
                    "subtypes_seen": [{"subtype": "SubType_Swamp", "count": 20}],
                    "action_types_seen": [{"action_type": "ActionType_Activate_Mana", "count": 12}],
                    "colors_seen": [],
                    "mana_cost_signatures_seen": [],
                },
            }
        }
    }
    (output_dir / "mtga-grp-id-overrides-latest.json").write_text(json.dumps(override_payload), encoding="utf-8")

    decklist = parse_arena_decklist_text(
        """
Deck
4 Swamp
4 Overgrown Tomb
4 Badgermole Cub
""",
        label="Fingerprint Test",
        source_path="fingerprint.txt",
    )
    decklist_path = decklists_root / "current_deck_latest.json"
    save_current_decklist(decklist, path=decklist_path)

    submit_row = {
        "kind": "ClientAction",
        "timestamp": "2026-04-27T12:00:00+00:00",
        "payload": {
            "type": "submit_deck_resp",
            "raw_client_action": {
                "payload": {
                    "submitDeckResp": {
                        "deck": {
                            "deckCards": [99991, 99991, 99991, 99991],
                            "sideboardCards": [],
                        }
                    }
                }
            },
        },
    }
    (match_logs_root / "sample.jsonl").write_text(json.dumps(submit_row) + "\n", encoding="utf-8")

    report = build_grp_id_candidate_report(
        decklist_path=decklist_path,
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="arena",
    )

    row = report.unresolved_mainboard_grp_ids[0]
    assert row.grp_id == 99991
    assert row.ranked_candidates[0].name == "Swamp"
    assert row.auto_suggestion == "Swamp"
    assert row.confirmation_status == "ready"
    assert any("Basic supertype" in reason for reason in row.ranked_candidates[0].reasons)


def test_build_grp_id_candidate_report_uses_best_scryfall_face_match_for_multiface_cards(tmp_path) -> None:
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    decklists_root = tmp_path / "decklists"
    decklists_root.mkdir()

    lookup_payload = {
        "cards_by_arena_id": {
            "1001": {
                "name": "Mosswood Dreadknight // Dread Whispers",
                "type_line": "Creature - Human Knight",
                "colors": ["B", "G"],
                "mana_cost": "{B}{G}",
                "card_faces": [
                    {
                        "name": "Mosswood Dreadknight",
                        "type_line": "Creature - Human Knight",
                        "colors": ["B", "G"],
                        "mana_cost": "{B}{G}",
                    },
                    {
                        "name": "Dread Whispers",
                        "type_line": "Sorcery - Adventure",
                        "colors": ["B"],
                        "mana_cost": "{3}{B}",
                    },
                ],
            },
            "1002": {
                "name": "Cut Down",
                "type_line": "Instant",
                "colors": ["B"],
                "mana_cost": "{B}",
            },
        }
    }
    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps(lookup_payload),
        encoding="utf-8",
    )

    override_payload = {
        "cards_by_grp_id": {
            "99991": {
                "name": "",
                "heuristic_role": "private_zone_relevant",
                "opening_hand_observations": 0,
                "local_private_hand_observations": 4,
                "top_opening_hand_cooccurrences": [],
                "fingerprint": {
                    "card_types_seen": [{"card_type": "CardType_Sorcery", "count": 8}],
                    "colors_seen": [{"color": "CardColor_Black", "count": 8}],
                    "mana_cost_signatures_seen": [{"mana_cost_signature": "1xBlack + 3xColorless", "count": 6}],
                    "action_types_seen": [{"action_type": "ActionType_Cast", "count": 6}],
                },
            }
        }
    }
    (output_dir / "mtga-grp-id-overrides-latest.json").write_text(json.dumps(override_payload), encoding="utf-8")

    decklist = parse_arena_decklist_text(
        """
Deck
1 Mosswood Dreadknight // Dread Whispers
1 Cut Down
""",
        label="Face Match Test",
        source_path="face-match.txt",
    )
    decklist_path = decklists_root / "current_deck_latest.json"
    save_current_decklist(decklist, path=decklist_path)

    submit_row = {
        "kind": "ClientAction",
        "timestamp": "2026-04-27T12:00:00+00:00",
        "payload": {
            "type": "submit_deck_resp",
            "raw_client_action": {
                "payload": {
                    "submitDeckResp": {
                        "deck": {
                            "deckCards": [99991],
                            "sideboardCards": [],
                        }
                    }
                }
            },
        },
    }
    (match_logs_root / "sample.jsonl").write_text(json.dumps(submit_row) + "\n", encoding="utf-8")

    report = build_grp_id_candidate_report(
        decklist_path=decklist_path,
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="arena",
    )

    row = report.unresolved_mainboard_grp_ids[0]
    assert row.grp_id == 99991
    assert row.ranked_candidates[0].name == "Mosswood Dreadknight // Dread Whispers"
    assert row.auto_suggestion == "Mosswood Dreadknight // Dread Whispers"
    assert any("Best Scryfall face match: Dread Whispers" in reason for reason in row.ranked_candidates[0].reasons)
    assert row.confirmation_status == "ready"


def test_build_grp_id_candidate_report_marks_imported_decklist_as_drifted_when_submit_deck_changes(tmp_path) -> None:
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    decklists_root = tmp_path / "decklists"
    decklists_root.mkdir()

    lookup_payload = {
        "cards_by_arena_id": {
            "1001": {"name": "Forest"},
            "1002": {"name": "Duress"},
            "1003": {"name": "Llanowar Elves"},
        }
    }
    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps(lookup_payload),
        encoding="utf-8",
    )
    (output_dir / "mtga-grp-id-overrides-latest.json").write_text(
        json.dumps({"cards_by_grp_id": {"99991": {"name": ""}}}),
        encoding="utf-8",
    )

    decklist = parse_arena_decklist_text(
        """
Deck
4 Forest
4 Llanowar Elves
""",
        label="Old Deck",
        source_path="old.txt",
    )
    decklist_path = decklists_root / "current_deck_latest.json"
    save_current_decklist(decklist, path=decklist_path)

    submit_row = {
        "kind": "ClientAction",
        "timestamp": "2026-05-05T12:00:00+00:00",
        "payload": {
            "type": "submit_deck_resp",
            "raw_client_action": {
                "payload": {
                    "submitDeckResp": {
                        "deck": {
                            "deckCards": [1001, 1001, 1001, 1001, 1002, 1002, 99991, 99991],
                            "sideboardCards": [],
                        }
                    }
                }
            },
        },
    }
    (match_logs_root / "sample.jsonl").write_text(json.dumps(submit_row) + "\n", encoding="utf-8")

    report = build_grp_id_candidate_report(
        decklist_path=decklist_path,
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="arena",
    )

    assert report.decklist_alignment == "drifted"
    assert report.decklist_alignment_notes
    assert any("drift" in note.lower() for note in report.decklist_alignment_notes)


def test_build_grp_id_candidate_report_prefers_active_submitted_deck_artifact(tmp_path) -> None:
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    decklists_root = tmp_path / "decklists"
    decklists_root.mkdir()
    status_root = tmp_path / "status"
    status_root.mkdir()

    lookup_payload = {
        "cards_by_arena_id": {
            "1001": {"name": "Forest"},
            "2002": {"name": "Duress"},
        }
    }
    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps(lookup_payload),
        encoding="utf-8",
    )
    (output_dir / "mtga-grp-id-overrides-latest.json").write_text(
        json.dumps({"cards_by_grp_id": {"99991": {"name": ""}}}),
        encoding="utf-8",
    )

    decklist = parse_arena_decklist_text(
        """
Deck
4 Forest
2 Duress
2 Fresh Unknown
""",
        label="Artifact Preferred",
        source_path="artifact.txt",
    )
    decklist_path = decklists_root / "current_deck_latest.json"
    save_current_decklist(decklist, path=decklist_path)

    stale_submit_row = {
        "kind": "ClientAction",
        "timestamp": "2026-04-01T12:00:00+00:00",
        "payload": {
            "type": "submit_deck_resp",
            "raw_client_action": {
                "payload": {
                    "submitDeckResp": {
                        "deck": {
                            "deckCards": [1001, 1001, 1001, 1001],
                            "sideboardCards": [],
                        }
                    }
                }
            },
        },
    }
    (match_logs_root / "sample.jsonl").write_text(json.dumps(stale_submit_row) + "\n", encoding="utf-8")

    active_submitted_deck_path = status_root / "active_submitted_deck_latest.json"
    active_submitted_deck_path.write_text(
        json.dumps(
            {
                "object": "manasight_active_submitted_deck",
                "submitted_at": "2026-05-05T22:30:00+00:00",
                "updated_at": "2026-05-05T22:30:01+00:00",
                "deck_cards": [1001, 1001, 1001, 1001, 2002, 2002, 99991, 99991],
                "sideboard_cards": [],
            }
        ),
        encoding="utf-8",
    )

    report = build_grp_id_candidate_report(
        decklist_path=decklist_path,
        active_submitted_deck_path=active_submitted_deck_path,
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="arena",
    )

    assert report.submit_deck_source_file == str(active_submitted_deck_path)
    assert report.remaining_mainboard_names == {"Fresh Unknown": 2}
    assert len(report.unresolved_mainboard_grp_ids) == 1
    assert report.unresolved_mainboard_grp_ids[0].grp_id == 99991


def test_build_grp_id_candidate_report_uses_exact_hand_confirmation_for_auto_suggestion(tmp_path) -> None:
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    decklists_root = tmp_path / "decklists"
    decklists_root.mkdir()

    lookup_payload = {
        "cards_by_arena_id": {
            "1001": {"name": "Forest", "type_line": "Basic Land — Forest", "colors": [], "mana_cost": ""},
            "1002": {
                "name": "Earthbender Ascension",
                "type_line": "Enchantment",
                "colors": ["G"],
                "mana_cost": "{2}{G}",
            },
            "1003": {
                "name": "Ouroboroid",
                "type_line": "Artifact Creature — Construct",
                "colors": [],
                "mana_cost": "{3}",
            },
        }
    }
    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps(lookup_payload),
        encoding="utf-8",
    )

    override_payload = {
        "cards_by_grp_id": {
            "99991": {
                "name": "",
                "heuristic_role": "opening_hand_relevant",
                "opening_hand_observations": 1,
                "local_private_hand_observations": 2,
                "top_opening_hand_cooccurrences": [],
                "fingerprint": {
                    "card_types_seen": [{"card_type": "CardType_Enchantment", "count": 6}],
                    "colors_seen": [{"color": "CardColor_Green", "count": 6}],
                    "mana_cost_signatures_seen": [{"mana_cost_signature": "1xGreen + 2xColorless", "count": 3}],
                },
            }
        }
    }
    (output_dir / "mtga-grp-id-overrides-latest.json").write_text(json.dumps(override_payload), encoding="utf-8")

    hand_confirmation_path = output_dir / "hand-confirmations-latest.json"
    hand_confirmation_path.write_text(
        json.dumps(
            {
                "object": "manasight_hand_confirmations",
                "generated_at": "2026-04-27T03:00:00+00:00",
                "updated_at": "2026-04-27T03:05:00+00:00",
                "deck_label": "Current Deck",
                "candidate_report_path": str(output_dir / "grp-id-candidate-report-latest.json"),
                "candidate_report_generated_at": "2026-04-27T03:00:00+00:00",
                "watchlist": {
                    "mainboard": [{"name": "Earthbender Ascension", "count": 3}],
                    "sideboard": [],
                },
                "confirmations": [
                    {
                        "confirmation_id": "c1",
                        "recorded_at": "2026-04-27T03:05:00+00:00",
                        "card_name": "Earthbender Ascension",
                        "hand_window": "opening_hand",
                        "section_hint": "mainboard",
                        "match_id_hint": "match-123",
                        "game_number": 1,
                        "status": "open",
                    },
                    {
                        "confirmation_id": "c2",
                        "recorded_at": "2026-04-27T03:06:00+00:00",
                        "card_name": "Ouroboroid",
                        "hand_window": "later_draw_step",
                        "section_hint": "mainboard",
                        "match_id_hint": "match-123",
                        "game_number": 1,
                        "status": "open",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    decklist = parse_arena_decklist_text(
        """
Deck
4 Forest
3 Earthbender Ascension
3 Ouroboroid
""",
        label="Confirmation Test",
        source_path="confirm.txt",
    )
    decklist_path = decklists_root / "current_deck_latest.json"
    save_current_decklist(decklist, path=decklist_path)

    submit_row = {
        "kind": "ClientAction",
        "timestamp": "2026-04-27T12:00:00+00:00",
        "payload": {
            "type": "submit_deck_resp",
            "raw_client_action": {
                "payload": {
                    "submitDeckResp": {
                        "deck": {
                            "deckCards": [1001, 1001, 1001, 1001, 99991, 99991, 99991],
                            "sideboardCards": [],
                        }
                    }
                }
            },
        },
    }
    game_state_row = {
        "kind": "GameState",
        "payload": {
            "raw_game_state": {
                "systemSeatIds": [1],
                "gameStateMessage": {
                    "gameInfo": {"matchID": "match-123", "gameNumber": 1},
                    "turnInfo": {"turnNumber": 1},
                    "zones": [
                        {
                            "zoneId": 31,
                            "type": "ZoneType_Hand",
                            "visibility": "Visibility_Private",
                            "ownerSeatId": 1,
                            "objectInstanceIds": [1, 2, 3, 4],
                        }
                    ],
                    "gameObjects": [
                        {"instanceId": 1, "grpId": 1001, "zoneId": 31, "ownerSeatId": 1},
                        {"instanceId": 2, "grpId": 1001, "zoneId": 31, "ownerSeatId": 1},
                        {"instanceId": 3, "grpId": 1001, "zoneId": 31, "ownerSeatId": 1},
                        {"instanceId": 4, "grpId": 99991, "zoneId": 31, "ownerSeatId": 1},
                    ],
                },
            }
        },
    }
    (match_logs_root / "sample.jsonl").write_text(
        json.dumps(submit_row) + "\n" + json.dumps(game_state_row) + "\n",
        encoding="utf-8",
    )

    report = build_grp_id_candidate_report(
        decklist_path=decklist_path,
        hand_confirmation_path=hand_confirmation_path,
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="arena",
    )

    row = report.unresolved_mainboard_grp_ids[0]
    assert row.manual_confirmation_hits == 1
    assert row.exact_manual_confirmation_hits == 1
    assert row.ranked_candidates[0].name == "Earthbender Ascension"
    assert row.auto_suggestion == "Earthbender Ascension"
    assert row.confirmation_status == "ready"
    assert any("Manual hand confirmation isolated this grpId" in reason for reason in row.ranked_candidates[0].reasons)


def test_build_grp_id_candidate_report_recovers_contextless_mulligan_hand_snapshots_from_match_window(tmp_path) -> None:
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    decklists_root = tmp_path / "decklists"
    decklists_root.mkdir()

    lookup_payload = {
        "cards_by_arena_id": {
            "1001": {"name": "Forest", "type_line": "Basic Land â€” Forest", "colors": [], "mana_cost": ""},
            "1002": {
                "name": "Earthbender Ascension",
                "type_line": "Enchantment",
                "colors": ["G"],
                "mana_cost": "{2}{G}",
            },
            "1003": {
                "name": "Ouroboroid",
                "type_line": "Artifact Creature â€” Construct",
                "colors": [],
                "mana_cost": "{3}",
            },
        }
    }
    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps(lookup_payload),
        encoding="utf-8",
    )

    override_payload = {
        "cards_by_grp_id": {
            "99991": {
                "name": "",
                "heuristic_role": "opening_hand_relevant",
                "opening_hand_observations": 1,
                "local_private_hand_observations": 2,
                "top_opening_hand_cooccurrences": [],
                "fingerprint": {
                    "card_types_seen": [{"card_type": "CardType_Enchantment", "count": 6}],
                    "colors_seen": [{"color": "CardColor_Green", "count": 6}],
                },
            }
        }
    }
    (output_dir / "mtga-grp-id-overrides-latest.json").write_text(json.dumps(override_payload), encoding="utf-8")

    hand_confirmation_path = output_dir / "hand-confirmations-latest.json"
    hand_confirmation_path.write_text(
        json.dumps(
            {
                "object": "manasight_hand_confirmations",
                "generated_at": "2026-04-27T03:00:00+00:00",
                "updated_at": "2026-04-27T03:05:00+00:00",
                "deck_label": "Current Deck",
                "candidate_report_path": str(output_dir / "grp-id-candidate-report-latest.json"),
                "candidate_report_generated_at": "2026-04-27T03:00:00+00:00",
                "watchlist": {
                    "mainboard": [{"name": "Earthbender Ascension", "count": 3}],
                    "sideboard": [],
                },
                "confirmations": [
                    {
                        "confirmation_id": "c1",
                        "recorded_at": "2026-04-27T03:05:00+00:00",
                        "card_name": "Earthbender Ascension",
                        "hand_window": "mulliganed_hand",
                        "section_hint": "mainboard",
                        "match_id_hint": "match-123",
                        "game_number": 1,
                        "status": "open",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    decklist = parse_arena_decklist_text(
        """
Deck
4 Forest
3 Earthbender Ascension
3 Ouroboroid
""",
        label="Context Recovery Test",
        source_path="context.txt",
    )
    decklist_path = decklists_root / "current_deck_latest.json"
    save_current_decklist(decklist, path=decklist_path)

    submit_row = {
        "kind": "ClientAction",
        "timestamp": "2026-04-27T12:00:00+00:00",
        "payload": {
            "type": "submit_deck_resp",
            "raw_client_action": {
                "payload": {
                    "submitDeckResp": {
                        "deck": {
                            "deckCards": [1001, 1001, 1001, 1001, 99991, 99991, 99991],
                            "sideboardCards": [],
                        }
                    }
                }
            },
        },
    }
    match_started_row = {
        "kind": "MatchState",
        "payload": {
            "type": "match_started",
            "match_id": "match-123",
        },
    }
    contextless_game_state_row = {
        "kind": "GameState",
        "payload": {
            "raw_game_state": {
                "systemSeatIds": [1],
                "gameStateMessage": {
                    "turnInfo": {"activePlayer": 1},
                    "zones": [
                        {
                            "zoneId": 31,
                            "type": "ZoneType_Hand",
                            "visibility": "Visibility_Private",
                            "ownerSeatId": 1,
                            "objectInstanceIds": [1, 2, 3, 4],
                        }
                    ],
                    "gameObjects": [
                        {"instanceId": 1, "grpId": 1001, "zoneId": 31, "ownerSeatId": 1},
                        {"instanceId": 2, "grpId": 1001, "zoneId": 31, "ownerSeatId": 1},
                        {"instanceId": 3, "grpId": 1001, "zoneId": 31, "ownerSeatId": 1},
                        {"instanceId": 4, "grpId": 99991, "zoneId": 31, "ownerSeatId": 1},
                    ],
                },
            }
        },
    }
    mulligan_row = {
        "kind": "ClientAction",
        "payload": {
            "type": "mulligan_resp",
            "decision": "mulligan",
        },
    }
    (match_logs_root / "sample.jsonl").write_text(
        "\n".join(
            [
                json.dumps(submit_row),
                json.dumps(match_started_row),
                json.dumps(contextless_game_state_row),
                json.dumps(mulligan_row),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = build_grp_id_candidate_report(
        decklist_path=decklist_path,
        hand_confirmation_path=hand_confirmation_path,
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="arena",
    )

    row = report.unresolved_mainboard_grp_ids[0]
    assert row.manual_confirmation_hits == 1
    assert row.exact_manual_confirmation_hits == 1
    assert row.ranked_candidates[0].name == "Earthbender Ascension"
    assert row.confirmation_status == "ready"
