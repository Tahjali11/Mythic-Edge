# Player.log Evidence Ledger Tier 3 Mulligans Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/140
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/139
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/141
- previous_merge_commit: 734c7c7f587e0951073b0c01b834e38cd7c60de1
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier3-mulligans
- target_artifact: docs/contracts/player_log_evidence_ledger_tier3_mulligans.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier3_mulligans_comparison.md
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
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- docs/decisions/ADR-0003-player-log-drift-policy.md

## Purpose

Issue #140 maps Tier 3 mulligan-count provenance in the Player.log evidence
ledger.

Mulligan counts are parser-owned derived values built from ClientAction
mulligan responses, current match/game context, parser state counters, and
`MatchSummary` / `GameSummary` model state. They are not standalone workbook
truth, analytics truth, or AI truth.

This contract documents provenance metadata only. It must not change parser
behavior, mulligan counting behavior, ClientAction parsing, parser state final
reconciliation, event classes, workbook schema, webhook payload shape, Apps
Script behavior, output transport, match/game identity, deduplication, or
analytics truth.

## Prior Play/Draw Boundary

Issue #139 is the completed sibling Tier 3 play/draw provenance slice.

PR #141 merged #139 into `codex/parser-reliability-intelligence` at
`734c7c7f587e0951073b0c01b834e38cd7c60de1`. Codex C may proceed from a branch
that contains that merge commit. The implementation must preserve the #139
play/draw entries, seed fields, notes, and tests while adding the mulligan
slice.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, validators, vocabulary constants, and privacy posture.

`docs/contracts/player_log_evidence_ledger_participant_player_team.md` remains
authoritative for local participant and player-team provenance. Mulligan counts
do not depend on player-team identity for counting, but future opening-hand and
local-zone interpretations may depend on participant provenance.

`docs/contracts/player_log_evidence_ledger_tier3_game_results.md` remains
authoritative for game number, per-game winners, and per-game result
provenance. Mulligan entries depend on game-slot identity but must not infer
counts from game result fields.

`docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md` remains
authoritative for result-derived match aggregates. `total_mulligans` is not a
Tier 1 result aggregate in issue #140; it is a Tier 3 mulligan entry derived
from per-game mulligan counts.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #140 provenance should be
recorded through this contract, implementation handoff, entry notes, and
focused tests rather than by changing the top-level ledger object shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- ClientAction parsing exposes mulligan response evidence.
- `src/mythic_edge_parser/app/state.py` owns `_MULLIGAN_COUNTS`,
  `_next_mulligan_count(...)`, current match/game context usage, and how
  ClientAction events update per-game model state.
- `src/mythic_edge_parser/app/models.py` owns `GameSummary.mulligans`,
  `MatchSummary.set_game_mulligans(...)`,
  `MatchSummary._game_mulligan_fields()`, `MatchSummary.total_mulligans`, and
  row serialization values.
- `src/mythic_edge_parser/app/evidence_ledger.py` describes provenance,
  confidence, finality, degradation, and review expectations.
- Workbook rows, Apps Script, webhook transport, dashboards, diagnostics,
  golden replay, feature-equity reports, drift reports, card-performance
  analytics, and AI output are downstream consumers only.

