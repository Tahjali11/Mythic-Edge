# Local Request Guard For Mutating Loopback Routes Contract

## Module

`security_local_request_guard_mutating_loopback_routes`

Plain English: this contract defines a local request guard for Mythic Edge's
loopback-only local app backend. A request guard is a per-backend-session secret
value, sent in a custom request header, that lets the backend reject
state-changing local app requests that did not come through the intended local
frontend session.

This is a Codex B contract artifact only. It does not implement code, change
CI, mutate CodeQL alerts, change parser behavior, change analytics truth, or
claim security assurance.

## Source Issue

- Child issue: https://github.com/Tahjali11/Mythic-Edge/issues/458
- Parent security workflow:
  https://github.com/Tahjali11/Mythic-Edge/issues/330
- Related follow-up: https://github.com/Tahjali11/Mythic-Edge/issues/459
- Contract artifact:
  `docs/contracts/security_local_request_guard_mutating_loopback_routes.md`

## Tracker

Parent security workflow #330 remains open. Issue #458 remains the focused
local-app request-guard child issue. Issue #459 remains the later upload byte
limit / upload hardening child and should inherit this request-guard posture
without being implemented here.

## Owning Layer

Local App / Security-quality hardening.

The request guard owns only local backend mutation authorization for the
private local app. It does not own parser truth, analytics truth, Match Journal
truth, workbook truth, webhook truth, Apps Script behavior, Google Sheets
behavior, OpenAI/AI behavior, production behavior, CodeQL lifecycle truth, or
security/privacy assurance.

## Internal Project Area

Local app security boundary.

Adjacent areas:

- frontend API wiring;
- FastAPI local backend route wiring;
- local app diagnostics and error-reporting redaction;
- browser JSONL import/upload;
- Match Journal local write facade;
- live capture process controls.

## Truth Owner

- Backend local request guard state owns whether a mutating local app request
  carries the current process-local guard value.
- Existing route handlers still own their current domain behavior after the
  guard passes.
- Existing parsers, analytics ingest, Match Journal service, JSONL import
  adapter, and error-report builders keep their existing truth boundaries.
- GitHub CodeQL remains an external alert lifecycle signal, not a local
  authorization authority.

The guard must never convert local app requests into parser truth, analytics
truth, AI truth, security assurance, privacy assurance, release readiness, or
production readiness.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- issue #458
- parent issue #330
- issue #458 Codex A refinement comment after #610 / PR #614
- `docs/contracts/security_quality_scanner_summary_aggregation.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_match_journal_cockpit_ui_backend.py`
- current branch/worktree status on
  `codex/security-next-prevention-330`

## Observed Current Behavior

`src/mythic_edge_parser/local_app/backend.py` creates a loopback local FastAPI
backend with explicit CORS origins:

- `http://127.0.0.1:5173`
- `http://localhost:5173`
- an optional loopback value from `MYTHIC_EDGE_LOCAL_APP_FRONTEND_ORIGIN`

The backend currently allows CORS request headers:

- `Accept`
- `Content-Type`

The backend currently has no explicit per-session request guard for mutating
routes. The current registered POST routes are:

| Route | Current purpose | Current guard status |
| --- | --- | --- |
| `POST /api/live/capture/start` | start local live capture | unguarded |
| `POST /api/live/capture/stop` | stop local live capture | unguarded |
| `POST /api/feedback/error-report/preview` | build sanitized report preview | unguarded |
| `POST /api/feedback/error-report/submit` | explicitly submit sanitized report to GitHub | unguarded |
| `POST /api/journal/notes` | write Match Journal note | unguarded |
| `POST /api/journal/opponent-labels` | write local opponent labels | unguarded |
| `POST /api/journal/review-flags` | write review flags | unguarded |
| `POST /api/journal/experiment-label` | write experiment label | unguarded |
| `POST /api/journal/display-corrections` | write display correction | unguarded |
| `POST /api/imports/jsonl` | start manual JSONL import by local path | unguarded |
| `POST /api/imports/jsonl/upload` | accept browser-uploaded JSONL files | unguarded |

