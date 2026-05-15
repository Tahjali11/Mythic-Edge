# Player.log Evidence Ledger Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/11

Contract thread target: `docs/contracts/player_log_evidence_ledger.md`

## Contract

`docs/contracts/player_log_evidence_ledger.md`

Source context:

- `docs/problem_representations/player_log_evidence_ledger.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`

## Role Performed

Module Implementer / comparison thread.

This pass compared current repository behavior against the Player.log evidence
ledger contract. It did not assume a known bug, and it did not implement
behavior changes because the user explicitly asked for comparison only unless
implementation is requested after this handoff.

## What The Code Is Supposed To Do

The proposed ledger is a new quality and provenance layer around parser-owned
truth. In plain English: it should explain which Player.log evidence supports
each important parser-managed output, how trustworthy that evidence is, whether
the value is live/provisional/final/reconciled, and what warning flags or
invariants apply when the log format drifts.

The ledger must not become a second source of match/game truth. `state.py`,
`models.py`, `extractors.py`, and related parser/runtime modules continue to
own interpretation and normalized outputs.

## Current Behavior Summary

The current repository has the parser truth-producing layers and several
runtime/status surfaces, but it does not yet implement the Player.log evidence
ledger described by the contract.

Current behavior includes:

- `src/mythic_edge_parser/app/models.py` builds normalized match, game, and
  history payloads, including match identity, queue/format/rank fields,
  game-level results, play/draw, mulligans, opening hand fields, and sync
  status.
- `src/mythic_edge_parser/app/state.py` updates `MatchSummary` from parsed
  events and decides live/final row readiness for match and game log updates.
- `src/mythic_edge_parser/app/sheet_schema.py` defines workbook-facing sync
  fields and runtime sheet headers.
- `src/mythic_edge_parser/app/extractors.py` reads structured facts from parsed
  event payloads for state/runtime consumers.
- `src/mythic_edge_parser/app/runtime_surfaces.py`, `diagnostics.py`,
  `gameplay_actions.py`, and `card_performance.py` write local status and
  derived artifacts.
- `src/mythic_edge_parser/app/log_drift_sensor.py` provides a narrower raw-log
  routing drift report for unknown entry signatures and unmatched API names.

The current implementation does not expose field-level `value_source`,
`confidence`, `finality`, `drift_flags`, `invariant_status`, or
`review_required` metadata for parser-managed outputs.

## Contract Matches

- Layer ownership matches the contract's intent: parser/state/model/extractor
  code owns interpretation, while workbook and webhook code remain transport or
  display layers.
- Existing match and game row surfaces cover many Tier 1-3 output fields the
  ledger must eventually reference, including match IDs, result fields,
  games won/lost, queue type, format, event ID, rank fields, play/draw,
  mulligans, opening-hand size/names, turn count, and game duration.
- Existing `MATCH_LOG_SYNC_FIELDS` and `GAME_LOG_SYNC_FIELDS` make the current
  workbook-facing row contract explicit and testable.
- Existing tests verify that Python sync fields match Apps Script field maps,
  preserving the current workbook payload shape.
- Existing state behavior distinguishes live match log rows from final match
  rows and treats game-log update finality per game based on non-empty
  `Game Result`.
- Existing runtime/status code records parser runtime facts, webhook successes
  and failures, event/router failures, active match snapshots, match history,
  deck profiles, collection profiles, action logs, and card-performance
  artifacts.
- Existing `log_drift_sensor.py` partially overlaps with the future Tier 6
  drift idea by detecting routed versus unknown Player.log entries, unmatched
  API names, and baseline deltas.
- Existing drift-sensor privacy behavior avoids preserving long sensitive
  tokens in unknown-entry signatures.
- No forbidden scope was changed during this comparison.

## Contract Mismatches / Not-Yet-Implemented V1 Requirements

These are implementation gaps against the v1 ledger contract, not evidence of a
new parser bug.

- The future contract modules do not exist:
  `src/mythic_edge_parser/app/evidence_ledger.py`,
  `src/mythic_edge_parser/app/schema_snapshot.py`,
  `src/mythic_edge_parser/app/drift_report.py`, and
  `src/mythic_edge_parser/app/invariants.py`.
- There is no structured ledger object with
  `object="mythic_edge_player_log_evidence_ledger"`,
  `ledger_version="player_log_evidence_ledger.v1"`, and machine-readable
  `entries`.
- There are no `ledger_entry`, `evidence_signal`, or `field_evidence` result
  structures with the required fields from the contract.
- There is no schema snapshot object with
  `object="mythic_edge_player_log_schema_snapshot"`.
