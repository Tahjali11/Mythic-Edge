# Parser Parity Limited Capture Packet Coverage Contract

## Module

`parser_parity_limited_capture_packet_coverage`

Plain English: this contract defines the safe parser-owned fact boundary for
future 17Lands-style Limited capture packets. A Limited capture packet is a
reviewable bundle of observed or parser-reconstructed Limited facts, such as a
draft session identity, pack/pick position, selected card, deckbuild signal,
match/game linkage, and result summary. The packet may describe parser-owned
facts and their provenance, confidence, finality, degradation, and review
state, but it must not become draft advice, card grades, archetype truth,
analytics truth, AI truth, coaching truth, private-harvest authorization, or
release readiness.

This Codex B pass writes only this contract. It does not implement code, open
a PR, activate #388 or #381, read private logs, run limited capture, create
fixtures, edit corpus metadata, change parser behavior, or claim readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/485
- Parent umbrella: https://github.com/Tahjali11/Mythic-Edge/issues/483
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/484
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/554
- Previous merge commit:
  `3f253f6c887a927e26a973ef92e5222f2db9b785`
- Related draft-session follow-up:
  https://github.com/Tahjali11/Mythic-Edge/issues/533
- Deferred action/draft enrichment follow-up:
  https://github.com/Tahjali11/Mythic-Edge/issues/486
- Base branch: `main`
- Target branch: `main`
- Contract branch:
  `codex/parser-parity-limited-capture-packet-485`
- Risk tier: High

Observed during this Codex B pass:

- The primary checkout was on a gone #455 branch with unrelated local work:
  `docs/project_roadmap.md` was modified and
  `docs/contracts/parser_parity_gre_annotation_semantics.md` was untracked.
- To preserve unrelated local work, this contract was written in a clean
  sibling worktree on branch
  `codex/parser-parity-limited-capture-packet-485`.
- The clean worktree was created from `origin/main`.
- `HEAD` was `3f253f6c887a927e26a973ef92e5222f2db9b785`.
- Issue #485 was open.
- Parent umbrella #483 was open.
- Pipeline tracker #388 was open and inactive.
- Parent private-evidence issue #434 was open.
- Issue #484 was closed and PR #554 was merged.
- Issue #533 was open as a child of #485.
- Issue #486 was open and deferred until #484/#485 have enough clarity.

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
- Issue #485 and Codex A reconciliation comment
- Parent umbrella #483
- Pipeline tracker #388
- Parent private-evidence issue #434
- Issue #484 and PR #554
- Issue #533
- Issue #486
- Public GitHub metadata for `rconroy293/mtga-log-client`
- `docs/contracts/parser_parity_gre_annotation_semantics.md`
- `docs/contracts/parser_owned_fact_capture_tracker.md`
- `docs/contracts/parser_corpus_draft_with_games_coverage.md`
- `docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md`
- `docs/contracts/parser_corpus_sealed_lifecycle_coverage.md`
- `docs/contracts/parser_corpus_sealed_entry_lifecycle_coverage.md`
- `docs/contracts/parser_corpus_sealed_deckbuild_coverage.md`
- `docs/contracts/parser_corpus_sealed_match_coverage.md`
- `docs/contracts/parser_draft_bot.md`
- `docs/contracts/parser_draft_human.md`
- `docs/contracts/parser_draft_complete.md`
- `docs/contracts/parser_draft_surface_parity_recommendation.md`
- `docs/contracts/parser_corpus_readiness_metrics.md`
- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/fixtures/draft_with_games_synthetic_slice.log`
- `tests/fixtures/golden_replay/draft_with_games_synthetic.manifest.json`
- `src/mythic_edge_parser/parsers/draft_bot.py`
- `src/mythic_edge_parser/parsers/draft_human.py`
- `src/mythic_edge_parser/parsers/draft_complete.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
- Focused draft, sealed, corpus parity, golden replay, state, GRE, gameplay
  action, opponent-card, and parser-owned fact tracker tests by inspection.

No 17Lands source code, 17Lands data, external logs, private `Player.log`,
private `UTC_Log`, app-data, live MTGA, diagnostics, drift, watcher, tailer,
private smoke, private harvest, draft capture, sealed capture, or limited
capture evidence was copied, imported, summarized, hashed, or read.

The public `rconroy293/mtga-log-client` repository was checked only as public
metadata and category reference. Its GPL-3.0 license reinforces that Mythic
Edge must not copy source code into this contract or future implementation.

## Owning Layer

