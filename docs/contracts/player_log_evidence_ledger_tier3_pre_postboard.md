# Player.log Evidence Ledger Tier 3 Pre/Postboard Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/149
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/147
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/148
- previous_merge_commit: 14c69c47a953387b0a4151aeff4b46a17aadae64
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier3-pre-postboard
- target_artifact: docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier3_pre_postboard_comparison.md
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
- docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- docs/decisions/ADR-0003-player-log-drift-policy.md

## Purpose

Issue #149 maps Tier 3 pre/postboard provenance in the Player.log evidence
ledger.

`Pre / Postboard` is a parser/model-owned game-log label derived from game
slot identity:

- game 1 serializes as `Preboard`
- game 2 and game 3 serialize as `Postboard`

This label is not direct proof that sideboarding happened. It is not submitted
deck evidence, deck-state evidence, card-change evidence, or strategy advice.
It must not be reconstructed from match format, queue type, sideboarding flags,
submit-deck flags, workbook formulas, dashboards, analytics, or AI output.

This contract documents provenance metadata only. It must not change parser
behavior, game-number assignment, `GameSummary.to_game_log_row(...)`,
sideboarding behavior, deck-state behavior, parser state final reconciliation,
parser event classes, workbook schema, webhook payload shape, Apps Script
behavior, output transport, match/game identity, deduplication, generated data,
runtime artifacts, or analytics truth.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, validators, vocabulary constants, privacy posture, and
the allowed `value_source`, `confidence`, `finality`, invariant, and drift
vocabularies.

`docs/contracts/player_log_evidence_ledger_tier3_game_results.md` remains
authoritative for `game_number` and game-slot identity. Pre/postboard entries
derive from that game slot. Issue #149 must not redefine game-number
extraction, context fallback, or game identity.

`docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md`,
`docs/contracts/player_log_evidence_ledger_tier3_turn_count.md`,
`docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md`,
`docs/contracts/player_log_evidence_ledger_tier3_mulligans.md`, and
`docs/contracts/player_log_evidence_ledger_tier3_play_draw.md` are sibling
Tier 3 slices. Issue #149 must preserve their seed fields, entries, notes, and
tests.

Tier 4 `sideboarding_and_deck_state` remains registered for future
sideboarding and submitted-deck provenance. Issue #149 does not implement or
rename that family.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #149 provenance should be
recorded through this contract, implementation handoff, entry notes, and
focused tests rather than by changing the top-level ledger object shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- `src/mythic_edge_parser/app/models.py` owns `GameSummary.game_number` and
  `GameSummary.to_game_log_row(...)` serialization for `Pre / Postboard`.
- `src/mythic_edge_parser/app/models.py` owns the fixed game slots exposed by
  `GAME_NUMBERS = (1, 2, 3)` and `_default_games()`.
- `src/mythic_edge_parser/app/state.py` owns when parser events assign or
  update current match/game context and touch `MatchSummary` game slots.
- `src/mythic_edge_parser/app/extractors.py` owns game-number extraction from
  GameState and GameResult payloads.
- `src/mythic_edge_parser/app/evidence_ledger.py` describes provenance,
  confidence, finality, degradation, drift, and review expectations.
- Workbook rows, Apps Script, webhook transport, dashboards, diagnostics,
  golden replay, feature-equity reports, drift reports, sideboarding analytics,
  deck-state analytics, gameplay advice, and AI output are downstream
  consumers only.

