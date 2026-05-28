# Player.log Evidence Ledger Tier 2 Queue / Format / Rank / Event-Context Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/167
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/166
- previous_integration_commit: 9f625ea0ef31cdbaa97a827a95ba3b4808562d11
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier2-context
- target_artifact: docs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier2_queue_format_rank_event_context_comparison.md
- risk_tier: Medium-High
- status: contract only

Required agent docs:

- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md

Related authority:

- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/parser_event_identity.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md

## Purpose

Issue #167 maps Tier 2 queue, format, rank, and event-context provenance in the
Player.log evidence ledger.

The seed fields in scope are exactly:

- `event_id`
- `super_format`
- `constructed_rank`
- `queue_type`

These fields decide how later reports and analytics group matches by Arena
event, format, queue length, rank, rankedness, and event family. The evidence
ledger must explain which values are directly observed, derived by parser
model methods, carried forward from a previous rank snapshot, unknown, or
degraded.

Plain English: Mythic Edge may say "this match looked like Traditional Ladder,
Constructed, Best of 3, with a carried-forward Diamond rank" only when the
parser-owned evidence and derivation path are explicit. Workbook formulas,
dashboard filters, runtime match history, analytics, Match Journal, overlays,
SQLite, Google Sheets sync, AI, and model providers must consume these parser
facts; they must not become truth owners.

This contract documents provenance metadata only. It must not change parser
behavior, event identity classifier behavior, rank parsing behavior, match
state parsing behavior, parser state final reconciliation, parser event
classes, workbook schema, webhook payload shape, Apps Script behavior, output
transport, match/game identity, deduplication, runtime artifacts, analytics
truth, AI truth, or model-provider behavior.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, validators, vocabulary constants, privacy posture, and the
allowed `value_source`, `confidence`, `finality`, invariant, drift, and privacy
vocabularies.

`docs/contracts/parser_event_identity.md` remains authoritative for
`classify_event_identity(...)` behavior and `EventIdentity` output
vocabulary. Issue #167 may document those classifier outputs as facets and
downstream context, but it must not change classifier precedence or allowed
values.

The Tier 5 contracts now seed `grp_id`, `gameplay_action`, and
`opponent_card_observation`. Issue #167 does not reopen Tier 5 behavior. It
maps the remaining Tier 2 context family needed before later analytics can
group parser facts by event, format, queue, and rank.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #167 provenance should be
recorded through this contract, implementation handoff, family notes, entry
notes, and focused tests rather than by changing the top-level ledger object
shape.

## Owning Layer

Owning layer: parser state/model interpretation and evidence-ledger metadata.

Truth boundary:

- `src/mythic_edge_parser/parsers/match_state.py` owns parsed MatchState
  `event_id` evidence from game-room config and player fallback paths.
- `src/mythic_edge_parser/parsers/rank.py` owns parsed Rank API payload
  evidence from `RankGetCombinedRankInfo`.
- `src/mythic_edge_parser/app/state.py` owns current match summary updates,
  event-id assignment precedence, game-info ingestion, latest constructed-rank
  snapshot storage, and carried-forward pre-match rank attachment.
- `src/mythic_edge_parser/app/models.py` owns `MatchSummary` fields and
  model-derived row/history facets such as `mtga_format()`,
  `mtga_queue_type()`, `rank_bucket()`, `to_match_log_row()`,
  `to_game_log_row()`, and `to_history_item()`.
- `src/mythic_edge_parser/app/event_identity.py` owns normalized
  event-classification vocabulary derived from `event_id`, `super_format`, and
  `match_win_condition`.
- `src/mythic_edge_parser/app/evidence_ledger.py` owns provenance metadata,
  confidence, finality, degradation behavior, drift flags, invariants, and
  protected boundary notes.
- `src/mythic_edge_parser/app/runtime_surfaces.py` may expose or filter match
  history using parser-produced event/rank context, but it does not own the
  truth for that context.
- Workbook formulas, dashboards, webhook transport, Apps Script, Match
  Journal, overlays, SQLite, Google Sheets sync, analytics, archetype
  classifiers, OpenAI/model-provider output, and AI output are downstream
  consumers only.

The evidence ledger describes support and uncertainty for parser-owned context
fields. It must not become a second event classifier, a rank parser, a workbook
schema migration, an analytics grouping oracle, or an AI truth layer.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier2_queue_format_rank_event_context_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md

Referenced but not silently owned:

- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/event_identity.py
- src/mythic_edge_parser/parsers/match_state.py
- src/mythic_edge_parser/parsers/rank.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- tests/test_event_identity.py
- tests/test_match_state_parser.py
- tests/test_state.py
- tests/test_app_models.py
- tests/test_runtime_surfaces.py

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` at
`9f625ea0ef31cdbaa97a827a95ba3b4808562d11`:

- Issue #166 is implemented on the integration branch.
- Tier 5 `card_identity_and_gameplay_actions` is a `seeded_sample` with seed
  fields:
  - `grp_id`
  - `gameplay_action`
  - `opponent_card_observation`
- Tier 2 `queue_format_rank_event_context` is currently `registered_future`
  with future fields:
  - `event_id`
  - `super_format`
  - `constructed_rank`
  - `queue_type`
- `match_state.py` parses `event_id` from
  `gameRoomInfo.gameRoomConfig.eventId`.
- If game-room config `eventId` is missing or blank, `match_state.py` falls
  back to the first non-blank player-level `eventId` from the selected player
  source.
- Game-room config `reservedPlayers` are preferred over `gameRoomInfo.players`
  for player source; empty or malformed lists fall back or normalize to an
  empty player list.
- `state._set_event_id(...)` sets `MatchSummary.event_id` from non-blank
  payload text. Once set, it preserves the existing value except that a stored
  `"Play"` value can be replaced by a later non-`"Play"` value.
- `MatchSummary.ingest_game_info(...)` stores `super_format` from
  `game_info.superFormat` and `match_win_condition` from
  `game_info.matchWinCondition` when present.
- `rank.py` parses `RankGetCombinedRankInfo` responses into `RankEvent`
  payload fields:
  - `constructed_class`
  - `constructed_level`
  - `limited_class`
  - `limited_level`
  - `constructed_percentile`
  - `limited_percentile`
  - `raw_rank`
- `state._normalized_rank_fields(...)` builds `constructed_rank` as
  `"Mythic {constructed_percentile}"` when class is `Mythic` and percentile is
  present; otherwise it builds `"{constructed_class} {constructed_level}"`.
- `state._update_match_summary(...)` stores the latest rank snapshot and last
  posted rank for every valid `RankEvent`.
- If a current match exists and is not ready, a rank event can apply to the
  current summary with `constructed_rank_source == "payload"`.
- If no current ready summary receives the rank, the latest rank snapshot can
  be carried into the next match summary with
  `constructed_rank_source == "carried_forward_pre_match"`.
- `MatchSummary.rank_bucket()` exposes row/history-facing rank bucket text:
  rank class, `Mythic %`, `Mythic #`, or blank.
- `MatchSummary.mtga_format()` uses `super_format` first, removing the
  `SuperFormat_` prefix when present. If `super_format` is blank, it falls
  back to `event_id` containing `Constructed` or `Limited`.
- `MatchSummary.mtga_queue_type()` uses `match_win_condition` mapping first,
  then `event_id` / raw condition text markers for Best of 3 or Best of 1,
  then sideboarding or multi-game fallback for Best of 3, and otherwise
  returns the raw condition text.
- `MatchSummary.event_identity()` calls
  `classify_event_identity(event_id, super_format, match_win_condition)`.
- `EventIdentity` exposes `rank_match_type`, `play_mode_family`,
  `event_family`, `queue_subtype`, `rank_eligible`, and boolean helper fields.
- `to_match_log_row()` exposes workbook-facing `My Rank`, `MTGA Format`,
  `MTGA Event ID`, `MTGA Queue Type`, and `MTGA Rank Raw`.
- `to_game_log_row()` exposes workbook-facing `MTGA Format`, `My Rank`,
  `MTGA Event ID`, and `MTGA Queue Type`.
- `to_history_item()` exposes parser-produced runtime/history fields including
  `rank`, `constructed_rank_raw`, `constructed_rank_source`, `super_format`,
  `match_win_condition`, `mtga_format`, `mtga_queue_type`, `event_id`, and all
  `EventIdentity` fields.
- `runtime_surfaces.py` filters match history by parser-produced format,
  queue type, event ID, rank match type, play mode family, event family, and
  queue subtype.

Observed risks, not fixed by this issue:

- `MTGA Format` can look directly observed even when it came from an
  `event_id` fallback.
- `MTGA Queue Type` can look directly observed even when it came from
  `event_id`, raw condition text, sideboarding, or total-games fallback.
- `My Rank` can look match-scoped even when the underlying
  `constructed_rank` was carried forward from a pre-match snapshot.
- `EventIdentity` outputs can look like raw MTGA fields even though they are
  parser-owned derived classifier fields.
- Novel Arena event IDs or match win conditions can degrade to `unknown` or
  raw text; downstream filters must not silently convert those values into
  clean format, queue, rankedness, archetype, or analytics truth.

## Scope Decision

Codex C should implement issue #167 as a Tier 2
`queue_format_rank_event_context` metadata slice in the existing evidence
ledger.

Required family metadata:

- Change Tier 2 `queue_format_rank_event_context.status` from
  `registered_future` to `seeded_sample`.
- Add exactly these Tier 2 seed fields, in this order:
  - `event_id`
  - `super_format`
  - `constructed_rank`
  - `queue_type`
- Remove those fields from Tier 2 `future_fields`.
- Keep Tier 2 `future_fields` empty after issue #167.
- Preserve all prior Tier 1, Tier 3, Tier 4, and Tier 5 seed fields and
  entries.
- Add family notes stating that issue #167 maps queue/format/rank/event
  context provenance without changing parser behavior, event identity
  classifier behavior, rank parsing behavior, match state parsing behavior,
  workbook schema, runtime filters, Match Journal, overlays, SQLite, Google
  Sheets sync, analytics, archetype classification, model-provider behavior,
  or AI truth.

