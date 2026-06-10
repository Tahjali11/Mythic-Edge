# Live App MTGA Process Detection, Shutdown Readiness Gate Comparison

## Role Performed

Codex C: Module Implementer / comparison thread for issue #337.

## Issue And Contract

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/337
- Contract: `docs/contracts/live_app_mtga_process_detection_shutdown_readiness_gate.md`
- Branch: `codex/live-mtga-process-lifecycle-gate`
- Base branch: `codex/analytics-foundation`
- Target artifact: `docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_comparison.md`
- Risk tier: High

## Branch And Git Status

Initial inspection confirmed the worktree was on `codex/live-mtga-process-lifecycle-gate` at `702121f` and synced `0 0` with `origin/codex/analytics-foundation`.

During implementation, `origin/codex/analytics-foundation` advanced by two docs-only commits:

- `fae5fdc` merge PR #338 from `codex/advisory-import-boundary-report`
- `5315353` docs: add advisory import-boundary report

Final status before handoff showed the #337 package active in the worktree and branch behind by two commits. No staging or commit was performed.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/live_app_mtga_process_detection_shutdown_readiness_gate.md`
- GitHub issue #337
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `tests/test_live_app_explicit_start_capture_control.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_auto_refresh_after_match_completion.py`

## Current Behavior Compared To Contract

Current repo behavior already provided explicit manual live capture start/stop, heartbeat/progress/no-row diagnostics, read-only watcher readiness/process-safeguard status, Diagnostics composition, and local SQLite writes for completed parser-owned match/game facts.

The gap was that the repo had no backend-owned Windows `MTGA.exe` process-presence signal, no `mtga_lifecycle` object, no 45-second reconnect-window state, no timeout-driven app-owned capture shutdown, and no safe automation readiness gate tied to the process lifecycle.

## Implementation Option Chosen

Implemented the smallest additive backend/frontend package authorized by the contract:

- Keep existing routes.
- Add a new mockable helper for sanitized Windows `tasklist` image-name detection.
- Add `mtga_process` and `automation_readiness` to `GET /api/live/watcher/process`.
- Add MTGA process entries to existing watcher Diagnostics.
- Add `mtga_lifecycle` to `GET /api/live/capture/status`.
- Keep GET status routes read-only; reconnect/shutdown state mutation happens inside the already-running app-owned capture supervisor.
- Keep manual capture as the default and keep auto-start blocked.

## Files Changed

