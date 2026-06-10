# Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/321

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

## Contract

`docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md`

## Internal Project Area

Local App / UI.

## Truth Owner

Backend live capture status owns lifecycle truth. The frontend only displays
sanitized status and calls explicit backend start/stop controls. Parser,
analytics, workbook, and AI truth ownership were unchanged.

## Bridge-Code Status

shared_support

## Role Performed

Codex C: Module Implementer / comparison thread.

## What Changed

Compared the current Dashboard live-capture workflow against the #321 contract.
The existing backend and frontend already supported explicit manual
start/stop, fail-closed stale/blocked display, Diagnostics routing, and
analytics refresh polling. The remaining gap was that the compact Dashboard
Live capture tile always replaced active capture detail with `Capture active.`,
which could hide the backend-led post-match success line authorized by the
contract.

Implemented a narrow frontend-only display fix: the Dashboard now preserves the
exact safe backend-led line `Most recent completed match was recorded.` when
that is the live-capture detail. Other active capture states still use the
compact `Capture active.` text.

## Files Changed

- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/live_app_frontend_capture_operator_workflow_refresh_comparison.md`

In-scope untracked contract preserved without C-thread edits:

- `docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md`

## Code Changed

Runtime frontend code changed in `frontend/src/App.tsx`.

Exact section changed:

- `compactLiveCaptureDetail(...)` now allows the contract-approved recorded
  match line through before applying generic compact active-capture copy.

No backend code, route shape, API schema, parser code, analytics schema,
watcher lifecycle, workbook/webhook, Apps Script, Sheets, OpenAI, AI/coaching,
or production behavior changed.

## Tests Added Or Updated

Updated `frontend/src/App.test.tsx`.

Exact test sections changed:

- Strengthened the Dashboard lifecycle-control test to assert `startCapture`
  and `stopCapture` are not called when the Dashboard loads.
- Added a focused Dashboard test proving the backend-led recorded-match line is
  shown in the Live capture tile without inventing score text or showing Start
  while capture is active.

## Interface Changes

None. No function signatures, payload fields, route paths, workbook columns,
environment variables, or script entrypoints changed.

## Contracted Area Status

Stayed inside the contracted Local App / UI frontend display surface. Manual
capture remains the v1.0 default operator workflow. Automatic capture startup,
stale cleanup/reset/delete/restart/recovery behavior, backend lifecycle
semantics, and parser/analytics truth ownership remain deferred and unchanged.

## Current Behavior Compared To Contract

- Dashboard manual start/stop controls already depend on backend
  `start_allowed`, `stop_allowed`, and capture status.
- Loading the Dashboard already avoids automatic capture startup; this is now
  pinned by test.
- Stale/blocked capture state already fails closed and routes to Diagnostics.
- Analytics auto-refresh status and manual refresh surfaces already existed.
- Diagnostics already rendered backend-led capture blurbs.
- Gap fixed: the Dashboard tile previously hid the safe
  `Most recent completed match was recorded.` line while capture was active.

## Implementation Option Chosen

Smallest scoped frontend-only display and test update. No backend lifecycle
changes were needed, so no route-back to Codex B was required.

## Validation Run

```text
git status --short --branch --untracked-files=all
-> ## codex/analytics-foundation...origin/codex/analytics-foundation
->  M frontend/src/App.test.tsx
->  M frontend/src/App.tsx
-> ?? docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md
-> ?? docs/implementation_handoffs/live_app_frontend_capture_operator_workflow_refresh_comparison.md

git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
-> 0 0

gh issue view 321 --json number,title,state,body,comments
-> issue #321 open

npm --prefix frontend run typecheck
-> passed

npm --prefix frontend run test -- --run frontend/src/App.test.tsx
-> path filter was repo-root relative while Vitest ran from frontend; rerun with frontend-relative path

npm --prefix frontend run test -- --run src/App.test.tsx
-> passed, 57 tests

npm --prefix frontend run test -- --run
-> passed, 96 tests

npm --prefix frontend run build
-> passed; generated frontend/dist was removed after validation

git diff --check
-> passed

py tools/check_agent_docs.py
-> passed, errors 0, warnings 0

path-scoped protected-surface scan over changed files
-> passed, forbidden 0, warnings 0

path-scoped secret/private-marker scan over changed files
-> passed, forbidden 0, warnings 0
```

## Still Unverified

- Live browser smoke against the running local app.

## Reviewer Focus

Ask Codex E to verify:

- The Dashboard shows the recorded-match line only from the backend-led
  sanitized live-capture detail.
- Dashboard load does not start capture automatically.
- Stale/blocked/unavailable states still fail closed and do not become
  restart/recovery controls.
- No backend lifecycle, parser, analytics schema, workbook/webhook, Apps
  Script, Sheets, OpenAI, AI/coaching, or production behavior changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #321.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/321

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md

Implementation handoff:
docs/implementation_handoffs/live_app_frontend_capture_operator_workflow_refresh_comparison.md

Risk tier:
Medium-High if kept frontend/workflow-only; High if backend lifecycle, stale recovery, or automatic startup behavior changes are needed

Goal:
Review the active implementation against the #321 contract. Confirm the manual
capture operator workflow remains the v1.0 default, automatic startup remains
deferred, and the Dashboard only displays backend-owned sanitized capture
status.

Review focus:
- Verify Dashboard load does not call start capture automatically.
- Verify the Dashboard Live capture tile can show the backend-led
  "Most recent completed match was recorded." line.
- Verify active capture does not invent score text, current-match result text,
  hidden-card inference, coaching, or analytics truth.
- Verify stale/blocked/unavailable states fail closed and route to Diagnostics
  without restart/recovery/reset/delete behavior.
- Verify no backend route shapes, API schemas, parser behavior, analytics
  schema/ingest, workbook/webhook/App Script/Sheets, OpenAI/AI/coaching, or
  production behavior changed.

Validation:
git status --short --branch --untracked-files=all
git diff --check
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py tools/check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed
files. If npm build creates frontend/dist, remove generated build output before
final handoff unless a later contract explicitly authorizes committing it.

Final report must include:
- role performed
- issue/tracker
- contract and implementation handoff reviewed
- files inspected
- findings first, ordered by severity
- validation run and result
- protected-surface status
- secret/private-marker status
- generated artifact status
- whether forbidden scope was touched
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/321"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md"
  target_artifact: "docs/contract_test_reports/live_app_frontend_capture_operator_workflow_refresh.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_frontend_capture_operator_workflow_refresh_comparison.md"
  risk_tier: "Medium-High if kept frontend/workflow-only; High if backend lifecycle, stale recovery, or automatic startup behavior changes are needed"
  branch: "codex/analytics-foundation"
  verdict: "frontend_workflow_refresh_ready_for_contract_review_after_full_validation"
  validation:
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run src/App.test.tsx -> passed, 57 tests"
    - "npm --prefix frontend run test -- --run -> passed, 96 tests"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  forbidden_scope_touched: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
