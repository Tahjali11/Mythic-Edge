# Parser GameState Diff Mechanics Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/117

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

`docs/contracts/parser_game_state_diff_mechanics.md`

## Role Performed

Codex C: Module Implementer.

## Summary Of Implementation Comparison

No blocking contract ambiguity was found. The current repo already preserved
raw update, previous-state, pending-count, and deletion-marker fields, but it
lacked the first-class parser-owned normalized
`game_state_diff_mechanics` object required by the contract.

Codex C implemented the smallest coherent parser-local helper, wired it into
GameState payload construction as an additive field, added focused synthetic
tests, and updated the parser payload-key snapshot only for the authorized
additive key.

## Confirmed Matches

- Existing top-level `update`, `pending_message_count`, `prev_game_state_id`,
  `diff_deleted_instance_ids`, and
  `diff_deleted_persistent_annotation_ids` remain backward compatible.
- Raw `players`, `zones`, `game_objects`, `annotations`,
  `persistent_annotations`, `timers`, `actions`, and `raw_game_state` remain
  preserved.
- `normalized_annotations` and `normalized_timers` behavior is unchanged.
- Regular and queued GameState messages still reach the same
  `build_game_state_payload()` path.
- No GRE dispatch, parser event class, parser state reconciliation, match/game
  identity, deduplication, workbook, webhook, Apps Script, output transport, or
  runtime status behavior was changed.

## Contract Mismatches Found And Fixed

- Missing parser-owned GameState diff mechanics helper.
  - Fixed by adding `src/mythic_edge_parser/parsers/gre/game_state_diff.py`.
- Missing additive `GameStateEvent.payload["game_state_diff_mechanics"]`.
  - Fixed in `src/mythic_edge_parser/parsers/gre/game_state.py`.
- Missing focused tests for update kind, queue status, linkage, deletion
  markers, malformed metadata, and no-reconstruction boundaries.
  - Fixed with `tests/test_gre_game_state_diff_parser.py`.

## Missing Safeguards Found And Added

- Diff updates are explicitly `partial_update` and never complete snapshots.
- Unknown or unsupported update markers become reviewable metadata.
- Missing, malformed, self-referential, and future previous-state links are
  degraded/reviewable.
- Deletion markers are copied from existing normalized top-level lists and
  counted as evidence only.
- Malformed deletion source shapes are flagged without dropping already
  normalized valid IDs.
- Section counts summarize observed list counts only and do not imply
  completeness.
- Queued status is source classification only and does not infer stale,
  complete, or partial state.

## Missing Or Weak Tests Found And Fixed

- Added `tests/test_gre_game_state_diff_parser.py`.
- Updated `tests/test_gre_game_state_parser.py` to assert the additive
  `game_state_diff_mechanics` payload while preserving existing top-level
  fields.
- Updated `tests/fixtures/schema_snapshots/parser_payload_keys.json` only for
  the additive `game_state_diff_mechanics` key.

## Files Changed

- `src/mythic_edge_parser/parsers/gre/game_state_diff.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_game_state_diff_parser.py`
- `tests/test_gre_game_state_parser.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `docs/implementation_handoffs/parser_game_state_diff_mechanics_comparison.md`

## Interface Changes

- Added parser-side constants and helper:
  - `GAME_STATE_DIFF_MECHANICS_OBJECT`
  - `SCHEMA_VERSION`
  - `build_game_state_diff_mechanics()`
- Added additive parser payload field:
  - `GameStateEvent.payload["game_state_diff_mechanics"]`
- No workbook columns, webhook fields, Apps Script mappings, runtime status
  schema, failed-post schema, parser event class schema, match identity, game
  identity, or deduplication interfaces were changed.

## Validation Evidence

```bash
python3 -m pytest -q tests/test_gre_game_state_diff_parser.py
# 7 passed

python3 -m pytest -q tests/test_gre_game_state_diff_parser.py tests/test_gre_game_state_parser.py
# 12 passed

python3 -m pytest -q tests/test_gre_annotations_parser.py tests/test_gre_timers_parser.py
# 12 passed

python3 -m pytest -q tests/test_event_schema_snapshots.py
# 6 passed

python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_golden_replay_harness.py
# 22 passed

python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_parsers.py tests/test_parser_regressions.py
# 46 passed

python3 -m pytest -q tests/test_saved_event_replay.py
# 26 passed

python3 -m pytest -q tests
# 736 passed

python3 -m ruff check src tests tools
# All checks passed.

git diff --check
# passed

