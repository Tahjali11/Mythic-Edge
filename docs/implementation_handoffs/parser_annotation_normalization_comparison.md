# Parser Annotation Normalization Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/113

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

`docs/contracts/parser_annotation_normalization.md`

## Role Performed

Codex C: Module Implementer.

## Summary Of Implementation Comparison

No blocking contract ambiguity was found. The current repo already preserved raw
GameState `annotations`, `persistent_annotations`, and
`diff_deleted_persistent_annotation_ids`, but it lacked the first-class
parser-owned annotation normalization layer and additive
`normalized_annotations` GameState payload field required by the contract.

Codex C implemented the smallest coherent normalizer, wired it into GameState
payload construction, moved gameplay-action annotation type/category/replacement
parsing onto the shared helper path, added focused synthetic tests, and updated
the parser payload-key snapshot for the contract-authorized additive field.

## Confirmed Matches

- Raw `annotations` remain shallow-copied in the GameState payload.
- Raw `persistent_annotations` remain shallow-copied in the GameState payload.
- `diff_deleted_persistent_annotation_ids` continues using
  `api_common.normalize_int_list()` behavior.
- `raw_game_state` behavior is unchanged.
- No new parser event class was added.
- GRE dispatch and game-result emission were not changed.
- Gameplay-action classification tests remain stable.
- Opponent-card observation tests remain stable and do not infer hidden cards,
  decklists, or archetypes.
- Diagnostics and golden replay tests remain stable.
- Workbook schema, webhook payload shape, Apps Script behavior, output
  transport, parser state final reconciliation, match/game identity, and
  deduplication were not changed.

## Contract Mismatches Found And Fixed

- Missing parser-owned GRE annotation normalization module.
  - Fixed by adding `src/mythic_edge_parser/parsers/gre/annotations.py`.
- Missing additive `GameStateEvent.payload["normalized_annotations"]`.
  - Fixed in `src/mythic_edge_parser/parsers/gre/game_state.py`.
- Scattered gameplay-action annotation parsing for type/category/replacement
  facts.
  - Narrowly replaced with calls into the shared normalizer while keeping
    persistent annotations out of gameplay-action classification to preserve
    existing behavior.

## Missing Safeguards Found And Added

- Malformed annotation sections now produce collection degradation flags instead
  of clean empty semantic evidence.
- Non-dict annotation entries now produce degraded placeholder records.
- Missing or malformed `type` values are flagged and do not become trusted
  markers.
- `affectedIds` and detail integer normalization now follow
  `api_common.normalize_int_list()` boundaries, including skipping booleans,
  floats, negative strings, invalid strings, and nested values.
- Detail string values must be strings before becoming semantic categories.
- Object replacement summaries require paired `orig_id` and `new_id` evidence.
- Zone-transfer semantic hints remain evidence hints only and do not reconstruct
  missing actions or game facts.

## Missing Or Weak Tests Found And Fixed

- Added focused normalizer tests in `tests/test_gre_annotations_parser.py`.
- Updated `tests/test_gre_game_state_parser.py` to assert the additive
  `normalized_annotations` payload while preserving raw annotation arrays.
- Updated `tests/fixtures/schema_snapshots/parser_payload_keys.json` to include
  the contract-authorized additive GameState payload key.

## Files Changed

- `src/mythic_edge_parser/parsers/gre/annotations.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `tests/test_gre_annotations_parser.py`
- `tests/test_gre_game_state_parser.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `docs/implementation_handoffs/parser_annotation_normalization_comparison.md`

## Interface Changes

- Added parser-side constants and helper functions:
  - `ANNOTATION_RECORD_OBJECT`
  - `ANNOTATION_COLLECTION_OBJECT`
  - `SCHEMA_VERSION`
  - `normalize_annotation_record()`
  - `normalize_annotation_arrays()`
  - `annotation_categories_for_instance()`
  - `replacement_instance_ids()`
- Added additive parser payload field:
  - `GameStateEvent.payload["normalized_annotations"]`
- No workbook columns, webhook fields, Apps Script mappings, runtime status
  schema, failed-post schema, parser event class schema, match identity, game
  identity, or deduplication interfaces were changed.

## Validation Evidence

```bash
python3 -m pytest -q tests/test_gre_annotations_parser.py
# 6 passed

python3 -m pytest -q tests/test_gre_game_state_parser.py
# 5 passed

python3 -m pytest -q tests/test_gameplay_actions.py
# 16 passed

python3 -m pytest -q tests/test_opponent_card_observations.py
# 10 passed

python3 -m pytest -q tests/test_parser_diagnostics_mode.py
# 10 passed

python3 -m pytest -q tests/test_golden_replay_harness.py
# 12 passed

python3 -m pytest -q tests/test_parser_regressions.py
# 2 passed

python3 -m pytest -q tests/test_event_schema_snapshots.py
# 6 passed

python3 -m pytest -q tests/test_saved_event_replay.py
# 26 passed

python3 -m pytest -q tests
# 723 passed

python3 -m ruff check src tests
# All checks passed.

git diff --check
# passed

python3 tools/check_protected_surfaces.py --base origin/main
# result: passed
# warnings: 4 pre-existing branch-scope protected-surface warnings for
# src/mythic_edge_parser/app/transforms.py, src/mythic_edge_parser/events.py,
# src/mythic_edge_parser/parsers/__init__.py, and
# src/mythic_edge_parser/parsers/truncation.py
```

