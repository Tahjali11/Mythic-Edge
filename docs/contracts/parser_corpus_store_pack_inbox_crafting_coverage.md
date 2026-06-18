# Parser Corpus Store Pack Inbox Crafting Coverage Contract

## Module

Store, pack, inbox, and crafting corpus evidence boundary for the parser
corpus parity report.

Plain English: this slice lets Mythic Edge account for exactly
`deck_api.store_pack_inbox_or_crafting` as a report-only corpus boundary. It
does not claim store API parsing, pack-opening parsing, inbox/reward parsing,
crafting or wildcard truth, inventory/economy truth, collection ownership, or
account-state truth. Current `InventoryInfo` StartHook parsing is adjacent
evidence only: it proves a bounded inventory snapshot parser surface, not the
broader store/pack/inbox/crafting scenario family.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/398
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/396
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/397
- Previous merge commit:
  `da8b3f66692ac0c8aa60544c4380dd9bc0c4f17c`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-store-pack-inbox-crafting-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `da8b3f66692ac0c8aa60544c4380dd9bc0c4f17c`
- target_artifact:
  `docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_store_pack_inbox_crafting_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_store_pack_inbox_crafting_coverage.md`
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
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/contracts/parser_corpus_deck_summary_coverage.md`
- `docs/contracts/parser_corpus_deck_upsert_coverage.md`
- `docs/implementation_handoffs/parser_corpus_deck_upsert_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_deck_upsert_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/inventory.py`
- `tests/test_parser_small_modules.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, source records, hash lists,
  byte-size row lists, capture-date row lists, parser source, store examples,
  economy examples, deck examples, account examples, or external corpus
  contents.

## Scope Decision

Implementation may proceed as report-only boundary coverage.

Codex B considered these paths:

1. Safe synthetic coverage.
2. Report-only boundary coverage.
3. Evidence-prerequisite or deferred status.

Selected path: report-only boundary coverage.

Reasoning:

- The repo has a narrow inventory parser:
  `src/mythic_edge_parser/parsers/inventory.py` recognizes StartHook responses
  with mapping-shaped `InventoryInfo` and emits `Inventory` events with
  `type == "inventory_snapshot"`.
- Focused tests in `tests/test_parser_small_modules.py` prove only that
  mapping-shaped `InventoryInfo` payloads are accepted and non-mapping or
  missing `InventoryInfo` payloads are ignored.
- That evidence does not prove store API parsing, pack-opening parsing,
  inbox/reward parsing, crafting/wildcard truth, transactions, collection
  ownership, account state, or broad inventory/economy support.
- A synthetic `deck_api.store_pack_inbox_or_crafting` fixture would overclaim
  support for a combined external-reference category that current Mythic Edge
  parser behavior does not own.
- Leaving the row as plain `missing` hides the useful boundary decision that
  Mythic Edge has inspected the family and intentionally refuses to conflate
  StartHook `InventoryInfo` snapshots with store/pack/inbox/crafting support.
- A pure deferred status would be accurate but less useful than a committed
  report-only boundary because the row is a known blind spot with explicit
  privacy and non-claim rules.

This decision records `deck_api.store_pack_inbox_or_crafting` as a report-only
corpus boundary. It changes corpus parity metadata and tests only; it does not
change parser behavior.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the
`deck_api.store_pack_inbox_or_crafting` scenario family. Parser modules own
their current inventory parsing behavior. Runtime surfaces, analytics,
workbook outputs, and AI/coaching surfaces remain downstream consumers and
must not own this coverage claim.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance
validation evidence. It is not a Parser behavior module and is not a runtime,
workbook, webhook, Apps Script, Google Sheets, analytics, local app, AI,
coaching, release, or production module.

## Truth Owner

Truth owner for `deck_api.store_pack_inbox_or_crafting` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Related parser truth owners that must not be reclassified by this contract:

- `src/mythic_edge_parser/parsers/inventory.py` owns StartHook
  `InventoryInfo` inventory snapshot parsing.
- `tests/test_parser_small_modules.py` owns focused inventory parser behavior
  expectations.
- Parser event classes own the current `Inventory` event kind and payload
  shape.

Truth boundary:

- `InventoryInfo` snapshot parsing is a bounded parser surface.
- Store, pack, inbox, crafting, reward, transaction, wildcard, collection
  ownership, account state, and economy state support are not currently
  claimed by this scenario-family row.
- `deck_api.start_hook_deck_snapshot` remains synthetic StartHook deck
  snapshot coverage.
- `deck_api.deck_summary` remains report-only boundary metadata.
- `deck_api.deck_upsert` remains report-only boundary metadata.
- `deck_api.event_set_deck` remains covered committed evidence.
- This contract owns only the report-only store/pack/inbox/crafting boundary
  row: Mythic Edge has no current dedicated store, pack, inbox, crafting,
  reward, transaction, or economy API parser claim.
- Corpus coverage status is review metadata. It is not account-state truth,
  currency-balance truth, pack-inventory truth, inbox/reward truth,
  crafting-choice truth, wildcard truth, collection ownership truth, deck
  identity truth, submitted-deck truth, match/game truth, analytics truth, AI
  truth, coaching truth, merge readiness, deploy readiness, release readiness,
  production behavior, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing InventoryInfo parser/test evidence and deck API boundary docs
  -> bounded committed report-only manifest/session-ledger metadata
  -> corpus parity boundary row for deck_api.store_pack_inbox_or_crafting
```

Forbidden reverse flow:

- Corpus coverage status must not change inventory parser behavior.
- Corpus metadata must not create, imply, or require store, pack, inbox,
  crafting, reward, transaction, wildcard, collection, account, or economy API
  parsers.
- Corpus metadata must not rename or reclassify the existing deck API families.
- Corpus metadata must not change `Inventory` event payload shape, event
  classes, runtime artifacts, workbook output, webhook output, Apps Script
  behavior, analytics, AI, coaching, release policy, or production behavior.
- Corpus metadata must not turn `InventoryInfo` evidence into a claim about
  live private currency balances, pack inventories, inbox contents, crafting
  choices, collection ownership, card ownership, deck identity, account state,
  economy transactions, archetypes, strategy, or gameplay advice.

Protected surfaces explicitly not touched:

- parser behavior
- inventory parser behavior
- parser event classes
- parser state final reconciliation
- router semantics
- match/game identity
- deduplication
- diagnostics report shape
- drift report behavior
- golden replay behavior
- feature-equity behavior
- evidence-ledger behavior
- runtime surfaces
- local active-deck, inventory, collection, or account artifacts
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

- `docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_store_pack_inbox_crafting_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_store_pack_inbox_crafting_coverage.md`

Files Codex C may inspect but must not change unless it routes back for a
contract clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/inventory.py`
- `tests/test_parser_small_modules.py`
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/contracts/parser_corpus_deck_summary_coverage.md`
- `docs/contracts/parser_corpus_deck_upsert_coverage.md`
- `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- inventory parser semantics changes
- store, pack, inbox, crafting, reward, transaction, wildcard, collection,
  account, or economy parser implementation
- workbook inventory/economy field changes
- runtime inventory/account artifact changes
- StartHook deck snapshot coverage changes
- deck-summary coverage changes
- deck-upsert coverage changes
- event-set deck coverage changes

## Public Interface

The public interface is the corpus parity report generated from:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

No parser API, runtime API, workbook API, webhook payload, Apps Script entry
point, Google Sheets surface, analytics schema, Match Journal schema, overlay
API, local app route, OpenAI/model-provider API, or production interface is
changed by this contract.

## Observed Current Behavior

Observed from the issue and current repo state:

- Issue #398 is open and routed to Codex B for contract writing.
- Tracker #158 remains open.
- PR #397 merged issue #396 into `codex/parser-parity` at
  `da8b3f66692ac0c8aa60544c4380dd9bc0c4f17c`.
- The current corpus parity report returns
  `partial_coverage_map_ready (45 families, 6 committed, 13 missing)`.
- The current corpus parity matrix reports
  `deck_api.start_hook_deck_snapshot` as `covered_synthetic`.
- The current corpus parity matrix reports `deck_api.deck_summary` as
  `covered_report_only`.
- The current corpus parity matrix reports `deck_api.deck_upsert` as
  `covered_report_only`.
