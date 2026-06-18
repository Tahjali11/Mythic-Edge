# Parser Corpus Deck Summary Coverage Contract

## Module

Deck summary corpus evidence boundary for the parser corpus parity report.

Plain English: this slice lets Mythic Edge account for exactly
`deck_api.deck_summary` as a report-only corpus boundary, not as a new parser
support claim. Current Mythic Edge code has parser-owned evidence for
`DeckSummaries` only inside StartHook `DeckCollection` parsing, and issue #392
already used that evidence for `deck_api.start_hook_deck_snapshot`. This
contract records that boundary so the deck-summary row no longer looks
unexamined, while explicitly not claiming a dedicated deck-summary API parser,
private deck identity, submitted-deck truth, deck-upsert behavior, inventory or
economy truth, analytics truth, AI truth, coaching truth, release readiness, or
production behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/394
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/392
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/393
- Previous merge commit:
  `4658ae79cd861309b795f4be71912f65cf444bbd`

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- branch: `codex/parser-corpus-deck-summary-coverage`
- base_branch: `codex/parser-parity`
- observed_base_commit: `4658ae79cd861309b795f4be71912f65cf444bbd`
- target_artifact:
  `docs/contracts/parser_corpus_deck_summary_coverage.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_deck_summary_coverage_comparison.md`
- expected_report:
  `docs/contract_test_reports/parser_corpus_deck_summary_coverage.md`
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
- `docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/contracts/parser_field_level_parity_audit.md`
- `docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/collection.py`
- `tests/test_collection_parser.py`

External reference status:

- Public Manasight metadata may be used only through already merged corpus
  parity and taxonomy-audit artifacts or as category-level reference context.
- This contract does not authorize importing, copying, mirroring, or committing
  Manasight logs, compressed corpus files, source records, hash lists,
  byte-size row lists, capture-date row lists, parser source, deck examples, or
  external corpus contents.

## Scope Decision

Implementation may proceed as report-only boundary coverage.

Codex B considered these paths:

1. Safe synthetic coverage.
2. Report-only boundary coverage.
3. Evidence-prerequisite or deferred status.

Selected path: report-only boundary coverage.

Reasoning:

- The repo has no dedicated parser for a standalone deck-summary API response.
- The only current parser-owned evidence is `DeckSummaries` inside
  `StartHook` payloads handled by `src/mythic_edge_parser/parsers/collection.py`.
- Issue #392 already used the StartHook `DeckSummaries` plus `Decks` evidence
  for `deck_api.start_hook_deck_snapshot`.
- Promoting `deck_api.deck_summary` to `covered_synthetic` from the same
  StartHook snapshot evidence would overread the prior coverage and risk
  implying dedicated deck-summary API support.
- Leaving the row as plain `missing` also hides a useful boundary decision:
  Mythic Edge has inspected the family and determined that current evidence is
  StartHook-bound, summary-only, and not a standalone parser-support claim.

This decision intentionally turns `deck_api.deck_summary` into a report-only
coverage boundary. It records what Mythic Edge knows and does not know, without
changing parser behavior or claiming broader deck API support.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns corpus coverage metadata for the `deck_api.deck_summary`
scenario family. Parser modules own the underlying StartHook parsing behavior.
Runtime surfaces, analytics, workbook outputs, and AI/coaching surfaces remain
downstream consumers and must not own this coverage claim.

## Internal Project Area

Corpus / Provenance.

This slice consumes Parser behavior evidence and Quality / Governance
validation evidence. It is not a Parser behavior module and is not a runtime,
workbook, webhook, Apps Script, Google Sheets, analytics, local app, AI,
coaching, release, or production module.

## Truth Owner

Truth owner for `deck_api.deck_summary` coverage status:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`

Truth owner for StartHook deck-summary field behavior referenced by this
coverage:

- `src/mythic_edge_parser/parsers/collection.py`
- `tests/test_collection_parser.py`
- `tests/test_event_schema_snapshots.py`

Truth boundary:

- `collection.try_parse(...)` owns StartHook event emission for `Collection`
  and `DeckCollection`.
- `_build_deck_collection_payload(...)` owns accepting list-shaped
  `DeckSummaries` plus mapping-shaped `Decks` and preserving source evidence
  under `raw_start_hook`.
- `_correlate_decks(...)` owns correlating StartHook deck summaries to deck
  payloads by `DeckId` and skipping orphaned or malformed entries.
- Issue #392 owns the synthetic StartHook deck snapshot coverage claim.
- This contract owns only the report-only deck-summary boundary row:
  StartHook `DeckSummaries` are known parser evidence, but a dedicated
  deck-summary API parser is not currently claimed.
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
existing StartHook DeckSummaries parser/test evidence and #392 boundary docs
  -> bounded committed report-only manifest/session-ledger metadata
  -> corpus parity boundary row for deck_api.deck_summary
```

