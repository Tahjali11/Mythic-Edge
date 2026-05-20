# Player.log Evidence Ledger Tier 3 Game Results Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/134
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/132
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/133
- previous_merge_commit: 9496026047f4817cad8456324d376ae33faa5968
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier3-game-results
- target_artifact: docs/contracts/player_log_evidence_ledger_tier3_game_results.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier3_game_results_comparison.md
- risk_tier: High
- status: contract only

Required agent docs:

- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md

Related authority:

- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/parser_gre_game_result.md
- docs/contracts/parser_match_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_state.md
- docs/contracts/parser_sheet_schema.md
- docs/decisions/ADR-0003-player-log-drift-policy.md

## Purpose

The evidence ledger can now explain Tier 1 match lifecycle fields and Tier 1
game-derived aggregate fields. Issue #134 fills the next missing dependency
layer: Tier 3 game-level result provenance.

Game-level results are parser-owned facts derived from observed game-scope
winner evidence and local player-team context. They support workbook-facing
match-row fields such as `Game 1 Result`, `Game 2 Result`, and `Game 3 Result`;
game-log rows such as `Game Result`; debug/history winner-team fields; and the
aggregate fields mapped in issue #132.

This contract documents provenance metadata only. It does not change parser
behavior, winner reconciliation, game identity, workbook row shape, webhook
transport, Apps Script behavior, or analytics truth.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
schema shape, vocabulary constants, validators, and privacy posture.

`docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md` remains
authoritative for match identity, match result, and sync-status provenance.

`docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md` remains
authoritative for aggregate fields:

- `games_won`
- `games_lost`
- `total_games`
- `match_win_flag`
- `game_win_rate`

Issue #134 should make those aggregate dependencies more explicit by adding
Tier 3 per-game result entries. It may update aggregate entry notes or
dependency signal text to cite the new Tier 3 entries, but it must not change
aggregate math or runtime behavior.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #134 provenance should be
recorded through this contract, implementation handoff, entry notes, and
focused tests rather than by changing the top-level ledger object shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- GRE `GameResult` parsing and `MatchState` parsing expose observed game-result
  evidence.
- `src/mythic_edge_parser/app/state.py` owns how game winners are applied to
  `MatchSummary`.
- `src/mythic_edge_parser/app/models.py` owns `GameSummary.winner_team`,
  `GameSummary.result_for_player(...)`, match-row per-game result fields, and
  game-log row result fields.
- `src/mythic_edge_parser/app/evidence_ledger.py` describes provenance,
  confidence, finality, degradation, and review expectations.
- Workbook rows, Apps Script, webhook transport, dashboards, diagnostics,
  golden replay, feature-equity reports, drift reports, and AI output are
  downstream consumers only.

