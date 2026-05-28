# Player.log Evidence Ledger Tier 5 Gameplay-Action Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/165
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_child_issue: https://github.com/Tahjali11/Mythic-Edge/issues/163
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/164
- previous_merge_commit: 61cc0c58beec85a8aeb23247098619061f975b82
- base_branch: codex/parser-reliability-intelligence
- target_artifact: docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier5_gameplay_action_comparison.md
- risk_tier: High
- status: contract only

## Source Artifacts

- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/problem_representation.md
- docs/agent_threads/module_contract.md
- docs/templates/problem_representation.md
- docs/templates/module_contract.md
- docs/problem_representations/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier5_card_identity_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier5_card_identity.md
- docs/contracts/parser_opponent_card_observations.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- src/mythic_edge_parser/app/evidence_ledger.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- src/mythic_edge_parser/parsers/gre/
- tests/test_evidence_ledger.py
- tests/test_gameplay_actions.py
- tests/test_opponent_card_observations.py
- GitHub issue #11
- GitHub issue #163
- GitHub issue #165
- GitHub PR #164

## Purpose

Issue #165 advances the Player.log evidence ledger from Tier 5 card identity
provenance into Tier 5 gameplay-action provenance.

Plain English: the ledger should be able to describe why Mythic Edge believes a
parser-managed gameplay action exists, which raw or normalized evidence supports
that action, how confident that support is, and where the boundary stops. It
must not turn action evidence into coaching, analytics, hidden-card knowledge,
player-mistake labels, or strategic advice.

This contract authorizes a future implementation pass to add a ledger seed for
the broad `gameplay_action` field only. It does not authorize parser behavior
changes, action-classification changes, workbook/webhook changes, or runtime
artifact shape changes.

## Relationship To Prior Contracts

- `docs/contracts/player_log_evidence_ledger_schema.md` defines ledger object,
  family, entry, evidence-signal, value-source, confidence, finality, drift,
  invariant, privacy, and validation vocabulary.
- `docs/contracts/player_log_evidence_ledger_tier5_card_identity.md` seeded
  exactly one Tier 5 field, `grp_id`, and left `gameplay_action` and
  `opponent_card_observation` as future fields.
- This contract moves only `gameplay_action` from Tier 5 future field to Tier 5
  seed field.
- `opponent_card_observation` remains a future Tier 5 field. It may be
  mentioned as a downstream consumer or dependency boundary, but it must not be
  seeded or redefined in this issue.
- `grp_id` provenance remains governed by the Tier 5 card-identity contract.
  This contract may depend on `grp_id` for card identity facets, but it must not
  duplicate or replace `grp_id` truth.

## Observed Current Behavior

Observed on `codex/parser-reliability-intelligence` at merge commit
61cc0c58beec85a8aeb23247098619061f975b82:

- Issue #165 is open and issue #11 remains open.
- Tier 5 `card_identity_and_gameplay_actions` currently has status
  `seeded_sample`.
- Tier 5 currently has `seed_fields: ["grp_id"]`.
- Tier 5 currently has `future_fields: ["gameplay_action",
  "opponent_card_observation"]`.
- `tests/test_evidence_ledger.py` currently treats `gameplay_action` and
  `opponent_card_observation` as deferred Tier 5 fields and forbids them as
  seed fields.
- `src/mythic_edge_parser/app/gameplay_actions.py` observes only parser events
  whose `kind` is `GameState`.
- Gameplay-action rows are built from GRE `GameState` payload context, action
  arrays, game object state, zone transitions, annotations, replacement-chain
  context, prior object state, turn tracking, seat mapping, and catalog/display
  enrichment.
- Existing action entry facets include `timestamp`, `match_id`, `game_number`,
  `game_state_id`, `turn_number`, `action_type`, `cast_mode`, `instance_id`,
  `grp_id`, `observed_grp_id`, `object_source_grp_id`, `overlay_grp_id`,
  `parent_id`, `identity_hint_source`, `actor_relation`, `actor_seat_id`,
  `from_zone_type`, `to_zone_type`, `raw_action_types`, `annotation_types`,
  `annotation_categories`, `replacement_source_id`, and
  `replacement_target_id`.
- Existing rendered/report facets include display labels, card name context,
  resolution status, layout, card faces, and summary text. Those facets are
  enrichment or display context, not new parser truth.