The current frontend API helpers call those routes with `fetch` and route-local
headers, but they do not include a guard header.

Existing tests already check route inventory, loopback CORS, disabled docs, and
absence of DELETE routes. Those tests should be preserved and extended rather
than replaced.

## Problem Statement

Loopback binding and CORS are useful local app boundaries, but they are not the
same as a request guard. A browser or local process can still attempt a
state-changing request to the loopback backend. Mythic Edge needs an explicit,
local-only, fail-closed proof on mutating requests so the backend can reject
requests that were not issued through the intended local app session.

This guard is a local hardening layer. It is not user authentication, cloud
authorization, OAuth, formal CSRF protection for a public website, malware
protection against a fully compromised local machine, or a production security
claim.

## Required Guarantees

Codex C must implement a local request guard that guarantees:

1. Every current registered local app POST route listed in this contract is
   guarded.
2. Future registered non-GET local app API routes must either use the guard or
   be explicitly listed as exempt with a contract-backed reason.
3. Read-only GET routes remain callable without the guard in this first slice
   unless a later contract classifies a specific read route as sensitive.
4. Unsupported methods should keep normal FastAPI behavior where practical; for
   example, `POST /api/health` should remain a method error rather than turning
   into a request-guard failure.
5. Guard values are generated locally, stored only in backend process memory,
   and never written to disk, config, environment variables, reports, logs,
   local storage, session storage, SQLite, issue bodies, or screenshots.
6. Guard failures return public-safe errors that do not reveal the expected
   token, the received token, private paths, endpoint values, environment
   values, or local artifact contents.
7. The frontend includes the guard value only in an HTTP request header for
   guarded mutating requests.
8. The guard does not change parser behavior, analytics schema, ingest
   semantics, Match Journal truth ownership, workbook/webhook/App Script/Sheets
   behavior, OpenAI/AI/coaching behavior, or production behavior.

## Guarded Route Inventory

Codex C must guard these current routes:

### Live Capture

- `POST /api/live/capture/start`
- `POST /api/live/capture/stop`

Rationale: these routes change live capture process/state. They must require a
valid guard before any precondition checks or state changes happen.

### Feedback And Error Reports

- `POST /api/feedback/error-report/preview`
- `POST /api/feedback/error-report/submit`

Rationale: `submit` is an external write. `preview` is also guarded because it
packages diagnostics and issue text that could reveal local status if triggered
outside the intended app session. The guard must not weaken the existing
preview-first and sanitized-submission rules.

### Match Journal Writes

- `POST /api/journal/notes`
- `POST /api/journal/opponent-labels`
- `POST /api/journal/review-flags`
- `POST /api/journal/experiment-label`
- `POST /api/journal/display-corrections`

Rationale: these routes write local human annotations. The guard must prevent
cross-session or unintended browser-origin writes while preserving current
Match Journal payload validation and service fail-closed behavior.

### Manual And Browser JSONL Import

- `POST /api/imports/jsonl`
- `POST /api/imports/jsonl/upload`

Rationale: these routes can start import work, read operator-supplied local
paths, or receive uploaded local files. The guard is required before path or
upload processing begins.

### Future Local App Mutations

Any future `POST`, `PUT`, `PATCH`, or `DELETE` route under `/api/` must be
guarded by default unless a later contract explicitly exempts it.

Likely future examples include:

- local app config write routes;
- setup wizard write routes;
- launcher or process-control routes;
- import job mutation routes;
- future feedback submission routes.

## Unguarded Route Rationale

The following current route families may remain unguarded in this first slice
because they are read-only status or data-display routes:

- `GET /api/health`
- `GET /api/app/setup-status`
- `GET /api/app/config`
- `GET /api/app/paths`
- `GET /api/analytics/database/status`
- `GET /api/live/player-log/status`
- `GET /api/live/watcher/status`
- `GET /api/live/watcher/process`
- `GET /api/live/watcher/diagnostics`
- `GET /api/live/ingest/status`
- `GET /api/live/capture/status`
- analytics history / dashboard / refresh-state GET routes
- `GET /api/runtime/status`
- `GET /api/journal`
- `GET /api/journal/notes`
- `GET /api/imports/jobs/{job_id}`

This does not make those routes public or unrestricted. They must keep the
existing loopback and redaction boundaries. If a later contract determines that
a read route exposes sensitive diagnostics, that route can be separately
guarded without expanding this mutation-focused issue.

## Token Lifecycle Contract

### Token Generation

The backend must generate an opaque, high-entropy guard value when the local app
backend process starts.

Required properties:

- generated with Python's cryptographic randomness facilities, such as
  `secrets.token_urlsafe` or equivalent;
- at least 128 bits of entropy;
- opaque to the frontend;
- not derived from usernames, machine paths, process IDs, ports, timestamps,
  environment values, Player.log metadata, SQLite state, Git refs, or local
  artifacts;
- regenerated on backend process restart.

### Token Storage

The guard value must be stored only in backend process memory, such as FastAPI
application state or a narrow local request-guard object owned by the app
factory.

Forbidden storage:

- repository files;
- app-data files;
- JSON config;
- environment variables;
- SQLite;
- logs;
- diagnostics reports;
- generated reports;
- browser `localStorage`;
- browser `sessionStorage`;
- query strings;
- request bodies;
- issue bodies.

### Header Name

Use a single custom request header:

```text
X-Mythic-Edge-Local-Request-Guard
```

The backend must treat header names case-insensitively, as HTTP normally does,
but tests should use this canonical spelling.

### Bootstrap Endpoint

Codex C may add a read-only bootstrap endpoint, recommended:

```text
GET /api/app/request-guard
```

This endpoint is allowed only to return the guard metadata needed by the
frontend:

```json
{
  "object": "mythic_edge_local_request_guard",
  "schema_version": 1,
  "status": "available",
  "header_name": "X-Mythic-Edge-Local-Request-Guard",
  "token": "<opaque process-local token>",
  "expires_on_backend_restart": true,
  "warnings": [],
  "errors": []
}
```

The endpoint must not return private paths, environment values, Player.log
metadata, SQLite contents, report contents, local artifact names, or route
payloads.

The endpoint itself remains a local bootstrap surface, not a public
authentication service. It must be subject to the existing loopback/CORS
origin posture. If `Origin` is present, it must be one of the allowed loopback
frontend origins.

## Backend Enforcement Contract

Codex C should prefer a shared backend guard helper or route dependency applied
to each registered mutating route, plus a route-inventory test that fails when
a new mutating `/api/` route is added without guard classification.

A broad middleware is acceptable only if it preserves normal `405 Method Not
Allowed` behavior for unsupported methods and does not interfere with CORS
preflight. Do not implement a middleware that blindly returns guard failures
for every non-GET request path before FastAPI route matching.

The enforcement order for guarded routes must be:

1. Host/origin safety checks;
2. guard header presence;
3. guard header value comparison;
4. route-specific request parsing and behavior.

Route-specific behavior must not run when the guard fails.

Use constant-time comparison, such as `hmac.compare_digest`, or an equivalent
safe comparison helper for token validation.

### Host And Origin Checks

Host and origin checks are defense-in-depth and must not replace the guard.

Required behavior:

- If `Origin` is present on a guarded route, it must match one of the resolved
  allowed loopback frontend origins.
- If `Origin` is absent but the guard is valid, the backend may allow the
  request to support local non-browser clients and focused tests.
- If `Host` is available in a real HTTP request, it must be loopback-compatible
  (`127.0.0.1` or `localhost`, with an allowed port shape).
- Focused tests may set a loopback `base_url` or loopback `Host` header rather
  than relying on FastAPI TestClient's default `testserver` host.

### Failure Status Codes

Guard failures must use public-safe JSON errors. The exact response envelope
may follow existing local app error conventions, but must preserve these codes:

| Failure | HTTP status | Error code |
| --- | --- | --- |
| missing guard header | `401` | `local_request_guard_missing` |
| blank guard header | `401` | `local_request_guard_missing` |
| invalid guard value | `403` | `local_request_guard_invalid` |
| disallowed `Origin` | `403` | `local_request_origin_not_allowed` |
| disallowed `Host` | `403` | `local_request_host_not_allowed` |
| guard unavailable because backend failed to initialize it | `503` | `local_request_guard_unavailable` |

Failure responses must not include:

- expected token;
- received token;
- token length;
- private paths;
- environment values;
- endpoint values;
- stack traces;
- local artifact contents.

### CORS Contract

If the frontend sends the custom guard header, backend CORS must allow it:

```text
Accept
Content-Type
X-Mythic-Edge-Local-Request-Guard
```

CORS preflight `OPTIONS` requests must not require the guard token.

Existing loopback-only origin filtering must remain. Do not add wildcard
origins, non-loopback origins, broad `allow_credentials`, or production-facing
CORS behavior.

## Frontend API Wiring Contract

Codex C must route all guarded frontend requests through one shared guarded
request helper or equivalent narrow API client layer.

Required frontend behavior:

1. Fetch the guard once from the backend bootstrap endpoint after the backend
   is reachable.
2. Keep the token in process/browser memory only.
3. Include `X-Mythic-Edge-Local-Request-Guard` on every guarded POST request.
4. Do not include the token on read-only GET routes unless a later contract
   explicitly requires it.
5. Do not include the token in URLs, query strings, request bodies, visible UI,
   console logs, error-report preview text, GitHub issue bodies, screenshots,
   or generated artifacts.
6. If the guard cannot be fetched, display or route a blocked/degraded local
   app state rather than attempting mutating requests without the header.

The current frontend POST helpers that must be converted to the shared guarded
path are:

- `startLiveCapture`
- `stopLiveCapture`
- `previewErrorReport`
- `submitErrorReport`
- `submitManualJsonlImport`
- `submitManualJsonlUpload`
- `submitMatchJournalNote`
- `submitMatchJournalOpponentLabels`
- `submitMatchJournalReviewFlag`
- `submitMatchJournalExperimentLabel`
- `submitMatchJournalDisplayCorrection`

## Privacy And Redaction Contract

The guard value is a local session secret. It must be treated as private even
though it is not a durable credential.

The following surfaces must exclude or redact the token and token-like header
values:

- error report preview;
- error report GitHub submission body;
- frontend error display;
- backend logs;
- test failure snapshots, if any;
- setup/status payloads other than the dedicated bootstrap endpoint;
- generated quality/security reports;
- contract-test reports;
- workflow handoff blocks.

If Codex C changes any diagnostic collector, it must add tests showing the
guard header value is not included in report bodies or local app diagnostic
payloads.

## Relationship To Issue #459

Issue #459 remains separate. This contract may guard
`POST /api/imports/jsonl/upload`, but it must not implement upload byte-limit
hardening, streaming upload changes, upload quarantine, file retention changes,
or browser upload redesign.

After #458 is implemented and reviewed, #459 should inherit the guarded upload
route and focus on upload size, memory, and file-handling boundaries.

## Out Of Scope

This contract does not authorize:

- cloud auth;
- user accounts;
- OAuth;
- durable credential storage;
- persistent request tokens;
- environment-variable contract changes for the guard token;
- public deployment;
- production behavior;
- CI changes;
- CodeQL alert mutation or dismissal;
- parser behavior changes;
- parser state final reconciliation changes;
- parser event class changes;
- match/game identity or deduplication changes;
- analytics schema or migration changes;
- analytics truth changes;
- Match Journal truth ownership changes;
- workbook schema changes;
- webhook payload changes;
- Apps Script changes;
- Google Sheets behavior changes;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- raw Player.log handling;
- raw JSONL artifact storage;
- SQLite content exposure;
- generated/local artifact commits;
- upload byte-limit hardening from #459.

