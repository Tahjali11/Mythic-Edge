# Parser Runner Contract-Test Report

## Findings

No blocking findings.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/36

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_runner.md`

## Implementation Under Test

Branch: `codex/parser-module-audit-suite`

Implementation handoff:
`docs/implementation_handoffs/parser_runner_comparison.md`

Reviewed source surfaces:

- `src/mythic_edge_parser/app/runner.py`
- `tests/test_runner.py`
- `tests/test_app_outputs.py`
- `tests/test_diagnostics.py`
- `tests/test_status_api.py`
- `tests/test_stream_unit.py`
- `tests/test_stream_integration.py`
- `tests/test_state.py`
- `tests/test_transforms.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_sheet_exports.py`
- `tests/test_parser_regressions.py`

Changed-file scope reviewed:

- `tests/test_runner.py`
- `docs/contracts/parser_runner.md`
- `docs/implementation_handoffs/parser_runner_comparison.md`
- `docs/contract_test_reports/parser_runner.md`

Runtime implementation code was not changed.

## Contract Summary

`src/mythic_edge_parser/app/runner.py` must remain the parser/runtime bridge. It
owns runtime orchestration, startup status, side-effect ordering, kept-event
archive and row dispatch, submitted-deck diagnostics, callback-driven posted
state, runner-stage failure recording, and shutdown sequencing.

Runner must not become parser truth, workbook schema truth, webhook payload
shape truth, Apps Script truth, parser state final reconciliation truth, match
or game identity truth, or deduplication truth.

## Checks Run

```bash
git diff --check
python3 -m pytest -q tests/test_runner.py
python3 -m pytest -q tests/test_app_outputs.py tests/test_diagnostics.py tests/test_status_api.py
python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py
python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_sheet_exports.py
python3 -m pytest -q tests/test_parser_regressions.py
python3 -m ruff check src tests
git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py data workbook_exports exports
python3 -m ruff check tests/test_runner.py
python3 -m pytest -q
```

## Results

- `git diff --check` -> passed with no output.
- `python3 -m pytest -q tests/test_runner.py` -> `18 passed in 0.35s`.
- `python3 -m pytest -q tests/test_app_outputs.py tests/test_diagnostics.py tests/test_status_api.py`
  -> `13 passed in 0.75s`.
- `python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py`
  -> `4 passed in 0.08s`.
- `python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_sheet_exports.py`
  -> `40 passed in 0.26s`.
- `python3 -m pytest -q tests/test_parser_regressions.py`
  -> `2 passed in 0.17s`.
- `python3 -m ruff check src tests` -> `All checks passed!`.
- `git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py data workbook_exports exports`
  -> passed with no output.
- `python3 -m ruff check tests/test_runner.py` -> `All checks passed!`.
- `python3 -m pytest -q` -> `522 passed in 1.22s`.

## Contract-Test Verdict

Pass.

The Module Implementer test-only patch satisfies the parser runner contract.
No blocking contract mismatch, missing focused test, protected-surface drift, or
runtime behavior change was found.

## Confirmed Contract Matches

- `runner.py` remains a runtime orchestration bridge and does not become parser
  truth owner.
- No runner implementation behavior changed for this pass.
- Focused tests cover display-safe paths, startup status sanitization, sheet
  posting aggregation, and debug row gating.
- Focused tests now cover kept-event side-effect ordering.
- Focused tests now cover dropped-event all-event surfaces versus kept-only
  archive and row paths.
- Focused tests now cover runner-stage failure recording and subscriber-loop
  continuation.
- Focused tests now cover `_startup_issues()` warning/error classifications.
- Focused tests now cover status API startup success and startup failure status
  updates.
- Focused tests now cover Game Log and Match Log success-callback copy
  semantics.
- Focused tests now cover shutdown ordering after stream creation.
- Parser state still sees every non-`None` event before keep/drop decisions.
- Diagnostics, gameplay observation, and analytics sidecar submission still
  run before the keep/drop branch.
- Kept events only are archived locally and posted through runner-owned
  workbook row paths.
- Submitted-deck diagnostics remain kept-event only and continue to consume
  parser-produced `ClientAction` payloads.
- Game Log and Match Log posted-state markers remain success-callback driven.
- MatchSummary once-only posting remains success-callback driven.
- Status API startup failure remains non-fatal and writes the contracted error
  status fields.
- Shutdown drains webhook results around dispatcher shutdown, stops analytics,
  marks runtime stopped, stops the status API, and shuts down the stream.
- No workbook schema, webhook payload shape, Apps Script behavior, parser
  event classes, parser state final reconciliation, extractor behavior, match
  identity, game identity, deduplication, secrets, environment variables, raw
  logs, generated data, runtime status files, failed posts, or workbook exports
  changed.

## Contract Mismatches

None.

## Missing Tests

None blocking.

The contract-required focused runner gaps documented by Codex B and Codex C are
covered in `tests/test_runner.py`:

- main-loop kept-event side-effect ordering
- dropped-event all-event surfaces and kept-only side effects
- runner-stage failure recording and continuation
- startup warning/error classification
- status API startup success/failure status updates
- Game Log and Match Log success-callback copy semantics
- shutdown ordering after stream creation

## Drift Notes

- No parser behavior drift found.
- No parser truth drift found; runner stays orchestration-only.
- No parser state final reconciliation drift found.
- No workbook schema, webhook payload shape, Apps Script behavior, parser event
  class, extractor, match identity, game identity, deduplication, raw-log,
  generated-data, runtime-status, failed-post, or workbook-export drift found.
- No protected runtime-source files changed.
- Tracker #5 remains open and must not be marked complete by Codex E.

## Remaining Non-Blocking Gaps

- GitHub Actions/PR checks were not observed in this local contract-test pass.
- The main-loop tests use fake stream/subscriber objects rather than a live
  MTGA event stream.
- Live webhook dispatcher, analytics sidecar, status API server, workbook, and
  Apps Script behavior were not exercised; those layers are out of scope for
  this runner contract-test pass.
- The contract records existing behavior for
  `stop_analytics_sidecar(wait_for_queue=False)` and status API
  disabled-by-configuration handling; this pass does not change those
  non-blocking risks.

## Recommendation

Approve for submitter work.

Next recommended role: Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for issue #36 and the parser runner contract audit.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/36

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_runner.md
- docs/implementation_handoffs/parser_runner_comparison.md
- docs/contract_test_reports/parser_runner.md
- src/mythic_edge_parser/app/runner.py
- tests/test_runner.py

Goal:
Submit the parser runner contract-audit test-only package for review, without targeting main.

Confirm:
- Codex E found no blocking findings.
- The changed implementation scope is test/docs only.
- Runtime implementation code is unchanged.
- The PR targets codex/parser-module-audit-suite.
- No workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, extractor behavior, match identity, game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports are included.

Validation:
Run or cite fresh validation:
git diff --check
python3 -m pytest -q tests/test_runner.py
python3 -m pytest -q tests/test_app_outputs.py tests/test_diagnostics.py tests/test_status_api.py
python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py
python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_sheet_exports.py
python3 -m pytest -q tests/test_parser_regressions.py
python3 -m ruff check src tests
python3 -m pytest -q

Output:
- Submitter verdict.
- PR/branch status.
- Validation evidence.
- Protected-surface confirmation.
- Next recommended role: Codex G only after PR checks pass and review is ready.
- A workflow_handoff block.

Do not merge, close issue #36, mark tracker #5 complete, target main, or change parser/runtime/workbook/App Script behavior.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/36"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_runner.md"
  target_artifact: "PR for parser runner contract audit"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check -> passed with no output"
    - "python3 -m pytest -q tests/test_runner.py -> 18 passed in 0.35s"
    - "python3 -m pytest -q tests/test_app_outputs.py tests/test_diagnostics.py tests/test_status_api.py -> 13 passed in 0.75s"
    - "python3 -m pytest -q tests/test_stream_unit.py tests/test_stream_integration.py -> 4 passed in 0.08s"
    - "python3 -m pytest -q tests/test_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_sheet_exports.py -> 40 passed in 0.26s"
    - "python3 -m pytest -q tests/test_parser_regressions.py -> 2 passed in 0.17s"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py data workbook_exports exports -> no output"
    - "python3 -m ruff check tests/test_runner.py -> All checks passed!"
    - "python3 -m pytest -q -> 522 passed in 1.22s"
  stop_conditions:
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, extractor behavior, match identity, game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned truth into runner orchestration, workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not target main; module PR work belongs on codex/parser-module-audit-suite."
    - "Do not mark tracker #5 complete."
```
