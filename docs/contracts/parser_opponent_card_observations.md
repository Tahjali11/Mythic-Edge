# Parser Opponent Card Observations Contract

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/50

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Codex A problem representation:
https://github.com/Tahjali11/Mythic-Edge/issues/50#issuecomment-4475315520

Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/48

Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/111

Previous merge commit: `76b63622494b0bbc6150e6bd19973b4ac8e0be0c`

Branch target: `codex/parser-reliability-intelligence`

This contract defines deterministic parser-supported opponent-card
observation facts. It is a contract artifact only. It does not implement code,
change parser behavior, add workbook or webhook output, change runtime status
file shape, infer hidden cards, classify archetypes, complete decklists, call
model providers, or commit raw private `Player.log` excerpts.

## Module

Parser opponent card observations.

Plain English: this module records what the parser can support about
opponent-visible cards and actions. It should produce evidence-bound facts
such as "the opponent cast this observed card from hand to stack on turn 4."
It must not produce guesses such as "the opponent is on Dimir Midrange" or
"the opponent likely has four copies of this card."

Risk tier: High.

The implementation surface is parser-adjacent and local, but the truth-boundary
risk is high. Opponent observations sit directly between raw `GameState`
evidence and later analytics. A weak contract could turn hidden information,
catalog guesses, archetype labels, partial decklists, or incomplete/truncated
evidence into parser truth.

## Owning Layer

Owning layer: parser-adjacent gameplay observation / parser intelligence
facts.

Truth boundary:

- MTGA `Player.log` is local observable evidence, not absolute game truth.
- GRE `GameState` payloads, action arrays, annotations, zones, game objects,
  seat mapping, and parser state context are the only acceptable evidence
  families for v1 observations.
- Parser and state layers continue to own match identity, game identity,
  final reconciliation, seat/team context, and event interpretation.
- This observation layer may record deterministic facts that those parser
  layers already support.
- This observation layer must not infer hidden cards, complete opponent
  decklists, classify archetypes, call OpenAI or other model providers, or
  move parser truth into workbook formulas, dashboard logic, webhook
  transport, Apps Script, AI output, or analytics surfaces.
- Card-name resolution is enrichment. Observed IDs, source evidence, and
  resolution status must remain available when names are uncertain.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_opponent_card_observations.md`

Future implementation artifacts owned by this contract, if authorized by the
Codex C implementation pass:

- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `tests/test_opponent_card_observations.py`
- `docs/implementation_handoffs/parser_opponent_card_observations_comparison.md`

Narrow integration surfaces allowed only when needed to satisfy this contract:

- `src/mythic_edge_parser/app/gameplay_actions.py`
- `tests/test_gameplay_actions.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `tests/test_golden_replay_harness.py`
- optional sanitized or synthetic golden replay fixture and manifest files
  under `tests/fixtures/golden_replay/`

Related files referenced but not silently owned:

- `src/mythic_edge_parser/app/grp_id_catalog.py`
- `src/mythic_edge_parser/app/card_performance.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/parser_gre_turn_info.md`
- `docs/contracts/parser_extractors.md`
- `docs/problem_representations/parser_feature_equity_with_manasight.md`

## Public Interface

V1 should prefer a small helper module consumed by tests and, if necessary, by
`gameplay_actions.py`. It should not add workbook columns, webhook fields,
Apps Script behavior, runtime status schema, or AI-facing truth.

Exact Python names may vary during implementation, but the public behavior
must preserve this shape:

```python
OPPONENT_CARD_OBSERVATION_OBJECT = "mythic_edge_opponent_card_observation"
OPPONENT_CARD_OBSERVATIONS_OBJECT = "mythic_edge_opponent_card_observations"
SCHEMA_VERSION = "parser_opponent_card_observations.v1"

def build_opponent_card_observation(
    action_entry: Mapping[str, Any],
) -> dict[str, Any] | None:
    ...

def build_opponent_card_observations_payload(
    action_entries: Iterable[Mapping[str, Any]],
    *,
    match_id: str = "",
) -> dict[str, Any]:
    ...
```

