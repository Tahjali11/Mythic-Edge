# Mythic Edge Learning Guide

## Who This Is For

This guide is for someone who is smart, curious, and new to programming.

If you are comfortable reading complicated ideas but do not yet feel fluent in code, this document is for you. I wrote it in plain English on purpose. The goal is not just to explain what Mythic Edge does, but to use Mythic Edge as a way to teach the basic ideas that show up in real software projects.

## What This Project Does In One Sentence

Mythic Edge watches MTG Arena's log file, turns messy raw text into structured match data, saves that data locally, and can send cleaned summaries to Google Sheets.

## The Big Picture

At a global level, the project is an automation pipeline:

```text
MTGA Player.log
    -> file tailer
    -> line buffer
    -> router
    -> parsers
    -> typed events
    -> match state / summaries
    -> local logs + Google Sheets + tier sync helpers
```

Here is the same idea in plain English:

1. MTG Arena writes a giant running text file called `Player.log`.
2. Mythic Edge watches that file for new lines.
3. It groups those lines into meaningful chunks.
4. It asks, "What kind of thing is this chunk?"
5. Specialized parser functions turn those chunks into structured event objects.
6. The app layer decides which events matter, remembers match context, and builds summaries.
7. The results get written to:
   - local JSONL files
   - Google Sheets through a webhook
   - tier-source snapshots for your workbook helper table

## Why The Project Is Organized This Way

This project separates responsibilities.

That is one of the most important ideas in programming.

Instead of building one giant script that does everything, Mythic Edge splits the work into layers:

- `log/` handles raw text coming off disk.
- `parsers/` know how to recognize specific MTGA message types.
- `events.py` defines the structured event shapes.
- `stream.py` moves events through the system.
- `app/` turns raw events into match summaries and sheet-ready rows.
- `tools/` contains user-facing helpers like the launcher and Scryfall tool.
- `tools/google_apps_script/Code.gs` is the Google Sheets side of the pipeline.

This makes the code easier to read, test, and repair.

## A Very Short Computer Science Primer

### Script, Module, Package

- A **script** is a file you run directly.
- A **module** is a Python file that contains reusable code.
- A **package** is a folder of modules that Python can import together.

In this project:

- `main.py` is a script.
- `src/mythic_edge_parser/app/runner.py` is a module.
- `src/mythic_edge_parser/` is a package.

### Function and Method

- A **function** is a named block of reusable behavior.
- A **method** is a function attached to a class.

Examples:

- `include_event(event)` is a function.
- `summary.to_match_log_row()` is a method.

### Class and Object

- A **class** is a blueprint.
- An **object** is a real instance built from that blueprint.

Example:

- `MatchSummary` is a class.
- `summary = MatchSummary(match_id="...")` creates an object.

### Dictionary and List

- A **dictionary** stores named values like `{ "match_id": "...", "game_wins": 2 }`.
- A **list** stores ordered items like `["card1", "card2", "card3"]`.

MTGA payloads are mostly dictionaries.

### JSON

**JSON** is a text format for structured data. It looks a lot like Python dictionaries and lists. MTGA logs often contain JSON inside bigger blocks of text. Google Sheets webhook payloads also use JSON.

### State

**State** means "what the program currently remembers."

For example:

- current match ID
- current game number
- current player team
- mulligan count so far
- whether a match summary has already been posted

This project keeps a lot of live state in `state.py`.

### Event-Driven Design

An **event** is "something that happened."

Examples:

- match started
- mulligan clicked
- sideboarding entered
- rank snapshot received
- game ended

Mythic Edge is event-driven because the log keeps producing events over time, and the program reacts to them as they arrive.

### Async

**Async** code is code designed for things that wait around a lot.

This project waits for:

- file updates
- new log entries
- webhook calls

`asyncio` lets the program keep listening without freezing.

## The Folder Structure In Plain English

- `main.py`
  The main start button for the parser.
- `live_print_filtered_v11_match_summary.py`
  An old filename kept around so older shortcuts still work.
- `sync_tier_buckets.py`
  A separate start button for refreshing workbook tier data.
- `src/mythic_edge_parser/`
  The real Python package.
- `src/mythic_edge_parser/log/`
  Low-level file reading and log entry grouping.
- `src/mythic_edge_parser/parsers/`
  Functions that recognize specific MTGA message shapes.
- `src/mythic_edge_parser/app/`
  The high-level "business logic" of the project.
- `tools/auto_launcher/`
  The desktop launcher UI.
- `tools/google_apps_script/`
  The Google Sheets webhook script.
- `tools/scryfall_parser/`
  A separate utility for downloading Scryfall Oracle card data.
- `data/`
  Output, snapshots, and other generated files.
- `tests/`
  Safety checks for the code.
- `examples/`
  Older versions and historical reference scripts.

## The System Walkthrough

