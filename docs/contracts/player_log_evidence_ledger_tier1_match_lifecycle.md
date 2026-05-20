# Player.log Evidence Ledger Tier 1 Match Lifecycle Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/130
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/128
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/129
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier1-match-lifecycle
- target_artifact: docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier1_match_lifecycle_comparison.md
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
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- docs/decisions/ADR-0003-player-log-drift-policy.md

## Purpose

Issue #128 created the machine-readable Player.log evidence ledger schema,
vocabulary constants, validators, output-family registry, and one Tier 1 seed
entry for `match_id`.

Issue #130 expands that registry across the highest-value Tier 1 match lifecycle
fields. The goal is provenance metadata: for each emitted match lifecycle
output, the ledger must say which parser-owned evidence supports it, how strong
that evidence is, what fallback means, and when a missing or degraded source
requires review.

This contract does not change parser behavior. It documents the current parser
truth surfaces so future diagnostics, drift reports, and field-evidence
attachment can reason about match lifecycle outputs without becoming a second
parser.

## Relationship To Issue #128 And The Broad Issue #11 Contract

`docs/contracts/player_log_evidence_ledger_schema.md` remains the schema and
vocabulary contract for:

- `VALUE_SOURCES`
- `CONFIDENCE_LEVELS`
- `FINALITY_LABELS`
- `INVARIANT_STATUSES`
- `DRIFT_FLAGS`
- ledger entry shape
- evidence signal shape
- field-evidence shape
- privacy validation

Issue #130 must preserve the #128 schema and vocabulary unless implementation
finds a direct impossibility. If implementation needs a new vocabulary label or
entry field, it must stop and route back to Codex B instead of silently changing
the schema.

The broad #11 contract still owns the long-term ledger map. This issue covers a
narrower Tier 1 slice only. It does not implement runtime field-evidence
attachment, drift report execution, schema snapshots, invariant execution, or
Tier 2-7 mapping.

The top-level `source_issue` in `evidence_ledger.py` may remain issue #128 as
the schema origin. Issue #130 provenance should be recorded through the new
contract, implementation handoff, and entry notes rather than by changing the
top-level ledger object shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- MTGA `Player.log` is local observable evidence, not absolute game truth.
- Parser events, extractors, parser state, and `MatchSummary` own match
  lifecycle interpretation.
- The evidence ledger documents source priority, fallback, confidence,
  finality, degradation, and review expectations for parser-owned outputs.
- The evidence ledger must not compute match facts, infer missing GameState
  data, reconcile winners, post webhooks, update workbooks, or decide merge,
  deploy, drift, analytics, or AI truth.
- Workbook rows, Apps Script, webhook transport, dashboards, diagnostics,
  golden replay, drift reports, and AI output are consumers or reporting
  surfaces.

## Observed Current Behavior

Observed from `codex/parser-reliability-intelligence` after PR #129:

- `src/mythic_edge_parser/app/evidence_ledger.py` exists.
- `tests/test_evidence_ledger.py` validates vocabulary constants, ledger shape,
  output-family registration, one `match_id` entry, copy safety,
  serialization, privacy, duplicate detection, and field-evidence review rules.
- The Tier 1 output family is `match_identity_and_lifecycle`.
- The only complete Tier 1 entry is `tier1.match_identity.match_id`.
- `src/mythic_edge_parser/app/models.py` owns `MatchSummary` fields and
  workbook-facing row construction.
- `src/mythic_edge_parser/app/state.py` owns parser-state updates, live/final
  row readiness, GameResult match-winner precedence, and posted-row snapshots.
- `src/mythic_edge_parser/app/sheet_schema.py` owns the current match-log sync
  field tuple, including the legacy workbook spelling `MGTA Start Time`.

Current parser model surfaces:

- `MatchSummary.match_id`
- `MatchSummary.first_event_time`
- `MatchSummary.last_event_time`
- `MatchSummary.player_team`
- `MatchSummary.match_winner_team`
- `MatchSummary.match_result_type`
- `MatchSummary.match_result_reason`
- `MatchSummary.match_wl`
- `MatchSummary.is_ready()`
- `MatchSummary.to_match_log_row(final=...)`
- `state.build_live_match_log_row(...)`
- `state.build_match_log_update(...)`

## Scope Decision

Codex C should expand the Tier 1 ledger from the #128 `match_id` seed to these
contracted entries:

| Entry ID | Parser field | Workbook-facing alias | Status |
| --- | --- | --- | --- |
| `tier1.match_identity.match_id` | `match_id` | `MTGA Match ID` | preserve #128 anchor |
| `tier1.match_lifecycle.match_started_at` | `first_event_time` / `match_started_at` | `MGTA Start Time` | add in #130 |
| `tier1.match_lifecycle.match_finished_at` | `last_event_time` / `match_finished_at` | `MTGA End Time` | add in #130 |
| `tier1.match_result.match_winner_team` | `match_winner_team` | none direct | add in #130 |
| `tier1.match_result.match_result` | `match_wl` / `match_result` | `Match Win?` | add in #130 |
| `tier1.match_lifecycle.match_sync_status` | match-row finality decision | `MTGA Sync Status` | add in #130 |

Codex C should defer these derived aggregate fields to a later Tier 1
game-aggregate provenance issue:

- `Games Won`
- `Games Lost`
- `Total Games`
- `Match Win Flag`
- `Game Win %`

Reasoning:

- The #130 lifecycle slice should map match identity, start/end time, winner,
  win/loss result, and live/final sync state.
- The aggregate fields depend on game-level winners, player team, and derived
  math. They are important, but they cross into game-level provenance and should
  be contracted with game-result evidence instead of squeezed into this pass.
- `Match Win Flag` is derived from `match_result`, but it should stay with the
  aggregate/derived field pass so the implementation does not partially map a
  math family while skipping the adjacent totals.

The Tier 1 output-family registry should move the six contracted fields into
`seed_fields` or otherwise mark them as fully mapped using existing #128 schema
vocabulary. Do not add new family statuses in this issue.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier1_match_lifecycle_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier1_match_lifecycle.md

Referenced but not owned:

- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/parsers/match_state.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- src/mythic_edge_parser/parsers/gre/game_result.py
- tests/test_state.py
- tests/test_gre_game_result_parser.py

Out of scope:

- parser behavior changes
- parser state final reconciliation changes
- parser event class changes
- workbook schema changes
- webhook payload changes
- Apps Script changes
- output transport changes
- match/game identity changes
- deduplication changes
- runtime field-evidence attachment
- drift report implementation
- schema snapshot implementation
- invariant execution
- diagnostics, replay, or feature-equity report-shape changes
- raw private Player.log excerpts
- generated data, runtime status files, failed posts, or workbook exports
- AI/model-provider behavior or AI truth

## Public Interface

Recommended implementation surface:

```python
src/mythic_edge_parser/app/evidence_ledger.py
```

Public constants and functions from #128 must remain stable:

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

No new runtime parser API is required for issue #130.

Required ledger-entry behavior:

- `iter_ledger_entries()` must return deep-copy-safe entries.
- `build_player_log_evidence_ledger()` must remain deterministic and JSON
  serializable.
- Each new entry must pass `validate_ledger_entry(...)`.
- The built ledger must pass `validate_player_log_evidence_ledger(...)`.
- Entry and signal IDs must remain stable, lowercase, dot-separated identifiers.
- Source paths must remain repo-relative or symbolic.
- Raw payload values, raw private log excerpts, absolute local paths, secrets,
  webhook URLs, and runtime artifacts must not be embedded.

## Inputs

The ledger describes these source categories; it does not consume live events at
runtime in this issue.

### Parser Event Evidence

`MatchState` events:

- source module: `src/mythic_edge_parser/parsers/match_state.py`
- relevant normalized paths:
  - `payload.match_id`
  - `payload.type`
  - `payload.players[]`
  - `payload.game_results[].scope`
  - `payload.game_results[].winning_team_id`
  - `payload.game_results[].result`
  - `payload.game_results[].reason`
