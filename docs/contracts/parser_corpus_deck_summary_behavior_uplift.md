# Parser Corpus Deck Summary Behavior Uplift Contract

## Module

`deck_api.deck_summary` parser corpus behavior uplift planning.

Plain English: Mythic Edge already records `deck_api.deck_summary` as a
report-only corpus boundary from issue #394. This contract decides whether that
row can safely move toward parser-behavior readiness from the currently owned
StartHook `DeckSummaries` evidence. The answer for this slice is no: the
current evidence is StartHook-bound and already belongs to
`deck_api.start_hook_deck_snapshot` from issue #392. Promoting
`deck_api.deck_summary` from the same evidence would double-count the StartHook
fixture and imply standalone deck-summary API support that Mythic Edge has not
proven.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/488
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/482
- Previous completed PR: https://github.com/Tahjali11/Mythic-Edge/pull/487
- Previous merge commit: `a046b4550aae18a07a61cd8222ac2927ea930b6e`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/394
- Related StartHook issue: https://github.com/Tahjali11/Mythic-Edge/issues/392
- Base branch inspected: `main`
- Contract branch:
  `codex/parser-corpus-deck-summary-behavior-uplift-488`
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

- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- `docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md`
- `docs/contracts/parser_corpus_deck_summary_coverage.md`
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/contracts/parser_corpus_deck_upsert_coverage.md`
- `docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md`
- `docs/contracts/player_log_evidence_ledger_tier3_deck_state.md`
- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/collection.py`
- `tests/test_collection_parser.py`
- `tests/test_event_schema_snapshots.py`

## Purpose

Define the narrowest safe behavior-uplift boundary for
`deck_api.deck_summary`.

This contract answers:

- whether `deck_api.deck_summary` may be promoted from `covered_report_only`
  in this slice;
- whether `parser_behavior_verified` may be added from existing StartHook
  evidence;
- what evidence would be required before a future uplift can proceed;
- which fixture, manifest, session-ledger, parser, privacy, and readiness
  changes are forbidden; and
- how #388 / #381 activation remains deferred.

This contract does not implement code, create fixtures, edit corpus metadata,
run private/live MTGA checks, activate #388/#381, or claim deck-summary parser
support.

## Observed Current Behavior

Observed on `main` at
`a046b4550aae18a07a61cd8222ac2927ea930b6e`:

- Issue #488 is open.
- Tracker #158 remains open.
- Related pipeline tracker #388 remains open and deferred.
- Parent private-evidence issue #434 remains open.
- Issue #482 is complete after PR #487.
- The corpus parity report says:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=16, report_only=17, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Current applicability metrics:

```yaml
parser_behavior_ready: false
parser_behavior_applicability_ready: false
parser_behavior_applicable_family_count: 37
parser_behavior_applicable_ready_family_count: 21
parser_behavior_applicable_not_ready_family_count: 16
parser_behavior_not_applicable_family_count: 8
pipeline_activation_ready_for_issue_388: false
```

Current `deck_api.deck_summary` row:

```yaml
scenario_family: "deck_api.deck_summary"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "deck_summary_boundary_report_v1"
```

Current adjacent evidence:

- `deck_api.start_hook_deck_snapshot` is `covered_synthetic`.
- `deck_api.start_hook_deck_snapshot` already carries
  `parser_behavior_verified` through `start_hook_deck_snapshot_synthetic_v1`.
- `src/mythic_edge_parser/parsers/collection.py` recognizes `StartHook`
  responses and emits `Collection` and `DeckCollection` events.
- `DeckCollection` events are emitted only when list-shaped `DeckSummaries`
  and mapping-shaped `Decks` can be correlated by string `DeckId`.
- The parser preserves source evidence under `raw_start_hook`.
- Focused collection parser tests cover StartHook player cards, correlated
  deck summaries, raw evidence preservation, orphaned summaries, real
  StartHook-like shape, and malformed deck-summary entries.

Current non-evidence:

- There is no observed dedicated standalone deck-summary API parser.
- There is no observed independent `deck_api.deck_summary` golden replay
  fixture distinct from the StartHook deck snapshot fixture.
- There is no observed parser-owned event family dedicated only to deck-summary
  API behavior.
- There is no observed contract authority to treat StartHook `DeckSummaries`
  as both `deck_api.start_hook_deck_snapshot` behavior evidence and
  standalone `deck_api.deck_summary` behavior evidence.

## Scope Decision

Selected path: preserve `covered_report_only`.

Codex B considered these paths:

1. Promote `deck_api.deck_summary` to `covered_synthetic` from the existing
   StartHook `DeckSummaries` fixture evidence.