If you launch the parser and then play a match, this is what happens:

1. `main.py` starts the app.
2. `runner.py` performs startup checks.
3. `stream.py` opens `Player.log` and watches it from the end.
4. `tailer.py` reads new text from the file.
5. `entry.py` groups raw lines into log entries.
6. `router.py` asks the parser modules whether they recognize each entry.
7. A parser returns structured events such as `GameStateEvent` or `ClientActionEvent`.
8. `transforms.py` decides which events are worth keeping.
9. `state.py` updates the match summary in memory.
10. `outputs.py` writes local JSONL files and optionally POSTs rows to Google Sheets.
11. `Code.gs` receives those rows and writes them into the workbook.

That full chain is the heart of the project.

---

# Script-By-Script Guide

## Root Entry Scripts

### `main.py`

**Global job:** start the main parser in the simplest possible way.

This file does almost no business logic. It mainly:

- figures out where `src/` lives
- makes sure Python can import the package
- imports the real app runner
- starts the async main loop

There are no local functions in this file. Its main purpose is to be easy to run.

### `live_print_filtered_v11_match_summary.py`

**Global job:** act as a compatibility wrapper for an older filename.

This file exists so old shortcuts or habits still work. It simply imports `run_parser` from `main.py` and starts it.

### `sync_tier_buckets.py`

**Global job:** refresh tier-source data without running the full match parser.

This is the "just update my meta deck buckets" script. It loads the same package path setup as `main.py`, then calls `sync_tier_sources`.

## Package Root

### `src/mythic_edge_parser/__init__.py`

**Global job:** make the package pleasant to import.

This file re-exports important names like `MtgaEventStream`, `StreamError`, and the event classes so another script can say `from mythic_edge_parser import MtgaEventStream`.

### `src/mythic_edge_parser/app/__init__.py`

**Global job:** expose the app runner without forcing a circular import.

It defines one small wrapper:

- `main()`
  Imports `runner.main` only when called, then returns it. This lazy import keeps the package boundary cleaner.

## Event Definitions

### `src/mythic_edge_parser/events.py`

**Global job:** define the vocabulary of the system.

This file says what kinds of structured events exist.

Important classes:

- `PerformanceClass`
  A category that says how urgently an event matters.
- `EventMetadata`
  Stores the timestamp, raw bytes, and a SHA-256 hash of the raw bytes.
- `BaseEvent`
  The common shape shared by all event classes.
- `GameStateEvent`, `ClientActionEvent`, `MatchStateEvent`, `GameResultEvent`, `RankEvent`, and others
  Specific event types used by the rest of the app.

Important method:

- `EventMetadata.__post_init__(self)`
  Automatically computes `raw_bytes_hash` after the object is created.

## Event Bus

### `src/mythic_edge_parser/event_bus.py`

**Global job:** let producers and consumers pass events around safely.

This is the internal message channel of the app.

Classes and methods:

- `Subscriber`
  A simple wrapper around an async queue.
- `Subscriber.recv(self)`
  Waits for the next event. Returns `None` when the bus is shutting down.
- `EventBus.__init__(self, capacity)`
  Creates the event bus and queue list.
- `EventBus.with_default_capacity(cls)`
  Convenience constructor that uses the default queue size.
- `EventBus.subscribe(self)`
  Creates and returns a new subscriber.
- `EventBus.publish(self, event)`
  Sends one event to every active subscriber.
- `EventBus.close(self)`
  Sends a sentinel value so subscribers know the stream has ended.

## Log Reading Layer

### `src/mythic_edge_parser/log/entry.py`

**Global job:** turn raw text lines into higher-level log entries.

Classes and functions:

- `EntryHeader`
  Enum describing what kind of log header a line has.
- `LogEntry`
  A small object with two fields: `header` and `body`.
- `LineBuffer.__init__(self)`
  Starts an empty buffer.
- `LineBuffer.feed(self, text)`
  Takes raw text, splits it into lines, groups lines into entries, and returns finished entries.
- `LineBuffer.flush(self)`
  Forces the current partial entry to become a final entry.
- `classify_line_header(line)`
  Looks at one line and decides which header type it belongs to.

### `src/mythic_edge_parser/log/tailer.py`

**Global job:** watch the log file as it changes.

Classes and methods:

- `TailerError`
  Custom exception for file-tail problems.
- `TailBatch`
  A tiny container for `entries` plus a `rotated` flag.
- `FileTailer.__init__(self, path)`
  Stores the path and initializes offsets and counters.
- `FileTailer.seconds_without_structured_headers(self)`
  Returns how long the tailer has gone without seeing structured MTGA headers.
- `FileTailer.open_from_start(cls, path)`
  Opens a file and reads from byte `0`.
- `FileTailer.open_from_end(cls, path)`
  Opens a file and starts at the end so old history is skipped.