- There is no contract-shaped drift report with
  `object="mythic_edge_player_log_drift_report"`.
- The existing `log_drift_sensor.py` report uses
  `object="player_log_drift_report"` and reports raw routing drift only. It
  does not map parser outputs to source evidence, fallback behavior,
  confidence downgrade rules, invariants, or review modules.
- Tier 0 metadata is absent from downstream-queryable JSON: no
  `parser_contract_version`, `parser_commit_sha`, `log_schema_snapshot_id`,
  `ledger_version`, `value_source`, `confidence`, `finality`, `drift_flags`,
  `invariant_status`, or `review_required` layer exists.
- Tier 1-3 fields are not represented as full ledger entries with direct
  evidence, fallback evidence, degradation behavior, and invariant checks.
- Tier 4-7 future-tier registrations do not exist in code.
- Runtime status does not report missing expected signal paths, changed signal
  types, degraded parser outputs, invariant failures, or recommended review
  modules in the contract's shape.
- Card-performance analytics expose card resolution status, but not the minimum
  confidence of required ingredients.
- Action/deck/card runtime surfaces expose useful local artifacts, but they do
  not expose ledger vocabulary or evidence metadata.

## Missing Safeguards

- No central vocabulary enforcement exists for `value_source`, `confidence`,
  `finality`, `drift_flags`, or `invariant_status`.
- No field-level degradation mechanism marks a value as `unknown`, `conflict`,
  low-confidence, or review-required when expected evidence disappears.
- No invariant engine checks that parser outputs, game flow, and observed log
  signals agree.
- No schema snapshot comparison records missing expected payload paths, changed
  signal types, or new unknown paths in the ledger's required categories.
- No safeguard distinguishes parser drift from transport failure, workbook
  drift, and deployment drift in a single ledger/drift-report shape.
- No provenance layer preserves whether rank or queue values came from direct
  evidence, carry-forward evidence, inference, or fallback.
- Opening hand exact names can be hidden when unresolved IDs are present, but
  there is no field-level metadata saying whether the size/name value is
  observed, inferred, enriched, or unknown.
- Current runtime artifacts may be useful evidence sources, but there is no
  stable contract tying those artifacts back to specific parser-managed fields.

## Missing Tests

Required future tests named by the contract are absent:

- `tests/test_evidence_ledger.py`
- `tests/test_schema_snapshot.py`
- `tests/test_drift_report.py`
- `tests/test_invariants.py`

Additional missing or future tests:

- Tests proving every Tier 1 field has direct evidence or an explicit fallback
  policy.
- Tests proving every Tier 2 field has a classification source and degradation
  behavior.
- Tests proving every Tier 3 field has source, confidence, and finality
  behavior.
- Synthetic drift tests where expected game-result, rank, queue, submit-deck,
  opening-hand, or action evidence is removed or reshaped.
- Tests proving conflicting evidence produces `value_source=conflict`,
  `confidence=low`, `conflicting_evidence`, and `review_required=true`.
- Tests proving low-confidence final parser-managed fields cannot be labeled as
  high confidence.
- Tests proving schema snapshot absence produces `schema_snapshot_missing`.
- Tests proving drift reports distinguish parser drift from webhook transport
  failure, workbook drift, and deployment drift.
- Tests proving card-performance metrics expose or inherit the lowest
  confidence of their required ingredients once ledger metadata exists.

## Stale Or Bridge-Code Areas

- `log_drift_sensor.py` is useful existing drift tooling, but it is bridge-like
  relative to this contract because it reports routing coverage rather than
  field-level evidence and invariant status.
- Runtime object names still use existing `manasight_*` object labels for local
  artifacts. That is current behavior, not a ledger contract implementation.
- `grp_id_candidates.py` and auto-launcher code contain legacy confidence
  percentages for card-ID candidate workflows. Those are not the ledger's
  field-level confidence vocabulary.
- Apps Script field-map tests intentionally bridge Python sync fields to
  workbook transport behavior; the ledger contract says not to change that
  shape in this comparison pass.
- Existing parser fixtures and regression tests prove output behavior, but they
  do not map each output back to raw payload paths or field-level evidence
  labels.

## Files Inspected

- `docs/agent_constitution.md`
- `docs/agent_threads/implementation.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/problem_representations/player_log_evidence_ledger.md`
- `docs/templates/implementation_handoff.md`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/card_performance.py`
- `src/mythic_edge_parser/app/event_identity.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `tests/test_app_models.py`
- `tests/test_sheet_schema.py`
- `tests/test_state.py`
- `tests/test_app_extractors.py`
- `tests/test_parser_regressions.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_gameplay_actions.py`
- `tests/test_log_drift_sensor.py`

