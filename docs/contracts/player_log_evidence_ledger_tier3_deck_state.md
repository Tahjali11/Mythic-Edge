# Player.log Evidence Ledger Tier 3 Deck-State Boundary Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/169
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/167
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/168
- previous_merge_commit: 015f4db64a55f55a8418731e03352f0072e12c14
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier3-deck-state
- target_artifact: docs/contracts/player_log_evidence_ledger_tier3_deck_state.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier3_deck_state_comparison.md
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
- docs/contracts/player_log_evidence_ledger_tier3_game_results.md
- docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md
- docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md
- docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md
- docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md
- docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md

## Purpose

Issue #169 defines the narrow Tier 3 game-level `deck_state` provenance
boundary in the Player.log evidence ledger.

The decision for this issue is:

`deck_state` must remain deferred. Codex C must not seed Tier 3
`game1_deck_state`, `game2_deck_state`, `game3_deck_state`, a generic
`deck_state` field, or any `tier3.deck_state.*` ledger entry in issue #169.

Reason:

- Current parser models do not expose a parser-owned `GameSummary.deck_state`
  or per-game deck-state fact.
- Current Tier 4 work already maps narrower evidence surfaces:
  `sideboarding_entered`, `submit_deck_seen`, and `submitted_deck_cards`.
- Those Tier 4 fields are evidence surfaces, not broad game-level deck-state
  truth.
- Runtime active-deck artifacts, deck profiles, collection matches, decklists,
  card catalog resolution, and GRP candidate reports are local operational,
  enrichment, reference, or review surfaces.
- Current evidence-ledger entries validate as `parser_managed_truth is True`;
  a boundary-only `deck_state` entry would make the ledger appear to own a fact
  it is deliberately refusing to claim.

Plain English: Mythic Edge can say "we observed deck-related evidence near this
match or game." It cannot yet safely say "this is the final deck state for Game
2." The ledger must preserve that distinction before Match Journal, analytics,
overlays, Google Sheets, sideboard-delta work, archetype workflows, or AI
consumers build on the data.

This contract documents provenance metadata only. It must not change parser
behavior, parser state final reconciliation, parser event classes, workbook
schema, webhook payload shape, Apps Script behavior, output transport, runtime
artifact behavior, Match Journal behavior, overlay behavior, SQLite behavior,
Google Sheets sync behavior, analytics truth, AI truth, or model-provider
behavior.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, validators, vocabulary constants, privacy posture, and
allowed `value_source`, `confidence`, `finality`, invariant, drift, and
privacy labels.

`docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md` remains
authoritative for `game1_pre_postboard`, `game2_pre_postboard`, and
`game3_pre_postboard`. Pre/postboard labels are game-slot labels only. They
are not sideboarding proof and not deck-state truth.

`docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
remains authoritative for `sideboarding_entered` and `submit_deck_seen`.
Those fields prove parser-observed signals only. They do not prove deck
contents, deck changes, sideboard deltas, deck identity, or per-game active
deck state.

`docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
remains authoritative for `submitted_deck_cards`. That field proves observed
normalized submitted mainboard and sideboard `grpId` list content from a
submit-deck response. It does not prove final per-game deck state, deck name,
deck ID, decklist identity, sideboard deltas, card names, collection
ownership, archetypes, matchup plans, gameplay advice, or AI truth.

`docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md`
remains authoritative for the Tier 4 broad deck-state boundary. Issue #169
refines the same boundary from the Tier 3 game-level perspective. It must not
weaken #161 by smuggling broad deck-state truth into Tier 3.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #169 provenance should be
recorded through this contract, implementation handoff, family notes, and
focused tests rather than by changing the top-level ledger object shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- `src/mythic_edge_parser/app/models.py` owns current `GameSummary` and
  `MatchSummary` parser-owned game and match facts.
- `src/mythic_edge_parser/app/state.py` owns current parser state updates,
  match/game context, sideboarding and submit-deck signal booleans, and final
  reconciliation behavior.
- `src/mythic_edge_parser/parsers/client_actions.py` owns parsed submit-deck
  client-action evidence and normalized `deck_cards` / `sideboard_cards`.
- `src/mythic_edge_parser/app/diagnostics.py` may write local active
  submitted-deck artifacts from normalized submit-deck payloads.
