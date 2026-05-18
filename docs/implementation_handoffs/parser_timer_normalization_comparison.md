# Parser Timer Normalization Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/115

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

`docs/contracts/parser_timer_normalization.md`

## Role Performed

Codex C: Module Implementer.

## Summary Of Implementation Comparison

No blocking contract ambiguity was found. The current repo already preserved raw
GameState `timers`, but it lacked the first-class parser-owned timer
normalization layer and additive `normalized_timers` GameState payload field
required by the contract.

Codex C implemented a pure GRE timer normalizer, wired it into GameState
payload construction, added focused synthetic tests, and updated the
parser payload-key snapshot only for the contract-authorized additive key.

## Confirmed Matches

- Raw `timers` remain shallow-copied in the GameState payload.
- `turn_info.py` remains unchanged and continues owning turn context.
- `normalized_annotations` behavior is preserved.
- `raw_game_state` behavior is unchanged.
- No new parser event class was added.
- GRE dispatch and game-result emission were not changed.
- Diagnostics, golden replay, saved replay, turn-info, annotation, and parser
  regression tests remain stable.
- Workbook schema, webhook payload shape, Apps Script behavior, output
  transport, parser state final reconciliation, match/game identity, and
  deduplication were not changed.

## Contract Mismatches Found And Fixed

- Missing parser-owned GRE timer normalization module.
  - Fixed by adding `src/mythic_edge_parser/parsers/gre/timers.py`.
- Missing additive `GameStateEvent.payload["normalized_timers"]`.
  - Fixed in `src/mythic_edge_parser/parsers/gre/game_state.py`.
- Missing timer-specific malformed-input tests.
  - Fixed with `tests/test_gre_timers_parser.py`.

## Missing Safeguards Found And Added

- Present non-list `timers` now produces collection degradation flag
  `malformed_timers_section`.
- Non-dict timer entries now produce degraded placeholder records with
  `malformed_timer_record`.
- Timer IDs, direct seat fields, booleans, strings, and numeric/time fields
  use distinct normalization policies instead of sharing unsafe coercion.
- Booleans are rejected as identifier or numeric timer values.
- Direct timer ownership comes only from timer record fields; turn-info context
  is carried separately and never populates `direct_seat_ids`.
- Explicit seconds and milliseconds fields are classified by field name only.
- Unknown-unit time fields remain unknown and receive
  `unknown_timer_time_unit`.
- Negative time values are preserved with `negative_timer_value`.
- Nested timer-related structures are not copied wholesale and receive
  `unsupported_timer_field_shape`.

## Missing Or Weak Tests Found And Fixed

- Added focused tests in `tests/test_gre_timers_parser.py` for collection shape,
  JSON serialization, non-mutation, malformed sections, placeholder records,
  timer IDs, strings, booleans, direct seat fields, time units, negative values,
  unsupported nested fields, data-loss flags, and turn-info context separation.
- Updated `tests/test_gre_game_state_parser.py` to assert additive
  `normalized_timers` while preserving raw `timers`.
- Updated `tests/fixtures/schema_snapshots/parser_payload_keys.json` only for
  the additive `normalized_timers` payload key.

## Files Changed

- `src/mythic_edge_parser/parsers/gre/timers.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_timers_parser.py`
- `tests/test_gre_game_state_parser.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `docs/implementation_handoffs/parser_timer_normalization_comparison.md`

## Interface Changes

- Added parser-side constants and helper functions:
  - `TIMER_RECORD_OBJECT`
  - `TIMER_COLLECTION_OBJECT`
  - `SCHEMA_VERSION`
  - `normalize_timer_record()`
  - `normalize_timer_array()`
  - `timer_records_by_direct_seat()`
- Added additive parser payload field:
  - `GameStateEvent.payload["normalized_timers"]`
- No workbook columns, webhook fields, Apps Script mappings, runtime status
  schema, failed-post schema, parser event class schema, match identity, game
  identity, or deduplication interfaces were changed.

## Validation Evidence

```bash
python3 -m pytest -q tests/test_gre_timers_parser.py
# 6 passed

python3 -m pytest -q tests/test_gre_game_state_parser.py
# 5 passed

python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_turn_info_parser.py tests/test_gre_annotations_parser.py
# 26 passed

python3 -m pytest -q tests/test_event_schema_snapshots.py
# 6 passed

python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_golden_replay_harness.py tests/test_parser_regressions.py
# 24 passed

python3 -m pytest -q tests/test_saved_event_replay.py
# 26 passed

python3 -m pytest -q tests
# 729 passed

python3 -m ruff check src tests
# All checks passed.

git diff --check
# passed

