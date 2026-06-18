# Parser Corpus Gameplay Event-Ordering Coverage Contract

## Module

Gameplay event-ordering corpus evidence boundary for the parser corpus parity
report.

Plain English: this slice lets Mythic Edge account for exactly
`gameplay_stress.event_ordering` as report-only boundary metadata. It does not
add parser support, committed gameplay fixtures, synthetic gameplay fixtures,
complete event-sequence truth, causal truth, hidden-action inference,
hidden-card inference, opponent-intent inference, player-mistake labeling,
best-line truth, gameplay advice, analytics truth, AI truth, coaching truth,
release readiness, production behavior, or full Mythic Edge corpus parity.

This contract explicitly prevents Mythic Edge from treating generic parser
timestamps, router dispatch order, GRE message order, gameplay-action
extraction, action-attribution report-only coverage, opponent-card
observations, ActionLogRow surfaces, analytics ingest, diagnostics, golden
replay behavior, feature-equity behavior, evidence-ledger provenance, or
public taxonomy metadata as event-ordering stress coverage.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/412
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/410
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/411
- Previous merge commit:
  `ac2c6e448e5192590d2f7a932ecc6097114e4c8b`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-gameplay-event-ordering-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `ac2c6e448e5192590d2f7a932ecc6097114e4c8b`
- target_artifact:
  `docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_gameplay_event_ordering_coverage.md`
- risk_tier: High
- status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority:

- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md`
- `docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md`
- `docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md`
- `docs/contracts/parser_runner.md`
- `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`
- `docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`
- `docs/contracts/analytics_gameplay_action_ingest.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `tests/test_gameplay_actions.py`
- `tests/test_opponent_card_observations.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_parser_regressions.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, raw session payloads, hash lists,
  byte-size row lists, capture-date row lists, parser source, external corpus
  contents, private Player.log excerpts, private local logs, private smoke
  outputs, generated/private/runtime artifacts, workbook exports, SQLite files,
  credentials, tokens, API keys, webhook URLs, decklists, deck names, card
  choices, sideboard choices, private strategy notes, or private reports.

## Observed Current Behavior

Observed on `codex/parser-parity` at merge commit
`ac2c6e448e5192590d2f7a932ecc6097114e4c8b`:

- Issue #412 is open and tracker #158 remains open.
- Issue #410 is closed after PR #411 merged gameplay action-attribution
  report-only boundary coverage.
- The current corpus parity report remains `partial_coverage_map_ready`.
- Current report summary:
  - `total_scenario_families`: 45
  - `covered_committed`: 6
  - `covered_synthetic`: 14
  - `covered_report_only`: 9
  - `partial`: 3
  - `missing`: 7
  - `blocked_private_evidence`: 1
  - `blocked_external_boundary`: 5
- `gameplay_stress.action_attribution` is `covered_report_only` with
  `coverage_basis == ["fixture_metadata_only"]` and entry
  `gameplay_action_attribution_boundary_report_v1`.
- `gameplay_stress.event_ordering` is `missing`, has
  `coverage_basis == ["external_reference_only"]`, and has no Mythic Edge
  entries.
- `src/mythic_edge_parser/router.py` extracts per-entry timestamps, records
  timestamp anomalies, and dispatches to parser modules in configured order.
- GRE parsing can emit one or more events from a single log entry, including
  `GameState` and queued GameState events.
- `src/mythic_edge_parser/app/gameplay_actions.py` emits parser-owned
  gameplay-action entries from `GameState` evidence.
- Diagnostics, golden replay, and feature-equity tools route committed or
  local lines through the router and may report event counts, event-kind
  sequences, router stats, timestamp anomalies, or replay diffs.
- None of those surfaces currently owns a dedicated
  `gameplay_stress.event_ordering` coverage claim.

## Scope Decision

Implementation may proceed as report-only boundary coverage.

Codex B considered these paths:

1. Safe synthetic event-ordering coverage.
2. Report-only boundary coverage.
3. Evidence-prerequisite, deferred, blocked-private-evidence, or
   blocked-external-boundary status.
4. Leave the family plain `missing` with sharper documentation only.

Selected path: report-only boundary coverage for
`gameplay_stress.event_ordering` only.

Reasoning:

- Mythic Edge has real parser-owned ordering-adjacent surfaces: log line order,
  per-entry timestamps when available, router dispatch order, GRE message
  expansion order, GameState IDs, gameplay-action entry order, diagnostics
  event counts, golden replay event-kind sequences, and feature-equity corpus
  routing summaries.
- Those surfaces are useful context, but they do not prove a stress corpus
  scenario for event ordering. They do not guarantee complete event-sequence
  truth across all MTGA event families, causal ordering, hidden actions,
  hidden cards, opponent intent, why an action happened, player mistakes,
  best-line truth, or gameplay advice.
- A synthetic event-ordering fixture would need a future contract that defines
  a reduced expected-sequence model, allowed event families, fixture shape, and
  exactly which parser-owned order facts count as support.
- A private-evidence blocker would be too strong for V1 because future coverage
  could plausibly be Mythic Edge-owned synthetic or sanitized metadata.
- Leaving the row plain `missing` hides an important inspected boundary:
  existing parser/router/replay ordering context is intentionally not enough
  for an event-ordering stress support claim.

This decision records `gameplay_stress.event_ordering` as report-only boundary
metadata. It changes corpus parity metadata and tests only; it does not change
parser behavior, router behavior, gameplay-action extraction, diagnostics,
golden replay, feature-equity behavior, analytics ingest, runtime behavior, or
evidence-ledger behavior.

`gameplay_stress.action_attribution` must remain report-only boundary metadata
from issue #410. This issue must not upgrade, reinterpret, or broaden the #410
coverage row.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for
`gameplay_stress.event_ordering`. Parser modules own observed event
interpretation, timestamps, router dispatch, GRE message handling, annotations,
gameplay-action extraction, match/game identity, parser event classes, and
parser state behavior. Diagnostics, golden replay, feature-equity, evidence
ledger, and analytics ingest are downstream or review surfaces unless a
separate contract grants them a stronger role. Corpus parity artifacts own only
the coverage-status boundary and non-claims.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence, diagnostics/replay evidence, and
Quality / Governance evidence for context, but it is not a Parser behavior
module, router module, diagnostics module, golden replay module, feature-equity
module, gameplay-action extraction module, analytics-ingest module, AI module,
coaching module, release-readiness module, or production module.

## Truth Owner

Truth owner for `gameplay_stress.event_ordering` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owners for parser and downstream behavior referenced only as non-claim
context:

- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`