- `src/mythic_edge_parser/app/runtime_surfaces.py` may expose latest
  active-deck state, active deck profiles, collection matches, missing-card
  summaries, and match-history deck snippets as local runtime surfaces.
- `src/mythic_edge_parser/app/decklists.py`, card catalog helpers, and
  `src/mythic_edge_parser/app/grp_id_candidates.py` provide local reference,
  enrichment, and review context.
- `src/mythic_edge_parser/app/sheet_exports.py` may serialize runtime deck
  snapshots for export, but exported runtime rows are not parser-owned
  per-game deck-state facts.
- `src/mythic_edge_parser/app/evidence_ledger.py` owns provenance metadata,
  confidence, finality, degradation behavior, drift flags, invariants, and
  boundary notes.
- Workbook formulas, dashboards, webhook transport, Apps Script, Match Journal,
  overlays, SQLite, Google Sheets sync, analytics, archetype classification,
  OpenAI/model-provider output, and AI output are downstream consumers only.

The evidence ledger describes support and uncertainty. It must not become a
second parser, a deck classifier, a sideboard-delta engine, a collection oracle,
a decklist identity resolver, a gameplay advisor, or an AI truth layer.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier3_deck_state.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier3_deck_state_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier3_deck_state.md

Referenced but not silently owned:

- docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md
- docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md
- docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md
- docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/parsers/client_actions.py
- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/decklists.py
- src/mythic_edge_parser/app/grp_id_candidates.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/app/sheet_exports.py
- tests/test_diagnostics.py
- tests/test_runtime_surfaces.py
- tests/test_grp_id_candidates.py
- tests/test_sheet_exports.py

## Public Interface

This contract covers evidence-ledger metadata for an intentionally deferred
field. It does not create a new runtime API, parser event, model property,
workbook column, webhook field, status field, or exported row field.

Current public ledger surfaces to preserve:

| Surface | Required issue #169 behavior |
| --- | --- |
| Tier 3 `game_level_facts.future_fields` | Must continue to contain exactly `deck_state` unless a future contract maps or removes it. |
| Tier 3 `game_level_facts.seed_fields` | Must not include `deck_state`, `game1_deck_state`, `game2_deck_state`, or `game3_deck_state`. |
| Ledger entry IDs | Must not include any `tier3.deck_state.*` entry in issue #169. |
| Tier 4 `sideboarding_and_deck_state.seed_fields` | Must remain exactly `sideboarding_entered`, `submit_deck_seen`, and `submitted_deck_cards`. |
| Tier 4 `sideboarding_and_deck_state.future_fields` | Must remain empty. |
| Tier 4 deck-state boundary | Must remain in notes/tests, not fake parser truth entries. |

Forbidden seed fields and entry families in issue #169:

- `deck_state`
- `game1_deck_state`
- `game2_deck_state`
- `game3_deck_state`
- `active_deck_state`
- `submitted_deck_by_game`
- `deck_identity`
- `deck_name`
- `deck_id`
- `decklist_identity`
- `sideboard_delta`
- `card_name`
- `collection_ownership`
- `archetype`
- `matchup_plan`
- `gameplay_advice`
- `player_mistake_label`
- any `tier3.deck_state.*`
- any `tier4.deck_state.*`

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` at
`015f4db64a55f55a8418731e03352f0072e12c14`:

- Issue #167 / PR #168 is deployed on `codex/parser-reliability-intelligence`.
- Tracker #11 remains open.
- Tier 3 `game_level_facts` is `seeded_sample`.
- Tier 3 seed fields currently cover game number, per-game winners, per-game
  results, starting player, play/draw, mulligans, opening hand,
  mulliganed-away cards, turn count, timing, duration, and pre/postboard.
- Tier 3 `future_fields` is exactly `["deck_state"]`.
- Tier 4 `sideboarding_and_deck_state` is `seeded_sample`.
- Tier 4 seed fields are exactly:
  - `sideboarding_entered`
  - `submit_deck_seen`
  - `submitted_deck_cards`
- Tier 4 `future_fields` is empty.
- `tests/test_evidence_ledger.py` asserts that broad deck state remains
  deferred and no `tier4.deck_state.*` entry exists.
- `tests/test_evidence_ledger.py` already includes broad Tier 4 boundary
  fragments covering runtime active submitted-deck artifacts, runtime active
  deck state, active deck profiles, collection/deck matching, card catalog
  lookup, local decklists, GRP candidate reports, review/degraded provenance,
  deck names, deck IDs, sideboard deltas, card names, collection ownership,
  model-provider output, and AI.
- `validate_ledger_entry(...)` requires `parser_managed_truth is True`.
- `GameSummary` has no `deck_state` field.
- `MatchSummary` has no per-game deck-state field.
- `MatchSummary` currently stores `sideboarding_entered` and
  `submit_deck_seen` booleans only.
- `client_actions.try_parse(...)` normalizes submit-deck responses to
  `deck_cards`, `sideboard_cards`, request context fields, and raw payload
  preservation.
- `diagnostics.record_submitted_deck(...)` can write a local
  `manasight_active_submitted_deck` artifact when normalized submitted lists
  are non-empty.
- `runtime_surfaces.py` normalizes `_ACTIVE_DECK_STATE`, caches match deck
  context, builds active deck profiles, matches active deck state to local
  collection deck payloads, and writes local runtime surfaces.
- `runtime_surfaces._deck_snapshot_brief(...)` can include deck signature,
  submitted timestamp, counts, matched deck name, deck ID, format, and match
  mode in match-history context.
- `sheet_exports.py` can export deck snapshot rows from runtime deck profile
  payloads.
- `grp_id_candidates.py` can load active submitted-deck artifacts or scan saved
  match logs to build review-oriented submitted-deck snapshots and candidate
  reports.

Observed risks:

- A latest runtime active-deck state can look like final game-level deck truth
  even when it is only latest-observed local operational state.
- A submit-deck payload can look game-scoped when it is event-scoped and may
  not prove final deck state for every game slot.
- A submitted-deck signature can look like deck identity when it is only a
  deterministic hash of normalized submitted lists.
- A matched collection deck can look like a Player.log fact when it is local
  enrichment.
- Pre/postboard can look like sideboarding or deck-state truth when it is only
  a game-slot label.
- A final absence of submit-deck evidence can look like proof of no deck change
  even when log truncation, summarization, rotation, malformed payloads, or
  unrouted entries may have hidden evidence.

## Scope Decision

Codex C should implement issue #169 as a metadata/test boundary hardening
slice.

Required implementation shape:

- Keep Tier 3 `game_level_facts.future_fields` as `["deck_state"]`.
- Keep Tier 3 `game_level_facts.seed_fields` unchanged.
- Do not add any `tier3.deck_state.*` entry.
- Keep Tier 4 `sideboarding_and_deck_state.seed_fields` exactly as
  `["sideboarding_entered", "submit_deck_seen", "submitted_deck_cards"]`.
- Keep Tier 4 `sideboarding_and_deck_state.future_fields` empty.
- Preserve all prior Tier 1, Tier 2, Tier 3, Tier 4, and Tier 5 seed fields
  and entries.
- Add or refine Tier 3 family notes in
  `src/mythic_edge_parser/app/evidence_ledger.py` only if needed to document
  the issue #169 game-level deck-state boundary.
- Add focused tests in `tests/test_evidence_ledger.py` proving the Tier 3
  `deck_state` deferral and the Tier 4 evidence-surface boundary are both
  durable.

Do not implement:

- parser behavior changes
- `GameSummary.deck_state`
- per-game deck-state storage
- submitted-deck-by-game logic
- runtime field-evidence attachment
- schema changes for non-truth boundary entries
- runtime deck-state artifact changes
- diagnostics report changes
- replay report changes
- workbook, webhook, Apps Script, Match Journal, overlay, SQLite, or Google
  Sheets sync changes
- analytics, archetype, advice, AI, or model-provider behavior

## Required Guarantees

### Game-Level Deck State Remains Deferred

`deck_state` remains a future Tier 3 field because current code does not expose
a parser-owned per-game deck-state fact.

No issue #169 implementation may claim:

- complete active decklist truth
- exact active deck identity
- exact submitted deck by game
- exact sideboard cards brought in or out
- hidden cards
- deck name or deck ID truth
- decklist identity
- collection ownership truth
- card-name truth
- archetype classification
- matchup plan
- sideboard-plan quality
- gameplay advice
- player mistake labels
- model-provider or AI truth

### Tier 4 Evidence Surfaces Stay Narrow

The prior Tier 4 fields keep their established meanings:

| Field | Meaning | Not allowed to prove |
| --- | --- | --- |
| `sideboarding_entered` | Parser observed a sideboarding-entry signal for the current match. | Changed cards, sideboard deltas, deck identity, sideboard quality, archetype, advice. |
| `submit_deck_seen` | Parser observed a submit-deck signal for the current match. | Submitted card content, complete deck state, deck name, decklist identity, sideboard deltas. |
| `submitted_deck_cards` | Parser observed non-empty normalized submitted mainboard/sideboard `grpId` list content from a submit-deck response. | Broad deck state, per-game deck state, card-name truth, deck identity, collection ownership, exact sideboard deltas, archetype, advice. |

### Boundary Notes Are Metadata, Not Truth Entries

If Codex C strengthens notes, the notes must describe what cannot be proven.
They must not create a new field that looks like parser truth.

Allowed invariant names for tests or notes:

- `tier3_deck_state_remains_deferred`
- `tier3_deck_state_no_game_slot_seed_fields`
- `tier3_deck_state_no_tier3_deck_state_entries`
- `tier3_deck_state_not_supported_by_pre_postboard_labels`
- `tier3_deck_state_not_supported_by_tier4_signal_booleans`
- `tier3_deck_state_not_supported_by_submitted_deck_cards_alone`
- `tier3_deck_state_runtime_surfaces_are_latest_observed_or_enrichment_only`
- `tier3_deck_state_downstream_consumers_do_not_own_truth`
- `tier3_deck_state_requires_schema_contract_for_boundary_only_entries`

These names may appear in tests or notes. They must not become new ledger
entries in issue #169.

## Evidence Boundary Matrix

| Evidence surface | Can prove | Cannot prove | Source label |
| --- | --- | --- | --- |
| `GameSummary.game_number` / fixed game slots | Game slot context for existing Tier 3 fields. | Deck state, sideboarding, submitted card content, deck identity. | `observed` or `derived` depending on upstream game-number evidence |
| `Pre / Postboard` | Game 1 versus game 2/3 label from game slot. | Sideboarding happened, submitted deck changed, active deck state. | `derived` |
| `sideboarding_entered` | Parser saw sideboarding-entry signal. | Changed cards, deck state, sideboard delta, advice. | `observed` signal boolean |
| `submit_deck_seen` | Parser saw submit-deck signal. | Submitted card content, deck state, deck identity. | `observed` signal boolean |
| `submitted_deck_cards` | Observed normalized submitted `grpId` lists when non-empty. | Final per-game deck state, deck identity, card names, collection ownership. | `observed` event-scoped evidence |
| Submit-deck request context / timestamp | Provenance context for event ordering and review. | Card content truth by itself, final deck state, per-game deck state. | `observed` context only |
| Submitted-deck counts/signature | Derived facets of normalized submitted lists. | Separate seed fields, deck identity, active deck truth. | `derived` |
| Active submitted-deck artifact | Local latest non-empty submitted-deck snapshot. | Source truth by itself, all-game final deck state, workbook truth. | `derived` fallback |
| Runtime `_ACTIVE_DECK_STATE` / match deck context | Latest-observed local operational cache. | Durable per-game final state, final reconciliation truth. | `derived` fallback |
| Active deck profile | Local profile from runtime deck state plus catalog/collection enrichment. | Parser-owned names, ownership, archetype, advice, deck identity truth. | enrichment/review only |
| Collection/deck matching | Best-effort local comparison against deck collection payloads. | Player.log fact, exact deck identity, collection ownership truth. | enrichment only |
| Card catalog lookup | Display/review resolution for IDs. | Observed card-name truth or hidden-card proof. | enrichment only |
| Local decklists | User/imported reference material. | Arena active deck truth or submitted deck truth. | reference only |
| GRP candidate report | Review support for card-ID/name reconciliation. | Authoritative card identity, deck state, decklist identity, gameplay truth. | review only |
| Deck snapshot export rows | Runtime profile export rows. | Parser-owned per-game deck-state facts. | downstream/export only |
| Match Journal, overlays, SQLite, Google Sheets, dashboards, analytics, AI | Downstream storage, display, analysis, or explanation. | Parser truth, final deck state, evidence ownership. | not source evidence |

## Value-Source, Confidence, Finality, And Degradation Rules

For issue #169, `deck_state` has no seeded value-source, confidence, or
finality entry because no parser-owned deck-state output is authorized.

If future work maps actual deck-state fields, it must distinguish:

- `observed`: direct parser-owned evidence for a field, not downstream
  enrichment.
- `derived`: deterministic parser/model derivation from parser-owned evidence.
- `inferred`: logic that is weaker than observed or derived and must be
  visibly labeled.
- `unknown`: absent, unavailable, unsupported, or not currently mapped.
- `conflict`: contradictory evidence or enrichment disagreement.
- `legacy_enriched`: old or local enrichment retained for compatibility, not
  parser truth.

Current required behavior:

- Missing submit-deck evidence leaves deck-state provenance deferred or
  unknown. It must not create a negative claim.
- Repeated submit-deck payloads remain event-scoped evidence. The latest value
  may be useful review context but not final per-game deck-state truth.
- Contradictory submitted lists, runtime artifacts, collection matches,
  decklists, catalog lookups, or GRP candidate reports require degraded or
  review-required provenance, not stronger truth.
- Runtime active deck state remains provisional latest-observed local state.
- Deck signatures remain derived facets, not deck identity.
- Matched deck names and deck IDs remain enrichment, not Player.log facts.
- Card names remain display/enrichment unless a separate card-identity
  contract owns the specific field.
- Source log truncation, summarization, rotation, malformed payloads, and
  unrouted entries must degrade confidence rather than allowing downstream
  consumers to fill gaps.

## Protected Surfaces

Do not change:

- parser behavior
- parser state final reconciliation
- parser event classes
- client-action parsing behavior
- submit-deck parsing behavior
- card-list normalization behavior
- runtime artifact write behavior
- runtime status file shape
- diagnostics behavior
- replay behavior
- feature-equity behavior
- drift detector behavior
- GRP candidate scoring behavior
- card catalog sync behavior
- decklist parsing behavior
- sheet schema
- sheet exports
- workbook schema
- webhook payload shape
- Apps Script behavior
- output transport
- ActionLogRow shape
- match identity
- game identity
- deduplication
- Match Journal behavior
- overlay behavior
- SQLite behavior
- Google Sheets sync behavior
- production behavior
- analytics truth
- AI truth
- OpenAI or model-provider behavior
- secrets, environment variables, API keys, tokens, credentials, or webhook
  URLs
- raw private Player.log excerpts
- generated card data
- local runtime artifacts
- runtime status files
- failed posts
- workbook exports

Do not infer hidden cards, complete decklists, classify archetypes, provide
gameplay advice, label player mistakes, or move analytics/AI truth into parser
truth.

## Side Effects

Allowed for Codex C:

- Update `src/mythic_edge_parser/app/evidence_ledger.py` family notes only if
  needed to make the Tier 3 deck-state deferral durable.
- Update `tests/test_evidence_ledger.py` focused metadata tests.
- Produce
  `docs/implementation_handoffs/player_log_evidence_ledger_tier3_deck_state_comparison.md`.

Forbidden for Codex C:

- Adding `GameSummary.deck_state` or `MatchSummary` deck-state fields.
- Adding `tier3.deck_state.*` or `tier4.deck_state.*` entries.
- Adding parser behavior.
- Adding runtime artifacts.
- Adding workbook, webhook, Apps Script, Match Journal, overlay, SQLite, or
  Google Sheets sync surfaces.
- Reading, copying, summarizing, or committing raw private logs.
- Adding card IDs, deck names, deck IDs, collection contents, local paths, or
  raw payload values to the ledger.

## Required Tests For Codex C

Focused tests in `tests/test_evidence_ledger.py` should prove:

- Tier 3 `future_fields` remains exactly `["deck_state"]`.
- Tier 3 `seed_fields` does not include `deck_state`, `game1_deck_state`,
  `game2_deck_state`, or `game3_deck_state`.
- No ledger entry starts with `tier3.deck_state.`.
- No ledger entry starts with `tier4.deck_state.`.
- Tier 4 `seed_fields` remains exactly `sideboarding_entered`,
  `submit_deck_seen`, and `submitted_deck_cards`.
- Tier 4 `future_fields` remains empty.
- Tier 3 family notes explicitly document the issue #169 game-level
  deck-state deferral.
- Tier 4 family notes continue to document the issue #161 boundary.
- No ledger output field named `active_deck_state`, `submitted_deck_by_game`,
  `deck_identity`, `deck_name`, `deck_id`, `decklist_identity`,
  `sideboard_delta`, `card_name`, `collection_ownership`, `archetype`,
  `matchup_plan`, `gameplay_advice`, `player_mistake_label`, `ai_truth`, or
  `model_provider_truth` exists.
- `submitted_deck_cards` remains observed submitted `grpId` list-content
  evidence, not broad deck-state truth.
- Runtime active deck state, active submitted-deck artifacts, active deck
  profiles, collection/deck matching, local decklists, card catalog lookup,
  sheet-export deck snapshot rows, and GRP candidate reports remain downstream,
  fallback, enrichment, reference, or review surfaces only.
- Built-in ledger and entries validate cleanly.
- Privacy validation remains path-only/no-values and rejects raw-log-like text,
  absolute local paths, secrets, webhook URLs, and token-shaped text.

Recommended focused validation for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m ruff check src tests tools
git diff --check
```

