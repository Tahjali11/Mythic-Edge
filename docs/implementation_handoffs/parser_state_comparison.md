# Parser State Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/6

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

The GitHub issue was reviewed for scope. It classifies this as a high-risk
parser/state audit, names `codex/parser-module-audit-suite` as the integration
branch, and asks this Module Implementer thread to produce this comparison
artifact before Module Reviewer contract testing.

## Contract

`docs/contracts/parser_state.md`

## Role Performed

Module Implementer / comparison thread.

This pass compared the current `src/mythic_edge_parser/app/state.py`
implementation and focused state tests against the parser state contract. No
behavior, tests, workbook schema, webhook payload shape, Apps Script behavior,
parser event classes, extractor behavior, match identity, game identity,
deduplication, final reconciliation, secrets, environment variables, raw logs,
generated data, runtime status files, failed posts, or workbook exports were
changed.

## Current Behavior Summary

The implementation is broadly aligned with the contract. `state.py` owns a
single mutable `ParserRuntimeState`, preserves current compatibility aliases,
ingests parsed event objects through `_update_match_summary(event)`, builds live
and final match/game rows from `MatchSummary`, and tracks posted-row snapshots
for changed-field update decisions.

The comparison did not find a clear contract mismatch that justified changing
parser behavior in this thread. The main gaps are missing direct tests and
implicit safeguards around compatibility aliases, no-op branches, and edge-case
GameResult finalization.

## Confirmed Matches

- State ownership: `ParserRuntimeState` contains the runtime containers and
  scalars named by the contract, and `RUNTIME_STATE` is the module singleton.
- Compatibility aliases: mutable module-level aliases point at the singleton's
  live containers, including context, match summaries, posted snapshots,
  mulligan counts, hand snapshots, and card lookup state.
- Reset behavior: `reset_runtime_state()` clears containers in place, restores
  default context, resets scalar lookup/rank/log state, and does not replace
  `RUNTIME_STATE`.
- Public builders and getters exist with the contracted names:
  `build_match_summary_row()`, `build_game_summary_rows()`,
  `build_match_log_row()`, `build_live_match_log_row()`,
  `build_match_log_update()`, `build_game_log_updates()`,
  `mark_match_log_posted()`, `mark_game_log_posted()`,
  `get_match_summary()`, `iter_match_summaries()`, `get_runtime_state()`, and
  `get_context_snapshot()`.
- Rank behavior matches the contract: rank text is normalized, stored in the
  latest rank snapshot, carried into the next created summary, and not applied
  to a completed ready summary.
- MatchState handling matches the contract: missing match IDs return early,
  context is updated when identity exists, summaries are created on demand,
  event IDs can replace `"Play"`, local team is inferred from players, game
  results are assigned sequentially, and match-scope results set match winner
  fields.
- GameState handling matches the contract: identity uses payload plus context
  fallback, summaries are touched, local team can be corrected, game info is
  ingested, turn counts advance through model safeguards, starting player is
  inferred from turn-one active player data, and opening-hand candidates are
  recorded only for 4-to-7-card local private hand zones.
- ClientAction handling matches the contract: actions require current match
  context, can correct local team, touch the current game, update mulligan
  counts, record discarded mulligan hands, set submit-deck/sideboarding flags,
  and handle generic starting-player responses.
- GameResult handling matches the contract's observed behavior: identity uses
  extractor/context fallback, game info is ingested, game winners and match
  winners remain separate, and match completion uses the top-level winning team
  when a completion marker or match-scope result is present.
- Hand and mulligan capture matches the contract: instance-to-grpId mappings
  accumulate per match/game, unresolved cards become placeholders, consecutive
  duplicate snapshots are not appended, discarded hands are captured before a
  non-keep decision increments mulligans, and bottomed cards are inferred from a
  longer prior snapshot only once per normalized game key.
- Row readiness matches the contract: final match summary and match log rows
  are withheld until `MatchSummary.is_ready()`, live match log rows can be built
  earlier, match log updates switch from live to final at readiness, and game
  log update finality is per game based on non-empty `Game Result`.
- Changed-field detection matches the contract: only schema sync fields are
  compared, blank first-post fields are ignored, floats are rounded before
  comparison, and repeated builds after mark-posted produce no update until a
  sync field changes.
- Mark-posted APIs store shallow row copies with `dict(row)`, not caller-owned
  dictionary references.
- Side effects remain narrow: this module mutates in-memory state and may call
  card catalog lookup/bootstrap helpers, but it does not write match logs,
  submit webhooks, mutate workbook state, or read secrets/environment variables.

## Contract Mismatches

