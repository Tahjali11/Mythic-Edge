# Parser Corpus Store Pack Inbox Crafting Behavior Framing Contract

## Module

`deck_api.store_pack_inbox_or_crafting` parser corpus behavior readiness
framing.

Plain English: Mythic Edge already records
`deck_api.store_pack_inbox_or_crafting` as a report-only corpus boundary from
issue #398. This contract decides whether that broad combined row can safely
move toward parser-behavior readiness from current inventory evidence. The
answer for this slice is no: current Mythic Edge evidence covers a narrow
StartHook `InventoryInfo` snapshot parser surface, but it does not prove store
API parsing, pack-opening parsing, inbox/reward parsing, crafting or wildcard
truth, transactions, economy behavior, collection ownership, account-state
truth, release readiness, production behavior, analytics truth, AI truth, or
coaching truth.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/492
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/490
- Previous completed PR: https://github.com/Tahjali11/Mythic-Edge/pull/491
- Previous merge commit: `3e2305b6efe2e7ed2cd73d93c45ceefd7c7b8bfb`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/398
- Base branch inspected: `main`
- Contract branch:
  `codex/parser-corpus-store-pack-inbox-crafting-behavior-framing-492`
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
- `docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md`
- `docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md`
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/contracts/parser_client_actions.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/inventory.py`
- `tests/test_parser_small_modules.py`

## Purpose

Define the narrowest safe readiness framing for the combined
`deck_api.store_pack_inbox_or_crafting` row.

This contract answers:

- whether the combined row may be promoted from `covered_report_only` in this
  slice;
- whether `parser_behavior_verified` may be added from current
  `InventoryInfo` snapshot parsing;
- whether the combined row should be split before future behavior work;
- what distinct evidence would be required before a future narrow uplift can
  proceed;
- which fixture, manifest, session-ledger, parser, privacy, and readiness
  changes are forbidden; and
- how #388 / #381 activation remains deferred.

This contract does not implement code, create fixtures, edit corpus metadata,
run private/live MTGA checks, activate #388/#381, or claim store, pack, inbox,
crafting, wildcard, transaction, reward, account, collection, economy, or
inventory parser support beyond the existing bounded `InventoryInfo` parser.

## Observed Current Behavior

Observed on `main` at
`3e2305b6efe2e7ed2cd73d93c45ceefd7c7b8bfb`:

- Issue #492 is open.
- Tracker #158 remains open.
- Related pipeline tracker #388 remains open and deferred.
- Parent private-evidence issue #434 remains open.
- Issue #490 is complete after PR #491.
- The corpus parity report says:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=16, report_only=17, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Current `deck_api.store_pack_inbox_or_crafting` row:

```yaml
scenario_family: "deck_api.store_pack_inbox_or_crafting"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "store_pack_inbox_crafting_boundary_report_v1"
parser_event_families: []
parser_claim_families:
  - "store_pack_inbox_crafting_boundary_report"
  - "inventory_info_reference_only"
  - "store_api_not_claimed"
  - "pack_inbox_crafting_not_claimed"
  - "inventory_economy_privacy_boundary"
