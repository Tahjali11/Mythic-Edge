# Frontend Analytics Auto-Refresh State Decomposition Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/706>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>

## Contract

`docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md`

## Role Performed

Codex C: Module Implementer.

## Scope And Boundary

Authorized slice: `frontend_analytics_auto_refresh_state` behind the existing
`frontend/src/App.tsx` facade.

This pass preserved the route/hash vocabulary, dashboard rendering behavior,
analytics auto-refresh cadence, refresh-state fetch semantics, revision
comparison semantics, visibility-pause behavior, in-flight guard behavior,
manual refresh behavior, API payload shape, backend routes, parser behavior,
workbook/webhook/App Script behavior, CI behavior, and all readiness/truth/
assurance non-claims.

## What Changed

- Extracted the analytics auto-refresh state machine, interval orchestration,
  visibility listener, revision tracking, in-flight guard, checked-at formatter,
  and public-safe notice component into `frontend/src/app_analytics_auto_refresh.tsx`.
- Kept `frontend/src/App.tsx` as the public facade and the only owner of the
  existing analytics view state updates.
- Added a callback bridge so the extracted hook can still honor the old
  active-effect cleanup guard before asynchronous analytics view reloads set
  React state.
- Added focused helper tests for immediate checking, 25-second cadence,
  unchanged revisions, changed revision reload, hidden-tab pause, and
  visible-tab immediate recheck.

## Files Changed

- `frontend/src/App.tsx`
- `frontend/src/app_analytics_auto_refresh.tsx`
- `frontend/src/app_analytics_auto_refresh.test.tsx`
- `docs/implementation_handoffs/core_frontend_app_shell_analytics_auto_refresh_state_decomposition_comparison.md`

## Interface Changes

No public interface changes.

Preserved:

- `frontend/src/App.tsx` import path
- named `SetupStatusApp` export
- default `SetupStatusApp` export
- `SetupStatusAppProps`
- accepted route/hash values and fallback behavior
- existing analytics refresh API dependency injection
- rendered auto-refresh notice label and copy

New private same-repo helper surface:

- `useAnalyticsAutoRefreshState`
- `AnalyticsAutoRefreshNotice`
- `AnalyticsAutoRefreshState`
- `AutoRefreshActiveCheck`

These helpers are internal to the frontend package and do not change API,
backend, parser, workbook, webhook, Apps Script, or CI contracts.

## Behavior Preservation Evidence

- `ANALYTICS_AUTO_REFRESH_INTERVAL_MS` remains `25_000`.
- Initial hook state remains `checking` with `checkedAt: null`.
- Safe refresh statuses remain `ok` and `empty`.
- Changed non-null revisions still reload all existing analytics views exactly
  once through the App-owned callback.
- Unchanged revisions do not reload analytics views.
- Hidden document state still pauses without fetching refresh state.
- Returning visible still triggers an immediate check.
- Degraded check/fetch paths still show the same public-safe manual-refresh
  fallback messages.
- The existing `App.test.tsx` auto-refresh scenario still passes.

## Validation Run

```bash
npm --prefix frontend ci
npm --prefix frontend test -- --run src/app_analytics_auto_refresh.test.tsx
npm --prefix frontend test -- --run src/App.test.tsx
npm --prefix frontend test -- --run src/App.test.tsx src/api.test.ts
npm --prefix frontend run typecheck
npm --prefix frontend run build
printf '%s\n' frontend/src/App.tsx frontend/src/app_analytics_auto_refresh.tsx frontend/src/app_analytics_auto_refresh.test.tsx | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' frontend/src/App.tsx frontend/src/app_analytics_auto_refresh.tsx frontend/src/app_analytics_auto_refresh.test.tsx | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main
npm --prefix frontend test -- --run src/app_analytics_auto_refresh.test.tsx src/App.test.tsx src/api.test.ts
git diff --check
python3 changed-frontend-file-whitespace-check
```

Results:

- `npm --prefix frontend ci`: passed; npm audit reported existing dependency
  advisory findings, not fixed in this decomposition scope.
