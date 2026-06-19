# Parser Corpus Companion / Large-Deck Behavior Uplift Contract

## Module

`gameplay_stress.companion_or_large_deck` parser corpus behavior uplift
planning.

Plain English: Mythic Edge already records companion / large-deck coverage as
report-only boundary metadata from issue #408. This contract defines the
narrowest safe path for moving the row toward parser-behavior readiness:
reduced synthetic deck-shape preservation evidence only. The uplift may prove
that existing parser surfaces preserve a companion-shaped deck field and a
large-deck-like submitted card-list shape. It must not claim companion
presence, companion legality, companion castability, large-deck truth, complete
decklist truth, hidden-card truth, analytics truth, AI truth, coaching truth,
readiness, production behavior, tracker completion, or full corpus parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/494
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/492
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/493
- Previous merge commit: `8d1e48c9c6bd0a20926829c2d7de1d516a24ac20`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/408
- Base branch inspected: `main`
- Contract branch:
  `codex/parser-corpus-companion-large-deck-behavior-uplift-494`
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
- `docs/contracts/parser_corpus_companion_large_deck_coverage.md`
- `docs/contracts/parser_corpus_store_pack_inbox_crafting_behavior_framing.md`
- `docs/contracts/parser_corpus_deck_summary_behavior_uplift.md`
- `docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md`
- `docs/contracts/parser_corpus_start_hook_deck_snapshot_coverage.md`
- `docs/contracts/player_log_evidence_ledger_tier3_deck_state.md`
- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
- `docs/contracts/player_log_evidence_ledger_tier5_card_identity.md`
- `docs/contracts/parser_client_actions.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `src/mythic_edge_parser/parsers/collection.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `tests/test_collection_parser.py`
- `tests/test_client_actions_parser.py`

## Purpose

Define the smallest safe evidence model for moving
`gameplay_stress.companion_or_large_deck` beyond the report-only boundary.

This contract answers:

- whether the row may move from `covered_report_only` toward
  `covered_synthetic`;
- what reduced synthetic parser evidence is sufficient;
- what `parser_behavior_verified` may and may not mean for this row;
- what fixture, manifest, session-ledger, parser, privacy, and readiness
  changes are allowed or forbidden; and
- how #388 / #381 activation remains deferred.

This contract does not implement code, create fixtures, edit corpus metadata,
run private/live MTGA checks, activate #388/#381, or claim companion /
large-deck parser support beyond reduced synthetic deck-shape preservation.

## Observed Current Behavior

Observed on `main` at
`8d1e48c9c6bd0a20926829c2d7de1d516a24ac20`:

- Issue #494 is open.
- Tracker #158 remains open.
- Related pipeline tracker #388 remains open and deferred.
- Parent private-evidence issue #434 remains open.
- Issue #492 is complete after PR #493.
- The corpus parity report state described by issue #494 is:

```text
partial_coverage_map_ready (45 families; committed=6, synthetic=16, report_only=17, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Current `gameplay_stress.companion_or_large_deck` row:

```yaml
scenario_family: "gameplay_stress.companion_or_large_deck"
coverage_status: "covered_report_only"
coverage_basis:
  - "fixture_metadata_only"
mythic_edge_entries:
  - "companion_large_deck_boundary_report_v1"
parser_event_families: []
parser_claim_families:
  - "companion_large_deck_boundary_report"
  - "generic_deck_snapshot_not_companion_or_large_deck"
  - "submitted_deck_cards_not_decklist_truth"
  - "card_identity_not_deck_shape_truth"
  - "companion_legality_not_claimed"
  - "decklist_completion_non_claim"