Required Tier 2 entries:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier2.queue_format_rank_event_context.event_id` | `event_id` | `MTGA Event ID` | `observed` or `derived` |
| `tier2.queue_format_rank_event_context.super_format` | `super_format` | `MTGA Format` | `observed` or `derived` |
| `tier2.queue_format_rank_event_context.constructed_rank` | `constructed_rank` | `MTGA Rank Raw` | `observed` or `derived` |
| `tier2.queue_format_rank_event_context.queue_type` | `queue_type` | `MTGA Queue Type` | `derived` |

Fields and facets not authorized as separate seed fields in issue #167:

- `mtga_format`
- `mtga_queue_type`
- `match_win_condition`
- `my_rank`
- `rank_bucket`
- `constructed_class`
- `constructed_level`
- `constructed_percentile`
- `constructed_rank_source`
- `limited_class`
- `limited_level`
- `limited_percentile`
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
- `format`
- `queue`
- `rankedness`
- `archetype`
- `matchup`
- `analytics_segment`

Those fields may appear only as source evidence, fallback evidence, derived
facets, downstream surfaces, invariants, notes, or future issue scope.

## Public Interface

This contract covers evidence-ledger metadata for existing parser, model, row,
and runtime-history surfaces. It does not create a new runtime API.

Authorized ledger fields:

| Ledger field | Entry ID | Meaning |
| --- | --- | --- |
| `event_id` | `tier2.queue_format_rank_event_context.event_id` | Raw or parser-selected MTGA event identifier for the match. |
| `super_format` | `tier2.queue_format_rank_event_context.super_format` | Raw MTGA super-format descriptor carried by GameState game info when available. |
| `constructed_rank` | `tier2.queue_format_rank_event_context.constructed_rank` | Constructed rank text normalized from `RankGetCombinedRankInfo` or carried forward from the latest pre-match snapshot. |
| `queue_type` | `tier2.queue_format_rank_event_context.queue_type` | Parser-derived queue-length label exposed as `MTGA Queue Type` from `MatchSummary.mtga_queue_type()`. |

Authorized facets inside entries:

| Facet | Existing surface | Contract status |
| --- | --- | --- |
| `MTGA Event ID` | `MatchSummary.event_id`, match/game log rows | Display/row label for `event_id`; not a separate seed. |
| `MTGA Format` | `MatchSummary.mtga_format()` | Display/row facet of `super_format`; may derive from `event_id` fallback. |
| `MTGA Queue Type` | `MatchSummary.mtga_queue_type()` | Display/row facet of `queue_type`; derived from match-win-condition/event/fallbacks. |
| `My Rank` | `MatchSummary.rank_bucket()` | Bucketed display facet of `constructed_rank`; not a separate seed. |
| `MTGA Rank Raw` | `MatchSummary.constructed_rank` | Row label for `constructed_rank`; not a separate seed. |
| `constructed_rank_source` | `MatchSummary.constructed_rank_source` | Provenance facet for payload versus carried-forward rank. |
| `match_win_condition` | `MatchSummary.match_win_condition` | Direct evidence/dependency for `queue_type`, not a seed field in #167. |
| `EventIdentity` fields | `MatchSummary.event_identity().to_dict()` | Derived classifier facets and runtime filters, not seed fields in #167. |
| runtime history filters | `runtime_surfaces.filter_match_history_payload()` | Downstream consumers of parser-produced context. |

Required compatibility:

- Do not rename or change `MatchSummary.event_id`.
- Do not rename or change `MatchSummary.super_format`.
- Do not rename or change `MatchSummary.constructed_rank`.
- Do not rename or change `MatchSummary.match_win_condition`.
- Do not change `MatchSummary.mtga_format()`.
- Do not change `MatchSummary.mtga_queue_type()`.
- Do not change `MatchSummary.rank_bucket()`.
- Do not change `MatchSummary.event_identity()`.
- Do not change `classify_event_identity(...)`.
- Do not change `match_state.py` event-id parsing/fallback behavior.
- Do not change `rank.py` payload shape or rank normalization behavior.
- Do not add workbook columns, webhook fields, Apps Script fields, parser
  events, runtime status fields, Match Journal behavior, overlay behavior,
  SQLite behavior, Google Sheets sync behavior, analytics behavior, or AI/model
  provider behavior.

## Evidence Boundary Matrix

| Evidence surface | Can prove | Cannot prove | Source label |
| --- | --- | --- | --- |
| MatchState `gameRoomConfig.eventId` | Direct observed event ID string when non-blank. | Format, queue, rankedness, archetype, matchup, analytics segment by itself. | `observed` |
| MatchState player-level `eventId` fallback | Observed fallback event ID when config event ID is missing or blank. | Same confidence as config path, downstream classification certainty. | `observed` fallback |
| `state._set_event_id(...)` stored summary value | Parser-selected event ID after current precedence rules. | New event-classification behavior or downstream truth. | `derived` when precedence/correction applies |
| GameState `game_info.superFormat` | Direct observed raw super-format descriptor when present. | Queue type, rankedness, archetype, card pool, matchup. | `observed` |
| `MatchSummary.mtga_format()` | Row/display format label from `super_format` or `event_id` fallback. | Raw `super_format` when fallback is used, workbook-owned format truth. | `derived` facet |
| GameState `game_info.matchWinCondition` | Direct raw match win condition. | Queue type label without parser derivation, rankedness by itself. | `observed` dependency |
| `MatchSummary.mtga_queue_type()` | Parser-derived queue type label. | Raw Arena queue truth when fallback is sideboarding/total-games-derived. | `derived` |
| Rank API constructed fields | Observed rank snapshot fields from `RankGetCombinedRankInfo`. | Match-scoped rank when applied by carry-forward only, limited-rank truth for constructed rank. | `observed` |
| Latest rank snapshot carry-forward | Parser-derived pre-match rank context for next match. | Direct match payload evidence, final post-match rank truth. | `derived` |
| `MatchSummary.rank_bucket()` | Display bucket for constructed rank. | Raw rank value, exact mythic percentile or mythic number when bucketed. | `derived` facet |
| `EventIdentity` classifier | Parser-derived normalized classification from event descriptors. | Raw MTGA field, workbook formula truth, archetype, matchup, advice. | `derived` |
| Runtime match-history filters | Filtering and available values from parser-produced history. | Source evidence or parser truth owner. | downstream consumer |
| Workbook, Apps Script, dashboard, analytics, Match Journal, overlay, SQLite, Google Sheets sync, AI | Display, transport, storage, grouping, explanation, or analysis. | Queue/format/rank/event-context truth. | not source evidence |

## Required Entry Behavior

### `event_id`

The `tier2.queue_format_rank_event_context.event_id` entry should use:

- `tier`: `2`
- `output_family`: `queue_format_rank_event_context`
- `output_field`: `event_id`
- `display_name`: `MTGA Event ID`
- `parser_owner`: `src/mythic_edge_parser/app/state.py`
- `model_surface`: `MatchSummary.event_id / MatchSummary.to_match_log_row`
- `downstream_surfaces`:
  - `MatchLogRow`
  - `GameLogRow`
  - `match_history`
  - `EventIdentity`
  - `runtime_surfaces`
- `parser_managed_truth`: `True`
- `coverage_status`: `seeded_sample`

Direct evidence should include:

- `match_state.event_id.game_room_config`
  - parser event kind: `MatchState`
  - raw event family: `matchGameRoomStateChangedEvent`
  - raw message type: ``
  - normalized path: `payload.event_id`
  - raw path:
    `matchGameRoomStateChangedEvent.gameRoomInfo.gameRoomConfig.eventId`
  - allowed types: `str`
  - value source: `observed`
  - confidence: `high`
  - finality: `live`

Fallback evidence should include:

- `match_state.event_id.player_fallback`
  - raw path:
    `matchGameRoomStateChangedEvent.gameRoomInfo.gameRoomConfig.reservedPlayers[].eventId`
    and `matchGameRoomStateChangedEvent.gameRoomInfo.players[].eventId`
  - value source: `observed`
  - confidence: `medium`
  - finality: `live`

- `parser_state.match_summary.event_id`
  - normalized path: `MatchSummary.event_id`
  - value source: `derived`
  - confidence: `medium`
  - finality: `provisional` before final rows

### `super_format`

The `tier2.queue_format_rank_event_context.super_format` entry should use:

- `tier`: `2`
- `output_family`: `queue_format_rank_event_context`
- `output_field`: `super_format`
- `display_name`: `MTGA Format`
- `parser_owner`: `src/mythic_edge_parser/app/models.py`
- `model_surface`: `MatchSummary.super_format / MatchSummary.mtga_format()`
- `downstream_surfaces`:
  - `MatchLogRow`
  - `GameLogRow`
  - `match_history`
  - `EventIdentity`
  - `runtime_surfaces`
- `parser_managed_truth`: `True`
- `coverage_status`: `seeded_sample`

Direct evidence should include:

- `game_state.game_info.super_format`
  - parser event kind: `GameState`
  - raw event family: `greToClientEvent`
  - raw message type: `GREMessageType_GameStateMessage`
  - normalized path: `payload.game_info.superFormat`
  - raw path:
    `greToClientMessages[].gameStateMessage.gameInfo.superFormat`
  - allowed types: `str`
  - value source: `observed`
  - confidence: `high`
  - finality: `live`

Fallback evidence should include:

- `model.match_summary.mtga_format_event_id_fallback`
  - normalized path: `MatchSummary.mtga_format()`
  - dependency path: `MatchSummary.event_id`
  - value source: `derived`
  - confidence: `medium`
  - finality: `provisional`

This fallback documents the row-facing `MTGA Format` label, not raw
`super_format` truth.

### `constructed_rank`

The `tier2.queue_format_rank_event_context.constructed_rank` entry should use:

- `tier`: `2`
- `output_family`: `queue_format_rank_event_context`
- `output_field`: `constructed_rank`
- `display_name`: `MTGA Rank Raw`
- `parser_owner`: `src/mythic_edge_parser/app/state.py`
- `model_surface`: `MatchSummary.constructed_rank / MatchSummary.rank_bucket()`
- `downstream_surfaces`:
  - `MatchLogRow`
  - `GameLogRow`
  - `match_history`
  - `runtime_surfaces`
- `parser_managed_truth`: `True`
- `coverage_status`: `seeded_sample`

Direct evidence should include:

- `rank.constructed_rank.payload`
  - parser event kind: `Rank`
  - raw event family: `api_response`
  - raw message type: `RankGetCombinedRankInfo`
  - normalized path:
    `payload.constructed_class + payload.constructed_level + payload.constructed_percentile`
  - raw path:
    `RankGetCombinedRankInfo.constructedClass + constructedLevel + constructedPercentile`
  - allowed types: `str`, `int`, `str-int`
  - value source: `observed`
  - confidence: `high`
  - finality: `live`

Fallback evidence should include:

- `rank.constructed_rank.latest_pre_match_snapshot`
  - normalized path:
    `state.latest_rank_snapshot -> MatchSummary.constructed_rank`
  - value source: `derived`
  - confidence: `medium`
  - finality: `provisional`
  - notes: `constructed_rank_source == "carried_forward_pre_match"`

- `model.match_summary.rank_bucket`
  - normalized path: `MatchSummary.rank_bucket()`
  - value source: `derived`
  - confidence: `medium`
  - finality: `provisional`
  - notes: row/history-facing `My Rank` bucket only, not raw rank truth

Limited rank fields are not in scope for `constructed_rank` truth in issue
#167. They may be mentioned only as ignored adjacent payload fields.

### `queue_type`

The `tier2.queue_format_rank_event_context.queue_type` entry should use:

- `tier`: `2`
- `output_family`: `queue_format_rank_event_context`
- `output_field`: `queue_type`
- `display_name`: `MTGA Queue Type`
- `parser_owner`: `src/mythic_edge_parser/app/models.py`
- `model_surface`: `MatchSummary.mtga_queue_type()`
- `downstream_surfaces`:
  - `MatchLogRow`
  - `GameLogRow`
  - `match_history`
  - `runtime_surfaces`
  - `EventIdentity`
- `parser_managed_truth`: `True`
- `coverage_status`: `seeded_sample`

Direct evidence should include:

- `game_state.game_info.match_win_condition`
  - parser event kind: `GameState`
  - raw event family: `greToClientEvent`
  - raw message type: `GREMessageType_GameStateMessage`
  - normalized path: `payload.game_info.matchWinCondition`
  - raw path:
    `greToClientMessages[].gameStateMessage.gameInfo.matchWinCondition`
  - allowed types: `str`
  - value source: `observed`
  - confidence: `high` for the raw condition, `high` for recognized mapped
    queue labels
  - finality: `live`

Fallback evidence should include:

- `model.match_summary.queue_type.event_id_markers`
  - normalized path: `MatchSummary.mtga_queue_type()`
  - dependency path: `MatchSummary.event_id`
  - value source: `derived`
  - confidence: `medium`
  - finality: `provisional`

- `model.match_summary.queue_type.sideboarding_or_games_fallback`
  - normalized path:
    `MatchSummary.sideboarding_entered + MatchSummary.total_games`
  - value source: `derived`
  - confidence: `low`
  - finality: `provisional`

- `model.match_summary.queue_type.raw_condition_passthrough`
  - normalized path: `MatchSummary.match_win_condition`
  - value source: `derived`
  - confidence: `low`
  - finality: `provisional`

`queue_type` is a parser-derived row label, not a raw MTGA field.

## Event Identity Classifier Facets

Issue #167 must document but not seed these classifier outputs:

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

Required guarantees:

- These values are parser-owned derived context from
  `classify_event_identity(event_id, super_format, match_win_condition)`.
- They are allowed as downstream facets in the Tier 2 entries.
- They must not become separate seed fields in issue #167.
- Unknown rankedness must remain unknown, especially for competitive special
  events where the classifier intentionally cannot prove rankedness.
- Runtime filters may consume these values; runtime filters must not define or
  overwrite them.

## Value Source Policy

Required policy labels:

- `observed`: raw parser event payload field observed from MatchState,
  GameState, or Rank event evidence.
- `derived`: parser state/model value built from observed fields, fallback
  precedence, carry-forward state, or model helper methods.
- `unknown`: missing, blank, malformed, novel, or unsupported descriptors.
- `conflict`: contradictory evidence or unexpected changes that require
  review.
- `legacy_enriched`: not expected for issue #167 seed entries; reserve for
  future downstream enrichment if needed.

Required mapping:

- `event_id` from game-room config -> `observed`.
- `event_id` from player fallback -> `observed`, fallback confidence.
- `event_id` replacement of `"Play"` by a later non-`"Play"` value ->
  `derived` precedence/correction context.
- `super_format` from `game_info.superFormat` -> `observed`.
- `MTGA Format` from `event_id` fallback -> `derived`.
- `constructed_rank` from Rank payload -> `observed`.
- `constructed_rank` carried into next match -> `derived`.
- `My Rank` bucket -> `derived` facet.
- `queue_type` from recognized match-win-condition mapping -> `derived` from
  observed dependency.
- `queue_type` from event-id markers -> `derived`.
- `queue_type` from sideboarding or total-games fallback -> `derived` weak
  fallback.
- EventIdentity values -> `derived`.
- Missing or novel descriptors -> `unknown`.
- Contradictory or changing context that cannot be resolved by existing
  precedence -> `conflict`.

## Confidence Policy

High confidence:

- `event_id` from game-room config.
- `super_format` from GameState game info.
- `constructed_rank` from a valid Rank payload applied directly to a current
  not-ready match summary.
- `queue_type` derived from a recognized `match_win_condition` enum.

Medium confidence:

- `event_id` from player-level fallback.
- `super_format` row-facing `MTGA Format` derived from event-id fallback.
- `constructed_rank` carried forward from the latest pre-match rank snapshot.
- `queue_type` derived from event-id Best-of markers.
- EventIdentity fields from recognized event/super-format/win-condition
  descriptors.

Low confidence / review required:

- `queue_type` derived only from sideboarding or total-games fallback.
- `queue_type` falling through to raw unrecognized condition text.
- Competitive special event rankedness classified as `unknown`.
- Generic draft or novel event descriptors with unknown rankedness.
- Missing `match_win_condition` where event ID fallback is also ambiguous.
- Conflict between observed `event_id`, `super_format`, and classifier output
  expectations.
- Carry-forward rank used when match association is unclear.

Unknown confidence:

- Missing or blank `event_id`.
- Missing or blank `super_format` with no event-id format fallback.
- Missing or blank constructed rank.
- Missing or blank queue evidence.
- Novel descriptors that do not classify.

## Finality Policy

- Raw MatchState, GameState, and Rank context values are `live` while the match
  is active.
- `event_id`, `super_format`, `constructed_rank`, and `queue_type` are
  `provisional` in live summaries and runtime/history snapshots before final
  match rows are emitted.
- Final match/game log rows may use `final` for the row-facing context values
  once final match output is emitted, but that does not change parser behavior.
- A later stronger parser-owned context value may be described as
  `reconciled` only if existing parser behavior corrects a prior value, such
  as replacing initial `"Play"` event ID with a later non-`"Play"` event ID.
- Rank carry-forward remains `provisional` or `final` only relative to the row
  lifecycle; it remains `derived` as provenance because it was not directly
  match-scoped.
- EventIdentity classifier outputs inherit finality from the source
  `event_id`, `super_format`, and `match_win_condition` context.

## Invariants

Codex C must preserve these invariants in metadata and tests:

- Tier 2 seeds exactly `event_id`, `super_format`, `constructed_rank`, and
  `queue_type`.
- Tier 2 `future_fields` is empty after issue #167.
- No separate Tier 2 seed fields are added for workbook-facing labels,
  classifier facets, rank buckets, match-win condition, runtime filters,
  analytics segments, archetypes, or AI outputs.
- `event_id` provenance distinguishes game-room config evidence from
  player-level fallback evidence.
- `super_format` provenance distinguishes raw `superFormat` evidence from
  row-facing `MTGA Format` fallback labels.
- `constructed_rank` provenance distinguishes direct Rank payload evidence
  from `carried_forward_pre_match` rank snapshots.
- `queue_type` provenance documents that `MTGA Queue Type` is parser-derived,
  with weaker confidence for event-id and sideboarding/total-games fallbacks.
- EventIdentity values remain parser-derived facets, not workbook or AI truth.
- Unknown or novel event descriptors must remain unknown/degraded rather than
  being silently coerced into clean rankedness, queue, format, archetype, or
  analytics truth.
- Workbook formulas, dashboards, webhook transport, Apps Script, Match
  Journal, overlays, SQLite, Google Sheets sync, analytics, archetype
  classifiers, and AI output must not populate Tier 2 truth.
- Ledger metadata must preserve `path_only_no_values` privacy posture and must
  not embed raw private Player.log excerpts, raw payload values, local logs,
  generated data, runtime status files, failed posts, workbook exports,
  secrets, credentials, tokens, webhook URLs, or API keys.

## Degradation Behavior

The Tier 2 entries must document degradation for:

- missing game-room config `eventId`;
- player-level `eventId` fallback use;
- blank or malformed player lists;
- stored `"Play"` event ID later replaced by a non-`"Play"` event ID;
- missing GameState `game_info.superFormat`;
- `MTGA Format` derived from event-id fallback instead of raw super-format;
- missing GameState `game_info.matchWinCondition`;
- `queue_type` derived from event-id markers;
- `queue_type` derived from sideboarding or total-games fallback;
- raw or novel `match_win_condition` pass-through;
- missing Rank payload fields;
- malformed rank payload fields that normalize to blank;
- constructed rank carried forward from a pre-match snapshot;
- limited rank fields present but not used for constructed rank;
- Mythic rank bucket collapsing exact percentile or number into `Mythic %` or
  `Mythic #`;
