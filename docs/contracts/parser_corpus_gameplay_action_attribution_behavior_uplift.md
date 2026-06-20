# Parser Corpus Gameplay Action-Attribution Behavior Uplift Contract

## Module

`gameplay_stress.action_attribution` parser corpus behavior uplift planning.

Plain English: Mythic Edge already records action-attribution coverage as
report-only boundary metadata from issue #410. This contract defines the
narrowest safe path for moving the row toward parser-behavior readiness:
reduced synthetic action-fact preservation evidence only. The uplift may prove
that existing `GameState` and `gameplay_actions.py` behavior can attribute
bounded action facts such as action type, actor relation, zone movement, raw
action labels, card identity hints, and timing context. It must not claim
causal truth, hidden-action truth, hidden-card truth, opponent intent, complete
event ordering, player mistakes, best-line truth, gameplay advice, analytics
truth, AI truth, coaching truth, release readiness, production behavior,
tracker completion, or full corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/496
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/494
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/495
- Previous merge commit: `f5c533d420058e364405b283a976923ec04d3b66`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/410
- Base branch inspected: `main`
- Contract branch:
  `codex/parser-corpus-gameplay-action-attribution-behavior-uplift-496`
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

- `docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md`
- `docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md`
- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- `docs/contracts/parser_corpus_readiness_metrics.md`
- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`
- `docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`
- `docs/contracts/analytics_gameplay_action_ingest.md`
- `docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `tests/test_gameplay_actions.py`
- `tests/test_opponent_card_observations.py`

## Purpose

Define the minimum safe evidence model for moving
`gameplay_stress.action_attribution` beyond the #410 report-only boundary.

This contract answers:

- whether the row may move from `covered_report_only` toward
  `covered_synthetic`;
- what reduced synthetic parser evidence is sufficient;
- what `parser_behavior_verified` may and may not mean for this row;
- which adjacent surfaces remain context only; and
- how #388 / #381 activation remains deferred.

This contract does not implement code, create fixtures, edit corpus metadata,
run private/live MTGA checks, activate #388/#381, or claim action-attribution
support beyond reduced synthetic action-fact preservation.

## Observed Current Behavior

Observed on `main` at
`f5c533d420058e364405b283a976923ec04d3b66`:

- Issue #496 is open.
- Tracker #158 remains open.
- Related pipeline tracker #388 remains open and deferred.
- Parent private-evidence issue #434 remains open.
- Issue #494 is complete after PR #495.
- The corpus parity report says:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=17, report_only=16, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Current `gameplay_stress.action_attribution` row:

```yaml
scenario_family: "gameplay_stress.action_attribution"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "gameplay_action_attribution_boundary_report_v1"
parser_event_families: []
parser_claim_families:
  - "gameplay_action_attribution_boundary_report"
  - "gameplay_action_extraction_not_stress_coverage"
  - "opponent_card_observation_not_action_attribution_truth"
  - "action_log_row_not_causal_truth"
  - "analytics_ingest_not_parser_truth"
  - "event_ordering_not_claimed"
  - "hidden_action_inference_non_claim"
```

Current adjacent parser behavior:

- `src/mythic_edge_parser/app/gameplay_actions.py` consumes `GameState` events
  through `observe_event(event)`.
- Gameplay-action extraction maintains per-match/game action state, tracks
  zones and objects, records raw action labels, classifies selected action
  types, preserves card identity hints, derives actor relation from local seat
  context, and writes local runtime action artifacts.
- Focused tests already exercise local turn, land, spell, limbo, annotation,
  adventure, hidden-rendering, and resolution-related behavior.
- `src/mythic_edge_parser/app/opponent_card_observations.py` consumes
  gameplay-action entries to build visible opponent-card observations, but
  opponent-card observation is downstream of gameplay action.
- The evidence-ledger Tier 5 gameplay-action contract maps
  `gameplay_action` as a broad provenance field, not as an action-causality or
  hidden-action truth source.
- Analytics gameplay-action ingest can store parser-normalized action facts,
  but analytics storage is downstream and does not own parser truth.

Current non-evidence:

- The #410 boundary explicitly says generic gameplay-action extraction,
  opponent-card observations, ActionLogRow surfaces, analytics ingest,
  evidence-ledger provenance, public taxonomy metadata, and local/private
  action artifacts are not action-attribution stress support by themselves.
- No current corpus entry proves a reduced action-fact expectation packet for
  `gameplay_stress.action_attribution`.
- `gameplay_stress.event_ordering` remains a separate row and must not be
  folded into this uplift.
- Current gameplay-action tests are parser tests, not corpus status authority
  until the manifest/session ledger cite a contract-authorized evidence entry.

## Scope Decision

Recommended future path: reduced synthetic action-fact behavior uplift.

A later Codex C implementation may move
`gameplay_stress.action_attribution` from `covered_report_only` toward
`covered_synthetic` with `parser_behavior_verified` only if it adds
Mythic Edge-owned synthetic evidence proving a reduced action-fact packet
through existing `GameState` and `gameplay_actions.py` behavior.

The reduced action-fact packet must prove parser-owned preservation of:

- at least one local action and at least one opponent action, or an explicitly
  justified equivalent actor-relation pair;
- `action_type`;
- `actor_relation`;
- `game_state_id`, `turn_number`, and timestamp context;
- `instance_id` and at least one card identity hint such as `grp_id`,
  `observed_grp_id`, `object_source_grp_id`, `parent_id`, or
  `identity_hint_source`;
- `from_zone_type` and `to_zone_type`;
- `raw_action_types` where a GRE action array is present; and
- annotation categories or annotation types when the synthetic sequence uses
  annotation-derived attribution.

The behavior claim is intentionally small:

- observed/derived parser-owned action facts, not causal truth;
- bounded actor relation, not player identity or opponent intent;
- bounded zone/action evidence, not complete event ordering;
- existing parser behavior, not new parser interpretation.

This contract authorizes a metadata/test/docs implementation path. It does not
authorize parser behavior changes. If Codex C cannot prove the reduced
synthetic action-fact packet using existing parser behavior, the row must
remain `covered_report_only` and route back to Codex B or Codex A.

## Owning Layer

Owning layer: Corpus / Provenance.

Supporting truth layers:

- `gameplay_actions.py` owns existing parser-owned gameplay-action extraction
  and action-entry facets.
- `opponent_card_observations.py` owns downstream visible opponent-card
  observation facts, not action-attribution truth.
- The evidence ledger owns provenance descriptions for parser-owned action
  facts.
- Analytics ingest owns downstream local storage of parser-normalized action
  facts.
- Corpus parity reporting owns status aggregation and readiness metrics.

This contract does not move truth ownership to corpus metadata, workbook
formulas, dashboards, Apps Script, webhook transport, analytics, AI, coaching,
readiness, deploy, production, or tracker lifecycle surfaces.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser, as the existing producer of gameplay-action facts.
- Quality / Governance, as the owner of validation and protected-surface
  discipline.

This slice is not analytics, AI, coaching, workbook, webhook, Apps Script,
local app, release readiness, production behavior, private-evidence execution,
or parser-evidence pipeline activation.

## Truth Owner

Truth owner for current report-only status:

- `docs/contracts/parser_corpus_gameplay_action_attribution_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for future reduced synthetic behavior evidence:

- `src/mythic_edge_parser/app/gameplay_actions.py`
- `tests/test_gameplay_actions.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- the future Codex C implementation handoff;
- the future Codex E contract-test report.

Truth boundary:

- A synthetic `GameState` sequence may prove only that existing gameplay-action
  extraction emits bounded action facts from parser-owned evidence.
- Corpus parity may claim `parser_behavior_verified` only for the reduced
  action-fact packet described above.
- The corpus row must not claim causal action truth, hidden-action truth,
  hidden-card truth, opponent intent, why an action happened, complete event
  ordering, action absence, player mistakes, best-line truth, archetype
  classification, decklist truth, gameplay advice, analytics truth, AI truth,
  coaching truth, private smoke success, release readiness, production
  behavior, #388/#381 activation, tracker completion, or full corpus parity.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
