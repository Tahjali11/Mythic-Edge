# Parser Runner Implementation Comparison

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/36

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Source contract: `docs/contracts/parser_runner.md`

Target branch: `codex/parser-module-audit-suite`

Role: Codex C: Module Implementer

Risk tier: High

## Summary Of Implementation Comparison

The current `runner.py` implementation matches the parser-runner contract for
the observed behavior reviewed in this pass. No runner behavior change was
needed.

The comparison found one clear contract mismatch in focused test coverage:
`tests/test_runner.py` covered display paths, startup status sanitization,
sheet-posting aggregation, and raw/GameState debug row gating, but did not
cover the contract-required main-loop ordering, dropped-event behavior,
runner-stage failure continuation, startup issue classification, status API
status updates, success-callback copy semantics, or shutdown order.

This pass adds focused tests for those missing contracted behaviors and leaves
parser/runtime/workbook/App Script behavior unchanged.

Changed files:

- `tests/test_runner.py`
- `docs/implementation_handoffs/parser_runner_comparison.md`

Referenced source artifact present in the worktree:

- `docs/contracts/parser_runner.md`

## Findings First

### Resolved: missing focused runner tests

Contract requirement:

- Add a focused async runner-loop test with fake stream/subscriber objects that
  proves per-event side-effect order.
- Add a dropped-event test proving state, diagnostics, gameplay observation,
  and analytics run while archive and row posting do not.
- Add an event-failure test proving `record_event_failure(..., stage="runner")`
  is called and the loop continues.
- Add `_startup_issues()` warning/error tests.
- Add status API startup success/failure tests where practical.
- Add success-callback copy-semantics tests for Game Log and Match Log rows.
- Add shutdown-order coverage where practical.

Initial state:

- `tests/test_runner.py` had 9 focused tests.
- Main-loop and callback ordering risks were documented but untested.

Resolution:

- Added fake stream/subscriber tests around `runner.main()`.
- Added dropped-event, failure-continuation, status API, startup issue,
  callback snapshot, and shutdown-order tests.
- `tests/test_runner.py` now has 18 passing tests.

### No behavior mismatch found

The new tests passed without modifying `src/mythic_edge_parser/app/runner.py`.
That confirms the audited behavior currently satisfies the contract for the
focused surfaces tested in this pass.

## Confirmed Matches

- `runner.py` remains a runtime orchestration bridge, not a parser truth owner.
- `main()` remains the async runtime entrypoint.
- `_display_path(None)` returns `""`.
- Project-relative display paths remain relative to `PROJECT_ROOT`.
- External POSIX paths and Windows-style paths on POSIX display as basenames.
- Startup status fields use display-safe paths and redacted webhook target
  text.
- `_sheet_posting_enabled()` includes GameState and sidecar/output posting
  flags.
- Raw/debug row posting stays gated by `POST_RAW_EVENT_ROWS` or
  `POST_GAMESTATE_ROWS` for `GameState` events.
- Parser state, diagnostics, gameplay observation, and analytics submission
  happen before the keep/drop branch.
- Dropped events still update all-event surfaces and do not reach local JSONL
  archive or runner-owned row posting.
- Kept events reach local JSONL archive, submitted-deck handling, debug rows,
  Game Log rows, MatchSummary row, Match Log row, and summary logging in the
  documented order.
- Runner-stage event failures call `record_event_failure(..., stage="runner")`
  and the subscriber loop continues.
- Startup issue classification preserves warning/error boundaries for missing
  log path, blank webhook, invalid webhook URL, missing tier normalization
  data, and unreadable tier JSON.
- Status API startup success writes local status API fields; startup failure is
  recorded as non-fatal status.
- Game Log and Match Log success callbacks snapshot row dictionaries and
  changed-field lists before asynchronous success handling.
- Shutdown drains webhook results around dispatcher shutdown, stops analytics,
  marks runtime stopped, stops status API, and shuts down the stream.

## Contract Mismatches

No unresolved contract mismatch is known after this pass.

The only mismatch found was missing focused test coverage. It was resolved in
`tests/test_runner.py`.

## Missing Safeguards

No blocking missing safeguard remains for this runner audit pass.

Behavior deliberately left unchanged:

- `stop_analytics_sidecar(wait_for_queue=False)` remains the observed shutdown
  behavior recorded by the contract.
- Status API disabled-by-configuration behavior remains as currently recorded:
  no explicit disabled status field is written when `start_status_api_server()`
  returns `None`.
- Runner shutdown calls are not independently wrapped in best-effort exception
  handlers; the contract records current behavior.

These are not fixed here because the contract documents them as current
behavior or future-risk areas, not required behavior changes for Codex C.

## Missing Or Weak Tests

Blocking focused test gaps from the contract were addressed.

Remaining non-blocking gaps:

- Tests use fake stream/subscriber objects rather than a live `MtgaEventStream`.
- Tests do not cover real thread lifecycle behavior in the webhook dispatcher,
  analytics sidecar, or status API server.
- Tests do not add a new end-to-end stream/router regression; adjacent existing
  stream and parser regression tests were run instead.
