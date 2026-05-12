# Parser State Module Contract

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/6

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the current `src/mythic_edge_parser/app/state.py`
behavior and the guarantees future parser-state work must preserve unless a
new problem representation and contract deliberately change them. This is a
contract artifact only. It does not implement behavior changes.

## Module

`src/mythic_edge_parser/app/state.py`

The module owns parser runtime state and transforms already-parsed MTGA events
into live and final `MatchSummary` / `GameSummary` state. It also decides when
match log and game log rows have changed enough to post again.

## Owning Layer

Parser and state interpretation.

The parser/state layer owns normalized match and game facts. Workbook formulas,
webhook transport, dashboards, helper tabs, and AI analysis must consume those
facts rather than reconstructing them. `state.py` may depend on parser event
payloads, extractor helpers, model row serializers, and sync-field definitions,
but it remains the source of truth for live parser runtime state.

## Files Owned By This Contract

- `src/mythic_edge_parser/app/state.py`
- `tests/test_state.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_parser_regressions.py`
- `tests/test_saved_event_replay.py`
- `docs/contracts/parser_state.md`

Related files whose behavior is referenced but not owned by this contract:

- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/grp_id_catalog.py`

## Parser Truth Ownership

Required ownership boundaries:

- `state.py` owns the live parser context: current match ID, current game
  number, and current local player team.
- `state.py` owns in-memory `MatchSummary` objects keyed by MTGA match ID.
- `state.py` owns rank carry-forward state used to seed future match summaries.
- `state.py` owns mulligan counters, hand snapshot history, card-ID lookup
  readiness flags, bottomed-card capture state, and game instance-to-grpId maps
  used for opening hand and mulliganed-away facts.
- `state.py` owns changed-field detection and last-posted snapshots for match
  log and game log sync decisions.
- `models.py` owns the row field shape and serialization for
  `MatchSummary.to_sheet_row()`, `MatchSummary.to_match_log_row()`, and
  `MatchSummary.to_game_sheet_rows()`.
- `sheet_schema.py` owns the field lists used to decide which match log and
  game log fields participate in update detection.
- `runner.py` and `outputs.py` may transport rows and call mark-posted
  callbacks after successful webhook dispatch. They do not own parser truth.
- Workbook, dashboard, helper formula, webhook, and AI layers must not become
  the source of match identity, game identity, winners, play/draw, mulligans,
  opening hands, final reconciliation, or deduplication.
- GameResult winner precedence for final reconciliation is parser-owned truth.
  Downstream workbook, webhook, Apps Script, dashboard, helper formula, and AI
  layers must not reinterpret nested GRE `results` to decide game winner, match
  winner, match result type, or match result reason.

## Public Interfaces

This module has two classes of public surface: supported module functions and
compatibility surfaces that are currently used by tests or sibling modules even
when their names are underscored.

### Supported Functions And Objects

| Interface | Current signature or shape | Contract status |
| --- | --- | --- |
| `ParserRuntimeState` | dataclass with mutable runtime containers and scalar state | Primary state container. |
| `RUNTIME_STATE` | module singleton `ParserRuntimeState` | Primary live state object. |
| `get_last_posted_rank()` | `() -> str` | Supported rank dedupe getter. |
| `set_last_posted_rank(rank_text)` | `(Any) -> None` | Supported rank dedupe setter. |
| `reset_runtime_state()` | `() -> None` | Supported test/runtime reset API. |
| `build_match_summary_row(match_id)` | `(str) -> dict[str, Any] | None` | Supported final match summary row builder. |
| `build_game_summary_rows(match_id)` | `(str) -> list[dict[str, Any]]` | Supported game row builder. |
| `build_match_log_row(match_id)` | `(str) -> dict[str, Any] | None` | Supported final match log row builder. |
| `build_live_match_log_row(match_id)` | `(str) -> dict[str, Any] | None` | Supported live match log row builder. |
| `build_match_log_update(match_id)` | `(str) -> tuple[dict[str, Any] | None, list[str], bool]` | Supported changed-field match log update builder. |
| `mark_match_log_posted(match_id, row)` | `(str, dict[str, Any]) -> None` | Supported match log snapshot marker. |
| `build_game_log_updates(match_id)` | `(str) -> list[tuple[dict[str, Any], list[str], bool]]` | Supported changed-field game log update builder. |
| `mark_game_log_posted(match_id, game_number, row)` | `(str, Any, dict[str, Any]) -> None` | Supported game log snapshot marker. |
| `get_match_summary(match_id)` | `(str) -> MatchSummary | None` | Supported live summary getter. |
| `iter_match_summaries()` | `() -> list[MatchSummary]` | Supported live summary iterator snapshot. |
| `get_runtime_state()` | `() -> ParserRuntimeState` | Supported runtime state getter. |
| `get_context_snapshot()` | `() -> dict[str, Any]` | Supported copy of current context. |

### Internal-Public Compatibility Surface

These names are underscored, but current code imports or mutates them directly.
Future work must preserve them until a migration contract explicitly replaces
them.

| Interface | Current consumers | Contract status |
| --- | --- | --- |
| `_update_match_summary(event)` | `runner.py`, focused tests, replay tests | Internal-public ingestion function. |
| `_CONTEXT` | `runner.py`, `transforms.py`, `runtime_surfaces.py`, `gameplay_actions.py`, tests | Compatibility alias for current context. |
| `_MATCH_SUMMARIES` | tests, runtime surfaces | Compatibility alias for summaries. |
| `_POSTED_MATCH_SUMMARIES` | `runner.py` | Compatibility alias for once-only match summary posting. |
| `_LOCAL_TURN_KEYS`, `_LOCAL_HAND_SNAPSHOT_KEYS`, `_SHEETS_TURN_KEYS` | `transforms.py`, tests | Compatibility dedupe containers. |
| `_POSTED_SUBMIT_DECK_KEYS`, `_POSTED_SIDEBOARD_KEYS` | `transforms.py` | Compatibility row dedupe containers. |
| `_GAME_ROWS_POSTED`, `_MATCH_ROWS_POSTED` | `transforms.py` | Compatibility raw game/match row dedupe containers. |
| `_MULLIGAN_COUNTS` | `transforms.py`, tests | Compatibility mulligan counter. |
| `_GAME_INSTANCE_GRP_IDS`, `_HAND_SNAPSHOT_HISTORY`, `_LATEST_HAND_SNAPSHOT`, `_BOTTOMED_CARDS_CAPTURED` | tests and hand/mulligan state | Compatibility gameplay card state. |
| `_ARENA_CARD_LOOKUP`, `_ARENA_CARD_LOOKUP_READY`, `_GAMEPLAY_CARD_LOOKUP_READY` | focused tests and parser regression tests | Compatibility card lookup bridge. |
| `_LAST_POSTED_MATCH_LOG_ROWS`, `_LAST_POSTED_GAME_LOG_ROWS` | focused tests | Compatibility changed-field snapshots. |
| `_context_key(match_id, game_number)` | `transforms.py` | Internal-public context fallback helper. |

## Inputs

### Event Input

`_update_match_summary(event)` observes:

- `event.kind`: string event family.
- `event.payload`: dict-like payload. Missing payload is treated as `{}`.
- `event.metadata.timestamp`: optional timestamp used through extractor helpers.

The current supported event kinds are:

| Event kind | Important payload fields | Observed source |
| --- | --- | --- |
| `MatchState` | `type`, `match_id`, `event_id`, `players`, `game_results` | match state parser |
| `GameState` | `identity`, `game_info`, `turn_info`, `raw_game_state`, `players`, `zones`, `game_objects` | GRE game state parser |
| `Rank` | `constructed_class`, `constructed_level`, `constructed_percentile` | rank parser |
| `ClientAction` | `type`, `message_type`, `decision`, `raw_client_action` | client action parser |
| `GameResult` | `identity`, `game_info`, `winning_team_id`, `result_type`, `reason`, `match_state`, `results`, nested `results[].scope`, nested `results[].winningTeamId`, nested `results[].result`, nested `results[].reason` | GRE game result parser |

Unknown event kinds are ignored.

### State Input

Row builders and update builders read the current in-memory state:

- `_MATCH_SUMMARIES[match_id]`
- `_LAST_POSTED_MATCH_LOG_ROWS[match_id]`
- `_LAST_POSTED_GAME_LOG_ROWS[(match_id, game_number)]`
- `_MATCH_LOG_SYNC_FIELDS`
- `_GAME_LOG_SYNC_FIELDS`

Opening hand and mulligan capture also read:

- `_ARENA_CARD_LOOKUP`
- `_ARENA_CARD_LOOKUP_READY`
- `_GAMEPLAY_CARD_LOOKUP_READY`
- `_GAME_INSTANCE_GRP_IDS`
- `_HAND_SNAPSHOT_HISTORY`
- `_LATEST_HAND_SNAPSHOT`

## Outputs

### In-Memory State Outputs

`_update_match_summary(event)` mutates the live `ParserRuntimeState` through
`RUNTIME_STATE` and compatibility aliases. It may create or update a
`MatchSummary`, touch a `GameSummary`, update context fields, record rank
snapshots, track mulligans, capture hand snapshots, or update dedupe containers.

### Row Outputs

| Builder | Current row source | Readiness | Provisional or final |
| --- | --- | --- | --- |
| `build_match_summary_row(match_id)` | `summary.to_sheet_row()` | Requires `summary.is_ready()` | Final summary only. |
| `build_game_summary_rows(match_id)` | `summary.to_game_sheet_rows()` | Requires summary existence; model omits empty games | Per-game rows may be live or final depending on game data. |
| `build_match_log_row(match_id)` | `summary.to_match_log_row(final=True)` | Requires `summary.is_ready()` | Final only. |
| `build_live_match_log_row(match_id)` | `summary.to_match_log_row(final=False)` | Requires summary and `summary.match_id` | Live/provisional. |
| `build_match_log_update(match_id)` | `summary.to_match_log_row(final=summary.is_ready())` | Requires summary and `summary.match_id`; returns `None` if no sync fields changed | Live until ready, final when ready. |
| `build_game_log_updates(match_id)` | `summary.to_game_sheet_rows()` | Requires summary; skips rows with invalid key or no sync-field changes | Live until `Game Result` is non-empty, final when game result exists. |

Changed-field lists contain only fields from `MATCH_LOG_SYNC_FIELDS` or
`GAME_LOG_SYNC_FIELDS`. Empty values are treated as not changed on the first
post. Floats are normalized with `round(value, 10)` before comparison.

## Observed Behavior

### Runtime State

- `ParserRuntimeState` stores mutable containers for dedupe keys, posted-row
  snapshots, context, mulligan counts, match summaries, game instance mappings,
  hand snapshots, and bottomed-card capture.
- `RUNTIME_STATE` is a module-level singleton.
- Most underscored module globals are aliases to `RUNTIME_STATE` containers.
  `reset_runtime_state()` clears containers in place so alias identity survives.
- Scalar compatibility globals, including rank text and card lookup flags, are
  synchronized by helper functions and reset behavior, not by a general alias
  mechanism.
- `current_log_date` and `current_log_path` live on `RUNTIME_STATE` and are used
  by `outputs.py` to cache daily JSONL paths.

### Reset Behavior

- `reset_runtime_state()` clears tracked sets and dicts in place.
- Context is restored to:
  - `current_match_id: ""`
  - `current_game_number: ""`
  - `current_player_team: ""`
- Current log path/date, card lookup flags, gameplay lookup readiness, latest
  rank snapshot, and last posted rank are reset to empty/default values.
- `RUNTIME_STATE` itself is not replaced.
- Container aliases remain usable after reset.

### Rank Behavior

- Rank payloads normalize to:
  - `Mythic <percentile>` when `constructed_class == "Mythic"` and percentile
    is present.
  - `<constructed_class> <constructed_level>` otherwise.
- Empty normalized rank text is ignored.
- A rank event updates `last_posted_rank` and the latest rank snapshot.
- A rank event before a match seeds the next created summary with
  `constructed_rank_source == "carried_forward_pre_match"`.
- A rank event during a current match updates the current summary only while
  that summary is not ready.
- A rank event after a completed summary does not overwrite that completed
  summary in the focused tests; it carries forward to the next match summary.

### MatchState Event Handling

- If no match ID can be read from payload or context, the event is ignored.
- The current match ID is updated from the payload or context.
- A `MatchSummary` is created if needed.
- First and last event timestamps are touched.
- `event_id` is set from payload when available. If an existing event ID is
  `"Play"`, a later non-`"Play"` value may replace it.
- Local player team is taken from existing context/summary when present;
  otherwise it is inferred from the configured local player in `players`.
- Game-scope results in `game_results` are assigned sequentially to game 1,
  game 2, and game 3.
- Match-scope results with a non-empty winning team set match winner, result
  type, and result reason.
- `type == "match_started"` sets current game number to `1`.

### GameState Event Handling

- Match ID and game number are extracted from payload identity/game info and may
  fall back to current context.
- If no match ID is available, the event is ignored.
- Current match ID is updated, and current game number is updated when present.
- A summary is created if needed and touched.
- Local team is updated from GameState player/seat data when available.
- `game_info` is passed to the summary to update MTGA format and queue inputs.
- The current game is touched, starting player is inferred from turn-one
  active player data when possible, and turn count monotonically advances.
- Opening-hand candidates are recorded from local private hand zones with 4 to
  7 cards.
- Opening hand is set only when the candidate belongs to turn 1 and matches the
  expected hand size after mulligans.

### ClientAction Event Handling

- Client actions are ignored when no current match ID is known.
- The current summary is touched and local team may be corrected from client
  action payloads.
- The current game is touched when a current game number exists.
- `mulligan_resp` and generic `ClientMessageType_MulliganResp` update mulligan
  count for the current match/game.
- Keep decisions return the existing mulligan count. Non-keep decisions
  increment the count.
- Before a non-keep decision increments the count, the latest hand snapshot for
  the match/game is recorded as mulliganed-away and removed from latest-snapshot
  state.
- `submit_deck_resp` and generic `ClientMessageType_SubmitDeckResp` set
  `submit_deck_seen`.
- Generic `ClientMessageType_ChooseStartingPlayerResp` sets the game starting
  player.
- Generic `ClientMessageType_EnterSideboardingReq` sets
  `sideboarding_entered`.

### GameResult Event Handling

Current observed behavior:

- Match ID, game number, winning team, result type, and reason are extracted
  from identity/game info/current context/top-level payload.
- If no match ID is available, the event is ignored.
- Current match ID is updated, and current game number is updated when present.
- A summary is created if needed and touched.
- `game_info` updates MTGA format and queue inputs.
- Summary player team is refreshed from current context when known.
- The game is touched and the game winner is set when game number and winner
  are usable.
- If payload `match_state` is `MatchState_MatchComplete` or payload `results`
  contains a match-scope result, a non-empty top-level winning team sets match
  winner, match result type, and match result reason.
- Current `MatchSummary` winner setters treat only `None` and `""` as missing,
  so numeric `0` can currently be accepted as a winner value even though the
  revised required guarantee below classifies `0` as unknown.
- The current GRE GameResult parser builds top-level `winning_team_id`,
  `result_type`, and `reason` from the latest `MatchScope_Game` result when one
  exists, and otherwise falls back to the last dict-like result. That fallback
  can make a match-scope result look like a game winner in top-level fields.
- Current state finalization detects whether a match-scope result exists, but
  does not independently extract the nested `MatchScope_Match.winningTeamId`,
  `result`, or `reason` for final match reconciliation.

### Hand And Mulligan Capture

- Hand snapshots are resolved from local private hand zone instance IDs and
  instance-to-grpId mappings.
- The per-game instance-to-grpId mapping accumulates across GameState events.
- When `_ARENA_CARD_LOOKUP_READY` is true and `_ARENA_CARD_LOOKUP` is a dict,
  state uses that lookup.
- Otherwise, state calls `resolve_grp_id_entry()` after attempting
  `bootstrap_grp_id_catalog()`.
- Missing or unresolved IDs become placeholders such as `[Arena ID 99999]` or
  `[Missing Arena ID for instance 101]`.
- In-memory opening hands may contain placeholders.
- `models.py` serializes `Opening Hand` and `Mulliganed Away` as blank strings
  when placeholders remain.
- Hand snapshot history avoids appending consecutive duplicate card lists.
- Bottomed cards are inferred from the most recent prior snapshot that is
  longer than the final kept hand, preserving duplicate-card counts.
- Bottomed-card capture runs once per normalized match/game key.

### Row Readiness And Changed-Field Behavior

- A summary is ready when `MatchSummary.is_ready()` is true, currently requiring
  match ID, local player team, and match winner team.
- Final match summary rows and final match log rows are withheld until ready.
- Live match log rows can be built before ready if a summary with a match ID
  exists.
- Match log updates use final rows once ready and live rows otherwise.
- Game log updates are per game and become final when the row has a non-empty
  `Game Result`.
- `mark_match_log_posted()` stores a shallow copy of the posted row.
- `mark_game_log_posted()` stores a shallow copy keyed by normalized match ID
  and integer game number.
- Repeated build calls after mark-posted return no update until a sync field
  changes.

### Observation APIs

- `get_match_summary()` returns the live `MatchSummary` object or `None`.
- `iter_match_summaries()` returns a list snapshot of live summary objects.
- `get_runtime_state()` returns the live `ParserRuntimeState` singleton.
- `get_context_snapshot()` returns a shallow copy of current context.

## Required Guarantees

Future work against this module must preserve these guarantees unless this
contract is explicitly revised:

- Parser/state remains the truth owner for match and game facts.
- `_update_match_summary(event)` remains the single ingestion boundary used by
  the runtime until a future contract splits it.
- Unknown event kinds remain no-ops.
- Missing match identity must not create anonymous summaries.
- Context fallback remains available for event payloads that omit match/game
  identity after context has been established.
- Current context updates must not move match/game identity derivation into
  workbook, webhook, dashboard, or AI layers.
- Rank carry-forward must not overwrite completed match summaries.
- A pre-match rank snapshot must seed the next match summary when no summary
  rank is already set.
- Local player team corrections from ClientAction and GameState must be allowed
  to fix earlier MatchState player-order guesses.
- Game winners and match winners must remain distinguishable.
- GameResult final reconciliation must use explicit parser-owned winner
  precedence:
  - Winner values `None`, `""`, `0`, and `"0"` are unknown. `0` is unknown, not
    a valid team winner, because current GRE payload building uses `0` as the
    default for missing winners and observed MTGA team winners are non-zero team
    IDs. Unknown winners must not set or overwrite game or match winners.
  - A non-zero winner value is valid even if it is not exactly `1` or `2`; the
    contract should not hard-code future Arena team IDs beyond treating zero as
    unknown.
  - Game winner must come from the latest nested result whose scope normalizes
    to `MatchScope_Game` / `Game` and whose winner is known. For GRE
    parser-produced payloads, top-level `winning_team_id` must represent that
    latest game-scope winner or remain unknown; a match-scope result must not be
    promoted into the game winner field.
  - If a legacy/manual `GameResult` payload has no nested `results` list at all,
    state may continue treating a known top-level `winning_team_id` as the game
    winner compatibility input. This compatibility fallback must not apply when
    a nested `results` list is present but lacks a valid game-scope winner.
  - Match winner must prefer the latest nested result whose scope normalizes to
    `MatchScope_Match` / `Match` and whose winner is known.
  - Match result type and match result reason must prefer the same nested
    match-scope result when present. If fallback to top-level match completion
    is used, result type and reason may still use nested match-scope `result`
    and `reason` when present; otherwise they fall back to top-level
    `result_type` and `reason`.
  - If no nested match-scope winner exists, state may fall back to a known
    top-level `winning_team_id` for the match winner only when
    `match_state == "MatchState_MatchComplete"`.
  - A top-level `winning_team_id` must not be used as the match winner solely
    because the payload contains a match-scope result. The match-scope result's
    own winner has precedence.
- Live match log rows must remain distinct from final match log rows through
  `MTGA Sync Status` and final-only fields such as `MTGA End Time`.
- Changed-field detection must compare only schema sync fields.
- Posted-row snapshots must update only through mark-posted calls, which runtime
  callbacks should call only after successful transport.
- Game log update finality must remain per game, based on non-empty
  `Game Result`.
- Match log update finality must remain per match summary readiness.
- Reset must clear state in place and preserve compatibility alias identity.
- Opening-hand capture may preserve partial in-memory placeholders, but
  workbook-facing exact card-list serialization must not pretend placeholders
  are known card names.
- Mark-posted APIs must store row copies, not references to mutable caller
  dictionaries.
- The row field names emitted by state-owned builders must continue to come
  from `models.py`; update detection fields must continue to come from
  `sheet_schema.py`.

## Error Behavior

Observed and required error behavior:

- Unknown event kinds are ignored.
- Event kinds that need a match ID return without mutation when no match ID is
  available, except for rank snapshots, which can be stored before a match.
- Invalid or missing game numbers skip game-key-specific updates.
- `mark_game_log_posted()` is a no-op for invalid match/game keys.
- Missing card lookup entries produce placeholders instead of exceptions.
- `bootstrap_grp_id_catalog()` exceptions are swallowed by
  `_ensure_gameplay_card_lookup()`.
- Missing timestamps are normalized by extractor helpers to current time.
- Webhook failures are outside this module. State should not mark rows posted
  until the transport layer invokes mark-posted after success.

Not guaranteed by current code:

- Non-dict payloads are not a supported input shape for `_update_match_summary`;
  current branches call `.get()` on payload.
- Thread safety is not guaranteed.
- Multiple simultaneous active matches are not modeled; the module has one
  current context.
- The current implementation does not yet satisfy the new nested
  `MatchScope_Match` winner precedence guarantee. That is an implementation
  target for the next Module Fixer/Implementer thread.

## Side Effects

`state.py` side effects are intentionally narrow:

- Mutates in-memory runtime state.
- May call `bootstrap_grp_id_catalog()` / `resolve_grp_id_entry()` while
  resolving hand snapshots.
- Does not write match log files directly.
- Does not submit webhooks directly.
- Does not mutate workbook state directly.
- Does not read secrets or environment variables directly.

## Dependency Order

For future behavior work, preserve this order:

1. Update this contract only through the parser audit workflow if the intended
   behavior changes.
2. Update `models.py` first when row shape, derived fields, or readiness meaning
   changes.
3. Update `sheet_schema.py` when changed-field sync fields change.
4. Update `state.py` ingestion, readiness, or dedupe behavior against the
   contract.
5. Update focused tests for state behavior.
6. Update runner, transport, runtime surfaces, or workbook-facing layers only
   after parser-owned truth is explicit.

## Compatibility

Compatibility that must remain until a future migration contract:

- Module-level container aliases must remain live after reset.
- Scalar rank compatibility must keep `get_last_posted_rank()` and
  `set_last_posted_rank()` synchronized with `RUNTIME_STATE.last_posted_rank`.
- Tests and runtime code may still seed `_ARENA_CARD_LOOKUP` and readiness flags
  directly.
- Tests and sibling modules may still use `_CONTEXT` and other underscore
  containers.
- `_update_match_summary()` remains callable despite its underscored name.

## Unknowns

- Whether direct mutation of underscored aliases should become a long-term
  supported API or be migrated behind explicit accessors.
- Whether `_update_match_summary()` should remain monolithic or be split into
  event-specific helpers in a future implementation thread.
- Whether current-context fallback is sufficient for out-of-order event replay
  across multiple matches.
- Whether card catalog bootstrap failures should stay silent or become
  observable diagnostics.
- Whether scalar aliases beyond last-posted rank need full two-way
  synchronization with `RUNTIME_STATE`.
- Whether `build_live_match_log_row()` has an active runtime caller or is
  compatibility surface for future/manual callers.
- Whether rank events after match completion but before context advances should
  be explicitly classified as post-match snapshots in state rather than relying
  on summary readiness.

## Suspected Gaps

These are not implementation instructions. They are contract risks for the next
thread to compare against current code and tests.

- Some focused tests manually clear subsets of state instead of always calling
  `reset_runtime_state()`, which can hide stale scalar state or unrelated
  containers.
- Compatibility aliases are clear for mutable containers but less clear for
  scalar aliases such as current log date/path, latest rank fields, and card
  lookup readiness flags.
- `GameResult` match finalization currently uses top-level `winning_team_id`
  when a match-scope result exists. This is no longer just a suspected gap: the
  required guarantee above now defines nested match-scope winner precedence and
  makes current behavior a contract mismatch to fix.
- `src/mythic_edge_parser/parsers/gre/game_result.py` currently falls back to
  the last dict-like result when no `MatchScope_Game` result exists, which can
  promote a match-scope result into top-level game-winner fields. The new
  guarantee requires parser-produced top-level game winner fields to remain
  game-scope-derived or unknown.
- MatchState game-scope results are assigned by list order rather than explicit
  game numbers.
- Swallowing card catalog bootstrap exceptions can make unresolved-card
  behavior hard to diagnose.
- There is no explicit concurrency protection around mutable module globals.
- Opening-hand and bottomed-card capture rely on event ordering and one active
  current context.
- The distinction between public API, internal-public runtime API, and
  test-only compatibility is implicit in code and imports.

## Validation Obligations

Focused parser-state validation:

```powershell
py -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_parser_regressions.py tests/test_saved_event_replay.py
```

Related model/schema checks when row behavior is touched:

```powershell
py -m pytest -q tests/test_app_models.py tests/test_sheet_schema.py
```

GameResult final reconciliation checks required for the next
Module Fixer/Implementer:

```powershell
py -m pytest -q tests/test_gre_game_result_parser.py tests/test_state.py tests/test_match_summary_from_match_state.py
```

Required focused coverage:

- `tests/test_gre_game_result_parser.py` must prove
  `build_game_result_payload()` uses the latest `MatchScope_Game` result for
  top-level game winner fields when multiple game-scope results exist.
- `tests/test_gre_game_result_parser.py` must prove a payload with no
  game-scope result does not promote a match-scope result into top-level
  game-winner fields; `winning_team_id` should remain `0` / unknown and
  top-level game result type/reason should remain empty unless a game-scope
  result exists.
- State-focused tests must prove a GameResult with both game-scope and
  match-scope nested results sets the game winner from the latest
  `MatchScope_Game` result while setting match winner, match result type, and
  match result reason from the nested `MatchScope_Match` result.
- State-focused tests must prove a nested match-scope winner beats a conflicting
  top-level `winning_team_id`.
- State-focused tests must prove fallback to top-level `winning_team_id` for
  match winner occurs only when no nested match-scope winner exists and
  `match_state == "MatchState_MatchComplete"`.
- State-focused tests must prove `0`, `"0"`, `None`, and `""` winner values are
  unknown and do not set or overwrite game or match winners.
- Existing parser-state focused tests must continue to pass.

Full repo check before a submitter opens or updates a module PR:

```powershell
.\tools\run_repo_checks.ps1
```

On non-Windows shells, use the equivalent Python invocation, for example:

```bash
python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_parser_regressions.py tests/test_saved_event_replay.py
```

## Acceptance Criteria

- `docs/contracts/parser_state.md` exists on
  `codex/parser-module-audit-suite`.
- The contract names parser/state as the owning truth layer.
- The contract identifies public interfaces and compatibility surfaces.
- The contract distinguishes observed behavior from required guarantees.
- The contract explicitly names unknowns and suspected gaps.
- The contract preserves live/final row separation and parser-owned truth.
- The contract lists validation obligations for focused and broader checks.
- No behavior changes are included in this contract thread.

## Next Workflow Action

Next role: Module Fixer (D).

The next thread has a concrete contract mismatch to fix: GameResult final
reconciliation must prefer nested match-scope winners and keep game winners
game-scope-derived. It should make the smallest coherent parser-owned code and
focused-test change against this revised contract, then update the parser-state
handoff/report artifacts as needed.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as the Module Fixer thread for https://github.com/Tahjali11/Mythic-Edge/issues/6 and docs/contracts/parser_state.md.

Implement the smallest coherent parser-owned fix for the revised GameResult final reconciliation contract. Game winner must come from the latest nested MatchScope_Game result. Match winner must prefer nested MatchScope_Match.winningTeamId, and match result type/reason must prefer the nested MatchScope_Match result when present. If no nested match-scope winner exists, fall back to top-level winning_team_id only when match_state == "MatchState_MatchComplete". Treat None, "", 0, and "0" as unknown winner values that must not set or overwrite game or match winners.

Update focused tests in tests/test_gre_game_result_parser.py, tests/test_state.py, and/or tests/test_match_summary_from_match_state.py to cover the required precedence and unknown-winner behavior. Update docs/implementation_handoffs/parser_state_comparison.md and docs/contract_test_reports/parser_state.md only as needed to record the fix and validation evidence.

Do not change workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports. Do not change final reconciliation beyond the GameResult winner precedence rule defined in this contract. Do not target main; future module PR work belongs on codex/parser-module-audit-suite.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/6"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "D"
  source_artifact: "docs/contracts/parser_state.md"
  target_artifact: "tests and parser-state handoff/report updates for GameResult final reconciliation"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "documentation-only contract update; no tests required in Module Contract Writer thread"
  stop_conditions:
    - "Stop and route back to Module Contract Writer if GameResult winner precedence remains ambiguous."
    - "Stop and route back to Thinker if the fix requires scope outside issue #6."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not change final reconciliation beyond the GameResult winner precedence rule defined in this contract."
    - "Do not target main until the parser module audit suite is complete."
```

## Handoff Packet

- Role performed: Module Contract Writer.
- Source problem representation: https://github.com/Tahjali11/Mythic-Edge/issues/6
- Audit tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5
- Contract produced: `docs/contracts/parser_state.md`
- Risk tier: High.
- Owning truth layer: parser and state interpretation.
- Public interface: `ParserRuntimeState`, `RUNTIME_STATE`, state reset/getter
  APIs, event ingestion, row builders, changed-field update builders,
  mark-posted APIs, and current compatibility aliases used by runtime/tests.
- Invariants: parser truth stays upstream; live/final rows stay distinct;
  changed-field detection uses schema sync fields; reset preserves alias
  identity; posted-row snapshots are marked only after successful transport.
- Required tests: focused parser-state tests, model/schema tests when row
  behavior changes, full repo checks before submitter PR work.
- Open questions or contract risks: alias support scope, monolithic ingestion,
  silent card lookup failures, and context fallback under out-of-order replay.
- Contract change made in this pass: nested GameResult match-scope winner
  extraction is no longer an open question. It is a required parser-owned final
  reconciliation guarantee, with `0` / `"0"` classified as unknown.
- Next recommended thread role: Module Fixer (D), focused on the concrete
  GameResult final reconciliation mismatch and required tests.
