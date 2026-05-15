# Parser Event Lifecycle Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/32

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_event_lifecycle.md`

## Role Performed

Codex C: Module Implementer.

## Summary

Compared `src/mythic_edge_parser/parsers/event_lifecycle.py`, event class
behavior, router dispatch ordering, transform/config lifecycle handling, saved
event replay, and focused tests against the parser event-lifecycle contract.

No parser behavior mismatch was found. The implementation matches the contract
for known marker mapping, non-match fallback, local regex matching semantics,
tuple precedence, event shape, raw body preservation, metadata construction,
router reachability, transform/config inclusion, saved replay mapping, and
side-effect boundaries.

The comparison did find focused test gaps listed by the contract. I added
focused tests only. No runtime/parser implementation code changed.

## Confirmed Matches

- `event_lifecycle.try_parse(entry, timestamp)` remains the public parser
  entrypoint.
- The parser reads `entry.body` and does not inspect `entry.header` directly.
- Known markers map to the contracted payload types:
  - `==> EventJoin` -> `event_join`
  - `==> EventClaimPrize` -> `event_claim_prize`
  - `==> EventEnterPairing` -> `event_enter_pairing`
- Unknown lifecycle-like markers and unrelated bodies return `None`.
- Matching uses local compiled regex patterns with `search()`.
- Matching is case-sensitive.
- Whitespace and newlines after `==>` are accepted.
- Prefix-match behavior is preserved for longer method names such as
  `EventJoinSomethingElse`.
- Multiple known markers use tuple precedence, not raw-text order:
  `event_join`, then `event_claim_prize`, then `event_enter_pairing`.
- Malformed or absent JSON after a known marker still emits lifecycle evidence.
- Lifecycle JSON fields are not extracted into first-class payload fields.
- Emitted events are `EventLifecycleEvent`.
- `EventLifecycleEvent.kind == "EventLifecycle"`.
- `EventLifecycleEvent.performance_class == PerformanceClass.DURABLE_PER_EVENT`.
- Metadata timestamp is passed through from `try_parse()`.
- Metadata raw bytes are `entry.body.encode()`, with a populated raw hash.
- Payload shape remains exactly `type` and `raw_event_lifecycle`.
- `raw_event_lifecycle` preserves the full raw body string.
- Router `UNITY_CROSS_THREAD_LOGGER` and `UNKNOWN` buckets keep lifecycle
  parsing after session and before rank/collection/inventory.
- Router dispatch stops after lifecycle event emission.
- `KEEP_EVENT_LIFECYCLE_TYPES` contains all three emitted lifecycle types.
- `include_event()` keeps known lifecycle event types and rejects unknown
  lifecycle types.
- `summarize()` emits `EventLifecycle type=<type>`.
- `to_serializable()` preserves lifecycle payloads.
- `to_sheet_rows()` returns no normalized workbook rows for lifecycle events.
- Saved records with `kind == "EventLifecycle"` reconstruct as
  `EventLifecycleEvent`.

## Contract Mismatches

None found.

No parser behavior changes were required.

## Missing Safeguards

None found in `event_lifecycle.py`.

The contracted safeguards are present:

- non-matching bodies return `None` for downstream parser/router handling
- lifecycle parsing remains narrow to the three known marker patterns
- raw lifecycle JSON is not parsed into first-class fields
- raw body evidence is preserved
- event metadata is derived from the raw body and router timestamp
- the parser does not mutate entries, state, runtime files, workbook rows,
  webhook output, failed posts, generated data, or exports

## Missing Or Weak Tests

The contract's suspected focused test gaps were confirmed in the pre-change
tests. They were addressed by focused additions to:

- `tests/test_parser_small_modules.py`
- `tests/test_router_unit.py`
- `tests/test_transforms.py`
- `tests/test_saved_event_replay.py`

Tests added or strengthened:

- event metadata timestamp, raw bytes, raw hash, performance class, and exact
  payload shape for known markers
- unrelated body fallback to `None`
- case-sensitive matching
- whitespace/newline handling after `==>`
- prefix-match behavior for longer method names
- tuple precedence when multiple lifecycle markers appear in one body
- malformed lifecycle JSON still emitting raw-only lifecycle evidence
- router `UNKNOWN` bucket lifecycle position before rank
- router dispatch stopping after lifecycle event emission
- lifecycle transform/config synchronization for all emitted types
- transform inclusion, summary, serialization, and no sheet rows for lifecycle
  events
- unknown lifecycle type exclusion by `include_event()`
- saved `EventLifecycle` record reconstruction

Remaining non-blocking test notes:

- No parser behavior tests were added for new lifecycle markers because the
  contract preserves the current three-marker set.
- No workbook, webhook, Apps Script, parser state, or identity tests were added
  because those surfaces were not changed and are outside this contract.
- Future changes to marker exactness, tuple precedence, router order, or
  lifecycle JSON extraction require a new problem representation and contract.

## Files Changed

- `tests/test_parser_small_modules.py`
- `tests/test_router_unit.py`
- `tests/test_transforms.py`
- `tests/test_saved_event_replay.py`
- `docs/implementation_handoffs/parser_event_lifecycle_comparison.md`

## Code Changed

No runtime code changed.

No parser behavior, parser state final reconciliation, workbook schema, webhook
payload shape, Apps Script behavior, parser event classes outside the contract,
extractor behavior, match/game identity, deduplication, secrets, environment
variables, raw logs, generated data, runtime status files, failed posts, or
workbook exports changed.

## Validation Evidence

Baseline checks before adding tests:

```bash
python3 -m pytest -q tests/test_parser_small_modules.py
# Pass: 18 passed in 0.14s.

