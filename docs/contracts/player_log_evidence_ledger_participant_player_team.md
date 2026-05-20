# Player.log Evidence Ledger Participant Player-Team Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/137
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/134
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/135
- previous_merge_commit: 9697a666f60fc60a8c13892b9815fd692056e298
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-participant-player-team
- target_artifact: docs/contracts/player_log_evidence_ledger_participant_player_team.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_participant_player_team_comparison.md
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
- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/player_log_evidence_ledger_tier3_game_results.md
- docs/contracts/parser_match_state.md
- docs/contracts/parser_gre_game_state.md
- docs/contracts/parser_client_actions.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_opponent_card_observations.md
- docs/decisions/ADR-0003-player-log-drift-policy.md

## Purpose

Issue #137 fills the participant and player-team provenance gap in the
Player.log evidence ledger.

Existing ledger entries can now explain match lifecycle fields, game-derived
aggregates, and game-level result fields. Those fields repeatedly depend on
local player team and seat/team mapping, but the ledger currently references
`MatchSummary.player_team` only as generic dependency language.

This contract defines how the evidence ledger should describe:

- the local player's team
- the opponent team derived from the local team
- the local system seat
- the participant seat/team mapping used by player-relative outputs

This is provenance metadata only. It must not change parser behavior, parser
state final reconciliation, event classes, workbook schema, webhook payload
shape, Apps Script behavior, output transport, match/game identity,
deduplication, or analytics truth.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, vocabulary constants, validators, and privacy posture.

`docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md` remains
authoritative for match identity, match result, and sync-status provenance.

`docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md` remains
authoritative for aggregate fields such as `games_won`, `games_lost`,
`match_win_flag`, and `game_win_rate`.

`docs/contracts/player_log_evidence_ledger_tier3_game_results.md` remains
authoritative for game winner and player-facing game result provenance.

Issue #137 should add the missing participant dependency entries and update
existing dependency references or notes where needed. It must not rewrite the
meaning of already mapped fields.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #137 provenance should be
recorded through this contract, implementation handoff, entry notes, and
focused tests rather than by changing the top-level ledger object shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- Player.log parser modules expose observed participant, seat, and team
  evidence.
- `src/mythic_edge_parser/app/extractors.py` owns current helper extraction for
  local player, local team, player seat, player team, and GameState system-seat
  mapping.
- `src/mythic_edge_parser/app/state.py` owns `current_player_team`,
  `_set_local_team(...)`, and how events update `MatchSummary.player_team`.
- `src/mythic_edge_parser/app/models.py` owns player-relative result
  derivation from `MatchSummary.player_team`.
- `src/mythic_edge_parser/app/gameplay_actions.py` owns current local-seat
  tracking for gameplay action actor relation labels.
- `src/mythic_edge_parser/app/opponent_card_observations.py` consumes local and
  actor seat mapping and degrades when seat mapping is missing.
- `src/mythic_edge_parser/app/evidence_ledger.py` describes provenance,
  confidence, finality, degradation, and review expectations.
- Workbook rows, Apps Script, webhook transport, dashboards, diagnostics,
  golden replay, feature-equity reports, drift reports, and AI output are
  downstream consumers only.

