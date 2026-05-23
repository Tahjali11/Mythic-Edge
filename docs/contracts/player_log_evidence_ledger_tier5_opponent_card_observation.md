# Player.log Evidence Ledger Tier 5 Opponent-Card-Observation Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/166
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- recent_completed_child: https://github.com/Tahjali11/Mythic-Edge/issues/165
- recent_completed_commit: 50cab7cf9d08761a9d16cb2dbabbb5fe7578a393
- base_branch: codex/parser-reliability-intelligence
- target_artifact: docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier5_opponent_card_observation_comparison.md
- risk_tier: Medium-High
- status: contract only

## Source Artifacts

- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md
- docs/contracts/parser_opponent_card_observations.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier5_gameplay_action_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier5_gameplay_action.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- src/mythic_edge_parser/app/evidence_ledger.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- src/mythic_edge_parser/app/gameplay_actions.py
- tests/test_opponent_card_observations.py
- tests/test_evidence_ledger.py
- GitHub issue #166

## Purpose

Issue #166 maps the remaining Tier 5 future field,
`opponent_card_observation`, into the Player.log evidence ledger.

Plain English: Mythic Edge already has parser-supported visible opponent-card
observation records. The ledger now needs to explain what those records can
prove, what evidence they depend on, how confidence and source labels should be
read, and where the boundary stops before downstream analytics, coaching, or AI
turn visible-card evidence into guesses.

This is a provenance contract only. It does not authorize parser behavior
changes, observation behavior changes, payload shape changes, workbook exposure,
webhook exposure, Apps Script changes, analytics truth, AI truth, or model
provider behavior.

## Relationship To Prior Tier 5 Contracts

Opponent-card-observation provenance follows two earlier Tier 5 foundations:

- `grp_id` provenance explains card identity support and uncertainty.
- `gameplay_action` provenance explains action-level evidence, actor relation,
  visibility-adjacent action facets, zone context, and action/source labels.

This contract maps the higher-level visible opponent-card observation that is
derived from those surfaces.

Required sequencing:

1. Tier 5 `grp_id` remains seeded by issue #163.
2. Tier 5 `gameplay_action` remains seeded by issue #165.
3. Tier 5 `opponent_card_observation` becomes the third and final current Tier
   5 seed field in issue #166.

`docs/contracts/parser_opponent_card_observations.md` remains authoritative for
the observation helper interface and payload shape. This contract does not
change that module contract; it adds ledger provenance for the already existing
surface.

## Observed Current Behavior

Observed on `codex/parser-reliability-intelligence` at
50cab7cf9d08761a9d16cb2dbabbb5fe7578a393:

- Issue #166 is open and tracker #11 remains open.
- Tier 5 `card_identity_and_gameplay_actions` has status `seeded_sample`.
- Tier 5 `seed_fields` is currently `["grp_id", "gameplay_action"]`.
- Tier 5 `future_fields` is currently `["opponent_card_observation"]`.
- Existing Tier 5 entries are:
  - `tier5.card_identity.grp_id`
  - `tier5.gameplay_action.gameplay_action`
- No ledger entry currently starts with `tier5.opponent_card_observation.`.
- `src/mythic_edge_parser/app/opponent_card_observations.py` already provides:
  - `build_opponent_card_observation(action_entry)`
  - `build_opponent_card_observations_payload(action_entries, match_id="")`
  - constants for object names and `SCHEMA_VERSION`.
- `build_opponent_card_observation()` returns `None` for non-mapping inputs,
  non-opponent action entries, unsupported action types, and hidden draws from
  library to hand without reveal or public-zone evidence.
- The helper emits an observation only when the source action entry is
  opponent-related and visibility is not `hidden_not_recorded`.
- Existing observation fields include identity, action, source, visibility,
  status, confidence, degradation, and review metadata.
- Existing visibility values include `action_visible`, `revealed`,
  `public_zone`, `derived_zone_transition`, and `ambiguous`.
- Existing hidden draw behavior suppresses clean observations.
- Existing source evidence values can include `action_array`, `annotation`,
  `zone_transition`, `object_presence_public_zone`, `gameplay_action_entry`,
  or `mixed`.
