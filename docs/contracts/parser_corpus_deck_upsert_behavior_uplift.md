# Parser Corpus Deck Upsert Behavior Uplift Contract

## Module

`deck_api.deck_upsert` parser corpus behavior uplift planning.

Plain English: Mythic Edge already records `deck_api.deck_upsert` as a
report-only corpus boundary from issue #396. This contract decides whether that
row can safely move toward parser-behavior readiness from current adjacent deck
evidence. The answer for this slice is no: current Mythic Edge evidence covers
nearby surfaces such as `deck_api.event_set_deck`, submit-deck client actions,
submitted-deck card-content provenance, StartHook deck snapshots, and
deck-summary boundaries, but none of those are dedicated deck-upsert API
parser behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/490
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/488
- Previous completed PR: https://github.com/Tahjali11/Mythic-Edge/pull/489
- Previous merge commit: `73f615d59211397f8a783b3971e43b2060b6ccfa`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/396
- Base branch inspected: `main`
- Contract branch:
  `codex/parser-corpus-deck-upsert-behavior-uplift-490`
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

- `docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md`
- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- `docs/contracts/parser_corpus_deck_summary_behavior_uplift.md`
- `docs/contracts/parser_corpus_deck_summary_coverage.md`
- `docs/contracts/parser_corpus_deck_upsert_coverage.md`
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md`
- `docs/contracts/parser_client_actions.md`
- `docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `tests/test_client_actions_parser.py`

## Purpose

Define the narrowest safe behavior-uplift boundary for
`deck_api.deck_upsert`.

This contract answers:

- whether `deck_api.deck_upsert` may be promoted from `covered_report_only`
  in this slice;
- whether `parser_behavior_verified` may be added from EventSetDeck,
  SubmitDeckResp, StartHook, deck-summary, submitted-deck-card, or deck-state
  evidence;
- what distinct evidence would be required before a future uplift can proceed;
- which fixture, manifest, session-ledger, parser, privacy, and readiness
  changes are forbidden; and
- how #388 / #381 activation remains deferred.

This contract does not implement code, create fixtures, edit corpus metadata,
run private/live MTGA checks, activate #388/#381, or claim deck-upsert parser
support.

## Observed Current Behavior

Observed on `main` at
`73f615d59211397f8a783b3971e43b2060b6ccfa`:

- Issue #490 is open.
- Tracker #158 remains open.
- Related pipeline tracker #388 remains open and deferred.
- Parent private-evidence issue #434 remains open.
- Issue #488 is complete after PR #489.
- The corpus parity report says:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=16, report_only=17, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Current `deck_api.deck_upsert` row:

```yaml
scenario_family: "deck_api.deck_upsert"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "deck_upsert_boundary_report_v1"
parser_event_families: []
parser_claim_families:
  - "deck_upsert_boundary_report"
  - "event_set_deck_reference_only"
  - "submit_deck_reference_only"
  - "dedicated_deck_upsert_api_not_claimed"
  - "deck_upsert_privacy_boundary"
```

Current adjacent evidence:

- `deck_api.event_set_deck` is `covered_committed` and
  `parser_behavior_verified`.
- `ClientMessageType_SubmitDeckResp` is parsed by
  `src/mythic_edge_parser/parsers/client_actions.py` as
  `submit_deck_resp`.
- `submit_deck_resp` payloads preserve request context and normalize
  `deck_cards` and `sideboard_cards`.
- Evidence-ledger contracts map `submit_deck_seen` and
  `submitted_deck_cards` as submit-deck signal and card-content provenance.
- `deck_api.start_hook_deck_snapshot` is `covered_synthetic`.
- `deck_api.deck_summary` remains `covered_report_only` after issue #488.

Current non-evidence:

- There is no observed dedicated deck-upsert parser route.
- There is no observed dedicated deck-upsert event family.
- There is no observed dedicated deck-upsert golden replay fixture.
- The current `deck_upsert_boundary_report_v1` entry has no parser event
  families.
- The current session ledger records `dedicated_deck_upsert_api_events: 0` and
  `dedicated_deck_upsert_parser_routes: 0`.