The ledger describes support for a parser-owned game-slot label. It does not
compute sideboarding, prove deck changes, infer sideboard use, infer deck-state
truth, or promote analytics interpretation into parser truth.

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` at
`14c69c47a953387b0a4151aeff4b46a17aadae64`:

- The Tier 3 `game_level_facts` family is already `seeded_sample` for game
  number, per-game winners, per-game results, starting-player, play/draw,
  mulligan, opening-hand, mulliganed-away, turn-count, timing, and duration
  provenance.
- The same family still lists broad future field `pre_postboard`.
- `GameSummary` stores `game_number`.
- `MatchSummary` initializes fixed `GameSummary` slots for games 1, 2, and 3.
- `MatchSummary.game(...)` accepts integer-like game numbers and returns a
  fixed game slot when the normalized number is 1, 2, or 3.
- `GameSummary.to_game_log_row(...)` serializes `Game Number` from
  `self.game_number`.
- `GameSummary.to_game_log_row(...)` serializes `Pre / Postboard` as
  `"Preboard" if self.game_number == 1 else "Postboard"`.
- Therefore, any non-1 `GameSummary.game_number` that reaches
  `to_game_log_row(...)` would serialize as `Postboard`, although the normal
  fixed game slots are 1, 2, and 3.
- `MatchSummary.to_game_sheet_rows()` emits rows only for game slots where
  `GameSummary.has_summary_data()` is true.
- `GameSummary.has_summary_data()` can become true from winner, starting
  player, mulligan count greater than zero, opening-hand data,
  mulliganed-away data, first-event time, or positive turn count.
- GameState events can set current game number and touch a game slot when
  extracted game identity or context provides a game number.
- ClientAction events can touch the current game slot from parser context.
- GameResult events can set current game number and touch a game slot from
  extracted result identity.
- MatchState `match_started` sets current game number to `1`, but MatchState
  does not directly emit per-game rows by itself.
- `MTGA Sideboard Entered` and `MTGA Submit Deck Seen` are match-log fields
  derived from separate `MatchSummary.sideboarding_entered` and
  `MatchSummary.submit_deck_seen` booleans.
- `GameSummary.to_game_log_row(...)` does not inspect
  `sideboarding_entered`, `submit_deck_seen`, submitted-deck contents, queue
  type, match format, game result, turn count, timing, or duration to populate
  `Pre / Postboard`.
- Game-log sync schema already includes `Pre / Postboard`.

Observed risks, not fixed by this issue:

- `Postboard` can look like proof that the player sideboarded, but current
  behavior only proves game slot 2 or 3.
- `Preboard` / `Postboard` can look like deck-state evidence, but it is not
  submitted-deck or card-change evidence.
- A context-derived or weakly established game number can produce a label even
  when direct game-number evidence is degraded.
- Unplayed game slots should not create standalone pre/postboard evidence.
- The literal workbook-facing spelling `Pre / Postboard`, `Preboard`, and
  `Postboard` is existing behavior and must not be changed by this issue.

## Scope Decision

Codex C should implement issue #149 as a Tier 3 `game_level_facts` metadata
slice in the existing evidence ledger.

Do not add a new output family. Do not add workbook columns, webhook fields,
runtime status fields, parser event classes, parser behavior paths, generated
data paths, analytics surfaces, or runtime field-evidence attachment.

Required Tier 3 seed fields to add:

- `game1_pre_postboard`
- `game2_pre_postboard`
- `game3_pre_postboard`

Required Tier 3 entries:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier3.pre_postboard.game1_pre_postboard` | `game1_pre_postboard` | `Pre / Postboard` | `derived` |
| `tier3.pre_postboard.game2_pre_postboard` | `game2_pre_postboard` | `Pre / Postboard` | `derived` |
| `tier3.pre_postboard.game3_pre_postboard` | `game3_pre_postboard` | `Pre / Postboard` | `derived` |

Required family metadata:

- Keep `game_level_facts.status` as `seeded_sample`.
- Add the three fields above to `game_level_facts.seed_fields`.
- Remove broad future field `pre_postboard` once the granular entries are
  seeded.
- Preserve prior #134, #137, #139, #140, #143, #145, and #147 Tier 3 seed
  fields and entries.
- Keep remaining future fields, at minimum:
  - `sideboarding`
  - `deck_state`
- Keep Tier 4 `sideboarding_and_deck_state` registered for future work.
- Add notes stating that issue #149 maps pre/postboard provenance without
  changing game-number assignment, `GameSummary.to_game_log_row(...)`,
  sideboarding behavior, submitted-deck behavior, deck-state behavior,
  diagnostics, replay, drift, analytics, or field-evidence attachment
  behavior.

