# Player.log Evidence Ledger Contract

GitHub issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Problem representation: `docs/problem_representations/player_log_evidence_ledger.md`

Agent docs:

- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Branch target: `codex/parser-module-audit-suite`

This contract defines the v1 design for a Player.log evidence ledger. It is a
contract artifact only. It does not implement behavior changes, change workbook
schema, change webhook payload shape, commit raw local logs, or move parser
truth downstream.

## Module

Player.log evidence ledger.

Recommended future implementation modules, subject to this contract:

- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/schema_snapshot.py`
- `src/mythic_edge_parser/app/drift_report.py`
- `src/mythic_edge_parser/app/invariants.py`

The ledger maps business-critical parser-managed outputs to the raw Player.log
signals that support them. It also defines value-source labels, confidence
labels, finality labels, drift flags, invariant checks, degradation behavior,
and validation requirements.

This contract uses Tier 0 for evidence metadata plus output tiers 1 through 7
from the problem representation.

Plain English: the ledger is an evidence map and warning system. It should help
the parser say "this value came from this log signal, with this confidence" and
"this value degraded because the expected signal disappeared." It must not
become a second parser or a workbook formula workaround.

## Owning Layer

Primary truth layer: parser and state interpretation.

Supporting layers:

- MTGA raw log source as the only local observable evidence source.
- Runtime diagnostics and status surfaces as reporting surfaces.
- Workbook landing sheets, helper formulas, dashboards, and analytics as
  consumers only.

Truth boundary:

- Player.log is evidence, not absolute game truth.
- `state.py`, `models.py`, and parser support modules own interpretation of
  Player.log evidence into parser-managed facts.
- The evidence ledger describes and audits that interpretation. It must not own
  match result, game result, play/draw, mulligan count, opening hand, deck
  submission, card action, workbook schema, or webhook identity.
- AI, workbook formulas, dashboard calculations, and Apps Script transport must
  not overwrite parser-owned truth.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/player_log_evidence_ledger.md`

Future implementation files owned by this contract:

- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/schema_snapshot.py`
- `src/mythic_edge_parser/app/drift_report.py`
- `src/mythic_edge_parser/app/invariants.py`

Files whose outputs and behavior the ledger must reference but not silently
change:

- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `src/mythic_edge_parser/app/event_identity.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/card_performance.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/parsers/`
- `tools/google_apps_script/Code.gs`

Required future tests:

- `tests/test_evidence_ledger.py`
- `tests/test_schema_snapshot.py`
- `tests/test_drift_report.py`
- `tests/test_invariants.py`

Existing tests that should remain part of the validation slice:

- `tests/test_app_models.py`
- `tests/test_sheet_schema.py`
- `tests/test_state.py`
- `tests/test_app_extractors.py`
- `tests/test_parser_regressions.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_gameplay_actions.py`

## Public Interface

The v1 public interface is structured metadata. Exact names may be implemented
as dataclasses, typed dictionaries, JSON schema, or constants, but the shapes
below are the contract that other code may depend on.

### Ledger Definition

Required logical shape:

```yaml
ledger:
  object: "mythic_edge_player_log_evidence_ledger"
  ledger_version: "player_log_evidence_ledger.v1"
  parser_contract_version: "v1"
  entries:
    - ledger_entry
```

V1 decision: the source of truth for ledger definitions should be a structured
machine-readable artifact owned by code, with this Markdown file as the human
contract. A later implementation may choose Python dataclasses plus JSON export,
or YAML/JSON plus loader functions, but it must preserve the logical shape in
this section.

### Ledger Entry

Required logical shape:

```yaml
ledger_entry:
  tier: 1
  output_family: "match_identity"
  output_field: "MTGA Match ID"
  parser_owner: "src/mythic_edge_parser/app/state.py"
  model_surface: "MatchSummary.to_match_log_row"
  downstream_surfaces:
    - "Match Log"
    - "match_history"
  parser_managed_truth: true
  direct_evidence:
    - evidence_signal
  fallback_evidence:
    - evidence_signal
  value_source_policy:
    direct: "observed"
    fallback: "derived"
    missing: "unknown"
    contradiction: "conflict"
    historical: "legacy_enriched"
  confidence_policy:
    direct: "high"
    fallback: "medium"
    weak_fallback: "low"
    missing: "unknown"
    contradiction: "low"
  finality_policy:
    live: "live"
    pre_result: "provisional"
    result_seen: "final"
    corrected_by_later_evidence: "reconciled"
  invariant_checks:
    - "stable_match_id_required"
  degradation_behavior:
    - "block final match-level row identity when match_id is missing"
  drift_flags:
    - "missing_expected_payload_path"
  recommended_review_modules:
    - "src/mythic_edge_parser/app/state.py"
  tests:
    - "tests/test_state.py"
