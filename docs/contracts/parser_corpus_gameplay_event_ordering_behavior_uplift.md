# Parser Corpus Gameplay Event-Ordering Behavior Uplift Contract

## Module

`gameplay_stress.event_ordering` parser corpus behavior uplift planning.

Plain English: Mythic Edge already records event-ordering coverage as
report-only boundary metadata from issue #412. This contract defines the
narrowest safe path for moving the row toward parser-behavior readiness:
reduced synthetic parser-observed sequence preservation only. The uplift may
prove that existing parser and gameplay-action surfaces preserve a bounded
ordered sequence for owned synthetic evidence. It must not claim complete
event-sequence truth, causal ordering truth, hidden-action truth, hidden-card
truth, opponent intent, player mistakes, best-line truth, gameplay advice,
analytics truth, AI truth, coaching truth, release readiness, production
behavior, tracker completion, or full corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/498
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/496
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/497
- Previous merge commit: `6ab8950e74f162af93b3e8ae0c950244d69cbcf1`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/412
- Base branch inspected: `main`
- Contract branch:
  `codex/parser-corpus-gameplay-event-ordering-behavior-uplift-498`
- Risk tier: High
- Status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority:

- `docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md`
- `docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md`
- `docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md`
- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- `docs/contracts/parser_corpus_readiness_metrics.md`
- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_runner.md`
- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`
- `docs/contracts/parser_corpus_missing_message_type_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- relevant parser, gameplay-action, and golden replay tests as reference only

## Purpose

Define the minimum safe evidence model for moving
`gameplay_stress.event_ordering` beyond the #412 report-only boundary.

This contract answers:

- whether the row may move from `covered_report_only` toward
  `covered_synthetic`;
- what reduced synthetic parser-observed ordering evidence is sufficient;
- what `parser_behavior_verified` may and may not mean for this row;
- how #496 action-attribution evidence may be used as adjacent context only;
  and
- how #388 / #381 activation remains deferred.

This contract does not implement code, create fixtures, edit corpus metadata,
run private/live MTGA checks, activate #388/#381, or claim event-ordering
support beyond reduced synthetic parser-observed sequence preservation.

## Observed Current Behavior

Observed on `main` at
`6ab8950e74f162af93b3e8ae0c950244d69cbcf1`:

- Issue #498 is open.
- Tracker #158 remains open.
- Related pipeline tracker #388 remains open and deferred.
- Parent private-evidence issue #434 remains open.
- Issue #496 is complete after PR #497.
- The corpus parity report state recorded by issue #498 is:

```text
45 families; committed=6, synthetic=18, report_only=15,
blocked_private=2, blocked_external=4, missing=0,
parser_behavior_ready=false,
pipeline_activation_ready_for_issue_388=false
```

Current `gameplay_stress.event_ordering` row:

```yaml
scenario_family: "gameplay_stress.event_ordering"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "gameplay_event_ordering_boundary_report_v1"
parser_event_families: []
parser_claim_families:
  - "gameplay_event_ordering_boundary_report"
  - "parser_timestamps_not_complete_ordering_truth"
  - "router_dispatch_order_not_stress_coverage"
  - "gameplay_action_order_not_event_sequence_truth"
  - "action_attribution_not_event_ordering_truth"
  - "diagnostics_replay_reports_not_parser_truth"
  - "hidden_action_inference_non_claim"
