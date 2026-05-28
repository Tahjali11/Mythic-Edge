# Player.log Evidence Ledger Tier 4 Deck-State Boundary Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/161
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/159
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/160
- previous_merge_commit: 06b3268258b4c35ec447362a6e9db5f089996836
- base_branch: codex/parser-reliability-intelligence
- target_artifact: docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier4_deck_state_boundary_comparison.md
- risk_tier: High
- status: contract only

Required agent docs:

- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md

Related authority:

- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md
- docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md

## Purpose

Issue #161 defines the Tier 4 broad deck-state provenance boundary for the
Player.log evidence ledger.

The prior Tier 4 slices mapped:

- `sideboarding_entered`
- `submit_deck_seen`
- `submitted_deck_cards`

Those fields are real parser-managed provenance surfaces, but they still do
not prove broad active deck state. This contract explains what submitted-deck,
runtime deck, collection matching, card catalog, decklist, and GRP candidate
evidence can and cannot prove before Mythic Edge advances to Tier 5 card
identity and gameplay-action provenance.

Plain English: Mythic Edge can say "we saw this submitted deck list-shaped
evidence" without saying "we know the full active deck, exact sideboard deltas,
deck name, archetype, collection ownership, card names, or gameplay advice."

This is a boundary contract. It does not authorize parser behavior changes.

## Scope Decision

Broad `deck_state` must remain explicitly deferred.

Codex C should not add a new seeded `deck_state` field, a new
`tier4.deck_state.*` ledger entry, or a fake boundary-only parser-truth entry in
issue #161.

Reason:

- The current evidence ledger schema validates entries as parser-managed truth:
  `validate_ledger_entry(...)` requires `parser_managed_truth is True`.
- A broad deck-state boundary is not itself a parser-owned game fact.
- Promoting a boundary note into a truth entry would make the ledger appear to
  own a fact it is deliberately refusing to claim.

Allowed issue #161 implementation shape:

- Keep Tier 3 `game_level_facts.future_fields` containing `deck_state`.
- Keep Tier 4 `sideboarding_and_deck_state.seed_fields` exactly:
  - `sideboarding_entered`
  - `submit_deck_seen`
  - `submitted_deck_cards`
- Keep Tier 4 `sideboarding_and_deck_state.future_fields` empty.
- Add or refine Tier 4 family notes documenting the deck-state boundary.
- Add focused tests proving the boundary is durable and the existing seed
  fields are not expanded.

If a future issue wants boundary-only ledger entries, it must first amend the
ledger schema to support non-parser-truth boundary metadata without weakening
existing parser-truth validation.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- `src/mythic_edge_parser/parsers/client_actions.py` owns parsed
  `ClientMessageType_SubmitDeckResp` events and normalized `deck_cards` /
  `sideboard_cards` payload paths.
- `src/mythic_edge_parser/app/evidence_ledger.py` owns provenance metadata,
  confidence/finality/degradation language, drift flags, and protected
  boundary notes.
- `src/mythic_edge_parser/app/diagnostics.py` may derive active submitted-deck
  artifacts, counts, and signatures from normalized submit-deck payloads.
- `src/mythic_edge_parser/app/runtime_surfaces.py` may keep latest-observed
  runtime deck state, active deck profiles, collection matches, and missing
  card reports.
- `src/mythic_edge_parser/app/card_catalog.py` and GRP catalog helpers may
  resolve or enrich card IDs for display/review.
- `src/mythic_edge_parser/app/decklists.py` may load local decklist reference
  material.
- `src/mythic_edge_parser/app/grp_id_candidates.py` may build review-oriented
  candidate reports from submitted-deck snapshots and related evidence.
- Workbook formulas, dashboards, webhook transport, Apps Script, analytics,
  archetype classification, matchup plans, gameplay advice, player-mistake
  labels, and AI/model-provider output are downstream consumers only.

The evidence ledger describes support and uncertainty. It must not become a
second parser, a deck classifier, a collection oracle, or an AI truth layer.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier4_deck_state_boundary_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier4_deck_state_boundary.md

Referenced but not silently owned:

- src/mythic_edge_parser/parsers/client_actions.py
- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/grp_id_candidates.py
- src/mythic_edge_parser/app/card_catalog.py
- src/mythic_edge_parser/app/decklists.py
- src/mythic_edge_parser/app/sheet_exports.py
- src/mythic_edge_parser/app/sheet_schema.py
- tests/test_diagnostics.py
- tests/test_runtime_surfaces.py
- tests/test_grp_id_candidates.py
- tests/test_sheet_schema.py

