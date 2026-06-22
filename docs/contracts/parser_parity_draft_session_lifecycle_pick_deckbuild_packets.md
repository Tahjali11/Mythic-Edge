# Parser Parity Draft Session Lifecycle And Pick/Deckbuild Packet Contract

## Module

`parser_parity_draft_session_lifecycle_pick_deckbuild_packets`

Plain English: this contract defines the safe parser-owned fact boundary for a
future draft-session lifecycle packet model. A draft-session lifecycle packet
would join observed draft entry/status, pack/pick, draft completion,
deckbuild/submit-deck signal, later match/game linkage, and result context into
reviewable public-safe summaries. The model may describe parser-owned facts and
their provenance, confidence, finality, degradation, and review state, but it
must not become draft advice, card grades, raredrafting value, archetype truth,
analytics truth, AI truth, coaching truth, private-harvest authorization, or
release readiness.

This Codex B pass writes only this contract. It does not implement code, open
a PR, activate #388 or #381, read private logs, run draft capture, create
fixtures, edit corpus metadata, change parser behavior, or claim readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/533
- Parent issue: https://github.com/Tahjali11/Mythic-Edge/issues/485
- Parent umbrella: https://github.com/Tahjali11/Mythic-Edge/issues/483
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/485
- Previous completed PR: https://github.com/Tahjali11/Mythic-Edge/pull/555
- Previous merge commit:
  `37267885d0445e8dcffb54857e41a36a00b6306b`
- Base branch: `main`
- Target branch: `main`
- Contract branch:
  `codex/parser-parity-draft-session-lifecycle-533`
- Risk tier: High

Observed during this Codex B pass:

- The primary checkout had unrelated local modifications and an untracked
  prior contract artifact, so this contract was written in a clean sibling
  worktree.
- The clean worktree was created from `origin/main` at
  `37267885d0445e8dcffb54857e41a36a00b6306b`.
- Issue #533 was open.
- Parent issue #485 was closed and PR #555 was merged.
- Parent umbrella #483 was open.
- Pipeline tracker #388 was open and inactive.
- Parent private-evidence issue #434 was open.
- Issue #486 was open and remains the separate broader action/draft enrichment
  follow-up.

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
- Issue #533
- Parent issue #485 and PR #555 completion comment
- Parent umbrella #483
- Pipeline tracker #388
- Parent private-evidence issue #434
- Issue #486
- Public GitHub metadata for `rconroy293/mtga-log-client`
- `docs/contracts/parser_parity_limited_capture_packet_coverage.md`
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
- `src/mythic_edge_parser/parsers/draft_bot.py`
- `src/mythic_edge_parser/parsers/draft_human.py`
- `src/mythic_edge_parser/parsers/draft_complete.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/event_identity.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
- `tests/fixtures/draft_parser_family_slice.log`
- `tests/fixtures/draft_with_games_synthetic_slice.log`
- `tests/fixtures/golden_replay/draft_with_games_synthetic.manifest.json`
- Focused draft, sealed, state, event identity, corpus parity, golden replay,
  and parser-owned fact tracker tests by inspection.

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

The parser owns normalized draft, deckbuild-signal, match, game, and result
facts. Corpus / Provenance may track field provenance, synthetic fixture
evidence, golden replay confirmation, parser-owned fact tracker progress, and
review status, but corpus metadata does not own parser truth.

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

Truth owner for future draft-session lifecycle and pick/deckbuild packet facts:

- draft event and pick facts:
  - `src/mythic_edge_parser/parsers/draft_bot.py`
  - `src/mythic_edge_parser/parsers/draft_human.py`
  - `src/mythic_edge_parser/parsers/draft_complete.py`
- submitted-deck signal facts:
  - `src/mythic_edge_parser/parsers/client_actions.py`
  - `src/mythic_edge_parser/app/transforms.py`
  - `src/mythic_edge_parser/app/state.py`
- draft/match/game linkage and limited event identity:
  - `src/mythic_edge_parser/parsers/match_state.py`
  - `src/mythic_edge_parser/parsers/gre/game_state.py`
  - `src/mythic_edge_parser/parsers/gre/game_result.py`
  - `src/mythic_edge_parser/app/state.py`
  - `src/mythic_edge_parser/app/event_identity.py`
- coverage and progress tracking:
  - `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
  - future public-safe target rows or reports explicitly authorized by #481,
    #485, or #533 contracts.

