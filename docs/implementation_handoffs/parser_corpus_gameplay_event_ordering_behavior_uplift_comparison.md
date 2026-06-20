# Parser Corpus Gameplay Event-Ordering Behavior Uplift Handoff

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/498
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/496
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/497
- Previous merge commit: `6ab8950e74f162af93b3e8ae0c950244d69cbcf1`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/412
- Branch: `codex/parser-corpus-gameplay-event-ordering-behavior-uplift-498`
- Base branch: `main`
- Source artifact:
  `docs/contracts/parser_corpus_gameplay_event_ordering_behavior_uplift.md`
- Risk tier: High

## Contract Comparison

The contract authorized moving only `gameplay_stress.event_ordering` beyond
the #412 report-only boundary if a reduced synthetic sequence packet could be
proven through existing parser-owned behavior.

The implementation satisfies that path with one focused synthetic
`GameState` -> `gameplay_actions.py` test. The test observes four ordered
synthetic GameState events and asserts the three emitted gameplay-action
entries preserve the selected order by:

- `game_state_id`;
- timestamp context;
- `action_type`;
- `actor_relation`;
- `instance_id`;
- `grp_id`;
- source and destination zone types; and
- raw GRE action labels.

No parser source, router behavior, GRE parser behavior, gameplay-action
extraction behavior, golden replay behavior, or runtime behavior was changed.

The contract suggested a dedicated reduced synthetic event-ordering sequence
packet. The new manifest/session-ledger entry uses the established corpus
metadata pattern and records `parser_behavior_verified` for only the bounded
synthetic sequence.

## Changes Made

- Added
  `test_gameplay_actions_preserve_reduced_event_ordering_sequence` in
  `tests/test_gameplay_actions.py`.
- Added `gameplay_event_ordering_synthetic_sequence_v1` to
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.
- Added `gameplay_event_ordering_synthetic_sequence_v1` to
  `tests/fixtures/parser_corpus/session_ledger.v1.json`.
- Updated `tests/test_corpus_parity_report.py` to pin the new manifest row,
  session-ledger row, status movement, readiness count movement, matrix row,
  and non-claims.
- Added this handoff.
- Added
  `docs/contract_test_reports/parser_corpus_gameplay_event_ordering_behavior_uplift.md`.

The contract source artifact was present in the worktree and used as input; it
was not modified by this implementation pass.

## Status Movement

Only one scenario family changed status:

| Scenario family | Before | After |
| --- | --- | --- |
| `gameplay_stress.event_ordering` | `covered_report_only` | `covered_synthetic` |

The resulting corpus parity summary is:

```yaml
total_scenario_families: 45
covered_committed: 6
covered_synthetic: 19
covered_report_only: 14
blocked_private_evidence: 2
blocked_external_boundary: 4
parser_behavior_ready: false
parser_behavior_ready_family_count: 24
pipeline_activation_ready_for_issue_388: false
pipeline_activation_blockers:
  - "report_only_families:14"
  - "blocked_private_evidence_families:2"
  - "blocked_external_boundary_families:4"
```

The corpus is still not parser-behavior ready and does not activate #388 or
#381.

## Preserved Boundaries

- No parser behavior, router behavior, GRE parser behavior, GameState parser
  behavior, gameplay-action extraction behavior, opponent-card-observation
  behavior, parser event classes, parser state final reconciliation,
  match/game identity, diagnostics, drift, golden replay, feature-equity,
  evidence-ledger, analytics behavior, workbook schema, webhook payload shape,
  Apps Script behavior, Google Sheets sync, output transport, CI gates, merge
  readiness, deploy readiness, production behavior, or final integration
  policy changed.
- No private Player.log, UTC_Log, live MTGA, private gameplay artifact,
  private smoke output, Manasight raw log, external corpus input, generated
  data, SQLite artifact, runtime artifact, workbook export, secret,
  credential, token, API key, or webhook URL was used.
- The #412 `gameplay_event_ordering_boundary_report_v1` row remains
  report-only non-claim metadata.