- No inspected contract authorizes treating EventSetDeck, SubmitDeckResp,
  submitted-deck card lists, StartHook deck snapshots, deck summaries,
  deck-state notes, inventory, or collection evidence as deck-upsert parser
  support.

## Scope Decision

Selected path: preserve `covered_report_only`.

Codex B considered these paths:

1. Promote `deck_api.deck_upsert` to `covered_synthetic` from adjacent
   EventSetDeck, SubmitDeckResp, StartHook, deck-summary, or submitted-deck
   evidence.
2. Keep `deck_api.deck_upsert` as `covered_report_only` and document the
   behavior-uplift blocker.
3. Split or reframe the taxonomy before any behavior uplift.
4. Add dedicated deck-upsert parser behavior under a future contract if owned
   evidence exists.

Selected decision: option 2, with options 3 or 4 as future prerequisites.

Reasoning:

- Issue #396 already records deck upsert as a report-only boundary because
  current evidence is adjacent-only.
- EventSetDeck is its own corpus family and must not be reclassified as
  upsert behavior.
- SubmitDeckResp and submitted-deck cards are submit-deck and card-content
  provenance surfaces, not deck-upsert API support.
- StartHook deck snapshots and deck summaries are separate deck API
  boundaries.
- The current row explicitly records zero dedicated deck-upsert events and
  zero dedicated deck-upsert parser routes.
- A behavior uplift without a dedicated parser-owned evidence path would imply
  broader deck API support than Mythic Edge currently proves.

Therefore this contract does not authorize Codex C to add fixtures, mutate the
manifest/session ledger, or change `deck_api.deck_upsert` status in #490.

## Owning Layer

Owning layer: Corpus / Provenance.

Supporting truth layers:

- Client-action parsing owns SubmitDeckResp normalization.
- Parser state owns observed submit-deck signal application to match state.
- Evidence ledger owns submitted-deck signal and card-content provenance
  boundaries.
- StartHook collection parsing owns StartHook deck snapshot behavior.
- Corpus parity reporting owns status aggregation and readiness metrics.

This contract does not move truth ownership to corpus metadata, workbook
formulas, dashboards, Apps Script, webhook transport, analytics, AI, coaching,
readiness, deploy, or production surfaces.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser, as the producer of adjacent EventSetDeck, client-action, StartHook,
  and submitted-deck facts.
- Quality / Governance, as the owner of validation and protected-surface
  discipline.

This slice is not analytics, AI, coaching, workbook, webhook, Apps Script,
local app, release readiness, production behavior, private evidence execution,
or parser-evidence pipeline activation.

## Truth Owner

Truth owner for current report-only status:

- `docs/contracts/parser_corpus_deck_upsert_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owners for adjacent parser evidence that must not be reclassified:

- `docs/contracts/parser_client_actions.md`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `tests/test_client_actions_parser.py`
- `docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/contracts/parser_corpus_deck_summary_coverage.md`
- `docs/contracts/parser_corpus_deck_summary_behavior_uplift.md`

Truth boundary:

- EventSetDeck behavior may prove only `deck_api.event_set_deck`.
- SubmitDeckResp behavior may prove submit-deck signal and submitted-deck
  card-content provenance, not deck-upsert API support.
- StartHook deck snapshot behavior may prove only
  `deck_api.start_hook_deck_snapshot`.
- Deck-summary boundary metadata remains report-only and does not prove
  deck-upsert support.
- `deck_api.deck_upsert` must remain report-only until a later contract
  introduces distinct parser-owned deck-upsert evidence or reframes the row.
- Corpus coverage status is review metadata. It is not deck identity truth,
  submitted-deck truth beyond existing parser-owned fields, active-deck truth,
  sideboard-delta truth, collection ownership truth, inventory/economy truth,
  analytics truth, AI truth, coaching truth, release readiness, production
  behavior, full corpus parity, tracker-completion authority, or #388/#381
  activation authority.

## Bridge-Code Status

`ambiguous_pending_follow_up`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Current allowed data flow:

```text
existing EventSetDeck / SubmitDeckResp / StartHook / deck-summary evidence
  -> deck_api.deck_upsert report-only boundary row
  -> corpus parity report non-claim metadata