- Existing evidence status values include `observed`, `degraded`, and
  `conflict`.
- Existing value source values include `observed`, `derived`, `unknown`, and
  `conflict`.
- Existing confidence values include `high`, `medium`, `low`, and `unknown`.
- Existing degradation flags include `missing_seat_mapping`,
  `actor_relation_conflict`, `action_seat_conflict`, `missing_card_identity`,
  `name_resolution_candidate`, `name_resolution_ambiguous`,
  `name_resolution_contradicted`, `name_resolution_name_only`,
  `name_resolution_unresolved`, `ambiguous_visibility`, and
  `data_loss_evidence`.
- Existing tests cover visible spell preservation, action-array seat fallback,
  observed/canonical identity differences, local/non-mapping suppression,
  missing-seat degradation, hidden draw suppression, missing identity
  degradation, candidate/contradicted name handling, actor-seat conflict,
  unresolved known-ID placeholder display, and collection payload counts.
- The #165 contract-test report recorded one non-blocking P3 test-hardening
  note: focused tests do not directly assert the exact set of
  `tier5.gameplay_action.*` entries.

## Scope Decision

The future implementation must add exactly one new Tier 5 seed field:

```yaml
seed_field: "opponent_card_observation"
ledger_entry_id: "tier5.opponent_card_observation.opponent_card_observation"
```

After implementation, the Tier 5 family must have:

```yaml
seed_fields:
  - "grp_id"
  - "gameplay_action"
  - "opponent_card_observation"
future_fields: []
```

Do not add separate Tier 5 seed fields for observation facets such as
`visibility`, `source_evidence`, `evidence_status`, `value_source`,
`confidence`, `review_required`, `degradation_flags`, `actor_seat_id`,
`local_seat_id`, `action_type`, `from_zone_type`, `to_zone_type`, `card_name`,
`display_name`, `resolution_status`, `name_resolution_source`, `layout`,
`card_faces`, hidden cards, decklists, sideboard deltas, archetypes, advice,
Line Tracer output, AI output, or model-provider output.

Those values are facets, evidence signals, dependencies, degradation labels, or
downstream context for the single `opponent_card_observation` entry.

## Truth Ownership

The parser-owned observation helper owns normalized visible opponent-card
observation facts. The evidence ledger owns provenance metadata that explains
support, uncertainty, confidence, and drift for those facts.

The ledger must not become:

- a second opponent-card parser;
- a hidden-card inference system;
- a complete opponent decklist builder;
- a sideboard-delta inference layer;
- an archetype classifier;
- a Line Tracer or coaching truth source;
- a player-mistake labeler;
- a model-provider or AI truth source;
- a workbook, webhook, or Apps Script workaround.

Downstream analytics may consume observations only with the associated source,
confidence, finality, visibility, degradation, and review labels.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md

Future implementation may touch only these files unless a later issue expands
scope:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier5_opponent_card_observation_comparison.md
- optional review report:
  docs/contract_test_reports/player_log_evidence_ledger_tier5_opponent_card_observation.md

Referenced but not behavior-owned by this contract:

- src/mythic_edge_parser/app/opponent_card_observations.py
- src/mythic_edge_parser/app/gameplay_actions.py
- tests/test_opponent_card_observations.py
- tests/test_gameplay_actions.py
- runtime opponent-card or gameplay-action artifacts
- workbook, webhook, Apps Script, production, analytics, AI, and model-provider
  surfaces

## Required Ledger Family Behavior

The Tier 5 `card_identity_and_gameplay_actions` family must:

- keep status `seeded_sample`;
- list `seed_fields` exactly as `["grp_id", "gameplay_action",
  "opponent_card_observation"]`;
- list `future_fields` as an empty list;
- include notes that issues #163, #165, and #166 map the current Tier 5 seed
  fields;
- preserve notes that card names, display labels, catalog lookup, deck identity,
  collection ownership, archetypes, gameplay advice, model-provider output, and
  AI remain enrichment or downstream surfaces;
- include both `gameplay_actions.py` and `opponent_card_observations.py` as
  owner modules.

## Required Ledger Entry