The ledger must not reconstruct missing ClientAction or GameState data, infer
hidden cards, infer decklists, classify archetypes, provide gameplay advice,
infer player mistakes, or move parser truth into workbook formulas, dashboard
logic, Apps Script, webhook transport, output transport, or AI.

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` after PR #141:

- The Tier 3 `game_level_facts` family is already `seeded_sample` for game
  number, game winners, game results, starting-player, and play/draw
  provenance.
- The same family still lists broad future field `mulligans`.
- `client_actions.py` specializes `ClientMessageType_MulliganResp` as a
  `mulligan_resp` ClientAction event.
- `MULLIGAN_DECISION_MAP` maps `MulliganOption_Mulligan` to `mulligan` and
  `MulliganOption_AcceptHand` to `keep`.
- Unknown future mulligan decisions are preserved as their original value.
- Missing or malformed `mulliganResp` payloads produce a `mulligan_resp` event
  with blank `decision`.
- Specialized ClientAction payloads preserve `game_state_id`, `resp_id`,
  `request_id`, and `raw_client_action`.
- `state.py` reads current `match_id` and `game_number` from parser context
  before applying a mulligan response.
- `_next_mulligan_count(match_id, game_number, decision)` returns `0` when
  match id or game number is missing.
- `_next_mulligan_count(...)` returns the current count for keep-like decisions
  `keep`, `kept`, `accept`, or `accepted`.
- `_next_mulligan_count(...)` increments the current count for any non-keep
  decision, including blank or unknown future decision values.
- `state.py` records discarded mulligan hands for non-keep decisions, but
  exact hand and mulliganed-away provenance is deferred by this contract.
- `MatchSummary.set_game_mulligans(...)` stores integer and integer-like string
  values for valid game slots.
- `MatchSummary.set_game_mulligans(...)` ignores booleans, invalid strings,
  non-finite floats, non-integral floats, negative values, and invalid game
  slots.
- `GameSummary.mulligans` defaults to `0`.
- `GameSummary.has_summary_data()` treats `mulligans > 0` as summary data, but
  a zero-mulligan game can still have summary data through winner, starting
  player, timing, turn count, opening hand, or mulliganed-away evidence.
- `MatchSummary._game_mulligan_fields()` returns `g1_mulligans`,
  `g2_mulligans`, and `g3_mulligans` from fixed game slots.
- `MatchSummary.total_mulligans` sums all per-game `GameSummary.mulligans`
  values.
- Match-log row fields `G1 Mulligans`, `G2 Mulligans`, and `G3 Mulligans`
  display the per-game count only when the game slot has summary data;
  otherwise they are blank.
- Match-log row field `MTGA Mulligans` displays `total_mulligans` on final rows
  even when it is `0`, but live rows display blank when total mulligans are
  zero.
- Game-log row field `Mulligans` displays the per-game count when the game has
  `first_event_time`; otherwise it is blank.
- `GameSummary.opening_hand_size()` falls back to `max(7 - mulligans, 0)` when
  no exact opening-hand list exists but the game has started.

Observed risks, not fixed by this issue:

- Current `_next_mulligan_count(...)` treats blank or unknown future decisions
  as non-keep and increments. The evidence ledger must not describe those
  values as high-confidence observed mulligans without degradation language.
- Current display rows can contain `0` for clean counts and `""` for no row
  display. The ledger must distinguish real zero from expected blank.
- Opening-hand size may depend on mulligans, but opening-hand, exact hand, and
  mulliganed-away provenance are not solved by issue #140.

## Scope Decision

Codex C should implement issue #140 as a Tier 3 `game_level_facts` metadata
slice in the existing evidence ledger.

Do not add a new output family. Do not add a workbook column, webhook field,
runtime status field, parser event class, parser behavior path, analytics
surface, or runtime field-evidence attachment.

Required Tier 3 seed fields to add:

- `game1_mulligans`
- `game2_mulligans`
- `game3_mulligans`
- `total_mulligans`

Required Tier 3 entries:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier3.mulligans.game1_mulligans` | `game1_mulligans` | `G1 Mulligans` | `observed` or `derived` |
| `tier3.mulligans.game2_mulligans` | `game2_mulligans` | `G2 Mulligans` | `observed` or `derived` |
| `tier3.mulligans.game3_mulligans` | `game3_mulligans` | `G3 Mulligans` | `observed` or `derived` |
| `tier3.mulligans.total_mulligans` | `total_mulligans` | `MTGA Mulligans` | `derived` |

Required family metadata:

- Keep `game_level_facts.status` as `seeded_sample`.
- Add the four fields above to `game_level_facts.seed_fields`.
- Remove broad `mulligans` from `game_level_facts.future_fields` once the
  granular entries are seeded.
- Preserve the #139 play/draw seed fields already present on the branch.
- Keep remaining future fields, at minimum:
  - `turn_count`
  - `opening_hand`
  - `game_timing`
  - `game_duration`
  - `pre_postboard`
  - `sideboarding`
  - `deck_state`
- Add notes stating that issue #140 maps the mulligan provenance slice and
  defers opening-hand, mulliganed-away, analytics, diagnostics, replay, drift,
  and field-evidence attachment work.

## Deferred Work

Defer all of the following:

- parser behavior changes
- mulligan counting behavior changes
- ClientAction parsing changes
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
- new play/draw behavior or provenance changes beyond preserving #139
- opening-hand provenance
- opening-hand size provenance
- exact opening-hand provenance
- mulliganed-away provenance
- card-performance or mulligan-tax analytics
- gameplay advice, mistake labels, deck inference, archetype classification, or
  AI/model-provider behavior

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier3_mulligans.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier3_mulligans_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier3_mulligans.md

Referenced but not owned:

- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_participant_player_team.md
- docs/contracts/player_log_evidence_ledger_tier3_game_results.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/parser_client_actions.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- src/mythic_edge_parser/parsers/client_actions.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/transforms.py
- src/mythic_edge_parser/app/sheet_schema.py
- tests/test_evidence_ledger.py
- tests/test_client_actions_parser.py
- tests/test_state.py
- tests/test_app_models.py
- tests/test_transforms.py
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
- Every new mulligan entry passes `validate_ledger_entry(...)`.
- The built ledger passes `validate_player_log_evidence_ledger(...)`.
- Entry IDs and signal IDs remain stable, lowercase, and dot-separated.
- Source paths remain repo-relative or symbolic.
- Raw payload values, raw private log excerpts, absolute local paths, secrets,
  webhook URLs, local runtime artifacts, generated data, failed posts, and
  workbook exports must not be embedded.

## Field Inventory

### `gameN_mulligans`

Meaning:

- The parser-owned mulligan count for fixed game slot `N`, where `N` is `1`,
  `2`, or `3`.

Current surfaces:

- `GameSummary.mulligans`
- `MatchSummary._game_mulligan_fields()`
- `MatchSummary.to_debug_dict()` fields `g1_mulligans`, `g2_mulligans`, and
  `g3_mulligans`
- Match-log row fields `G1 Mulligans`, `G2 Mulligans`, `G3 Mulligans`
- Game-log row field `Mulligans` for the row's game number
- ClientAction row `mulligan_count` as a live event/reporting surface

Output role:

- Parser-owned per-game fact.
- Existing workbook-visible downstream aliases already exist; issue #140 must
  not change their shape.

### `total_mulligans`

Meaning:

- The parser-owned total mulligan count for the match, derived from per-game
  mulligan counts.

Current surfaces:

- `MatchSummary.total_mulligans`
- `MatchSummary.to_sheet_row()` field `total_mulligans`
- Match-log row field `MTGA Mulligans`
- Match-history/debug payloads

Output role:

- Tier 3 derived mulligan field.
- Not a Tier 1 result aggregate.
- Not a directly observed raw-log value.

## Source Evidence Priority

This priority is for ledger confidence and provenance language. It must not be
implemented as a parser behavior change in issue #140.

### Direct ClientAction Evidence

Use high-confidence `observed` provenance for a per-game mulligan increment
when a current-match/current-game ClientAction event has:

- `payload.type == "mulligan_resp"`
- known match id from parser context
- known game number from parser context
- normalized `decision == "mulligan"`
- coherent state counter progression for that game slot

Relevant raw and normalized paths:

- `ClientToGREMessage.payload.type`
- `ClientToGREMessage.payload.mulliganResp.decision`
- `payload.type`
- `payload.decision`
- `payload.game_state_id`
- `payload.resp_id`
- `payload.request_id`

Use medium-confidence `observed` or `derived` provenance for keep-like
responses when they confirm the current count:

- `decision == "keep"`
- `decision == "kept"`
- `decision == "accept"`
- `decision == "accepted"`

Keep-like decisions do not increment the count. They can support confidence in
the current count only when match/game context is known.

### Parser State Counter Evidence

Use derived provenance for values read from:

- `_MULLIGAN_COUNTS[(match_id, game_number)]`
- `GameSummary.mulligans`
- `MatchSummary._game_mulligan_fields()`

Parser state counter evidence is required to explain final row values, but it
is not raw-log observed evidence by itself.

### Game Slot Identity

Per-game mulligan entries depend on game slot identity.

Required dependency:

- `tier3.game_results.game_number`

If match id or game number is missing, `_next_mulligan_count(...)` currently
returns `0`. The ledger must describe that as missing-context fallback, not a
high-confidence clean zero.

### Total Mulligans

`total_mulligans` is derived from:

- `tier3.mulligans.game1_mulligans`
- `tier3.mulligans.game2_mulligans`
- `tier3.mulligans.game3_mulligans`
- `MatchSummary.total_mulligans`