```

Forbidden reverse flow:

- Corpus coverage status must not change parser behavior.
- Corpus metadata must not create, imply, or require a dedicated deck-upsert
  parser.
- Corpus metadata must not add `parser_behavior_verified` to
  `deck_api.deck_upsert` from adjacent evidence.
- Corpus metadata must not reclassify EventSetDeck, SubmitDeckResp,
  submitted-deck cards, StartHook deck snapshots, deck summaries, deck state,
  inventory, or collection evidence as deck-upsert behavior.
- Corpus metadata must not move private deck contents, deck identity,
  submitted-deck facts, decklist completion, analytics, AI, coaching, workbook,
  webhook, or Apps Script interpretation into parser truth.

Protected surfaces explicitly not touched:

- parser behavior
- client-action parser behavior
- parser event classes
- parser state final reconciliation
- router semantics
- match/game identity
- deduplication
- diagnostics behavior
- drift reports
- golden replay behavior
- feature-equity behavior
- evidence-ledger behavior
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- runtime status files
- failed posts
- workbook exports
- analytics truth
- AI/model-provider behavior
- coaching behavior
- CI gates
- merge readiness
- deploy readiness
- production behavior
- final integration policy

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md`

Files future roles may inspect:

- `docs/contracts/parser_corpus_deck_upsert_coverage.md`
- `docs/contracts/parser_corpus_deck_summary_behavior_uplift.md`
- `docs/contracts/parser_corpus_deck_summary_coverage.md`
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/contracts/parser_client_actions.md`
- `docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `tests/test_client_actions_parser.py`

Files Codex C is not authorized to change from this contract:

- corpus manifest or session-ledger status for `deck_api.deck_upsert`
- golden replay fixtures or manifests
- client-action parser source
- client-action parser tests
- evidence-ledger implementation
- parser event classes
- runtime surfaces
- workbook/webhook/App Script/Sheets outputs
- analytics, AI, coaching, release, or production code

If a later role believes any of those files must change, route back to Codex A
or Codex B for a new scoped contract.

## Public Interface

No runtime public API is added by this contract.

The current corpus row should remain:

```yaml
scenario_family: "deck_api.deck_upsert"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "deck_upsert_boundary_report_v1"
```

This contract does not authorize:

```yaml
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
```

for `deck_api.deck_upsert` in issue #490.

## Future Behavior-Uplift Prerequisites

Future behavior uplift requires one of these prerequisite decisions.

### Option A: Dedicated Deck-Upsert Evidence

A future Codex A/B issue may authorize behavior uplift only if distinct owned
evidence exists for a dedicated deck-upsert API response.

Required future evidence would include:

- a dedicated parser route or clearly documented existing route for the
  upsert payload;
- accepted raw payload shape;
- emitted parser event family or explicitly bounded parser-owned output;
- malformed/partial payload behavior;
- raw evidence preservation expectations;
- focused tests for that behavior;
- corpus manifest/session-ledger entries distinct from
  `deck_upsert_boundary_report_v1`; and
- explicit non-claims around deck identity, private deck contents, active-deck
  truth, submitted-deck truth, sideboard deltas, collection ownership,
  inventory/economy, analytics, AI, coaching, readiness, and production truth.

### Option B: Taxonomy Reframe Or Deprecation

A future Codex A/B issue may decide that `deck_api.deck_upsert` should remain
a permanent report-only blind-spot row, or that the public taxonomy should be
split into narrower rows once Mythic Edge has clearer evidence.

Examples of narrower rows could include:

- `deck_api.event_set_deck`, already covered separately;
- submit-deck signal and submitted-deck card-content provenance, already owned
  by parser and evidence-ledger contracts; and
- a future dedicated upsert API row, only if owned evidence appears.

### Option C: Preserve Report-Only Boundary

If neither prerequisite is selected, the current row remains
`covered_report_only`.

This is the selected path for #490.

## Behavior-Uplift Packet

This section is a reusable packet pattern for future behavior-uplift rows. In
this contract it applies only to `deck_api.deck_upsert`. It must not be used
here to solve, promote, or reclassify any other corpus row.

