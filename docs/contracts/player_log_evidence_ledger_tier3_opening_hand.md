# Player.log Evidence Ledger Tier 3 Opening-Hand Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/143
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/140
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/142
- previous_merge_commit: 33a8bc2cba188389fe885b2446da51ac48c8555e
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier3-opening-hand
- target_artifact: docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md
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
- docs/contracts/player_log_evidence_ledger_tier3_play_draw.md
- docs/contracts/player_log_evidence_ledger_tier3_mulligans.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- docs/decisions/ADR-0003-player-log-drift-policy.md

## Purpose

Issue #143 maps Tier 3 opening-hand ownership provenance in the Player.log
evidence ledger.

Opening-hand values are parser-owned facts built from local private-hand
GameState evidence, hand snapshot history, card instance-to-GRP mapping,
card-name resolution, #137 local participant context, and #140 mulligan-count
context. They are privacy-sensitive and strategically important. The evidence
ledger must explain what supports exact opening-hand lists, opening-hand size,
and mulliganed-away card lists without changing parser behavior.

This contract documents provenance metadata only. It must not change parser
behavior, local private-hand extraction, opening-hand selection,
mulliganed-away capture, card-name resolution, generated card data, parser
state final reconciliation, event classes, workbook schema, webhook payload
shape, Apps Script behavior, output transport, match/game identity,
deduplication, or analytics truth.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, validators, vocabulary constants, and privacy posture.

`docs/contracts/player_log_evidence_ledger_participant_player_team.md` remains
authoritative for local system-seat and participant/team provenance. Opening
hand ownership depends on local-seat context but must not redefine participant
truth.

`docs/contracts/player_log_evidence_ledger_tier3_game_results.md` remains
authoritative for game number and game-slot identity. Opening-hand entries
depend on the correct game slot but must not infer hand values from results.

`docs/contracts/player_log_evidence_ledger_tier3_play_draw.md` remains
authoritative for starting-player and play/draw provenance. Opening-hand
entries may be consumed by future review with play/draw context, but issue
#143 must not change play/draw entries or behavior.

`docs/contracts/player_log_evidence_ledger_tier3_mulligans.md` remains
authoritative for per-game and total mulligan provenance. Opening-hand size may
fall back to `7 - mulligans`, and mulliganed-away capture may observe
non-keep mulligan flow, but issue #143 must not redefine or recalculate
mulligan counts.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #143 provenance should be
recorded through this contract, implementation handoff, entry notes, and
focused tests rather than by changing the top-level ledger object shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- GRE GameState parsing preserves raw private-hand, zone, object, turn, and
  game-slot evidence as parser input.
- `src/mythic_edge_parser/app/extractors.py` owns current helper extraction for
  local private-hand instance ids and instance-to-GRP lookup.
- `src/mythic_edge_parser/app/state.py` owns hand snapshot history, GRP lookup
  accumulation, opening-hand candidate selection, discarded mulligan hand
  capture, bottomed-card capture, and card-name resolution calls.
- `src/mythic_edge_parser/app/models.py` owns `GameSummary.opening_hand`,
  `GameSummary.mulliganed_away`, `GameSummary.opening_hand_size()`,
  exact card-list serialization, and game-log row values.
- `src/mythic_edge_parser/app/grp_id_catalog.py` owns current GRP catalog and
  card-name lookup behavior.
- `src/mythic_edge_parser/app/evidence_ledger.py` describes provenance,
  confidence, finality, degradation, and review expectations.
- Workbook rows, Apps Script, webhook transport, dashboards, diagnostics,
  golden replay, feature-equity reports, drift reports, card-performance
  analytics, mulligan analytics, and AI output are downstream consumers only.