- The current corpus parity matrix reports `deck_api.event_set_deck` as
  `covered_committed`.
- The current corpus parity matrix reports
  `deck_api.store_pack_inbox_or_crafting` as `missing` with
  `coverage_basis == ["external_reference_only"]` and no Mythic Edge entries.
- `inventory.try_parse(...)` recognizes StartHook `InventoryInfo` only when it
  is mapping-shaped and emits an `Inventory` event with
  `payload["type"] == "inventory_snapshot"`.
- Focused inventory tests assert mapping-shaped `InventoryInfo` is accepted,
  missing `InventoryInfo` returns `None`, and non-mapping `InventoryInfo`
  returns `None`.
- No inspected contract or test authorizes treating `InventoryInfo` snapshots
  as store, pack, inbox, crafting, reward, transaction, wildcard, collection
  ownership, or economy API support.

## Required Guarantees

Codex C must preserve these guarantees:

- The only scenario family whose corpus parity status may change in this slice
  is `deck_api.store_pack_inbox_or_crafting`.
- `deck_api.store_pack_inbox_or_crafting` must become
  `covered_report_only`, not `covered_committed` or `covered_synthetic`.
- `coverage_basis` for the new boundary must be exactly
  `["fixture_metadata_only"]` unless Codex C routes back for contract
  clarification.
- `parser_behavior_verified` must not be used for
  `deck_api.store_pack_inbox_or_crafting` in this slice.
- The new manifest entry must have no parser event families.
- The new manifest entry must state that store, pack, inbox, crafting, reward,
  transaction, wildcard, collection, account, and economy API behavior is not
  claimed.
- The new manifest entry must explicitly reject using `InventoryInfo`,
  StartHook deck snapshot, deck summary, deck upsert, event-set deck, or
  submit-deck evidence as proof of store/pack/inbox/crafting parser support.
- Existing rows for `deck_api.start_hook_deck_snapshot`,
  `deck_api.deck_summary`, `deck_api.deck_upsert`, and
  `deck_api.event_set_deck` must retain their existing semantic boundaries.
- No raw private evidence, external corpus contents, private economy/account
  data, currency balances, pack inventories, inbox contents, crafting choices,
  collection ownership data, private decklists, private deck names, card
  choices, strategy notes, generated artifacts, runtime artifacts, SQLite
  files, workbook exports, credentials, tokens, keys, or webhook endpoints may
  be committed or reproduced.

## Authorized Manifest Entry

Codex C should add one report-only manifest entry with this intended shape:

```yaml
entry_id: "store_pack_inbox_crafting_boundary_report_v1"
title: "Store pack inbox crafting boundary report"
entry_type: "session_ledger_entry"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
scenario_families:
  - "deck_api.store_pack_inbox_or_crafting"
parser_event_families: []
parser_claim_families:
  - "store_pack_inbox_crafting_boundary_report"
  - "inventory_info_reference_only"
  - "store_api_not_claimed"
  - "pack_inbox_crafting_not_claimed"
  - "inventory_economy_privacy_boundary"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
linked_issues:
  - "https://github.com/Tahjali11/Mythic-Edge/issues/398"
authorized_by_contract:
  - "docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md"
```

Expected known gap language:

- Store/pack/inbox/crafting coverage is report-only boundary metadata.
- Mythic Edge has bounded `InventoryInfo` snapshot parsing, but that does not
  prove store API parsing, pack-opening parsing, inbox/reward parsing,
  crafting/wildcard truth, transactions, collection ownership, account state,
  or broad inventory/economy support.
- The entry does not prove currency balances, pack inventory, inbox contents,
  crafting choices, collection ownership, card ownership, deck identity,
  submitted-deck truth, sideboard-delta truth, inventory/economy truth,
  analytics truth, AI truth, coaching truth, release readiness, or production
  behavior.

Expected review-note language:

- The row is intentionally report-only.
- It prevents false parity claims by documenting why `InventoryInfo` and
  adjacent deck API evidence are not store/pack/inbox/crafting evidence.
- Future dedicated coverage remains blocked until Mythic Edge has owned,
  sanitized, parser-supported evidence for a narrower store, pack, inbox,
  reward, crafting, transaction, or economy surface.