Required interface behavior:

- Return `None` for entries that are not supported opponent-visible card
  observations.
- Return JSON-serializable dictionaries.
- Avoid filesystem writes in v1.
- Preserve input entries without mutation.
- Avoid importing workbook, webhook, Apps Script, OpenAI, or model-provider
  surfaces.
- Treat malformed optional input as unknown/degraded instead of raising, unless
  a caller passes a non-mapping object where the focused tests explicitly
  expect neutral output.

## Observed Current Behavior

Observed on `codex/parser-reliability-intelligence` after PR #111:

- Issue #50 is open and belongs to tracker #47.
- Tracker #47 is open.
- PR #111 is merged into `codex/parser-reliability-intelligence` at
  `76b63622494b0bbc6150e6bd19973b4ac8e0be0c`.
- `gameplay_actions.py` observes `GameState` events only.
- `gameplay_actions.py` consumes normalized and fallback extractor surfaces
  for `identity`, `system_seat_ids`, `zones`, `game_objects`, `annotations`,
  and `actions`.
- `gameplay_actions.py` currently derives `actor_relation` as `local`,
  `opponent`, or `unknown` by comparing local seat ID with object
  controller/owner seat ID.
- `gameplay_actions.py` writes runtime action JSON and Markdown artifacts with
  action entries, rendered display names, `resolution_status`,
  `visible_in_log`, and summaries.
- Current action entries include useful raw material: match ID, game number,
  game-state ID, timestamp, turn number, action type, cast mode, instance ID,
  canonical and observed GRP IDs, source/object IDs, parent ID, actor
  relation, zone transition, raw action types, and annotation types.
- `grp_id_catalog.py` enriches GRP IDs with display names and resolution
  status. It also records gameplay observations, but the catalog is generated
  enrichment and must not become parser truth for card identity.
- `card_performance.py` intentionally filters action entries to blank/local
  actor relation before aggregating card-performance metrics.
- Current gameplay-action tests cover many local action and cleanup cases, and
  some opponent-owned objects appear in test fixtures, but there are no focused
  tests proving a durable opponent-card-observation payload.
- Current golden replay manifests cover parser health, match/game/result facts,
  diagnostics, truncation/data-loss status, parser state, final
  reconciliation, and selected parser-owned rows. They do not yet cover
  opponent-visible card observations.
- The evidence ledger registers card identity and gameplay actions as Tier 5
  future fields and states that card names are resolved enrichment, instance
  IDs are game-local, and observed IDs must be preserved when name resolution
  is uncertain.

## Inputs

Primary input:

- Rendered or raw gameplay action entry dictionaries produced from
  `gameplay_actions.py`.

Allowed supporting evidence sources:

- `GameStateEvent.payload.identity`
- `GameStateEvent.payload.system_seat_ids`
- `GameStateEvent.payload.game_state_id` or `msg_id`
- `GameStateEvent.payload.turn_number`
- `GameStateEvent.payload.zones`
- `GameStateEvent.payload.game_objects`
- `GameStateEvent.payload.actions`
- `GameStateEvent.payload.annotations`
- preserved raw `GameState` subpayloads only through existing extractor
  fallback behavior
- parser context for current match/game identity only where existing parser
  layers already use that context
- `grp_id_catalog.py` lookup entries for name enrichment only

Forbidden evidence sources:

- opponent archetype labels
- opponent variant labels
- manually assigned matchup labels
- inferred or completed opponent decklists
- hidden opponent hand/library/deck contents
- workbook formulas
- dashboard calculations
- Apps Script behavior
- webhook delivery state
- AI or model-provider output
- generated card-performance metrics
- raw private logs outside committed sanitized fixtures

## Output Payload Shape

### Observation Payload