```

Current adjacent parser behavior:

- `src/mythic_edge_parser/parsers/collection.py` parses `StartHook`
  collection responses.
- `DeckCollection` is emitted only when list-shaped `DeckSummaries` and
  mapping-shaped `Decks` can be correlated by string `DeckId`.
- `DeckCollection` preserves the correlated deck payload under `list` and the
  raw StartHook payload under `raw_start_hook`.
- Existing tests already exercise StartHook deck payload preservation,
  including real-like deck payloads where `Companions` may appear as a raw deck
  list field.
- `src/mythic_edge_parser/parsers/client_actions.py` parses
  `ClientMessageType_SubmitDeckResp` as `submit_deck_resp`.
- Submit-deck parsing normalizes `deck_cards` and `sideboard_cards` integer
  lists from direct and nested submitted-deck payload shapes.
- Existing tests cover submit-deck list normalization, malformed list fallback,
  request context preservation, and raw payload preservation.

Current non-evidence:

- There is no committed dedicated companion fixture.
- There is no committed dedicated large-deck fixture.
- There is no parser-owned companion-legality detector.
- There is no parser-owned companion castability detector.
- There is no parser-owned full decklist, deck identity, or deck ownership
  detector.
- The current report-only row records zero dedicated companion fixtures, zero
  dedicated large-deck fixtures, zero companion-legality claims, and zero
  decklist-completion claims.
- The #408 boundary explicitly says adjacent deck/card surfaces do not prove
  companion presence, companion legality, large-deck size, complete decklists,
  deck identity, hidden-card truth, archetype classification, gameplay advice,
  analytics truth, AI truth, coaching truth, release readiness, or production
  behavior.

## Scope Decision

Recommended future path: reduced synthetic deck-shape behavior uplift.

A later Codex C implementation may move
`gameplay_stress.companion_or_large_deck` from `covered_report_only` toward
`covered_synthetic` with `parser_behavior_verified` only if it adds
Mythic Edge-owned synthetic evidence proving both:

1. existing StartHook deck-collection parsing preserves a companion-shaped
   deck payload field from an obviously synthetic deck payload; and
2. existing submit-deck parsing preserves and normalizes a large-deck-like
   submitted `deck_cards` list from an obviously synthetic payload.

The behavior claim is intentionally small:

- companion-shaped field preservation, not companion truth;
- large submitted-list shape preservation, not large-deck truth; and
- existing parser behavior, not new parser interpretation.

This contract authorizes a metadata/test/docs implementation path. It does not
authorize parser behavior changes. If Codex C cannot prove the reduced
synthetic deck-shape path using existing parser behavior, the row must remain
`covered_report_only` and route back to Codex B or Codex A.

## Owning Layer

Owning layer: Corpus / Provenance.

Supporting truth layers:

- Collection parsing owns StartHook `Collection` and `DeckCollection` event
  emission and raw deck payload preservation.
- Client-action parsing owns `SubmitDeckResp` event emission and submitted
  card-list normalization.
- Corpus parity reporting owns status aggregation and readiness metrics.

This contract does not move truth ownership to corpus metadata, workbook
formulas, dashboards, Apps Script, webhook transport, analytics, AI, coaching,
readiness, deploy, production, or tracker lifecycle surfaces.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser, as the existing producer of StartHook and submit-deck facts.
- Quality / Governance, as the owner of validation and protected-surface
  discipline.

This slice is not analytics, AI, coaching, workbook, webhook, Apps Script,
local app, release readiness, production behavior, private-evidence execution,
or parser-evidence pipeline activation.

## Truth Owner

Truth owner for current report-only status:

- `docs/contracts/parser_corpus_companion_large_deck_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for future reduced synthetic behavior evidence:

- `src/mythic_edge_parser/parsers/collection.py`
- `tests/test_collection_parser.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `tests/test_client_actions_parser.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- the future Codex C implementation handoff;
- the future Codex E contract-test report.

Truth boundary:

- A synthetic StartHook fixture may prove only that existing
  `DeckCollection` output preserves a companion-shaped payload field.
- A synthetic SubmitDeckResp fixture may prove only that existing
  `ClientAction` output preserves and normalizes a large-deck-like submitted
  card-list shape.
- The corpus row may claim `parser_behavior_verified` only for the reduced
  synthetic deck-shape preservation path described above.
- The corpus row must not claim companion presence, companion legality,
  companion castability, in-game companion availability, large-deck legality,
  large-deck submitted truth, complete decklist contents, exact deck identity,
  deck ownership, sideboard choice truth, hidden-card truth, archetype
  classification, matchup plans, gameplay advice, player mistakes, analytics
  truth, AI truth, coaching truth, private smoke success, release readiness,
  production behavior, #388/#381 activation, tracker completion, or full
  corpus parity.

## Bridge-Code Status

`bridge_code`

