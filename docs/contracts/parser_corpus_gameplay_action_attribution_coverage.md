# Parser Corpus Gameplay Action-Attribution Coverage Contract

## Module

Gameplay action-attribution corpus evidence boundary for the parser corpus
parity report.

Plain English: this slice lets Mythic Edge account for exactly
`gameplay_stress.action_attribution` as report-only boundary metadata. It does
not add parser support, committed gameplay fixtures, synthetic gameplay
fixtures, action-causality inference, hidden-action inference, event-ordering
coverage, player-mistake labeling, gameplay advice, analytics truth, AI truth,
coaching truth, release readiness, production behavior, or full Mythic Edge
corpus parity.

This contract explicitly prevents Mythic Edge from treating generic
gameplay-action extraction, opponent-card observations, ActionLogRow surfaces,
analytics gameplay-action ingest, evidence-ledger provenance, public taxonomy
metadata, or local/private action artifacts as action-attribution stress
coverage.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/410
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/408
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/409
- Previous merge commit:
  `574cd23d046d19fb64266d079d1d6173d23f7cf4`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-gameplay-action-attribution-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `574cd23d046d19fb64266d079d1d6173d23f7cf4`
- target_artifact:
  `docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md`
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
- `docs/contracts/parser_corpus_companion_large_deck_coverage.md`
- `docs/contract_test_reports/parser_corpus_companion_large_deck_coverage.md`
- `docs/implementation_handoffs/parser_corpus_companion_large_deck_coverage_comparison.md`
- `docs/contracts/player_log_evidence_ledger_tier5_card_identity.md`
- `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`
- `docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`
- `docs/contracts/parser_opponent_card_observations.md`
- `docs/contracts/analytics_gameplay_action_ingest.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/card_performance.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/state.py`
- `tests/test_gameplay_actions.py`
- `tests/test_opponent_card_observations.py`
- `tests/test_analytics_gameplay_action_ingest.py`

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
`574cd23d046d19fb64266d079d1d6173d23f7cf4`:

- Issue #410 is open and tracker #158 remains open.
- Issue #408 is closed after PR #409 merged companion / large-deck report-only
  coverage.
- The current corpus parity report remains `partial_coverage_map_ready`.
- Current report summary:
  - `total_scenario_families`: 45
  - `covered_committed`: 6
  - `covered_synthetic`: 14
  - `covered_report_only`: 8
  - `partial`: 3
  - `missing`: 8
  - `blocked_private_evidence`: 1
  - `blocked_external_boundary`: 5
- `gameplay_stress.action_attribution` is `missing`, has
  `coverage_basis == ["external_reference_only"]`, and has no Mythic Edge
  entries.
- `gameplay_stress.event_ordering` is also `missing`, has
  `coverage_basis == ["external_reference_only"]`, and has no Mythic Edge
  entries.
- The Manasight taxonomy audit maps action attribution and event ordering
  together, but marks the action-attribution family as
  `needs_parser_behavior_before_corpus_claim`.
- `src/mythic_edge_parser/app/gameplay_actions.py` already emits
  parser-owned gameplay-action entries from `GameState` evidence.
- `src/mythic_edge_parser/app/opponent_card_observations.py` derives visible
  opponent-card observations from gameplay-action entries.
- `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`
  documents broad gameplay-action provenance, and
  `docs/contracts/analytics_gameplay_action_ingest.md` documents analytics
  storage of parser-normalized gameplay actions.

## Scope Decision

Implementation may proceed as report-only boundary coverage.

Codex B considered these paths:

1. Safe synthetic action-attribution coverage.
2. Report-only boundary coverage.
3. Evidence-prerequisite, deferred, blocked-private-evidence, or
   blocked-external-boundary status.
4. Leave the family plain `missing` with sharper documentation only.

Selected path: report-only boundary coverage for
`gameplay_stress.action_attribution` only.

Reasoning:

- Mythic Edge has real parser-owned gameplay-action extraction, opponent-card
  observation, evidence-ledger provenance, and analytics ingest surfaces.
- Those surfaces can describe bounded observed action facts, actor relation,
  card identity context, zone movement, annotation context, visibility labels,
  degradation, confidence, and analytics storage.