The ledger must not reconstruct missing GameState data, infer hidden cards,
complete decklists, classify archetypes, provide gameplay advice, infer player
mistakes, or move parser truth into workbook formulas, dashboard logic, Apps
Script, webhook transport, output transport, generated card data, or AI.

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` after PR #142:

- The Tier 3 `game_level_facts` family is already `seeded_sample` for game
  number, game winners, game results, starting-player, play/draw, and mulligan
  provenance.
- The same family still lists broad future field `opening_hand`.
- Game-log schema already includes `Opening Hand Size`, `Opening Hand`, and
  `Mulliganed Away`.
- `_extract_local_private_hand_instance_ids(...)` reads `systemSeatIds[0]` as
  local seat when available.
- `_extract_local_private_hand_instance_ids(...)` scans hand zones with
  `type == "ZoneType_Hand"` and `visibility == "Visibility_Private"`.
- When local seat is known, zones with owner seat known and not equal to local
  seat are rejected.
- Malformed or missing owner-seat values currently normalize to unknown and
  may be accepted as local private-hand evidence.
- The first matching private hand zone wins.
- GameState extraction can fall back to queued GameState zone and object
  payloads.
- `_extract_instance_grp_lookup(...)` maps `gameObjects[].instanceId` to
  `grpId`, `grp_id`, `overlayGrpId`, or `overlay_grp_id` when both normalize
  to integers.
- `_record_opening_hand_candidate(...)` ignores snapshots without a valid
  normalized match/game key.
- `_record_opening_hand_candidate(...)` ignores hand snapshots with fewer than
  4 or more than 7 instance ids.
- `_record_opening_hand_candidate(...)` rejects a GameState whose turn match id
  conflicts with the current match summary.
- `_record_opening_hand_candidate(...)` records hand snapshots and latest hand
  snapshot before deciding whether the snapshot becomes the opening hand.
- Opening-hand assignment requires turn number exactly `1`.
- Opening-hand assignment requires the snapshot size to match
  `max(7 - mulligans, 0)` when that expected size is nonzero.
- `_resolve_hand_snapshot(...)` resolves cards through the active Arena lookup
  when ready, otherwise through `resolve_grp_id_entry(...)`.
- Missing or unresolved GRP/card-name evidence becomes placeholder text such as
  an Arena ID placeholder or missing-Arena-ID placeholder.
- `_record_hand_snapshot(...)` suppresses adjacent duplicate snapshots and
  stores the latest hand snapshot.
- `GameSummary.set_opening_hand(...)` keeps the better snapshot: any snapshot
  when none exists, a longer snapshot, or an equal-length snapshot with fewer
  placeholders.
- `GameSummary.opening_hand_size()` returns exact opening-hand list length
  first. If no exact opening hand exists but the game has started, it returns
  `max(7 - mulligans, 0)`. If the game has not started, it returns blank.
- `_serialize_exact_card_list(...)` returns blank for empty card lists and for
  any list containing placeholder card names.
- `GameSummary.to_game_log_row(...)` exposes `Opening Hand Size`,
  `Opening Hand`, and `Mulliganed Away`.
- `_record_discarded_mulligan_hand(...)` adds the latest hand snapshot to
  `mulliganed_away` for non-keep mulligan flow, then removes the latest
  snapshot.
- `_capture_bottomed_cards(...)` compares a prior longer snapshot against the
  final hand, adds the list difference to `mulliganed_away`, and captures
  bottomed cards only once per game key.

Observed risks, not fixed by this issue:

- Malformed private-zone owner-seat evidence can currently be accepted as
  local. The ledger must mark that path degraded/review-required rather than
  high confidence.
- Exact hand card lists can exist in parser state while row serialization
  returns blank because one or more placeholder values are present.
- `Opening Hand Size` can be observed from exact hand length or derived from
  fallback mulligan math. The ledger must distinguish those meanings.
- Mulliganed-away lists can come from discarded pre-keep hand snapshots or
  bottomed-card differences. The ledger must document both without treating
  them as mulligan-count evidence.
- Raw private hand contents and raw GameState payloads are local/private
  evidence and must not be embedded in ledger metadata.

## Scope Decision

Codex C should implement issue #143 as a Tier 3 `game_level_facts` metadata
slice in the existing evidence ledger.

Do not add a new output family. Do not add a workbook column, webhook field,
runtime status field, parser event class, parser behavior path, generated card
data, analytics surface, or runtime field-evidence attachment.

Required Tier 3 seed fields to add:

- `game1_opening_hand_size`
- `game2_opening_hand_size`
- `game3_opening_hand_size`
- `game1_opening_hand`
- `game2_opening_hand`
- `game3_opening_hand`
- `game1_mulliganed_away`
- `game2_mulliganed_away`
- `game3_mulliganed_away`

Required Tier 3 entries:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier3.opening_hand.game1_opening_hand_size` | `game1_opening_hand_size` | `Opening Hand Size` | `observed` or `derived` |
| `tier3.opening_hand.game2_opening_hand_size` | `game2_opening_hand_size` | `Opening Hand Size` | `observed` or `derived` |
| `tier3.opening_hand.game3_opening_hand_size` | `game3_opening_hand_size` | `Opening Hand Size` | `observed` or `derived` |
| `tier3.opening_hand.game1_opening_hand` | `game1_opening_hand` | `Opening Hand` | `observed` |
| `tier3.opening_hand.game2_opening_hand` | `game2_opening_hand` | `Opening Hand` | `observed` |
| `tier3.opening_hand.game3_opening_hand` | `game3_opening_hand` | `Opening Hand` | `observed` |
| `tier3.opening_hand.game1_mulliganed_away` | `game1_mulliganed_away` | `Mulliganed Away` | `observed` or `derived` |
| `tier3.opening_hand.game2_mulliganed_away` | `game2_mulliganed_away` | `Mulliganed Away` | `observed` or `derived` |
| `tier3.opening_hand.game3_mulliganed_away` | `game3_mulliganed_away` | `Mulliganed Away` | `observed` or `derived` |

Required family metadata:

- Keep `game_level_facts.status` as `seeded_sample`.
- Add the nine fields above to `game_level_facts.seed_fields`.
- Remove broad `opening_hand` from `game_level_facts.future_fields` once the
  granular entries are seeded.
- Preserve the #134 game-result, #139 play/draw, and #140 mulligan seed fields
  already present on the branch.
- Keep remaining future fields, at minimum:
  - `turn_count`
  - `game_timing`
  - `game_duration`
  - `pre_postboard`
  - `sideboarding`
  - `deck_state`
- Add notes stating that issue #143 maps opening-hand ownership, exact-list,
  size, and mulliganed-away provenance while deferring analytics, diagnostics,
  replay, drift, schema snapshots, invariant execution, generated-data changes,
  and field-evidence attachment work.

## Deferred Work

Defer all of the following:

- parser behavior changes
- local private-hand extraction changes
- opening-hand selection changes
- mulliganed-away capture changes
- card-name resolution changes
- GRP catalog behavior changes
- generated card data changes
- parser state final reconciliation changes
- parser event class changes
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
- turn-count provenance
- timing and duration provenance
- pre/postboard, sideboarding, or deck-state provenance
- mulligan-tax, opening-hand, card-performance, gameplay advice, mistake
  labels, deck inference, archetype classification, or AI/model-provider
  behavior

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier3_opening_hand.md

Referenced but not owned:

- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_participant_player_team.md
- docs/contracts/player_log_evidence_ledger_tier3_game_results.md
- docs/contracts/player_log_evidence_ledger_tier3_play_draw.md
- docs/contracts/player_log_evidence_ledger_tier3_mulligans.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- src/mythic_edge_parser/app/extractors.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/grp_id_catalog.py
- src/mythic_edge_parser/app/sheet_schema.py
- tests/test_app_extractors.py
- tests/test_state.py
- tests/test_app_models.py
- tests/test_grp_id_catalog.py
- tests/test_match_summary_from_match_state.py
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
- Every new opening-hand entry passes `validate_ledger_entry(...)`.
- The built ledger passes `validate_player_log_evidence_ledger(...)`.
- Entry IDs and signal IDs remain stable, lowercase, and dot-separated.
- Source paths remain repo-relative or symbolic.
- Raw payload values, raw private hand contents, raw card lists, raw Player.log
  excerpts, raw GameState payloads, absolute local paths, secrets, webhook
  URLs, local runtime artifacts, generated data, failed posts, and workbook
  exports must not be embedded.

## Field Inventory

### `gameN_opening_hand_size`

Meaning:

- The parser-owned opening hand size for fixed game slot `N`, where `N` is
  `1`, `2`, or `3`.

Current surfaces:

- `GameSummary.opening_hand_size()`
- Game-log row field `Opening Hand Size`
- `GameSummary.opening_hand` length when exact hand evidence exists
- fallback `max(7 - mulligans, 0)` when the game has started and exact hand is
  missing

Output role:

- Parser-owned game-log fact.
- Not a match-log field.
- Not directly observed when derived from mulligan fallback math.

### `gameN_opening_hand`

Meaning:

- The parser-owned exact local opening-hand card-list value for fixed game slot
  `N`.

Current surfaces:

- `GameSummary.opening_hand`
- `GameSummary.set_opening_hand(...)`
- Game-log row field `Opening Hand`
- `_serialize_exact_card_list(...)`

Output role:

- Parser-owned local/private exact-list fact.
- Workbook-visible downstream alias already exists in the game log; issue
  #143 must not change its shape.
- Placeholder-containing lists are present in parser state but serialize as
  blank in the game-log row.

### `gameN_mulliganed_away`

Meaning:

- The parser-owned local card-list value for cards seen in discarded mulligan
  hands or bottomed from a prior longer hand snapshot for fixed game slot `N`.

Current surfaces:

- `GameSummary.mulliganed_away`
- `GameSummary.add_mulliganed_away(...)`
- `_record_discarded_mulligan_hand(...)`
- `_capture_bottomed_cards(...)`
- Game-log row field `Mulliganed Away`
- `_serialize_exact_card_list(...)`

Output role:

- Parser-owned local/private card-list fact.
- Not evidence for mulligan count.
- Placeholder-containing lists are present in parser state but serialize as
  blank in the game-log row.

## Source Evidence Priority

This priority is for ledger confidence and provenance language. It must not be
implemented as a parser behavior change in issue #143.

Priority order for opening-hand metadata:

1. local private-hand GameState evidence with known local seat ownership
2. turn-one exact local opening-hand snapshot with coherent expected size
3. card instance-to-GRP and card-name resolution evidence
4. parser state/model surfaces that preserve or expose those values
5. fallback opening-hand size derived from #140 mulligan count
6. discarded-hand or bottomed-card list evidence for `Mulliganed Away`
7. unknown/degraded fallback when required dependencies are missing,
   placeholder-only, malformed, contradictory, or privacy-sensitive

Parser state/model surfaces are evidence consumers and exposed parser-owned
fields in this contract. They are not independent raw evidence sources that can
override clearer GameState, local-ownership, or card-resolution evidence.

### Local Private-Hand Ownership Evidence

Use high-confidence `observed` provenance when a GameState supplies:

- `systemSeatIds[0]` or equivalent local-seat context,
- a hand zone with `type == "ZoneType_Hand"`,
- `visibility == "Visibility_Private"`,
- `ownerSeatId` matching the local seat,
- and a non-empty normalized `objectInstanceIds` list.

Relevant helper:

- `_extract_local_private_hand_instance_ids(payload)`

Relevant raw paths include:

- `greToClientMessages[].gameStateMessage.systemSeatIds[]`
- `greToClientMessages[].gameStateMessage.zones[].type`
- `greToClientMessages[].gameStateMessage.zones[].visibility`
- `greToClientMessages[].gameStateMessage.zones[].ownerSeatId`
- `greToClientMessages[].gameStateMessage.zones[].objectInstanceIds[]`
- `queuedGameStateMessage.gameStateMessage.zones[]`

Required dependency entries:

- `tier1.participants.local_system_seat_id`
- `tier1.participants.participant_team_mapping`

If owner-seat evidence is missing or malformed, current extraction may still
accept the private hand zone. The ledger must describe that path as degraded
and review-required for local ownership.

