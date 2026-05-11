from mythic_edge_parser.app import sheet_exports


def test_safe_int_ignores_bool_values() -> None:
    assert sheet_exports._safe_int(True) == ""
    assert sheet_exports._safe_int(False) == ""


def test_collect_runtime_sheet_rows_emits_new_families_once() -> None:
    sheet_exports.reset_sheet_export_state()

    rows = sheet_exports.collect_runtime_sheet_rows(
        action_payload={
            "generated_at": "2026-05-06T04:14:36+00:00",
            "entries": [
                {
                    "match_id": "match-1",
                    "game_number": 1,
                    "turn_number": 3,
                    "timestamp": "2026-05-06T00:08:33+00:00",
                    "action_type": "spell_cast",
                    "cast_mode": "adventure_face",
                    "grp_id": 97547,
                    "card_name": "Mosswood Dreadknight // Dread Whispers",
                    "display_name": "Mosswood Dreadknight // Dread Whispers",
                    "resolution_status": "confirmed",
                    "actor_relation": "local",
                    "from_zone_type": "ZoneType_Hand",
                    "to_zone_type": "ZoneType_Stack",
                    "summary": "local cast Mosswood Dreadknight // Dread Whispers from hand to stack",
                }
            ],
        },
        deck_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "submitted_at": "2026-05-06T00:10:40+00:00",
            "match_id": "match-1",
            "signature": "deck-signature-1",
            "matched_decks": [
                {
                    "name": "Azban Midrange",
                    "match_mode": "same_pool_sideboarded",
                    "format": "TraditionalStandard",
                }
            ],
            "mainboard": [{"arena_id": 77508, "count": 2, "section": "mainboard", "name": "Duress"}],
            "sideboard": [],
        },
        collection_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "collection_available": True,
            "inventory_available": True,
            "owned_unique_cards": 100,
            "owned_total_card_copies": 400,
            "owned_by_rarity": {"rare": 20},
            "inventory": {"gold": 1000, "gems": 250},
            "active_deck_missing_by_rarity": {"rare": 1},
            "active_deck_completion": {"completion_rate": 0.95},
            "wanted_cards": ["Card A"],
        },
        status_payload={
            "updated_at": "2026-05-06T04:14:48+00:00",
            "status": "running",
            "current_match_id": "match-1",
            "current_game_number": 1,
            "current_player_team": 1,
            "last_event_kind": "GameState",
            "last_event_at": "2026-05-06T00:14:48+00:00",
            "webhook_successes": 3,
            "webhook_failures": 0,
            "event_failures": 0,
            "router_failures": 0,
            "active_deck_signature": "deck-signature-1",
            "active_deck_name": "Azban Midrange",
            "active_match_action_count": 1,
        },
        card_performance_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "cards": [
                {
                    "card_key": "grp:77508",
                    "grp_id": 77508,
                    "card_name": "Duress",
                    "display_name": "Duress",
                    "resolution_status": "exact_numeric_match",
                    "layout": "normal",
                    "card_faces": [],
                    "games_seen": 1,
                    "seen_in_game_games": 1,
                    "seen_in_game_win_rate": 1.0,
                    "opening_hand_games": 0,
                    "opening_hand_win_rate": "",
                    "cast_games": 1,
                    "cast_win_rate": 1.0,
                    "postboard_cast_games": 0,
                    "postboard_cast_win_rate": "",
                    "mulliganed_away_games": 0,
                    "mulligan_tax": "",
                    "top_matchups": [],
                    "top_packages": [],
                }
            ],
        },
    )

    assert {row["event_family"] for row in rows} == {
        "ActionLogRow",
        "DeckSnapshotRow",
        "CollectionSnapshotRow",
        "ParserStatusRow",
        "CardPerformanceRow",
    }

    repeated_rows = sheet_exports.collect_runtime_sheet_rows(
        action_payload={
            "generated_at": "2026-05-06T04:14:36+00:00",
            "entries": [
                {
                    "match_id": "match-1",
                    "game_number": 1,
                    "timestamp": "2026-05-06T00:08:33+00:00",
                    "action_type": "spell_cast",
                    "grp_id": 97547,
                    "from_zone_type": "ZoneType_Hand",
                    "to_zone_type": "ZoneType_Stack",
                }
            ],
        },
        deck_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "submitted_at": "2026-05-06T00:10:40+00:00",
            "match_id": "match-1",
            "signature": "deck-signature-1",
            "matched_decks": [
                {
                    "name": "Azban Midrange",
                    "match_mode": "same_pool_sideboarded",
                    "format": "TraditionalStandard",
                }
            ],
            "mainboard": [{"arena_id": 77508, "count": 2, "section": "mainboard", "name": "Duress"}],
            "sideboard": [],
        },
        collection_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "collection_available": True,
            "inventory_available": True,
            "owned_unique_cards": 100,
            "owned_total_card_copies": 400,
            "owned_by_rarity": {"rare": 20},
            "inventory": {"gold": 1000, "gems": 250},
            "active_deck_missing_by_rarity": {"rare": 1},
            "active_deck_completion": {"completion_rate": 0.95},
            "wanted_cards": ["Card A"],
        },
        status_payload={
            "updated_at": "2026-05-06T04:15:48+00:00",
            "status": "running",
            "current_match_id": "match-1",
            "current_game_number": 1,
            "current_player_team": 1,
            "last_event_kind": "GameState",
            "last_event_at": "2026-05-06T00:14:48+00:00",
            "webhook_successes": 3,
            "webhook_failures": 0,
            "event_failures": 0,
            "router_failures": 0,
            "active_deck_signature": "deck-signature-1",
            "active_deck_name": "Azban Midrange",
            "active_match_action_count": 1,
        },
        card_performance_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "cards": [
                {
                    "card_key": "grp:77508",
                    "grp_id": 77508,
                    "card_name": "Duress",
                    "display_name": "Duress",
                    "resolution_status": "exact_numeric_match",
                    "layout": "normal",
                    "card_faces": [],
                    "games_seen": 1,
                    "seen_in_game_games": 1,
                    "seen_in_game_win_rate": 1.0,
                    "opening_hand_games": 0,
                    "opening_hand_win_rate": "",
                    "cast_games": 1,
                    "cast_win_rate": 1.0,
                    "postboard_cast_games": 0,
                    "postboard_cast_win_rate": "",
                    "mulliganed_away_games": 0,
                    "mulligan_tax": "",
                    "top_matchups": [],
                    "top_packages": [],
                }
            ],
        },
    )

    assert repeated_rows == []


