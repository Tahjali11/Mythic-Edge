# Player.log Evidence Ledger Tier 3 Play/Draw Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/139
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/137
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/138
- previous_merge_commit: 869491a7999ebf2510c19925f1f671d1f37f2113
- parallel_issue: https://github.com/Tahjali11/Mythic-Edge/issues/140
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier3-play-draw
- target_artifact: docs/contracts/player_log_evidence_ledger_tier3_play_draw.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier3_play_draw_comparison.md
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
- docs/contracts/player_log_evidence_ledger_participant_player_team.md
- docs/contracts/player_log_evidence_ledger_tier3_game_results.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/parser_client_actions.md
- docs/contracts/parser_gre_game_state.md
- docs/contracts/parser_gre_turn_info.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- docs/decisions/ADR-0003-player-log-drift-policy.md

## Purpose

Issue #139 maps Tier 3 starting-player and play/draw provenance in the
Player.log evidence ledger.

Play/draw is not a standalone raw Player.log fact. It is a parser-owned derived
value built from starting-player evidence plus local player-team context.
Starting-player evidence can be explicit, observed from turn-one GameState
active-player data, or inferred for later games from the previous game winner.

This contract documents provenance metadata only. It must not change parser
behavior, starting-player extraction, later-game inference, parser state final
reconciliation, event classes, workbook schema, webhook payload shape, Apps
Script behavior, output transport, match/game identity, deduplication, or
analytics truth.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, validators, vocabulary constants, and privacy posture.

`docs/contracts/player_log_evidence_ledger_participant_player_team.md` remains
authoritative for `player_team`, `opponent_team`, `local_system_seat_id`, and
participant mapping provenance. Issue #139 depends on those entries and must
not redefine participant truth.

`docs/contracts/player_log_evidence_ledger_tier3_game_results.md` remains
authoritative for `game_number`, per-game winners, and per-game result
provenance. Issue #139 depends on prior-game winner provenance for inferred
later-game starting player values.

`docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md` remains
authoritative for aggregate match fields. Issue #139 may cite aggregate
consumers but must not change aggregate math.

Issue #140 covers mulligan provenance in a parallel contract. Issue #139 must
not seed mulligan ledger entries, change mulligan counting, or depend on
unmerged #140 implementation details.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #139 provenance should be
recorded through this contract, implementation handoff, entry notes, and
focused tests rather than by changing the top-level ledger object shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- ClientAction parsing preserves explicit choose-starting-player response
  evidence as parser input.
- GRE GameState parsing preserves turn-one active-player and player mapping
  evidence as parser input.
- `src/mythic_edge_parser/app/extractors.py` owns current helper extraction for
  starting-player values from ClientAction and GameState payloads.
- `src/mythic_edge_parser/app/state.py` owns how ClientAction and GameState
  events update `GameSummary.starting_player`.
- `src/mythic_edge_parser/app/models.py` owns
  `GameSummary.starting_player`, `GameSummary.play_draw(...)`,
  `MatchSummary.effective_starting_player(...)`, and
  `MatchSummary.game_play_draw(...)`.
- `src/mythic_edge_parser/app/evidence_ledger.py` describes provenance,
  confidence, finality, degradation, and review expectations.
- Workbook rows, Apps Script, webhook transport, dashboards, diagnostics,
  golden replay, feature-equity reports, drift reports, and AI output are
  downstream consumers only.