- Those surfaces do not prove a stress corpus scenario for action attribution:
  they do not guarantee causal action truth, hidden choices, hidden cards,
  opponent intent, why an action happened, event ordering beyond parser-owned
  evidence, player mistakes, strategic correctness, or best-line truth.
- A synthetic gameplay-action attribution fixture would need a future contract
  that defines a reduced expected-facts model and proves exactly which
  parser-owned facts count as attribution support.
- A private-evidence blocker would be too strong for V1 because future coverage
  could plausibly be Mythic Edge-owned synthetic or sanitized metadata.
- Leaving the row plain `missing` hides an important inspected boundary:
  existing gameplay-action infrastructure is intentionally not enough for a
  stress coverage claim.

This decision records `gameplay_stress.action_attribution` as report-only
boundary metadata. It changes corpus parity metadata and tests only; it does
not change gameplay-action extraction, parser behavior, analytics ingest, or
runtime behavior.

`gameplay_stress.event_ordering` must remain unchanged in this issue. Event
ordering needs its own child issue unless a later contract explicitly
authorizes paired movement.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for
`gameplay_stress.action_attribution`. Parser modules own observed GameState
interpretation, gameplay-action extraction, actor relation, card identity,
opponent-card observation, match/game identity, and parser state behavior.
Analytics ingest owns only downstream storage of parser-normalized facts.
Corpus parity artifacts own only the coverage-status boundary and non-claims.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence, evidence-ledger provenance, and
Quality / Governance evidence for context, but it is not a Parser behavior
module, gameplay-action extraction module, opponent-card-observation module,
analytics-ingest module, diagnostics module, golden replay module, AI module,
coaching module, release-readiness module, or production module.

## Truth Owner

Truth owner for `gameplay_stress.action_attribution` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owners for parser and downstream behavior referenced only as non-claim
context:

- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/state.py`

Truth boundary:

- `gameplay_actions.py` may say which parser-owned gameplay-action entries
  were observed or derived from existing `GameState` evidence.
- `opponent_card_observations.py` may say which visible opponent-card
  observations were derived from gameplay-action entries.
- The evidence ledger may describe provenance, confidence, finality,
  degradation, and drift labels for gameplay-action facts.
- Analytics ingest may store parser-normalized gameplay-action facts.
- Corpus parity may say that Mythic Edge has an inspected report-only boundary
  for `gameplay_stress.action_attribution`.
- Corpus parity must not infer hidden actions, hidden cards, causal intent,
  event ordering beyond parser-owned evidence, why an action happened, player
  mistakes, archetypes, decklists, gameplay advice, analytics truth, AI truth,
  coaching truth, release readiness, production behavior, or full corpus parity
  from existing action surfaces.

Coverage status is review metadata. It is not parser truth,
gameplay-action truth, event-ordering truth, action-causality truth,
analytics truth, AI truth, coaching truth, merge readiness, deploy readiness,
public/private release readiness, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing gameplay-action / opponent-observation / evidence-ledger docs
  -> explicit action-attribution non-claim boundary metadata
  -> corpus parity row for gameplay_stress.action_attribution
```

Forbidden reverse flow:

- Corpus coverage status must not change parser behavior.
- Corpus metadata must not change gameplay-action extraction,
  opponent-card-observation behavior, parser event classes, ActionLogRow shape,
  analytics ingest, runtime artifacts, router dispatch, match/game identity,
  parser state final reconciliation, workbook output, analytics, AI, coaching,
  release policy, or production behavior.
- Corpus metadata must not turn generic gameplay-action rows,
  opponent-card-observation rows, ActionLogRow surfaces, evidence-ledger
  provenance, analytics ingest, public taxonomy labels, local private action
  artifacts, or private gameplay logs into action-attribution stress support.

Protected surfaces explicitly not touched:

- parser behavior
- gameplay-action extraction behavior
- opponent-card-observation behavior
- parser event classes
- ActionLogRow shape
- router semantics
- parser state final reconciliation
- match/game identity
- deduplication
- diagnostics report shape
- drift report behavior
- golden replay behavior
- feature-equity behavior
- evidence-ledger behavior
- analytics ingest behavior
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

