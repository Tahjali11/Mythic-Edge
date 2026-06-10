# Live App Stale Capture Dashboard Recovery Contract Test Report

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/315
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/302
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/304
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/294

## Tracker

N/A.

## Contract

- `docs/contracts/live_app_stale_capture_dashboard_recovery.md`

## Implementation Under Test

- Worktree: `MythicEdge-stale-capture-dashboard-recovery-315`
- Branch: `codex/live-app-stale-capture-dashboard-recovery-315`
- Base branch: `origin/codex/analytics-foundation`
- Implementation handoff: `docs/implementation_handoffs/live_app_stale_capture_dashboard_recovery_comparison.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The Dashboard Live capture card must fail closed for stale or ambiguous live-capture status, keep backend capture status as lifecycle truth, avoid frontend-owned restart or recovery behavior, keep a stable lifecycle-control area, and keep a compact diagnostics affordance visible without exposing raw/private artifacts or changing backend/parser/analytics/workbook/AI/prod behavior.

## Internal Project Area Reviewed

- Primary area: Local App / UI.
- Adjacent area: Live Player.log Mode.
- Reviewed scope is frontend-only display and tests. Backend lifecycle, parser truth, analytics schema, Match Journal, workbook/webhook, Apps Script/Sheets, OpenAI/AI/coaching, Line Tracer, and production behavior were not changed.

## Bridge-Code Status Reviewed

`bridge_code`: existing backend live capture status flows into Dashboard display. The implementation keeps the frontend as a presentation layer and does not create reverse flow into parser state, live capture state, SQLite facts, workbook/webhook transport, production systems, or AI/coaching systems.

## Findings First

No blocking findings.

## Checks Run

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
git diff --name-status origin/codex/analytics-foundation...HEAD
gh issue view 315 --repo Tahjali11/Mythic-Edge --json number,title,state,url
git diff --check
py tools\check_agent_docs.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
```

Path-scoped protected-surface and secret/private-marker scans were run over:

- `docs/contracts/live_app_stale_capture_dashboard_recovery.md`
- `docs/implementation_handoffs/live_app_stale_capture_dashboard_recovery_comparison.md`
- `docs/contract_test_reports/live_app_stale_capture_dashboard_recovery.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

## Results

- Branch confirmed: `codex/live-app-stale-capture-dashboard-recovery-315`.
- Branch sync: `0 0` against `origin/codex/analytics-foundation`.
- Issue #315 state: open.
- `git diff --name-status origin/codex/analytics-foundation...HEAD` showed no committed branch diff because the #315 package is active as uncommitted worktree changes. `git status --short --branch --untracked-files=all` showed the reviewed package files.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed, 47 files checked, errors 0, warnings 0.
- `npm --prefix frontend ci` -> passed, 113 packages installed, 0 vulnerabilities.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> passed, 3 files and 95 tests.
- `npm --prefix frontend run build` -> passed.
- Generated `frontend/dist` was removed after build validation.
- Temporary `frontend/node_modules` was removed after validation.
- Path-scoped protected-surface scan -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| N/A | N/A | N/A | no findings | not_blocking | N/A | Contract review plus focused frontend validation found no blocking mismatch. | F |

## Confirmed Contract Matches

- Stale `status=stale` with `state.stale=true`, `running=false`, `start_allowed=false`, `stop_allowed=false`, `reason=capture_state_stale`, and restart-implying backend blurb no longer renders `Ready to start`, `Start capture`, `Stop capture`, or restart copy on the Dashboard.
- Stale Dashboard display renders `Needs review`, safe compact copy, a disabled lifecycle control, and a diagnostics link to `#diagnostics`.
- Ready/stopped status still exposes `Start capture` only when backend status and `start_allowed=true` support it.
- Capturing status still exposes `Stop capture` only when backend status, `running=true`, and `stop_allowed=true` support it.
- Unavailable and contradictory states fail closed with no Start/Stop action and keep diagnostics reachable.
- The diagnostics affordance is separate from the lifecycle control, accessible by label, and does not start, stop, reset, restart, repair, delete, upload, inspect private files, or browse data.
- The implementation is frontend-only: no backend route shapes, backend lifecycle semantics, parser behavior, analytics schema/ingest, #302 diagnostics, #294 auto-refresh, Match Journal behavior, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior, Line Tracer behavior, or production behavior changed.
- No raw Player.log contents, raw JSONL, raw private paths, raw hashes, SQL text, SQLite contents, secrets, environment values, runtime artifacts, workbook exports, or local-only artifacts are rendered by the changed Dashboard path.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests found.