`total_mulligans` must not be described as directly observed from raw logs,
workbook formulas, Apps Script, dashboard logic, or AI.

## Decision Semantics

Required decision vocabulary:

- `mulligan`: observed non-keep response; increments count.
- `keep`, `kept`, `accept`, `accepted`: keep-like response; confirms current
  count without incrementing.
- `unknown`: blank, missing, malformed, future, or unrecognized decision value.

Current parser behavior increments for non-keep values, including blank and
unknown future values. Provenance must not label those increments as
high-confidence observed mulligans.

Contracted provenance policy:

- Known `mulligan` decision can support high-confidence count increment.
- Known keep-like decision can support current-count confirmation.
- Unknown, blank, malformed, or future decision values are degraded and
  review-required.
- Missing match or game context is degraded and review-required.
- Duplicate or replayed ClientAction evidence is review-required unless a
  future behavior contract proves deduplication for this surface.

## Zero And Blank Semantics

Zero is a valid count. Blank is a display/state condition.

Required policy:

- `0` can be high-confidence only when the game is known to have been played
  and the parser has coherent keep/no-mulligan evidence or final parser state.
- `0` with missing match/game context is not high-confidence.
- `0` in a final match row `MTGA Mulligans` means total parser count is zero.
- blank `MTGA Mulligans` in a live match row means total parser count is zero
  and row finality is live/provisional.
- blank `G1/G2/G3 Mulligans` means the corresponding game slot lacks summary
  data for display; it does not prove zero mulligans.
- blank game-log `Mulligans` means no game row should be emitted or no first
  event time exists for the game; it does not prove zero mulligans.
- unplayed game slots should be expected blank, not degraded.
- played game slots with missing or degraded ClientAction evidence should be
  represented as unknown/degraded rather than silently clean.

## Output Entries

### `tier3.mulligans.game1_mulligans`

Field meaning:

- Parser field: `MatchSummary._game_mulligan_fields()["g1_mulligans"]`
- Model surface: `MatchSummary.games[1].mulligans`
- Match-row alias: `G1 Mulligans`
- Game-log alias: `Mulligans` when `Game Number == 1`

Required evidence policy:

- `observed` from known game 1 `mulligan_resp` events with known match/game
  context.
- `derived` from `GameSummary.mulligans` and `_MULLIGAN_COUNTS`.
- `unknown` or degraded when match/game context is missing or decision value is
  unknown.
- expected blank when game 1 has no summary data and no game row.

Required signal examples:

- `client_action.game1.mulligan_response`
- `parser_state.mulligan_counts.game1`
- `parser_state.match_summary.game1_mulligans`
- `tier3.game_results.game_number_dependency`

Required invariants:

- game 1 mulligan count must not be inferred from opening-hand size.
- unknown decisions must not be high-confidence mulligan evidence.
- blank display is not equivalent to zero.

### `tier3.mulligans.game2_mulligans`

Field meaning:

- Parser field: `MatchSummary._game_mulligan_fields()["g2_mulligans"]`
- Model surface: `MatchSummary.games[2].mulligans`
- Match-row alias: `G2 Mulligans`
- Game-log alias: `Mulligans` when `Game Number == 2`

Required evidence policy:

- Same as game 1, scoped to game 2.
- Expected blank when game 2 was not played.
- Degraded/review-required when game 2 was played but mulligan ClientAction
  evidence is missing, malformed, contextless, or contradictory.

Required signal examples:

- `client_action.game2.mulligan_response`
- `parser_state.mulligan_counts.game2`
- `parser_state.match_summary.game2_mulligans`
- `tier3.game_results.game_number_dependency`

### `tier3.mulligans.game3_mulligans`

Field meaning:

- Parser field: `MatchSummary._game_mulligan_fields()["g3_mulligans"]`
- Model surface: `MatchSummary.games[3].mulligans`
- Match-row alias: `G3 Mulligans`
- Game-log alias: `Mulligans` when `Game Number == 3`

Required evidence policy:

- Same as game 1, scoped to game 3.
- Expected blank when game 3 was not played.
- Degraded/review-required when game 3 was played but mulligan ClientAction
  evidence is missing, malformed, contextless, or contradictory.

Required signal examples:

- `client_action.game3.mulligan_response`
- `parser_state.mulligan_counts.game3`
- `parser_state.match_summary.game3_mulligans`
- `tier3.game_results.game_number_dependency`

### `tier3.mulligans.total_mulligans`

Field meaning:

- Parser field: `MatchSummary.total_mulligans`
- Debug alias: `total_mulligans`
- Match-row alias: `MTGA Mulligans`

Required evidence policy:

- `derived` from the three per-game mulligan entries.
- `derived` from `MatchSummary.total_mulligans`.
- `unknown` or degraded when one or more played game slots have unknown or
  conflicting mulligan provenance.
- Expected `0` on final rows when all known per-game counts are zero and no
  played slot is degraded.
- Expected blank on live match rows when total is zero and finality is live.

Required signal examples:

- `parser_state.match_summary.total_mulligans`
- `ledger.tier3.mulligans.game1_mulligans_dependency`
- `ledger.tier3.mulligans.game2_mulligans_dependency`
- `ledger.tier3.mulligans.game3_mulligans_dependency`

Required invariants:

- total mulligans equals the sum of per-game mulligan counts.
- total mulligans is derived, not observed.
- total mulligans must not include unplayed-slot blanks as counts.
- total mulligans must not be inferred from opening-hand size, card analytics,
  workbook formulas, dashboard logic, Apps Script, webhook transport, or AI.

## Dependency Map To Existing Entries

Codex C should make dependencies explicit in new entries and may update notes
on existing entries where helpful.

Required dependency links:

- each per-game mulligan entry depends on `tier3.game_results.game_number`.
- each per-game mulligan entry may cite parser context
  `current_match_id` and `current_game_number` as required context.
- `total_mulligans` depends on all three per-game mulligan entries.
- opening-hand provenance remains deferred but may note that
  `opening_hand_size()` can consume mulligan counts later.

Forbidden dependency links:

- do not derive mulligan counts from opening-hand size.
- do not derive mulligan counts from exact opening hand or mulliganed-away
  cards.
- do not derive mulligan counts from play/draw, game result, match result,
  aggregate result fields, workbook formulas, dashboards, Apps Script, webhook
  transport, or AI output.

## Confidence, Finality, And Degradation Rules

Use existing vocabulary only:

- `value_source`: `observed`, `derived`, `unknown`, `conflict`
- `confidence`: `high`, `medium`, `low`, `unknown`
- `finality`: `live`, `provisional`, `final`, `reconciled`
- drift/degradation flags from the existing `DRIFT_FLAGS` vocabulary

Required policies:

- Known non-keep `mulligan` decisions in known match/game context may be
  high-confidence observed increment evidence.
- Keep-like decisions in known match/game context may be medium-confidence
  observed confirmation evidence for the current count.
- Per-game final counts are derived from parser state and ClientAction
  evidence.
- Total mulligans is derived from per-game counts.
- Missing match id or game number is low confidence and review-required.
- Unknown, blank, malformed, or future decisions are degraded and
  review-required.
- Contextless fallback `0` is not a high-confidence clean zero.
- Duplicate or replayed ClientAction risk is review-required unless a future
  behavior contract proves this surface is deduplicated.
- Data-loss, truncation, or line-buffer evidence lowers confidence; the ledger
  must not reconstruct missing mulligan actions.
- Entries are generally `live` or `provisional` during active parsing and may
  be `final` once final match result evidence exists without later stronger
  correction.
- If later stronger evidence corrects a final count, use `reconciled` in
  future field-evidence language.

Required degradation behavior:

- missing context leaves per-game count unknown or degraded.
- unknown decision values cannot support high-confidence observed mulligans.
- expected unplayed-slot blanks are not failures.
- played slots with missing ClientAction evidence require review language.
- final total `0` can be valid; live blank total can also be valid.
- opening-hand size fallback is a downstream dependency, not evidence for
  mulligan count.

## Privacy And Serialization Rules

Mulligan provenance must remain path-only and metadata-only.

The contract allows symbolic raw paths such as:

- `ClientToGREMessage.payload.type`
- `ClientToGREMessage.payload.mulliganResp.decision`
- `ClientToGREMessage.payload.gameStateId`
- `ClientToGREMessage.payload.respId`
- `ClientToGREMessage.requestId`

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
- raw opening-hand card lists
- raw mulliganed-away card lists

