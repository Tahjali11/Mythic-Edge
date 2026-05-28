# Player.log Evidence Ledger Tier 5 Card Identity Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/163
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/161
- previous_integration_commit: 2a96d5701f6939fd7a78d71383c35d43095d69c0
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier5-card-identity
- target_artifact: docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier5_card_identity_comparison.md
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
- docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md
- docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md
- docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md
- docs/contracts/parser_opponent_card_observations.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md

## Purpose

Issue #163 maps the first Tier 5 card identity provenance boundary in the
Player.log evidence ledger.

The field in scope is:

- `grp_id`

This field means Mythic Edge can document provenance for observed or
parser-derived Arena `grpId` card identity values that appear in existing card
identity, gameplay action, submitted-deck, opening-hand, and opponent-card
observation surfaces.

This contract deliberately keeps the first Tier 5 seed narrow. It authorizes
one ledger seed field, `grp_id`, and allows that entry to describe tightly
related identity facets:

- direct `grpId` evidence
- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `parent_id`
- replacement-chain or prior-instance identity context
- `identity_hint_source`
- catalog resolution status as enrichment context
- card names, display labels, layouts, and card faces as enrichment context
  only

Those facets are not separate ledger output fields in issue #163. They must
remain inside the `grp_id` entry, family notes, or future issue scope until a
later contract explicitly maps them.

Plain English: Mythic Edge may say "this parser surface is using this `grpId`
and here is why." It must not say "this resolved name, deck match, catalog
candidate, collection match, display label, or model explanation is now direct
Player.log truth."

This contract documents provenance metadata only. It must not change parser
behavior, GameState parsing, gameplay-action classification, opponent-card
observation behavior, card catalog sync/refresh behavior, GRP candidate
scoring, runtime active deck artifact shape, parser state final
reconciliation, parser event classes, workbook schema, webhook payload shape,
Apps Script behavior, output transport, runtime artifact behavior, production
behavior, environment variable contracts, OpenAI/model-provider behavior, or
AI/analytics truth.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, validators, vocabulary constants, privacy posture, and the
allowed `value_source`, `confidence`, `finality`, invariant, drift, and privacy
vocabularies.

`docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
remains authoritative for submitted-deck card-list content. Issue #163 may
describe how submitted `grpId` list values participate in card identity
provenance, but it must not redefine `submitted_deck_cards`, submitted-deck
counts, submitted-deck signatures, broad deck state, deck identity, or
sideboard deltas.

`docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md`
remains authoritative for the broad deck-state boundary. Issue #163 must
preserve the decision that runtime active deck state, active deck profiles,
collection/deck matching, card catalog lookup, local decklists, and GRP
candidate reports are derived, enrichment, reference, or review surfaces rather
than parser truth for broad deck state.

`docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md` remains
authoritative for opening-hand provenance. Issue #163 may document shared
card-identity semantics for `grpId` values and card-name resolution context,
but it must not change private-hand extraction, opening-hand selection,
mulliganed-away capture, or card-list serialization behavior.

`docs/contracts/parser_opponent_card_observations.md` remains authoritative for
opponent-visible observation payloads. Issue #163 prepares the shared card
identity boundary for those payloads, but it must not change observation
filtering, visibility rules, or opponent-card observation payload behavior.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #163 provenance should be
recorded through this contract, implementation handoff, family notes, entry
notes, and focused tests rather than by changing the top-level ledger object
shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- GRE GameState parser and extractor surfaces own observed object identity
  inputs from `Player.log` payloads.
- `src/mythic_edge_parser/app/gameplay_actions.py` owns local normalized
  gameplay action entries and canonical `grp_id` selection from GameState
  object identity hints.
- `src/mythic_edge_parser/app/opponent_card_observations.py` owns
  opponent-visible observation records derived from gameplay action entries.
- `src/mythic_edge_parser/app/grp_id_catalog.py` and
  `src/mythic_edge_parser/app/card_catalog.py` own local catalog enrichment,
  display labels, candidate rows, resolved names, layout metadata, card-face
  metadata, and contradiction markers.
- `src/mythic_edge_parser/app/evidence_ledger.py` owns provenance metadata,
  confidence, finality, degradation behavior, drift flags, invariants, and
  protected boundary notes.
- Workbook formulas, dashboards, webhook transport, Apps Script, analytics,
  card-performance interpretation, active deck profiles, local decklists,
  collection matching, archetype classification, matchup plans, gameplay
  advice, player-mistake labels, OpenAI/model-provider output, and AI output
  are downstream or enrichment surfaces only.

The evidence ledger describes support and uncertainty for card identity fields.
It must not become a second parser, a card catalog oracle, a deck classifier, a
collection ownership source, a hidden-card inference layer, or an AI truth
layer.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier5_card_identity.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier5_card_identity_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier5_card_identity.md

Referenced but not silently owned:

- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- src/mythic_edge_parser/app/grp_id_catalog.py
- src/mythic_edge_parser/app/card_catalog.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/grp_id_candidates.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/models.py
- tests/test_gameplay_actions.py
- tests/test_opponent_card_observations.py
- tests/test_grp_id_catalog.py
- tests/test_card_catalog.py

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` at
`2a96d5701f6939fd7a78d71383c35d43095d69c0`:

- Issue #161 is deployed.
- Tracker #11 remains open.
- Tier 4 `sideboarding_and_deck_state` is a `seeded_sample` with seed fields:
  - `sideboarding_entered`
  - `submit_deck_seen`
  - `submitted_deck_cards`
- Tier 4 `future_fields` is empty.
- The Tier 4 deck-state boundary states that broader `deck_state`, deck names,
  deck IDs, sideboard deltas, card names, collection ownership, archetypes,
  matchup plans, gameplay advice, player-mistake labels, model-provider
  output, and AI remain outside parser truth.
- Tier 5 `card_identity_and_gameplay_actions` is currently
  `registered_future` with future fields:
  - `grp_id`
  - `gameplay_action`
  - `opponent_card_observation`
- `gameplay_actions.py` normalizes GameState object identity into fields such
  as `grp_id`, `observed_grp_id`, `overlay_grp_id`, `object_source_grp_id`,
  `parent_id`, and `identity_hint_source`.
- `gameplay_actions.py` prefers `object_source_grp_id`, then parent-chain
  candidates, prior-instance canonical identity, replacement-chain canonical
  identity, and finally direct object candidates when resolving canonical
  `grp_id`.
- Direct object candidates include raw `grpId`, `overlayGrpId`, and
  `objectSourceGrpId` after integer normalization.
- Gameplay action rendering can enrich entries with `card_name`,
  `display_name`, `resolution_status`, `layout`, and `card_faces` from the GRP
  catalog.
- Local active deck profile matching can supply display names for local actor
  entries when exact active-deck arena IDs are available.
- `grp_id_catalog.py` stores resolved names, display names, candidate names,
  primary sources, layout and card-face metadata, observation counts, observed
  type/action hints, contradiction flags, and demoted names.
- `grp_id_catalog.py` can return exact numeric Arena lookup matches,
  confirmed overrides, inferred-confirmed overrides, legacy auto-promoted
  candidates, candidate names, unresolved placeholders, and contradicted
  entries.
- `opponent_card_observations.py` preserves `grp_id`, observed/fallback ID
  fields, identity hint source, name-resolution status, source evidence,
  value source, confidence, visibility, degradation flags, and review-required
  status for opponent-visible observations.
- Current tests already cover many card identity behaviors in gameplay actions,
  opponent-card observations, and GRP catalog code, but the evidence ledger has
  no Tier 5 seeded entry yet.

Observed risks, not fixed by this issue:

- Resolved `card_name` or `display_name` values can look like observed
  Player.log truth even when they came from catalog, active deck, local
  decklist, override, candidate, or display fallback enrichment.
- `instance_id` can look durable even though it is game-local object identity.
- `overlay_grp_id`, `object_source_grp_id`, parent-chain identity,
  prior-instance identity, and replacement-chain identity can look equally
  strong as direct `grpId` evidence without explicit confidence rules.