| Question | Contracted answer for #490 |
| --- | --- |
| Scenario family | `deck_api.deck_upsert` |
| Current status and basis | `covered_report_only` with `fixture_metadata_only` through `deck_upsert_boundary_report_v1` |
| Target status, if any | No target status movement in #490; preserve `covered_report_only` |
| May `parser_behavior_verified` be added? | No, not from EventSetDeck, SubmitDeckResp, submitted-deck cards, StartHook, deck-summary, deck-state, inventory, or collection evidence; future addition requires distinct deck-upsert evidence under a new contract |
| Evidence type | Remain report-only in #490; future evidence may be synthetic or committed sanitized only if separately contracted; private-gated and external-gated evidence are forbidden in this lane |
| Fixture/golden replay changes | Forbidden in #490; do not add, mutate, or relabel fixtures for `deck_api.deck_upsert` |
| Manifest/session-ledger changes | Forbidden in #490 except under a later contract; do not change status, basis, entries, readiness flags, or related counts for this row |
| Parser behavior changes | Forbidden; no client-action parser, event-class, router, state, runtime, workbook, webhook, or analytics changes |
| Private/external inputs | Private Player.log, UTC_Log, live MTGA checks, live deck API checks, Manasight/external raw corpora, decklists, deck names, card choices, strategy notes, and private reports are forbidden |
| Required non-claims | No dedicated deck-upsert parser support, deck identity truth, active-deck truth, submitted-deck truth beyond existing parser-owned fields, sideboard-delta truth, decklist completion, collection ownership truth, inventory/economy truth, deck-summary support, StartHook support, EventSetDeck support, submit-deck support, archetype truth, analytics truth, AI truth, coaching truth, private smoke, release readiness, production behavior, full corpus parity, tracker completion, or #388/#381 activation claims |
| Focused validation | Corpus parity report, corpus status inspection, docs check, diff check, path-scoped secret scan, path-scoped protected-surface scan |
| #388/#381 stop condition | Do not activate #388 or #381 from this row; preserving report-only status does not improve parser-behavior readiness counts |

Future behavior-uplift contracts may copy this packet shape, but each future
row still needs its own issue, contract, evidence decision, non-claims, and
validation plan.

## Explicit Non-Claims

This contract does not claim:

- `deck_api.deck_upsert` parser behavior support;
- dedicated deck-upsert API support;
- new deck-upsert fixture coverage;
- new deck-upsert golden replay coverage;
- EventSetDeck support beyond the existing `deck_api.event_set_deck` family;
- SubmitDeckResp support beyond existing parser and evidence-ledger surfaces;
- deck-summary support beyond the existing report-only row;
- StartHook deck snapshot support beyond the existing synthetic row;
- submitted-deck card-content truth beyond existing parser/evidence-ledger
  fields;
- deck identity truth;
- active-deck truth;
- sideboard-delta truth;
- collection ownership truth;
- inventory or economy truth;
- decklist completion;
- archetype truth;
- gameplay advice;
- analytics truth;
- AI truth;
- coaching truth;
- private smoke success;
- release readiness;
- production behavior;
- full corpus parity;
- tracker completion;
- #388 / #381 activation.

## Inputs

Allowed inputs:

- repo-owned contracts, handoffs, reports, fixtures, and tests;
- current corpus manifest and session ledger metadata;
- current corpus parity report output;
- current client-action parser implementation and focused tests;
- current evidence-ledger contracts for submit-deck surfaces;
- public GitHub issue/PR metadata for #396, #488, #489, and #490.

Forbidden inputs:

- private Player.log excerpts;
- UTC_Log excerpts;
- live MTGA runs;
- live deck API checks;
- local app-data or runtime artifacts;
- private smoke outputs;
- screenshots;
- Manasight raw logs, compressed corpus files, parser source, or external
  corpus contents;
- generated/private/runtime artifacts;
- SQLite files;
- workbook exports;
- secrets, credentials, tokens, API keys, or webhook URLs;
- private decklists, deck names, card choices, collection data, or strategy
  notes.

## Validation Obligations

Codex B validation for this contract should include:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json \
  --out /tmp/mythic_edge_issue_490_corpus_report.json
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

Codex E validation should verify:

- the contract preserves #396's report-only boundary;
- the contract does not authorize status movement for
  `deck_api.deck_upsert`;
- the contract does not authorize `parser_behavior_verified`;
- the contract does not reclassify EventSetDeck, SubmitDeckResp,
  submitted-deck cards, StartHook, deck-summary, deck-state, inventory, or
  collection evidence as deck-upsert behavior;
