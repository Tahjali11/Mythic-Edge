# Security Local Request Guard Mutating Loopback Routes Comparison

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/458>

## Parent Security Workflow

<https://github.com/Tahjali11/Mythic-Edge/issues/330>

## Contract

`docs/contracts/security_local_request_guard_mutating_loopback_routes.md`

## Internal Project Area

Local app security boundary.

## Truth Owner

The backend process-local request guard owns only whether a mutating local app
request carries the current process-local guard value. Existing route handlers
still own their current domain behavior after the guard passes.

## Bridge-Code Status

`shared_support`

The guard supports multiple local app write surfaces, but it does not bridge
parser facts into downstream systems.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

- Initial contract worktree: `codex/security-next-prevention-330`
- Implementation branch created and used:
  `codex/local-request-guard-mutating-routes-458`
- Base observed before implementation: even with `origin/main`, `0 0`

Initial status before implementation:

```text
## codex/security-next-prevention-330...origin/main
?? docs/contracts/security_local_request_guard_mutating_loopback_routes.md
```

Final status before final validation:

```text
## codex/local-request-guard-mutating-routes-458
 M frontend/src/api.test.ts
 M frontend/src/api.ts
 M src/mythic_edge_parser/local_app/backend.py
 M tests/test_analytics_browser_jsonl_upload.py
 M tests/test_analytics_local_app_backend.py
 M tests/test_analytics_manual_jsonl_import.py
 M tests/test_live_app_explicit_start_capture_control.py
 M tests/test_match_journal_cockpit_ui_backend.py
?? docs/contracts/security_local_request_guard_mutating_loopback_routes.md
?? docs/implementation_handoffs/security_local_request_guard_mutating_loopback_routes_comparison.md
?? tests/local_app_request_guard_helpers.py
```

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/security_local_request_guard_mutating_loopback_routes.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_match_journal_cockpit_ui_backend.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `tests/test_analytics_browser_jsonl_upload.py`
- `tests/test_live_app_explicit_start_capture_control.py`

## Current Behavior Compared To Contract

Before this change, the local app backend had loopback CORS posture but no
process-local request guard on mutating routes. Current frontend helpers called
POST routes directly with route-local headers.

The current registered POST routes matched the contract inventory and were
unguarded before implementation.

## Implementation Option Chosen

Implemented the smallest contract-aligned local request guard:

- generate one opaque process-local token at backend app creation;
- store it only in FastAPI process state;
- expose a narrow read-only bootstrap endpoint at
  `GET /api/app/request-guard`;
- enforce the guard through one shared FastAPI dependency on every current
  registered POST route;
- keep CORS loopback-only while allowing
  `X-Mythic-Edge-Local-Request-Guard`;
- route all frontend mutating helpers through one guarded fetch helper that
  lazily fetches and caches the token in module memory only;
- leave read-only GET helpers unguarded.

## Guarded Route Inventory

Guarded with `require_local_request_guard`:

- `POST /api/live/capture/start`
- `POST /api/live/capture/stop`
- `POST /api/feedback/error-report/preview`
- `POST /api/feedback/error-report/submit`
- `POST /api/journal/notes`
- `POST /api/journal/opponent-labels`
- `POST /api/journal/review-flags`
- `POST /api/journal/experiment-label`
- `POST /api/journal/display-corrections`
- `POST /api/imports/jsonl`
- `POST /api/imports/jsonl/upload`

Read-only GET routes remain unguarded in this slice, including
`GET /api/app/request-guard`, which is limited to local loopback host/origin
posture and returns only guard metadata.

## Token Lifecycle Implemented

- Generated with `secrets.token_urlsafe(32)` when `create_app()` constructs
  the backend app.
- Stored only in `app.state.local_request_guard_token`.
- Regenerated on backend process/app restart.
- Delivered only through `GET /api/app/request-guard`.
- Sent by the frontend only in the
  `X-Mythic-Edge-Local-Request-Guard` request header for guarded POST helpers.
- Not written to disk, config, environment variables, reports, SQLite,
  browser storage, query strings, or request bodies.
- Compared with `hmac.compare_digest`.
- Public-safe failures:
  - missing/blank header: `401`, `local_request_guard_missing`
  - invalid token: `403`, `local_request_guard_invalid`
  - disallowed origin: `403`, `local_request_origin_not_allowed`
  - disallowed host: `403`, `local_request_host_not_allowed`
  - unavailable guard state: `503`, `local_request_guard_unavailable`

## Files Changed