The ledger must not reconstruct missing GameState data, infer hidden
participants, infer hidden cards, infer decklists, classify archetypes, provide
gameplay advice, or move parser truth into workbook formulas, dashboard logic,
Apps Script, webhook transport, output transport, or AI.

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` after PR #135:

- `match_state.py` normalizes raw `reservedPlayers` or `players` into payload
  `players[]` entries with `user_id`, `player_name`, `system_seat_id`, and
  `team_id`.
- Missing raw `systemSeatId` or `teamId` in `match_state.py` currently becomes
  `0` in the normalized payload.
- `_safe_local_player(players)` returns the player at `LOCAL_PLAYER_INDEX` when
  the index is in range, otherwise the first player. It returns `{}` for
  malformed or empty player lists.
- `state.py` handles `MatchState` by using `_CONTEXT["current_player_team"]` or
  `summary.player_team` first, then `_safe_local_player(players).team_id` when
  no team is already known.
- `game_state.py` preserves `system_seat_ids` from raw `systemSeatIds` and
  preserves `players[]` from the GameState message.
- `_extract_local_team_from_game_state(payload)` treats the first normalized
  `system_seat_ids` value as the local system seat, then finds the matching
  GameState player record and returns that player's team.
- `_player_seat_id(...)` accepts `systemSeatNumber`, `systemSeatId`, or
  `system_seat_id`; `_player_team_id(...)` accepts `teamId` or `team_id`.
- `_extract_local_team_from_client_action(payload)` reads top-level `team_id`
  or `teamId`, then raw client-action payload fields, then nested
  `chooseStartingPlayerResp`, `mulliganResp`, and `submitDeckResp` fields.
- `_set_local_team(summary, team_id)` writes
  `_CONTEXT["current_player_team"]` and `summary.player_team` when `team_id` is
  not `None` or blank.
- `GameResult` handling copies `_CONTEXT["current_player_team"]` into the match
  summary when the context value is present.
- `MatchSummary.opponent_team()` currently derives `2` from local team `1`,
  derives `1` from local team `2`, and otherwise returns blank.
- `GameSummary.result_for_player(player_team)`, `MatchSummary.match_wl`,
  `game_wins`, `game_losses`, `match_win_flag`, `game_win_rate`, and
  `game_play_draw(...)` all depend on local player-team context.
- `gameplay_actions.py` stores `GameplayGameState.local_seat_id` from the first
  GameState `system_seat_ids` value and labels actor relation as `local`,
  `opponent`, or `unknown` by comparing object controller/owner seat to that
  local seat.
- `opponent_card_observations.py` emits observations only for entries already
  labeled `actor_relation == "opponent"` and degrades with
  `missing_seat_mapping` when actor or local seat mapping is unavailable.
- Existing evidence-ledger entries reference
  `parser_state.match_summary.player_team_dependency` for match result,
  aggregate, and per-game result fields.

Observed risk, not fixed by this issue:

- Current helper code can normalize `0`, booleans, or float-like values through
  Python integer conversion paths in some contexts. For participant provenance,
  this contract treats `0` and booleans as unknown-like values, even if current
  parser behavior can carry them. Correcting parser behavior requires a
  separate scoped contract.

## Scope Decision

Codex C should implement issue #137 as a Tier 1 dependency slice in the
existing `match_identity_and_lifecycle` output family.

Do not add a new output family. Do not add a workbook column, webhook field,
runtime status field, parser event class, or parser behavior path.

Required Tier 1 seed fields to add:

- `player_team`
- `opponent_team`
- `local_system_seat_id`
- `participant_team_mapping`

Required Tier 1 entries:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier1.participants.player_team` | `player_team` | `player_team` | `observed` or `derived` |
| `tier1.participants.opponent_team` | `opponent_team` | `opponent_team` | `derived` |
| `tier1.participants.local_system_seat_id` | `local_system_seat_id` | `local_system_seat_id` | `observed` or `derived` |
| `tier1.participants.participant_team_mapping` | `participant_team_mapping` | `participant_team_mapping` | `observed` or `derived` |

Do not add `participant_mapping_confidence` as a field entry in this issue.
Confidence belongs in the existing ledger evidence vocabulary through each
entry's `confidence_policy`, evidence signals, `drift_flags`, and future
field-evidence attachments.

Required family metadata:

- Keep `match_identity_and_lifecycle.status` as `seeded_sample`.
- Add the four participant seed fields to
  `match_identity_and_lifecycle.seed_fields`.
- Add notes stating that issue #137 maps participant/team dependency
  provenance used by prior #130, #132, and #134 entries.
- Keep Tier 2-7 future fields registered but do not complete them in issue
  #137.

## Deferred Work

Defer all of the following:

- parser behavior changes
- local player selection behavior or `LOCAL_PLAYER_INDEX` semantics
- runtime field-evidence attachment
- drift reports
- schema snapshots
- invariant execution
- diagnostics report changes
- golden replay report changes
- feature-equity report changes
- workbook schema changes
- webhook or output transport changes
- Apps Script mapping changes
- opponent-card observation behavior changes
- gameplay action actor-relation behavior changes
- future play/draw provenance entries
- future opening-hand ownership provenance entries
- future opponent-card observation ledger entries
- future analytics consumer rules

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_participant_player_team.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_participant_player_team_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_participant_player_team.md

Referenced but not owned:

- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/player_log_evidence_ledger_tier3_game_results.md
- docs/contracts/parser_match_state.md
- docs/contracts/parser_gre_game_state.md
- docs/contracts/parser_client_actions.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_opponent_card_observations.md
- src/mythic_edge_parser/app/extractors.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- src/mythic_edge_parser/parsers/match_state.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- src/mythic_edge_parser/parsers/client_actions.py
- tests/test_state.py
- tests/test_app_extractors.py
- tests/test_gameplay_actions.py
- tests/test_opponent_card_observations.py

## Public Interface

Recommended implementation surface:

```python
src/mythic_edge_parser/app/evidence_ledger.py
```

Public constants and functions from prior evidence-ledger work must remain
stable:

- `LEDGER_OBJECT`
- `LEDGER_SCHEMA_VERSION`
- `LEDGER_VERSION`
- `FIELD_EVIDENCE_OBJECT`
- `FIELD_EVIDENCE_SCHEMA_VERSION`
- `VALUE_SOURCES`
- `CONFIDENCE_LEVELS`
- `FINALITY_LABELS`
- `INVARIANT_STATUSES`
- `DRIFT_FLAGS`
- `build_player_log_evidence_ledger()`
- `iter_ledger_entries()`
- `validate_player_log_evidence_ledger(...)`
- `validate_ledger_entry(...)`
- `validate_field_evidence(...)`

No new runtime parser API is required.

Required ledger-entry behavior:

- `iter_ledger_entries()` remains deep-copy safe.
- `build_player_log_evidence_ledger()` remains deterministic and JSON
  serializable.
- Every new participant entry passes `validate_ledger_entry(...)`.
- The built ledger passes `validate_player_log_evidence_ledger(...)`.
- Entry IDs and signal IDs remain stable, lowercase, and dot-separated.
- Source paths remain repo-relative or symbolic.
- Raw payload values, raw private log excerpts, absolute local paths, secrets,
  webhook URLs, local runtime artifacts, generated data, failed posts, and
  workbook exports must not be embedded.

## Participant Field Inventory

### `player_team`

Meaning:

- The parser-owned local player team used to derive player-relative match,
  game, aggregate, play/draw, and local/opponent labels.

Current surfaces:

- `_CONTEXT["current_player_team"]`
- `MatchSummary.player_team`
- `MatchState.payload.players[].team_id`
- `GameState.payload.system_seat_ids[0]` plus `GameState.payload.players[]`
- `ClientAction.payload.team_id` or nested `teamId`

Output role:

- Dependency field, not a new workbook or webhook output.

### `opponent_team`

Meaning:

- The opponent team derived from known local `player_team` for current two-team
  MTGA match assumptions.

Current surfaces:

- `MatchSummary.opponent_team()`
- downstream play/draw and seat/team reasoning

Output role:

- Dependency field, not a new workbook or webhook output.

### `local_system_seat_id`

Meaning:

- The local player's system seat identifier used to resolve local/private zones
  and local/opponent actor relation labels.

Current surfaces:

- `GameState.payload.system_seat_ids[0]`
- raw `greToClientMessages[].systemSeatIds[0]`
- MatchState player `system_seat_id` selected by `_safe_local_player(...)`
- `GameplayGameState.local_seat_id`
- opponent-card observation input `local_seat_id`

Output role:

- Dependency field, not a new workbook or webhook output.

### `participant_team_mapping`

Meaning:

- A provenance description of how local seat, local team, opponent team, and
  available participant records relate for the current match.

Current surfaces:

- MatchState selected local player record
- GameState `system_seat_ids` plus `players[]` records
- ClientAction team fields as supplemental evidence
- parser context carry-forward within the active match
- gameplay action actor relation labels
- opponent-card observation degradation flags

Output role:

- Dependency field, not a new workbook or webhook output.

## Source Evidence Priority

This priority is for ledger confidence and provenance language. It must not be
implemented as a parser behavior change in issue #137.

### Strong Direct Evidence

Use high-confidence `observed` provenance when current match evidence includes
non-conflicting participant data from:

- GameState `systemSeatIds[0]` plus a `players[]` record with matching
  `systemSeatNumber` or `systemSeatId` and known nonzero `teamId`.
- MatchState selected local player data from `_safe_local_player(...)` when the
  configured local player index is in range and provides known nonzero
  `team_id` and optional seat data.