This contract does not make public 17Lands surfaces, corpus metadata,
downstream analytics, workbook formulas, dashboard logic, Apps Script, webhook
transport, AI output, or coaching output a truth owner for draft lifecycle
facts.

## Bridge-Code Status

`deferred_future_boundary`

Codex B authorizes no bridge code. If a later pass is explicitly authorized
after review, the allowed data flow is:

```text
parser-owned DraftBot / DraftHuman / DraftComplete / ClientAction / MatchState / GRE facts
  -> field-level source, confidence, finality, and degradation metadata
  -> public-safe draft session lifecycle and pick/deckbuild packet summaries
  -> parser-owned fact tracker coverage progress
  -> optional corpus/golden replay evidence summaries
```

Forbidden reverse flow:

- Draft-session packets must not change parser behavior.
- Parser-owned fact tracker rows must not create parser facts.
- Corpus coverage statuses must not rewrite draft/session/game semantics.
- Public 17Lands category surfaces must not become Mythic Edge parser truth.
- Analytics, AI, workbook, webhook, Apps Script, dashboard, and coaching
  surfaces must not define draft-session lifecycle truth.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_parity_draft_session_lifecycle_pick_deckbuild_packets.md`

Potential future implementation files, only if separately authorized:

- `src/mythic_edge_parser/app/draft_session_lifecycle.py`
- `tests/test_draft_session_lifecycle.py`
- `src/mythic_edge_parser/app/limited_capture_packets.py`, only if #485 and
  #533 are implemented together under a later explicit contract;
- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`, only for
  additive target rows or report references;
- `tests/test_parser_owned_fact_tracker.py`, only for additive public-safe
  tracker fixtures;
- `docs/implementation_handoffs/parser_parity_draft_session_lifecycle_pick_deckbuild_packets_comparison.md`;
- `docs/contract_test_reports/parser_parity_draft_session_lifecycle_pick_deckbuild_packets.md`.

Potential future evidence or coverage files, only if separately authorized:

- synthetic public-safe fixtures under existing fixture directories;
- golden replay fixture/manifest additions after separate fixture-promotion
  authority;
- public-safe parser-owned fact tracker fixture/report files.

Referenced but not behavior-owned by this contract:

- draft parser modules;
- client action parser modules;
- GRE parser modules;
- parser state modules;
- corpus manifest and session ledger;
- workbook/webhook/App Script/output/analytics/AI surfaces.

## Observed Current Behavior

Current draft parser behavior:

- `DraftBot` recognizes `BotDraftDraftStatus` and `BotDraftDraftPick`.
- `DraftHuman` recognizes `Draft.Notify`, `EventPlayerDraftMakePick`, and
  qualifying `LogBusinessEvents` payloads with picked-card evidence.
- `DraftComplete` recognizes `DraftCompleteDraft`.
- Draft payloads may preserve `draft_id`, `event_id`, `draft_status`,
  `pack_number`, `pick_number`, `pack_card_ids`, `picked_card_id`, and
  `picked_card_ids` when source payloads provide those values.
- `DraftComplete` may preserve `draft_id`, `event_id`, `queue_id`,
  `draft_status`, `completion_status`, `draft_type`, `draft_mode`,
  `completion_source`, `is_bot_draft`, and `is_human_draft`.
- Draft parsers preserve parsed raw draft payloads inside event payloads.
- There is no current canonical draft-session lifecycle object, no canonical
  draft-session ID, no pick sequence continuity validator, and no built-in
  draft-to-match joiner.

Current deckbuild and match behavior:

- `ClientAction` recognizes `ClientMessageType_SubmitDeckResp` and normalizes
  `deck_cards` and `sideboard_cards`.
- `state.py` and `transforms.py` treat submit-deck responses as a
  `submit_deck_seen` signal.
- Match summaries and workbook rows expose `MTGA Submit Deck Seen`, but they do
  not expose raw deck cards or sideboard cards.
- `event_identity.py` classifies limited, draft, sealed, premier draft,
  traditional draft, quick draft, and related event families from parser-owned
  event IDs and match metadata.
- Match/game linkage comes from `MatchState`, GRE `GameState`, GRE
  `GameResult`, and parser state final reconciliation.

Current corpus/replay behavior:

- `draft_parser_family_slice.log` is a synthetic draft parser-family fixture
  with bot draft, human draft, draft complete, and one GameState anchor.
- `draft_with_games_synthetic_slice.log` is a reduced synthetic
  draft-with-games fixture with `DraftBot`, `DraftComplete`, `MatchState`,
  `GameState`, and `GameResult`.