- relevant raw path examples:
  - `matchGameRoomStateChangedEvent.gameRoomInfo.gameRoomConfig.matchId`
  - `matchGameRoomStateChangedEvent.gameRoomInfo.results[]`

`GameState` events:

- source module: `src/mythic_edge_parser/parsers/gre/game_state.py`
- relevant normalized paths:
  - `payload.identity.match_id`
  - `payload.game_info.matchID`
  - `payload.turn_info`
  - player/team fields consumed by parser state
- relevant raw path examples:
  - `greToClientMessages[].gameStateMessage.gameInfo.matchID`

`GameResult` events:

- source module: `src/mythic_edge_parser/parsers/gre/game_result.py`
- relevant normalized paths:
  - `payload.identity.match_id`
  - `payload.game_info.matchID`
  - `payload.results[].scope`
  - `payload.results[].winning_team_id`
  - `payload.results[].result`
  - `payload.results[].reason`
  - `payload.match_state`
  - `payload.winning_team_id`
  - `payload.result_type`
  - `payload.reason`
- relevant raw path examples:
  - `greToClientMessages[].gameStateMessage.gameInfo.matchID`
  - `greToClientMessages[].gameStateMessage.results[]`

Parser event metadata:

- relevant symbolic paths:
  - `metadata.timestamp`
  - `log_entry.timestamp`

### Parser State And Model Evidence

`MatchSummary` state:

- `match_id`
- `first_event_time`
- `last_event_time`
- `player_team`
- `match_winner_team`
- `match_result_type`
- `match_result_reason`
- `match_wl`
- `is_ready()`

State-builder decisions:

- `build_live_match_log_row(...)` emits a live row when a summary exists with
  a match ID.
- `build_match_log_update(...)` derives `final=True` from summary readiness.
- `MatchSummary.to_match_log_row(final=False)` emits `MTGA Sync Status` as
  `Live` and leaves `MTGA End Time` blank.
- `MatchSummary.to_match_log_row(final=True)` emits `MTGA Sync Status` as
  `Final` and uses `last_event_time` for `MTGA End Time`.

## Outputs

The output is a richer code-owned evidence-ledger registry. It remains local
metadata until a future contract adds runtime field-evidence attachment.

Required output-family updates:

- Tier 1 family `match_identity_and_lifecycle` must include the six contracted
  fields as mapped seed fields or equivalent fully mapped entries.
- Deferred aggregate fields may remain in `future_fields` or notes, but they
  must not be represented as fully mapped entries in #130.

Required new entries:

### `tier1.match_identity.match_id`

Preserve the #128 anchor entry.

Required behavior:

- Keep `output_family` as `match_identity_and_lifecycle`.
- Keep `output_field` as `match_id`.
- Keep `display_name` as `MTGA Match ID`.
- Preserve direct evidence from `MatchState`, `GameState`, and `GameResult`.
- Preserve parser-context fallback as derived, medium-confidence,
  provisional evidence.
- Update notes only if needed to say this entry is the #128 anchor preserved by
  #130.

### `tier1.match_lifecycle.match_started_at`

Field meaning:

- Parser field: `MatchSummary.first_event_time`
- Conceptual field: `match_started_at`
- Workbook-facing alias: `MGTA Start Time`

Required evidence policy:

- Preferred evidence: the timestamp metadata on the first trusted match-start
  event for the summary, especially `MatchState` with
  `payload.type == "match_started"`.
- Fallback evidence: `MatchSummary.first_event_time` derived from the first
  trusted parser event that touches the match summary.
- Value source:
  - `observed` when using event metadata from an explicit match-start event.
  - `derived` when using first-summary-touch fallback.
  - `unknown` when no timestamp is available.
- Confidence:
  - `high` for explicit match-start metadata.
  - `medium` for first-summary-touch fallback.
  - `unknown` when missing.
