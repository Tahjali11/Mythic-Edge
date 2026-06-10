# Analytics App Dashboard Live Capture Control Clarity - Implementation Handoff

## Role Performed

Codex C: Module Implementer / restoration and comparison thread.

## Issue And Contract

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/304
- Contract used: `docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md`
- Target artifact: `docs/implementation_handoffs/analytics_app_dashboard_live_capture_control_clarity_comparison.md`
- Worktree branch: `codex/dashboard-live-capture-control-restore-304`
- Base branch: `origin/codex/analytics-foundation`
- Risk tier: Medium frontend-only; High if backend/API lifecycle changes are needed.

## Git Status

Implementation was restored in a separate sibling worktree:

```text
MythicEdge-dashboard-live-capture-control-304
```

The worktree began clean from `origin/codex/analytics-foundation`. The #304 package was restored from the clean #304-only stash labeled `codex-preserve-304-dashboard-control-before-294`.

Final dirty files are #304-scoped only:

- `docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md`
- `docs/implementation_handoffs/analytics_app_dashboard_live_capture_control_clarity_comparison.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- Issue #304 via GitHub CLI
- `docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`

## Current Behavior Compared To Contract

The current repo already has backend-owned live capture lifecycle truth and frontend helpers:

- `fetchLiveCaptureStatus()`
- `startLiveCapture()`
- `stopLiveCapture()`
- typed `LiveCaptureStatusResponse`, `LiveCaptureStartResult`, and `LiveCaptureStopResult`

The contracted gap was Dashboard placement and operator clarity. The Dashboard could display a Live capture state, while the full lifecycle control lived in Diagnostics. The contract requires a stable Dashboard control area that uses backend status and allowed-action fields rather than frontend-owned capture truth.

## Implementation Option Chosen

Implemented the frontend-only option authorized by the contract:

- Restore the #304 Dashboard control package in a separate worktree.
- Preserve the current #294 `AnalyticsAutoRefreshNotice` placement when resolving the `frontend/src/App.tsx` conflict.
- Keep backend status as lifecycle truth.
- Add a stable action slot inside the existing Dashboard Live capture tile.
- Use existing start/stop handlers and reconcile from backend `capture_status`.
- Use a Diagnostics link rather than misleading Start/Stop controls for unavailable, blocked, stale, failed, degraded, unknown, or contradictory status.

No backend route, response schema, parser, analytics schema, or capture lifecycle behavior changed.

## Files Changed

- `docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md`
- `docs/implementation_handoffs/analytics_app_dashboard_live_capture_control_clarity_comparison.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

## Exact Sections Changed

### `frontend/src/App.tsx`

- Passed live capture control state and handlers into `CockpitStatusRail`.
- Preserved `AnalyticsAutoRefreshNotice` after the Dashboard status rail.
- Added `DashboardLiveCaptureControl` for the Dashboard Live capture tile.
- Added Dashboard-only lifecycle action derivation for:
  - start
  - stop
  - starting pending
  - stopping pending
  - diagnostics fallback
  - checking/no-action placeholder
- Added fail-closed Dashboard status handling for contradictory `status=capturing` with `capture.running=false`.

### `frontend/src/App.css`

- Added `.cockpitTileFooter` so status pill and action slot align consistently.
- Added Dashboard capture action-slot styles.
- Added responsive behavior so the action slot does not clip on small screens.

### `frontend/src/App.test.tsx`

- Added Dashboard tests proving:
  - persistent lifecycle control exists in the Live capture tile;
  - `Start capture` uses the existing handler;
  - repeated clicks are disabled while starting;
  - backend `capture_status` reconciles to `Stop capture`;
  - repeated clicks are disabled while stopping;
  - stop reconciliation returns to `Start capture`;
  - malformed/unavailable control state exposes no Start/Stop action;
  - contradictory active-looking status fails closed;
  - blocked ownership routes to Diagnostics without Start/Stop.

### `docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md`

- Restored the #304 contract artifact from the preserved #304 package.

### `docs/implementation_handoffs/analytics_app_dashboard_live_capture_control_clarity_comparison.md`

- Replaced the older stash-era handoff with this restoration-aware Codex C handoff.

## Change Classification

- Code changed: yes, frontend only.
- Tests changed: yes, focused frontend tests.
- Docs changed: yes, contract artifact and implementation handoff.
- Backend changed: no.
- Parser/runtime changed: no.
- Analytics schema or ingest changed: no.
- Fixtures/snapshots changed: no.
- Generated artifacts kept: no.

## Validation Run

- `npm --prefix frontend ci` -> passed, generated ignored local `frontend/node_modules`
- `npm --prefix frontend run typecheck` -> passed
- `npm --prefix frontend run test -- --run` -> passed, 3 files / 94 tests
- `npm --prefix frontend run build` -> passed
- `frontend/dist` cleanup -> removed generated build output
- `frontend/node_modules` cleanup -> removed validation-only dependency output
- `git diff --check` -> passed
- `py tools/check_agent_docs.py` -> passed
- path-scoped protected-surface scan over #304 touched files -> passed, forbidden 0, warnings 0
- path-scoped secret/private-marker scan over #304 touched files -> passed, forbidden 0, warnings 0

