# Mythic Edge

Mythic Edge is a personal MTG Arena data pipeline.

At a high level, it does four jobs:

1. Watches MTGA's `Player.log` while you play.
2. Turns raw log noise into clean match and game summaries.
3. Pushes those summaries into your Google Sheet.
4. Stores local logs and reference data so you can debug, backfill, and build better analytics over time.

## Plain-English Architecture

```text
MTGA Player.log
  -> event stream + parsers
  -> in-memory match/game summaries
  -> local JSONL archive
  -> Google Sheets webhook
  -> dashboard analytics
```

The most important mental model is:

- `main.py` starts the parser.
- `src/mythic_edge_parser/app/runner.py` is the main runtime loop.
- `state.py` is the parser's working memory.
- `models.py` shapes match and game rows.
- `tools/google_apps_script/Code.gs` is the Google Sheets receiver.

## What To Run

- `main.py`
  The current parser entrypoint.
- `live_print_filtered_v11_match_summary.py`
  Older filename kept as a compatibility shortcut.
- `sync_tier_buckets.py`
  Refreshes meta-tier source data.
- `sync_card_catalog.py`
  Builds the Arena-aware Scryfall card catalog.
- `validate_arena_ids.py`
  Checks how well MTGA `grpId` values map to the local card catalog.
- `backfill_game_log_from_match_logs.py`
  Replays saved local logs back into `Game Log`.

## Folder Map

### Root files

- `main.py`
- `live_print_filtered_v11_match_summary.py`
- `sync_tier_buckets.py`
- `sync_card_catalog.py`
- `validate_arena_ids.py`
- `backfill_game_log_from_match_logs.py`
- `README.md`
- `pyproject.toml`

### Main code

- `src/mythic_edge_parser/app/`
  App-specific runtime logic, models, diagnostics, outputs, tier sync, and card catalog code.
- `src/mythic_edge_parser/parsers/`
  The individual MTGA event parsers.
- `src/mythic_edge_parser/log/`
  Low-level log reading and buffering utilities.

### Tools

- `tools/auto_launcher/`
  The launcher app and settings flow.
- `tools/google_apps_script/`
  The Apps Script webhook code used by the Google Sheet.
- `tools/scryfall_parser/`
  Thin wrapper around the integrated card-catalog sync.

### Data

- `data/match_logs/`
  Saved local JSONL match/game event logs.
- `data/oracle_data/`
  Card catalog outputs and Arena lookup files.
- `data/tier_sources/`
  Tier-source snapshots and normalization overrides.
- `data/runtime_logs/`
  Daily runtime logs.
- `data/status/`
  Latest runtime status snapshot.
- `data/failed_posts/`
  Rows that could not be posted to Google Sheets.
- `data/bad_events/`
  Event or router failures captured for debugging.

## Runtime Health And Troubleshooting

When something goes wrong, start here:

- `data/status/manasight_status_latest.json`
  Fastest way to see whether the parser is running, what the last event was, and whether webhook posting is succeeding.
- `data/runtime_logs/<MM_DD_YY>/manasight_runtime.log`
  Human-readable runtime log.
- `data/failed_posts/<MM_DD_YY>/failed_posts_<MM_DD_YY>.jsonl`
  Rows that failed to reach the Google Sheets webhook.
- `data/bad_events/<MM_DD_YY>/bad_events_<MM_DD_YY>.jsonl`
  Per-event failures inside the parser.

The auto launcher now surfaces the same information directly in its `Runtime health and troubleshooting` panel.

From the launcher, you can now:

- see the current parser status
- see the last event the parser processed
- see the current match and game context
- see webhook success/failure counts
- open the status file, runtime log, failed posts folder, and bad events folder with one click

## Google Sheets Design

The workbook is now organized around normalized rows rather than raw-event dumping:

- `Match Log`
  One row per match.
- `Game Log`
  One row per game.
- `Dashboard`
  Analytics and review views.
- `Helper Table`
  Hidden backend support logic.
- `Tier Source Data`
  Hidden source data for tier buckets.

## Current Card-Catalog Direction

The project now uses an Arena-aware Scryfall card catalog based on `default_cards`, not the older Oracle-only export.

That matters because MTGA gameplay logs expose Arena-facing IDs such as `grpId`, not just Oracle-style card identities.

## Development

For GitHub/Codex module work, use the four-thread workflow in `docs/codex_module_workflow.md`:

1. problem representation
2. module contract
3. implementation
4. contract testing

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -e .[dev]
pytest
python -m pytest --cov=src/mythic_edge_parser --cov-report=term-missing tests
python -m ruff check src tests
```

For a single local repo-level check on Windows PowerShell:

```powershell
.\tools\run_repo_checks.ps1
.\tools\run_repo_checks.ps1 -Coverage
```

For a safer touched-files-first lint pass on Windows PowerShell:

```powershell
.\tools\run_touched_file_checks.ps1 src\mythic_edge_parser\log\entry.py tests\test_entry_buffer_edges.py
```

That script only lints the Python files you name directly, which is useful when the whole repo still has older lint debt.

## Notes

- `__pycache__` and `.pytest_cache` are normal Python byproducts.
- The sheet-facing pipeline is designed to tolerate partial live updates and then reconcile to final match summaries.
- Opening-hand card analytics are now being built on top of the Arena-aware card catalog and the `Game Log` table.