Source project area: Parser.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
owned synthetic StartHook and SubmitDeckResp deck-shape test inputs
  -> existing collection and client-action parser behavior
  -> focused parser test assertions
  -> corpus manifest/session-ledger behavior metadata
  -> corpus parity readiness metrics
```

Forbidden reverse flow:

- Corpus readiness must not change parser behavior.
- Corpus metadata must not create parser-owned facts absent from parser output.
- Corpus metadata must not force generic deck snapshots, submitted-deck lists,
  card identity evidence, StartHook summaries, public taxonomy labels, or local
  private deck material to mean companion / large-deck truth.
- Corpus metadata must not move decklists, companion legality, archetypes,
  analytics, AI, coaching, workbook, webhook, or Apps Script interpretation
  into parser truth.

Protected surfaces explicitly not touched:

- parser behavior;
- parser event classes;
- parser state final reconciliation;
- router semantics;
- match/game identity;
- deduplication;
- diagnostics behavior;
- drift report behavior;
- golden replay behavior;
- feature-equity behavior;
- evidence-ledger behavior;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- output transport;
- runtime status files;
- failed posts;
- workbook exports;
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

- `docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md`

Future Codex C files authorized only if implementation is selected:

- `tests/test_collection_parser.py`
- `tests/test_client_actions_parser.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_corpus_companion_large_deck_behavior_uplift_comparison.md`
- `docs/contract_test_reports/parser_corpus_companion_large_deck_behavior_uplift.md`

Files Codex C may inspect but must not change without contract loopback:

- `src/mythic_edge_parser/parsers/collection.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/corpus_parity_report.py`, except for focused
  report-test compatibility if metadata rendering requires it;
- adjacent corpus/evidence-ledger contracts and reports.

Not owned by this contract:

- parser semantics;
- new parser events;
- parser state final reconciliation;
- deck-state logic;
- submitted-deck runtime artifact behavior;
- card identity resolution;
- private evidence;
- external corpus contents;
- workbook/webhook/App Script/Sheets/analytics/AI/coaching surfaces.

## Public Interface

No runtime public API is added by Codex B.

Future Codex C may add committed synthetic test evidence and corpus metadata
that make the corpus parity public report show
`gameplay_stress.companion_or_large_deck` as behavior-ready in the limited
deck-shape sense. The intended eventual corpus row shape is:

```yaml
scenario_family: "gameplay_stress.companion_or_large_deck"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
```

The existing report-only entry `companion_large_deck_boundary_report_v1` should
remain as historical non-claim metadata unless Codex C has a strong reason to
route back for a replacement or migration contract. A new synthetic evidence
entry should be added rather than rewriting #408's boundary into a behavior
claim.

## Minimum Parser-Owned Evidence

Future uplift requires both synthetic evidence legs below.

### Companion-Shaped StartHook Evidence

Required:

- one focused synthetic StartHook collection/deck payload in
  `tests/test_collection_parser.py`;
- an obviously synthetic `DeckSummaries` entry and matching `Decks` mapping;
- a deck list payload that includes a `Companions` field with synthetic integer
  card identifiers or an equivalent obvious synthetic companion-shaped list
  supported by current parser behavior;
- emitted `DeckCollection` event;
- assertion that the correlated deck payload preserves the synthetic
  companion-shaped field under the existing raw/list payload boundary; and
- assertion that `raw_start_hook` is preserved.

Allowed:

- obvious synthetic deck IDs and names that cannot be mistaken for private
  local deck material;
- synthetic integer card IDs with no card-name, legality, ownership,
  collection, or strategy meaning.

Not sufficient:

- existing `Companions: []` preservation alone;
- StartHook `DeckSummaries` without a correlated deck payload;
- deck summary metadata with no companion-shaped field;
- corpus metadata asserting companion support without parser output.

Non-claims:

- no companion presence truth;
- no companion legality truth;
- no companion castability truth;
- no sideboard companion state truth;
- no in-game companion availability truth.

### Large-Deck-Like SubmitDeckResp Evidence

Required:

- one focused synthetic `ClientMessageType_SubmitDeckResp` payload in
  `tests/test_client_actions_parser.py`;
- a submitted `deck_cards` list with a clearly documented count greater than
  60, preferably using obvious synthetic integer card IDs;
- optional synthetic `sideboard_cards`, if helpful for existing parser shape;
- emitted `ClientAction` event with payload type `submit_deck_resp`;
- assertion that `deck_cards` preserves the full large-list shape and count;
- assertion that `sideboard_cards` preservation remains normal and bounded;
  and
- assertion that request context and raw payload preservation still follow the
  existing client-action contract.

Allowed:

- a reduced synthetic list long enough to prove list-shape handling, such as
  80 synthetic integers;
- synthetic IDs only, with no card names, deck names, deck IDs, deck hashes,
  private paths, strategy notes, or private decklists.

Not sufficient:

- a normal-size submit-deck payload;
- a malformed payload fallback to empty lists;
- submitted-deck card-content evidence alone;
- a list count used to claim deck legality, deck identity, or complete
  decklist truth.

Non-claims:

- no large-deck legality truth;
- no complete decklist truth;
- no submitted-deck finality truth beyond existing submitted-list evidence;
- no hidden-card truth;
- no archetype, matchup, analytics, AI, or coaching truth.

## Recommended Evidence / Status Path

Recommended Codex C path:

1. Add one focused collection parser test for companion-shaped StartHook deck
   payload preservation.
2. Add one focused client-action parser test for large-deck-like
   SubmitDeckResp list-shape preservation.
3. Add one new corpus manifest entry for the synthetic deck-shape behavior
   evidence.
4. Add one new session-ledger entry for the synthetic deck-shape behavior
   evidence.
5. Keep `companion_large_deck_boundary_report_v1` as report-only non-claim
   metadata.
6. Update focused corpus parity tests for the new status, entry list, claim
   families, summary row, and non-claims.
7. Write the implementation handoff and contract-test report.

Allowed future status movement:

- from `covered_report_only` to `covered_synthetic`;
- with `coverage_basis` including both `fixture_metadata_only` and
  `parser_behavior_verified`;
- only after both reduced synthetic evidence legs pass focused parser tests.

Disallowed in this lane:

- `covered_committed`, unless a later sanitized fixture-promotion issue
  explicitly creates a reviewed sanitized fixture;
- private/local-only evidence;
- external corpus evidence;
- status movement without both synthetic evidence legs;
- status movement based only on #408 report-only metadata, generic deck
  snapshots, submitted-deck card-content provenance, StartHook deck summaries,
  card identity provenance, public taxonomy metadata, or private deck material.

## Behavior-Uplift Packet

This packet applies only to
`gameplay_stress.companion_or_large_deck`. It is a reusable pattern note for
future behavior-uplift rows, but it must not be used here to solve, promote,
or reclassify any other corpus row.

| Question | Contracted answer for #494 |
| --- | --- |
| Scenario family | `gameplay_stress.companion_or_large_deck` |
| Current status and basis | `covered_report_only` with `fixture_metadata_only` through `companion_large_deck_boundary_report_v1` |
| Target status, if any | `covered_synthetic` only after both reduced synthetic deck-shape parser tests pass |
| May `parser_behavior_verified` be added? | Yes, but only to a new synthetic evidence entry and only for companion-shaped field preservation plus large-list shape preservation |
| Evidence type | Synthetic committed parser-focused tests preferred; private-gated and external-gated evidence are forbidden in this lane |
| Fixture/golden replay changes | Focused parser tests are allowed; golden replay fixture changes are not required for V1 and should not be added unless Codex C can justify them without changing report or parser behavior |
| Manifest/session-ledger changes | Additive entries citing this contract are allowed; changing unrelated rows or removing #408 report-only boundary metadata is forbidden |
| Parser behavior changes | Forbidden; if existing parser behavior cannot support the reduced evidence path, route back instead of changing parser behavior |
| Private/external inputs | Private Player.log, UTC_Log, live MTGA, private decks, decklists, Manasight/external raw corpora, private reports, and generated/private artifacts are forbidden |
| Required non-claims | No companion presence, companion legality, companion castability, in-game companion availability, large-deck legality, complete decklist, deck identity, deck ownership, hidden-card, archetype, gameplay advice, analytics truth, AI truth, coaching truth, private smoke, release readiness, production behavior, full corpus parity, tracker completion, or #388/#381 activation claims |
| Focused validation | Collection parser tests, client-action parser tests, corpus parity report/tests, docs check, ruff, diff check, path-scoped secret scan, path-scoped protected-surface scan |
| #388/#381 stop condition | Do not activate #388 or #381 from this row; the row may improve readiness counts but does not start the parser-evidence pipeline by itself |

Future behavior-uplift contracts may copy this packet shape, but each future
row still needs its own issue, contract, evidence decision, non-claims, and
validation plan.

## Required Future Manifest Entry Shape

The exact `entry_id` may vary, but future Codex C should prefer:

```yaml
entry_id: "companion_large_deck_synthetic_deck_shape_v1"
title: "Companion / large-deck synthetic deck-shape parser evidence"
entry_type: "focused_parser_tests"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
scenario_families:
  - "gameplay_stress.companion_or_large_deck"