## Observed Current Behavior

Observed on `codex/parser-reliability-intelligence` at
`06b3268258b4c35ec447362a6e9db5f089996836`:

- Issue #159 / PR #160 is merged.
- The Tier 4 `sideboarding_and_deck_state` family is `seeded_sample`.
- Tier 4 seed fields are:
  - `sideboarding_entered`
  - `submit_deck_seen`
  - `submitted_deck_cards`
- Tier 4 future fields are empty.
- Tier 3 `game_level_facts.future_fields` still contains `deck_state`.
- `tests/test_evidence_ledger.py` already asserts that no
  `tier4.deck_state.*` entry exists.
- The `submitted_deck_cards` entry states that submitted deck lists are
  observed normalized `grpId` list content, not broad deck-state truth.
- The `submitted_deck_cards` entry treats counts and submitted-deck signature
  as derived facets inside the entry, not separate ledger fields.
- `diagnostics.record_submitted_deck(...)` can write a local
  `manasight_active_submitted_deck` artifact from non-empty normalized
  submitted deck lists.
- `runtime_surfaces.py` can normalize active deck state, cache latest observed
  deck context, build active deck profiles, match active deck state to local
  deck collections, and build collection/missing-card summaries.
- `grp_id_candidates.py` can load an active submitted-deck artifact, scan saved
  match logs for the latest submitted-deck snapshot, and build candidate
  reports for review.
- Runtime deck profiles and collection profiles include volatile generated
  timestamps and local artifact paths, so they are not stable ledger truth
  records.

Observed risks:

- A latest runtime active-deck snapshot can look like durable deck-state truth
  even when it is only latest-observed operational state.
- A submitted-deck signature can look like a deck identity even though it is
  only a deterministic hash of normalized submitted lists.
- A collection/deck match can look like a Player.log fact even though it is an
  enrichment comparison against local collection/deck artifacts.
- Card catalog resolution can look like observed card-name truth even though
  Tier 5 card identity provenance has not been mapped yet.
- GRP candidate reports can look like authoritative card identity or deck
  alignment, but they are review support only.

## Required V1 Behavior

### Existing Seed Fields

The following Tier 4 seed fields remain parser-managed truth metadata:

| Field | Meaning | Not allowed to prove |
| --- | --- | --- |
| `sideboarding_entered` | Parser observed a sideboarding-entry signal for the current match. | Changed cards, sideboard deltas, deck identity, sideboard quality, archetype, advice. |
| `submit_deck_seen` | Parser observed a submit-deck signal for the current match. | Submitted card content, complete deck state, deck name, decklist identity, sideboard deltas. |
| `submitted_deck_cards` | Parser observed non-empty normalized submitted mainboard/sideboard `grpId` list content from a submit-deck response. | Broad deck state, card-name truth, deck identity, collection ownership, exact sideboard deltas, archetype, advice. |

### Broad Deck State

`deck_state` remains deferred and means future work only.

No issue #161 implementation may claim:

- complete active decklist truth
- exact active deck identity
- exact submitted deck by game
- exact sideboard cards brought in or out
- hidden cards
- deck name or deck ID truth
- format or match mode truth
- collection ownership truth
- card-name truth
- archetype classification
- matchup plan
- sideboard-plan quality
- gameplay advice
- player mistake labels
- model-provider or AI truth

## Evidence Boundary Matrix