- `docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md`

Future implementation files owned by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md`

Referenced but not silently owned:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/card_performance.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/state.py`
- `tests/test_gameplay_actions.py`
- `tests/test_opponent_card_observations.py`
- `tests/test_analytics_gameplay_action_ingest.py`

Codex C may edit `src/mythic_edge_parser/app/corpus_parity_report.py` only if
the existing report code cannot represent the contracted manifest/session
ledger metadata. Codex C must not edit parser, runtime, analytics, workbook, or
local app modules unless it returns to Codex B with a contract loopback.

## Public Interface

This contract covers corpus parity metadata only.

Authorized scenario family:

| Scenario family | Authorized status | Meaning |
| --- | --- | --- |
| `gameplay_stress.action_attribution` | `covered_report_only` | The corpus report records that action-attribution coverage has an inspected non-claim boundary. |

Adjacent scenario family preserved:

| Scenario family | Required status in this issue | Meaning |
| --- | --- | --- |
| `gameplay_stress.event_ordering` | unchanged / currently `missing` | Event-ordering coverage remains deferred to a separate child issue. |

Authorized manifest entry:

| Field | Required value |
| --- | --- |
| `entry_id` | `gameplay_action_attribution_boundary_report_v1` |
| `entry_type` | `session_ledger_entry` |
| `source_kind` | `committed_count_only_report` |
| `commit_status` | `committed` |
| `privacy_class` | `committed_count_only` |
| `sanitization_status` | `not_applicable_count_only` |
| `scenario_families` | `["gameplay_stress.action_attribution"]` |
| `parser_event_families` | `[]` |
| `coverage_status` | `covered_report_only` |
| `coverage_basis` | `["fixture_metadata_only"]` |

Required `parser_claim_families`:

- `gameplay_action_attribution_boundary_report`
- `gameplay_action_extraction_not_stress_coverage`
- `opponent_card_observation_not_action_attribution_truth`
- `action_log_row_not_causal_truth`
- `analytics_ingest_not_parser_truth`
- `event_ordering_not_claimed`
- `hidden_action_inference_non_claim`

Required manifest notes or review text must state that the entry is report-only
boundary metadata and does not claim:

- action-attribution parser stress support
- causal action truth
- hidden actions
- hidden cards
- opponent intent
- why an action happened
- event ordering
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
| `session_id` | `gameplay_action_attribution_boundary_report_v1` |
| `authorized_by_contract` | `docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md` |
| `scenario_families` | `["gameplay_stress.action_attribution"]` |
| `format_family` | `gameplay_stress` |
| `match_shape` | `gameplay_action_attribution_boundary_report_only` |
| `record_summary` | `committed_gameplay_action_attribution_boundary_metadata_only` |

Required session-ledger `parser_coverage` facts:

- `event_families` must be `{}`.
- `unknown_entries` must be `0`.
- `truncation_count` must be `0`.
- `gameplay_action_reference_entries` must be `1`.
- `opponent_card_observation_reference_entries` must be `1`.
- `action_log_reference_entries` must be `1`.
- `analytics_ingest_reference_entries` must be `1`.
- `dedicated_action_attribution_fixtures` must be `0`.
- `dedicated_event_ordering_fixtures` must be `0`.
- `hidden_action_claims` must be `0`.
- `causal_intent_claims` must be `0`.
- `event_ordering_claims` must be `0`.

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
- no gameplay-action extraction behavior changes
- no opponent-card-observation behavior changes
- no ActionLogRow shape changes
- no analytics ingest behavior changes
- no corpus parity report CLI behavior changes unless required by existing
  metadata rendering
- no diagnostics, golden replay, feature-equity, evidence-ledger, runtime
  status, workbook, webhook, Apps Script, Google Sheets, AI, or coaching
  interface changes

## Inputs

Allowed inputs:

- Existing committed corpus parity manifest and session ledger.
- Existing committed contracts and contract-test reports for corpus parity,
  action attribution taxonomy mapping, gameplay-action provenance,
  opponent-card-observation provenance, card identity provenance, and analytics
  gameplay-action ingest.