parser_event_families:
  - "DeckCollection"
  - "ClientAction"
parser_claim_families:
  - "synthetic_companion_shape_field_preservation"
  - "synthetic_large_deck_list_shape_preservation"
  - "deck_shape_preservation_not_deck_identity_truth"
  - "companion_legality_non_claim"
  - "decklist_completion_non_claim"
  - "hidden_card_non_claim"
coverage_status: "covered_synthetic"
coverage_basis:
  - "fixture_metadata_only"
  - "parser_behavior_verified"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/494"
authorized_by_contract: "docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md"
```

Required known-gap language:

- The fixture proves reduced synthetic deck-shape preservation only.
- It does not prove companion presence, companion legality, companion
  castability, live MTGA companion behavior, large-deck legality, complete
  decklists, exact deck identity, hidden-card truth, archetype classification,
  gameplay advice, analytics truth, AI truth, coaching truth, release
  readiness, or production behavior.
- The #408 `companion_large_deck_boundary_report_v1` entry remains report-only
  non-claim metadata.

Required `paths` should include:

```yaml
paths:
  collection_parser_test: "tests/test_collection_parser.py"
  client_actions_parser_test: "tests/test_client_actions_parser.py"
  corpus_parity_test: "tests/test_corpus_parity_report.py"
```

## Required Future Session-Ledger Shape

The exact `session_id` may vary, but future Codex C should prefer:

```yaml
session_id: "companion_large_deck_synthetic_deck_shape_v1"
title: "Companion / large-deck synthetic deck-shape parser evidence"
source_kind: "synthetic_committed_fixture"
commit_status: "committed"
privacy_class: "synthetic_committable"
sanitization_status: "synthetic"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/494"
authorized_by_contract: "docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md"
scenario_families:
  - "gameplay_stress.companion_or_large_deck"
