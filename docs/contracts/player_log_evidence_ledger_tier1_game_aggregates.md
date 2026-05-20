# Player.log Evidence Ledger Tier 1 Game Aggregates Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/132
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/130
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/131
- previous_merge_commit: c5e4aa9952ba2026ecf5a0778254701c521fa278
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier1-game-aggregates
- target_artifact: docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier1_game_aggregates_comparison.md
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
- docs/contracts/parser_models.md
- docs/contracts/parser_state.md
- docs/contracts/parser_sheet_schema.md
- docs/decisions/ADR-0003-player-log-drift-policy.md

## Purpose

Issue #130 expanded the Player.log evidence ledger across Tier 1 match identity,
timing, match winner, match result, and sync-status fields. It deliberately
left the game-derived aggregate fields in the Tier 1 future list.

Issue #132 maps those deferred aggregate fields. These outputs are
parser-owned, user-facing, and high value, but they are not directly observed
raw Player.log facts. They are computed by `MatchSummary` from per-game winner
state, local player-team state, and already-mapped match-result state.

This contract defines provenance metadata only. It does not change aggregate
math, final reconciliation, game-winner handling, workbook row shape, webhook
transport, Apps Script behavior, or analytics truth.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
the schema, validators, privacy posture, and vocabulary constants.

`docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md` remains
authoritative for the already mapped Tier 1 fields:

- `match_id`
- `match_started_at`
- `match_finished_at`
- `match_winner_team`
- `match_result`
- `match_sync_status`

Issue #132 must preserve those entries and add the aggregate entries that #130
deferred:

- `games_won`
- `games_lost`
- `total_games`
- `match_win_flag`
- `game_win_rate`

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #132 provenance should be
recorded through this contract, the implementation handoff, entry notes, and
focused tests rather than by changing the top-level ledger object shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- `src/mythic_edge_parser/app/models.py` owns current aggregate math.
- `src/mythic_edge_parser/app/state.py` owns how game winners and local player
  team reach `MatchSummary`.
- `src/mythic_edge_parser/app/evidence_ledger.py` describes provenance,
  confidence, finality, degradation, and review expectations.
- The evidence ledger must not compute aggregates at runtime, infer missing
  games, infer missing winners, alter row values, or decide parser truth.