- `FileTailer.poll(self)`
  Waits briefly, reads any newly added text, handles file rotation, and returns a `TailBatch`.

## Router Layer

### `src/mythic_edge_parser/router.py`

**Global job:** decide which parser should handle a log entry.

Classes and functions:

- `RouterStats`
  Keeps simple counts such as how many entries were routed successfully.
- `Router.__init__(self)`
  Creates a router with empty stats.
- `Router.stats(self)`
  Returns the current stats object.
- `Router.reset(self)`
  Clears the stats.
- `Router.route(self, entry)`
  Extracts a timestamp, sends the entry through parser functions, updates stats, and returns structured events.
- `extract_timestamp(body)`
  Pulls a timestamp from the first line of a log entry.
- `dispatch_to_parsers(entry, timestamp)`
  Tries the parser modules in order and returns the first successful result.

## Stream Layer

### `src/mythic_edge_parser/stream.py`

**Global job:** connect the tailer, router, and event bus into one live pipeline.

Classes and methods:

- `StreamError`
  High-level stream startup error.
- `MtgaEventStream.start(cls, log_path)`
  Opens the tailer, creates the event bus, starts the background pipeline task, and returns the stream plus a subscriber.
- `MtgaEventStream.shutdown(self)`
  Stops the stream and waits for the pipeline task to finish.

Important behavior:

- the stream now starts from the end of the file, not the beginning
- malformed routed entries get written to the bad-entry diagnostics file instead of silently killing the session

## Utility and Privacy Helpers

### `src/mythic_edge_parser/util.py`

**Global job:** hold a few small generic helpers.

- `compress_log(text)`
  Gzip-compresses a log string.
- `content_hash(content)`
  Returns a SHA-256 hash of some bytes.

### `src/mythic_edge_parser/sanitize.py`

**Global job:** redact sensitive information from logs.

- `scrub_raw_log(text)`
  Replaces tokens, account IDs, display names, and local usernames with redacted placeholders.

## Parser Helper Module

### `src/mythic_edge_parser/parsers/api_common.py`

**Global job:** provide shared helper functions for parser modules.

- `find_json_value(text)`
  Scans a larger text blob and returns the first JSON object or array it can decode.
- `parse_json_from_body(body, context="")`
  Pulls structured JSON out of a log body and returns it as a dictionary.
- `is_api_request(body, name)`
  Checks whether a body looks like a specific API request.
- `is_api_response(body, name)`
  Checks whether a body looks like a specific API response.
- `normalize_int_list(value)`
  Converts a mixed list into a clean list of integers.

## Specific Parser Modules

### `src/mythic_edge_parser/parsers/metadata.py`

**Global job:** detect whether detailed logging is enabled.

- `try_parse(entry, timestamp)`
  Returns a `DetailedLoggingStatusEvent` when the entry says detailed logs are enabled or disabled.

### `src/mythic_edge_parser/parsers/gre.py`

**Global job:** parse GRE game-state traffic, which is some of the most important match data.

- `try_parse(entry, timestamp)`
  Detects GRE game-state messages and can emit both `GameStateEvent` and `GameResultEvent`.
- `build_game_state_payload(message, gsm)`
  Builds a clean payload dictionary for a game-state event.
- `is_game_over(gsm)`
  Checks whether the GRE state says the game has ended.
- `build_game_result_payload(gsm)`
  Builds a payload that captures who won, what the result type was, and why.

### `src/mythic_edge_parser/parsers/client_actions.py`

**Global job:** parse actions the client sends back to the game engine.

- `try_parse(entry, timestamp)`
  Recognizes client-to-GRE messages and turns them into `ClientActionEvent`s.
- `extract_inner_payload(parsed)`
  Pulls the real message payload out of the outer wrapper.
- `build_mulligan(inner, envelope)`
  Builds a normalized mulligan payload.
- `build_select_n(inner, envelope)`
  Builds a normalized "pick N options" payload.
- `build_submit_deck(inner, envelope)`
  Builds a normalized submitted-deck payload.

### `src/mythic_edge_parser/parsers/match_state.py`

**Global job:** parse the overall match-room state.

- `try_parse(entry, timestamp)`
  Recognizes match-room state updates and creates a `MatchStateEvent`.
- `build_payload(state_event)`
  Normalizes the room state into match ID, players, result list, and match-complete information.

### `src/mythic_edge_parser/parsers/rank.py`

**Global job:** parse rank snapshots.

- `try_parse(entry, timestamp)`
  Recognizes the combined-rank API response and builds a `RankEvent`.

### `src/mythic_edge_parser/parsers/session.py`

**Global job:** parse login/session lifecycle information.

- `try_parse(entry, timestamp)`
  Detects account updates, authentication responses, and logout events, then returns a `SessionEvent`.

### `src/mythic_edge_parser/parsers/event_lifecycle.py`