## Validation Requirements

### Codex C Required Validation

Codex C must run focused validation after implementation:

```powershell
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_live_app_explicit_start_capture_control.py
py -m ruff check src\mythic_edge_parser\local_app tests
npm --prefix frontend run test -- --run frontend/src/api.test.ts frontend/src/App.test.tsx
git diff --check
```

Codex C must also run path-scoped protected-surface and secret/private-marker
scans over changed files.

### Backend Test Expectations

Backend tests must prove:

- every guarded route rejects missing guard values;
- every guarded route rejects invalid guard values;
- every guarded route accepts a valid guard value and then preserves existing
  route-specific behavior;
- route-specific behavior is not called when the guard fails;
- disallowed `Origin` fails even when a guard-like header is present;
- CORS preflight allows the custom guard header for approved loopback origins;
- unsupported methods preserve appropriate method errors where practical;
- read-only GET routes that remain unguarded still work without the guard;
- the route inventory fails when a mutating route is added without guard
  classification.

### Frontend Test Expectations

Frontend tests must prove:

- guarded API helpers include the custom guard header;
- GET helpers do not include the guard header by default;
- missing/unavailable guard state blocks mutating helper calls or maps to a
  clear degraded state;
- multipart upload uses the custom guard header without setting an unsafe
  manual `Content-Type`;
- error report preview/submission does not include the token in generated issue
  text or fallback copy text.

### Codex E Review Expectations

Codex E must verify:

- every current POST route is guarded;
- no new unclassified mutating route was added;
- no route writes state before guard validation;
- no guard value is persisted, logged, displayed, or committed;
- CORS remains loopback-only;
- existing tests were updated intentionally rather than weakened;
- #459 scope was not absorbed;
- no parser, analytics, workbook, webhook, Apps Script, Google Sheets, AI,
  coaching, or production behavior changed.

## Acceptance Criteria

This issue is acceptable when:

- `docs/implementation_handoffs/security_local_request_guard_mutating_loopback_routes_comparison.md`
  compares current backend/frontend behavior to this contract;
- all current local app POST routes are guarded;
- the backend exposes a narrow process-local guard bootstrap path or an
  equivalent safe frontend delivery mechanism;
- frontend mutating calls include the guard consistently;
- failures are public-safe and use the required status/code vocabulary;
- guard values are not persisted or included in reports;
- focused backend and frontend tests pass;
- path-scoped protected-surface and secret/private scans do not show new
  forbidden exposure;
- #459 remains open or separately routed if upload byte-limit hardening still
  needs work.

## Unknowns

- Whether Codex C will choose a route dependency, explicit helper, or
  route-preserving middleware. Any choice is acceptable if it satisfies this
  contract and preserves unsupported-method behavior.
- Whether the implementation should expose the bootstrap endpoint as
  `/api/app/request-guard` exactly or use an equivalent narrow path. If a
  different path is chosen, the implementation handoff must explain why.
- Whether a future read-route guard will be needed for sensitive diagnostics.
  That is intentionally deferred.

## Suspected Gaps

- Current CORS allow-headers do not include the custom guard header.
- Current frontend POST helpers are split across route-specific functions,
  which increases the risk of a future helper missing the guard.
- Current backend route tests verify CORS and route inventory but not
  per-session mutation authorization.
- Current error-report tests likely need a redaction assertion for the guard
  token once the token exists.

## Protected-Surface Assessment

Risk tier: High security workflow risk; medium local-app runtime risk.

Expected touched surfaces for Codex C:

- local app backend request/route wiring;
- frontend API helper wiring;
- local app backend and frontend tests.

Protected surfaces that must not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity;
- deduplication;
- analytics schema and migrations;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- raw logs and private/local artifacts.

## Next Recommended Role

Codex C: Module Implementer.

Codex C should reconcile the implementation branch before editing. The current
Codex B worktree is `codex/security-next-prevention-330`, while the issue
refinement recommended `codex/local-request-guard-mutating-routes-458` for
implementation. Use the branch authorized by the user/current handoff and
preserve unrelated worktree changes.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/458

