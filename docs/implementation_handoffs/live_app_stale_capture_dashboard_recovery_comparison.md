# Live App Stale Capture Dashboard Recovery Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Issue And Related Issues

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/315
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/302
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/304
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/294

## Contract Used

- `docs/contracts/live_app_stale_capture_dashboard_recovery.md`

## Branch And Worktree

- Worktree: isolated sibling worktree `MythicEdge-stale-capture-dashboard-recovery-315`
- Branch: `codex/live-app-stale-capture-dashboard-recovery-315`
- Base branch: `origin/codex/analytics-foundation`
- Branch sync before implementation: `0 0`
- Initial git status: one untracked contract artifact.

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/live_app_stale_capture_dashboard_recovery.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

## Current Behavior Compared To Contract

The current Dashboard already consumed backend live capture lifecycle status and already avoided Start/Stop actions for several blocked or contradictory states. However, when the Live capture card was blocked or stale, the lifecycle control area could be replaced by a larger diagnostics fallback link instead of retaining one stable lifecycle control plus a separate compact diagnostics affordance.

The contract requires stale capture state to fail closed. A stale backend response with `running=false`, `start_allowed=false`, `stop_allowed=false`, and a blurb that says `Restart capture` must not display as ready to start, must not expose Start/Stop/Restart controls, and must still provide diagnostics access.

## Implementation Option Chosen

Implemented the smallest frontend-only display correction:

- keep the Dashboard lifecycle slot stable across states;
- keep Start capture and Stop capture only when existing backend status and action flags make them safe;
- render stale, unavailable, loading, and blocked states as disabled lifecycle controls;
- add a compact, always-visible diagnostics link beside the lifecycle control;
- map stale dashboard detail copy to safe review language instead of surfacing restart-implying backend blurb text.

No backend lifecycle behavior, route shape, parser behavior, analytics schema, auto-refresh, or #302 diagnostics behavior was changed.