- Corroborated MatchState and GameState participant evidence that agree on
  local team and seat mapping.

### Supplemental Evidence

Use medium-confidence `observed` or `derived` provenance when participant data
comes from:

- ClientAction top-level `team_id` or `teamId`.
- ClientAction nested `chooseStartingPlayerResp.teamId`,
  `mulliganResp.teamId`, or `submitDeckResp.teamId`.
- MatchState selected local player fallback to the first player because
  `LOCAL_PLAYER_INDEX` is out of range.
- Parser-produced top-level payload fields that lack enough seat context to
  prove the full mapping.

ClientAction team evidence may corroborate or repair confidence language for
the current match, but it must not silently override contradictory MatchState
or GameState evidence in ledger wording.

### Parser Context Carry-Forward

Use medium-confidence `derived` and `provisional` provenance when
`_CONTEXT["current_player_team"]` or `MatchSummary.player_team` is carried
within a known current match.

Use low-confidence `derived` and review-required provenance when context might
be stale, detached from a known match id, or contradicted by later participant
evidence.

Context carry-forward across a match boundary is not acceptable high-confidence
participant evidence.

### Derived Opponent Identity

`opponent_team` is derived only from known local `player_team`.

Current model behavior derives:

- local team `1` -> opponent team `2`
- local team `2` -> opponent team `1`
- any other local team -> blank

Do not hard-code new opponent-team behavior in issue #137. The ledger may say
that non-`1`/`2` local teams cannot currently produce a high-confidence
`opponent_team` through `MatchSummary.opponent_team()`.

## Unknown-Like Values

For participant provenance, these values are unknown and must not be described
as valid high-confidence player/team/seat identifiers:

- `None`
- `""`
- whitespace-only strings
- `0`
- `0.0`
- `"0"`
- `" 0 "`
- booleans

Nonzero integer-like values may be valid observed identifiers, but confidence
depends on source context and conflicts.

This unknown-like policy is a provenance guarantee. It does not change current
parser normalization or assignment behavior in issue #137.

## Output Entries

### `tier1.participants.player_team`

Field meaning:

- Parser field: `MatchSummary.player_team`
- Context alias: `_CONTEXT["current_player_team"]`
- Dependency alias used by prior entries:
  `parser_state.match_summary.player_team_dependency`

Required evidence policy:

- `observed` from current MatchState selected local player team.
- `observed` from current GameState local system seat to player team mapping.
- `observed` or `derived` from ClientAction team fields as supplemental
  current-match evidence.
- `derived` from parser context carry-forward within the active match.
- `unknown` when missing, blank, zero-like, boolean, stale, detached from
  match identity, or contradictory.

Required signal examples:

- `match_state.players.selected_local_player_team`
- `game_state.system_seat_ids.local_player_team`
- `client_action.local_player_team`
- `parser_context.current_player_team`
- `parser_state.match_summary.player_team`

Required invariants:

- player-facing result fields require known non-conflicting `player_team` for
  high confidence.
- known match/game winners alone are insufficient for high-confidence
  player-facing win/loss.
- zero-like and boolean team values are unknown for provenance.
- context carry-forward is not high-confidence when match identity is missing
  or stale.

### `tier1.participants.opponent_team`

Field meaning:

- Model surface: `MatchSummary.opponent_team()`
- Derived participant dependency for local/opponent reasoning.

Required evidence policy:

- `derived` from known local `player_team`.
- High confidence only when `player_team` is high-confidence and is currently
  supported by the two-team `1`/`2` model behavior.
- `unknown` when `player_team` is missing, degraded, conflicting, not `1` or
  `2`, or stale.

Required signal examples:

- `parser_state.match_summary.opponent_team`
- `ledger.tier1.participants.player_team_dependency`

Required invariants:

- opponent team is not directly observed by workbook formulas, dashboards, AI,
  or output transport.
- opponent team must not be guessed when local team is unknown.
- opponent team derivation must not create hidden information claims.

### `tier1.participants.local_system_seat_id`

Field meaning:

- Parser/GameState field: local system seat used to map local/private zones and
  actor relation labels.
- Gameplay surface: `GameplayGameState.local_seat_id`.

Required evidence policy:

- `observed` from current GameState `systemSeatIds[0]`.
- `observed` from selected MatchState local player `systemSeatId` when
  available and nonzero.