Parent security workflow:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Contract:
docs/contracts/security_local_request_guard_mutating_loopback_routes.md

Goal:
Compare the current local app backend/frontend route behavior against the
contract, then implement the local request guard for mutating loopback backend
routes.

Before editing:
- Confirm branch and git status.
- Preserve unrelated local changes.
- Read AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md,
  docs/codex_module_workflow.md, docs/agent_threads/implementation.md, and
  docs/contracts/security_local_request_guard_mutating_loopback_routes.md.
- Inspect src/mythic_edge_parser/local_app/backend.py, frontend/src/api.ts,
  frontend/src/api.test.ts, tests/test_analytics_local_app_backend.py,
  tests/test_match_journal_cockpit_ui_backend.py,
  tests/test_analytics_manual_jsonl_import.py,
  tests/test_analytics_browser_jsonl_upload.py, and
  tests/test_live_app_explicit_start_capture_control.py.

Implement only:
- a process-local request guard token generated by the backend;
- a narrow frontend delivery mechanism, preferably GET /api/app/request-guard;
- backend guard enforcement on all current registered POST routes;
- CORS allow-header support for X-Mythic-Edge-Local-Request-Guard;
- frontend API header wiring through a shared guarded request path;
- focused backend/frontend tests;
- docs/implementation_handoffs/security_local_request_guard_mutating_loopback_routes_comparison.md.

Do not:
- implement #459 upload byte-limit hardening;
- introduce cloud auth, user accounts, OAuth, durable credentials, or
  persistent guard storage;
- log, report, display, commit, or persist the guard token;
- change parser behavior, analytics schema, Match Journal truth ownership,
  workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior, or
  production behavior;
- mutate CodeQL alerts;
- change CI;
- target main without explicit approval.

Validation:
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_live_app_explicit_start_capture_control.py
py -m ruff check src\mythic_edge_parser\local_app tests
npm --prefix frontend run test -- --run frontend/src/api.test.ts frontend/src/App.test.tsx
git diff --check

Also run path-scoped protected-surface and secret/private-marker scans over the
changed files.

Final output must include:
- role performed
- issue and parent issue
- branch and git status
- implementation handoff artifact
- guarded route inventory
- token lifecycle implemented
- backend/frontend files changed
- validation run and result
- protected-surface status
- secret/private-marker status
- remaining risks
- next recommended role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/458"
  parent_security_workflow: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  related_follow_up: "https://github.com/Tahjali11/Mythic-Edge/issues/459"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #458 and parent security workflow #330"
  contract_artifact: "docs/contracts/security_local_request_guard_mutating_loopback_routes.md"
  target_artifact: "docs/implementation_handoffs/security_local_request_guard_mutating_loopback_routes_comparison.md"
  risk_tier: "High security workflow risk; medium local-app runtime risk"
  branch_observed_by_codex_b: "codex/security-next-prevention-330"
  recommended_implementation_branch_from_issue: "codex/local-request-guard-mutating-routes-458"
  decision: "Guard all current registered local app POST routes with a process-local per-session header guard; keep read-only GET routes unguarded in this first slice; keep #459 upload byte-limit hardening separate."
  validation:
    - "git diff --check -- docs\\contracts\\security_local_request_guard_mutating_loopback_routes.md -> passed, but file is untracked"
    - "new-file no-index whitespace check against an empty file -> passed"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan over contract artifact"
    - "path-scoped secret/private-marker scan over contract artifact"
  stop_conditions:
    - "Do not implement #459 upload byte-limit hardening in this slice."
    - "Do not introduce cloud auth, user accounts, OAuth, durable credentials, persistent request tokens, or environment contract drift."
    - "Do not log, report, display, persist, commit, or expose the guard token."
    - "Do not change parser behavior, analytics schema, Match Journal truth ownership, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior, production behavior, or CI."
```
