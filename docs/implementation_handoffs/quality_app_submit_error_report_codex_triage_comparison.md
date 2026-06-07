# Quality App Submit Error Report Codex Triage Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/281

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

## Umbrella

https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/quality_app_submit_error_report_codex_triage.md`

## Internal Project Area

Local app Quality/Governance support: private-local diagnostic report preparation for later Codex or GitHub triage.

## Truth Owner

The report preview is triage evidence only. Parser/state, analytics ingest, live watcher, Match Journal, workbook/webhook, Apps Script, Sheets, OpenAI/AI, and production layers remain truth owners for their existing domains.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex C: Module Implementer.

## Current Behavior Compared To Contract

Before this pass, the local app exposed setup status, live watcher status, live diagnostics, analytics history, manual import, and Match Journal surfaces, but it had no dedicated sanitized error-report preview route and no frontend form/copy flow.

The contract requires a first copy-first, local-first implementation:

- build a sanitized preview/report composition path;
- expose a frontend form, preview, and copy flow;
- show included and excluded diagnostic categories;
- block or redact unsafe user-entered values;
- avoid external submission, file writes, raw private data reads, and runtime truth changes.

## Implementation Option Chosen

Implemented the narrow preview-only route and UI:

- `POST /api/feedback/error-report/preview` returns deterministic sanitized Markdown.
- The frontend adds a "Report an Error" surface with required user fields, preview generation, included/excluded category display, and clipboard copy.
- No submit route, GitHub issue creation, connector/OAuth flow, external network write, report-file write, or attachment path was added.

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/quality_app_submit_error_report_codex_triage.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/App.test.tsx`

## Files Changed

- `src/mythic_edge_parser/local_app/error_reports.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/quality_app_submit_error_report_codex_triage_comparison.md`

The contract artifact `docs/contracts/quality_app_submit_error_report_codex_triage.md` was present as an untracked Codex B artifact and was preserved without edits.

## Exact Sections Changed

### Backend

- Added `error_reports.py` with:
  - preview schema constant `quality_app_submit_error_report_codex_triage.v1`;
  - allowed affected-area and severity vocabularies;
  - deterministic redaction of private local paths to `<redacted_local_path>`;
  - blocking guard for endpoint-like, token-like, secret-assignment-like, and raw-hash-like user-entered values;
  - safe diagnostic packet composition from existing status builders;
  - deterministic Markdown report body and Codex triage prompt.
- Added `POST /api/feedback/error-report/preview` to `backend.py`.
- Did not add `/api/feedback/error-report/submit`.

### Frontend

- Added error-report request/response types and schema constant in `types.ts`.
- Added `ErrorReportApiError`, `previewErrorReport`, response validation, and loopback-only API base handling in `api.ts`.
- Added `ErrorReportPanel` in `App.tsx`:
  - form fields for summary, expected behavior, actual behavior, reproduction steps, affected area, and severity;
  - preview request through the backend;
  - included diagnostics, excluded private data, redaction summary, and warnings display;
  - copyable Markdown textarea and `Copy Report` action;
  - explicit `External submission disabled` messaging.
- Added a left-rail `Report` anchor to the new local section.
- Added scoped CSS for the form, preview, category lists, and responsive layout.

### Tests

- Added backend tests for preview shape, path redaction, privacy blocking, no app-data writes, and no submit route.
- Added frontend tests for preview-before-copy, copy flow, included/excluded messaging, blocked preview behavior, and absence of external-submit controls.
- Updated the route inventory and existing text assertion for the new affected-area option.

## Code Changed

Yes. Backend local-app support code and frontend local-app UI/API code changed.

## Tests Changed

Yes. Focused backend and frontend tests were added/updated.

## Interface Changes

Added a new local backend preview route:

```text
POST /api/feedback/error-report/preview
```

Added frontend-only TypeScript request/response types for the preview route.

No existing backend route shape, parser output, analytics schema/ingest contract, workbook schema, webhook payload, Apps Script behavior, or production interface was changed.

## Validation Run