- competitive special events with unknown rankedness;
- novel Arena event IDs, super formats, queue descriptors, or win conditions;
- classifier outputs returning `unknown`;
- runtime history filters seeing blank or unknown context;
- disagreement between event ID, super format, match win condition, and
  classifier expectations.

Recommended drift flags:

- `missing_expected_payload_path`
- `new_unknown_payload_path`
- `fallback_used`
- `weak_fallback_used`
- `conflicting_evidence`
- `changed_signal_type`
- `schema_snapshot_missing`
- `fixture_gap`
- `sensitive_evidence_redacted`

## Unknowns And Suspected Gaps

Unknowns:

- Whether future Arena event descriptors will require new
  `EventIdentity.queue_subtype` values.
- Whether limited rank fields should eventually receive their own provenance
  field. They are out of scope for issue #167.
- Whether runtime field-evidence attachment will need row-level evidence
  payloads for `MTGA Format`, `MTGA Queue Type`, `My Rank`, or EventIdentity
  facets. That is deferred.
- Whether future analytics will need a separate `rankedness` or
  `analytics_segment` provenance field. That is deferred.

Suspected gaps:

- Queue type confidence can be weak when only sideboarding or total-games
  fallback supports Best of 3.
- Carried-forward rank snapshots are useful but not match-scoped direct
  evidence.