## Protected Surface Status

No protected parser/runtime/workbook/webhook/App Script/Sheets/analytics schema/OpenAI/AI/coaching/production behavior was intentionally touched.

The implementation only consumes existing frontend API helper results and existing handlers.

## Generated / Private Artifact Status

- No raw Player.log content was read, stored, printed, or exposed.
- No raw JSONL payloads, private paths, raw hashes, SQLite contents, secrets, credentials, environment values, runtime files, workbook exports, app-data files, or local-only artifacts were created or committed.
- `frontend/node_modules` was generated by `npm ci` and removed before handoff.
- `frontend/dist` was generated by the build check and removed before handoff.

## Remaining Risks Or Unverified Layers

- Browser visual smoke was not run in this restoration handoff.
- Diagnostics route control remains as-is; only the Dashboard action slot was changed.
- #302 heartbeat/no-row diagnostics and #294 auto-refresh remain separate scopes.
- The duplicate preserved #304 stashes were left untouched; this thread restored from one clean #304-only stash and did not delete local backup state.

## Forbidden Scope

Forbidden scope was not touched intentionally:

- no backend lifecycle semantics changed;
- no parser behavior changed;
- no analytics schema/migration/ingest behavior changed;
- no destructive UI/database/import/job controls added;
- no arbitrary SQL/database browsing added;
- no external writes added;
- no issue closure, staging, commit, PR, merge, or deploy action performed.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #304.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/304

Base branch:
codex/analytics-foundation

Implementation worktree branch:
codex/dashboard-live-capture-control-restore-304

Contract:
docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_dashboard_live_capture_control_clarity_comparison.md

Goal:
Review the restored #304 frontend-only Dashboard Live capture persistent-control implementation against the contract. Start from a contract-test stance: verify the implementation preserves backend-owned live capture lifecycle truth while adding a stable Dashboard action slot.

Inspect:
- git status --short --branch --untracked-files=all
- docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md
- docs/implementation_handoffs/analytics_app_dashboard_live_capture_control_clarity_comparison.md
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx
- frontend/src/api.ts
- frontend/src/types.ts
- frontend/src/status.ts

Review focus:
- Dashboard Live capture card has one persistent lifecycle control area.
- Stopped/ready shows Start capture only when backend status payload allows it.
- Starting and stopping states disable repeated clicks.
- Capturing shows Stop capture only when `status=capturing`, `capture.running=true`, and `stop_allowed=true`.
- Blocked/unavailable/malformed/contradictory states show no misleading Start/Stop and keep Diagnostics reachable.
- Start/Stop handlers use existing API helpers and reconcile from backend `capture_status`.
- Accessible names exist for Start capture, Stop capture, pending states, and Diagnostics fallback.
- The #294 auto-refresh Dashboard notice remains present and is not replaced by #304.
- No #302 heartbeat/no-row diagnostic backend behavior is implemented under #304.
- No backend route shape, backend lifecycle, parser, analytics schema, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed.
- No raw/private/local artifacts or destructive controls were introduced.

Validation:
- npm --prefix frontend run typecheck
- npm --prefix frontend run test -- --run
- npm --prefix frontend run build
- git diff --check
- py tools/check_agent_docs.py
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files
- remove frontend/dist after build if generated

Output:
- findings first, ordered by severity
- contract matches and mismatches
- validation run and result
- protected-surface/private-artifact status
- whether #304 can proceed to Codex F or must route to Codex D/B
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/304"
  completed_thread: "C"
  next_thread: "E"
  contract_artifact: "docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_app_dashboard_live_capture_control_clarity_comparison.md"
  worktree: "MythicEdge-dashboard-live-capture-control-304"
  branch: "codex/dashboard-live-capture-control-restore-304"
  base_branch: "origin/codex/analytics-foundation"
  risk_tier: "Medium frontend-only; High if backend/API lifecycle changes are needed"
  restoration_source: "stash label codex-preserve-304-dashboard-control-before-294"
  implementation_summary:
    - "Restored the #304 frontend-only package in a separate worktree."
    - "Added a stable Dashboard Live capture lifecycle action slot."
    - "Start/Stop remain driven by existing backend status and existing frontend handlers."
    - "Blocked, unavailable, malformed, stale, degraded, unknown, and contradictory states fail closed to Diagnostics."
    - "Preserved the current #294 analytics auto-refresh notice in the Dashboard."
  validation:
    - "npm --prefix frontend ci -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> passed, 3 files / 94 tests"
    - "npm --prefix frontend run build -> passed"
    - "frontend/dist cleanup -> removed generated build output"
    - "frontend/node_modules cleanup -> removed validation-only dependency output"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan over #304 touched files -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over #304 touched files -> passed, forbidden 0, warnings 0"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
