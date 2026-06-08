# Analytics App Frontend Information Architecture Layout Polish Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/299

Issue lifecycle status during this review: closed. This is a follow-on polish artifact. No issue lifecycle action was taken.

## Tracker

N/A. The #299 contract treats issues #204 and #207 as historical context for this work.

## Contract

`docs/contracts/analytics_app_frontend_information_architecture.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Implementation handoff:

- `docs/implementation_handoffs/analytics_app_frontend_information_architecture_layout_polish_comparison.md`

Reviewed focused slices:

- compact left rail
- stable active navigation state
- aligned dashboard status badges
- frontend-only Dashboard density pass

Reviewed files:

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_app_frontend_information_architecture_layout_polish_comparison.md`
- `docs/contracts/analytics_app_frontend_information_architecture.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The frontend may polish route display state, navigation layout, active-state styling, Dashboard density, and status badge placement only. It must keep the local app cockpit useful, readable, and truthful without changing backend route shapes, parser behavior, analytics schema or ingest, live watcher behavior, Match Journal backend behavior, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior, Line Tracer behavior, or production behavior.

## Internal Project Area Reviewed

Local App / UI.

## Bridge-Code Status Reviewed

`bridge_code`

This slice remains a frontend display bridge over existing backend/status data. The reviewed changes do not write route state, layout state, or visual badge state back into parser, analytics, live capture, Match Journal, workbook, AI, or production surfaces.

## Findings First

No blocking findings.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-299-LP-001 | none | `not_reproduced` | no blocking layout-polish mismatch found | not_blocking | Review requested verification of compact rail grouping, stable active state, and dashboard badge alignment for the focused #299 layout-polish slice. | Source review, full frontend validation, desktop browser DOM/layout smoke, and 390px mobile-width browser DOM/layout smoke found the focused rail/status polish consistent with the contract and handoff. | F |
| CT-299-DP-001 | none | `not_reproduced` | no blocking Dashboard density mismatch found | not_blocking | Follow-on Codex C density pass removed the dashboard header status badge, reduced the default dashboard status row to three cards, shortened tile copy, and pinned card badges bottom-left. | Source review, focused tests, full frontend validation, desktop browser DOM/layout smoke, and 390px mobile-width browser DOM/layout smoke found the density pass readable and consistent with the contract. | F |

## Confirmed Contract Matches

- `frontend/src/App.tsx` keeps the route model frontend-only and keeps `Privacy` in the primary rail group with Dashboard, Coach, Analytics, Review, Feedback, Import, and Diagnostics.
- The active rail item still exposes `aria-current="page"`.
- The active `Current` text pill remains removed, avoiding active/inactive item shape changes.
- `frontend/src/App.css` uses stable rail link dimensions and a compact active pseudo-element indicator.
- The Dashboard header no longer renders a top-right status pill.
- The default Dashboard health row now renders exactly three cards: App connection, Live capture, and Analytics database.
- Player.log monitor and Data trust are no longer permanent health-row cards, but their owning details remain reachable through Diagnostics and Privacy/Trust surfaces.
- The Live capture card keeps status distinctions via the status pill, including Stopped, Ready to start, Capturing, Blocked, Setup needed, Unavailable, and Needs review.
- The implementation preserves the deeper Dashboard sections: Decision Support, Coach boundary, route cards, Trust and Freshness, and Technical Details.
- Unknown, deferred, degraded, unavailable, not-running, and capture states remain governed by existing status translation logic; this density pass did not turn them into Ready or Capturing.
- Desktop browser smoke measured all eight rail links at 38px height, with the active dot rendered as 7px by 7px.
- Desktop browser smoke measured three Dashboard health cards, no Dashboard header status pill, no title/status overlap, and no horizontal overflow.
- Mobile-width browser smoke at 390px measured all eight rail links at 38px height with no rail link overflow, three stacked health cards, no title/status overlap, and no horizontal overflow.
- Existing dashboard and route content remains reachable.
- No destructive controls, arbitrary SQL/database browsing, raw Player.log display, raw private paths, raw hashes, secrets, generated SQLite contents, runtime artifacts, workbook exports, or local-only artifact exposure was introduced.
- No backend or protected production-facing surfaces were changed.

## Contract Mismatches

None found.

## Missing Tests Or Safeguards

No blocking missing test was found.

Focused tests now assert:

- Privacy is in the primary nav.
- The `Current` pill is absent.
- The Dashboard header no longer has a status pill.
- The Dashboard health row has exactly three cards.
- Player.log monitor and Data trust are absent from the default health row.
- Live capture compact copy remains status-specific.

CSS dimensions and badge alignment are not directly asserted in Vitest/JSDOM. This review covered that visual risk with read-only browser DOM/layout smoke at desktop and 390px mobile width.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
git diff --name-status
gh issue view 299 --repo Tahjali11/Mythic-Edge --json number,title,state,url
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
Remove generated frontend/dist
git diff --check
py tools\check_agent_docs.py
Browser DOM/layout smoke at http://127.0.0.1:5173/#dashboard
Path-scoped protected-surface scan over reviewed files
Path-scoped secret/private-marker scan over reviewed files
```

Results:

- Branch/status: `codex/analytics-foundation...origin/codex/analytics-foundation`.
- Dirty files before report update: `frontend/src/App.css`, `frontend/src/App.test.tsx`, `frontend/src/App.tsx`, and untracked layout-polish implementation handoff/report.
- Unrelated untracked docs observed and left untouched:
  - `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`
  - `docs/problem_representations/setup_app_private_local_v1_installation_wizard_prompt.md`