```

Required entry fields:

- `tier`
- `output_family`
- `output_field`
- `parser_owner`
- `model_surface`
- `downstream_surfaces`
- `parser_managed_truth`
- `direct_evidence`
- `fallback_evidence`
- `value_source_policy`
- `confidence_policy`
- `finality_policy`
- `invariant_checks`
- `degradation_behavior`
- `drift_flags`
- `recommended_review_modules`
- `tests`

### Evidence Signal

Required logical shape:

```yaml
evidence_signal:
  signal_id: "game_result.gre_game_state.results.winning_team"
  parser_event_kind: "GameResult"
  raw_event_family: "greToClientEvent"
  raw_message_type: "GREMessageType_GameStateMessage"
  normalized_payload_path: "payload.results[].winningTeamId"
  raw_payload_path: "greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId"
  required_for_final: true
  value_source_when_used: "observed"
  confidence_when_used: "high"
  finality_when_used: "final"
  allowed_types:
    - "int"
    - "str-int"
  missing_behavior: "mark game winner unknown"
```

Required evidence fields:

- `signal_id`
- `parser_event_kind`
- `raw_event_family`
- `raw_message_type`
- `normalized_payload_path`
- `raw_payload_path`
- `required_for_final`
- `value_source_when_used`
- `confidence_when_used`
- `finality_when_used`
- `allowed_types`
- `missing_behavior`

### Field Evidence Result

Runtime metadata produced by future implementation should use this logical
shape. V1 should keep this metadata internal to diagnostics, status, drift
reports, JSON artifacts, or tests unless a later contract explicitly approves
workbook/webhook shape changes.

```yaml
field_evidence:
  output_family: "game_level_facts"
  output_field: "Game Result"
  value_source: "observed"
  confidence: "high"
  finality: "final"
  source_event_kind: "GameResult"
  source_event_type: "game_result"
  source_payload_paths:
    - "payload.results[].winningTeamId"
  source_event_timestamp: "2026-05-12T12:00:00+00:00"
  drift_flags: []
  invariant_status: "passed"
  degraded_reason: ""
  review_required: false
```

Required result fields:

- `output_family`
- `output_field`
- `value_source`
- `confidence`
- `finality`
- `source_event_kind`
- `source_event_type`
- `source_payload_paths`
- `source_event_timestamp`
- `drift_flags`
- `invariant_status`
- `degraded_reason`
- `review_required`

### Schema Snapshot

Required logical shape:

```yaml
schema_snapshot:
  object: "mythic_edge_player_log_schema_snapshot"
  schema_snapshot_id: "sha256-or-stable-id"
  parser_version: ""
  parser_commit_sha: ""
  generated_at: ""
  fixture_ids:
    - "bo3_match_win_redacted"
  observed_event_families:
    - "matchGameRoomStateChangedEvent"
    - "greToClientEvent"
  observed_payload_paths:
    - path: "greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId"
      observed_types: ["int"]
      sample_count: 3
      redacted: false
```

The schema snapshot must not contain raw unredacted local logs, secrets, webhook
URLs, account tokens, or sensitive player identity fields.

### Drift Report

Required logical shape:

```yaml
drift_report:
  object: "mythic_edge_player_log_drift_report"
  generated_at: ""
  parser_version: ""
  parser_commit_sha: ""
  ledger_version: "player_log_evidence_ledger.v1"
  schema_snapshot_compared: ""
  observed_event_families: []
  missing_expected_event_families: []
  missing_expected_payload_paths: []
  changed_signal_types: []
  new_unknown_signals: []
  affected_outputs: []
  output_confidence_downgrades: []
  invariant_failures: []
  fallback_paths_used: []
  unrecoverable_facts: []
  recommended_review_modules: []
  recommended_github_issue_titles: []