python3 tools/check_protected_surfaces.py --base origin/main
# result: passed
# warnings: 7 branch-scope warnings for protected parser/match surfaces already
# present on the reliability branch and the contract-authorized GameState
# payload change in this module.
```

## Still-Unverified Layers

- No live workbook, webhook, Apps Script, output transport, local status file,
  or production runtime behavior was exercised.
- CI was not run in GitHub from this thread.
- Timer normalization covers v1 synthetic shapes; broader Arena timer drift
  remains a future diagnostics/evidence-ledger concern.
- Clock-pressure analytics, gameplay advice, player-mistake labels, and
  GameState diff/update/deletion mechanics remain intentionally outside this
  module.

## Unrelated Local Files Not Absorbed

The worktree also contains unrelated untracked local artifacts that were not
edited or included in this module:

- `docs/.DS_Store`
- `docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md`
- `docs/contracts/repo_wide_llm_advisory_review_scaffold.md`
- `docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md`

## Reviewer Focus

Please verify that:

- `normalized_timers` is additive and parser-owned only.
- Raw `timers`, `normalized_annotations`, `turn_info`, and `raw_game_state`
  preservation remain intact.
- Malformed timer evidence becomes degraded/review-required evidence and not
  clean parser facts.
- Turn-info context is separate and does not assign timer ownership.
- Numeric/time-unit normalization does not infer units from magnitude.
- The schema snapshot update is limited to the authorized additive GameState
  payload key.
- No analytics, coaching, clock-pressure, player-mistake, AI/model-provider, or
  downstream truth behavior was introduced.

## Next Workflow Action

Next role: Codex E: Module Reviewer in contract-test mode.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #115: GameState timer normalization module.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/115
- Related evidence/resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Branch/base: codex/parser-reliability-intelligence
- Contract: docs/contracts/parser_timer_normalization.md
- Implementation handoff: docs/implementation_handoffs/parser_timer_normalization_comparison.md

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/contract_test.md
- docs/contracts/parser_timer_normalization.md
- docs/implementation_handoffs/parser_timer_normalization_comparison.md
- src/mythic_edge_parser/parsers/gre/timers.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- tests/test_gre_timers_parser.py
- tests/test_gre_game_state_parser.py
- src/mythic_edge_parser/parsers/gre/turn_info.py
- tests/test_gre_turn_info_parser.py
- src/mythic_edge_parser/parsers/gre/annotations.py
- tests/test_gre_annotations_parser.py
- tests/test_event_schema_snapshots.py
- tests/test_parser_diagnostics_mode.py
- tests/test_golden_replay_harness.py
- tests/test_parser_regressions.py
- tests/test_saved_event_replay.py

Goal:
Verify the Codex C implementation against the parser timer normalization contract.

Confirm:
- Raw timers, normalized_annotations, turn_info, and raw_game_state behavior remain preserved.
- normalized_timers is additive, JSON-serializable, deterministic, and parser-owned.
- normalize_timer_record() and normalize_timer_array() match the contracted shape and malformed-input behavior.
- Timer IDs, string fields, boolean fields, numeric fields, direct seat fields, time values, unsupported fields, source evidence, evidence status, value source, confidence, degradation flags, and review_required fields follow the contract.
- timer_records_by_direct_seat() exposes only direct timer seat evidence.
- Turn-info context is carried separately and never populates record ownership or direct_seat_ids.
- Explicit seconds and milliseconds are classified by field-name unit only, unknown-unit timer values remain unknown, and numeric magnitude is not used to infer units.
- Diagnostics, golden replay, saved replay, turn-info, annotation, parser regression, and schema snapshot behavior remain inside the contracted parser-owned evidence boundary.
- No workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.
- No clock-pressure analytics, gameplay advice, player-mistake labels, hidden-card inference, decklist completion, archetype classification, OpenAI/model-provider behavior, or AI/analytics truth was introduced.

Validation:
Run:
python3 -m pytest -q tests/test_gre_timers_parser.py
python3 -m pytest -q tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_gre_turn_info_parser.py
python3 -m pytest -q tests/test_gre_annotations_parser.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_parser_regressions.py
python3 -m pytest -q tests/test_saved_event_replay.py
python3 -m ruff check src tests
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main

If feasible, also run:
python3 -m pytest -q tests

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not:
- Target main directly.
- Close tracker #47.
- Close related issue #11.
- Change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Build clock-pressure analytics, gameplay advice, player-mistake labels, hidden-card inference, decklist completion, archetype classification, model-provider behavior, or AI/analytics truth.
- Solve GameState diff/update/deletion mechanics in this module.
- Stage, commit, merge, or open a PR unless separately instructed.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/115"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/113"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/114"
  previous_merge_commit: "bbcd61656f2af7981936e415e6d1431f5889f012"
  completed_thread: "C"
  next_thread: "E"
  verdict: "ready_for_contract_test_review"
  branch: "codex/parser-reliability-intelligence"
  source_artifact: "docs/contracts/parser_timer_normalization.md"
  target_artifact: "docs/implementation_handoffs/parser_timer_normalization_comparison.md"
  risk_tier: "High"
  validation:
    - "python3 -m pytest -q tests/test_gre_timers_parser.py"
    - "python3 -m pytest -q tests/test_gre_game_state_parser.py"
    - "python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_turn_info_parser.py tests/test_gre_annotations_parser.py"
    - "python3 -m pytest -q tests/test_event_schema_snapshots.py"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_golden_replay_harness.py tests/test_parser_regressions.py"
    - "python3 -m pytest -q tests/test_saved_event_replay.py"
    - "python3 -m pytest -q tests"
    - "python3 -m ruff check src tests"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not build clock-pressure analytics, gameplay advice, player-mistake labels, hidden-card inference, decklist completion, archetype classification, model-provider behavior, or AI/analytics truth."
    - "Do not solve GameState diff/update/deletion mechanics in this module."
```