- Workbook formulas, dashboard logic, Apps Script, webhook transport,
  diagnostics, drift reports, golden replay, feature-equity reports, and AI
  output remain downstream consumers.

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` after PR #131:

- Tier 1 output family `match_identity_and_lifecycle` has six seed fields from
  #130 and five aggregate future fields.
- `tests/test_evidence_ledger.py` currently asserts that aggregate fields remain
  deferred.
- `MatchSummary.game_wins` returns `0` when `player_team` is missing; otherwise
  it counts games whose `winner_team == player_team`.
- `MatchSummary.game_losses` counts games whose `winner_team` is not `None` or
  `""`, then subtracts `game_wins`.
- `MatchSummary.total_games` returns `game_wins + game_losses`.
- `MatchSummary.match_win_flag` returns `""` when `match_wl` is blank, `1` for
  `"W"`, and `0` otherwise.
- `MatchSummary.game_win_rate` returns `""` when `total_games == 0`; otherwise
  it returns `game_wins / total_games`.
- `MatchSummary.to_debug_dict()` exposes `game_wins`, `game_losses`,
  `total_games`, `match_win_flag`, and `game_win_rate`.
- `MatchSummary.to_history_item()` exposes `games_won`, `games_lost`,
  `total_games`, `match_win_flag`, and `game_win_rate`.
- `MatchSummary.to_match_log_row(...)` exposes workbook aliases:
  - `Games Won`
  - `Games Lost`
  - `Total Games`
  - `Match Win Flag`
  - `Game Win %`
- In workbook-facing match-log rows, `Games Won`, `Games Lost`, and
  `Total Games` are blank when `total_games == 0`.
- In workbook-facing match-log rows, `Game Win %` is blank when
  `total_games == 0`.
- Live match rows can show provisional game aggregates before the match is
  final.

Suspected gap, not fixed by this issue:

- `MatchSummary.set_game_winner(...)` currently stores any winner value except
  `None` and `""`. Parser state protects some `GameResult` paths with known
  winner checks, but aggregate provenance must not overstate confidence when a
  dependency carries an unknown-like winner value such as `0` or `"0"`.
  Correcting any underlying behavior requires a separate scoped contract.

## Scope Decision

Codex C should add full ledger entries for all five aggregate fields in one
coherent implementation pass:

| Entry ID | Parser field | Workbook alias | Required source label |
| --- | --- | --- | --- |
| `tier1.match_aggregates.games_won` | `MatchSummary.game_wins` | `Games Won` | `derived` |
| `tier1.match_aggregates.games_lost` | `MatchSummary.game_losses` | `Games Lost` | `derived` |
| `tier1.match_aggregates.total_games` | `MatchSummary.total_games` | `Total Games` | `derived` |
| `tier1.match_aggregates.match_win_flag` | `MatchSummary.match_win_flag` | `Match Win Flag` | `derived` |
| `tier1.match_aggregates.game_win_rate` | `MatchSummary.game_win_rate` | `Game Win %` | `derived` |

These entries should stay in output family `match_identity_and_lifecycle`.
The `match_aggregates` segment belongs in entry IDs only; it does not require a
new output family in this issue.

Codex C should update Tier 1 family metadata so these five fields move from
`future_fields` to the mapped seed field set, using the existing #128 status
vocabulary. Do not add a new family status in issue #132.

## Deferred Work

Defer full ledger entries for per-game facts to a later Tier 3 game-level facts
issue:

- `Game 1 Result`
- `Game 2 Result`
- `Game 3 Result`
- game-level winner-team fields
- play/draw provenance
- mulligan provenance
- turn-count provenance
- opening-hand provenance

Issue #132 may reference these fields as aggregate dependencies, but it must
not claim that Tier 3 game-level provenance is complete.

Also defer:

- runtime field-evidence attachment
- drift report generation
- schema snapshots
- invariant execution machinery
- diagnostics, golden replay, or feature-equity report-shape changes
- participant/player-team provenance beyond dependency language
- workbook schema or webhook payload changes
- parser state behavior changes

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier1_game_aggregates_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier1_game_aggregates.md

Referenced but not owned:

- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/parser_models.md
- docs/contracts/parser_state.md
- docs/contracts/parser_sheet_schema.md
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/app/golden_replay.py
- tests/test_state.py
- tests/test_app_models.py
- tests/test_golden_replay_harness.py
- tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json
- tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json

## Public Interface

Recommended implementation surface:

```python
src/mythic_edge_parser/app/evidence_ledger.py
```

Public constants and functions from #128 and #130 must remain stable:

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
- Every new aggregate entry passes `validate_ledger_entry(...)`.
- The built ledger passes `validate_player_log_evidence_ledger(...)`.
- Entry IDs and signal IDs remain stable, lowercase, and dot-separated.
- Source paths remain repo-relative or symbolic.
- Raw payload values, raw private log excerpts, absolute local paths, secrets,
  webhook URLs, local runtime artifacts, generated data, failed posts, and
  workbook exports must not be embedded.

## Inputs And Dependencies

The ledger describes these parser-owned dependencies; it does not consume live
events at runtime in this issue.

### Game Winner Dependencies

Source surfaces:

- `MatchSummary.games[1].winner_team`
- `MatchSummary.games[2].winner_team`
- `MatchSummary.games[3].winner_team`
- `GameSummary.winner_team`
- `MatchSummary._game_winner_fields()`

Source modules:

- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/state.py`

Dependency meaning:

- Per-game winner state is the input used by aggregate math.
- Per-game winner provenance is not fully mapped in this issue.
- A winner dependency is high confidence only when it came from parser-owned
  game result evidence and does not carry an unknown-like value.
- Unknown-like winner values, missing game numbers, or contradictory game
  winners should make future aggregate field evidence degraded or
  review-required.

### Local Player Team Dependency

Source surfaces:

- `MatchSummary.player_team`
- `state._set_local_team(...)`
- `GameSummary.result_for_player(player_team)`

Dependency meaning:

- `game_wins`, `game_losses`, `game_result`, and `game_win_rate` depend on the
  local player team.
- Missing local player team prevents high-confidence aggregate evidence even if
  game winners exist.
- Issue #132 does not fully map participant provenance.

### Match Result Dependency

Source surfaces:

- `MatchSummary.match_wl`
- `MatchSummary.match_win_flag`
- Existing ledger entry `tier1.match_result.match_result`

