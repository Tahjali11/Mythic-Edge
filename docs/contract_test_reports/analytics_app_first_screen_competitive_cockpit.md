# Analytics App First-Screen Competitive Cockpit Contract Test Report

## Follow-Up After Fixer - 2026-07-16

### Verdict

No blocking findings. The dashboard status-truthfulness and action-clarity
corrective pass matches the existing frontend-only contract.

`report_lifecycle`: `followup_after_fixer`

This fixed-state confirmation does not reopen issue #278, alter its merged PR,
or authorize submission, merge, Sites publication, deployment, external
writes, backend changes, or production behavior.

### Fixed-State Finding Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-278-FIX-001 | P1 | `fixed_state_followup` | fixed_confirmed | not_blocking | `buildCockpitStatusItems` emitted `Connected` but selected detail copy by testing for `Ready`, causing a successful setup response to say that the backend needed review. | The ready render remains gated by a successful validated setup response; the App connection now says `Connected`, uses fixed reachability copy, preserves redaction warning state, and routes to Diagnostics or Privacy. Focused tests passed. | F |
| CT-278-FIX-002 | P1 | `fixed_state_followup` | fixed_confirmed | not_blocking | The Analytics database tile used only aggregate history status and collapsed loading, errors, setup gaps, degradation, and contradictory row evidence into `No history yet.` | `analyticsDatabaseCockpitSummary` now keeps setup-database status, endpoint status, returned-row evidence, and redaction evidence distinct. `Empty history` requires both endpoints to report empty with no rows; blocked endpoint severity wins over redaction degradation. Focused contradiction, empty, degraded, blocked, and redaction tests passed. | F |
| CT-278-FIX-003 | P2 | `fixed_state_followup` | fixed_confirmed | not_blocking | App connection and Analytics database rail tiles lacked the contract-required details or recovery affordance. | Both tiles now expose keyboard-focusable links to existing Diagnostics, Analytics, Import, or Privacy routes. Tests verify the contextual hrefs, and the existing mobile breakpoint stacks the footer controls. | F |

### Current Scope And Freshness

- Branch: `codex/analytics-foundation`.
- Fresh fetch result: local `HEAD` is `0` ahead and `0` behind
  `origin/codex/analytics-foundation` before these uncommitted changes.
- Issue #278 is closed; PR #279 is merged into
  `codex/analytics-foundation`; this is an explicitly requested corrective
  reentry.
- Trackers #204 and #207 are closed. Release-readiness tracker #136 remains
  open.
- No open PR currently uses `codex/analytics-foundation` as its head branch.
- The reviewed diff contains only the three frontend files and the untracked
  fixer handoff named below. This report is the only file edited by Codex E.

### Files Reviewed In The Follow-Up

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_status_truthfulness_fixer.md`
- `docs/contracts/analytics_app_first_screen_competitive_cockpit.md`
- this contract-test report

### Confirmed Contract Matches

- A successful validated setup response is treated as backend reachability;
  aggregate setup degradation no longer changes the App connection into a
  false failure.
- Setup-value redaction remains visible without falsely claiming that the
  backend connection failed, and the action routes to Privacy.
- Analytics database status does not infer source facts. It translates the
  validated setup section and validated history responses into display-only
  status, detail, and navigation.
- Available history is not described as absent when database setup reports
  missing or empty.
- A database-level empty claim plus returned rows fails closed as
  `Needs review`.
- `Empty history` is emitted only when both history endpoints report empty and
  both return no rows.
- Endpoint error, unavailable, degraded, or missing status is evaluated before
  a display-redaction warning, preventing a more serious status from being
  downgraded to generic privacy degradation.
- No backend payload shape, API route, database schema, parser interface,
  environment contract, build contract, hosting contract, or protected truth
  owner changed.

### Follow-Up Validation

```powershell
npm.cmd --prefix frontend test -- --run src/App.test.tsx src/status.test.ts
# 2 files passed; 67 tests passed

npm.cmd --prefix frontend test -- --run
# 4 files passed; 118 tests passed

npm.cmd --prefix frontend run typecheck
# passed

npm.cmd --prefix frontend run build
# passed; Sites-compatible server/client build and 5 hosting-shape tests passed

git diff --check
py tools\check_agent_docs.py
# passed

