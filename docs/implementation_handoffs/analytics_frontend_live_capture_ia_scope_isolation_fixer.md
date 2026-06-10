# Analytics Frontend Live Capture IA Scope-Isolation Fixer

## Issues

- Primary: https://github.com/Tahjali11/Mythic-Edge/issues/299
- Related: https://github.com/Tahjali11/Mythic-Edge/issues/297
- Adjacent unrelated dirty scope: issue #281/#298 error-report request-shape work.

## Branch

`codex/analytics-frontend-live-capture-ia-297-299`

## Source Handoff

Codex F stopped before staging because the current dirty worktree mixes the reviewed #297/#299 frontend package with #281/#298 error-report request-shape changes.

## Role Performed

Codex D: Module Fixer / scope-isolation thread.

## Fault Category

Package-boundary / staging isolation blocker.

The #297/#299 implementation and validation are code-clean, but file-level staging would include unrelated #298 error-report request-shape changes. The blocker is not a route-rendering or live-capture runtime failure; it is a submitter packaging problem.

## Finding

Whole-file staging of shared frontend files is unsafe because:

- `frontend/src/App.tsx` contains both #297/#299 live-capture/route-shell work and #298 `ErrorReportPanel` request-shape changes.
- `frontend/src/App.test.tsx` contains both #297/#299 route/live-capture tests and #298 feedback/feature-request error-report tests.
- `frontend/src/types.ts` contains both #297 live-capture types / #299 watcher-readiness narrowing and #298 error-report request type changes.

Whole-file staging of backend error-report files is also unsafe for this package because they are outside the #297/#299 reviewed scope.

## Inspection Result

The original #281 preview/copy error-report surface already exists in `HEAD`. The unrelated dirty scope is the later #298 request-shape change from severity-based reports to `report_type`-based bug/feedback/feature-request reports. That means a reviewed #297/#299 package is still possible, but only with hunk-level or edited-patch staging.

## Safe Whole-File Scope

These files can be included as whole files for the #297/#299 package:

- `docs/contracts/live_app_explicit_start_capture_control.md`
- `docs/contract_test_reports/live_app_explicit_start_capture_control.md`
- `docs/implementation_handoffs/live_app_explicit_start_capture_control_comparison.md`
- `docs/implementation_handoffs/live_app_explicit_start_capture_control_fixer.md`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `tests/test_live_app_explicit_start_capture_control.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `docs/contracts/analytics_app_frontend_information_architecture.md`
- `docs/contract_test_reports/analytics_app_frontend_information_architecture.md`
- `docs/implementation_handoffs/analytics_app_frontend_information_architecture_comparison.md`
- `docs/implementation_handoffs/analytics_app_frontend_information_architecture_fixer.md`
- `docs/implementation_handoffs/analytics_frontend_live_capture_ia_scope_isolation_fixer.md`
- `frontend/src/api.ts`
- `frontend/src/App.css`

Notes:

- `frontend/src/api.ts` contains #297 live-capture API helpers plus the #299 readiness-only watcher validator fix. It does not contain the #298 request-shape diff.
- `frontend/src/App.css` contains #297/#299 live-capture control and route-shell styling. No #298 request-shape dependency was found there.
- `src/mythic_edge_parser/local_app/backend.py` contains only the #297 live-capture route additions in the current diff.

## Hunk-Level Scope

These files must not be staged as whole files for a #297/#299-only package:

- `frontend/src/types.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`

Stage only the #297/#299 hunks:

- `frontend/src/types.ts`
  - Include `LIVE_CAPTURE_*` constants.
  - Include `LiveCaptureStatusResponse`, `LiveCaptureStartResult`, and `LiveCaptureStopResult`.
  - Include the #299 `LiveWatcherSummary` readiness-only narrowing:
    - `running: false`
    - `parser_runner_started: false`
    - `tailing_started: false`
    - `sqlite_live_writes_enabled: false`
  - Exclude the #298 `ErrorReportSeverity` to `ErrorReportType` change and all `ErrorReportPreviewRequest` request-shape changes.

- `frontend/src/App.tsx`
  - Include #297 live-capture API imports, props, state, fetch/start/stop handlers, `LiveCaptureControlPanel`, and live-capture status helper changes.
  - Include #299 route shell, `APP_ROUTES`, rail active-state behavior, dashboard route cards, privacy details, route-gated Analytics/Review/Coach/Feedback/Import/Diagnostics rendering, and diagnostics disclosure changes.
  - Exclude #298 error-report request-shape changes:
    - `ErrorReportType` import replacing `ErrorReportSeverity`.
    - `ERROR_REPORT_TYPE_OPTIONS`.
    - `reportType`, `feedback`, `featureGoal`, `featureLocation`, and `featureSuccess` state.
    - `ErrorReportPanel` request construction using `report_type`.
    - Feedback/feature-request-specific form fields.
  - The staged #299 Feedback route should render the existing #281 `ErrorReportPanel` shape from `HEAD`.

- `frontend/src/App.test.tsx`
  - Include #297 live-capture control tests and fixtures.
  - Include #299 route-gating tests, active rail-state tests, and route-specific `setRoute(...)` updates.
  - Include the #299 active-live-capture fixture correction that leaves `/api/live/watcher/status` readiness-only.
  - Exclude #298 error-report tests:
    - feedback report shape test.
    - feature request shape test.
    - existing error-report expectations changed from `severity` to `report_type`.
    - `buildErrorReportPreviewPayload` title change to include report type.

## Must Remain Unstaged For #297/#299

- `docs/contracts/quality_app_submit_error_report_codex_triage.md`
- `docs/contracts/quality_app_error_report_github_submission.md`
- `src/mythic_edge_parser/local_app/error_reports.py`
- `tests/test_analytics_local_app_backend.py`
- #298 hunks inside `frontend/src/App.tsx`
- #298 hunks inside `frontend/src/App.test.tsx`
- #298 hunks inside `frontend/src/types.ts`

## Submitter Guidance

Codex F should not use file-level `git add` on the three mixed frontend files. Use edited-patch or interactive hunk staging, then verify:

```powershell
git diff --cached --name-status
git diff --cached -- frontend\src\App.tsx frontend\src\App.test.tsx frontend\src\types.ts
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run
npm --prefix frontend run build
```

After build validation, remove `frontend/dist` if created.

If edited-patch staging is too risky, the safer workflow is one of:

- submit/review #298 first, then submit #297/#299 as a combined package; or
- get explicit user authorization to submit a broader #297/#298/#299 package; or
- create a fresh clean worktree from the branch base and apply only the #297/#299 patch there.

## Validation

No runtime code was changed in this scope-isolation pass. The current mixed worktree had already been made validation-clean in the preceding D pass.

This pass validates the package-boundary diagnosis and documents a safe submitter path without staging, committing, pushing, or reverting unrelated work.

## Forbidden Scope Status

Forbidden scope touched: false.

No parser behavior, parser final reconciliation, analytics schema/migrations, manual import semantics, replay ingest semantics, Match Journal truth ownership, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, secrets, raw logs, raw JSONL payloads, generated runtime artifacts, workbook exports, or local-only runtime artifacts were changed.

## Remaining Risk

- A #297/#299-only staged package has not been created in this D pass.
- Hunk-level staging needs careful review by Codex F.
- Browser/mobile visual smoke for #299 remains unverified.

## Next Recommended Role

Codex F submitter, using hunk-level staging from this handoff, or Codex E if the user wants independent confirmation of the package split before staging.

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer / scope-isolation thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/299"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/297"
  branch: "codex/analytics-frontend-live-capture-ia-297-299"
  source_handoff: "Codex F blocked_before_staging"
  implementation_handoff: "docs/implementation_handoffs/analytics_frontend_live_capture_ia_scope_isolation_fixer.md"
  finding_addressed:
    - "Reviewed #297/#299 frontend files are mixed with #281/#298 error-report request-shape changes."
  resolution:
    - "No code revert performed."
    - "Documented exact whole-file and hunk-level staging boundaries for a #297/#299-only package."
    - "Identified #298 surfaces that must remain unstaged unless the user authorizes a broader package."
  validation:
    - "No runtime code changed in this pass."
    - "Use npm frontend typecheck/full tests/build after Codex F creates the staged package."
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex F submitter with hunk-level staging, or Codex E confirmation of package split"
```
