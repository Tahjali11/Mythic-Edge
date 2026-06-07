# Analytics React Vite Setup-Status Page Contract

## Module

Local app frontend setup-status page.

This contract defines the first frontend implementation slice under the local
developer app shell umbrella: a React + TypeScript + Vite page that displays
the local setup/status data exposed by the completed backend setup-status
skeleton.

Plain English: build the first read-only local app screen. It should show the
dashboard lights from the backend, not add controls that start changing files,
databases, parser runtime, Sheets, AI, or production state.

## Source Issue

- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/209>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Completed backend child: <https://github.com/Tahjali11/Mythic-Edge/issues/208>
- Umbrella contract: `docs/contracts/analytics_local_developer_app_shell.md`
- Backend contract: `docs/contracts/analytics_app_backend_setup_status.md`
- Backend review report:
  `docs/contract_test_reports/analytics_app_backend_setup_status.md`

## Branch

Current intended branch:

```text
codex/analytics-foundation
```

Observed during this Codex B pass:

```text
45207a41447e5239a2d56203d5ce81057e20d062
```

Local branch state observed:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
```

This contract does not stage, commit, push, open a PR, close issues, or target
`main`.

## Authority And Source Artifacts Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- tracker #204
- umbrella issue #207
- completed backend child #208
- source issue #209
- `docs/project_roadmap.md`
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_app_backend_setup_status.md`
- `docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md`
- `docs/contract_test_reports/analytics_app_backend_setup_status.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`
- `pyproject.toml`
- `.gitignore`

## Risk Tier

High.

Reasons:

- introduces the first local web UI surface
- introduces Node.js, npm, frontend dependencies, and a lockfile
- can accidentally display private paths, raw local data, secrets, or unsafe
  backend response values
- can accidentally add action controls before backend contracts authorize them
- can blur setup display state with parser truth, analytics truth, deploy
  readiness, or production authority
- can create generated frontend artifacts if ignore rules and validation are
  loose

## Owning Layer

Primary owner: local analytics usability / frontend display surface.

Truth boundaries:

- Parser/state owns MTGA event interpretation, match/game identity, final
  reconciliation, parser event classes, and parser-managed facts.
- The Player.log evidence ledger owns provenance, confidence, finality, drift,
  degradation, invariant, and review vocabulary.
- Analytics ingest and SQLite own downstream local storage and deterministic
  query surfaces, not parser truth.
- The backend setup/status package owns setup/status response semantics.
- The frontend owns presentation, navigation, loading/error states, and safe
  rendering only.

The frontend must not become parser truth, analytics truth, evidence truth,
workbook truth, AI truth, gameplay advice, hidden-card inference, archetype
classification, player-mistake truth, merge readiness, deploy readiness, or
production authority.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_react_vite_setup_status_page.md`

Future Codex C implementation files authorized by this contract:

- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/index.html`
- `frontend/vite.config.ts`
- `frontend/tsconfig.json`
- `frontend/tsconfig.node.json` or equivalent Vite TypeScript config split
- `frontend/src/main.tsx`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- `frontend/src/App.css` or `frontend/src/styles.css`
- focused frontend tests under `frontend/src/`
- `docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md`

Conditional implementation file:

- `.gitignore`, only to ignore frontend generated artifacts such as
  `frontend/node_modules/`, `frontend/dist/`, `frontend/.vite/`, and
  `frontend/coverage/`.