Dependency meaning:

- `match_win_flag` is derived from match result, not directly from game totals.
- `match_win_flag` must agree with `Match Win?`.
- A blank `match_wl` yields a blank `match_win_flag`.

### Aggregate Math Dependencies

Source surfaces:

- `MatchSummary.game_wins`
- `MatchSummary.game_losses`
- `MatchSummary.total_games`
- `MatchSummary.game_win_rate`

Dependency meaning:

- `total_games` is derived from wins plus losses.
- `game_win_rate` is derived from wins divided by total games when
  `total_games > 0`.
- Blank `Game Win %` with no completed games is expected, not a zero win rate.

## Output Entries

### `tier1.match_aggregates.games_won`

Field meaning:

- Parser field: `MatchSummary.game_wins`
- Debug/history aliases: `game_wins`, `games_won`
- Workbook-facing alias: `Games Won`

Required evidence policy:

- The value is `derived`, not raw-log `observed`.
- Direct ledger evidence should reference `MatchSummary.game_wins`.
- Dependency evidence should reference per-game `winner_team` fields and
  `MatchSummary.player_team`.
- High confidence requires known local player team and high-confidence
  per-game winner dependencies.
- Live rows may carry provisional wins for completed games observed so far.
- Final rows may carry final wins only when underlying game-winner and player
  team dependencies are final enough under current parser-state rules.

Missing/degraded behavior:

- Missing `player_team` prevents high-confidence wins. Current model may return
  `0`; future field evidence should mark that as degraded/unknown rather than
  confidently "zero wins."
- Missing game winners are not counted as wins and must not be invented.
- Unknown-like winner values such as `0` or `"0"` should make future field
  evidence review-required if they affect the count.
- Workbook-facing `Games Won` is blank when `total_games == 0`.

Required signal examples:

- `parser_state.match_summary.game_wins`
- `parser_state.match_summary.game_winner_dependencies`
- `parser_state.match_summary.player_team_dependency`

### `tier1.match_aggregates.games_lost`

Field meaning:

- Parser field: `MatchSummary.game_losses`
- Debug/history aliases: `game_losses`, `games_lost`
- Workbook-facing alias: `Games Lost`

Required evidence policy:

- The value is `derived`, not raw-log `observed`.
- Direct ledger evidence should reference `MatchSummary.game_losses`.
- Dependency evidence should reference completed-game winner state,
  `MatchSummary.game_wins`, and `MatchSummary.player_team`.
- Current model derives losses as completed games minus wins.
- High confidence requires known local player team and high-confidence
  completed-game winner dependencies.
- Live rows may carry provisional losses for completed games observed so far.

Missing/degraded behavior:

- Missing `player_team` prevents high-confidence losses. Current model may
  count completed games as losses if local team is missing; future field
  evidence must mark that condition degraded/review-required.
- Missing game winners are not completed games and must not be treated as
  losses.
- Unknown-like winner values should make future field evidence review-required.
- Workbook-facing `Games Lost` is blank when `total_games == 0`.

Required signal examples:

- `parser_state.match_summary.game_losses`
- `parser_state.match_summary.completed_game_dependencies`
- `parser_state.match_summary.game_wins_dependency`
- `parser_state.match_summary.player_team_dependency`

### `tier1.match_aggregates.total_games`

Field meaning:

- Parser field: `MatchSummary.total_games`
- Debug/history alias: `total_games`
- Workbook-facing alias: `Total Games`

Required evidence policy:

- The value is `derived`, not raw-log `observed`.
- Direct ledger evidence should reference `MatchSummary.total_games`.
- Dependency evidence should reference `MatchSummary.game_wins` and
  `MatchSummary.game_losses`.
- `total_games` must represent completed games known to parser state, not a
  guessed match length or expected best-of count.
- Do not infer missing game results from match format, sideboarding evidence,
  workbook formulas, or AI output.

Missing/degraded behavior:

- `total_games == 0` means no completed game winners are represented by current
  aggregate math.
- Workbook-facing `Total Games` is blank when `total_games == 0`.
- Blank `Total Games` with no completed game evidence is expected.
- Blank or low total games in a final match may still require review if future
  field evidence has reason to expect game-result evidence.
- Impossible totals, negative totals, or totals that disagree with wins plus
  losses must be review-required.

Required signal examples:

- `parser_state.match_summary.total_games`
- `parser_state.match_summary.game_wins_dependency`
- `parser_state.match_summary.game_losses_dependency`

### `tier1.match_aggregates.match_win_flag`

Field meaning:

- Parser field: `MatchSummary.match_win_flag`
- Workbook-facing alias: `Match Win Flag`

Required evidence policy:

- The value is `derived`, not raw-log `observed`.
- Direct ledger evidence should reference `MatchSummary.match_win_flag`.
- Dependency evidence should reference `MatchSummary.match_wl` and existing
  entry `tier1.match_result.match_result`.
- `match_win_flag` is a numeric alias of match result:
  - `1` for match result `"W"`
  - `0` for match result `"L"`
  - `""` when match result is blank/unknown
- It must not be independently inferred from `games_won`, `games_lost`, best-of
  structure, workbook formulas, or AI output.

Missing/degraded behavior:

- Missing or degraded `match_result` yields blank or degraded
  `match_win_flag`.
- Conflict between `match_win_flag` and `Match Win?` is review-required.
- A blank `Match Win Flag` when `Match Win?` is blank is expected.

Required signal examples:

- `parser_state.match_summary.match_win_flag`
- `parser_state.match_summary.match_wl_dependency`
- `ledger.tier1.match_result.match_result_dependency`

### `tier1.match_aggregates.game_win_rate`

Field meaning:

- Parser field: `MatchSummary.game_win_rate`
- Debug/history alias: `game_win_rate`
- Workbook-facing alias: `Game Win %`

Required evidence policy:

- The value is `derived`, not raw-log `observed`.
- Direct ledger evidence should reference `MatchSummary.game_win_rate`.
- Dependency evidence should reference `MatchSummary.game_wins` and
  `MatchSummary.total_games`.
- When `total_games > 0`, `game_win_rate` must equal
  `game_wins / total_games`.
- When `total_games == 0`, `game_win_rate` is blank. That blank is expected and
  should be modeled as not applicable, not as `0.0`.

Missing/degraded behavior:

- Missing or degraded `game_wins` or `total_games` makes `game_win_rate`
  degraded or unknown.
- Division-by-zero must not happen.
- A blank rate with no completed games is expected and should not require review
  by itself.
- A blank rate with completed games, a nonblank rate with zero completed games,
  a negative rate, or a rate outside `0 <= rate <= 1` is review-required.

Required signal examples:

- `parser_state.match_summary.game_win_rate`
- `parser_state.match_summary.game_wins_dependency`
- `parser_state.match_summary.total_games_dependency`

## Confidence And Finality Rules

All five aggregate entries:

- `value_source_policy.direct` must be `derived`.
- `value_source_policy.fallback` must be `derived`.
- `value_source_policy.missing` must be `unknown`.
- `value_source_policy.contradiction` must be `conflict`.

Confidence:

- `high`: all required dependencies are parser-owned and high-confidence.
- `medium`: live/provisional rows with partial but coherent completed-game
  evidence.
- `low`: dependency conflict, unknown-like winner values in dependencies, or
  aggregate invariant risk.
- `unknown`: missing required dependency.

Finality:

- `live`: aggregate appears in a live match row before match readiness.
- `provisional`: aggregate depends on partial or not-yet-final game evidence.
- `final`: final match row and dependencies are final enough under current
  parser state.
- `reconciled`: future field-evidence attachment records a later stronger
  correction.

Expected blank distinctions:

- Blank `Games Won`, `Games Lost`, `Total Games`, or `Game Win %` with
  `total_games == 0` is expected for workbook-facing rows.
- Debug/history JSON may expose numeric `0` for counts when workbook-facing
  aliases are blank.
- Blank `Match Win Flag` is expected when `Match Win?` is blank.
- Expected blank output is not the same as unknown source evidence. Future
  field-evidence attachment should use `not_applicable` for expected blank
  rate/count display cases and `unknown` or `degraded` when required evidence is
  missing or contradictory.

## Invariants

- All five aggregate entries must remain Tier 1 entries in
  `match_identity_and_lifecycle`.
- Aggregate fields are derived parser-owned outputs, not raw Player.log
  observed values.