Optional adjacent validation if Codex C touches or suspects adjacent metadata:

```bash
python3 -m pytest -q tests/test_diagnostics.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_sheet_exports.py
```

Protected-surface validation when available:

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin <<'EOF'
src/mythic_edge_parser/app/evidence_ledger.py
tests/test_evidence_ledger.py
docs/contracts/player_log_evidence_ledger_tier3_deck_state.md
docs/implementation_handoffs/player_log_evidence_ledger_tier3_deck_state_comparison.md
EOF
```

Documentation-only validation for this Codex B pass:

```bash
git diff --check
python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin <<'EOF'
docs/contracts/player_log_evidence_ledger_tier3_deck_state.md
EOF
```

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_tier3_deck_state.md` exists.
- The contract explicitly decides that `deck_state` must remain deferred for
  issue #169.
- The contract explains why no Tier 3 deck-state seed entries are safe under
  the current parser-owned truth model.
- The contract preserves the prior Tier 4 boundary:
  `sideboarding_entered`, `submit_deck_seen`, and `submitted_deck_cards` are
  evidence surfaces, not broad deck-state truth.
- The contract names observed behavior, required guarantees, unknowns,
  suspected gaps, protected surfaces, validation expectations, and a Codex C
  handoff.
- No behavior, schema, runtime, workbook, webhook, Apps Script, production,
  analytics, AI, secrets, raw logs, generated data, or local artifact changes
  are made in the contract writer pass.