### Exact Opening-Hand Snapshot Evidence

Use high-confidence `observed` provenance for exact opening-hand list when:

- local private-hand ownership is known,
- game slot identity is known,
- hand snapshot contains 4 through 7 normalized instance ids,
- turn match id is blank, missing, or matches the current match summary,
- turn number is exactly `1`,
- the snapshot length matches expected hand size when expected size is nonzero,
- instance-to-GRP mapping is coherent,
- card names are resolved without placeholders,
- and the parser-selected snapshot is the best current snapshot.

Relevant helpers:

- `_record_opening_hand_candidate(...)`
- `_record_hand_snapshot(...)`
- `_resolve_hand_snapshot(...)`
- `GameSummary.set_opening_hand(...)`
- `_better_opening_hand_snapshot(...)`

Relevant raw and normalized paths include:

- `payload.identity.game_number`
- `payload.turn_info.turn_number`
- `payload.game_info.matchID`
- `payload.raw_game_state.gameStateMessage.turnInfo.turnNumber`
- `payload.raw_game_state.gameStateMessage.zones[].objectInstanceIds[]`
- `payload.raw_game_state.gameStateMessage.gameObjects[].instanceId`
- `payload.raw_game_state.gameStateMessage.gameObjects[].grpId`
- `payload.raw_game_state.gameStateMessage.gameObjects[].overlayGrpId`

Opening-hand snapshots with unresolved placeholders are still observed
private-hand snapshots, but exact card-list confidence is degraded and row
serialization can be blank.

### Card Identity Resolution Evidence

Use `observed` or `derived` provenance for card identity resolution when
instance ids map to GRP ids and the GRP id lookup resolves to a card name.

Relevant helpers:

- `_extract_instance_grp_lookup(payload)`
- `_resolve_hand_snapshot(...)`
- `resolve_grp_id_entry(...)`
- `resolve_grp_id_name(...)`

Relevant raw and normalized paths include:

- `gameObjects[].instanceId`
- `gameObjects[].grpId`
- `gameObjects[].overlayGrpId`
- `grp_id_catalog.cards_by_grp_id`
- `arena_lookup[grp_id]`

Missing GRP ids, unresolved names, placeholder display values, generated data
staleness, or candidate-only resolution must lower confidence. Issue #143 must
not change GRP catalog behavior or generated card data.

### Opening-Hand Size Fallback

`Opening Hand Size` uses exact opening-hand length first. Only when no exact
opening hand exists and the game has started may it use fallback math:

- `max(7 - GameSummary.mulligans, 0)`

Required dependency:

- `tier3.mulligans.gameN_mulligans`

Fallback size is `derived`, not observed. It must not imply exact card-list
evidence.

### Mulliganed-Away Evidence

Use observed/degraded provenance for `Mulliganed Away` when card-list evidence
comes from:

- `_record_discarded_mulligan_hand(...)`, using the latest local private-hand
  snapshot when a non-keep mulligan response is handled, or
- `_capture_bottomed_cards(...)`, using list difference between a prior longer
  snapshot and the final opening hand.

Relevant dependencies:

- `tier3.mulligans.gameN_mulligans`
- local private-hand ownership evidence
- hand snapshot history
- exact opening-hand snapshot evidence for bottomed-card difference

Mulliganed-away cards are not evidence for mulligan count. They must not
rewrite #140 mulligan provenance.

## Placeholder, Blank, And Privacy Semantics

Placeholder values are degraded evidence.

Required policy:

- Exact card-list entries are high confidence only when local ownership,
  instance ids, GRP mapping, and card-name resolution are coherent and no
  placeholder values remain.
- Parser state may retain placeholder-containing lists.
- Game-log row `Opening Hand` and `Mulliganed Away` serialize as blank when a
  list is empty or contains any placeholder.
- Blank serialized `Opening Hand` does not prove no opening-hand evidence
  exists.
- Blank serialized `Mulliganed Away` does not prove no discarded/bottomed
  evidence exists.
- `Opening Hand Size` may still be observed from a placeholder-containing exact
  hand list length, but exact card-list confidence is degraded.
- Unplayed game slots should be expected blank, not degraded.
- Played game slots with missing local-private-hand, missing card mapping, or
  placeholder-only evidence should be degraded/review-worthy.
- Raw hand contents, raw object instance ids, raw GameState payloads, and raw
  Player.log lines must not be embedded in the ledger.

## Output Entries

### `tier3.opening_hand.game1_opening_hand_size`

Field meaning:

- Parser field: `GameSummary.opening_hand_size()` for game 1
- Model surface: `MatchSummary.games[1].opening_hand_size()`
- Game-log alias: `Opening Hand Size` when `Game Number == 1`

Required evidence policy:

- `observed` from exact game 1 opening-hand list length when exact local
  private-hand evidence is coherent.
- `derived` from #140 game 1 mulligan count fallback when exact hand is
  missing but the game has started.
- `unknown` or degraded when game 1 is played but local ownership, card
  identity, or mulligan dependency is missing/degraded.
- expected blank when game 1 has no game-start evidence.

Required signal examples:

- `game_state.game1.local_private_hand_snapshot`
- `parser_state.match_summary.game1_opening_hand_size`
- `ledger.tier3.opening_hand.game1_opening_hand_dependency`
- `ledger.tier3.mulligans.game1_mulligans_dependency`
- `ledger.tier1.participants.local_system_seat_id_dependency`