## Compatibility Expectations

Implementation must preserve:

- ledger schema version unless a separate contract authorizes a version bump
- public evidence-ledger constants and validators
- current parser behavior
- current mulligan counting behavior
- current ClientAction parsing behavior
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

- Codex C verifies the branch contains PR #141 / merge commit
  `734c7c7f587e0951073b0c01b834e38cd7c60de1` before editing.
- #139 play/draw seed fields and `tier3.play_draw.*` entries remain present
  and valid after mulligan entries are added.
- `game_level_facts.seed_fields` includes the existing #134 and #139 fields
  plus `game1_mulligans`, `game2_mulligans`, `game3_mulligans`, and
  `total_mulligans`.
- `game_level_facts.future_fields` no longer lists broad `mulligans` after the
  granular entries are seeded.
- all four `tier3.mulligans.*` entries exist and validate.
- per-game mulligan entries cite direct ClientAction `mulligan_resp` evidence.
- per-game mulligan entries cite parser state count/model dependencies.
- per-game mulligan entries cite game-number or current-game context
  dependencies.
- total mulligans entry cites all three per-game mulligan dependencies.
- total mulligans is documented as `derived`, not `observed`.
- unknown, blank, malformed, or future decision values are documented as
  degraded/review-required.
- zero/blank semantics are documented for game-log and match-log outputs.
- opening-hand, exact hand, and mulliganed-away fields remain deferred.
- all new signals use path-only privacy and do not embed raw values.
- `validate_player_log_evidence_ledger()` returns `[]`.
- every built-in entry passes `validate_ledger_entry(...)`.

Recommended adjacent behavior tests to run as evidence, not to change behavior:

- `tests/test_client_actions_parser.py`
- `tests/test_state.py`
- `tests/test_app_models.py`
- `tests/test_transforms.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_golden_replay_harness.py`