## Unknowns And Open Questions

- Future work may need a separate schema amendment for boundary-only ledger
  entries if the ledger wants first-class non-parser-truth boundary metadata.
- Future work must decide whether an actual parser-owned per-game deck-state
  model field is needed, and if so which parser evidence can support it.
- Future sideboard-delta feasibility remains unresolved. Submitted deck lists
  may support review context, but exact sideboard-in/out truth must not be
  inferred without a new scoped contract.
- Future Match Journal, overlay, SQLite, Google Sheets sync, and analytics
  consumers will need explicit contracts if they store deck-state-like review
  context.
- Runtime active deck profiles currently mix submitted lists, collection
  matching, catalog enrichment, generated timestamps, and local paths. They
  are not stable parser-owned evidence records.
- Collection/deck matching quality depends on local collection freshness and
  decklist alignment; this contract does not define freshness validation.

## Suspected Gaps

- Tier 3 family notes currently leave `deck_state` deferred but may not
  explicitly mention issue #169 or the game-level deck-state boundary.
- Existing tests are strong for the Tier 4 boundary, but they may not yet
  assert that no `tier3.deck_state.*` entries or per-game deck-state seed
  fields exist.
- Existing tests may not explicitly distinguish Tier 3 game-level deferral from
  Tier 4 submitted-deck card-content evidence.