# Path-scoped protected-surface and secret/private-marker scans over the
# three frontend files, fixer handoff, and this follow-up report:
# passed; forbidden 0, warnings 0
```

`frontend/dist` and the build-touched ignored `frontend/.wrangler` helper
directory were removed after validation. No generated artifact was kept, and
no deployment or hosted resource was contacted.

### Missing Tests And Residual Risk

No blocking required test is missing. The focused suite covers the corrected
ready, setup-missing, contradictory-empty, proven-empty, degraded, blocked,
and redacted states. Loading and transport-error fallbacks were also inspected
directly in `analyticsDatabaseCockpitSummary`; existing analytics error tests
continue to pass.

Still unverified:

- Browser-level visual and responsive behavior was not exercised because this
  review did not authorize browser visual QA.
- The frontend was not run against private live app data.
- No backend process, live capture, external write, Sites publication, or
  deployment was started.

### Drift Classification

- Implementation drift: corrected; no remaining contract mismatch found.
- Repo drift: none in reviewed scope.
- Issue lifecycle: closed-issue corrective reentry, explicitly requested.
- PR lifecycle: no follow-up PR exists and none was created by this review.
- Deployment, workbook, Apps Script, live-data, and production drift: not
  inspected and not claimed.

### Follow-Up Recommendation

Approve the corrective frontend package. The next workflow role is Codex F
only after the owner directs submission packaging from a dedicated topic
branch targeting `codex/analytics-foundation`; Codex E grants no GitHub or
deployment authority.

Pasteable Codex F prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for the independently reviewed #278 closed-issue corrective reentry.

Current branch: codex/analytics-foundation
Recommended topic branch: codex/analytics-cockpit-status-truthfulness-278-followup
PR target: codex/analytics-foundation

Reviewed source artifact:
docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_status_truthfulness_fixer.md

Reviewed report:
docs/contract_test_reports/analytics_app_first_screen_competitive_cockpit.md

Stage only:
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx
- docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_status_truthfulness_fixer.md
- docs/contract_test_reports/analytics_app_first_screen_competitive_cockpit.md

Create the dedicated topic branch, reverify the exact staged package, commit,
push, and open a draft PR targeting codex/analytics-foundation. Use `Refs #278`;
do not reopen or close #278 and do not use `Closes #278`.

Do not target main, publish to Sites, deploy, merge, change implementation,
stage unrelated files, start backend/live capture, or perform external writes
beyond the explicitly requested branch push and draft PR creation.
```

### Follow-Up Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / follow-up contract-test thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/278"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  completed_thread: "E"
  next_thread: "F"
  branch: "codex/analytics-foundation"
  recommended_submitter_branch: "codex/analytics-cockpit-status-truthfulness-278-followup"
  source_artifact: "docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_status_truthfulness_fixer.md"
  target_artifact: "docs/contract_test_reports/analytics_app_first_screen_competitive_cockpit.md"
  report_lifecycle: "followup_after_fixer"
  finding_status:
    CT-278-FIX-001: "fixed_confirmed"
    CT-278-FIX-002: "fixed_confirmed"
    CT-278-FIX-003: "fixed_confirmed"
  validation:
    - "focused App/status tests -> 67 passed"
    - "full frontend tests -> 118 passed"
    - "frontend typecheck -> passed"
    - "Sites-compatible frontend build -> passed; 5 hosting-shape tests passed"
    - "git diff --check -> passed"
    - "agent docs consistency -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  deployment_authorized: false
  external_writes_authorized: false
  ready_for_codex_f: true
  next_recommended_role: "Codex F: dedicated topic-branch submitter, after owner direction"
```

## Historical Initial Review

The remainder of this report preserves the original Codex E review evidence
for the cockpit implementation merged through PR #279. Its issue status,
working-tree snapshot, validation counts, and `final_approval` lifecycle are
historical observations, not the active 2026-07-16 follow-up state.

## Findings

No blocking findings.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-278-000 | none | `not_reproduced` | no findings | not_blocking | Codex E reviewed the #278 frontend-only implementation for first-screen hierarchy, raw-label demotion, status translation, diagnostics reachability, privacy redaction, destructive controls, and protected-surface drift. | Code inspection plus frontend tests, typecheck, build, diff check, agent docs, protected-surface scan, and secret/private-marker scan passed. | F |

## Role Performed