## Still-Unverified Layers

- No live workbook, webhook, Apps Script, output transport, or production
  runtime behavior was exercised.
- CI was not run in GitHub from this thread.
- Persistent annotation lifecycle, timer normalization, and GameState
  diff/update/deletion mechanics remain intentionally outside this module.
- The normalizer handles v1 synthetic annotation shapes; broader Arena
  annotation drift remains a future evidence-ledger/diagnostics concern.

## Unrelated Local Files Not Absorbed

The worktree also contains unrelated untracked local artifacts that were not
edited or included in this module:

- `docs/.DS_Store`
- `docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md`
- `docs/contracts/repo_wide_llm_advisory_review_scaffold.md`
- `docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md`

## Reviewer Focus

Please verify that:

- `normalized_annotations` is additive and parser-owned only.
- Raw annotation arrays and `raw_game_state` preservation remain intact.
- Malformed annotation evidence becomes degraded/review-required evidence and
  not clean parser facts.
- Gameplay actions consume only the annotation evidence they previously
  consumed, while using the shared normalizer.
- Opponent-card observations do not gain hidden-information inference.
- The schema snapshot update is limited to the authorized additive GameState
  payload key.

## Next Workflow Action

Next role: Codex E: Module Reviewer in contract-test mode.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #113: Annotation normalization module.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/113
- Related evidence/resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Branch/base: codex/parser-reliability-intelligence
- Contract: docs/contracts/parser_annotation_normalization.md
- Implementation handoff: docs/implementation_handoffs/parser_annotation_normalization_comparison.md

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/contract_test.md
- docs/contracts/parser_annotation_normalization.md
- docs/implementation_handoffs/parser_annotation_normalization_comparison.md
- src/mythic_edge_parser/parsers/gre/annotations.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- tests/test_gre_annotations_parser.py
- tests/test_gre_game_state_parser.py
- src/mythic_edge_parser/app/gameplay_actions.py
- tests/test_gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- tests/test_opponent_card_observations.py
- src/mythic_edge_parser/app/parser_diagnostics.py
- tests/test_parser_diagnostics_mode.py
- src/mythic_edge_parser/app/golden_replay.py
- tests/test_golden_replay_harness.py
- tests/test_parser_regressions.py
- tests/test_event_schema_snapshots.py
- tests/test_saved_event_replay.py

Goal:
Verify the Codex C implementation against the parser annotation normalization contract.

Confirm:
- Raw annotations, persistent_annotations, diff_deleted_persistent_annotation_ids, and raw_game_state behavior remain preserved.
- normalized_annotations is additive, JSON-serializable, deterministic, and parser-owned.
- normalize_annotation_record() and normalize_annotation_arrays() match the contracted shape and malformed-input behavior.
- Source arrays, source indexes, persistent flags, annotation IDs, type names, affected IDs, details, markers, object replacements, zone transfers, evidence status, value source, confidence, degradation flags, and review_required fields follow the contract.
- annotation_categories_for_instance() and replacement_instance_ids() expose only normalized annotation evidence.
- Gameplay actions remain behavior-stable and do not consume persistent annotation semantics unexpectedly.
- Opponent-card observations do not infer hidden cards, complete decklists, or archetypes.
- Diagnostics, golden replay, saved replay, and schema snapshots remain within the contracted parser-owned evidence boundary.
- No workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

Validation:
Run:
python3 -m pytest -q tests/test_gre_annotations_parser.py
python3 -m pytest -q tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_gameplay_actions.py
python3 -m pytest -q tests/test_opponent_card_observations.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_parser_regressions.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
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
- Infer hidden cards, complete decklists, classify archetypes, call model providers, or move parser truth downstream.
- Solve timer normalization or GameState diff/update/deletion mechanics in this module.
- Stage, commit, merge, or open a PR unless separately instructed.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/113"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  verdict: "ready_for_contract_test_review"
  branch: "codex/parser-reliability-intelligence"
  source_artifact: "docs/contracts/parser_annotation_normalization.md"
  target_artifact: "docs/implementation_handoffs/parser_annotation_normalization_comparison.md"
  risk_tier: "High"
  validation:
    - "python3 -m pytest -q tests/test_gre_annotations_parser.py"
    - "python3 -m pytest -q tests/test_gre_game_state_parser.py"
    - "python3 -m pytest -q tests/test_gameplay_actions.py"
    - "python3 -m pytest -q tests/test_opponent_card_observations.py"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q tests/test_parser_regressions.py"
    - "python3 -m pytest -q tests/test_event_schema_snapshots.py"
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
    - "Do not infer hidden cards, complete decklists, classify archetypes, call model providers, or move parser truth downstream."
    - "Do not solve timer normalization or GameState diff/update/deletion mechanics in this module."
```