## Required Pre/Postboard Semantics

Each pre/postboard entry must document these durable meanings:

- `Pre / Postboard` is derived from `GameSummary.game_number`.
- Game 1 maps to `Preboard`.
- Game 2 maps to `Postboard`.
- Game 3 maps to `Postboard`.
- `Postboard` means game slot 2 or 3. It is not direct evidence that
  sideboarding happened.
- `Preboard` means game slot 1. It is not proof that no sideboarding-capable
  match context exists.
- The value is not observed directly from a Player.log sideboarding event.
- The value is not submitted-deck evidence.
- The value is not proof that deck contents changed.
- The value is not proof of Best-of-Three format by itself.
- The value must not be inferred from queue type, match format, sideboarding
  flags, submit-deck flags, game result, turn count, timing, duration, opening
  hand, mulligans, workbook formulas, dashboards, analytics, or AI output.
- Missing, invalid, context-only, or degraded game-number evidence must
  degrade pre/postboard provenance rather than invent stronger sideboarding or
  deck-state claims.
- Unplayed game slots must not create standalone pre/postboard ledger truth.

## Source Evidence Priority

Pre/postboard provenance should document these sources in order:

1. `MatchSummary.games[N].game_number` / `GameSummary.game_number` for the
   fixed game slot.
2. `GameSummary.to_game_log_row(...).["Pre / Postboard"]` serialization for
   the game-log row.
3. The corresponding `tier3.game_results.game_number` ledger entry as the
   upstream game-slot dependency.
4. GameState, GameResult, and parser context game-number extraction only as
   upstream evidence for game-slot identity, not as separate sideboarding
   evidence.
5. `GameSummary.has_summary_data()` as row-emission context only.

The ledger must not use these as pre/postboard evidence:

- `MatchSummary.sideboarding_entered`
- `MatchSummary.submit_deck_seen`
- `ClientMessageType_EnterSideboardingReq`
- `ClientMessageType_SubmitDeckResp`
- submitted deck contents, mainboard cards, or sideboard cards
- queue type, match format, event id, or match win condition
- play/draw, mulligans, opening hand, turn count, timing, duration, result, or
  winner fields
- workbook formulas, dashboard calculations, Apps Script behavior, webhook
  delivery, diagnostics summaries, golden replay manifests, analytics, or AI
  output

## Required Entry Shape

Each `tier3.pre_postboard.gameN_pre_postboard` entry must use the existing
ledger entry schema.

Common required values:

- `tier`: `3`
- `output_family`: `game_level_facts`
- `parser_owner`: `src/mythic_edge_parser/app/models.py`
- `model_surface`: `GameSummary.to_game_log_row()["Pre / Postboard"]`
- `downstream_surfaces`: include `GameLogRow`, `match_history`, and
  `state_snapshots`
- `parser_managed_truth`: `True`
- `coverage_status`: `seeded_sample`
- `fixture_refs`: empty list unless Codex C adds a sanitized fixture reference
  already present in the repo

Per-game expected values:

| Game | Output field | Display alias | Expected label | Model source |
| --- | --- | --- | --- | --- |
| 1 | `game1_pre_postboard` | `Pre / Postboard` | `Preboard` | `MatchSummary.games[1].game_number` |
| 2 | `game2_pre_postboard` | `Pre / Postboard` | `Postboard` | `MatchSummary.games[2].game_number` |
| 3 | `game3_pre_postboard` | `Pre / Postboard` | `Postboard` | `MatchSummary.games[3].game_number` |

Direct evidence should include path-only signal metadata for:

- `parser_state.match_summary.gameN_game_number`
- `model.game_summary.gameN_pre_postboard_label`
- `game_log_row.gameN_pre_postboard`

Fallback evidence should include path-only signal metadata for:

- `ledger.tier3.game_results.gameN_game_number_dependency`
- `parser_context.current_game_number`
- `game_summary.gameN_has_summary_data`

Forbidden or negative evidence notes should explicitly mention:

- `match_summary.sideboarding_entered_not_pre_postboard_evidence`
- `match_summary.submit_deck_seen_not_pre_postboard_evidence`
- `submitted_deck_contents_not_pre_postboard_evidence`