Required logical shape:

```yaml
object: "mythic_edge_opponent_card_observation"
schema_version: "parser_opponent_card_observations.v1"
match_id: "match-id"
game_number: 1
game_state_id: 123
timestamp: "2026-05-18T00:00:00+00:00"
turn_number: 4
actor_relation: "opponent"
actor_seat_id: 2
local_seat_id: 1
instance_id: 456
grp_id: 789
observed_grp_id: 789
overlay_grp_id: null
object_source_grp_id: null
parent_id: null
identity_hint_source: "direct_grp_id"
card_name: "Resolved Name"
display_name: "Resolved Name"
resolution_status: "resolved"
name_resolution_source: "grp_id_catalog"
layout: ""
card_faces: []
action_type: "spell_cast"
cast_mode: ""
source_evidence: "action_array"
evidence_status: "observed"
value_source: "observed"
confidence: "high"
visibility: "action_visible"
from_zone_type: "ZoneType_Hand"
to_zone_type: "ZoneType_Stack"
raw_action_types: []
annotation_types: []
annotation_categories: []
degradation_flags: []
review_required: false
```

Required fields:

- `object`
- `schema_version`
- `match_id`
- `game_number`
- `game_state_id`
- `timestamp`
- `turn_number`
- `actor_relation`
- `actor_seat_id`
- `local_seat_id`
- `instance_id`
- `grp_id`
- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `parent_id`
- `identity_hint_source`
- `card_name`
- `display_name`
- `resolution_status`
- `name_resolution_source`
- `layout`
- `card_faces`
- `action_type`
- `cast_mode`
- `source_evidence`
- `evidence_status`
- `value_source`
- `confidence`
- `visibility`
- `from_zone_type`
- `to_zone_type`
- `raw_action_types`
- `annotation_types`
- `annotation_categories`
- `degradation_flags`
- `review_required`

### Collection Payload

Required logical shape:

```yaml
object: "mythic_edge_opponent_card_observations"
schema_version: "parser_opponent_card_observations.v1"
match_id: "match-id"
total_observations: 1
degraded_observations: 0
review_required: false
observations:
  - opponent_card_observation
```

The collection payload is a local parser-intelligence artifact shape. V1 must
not expose it through workbook schema, webhook payloads, Apps Script, or
runtime status file schema.

## Allowed Values

### `actor_relation`

Allowed values:

- `opponent`

V1 opponent-card observations must not emit `local` or `unknown` rows. Entries
with `local` or `unknown` actor relation may remain in existing gameplay-action
logs, but they are not opponent-card observations.

### `action_type`

Allowed v1 values:

- `spell_cast`
- `land_played`
- `put_onto_battlefield_from_hand`
- `permanent_resolved`
- `permanent_left_battlefield`
- `permanent_died`
- `card_discarded`
- `spell_resolved_to_graveyard`
- `card_exiled`
- `zone_change`
- `object_revealed`
- `public_zone_presence`
- `unknown`

Opponent `card_drawn` from library to hand must not become a clean
card-identity observation unless the same entry also has explicit reveal or
public-zone evidence. Hidden draws may produce no observation, or a degraded
review note in a diagnostics/golden replay context, but not a clean observed
card fact.

### `source_evidence`

Allowed values:

- `action_array`
- `annotation`
- `zone_transition`
- `object_presence_public_zone`
- `gameplay_action_entry`
- `mixed`
- `unknown`

`action_array` is strongest when a direct `actions` entry names a seat,
action type, and instance ID. `zone_transition` is allowed only when derived
from consecutive parser-observed `GameState` payloads and must not imply hidden
information.

### `evidence_status` And `value_source`

Allowed `evidence_status` values:

- `observed`
- `derived`
- `inferred`
- `unknown`
- `conflict`
- `degraded`

Allowed `value_source` values, aligned with the evidence ledger:

- `observed`
- `derived`
- `inferred`
- `unknown`
- `conflict`

