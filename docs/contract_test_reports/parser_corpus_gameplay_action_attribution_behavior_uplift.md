# Parser Corpus Gameplay Action-Attribution Behavior Uplift Report

## Verdict

`gameplay_stress.action_attribution` has one reduced synthetic
parser-behavior uplift ready for Codex E review.

The evidence is narrow. It proves that existing `GameState` ->
`gameplay_actions.py` behavior preserves bounded local and opponent
action-fact fields. It does not claim causal action truth, hidden-action
truth, hidden-card truth, opponent intent, complete event ordering, action
absence, player mistakes, best-line truth, gameplay advice, analytics truth,
AI truth, coaching truth, tracker completion, #388/#381 activation, readiness,
production behavior, or full corpus parity.

## Evidence Added

- Gameplay-action parser evidence:
  `test_gameplay_actions_preserve_reduced_action_attribution_facts`
- Corpus manifest entry:
  `gameplay_action_attribution_synthetic_action_facts_v1`
- Session-ledger entry:
  `gameplay_action_attribution_synthetic_action_facts_v1`

The #410 entry `gameplay_action_attribution_boundary_report_v1` remains present
and report-only. The `gameplay_stress.event_ordering` row remains unchanged.

## Parser-Owned Evidence

The focused parser test verifies:

- two emitted gameplay-action entries;
- one local actor relation and one opponent actor relation;
- preserved `spell_cast` action type for both entries;
- preserved `game_state_id`, `game_number`, `turn_number`, and timestamp
  context;
- preserved `instance_id`, `grp_id`, `observed_grp_id`, and
  `identity_hint_source`;
- preserved hand-to-stack zone movement;
- preserved raw GRE action labels from the action arrays; and
- temporary runtime output paths under the test directory.

The corpus metadata records the existing parser event family only:

- `GameState`

## Corpus Status Effect

Before issue #496:

```yaml
gameplay_stress.action_attribution:
  coverage_status: "covered_report_only"
  coverage_basis:
    - "fixture_metadata_only"
  mythic_edge_entries:
    - "gameplay_action_attribution_boundary_report_v1"
```

After issue #496:

```yaml
gameplay_stress.action_attribution:
  coverage_status: "covered_synthetic"
  coverage_basis:
    - "fixture_metadata_only"
    - "parser_behavior_verified"
  mythic_edge_entries:
    - "gameplay_action_attribution_boundary_report_v1"
    - "gameplay_action_attribution_synthetic_action_facts_v1"
```

Current overall corpus summary:

```yaml
total_scenario_families: 45
covered_committed: 6
covered_synthetic: 18
covered_report_only: 15
blocked_private_evidence: 2
blocked_external_boundary: 4
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
```

## Privacy And Protected Boundaries

- No private Player.log, UTC_Log, live MTGA, private gameplay action artifact,
  private smoke output, Manasight raw log, external corpus input, generated
  data, SQLite artifact, runtime artifact, workbook export, secret,
  credential, token, API key, or webhook URL was used.
- No parser behavior, gameplay-action extraction behavior,
  opponent-card-observation behavior, parser event classes, ActionLogRow
  shape, parser state final reconciliation, router semantics, match/game
  identity, diagnostics, drift, golden replay, feature-equity,
  evidence-ledger, analytics ingest, workbook schema, webhook payload shape,
  Apps Script behavior, Google Sheets sync, output transport, CI gates, merge
  readiness, deploy readiness, production behavior, or final integration
  policy changed.
- The #410 report-only row was preserved.
- The event-ordering row was not promoted.

## Non-Claims

This report does not claim:

- causal action truth;
- hidden-action truth;
- hidden-card truth;
- opponent intent;
- complete event ordering;
- action absence;
- player mistakes;
- best-line truth;
- archetype classification;
- decklist truth;
- gameplay advice;
- analytics truth;
- AI truth;
- coaching truth;
- private smoke success;
- release readiness;
- production behavior;
- full corpus parity;
- tracker completion;
- #388 or #381 activation.

## Validation

- `PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py::test_gameplay_actions_preserve_reduced_action_attribution_facts`
  passed: 1 test.
