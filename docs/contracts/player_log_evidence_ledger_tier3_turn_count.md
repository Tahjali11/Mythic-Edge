# Player.log Evidence Ledger Tier 3 Turn-Count Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/145
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/143
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/144
- previous_merge_commit: af6d5f554720b159975e8fecfcf008298fd8ca76
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier3-turn-count
- target_artifact: docs/contracts/player_log_evidence_ledger_tier3_turn_count.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md
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
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/parser_gre_turn_info.md
- docs/contracts/parser_gre_game_state.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- docs/decisions/ADR-0003-player-log-drift-policy.md

## Purpose

Issue #145 maps Tier 3 turn-count provenance in the Player.log evidence ledger.

Turn count is a parser-owned game-level fact derived from observed GRE
GameState turn-number evidence, parser extraction, parser state updates, and
`GameSummary.turn_count`. The durable meaning is "maximum observed valid turn
number for this game slot," not reconstructed total turns.

This contract documents provenance metadata only. It must not change parser
behavior, turn-count update behavior, GameState parsing, turn-info
normalization, parser state final reconciliation, parser event classes,
workbook schema, webhook payload shape, Apps Script behavior, output
transport, match/game identity, deduplication, generated data, or analytics
truth.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, validators, vocabulary constants, privacy posture, and
the allowed `value_source`, `confidence`, `finality`, invariant, and drift
vocabularies.

`docs/contracts/player_log_evidence_ledger_tier3_game_results.md` remains
authoritative for game number, per-game winners, and per-game result
provenance. Turn-count entries depend on the correct game slot but must not
infer turn counts from winners, result scope, or match completion.

`docs/contracts/player_log_evidence_ledger_participant_player_team.md` remains
authoritative for participant and player-team provenance. Turn count does not
depend on local player-team identity.

`docs/contracts/player_log_evidence_ledger_tier3_play_draw.md`,
`docs/contracts/player_log_evidence_ledger_tier3_mulligans.md`, and
`docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md` are sibling
Tier 3 slices. Issue #145 must preserve their seed fields, entries, notes, and
tests.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #145 provenance should be
recorded through this contract, implementation handoff, entry notes, and
focused tests rather than by changing the top-level ledger object shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- GRE turn-info parsing owns the normalized turn-number value exposed from
  `gameStateMessage.turnInfo.turnNumber`.
- GRE GameState parsing owns propagation of that normalized value into
  `payload.turn_number`, `payload.turn_info.turn_number`, and
  `payload.identity.turn_number`.
- `src/mythic_edge_parser/app/extractors.py` owns current turn-info extraction
  priority across identity, turn-info payload, top-level payload, and context.
- `src/mythic_edge_parser/app/state.py` owns applying GameState turn-number
  evidence to the current `MatchSummary` game slot.
- `src/mythic_edge_parser/app/models.py` owns `GameSummary.turn_count`,
  `GameSummary.set_turn_count(...)`, `MatchSummary.set_game_turn_count(...)`,
  and row serialization for `G1 Turn Count`, `G2 Turn Count`,
  `G3 Turn Count`, and game-log `Turn Count`.
- `src/mythic_edge_parser/app/evidence_ledger.py` describes provenance,
  confidence, finality, degradation, drift, and review expectations.
- Workbook rows, Apps Script, webhook transport, dashboards, diagnostics,
  golden replay, feature-equity reports, drift reports, timing analytics,
  clock-pressure analytics, gameplay advice, and AI output are downstream
  consumers only.