- `src/mythic_edge_parser/local_app/mtga_process_lifecycle.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `tests/test_live_app_mtga_process_lifecycle.py`
- `docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_comparison.md`

The untracked contract `docs/contracts/live_app_mtga_process_detection_shutdown_readiness_gate.md` was preserved and included as the source contract artifact.

## Exact Sections Changed

- Added `mtga_process_lifecycle.py` with `build_mtga_process_status(...)`, `build_automation_readiness(...)`, safe detector parsing, and privacy flags.
- Extended `live_watcher_process.py` response with `mtga_process` and blocked `automation_readiness`.
- Extended `live_watcher_diagnostics.py` with MTGA process diagnostics, automation-start blocked diagnostics, and process-source limitations that exclude PID/raw-output display.
- Extended `live_capture_control.py` with sanitized `mtga_lifecycle`, supervisor-owned MTGA checks, reconnect-window state, timeout shutdown, operator-stop lifecycle labels, and persistent auto-start blocking.
- Extended frontend `types.ts` and `api.ts` with strict `mtga_process`, `mtga_lifecycle`, and `automation_readiness` validators.
- Updated frontend tests to include and reject unsafe MTGA lifecycle/process payloads.
- Added backend tests for detector safety, process/diagnostics display, GET read-only lifecycle status, reconnect, reconnected continuation, timeout shutdown, and preservation of completed row metadata.

## Change Type

Code changed: yes.
Tests changed: yes.
Docs changed: yes, implementation handoff only.
Schema/migration changed: no.
Fixtures/snapshots changed: no.
Frontend build output committed: no.

## Validation Run

- `py -m pytest -q tests\test_live_app_mtga_process_lifecycle.py` -> passed, 7 tests.
- `py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py` -> passed, 41 tests.
- `py -m pytest -q tests\test_live_app_mtga_process_lifecycle.py tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py tests\test_analytics_auto_refresh_after_match_completion.py` -> passed, 54 tests.
- `npm --prefix frontend ci` -> passed; created local `node_modules` only.
- `npm --prefix frontend run typecheck` -> passed after frontend test fixtures were updated.
- `npm --prefix frontend run test -- --run` -> passed, 3 files / 96 tests.
- `npm --prefix frontend run build` -> passed.
- Removed generated `frontend/dist` after build.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- `py tools/check_agent_docs.py` -> passed.
- path-scoped protected-surface scan over changed files -> passed, forbidden 0, warnings 0.
- path-scoped secret/private-marker scan over changed files -> passed, forbidden 0, warnings 0.
- new-file whitespace/final-newline check -> passed.
- generated artifact status check -> `frontend/dist` absent.

## Protected-Surface Status

No parser behavior, parser state final reconciliation, event classes, match/game identity, deduplication, analytics schema/migrations, workbook schema, webhook payload shape, Apps Script, Sheets, OpenAI/AI/coaching, Line Tracer, or production behavior was intentionally changed.

## Secret And Private Artifact Status

The detector and tests avoid raw `tasklist` output, PIDs, command lines, environment values, raw Player.log content, raw paths, raw hashes, secrets, endpoint values, generated SQLite contents, stack traces, runtime files, and private/local artifacts.

`frontend/dist` was removed after build. `frontend/node_modules` was installed locally for validation and remains an ignored/generated dependency directory, not an implementation artifact.

## Remaining Risks Or Unverified Layers

- The branch is behind `origin/codex/analytics-foundation` by two commits and should be refreshed or reviewed for conflicts before Codex F/PR work.
- No real MTGA process was inspected; tests use mocked detector output as required by the contract.
- No live private Player.log/app-data root was used.
- No browser visual smoke was run; this implementation changed validators and test fixtures, not primary UI layout.

## Forbidden Scope

Forbidden scope was not touched. Automatic capture startup was not implemented. MTGA is not launched or killed. The implementation does not expose process command lines, environment values, PIDs, raw detector output, raw Player.log content, or private/local artifacts.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #337.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/337

Branch:
codex/live-mtga-process-lifecycle-gate

Base branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_mtga_process_detection_shutdown_readiness_gate.md

Implementation handoff:
docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_comparison.md

Goal:
Review the active #337 implementation against the contract. Confirm the Windows-only MTGA.exe process detector, sanitized mtga_process and mtga_lifecycle fields, 45-second backend-owned reconnect window, safe app-owned timeout shutdown, Diagnostics-first display, and blocked automation readiness gate. Lead with findings if any.

Before reviewing:
- Confirm branch and git status.
- Note that the implementation branch may be behind origin/codex/analytics-foundation by two docs-only commits.
- Read the contract and implementation handoff.
- Inspect changed backend, frontend validator, and focused test files.

Review focus:
- Detector uses a fixed tasklist command vector with shell=false and exposes no PID, command line, environment values, raw stdout/stderr, raw paths, or private artifacts.
- GET routes remain read-only except in-memory response computation.
- Reconnect/shutdown mutation happens only inside the app-owned running capture supervisor.
- Player.log silence while MTGA.exe is detected does not stop capture.
- Timeout shutdown stops only app-owned capture and preserves completed parser-owned write metadata.
- Automatic startup remains blocked and automatic_start_allowed=false.
- Frontend validators reject unsafe process/lifecycle payloads.
- No parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed.

Validation to run:
py -m pytest -q tests\test_live_app_mtga_process_lifecycle.py tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py tests\test_analytics_auto_refresh_after_match_completion.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py

Run path-scoped protected-surface and secret/private-marker scans over changed files. Remove frontend/dist after build if created.

Final report must include:
- role performed
- issue/contract/handoff reviewed
- branch and git status
- findings first, ordered by severity
- validation run and results
- protected-surface status
- secret/private-marker status
- generated artifact status
- whether forbidden scope was touched
- recommendation for next role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/337"
  completed_thread: "C"
  next_thread: "E"
  contract_artifact: "docs/contracts/live_app_mtga_process_detection_shutdown_readiness_gate.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_comparison.md"
  branch: "codex/live-mtga-process-lifecycle-gate"
  base_branch: "codex/analytics-foundation"
  risk_tier: "High"
  verdict: "implemented_active_ready_for_contract_review"
  decision: "Windows-only MTGA.exe process detection, backend-owned reconnect/shutdown lifecycle, Diagnostics-first display, and blocked automation readiness gate. Manual capture remains default; auto-start remains blocked."
  validation:
    - "py -m pytest -q tests\\test_live_app_mtga_process_lifecycle.py -> passed"
    - "py -m pytest -q tests\\test_live_app_explicit_start_capture_control.py tests\\test_analytics_local_app_backend.py -> passed"
    - "py -m pytest -q tests\\test_live_app_mtga_process_lifecycle.py tests\\test_live_app_explicit_start_capture_control.py tests\\test_analytics_local_app_backend.py tests\\test_analytics_auto_refresh_after_match_completion.py -> passed"
    - "npm --prefix frontend ci -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> passed"
    - "npm --prefix frontend run build -> passed"
    - "frontend/dist removed after build"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "new-file whitespace/final-newline check -> passed"
    - "generated artifact status -> frontend/dist absent"
  branch_sync_note: "branch is behind origin/codex/analytics-foundation by two docs-only commits at handoff time"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