Use `evidence_status=degraded` with `value_source=unknown`, `derived`, or
`inferred` when the observation is incomplete but still useful for review.
Do not invent a ledger `value_source=degraded`.

Status guidance:

- `observed`: direct action, annotation, or public-zone evidence supports the
  card/action fact.
- `derived`: a stable parser state transition supports the fact without
  guessing hidden information.
- `inferred`: indirect evidence suggests the fact, but it is not strong enough
  for high-confidence clean analytics.
- `unknown`: required evidence is missing.
- `conflict`: seat, identity, zone, or card evidence disagrees.
- `degraded`: data-loss, truncation, missing identity, missing seat mapping, or
  weak evidence prevents clean observation.

### `confidence`

Allowed values:

- `high`
- `medium`
- `low`
- `unknown`

High confidence requires known opponent actor relation, visible evidence, and
stable card identity or an explicit unknown-card observation that does not
claim a name. Candidate names, ambiguous names, hidden-zone cleanup, or missing
seat mapping cannot be high confidence.

### `visibility`

Allowed values:

- `action_visible`
- `public_zone`
- `revealed`
- `derived_zone_transition`
- `ambiguous`
- `hidden_not_recorded`

`hidden_not_recorded` is a reason not to emit a clean observation. If an
implementation reports it, it must be a degradation/review artifact, not a
parser-owned observed card fact.

### `resolution_status`

Allowed normalized values:

- `resolved`
- `confirmed`
- `candidate`
- `unresolved`
- `contradicted`
- `ambiguous`
- `name_only`

Current `grp_id_catalog.py` statuses such as `confirmed`, `candidate`,
`unresolved`, and `contradicted` may be preserved. If implementation maps
catalog-specific statuses to normalized observation statuses, it must preserve
the source status in `name_resolution_source` or another explicit field.

## Required Guarantees

### Actor Relation And Seat Mapping

- An opponent observation requires a known local seat ID.
- An opponent observation requires a known actor seat ID.
- The actor seat ID must be different from the local seat ID.
- Actor seat should prefer controller seat when available, then owner seat.
- Direct action-array seat evidence may strengthen actor mapping but must not
  override contradictory controller/owner evidence silently.
- Missing local seat, missing actor seat, malformed seat IDs, or contradictory
  seat evidence must produce no clean opponent observation.
- If contradictory actor evidence is reported, use `evidence_status=conflict`,
  `confidence=low`, a degradation flag, and `review_required=true`.

### Visibility And Hidden Information

Allowed clean observations must be tied to at least one of:

- a visible action by an opponent;
- a public-zone object presence;
- an explicit reveal annotation or action;
- a stable zone transition into or out of a public/revealed/action-visible
  state.

Forbidden as clean observations:

- cards only present in opponent private hand zones;
- cards only present in opponent library zones;
- cards only present in hidden opponent deck contents;
- inferred copies, likely sideboard cards, likely archetype staples, or cards
  not represented in parser evidence;
- `card_drawn` identity from library to hand without explicit reveal/public
  evidence;
- cleanup of revealed-card shadow objects when existing gameplay-action
  behavior correctly suppresses them.

### Card Identity And Name Resolution

- `instance_id` is game-local and must not be treated as durable historical
  card identity.
- `grp_id`, `observed_grp_id`, `overlay_grp_id`, `object_source_grp_id`, and
  `parent_id` must be preserved when present.
- Canonical `grp_id` may be derived from object source, parent chain, prior
  instance, replacement chain, direct GRP ID, or overlay GRP ID only when the
  source is recorded in `identity_hint_source`.
- If canonical identity differs from observed identity, both values must
  remain visible.
- `card_name` and `display_name` are enrichment from `grp_id_catalog.py` or
  other parser-owned local card lookup surfaces. They are not raw Player.log
  truth.