Truth boundary:

- Router and parser modules may say which events were emitted from each log
  entry and in what dispatch order current code produced them.
- Event metadata may carry observed timestamps when parseable.
- GRE/GameState parsing may preserve message IDs and payload order fields
  where current parser behavior already exposes them.
- Gameplay-action extraction may say which action entries were observed or
  derived from existing `GameState` evidence.
- Diagnostics, golden replay, and feature-equity reports may summarize
  parser/replay output for review.
- Corpus parity may say that Mythic Edge has an inspected report-only boundary
  for `gameplay_stress.event_ordering`.
- Corpus parity must not infer complete event-sequence truth, causal truth,
  hidden actions, hidden cards, opponent intent, why an action happened,
  player mistakes, best-line truth, archetypes, decklists, gameplay advice,
  analytics truth, AI truth, coaching truth, release readiness, production
  behavior, or full corpus parity from existing timestamp/router/replay
  surfaces.

Coverage status is review metadata. It is not parser truth, event-ordering
truth, action-attribution truth, action-causality truth, diagnostics truth,
replay truth, analytics truth, AI truth, coaching truth, merge readiness,
deploy readiness, public/private release readiness, or tracker-completion
authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing parser/router/replay/diagnostics ordering-adjacent docs
  -> explicit event-ordering non-claim boundary metadata
  -> corpus parity row for gameplay_stress.event_ordering
```

Forbidden reverse flow:

- Corpus coverage status must not change parser behavior.
- Corpus metadata must not change router behavior, GRE dispatch, GameState
  parsing, gameplay-action extraction, opponent-card-observation behavior,
  parser event classes, ActionLogRow shape, diagnostics, golden replay,
  feature-equity, evidence-ledger behavior, analytics ingest, runtime
  artifacts, match/game identity, parser state final reconciliation, workbook
  output, analytics, AI, coaching, release policy, or production behavior.
- Corpus metadata must not turn generic parser timestamps, router dispatch
  order, gameplay-action rows, action-attribution report-only coverage,
  opponent-card-observation rows, ActionLogRow surfaces, diagnostics reports,
  golden replay reports, feature-equity reports, evidence-ledger provenance,
  analytics ingest, public taxonomy labels, local private artifacts, or private
  gameplay logs into event-ordering stress support.

Protected surfaces explicitly not touched:

- parser behavior
- router behavior
- GRE parser behavior
- GameState parser behavior
- gameplay-action extraction behavior
- opponent-card-observation behavior
- parser event classes
- ActionLogRow shape
- diagnostics report shape
- drift report behavior
- golden replay behavior
- feature-equity behavior
- evidence-ledger behavior
- analytics ingest behavior
- parser state final reconciliation
- match/game identity
- deduplication
- runtime status artifacts or schema
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- failed delivery artifacts
- workbook exports
- SQLite/local app behavior
- analytics truth
- AI truth
- coaching behavior
- OpenAI/model-provider behavior
- CI gates
- merge readiness
- deploy readiness
- production behavior
- final integration policy

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md`