- Finality:
  - `live` while the match is active.
  - `final` when included in a final row without later correction.
  - `reconciled` only if a future field-evidence attachment layer records a
    later stronger correction.
- Missing behavior:
  - Leave the value blank.
  - Mark future field evidence as `unknown` confidence and review-worthy.
  - Do not infer a start timestamp from wall-clock runtime, workbook state, or
    file modification time.

Required signal examples:

- `match_state.match_started.timestamp`
- `parser_state.match_summary.first_event_time`

### `tier1.match_lifecycle.match_finished_at`

Field meaning:

- Parser field: `MatchSummary.last_event_time`
- Conceptual field: `match_finished_at`
- Workbook-facing alias: `MTGA End Time`

Required evidence policy:

- Preferred evidence: timestamp metadata on final result evidence, especially a
  `GameResult` or `MatchState` event that establishes match completion.
- Fallback evidence: `MatchSummary.last_event_time` from the latest trusted
  event that touched the summary at the time a final row is emitted.
- Value source:
  - `observed` when using final-result or match-completion event metadata.
  - `derived` when using latest-summary-touch fallback.
  - `unknown` when no timestamp is available.
- Confidence:
  - `high` for final-result or match-completion metadata.
  - `medium` for latest-summary-touch fallback.
  - `unknown` when missing.
- Finality:
  - `live` rows must leave `MTGA End Time` blank.
  - `final` applies only when the match row is final.
  - `reconciled` applies only to a later stronger correction recorded by future
    field-evidence tooling.
- Missing behavior:
  - A missing finish timestamp must leave the end-time field blank.
  - It must not block parser finalization by itself, because current readiness
    is based on `match_id`, `player_team`, and `match_winner_team`.
  - It must require review in future field-evidence output.

Required signal examples:

- `game_result.match_complete.timestamp`
- `match_state.match_complete.timestamp`
- `parser_state.match_summary.last_event_time`

### `tier1.match_result.match_winner_team`

Field meaning:

- Parser field: `MatchSummary.match_winner_team`
- Workbook-facing alias: none direct; it feeds `Match Win?`, `Match Win Flag`,
  match history, and debug/state surfaces.

Required precedence policy:

- Preferred evidence is the latest nested result whose scope normalizes to
  `MatchScope_Match` / `Match` and whose winner is known.
- `GameResult.results[]` match-scope winner takes precedence over top-level
  `payload.winning_team_id`.
- `MatchState.game_results[]` match-scope winner remains valid match-scope
  evidence.
- If no nested match-scope winner exists, state may fall back to top-level
  `GameResult.payload.winning_team_id` only when
  `payload.match_state == "MatchState_MatchComplete"` and the winner is known.
- Do not infer match winner from game wins, best-of structure, workbook values,
  dashboard formulas, or AI output in this issue.

Known-winner semantics:

- `None`, `""`, `0`, and `"0"` are unknown winner values.
- `0` is unknown, not a valid team winner, because current GRE payload building
  uses `0` as the default for missing winners.
- Non-zero winner values are valid even if they are not exactly `1` or `2`.
- Unknown winner values must not set or overwrite a previously known
  `match_winner_team`.

Required evidence policy:

- Value source:
  - `observed` for nested match-scope winner evidence.
  - `observed` with lower confidence for the top-level match-complete fallback.
  - `unknown` when no known winner exists.
  - `conflict` when future evidence attachment detects contradictory final
    winner sources.
- Confidence:
  - `high` for nested match-scope winner evidence.
  - `medium` for top-level `MatchState_MatchComplete` fallback.
  - `low` for conflicting evidence.
  - `unknown` when missing.
- Finality:
  - `final` when supported by final match-scope or match-complete evidence.
  - `provisional` only for incomplete or fallback-derived live evidence.
  - `reconciled` only if future field-evidence tooling records a later stronger
    correction.
- Missing behavior:
  - Keep match winner unknown.
  - Do not mark `Match Win?` high-confidence.
  - Keep final row readiness blocked by current parser-state readiness rules.

