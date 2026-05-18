# GSM Truncation Parser Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/107

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

`docs/contracts/parser_gsm_truncation.md`

## Role Performed

Codex C: Module Implementer

## Comparison Before Editing

Confirmed current gaps against the contract:

- `src/mythic_edge_parser/events.py` had no `TruncationEvent`, and
  `GameEvent` did not include a truncation/data-loss event.
- `src/mythic_edge_parser/log/entry.py` had no first-class truncation marker
  header; the sanitized marker shape would have fallen into unknown header
  handling.
- `src/mythic_edge_parser/router.py` had no truncation dispatch path.
- No dedicated `src/mythic_edge_parser/parsers/truncation.py` module existed.
- `src/mythic_edge_parser/app/saved_event_replay.py` did not map
  `"Truncation"` to an event class.
- `src/mythic_edge_parser/app/transforms.py` would not include or summarize
  `Truncation` events.
- Parser event schema snapshots did not include a truncation event class or
  payload key set.
- Focused tests did not cover GSM truncation detection, false-positive
  boundaries, count normalization, routing stats, replay, transforms, or drift
  counting.

Confirmed boundaries that were preserved:

- GRE JSON parsing remains owned by `parsers/gre/__init__.py`.
- Truncation markers do not emit `GameStateEvent`, `GameResultEvent`,
  `MatchStateEvent`, or `ClientActionEvent`.
- Counts are normalized only as data-loss evidence about the omitted payload
  shape.
- Workbook schema, webhook payload shape, Apps Script behavior, runtime status
  schema, failed-post schema, parser state final reconciliation, match identity,
  game identity, and deduplication were not changed.
- Tests use sanitized synthetic marker text only. No raw private Player.log
  excerpts or Manasight source code were copied.

## What Changed

Implemented first-class parser-owned GSM truncation evidence:

- Added `TruncationEvent` with kind `"Truncation"` and
  `PerformanceClass.INTERACTIVE_DISPATCH`.
- Added `TruncationEvent` to the public `GameEvent` union and package exports.
- Added `EntryHeader.TRUNCATION_MARKER` with multiline buffering for sanitized
  marker lines beginning with `"[Message summarized"`.
- Added `src/mythic_edge_parser/parsers/truncation.py` with a conservative
  `try_parse()` that emits one `TruncationEvent` for explicit marker blocks.
- Added router dispatch for `EntryHeader.TRUNCATION_MARKER`.
- Added saved replay support for `"Truncation"` records.
- Updated transforms so `include_event()` keeps `Truncation`, `to_sheet_rows()`
  continues returning `[]`, and `summarize()` emits a concise sanitized summary.
- Updated parser event class and parser payload key snapshots for the new event
  only.

## Files Changed

Runtime/parser files:

- `src/mythic_edge_parser/__init__.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/parsers/truncation.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `src/mythic_edge_parser/app/transforms.py`

Focused tests and snapshots:

- `tests/test_gsm_truncation_parser.py`
- `tests/test_log_entry_headers.py`
- `tests/test_entry_buffer_edges.py`
- `tests/test_router_unit.py`
- `tests/test_saved_event_replay.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_log_drift_sensor.py`
- `tests/fixtures/schema_snapshots/parser_event_classes.json`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`

Handoff:

- `docs/implementation_handoffs/parser_gsm_truncation_comparison.md`

Source artifact note:

- `docs/contracts/parser_gsm_truncation.md` was present as an untracked source
  artifact before this implementation pass and was read but not edited.

## Interface Changes

Parser/event interface changes:

- New event class: `TruncationEvent`.
- New event kind: `"Truncation"`.
- New public event union member: `TruncationEvent` in `GameEvent`.
- New header enum member: `EntryHeader.TRUNCATION_MARKER` with value
  `"TruncationMarker"`.
- New parser module API:
  `mythic_edge_parser.parsers.truncation.try_parse(entry, timestamp)`.
- Saved replay now reconstructs saved records whose kind is `"Truncation"`.

Payload fields for `TruncationEvent`:

- `type`
- `marker_family`
- `affected_event_family`
- `affected_message_type`
- `data_loss`
- `recoverable`
- `parser_confidence`
- `value_source`
- `confidence`
- `finality`
- `drift_flag`
- `source_header`
- `game_object_count`
- `annotation_count`
- `raw_marker_summary`

No workbook columns, webhook fields, Apps Script mappings, runtime status schema
fields, failed-post schema fields, environment variables, secrets, or generated
data formats were added or changed.