Referenced but not owned:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`
- `pyproject.toml`

Codex C must route back to Codex B before editing referenced-but-not-owned
backend or Python source modules.

## Observed Current Behavior

Repo state:

- Backend setup/status issue #208 is closed.
- Tracker #204 remains open.
- Umbrella issue #207 remains open.
- Source issue #209 is open.
- Backend setup/status code exists under `src/mythic_edge_parser/local_app/`.
- Backend setup/status tests exist and were previously validated.
- `pyproject.toml` already contains optional `app` dependencies for FastAPI and
  dev test support for FastAPI/httpx.
- There is no `frontend/` directory.
- There is no root `package.json`.
- There is no frontend `package.json`, `package-lock.json`, Vite config, React
  entrypoint, TypeScript config, CSS, or frontend test setup.
- `.gitignore` does not yet include frontend generated artifact rules.

Backend surface currently available for display:

- `GET /api/health`
- `GET /api/app/setup-status`
- `GET /api/app/config`
- `GET /api/app/paths`
- `GET /api/analytics/database/status`
- `GET /api/runtime/status`

The frontend should use `GET /api/app/setup-status` as the primary source for
the setup-status page. That aggregate endpoint already includes:

- path status
- config status
- Player.log status
- analytics database status
- migration availability/status
- runtime/deferred status
- capabilities

Observed gap:

- No browser-visible setup/status page exists.
- No frontend dependency, lockfile, Node version, npm script, test, typecheck,
  or build policy exists in committed frontend files.
- No frontend API client exists for the setup/status endpoint.
- No frontend guard exists for backend-unavailable, malformed-response, or
  unsafe-display-value states.

## Contract Decisions

### Frontend Folder

The first frontend package must live under:

```text
frontend/
```

Do not add a root `package.json`, npm workspace, pnpm workspace, yarn workspace,
or frontend files under `src/mythic_edge_parser/` in this slice.

Reason: the Python package remains the parser/backend package. The web app is a
local app display surface and should be reviewable as a separate frontend
package.

### Package Manager And Lockfile

npm is the required package manager for this first frontend slice.

Required guarantees:

- `frontend/package.json` defines every frontend validation script used by this
  contract.
- `frontend/package-lock.json` is committed with dependency changes.
- `frontend/node_modules/` is never committed.
- `frontend/dist/`, `frontend/.vite/`, and `frontend/coverage/` are generated
  local artifacts and must be ignored.
- Do not add pnpm, yarn, bun, npx-based primary workflow, or a second package
  manager in this slice.
- Do not install global packages as part of implementation.

### Node Version Policy

`frontend/package.json` must include an `engines.node` field.

Required first-slice policy:

```json
{
  "engines": {
    "node": ">=20"
  }
}
```

Codex C must record the local `node --version` and `npm --version` used for
validation in the implementation handoff. If the local toolchain cannot satisfy
this policy, Codex C must stop and report the blocker instead of changing the
contract or falling back to another toolchain.

Do not add `.node-version` in this slice unless Codex C finds an existing repo
or CI pattern that requires it and routes that decision through the handoff.

### Dependencies

Allowed runtime dependencies:

- `react`
- `react-dom`

Allowed development dependencies:

- `@vitejs/plugin-react`
- `vite`
- `typescript`
- `@types/react`
- `@types/react-dom`
- `vitest`
- `@testing-library/react`
- `@testing-library/jest-dom`
- `jsdom`

No design-system, router, state-management, icon, chart, animation, CSS
framework, generated client, or API-codegen dependency is authorized in this
first slice. If Codex C believes another dependency is necessary, route back to
Codex B.

### Required npm Scripts

`frontend/package.json` must define:

```json
{
  "scripts": {
    "dev": "vite",
    "typecheck": "tsc --noEmit",
    "test": "vitest",
    "build": "tsc --noEmit && vite build",
    "preview": "vite preview"
  }
}
```

This first slice does not require an ESLint/lint script because the repo has no
existing frontend lint policy. Do not add an ESLint dependency or config unless
Codex C routes that as a contract question. TypeScript typechecking, focused
tests, and the Vite production build are the required deterministic frontend
checks.

## Public Interface

Frontend package:

```text
frontend/
```

Required public npm commands:

```powershell
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
```

Recommended frontend module surfaces:

```text
frontend/src/api.ts
frontend/src/types.ts
frontend/src/status.ts
frontend/src/App.tsx
frontend/src/main.tsx
```

Recommended TypeScript exports:

```ts
type SetupStatusResponse
type SectionStatus
type CapabilityStatus
function getApiBaseUrl(): string
async function fetchSetupStatus(fetchImpl?: typeof fetch): Promise<SetupStatusResponse>
function isSafeDisplayValue(value: unknown): value is string
function statusTone(status: string): "ok" | "degraded" | "missing" | "unavailable" | "error" | "deferred" | "unknown"
```

Names may differ if Codex C records why, but the semantic surfaces must remain
small, typed, and testable.

## Backend API Consumption Contract

Primary endpoint:

```text
GET /api/app/setup-status
```

First-slice decision:

- The setup/status page must fetch only the aggregate setup-status endpoint for
  its main data.
- A successful aggregate response is sufficient to treat the backend as
  reachable for the UI.
- Do not call every individual backend endpoint from the first page unless
  Codex C routes back with a concrete contract need.

Allowed backend base URL behavior:

- Default base URL: same origin, using a relative `/api/app/setup-status`
  request.
- Optional local dev override:
  `VITE_MYTHIC_EDGE_API_BASE_URL`.
- The override must be empty, `http://127.0.0.1:<port>`, or
  `http://localhost:<port>`.
