from __future__ import annotations

import argparse
from pathlib import Path

from mythic_edge_parser.app.card_catalog import load_combined_card_lookup
from mythic_edge_parser.app.decklists import (
    canonicalize_decklist_names,
    load_current_decklist_text,
    save_current_decklist,
    validate_decklist_names,
)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import an Arena-exported decklist as the current Mythic Edge deck.")
    parser.add_argument("source_file", help="Path to an Arena-exported decklist text file.")
    parser.add_argument("--label", default="", help="Optional label to store instead of the filename stem.")
    parser.add_argument("--format", default="arena", help="Card catalog format to validate against. Default: arena.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    snapshot = load_current_decklist_text(Path(args.source_file))
    if args.label.strip():
        snapshot.label = args.label.strip()

    lookup = load_combined_card_lookup(format_key=args.format.strip().lower() or "arena")
    snapshot = canonicalize_decklist_names(snapshot, cards_by_arena_id=lookup)
    output_path = save_current_decklist(snapshot)
    known_names = {str(card.get("name", "")).strip() for card in lookup.values() if str(card.get("name", "")).strip()}
    validation = validate_decklist_names(snapshot, known_names=known_names)

    print(f"Current deck saved: {output_path}")
    print(
        f"Mainboard cards: {sum(entry.count for entry in snapshot.mainboard)} | "
        f"Sideboard cards: {sum(entry.count for entry in snapshot.sideboard)}"
    )
    if validation["missing_mainboard_names"] or validation["missing_sideboard_names"]:
        print("Decklist validation found unknown names:")
        if validation["missing_mainboard_names"]:
            print(f"  Mainboard: {', '.join(validation['missing_mainboard_names'])}")
        if validation["missing_sideboard_names"]:
            print(f"  Sideboard: {', '.join(validation['missing_sideboard_names'])}")
    else:
        print("All decklist names matched the local card catalog.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