- GRP candidate reports can look like confirmed identity even though they are
  review support.
- Active deck profiles or local decklist matches can look like card identity
  truth even though they are local enrichment.
- Opponent-card observations can look like hidden-card inference or complete
  decklist evidence if downstream consumers ignore visibility, degradation,
  and confidence fields.

## Scope Decision

Codex C should implement issue #163 as a Tier 5
`card_identity_and_gameplay_actions` metadata slice in the existing evidence
ledger.

Required family metadata:

- Change Tier 5 `card_identity_and_gameplay_actions.status` from
  `registered_future` to `seeded_sample`.
- Add exactly one Tier 5 seed field:
  - `grp_id`
- Remove `grp_id` from Tier 5 `future_fields`.
- Preserve Tier 5 `future_fields` for later work:
  - `gameplay_action`
  - `opponent_card_observation`
- Add family notes stating that issue #163 maps card identity `grp_id`
  provenance only.
- Add family notes stating that gameplay-action provenance and
  opponent-card-observation provenance remain future work.
- Preserve all prior Tier 1, Tier 3, and Tier 4 seed fields and entries.

Required Tier 5 entry:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier5.card_identity.grp_id` | `grp_id` | `Card GRP ID` | `observed` or `derived` |

Fields not authorized as separate seed fields in issue #163:

- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `parent_id`
- `instance_id`
- `identity_hint_source`
- `card_name`
- `display_name`
- `resolution_status`
- `layout`
- `card_faces`
- `name_resolution_source`
- `candidate_names`
- `deck_name`
- `deck_id`
- `decklist_identity`
- `collection_ownership`
- `gameplay_action`
- `opponent_card_observation`

Those fields may appear in the `grp_id` entry only as source evidence,
fallback evidence, confidence context, degradation context, notes, or future
field references.

## Public Interface

This contract covers evidence-ledger metadata for existing parser and
parser-adjacent surfaces. It does not create a new runtime API.

Authorized ledger field:

| Ledger field | Entry ID | Meaning |
| --- | --- | --- |
| `grp_id` | `tier5.card_identity.grp_id` | Card identity value expressed as a normalized Arena `grpId` integer when supported by Player.log object or parser-derived identity evidence. |

Authorized evidence facets inside the single entry:

| Facet | Existing surface | Contract status |
| --- | --- | --- |
| Direct `grpId` | GameState object `grpId` / gameplay action `observed_grp_id` | Direct observed ID evidence when present and normalized. |
| `object_source_grp_id` | GameState object `objectSourceGrpId` / gameplay action field | Derived fallback ID evidence; stronger than display/name enrichment but not the same as direct `grpId`. |
| `overlay_grp_id` | GameState object `overlayGrpId` / gameplay action field | Derived fallback ID evidence; review required when conflicting with direct/source IDs. |
| `parent_id` and parent chain | GameState object `parentId` plus related object identity | Derived fallback context; not durable card identity by itself. |
| replacement or prior-instance chain | Normalized annotation/replacement/prior object state | Derived fallback context; not direct observed card identity. |
| `identity_hint_source` | Gameplay action and opponent observation entries | Provenance label for why canonical `grp_id` was selected. |
| `card_name` / `display_name` | GRP catalog, active deck index, placeholders | Enrichment/display context only; not separate parser truth in #163. |
| `resolution_status` | GRP catalog or opponent observation normalization | Confidence/degradation context only; not separate parser truth in #163. |
| `layout` / `card_faces` | Card/GRP catalog metadata | Enrichment/display context only; not separate parser truth in #163. |
| submitted `grpId` lists | Tier 4 `submitted_deck_cards` | Adjacent observed card-list evidence, not broad deck-state or card-name truth. |
| opening-hand card names | Tier 3 opening-hand entries | Existing path-only provenance dependency, not a Tier 5 card-name seed. |

Required compatibility:

- Do not rename `grp_id`, `observed_grp_id`, `overlay_grp_id`,
  `object_source_grp_id`, `parent_id`, or `identity_hint_source`.
- Do not rename `card_name`, `display_name`, `resolution_status`, `layout`, or
  `card_faces`.
- Do not change canonical `grp_id` selection in `gameplay_actions.py`.
- Do not change `opponent_card_observations.py` payload behavior.
- Do not change GRP catalog resolution, candidate, contradiction, or display
  behavior.
- Do not add workbook columns, webhook fields, Apps Script fields, parser
  events, runtime status fields, generated card data, or runtime artifacts.

## Evidence Boundary Matrix

| Evidence surface | Can prove | Cannot prove | Source label |
| --- | --- | --- | --- |
| GameState object `grpId` | Observed object-level card ID candidate. | Card name, deck identity, hidden-card proof, final global card identity across all objects. | `observed` |
| GameState object `objectSourceGrpId` | Source object card ID fallback for linked/support objects. | Direct printed object identity in all cases, card name, deck identity. | `derived` fallback |
| GameState object `overlayGrpId` | Overlay card ID fallback when direct/source ID is absent. | Stronger truth than direct/source ID, card name, deck identity. | `derived` fallback |
| GameState object `parentId` | Parent-chain context for resolving child/support objects. | Card ID by itself, durable identity outside the current game object graph. | `derived` fallback context |
| Prior-instance / replacement-chain context | Continuity context for object identity across diffs and replacements. | New observed card identity by itself, hidden-card proof. | `derived` fallback context |
| Gameplay action `grp_id` | Canonical action-level ID chosen by parser logic from known identity hints. | Card name truth, action correctness beyond existing action classifier, opponent deck contents. | `observed` when direct, otherwise `derived` |
| Opponent-card observation `grp_id` | Opponent-visible observation ID when visibility and action evidence support it. | Hidden cards, complete opponent decklist, archetype, game advice. | `observed` or `derived` based on source |
| GRP catalog exact numeric lookup | Name/display enrichment for a known ID. | Source Player.log observation, collection ownership, deck identity. | `legacy_enriched` |
| GRP override confirmed or inferred-confirmed name | Local/manual or inferred name enrichment. | Observed Player.log name truth. | `legacy_enriched`; review when inferred |
| Candidate report name | Review-oriented candidate label. | Confirmed card identity, parser truth, deck identity. | `legacy_enriched`; low confidence |
| Contradicted catalog entry | Evidence that enrichment is unsafe. | Replacement fact by itself. | `conflict` / review |
| Active deck profile exact name | Local deck enrichment for local actor display. | Player.log card-name truth, collection ownership truth, deck identity. | enrichment only |
| Tier 4 `submitted_deck_cards` | Submitted `grpId` list content from submit-deck response. | Card names, broad deck state, sideboard deltas, deck identity. | `observed` for IDs only |
| Workbook, Apps Script, dashboard, analytics, AI | Display, transport, analysis, or explanation. | Parser truth, evidence ownership, card identity truth. | not source evidence |

## Required Entry Behavior

The `tier5.card_identity.grp_id` entry should use:

- `tier`: `5`
- `output_family`: `card_identity_and_gameplay_actions`
- `output_field`: `grp_id`
- `display_name`: `Card GRP ID`
- `parser_owner`: `src/mythic_edge_parser/app/gameplay_actions.py`
- `model_surface`: `gameplay_action_entry.grp_id / opponent_card_observation.grp_id`
- `downstream_surfaces`:
  - `gameplay_actions`
  - `opponent_card_observations`
  - `submitted_deck_cards`
  - `opening_hand`
  - `grp_id_catalog`
  - `future_card_performance`
  - `future_analytics_consumers`
- `parser_managed_truth`: `True`
- `coverage_status`: `seeded_sample`

Direct evidence should include at minimum:

- `game_state.game_object.grp_id`
  - parser event kind: `GameState`
  - raw event family: `greToClientEvent`
  - raw message type: `GREMessageType_GameStateMessage`
  - normalized path: `gameplay_action_entry.observed_grp_id`
  - raw path: `greToClientMessages[].gameStateMessage.gameObjects[].grpId`
  - allowed types: `int`, `str-int`
  - value source when used: `observed`
  - confidence when used: `high`
  - finality when used: `live`
  - missing behavior: use documented fallback identity hints or mark unknown

- `gameplay_action.canonical_grp_id_direct`
  - parser event kind: `GameState`
  - raw event family: `greToClientEvent`
  - raw message type: `GREMessageType_GameStateMessage`
  - normalized path:
    `gameplay_action_entry.grp_id + gameplay_action_entry.identity_hint_source`
  - raw path: `greToClientMessages[].gameStateMessage.gameObjects[]`
  - allowed types: `int`, `str-int`
  - value source when used: `observed` when `identity_hint_source` is
    `direct_grp_id`
  - confidence when used: `high`
  - finality when used: `provisional`

- `opponent_card_observation.grp_id`
  - parser event kind: `opponent_card_observation`
  - raw event family: `derived_from_gameplay_action`
  - raw message type: ``
  - normalized path:
    `opponent_card_observation.grp_id + opponent_card_observation.identity_hint_source`
  - raw path: ``
  - allowed types: `int`, `str-int`
  - value source when used: mirror source from gameplay action entry
  - confidence when used: mirror confidence from gameplay action entry and
    visibility evidence
  - finality when used: `provisional`

Fallback evidence should include at minimum:

- `game_state.game_object.object_source_grp_id`
- `game_state.game_object.overlay_grp_id`
- `game_state.game_object.parent_chain_grp_id`
- `game_state.game_object.prior_instance_grp_id`
- `game_state.game_object.replacement_chain_grp_id`
- `tier4.submitted_deck_cards.submitted_grp_ids`
- `tier3.opening_hand.grp_id_resolution_path`
- `grp_id_catalog.name_resolution_context`
- `active_deck_profile.display_name_context`
- `grp_id_candidate_report.review_context`

Fallback evidence from catalog, active deck, local decklists, collection
matches, generated card data, or candidate reports must use
`legacy_enriched`, `derived`, `unknown`, or review/degradation language as
appropriate. It must not be treated as direct observed Player.log card identity.

## Value Source Policy

Required policy labels:

- `observed`: direct GameState `grpId` evidence or direct submitted `grpId`
  list content.
- `derived`: canonical `grp_id` selected from object source, overlay, parent,
  replacement, prior-instance, or parser action-entry context.
- `legacy_enriched`: catalog, active deck, local decklist, collection, or
  candidate information used for names, display labels, layout, faces, or
  review context.
- `unknown`: no usable ID evidence after normalization.
- `conflict`: contradictory ID hints, contradicted catalog metadata, or
  disagreement that blocks stronger provenance.

Required mapping:

- Direct `grpId` path present and normalized -> `observed`.
- Canonical ID selected from `object_source_grp_id` -> `derived`.
- Canonical ID selected from `overlay_grp_id` -> `derived`, review required if
  direct/source ID conflicts.
- Canonical ID selected from parent chain -> `derived`.
- Canonical ID selected from prior instance -> `derived`.
- Canonical ID selected from replacement chain -> `derived`.
- Names, display labels, layouts, card faces, active deck matches, and
  candidate names -> `legacy_enriched` when mentioned at all.
- Missing, malformed, boolean, empty, or non-normalizable ID values ->
  `unknown`.
- Conflicting direct/source/overlay/catalog signals -> `conflict`.

## Confidence Policy

High confidence:

- Direct normalized `grpId` from GameState object evidence.
- Direct submitted `grpId` list values already covered by Tier 4
  `submitted_deck_cards`.
- Gameplay action `grp_id` where `identity_hint_source == "direct_grp_id"` and
  no conflict/degradation is present.

Medium confidence:

- Canonical `grp_id` derived from `object_source_grp_id`.
- Canonical `grp_id` derived from parent chain, replacement chain, or prior
  instance when related object context is available and non-conflicting.
- Opponent-card observation `grp_id` derived from visible action evidence with
  known seat mapping and no card identity conflict.

Low confidence / review required:

- Canonical `grp_id` derived from `overlay_grp_id` when direct/source evidence
  is absent.
- Candidate-only catalog labels.
- Inferred-confirmed or legacy auto-promoted catalog labels.
- Name-only observation labels.
- Contradicted catalog entries.
- Missing seat mapping for opponent observations.
- Ambiguous visibility for opponent observations.
- Data-loss or truncation evidence affecting the GameState/object context.
- Any disagreement between direct `grpId`, source ID, overlay ID, parent-chain
  ID, replacement-chain ID, active deck enrichment, catalog enrichment, or
  candidate reports.

Unknown confidence:

- No usable ID evidence.
- Malformed or non-normalizable ID values.
- Missing catalog when only name/display enrichment would be available.

## Finality Policy

- GameState object IDs are `live` while events are being processed.
- Gameplay action rows and opponent-card observation records are
  `provisional` during the live match because later GameState diffs,
  replacement chains, catalog updates, or contradiction flags can change
  display and review context.
- Saved action reports are event-scoped final artifacts for the observed run,
  but they are not global card-name or deck identity truth.
- Tier 4 submitted `grpId` list content remains final only under its own
  submitted-deck contract. It does not make names, deck identity, or sideboard
  deltas final.
- Catalog resolution is never stronger than enrichment finality in issue #163.
  A catalog update, override, contradiction, or candidate report can change
  name/display enrichment without changing the underlying `grp_id` evidence.
- Future field-evidence attachment may use `reconciled` only when a later
  contract defines exact reconciliation rules.

## Invariants

Codex C must preserve these invariants in metadata and tests:

- Tier 5 seeds exactly `grp_id` in issue #163.
- Tier 5 keeps `gameplay_action` and `opponent_card_observation` as future
  fields.
- No Tier 5 seed field is added for card names, display labels, catalog
  resolution, layout, card faces, deck names, deck IDs, collection ownership,
  decklist identity, sideboard deltas, card-performance analytics, gameplay
  advice, player mistake labels, model-provider output, or AI.
- `grp_id` may be observed or derived; the evidence entry must distinguish
  direct ID evidence from fallback ID evidence.
- `instance_id` is game-local object identity and must not be treated as
  durable card identity.
- `identity_hint_source` is provenance context, not a separate output truth
  field.
- `card_name`, `display_name`, `resolution_status`, `layout`, and
  `card_faces` are enrichment or degradation context in issue #163.
- Candidate names and active deck profile names are review/display context,
  not parser truth.
- Opponent-card observation IDs must not infer hidden cards, complete
  opponent decklists, archetypes, matchup plans, gameplay advice, or AI truth.
- Workbook formulas, dashboards, webhook transport, Apps Script, analytics,
  card-performance reports, and AI output must not populate `grp_id` truth.
- Ledger metadata must preserve `path_only_no_values` privacy posture and must
  not embed raw private `Player.log` excerpts, raw submitted-deck values, deck
  names, decklists, collection contents, generated card data, secrets, runtime
  status files, failed posts, or workbook exports.

## Degradation Behavior

The Tier 5 `grp_id` entry must document degradation for:

- missing direct `grpId`
- missing all fallback ID hints
- malformed, boolean, empty, or non-normalizable ID values
- conflicting direct/source/overlay/parent/replacement/prior-instance IDs
- canonical ID selected from fallback rather than direct evidence
- missing parent object for parent-chain identity
- missing replacement source for replacement-chain identity
- stale prior-instance context
- missing catalog data when display/name enrichment is requested
- unresolved catalog entry
- candidate-only catalog entry
- inferred-confirmed or legacy auto-promoted name
- contradicted catalog entry
- active deck profile or local decklist mismatch
- GRP candidate report disagreement
- opponent observation missing seat mapping
- opponent observation ambiguous visibility
- truncation or data-loss evidence affecting GameState context

Recommended drift flags:

- `missing_expected_payload_path`
- `fallback_used`
- `weak_fallback_used`
- `conflicting_evidence`
- `schema_snapshot_missing`
- `fixture_gap`
- `sensitive_evidence_redacted`

## Deferred Work

Defer all of the following:

- parser behavior changes
- GameState parser changes
- extractor changes
- gameplay-action classification changes
- opponent-card-observation behavior changes
- card catalog sync/refresh changes
- GRP candidate scoring or promotion changes
- generated card data changes
- runtime active deck artifact shape changes
- runtime status field changes
- runtime field-evidence attachment
- schema snapshots
- invariant execution
- diagnostics report changes
- replay report changes
- feature-equity report changes
- field-evidence attachment
- workbook schema changes
- webhook payload changes
- Apps Script behavior changes
- output transport changes
- parser state final reconciliation changes
- parser event class changes
- match/game identity or deduplication changes
- gameplay-action provenance field seeding
- opponent-card-observation provenance field seeding
- sideboard-delta feasibility or implementation
- deck names, deck IDs, decklist identity, collection ownership, card-name
  truth, archetype labels, matchup plans, gameplay advice, player-mistake
  labels, OpenAI/model-provider behavior, and AI truth

## Validation Obligations

Codex C must run at least:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m ruff check src tests tools
git diff --check
```