- `games_won + games_lost == total_games` for numeric aggregate values.
- `total_games` must not be negative.
- `games_won` and `games_lost` must not be negative.
- `games_won <= total_games` and `games_lost <= total_games`.
- `game_win_rate == games_won / total_games` when `total_games > 0`.
- `game_win_rate` is blank when `total_games == 0`.
- `game_win_rate` must stay within `0 <= rate <= 1` when numeric.
- `match_win_flag` must agree with `Match Win?`.
- `match_win_flag` must be blank when `Match Win?` is blank.
- `match_win_flag` must not be inferred from game aggregates.
- Game aggregates must not infer missing game winners, missing local player
  team, or missing GameState data.
- Per-game result provenance remains deferred to Tier 3.

## Error Behavior

Malformed or missing ledger metadata:

- Validators must report errors rather than raising for ordinary malformed
  payloads.
- Duplicate entry IDs and duplicate signal IDs must be reported.
- Unknown vocabulary values must be reported.
- Absolute paths, raw log-like text, secret-like text, webhook-like URLs, raw
  private logs, generated data paths, runtime status paths, failed-post paths,
  and workbook-export references must be rejected by privacy validation.

Missing source dependencies:

- Missing player team makes aggregate confidence unknown or degraded.
- Missing per-game winners means those games are not completed for aggregate
  math; do not invent them.
- Missing match result makes `match_win_flag` blank or unknown.
- Missing total-games denominator makes `game_win_rate` unknown or not
  applicable depending on whether there are no completed games or contradictory
  evidence.

Contradictory source dependencies:

- Future field evidence should use `conflict`, low confidence,
  `conflicting_evidence`, and `review_required`.
- Issue #132 implementation should only describe this behavior in ledger
  entries; it must not implement runtime conflict resolution.

Invariant failures:

- Future field evidence should use `invariant_failed`, low confidence, and
  `review_required`.
- Issue #132 implementation should not add invariant execution machinery.

## Side Effects

This contract pass writes only:

- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md

Future Codex C implementation may change only:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier1_game_aggregates_comparison.md

Future Codex C should not change parser behavior, parser state mutation,
workbook sync, webhook posts, Apps Script, output transport, runtime status
files, failed posts, raw logs, generated data, or workbook exports.

## Dependency Order

Codex C should implement in this order:

1. Compare `evidence_ledger.py` and `tests/test_evidence_ledger.py` against
   this contract.
2. Preserve all #128 and #130 constants, validators, and entries.
3. Move aggregate fields from Tier 1 `future_fields` to mapped seed fields,
   using existing schema vocabulary.
4. Add entries for `games_won`, `games_lost`, `total_games`,
   `match_win_flag`, and `game_win_rate`.
5. Add focused tests for entry IDs, output fields, workbook aliases, derived
   source policy, dependency signals, aggregate deferral removal, invariant
   names, expected blank behavior, privacy, validation, copy safety, and
   deterministic serialization.
6. Run focused evidence-ledger tests.
7. Run adjacent parser-state/model/golden replay tests because the contract
   documents aggregate behavior, even though Codex C should not change parser
   behavior.
8. Produce the implementation handoff.

## Compatibility

- Existing workbook-facing field names must remain unchanged:
  - `Games Won`
  - `Games Lost`
  - `Total Games`
  - `Match Win Flag`
  - `Game Win %`
- Existing #128/#130 public constants, validators, and ledger build functions
  must remain available.
- Existing #128/#130 entry IDs must remain stable.
- Existing value-source, confidence, finality, invariant-status, and drift-flag
  vocabularies must remain stable.
- Existing JSON/debug/history field names must remain unchanged.
- Existing `MATCH_LOG_SYNC_FIELDS` must remain unchanged.
- Existing golden replay manifest shapes must remain unchanged.

## Tests Required

Future implementation should run at minimum:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_state.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m ruff check src tests tools
git diff --check
```

Recommended if implementation remains ledger metadata plus tests:

```bash
python3 -m pytest -q tests/test_app_models.py
python3 -m pytest -q
```

Recommended focused assertions:

- Built ledger validates cleanly.
- `iter_ledger_entries()` contains the existing six Tier 1 entries plus five
  aggregate entries.
- Tier 1 `seed_fields` contains all eleven mapped Tier 1 fields.
- Tier 1 `future_fields` no longer contains `games_won`, `games_lost`,
  `total_games`, `match_win_flag`, or `game_win_rate`.
- Aggregate entries have `value_source_policy.direct == "derived"`.
- Aggregate entries reference `MatchSummary` model surfaces.
- `games_won`, `games_lost`, and `total_games` entries include game-winner and
  player-team dependency signals.
- `match_win_flag` references `match_wl` / `match_result` dependency and does
  not claim game-total inference.
- `game_win_rate` references `game_wins` and `total_games` dependencies and
  documents blank/not-applicable behavior for zero completed games.
- Entry invariant names cover totals, flag agreement, and rate calculation.
- Entry privacy validation still rejects raw-log-like text and absolute paths.
- Serialization remains deterministic and copy safe.

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md` exists.
- The contract preserves parser truth ownership.
- The contract separates observed current behavior from required ledger
  metadata guarantees.
