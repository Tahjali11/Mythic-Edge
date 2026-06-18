# Parser Corpus StartHook Deck Snapshot Coverage Contract

## Module

StartHook deck snapshot corpus coverage for the parser corpus parity report.

Plain English: this slice lets Mythic Edge cover exactly
`deck_api.start_hook_deck_snapshot` with repo-owned synthetic metadata and
existing parser-owned StartHook collection/deck-collection parser evidence. It
proves only that Mythic Edge can recognize a bounded `StartHook` response with
`PlayerCards`, `DeckSummaries`, and `Decks`, emit `Collection` and
`DeckCollection` events, correlate a deck summary to a deck payload by
`DeckId`, preserve source evidence, and keep the result inside corpus metadata.
It does not prove private deck contents, submitted-deck truth, deck identity
truth, deck-summary API coverage, deck-upsert behavior, inventory/economy
coverage, analytics truth, AI truth, coaching truth, release readiness, or
production behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/392
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/389
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/390
- Previous merge commit:
  `6591490e6eafcb8f90773e6b8b493cfb85ee0285`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-start-hook-deck-snapshot-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `6591490e6eafcb8f90773e6b8b493cfb85ee0285`
- target_artifact:
  `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md`
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
- `docs/contracts/parser_field_level_parity_audit.md`
- `docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/collection.py`
- `src/mythic_edge_parser/parsers/inventory.py`
- `tests/test_collection_parser.py`
- `tests/test_parser_small_modules.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `tests/test_runtime_surfaces.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, source records, hash lists,
  byte-size row lists, capture-date row lists, parser source, deck examples, or
  external corpus contents.

## Scope Decision

Implementation may proceed as safe synthetic coverage.

Codex B considered these paths:

1. Safe synthetic coverage.
2. Report-only coverage.
3. Evidence-prerequisite or approval-gated private smoke planning before
   coverage.

Selected path: safe synthetic coverage.

Reasoning:

- `src/mythic_edge_parser/parsers/collection.py` already recognizes
  `StartHook` responses and emits `Collection` events for mapping-shaped
  `PlayerCards`.
- The same parser emits `DeckCollection` events for list-shaped
  `DeckSummaries` plus mapping-shaped `Decks` when at least one summary can be
  correlated to a deck payload by `DeckId`.
- `tests/test_collection_parser.py` already uses synthetic StartHook payloads
  for player cards, deck summaries, deck payloads, orphaned deck summaries,
  and malformed summary entries.
- The field-level parity audit labels `Collection` and `DeckCollection` as
  `documented_partial`, not unknown, and identifies focused tests plus schema
  snapshots as existing evidence.
- A corpus manifest/session-ledger entry can summarize this parser evidence
  without committing private decklists, private deck names, collection data, or
  external corpus material.

This decision is intentionally narrow. It does not claim live MTGA StartHook
payload diversity has been observed in committed fixtures, that any deck name
or card list is private-user truth, or that adjacent deck/economy API families
are covered.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the
`deck_api.start_hook_deck_snapshot` scenario family. Parser modules own the
underlying StartHook parsing behavior. Runtime surfaces may consume
collection/deck events downstream, but they do not own this coverage claim.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance
validation evidence. It is not a Parser behavior module and is not a runtime,
workbook, webhook, Apps Script, Google Sheets, analytics, local app, AI,
coaching, release, or production module.

## Truth Owner

Truth owner for `deck_api.start_hook_deck_snapshot` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Truth owner for StartHook parser behavior referenced by this coverage:

- `src/mythic_edge_parser/parsers/collection.py`
- `tests/test_collection_parser.py`
- `tests/test_event_schema_snapshots.py`

Related parser truth owner that remains out of this slice:

- `src/mythic_edge_parser/parsers/inventory.py` owns `InventoryInfo` parsing.
  Inventory/economy coverage is not authorized by this issue.

Downstream consumers that remain non-authoritative for this corpus claim:

- `src/mythic_edge_parser/app/runtime_surfaces.py`
- workbook/export surfaces
- webhook/App Script transport
- analytics and AI/coaching surfaces

Truth boundary:

- `collection.try_parse(...)` owns StartHook event emission for `Collection`
  and `DeckCollection`.
- `_build_collection_payload(...)` owns accepting mapping-shaped
  `PlayerCards` and preserving source evidence under `raw_start_hook`.
- `_build_deck_collection_payload(...)` owns accepting list-shaped
  `DeckSummaries` plus mapping-shaped `Decks` and preserving source evidence
  under `raw_start_hook`.
- `_correlate_decks(...)` owns correlating deck summaries to deck payloads by
  `DeckId` and skipping orphaned or malformed entries.
- Corpus parity artifacts own only the coverage row for
  `deck_api.start_hook_deck_snapshot`.
- Corpus coverage status is review metadata. It is not deck identity truth,
  submitted-deck truth, active-deck truth, sideboard-delta truth, collection
  ownership truth, match/game truth, inventory/economy truth, analytics truth,
  AI truth, coaching truth, merge readiness, deploy readiness, release
  readiness, production behavior, or tracker-completion authority.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
existing StartHook Collection / DeckCollection parser evidence
  -> bounded synthetic committed corpus manifest/session-ledger metadata
  -> corpus parity coverage row for deck_api.start_hook_deck_snapshot
```

Forbidden reverse flow:

- Corpus coverage status must not change StartHook parser behavior.
- Corpus metadata must not change `CollectionEvent`, `DeckCollectionEvent`, or
  `InventoryEvent` classes.
- Corpus metadata must not change runtime active-deck matching, collection
  profile behavior, local status files, workbook output, webhook output,
  Apps Script behavior, analytics, AI, coaching, release policy, or production
  behavior.
- Corpus metadata must not turn synthetic StartHook deck snapshot evidence
  into a claim about live private deck contents, exact deck identity, submitted
  deck facts, sideboard deltas, decklist completion, archetypes, card choices,
  collection ownership, economy state, or gameplay advice.

Protected surfaces explicitly not touched:

- parser behavior
- StartHook parser behavior
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
- local active-deck or collection artifacts
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

- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `tests/test_collection_parser.py`, only for focused synthetic test evidence
  that does not change behavior
- `docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md`

Files Codex C may inspect but must not change unless it routes back for a
contract clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/collection.py`
- `src/mythic_edge_parser/parsers/inventory.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `tests/test_parser_small_modules.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_event_schema_snapshots.py`

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- StartHook parser semantics changes
- inventory/economy parser changes
- runtime active-deck or collection-profile behavior changes
- deck-summary coverage
- deck-upsert coverage
- store, pack, inbox, crafting, wildcard, inventory, or economy coverage
- committed decklists, deck names, or private collection records
- private smoke execution
- committed external corpus material
- diagnostics report changes
- golden replay behavior changes
- feature-equity behavior changes
- evidence-ledger behavior changes
- workbook, webhook, Apps Script, Google Sheets, local app, analytics, AI,
  coaching, CI, final integration, and production surfaces

## Public Interface

The public corpus interface remains the existing corpus parity report API:

```text
build_corpus_parity_report(
    manifest_path,
    *,
    session_ledger_path=None,
    feature_equity_report=None,
    external_reference=None,
) -> dict

write_corpus_parity_report(...) -> dict

validate_corpus_manifest(payload) -> list[str]
validate_session_ledger(payload) -> list[str]
```

The command-line interface remains:

```bash
python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

The parser behavior interface referenced by this contract is existing evidence
only:

```text
collection.try_parse(entry, timestamp) -> GameEvent | list[GameEvent] | None

CollectionEvent.kind == "Collection"
CollectionEvent.payload["type"] == "collection_snapshot"
CollectionEvent.payload["player_cards"] == mapping
CollectionEvent.payload["raw_start_hook"] == parsed StartHook mapping

DeckCollectionEvent.kind == "DeckCollection"
DeckCollectionEvent.payload["type"] == "deck_collection_snapshot"
DeckCollectionEvent.payload["decks"] == correlated mapping by DeckId
DeckCollectionEvent.payload["raw_start_hook"] == parsed StartHook mapping
```

No new public parser, runtime, workbook, webhook, Apps Script, analytics, AI,
or production interface is authorized by this contract.

## Observed Current Behavior

Observed on `codex/parser-parity` at
`6591490e6eafcb8f90773e6b8b493cfb85ee0285`:

- Issue #392 is open under tracker #158.
- Tracker #158 remains open.
- Issue #389 is closed and PR #390 is merged into `codex/parser-parity`.
- The current corpus parity report is still partial:
  `partial_coverage_map_ready` with 45 scenario families, 6 committed
  families, 12 synthetic families, 2 report-only families, 3 partial families,
  16 missing families, and 6 external-boundary families.
- `deck_api.start_hook_deck_snapshot` is `missing` with
  `coverage_basis: ["external_reference_only"]`.
- `deck_api.deck_summary` is `missing`.
- `deck_api.deck_upsert` is `missing`.
- `deck_api.event_set_deck` is `covered_committed`.
- `deck_api.store_pack_inbox_or_crafting` is `missing`.
- `src/mythic_edge_parser/parsers/collection.py` emits:
  - `Collection` for mapping-shaped `PlayerCards`;
  - `DeckCollection` for list-shaped `DeckSummaries` plus mapping-shaped
    `Decks` when at least one `DeckId` correlates.
- `src/mythic_edge_parser/parsers/collection.py` preserves source evidence as
  `raw_start_hook` for both event kinds.
- `tests/test_collection_parser.py` covers:
  - `PlayerCards` only;
  - combined `PlayerCards`, `DeckSummaries`, and `Decks`;
  - orphaned deck summary skipping;
  - a StartHook shape that emits `DeckCollection`;
  - non-mapping `PlayerCards` returning `None`;
  - empty correlated decks returning `None`;
  - malformed deck summary entries being skipped.
- The field-level parity audit labels `Collection` and `DeckCollection` as
  `documented_partial` because focused tests and schema snapshots exist but
  committed corpus coverage is zero.
- `src/mythic_edge_parser/parsers/inventory.py` separately parses StartHook
  `InventoryInfo` into `Inventory`; that is adjacent but out of scope here.
- `src/mythic_edge_parser/app/runtime_surfaces.py` consumes `DeckCollection`,
  `Collection`, and `Inventory` events downstream. This contract does not
  authorize runtime-surface changes.

## Required Guarantees

### Scenario Family Boundary

Codex C may close only this corpus coverage gap:

- `deck_api.start_hook_deck_snapshot`

The implementation must not mark any of these families as covered or changed:

- `deck_api.deck_summary`
- `deck_api.deck_upsert`
- `deck_api.store_pack_inbox_or_crafting`
- `deck_api.event_set_deck`
- any inventory/economy, deck identity, submitted-deck, sideboard-delta,
  runtime, analytics, AI, coaching, release-readiness, or production family not
  explicitly named above

### Coverage Status

The authorized V1 coverage status is:

```yaml
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
```

Rationale:

- The coverage uses synthetic StartHook metadata and focused parser tests, not
  private or external log material.
- The current parser already emits the relevant event kinds and payload
  structures.
- The contract can assert privacy boundaries through manifest/session metadata
  and focused tests without adding parser behavior.

Codex C must not use `covered_committed`, `covered_report_only`, `partial`,
`blocked_private_evidence`, or `blocked_external_boundary` for this family in
issue #392 unless it routes back to Codex B with evidence that the selected
synthetic path is unsafe.

### Synthetic StartHook Shape

The synthetic parser evidence should use a minimal StartHook shape with:

```yaml
PlayerCards:
  "123": 4
DeckSummaries:
  - DeckId: "deck-1"
    Name: "Synthetic Deck"
    Attributes:
      - name: "Format"
        value: "Standard"
Decks:
  deck-1:
    MainDeck:
      - cardId: 1
        quantity: 4
    Sideboard: []
```

Required parser evidence:

- Parser route: `collection.try_parse(...)`.
- Event kinds: `Collection`, `DeckCollection`.
- `Collection.payload["type"] == "collection_snapshot"`.
- `Collection.payload["player_cards"]` preserves the mapping.
- `Collection.payload["raw_start_hook"]` exists.
- `DeckCollection.payload["type"] == "deck_collection_snapshot"`.
- `DeckCollection.payload["decks"]` has exactly one correlated deck id.
- The correlated deck preserves summary fields.
- The correlated deck stores the associated deck payload under `list`.
- `DeckCollection.payload["raw_start_hook"]` exists.
- Non-mapping `PlayerCards` remains rejected by existing behavior.
- Orphaned or malformed deck summaries remain skipped by existing behavior.

Codex C may adjust the synthetic IDs and names if needed, but the evidence
must remain synthetic and must not use private deck names, private card
choices, private decklists, or external corpus examples.

### Manifest Entry

Codex C should add exactly one corpus manifest entry for this family.

Recommended entry id:

```text
start_hook_deck_snapshot_synthetic_v1
```

Recommended logical shape:

```yaml
entry_id: "start_hook_deck_snapshot_synthetic_v1"
entry_type: "session_ledger_entry"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/392"
authorized_by_contract: "docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md"
paths:
  session_ledger: "tests/fixtures/parser_corpus/session_ledger.v1.json"
  collection_parser_test: "tests/test_collection_parser.py"
  corpus_parity_test: "tests/test_corpus_parity_report.py"
scenario_families:
  - "deck_api.start_hook_deck_snapshot"
parser_event_families:
  - "Collection"
  - "DeckCollection"
parser_claim_families:
  - "start_hook_collection_snapshot"
  - "start_hook_deck_collection_snapshot"
  - "start_hook_deck_summary_to_deck_map_correlation"
  - "start_hook_raw_evidence_preservation"
  - "start_hook_deck_snapshot_privacy_boundary"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
```

Required known gap:

```text
Synthetic StartHook deck snapshot metadata does not prove private deck
contents, exact deck identity, submitted-deck truth, sideboard-delta truth,
collection ownership truth, inventory/economy state, deck-summary coverage,
deck-upsert coverage, store/pack/inbox/crafting coverage, archetype
classification, decklist completion, analytics truth, AI truth, coaching
truth, release readiness, or production behavior.
```

Required review note:

```text
Synthetic StartHook deck snapshot coverage proves parser-owned Collection and
DeckCollection StartHook metadata only; it preserves a bounded deck snapshot as
evidence and does not claim deck identity, submitted-deck, sideboard-delta,
inventory/economy, analytics, AI, coaching, release, or production truth.
```

### Session Ledger Entry

Codex C should add a matching session ledger row.

Recommended logical shape:

```yaml
session_id: "start_hook_deck_snapshot_synthetic_v1"
title: "Synthetic StartHook deck snapshot evidence"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/392"
authorized_by_contract: "docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md"
scenario_families:
  - "deck_api.start_hook_deck_snapshot"
format_family: "deck_api"
match_shape: "start_hook_deck_snapshot_signal_only"
record_summary: "synthetic_start_hook_summary_only"
parser_coverage:
  event_families:
    Collection: 1
    DeckCollection: 1
  unknown_entries: 0
  truncation_count: 0
  start_hook_collection_snapshots: 1
  start_hook_deck_collection_snapshots: 1
  start_hook_correlated_decks: 1
  start_hook_orphaned_deck_summaries_skipped: 0
  start_hook_malformed_deck_summaries_skipped: 0
game_rows:
  count: 0
  result_shape: "not_applicable"
known_gaps:
  - "Synthetic StartHook deck snapshot metadata does not prove private deck contents, exact deck identity, submitted-deck truth, sideboard-delta truth, collection ownership truth, inventory/economy state, deck-summary coverage, deck-upsert coverage, store/pack/inbox/crafting coverage, analytics truth, AI truth, coaching truth, release readiness, or production behavior."
report_only_redactions:
  raw_log_lines_included: false
  private_paths_included: false
  raw_payloads_included: false
  external_logs_included: false
  decklists_included: false
  private_deck_names_included: false
  private_collection_data_included: false
```