If the existing ledger style requires different signal IDs for consistency,
Codex C may use equivalent names, but the IDs must remain stable, granular,
and game-specific.

## Value Source, Confidence, And Finality

Value-source policy:

- `derived`: the value is derived from game slot identity and model
  serialization.
- `unknown`: no valid game slot exists or no row is emitted for an unplayed
  slot.
- `conflict`: game-slot evidence conflicts or the row label disagrees with the
  expected slot mapping.
- `observed` must not be used for the pre/postboard label itself because the
  label is not directly observed from a Player.log sideboarding event.
- `inferred` must not be used for pre/postboard in issue #149.
- `legacy_enriched` must not be used unless a later contract explicitly
  authorizes a legacy enrichment path.

Confidence policy:

- `high`: a valid fixed game slot exists and row serialization matches the
  contract mapping: game 1 `Preboard`, game 2/3 `Postboard`.
- `medium`: the value depends on normalized parser/model game slot state with
  no known conflict, but direct upstream game-number evidence is not present
  in the current entry.
- `low`: context fallback, weak game-number assignment, row-emission
  ambiguity, or missing/partial upstream evidence contributed.
- `unknown`: no valid game slot or emitted row exists.

Finality policy:

- `live`: the game slot has live summary data and the game-log row can still
  change for other fields, while the slot-based label remains deterministic.
- `provisional`: game-slot identity came from weak context or partial evidence.
- `final`: the game row is final and the slot-derived label is stable.
- `reconciled`: final match summary output has been reconciled without
  changing the slot-derived pre/postboard semantics.

Finality must not imply observed sideboarding. A final `Postboard` label can
still have no sideboarding or submitted-deck evidence.

## Invariant Checks

Each per-game pre/postboard entry must include game-specific invariant IDs
equivalent to:

- `gameN_pre_postboard_requires_game_slot_identity`
- `gameN_pre_postboard_derived_from_game_number`
- `gameN_pre_postboard_game1_preboard_game2_game3_postboard`
- `gameN_pre_postboard_postboard_not_sideboarding_proof`
- `gameN_pre_postboard_not_submitted_deck_or_deck_state_evidence`
- `gameN_pre_postboard_not_inferred_from_format_queue_results_turn_count_timing_or_ai`
- `gameN_pre_postboard_unplayed_slot_unknown_not_standalone_truth`

If Codex C names them with `game1`, `game2`, and `game3` rather than `gameN`,
the tests must assert the concrete IDs.

## Degradation Behavior

Each per-game entry must describe how the ledger reports:

- missing game-number evidence
- invalid game-number evidence
- context-only game-number fallback
- conflicting game-number evidence
- missing row emission because the game slot has no summary data
- row label that disagrees with the expected game-slot mapping
- `Postboard` appearing without sideboarding-entered evidence
- `Postboard` appearing without submit-deck evidence
- Best-of-One or unknown-format matches with only game 1 played
- truncated, summarized, rotated, or partial logs near game-slot evidence

Required outcomes:

- Missing or invalid game slot yields `unknown` or degraded provenance.
- Context-only game-number fallback is reviewable.
- Unplayed slots remain blank/unknown and must not be treated as real
  `Preboard` or `Postboard` rows.
- `Postboard` without sideboarding-entered or submit-deck evidence remains a
  valid slot-derived label, but it is not sideboarding/deck-state proof.
- Sideboarding and deck-state questions remain future ledger work.
- Truncation/data-loss evidence must lower confidence and must not cause
  reconstruction.

## Privacy And Serialization Rules

Pre/postboard ledger metadata may include path-only evidence identifiers and
schema-level descriptions. It must not embed raw Player.log lines, raw
GameState payloads, raw ClientAction payloads, submitted deck contents, local
diagnostics artifacts, failed posts, workbook exports, secrets, webhook URLs,
generated data, or runtime status files.

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
- `docs/implementation_handoffs/player_log_evidence_ledger_tier3_pre_postboard_comparison.md`