- `src/mythic_edge_parser/app/opponent_card_observations.py` consumes gameplay
  action entries to produce opponent-card-observation artifacts. That surface
  remains downstream and deferred for this contract.
- Existing runtime action files and status files are local runtime artifacts and
  are not ledger source truth.

## Required Scope Decision

The future implementation must add exactly one new Tier 5 seed field:

```yaml
seed_field: "gameplay_action"
ledger_entry_id: "tier5.gameplay_action.gameplay_action"
```

After implementation, the Tier 5 family must have:

```yaml
seed_fields:
  - "grp_id"
  - "gameplay_action"
future_fields:
  - "opponent_card_observation"
```

Do not add separate Tier 5 seed fields for `action_type`, `timestamp`,
`match_id`, `game_number`, `game_state_id`, `turn_number`, `actor_relation`,
`actor_seat_id`, `from_zone_type`, `to_zone_type`, `cast_mode`,
`raw_action_types`, `annotation_types`, `annotation_categories`,
`resolution_status`, `card_name`, `display_name`, `summary`, `grp_id`, or
`opponent_card_observation`.

Those values are facets, evidence signals, dependencies, or display context for
the single `gameplay_action` entry.

## Truth Ownership

Parser/state and parser-owned action processing own gameplay-action
interpretation. The evidence ledger describes provenance for parser-managed
action facts; it does not compute or correct them.

The ledger must not become:

- a second gameplay-action parser;
- a workbook workaround;
- a webhook or Apps Script schema migration;
- an analytics truth source;
- an AI or coaching truth source;
- a hidden-card inference engine;
- a player-mistake classifier;
- a strategic advice layer.

Downstream analytics, reports, workbooks, dashboards, Apps Script, webhook
transport, and AI may consume parser-produced gameplay-action facts only as
downstream context.

## Public Interfaces

Future implementation may touch only these surfaces unless a later issue
explicitly expands scope:

- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`
- `docs/implementation_handoffs/player_log_evidence_ledger_tier5_gameplay_action_comparison.md`
- optional focused review report:
  `docs/contract_test_reports/player_log_evidence_ledger_tier5_gameplay_action.md`

Referenced but not behavior-owned by this contract:

- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `tests/test_gameplay_actions.py`
- `tests/test_opponent_card_observations.py`
- schema snapshots and golden fixtures
- runtime gameplay-action artifacts
- workbook/webhook/App Script surfaces

## Required Ledger Family Behavior

The Tier 5 family entry for `card_identity_and_gameplay_actions` must:

- keep status `seeded_sample`;
- include `grp_id` and `gameplay_action` in `seed_fields`;
- keep `opponent_card_observation` in `future_fields`;
- preserve notes saying card names, display labels, catalog lookup, deck
  identity, collection ownership, archetypes, gameplay advice,
  model-provider output, and AI remain enrichment or downstream surfaces;
- include `src/mythic_edge_parser/app/gameplay_actions.py` in owner modules;
- include `src/mythic_edge_parser/app/opponent_card_observations.py` only as a
  downstream/future boundary, not as a seeded owner for this issue.

## Required Ledger Entry

Add one ledger entry with this logical identity:

```yaml
entry_id: "tier5.gameplay_action.gameplay_action"
tier: 5
output_family: "card_identity_and_gameplay_actions"
output_field: "gameplay_action"
display_name: "Gameplay Action"
parser_owner: "src/mythic_edge_parser/app/gameplay_actions.py"
model_surface: "gameplay_action_entry"
parser_managed_truth: true
coverage_status: "seeded_sample"
```

Required downstream surfaces:

- `gameplay_actions`
- `opponent_card_observations`
- `future_card_performance`
- `future_analytics_consumers`

Allowed downstream surfaces may also name local action reports or runtime action
views, but they must be labeled as downstream/runtime surfaces, not source
truth.

## Gameplay-Action Facets

The `gameplay_action` entry must document provenance for these facets as parts
of the single broad field:

| Facet | Contract Status |
| --- | --- |
| `timestamp` | Event timing context for the action, not a separate seed field. |
| `match_id` | Match association context, not match identity truth. |
| `game_number` | Game association context, not game identity truth. |
| `game_state_id` | GRE state context, not durable row identity. |
| `turn_number` | Turn context when available or derived by existing action tracking. |
| `action_type` | Parser-owned normalized action classification. |
| `raw_action_types` | Preserved raw action-array labels when present. |
| `cast_mode` | Derived action detail for existing cast-mode classification. |
| `actor_relation` | Seat-mapping-derived local/opponent/unknown context. |
| `actor_seat_id` | Observed or derived seat context, not player identity truth. |
| `from_zone_type` | Zone-transition context. |
| `to_zone_type` | Zone-transition context. |
| `grp_id` and related ID hints | Card identity dependency governed by Tier 5 `grp_id`. |
| annotations and categories | Supporting action evidence or degradation context. |
| replacement IDs | Supporting context for object replacement chains. |
| display/card-name/summary fields | Enrichment/display context only. |

## Direct Evidence Signals

The `gameplay_action` ledger entry must include direct evidence signals for
current observed gameplay-action sources. Signal IDs may be adjusted by Codex C
if they remain stable, lower-case, dot-separated, unique within the entry, and
semantically equivalent.

Required direct signal coverage:

- `game_state.gameplay_action.event_context`
  - parser_event_kind: `GameState`
  - parser_event_type: `GREMessageType_GameStateMessage`
  - raw_event_family: `greToClientEvent`
  - normalized_payload_path:
    `gameplay_action_entry.timestamp + gameplay_action_entry.match_id +
    gameplay_action_entry.game_number + gameplay_action_entry.game_state_id`
  - raw_payload_path:
    `greToClientMessages[].gameStateMessage + EventMetadata.timestamp`
  - value_source_when_used: `observed`
  - confidence_when_used: `high`
  - finality_when_used: `live`

- `game_state.gameplay_action.action_array`
  - parser_event_kind: `GameState`
  - parser_event_type: `GREMessageType_GameStateMessage`
  - raw_event_family: `greToClientEvent`
  - normalized_payload_path:
    `gameplay_action_entry.raw_action_types + gameplay_action_entry.action_type`
  - raw_payload_path:
    `greToClientMessages[].gameStateMessage.actions[].action.actionType`
  - value_source_when_used: `observed`
  - confidence_when_used: `high`
  - finality_when_used: `live`

- `game_state.gameplay_action.turn_context`
  - parser_event_kind: `GameState`
  - parser_event_type: `GREMessageType_GameStateMessage`
  - raw_event_family: `greToClientEvent`
  - normalized_payload_path: `gameplay_action_entry.turn_number`
  - raw_payload_path: `greToClientMessages[].gameStateMessage.turnInfo`
  - value_source_when_used: `observed`
  - confidence_when_used: `high`
  - finality_when_used: `live`

- `game_state.gameplay_action.object_zone_context`
  - parser_event_kind: `GameState`
  - parser_event_type: `GREMessageType_GameStateMessage`
  - raw_event_family: `greToClientEvent`
  - normalized_payload_path:
    `gameplay_action_entry.instance_id +
    gameplay_action_entry.from_zone_type + gameplay_action_entry.to_zone_type`
  - raw_payload_path:
    `greToClientMessages[].gameStateMessage.gameObjects[] +
    greToClientMessages[].gameStateMessage.zones[]`
  - value_source_when_used: `observed`
  - confidence_when_used: `high`
  - finality_when_used: `live`

- `game_state.gameplay_action.actor_context`
  - parser_event_kind: `GameState`
  - parser_event_type: `GREMessageType_GameStateMessage`
  - raw_event_family: `greToClientEvent`
  - normalized_payload_path:
    `gameplay_action_entry.actor_relation +
    gameplay_action_entry.actor_seat_id`
  - raw_payload_path:
    `greToClientMessages[].gameStateMessage.actions[].seatId +
    greToClientMessages[].gameStateMessage.gameObjects[].controllerSeatId`
  - value_source_when_used: `derived`
  - confidence_when_used: `medium`
  - finality_when_used: `live`

## Fallback Evidence Signals

The `gameplay_action` ledger entry must include fallback evidence for existing
derived action paths:

- `gameplay_action.zone_transition_diff`
  - describes existing classification from prior and current object zone state;
  - value_source_when_used: `derived`;
  - confidence_when_used: `medium`;
  - missing_behavior: action may be omitted or downgraded when previous/current
    zone evidence is missing or contradictory.

- `gameplay_action.partial_diff_inference`
  - describes existing partial-diff fallback classification when full prior
    object context is unavailable;
  - value_source_when_used: `inferred`;
  - confidence_when_used: `low`;
  - missing_behavior: do not promote to high confidence without direct action or
    complete zone evidence.

- `gameplay_action.annotation_context`
  - describes annotation types/categories that support or suppress action
    classification;
  - value_source_when_used: `derived`;
  - confidence_when_used: `medium`;
  - missing_behavior: action should remain uncertain when annotations are the
    only support.

- `tier5.card_identity.grp_id_dependency`
  - describes card identity dependency on the existing `tier5.card_identity.grp_id`
    entry;
  - value_source_when_used: `derived`;
  - confidence_when_used: `medium`;
  - missing_behavior: action may still exist without a card identity, but card
    identity confidence must not be overstated.

- `gameplay_action.rendered_display_context`
  - describes card names, display labels, summary text, layout, card faces, and
    resolution status as display/enrichment context;
  - value_source_when_used: `legacy_enriched`;
  - confidence_when_used: `low`;
  - missing_behavior: missing display context must not erase the underlying
    parser-owned action.

Do not use opponent-card-observation output as fallback source truth for
gameplay action. Opponent-card observation is a downstream consumer and remains
a future Tier 5 field.

## Value-Source Policy

The `gameplay_action` entry must use this policy:

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

- `observed`: direct current GameState evidence such as event context, raw
  action-array labels, object state, zone state, seat IDs, or turn data.
- `derived`: action facets computed from observed evidence without guessing,
  such as local/opponent relation from seat mapping or zone transition from
  prior/current object state.
- `inferred`: best-effort fallback from partial diffs or incomplete state.
- `unknown`: no usable evidence exists for the facet.
- `conflict`: action-array, object, zone, seat, or annotation evidence
  disagrees.
- `legacy_enriched`: display/catalog/deck-name context retained or enriched
  outside current direct log evidence.

## Confidence Policy

The `gameplay_action` entry must use this policy:

```yaml
confidence_policy:
  direct: "high"
  fallback: "medium"
  inferred: "low"
  unavailable: "unknown"
  contradiction: "low"