**Global job:** parse event-queue lifecycle markers like entering pairing or claiming prizes.

- `try_parse(entry, timestamp)`
  Matches known event-lifecycle patterns and returns an `EventLifecycleEvent`.

### `src/mythic_edge_parser/parsers/collection.py`

**Global job:** parse collection snapshots from `StartHook`.

- `try_parse(entry, timestamp)`
  Returns a `CollectionEvent` if the body contains `PlayerCards`.

### `src/mythic_edge_parser/parsers/inventory.py`

**Global job:** parse inventory snapshots from `StartHook`.

- `try_parse(entry, timestamp)`
  Returns an `InventoryEvent` if the body contains `InventoryInfo`.

## App Layer

### `src/mythic_edge_parser/app/config.py`

**Global job:** hold configuration and environment-driven paths/flags.

This file does not define functions. It mainly defines constants such as:

- which event types should be kept
- where `Player.log` lives
- where local outputs should be stored
- whether raw rows, match-log rows, or tier sync are enabled

### `src/mythic_edge_parser/app/diagnostics.py`

**Global job:** make troubleshooting real instead of guesswork.

- `setup_runtime_logging()`
  Configures a shared logger that writes to both the console and a daily runtime log file.
- `get_logger(name=None)`
  Returns the shared logger or a namespaced child logger.
- `current_runtime_log_path()`
  Returns the path to the active runtime log file.
- `record_failed_post(row, exc, response_text="")`
  Saves a failed webhook POST to a daily JSONL file.
- `record_event_failure(event, exc, stage)`
  Saves a failed event-processing attempt to a JSONL file.
- `record_router_failure(entry, exc)`
  Saves a failed routing/parsing attempt to a JSONL file.
- `_append_jsonl_record(root, prefix, record)`
  Internal helper that appends one diagnostics record to a daily file.
- `_daily_folder_name(dt)`
  Converts a date into the project’s daily folder format.
- `_safe_json_value(value)`
  Converts objects into JSON-safe values for diagnostics storage.

### `src/mythic_edge_parser/app/extractors.py`

**Global job:** pull important facts out of messy payload dictionaries.

- `_safe_local_player(players)`
  Returns the local player safely, even if the expected index is missing.
- `_extract_turn_info(payload)`
  Pulls out match ID, game number, turn number, active player, phase, step, and stage from a game-state payload.
- `_extract_starting_player_from_client_action(payload)`
  Searches several possible keys to find which player chose to start.
- `_infer_scope_label(scope_value)`
  Normalizes scope values like `MatchScope_Game` into plain labels like `Game`.
- `_extract_game_result_identity(payload, context)`
  Pulls out the identity of a game result: match, game, winner, result type, and reason.
- `_has_match_scope_result(payload)`
  Checks whether a result payload also includes a match-level result.
- `_event_datetime(event)`
  Returns a safe `datetime` for an event.
- `_safe_iso(event)`
  Returns a safe ISO timestamp string for an event.

### `src/mythic_edge_parser/app/models.py`

**Global job:** define the clean in-memory summary objects.

#### `GameSummary`

- `play_draw(self, player_team)`
  Returns `Play` or `Draw` from the local player’s perspective.
- `result_for_player(self, player_team)`
  Returns `W` or `L` for the local player.
- `has_summary_data(self)`
  Says whether this game has enough data to be worth exporting.
- `to_debug_dict(self, player_team)`
  Builds a human-readable dictionary of the game.
- `to_sheet_row(self, match)`
  Converts one game into a sheet-ready row.

#### `_default_games()`

- Creates three empty `GameSummary` objects for games 1, 2, and 3.

#### `MatchSummary`

- `touch(self, timestamp)`
  Updates first/last seen timestamps.
- `game(self, game_number)`
  Returns the `GameSummary` for a given game number.
- `set_game_winner(self, game_number, winner_team)`
  Stores who won a game.
- `set_game_starting_player(self, game_number, starting_player)`
  Stores who was on the play for a game.
- `set_game_mulligans(self, game_number, mulligans)`
  Stores mulligan count for a game.
- `opponent_team(self)`
  Returns the opponent’s team ID.
- `effective_starting_player(self, game_number)`
  Uses explicit data if present; otherwise infers the next game’s starter from the previous game result.
- `game_play_draw(self, game_number)`
  Returns `Play` or `Draw` for a specific game.
- `game_wins(self)`
  Counts how many games the local player won.
- `game_losses(self)`
  Counts how many games the local player lost.
- `match_wl(self)`
  Returns overall match result as `W` or `L`.
- `total_mulligans(self)`
  Adds mulligans across games.
- `total_games(self)`
  Counts completed games.
- `match_win_flag(self)`
  Returns `1` for a win, `0` for a loss, or blank if unknown.
- `game_win_rate(self)`
  Returns game win rate as a fraction.