def test_collect_runtime_sheet_rows_reposts_parser_status_when_meaningful_values_change() -> None:
    sheet_exports.reset_sheet_export_state()

    first_rows = sheet_exports.collect_runtime_sheet_rows(
        status_payload={
            "updated_at": "2026-05-06T04:14:48+00:00",
            "status": "running",
            "current_match_id": "match-1",
            "current_game_number": 1,
            "current_player_team": 1,
            "last_event_kind": "GameState",
            "last_event_at": "2026-05-06T00:14:48+00:00",
            "webhook_successes": 3,
            "webhook_failures": 0,
            "event_failures": 0,
            "router_failures": 0,
            "active_deck_signature": "deck-signature-1",
            "active_deck_name": "Azban Midrange",
            "active_match_action_count": 1,
        },
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_card_performance_rows=False,
    )
    assert len(first_rows) == 1
    assert first_rows[0]["event_family"] == "ParserStatusRow"

    second_rows = sheet_exports.collect_runtime_sheet_rows(
        status_payload={
            "updated_at": "2026-05-06T04:15:48+00:00",
            "status": "running",
            "current_match_id": "match-1",
            "current_game_number": 1,
            "current_player_team": 1,
            "last_event_kind": "GameState",
            "last_event_at": "2026-05-06T00:14:48+00:00",
            "webhook_successes": 3,
            "webhook_failures": 0,
            "event_failures": 0,
            "router_failures": 0,
            "active_deck_signature": "deck-signature-1",
            "active_deck_name": "Azban Midrange",
            "active_match_action_count": 2,
        },
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_card_performance_rows=False,
    )
    assert second_rows == []