Primary owning layer: Parser.

Supporting layer: Corpus / Provenance.

The parser owns normalized facts emitted from draft, sealed, match, game,
client-action, GRE, gameplay-action, and opponent-card surfaces. Corpus /
Provenance may track packet coverage, field provenance, synthetic fixture
evidence, golden replay confirmation, and review status, but corpus metadata
does not own parser truth.

## Internal Project Area

Primary: Parser.

Supporting:

- Corpus / Provenance, for coverage, fixture, provenance, and replay evidence;
- Quality / Governance, for workflow, validation, and protected-surface
  review.

This contract is not analytics, AI, coaching, workbook/transport, local app,
release readiness, production behavior, private-evidence execution, or #388
activation work.

## Truth Owner

Truth owner for future Limited capture packet facts:

- draft event facts:
  - `src/mythic_edge_parser/parsers/draft_bot.py`
  - `src/mythic_edge_parser/parsers/draft_human.py`
  - `src/mythic_edge_parser/parsers/draft_complete.py`
- sealed/deckbuild and submitted-deck signal facts:
  - `src/mythic_edge_parser/parsers/client_actions.py`
  - `src/mythic_edge_parser/app/state.py`
  - `src/mythic_edge_parser/app/models.py`
  - `src/mythic_edge_parser/app/event_identity.py`
- match/game identity, game state, and result facts:
  - `src/mythic_edge_parser/parsers/match_state.py`
  - `src/mythic_edge_parser/parsers/gre/game_state.py`
  - `src/mythic_edge_parser/parsers/gre/game_result.py`
  - `src/mythic_edge_parser/app/state.py`
  - `src/mythic_edge_parser/app/models.py`
- gameplay action and visible opponent-card facts:
  - `src/mythic_edge_parser/app/gameplay_actions.py`
  - `src/mythic_edge_parser/app/opponent_card_observations.py`
- coverage and progress tracking:
  - `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
  - `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
  - `tests/fixtures/parser_corpus/session_ledger.v1.json`
  - future public-safe coverage progress reports explicitly authorized by
    #481/#485/#533 contracts.

This contract does not make public 17Lands surfaces, corpus metadata,
downstream analytics, workbook formulas, dashboard logic, Apps Script,
webhook transport, AI output, or coaching output a truth owner for Limited
facts.

## Bridge-Code Status

`deferred_future_boundary`

Codex B authorizes no bridge code. If a later pass is explicitly authorized
after review, the allowed data flow is:

```text
parser-owned draft / sealed / match / game / action facts
  -> field-level source, confidence, finality, and degradation metadata
  -> public-safe Limited capture packet summaries
  -> parser-owned fact tracker coverage progress
  -> optional corpus/golden replay evidence summaries
```

Forbidden reverse flow:

- Limited packet summaries must not change parser behavior.
- Parser-owned fact tracker rows must not create parser facts.
- Corpus coverage statuses must not rewrite draft/session/game semantics.
- Public 17Lands category surfaces must not become Mythic Edge parser truth.
- Analytics, AI, workbook, webhook, Apps Script, dashboard, and coaching
  surfaces must not define Limited packet truth.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_parity_limited_capture_packet_coverage.md`

Potential future implementation files, only if separately authorized:

- `src/mythic_edge_parser/app/limited_capture_packets.py`
- `tests/test_limited_capture_packets.py`
- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`, only for
  additive target rows or report references
- `tests/test_parser_owned_fact_tracker.py`, only for additive public-safe
  tracker fixtures
- `docs/implementation_handoffs/parser_parity_limited_capture_packet_coverage_comparison.md`
- `docs/contract_test_reports/parser_parity_limited_capture_packet_coverage.md`

Potential future evidence or coverage files, only if separately authorized:

- synthetic public-safe fixtures under existing fixture directories;
- golden replay fixture/manifest additions after separate fixture-promotion
  authority;
- public-safe parser-owned fact tracker fixture/report files.

Referenced but not behavior-owned by this contract:

- draft parser modules;
- GRE parser modules;
- parser state modules;
- gameplay action modules;
- opponent-card observation modules;
- corpus manifest and session ledger;
- workbook/webhook/App Script/output/analytics/AI surfaces.

## Observed Current Behavior

Current draft parser behavior:

- `DraftBot` recognizes `BotDraftDraftStatus` and `BotDraftDraftPick`.
- `DraftHuman` recognizes `Draft.Notify`,
  `EventPlayerDraftMakePick`, and qualifying `LogBusinessEvents` payloads with
  picked-card evidence.
