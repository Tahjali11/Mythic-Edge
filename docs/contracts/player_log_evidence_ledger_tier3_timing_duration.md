# Player.log Evidence Ledger Tier 3 Timing And Duration Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/147
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/145
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/146
- previous_merge_commit: 0aede4890710768c7abd2fb2a561c7ce8b10fdba
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier3-timing-duration
- target_artifact: docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md
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
- docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md
- docs/contracts/player_log_evidence_ledger_tier3_turn_count.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- docs/decisions/ADR-0003-player-log-drift-policy.md

## Purpose

Issue #147 maps Tier 3 game timing and game duration provenance in the
Player.log evidence ledger.

Game timing is parser-owned observation-boundary data. It records when Mythic
Edge first and last observed parser events assigned to a game slot. Game
duration is derived from those stored endpoints through
`GameSummary.duration_seconds()`.

These values are not Arena internal clock values. They are not rope timers,
priority timers, player clock pressure, complete game timelines, or gameplay
advice. They must not be reconstructed from turn count, result evidence,
action volume, workbook formulas, dashboards, analytics, or AI output.

This contract documents provenance metadata only. It must not change parser
behavior, timestamp parsing, `_safe_iso(...)`, `GameSummary.touch(...)`,
`MatchSummary.touch_game(...)`, `duration_seconds()`, parser state final
reconciliation, parser event classes, workbook schema, webhook payload shape,
Apps Script behavior, output transport, match/game identity, deduplication,
generated data, runtime artifacts, or analytics truth.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, validators, vocabulary constants, privacy posture, and
the allowed `value_source`, `confidence`, `finality`, invariant, and drift
vocabularies.

`docs/contracts/player_log_evidence_ledger_tier3_game_results.md` remains
authoritative for game number and game-slot identity. Timing entries depend on
game-slot assignment but must not infer timing from winners or results.

`docs/contracts/player_log_evidence_ledger_tier3_turn_count.md` remains
authoritative for max-observed turn-count provenance. Duration must not be
reconstructed from turn count, and turn count must not be reconstructed from
duration.

`docs/contracts/player_log_evidence_ledger_tier3_play_draw.md`,
`docs/contracts/player_log_evidence_ledger_tier3_mulligans.md`, and
`docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md` are sibling
Tier 3 slices. Issue #147 must preserve their seed fields, entries, notes, and
tests.

Tier 1 `match_started_at` and `match_finished_at` entries already describe
match-level timing fields such as `MGTA Start Time` and `MTGA End Time`.
Issue #147 does not replace or redefine those match-level entries. It adds
game-level timing and duration provenance.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #147 provenance should be
recorded through this contract, implementation handoff, entry notes, and
focused tests rather than by changing the top-level ledger object shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- `src/mythic_edge_parser/router.py` owns extraction of a timestamp from the
  first log-entry line and tracks timestamp-missing and timestamp-parse-failure
  stats.
- `EventMetadata.timestamp` carries the parser event timestamp when extraction
  succeeds.
- `src/mythic_edge_parser/app/extractors.py` owns `_safe_iso(...)` and its
  current fallback behavior when event metadata lacks a valid timestamp.
- `src/mythic_edge_parser/app/state.py` owns when parser events touch match and
  game summaries.
- `src/mythic_edge_parser/app/models.py` owns
  `GameSummary.first_event_time`, `GameSummary.last_event_time`,
  `GameSummary.duration_seconds()`, `GameSummary.to_debug_dict()`, and
  game-log row serialization for `timestamp` and `Game Duration`.
- `src/mythic_edge_parser/app/evidence_ledger.py` describes provenance,
  confidence, finality, degradation, drift, and review expectations.
- Workbook rows, Apps Script, webhook transport, dashboards, diagnostics,
  golden replay, feature-equity reports, drift reports, timing analytics,
  clock-pressure analytics, gameplay advice, and AI output are downstream
  consumers only.

