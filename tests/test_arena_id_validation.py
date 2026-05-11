import json

from mythic_edge_parser.app.arena_id_validation import (
    refresh_grp_id_overrides_from_logs,
    validate_saved_match_logs,
)


def test_validate_saved_match_logs_counts_matches_and_unmatched_ids(tmp_path) -> None:
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()

    lookup_payload = {
        "cards_by_arena_id": {
            "91829": {"name": "Forest", "set": "dmu", "collector_number": "281"},
        }
    }
    (output_dir / "scryfall-default_cards-standard-latest-arena-lookup.json").write_text(
        json.dumps(lookup_payload),
        encoding="utf-8",
    )

    sample_row = {
        "kind": "GameState",
        "payload": {
            "raw_game_state": {
                "gameStateMessage": {
                    "gameInfo": {"matchID": "m1", "gameNumber": 1},
                    "turnInfo": {"turnNumber": 1},
                    "gameObjects": [
                        {"instanceId": 1, "grpId": 91829, "zoneId": 31, "ownerSeatId": 1},
                        {"instanceId": 2, "grpId": 99999, "zoneId": 31, "ownerSeatId": 1},
                    ],
                }
            }
        },
    }
    (match_logs_root / "sample.jsonl").write_text(json.dumps(sample_row) + "\n", encoding="utf-8")

    result = validate_saved_match_logs(
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="standard",
    )

    assert result.lookup_total_cards == 1
    assert result.scanned_files == 1
    assert result.total_observations == 2
    assert result.distinct_arena_ids == 2
    assert result.matched_distinct_arena_ids == 1
    assert result.unmatched_distinct_arena_ids == 1
    assert result.top_matched_cards[0]["name"] == "Forest"
    assert result.unmatched_samples[0].arena_id == 99999
    assert result.report_path is not None
    assert result.report_path.exists()


def test_refresh_grp_id_overrides_adds_blank_stubs_for_unmatched_ids(tmp_path) -> None:
    match_logs_root = tmp_path / "match_logs"
    match_logs_root.mkdir()
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()

    lookup_payload = {
        "cards_by_arena_id": {
            "91829": {"name": "Forest", "set": "dmu", "collector_number": "281"},
        }
    }
    (output_dir / "scryfall-default_cards-arena-latest-arena-lookup.json").write_text(
        json.dumps(lookup_payload),
        encoding="utf-8",
    )

    override_path = output_dir / "mtga-grp-id-overrides-latest.json"
    override_path.write_text(
        json.dumps({"cards_by_grp_id": {"77777": {"name": "Known Override"}}}),
        encoding="utf-8",
    )

    sample_row = {
        "kind": "GameState",
        "payload": {
            "raw_game_state": {
                "systemSeatIds": [1],
                "gameStateMessage": {
                    "gameInfo": {"matchID": "m1", "gameNumber": 1},
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
                    "actions": [
                        {
                            "action": {
                                "instanceId": 2,
                                "actionType": "ActionType_Cast",
                                "manaCost": [
                                    {"count": 1, "color": ["ManaColor_Black"]},
                                    {"count": 2, "color": []},
                                ],
                            }
                        }
                    ],
                    "gameObjects": [
                        {"instanceId": 1, "grpId": 91829, "zoneId": 31, "ownerSeatId": 1},
                        {
                            "instanceId": 2,
                            "grpId": 99999,
                            "overlayGrpId": 199999,
                            "name": 1078904,
                            "zoneId": 31,
                            "ownerSeatId": 1,
                            "cardTypes": ["CardType_Instant"],
                            "superTypes": ["SuperType_Basic"],
                            "subtypes": ["SubType_Swamp"],
                            "color": ["CardColor_Black"],
                            "power": {"value": 0},
                            "toughness": {"value": 0},
                            "uniqueAbilities": [{"grpId": 55555}],
                        },
                        {"instanceId": 3, "grpId": 91829, "zoneId": 31, "ownerSeatId": 1},
                        {"instanceId": 4, "grpId": 91829, "zoneId": 31, "ownerSeatId": 1},
                    ],
                }
            }
        },
    }
    (match_logs_root / "sample.jsonl").write_text(json.dumps(sample_row) + "\n", encoding="utf-8")

    result = refresh_grp_id_overrides_from_logs(
        match_logs_root=match_logs_root,
        output_dir=output_dir,
        format_key="arena",
    )

    payload = json.loads(override_path.read_text(encoding="utf-8"))
    assert result.added_stub_count == 1
    assert payload["cards_by_grp_id"]["77777"]["name"] == "Known Override"
    assert payload["cards_by_grp_id"]["99999"]["name"] == ""
    assert payload["cards_by_grp_id"]["99999"]["observations"] == 1
    assert payload["cards_by_grp_id"]["99999"]["distinct_games_seen"] == 1
    assert payload["cards_by_grp_id"]["99999"]["heuristic_role"] == "opening_hand_relevant"
    assert payload["cards_by_grp_id"]["99999"]["local_private_hand_observations"] == 1
    assert payload["cards_by_grp_id"]["99999"]["opening_hand_observations"] == 1
    assert payload["cards_by_grp_id"]["99999"]["zones_seen"]["ZoneType_Hand|Visibility_Private|local"] == 1
    assert payload["cards_by_grp_id"]["99999"]["owner_seat_counts"]["local"] == 1
    assert payload["cards_by_grp_id"]["99999"]["sample_match_id"] == "m1"
    assert payload["cards_by_grp_id"]["99999"]["sample_match_ids"] == ["m1"]
    assert payload["cards_by_grp_id"]["99999"]["top_opening_hand_cooccurrences"] == [
        {"name": "Forest", "count": 1}
    ]
    assert payload["cards_by_grp_id"]["99999"]["fingerprint"]["card_types_seen"] == [
        {"card_type": "CardType_Instant", "count": 1}
    ]
    assert payload["cards_by_grp_id"]["99999"]["fingerprint"]["observed_name_keys"] == [
        {"name_key": "1078904", "count": 1}
    ]
    assert payload["cards_by_grp_id"]["99999"]["fingerprint"]["mana_cost_signatures_seen"] == [
        {"mana_cost_signature": "1xBlack + 2xColorless", "count": 1}
    ]
    assert result.fingerprint_report_path is not None
    assert result.fingerprint_report_path.exists()
    assert result.fingerprint_markdown_path is not None
    assert result.fingerprint_markdown_path.exists()

    fingerprint_payload = json.loads(result.fingerprint_report_path.read_text(encoding="utf-8"))
    assert fingerprint_payload["entries"][0]["grp_id"] == 99999
    assert fingerprint_payload["entries"][0]["fingerprint"]["overlay_grp_ids_seen"] == [
        {"overlay_grp_id": "199999", "count": 1}
    ]