```

## Label Vocabulary

### Value Source

- `observed`: directly read from current Player.log evidence.
- `derived`: computed from multiple observed facts without guessing.
- `inferred`: best-effort fallback from indirect evidence.
- `unknown`: unavailable or not safely recoverable.
- `conflict`: multiple evidence paths disagree.
- `legacy_enriched`: enriched from older retained metadata that is not currently
  emitted by current Player.log evidence.

Required ordering when multiple labels could apply:

1. `conflict`
2. `unknown`
3. `legacy_enriched`
4. `inferred`
5. `derived`
6. `observed`

### Confidence

- `high`: directly observed or derived from stable observed facts.
- `medium`: inferred or derived from a known fallback with strong support.
- `low`: inferred from weak, incomplete, or conflicting support.
- `unknown`: no trustworthy evidence.

Derived analytics must inherit the lowest confidence of their required
ingredients unless a metric explicitly excludes weak ingredients.

### Finality

- `live`: still updating during active parsing.
- `provisional`: likely but not reconciled against final result evidence.
- `final`: emitted after final result evidence.
- `reconciled`: a final value updated by later stronger evidence.

Finality does not imply high confidence. A value can be final but unknown or
final but low confidence.

### Drift Flags

V1 drift flags:

- `missing_expected_event_family`
- `missing_expected_payload_path`
- `changed_signal_type`
- `new_unknown_event_family`
- `new_unknown_payload_path`
- `fallback_used`
- `weak_fallback_used`
- `conflicting_evidence`
- `invariant_failed`
- `schema_snapshot_missing`
- `fixture_gap`
- `parser_exception`
- `transport_failure`
- `workbook_drift`
- `deployment_drift`
- `sensitive_evidence_redacted`

Drift flags must distinguish parser evidence drift from webhook transport
failure, workbook drift, and deployed Apps Script drift.

### Invariant Status

- `passed`
- `failed`
- `not_applicable`
- `not_checked`
- `degraded`

`review_required` must be true when `invariant_status` is `failed`, when
`value_source` is `conflict`, or when a final parser-managed field depends on a
low-confidence fallback.

## Inputs

Primary inputs:

- current MTGA `Player.log`
- current `Player-prev.log`
- saved raw or filtered match logs under local ignored data directories
- committed redacted regression fixtures
- parser event payloads
- parser-managed output rows and JSON artifacts
- parser runtime status and failure logs

Raw local logs are allowed as local evidence during development, but they must
not be committed unless redacted and explicitly approved.

Representative parser event kinds:

- `MatchState`
- `GameState`
- `GameResult`
- `ClientAction`
- `Rank`
- `EventLifecycle`
- `DetailedLoggingStatus`
- `DeckCollection`
- `Collection`
- `Inventory`
- connection and router diagnostic events

Representative raw event families:

- `matchGameRoomStateChangedEvent`
- `greToClientEvent`
- `GREMessageType_ConnectResp`
- `GREMessageType_GameStateMessage`
- `GREMessageType_QueuedGameStateMessage`
- `GREMessageType_IntermissionReq`
- `GREMessageType_SubmitDeckReq`
- `ClientMessageType_MulliganResp`
- `ClientMessageType_SelectNResp`
- `ClientMessageType_SubmitDeckResp`
- `EventJoin`
- `EventEnterPairing`
- `RankGetCombinedRankInfo`
- `StartHook`
- `authenticateResponse`

## Outputs

V1 required outputs:

- structured ledger definition for Tier 0 metadata and Tier 1-3 entries
- registered future-tier placeholders for Tier 4-7
- schema snapshot format
- drift report format
- invariant check names and expected statuses
- validation requirements and synthetic drift test requirements

V1 non-output:

- No workbook columns are added.
- No webhook payload fields are added.
- No Apps Script behavior is changed.
- No parser interpretation behavior is changed by this contract thread.

## Required V1 Behavior

### Tier 0: Evidence And Quality Metadata

V1 must define the metadata vocabulary and result shape that can attach to any
business-critical parser output. It does not need to expose the metadata in
workbook rows immediately.

Required Tier 0 metadata fields:

- `parser_version`
- `parser_commit_sha`
- `log_schema_snapshot_id`
- `ledger_version`
- `source_log_session_id`
- `source_log_file`
- `source_event_kind`
- `source_event_type`
- `source_payload_paths`
- `source_event_timestamp`
- `value_source`
- `confidence`
- `degraded_reason`
- `finality`
- `drift_flags`
- `invariant_status`
- `review_required`

Required rule: field-level metadata must be queryable by downstream JSON
surfaces and tests even if it is not yet workbook-visible.

### Tier 1: Match Identity And Lifecycle

V1 must define full ledger entries for these fields:

- `match_id`
- `match_started_at`
- `match_finished_at`
- `match_sync_status`
- `current_game_number`
- `player_team`
- `player_seat_id`
- `opponent_team`
- `opponent_seat_id`
- `match_winner_team`
- `match_result`
- `match_result_type`
- `match_result_reason`
- `games_won`
- `games_lost`
- `total_games`
- `match_win_flag`
- `game_win_rate`

Current row/schema surfaces:

- `MTGA Match ID`
- `MGTA Start Time`
- `MTGA End Time`
- `MTGA Sync Status`
- `Match Win?`
- `Games Won`
- `Games Lost`
- `Total Games`
- `Match Win Flag`
- `Game Win %`
- match history JSON fields with matching concepts

Required evidence map:

| Output family | Fields | Direct evidence | Fallback evidence | Missing behavior |
| --- | --- | --- | --- | --- |
| match identity | `match_id`, `current_match_id` | `MatchState.payload.match_id`; raw `matchGameRoomStateChangedEvent.gameRoomInfo.gameRoomConfig.matchId`; `GameState.identity.match_id`; `GameResult.identity.match_id`; `GameResult.game_info.matchID` | parser context only after a trusted prior match identity | block final match-level row identity; mark `unknown` |
| match timing | `match_started_at`, `match_finished_at`, `MGTA Start Time`, `MTGA End Time` | event metadata timestamp for match start/result events | first/last trusted event touching the summary | leave blank if no timestamp; mark fallback as `derived` |
| participant mapping | `player_team`, `player_seat_id`, `opponent_team`, `opponent_seat_id` | `MatchState.players[]`; raw reserved players; `GameState.system_seat_ids`; `GameState.players[]` | client action local team; context after prior trusted event | downgrade win/loss and play/draw if missing |
| match winner | `match_winner_team`, `match_result`, `Match Win?` | match-scope `GameResult.results[]`; `MatchState.game_results[]` with `MatchScope_Match`; `match_state=MatchState_MatchComplete` plus known winner | none unless a future contract defines safe BO structure inference | final result remains unknown; conflict requires review |
| match aggregates | `games_won`, `games_lost`, `total_games`, `match_win_flag`, `game_win_rate` | parser-owned game winners and player team | none beyond game-level ledger entries | unknown if required ingredients unknown |
| sync status | `MTGA Sync Status`, `match_sync_status` | parser row finality decision from `state.py` readiness | live/provisional row construction | live/provisional only; final blocked without match winner and local team |

Required Tier 1 invariants:

- A final match row must have one stable `match_id`.
- A final match winner must map to a known participant/team when participants
  are known.
- `games_won + games_lost` must equal `total_games`.
- `match_win_flag` must agree with `match_result`.
- A match should not become final before a final result source is seen.
- Missing local team must prevent high-confidence `Match Win?`.

### Tier 2: Queue, Format, Rank, And Event Context

V1 must define full ledger entries for these fields:

- `event_id`
- `super_format`
- `match_win_condition`
- `mtga_format`
- `mtga_queue_type`
- `rank_match_type`
- `play_mode_family`
- `event_family`
- `queue_subtype`
- `rank_eligible`
- `is_ranked_match`
- `is_unranked_match`
- `is_constructed_match`
- `is_limited_match`
- `is_draft_match`
- `is_sealed_match`
- `is_ladder_match`
- `is_special_event_match`
- `is_event_match`
- `constructed_rank_raw`
- `constructed_rank_class`
- `constructed_rank_level`
- `constructed_rank_percentile`
- `rank_bucket`
- `rank_source`

Current row/schema surfaces:

- `MTGA Event ID`
- `MTGA Format`
- `MTGA Queue Type`
- `My Rank`
- `MTGA Rank Raw`
- match history event identity fields

Required evidence map:

| Output family | Fields | Direct evidence | Fallback evidence | Missing behavior |
| --- | --- | --- | --- | --- |
| event identity | `event_id` | match room config `eventId`; parser `MatchState.payload.event_id` | reserved player `eventId`; event lifecycle names only if explicitly mapped | mark unknown or inferred; do not invent |
| format | `super_format`, `mtga_format`, constructed/limited flags | `GameState.game_info.superFormat`; raw `gameInfo.superFormat` | event ID string classifier | use `derived` or `inferred` label based on source strength |
| queue type | `match_win_condition`, `mtga_queue_type` | `GameState.game_info.matchWinCondition` | event ID markers; sideboarding or multi-game evidence | lower confidence when inferred from sideboarding/total games |
| event classification | `rank_match_type`, `play_mode_family`, `event_family`, `queue_subtype`, boolean flags | `event_identity.classify_event_identity()` from observed `event_id`, `super_format`, and `match_win_condition` | same classifier with partial ingredients | unknown flags must remain unknown/false according to classifier contract |
| constructed rank | `constructed_rank_raw`, `constructed_rank_class`, `constructed_rank_level`, `constructed_rank_percentile`, `rank_bucket`, `rank_source` | `Rank` payload / rank API response | rank carried forward to next match only while labeled as carried-forward | rank unknown if rank evidence disappears; stale rank must not be high confidence |

Required Tier 2 invariants:

- `Best of 1` should not contain postboard game rows.
- Sideboarding evidence implies Bo3 or another multi-game mode.
- Ranked-only analytics must not include unranked or unknown-rank-eligibility
  matches unless explicitly allowed.
- Rank carry-forward must expose a source label and must not look directly
  observed for the later match.

### Tier 3: Game-Level Facts

V1 must define full ledger entries for these fields:

- `game_number`
- `pre_postboard`
- `game_started_at`
- `game_finished_at`
- `game_duration`
- `game_winner_team`
- `game_result`
- `starting_player`
- `play_draw`
- `turn_count`
- `mulligan_count`
- `opening_hand_size`
- `opening_hand`
- `mulliganed_away`

Current row/schema surfaces:

- `Game Number`
- `Pre / Postboard`
- `Play / Draw`
- `Game Result`
- `Turn Count`
- `Game Duration`
- `G1 Play / Draw`
- `G2 Play / Draw`
- `G3 Play / Draw`
- `Game 1 Result`
- `Game 2 Result`
- `Game 3 Result`
- `G1 Mulligans`
- `G2 Mulligans`
- `G3 Mulligans`
- `G1 Turn Count`
- `G2 Turn Count`
- `G3 Turn Count`
- `Opening Hand Size`
- `Opening Hand`
- `Mulliganed Away`

Required evidence map:

| Output family | Fields | Direct evidence | Fallback evidence | Missing behavior |
| --- | --- | --- | --- | --- |
| game identity | `game_number`, current game number | `GameState.identity.game_number`; `GameState.game_info.gameNumber`; `GameResult.identity.game_number`; `GameResult.game_info.gameNumber` | parser context only after trusted prior game identity | do not attach facts to a guessed game without low-confidence metadata |
| game timing | `game_started_at`, `game_finished_at`, `game_duration` | event metadata timestamps for game state/result events | first/last event touching the game | leave duration blank if timestamps invalid; duration cannot be negative |
| game winner | `game_winner_team`, `game_result`, game result row fields | game-scope `GameResult.results[]`; top-level game result winner when no nested results exist; `MatchState.game_results[]` by game order | tightly constrained match-structure inference only if future contract approves | unknown if winner missing; no promotion from match winner by default |
| starting player | `starting_player`, `play_draw`, G1-G3 play/draw | client choose-starting-player response; turn-one `GameState.turnInfo.activePlayer` plus player/team mapping | later-game inference from prior game winner only when current model rules support it | play/draw blank or lower confidence |
| turn count | `turn_count`, G1-G3 turn counts | `GameState.turnInfo.turnNumber` | none | preserve maximum observed turn; unknown if absent |
| mulligans | `mulligan_count`, G1-G3 mulligans, total mulligans | `ClientAction` mulligan responses | opening hand size inference only with explicit low/medium confidence policy | unknown or low confidence; invalid counts must not poison state |
| opening hand | `opening_hand_size`, `opening_hand`, `mulliganed_away` | local private hand zones, object instance IDs, `grpId`/`overlayGrpId`, card catalog resolution | size from mulligan count; names from historical resolution only as enrichment | preserve size when possible; exact names blank/unknown when unresolved |
| pre/postboard | `pre_postboard` | game number and sideboarding lifecycle | game number only | game 1 normally preboard; later games normally postboard |

Required Tier 3 invariants:

- Game numbers should progress within a match and should not randomly reset
  without a new match.
- `Preboard` should normally map to game 1; later games should normally be
  `Postboard`.
- `play_draw` must agree with local player/team and starting player.
- A game winner should be one of the known teams or should be unknown.
- `game_duration` must not be negative.
- `turn_count` must not decrease for a game once observed.
- Opening hand exact card names are high confidence only when instance IDs map
  to resolved card identities.

## Future Tiers

V1 must register Tier 4-7 as future tiers with enough shape for drift reports to
name affected outputs. V1 does not need full field-by-field ledger coverage for
these tiers unless implementation scope is explicitly expanded.

### Tier 4: Sideboarding And Deck State

V1 future-tier fields:

- `sideboarding_entered`
- `submit_deck_seen`
- `submitted_deck_signature_by_game`
- `submitted_deck_timestamp_by_game`
- `mainboard_cards_by_game`
- `sideboard_cards_by_game`
- `sideboard_delta_g1_to_g2`
- `sideboard_delta_g2_to_g3`
- `cards_brought_in`
- `cards_taken_out`
- `deck_signature`
- `deck_name`
- `deck_id`
- `deck_match_mode`
- `deck_format`
- `mainboard_count`
- `sideboard_count`
- `deck_identity_confidence`

V1 required behavior:

- Register these outputs as Tier 4 and parser-adjacent.
- Define submit-deck evidence as the required direct source for exact deck
  signatures and card deltas.
- Define deck collection matching and deck names as enrichment, not raw parser
  truth.
- Include the synthetic missing submit-deck drift test in future validation.
- Do not compute sideboard deltas from later gameplay actions alone.

### Tier 5: Card Identity And Gameplay Actions

V1 future-tier fields:

- `grp_id`
- `instance_id`
- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `parent_id`
- `identity_hint_source`
- `card_name`
- `display_name`
- `resolution_status`
- `layout`
- `card_faces`
- `actor_relation`
- `turn_number`
- `game_state_id`
- `action_type`
- `cast_mode`
- `from_zone`
- `to_zone`
- `raw_action_types`
- `annotation_types`
- `annotation_categories`
- `visible_in_log`

V1 required behavior:

- Register these outputs as Tier 5.
- Treat card names as resolved enrichment, not raw Player.log truth.
- Treat `instance_id` as game-local, not durable historical card identity.
- Require future entries to preserve observed IDs even when name resolution is
  uncertain.

### Tier 6: Runtime Health And Drift Detection

V1 future-tier fields:

- `detailed_logging_enabled`
- `current_match_id`
- `current_game_number`
- `current_player_team`
- `last_event_kind`
- `last_event_type`
- `last_event_at`
- `webhook_successes`
- `webhook_failures`
- `event_failures`
- `router_failures`
- `active_deck_signature`
- `active_deck_name`
- `active_match_action_count`
- `missing_expected_signals`
- `new_unknown_signals`
- `changed_signal_types`
- `changed_signal_paths`
- `degraded_outputs`
- `invariant_failures`
- `recommended_review_modules`
- `recommended_github_issue_titles`

V1 required behavior:

- Define the drift report shape in this contract.
- Require parser drift to be separate from transport, workbook, and deployment
  drift.
- Require new unknown signals to be sampled for review without becoming trusted
  parser inputs.

### Tier 7: Derived Analytics Outputs

V1 future-tier outputs:

- `seen_win_rate`
- `opening_hand_win_rate`
- `cast_win_rate`
- `postboard_cast_win_rate`
- `mulligan_tax`
- `top_matchups`
- `top_packages`
- sideboarding recommendations
- matchup notes
- card-performance summaries

V1 required behavior:

- Register these as analytics outputs, not parser truth.
- Derived analytics must expose the minimum confidence of required ingredients
  or exclude weak ingredients from clean-truth metrics.
- AI-generated summaries and recommendations may explain parser facts but must
  not own them.

## Fields Not Treated As Parser-Managed Truth

These fields may consume parser facts but must not overwrite parser-owned truth:

- `Experiment ID`
- `Deck Code`
- `Opponent Archetype`
- `Opponent Variant`
- `Deck Tier`
- `Valid?`
- `General Analysis?`
- `Primary Comparison Analysis?`
- `Reason Tag`
- `Pilot Error?`
- `One-line note`
- `Rank Group`
- `Mythic Split`
- `Queue Bucket (Auto)`
- `Primary Comparison (Auto)`
- manually assigned matchup labels
- manually assigned sideboarding lesson labels
- external metagame tier labels
- AI-generated summaries, classifications, or recommendations

## Invariants

Global invariants:

- The ledger must not create a second source of parser truth.
- Every Tier 1-3 parser-managed output must have at least one ledger entry.
- Every Tier 1-3 ledger entry must define direct evidence, missing behavior,
  confidence behavior, finality behavior, and at least one invariant or explicit
  `not_applicable` invariant reason.
- Missing direct evidence must either use an approved fallback with lower or
  equal confidence, or mark the value `unknown`.
- Conflicting evidence must produce `value_source=conflict`,
  `confidence=low`, a `conflicting_evidence` drift flag, and
  `review_required=true`.
- A final workbook-facing parser field must not be high-confidence if its
  required raw evidence is missing.
- Transport failures must not be reported as parser evidence drift.
- Parser evidence drift must not be hidden because webhook or workbook transport
  still succeeds.

## Error Behavior

Malformed input:

- Missing expected event families or paths produce drift flags, not crashes.
- Changed field types produce `changed_signal_type` flags.
- Unparseable local logs are counted as parser/router failures and are not
  trusted evidence.
- Redacted sensitive fields must produce `sensitive_evidence_redacted` when they
  affect a ledger entry.

Missing source data:

- Required direct evidence missing from current logs downgrades confidence or
  marks the value unknown according to the entry policy.
- Missing golden fixtures produce `fixture_gap` and block claims of full
  validation.
- Missing schema snapshot produces `schema_snapshot_missing`.

Partial downstream state:

- Workbook drift, Apps Script deployment drift, and webhook transport failure
  must be labeled separately from parser evidence drift.
- Workbook formulas must not be used as error handlers for missing parser
  evidence.

## Side Effects

Allowed future v1 side effects:

- write local schema snapshot JSON/Markdown artifacts under approved runtime or
  test output paths
- write local drift report JSON/Markdown artifacts under approved runtime or
  test output paths
- update runtime status fields with drift-summary information only after an
  implementation contract approves the exact field names
- create redacted committed fixtures only after redaction rules are approved

Forbidden in v1 without a new contract:

- adding workbook columns
- changing webhook payload shape
- changing Apps Script receiver behavior
- committing raw unredacted local MTGA logs
- changing parser final reconciliation behavior
- generating GitHub issues automatically
- using AI analytics as parser truth

## Dependency Order

Implementation must proceed in this order:

1. Add structured ledger definitions without changing parser behavior.
2. Add schema snapshot builder against committed redacted fixtures.
3. Add invariant and drift-report evaluators that read parser outputs.
4. Add tests for ledger coverage and synthetic drift.
5. Wire optional runtime/status reporting only after the structured ledger and
   drift reports are verified.
6. Propose workbook/webhook exposure only in a later contract if needed.

## Compatibility

- Existing workbook row shapes must remain compatible in v1.
- Existing webhook payload shape must remain compatible in v1.
- Existing Apps Script behavior must remain compatible in v1.
- Existing parser-managed row fields from `models.py` and `sheet_schema.py`
  remain the current downstream field names.
- Historical rows without evidence metadata must remain readable.
- `MGTA Start Time` keeps its current spelling unless a separate workbook-schema
  contract changes it.
- `legacy_enriched` values must be opt-in for clean analytics until a future
  analytics contract says otherwise.

## Validation Requirements

Focused contract validation:

```powershell
py -m pytest -q tests/test_app_models.py tests/test_sheet_schema.py
py -m pytest -q tests/test_state.py tests/test_app_extractors.py
```

Regression validation:

```powershell
py -m pytest -q tests/test_parser_regressions.py
```

Runtime-surface validation:

```powershell
py -m pytest -q tests/test_runtime_surfaces.py
```

Gameplay/action validation:

```powershell
py -m pytest -q tests/test_gameplay_actions.py
```

Future ledger-specific validation:

```powershell
py -m pytest -q tests/test_evidence_ledger.py tests/test_schema_snapshot.py tests/test_drift_report.py tests/test_invariants.py
```

Repo-level validation before PR submission:

```powershell
.\tools\run_repo_checks.ps1
```

Future synthetic drift tests must prove:

- removing game-result winner evidence marks affected game/match outputs
  degraded or unknown and recommends `state.py` / `extractors.py` review
- removing rank evidence marks rank outputs unknown or carried-forward with
  non-observed source labels
- removing submit-deck evidence leaves exact sideboard deltas unknown and
  recommends deck/sideboarding review
- every Tier 1 field has direct or explicit fallback evidence
- every Tier 2 field has classification source and degradation behavior
- every Tier 3 field has source, confidence, and finality behavior
- Tier 4 sideboarding distinguishes lifecycle detection from exact deck delta
  evidence
- Tier 5 card/action fields record identity confidence or resolution status
- Tier 6 status output distinguishes parser drift from transport failure
- non-parser-managed fields cannot overwrite parser-owned truth
- committed fixtures do not contain sensitive raw identity data
- golden fixture outputs remain stable under the current parser

## Golden Fixture Requirements

V1 implementation must use committed redacted fixtures or synthetic structured
fixtures. Raw local logs must not be committed without redaction approval.

Recommended fixture categories:

- Bo1 match win
- Bo1 match loss
- Bo3 match win
- Bo3 match loss
- sideboarding between games
- game 1 on the play
- game 1 on the draw
- mulligan to six or lower
- opening hand captured with exact card names
- opening hand partially unresolved, if available
- concede
- timeout or disconnect, if available
- ranked constructed
- unranked constructed
- limited or draft, if in scope
- deck submission / submit deck response
- rank snapshot before or during a match
- game result and match result with both game-scope and match-scope results

Each fixture must record:

- fixture ID
- redaction status
- source schema snapshot ID
- parser commit/version
- expected `MatchLogRow`
- expected `GameLogRow` rows
- expected match history item
- expected action/card outputs if relevant
- known caveats
- privacy redaction notes

## Required V1 Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger.md` exists.
- The contract links to the problem representation, constitution, Module
  Contract Writer rules, and module contract template.
