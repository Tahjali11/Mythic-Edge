# Quality App Error Report GitHub Submission Contract

## Module

`quality_app_error_report_github_submission`

Plain English: this contract defines the safe follow-up to the copy-first error-report preview workflow. The local app may let the operator explicitly submit a sanitized report to GitHub Issues after preview review. The app must never auto-file issues, store GitHub tokens, attach private files, or submit raw/local/private artifacts.

This is a contract-writing artifact only. It does not implement code, create GitHub issues, create labels, change runtime behavior, or authorize production-facing behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/298
- Related prior issue: https://github.com/Tahjali11/Mythic-Edge/issues/281
- Prior PR: https://github.com/Tahjali11/Mythic-Edge/pull/282
- Branch: `codex/analytics-foundation`
- Risk tier: High
- Source artifact: GitHub issue #298

Required repo authorities:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

## Tracker

N/A. Issues #204 and #207 are closed historical context, not active trackers for this contract.

## Owning Layer

Primary owning layer: Local App / Backend and UI.

Supporting external-write layer: local GitHub CLI invocation, explicitly controlled by the local operator.

The backend owns submission gating, preview rebuilding, privacy guard execution, label mapping, command construction, and safe fallback results. The frontend owns preview-before-submit flow, user confirmation, success/failure display, and copy fallback.

## Internal Project Area

Primary area: Local App / UI.

Secondary area: Quality / Developer Workflow.

## Truth Owner

The sanitized report is triage evidence only. It is not parser truth, analytics truth, live watcher truth, Match Journal truth, privacy-policy authority, release readiness, or a root-cause diagnosis.

GitHub owns the created issue after successful submission. Mythic Edge local app owns only the explicit submit attempt, safe request/response shape, and fallback report body.

## Bridge-Code Status

`bridge_code`

Bridge details:

- source internal project area: Local App diagnostics and report preview
- consuming external project area: GitHub Issues in `Tahjali11/Mythic-Edge`
- allowed data flow: sanitized preview request to backend privacy guard to local `gh issue create` to returned issue URL
- forbidden reverse-flow: GitHub issue state must not modify parser state, analytics storage, live capture state, Match Journal records, local app config, secrets, credentials, workbook transport, or production behavior

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/quality_app_error_report_github_submission.md`

Future Codex C implementation files authorized, subject to comparison and validation:

- `src/mythic_edge_parser/local_app/error_reports.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- optional new local-app backend helper module under `src/mythic_edge_parser/local_app/`, if separating GitHub submission code from preview code keeps the boundary clearer
- `docs/implementation_handoffs/quality_app_error_report_github_submission_comparison.md`

Reference-only surfaces:

- `docs/contracts/quality_app_submit_error_report_codex_triage.md`
- `docs/contract_test_reports/quality_app_submit_error_report_codex_triage.md`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`, if useful for issue body wording
- current GitHub labels

Not owned by this contract:

- parser modules
- analytics schema, migrations, ingest, or query semantics
- live watcher or capture behavior
- Match Journal repository/service behavior
- workbook/webhook/App Script/Sheets behavior
- OpenAI/model-provider runtime integration
- GitHub label administration
- generated/private/local artifacts

## Observed Current Behavior

Observed on `codex/analytics-foundation` during this contract pass:

- Issue #298 is open.
- The target contract artifact did not exist before this pass.
- The worktree has pre-existing uncommitted local app, live-capture, frontend, and error-report files. This Codex B pass must not revert, stage, or overwrite them.
- Issue #281 and PR #282 completed the copy-first report preview slice.
- The backend currently exposes `POST /api/feedback/error-report/preview`.
- The current preview response includes schema `quality_app_submit_error_report_codex_triage.v1`, `status`, `issue_title`, `issue_body_markdown`, included diagnostics, excluded private data, redaction summary, warnings, next recommended role, and `external_submission_enabled: false`.
- Focused tests currently verify preview shape, redaction, privacy blocking, invalid requests, and absence of `/api/feedback/error-report/submit`.
- The frontend currently exposes preview/copy behavior and labels external submission disabled.
- Current GitHub labels include `bug`, `enhancement`, `question`, `workflow:problem`, and `layer:dashboard`.
- Current GitHub labels do not include dedicated `feedback` or `feature-request` labels.

## Contract Decision

Issue #298 should authorize a new explicit submit route and UI action that creates a GitHub Issue only after the sanitized preview path succeeds.

Approved first slice:

- add a backend submit route: `POST /api/feedback/error-report/submit`;
- accept the same structured request shape as preview;
- rebuild the sanitized preview server-side immediately before submission;
- run the privacy guard immediately before issue creation;
- use local `gh issue create` through argument-list subprocess execution;
- target only `Tahjali11/Mythic-Edge`;
- map report type to existing labels with graceful fallbacks;
- return a structured success or safe fallback response;
- show a frontend `Submit report` action only after preview is ready and backend capability says external submission is enabled;
- keep `Copy Report` fallback available in every non-submitted or failed state;
- use mocked GitHub submission in automated tests.

Not approved:

- automatic issue filing;
- frontend-direct GitHub API calls;
- storing GitHub tokens in app config;
- runtime creation of labels;
- attachments;
- screenshots;
- report file history;
- telemetry or remote logging;
- continuous monitoring;
- arbitrary GitHub operations;
- live GitHub issue creation in automated tests.

## Public Interface

### Existing Preview Route

The existing preview route remains the source of the sanitized report body:

```text
POST /api/feedback/error-report/preview
```

The preview route must remain usable without GitHub CLI availability. It must still return `external_submission_enabled: false` unless Codex C explicitly updates the capability model in a compatible way.

### New Submit Route

Codex C may add:

```text
POST /api/feedback/error-report/submit
```

The submit route must be local loopback-only through the existing local app backend. It must not be callable as a generic GitHub operation. It must submit only a sanitized Mythic Edge error report to `Tahjali11/Mythic-Edge`.

### Submit Request Shape

The submit route should accept the same request fields as preview:

- `summary`
- `report_type`
- `affected_area`
- bug fields: `expected_behavior`, `actual_behavior`, optional `reproduction_steps`
- feedback field: `feedback`
- feature-request fields: `feature_goal`, `feature_location`, `feature_success`
- `current_frontend_surface`, optional
- `include_diagnostics`, optional
- `selected_job_id`, optional if already supported by preview diagnostics

Codex C may add an optional `preview_acknowledged` boolean or `preview_nonce` only if needed to prove preview-first UX. The backend must still rebuild the preview and privacy guard server-side; it must not trust frontend preview text as the submitted body.

### Submit Response Shape

Response object:

```text
object: mythic_edge_local_app_error_report_submission
schema_version: quality_app_error_report_github_submission.v1
```

Top-level fields:

- `object`
- `schema_version`
- `status`
- `external_submission_enabled`
- `submitted`
- `issue_url`
- `issue_number`
- `issue_title`
- `issue_body_markdown`
- `labels`
- `fallback_available`
- `warnings`
- `errors`

Allowed `status` values:

- `submitted`
- `preview_required`
- `blocked_privacy_guard`
- `blocked_missing_gh`
- `blocked_gh_unauthenticated`
- `blocked_wrong_repo`
- `blocked_label_unavailable`
- `submission_failed`
- `invalid_request`

On success:

- `status`: `submitted`
- `submitted`: `true`
- `issue_url`: GitHub issue URL
- `issue_number`: created issue number when safely parsed
- `fallback_available`: `true`
- `issue_body_markdown`: the same sanitized body submitted

On failure:

- `submitted`: `false`
- `issue_url`: `null`
- `issue_number`: `null`
- `fallback_available`: `true`
- `issue_body_markdown`: sanitized copyable fallback when preview was ready
- `errors`: safe error codes only

The response must not include raw command stderr, raw stack traces, sensitive local paths, environment values, tokens, auth details, or unredacted user-entered unsafe values.

## GitHub Auth And Tool Boundary

Approved first implementation path: local GitHub CLI.

Reason:

- uses the operator's existing local GitHub authentication;
- avoids storing tokens in Mythic Edge config;
- can be mocked cleanly in tests;
- keeps the external write behind backend validation.

Required command behavior:

- use argument-list subprocess execution, not shell string concatenation;
- use an explicit repo argument: `--repo Tahjali11/Mythic-Edge`;
- use an explicit title argument from the rebuilt sanitized preview;
- pass the body through a safe temporary file or a safe stdin/body-file mechanism;
- delete any temporary body file immediately after the command finishes;
- never create a persistent report file by default;
- set a short timeout;
- capture output for parsing but return only safe parsed status;
- do not echo raw stderr/stdout to API responses.

The backend may verify `gh` availability and auth using safe commands such as `gh auth status` and may verify repository access with a safe metadata call. It must not print credential details, auth tokens, usernames from paths, or raw tool output to the frontend.

The GitHub API is deferred for this first slice. A future contract may authorize API use if the project later needs non-CLI submission, but it must define token storage and credential policy first.

## Label And Classification Contract

The app must not create labels dynamically at runtime.

Current label observation:

- available: `bug`
- available: `enhancement`
- available: `question`
- available: `workflow:problem`
- available: `layer:dashboard`
- absent: `feedback`
- absent: `feature-request`

Required first-slice label mapping:

| Report type | Required title tag | Preferred labels when available | Fallback labels |
| --- | --- | --- | --- |
| `bug` | `[error-report] [bug] [affected_area] ...` | `bug`, `workflow:problem`, safe area label | `bug`, `workflow:problem`, `layer:dashboard` |
| `feedback` | `[error-report] [feedback] [affected_area] ...` | `feedback`, `workflow:problem`, safe area label | `question`, `workflow:problem`, `layer:dashboard` |
| `feature_request` | `[error-report] [feature_request] [affected_area] ...` | `feature-request`, `workflow:problem`, safe area label | `enhancement`, `workflow:problem`, `layer:dashboard` |

The submitter should use available labels only. Missing optional preferred labels must degrade to fallback labels instead of blocking submission. Missing baseline labels such as `workflow:problem` or the fallback report-type label should return `blocked_label_unavailable` with the sanitized copy fallback.

Area labels:

- `layer:dashboard` is acceptable for local app UI, analytics app, feedback, and general local app reports.
- Parser, webhook, workbook, or other layer labels must be used only if the label exists and the report area clearly maps to it.
- The issue body must carry the exact `affected_area` regardless of label availability.

## Privacy Guard Contract

The submit route must run privacy checks immediately before GitHub issue creation by rebuilding the sanitized preview server-side.

The submit route must refuse to submit if preview status is not `preview_ready`.

The submit route must not submit or attach:

- raw Player.log files;
- raw Player.log lines;
- raw JSONL artifacts;
- saved-event lines;
- SQLite database files;
- SQLite table contents;
- SQLite sidecar files;
- runtime logs;
- transport-failure payload artifacts;
- workbook exports;
- screenshots in the first slice;
- full private local paths;
- raw file hashes;
- secrets;
- credentials;
- tokens;
- OAuth values;
- endpoint values;
- spreadsheet IDs;
- environment values;
- arbitrary local files;
- generated/private/local-only artifacts.

User-entered text must pass the same privacy guard used by preview. Secret-like, endpoint-like, token-like, raw-hash-like, and unsafe values must block submission without echoing the unsafe value.

Private path-like user text may be redacted only when the preview guard already redacts it deterministically and includes a visible redaction summary.

## Preview Rebuild Policy

The submit route must not accept `issue_title` or `issue_body_markdown` from the frontend as authority.

Required flow:

1. receive structured report request;
2. rebuild preview server-side;
3. verify rebuilt preview status is `preview_ready`;
4. compute labels from rebuilt `report_type` and `affected_area`;
5. check label availability or use fallback labels;
6. submit the rebuilt title/body through `gh issue create`;
7. return issue URL or sanitized fallback.

This prevents stale or modified frontend preview content from bypassing privacy checks.

## Frontend UX Contract

Required frontend states:

- editing report;
- preview loading;
- preview ready;
- preview blocked/invalid;
- submit available;
- submitting;
- submitted;
- submission unavailable;
- submission failed with copy fallback.

Required UX rules:

- preview must happen before submit;
- `Submit report` must be visible only after preview is `preview_ready` and backend capability says external submission is enabled;
- button copy must make the external write clear, for example: `Submit report to GitHub`;
- a confirmation phrase or explanatory line must say the action creates a GitHub Issue in `Tahjali11/Mythic-Edge`;
- submission must require a deliberate user click;
- no automatic submission from runtime errors;
- `Copy Report` remains available after preview and after failed submission;
- success state must show a safe issue URL link;
- failure states must show safe status labels and copy fallback;
- no attachments or screenshot controls in the first slice.

Frontend must not store report bodies in browser storage. It may keep in-memory form state for the current session.

## Fallback Behavior

Fallback must be copy-first and safe.

Fallback is required when:

- GitHub CLI is missing;
- GitHub CLI is unavailable;
- GitHub CLI is unauthenticated;
- repository verification fails;
- labels are unavailable and no safe fallback exists;
- submission times out;
- command exits with an error;
- privacy guard blocks submission;
- network is unavailable;
- response parsing fails.

Fallback response must include:

- sanitized `issue_title`;
- sanitized `issue_body_markdown`;
- safe error/status code;
- clear instruction that no GitHub issue was created;
- `fallback_available: true`.

Fallback must not include raw command stderr/stdout or credential/tooling details.

## Duplicate And Noise Control

First slice duplicate control should be lightweight:

- title prefix `[error-report]`;
- report-type and affected-area title tags;
- preview-before-submit;
- optional frontend warning if the current session has already submitted the same preview title/body;
- disabled submit button while a submit attempt is in flight.

Do not add a server-side duplicate detector or GitHub search gate in the first slice unless Codex C finds a very small safe implementation and routes it back for contract clarification.

## Error Behavior

Invalid request:

- return `invalid_request`;
- include safe invalid field codes;
- no GitHub command runs.

Privacy blocked:

- return `blocked_privacy_guard`;
- include safe privacy warning codes;
- no GitHub command runs.

Missing GitHub CLI:

- return `blocked_missing_gh`;
- include copy fallback;
- do not attempt submission.

Unauthenticated GitHub CLI:

- return `blocked_gh_unauthenticated`;
- include copy fallback;
- do not expose raw auth output.

Wrong repo or unavailable repo:

- return `blocked_wrong_repo`;
- include copy fallback;
- do not submit to any alternate repo.

Missing labels:

- use fallbacks where allowed;
- return `blocked_label_unavailable` only when baseline labels required by this contract are unavailable.

Submission failure:

- return `submission_failed`;
- include copy fallback;
- do not expose raw command output.

## Side Effects

Allowed side effects during explicit successful submit:

- a GitHub Issue is created in `Tahjali11/Mythic-Edge`;
- a short-lived temporary Markdown body file may be created and deleted during command execution;
- frontend in-memory state may record success/failure for the current session.

Forbidden side effects:

- automatic issue creation;
- GitHub label creation;
- GitHub token storage;
- attachment upload;
- report file history;
- telemetry;
- remote logging;
- parser behavior changes;
- analytics schema/migration/ingest changes;
- live watcher behavior changes;
- Match Journal behavior changes;
- workbook/webhook/App Script/Sheets behavior changes;
- OpenAI/model-provider calls;
- production behavior changes;
- generated/private/local artifact commits;
- staging, commit, push, PR, merge, or issue closure unless explicitly requested by a later role.

## Compatibility

Implementation must preserve:

- existing preview route request shape;
- existing preview response fields;
- existing privacy blocking and redaction behavior;
- existing copy-first fallback behavior;
- existing local app backend health/setup/status routes;
- existing live capture controls;
- existing manual import behavior;
- existing Match Journal behavior;
- existing no-attachment posture.

The submit route may add new response types and frontend API helpers, but it must not break existing preview tests or consumers.

## Unknowns

- Whether dedicated `feedback` and `feature-request` labels should be created later by a human or a separate repo-label governance issue.
- Whether a future issue should add attachments or screenshots. They are forbidden in this first slice.
- Whether a future non-CLI GitHub API path is useful. It is deferred until token and credential policy is contracted.
- Whether issue templates should be updated for error reports. This contract does not authorize template edits.

## Suspected Gaps

- No submit route currently exists.
- Current frontend explicitly says external submission is disabled.
- Current tests assert the submit route is absent; Codex C must update those tests when implementing #298.
- Current report preview schema is for Codex triage. Codex C must either preserve it for preview and add a separate submission schema, or add compatible submit-only fields without breaking preview.
- Runtime label availability is not currently represented in the preview response.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema, migrations, or ingest behavior;
- live watcher behavior;
- live capture semantics;
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
- GitHub label administration;
- credential or environment-variable policy.

Do not expose raw Player.log content, private JSONL payloads, generated SQLite contents, full private paths, sensitive local values, screenshots, arbitrary local files, arbitrary SQL, database browsing, destructive controls, secrets, tokens, endpoint values, spreadsheet IDs, environment values, generated/private/local artifacts, or raw tool output.

## Tests Required

Codex C must add or update backend tests proving:

- `POST /api/feedback/error-report/submit` exists;
- submit accepts the same structured request as preview;
- submit rebuilds preview server-side;
- submit refuses non-ready preview results;
- privacy-blocked request does not call GitHub tooling;
- invalid request does not call GitHub tooling;
- successful submission uses mocked `gh issue create`;
- command invocation uses argument-list execution, not shell string concatenation;
- target repo is exactly `Tahjali11/Mythic-Edge`;
- temporary body file, if used, is removed after success and failure;
- missing `gh` returns `blocked_missing_gh` with copy fallback;
- unauthenticated `gh` returns `blocked_gh_unauthenticated` with copy fallback;
- wrong repo/unavailable repo returns `blocked_wrong_repo` with copy fallback;
- missing optional `feedback` or `feature-request` labels uses fallback labels;
- missing required baseline labels returns `blocked_label_unavailable`;
- submission failure returns `submission_failed` with copy fallback;
- no raw/private markers appear in response bodies.

Codex C must add or update frontend tests proving:

- preview-before-submit behavior;
- `Submit report to GitHub` appears only after preview is ready and external submission is enabled;
- no submit happens automatically;
- submit button is disabled while submission is in flight;
- success state renders safe issue URL;
- failure states preserve `Copy Report` fallback;
- blocked preview does not expose submit;
- no attachments or screenshot controls appear;
- no raw/private values are displayed.

No automated validation may create a live GitHub Issue. Live submission must be mocked in tests. A manual live smoke may be run only with explicit user approval, using a deliberately safe synthetic report, and must record the created issue URL plus cleanup/closure routing if the user asks for it.

Recommended validation:

```powershell
py -m pytest -q tests\test_analytics_local_app_backend.py
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
```

Codex C and Codex E must also run path-scoped protected-surface and secret/private-marker scans over changed files:

```powershell
@'
<changed file paths>
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

