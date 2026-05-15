# Parser Saved Event Replay Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/54

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_saved_event_replay.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

This pass compared `src/mythic_edge_parser/app/saved_event_replay.py` and
`tests/test_saved_event_replay.py` against the saved-event replay contract. The
work stayed on `codex/parser-module-audit-suite` and did not open a PR, target
`main`, close issue #54, or mark tracker #5 complete.

## What Changed

The replay implementation already matches the contract's observed public
behavior. No runtime code was changed.

Focused tests were added to lock down contract-required replay behavior that
was previously implicit:

- exact supported event-kind mapping and unsupported-kind skip behavior
- all seven supported saved event kinds reconstructing successfully
- unversioned JSONL files losing to versioned files in the same parent
  directory
- global per-call raw-hash dedupe across selected files
- blank or missing raw hashes not participating in dedupe
- unknown-kind records incrementing skipped counts
- unknown-kind records with a nonblank hash consuming that hash before skip
- blank lines being invisible to stats
- callback exceptions propagating
- invalid JSON failing fast
- missing nested `payload` defaulting to an empty payload
- falsey or blank timestamps reconstructing as `None`
- invalid nonblank timestamps failing fast
- replay metadata raw bytes and raw hash being derived from the saved JSONL
  line, not from the stored `raw_bytes_hash`

Plain English: the replay utility is still only a local archive replay helper.
It reads saved JSONL records, reconstructs supported parser event objects,
dedupes by stored raw hash during that replay call, and calls the callback. It
does not interpret match/game truth, mutate parser state by itself, post
webhooks, write workbook rows, or change archive writing.

## Contract Matches

- `ReplayStats` exists with slotted dataclass fields `files_processed`,
  `events_processed`, and `events_skipped`.
- `EVENT_CLASS_BY_KIND` contains the seven contracted exact, case-sensitive
  supported kinds: `ClientAction`, `DetailedLoggingStatus`, `EventLifecycle`,
  `GameResult`, `GameState`, `MatchState`, and `Rank`.
- `latest_jsonl_files(root)` recursively scans `*.jsonl`, groups by exact
  parent directory, uses the highest `_v<number>_` filename version, treats
  unversioned files as `-1`, and sorts selected files by parent directory name.
- `event_from_saved_record(raw_line, payload)` reconstructs supported event
  objects from `kind`, parsed `timestamp`, and nested `payload`.
- Unknown, missing, differently cased, or whitespace-padded kinds return
  `None` rather than inventing parser events.
- Missing nested `payload` becomes `{}`.
- Missing, falsey, empty, and whitespace-only timestamps become `None`.
- Invalid nonblank timestamps fail fast through `datetime.fromisoformat()`.
- Replayed event metadata uses the saved JSONL line as `raw_bytes`; therefore
  `metadata.raw_bytes_hash` is recalculated from the saved line, not copied
  from the stored archive hash field.
- `replay_latest_saved_events(root, on_event)` uses a fresh replay-local
  `seen_raw_hashes` set per call.
- Nonblank `raw_bytes_hash` dedupe is global across selected files in one
  replay call.
- Blank or missing hashes do not participate in dedupe.
- Duplicate nonblank hashes are skipped before event reconstruction.
- A first-seen nonblank hash is consumed before unknown-kind skipping.
- Blank lines are ignored without changing stats.
- `events_processed` increments only after the callback returns normally.
- Unknown/unsupported kinds and duplicate hashes increment `events_skipped`.
- Invalid JSON, invalid timestamps, file errors, and callback errors remain
  fail-fast rather than being converted into skipped counts.
- The module remains callback-driven and does not call parser state, submit
  webhooks, write workbook rows, mutate Apps Script, or update runtime status.

## Contract Mismatches

No runtime implementation mismatch was found in
`src/mythic_edge_parser/app/saved_event_replay.py`.

The comparison found focused-test gaps against required or contract-covered
behavior. Those gaps were addressed in `tests/test_saved_event_replay.py`
without changing runtime behavior.

## Missing Safeguards

No new runtime safeguards were added because the contract documents current
fail-fast behavior as v1 compatibility.

Remaining comparison notes:

- Equal-version tie behavior still depends on `Path.rglob()` discovery order.
  The contract identifies this as an unknown/suspected gap rather than a
  required behavior change.
- Sorting by `path.parent.name` can still be ambiguous if different branches
  contain same-named parent directories.
- Non-dict top-level JSON and non-dict nested payload values remain fail-fast
  or event-constructor-owned behavior. The contract does not authorize a new
  graceful degradation policy.
- Replay still reconstructs only the seven contracted kinds, while
  `transforms.include_event()` may archive additional event kinds such as
  `Inventory`, `DeckCollection`, `MatchConnectionState`, `TcpConnectionClose`,
  `WebSocketClosed`, and `ConnectionError`.

## Missing Or Weak Tests

Resolved in this pass:

- every contracted supported event kind reconstructs successfully
- exact supported-kind mapping and unsupported-kind skip behavior
- unknown-kind skip stats
- falsey/blank timestamp behavior
- invalid timestamp fail-fast behavior
- invalid JSON fail-fast behavior
- missing payload default behavior
- latest-file unversioned-versus-versioned behavior
- cross-file global raw-hash dedupe
- blank/missing raw hash non-dedupe behavior
- hash consumption before unknown-kind skipping
- callback exception visibility
- replay metadata raw line hash behavior