Codex C may adjust summary count field names to match existing session-ledger
style, but must preserve the meaning and privacy boundary.

### Non-Claims

The StartHook deck snapshot coverage row must explicitly not claim:

- full Mythic Edge corpus parity;
- parser support from corpus metadata alone;
- live private StartHook payload diversity;
- private deck contents;
- private deck names;
- exact deck identity truth;
- submitted-deck truth;
- active-deck truth;
- sideboard-delta truth;
- collection ownership truth;
- inventory/economy state;
- deck-summary coverage;
- deck-upsert coverage;
- store, pack, inbox, crafting, wildcard, or economy coverage;
- decklist completion;
- hidden-card inference;
- archetype classification;
- gameplay advice;
- player-mistake labels;
- diagnostics readiness;
- release readiness;
- analytics truth;
- AI truth;
- coaching truth;
- merge readiness;
- deploy readiness;
- production behavior;
- tracker #158 completion.

### Deferred Deck API Families

`deck_api.deck_summary` remains missing. It needs a separate problem
representation and contract if Mythic Edge later wants to cover dedicated deck
summary API behavior beyond the StartHook snapshot correlation already
represented here.

`deck_api.deck_upsert` remains missing. It needs a separate problem
representation and contract.

`deck_api.store_pack_inbox_or_crafting` remains missing. It needs a separate
problem representation and contract, and must preserve inventory/economy
privacy boundaries.

`deck_api.event_set_deck` remains `covered_committed`; Codex C must not alter
that row except for adjacent boundary assertions if needed.

## Inputs

Allowed inputs:

- Current repo docs and contracts named by this contract.
- Existing corpus parity manifest and session ledger.
- Existing StartHook parser code and focused tests.
- Current report output from the corpus parity CLI.
- Local synthetic values written in tests or metadata under this contract.
- Public Manasight metadata only through category-level taxonomy context
  already represented by prior corpus parity artifacts.

Forbidden inputs:

- Manasight raw logs, compressed corpus files, source records, hash lists,
  byte-size row lists, capture-date row lists, parser source, deck examples,
  or external corpus contents.
- Private Player.log excerpts, private local logs, private smoke outputs,
  generated data, SQLite files, runtime artifacts, workbook exports,
  credentials, tokens, API keys, webhook endpoints, IP/network traces, private
  decklists, private deck names, card choices, collection ownership data,
  inventory/economy state, sideboard plans, strategy notes, private reports, or
  local MTGA settings dumps.
- Newly generated local reports committed as source artifacts, unless a later
  contract authorizes exact report artifact storage.

## Outputs

Authorized output changes for Codex C:

- One new corpus manifest entry for `deck_api.start_hook_deck_snapshot`.
- One new session ledger entry for `deck_api.start_hook_deck_snapshot`.
- Focused collection parser tests only if needed to pin the synthetic StartHook
  evidence described by this contract.
- Focused corpus parity tests proving:
  - the new manifest entry validates;
  - the new session entry validates;
  - `deck_api.start_hook_deck_snapshot` is `covered_synthetic`;
  - `deck_api.deck_summary` remains `missing`;
  - `deck_api.deck_upsert` remains `missing`;
  - `deck_api.event_set_deck` remains `covered_committed`;
  - `deck_api.store_pack_inbox_or_crafting` remains `missing`;
  - required non-claims are present in known gaps or review notes.