@'
<changed file paths>
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

If `npm --prefix frontend run build` creates `frontend/dist`, generated build output must be removed before handoff unless a later contract explicitly authorizes committing it.

## Acceptance Criteria

- `docs/contracts/quality_app_error_report_github_submission.md` exists.
- The contract defines `POST /api/feedback/error-report/submit`.
- The contract requires preview rebuild and privacy guard immediately before submission.
- The contract selects local `gh issue create` as the first implementation path.
- The contract forbids GitHub token storage in app config.
- The contract defines label mapping with current-label fallbacks.
- The contract forbids runtime label creation.
- The contract defines submit response shape and failure statuses.
- The contract defines frontend preview-first submit UX.
- The contract requires mocked GitHub submission tests and forbids live issue creation in automated tests.
- The contract preserves parser/runtime/analytics/live watcher/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production boundaries.
- No implementation, external write, label creation, PR, merge, issue closure, or main-target work is performed in the Codex B pass.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #298.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/298

Related prior issue:
https://github.com/Tahjali11/Mythic-Edge/issues/281

Branch:
codex/analytics-foundation

Contract:
docs/contracts/quality_app_error_report_github_submission.md

Goal:
Compare the current copy-first error-report preview implementation against the contract, then implement the smallest safe explicit GitHub Issue submission flow. Preserve preview-first behavior, privacy guards, local-operator-only external writes, and copy fallback.