- The contract names parser and state interpretation as the truth-owning layer.
- The ledger entry, evidence signal, field evidence result, schema snapshot, and
  drift report shapes are defined.
- The value source, confidence, finality, drift flag, and invariant status
  vocabularies are defined.
- Tier 0 metadata is required.
- Tier 1-3 fields are mapped to evidence, fallback behavior, invariants, and
  degradation rules.
- Tier 4-7 are represented as future tiers with v1 registration rules.
- Non-parser-managed fields are explicitly excluded from parser truth.
- Validation commands and future ledger-specific synthetic drift tests are
  listed.
- V1 explicitly avoids workbook schema and webhook payload changes.
- No behavior changes are implemented in the contract thread.

## Unknowns

- Whether the implementation should use Python dataclasses, YAML/JSON, or a
  hybrid as the canonical machine-readable source.
- Whether field evidence metadata should first appear only in internal JSON
  artifacts, runtime status, workbook rows, or all of them.
- Whether metadata should be stored per field, per row, or both.
- Whether degraded parser outputs should be posted, held locally, or posted with
  warnings once workbook exposure is designed.
- Whether drift reports should create GitHub issues automatically or only
  suggest issue titles and bodies.
- Which raw logs should become the first approved golden fixtures.
- What exact redaction policy is sufficient for committed raw-log slices.
- Whether v1 implementation should fully cover Tier 4 sideboarding/deck fields
  or only register them.