Future implementation files owned by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_gameplay_event_ordering_coverage.md`

Referenced but not silently owned:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- `tests/test_gameplay_actions.py`
- `tests/test_opponent_card_observations.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_parser_regressions.py`

Codex C may edit `src/mythic_edge_parser/app/corpus_parity_report.py` only if
the existing report code cannot represent the contracted manifest/session
ledger metadata. Codex C must not edit parser, router, diagnostics, replay,
feature-equity, runtime, analytics, workbook, or local app modules unless it
returns to Codex B with a contract loopback.

## Public Interface

This contract covers corpus parity metadata only.

Authorized scenario family:

| Scenario family | Authorized status | Meaning |
| --- | --- | --- |
| `gameplay_stress.event_ordering` | `covered_report_only` | The corpus report records that event-ordering coverage has an inspected non-claim boundary. |

Adjacent scenario family preserved:

| Scenario family | Required status in this issue | Meaning |
| --- | --- | --- |
| `gameplay_stress.action_attribution` | unchanged / `covered_report_only` | Action-attribution remains report-only boundary metadata from issue #410. |

Authorized manifest entry:

| Field | Required value |
| --- | --- |
| `entry_id` | `gameplay_event_ordering_boundary_report_v1` |
| `entry_type` | `session_ledger_entry` |
| `source_kind` | `committed_count_only_report` |
| `commit_status` | `committed` |
| `privacy_class` | `committed_count_only` |
| `sanitization_status` | `not_applicable_count_only` |
| `scenario_families` | `["gameplay_stress.event_ordering"]` |
| `parser_event_families` | `[]` |
| `coverage_status` | `covered_report_only` |
| `coverage_basis` | `["fixture_metadata_only"]` |

Required `parser_claim_families`:

- `gameplay_event_ordering_boundary_report`
- `parser_timestamps_not_complete_ordering_truth`
- `router_dispatch_order_not_stress_coverage`
- `gameplay_action_order_not_event_sequence_truth`
- `action_attribution_not_event_ordering_truth`
- `diagnostics_replay_reports_not_parser_truth`
- `hidden_action_inference_non_claim`

Required manifest notes or review text must state that the entry is report-only
boundary metadata and does not claim:

- event-ordering parser stress support
- complete event-sequence truth
- causal ordering truth
- hidden actions
- hidden cards
- opponent intent
- why an action happened
- action-attribution support beyond #410 report-only metadata
- player mistakes
- best-line truth
- archetype classification
- decklist completion
- gameplay advice
- analytics truth
- AI truth
- coaching truth
- release readiness
- production behavior
- full Mythic Edge corpus parity

Authorized session ledger entry:

| Field | Required value |
| --- | --- |
| `session_id` | `gameplay_event_ordering_boundary_report_v1` |
| `authorized_by_contract` | `docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md` |
| `scenario_families` | `["gameplay_stress.event_ordering"]` |
| `format_family` | `gameplay_stress` |
| `match_shape` | `gameplay_event_ordering_boundary_report_only` |
| `record_summary` | `committed_gameplay_event_ordering_boundary_metadata_only` |

Required session-ledger `parser_coverage` facts:

- `event_families` must be `{}`.
- `unknown_entries` must be `0`.
- `truncation_count` must be `0`.
- `timestamp_reference_entries` must be `1`.
- `router_dispatch_reference_entries` must be `1`.
- `game_state_reference_entries` must be `1`.
- `gameplay_action_reference_entries` must be `1`.
- `diagnostics_reference_entries` must be `1`.
- `golden_replay_reference_entries` must be `1`.
- `feature_equity_reference_entries` must be `1`.
- `dedicated_event_ordering_fixtures` must be `0`.
- `dedicated_action_attribution_fixtures` must be `0`.
- `hidden_action_claims` must be `0`.
- `causal_ordering_claims` must be `0`.
- `complete_sequence_claims` must be `0`.

Required session-ledger game row summary:

- `game_rows.count` must be `0`.
- `game_rows.result_shape` must be `not_applicable`.

Required redaction and privacy facts:

- no raw/private Player.log excerpts
- no external corpus payloads
- no private local action artifacts
- no private smoke outputs
- no generated/private/runtime artifacts
- no decklists
- no deck names
- no card choices
- no sideboard choices
- no private strategy notes
- no credentials, tokens, API keys, or webhook URLs

Forbidden public-interface changes:

- no new parser events
- no parser route changes
- no router behavior changes
- no GRE/GameState parser behavior changes
- no gameplay-action extraction behavior changes
- no opponent-card-observation behavior changes
- no ActionLogRow shape changes
- no analytics ingest behavior changes
- no diagnostics, golden replay, feature-equity, evidence-ledger, runtime
  status, workbook, webhook, Apps Script, Google Sheets, AI, or coaching
  interface changes

## Inputs

Allowed inputs:

- Existing committed corpus parity manifest and session ledger.
- Existing committed contracts and contract-test reports for corpus parity,
  event-ordering taxonomy mapping, action-attribution report-only coverage,
  parser runner behavior, gameplay-action provenance, diagnostics, golden
  replay, feature-equity, and analytics ingest.
- Existing focused parser, diagnostics, replay, feature-equity, and analytics
  tests for adjacent ordering context, used only as non-claim context.
- Public Manasight metadata only as category-level reference context through
  the already merged taxonomy audit or public metadata pages.

Forbidden inputs:

- Manasight raw logs, `.log.gz` files, compressed corpus files, raw session
  payloads, external corpus contents, hash lists, byte-size row lists, or
  capture-date row lists.
- Private Player.log excerpts, private local logs, private action artifacts,
  private smoke outputs, generated/private/runtime artifacts, SQLite files,
  workbook exports, failed posts, secrets, credentials, tokens, API keys, or
  webhook URLs.
- Decklists, deck names, card choices, sideboard choices, private strategy
  notes, private reports, opponent identifiers, account identifiers, local
  paths, machine paths, or private match context.
- Model-provider output or AI interpretation.

## Outputs

Authorized outputs for Codex C:

- One corpus manifest entry for `gameplay_stress.event_ordering`.
- One session-ledger entry with count-only, report-only boundary metadata.
- Focused tests proving the corpus report renders the row as
  `covered_report_only`, preserves the required non-claims, and keeps
  `gameplay_stress.action_attribution` unchanged as report-only metadata.
- An implementation handoff and contract test report.

Forbidden outputs:

- committed raw or synthetic gameplay log slices
- committed event-ordering fixtures
- committed action-attribution fixtures
- committed private action artifacts
- new parser event classes
- new parser route behavior
- new router behavior
- new gameplay-action extraction behavior
- new opponent-card-observation behavior
- new ActionLogRow fields
- new diagnostics/golden replay/feature-equity report behavior
- new runtime files
- new workbook/export/webhook/App Script fields
- new analytics tables/views/ingest behavior
- AI/model-provider outputs
- release-readiness or deploy-readiness verdicts

## Invariants

- `gameplay_stress.event_ordering` may become only `covered_report_only` in
  this slice.
- `coverage_basis` must remain exactly `["fixture_metadata_only"]` unless a
  future contract authorizes a real fixture path.
- `parser_event_families` must remain empty for the authorized entry.
- `gameplay_stress.action_attribution` must remain report-only and must not be
  upgraded or reinterpreted in this issue.
- Parser timestamps are not complete event-ordering truth.
- Router dispatch order is not event-ordering stress coverage.
- Gameplay-action order is not complete event-sequence truth.
- Diagnostics, golden replay, and feature-equity reports are not parser truth.
- Public taxonomy metadata is not parser support evidence.
- Corpus parity status must not become parser truth, event-ordering truth,
  action-attribution truth, causal truth, diagnostics truth, replay truth,
  analytics truth, AI truth, coaching truth, merge readiness, deploy readiness,
  release readiness, production behavior, or tracker-completion authority.

## Error Behavior

Malformed manifest or session-ledger data must fail existing corpus parity
validation tests. Codex C must not add permissive parsing that silently accepts
ambiguous coverage claims.

If implementation discovers that the existing corpus report cannot represent
the contracted report-only boundary without changing report code, Codex C may
make the smallest corpus-report-only code change and document it in the
implementation handoff. That change must not affect parser, router,
diagnostics, replay, feature-equity, analytics, runtime, workbook, or local app
behavior.

If implementation discovers that event-ordering coverage needs parser
behavior, router behavior, diagnostics behavior, a reduced expected-sequence
model, private evidence, or action-attribution movement, Codex C must stop and
route back to Codex B. This contract does not authorize parser behavior
changes or synthetic fixture promotion.

If private evidence would be needed to make a stronger claim, the row must
remain report-only and the private evidence must stay out of the repo and out
of GitHub issue comments.

## Side Effects

Allowed future Codex C side effects:

- Edit committed corpus parity metadata.
- Edit focused corpus parity tests.
- Write implementation handoff and contract test report docs.

Forbidden side effects:

- opening or closing issues
- opening a PR unless separately asked
- staging or committing unless separately asked
- changing parser behavior
- changing router behavior
- changing diagnostics, replay, feature-equity, or analytics behavior
- creating runtime/generated/private artifacts
- committing local logs or raw private evidence
- changing CI gates, merge policy, deploy policy, or production behavior

## Dependency Order

Codex C should make changes in this order:

1. Confirm branch and base state against `origin/codex/parser-parity`.
2. Compare current manifest/session-ledger/report behavior against this
   contract.
3. Add the manifest entry.
4. Add the session-ledger entry.
5. Add focused corpus parity tests for status, claim families, non-claims,
   action-attribution preservation, and summary counts.
6. Run focused validation.
7. Write the implementation handoff and contract test report.
8. Run docs/protected-surface/secret checks on the changed files.

## Compatibility

Compatibility expectations:

- Existing covered families and summary counts must remain stable except for
  the one status move authorized here.
- Current report semantics for `covered_committed`, `covered_synthetic`,
  `covered_report_only`, `partial`, `missing`, `blocked_private_evidence`, and
  `blocked_external_boundary` must remain compatible.
- Existing parser runner, gameplay-action, opponent-card-observation,
  action-attribution, diagnostics, golden replay, feature-equity,
  evidence-ledger, and analytics-ingest contracts must not be reinterpreted.
- `gameplay_stress.action_attribution` must remain `covered_report_only`
  unless the current base branch already contains separately merged authorized
  movement.
- No report consumer may treat this row as event-ordering parser support.

Expected summary-count delta after Codex C:

- `covered_report_only` increases by `1`.
- `missing` decreases by `1`.
- Other status counts remain unchanged unless the current base branch already
  contains unrelated merged changes.

## Tests Required

Codex C must run or justify not running:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_coverage_comparison.md docs/contract_test_reports/parser_corpus_gameplay_event_ordering_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_coverage_comparison.md docs/contract_test_reports/parser_corpus_gameplay_event_ordering_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Codex C should also inspect, but should not need to run unless it edits
adjacent code:

- `tests/test_parser_regressions.py`
- `tests/test_gameplay_actions.py`
- `tests/test_opponent_card_observations.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- focused diagnostics, golden replay, and feature-equity tests