- EventIdentity unknown values are safe, but downstream analytics may need
  explicit review/degraded handling before using them as filters.
- Current tests may not assert the exact Tier 2 entry set because Tier 2 is
  currently registered future.

## Deferred Work

Defer all of the following:

- parser behavior changes
- event identity classifier behavior changes
- rank parser behavior changes
- match state parser behavior changes
- parser state final reconciliation changes
- parser event class changes
- workbook schema changes
- webhook payload changes
- Apps Script behavior changes
- output transport changes
- runtime field-evidence attachment
- schema snapshots
- invariant execution
- drift report implementation
- diagnostics report changes
- replay report changes
- feature-equity report changes
- Match Journal behavior
- overlay behavior
- SQLite behavior
- Google Sheets sync behavior
- analytics behavior
- archetype classification or suggestion behavior
- hidden-card inference
- complete decklist inference
- gameplay advice
- player-mistake labels
- model-provider behavior
- AI truth
- raw private Player.log evidence or local runtime artifact commits

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
python3 -m pytest -q tests/test_event_identity.py
python3 -m pytest -q tests/test_match_state_parser.py tests/test_state.py tests/test_app_models.py
python3 -m pytest -q tests/test_runtime_surfaces.py
```

Codex C should run a protected-surface check when available:

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence
```