- `src/mythic_edge_parser/local_app/backend.py`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `tests/local_app_request_guard_helpers.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_match_journal_cockpit_ui_backend.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `tests/test_analytics_browser_jsonl_upload.py`
- `tests/test_live_app_explicit_start_capture_control.py`
- `docs/implementation_handoffs/security_local_request_guard_mutating_loopback_routes_comparison.md`

Preserved untracked contract artifact:

- `docs/contracts/security_local_request_guard_mutating_loopback_routes.md`

## Exact Sections Changed

### Backend

`src/mythic_edge_parser/local_app/backend.py`

- Added guard constants and `GUARDED_MUTATING_API_ROUTES`.
- Added process-local token initialization in `create_app`.
- Added `GET /api/app/request-guard`.
- Added `require_local_request_guard`.
- Added origin, host, token retrieval, error-envelope, and loopback-host helper
  functions.
- Added guard dependencies to every current registered POST route.
- Added CORS allow-header support for
  `X-Mythic-Edge-Local-Request-Guard`.

### Frontend

`frontend/src/api.ts`

- Added request-guard constants, in-memory guard cache, and test reset helper.
- Added `guardedFetch`, `fetchLocalRequestGuard`, and guard response
  validation.
- Converted all current mutating helper calls to use `guardedFetch`.
- Kept GET helpers without the guard header.
- Kept multipart upload without manual `Content-Type`.

### Tests

`tests/test_analytics_local_app_backend.py`

- Added bootstrap endpoint shape/redaction assertions.
- Added route inventory and dependency assertions for all current POST routes.
- Added missing, blank, and invalid guard failure checks.
- Added disallowed origin/host checks.
- Extended CORS preflight check to include the custom guard header.

`tests/local_app_request_guard_helpers.py`

- Added a guarded local TestClient wrapper for existing route behavior tests.

Other focused backend test files:

- Updated existing local app POST behavior tests to use the guarded client so
  route-specific assertions now exercise the valid-token path.

`frontend/src/api.test.ts`

- Added synthetic guard bootstrap payload helper.
- Added cache reset between tests.
- Updated mutating helper tests to expect guard bootstrap plus guarded POST.
- Added guard-unavailable behavior that blocks POST.

## Code Changed

Yes. Local app backend request wiring and frontend API helper wiring changed.
No parser, analytics schema, Match Journal truth ownership, workbook/webhook,
Apps Script, Google Sheets, OpenAI/AI/coaching, CodeQL alert lifecycle, CI, or
production behavior changed.

## Tests Added Or Updated

Yes. Focused backend and frontend tests were updated to cover guard behavior
and preserve existing route behavior behind a valid guard.

## Interface Changes

Added one local backend read-only bootstrap endpoint:

```text
GET /api/app/request-guard
```

Added one required request header for current mutating local app POST routes:

```text
X-Mythic-Edge-Local-Request-Guard
```

No durable credential, environment-variable contract, API schema for existing
routes, parser output, workbook schema, webhook payload, CI gate, or production
interface changed.

## Contracted Area Status

Implementation stayed inside the local app security boundary, frontend API
wiring, and focused tests. Issue #459 upload byte-limit hardening was not
implemented.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
git fetch --prune
gh issue view 458 --json number,state,title,url,body --comments
gh issue view 330 --json number,state,title,url,body
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_live_app_explicit_start_capture_control.py
py -m ruff check src\mythic_edge_parser\local_app tests
npm --prefix frontend ci
npm --prefix frontend run test -- --run frontend/src/api.test.ts frontend/src/App.test.tsx
npm --prefix frontend run test -- --run src/api.test.ts src/App.test.tsx
npm --prefix frontend run typecheck
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over changed files
path-scoped secret/private-marker scan over changed files
```

Results:

- Issue #458: open.
- Parent issue #330: open.
- `tests\test_analytics_local_app_backend.py`: passed, `32 passed`.
- `tests\test_match_journal_cockpit_ui_backend.py`: passed, `15 passed`.
- `tests\test_analytics_manual_jsonl_import.py`: passed, `14 passed`.
- `tests\test_analytics_browser_jsonl_upload.py`: passed, `11 passed`.
- `tests\test_live_app_explicit_start_capture_control.py`: passed,
  `12 passed`.
- Ruff local-app/tests scope: passed.
- `npm --prefix frontend ci`: passed; created local ignored
  `frontend/node_modules`; npm reported two high-severity audit findings, but
  dependency changes and `npm audit fix` are out of scope.
- Prompted frontend command with `frontend/src/...` filters: failed because
  `npm --prefix frontend` runs Vitest from the `frontend` directory and no
  matching files were found.
- Equivalent frontend command with `src/...` filters: passed,
  `2 passed`, `96 passed`.
- Frontend typecheck: passed.
- `git diff --check`: passed after final handoff update.
- `py tools\check_agent_docs.py`: passed.
- Path-scoped protected-surface scan over changed files: passed,
  `forbidden 0`, `warnings 0`.
- Path-scoped secret/private-marker scan over changed files: passed,
  `forbidden 0`, `warnings 0`.

## Protected-Surface Status

Path-scoped protected-surface scan passed with `forbidden 0`, `warnings 0`.
Intended protected surfaces were not touched.

## Secret And Private-Marker Status

