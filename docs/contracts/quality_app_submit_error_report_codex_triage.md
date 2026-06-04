# Quality App Submit Error Report For Codex Triage Contract

## Purpose

Define the safe first Mythic Edge local-app workflow for preparing an error report that the user can paste into a future Codex thread or GitHub issue for triage.

This contract treats the local app as a private-local diagnostic helper. It may gather safe status labels, user-described symptoms, validation labels, and redacted environment summaries. It must not upload reports, auto-submit issues, authorize connectors, expose raw private data, or promote diagnostics into parser, analytics, Match Journal, live watcher, workbook, AI, or production truth.

## Source Scope

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/281
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Recent PR: https://github.com/Tahjali11/Mythic-Edge/pull/280
- Intended branch: `codex/analytics-foundation`
- Risk tier: High
- Role: Codex B / Module Contract Writer

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- Issue #281
- Tracker #204
- Umbrella issue #207
- PR #280
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_app_first_screen_competitive_cockpit.md`
- `docs/contracts/live_player_log_v1_supported_readiness.md`
- `docs/contracts/private_local_v1_operator_readme_launch_guide.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/status.ts`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.test.tsx`
- `src/mythic_edge_parser/local_app/`
- `tools/check_secret_patterns.py`
- `tools/check_protected_surfaces.py`

## Observed Current Behavior

- The local app has a competitive cockpit first screen with setup, live Player.log, analytics, Match Journal, and diagnostics-oriented status surfaces.
- The frontend already separates user-facing status from lower-level technical details through a progressive-disclosure control.
- The backend exposes local loopback API routes for health, setup status, runtime paths, analytics status/history, manual import jobs, Match Journal, live watcher status, live ingest status, and live watcher diagnostics.
- Existing live diagnostics are designed as metadata-only summaries and explicitly avoid raw Player.log content, raw paths, SQL data, stack traces, secrets, and environment values.
- No first-class error-report preview, copyable triage packet, or error-report UI exists yet.
- No approved app route currently creates GitHub issues, submits reports to Codex/OpenAI/Google, or authorizes external connectors.

## Required Guarantees

### Report Objective

The first implementation must let the user prepare a sanitized report packet that includes:

- what the user saw;
- what the user expected;
- what steps led to the issue;
- which local app area appears affected;
- safe status and diagnostic labels that can help Codex triage the problem later;
- a clear statement of what private data was excluded.

The report is triage evidence only. It must not become a source of parser truth, analytics truth, Match Journal truth, live watcher truth, privacy-policy authority, or release readiness authority.

### First-Slice Strategy

The approved first slice is copy-first and local-first:

- Required: a sanitized preview and copyable Markdown report.
- Allowed: a user-triggered browser download of the sanitized Markdown report.
- Deferred: backend-written report files under app-data.
- Deferred: live GitHub issue creation.
- Forbidden: automatic submission to GitHub, Codex, OpenAI, Google, or any other external service.

The app may use labels such as `Prepare Error Report`, `Preview Report`, and `Copy Report`. If a future UI includes `Submit Error Report`, the action must mean "prepare/copy a reviewed report" unless a later contract explicitly authorizes external GitHub submission.

## Allowed Report Sources

### User-Entered Fields

The report may include user-entered:

- short summary or title;
- expected behavior;
- actual behavior;
- reproduction steps;
- affected area;
- severity;
- optional notes the user intentionally types into the report form.

Allowed affected-area values should include:

- `local_app_ui`
- `install_launch`
- `manual_import`
- `analytics`
- `live_player_log`
- `match_journal`
- `parser`
- `privacy`
- `unknown`

Allowed severity values should include:

- `blocker`
- `degraded`
- `annoyance`
- `question`

### Frontend Status Sources

The report may include frontend-visible safe metadata:

- current app page or panel;
- current user-facing status labels;
- current validation labels;
- known route reachability states;
- safe error codes or symbolic error labels;
- whether the report was generated from the first-screen cockpit or a technical-details surface.

The frontend must not include raw API payload dumps, browser storage dumps, stack traces with private paths, generated database contents, arbitrary local files, or screenshots in this first slice.

### Backend Status Sources

The report may include backend-provided safe summaries from existing local routes:

- backend health status;
- setup/status aggregate label;
- app profile and release/ref metadata when safely available;
- runtime path labels as symbolic categories only;
- local app config readiness labels;
- Player.log configured/found/missing/stale/blocked summary without raw path or content;
- live watcher process status vocabulary;
- live capture status vocabulary;
- live watcher diagnostics counts and labels;
- analytics database status and migration/schema status without table contents;
- manual import job status summary only when the user explicitly selects a relevant job and the job summary is already sanitized;
- Match Journal readiness/status summary without note bodies unless the user manually types those note details into the report form;
- local GitHub CLI availability/auth/repo labels only as capability status, without tokens or credential material.

## Required Report Shape

### Preview API Shape

Codex C should prefer a preview-first backend route:

- `POST /api/feedback/error-report/preview`

The route should accept a structured request containing:

- `summary`
- `expected_behavior`
- `actual_behavior`
- `reproduction_steps`
- `affected_area`
- `severity`
- `current_frontend_surface`, if supplied by the frontend
- `include_diagnostics`, defaulting to a safe minimal set
- `selected_job_id`, optional and only for already-sanitized import job summaries

The route should return:

- `schema`: `quality_app_submit_error_report_codex_triage.v1`
- `status`: `preview_ready`, `invalid_request`, or `blocked_privacy_guard`
- `issue_title`
- `issue_body_markdown`
- `included_diagnostic_categories`
- `excluded_private_data`
- `redaction_summary`
- `warnings`
- `next_recommended_role`
- `external_submission_enabled`: always `false` in the first slice

### Markdown Packet Shape

The copyable Markdown report must include:

- title prefixed with `[error-report]`;
- user symptom summary;
- expected behavior;
- actual behavior;
- reproduction steps;
- affected area;
- severity;
- safe diagnostic packet;
- privacy exclusion statement;
- suspected source area, if the app can safely label one;
- suggested next workflow role;
- pasteable Codex triage prompt.

The report must be understandable without raw private artifacts.

## Redaction And Exclusion Rules

The report must exclude:

- raw Player.log contents or raw log lines;
- raw JSONL payloads or saved-event lines;
- SQLite database contents, table rows, WAL/SHM/journal contents, or generated database files;
- runtime logs and transport-failure payloads;
- workbook exports;
- screenshots or attachments in the first slice;
- full private local paths;
- raw hashes of private files;
- secrets, credentials, tokens, API keys, OAuth material, endpoint values, spreadsheet IDs, environment values, or connector authorization data;
- arbitrary local files;
- generated/private/local-only artifacts;
- stack traces unless private paths and sensitive values are removed.

User-entered text must pass the same privacy guard. Secret-like values and endpoint-like values should block preview generation. Private local paths may be redacted to symbolic labels such as `<redacted_local_path>` only if the redaction is deterministic and visible in the redaction summary.

The report should state that excluded data was intentionally not collected or attached.

## Copy, Download, And Local File Policy

- Copyable Markdown is required.
- A browser-generated Markdown download is allowed if it uses the already-sanitized preview body and requires an explicit user action.
- The backend must not write report files to app-data by default in the first slice.
- Backend-written report files are deferred to a later contract and, if later allowed, must be sanitized, user-triggered, local-only, and ignored by Git.
- The implementation must not create or commit generated report files, app-data files, logs, databases, frontend build output, or other local-only artifacts.

## External Submission Boundary

The first slice must not submit reports to external services.

Specifically:

- no automatic GitHub issue creation;
- no direct frontend GitHub API calls;
- no Codex/OpenAI/Google submission;
- no connector/plugin/MCP authorization;
- no OAuth or credential changes;
- no sharing changes;
- no attachment upload.

A later contract may authorize manual GitHub issue creation through a local backend route only if all of the following are true:

- the user reviews the preview first;
- the user performs a second explicit action;
- the backend uses the locally installed GitHub CLI rather than storing tokens;
- the backend verifies the intended repository before submitting;
- external submission is disabled by default in tests;
- validation mocks the submission path and does not create live issues without explicit user approval.

## Backend Contract

The backend may add a narrow feedback/report module and route for preview generation. It should:

- compose a safe diagnostic packet from existing local status helpers;
- validate request fields;
- reject or redact unsafe user-entered values;
- return deterministic Markdown for easy copy/paste comparison in tests;
- avoid subprocess calls in the preview route unless they are strictly safe metadata checks;
- avoid reading raw private files;
- avoid reading raw Player.log content;
- avoid querying arbitrary SQLite contents;
- avoid writing local files by default;
- avoid all external network writes.

The backend must keep report generation separate from parser, analytics ingest, live watcher, Match Journal, and setup behavior.

## Frontend Contract

The frontend may add a small error-report surface to the local app cockpit. It should:

- provide clear fields for user symptom, expected behavior, actual behavior, steps, affected area, and severity;
- request a sanitized backend preview before offering copy/download actions;
- show which diagnostic categories were included;
- show which data categories were excluded;
- expose copyable Markdown;
- keep the surface non-destructive;
- avoid arbitrary file pickers, arbitrary SQL views, raw payload displays, or external submit controls in the first slice.

The UI should keep user-facing language plain and actionable. Developer diagnostics may live behind the existing technical-details boundary.

## Codex Triage Prompt Policy

The generated report may include a pasteable prompt for a future Codex thread. That prompt should instruct Codex to:

- treat the report as sanitized triage evidence, not truth authority;
- inspect the relevant repo files before proposing fixes;
- preserve parser, analytics, live watcher, Match Journal, workbook, and AI boundaries;
- avoid reading local private artifacts unless the user explicitly approves a scoped action;
- route to the Mythic Edge workflow role that fits the failure.

On-command subagent triage remains an operator workflow, not an always-running app feature. Project-scoped `.codex/agents/` files, autonomous triage agents, continuous monitoring, and external submission are deferred.

## Validation Requirements

Codex C should run the smallest relevant validation set, including:

- focused backend tests for preview shape, invalid input, privacy guard behavior, redaction summaries, and no default file writes;
- focused frontend tests for form behavior, preview-before-copy behavior, exclusion messaging, copy fallback, and no external submit control in the first slice;
- tests proving raw private values are not rendered in preview output;
- `npm test` or the repo-approved focused frontend test command when frontend files change;
- `npm run build` when frontend build behavior changes;
- focused `pytest` for local app backend routes when backend files change;
- `ruff` or repo-approved Python formatting/lint checks for touched Python files;
- `git diff --check`;
- path-scoped secret/private-marker scan for changed files;
- path-scoped protected-surface scan for changed files.

Automated validation must not create live GitHub issues, start live Player.log watching, import private JSONL files, read raw Player.log content, or create committed local artifacts.

## Acceptance Criteria

Implementation is acceptable when:

- a sanitized preview route or equivalent safe report composition path exists;
- the frontend lets the user prepare and copy a report without external submission;
- the report includes user symptoms and safe diagnostics;
- unsafe fields are excluded, redacted, or blocked with visible warnings;
- generated reports identify excluded data categories;
- no raw private data appears in tests, snapshots, UI output, or committed artifacts;
- no parser, analytics, live watcher, Match Journal, workbook, webhook, Apps Script, Google Sheets, OpenAI, AI/coaching, Line Tracer, production, or schema behavior changes occur;
- validation evidence demonstrates privacy guard behavior and no automatic external writes.

## Unknowns

- Whether issue #281 will later authorize live GitHub issue creation through local `gh`.
- Whether a future report-file history under app-data is useful enough to justify a separate contract.
- Whether the app needs a dedicated docs page for Codex triage prompts or whether the prompt embedded in the report is sufficient.
- Whether screenshots should ever be supported; they are out of scope for the first slice.

## Suspected Gaps

- No current frontend affordance lets the user package a triage report from the cockpit.
- No backend report composer currently centralizes privacy-safe local status summaries.
- Existing diagnostics are safe individually, but there is no single report schema that records included and excluded diagnostic categories.
- Issue #281 mentions GitHub issue creation, but the current private-local boundary requires copy/preview first and external submission only under a later explicit approval path.

## Protected Surfaces

This contract must not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema, migrations, or ingest behavior;
- live watcher behavior;
- Match Journal truth ownership;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- hidden-card inference;
- archetype inference;
- player-mistake labels;
- gameplay advice;
- secrets, credentials, endpoint values, environment values, or connector authorizations;
- raw logs, generated data, runtime files, database files, local-only artifacts, or workbook exports.

## Expected Codex C Scope

Codex C should compare the current local app against this contract and implement only the first copy-first report-preparation slice. It may add focused backend/frontend tests and minimal docs if needed to make the report shape clear. It should not implement live GitHub submission unless a later explicit user instruction or contract authorizes that scope.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #281.

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

Goal:
Compare the current local app against the contract and implement the first copy-first, local-first sanitized error-report preparation slice for Codex triage.

Implement only:
- a sanitized preview/report composition path;
- a frontend form/preview/copy flow;
- safe included/excluded diagnostic-category messaging;
- focused tests for preview shape, privacy guard behavior, frontend copy flow, and no external submission.

Do not:
- auto-submit to GitHub, Codex, OpenAI, Google, or any external service;
- add live GitHub issue creation unless separately authorized;
- create connector/plugin/OAuth/credential changes;
- read, copy, print, store, or commit raw Player.log content, raw JSONL payloads, raw paths, raw hashes, secrets, endpoint values, spreadsheet IDs, environment values, generated SQLite contents, runtime logs, transport-failure payloads, workbook exports, frontend build output, app-data files, or local-only artifacts;
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest, live watcher behavior, Match Journal truth ownership, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice;
- add destructive UI controls or arbitrary SQL/database browsing;
- target main.

Before editing:
- confirm branch and git status;
- inspect current backend/frontend local app files and tests;
- identify unrelated changes and leave them untouched;
- state the minimal implementation plan.

Validation:
- focused backend tests for report preview/privacy behavior;
- focused frontend tests for report form/preview/copy behavior;
- npm/build validation if frontend build behavior changes;
- git diff --check;
- path-scoped secret/private-marker scan for changed files;
- path-scoped protected-surface scan for changed files.

Final handoff must include files changed, validation run, privacy/protected-surface assessment, remaining risks, next recommended role, and workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex B: Module Contract Writer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/281"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  recent_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/280"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/quality_app_submit_error_report_codex_triage.md"
  risk_tier: "High"
  recommended_first_slice: "copy-first sanitized report preview; no external submission"
  next_recommended_role: "Codex C: Module Implementer"
  stop_conditions:
    - "Do not auto-submit to GitHub, Codex, OpenAI, Google, or any external service."
    - "Do not add live GitHub issue creation unless a later contract or explicit user instruction authorizes it."
    - "Do not read, copy, print, store, or commit raw private artifacts, secrets, endpoint values, generated databases, app-data files, runtime logs, or local-only artifacts."
    - "Do not change parser/runtime/analytics/live watcher/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not target main."
```
