# Parser Event Lifecycle Contract-Test Report

## Findings

No blocking findings.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/32

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_event_lifecycle.md`

## Implementation Under Test

Branch: `codex/parser-module-audit-suite`

Implementation handoff:
`docs/implementation_handoffs/parser_event_lifecycle_comparison.md`

Reviewed source surfaces:

- `src/mythic_edge_parser/parsers/event_lifecycle.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`

Changed-file scope reviewed:

- `tests/test_parser_small_modules.py`
- `tests/test_router_unit.py`
- `tests/test_transforms.py`
- `tests/test_saved_event_replay.py`
- `docs/contracts/parser_event_lifecycle.md`
- `docs/implementation_handoffs/parser_event_lifecycle_comparison.md`
- `docs/contract_test_reports/parser_event_lifecycle.md`

Runtime implementation code was not changed.

## Contract Summary

`src/mythic_edge_parser/parsers/event_lifecycle.py` owns narrow parser-layer
recognition of three MTGA event lifecycle request markers and emits
`EventLifecycleEvent` evidence with raw-body preservation. It does not parse
lifecycle JSON fields, infer match or game identity, mutate parser state, post
workbook rows, or own downstream analytics.

The contract intentionally preserves current local regex behavior, including
case-sensitive matching, whitespace after `==>`, prefix matches for longer
method names, and tuple-order precedence when multiple lifecycle markers appear
in one body.

## Checks Run

```bash
python3 -m pytest -q tests/test_parser_small_modules.py
python3 -m pytest -q tests/test_router_unit.py tests/test_transforms.py
python3 -m pytest -q tests/test_saved_event_replay.py tests/test_parser_regressions.py
python3 -m pytest -q
python3 -m ruff check src tests
git diff --check
git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
```

## Results

- `python3 -m pytest -q tests/test_parser_small_modules.py`
  -> `26 passed in 0.07s`.
- `python3 -m pytest -q tests/test_router_unit.py tests/test_transforms.py`
  -> `24 passed in 0.17s`.
- `python3 -m pytest -q tests/test_saved_event_replay.py tests/test_parser_regressions.py`
  -> `5 passed in 0.18s`.
- `python3 -m pytest -q` -> `513 passed in 1.14s`.
- `python3 -m ruff check src tests` -> `All checks passed!`.
- `git diff --check` -> passed with no output.
- `git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py`
  -> passed with no output.

## Contract-Test Verdict

Pass.

The Module Implementer comparison and focused test additions match the parser
event-lifecycle contract. The prior suspected focused-test gaps are covered,
and no behavior mismatch was found.

## Confirmed Contract Matches

- `event_lifecycle.try_parse(entry, timestamp)` remains the public parser
  entrypoint.
- `EventJoin`, `EventClaimPrize`, and `EventEnterPairing` map to the
  contracted lifecycle payload types.
- Unknown lifecycle-like markers and unrelated bodies return `None`.
- Matching remains case-sensitive.
- Whitespace and newline after `==>` are accepted.
- Prefix-match behavior for longer method names is preserved.
- Multiple known markers follow tuple precedence rather than raw-text order.
- Malformed lifecycle JSON still emits raw-only lifecycle evidence.
- Emitted events are `EventLifecycleEvent`.
- `EventLifecycleEvent.kind == "EventLifecycle"`.
- `EventLifecycleEvent.performance_class == PerformanceClass.DURABLE_PER_EVENT`.
- Metadata timestamp is passed through from `try_parse()`.
- Metadata raw bytes are `entry.body.encode()`, and raw hash is populated.
- Payload shape remains exactly `type` and `raw_event_lifecycle`.
- `raw_event_lifecycle` preserves the full raw body string.
- Lifecycle parser does not extract JSON fields into first-class payload data.
- Router `UNITY_CROSS_THREAD_LOGGER` and `UNKNOWN` bucket lifecycle ordering
  remains after session and before rank/collection/inventory.
- Router dispatch stops after lifecycle event emission.
- `KEEP_EVENT_LIFECYCLE_TYPES` contains all emitted lifecycle types.
- `include_event()`, `summarize()`, `to_serializable()`, and `to_sheet_rows()`
  handle lifecycle events as contracted.
- Saved `EventLifecycle` records reconstruct as `EventLifecycleEvent`.
- No parser state final reconciliation, workbook schema, webhook payload
  shape, Apps Script behavior, parser event classes outside the contract,
  extractor behavior, match/game identity, deduplication, final
  reconciliation, secrets, environment variables, raw logs, generated data,
  runtime status files, failed posts, or workbook exports changed.

## Contract Mismatches

None.

## Missing Tests

None blocking.

Focused coverage now includes:

- known lifecycle marker mapping and exact payload shape
- unknown marker and unrelated-body fallback to `None`
- case-sensitive matching
- whitespace/newline handling after `==>`
- current prefix-match behavior for longer method names
- tuple precedence for multi-marker bodies
- malformed lifecycle JSON still producing raw-only lifecycle evidence
- metadata timestamp, raw bytes, raw hash, event kind, and performance class
- router `UNKNOWN` bucket lifecycle position before rank
- router dispatch stopping after lifecycle event emission
- transform/config synchronization for all emitted lifecycle types
- transform inclusion, summary, serialization, and no sheet rows for lifecycle
  events
- unknown lifecycle type exclusion by `include_event()`
- saved `EventLifecycle` record reconstruction

## Drift Notes

- No parser behavior drift found.
- No lifecycle marker truth drift found; raw marker recognition remains in the
  parser layer.
- No router dispatch-order drift found in the reviewed surface.
- No transform/config lifecycle inclusion drift found.
- No saved-event replay drift found for `EventLifecycle` records.
- No parser state final reconciliation drift found in the reviewed surface.
- No workbook/webhook/App Script/runtime artifact drift found in the reviewed
  surface.
- No protected runtime-source files changed.

## Remaining Non-Blocking Gaps

- Prefix matching for longer method names remains an explicit contract risk,
  but the contract preserves current behavior and the focused tests lock it.
- Multiple known markers still use tuple precedence rather than raw-text order;
  future changes require a new problem representation and contract.
- Lifecycle JSON content remains raw-only. Extracting event IDs, queue IDs, or
  other fields would require a new contract.
- GitHub Actions were not checked because no PR exists for this module yet.
- Live workbook behavior was not checked; workbook schema and exports are out
  of scope.
- Deployed Apps Script behavior was not checked; Apps Script behavior is out
  of scope.

## Recommendation

Approve for submitter work.

Next recommended role: Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for issue #32 and the parser event-lifecycle contract audit.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/32

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_event_lifecycle.md
- docs/implementation_handoffs/parser_event_lifecycle_comparison.md
- docs/contract_test_reports/parser_event_lifecycle.md
- tests/test_parser_small_modules.py
- tests/test_router_unit.py
- tests/test_transforms.py
- tests/test_saved_event_replay.py

Reviewer verdict:
No blocking findings. The parser event-lifecycle contract audit is ready for submitter work.

Submitter requirements:
- Verify current branch and changed-file scope.
- Stage only the reviewed parser event-lifecycle audit artifacts.
- Commit and push the branch.
- Open or update a draft PR targeting codex/parser-module-audit-suite, not main.
- Do not merge, close issue #32, or mark tracker #5 complete; those are Codex G responsibilities.

Validation to run or verify:
python3 -m pytest -q tests/test_parser_small_modules.py
python3 -m pytest -q tests/test_router_unit.py tests/test_transforms.py
python3 -m pytest -q tests/test_saved_event_replay.py tests/test_parser_regressions.py
python3 -m pytest -q
python3 -m ruff check src tests
git diff --check

Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes outside the contract, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not merge, close issue #32, mark tracker #5 complete, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/32"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_event_lifecycle.md"
  target_artifact: "docs/contract_test_reports/parser_event_lifecycle.md"
  risk_tier: "Medium"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_parser_small_modules.py -> 26 passed in 0.07s"
    - "python3 -m pytest -q tests/test_router_unit.py tests/test_transforms.py -> 24 passed in 0.17s"
    - "python3 -m pytest -q tests/test_saved_event_replay.py tests/test_parser_regressions.py -> 5 passed in 0.18s"
    - "python3 -m pytest -q -> 513 passed in 1.14s"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "git diff --check -> passed with no output"
    - "git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py -> passed with no output"
  stop_conditions:
    - "Do not change parser behavior unless required by the contract and covered by focused tests."
    - "Do not expand the marker set, parse lifecycle JSON into new fields, or change router dispatch order unless routed through an explicit contract decision."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes outside the contract, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned lifecycle marker truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not merge, close issue #32, or mark tracker #5 complete; route deployer work to Codex G."
    - "Do not target main unless explicitly approved."
```