- Candidate or ambiguous names must not be treated as clean resolved names.
- Missing or unresolved names must not block an observation when ID/action
  evidence is otherwise sufficient; instead preserve IDs, use placeholder
  display text, and mark the resolution status.
- A name-only observation without observed IDs is low confidence and must
  preserve `resolution_status=name_only`.

### Truncation And Data-Loss Behavior

- GSM truncation/data-loss evidence must never produce clean opponent-card
  confidence.
- If a relevant `GameState` message is truncated, summarized, missing object
  arrays, missing action arrays, or missing annotation arrays, affected
  observations must be absent or marked degraded/review-required.
- Golden replay and diagnostics should report missing expected opponent
  observations as `diff` or `review`, not `pass`.
- Do not reconstruct missing game objects, hidden cards, actions, annotations,
  or zone transitions after truncation.

## Relationships To Existing Modules

### `gameplay_actions.py`

`gameplay_actions.py` is the closest current implementation surface. It owns
runtime gameplay action detection and local action logs. The opponent
observation helper should consume its action-entry shape or be called from a
narrow hook inside it.

Required boundary:

- Do not change existing gameplay action entry fields unless Codex C proves the
  change is contract-required and focused tests cover compatibility.
- Do not change runtime action JSON/Markdown shape in v1 unless a follow-up
  contract explicitly authorizes runtime artifact changes.
- Existing local gameplay-action behavior must remain compatible.

### `grp_id_catalog.py`

`grp_id_catalog.py` may enrich observations with display names, resolution
status, layout, and card faces. It must not become the source of observed card
truth.

Required boundary:

- Observed IDs and evidence status must remain even when catalog lookup fails.
- Catalog candidate names are lower-confidence enrichment.
- Generated catalog files remain generated/local artifacts and must not be
  committed as part of this contract.

### `card_performance.py`

`card_performance.py` currently filters gameplay action entries to blank/local
actor relation before aggregating card metrics. This must remain true in v1.

Required boundary:

- Do not make card-performance aggregation include opponent cards.
- Opponent observation facts may support future analytics, but that future
  analytics layer needs its own contract.
- If any action-entry shape changes, run card-performance tests and preserve
  local-only aggregation behavior.

### Diagnostics Mode

Diagnostics mode may later summarize whether opponent-observation evidence is
available, degraded, missing, or blocked by truncation. It must not become the
truth source for observations.

V1 implementation should avoid diagnostics report schema changes unless Codex
C explicitly identifies a contract-required reason and adds focused tests.

### Golden Replay Harness

Golden replay is the preferred protection for this module after focused unit
tests exist.

Allowed v1 strategy:

- Add a sanitized or synthetic fixture with an opponent-visible card sequence.
- Add an optional `opponent_card_observations` expected section to golden
  replay manifests.
- Keep that section optional so existing #48 manifests remain compatible.
- Compare reduced observation facts rather than broad runtime action logs.

Forbidden golden replay behavior:

- no raw private logs;
- no hidden-card or archetype guesses in expected output;
- no expected-output updates without issue, contract, and review;
- no use of replay output as parser truth.

### Evidence Ledger

This module implements part of the evidence-ledger Tier 5 future surface:
card identity and gameplay actions.

Required alignment:

- Use the ledger's value-source and confidence vocabulary.
- Treat card names as enrichment.
- Treat instance IDs as game-local.
- Preserve observed IDs when name resolution is uncertain.
- Mark missing or conflicting evidence as unknown, conflict, degraded, or
  review-required rather than silently accepting a guess.

## Fixture And Golden Replay Strategy

Future implementation should start with focused unit tests, then add one
minimal golden replay fixture if the parser path can exercise the same
behavior without raw private logs.

Recommended fixture coverage:

- opponent casts a visible spell from hand to stack;
- opponent plays a visible land from hand to battlefield;
- opponent discards or reveals a card with explicit public/reveal evidence;
- missing seat mapping produces no clean opponent observation;
- unresolved GRP ID preserves IDs and marks name resolution as unresolved;
- candidate/contradicted catalog name remains lower confidence;
- hidden opponent hand/library movement does not create a clean observation;
- truncation or missing arrays creates degraded/review evidence rather than a
  clean pass.

Golden replay expectations should prefer reduced facts:

- `match_id`
- `game_number`
- `game_state_id`
- `turn_number`
- `actor_relation`
- `actor_seat_id`
- `instance_id`
- `grp_id`
- `observed_grp_id`
- `identity_hint_source`
- `action_type`
- `source_evidence`
- `evidence_status`
- `confidence`
- `visibility`
- `resolution_status`
- `degradation_flags`

Golden replay should not snapshot full raw `GameState` payloads, full runtime
action artifacts, workbook rows, analytics labels, or card-performance output
for this module.

## Invariants

- Every emitted v1 observation has `actor_relation="opponent"`.
- Every clean opponent observation has known local seat and known actor seat.
- No clean observation is emitted for hidden opponent cards.
- No observation claims an archetype, matchup label, decklist, sideboard plan,
  or likely card copy count.
- `display_name` and `card_name` never replace observed ID evidence.
- `instance_id` is game-local.
- `grp_id` provenance is visible through `identity_hint_source` and preserved
  observed ID fields.
- Truncated or incomplete `GameState` evidence cannot produce high-confidence
  clean observations.
- Card-performance aggregation remains local-only in v1.
- Workbook schema, webhook payload shape, Apps Script behavior, output
  transport, parser event classes, match/game identity, deduplication, final
  reconciliation, secrets, environment variables, runtime status file schema,
  failed posts, generated data, raw logs, and workbook exports remain
  unchanged.

## Error Behavior

Malformed action entry:

- return `None` or a degraded observation only when enough fields remain to
  preserve source uncertainty;
- do not raise for missing optional fields;
- do not guess actor relation or card identity.

Missing seat mapping:

- emit no clean opponent observation;
- if reported, use `missing_seat_mapping` degradation and
  `review_required=true`.

Missing card identity:

- preserve action and context if visible;
- leave ID/name fields empty or neutral;
- use `resolution_status=unresolved`, `confidence=low` or `unknown`, and a
  degradation flag.

Contradictory identity or actor evidence:

- use `evidence_status=conflict`;
- use `confidence=low`;
- include a specific degradation flag;
- require review.

Hidden-zone evidence:

- do not emit a clean observation;
- do not preserve hidden card names as observed facts;
- do not infer hidden opponent cards from later public objects unless the
  public evidence itself supports the observation.

Truncation/data loss:

- mark affected observation coverage degraded/review-required;
- do not reconstruct missing payload sections.

## Side Effects

Allowed side effect in this Codex B thread:

- create `docs/contracts/parser_opponent_card_observations.md`.

Allowed future v1 implementation side effects:

- add pure helper code;
- add focused tests;
- add sanitized or synthetic committed golden replay fixture/manifest coverage
  if needed;
- extend golden replay comparison with an optional expected observation section.

Forbidden future v1 side effects without a new contract:

- no workbook schema changes;
- no webhook payload shape changes;
- no Apps Script behavior changes;
- no output transport changes;
- no parser state final reconciliation changes;
- no parser event class changes;
- no match/game identity changes;
- no deduplication changes;
- no runtime status file schema changes;
- no new generated data commitments;
- no failed-post changes;
- no workbook export changes;
- no raw private log commitments;
- no OpenAI or model-provider calls.

## Dependency Order

Future implementation should proceed in this order:

1. Add `opponent_card_observations.py` as a pure helper module.
2. Add `tests/test_opponent_card_observations.py` for payload shape, actor
   relation, visibility, name resolution, hidden information, degradation, and
   malformed input behavior.
3. Add only the narrow `gameplay_actions.py` integration needed to consume or
   expose existing action entries, without changing runtime artifact shape.