- The contract preserves #128 schema/vocabulary and all #130 entries.
- The contract defines all five aggregate ledger entries.
- The contract keeps full per-game fact provenance deferred to Tier 3.
- The contract states that aggregates are derived, not raw observed values.
- The contract defines confidence, finality, expected blank, degraded, unknown,
  and conflict behavior.
- The contract defines invariant and review-required expectations.
- The contract lists implementation files, validation commands, and protected
  surfaces.
- The contract routes to Codex C with a pasteable handoff.

## Open Questions And Contract Risks

- The #128 schema still uses `seeded_sample` for a Tier 1 family that now has
  more than a sample. Do not add a new status in #132, but a later schema
  cleanup may rename this status.
- Aggregate confidence depends on game-winner and player-team provenance that
  is not fully mapped in this issue. The entries must document dependencies
  without pretending Tier 3 provenance is complete.
- Current model behavior can return numeric `0` for aggregate counts in debug
  surfaces while workbook-facing aliases are blank. The contract preserves this
  compatibility and asks future field evidence to distinguish expected blank
  display from unknown evidence.
- Unknown-like per-game winner values can affect aggregate math if they reach
  `GameSummary.winner_team`. This issue records the risk but does not authorize
  behavior changes.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #132, Tier 1 game-derived aggregate provenance under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/132
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/130
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/131
- Previous merge commit: c5e4aa9952ba2026ecf5a0778254701c521fa278
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier1-game-aggregates
- Contract: docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- Existing schema contract: docs/contracts/player_log_evidence_ledger_schema.md
- Existing lifecycle contract: docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md

Goal:
Compare the current evidence ledger implementation and focused tests against the Tier 1 game aggregate contract. Implement only the smallest metadata/test changes needed to expand the ledger registry across the contracted aggregate fields.

Use:
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/parser_models.md
- docs/contracts/parser_state.md
- docs/contracts/parser_sheet_schema.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/app/golden_replay.py
- tests/test_state.py
- tests/test_app_models.py
- tests/test_golden_replay_harness.py

Do:
- Preserve the #128 schema, validators, vocabulary constants, and match_id anchor entry.
- Preserve all #130 Tier 1 lifecycle/result/sync entries.
- Add ledger entries for games_won, games_lost, total_games, match_win_flag, and game_win_rate.
- Move those five fields from Tier 1 future fields to mapped seed fields using existing schema vocabulary.
- Keep full per-game result provenance deferred to a later Tier 3 game-level facts issue.
- Use existing value-source, confidence, finality, invariant-status, and drift-flag vocabulary only.
- Preserve parser-owned truth boundaries.
- Add focused tests for the expanded entry set, derived source policy, dependency signals, expected blank behavior, invariants, validation, privacy, copy safety, and deterministic serialization.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_tier1_game_aggregates_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser behavior.
- Change parser state final reconciliation.
- Change parser event classes.
- Change workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or AI/analytics truth.
- Implement runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, or feature-equity report changes.
- Reconstruct missing GameState data or infer facts that Player.log did not provide.
- Commit raw private Player.log excerpts.
- Target main directly.
- Close issue #11.
- Stage or commit unless explicitly asked.

Validation:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_state.py
- python3 -m pytest -q tests/test_golden_replay_harness.py
- python3 -m ruff check src tests tools
- git diff --check
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/132"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/130"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/131"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier1_game_aggregates_comparison.md"
  verdict: "ready_for_module_implementer"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier1-game-aggregates"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_state.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, or AI/analytics truth."
    - "Do not reconstruct missing GameState data or infer facts that the Player.log did not provide."
    - "Do not implement runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, or feature-equity report changes."
    - "Do not commit raw private Player.log excerpts."
```