Required invariants:

- exact opening-hand length outranks fallback mulligan math.
- fallback size must be labeled derived, not observed.
- blank size for unplayed game slot is expected.

### `tier3.opening_hand.game2_opening_hand_size`

Field meaning:

- Parser field: `GameSummary.opening_hand_size()` for game 2
- Model surface: `MatchSummary.games[2].opening_hand_size()`
- Game-log alias: `Opening Hand Size` when `Game Number == 2`

Required evidence policy:

- Same as game 1, scoped to game 2.
- Expected blank when game 2 was not played.
- Degraded/review-required when game 2 was played but local private-hand or
  fallback mulligan evidence is missing/degraded.

Required signal examples:

- `game_state.game2.local_private_hand_snapshot`
- `parser_state.match_summary.game2_opening_hand_size`
- `ledger.tier3.opening_hand.game2_opening_hand_dependency`
- `ledger.tier3.mulligans.game2_mulligans_dependency`
- `ledger.tier1.participants.local_system_seat_id_dependency`

### `tier3.opening_hand.game3_opening_hand_size`

Field meaning:

- Parser field: `GameSummary.opening_hand_size()` for game 3
- Model surface: `MatchSummary.games[3].opening_hand_size()`
- Game-log alias: `Opening Hand Size` when `Game Number == 3`

Required evidence policy:

- Same as game 1, scoped to game 3.
- Expected blank when game 3 was not played.
- Degraded/review-required when game 3 was played but local private-hand or
  fallback mulligan evidence is missing/degraded.

Required signal examples:

- `game_state.game3.local_private_hand_snapshot`
- `parser_state.match_summary.game3_opening_hand_size`
- `ledger.tier3.opening_hand.game3_opening_hand_dependency`
- `ledger.tier3.mulligans.game3_mulligans_dependency`
- `ledger.tier1.participants.local_system_seat_id_dependency`

### `tier3.opening_hand.game1_opening_hand`

Field meaning:

- Parser field: `MatchSummary.games[1].opening_hand`
- Model surface: `GameSummary.opening_hand`
- Game-log alias: `Opening Hand` when `Game Number == 1`

Required evidence policy:

- `observed` from exact game 1 local private-hand snapshot when ownership,
  turn-one, expected-size, instance mapping, and card-name resolution are
  coherent.
- `observed` but degraded when instance ids are observed but one or more cards
  resolve to placeholders.
- `unknown` when local ownership, game slot, turn-one, hand-zone, or
  instance-id evidence is missing.
- expected blank when the game was unplayed.

Required signal examples:

- `game_state.game1.local_private_hand_zone`
- `game_state.game1.local_private_hand_instance_ids`
- `game_state.game1.instance_grp_lookup`
- `grp_id_catalog.game1.card_name_resolution`
- `parser_state.hand_snapshot_history.game1`
- `parser_state.match_summary.game1_opening_hand`
- `ledger.tier1.participants.local_system_seat_id_dependency`
- `ledger.tier1.participants.participant_team_mapping_dependency`

Required invariants:

- exact opening hand requires local private-hand ownership evidence.
- placeholder-containing lists are degraded and may serialize blank.
- exact opening hand must not be reconstructed from decklists, analytics, or
  AI.

### `tier3.opening_hand.game2_opening_hand`

Field meaning:

- Parser field: `MatchSummary.games[2].opening_hand`
- Model surface: `GameSummary.opening_hand`
- Game-log alias: `Opening Hand` when `Game Number == 2`

Required evidence policy:

- Same as game 1, scoped to game 2.
- Expected blank when game 2 was not played.
- Degraded/review-required when game 2 was played but local private-hand,
  turn-one, instance, GRP, or card-name evidence is missing/degraded.

Required signal examples:

- `game_state.game2.local_private_hand_zone`
- `game_state.game2.local_private_hand_instance_ids`
- `game_state.game2.instance_grp_lookup`
- `grp_id_catalog.game2.card_name_resolution`
- `parser_state.hand_snapshot_history.game2`
- `parser_state.match_summary.game2_opening_hand`
- `ledger.tier1.participants.local_system_seat_id_dependency`

### `tier3.opening_hand.game3_opening_hand`

Field meaning:

- Parser field: `MatchSummary.games[3].opening_hand`
- Model surface: `GameSummary.opening_hand`
- Game-log alias: `Opening Hand` when `Game Number == 3`

Required evidence policy:

- Same as game 1, scoped to game 3.
- Expected blank when game 3 was not played.
- Degraded/review-required when game 3 was played but local private-hand,
  turn-one, instance, GRP, or card-name evidence is missing/degraded.

Required signal examples:

- `game_state.game3.local_private_hand_zone`
- `game_state.game3.local_private_hand_instance_ids`
- `game_state.game3.instance_grp_lookup`
- `grp_id_catalog.game3.card_name_resolution`
- `parser_state.hand_snapshot_history.game3`
- `parser_state.match_summary.game3_opening_hand`
- `ledger.tier1.participants.local_system_seat_id_dependency`

### `tier3.opening_hand.game1_mulliganed_away`

Field meaning:

- Parser field: `MatchSummary.games[1].mulliganed_away`
- Model surface: `GameSummary.mulliganed_away`
- Game-log alias: `Mulliganed Away` when `Game Number == 1`

Required evidence policy:

- `observed` from discarded latest local hand snapshot when a non-keep
  mulligan response is handled in game 1.
- `derived` from bottomed-card difference between a prior longer snapshot and
  the final game 1 opening hand.
- degraded when hand ownership, snapshot history, card identity, or #140
  mulligan context is missing/degraded.
- expected blank when no mulliganed-away evidence exists or the game was
  unplayed.

Required signal examples:

- `parser_state.latest_hand_snapshot.game1`
- `parser_state.hand_snapshot_history.game1`
- `parser_state.bottomed_cards_capture.game1`
- `parser_state.match_summary.game1_mulliganed_away`
- `ledger.tier3.mulligans.game1_mulligans_dependency`
- `ledger.tier3.opening_hand.game1_opening_hand_dependency`

Required invariants:

- mulliganed-away cards are not evidence for mulligan count.
- bottomed-card difference requires a prior longer snapshot and final hand.
- placeholder-containing lists are degraded and may serialize blank.

### `tier3.opening_hand.game2_mulliganed_away`

Field meaning:

- Parser field: `MatchSummary.games[2].mulliganed_away`
- Model surface: `GameSummary.mulliganed_away`
- Game-log alias: `Mulliganed Away` when `Game Number == 2`

Required evidence policy:

- Same as game 1, scoped to game 2.
- Expected blank when game 2 was not played or no mulliganed-away evidence is
  present.
- Degraded/review-required when game 2 was played but hand ownership, snapshot
  history, card identity, or #140 mulligan context is missing/degraded.

Required signal examples:

- `parser_state.latest_hand_snapshot.game2`
- `parser_state.hand_snapshot_history.game2`
- `parser_state.bottomed_cards_capture.game2`
- `parser_state.match_summary.game2_mulliganed_away`
- `ledger.tier3.mulligans.game2_mulligans_dependency`
- `ledger.tier3.opening_hand.game2_opening_hand_dependency`

### `tier3.opening_hand.game3_mulliganed_away`

Field meaning:

- Parser field: `MatchSummary.games[3].mulliganed_away`
- Model surface: `GameSummary.mulliganed_away`
- Game-log alias: `Mulliganed Away` when `Game Number == 3`

Required evidence policy:

- Same as game 1, scoped to game 3.
- Expected blank when game 3 was not played or no mulliganed-away evidence is
  present.
- Degraded/review-required when game 3 was played but hand ownership, snapshot
  history, card identity, or #140 mulligan context is missing/degraded.

Required signal examples:

- `parser_state.latest_hand_snapshot.game3`
- `parser_state.hand_snapshot_history.game3`
- `parser_state.bottomed_cards_capture.game3`
- `parser_state.match_summary.game3_mulliganed_away`
- `ledger.tier3.mulligans.game3_mulligans_dependency`
- `ledger.tier3.opening_hand.game3_opening_hand_dependency`

## Dependency Map To Existing Entries

Codex C should make dependencies explicit in new entries and may update notes
on existing entries where helpful.

Required dependency links:

- each opening-hand entry depends on `tier3.game_results.game_number`.
- each exact opening-hand entry depends on
  `tier1.participants.local_system_seat_id`.
- each exact opening-hand entry should cite
  `tier1.participants.participant_team_mapping` when ownership confidence
  depends on local-seat/team mapping.
- each opening-hand size entry depends on its exact opening-hand entry first.
- each opening-hand size entry may fall back to the corresponding
  `tier3.mulligans.gameN_mulligans` entry.
- each mulliganed-away entry depends on its corresponding exact opening-hand
  entry when bottomed-card difference is used.
- each mulliganed-away entry depends on the corresponding
  `tier3.mulligans.gameN_mulligans` entry for mulligan-flow context.
- all exact-list entries depend on card instance-to-GRP mapping and card-name
  resolution behavior.

Forbidden dependency links:

- do not derive exact opening hand from opening-hand size.
- do not derive exact opening hand from mulligan count.
- do not derive exact opening hand from decklists, card-performance analytics,
  workbook formulas, dashboards, Apps Script, webhook transport, or AI output.
- do not derive mulligan count from opening hand or mulliganed-away cards.
- do not change GRP catalog or generated data behavior to satisfy this
  contract.

## Confidence, Finality, And Degradation Rules

Use existing vocabulary only:

- `value_source`: `observed`, `derived`, `unknown`, `conflict`
- `confidence`: `high`, `medium`, `low`, `unknown`
- `finality`: `live`, `provisional`, `final`, `reconciled`
- drift/degradation flags from the existing `DRIFT_FLAGS` vocabulary

Required policies:

- Exact local private-hand evidence with known local ownership, turn-one
  context, coherent expected size, and fully resolved card names may be
  high-confidence observed evidence.
- Private hand-zone evidence with missing or malformed owner-seat evidence is
  observed but degraded/review-required for local ownership.
- Placeholder-containing exact lists are observed but degraded for exact
  card-list display.
- Opening-hand size from exact hand length is observed.
- Opening-hand size from `7 - mulligans` fallback is derived and depends on
  #140 mulligan provenance.
- Mulliganed-away discarded hand evidence is observed from local hand snapshot
  history and mulligan flow.