- Focused helper tests: 3 passed.
- Existing App facade tests: 57 passed.
- App/API combined tests: 96 passed.
- Final helper/App/API combined tests: 99 passed.
- Frontend typecheck: passed.
- Frontend build: passed.
- Path-scoped secret/private marker scan over changed frontend files: passed.
- Path-scoped protected-surface scan over changed frontend files: passed.
- `python3 tools/check_secret_patterns.py --all`: failed on pre-existing
  unrelated repository findings outside this changed frontend slice.
- `python3 tools/check_protected_surfaces.py --base origin/main`: passed with
  no changed paths reported because the tool compares committed refs; the
  path-scoped protected-surface scan above covered the unstaged changed files.
- `git diff --check`: passed.
- Direct whitespace/final-newline check over changed frontend files: passed.

## Still Unverified

- No browser/manual smoke was run.
- No live backend, live capture, workbook, webhook, Apps Script, parser, or
  production behavior was exercised.
- The repo-wide secret scan still has legacy findings outside this slice; this
  implementation relies on the passing path-scoped scan for changed files.

## Reviewer Focus

- Confirm the extracted hook preserves the old effect order, active cleanup
  guard, in-flight guard, revision comparison, visibility pause, and 25-second
  cadence.
- Confirm `frontend/src/App.tsx` remains the public facade and still owns the
  actual analytics view state updates.
- Confirm no route/hash, dashboard rendering, API payload, backend route,
  parser, workbook/webhook, Apps Script, CI, readiness, truth, or assurance
  boundary changed.

## Next Workflow Action

Next role: Codex E.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Reviewer for Mythic Edge issue #706.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/706

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Contract:
docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md

Implementation handoff:
docs/implementation_handoffs/core_frontend_app_shell_analytics_auto_refresh_state_decomposition_comparison.md

Review the behavior-preserving same-repo extraction for frontend_analytics_auto_refresh_state. Lead with findings. Verify that the extracted helper preserves App.tsx as the facade, keeps the 25-second cadence, revision comparison, visibility-pause behavior, in-flight guard, active cleanup guard, public-safe notice copy, and all existing analytics view reload behavior. Confirm no frontend behavior, route/hash behavior, dashboard rendering behavior, API payload behavior, live-capture behavior, backend route behavior, parser behavior, workbook/webhook/App Script behavior, CI behavior, readiness claim, truth claim, or assurance claim changed.

Validation evidence to review:
- npm --prefix frontend test -- --run src/app_analytics_auto_refresh.test.tsx src/App.test.tsx src/api.test.ts
- npm --prefix frontend run typecheck
- npm --prefix frontend run build
- path-scoped secret/private marker scan for changed frontend files
- path-scoped protected-surface scan for changed frontend files
- git diff --check

Expected output:
Findings first, verdict, validation reviewed, remaining risk, recommended next role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/706"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  source_decision_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/697"
  completed_thread: "C"
  next_thread: "E"
  verdict: "frontend_analytics_auto_refresh_state_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/frontend-analytics-auto-refresh-state-706"
  source_artifact: "docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md"
  target_artifact: "docs/implementation_handoffs/core_frontend_app_shell_analytics_auto_refresh_state_decomposition_comparison.md"
  candidate_id: "frontend_analytics_auto_refresh_state"
  candidate_surface: "frontend/src/App.tsx"
  implementation_scope: "behavior_preserving_same_repo_private_helper_hook_extraction"
  frontend_behavior_change_authorized: false
  route_hash_behavior_change_authorized: false
  dashboard_rendering_change_authorized: false
  analytics_auto_refresh_cadence_change_authorized: false
  analytics_refresh_fetch_semantics_change_authorized: false
  analytics_revision_handling_change_authorized: false
  visibility_pause_behavior_change_authorized: false
  api_payload_change_authorized: false
  live_capture_behavior_change_authorized: false
  backend_route_change_authorized: false
  parser_behavior_change_authorized: false
  workbook_webhook_change_authorized: false
  apps_script_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
  analytics_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  validation:
    - "npm --prefix frontend test -- --run src/app_analytics_auto_refresh.test.tsx src/App.test.tsx src/api.test.ts -> 99 passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run build -> passed"
    - "path-scoped secret/private marker scan over changed frontend files -> passed"
    - "path-scoped protected-surface scan over changed frontend files -> passed"
    - "git diff --check -> passed"
```