2. Keep `deck_api.deck_summary` as `covered_report_only` and document the
   behavior-uplift blocker.
3. Split or reframe the taxonomy before any behavior uplift.

Selected decision: option 2, with option 3 as the next prerequisite if the
project wants future behavior uplift.

Reasoning:

- Issue #392 already owns the safe synthetic behavior claim for
  `deck_api.start_hook_deck_snapshot`.
- Issue #394 already records `deck_api.deck_summary` as a report-only
  boundary because current evidence is StartHook-bound.
- Reusing the same StartHook fixture to add `parser_behavior_verified` to
  `deck_api.deck_summary` would double-count one parser behavior as two
  separate coverage claims.
- The row name `deck_api.deck_summary` can reasonably be read as a standalone
  deck-summary API family, but the current parser evidence is not standalone.
- A behavior uplift without a taxonomy split or new dedicated evidence would
  imply broader deck API support than Mythic Edge currently proves.

Therefore this contract does not authorize Codex C to add fixtures, mutate the
manifest/session ledger, or change `deck_api.deck_summary` status in #488.

## Owning Layer

Owning layer: Corpus / Provenance.

Supporting truth layers:

- Collection parsing owns StartHook `Collection` and `DeckCollection` event
  emission.
- StartHook deck snapshot corpus coverage owns the existing synthetic
  behavior-ready evidence for StartHook `DeckSummaries` plus `Decks`.
- Deck-summary corpus coverage owns the current report-only boundary row.
- Corpus parity reporting owns status aggregation and readiness metrics.

This contract does not move truth ownership to corpus metadata, workbook
formulas, dashboards, Apps Script, webhook transport, analytics, AI, coaching,
readiness, deploy, or production surfaces.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser, as the existing producer of StartHook collection/deck-collection
  facts.
- Quality / Governance, as the owner of validation and protected-surface
  discipline.

This slice is not analytics, AI, coaching, workbook, webhook, Apps Script,
local app, release readiness, production behavior, private evidence execution,
or parser-evidence pipeline activation.

## Truth Owner

Truth owner for current report-only status:

- `docs/contracts/parser_corpus_deck_summary_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for current StartHook behavior evidence:

- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `src/mythic_edge_parser/parsers/collection.py`
- `tests/test_collection_parser.py`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`

Truth boundary:

- StartHook `DeckSummaries` plus `Decks` behavior may prove
  `deck_api.start_hook_deck_snapshot`.
- The same StartHook behavior must not be reused as standalone
  `deck_api.deck_summary` parser-behavior evidence in this slice.
- `deck_api.deck_summary` must remain report-only until a later contract
  either splits the taxonomy or introduces distinct parser-owned evidence.
- Corpus coverage status is review metadata. It is not deck identity truth,
  submitted-deck truth, active-deck truth, sideboard-delta truth, collection
  ownership truth, inventory/economy truth, analytics truth, AI truth,
  coaching truth, release readiness, production behavior, full corpus parity,
  tracker-completion authority, or #388/#381 activation authority.

## Bridge-Code Status

`ambiguous_pending_follow_up`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Current allowed data flow:

```text
existing StartHook DeckSummaries parser/test evidence
  -> deck_api.start_hook_deck_snapshot behavior-ready row
  -> deck_api.deck_summary report-only boundary row
  -> corpus parity report non-claim metadata
```

Forbidden reverse flow:

- Corpus coverage status must not change StartHook parser behavior.
- Corpus metadata must not create, imply, or require a dedicated standalone
  deck-summary parser.
- Corpus metadata must not add `parser_behavior_verified` to
  `deck_api.deck_summary` from the StartHook snapshot fixture.
- Corpus metadata must not move private deck contents, deck identity,
  submitted-deck facts, decklist completion, analytics, AI, coaching, workbook,
  webhook, or Apps Script interpretation into parser truth.

Protected surfaces explicitly not touched:

- parser behavior
- StartHook parser behavior
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

- `docs/contracts/parser_corpus_deck_summary_behavior_uplift.md`

Files future roles may inspect:

- `docs/contracts/parser_corpus_deck_summary_coverage.md`
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/collection.py`
- `tests/test_collection_parser.py`
- `tests/test_event_schema_snapshots.py`

Files Codex C is not authorized to change from this contract:

- corpus manifest or session-ledger status for `deck_api.deck_summary`
- golden replay fixtures or manifests
- collection parser source
- collection parser tests
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
scenario_family: "deck_api.deck_summary"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "deck_summary_boundary_report_v1"
```

This contract does not authorize:

```yaml
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
```

for `deck_api.deck_summary` in issue #488.

## Future Behavior-Uplift Prerequisites

Future behavior uplift requires one of these prerequisite decisions.