## Files Changed

- `docs/implementation_handoffs/player_log_evidence_ledger_comparison.md`

## Code Changed

Docs-only. No Python code or tests changed.

No workbook schema, webhook payload shape, deployed Apps Script behavior,
parser final reconciliation behavior, secrets, environment variables, raw local
logs, generated card data, runtime status files, or live workbook state were
changed.

## Interface Changes

None.

No function signatures, payload fields, workbook columns, environment
variables, Apps Script entrypoints, parser event classes, runtime status files,
or row field names changed.

## Tests Added Or Updated

None.

This was a comparison pass. Missing tests are listed above for the next role.

## Validation Run

Existing focused validation:

```powershell
py -m pytest -q tests/test_app_models.py tests/test_sheet_schema.py tests/test_state.py tests/test_app_extractors.py tests/test_parser_regressions.py tests/test_runtime_surfaces.py tests/test_gameplay_actions.py tests/test_log_drift_sensor.py
```

Result:

```text
94 passed in 1.18s
```

Future ledger-specific validation from the contract could not be run because
the future test files do not exist yet:

```powershell
py -m pytest -q tests/test_evidence_ledger.py tests/test_schema_snapshot.py tests/test_drift_report.py tests/test_invariants.py
```

## Forbidden Scope

Forbidden scope was not touched.

Specifically, this pass did not change workbook schema, webhook payload shape,
deployed Apps Script behavior, parser final reconciliation behavior, secrets,
environment variables, raw local logs, generated card data, runtime status
files, or live workbook state.

## Still Unverified

- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Webhook transport behavior was not exercised.
- Full repo test suite was not run because no code or tests changed.
- Future ledger modules and ledger-specific tests are unimplemented.
- No raw Player.log schema snapshot comparison was generated.
- No invariant engine was exercised because no invariant engine exists yet.

## Reviewer Focus

Ask the Module Reviewer / contract-test thread to pay special attention to:

- whether this handoff correctly classifies the ledger as unimplemented future
  behavior rather than a current parser bug
- whether `log_drift_sensor.py` should be treated as a reusable seed for
  `drift_report.py` or kept as a separate raw-routing audit tool
- whether Tier 0 metadata should live only in local JSON/status artifacts at
  first, or whether later implementation should also expose optional workbook
  columns in a separate schema-change thread
- whether current Tier 1-3 row outputs are complete enough to build ledger
  entries without changing parser interpretation behavior
- whether future tests should begin with static ledger coverage tests before
  synthetic drift/replay tests

## Next Workflow Action

Next role: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as the Module Reviewer / contract-test thread for docs/contracts/player_log_evidence_ledger.md.

Review docs/implementation_handoffs/player_log_evidence_ledger_comparison.md against docs/contracts/player_log_evidence_ledger.md and the current repository behavior.

Do not assume there is a known bug. This is a contract-review and test-planning pass. Do not implement behavior changes unless the review finds a clear, safe, local documentation or test correction that does not change parser behavior.

Focus on whether the comparison correctly separates:
- current parser behavior that already matches the contract's layer boundaries
- not-yet-implemented v1 ledger requirements
- missing safeguards
- missing tests
- stale or bridge-code areas

Do not change workbook schema, webhook payload shape, deployed Apps Script behavior, parser final reconciliation behavior, secrets, environment variables, raw local logs, generated card data, runtime status files, or live workbook state.

Run the smallest focused validation needed to verify the comparison claims. At minimum, inspect:
- docs/contracts/player_log_evidence_ledger.md
- docs/implementation_handoffs/player_log_evidence_ledger_comparison.md
- src/mythic_edge_parser/app/log_drift_sensor.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/sheet_schema.py
- tests/test_log_drift_sensor.py
- the focused tests listed in the handoff

Final review must include findings first, ordered by severity, then missing-test recommendations, validation run and result, still-unverified layers, and the next recommended role.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/player_log_evidence_ledger.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "py -m pytest -q tests/test_app_models.py tests/test_sheet_schema.py tests/test_state.py tests/test_app_extractors.py tests/test_parser_regressions.py tests/test_runtime_surfaces.py tests/test_gameplay_actions.py tests/test_log_drift_sensor.py"
    - "94 passed in 1.18s"
  stop_conditions:
    - "Do not implement behavior changes unless the user explicitly asks after the comparison handoff."
    - "Do not change workbook schema, webhook payload shape, deployed Apps Script behavior, parser final reconciliation behavior, secrets, environment variables, raw local logs, generated card data, runtime status files, or live workbook state."
```