Required signal examples:

- `game_result.results.match_scope_winner`
- `match_state.game_results.match_scope_winner`
- `game_result.top_level_match_complete_winner`

### `tier1.match_result.match_result`

Field meaning:

- Parser field: `MatchSummary.match_wl`
- Conceptual field: `match_result`
- Workbook-facing alias: `Match Win?`

Required evidence policy:

- `match_result` is derived from `MatchSummary.match_winner_team` and
  `MatchSummary.player_team`.
- It is not directly observed in Player.log as `W` or `L`.
- It must inherit review and confidence constraints from both dependencies.
- Missing `player_team` must prevent high-confidence `Match Win?`.
- Missing or unknown `match_winner_team` must produce an unknown/blank result.
- A known winner without a known local player team is not enough to mark a
  player win/loss result.

Value source:

- `derived` when both dependencies are known.
- `unknown` when either dependency is missing.
- `conflict` when future field-evidence tooling detects contradictory
  participant or winner evidence.

Confidence:

- `high` only when `match_winner_team` is high-confidence and `player_team` is
  known from parser-owned participant/team evidence.
- `medium` when the winner was a medium-confidence fallback but player team is
  known.
- `unknown` when either dependency is missing.
- `low` when dependencies conflict.

Finality:

- `final` only when match winner is final and player team is known.
- `provisional` for live/incomplete rows.
- `reconciled` only if later stronger evidence changes the result.

Required signal examples:

- `parser_state.match_summary.match_wl`
- `parser_state.match_summary.match_winner_team_dependency`
- `parser_state.match_summary.player_team_dependency`

### `tier1.match_lifecycle.match_sync_status`

Field meaning:

- Parser field: the state/model row finality decision passed to
  `MatchSummary.to_match_log_row(final=...)`
- Workbook-facing alias: `MTGA Sync Status`

Required evidence policy:

- `match_sync_status` is parser-state derived, not directly observed in
  Player.log.
- Current `Final` status is based on `MatchSummary.is_ready()`, which requires:
  - `match_id`
  - known `player_team`
  - known `match_winner_team`
- Current `Live` status is emitted by live row construction when a summary with
  a match ID exists but final readiness has not been reached.
- The ledger may document this readiness rule, but must not change it.

Value source:

- `derived` for both `Live` and `Final`.
- `unknown` only if the status cannot be associated with a known summary.
- `conflict` only if future field-evidence tooling detects an impossible row
  state.

Confidence:

- `high` when the readiness rule is satisfied by known parser-state fields.
- `medium` for live/provisional rows that have match identity but incomplete
  final ingredients.
- `unknown` if the row cannot be tied to a match summary.

Finality:

- `live` for `Live`.
- `final` for `Final`.
- `reconciled` only if later field-evidence tooling records a corrected status.

Missing behavior:

- Missing match ID should prevent meaningful sync-status evidence.
- Missing winner or local team should keep match status live/provisional under
  current readiness rules.
- Do not let workbook row presence, Apps Script upsert state, webhook delivery,
  or dashboard display decide finality.

Required signal examples:

- `parser_state.match_summary_ready`
- `parser_state.live_match_log_row`
- `models.match_summary.to_match_log_row.final_argument`

## Invariants

- The #128 `match_id` entry must remain present and valid.
- All #130 entries must use existing #128 schema and vocabulary.
- All #130 entries must belong to Tier 1 and output family
  `match_identity_and_lifecycle`.
- `MGTA Start Time` must keep its current legacy workbook spelling.
- `MTGA End Time` must be documented as blank for live rows.
- `MTGA Sync Status` must be documented as parser-state derived, not raw-log
  observed.
- `Match Win?` must be documented as derived from winner plus local player team,
  not directly observed.
- Nested match-scope winner evidence must take precedence over top-level winner
  fallback.
- Top-level `winning_team_id` may be match-winner fallback only when
  `match_state == "MatchState_MatchComplete"` and no nested match-scope winner
  exists.