```

Current adjacent parser behavior:

- `src/mythic_edge_parser/router.py` extracts a timestamp per log entry when
  present and dispatches to parser modules in a configured order.
- `dispatch_to_parsers(entry, timestamp)` returns the first parser result for
  the entry, preserving the parser-provided list order when a parser emits
  multiple events.
- GRE GameState parsing carries `msg_id`, `game_state_id`, message type,
  payload type, raw GameState copy, identity fields, turn info, annotations,
  timers, actions, and diff fields.
- `src/mythic_edge_parser/app/gameplay_actions.py` observes `GameState` events
  and writes action entries in the order current code emits them.
- Focused action-attribution tests now assert bounded local and opponent
  action facts, including action type, actor relation, timestamps,
  `game_state_id`, raw action labels, zone movement, and card identity hints.
- Corpus metadata for issue #496 now includes
  `gameplay_action_attribution_synthetic_action_facts_v1` as
  `covered_synthetic` with `parser_behavior_verified`.

Current non-evidence:

- The #412 boundary explicitly says parser timestamps, router dispatch order,
  GRE message order, gameplay-action row order, action-attribution coverage,
  diagnostics, golden replay, feature-equity, evidence-ledger provenance,
  analytics ingest, and public taxonomy metadata are not event-ordering stress
  support by themselves.
- The #496 action-attribution uplift explicitly preserves
  `event_ordering_non_claim`; it proves reduced action-fact preservation, not
  event-ordering support.
- No current corpus entry proves a dedicated reduced event-ordering expectation
  packet for `gameplay_stress.event_ordering`.
- `drift_debug.missing_message_type` remains a separate row and must not be
  folded into this uplift.

## Scope Decision

Recommended future path: reduced synthetic parser-observed event-ordering
uplift.

A later Codex C implementation may move
`gameplay_stress.event_ordering` from `covered_report_only` toward
`covered_synthetic` with `parser_behavior_verified` only if it adds
Mythic Edge-owned synthetic evidence proving a reduced sequence packet through
existing parser and gameplay-action behavior.

The reduced sequence packet must prove parser-owned preservation of:

- at least three explicitly ordered synthetic observations;
- at least two emitted gameplay-action entries derived from that sequence;
- increasing or otherwise explicitly expected `game_state_id` values;
- increasing or otherwise explicitly expected timestamp context when
  timestamps are present;
- output entry order matching the owned input sequence for the selected
  reduced path;
- raw action labels or parser event identity sufficient to show the sequence
  was observed, not invented by corpus metadata; and
- a clear assertion that the packet proves only reduced parser-observed
  sequence preservation.

The behavior claim is intentionally small:

- parser-observed sequence preservation, not complete game chronology;
- reduced synthetic evidence, not live Player.log health;
- existing parser behavior, not new parser interpretation;
- output order for selected current surfaces, not causal order;
- visible emitted facts only, not hidden actions, hidden cards, or absences.

This contract authorizes a metadata/test/docs implementation path. It does not
authorize parser behavior changes. If Codex C cannot prove the reduced
synthetic sequence packet using existing behavior, the row must remain
`covered_report_only` and route back to Codex B or Codex A.

## Owning Layer

Owning layer: Corpus / Provenance.

Supporting truth layers:

- Router and parser modules own current event dispatch and parser-emitted event
  order.
- GRE GameState parsing owns current message fields and payload preservation.
- `gameplay_actions.py` owns current gameplay-action extraction and action
  entry ordering from observed `GameState` inputs.
- Golden replay owns committed fixture execution only when a later
  implementation chooses a replay-backed route.
- Corpus parity reporting owns status aggregation and readiness metrics.

This contract does not move truth ownership to corpus metadata, workbook
formulas, dashboards, Apps Script, webhook transport, analytics, AI, coaching,
readiness, deploy, production, or tracker lifecycle surfaces.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser, as the existing producer of parser events and gameplay-action facts.
- Quality / Governance, as the owner of validation and protected-surface
  discipline.

This slice is not analytics, AI, coaching, workbook, webhook, Apps Script,
local app, release readiness, production behavior, private-evidence execution,
or parser-evidence pipeline activation.

## Truth Owner

Truth owner for current report-only status:

- `docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for future reduced synthetic behavior evidence:

- the focused parser/gameplay-action tests added or cited by Codex C;
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- `tests/test_corpus_parity_report.py`;
- the future Codex C implementation handoff; and
- the future Codex E contract-test report.

Truth boundary:

- A synthetic event sequence may prove only that existing Mythic Edge behavior
  preserves the selected reduced parser-observed order.
- Corpus parity may claim `parser_behavior_verified` only for the reduced
  event-ordering packet described above.
- Corpus parity must not claim complete event-sequence truth, causal ordering
  truth, hidden-action truth, hidden-card truth, opponent intent, action
  absence, player mistakes, best-line truth, archetype classification,
  decklist truth, gameplay advice, analytics truth, AI truth, coaching truth,
  private smoke success, release readiness, production behavior, #388/#381
  activation, tracker completion, or full corpus parity.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