format_family: "gameplay_stress"
match_shape: "companion_large_deck_synthetic_deck_shape"
record_summary: "committed_synthetic_companion_and_large_deck_shape_parser_tests"
```

Required session-ledger `parser_coverage` facts:

```yaml
parser_coverage:
  event_families:
    DeckCollection: 1
    ClientAction: 1
  unknown_entries: 0
  truncation_count: 0
  synthetic_companion_shape_fixtures: 1
  synthetic_large_deck_shape_fixtures: 1
  companion_legality_claims: 0
  companion_castability_claims: 0
  large_deck_legality_claims: 0
  decklist_completion_claims: 0
  deck_identity_claims: 0
```

Required session-ledger game row summary:

```yaml
game_rows:
  count: 0
  result_shape: "not_applicable"
```

Required redaction and privacy facts:

- no raw/private Player.log excerpts
- no external corpus payloads
- no private decklists
- no raw submitted-deck payloads from private/local logs
- no deck names from private/local logs
- no deck IDs from private/local logs
- no sideboard choices from private/local logs
- no companion candidates from private/local logs
- no card choices from private/local logs
- no strategy notes
- no local smoke outputs
- no generated/private/runtime artifacts
- no credentials, tokens, API keys, or webhook URLs

## Inputs

Allowed inputs:

- Existing committed parser source and focused parser tests for collection and
  client-action parsing.
- New obvious synthetic payloads embedded in focused tests.
- Existing committed corpus parity manifest and session ledger.
- Existing committed contracts and reports for companion / large-deck
  boundary, StartHook deck snapshots, submitted-deck card-content provenance,
  card identity provenance, deck-state deferral, and behavior readiness.
- Public Manasight metadata only as already merged taxonomy/category context,
  not as raw evidence.

Forbidden inputs:

- Manasight raw logs, `.log.gz` files, compressed corpus files, raw session
  payloads, external corpus contents, hash lists, byte-size row lists,
  capture-date row lists, or parser source.
- Private Player.log excerpts, UTC_Log excerpts, private local logs, raw
  submitted-deck payloads from private evidence, raw decklists, sealed pools,
  deck names, deck IDs, companion choices, sideboard choices, card choices,
  strategy notes, private smoke reports, local runtime artifacts, generated
  data, SQLite files, workbook exports, secrets, credentials, tokens, API
  keys, or webhook URLs.
- Model-provider output or AI interpretation.

## Outputs

Authorized outputs for Codex C:

- Focused parser tests proving the two reduced synthetic evidence legs.
- One corpus manifest entry for the new reduced synthetic deck-shape evidence.
- One session-ledger entry for the new reduced synthetic deck-shape evidence.
- Focused corpus parity tests proving the row moves to `covered_synthetic`
  with the required non-claims.
- An implementation handoff and contract-test report.

Forbidden outputs:

- committed raw or synthetic gameplay log slices, unless a later contract
  explicitly authorizes golden replay coverage;
- committed private decklists;
- committed private deck names or private deck IDs;
- committed real companion candidates or real card choices;
- new parser event classes;
- new parser route behavior;
- new runtime files;
- new workbook/export/webhook/App Script fields;
- new analytics tables/views;
- AI/model-provider outputs;
- release-readiness, deploy-readiness, production-readiness, tracker-completion,
  or full-parity verdicts.

## Invariants

- `gameplay_stress.companion_or_large_deck` may move to `covered_synthetic`
  only if both reduced synthetic evidence legs pass.
- `coverage_basis` for the new synthetic entry must include
  `parser_behavior_verified`.
- Existing #408 report-only metadata must remain available as a non-claim
  boundary.
- Parser event families for the new synthetic entry must be limited to
  existing parser event kinds, expected as `DeckCollection` and `ClientAction`.
- Synthetic companion-shaped field preservation is not companion presence,
  legality, or castability.
- Synthetic large-list preservation is not large-deck legality, complete
  decklist truth, or deck identity truth.
- Card IDs used in tests must be obvious synthetic integers with no card-name,
  ownership, deck identity, legality, archetype, or strategy meaning.
- Public taxonomy metadata is not parser support evidence.
- Local private or large-looking deck material must not be committed.
- Corpus parity status must not become parser truth, deck-state truth,
  submitted-deck truth, analytics truth, AI truth, coaching truth, merge
  readiness, deploy readiness, release readiness, production behavior, #388
  activation, #381 activation, or tracker-completion authority.

## Error Behavior

Malformed manifest or session-ledger data must fail existing corpus parity
validation tests. Codex C must not add permissive parsing that silently accepts
ambiguous coverage claims.

If implementation discovers that current parser behavior cannot preserve the
contracted companion-shaped field or large-list shape without source changes,
Codex C must stop and route back. This contract does not authorize parser
behavior changes.

If implementation discovers that the corpus report cannot represent the
contracted synthetic evidence without a small report-only adjustment, Codex C
may make the smallest corpus-report-only code change and document it. That
change must not affect parser behavior or protected surfaces.

If private evidence would be needed to make a stronger claim, the row must not
be promoted from private evidence in this lane. Private evidence must stay out
of the repo and out of GitHub issue comments.

## Side Effects

Allowed future Codex C side effects:

- Add focused synthetic parser tests.
- Edit committed corpus parity metadata.
- Edit focused corpus parity tests.
- Write implementation handoff and contract-test report docs.

Forbidden side effects:

- opening or closing issues;
- opening a PR unless separately asked;
- staging or committing unless separately asked;
- changing parser behavior;
- changing parser event classes;
- creating runtime/generated/private artifacts;
- committing local logs or raw private evidence;
- changing CI gates, merge policy, deploy policy, production behavior, or
  final integration policy.

## Dependency Order

Codex C should make changes in this order:

1. Confirm branch and base state against `main`.
2. Compare current manifest/session-ledger/report behavior against this
   contract.
3. Add focused collection parser test for synthetic companion-shaped field
   preservation.
4. Add focused client-action parser test for synthetic large-list shape
   preservation.
5. Add the new corpus manifest entry.
6. Add the new session-ledger entry.
7. Update focused corpus parity tests for status, claim families, non-claims,
   summary counts, and readiness metrics.
8. Run focused validation.
9. Write the implementation handoff and contract-test report.
10. Run docs/protected-surface/secret checks on changed files.

## Compatibility

Compatibility expectations:

- Existing #408 report-only entry remains as non-claim boundary metadata.
- Existing covered families and summary counts must remain stable except for
  the status/count deltas authorized by this contract.
- Current report semantics for `covered_committed`, `covered_synthetic`,
  `covered_report_only`, `partial`, `missing`, `blocked_private_evidence`, and
  `blocked_external_boundary` must remain compatible.
- Existing entries for StartHook deck snapshot, deck summary, deck upsert,
  submitted-deck card-content provenance, card identity provenance, and
  deck-state deferral must not be reinterpreted.
- No report consumer may treat this row as companion legality, castability,
  large-deck legality, complete decklist, deck identity, hidden-card,
  analytics, AI, coaching, release, deploy, production, or full-parity truth.

Expected summary-count delta after Codex C, relative to issue #494 state:

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
PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_client_actions_parser.py tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md tests/test_collection_parser.py tests/test_client_actions_parser.py tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_companion_large_deck_behavior_uplift_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_behavior_uplift.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md tests/test_collection_parser.py tests/test_client_actions_parser.py tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_corpus_companion_large_deck_behavior_uplift_comparison.md docs/contract_test_reports/parser_corpus_companion_large_deck_behavior_uplift.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
```