4. Add focused compatibility tests in `tests/test_gameplay_actions.py`.
5. Add golden replay optional-section support and sanitized/synthetic fixture
   coverage only after focused tests pass.
6. Run `card_performance.py` tests if action-entry shape or actor-relation
   behavior is touched.
7. Route to Codex E for contract-test review.

Route back to Codex B if implementation requires runtime status schema
changes, workbook/webhook exposure, event class changes, archetype/decklist
output, hidden-card inference, or diagnostics schema changes beyond a narrow
review summary.

## Compatibility

- Existing `gameplay_actions.py` runtime action JSON and Markdown artifacts
  remain compatible.
- Existing `card_performance.py` local-only action aggregation remains
  compatible.
- Existing golden replay manifests remain compatible because opponent
  observation expectations are optional.
- Existing diagnostics report shape remains compatible unless a later contract
  authorizes an explicit diagnostics schema expansion.
- Existing `grp_id_catalog.py` generated catalog behavior remains enrichment
  only.
- Existing workbook rows, webhook payloads, Apps Script receiver behavior, and
  parser event classes remain unchanged.

## Unknowns

- Whether v1 should be a pure helper only or include a narrow
  `gameplay_actions.py` hook.
- Whether golden replay should compare observations directly from the helper or
  from gameplay-action entries emitted during replay.
- Whether future annotation normalization should add stronger
  `source_evidence=annotation` guarantees before broader opponent observation
  coverage.
- Whether diagnostics mode should eventually report opponent-observation
  coverage counts.
- Whether a future analytics contract should consume opponent observations for
  archetype hypotheses.

## Suspected Gaps

- No dedicated opponent-card observation module exists.
- Focused opponent-observation tests do not exist.
- Current gameplay-action tests are strong for local actions but do not freeze
  a public opponent-observation payload.
- Current golden replay manifests do not cover opponent-visible card facts.
- Current evidence-ledger implementation is not machine-readable, so v1 must
  align with the ledger vocabulary without pretending field-level ledger
  metadata already exists.
- Current card-performance metrics do not expose ingredient confidence and
  should remain local-only.

## Validation Requirements

Contract-writer validation for this docs-only pass:

```bash
git diff --check
```

Future focused implementation validation:

```bash
python3 -m pytest -q tests/test_opponent_card_observations.py
python3 -m pytest -q tests/test_gameplay_actions.py tests/test_card_performance.py tests/test_grp_id_catalog.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_protected_surfaces.py --base origin/main
```

If golden replay fixture coverage is added:

```bash
python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_parser_regressions.py
python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
```

If diagnostics mode is touched:

```bash
python3 -m pytest -q tests/test_parser_diagnostics_mode.py
```

If a secret/private-marker scanner exists in the active branch, run it before
submitter work against new committed fixture and manifest paths.

## Acceptance Criteria

- `docs/contracts/parser_opponent_card_observations.md` exists.
- The contract links issue #50, tracker #47, related issue #11, the Codex A
  problem representation, previous issue #48, PR #111, and the parser
  reliability branch.
- The contract marks risk tier High.
- The contract names parser-adjacent gameplay observation / parser
  intelligence facts as the owning layer.
- The contract preserves parser/state truth ownership.
- The contract defines observation payload shape.
- The contract defines allowed evidence sources and forbidden sources.
- The contract defines actor relation and seat-mapping requirements.
- The contract defines visibility and hidden-information rules.
- The contract defines card identity and name-resolution rules.
- The contract defines observed/derived/inferred/degraded/conflict/unknown
  vocabulary and aligns value-source/confidence with the evidence ledger.
- The contract defines truncation/data-loss behavior.
- The contract defines relationships to `gameplay_actions.py`,
  `grp_id_catalog.py`, `card_performance.py`, diagnostics mode, golden replay,
  and the evidence ledger.