```

Current adjacent parser evidence:

- `src/mythic_edge_parser/parsers/inventory.py` recognizes `StartHook`
  responses with mapping-shaped `InventoryInfo`.
- Successful inventory parses emit an `Inventory` event with
  `payload["type"] == "inventory_snapshot"`.
- The parser preserves the inventory payload and `raw_start_hook`.
- Focused tests assert mapping-shaped `InventoryInfo` is accepted, missing
  `InventoryInfo` returns `None`, and non-mapping `InventoryInfo` returns
  `None`.

Current non-evidence:

- There is no observed store API parser route.
- There is no observed pack-opening parser route.
- There is no observed inbox or reward parser route.
- There is no observed crafting or wildcard parser route.
- There is no observed transaction or economy parser route.
- There is no observed parser-owned collection ownership, account-state,
  currency-balance, pack inventory, inbox-content, crafting-choice, or
  wildcard truth model.
- The current corpus row has no parser event families.
- The current session ledger records dedicated pack/inbox/crafting events and
  dedicated economy parser routes as zero.

## Scope Decision

Selected path: preserve `covered_report_only` and require future splitting or
dedicated evidence before behavior uplift.

Codex B considered these paths:

1. Promote the combined row to `covered_synthetic` from current `InventoryInfo`
   parser evidence.
2. Keep the combined row as `covered_report_only` and document the
   behavior-readiness blocker.
3. Split the combined row into narrower future issue families before any
   behavior work.
4. Defer the combined row entirely until private/live/economy evidence is
   authorized.

Selected decision: option 2 now, with option 3 as the required future
framing route if the project wants behavior uplift.

Reasoning:

- Issue #398 already records the combined row as a report-only blind-spot
  boundary.
- Current inventory parsing is too narrow to support the broad combined row.
- A synthetic fixture for the combined row would risk implying account,
  economy, store, pack, inbox, reward, crafting, wildcard, or transaction
  behavior that Mythic Edge does not own.
- The combined family hides multiple distinct surfaces that should not share
  one behavior-readiness proof.
- A narrower future row for bounded `InventoryInfo` snapshots may be possible,
  but that is not the same as proving store/pack/inbox/crafting behavior.

Therefore this contract does not authorize Codex C to add fixtures, mutate the
manifest/session ledger, or change
`deck_api.store_pack_inbox_or_crafting` status in #492.

## Owning Layer

Owning layer: Corpus / Provenance.

Supporting truth layers:

- Inventory parsing owns current StartHook `InventoryInfo` snapshot event
  emission.
- Corpus parity reporting owns status aggregation and readiness metrics.
- Quality / Governance owns protected-surface discipline and next-role
  routing.

This contract does not move truth ownership to corpus metadata, workbook
formulas, dashboards, Apps Script, webhook transport, analytics, AI, coaching,
readiness, deploy, or production surfaces.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser, as the producer of the existing bounded `Inventory` event.
- Quality / Governance, as the owner of validation and protected-surface
  discipline.

This slice is not analytics, AI, coaching, workbook, webhook, Apps Script,
local app, release readiness, production behavior, private evidence execution,
store/economy runtime integration, or parser-evidence pipeline activation.

## Truth Owner

Truth owner for current report-only status:

- `docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for current bounded inventory parser evidence:

- `src/mythic_edge_parser/parsers/inventory.py`
- `tests/test_parser_small_modules.py`

Truth boundary:

- StartHook `InventoryInfo` parsing may prove only bounded inventory snapshot
  recognition.
- Bounded inventory snapshot parsing must not be reused as store, pack, inbox,
  reward, crafting, wildcard, transaction, account, collection ownership, or
  economy parser-behavior evidence in this slice.
- The combined `deck_api.store_pack_inbox_or_crafting` row must remain
  report-only until a later contract splits the row or introduces distinct
  parser-owned evidence for a narrow sub-surface.
- Corpus coverage status is review metadata. It is not account-state truth,
  currency-balance truth, pack-inventory truth, inbox-content truth,
  crafting-choice truth, wildcard truth, collection ownership truth, card
  ownership truth, deck identity truth, submitted-deck truth, analytics truth,
  AI truth, coaching truth, release readiness, production behavior, full
  corpus parity, tracker-completion authority, or #388/#381 activation
  authority.

## Bridge-Code Status

`ambiguous_pending_follow_up`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Current allowed data flow:

```text
existing StartHook InventoryInfo parser/test evidence
  -> deck_api.store_pack_inbox_or_crafting report-only boundary row
  -> corpus parity report non-claim metadata
```

Forbidden reverse flow:

- Corpus coverage status must not change inventory parser behavior.
- Corpus metadata must not create, imply, or require store, pack, inbox,
  crafting, reward, transaction, wildcard, collection, account, or economy API
  parsers.