- The draft-with-games golden replay manifest proves one reduced synthetic
  draft event plus limited game/result path. It does not prove all draft
  queues, BO3 draft, sideboarding, deck construction, draft picks across a
  complete draft, card pools, submitted decklists, archetypes, analytics truth,
  AI truth, coaching truth, release readiness, or production behavior.

Current #485 behavior:

- `docs/contracts/parser_parity_limited_capture_packet_coverage.md` defines
  broad Limited packet family vocabulary.
- #485 explicitly defers canonical draft-session ID construction, joining draft
  IDs to match IDs, pack/pick sequence continuity, deckbuild lifecycle
  transitions, card-pool/submitted-deck public-safe summary rules, and draft
  queue lifecycle differences to #533.

## Problem Statement

Mythic Edge has individual parser-owned draft event facts, submit-deck signals,
limited match/game facts, and a broad Limited packet contract. What is missing
is a narrow lifecycle model that explains how those facts may be joined safely.

Without this contract, future work could accidentally:

- treat `draft_id`, `event_id`, or `match_id` alone as a complete draft session;
- join draft picks, deckbuild, and matches without field-level provenance;
- publish private decklists, card choices, sealed pools, or strategy notes;
- treat a submit-deck response as decklist truth;
- treat a single synthetic draft-with-games fixture as full draft lifecycle
  coverage;
- copy or mimic external parser source;
- move draft advice, card grades, archetype labels, or analytics into parser
  truth;
- promote #388/#381, private harvest, fixture promotion, or corpus status
  changes without approval.

## First Bad Value

The first bad value is any draft-session lifecycle field, pick packet,
deckbuild packet, match-link packet, parser-owned fact tracker row, corpus
report, golden replay expectation, review packet, implementation handoff, or
next-role prompt that treats existing draft parser events, submit-deck
responses, synthetic draft-with-games coverage, sealed synthetic metadata,
public 17Lands category references, or private evidence plans as any of the
following:

- full draft-session lifecycle support;
- parser support for every #533 candidate lifecycle field;
- complete pick sequence truth;
- complete draft pool or sealed pool truth;
- submitted decklist truth;
- private-harvest authorization;
- fixture-promotion readiness;
- corpus status readiness;
- parser behavior readiness;
- #388 or #381 activation readiness;
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

- draft-session lifecycle packet families;
- current source coverage state;
- canonical session ID and join-confidence rules;
- pick packet and deckbuild packet public-safe shapes;
- field-level provenance, confidence, finality, degradation, and review rules;
- allowed and forbidden inputs;
- how current synthetic fixtures may be referenced without overclaiming;
- how #481, #485, and #486 relate to this lane.

This contract does not approve an immediate Codex C implementation because the
current handoff sets `implementation_authorized=false`.

After Codex E review and explicit user authorization, a later implementation
may choose one of these narrow paths:

1. `schema_and_validator_only`: add an in-memory/public-safe lifecycle packet
   schema and validator with synthetic test payloads only.
2. `synthetic_fixture_lifecycle_projection`: project fields from existing
   committed synthetic draft fixtures into reduced lifecycle summaries without
   changing parser behavior or corpus statuses.
3. `route_to_486_first`: defer broader draft/action enrichment when lifecycle
   packet modeling depends on action streams, board snapshots, drawn cards, or
   legacy draft shapes outside #533.

If Codex C cannot keep the implementation public-safe, additive, and
non-authoritative, it must stop and route back to Codex B or Codex A.

## Packet Families

V1 packet family vocabulary:

| Packet family | Purpose | Current status |
| --- | --- | --- |
| `draft_session_lifecycle_packet` | Session identity, event/course context, draft mode, lifecycle phases, and match linkage. | Contract-only; no unified lifecycle object exists. |
| `draft_pick_packet` | One observed pack/pick point with pack number, pick number, available-card IDs, selected-card ID, method, and provenance. | Partially sourced by DraftBot/Human event payloads; no sequence validator. |
| `draft_pick_sequence_summary` | Public-safe aggregate of pick count, first/last observed pick, gaps, conflicts, and queue/mode context. | Contract-only; no complete draft sequence claim. |
| `draft_deckbuild_packet` | Submit-deck/deckbuild signal, deck card count summary, sideboard count summary, and redacted card-list policy. | Submit-deck signal exists; public card-list summaries are gated. |
| `draft_match_link_packet` | Link from draft session to match ID, game number, event ID, queue identity, and result context. | Partially sourced by synthetic fixtures and parser state; join confidence must be explicit. |
| `draft_lifecycle_provenance_summary` | Packet-level source refs, confidence, finality, degradation, review status, and non-claims. | New contract vocabulary only. |