- Whether historical records should be backfilled with evidence metadata or
  metadata should begin only after ledger implementation.
- How `legacy_enriched` values should be displayed to analytics by default.

## Suspected Implementation Gaps

- No `evidence_ledger.py`, `schema_snapshot.py`, `drift_report.py`, or
  `invariants.py` module currently exists.
- Current parser rows do not expose field-level `value_source`, `confidence`,
  `finality`, `drift_flags`, or `invariant_status`.
- Current runtime status does not report missing expected signals, changed
  signal types, degraded outputs, invariant failures, or recommended review
  modules.
- Current parser regression fixtures verify expected normalized outputs but do
  not map those outputs to raw evidence paths.
- Current tests do not synthetically remove game-result, rank, or submit-deck
  evidence and assert degradation metadata.
- Current card-performance metrics do not expose ingredient confidence.
- Current deck/sideboarding outputs do not have per-game deck signatures or
  exact sideboard deltas as parser-managed facts.
- Current workbook row shape has no metadata columns and should remain unchanged
  until a future workbook-schema contract approves a migration.
- Current drift classification does not distinguish all of parser drift,
  transport failure, workbook drift, and deployment drift.

## Next Workflow Action

Next role: Module Implementer (C)

Pasteable prompt:

````text
Use the Mythic Edge agent constitution. Act as the Module Implementer thread for docs/contracts/player_log_evidence_ledger.md.