Codex E: Module Reviewer / contract-test thread for issue #278.

## Issue Reviewed

https://github.com/Tahjali11/Mythic-Edge/issues/278

Issue status: open.

## Contract And Handoff Used

- Contract: `docs/contracts/analytics_app_first_screen_competitive_cockpit.md`
- Implementation handoff: `docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md`
- Branch: `codex/analytics-foundation`

## Report Lifecycle

`report_lifecycle`: `final_approval`

This approval is limited to the reviewed frontend-only #278 cockpit slice. It does not authorize issue closure, tracker closure, merge, production release, backend route changes, parser behavior changes, analytics schema changes, live watcher behavior changes, workbook/webhook/App Script/Sheets changes, OpenAI/AI/coaching behavior, or production behavior.

## Contract Summary

Issue #278 requires the React local app first screen to stop presenting itself as a setup/status console and instead present a competitive decision-support cockpit. The implementation must keep backend contracts and truth ownership unchanged, translate backend/internal statuses into player-facing labels, move setup grids and live diagnostics behind a details affordance, keep analytics/review value visible first, preserve privacy redaction, and avoid destructive controls or raw/private artifact exposure.

## Internal Project Area Reviewed

Local App / UI.

Adjacent areas reviewed for non-drift only:

- Analytics / SQLite local storage.
- Live Player.log status and diagnostics.
- Match Journal.
- Quality / Governance release readiness.

## Bridge-Code Status Reviewed

`bridge_code`: existing validated backend/live/analytics/journal payloads -> frontend validation and redaction -> cockpit status translation -> competitive review modules -> diagnostics/details on demand.

The implementation remains display and orchestration only. It does not move parser truth, analytics truth, live capture truth, Match Journal truth, workbook truth, production truth, or AI/coaching truth into the frontend.

## Files Reviewed

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/status.ts`
- `frontend/src/status.test.ts`
- `frontend/src/App.test.tsx`
- `docs/contracts/analytics_app_first_screen_competitive_cockpit.md`
- `docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md`
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/review.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Branch And Git Status

Branch: `codex/analytics-foundation`

Current reviewed working tree:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
 M frontend/src/App.css
 M frontend/src/App.test.tsx
 M frontend/src/App.tsx
 M frontend/src/status.test.ts
 M frontend/src/status.ts
?? docs/contracts/analytics_app_first_screen_competitive_cockpit.md
?? docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md
?? docs/contract_test_reports/analytics_app_first_screen_competitive_cockpit.md
```

No unrelated dirty files were observed.

## Confirmed Contract Matches

- Ready-state H1 is now `Mythic Edge Cockpit`, not `Setup Status`.
- The ready-state JSX order is contract-aligned:
  - cockpit header;
  - compact health/status rail;
  - competitive insight grid;
  - trust/freshness/privacy layer;
  - analytics/review sections;
  - Match Journal and manual import affordances;
  - technical details containing setup grids and live diagnostics.
- `Setup Status` and `Live Diagnostics` remain reachable through the `Show technical details` disclosure.
- Default first-screen tests assert that raw/internal labels such as `readiness_only`, `safeguards_only`, `not_capturing`, `not_running`, `start route`, `stop route`, and `ui controls` are not visible before technical details are opened.
- Raw diagnostic labels remain reachable only after opening technical details, matching the contract's progressive disclosure boundary.
- `cockpitStatusFromRawStatus(...)` translates raw/backend statuses into player-facing labels.
- `deferred`, `disabled`, `state_only`, `readiness_only`, and `safeguards_only` translate to `Limited data`, not `Ready`.
- `not_checked` and unknown statuses translate to `Needs review`, not `Ready`.
- Live capture `not_running` translates to `Waiting for Arena activity`, not `Ready`.
- Frontend tests cover hierarchy, raw-label demotion, technical details reachability, unsafe path redaction, non-destructive controls, and status translation.
- No backend route shapes, parser behavior, analytics schema/ingest behavior, live watcher behavior, Match Journal backend behavior, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior, or production behavior changed.

## Contract Mismatches

None found.

## Missing Tests Or Safeguards

No blocking missing tests or safeguards found.

Non-blocking residual risk:

- A live browser/manual smoke against a running local app was not performed in this review. The implementation handoff records that no local app instance was listening during Codex C and the launcher was not started to avoid runtime artifacts. Frontend tests and build/typecheck were used as the validation basis.

