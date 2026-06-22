# Parser Parity Action Streams, Board Snapshots, And Draw Records Contract

## Module

`parser_parity_action_streams_board_snapshots_draw_records`

Plain English: this contract defines the safe parser-owned fact boundary for
future action stream, board snapshot, and draw record packets. These packets
may summarize observed GRE facts, reconstructed state transitions, inferred
action labels, degraded actions, public board projections, visible-card
changes, and draw-related evidence. They must not become complete game
chronology, complete Arena board state, hidden-card truth, opponent intent,
player-mistake labels, gameplay advice, analytics truth, AI truth, coaching
truth, private-harvest authorization, release readiness, or production
behavior.

This Codex B pass writes only this contract. It does not implement code, open
a PR, activate #388 or #381, read private logs, run private harvest, create
fixtures, edit corpus metadata, change parser behavior, or claim readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/532
- Parent issue: https://github.com/Tahjali11/Mythic-Edge/issues/486
- Parent umbrella: https://github.com/Tahjali11/Mythic-Edge/issues/483
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/533
- Previous completed PR: https://github.com/Tahjali11/Mythic-Edge/pull/556
- Previous merge commit:
  `ff40a51cc397e511855135d449ca9d068a7e6cee`
- Base branch: `main`
- Target branch: `main`
- Contract branch:
  `codex/parser-parity-action-streams-board-snapshots-532`
- Risk tier: High

Observed during this Codex B pass:

- The primary checkout had unrelated local governance/workflow modifications,
  so this contract was written in a clean sibling worktree.
- The clean worktree was created from `origin/main` at
  `ff40a51cc397e511855135d449ca9d068a7e6cee`.
- Issue #532 was open.
- Parent issue #486 was open.
- Parent umbrella #483 was open.
- Pipeline tracker #388 was open and inactive.
- Parent private-evidence issue #434 was open.
- Issue #533 was closed and PR #556 was merged.

Current authorization facts to preserve:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
implementation_authorized: false
```

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

Tracker #388 remains open and inactive. This contract does not activate #388
or #381.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- Issue #532 and its Codex A reconciliation comment
- Parent issue #486
- Parent umbrella #483
- Pipeline tracker #388
- Parent private-evidence issue #434
- Issue #533 and PR #556
- `docs/contracts/parser_parity_draft_session_lifecycle_pick_deckbuild_packets.md`
- `docs/contracts/parser_parity_limited_capture_packet_coverage.md`
- `docs/contracts/parser_parity_gre_annotation_semantics.md`
- `docs/contracts/parser_owned_fact_capture_tracker.md`
- `docs/contracts/parser_corpus_gameplay_action_attribution_behavior_uplift.md`
- `docs/contracts/parser_corpus_gameplay_event_ordering_behavior_uplift.md`
- `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`
- `docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`
- `docs/contracts/parser_game_state_diff_mechanics.md`
- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/parser_opponent_card_observations.md`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/annotations.py`
- Focused gameplay-action, opponent-card, GRE GameState, parser-owned fact
  tracker, corpus parity, and golden replay tests by inspection.

No Hollowmark source code, 17Lands source/data, Manasight source/corpus data,
external logs, private `Player.log`, private `UTC_Log`, app-data, live MTGA,
diagnostics, drift, watcher, tailer, private smoke, private harvest, draft
capture, sealed capture, or limited capture evidence was copied, imported,
summarized, hashed, or read.

## Owning Layer

Primary owning layer: Parser.

Supporting layer: Corpus / Provenance.

The parser owns normalized GRE, state, gameplay-action, visible opponent-card,
and future action/snapshot/draw packet facts. Corpus / Provenance may later
track packet evidence, synthetic fixtures, golden replay confirmation,
parser-owned fact tracker progress, and review status, but corpus metadata does
not own parser truth.

## Internal Project Area

Primary: Parser.

Supporting:

- Corpus / Provenance, for future evidence, fixture, provenance, replay, and
  parser-owned fact tracker reporting.
- Quality / Governance, for workflow, validation, and protected-surface
  discipline.

This contract is not analytics, AI, coaching, workbook/transport, local app,
release readiness, production behavior, private-evidence execution, or #388
activation work.

## Truth Owner

Truth owner for current source facts:

- `src/mythic_edge_parser/parsers/gre/game_state.py`
  owns normalized GRE GameState payload construction, raw list preservation,
  turn identity, diff metadata, and additive normalized evidence views.
- `src/mythic_edge_parser/parsers/gre/annotations.py`
  owns normalized annotation records and marker summaries.
- `src/mythic_edge_parser/app/gameplay_actions.py`
  owns current parser-normalized gameplay-action extraction and action-entry
  facets.
- `src/mythic_edge_parser/app/opponent_card_observations.py`
  owns downstream visible opponent-card observations and hidden-draw
  suppression behavior.
- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
  owns future public-safe target, ledger, and progress metadata only.

Truth owner for future #532 packet facts, if later implemented:

- a new parser-owned action/snapshot/draw packet helper, or an explicitly
  authorized additive section in an existing parser-owned helper;
- focused tests and implementation handoffs created under a later issue
  authorization; and
- future contract-test reports that verify the implementation against this
  contract.

This contract does not make public external references, corpus metadata,
downstream analytics, workbook formulas, dashboard logic, Apps Script, webhook
transport, AI output, or coaching output truth owners for action, board, draw,
or visible-card facts.

## Bridge-Code Status

`deferred_future_boundary`

Codex B authorizes no bridge code. If a later pass is explicitly authorized
after review, the allowed data flow is:

```text
parser-owned GRE GameState / annotations / diff mechanics / gameplay actions / visible observations
  -> field-level source, confidence, finality, degradation, and review metadata
  -> public-safe action stream, board snapshot, draw record, and visible-card packets
  -> parser-owned fact tracker coverage progress
  -> optional corpus/golden replay evidence summaries