owned synthetic parser-observed sequence test input
  -> existing parser and gameplay_actions.py behavior
  -> focused test assertions
  -> corpus manifest/session-ledger behavior metadata
  -> corpus parity readiness metrics
```

Forbidden reverse flow:

- Corpus readiness must not change parser behavior.
- Corpus metadata must not create parser-owned facts absent from parser or
  gameplay-action output.
- Corpus metadata must not turn parser timestamps, router dispatch order, GRE
  message order, gameplay-action row order, action-attribution evidence,
  diagnostics, golden replay, feature-equity, evidence-ledger provenance,
  analytics ingest, public taxonomy labels, private action artifacts, or local
  gameplay logs into broad event-ordering support.
- Corpus metadata must not move causality, hidden information, action absence,
  player mistakes, analytics, AI, coaching, workbook, webhook, or Apps Script
  interpretation into parser truth.

Protected surfaces explicitly not touched:

- parser behavior;
- router behavior;
- GRE parser behavior;
- GameState parser behavior;
- gameplay-action extraction behavior;
- opponent-card-observation behavior;
- parser event classes;
- ActionLogRow shape;
- parser state final reconciliation;
- match/game identity;
- deduplication;
- diagnostics behavior;
- drift report behavior;
- golden replay behavior;
- feature-equity behavior;
- evidence-ledger behavior;
- analytics ingest behavior;
- runtime status files or schema;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- output transport;
- failed posts;
- workbook exports;
- SQLite/local app behavior;
- analytics truth;
- AI/model-provider behavior;
- coaching behavior;
- CI gates;
- merge readiness;
- deploy readiness;
- production behavior;
- final integration policy.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_gameplay_event_ordering_behavior_uplift.md`

Future Codex C files authorized only if implementation is selected:

- `tests/test_gameplay_actions.py`, for a dedicated reduced
  event-ordering/action-sequence preservation test, if existing tests are not
  enough;
- focused parser/router/GRE/golden-replay tests only if Codex C chooses a
  narrower route that needs them;
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- `tests/test_corpus_parity_report.py`;
- `docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_behavior_uplift_comparison.md`;
- `docs/contract_test_reports/parser_corpus_gameplay_event_ordering_behavior_uplift.md`.

Files Codex C may inspect but must not change unless the implementation
contract is looped back:

- `src/mythic_edge_parser/router.py`;
- `src/mythic_edge_parser/parsers/gre/__init__.py`;
- `src/mythic_edge_parser/parsers/gre/game_state.py`;
- `src/mythic_edge_parser/app/gameplay_actions.py`;
- `src/mythic_edge_parser/app/golden_replay.py`;
- `src/mythic_edge_parser/app/parser_diagnostics.py`;
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`;
- adjacent contracts, handoffs, and reports.

Not owned by this contract:

- parser semantics;
- router semantics;
- GRE or GameState parser behavior;
- gameplay-action extraction behavior;
- opponent-card-observation behavior;
- private evidence;
- external corpus contents;
- workbook/webhook/App Script/Sheets/analytics/AI/coaching surfaces.

## Public Interface

No runtime public API is added by Codex B.

Future Codex C may add committed synthetic tests and corpus metadata that make
the corpus parity public report show `gameplay_stress.event_ordering` as a
reduced synthetic behavior-ready row. The intended eventual corpus row shape
is:

```yaml
scenario_family: "gameplay_stress.event_ordering"
coverage_status: "covered_synthetic"
coverage_basis:
  - "parser_behavior_verified"
  - "fixture_metadata_only"