Resolved by Module Fixer follow-up after the revised contract:

- `build_game_result_payload()` no longer promotes a nested
  `MatchScope_Match` result into top-level game-winner fields when no
  game-scope result exists.
- GameResult state reconciliation now uses the latest known nested
  `MatchScope_Game` winner for the game winner.
- GameResult state reconciliation now prefers the latest known nested
  `MatchScope_Match` winner, result type, and reason for match finalization.
- If no nested match-scope winner exists, match winner fallback to top-level
  `winning_team_id` now occurs only when
  `match_state == "MatchState_MatchComplete"`.
- Winner values `None`, `""`, `0`, and `"0"` are treated as unknown and do not
  set or overwrite game or match winners.

## Missing Safeguards

- Resolved by Module Fixer follow-up: nested GameResult match-scope winners are
  now parser-owned final reconciliation inputs rather than only evidence that a
  match-scope result exists.
- Scalar compatibility is limited. Rank helpers synchronize through
  `get_last_posted_rank()` / `set_last_posted_rank()` and reset, while other
  scalar aliases such as current log date/path and lookup readiness flags are
  not general two-way aliases.
- Many tests manually clear selected state containers instead of calling
  `reset_runtime_state()`. That can hide stale scalar state, alias drift, or
  unrelated container residue.
- Card catalog bootstrap failures are swallowed during gameplay lookup setup,
  which preserves current behavior but leaves unresolved-card causes
  unobservable.
- The module intentionally has no thread-safety guard and models only one
  active current context. Out-of-order replay across multiple active matches
  remains an unprotected design edge.
- Non-dict event payloads are explicitly outside the contract guarantee. The
  implementation calls `.get()` inside supported event branches.

## Missing Or Weak Tests

- Resolved by Module Fixer follow-up: focused tests now prove unknown event
  kinds are complete no-ops.
- Resolved by Module Fixer follow-up: focused tests now prove MatchState,
  GameState, ClientAction, and GameResult events with missing identity avoid
  anonymous summary creation.
- Resolved by Module Fixer follow-up: reset coverage now asserts alias object
  identity before and after reset and confirms `RUNTIME_STATE` itself is not
  replaced.
- Resolved by Module Fixer follow-up: reset coverage now directly asserts
  current log date/path, latest rank fields, and runtime lookup-readiness scalar
  fields on `RUNTIME_STATE`.
- Resolved by Module Fixer follow-up: direct tests mutate caller rows after
  `mark_match_log_posted()` and `mark_game_log_posted()` to prove posted
  snapshots are copies.
- Resolved by Module Fixer follow-up: changed-field tests now directly prove
  non-sync-field changes are ignored and float normalization with
  `round(value, 10)` suppresses insignificant churn.
- Resolved by Module Fixer follow-up: direct tests now cover invalid
  `mark_game_log_posted()` keys and invalid game numbers being skipped by
  game-log update paths.
- Resolved by Module Fixer follow-up: direct tests now cover
  `build_live_match_log_row()` and `build_match_summary_row()` readiness and
  withholding behavior.
- Resolved by Module Fixer follow-up: observation API tests now cover
  `iter_match_summaries()` returning a list snapshot and
  `get_context_snapshot()` returning a shallow copy.
- Resolved by Module Fixer follow-up: context fallback tests now prove
  GameState/GameResult payloads can use established current context when
  identity fields are omitted.
- Resolved by Module Fixer follow-up after contract revision: nested
  GameResult match-scope result variants now have focused parser and state
  coverage.
- Resolved by Module Fixer follow-up: hand snapshot history now has a narrow
  test for consecutive duplicate suppression and once-only bottomed-card
  capture.
- `tests/test_saved_event_replay.py` validates replay reconstruction/dedupe but
  does not assert reconstructed events update parser state; that may be fine if
  this file is considered replay utility coverage rather than parser-state
  coverage.

## Files Changed

- `docs/implementation_handoffs/parser_state_comparison.md`
- `docs/contract_test_reports/parser_state.md`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `tests/test_gre_game_result_parser.py`
- `tests/test_state.py`

## Code Changed

Module Fixer follow-up changed parser-owned GameResult reconciliation code:

- `build_game_result_payload()` now selects the latest known
  `MatchScope_Game` result for top-level game-winner fields and leaves those
  fields unknown when no valid game-scope result exists.
- `state.py` now separates game winner selection from match winner selection,
  prefers nested match-scope winners for match finalization, and falls back to
  top-level match winners only for `MatchState_MatchComplete`.
- Extractor helpers now centralize known-winner checks and latest scoped
  GameResult extraction for state reconciliation.