```

Forbidden reverse flow:

- Packet summaries must not change parser behavior.
- Board snapshots must not rewrite parser state.
- Draw records must not create hidden-card truth.
- Parser-owned fact tracker rows must not create parser facts.
- Corpus coverage statuses must not rewrite action/snapshot/draw semantics.
- Public Hollowmark, 17Lands, or Manasight category surfaces must not become
  Mythic Edge parser truth.
- Analytics, AI, workbook, webhook, Apps Script, dashboard, and coaching
  surfaces must not define action stream, board snapshot, or draw record
  truth.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_parity_action_streams_board_snapshots_draw_records.md`

Potential future implementation files, only if separately authorized:

- `src/mythic_edge_parser/app/action_stream_packets.py`
- `tests/test_action_stream_packets.py`
- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`, only for
  additive target rows or report references;
- `tests/test_parser_owned_fact_tracker.py`, only for additive public-safe
  tracker fixtures;
- `docs/implementation_handoffs/parser_parity_action_streams_board_snapshots_draw_records_comparison.md`;
- `docs/contract_test_reports/parser_parity_action_streams_board_snapshots_draw_records.md`.

Potential future evidence or coverage files, only if separately authorized:

- synthetic public-safe fixtures under existing fixture directories;
- golden replay fixture/manifest additions after separate fixture-promotion
  authority;
- public-safe parser-owned fact tracker fixture/report files.

Referenced but not behavior-owned by this contract:

- GRE parser modules;
- gameplay-action modules;
- opponent-card observation modules;
- parser state modules;
- corpus manifest and session ledger;
- runtime action status artifacts;
- workbook/webhook/App Script/output/analytics/AI surfaces.

## Observed Current Behavior

Current GRE GameState behavior:

- `game_state.py` builds `GameStateEvent.payload` dictionaries from selected
  GRE `gameStateMessage` or `queuedGameStateMessage.gameStateMessage` inputs.
- The payload preserves `game_state_id`, message metadata, `identity`,
  `turn_info`, raw `players`, raw `zones`, raw `game_objects`, raw
  `annotations`, raw `persistent_annotations`, raw `timers`, raw `actions`,
  update/diff metadata, normalized annotations, normalized timers, and
  `game_state_diff_mechanics`.
- The GameState diff mechanics contract forbids treating diffs as complete
  snapshots or reconstructing missing GameState data.

Current annotation behavior:

- `annotations.py` normalizes raw annotation records, preserves unknown type
  names, extracts marker summaries such as zone transfers and object
  replacement pairs, and carries source, confidence, degradation, and
  review-required metadata.
- The GRE annotation semantics contract defines future typed semantic-fact
  expectations for selected annotation types, but #484 does not make
  annotations hidden-card truth, gameplay advice, or action causality truth.

Current gameplay-action behavior:

- `gameplay_actions.py` observes parser events whose `kind` is `GameState`.
- It maintains in-memory per-match/game state for known zones, objects, turn
  tracking, active player tracking, and action deduplication.
- It emits local runtime action entries for a bounded set of current
  behaviors, including `turn_started`, `spell_cast`, `spell_finished`,
  `land_played`, `put_onto_battlefield_from_hand`, `permanent_resolved`,
  `card_drawn`, `permanent_left_battlefield`, `permanent_died`,
  `card_discarded`, `spell_resolved_to_graveyard`, `card_exiled`, and
  `zone_change`.
- It uses raw GRE action labels, zone transitions, annotation categories,
  normalized object state, object replacement context, turn context, seat
  mapping, and card identity hints.
- It writes local runtime action JSON and Markdown artifacts. Those artifacts
  are local/generated runtime surfaces, not committed source truth.
- Existing tests cover selected local turn, land, spell, partial-diff,
  hidden-rendering, annotation-chain, and resolution behaviors.

Current opponent-card observation behavior:

- `opponent_card_observations.py` consumes gameplay-action entries to emit
  visible opponent-card observations.
- Hidden opponent draws from library to hand without reveal or public-zone
  evidence are suppressed and do not become clean observations.
- Observation fields carry identity, action, visibility, source evidence,
  evidence status, value source, confidence, degradation, and review metadata.

Current #481/#483/#486/#533 state:

- `parser_owned_fact_tracker.py` is a metadata-only scoreboard and does not
  read raw logs, approve fixtures, mutate corpus metadata, or create parser
  truth.
- The #533 draft-session lifecycle contract explicitly defers action streams,
  board snapshots, draw records, action sequence/monotonic ordering semantics,
  card played/cast labels, activated ability labels, attack/block
  participation, and inferred action labels to #486/#532.
- No canonical action stream packet, board snapshot packet, draw record
  packet, visible-card change packet, zone-transition packet, or public-safe
  action-window summary exists yet.
- No current public interface states when a board projection is full,
  partial, diff-derived, degraded, review-required, or unavailable.

## Problem Statement

Mythic Edge has strong raw GRE preservation and bounded gameplay-action
surfaces, but it does not yet have a stable contract for action-level history
or public board/draw summaries.

Without this contract, future work could accidentally treat:

- current gameplay-action runtime artifacts as complete action streams;
- current GameState object arrays as complete board truth;
- diff-derived state as a full snapshot;
- a library-to-hand transition as hidden-card identity;
- action list order as causal ordering;
- draw records as hand reconstruction;
- visible-card changes as complete decklist or sideboard truth; or
- parser-owned facts as gameplay advice, analytics truth, AI truth, coaching
  truth, release readiness, or production behavior.

The safe path is to define small packet families with explicit source,
confidence, finality, degradation, and review labels before any implementation
or fixture work begins.

## First Bad Value

The first bad value is any future action stream, board snapshot, draw record,
visible-card record, parser-owned fact tracker row, corpus report, golden
replay expectation, analytics row, AI summary, handoff, or issue comment that
treats reduced observed/reconstructed parser evidence as:

- complete causal chronology;
- complete board state;
- hidden-card truth;
- complete hand, library, deck, or sideboard truth;
- opponent intent;
- player mistakes;
- best-line or optimal-play truth;
- gameplay advice;
- analytics truth;
- AI truth;
- coaching truth;
- parser behavior readiness;
- fixture-promotion readiness;
- release readiness;
- production behavior; or
- full parser parity.

## Scope Decision

Selected path: schema-first contract boundary with future implementation gated
behind explicit authorization.

This contract defines:

- action stream packet vocabulary;
- board snapshot packet vocabulary;
- draw record and visible-card-change vocabulary;
- zone-transition and life/resource-change vocabulary;
- field-level source, provenance, confidence, finality, degradation, and
  review rules;
- allowed and forbidden inputs;
- relationship to #486, #533, #484, #481, and #388; and
- validation expectations for later implementation.

This contract does not approve an immediate Codex C implementation because the
current handoff sets `implementation_authorized=false`.

After Codex E review and explicit user authorization, a later implementation
may choose one of these narrow paths:

1. `schema_and_validator_only`: add in-memory public-safe packet schema
   builders or validators with synthetic test payloads only.
2. `synthetic_game_state_projection`: project reduced action/snapshot/draw
   summaries from Mythic Edge-owned synthetic GameState events without
   changing parser behavior or corpus statuses.
3. `gameplay_action_packet_projection`: project a reduced action stream from
   existing gameplay-action entries while labeling order and causality
   non-claims.
4. `split_before_implementation`: split attack/block participation,
   activated-ability labels, complete board snapshot expectations, or draw
   identity semantics into smaller child issues if they cannot fit safely.

If Codex C cannot keep the implementation public-safe, additive,
synthetic-first, and non-authoritative, it must stop and route back to Codex B
or Codex A.

## Packet Families

V1 packet family vocabulary:

| Packet family | Purpose | Current status |
| --- | --- | --- |
| `action_stream_packet` | Ordered reduced list of parser-observed or parser-reconstructed action records for one match/game/window. | Contract-only; no canonical packet exists. |
| `action_record` | One bounded action fact with source, ordering basis, action label, actor relation, object/card hints, zone movement, and review labels. | Partially sourced by gameplay-action entries; not a complete action truth. |
| `board_snapshot_packet` | Reduced public board projection at one GameState/window, including visible/public zones and object summaries. | Contract-only; GameState payloads exist but no complete board packet exists. |
| `board_object_summary` | One object within a board projection with object IDs, zone, controller/owner, card identity hints, and confidence. | Partially sourced by GameState objects; hidden or malformed values must degrade. |
| `draw_record_packet` | Reduced draw-related evidence summary for one match/game/window. | Contract-only; current gameplay actions can classify some `card_drawn` transitions. |
| `draw_record` | One draw-related observation or suppressed/unknown draw marker with visibility, identity policy, and confidence. | Contract-only; opponent hidden draws must not become clean visible-card facts. |
| `visible_card_change_record` | One public or parser-visible card appearance/disappearance/zone-change summary. | Partially adjacent to gameplay actions and opponent observations. |
| `zone_transition_record` | One normalized movement between zones with source and confidence labels. | Partially adjacent to gameplay-action entries. |
| `life_resource_change_record` | Future reduced record for life, counters, mana, or resource changes where parser evidence is explicit. | Deferred until GRE annotation semantics or parser-owned facts authorize it. |
| `action_window_summary` | Public-safe aggregate counts, degraded counts, review-required counts, first/last observed state, and non-claims. | Contract-only. |

## Normalized Record Shape

Future implementation may adjust field names only if Codex E confirms semantic
equivalence. V1 packet objects must be JSON-serializable, deterministic, and
free of raw private payloads.

### Common Packet Metadata

Every packet family must include:

```yaml
object: "<packet object name>"
schema_version: "parser_parity_action_streams_board_snapshots_draw_records.v1"
source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/532"
parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/486"
parent_umbrella: "https://github.com/Tahjali11/Mythic-Edge/issues/483"
pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
match_id: "<parser-owned match id or blank>"
game_number: "<parser-owned game number or blank>"
packet_id: "<deterministic public-safe id>"
packet_scope: "<match|game|turn|game_state|window|review_required>"
source_event_refs: []
source_packet_refs: []
total_records: 0
degraded_records: 0
review_required: false
value_source: "<observed|derived|inferred|unknown|conflict>"
confidence: "<high|medium|low|unknown>"
finality: "<provisional|final|snapshot_only|review_required>"
degradation_flags: []
non_claims: []
```

### `action_record`

Required logical fields:

```yaml
record_id: "<deterministic packet-local id>"
sequence_index: 0
ordering_basis:
  - "game_state_id"