- Corpus metadata must not add `parser_behavior_verified` to the combined row
  from `InventoryInfo` evidence.
- Corpus metadata must not reclassify StartHook deck snapshots, deck-summary,
  deck-upsert, event-set deck, submit-deck, submitted-deck-card, inventory, or
  collection evidence as store/pack/inbox/crafting behavior.
- Corpus metadata must not move private economy or account facts, deck
  contents, collection ownership, analytics, AI, coaching, workbook, webhook,
  or Apps Script interpretation into parser truth.

Protected surfaces explicitly not touched:

- parser behavior
- inventory parser behavior
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
- runtime inventory/account artifacts
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

- `docs/contracts/parser_corpus_store_pack_inbox_crafting_behavior_framing.md`

Files future roles may inspect:

- `docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md`
- `docs/contracts/parser_corpus_deck_summary_behavior_uplift.md`
- `docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md`
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/contracts/parser_client_actions.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/inventory.py`
- `tests/test_parser_small_modules.py`

Files Codex C is not authorized to change from this contract:

- corpus manifest or session-ledger status for
  `deck_api.store_pack_inbox_or_crafting`
- golden replay fixtures or manifests
- inventory parser source
- inventory parser tests
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
scenario_family: "deck_api.store_pack_inbox_or_crafting"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "store_pack_inbox_crafting_boundary_report_v1"
```

This contract does not authorize:

```yaml
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
```

for `deck_api.store_pack_inbox_or_crafting` in issue #492.

## Future Framing Paths

Future behavior work requires one of these prerequisite decisions.

### Option A: Split The Combined Row

A future Codex A/B issue may split or supplement the combined taxonomy with
narrower issue families, for example:

- bounded `InventoryInfo` snapshot recognition;
- store API response parsing;
- pack-opening parsing;
- inbox or reward parsing;
- crafting or wildcard parsing;
- transaction or economy parsing;
- collection ownership or account-state parsing.

Each future surface needs its own issue, contract, evidence decision,
protected-surface list, privacy posture, and non-claims. A fixture for one
surface must not promote the entire combined row unless the contract explicitly
authorizes that status semantics.

### Option B: Dedicated Narrow Evidence

A future Codex A/B issue may authorize behavior uplift for one narrow
sub-surface only if distinct owned evidence exists.

Required future evidence would include:

- a dedicated parser route or clearly documented existing route for that
  surface;
- accepted raw payload shape;
- emitted parser event family or explicitly bounded parser-owned output;
- malformed/partial payload behavior;
- raw evidence preservation expectations;
- focused tests for that behavior;
- corpus manifest/session-ledger entries distinct from
  `store_pack_inbox_crafting_boundary_report_v1`; and
- explicit non-claims around account state, private economy values, collection
  ownership, card ownership, rewards, currency balances, analytics, AI,
  coaching, readiness, and production truth.

### Option C: Preserve Report-Only Boundary

If neither prerequisite is selected, the current combined row remains
`covered_report_only`.

This is the selected path for #492.

## Behavior-Framing Packet

This section is a reusable packet pattern for broad combined rows that need
framing before behavior uplift. In this contract it applies only to
`deck_api.store_pack_inbox_or_crafting`. It must not be used here to solve,
promote, or reclassify any other corpus row.