- Implementation handoff and contract-test report documents.

Expected report summary after implementation, assuming no other branch changes:

```text
partial_coverage_map_ready (45 families, 6 committed, 15 missing)
```

Expected summary count changes:

- `covered_synthetic`: 12 -> 13
- `missing`: 16 -> 15
- `covered_committed`: unchanged
- `covered_report_only`: unchanged
- `partial`: unchanged
- `blocked_external_boundary`: unchanged

## Invariants

- `deck_api.start_hook_deck_snapshot` coverage must be `covered_synthetic`.
- `deck_api.start_hook_deck_snapshot` coverage basis must be exactly:
  `fixture_metadata_only`, `parser_behavior_verified`.
- The new entry must use `parser_event_families: ["Collection", "DeckCollection"]`.
- The new entry must not use `Inventory`, `ClientAction`, `MatchState`,
  `GameState`, `GameResult`, or runtime-only event families.
- The new entry must not use `diagnostics_only`, `evidence_ledger_only`,
  `count_ratchet_only`, or `external_reference_only`.
- The synthetic evidence must be StartHook-only and synthetic.
- The synthetic evidence must prove player-card mapping acceptance and
  deck-summary/deck-map correlation.
- The synthetic evidence must not include private deck names, private deck
  contents, private collection data, or external examples.
- The synthetic evidence must not claim actual live Arena behavior.
- `deck_api.deck_summary` must remain `missing`.
- `deck_api.deck_upsert` must remain `missing`.
- `deck_api.store_pack_inbox_or_crafting` must remain `missing`.
- `deck_api.event_set_deck` must remain `covered_committed`.
- The corpus parity report may remain `partial_coverage_map_ready`.
- No parser source, StartHook parser behavior, parser event classes, parser
  state, router, runtime, diagnostics, golden replay, feature-equity,
  evidence-ledger, workbook, webhook, Apps Script, analytics, AI, coaching, CI,
  merge, deploy, release, or production behavior change is authorized.

## Error Behavior

Contract ambiguity:

- If Codex C cannot represent this slice using the existing manifest/session
  schema and allowed status/basis vocabulary, it must route back to Codex B.

Synthetic shape mismatch:

- If the focused synthetic StartHook shape cannot emit both `Collection` and
  `DeckCollection` without source changes, Codex C must route back to Codex B
  rather than changing the parser in this issue.

Adjacent deck API pressure:

- If implementation appears to require covering deck summary, deck upsert,
  store, pack, inbox, crafting, inventory, economy, runtime active-deck
  matching, or submitted-deck behavior, stop and route back.

Existing test failure:

- If focused parser or corpus tests fail before Codex C edits metadata, Codex C
  must report the base failure and not patch parser behavior inside this issue.

Privacy or protected-surface warnings:

- If secret/private-marker or protected-surface checks warn on the new docs or
  metadata, Codex C must reword or narrow the metadata. It must not suppress
  checks or add broad allowlists.

Generated artifact temptation:

- If implementation would require committing generated reports, private smoke
  output, private decks, or runtime artifacts, stop and route back. Issue #392
  authorizes synthetic metadata and tests only.

## Side Effects

Codex B side effects:

- Create only this contract.

Codex C authorized side effects:

- Edit corpus manifest JSON.
- Edit session ledger JSON.
- Edit focused corpus parity tests.
- Edit focused collection parser tests only if needed.
- Write implementation handoff.
- Write contract-test report.

No runtime side effects, local external writes, GitHub issue closure, PR
creation, tracker completion, generated artifact commits, workbook changes,
webhook changes, Apps Script changes, analytics changes, AI/model-provider
calls, or production behavior changes are authorized.

## Dependency Order

Codex C should proceed in this order:

1. Verify branch state against `origin/codex/parser-parity`.
2. Run the current corpus parity report and capture the deck API rows.
3. Confirm existing StartHook parser evidence or add a focused synthetic test
   that does not change parser behavior.