- `derived` from current gameplay action local-seat state only as parser-owned
  carry-forward evidence.
- `unknown` when missing, blank, zero-like, boolean, stale, or contradictory.

Required signal examples:

- `game_state.system_seat_ids.local_system_seat`
- `match_state.players.selected_local_player_seat`
- `gameplay_actions.local_seat_id`

Required invariants:

- local private zone interpretation requires known local seat for high
  confidence.
- actor relation labels require known local and actor seats for high
  confidence.
- missing local seat must be reviewable through degradation language rather
  than silently treated as opponent evidence.

### `tier1.participants.participant_team_mapping`

Field meaning:

- The ledger dependency explaining whether local seat, local team, opponent
  team, and participant records agree for the current match.

Required evidence policy:

- `observed` when current MatchState or GameState includes enough non-conflicting
  seat/team records to map local participant identity.
- `derived` when the mapping is assembled from local seat plus known
  `player_team` and `opponent_team`.
- `unknown` when local seat or local team is missing.
- `conflict` when MatchState, GameState, ClientAction, context, or gameplay
  action evidence disagree in a way that can invert local/opponent labels.

Required signal examples:

- `match_state.players.participant_team_mapping`
- `game_state.players.participant_team_mapping`
- `client_action.participant_team_supplement`
- `parser_context.participant_team_carry_forward`
- `opponent_card_observations.missing_seat_mapping_dependency`

Required invariants:

- participant mapping must stay parser-owned.
- missing mapping degrades player-facing and local/opponent-dependent outputs.
- conflicting mapping requires review and low confidence.
- participant mapping must not infer hidden opponent identity, cards, decklists,
  archetypes, or advice.

## Dependency Map To Existing Entries

Codex C should update existing ledger entries or notes so participant
dependencies are explicit.

Required dependency links:

- `tier1.match_lifecycle.match_result` depends on
  `tier1.participants.player_team`.
- `tier1.game_aggregates.games_won` depends on
  `tier1.participants.player_team`.
- `tier1.game_aggregates.games_lost` depends on
  `tier1.participants.player_team`.
- `tier1.game_aggregates.match_win_flag` depends on
  `tier1.participants.player_team`.
- `tier1.game_aggregates.game_win_rate` depends on
  `tier1.participants.player_team` through `games_won` and `games_lost`.
- `tier3.game_results.game1_result` depends on
  `tier1.participants.player_team`.
- `tier3.game_results.game2_result` depends on
  `tier1.participants.player_team`.
- `tier3.game_results.game3_result` depends on
  `tier1.participants.player_team`.

Future dependency links, not implemented in issue #137:

- play/draw depends on `player_team`, `opponent_team`, and starting-player
  provenance.
- opening-hand and local-zone provenance depends on `local_system_seat_id`.
- opponent-card observations depend on `local_system_seat_id` and
  `participant_team_mapping`.
- analytics confidence depends on participant mapping confidence but must not
  become parser truth.

Existing signal ID compatibility:

- Current entries may already reference
  `parser_state.match_summary.player_team_dependency`.
- Codex C may preserve that signal ID for backward readability, add a new
  `ledger.tier1.participants.player_team_dependency` signal, or update notes to
  point to `tier1.participants.player_team`.
- If a signal ID changes, focused tests must prove all dependent entries still
  reference participant provenance explicitly.

## Confidence, Finality, And Degradation Rules

Use existing vocabulary only:

- `value_source`: `observed`, `derived`, `unknown`, `conflict`
- `confidence`: `high`, `medium`, `low`, `unknown`
- `finality`: `live`, `provisional`, `final`, `reconciled`
- drift/degradation flags from the existing `DRIFT_FLAGS` vocabulary

Required policies:

- Direct, current, non-conflicting GameState seat/team mapping may be high
  confidence.
- Direct, current, non-conflicting MatchState selected local player team may be
  high confidence when local selection is configured and in range.
- ClientAction team fields are supplemental and should not be high confidence
  alone unless corroborated by stronger participant evidence.
- Parser context carry-forward inside a known match is medium confidence and
  provisional.
- Stale or matchless context is low confidence and review-required.
- Missing participant mapping is `unknown`.
- Contradictory participant evidence is `conflict`, low confidence, and
  review-required.