Add one ledger entry with this logical identity:

```yaml
entry_id: "tier5.opponent_card_observation.opponent_card_observation"
tier: 5
output_family: "card_identity_and_gameplay_actions"
output_field: "opponent_card_observation"
display_name: "Opponent Card Observation"
parser_owner: "src/mythic_edge_parser/app/opponent_card_observations.py"
model_surface: "opponent_card_observation / opponent_card_observations_payload"
parser_managed_truth: true
coverage_status: "seeded_sample"
```

Required downstream surfaces:

- `opponent_card_observations`
- `future_card_performance`
- `future_analytics_consumers`

Allowed dependency surfaces:

- `gameplay_actions`
- `tier5.card_identity.grp_id`
- `tier5.gameplay_action.gameplay_action`
- `grp_id_catalog`

Dependency surfaces must not be represented as independent truth for this entry.

## Observation Facets

The `opponent_card_observation` entry must document these facets as parts of
the single broad field:

| Facet | Contract Status |
| --- | --- |
| `object` | Payload marker, not separate truth. |
| `schema_version` | Payload schema marker, not workbook/webhook schema. |
| `match_id` | Match association context from gameplay action. |
| `game_number` | Game association context from gameplay action. |
| `game_state_id` | GRE state context from gameplay action. |
| `timestamp` | Event timing context, live/provisional. |
| `turn_number` | Turn context from gameplay action. |
| `actor_relation` | Must be `opponent` for emitted observations. |
| `actor_seat_id` and `local_seat_id` | Seat mapping context. |
| `instance_id` | Game-local object identity, not durable card identity. |
| `grp_id` and identity hints | Card identity dependency governed by Tier 5 `grp_id`. |
| `card_name` and `display_name` | Enrichment/display context. |
| `resolution_status` and `name_resolution_source` | Name-resolution confidence context. |
| `action_type` and `cast_mode` | Gameplay-action dependency context. |
| `source_evidence` | Source label derived from action array, annotation, zone, public-zone, or mixed support. |
| `evidence_status` | Observation support status. |
| `value_source` | Ledger-compatible source label. |
| `confidence` | Ledger-compatible confidence label. |
| `visibility` | Public visibility boundary. |
| `from_zone_type` and `to_zone_type` | Zone context for visibility and action support. |
| `raw_action_types` | Preserved action-array labels when available. |
| `annotation_types` and `annotation_categories` | Reveal or support context. |
| `degradation_flags` | Explicit uncertainty and drift context. |
| `review_required` | Downstream review flag, not truth. |

## Direct Evidence Signals

The `opponent_card_observation` ledger entry must include direct evidence for
current visible observation sources. Signal IDs may vary if they remain stable,
lower-case, dot-separated, unique within the entry, and semantically equivalent.

Required direct signal coverage:

- `opponent_card_observation.visible_action_source`
  - parser_event_kind: `opponent_card_observation`
  - parser_event_type: `parser_opponent_card_observations.v1`
  - raw_event_family: `derived_from_gameplay_action`
  - normalized_payload_path:
    `opponent_card_observation.action_type +
    opponent_card_observation.source_evidence +
    opponent_card_observation.raw_action_types`
  - raw_payload_path:
    `gameplay_action_entry.action_type + gameplay_action_entry.raw_action_types`
  - value_source_when_used: `observed`
  - confidence_when_used: `high`
  - finality_when_used: `provisional`

- `opponent_card_observation.visibility_context`
  - parser_event_kind: `opponent_card_observation`
  - parser_event_type: `parser_opponent_card_observations.v1`
  - raw_event_family: `derived_from_gameplay_action`
  - normalized_payload_path:
    `opponent_card_observation.visibility +
    opponent_card_observation.from_zone_type +
    opponent_card_observation.to_zone_type`
  - raw_payload_path:
    `gameplay_action_entry.action_type + gameplay_action_entry.from_zone_type +
    gameplay_action_entry.to_zone_type + gameplay_action_entry.annotation_types +
    gameplay_action_entry.annotation_categories`
  - value_source_when_used: `observed`
  - confidence_when_used: `high`
  - finality_when_used: `provisional`