The evidence ledger describes support for parser-owned timing fields. It does
not compute time, repair timestamps, reconstruct missing events, decide game
duration truth, or promote runtime clock fallback into Arena timing truth.

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` at
`0aede4890710768c7abd2fb2a561c7ce8b10fdba`:

- The Tier 3 `game_level_facts` family is already `seeded_sample` for game
  number, per-game winners, per-game results, starting-player, play/draw,
  mulligan, opening-hand, mulliganed-away, and turn-count provenance.
- The same family still lists broad future fields `game_timing` and
  `game_duration`.
- `router._extract_timestamp_state(...)` reads only the first log-entry line
  for a timestamp.
- Missing timestamp text increments router `timestamp_missing` stats.
- Invalid timestamp text increments router `timestamp_parse_failure` stats.
- Successful timestamp parsing returns a UTC `datetime`.
- Parser events carry timestamp evidence through `EventMetadata.timestamp`.
- `_safe_iso(event)` returns `event.metadata.timestamp.isoformat()` when the
  metadata timestamp is a `datetime`.
- `_safe_iso(event)` currently falls back to `datetime.now().isoformat()` when
  event metadata is missing or not a `datetime`.
- `MatchSummary.touch(...)` and `GameSummary.touch(...)` ignore blank
  timestamps, set `first_event_time` only once, and update `last_event_time`
  on each nonblank timestamp.
- `state._set_first_last(...)` touches match summary timing from parser events
  that update a match summary.
- GameState events touch game timing when a match id and game number can be
  resolved.
- ClientAction events touch game timing when current parser context has a game
  number.
- GameResult events touch game timing through their resolved game number.
- Rank events can touch match timing while a current match exists and the
  summary is not final-ready, but they do not touch game timing.
- MatchState events touch match timing and can set current game number to `1`
  for `match_started`, but they do not directly touch per-game timing.
- `GameSummary.duration_seconds()` calls `_duration_seconds(...)`.
- `_duration_seconds(...)` returns blank when either endpoint is blank or when
  either endpoint cannot be parsed by `datetime.fromisoformat(...)`.
- `_duration_seconds(...)` returns
  `max(int((finished - started).total_seconds()), 0)` when both endpoints
  parse, so out-of-order endpoints clamp to `0`.
- `GameSummary.to_debug_dict(...)` includes `first_event_time`,
  `last_event_time`, and `duration_seconds`.
- `GameSummary.to_game_log_row(...)` serializes row `timestamp` as
  `game.last_event_time or match.last_event_time or match.first_event_time`.
- `GameSummary.to_game_log_row(...)` serializes `Game Duration` from
  `GameSummary.duration_seconds()`.
- Game-log sync schema includes `Game Duration` but does not include separate
  workbook columns for game first-event or last-event time.
- Match-log sync schema includes match-level `MGTA Start Time` and
  `MTGA End Time`, which remain Tier 1 match lifecycle fields.

Observed risks, not fixed by this issue:

- `_safe_iso(...)` can use runtime wall-clock time when parser event metadata
  lacks a valid timestamp. Ledger metadata must describe this as weak,
  degraded, review-required fallback evidence, not clean Arena observation
  time.
- A game's first and last observed parser events may be later than true Arena
  game start or earlier than true Arena game end when logs are truncated,
  summarized, rotated, partially parsed, or missing early/late entries.
- `Game Duration` can be `0` because endpoints are equal or out of order and
  clamped, not because Arena confirmed a zero-second game.
- Blank duration means unavailable or unparseable endpoints, not proof of
  zero duration.
- Game-log `timestamp` can fall back to match-level timing when game-level
  last-event time is absent.

## Scope Decision

Codex C should implement issue #147 as a Tier 3 `game_level_facts` metadata
slice in the existing evidence ledger.

Do not add a new output family. Do not add workbook columns, webhook fields,
runtime status fields, parser event classes, parser behavior paths, generated
data paths, analytics surfaces, or runtime field-evidence attachment.

Required Tier 3 seed fields to add:

- `game1_first_event_time`
- `game2_first_event_time`
- `game3_first_event_time`
- `game1_last_event_time`
- `game2_last_event_time`
- `game3_last_event_time`
- `game1_duration_seconds`
- `game2_duration_seconds`
- `game3_duration_seconds`

Required Tier 3 entries:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier3.game_timing.game1_first_event_time` | `game1_first_event_time` | `Game 1 First Observed Event Time` | `observed` or `derived` |
| `tier3.game_timing.game2_first_event_time` | `game2_first_event_time` | `Game 2 First Observed Event Time` | `observed` or `derived` |
| `tier3.game_timing.game3_first_event_time` | `game3_first_event_time` | `Game 3 First Observed Event Time` | `observed` or `derived` |
| `tier3.game_timing.game1_last_event_time` | `game1_last_event_time` | `Game 1 Last Observed Event Time` | `observed` or `derived` |
| `tier3.game_timing.game2_last_event_time` | `game2_last_event_time` | `Game 2 Last Observed Event Time` | `observed` or `derived` |
| `tier3.game_timing.game3_last_event_time` | `game3_last_event_time` | `Game 3 Last Observed Event Time` | `observed` or `derived` |
| `tier3.game_duration.game1_duration_seconds` | `game1_duration_seconds` | `Game Duration` | `derived` |
| `tier3.game_duration.game2_duration_seconds` | `game2_duration_seconds` | `Game Duration` | `derived` |
| `tier3.game_duration.game3_duration_seconds` | `game3_duration_seconds` | `Game Duration` | `derived` |

