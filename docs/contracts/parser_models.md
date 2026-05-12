# Parser Models Module Contract

Problem representation: https://github.com/Tahjali11/Mythic-Edge/issues/2

Role docs:

- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Status: contract draft based on GitHub issue #2, the current `src/mythic_edge_parser/app/models.py` code, and existing tests. Issue #2 was read through the authenticated GitHub CLI in this local environment; it currently has no comments.

## Module

`src/mythic_edge_parser/app/models.py`

This module owns the in-memory match and game summary shapes and the serializer methods that turn parser-managed facts into workbook-facing rows and runtime-history payloads.

Plain English: this file is where already-interpreted match/game facts become stable dictionaries for the rest of the pipeline. It should not parse raw MTGA log text, post webhooks, edit Google Sheets, or decide workbook formulas.

## Owning Layer

Primary truth layer: parser and state interpretation.

The model objects are parser-owned truth carriers for normalized match and game facts after `state.py` has interpreted raw MTGA events. Downstream layers may transport, store, or display these values, but should not become the truth owner for match result, game result, play/draw, mulligan count, opening hand, queue type, or rank bucket.

## Files Owned By This Contract

- `src/mythic_edge_parser/app/models.py`

Files that depend on this contract:

- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `tools/google_apps_script/Code.gs`
- `tests/test_app_models.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_sheet_schema.py`
- parser replay/regression tests that snapshot `MatchSummary.to_sheet_row()`

## Public Interface

The public interface means the functions, classes, fields, and row keys other code is allowed to depend on.

### Constants

- `GAME_NUMBERS = (1, 2, 3)`
  - Observed behavior: every `MatchSummary` gets exactly three game slots.
  - Required guarantee: serializer output remains stable for game 1, game 2, and game 3 unless a future workbook-schema contract changes this.

- `MYTHIC_RANK_LABEL = "Mythic"`
  - Observed behavior: `rank_bucket()` uses this label to decide Mythic split buckets.

- `MTGA_QUEUE_TYPE_MAP`
  - Observed behavior: known MTGA match-win-condition strings normalize to labels such as `Best of 3`, `Best of 1`, and `Single Elimination`.

### `GameSummary`

Constructor fields:

- `game_number: int`
- `winner_team: Any = ""`
- `starting_player: Any = ""`
- `mulligans: int = 0`
- `opening_hand: list[str]`
- `mulliganed_away: list[str]`
- `first_event_time: str = ""`
- `last_event_time: str = ""`
- `turn_count: int = 0`

Public methods:

- `touch(timestamp: str) -> None`
- `set_turn_count(turn_number: Any) -> None`
- `duration_seconds() -> int | str`
- `opening_hand_size() -> int | str`
- `play_draw(player_team: Any) -> str`
- `result_for_player(player_team: Any) -> str`
- `set_opening_hand(cards: list[str]) -> None`
- `add_mulliganed_away(cards: list[str]) -> None`
- `has_summary_data() -> bool`
- `to_debug_dict(player_team: Any) -> dict[str, Any]`
- `to_sheet_row(match: MatchSummary) -> dict[str, Any]`
- `to_game_log_row(match: MatchSummary) -> dict[str, Any]`

### `MatchSummary`

Constructor fields:

- `match_id: str`
- `first_event_time: str = ""`
- `last_event_time: str = ""`
- `player_team: Any = ""`
- `match_winner_team: Any = ""`
- `match_result_type: str = ""`
- `match_result_reason: str = ""`
- `sideboarding_entered: bool = False`
- `submit_deck_seen: bool = False`
- `constructed_rank: str = ""`
- `constructed_class: str = ""`
- `constructed_level: str = ""`
- `constructed_percentile: Any = None`
- `constructed_rank_source: str = ""`
- `event_id: str = ""`
- `super_format: str = ""`
- `match_win_condition: str = ""`
- `games: dict[int, GameSummary]`

Public methods and properties:

- `touch(timestamp: str) -> None`
- `game(game_number: Any) -> GameSummary | None`
- `set_game_winner(game_number: Any, winner_team: Any) -> None`
- `set_game_starting_player(game_number: Any, starting_player: Any) -> None`
- `set_game_mulligans(game_number: Any, mulligans: int) -> None`
- `set_game_opening_hand(game_number: Any, opening_hand: list[str]) -> None`
- `add_game_mulliganed_away(game_number: Any, cards: list[str]) -> None`
- `touch_game(game_number: Any, timestamp: str) -> None`
- `set_game_turn_count(game_number: Any, turn_number: Any) -> None`
- `ingest_game_info(game_info: dict[str, Any]) -> None`
- `opponent_team() -> Any`
- `effective_starting_player(game_number: int) -> Any`
- `game_play_draw(game_number: int) -> str`
- `game_wins -> int`
- `game_losses -> int`
- `match_wl -> str`
- `total_mulligans -> int`
- `total_games -> int`
- `match_win_flag -> int | str`
- `game_win_rate -> float | str`
- `is_ready() -> bool`
- `rank_bucket() -> str`
- `mtga_format() -> str`
- `mtga_queue_type() -> str`
- `event_identity() -> EventIdentity`
- `played_date() -> str`
- `set_constructed_rank(...) -> None`
- `to_debug_dict() -> dict[str, Any]`
- `to_sheet_row() -> dict[str, Any]`
- `to_history_item() -> dict[str, Any]`
- `to_match_log_row(final: bool = True) -> dict[str, Any]`
- `to_game_sheet_rows() -> list[dict[str, Any]]`

## Inputs

### Parser State Inputs

Source: `src/mythic_edge_parser/app/state.py`

Observed behavior:

- `MatchState` events create or update `MatchSummary`.
- `GameState` events update match time, game time, local team, game info, starting player, turn count, and opening-hand candidates.
- `Rank` events update constructed rank fields before or during a match.
- `ClientAction` events update local team, game touch time, mulligans, submit-deck state, sideboarding state, and explicit starting player.
- `GameResult` events update game winner, match winner, result type, result reason, event timing, and game info.

Required guarantees:

- `models.py` should remain event-type agnostic. It should accept normalized values from `state.py`, not raw log structures.
- Invalid or missing game numbers should not create new game slots.
- Missing parser facts should serialize as blank strings where existing rows expect blanks.

### Timestamp Inputs

Source: event metadata normalized by `state.py`.

Observed behavior:

- `GameSummary.touch()` ignores blank timestamps.
- `MatchSummary.touch()` sets `first_event_time` once and updates `last_event_time` every call.
- Durations use `datetime.fromisoformat()` and return blank on parse failure.
- Negative durations clamp to `0`.
- `played_date()` returns the ISO date when the timestamp parses, otherwise the first 10 characters of the timestamp.

Required guarantees:

- Timestamp parsing failures must not crash row serialization.
- Durations must stay numeric seconds or blank, not formatted text.

### Team And Result Inputs

Source: normalized team IDs from parser extractors and state.

Observed behavior:

- `player_team`, `winner_team`, and `starting_player` are compared directly.
- `result_for_player()` returns `W`, `L`, or blank.
- `play_draw()` returns `Play`, `Draw`, or blank.
- `opponent_team()` only knows teams `1` and `2`; other values return blank.

Required guarantees:

- Do not infer a result when either the local player team or winner team is missing.
- Do not infer play/draw when either local player team or starting player is missing.

### Card List Inputs

Source: `state.py` resolves hand snapshots from Arena `grpId` values before calling model setters.

Observed behavior:

- `opening_hand` and `mulliganed_away` are lists of display strings.
- Placeholder cards start with `[` such as `[Arena ID 96185]`.
- Exact card lists serialize as `"; "` joined strings only when there are no placeholders.
- A partial card list with any placeholder serializes as blank for workbook-facing exact-list fields.

Required guarantees:

- Models may preserve partial lists internally for debugging, but `Game Log` exact-card fields must stay blank when any card is unresolved.
- Placeholder suppression belongs in parser/model serialization, not workbook formulas.

### Event Identity Inputs

Source: `event_id`, `super_format`, and `match_win_condition`.

Observed behavior:

- `MatchSummary.event_identity()` delegates to `classify_event_identity()`.
- `to_history_item()` exposes normalized event identity fields used by runtime surfaces and filters.

Required guarantees:

- Match history payloads must continue to expose rank/type/filter fields needed by runtime surfaces.

## Outputs

### `MatchSummary.to_sheet_row()`

Destination: legacy `MTGA Match Summary Feed` and Apps Script bridge behavior.

Observed row identity:

- `event_family`: `MatchSummary`
- `event_type`: `match_summary`
- `scope`: `Match`
- `match_id`: parser match ID

Observed fields:

- timing: `timestamp`, `first_event_time`, `last_event_time`
- match identity/result: `match_id`, `player_team`, `winner_team`, `result_type`, `result_reason`, `match_wl`
- per-game winners: `g1_winner_team`, `g2_winner_team`, `g3_winner_team`
- per-game play/draw: `g1_play_draw`, `g2_play_draw`, `g3_play_draw`
- per-game mulligans: `g1_mulligans`, `g2_mulligans`, `g3_mulligans`
- aggregate stats: `total_mulligans`, `game_wins`, `game_losses`
- booleans: `sideboarding_entered`, `submit_deck_seen`
- rank: `constructed_rank`, `my_rank`
- per-game results: `g1_result`, `g2_result`, `g3_result`
- `raw_json`: JSON dump of `to_debug_dict()`

Required guarantees:

- This row remains backward compatible while Apps Script still accepts `MatchSummary`.
- New implementation should prefer `MatchLogRow` for current `Match Log` updates unless a future contract retires this bridge.

### `MatchSummary.to_match_log_row(final: bool = True)`

Destination: `Match Log` workbook landing sheet through `MatchLogRow`.

Observed row identity:

- `event_family`: `MatchLogRow`
- `event_type`: `match_log_row`
- `scope`: `Match`
- `match_id`: parser match ID
- `MTGA Match ID`: same parser match ID

Observed workbook fields:

- `Date`
- `Experiment ID`
- `Deck Code`
- `Opponent Archetype`
- `Opponent Variant`
- `My Rank`
- `Opponent Rank`
- `Deck Tier`
- `G1 Play / Draw`
- `Game 1 Result`
- `G2 Play / Draw`
- `Game 2 Result`
- `G3 Play / Draw`
- `Game 3 Result`
- `Games Won`
- `Games Lost`
- `Match Win?`
- `Valid?`
- `General Analysis?`
- `Primary Comparison Analysis?`
- `Reason Tag`
- `Pilot Error?`
- `One-line note`
- `Rank Group`
- `Mythic Split`
- `Total Games`
- `Match Win Flag`
- `Game Win %`
- `Queue Bucket (Auto)`
- `Primary Comparison (Auto)`
- `Event Round`
- `MTGA Match ID`
- `MTGA Format`
- `MTGA Event ID`
- `MTGA Queue Type`
- `G1 Mulligans`
- `G2 Mulligans`
- `G3 Mulligans`
- `G1 Turn Count`
- `G2 Turn Count`
- `G3 Turn Count`
- `MGTA Start Time`
- `MTGA End Time`
- `MTGA Rank Raw`
- `MTGA Mulligans`
- `MTGA Sideboard Entered`
- `MTGA Submit Deck Seen`
- `MTGA Sync Status`

Observed provisional-vs-final behavior:

- `final=True` sets `MTGA Sync Status` to `Final`.
- `final=False` sets `MTGA Sync Status` to `Live`.
- `final=False` leaves `MTGA End Time` blank.
- `final=False` leaves sideboard and submit-deck fields blank when the flag has not been observed.
- `final=True` turns missing sideboard and submit-deck flags into `No`.
- `MTGA Mulligans` is blank during live rows when total mulligans is zero; otherwise it can show the current parser count.
- Live rows can include provisional game wins/losses and game results before final match result exists.

Required guarantees:

- The row must remain upsertable by `tools/google_apps_script/Code.gs` using match ID.
- Parser-managed fields must continue to match `MATCH_LOG_SYNC_FIELDS` from `sheet_schema.py`.
- The existing workbook typo `MGTA Start Time` is part of the current contract and must not be silently renamed.

### `GameSummary.to_game_log_row(match)`

Destination: `Game Log` workbook landing sheet through `GameLogRow`.

Observed row identity:

- `event_family`: `GameLogRow`
- `event_type`: `game_log_row`
- `scope`: `Game`
- `match_id`: parser match ID
- `Game Number`: game number

Observed workbook fields:

- `Date`
- `MTGA Format`
- `My Rank`
- `MTGA Match ID`
- `Game Number`
- `Pre / Postboard`
- `Play / Draw`
- `Mulligans`
- `Opening Hand Size`
- `Opening Hand`
- `Mulliganed Away`
- `Game Result`
- `Turn Count`
- `Game Duration`
- `MTGA Event ID`
- `MTGA Queue Type`

Observed behavior:

- Game 1 is `Preboard`; games 2 and 3 are `Postboard`.
- `Opening Hand Size` is the exact opening-hand length when known.
- If no opening-hand list exists but the game has started, opening-hand size falls back to `max(7 - mulligans, 0)`.
- `Opening Hand` and `Mulliganed Away` are blank when any card in that list is unresolved.
- `Game Duration` is seconds from game first event to game last event.
- `to_game_sheet_rows()` emits only games where `has_summary_data()` is true.