```

The existing report-only entry `gameplay_event_ordering_boundary_report_v1`
should remain as historical non-claim metadata unless Codex C has a strong
reason to route back for a replacement or migration contract. A new synthetic
evidence entry should be added rather than rewriting #412's boundary entry into
a behavior claim.

Recommended new manifest entry id:

```text
gameplay_event_ordering_synthetic_sequence_v1
```

Recommended new session id:

```text
gameplay_event_ordering_synthetic_sequence_v1
```

Recommended manifest claim families:

```yaml
parser_claim_families:
  - "synthetic_parser_observed_sequence_preservation"
  - "game_state_id_sequence_preservation"
  - "timestamp_context_sequence_preservation"
  - "gameplay_action_entry_order_preservation"
  - "event_ordering_synthetic_boundary"
  - "complete_event_sequence_non_claim"
  - "causal_ordering_non_claim"
  - "hidden_action_non_claim"
  - "hidden_card_non_claim"
  - "action_absence_non_claim"
```

Recommended manifest paths, adjusted only if Codex C selects a different
focused test route:

```yaml
paths:
  gameplay_actions_test: "tests/test_gameplay_actions.py"
  corpus_parity_test: "tests/test_corpus_parity_report.py"
```

## Minimum Parser-Owned Evidence

Future uplift requires a dedicated reduced sequence assertion. Codex C must not
rely on #496 action-attribution evidence alone.

### Required Sequence Evidence

Required:

- one Mythic Edge-owned synthetic sequence with at least three ordered
  observations;
- at least two resulting gameplay-action entries, or an explicitly justified
  equivalent parser-emitted event sequence if Codex C chooses a parser/router
  route;
- explicit expected order by input step, `game_state_id`, timestamp context, or
  a clearly named synthetic sequence index;
- assertion that output order matches the expected reduced sequence;
- assertion that the test uses existing behavior only;
- assertion that raw action labels, parser event identities, or GameState
  fields make the sequence observable from parser-owned evidence; and
- no private logs, external corpus contents, local runtime artifacts, or live
  checks.

Allowed:

- synthetic `GameStateEvent` objects in focused tests;
- synthetic timestamps and synthetic raw metadata bytes;
- synthetic local/opponent actor context only when already supported by current
  tests;
- existing `gameplay_actions.py` runtime-artifact writes redirected to a test
  temp directory;
- a golden replay fixture only if Codex C can keep it small, synthetic, and
  parser-behavior-only.

Not sufficient:

- #496 action-attribution assertions by themselves;
- generic parser timestamp extraction;
- router dispatch order by itself;
- GRE message order by itself;
- gameplay-action row order without a dedicated event-ordering expectation;
- diagnostics event counts;
- golden replay event-kind summaries without a dedicated expected sequence;
- feature-equity count ratchets;
- evidence-ledger provenance descriptions;
- analytics ingest ordering;
- corpus metadata assertions with no parser test evidence.

### Required Non-Claims

Every manifest/session-ledger entry and implementation handoff must preserve
these non-claims:

- no complete event-sequence truth;
- no causal ordering truth;
- no hidden-action truth;
- no hidden-card truth;
- no opponent-intent truth;
- no action absence truth;
- no player-mistake truth;
- no best-line truth;
- no gameplay advice;
- no analytics truth;
- no AI truth;
- no coaching truth;
- no private smoke success;
- no release readiness;
- no production behavior;
- no #388/#381 activation;
- no tracker completion;
- no full corpus parity.

## Behavior-Uplift Packet

This row's reusable packet is:

```yaml
scenario_family: "gameplay_stress.event_ordering"
current_status: "covered_report_only"
current_basis:
  - "fixture_metadata_only"
target_status_if_successful: "covered_synthetic"
parser_behavior_verified_may_be_added: true
evidence_type: "synthetic"
fixture_or_test_route:
  preferred: "focused synthetic gameplay-action/parser sequence test"
  optional: "small synthetic golden replay only if needed"
fixture_golden_replay_changes:
  allowed:
    - "dedicated synthetic fixture or focused test data if required"
  forbidden:
    - "private Player.log or external corpus contents"
    - "fixture that claims complete event chronology"
manifest_session_ledger_changes:
  allowed:
    - "add gameplay_event_ordering_synthetic_sequence_v1"
    - "preserve gameplay_event_ordering_boundary_report_v1 as report-only history"
  forbidden:
    - "rewrite #412 boundary entry into behavior evidence"
    - "promote unrelated rows"