- `opponent_card_observation.actor_seat_context`
  - parser_event_kind: `opponent_card_observation`
  - parser_event_type: `parser_opponent_card_observations.v1`
  - raw_event_family: `derived_from_gameplay_action`
  - normalized_payload_path:
    `opponent_card_observation.actor_relation +
    opponent_card_observation.actor_seat_id +
    opponent_card_observation.local_seat_id`
  - raw_payload_path:
    `gameplay_action_entry.actor_relation +
    gameplay_action_entry.actor_seat_id +
    gameplay_action_entry.local_seat_id +
    gameplay_action_entry.raw_action_types`
  - value_source_when_used: `derived`
  - confidence_when_used: `medium`
  - finality_when_used: `provisional`

- `opponent_card_observation.card_identity_context`
  - parser_event_kind: `opponent_card_observation`
  - parser_event_type: `parser_opponent_card_observations.v1`
  - raw_event_family: `derived_from_gameplay_action`
  - normalized_payload_path:
    `opponent_card_observation.grp_id +
    opponent_card_observation.observed_grp_id +
    opponent_card_observation.overlay_grp_id +
    opponent_card_observation.object_source_grp_id +
    opponent_card_observation.parent_id +
    opponent_card_observation.identity_hint_source`
  - raw_payload_path:
    `gameplay_action_entry.grp_id + gameplay_action_entry.observed_grp_id +
    gameplay_action_entry.overlay_grp_id +
    gameplay_action_entry.object_source_grp_id +
    gameplay_action_entry.parent_id +
    gameplay_action_entry.identity_hint_source`
  - value_source_when_used: `observed`
  - confidence_when_used: `high`
  - finality_when_used: `provisional`

- `opponent_card_observation.status_context`
  - parser_event_kind: `opponent_card_observation`
  - parser_event_type: `parser_opponent_card_observations.v1`
  - raw_event_family: `derived_from_gameplay_action`
  - normalized_payload_path:
    `opponent_card_observation.evidence_status +
    opponent_card_observation.value_source +
    opponent_card_observation.confidence +
    opponent_card_observation.degradation_flags +
    opponent_card_observation.review_required`
  - raw_payload_path:
    `gameplay_action_entry + opponent_card_observation computed status labels`
  - value_source_when_used: `derived`
  - confidence_when_used: `medium`
  - finality_when_used: `provisional`

## Fallback Evidence Signals

The entry must include fallback/degraded evidence for:

- `opponent_card_observation.revealed_annotation_context`
  - describes reveal evidence from annotation types or categories;
  - value_source_when_used: `observed`;
  - confidence_when_used: `high` when card identity and seat mapping remain
    clean, otherwise degraded by status context.

- `opponent_card_observation.public_zone_presence`
  - describes public-zone visibility such as battlefield, command, exile,
    graveyard, limbo, revealed, or stack presence;
  - value_source_when_used: `observed`;
  - confidence_when_used: `high` when identity and seat mapping remain clean.

- `opponent_card_observation.derived_zone_transition`
  - describes visibility derived from transitions involving public zones;
  - value_source_when_used: `derived`;
  - confidence_when_used: `medium`.

- `tier5.gameplay_action.gameplay_action_dependency`
  - describes dependency on the existing gameplay-action entry;
  - value_source_when_used: `derived`;
  - confidence_when_used: `medium`;
  - missing_behavior: missing or degraded gameplay-action provenance degrades
    observation provenance.

- `tier5.card_identity.grp_id_dependency`
  - describes dependency on the existing card identity entry;
  - value_source_when_used: `derived`;
  - confidence_when_used: `medium`;
  - missing_behavior: missing card identity leaves the observation degraded or
    review-required, not guessed.

- `opponent_card_observation.name_resolution_enrichment`
  - describes `card_name`, `display_name`, `resolution_status`,
    `name_resolution_source`, `layout`, and `card_faces` as display/enrichment
    context;
  - value_source_when_used: `legacy_enriched`;
  - confidence_when_used: `low`;
  - missing_behavior: display/name gaps must not erase visible-card evidence or
    promote names to observed Player.log truth.