Codex C should run adjacent focused tests if implementation references or
updates any adjacent notes, constants, or entry paths:

```bash
python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_grp_id_catalog.py tests/test_card_catalog.py
```

Codex C should run a protected-surface check when available:

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence
```

Validation evidence must prove:

- the Tier 5 family status becomes `seeded_sample`;
- Tier 5 `seed_fields` is exactly `["grp_id"]`;
- Tier 5 `future_fields` keeps `gameplay_action` and
  `opponent_card_observation`;
- the `tier5.card_identity.grp_id` entry validates under the existing ledger
  schema;
- direct and fallback evidence paths are documented;
- card names, display labels, layouts, faces, candidates, deck names, deck
  IDs, collection ownership, decklist identity, sideboard deltas,
  card-performance analytics, gameplay advice, model-provider output, and AI
  are not promoted to seed fields or parser truth;
- Tier 4 deck-state boundary notes from #161 remain preserved;
- Tier 4 `submitted_deck_cards` remains unchanged as observed submitted
  `grpId` list content only;
- Tier 3 opening-hand card-name references remain path-only provenance and are
  not redefined by Tier 5.

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_tier5_card_identity.md` exists.
- `src/mythic_edge_parser/app/evidence_ledger.py` is updated only for Tier 5
  metadata, the new `grp_id` entry, and related notes if Codex C implements.
