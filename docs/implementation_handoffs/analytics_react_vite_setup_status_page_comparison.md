# Analytics React Vite Setup-Status Page Comparison

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/209>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/204>

## Umbrella Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/207>

## Completed Backend Child

<https://github.com/Tahjali11/Mythic-Edge/issues/208>

## Contract

`docs/contracts/analytics_react_vite_setup_status_page.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Risk Tier

High.

## Branch And Git Status

Branch confirmed: `codex/analytics-foundation`.

Initial status after npm was installed:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
?? docs/contracts/analytics_react_vite_setup_status_page.md
?? docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md
```

Remote relation:

```text
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0
```

Issue state checked with GitHub CLI:

- #209: OPEN
- #204: OPEN
- #207: OPEN
- #208: CLOSED

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_react_vite_setup_status_page.md`
- `docs/contracts/analytics_app_backend_setup_status.md`
- `docs/contract_test_reports/analytics_app_backend_setup_status.md`
- `docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`
- `pyproject.toml`
- `.gitignore`

## Current Behavior Compared To Contract

Contract matches before implementation:

- The backend setup-status child exists and #208 is closed.
- The local app backend exposes `GET /api/app/setup-status`.
- Backend route tests cover read-only setup-status behavior and safe backend
  display values.
- FastAPI remains an optional app dependency in `pyproject.toml`.
- No root `package.json` or root `package-lock.json` exists.

Contract gaps closed:

- Added the first frontend package under `frontend/`.
- Added npm package metadata and committed lockfile.
- Added React + TypeScript + Vite config and entrypoint.
- Added typed frontend API boundary for `GET /api/app/setup-status`.
- Added setup/status UI with safe rendering and non-interactive deferred
  sections.
- Added focused frontend tests for happy/degraded, backend unavailable,
  malformed response, incompatible schema, unsafe display redaction, and no
  action controls.
- Added `.gitignore` rules for generated frontend artifacts.
- Updated this implementation handoff with validation, remaining risks, and
  next-role routing.

## Implementation Option Chosen

Implemented the smallest frontend-only setup-status page authorized by the
contract.

The implementation keeps the frontend as a local display surface. It does not
read local files, inspect app-data folders, open SQLite, infer parser state,
change backend routes, or introduce controls that mutate anything.

## Files Changed

- `.gitignore`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/index.html`
- `frontend/vite.config.ts`
- `frontend/tsconfig.json`
- `frontend/tsconfig.node.json`
- `frontend/src/main.tsx`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- `frontend/src/App.css`
- `frontend/src/vite-env.d.ts`
- `frontend/src/test/setup.ts`
- `frontend/src/api.test.ts`
- `frontend/src/status.test.ts`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md`

Existing untracked source contract left in place:

- `docs/contracts/analytics_react_vite_setup_status_page.md`

## Exact Sections Changed

`.gitignore`:

- Added ignore rules for `frontend/node_modules/`, `frontend/dist/`,
  `frontend/.vite/`, and `frontend/coverage/`.

`frontend/package.json`:

- Added the required npm scripts.
- Added `engines.node` with `>=20`.
- Added only authorized runtime dependencies: `react`, `react-dom`.
- Added only authorized development dependencies: Vite, TypeScript, React
  plugin, Vitest, Testing Library, jest-dom, jsdom, and React type packages.

`frontend/src/api.ts`:

- Added `getApiBaseUrl(...)` with same-origin default and loopback-only local
  override validation.
- Added `fetchSetupStatus(...)` for the aggregate setup-status endpoint.
- Added safe error classes and response-shape validation for malformed and
  incompatible payloads.

`frontend/src/types.ts`:

- Added typed constants and response shapes for the setup-status schema.

`frontend/src/status.ts`:

- Added status-tone mapping.
- Added safe display-value guard and redaction helper.

`frontend/src/App.tsx` and `frontend/src/App.css`:

- Added the read-only setup/status first screen.
- Added loading, backend unavailable, malformed, incompatible, ready/degraded,
  unsafe-display-redacted, and deferred display states.
- Added fixed status panels with responsive CSS and text status labels.

Frontend tests:

- Added API helper tests.
- Added status/privacy helper tests.
- Added React rendering tests for core UI states and no action controls.

## Code Changed

Runtime code changed: frontend-only.

Python/backend code changed: no.

Parser behavior changed: no.

Backend route payload shape changed: no.

Tests changed: yes, frontend tests were added.

Docs changed: yes, this handoff.

Dependency metadata changed: yes, frontend package metadata and lockfile.

## Interface Changes

New frontend package interface:

- `npm --prefix frontend ci`
- `npm --prefix frontend run typecheck`
- `npm --prefix frontend run test -- --run`
- `npm --prefix frontend run build`
- `npm --prefix frontend run dev`
- `npm --prefix frontend run preview`

New frontend module surfaces:

- `getApiBaseUrl(...)`
- `fetchSetupStatus(...)`
- `statusTone(...)`
- `isSafeDisplayValue(...)`
- `safeDisplayValue(...)`
- `SetupStatusApp`

No backend route, parser output field, workbook column, webhook field, Apps
Script entrypoint, environment-variable contract, or production interface
changed.

## Node And Npm Versions

Installed/exposed npm with user-scope Node.js LTS from winget.

Validation toolchain:

```text
node --version -> v24.16.0
npm --version -> 11.13.0
```

## Dependency And Lockfile Decision

`frontend/package-lock.json` was generated with npm.

Selected package versions recorded in `frontend/package.json`:

- `react`: `^19.2.6`
- `react-dom`: `^19.2.6`
- `@vitejs/plugin-react`: `^6.0.2`
- `vite`: `^8.0.14`
- `typescript`: `^6.0.3`
- `@types/react`: `^19.2.15`
- `@types/react-dom`: `^19.2.3`
- `vitest`: `^4.1.7`
- `@testing-library/react`: `^16.3.2`
- `@testing-library/jest-dom`: `^6.9.1`
- `jsdom`: `^29.1.1`

No alternate package manager, root package file, workspace, generated client,
CSS framework, router, state manager, icon library, chart library, or lint
stack was added.

## API Consumption Behavior

The frontend fetches only the aggregate endpoint:

```text
/api/app/setup-status
```

Default API base URL is same origin.

Optional local override is accepted only when empty or loopback HTTP with a
valid port, such as `http://127.0.0.1:8000` or `http://localhost:8000`.