- Existing focused parser and analytics tests for adjacent gameplay-action
  evidence, used only as non-claim context.
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

- One corpus manifest entry for `gameplay_stress.action_attribution`.
- One session-ledger entry with count-only, report-only boundary metadata.
- Focused tests proving the corpus report renders the row as
  `covered_report_only`, preserves the required non-claims, and keeps
  `gameplay_stress.event_ordering` unchanged.
- An implementation handoff and contract test report.

Forbidden outputs:

- committed raw or synthetic gameplay log slices
- committed action-attribution fixtures
- committed event-ordering fixtures
- committed private action artifacts
- new parser event classes
- new parser route behavior
- new gameplay-action extraction behavior
- new opponent-card-observation behavior
- new ActionLogRow fields
- new runtime files
- new workbook/export/webhook/App Script fields
- new analytics tables/views/ingest behavior
- AI/model-provider outputs
- release-readiness or deploy-readiness verdicts

## Invariants

- `gameplay_stress.action_attribution` may become only
  `covered_report_only` in this slice.
- `coverage_basis` must remain exactly `["fixture_metadata_only"]` unless a
  future contract authorizes a real fixture path.
- `parser_event_families` must remain empty for the authorized entry.
- `gameplay_stress.event_ordering` must remain unchanged in this issue.
- Gameplay-action extraction is not action-attribution stress coverage.
- Opponent-card observations are not action-attribution truth.
- ActionLogRow surfaces are not causal or intent truth.
- Analytics gameplay-action ingest is not parser truth.
- Public taxonomy metadata is not parser support evidence.
- Corpus parity status must not become parser truth, gameplay-action truth,
  event-ordering truth, action-causality truth, analytics truth, AI truth,
  coaching truth, merge readiness, deploy readiness, release readiness,
  production behavior, or tracker-completion authority.

## Error Behavior

Malformed manifest or session-ledger data must fail existing corpus parity
validation tests. Codex C must not add permissive parsing that silently accepts
ambiguous coverage claims.

If implementation discovers that the existing corpus report cannot represent
the contracted report-only boundary without changing report code, Codex C may
make the smallest corpus-report-only code change and document it in the
implementation handoff. That change must not affect parser, analytics, runtime,
workbook, or local app behavior.

If implementation discovers that action-attribution coverage needs parser
behavior, a reduced expected-facts model, private evidence, or event-ordering
movement, Codex C must stop and route back to Codex B. This contract does not
authorize parser behavior changes or synthetic fixture promotion.

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
- changing analytics ingest behavior
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
   event-ordering preservation, and summary counts.
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
- Existing gameplay-action, opponent-card-observation, card-identity,
  evidence-ledger, and analytics-ingest contracts must not be reinterpreted.
- `gameplay_stress.event_ordering` must remain `missing` unless the current
  base branch already contains separately merged authorized movement.
- No report consumer may treat this row as action-attribution parser support.

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
printf '%s\n' docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Codex C should also inspect, but should not need to run unless it edits
adjacent code:

- `tests/test_gameplay_actions.py`
- `tests/test_opponent_card_observations.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_evidence_ledger.py`

## Acceptance Criteria

- `docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md`
  exists and records the report-only boundary.
- Codex C can implement the contract with corpus metadata/tests/docs only.
- `gameplay_stress.action_attribution` is represented as
  `covered_report_only`, not `covered_synthetic`.
- `gameplay_stress.event_ordering` remains unchanged.
- The manifest and session ledger preserve explicit non-claims for causal
  truth, hidden actions, hidden cards, opponent intent, event ordering, player
  mistakes, best-line truth, archetype classification, decklists, gameplay
  advice, analytics truth, AI truth, coaching truth, release readiness,
  production behavior, and full corpus parity.
- No parser behavior, analytics behavior, runtime behavior, or protected
  surface changes are authorized.
- No raw/private/external corpus contents or private action artifacts are
  committed.

## Unknowns

- No committed Mythic Edge-owned fixture currently proves an
  action-attribution stress scenario.
