# Parser Timer Normalization Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/115

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/113

Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/114

Previous merge commit: `bbcd61656f2af7981936e415e6d1431f5889f012`

## Contract

- `docs/contracts/parser_timer_normalization.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch: `codex/parser-reliability-intelligence`

Changed files reviewed:

- `docs/contracts/parser_timer_normalization.md`
- `docs/implementation_handoffs/parser_timer_normalization_comparison.md`
- `src/mythic_edge_parser/parsers/gre/timers.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_timers_parser.py`
- `tests/test_gre_game_state_parser.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`

Unrelated local files observed and excluded from this review:

- `docs/.DS_Store`
- `docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md`
- `docs/contracts/repo_wide_llm_advisory_review_scaffold.md`
- `docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md`

## Findings

No blocking findings.

## Contract-Test Verdict

The implementation satisfies the parser timer normalization contract in the
reviewed scope. `normalized_timers` is an additive parser-owned
`GameStateEvent.payload` field, raw `timers` and `raw_game_state` preservation
remain intact, timer malformed-input behavior degrades into reviewable evidence,
and turn-info context remains separate from timer ownership.

Next recommended role: Codex F: Module Submitter.

## Contract Summary

The timer normalization module must preserve raw GRE GameState timer arrays
while adding a stable parser-owned normalized timer evidence view. It may expose
normalized records, collection summaries, and direct-seat helper summaries for
parser-adjacent consumers, but it must not infer clock pressure, player
mistakes, hidden cards, decklists, archetypes, or GameState diff/update/deletion
mechanics. It must not move timer truth into workbook formulas, dashboards,
webhook transport, Apps Script, runtime status files, AI, or analytics surfaces.

## Checks Run

```bash
git fetch --prune
gh issue view 115 --json number,title,state,body,labels,url
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
printf '%s\n' src/mythic_edge_parser/parsers/gre/timers.py src/mythic_edge_parser/parsers/gre/game_state.py tests/test_gre_timers_parser.py tests/test_gre_game_state_parser.py tests/fixtures/schema_snapshots/parser_payload_keys.json docs/contracts/parser_timer_normalization.md docs/implementation_handoffs/parser_timer_normalization_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
python3 -m pytest -q tests
python3 tools/check_secret_patterns.py --base origin/main
python3 tools/check_protected_surfaces.py --base origin/main
```

## Results

- Issue #115: open, tracker #47-linked, parser reliability branch scope
  confirmed.
- Timer normalizer tests: `6 passed in 0.03s`.
- GameState parser tests: `5 passed in 0.03s`.
- Turn-info parser tests: `15 passed in 0.04s`.
- Annotation normalizer tests: `6 passed in 0.03s`.
- Event schema snapshot tests: `6 passed in 0.17s`.
- Parser diagnostics mode tests: `10 passed in 0.06s`.
- Golden replay harness tests: `12 passed in 0.14s`.
- Parser regression tests: `2 passed in 0.09s`.
- Saved event replay tests: `26 passed in 0.04s`.
- Ruff: `All checks passed!`.
- `git diff --check`: passed with no output.
- Explicit #115 changed-path protected-surface gate: `changed_paths: 7`,
  `forbidden: 0`, `warnings: 2`, `result: passed`.
- Golden replay CLI over committed manifests:
  `Golden replay: pass (2 manifests, 2 pass, 0 degraded, 0 review, 0 diff, 0 fail)`.
- Full local test suite: `729 passed in 1.02s`.
- Branch-scope protected-surface gate against `origin/main`: `changed_paths: 47`,
  `forbidden: 0`, `warnings: 7`, `result: passed`.
- `tools/check_secret_patterns.py`: unavailable on this branch.

The two explicit #115 protected-surface warnings are contract-authorized
parser-owned changes:
`src/mythic_edge_parser/parsers/gre/timers.py` and
`src/mythic_edge_parser/parsers/gre/game_state.py`.

The branch-scope protected-surface warnings include prior parser reliability
work already present on `codex/parser-reliability-intelligence`, plus the
current GameState integration surface:
`src/mythic_edge_parser/app/gameplay_actions.py`,
`src/mythic_edge_parser/app/transforms.py`,
`src/mythic_edge_parser/events.py`,
`src/mythic_edge_parser/parsers/__init__.py`,
`src/mythic_edge_parser/parsers/gre/annotations.py`,
`src/mythic_edge_parser/parsers/gre/game_state.py`, and
`src/mythic_edge_parser/parsers/truncation.py`.

## Confirmed Contract Matches

- `src/mythic_edge_parser/parsers/gre/timers.py` exposes the contracted
  constants and helpers:
  `TIMER_RECORD_OBJECT`, `TIMER_COLLECTION_OBJECT`, `SCHEMA_VERSION`,
  `normalize_timer_record()`, `normalize_timer_array()`, and
  `timer_records_by_direct_seat()`.
- Normalized timer collection payloads include the contracted object,
  schema version, counts, source array, timer ID/type unions, direct seat
  unions, unit counts, contextual turn-info, degradation flags, and records.
- Normalized timer records include the contracted object, schema version,
  source metadata, timer identity, type/name/category/evidence strings,
  direct seat evidence, boolean evidence, numeric/time values, unit evidence,
  unsupported-field evidence, source evidence, evidence status, value source,
  confidence, degradation flags, and review status.
- Helper outputs are JSON-serializable, deterministic, and preserve input
  objects without mutation.
- `GameStateEvent.payload["normalized_timers"]` is additive and parser-owned.
- Raw `payload["timers"]` remains present with the existing shallow-copy
  semantics.
- `raw_game_state` behavior remains unchanged.
- `normalized_annotations` behavior remains preserved.
- Missing or `None` timer sections produce zero normalized records without
  degradation.
- Present non-list timer sections produce `malformed_timers_section`.
- Non-dict timer entries produce degraded placeholder records with
  `malformed_timer_record`.
- Timer ID and direct-seat fields follow the contracted scalar normalization,
  including rejecting booleans, floats, negative strings, invalid strings,
  empty strings, nested values, dictionaries, and `None`.
- String fields require actual strings and do not coerce numeric or boolean
  values into parser facts.
- Boolean fields require actual booleans and do not become integer evidence.
- Numeric/time fields reject booleans, non-finite floats, invalid strings, and
  nested shapes.
- Explicit seconds and milliseconds units are assigned by field name only.
- Unknown-unit time-like fields remain unknown and produce
  `unknown_timer_time_unit`; numeric magnitude is not used to infer units.
- Negative timer values are preserved as evidence and flagged with
  `negative_timer_value`.
- Unsupported nested timer fields are not copied wholesale and are flagged with
  `unsupported_timer_field_shape`.
- Data-loss/truncation-like timer markers are preserved as parser evidence
  rather than reconstructed hidden state.
- `turn_info` context is carried only in collection-level
  `contextual_turn_info` and never populates record ownership or
  `direct_seat_ids`.
- `timer_records_by_direct_seat()` groups records only by direct timer-seat
  evidence.
- The schema snapshot update is limited to the additive
  `normalized_timers` GameState payload key.
- Existing diagnostics, golden replay, saved replay, turn-info, annotation,
  parser regression, event schema snapshot, and full-suite tests remain green.
- No workbook schema, webhook payload shape, Apps Script behavior, output
  transport, runtime status file schema, parser state final reconciliation,
  parser event class, match/game identity, deduplication, secrets, environment
  variables, raw logs, generated data, failed posts, workbook exports,
  clock-pressure analytics, gameplay advice, player-mistake labels,
  hidden-card inference, decklist completion, archetype classification,
  OpenAI/model-provider behavior, AI truth, or analytics truth changes were
  found in the #115 scope.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests found.

Focused tests cover collection shape, JSON serialization, input immutability,
missing and malformed sections, placeholder records, timer IDs, strings,
booleans, direct seat fields, time units, negative values, unsupported nested
fields, data-loss flags, turn-info context separation, additive GameState
payload behavior, raw timer preservation, schema snapshot keys, diagnostics
compatibility, golden replay compatibility, parser regressions, and saved event
replay.

Non-blocking note: broader live Arena timer drift, clock-pressure analytics,
player-decision interpretation, and GameState diff/update/deletion mechanics
remain intentionally outside v1.

## Drift Notes

- Repo drift: expected addition of a parser-side GRE timer normalizer, additive
  GameState payload field, focused tests, schema snapshot update, contract,
  handoff, and this contract-test report.
- Parser behavior drift: contract-authorized additive normalized timer evidence
  only.
- Raw GameState payload drift: none found for raw `timers` or `raw_game_state`.
- Parser event class drift: none found.
- Parser state final reconciliation drift: none found.
- Match/game identity drift: none found.
- Deduplication drift: none found.
- Workbook schema drift: none found.
- Webhook payload drift: none found.
- Apps Script drift: none found.
- Output transport drift: none found.
- Runtime status schema drift: none found.
- Failed-post schema drift: none found.
- Local-data drift: no raw private logs, generated runtime artifacts, failed
  posts, runtime status files, or workbook exports were added in the reviewed
  #115 scope.
- Previous parser reliability drift: branch comparisons against `origin/main`
  still include prior issue #107 and #113 surfaces; those are not part of this
  #115 finding set.

## Remaining Non-Blocking Gaps

- Remote CI has not run in this local Codex E pass.
- `tools/check_secret_patterns.py` is absent on this branch, so the optional
  branch-native content scanner was recorded as unavailable.
- Live Arena timer shape drift remains future evidence-ledger/diagnostics work,
  not a blocker for this v1 parser-owned normalization package.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #115: GameState timer normalization module.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/115
- Related evidence/resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Branch/base: codex/parser-reliability-intelligence
- Contract: docs/contracts/parser_timer_normalization.md
- Implementation handoff: docs/implementation_handoffs/parser_timer_normalization_comparison.md
- Contract-test report: docs/contract_test_reports/parser_timer_normalization.md

Goal:
Prepare the parser timer normalization package for PR submission into codex/parser-reliability-intelligence.

Scope to include:
- docs/contracts/parser_timer_normalization.md
- docs/implementation_handoffs/parser_timer_normalization_comparison.md
- docs/contract_test_reports/parser_timer_normalization.md
- src/mythic_edge_parser/parsers/gre/timers.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- tests/test_gre_timers_parser.py
- tests/test_gre_game_state_parser.py
- tests/fixtures/schema_snapshots/parser_payload_keys.json

Do not include unrelated local files:
- docs/.DS_Store
- docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md
- docs/contracts/repo_wide_llm_advisory_review_scaffold.md
- docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md

Codex E verdict:
No blocking findings. The implementation satisfies the parser timer normalization contract in the reviewed scope. normalized_timers is additive and parser-owned; raw timers, raw_game_state, normalized_annotations, turn-info separation, malformed-input degradation, and schema snapshot boundaries are preserved.

Validation reviewed:
- python3 -m pytest -q tests/test_gre_timers_parser.py -> 6 passed
- python3 -m pytest -q tests/test_gre_game_state_parser.py -> 5 passed
- python3 -m pytest -q tests/test_gre_turn_info_parser.py -> 15 passed
- python3 -m pytest -q tests/test_gre_annotations_parser.py -> 6 passed
- python3 -m pytest -q tests/test_event_schema_snapshots.py -> 6 passed
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py -> 10 passed
- python3 -m pytest -q tests/test_golden_replay_harness.py -> 12 passed
- python3 -m pytest -q tests/test_parser_regressions.py -> 2 passed
- python3 -m pytest -q tests/test_saved_event_replay.py -> 26 passed
- python3 -m ruff check src tests -> All checks passed
- git diff --check -> passed
- explicit #115 protected-surface gate -> forbidden 0, warnings 2, result passed
- python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay -> pass
- python3 -m pytest -q tests -> 729 passed
- branch-scope protected-surface gate -> forbidden 0, warnings 7, result passed

Submitter responsibilities:
- Verify the exact staged/committed scope.
- Create or update the PR against codex/parser-reliability-intelligence.
- Do not target main.
- Do not merge, close issue #115, close tracker #47, or close related issue #11.
- Leave merge/deployment/issue closure/tracker updates for Codex G.

Stop conditions:
- Do not include unrelated local files.
- Do not change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Do not build clock-pressure analytics, gameplay advice, player-mistake labels, hidden-card inference, decklist completion, archetype classification, model-provider behavior, or AI/analytics truth.
- Do not solve GameState diff/update/deletion mechanics in this module.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/115"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/113"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/114"
  previous_merge_commit: "bbcd61656f2af7981936e415e6d1431f5889f012"
  completed_thread: "E"
  next_thread: "F"
  verdict: "No blocking findings. Ready for Codex F."
  branch: "codex/parser-reliability-intelligence"
  source_artifact: "docs/contracts/parser_timer_normalization.md"
  target_artifact: "docs/contract_test_reports/parser_timer_normalization.md"
  risk_tier: "High"
  validation:
    - "python3 -m pytest -q tests/test_gre_timers_parser.py -> 6 passed"
    - "python3 -m pytest -q tests/test_gre_game_state_parser.py -> 5 passed"
    - "python3 -m pytest -q tests/test_gre_turn_info_parser.py -> 15 passed"
    - "python3 -m pytest -q tests/test_gre_annotations_parser.py -> 6 passed"
    - "python3 -m pytest -q tests/test_event_schema_snapshots.py -> 6 passed"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py -> 10 passed"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py -> 12 passed"
    - "python3 -m pytest -q tests/test_parser_regressions.py -> 2 passed"
    - "python3 -m pytest -q tests/test_saved_event_replay.py -> 26 passed"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "git diff --check -> passed"
    - "explicit #115 protected-surface gate -> forbidden 0, warnings 2, result passed"
    - "python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay -> pass"
    - "python3 -m pytest -q tests -> 729 passed"
    - "branch-scope protected-surface gate -> forbidden 0, warnings 7, result passed"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not include unrelated local files."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not build clock-pressure analytics, gameplay advice, player-mistake labels, hidden-card inference, decklist completion, archetype classification, model-provider behavior, or AI/analytics truth."
    - "Do not solve GameState diff/update/deletion mechanics in this module."
```