- `opponent_card_observation.degraded_or_conflicting_status`
  - describes missing seat mapping, actor-seat conflict, missing card identity,
    ambiguous visibility, candidate/ambiguous/contradicted/name-only
    resolution, and data-loss evidence;
  - value_source_when_used: `unknown` or `conflict`;
  - confidence_when_used: `low`.

## Value-Source Policy

The `opponent_card_observation` entry must use this policy:

```yaml
value_source_policy:
  direct: "observed"
  fallback: "derived"
  inferred: "inferred"
  unavailable: "unknown"
  contradiction: "conflict"
  historical: "legacy_enriched"
```

Interpretation:

- `observed`: visible action, reveal, public-zone presence, direct raw action
  labels, or direct visible identity evidence from gameplay-action sources.
- `derived`: visible observation support computed from gameplay-action context,
  seat mapping, zone transitions, or Tier 5 dependencies.
- `inferred`: reserved for future best-effort fallbacks; current implementation
  should avoid promoting inferred opponent facts.
- `unknown`: missing seat mapping, missing identity, unavailable source evidence,
  or status that cannot safely support a fact.
- `conflict`: actor-seat disagreement, contradicted name resolution, or other
  contradictory evidence.
- `legacy_enriched`: display names, catalog labels, layout, faces, and other
  enrichment context.

## Confidence Policy

The `opponent_card_observation` entry must use this policy:

```yaml
confidence_policy:
  direct: "high"
  fallback: "medium"
  inferred: "low"
  unavailable: "unknown"
  contradiction: "low"
```

Required confidence boundaries:

- High confidence is allowed for clean visible observations with opponent actor
  relation, non-hidden visibility, usable card identity, and no degradation
  flags.
- Medium confidence is appropriate for candidate name resolution or derived
  zone-transition observations.
- Low confidence is required for conflicts, missing seat mapping, missing card
  identity, ambiguous visibility, contradicted/ambiguous/name-only name
  resolution, and data-loss evidence.
- Unknown confidence is required when evidence is insufficient or unavailable.

## Finality Policy

The `opponent_card_observation` entry must use this policy:

```yaml
finality_policy:
  live: "live"
  provisional: "provisional"
  final: "final"
  reconciled: "reconciled"
```

Current opponent-card observations are event/action-scoped parser observations
derived from gameplay-action entries. They are not final workbook facts and do
not have field-level final reconciliation. A later contract must define any
row-level final or reconciled attachment before downstream analytics treat an
observation as final evidence.

## Invariant Checks

The entry must include invariant names proving:

- `tier5_seeds_exactly_grp_id_gameplay_action_and_opponent_card_observation`
- `tier5_future_fields_empty_after_opponent_card_observation_seed`
- `opponent_card_observation_is_single_seed_with_facets_not_many_seed_fields`
- `opponent_card_observation_depends_on_tier5_grp_id`
- `opponent_card_observation_depends_on_tier5_gameplay_action`
- `opponent_card_observation_requires_opponent_actor_relation`
- `opponent_card_observation_hidden_draws_are_not_recorded`
- `opponent_card_observation_visibility_labels_preserve_public_evidence_boundary`
- `opponent_card_observation_source_confidence_and_degradation_travel_together`
- `opponent_card_observation_name_resolution_is_enrichment_context_only`
- `opponent_card_observation_does_not_infer_hidden_cards_or_complete_decklists`
- `opponent_card_observation_does_not_prove_sideboard_archetype_advice_line_tracer_ai_or_model_truth`
- `opponent_card_observation_workbook_webhook_apps_script_analytics_and_ai_are_not_source_truth`
- `opponent_card_observation_privacy_path_only_no_values`

Codex C may choose equivalent stable invariant names if focused tests prove the
same guarantees.

## Degradation Behavior

The entry must document degradation for:

- non-mapping action input;
- non-opponent action input;
- unsupported or missing action type;
- hidden draw from library to hand without reveal/public-zone evidence;
- missing local or actor seat mapping;
- actor relation conflict;
- action-seat conflict;
- missing `grp_id` and `observed_grp_id`;
- candidate, ambiguous, contradicted, name-only, or unresolved name resolution;
- ambiguous visibility;
- data-loss or truncation evidence;
- missing gameplay-action dependency;
- degraded gameplay-action provenance;
- missing card-identity dependency;
- display/catalog enrichment being unavailable or contradicted.