## Authorized Session-Ledger Entry

Codex C should add one session-ledger entry with this intended shape:

```yaml
session_id: "store_pack_inbox_crafting_boundary_report_v1"
title: "Store pack inbox crafting boundary report"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/398"
authorized_by_contract: "docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md"
scenario_families:
  - "deck_api.store_pack_inbox_or_crafting"
format_family: "deck_api"
match_shape: "store_pack_inbox_crafting_boundary_report_only"
record_summary: "committed_store_pack_inbox_crafting_boundary_metadata_only"
parser_coverage:
  event_families: {}
  unknown_entries: 0
  truncation_count: 0
  inventory_info_reference_entries: 1
  dedicated_store_api_events: 0
  dedicated_pack_inbox_crafting_events: 0
  dedicated_economy_parser_routes: 0
game_rows:
  count: 0
  result_shape: "not_applicable"
```

The exact numeric reference counts may be adjusted only if Codex C documents
the observed repo evidence in the implementation handoff. Dedicated store,
pack, inbox, crafting, reward, transaction, wildcard, collection, account, or
economy API event and parser-route counts must remain zero in this slice.

Required report-only redactions:

```yaml
raw_log_lines_included: false
private_paths_included: false
raw_payloads_included: false
external_logs_included: false
decklists_included: false
private_deck_names_included: false
private_collection_data_included: false
private_economy_data_included: false
currency_balances_included: false
pack_inventory_included: false
inbox_contents_included: false
crafting_choices_included: false
```

## Expected Corpus Report Change

After Codex C, the matrix row for
`deck_api.store_pack_inbox_or_crafting` should be:

```yaml
scenario_family: "deck_api.store_pack_inbox_or_crafting"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "store_pack_inbox_crafting_boundary_report_v1"
external_reference_status: "reference_category_not_checked"
```

Expected note:

- Store/pack/inbox/crafting coverage is report-only boundary metadata.
- Mythic Edge has bounded StartHook `InventoryInfo` snapshot parsing, but does
  not claim store API parsing, pack-opening parsing, inbox/reward parsing,
  crafting/wildcard truth, transactions, collection ownership, account state,
  economy API support, or inventory/economy truth from that surface.

Expected summary count movement, assuming no other branch changes:

- `covered_report_only`: increases by 1.
- `missing`: decreases by 1.
- `covered_committed`: unchanged.
- `covered_synthetic`: unchanged.
- `partial`: unchanged.
- `blocked_external_boundary`: unchanged.

Codex C must record the actual before/after counts in its implementation
handoff and contract test report.

## Validation Obligations

Codex C must run focused validation:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m pytest -q tests/test_parser_small_modules.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
printf '%s\n' \
  docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md \
  docs/implementation_handoffs/parser_corpus_store_pack_inbox_crafting_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_store_pack_inbox_crafting_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' \
  docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md \
  docs/implementation_handoffs/parser_corpus_store_pack_inbox_crafting_coverage_comparison.md \
  docs/contract_test_reports/parser_corpus_store_pack_inbox_crafting_coverage.md \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  tests/fixtures/parser_corpus/session_ledger.v1.json \
  tests/test_corpus_parity_report.py \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Codex C may add narrower or platform-specific commands if local tool behavior
requires it. Any skipped command must be reported with the reason.

Codex E/F/G should verify:

- Only authorized files changed.
- The contract path is cited by the new manifest/session-ledger entries.
- `deck_api.store_pack_inbox_or_crafting` is `covered_report_only`, not
  synthetic or committed.
- `parser_behavior_verified` is absent from the store/pack/inbox/crafting row.
- `parser_event_families` is empty for the new boundary entry.
- `deck_api.start_hook_deck_snapshot` remains `covered_synthetic`.
- `deck_api.deck_summary` remains `covered_report_only`.
- `deck_api.deck_upsert` remains `covered_report_only`.
- `deck_api.event_set_deck` remains `covered_committed`.
- No private or external corpus evidence was committed.
- No parser/runtime/workbook/webhook/App Script/analytics/AI behavior changed.

## Acceptance Criteria

This module is complete when:

- `docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md` exists
  and is cited by the implementation handoff and report.