## Acceptance Criteria

- `docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md` exists
  and records the report-only boundary.
- Codex C can implement the contract with corpus metadata/tests/docs only.
- `gameplay_stress.event_ordering` is represented as `covered_report_only`,
  not `covered_synthetic`.
- `gameplay_stress.action_attribution` remains report-only and is not upgraded.
- The manifest and session ledger preserve explicit non-claims for complete
  event-sequence truth, causal ordering, hidden actions, hidden cards, opponent
  intent, player mistakes, best-line truth, archetype classification,
  decklists, gameplay advice, analytics truth, AI truth, coaching truth,
  release readiness, production behavior, and full corpus parity.
- No parser behavior, router behavior, diagnostics behavior, replay behavior,
  feature-equity behavior, analytics behavior, runtime behavior, or protected
  surface changes are authorized.
- No raw/private/external corpus contents or private action artifacts are
  committed.

## Unknowns

- No committed Mythic Edge-owned fixture currently proves an event-ordering
  stress scenario.
- The reduced expected-sequence model for future synthetic event-ordering
  coverage remains undefined.
- It remains unknown whether future event-ordering coverage should be scoped by
  log line order, timestamp order, GRE message order, GameState ID order,
  gameplay-action order, diagnostics/golden replay event-kind sequences, or a
  smaller evidence model.