Required guarantees:

- The row must remain upsertable by Apps Script using `(MTGA Match ID, Game Number)`.
- Parser-managed fields must continue to match `GAME_LOG_SYNC_FIELDS` from `sheet_schema.py`.
- Game rows may be provisional until `Game Result` is nonblank.

### `MatchSummary.to_history_item()`

Destination: runtime status/history JSON written by `runtime_surfaces.py`.

Observed behavior:

- Emits match ID, date, start/end times, result, game counts, rank, raw queue fields, normalized queue identity, flags, rates, and per-game debug payloads.
- Runtime surfaces add deck context and timeline path after this method returns.

Required guarantees:

- Keep history-filter fields stable unless runtime surface filters are updated in the same implementation pass.

### Debug Payloads

Destinations:

- `raw_json` in sheet rows
- active match snapshot in runtime surfaces
- local debugging by tests and operators

Observed behavior:

- `to_debug_dict()` includes raw parser facts plus derived facts.
- Game debug payloads include opening-hand and mulliganed-away lists even when exact workbook fields are blank.

Required guarantees:

- Debug payloads may be richer than workbook fields, but they must not contradict workbook-facing derived values.

## Observed Behavior

This section records what the current code and tests demonstrate today.

- A ready match requires `match_id`, `player_team`, and `match_winner_team`.
- Game slots are fixed to games 1, 2, and 3.
- Game-number coercion accepts values that `int()` can parse; invalid values no-op.
- Missing values generally serialize as blank strings.
- Match win/loss is blank until match winner and player team are both known.
- Game win rate is blank when total games is zero.
- Mythic percentile ranks display as `Mythic %`.
- Mythic numbered ranks display as `Mythic #`.
- Other constructed rank classes display as the class name.
- `SuperFormat_` prefixes are stripped for `MTGA Format`.
- Event ID fallback detects `Constructed` and `Limited`.
- Queue type uses explicit match-win-condition mappings first, then event/text heuristics, then sideboarding or total games.
- Later-game play/draw can be inferred from the previous game's winner when explicit starting-player data is missing.
- Explicit starting-player data beats inferred starting-player data.
- Unused game slots stay blank when they have no summary data.
- Partial card lists containing placeholders are retained internally but hidden from exact-card workbook fields.
- Runtime match history uses `to_history_item()` and then adds deck context outside this module.

## Required Guarantees

Future implementation against this contract must preserve these guarantees unless issue #2 is explicitly amended.

- `models.py` remains the parser-owned row-shaping layer.
- `state.py` remains responsible for interpreting raw events and feeding normalized facts into models.
- `outputs.py` remains transport only.
- Apps Script remains transport/upsert only.
- Workbook formulas and dashboards must not become the truth owner for parser facts.
- `MatchLogRow` shape must stay compatible with the `Match Log` tab and Apps Script field map.
- `GameLogRow` shape must stay compatible with the `Game Log` tab and Apps Script field map.
- `MatchSummary` legacy row compatibility must be preserved until a migration contract retires it.
- Live rows must be explicitly marked `Live`; final rows must be explicitly marked `Final`.
- Final reconciliation must be able to overwrite provisional live values downstream.
- Unknown, malformed, or unavailable parser facts should serialize as blanks rather than fabricated values.
- Exact card-list workbook fields must not expose partial unresolved placeholder lists.

## Error Behavior

Observed behavior:

- Invalid game numbers return `None` or no-op through `MatchSummary.game()`.
- Invalid turn numbers are ignored by `GameSummary.set_turn_count()`.
- Invalid duration timestamps return blank duration.
- Invalid played-date timestamps return the first 10 characters of the string.
- Non-dict `game_info` passed to `ingest_game_info()` is ignored.
- Empty winner or starting-player values do not overwrite existing game fields.
- Empty opening-hand inputs are ignored.
- Empty mulliganed-away inputs are ignored.

Required guarantees:

- Model serialization should not raise exceptions for missing optional parser facts.
- Structural errors that imply a workbook schema change should be caught by tests or contract review, not masked in workbook formulas.

## Side Effects

Observed behavior:

- Model mutator methods change only the `MatchSummary` or nested `GameSummary` instance.
- Serializer methods return dictionaries or lists and do not write files, post webhooks, mutate workbook state, or update global parser state.
- `event_identity()` calls `classify_event_identity()` but does not mutate identity state.

Required guarantees:

- Keep external I/O out of `models.py`.
- Keep global runtime state ownership in `state.py` and runtime surface modules, not model objects.