- `tests/test_evidence_ledger.py` has focused tests for the Tier 5 family,
  `grp_id` entry, evidence paths, policies, degradation language, and
  protected non-truth boundaries.
- No parser behavior, runtime artifact shape, workbook/webhook/App Script
  surface, output transport, generated card data, secrets, raw logs, runtime
  files, failed posts, workbook exports, production behavior, or
  AI/analytics truth changes are included.
- The implementation handoff explains any untouched adjacent behavior and any
  remaining risks for later gameplay-action or opponent-observation provenance
  issues.

## Open Questions And Contract Risks

- A later contract may decide to seed `gameplay_action` or
  `opponent_card_observation` as separate Tier 5 fields. This contract
  intentionally does not do that.
- A later contract may decide to map lower-confidence card-name or
  resolution-status provenance. That would require explicit wording that names
  are enrichment, not observed Player.log truth.
- Existing gameplay-action rendering uses active deck and catalog enrichment
  for display. This contract does not change that behavior; it only prevents
  the ledger from promoting those display values into parser truth.
- If future field-evidence attachment needs row-level `grp_id` evidence, it
  must define exact attachment shape and privacy rules in a separate issue.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #163, Tier 5 card identity provenance boundary under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/163
- Previous completed issue: #161
- Latest verified integration commit: 2a96d5701f6939fd7a78d71383c35d43095d69c0
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier5-card-identity
- Contract: docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- Expected implementation handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier5_card_identity_comparison.md

