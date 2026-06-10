# Analytics App Frontend Information Architecture Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/299

## Tracker

N/A. The contract identifies issues #204 and #207 as closed historical context.

## Contract

`docs/contracts/analytics_app_frontend_information_architecture.md`

## Internal Project Area

Local App / UI.

## Truth Owner

The frontend owns navigation state, visual hierarchy, layout, panel visibility, focus behavior, and user-facing status translation. Parser facts, analytics facts, live capture truth, Match Journal truth, privacy policy authority, external submission authority, and AI/coaching truth remain outside the frontend.

## Bridge-Code Status

`bridge_code`

Allowed flow is existing backend API responses into frontend validation and display. No reverse flow from route state, browser storage, dashboard labels, or visual badges to parser, analytics, live capture, Match Journal, GitHub, workbook, or AI systems was added.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

Branch confirmed: `codex/analytics-foundation`.

Git status before this #299 pass already contained unrelated dirty and untracked work from adjacent local-app slices. Those files were preserved and not reverted.

Current dirty paths observed during the pass:

- `docs/contracts/quality_app_submit_error_report_codex_triage.md`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/error_reports.py`
- `tests/test_analytics_local_app_backend.py`
- `docs/contract_test_reports/live_app_explicit_start_capture_control.md`
- `docs/contracts/analytics_app_frontend_information_architecture.md`
- `docs/contracts/live_app_explicit_start_capture_control.md`
- `docs/contracts/quality_app_error_report_github_submission.md`
- `docs/implementation_handoffs/live_app_explicit_start_capture_control_comparison.md`
- `docs/implementation_handoffs/live_app_explicit_start_capture_control_fixer.md`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `tests/test_live_app_explicit_start_capture_control.py`

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_app_frontend_information_architecture.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- GitHub issue #299, via `gh issue view 299 --comments`

## Current Behavior Compared To Contract

The app already had a local shell, left rail, dashboard header, status rail, Decision Support modules, Coach boundary panel, trust/privacy summary, feedback report prep, analytics tables, Match Journal cockpit, manual import panel, and diagnostics disclosure.

The main contract gap was information architecture: most surfaces still lived in one long document below the dashboard. Rail links were hash anchors, but the app did not yet behave like route-gated modes with Dashboard as the compact first-screen cockpit.

The contract authorized a frontend-only first slice to route Dashboard, Coach, Analytics, Review, Privacy, Feedback, Import, and Diagnostics while preserving all existing backend/API behavior and safety boundaries.

## Implementation Option Chosen

Implemented a hash-route frontend mode model instead of adding a router dependency or backend support. This is the smallest scoped change because it keeps existing API calls, typed payload validation, browser storage posture, and workflow components intact while changing only presentation and visibility.

## Files Changed

Intended #299 implementation files:

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_app_frontend_information_architecture_comparison.md`

The #299 contract file was pre-existing untracked Codex B output and is included as the governing artifact, not authored in this implementation pass.

## Exact Sections Changed

`frontend/src/App.tsx`:

- Added frontend-only `AppRoute`, `APP_ROUTES`, and `RAIL_ITEMS` route definitions.
- Added hash-route state and `hashchange` handling in `SetupStatusApp`.
- Gated major surfaces by route:
  - Dashboard: cockpit status, live capture control, Decision Support modules, Coach boundary, route cards, trust/privacy summary.
  - Analytics: Decision Support modules plus read-only analytics history, split, early-game, action, and observation sections.
  - Review: Match Journal cockpit.
  - Coach: pending/deferred Coach boundary.
  - Feedback: sanitized copy-first error report surface.
  - Import: manual/browser JSONL import surface.
  - Privacy: trust/privacy summary and local-only boundary details.
  - Diagnostics: setup status and live diagnostics, visible by route; dashboard keeps the technical disclosure collapsed by default.
- Reworked `Shell` left rail to render route links with visible labels, keyboard focus styling hooks, accessible names, and visible active state.
- Added route-card and privacy-detail panels for safe navigation into deeper modes.