Read-only comparison surfaces:

- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `tests/test_app_models.py`
- `tests/test_state.py`
- `tests/test_sheet_schema.py`

Behavior changes are out of scope for issue #149.

## Validation Obligations

Codex C must add or update focused evidence-ledger tests that prove:

- all three `tier3.pre_postboard.gameN_pre_postboard` entries exist
- the entries validate with `validate_ledger_entry(...)`
- the Tier 3 family includes `game1_pre_postboard`,
  `game2_pre_postboard`, and `game3_pre_postboard` in `seed_fields`
- broad future field `pre_postboard` is removed from `future_fields`
- remaining deferred fields still include `sideboarding` and `deck_state`
- prior #139, #140, #143, #145, and #147 entries remain present and unchanged
  in scope
- direct evidence documents game-slot model state and game-log row
  serialization
- fallback evidence documents game-number dependency, parser context fallback,
  and row-emission context
- value-source policy uses `derived`, `unknown`, and `conflict` and excludes
  observed/inferred/legacy-enriched pre/postboard truth
- confidence policy marks weak game-number context and unplayed slots as
  degraded or unknown
- invariant checks document game 1 `Preboard`, games 2/3 `Postboard`, and the
  no-sideboarding-proof boundary
- degradation behavior documents that `Postboard` is not sideboarding proof and
  not submitted-deck/deck-state evidence
- privacy remains path-only and no raw logs, submitted deck contents, or local
  artifacts are introduced