- It remains unknown whether future coverage should pair with action
  attribution or remain independent.

## Suspected Gaps

- Corpus parity can currently express that the family has been inspected, but
  not that Mythic Edge has dedicated event-ordering stress support.
- The phrase "event ordering" is easy to overread as complete causal sequence
  reconstruction.
- Future coverage will likely need a smaller expected-sequence schema before
  safe synthetic fixtures can be committed.
- Diagnostics, golden replay, and feature-equity tools may be useful evidence
  surfaces later, but they must not become parser truth or coverage truth by
  implication.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #412, gameplay event-ordering corpus coverage, under tracker #158.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/412

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md

Goal:
Implement the smallest corpus metadata/test/docs package needed to satisfy the contract. This is report-only boundary coverage for `gameplay_stress.event_ordering`, not parser support, not synthetic gameplay coverage, and not an upgrade to action-attribution coverage.

Expected files:
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_coverage_comparison.md
- docs/contract_test_reports/parser_corpus_gameplay_event_ordering_coverage.md

Required behavior:
- Add exactly one report-only manifest entry for `gameplay_stress.event_ordering`.
- Add exactly one count-only session-ledger entry.
- Keep `coverage_status` as `covered_report_only`.
- Keep `coverage_basis` as `["fixture_metadata_only"]`.
- Keep `parser_event_families` empty.
- Keep `gameplay_stress.action_attribution` unchanged as report-only boundary metadata.
- Preserve explicit non-claims for event-ordering parser stress support, complete event-sequence truth, causal ordering, hidden actions, hidden cards, opponent intent, action-attribution support beyond #410, player mistakes, best-line truth, archetype classification, decklists, gameplay advice, analytics truth, AI truth, coaching truth, release readiness, production behavior, and full corpus parity.
- Do not change parser behavior or protected surfaces.