- the contract does not authorize fixture, manifest, session-ledger, parser,
  workbook, webhook, Apps Script, analytics, AI, coaching, readiness, or
  production changes;
- the contract preserves #388/#381 activation gates;
- validation output is documented in
  `docs/contract_test_reports/parser_corpus_deck_upsert_behavior_uplift.md`.

Codex C validation is not applicable unless a later contract authorizes
implementation.

## Acceptance Criteria

This contract is complete when:

- `docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md` exists;
- observed current behavior is separated from required guarantees;
- the status decision preserves `covered_report_only`;
- the contract explains why EventSetDeck, SubmitDeckResp, submitted-deck cards,
  StartHook, deck-summary, deck-state, inventory, and collection evidence
  cannot add `parser_behavior_verified` to `deck_api.deck_upsert`;
- future prerequisite paths are explicit;
- the behavior-uplift packet is included but scoped only to this row;
- protected surfaces and non-claims are explicit;
- validation expectations are listed; and
- the workflow handoff routes away from Codex C unless new implementation
  authority is created.

## Recommended Next Role

Recommended next role: Codex E: Module Reviewer.

Reason: #490 produces a contract that intentionally does not authorize Codex C
implementation. The next useful step is review/contract-test validation. If
the project wants behavior uplift later, Codex A should frame a follow-up issue
for either dedicated deck-upsert evidence or taxonomy reframing.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #490.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/490

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/488

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/489

Previous merge commit:
73f615d59211397f8a783b3971e43b2060b6ccfa

Prior deck-upsert boundary:
https://github.com/Tahjali11/Mythic-Edge/issues/396

Contract under review:
docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md

Goal:
Review the #490 contract and produce
docs/contract_test_reports/parser_corpus_deck_upsert_behavior_uplift.md.

Verify that the contract preserves `deck_api.deck_upsert` as
`covered_report_only`, does not authorize `parser_behavior_verified`, does not
reclassify EventSetDeck, SubmitDeckResp, submitted-deck cards, StartHook,
deck-summary, deck-state, inventory, or collection evidence as deck-upsert
behavior, does not authorize fixtures or corpus status changes, and keeps
#388/#381 activation deferred.

Do not implement code.
Do not open a PR unless explicitly instructed.
Do not close #158, #388, #434, or #490.
Do not change corpus statuses, fixtures, parser behavior, workbook/webhook/App
Script behavior, analytics truth, AI truth, coaching truth, release readiness,
production behavior, or final integration policy.
Do not claim dedicated deck-upsert API support or full corpus parity.

Expected output:
- Contract-test report
- Verdict: ready for no-op/defer, needs contract clarification, or route to
  Codex A for taxonomy/evidence split
- Validation evidence
- workflow_handoff block
```

If implementation is later desired, use Codex A first to frame one of:

- dedicated deck-upsert parser evidence; or
- taxonomy reframing for deck API surfaces.

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/490"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/488"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/489"
  previous_merge_commit: "73f615d59211397f8a783b3971e43b2060b6ccfa"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/396"
  completed_thread: "B"
  next_thread: "E"
  verdict: "deck_upsert_behavior_uplift_deferred_report_only_boundary_preserved"
  risk_tier: "High"
  branch: "codex/parser-corpus-deck-upsert-behavior-uplift-490"
  base_branch: "main"
  selected_family: "deck_api.deck_upsert"
  current_status: "covered_report_only"
  selected_path: "preserve_report_only_dedicated_deck_upsert_evidence_or_taxonomy_reframe_required_before_behavior_uplift"
  target_artifact: "docs/contract_test_reports/parser_corpus_deck_upsert_behavior_uplift.md"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  stop_conditions:
    - "Do not target main directly unless explicitly approved."
    - "Do not close tracker #158, pipeline tracker #388, parent issue #434, or issue #490."
    - "Do not activate #388 or #381."
    - "Do not promote deck_api.deck_upsert or add parser_behavior_verified from adjacent evidence."
    - "Do not claim dedicated deck-upsert API support, parser support, readiness, production behavior, analytics truth, AI truth, coaching truth, full corpus parity, or tracker completion."
```