Required family metadata:

- Keep `game_level_facts.status` as `seeded_sample`.
- Add the nine fields above to `game_level_facts.seed_fields`.
- Remove broad future fields `game_timing` and `game_duration` once the
  granular entries are seeded.
- Preserve prior #134, #137, #139, #140, #143, and #145 Tier 3 seed fields and
  entries.
- Keep remaining future fields, at minimum:
  - `pre_postboard`
  - `sideboarding`
  - `deck_state`
- Add notes stating that issue #147 maps game timing and duration provenance
  without changing timestamp parsing, `_safe_iso(...)`, state touch behavior,
  model duration behavior, row serialization, diagnostics, replay, drift,
  analytics, or field-evidence attachment behavior.

## Required Timing And Duration Semantics

Each timing and duration entry must document these durable meanings:

- Game first-event time means the first nonblank timestamp recorded by
  `GameSummary.touch(...)` for that game slot.
- Game last-event time means the latest nonblank timestamp recorded by
  `GameSummary.touch(...)` for that game slot.
- These endpoints are parser observation boundaries, not Arena's authoritative
  internal start/end times.
- Game duration means `GameSummary.duration_seconds()`, currently
  `max(last_event_time - first_event_time, 0)` when both endpoints parse.
- Duration is derived only from parser-owned stored endpoints.
- Blank duration means missing, blank, or unparseable endpoints.
- Blank duration is unknown/unavailable, not a real zero-second game.
- Zero duration is reviewable because it may mean equal timestamps or
  out-of-order/clamped endpoints.
- Runtime wall-clock fallback from `_safe_iso(...)` is weak/degraded evidence.
  It must never be described as high-confidence Arena timestamp evidence.
- Timing must not be reconstructed from turn count, game result, action count,
  game object count, mulligans, opening hand, play/draw, match duration,
  workbook formulas, dashboards, diagnostics reports, replay manifests,
  analytics, or AI output.

## Source Evidence Priority

Game timing provenance should document these sources in order:

1. Parser event `EventMetadata.timestamp` derived from the first-line
   Player.log timestamp for GameState, ClientAction, or GameResult events
   assigned to the same normalized match id and game number.
2. Parser state/model endpoints:
   `MatchSummary.games[N].first_event_time` and
   `MatchSummary.games[N].last_event_time`.
3. Game-log row `timestamp` as the serialized downstream timestamp, noting
   its fallback order:
   `game.last_event_time or match.last_event_time or match.first_event_time`.
4. Router timestamp anomaly counters as review/degradation context only:
   `timestamp_missing` and `timestamp_parse_failure`.
5. `_safe_iso(...)` runtime-clock fallback as weak fallback context only.

Game duration provenance should document these sources in order:

1. `MatchSummary.games[N].duration_seconds()` / `GameSummary.duration_seconds()`.
2. The matching `gameN_first_event_time` ledger entry.
3. The matching `gameN_last_event_time` ledger entry.
4. `_duration_seconds(...)` clamp and parse behavior as model semantics.