```

Required confidence boundaries:

- High confidence is allowed only when direct GameState action/context evidence
  supports the normalized action and no known conflict is present.
- Medium confidence is appropriate for zone-transition-derived actions,
  actor/zone context derived from observed state, and action details that depend
  on multiple observed inputs.
- Low confidence is required for partial-diff inference, display-only
  enrichment, missing seat mapping, missing zones, missing card identity, or
  conflicting evidence.
- Unknown confidence is required when a facet cannot be safely supported.

## Finality Policy

The `gameplay_action` entry must use this policy:

```yaml
finality_policy:
  live: "live"
  provisional: "provisional"
  final: "final"
  reconciled: "reconciled"
```

Current gameplay-action artifacts are live/runtime action observations. This
contract does not require row-level final evidence attachment or final
reconciliation behavior. A future contract must explicitly define any field-level
final/reconciled attachment before action provenance can be treated as final
row evidence.

## Invariant Checks

The `gameplay_action` ledger entry must include invariant names that prove:

- `tier5_seeds_exactly_grp_id_and_gameplay_action`
- `opponent_card_observation_remains_future_field`
- `gameplay_action_is_single_seed_with_facets_not_many_seed_fields`
- `gameplay_action_action_type_is_parser_owned_classification`
- `gameplay_action_raw_action_types_preserve_observed_labels_when_available`
- `gameplay_action_actor_relation_depends_on_seat_mapping`
- `gameplay_action_zone_context_distinguishes_observed_state_from_inference`
- `gameplay_action_card_identity_depends_on_tier5_grp_id`
- `gameplay_action_display_fields_are_enrichment_only`
- `gameplay_action_does_not_infer_hidden_cards_or_complete_decklists`
- `gameplay_action_does_not_prove_player_mistakes_or_strategy`
- `gameplay_action_workbook_webhook_apps_script_analytics_and_ai_are_not_source_truth`
- `gameplay_action_privacy_path_only_no_values`

Codex C may choose equivalent stable invariant names if the tests prove the
same guarantees.

## Degradation Behavior

The entry must document degradation for:

- missing `GameState` payloads;
- missing event timestamp;
- missing match or game association;
- missing turn data;
- missing raw action-array labels;
- missing prior/current object state;
- missing zone maps or zone IDs;
- missing seat mapping;
- missing or conflicting local/opponent actor relation;
- missing `grp_id` or conflicting card identity hints;
- action-array evidence that disagrees with zone-diff evidence;
- annotation-only or partial-diff-only action evidence;
- catalog/display enrichment being unavailable;
- opponent-card-observation dependency being deferred.

Expected degradation behavior is explicit uncertainty, lower confidence, omitted
action evidence when unsafe, or path-only review context. The ledger must not
fill missing action truth with workbook formulas, Apps Script, AI, archetype
labels, strategy assumptions, or hidden-card guesses.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- GameState parsing;
- gameplay-action extraction or classification;
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
- runtime action artifact shape;
- runtime status file content or locations;
- failed posts;
- workbook exports;
- production deployment behavior;
- CI gates;
- Pyright gate behavior;
- OpenAI or model-provider behavior;
- analytics truth;
- AI truth;
- secrets, credentials, environment variables, webhook URLs, or API keys;
- raw private `Player.log` excerpts;
- generated card data;
- local-only artifacts.

Protected-surface warnings from tooling are review signals, not authorization.

## Out Of Scope

Do not implement or authorize:

- gameplay action extraction changes;
- new action kinds;
- new parser event kinds;
- new workbook columns;
- new webhook fields;
- Apps Script changes;
- schema snapshot updates;
- golden fixture updates;
- drift baseline updates;
- opponent-card-observation seeding;
- card-performance analytics;
- Line Tracer behavior;
- coaching evaluation;
- player-mistake labels;
- strategic or sideboard advice;
- archetype classification;
- hidden-card inference;
- complete decklist inference;
- model-provider integration;
- production deployment.

## Unknowns

- Whether every existing action type has enough current GameState evidence to
  deserve the same confidence label.
- Whether `turn_started` should eventually receive a narrower sub-entry or stay
  as a facet of broad gameplay action.
- Whether future field-level finality should attach action evidence to rows,
  runtime action reports, or a separate ledger report.
- Whether schema snapshots should later assert stable runtime action report
  fields. This contract does not authorize snapshot updates.
- Whether future opponent-card-observation provenance should mirror the
  gameplay-action entry or remain independent. That remains deferred.

## Suspected Gaps

- Tier 5 currently treats `gameplay_action` as a future field even though
  gameplay-action runtime code and focused tests already exist.
- The current ledger has a `grp_id` entry that mentions gameplay-action surfaces,
  but no separate entry describes action provenance as a first-class field.
- Tests currently forbid `gameplay_action` as a seed field, which is correct for
  issue #163 but must change for issue #165.
- The current ledger does not yet express the confidence boundary between direct
  action-array evidence, zone-transition-derived evidence, partial-diff
  inference, display enrichment, and downstream opponent-card observations.
- The current ledger does not yet state that gameplay-action provenance must not
  become analytics, coaching, mistake-label, or hidden-card truth.

## Validation Requirements For Codex C

Required focused validation:

```powershell
py -m pytest -q tests\test_evidence_ledger.py
py -m ruff check src tests tools
git diff --check
```

Required adjacent validation if implementation references or edits adjacent
tests, notes, or source surfaces:

```powershell
py -m pytest -q tests\test_gameplay_actions.py tests\test_opponent_card_observations.py
```

Required protected-surface check for the expected changed-file set:

```powershell
@'
docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md
src/mythic_edge_parser/app/evidence_ledger.py
tests/test_evidence_ledger.py
docs/implementation_handoffs/player_log_evidence_ledger_tier5_gameplay_action_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
```

Codex C must clearly state if broader tests are not run and why.

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md` exists.
- Codex C compares current code/tests against this contract before editing.
- Tier 5 `seed_fields` becomes exactly `["grp_id", "gameplay_action"]`.
- Tier 5 `future_fields` becomes exactly `["opponent_card_observation"]`.
- A validating entry exists for `tier5.gameplay_action.gameplay_action`.
- The new entry validates under the existing ledger schema.
- The new entry documents direct GameState evidence, fallback/derived action
  evidence, value-source policy, confidence policy, finality policy, invariant
  checks, degradation behavior, privacy posture, and protected non-truth
  boundaries.