def test_collect_runtime_sheet_rows_reposts_parser_status_when_core_context_changes() -> None:
    sheet_exports.reset_sheet_export_state()

    first_rows = sheet_exports.collect_runtime_sheet_rows(
        status_payload={
            "updated_at": "2026-05-06T04:14:48+00:00",
            "status": "running",
            "current_match_id": "match-1",
            "current_game_number": 1,
            "current_player_team": 1,
            "last_event_kind": "GameState",
            "last_event_at": "2026-05-06T00:14:48+00:00",
            "webhook_successes": 3,
            "webhook_failures": 0,
            "event_failures": 0,
            "router_failures": 0,
            "active_deck_signature": "deck-signature-1",
            "active_deck_name": "Azban Midrange",
            "active_match_action_count": 1,
        },
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_card_performance_rows=False,
    )
    assert len(first_rows) == 1

    second_rows = sheet_exports.collect_runtime_sheet_rows(
        status_payload={
            "updated_at": "2026-05-06T04:15:48+00:00",
            "status": "running",
            "current_match_id": "match-1",
            "current_game_number": 2,
            "current_player_team": 1,
            "last_event_kind": "GameResult",
            "last_event_at": "2026-05-06T00:15:48+00:00",
            "webhook_successes": 30,
            "webhook_failures": 0,
            "event_failures": 0,
            "router_failures": 0,
            "active_deck_signature": "deck-signature-1",
            "active_deck_name": "Azban Midrange",
            "active_match_action_count": 9,
        },
        post_action_rows=False,
        post_deck_snapshot_rows=False,
        post_collection_snapshot_rows=False,
        post_card_performance_rows=False,
    )
    assert len(second_rows) == 1
    assert second_rows[0]["current_game_number"] == 2


def test_collect_runtime_sheet_rows_does_not_repost_deck_snapshot_when_only_generated_at_changes() -> None:
    sheet_exports.reset_sheet_export_state()

    first_rows = sheet_exports.collect_runtime_sheet_rows(
        deck_payload={
            "generated_at": "2026-05-06T04:14:48+00:00",
            "submitted_at": "2026-05-06T00:10:40+00:00",
            "match_id": "match-1",
            "signature": "deck-signature-1",
            "matched_decks": [
                {
                    "name": "Azban Midrange",
                    "match_mode": "same_pool_sideboarded",
                    "format": "TraditionalStandard",
                }
            ],
            "mainboard": [{"arena_id": 77508, "count": 2, "section": "mainboard", "name": "Duress"}],
            "sideboard": [],
        },
        post_action_rows=False,
        post_collection_snapshot_rows=False,
        post_parser_status_rows=False,
        post_card_performance_rows=False,
    )
    assert len(first_rows) == 1
    assert first_rows[0]["event_family"] == "DeckSnapshotRow"

    repeated_rows = sheet_exports.collect_runtime_sheet_rows(
        deck_payload={
            "generated_at": "2026-05-06T04:15:48+00:00",
            "submitted_at": "2026-05-06T00:10:40+00:00",
            "match_id": "match-1",
            "signature": "deck-signature-1",
            "matched_decks": [
                {
                    "name": "Azban Midrange",
                    "match_mode": "same_pool_sideboarded",
                    "format": "TraditionalStandard",
                }
            ],
            "mainboard": [{"arena_id": 77508, "count": 2, "section": "mainboard", "name": "Duress"}],
            "sideboard": [],
        },
        post_action_rows=False,
        post_collection_snapshot_rows=False,
        post_parser_status_rows=False,
        post_card_performance_rows=False,
    )
    assert repeated_rows == []
