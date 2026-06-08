# Quality App Error Report GitHub Submission Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/298

## Tracker

N/A. The contract identifies issues #204 and #207 as closed historical context.

## Related Prior Issue

https://github.com/Tahjali11/Mythic-Edge/issues/281

## Contract

`docs/contracts/quality_app_error_report_github_submission.md`

## Internal Project Area

Primary: Local App / UI.

Secondary: Quality / Developer Workflow.

## Truth Owner

The sanitized report is triage evidence only. It is not parser truth, analytics truth, live watcher truth, Match Journal truth, privacy-policy authority, release readiness, or a root-cause diagnosis.

GitHub owns the created issue after successful submission. Mythic Edge local app owns only the explicit submit attempt, safe request/response shape, and fallback report body.

## Bridge-Code Status

`bridge_code`

Allowed flow: sanitized report request to backend privacy guard, local `gh issue create`, returned issue URL. No reverse flow from GitHub issue state to parser, analytics, live capture, Match Journal, app config, workbook, or AI systems was added.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

Branch confirmed: `codex/analytics-foundation`.

Initial status was clean relative to `origin/codex/analytics-foundation`; the #298 contract was missing from the checkout and was restored from preserved untracked-work commit `b819cac` as `docs/contracts/quality_app_error_report_github_submission.md`.

Final changed/untracked files for #298:

- `docs/contracts/quality_app_error_report_github_submission.md`
- `docs/implementation_handoffs/quality_app_error_report_github_submission_comparison.md`
- `src/mythic_edge_parser/local_app/error_reports.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/quality_app_error_report_github_submission.md`
- `docs/contracts/quality_app_submit_error_report_codex_triage.md`
- GitHub issue #298
- `src/mythic_edge_parser/local_app/error_reports.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`

## Current Behavior Compared To Contract

Current repo behavior already had the #281 copy-first preview route:

- `POST /api/feedback/error-report/preview`
- sanitized Markdown report composition
- privacy blocking for endpoint-like, token-like, secret-like, and hash-like values
- private path redaction
- copy-only frontend flow

The #298 gaps were:

- no `POST /api/feedback/error-report/submit`;
- no structured submission response;
- no local `gh issue create` boundary;
- no report-type label mapping;
- no frontend submit-after-preview action;
- tests still asserted submit route absence.

## Implementation Option Chosen

Implemented the smallest explicit local GitHub CLI path:

- backend rebuilds preview server-side before every submit;
- backend refuses invalid or privacy-blocked previews;
- backend uses a `GitHubIssueSubmitter` protocol for mocked tests;
- default runtime submitter uses local `gh` with argument-list `subprocess.run(..., shell=False)`;
- issue body is passed through a temporary Markdown file inside `TemporaryDirectory`, which is removed automatically;
- labels map to existing labels with contract fallbacks;
- frontend only shows `Submit report to GitHub` after a ready preview with submission enabled.

## Files Changed

`docs/contracts/quality_app_error_report_github_submission.md`:

- Restored missing Codex B contract artifact from preserved local untracked-work commit `b819cac`.

`src/mythic_edge_parser/local_app/error_reports.py`:

- Added submission constants and response schema.
- Added report-type support for `bug`, `feedback`, and `feature_request`.
- Added server-side submit flow through `build_error_report_submission`.
- Added `GitHubIssueSubmitter`, `GitHubSubmitterError`, and `GhCliIssueSubmitter`.
- Added label mapping and fallback logic.
- Added safe GitHub issue URL parsing and repo verification.
- Kept preview as the privacy guard and fallback body source.

`src/mythic_edge_parser/local_app/backend.py`:

- Added injectable `error_report_submitter` parameter for tests.
- Added `POST /api/feedback/error-report/submit`.

`tests/test_analytics_local_app_backend.py`:

- Added mocked submitter.
- Updated route inventory.
- Updated preview title/capability expectations.
- Replaced old submit-route-absent assertion.
- Added submit success, privacy-blocked no-call, label fallback, missing `gh`, and required-label fallback tests.

`frontend/src/types.ts`:

- Added submission object/schema constants.
- Added `ErrorReportType`.
- Expanded preview request to support bug, feedback, and feature-request field shapes.
- Added `ErrorReportSubmissionResponse`.

`frontend/src/api.ts`:

- Added `submitErrorReport`.
- Added submit response validation.

`frontend/src/api.test.ts`:

- Added submit helper response validation test.

`frontend/src/App.tsx`:

- Added report-type selector and type-specific form fields.
- Added `submitReport` prop defaulting to `submitErrorReport`.
- Added submit state and `Submit report to GitHub` action after ready preview only.
- Added success and fallback submission result rendering.
- Kept `Copy Report` fallback available.