The packet family names are contract vocabulary. They do not create public
Python APIs until a later implementation is explicitly authorized.

## In-Scope And Deferred Fields

| Field group | Current likely source | #533 V1 decision |
| --- | --- | --- |
| draft ID | DraftBot/Human/Complete payloads | In schema; optional; observed only when present. |
| canonical draft session ID | Derived from public-safe observed IDs or symbolic refs | In schema; never high confidence from one weak key alone. |
| course/event ID | Draft payload aliases and match/event identity | In schema; distinguish draft event ID from match event ID. |
| event name | Draft payload aliases and event identity | In schema; not archetype or queue truth by itself. |
| draft mode/type | DraftComplete payload and source method | In schema; optional; bot/human/unknown only when observed or reviewed. |
| lifecycle phase | Draft status/completion, submit-deck signal, match state, result | In schema; phase confidence must cite source fields. |
| pack number | DraftBot/Human payloads | In schema; optional; preserve observed index without reinterpretation. |
| pick number | DraftBot/Human payloads | In schema; optional; preserve observed index without reinterpretation. |
| available cards in pack | DraftBot/Human `pack_card_ids` | In schema; public committed values synthetic only unless separately sanitized. |
| selected/picked card | DraftBot/Human `picked_card_id` / `picked_card_ids` | In schema; public committed values synthetic only unless separately sanitized. |
| pick sequence continuity | Derived from ordered pick packets | In schema; reports gaps/conflicts only, no complete-draft claim by default. |
| autopick | Not current first-class Mythic Edge field | Deferred until source evidence is identified and contracted. |
| time remaining | Not current first-class Mythic Edge field | Deferred until source evidence is identified and contracted. |
| draft seats / pod context | Not current first-class Mythic Edge field | Deferred or review-required unless explicitly observed in a future source. |
| card pool | Not safe from current public evidence | Deferred/private-gated; public reports may use counts or symbolic refs only. |
| submitted limited deck | `SubmitDeckResp` signal and future summary policy | Signal in schema; card-list content private-gated except synthetic values. |
| maindeck / sideboard counts | `SubmitDeckResp` normalized lists | Counts may be public-safe for synthetic or approved sanitized summaries. |
| maindeck / sideboard card IDs | `SubmitDeckResp` normalized lists | Forbidden in public artifacts unless synthetic or separately sanitized/approved. |
| companion / command-zone | Submitted deck or game-state signals where observed | Deferred until explicit source mapping and synthetic fixtures exist. |
| match ID | MatchState/GRE/parser state | In schema as match-link field; does not prove draft session by itself. |
| game number | GRE/parser state | In schema as match-link field. |
| event ID after draft | MatchState/parser state | In schema; distinguish from draft/course IDs. |
| game result / match result | GRE game result/parser state | In schema as result context; finality depends on parser reconciliation. |
| Premier Draft | Draft event ID/mode and event identity | Priority V1 queue family. |
| Traditional Draft | Draft event ID/mode and event identity | Priority V1 queue family; no BO3 sideboard claim without evidence. |
| Quick Draft / bot draft | DraftBot/Complete and event identity | Allowed V1 queue family because current synthetic evidence exists. |
| Sealed deckbuild | Submit-deck signal plus sealed context | Reference boundary only; reuse sealed contracts and avoid decklist/pool truth. |

## Lifecycle Phase Vocabulary

Allowed `lifecycle_phase` values:

- `unknown`
- `draft_entered`
- `draft_pack_seen`
- `draft_pick_recorded`
- `draft_completed`
- `deckbuild_started`
- `submit_deck_seen`
- `match_linked`
- `game_started`
- `game_completed`
- `match_completed`
- `review_required`
- `degraded`

Rules:

- A lifecycle packet may include multiple phase observations.
- Phase order must be explicit and source-backed.
- Missing phases must stay missing; validators must not synthesize them.
- `submit_deck_seen` is a signal, not submitted deck truth.
- `match_linked` requires a `draft_match_link_packet`, not just a shared event
  name.
- `game_completed` and `match_completed` require parser state or GRE result
  evidence.

## Join Confidence Rules

Allowed `join_confidence` values:

- `high`: direct shared parser-owned identifier or reviewed synthetic fixture
  path proves the join for the claimed fields.
- `medium`: multiple parser-owned fields and lifecycle order support the join,
  but one direct identifier is absent.
