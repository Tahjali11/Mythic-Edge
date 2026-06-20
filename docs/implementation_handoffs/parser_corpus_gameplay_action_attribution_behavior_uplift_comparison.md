# Parser Corpus Gameplay Action-Attribution Behavior Uplift Handoff

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/496
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/494
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/495
- Previous merge commit: `f5c533d420058e364405b283a976923ec04d3b66`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/410
- Branch: `codex/parser-corpus-gameplay-action-attribution-behavior-uplift-496`
- Base branch: `main`
- Source artifact:
  `docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md`
- Risk tier: High

## Contract Comparison

The contract authorized moving only `gameplay_stress.action_attribution` beyond
the #410 report-only boundary if a reduced synthetic action-fact packet could
be proven through existing `GameState` -> `gameplay_actions.py` behavior.

The implementation satisfies that path with one focused synthetic test that
emits one local spell action and one opponent spell action through
`gameplay_actions.observe_event()`. The test asserts the bounded parser-owned
facts named by the contract:

- `action_type`
- `actor_relation`
- `game_state_id`, `game_number`, `turn_number`, and timestamp context
- `instance_id`, `grp_id`, `observed_grp_id`, and `identity_hint_source`
- `from_zone_type` and `to_zone_type`
- raw GRE action labels from the action array

No parser source or gameplay-action extraction behavior was changed.

As in the adjacent #494 implementation, the contract suggested
`focused_parser_tests` as an entry type, but the current corpus manifest
validator does not include that vocabulary. The new manifest entry therefore
uses the existing `session_ledger_entry` entry type while preserving the
contracted title, paths, event family, claim families, coverage status, basis,
and non-claims.

## Changes Made

- Added
  `test_gameplay_actions_preserve_reduced_action_attribution_facts` in
  `tests/test_gameplay_actions.py`.
- Added `gameplay_action_attribution_synthetic_action_facts_v1` to
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.
- Added `gameplay_action_attribution_synthetic_action_facts_v1` to
  `tests/fixtures/parser_corpus/session_ledger.v1.json`.
- Updated `tests/test_corpus_parity_report.py` to pin the new manifest row,
  session-ledger row, status movement, readiness count movement, matrix row,
  and non-claims.
- Added this handoff.
- Added
  `docs/contract_test_reports/parser_corpus_gameplay_action_attribution_behavior_uplift.md`.

The contract source artifact was present in the worktree and used as input; it
was not modified by this implementation pass.

## Status Movement

Only one scenario family changed status:

| Scenario family | Before | After |
| --- | --- | --- |
| `gameplay_stress.action_attribution` | `covered_report_only` | `covered_synthetic` |

The resulting corpus parity summary is:

```yaml
total_scenario_families: 45
covered_committed: 6
covered_synthetic: 18
covered_report_only: 15
blocked_private_evidence: 2
blocked_external_boundary: 4
parser_behavior_ready: false
parser_behavior_ready_family_count: 23
pipeline_activation_ready_for_issue_388: false
pipeline_activation_blockers:
  - "report_only_families:15"
  - "blocked_private_evidence_families:2"
  - "blocked_external_boundary_families:4"
```

The corpus is still not parser-behavior ready and does not activate #388 or
#381.

## Preserved Boundaries

- No parser behavior, gameplay-action extraction behavior,
  opponent-card-observation behavior, parser event classes, ActionLogRow shape,
  parser state final reconciliation, router semantics, match/game identity,
  diagnostics, drift, golden replay, feature-equity, evidence-ledger,
  analytics ingest, workbook schema, webhook payload shape, Apps Script
  behavior, Google Sheets sync, output transport, CI gates, merge readiness,
  deploy readiness, production behavior, or final integration policy changed.
- No private Player.log, UTC_Log, live MTGA, private action artifact,
  Manasight raw log, external corpus input, generated data, SQLite artifact,
  runtime artifact, workbook export, secret, credential, token, API key, or
  webhook URL was used.
- The #410 `gameplay_action_attribution_boundary_report_v1` row remains
  report-only non-claim metadata.
- The `gameplay_stress.event_ordering` row remains unchanged.
- The new evidence does not claim causal action truth, hidden-action truth,
  hidden-card truth, opponent intent, complete event ordering, action absence,
  player mistakes, best-line truth, archetype classification, decklist truth,
  gameplay advice, analytics truth, AI truth, coaching truth, private smoke
  success, release readiness, production behavior, #388/#381 activation,
  tracker completion, or full corpus parity.

## Validation Run

- `PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py::test_gameplay_actions_preserve_reduced_action_attribution_facts`
  passed: 1 test.
- `PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py tests/test_corpus_parity_report.py`
  passed: 25 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=18, report_only=15, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`.
- `python3 tools/check_agent_docs.py` passed: checked files 34, errors 0,
  warnings 0.
- Path-scoped secret/private-marker scan passed: scanned paths 7,
  forbidden 0, warnings 0.
- Path-scoped protected-surface scan passed: changed paths 7, forbidden 0,
  warnings 0.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.

## Residual Risks

- The new evidence is synthetic and proves only reduced local/opponent
  action-fact preservation in focused parser tests.
- It does not prove causal action truth, hidden-action truth, hidden-card
  truth, opponent intent, complete event ordering, action absence, player
  mistakes, best-line truth, real private gameplay behavior, analytics truth,
  AI truth, coaching truth, release readiness, production behavior, or full
  corpus parity.
- Remaining report-only, private-evidence, and external-boundary rows keep the
  overall corpus from parser-behavior readiness.

## Reviewer Focus

Codex E should verify:

- no parser source files changed;
- the reduced action-fact packet is present and bounded;
- `gameplay_action_attribution_boundary_report_v1` remains report-only;
- `gameplay_stress.event_ordering` remains report-only and unchanged;
- readiness metrics move exactly one family from report-only to synthetic;
- #388/#381 activation remains false/deferred; and
- no private/external/raw/generated artifacts are present.

## Next Recommended Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #496, gameplay action-attribution
behavior uplift under tracker #158.

Review:
- docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md
- tests/test_gameplay_actions.py
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_behavior_uplift_comparison.md
- docs/contract_test_reports/parser_corpus_gameplay_action_attribution_behavior_uplift.md

Verify that gameplay_stress.action_attribution is promoted only by the new
focused synthetic GameState -> gameplay_actions.py action-fact preservation
test, that gameplay_action_attribution_boundary_report_v1 remains report-only
non-claim metadata, and that gameplay_stress.event_ordering remains unchanged.

Do not target main directly. Do not close tracker #158, #388, #434, or #496.
Do not activate #388 or #381. Do not run private/live checks. Do not claim
causal action truth, hidden-action truth, hidden-card truth, opponent intent,
complete event ordering, action absence, player mistakes, best-line truth,
gameplay advice, analytics truth, AI truth, coaching truth, readiness,
production behavior, full corpus parity, or tracker completion.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/496"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/494"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/495"
  previous_merge_commit: "f5c533d420058e364405b283a976923ec04d3b66"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/410"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_behavior_uplift_comparison.md"
  report_artifact: "docs/contract_test_reports/parser_corpus_gameplay_action_attribution_behavior_uplift.md"
  verdict: "gameplay_action_attribution_behavior_uplift_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-gameplay-action-attribution-behavior-uplift-496"
  base_branch: "main"
  selected_family: "gameplay_stress.action_attribution"
  prior_status: "covered_report_only"
  current_status: "covered_synthetic"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  recommended_next_role: "Codex E: Module Reviewer"
```