- `is_ready(self)`
  Says whether the summary is complete enough to export.
- `rank_bucket(self)`
  Converts detailed rank information into a workbook-friendly label like `Mythic %`.
- `played_date(self)`
  Returns the match date.
- `to_debug_dict(self)`
  Builds a verbose debugging view of the whole match.
- `to_sheet_row(self)`
  Converts the match into a `MatchSummary` row for Sheets.
- `to_match_log_row(self)`
  Converts the match into the workbook-shaped `MatchLogRow`.
- `to_game_sheet_rows(self)`
  Exports one row per game when game-level data exists.

### `src/mythic_edge_parser/app/state.py`

**Global job:** hold the parser’s live memory and build summaries over time.

This is one of the most important files in the project.

- `_context_key(match_id, game_number)`
  Builds a stable key for de-duplication.
- `_next_mulligan_count(match_id, game_number, decision)`
  Tracks how many mulligans have happened for a specific game.
- `_ensure_match_summary(match_id)`
  Creates a `MatchSummary` if one does not already exist.
- `_set_first_last(summary, event)`
  Updates the summary’s first and last timestamps.
- `_update_match_summary(event)`
  The heart of the state system. Reads incoming events and updates the live match summary.
- `_match_summary_ready(summary)`
  Small helper that asks whether a summary is ready to export.
- `build_match_summary_row(match_id)`
  Returns a sheet row if the match summary is ready.
- `build_game_summary_rows(match_id)`
  Returns per-game summary rows.
- `build_match_log_row(match_id)`
  Returns the workbook-shaped match log row.

### `src/mythic_edge_parser/app/transforms.py`

**Global job:** decide what to keep and how to format it.

- `_base_sheet_row(event)`
  Builds the common base shape for raw event rows sent to Sheets.
- `include_event(event)`
  Decides whether an event is important enough to keep at all.
- `to_serializable(event)`
  Converts an event into a JSON-safe dictionary for local JSONL storage.
- `to_sheet_rows(event)`
  Converts one raw event into zero, one, or multiple raw sheet rows.
- `summarize(event)`
  Builds one short console line describing an event.

### `src/mythic_edge_parser/app/outputs.py`

**Global job:** write data out of the app.

- `post_row_to_google_sheets(row)`
  Sends one row to the webhook. Returns `True` on success and writes failed rows to disk on failure.
- `_daily_folder_name(event_dt)`
  Builds the day-folder name like `04_18_26`.
- `_ensure_daily_log_path(event_dt)`
  Finds or creates the JSONL file path for a given day.
- `append_local_jsonl(local_row, event_dt)`
  Appends one serialized row to the local daily JSONL log.

### `src/mythic_edge_parser/app/tier_sync.py`

**Global job:** refresh tier-source deck data from outside websites.

#### Data classes

- `TierRecord.to_sheet_row(self)`
  Converts one tier-source record into a row dictionary.
- `TierSyncResult.records(self)`
  Returns the snapshot’s rows.
- `TierSyncResult.ok_rows(self)`
  Counts the rows that are usable deck rows.
- `TierSyncResult.available_sources(self)`
  Counts how many sources successfully produced deck rows.
- `TierSyncResult.summary_line(self)`
  Builds a one-line status summary.

#### Functions

- `sync_tier_sources(post_to_webhook=True)`
  Runs the full tier refresh, writes a local snapshot, and optionally posts it to the webhook.
- `build_tier_snapshot_payload()`
  Builds the full workbook-ready snapshot payload.
- `write_tier_snapshot(snapshot)`
  Saves the snapshot JSON locally.
- `load_normalization_overrides()`
  Loads the deck-name alias table from disk.
- `_scrape_mtggoldfish(session, refreshed_at, overrides)`
  Scrapes MTGGoldfish and returns tier records.
- `_scrape_mtgtop8(session, refreshed_at, overrides)`
  Scrapes MTGTop8 and returns tier records.
- `_scrape_untapped(session, refreshed_at, overrides)`
  Tries to scrape Untapped and records an unavailable status if the real rows are not public.
- `_build_ok_record(source_key, refreshed_at, raw_name, meta_share_pct, tier_letter, overrides)`
  Builds a successful tier record.
- `_build_unavailable_record(source_key, refreshed_at, notes)`
  Builds a placeholder record that explains why a source is unavailable.
- `normalize_archetype_name(source_key, raw_name, overrides)`
  Maps raw site names to your preferred canonical deck names.
- `classify_tier_bucket(meta_share_pct, tier_letter)`
  Converts percentages or letter tiers into `Tier 1`, `Tier 2`, `Tier 3`, or `Fringe`.
- `_parse_percent(text)`
  Pulls a percent number out of a text string.
- `_clean_text(text)`
  Trims and normalizes whitespace.
- `_normalize_key(text)`
  Creates a case-insensitive key for alias matching.