- `low`: weak or partial metadata suggests a join but requires review.
- `unknown`: no safe join evidence.
- `conflict`: candidate join evidence disagrees.
- `review_required`: human/Codex review is required before using the join.

Join rules:

- `draft_id` alone may identify draft-event packets, but it does not prove later
  match linkage by itself.
- `event_id` or `event_name` alone must not create a high-confidence session
  join.
- `match_id` alone must not prove draft-session identity.
- Time ordering alone must be `low` or `review_required`.
- A committed synthetic fixture may support `high` only for the exact synthetic
  fields included in that fixture and manifest.
- A private local window may support only local/private review status unless a
  later approved workflow produces a sanitized public summary.
- Conflicting draft IDs, event IDs, queue IDs, or match IDs must produce
  `conflict` or `review_required`.

## Normalized Lifecycle Packet Shape

A future packet, if separately authorized, must be public-safe and
field-provenance-first:

```yaml
object: "mythic_edge_draft_session_lifecycle_packet"
schema_version: "parser_parity_draft_session_lifecycle_packet.v1"
packet_id: "synthetic-or-symbolic-public-safe-id"
source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/533"
parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/485"
parent_umbrella: "https://github.com/Tahjali11/Mythic-Edge/issues/483"
pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
source_refs:
  - "repo-relative-fixture-or-symbolic-review-ref"
draft_session_id: "synthetic-draft-with-games-1"
draft_session_id_status: "synthetic_public_id"
queue_family: "quick_draft|premier_draft|traditional_draft|sealed|unknown"
lifecycle_status: "synthetic_lifecycle_packet_ready"
phase_observations: []
pick_packets: []
pick_sequence_summary: {}
deckbuild_packet: {}
match_links: []
field_provenance: {}
non_claims:
  - "not_full_draft_session_lifecycle_support"
  - "not_private_harvest_authorization"
```

Required top-level fields:

- `object`
- `schema_version`
- `packet_id`
- `source_issue`
- `parent_issue`
- `parent_umbrella`
- `pipeline_tracker`
- `source_refs`
- `draft_session_id`
- `draft_session_id_status`
- `queue_family`
- `lifecycle_status`
- `phase_observations`
- `pick_packets`
- `pick_sequence_summary`
- `deckbuild_packet`
- `match_links`
- `field_provenance`
- `non_claims`

Public packet artifacts must not include raw log lines, raw payload bodies,
private paths, private hashes, source-byte offsets, deck names, private
decklists, sealed pools, private card choices, private strategy notes, or
external corpus contents.

## Draft Pick Packet Shape

Each future `draft_pick_packet` must be public-safe:

```yaml
object: "mythic_edge_draft_pick_packet"
schema_version: "parser_parity_draft_pick_packet.v1"
pick_packet_id: "synthetic-draft-with-games-1.pick.1"
draft_session_id: "synthetic-draft-with-games-1"
source_event_kind: "DraftBot|DraftHuman"
source_method: "BotDraftDraftStatus|BotDraftDraftPick|Draft.Notify|EventPlayerDraftMakePick|LogBusinessEvents"
api_direction: "request|response|unknown"
pack_number:
  value: 1
  value_source: "observed"
  confidence: "high"
  finality: "stable"
  source_ref: "repo-relative-fixture-ref"
pick_number:
  value: 1
  value_source: "observed"
  confidence: "high"
  finality: "stable"
  source_ref: "repo-relative-fixture-ref"
available_card_ids:
  value: [1001, 1002, 1003]
  public_value_policy: "synthetic_only"
selected_card_id:
  value: 1001
  public_value_policy: "synthetic_only"
degradation_flags: []
review_required: false
non_claims:
  - "not_pick_advice"
  - "not_card_quality_truth"
```

Rules:

- `available_card_ids` and `selected_card_id` may be committed only when they
  are synthetic or separately sanitized/approved.
- A pick packet may include counts without card IDs when card IDs are
  private-gated.
- Pack and pick numbering must preserve source evidence and avoid
  zero-based/one-based reinterpretation unless a future contract proves the
  transformation.
- A pick packet must not label the pick as correct, incorrect, forced,
  raredraft, signal, archetype, or best pick.

## Draft Deckbuild Packet Shape

Each future `draft_deckbuild_packet` must be public-safe:

```yaml
object: "mythic_edge_draft_deckbuild_packet"
schema_version: "parser_parity_draft_deckbuild_packet.v1"
deckbuild_packet_id: "synthetic-draft-with-games-1.deckbuild"
draft_session_id: "synthetic-draft-with-games-1"
submit_deck_seen:
  value: true
  value_source: "observed"
  confidence: "high"
  finality: "stable"
deck_main_count:
  value: 40
  value_source: "derived"
  confidence: "medium"
  finality: "stable"
deck_sideboard_count:
  value: 5
  value_source: "derived"
  confidence: "medium"
  finality: "stable"
deck_card_ids_policy: "synthetic_only|private_gated|redacted_counts_only|not_available"
sideboard_card_ids_policy: "synthetic_only|private_gated|redacted_counts_only|not_available"
degradation_flags: []
review_required: false
non_claims:
  - "not_decklist_truth"
  - "not_card_pool_truth"
```

Rules:

- `submit_deck_seen` may be parser-owned signal evidence.
- Submit-deck card lists are sensitive card-content evidence.
- Public artifacts may include card IDs only for synthetic or separately
  sanitized/approved evidence.
- Private decklists, deck names, sealed pools, draft pools, sideboard choices,
  and strategy notes must not be committed.
- Counts may be public-safe only when they do not expose private deck
  construction in a way forbidden by the current issue/contract.
- Deckbuild packets must not label deck quality, archetype, synergy, mana
  quality, sideboard correctness, or pick/deck construction quality.

## Draft Match Link Packet Shape

Each future `draft_match_link_packet` must be public-safe:

```yaml
object: "mythic_edge_draft_match_link_packet"
schema_version: "parser_parity_draft_match_link_packet.v1"
match_link_packet_id: "synthetic-draft-with-games-1.match.1"
draft_session_id: "synthetic-draft-with-games-1"
match_id: "synthetic-draft-with-games-match-1"
match_event_id: "Event_Limited_Draft_Synthetic"
game_numbers: [1]
queue_family: "quick_draft"
join_confidence: "high"
join_basis:
  - "same_synthetic_fixture"
  - "ordered_draft_complete_before_match_state"
result_context:
  match_result: "W"
  game_results:
    - game_number: 1
      result: "W"
degradation_flags: []
review_required: false
non_claims:
  - "not_full_limited_match_parity"
```

Rules:

- Match linkage must cite parser-owned source refs.
- Event family, queue family, and rank context are metadata, not skill or
  matchmaking truth.
- Result context is parser/state truth only for the fields normally owned by
  parser state and final reconciliation.
- Match linkage does not imply complete draft picks, complete deckbuild,
  hidden cards, deck quality, or gameplay advice.

## Status Vocabulary

Allowed `lifecycle_status` values:

- `contract_only`
- `schema_ready`
- `synthetic_lifecycle_packet_ready`
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
- any status directly to `full_draft_lifecycle_parity`;
- any status directly to `draft_advice_ready` or equivalent downstream
  coaching language.

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
- `pick_sequence_gap`
- `pick_sequence_conflict`
- `deckbuild_signal_only`
- `deck_contents_redacted`
- `private_evidence_redacted`
- `external_reference_only`
- `synthetic_only`
- `review_required`

## Relationship To #485 Limited Capture Packet Coverage

#485 defines the broad Limited packet vocabulary. This #533 contract refines
these #485 packet families:

- `limited_session_packet` becomes `draft_session_lifecycle_packet` for draft
  and draft-like sessions;
- `limited_pick_packet` becomes `draft_pick_packet` plus
  `draft_pick_sequence_summary`;
- `limited_deckbuild_packet` becomes `draft_deckbuild_packet` with explicit
  public/private card-content policy;
- `limited_match_packet` contributes to `draft_match_link_packet`;
- `limited_packet_provenance_summary` remains the shared provenance model.

#533 does not replace #485. It narrows the lifecycle and join rules needed
before future code can safely build draft-session packets.

## Relationship To #481 Parser-Owned Fact Tracker

#481 owns metadata-only target matrices, local session ledgers, and coverage
progress reports. This contract may contribute future target fact rows, but it
does not add them now.

Recommended future fact families:

- `limited.draft_session_identity`
- `limited.draft_lifecycle_phase`
- `limited.draft_pick_packet`
- `limited.draft_pick_sequence`
- `limited.draft_deckbuild_signal`
- `limited.draft_match_link`
- `limited.draft_result_context`

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
`review_required`, `synthetic_lifecycle_packet_ready`,
`private_evidence_blocked`, or `external_reference_only` according to
evidence. A tracker row must not become `promoted_golden_fixture` without
review, proof, draft fixture/manifest metadata, and explicit
fixture-promotion authority.