The ledger must not use these as timing or duration evidence:

- turn count
- game result or winner fields
- play/draw or starting-player fields
- mulligan count, opening hand, or mulliganed-away fields
- action count, zone count, object count, annotation count, or GameState count
- match-level `MGTA Start Time` or `MTGA End Time` as substitutes for
  game-level endpoints
- workbook formulas, dashboard calculations, Apps Script behavior, webhook
  delivery, diagnostics summaries, golden replay manifests, analytics, or AI
  output

## Required Entry Shape

Each `tier3.game_timing.gameN_first_event_time` and
`tier3.game_timing.gameN_last_event_time` entry must use the existing ledger
entry schema.

Common timing entry values:

- `tier`: `3`
- `output_family`: `game_level_facts`
- `parser_owner`: `src/mythic_edge_parser/app/state.py`
- `model_surface`: `MatchSummary.games[N].first_event_time` or
  `MatchSummary.games[N].last_event_time`
- `downstream_surfaces`: include `GameLogRow`, `state_snapshots`, and
  `match_history`
- `parser_managed_truth`: `True`
- `coverage_status`: `seeded_sample`
- `fixture_refs`: empty list unless Codex C adds a sanitized fixture reference
  already present in the repo

Timing direct evidence should include path-only signal metadata for:

- `game_state.gameN.event_timestamp`
- `client_action.gameN.event_timestamp`
- `game_result.gameN.event_timestamp`
- `parser_state.match_summary.gameN_first_event_time`
- `parser_state.match_summary.gameN_last_event_time`

Timing fallback evidence should include path-only signal metadata for:

- `router.timestamp_missing`
- `router.timestamp_parse_failure`
- `extractor.safe_iso.runtime_clock_fallback`
- `ledger.tier3.game_results.gameN_game_number_dependency`

Each `tier3.game_duration.gameN_duration_seconds` entry must use the existing
ledger entry schema.

Common duration entry values:

- `tier`: `3`
- `output_family`: `game_level_facts`
- `parser_owner`: `src/mythic_edge_parser/app/models.py`
- `model_surface`: `MatchSummary.games[N].duration_seconds()`
- `downstream_surfaces`: include `GameLogRow`, `state_snapshots`, and
  `match_history`
- `parser_managed_truth`: `True`
- `coverage_status`: `seeded_sample`
- `fixture_refs`: empty list unless Codex C adds a sanitized fixture reference
  already present in the repo

Duration direct evidence should include path-only signal metadata for:

- `parser_state.match_summary.gameN_duration_seconds`
- `model.game_summary.gameN_duration_seconds`

Duration fallback evidence should include path-only signal metadata for:

- `ledger.tier3.game_timing.gameN_first_event_time_dependency`
- `ledger.tier3.game_timing.gameN_last_event_time_dependency`
- `model.duration_seconds.gameN_clamp_behavior`
- `router.timestamp_missing`
- `router.timestamp_parse_failure`

If the existing ledger style requires different signal IDs for consistency,
Codex C may use equivalent names, but the IDs must remain stable, granular,
and game-specific.

## Value Source, Confidence, And Finality

Value-source policy:

- `observed`: a valid parser event timestamp was assigned to the game slot.
- `derived`: parser state/model endpoints or duration were built from observed
  event timestamps.
- `unknown`: no valid game-slot timing endpoint is available.
- `conflict`: source timestamps contradict stored endpoints or create
  unexplained out-of-order timing.
- `inferred` must not be used for game timing or duration in issue #147.
- `legacy_enriched` must not be used unless a later contract explicitly
  authorizes a legacy enrichment path.

Confidence policy:

- `high`: valid Player.log event timestamp metadata supports the game slot and
  no timestamp anomaly or source conflict is known.
- `medium`: the value is available only through parser state/model surfaces or
  through context-resolved game assignment with no known conflict.
- `low`: `_safe_iso(...)` runtime-clock fallback, weak context, partial
  evidence, timestamp anomaly counters, out-of-order endpoints, or serialized
  row fallback contributed.
- `unknown`: no valid endpoint or duration can be established from parser-owned
  evidence.

Finality policy:

- `live`: the game is still in progress and last-event time/duration may
  increase.
- `provisional`: the game has partial timing evidence, weak fallback, or
  missing completion context.
- `final`: the game has ended and the stored endpoints/duration are the final
  parser-owned values available from observed evidence.
- `reconciled`: final match summary output has been reconciled without
  changing the parser-owned timing semantics.

Finality must not imply exact Arena internal duration. A final duration can
still be degraded when timestamps are missing, malformed, fallback-derived,
out of order, truncated, or otherwise incomplete.

## Invariant Checks

Each per-game first-event entry must include game-specific invariant IDs
equivalent to:

- `gameN_first_event_time_requires_game_slot_identity`
- `gameN_first_event_time_is_first_observed_parser_event_for_slot`
- `gameN_first_event_time_not_arena_internal_start_time`
- `gameN_first_event_time_runtime_clock_fallback_degraded`
- `gameN_first_event_time_not_inferred_from_results_or_turn_count`

Each per-game last-event entry must include game-specific invariant IDs
equivalent to:

- `gameN_last_event_time_requires_game_slot_identity`
- `gameN_last_event_time_is_latest_observed_parser_event_for_slot`
- `gameN_last_event_time_not_arena_internal_end_time`
- `gameN_last_event_time_row_timestamp_fallback_is_reviewable`
- `gameN_last_event_time_not_inferred_from_results_or_turn_count`

Each per-game duration entry must include game-specific invariant IDs
equivalent to:

- `gameN_duration_requires_first_and_last_event_times`
- `gameN_duration_seconds_uses_model_duration_seconds`
- `gameN_duration_blank_is_unknown_not_zero`
- `gameN_duration_zero_is_reviewable_clamped_or_equal_endpoint`
- `gameN_duration_not_arena_clock_rope_or_clock_pressure`
- `gameN_duration_not_reconstructed_from_turn_count_results_actions_or_ai`

If Codex C names them with `game1`, `game2`, and `game3` rather than `gameN`,
the tests must assert the concrete IDs.

## Degradation Behavior

Each timing entry must describe how the ledger reports:

- missing event metadata timestamp
- invalid Player.log timestamp parse
- missing first-line timestamp
- `_safe_iso(...)` runtime-clock fallback
- missing game-slot identity
- weak context game-number assignment
- partial GameState, ClientAction, or GameResult evidence
- truncation, summarization, rotation, or data loss near timing evidence
- conflicting timestamps for the same game slot
- game-log row timestamp falling back to match-level timing
- unplayed game slots

Each duration entry must describe how the ledger reports:

- blank first endpoint
- blank last endpoint
- invalid ISO endpoint strings
- equal endpoints
- out-of-order endpoints clamped to zero
- missing or degraded timing dependencies
- data-loss/truncation evidence
- unplayed game slots

Required outcomes:

- Missing, invalid, or fallback timing evidence yields unknown or degraded
  provenance.
- Runtime-clock fallback is always degraded/review-required and must not be
  high confidence.
- Blank duration means unknown/unavailable, not zero.
- Zero duration is reviewable and may indicate equal timestamps or clamped
  out-of-order endpoints.
- Conflicting timing evidence must carry `conflicting_evidence` unless the
  stored first/last endpoint behavior explains it.
- Truncation/data-loss evidence must lower confidence and must not cause
  reconstruction.
- Unplayed slots remain blank/unknown and must not be treated as zero-duration
  games.

## Privacy And Serialization Rules

Timing and duration ledger metadata may include path-only evidence identifiers
and schema-level descriptions. It must not embed raw Player.log lines, raw
GameState payloads, raw ClientAction payloads, local diagnostics artifacts,
failed posts, workbook exports, secrets, webhook URLs, generated data, or
runtime status files.

Allowed evidence privacy class remains `path_only_no_values`.

The contract does not authorize field-evidence runtime attachment. If a later
issue adds runtime field-evidence records, it must follow the existing
`FIELD_EVIDENCE_SCHEMA_VERSION` contract and must still avoid raw private log
content.

## Public Interfaces

Codex C may update only documentation-adjacent evidence-ledger metadata and
focused tests unless the implementation comparison discovers that a metadata
test cannot be satisfied without a contract loopback.