- Participant entries are generally `live` or `provisional` during active
  parsing and may be `final` once final match result evidence exists without
  later stronger participant correction.
- If later stronger participant evidence corrects a final value, use
  `reconciled` in future field-evidence language.

Required degradation behavior:

- missing player team prevents high-confidence player-facing `W` / `L`.
- missing local seat prevents high-confidence local/private zone and actor
  relation labels.
- conflicting participant mapping can invert results and actor labels, so it
  must be visible in entry degradation text.
- zero-like and boolean participant identifiers are unknown for provenance.
- known winner evidence does not repair missing participant evidence.

## Privacy And Serialization Rules

Participant provenance must remain path-only and metadata-only.

The contract allows symbolic raw paths such as:

- `matchGameRoomStateChangedEvent.gameRoomInfo.gameRoomConfig.reservedPlayers[].teamId`
- `matchGameRoomStateChangedEvent.gameRoomInfo.gameRoomConfig.reservedPlayers[].systemSeatId`
- `greToClientMessages[].systemSeatIds[0]`
- `greToClientMessages[].gameStateMessage.players[].teamId`
- `ClientToGREMessage.payload.*.teamId`

The contract forbids embedding:

- raw player names
- raw user ids
- raw private Player.log excerpts
- raw log paths
- secrets
- tokens
- webhook URLs
- Apps Script URLs
- local runtime status artifacts
- failed posts
- generated data
- workbook exports

## Compatibility Expectations

Implementation must preserve:

- ledger schema version unless a separate contract authorizes a version bump
- public evidence-ledger constants and validators
- current parser behavior
- current event classes and parser payload shapes
- current workbook schema
- current webhook payload shape
- current Apps Script behavior
- current output transport
- current match/game identity and deduplication behavior
- current opponent-card observation and gameplay action behavior

Implementation may change:

- evidence-ledger registry entries
- evidence-ledger family seed-field metadata
- evidence-ledger entry notes and dependency signals
- focused evidence-ledger tests
- implementation handoff and contract-test report docs

## Test Obligations

Codex C must add or update focused tests in `tests/test_evidence_ledger.py`.

Required assertions:

- `match_identity_and_lifecycle.seed_fields` includes `player_team`,
  `opponent_team`, `local_system_seat_id`, and
  `participant_team_mapping`.
- `tier1.participants.player_team` exists and validates.
- `tier1.participants.opponent_team` exists and validates.
- `tier1.participants.local_system_seat_id` exists and validates.
- `tier1.participants.participant_team_mapping` exists and validates.
- participant entries use existing vocabulary only.
- participant entries use path-only privacy and do not embed raw values.
- `player_team` degradation text treats missing, blank, zero-like, and boolean
  values as unknown for provenance.
- `opponent_team` is derived from `player_team` and does not infer when
  `player_team` is unknown.
- `local_system_seat_id` cites GameState `systemSeatIds[0]` and degrades
  missing or conflicting seat mapping.
- `participant_team_mapping` cites MatchState, GameState, ClientAction, parser
  context, and downstream missing-seat-mapping dependencies.
- existing match result, aggregate, and game result entries explicitly cite
  participant/player-team provenance.
- `validate_player_log_evidence_ledger()` returns `[]`.
- every built-in entry passes `validate_ledger_entry(...)`.

Recommended adjacent behavior tests to run as evidence, not to change behavior:

- `tests/test_state.py`
- `tests/test_app_extractors.py`
- `tests/test_gameplay_actions.py`
- `tests/test_opponent_card_observations.py`