- `DraftComplete` recognizes `DraftCompleteDraft`.
- Draft payloads may preserve `draft_id`, `event_id`, `draft_status`,
  `pack_number`, `pick_number`, `pack_card_ids`, `picked_card_id`, and
  `picked_card_ids` when source payloads provide those values.
- Draft payloads preserve parsed raw draft payloads inside event payloads.
- There is no current unified Limited capture packet model that joins draft
  event facts to deckbuild, match, game, result, opening-hand, mulligan,
  visible-opponent-card, or rank facts.

Current corpus/replay behavior:

- Corpus parity report command reports:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=22, report_only=11, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

- `draft_with_games_boundary_report_v1` remains report-only metadata.
- `draft_with_games_synthetic_v1` is a reduced synthetic completed
  draft-with-games path with `DraftBot`, `DraftComplete`, `MatchState`,
  `GameState`, and `GameResult`.
- The synthetic draft-with-games fixture proves one reduced synthetic draft
  event plus limited game/result path through golden replay. It does not prove
  all draft queues, BO3 draft, sideboarding, deck construction, draft pick
  quality, draft pools, submitted decklists, archetypes, analytics truth, AI
  truth, coaching truth, release readiness, or production behavior.
- Sealed entry, sealed deckbuild, and sealed match rows have narrow synthetic
  coverage. Each row explicitly preserves non-claims around sealed pool
  contents, decklists, card choices, archetypes, analytics truth, AI truth,
  coaching truth, and full lifecycle support.

Current #484 behavior:

- `docs/contracts/parser_parity_gre_annotation_semantics.md` defines a future
  semantic-fact boundary for selected GRE annotation types.
- #484 does not implement typed GRE semantic facts in code.
- Limited packet work may reference #484 vocabulary, but it must not claim
  typed GRE annotation support until future implementation and review prove
  it.

Current #481 behavior:

- `parser_owned_fact_tracker.py` exists as a metadata-only tracker for
  public-safe target matrices, local session ledgers, and coverage progress
  reports from supplied synthetic or already-sanitized metadata.
- The tracker is not a raw-log reader, fixture promoter, corpus mutator,
  parser behavior layer, or readiness gate.
- #485 may define future target fact rows for the tracker, but this contract
  does not add or mutate tracker data.

## Problem Statement

Mythic Edge has individual parser-owned Limited-related facts, narrow
synthetic corpus evidence, and a parser-owned fact tracker. What is missing is
a contract for the shape and safety rules of an integrated Limited capture
packet.

Without a contract, future work could accidentally:

- treat a single synthetic draft-with-games fixture as full 17Lands-style
  Limited coverage;
- join draft, deckbuild, match, game, and visible-card facts without field
  provenance;
- publish private decklists, card choices, sealed pools, or strategy notes;
- copy or mimic external parser source;
- move draft advice, card grades, archetype labels, or analytics into parser
  truth;
- promote #388/#381, private harvest, fixture promotion, or corpus status
  changes without approval.

## First Bad Value

The first bad value is any Limited packet field, parser-owned fact tracker row,
corpus report, golden replay expectation, review packet, implementation
handoff, or next-role prompt that treats existing draft parser events,
synthetic draft-with-games coverage, sealed synthetic metadata, generic GRE
annotations, public 17Lands category references, or private evidence plans as
any of the following:

- full 17Lands-style packet parity;
- parser support for every #485 target fact;
- live Limited capture success;
- private-harvest authorization;
- fixture-promotion readiness;
- corpus status readiness;
- parser behavior readiness;
- #388 or #381 activation readiness;
- decklist truth;
- card pool truth;
- hidden-card truth;
- draft-pick quality truth;
- archetype truth;
- matchup truth;
- analytics truth;
- AI truth;
- coaching truth;
- release readiness;
- production behavior.

## Scope Decision

Selected path: schema-first contract boundary with future implementation
gated behind explicit authorization.

This contract defines:

- target Limited packet families;
- current field coverage state;
- field-level provenance, confidence, finality, degradation, and review rules;
- allowed and forbidden inputs;
- how current synthetic fixtures may be referenced without overclaiming;
- how #481, #484, #533, and #486 relate to this lane.

This contract does not approve an immediate Codex C implementation because the
current handoff sets `implementation_authorized=false`.

After Codex E review and explicit user authorization, a later implementation
may choose one of these narrow paths:

1. `schema_and_validator_only`: add an in-memory/public-safe packet schema and
   validator with synthetic test payloads only.
2. `synthetic_fixture_packet_projection`: project fields from existing
   committed synthetic draft/sealed fixtures into reduced packet summaries
   without changing parser behavior or corpus statuses.
3. `route_to_533_first`: defer implementation until #533 defines the
   draft-session lifecycle and pick/deckbuild packet model.

If Codex C cannot keep the implementation public-safe, additive, and
non-authoritative, it must stop and route back to Codex B or Codex A.

## Packet Families

V1 packet family vocabulary:

| Packet family | Purpose | Current status |
| --- | --- | --- |
| `limited_session_packet` | Draft/sealed session identity and lifecycle context. | Contract-only; #533 owns lifecycle modeling details. |
| `limited_pick_packet` | Pack/pick position, available-card IDs, selected-card ID, autopick, and timer hints where observed. | Partially sourced by DraftBot/Human event payloads; no unified packet. |
| `limited_deckbuild_packet` | Card pool, submitted limited deck, maindeck, sideboard, companion, and command-zone signals where observed. | Mostly deferred/private-gated; sealed deckbuild currently proves only bounded submit-deck signal metadata. |
| `limited_match_packet` | Match ID, event ID, queue/format/rank context, match result, and match-level finality. | Partially sourced by parser state and synthetic draft/sealed fixtures. |
| `limited_game_packet` | Game number, play/draw, opening hand, mulligans, drawn-hand/drawn-card evidence, game result, result reason, and turn count. | Partially sourced by parser state and GRE result fixtures; drawn-card coverage remains deferred to #486 unless already parser-owned elsewhere. |
| `limited_visible_opponent_packet` | Opponent visible card IDs and observation provenance. | Partially sourced by opponent-card observations; hidden-card inference forbidden. |
| `limited_packet_provenance_summary` | Packet-level source refs, confidence, finality, degradation, review status, and non-claims. | New contract vocabulary only. |

The packet family names are contract vocabulary. They do not create public
Python APIs until a later implementation is explicitly authorized.

## Field Groups And Decisions

| Target field group | Current likely source | V1 decision |
| --- | --- | --- |
| draft ID | DraftBot/Human/Complete payloads | In schema; optional; observed only when present. |
| course/event ID | Draft payload aliases and match/event identity | In schema; optional; must distinguish draft event ID from match event ID. |
| event name | Draft payload aliases and event identity | In schema; optional; not archetype or queue truth by itself. |
| event state/module | Draft status/completion payloads | In schema; optional; no lifecycle claim until #533. |
| pack number | DraftBot/Human payloads | In schema; optional; preserve observed index without zero/one-based reinterpretation. |
| pick number | DraftBot/Human payloads | In schema; optional; preserve observed index without zero/one-based reinterpretation. |
| available cards in pack | DraftBot/Human `pack_card_ids` | In schema; public committed values may be synthetic only unless separately sanitized. |
| selected/picked card | DraftBot/Human `picked_card_id` / `picked_card_ids` | In schema; public committed values may be synthetic only unless separately sanitized. |
| autopick | Not current first-class Mythic Edge field | Deferred until source evidence is identified and contracted. |
| time remaining | Not current first-class Mythic Edge field | Deferred until source evidence is identified and contracted. |
| card pool | Not safe from current public evidence | Deferred/private-gated; public reports may use counts or symbolic refs only. |
| submitted limited deck | Submit-deck signal and future #533 deckbuild model | Deferred/private-gated except synthetic/public-safe submit-deck signal metadata. |
| maindeck/sideboard | Submit-deck card lists when observed | Deferred/private-gated; no private decklists or card choices in public artifacts. |
| companion/command-zone | Submitted-deck or game-state signals where observed | Deferred until explicit source mapping and synthetic fixtures exist. |
| match ID | MatchState/GRE/parser state | In schema; observed/parser-owned when emitted by normal parser path. |
| game number | GRE/parser state | In schema; observed/parser-owned when emitted by normal parser path. |
| event ID after draft | MatchState/parser state | In schema; distinguish from draft/course IDs. |
| play/draw | Parser state from starting player/team | In schema; confidence depends on starting-player evidence. |
| opening hand | Parser state opening hand evidence | In schema; committed public values synthetic only unless separately sanitized. |
| drawn hands | Not current unified field | Deferred to #486/#533 unless a later contract identifies parser-owned evidence. |
| drawn cards | Gameplay/action or hand-confirmation evidence | Deferred to #486 unless separately contracted as parser-owned fact. |
| mulligan count | Parser state / models | In schema; local player mulligan count only unless opponent evidence is contracted. |
| opponent mulligan count | Not current first-class packet field | Deferred until explicit source mapping and tests exist. |
| opponent visible card IDs | Opponent-card observations and visible zones | In schema as visible-only; no hidden-card inference. |
| game result | GRE game result/parser state | In schema; finality depends on final reconciliation evidence. |
| match result | GRE/parser state final reconciliation | In schema; finality depends on normal parser state. |
| result reason | GRE game result | In schema; observed only when source emits it. |
| turns | GRE turn info/parser state | In schema; `unknown` if missing or degraded. |
| rank context | Rank parser/model fields | In schema; optional; not Limited skill or matchmaking truth. |