owned synthetic GameState action-fact test inputs
  -> existing gameplay_actions.py behavior
  -> focused parser test assertions
  -> corpus manifest/session-ledger behavior metadata
  -> corpus parity readiness metrics
```

Forbidden reverse flow:

- Corpus readiness must not change parser behavior.
- Corpus metadata must not create parser-owned facts absent from gameplay
  action output.
- Corpus metadata must not turn opponent observations, ActionLogRow rows,
  analytics ingest, evidence-ledger provenance, public taxonomy labels,
  private action artifacts, or local gameplay logs into action-attribution
  support.
- Corpus metadata must not move causality, hidden information, event ordering,
  player mistakes, analytics, AI, coaching, workbook, webhook, or Apps Script
  interpretation into parser truth.

Protected surfaces explicitly not touched:

- parser behavior;
- gameplay-action extraction behavior;
- opponent-card-observation behavior;
- parser event classes;
- ActionLogRow shape;
- router semantics;
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

- `docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md`

Future Codex C files authorized only if implementation is selected:

- `tests/test_gameplay_actions.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_behavior_uplift_comparison.md`
- `docs/contract_test_reports/parser_corpus_gameplay_action_attribution_behavior_uplift.md`

Files Codex C may inspect but must not change without contract loopback:

- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/state.py`
- `tests/test_opponent_card_observations.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- adjacent corpus/evidence-ledger contracts and reports.

Not owned by this contract:

- parser semantics;
- new parser events;
- parser state final reconciliation;
- opponent-card-observation semantics;
- analytics ingest behavior;
- runtime artifact shapes;
- ActionLogRow shape;
- private evidence;
- external corpus contents;
- workbook/webhook/App Script/Sheets/analytics/AI/coaching surfaces.

## Public Interface

No runtime public API is added by Codex B.

Future Codex C may add committed synthetic test evidence and corpus metadata
that make the corpus parity public report show
`gameplay_stress.action_attribution` as behavior-ready in the limited
action-fact sense. The intended eventual corpus row shape is:

```yaml
scenario_family: "gameplay_stress.action_attribution"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
```

The existing report-only entry `gameplay_action_attribution_boundary_report_v1`
should remain as historical non-claim metadata unless Codex C has a strong
reason to route back for a replacement or migration contract. A new synthetic
evidence entry should be added rather than rewriting #410's boundary into a
behavior claim.

## Minimum Parser-Owned Evidence

Future uplift requires one focused synthetic action-fact packet.

Required:

- one focused test in `tests/test_gameplay_actions.py` or an equivalent
  already-focused test group explicitly cited by the implementation handoff;
- synthetic `GameStateEvent` input only;
- no raw/private log lines;
- no private paths, local app-data, private action artifacts, or generated
  runtime artifacts committed;
- existing `gameplay_actions.observe_event()` path;
- at least two emitted gameplay-action entries unless Codex C justifies a
  narrower single-entry packet;
- at least one action with explicit raw GRE action label context;
- at least one action with actor relation verified as `local` or `opponent`;
- zone movement evidence showing `from_zone_type` and `to_zone_type`;
- timing/context fields including `timestamp`, `game_state_id`, `game_number`,
  and `turn_number`;
- card identity context including `instance_id` and at least one `grp_id` or
  identity-hint field; and
- assertion that local runtime write paths are redirected to temporary test
  directories and do not touch real local artifacts.

Recommended reduced packet:

- one local action such as `land_played` or `spell_cast`;
- one opponent action such as `spell_cast`, if existing behavior can produce
  it without parser changes;
- direct action-array evidence via `raw_action_types`;
- one annotation-derived or replacement-chain facet only if existing tests
  already support it cleanly.

Not sufficient:

- a corpus manifest/session-ledger update with no focused gameplay-action
  evidence;
- an opponent-card-observation test alone;
- analytics ingest tests alone;
- evidence-ledger provenance alone;
- ActionLogRow or Markdown output alone;
- a test that proves only rendering/display without action-entry facts;
- a test that depends on private Player.log, UTC_Log, local runtime files, live
  MTGA, external corpora, or model-provider output.

## Recommended Evidence / Status Path

Recommended Codex C path:

1. Add or identify a focused reduced action-fact test in
   `tests/test_gameplay_actions.py`.
2. Assert the required action-entry facts, not just rendered Markdown.
3. Add one new corpus manifest entry for the synthetic action-fact behavior
   evidence.
4. Add one new session-ledger entry for the same synthetic action-fact
   evidence.
5. Keep `gameplay_action_attribution_boundary_report_v1` as report-only
   non-claim metadata.
6. Update focused corpus parity tests for the new status, entry list, claim
   families, summary row, and non-claims.
7. Verify `gameplay_stress.event_ordering` is unchanged.
8. Write the implementation handoff and contract-test report.

Allowed future status movement:

- from `covered_report_only` to `covered_synthetic`;
- with `coverage_basis` including both `fixture_metadata_only` and
  `parser_behavior_verified`;
- only after the reduced synthetic action-fact packet passes focused tests.

Disallowed in this lane:

- `covered_committed`, unless a later sanitized fixture-promotion issue
  explicitly creates a reviewed sanitized fixture;
- private/local-only evidence;
- external corpus evidence;
- status movement without focused action-fact evidence;
- status movement based only on #410 report-only metadata, generic
  gameplay-action existence, opponent-card observations, ActionLogRow output,
  analytics ingest, evidence-ledger provenance, public taxonomy metadata, or
  private gameplay material.

## Behavior-Uplift Packet

This packet applies only to `gameplay_stress.action_attribution`. It is a
reusable pattern note for future behavior-uplift rows, but it must not be used
here to solve, promote, or reclassify any other corpus row.

| Question | Contracted answer for #496 |
| --- | --- |
| Scenario family | `gameplay_stress.action_attribution` |
| Current status and basis | `covered_report_only` with `fixture_metadata_only` through `gameplay_action_attribution_boundary_report_v1` |
| Target status, if any | `covered_synthetic` only after a reduced synthetic action-fact parser test packet passes |
| May `parser_behavior_verified` be added? | Yes, but only to a new synthetic evidence entry and only for bounded action-fact preservation |
| Evidence type | Synthetic committed parser-focused tests preferred; private-gated and external-gated evidence are forbidden in this lane |
| Fixture/golden replay changes | Focused gameplay-action parser tests are allowed; golden replay fixture changes are not required for V1 and should not be added unless Codex C can justify them without changing parser or report behavior |
| Manifest/session-ledger changes | Additive entries citing this contract are allowed; changing unrelated rows or removing #410 report-only boundary metadata is forbidden |
| Parser behavior changes | Forbidden; if existing parser behavior cannot support the reduced evidence path, route back instead of changing parser behavior |
| Private/external inputs | Private Player.log, UTC_Log, live MTGA, private action artifacts, Manasight/external raw corpora, private reports, and generated/private artifacts are forbidden |
| Required non-claims | No causal truth, hidden-action truth, hidden-card truth, opponent intent, event-ordering truth, action absence, player mistakes, best-line truth, gameplay advice, analytics truth, AI truth, coaching truth, private smoke, release readiness, production behavior, full corpus parity, tracker completion, or #388/#381 activation claims |
| Focused validation | Gameplay-action tests, corpus parity report/tests, docs check, ruff, diff check, path-scoped secret scan, path-scoped protected-surface scan |
| #388/#381 stop condition | Do not activate #388 or #381 from this row; the row may improve readiness counts but does not start the parser-evidence pipeline by itself |

Future behavior-uplift contracts may copy this packet shape, but each future
row still needs its own issue, contract, evidence decision, non-claims, and
validation plan.

## Required Future Manifest Entry Shape

The exact `entry_id` may vary, but future Codex C should prefer:

```yaml
entry_id: "gameplay_action_attribution_synthetic_action_facts_v1"
title: "Gameplay action-attribution synthetic action-fact parser evidence"
entry_type: "focused_parser_tests"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
scenario_families:
  - "gameplay_stress.action_attribution"