Forbidden reverse flow:

- Corpus coverage status must not change StartHook parser behavior.
- Corpus metadata must not create, imply, or require a dedicated deck-summary
  parser.
- Corpus metadata must not change `CollectionEvent`, `DeckCollectionEvent`, or
  `InventoryEvent` classes.
- Corpus metadata must not change runtime active-deck matching, collection
  profile behavior, workbook output, webhook output, Apps Script behavior,
  analytics, AI, coaching, release policy, or production behavior.
- Corpus metadata must not turn StartHook `DeckSummaries` evidence into a
  claim about live private deck contents, exact deck identity, submitted deck
  facts, sideboard deltas, decklist completion, archetypes, card choices,
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

- `docs/contracts/parser_corpus_deck_summary_coverage.md`

Future Codex C files authorized by this contract:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_deck_summary_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_deck_summary_coverage.md`

Files Codex C may inspect but must not change unless it routes back for a
contract clarification:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/collection.py`
- `tests/test_collection_parser.py`
- `tests/test_event_schema_snapshots.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `tests/test_runtime_surfaces.py`

Out of scope unless a later contract explicitly authorizes it:

- parser source changes
- StartHook parser semantics changes
- dedicated deck-summary parser implementation
- inventory/economy parser changes
- runtime active-deck or collection-profile behavior changes
- StartHook deck snapshot coverage changes
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
DeckCollectionEvent.kind == "DeckCollection"
DeckCollectionEvent.payload["type"] == "deck_collection_snapshot"
DeckCollectionEvent.payload["decks"] == correlated mapping by DeckId
DeckCollectionEvent.payload["raw_start_hook"] == parsed StartHook mapping
```

No new public parser, runtime, workbook, webhook, Apps Script, analytics, AI,
or production interface is authorized by this contract.

## Observed Current Behavior

Observed on `codex/parser-parity` at
`4658ae79cd861309b795f4be71912f65cf444bbd`:

- Issue #394 is open under tracker #158.
- Tracker #158 remains open.
- Issue #392 is closed and PR #393 is merged into `codex/parser-parity`.
- The current corpus parity report is still partial:
  `partial_coverage_map_ready` with 45 scenario families, 6 committed
  families, 13 synthetic families, 2 report-only families, 3 partial families,
  15 missing families, and 6 external-boundary families.
- `deck_api.start_hook_deck_snapshot` is `covered_synthetic` through
  `start_hook_deck_snapshot_synthetic_v1`.
- `deck_api.deck_summary` is `missing` with
  `coverage_basis: ["external_reference_only"]`.
- `deck_api.deck_upsert` is `missing`.
- `deck_api.event_set_deck` is `covered_committed`.
- `deck_api.store_pack_inbox_or_crafting` is `missing`.
- `src/mythic_edge_parser/parsers/collection.py` emits `DeckCollection` for
  list-shaped `DeckSummaries` plus mapping-shaped `Decks` when at least one
  `DeckId` correlates.
- `tests/test_collection_parser.py` pins StartHook `DeckSummaries`
  correlation, source evidence preservation, orphan skipping, and malformed
  summary skipping.
- Repo-wide search found no dedicated standalone deck-summary parser surface.
- The field-level parity audit labels `DeckCollection` as
  `documented_partial`; it says DeckCollection evidence is enrichment and does
  not replace submitted-deck evidence.
- The #392 contract and report explicitly state that StartHook deck snapshot
  coverage does not claim deck-summary coverage.

## Required Guarantees

### Scenario Family Boundary

Codex C may close only this corpus coverage gap:

- `deck_api.deck_summary`

The implementation must not mark any of these families as covered or changed:

- `deck_api.deck_upsert`
- `deck_api.store_pack_inbox_or_crafting`
- `deck_api.start_hook_deck_snapshot`
- `deck_api.event_set_deck`
- any inventory/economy, deck identity, submitted-deck, sideboard-delta,
  runtime, analytics, AI, coaching, release-readiness, or production family not
  explicitly named above

