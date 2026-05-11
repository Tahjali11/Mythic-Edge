from pathlib import Path

from mythic_edge_parser.app.decklists import (
    build_catalog_name_aliases,
    canonicalize_decklist_names,
    load_current_decklist,
    parse_arena_decklist_text,
    save_current_decklist,
)


def test_parse_arena_decklist_text_handles_mainboard_and_sideboard() -> None:
    snapshot = parse_arena_decklist_text(
        """
Deck
4 Llanowar Elves (FDN) 227
3 Mosswood Dreadknight // Dread Whispers (WOE) 231

Sideboard
2 Duress (STA) 29
""",
        label="Golgari Test",
        source_path="deck.txt",
    )

    assert snapshot.label == "Golgari Test"
    assert [entry.name for entry in snapshot.mainboard] == [
        "Llanowar Elves",
        "Mosswood Dreadknight // Dread Whispers",
    ]
    assert [entry.count for entry in snapshot.mainboard] == [4, 3]
    assert [entry.name for entry in snapshot.sideboard] == ["Duress"]
    assert [entry.count for entry in snapshot.sideboard] == [2]


def test_save_and_load_current_decklist_round_trip(tmp_path) -> None:
    snapshot = parse_arena_decklist_text("Deck\n4 Forest\n", label="Simple Deck", source_path="deck.txt")
    output_path = tmp_path / "current_deck_latest.json"

    save_current_decklist(snapshot, path=output_path)
    loaded = load_current_decklist(output_path)

    assert loaded.label == "Simple Deck"
    assert loaded.source_path == "deck.txt"
    assert loaded.mainboard[0].name == "Forest"
    assert loaded.mainboard[0].count == 4


def test_canonicalize_decklist_names_maps_unique_face_name_to_full_name() -> None:
    snapshot = parse_arena_decklist_text(
        "Deck\n2 Mosswood Dreadknight\n",
        label="DFC Test",
        source_path="deck.txt",
    )
    lookup = {
        "1": {
            "name": "Mosswood Dreadknight // Dread Whispers",
            "card_faces": [
                {"name": "Mosswood Dreadknight"},
                {"name": "Dread Whispers"},
            ],
        }
    }

    aliases = build_catalog_name_aliases(lookup)
    canonical = canonicalize_decklist_names(snapshot, cards_by_arena_id=lookup)

    assert aliases["Mosswood Dreadknight"] == "Mosswood Dreadknight // Dread Whispers"
    assert canonical.mainboard[0].name == "Mosswood Dreadknight // Dread Whispers"
    assert canonical.mainboard[0].count == 2


def test_load_current_decklist_skips_malformed_entries_instead_of_crashing(tmp_path: Path) -> None:
    output_path = tmp_path / "current_deck_latest.json"
    output_path.write_text(
        """
{
  "label": "Malformed Deck",
  "generated_at": "2026-05-08T00:00:00+00:00",
  "source_path": "deck.txt",
  "mainboard": [
    {"name": "Forest", "count": "4"},
    {"name": "", "count": 2},
    {"name": "Swamp", "count": "x"}
  ],
  "sideboard": [
    {"name": "Duress", "count": 2},
    "bad row"
  ]
}
""".strip(),
        encoding="utf-8",
    )

    loaded = load_current_decklist(output_path)

    assert [(entry.name, entry.count) for entry in loaded.mainboard] == [("Forest", 4)]
    assert [(entry.name, entry.count) for entry in loaded.sideboard] == [("Duress", 2)]