- `store_pack_inbox_crafting_boundary_report_v1` exists in the corpus manifest
  and session ledger.
- The corpus parity report maps `deck_api.store_pack_inbox_or_crafting` to
  `covered_report_only` with `coverage_basis == ["fixture_metadata_only"]`.
- The report clearly distinguishes store/pack/inbox/crafting boundary metadata
  from StartHook `InventoryInfo`, StartHook deck snapshot, deck summary, deck
  upsert, event-set deck, submit-deck, account state, and inventory/economy
  truth.
- Focused corpus parity tests cover the new manifest, session-ledger, report
  row, non-claims, and unchanged adjacent family statuses.
- The implementation handoff records comparison, files changed, validation run,
  open risks, and next recommended role.
- The contract test report records the validation evidence and final row
  counts.

## Unknowns

- Whether future owned Mythic Edge evidence will expose narrow store, pack,
  inbox, reward, crafting, transaction, wildcard, collection, account, or
  economy parser surfaces.
- Whether any future fixture can prove one of those surfaces without committing
  private account/economy data, currency balances, pack inventory, inbox
  contents, crafting choices, collection ownership data, private decklists,
  deck names, card choices, or external corpus contents.
- Whether this combined scenario family should later split into smaller
  families if owned evidence reveals distinct payload classes.

These unknowns do not block report-only boundary coverage.

## Suspected Gaps

- The current corpus matrix can make `deck_api.store_pack_inbox_or_crafting`
  look simply unexamined, even though adjacent inventory evidence has been
  deliberately scoped away from store/pack/inbox/crafting support.
- `InventoryInfo` can sound broader than it is; current parser tests prove only
  a mapping-shaped StartHook inventory snapshot event.
- Store, pack, inbox, crafting, reward, transaction, wildcard, collection, and
  account surfaces carry stronger privacy risk than ordinary match fixtures.
- Future work could accidentally use account/economy metadata as parity
  evidence unless this boundary is explicit.

## Non-Claims

This contract does not claim:

- store API parser support
- pack-opening parser support
- inbox or reward parser support
- crafting or wildcard truth
- transaction or purchase truth
- account-state truth
- currency-balance truth
- pack-inventory truth
- inbox-content truth
- collection ownership truth
- broad inventory/economy truth
- card ownership truth
- deck identity truth
- decklist completion
- submitted-deck truth
- sideboard-delta truth
- archetype truth
- matchup-plan truth
- gameplay advice
- player-mistake labels
- analytics truth
- AI truth
- coaching truth
- release readiness
- production behavior
- tracker completion

## Stop Conditions

Codex C must stop and route back to Codex B if implementation would require:

- parser code changes
- parser event class changes
- inventory parser behavior changes
- store, pack, inbox, crafting, reward, transaction, wildcard, collection,
  account, or economy parser implementation
- corpus vocabulary changes outside existing allowed values
- reclassifying `deck_api.start_hook_deck_snapshot`
- reclassifying `deck_api.deck_summary`
- reclassifying `deck_api.deck_upsert`
- reclassifying `deck_api.event_set_deck`
- private or external corpus evidence
- raw Player.log excerpts
- Manasight source or raw corpus contents
- private economy/account data
- currency balances
- pack inventories
- inbox contents
- crafting choices
- collection ownership data
- private decklists, deck names, card choices, sideboard plans, or strategy
  notes
- workbook, webhook, Apps Script, Google Sheets, runtime, analytics, local app,
  AI, OpenAI/model-provider, CI, merge, deploy, release, or production changes

## Recommended Next Role

Codex C: Module Implementer.

Implementation should proceed as a metadata/test-only corpus parity update.