Do not:
- Target main directly.
- Close tracker #158.
- Close issue #412.
- Claim full Mythic Edge corpus parity.
- Promote this family to covered_synthetic without contract loopback.
- Upgrade or reinterpret `gameplay_stress.action_attribution` without contract loopback.
- Import, copy, mirror, or commit Manasight raw logs, external corpus contents, private Player.log excerpts, private local logs, private smoke outputs, generated/private/runtime artifacts, workbook exports, SQLite files, credentials, tokens, API keys, webhook URLs, decklists, deck names, card choices, sideboard choices, private strategy notes, or private reports.
- Change parser behavior, router behavior, GRE/GameState parser behavior, gameplay-action extraction behavior, opponent-card-observation behavior, parser event classes, ActionLogRow shape, diagnostics report shape, drift report behavior, golden replay behavior, feature-equity behavior, evidence-ledger behavior, parser state final reconciliation, match/game identity, deduplication, runtime status, analytics ingest, workbook, webhook, Apps Script, Google Sheets sync, output transport, analytics truth, AI/OpenAI, coaching, CI gates, merge policy, deploy policy, or production behavior.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- printf '%s\n' docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_coverage_comparison.md docs/contract_test_reports/parser_corpus_gameplay_event_ordering_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
- printf '%s\n' docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_coverage_comparison.md docs/contract_test_reports/parser_corpus_gameplay_event_ordering_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
- python3 -m ruff check src tests tools
- git diff --check

End with:
- implementation summary
- files changed
- validation results
- remaining risks
- recommended next role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/412"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/410"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/411"
  previous_merge_commit: "ac2c6e448e5192590d2f7a932ecc6097114e4c8b"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_gameplay_event_ordering_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_gameplay_event_ordering_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_gameplay_event_ordering_coverage.md"
  verdict: "contract_ready_for_report_only_boundary_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-gameplay-event-ordering-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "changed-file secret/protected-surface checks"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #158."
    - "Do not close issue #412."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not promote gameplay_stress.event_ordering to covered_synthetic without contract loopback."
    - "Do not upgrade or reinterpret gameplay_stress.action_attribution without contract loopback."
    - "Do not claim event-ordering support from generic parser timestamps, router dispatch order, gameplay-action extraction, action-attribution report-only coverage, opponent-card observations, ActionLogRow surfaces, analytics ingest, diagnostics, golden replay, feature-equity, evidence-ledger provenance, or public taxonomy evidence alone."
    - "Do not infer hidden actions, hidden cards, causal intent, complete event ordering beyond parser-owned evidence, player mistakes, archetypes, decklists, gameplay advice, analytics truth, AI truth, coaching truth, release readiness, or production behavior."
    - "Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, private smoke outputs, generated/private/runtime artifacts, workbook exports, SQLite files, decklists, deck names, card choices, sideboard choices, private strategy notes, private reports, or secrets."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/analytics/AI/production surfaces without a new explicit contract."
```