- `PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py tests/test_corpus_parity_report.py`
  passed: 25 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=18, report_only=15, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`.
- `python3 tools/check_agent_docs.py` passed.
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
  truth, opponent intent, complete event ordering, real private gameplay
  behavior, analytics truth, AI truth, coaching truth, release readiness,
  production behavior, or full corpus parity.
- Overall corpus readiness remains blocked by report-only, private-evidence,
  and external-boundary rows.

## Codex E Contract-Test Review

Report lifecycle: `final_approval`

### Findings

No blocking findings.

No non-blocking implementation findings were identified in this review pass.

### Contract-Test Verdict

Approved for Codex F module submission.

The implementation satisfies the #496 contract as a narrow synthetic
behavior-uplift package. It promotes only
`gameplay_stress.action_attribution` from `covered_report_only` to
`covered_synthetic`, preserves the #410 report-only boundary entry, keeps
`gameplay_stress.event_ordering` unchanged, and leaves #388/#381 activation
false.

This review does not authorize merge, deployment, tracker closure, private/live
checks, parser-evidence pipeline activation, or any production-readiness claim.

### Contract Matches

- The changed scope is limited to the authorized contract, handoff, report,
  corpus manifest, session ledger, corpus parity tests, and gameplay-action
  focused test.
- `gameplay_action_attribution_synthetic_action_facts_v1` is synthetic,
  committed, privacy-safe metadata tied to issue #496.
- The new focused parser test proves existing `GameState` ->
  `gameplay_actions.py` behavior preserves two bounded action entries: one
  local and one opponent.
- The focused test asserts action type, actor relation, game/timing context,
  instance IDs, GRP identity hints, hand-to-stack zone movement, raw GRE action
  labels, and temporary runtime-output redirection.
- The manifest and session ledger keep the evidence scoped to `GameState` and
  explicitly preserve non-claims for causal truth, hidden-action truth,
  hidden-card truth, opponent intent, complete event ordering, player mistakes,
  gameplay advice, analytics truth, AI truth, coaching truth, release
  readiness, production behavior, tracker completion, and full corpus parity.
- Corpus readiness metrics move exactly one family from report-only to
  synthetic: synthetic 17 -> 18 and report-only 16 -> 15.
- `parser_behavior_ready` and `pipeline_activation_ready_for_issue_388` remain
  `false`.

### Contract Mismatches

None found.

### Missing Tests Or Safeguards

None blocking.

The focused test and corpus parity assertions cover the contracted reduced
action-fact packet and the row/status/readiness deltas. Full pytest also passed
as an extra confidence check.

### Validation Rerun

- `PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py::test_gameplay_actions_preserve_reduced_action_attribution_facts`
  passed: 1 test.
- `PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py tests/test_corpus_parity_report.py`
  passed: 25 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=18, report_only=15, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`.
- Path-scoped secret/private-marker scan for the 7 changed/untracked package
  files passed: forbidden 0, warnings 0.
- Path-scoped protected-surface gate for the 7 changed/untracked package files
  passed: forbidden 0, warnings 0.
- Path-scoped validation selector for the 7 changed/untracked package files
  passed with selection status `ok`.
- `python3 tools/check_agent_docs.py` passed: checked files 34, errors 0,
  warnings 0.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.
- `PYTHONPATH=src python3 -m pytest -q` passed: 1775 tests.

### Drift Classification

- Parser behavior drift: none found.
- Gameplay-action extraction behavior drift: none found.
- Corpus status drift: intentional and contract-authorized for
  `gameplay_stress.action_attribution` only.
- Adjacent row drift: none found; `gameplay_stress.event_ordering` remains
  report-only.
- Private/local/generated artifact drift: none found in the final worktree
  sweep after validation.
- Workbook, webhook, Apps Script, analytics, AI/coaching, CI, merge/deploy, and
  production drift: none found.

### Remaining Risks

- The evidence is synthetic and proves only reduced local/opponent action-fact
  preservation.
- It does not prove causal action truth, hidden actions, hidden cards, opponent
  intent, complete event ordering, action absence, private gameplay behavior,
  analytics truth, AI truth, coaching truth, release readiness, production
  behavior, #388/#381 activation, tracker completion, or full corpus parity.
- Remaining report-only, private-evidence, and external-boundary rows still
  block overall parser-behavior readiness.

### Next Recommended Role

Codex F: Module Submitter.

### Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/496"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/494"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/495"
  previous_merge_commit: "f5c533d420058e364405b283a976923ec04d3b66"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md"
  target_artifact: "docs/contract_test_reports/parser_corpus_gameplay_action_attribution_behavior_uplift.md"
  verdict: "ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-gameplay-action-attribution-behavior-uplift-496"
  base_branch: "main"
  selected_family: "gameplay_stress.action_attribution"
  prior_status: "covered_report_only"
  current_status: "covered_synthetic"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  next_recommended_role: "Codex F: Module Submitter"
```