Source artifacts:
- `docs/agent_constitution.md`
- `docs/agent_threads/implementation.md`
- `docs/problem_representations/player_log_evidence_ledger.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/templates/implementation_handoff.md`

Task:
Compare the current repository behavior to `docs/contracts/player_log_evidence_ledger.md` and produce `docs/implementation_handoffs/player_log_evidence_ledger_comparison.md`.

Do not assume there is a known bug. This is a contract audit / implementation comparison pass.

Required workflow:
1. Inspect the contract and problem representation.
2. Inspect current parser-managed output surfaces in `models.py`, `sheet_schema.py`, `state.py`, `extractors.py`, `event_identity.py`, `runtime_surfaces.py`, `gameplay_actions.py`, `card_performance.py`, and `diagnostics.py`.
3. Determine which v1 contract pieces already exist, which are missing, and which would require new modules.
4. Produce an implementation handoff that separates docs-only findings, safe local implementation candidates, forbidden scope, and open questions.
5. Do not implement behavior changes unless the user explicitly asks for implementation after this comparison.
6. Do not change workbook schema, webhook payload shape, deployed Apps Script behavior, parser final reconciliation behavior, secrets, environment variables, raw local logs, generated card data, runtime status files, or live workbook state.

Validation to report if code is changed:

```powershell
py -m pytest -q tests/test_app_models.py tests/test_sheet_schema.py
py -m pytest -q tests/test_state.py tests/test_app_extractors.py
py -m pytest -q tests/test_parser_regressions.py
py -m pytest -q tests/test_runtime_surfaces.py
py -m pytest -q tests/test_gameplay_actions.py
```

Final handoff must include:
- role performed
- source artifacts used
- artifact produced
- files changed
- code changed or docs-only
- contract matches
- contract mismatches
- missing tests
- forbidden scope touched or not
- validation run and result
- still-unverified layers
- next recommended thread role
````

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "Docs-only contract; behavior tests not run."
  stop_conditions:
    - "Do not implement behavior changes unless the user explicitly asks after the comparison handoff."
    - "Stop before workbook schema, webhook payload, Apps Script deployment, parser final reconciliation, raw-log fixture, or runtime status shape changes."
    - "Stop if raw local MTGA logs are needed before redaction rules are approved."
```