- Unknown winner values `None`, `""`, `0`, and `"0"` must remain unknown and
  must not overwrite a known winner.
- Game-level result aggregation must not be used to infer match winner in this
  issue.
- Derived aggregate fields must remain deferred from full #130 entry coverage.
- The ledger must not include raw private logs, raw payload values, absolute
  local paths, secrets, webhook URLs, generated data, runtime status files,
  failed posts, or workbook exports.

## Error Behavior

Malformed or missing ledger metadata:

- Validators must report errors rather than raising for ordinary malformed
  payloads.
- Duplicate entry IDs and duplicate signal IDs must be reported.
- Unknown vocabulary values must be reported.
- Absolute paths, raw log-like text, secret-like text, and webhook-like URLs
  must be reported by privacy validation.

Missing source evidence:

- Missing timestamp evidence yields unknown/blank timing fields and future
  review-required field evidence.
- Missing match winner keeps match result unknown and prevents high-confidence
  result evidence.
- Missing local player team keeps `Match Win?` unknown or degraded even when a
  match winner is known.
- Missing final readiness ingredients keeps sync status live/provisional under
  current parser-state behavior.

Contradictory source evidence:

- Future field-evidence attachment should use `conflict`, low confidence, and
  `conflicting_evidence`.
- Issue #130 implementation should only describe the conflict behavior in
  ledger entries; it must not implement runtime conflict resolution.

## Side Effects

This contract pass writes only:

- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md

Future Codex C implementation may change only:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier1_match_lifecycle_comparison.md

Future Codex C should not change parser behavior, runtime state mutation,
webhook posts, workbook sync, Apps Script, output transport, raw logs, generated
data, failed posts, runtime status files, or workbook exports.

## Dependency Order

Codex C should implement in this order:

1. Compare current `evidence_ledger.py` and `tests/test_evidence_ledger.py`
   against this contract.
2. Update Tier 1 output-family metadata to mark the six contracted fields as
   mapped, using existing schema vocabulary.
3. Preserve and, if needed, lightly update the #128 `match_id` entry notes.
4. Add entries for `match_started_at`, `match_finished_at`,
   `match_winner_team`, `match_result`, and `match_sync_status`.
5. Add focused tests for entry IDs, field aliases, direct/fallback evidence,
   derived aggregate deferral, privacy validation, copy safety, and
   deterministic serialization.
6. Run focused evidence-ledger tests.
7. Run adjacent parser-state tests because this contract documents state-owned
   finality and winner precedence, even though Codex C should not change state
   behavior.
8. Produce the implementation handoff.

## Compatibility

- The legacy workbook field spelling `MGTA Start Time` must remain unchanged.
- Existing workbook-facing field names must remain unchanged.
- Existing webhook payload shape must remain unchanged.
- Existing Apps Script assumptions must remain unchanged.
- Existing parser-state final reconciliation must remain unchanged.
- Existing #128 public constants, validators, and ledger build functions must
  remain available.
- Existing `match_id` ledger entry ID must remain stable.
- Existing value-source, confidence, finality, invariant-status, and drift-flag
  vocabularies must remain stable.

## Tests Required

Future implementation should run at minimum:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_state.py
python3 -m ruff check src tests tools
git diff --check
```

Recommended focused assertions:

- The built ledger validates cleanly.
- `iter_ledger_entries()` contains exactly the #128 `match_id` entry plus the
  five #130 lifecycle/result entries, unless Codex C explicitly documents a
  safer equivalent count.
- Tier 1 family metadata marks the six contracted fields as mapped.
- Deferred aggregate fields are not full ledger entries in #130.
- Each new entry has at least one evidence signal and all signal IDs are unique.
- `match_started_at` references explicit match-start metadata and
  first-summary-touch fallback.
- `match_finished_at` references final-result/match-completion metadata and
  last-summary-touch fallback.
- `match_winner_team` documents nested match-scope precedence and top-level
  match-complete fallback.
- `match_result` is marked derived from `match_winner_team` and `player_team`.
- `match_sync_status` is marked derived from parser-state readiness/live row
  construction.
- Entry privacy validation rejects raw-log-like text and absolute paths.
- Serialization remains deterministic.

Adjacent tests:

- `tests/test_state.py` should continue to prove nested match-scope winner
  precedence, top-level fallback gating, sync status behavior, and unknown
  winner handling.
- If those adjacent tests already cover the behavior, Codex C should cite them
  rather than changing parser state.

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md` exists.
- The contract clearly preserves parser truth ownership.
- The contract separates observed current behavior from required ledger
  metadata guarantees.
