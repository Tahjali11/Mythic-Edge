# Analytics App Frontend Information Architecture Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/299

## Tracker

N/A. The contract treats issues #204 and #207 as historical closed context for this slice.

## Contract

`docs/contracts/analytics_app_frontend_information_architecture.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Reviewed changed-path set:

- `docs/contracts/analytics_app_frontend_information_architecture.md`
- `docs/contract_test_reports/analytics_app_frontend_information_architecture.md`
- `docs/implementation_handoffs/analytics_app_frontend_information_architecture_comparison.md`
- `docs/implementation_handoffs/analytics_app_frontend_information_architecture_fixer.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/types.ts`

Adjacent dirty paths remain from #297 live-capture and #281/#298 error-report work. They were inspected only where they affected validation or submitter package ordering.

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The frontend should behave like a route-gated local competitive cockpit instead of one long technical page. The frontend owns navigation state, layout, display hierarchy, panel visibility, and user-facing status translation only. Parser truth, analytics truth, live-capture semantics, Match Journal truth, backend route contracts, workbook/webhook/App Script/Sheets behavior, GitHub submission authority, OpenAI/AI/coaching behavior, and production behavior remain outside this frontend information-architecture slice.

Required routes are Dashboard, Coach, Analytics, Review, Privacy, Feedback, Import, and Diagnostics. Dashboard must stay compact; deeper analytics, Match Journal review, manual import, diagnostics, privacy details, and feedback must remain reachable without dominating the first screen.

## Internal Project Area Reviewed

Local App / UI.

No internal project boundary mismatch was found in the route/display implementation or the D follow-up validator fix.

## Bridge-Code Status Reviewed

`bridge_code`

The frontend consumes existing local backend responses and displays them. The reviewed #299 route state does not flow back into parser facts, analytics facts, live-capture truth, Match Journal records, GitHub, workbook, AI, or production surfaces.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-299-001 | P1 | `fixed_state_followup` | fixed | not_blocking | Initial review found the dirty worktree was not submitter-ready because the full frontend suite failed in `frontend/src/api.test.ts`; `fetchLiveWatcherStatus(...)` accepted a readiness-only watcher payload that claimed running/parser/tailing/SQLite-write activity. | Codex D tightened the watcher validator and type shape to require readiness-only activity fields to be `false`. `npm --prefix frontend test -- --run src/api.test.ts` passed in the D handoff, and this E confirmation reran the full frontend suite: 3 files, 86 tests passed. | F |
| CT-299-002 | P3 | `fixed_state_followup` | fixed | not_blocking | Initial review left browser/mobile visual smoke unverified. | This E confirmation ran privacy-safe headless Edge smoke against `http://127.0.0.1:5173/`: desktop screenshots for dashboard, analytics, review, feedback, privacy, diagnostics, and import, plus a narrow mobile dashboard screenshot. All screenshots were created with expected dimensions, nonzero byte sizes, and nonblank pixel samples, then removed. | F |

No blocking findings remain.

## Confirmed Contract Matches

- Route model includes Dashboard, Coach, Analytics, Review, Privacy, Feedback, Import, and Diagnostics.
- Unknown hash routes fall back safely to Dashboard.
- Left rail exposes the required modes, including Privacy in the footer.
- Active state is visible and programmatic through `aria-current="page"` plus a visible `Current` marker.
- Dashboard renders as a compact cockpit: status rail, explicit live-capture control, Decision Support modules, AI Coach boundary, route cards, and trust/privacy summary.
- Analytics, Review, Feedback, Import, Privacy, Diagnostics, and Coach content is route-gated rather than rendered as one long default page.
- Dashboard keeps technical details collapsed behind a disclosure control; Diagnostics route exposes the technical view directly.
- Feedback remains preview/copy/local only and does not expose live GitHub issue creation or external submission controls.
- AI Coach remains pending/boundary-only and does not claim model-provider runtime support.
- Match Journal review remains in the Review route and does not claim parser truth ownership.
- Manual import remains in the Import route and does not show raw JSONL payloads or raw path details in the dashboard-first flow.
- Tests cover route visibility, hidden/moved sections, active rail state, unknown route fallback, dashboard priorities, feedback access, privacy/forbidden controls, and absence of destructive SQL/database/coaching controls.
- #297 live-capture labels remain explicit that capture must be started before new games are added to SQLite.
- `fetchLiveWatcherStatus` now rejects readiness-only watcher payloads that claim active watcher/parser/tailing/SQLite-write activity.

## Contract Mismatches

None remaining.

## Missing Tests Or Safeguards

No blocking #299 test gap remains.