### Option A: Taxonomy Split

A future Codex A/B issue may split the current ambiguous row into separate
coverage families, for example:

- `deck_api.start_hook_deck_summary_view`, meaning the bounded `DeckSummaries`
  view inside StartHook `DeckCollection`; and
- `deck_api.deck_summary_standalone`, meaning a distinct standalone
  deck-summary API response, if such a parser surface is ever owned.

If this split is accepted, the StartHook-bound family may cite #392 evidence.
The standalone family must remain unproven until distinct evidence exists.

### Option B: Dedicated Standalone Evidence

A future Codex A/B issue may authorize behavior uplift for
`deck_api.deck_summary` only if distinct owned evidence exists for a
standalone deck-summary API response.

Required future evidence would include:

- a dedicated parser route or clearly documented existing route for the
  standalone payload;
- accepted raw payload shape;
- emitted parser event family or explicitly bounded parser-owned output;
- malformed/partial payload behavior;
- raw evidence preservation expectations;
- focused tests for that behavior;
- corpus manifest/session-ledger entries distinct from
  `start_hook_deck_snapshot_synthetic_v1`; and
- explicit non-claims around deck identity, deck contents, submitted decks,
  inventory/economy, analytics, AI, coaching, readiness, and production truth.

### Option C: Preserve Report-Only Boundary

If neither prerequisite is selected, the current row remains
`covered_report_only`.

This is the selected path for #488.

## Behavior-Uplift Packet

This section is a reusable packet pattern for future behavior-uplift rows. In
this contract it applies only to `deck_api.deck_summary`. It must not be used
here to solve, promote, or reclassify any other corpus row.

| Question | Contracted answer for #488 |
| --- | --- |
| Scenario family | `deck_api.deck_summary` |
| Current status and basis | `covered_report_only` with `fixture_metadata_only` through `deck_summary_boundary_report_v1` |
| Target status, if any | No target status movement in #488; preserve `covered_report_only` |
| May `parser_behavior_verified` be added? | No, not from existing StartHook `DeckSummaries` evidence; future addition requires a taxonomy split or distinct standalone evidence under a new contract |
| Evidence type | Remain report-only in #488; future evidence may be synthetic or committed sanitized only if separately contracted; private-gated and external-gated evidence are forbidden in this lane |
| Fixture/golden replay changes | Forbidden in #488; do not add, mutate, or relabel fixtures for `deck_api.deck_summary` |
| Manifest/session-ledger changes | Forbidden in #488 except under a later contract; do not change status, basis, entries, readiness flags, or related counts for this row |
| Parser behavior changes | Forbidden; no collection parser, event-class, router, state, runtime, workbook, webhook, or analytics changes |
| Private/external inputs | Private Player.log, UTC_Log, live MTGA checks, Manasight/external raw corpora, decklists, deck names, card choices, strategy notes, and private reports are forbidden |
| Required non-claims | No standalone deck-summary API support, deck identity truth, submitted-deck truth, active-deck truth, sideboard-delta truth, collection ownership truth, inventory/economy truth, deck-upsert behavior, store/pack/inbox/crafting behavior, archetype truth, analytics truth, AI truth, coaching truth, private smoke, release readiness, production behavior, full corpus parity, tracker completion, or #388/#381 activation claims |
| Focused validation | Corpus parity report, corpus status inspection, docs check, diff check, path-scoped secret scan, path-scoped protected-surface scan |
| #388/#381 stop condition | Do not activate #388 or #381 from this row; preserving report-only status does not improve parser-behavior readiness counts |

Future behavior-uplift contracts may copy this packet shape, but each future
row still needs its own issue, contract, evidence decision, non-claims, and
validation plan.

## Explicit Non-Claims

This contract does not claim:

- `deck_api.deck_summary` parser behavior support;
- standalone deck-summary API support;
- new deck-summary fixture coverage;
- new deck-summary golden replay coverage;
- deck identity truth;
- submitted-deck truth;
- active-deck truth;
- sideboard-delta truth;
- collection ownership truth;
- inventory or economy truth;
- deck-upsert behavior;
- store, pack, inbox, crafting, wildcard, inventory, or economy coverage;
- exact live private deck contents;
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
- current `collection.py` parser implementation;
- focused collection parser and corpus parity tests;
- public GitHub issue/PR metadata for #392, #394, #482, #487, and #488.

Forbidden inputs:

- private Player.log excerpts;
- UTC_Log excerpts;
- live MTGA runs;
- local app-data or runtime artifacts;
- private smoke outputs;
- screenshots;
- Manasight raw logs, compressed corpus files, parser source, or external
  corpus contents;