The ledger must not reconstruct missing turns, skipped phases, hidden actions,
or facts that the Player.log did not provide. It must not infer turn count from
game duration, action volume, phase labels, result timing, mulligans,
opening-hand size, play/draw, winner, or AI/analytics output.

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` at
`af6d5f554720b159975e8fecfcf008298fd8ca76`:

- The Tier 3 `game_level_facts` family is already `seeded_sample` for game
  number, per-game winners, per-game results, starting-player, play/draw,
  mulligan, opening-hand size, exact opening hand, and mulliganed-away
  provenance.
- The same family still lists broad future field `turn_count`.
- `build_turn_info(...)` returns `{}` when `turnInfo` is missing or not a
  dictionary.
- `build_turn_info(...)` normalizes `turnInfo.turnNumber` through `int(...)`
  and returns `None` on `TypeError` or `ValueError`.
- Integer-like strings such as `" 3 "` currently normalize to `3`.
- Non-integral strings such as `"1.5"` currently normalize to `None`.
- Existing tests lock current integer-normalization behavior where booleans
  and floats can pass through `int(...)` on selected fields.
- Existing tests show negative turn-number strings can normalize to negative
  integers in the GameState payload.
- `build_game_state_payload(...)` exposes the normalized turn number at
  top-level `turn_number`, `turn_info.turn_number`, and
  `identity.turn_number`.
- Queued GameState messages are represented with payload type
  `queued_game_state_message` and may supply fallback GameState evidence when
  the current message is partial.
- `_extract_turn_info(...)` hydrates game-state identity and reads turn number
  from `identity.turn_number`, `turn_info.turn_number`,
  `turn_info.turnNumber`, or top-level `payload.turn_number`.
- `state.py` handles `GameState` events by extracting match id, game number,
  and turn number, touching the game slot, and calling
  `summary.set_game_turn_count(game_number, turn_number)`.
- `GameSummary.turn_count` defaults to `0`.
- `GameSummary.set_turn_count(...)` attempts integer normalization and stores
  the value only when it is greater than the current `turn_count`.
- Current model behavior therefore stores the maximum observed integer turn
  number and ignores missing, malformed, lower, equal, zero, or negative
  values when the current count is the default `0`.
- `GameSummary.has_summary_data()` treats `turn_count > 0` as summary data.
- Game-log row `Turn Count` serializes `turn_count` when nonzero, otherwise
  blank.
- Match-log row `G1 Turn Count`, `G2 Turn Count`, and `G3 Turn Count`
  serialize each game slot turn count when nonzero, otherwise blank.

Observed risks, not fixed by this issue:

- Parser normalization currently allows some values that should not be
  described as clean high-confidence turn-count evidence, including booleans,
  floats coerced by `int(...)`, and negative integers.
- The display layer uses blank for unobserved/no positive turn count; the
  ledger must not describe blank as a real zero-turn game.
- A later observed higher turn number replaces an earlier count, so the output
  is max-observed turn number, not a complete turn timeline.
- Missing or partial GameState evidence can produce unknown turn count even
  when other game facts are known.
- Truncation, data loss, or queued-message fallback can make turn count
  degraded without making the game result, mulligan, opening-hand, or play/draw
  entries invalid.

## Scope Decision

Codex C should implement issue #145 as a Tier 3 `game_level_facts` metadata
slice in the existing evidence ledger.

Do not add a new output family. Do not add a workbook column, webhook field,
runtime status field, parser event class, parser behavior path, generated data
path, analytics surface, or runtime field-evidence attachment.

Required Tier 3 seed fields to add:

- `game1_turn_count`
- `game2_turn_count`
- `game3_turn_count`

Required Tier 3 entries:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier3.turn_count.game1_turn_count` | `game1_turn_count` | `G1 Turn Count` | `observed` or `derived` |
| `tier3.turn_count.game2_turn_count` | `game2_turn_count` | `G2 Turn Count` | `observed` or `derived` |
| `tier3.turn_count.game3_turn_count` | `game3_turn_count` | `G3 Turn Count` | `observed` or `derived` |

Required family metadata:

- Keep `game_level_facts.status` as `seeded_sample`.
- Add the three fields above to `game_level_facts.seed_fields`.
- Remove broad `turn_count` from `game_level_facts.future_fields` once the
  granular entries are seeded.