parser_event_families:
  - "GameState"
parser_claim_families:
  - "synthetic_action_fact_extraction"
  - "actor_relation_preservation"
  - "zone_movement_attribution"
  - "raw_action_type_preservation"
  - "card_identity_hint_preservation"
  - "action_attribution_synthetic_boundary"
  - "causal_truth_non_claim"
  - "hidden_action_non_claim"
  - "event_ordering_non_claim"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/496"
authorized_by_contract: "docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md"
```

Required known-gap language:

- The fixture proves reduced synthetic action-fact preservation only.
- It does not prove causal action truth, hidden actions, hidden cards,
  opponent intent, why an action happened, complete event ordering, action
  absence, player mistakes, best-line truth, archetype classification,
  decklist truth, gameplay advice, analytics truth, AI truth, coaching truth,
  release readiness, production behavior, #388/#381 activation, tracker
  completion, or full corpus parity.
- The #410 `gameplay_action_attribution_boundary_report_v1` entry remains
  report-only non-claim metadata.

Required `paths` should include:

```yaml
paths:
  gameplay_actions_test: "tests/test_gameplay_actions.py"
  corpus_parity_test: "tests/test_corpus_parity_report.py"
```

## Required Future Session-Ledger Shape

The exact `session_id` may vary, but future Codex C should prefer:

```yaml
session_id: "gameplay_action_attribution_synthetic_action_facts_v1"
title: "Gameplay action-attribution synthetic action-fact parser evidence"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/496"
authorized_by_contract: "docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md"
scenario_families:
  - "gameplay_stress.action_attribution"