parser_behavior_changes_allowed: false
private_external_inputs_forbidden: true
required_non_claims:
  - "complete_event_sequence_truth"
  - "causal_ordering_truth"
  - "hidden_action_truth"
  - "hidden_card_truth"
  - "opponent_intent_truth"
  - "player_mistake_truth"
  - "best_line_truth"
  - "gameplay_advice"
  - "analytics_truth"
  - "ai_truth"
  - "coaching_truth"
  - "release_readiness"
  - "production_behavior"
focused_validation_commands:
  - "PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py tests/test_corpus_parity_report.py"
  - "PYTHONPATH=src python3 -m pytest -q focused parser/router/GRE/golden-replay tests if touched"
stop_conditions_for_issue_388_381_activation:
  - "do not activate #388/#381"
  - "do not mark pipeline_activation_ready_for_issue_388 true"
  - "do not close tracker #158"
```

This packet is a pattern note for future behavior-uplift rows, but this
contract applies it only to `gameplay_stress.event_ordering`.

## Compatibility Expectations

- Existing #412 report-only boundary must remain readable and testable.
- Existing #496 action-attribution synthetic entry must remain scoped to action
  facts and must keep an explicit event-ordering non-claim.
- `drift_debug.missing_message_type` must remain unchanged unless a separate
  contract authorizes work on that row.
- Readiness metrics may count this row as parser-behavior-ready only after the
  family's winning status is `covered_synthetic` and its coverage basis
  includes `parser_behavior_verified`.
- `pipeline_activation_ready_for_issue_388` must remain false unless every
  separately required readiness gate is satisfied by later contracts.
- Public reports must continue to sanitize private paths, raw logs, secrets,
  runtime artifacts, failed posts, workbook exports, private reports, and
  external corpus contents.

## Validation Obligations For Codex C

Codex C must produce:

- a comparison handoff at
  `docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_behavior_uplift_comparison.md`;
- a contract-test report at
  `docs/contract_test_reports/parser_corpus_gameplay_event_ordering_behavior_uplift.md`;
- focused test evidence for the reduced event-ordering packet;
- corpus metadata tests proving the intended manifest and session-ledger
  changes;
- explicit evidence that #496 action-attribution is not reinterpreted as
  event-ordering support;
- explicit evidence that `drift_debug.missing_message_type` is unchanged; and
- clean git status with no private/generated artifacts.

Minimum validation commands:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m pytest -q tests/test_router.py tests/test_gre_game_state_parser.py tests/test_golden_replay_harness.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
python3 tools/select_validation.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

Codex C may narrow the parser/router/GRE/golden-replay pytest command to only
touched focused tests if the implementation uses `tests/test_gameplay_actions.py`
and corpus metadata only. Codex C must explain any narrowed validation in the
handoff.

## Acceptance Criteria

Future implementation is acceptable only if:

- `gameplay_stress.event_ordering` has a new synthetic behavior entry;
- the row's winning status becomes `covered_synthetic` only with
  `parser_behavior_verified`;
- the reduced sequence packet has at least one dedicated focused test;
- the old report-only boundary entry remains report-only or is migrated only
  through an explicit contract loopback;
- all required non-claims are present in metadata, handoff, and report;
- #496 action-attribution remains scoped to action facts;
- `drift_debug.missing_message_type` remains unchanged;
- #388/#381 remain inactive; and
- no protected parser/runtime/workbook/webhook/App Script/analytics/AI/coaching
  surfaces are changed.

Route back to Codex B or Codex A if:

- existing behavior cannot preserve the reduced sequence without parser code
  changes;
- the only available evidence is #496 action-attribution;
- a fixture would require private or external raw logs;
- the implementation would need to claim complete chronology, causality,
  hidden actions, hidden cards, opponent intent, or action absence; or
- validation changes would touch protected surfaces.

## Recommended Next Role

Codex C: Module Implementer.

Codex C should implement metadata/test/docs only. It should not implement
parser behavior changes.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #498.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/498

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/496

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/497

Previous merge commit:
6ab8950e74f162af93b3e8ae0c950244d69cbcf1

Base branch:
main

Contract:
docs/contracts/parser_corpus_gameplay_event_ordering_behavior_uplift.md

Goal:
Implement the smallest metadata/test/docs change needed to satisfy the
event-ordering behavior uplift contract for `gameplay_stress.event_ordering`.

Required implementation boundary:
- Add a dedicated reduced synthetic event-ordering sequence packet.
- Prefer a focused synthetic gameplay-action/parser sequence test proving
  parser-observed sequence preservation through existing behavior.
- Add or update corpus manifest/session-ledger metadata so the row may move
  from `covered_report_only` to `covered_synthetic` only with
  `parser_behavior_verified`.
- Preserve `gameplay_event_ordering_boundary_report_v1` as report-only
  historical boundary metadata unless you route back for a contract loopback.
- Do not use #496 action-attribution evidence alone as event-ordering support.
- Do not change parser behavior.

Expected files:
- tests/test_gameplay_actions.py, or another focused parser/router/GRE/golden
  replay test only if the contract route requires it
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_behavior_uplift_comparison.md
- docs/contract_test_reports/parser_corpus_gameplay_event_ordering_behavior_uplift.md

Do not:
- Activate #388 / #381.
- Close #158, #388, #434, or #498.
- Promote blocked or unrelated report-only rows.
- Change parser behavior, router behavior, GRE parser behavior, GameState
  parser behavior, gameplay-action extraction, opponent-card observations,
  diagnostics behavior, golden replay behavior, feature-equity behavior,
  evidence-ledger behavior, analytics behavior, workbook schema, webhook
  payload shape, Apps Script behavior, Google Sheets sync, output transport,
  CI gates, merge readiness, deploy readiness, production behavior, or final
  integration policy.
- Run private Player.log, UTC_Log, live MTGA, gameplay, network, or private
  smoke checks.
- Import, copy, mirror, summarize, or commit Manasight raw logs, compressed
  corpus files, parser source, external corpus contents, private logs,
  generated/runtime artifacts, workbook exports, secrets, tokens, API keys,
  webhook URLs, decklists, card choices, screenshots, private strategy notes,
  or private reports.
- Claim complete event-sequence truth, causal-ordering truth, hidden-action
  truth, hidden-card truth, opponent-intent truth, player-mistake truth,
  best-line truth, gameplay advice, analytics truth, AI truth, coaching truth,
  release readiness, production behavior, tracker completion, or full corpus
  parity.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py tests/test_corpus_parity_report.py
- PYTHONPATH=src python3 -m pytest -q focused parser/router/GRE/golden-replay tests if touched
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- run path-scoped secret/protected-surface checks for changed files
- git diff --check

End with:
- files changed
- reduced event-ordering evidence added
- validation run
- remaining risks/open questions
- recommended next role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/498"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/496"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/497"
  previous_merge_commit: "6ab8950e74f162af93b3e8ae0c950244d69cbcf1"
  completed_thread: "B"
  next_thread: "C"
  base_branch: "main"
  selected_family: "gameplay_stress.event_ordering"
  prior_status: "covered_report_only"
  authorized_target_status: "covered_synthetic"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  target_contract: "docs/contracts/parser_corpus_gameplay_event_ordering_behavior_uplift.md"
  expected_implementation_handoff: "docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_behavior_uplift_comparison.md"
  expected_contract_test_report: "docs/contract_test_reports/parser_corpus_gameplay_event_ordering_behavior_uplift.md"
  verdict: "reduced_synthetic_event_ordering_behavior_uplift_authorized"
  risk_tier: "High"
  stop_conditions:
    - "Do not activate #388 / #381."
    - "Do not close #158, #388, #434, or #498."
    - "Do not promote blocked or unrelated report-only rows."
    - "Do not claim event-ordering support from #496 action-attribution evidence alone."
    - "Do not claim complete event-sequence truth, causal-ordering truth, hidden-action truth, hidden-card truth, analytics truth, AI truth, coaching truth, release readiness, production behavior, tracker completion, or full corpus parity."
    - "Do not change parser behavior, router behavior, GRE parser behavior, GameState parser behavior, gameplay-action extraction, workbook schema, webhook payload shape, Apps Script behavior, analytics truth, AI truth, coaching truth, CI gates, deploy policy, production behavior, or final integration policy."
```