## Pasteable Codex C Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #398, store/pack/inbox/crafting corpus evidence boundary.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/398

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Base branch:
  codex/parser-parity

  Contract:
  docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md

  Goal:
  Implement the smallest metadata/test-only corpus parity change that satisfies the store/pack/inbox/crafting coverage contract. Add report-only boundary coverage for exactly deck_api.store_pack_inbox_or_crafting without changing parser behavior or claiming store, pack, inbox, crafting, reward, transaction, wildcard, collection, account, or economy API parser support.

  Required behavior:
  - Add store_pack_inbox_crafting_boundary_report_v1 to the corpus manifest and session ledger.
  - Change the corpus parity row for deck_api.store_pack_inbox_or_crafting from missing/external_reference_only to covered_report_only/fixture_metadata_only.
  - Keep parser_event_families empty for the new boundary entry.
  - Do not include parser_behavior_verified for deck_api.store_pack_inbox_or_crafting.
  - Explicitly document that InventoryInfo, StartHook deck snapshot, deck summary, deck upsert, event-set deck, submit-deck, and submitted-deck-card evidence are reference-only adjacent evidence, not store/pack/inbox/crafting support.
  - Preserve the existing statuses and meanings of deck_api.start_hook_deck_snapshot, deck_api.deck_summary, deck_api.deck_upsert, and deck_api.event_set_deck.
  - Produce docs/implementation_handoffs/parser_corpus_store_pack_inbox_crafting_coverage_comparison.md and docs/contract_test_reports/parser_corpus_store_pack_inbox_crafting_coverage.md.

  Validation:
  - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
  - PYTHONPATH=src python3 -m pytest -q tests/test_parser_small_modules.py
  - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
  - python3 tools/check_agent_docs.py
  - printf '%s\n' docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md docs/implementation_handoffs/parser_corpus_store_pack_inbox_crafting_coverage_comparison.md docs/contract_test_reports/parser_corpus_store_pack_inbox_crafting_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
  - printf '%s\n' docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md docs/implementation_handoffs/parser_corpus_store_pack_inbox_crafting_coverage_comparison.md docs/contract_test_reports/parser_corpus_store_pack_inbox_crafting_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
  - python3 -m ruff check src tests tools
  - git diff --check

  Do not:
  - Implement parser behavior.
  - Change inventory parser behavior.
  - Change parser event classes, parser state final reconciliation, router semantics, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, diagnostics, golden replay, feature-equity, evidence-ledger behavior, runtime artifacts, analytics truth, AI truth, coaching behavior, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, release policy, or production behavior.
  - Commit or reproduce raw/private Player.log excerpts, Manasight logs, external corpus contents, private economy/account data, currency balances, pack inventories, inbox contents, crafting choices, collection ownership data, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, deck names, card choices, or strategy notes.
  - Claim full Mythic Edge corpus parity or store/pack/inbox/crafting parser support.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/398"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/396"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/397"
  previous_merge_commit: "da8b3f66692ac0c8aa60544c4380dd9bc0c4f17c"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_store_pack_inbox_crafting_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_store_pack_inbox_crafting_coverage.md"
  verdict: "contract_ready_for_report_only_store_pack_inbox_crafting_boundary"
  risk_tier: "High"
  branch: "codex/parser-corpus-store-pack-inbox-crafting-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim store/pack/inbox/crafting parser support from InventoryInfo or adjacent deck evidence."
    - "Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, private economy/account data, currency balances, pack inventories, inbox contents, crafting choices, collection ownership data, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, deck names, card choices, strategy notes, or private reports."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/evidence-ledger/analytics/AI/production surfaces without a new explicit contract."
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/398"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/396"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/397"
  previous_merge_commit: "da8b3f66692ac0c8aa60544c4380dd9bc0c4f17c"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_store_pack_inbox_crafting_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_store_pack_inbox_crafting_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_store_pack_inbox_crafting_coverage.md"
  verdict: "contract_ready_for_report_only_store_pack_inbox_crafting_boundary"
  risk_tier: "High"
  branch: "codex/parser-corpus-store-pack-inbox-crafting-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  validation:
    - "pending - Codex C implementation should run focused corpus parity, inventory parser, report generation, docs, secret, protected-surface, ruff, and diff checks."
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim store/pack/inbox/crafting parser support from InventoryInfo or adjacent deck evidence."
    - "Do not import, copy, mirror, or commit Manasight raw logs or external corpus contents."
    - "Do not commit private Player.log excerpts, private local logs, private economy/account data, currency balances, pack inventories, inbox contents, crafting choices, collection ownership data, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, webhook URLs, decklists, deck names, card choices, strategy notes, or private reports."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/evidence-ledger/analytics/AI/production surfaces without a new explicit contract."
```