Recommended validation commands for Codex C:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_app_models.py tests/test_state.py tests/test_sheet_schema.py
python3 -m ruff check src tests tools
```

If the local environment uses `py`, Codex C may use the equivalent `py -m`
commands after verifying the active workflow.

## Protected Surfaces And Stop Conditions

Do not implement behavior changes in Codex B.

Codex C must stop and route back to Codex B or Codex A if satisfying this
contract appears to require:

- parser behavior changes
- game-number assignment changes
- `GameSummary.to_game_log_row(...)` changes
- literal value changes for `Pre / Postboard`, `Preboard`, or `Postboard`
- sideboarding behavior changes
- submitted-deck behavior changes
- deck-state behavior changes
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
- reconstructing missing sideboarding, submitted-deck, deck-state, game-slot,
  hidden-card, or match-format facts absent from Player.log evidence
- moving parser-owned truth into workbook formulas, dashboard logic, Apps
  Script, webhook delivery, diagnostics reports, golden replay manifests,
  analytics, or AI output

Do not target `main` directly. Issue #149 work belongs on a branch based on
`codex/parser-reliability-intelligence`.

Do not close issue #11.

## Acceptance Criteria

Issue #149 is implementation-ready when:

- this contract exists at
  `docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md`
- Codex C can implement by editing only evidence-ledger metadata, focused
  evidence-ledger tests, and the implementation handoff
- the contract preserves prior evidence-ledger schema/vocabulary and prior
  Tier 3 slices
- the contract explicitly defines pre/postboard as a game-slot-derived label
- the contract explicitly maps game 1 to `Preboard` and games 2/3 to
  `Postboard`
- the contract explicitly states that `Postboard` is not sideboarding,
  submitted-deck, or deck-state proof
- the contract explicitly rejects reconstruction from missing evidence
- validation obligations and stop conditions are clear

## Pasteable Codex C Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #149, Tier 3 pre/postboard provenance under tracker #11.

  Context:
  - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
  - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/149
  - Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/147
  - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/148
  - Previous merge commit: 14c69c47a953387b0a4151aeff4b46a17aadae64
  - Base branch: codex/parser-reliability-intelligence
  - Contract: docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md
  - Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier3_pre_postboard_comparison.md

  Goal:
  Implement the evidence-ledger metadata and focused tests for Tier 3 pre/postboard provenance. Keep the implementation metadata-only and preserve existing parser behavior.

  Read first:
  - AGENTS.md
  - docs/agent_rules.yml
  - docs/agent_constitution.md
  - docs/codex_module_workflow.md
  - docs/agent_threads/implementation.md
  - docs/contracts/player_log_evidence_ledger_schema.md
  - docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md
  - docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md
  - docs/contracts/player_log_evidence_ledger_tier3_game_results.md
  - src/mythic_edge_parser/app/evidence_ledger.py
  - tests/test_evidence_ledger.py
  - src/mythic_edge_parser/app/models.py
  - src/mythic_edge_parser/app/state.py
  - src/mythic_edge_parser/app/extractors.py
  - src/mythic_edge_parser/app/sheet_schema.py

  Do:
  - Create a branch from codex/parser-reliability-intelligence, not main.
  - Compare current evidence-ledger metadata and tests against the contract before editing.
  - Add game1_pre_postboard, game2_pre_postboard, and game3_pre_postboard to Tier 3 seed fields.
  - Add entries tier3.pre_postboard.game1_pre_postboard, tier3.pre_postboard.game2_pre_postboard, and tier3.pre_postboard.game3_pre_postboard.
  - Remove broad future field pre_postboard after the granular entries are seeded.
  - Preserve prior Tier 3 game-result, play/draw, mulligan, opening-hand, turn-count, timing, and duration entries.
  - Keep sideboarding and deck_state deferred.
  - Add focused tests for entry shape, source evidence, fallback evidence, value-source policy, confidence/finality policy, game-slot label mapping, unplayed-slot behavior, no-sideboarding-proof boundary, no-submitted-deck/deck-state boundary, and protected downstream boundaries.
  - Produce docs/implementation_handoffs/player_log_evidence_ledger_tier3_pre_postboard_comparison.md with comparison, files changed, validation, open risks, and next recommended role.

  Do not:
  - Change parser behavior, game-number assignment, GameSummary.to_game_log_row behavior, literal Pre / Postboard values, sideboarding behavior, submitted-deck behavior, deck-state behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, diagnostics, replay, drift, schema snapshot, invariant execution, feature-equity reports, runtime field-evidence attachment, or analytics truth.
  - Reconstruct missing sideboarding, submitted-deck, deck-state, game-slot, hidden-card, or match-format facts the Player.log did not provide.
  - Move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, diagnostics reports, golden replay manifests, analytics, or AI output.
  - Target main directly.
  - Close issue #11.
  - Stage or commit unless explicitly asked.

  Validation:
  - python3 -m pytest -q tests/test_evidence_ledger.py
  - python3 -m pytest -q tests/test_app_models.py tests/test_state.py tests/test_sheet_schema.py
  - python3 -m ruff check src tests tools

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/149"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_pre_postboard_comparison.md"
  verdict: "pre_postboard_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  recommended_implementation_branch: "codex/player-log-evidence-ledger-tier3-pre-postboard"
  validation:
    - "Contract writer pass only; no parser behavior validation run."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, game-number assignment, GameSummary.to_game_log_row behavior, literal Pre / Postboard values, sideboarding behavior, submitted-deck behavior, deck-state behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, diagnostics, replay, drift, schema snapshot, invariant execution, feature-equity reports, runtime field-evidence attachment, or analytics truth."
    - "Do not reconstruct missing sideboarding, submitted-deck, deck-state, game-slot, hidden-card, or match-format facts the Player.log did not provide."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, diagnostics reports, golden replay manifests, analytics, or AI output."
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/149"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier3_pre_postboard_comparison.md"
  verdict: "pre_postboard_provenance_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  recommended_implementation_branch: "codex/player-log-evidence-ledger-tier3-pre-postboard"
  validation:
    - "Documentation-only contract checks are sufficient for Codex B."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, game-number assignment, GameSummary.to_game_log_row behavior, literal Pre / Postboard values, sideboarding behavior, submitted-deck behavior, deck-state behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, diagnostics, replay, drift, schema snapshot, invariant execution, feature-equity reports, runtime field-evidence attachment, or analytics truth."
    - "Do not reconstruct missing sideboarding, submitted-deck, deck-state, game-slot, hidden-card, or match-format facts the Player.log did not provide."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, diagnostics reports, golden replay manifests, analytics, or AI output."
```