- Non-loopback or wildcard override values must be rejected in frontend code
  and shown as a safe configuration error.
- Do not commit `.env`, `.env.local`, `.env.*.local`, backend origins with real
  private hostnames, secrets, tokens, API keys, or webhook URLs.

Backend responsibility boundaries:

- The backend owns setup/status semantics.
- The frontend must not read local files, inspect `%LOCALAPPDATA%`, open SQLite,
  discover Player.log, infer migration status, or validate config by itself.
- The frontend may apply a defensive presentation guard that refuses to render
  unsafe display strings, but that guard is a privacy safeguard only; it does
  not make the frontend the owner of path redaction truth.

If CORS, backend serving, or endpoint-shape issues block manual browser
validation, Codex C must report the blocker. It must not change backend CORS,
backend routes, backend payload shape, or Python source in this slice.

## Input Shape

Input source:

- JSON response from `GET /api/app/setup-status`.

Required top-level fields:

- `object`
- `schema_version`
- `status`
- `paths`
- `config`
- `player_log`
- `analytics_database`
- `migrations`
- `runtime`
- `capabilities`

Required expected values:

- `schema_version = "analytics_app_backend_setup_status.v1"`
- `object = "mythic_edge_local_app_setup_status"`

Allowed top-level status labels:

- `ok`
- `degraded`
- `missing`
- `unavailable`
- `error`

The frontend must tolerate unknown additional fields. Unknown fields should not
be rendered unless they are explicitly added to this contract or a later
contract.

Malformed input behavior:

- missing required fields: show safe malformed-response state
- wrong `schema_version`: show safe incompatible-response state
- non-object JSON: show safe malformed-response state
- network failure: show backend-unavailable state
- fetch timeout or abort: show backend-unavailable state

The UI must not dump raw JSON or stack traces into the page.

## Output Shape

Output destination:

- local browser page served by Vite during development or future backend/static
  serving in a later contract

Required first page:

- setup/status page as the first screen
- no marketing/landing-page detour
- no route navigation requirement

Required panels:

- overall setup status
- backend reachability
- app-data folder status
- local config status
- Player.log status
- analytics database status
- migration availability/status
- runtime/deferred capability status
- disabled/deferred future sections for manual import, analytics views, and
  live watcher status

Required display principles:

- use backend-provided status labels and display labels
- present path values only through safe display strings such as `<app_data>`,
  `<configured_player_log>`, and `<detected_mtga_player_log>`
- never display raw Player.log contents
- never display raw JSONL artifact contents
- never display full private user-profile paths
- never display secrets, webhook URLs, API keys, tokens, or OAuth state
- do not show stack traces, dependency internals, or local environment dumps

Deferred placeholders may be visible, but they must be non-interactive status
surfaces. They must not contain file pickers, import buttons, start/stop
buttons, reset buttons, delete buttons, DB init buttons, Git controls, Google
Sheets controls, OpenAI/AI controls, or production/deployment controls.

## UI State Contract

Required states:

- loading
- backend ok
- backend degraded
- missing setup pieces
- unavailable app-data/backend response
- backend unavailable/network error
- malformed or incompatible response
- unsafe display value redacted

The UI should be quiet and operational, suitable for repeated local developer
use. It should prioritize clear scanning over marketing copy.