The ledger must not reconstruct missing GameState data, infer unobserved game
results, promote match-scope results into game-scope truth, or move parser truth
into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI.

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` after PR #133:

- Tier 3 output family `game_level_facts` is still registered for future work.
- The family currently lists broad future fields such as `game_result`,
  `play_draw`, `mulligans`, `turn_count`, and `opening_hand`.
- `GameResult` parser payloads preserve `results[]` and select the latest known
  game-scope winner for top-level `winning_team_id`, `result_type`, and
  `reason`.
- `GameResult` parsing treats missing, blank, numeric zero, string zero, and
  boolean winner values as unknown for game-scope top-level selection.
- `GameResult` parsing does not promote match-scope results into game winners.
- `MatchState` parsing preserves `game_results[]` from final match result lists.
- Parser state applies `MatchState.game_results[]` game-scope winners to game
  slots by ordered list position.
- Parser state applies `GameResult` game-scope winner evidence to the game
  number from `identity.game_number`, `game_info.gameNumber`, or current
  parser context.
- Parser state uses nested game-scope `GameResult.results[]` when present and
  known; top-level `winning_team_id` remains a compatibility input when no
  nested results list exists.
- `GameSummary.result_for_player(player_team)` derives `W`, `L`, or blank from
  `winner_team` and local `player_team`.
- Match-row fields `Game 1 Result`, `Game 2 Result`, and `Game 3 Result` are
  derived from the fixed game slots.
- Game-log row field `Game Result` is derived from the same game summary for
  the specific game row.
- Game log update finality is currently based on nonblank `Game Result`.

Suspected gap, not fixed by this issue:

- `MatchSummary.set_game_winner(...)` stores any winner value except `None` and
  `""`. Parser state and GRE parser paths avoid several unknown winner values,
  but provenance must not overstate confidence if unknown-like values reach
  `GameSummary.winner_team` through another path. Correcting behavior requires
  a separate scoped contract.

## Scope Decision

Codex C should convert the Tier 3 `game_level_facts` family from purely
registered future metadata into a seeded game-result provenance slice.

Required Tier 3 seed fields:

- `game_number`
- `game1_winner_team`
- `game2_winner_team`
- `game3_winner_team`
- `game1_result`
- `game2_result`
- `game3_result`

Required Tier 3 entries:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier3.game_results.game_number` | `game_number` | `Game Number` | `observed` or `derived` |
| `tier3.game_results.game1_winner_team` | `game1_winner_team` | `g1_winner_team` | `observed` |
| `tier3.game_results.game2_winner_team` | `game2_winner_team` | `g2_winner_team` | `observed` |
| `tier3.game_results.game3_winner_team` | `game3_winner_team` | `g3_winner_team` | `observed` |
| `tier3.game_results.game1_result` | `game1_result` | `Game 1 Result` | `derived` |
| `tier3.game_results.game2_result` | `game2_result` | `Game 2 Result` | `derived` |
| `tier3.game_results.game3_result` | `game3_result` | `Game 3 Result` | `derived` |

Required family metadata:

- `game_level_facts.status` should become `seeded_sample`.
- `game_level_facts.seed_fields` should list the seven seed fields above.
- `game_level_facts.future_fields` should keep the remaining unmapped Tier 3
  areas, at minimum:
  - `play_draw`
  - `mulligans`
  - `turn_count`
  - `opening_hand`
- Do not add a new family status in issue #134.

## Deferred Work

Defer full provenance for:

- play/draw
- starting player
- mulligans
- opening-hand size
- exact opening hand
- mulliganed-away cards
- turn count
- game timing
- game duration
- pre/postboard labels
- sideboarding and deck-state facts
- runtime field-evidence attachment
- drift reports
- schema snapshots
- invariant execution
- diagnostics, replay, or feature-equity report-shape changes

Issue #134 may reference those fields as context, but it must not map them as
complete ledger entries.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier3_game_results.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier3_game_results_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier3_game_results.md

Referenced but not owned:

- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/parser_gre_game_result.md
- docs/contracts/parser_match_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_state.md
- docs/contracts/parser_sheet_schema.md
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/parsers/gre/game_result.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- src/mythic_edge_parser/parsers/match_state.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/app/golden_replay.py
- tests/test_state.py
- tests/test_gre_game_result_parser.py
- tests/test_match_summary_from_match_state.py
- tests/test_app_models.py
- tests/test_golden_replay_harness.py
- tests/fixtures/golden_replay/*.manifest.json
- tests/fixtures/parser_regression_*_expected.json

## Public Interface

Recommended implementation surface:

```python
src/mythic_edge_parser/app/evidence_ledger.py
```

Public constants and functions from #128, #130, and #132 must remain stable:

- `LEDGER_OBJECT`
- `LEDGER_SCHEMA_VERSION`
- `LEDGER_VERSION`
- `FIELD_EVIDENCE_OBJECT`
- `FIELD_EVIDENCE_SCHEMA_VERSION`
- `VALUE_SOURCES`
- `CONFIDENCE_LEVELS`
- `FINALITY_LABELS`
- `INVARIANT_STATUSES`
- `DRIFT_FLAGS`
- `build_player_log_evidence_ledger()`
- `iter_ledger_entries()`
- `validate_player_log_evidence_ledger(...)`
- `validate_ledger_entry(...)`
- `validate_field_evidence(...)`

No new runtime parser API is required.

Required ledger-entry behavior:

- `iter_ledger_entries()` remains deep-copy safe.
- `build_player_log_evidence_ledger()` remains deterministic and JSON
  serializable.
- Every new Tier 3 entry passes `validate_ledger_entry(...)`.
- The built ledger passes `validate_player_log_evidence_ledger(...)`.
- Entry IDs and signal IDs remain stable, lowercase, and dot-separated.
- Source paths remain repo-relative or symbolic.
- Raw payload values, raw private log excerpts, absolute local paths, secrets,
  webhook URLs, local runtime artifacts, generated data, failed posts, and
  workbook exports must not be embedded.

## Inputs And Dependencies

The ledger describes these parser-owned dependencies; it does not consume live
events at runtime in this issue.

### Game Slot Identity

Source surfaces:

- `GameResult.payload.identity.game_number`
- `GameResult.payload.game_info.gameNumber`
- `GameState.identity.game_number`
- parser context `current_game_number`
- `MatchState.game_results[]` ordered list position

Policy:

- Direct game-number evidence is `observed` when it comes from `GameResult` or
  `GameState` identity/game-info fields.
- Parser-context fallback is `derived` and provisional.
- `MatchState.game_results[]` list position is a medium-confidence derived
  mapping to fixed game slots.
- Valid game slots for this contract are games 1, 2, and 3, matching current
  `MatchSummary` slots.
- Invalid or missing game numbers must not attach evidence to a guessed slot.

### Game Winner Evidence

Preferred direct evidence:

- latest known nested `GameResult.results[]` entry whose scope normalizes to
  `MatchScope_Game` / `Game`
- `MatchState.game_results[]` entry whose scope normalizes to
  `MatchScope_Game` / `Game`, mapped by list order

Fallback evidence:

- top-level `GameResult.payload.winning_team_id` only for legacy/manual
  `GameResult` payloads that have no nested `results` list
- parser-produced top-level `winning_team_id` may describe the selected latest
  game-scope winner, but nested `results[]` remains the stronger provenance
  when present

Forbidden evidence:

- match-scope `GameResult.results[]`
- match-scope `MatchState.game_results[]`
- match winner
- game aggregates
- workbook formulas
- dashboard logic
- Apps Script state
- AI or analytics output

Unknown winner semantics:

- `None`, `""`, `0`, `0.0`, `"0"`, `" 0 "`, and booleans are unknown winner
  values for provenance purposes.
- Unknown winner values must not be represented as high-confidence game
  winners.
- Unknown winner values must not overwrite a previously known game winner in
  provenance language.
- Non-zero winner values are valid without hard-coding only teams `1` and `2`.

### Player-Facing Game Result Derivation

Source surfaces:

- `GameSummary.result_for_player(player_team)`
- `MatchSummary._game_result_fields()`
- `MatchSummary.to_match_log_row(final=...)`
- `GameSummary.to_game_log_row(match)`
- `MatchSummary.player_team`
- per-game `GameSummary.winner_team`

Policy:

- Player-facing result is `derived`, not raw-log `observed`.
- Current values are `"W"`, `"L"`, or blank.
- High confidence requires known local player team and high-confidence game
  winner evidence for that slot.
- Missing player team prevents high-confidence `W` / `L`.
- Missing game winner yields blank/unknown, not an inferred loss.
- A game not played and a played game with missing result must be distinguishable
  in future field evidence:
  - not played: `not_applicable` invariant status or expected blank
  - played but missing/degraded result: `unknown` or `degraded` with review
    required when evidence indicates the game should have a result

## Output Entries

### `tier3.game_results.game_number`

Field meaning:

- Parser field: game slot identity used by `MatchSummary.game(...)`
- Workbook-facing alias: `Game Number` in game-log rows
- Match-row relationship: game slots 1, 2, and 3

Required evidence policy:

- `observed` from `GameResult.identity.game_number`,
  `GameResult.game_info.gameNumber`, or `GameState.identity.game_number`.
- `derived` from parser context `current_game_number`.
- `derived` from `MatchState.game_results[]` ordered list position.
- `unknown` when no valid slot is available.

Required signal examples:

- `game_result.identity.game_number`
- `game_result.game_info.game_number`
- `game_state.identity.game_number`
- `parser_context.current_game_number`
- `match_state.game_results.list_order`

Required invariants:

- game number must be 1, 2, or 3 for this contract
- per-game result entries must not attach to an unknown game number
- game-log row identity must remain `(MTGA Match ID, Game Number)`

### `tier3.game_results.game1_winner_team`

Field meaning:

- Parser field: `MatchSummary.games[1].winner_team`
- Debug alias: `g1_winner_team`
- Downstream result alias: `Game 1 Result`

Required evidence policy:

- `observed` from game-scope `GameResult.results[]` for game slot 1.
- `observed` from game-scope `MatchState.game_results[0]` by ordered list
  mapping.
- `observed` with medium confidence from top-level legacy `GameResult`
  `winning_team_id` only when no nested results list exists and slot identity is
  game 1.
- `unknown` when winner evidence is missing, unknown-like, contradictory, or
  attached to no valid slot.

Required signal examples:

- `game_result.game1.game_scope_winner`
- `match_state.game_results.game1_scope_winner`
- `game_result.game1.top_level_legacy_winner`

### `tier3.game_results.game2_winner_team`

Field meaning:

- Parser field: `MatchSummary.games[2].winner_team`
- Debug alias: `g2_winner_team`
- Downstream result alias: `Game 2 Result`

Required evidence policy:

- Same as game 1, scoped to game slot 2.
- `MatchState.game_results[1]` is the ordered list mapping for game 2.
- Blank game 2 may be expected for best-of-one or unplayed game 2, but not if
  evidence says game 2 completed.

Required signal examples:

- `game_result.game2.game_scope_winner`
- `match_state.game_results.game2_scope_winner`
- `game_result.game2.top_level_legacy_winner`

### `tier3.game_results.game3_winner_team`

Field meaning:

- Parser field: `MatchSummary.games[3].winner_team`
- Debug alias: `g3_winner_team`
- Downstream result alias: `Game 3 Result`

Required evidence policy:

- Same as game 1, scoped to game slot 3.
- `MatchState.game_results[2]` is the ordered list mapping for game 3.
- Blank game 3 may be expected when a match ends in one or two games, but not
  if evidence says game 3 completed.

Required signal examples:

- `game_result.game3.game_scope_winner`
- `match_state.game_results.game3_scope_winner`
- `game_result.game3.top_level_legacy_winner`

### `tier3.game_results.game1_result`

Field meaning:

- Parser field: `MatchSummary._game_result_fields()["g1_result"]`
- Model surface: `GameSummary.result_for_player(match.player_team)`
- Workbook-facing alias: `Game 1 Result`
- Game-log relationship: `Game Result` when `Game Number == 1`

Required evidence policy:

- `derived` from `game1_winner_team` plus `MatchSummary.player_team`.
- `unknown` or blank when winner or player team is missing.
- `conflict` when the winner dependency conflicts with other game 1 evidence.
- Must not infer from `games_won`, `match_result`, match winner, match format,
  workbook formulas, or AI.

Required signal examples:

- `parser_state.match_summary.game1_result`
- `ledger.tier3.game_results.game1_winner_team_dependency`
- `parser_state.match_summary.player_team_dependency`

### `tier3.game_results.game2_result`

Field meaning:

- Parser field: `MatchSummary._game_result_fields()["g2_result"]`
- Model surface: `GameSummary.result_for_player(match.player_team)`
- Workbook-facing alias: `Game 2 Result`
- Game-log relationship: `Game Result` when `Game Number == 2`

Required evidence policy:

- Same as game 1, scoped to game slot 2.
- Blank game 2 is expected when game 2 was not played.
- Blank game 2 is degraded/review-worthy when evidence indicates game 2
  completed but no player-facing result can be derived.

Required signal examples:

- `parser_state.match_summary.game2_result`
- `ledger.tier3.game_results.game2_winner_team_dependency`
- `parser_state.match_summary.player_team_dependency`

### `tier3.game_results.game3_result`

Field meaning:

- Parser field: `MatchSummary._game_result_fields()["g3_result"]`
- Model surface: `GameSummary.result_for_player(match.player_team)`
- Workbook-facing alias: `Game 3 Result`
- Game-log relationship: `Game Result` when `Game Number == 3`

Required evidence policy:

- Same as game 1, scoped to game slot 3.
- Blank game 3 is expected when game 3 was not played.
- Blank game 3 is degraded/review-worthy when evidence indicates game 3
  completed but no player-facing result can be derived.

Required signal examples:

- `parser_state.match_summary.game3_result`
- `ledger.tier3.game_results.game3_winner_team_dependency`
- `parser_state.match_summary.player_team_dependency`

## Confidence And Finality Rules

Game-number confidence:

- `high`: observed game number from parser-owned event identity or game info.
- `medium`: parser context fallback or MatchState result-list ordering.
- `unknown`: no valid slot.
- `low`: conflicting game numbers for the same event or row.

Game-winner confidence:

- `high`: known nested game-scope result with valid game slot.
- `medium`: MatchState ordered-list mapping or top-level legacy GameResult
  fallback with valid slot.
- `low`: contradictory game-scope evidence, unknown-like winner values reaching
  state, or degraded/truncated evidence.
- `unknown`: missing winner or missing slot.

Player-facing result confidence:

- `high`: high-confidence winner plus known local player team.
- `medium`: medium-confidence winner plus known local player team.
- `low`: conflicting winner or player-team evidence.
- `unknown`: missing winner or missing player team.

Finality:

- `live`: in-progress game evidence before a game result is known.
- `provisional`: partial result evidence or fallback-derived slot mapping.
- `final`: known game result evidence used by current parser state.
- `reconciled`: future field-evidence attachment records a later stronger
  correction.

Data-loss and truncation:

- Truncation/data-loss evidence may lower confidence or require review in
  future field evidence.
- This issue should only document that relationship. It must not reconstruct
  missing data or change diagnostics/replay report shapes.

## Invariants

- Tier 3 game result entries must use output family `game_level_facts`.
- Game slot identity must be 1, 2, or 3.
- Game winner entries must not use match-scope result evidence.
- Match winner must not be promoted into game winner.
- Game aggregates must not invent missing per-game winners.
- Player-facing game result must be derived from game winner plus local player
  team.
- Missing local player team prevents high-confidence `Game N Result`.
- Missing game winner yields blank/unknown `Game N Result`, not an inferred
  loss.
- Unknown-like winners (`None`, `""`, `0`, `0.0`, `"0"`, `" 0 "`, booleans)
  must not become high-confidence winners.
- `GameLogRow` finality remains a downstream state decision based on nonblank
  `Game Result`; the ledger must not change that rule.
- Issue #132 aggregate entries may cite Tier 3 dependencies, but aggregate math
  remains unchanged.

## Error Behavior

Malformed or missing ledger metadata:

- Validators must report errors rather than raising for ordinary malformed
  payloads.
- Duplicate entry IDs and duplicate signal IDs must be reported.
- Unknown vocabulary values must be reported.
- Absolute paths, raw log-like text, secret-like text, webhook-like URLs, raw
  private logs, generated data paths, runtime status paths, failed-post paths,
  and workbook-export references must be rejected by privacy validation.

Missing source evidence:

- Missing game number yields unknown slot evidence.
- Missing winner yields unknown winner evidence.
- Missing player team yields unknown/degraded player-facing result evidence.
- A not-played game may have expected blank result evidence.
- A played or completed game with missing result evidence should be degraded or
  review-required in future field-evidence output.

Contradictory source evidence:

- Contradictory winners for the same game slot should use `conflict`, low
  confidence, `conflicting_evidence`, and `review_required` in future
  field-evidence output.
- Issue #134 implementation should only describe this behavior in ledger
  entries; it must not implement runtime conflict resolution.

## Side Effects

This contract pass writes only:

- docs/contracts/player_log_evidence_ledger_tier3_game_results.md

Future Codex C implementation may change only:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier3_game_results_comparison.md

Future Codex C should not change parser behavior, parser state mutation,
workbook sync, webhook posts, Apps Script, output transport, runtime status
files, failed posts, raw logs, generated data, workbook exports, diagnostics
reports, replay reports, feature-equity reports, drift reports, schema
snapshots, or invariant execution machinery.

## Dependency Order

Codex C should implement in this order:

1. Compare `evidence_ledger.py` and `tests/test_evidence_ledger.py` against
   this contract.
2. Preserve all #128, #130, and #132 constants, validators, and entries.
3. Update `game_level_facts` family metadata to `seeded_sample` and add the
   seven Tier 3 game-result seed fields.
4. Add the game-number entry.
5. Add game 1/2/3 winner-team entries.
6. Add game 1/2/3 player-facing result entries.
7. Update #132 aggregate entry notes or dependency signals only as needed to
   reference the new Tier 3 entries.
8. Add focused tests for family metadata, entry IDs, source/fallback policy,
   unknown winner semantics, slot identity, aggregate dependency references,
   validation, privacy, copy safety, and deterministic serialization.
9. Run focused evidence-ledger tests and adjacent parser/state tests.
10. Produce the implementation handoff.

## Compatibility

- Existing workbook-facing field names must remain unchanged:
  - `Game 1 Result`
  - `Game 2 Result`
  - `Game 3 Result`
  - `Game Result`
  - `Game Number`
- Existing debug/history field names must remain unchanged:
  - `g1_winner_team`
  - `g2_winner_team`
  - `g3_winner_team`
  - `g1_result`
  - `g2_result`
  - `g3_result`
- Existing #128/#130/#132 public constants, validators, and ledger build
  functions must remain available.
- Existing #128/#130/#132 entry IDs must remain stable.
- Existing value-source, confidence, finality, invariant-status, and drift-flag
  vocabularies must remain stable.
- Existing `MATCH_LOG_SYNC_FIELDS` and `GAME_LOG_SYNC_FIELDS` must remain
  unchanged.
- Existing golden replay manifest shapes must remain unchanged.

## Tests Required

Future implementation should run at minimum:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_state.py
python3 -m pytest -q tests/test_gre_game_result_parser.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m ruff check src tests tools
git diff --check
```

Recommended if implementation remains ledger metadata plus tests:

```bash
python3 -m pytest -q tests/test_app_models.py tests/test_match_summary_from_match_state.py
python3 -m pytest -q
```

Recommended focused assertions:

- Built ledger validates cleanly.
- Tier 3 `game_level_facts` family has status `seeded_sample`.
- Tier 3 seed fields contain the seven contracted fields.
- Remaining Tier 3 future fields still list deferred areas.
- `iter_ledger_entries()` contains all existing entries plus seven Tier 3 game
  result entries.
- Winner-team entries use `observed` direct evidence and include nested
  GameResult and MatchState game-scope signals.
- Winner-team entries document top-level legacy GameResult fallback.
- Winner-team entries reject match-scope promotion in invariant/degradation
  text.
- Result entries use `derived` direct evidence and cite winner-team plus
  player-team dependencies.
- Result entries distinguish expected blank not-played games from
  played-but-missing/degraded results.
- Aggregate entries from #132 cite Tier 3 game result dependencies in notes or
  signal text.
- Entry privacy validation still rejects raw-log-like text and absolute paths.
- Serialization remains deterministic and copy safe.

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_tier3_game_results.md` exists.
- The contract preserves parser truth ownership.
- The contract separates observed current behavior from required ledger
  metadata guarantees.
- The contract preserves #128 schema/vocabulary and all #130/#132 entries.
- The contract defines exact Tier 3 game result entry IDs and field names.
- The contract maps preferred and fallback evidence sources for game number,
  game winner, and player-facing game result.
- The contract keeps match-scope result evidence out of game winner truth.
- The contract keeps per-game result provenance distinct from Tier 1 aggregate
  provenance.
- The contract defers non-result Tier 3 work.
- The contract lists implementation files, validation commands, and protected
  surfaces.
- The contract routes to Codex C with a pasteable handoff.

## Open Questions And Contract Risks

- Current ledger family statuses have only `seeded_sample` and
  `registered_future`. Moving Tier 3 to `seeded_sample` is the best available
  label, but a future schema cleanup may want a clearer status.
- MatchState game results are ordered-list mapped rather than explicitly
  game-numbered. The contract marks that as medium-confidence derived slot
  evidence rather than direct slot identity.
- Some model paths can carry unknown-like winner values if they reach
  `GameSummary.winner_team` outside protected parser paths. This issue records
  the provenance risk but does not authorize behavior changes.
- Distinguishing "not played" from "played but missing result" will need future
  runtime field-evidence attachment or diagnostics context; this issue only
  defines the vocabulary and review posture.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #134, Tier 3 game-level result provenance under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/134
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/132
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/133
- Previous merge commit: 9496026047f4817cad8456324d376ae33faa5968
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier3-game-results
- Contract: docs/contracts/player_log_evidence_ledger_tier3_game_results.md

Goal:
Compare the current evidence ledger implementation and focused tests against the Tier 3 game result contract. Implement only the smallest metadata/test changes needed to add game-level result provenance entries.

Use:
- docs/contracts/player_log_evidence_ledger_tier3_game_results.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/parser_gre_game_result.md
- docs/contracts/parser_match_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_state.md
- docs/contracts/parser_sheet_schema.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/parsers/gre/game_result.py
- src/mythic_edge_parser/parsers/match_state.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/app/golden_replay.py
- tests/test_state.py
- tests/test_gre_game_result_parser.py
- tests/test_app_models.py
- tests/test_match_summary_from_match_state.py
- tests/test_golden_replay_harness.py

Do:
- Preserve the #128 schema, validators, vocabulary constants, and match_id anchor entry.
- Preserve all #130 and #132 entries.
- Update the Tier 3 game_level_facts family from registered future metadata to a seeded game-result provenance slice.
- Add entries for game_number, game1_winner_team, game2_winner_team, game3_winner_team, game1_result, game2_result, and game3_result.
- Keep play/draw, mulligan, turn-count, opening-hand, timing, duration, pre/postboard, sideboarding, and deck-state provenance deferred.
- Use existing value-source, confidence, finality, invariant-status, and drift-flag vocabulary only.
- Preserve parser-owned truth boundaries.
- Add focused tests for the expanded Tier 3 entry set, game-scope source policy, match-scope non-promotion, unknown winner semantics, slot identity, aggregate dependency references, expected blank behavior, validation, privacy, copy safety, and deterministic serialization.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_tier3_game_results_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser behavior.
- Change parser state final reconciliation.
- Change parser event classes.
- Change workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or AI/analytics truth.
- Implement runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, or feature-equity report changes.
- Reconstruct missing GameState data or infer facts that Player.log did not provide.
- Promote match-scope results into game-level results.
- Commit raw private Player.log excerpts.
- Target main directly.
- Close issue #11.
- Stage or commit unless explicitly asked.

Validation:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_state.py
- python3 -m pytest -q tests/test_gre_game_result_parser.py
- python3 -m pytest -q tests/test_golden_replay_harness.py
- python3 -m ruff check src tests tools
- git diff --check
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/134"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/132"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/133"
  previous_merge_commit: "9496026047f4817cad8456324d376ae33faa5968"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_game_results.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_game_results_comparison.md"
  verdict: "ready_for_module_implementer"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-game-results"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_state.py"
    - "python3 -m pytest -q tests/test_gre_game_result_parser.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, or AI/analytics truth."
    - "Do not reconstruct missing GameState data or infer facts that Player.log did not provide."
    - "Do not promote match-scope results into game-level results."
    - "Do not implement runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, or feature-equity report changes."
    - "Do not commit raw private Player.log excerpts."
```