- generated/private/runtime artifacts;
- SQLite files;
- workbook exports;
- secrets, credentials, tokens, API keys, or webhook URLs;
- private decklists, deck names, card choices, or strategy notes.

## Validation Obligations

Codex B validation for this contract should include:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json \
  --out /tmp/mythic_edge_issue_488_corpus_report.json
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_deck_summary_behavior_uplift.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_deck_summary_behavior_uplift.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

Codex E validation should verify:

- the contract preserves #394's report-only boundary;
- the contract does not authorize status movement for
  `deck_api.deck_summary`;
- the contract does not duplicate #392 behavior evidence;
- the contract does not authorize fixture, manifest, session-ledger, parser,
  workbook, webhook, Apps Script, analytics, AI, coaching, readiness, or
  production changes;
- the contract preserves #388/#381 activation gates;
- validation output is documented in
  `docs/contract_test_reports/parser_corpus_deck_summary_behavior_uplift.md`.

Codex C validation is not applicable unless a later contract authorizes
implementation.

## Acceptance Criteria

This contract is complete when:

- `docs/contracts/parser_corpus_deck_summary_behavior_uplift.md` exists;
- observed current behavior is separated from required guarantees;
- the status decision preserves `covered_report_only`;
- the contract explains why existing StartHook evidence cannot add
  `parser_behavior_verified` to `deck_api.deck_summary`;
- future prerequisite paths are explicit;
- the behavior-uplift packet is included but scoped only to this row;
- protected surfaces and non-claims are explicit;
- validation expectations are listed; and
- the workflow handoff routes away from Codex C unless new implementation
  authority is created.

## Recommended Next Role

Recommended next role: Codex E: Module Reviewer.

Reason: #488 produces a contract that intentionally does not authorize Codex C
implementation. The next useful step is review/contract-test validation. If
the project wants behavior uplift later, Codex A should frame a follow-up issue
for either a taxonomy split or dedicated standalone deck-summary evidence.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #488.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/488

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/482

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/487

Previous merge commit:
a046b4550aae18a07a61cd8222ac2927ea930b6e

Prior deck-summary boundary:
https://github.com/Tahjali11/Mythic-Edge/issues/394

Related StartHook boundary:
https://github.com/Tahjali11/Mythic-Edge/issues/392

Contract under review:
docs/contracts/parser_corpus_deck_summary_behavior_uplift.md

Goal:
Review the #488 contract and produce
docs/contract_test_reports/parser_corpus_deck_summary_behavior_uplift.md.

Verify that the contract preserves `deck_api.deck_summary` as
`covered_report_only`, does not authorize `parser_behavior_verified`, does not
double-count StartHook `DeckSummaries` evidence from #392, does not authorize
fixtures or corpus status changes, and keeps #388/#381 activation deferred.

Do not implement code.
Do not open a PR unless explicitly instructed.
Do not close #158, #388, #434, or #488.
Do not change corpus statuses, fixtures, parser behavior, workbook/webhook/App
Script behavior, analytics truth, AI truth, coaching truth, release readiness,
production behavior, or final integration policy.
Do not claim standalone deck-summary API support or full corpus parity.

Expected output:
- Contract-test report
- Verdict: ready for no-op/defer, needs contract clarification, or route to
  Codex A for taxonomy/evidence split
- Validation evidence
- workflow_handoff block
```

If implementation is later desired, use Codex A first to frame one of:

- taxonomy split for StartHook-bound deck-summary view versus standalone
  deck-summary API; or
- dedicated standalone deck-summary parser evidence.

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/488"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/482"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/487"
  previous_merge_commit: "a046b4550aae18a07a61cd8222ac2927ea930b6e"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/394"
  related_start_hook_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/392"
  completed_thread: "B"
  next_thread: "E"
  verdict: "deck_summary_behavior_uplift_deferred_report_only_boundary_preserved"
  risk_tier: "High"
  branch: "codex/parser-corpus-deck-summary-behavior-uplift-488"
  base_branch: "main"
  selected_family: "deck_api.deck_summary"
  current_status: "covered_report_only"
  selected_path: "preserve_report_only_taxonomy_or_distinct_evidence_required_before_behavior_uplift"
  target_artifact: "docs/contract_test_reports/parser_corpus_deck_summary_behavior_uplift.md"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  stop_conditions:
    - "Do not target main directly unless explicitly approved."
    - "Do not close tracker #158, pipeline tracker #388, parent issue #434, or issue #488."
    - "Do not activate #388 or #381."
    - "Do not promote deck_api.deck_summary or add parser_behavior_verified from StartHook evidence."
    - "Do not claim standalone deck-summary API support, parser support, readiness, production behavior, analytics truth, AI truth, coaching truth, full corpus parity, or tracker completion."
```