Goal:
Implement only the metadata and focused test changes needed to satisfy the Tier 5 card identity contract. Seed exactly one Tier 5 evidence-ledger field, `grp_id`, and preserve card names, catalog lookup, deck identity, collection ownership, gameplay-action provenance, opponent-card-observation provenance, analytics, and AI as enrichment/future/downstream boundaries rather than parser truth.

Read first:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md
- docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md
- docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md
- docs/contracts/parser_opponent_card_observations.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- src/mythic_edge_parser/app/grp_id_catalog.py
- src/mythic_edge_parser/app/card_catalog.py

Do:
- Compare current evidence-ledger behavior against the contract before editing.
- Change Tier 5 `card_identity_and_gameplay_actions` from `registered_future` to `seeded_sample`.
- Add exactly one Tier 5 seed field: `grp_id`.
- Keep `gameplay_action` and `opponent_card_observation` as future fields.
- Add a validating entry `tier5.card_identity.grp_id`.
- Document direct and fallback evidence paths for direct `grpId`, object-source ID, overlay ID, parent-chain, prior-instance, replacement-chain, submitted-deck ID lists, opening-hand ID/name-resolution path context, GRP catalog enrichment, active deck display context, and GRP candidate review context.
- Add focused tests proving the Tier 5 seed field, entry, policies, degradation behavior, and protected non-truth boundaries.
- Preserve Tier 3 opening-hand, Tier 4 submitted-deck, and Tier 4 deck-state boundary behavior and tests.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_tier5_card_identity_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Implement parser behavior changes.
- Change GameState parsing, extractors, gameplay-action classification, opponent-card-observation behavior, card catalog refresh/sync behavior, GRP candidate scoring or promotion, runtime active deck artifact shape, runtime status fields, generated card data, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, production behavior, environment variable contracts, OpenAI/model-provider behavior, or AI/analytics truth.
- Add seed fields for card_name, display_name, resolution_status, layout, card_faces, observed_grp_id, overlay_grp_id, object_source_grp_id, parent_id, identity_hint_source, gameplay_action, opponent_card_observation, deck names, deck IDs, collection ownership, decklist identity, sideboard deltas, archetypes, matchup plans, gameplay advice, player-mistake labels, model-provider output, or AI.
- Commit raw private Player.log excerpts, raw submitted-deck values, raw decklists, local runtime artifacts, generated card data, failed posts, runtime status files, workbook exports, secrets, tokens, credentials, or webhook URLs.
- Target main directly or close tracker #11.

