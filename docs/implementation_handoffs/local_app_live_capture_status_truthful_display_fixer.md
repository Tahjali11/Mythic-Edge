# Local App Live Capture Status Truthful Display Fixer Handoff

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/295
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/294

## Tracker

N/A.

## Contract

`docs/contracts/local_app_live_capture_status_truthful_display.md`

## Review Artifact

`docs/contract_test_reports/local_app_live_capture_status_truthful_display.md`

## Implementation Handoff

`docs/implementation_handoffs/local_app_live_capture_status_truthful_display_comparison.md`

## Required Governance

- `docs/agent_constitution.md`
- `docs/agent_threads/module_fixer.md`

## Internal Project Area

Local App / UI status translation.

## Truth Owner

Truth ownership remains upstream:

- parser/state owns parser facts and final reconciliation;
- live watcher/process surfaces own watcher readiness and process-control
  status;
- live SQLite capture status owns whether live SQLite writes are active,
  disabled, status-only, or blocked;
- frontend owns only safe user-facing status translation and detail text.

## Bridge-Code Status

`bridge_code`

## Role Performed

Codex D: Module Fixer.

## Source Finding

CT-295-001 P1: conflicting live-capture payloads could still render
`Capturing` before disabled/status-only evidence was honored.

Fault category: frontend status-precedence implementation gap.

## Fix Produced

Implemented a narrow frontend-only consistency/order fix:

- added a regression test where `live_sqlite_capture.status = "disabled"` and
  `mode = "status_only"` conflict with active-looking watcher/process booleans;
- moved explicit live SQLite blocked, unavailable, disabled, status-only, and
  direct SQLite-write-disabled evidence ahead of the active-capture branch;
- kept `Capturing` available only after those stricter live-capture stop
  conditions have been ruled out;
- preserved the existing active-capture success test for consistent running
  evidence.

No backend route, watcher process, live ingest, live SQLite capture semantic,
parser, analytics schema, workbook, webhook, Apps Script, Sheets, OpenAI/model
provider, AI/coaching, Line Tracer, production, or generated/private artifact
behavior changed.

## Files Changed By This D Fix

- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/local_app_live_capture_status_truthful_display_fixer.md`

Existing #295 artifacts preserved in the working tree:

- `docs/contracts/local_app_live_capture_status_truthful_display.md`
- `docs/implementation_handoffs/local_app_live_capture_status_truthful_display_comparison.md`
- `docs/contract_test_reports/local_app_live_capture_status_truthful_display.md`

Existing unrelated/mixed worktree changes were left untouched.

## Code Changed

Yes. Frontend runtime code changed only in
`frontend/src/App.tsx`.

The change is limited to status-label precedence inside
`liveCaptureStatusFromSetupPayload(...)`.

## Tests Changed

Yes. Added one focused regression in `frontend/src/App.test.tsx`:

- disabled/status-only live SQLite capture outranks active-looking watcher
  evidence and renders `Capture disabled`, not `Capturing` or `Ready`.

Before the fix, the new regression failed with the Live capture card rendering
`Capturing`.

After the fix, the focused frontend suite passed.

## Interface Changes

No backend route shape, API payload shape, environment variable contract,
database schema, migration, parser output, workbook schema, webhook payload, or
Apps Script interface changed.

## Contracted Area Status

Stayed inside the Local App / UI display translation surface.

No issue #294 auto-refresh work was implemented.

## Branch And Worktree Status

Branch: `codex/analytics-foundation`, behind
`origin/codex/analytics-foundation` by 9 commits.

This D thread did not pull, rebase, merge, stage, commit, push, open a PR,
target main, close issues, or resolve branch sync.

The working tree was mixed before this fix, including existing #295/#294 files
and unrelated error-report/roadmap changes. This D thread preserved that state
and only changed the #295 frontend status precedence/test plus this handoff.

## Validation Run

```powershell
npm --prefix frontend test -- --run src/App.test.tsx src/status.test.ts
npm --prefix frontend run typecheck
py -m pytest -q tests\test_analytics_local_app_backend.py
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over the #295 package
path-scoped secret/private-marker scan over the #295 package
```

Results:

- Focused frontend regression before fix: failed as expected; conflicting
  disabled/status-only payload rendered `Capturing`.
- Focused frontend tests after fix: passed, 2 files, 51 tests.
- Frontend typecheck: passed.
- Focused backend setup-status/local-app backend tests: passed, 24 tests, 1
  existing FastAPI/Starlette TestClient deprecation warning.
- Frontend build: passed.
- `frontend/dist` was created by build validation and removed.
- `git diff --check`: passed.
- Agent docs check: passed.
- Path-scoped protected-surface scan over eight #295 paths: passed,
  `forbidden: 0`, `warnings: 0`.
- Path-scoped secret/private-marker scan over eight #295 paths: passed,
  `forbidden: 0`, `warnings: 0`.

## Generated Artifact Status

`frontend/dist` was generated by build validation and removed.

No generated/private/runtime/local artifact was retained.

## Forbidden Scope Status

Forbidden scope touched: false.

No watcher process was started or stopped. No Player.log content was tailed,
read, copied, hashed, or stored. No live parser ingest, live SQLite capture
semantic, parser/runtime, analytics schema, workbook/webhook/App Script/Sheets,
OpenAI/model-provider, AI/coaching, Line Tracer, production, staging, commit,
push, PR, merge, or issue-close behavior changed.

## Still Unverified

- Browser/manual visual smoke was not run.
- Branch freshness remains unresolved because the branch is behind origin by 9
  commits.
- Full repository tests were not rerun.
- Unrelated existing local changes remain mixed in the working tree.

## Reviewer Focus

Codex E should confirm:

- disabled/status-only live SQLite capture now outranks active-looking
  watcher/process booleans;
- `Capturing` still appears for consistent strict active evidence;
- `Ready` is not shown on the Live capture card for the disabled/status-only
  issue #295 state;
- no backend or protected product surface changed;
- generated `frontend/dist` is absent.

## Next Workflow Action

Next role: Codex E: Module Reviewer / confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #295.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/295

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/294

Branch:
codex/analytics-foundation

Contract:
docs/contracts/local_app_live_capture_status_truthful_display.md

Review artifact:
docs/contract_test_reports/local_app_live_capture_status_truthful_display.md

Fixer handoff:
docs/implementation_handoffs/local_app_live_capture_status_truthful_display_fixer.md

Confirm only CT-295-001:
- disabled/status-only live SQLite capture outranks active-looking watcher/process booleans;
- the Live capture card does not render Ready or Capturing for disabled/status-only evidence;
- Capturing still requires consistent strict active evidence;
- no issue #294 auto-refresh, watcher controls, live ingest, live SQLite capture semantic, parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/production behavior changed;
- generated frontend/dist is absent.

Suggested validation:
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run src/App.test.tsx src/status.test.ts
py -m pytest -q tests\test_analytics_local_app_backend.py
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface and secret/private-marker scans over the #295 package.

Route to Codex F only if CT-295-001 is confirmed fixed.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/295"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/local_app_live_capture_status_truthful_display.md"
  review_artifact: "docs/contract_test_reports/local_app_live_capture_status_truthful_display.md"
  implementation_handoff: "docs/implementation_handoffs/local_app_live_capture_status_truthful_display_fixer.md"
  finding_fixed:
    - "CT-295-001 P1: disabled/status-only live SQLite capture evidence now outranks active-looking watcher/process booleans."
  validation:
    - "focused frontend regression before fix failed as expected"
    - "focused frontend tests after fix -> passed, 51 tests"
    - "frontend typecheck -> passed"
    - "focused backend setup-status/local-app backend tests -> passed, 24 tests, 1 existing third-party warning"
    - "frontend build -> passed; frontend/dist removed"
    - "git diff --check -> passed"
    - "agent docs check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  protected_surface_status: "passed, forbidden 0, warnings 0"
  secret_private_marker_status: "passed, forbidden 0, warnings 0"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex E confirmation thread"
```
