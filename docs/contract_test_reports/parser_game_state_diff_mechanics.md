# Parser GameState Diff Mechanics Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/117

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/115

Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/116

Previous merge commit: `1afd981bc36ea3ebb68564a04f7ca985367ca9bf`

## Contract

- `docs/contracts/parser_game_state_diff_mechanics.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch: `codex/parser-reliability-intelligence`

Changed files reviewed:

- `docs/contracts/parser_game_state_diff_mechanics.md`
- `docs/implementation_handoffs/parser_game_state_diff_mechanics_comparison.md`
- `src/mythic_edge_parser/parsers/gre/game_state_diff.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_game_state_diff_parser.py`
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

The implementation satisfies the parser GameState diff mechanics contract in
the reviewed scope. `game_state_diff_mechanics` is an additive parser-owned
`GameStateEvent.payload` field, diff GameState messages are not represented as
complete snapshots, deletion markers remain evidence only, and malformed or
unknown update/linkage/deletion metadata becomes degraded or review-required
metadata instead of reconstructed state.

Next recommended role: Codex F: Module Submitter.

## Contract Summary

The GameState diff mechanics module must preserve existing raw and
backward-compatible GameState payload fields while adding a stable
parser-owned metadata object for update kind, queued source classification,
previous-state linkage, deletion markers, section counts, degradation flags,
and review status. It must not reconstruct missing GameState data, treat diffs
as complete snapshots, infer hidden information, or move GameState diff truth
into workbook formulas, dashboards, webhook transport, Apps Script, runtime
status files, AI, or analytics surfaces.

## Checks Run

```bash
git fetch --prune
gh issue view 117 --json number,title,state,body,labels,url
python3 -m pytest -q tests/test_gre_game_state_diff_parser.py
python3 -m pytest -q tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_gre_annotations_parser.py tests/test_gre_timers_parser.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
python3 -m pytest -q tests/test_parsers.py tests/test_parser_regressions.py
python3 -m pytest -q tests/test_saved_event_replay.py
python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' src/mythic_edge_parser/parsers/gre/game_state_diff.py src/mythic_edge_parser/parsers/gre/game_state.py tests/test_gre_game_state_diff_parser.py tests/test_gre_game_state_parser.py tests/fixtures/schema_snapshots/parser_payload_keys.json docs/contracts/parser_game_state_diff_mechanics.md docs/implementation_handoffs/parser_game_state_diff_mechanics_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main
python3 tools/check_secret_patterns.py --base origin/main
python3 -m pytest -q tests
```

## Results

- Issue #117: open, tracker #47-linked, parser reliability branch scope
  confirmed.
- GameState diff mechanics tests: `7 passed in 0.05s`.
- GameState parser tests: `5 passed in 0.05s`.
- Annotation and timer parser tests: `12 passed in 0.06s`.
- Event schema snapshot tests: `6 passed in 0.18s`.
- Parser diagnostics mode tests: `10 passed in 0.09s`.
- Golden replay harness tests: `12 passed in 0.26s`.
- Gameplay action and opponent observation tests: `26 passed in 0.19s`.
- Parser dispatch and regression tests: `20 passed in 0.14s`.
- Saved event replay tests: `26 passed in 0.07s`.
- Golden replay CLI over committed manifests:
  `Golden replay: pass (2 manifests, 2 pass, 0 degraded, 0 review, 0 diff, 0 fail)`.
- Ruff: `All checks passed!`.
- `git diff --check`: passed with no output.
- Explicit #117 changed-path protected-surface gate: `changed_paths: 7`,
  `forbidden: 0`, `warnings: 2`, `result: passed`.
- Branch-scope protected-surface gate against `origin/main`: `changed_paths: 52`,
  `forbidden: 0`, `warnings: 8`, `result: passed`.
- `tools/check_secret_patterns.py`: unavailable on this branch.
- Full local test suite: `736 passed in 1.83s`.

The two explicit #117 protected-surface warnings are contract-authorized
parser-owned changes:
`src/mythic_edge_parser/parsers/gre/game_state_diff.py` and
`src/mythic_edge_parser/parsers/gre/game_state.py`.

The branch-scope protected-surface warnings include prior parser reliability
surfaces already present on `codex/parser-reliability-intelligence`, plus the
current GameState integration surface:
`src/mythic_edge_parser/app/gameplay_actions.py`,
`src/mythic_edge_parser/app/transforms.py`,
`src/mythic_edge_parser/events.py`,
`src/mythic_edge_parser/parsers/__init__.py`,
`src/mythic_edge_parser/parsers/gre/annotations.py`,
`src/mythic_edge_parser/parsers/gre/game_state.py`,
`src/mythic_edge_parser/parsers/gre/timers.py`, and
`src/mythic_edge_parser/parsers/truncation.py`.

## Confirmed Contract Matches

- `src/mythic_edge_parser/parsers/gre/game_state_diff.py` exposes the
  contracted object marker, schema version, and
  `build_game_state_diff_mechanics()` helper.
- The helper returns JSON-serializable deterministic dictionaries and preserves
  the input `message` and `gsm` objects without mutation.
- `GameStateEvent.payload["game_state_diff_mechanics"]` is additive and
  parser-owned.
- Existing top-level `update`, `pending_message_count`, `prev_game_state_id`,
  `diff_deleted_instance_ids`, and
  `diff_deleted_persistent_annotation_ids` remain present and backward
  compatible.
- Raw `players`, `zones`, `game_objects`, `annotations`,
  `persistent_annotations`, `timers`, `actions`, and `raw_game_state` remain
  preserved with existing shallow-copy/raw-reference behavior.
- Existing `normalized_annotations` and `normalized_timers` behavior remains
  preserved.
- The normalized object includes the required shape: object marker, schema,
  source payload type, message type, queue flag, GameState IDs, message ID,
  update raw/kind, state completeness, complete-snapshot boolean, pending
  count, previous-state ID/status, linkage status, deletion evidence, deletion
  counts, section counts, source-field evidence, evidence labels, confidence,
  degradation flags, and review status.
- Regular and queued GameState payloads both receive the same normalized
  mechanics shape.
- `full` updates map to `complete_snapshot` with
  `is_complete_snapshot is True`.
- `diff` updates map to `partial_update` with
  `is_complete_snapshot is False`.
- Missing update kinds become unknown and review-required without crashing.
- Unknown non-empty update kinds become degraded and review-required.
- Clean previous-state linkage is classified as `linked`.
- Diff updates without previous-state IDs are degraded with
  `missing_prev_game_state_id`.
- Malformed previous-state IDs are degraded with
  `malformed_prev_game_state_id`.
- Self-referential and future previous-state IDs are degraded.
- Deletion ID lists are copied from existing normalized top-level lists, source
  order is preserved, counts are correct, and
  `deletion_evidence_present` is a boolean output rather than a degradation
  flag.
- Malformed deletion source shapes add the matching degradation flags while
  preserving already-normalized valid IDs supplied by the top-level
  normalization.
- Section counts are counts only and do not duplicate raw sections or imply
  completeness.
- Full updates with deletion markers remain full updates and are not inferred
  as diffs.
- Queue status is source classification only and does not automatically degrade
  the payload.
- Current GRE dispatch and current-over-queued selection semantics are not
  changed in the reviewed diff.
- The parser payload schema snapshot update is limited to the authorized
  additive `game_state_diff_mechanics` key.
- No parser event class, parser state final reconciliation, match/game
  identity, deduplication, workbook schema, webhook payload shape, Apps Script
  behavior, output transport, runtime status schema, failed-post schema,
  workbook export, secret, credential, environment variable, OpenAI or
  model-provider surface change was found in the #117 scope.
- No full-state reconstruction, hidden-card inference, decklist completion,
  archetype classification, gameplay advice, player-mistake labeling,
  clock-pressure analytics, feature-equity corpus ratchet/reporting, or
  field-level parity audit behavior was introduced.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests found.

Focused tests cover the object marker and schema, JSON serialization,
non-mutation, full and diff update mapping, queued source classification,
missing and unknown update behavior, clean/missing/malformed/self/future
linkage boundaries, deletion evidence and malformed deletion source shapes,
negative pending counts, section counts, no-reconstruction boundaries,
additive GameState payload behavior, raw field preservation, snapshot key
updates, annotation/timer compatibility, diagnostics compatibility, golden
replay compatibility, gameplay action and opponent observation compatibility,
parser dispatch/regression behavior, and saved event replay behavior.

Non-blocking note: diagnostics summaries, golden replay manifest assertions,
evidence-ledger citation, and future gameplay-action use of this normalized
object remain future consumer work and are not required by v1.

## Drift Notes

- Repo drift: expected addition of a parser-side GRE GameState diff mechanics
  helper, additive GameState payload field, focused tests, schema snapshot
  update, contract, handoff, and this contract-test report.
- Parser behavior drift: contract-authorized additive normalized GameState
  diff mechanics evidence only.
- Raw GameState payload drift: none found for existing raw sections or
  `raw_game_state`.
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
  #117 scope.
- Previous parser reliability drift: branch comparisons against `origin/main`
  still include prior issue #107, #113, and #115 surfaces; those are not part
  of this #117 finding set.

## Remaining Non-Blocking Gaps

- Remote CI has not run in this local Codex E pass.
- `tools/check_secret_patterns.py` is absent on this branch, so the optional
  branch-native content scanner was recorded as unavailable.
- Live Arena diff/update/deletion shape drift remains future
  evidence-ledger/diagnostics work, not a blocker for this v1 parser-owned
  mechanics package.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #117: GameState diff/update/deletion mechanics module.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- Related resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/117
- Branch/base: codex/parser-reliability-intelligence
- Contract: docs/contracts/parser_game_state_diff_mechanics.md
- Implementation handoff: docs/implementation_handoffs/parser_game_state_diff_mechanics_comparison.md
- Contract-test report: docs/contract_test_reports/parser_game_state_diff_mechanics.md
- Previous completed issue: #115 GameState timer normalization
- Previous PR: #116
- Previous merge commit: 1afd981bc36ea3ebb68564a04f7ca985367ca9bf

Goal:
Prepare the GameState diff mechanics package for PR submission into codex/parser-reliability-intelligence.

Scope to include:
- docs/contracts/parser_game_state_diff_mechanics.md
- docs/implementation_handoffs/parser_game_state_diff_mechanics_comparison.md
- docs/contract_test_reports/parser_game_state_diff_mechanics.md
- src/mythic_edge_parser/parsers/gre/game_state_diff.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- tests/test_gre_game_state_diff_parser.py
- tests/test_gre_game_state_parser.py
- tests/fixtures/schema_snapshots/parser_payload_keys.json

Do not include unrelated local files:
- docs/.DS_Store
- docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md
- docs/contracts/repo_wide_llm_advisory_review_scaffold.md
- docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md

Codex E verdict:
No blocking findings. The implementation satisfies the parser GameState diff mechanics contract in the reviewed scope. game_state_diff_mechanics is additive and parser-owned; diff GameState payloads are not complete snapshots; deletion markers are evidence only; malformed update/linkage/deletion metadata is reviewable/degraded; and no downstream truth, workbook, webhook, Apps Script, parser state, event class, identity, deduplication, runtime, failed-post, export, secret, model-provider, or AI/analytics surface changed.

Validation reviewed:
- python3 -m pytest -q tests/test_gre_game_state_diff_parser.py -> 7 passed
- python3 -m pytest -q tests/test_gre_game_state_parser.py -> 5 passed
- python3 -m pytest -q tests/test_gre_annotations_parser.py tests/test_gre_timers_parser.py -> 12 passed
- python3 -m pytest -q tests/test_event_schema_snapshots.py -> 6 passed
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py -> 10 passed
- python3 -m pytest -q tests/test_golden_replay_harness.py -> 12 passed
- python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py -> 26 passed
- python3 -m pytest -q tests/test_parsers.py tests/test_parser_regressions.py -> 20 passed
- python3 -m pytest -q tests/test_saved_event_replay.py -> 26 passed
- python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay -> pass
- python3 -m ruff check src tests tools -> All checks passed
- git diff --check -> passed
- explicit #117 protected-surface gate -> forbidden 0, warnings 2, result passed
- branch-scope protected-surface gate -> forbidden 0, warnings 8, result passed
- python3 -m pytest -q tests -> 736 passed

Submitter responsibilities:
- Verify the exact staged/committed scope.
- Create or update the PR against codex/parser-reliability-intelligence.
- Do not target main.
- Do not merge, close issue #117, close tracker #47, or close related issue #11.
- Leave merge/deployment/issue closure/tracker updates for Codex G.

Stop conditions:
- Do not include unrelated local files.
- Do not reconstruct missing GameState data or treat diff GameState messages as full state snapshots.
- Do not change parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status files, failed posts, workbook exports, secrets, credentials, environment variables, OpenAI/model-provider behavior, or AI/analytics truth.
- Do not infer hidden cards, complete decklists, archetypes, gameplay advice, player mistakes, or clock-pressure analytics.
- Do not copy Manasight source code or commit raw private Player.log excerpts, generated data, local logs, failed posts, runtime status files, or workbook exports.
- Do not solve feature-equity corpus ratchet/reporting or field-level parity audit in this module.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/117"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/115"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/116"
  previous_merge_commit: "1afd981bc36ea3ebb68564a04f7ca985367ca9bf"
  completed_thread: "E"
  next_thread: "F"
  verdict: "No blocking findings. Ready for Codex F."
  branch: "codex/parser-reliability-intelligence"
  source_artifact: "docs/contracts/parser_game_state_diff_mechanics.md"
  target_artifact: "docs/contract_test_reports/parser_game_state_diff_mechanics.md"
  risk_tier: "High"
  validation:
    - "python3 -m pytest -q tests/test_gre_game_state_diff_parser.py -> 7 passed"
    - "python3 -m pytest -q tests/test_gre_game_state_parser.py -> 5 passed"
    - "python3 -m pytest -q tests/test_gre_annotations_parser.py tests/test_gre_timers_parser.py -> 12 passed"
    - "python3 -m pytest -q tests/test_event_schema_snapshots.py -> 6 passed"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py -> 10 passed"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py -> 12 passed"
    - "python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py -> 26 passed"
    - "python3 -m pytest -q tests/test_parsers.py tests/test_parser_regressions.py -> 20 passed"
    - "python3 -m pytest -q tests/test_saved_event_replay.py -> 26 passed"
    - "python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay -> pass"
    - "python3 -m ruff check src tests tools -> All checks passed!"
    - "git diff --check -> passed"
    - "explicit #117 protected-surface gate -> forbidden 0, warnings 2, result passed"
    - "branch-scope protected-surface gate -> forbidden 0, warnings 8, result passed"
    - "python3 -m pytest -q tests -> 736 passed"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not include unrelated local files."
    - "Do not reconstruct missing GameState data or treat diff GameState messages as full state snapshots."
    - "Do not change parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status files, failed posts, workbook exports, secrets, credentials, environment variables, OpenAI/model-provider behavior, or AI/analytics truth."
    - "Do not infer hidden cards, complete decklists, archetypes, gameplay advice, player mistakes, or clock-pressure analytics."
    - "Do not copy Manasight source code or commit raw private Player.log excerpts, generated data, local logs, failed posts, runtime status files, or workbook exports."
    - "Do not solve feature-equity corpus ratchet/reporting or field-level parity audit in this module."
```