```text
py -m pytest -q tests\test_analytics_local_app_backend.py -> 21 passed, 1 StarletteDeprecationWarning
npm --prefix frontend run typecheck -> passed
npm --prefix frontend run test -- --run -> 71 passed
py -m ruff check src\mythic_edge_parser\local_app\error_reports.py src\mythic_edge_parser\local_app\backend.py tests\test_analytics_local_app_backend.py -> passed
npm --prefix frontend run build -> passed
frontend/dist cleanup -> generated build output removed
git diff --check -> passed
py tools\check_agent_docs.py -> passed
path-scoped protected-surface scan over changed files -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan over changed files -> passed, forbidden 0, warnings 0
browser DOM smoke at http://127.0.0.1:5173/ -> passed; report panel, Report nav, Preview Report button, external-submission-disabled messaging, and zero submit/create-GitHub buttons confirmed
```

## Privacy Assessment

The preview route:

- never reads raw Player.log content;
- never reads raw JSONL payloads or arbitrary files;
- never queries SQLite table contents;
- never writes report files;
- never starts watchers or parser workflows;
- never calls GitHub, Codex, OpenAI, Google, or another external service;
- redacts user-entered private local paths;
- blocks endpoint-like, token-like, secret-assignment-like, and raw-hash-like user-entered values;
- reports included diagnostics and excluded private data explicitly.

## Protected-Surface Status

No parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest, live watcher behavior, Match Journal truth ownership, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice was changed.

## Generated Artifact Status

`frontend/dist` was generated by `npm --prefix frontend run build` and removed. No generated database, app-data, report file, runtime log, failed post, workbook export, or local-only artifact was kept.

## Still Unverified

- Manual clipboard behavior in a real browser remains useful for Codex E or user visual review; automated frontend tests covered the clipboard path.
- Live GitHub issue creation is intentionally unimplemented and unverified.
- Backend-written report history under app-data is intentionally deferred.

## Reviewer Focus

Ask Codex E to verify:

- the preview route does not become an external submission path;
- user-entered unsafe values are blocked or redacted before appearing in report Markdown;
- diagnostic categories are safe summaries only;
- the frontend has no `Submit Error Report` or GitHub issue creation action;
- no protected truth ownership boundary moved.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #281.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/281

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/quality_app_submit_error_report_codex_triage.md

Implementation handoff:
docs/implementation_handoffs/quality_app_submit_error_report_codex_triage_comparison.md

Review goal:
Compare the implementation diff, tests, and handoff against the contract. Lead with findings, especially privacy leaks, accidental external submission paths, missing preview/copy safeguards, unsafe diagnostics, or protected-surface drift.

Focus files:
- src/mythic_edge_parser/local_app/error_reports.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_local_app_backend.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx

Do not edit files. Do not stage, commit, push, open a PR, close issues, or run live external submission.

Validation to consider:
- py -m pytest -q tests\test_analytics_local_app_backend.py
- npm --prefix frontend run typecheck
- npm --prefix frontend run test -- --run
- npm --prefix frontend run build
- git diff --check
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files

Return:
- findings first, ordered by severity;
- contract matches and mismatches;
- validation run and result;
- privacy/protected-surface assessment;
- whether forbidden scope was touched;
- next recommended role;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/281"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/quality_app_submit_error_report_codex_triage.md"
  target_artifact: "docs/implementation_handoffs/quality_app_submit_error_report_codex_triage_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py -> 21 passed, 1 StarletteDeprecationWarning"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> 71 passed"
    - "py -m ruff check touched backend/test files -> passed"
    - "npm --prefix frontend run build -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "browser DOM smoke at http://127.0.0.1:5173/ -> passed"
  stop_conditions:
    - "Do not auto-submit to GitHub, Codex, OpenAI, Google, or any external service."
    - "Do not add live GitHub issue creation unless separately authorized."
    - "Do not read, copy, print, store, or commit raw private artifacts, secrets, endpoint values, generated databases, app-data files, runtime logs, or local-only artifacts."
    - "Do not change parser/runtime/analytics/live watcher/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not target main."
```