## Normalized Packet Shape

A future packet, if separately authorized, must be public-safe and
field-provenance-first:

```yaml
object: "mythic_edge_limited_capture_packet"
schema_version: "parser_parity_limited_capture_packet.v1"
packet_id: "synthetic-or-symbolic-public-safe-id"
packet_family: "limited_session_packet"
source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/485"
parent_umbrella: "https://github.com/Tahjali11/Mythic-Edge/issues/483"
pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
source_refs:
  - "repo-relative-fixture-or-symbolic-review-ref"
format_family: "limited_draft"
queue_family: "premier_draft|traditional_draft|quick_draft|sealed|unknown"
session_ref:
  draft_id: ""
  course_event_id: ""
  match_event_id: ""
  match_id: ""
  game_number: null
packet_status: "synthetic_packet_ready"
fields:
  draft_id:
    value: "synthetic-draft-with-games-1"
    value_source: "observed"
    confidence: "high"
    finality: "provisional"
    source_surface: "DraftBot"
    source_ref: "tests/fixtures/draft_with_games_synthetic_slice.log#synthetic-event-1"
    degradation_flags: []
    review_required: false
non_claims:
  - "not_full_limited_packet_parity"
  - "not_private_harvest_authorization"
```

Required top-level fields:

- `object`
- `schema_version`
- `packet_id`
- `packet_family`
- `source_issue`
- `parent_umbrella`
- `pipeline_tracker`
- `source_refs`
- `format_family`
- `queue_family`
- `session_ref`
- `packet_status`
- `fields`
- `non_claims`

Required per-field metadata:

- `value`
- `value_source`
- `confidence`
- `finality`
- `source_surface`
- `source_ref`
- `degradation_flags`
- `review_required`

Public packet artifacts must not include raw log lines, raw payload bodies,
private paths, private hashes, source-byte offsets, deck names, private
decklists, sealed pools, private card choices, private strategy notes, or
external corpus contents.

## Status Vocabulary

Allowed `packet_status` values:

- `contract_only`
- `schema_ready`
- `synthetic_packet_ready`
- `report_only_reference`
- `private_evidence_blocked`
- `external_reference_only`
- `review_required`
- `invalid`

Forbidden status transitions:

- `contract_only` directly to `parser_behavior_ready=true`;
- any status directly to `pipeline_activation_ready_for_issue_388=true`;
- any status directly to `private_harvest_authorized=true`;
- any status directly to `fixture_promotion_authorized=true`;
- any status directly to `corpus_status_change_authorized=true`;
- any status directly to `full_limited_packet_parity`.

## Field Provenance And Confidence

Allowed `value_source` values:

- `observed`: directly emitted by current parser-normalized source evidence.
- `derived`: computed from parser-owned observed values.
- `inferred`: best-effort parser fallback; must be low or medium confidence
  and reviewable.
- `unknown`: unavailable from current evidence.
- `conflict`: source evidence disagrees.
- `legacy_enriched`: carried from older retained metadata and clearly marked.

Allowed `confidence` values:

- `high`: direct observed parser evidence with no relevant degradation.
- `medium`: derived or joined from parser-owned sources with clear provenance.
- `low`: inferred, partial, degraded, or source-shape uncertain.
- `unknown`: source unavailable or unsupported.

Allowed `finality` values:

- `provisional`: may change during live parsing or before reconciliation.
- `stable`: stable for the packet source but not a final match/game result.
- `final`: produced by final parser reconciliation or committed golden replay
  expected output.
- `unknown`: source does not expose finality.
- `review_required`: conflicting or ambiguous enough to need human review.

Required degradation flags:

- `missing_source_field`
- `malformed_source_field`
- `unsupported_source_shape`
- `source_conflict`
- `join_key_missing`
- `session_link_unresolved`
- `private_evidence_redacted`
- `external_reference_only`
- `synthetic_only`
- `semantic_projection_unimplemented`
- `review_required`

## Relationship To #484 GRE Annotation Semantics

#484 defines a future typed GRE annotation semantic-fact boundary. This
contract may use #484 names as planned source vocabulary, but it must not
claim those semantics are implemented.

Rules:

- Generic preserved GRE annotations are not enough to mark a Limited packet
  field as high-confidence semantic support.
- A future Limited packet may cite typed #484 semantic facts only after #484
  has an implementation, tests, and review for the exact annotation type.
- #484 semantics may support action or visible-card context, but they must not
  infer hidden cards, opponent intent, player mistakes, card quality,
  archetypes, matchup truth, or gameplay advice.

## Relationship To #481 Parser-Owned Fact Tracker

#481 owns metadata-only target matrices, local session ledgers, and coverage
progress reports. This contract may contribute future target fact rows, but it
does not add them now.

Recommended future fact families:

- `limited.session_identity`
- `limited.draft_pick_position`
- `limited.draft_pick_cards`
- `limited.deckbuild_signal`
- `limited.match_linkage`
- `limited.game_summary`
- `limited.visible_opponent_cards`
- `limited.result_summary`
- `limited.rank_context`