Still missing or intentionally not added:

- equal-version tie behavior for two files in the same parent directory
- duplicate final parent directory names from different nested paths
- exact exception behavior for non-dict top-level JSON values
- exact exception behavior for non-dict nested payload values
- parser-state integration replay test that feeds replayed `MatchState` /
  `GameResult` events into state; the contract leaves this as an unknown
- a contract decision on whether every archived event kind should become
  replayable

## Files Changed

- `tests/test_saved_event_replay.py`
- `docs/implementation_handoffs/parser_saved_event_replay_comparison.md`

## Code Changed

No runtime code changed.

`src/mythic_edge_parser/app/saved_event_replay.py` was not edited. The only
code-like change was focused test coverage in `tests/test_saved_event_replay.py`.

## Tests Added Or Updated

Updated `tests/test_saved_event_replay.py`:

- added exact mapping and all-supported-kind reconstruction tests
- added timestamp, missing-payload, invalid-JSON, metadata-hash, callback
  exception, hash-dedupe, unknown-kind, and latest-file selection coverage

## Interface Changes

None.

No function signatures, parser event classes, archive JSONL producer shape,
webhook payloads, workbook columns, Apps Script entrypoints, environment
variables, runtime status files, parser-state final reconciliation, match
identity, game identity, or production dedupe semantics changed.

## Validation Run

Baseline focused check before edits:

```powershell
py -m pytest -q tests\test_saved_event_replay.py
```

Result:

```text
3 passed in 0.11s
```

Focused replay check after test updates:

```powershell
py -m pytest -q tests\test_saved_event_replay.py
```

Result:

```text
23 passed in 0.18s
```

Related parser regression check:

```powershell
py -m pytest -q tests\test_saved_event_replay.py tests\test_parser_regressions.py
```

Result:

```text
25 passed in 0.27s
```

Lint:

```powershell
py -m ruff check src tests
```

Result:

```text
All checks passed!
```

Diff whitespace:

```powershell
git diff --check
```

Result:

```text
Passed with no output.
```

## Forbidden Scope Confirmation

Forbidden scope was not touched.

This pass did not change parser behavior outside `saved_event_replay.py`,
parser state final reconciliation, workbook schema, webhook payload shape,
deployed Apps Script behavior, parser event classes, match identity, game
identity, production deduplication semantics outside replay, secrets,
environment variables, raw local logs, generated card data, runtime status
files, failed posts, workbook exports, or archive JSONL shape produced by
runtime code.

## Still Unverified

- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Webhook transport was not exercised.
- Replay into parser state was not exercised because the contract leaves that
  integration question unresolved.
- Full repo pytest was not run because runtime code did not change.
- GitHub issue/tracker state was not modified.

## Reviewer Focus

Ask Codex E / Module Reviewer to pay special attention to:

- whether test-only coverage is the right Codex C action for this contract
- whether `saved_event_replay.py` should remain unchanged despite unsupported
  archived event kinds
- whether fail-fast malformed-record behavior should stay as v1 compatibility
  or route back to Codex B for a degradation-policy contract update
- whether equal-version tie behavior and duplicate parent-name ordering need
  future contract clarification
- whether parser-state integration replay should be a future test requirement

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer / contract-test thread for https://github.com/Tahjali11/Mythic-Edge/issues/54.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Review:
- docs/contracts/parser_saved_event_replay.md
- docs/implementation_handoffs/parser_saved_event_replay_comparison.md
- src/mythic_edge_parser/app/saved_event_replay.py
- tests/test_saved_event_replay.py

Goal:
Verify that the Codex C comparison and test-only updates satisfy the saved-event replay contract without changing runtime replay behavior or protected downstream surfaces.

Focus on:
- public replay interfaces
- latest-file selection semantics
- event kind mapping
- timestamp behavior
- raw hash dedupe scope
- stats counting rules
- malformed and unknown record behavior
- callback side-effect boundaries
- parser truth ownership boundaries

Do not implement changes during review unless explicitly asked. Lead with findings, ordered by severity. If there are no blocking findings, say so clearly and identify any remaining non-blocking gaps.

Validation to consider:
py -m pytest -q tests\test_saved_event_replay.py
py -m pytest -q tests\test_saved_event_replay.py tests\test_parser_regressions.py
py -m ruff check src tests
git diff --check

Do not change parser behavior outside saved_event_replay.py. Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match identity, game identity, production deduplication semantics outside replay, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or archive JSONL shape produced by runtime code. Do not target main, open a PR, close issue #54, or mark tracker #5 complete.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/54"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/parser_saved_event_replay.md"
  target_artifact: "docs/implementation_handoffs/parser_saved_event_replay_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "py -m pytest -q tests\\test_saved_event_replay.py -> 23 passed in 0.18s"
    - "py -m pytest -q tests\\test_saved_event_replay.py tests\\test_parser_regressions.py -> 25 passed in 0.27s"
    - "py -m ruff check src tests -> All checks passed!"
    - "git diff --check -> passed with no output"
  stop_conditions:
    - "Do not change parser behavior outside saved_event_replay.py."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match identity, game identity, production deduplication semantics outside replay, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not change archive JSONL shape produced by runtime code unless routed back through a contract update."
    - "Do not target main."
    - "Do not open a PR from the comparison thread unless explicitly asked."
    - "Do not close issue #54 or mark tracker #5 complete."
```