- `git diff --name-status`: frontend-only code/test diff before report update.
- Issue #299: closed.
- `npm --prefix frontend run typecheck`: passed.
- `npm --prefix frontend run test -- --run`: passed, 3 files, 86 tests.
- `npm --prefix frontend run build`: passed.
- `frontend/dist`: removed after build validation.
- `git diff --check`: passed.
- `py tools\check_agent_docs.py`: passed, 46 files checked, 0 errors, 0 warnings.
- Browser desktop DOM/layout smoke: passed; all 8 primary rail links present, active Dashboard link had `aria-current="page"`, no `Current` text was visible, active dot measured 7px by 7px, the Dashboard header had 0 status pills, the Dashboard health row had exactly 3 cards, no health-card title/status overlap was measured, and no horizontal overflow was measured.
- Browser mobile-width DOM/layout smoke at 390px: passed; all 8 primary rail links present, all rail links measured 38px high, no rail link overflow was measured, the Dashboard header had 0 status pills, the Dashboard health row had exactly 3 stacked cards, no health-card title/status overlap was measured, and no horizontal overflow was measured.

## Protected-Surface Status

Path-scoped protected-surface scan status: passed, forbidden 0, warnings 0.

No reviewed evidence showed changes to backend route shapes, parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest, live watcher behavior, Match Journal backend behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, or production behavior.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan status: passed, forbidden 0, warnings 0.

No raw Player.log content, raw JSONL payloads, SQLite contents, raw private paths, raw hashes, secrets, endpoint values, environment values, generated artifacts, runtime logs, workbook exports, or local-only artifacts were exposed by the reviewed diff or browser smoke output.

## Generated Artifact Status

`frontend/dist` was created by build validation and removed. No generated build output, SQLite database, raw log, runtime artifact, workbook export, app-data file, or local-only artifact was intentionally retained.

## Browser And Visual Smoke Status

Desktop browser DOM/layout smoke passed against `http://127.0.0.1:5173/#dashboard`.

Mobile-width browser DOM/layout smoke passed at 390px.

The smoke checked DOM/layout measurements rather than saving screenshots, so no screenshot artifact cleanup was required.

## Remaining Risk

Mobile still requires scrolling to see all three health cards because the rail remains visible above the Dashboard content. This is not a blocking mismatch for this density pass because the cards are readable, stacked cleanly, and do not overlap or overflow at 390px.

## Drift Notes

- Issue lifecycle drift: issue #299 is already closed while this follow-on polish remains in the local worktree.
- Repo/worktree state: the focused frontend files and layout-polish handoff/report are dirty or untracked until Codex F stages them intentionally.
- Unrelated untracked docs were present and ignored.
- No workbook, deployment, live watcher, private app-data, or production state was inspected or changed.

## Forbidden Scope

Forbidden scope was not touched by this Codex E review. No implementation files were edited, no watcher was started or stopped, no raw Player.log or private app-data was read, no external submission was run, and no staging, commit, push, PR, merge, issue closure, tracker update, main-targeting, or production-facing action was performed.

## Recommendation

Approve this focused layout-polish and Dashboard density slice for Codex F.

Codex F should stage only the reviewed frontend files plus the layout-polish handoff and this contract-test report. Because #299 is already closed, F/G should use issue-linking wording that reflects this as a follow-on polish artifact rather than re-closing #299.

## Next Workflow Action

Next role: Codex F / Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for the focused #299 frontend layout-polish and Dashboard density slice.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/299

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_frontend_information_architecture.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_frontend_information_architecture_layout_polish_comparison.md

Review artifact:
docs/contract_test_reports/analytics_app_frontend_information_architecture_layout_polish.md

Reviewed files:
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx
- docs/implementation_handoffs/analytics_app_frontend_information_architecture_layout_polish_comparison.md
- docs/contract_test_reports/analytics_app_frontend_information_architecture_layout_polish.md

Goal:
Stage only the reviewed #299 layout-polish/Dashboard-density files, commit them, push a branch, and open a draft PR to codex/analytics-foundation. Since issue #299 is already closed, do not use closing keywords; use Refs #299.

Suggested validation before commit:
- git status --short --branch --untracked-files=all
- npm --prefix frontend run typecheck
- npm --prefix frontend run test -- --run
- npm --prefix frontend run build
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over staged files
- path-scoped secret/private-marker scan over staged files
- remove frontend/dist after build validation if created

Do not:
- stage unrelated files
- target main
- close issue #299 or mark trackers complete
- change backend route shapes, parser behavior, analytics schema/ingest, live watcher behavior, Match Journal backend behavior, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior, Line Tracer behavior, or production behavior
- expose raw/private/generated/local artifacts

Final output:
- role performed
- files staged
- commit hash
- draft PR URL and target branch
- validation run and result
- protected-surface and secret/private-marker status
- generated artifact status
- remaining risk
- workflow_handoff block routing to Codex G
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/299"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/analytics_app_frontend_information_architecture.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_app_frontend_information_architecture_layout_polish_comparison.md"
  target_artifact: "docs/contract_test_reports/analytics_app_frontend_information_architecture_layout_polish.md"
  focused_slice: "compact left rail, stable active nav state, aligned dashboard status badges, Dashboard density"
  risk_tier: "Low-to-medium frontend-only"
  branch: "codex/analytics-foundation"
  findings:
    - "No blocking findings."
  validation:
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> passed, 3 files, 86 tests"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "desktop browser DOM/layout smoke -> passed"
    - "390px mobile-width browser DOM/layout smoke -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  protected_surface_status: "passed"
  secret_private_marker_status: "passed"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter"
```