`frontend/src/App.css`:

- Added active/focus left-rail styling and a visible `Current` marker so active state is not color-only.
- Added route-card and privacy-detail layout styles.
- Preserved responsive shell constraints already present in the app.

`frontend/src/App.test.tsx`:

- Reset hash state between tests.
- Added route helper and route-aware setup for Analytics, Review, Feedback, Import, and Diagnostics tests.
- Updated dashboard assertions to prove long forms/tables/cockpits are not rendered by default.
- Added explicit unknown-route fallback coverage.
- Added active rail state coverage for routed Analytics views.
- Kept existing safety assertions for forbidden destructive controls, raw/private display, no external submission, and no AI/coaching claims.

## Code Changed

Yes, frontend runtime code changed. The changes are limited to frontend route/display behavior in `frontend/src/App.tsx` and presentation styles in `frontend/src/App.css`.

No backend code was intentionally changed for #299. Existing dirty backend/API/type files belong to adjacent local-app work and were left untouched by this pass.

## Tests Added Or Updated

Yes. Focused frontend tests were updated in `frontend/src/App.test.tsx` for route-gated rendering, default Dashboard behavior, unknown route fallback, active rail state, and moved section visibility.

## Interface Changes

No backend API route, payload, schema, SQLite, parser, workbook, webhook, Apps Script, Sheets, OpenAI, AI/coaching, or production interface changed.

Frontend-only URL hash routes were introduced/refined:

- `#dashboard`
- `#coach`
- `#analytics`
- `#review`
- `#privacy`
- `#feedback`
- `#import`
- `#diagnostics`

Unknown hash routes fall back to Dashboard.

## Validation Run

Passed:

```powershell
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run src/App.test.tsx
npm --prefix frontend run build
git diff --check
py tools/check_agent_docs.py
@'
docs/contracts/analytics_app_frontend_information_architecture.md
docs/implementation_handoffs/analytics_app_frontend_information_architecture_comparison.md
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
'@ | py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/analytics_app_frontend_information_architecture.md
docs/implementation_handoffs/analytics_app_frontend_information_architecture_comparison.md
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
'@ | py tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Focused App test result:

```powershell
npm --prefix frontend run test -- --run src/App.test.tsx
# passed, 52 tests
```

Full frontend test result:

```powershell
npm --prefix frontend run test -- --run
# failed: frontend/src/api.test.ts "rejects malformed live status responses safely"
```

The full-suite failure is in the pre-existing dirty API/live-watcher validation surface, not in the #299 route/IA files changed by this implementation pass. Codex C left that adjacent work untouched.

## Protected-Surface Status

Path-scoped scan over the #299 contract, handoff, and touched frontend files passed with `forbidden: 0` and `warnings: 0`.

Implementation stayed inside Local App / UI frontend files and did not intentionally touch backend/parser/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.

## Secret And Private-Marker Status

Path-scoped scan over the #299 contract, handoff, and touched frontend files passed with `forbidden: 0` and `warnings: 0`.

The UI changes do not add raw Player.log content, raw JSONL payloads, raw private paths, raw hashes, secrets, credentials, endpoint values, spreadsheet IDs, environment values, generated SQLite contents, runtime files, workbook exports, frontend build output, app-data files, or local-only artifacts.

## Generated Artifact Status

`npm --prefix frontend run build` created `frontend/dist`; it was removed before final handoff. No generated build output is intended for commit.

## Still Unverified

- Live browser visual/mobile smoke was not run in this pass.
- Full frontend suite remains blocked by the unrelated `frontend/src/api.test.ts` live-watcher validation failure described above.
- Because adjacent #297/#281 files were already dirty in the same frontend files, Codex E should distinguish #299 IA behavior from pre-existing explicit-capture and error-report changes.

## Forbidden Scope

Forbidden scope was not intentionally touched for #299:

- no backend routes or API schemas changed;
- no parser behavior changed;
- no analytics schema, migration, or ingest behavior changed;
- no live capture semantics changed;
- no Match Journal backend behavior changed;
- no workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed;
- no destructive UI/database/import/job/watcher controls were added by the #299 IA slice;
- no staging, commit, push, PR, merge, deploy, or issue closure was performed.

## Reviewer Focus

Ask Codex E to verify:

- the route model covers Dashboard, Coach, Analytics, Review, Privacy, Feedback, Import, and Diagnostics;
- Dashboard remains compact and does not render long forms/tables/cockpits by default;
- all moved workflows remain reachable;
- active rail state is visible and programmatically understandable;
- forbidden controls/claims remain absent;
- #299 did not absorb unrelated #297/#281 backend/API behavior.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #299.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/299

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_frontend_information_architecture.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_frontend_information_architecture_comparison.md

Risk tier:
High overall; first implementation slice Medium frontend-only

Goal:
Review the Codex C implementation against the contract. Verify that the local app frontend information architecture is frontend-only, route-gated, accessible, safe, and scoped. Lead with findings ordered by severity.

Before reviewing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and identify unrelated dirty or untracked files, especially adjacent #297 live-capture and #281/#298 error-report work.
- Read the contract and implementation handoff.
- Inspect frontend/src/App.tsx, frontend/src/App.css, frontend/src/App.test.tsx, and reference-only backend/API surfaces only as needed to confirm no route-shape/schema changes were made.

Review focus:
- Dashboard is the default route and stays a compact cockpit.
- Unknown routes safely fall back to Dashboard.
- Left rail exposes Dashboard, Coach, Analytics, Review, Privacy, Feedback, Import, and Diagnostics with accessible names, visible labels, visible focus, and active state not conveyed by color alone.
- Dashboard does not render full technical setup grids, manual import forms, long analytics/history tables, Match Journal cockpit forms, or full feedback forms by default.
- Analytics, Review, Feedback, Import, Privacy, Coach, and Diagnostics routes expose their intended existing surfaces without changing backend/API behavior.
- Existing safe redaction, privacy boundaries, disabled states, malformed-response handling, and no-external-submission posture are preserved.
- No arbitrary SQL, database browsing, destructive controls, AI/coaching claims, hidden-card claims, player-mistake labels, best-line advice, raw payloads, raw hashes, full paths, secrets, or generated/private artifacts are exposed.
- Distinguish #299 IA changes from unrelated pre-existing dirty work in the same branch.

Validation:
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools/check_agent_docs.py

Run path-scoped protected-surface and secret/private-marker scans over changed #299 files:
- docs/contracts/analytics_app_frontend_information_architecture.md
- docs/implementation_handoffs/analytics_app_frontend_information_architecture_comparison.md
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx

If npm build creates frontend/dist, remove generated build output before final handoff unless explicitly authorized.

Final output must include:
- role performed
- issue and contract reviewed
- implementation handoff reviewed
- branch and git status
- findings first, ordered by severity
- tests/validation run and results
- protected-surface and secret/private-marker status
- generated/private artifact status
- whether forbidden scope was touched
- remaining risk
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/299"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/analytics_app_frontend_information_architecture.md"
  target_artifact: "docs/implementation_handoffs/analytics_app_frontend_information_architecture_comparison.md"
  risk_tier: "High overall; first implementation slice Medium frontend-only"
  branch: "codex/analytics-foundation"
  validation:
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run src/App.test.tsx -> passed, 52 tests"
    - "npm --prefix frontend run test -- --run -> failed in unrelated frontend/src/api.test.ts live-watcher validation"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan over #299 files -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over #299 files -> passed, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not target main."
    - "Do not change backend API contracts."
    - "Do not implement issue #294 auto-refresh, issue #297 live capture behavior changes, or issue #298 live GitHub submission."
    - "Do not change parser/runtime/analytics schema/analytics ingest/live capture/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not expose arbitrary SQL, database browsing, destructive controls, raw/private artifacts, generated data, or secrets."
```