Validation commands for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q
python3 -m ruff check src tests tools
git diff --check
```

If protected-surface tooling is available in the branch, Codex C should run the
repo's protected-surface checks and report `forbidden 0`.

## Acceptance Criteria

Issue #140 is implementation-ready when:

- this contract exists at
  `docs/contracts/player_log_evidence_ledger_tier3_mulligans.md`.
- Codex C can implement the mulligan provenance slice with evidence-ledger
  metadata and tests only on top of the merged #139 play/draw package.
- no parser behavior changes are required.
- no protected surface changes are required.
- direct response evidence, parser-state derived counts, total count
  derivation, zero/blank semantics, missing context, and unknown decisions are
  distinguishable.
- opening-hand and mulliganed-away provenance remain explicitly deferred.
- the route to Codex C is unambiguous and requires preserving the #139
  play/draw entries.

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

  Act as Codex C: Module Implementer for issue #140, Tier 3 mulligan provenance under issue #11.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/140
    - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/139
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/141
    - Previous merge commit: 734c7c7f587e0951073b0c01b834e38cd7c60de1
    - Base branch: codex/parser-reliability-intelligence
    - Recommended implementation branch: codex/player-log-evidence-ledger-tier3-mulligans
    - Contract: docs/contracts/player_log_evidence_ledger_tier3_mulligans.md
    - Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier3_mulligans_comparison.md

  Gate:
    - Before editing, verify your branch contains PR #141 / merge commit 734c7c7f587e0951073b0c01b834e38cd7c60de1.
    - If the merge commit is missing, sync from codex/parser-reliability-intelligence before editing.

  Goal:
    Implement the Tier 3 mulligan evidence-ledger provenance slice defined by the contract. Add or update evidence-ledger metadata and focused tests only.

  Read first:
    - AGENTS.md
    - docs/agent_rules.yml
    - docs/agent_constitution.md
    - docs/codex_module_workflow.md
    - docs/agent_threads/implementation.md
    - docs/contracts/player_log_evidence_ledger_tier3_mulligans.md
    - docs/contracts/player_log_evidence_ledger_schema.md
    - docs/contracts/player_log_evidence_ledger_participant_player_team.md
    - docs/contracts/player_log_evidence_ledger_tier3_game_results.md
    - docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
    - src/mythic_edge_parser/app/evidence_ledger.py
    - tests/test_evidence_ledger.py
    - src/mythic_edge_parser/parsers/client_actions.py
    - src/mythic_edge_parser/app/state.py
    - src/mythic_edge_parser/app/models.py
    - src/mythic_edge_parser/app/sheet_schema.py

  Do:
    - Compare current evidence-ledger metadata against the contract before editing.
    - Add Tier 3 seed fields for game1_mulligans, game2_mulligans, game3_mulligans, and total_mulligans.
    - Add validating ledger entries for tier3.mulligans.game1_mulligans, tier3.mulligans.game2_mulligans, tier3.mulligans.game3_mulligans, and tier3.mulligans.total_mulligans.
    - Preserve #139 play/draw seed fields, entries, notes, and tests.
    - Make total_mulligans explicitly derived from the three per-game mulligan entries.
    - Document zero/blank/final/live semantics in evidence metadata.
    - Document unknown, blank, malformed, or future decision values as degraded/review-required.
    - Keep privacy path-only and do not embed raw player values, raw logs, raw hand lists, or raw mulliganed-away card lists.
    - Add focused tests in tests/test_evidence_ledger.py.
    - Produce docs/implementation_handoffs/player_log_evidence_ledger_tier3_mulligans_comparison.md with comparison, changes made, validation, risks, and next recommended role.

  Do not:
    - Change parser behavior.
    - Change mulligan counting behavior.
    - Change ClientAction parsing behavior.
    - Change parser state final reconciliation.
    - Change parser event classes.
    - Change workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or production behavior.
    - Rework, remove, or weaken #139 play/draw provenance.
    - Map play/draw, opening-hand, opening-hand size, exact hand, mulliganed-away, turn-count, timing/duration, pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay, drift, schema snapshot, invariant execution, or runtime field-evidence attachment behavior.
    - Infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, or AI/analytics truth.
    - Commit raw private Player.log excerpts.
    - Target main directly.
    - Close issue #11.
    - Stage or commit unless explicitly asked.

  Validation:
    - python3 -m pytest -q tests/test_evidence_ledger.py
    - python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py
    - python3 -m pytest -q tests/test_golden_replay_harness.py
    - python3 -m pytest -q
    - python3 -m ruff check src tests tools
    - git diff --check

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/140"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/139"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/141"
  previous_merge_commit: "734c7c7f587e0951073b0c01b834e38cd7c60de1"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_mulligans.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_mulligans_comparison.md"
  verdict: "tier3_mulligan_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-mulligans"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_client_actions_parser.py tests/test_state.py tests/test_app_models.py tests/test_transforms.py tests/test_match_summary_from_match_state.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Verify the branch contains PR #141 / merge commit 734c7c7f587e0951073b0c01b834e38cd7c60de1 before editing."
    - "Do not rework, remove, or weaken #139 play/draw provenance."
    - "Do not change parser behavior, mulligan counting behavior, ClientAction parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not map play/draw, opening-hand, opening-hand size, exact hand, mulliganed-away, turn-count, timing/duration, pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay, drift, schema snapshot, invariant execution, or runtime field-evidence attachment behavior."
    - "Do not reconstruct missing GameState data or infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, or AI/analytics truth."
    - "Do not commit raw private Player.log excerpts or local diagnostics artifacts."
```

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/140"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/139"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/141"
  previous_merge_commit: "734c7c7f587e0951073b0c01b834e38cd7c60de1"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_mulligans.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_mulligans_comparison.md"
  verdict: "tier3_mulligan_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier3-mulligans"
  validation:
    - "not run - contract writer pass"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not implement code in Codex B."
    - "Verify the branch contains PR #141 / merge commit 734c7c7f587e0951073b0c01b834e38cd7c60de1 before editing."
    - "Do not rework, remove, or weaken #139 play/draw provenance."
    - "Do not change parser behavior, mulligan counting behavior, ClientAction parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, environment variable contracts, or AI/analytics truth."
    - "Do not map play/draw, opening-hand, opening-hand size, exact hand, mulliganed-away, turn-count, timing/duration, pre/postboard, sideboarding, deck-state, analytics, diagnostics, replay, drift, schema snapshot, invariant execution, or runtime field-evidence attachment behavior."
    - "Do not reconstruct missing GameState data or infer hidden cards, decklists, archetypes, gameplay advice, player mistakes, or AI/analytics truth."
    - "Do not commit raw private Player.log excerpts or local diagnostics artifacts."