## Relationship To #486 Action And Draft Enrichment

#486 owns broader action and draft surface enrichment inspired by Hollowmark.
This #533 contract must not duplicate #486 action definitions.

Fields deferred to #486 unless separately authorized:

- legacy draft shapes not already covered by DraftBot/Human/Complete;
- wrapped `CurrentModule: BotDraft` or JSON-string payload forms not already
  parser-owned;
- action streams;
- board snapshots;
- draw records;
- action sequence or monotonic ordering semantics beyond pick sequence
  bookkeeping;
- card played/cast labels;
- activated ability labels;
- attack/block participation;
- inferred action labels.

## Synthetic Fixture Requirements

Future synthetic fixtures for #533 must:

- be Mythic Edge-owned and public-safe;
- state that they are synthetic, not raw `Player.log`;
- contain no private player names, private account identifiers, deck names,
  strategy notes, sealed pools, private draft pools, private card choices, raw
  external logs, or external corpus contents;
- exercise the normal parser path rather than direct object construction when
  claiming parser behavior;
- include expected reduced parser-owned outputs only for the fields claimed;
- include packet-level and field-level non-claims;
- keep draft-only, draft-with-games, pick-sequence, deckbuild-signal, sealed
  entry, sealed-deckbuild, and sealed-match claims separate.

The existing `draft_with_games_synthetic_v1` fixture may be referenced as
single-path reduced evidence for draft event plus limited game/result flow. It
must not be used as proof of complete draft-session lifecycle coverage.

## Golden Replay Confirmation Requirements

Golden replay may support stronger-than-schema claims only when all of these
are true:

1. The source fixture is synthetic or separately sanitized and approved.
2. The golden replay manifest names the #533 contract authority.
3. The expected output includes only public-safe reduced parser-owned fields.
4. The packet fields cite exact repo-relative fixture/manifest refs, not raw
   private paths or raw payloads.
5. Focused tests prove the parser path emits the claimed fields.
6. Codex E review confirms the fixture does not overclaim lifecycle parity,
   decklist truth, pick advice, analytics truth, AI truth, coaching truth,
   release readiness, or production readiness.

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
- synthetic public-safe lifecycle packet examples authored by Mythic Edge;
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
- a lifecycle packet claims high-confidence match linkage from event ID alone;
- a pick packet claims complete sequence coverage with missing or conflicting
  pick numbers;
- a deckbuild packet includes private card IDs, deck names, decklists, sealed
  pools, draft pools, or strategy notes;
- a packet claims full draft lifecycle parity from one synthetic fixture;
- a packet implies draft advice, card-quality truth, archetype truth,
  analytics truth, AI truth, coaching truth, readiness, release, deploy, or
  production claims.

Failure status should be `invalid` or `review_required`, not silent omission.

## Side Effects

Codex B side effects:

- Create
  `docs/contracts/parser_parity_draft_session_lifecycle_pick_deckbuild_packets.md`.

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
- Existing `ClientAction` submit-deck payload behavior remains unchanged.
- Existing state behavior that records `submit_deck_seen` without exposing
  deck card lists remains unchanged.
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
printf '%s\n' docs/contracts/parser_parity_draft_session_lifecycle_pick_deckbuild_packets.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_parity_draft_session_lifecycle_pick_deckbuild_packets.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_parity_draft_session_lifecycle_pick_deckbuild_packets.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
python3 tools/check_agent_docs.py
```

For a future implementation only if separately authorized:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_draft_session_lifecycle.py
PYTHONPATH=src python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py
PYTHONPATH=src python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_game_result_parser.py tests/test_state.py
PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py
git diff --check
```

Future implementation must also run path-scoped secret and protected-surface
checks over every changed path.

## Acceptance Criteria

- The contract file exists at
  `docs/contracts/parser_parity_draft_session_lifecycle_pick_deckbuild_packets.md`.
- The contract preserves `parser_behavior_ready=false`,
  `pipeline_activation_ready_for_issue_388=false`,
  `private_harvest_authorized=false`,
  `fixture_promotion_authorized=false`,
  `corpus_status_change_authorized=false`, and
  `implementation_authorized=false`.
- The contract defines draft-session lifecycle, pick, deckbuild, and match-link
  packet families without implementing code.
- The contract distinguishes existing draft parser events and reduced
  draft-with-games synthetic evidence from full draft-session lifecycle
  support.