timestamp: ""
game_state_id: ""
turn_number: ""
active_player_seat_id: ""
actor_relation: "<local|opponent|unknown>"
actor_seat_id: ""
action_type: "<spell_cast|land_played|card_drawn|zone_change|turn_started|unknown|...>"
action_label_source: "<raw_action_array|zone_transition|annotation|derived|inferred|unknown|conflict>"
instance_id: ""
grp_id: ""
observed_grp_id: ""
object_source_grp_id: ""
overlay_grp_id: ""
parent_id: ""
identity_hint_source: ""
from_zone_type: ""
to_zone_type: ""
raw_action_types: []
annotation_types: []
annotation_categories: []
source_evidence: []
value_source: "<observed|derived|inferred|unknown|conflict>"
confidence: "<high|medium|low|unknown>"
finality: "<provisional|final|snapshot_only|review_required>"
degradation_flags: []
review_required: false
non_claims: []
```

Allowed `action_label_source` meanings:

- `raw_action_array`: sourced from a GRE action array label;
- `zone_transition`: sourced from observed previous/current zone movement;
- `annotation`: sourced from normalized annotation marker/category evidence;
- `derived`: computed from parser-owned observed facts;
- `inferred`: best-effort label from partial evidence and must not be high
  confidence;
- `unknown`: source is missing or unsupported;
- `conflict`: evidence disagrees and must require review.

`sequence_index` is packet-local ordering only. It is not a global action
sequence number, causal order guarantee, or proof that missing hidden actions
did not occur.

### `board_snapshot_packet`

Required logical fields:

```yaml
snapshot_id: "<deterministic public-safe id>"
snapshot_kind: "<reduced_board_projection|public_zone_projection|diff_projection|review_required>"
snapshot_completeness: "<reduced_observed_projection|partial_diff_projection|not_complete_state|unknown|conflict>"
game_state_id: ""
turn_number: ""
active_player_seat_id: ""
update_kind: ""
diff_mechanics_ref: ""
zones: []
objects: []
source_evidence: []
value_source: "<observed|derived|unknown|conflict>"
confidence: "<high|medium|low|unknown>"
finality: "<snapshot_only|provisional|review_required>"
degradation_flags: []
review_required: false
non_claims:
  - "not_complete_arena_state"
  - "not_hidden_zone_truth"