Expected degradation behavior is neutral omission, explicit `unknown`,
`derived`, or `conflict` value-source labels, lower confidence, degradation
flags, and `review_required` when appropriate. The ledger must not reconstruct
missing observation facts from workbook formulas, dashboards, Apps Script,
webhooks, AI, archetype labels, card-performance analytics, or model-provider
output.

## Drift And Downstream Analytics Labels

The entry must include drift flags that downstream analytics can preserve:

- `missing_expected_payload_path`
- `fallback_used`
- `weak_fallback_used`
- `conflicting_evidence`
- `invariant_failed`
- `schema_snapshot_missing`
- `fixture_gap`
- `sensitive_evidence_redacted`

Downstream analytics must treat `degradation_flags`, `visibility`,
`value_source`, `confidence`, `evidence_status`, `review_required`, and
`finality_policy` as required context. Analytics that ignore those labels must
not claim clean opponent-card truth.

## #165 P3 Test-Hardening Note

The #165 contract-test report recorded a non-blocking P3 finding: focused tests
did not directly assert that the exact set of `tier5.gameplay_action.*` entries
is `{"tier5.gameplay_action.gameplay_action"}`.

Because issue #166 necessarily updates `tests/test_evidence_ledger.py`, Codex C
should include this as a narrow test-hardening acceptance item:

- assert that `tier5.gameplay_action.*` entry IDs are exactly
  `{"tier5.gameplay_action.gameplay_action"}`;
- assert that `tier5.opponent_card_observation.*` entry IDs are exactly
  `{"tier5.opponent_card_observation.opponent_card_observation"}`.

This is test hardening only. It must not change gameplay-action behavior,
opponent-card-observation behavior, parser behavior, or runtime artifact shape.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- gameplay-action extraction or classification behavior;
- opponent-card-observation behavior;
- parser state final reconciliation;
- parser event classes;
- event `kind` values;
- parser payload shapes;
- match identity;
- game identity;
- deduplication;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- output transport;
- production behavior;
- runtime status files;
- failed posts;
- workbook exports;
- runtime action artifact shape;
- local runtime artifacts;
- generated card data;
- raw private `Player.log` excerpts;
- secrets, credentials, webhook URLs, API keys, tokens, or environment variables;
- analytics truth;
- AI truth;
- Line Tracer or coaching truth;
- OpenAI or model-provider behavior;
- schema snapshots;
- golden fixtures;
- drift baselines;
- CI gates or Pyright gate behavior.

Protected-surface warnings are review signals, not authorization.

## Out Of Scope

Do not implement or authorize:

- hidden-card inference;
- complete opponent decklist reconstruction;
- sideboard-delta inference;
- archetype classification;
- gameplay advice;
- player-mistake labels;
- Line Tracer behavior;
- AI coaching behavior;
- model-provider calls or truth;
- card-performance aggregation changes;
- workbook/webhook/App Script exposure;
- runtime status schema changes;
- fixture, snapshot, or baseline changes;
- raw private log imports.

## Unknowns

- Whether future analytics should consume opponent observations directly or
  through a separate confidence-filtered analytics contract.
- Whether public-zone observations need a future sub-entry if downstream users
  need to separate public-zone presence from action-triggered visibility.
- Whether future final/reconciled labels should attach to observations after
  game or match completion.
- Whether golden fixtures should later include reduced opponent-observation
  expectations. This contract does not authorize fixture updates.
- Whether Line Tracer should consume opponent observations. That requires a
  separate issue and contract.

## Suspected Gaps

- Tier 5 still lists `opponent_card_observation` as a future field even though
  the helper module and focused tests already exist.
- No ledger entry currently explains observation provenance, visibility labels,
  source/confidence labels, degradation flags, or review-required semantics.
- Existing ledger tests still assert that `opponent_card_observation` is
  deferred.
- Current tests do not directly assert exact `tier5.gameplay_action.*` entry ID
  set, per the #165 P3 note.