Responsive requirements:

- desktop and mobile widths must not overlap controls or text
- long status strings and display labels must wrap safely
- fixed-format status tiles or panels must have stable dimensions and avoid
  layout shift from loading/error labels
- font sizes must not scale with viewport width
- letter spacing must remain `0`

Accessibility requirements:

- status values must be readable as text, not color alone
- page landmarks, headings, and buttons/links must have accessible names
- disabled/deferred sections must be communicated as status, not as broken
  controls

## Path And Privacy Rendering Contract

Allowed path display values:

- `<app_data>`
- `<app_data>\config`
- `<app_data>\db`
- `<app_data>\db\mythic_edge.sqlite3`
- `<configured_player_log>`
- `<detected_mtga_player_log>`
- `%LOCALAPPDATA%\MythicEdgeDev`
- symbolic labels introduced by the backend setup/status contract

Forbidden default display values:

- absolute Windows user-profile paths
- absolute macOS user-profile paths
- absolute Linux home-directory paths
- raw temporary test paths
- raw `Player.log` content
- raw JSONL content
- webhook URLs
- API keys
- tokens
- OAuth state

Frontend tests must include at least one synthetic unsafe path-like value and
prove it is not rendered.

## Error Behavior

Backend unavailable:

- render a safe unavailable state
- do not show stack trace or raw exception object
- do not retry in a loop faster than a human could understand

Malformed response:

- render a safe malformed-response state
- do not render unknown payload blobs

Incompatible schema version:

- render a safe incompatible-response state
- name the expected schema version
- do not reinterpret the response as a newer truth source

Unsafe display value:

- render a redacted placeholder such as `<redacted_path>`
- mark the affected panel as degraded or warning-level
- do not hide the whole page if the rest of the payload is safe

Contract conflict:

- if the page needs a backend field that is absent from
  `analytics_app_backend_setup_status.v1`, Codex C must route back to Codex B
  or a backend contract, not edit backend behavior in the frontend slice.

## Side Effects

Allowed side effects in Codex C:

- add `frontend/` source, config, tests, and lockfile
- update `.gitignore` for frontend generated artifacts only
- create
  `docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md`

Forbidden side effects:

- no backend behavior changes
- no Python source changes
- no parser/runtime/workbook/webhook/Apps Script/Sheets/Match Journal/OpenAI/AI
  behavior changes
- no generated SQLite database, WAL, SHM, or journal files
- no local app-data folders
- no raw Player.log, JSONL, runtime status, failed post, workbook export, or
  generated card/tier data
- no `.env`, `.env.local`, secret, token, credential, webhook URL, or OAuth
  state
- no `node_modules/`, `dist/`, `.vite/`, or frontend coverage artifacts
- no Git branch, merge, pull, push, PR, issue closure, or tracker completion
  unless a later role explicitly authorizes it

## Dependency Order

Recommended Codex C order:

1. Confirm branch and worktree state.
2. Inspect `docs/contracts/analytics_react_vite_setup_status_page.md` and the
   backend setup/status contract.
3. Confirm no existing `frontend/` or package files have appeared since this
   contract.
4. Record local `node --version` and `npm --version`.
5. Add `.gitignore` frontend generated-artifact rules.
6. Add the Vite React TypeScript package under `frontend/`.
7. Add typed API client and response/status helpers.
8. Add the setup/status page and CSS.
9. Add focused frontend tests for happy, degraded, unavailable, malformed, and
   unsafe-display-value states.
10. Run frontend validation first, then adjacent backend tests.
11. Write the implementation handoff.

## Compatibility

Must remain compatible with:

- backend setup/status schema version
  `analytics_app_backend_setup_status.v1`
- existing backend endpoints and route shapes
- existing Python package metadata and optional `app` dependency group
- existing analytics roadmap and local developer app shell contract
- existing generated-artifact and secret/private-marker policies

This contract does not require packaged mode, backend static file serving,
backend CORS changes, a launcher, or a bootstrapper.

## Tests Required

Frontend validation:

```powershell
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
```

Adjacent backend validation:

```powershell
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
```

Repo checks:

```powershell
git diff --check
```

Path-scoped protected-surface check:

```powershell
@'
.gitignore
frontend/package.json
frontend/package-lock.json
frontend/index.html
frontend/vite.config.ts
frontend/tsconfig.json
frontend/tsconfig.node.json
frontend/src/main.tsx
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/status.ts
frontend/src/App.css
docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Path-scoped secret/private-marker scan:

```powershell
@'
.gitignore
frontend/package.json
frontend/package-lock.json
frontend/index.html
frontend/vite.config.ts
frontend/tsconfig.json
frontend/tsconfig.node.json
frontend/src/main.tsx
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/status.ts
frontend/src/App.css
docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Manual/browser smoke expectation:

- Codex C should start the Vite dev server after implementation if the local
  Node/npm install succeeds.
- If the backend is not running, the page must still render the safe
  backend-unavailable state.
- If a backend server is available, Codex C may test against it, but must not
  change backend code to make the smoke test pass.

Required test assertions:

- setup-status happy/degraded payload renders expected safe status labels
- backend-unavailable state renders without stack traces
- malformed response renders a safe error state
- unsupported schema version renders a safe incompatible state
- unsafe full-path-like display values are redacted
- disabled/deferred sections have no action controls
- no test fixture or snapshot contains raw private paths, raw Player.log
  contents, raw JSONL payloads, secrets, webhook URLs, API keys, or tokens

## Acceptance Criteria

Codex C satisfies this contract when:

- `frontend/` contains a React + TypeScript + Vite package.
- `frontend/package-lock.json` is committed and `node_modules/` is ignored.
- `frontend/package.json` contains the required npm scripts and Node engine
  policy.
- The first screen is a setup/status page, not a marketing landing page.
- The page consumes `GET /api/app/setup-status` through a typed API boundary.
- The page handles loading, ok/degraded/missing/unavailable/error,
  backend-unavailable, malformed-response, incompatible-response, and unsafe
  display-value states.
- Safe path labels are rendered and unsafe path-like values are not rendered.
- Manual import, analytics views, and live watcher sections are deferred
  display-only placeholders with no controls.
- No backend, parser, runtime, workbook, webhook, Apps Script, Sheets, Match
  Journal, OpenAI, AI, production, generated local artifact, secret, raw log, or
  local JSONL behavior changes occur.
- Required frontend and adjacent backend validation passes or failures are
  documented with exact command output.
- The implementation handoff records exact files changed, dependency versions,
  Node/npm versions, validation results, and unverified layers.

## Unknowns And Open Questions

- Exact local Node/npm versions are unknown until Codex C runs them.
- No backend server runner or launcher exists yet, so full live browser testing
  against a running backend may be unavailable.
- Backend CORS/server-origin behavior may need a later launcher or backend
  contract if same-origin/proxy-free development is awkward.
- Packaged mode and static file serving are not defined yet.
- A future frontend lint policy may be useful, but this first slice only
  requires typecheck, tests, and build.
- Future UI sections for manual import, analytics views, Match Journal, live
  watcher, OpenAI/AI, or Google Sheets require separate contracts.

## Suspected Gaps

- `.gitignore` currently lacks frontend generated-artifact entries.
- There is no frontend package or lockfile.
- There is no frontend validation in repo checks yet.
- There is no frontend-safe response-type contract in TypeScript.
- There is no browser smoke habit for the local app yet.
- There is no local launcher to start backend plus frontend together.

## Protected Surfaces

This contract does not authorize changes to:

- backend behavior or backend route payload shape
- parser behavior
- parser state final reconciliation
- parser event classes
- match/game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- output transport
- Google Sheets sync
- Match Journal or cockpit behavior
- OpenAI/model-provider behavior
- AI/coaching behavior
- production behavior
- deployment behavior
- secrets, credentials, environment variables, webhook URLs, API keys, tokens,
  or OAuth state
- raw Player.log files
- local legacy JSONL artifacts
- generated SQLite DB/WAL/SHM/journal files
- runtime logs/status files
- failed-delivery payload artifacts
- workbook exports
- generated card/tier data
- branch, merge, pull, push, or release behavior from the UI/frontend