- `_write_json(path, payload)`
  Writes JSON to disk.

### `src/mythic_edge_parser/app/runner.py`

**Global job:** run the whole application.

This is the real operational center of the parser.

- `_startup_issues()`
  Performs startup checks such as log-path existence, webhook validity, and tier-normalization JSON readability.
- `main()`
  Initializes diagnostics, runs preflight checks, optionally refreshes tier buckets, starts the stream, processes events forever, writes outputs, and captures event-level failures.

## Command-Line Tool

### `src/mythic_edge_parser/bin/scrub.py`

**Global job:** expose the log scrubber as a command-line program.

- `main()`
  Reads text from standard input, scrubs it, writes the cleaned version, and returns an exit code.

## User-Facing Tools

### `tools/auto_launcher/manasight_launcher_auto.py`

**Global job:** give you a simple desktop UI for running the parser.

Top-level helpers:

- `load_settings()`
  Loads saved launcher settings from JSON.
- `save_settings(data)`
  Writes launcher settings to JSON.
- `is_process_running(process_name)`
  Checks whether MTGA is currently running.

`LauncherApp` methods:

- `__init__(self)`
  Creates the window, state variables, and background timers.
- `_build_ui(self)`
  Builds the whole Tkinter interface.
- `browse_project_root(self)`
  Lets the user choose a project folder.
- `browse_script_file(self)`
  Lets the user choose which script to run.
- `browse_player_log(self)`
  Lets the user choose `Player.log`.
- `refresh_scripts(self)`
  Scans the project folder for runnable parser scripts.
- `persist_settings(self)`
  Saves the current UI settings.
- `_validate(self)`
  Checks that the chosen paths exist and nothing is already running.
- `_sheet_posting_enabled(self)`
  Returns whether any sheet-posting mode is turned on.
- `start_script(self)`
  Validates settings, warns about blank webhooks, sets environment variables, and launches the parser subprocess.
- `_reader_thread(self)`
  Reads live output from the running subprocess.
- `_drain_log_queue(self)`
  Moves queued log lines into the launcher text box.
- `_watch_mtga_loop(self)`
  Monitors whether MTGA opens or closes.
- `_prompt_start_for_mtga_session(self)`
  Asks whether to start the parser when MTGA is detected.
- `_log(self, message)`
  Appends one line to the launcher log window.
- `stop_script(self)`
  Stops the running subprocess.
- `open_output_folder(self)`
  Opens the match-log output folder in the file explorer.
- `on_close(self)`
  Saves settings and handles shutdown behavior when the window closes.

### `tools/scryfall_parser/scryfall_parser.py`

**Global job:** download Scryfall Oracle data and filter it by format legality.

- `download_latest_oracle_file()`
  Downloads the latest Oracle bulk data file into `data/oracle_data/`.
- `filter_legal_cards(oracle_path, fmt_key)`
  Filters the Oracle data by format legality and writes both JSON and CSV outputs.
- `main()`
  Prompts the user for a format, downloads the file, and filters it.

## Google Sheets Support Script

### `tools/google_apps_script/Code.gs`

**Global job:** receive webhook posts and update the workbook.

Think of this file as the "Google Sheets half" of Mythic Edge.

Core functions:

- `onOpen()`
  Adds the custom `MTGA Tools` menu to the workbook.
- `getWorkbook_()`
  Opens the target spreadsheet by ID.
- `getSheet_(ss, name)`
  Returns a sheet by name, or `null`.
- `getSheetOrThrow_(ss, name)`
  Returns a sheet by name, or throws an error if it is missing.
- `getHeaderMap_(sheet, headerRow)`
  Builds a dictionary from header names to column numbers.
- `getMatchLogHeaderMap_(sheet)`
  Special case of `getHeaderMap_` for the Match Log tab.
- `findLastNonBlankRowInColumn_(sheet, col, startRow)`
  Finds the last used row in a specific column.
- `getNextMatchLogAppendRow_(sheet)`
  Chooses the next row where a new Match Log entry should go.
- `doPost(e)`
  Main webhook entry point. Reads JSON, decides what kind of payload it is, writes it to the right place, and returns a JSON response.
- `buildSummaryRow_(data)`
  Converts a `MatchSummary` payload into a summary-sheet row.
- `buildArchiveRow_(data)`
  Converts a raw event payload into an archive row.
- `upsertMatchLogFromPayload_(ss, data)`
  Ensures the match has a row in `Match Log` and updates it.
- `buildMatchLogFieldMap_(data)`
  Maps parser payload fields to workbook columns.
- `writeMatchLogFields_(sheet, row, fieldMap)`
  Writes mapped values into a Match Log row.
- `applyMatchLogDefaults_(sheet, row, fieldMap)`
  Fills default values like `OK` or `Yes` where needed.
- `setIfBlank_(sheet, row, col, value)`
  Writes a value only if the target cell is blank.