- Mulliganed-away bottomed-card evidence is derived from list difference
  between prior longer snapshot and final hand.
- Missing system seat ids, missing hand zone, empty instance list, missing GRP
  mapping, unresolved card names, placeholder-only lists, turn-number mismatch,
  match-id mismatch, or expected-size mismatch are degraded/review-worthy.
- Data-loss, truncation, or line-buffer evidence lowers confidence; the ledger
  must not reconstruct missing hand data.
- Entries are generally `live` or `provisional` during active parsing and may
  be `final` once final match result evidence exists without later stronger
  correction.
- If later stronger evidence corrects a final opening-hand value, use
  `reconciled` in future field-evidence language.

Required degradation behavior:

- malformed owner-seat evidence cannot support high-confidence local ownership.
- missing or unresolved card identity degrades exact card-list confidence.
- placeholder-containing list serialization as blank is expected display
  behavior and must not be treated as evidence absence by itself.
- fallback opening-hand size is not exact hand evidence.
- unplayed-slot blanks are expected.
- played slots with missing local private-hand evidence are degraded and
  review-worthy.
- raw private hand contents must not be embedded in ledger entries or tests.

## Privacy And Serialization Rules

Opening-hand provenance must remain path-only and metadata-only.

The contract allows symbolic raw paths such as:

- `greToClientMessages[].gameStateMessage.systemSeatIds[]`
- `greToClientMessages[].gameStateMessage.zones[].type`
- `greToClientMessages[].gameStateMessage.zones[].visibility`
- `greToClientMessages[].gameStateMessage.zones[].ownerSeatId`
- `greToClientMessages[].gameStateMessage.zones[].objectInstanceIds[]`
- `greToClientMessages[].gameStateMessage.gameObjects[].instanceId`
- `greToClientMessages[].gameStateMessage.gameObjects[].grpId`
- `greToClientMessages[].gameStateMessage.turnInfo.turnNumber`
- `ledger.entries[tier3.mulligans.gameN_mulligans]`
- `ledger.entries[tier1.participants.local_system_seat_id]`

The contract forbids embedding:

- raw player names
- raw user ids
- raw private Player.log excerpts
- raw GameState payloads
- raw private hand contents
- raw opening-hand card lists
- raw mulliganed-away card lists
- raw object instance id values
- raw GRP id values as examples
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
- current local private-hand extraction behavior
- current opening-hand selection behavior
- current mulliganed-away capture behavior
- current card-name resolution and GRP catalog behavior
- current generated card data files
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

- `game_level_facts.seed_fields` includes the existing #134, #139, and #140
  fields plus the nine opening-hand fields.
- `game_level_facts.future_fields` no longer lists broad `opening_hand` after
  the granular entries are seeded.
- all nine `tier3.opening_hand.*` entries exist and validate.
- opening-hand size entries cite exact opening-hand dependency and #140
  mulligan fallback dependency.
- exact opening-hand entries cite local private-hand GameState zone evidence.
- exact opening-hand entries cite local-seat/participant dependencies from
  #137.
- exact opening-hand entries cite instance-to-GRP and card-name resolution
  dependencies.
- exact opening-hand entries document placeholder-containing lists as
  degraded/blank-display behavior.
- opening-hand size entries distinguish observed exact list length from
  derived fallback `7 - mulligans`.
- mulliganed-away entries cite discarded hand snapshot and bottomed-card
  difference evidence.
- mulliganed-away entries cite #140 mulligan dependency but do not claim to
  determine mulligan counts.
- unplayed game slot blank behavior is documented.
- played game slots with missing private-hand evidence are degraded or
  review-worthy in metadata language.
- all new signals use path-only privacy and do not embed raw card lists, raw
  instance id values, raw GRP id values, raw logs, or raw GameState payloads.
- #139 play/draw and #140 mulligan entries remain present and valid.
- `validate_player_log_evidence_ledger()` returns `[]`.
- every built-in entry passes `validate_ledger_entry(...)`.

Recommended adjacent behavior tests to run as evidence, not to change behavior:

- `tests/test_app_extractors.py`
- `tests/test_state.py`
- `tests/test_app_models.py`
- `tests/test_grp_id_catalog.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_golden_replay_harness.py`