```

Board snapshots must be described as reduced projections. They must not claim
to contain:

- full hidden zones;
- complete libraries;
- complete hands unless explicitly visible and parser-owned;
- complete decklists or sideboards;
- complete object history;
- complete counter/power/toughness truth unless the relevant parser-owned
  source fields explicitly support those values; or
- causal explanations for why the state changed.

If a GameState update is a diff, lacks previous-state linkage, has deletion
markers, or otherwise cannot support a complete projection, the snapshot must
use `partial_diff_projection`, `not_complete_state`, or `review_required`.

### `board_object_summary`

Required logical fields:

```yaml
instance_id: ""
grp_id: ""
observed_grp_id: ""
object_source_grp_id: ""
overlay_grp_id: ""
parent_id: ""
identity_hint_source: ""
zone_id: ""
zone_type: ""
visibility: ""
owner_seat_id: ""
controller_seat_id: ""
object_type: ""
card_types: []
super_types: []
subtypes: []
colors: []
power: ""
toughness: ""
source_evidence: []
value_source: "<observed|derived|unknown|conflict>"
confidence: "<high|medium|low|unknown>"
degradation_flags: []
review_required: false
```

Object summaries must omit, blank, or degrade unsupported fields. They must
not guess hidden identities or fill missing values from analytics, AI,
workbook, decklists, private strategy notes, or external data.

### `draw_record`

Required logical fields:

```yaml
record_id: "<deterministic packet-local id>"
draw_record_type: "<visible_draw|local_draw_observed|hidden_draw_suppressed|draw_transition_degraded|unknown>"
timestamp: ""
game_state_id: ""
turn_number: ""
actor_relation: "<local|opponent|unknown>"
actor_seat_id: ""
from_zone_type: "ZoneType_Library"
to_zone_type: "ZoneType_Hand"
instance_id: ""
grp_id: ""
identity_policy: "<visible_identity_allowed|identity_redacted|identity_unknown|identity_forbidden>"
visibility: "<visible|local_visible|hidden_not_recorded|ambiguous|unknown>"
source_evidence: []
value_source: "<observed|derived|unknown|conflict>"
confidence: "<high|medium|low|unknown>"
degradation_flags: []
review_required: false
non_claims:
  - "not_hand_reconstruction"
  - "not_hidden_card_truth"