## Validation Run

```powershell
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
@'
frontend/src/App.tsx
frontend/src/App.css
frontend/src/status.ts
frontend/src/status.test.ts
frontend/src/App.test.tsx
docs/contracts/analytics_app_first_screen_competitive_cockpit.md
docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md
docs/contract_test_reports/analytics_app_first_screen_competitive_cockpit.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
frontend/src/App.tsx
frontend/src/App.css
frontend/src/status.ts
frontend/src/status.test.ts
frontend/src/App.test.tsx
docs/contracts/analytics_app_first_screen_competitive_cockpit.md
docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md
docs/contract_test_reports/analytics_app_first_screen_competitive_cockpit.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
Test-Path frontend\dist
git status --short --branch --untracked-files=all
```

Results:

- Frontend Vitest: `3 files passed`, `69 tests passed`.
- Frontend typecheck: passed.
- Frontend build: passed.
- `frontend/dist` was generated by build and removed.
- `git diff --check`: passed.
- Agent docs check: passed, `errors: 0`, `warnings: 0`.
- Path-scoped protected-surface scan: passed, `changed_paths: 8`, `forbidden: 0`, `warnings: 0`.
- Path-scoped secret/private-marker scan: passed, `scanned_paths: 8`, `forbidden: 0`, `warnings: 0`.
- `frontend/dist`: absent after cleanup.

## Protected-Surface Status

Passed. The path-scoped protected-surface scan over the touched frontend files, contract, handoff, and report returned `forbidden: 0`, `warnings: 0`.

No protected backend/parser/runtime/analytics schema/live watcher/Match Journal backend/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production files were edited.

## Secret / Private-Marker Status

Passed. The path-scoped secret/private-marker scan over the touched frontend files, contract, handoff, and report returned `forbidden: 0`, `warnings: 0`.

No raw Player.log content, raw private paths, raw hashes, secrets, generated SQLite contents, runtime artifacts, workbook exports, frontend build output, or local-only artifacts were added.

## Generated Artifact Status

`npm --prefix frontend run build` created `frontend/dist`; it was removed after validation. `frontend/dist` is absent.

## Drift Notes

- Repo drift: none found in reviewed scope.
- Backend/parser/analytics schema/live watcher/Match Journal backend drift: none found in the diff.
- Workbook/deployed Apps Script/Google Sheets/production drift: not checked and not claimed.
- Local runtime/browser drift: live browser smoke was not run; no local app runtime was started by this review.

## Recommendation

Approve the #278 frontend-only cockpit implementation and route to Codex F for submitter work.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #278.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/278

Branch:
codex/analytics-foundation

Reviewed contract:
docs/contracts/analytics_app_first_screen_competitive_cockpit.md

Reviewed implementation handoff:
docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md

Reviewed contract-test report:
docs/contract_test_reports/analytics_app_first_screen_competitive_cockpit.md

Reviewed files:
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/status.ts
- frontend/src/status.test.ts
- frontend/src/App.test.tsx
- docs/contracts/analytics_app_first_screen_competitive_cockpit.md
- docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md
- docs/contract_test_reports/analytics_app_first_screen_competitive_cockpit.md

Goal:
Submit the reviewed #278 frontend-only first-screen competitive cockpit slice. Stage only the reviewed #278 files, commit, push, and open/update a draft PR targeting codex/analytics-foundation unless current branch policy or repo state requires a different reviewed target.

Do not target main, close #278, mark trackers complete, change backend/parser/analytics schema/live watcher/Match Journal backend/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior, or add destructive controls/arbitrary SQL/database browsing.
```

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / contract-test thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/278"
  completed_thread: "E"
  next_thread: "F"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_app_first_screen_competitive_cockpit.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md"
  report_artifact: "docs/contract_test_reports/analytics_app_first_screen_competitive_cockpit.md"
  findings:
    - "No blocking findings."
  validation:
    - "npm --prefix frontend test -- --run -> 69 passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run build -> passed"
    - "frontend/dist removed after build"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
  protected_surface_status: "passed"
  secret_private_marker_status: "passed"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  remaining_risk:
    - "Live browser/manual smoke against a running local app was not performed."
  next_recommended_role: "Codex F: Module Submitter"
```