- The contract defines fixture and golden replay strategy.
- The contract names validation commands for future implementation and review.
- The contract names protected surfaces and stop conditions.
- The contract does not implement code, target `main`, close tracker #47,
  close issue #11, change protected surfaces, infer hidden cards, classify
  archetypes, call model providers, copy Manasight source, or commit raw
  private `Player.log` excerpts.

## Next Workflow Action

Next role: Codex C, Module Implementer.

Pasteable prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #50 and docs/contracts/parser_opponent_card_observations.md.

  Goal:
  Implement the smallest coherent deterministic opponent-card observation helper needed to satisfy the contract. The module should record parser-supported observations about opponent-visible cards and actions while keeping archetype, decklist, and hidden-information inference out of parser truth.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/50
    - Related evidence/resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
    - Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/48
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/111
    - Previous merge commit: 76b63622494b0bbc6150e6bd19973b4ac8e0be0c
    - Branch/base: codex/parser-reliability-intelligence

  Use:
    - AGENTS.md
    - docs/agent_constitution.md
    - docs/agent_rules.yml
    - docs/codex_module_workflow.md
    - docs/agent_threads/implementation.md
    - docs/contracts/parser_opponent_card_observations.md
    - docs/contracts/player_log_evidence_ledger.md
    - docs/contracts/parser_golden_replay_harness.md
    - docs/contracts/parser_diagnostics_mode.md
    - docs/contracts/parser_gre_game_state.md
    - docs/contracts/parser_gre_turn_info.md
    - docs/contracts/parser_extractors.md
    - src/mythic_edge_parser/app/gameplay_actions.py
    - src/mythic_edge_parser/app/grp_id_catalog.py
    - src/mythic_edge_parser/app/card_performance.py
    - src/mythic_edge_parser/app/golden_replay.py
    - src/mythic_edge_parser/app/parser_diagnostics.py
    - tests/test_gameplay_actions.py
    - tests/test_card_performance.py
    - tests/test_grp_id_catalog.py
    - tests/test_golden_replay_harness.py

  Do:
    - Compare current gameplay action, catalog, card-performance, diagnostics, and golden replay behavior against the contract before editing.
    - Add a pure opponent-card observation helper and focused tests first.
    - Preserve existing gameplay action payload compatibility unless the contract-required narrow integration is unavoidable.
    - Preserve card-performance local-only aggregation.
    - Add sanitized or synthetic golden replay coverage only if needed and keep opponent observation expectations reduced and optional.
    - Preserve observed IDs, actor relation, evidence status, confidence, visibility, and degradation flags together.
    - Produce docs/implementation_handoffs/parser_opponent_card_observations_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

  Do not:
    - Target main directly.
    - Close tracker #47 or related issue #11.
    - Change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
    - Infer hidden opponent cards, complete opponent decklists, classify archetypes, call OpenAI/model providers, or move parser truth into workbook formulas, dashboard logic, webhook transport, Apps Script, AI, or analytics surfaces.
    - Make card performance aggregate opponent cards.
    - Copy Manasight source code or commit raw private Player.log excerpts.
    - Stage or commit unless explicitly asked.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/50"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/48"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/111"
  previous_merge_commit: "76b63622494b0bbc6150e6bd19973b4ac8e0be0c"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_opponent_card_observations.md"
  target_artifact: "docs/implementation_handoffs/parser_opponent_card_observations_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_opponent_card_observations.py"
    - "python3 -m pytest -q tests/test_gameplay_actions.py tests/test_card_performance.py tests/test_grp_id_catalog.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not infer hidden opponent cards, complete opponent decklists, classify archetypes, call OpenAI/model providers, or move parser truth into workbook formulas, dashboard logic, webhook transport, Apps Script, AI, or analytics surfaces."
    - "Do not make card performance aggregate opponent cards."
    - "Do not copy Manasight source code or commit raw private Player.log excerpts."
```