`frontend/src/App.test.tsx`:

- Updated report tests for report type, optional reproduction steps, preview-first submit, mocked success URL, and blocked-preview no-submit behavior.

## Code Changed

Yes. Runtime code changed in the local app backend and frontend:

- Backend local app report submission route and helper code.
- Frontend report form, API helper, and display state.

No parser, analytics schema/migration/ingest, live watcher, live capture semantics, Match Journal truth ownership, workbook, webhook, Apps Script, Sheets, OpenAI, AI/coaching, Line Tracer, or production behavior was intentionally changed.

## Tests Added Or Updated

Yes:

- Backend tests in `tests/test_analytics_local_app_backend.py`.
- Frontend component tests in `frontend/src/App.test.tsx`.
- Frontend API tests in `frontend/src/api.test.ts`.

Automated tests mock GitHub submission and do not create live GitHub issues.

## Interface Changes

Added backend route:

```text
POST /api/feedback/error-report/submit
```

Added submit response object:

```text
object: mythic_edge_local_app_error_report_submission
schema_version: quality_app_error_report_github_submission.v1
```

Preview request now supports `report_type` and type-specific fields while retaining existing bug fields and severity:

- `bug`: `expected_behavior`, `actual_behavior`, optional `reproduction_steps`
- `feedback`: `feedback`
- `feature_request`: `feature_goal`, `feature_location`, `feature_success`

No GitHub tokens, credentials, environment variable contracts, backend route shapes outside feedback submission, workbook columns, webhook fields, Apps Script surfaces, parser outputs, analytics schema objects, or generated artifacts were added.

## Contracted Area Status

Implementation stayed inside the contracted Local App / UI and Quality / Developer Workflow bridge surface.

The only external side effect available at runtime is the explicitly clicked backend `gh issue create` path after preview is ready. Automated validation uses mocked submitters only.

## Validation Run

```powershell
py -m pytest -q tests\test_analytics_local_app_backend.py
# 26 passed, 1 Starlette/httpx deprecation warning

npm --prefix frontend run typecheck
# passed

npm --prefix frontend run test -- --run src/App.test.tsx src/api.test.ts
# 81 passed

npm --prefix frontend run test -- --run
# 85 passed

npm --prefix frontend run build
# passed; frontend/dist removed after build

py -m ruff check src tests tools
# All checks passed
```

```powershell
git diff --check
// passed

py tools/check_agent_docs.py
// passed

@'
docs/contracts/quality_app_error_report_github_submission.md
docs/implementation_handoffs/quality_app_error_report_github_submission_comparison.md
src/mythic_edge_parser/local_app/error_reports.py
src/mythic_edge_parser/local_app/backend.py
tests/test_analytics_local_app_backend.py
frontend/src/types.ts
frontend/src/api.ts
frontend/src/api.test.ts
frontend/src/App.tsx
frontend/src/App.test.tsx
'@ | py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
// passed, forbidden 0, warnings 0

@'
docs/contracts/quality_app_error_report_github_submission.md
docs/implementation_handoffs/quality_app_error_report_github_submission_comparison.md
src/mythic_edge_parser/local_app/error_reports.py
src/mythic_edge_parser/local_app/backend.py
tests/test_analytics_local_app_backend.py
frontend/src/types.ts
frontend/src/api.ts
frontend/src/api.test.ts
frontend/src/App.tsx
frontend/src/App.test.tsx
'@ | py tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
// passed, forbidden 0, warnings 0
```

## Protected-Surface Status

Path-scoped protected-surface scan over changed #298 files passed with `forbidden: 0` and `warnings: 0`. Implementation stayed out of parser/runtime truth, analytics schema/ingest, live watcher semantics, live capture semantics, Match Journal truth ownership, workbook/webhook/App Script/Sheets, OpenAI/AI/coaching, Line Tracer, and production behavior.

## Secret And Private-Artifact Status

Path-scoped secret/private-marker scan over changed #298 files passed with `forbidden: 0` and `warnings: 0`. Implementation does not store GitHub tokens in app config, does not attach files or screenshots, does not expose raw `gh` output, and does not submit raw Player.log, JSONL, SQLite contents, private paths, hashes, secrets, endpoint values, spreadsheet IDs, environment values, runtime logs, transport-failure payloads, workbook exports, generated/private/local artifacts, arbitrary files, arbitrary SQL, or database browsing.

## Generated Artifact Status

`npm --prefix frontend run build` created `frontend/dist`; it was removed before handoff. No generated build output is intended for commit.

## Still Unverified