Before editing:
- Confirm branch and git status.
- Identify unrelated dirty files and do not revert them.
- Read issue #298, the #281 contract/report, and the #298 contract.
- Inspect error_reports.py, backend.py, frontend App/api/types/tests, backend tests, and current GitHub label assumptions.
- State the minimal implementation plan.

Do:
- Add POST /api/feedback/error-report/submit.
- Rebuild sanitized preview server-side immediately before submission.
- Refuse submission unless rebuilt preview status is preview_ready.
- Use local gh issue create through argument-list subprocess execution.
- Target exactly Tahjali11/Mythic-Edge.
- Map Bug/Feedback/Feature Request to available labels with contracted fallbacks.
- Return structured success or safe fallback responses.
- Keep Copy Report fallback available.
- Add backend tests with mocked GitHub tooling for success, missing gh, unauthenticated gh, wrong repo, label fallback/blocking, privacy-blocked, invalid request, and submission failure.
- Add frontend tests for preview-first submit, visibility/enabled states, success URL, fallback behavior, and absence of automatic submit/attachments.
- Produce docs/implementation_handoffs/quality_app_error_report_github_submission_comparison.md.

Do not:
- create a live GitHub Issue in automated tests;
- auto-file issues from runtime errors;
- store GitHub tokens in app config;
- create labels dynamically at runtime;
- attach files or screenshots;
- expose raw Player.log content, private JSONL payloads, SQLite contents, full private paths, sensitive local values, raw tool output, secrets, endpoint values, spreadsheet IDs, environment values, runtime logs, transport-failure payloads, workbook exports, generated/private/local artifacts, arbitrary SQL, or database browsing;
- change parser behavior, parser final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest, live watcher behavior, live capture semantics, Match Journal truth ownership, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice;
- target main;
- stage, commit, push, open a PR, merge, create labels, or close issues unless explicitly asked.