- The contract defines join-confidence rules that prevent event ID, match ID,
  or time ordering from becoming high-confidence lifecycle truth by itself.
- The contract defines public-safe card-content policy for pick and deckbuild
  packets.
- The contract defines field-level `value_source`, `confidence`, `finality`,
  degradation, and review-required rules.
- The contract preserves #485, #481, and #486 boundaries.
- The contract forbids external source copying, raw/private logs, private deck
  contents, private card choices, strategy notes, and secrets.
- The contract does not change parser behavior, parser event classes, state
  reconciliation, corpus metadata, fixtures, workbook/webhook/App Script,
  analytics, AI, coaching, CI gates, release, deploy, or production behavior.

## Open Questions And Contract Risks

- Whether future implementation should live in a dedicated
  `draft_session_lifecycle.py` module or inside the broader #485
  `limited_capture_packets.py` helper.
- Whether future lifecycle projection should start from existing synthetic
  draft fixtures or wait for a dedicated pick-sequence fixture.
- Which exact source surfaces can safely support autopick, time remaining,
  draft seats, pod context, opponent mulligan counts, and complete deckbuild
  transitions.
- Whether local-only private captures should ever publish card-list summaries,
  or only counts and symbolic review refs.
- Whether Sealed deckbuild should remain governed entirely by the sealed
  contracts or share the `draft_deckbuild_packet` redaction vocabulary later.

## Next Workflow Action

Next role: Codex E, contract review.

Rationale: the current handoff sets `implementation_authorized=false`, so the
next safe step is independent contract review. Codex C implementation should
wait for explicit user authorization after review.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #533.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/533

Parent issue:
https://github.com/Tahjali11/Mythic-Edge/issues/485

Parent umbrella:
https://github.com/Tahjali11/Mythic-Edge/issues/483

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous completed issue:
https://github.com/Tahjali11/Mythic-Edge/issues/485

Previous completed PR:
https://github.com/Tahjali11/Mythic-Edge/pull/555

Contract artifact:
docs/contracts/parser_parity_draft_session_lifecycle_pick_deckbuild_packets.md

Goal:
Review the #533 draft-session lifecycle and pick/deckbuild packet contract for
correctness, scope control, protected-surface safety, parser truth ownership,
privacy, field-level provenance, lifecycle join confidence, #481/#485/#486
boundary preservation, and false readiness flags.

Review stance:
Lead with findings ordered by severity. Do not implement fixes. If the
contract is clear and safe, say so and route to Codex F for docs-only
submission. If it overclaims implementation, full lifecycle parity, private
evidence, fixture promotion, corpus status changes, parser behavior readiness,
draft advice, decklist truth, analytics truth, AI truth, coaching truth, or
release readiness, route back to Codex B with concrete findings.

Protected boundaries:
- Do not implement code.
- Do not open a PR.
- Do not close #533, #485, #483, #388, or #434.
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/533"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/485"
  parent_umbrella: "https://github.com/Tahjali11/Mythic-Edge/issues/483"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/485"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/555"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue #533 and #485 merge handoff"
  target_artifact: "docs/contracts/parser_parity_draft_session_lifecycle_pick_deckbuild_packets.md"
  verdict: "draft_session_lifecycle_pick_deckbuild_packet_contract_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/parser-parity-draft-session-lifecycle-533"
  previous_merge_commit: "37267885d0445e8dcffb54857e41a36a00b6306b"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
  validation:
    - "git diff --check"
    - "printf '%s\\n' docs/contracts/parser_parity_draft_session_lifecycle_pick_deckbuild_packets.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_parity_draft_session_lifecycle_pick_deckbuild_packets.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_parity_draft_session_lifecycle_pick_deckbuild_packets.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin"
    - "python3 tools/check_agent_docs.py"
  stop_conditions:
    - "Do not implement code unless explicitly authorized after contract review."
    - "Do not activate #388 or #381."
    - "Do not read or run private/live draft, sealed, or limited capture evidence."
    - "Do not copy 17Lands source code or import external/private logs."
    - "Do not commit private decklists, card choices, sealed pools, draft pools, strategy notes, private paths, raw payload bodies, generated artifacts, SQLite files, workbook exports, credentials, tokens, API keys, or webhook URLs."
    - "Do not claim full draft-session lifecycle support, full Limited packet parity, parser_behavior_ready, pipeline activation readiness, private harvest readiness, fixture promotion readiness, corpus status readiness, release readiness, production behavior, analytics truth, AI truth, or coaching truth."
```