- Preserve prior #134, #137, #139, #140, and #143 Tier 3 seed fields and
  entries.
- Keep remaining future fields, at minimum:
  - `game_timing`
  - `game_duration`
  - `pre_postboard`
  - `sideboarding`
  - `deck_state`
- Add notes stating that issue #145 maps turn-count provenance without
  changing turn-info parsing, GameState parsing, parser state, row
  serialization, diagnostics, replay, drift, timing analytics, or
  field-evidence attachment behavior.

## Required Turn-Count Semantics

Each turn-count entry must document the following durable meaning:

- The value is the maximum observed valid positive turn number for that game
  slot.
- The value is not a reconstructed number of turns that must have occurred.
- The value is not a count of actions, decisions, priority passes, phases,
  steps, timers, elapsed duration, logs lines, or GameState messages.
- A clean positive integer from GameState turn-info evidence may support a
  high-confidence observed or derived value.
- Integer-like string evidence may support a value only when the parser
  normalized it deterministically and the source path is otherwise valid.
- `0` is not a valid turn-count fact. It represents no observed positive turn
  count in current model state and serializes as blank.
- Blank output means unknown/unobserved/unplayed/no positive count available,
  not a real zero-turn game.
- Negative values are invalid turn-count facts. Current payload normalization
  may expose them, but current model update behavior must not promote them
  above the default count. Ledger entries must treat negative evidence as
  degraded/review-required if encountered.
- Boolean-like values are not clean turn-count evidence, even if current
  `int(...)` normalization could coerce them. Ledger entries must mark that
  path degraded/review-required rather than high confidence.
- Non-integral strings, malformed objects, missing `turnInfo`, missing
  `turnNumber`, partial GameState messages, and truncation/data-loss evidence
  must produce unknown or degraded provenance, not invented counts.

## Source Evidence Priority

Turn-count provenance should document these sources in order:

1. Current GameState `gameStateMessage.turnInfo.turnNumber` evidence for the
   same normalized match id and game number.
2. Queued GameState `gameStateMessage.turnInfo.turnNumber` fallback evidence
   when current GameState payload is partial and the queued payload supplies
   the usable turn info.
3. Normalized parser payload surfaces:
   `payload.turn_info.turn_number`, `payload.identity.turn_number`, and
   `payload.turn_number`.
4. Extractor output from `_extract_turn_info(...)` after game-slot hydration.
5. Parser state/model output in `MatchSummary.games[N].turn_count`.

The ledger may cite parser state/model output as direct evidence for the
serialized row field, but it should still document the upstream GameState
turn-number paths that support the model value.

The ledger must not use these as turn-count evidence:

- match result or winner fields
- play/draw or starting-player fields
- mulligan count, opening hand, or mulliganed-away fields
- game duration or timing fields
- action count, zone count, object count, or annotation count
- workbook formulas, dashboard calculations, Apps Script behavior, webhook
  delivery, diagnostics summaries, golden replay manifests, analytics, or AI
  output

## Required Entry Shape

Each `tier3.turn_count.gameN_turn_count` entry must use the existing ledger
entry schema.

Common required values:

- `tier`: `3`
- `output_family`: `game_level_facts`
- `parser_owner`: `src/mythic_edge_parser/app/state.py`
- `model_surface`: `MatchSummary.games[N].turn_count`
- `downstream_surfaces`: include `MatchLogRow`, `GameLogRow`, and
  `match_history`
- `parser_managed_truth`: `True`
- `coverage_status`: `seeded_sample`
- `fixture_refs`: empty list unless Codex C adds a sanitized fixture reference
  already present in the repo

Per-game expected values:

| Game | Output field | Display aliases | Model surface |
| --- | --- | --- | --- |
| 1 | `game1_turn_count` | `G1 Turn Count`, game-log `Turn Count` when `Game Number == 1` | `MatchSummary.games[1].turn_count` |
| 2 | `game2_turn_count` | `G2 Turn Count`, game-log `Turn Count` when `Game Number == 2` | `MatchSummary.games[2].turn_count` |
| 3 | `game3_turn_count` | `G3 Turn Count`, game-log `Turn Count` when `Game Number == 3` | `MatchSummary.games[3].turn_count` |