```

Draw record rules:

- Opponent hidden library-to-hand movement without reveal or public-zone
  evidence must not emit a clean visible-card fact.
- A future implementation may choose to suppress hidden draws entirely, or emit
  a redacted `hidden_draw_suppressed` marker with blank identity fields and
  `identity_policy: "identity_forbidden"`.
- Local draws may be represented only with parser-owned evidence and must not
  leak private hand contents into public committed artifacts.
- Draw records must not reconstruct hands, libraries, decklists, sideboards,
  archetypes, matchup plans, or hidden-card availability.

### `visible_card_change_record`

Required logical fields:

```yaml
record_id: "<deterministic packet-local id>"
change_type: "<appeared_public|left_public|revealed|hidden_suppressed|zone_changed|unknown|conflict>"
timestamp: ""
game_state_id: ""
turn_number: ""
actor_relation: "<local|opponent|unknown>"
instance_id: ""
grp_id: ""
from_zone_type: ""
to_zone_type: ""
visibility: "<public|revealed|derived_zone_transition|ambiguous|hidden_not_recorded|unknown>"
source_evidence: []
value_source: "<observed|derived|unknown|conflict>"
confidence: "<high|medium|low|unknown>"
degradation_flags: []
review_required: false
```

Visible-card change records may cite gameplay actions and opponent-card
observations, but they must preserve the observation layer's hidden-card and
visibility restrictions.

## Source, Confidence, Finality, And Degradation Vocabulary

Allowed `value_source` values:

- `observed`: directly present in parser-owned GRE or parser-normalized
  evidence.
- `derived`: computed from parser-owned observed values.
- `inferred`: best-effort label from partial evidence; never high confidence.
- `unknown`: unavailable or unsupported.
- `conflict`: evidence disagrees.

Allowed `confidence` values:

- `high`: direct parser-owned evidence supports the value, no relevant
  degradation flags exist, and the value is not hidden or inferred.
- `medium`: multiple parser-owned signals are consistent but some context is
  derived or incomplete.
- `low`: partial or inferred support only, or the field is useful but
  degraded.
- `unknown`: no reliable value can be produced.

Allowed `finality` values:

- `provisional`: live or packet-local value that may be superseded by later
  parser events.
- `final`: only after the owning parser state/replay path proves the field is
  final for the relevant scope.
- `snapshot_only`: true only for the source GameState/window; not durable game
  truth.
- `review_required`: evidence ambiguity or conflict requires review.

Required degradation flags include, when applicable:

- `missing_match_identity`
- `missing_game_number`
- `missing_game_state_id`
- `missing_turn_context`
- `missing_seat_mapping`
- `actor_relation_unknown`
- `action_label_inferred`
- `action_label_conflict`
- `ordering_basis_missing`
- `sequence_gap_possible`
- `diff_snapshot_not_complete`
- `previous_state_link_missing`
- `deletion_marker_present`
- `hidden_card_identity_forbidden`
- `draw_identity_redacted`
- `visibility_ambiguous`
- `missing_card_identity`
- `object_identity_conflict`
- `zone_transition_conflict`
- `unsupported_annotation_semantics`
- `external_or_private_evidence_forbidden`

Every record with degradation flags must either set `review_required: true` or
document why the degraded condition is an expected non-claim.

## Event Ordering And Sequence Non-Claims

Action stream packets may expose packet-local order only. They must not claim:

- complete event sequence truth;
- complete causal order;
- absence of hidden actions;
- that every Arena action has a record;
- that timestamps are complete ordering truth;
- that `game_state_id` is a global ordering key;
- that gameplay-action row order proves all parser event order;
- that action-attribution coverage proves event-ordering support; or
- that board snapshots explain why an action happened.

If a future implementation needs stronger sequence semantics, it must route to
a separate contract or explicitly build on the #498 event-ordering behavior
uplift lane.

## Relationship To #486 Action And Draft Enrichment

#486 owns the broader action and draft surface enrichment lane. This #532
contract owns the first narrow action-history slice:

- action streams;
- board snapshots;
- draw records;
- visible-card change summaries;
- zone transition summaries; and
- strict non-claims for hidden information and causality.

Fields still deferred outside #532 unless separately authorized:

- legacy draft shapes not covered by #533;
- full attack/block participation semantics;
- activated ability semantic parity beyond current raw action labels;
- complete board-state reconstruction;
- complete hand/library/deck/sideboard reconstruction;
- strategic action quality;
- player-mistake labeling;
- archetype or matchup inference;
- UI overlays, Match Journal display, workbook output, or analytics endpoint
  exposure.

## Relationship To #533 Draft Lifecycle Packets

#533 owns draft-session lifecycle, pick/deckbuild packets, and draft-to-match
linkage. This #532 contract must not duplicate #533 lifecycle ownership.

Future integration may link #533 and #532 only by reference:

- #533 packets may cite #532 action/snapshot/draw packets as later game
  context after a draft session.
- #532 action/snapshot/draw packets may cite #533 `draft_session_id` only when
  that field is parser-owned and available.
- Neither packet family may turn draft picks, card pool contents, submitted
  decklists, sideboards, or strategic choices into advice or analytics truth.

## Relationship To #484 GRE Annotation Semantics

#484 defines selected GRE annotation semantic parity. #532 may use normalized
annotations and future typed semantic facts only as source evidence with
confidence and degradation labels.

#532 must not:

- infer hidden-card identity from annotations;
- convert raw annotation presence into action causality truth;
- treat unsupported annotation types as known semantics;
- use annotation details to produce gameplay advice; or
- create new annotation semantics without #484-compatible authority.

Unsupported or ambiguous annotation support must produce `unknown`,
`inferred`, `low`, or `review_required` labels.

## Relationship To #481 Parser-Owned Fact Tracker

#481 may track future #532 fact targets and lifecycle status. It must not
create parser facts or approve readiness.

Potential future tracker fact families:

- `gameplay_action.action_stream_packet`
- `gameplay_action.board_snapshot_packet`
- `gameplay_action.draw_record_packet`
- `gameplay_action.visible_card_change_record`
- `gameplay_action.zone_transition_record`

Tracker status must begin as `not_captured`, `deferred_feature_expansion`,
`review_required`, `synthetic_packet_ready`, `private_evidence_blocked`, or
`external_reference_only` according to evidence. A tracker row must not become
`human_approved`, `promotion_proof_ready`, `fixture_manifest_draft_ready`,
`promoted_golden_fixture`, or platform-confirmed without separate review,
proof, fixture/manifest metadata, and explicit fixture-promotion authority.

The following flags remain false:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
implementation_authorized: false
```