Tracker rows must preserve:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
implementation_authorized: false
```

Tracker rows must begin as `not_captured`, `deferred_feature_expansion`,
`review_required`, `synthetic_packet_ready`, `private_evidence_blocked`, or
`external_reference_only` according to evidence. A tracker row must not become
`promoted_golden_fixture` without review, proof, draft fixture/manifest
metadata, and explicit fixture-promotion authority.

## Relationship To #533 Draft Session Lifecycle

#533 owns the detailed draft-session lifecycle model: entering the event,
draft seats or bot/human context when visible, pack/pick progression,
deckbuild, deck submission, match linkage, and result context.

This contract intentionally stops short of implementing #533. It defines the
packet vocabulary that #533 may consume or refine.

Fields deferred to #533 unless separately authorized:

- canonical `draft_session_id` construction;
- joining draft IDs to match IDs across draft/deckbuild/matches;
- pack/pick sequence continuity rules;
- deckbuild lifecycle transitions;
- card-pool and submitted-deck public-safe summary rules;
- Premier Draft versus Traditional Draft versus Quick Draft lifecycle
  differences;
- Sealed deckbuild lifecycle beyond the existing sealed synthetic metadata
  boundary.

## Relationship To #486 Action And Draft Enrichment

#486 owns broader action and draft surface enrichment inspired by Hollowmark.
This #485 contract must not duplicate #486 action definitions.

Fields deferred to #486 unless separately authorized:

- card played/cast labels beyond existing parser-owned gameplay actions;
- activated ability labels;
- attack/block participation;
- land-drop labels;
- draw-card and drawn-hand reconstruction;
- action sequence or monotonic ordering semantics;
- board snapshots;
- inferred action labels;
- legacy draft shapes not already covered by DraftBot/Human/Complete.

## Synthetic Fixture Requirements

Future synthetic fixtures for Limited capture packets must:

- be Mythic Edge-owned and public-safe;
- state that they are synthetic, not raw `Player.log`;
- contain no private player names, private account identifiers, deck names,
  strategy notes, sealed pools, private draft pools, private card choices, raw
  external logs, or external corpus contents;
- exercise the normal parser path rather than direct object construction when
  claiming parser behavior;
- include expected reduced parser-owned outputs only for the fields claimed;
- include packet-level and field-level non-claims;
- keep draft-only, draft-with-games, sealed-entry, sealed-deckbuild, and
  sealed-match claims separate.

The existing `draft_with_games_synthetic_v1` fixture may be referenced as
single-path reduced evidence for draft event plus limited game/result flow. It
must not be used as proof of complete Limited packet coverage.

## Golden Replay Confirmation Requirements

Golden replay may support stronger-than-schema claims only when all of these
are true:

1. The source fixture is synthetic or separately sanitized and approved.
2. The golden replay manifest names the #485 or #533 contract authority.
3. The expected output includes only public-safe reduced parser-owned fields.
4. The packet fields cite exact repo-relative fixture/manifest refs, not raw
   private paths or raw payloads.
5. Focused tests prove the parser path emits the claimed fields.
6. Codex E review confirms the fixture does not overclaim packet parity,
   analytics truth, AI truth, coaching truth, release readiness, or production
   readiness.

Golden replay confirmation still does not imply private harvest approval,
corpus status changes, #388/#381 activation, or full 17Lands-scale parity.

## Allowed Inputs

Allowed for contract and future public-safe implementation planning:

- current Mythic Edge repo contracts;
- current Mythic Edge parser modules and tests;
- current committed synthetic fixtures and golden replay manifests;
- current corpus manifest/session ledger metadata;
- public GitHub issue and PR metadata;
- public 17Lands repository metadata and category-level field inspiration;
- synthetic public-safe packet examples authored by Mythic Edge;
- already-sanitized public-safe review packets if separately authorized by a
  later contract.

Allowed only in local/private workflows after explicit approval:

- user-selected private `Player.log` or normalized `UTC_Log` windows;
- local-only private capture summaries;
- local-only private review packets;
- symbolic offset-window metadata that contains no raw private paths, hashes,
  lines, or payloads.

## Forbidden Inputs

Forbidden in this contract and any public artifact:

- 17Lands source code;
- 17Lands data or logs;
- Manasight or Hollowmark source code;
- external raw corpus contents;
- raw private `Player.log` or `UTC_Log` lines;
- private app-data contents;
- live MTGA capture output;
- private draft/sealed captures;
- private decklists;
- deck names;
- sealed pools;
- draft pools;
- card choices;
- sideboard choices;
- strategy notes;
- source hashes derived from private content;
- exact private paths;
- raw payload bodies;
- screenshots;
- runtime artifacts;
- SQLite databases;
- workbook exports;
- credentials, tokens, API keys, webhook URLs, or secrets.

## Error Behavior

Future validators or packet builders must fail closed when:

- required top-level packet keys are missing;
- any field lacks provenance metadata;
- `source_ref` contains an absolute local path;
- raw source content appears in a public packet;
- a private source class appears without explicit local-only approval;
- confidence is `high` without `observed` or reviewed `derived` evidence;
- a packet claims fields outside its packet family;
- a packet claims full Limited parity from one synthetic fixture;
- a packet implies draft advice, card-quality truth, archetype truth,
  analytics truth, AI truth, coaching truth, readiness, release, deploy, or
  production claims.

Failure status should be `invalid` or `review_required`, not silent omission.

## Side Effects

Codex B side effects:

- Create `docs/contracts/parser_parity_limited_capture_packet_coverage.md`.

No runtime state, parser output, workbook, webhook, Apps Script, corpus
metadata, fixture, issue, PR, tracker, local artifact, private file, scheduled
job, or external service is changed by this contract.

Future implementation side effects, only if separately authorized, must be
limited to explicit public-safe repo files named by that later issue and
contract.

## Compatibility

Compatibility rules:

- Existing `DraftBot`, `DraftHuman`, and `DraftComplete` event kinds and
  payload fields remain unchanged.
- Existing draft-only, draft-with-games, sealed-entry, sealed-deckbuild, and
  sealed-match corpus rows remain unchanged by this contract.
- Existing workbook schema, webhook payload shape, Apps Script behavior,
  output transport, analytics ingest, local app behavior, AI/model-provider
  behavior, and production behavior remain unchanged.
- Current public synthetic fixture meanings remain bounded by their source
  contracts.

## Tests Required

For this Codex B contract pass:

```bash
git status --short --branch
git diff --check
printf '%s\n' docs/contracts/parser_parity_limited_capture_packet_coverage.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_parity_limited_capture_packet_coverage.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/select_validation.py --base origin/main
```

For a future implementation only if separately authorized:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_limited_capture_packets.py
PYTHONPATH=src python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py
PYTHONPATH=src python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_game_result_parser.py tests/test_state.py
PYTHONPATH=src python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py
git diff --check
```

Future implementation must also run path-scoped secret and protected-surface
checks over every changed path.

## Acceptance Criteria

- The contract file exists at
  `docs/contracts/parser_parity_limited_capture_packet_coverage.md`.
- The contract preserves `parser_behavior_ready=false`,
  `pipeline_activation_ready_for_issue_388=false`,
  `private_harvest_authorized=false`,
  `fixture_promotion_authorized=false`,
  `corpus_status_change_authorized=false`, and
  `implementation_authorized=false`.
- The contract defines Limited packet families and field groups without
  implementing code.
- The contract distinguishes current reduced synthetic draft-with-games
  evidence from full Limited packet parity.