Validation evidence must prove:

- Tier 2 family status becomes `seeded_sample`.
- Tier 2 `seed_fields` is exactly
  `["event_id", "super_format", "constructed_rank", "queue_type"]`.
- Tier 2 `future_fields` is exactly `[]`.
- The four Tier 2 entries validate under the existing ledger schema.
- Direct and fallback evidence paths are documented for each entry.
- `match_win_condition`, `mtga_format`, `mtga_queue_type`, `my_rank`,
  `rank_bucket`, constructed rank facets, EventIdentity fields, runtime
  filters, analytics segments, archetypes, Match Journal, overlays, SQLite,
  Google Sheets sync, model-provider output, and AI are not promoted to seed
  fields or truth owners.
- Prior Tier 1, Tier 3, Tier 4, and Tier 5 seed fields remain unchanged.
- Path-only privacy is preserved and no raw Player.log excerpts or raw payload
  values appear in ledger metadata or tests.

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md`
  exists.
- `src/mythic_edge_parser/app/evidence_ledger.py` is updated only for Tier 2
  metadata, the four Tier 2 entries, and related notes if Codex C implements.
- `tests/test_evidence_ledger.py` has focused tests for the Tier 2 family, the
  four entries, evidence paths, policies, degradation behavior, exact entry
  IDs, forbidden seed fields, and built-in ledger validation.
- No parser behavior, classifier behavior, rank parsing behavior, match state
  parsing behavior, workbook/webhook/App Script surface, output transport,
  runtime artifact shape, generated data, secrets, raw logs, runtime files,
  failed posts, workbook exports, production behavior, analytics truth, AI
  truth, or model-provider behavior changes are included.
- The implementation handoff explains untouched adjacent behavior and any
  remaining risks for future runtime field-evidence attachment, drift reports,
  schema snapshots, analytics grouping, or Tier 6/Tier 7 issues.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #167, Tier 2 queue/format/rank/event-context provenance under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/167
- Previous completed issue: #166
- Latest verified integration commit for this contract pass: 9f625ea0ef31cdbaa97a827a95ba3b4808562d11
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier2-context
- Contract: docs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md
- Expected implementation handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier2_queue_format_rank_event_context_comparison.md

Goal:
Implement only the metadata and focused test changes needed to satisfy the Tier 2 queue/format/rank/event-context contract. Seed exactly four Tier 2 evidence-ledger fields: event_id, super_format, constructed_rank, and queue_type. Preserve workbook labels, EventIdentity classifier facets, rank buckets, match_win_condition, runtime filters, analytics, archetype classification, Match Journal, overlay, SQLite, Google Sheets sync, model-provider output, and AI as facets/future/downstream boundaries rather than separate seed fields or truth owners.

Read first:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/parser_event_identity.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/event_identity.py
- src/mythic_edge_parser/parsers/match_state.py
- src/mythic_edge_parser/parsers/rank.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- tests/test_event_identity.py
- tests/test_match_state_parser.py
- tests/test_state.py
- tests/test_app_models.py
- tests/test_runtime_surfaces.py

Do:
- Compare current evidence-ledger behavior against the contract before editing.
- Change Tier 2 `queue_format_rank_event_context` from `registered_future` to `seeded_sample`.
- Add exactly these Tier 2 seed fields, in order: `event_id`, `super_format`, `constructed_rank`, `queue_type`.
- Set Tier 2 `future_fields` to an empty list.
- Add validating entries:
  - `tier2.queue_format_rank_event_context.event_id`
  - `tier2.queue_format_rank_event_context.super_format`
  - `tier2.queue_format_rank_event_context.constructed_rank`
  - `tier2.queue_format_rank_event_context.queue_type`
- Document direct and fallback evidence paths for MatchState event ID, player event ID fallback, GameState superFormat, GameState matchWinCondition, RankGetCombinedRankInfo constructed rank payload, carried-forward pre-match rank snapshots, model format/queue helpers, and EventIdentity classifier facets.
- Add focused tests proving the Tier 2 seed fields, entry IDs, policies, degradation behavior, and protected non-truth boundaries.
- Preserve prior Tier 1, Tier 3, Tier 4, and Tier 5 seed fields and entries.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_tier2_queue_format_rank_event_context_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Implement parser behavior changes.
- Change event identity classifier behavior, rank parsing behavior, match state parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, analytics truth, AI truth, model-provider behavior, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, or archetype classification behavior.
- Add seed fields for mtga_format, mtga_queue_type, match_win_condition, my_rank, rank_bucket, constructed_class, constructed_level, constructed_percentile, constructed_rank_source, limited rank fields, EventIdentity fields, runtime filter fields, analytics segments, archetypes, model-provider output, or AI.
- Infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, label player mistakes, or move analytics/AI truth into parser truth.
- Implement runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, feature-equity report changes, Match Journal behavior, overlay behavior, SQLite behavior, or Google Sheets sync changes.
- Commit raw private Player.log excerpts, raw payload values, local runtime artifacts, generated data, failed posts, runtime status files, workbook exports, secrets, tokens, credentials, webhook URLs, or API keys.
- Target main directly or close tracker #11.

Validation:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_event_identity.py
- python3 -m pytest -q tests/test_match_state_parser.py tests/test_state.py tests/test_app_models.py
- python3 -m pytest -q tests/test_runtime_surfaces.py if metadata references runtime filters
- python3 -m ruff check src tests tools
- git diff --check
- If available: python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/167"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier2_queue_format_rank_event_context_comparison.md"
  verdict: "contract_complete_ready_for_metadata_implementation"
  risk_tier: "Medium-High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier2-context"
  latest_verified_remote_commit: "9f625ea0ef31cdbaa97a827a95ba3b4808562d11"
  authorized_seed_fields:
    - "event_id"
    - "super_format"
    - "constructed_rank"
    - "queue_type"
  authorized_seed_entries:
    - "tier2.queue_format_rank_event_context.event_id"
    - "tier2.queue_format_rank_event_context.super_format"
    - "tier2.queue_format_rank_event_context.constructed_rank"
    - "tier2.queue_format_rank_event_context.queue_type"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_event_identity.py"
    - "python3 -m pytest -q tests/test_match_state_parser.py tests/test_state.py tests/test_app_models.py"
    - "python3 -m pytest -q tests/test_runtime_surfaces.py if metadata references runtime filters"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence if available"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #11."
    - "Do not implement parser behavior changes."
    - "Do not change event identity classifier behavior, rank parsing behavior, match state parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, analytics truth, AI truth, model-provider behavior, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, or archetype classification behavior."
    - "Do not add seed fields for mtga_format, mtga_queue_type, match_win_condition, my_rank, rank_bucket, constructed_class, constructed_level, constructed_percentile, constructed_rank_source, limited rank fields, EventIdentity fields, runtime filter fields, analytics segments, archetypes, model-provider output, or AI."
    - "Do not infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, label player mistakes, or move analytics/AI truth into parser truth."
    - "Do not implement runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, feature-equity report changes, Match Journal behavior, overlay behavior, SQLite behavior, or Google Sheets sync changes."
    - "Do not commit raw private Player.log excerpts, raw payload values, local runtime artifacts, generated data, failed posts, runtime status files, workbook exports, secrets, tokens, credentials, webhook URLs, or API keys."
```