- Focused tests prove `gameplay_action` is the only newly seeded Tier 5 field.
- Focused tests prove no separate seed fields are added for action facets,
  display fields, analytics, AI, or opponent-card observation.
- No parser behavior, gameplay-action classification, workbook schema, webhook
  payload, Apps Script behavior, runtime artifact shape, raw logs, secrets,
  generated data, failed posts, workbook exports, or production behavior change.
- Tracker #11 remains open.
- The work does not target `main` directly.

## Codex C Handoff Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #165.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/165

Base branch:
codex/parser-reliability-intelligence

Contract:
docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md

Expected implementation handoff:
docs/implementation_handoffs/player_log_evidence_ledger_tier5_gameplay_action_comparison.md

Goal:
Compare the current evidence-ledger code and tests against the Tier 5 gameplay-action contract, then implement only the metadata and focused tests needed to seed `gameplay_action` as a first-class Tier 5 evidence-ledger field. Preserve `grp_id` provenance and keep `opponent_card_observation` deferred.

Before editing:
- Confirm the branch is `codex/parser-reliability-intelligence`.
- Inspect `git status --short --branch`.
- State what gameplay-action provenance is supposed to do, what current code/tests already do, what gaps remain, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md
- docs/contracts/parser_opponent_card_observations.md
- src/mythic_edge_parser/app/evidence_ledger.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- tests/test_evidence_ledger.py
- tests/test_gameplay_actions.py
- tests/test_opponent_card_observations.py