4. Add the manifest entry.
5. Add the session ledger entry.
6. Add focused corpus parity assertions.
7. Run validation.
8. Write the implementation handoff and contract-test report.

## Compatibility

This contract preserves:

- corpus manifest schema version `parser_corpus_manifest.v1`;
- session ledger schema version `parser_corpus_session_ledger.v1`;
- scenario family id `deck_api.start_hook_deck_snapshot`;
- coverage status vocabulary;
- coverage basis vocabulary;
- existing `Collection` payload shape;
- existing `DeckCollection` payload shape;
- existing `raw_start_hook` preservation;
- existing deck correlation behavior by `DeckId`;
- existing inventory/economy boundary;
- existing committed `deck_api.event_set_deck` coverage;
- adjacent missing deck API rows.

No migration is authorized.

## Tests Required

Focused validation for Codex C:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m pytest -q tests/test_parser_small_modules.py tests/test_runtime_surfaces.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
git diff --check
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_collection_parser.py docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_collection_parser.py docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py tests/test_collection_parser.py docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

Recommended broader validation if the environment is ready:

```bash
PYTHONPATH=src python3 -m ruff check src tests
```

Codex C must record any skipped validation and why.

## Acceptance Criteria

- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md` exists.
- Codex C updates only the corpus metadata/test/report surfaces authorized by
  this contract, unless it routes back.
- The corpus manifest validates cleanly.
- The session ledger validates cleanly.
- The corpus parity report still returns `partial_coverage_map_ready`.
- `deck_api.start_hook_deck_snapshot` reports:
  - `coverage_status: covered_synthetic`
  - `coverage_basis: ["fixture_metadata_only", "parser_behavior_verified"]`
  - one Mythic Edge entry, `start_hook_deck_snapshot_synthetic_v1`
- `deck_api.deck_summary` remains `missing`.
- `deck_api.deck_upsert` remains `missing`.
- `deck_api.event_set_deck` remains `covered_committed`.
- `deck_api.store_pack_inbox_or_crafting` remains `missing`.
- Focused tests prove parser-owned StartHook `Collection` and
  `DeckCollection` evidence without parser behavior changes.
- Tests assert non-claims and adjacent deck API boundaries.
- No raw/private/external/generated artifacts are committed.
- No protected parser/runtime/workbook/webhook/App Script/diagnostics/golden
  replay/feature-equity/evidence-ledger/analytics/AI/production behavior
  changes are made.
- The implementation handoff and contract-test report name remaining gaps.

## Open Questions And Suspected Gaps

- The selected synthetic shape proves a bounded parser-normalization path, not
  actual live Arena StartHook payload diversity.
- The parser payload preserves broad StartHook structures; it does not deeply
  normalize deck contents, collection ownership, or economy fields.
- If future private smoke evidence shows different payload fields, that should
  become a new scoped issue and contract.
- `deck_api.deck_summary`, `deck_api.deck_upsert`, and
  `deck_api.store_pack_inbox_or_crafting` remain separate rows.
- Runtime deck matching and local active-deck summaries are downstream
  consumers and remain outside this corpus contract.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #392.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/392

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md

Goal:
Implement the smallest metadata/test/report-only change needed to satisfy the
StartHook deck snapshot corpus coverage contract. Move only
`deck_api.start_hook_deck_snapshot` from missing to `covered_synthetic` using
synthetic StartHook metadata and existing Collection / DeckCollection parser
behavior. Do not change parser behavior.

Before editing:
1. Fetch and verify `origin/codex/parser-parity`.
2. Create or use a clean implementation branch from `codex/parser-parity`.
3. Confirm PR #390 merged at
   `6591490e6eafcb8f90773e6b8b493cfb85ee0285` or record the newer base.
4. Inspect `git status --short --branch`.
5. Leave unrelated or untracked local artifacts alone.

Read:
- docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md
- docs/contracts/parser_corpus_parity_expansion.md
- docs/contracts/parser_field_level_parity_audit.md
- docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- src/mythic_edge_parser/app/corpus_parity_report.py
- tests/test_corpus_parity_report.py
- src/mythic_edge_parser/parsers/collection.py
- src/mythic_edge_parser/parsers/inventory.py
- tests/test_collection_parser.py
- tests/test_parser_small_modules.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- tests/test_runtime_surfaces.py

Do:
- Compare the current corpus parity report against the contract before editing.
- Confirm or add focused synthetic StartHook parser evidence for Collection and
  DeckCollection without parser behavior changes.
- Add exactly one manifest entry for
  `start_hook_deck_snapshot_synthetic_v1`.
- Add the matching session ledger entry.
- Add focused tests proving `deck_api.start_hook_deck_snapshot` is
  `covered_synthetic` and adjacent deck API rows remain bounded.
- Produce
  `docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md`.
- Produce
  `docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md`.

Do not:
- Change parser behavior.
- Change StartHook parser behavior, parser state final reconciliation, parser
  event classes, router semantics, diagnostics, drift reports, golden replay,
  feature-equity, evidence-ledger behavior, runtime surfaces, match/game
  identity, workbook/webhook or Apps Script behavior, analytics truth, AI
  truth, production behavior, CI gates, merge readiness, deploy readiness, or
  tracker lifecycle behavior.
- Cover `deck_api.deck_summary`, `deck_api.deck_upsert`, or
  `deck_api.store_pack_inbox_or_crafting` in issue #392.
- Alter `deck_api.event_set_deck` beyond adjacent boundary assertions.
- Claim private deck contents, private deck names, exact deck identity,
  submitted-deck truth, active-deck truth, sideboard-delta truth, collection
  ownership truth, inventory/economy state, decklist completion, archetype
  classification, hidden-card inference, gameplay advice, player-mistake
  labels, release readiness, analytics truth, AI truth, coaching truth,
  production behavior, full corpus parity, or parser support from corpus
  metadata alone.
- Import, copy, mirror, or commit external corpus contents or forbidden
  private/generated/local artifacts named by the contract.
- Target main directly.
- Close issue #392 or tracker #158.
- Stage or commit unless explicitly asked.

Validation:
- Run the focused validation commands from the contract.
- Run changed-file secret/private and protected-surface checks.
- Record skipped validation with reasons.

Expected output:
- Updated corpus manifest/session ledger/tests.
- Implementation handoff.
- Contract-test report.
- Validation summary.
- workflow_handoff block to Codex E.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/392"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/389"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/390"
  previous_merge_commit: "6591490e6eafcb8f90773e6b8b493cfb85ee0285"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md"
  verdict: "contract_ready_for_synthetic_start_hook_deck_snapshot_coverage"
  risk_tier: "High"
  branch: "codex/parser-corpus-start-hook-deck-snapshot-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "safe_synthetic_coverage"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_parser_small_modules.py tests/test_runtime_surfaces.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
    - "changed-file secret/private marker scan"
    - "changed-file protected-surface gate"
    - "changed-file validation selector"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not close issue #392."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim parser support from corpus metadata alone."
    - "Do not cover deck_api.deck_summary, deck_api.deck_upsert, deck_api.store_pack_inbox_or_crafting, or any other adjacent family in issue #392."
    - "Do not claim private deck contents, private deck names, exact deck identity, submitted-deck truth, active-deck truth, sideboard-delta truth, collection ownership truth, inventory/economy state, decklist completion, archetype classification, hidden-card inference, gameplay advice, player-mistake labels, release readiness, analytics truth, AI truth, coaching truth, production behavior, or tracker completion."
    - "Do not import, copy, mirror, or commit external corpus contents or forbidden private/generated/local artifacts named by the contract."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/evidence-ledger/analytics/AI/production surfaces without a new explicit contract."
```