## Out Of Scope

- Implementation code in the Codex B pass.
- Backend code changes.
- Manual import UI.
- File picker or drag/drop import controls.
- Live Player.log watcher controls.
- Parser runner process controls.
- Analytics dashboard pages.
- Match Journal or cockpit UI.
- Google Sheets sync.
- OpenAI/model-provider runtime integration.
- AI/coaching behavior.
- Installer/bootstrapper implementation.
- Launcher implementation.
- Production packaging.
- Static file serving from FastAPI.
- Destructive buttons or reset/delete/wipe actions.
- Any production-facing deploy behavior.

## Validation Expectations For This Contract

Codex B validation for this docs-only contract:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/analytics_react_vite_setup_status_page.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/analytics_react_vite_setup_status_page.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #209.

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

Goal:
Compare current repo state to the contract and implement only the first React + TypeScript + Vite setup-status page under frontend/. Produce docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated local artifacts.
- Confirm no frontend/ package exists already, or reconcile any existing frontend files against the contract.
- Record node --version and npm --version.
- State what the frontend setup-status page is supposed to do, what the repo currently does, why the gap exists, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/analytics_react_vite_setup_status_page.md
- docs/contracts/analytics_local_developer_app_shell.md
- docs/contracts/analytics_app_backend_setup_status.md
- docs/contract_test_reports/analytics_app_backend_setup_status.md
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/setup_status.py
- tests/test_analytics_local_app_backend.py
- tests/test_analytics_local_app_config.py
- pyproject.toml
- .gitignore

Implement only:
- frontend/ React + TypeScript + Vite package
- npm/package-lock policy required by the contract
- typed API client for GET /api/app/setup-status
- setup/status page and CSS
- focused frontend tests for ok/degraded, unavailable, malformed, incompatible schema, unsafe display redaction, and deferred no-control sections
- .gitignore additions for frontend generated artifacts only
- docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md

Do not:
- change backend behavior, backend route payload shape, Python source, parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, Google Sheets sync, Match Journal/cockpit behavior, OpenAI/model-provider behavior, AI/coaching behavior, production behavior, deployment behavior, secrets, raw logs, local JSONL artifacts, generated SQLite files, runtime status files, failed-delivery payload artifacts, workbook exports, generated data, or target main
- implement manual import UI, file pickers, drag/drop import, live watcher controls, parser runner controls, analytics dashboard pages, launcher/bootstrapper behavior, static FastAPI serving, destructive buttons, reset/delete/wipe actions, Git controls, Google Sheets controls, or OpenAI/AI controls
- commit node_modules, frontend/dist, frontend/.vite, coverage, .env files, secrets, tokens, webhook URLs, raw private paths, screenshots with private data, or local generated artifacts
- stage, commit, push, open a PR, close #204/#207/#208/#209, or merge unless explicitly asked

Validation:
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
git diff --check

Also run path-scoped protected-surface and secret/private-marker scans over the files touched by this issue.

If feasible after implementation, start the Vite dev server and verify the page renders a safe backend-unavailable state when no backend is running. If a backend server is not available, do not change backend code; document that live backend smoke remains unverified.

Final handoff must include:
- role performed
- source issue/tracker/umbrella issue/completed backend child
- source contract used
- files changed
- exact frontend modules/components/tests changed
- Node/npm versions used
- dependency and lockfile decision
- API consumption behavior
- UI states implemented
- what was verified
- what remains unverified
- whether any forbidden scope was touched
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/209"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_backend_child: "https://github.com/Tahjali11/Mythic-Edge/issues/208"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #209"
  target_artifact: "docs/contracts/analytics_react_vite_setup_status_page.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped protected-surface gate for docs/contracts/analytics_react_vite_setup_status_page.md"
    - "path-scoped secret/private-marker scan for docs/contracts/analytics_react_vite_setup_status_page.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main unless explicitly approved."
    - "Do not change backend behavior unless a later contract authorizes it."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
    - "Do not expose destructive UI actions."
```