- No ledger tests yet enforce the boundary that opponent observations do not
  prove hidden cards, decklists, sideboard deltas, archetypes, advice, Line
  Tracer output, AI output, or model-provider truth.

## Validation Requirements For Codex C

Required focused validation:

```powershell
py -m pytest -q tests\test_evidence_ledger.py
py -m pytest -q tests\test_opponent_card_observations.py
py -m ruff check src tests tools
git diff --check
```

Required adjacent validation if implementation references or changes gameplay
action tests, action-entry notes, or behavior-adjacent assertions:

```powershell
py -m pytest -q tests\test_gameplay_actions.py tests\test_opponent_card_observations.py
```

Required path-scoped protected-surface check for the expected changed-file set:

```powershell
@'
docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md
src/mythic_edge_parser/app/evidence_ledger.py
tests/test_evidence_ledger.py
docs/implementation_handoffs/player_log_evidence_ledger_tier5_opponent_card_observation_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
```

Codex C must state if any broader validation is skipped and why.

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`
  exists.
- Codex C compares current code/tests against this contract before editing.
- Tier 5 `seed_fields` becomes exactly `["grp_id", "gameplay_action",
  "opponent_card_observation"]`.
- Tier 5 `future_fields` becomes exactly `[]`.
- A validating entry exists for
  `tier5.opponent_card_observation.opponent_card_observation`.
- The new entry validates under the existing ledger schema.
- The new entry documents visible action, visibility, actor-seat, card identity,
  status, dependency, enrichment, value-source, confidence, finality, drift,
  invariant, degradation, and privacy boundaries.
- Focused tests prove `opponent_card_observation` is the only newly seeded Tier
  5 field.
- Focused tests prove no separate seed fields are added for observation facets,
  hidden cards, decklists, sideboard deltas, archetypes, advice, Line Tracer,
  AI, or model-provider output.
- Focused tests include the #165 exact-entry hardening assertion for
  `tier5.gameplay_action.*`.
- No parser behavior, gameplay-action behavior, opponent-card-observation
  behavior, workbook schema, webhook payload, Apps Script behavior, output
  transport, runtime artifact shape, runtime status file, raw log, secret,
  generated-data, failed-post, workbook-export, fixture, snapshot, drift
  baseline, production, analytics-truth, AI-truth, Line Tracer, or
  model-provider surface changes.
- Tracker #11 remains open.
- The work does not target `main` directly.

## Codex C Handoff Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #166.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/166

Base branch:
codex/parser-reliability-intelligence

Contract:
docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md

Expected implementation handoff:
docs/implementation_handoffs/player_log_evidence_ledger_tier5_opponent_card_observation_comparison.md

Goal:
Compare the current evidence-ledger code and tests against the Tier 5 opponent-card-observation contract, then implement only the metadata and focused tests needed to seed `opponent_card_observation` as a first-class Tier 5 evidence-ledger field. Preserve `grp_id` and `gameplay_action` provenance, and do not change opponent-card-observation parser behavior.

Before editing:
- Confirm the branch is `codex/parser-reliability-intelligence`.
- Inspect `git status --short --branch`.
- State what opponent-card-observation provenance is supposed to do, what current code/tests already do, what gaps remain, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/parser_opponent_card_observations.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md
- docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md
- docs/contract_test_reports/player_log_evidence_ledger_tier5_gameplay_action.md
- src/mythic_edge_parser/app/evidence_ledger.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- src/mythic_edge_parser/app/gameplay_actions.py
- tests/test_evidence_ledger.py
- tests/test_opponent_card_observations.py
- tests/test_gameplay_actions.py

Do:
- Change only evidence-ledger metadata and focused ledger tests unless comparison proves a docs-only note is needed.
- Keep Tier 5 status `seeded_sample`.
- Set Tier 5 seed fields to exactly `["grp_id", "gameplay_action", "opponent_card_observation"]`.
- Set Tier 5 future fields to exactly `[]`.
- Add one ledger entry: `tier5.opponent_card_observation.opponent_card_observation`.
- Document visible action, visibility, actor-seat, card identity, status, dependency, enrichment, value-source, confidence, finality, invariant, drift, degradation, and path-only privacy boundaries.
- Add focused tests proving no separate Tier 5 seed fields are added for observation facets, hidden cards, decklists, sideboard deltas, archetypes, advice, Line Tracer, AI, or model-provider output.
- Add the #165 P3 test-hardening assertion that the exact set of `tier5.gameplay_action.*` entry IDs is `{"tier5.gameplay_action.gameplay_action"}`.
- Add an equivalent exact-entry assertion for `tier5.opponent_card_observation.*`.
- Produce `docs/implementation_handoffs/player_log_evidence_ledger_tier5_opponent_card_observation_comparison.md`.

Do not:
- Change parser behavior.
- Change gameplay-action extraction or classification behavior.
- Change opponent-card-observation behavior or payload shape.
- Change parser state final reconciliation, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, production behavior, runtime status files, failed posts, workbook exports, runtime action artifact shape, local runtime artifacts, generated card data, raw logs, secrets, credentials, environment variables, schema snapshots, golden fixtures, drift baselines, CI gates, Pyright gate behavior, analytics truth, AI truth, Line Tracer behavior, OpenAI/model-provider behavior, or model-provider truth.
- Infer hidden cards, complete decklists, sideboard deltas, archetypes, gameplay advice, player mistake labels, Line Tracer/AI coaching, or model-provider truth.
- Target main directly.
- Close tracker #11.
- Stage, commit, push, open a PR, or merge unless explicitly asked.

Validation:
py -m pytest -q tests\test_evidence_ledger.py
py -m pytest -q tests\test_opponent_card_observations.py
py -m ruff check src tests tools
git diff --check

If adjacent behavior surfaces are referenced or touched, also run:
py -m pytest -q tests\test_gameplay_actions.py tests\test_opponent_card_observations.py

Run the path-scoped protected-surface check for changed files:
@'
docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md
src/mythic_edge_parser/app/evidence_ledger.py
tests/test_evidence_ledger.py
docs/implementation_handoffs/player_log_evidence_ledger_tier5_opponent_card_observation_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin

Final handoff must include:
- role performed
- issue/tracker used
- source artifacts inspected
- comparison summary
- files changed
- exact ledger/test sections changed
- validation run
- protected surfaces status
- remaining unverified layers
- next recommended role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/166"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier5_opponent_card_observation_comparison.md"
  verdict: "contract_complete_ready_for_metadata_implementation"
  risk_tier: "Medium-High"
  branch: "codex/parser-reliability-intelligence"
  authorized_seed_fields:
    - "grp_id"
    - "gameplay_action"
    - "opponent_card_observation"
  authorized_future_fields: []
  authorized_seed_entries:
    - "tier5.opponent_card_observation.opponent_card_observation"
  validation:
    - "py -m pytest -q tests\\test_evidence_ledger.py"
    - "py -m pytest -q tests\\test_opponent_card_observations.py"
    - "py -m ruff check src tests tools"
    - "git diff --check"
    - "py -m pytest -q tests\\test_gameplay_actions.py tests\\test_opponent_card_observations.py if adjacent behavior surfaces are referenced or touched"
    - "path-scoped protected-surface check for the changed-file set"
  test_hardening:
    - "Assert exact tier5.gameplay_action.* entry set to close #165 P3."
    - "Assert exact tier5.opponent_card_observation.* entry set."
  stop_conditions:
    - "Do not change parser behavior."
    - "Do not change gameplay-action extraction or classification behavior."
    - "Do not change opponent-card-observation behavior or payload shape."
    - "Do not infer hidden cards, complete decklists, sideboard deltas, archetypes, gameplay advice, player mistake labels, Line Tracer/AI coaching, or model-provider truth."
    - "Do not change parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, production behavior, runtime status files, failed posts, workbook exports, runtime action artifact shape, local runtime artifacts, generated card data, raw logs, secrets, schema snapshots, golden fixtures, drift baselines, CI gates, analytics truth, AI truth, OpenAI/model-provider behavior, or model-provider truth."
    - "Do not target main directly."
    - "Do not close tracker #11."
```