- `firstDefined_(...values)`
  Returns the first non-blank value.
- `firstDefinedNumber_(...values)`
  Returns the first numeric value.
- `computeTotalGames_(gamesWon, gamesLost)`
  Adds wins and losses.
- `computeGameWinRate_(gamesWon, totalGames)`
  Computes game win percentage.
- `deriveMatchWinFlag_(matchWin)`
  Converts `W` or `L` into `1` or `0`.
- `parseDateOrBlank_(value)`
  Converts a value into a Google Sheets date if possible.
- `boolToYesNo_(value)`
  Converts booleans or truthy text into `Yes` / `No`.
- `deriveMyRank_(data)`
  Builds the workbook-style rank label.
- `deriveGameResult_(winnerTeam, playerTeam)`
  Converts winning team into `W` or `L` for the local player.
- `jsonResponse_(payload)`
  Returns JSON from the web app.
- `logDebug_(debugSheet, status, matchId, data, destination)`
  Appends a row to `Webhook Debug`.

Tier helper functions:

- `prepareTierSourceHelpers()`
  Sets up the hidden support tab and workbook controls for tier data.
- `upsertTierSourceSnapshot_(ss, data)`
  Rewrites the tier-source data tab from a webhook snapshot.
- `ensureTierSourceDataSheet_(ss)`
  Creates the hidden support tab if needed.
- `rewriteTierSourceData_(sheet, records)`
  Replaces the support tab contents with fresh records.
- `buildTierSourceDataRow_(record)`
  Converts one tier record into a sheet row.
- `configureHelperTableTierSourceControls_(helperSheet, tierSheet)`
  Builds the dropdown and formulas in `Helper Table`.
- `getUniqueTierSourceLabels_(sheet, lastRow)`
  Extracts the distinct source labels.
- `resetTierBucketSpillArea_(helperSheet)`
  Rebuilds the tier bucket formulas, including `Other / Unknown`.
- `hideSheetIfSafe_(ss, sheet)`
  Hides a support sheet if it is safe to do so.

Workbook cleanup functions:

- `prepareWorkbookForPhase1()`
  Hides old tabs and freezes parser-managed columns.
- `freezeParserManagedMatchLogColumns_(sheet)`
  Replaces formulas with values in parser-managed columns.
- `hideLegacyMtgaTabs_(ss)`
  Hides older helper/archive tabs.
- `ensureMatchLogRowForMatchId_(ss, matchId)`
  Finds or creates the Match Log row for a match.

Test helpers:

- `testMatchLogWrite()`
  Writes a fake Match Log row for testing.
- `testTierSourceWrite()`
  Writes fake tier-source rows for testing.

## Historical Example Scripts

### `examples/live_print.py`

**Global job:** a minimal "just print live events" example.

- `main()`
  Starts the stream and prints events as they arrive.

### `examples/live_print_filtered_v8.py`
### `examples/live_print_filtered_v9.py`
### `examples/live_print_filtered_v10_fixed.py`

**Global job:** older all-in-one parser scripts from before the codebase was split into clean modules.**

These historical files combine many behaviors that are now separated into:

- `extractors.py`
- `state.py`
- `transforms.py`
- `outputs.py`
- `runner.py`

Their functions have the same broad jobs as the modern modular versions:

- `_safe_local_player`, `_extract_turn_info`, `_extract_starting_player_from_client_action`
  Old helper functions that later moved into `extractors.py`.
- `_context_key`, `_next_mulligan_count`, `_update_context`
  Old state-tracking helpers that later moved into `state.py`.
- `include_event`, `to_serializable`, `summarize`, `_base_sheet_row`, `to_sheet_rows`
  Older transformation and export helpers that later moved into `transforms.py`.
- `post_row_to_google_sheets`, `_event_datetime`, `_daily_folder_name`, `_ensure_daily_log_path`
  Older output helpers that later moved into `outputs.py`.
- `main()`
  Old monolithic runtime loop that later became `runner.py`.

`v9.py` also contains `_build_game_result_rows`, which was an earlier attempt to create explicit game-result rows.

## Test Files

The test suite is part of the project’s learning story because it shows what the code is trying to guarantee.

### `tests/test_app_config.py`

- `test_default_match_logs_root_uses_data_folder(monkeypatch)`
  Verifies that config paths default to the repo’s `data/` folders.

### `tests/test_app_extractors.py`

- `test_extract_starting_player_from_nested_raw_client_action()`
  Verifies that starting-player extraction still works when the useful data is nested.

### `tests/test_app_models.py`

- `test_match_summary_sheet_row_matches_workbook_shape()`
  Verifies `MatchSummary` export shape.
- `test_game_summary_rows_exist_for_future_exports()`
  Verifies per-game export rows.
- `test_match_log_row_matches_first_phase_workbook_shape()`
  Verifies the workbook-shaped Match Log export.