- No live GitHub issue was created. This is intentional; the contract forbids live issue creation in automated tests. A manual smoke would require explicit user approval and a deliberately safe synthetic report.
- Runtime behavior with the user's actual `gh` authentication was not exercised.

## Forbidden Scope

Forbidden scope was not intentionally touched:

- no parser behavior changes;
- no parser final reconciliation, event class, match/game identity, or deduplication changes;
- no analytics schema/migration/ingest changes;
- no live watcher or live capture semantic changes;
- no Match Journal truth changes;
- no workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production changes;
- no GitHub label creation;
- no attachments or screenshots;
- no staging, commit, push, PR, merge, deploy, or issue closure.

## Reviewer Focus

Ask Codex E to verify:

- submit route rebuilds preview and privacy guard before issue creation;
- backend never trusts frontend-provided Markdown;
- `gh` invocation is argument-list, repo-fixed, and does not expose raw tool output;
- label fallback behavior matches the contract;
- frontend submit button is preview-first and explicit;
- copy fallback remains available;
- automated tests do not create live GitHub issues;
- no protected surfaces were touched.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #298.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/298

Related prior issue:
https://github.com/Tahjali11/Mythic-Edge/issues/281

Branch:
codex/analytics-foundation

Contract:
docs/contracts/quality_app_error_report_github_submission.md

Implementation handoff:
docs/implementation_handoffs/quality_app_error_report_github_submission_comparison.md

Risk tier:
High

Goal:
Review the Codex C implementation against the contract. Verify that GitHub Issue submission is explicit, preview-first, privacy-guarded, local-operator-only, and uses mocked external writes in automated tests. Lead with findings ordered by severity.

Before reviewing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and changed files.
- Read issue #298, related issue #281, the #298 contract, and the implementation handoff.
- Inspect src/mythic_edge_parser/local_app/error_reports.py, src/mythic_edge_parser/local_app/backend.py, tests/test_analytics_local_app_backend.py, frontend/src/types.ts, frontend/src/api.ts, frontend/src/api.test.ts, frontend/src/App.tsx, and frontend/src/App.test.tsx.

Review focus:
- POST /api/feedback/error-report/submit exists and is local-app scoped.
- Submit accepts structured report fields and rebuilds preview server-side.
- Submit refuses invalid or privacy-blocked preview output before any GitHub call.
- GitHub submission uses local gh through argument-list subprocess execution and targets exactly Tahjali11/Mythic-Edge.
- No GitHub tokens are stored in app config.
- Labels map to bug/feedback/feature_request with contracted fallbacks and no runtime label creation.
- Responses are structured and safe, with fallback Markdown available on failure.
- Raw command stderr/stdout, private paths, raw payloads, secrets, hashes, endpoint values, screenshots, attachments, local artifacts, arbitrary SQL, and database browsing are not exposed.
- Frontend shows Submit report to GitHub only after preview_ready and external_submission_enabled.
- No automatic submission happens.
- Copy Report remains available after preview and after failed submission.
- Automated tests mock GitHub submission and do not create live GitHub issues.
- No parser/runtime/analytics schema/live watcher/live capture/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed.

Validation:
py -m pytest -q tests\test_analytics_local_app_backend.py
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools/check_agent_docs.py

Run path-scoped protected-surface and secret/private-marker scans over:
- docs/contracts/quality_app_error_report_github_submission.md
- docs/implementation_handoffs/quality_app_error_report_github_submission_comparison.md
- src/mythic_edge_parser/local_app/error_reports.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_local_app_backend.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/api.test.ts
- frontend/src/App.tsx
- frontend/src/App.test.tsx

If npm build creates frontend/dist, remove generated build output before final handoff unless explicitly authorized.

Final output must include:
- role performed
- issue and contract reviewed
- implementation handoff reviewed
- branch and git status
- findings first, ordered by severity
- validation run and result
- protected-surface status
- secret/private-marker status
- generated/private artifact status
- whether forbidden scope was touched
- remaining risk
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/298"
  related_prior_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/281"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/quality_app_error_report_github_submission.md"
  target_artifact: "docs/implementation_handoffs/quality_app_error_report_github_submission_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py -> passed, 26 tests"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run src/App.test.tsx src/api.test.ts -> passed, 81 tests"
    - "npm --prefix frontend run test -- --run -> passed, 85 tests"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan over #298 files -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over #298 files -> passed, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not target main."
    - "Do not create a live GitHub Issue in automated tests."
    - "Do not auto-file issues from runtime errors."
    - "Do not store GitHub tokens in app config."
    - "Do not create labels dynamically from app runtime."
    - "Do not attach raw/private files or screenshots."
    - "Do not change parser/runtime/analytics/live watcher/live capture/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