The focused frontend tests cover the required stale fail-closed case, Start/Stop preservation for safe backend states, diagnostics reachability, unavailable/error behavior, and contradictory capture status regression paths. Browser visual smoke was not run by this review; this is a non-blocking residual risk for layout polish.

## Drift Notes

- Repository drift: none found in reviewed scope.
- Branch/package status: the #315 branch is 0/0 with `origin/codex/analytics-foundation`, and the package is active as dirty/untracked worktree changes ready for Codex F staging.
- Workbook/deployment/local-data drift: not applicable to this frontend-only review.

## Protected-Surface Status

Passed. Path-scoped protected-surface scan over the reviewed #315 files reported forbidden 0 and warnings 0.

## Secret And Private-Marker Status

Passed. Path-scoped secret/private-marker scan over the reviewed #315 files reported forbidden 0 and warnings 0.

## Generated/Private Artifact Status

- `frontend/dist` removed after build validation.
- `frontend/node_modules` removed after validation.
- No generated/private/local artifacts were kept in Git status.

## Forbidden Scope

Forbidden scope touched: false.

## Recommendation

Approve for Codex F. Stage only the reviewed #315 files and open/update the draft PR to `codex/analytics-foundation`.

## Next Workflow Action

Next role: Codex F / Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #315.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/315

Branch:
codex/live-app-stale-capture-dashboard-recovery-315

Base branch:
origin/codex/analytics-foundation

Contract:
docs/contracts/live_app_stale_capture_dashboard_recovery.md

Implementation handoff:
docs/implementation_handoffs/live_app_stale_capture_dashboard_recovery_comparison.md

Review artifact:
docs/contract_test_reports/live_app_stale_capture_dashboard_recovery.md

Goal:
Submit the reviewed #315 frontend-only Dashboard stale capture recovery package. Stage only reviewed #315 files, commit, push, and open or update a draft PR targeting codex/analytics-foundation. Do not merge or close issues.

Files approved for staging:
- docs/contracts/live_app_stale_capture_dashboard_recovery.md
- docs/implementation_handoffs/live_app_stale_capture_dashboard_recovery_comparison.md
- docs/contract_test_reports/live_app_stale_capture_dashboard_recovery.md
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx

Before staging:
- Confirm branch and git status.
- Confirm no generated frontend/dist or frontend/node_modules are kept.
- Confirm no unrelated dirty files are staged.

Suggested validation before commit:
- npm --prefix frontend ci
- npm --prefix frontend run typecheck
- npm --prefix frontend run test -- --run
- npm --prefix frontend run build
- remove frontend/dist and frontend/node_modules after validation
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface and secret/private-marker scans over staged files

Do not:
- edit implementation unless explicitly asked
- stage unrelated files
- start, stop, restart, tail, or control a real live watcher
- read, copy, hash, summarize, store, or expose raw Player.log contents
- change backend route shapes, parser behavior, analytics schema/ingest, live watcher behavior, Match Journal backend behavior, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior, Line Tracer behavior, or production behavior
- target main, merge, close issue #315, or mark trackers complete

Final output:
- role performed
- branch and target branch
- files staged
- commit hash
- PR URL
- validation run and result
- protected-surface status
- secret/private-marker status
- generated artifact status
- remaining risk
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/315"
  completed_thread: "E"
  next_thread: "F"
  worktree: "MythicEdge-stale-capture-dashboard-recovery-315"
  branch: "codex/live-app-stale-capture-dashboard-recovery-315"
  base_branch: "origin/codex/analytics-foundation"
  contract_artifact: "docs/contracts/live_app_stale_capture_dashboard_recovery.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_stale_capture_dashboard_recovery_comparison.md"
  review_artifact: "docs/contract_test_reports/live_app_stale_capture_dashboard_recovery.md"
  risk_tier: "Medium frontend-only; High if backend lifecycle or recovery behavior changes are needed"
  findings: []
  validation:
    - "git status --short --branch --untracked-files=all -> reviewed #315 dirty/untracked package"
    - "git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "npm --prefix frontend ci -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> passed, 3 files, 95 tests"
    - "npm --prefix frontend run build -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  recommendation: "Route to Codex F."
```