| Evidence surface | Can prove | Cannot prove | Source label |
| --- | --- | --- | --- |
| Submit-deck `ClientAction` with `payload.deck_cards` / `payload.sideboard_cards` | Observed event-scoped submitted `grpId` list content when non-empty and normalized. | Complete active deck state, deck identity, card names, collection ownership, sideboard deltas, hidden cards. | `observed` |
| Request context / event timestamp | Provenance context for the submit-deck event. | Card content truth by itself, final deck state, per-game deck state. | `observed` for the context path, provenance only |
| Derived mainboard/sideboard counts | Counts derived from normalized submitted lists. | Separate ledger fields, complete deck truth, deck validity, deck identity. | `derived` |
| Submitted-deck signature | Deterministic signature derived from normalized submitted lists. | Named deck identity, decklist alignment, archetype, gameplay quality. | `derived` |
| Active submitted-deck artifact | Local derived snapshot of latest non-empty submitted-deck payload. | Source evidence by itself, all-game final deck state, workbook truth. | `derived` fallback |
| Runtime `_ACTIVE_DECK_STATE` / match deck context | Latest-observed operational cache and optional match context. | Durable source fact without event linkage, final reconciliation truth, complete deck state. | `derived` fallback |
| Active deck profile | Local profile derived from runtime active deck state plus catalog/collection enrichment. | Parser-owned card-name truth, collection ownership truth, archetype, advice. | `derived` / `legacy_enriched` as future metadata only |
| Collection/deck matching | Best-effort enrichment comparing active deck counters to local DeckCollection/Collection payloads. | Player.log fact, exact deck identity, ownership truth, match result truth. | enrichment only; do not use as parser truth |
| Card catalog lookup | Display/review resolution for card IDs when catalog data is available. | Tier 5 observed card identity truth, hidden card proof, gameplay-action truth. | enrichment only |
| Local decklist reference | User/imported reference material for comparison. | Arena active deck truth, submitted deck truth, parser-owned card evidence. | enrichment/reference only |
| GRP candidate report | Review support for candidate card ID/name reconciliation. | Authoritative card identity, collection ownership, deck state, gameplay truth. | review support only |
| Workbook, Apps Script, dashboard, analytics, AI | Downstream transport, display, analysis, or explanation. | Parser truth, evidence ownership, final deck state, gameplay advice as fact. | not source evidence |

## Confidence, Finality, And Degradation Rules

High confidence:

- Direct observed `ClientAction` submit-deck evidence with
  `type == "submit_deck_resp"` and at least one non-empty normalized
  `deck_cards` or `sideboard_cards` list.

Medium confidence:

- Counts and signatures derived from high-confidence normalized submitted
  lists.
- Runtime active submitted-deck artifacts when they can be traced back to a
  submit-deck event and current match context.

Low confidence / review required:

- Runtime active deck state without source-event linkage.
- Raw preserved payload paths when normalized lists are empty or unavailable.
- Runtime artifact, collection match, and GRP candidate report disagreement.
- Collection/deck matching that depends on stale, partial, or local-only
  collection/decklist data.

Unknown or degraded:

- No submit-deck event.
- Submit-deck event with both normalized lists empty.
- Missing, malformed, non-list, boolean, object, truncated, summarized,
  rotated, stale, or disconnected deck evidence.
- Runtime cache exists but lacks match context or event timestamp linkage.
- Card catalog, decklist, collection, or GRP candidate inputs are unavailable.

Finality:

- Submit-deck event evidence is event-scoped.
- Runtime active-deck snapshots are provisional latest-observed state.
- Saved event/log replay can preserve event-scoped evidence, but this does not
  convert it into final broad deck-state truth.
- `reconciled` should be reserved for future field-evidence records corrected
  by stronger later evidence. Issue #161 does not implement such attachment.

## Required Invariants

Codex C should preserve or add tests for these invariants:

- `deck_state` remains deferred in Tier 3.
- No `tier4.deck_state.*` entry exists in issue #161.
- Tier 4 seed fields remain exactly `sideboarding_entered`,
  `submit_deck_seen`, and `submitted_deck_cards`.
- `submitted_deck_cards` remains the only Tier 4 card-content field.
- Counts and submitted-deck signature remain derived facets, not separate
  ledger fields.
- Runtime active deck state and active submitted-deck artifacts remain derived
  fallback surfaces only.
- Collection/deck matching remains enrichment only.
- Card catalog resolution remains enrichment only until Tier 5 maps card
  identity provenance.
- Local decklists remain reference material only.
- GRP candidate reports remain review support only.
- Disagreement between submitted payloads, runtime artifacts, collection
  matches, decklists, card catalog, and GRP candidates produces review-required
  or degraded provenance, not stronger truth.
- Workbook formulas, webhook transport, Apps Script, dashboards, analytics,
  and AI/model-provider output must not populate deck-state truth.
- Ledger metadata must remain `path_only_no_values` and must not serialize raw
  private log excerpts, raw payload values, real card IDs, deck names, deck IDs,
  local artifact contents, runtime status files, or generated data.

Recommended new invariant names for family notes/tests:

- `deck_state_boundary_keeps_deck_state_deferred`
- `deck_state_boundary_no_tier4_deck_state_entry`
- `deck_state_boundary_runtime_artifacts_are_derived_latest_observed_only`
- `deck_state_boundary_collection_matching_is_enrichment_only`
- `deck_state_boundary_catalog_decklist_grp_candidates_are_not_parser_truth`
- `deck_state_boundary_conflicts_require_review`
- `deck_state_boundary_no_hidden_cards_archetypes_advice_or_ai_truth`