## Files Changed

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/live_app_stale_capture_dashboard_recovery_comparison.md`

Preserved and included in scope:

- `docs/contracts/live_app_stale_capture_dashboard_recovery.md`

## Exact Sections Changed

### `frontend/src/App.tsx`

- Reworked `DashboardLiveCaptureAction` to use a disabled `blocked` action instead of replacing blocked states with a diagnostics action.
- Updated `DashboardLiveCaptureControl` to always render a compact diagnostics link with accessible label `View live capture diagnostics`.
- Updated `dashboardLiveCaptureAction` so `liveCaptureDashboardBlocked(...)` is checked before Start/Stop selection.
- Added `dashboardLiveCaptureBlockedAction(...)` for disabled unavailable/needs-review controls.
- Added `liveCaptureDashboardDetail(...)` to keep stale dashboard copy safe and compact.
- Updated the Live capture cockpit tile detail to use safe dashboard detail text for `Needs review`.

### `frontend/src/App.css`

- Reworked `.dashboardCaptureControl` and `.dashboardCaptureActionSlot` for a stable lifecycle slot plus compact diagnostics affordance.
- Replaced the old full-width diagnostics fallback link styling with `.captureDiagnosticsLink`.
- Updated mobile sizing so the lifecycle action and diagnostics affordance stay stable without clipping.

### `frontend/src/App.test.tsx`

- Strengthened the existing start/stop dashboard test to assert diagnostics remains visible beside safe actions.
- Added a stale-state regression test covering `status=stale`, `state.stale=true`, `capture.reason=capture_state_stale`, `start_allowed=false`, `stop_allowed=false`, and restart-implying backend blurb text.

## Change Type

- Code changed: yes, frontend only.
- Tests changed: yes, focused frontend tests.
- Docs changed: yes, implementation handoff only.
- Backend changed: no.
- Parser/runtime/analytics schema changed: no.

## Validation Run

- `git status --short --branch --untracked-files=all` -> branch confirmed; contract initially untracked.
- `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation` -> `0 0`.
- `git diff --check` -> passed before frontend dependency install.
- `npm --prefix frontend run typecheck` -> initially failed because isolated worktree had no installed frontend dependencies (`tsc` missing).
- `npm --prefix frontend ci` -> passed; 113 packages installed temporarily, 0 vulnerabilities reported.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> passed; 3 test files, 95 tests.
- `npm --prefix frontend run build` -> passed.
- Generated `frontend/dist` and temporary `frontend/node_modules` were removed after validation.
- `py tools/check_agent_docs.py` -> passed.
- Path-scoped protected-surface scan over touched files -> passed; forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over touched files -> passed; forbidden 0, warnings 0.

## Protected-Surface Status

No parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior was touched.

## Secret And Private Artifact Status

No raw Player.log content, raw JSONL payloads, raw private paths, raw hashes, secrets, endpoint values, environment values, SQLite database files, runtime artifacts, or local-only artifacts were added.

## Generated Artifact Status

- `frontend/dist` removed after build validation.
- `frontend/node_modules` removed after validation.

## Remaining Risks And Unverified Layers

- Browser visual smoke was not run in this Codex C pass.
- Final path-scoped protected-surface and secret/private-marker scans should be run after this handoff is included in the touched-file list.
- Backend lifecycle recovery semantics remain intentionally unchanged and unverified by this frontend-only slice.

## Forbidden Scope

Forbidden scope touched: false.

No stale recovery, reset, restart, cleanup, backend lifecycle semantics, #302 diagnostics, #294 auto-refresh, arbitrary SQL, destructive controls, external writes, parser behavior, analytics schema, workbook/webhook, Apps Script, Sheets, AI/coaching, or production behavior was added.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #315.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/315

Related issues:
- https://github.com/Tahjali11/Mythic-Edge/issues/302
- https://github.com/Tahjali11/Mythic-Edge/issues/304
- https://github.com/Tahjali11/Mythic-Edge/issues/294

Branch:
codex/live-app-stale-capture-dashboard-recovery-315

Base branch:
origin/codex/analytics-foundation

Contract:
docs/contracts/live_app_stale_capture_dashboard_recovery.md

Implementation handoff:
docs/implementation_handoffs/live_app_stale_capture_dashboard_recovery_comparison.md

Risk tier:
Medium frontend-only; High if backend lifecycle or recovery behavior changes are needed.

Goal:
Review the active #315 package against docs/contracts/live_app_stale_capture_dashboard_recovery.md. Confirm that the Dashboard Live capture card fails closed for stale capture state, keeps backend lifecycle status as truth, preserves a stable lifecycle control, keeps diagnostics as a compact separate affordance, and does not expose restart/recovery behavior without backend authorization.

Review focus:
- Confirm stale status with running=false, start_allowed=false, stop_allowed=false, reason=capture_state_stale, and restart-implying backend blurb does not display Ready to start, Start capture, Stop capture, or Restart capture on the Dashboard.
- Confirm ready/stopped still exposes Start capture only when backend start_allowed=true.
- Confirm capturing still exposes Stop capture only when backend running=true and stop_allowed=true.
- Confirm blocked/unavailable/contradictory states fail closed with disabled lifecycle controls and visible diagnostics.
- Confirm diagnostics affordance routes to #diagnostics and is keyboard/accessibility reachable.
- Confirm no backend route shapes, lifecycle semantics, parser behavior, analytics schema/ingest, #302 diagnostics, #294 auto-refresh, external writes, raw/private artifacts, or destructive controls changed.

Validation:
git status --short --branch --untracked-files=all
git diff --check
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build

After npm validation, remove generated frontend/dist and frontend/node_modules before final report unless a later contract explicitly authorizes keeping them.

Run path-scoped protected-surface and secret/private-marker scans over:
- docs/contracts/live_app_stale_capture_dashboard_recovery.md
- docs/implementation_handoffs/live_app_stale_capture_dashboard_recovery_comparison.md
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx

Final report must include:
- role performed
- issue and related issues
- contract and handoff reviewed
- branch and git status
- findings first, ordered by severity
- validation run and result
- protected-surface status
- secret/private-marker status
- generated artifact status
- whether forbidden scope was touched
- verdict for Codex F readiness or route back to Codex D/C
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/315"
  related_issues:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/302"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/304"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  completed_thread: "C"
  next_thread: "E"
  worktree: "MythicEdge-stale-capture-dashboard-recovery-315"
  branch: "codex/live-app-stale-capture-dashboard-recovery-315"
  base_branch: "origin/codex/analytics-foundation"
  contract_artifact: "docs/contracts/live_app_stale_capture_dashboard_recovery.md"
  target_artifact: "docs/implementation_handoffs/live_app_stale_capture_dashboard_recovery_comparison.md"
  risk_tier: "Medium frontend-only; High if backend lifecycle or recovery behavior changes are needed"
  implementation_summary:
    - "Kept Dashboard Live capture lifecycle control stable across states."
    - "Added compact always-visible diagnostics link beside lifecycle control."
    - "Mapped stale Dashboard detail copy away from restart-implying backend blurb text."
    - "Added focused stale fail-closed and diagnostics-presence frontend assertions."
  validation:
    - "git diff --check -> passed before dependency install"
    - "npm --prefix frontend ci -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> passed, 3 files, 95 tests"
    - "npm --prefix frontend run build -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  generated_artifacts_removed:
    - "frontend/dist"
    - "frontend/node_modules"
  forbidden_scope_touched: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