Non-loopback, wildcard, non-HTTP, path-bearing, query-bearing, or hash-bearing
base URLs are rejected and shown as safe configuration errors.

## UI States Implemented

- Loading.
- Backend reachable with ok/degraded/missing/unavailable/error status panels.
- Backend unavailable or network failure.
- Malformed response.
- Incompatible schema with expected schema version.
- Unsafe display value redacted with `<redacted_path>`.
- Deferred manual import, analytics views, and live watcher sections.

The UI exposes no buttons, inputs, file pickers, import controls, start/stop
controls, reset/delete/wipe controls, Sheets controls, AI controls, or
production controls.

## Validation Run

```text
git status --short --branch -> ## codex/analytics-foundation...origin/codex/analytics-foundation plus untracked contract/handoff and frontend changes
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0
GitHub CLI issue checks -> #209/#204/#207 open, #208 closed
node --version -> v24.16.0
npm --version -> 11.13.0
npm --prefix frontend ci -> passed, 113 packages, 0 vulnerabilities
npm --prefix frontend run typecheck -> passed
npm --prefix frontend run test -- --run -> passed, 3 files, 11 tests
npm --prefix frontend run build -> passed
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py -> 18 passed, 1 third-party warning
git diff --check -> passed
path-scoped protected-surface check -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0
```

Browser smoke:

```text
Vite dev server on http://127.0.0.1:5173/ -> served page
Playwright CLI snapshot -> page rendered Backend unavailable
Playwright CLI eval document body -> Backend unavailable / Backend setup status is unavailable / unavailable
Network requests -> /api/app/setup-status returned 404 from Vite without backend, as expected for no backend server
Vite dev server -> stopped after smoke test
```

One validation note:

- An initial parallel validation attempt failed because `npm ci`, typecheck,
  and tests were started at the same time while `node_modules` was being
  rebuilt. Sequential rerun passed and is the validation result recorded above.

## Protected-Surface Status

No parser, parser state, backend route, workbook, webhook, Apps Script, Sheets,
AI, production, or generated local data behavior changed.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan over touched files passed with
`forbidden 0, warnings 0`.

Frontend tests use synthetic unsafe path-like values and do not include raw
private machine paths, raw Player.log contents, raw JSONL payloads, secrets,
webhook URLs, API keys, or tokens.

## Generated Artifact Status

`frontend/package-lock.json` is the committed dependency lockfile.

Generated local artifacts:

- `frontend/node_modules/` exists locally and is ignored.
- `frontend/dist/` was produced by build validation and removed afterward.
- `frontend/.vite/` is absent.
- `frontend/coverage/` is absent.

No generated SQLite database, WAL, SHM, journal, raw log, local JSONL artifact,
runtime output, retry payload, workbook export, or generated card/tier data was
created or changed.

## Forbidden Scope

Forbidden scope touched: no.

Backend behavior unchanged: yes.

No destructive UI actions exposed: yes.

No parser/runtime/workbook/webhook/App Script/Sheets/AI/production behavior
changed: yes.

## Still Unverified

- Live backend integration with a running FastAPI server.
- Future packaged/static serving mode.
- Future launcher or bootstrapper behavior.
- Future frontend lint policy.
- Production behavior, which is out of scope.