Allowed implementation surfaces:

- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`
- `docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md`

Read-only comparison surfaces:

- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `tests/test_router_unit.py`
- `tests/test_app_models.py`
- `tests/test_state.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_parser_regressions.py`

Behavior changes are out of scope for issue #147.

## Validation Obligations

Codex C must add or update focused evidence-ledger tests that prove:

- all six `tier3.game_timing.gameN_*_event_time` entries exist
- all three `tier3.game_duration.gameN_duration_seconds` entries exist
- the entries validate with `validate_ledger_entry(...)`
- the Tier 3 family includes the nine timing/duration fields in `seed_fields`
- broad future fields `game_timing` and `game_duration` are removed from
  `future_fields`
- remaining deferred fields still include `pre_postboard`, `sideboarding`, and
  `deck_state`
- prior #139, #140, #143, and #145 entries remain present and unchanged in
  scope
- timing direct evidence documents event timestamps and parser state/model
  endpoints
- timing fallback evidence documents router timestamp anomalies, `_safe_iso`
  runtime-clock fallback, and game-slot dependency
- duration direct evidence documents `GameSummary.duration_seconds()`
- duration fallback evidence documents first/last endpoint dependencies and
  clamp behavior
- value-source policy distinguishes observed, derived, unknown, and conflict
  while excluding inferred timing/duration truth
- confidence policy marks runtime-clock fallback, missing/invalid timestamps,
  weak context, out-of-order endpoints, and row fallback as degraded or
  reviewable
- invariant checks document observation-boundary semantics, blank-versus-zero
  behavior, zero-duration review, and no reconstruction from turn count,
  results, action volume, analytics, or AI
- privacy remains path-only and no raw log excerpts are introduced

Recommended validation commands for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_app_models.py tests/test_state.py tests/test_router_unit.py
python3 -m ruff check src tests tools
```

If the local environment uses `py`, Codex C may use the equivalent `py -m`
commands after verifying the active workflow.

## Protected Surfaces And Stop Conditions

Do not implement behavior changes in Codex B.

Codex C must stop and route back to Codex B or Codex A if satisfying this
contract appears to require:

- parser behavior changes
- timestamp parsing changes
- `_safe_iso(...)` behavior changes
- `GameSummary.touch(...)` or `MatchSummary.touch_game(...)` changes
- `duration_seconds()` behavior changes
- parser state final reconciliation changes
- parser event class changes
- workbook schema changes
- webhook payload shape changes
- Apps Script changes
- output transport changes
- match/game identity changes
- deduplication changes
- environment variable or secret changes
- raw log, generated data, runtime status file, failed-post, or workbook-export
  changes
- runtime field-evidence attachment
- diagnostics, replay, drift, schema snapshot, invariant execution, or
  feature-equity report changes
- reconstructing missing game start/end, skipped phases, hidden actions, or
  facts absent from Player.log evidence
- moving parser-owned truth into workbook formulas, dashboard logic, Apps
  Script, webhook delivery, diagnostics reports, golden replay manifests,
  analytics, or AI output

Do not target `main` directly. Issue #147 work belongs on a branch based on
`codex/parser-reliability-intelligence`.

Do not close issue #11.

## Acceptance Criteria

Issue #147 is implementation-ready when:

- this contract exists at
  `docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md`
- Codex C can implement by editing only evidence-ledger metadata, focused
  evidence-ledger tests, and the implementation handoff
- the contract preserves prior evidence-ledger schema/vocabulary and prior
  Tier 3 slices
- the contract explicitly defines timing as parser observation-boundary data
- the contract explicitly defines duration as model-derived seconds from
  first/last game endpoints
- the contract explicitly distinguishes blank duration from zero duration
- the contract explicitly marks runtime-clock fallback as degraded
- the contract explicitly rejects reconstruction from missing evidence
- validation obligations and stop conditions are clear