- Existing tests may not explicitly protect against `submitted_deck_by_game`,
  `decklist_identity`, `ai_truth`, or `model_provider_truth` entering ledger
  output fields.
- The code has runtime deck snapshots and sheet export rows whose names can
  tempt downstream consumers to treat them as parser facts. The ledger needs
  durable notes/tests to keep them bounded.

## Codex C Handoff

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #169, Tier 3 game-level deck_state provenance boundary under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/169
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/167
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/168
- Previous merge commit: 015f4db64a55f55a8418731e03352f0072e12c14
- Base branch: codex/parser-reliability-intelligence
- Contract: docs/contracts/player_log_evidence_ledger_tier3_deck_state.md
- Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier3_deck_state_comparison.md

Goal:
Compare the current evidence-ledger implementation and focused tests against the Tier 3 game-level deck_state boundary contract. Implement only the smallest coherent metadata/test changes needed to make the deferral durable.

Decision to preserve:
- deck_state remains deferred in Tier 3 for issue #169.
- Do not add game1_deck_state, game2_deck_state, game3_deck_state, deck_state seed fields, tier3.deck_state.* entries, or tier4.deck_state.* entries.
- Preserve the prior Tier 4 boundary: sideboarding_entered, submit_deck_seen, and submitted_deck_cards are evidence surfaces, not broad deck-state truth.