Validation commands for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_app_extractors.py tests/test_state.py tests/test_app_models.py tests/test_grp_id_catalog.py tests/test_match_summary_from_match_state.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q
python3 -m ruff check src tests tools
git diff --check
```

If protected-surface tooling is available in the branch, Codex C should run the
repo's protected-surface checks and report `forbidden 0`.

## Acceptance Criteria

Issue #143 is implementation-ready when:

- this contract exists at
  `docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md`.
- Codex C can implement the opening-hand provenance slice with evidence-ledger
  metadata and tests only.
- no parser behavior changes are required.
- no protected surface changes are required.
- local private-hand ownership, exact list evidence, opening-hand size
  fallback, card-resolution degradation, placeholder serialization, and
  mulliganed-away provenance are distinguishable.
- dependencies on #137 participant/local-seat provenance and #140 mulligan
  provenance are explicit.
- raw private hand contents and generated data remain out of the repo diff.
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

  Act as Codex C: Module Implementer for issue #143, Tier 3 opening-hand ownership provenance under issue #11.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/143
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/140
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/142
    - Previous merge commit: 33a8bc2cba188389fe885b2446da51ac48c8555e
    - Base branch: codex/parser-reliability-intelligence
    - Recommended implementation branch: codex/player-log-evidence-ledger-tier3-opening-hand
    - Contract: docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md
    - Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md

  Goal:
    Implement the Tier 3 opening-hand ownership evidence-ledger provenance slice defined by the contract. Add or update evidence-ledger metadata and focused tests only.

  Read first:
    - AGENTS.md
    - docs/agent_rules.yml
    - docs/agent_constitution.md
    - docs/codex_module_workflow.md
    - docs/agent_threads/implementation.md
    - docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md
    - docs/contracts/player_log_evidence_ledger_schema.md
    - docs/contracts/player_log_evidence_ledger_participant_player_team.md
    - docs/contracts/player_log_evidence_ledger_tier3_game_results.md
    - docs/contracts/player_log_evidence_ledger_tier3_play_draw.md
    - docs/contracts/player_log_evidence_ledger_tier3_mulligans.md
    - src/mythic_edge_parser/app/evidence_ledger.py
    - tests/test_evidence_ledger.py
    - src/mythic_edge_parser/app/extractors.py
    - src/mythic_edge_parser/app/state.py
    - src/mythic_edge_parser/app/models.py
    - src/mythic_edge_parser/app/grp_id_catalog.py
    - src/mythic_edge_parser/app/sheet_schema.py

  Do:
    - Compare current evidence-ledger metadata against the contract before editing.
    - Add Tier 3 seed fields for game1/2/3_opening_hand_size, game1/2/3_opening_hand, and game1/2/3_mulliganed_away.
    - Add validating ledger entries for all nine tier3.opening_hand.* entries.
    - Preserve #134 game-result, #139 play/draw, and #140 mulligan seed fields, entries, notes, and tests.
    - Document local private-hand ownership evidence and malformed owner-seat degradation.
    - Document exact hand, opening-hand size fallback, placeholder serialization, and mulliganed-away provenance.
    - Keep privacy path-only and do not embed raw player values, raw logs, raw GameState payloads, raw hand lists, raw instance ids, raw GRP ids, or generated data.
    - Add focused tests in tests/test_evidence_ledger.py.
    - Produce docs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md with comparison, changes made, validation, risks, and next recommended role.

  Do not:
    - Change parser behavior.
    - Change local private-hand extraction behavior.
    - Change opening-hand selection behavior.
    - Change mulliganed-away capture behavior.
    - Change card-name resolution, GRP catalog behavior, generated card data, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth.
    - Rework, remove, or weaken #139 play/draw or #140 mulligan provenance.
    - Map turn-count, timing/duration, pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay, drift, schema snapshot, invariant execution, or runtime field-evidence attachment behavior.
    - Infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, label player mistakes, or move parser truth into AI/analytics truth.
    - Commit raw private Player.log excerpts, raw hand payloads, local diagnostics artifacts, or generated card data.
    - Target main directly.
    - Close issue #11.
    - Stage or commit unless explicitly asked.

  Validation:
    - python3 -m pytest -q tests/test_evidence_ledger.py
    - python3 -m pytest -q tests/test_app_extractors.py tests/test_state.py tests/test_app_models.py tests/test_grp_id_catalog.py tests/test_match_summary_from_match_state.py
    - python3 -m pytest -q tests/test_golden_replay_harness.py
    - python3 -m pytest -q
    - python3 -m ruff check src tests tools
    - git diff --check

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/143"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/140"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/142"
  previous_merge_commit: "33a8bc2cba188389fe885b2446da51ac48c8555e"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md"
  verdict: "tier3_opening_hand_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-opening-hand"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_app_extractors.py tests/test_state.py tests/test_app_models.py tests/test_grp_id_catalog.py tests/test_match_summary_from_match_state.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, local private-hand extraction behavior, opening-hand selection behavior, mulliganed-away capture behavior, card-name resolution, GRP catalog behavior, generated card data, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not rework, remove, or weaken #139 play/draw or #140 mulligan provenance."
    - "Do not map turn-count, timing/duration, pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay, drift, schema snapshot, invariant execution, or runtime field-evidence attachment behavior."
    - "Do not reconstruct missing GameState data, infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, label player mistakes, or move parser truth into AI/analytics truth."
    - "Do not commit raw private Player.log excerpts, raw hand payloads, local diagnostics artifacts, generated card data, or workbook exports."
```

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/143"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/140"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/142"
  previous_merge_commit: "33a8bc2cba188389fe885b2446da51ac48c8555e"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_opening_hand_comparison.md"
  verdict: "tier3_opening_hand_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-opening-hand"
  validation:
    - "not run - contract writer pass"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not implement code in Codex B."
    - "Do not change parser behavior, local private-hand extraction behavior, opening-hand selection behavior, mulliganed-away capture behavior, card-name resolution, GRP catalog behavior, generated card data, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not rework, remove, or weaken #139 play/draw or #140 mulligan provenance."
    - "Do not map turn-count, timing/duration, pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay, drift, schema snapshot, invariant execution, or runtime field-evidence attachment behavior."
    - "Do not reconstruct missing GameState data, infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, label player mistakes, or move parser truth into AI/analytics truth."
    - "Do not commit raw private Player.log excerpts, raw hand payloads, local diagnostics artifacts, generated card data, or workbook exports."