Validation:
- py -m pytest -q tests\test_analytics_local_app_backend.py
- npm --prefix frontend run typecheck
- npm --prefix frontend run test -- --run
- npm --prefix frontend run build
- py -m ruff check src tests tools
- git diff --check
- py tools/check_agent_docs.py
- path-scoped protected-surface and secret/private-marker scans over changed files
- remove frontend/dist before final handoff if build created it

Final output:
- role performed
- issue and contract used
- files changed
- implementation summary
- validation run
- protected-surface and private-artifact status
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/298"
  related_prior_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/281"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #298"
  contract_artifact: "docs/contracts/quality_app_error_report_github_submission.md"
  target_artifact: "docs/implementation_handoffs/quality_app_error_report_github_submission_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "Codex B docs-only validation: git diff --check"
    - "Codex B docs-only validation: py tools\\check_agent_docs.py"
    - "Codex B docs-only validation: path-scoped protected-surface scan for the contract"
    - "Codex B docs-only validation: path-scoped secret/private-marker scan for the contract"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not create a live GitHub Issue in Codex B."
    - "Do not target main."
    - "Do not auto-file issues from runtime errors."
    - "Do not store GitHub tokens in app config."
    - "Do not create labels dynamically from app runtime."
    - "Do not attach raw/private files or screenshots."
    - "Do not change parser/runtime/analytics/live watcher/live capture/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