format_family: "gameplay_stress"
match_shape: "gameplay_action_attribution_synthetic_action_facts"
record_summary: "committed_synthetic_action_fact_parser_tests"
```

Required session-ledger `parser_coverage` facts:

```yaml
parser_coverage:
  event_families:
    GameState: 1
  unknown_entries: 0
  truncation_count: 0
  synthetic_action_fact_fixtures: 1
  gameplay_action_entries_asserted: 2
  local_actor_relation_assertions: 1
  opponent_actor_relation_assertions: 1
  raw_action_type_assertions: 1
  zone_movement_assertions: 1
  card_identity_hint_assertions: 1
  hidden_action_claims: 0
  hidden_card_claims: 0
  causal_intent_claims: 0
  event_ordering_claims: 0
  player_mistake_claims: 0
```

If Codex C implements a single-entry reduced packet, the session ledger must
set `gameplay_action_entries_asserted: 1`, explain why the narrower packet is
sufficient, and preserve all non-claims. The preferred path remains a
two-entry packet with local and opponent actor-relation coverage.

Required session-ledger game row summary:

```yaml
game_rows:
  count: 0
  result_shape: "not_applicable"
```

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
- no opponent identifiers from private logs
- no account identifiers
- no local paths or machine paths
- no credentials, tokens, API keys, or webhook URLs

## Inputs

Allowed inputs:

- Existing committed parser source and focused tests for gameplay-action
  extraction.
- New obvious synthetic `GameStateEvent` payloads embedded in focused tests.
- Existing committed corpus parity manifest and session ledger.
- Existing committed contracts and reports for action attribution,
  gameplay-action provenance, opponent-card-observation provenance, analytics
  gameplay-action ingest, and behavior readiness.
- Public Manasight metadata only as already merged taxonomy/category context,
  not as raw evidence.

Forbidden inputs:

- Manasight raw logs, `.log.gz` files, compressed corpus files, raw session
  payloads, external corpus contents, hash lists, byte-size row lists,
  capture-date row lists, or parser source.
- Private Player.log excerpts, UTC_Log excerpts, private local logs, private
  action artifacts, private smoke outputs, raw gameplay payloads from private
  evidence, decklists, deck names, card choices, sideboard choices, private
  strategy notes, local runtime artifacts, generated data, SQLite files,
  workbook exports, secrets, credentials, tokens, API keys, or webhook URLs.
- Model-provider output or AI interpretation.

## Outputs

Authorized outputs for Codex C:

- Focused parser tests proving the reduced synthetic action-fact packet.
- One corpus manifest entry for the new reduced synthetic action-fact evidence.
- One session-ledger entry for the new reduced synthetic action-fact evidence.
- Focused corpus parity tests proving the row moves to `covered_synthetic`
  with the required non-claims.
- An implementation handoff and contract-test report.

Forbidden outputs:

- committed raw/private gameplay log slices;
- committed private action artifacts;
- committed event-ordering fixtures;
- new parser event classes;
- new parser route behavior;
- new gameplay-action extraction behavior;
- new opponent-card-observation behavior;
- new ActionLogRow fields;
- new runtime files outside temporary test directories;
- new workbook/export/webhook/App Script fields;
- new analytics tables/views/ingest behavior;
- AI/model-provider outputs;
- release-readiness, deploy-readiness, production-readiness, tracker-completion,
  or full-parity verdicts.

## Invariants

- `gameplay_stress.action_attribution` may move to `covered_synthetic` only if
  the reduced synthetic action-fact packet passes.
- `coverage_basis` for the new synthetic entry must include
  `parser_behavior_verified`.
- Existing #410 report-only metadata must remain available as a non-claim
  boundary.
- `gameplay_stress.event_ordering` must remain unchanged in this issue.
- Parser event families for the new synthetic entry must be limited to
  existing source event kinds, expected as `GameState`.
- Gameplay-action extraction is not causal action truth.
- Opponent-card observations are not action-attribution truth.
- ActionLogRow surfaces are not causal or intent truth.
- Analytics gameplay-action ingest is not parser truth.
- Public taxonomy metadata is not parser support evidence.
- Local private gameplay material must not be committed.
- Corpus parity status must not become parser truth, gameplay-action truth,
  event-ordering truth, action-causality truth, analytics truth, AI truth,
  coaching truth, merge readiness, deploy readiness, release readiness,
  production behavior, #388 activation, #381 activation, or
  tracker-completion authority.

## Error Behavior

Malformed manifest or session-ledger data must fail existing corpus parity
validation tests. Codex C must not add permissive parsing that silently accepts
ambiguous coverage claims.

If implementation discovers that current gameplay-action behavior cannot
produce the contracted action-fact packet without source changes, Codex C must
stop and route back. This contract does not authorize parser behavior changes.

If implementation discovers that the corpus report cannot represent the
contracted synthetic evidence without a small report-only adjustment, Codex C
may make the smallest corpus-report-only code change and document it. That
change must not affect parser behavior or protected surfaces.

If event ordering would need to move together with action attribution, Codex C
must stop and route back. This contract explicitly keeps
`gameplay_stress.event_ordering` unchanged.

If private evidence would be needed to make a stronger claim, the row must not
be promoted from private evidence in this lane. Private evidence must stay out
of the repo and out of GitHub issue comments.

## Side Effects

Allowed future Codex C side effects:

- Add focused synthetic gameplay-action parser tests.
- Edit committed corpus parity metadata.
- Edit focused corpus parity tests.
- Write implementation handoff and contract-test report docs.

Forbidden side effects:

- opening or closing issues;
- opening a PR unless separately asked;
- staging or committing unless separately asked;
- changing parser behavior;
- changing gameplay-action extraction behavior;
- changing opponent-card-observation behavior;
- changing analytics ingest behavior;
- creating runtime/generated/private artifacts;
- committing local logs or raw private evidence;
- changing CI gates, merge policy, deploy policy, production behavior, or
  final integration policy.

## Dependency Order

Codex C should make changes in this order:

1. Confirm branch and base state against `main`.
2. Compare current manifest/session-ledger/report behavior against this
   contract.
3. Add or identify the focused reduced action-fact parser test.
4. Add the new corpus manifest entry.
5. Add the new session-ledger entry.
6. Update focused corpus parity tests for status, claim families, non-claims,
   summary counts, readiness metrics, and event-ordering preservation.
7. Run focused validation.
8. Write the implementation handoff and contract-test report.
9. Run docs/protected-surface/secret checks on changed files.

## Compatibility

Compatibility expectations:

- Existing #410 report-only entry remains as non-claim boundary metadata.
- Existing covered families and summary counts must remain stable except for
  the status/count deltas authorized by this contract.
- Current report semantics for `covered_committed`, `covered_synthetic`,
  `covered_report_only`, `partial`, `missing`, `blocked_private_evidence`, and
  `blocked_external_boundary` must remain compatible.
- Existing entries for gameplay-action provenance, opponent-card observations,
  analytics gameplay-action ingest, and event ordering must not be
  reinterpreted.
- No report consumer may treat this row as causal truth, hidden-action truth,
  hidden-card truth, opponent intent, event-ordering truth, analytics truth,
  AI truth, coaching truth, release readiness, deploy readiness, production
  behavior, or full-parity truth.

Expected summary-count delta after Codex C, relative to issue #496 state:

- `covered_synthetic` increases by `1`.
- `covered_report_only` decreases by `1`.
- `parser_behavior_ready_family_count` may increase by `1` only if existing
  readiness implementation derives it from the new synthetic row.
- `pipeline_activation_ready_for_issue_388` remains `false`.
- Other status counts remain unchanged unless the base branch already contains
  unrelated merged changes.

## Tests Required

Codex C must run or justify not running:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md tests/test_gameplay_actions.py tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_behavior_uplift_comparison.md docs/contract_test_reports/parser_corpus_gameplay_action_attribution_behavior_uplift.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md tests/test_gameplay_actions.py tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_behavior_uplift_comparison.md docs/contract_test_reports/parser_corpus_gameplay_action_attribution_behavior_uplift.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Codex E should also inspect:

- that no parser source files changed;
- that the reduced action-fact packet is present and bounded;
- that `gameplay_stress.event_ordering` remains unchanged;
- that all non-claims remain visible in manifest, session ledger, report
  output, handoff, and contract-test report;
- that #388/#381 activation remains false/deferred; and
- that no private/external/raw/generated artifacts were committed.

## Acceptance Criteria

- `docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md`
  exists and records the reduced synthetic action-fact evidence model.
- Codex C can implement the contract with focused tests, corpus
  metadata/tests, and docs only.
- The new synthetic entry proves bounded action facts through existing
  `GameState` and `gameplay_actions.py` behavior.
- `gameplay_stress.action_attribution` may move to `covered_synthetic` only
  with `parser_behavior_verified` tied to the reduced action-fact claim.
- The #410 report-only boundary remains as non-claim metadata.
- `gameplay_stress.event_ordering` remains unchanged.
- No parser behavior or protected surface changes are authorized.
- No raw/private/external corpus contents, private action artifacts, local
  smoke outputs, or generated private artifacts are committed.
- No causal, hidden-action, event-ordering, advice, analytics, AI, coaching,
  readiness, production, #388/#381 activation, tracker-completion, or full
  parity claims are made.

## Unknowns

- Codex C may choose whether the reduced packet is a new focused test or a
  tighter assertion around existing gameplay-action tests. The implementation
  handoff must cite the exact test evidence either way.
- The exact synthetic action sequence may vary, but it must remain small,
  readable, synthetic, and parser-owned.
- The reduced synthetic evidence does not answer whether Mythic Edge should
  ever implement causal action attribution, hidden-action modeling, or
  event-ordering stress coverage.

## Suspected Gaps

- Adjacent gameplay-action surfaces are easy to overread as causality,
  intent, or event ordering.
- A future product-grade action-attribution feature would need a separate
  parser behavior contract for explicit causal semantics, if Mythic Edge ever
  wants that.
- `gameplay_stress.event_ordering` likely remains a separate behavior-uplift
  row after this issue.
- The row may become behavior-ready in a narrow synthetic sense while still
  remaining far from live/private action-attribution validation.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #496, gameplay action-attribution behavior uplift, under tracker #158.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/496

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related parser-evidence pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/494

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/495

Previous merge commit:
f5c533d420058e364405b283a976923ec04d3b66

Prior boundary issue:
https://github.com/Tahjali11/Mythic-Edge/issues/410

Base branch:
main

Contract:
docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md

Goal:
Implement the smallest focused test, corpus metadata/test, and docs package needed to satisfy the contract. This is reduced synthetic action-fact preservation evidence for `gameplay_stress.action_attribution`, not causal action truth, hidden-action truth, hidden-card truth, opponent intent, complete event ordering, player mistakes, best-line truth, gameplay advice, analytics truth, AI truth, coaching truth, readiness, production behavior, #388/#381 activation, tracker completion, or full corpus parity.

Expected files:
- tests/test_gameplay_actions.py
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_behavior_uplift_comparison.md
- docs/contract_test_reports/parser_corpus_gameplay_action_attribution_behavior_uplift.md

Required implementation:
- Add or identify one focused reduced synthetic action-fact test proving existing `GameState` -> `gameplay_actions.py` behavior preserves bounded action facts.
- Prefer at least one local action and one opponent action, or justify a narrower packet in the handoff.
- Assert action type, actor relation, game/timing context, zone movement, raw action labels when present, and card identity hints.
- Add one new corpus manifest entry, preferably `gameplay_action_attribution_synthetic_action_facts_v1`.
- Add one new session-ledger entry for the same synthetic action-fact evidence.
- Move `gameplay_stress.action_attribution` only to `covered_synthetic` with coverage basis including `fixture_metadata_only` and `parser_behavior_verified`.
- Keep `gameplay_action_attribution_boundary_report_v1` as report-only non-claim boundary metadata.
- Keep `gameplay_stress.event_ordering` unchanged.
- Preserve explicit non-claims for causal truth, hidden-action truth, hidden-card truth, opponent intent, event-ordering truth, action absence, player mistakes, best-line truth, gameplay advice, analytics truth, AI truth, coaching truth, private smoke success, release readiness, production behavior, #388/#381 activation, tracker completion, and full corpus parity.

Do not:
- Target main directly.
- Close tracker #158, #388, #434, or issue #496.
- Activate #388 or #381.
- Change parser behavior, gameplay-action extraction behavior, opponent-card-observation behavior, parser event classes, ActionLogRow shape, parser state final reconciliation, router semantics, match/game identity, diagnostics, drift, golden replay, feature-equity, evidence-ledger, analytics ingest, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy.
- Import, copy, mirror, summarize, or commit Manasight raw logs, compressed corpus files, parser source, external corpus contents, private Player.log excerpts, private local logs, raw gameplay payloads from private evidence, private action artifacts, decklists, deck names, card choices, sideboard choices, strategy notes, private smoke reports, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, or webhook URLs.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py tests/test_corpus_parity_report.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- path-scoped secret scan for changed files
- path-scoped protected-surface scan for changed files
- python3 -m ruff check src tests tools
- git diff --check

If existing parser behavior cannot support the reduced synthetic action-fact packet without parser code changes, stop and route back to Codex B or Codex A. Do not change parser behavior in this lane.
```

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/496"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/494"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/495"
  previous_merge_commit: "f5c533d420058e364405b283a976923ec04d3b66"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/410"
  completed_thread: "B"
  next_thread: "C"
  verdict: "gameplay_action_attribution_behavior_uplift_contract_ready"
  risk_tier: "High"
  base_branch: "main"
  target_artifact: "docs/implementation_handoffs/parser_corpus_gameplay_action_attribution_behavior_uplift_comparison.md"
  contract_artifact: "docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md"
  selected_family: "gameplay_stress.action_attribution"
  current_status: "covered_report_only"
  authorized_target_status: "covered_synthetic"
  parser_behavior_ready_after_contract: "conditional_on_codex_c_synthetic_action_fact_tests"
  pipeline_activation_ready_for_issue_388: false
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #158, #388, #434, or issue #496."
    - "Do not activate #388 or #381."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/analytics/AI/coaching/production surfaces."
    - "Do not claim causal truth, hidden-action truth, hidden-card truth, opponent intent, event-ordering truth, action absence, player mistakes, best-line truth, gameplay advice, analytics truth, AI truth, coaching truth, readiness, production behavior, tracker completion, or full corpus parity."
    - "Do not commit private/external/raw/generated artifacts, private action artifacts, decklists, card choices, strategy notes, secrets, credentials, tokens, API keys, or webhook URLs."