The ledger must not reconstruct missing GameState data, infer hidden cards,
infer decklists, classify archetypes, provide gameplay advice, infer player
mistakes, or move parser truth into workbook formulas, dashboard logic, Apps
Script, webhook transport, output transport, or AI.

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` after PR #138:

- The Tier 3 `game_level_facts` family is already `seeded_sample` for game
  number, game winners, and game results.
- The same family still lists broad future fields `play_draw` and
  `starting_player`.
- `client_actions.py` does not emit a specialized choose-starting-player event;
  unknown client-action messages become `generic_client_action` payloads with
  `message_type` and `raw_client_action`.
- `_extract_starting_player_from_client_action(...)` reads top-level
  `starting_player_system_seat_id`, `startingPlayerSystemSeatId`,
  `chosen_system_seat_id`, `chosenSystemSeatId`, `system_seat_id`,
  `systemSeatId`, `seat_id`, `seatId`, `selected_system_seat_id`, or
  `selectedSystemSeatId`, then the same fields inside raw
  `ClientToGREMessage.payload`, then the same fields inside
  `chooseStartingPlayerResp`.
- `_extract_starting_player_from_client_action(...)` returns the raw value
  shape and does not coerce it to an integer.
- `state.py` handles generic ClientAction
  `ClientMessageType_ChooseStartingPlayerResp` by setting the current game's
  starting player from `_extract_starting_player_from_client_action(...)`.
- `turn_info.py` normalizes `turnNumber` and `activePlayer` /
  `activePlayerSeatId` into `turn_number` and `active_player_seat_id`.
- `game_state.py` preserves normalized `turn_info`, `identity`,
  `active_player_seat_id`, `players[]`, and `system_seat_ids`.
- `_extract_starting_player_from_game_state(...)` returns `None` unless the
  GameState turn number is exactly `1`.
- On turn one, `_extract_starting_player_from_game_state(...)` uses
  `active_player_seat_id`. If a matching `players[]` record has a team id, it
  returns the team id; otherwise it returns the active seat id.
- `state.py` handles GameState by calling `set_game_starting_player(...)` for
  the current game using `_extract_starting_player_from_game_state(...)`.
- `MatchSummary.set_game_starting_player(...)` stores any value except `None`
  and `""` for valid game slots.
- `_play_draw_label(starting_player, player_team)` returns blank if either
  value is `None` or `""`; otherwise it returns `Play` when the values are
  equal and `Draw` when they differ.
- `GameSummary.play_draw(player_team)` uses the stored
  `GameSummary.starting_player` directly.
- `MatchSummary.effective_starting_player(game_number)` returns explicit
  `GameSummary.starting_player` first.
- If a later game has summary data but no explicit starting player,
  `MatchSummary.effective_starting_player(...)` infers the starter from the
  previous game winner and local player team:
  - if the previous game winner equals `player_team`, the next starter is
    `opponent_team()`;
  - otherwise the next starter is `player_team`.
- `MatchSummary.game_play_draw(game_number)` derives `Play` / `Draw` from
  `effective_starting_player(...)` plus `player_team`.
- Match-log row fields `G1 Play / Draw`, `G2 Play / Draw`, and
  `G3 Play / Draw` use `MatchSummary.game_play_draw(...)`.
- Game-log row field `Play / Draw` also uses `MatchSummary.game_play_draw(...)`.
- Debug/history fields include `g1_starting_player`, `g2_starting_player`,
  `g3_starting_player`, `g1_play_draw`, `g2_play_draw`, and `g3_play_draw`.

Observed risks, not fixed by this issue:

- Current starting-player setters can retain zero-like, boolean, or seat-only
  values. The provenance contract treats those as unknown or degraded when
  they cannot be tied to a known team, but issue #139 must not change parser
  behavior.
- A seat id can numerically equal a team id in common two-player matches. The
  ledger must not overstate confidence when the source is seat-only evidence
  and team mapping is missing.

## Scope Decision

Codex C should implement issue #139 as a Tier 3 `game_level_facts` metadata
slice in the existing evidence ledger.

Do not add a new output family. Do not add a workbook column, webhook field,
runtime status field, parser event class, or parser behavior path.

Required Tier 3 seed fields to add:

- `game1_starting_player`
- `game2_starting_player`
- `game3_starting_player`
- `game1_play_draw`
- `game2_play_draw`
- `game3_play_draw`

Required Tier 3 entries:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier3.play_draw.game1_starting_player` | `game1_starting_player` | `g1_starting_player` | `observed` or `derived` |
| `tier3.play_draw.game2_starting_player` | `game2_starting_player` | `g2_starting_player` | `observed`, `derived`, or `inferred` |
| `tier3.play_draw.game3_starting_player` | `game3_starting_player` | `g3_starting_player` | `observed`, `derived`, or `inferred` |
| `tier3.play_draw.game1_play_draw` | `game1_play_draw` | `G1 Play / Draw` | `derived` |
| `tier3.play_draw.game2_play_draw` | `game2_play_draw` | `G2 Play / Draw` | `derived` |
| `tier3.play_draw.game3_play_draw` | `game3_play_draw` | `G3 Play / Draw` | `derived` |

Required family metadata:

- Keep `game_level_facts.status` as `seeded_sample`.
- Add the six fields above to `game_level_facts.seed_fields`.
- Remove broad `play_draw` and `starting_player` from
  `game_level_facts.future_fields` once the granular seed fields are added.
- Keep remaining future fields, at minimum:
  - `mulligans`
  - `turn_count`
  - `opening_hand`
  - `game_timing`
  - `game_duration`
  - `pre_postboard`
  - `sideboarding`
  - `deck_state`
- Add notes stating that issue #139 maps the starting-player and play/draw
  provenance slice and depends on #137 participant provenance plus #134
  game-result provenance.

## Deferred Work

Defer all of the following:

- parser behavior changes
- starting-player extraction changes
- later-game starting-player inference changes
- parser state final reconciliation changes
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
- match/game identity or deduplication changes
- mulligan provenance, which belongs to issue #140
- opening-hand provenance
- turn-count provenance
- timing and duration provenance
- pre/postboard, sideboarding, or deck-state provenance
- analytics consumer rules

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier3_play_draw.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier3_play_draw_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier3_play_draw.md

Referenced but not owned:

- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_participant_player_team.md
- docs/contracts/player_log_evidence_ledger_tier3_game_results.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/parser_client_actions.md
- docs/contracts/parser_gre_game_state.md
- docs/contracts/parser_gre_turn_info.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- src/mythic_edge_parser/app/extractors.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/parsers/client_actions.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- src/mythic_edge_parser/parsers/gre/turn_info.py
- tests/test_app_extractors.py
- tests/test_app_models.py
- tests/test_match_summary_from_match_state.py
- tests/test_state.py
- tests/test_golden_replay_harness.py
- tests/fixtures/golden_replay/*.manifest.json
- tests/fixtures/parser_regression_*_expected.json

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
- Every new play/draw entry passes `validate_ledger_entry(...)`.
- The built ledger passes `validate_player_log_evidence_ledger(...)`.
- Entry IDs and signal IDs remain stable, lowercase, and dot-separated.
- Source paths remain repo-relative or symbolic.
- Raw payload values, raw private log excerpts, absolute local paths, secrets,
  webhook URLs, local runtime artifacts, generated data, failed posts, and
  workbook exports must not be embedded.

## Field Inventory

### `gameN_starting_player`

Meaning:

- The effective starting-player value for fixed game slot `N`, where `N` is
  `1`, `2`, or `3`.
- This value may be explicit, observed from turn-one GameState evidence, or
  inferred by model logic for later games.

Current surfaces:

- `GameSummary.starting_player`
- `MatchSummary.effective_starting_player(N)`
- `MatchSummary.to_debug_dict()` fields `g1_starting_player`,
  `g2_starting_player`, and `g3_starting_player`
- GameState and ClientAction state update paths

Output role:

- Parser-owned dependency field for play/draw.
- Debug/history field.
- Not a new workbook or webhook schema field.

### `gameN_play_draw`

Meaning:

- The player-facing `Play` / `Draw` label for fixed game slot `N`, derived
  from effective starting player plus local `player_team`.

Current surfaces:

- `MatchSummary.game_play_draw(N)`
- `MatchSummary._game_play_draw_fields()`
- Match-log row fields `G1 Play / Draw`, `G2 Play / Draw`,
  `G3 Play / Draw`
- Game-log row field `Play / Draw`
- Debug/history fields `g1_play_draw`, `g2_play_draw`, `g3_play_draw`

Output role:

- Parser-owned derived field.
- Workbook-visible downstream aliases already exist; issue #139 must not
  change their shape.

## Source Evidence Priority

This priority is for ledger confidence and provenance language. It must not be
implemented as a parser behavior change in issue #139.

Priority order for provenance metadata:

1. explicit current-game `ClientMessageType_ChooseStartingPlayerResp` evidence
2. turn-one GameState active-player evidence
3. current parser state/model surfaces that preserve or expose those values
4. later-game inference from previous game winner plus participant context
5. unknown/degraded fallback when required dependencies are missing or
   contradictory

Parser state/model surfaces are evidence consumers and exposed parser-owned
fields in this contract. They are not independent raw evidence sources that can
override clearer ClientAction or GameState evidence.

### Explicit ClientAction Evidence

Use high-confidence `observed` provenance when a current-game
`ClientMessageType_ChooseStartingPlayerResp` supplies a non-conflicting
starting-player value that can be mapped to a known team.

Relevant normalized helper:

- `_extract_starting_player_from_client_action(payload)`

Relevant raw paths include:

- `ClientToGREMessage.payload.systemSeatId`
- `ClientToGREMessage.payload.seatId`
- `ClientToGREMessage.payload.chooseStartingPlayerResp.systemSeatId`
- `ClientToGREMessage.payload.chooseStartingPlayerResp.seatId`

If the explicit value is seat-only and cannot be mapped to a known team, use
medium or low confidence and degradation language rather than high confidence.

### Turn-One GameState Evidence

Use high-confidence `observed` provenance when a turn-one GameState supplies
`activePlayer` / `activePlayerSeatId` and a matching `players[]` record maps
that active seat to a known team.

Relevant normalized helper:

- `_extract_starting_player_from_game_state(payload)`

Relevant raw paths include:

- `greToClientMessages[].gameStateMessage.turnInfo.turnNumber`
- `greToClientMessages[].gameStateMessage.turnInfo.activePlayer`
- `greToClientMessages[].gameStateMessage.turnInfo.activePlayerSeatId`
- `greToClientMessages[].gameStateMessage.players[].systemSeatNumber`
- `greToClientMessages[].gameStateMessage.players[].systemSeatId`
- `greToClientMessages[].gameStateMessage.players[].teamId`

If turn-one evidence only provides active seat and no team mapping, document it
as observed seat evidence but degraded for player-facing play/draw.

### Later-Game Inference

For game 2 and game 3 only, use `inferred` provenance when
`MatchSummary.effective_starting_player(...)` derives a starting player from:

- the previous game's winner,
- local `player_team`,
- derived `opponent_team`,
- and the current game having summary data.

Relevant model logic:

- If previous game winner equals local `player_team`, the next starter is
  `opponent_team()`.
- Otherwise the next starter is local `player_team`.

This is not observed Player.log starting-player evidence. It must be labeled
as inferred/derived and should not be high-confidence unless all dependencies
are known and non-conflicting.

Game 1 must not use later-game inference.

### Player-Team Dependency

`Play` / `Draw` requires known local `player_team`.

Required participant dependencies:

- `tier1.participants.player_team`
- `tier1.participants.opponent_team` for later-game inference
- `tier1.participants.participant_team_mapping` when seat/team mapping affects
  confidence

Known starting-player evidence without known local player team is insufficient
for high-confidence `Play` / `Draw`.

## Unknown-Like Values

For starting-player and play/draw provenance, these values are unknown or
degraded and must not be described as valid high-confidence team identifiers:

- `None`
- `""`
- whitespace-only strings
- `0`
- `0.0`
- `"0"`
- `" 0 "`
- booleans

Nonzero integer-like values may be valid observed identifiers, but confidence
depends on whether the value is known to be a team id or only a seat id.

This unknown-like policy is a provenance guarantee. It does not change current
parser normalization or assignment behavior in issue #139.

## Output Entries

### `tier3.play_draw.game1_starting_player`

Field meaning:

- Parser field: `MatchSummary.effective_starting_player(1)`
- Stored source: `MatchSummary.games[1].starting_player`
- Debug alias: `g1_starting_player`

Required evidence policy:

- `observed` from explicit current-game choose-starting-player ClientAction
  evidence when it maps to a known team.
- `observed` from turn-one GameState active-player evidence when it maps to a
  known team.
- `observed` but degraded when only active seat evidence exists.
- `unknown` when missing, unknown-like, seat-only without mapping, conflicting,
  or attached to no valid game slot.
- Game 1 must not use later-game inference.

Required signal examples:

- `client_action.game1.choose_starting_player`
- `game_state.game1.turn_one_active_player_team`
- `game_state.game1.turn_one_active_player_seat`
- `tier3.game_results.game_number_dependency`
- `ledger.tier1.participants.participant_team_mapping_dependency`

Required invariants:

- game 1 starting player is explicit or observed, not inferred from a previous
  game.
- turn-one GameState evidence requires `turn_number == 1`.
- seat-only evidence cannot support high-confidence play/draw without
  participant mapping.

### `tier3.play_draw.game2_starting_player`

Field meaning:

- Parser field: `MatchSummary.effective_starting_player(2)`
- Stored source: `MatchSummary.games[2].starting_player` when explicit
- Inferred source: previous game winner and player-team context when explicit
  source is blank
- Debug alias: `g2_starting_player`

Required evidence policy:

- Same explicit ClientAction and turn-one GameState policy as game 1, scoped to
  game 2.
- `inferred` from game 1 winner plus participant provenance only when game 2
  has summary data and no explicit starting-player value exists.
- `unknown` when no explicit evidence exists, game 2 has no summary data, or
  required inference dependencies are missing/degraded.

Required signal examples:

- `client_action.game2.choose_starting_player`
- `game_state.game2.turn_one_active_player_team`
- `game_state.game2.turn_one_active_player_seat`
- `model.game2.inferred_starting_player_from_previous_game`
- `ledger.tier3.game_results.game1_winner_team_dependency`
- `ledger.tier1.participants.player_team_dependency`
- `ledger.tier1.participants.opponent_team_dependency`

Required invariants:

- explicit starting-player evidence outranks inferred starting-player logic.
- inferred game 2 starter requires game 1 winner and participant provenance.
- blank game 2 starter is expected for an unplayed game 2.

### `tier3.play_draw.game3_starting_player`

Field meaning:

- Parser field: `MatchSummary.effective_starting_player(3)`
- Stored source: `MatchSummary.games[3].starting_player` when explicit
- Inferred source: game 2 winner and player-team context when explicit source
  is blank
- Debug alias: `g3_starting_player`

Required evidence policy:

- Same explicit ClientAction and turn-one GameState policy as game 1, scoped to
  game 3.
- `inferred` from game 2 winner plus participant provenance only when game 3
  has summary data and no explicit starting-player value exists.
- `unknown` when no explicit evidence exists, game 3 has no summary data, or
  required inference dependencies are missing/degraded.

Required signal examples:

- `client_action.game3.choose_starting_player`
- `game_state.game3.turn_one_active_player_team`
- `game_state.game3.turn_one_active_player_seat`
- `model.game3.inferred_starting_player_from_previous_game`
- `ledger.tier3.game_results.game2_winner_team_dependency`
- `ledger.tier1.participants.player_team_dependency`
- `ledger.tier1.participants.opponent_team_dependency`

Required invariants:

- explicit starting-player evidence outranks inferred starting-player logic.
- inferred game 3 starter requires game 2 winner and participant provenance.
- blank game 3 starter is expected for an unplayed game 3.

### `tier3.play_draw.game1_play_draw`

Field meaning:

- Parser field: `MatchSummary._game_play_draw_fields()["g1_play_draw"]`
- Model surface: `MatchSummary.game_play_draw(1)`
- Match-row alias: `G1 Play / Draw`
- Game-log alias: `Play / Draw` when `Game Number == 1`

Required evidence policy:

- `derived` from `game1_starting_player` plus local `player_team`.
- `unknown` or blank when either dependency is missing or degraded.
- `conflict` when starting-player evidence conflicts across ClientAction,
  GameState, model state, or participant mapping.
- Must not infer from match result, aggregate counts, workbook formulas,
  dashboards, Apps Script, webhook transport, or AI.

Required signal examples:

- `parser_state.match_summary.game1_play_draw`
- `ledger.tier3.play_draw.game1_starting_player_dependency`
- `ledger.tier1.participants.player_team_dependency`

Required invariants:

- game 1 play/draw requires known starting player and player team.
- missing starting-player evidence does not imply Draw.
- unplayed game slot blank behavior is not a loss of evidence.

### `tier3.play_draw.game2_play_draw`

Field meaning:

- Parser field: `MatchSummary._game_play_draw_fields()["g2_play_draw"]`
- Model surface: `MatchSummary.game_play_draw(2)`
- Match-row alias: `G2 Play / Draw`
- Game-log alias: `Play / Draw` when `Game Number == 2`

Required evidence policy:

- Same as game 1, scoped to game 2.
- If `game2_starting_player` is inferred, the play/draw value is derived from
  an inferred dependency and must expose that weaker provenance.
- Blank game 2 play/draw is expected when game 2 was not played.
- Blank game 2 play/draw is degraded/review-worthy when evidence indicates
  game 2 was played but starting-player or participant evidence is missing.

Required signal examples:

- `parser_state.match_summary.game2_play_draw`
- `ledger.tier3.play_draw.game2_starting_player_dependency`
- `ledger.tier1.participants.player_team_dependency`

### `tier3.play_draw.game3_play_draw`

Field meaning:

- Parser field: `MatchSummary._game_play_draw_fields()["g3_play_draw"]`
- Model surface: `MatchSummary.game_play_draw(3)`
- Match-row alias: `G3 Play / Draw`
- Game-log alias: `Play / Draw` when `Game Number == 3`

Required evidence policy:

- Same as game 1, scoped to game 3.
- If `game3_starting_player` is inferred, the play/draw value is derived from
  an inferred dependency and must expose that weaker provenance.
- Blank game 3 play/draw is expected when game 3 was not played.
- Blank game 3 play/draw is degraded/review-worthy when evidence indicates
  game 3 was played but starting-player or participant evidence is missing.

Required signal examples:

- `parser_state.match_summary.game3_play_draw`
- `ledger.tier3.play_draw.game3_starting_player_dependency`
- `ledger.tier1.participants.player_team_dependency`

## Dependency Map To Existing Entries

Codex C should make dependencies explicit in new entries and may update notes
on existing entries where helpful.

Required dependency links:

- `tier3.play_draw.game1_starting_player` depends on
  `tier3.game_results.game_number` and participant mapping.
- `tier3.play_draw.game2_starting_player` depends on
  `tier3.game_results.game_number`, participant mapping, and may depend on
  `tier3.game_results.game1_winner_team` for inference.
- `tier3.play_draw.game3_starting_player` depends on
  `tier3.game_results.game_number`, participant mapping, and may depend on
  `tier3.game_results.game2_winner_team` for inference.
- each `gameN_play_draw` entry depends on `gameN_starting_player`.
- each `gameN_play_draw` entry depends on
  `tier1.participants.player_team`.
- later-game inferred starting-player entries depend on
  `tier1.participants.opponent_team` when previous game winner equals local
  player team.

Future dependency links, not implemented in issue #139:

- mulligan and opening-hand review may consume play/draw provenance.
- sideboarding and pre/postboard review may consume game-number and play/draw
  provenance.
- analytics may consume play/draw confidence but must not become parser truth.

## Confidence, Finality, And Degradation Rules

Use existing vocabulary only:

- `value_source`: `observed`, `derived`, `inferred`, `unknown`, `conflict`
- `confidence`: `high`, `medium`, `low`, `unknown`
- `finality`: `live`, `provisional`, `final`, `reconciled`
- drift/degradation flags from the existing `DRIFT_FLAGS` vocabulary

Required policies:

- Explicit, current, non-conflicting choose-starting-player evidence that maps
  to a known team may be high-confidence observed evidence.
- Turn-one GameState active-player evidence that maps to a known team may be
  high-confidence observed evidence.
- Turn-one active-player seat evidence without team mapping is observed but
  degraded for player-facing play/draw.
- Later-game model inference is `inferred`, not observed.
- `Play` / `Draw` labels are derived, not observed.
- Player-facing play/draw is high confidence only when starting-player and
  `player_team` dependencies are known and non-conflicting.
- Missing starting-player evidence is `unknown`.
- Missing player-team evidence is `unknown`.
- Conflicting ClientAction, GameState, model, or participant evidence is
  `conflict`, low confidence, and review-required.
- Participant and game-result dependencies must surface weaker confidence when
  play/draw depends on inferred later-game logic.
- Entries are generally `live` or `provisional` during active parsing and may
  be `final` once final match result evidence exists without later stronger
  correction.
- If later stronger starting-player or participant evidence corrects a final
  value, use `reconciled` in future field-evidence language.

Required degradation behavior:

- missing starting player leaves play/draw blank.
- missing local player team leaves play/draw blank.
- known starting player without known player team is insufficient for
  high-confidence `Play` / `Draw`.
- known player team without starting-player evidence is insufficient for
  high-confidence `Play` / `Draw`.
- seat-only starting-player evidence is degraded unless participant mapping
  proves the corresponding team.
- unplayed game slot blanks are expected, not errors.
- played game slots with missing starting-player evidence are degraded and
  review-worthy.
- match result, aggregate counts, workbook formulas, dashboards, Apps Script,
  webhook transport, and AI must not populate play/draw.

## Privacy And Serialization Rules

Play/draw provenance must remain path-only and metadata-only.

The contract allows symbolic raw paths such as:

- `ClientToGREMessage.payload.chooseStartingPlayerResp.systemSeatId`
- `ClientToGREMessage.payload.systemSeatId`
- `greToClientMessages[].gameStateMessage.turnInfo.turnNumber`
- `greToClientMessages[].gameStateMessage.turnInfo.activePlayer`
- `greToClientMessages[].gameStateMessage.turnInfo.activePlayerSeatId`
- `greToClientMessages[].gameStateMessage.players[].systemSeatNumber`
- `greToClientMessages[].gameStateMessage.players[].teamId`

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
- current starting-player extraction behavior
- current later-game inference behavior
- current event classes and parser payload shapes
- current workbook schema
- current webhook payload shape
- current Apps Script behavior
- current output transport
- current match/game identity and deduplication behavior

Implementation may change:

- evidence-ledger registry entries
- evidence-ledger family seed-field metadata
- evidence-ledger entry notes and dependency signals
- focused evidence-ledger tests
- implementation handoff and contract-test report docs

## Test Obligations

Codex C must add or update focused tests in `tests/test_evidence_ledger.py`.

Required assertions:

- `game_level_facts.seed_fields` includes the existing #134 fields plus
  `game1_starting_player`, `game2_starting_player`,
  `game3_starting_player`, `game1_play_draw`, `game2_play_draw`, and
  `game3_play_draw`.
- `game_level_facts.future_fields` no longer lists broad `play_draw` or
  `starting_player` after the granular entries are seeded.
- all six `tier3.play_draw.*` entries exist and validate.
- starting-player entries cite explicit ClientAction evidence.
- starting-player entries cite turn-one GameState active-player evidence.
- game 1 starting-player entry does not claim later-game inference.
- game 2 starting-player entry cites game 1 winner dependency for inference.
- game 3 starting-player entry cites game 2 winner dependency for inference.
- play/draw entries cite their starting-player dependency and
  `tier1.participants.player_team`.
- later-game inferred starting-player behavior is labeled `inferred` in
  evidence metadata.
- blank expected behavior for unplayed game slots is documented.
- played game slots with missing starting-player evidence are degraded or
  review-worthy in metadata language.
- all new signals use path-only privacy and do not embed raw values.
- `validate_player_log_evidence_ledger()` returns `[]`.
- every built-in entry passes `validate_ledger_entry(...)`.

Recommended adjacent behavior tests to run as evidence, not to change behavior:

- `tests/test_app_extractors.py`
- `tests/test_app_models.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_state.py`
- `tests/test_golden_replay_harness.py`

Validation commands for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_app_extractors.py tests/test_app_models.py tests/test_match_summary_from_match_state.py tests/test_state.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q
python3 -m ruff check src tests tools
git diff --check
```

If protected-surface tooling is available in the branch, Codex C should run the
repo's protected-surface checks and report `forbidden 0`.

## Acceptance Criteria

Issue #139 is implementation-ready when:

- this contract exists at
  `docs/contracts/player_log_evidence_ledger_tier3_play_draw.md`.
- Codex C can implement the play/draw provenance slice with evidence-ledger
  metadata and tests only.
- no parser behavior changes are required.
- no protected surface changes are required.
- direct, observed, inferred, derived, missing, and conflicting play/draw
  provenance are distinguishable.
- dependencies on #137 participant provenance and #134 game-result provenance
  are explicit.
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

  Act as Codex C: Module Implementer for issue #139, Tier 3 play/draw provenance under issue #11.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/139
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/137
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/138
    - Previous merge commit: 869491a7999ebf2510c19925f1f671d1f37f2113
    - Base branch: codex/parser-reliability-intelligence
    - Recommended implementation branch: codex/player-log-evidence-ledger-tier3-play-draw
    - Contract: docs/contracts/player_log_evidence_ledger_tier3_play_draw.md
    - Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier3_play_draw_comparison.md

  Goal:
    Implement the Tier 3 starting-player and play/draw evidence-ledger provenance slice defined by the contract. Add or update evidence-ledger metadata and focused tests only.

  Read first:
    - AGENTS.md
    - docs/agent_rules.yml
    - docs/agent_constitution.md
    - docs/codex_module_workflow.md
    - docs/agent_threads/implementation.md
    - docs/contracts/player_log_evidence_ledger_tier3_play_draw.md
    - docs/contracts/player_log_evidence_ledger_schema.md
    - docs/contracts/player_log_evidence_ledger_participant_player_team.md
    - docs/contracts/player_log_evidence_ledger_tier3_game_results.md
    - docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
    - src/mythic_edge_parser/app/evidence_ledger.py
    - tests/test_evidence_ledger.py
    - src/mythic_edge_parser/app/extractors.py
    - src/mythic_edge_parser/app/state.py
    - src/mythic_edge_parser/app/models.py
    - src/mythic_edge_parser/parsers/client_actions.py
    - src/mythic_edge_parser/parsers/gre/game_state.py
    - src/mythic_edge_parser/parsers/gre/turn_info.py

  Do:
    - Compare current evidence-ledger metadata against the contract before editing.
    - Add Tier 3 seed fields for game1_starting_player, game2_starting_player, game3_starting_player, game1_play_draw, game2_play_draw, and game3_play_draw.
    - Add validating ledger entries for tier3.play_draw.game1_starting_player, tier3.play_draw.game2_starting_player, tier3.play_draw.game3_starting_player, tier3.play_draw.game1_play_draw, tier3.play_draw.game2_play_draw, and tier3.play_draw.game3_play_draw.
    - Make play/draw entries explicitly cite #137 participant provenance and #134 game-result provenance where needed.
    - Label later-game starting-player inference as inferred, not observed.
    - Keep privacy path-only and do not embed raw player values or raw log excerpts.
    - Add focused tests in tests/test_evidence_ledger.py.
    - Produce docs/implementation_handoffs/player_log_evidence_ledger_tier3_play_draw_comparison.md with comparison, changes made, validation, risks, and next recommended role.

  Do not:
    - Change parser behavior.
    - Change starting-player extraction behavior.
    - Change later-game starting-player inference behavior.
    - Change parser state final reconciliation.
    - Change parser event classes.
    - Change workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or production behavior.
    - Add runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, or feature-equity report changes.
    - Map mulligan, opening-hand, turn-count, timing/duration, pre/postboard, sideboarding, or deck-state provenance.
    - Infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, or AI/analytics truth.
    - Commit raw private Player.log excerpts.
    - Target main directly.
    - Close issue #11.
    - Stage or commit unless explicitly asked.

  Validation:
    - python3 -m pytest -q tests/test_evidence_ledger.py
    - python3 -m pytest -q tests/test_app_extractors.py tests/test_app_models.py tests/test_match_summary_from_match_state.py tests/test_state.py
    - python3 -m pytest -q tests/test_golden_replay_harness.py
    - python3 -m pytest -q
    - python3 -m ruff check src tests tools
    - git diff --check

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/139"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/137"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/138"
  previous_merge_commit: "869491a7999ebf2510c19925f1f671d1f37f2113"
  parallel_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/140"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_play_draw.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_play_draw_comparison.md"
  verdict: "tier3_play_draw_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-play-draw"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_app_extractors.py tests/test_app_models.py tests/test_match_summary_from_match_state.py tests/test_state.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, starting-player extraction behavior, later-game starting-player inference behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not map mulligan, opening-hand, turn-count, timing/duration, pre/postboard, sideboarding, or deck-state provenance."
    - "Do not reconstruct missing GameState data or infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, or AI/analytics truth."
    - "Do not commit raw private Player.log excerpts or local diagnostics artifacts."
```

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/139"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/137"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/138"
  previous_merge_commit: "869491a7999ebf2510c19925f1f671d1f37f2113"
  parallel_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/140"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_play_draw.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_play_draw_comparison.md"
  verdict: "tier3_play_draw_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-play-draw"
  validation:
    - "not run - contract writer pass"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not implement code in Codex B."
    - "Do not change parser behavior, starting-player extraction behavior, later-game starting-player inference behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not map mulligan, opening-hand, turn-count, timing/duration, pre/postboard, sideboarding, or deck-state provenance."
    - "Do not reconstruct missing GameState data or infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, or AI/analytics truth."
    - "Do not commit raw private Player.log excerpts or local diagnostics artifacts."