Do:
- Verify the branch is based on codex/parser-reliability-intelligence and inspect git status.
- Read AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, docs/agent_threads/implementation.md, and the contract.
- Keep Tier 3 future_fields exactly ["deck_state"].
- Preserve existing Tier 1, Tier 2, Tier 3, Tier 4, and Tier 5 seed fields and entries.
- Add or refine Tier 3 family notes in src/mythic_edge_parser/app/evidence_ledger.py only if needed to document the issue #169 game-level deck-state deferral.
- Add focused tests in tests/test_evidence_ledger.py proving the Tier 3 deck_state deferral, absence of tier3.deck_state.* entries, absence of per-game deck-state seed fields, and continued Tier 4 evidence-surface boundary.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_tier3_deck_state_comparison.md with comparison, files changed, validation, protected-surface status, remaining risks, and next recommended role.

Do not:
- Do not change parser behavior, parser state final reconciliation, parser event classes, client-action parsing behavior, submit-deck parsing behavior, card-list normalization behavior, runtime artifact write behavior, runtime status file shape, diagnostics behavior, replay behavior, feature-equity behavior, drift detector behavior, GRP candidate scoring behavior, card catalog sync behavior, decklist parsing behavior, sheet schema, sheet exports, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts.
- Do not infer hidden cards, complete decklists, sideboard deltas, deck names, deck IDs, collection ownership, card-name truth, archetypes, matchup plans, gameplay advice, player mistake labels, or model-provider truth.
- Do not commit raw private Player.log excerpts, raw payload values, submitted deck card IDs, local active deck artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, generated data, or local paths.
- Do not target main directly.
- Do not close issue #11.
- Do not stage or commit unless explicitly asked.

Validation:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m ruff check src tests tools
- git diff --check
- Path-scoped protected-surface check for the contract, evidence_ledger.py, tests/test_evidence_ledger.py, and the implementation handoff if the tool is available.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/169"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/167"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/168"
  previous_merge_commit: "015f4db64a55f55a8418731e03352f0072e12c14"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_deck_state.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_deck_state_comparison.md"
  verdict: "tier3_deck_state_deferred_boundary_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-deck-state"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface check for docs/contracts/player_log_evidence_ledger_tier3_deck_state.md"
  stop_conditions:
    - "Do not close issue #11."
    - "Do not target main directly."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, client-action parsing behavior, submit-deck parsing behavior, card-list normalization behavior, runtime artifact write behavior, runtime status file shape, diagnostics behavior, replay behavior, feature-equity behavior, drift detector behavior, GRP candidate scoring behavior, card catalog sync behavior, decklist parsing behavior, sheet schema, sheet exports, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts."
    - "Do not add deck_state seed fields, game1_deck_state, game2_deck_state, game3_deck_state, tier3.deck_state.* entries, tier4.deck_state.* entries, sideboard deltas, hidden-card inference, complete decklists, deck names, deck IDs, collection ownership truth, card-name truth, archetype classification, matchup plans, gameplay advice, player mistake labels, AI truth, or model-provider truth."
    - "Do not commit raw private Player.log excerpts, raw payload values, submitted deck card IDs, local active deck artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, generated data, or local paths."
```