- Tests do not change or assert status API disabled-by-configuration status
  fields because the contract records current behavior and does not require a
  change.

## Validation Evidence

Commands run:

```bash
python3 -m pytest -q tests/test_runner.py
```

Result:

```text
18 passed in 0.24s
```

```bash
python3 -m ruff check tests/test_runner.py
```

Result:

```text
All checks passed!
```

```bash
python3 -m pytest -q tests/test_app_outputs.py tests/test_diagnostics.py tests/test_status_api.py
```

Result:

```text
13 passed in 1.70s
```

```bash
python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py
```

Result:

```text
4 passed in 0.61s
```

```bash
python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_sheet_exports.py
```

Result:

```text
40 passed in 1.18s
```

```bash
python3 -m pytest -q tests/test_parser_regressions.py
```

Result:

```text
2 passed in 0.72s
```

```bash
python3 -m ruff check src tests
```

Result:

```text
All checks passed!
```

```bash
git diff --check
```

Result: passed with no output.

```bash
python3 -m pytest -q
```

Result:

```text
522 passed in 1.34s
```

## Still-Unverified Layers

- A live MTGA parser run was not executed.
- GitHub Actions/Windows CI was not executed in this pass.
- Submitter/deployer PR checks have not run.
- Tracker #5 remains open and must not be marked complete by this role.

## Protected Surface Evidence

No changes were made to:

- `src/mythic_edge_parser/app/runner.py`
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- parser state final reconciliation
- extractor behavior
- match identity
- game identity
- deduplication
- secrets
- environment variables
- raw logs
- generated data
- runtime status files
- failed posts
- workbook exports

Name-only protected surface sanity command run:

```bash
git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py data workbook_exports exports
```

Result: no output.

## Next Recommended Role

Next recommended role: Codex E: Module Reviewer in contract-test mode.

Reason: the contract comparison is complete, the missing focused tests were
added, validation is passing for focused and adjacent checks, and no behavior
fix was required. Reviewer should verify the new tests against the contract
and confirm the protected surfaces stayed untouched.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #36:
https://github.com/Tahjali11/Mythic-Edge/issues/36

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_runner.md
- docs/implementation_handoffs/parser_runner_comparison.md
- src/mythic_edge_parser/app/runner.py
- tests/test_runner.py
- tests/test_app_outputs.py
- tests/test_diagnostics.py
- tests/test_status_api.py
- tests/test_stream_unit.py
- tests/test_stream_integration.py
- tests/test_state.py
- tests/test_transforms.py
- tests/test_runtime_surfaces.py
- tests/test_sheet_exports.py
- tests/test_parser_regressions.py

Goal:
Verify the Module Implementer patch against the parser runner contract.

Confirm:
- `runner.py` remains a runtime orchestration bridge and does not become parser truth owner.
- No runner behavior changed unless explicitly required by the contract.
- Focused tests cover display-safe paths, startup status sanitization, sheet posting aggregation, and debug row gating.
- Focused tests now cover kept-event side-effect ordering.
- Focused tests now cover dropped-event all-event surfaces versus kept-only archive/row paths.
- Focused tests now cover runner-stage failure recording and subscriber-loop continuation.
- Focused tests now cover `_startup_issues()` warning/error classifications.
- Focused tests now cover status API startup success and startup failure status updates.
- Focused tests now cover Game Log and Match Log success-callback copy semantics.
- Focused tests now cover shutdown ordering after stream creation.
- Parser state still sees every non-`None` event before keep/drop decisions.
- Diagnostics, gameplay observation, and analytics sidecar submission still run before the keep/drop branch.
- Kept events only are archived locally and posted through runner-owned workbook row paths.
- Posted-state markers remain success-callback driven.
- No workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, extractor behavior, match identity, game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

Validation:
Run:
git diff --check
python3 -m pytest -q tests/test_runner.py
python3 -m pytest -q tests/test_app_outputs.py tests/test_diagnostics.py tests/test_status_api.py
python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py
python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_sheet_exports.py
python3 -m pytest -q tests/test_parser_regressions.py
python3 -m ruff check src tests

If feasible, run:
python3 -m pytest -q

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, parser event classes, extractor behavior, match identity, game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not move parser-owned truth into runner orchestration, workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation.
Do not stage, commit, merge, target main, or mark tracker #5 complete.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/36"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_runner.md"
  target_artifact: "docs/implementation_handoffs/parser_runner_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_runner.py"
    - "python3 -m ruff check tests/test_runner.py"
    - "python3 -m pytest -q tests/test_app_outputs.py tests/test_diagnostics.py tests/test_status_api.py"
    - "python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py"
    - "python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_sheet_exports.py"
    - "python3 -m pytest -q tests/test_parser_regressions.py"
    - "python3 -m ruff check src tests"
    - "git diff --check"
    - "python3 -m pytest -q"
  stop_conditions:
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, extractor behavior, match identity, game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned truth into runner orchestration, workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not target main; module PR work belongs on codex/parser-module-audit-suite."
    - "Do not mark tracker #5 complete."
```