Codex E should also inspect:

- that no parser source files changed;
- that both synthetic evidence legs are present;
- that all companion / large-deck non-claims remain visible in manifest,
  session ledger, report output, handoff, and contract-test report;
- that #388/#381 activation remains false/deferred; and
- that no private/external/raw/generated artifacts were committed.

## Acceptance Criteria

- `docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md`
  exists and records the reduced synthetic deck-shape evidence model.
- Codex C can implement the contract with focused tests, corpus
  metadata/tests, and docs only.
- The new synthetic entry proves both companion-shaped StartHook field
  preservation and large-list SubmitDeckResp preservation through existing
  parser behavior.
- `gameplay_stress.companion_or_large_deck` may move to `covered_synthetic`
  only with `parser_behavior_verified` tied to the reduced deck-shape claim.
- The #408 report-only boundary remains as non-claim metadata.
- No parser behavior or protected surface changes are authorized.
- No raw/private/external corpus contents, decklists, private deck names,
  private deck IDs, real companion choices, local smoke outputs, or generated
  private artifacts are committed.
- No readiness, production, analytics, AI, coaching, #388/#381 activation,
  tracker-completion, or full-parity claims are made.

## Unknowns

- The exact synthetic card ID count for the large-list test can be chosen by
  Codex C, but it must be greater than 60 and small enough to keep the test
  readable.