- No committed Mythic Edge-owned fixture currently proves an event-ordering
  stress scenario.
- The reduced expected-facts model for future synthetic action-attribution
  coverage remains undefined.
- It remains unknown whether future action-attribution coverage should be split
  by action type, actor relation, zone movement, annotations, replacement
  chains, opponent visibility, or another evidence model.

## Suspected Gaps

- Corpus parity can currently express that the family has been inspected, but
  not that Mythic Edge has dedicated action-attribution stress support.
- The phrase "action attribution" is easy to overread as causal intent or
  hidden-action truth.
- Future coverage will likely need a smaller expected-facts schema before safe
  synthetic fixtures can be committed.
- Event-ordering coverage likely needs a separate contract because it may
  require different evidence and invariants.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #410, gameplay action-attribution corpus coverage, under tracker #158.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/410

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md

Goal:
Implement the smallest corpus metadata/test/docs package needed to satisfy the contract. This is report-only boundary coverage for `gameplay_stress.action_attribution`, not parser support, not synthetic gameplay coverage, and not event-ordering coverage.

Expected files:
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md
- docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md

Required behavior:
- Add exactly one report-only manifest entry for `gameplay_stress.action_attribution`.
- Add exactly one count-only session-ledger entry.
- Keep `coverage_status` as `covered_report_only`.
- Keep `coverage_basis` as `["fixture_metadata_only"]`.
- Keep `parser_event_families` empty.
- Keep `gameplay_stress.event_ordering` unchanged.
- Preserve explicit non-claims for action-attribution parser stress support, causal action truth, hidden actions, hidden cards, opponent intent, event ordering, player mistakes, best-line truth, archetype classification, decklists, gameplay advice, analytics truth, AI truth, coaching truth, release readiness, production behavior, and full corpus parity.
- Do not change parser behavior or protected surfaces.

Do not:
- Target main directly.
- Close tracker #158.
- Close issue #410.
- Claim full Mythic Edge corpus parity.
- Promote this family to covered_synthetic without contract loopback.
- Move `gameplay_stress.event_ordering` without contract loopback.
- Import, copy, mirror, or commit Manasight raw logs, external corpus contents, private Player.log excerpts, private local logs, private smoke outputs, generated/private/runtime artifacts, workbook exports, SQLite files, credentials, tokens, API keys, webhook URLs, decklists, deck names, card choices, sideboard choices, private strategy notes, or private reports.
- Change parser behavior, gameplay-action extraction behavior, opponent-card-observation behavior, parser event classes, ActionLogRow shape, router semantics, parser state final reconciliation, match/game identity, deduplication, diagnostics, golden replay, feature-equity, evidence ledger, runtime status, analytics ingest, workbook, webhook, Apps Script, Google Sheets sync, output transport, analytics truth, AI/OpenAI, coaching, CI gates, merge policy, deploy policy, or production behavior.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- printf '%s\n' docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
- printf '%s\n' docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/410"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/408"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/409"
  previous_merge_commit: "574cd23d046d19fb64266d079d1d6173d23f7cf4"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_gameplay_action_attribution_coverage.md"
  verdict: "contract_ready_for_report_only_boundary_metadata"
  risk_tier: "High"
  branch: "codex/parser-corpus-gameplay-action-attribution-coverage"
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
    - "Do not close issue #410."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not promote gameplay_stress.action_attribution to covered_synthetic without contract loopback."
    - "Do not move gameplay_stress.event_ordering without contract loopback."
    - "Do not claim action-attribution support from generic gameplay-action extraction, opponent-card observations, ActionLogRow surfaces, analytics gameplay-action ingest, evidence-ledger provenance, or public taxonomy evidence alone."
    - "Do not infer hidden actions, hidden cards, causal intent, event ordering beyond parser-owned evidence, player mistakes, archetypes, decklists, gameplay advice, analytics truth, AI truth, coaching truth, release readiness, or production behavior."
    - "Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, private smoke outputs, generated/private/runtime artifacts, workbook exports, SQLite files, decklists, deck names, card choices, sideboard choices, private strategy notes, private reports, or secrets."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/analytics/AI/production surfaces without a new explicit contract."
```