python3 -m pytest -q tests/test_router_unit.py tests/test_transforms.py
# Pass: 20 passed in 0.31s.

python3 -m pytest -q tests/test_saved_event_replay.py tests/test_parser_regressions.py
# Pass: 4 passed in 0.31s.
```

Checks after adding focused tests:

```bash
python3 -m pytest -q tests/test_parser_small_modules.py
# Pass: 26 passed in 0.06s.

python3 -m pytest -q tests/test_router_unit.py tests/test_transforms.py
# Pass: 24 passed in 0.16s.

python3 -m pytest -q tests/test_saved_event_replay.py tests/test_parser_regressions.py
# Pass: 5 passed in 0.16s.

python3 -m ruff check src tests
# Pass: All checks passed!
```

Protected runtime-source diff check:

```bash
git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
# Pass: no runtime implementation files changed.
```

Final documentation/worktree validation:

```bash
git diff --check
# Pass: no whitespace errors.

python3 -m pytest -q
# Pass: 513 passed in 3.16s.
```

## Still-Unverified Layers

- Live workbook behavior was not checked; no workbook schema or workbook export
  behavior was in scope.
- Deployed Apps Script behavior was not checked; no Apps Script behavior was in
  scope.
- GitHub Actions were not checked because no PR exists for this module yet.

## Next Recommended Role

Codex E: Module Reviewer in contract-test mode.

No Codex D fixer pass is recommended because no behavior mismatch or failing
validation remains after the focused test additions.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #32:
https://github.com/Tahjali11/Mythic-Edge/issues/32

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_event_lifecycle.md
- docs/implementation_handoffs/parser_event_lifecycle_comparison.md
- src/mythic_edge_parser/parsers/event_lifecycle.py
- tests/test_parser_small_modules.py
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/router.py
- tests/test_router_unit.py
- src/mythic_edge_parser/app/config.py
- src/mythic_edge_parser/app/transforms.py
- tests/test_transforms.py
- src/mythic_edge_parser/app/saved_event_replay.py
- tests/test_saved_event_replay.py
- tests/test_parser_regressions.py

Goal:
Verify the Module Implementer comparison and focused test additions against the parser event-lifecycle contract.

Confirm:
- EventJoin, EventClaimPrize, and EventEnterPairing map to the contracted lifecycle payload types.
- unknown lifecycle-like markers and unrelated bodies return None.
- matching remains case-sensitive.
- whitespace/newline after ==> is accepted.
- prefix-match behavior for longer method names is preserved.
- multiple known markers follow tuple precedence rather than raw-text order.
- malformed lifecycle JSON still emits raw-only lifecycle evidence.
- EventLifecycleEvent kind, DurablePerEvent performance class, timestamp, raw bytes, raw hash, and payload shape match the contract.
- raw_event_lifecycle preserves the full raw body string.
- lifecycle parser does not extract JSON fields into first-class payload data.
- router UNITY_CROSS_THREAD_LOGGER and UNKNOWN bucket lifecycle ordering remains after session and before rank/collection/inventory.
- router dispatch stops after lifecycle event emission.
- KEEP_EVENT_LIFECYCLE_TYPES contains all emitted lifecycle types.
- include_event(), summarize(), to_serializable(), and to_sheet_rows() handle lifecycle events as contracted.
- saved EventLifecycle records reconstruct as EventLifecycleEvent.
- no parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes outside the contract, extractor behavior, match/game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

Validation:
Run:
python3 -m pytest -q tests/test_parser_small_modules.py
python3 -m pytest -q tests/test_router_unit.py tests/test_transforms.py
python3 -m pytest -q tests/test_saved_event_replay.py tests/test_parser_regressions.py
python3 -m pytest -q
python3 -m ruff check src tests
git diff --check

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes outside the contract, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not stage, commit, merge, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/32"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_event_lifecycle.md"
  target_artifact: "docs/implementation_handoffs/parser_event_lifecycle_comparison.md"
  risk_tier: "Medium"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_parser_small_modules.py"
    - "python3 -m pytest -q tests/test_router_unit.py tests/test_transforms.py"
    - "python3 -m pytest -q tests/test_saved_event_replay.py tests/test_parser_regressions.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests"
    - "git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py"
    - "git diff --check"
  stop_conditions:
    - "Route to Module Contract Writer if the contract is ambiguous or inaccurate."
    - "Route to Module Fixer if reviewer finds a concrete parser behavior or focused-test mismatch."
    - "Do not change parser behavior unless required by the contract and covered by focused tests."
    - "Do not expand the marker set, parse lifecycle JSON into new fields, or change router dispatch order unless routed through an explicit contract decision."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes outside the contract, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned lifecycle marker truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not target main unless explicitly approved."
```