## Tests Changed

Module Fixer follow-up added direct focused tests in `tests/test_state.py` for:

- unknown event no-op behavior
- missing-identity no-op behavior
- reset alias identity and scalar reset behavior
- posted-row copy semantics
- schema-only changed-field detection and float normalization
- invalid game-log posted/update keys
- live/final row builder readiness
- observation API snapshot/copy behavior
- GameState/GameResult context fallback
- hand snapshot duplicate suppression and once-only bottomed-card capture
- GameResult final reconciliation precedence and unknown-winner behavior

Module Fixer follow-up also added focused tests in
`tests/test_gre_game_result_parser.py` for GRE GameResult payload top-level
game winner selection.

## Interface Changes

None.

No function signatures, payload fields, workbook columns, environment
variables, Apps Script entrypoints, match identity rules, game identity rules,
or deduplication behavior changed. Final reconciliation changed only within the
contracted GameResult winner precedence rule.

## Validation Evidence

Static inspection:

- Read `docs/agent_constitution.md`.
- Read `docs/agent_threads/implementation.md`.
- Read `docs/contracts/parser_state.md`.
- Reviewed GitHub issue #6.
- Compared `src/mythic_edge_parser/app/state.py`.
- Compared focused tests:
  - `tests/test_state.py`
  - `tests/test_match_summary_from_match_state.py`
  - `tests/test_parser_regressions.py`
  - `tests/test_saved_event_replay.py`

Focused GameResult reconciliation validation:

```bash
python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_state.py tests/test_match_summary_from_match_state.py
```

Result:

```text
32 passed in 0.10s
```

Focused parser-state validation:

```bash
python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_parser_regressions.py tests/test_saved_event_replay.py
```

Result:

```text
30 passed in 0.12s
```

Related model/schema validation:

```bash
python3 -m pytest -q tests/test_app_models.py tests/test_sheet_schema.py
```

Result:

```text
12 passed in 0.04s
```

Lint:

```bash
python3 -m ruff check src tests
```

Result:

```text
All checks passed!
```

Full repo validation:

```bash
python3 -m pytest -q
```

Result:

```text
334 passed in 0.86s
```

The previously observed local runner path-sanitization failure did not
reproduce in this final full-suite run.

## Still Unverified

- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Webhook dispatch was not exercised.

## Reviewer Focus

Ask the Module Reviewer to verify the revised GameResult final reconciliation
implementation, especially:

- Latest nested game-scope result selection for game winners.
- Nested match-scope winner/result/reason precedence for match finalization.
- Top-level match winner fallback only on `MatchState_MatchComplete`.
- Unknown winner values `None`, `""`, `0`, and `"0"` not setting or
  overwriting winners.
- That no prohibited downstream surfaces changed.

## Next Workflow Action

Next role: Module Reviewer in contract-test mode.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution. Act as the Module Reviewer thread in contract-test mode for https://github.com/Tahjali11/Mythic-Edge/issues/6, docs/contracts/parser_state.md, docs/implementation_handoffs/parser_state_comparison.md, and docs/contract_test_reports/parser_state.md.

Verify the Module Fixer implementation patch against the revised parser state contract. Confirm GameResult final reconciliation uses the latest nested MatchScope_Game result for game winners, prefers nested MatchScope_Match winner/result/reason for match finalization, falls back to top-level winning_team_id only when no nested match-scope winner exists and match_state is MatchState_MatchComplete, and treats None, "", 0, and "0" as unknown winners. Produce or update docs/contract_test_reports/parser_state.md with confirmed matches, contract mismatches, missing tests, drift classification, validation evidence, and a handoff to Module Fixer, Module Contract Writer, Thinker, Module Submitter, or none.

Confirm no workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed. Do not target main; future module PR work belongs on codex/parser-module-audit-suite.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/6"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/parser_state.md"
  target_artifact: "docs/contract_test_reports/parser_state.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_state.py tests/test_match_summary_from_match_state.py -> 32 passed in 0.10s"
    - "python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_parser_regressions.py tests/test_saved_event_replay.py -> 30 passed in 0.12s"
    - "python3 -m pytest -q tests/test_app_models.py tests/test_sheet_schema.py -> 12 passed in 0.04s"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "python3 -m pytest -q -> 334 passed in 0.86s"
  stop_conditions:
    - "Stop and route back to Module Contract Writer if the contract is ambiguous, inaccurate, or would require changing downstream truth ownership."
    - "Stop and route back to Thinker if review discovers scope outside issue #6."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not target main until the parser module audit suite is complete."
```