Do:
- Change only evidence-ledger metadata and focused ledger tests unless comparison proves a docs-only note is needed.
- Keep Tier 5 status `seeded_sample`.
- Set Tier 5 seed fields to exactly `["grp_id", "gameplay_action"]`.
- Set Tier 5 future fields to exactly `["opponent_card_observation"]`.
- Add one ledger entry: `tier5.gameplay_action.gameplay_action`.
- Document direct GameState evidence, fallback zone/partial-diff/annotation evidence, `grp_id` dependency, display-enrichment boundary, value-source policy, confidence policy, finality policy, invariants, degradation behavior, and path-only privacy posture.
- Add focused tests proving no separate Tier 5 seed fields are added for action facets, display labels, opponent-card observation, analytics, coaching, AI, hidden-card inference, or strategy.
- Produce `docs/implementation_handoffs/player_log_evidence_ledger_tier5_gameplay_action_comparison.md`.

Do not:
- Change gameplay-action extraction/classification behavior.
- Change opponent-card-observation behavior.
- Change parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime action artifact shape, runtime status files, failed posts, workbook exports, CI gates, Pyright gates, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, secrets, credentials, environment variables, raw logs, generated data, schema snapshots, golden fixtures, or drift baselines.
- Add opponent-card-observation as a seed field.
- Target main directly.
- Close tracker #11.
- Stage, commit, push, open a PR, or merge unless explicitly asked.

Validation:
py -m pytest -q tests\test_evidence_ledger.py
py -m ruff check src tests tools
git diff --check

If adjacent behavior surfaces are referenced or touched, also run:
py -m pytest -q tests\test_gameplay_actions.py tests\test_opponent_card_observations.py

Run the path-scoped protected-surface check for changed files:
@'
docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md
src/mythic_edge_parser/app/evidence_ledger.py
tests/test_evidence_ledger.py
docs/implementation_handoffs/player_log_evidence_ledger_tier5_gameplay_action_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin

Final handoff must include:
- role performed
- issue/tracker used
- source artifacts inspected
- comparison summary
- files changed
- exact function/test sections changed
- validation run
- protected surfaces status
- remaining unverified layers
- next recommended role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/165"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier5_gameplay_action_comparison.md"
  verdict: "contract_complete_ready_for_metadata_implementation"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  authorized_seed_fields:
    - "grp_id"
    - "gameplay_action"
  authorized_future_fields:
    - "opponent_card_observation"
  authorized_seed_entries:
    - "tier5.gameplay_action.gameplay_action"
  validation:
    - "py -m pytest -q tests\\test_evidence_ledger.py"
    - "py -m ruff check src tests tools"
    - "git diff --check"
    - "py -m pytest -q tests\\test_gameplay_actions.py tests\\test_opponent_card_observations.py if adjacent behavior surfaces are referenced or touched"
    - "path-scoped protected-surface check for the changed-file set"
  stop_conditions:
    - "Do not change gameplay-action extraction or classification behavior."
    - "Do not seed opponent_card_observation in issue #165."
    - "Do not add separate Tier 5 seed fields for gameplay-action facets."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime artifact shape, runtime status files, failed posts, workbook exports, CI gates, production behavior, analytics truth, AI truth, model-provider behavior, secrets, raw logs, generated data, schema snapshots, golden fixtures, or drift baselines."
    - "Do not target main directly."
    - "Do not close tracker #11."
```