## Validation Run

Focused contract suite:

```bash
python3 -m pytest -q tests/test_gsm_truncation_parser.py tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_router_unit.py tests/test_parsers.py tests/test_saved_event_replay.py tests/test_event_schema_snapshots.py tests/test_log_drift_sensor.py
```

Result:

```text
88 passed in 0.14s
```

Regression/touched-surface suite:

```bash
python3 -m pytest -q tests/test_parser_regressions.py tests/test_router_smoke.py tests/test_tailer_router_integration.py
```

Result:

```text
4 passed in 0.07s
```

Ruff:

```bash
python3 -m ruff check src tests
```

Result:

```text
All checks passed!
```

Protected-surface gate, committed branch diff mode:

```bash
python3 tools/check_protected_surfaces.py --base origin/main
```

Result:

```text
changed_paths: 1
forbidden: 0
warnings: 0
result: passed
```

Protected-surface gate, explicit local changed-file mode:

```bash
{ git diff --name-only; printf '%s\n' docs/contracts/parser_gsm_truncation.md src/mythic_edge_parser/parsers/truncation.py tests/test_gsm_truncation_parser.py; } | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Result:

```text
changed_paths: 19
forbidden: 0
warnings: 4
result: passed
```

The four warnings are protected parser/event/parser-module classifications for
contract-authorized files.

Full local test suite:

```bash
python3 -m pytest -q
```

Result:

```text
685 passed in 1.57s
```

Whitespace check:

```bash
git diff --check
```

Result: passed with no output.

Unavailable on this branch:

```bash
python3 tools/select_validation.py --base origin/main
python3 tools/check_secret_patterns.py --base origin/main
```

Result: both commands failed because those tool files are not present in the
`codex/parser-reliability-intelligence` worktree. This matches the contract
allowance to record branch-local hardening tools as unavailable.

## Still Unverified

- Remote CI has not run in this Codex C pass.
- Live Arena marker variants beyond the contracted sanitized
  `"[Message summarized"` family remain unknown.
- No live Player.log, workbook, webhook, Apps Script, runtime status file, or
  failed-post queue was exercised.
- No diagnostics UI/reporting field was added; current drift visibility is
  through existing routed-event-kind counting only.
- `docs/contracts/parser_gsm_truncation.md` remains an untracked source
  artifact in this worktree and should be handled intentionally by Codex F
  after review.

## Reviewer Focus

Codex E should pay special attention to:

- Whether marker recognition is conservative enough and does not over-classify
  nearby prose, unknown headers, GRE JSON, client actions, or count-only text.
- Whether the event payload stays within data-loss evidence and does not
  reconstruct omitted GameState facts.
- Whether router stats count exactly one routed event per marker block and do
  not also count it as unknown.
- Whether timestamp present, missing, and malformed paths preserve existing
  router semantics.
- Whether saved replay and parser schema snapshots changed only for
  `Truncation`.
- Whether `include_event()`, `to_sheet_rows()`, and `summarize()` meet the
  transform contract without changing workbook/webhook/App Script surfaces.

## Next Workflow Action

Next role: Codex E: Module Reviewer in contract-test mode.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for parser reliability issue #107:
https://github.com/Tahjali11/Mythic-Edge/issues/107

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/47

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Use:
- docs/contracts/parser_gsm_truncation.md
- docs/implementation_handoffs/parser_gsm_truncation_comparison.md
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/log/entry.py
- src/mythic_edge_parser/router.py
- src/mythic_edge_parser/parsers/__init__.py
- src/mythic_edge_parser/parsers/truncation.py
- src/mythic_edge_parser/parsers/gre/__init__.py
- src/mythic_edge_parser/app/saved_event_replay.py
- src/mythic_edge_parser/app/transforms.py
- tests/test_gsm_truncation_parser.py
- tests/test_log_entry_headers.py
- tests/test_entry_buffer_edges.py
- tests/test_router_unit.py
- tests/test_parsers.py
- tests/test_saved_event_replay.py
- tests/test_event_schema_snapshots.py
- tests/test_log_drift_sensor.py
- tests/fixtures/schema_snapshots/parser_event_classes.json
- tests/fixtures/schema_snapshots/parser_payload_keys.json

Goal:
Verify the Codex C implementation against the GSM truncation marker contract.

Confirm:
- `TruncationEvent` exists with kind `"Truncation"` and `InteractiveDispatch` performance class.
- `GameEvent` includes `TruncationEvent`.
- The dedicated truncation parser emits exactly one first-class event for the sanitized explicit GSM marker shape.
- Count parsing is conservative: explicit nonnegative integers only, zero valid, missing/malformed/negative ambiguous values become `None`, and one count is not inferred from the other.
- The event payload contains only parser-owned data-loss evidence and no reconstructed GameState objects, annotations, zones, actions, timers, raw private logs, secrets, webhook URLs, or environment values.
- Metadata raw-bytes hash behavior is preserved.
- Header and buffer handling classify only the explicit `"[Message summarized"` marker family as multiline `TruncationMarker`.
- Nearby non-marker text, count-only lines, normal GRE JSON, client actions, match state, metadata, connection messages, and unrelated unknown headers are not routed as truncation.
- Router dispatch counts marker entries as routed, not unknown, and preserves timestamp present/missing/malformed stats.
- GRE parsing remains sibling behavior and does not receive fabricated `gameStateMessage` dictionaries.
- Saved-event replay reconstructs `Truncation`.
- Parser event schema snapshots and payload snapshots changed only for the new event and payload keys.
- `include_event()` includes `Truncation`, `to_sheet_rows()` returns `[]`, and `summarize()` uses normalized fields only.
- Drift reports count routed `Truncation` events and do not list the synthetic marker as an unknown signature.
- Workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, extractor behavior, match/game identity, deduplication, secrets, environment variables, raw logs, generated runtime artifacts, runtime status schema, failed-post schema, and workbook exports did not change.

Validation:
Run:
python3 -m pytest -q tests/test_gsm_truncation_parser.py tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_router_unit.py tests/test_parsers.py tests/test_saved_event_replay.py tests/test_event_schema_snapshots.py tests/test_log_drift_sensor.py
python3 -m pytest -q tests/test_parser_regressions.py tests/test_router_smoke.py tests/test_tailer_router_integration.py
python3 -m ruff check src tests
python3 -m pytest -q
git diff --check

Also run:
python3 tools/check_protected_surfaces.py --base origin/main

If reviewing uncommitted local files before submission, also run the protected-surface gate with an explicit changed-path stdin list because base-vs-HEAD mode does not include unstaged/untracked files.

Record `tools/select_validation.py` and `tools/check_secret_patterns.py` as unavailable if they are still absent from this branch.

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F if no blocking findings, otherwise Codex D or Codex B.
- workflow_handoff block.

Do not fix code in review mode.
Do not copy Manasight source code.
Do not paste raw private Player.log excerpts into repo files.
Do not reconstruct omitted GameState payload data.
Do not infer match winner, game winner, match identity, game identity, or final reconciliation facts from truncation alone.
Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, extractor behavior, match/game identity, deduplication, secrets, environment variables, raw logs, generated runtime artifacts committed to the repo, runtime status file schema, failed-post schema, or workbook exports.
Do not target main directly.
Do not stage or commit.
Do not mark tracker #47 complete.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/107"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_gsm_truncation.md"
  target_artifact: "docs/implementation_handoffs/parser_gsm_truncation_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_gsm_truncation_parser.py tests/test_log_entry_headers.py tests/test_entry_buffer_edges.py tests/test_router_unit.py tests/test_parsers.py tests/test_saved_event_replay.py tests/test_event_schema_snapshots.py tests/test_log_drift_sensor.py"
    - "python3 -m pytest -q tests/test_parser_regressions.py tests/test_router_smoke.py tests/test_tailer_router_integration.py"
    - "python3 -m ruff check src tests"
    - "python3 -m pytest -q"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "explicit local changed-path protected-surface stdin check"
    - "git diff --check"
    - "not run - tools/select_validation.py unavailable on this branch"
    - "not run - tools/check_secret_patterns.py unavailable on this branch"
  stop_conditions:
    - "Do not copy Manasight source code."
    - "Do not paste raw private Player.log excerpts into repo files."
    - "Do not reconstruct omitted GameState payload data."
    - "Do not infer match winner, game winner, match identity, game identity, or final reconciliation facts from truncation alone."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, extractor behavior, match/game identity, deduplication, secrets, environment variables, raw logs, generated runtime artifacts committed to the repo, runtime status file schema, failed-post schema, or workbook exports."
    - "Do not target main directly; parser reliability work belongs on codex/parser-reliability-intelligence."
    - "Do not mark tracker #47 complete."
```