- The contract maps #485 target facts to parser-owned source surfaces or
  deferred/private-gated boundaries.
- The contract defines field-level `value_source`, `confidence`, `finality`,
  degradation, and review-required rules.
- The contract preserves #484, #481, #533, and #486 boundaries.
- The contract forbids external source copying, raw/private logs, private deck
  contents, private card choices, strategy notes, and secrets.
- The contract does not change parser behavior, parser event classes, state
  reconciliation, corpus metadata, fixtures, workbook/webhook/App Script,
  analytics, AI, coaching, CI gates, release, deploy, or production behavior.

## Open Questions And Contract Risks

- Whether #533 should implement draft-session lifecycle before any #485 packet
  schema helper exists.
- Whether future packet builders should live in a new
  `limited_capture_packets.py` module or as parser-owned fact tracker support.
- Whether local-only private captures should ever publish card-list summaries,
  or only counts and symbolic review refs.
- Which exact source surfaces can safely support opponent mulligan count,
  drawn hands, drawn cards, autopick, and time remaining.
- Whether future 17Lands-reference checks should remain issue-text-only or use
  a dedicated public-reference metadata artifact.

## Next Workflow Action

Next role: Codex E, contract review.

Rationale: the current handoff sets `implementation_authorized=false`, so the
next safe step is independent contract review. Codex C implementation should
wait for explicit user authorization after review.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #485.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/485

Parent umbrella:
https://github.com/Tahjali11/Mythic-Edge/issues/483

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/484

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/554

Contract artifact:
docs/contracts/parser_parity_limited_capture_packet_coverage.md

Goal:
Review the #485 limited capture packet coverage contract for correctness,
scope control, protected-surface safety, parser truth ownership, privacy,
field-level provenance, #481/#484/#533/#486 boundary preservation, and false
readiness flags.

Review stance:
Lead with findings ordered by severity. Do not implement fixes. If the
contract is clear and safe, say so and route to Codex F for docs-only
submission. If it overclaims implementation, packet parity, private evidence,
fixture promotion, corpus status changes, parser behavior readiness,
analytics truth, AI truth, coaching truth, or release readiness, route back to
Codex B with concrete findings.

Protected boundaries:
- Do not implement code.
- Do not open a PR.
- Do not close #485, #483, #388, or #434.
- Do not activate #388 or #381.
- Do not run or read private Player.log, UTC_Log, app-data, live MTGA,
  diagnostics, drift, watcher, private smoke, private harvest, draft capture,
  sealed capture, or limited capture evidence.
- Do not import, copy, summarize, hash, or commit 17Lands source code,
  17Lands data, external logs, private logs, private paths, generated private
  artifacts, runtime files, SQLite databases, tokens, credentials, API keys,
  webhook URLs, workbook exports, decklists, card choices, private strategy
  notes, or local-only outputs.
- Do not change parser behavior, parser event classes, parser state final
  reconciliation, router semantics, match/game identity, deduplication,
  workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, analytics behavior, OpenAI/model-provider behavior,
  AI/coaching behavior, CI gates, merge readiness, deploy readiness,
  production behavior, or final integration policy.

Expected output:
- Findings first, if any.
- Contract review summary.
- Validation reviewed or run.
- Recommended next role.
- workflow_handoff block with repository and repository_url.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/485"
  parent_umbrella: "https://github.com/Tahjali11/Mythic-Edge/issues/483"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/484"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/554"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue #485 and Codex A reconciliation comment"
  target_artifact: "docs/contracts/parser_parity_limited_capture_packet_coverage.md"
  verdict: "limited_capture_packet_contract_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/parser-parity-limited-capture-packet-485"
  previous_merge_commit: "3f253f6c887a927e26a973ef92e5222f2db9b785"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
  validation:
    - "git diff --check"
    - "printf '%s\\n' docs/contracts/parser_parity_limited_capture_packet_coverage.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_parity_limited_capture_packet_coverage.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_parity_limited_capture_packet_coverage.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin"
    - "python3 tools/check_agent_docs.py"
  stop_conditions:
    - "Do not implement code unless explicitly authorized after contract review."
    - "Do not activate #388 or #381."
    - "Do not read or run private/live Limited capture evidence."
    - "Do not copy 17Lands source code or import external/private logs."
    - "Do not claim full Limited packet parity, parser_behavior_ready, pipeline activation readiness, private harvest readiness, fixture promotion readiness, corpus status readiness, release readiness, production behavior, analytics truth, AI truth, or coaching truth."
```