## Pasteable Codex C Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #147, Tier 3 timing and duration provenance under tracker #11.

  Context:
  - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
  - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/147
  - Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/145
  - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/146
  - Previous merge commit: 0aede4890710768c7abd2fb2a561c7ce8b10fdba
  - Base branch: codex/parser-reliability-intelligence
  - Contract: docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md
  - Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md

  Goal:
  Implement the evidence-ledger metadata and focused tests for Tier 3 game timing and duration provenance. Keep the implementation metadata-only and preserve existing parser behavior.

  Read first:
  - AGENTS.md
  - docs/agent_rules.yml
  - docs/agent_constitution.md
  - docs/codex_module_workflow.md
  - docs/agent_threads/implementation.md
  - docs/contracts/player_log_evidence_ledger_schema.md
  - docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md
  - docs/contracts/player_log_evidence_ledger_tier3_turn_count.md
  - src/mythic_edge_parser/app/evidence_ledger.py
  - tests/test_evidence_ledger.py
  - src/mythic_edge_parser/router.py
  - src/mythic_edge_parser/events.py
  - src/mythic_edge_parser/app/extractors.py
  - src/mythic_edge_parser/app/state.py
  - src/mythic_edge_parser/app/models.py
  - src/mythic_edge_parser/app/sheet_schema.py

  Do:
  - Create a branch from codex/parser-reliability-intelligence, not main.
  - Compare current evidence-ledger metadata and tests against the contract before editing.
  - Add game1/game2/game3 first-event-time, last-event-time, and duration-seconds fields to Tier 3 seed fields.
  - Add entries under tier3.game_timing.* and tier3.game_duration.* exactly as contracted or with equivalent stable game-specific IDs.
  - Remove broad future fields game_timing and game_duration after the granular entries are seeded.
  - Preserve prior Tier 3 game-result, play/draw, mulligan, opening-hand, and turn-count entries.
  - Add focused tests for entry shape, source evidence, fallback evidence, value-source policy, confidence/finality policy, blank-versus-zero behavior, zero-duration review, runtime-clock fallback degradation, observation-boundary semantics, and protected downstream boundaries.
  - Produce docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md with comparison, files changed, validation, open risks, and next recommended role.

  Do not:
  - Change parser behavior, timestamp parsing, _safe_iso behavior, GameSummary.touch behavior, MatchSummary.touch_game behavior, duration_seconds behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, diagnostics, replay, drift, schema snapshot, invariant execution, feature-equity reports, runtime field-evidence attachment, or analytics truth.
  - Reconstruct missing game start/end, skipped phases, hidden actions, or facts the Player.log did not provide.
  - Move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, diagnostics reports, golden replay manifests, analytics, or AI output.
  - Target main directly.
  - Close issue #11.
  - Stage or commit unless explicitly asked.

  Validation:
  - python3 -m pytest -q tests/test_evidence_ledger.py
  - python3 -m pytest -q tests/test_app_models.py tests/test_state.py tests/test_router_unit.py
  - python3 -m ruff check src tests tools

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/147"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md"
  verdict: "timing_duration_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  recommended_implementation_branch: "codex/player-log-evidence-ledger-tier3-timing-duration"
  validation:
    - "Contract writer pass only; no parser behavior validation run."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, timestamp parsing, _safe_iso behavior, GameSummary.touch behavior, MatchSummary.touch_game behavior, duration_seconds behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, diagnostics, replay, drift, schema snapshot, invariant execution, feature-equity reports, runtime field-evidence attachment, or analytics truth."
    - "Do not reconstruct missing game start/end, skipped phases, hidden actions, or facts the Player.log did not provide."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, diagnostics reports, golden replay manifests, analytics, or AI output."
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/147"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_timing_duration_comparison.md"
  verdict: "timing_duration_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  recommended_implementation_branch: "codex/player-log-evidence-ledger-tier3-timing-duration"
  validation:
    - "Documentation-only contract checks are sufficient for Codex B."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, timestamp parsing, _safe_iso behavior, GameSummary.touch behavior, MatchSummary.touch_game behavior, duration_seconds behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, diagnostics, replay, drift, schema snapshot, invariant execution, feature-equity reports, runtime field-evidence attachment, or analytics truth."
    - "Do not reconstruct missing game start/end, skipped phases, hidden actions, or facts the Player.log did not provide."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, diagnostics reports, golden replay manifests, analytics, or AI output."
```
