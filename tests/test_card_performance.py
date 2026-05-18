import json

from mythic_edge_parser.app import card_performance


def test_refresh_card_performance_artifacts_aggregates_opening_cast_seen_and_mulligan_metrics(
    tmp_path, monkeypatch
) -> None:
    status_root = tmp_path / "status"
    actions_root = status_root / "actions"
    status_root.mkdir(parents=True, exist_ok=True)
    actions_root.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(card_performance, "MATCH_HISTORY_PATH", status_root / "match_history_latest.json")
    monkeypatch.setattr(card_performance, "STATUS_ACTIONS_ROOT", actions_root)
    monkeypatch.setattr(card_performance, "CARD_PERFORMANCE_PATH", status_root / "card_performance_latest.json")
    monkeypatch.setattr(card_performance, "CARD_PERFORMANCE_MARKDOWN_PATH", status_root / "card_performance_latest.md")
    monkeypatch.setattr(
        card_performance,
        "load_grp_id_catalog_lookup",
        lambda: {
            "1001": {
                "resolved_name": "Card A",
                "display_name": "Card A",
                "resolution_status": "confirmed",
                "resolved_layout": "",
                "resolved_card_faces": [],
            },
            "2002": {
                "resolved_name": "Card B",
                "display_name": "Card B",
                "resolution_status": "confirmed",
                "resolved_layout": "",
                "resolved_card_faces": [],
            },
        },
    )

    (status_root / "match_history_latest.json").write_text(
        json.dumps(
            {
                "matches": [
                    {
                        "match_id": "match-1",
                        "games": [
                            {
                                "game_number": 1,
                                "result": "W",
                                "opening_hand": ["Card A", "Card B"],
                                "mulliganed_away": [],
                            },
                            {
                                "game_number": 2,
                                "result": "L",
                                "opening_hand": ["Card B"],
                                "mulliganed_away": ["Card A"],
                            },
                        ],
                    }
                ]
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (actions_root / "match-1.json").write_text(
        json.dumps(
            {
                "match_id": "match-1",
                "entries": [
                    {
                        "match_id": "match-1",
                        "game_number": 1,
                        "action_type": "spell_cast",
                        "grp_id": 1001,
                        "card_name": "Card A",
                        "display_name": "Card A",
                        "resolution_status": "confirmed",
                        "layout": "",
                        "card_faces": [],
                        "actor_relation": "local",
                    },
                    {
                        "match_id": "match-1",
                        "game_number": 1,
                        "action_type": "land_played",
                        "grp_id": 2002,
                        "card_name": "Card B",
                        "display_name": "Card B",
                        "resolution_status": "confirmed",
                        "layout": "",
                        "card_faces": [],
                        "actor_relation": "local",
                    },
                    {
                        "match_id": "match-1",
                        "game_number": 2,
                        "action_type": "land_played",
                        "grp_id": 2002,
                        "card_name": "Card B",
                        "display_name": "Card B",
                        "resolution_status": "confirmed",
                        "layout": "",
                        "card_faces": [],
                        "actor_relation": "local",
                    },
                    {
                        "match_id": "match-1",
                        "game_number": 2,
                        "action_type": "spell_cast",
                        "grp_id": 9999,
                        "card_name": "Opponent Card",
                        "display_name": "Opponent Card",
                        "resolution_status": "confirmed",
                        "layout": "",
                        "card_faces": [],
                        "actor_relation": "opponent",
                    },
                ],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    payload = card_performance.refresh_card_performance_artifacts(
        history_path=status_root / "match_history_latest.json",
        actions_root=actions_root,
    )

    assert payload["total_cards"] == 2
    cards_by_name = {card["display_name"]: card for card in payload["cards"]}
    assert "Opponent Card" not in cards_by_name
    assert cards_by_name["Card A"]["opening_hand_games"] == 1
    assert cards_by_name["Card A"]["opening_hand_win_rate"] == 1.0
    assert cards_by_name["Card A"]["cast_games"] == 1
    assert cards_by_name["Card A"]["cast_win_rate"] == 1.0
    assert cards_by_name["Card A"]["mulliganed_away_games"] == 1
    assert cards_by_name["Card A"]["mulligan_tax"] == 0.5
    assert cards_by_name["Card B"]["opening_hand_games"] == 2
    assert cards_by_name["Card B"]["seen_in_game_games"] == 2

    markdown = (status_root / "card_performance_latest.md").read_text(encoding="utf-8")
    assert "Card A" in markdown
    assert "Card B" in markdown