## Dependency Order

If a future implementation changes this contract, update and validate in this order:

1. Update `docs/contracts/parser_models.md` to name the intended contract change.
2. Update `src/mythic_edge_parser/app/models.py`.
3. Update `src/mythic_edge_parser/app/sheet_schema.py` if workbook sync fields changed.
4. Update `tools/google_apps_script/Code.gs` if Apps Script field maps, tab names, or upsert keys changed.
5. Update `src/mythic_edge_parser/app/state.py` if parser inputs into the model changed.
6. Update runtime-history consumers such as `runtime_surfaces.py` if `to_history_item()` changed.
7. Update focused tests.
8. Run the smallest relevant checks before broader repo checks.

## Compatibility

Current compatibility requirements:

- `MatchSummary.to_sheet_row()` remains a legacy bridge row while Apps Script still accepts `event_family == "MatchSummary"`.
- `MatchLogRow` is the current normalized match landing row.
- `GameLogRow` is the current normalized game landing row.
- `GameSummary.to_sheet_row()` exists, but no current tests or code paths were found that depend on posting `event_family == "GameSummary"` directly.
- The workbook field name `MGTA Start Time` is misspelled in code and must remain stable unless a workbook migration contract changes it.
- The parser assumes at most three games per match.
- Apps Script currently writes by header names, so header spelling is part of the interface.

## Unknowns

- It is unknown whether live workbook state exactly matches repository `Code.gs`.
- It is unknown whether deployed Apps Script matches repository `tools/google_apps_script/Code.gs`.
- It is unknown whether `GameSummary.to_sheet_row()` is intentionally retained for future use or is stale bridge code.
- It is unknown whether `MGTA Start Time` is an accepted workbook typo or queued for migration.
- It is unknown whether queue-type heuristics are complete for all current MTGA event IDs.
- It is unknown whether match history consumers outside the repo depend on all `to_history_item()` fields.

## Suspected Gaps

- There is no direct test that `to_match_log_row()` contains every field listed in `MATCH_LOG_SYNC_FIELDS`.
- There is no direct test that `to_game_log_row()` contains every field listed in `GAME_LOG_SYNC_FIELDS`.
- There is no direct test that Apps Script and Python agree on every `MatchLogRow` and `GameLogRow` field name.
- `MatchSummary.touch()` does not explicitly ignore blank timestamps the way `GameSummary.touch()` does.
- `set_game_mulligans()` accepts the annotated `int` but does not enforce or coerce integer input.
- `effective_starting_player()` infers later-game play/draw from the immediately previous game only; that is tested for common cases but may need more contract tests for unusual retirements or missing intermediate game data.
- `mtga_queue_type()` falls back to sideboarding and total-games heuristics, which can make provisional live queue labels depend on partially observed state.
- `played_date()` returns the first 10 characters of an invalid timestamp, which is tolerant but may hide malformed timestamp sources.

## Tests Required

Focused checks for this module:

```powershell
py -m pytest -q tests/test_app_models.py
py -m pytest -q tests/test_match_summary_from_match_state.py
py -m pytest -q tests/test_runtime_surfaces.py
py -m pytest -q tests/test_sheet_schema.py
```

Recommended contract-test additions before behavior changes:

- Assert `set(MATCH_LOG_SYNC_FIELDS)` is a subset of `MatchSummary(...).to_match_log_row().keys()`.
- Assert `set(GAME_LOG_SYNC_FIELDS)` is a subset of each emitted `GameLogRow` keys.
- Assert Apps Script `buildMatchLogFieldMap_()` and `buildGameLogFieldMap_()` field names match Python row keys or documented fallback aliases.
- Add a regression case for blank timestamp handling if `MatchSummary.touch()` behavior is changed.
- Add edge cases for queue type inference and later-game starting-player inference if issue #2 touches those behaviors.

Broader checks before merging implementation that changes row shapes:

```powershell
py -m pytest -q tests
py -m ruff check src tests
.\tools\run_repo_checks.ps1
```

## Acceptance Criteria

- The parser model contract exists at `docs/contracts/parser_models.md`.
- The contract links to issue #2, the constitution, the module contract role rules, and the module contract template.
- The contract names parser/state interpretation as the truth-owning layer.
- Public classes, methods, row fields, and downstream dependents are listed.
- Observed behavior is separated from required guarantees.
- Provisional live values are distinguished from final reconciled values.
- Unknowns and suspected gaps are explicitly recorded.
- No runtime behavior changes are made as part of this contract thread.
