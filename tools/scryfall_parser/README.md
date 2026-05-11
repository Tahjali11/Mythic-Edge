# Scryfall Parser Tool

This folder is now just a friendly launcher for the integrated Mythic Edge
card-catalog sync.

- `scryfall_parser.py`: thin wrapper around
  `src/mythic_edge_parser/app/card_catalog.py`
- `run_scryfall_parser.bat`: simple Windows launcher for the script

The new sync uses Scryfall `default_cards` by default so it can keep
Arena-relevant fields such as `arena_id`, not just Oracle text.

Outputs are written into `../../data/oracle_data/`:
- `scryfall-default_cards-<format>-latest.json`
- `scryfall-default_cards-<format>-latest-arena-lookup.json`
- `scryfall-default_cards-<format>-latest.csv`