| Question | Contracted answer for #492 |
| --- | --- |
| Scenario family | `deck_api.store_pack_inbox_or_crafting` |
| Current status and basis | `covered_report_only` with `fixture_metadata_only` through `store_pack_inbox_crafting_boundary_report_v1` |
| Target status, if any | No target status movement in #492; preserve `covered_report_only` |
| May `parser_behavior_verified` be added? | No, not from current `InventoryInfo` snapshot evidence; future addition requires a split/narrow sub-surface or dedicated evidence under a new contract |
| Evidence type | Remain report-only in #492; future evidence may be synthetic or committed sanitized only for a narrow separately contracted surface; private-gated and external-gated evidence are forbidden in this lane |
| Fixture/golden replay changes | Forbidden in #492; do not add, mutate, or relabel fixtures for the combined row |
| Manifest/session-ledger changes | Forbidden in #492 except under a later contract; do not change status, basis, entries, readiness flags, or related counts for this row |
| Parser behavior changes | Forbidden; no inventory parser, event-class, router, state, runtime, workbook, webhook, store/economy, or analytics changes |
| Private/external inputs | Private Player.log, UTC_Log, live MTGA checks, live store/pack/inbox/crafting checks, Manasight/external raw corpora, account data, currency balances, pack inventories, inbox contents, crafting choices, collection ownership data, decklists, deck names, card choices, strategy notes, and private reports are forbidden |
| Required non-claims | No store API support, pack-opening support, inbox/reward support, crafting/wildcard truth, transaction truth, economy truth, account-state truth, collection ownership truth, currency-balance truth, pack-inventory truth, card-ownership truth, deck identity truth, submitted-deck truth, sideboard truth, archetype truth, analytics truth, AI truth, coaching truth, private smoke, release readiness, production behavior, full corpus parity, tracker completion, or #388/#381 activation claims |
| Focused validation | Corpus parity report, corpus status inspection, docs check, diff check, path-scoped secret scan, path-scoped protected-surface scan |
| #388/#381 stop condition | Do not activate #388 or #381 from this row; preserving report-only status does not improve parser-behavior readiness counts |

Future behavior-framing contracts may copy this packet shape, but each future
row still needs its own issue, contract, evidence decision, non-claims, and
validation plan.

## Explicit Non-Claims

This contract does not claim:

- `deck_api.store_pack_inbox_or_crafting` parser behavior support;
- broad inventory or economy support;
- store API support;
- pack-opening parser support;
- inbox or reward parser support;
- crafting or wildcard truth;
- transaction truth;
- account-state truth;
- collection ownership truth;
- currency-balance truth;
- pack-inventory truth;
- inbox-content truth;
- card-ownership truth;
- deck identity truth;
- submitted-deck truth;
- sideboard-delta truth;
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
- current inventory parser implementation and focused tests;
- public GitHub issue/PR metadata for #398, #490, #491, and #492.

Forbidden inputs:

- private Player.log excerpts;
- UTC_Log excerpts;
- live MTGA runs;
- live deck API, store, pack, inbox, crafting, reward, economy, or network
  checks;
- local app-data or runtime artifacts;
- private smoke outputs;
- screenshots;
- Manasight raw logs, compressed corpus files, parser source, or external
  corpus contents;
- generated/private/runtime artifacts;
- SQLite files;
- workbook exports;
- secrets, credentials, tokens, API keys, or webhook URLs;
- private decklists, deck names, card choices, collection data, account data,
  currency balances, pack inventories, inbox contents, crafting choices, or
  strategy notes.

## Validation Obligations

Codex B validation for this contract should include:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json \
  --out /tmp/mythic_edge_issue_492_corpus_report.json
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_store_pack_inbox_crafting_behavior_framing.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_store_pack_inbox_crafting_behavior_framing.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

Codex E validation should verify:

- the contract preserves #398's report-only boundary;
- the contract does not authorize status movement for the combined row;
- the contract does not authorize `parser_behavior_verified`;
- the contract does not reclassify `InventoryInfo`, StartHook deck snapshots,
  deck-summary, deck-upsert, event-set deck, submit-deck, submitted-deck-card,
  inventory, or collection evidence as store/pack/inbox/crafting behavior;
- the contract routes future behavior work through split or narrow follow-up
  issues;
- the contract does not authorize fixture, manifest, session-ledger, parser,
  workbook, webhook, Apps Script, analytics, AI, coaching, readiness, or
  production changes;
- the contract preserves #388/#381 activation gates;
- validation output is documented in
  `docs/contract_test_reports/parser_corpus_store_pack_inbox_crafting_behavior_framing.md`.

Codex C validation is not applicable unless a later contract authorizes
implementation.

## Acceptance Criteria

This contract is complete when:

- `docs/contracts/parser_corpus_store_pack_inbox_crafting_behavior_framing.md`
  exists;
- observed current behavior is separated from required guarantees;
- the status decision preserves `covered_report_only`;
- the contract explains why bounded `InventoryInfo` snapshot evidence cannot
  add `parser_behavior_verified` to the combined row;
- future split/narrow prerequisite paths are explicit;
- the behavior-framing packet is included but scoped only to this row;
- protected surfaces and non-claims are explicit;
- validation expectations are listed; and
- the workflow handoff routes away from Codex C unless new implementation
  authority is created.

## Recommended Next Role

Recommended next role: Codex E: Module Reviewer.

Reason: #492 produces a contract that intentionally does not authorize Codex C
implementation. The next useful step is review/contract-test validation. If
the project wants behavior uplift later, Codex A should frame a follow-up issue
for splitting this combined row or for one narrow dedicated sub-surface.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #492.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/492

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/490

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/491

Previous merge commit:
3e2305b6efe2e7ed2cd73d93c45ceefd7c7b8bfb

Prior store/pack/inbox/crafting boundary:
https://github.com/Tahjali11/Mythic-Edge/issues/398

Contract under review:
docs/contracts/parser_corpus_store_pack_inbox_crafting_behavior_framing.md

Goal:
Review the #492 contract and produce
docs/contract_test_reports/parser_corpus_store_pack_inbox_crafting_behavior_framing.md.

Verify that the contract preserves `deck_api.store_pack_inbox_or_crafting` as
`covered_report_only`, does not authorize `parser_behavior_verified`, does not
reclassify bounded InventoryInfo snapshot evidence as store, pack, inbox,
reward, crafting, wildcard, transaction, economy, account, or collection
behavior, does not authorize fixtures or corpus status changes, and keeps
#388/#381 activation deferred.

Do not implement code.
Do not open a PR unless explicitly instructed.
Do not close #158, #388, #434, or #492.
Do not change corpus statuses, fixtures, parser behavior, workbook/webhook/App
Script behavior, analytics truth, AI truth, coaching truth, release readiness,
production behavior, or final integration policy.
Do not claim store/pack/inbox/crafting parser support or full corpus parity.

Expected output:
- Contract-test report
- Verdict: ready for no-op/defer, needs contract clarification, or route to
  Codex A for split/narrow evidence framing
- Validation evidence
- workflow_handoff block
```

If implementation is later desired, use Codex A first to frame one of:

- split taxonomy/follow-up surfaces for this broad row; or
- dedicated narrow inventory/store/pack/inbox/crafting/economy evidence.

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/492"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/490"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/491"
  previous_merge_commit: "3e2305b6efe2e7ed2cd73d93c45ceefd7c7b8bfb"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/398"
  completed_thread: "B"
  next_thread: "E"
  verdict: "store_pack_inbox_crafting_behavior_framing_preserve_report_only_split_required_before_uplift"
  risk_tier: "High"
  branch: "codex/parser-corpus-store-pack-inbox-crafting-behavior-framing-492"
  base_branch: "main"
  selected_family: "deck_api.store_pack_inbox_or_crafting"
  current_status: "covered_report_only"
  selected_path: "preserve_report_only_split_or_dedicated_narrow_evidence_required_before_behavior_uplift"
  target_artifact: "docs/contract_test_reports/parser_corpus_store_pack_inbox_crafting_behavior_framing.md"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  stop_conditions:
    - "Do not target main directly unless explicitly approved."
    - "Do not close tracker #158, pipeline tracker #388, parent issue #434, or issue #492."
    - "Do not activate #388 or #381."
    - "Do not promote deck_api.store_pack_inbox_or_crafting or add parser_behavior_verified from InventoryInfo evidence."
    - "Do not claim store, pack, inbox, reward, crafting, wildcard, transaction, economy, account, collection ownership, readiness, production behavior, analytics truth, AI truth, coaching truth, full corpus parity, or tracker completion."
```