Manual visual review in the user's real browser and full repository pytest remain unverified, but they are not required blockers for this frontend-only confirmation.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
git diff --name-status
gh issue view 299 --json number,state,title,url,labels
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run
npm --prefix frontend run build
py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py tests\test_live_app_parser_owned_fact_capture_sqlite.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over the #299 package
path-scoped secret/private-marker scan over the #299 package
privacy-safe headless Edge route/mobile screenshot smoke
```

Results:

- Issue #299: open.
- Branch: `codex/analytics-foundation`, even with `origin/codex/analytics-foundation`.
- `npm --prefix frontend run typecheck`: passed.
- `npm --prefix frontend test -- --run`: passed, 3 files, 86 tests.
- `npm --prefix frontend run build`: passed; generated `frontend/dist` was removed.
- Focused adjacent backend/live pytest: passed, 44 tests, 1 existing FastAPI/Starlette deprecation warning.
- `py -m ruff check src tests tools`: passed.
- `git diff --check`: passed.
- `py tools\check_agent_docs.py`: passed, 46 files checked, 0 errors, 0 warnings.
- Path-scoped protected-surface scan over 10 #299 package paths: passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over 10 #299 package paths: passed, forbidden 0, warnings 0.
- Browser/mobile smoke: passed in headless Edge. Desktop route screenshots for dashboard, analytics, review, feedback, privacy, diagnostics, and import were created; narrow mobile dashboard screenshot was created. Screenshot artifacts were temporary and removed.
- `frontend/dist`: absent after cleanup.

## Protected-Surface Status

Path-scoped protected-surface scan passed with forbidden 0 and warnings 0.

No reviewed evidence showed changes to parser behavior, parser state final reconciliation, analytics schema/migrations/ingest, live-capture semantics beyond adjacent already-reviewed #297 frontend/backend work, Match Journal truth ownership, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, hidden-card inference, archetype inference, player-mistake labels, best-line advice, or gameplay advice.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan passed with forbidden 0 and warnings 0.

The browser smoke did not inspect real Player.log contents, private app-data, raw JSONL, SQLite contents, workbook exports, runtime files, secrets, endpoints, credentials, environment values, or local-only artifacts.

## Generated Artifact Status

`frontend/dist` was created by build validation and removed. Temporary headless Edge screenshots and profiles were removed. No generated SQLite database, raw Player.log, app-data file, runtime artifact, workbook export, screenshot artifact, or local-only artifact was intentionally retained in the repo by this review.

## Package-Ordering Recommendation

The combined #297/#299 frontend package is validation-clean now. Because #299 app-shell work and #297 explicit live-capture control share frontend files, Codex F should avoid pretending this is an isolated #299-only package unless it can stage a clean isolated diff.

Recommended Codex F posture:

- Prefer a deliberately combined #297/#299 PR/package if the staged diff necessarily includes shared `frontend/src/App.tsx`, `frontend/src/App.css`, `frontend/src/App.test.tsx`, `frontend/src/api.ts`, `frontend/src/api.test.ts`, and `frontend/src/types.ts` changes.
- Reference both durable review artifacts:
  - `docs/contract_test_reports/live_app_explicit_start_capture_control.md`
  - `docs/contract_test_reports/analytics_app_frontend_information_architecture.md`
- Leave unrelated #281/#298 error-report contract/source files unstaged unless a separate reviewed package explicitly authorizes including them.
- If a standalone #299 PR is required, isolate it on a clean branch after #297 is submitted or merged, then rerun validation.

## Drift Notes

- Repo/local worktree drift: dirty files from #299, #297, and #281/#298 remain in the same checkout.
- Issue lifecycle: #299 is open.
- PR lifecycle: no #299 PR was inspected or changed in this review.
- Deployment/workbook/live external state: not inspected.

## Forbidden Scope

Forbidden scope was not touched by this Codex E review. No implementation files were edited, no real watcher was started or stopped, no real/private Player.log content was read, copied, hashed, summarized, or exposed, no live GitHub issue submission was run, and no staging, commit, push, PR, merge, issue closure, or main-targeting action was performed.

## Recommendation

Approve for Codex F with package-ordering caution. Route to Codex F to stage only reviewed #297/#299 files, or isolate #299 after #297 if a standalone package is required.

## Next Workflow Action

Next role: Codex F / Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for the reviewed #297/#299 local app frontend package.

Issues:
- #297: https://github.com/Tahjali11/Mythic-Edge/issues/297
- #299: https://github.com/Tahjali11/Mythic-Edge/issues/299

Branch:
codex/analytics-foundation

Review artifacts:
- docs/contract_test_reports/live_app_explicit_start_capture_control.md
- docs/contract_test_reports/analytics_app_frontend_information_architecture.md

Goal:
Prepare a draft PR for the reviewed package only. Stage only reviewed #297/#299 files. Do not stage unrelated #281/#298 error-report contract/source files unless a separate reviewed artifact authorizes them.

Before staging:
- Confirm branch and git status.
- Inspect dirty files and classify #297/#299 versus unrelated #281/#298 work.
- Confirm validation remains green or rerun the focused validation below.

Suggested validation:
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run
npm --prefix frontend run build
py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py tests\test_live_app_parser_owned_fact_capture_sqlite.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over staged files.
Remove frontend/dist after build validation if created.

Do not:
- stage unrelated error-report files or other unreviewed dirty files
- target main
- close #297 or #299
- merge, deploy, or change production behavior
- change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior
- expose raw/private/generated/local artifacts

Final output:
- role performed
- issues included
- files staged
- commit hash
- draft PR URL and target branch
- validation run
- protected-surface and secret/private-marker status
- generated artifact status
- remaining risk
- workflow_handoff block routing to Codex G
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/299"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/297"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/analytics_app_frontend_information_architecture.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_app_frontend_information_architecture_fixer.md"
  target_artifact: "docs/contract_test_reports/analytics_app_frontend_information_architecture.md"
  branch: "codex/analytics-foundation"
  fixed_findings_confirmed:
    - "CT-299-001 P1: full frontend suite passes; readiness-only watcher payloads claiming active watcher/parser/tailing/SQLite-write activity are rejected."
    - "CT-299-002 P3: privacy-safe headless Edge desktop/mobile visual smoke was run and passed; temporary screenshots removed."
  validation:
    - "frontend typecheck -> passed"
    - "frontend tests -> passed, 86 passed"
    - "frontend build -> passed; frontend/dist removed"
    - "focused adjacent backend/live pytest -> passed, 44 passed, 1 existing warning"
    - "ruff -> passed"
    - "git diff --check -> passed"
    - "agent docs -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "headless Edge visual smoke -> passed for desktop routes and mobile dashboard"
  package_ordering: "Prefer combined reviewed #297/#299 package unless #299 can be isolated cleanly after #297; leave unrelated #281/#298 files unstaged."
  protected_surface_status: "passed"
  secret_private_marker_status: "passed"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter"
```