Direct evidence should include path-only signal metadata for:

- `game_state.gameN.turn_info_turn_number`
- `game_state.gameN.identity_turn_number`
- `game_state.gameN.payload_turn_number`
- `extractor.gameN.turn_number`
- `parser_state.match_summary.gameN_turn_count`

Fallback evidence should include path-only signal metadata for:

- `queued_game_state.gameN.turn_info_turn_number`
- `ledger.tier3.game_results.gameN_game_number_dependency`
- `ledger.tier3.turn_count.gameN_turn_count_prior_observation`

If the existing ledger style requires different signal IDs for consistency,
Codex C may use equivalent names, but the IDs must remain stable, granular,
and game-specific.

## Value Source, Confidence, And Finality

Value-source policy:

- `observed`: a valid positive turn number came directly from GameState
  turn-info evidence for the same game slot.
- `derived`: the row field comes from parser state/model max-observed state
  built from observed GameState turn-info evidence.
- `unknown`: no valid positive turn-number evidence is available for the game
  slot.
- `conflict`: multiple source paths disagree in a way that cannot be explained
  by max-observed progression or queued fallback.
- `inferred` must not be used for turn count in issue #145.
- `legacy_enriched` must not be used unless a later contract explicitly
  authorizes a legacy enrichment path.

Confidence policy:

- `high`: current or queued GameState turn-info evidence provides a valid
  positive integer for the same game slot and parser state reflects the
  max-observed value.
- `medium`: the value is present only through normalized parser/model surfaces
  or integer-like string normalization, with no contradictory evidence.
- `low`: the value requires weak fallback, queued-message fallback with partial
  current payload, or source-path ambiguity.
- `unknown`: no valid positive turn-number evidence exists.

Finality policy:

- `live`: the game is still in progress and the maximum observed turn number
  may increase.
- `provisional`: the game slot has partial evidence, fallback evidence, or
  missing completion context.
- `final`: the game has ended and the max-observed turn count is the final
  parser-owned value available from observed evidence.
- `reconciled`: final match summary output has been reconciled without changing
  the parser-owned max-observed value.

Finality must not imply that missing turns were reconstructed. A final value
can still be degraded if truncation, data loss, malformed input, or source
conflict affected the evidence.

## Invariant Checks

Each per-game entry must include game-specific invariant IDs equivalent to:

- `gameN_turn_count_requires_game_slot_identity`
- `gameN_turn_count_uses_max_observed_positive_turn_number`
- `gameN_turn_count_blank_output_is_not_zero`
- `gameN_turn_count_zero_is_unknown_not_valid`
- `gameN_turn_count_negative_or_boolean_evidence_degraded`
- `gameN_turn_count_not_reconstructed_from_duration_or_actions`
- `gameN_turn_count_not_inferred_from_results_play_draw_mulligans_or_opening_hand`
- `gameN_turn_count_queued_fallback_is_reviewable`

If Codex C names them with `game1`, `game2`, and `game3` rather than `gameN`,
the tests must assert the concrete IDs.

## Degradation Behavior

Each per-game entry must describe how the ledger reports:

- missing `turnInfo`
- missing `turnNumber`
- malformed `turnNumber`
- non-integral strings
- object/list values
- booleans coerced by current parser normalization
- floats truncated by current parser normalization
- negative values
- zero values
- partial GameState payloads
- queued-message fallback
- conflicting current versus queued values
- lower later observations after a higher value was already stored
- truncation/data-loss markers near GameState evidence
- unplayed game slots

Required outcomes:

- Missing or malformed evidence yields `unknown` or degraded provenance.
- Valid positive max-observed evidence yields observed/derived provenance.
- Queued fallback is allowed but must be reviewable and should carry
  `fallback_used` or `weak_fallback_used` when appropriate.
- Conflicting evidence that cannot be explained by max-observed progression
  must carry `conflicting_evidence`.
- Truncation/data-loss evidence must carry a drift/degradation note and must
  not cause reconstruction.
- Unplayed slots remain blank/unknown and must not be treated as zero-turn
  games.

## Privacy And Serialization Rules

Turn-count ledger metadata may include path-only evidence identifiers and
schema-level descriptions. It must not embed raw Player.log lines, raw
GameState payloads, raw local diagnostics artifacts, failed posts, workbook
exports, secrets, webhook URLs, or generated data.

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
- `docs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md`

Read-only comparison surfaces:

- `src/mythic_edge_parser/parsers/gre/turn_info.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `tests/test_gre_turn_info_parser.py`
- `tests/test_gre_game_state_parser.py`
- `tests/test_app_extractors.py`
- `tests/test_state.py`
- `tests/test_app_models.py`
- `tests/test_match_summary_from_match_state.py`

Behavior changes are out of scope for issue #145.

## Validation Obligations

Codex C must add or update focused evidence-ledger tests that prove:

- all three `tier3.turn_count.gameN_turn_count` entries exist
- the entries validate with `validate_ledger_entry(...)`
- the Tier 3 family includes `game1_turn_count`, `game2_turn_count`, and
  `game3_turn_count` in `seed_fields`
- broad future field `turn_count` is removed from `future_fields`
- remaining deferred fields still include `game_timing`, `game_duration`,
  `pre_postboard`, `sideboarding`, and `deck_state`
- prior #139, #140, and #143 entries remain present and unchanged in scope
- direct evidence documents GameState turn-info, normalized payload, extractor,
  and parser state/model surfaces
- fallback evidence documents queued GameState fallback and game-slot
  dependency
- value-source policy distinguishes observed, derived, unknown, and conflict
  while excluding inferred turn-count truth
- confidence policy marks boolean, float, negative, zero, malformed, missing,
  and fallback paths as degraded or reviewable
- invariant checks document max-observed semantics, blank-versus-zero behavior,
  and no reconstruction from duration/actions/results/play-draw/mulligans or
  opening hand
- privacy remains path-only and no raw log excerpts are introduced

Recommended validation commands for Codex C:

```bash
py -m pytest -q tests/test_evidence_ledger.py
py -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_app_extractors.py tests/test_state.py tests/test_app_models.py
py -m ruff check src tests
```

If the environment does not provide `py`, use the repository-standard Python
invocation documented by the active workflow after verifying it locally.

## Protected Surfaces And Stop Conditions

Do not implement behavior changes in Codex B.

Codex C must stop and route back to Codex B or Codex A if satisfying this
contract appears to require:

- parser behavior changes
- turn-count update behavior changes
- GameState parsing changes
- turn-info normalization changes
- extractor behavior changes
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
- reconstructing missing turns, skipped phases, hidden actions, or facts absent
  from Player.log evidence
- moving parser-owned truth into workbook formulas, dashboard logic, Apps
  Script, webhook delivery, diagnostics reports, golden replay manifests,
  analytics, or AI output

Do not target `main` directly. Issue #145 work belongs on a branch based on
`codex/parser-reliability-intelligence`.

Do not close issue #11.

## Acceptance Criteria

Issue #145 is implementation-ready when:

- this contract exists at
  `docs/contracts/player_log_evidence_ledger_tier3_turn_count.md`
- Codex C can implement by editing only evidence-ledger metadata, focused
  evidence-ledger tests, and the implementation handoff
- the contract preserves prior evidence-ledger schema/vocabulary and prior
  Tier 3 slices
- the contract explicitly defines turn count as max observed valid positive
  turn number
- the contract explicitly distinguishes blank from zero
- the contract explicitly rejects reconstruction from missing evidence
- validation obligations and stop conditions are clear

## Pasteable Codex C Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #145, Tier 3 turn-count provenance under tracker #11.

  Context:
  - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
  - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/145
  - Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/143
  - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/144
  - Previous merge commit: af6d5f554720b159975e8fecfcf008298fd8ca76
  - Base branch: codex/parser-reliability-intelligence
  - Contract: docs/contracts/player_log_evidence_ledger_tier3_turn_count.md
  - Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md

  Goal:
  Implement the evidence-ledger metadata and focused tests for Tier 3 turn-count provenance. Keep the implementation metadata-only and preserve existing parser behavior.

  Read first:
  - AGENTS.md
  - docs/agent_rules.yml
  - docs/agent_constitution.md
  - docs/codex_module_workflow.md
  - docs/agent_threads/implementation.md
  - docs/contracts/player_log_evidence_ledger_schema.md
  - docs/contracts/player_log_evidence_ledger_tier3_turn_count.md
  - docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md
  - src/mythic_edge_parser/app/evidence_ledger.py
  - tests/test_evidence_ledger.py
  - src/mythic_edge_parser/parsers/gre/turn_info.py
  - src/mythic_edge_parser/parsers/gre/game_state.py
  - src/mythic_edge_parser/app/extractors.py
  - src/mythic_edge_parser/app/state.py
  - src/mythic_edge_parser/app/models.py

  Do:
  - Create a branch from codex/parser-reliability-intelligence, not main.
  - Compare current evidence-ledger metadata and tests against the contract before editing.
  - Add game1_turn_count, game2_turn_count, and game3_turn_count to the Tier 3 seed fields.
  - Add entries tier3.turn_count.game1_turn_count, tier3.turn_count.game2_turn_count, and tier3.turn_count.game3_turn_count.
  - Remove broad future field turn_count after the granular entries are seeded.
  - Preserve prior Tier 3 game-result, play/draw, mulligan, and opening-hand entries.
  - Add focused tests for entry shape, source evidence, fallback evidence, value-source policy, confidence/finality policy, blank-versus-zero behavior, max-observed semantics, degradation behavior, and protected downstream boundaries.
  - Produce docs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md with comparison, files changed, validation, open risks, and next recommended role.

  Do not:
  - Change parser behavior, turn-count update behavior, GameState parsing, turn-info normalization, extractor behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or analytics truth.
  - Reconstruct missing turns, skipped phases, hidden actions, or facts the Player.log did not provide.
  - Move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, diagnostics reports, golden replay manifests, analytics, or AI output.
  - Target main directly.
  - Close issue #11.
  - Stage or commit unless explicitly asked.

  Validation:
  - py -m pytest -q tests/test_evidence_ledger.py
  - py -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_app_extractors.py tests/test_state.py tests/test_app_models.py
  - py -m ruff check src tests

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/145"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_turn_count.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md"
  verdict: "turn_count_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  recommended_implementation_branch: "codex/player-log-evidence-ledger-tier3-turn-count"
  validation:
    - "Contract writer pass only; no parser behavior validation run."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, turn-count update behavior, GameState parsing, turn-info normalization, extractor behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or analytics truth."
    - "Do not reconstruct missing turns, skipped phases, hidden actions, or facts the Player.log did not provide."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, diagnostics reports, golden replay manifests, analytics, or AI output."
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/145"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_turn_count.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_turn_count_comparison.md"
  verdict: "turn_count_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  recommended_implementation_branch: "codex/player-log-evidence-ledger-tier3-turn-count"
  validation:
    - "Documentation-only contract checks are sufficient for Codex B."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, turn-count update behavior, GameState parsing, turn-info normalization, extractor behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or analytics truth."
    - "Do not reconstruct missing turns, skipped phases, hidden actions, or facts the Player.log did not provide."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, diagnostics reports, golden replay manifests, analytics, or AI output."
```