python3 tools/check_protected_surfaces.py --base origin/main
# result: passed
# warnings: 8 branch-scope protected parser/match-surface warnings on the
# reliability branch, including the contract-authorized GameState integration
# in this module.
```

## Still-Unverified Layers

- No live workbook, webhook, Apps Script, output transport, local status file,
  failed-post, workbook export, or production runtime behavior was exercised.
- CI was not run in GitHub from this thread.
- Diagnostics and golden replay can consume this object in future modules, but
  no broad consumer rewrites were made here.
- Full GameState reconstruction, feature-equity corpus ratchet/reporting, and
  field-level parity audit remain intentionally outside this module.

## Unrelated Local Files Not Absorbed

The worktree also contains unrelated untracked local artifacts that were not
edited or included in this module:

- `docs/.DS_Store`
- `docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md`
- `docs/contracts/repo_wide_llm_advisory_review_scaffold.md`
- `docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md`

The source contract `docs/contracts/parser_game_state_diff_mechanics.md` is
also currently untracked and should be included by the submitter with this
module if still untracked at submission time.

## Reviewer Focus

Please verify that:

- `game_state_diff_mechanics` is additive and parser-owned only.
- Diff GameState payloads are never classified as complete snapshots.
- Deletion IDs are evidence only and do not cause reconstruction or raw-section
  mutation.
- Unknown and malformed update/linkage/deletion fields become reviewable or
  degraded metadata.
- Existing top-level compatibility fields keep their current behavior.
- Snapshot updates are limited to the authorized additive payload key.
- No downstream truth, analytics, hidden-card inference, state reconstruction,
  parser event class, parser state, identity, workbook, webhook, Apps Script,
  or output transport behavior was introduced.

## Next Workflow Action

Next role: Codex E: Module Reviewer in contract-test mode.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #117: GameState diff/update/deletion mechanics module.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- Related resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/117
- Branch/base: codex/parser-reliability-intelligence
- Contract: docs/contracts/parser_game_state_diff_mechanics.md
- Implementation handoff: docs/implementation_handoffs/parser_game_state_diff_mechanics_comparison.md
- Previous completed issue: #115 GameState timer normalization
- Previous PR: #116
- Previous merge commit: 1afd981bc36ea3ebb68564a04f7ca985367ca9bf

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/contract_test.md
- docs/contracts/parser_game_state_diff_mechanics.md
- docs/implementation_handoffs/parser_game_state_diff_mechanics_comparison.md
- src/mythic_edge_parser/parsers/gre/game_state_diff.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- src/mythic_edge_parser/parsers/gre/__init__.py
- src/mythic_edge_parser/parsers/gre/annotations.py
- src/mythic_edge_parser/parsers/gre/timers.py
- tests/test_gre_game_state_diff_parser.py
- tests/test_gre_game_state_parser.py
- tests/test_gre_annotations_parser.py
- tests/test_gre_timers_parser.py
- tests/test_event_schema_snapshots.py
- tests/test_parser_diagnostics_mode.py
- tests/test_golden_replay_harness.py
- tests/test_gameplay_actions.py
- tests/test_opponent_card_observations.py
- tests/test_parsers.py
- tests/test_parser_regressions.py
- tests/test_saved_event_replay.py

Goal:
Verify the Codex C implementation against the GameState diff mechanics contract.

Confirm:
- The implementation is additive and parser-local.
- The normalized object shape matches the contract.
- Regular and queued GameState payloads both get game_state_diff_mechanics.
- full updates map to complete_snapshot and is_complete_snapshot true.
- diff updates map to partial_update and is_complete_snapshot false.
- Missing or unknown update markers are reviewable and do not crash.
- Missing, malformed, self-referential, and future previous-state links are degraded/reviewable.
- Deletion ID lists are copied from existing normalized top-level lists and counted correctly.
- Deletion markers do not reconstruct missing objects, remove raw objects, synthesize annotations, or treat diffs as full snapshots.
- Section counts are counts only and do not imply completeness.
- Existing top-level update, pending_message_count, prev_game_state_id, diff_deleted_instance_ids, diff_deleted_persistent_annotation_ids, normalized_annotations, normalized_timers, and raw_game_state behavior is preserved.
- Snapshot updates are limited to the authorized additive payload key.
- No parser event class, parser state final reconciliation, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status, failed-post, workbook export, secret, credential, environment variable, OpenAI/model-provider, or AI/analytics truth surface changed.

Validation:
Run:
python3 -m pytest -q tests/test_gre_game_state_diff_parser.py
python3 -m pytest -q tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_gre_annotations_parser.py tests/test_gre_timers_parser.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
python3 -m pytest -q tests/test_parsers.py tests/test_parser_regressions.py
python3 -m pytest -q tests/test_saved_event_replay.py
python3 -m ruff check src tests tools
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
- Reconstruct missing GameState data or treat diff GameState messages as full state snapshots.
- Change parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status files, failed posts, workbook exports, secrets, credentials, environment variables, OpenAI/model-provider behavior, or AI/analytics truth.
- Infer hidden cards, complete decklists, archetypes, gameplay advice, player mistakes, or clock-pressure analytics.
- Copy Manasight source code or commit raw private Player.log excerpts, generated data, local logs, failed posts, runtime status files, or workbook exports.
- Solve feature-equity corpus ratchet/reporting or field-level parity audit in this module.
- Stage, commit, merge, or open a PR unless separately instructed.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/117"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_game_state_diff_mechanics.md"
  target_artifact: "docs/implementation_handoffs/parser_game_state_diff_mechanics_comparison.md"
  verdict: "ready_for_contract_test_review"
  branch: "codex/parser-reliability-intelligence"
  risk_tier: "High"
  validation:
    - "python3 -m pytest -q tests/test_gre_game_state_diff_parser.py"
    - "python3 -m pytest -q tests/test_gre_game_state_diff_parser.py tests/test_gre_game_state_parser.py"
    - "python3 -m pytest -q tests/test_gre_annotations_parser.py tests/test_gre_timers_parser.py"
    - "python3 -m pytest -q tests/test_event_schema_snapshots.py"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_parsers.py tests/test_parser_regressions.py"
    - "python3 -m pytest -q tests/test_saved_event_replay.py"
    - "python3 -m pytest -q tests"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not reconstruct missing GameState data or treat diff GameState messages as full state snapshots."
    - "Do not change parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status files, failed posts, workbook exports, secrets, credentials, environment variables, OpenAI/model-provider behavior, or AI/analytics truth."
    - "Do not infer hidden cards, complete decklists, archetypes, gameplay advice, player mistakes, or clock-pressure analytics."
    - "Do not copy Manasight source code or commit raw private Player.log excerpts, generated data, local logs, failed posts, runtime status files, or workbook exports."
    - "Do not solve feature-equity corpus ratchet/reporting or field-level parity audit in this module."
```