- The contract preserves #128 schema/vocabulary and the `match_id` anchor.
- The contract defines the exact #130 Tier 1 field set.
- The contract explicitly defers game-derived aggregate fields.
- The contract defines direct, fallback, derived, unknown, degraded, and
  conflict behavior for each contracted field.
- The contract documents match-winner precedence and unknown-winner semantics.
- The contract documents live/final sync-status provenance without changing
  final reconciliation.
- The contract lists implementation files, validation commands, and protected
  surfaces.
- The contract routes to Codex C with a pasteable handoff.

## Open Questions And Contract Risks

- The #128 schema has only `seeded_sample` and `registered_future` family
  statuses. #130 should not add a new status, but the name `seeded_sample` is
  increasingly broad once multiple Tier 1 fields are mapped. A future schema
  cleanup may add a clearer status such as `mapped`.
- `match_result` depends on `player_team`, but full participant mapping remains
  outside this issue. The entry must document that dependency without pretending
  participant provenance is fully mapped.
- `match_finished_at` currently comes from `last_event_time`; if the final
  winner arrives on an event with no timestamp, the end time can be blank even
  when the match is final. The ledger should mark that as degraded/unknown, not
  a parser error by itself.
- The broad #11 Tier 1 map includes more fields than #130. This contract is a
  deliberate slice, not completion of Tier 1.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #130, Tier 1 match lifecycle evidence ledger expansion under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/130
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/128
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/129
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier1-match-lifecycle
- Contract: docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- Existing schema contract: docs/contracts/player_log_evidence_ledger_schema.md

Goal:
Compare the current evidence ledger implementation and focused tests against the Tier 1 match lifecycle contract. Implement only the smallest documentation-aligned code/test changes needed to expand the ledger registry across the contracted Tier 1 match lifecycle fields.

Use:
- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/sheet_schema.py
- tests/test_state.py

Do:
- Preserve the #128 schema, validators, vocabulary constants, and match_id anchor entry.
- Add ledger entries for match_started_at, match_finished_at, match_winner_team, match_result, and match_sync_status.
- Keep derived aggregate fields deferred: Games Won, Games Lost, Total Games, Match Win Flag, and Game Win %.
- Use existing value-source, confidence, finality, invariant-status, and drift-flag vocabulary only.
- Preserve parser-owned truth boundaries.
- Add focused tests for the expanded entry set, source/fallback policies, aggregate deferral, validation, privacy, copy safety, and deterministic serialization.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_tier1_match_lifecycle_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser behavior.
- Change parser state final reconciliation.
- Change parser event classes.
- Change workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or AI/analytics truth.
- Implement runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, or feature-equity report changes.
- Reconstruct missing GameState data or infer facts that Player.log did not provide.
- Commit raw private Player.log excerpts.
- Target main directly.
- Close issue #11.
- Stage or commit unless explicitly asked.

Validation:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_state.py
- python3 -m ruff check src tests tools
- git diff --check
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/130"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/128"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/129"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier1_match_lifecycle_comparison.md"
  verdict: "ready_for_module_implementer"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier1-match-lifecycle"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_state.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, or AI/analytics truth."
    - "Do not reconstruct missing GameState data or infer facts that the Player.log did not provide."
    - "Do not implement runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, or feature-equity report changes."
    - "Do not commit raw private Player.log excerpts."
```