## Reviewer Focus

Codex E should review:

- Whether the dependency versions and npm lockfile are acceptable for this first
  frontend slice.
- Whether `getApiBaseUrl(...)` is strict enough for the contract's loopback-only
  override.
- Whether safe display redaction covers the right level of privacy risk without
  turning frontend into truth owner.
- Whether the UI truly has no action controls.
- Whether the page uses only the aggregate setup-status endpoint.
- Whether the generated artifact cleanup and ignore rules are sufficient.

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #209.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/209

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Completed backend child:
https://github.com/Tahjali11/Mythic-Edge/issues/208

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_react_vite_setup_status_page.md

Implementation handoff:
docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md

Risk tier:
High

Review goal:
Review Codex C's React + TypeScript + Vite setup-status page against the contract. Lead with findings. Confirm the frontend is read-only, uses only the aggregate setup-status endpoint, handles required UI states safely, commits package-lock, and does not change backend/parser/workbook/webhook/App Script/Sheets/AI/production behavior.

Before reviewing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and identify unrelated dirty or untracked files.
- Confirm issue #209, tracker #204, and umbrella issue #207 are open and issue #208 is closed if GitHub CLI is available.
- Read the contract and implementation handoff.
- Inspect .gitignore, frontend/package.json, frontend/package-lock.json, frontend config files, frontend/src/, frontend tests, and the handoff.
- Do not assume the implementation is correct.

Review checks:
- Confirm no root package.json/workspace/alternate package manager was added.
- Confirm package.json has the required scripts and engines.node >=20.
- Confirm dependencies are limited to the contract-authorized set.
- Confirm frontend/package-lock.json exists and generated artifacts are ignored.
- Confirm the API client fetches only GET /api/app/setup-status for main data.
- Confirm non-loopback API base URL overrides are rejected safely.
- Confirm malformed, incompatible, unavailable, degraded/missing, and unsafe-display states are handled without dumping raw JSON, stack traces, private paths, raw logs, secrets, webhook URLs, or local artifacts.
- Confirm manual import, analytics views, and live watcher sections are display-only and expose no action controls.
- Confirm backend behavior and backend route payload shape were not changed.
- Confirm parser/runtime/workbook/webhook/App Script/Sheets/AI/production behavior was not changed.

Validation:
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
git diff --check

Also run path-scoped protected-surface and secret/private-marker checks over:
- .gitignore
- docs/contracts/analytics_react_vite_setup_status_page.md
- docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md
- frontend/package.json
- frontend/package-lock.json
- frontend/index.html
- frontend/vite.config.ts
- frontend/tsconfig.json
- frontend/tsconfig.node.json
- frontend/src/main.tsx
- frontend/src/App.tsx
- frontend/src/api.ts
- frontend/src/types.ts
- frontend/src/status.ts
- frontend/src/App.css
- frontend/src/vite-env.d.ts
- frontend/src/test/setup.ts
- frontend/src/api.test.ts
- frontend/src/status.test.ts
- frontend/src/App.test.tsx

If feasible, run a browser smoke test of the Vite page. If no backend server is running, verify the page renders the safe backend-unavailable state without changing backend code.

Do not:
- edit code in review mode
- target main
- change backend behavior, parser behavior, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, AI behavior, production behavior, secrets, raw logs, generated data, local JSONL artifacts, or generated database artifacts
- expose destructive UI actions
- stage, commit, push, open a PR, merge, or close issues

Final report must include:
- role performed
- issue/tracker/umbrella issue/completed backend child
- contract and handoff reviewed
- findings first, ordered by severity with file/line references
- validation run and result
- dependency and lockfile assessment
- API consumption assessment
- UI state and no-control assessment
- protected-surface status
- secret/private-marker status
- generated artifact status
- whether forbidden scope was touched
- verdict
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/209"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_backend_child: "https://github.com/Tahjali11/Mythic-Edge/issues/208"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/analytics_react_vite_setup_status_page.md"
  target_artifact: "docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "node --version -> v24.16.0"
    - "npm --version -> 11.13.0"
    - "npm --prefix frontend ci -> passed, 113 packages, 0 vulnerabilities"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> passed, 3 files, 11 tests"
    - "npm --prefix frontend run build -> passed"
    - "py -m pytest -q tests\\test_analytics_local_app_config.py tests\\test_analytics_local_app_backend.py -> 18 passed, 1 third-party warning"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "browser smoke -> Vite page rendered safe backend-unavailable state without backend"
  stop_conditions:
    - "Do not target main."
    - "Do not change backend behavior unless a later contract authorizes it."
    - "Do not expose destructive UI actions."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/AI/production behavior."
    - "Do not create or commit generated/private/local artifacts or secrets."
    - "Do not stage, commit, push, open a PR, merge, or close issues unless explicitly asked."
```