- The existing corpus report may need only metadata/test updates; if a report
  rendering edge case appears, Codex C may make a small report-only adjustment
  and must document it.
- The reduced synthetic evidence does not answer whether Mythic Edge should
  ever implement companion legality or large-deck classification.

## Suspected Gaps

- Adjacent deck evidence surfaces are easy to overread as deck-state truth.
- A future product-grade companion feature would need a separate parser
  behavior contract for actual companion semantics.
- A future product-grade large-deck feature would need a separate parser
  behavior contract for explicit deck-size semantics, if Mythic Edge ever wants
  that.
- The row may become behavior-ready in a narrow synthetic sense while still
  remaining far from live/private companion or large-deck validation.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #494, companion / large-deck behavior uplift, under tracker #158.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/494

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related parser-evidence pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/492

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/493

Previous merge commit:
8d1e48c9c6bd0a20926829c2d7de1d516a24ac20

Prior boundary issue:
https://github.com/Tahjali11/Mythic-Edge/issues/408

Base branch:
main

Contract:
docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md

Goal:
Implement the smallest focused test, corpus metadata/test, and docs package needed to satisfy the contract. This is reduced synthetic deck-shape preservation evidence for `gameplay_stress.companion_or_large_deck`, not companion presence, companion legality, companion castability, large-deck legality, complete decklist truth, deck identity truth, analytics truth, AI truth, coaching truth, readiness, production behavior, #388/#381 activation, tracker completion, or full corpus parity.