Validation:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m ruff check src tests tools
- git diff --check
- If adjacent surfaces are touched or referenced in changed tests: python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_grp_id_catalog.py tests/test_card_catalog.py
- If available: python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/163"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier5_card_identity.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier5_card_identity_comparison.md"
  verdict: "contract_complete_ready_for_metadata_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier5-card-identity"
  latest_verified_remote_commit: "2a96d5701f6939fd7a78d71383c35d43095d69c0"
  authorized_seed_fields:
    - "grp_id"
  authorized_seed_entries:
    - "tier5.card_identity.grp_id"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_grp_id_catalog.py tests/test_card_catalog.py if adjacent surfaces are touched or changed tests reference them"
    - "python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence if available"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #11."
    - "Do not implement parser behavior changes."
    - "Do not change GameState parsing, extractors, gameplay-action classification, opponent-card-observation behavior, card catalog refresh/sync behavior, GRP candidate scoring or promotion, runtime active deck artifact shape, runtime status fields, generated card data, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, production behavior, environment variable contracts, OpenAI/model-provider behavior, or AI/analytics truth."
    - "Do not add seed fields for card_name, display_name, resolution_status, layout, card_faces, observed_grp_id, overlay_grp_id, object_source_grp_id, parent_id, identity_hint_source, gameplay_action, opponent_card_observation, deck names, deck IDs, collection ownership, decklist identity, sideboard deltas, archetypes, matchup plans, gameplay advice, player-mistake labels, model-provider output, or AI."
    - "Do not commit raw private Player.log excerpts, raw submitted-deck values, raw decklists, local runtime artifacts, generated card data, failed posts, runtime status files, workbook exports, secrets, tokens, credentials, or webhook URLs."
```