### Coverage Status

The authorized V1 coverage status is:

```yaml
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
```

Rationale:

- The coverage row is a committed metadata/report boundary, not a parser
  behavior proof for a dedicated deck-summary API.
- Existing parser behavior has already been used to cover the StartHook deck
  snapshot row.
- The row should make the deck-summary boundary visible without claiming
  unsupported parser support.

Codex C must not use `covered_synthetic`, `covered_committed`, `partial`,
`blocked_private_evidence`, or `blocked_external_boundary` for this family in
issue #394 unless it routes back to Codex B with evidence that this contract's
report-only path is wrong.

### Deck Summary Evidence Boundary

The in-scope evidence is:

- StartHook `DeckSummaries` field handling as already present in
  `DeckCollection` parser behavior.
- Existing #392 synthetic evidence proving StartHook
  `DeckSummaries` plus `Decks` correlation by `DeckId`.
- Existing focused tests proving orphaned and malformed deck summaries are
  skipped.
- Corpus metadata that records this as a boundary decision.

The out-of-scope evidence is:

- a standalone deck-summary API response;
- any new parser route;
- any private deck name, decklist, card choice, or collection ownership data;
- any live/private StartHook sample;
- any external corpus sample.

### Manifest Entry

Codex C should add exactly one corpus manifest entry for this family.

Recommended entry id:

```text
deck_summary_boundary_report_v1
```

Recommended logical shape:

```yaml
entry_id: "deck_summary_boundary_report_v1"
entry_type: "session_ledger_entry"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/394"
authorized_by_contract: "docs/contracts/parser_corpus_deck_summary_coverage.md"
paths:
  session_ledger: "tests/fixtures/parser_corpus/session_ledger.v1.json"
  prior_start_hook_contract: "docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md"
  prior_start_hook_report: "docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md"
  corpus_parity_test: "tests/test_corpus_parity_report.py"
scenario_families:
  - "deck_api.deck_summary"
parser_event_families: []
parser_claim_families:
  - "deck_summary_boundary_report"
  - "start_hook_deck_summaries_reference_only"
  - "dedicated_deck_summary_api_not_claimed"
  - "deck_summary_privacy_boundary"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
```

Required known gap:

```text
Deck summary boundary coverage records that current Mythic Edge evidence is
StartHook-bound and report-only; it does not prove a dedicated deck-summary API
parser, private deck contents, exact deck identity, submitted-deck truth,
sideboard-delta truth, collection ownership truth, inventory/economy state,
deck-upsert coverage, store/pack/inbox/crafting coverage, archetype
classification, decklist completion, analytics truth, AI truth, coaching
truth, release readiness, or production behavior.
```

Required review note:

```text
Deck summary coverage is report-only boundary metadata: Mythic Edge has
StartHook DeckSummaries evidence through the existing DeckCollection parser and
#392 coverage, but does not claim a standalone deck-summary API parser or deck
identity/submitted-deck truth.
```

### Session Ledger Entry

Codex C should add a matching session ledger row.

Recommended logical shape:

```yaml
session_id: "deck_summary_boundary_report_v1"
title: "Deck summary boundary report"
source_kind: "committed_count_only_report"
commit_status: "committed"
privacy_class: "committed_count_only"
sanitization_status: "not_applicable_count_only"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/394"
authorized_by_contract: "docs/contracts/parser_corpus_deck_summary_coverage.md"
scenario_families:
  - "deck_api.deck_summary"
format_family: "deck_api"
match_shape: "deck_summary_boundary_report_only"
record_summary: "committed_deck_summary_boundary_metadata_only"
parser_coverage:
  event_families: {}
  unknown_entries: 0
  truncation_count: 0
  start_hook_deck_summaries_reference_entries: 1
  dedicated_deck_summary_api_events: 0
  dedicated_deck_summary_parser_routes: 0
game_rows:
  count: 0
  result_shape: "not_applicable"
known_gaps:
  - "Deck summary boundary coverage records StartHook-bound report-only evidence and does not prove dedicated deck-summary API parsing, private deck contents, exact deck identity, submitted-deck truth, sideboard-delta truth, collection ownership truth, inventory/economy state, deck-upsert coverage, store/pack/inbox/crafting coverage, analytics truth, AI truth, coaching truth, release readiness, or production behavior."
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

The deck summary coverage row must explicitly not claim:

- full Mythic Edge corpus parity;
- parser support from corpus metadata alone;
- a dedicated deck-summary API parser;
- live private StartHook or deck-summary payload diversity;
- private deck contents;
- private deck names;
- exact deck identity truth;
- submitted-deck truth;
- active-deck truth;
- sideboard-delta truth;
- collection ownership truth;
- inventory/economy state;
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

`deck_api.deck_upsert` remains missing. It needs a separate problem
representation and contract.

`deck_api.store_pack_inbox_or_crafting` remains missing. It needs a separate
problem representation and contract, and must preserve inventory/economy
privacy boundaries.

`deck_api.start_hook_deck_snapshot` remains `covered_synthetic`; Codex C must
not alter that row except for adjacent boundary assertions if needed.

`deck_api.event_set_deck` remains `covered_committed`; Codex C must not alter
that row except for adjacent boundary assertions if needed.

## Inputs

Allowed inputs:

- Current repo docs and contracts named by this contract.
- Existing corpus parity manifest and session ledger.
- Existing StartHook parser code and focused tests.
- Current report output from the corpus parity CLI.
- Current #392 contract, handoff, and report artifacts.
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

- One new corpus manifest entry for `deck_api.deck_summary`.
- One new session ledger entry for `deck_api.deck_summary`.
- Focused corpus parity tests proving:
  - the new manifest entry validates;
  - the new session entry validates;
  - `deck_api.deck_summary` is `covered_report_only`;
  - `deck_api.start_hook_deck_snapshot` remains `covered_synthetic`;
  - `deck_api.deck_upsert` remains `missing`;
  - `deck_api.event_set_deck` remains `covered_committed`;
  - `deck_api.store_pack_inbox_or_crafting` remains `missing`;
  - required non-claims are present in known gaps or review notes.
- Implementation handoff and contract-test report documents.

No parser tests are required for new behavior because this slice intentionally
does not claim new parser behavior. Codex C may run existing focused parser
tests for evidence, but must not change parser source or parser tests unless
the contract is looped back.

Expected report summary after implementation, assuming no other branch changes:

```text
partial_coverage_map_ready (45 families, 6 committed, 14 missing)
```

Expected summary count changes:

- `covered_report_only`: 2 -> 3
- `missing`: 15 -> 14
- `covered_committed`: unchanged
- `covered_synthetic`: unchanged
- `partial`: unchanged
- `blocked_external_boundary`: unchanged

## Invariants

- `deck_api.deck_summary` coverage must be `covered_report_only`.
- `deck_api.deck_summary` coverage basis must be exactly:
  `fixture_metadata_only`.
- The new entry must use `parser_event_families: []`.
- The new entry must not use `Collection`, `DeckCollection`, `Inventory`,
  `ClientAction`, `MatchState`, `GameState`, `GameResult`, or runtime-only
  event families.
- The new entry must not use `parser_behavior_verified`, `diagnostics_only`,
  `evidence_ledger_only`, `count_ratchet_only`, or `external_reference_only`.
- The new entry must not claim a dedicated deck-summary API parser.
- The new entry must not add a synthetic parser fixture or new parser
  behavior.
- `deck_api.start_hook_deck_snapshot` must remain `covered_synthetic`.
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

Synthetic temptation:

- If Codex C believes deck-summary coverage should be `covered_synthetic`, it
  must route back to Codex B with evidence of a dedicated parser behavior or a
  contract-safe reason to reinterpret the family.

Adjacent deck API pressure:

- If implementation appears to require covering deck upsert, store, pack,
  inbox, crafting, inventory, economy, runtime active-deck matching, or
  submitted-deck behavior, stop and route back.

Existing test failure:

- If focused parser or corpus tests fail before Codex C edits metadata, Codex C
  must report the base failure and not patch parser behavior inside this issue.

Privacy or protected-surface warnings:

- If secret/private-marker or protected-surface checks warn on the new docs or
  metadata, Codex C must reword or narrow the metadata. It must not suppress
  checks or add broad allowlists.

Generated artifact temptation:

- If implementation would require committing generated reports, private smoke
  output, private decks, or runtime artifacts, stop and route back. Issue #394
  authorizes report-only metadata and tests only.

## Side Effects

Codex B side effects:

- Create only this contract.

Codex C authorized side effects:

- Edit corpus manifest JSON.
- Edit session ledger JSON.
- Edit focused corpus parity tests.
- Write implementation handoff.
- Write contract-test report.

No parser source edits, parser test edits, runtime side effects, local external
writes, GitHub issue closure, PR creation, tracker completion, generated
artifact commits, workbook changes, webhook changes, Apps Script changes,
analytics changes, AI/model-provider calls, or production behavior changes are
authorized.

## Dependency Order

Codex C should proceed in this order:

1. Verify branch state against `origin/codex/parser-parity`.
2. Run the current corpus parity report and capture the deck API rows.
3. Confirm no dedicated deck-summary parser surface exists on the current
   branch, or route back if one has appeared.
4. Add the report-only manifest entry.
5. Add the report-only session ledger entry.
6. Add focused corpus parity assertions.
7. Run validation.
8. Write the implementation handoff and contract-test report.

## Compatibility

This contract preserves:

- corpus manifest schema version `parser_corpus_manifest.v1`;
- session ledger schema version `parser_corpus_session_ledger.v1`;
- scenario family id `deck_api.deck_summary`;
- coverage status vocabulary;
- coverage basis vocabulary;
- existing `DeckCollection` payload shape;
- existing `raw_start_hook` preservation;
- existing deck correlation behavior by `DeckId`;
- existing StartHook deck snapshot coverage;
- existing inventory/economy boundary;
- existing committed `deck_api.event_set_deck` coverage;
- adjacent missing deck API rows.

No migration is authorized.

## Tests Required

Focused validation for Codex C:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
git diff --check
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_deck_summary_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_deck_summary_coverage_comparison.md docs/contract_test_reports/parser_corpus_deck_summary_coverage.md | python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_deck_summary_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_deck_summary_coverage_comparison.md docs/contract_test_reports/parser_corpus_deck_summary_coverage.md | python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_deck_summary_coverage.md tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_deck_summary_coverage_comparison.md docs/contract_test_reports/parser_corpus_deck_summary_coverage.md | python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

Recommended broader validation if the environment is ready:

```bash
PYTHONPATH=src python3 -m ruff check src tests
```

Codex C must record any skipped validation and why.

## Acceptance Criteria

- `docs/contracts/parser_corpus_deck_summary_coverage.md` exists.
- Codex C updates only the corpus metadata/test/report surfaces authorized by
  this contract, unless it routes back.
- The corpus manifest validates cleanly.
- The session ledger validates cleanly.
- The corpus parity report still returns `partial_coverage_map_ready`.
- `deck_api.deck_summary` reports:
  - `coverage_status: covered_report_only`
  - `coverage_basis: ["fixture_metadata_only"]`
  - one Mythic Edge entry, `deck_summary_boundary_report_v1`
- `deck_api.start_hook_deck_snapshot` remains `covered_synthetic`.
- `deck_api.deck_upsert` remains `missing`.
- `deck_api.event_set_deck` remains `covered_committed`.
- `deck_api.store_pack_inbox_or_crafting` remains `missing`.
- Tests assert non-claims and adjacent deck API boundaries.
- No parser source or parser test changes are required.
- No raw/private/external/generated artifacts are committed.
- No protected parser/runtime/workbook/webhook/App Script/diagnostics/golden
  replay/feature-equity/evidence-ledger/analytics/AI/production behavior
  changes are made.
- The implementation handoff and contract-test report name remaining gaps.

## Open Questions And Suspected Gaps

- The selected report-only path proves that the deck-summary boundary is
  inspected, not that a dedicated deck-summary parser exists.
- If future code adds a standalone deck-summary parser, this family may need a
  new contract update before promotion to `covered_synthetic`.
- Dedicated deck upsert and store/pack/inbox/crafting surfaces remain separate
  future rows.
- Runtime deck matching and local active-deck summaries are downstream
  consumers and remain outside this corpus contract.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #394.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/394

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Base branch:
codex/parser-parity

Contract:
docs/contracts/parser_corpus_deck_summary_coverage.md

Goal:
Implement the smallest metadata/test/report-only change needed to satisfy the
deck summary corpus evidence boundary contract. Move only
`deck_api.deck_summary` from missing to `covered_report_only` using committed
boundary metadata. Do not change parser behavior and do not claim a dedicated
deck-summary API parser.

Before editing:
1. Fetch and verify `origin/codex/parser-parity`.
2. Create or use a clean implementation branch from `codex/parser-parity`.
3. Confirm PR #393 merged at
   `4658ae79cd861309b795f4be71912f65cf444bbd` or record the newer base.
4. Inspect `git status --short --branch`.
5. Leave unrelated or untracked local artifacts alone.

Read:
- docs/contracts/parser_corpus_deck_summary_coverage.md
- docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md
- docs/implementation_handoffs/parser_corpus_start_hook_deck_snapshot_coverage_comparison.md
- docs/contract_test_reports/parser_corpus_start_hook_deck_snapshot_coverage.md
- docs/contracts/parser_field_level_parity_audit.md
- docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- src/mythic_edge_parser/app/corpus_parity_report.py
- tests/test_corpus_parity_report.py
- src/mythic_edge_parser/parsers/collection.py
- tests/test_collection_parser.py

Do:
- Compare the current corpus parity report against the contract before editing.
- Confirm no dedicated deck-summary parser surface exists on the current branch,
  or route back if one has appeared.
- Add exactly one manifest entry for `deck_summary_boundary_report_v1`.
- Add the matching session ledger entry.
- Add focused tests proving `deck_api.deck_summary` is `covered_report_only`
  and adjacent deck API rows remain bounded.
- Produce
  `docs/implementation_handoffs/parser_corpus_deck_summary_coverage_comparison.md`.
- Produce
  `docs/contract_test_reports/parser_corpus_deck_summary_coverage.md`.

Do not:
- Change parser behavior.
- Change StartHook parser behavior, parser state final reconciliation, parser
  event classes, router semantics, diagnostics, drift reports, golden replay,
  feature-equity, evidence-ledger behavior, runtime surfaces, match/game
  identity, workbook/webhook or Apps Script behavior, analytics truth, AI
  truth, production behavior, CI gates, merge readiness, deploy readiness, or
  tracker lifecycle behavior.
- Cover `deck_api.deck_upsert` or `deck_api.store_pack_inbox_or_crafting` in
  issue #394.
- Alter `deck_api.start_hook_deck_snapshot` or `deck_api.event_set_deck`
  beyond adjacent boundary assertions.
- Claim a dedicated deck-summary API parser, private deck contents, private
  deck names, exact deck identity, submitted-deck truth, active-deck truth,
  sideboard-delta truth, collection ownership truth, inventory/economy state,
  decklist completion, archetype classification, hidden-card inference,
  gameplay advice, player-mistake labels, release readiness, analytics truth,
  AI truth, coaching truth, production behavior, full corpus parity, or parser
  support from corpus metadata alone.
- Import, copy, mirror, or commit external corpus contents or forbidden
  private/generated/local artifacts named by the contract.
- Target main directly.
- Close issue #394 or tracker #158.
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/394"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/392"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/393"
  previous_merge_commit: "4658ae79cd861309b795f4be71912f65cf444bbd"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_deck_summary_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_deck_summary_coverage_comparison.md"
  expected_report: "docs/contract_test_reports/parser_corpus_deck_summary_coverage.md"
  verdict: "contract_ready_for_report_only_deck_summary_boundary"
  risk_tier: "High"
  branch: "codex/parser-corpus-deck-summary-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "covered_report_only_boundary"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
    - "changed-file secret/private marker scan"
    - "changed-file protected-surface gate"
    - "changed-file validation selector"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not close issue #394."
    - "Do not claim full Mythic Edge corpus parity."
    - "Do not claim parser support from corpus metadata alone."
    - "Do not promote deck_api.deck_summary to covered_synthetic without contract loopback."
    - "Do not claim a dedicated deck-summary API parser."
    - "Do not cover deck_api.deck_upsert, deck_api.store_pack_inbox_or_crafting, or any other adjacent family in issue #394."
    - "Do not claim private deck contents, private deck names, exact deck identity, submitted-deck truth, active-deck truth, sideboard-delta truth, collection ownership truth, inventory/economy state, decklist completion, archetype classification, hidden-card inference, gameplay advice, player-mistake labels, release readiness, analytics truth, AI truth, coaching truth, production behavior, or tracker completion."
    - "Do not import, copy, mirror, or commit external corpus contents or forbidden private/generated/local artifacts named by the contract."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/diagnostics/golden-replay/feature-equity/evidence-ledger/analytics/AI/production surfaces without a new explicit contract."
```