Expected files:
- tests/test_collection_parser.py
- tests/test_client_actions_parser.py
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_companion_large_deck_behavior_uplift_comparison.md
- docs/contract_test_reports/parser_corpus_companion_large_deck_behavior_uplift.md

Required implementation:
- Add one focused synthetic StartHook/DeckCollection test proving existing parser behavior preserves a companion-shaped deck payload field from obvious synthetic data.
- Add one focused synthetic SubmitDeckResp/ClientAction test proving existing parser behavior preserves and normalizes a large-deck-like `deck_cards` list with a count greater than 60.
- Add one new corpus manifest entry, preferably `companion_large_deck_synthetic_deck_shape_v1`.
- Add one new session-ledger entry for the same synthetic deck-shape evidence.
- Move `gameplay_stress.companion_or_large_deck` only to `covered_synthetic` with coverage basis including `fixture_metadata_only` and `parser_behavior_verified`.
- Keep `companion_large_deck_boundary_report_v1` as report-only non-claim boundary metadata.
- Preserve explicit non-claims for companion presence, companion legality, companion castability, in-game companion availability, large-deck legality, complete decklist truth, deck identity, deck ownership, sideboard choice truth, hidden-card truth, archetype classification, gameplay advice, analytics truth, AI truth, coaching truth, private smoke success, release readiness, production behavior, #388/#381 activation, tracker completion, and full corpus parity.

Do not:
- Target main directly.
- Close tracker #158, #388, #434, or issue #494.
- Activate #388 or #381.
- Change parser behavior, parser event classes, parser state final reconciliation, router semantics, match/game identity, diagnostics, drift, golden replay, feature-equity, evidence-ledger, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics truth, AI/model-provider behavior, coaching behavior, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy.
- Import, copy, mirror, summarize, or commit Manasight raw logs, compressed corpus files, parser source, external corpus contents, private Player.log excerpts, private local logs, raw submitted-deck payloads from private evidence, decklists, deck names, deck IDs, companion choices, sideboard choices, card choices, strategy notes, private smoke reports, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, or webhook URLs.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_collection_parser.py tests/test_client_actions_parser.py tests/test_corpus_parity_report.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- path-scoped secret scan for changed files
- path-scoped protected-surface scan for changed files
- python3 -m ruff check src tests tools
- git diff --check

If existing parser behavior cannot support the two reduced synthetic evidence legs without parser code changes, stop and route back to Codex B or Codex A. Do not change parser behavior in this lane.
```

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/494"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/492"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/493"
  previous_merge_commit: "8d1e48c9c6bd0a20926829c2d7de1d516a24ac20"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/408"
  completed_thread: "B"
  next_thread: "C"
  verdict: "companion_large_deck_behavior_uplift_contract_ready"
  risk_tier: "High"
  base_branch: "main"
  target_artifact: "docs/implementation_handoffs/parser_corpus_companion_large_deck_behavior_uplift_comparison.md"
  contract_artifact: "docs/contracts/parser_corpus_companion_large_deck_behavior_uplift.md"
  selected_family: "gameplay_stress.companion_or_large_deck"
  current_status: "covered_report_only"
  authorized_target_status: "covered_synthetic"
  parser_behavior_ready_after_contract: "conditional_on_codex_c_synthetic_deck_shape_tests"
  pipeline_activation_ready_for_issue_388: false
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #158, #388, #434, or issue #494."
    - "Do not activate #388 or #381."
    - "Do not change parser behavior or protected parser/runtime/workbook/webhook/App Script/analytics/AI/coaching/production surfaces."
    - "Do not claim companion presence, companion legality, companion castability, large-deck legality, complete decklist truth, deck identity truth, hidden-card truth, analytics truth, AI truth, coaching truth, readiness, production behavior, tracker completion, or full corpus parity."
    - "Do not commit private/external/raw/generated artifacts, decklists, deck names, deck IDs, companion choices, strategy notes, secrets, credentials, tokens, API keys, or webhook URLs."