These names may appear in tests or notes. They should not become new ledger
entries in issue #161.

## Protected Surfaces

Do not change:

- parser behavior
- client-action parsing behavior
- parser state final reconciliation
- parser event classes
- router behavior
- match identity
- game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- output transport
- runtime status file shape or writes
- failed-post behavior
- workbook exports
- production behavior
- diagnostics behavior
- replay behavior
- drift detector behavior
- GRP candidate scoring behavior
- card catalog sync behavior
- decklist parsing behavior
- analytics truth
- AI truth
- OpenAI or model-provider runtime behavior
- secrets, environment variables, API keys, tokens, or webhook URLs
- raw private Player.log excerpts
- generated card data or local runtime artifacts

## Side Effects

Allowed for Codex C:

- Update `src/mythic_edge_parser/app/evidence_ledger.py` notes only if needed
  to make the deck-state boundary durable.
- Update `tests/test_evidence_ledger.py` focused metadata tests.
- Produce
  `docs/implementation_handoffs/player_log_evidence_ledger_tier4_deck_state_boundary_comparison.md`.

Forbidden for Codex C:

- Adding parser behavior.
- Adding new runtime artifacts.
- Reading, copying, summarizing, or committing raw private logs.
- Adding card IDs, deck names, deck IDs, collection contents, or raw payload
  values to the ledger.
- Adding workbook/webhook/App Script fields.
- Adding a new parser event kind or payload shape.
- Adding Draft, card identity, gameplay action, archetype, coaching, or AI
  behavior.

## Required Tests For Codex C

Focused tests in `tests/test_evidence_ledger.py` should prove:

- Tier 3 `future_fields` still contains `deck_state`.
- Tier 4 `seed_fields` are exactly the existing three fields.
- Tier 4 `future_fields` stays empty.
- No ledger entry starts with `tier4.deck_state.`.
- No new ledger output field named `deck_state`, `active_deck_state`,
  `deck_identity`, `deck_name`, `deck_id`, `sideboard_delta`,
  `card_name`, `collection_ownership`, `archetype`, `matchup_plan`,
  `gameplay_advice`, or `player_mistake_label` exists.
- Tier 4 family notes explicitly document the issue #161 broad deck-state
  boundary.
- The `submitted_deck_cards` entry continues to document runtime active deck
  state, active deck profile, and GRP candidate report only as downstream or
  fallback surfaces, not source truth.
- Counts and signature remain derived facets in `submitted_deck_cards`.
- Ledger privacy validation still rejects raw-log-like text and absolute local
  paths.
- Built-in ledger and entries validate cleanly.
- Existing Tier 1, Tier 3, #151, and #159 entries remain present and valid.

Recommended focused validation for Codex C:

```powershell
py -m pytest -q tests\test_evidence_ledger.py
py -m ruff check src tests tools
git diff --check
```

Optional adjacent validation if Codex C touches or suspects adjacent metadata:

```powershell
py -m pytest -q tests\test_diagnostics.py tests\test_runtime_surfaces.py tests\test_grp_id_candidates.py
py -m pytest -q tests\test_sheet_schema.py
```

Protected-surface validation:

```powershell
@'
src/mythic_edge_parser/app/evidence_ledger.py
tests/test_evidence_ledger.py
docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md
docs/implementation_handoffs/player_log_evidence_ledger_tier4_deck_state_boundary_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
```

Documentation-only validation for this Codex B pass:

```powershell
git diff --check
@'
docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
```

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md`
  exists.
- The contract keeps broad `deck_state` deferred.
- The contract explicitly chooses Tier 4 family notes/tests over a new
  boundary-only ledger entry for issue #161.
- The contract defines what submitted-deck evidence, runtime deck artifacts,
  collection matching, card catalog lookup, local decklists, and GRP candidate
  reports can and cannot prove.
- The contract preserves parser truth ownership and downstream boundaries.
- The contract defines confidence, finality, degradation, protected surfaces,
  validation, and acceptance criteria for Codex C.
- No behavior, schema, runtime, workbook, webhook, Apps Script, production,
  analytics, AI, secrets, raw logs, generated data, or local artifact changes
  are made in the contract writer pass.

## Unknowns And Open Questions

- Future Tier 5 needs to decide how card identity provenance distinguishes
  `grpId`, `instance_id`, `overlayGrpId`, `objectSourceGrpId`, local catalog
  display names, and unresolved candidates.
- Future work needs to decide whether exact sideboard deltas can ever be
  mapped from observed submitted-deck evidence without over-claiming hidden
  information.
- Future work may need a separate schema amendment for non-truth boundary
  entries if the ledger wants first-class boundary metadata that is not a
  parser-managed output field.
- Runtime active deck profiles currently mix source-derived lists with
  collection/catalog enrichment and generated timestamps. This contract treats
  them as derived local surfaces, not stable evidence records.
- Collection/deck matching quality depends on local data freshness. This
  contract does not define freshness validation.

## Suspected Implementation Gaps

- Tier 4 family notes currently say broader deck-state provenance remains
  deferred, but they may not explicitly name the issue #161 boundary across
  runtime active deck state, collection matching, card catalog, local decklists,
  and GRP candidate reports.
- Existing tests assert no `tier4.deck_state.*` entry exists, but they may not
  yet assert that deck names, deck IDs, card names, collection ownership,
  sideboard deltas, archetypes, advice, and AI truth remain unseeded deck-state
  boundaries.
- Existing tests may not explicitly state that runtime active deck snapshots
  are latest-observed derived operational state, not durable source truth.

## Codex C Handoff

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #161, Tier 4 broad deck-state provenance boundary under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/161
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/159
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/160
- Previous merge commit: 06b3268258b4c35ec447362a6e9db5f089996836
- Base branch: codex/parser-reliability-intelligence
- Contract: docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md
- Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier4_deck_state_boundary_comparison.md

Goal:
Compare the current evidence-ledger implementation and focused tests against the Tier 4 broad deck-state boundary contract. Implement only the smallest coherent metadata/test changes needed to make the boundary durable.

Do:
- Verify the branch is codex/parser-reliability-intelligence and inspect git status.
- Read AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, docs/agent_threads/implementation.md, and the contract.
- Keep broad deck_state deferred in Tier 3.
- Do not add a tier4.deck_state.* entry or a new deck_state seed field.
- Preserve Tier 4 seed fields exactly: sideboarding_entered, submit_deck_seen, submitted_deck_cards.
- Add or refine Tier 4 family notes in src/mythic_edge_parser/app/evidence_ledger.py only if needed to document the issue #161 boundary.
- Add focused tests in tests/test_evidence_ledger.py proving submitted-deck, runtime deck, collection matching, card catalog, decklist, and GRP candidate surfaces remain bounded and non-authoritative for broad deck-state truth.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_tier4_deck_state_boundary_comparison.md with comparison, files changed, validation, protected-surface status, remaining risks, and next recommended role.

Do not:
- Do not change parser behavior, client-action parsing behavior, parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status files, failed posts, workbook exports, diagnostics behavior, replay behavior, drift detector behavior, GRP candidate scoring behavior, card catalog sync behavior, decklist parsing behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, secrets, environment variables, raw logs, generated data, or local runtime artifacts.
- Do not infer hidden cards, complete decklists, sideboard deltas, deck names, deck IDs, collection ownership, card-name truth, archetypes, matchup plans, gameplay advice, player mistake labels, or model-provider truth.
- Do not commit raw private Player.log excerpts, raw payload values, submitted deck card IDs, local active deck artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, or generated data.
- Do not target main directly.
- Do not close issue #11.
- Do not stage or commit unless explicitly asked.

Validation:
- py -m pytest -q tests\test_evidence_ledger.py
- py -m ruff check src tests tools
- git diff --check
- Path-scoped protected-surface check for the contract, evidence_ledger.py, tests/test_evidence_ledger.py, and the implementation handoff.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/161"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/159"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/160"
  previous_merge_commit: "06b3268258b4c35ec447362a6e9db5f089996836"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier4_deck_state_boundary_comparison.md"
  verdict: "tier4_deck_state_boundary_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface check for docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md"
  stop_conditions:
    - "Do not close issue #11."
    - "Do not target main directly."
    - "Do not change parser behavior, client-action parsing behavior, parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status files, failed posts, workbook exports, diagnostics behavior, replay behavior, drift detector behavior, GRP candidate scoring behavior, card catalog sync behavior, decklist parsing behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, secrets, environment variables, raw logs, generated data, or local runtime artifacts."
    - "Do not add tier4.deck_state.* entries, deck_state seed fields, sideboard deltas, hidden-card inference, complete decklists, deck names, deck IDs, collection ownership truth, card-name truth, archetype classification, matchup plans, gameplay advice, player mistake labels, or model-provider truth."
    - "Do not commit raw private Player.log excerpts, raw payload values, submitted deck card IDs, local active deck artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, or generated data."
```