Validation commands for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
python3 -m pytest -q
python3 -m ruff check src tests tools
git diff --check
```

If protected-surface tooling is available in the branch, Codex C should run the
repo's protected-surface checks and report `forbidden 0`.

## Acceptance Criteria

Issue #137 is implementation-ready when:

- this contract exists at
  `docs/contracts/player_log_evidence_ledger_participant_player_team.md`.
- Codex C can implement the participant dependency slice with evidence-ledger
  metadata and tests only.
- no parser behavior changes are required.
- no protected surface changes are required.
- participant dependencies are explicit enough for Codex E to verify prior
  #130, #132, and #134 entries.
- missing, unknown, stale, and conflicting participant evidence is represented
  as degraded or unknown in metadata language.
- the route to Codex C is unambiguous.

## Recommended Next Role

Next role: Codex C / Module Implementer.

Codex C should implement the smallest coherent evidence-ledger registry and
test changes needed to satisfy this contract. It should not change parser
behavior.

## Pasteable Codex C Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #137, participant/player-team provenance under issue #11.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/137
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/134
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/135
    - Previous merge commit: 9697a666f60fc60a8c13892b9815fd692056e298
    - Base branch: codex/parser-reliability-intelligence
    - Recommended implementation branch: codex/player-log-evidence-ledger-participant-player-team
    - Contract: docs/contracts/player_log_evidence_ledger_participant_player_team.md
    - Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_participant_player_team_comparison.md

  Goal:
    Implement the participant/player-team evidence-ledger dependency slice defined by the contract. Add or update evidence-ledger metadata and focused tests only.

  Read first:
    - AGENTS.md
    - docs/agent_rules.yml
    - docs/agent_constitution.md
    - docs/codex_module_workflow.md
    - docs/agent_threads/implementation.md
    - docs/contracts/player_log_evidence_ledger_participant_player_team.md
    - docs/contracts/player_log_evidence_ledger_schema.md
    - docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
    - docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
    - docs/contracts/player_log_evidence_ledger_tier3_game_results.md
    - src/mythic_edge_parser/app/evidence_ledger.py
    - tests/test_evidence_ledger.py
    - src/mythic_edge_parser/app/extractors.py
    - src/mythic_edge_parser/app/state.py
    - src/mythic_edge_parser/app/models.py
    - src/mythic_edge_parser/app/gameplay_actions.py
    - src/mythic_edge_parser/app/opponent_card_observations.py

  Do:
    - Compare current evidence-ledger metadata against the contract before editing.
    - Add Tier 1 participant seed fields for player_team, opponent_team, local_system_seat_id, and participant_team_mapping.
    - Add validating ledger entries for tier1.participants.player_team, tier1.participants.opponent_team, tier1.participants.local_system_seat_id, and tier1.participants.participant_team_mapping.
    - Make existing match result, aggregate, and game result entries explicitly cite participant/player-team provenance.
    - Keep privacy path-only and do not embed raw player values.
    - Add focused tests in tests/test_evidence_ledger.py.
    - Produce docs/implementation_handoffs/player_log_evidence_ledger_participant_player_team_comparison.md with comparison, changes made, validation, risks, and next recommended role.

  Do not:
    - Change parser behavior.
    - Change local player selection behavior or LOCAL_PLAYER_INDEX semantics.
    - Change parser state final reconciliation.
    - Change parser event classes.
    - Change workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or production behavior.
    - Change opponent-card observation behavior or gameplay actor-relation behavior.
    - Add runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, or feature-equity report changes.
    - Infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, or AI/analytics truth.
    - Commit raw private Player.log excerpts.
    - Target main directly.
    - Close issue #11.
    - Stage or commit unless explicitly asked.

  Validation:
    - python3 -m pytest -q tests/test_evidence_ledger.py
    - python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
    - python3 -m pytest -q
    - python3 -m ruff check src tests tools
    - git diff --check

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/137"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/134"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/135"
  previous_merge_commit: "9697a666f60fc60a8c13892b9815fd692056e298"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_participant_player_team.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_participant_player_team_comparison.md"
  verdict: "participant_player_team_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-participant-player-team"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not change local player selection behavior or LOCAL_PLAYER_INDEX semantics."
    - "Do not change opponent-card observation behavior or gameplay actor-relation behavior."
    - "Do not reconstruct missing GameState data or infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, or AI/analytics truth."
    - "Do not commit raw private Player.log excerpts or local diagnostics artifacts."
```

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/137"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/134"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/135"
  previous_merge_commit: "9697a666f60fc60a8c13892b9815fd692056e298"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_participant_player_team.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_participant_player_team_comparison.md"
  verdict: "participant_player_team_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-participant-player-team"
  validation:
    - "not run - contract writer pass"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not implement code in Codex B."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not change local player selection behavior or LOCAL_PLAYER_INDEX semantics."
    - "Do not change opponent-card observation behavior or gameplay actor-relation behavior."
    - "Do not reconstruct missing GameState data or infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, or AI/analytics truth."
    - "Do not commit raw private Player.log excerpts or local diagnostics artifacts."