## Allowed Inputs

Allowed for this contract and any later explicitly authorized public-safe
implementation:

- GitHub issue/PR metadata for #532, #486, #483, #388, #434, #533, and
  related parser-parity contracts.
- Repo-owned contracts and implementation handoffs.
- Existing parser source and tests by inspection.
- Synthetic Mythic Edge-owned test events or fixtures that contain no private
  raw log lines, no private player identifiers, no private paths, no external
  corpus contents, and no strategy notes.
- Existing parser-normalized `GameStateEvent` payloads created in tests.
- Existing parser-owned gameplay-action entries created in tests.
- Existing parser-owned visible opponent-card observation records created in
  tests.
- Public external repository metadata or issue text as category reference only,
  without copying source/data/log content.

Allowed future source fields, only when produced by parser-owned modules:

- `match_id`, `game_number`, `game_state_id`, timestamps, turn context, active
  player context, zones, game objects, actions, annotations, diff mechanics,
  gameplay-action entries, and visible opponent-card observations.

## Forbidden Inputs

Forbidden for Codex B and for later implementation unless a new explicit
contract and user approval authorize them:

- private `Player.log`;
- raw or normalized private `UTC_Log`;
- app-data;
- live MTGA;
- diagnostics, drift, watcher, tailer, packet, network, OS/router, or private
  smoke evidence;
- private harvest outputs;
- private draft, sealed, limited, hand, library, deck, or sideboard captures;
- private logs, private paths, generated private artifacts, runtime files,
  SQLite databases, tokens, credentials, API keys, webhook URLs, workbook
  exports, decklists, card choices, sideboard choices, or private strategy
  notes;
- Hollowmark source code;
- 17Lands source code or data;
- Manasight source code, corpus data, raw logs, compressed logs, hash lists,
  byte-size lists, or capture-date row lists;
- external corpus contents;
- analytics labels, AI output, workbook formulas, dashboard classifications, or
  coaching text as parser evidence.

## Error Behavior

Future implementation must fail closed:

- Missing match identity or game number must reject the packet or set
  `review_required` with `missing_match_identity` or `missing_game_number`.
- Missing `game_state_id`, ordering basis, or turn context must degrade rather
  than fabricate sequence order.
- Diff-derived snapshots must use `partial_diff_projection` or
  `not_complete_state`; they must not claim complete state.
- Deletion markers must lower completeness and may require review.
- Hidden draws must be suppressed or redacted; they must not emit clean card
  identity.
- Conflicting zone, object, card, actor, or action evidence must set
  `value_source: "conflict"` and `review_required: true`.
- Unsupported annotation semantics must remain `unknown`, `inferred`, or
  review-required.
- Malformed or unexpected source values must not raise during normal parser use
  if a later implementation is integrated into parser runtime; they should
  become degraded metadata.
- Contract ambiguity, requested private input, or requested protected-surface
  change must stop and route back to Codex B or Codex A.

## Side Effects

Codex B side effects:

- Writes this contract file only.

Future implementation side effects, only if separately authorized:

- May create in-memory packet objects and focused synthetic tests.
- May write an implementation handoff.
- May add public-safe synthetic fixtures only if explicitly authorized.

Forbidden side effects:

- no runtime status files;
- no local action status artifacts;
- no private evidence files;
- no committed raw logs or private reports;
- no fixture promotion;
- no corpus metadata edits;
- no workbook, webhook, Apps Script, Google Sheets, analytics, AI, coaching,
  CI, release, deploy, or production behavior changes;
- no issue creation, PR creation, staging, commit, push, merge, or tracker
  closure in Codex B.

## Dependency Order For Future Implementation

If implementation is later explicitly authorized, use this order:

1. Add public-safe packet schema constants and validators or builders.
2. Add focused synthetic tests for malformed/missing/degraded cases.
3. Add reduced synthetic action stream tests using existing parser-owned
   `GameStateEvent` or gameplay-action entries.
4. Add reduced board snapshot tests that prove partial/diff snapshots do not
   claim complete state.
5. Add draw record tests proving hidden opponent draws are suppressed or
   redacted.
6. Add parser-owned fact tracker rows only if #481-compatible and separately
   authorized.
7. Add corpus/golden replay references only after separate fixture-promotion
   or corpus-status authority.

Any need to change parser behavior, parser event classes, state final
reconciliation, workbook/webhook/App Script behavior, analytics behavior, AI
behavior, or production behavior must stop for a new issue/contract.

## Compatibility

Future implementation must preserve:

- existing `GameStateEvent.payload` fields;
- existing `game_state_diff_mechanics` behavior;
- existing `normalized_annotations` behavior;
- existing `gameplay_actions.py` runtime action behavior unless a later
  contract explicitly changes it;
- existing opponent-card hidden-draw suppression;
- existing parser-owned fact tracker false readiness/non-authorization flags;
- existing corpus manifest and session ledger state unless separately
  authorized.

New packet shapes must be additive. Existing consumers must not be required to
use them unless a later contract updates those consumers.

## Synthetic Fixture Requirements

Future synthetic fixtures or tests for #532 must:

- be Mythic Edge-owned and public-safe;
- state that they are synthetic, not raw `Player.log`;
- contain no private player names, private account identifiers, deck names,
  strategy notes, sealed pools, draft pools, private card choices, raw external
  logs, or external corpus contents;
- exercise the normal parser path when claiming parser behavior;
- include expected reduced parser-owned outputs only for fields claimed;
- include explicit negative assertions for hidden draw/card identity behavior;
- include explicit degradation expectations for diff/partial board snapshots;
- include explicit ordering non-claims when asserting packet-local order;
- avoid asserting complete game chronology or complete board state.

## Golden Replay Confirmation Requirements

No golden replay confirmation is authorized by this contract.

If a later issue authorizes stronger-than-synthetic claims, that issue must
require:

- a reviewed public-safe fixture;
- a golden replay manifest;
- expected reduced packet outputs only;
- proof that no raw/private log lines or external corpus contents were
  committed;
- review of hidden-card, draw, board-completeness, and ordering non-claims;
- Codex E review before Codex F submitter work;
- Codex G explicit merge/close/tracker approval.

Golden replay must not turn packet summaries into complete game truth,
production readiness, analytics truth, AI truth, or coaching truth.

## Tests Required

Codex B validation for this contract:

```bash
git diff --check
git diff --no-index --check /dev/null docs/contracts/parser_parity_action_streams_board_snapshots_draw_records.md
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_parity_action_streams_board_snapshots_draw_records.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_parity_action_streams_board_snapshots_draw_records.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_parity_action_streams_board_snapshots_draw_records.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

Future Codex C validation, only if implementation is separately authorized:

```bash
python3 -m pytest -q tests/test_action_stream_packets.py
python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_game_state_diff_parser.py
python3 -m pytest -q tests/test_parser_owned_fact_tracker.py
python3 -m pytest -q tests/test_golden_replay_harness.py
```

If future work touches corpus metadata, also require:

```bash
python3 -m pytest -q tests/test_corpus_parity_report.py
```

All later implementations must also run path-scoped secret/private marker
checks, protected-surface checks, validation selector, and `git diff --check`.

## Acceptance Criteria

- This contract exists at
  `docs/contracts/parser_parity_action_streams_board_snapshots_draw_records.md`.
- The contract links to the source issue, parent issue, umbrella, tracker, and
  private-evidence parent.
- The contract names Parser as truth owner and Corpus / Provenance as
  supporting evidence owner.
- The contract defines action stream, action record, board snapshot, board
  object summary, draw record, visible-card change, zone transition, and action
  window summary vocabulary.
- The contract preserves hidden-card, board-completeness, ordering, analytics,
  AI, coaching, release, production, fixture-promotion, corpus-status, and
  #388/#381 non-claims.
- The contract recommends Codex E review before any implementation.
- The contract changes no parser behavior and no protected downstream surface.

## Open Questions And Contract Risks

- Whether future board snapshots should be a parser runtime helper, replay-only
  helper, or corpus/provenance report helper remains open until
  implementation is authorized.
- Whether attack/block participation and activated-ability labels need smaller
  child contracts is likely, because those labels are higher risk than zone
  transitions and draw suppression.
- Whether local-player draw identity can be represented in public-safe
  committed artifacts remains unresolved and should default to redaction or
  synthetic-only evidence.
- Whether #532 should later update parser-owned fact tracker rows depends on
  #481-compatible implementation authority, not this contract alone.
- Whether golden replay should confirm these packets depends on a later
  fixture-promotion contract and explicit approval.

## Next Workflow Action

Next role: Codex E, Module Reviewer / Contract Tester.

Reason: the current handoff says `implementation_authorized=false`, so this
docs-only contract should be reviewed before any Codex C implementation is
considered.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for issue #532.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/532

Parent issue:
https://github.com/Tahjali11/Mythic-Edge/issues/486

Parent umbrella:
https://github.com/Tahjali11/Mythic-Edge/issues/483

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/533

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/556

Previous merge commit:
ff40a51cc397e511855135d449ca9d068a7e6cee

Base branch:
main

Contract artifact:
docs/contracts/parser_parity_action_streams_board_snapshots_draw_records.md

Task:
Review the #532 contract for action streams, board snapshots, and draw records
against issue #532, parent issue #486, umbrella #483, tracker #388, parent
private-evidence issue #434, the prior #533 contract, and the current parser
truth/protected-surface rules. Lead with findings. Confirm whether the
contract safely preserves hidden-card, complete-board-state, ordering,
analytics/AI/coaching, readiness, fixture-promotion, corpus-status, private
harvest, and #388/#381 non-claims.

Protected boundaries:
- Do not implement code.
- Do not open a PR.
- Do not close #532, #486, #483, #388, or #434.
- Do not activate #388 or #381.
- Do not run or read private Player.log, UTC_Log, app-data, live MTGA,
  diagnostics, drift, watcher, tailer, private smoke, private harvest, draft,
  sealed, or limited capture evidence.
- Do not create fixtures, corpus metadata edits, parser behavior changes,
  workbook/webhook/App Script changes, analytics changes, AI/coaching changes,
  readiness claims, release claims, deploy claims, or production claims.

Expected output:
- Findings first, if any.
- Contract-test verdict.
- Validation performed.
- Recommended next role.
- workflow_handoff block with repository and repository_url.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/532"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/486"
  parent_umbrella: "https://github.com/Tahjali11/Mythic-Edge/issues/483"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/533"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/556"
  completed_thread: "B"
  next_thread: "E"
  verdict: "contract_written_review_required_before_implementation"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/parser-parity-action-streams-board-snapshots-532"
  source_artifact: "https://github.com/Tahjali11/Mythic-Edge/issues/532"
  target_artifact: "docs/contracts/parser_parity_action_streams_board_snapshots_draw_records.md"
  previous_merge_commit: "ff40a51cc397e511855135d449ca9d068a7e6cee"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
  validation:
    - "git diff --check"
    - "git diff --no-index --check /dev/null docs/contracts/parser_parity_action_streams_board_snapshots_draw_records.md"
    - "python3 tools/check_agent_docs.py"
    - "path-scoped secret/private marker scan"
    - "path-scoped protected-surface scan"
    - "path-scoped validation selector"
  stop_conditions:
    - "Do not implement code until a later issue/user authorization explicitly allows it."
    - "Do not open a PR in Codex B."
    - "Do not close #532, #486, #483, #388, or #434."
    - "Do not activate #388 or #381."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, diagnostics, drift, watcher, tailer, private smoke, private harvest, draft capture, sealed capture, or limited capture evidence."
    - "Do not create fixtures, corpus metadata edits, parser behavior changes, workbook/webhook/App Script changes, analytics changes, AI/coaching changes, readiness claims, release claims, deploy claims, or production claims."
```