Path-scoped secret/private-marker scan passed with `forbidden 0`, `warnings 0`.
The guard value is generated only at runtime and no live token, private path,
raw payload, secret, credential, generated SQLite content, raw log, workbook
export, or local-only artifact was committed.

## Generated Artifact Status

`npm --prefix frontend ci` created local ignored `frontend/node_modules` for
validation. It is not part of `git status` and must not be staged or committed.

## Remaining Risks

- GitHub CodeQL alert lifecycle was not mutated or rerun.
- Browser runtime behavior was validated through frontend unit tests, not a
  live browser smoke.
- npm audit reported two high-severity dependency findings during local
  install; this implementation did not change dependencies or run remediation.
- Codex E should independently verify that every mutating route remains
  guarded and that no token is persisted or echoed in reports.

## Reviewer Focus

Codex E should verify:

- every current registered POST route has the guard dependency;
- no route-specific behavior executes before missing/blank/invalid guard
  rejection;
- read-only GET routes remain unguarded except for bootstrap host/origin
  safety;
- `GET /api/app/request-guard` returns only public-safe metadata plus the token
  needed by the local frontend;
- frontend mutating helpers include the guard header;
- frontend GET helpers do not include the guard header by default;
- multipart upload does not set manual `Content-Type`;
- `LOG`, reports, UI, request bodies, query strings, storage, and diagnostics
  do not persist or echo the token;
- #459 byte-limit/upload hardening was not absorbed.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #458.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/458

Parent security workflow:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Branch:
codex/local-request-guard-mutating-routes-458

Contract:
docs/contracts/security_local_request_guard_mutating_loopback_routes.md

Implementation handoff:
docs/implementation_handoffs/security_local_request_guard_mutating_loopback_routes_comparison.md

Review goal:
Verify the local request guard implementation against the contract. Lead with findings.

Check:
- every current registered local app POST route is guarded;
- missing, blank, invalid, disallowed Origin, and disallowed Host failures use the contracted status/code vocabulary;
- route-specific behavior does not run when the guard fails;
- CORS remains loopback-only and allows X-Mythic-Edge-Local-Request-Guard;
- GET /api/app/request-guard is narrow, local, public-safe, and does not expose private artifacts;
- frontend mutating helpers fetch the guard once in memory and include the header;
- frontend GET helpers do not include the guard header by default;
- multipart upload includes the guard header without manual Content-Type;
- the token is not persisted, logged, displayed, included in reports, stored in browser storage, placed in URLs, or committed;
- issue #459 upload byte-limit hardening was not implemented;
- no parser, analytics schema, Match Journal truth ownership, workbook/webhook/App Script/Sheets, OpenAI/AI/coaching, production behavior, CodeQL alert lifecycle, or CI behavior changed.

Validation:
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_live_app_explicit_start_capture_control.py
py -m ruff check src\mythic_edge_parser\local_app tests
npm --prefix frontend run test -- --run src/api.test.ts src/App.test.tsx
npm --prefix frontend run typecheck
git diff --check

Run path-scoped protected-surface and secret/private-marker scans over changed files.

Do not stage, commit, push, open a PR, mutate CodeQL alerts, close #458, close #330, implement #459, or change CI unless explicitly asked.

Produce docs/contract_test_reports/security_local_request_guard_mutating_loopback_routes.md and a workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/458"
  parent_security_workflow: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  related_follow_up: "https://github.com/Tahjali11/Mythic-Edge/issues/459"
  completed_thread: "C"
  next_thread: "E"
  contract_artifact: "docs/contracts/security_local_request_guard_mutating_loopback_routes.md"
  target_artifact: "docs/implementation_handoffs/security_local_request_guard_mutating_loopback_routes_comparison.md"
  branch: "codex/local-request-guard-mutating-routes-458"
  risk_tier: "High security workflow risk; medium local-app runtime risk"
  guarded_routes:
    - "POST /api/live/capture/start"
    - "POST /api/live/capture/stop"
    - "POST /api/feedback/error-report/preview"
    - "POST /api/feedback/error-report/submit"
    - "POST /api/journal/notes"
    - "POST /api/journal/opponent-labels"
    - "POST /api/journal/review-flags"
    - "POST /api/journal/experiment-label"
    - "POST /api/journal/display-corrections"
    - "POST /api/imports/jsonl"
    - "POST /api/imports/jsonl/upload"
  validation:
    - "focused backend pytest commands -> passed"
    - "py -m ruff check src\\mythic_edge_parser\\local_app tests -> passed"
    - "npm --prefix frontend run test -- --run frontend/src/api.test.ts frontend/src/App.test.tsx -> failed path filter under --prefix"
    - "npm --prefix frontend run test -- --run src/api.test.ts src/App.test.tsx -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  forbidden_scope_touched: false
  generated_artifacts_kept: "frontend/node_modules created locally by npm ci for validation; ignored and not staged"
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
