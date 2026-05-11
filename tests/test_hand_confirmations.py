import json

from mythic_edge_parser.app.hand_confirmations import (
    load_hand_confirmation_payload,
    record_hand_confirmation,
    refresh_hand_confirmation_file,
)


def test_refresh_hand_confirmation_file_builds_watchlist_and_markdown(tmp_path) -> None:
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    candidate_report_path = output_dir / "grp-id-candidate-report-latest.json"
    confirmation_path = output_dir / "hand-confirmations-latest.json"

    candidate_report_path.write_text(
        json.dumps(
            {
                "generated_at": "2026-04-27T03:00:00+00:00",
                "deck_label": "Current Deck",
                "remaining_mainboard_names": {"Badgermole Cub": 4, "Ba Sing Se": 2},
                "remaining_sideboard_names": {"Day of Black Sun": 2},
            }
        ),
        encoding="utf-8",
    )

    json_path, markdown_path = refresh_hand_confirmation_file(
        path=confirmation_path,
        candidate_report_path=candidate_report_path,
    )

    assert json_path.exists()
    assert markdown_path.exists()

    payload = load_hand_confirmation_payload(json_path)
    assert payload["deck_label"] == "Current Deck"
    assert payload["watchlist"]["mainboard"] == [
        {"name": "Ba Sing Se", "count": 2},
        {"name": "Badgermole Cub", "count": 4},
    ]
    assert payload["watchlist"]["sideboard"] == [{"name": "Day of Black Sun", "count": 2}]

    markdown = markdown_path.read_text(encoding="utf-8")
    assert "## Current Watchlist" in markdown
    assert "`4x` Badgermole Cub" in markdown


def test_record_hand_confirmation_appends_confirmation_and_preserves_watchlist(tmp_path) -> None:
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    candidate_report_path = output_dir / "grp-id-candidate-report-latest.json"
    confirmation_path = output_dir / "hand-confirmations-latest.json"

    candidate_report_path.write_text(
        json.dumps(
            {
                "generated_at": "2026-04-27T03:00:00+00:00",
                "deck_label": "Current Deck",
                "remaining_mainboard_names": {"Badgermole Cub": 4},
                "remaining_sideboard_names": {"Day of Black Sun": 2},
            }
        ),
        encoding="utf-8",
    )

    refresh_hand_confirmation_file(path=confirmation_path, candidate_report_path=candidate_report_path)
    entry, json_path, markdown_path = record_hand_confirmation(
        card_name="Badgermole Cub",
        hand_window="mulliganed_hand",
        match_id_hint="match-123",
        game_number=1,
        match_date_hint="2026-04-26",
        match_time_hint="22:55",
        opponent_archetype="Izzet Prowess",
        note="Seen in opening seven.",
        path=confirmation_path,
        candidate_report_path=candidate_report_path,
    )

    assert entry["section_hint"] == "mainboard"
    payload = load_hand_confirmation_payload(json_path)
    assert len(payload["confirmations"]) == 1
    assert payload["confirmations"][0]["card_name"] == "Badgermole Cub"
    assert payload["confirmations"][0]["hand_window"] == "mulliganed_hand"
    assert payload["confirmations"][0]["match_id_hint"] == "match-123"
    assert payload["confirmations"][0]["game_number"] == 1

    markdown = markdown_path.read_text(encoding="utf-8")
    assert "Badgermole Cub" in markdown
    assert "Mulliganed hand" in markdown
    assert "match-123" in markdown
    assert "Izzet Prowess" in markdown


def test_refresh_hand_confirmation_file_uses_submitted_deck_auto_suggestions_when_decklist_is_drifted(tmp_path) -> None:
    output_dir = tmp_path / "oracle_data"
    output_dir.mkdir()
    candidate_report_path = output_dir / "grp-id-candidate-report-latest.json"
    confirmation_path = output_dir / "hand-confirmations-latest.json"

    candidate_report_path.write_text(
        json.dumps(
            {
                "generated_at": "2026-05-05T03:00:00+00:00",
                "deck_label": "Old Imported Deck",
                "decklist_alignment": "drifted",
                "decklist_alignment_notes": [
                    (
                        "Mainboard decklist drift: imported deck expects 5 unresolved card(s), but the latest "
                        "submitted deck has 2 unresolved grpId copy/copies."
                    )
                ],
                "remaining_mainboard_names": {"Stale Card": 5},
                "remaining_sideboard_names": {},
                "unresolved_mainboard_grp_ids": [
                    {
                        "grp_id": 99991,
                        "submitted_count": 2,
                        "auto_suggestion": "Fresh Card",
                        "ranked_candidates": [
                            {"name": "Fresh Card", "score": 140},
                        ],
                    },
                    {
                        "grp_id": 99992,
                        "submitted_count": 3,
                        "auto_suggestion": "",
                        "ranked_candidates": [
                            {"name": "Maybe Card", "score": 100},
                        ],
                    },
                ],
                "unresolved_sideboard_grp_ids": [],
            }
        ),
        encoding="utf-8",
    )

    json_path, markdown_path = refresh_hand_confirmation_file(
        path=confirmation_path,
        candidate_report_path=candidate_report_path,
    )

    payload = load_hand_confirmation_payload(json_path)
    assert payload["decklist_alignment"] == "drifted"
    assert payload["watchlist_source"] == "submitted_deck_auto_suggestions"
    assert payload["watchlist"]["mainboard"] == [
        {
            "name": "Fresh Card",
            "count": 2,
            "source": "submitted_deck_auto_suggestion",
            "grp_id": 99991,
        }
    ]
    assert payload["watchlist_diagnostics"]["mainboard"] == [
        {
            "grp_id": 99992,
            "count": 3,
            "top_candidate_name": "Maybe Card",
            "top_candidate_score": 100,
        }
    ]

    markdown = markdown_path.read_text(encoding="utf-8")
    assert "Decklist alignment" in markdown
    assert "`2x` Fresh Card" in markdown
    assert "grpId 99992" in markdown