- `test_missing_later_game_starting_player_is_inferred_from_previous_game_result()`
  Verifies the play/draw fallback rule.
- `test_explicit_starting_player_beats_inferred_starting_player()`
  Verifies that real data wins over inferred data.

### `tests/test_app_outputs.py`

- `_FakeHttpFailureResponse.raise_for_status(self)`
  Test helper that simulates an HTTP failure.
- `test_failed_webhook_posts_are_saved_locally(tmp_path, monkeypatch)`
  Verifies that failed posts land in the diagnostics file.

### `tests/test_entrypoints.py`

- `test_legacy_entrypoint_delegates_to_modular_main()`
  Verifies that the legacy filename still points at the real parser.

### `tests/test_log_entry_headers.py`

- `test_classify_line_header_handles_utc_log_prefix()`
  Verifies that UTC-style numeric prefixes do not break header recognition.

### `tests/test_match_summary_from_match_state.py`

- `test_match_state_final_results_populate_match_summary()`
  Verifies that final match-state result lists correctly build summaries.

### `tests/test_parsers.py`

- `test_metadata_parse()`
  Verifies metadata parsing.
- `test_match_state_parse()`
  Verifies match-state parsing.
- `test_client_submit_deck_parse()`
  Verifies deck-submission parsing.
- `test_gre_game_over_emits_game_state_and_game_result()`
  Verifies GRE game-over parsing.

### `tests/test_sanitize.py`

- `test_scrub_removes_bearer_and_user_path()`
  Verifies that the scrubber removes sensitive strings.

### `tests/test_scryfall_tool.py`

- `test_scryfall_tool_writes_to_repo_data_folder()`
  Verifies that the Scryfall tool writes into the repo, not somewhere external.

### `tests/test_tailer.py`

- `test_open_from_end_skips_existing_log_history(tmp_path)`
  Verifies the fix that prevents stale startup rows.

### `tests/test_tier_sync.py`

- `_FakeResponse.__init__(self, text)`
  Test helper that stores fake HTML.
- `_FakeResponse.raise_for_status(self)`
  Fake success status method.
- `_FakeSession.__init__(self, html)`
  Fake requests session that stores canned HTML.
- `_FakeSession.get(self, url, timeout)`
  Returns the canned fake response.
- `test_classify_tier_bucket_supports_percent_thresholds()`
  Verifies percentage-based tier mapping.
- `test_classify_tier_bucket_supports_letter_tiers()`
  Verifies letter-tier mapping.
- `test_normalize_archetype_name_uses_source_specific_override()`
  Verifies alias overrides.
- `test_scrape_mtggoldfish_extracts_archetypes_and_meta_share()`
  Verifies MTGGoldfish scraping.
- `test_scrape_mtgtop8_extracts_breakdown_rows()`
  Verifies MTGTop8 scraping.
- `test_scrape_untapped_reports_unavailable_when_public_html_is_premium_locked()`
  Verifies the graceful Untapped fallback.

---

# How To Read This Project As A Beginner

If you want to learn coding from this project, I would read it in this order:

1. `main.py`
   This shows how the program starts.
2. `app/runner.py`
   This shows the top-level workflow.
3. `app/models.py`
   This shows what the program is trying to build.
4. `app/state.py`
   This shows how the program remembers what is happening.
5. `app/transforms.py`
   This shows how the program chooses what matters.
6. `app/extractors.py`
   This shows how the program digs specific values out of messy data.
7. `stream.py`, `router.py`, `parsers/`
   This shows how raw logs become structured events.
8. `tools/auto_launcher/manasight_launcher_auto.py`
   This shows how a user-facing GUI starts a subprocess.
9. `tools/google_apps_script/Code.gs`
   This shows the Google Sheets half of the pipeline.

## A Good Beginner Exercise

Try answering these questions by reading the code:

1. Where does the parser first learn the `match_id`?
2. Where does it decide a log entry is important enough to keep?
3. Where does it infer `Play` or `Draw`?
4. Where does it decide the row is ready to send to Sheets?
5. Where does it save failures now if the webhook breaks?

If you can answer those five questions, you are already reading real software, not just toy examples.

## What To Be Proud Of

This is not a tiny beginner script anymore.

It has:

- a streaming pipeline
- modular parsers
- stateful summary building
- Google Sheets integration
- a GUI launcher
- web scraping helpers
- diagnostics
- tests

That is a serious personal software project.

## Final Mental Model

If you forget everything else, remember this:

- `log/` reads
- `parsers/` recognize
- `events.py` names things
- `stream.py` moves things
- `state.py` remembers
- `models.py` defines the clean output
- `transforms.py` decides what to keep
- `outputs.py` writes
- `runner.py` coordinates
- `Code.gs` finishes the trip into Google Sheets

That is the whole project in one sentence.