- The #496 `gameplay_action_attribution_synthetic_action_facts_v1` row remains
  action-fact evidence only and is not used as event-ordering support.
- The new evidence does not claim complete event-sequence truth, causal
  ordering truth, hidden-action truth, hidden-card truth, opponent intent,
  action absence, player mistakes, best-line truth, gameplay advice, analytics
  truth, AI truth, coaching truth, private smoke success, release readiness,
  production behavior, #388/#381 activation, tracker completion, or full
  corpus parity.

## Validation Run

- `PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py::test_gameplay_actions_preserve_reduced_event_ordering_sequence`
  passed: 1 test.
- `PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py tests/test_corpus_parity_report.py`
  passed: 26 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=19, report_only=14, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`.
- `python3 tools/check_agent_docs.py` passed.
- Path-scoped secret/private-marker scan passed: scanned paths 7,
  forbidden 0, warnings 0.
- Path-scoped protected-surface scan passed: changed paths 7, forbidden 0,
  warnings 0.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.

No router, GRE, or golden-replay focused tests were run because the
implementation touched no router, GRE parser, GameState parser, or golden
replay files. The contracted route allowed the narrower focused
`tests/test_gameplay_actions.py` path for this implementation.

## Residual Risks

- The new evidence is synthetic and proves only reduced parser-observed
  sequence preservation for one bounded synthetic path.
- It does not prove complete event-sequence truth, causal ordering truth,
  hidden-action truth, hidden-card truth, opponent intent, action absence,
  player mistakes, best-line truth, real private gameplay behavior, analytics
  truth, AI truth, coaching truth, release readiness, production behavior, or
  full corpus parity.
- Remaining report-only, private-evidence, and external-boundary rows keep the
  overall corpus from parser-behavior readiness.

## Reviewer Focus

Codex E should verify:

- no parser source files changed;
- the reduced event-ordering sequence packet is present and bounded;
- `gameplay_event_ordering_boundary_report_v1` remains report-only;
- `gameplay_action_attribution_synthetic_action_facts_v1` is not used as the
  event-ordering evidence source;
- readiness metrics move exactly one family from report-only to synthetic;
- #388/#381 activation remains false/deferred; and
- no private/external/raw/generated artifacts are present.

## Next Recommended Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #498, gameplay event-ordering
behavior uplift under tracker #158.

Review:
- docs/contracts/parser_corpus_gameplay_event_ordering_behavior_uplift.md
- tests/test_gameplay_actions.py
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_behavior_uplift_comparison.md
- docs/contract_test_reports/parser_corpus_gameplay_event_ordering_behavior_uplift.md

Verify that gameplay_stress.event_ordering is promoted only by the new
focused synthetic GameState -> gameplay_actions.py sequence-preservation test,
that gameplay_event_ordering_boundary_report_v1 remains report-only non-claim
metadata, and that #496 action-attribution evidence is not treated as
event-ordering support.

Do not target main directly. Do not close tracker #158, #388, #434, or #498.
Do not activate #388 or #381. Do not run private/live checks. Do not claim
complete event-sequence truth, causal ordering truth, hidden-action truth,
hidden-card truth, opponent intent, action absence, player mistakes,
best-line truth, gameplay advice, analytics truth, AI truth, coaching truth,
readiness, production behavior, full corpus parity, or tracker completion.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/498"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/496"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/497"
  previous_merge_commit: "6ab8950e74f162af93b3e8ae0c950244d69cbcf1"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/412"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_gameplay_event_ordering_behavior_uplift.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_behavior_uplift_comparison.md"
  report_artifact: "docs/contract_test_reports/parser_corpus_gameplay_event_ordering_behavior_uplift.md"
  verdict: "gameplay_event_ordering_behavior_uplift_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-gameplay-event-ordering-behavior-uplift-498"
  base_branch: "main"
  selected_family: "gameplay_stress.event_ordering"
  prior_status: "covered_report_only"
  current_status: "covered_synthetic"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
```
