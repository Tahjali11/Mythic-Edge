# Analytics Local Developer App Shell Contract

## Module

Local developer app shell for Mythic Edge analytics usability.

This contract defines the umbrella boundaries for a Windows-first local
developer app made of:

- a Windows bootstrapper/setup surface
- a loopback-only FastAPI backend
- a React + TypeScript + Vite frontend
- a developer launcher
- an app-owned generated data folder under `%LOCALAPPDATA%\MythicEdgeDev\`

The app shell is an access and orchestration surface. It is not a parser, not a
second evidence ledger, not workbook sync, not Match Journal, not AI coaching,
not deploy tooling, and not a production installer.

## Source Issue

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Source artifact: GitHub issue #207 problem representation

## Branch

Current intended branch:

```text
codex/analytics-foundation
```

Observed during this contract pass:

```text
8dfc7b7394e55120c5026aeef87d77a650c551f9
```

The local branch was one commit ahead of
`origin/codex/analytics-foundation` during this contract pass. Codex B did not
push, open a PR, or target `main`.

## Risk Tier

High.

Reasons:

- the work introduces a local API and web UI action surface
- it introduces Node.js/npm/frontend dependency and lockfile policy
- it may create generated folders, local SQLite files, logs, imports, jobs, and
  diagnostics
- it may eventually start long-running parser or watcher processes
- it can expose private local paths or local artifact labels if not designed
  carefully
- it can blur parser truth, analytics storage, UI display, and human actions
- it overlaps nearby but separate Match Journal and cockpit work

## Contract Decision

Issue #207 should be treated as the umbrella contract for the local developer
app shell.

Implementation should split before code is added. Do not route this umbrella
contract directly to a broad Codex C implementation that adds bootstrapper,
backend, frontend, import workflows, analytics views, and live watcher behavior
all at once.

Recommended child issue order:

1. Windows app-data/config and backend health/config/path skeleton
2. React + TypeScript + Vite frontend shell and setup/status page
3. Windows developer launcher/bootstrapper setup workflow
4. Manual JSONL import orchestration through the existing adapter and analytics
   ingest
5. Curated read-only analytics views from SQLite
6. Live Player.log watcher status page
7. Live watcher process control and SQLite writes, only after manual import and
   replay ingest are proven

Plain English: this contract says what the whole local app is allowed to become,
but the first code slice should be small enough to review safely.

## Owning Layer

Primary owner: local analytics usability / developer app shell.

Truth boundaries:

- Parser/state owns MTGA event interpretation, match/game identity, final
  reconciliation, parser event classes, and parser-managed facts.
- The Player.log evidence ledger owns provenance, confidence, finality, drift,
  degradation, invariant, and review vocabulary.
- Analytics ingest owns copying parser-normalized facts into local SQLite.
- SQLite owns local queryable storage and deterministic views.
- The FastAPI backend owns local orchestration over existing services and local
  generated app state.
- The frontend owns display and user actions through backend endpoints only.
- The bootstrapper owns local setup orchestration only.

The app shell must not become parser truth, analytics truth, workbook truth, AI
truth, hidden-card inference, archetype classification, player-mistake truth,
gameplay advice, merge readiness, deploy readiness, or production authority.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_local_developer_app_shell.md`

Future child contracts may authorize new files such as:

- `src/mythic_edge_parser/local_app/`
- `tests/test_analytics_local_app_*.py`
- `frontend/`
- `tools/dev_app/`
- `docs/implementation_handoffs/analytics_local_developer_app_shell_*.md`

This umbrella contract does not itself authorize implementation changes.

Reference-only source surfaces:

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/app/config.py`
- `tools/auto_launcher/`
- `pyproject.toml`
- `.gitignore`
- existing analytics, runner, and status API tests

Not owned by this contract:

- parser behavior
- parser state final reconciliation
- parser event classes
- match/game identity or deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- output transport
- Google Sheets sync
- Match Journal or cockpit API behavior
- OpenAI/model-provider runtime integration
- AI/coaching behavior
- production deployment behavior
- generated SQLite files, WAL/SHM/journal files, raw Player.log files, private
  JSONL artifacts, runtime logs/status files, failed posts, workbook exports,
  generated card/tier data, secrets, credentials, tokens, API keys, or webhook
  URLs

## Observed Current Behavior

Repository and workflow:

- Issue #207 is open and describes the local developer app shell.
- Tracker #204 is open for analytics usability and local ingest.
- The intended integration branch is `codex/analytics-foundation`.
- No reviewed FastAPI backend exists in the repo.
- No React/Vite frontend exists in the repo.
- No `package.json`, frontend lockfile, Node version policy, or npm validation
  command exists in the current Python package metadata.
- `.gitignore` already ignores local/generated data roots including
  `data/analytics/`, runtime logs, status, failed posts, bad events, oracle
  data, tier sources, and local review artifacts.

Existing analytics building blocks:

- SQLite analytics schema and migrations exist.
- The migration loader applies plain SQL migrations to caller-supplied SQLite
  connections.
- Parser-normalized replay ingest exists.
- Gameplay-action, opponent-card-observation, and field-evidence ingest exist.
- Deterministic derived SQL views and replay/view validation harnesses exist.
- A legacy JSONL artifact adapter exists on this branch and adapts generated
  saved-event JSONL into parser-normalized replay input without trusting legacy
  derived labels as parser truth.

Existing operational surfaces:

- `runner.py` drives live parser runtime behavior and uses `MtgaEventStream`.
- `stream.py` tails MTGA `Player.log` from the end of the file and publishes
  events through the router and event bus.
- `config.py` is environment-driven and contains existing generated-data paths
  plus status API settings.
- `status_api.py` exposes a small stdlib HTTP API for status/runtime payloads.
- `tools/auto_launcher/manasight_launcher_auto.py` is a legacy Tkinter launcher
  with Manasight naming and direct local process/script management.

Observed gap:

- There is no reviewed app-owned local data folder contract.
- There is no reviewed local web backend/frontend contract.
- There is no reviewed Windows bootstrapper contract.
- There is no safe route inventory for app-shell endpoints.
- There is no frontend dependency, lockfile, or validation policy.
- There is no single local web UI that can display setup health, manual import
  state, curated analytics, diagnostics, or future watcher status.

## Required App Data Folder Contract

The local developer app must store generated app state outside the repo by
default:

```text
%LOCALAPPDATA%\MythicEdgeDev\
```

Required subfolders:

- `config\`
- `db\`
- `logs\`
- `imports\`
- `jobs\`
- `diagnostics\`

Required guarantees:

- The app must not create SQLite databases, logs, imports, jobs, or diagnostics
  inside the repo by default.
- The app must not overwrite an existing repo checkout.
- App-data creation must be idempotent. Running setup twice should preserve
  existing config and generated files unless a later child contract defines an
  explicit migration or backup behavior.
- Local app config must live under
  `%LOCALAPPDATA%\MythicEdgeDev\config\` unless a future contract authorizes a
  different location.
- Local SQLite database files must live under
  `%LOCALAPPDATA%\MythicEdgeDev\db\` for the app shell, even though lower-level
  analytics code may still support caller-supplied in-memory or temporary test
  connections.
- Raw Player.log contents and raw saved-event JSONL payloads must not be copied
  into the app-data folder unless a future sanitizer/import contract explicitly
  authorizes a redacted fixture-like artifact.
- App logs and diagnostics must not include secrets, webhook URLs, API keys,
  tokens, raw Player.log lines, raw JSONL payloads, or unnecessarily precise
  private paths.

## Local Config Contract

Recommended generated config path:

```text
%LOCALAPPDATA%\MythicEdgeDev\config\app_config.json
```

Allowed local config values:

- selected repo path
- app data root
- analytics database path
- Player.log path or detection status
- backend host/port preferences
- frontend dev-server port preferences
- safe feature flags for disabled/enabled app sections

Required guarantees:

- Local config is generated private state and must never be committed.
- Config may store full local paths because it is private local state, but
  committed tests, snapshots, logs, docs, and diagnostics must use temporary
  paths, redacted labels, or display-only path labels.
- Backend responses should default to safe display labels and booleans for
  diagnostics. Returning full paths to the local loopback frontend may be
  allowed only for explicit configuration screens and must not be copied into
  committed fixtures or logs.
- Environment variables may override config for development only. They must not
  become required for normal app use unless a child contract says so.
- Config must not store credentials, webhook URLs, OpenAI API keys, OAuth
  tokens, GitHub tokens, or Google credentials.

## Windows Bootstrapper Contract

The Windows bootstrapper may own:

- detecting Git, Python, Node.js, and npm availability
- checking the current repo or optionally cloning Mythic Edge from GitHub into a
  user-selected or default code location
- creating `%LOCALAPPDATA%\MythicEdgeDev\` and required subfolders
- creating or updating generated local config under app-data
- detecting likely MTGA Player.log locations without reading raw log contents
- installing Python dependencies in a repo-local environment when explicitly
  invoked
- installing frontend dependencies with lockfile-backed npm commands after a
  frontend child contract adds the frontend package
- initializing or smoke-checking a local SQLite database by calling existing
  migration loader behavior after the relevant child contract authorizes it
- creating a launcher script or shortcut
- running setup health checks and reporting actionable status

The bootstrapper must not:

- overwrite an existing repo checkout without explicit user approval
- silently run `git pull`, `git push`, branch switching, merges, rebases, resets,
  or remote writes
- commit generated files
- create, rotate, print, or modify credentials
- change production workbook, webhook, Apps Script, Google Sheets, Match
  Journal, OpenAI, AI/coaching, or deployment behavior
- change parser behavior
- delete app data, local imports, logs, diagnostics, generated databases, or
  repo files in the first version

Bootstrapper implementation should be split into its own child issue. The first
backend/frontend skeleton must not depend on a complete installer.

## Backend Contract

Future backend implementation should use FastAPI only after a child contract
authorizes dependency and package changes.

Recommended package boundary:

```text
src/mythic_edge_parser/local_app/
```

The backend may own:

- loopback-only local API routes
- health/config/runtime path reporting
- app-data folder discovery and non-destructive creation through helpers
- safe Player.log path detection/configuration workflow
- local SQLite database initialization by calling the analytics migration loader
- manual JSONL import orchestration by calling the existing legacy JSONL adapter
  and analytics ingest code
- job/status tracking for long-running imports or future watcher processes
- read-only analytics query endpoints over existing SQLite tables and views
- future live watcher lifecycle/status only after a later contract authorizes it

The backend must not:

- reinterpret raw Player.log events outside parser-owned code
- change parser behavior or final reconciliation
- create frontend-owned parser facts
- store raw Player.log payloads in SQLite
- expose secrets, webhook URLs, API keys, tokens, or raw local artifact contents
- perform git branch/pull/push/merge/reset operations from the UI
- call OpenAI or model providers
- write Google Sheets
- change workbook/webhook/Apps Script behavior
- expose destructive local-file or database deletion actions in the first
  version

### First Backend Endpoint Inventory

The first implementation child should be limited to read-only health/config/path
reporting plus safe app-data helper tests.

Recommended first endpoints:

- `GET /api/health`
- `GET /api/app/config`
- `GET /api/app/paths`
- `GET /api/analytics/database/status`
- `GET /api/runtime/status`

First endpoint guarantees:

- Bind to `127.0.0.1` by default, not `0.0.0.0`.
- Use explicit local development CORS origins such as
  `http://127.0.0.1:<frontend_port>` and `http://localhost:<frontend_port>`.
- Return JSON only.
- Return safe display labels for private paths by default.
- Do not import JSONL artifacts.
- Do not tail Player.log.
- Do not start the parser runner.
- Do not create or mutate SQLite facts except for future explicit database
  initialization after a child contract authorizes it.
- Do not read raw Player.log contents.
- Do not expose destructive actions.

Future endpoints for import, analytics views, jobs, and live watcher behavior
must be introduced by later child contracts.

## Frontend Contract

Future frontend implementation should use React + TypeScript + Vite only after
a child contract authorizes dependency and package changes.

Recommended folder:

```text
frontend/
```

The frontend may own:

- setup/status display
- safe local path/config display and configuration forms
- manual import form in a later child issue
- import/job history display in a later child issue
- live watcher status display in a later child issue
- curated read-only analytics pages in later child issues
- diagnostics/import-quality pages
- calls to backend API routes

The frontend must not:

- write SQLite directly
- import Python internals
- own parser truth, analytics truth, or evidence truth
- expose destructive actions in the first version
- expose secrets, webhook URLs, API keys, tokens, raw local artifacts, or raw
  Player.log content
- implement Google Sheets, Match Journal, OpenAI, model-provider, or AI coaching
  behavior
- classify archetypes, infer hidden cards, label player mistakes, or provide
  gameplay advice as facts

### First Frontend View Inventory

The first frontend child should be a setup/status shell only.

Required first views or panels:

- setup health
- backend health
- app-data folder status
- analytics database status
- Player.log detection/configuration status
- disabled placeholders for manual import, analytics views, and live watcher
  sections

The first frontend must not expose:

- delete buttons
- reset database buttons
- raw file viewers
- Git controls
- production deployment controls
- Google Sheets sync controls
- OpenAI/AI controls
- live watcher start/stop controls unless a later child contract authorizes
  them

## Node.js And npm Policy

No Node/npm files are authorized by this Codex B contract-writing pass.

When a frontend child contract authorizes implementation:

- `frontend/package.json` must define exact npm scripts used for validation.
- `frontend/package-lock.json` must be committed with dependency changes.
- `node_modules/` must never be committed.
- The Node version policy must be documented in `frontend/package.json`
  `engines.node` or a dedicated version file chosen by that child contract.
- npm must be the first package manager unless a future contract explicitly
  authorizes pnpm, yarn, or another tool.
- Frontend validation commands must be deterministic and non-interactive.

Recommended future commands:

```powershell
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run lint
npm --prefix frontend run build
```

Exact commands must be defined by the frontend child contract after
`package.json` exists.

## Developer Launcher Contract

First launcher mode should be developer mode only.

The developer launcher may own:

- starting the FastAPI backend
- starting the Vite dev server
- opening the browser to the local frontend
- writing basic non-secret process logs under app-data
- reporting child process status
- stopping child processes it started when possible

The launcher must not:

- silently kill unrelated Python, Node, MTGA, browser, or shell processes
- leave hidden long-running processes without visible status
- change parser behavior
- start live Player.log writes until a later contract authorizes it
- run destructive cleanup
- run git operations from the UI
- require packaged app mode in the first slice

Packaged mode may be considered later after the developer shell, backend,
frontend, import workflow, and read-only analytics views are stable.

## Manual Import Before Live Watcher

Manual JSONL import must come before live watcher writes.

Required sequence:

1. app shell and setup/status views
2. manual JSONL import using existing
   `analytics_legacy_jsonl_adapter.py` and `analytics_ingest.py`
3. read-only analytics views over imported SQLite data
4. live watcher status only
5. live watcher process control
6. live watcher writes completed parser-owned facts to SQLite

Reason: manual import is easier to validate because the selected input is fixed.
Live Player.log watching is more fragile because the file may be actively
written, rotated, truncated, incomplete, or duplicated.

Manual import routes must not store raw JSONL payloads in SQLite and must not
trust legacy `derived` fields as parser truth.

## Curated Analytics View Boundaries

Future analytics views should be read-only projections over existing SQLite
tables and views.

Recommended first view families:

- match history
- game history
- opening hands
- mulligans and bottomed/discarded cards when available
- first turns / opening line review from existing deterministic views
- gameplay action review
- opponent card observations
- import quality and diagnostics

These pages must not become:

- broad SQL browser
- hidden-card inference
- complete-decklist inference
- sideboard-delta truth
- archetype classification truth
- player-mistake labels
- gameplay advice
- AI coaching
- parser truth
- deploy readiness

## Match Journal And External Surface Boundaries

Issue #207 must not continue, close, redefine, or implement paused Match
Journal/cockpit work from issues #202 and #203 unless the user explicitly
reauthorizes that work through a scoped issue and contract.

This app shell also does not authorize:

- Google Sheets sync
- Google Docs collaboration edits
- Apps Script behavior
- webhook payload changes
- OpenAI API runtime integration
- model-provider behavior
- AI coaching evaluation
- production deployment behavior
- live external writes

## Required Guarantees

For all future child implementations:

- Preserve parser truth ownership.
- Keep app-generated files out of Git.
- Keep private local paths, raw logs, raw JSONL payloads, secrets, and webhook
  URLs out of committed tests, docs, screenshots, and logs.
- Use existing parser/analytics public interfaces instead of duplicating parser
  interpretation in the UI or backend.
- Keep manual import and live watcher behavior separate.
- Prefer read-only routes and UI first.
- Make any state-changing action explicit, narrow, test-covered, and
  non-destructive.
- Keep backend/frontend dependency changes deterministic and reviewable.
- Stop and route back to Codex B if implementation needs schema changes,
  parser changes, new protected-surface behavior, or a broader dependency
  strategy.

## Unknowns And Open Questions

- Exact child issue IDs are not yet created.
- The final FastAPI package name is not implemented; `local_app` is the
  recommended boundary but may be adjusted by a focused child contract.
- The frontend folder is not implemented; `frontend/` is the recommended folder
  but may be adjusted by a focused child contract.
- The exact Node version is not known.
- The exact launcher language is not decided. PowerShell-first, Python-first,
  or a small pair of scripts are all possible future options.
- The app config schema is not implemented.
- Full-path display rules need concrete tests in the first backend/frontend
  child implementation.
- Live watcher process-control safeguards need their own contract before code.
- Database initialization behavior must decide when folder/database creation is
  automatic versus explicit.

## Suspected Gaps

- `status_api.py` currently uses stdlib HTTP and broad CORS behavior. It is a
  useful reference surface, but it is not the reviewed FastAPI app shell.
- `config.py` currently includes a Windows default Player.log path and repo
  `data/` paths. A local app must avoid leaking private paths into committed
  artifacts and should use app-data paths for generated app files.
- `tools/auto_launcher/manasight_launcher_auto.py` remains legacy Manasight
  launcher code with direct process/script management. It should be treated as
  reference-only unless a child contract deliberately migrates or replaces
  behavior.
- There is no frontend dependency policy yet.
- There are no app-data helper tests.
- There are no backend route tests.
- There are no frontend build/typecheck tests.
- There is no job-status model for imports or future watcher processes.

## Protected Surfaces

This contract does not authorize changes to:

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
- Match Journal or cockpit API behavior
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
- failed posts
- workbook exports
- generated card/tier data
- branch, merge, pull, push, or release behavior from the UI

## Out Of Scope

- Implementation code in the Codex B pass.
- Adding FastAPI, React, Vite, TypeScript, npm, package files, or lockfiles in
  this pass.
- Creating a SQLite database file.
- Creating app-data folders in this pass.
- Copying, sanitizing, or committing local raw logs or JSONL artifacts.
- Final app packaging.
- macOS installer.
- public end-user installer.
- Google Sheets sync.
- Match Journal work.
- workbook schema, webhook, or Apps Script changes.
- OpenAI/model-provider runtime integration.
- AI coaching.
- Line Tracer.
- gameplay advice.
- hidden-card inference.
- archetype classification.
- player-mistake labels as facts.
- destructive UI actions.
- git pull/push/merge/branch switching from the UI.
- production deployment behavior.

## Validation Expectations

Codex B validation for this docs-only contract:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/analytics_local_developer_app_shell.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Expected validation for the first backend/app-data child implementation:

```powershell
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_*.py tests\test_status_api.py tests\test_runner.py
py -m ruff check src tests tools
git diff --check
py tools\check_secret_patterns.py --all
```

Expected validation after frontend files exist:

```powershell
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run lint
npm --prefix frontend run build
git diff --check
py tools\check_secret_patterns.py --all
```

Expected evidence for future Codex C/E work:

- backend health/config/path endpoints tested with temporary app-data roots
- loopback-only bind and CORS behavior tested
- generated folders and databases created only under temporary paths in tests
- app-data generated files remain ignored and uncommitted
- frontend builds and typechecks without raw local path fixtures
- manual import route, when implemented, calls existing adapter and ingest
  boundaries
- no raw Player.log payloads are stored in SQLite
- no dangerous UI actions are exposed
- protected-surface and secret/private marker checks pass

## Acceptance Criteria

This contract is accepted when:

- `docs/contracts/analytics_local_developer_app_shell.md` exists.
- It defines the app shell as an access/orchestration surface, not a truth
  surface.
- It records the app-data folder contract under
  `%LOCALAPPDATA%\MythicEdgeDev\`.
- It defines bootstrapper, backend, frontend, launcher, manual import,
  analytics view, and live watcher boundaries.
- It defines the recommended implementation split before code.
- It preserves all protected surfaces and forbids destructive first-version UI
  actions.
- Docs-only validation passes or failures are documented.

## Next Workflow Action

Next role: Codex A: Thinker / Problem Representation for the first focused
implementation child issue.

Recommended child issue title:

```text
[analytics/app] Local app backend config and setup-status skeleton
```

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex A: Thinker / Problem Representation for the first implementation child of the local developer app shell.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Source contract:
docs/contracts/analytics_local_developer_app_shell.md

Current branch:
codex/analytics-foundation

Goal:
Create the first focused child issue for a local app backend config and setup-status skeleton. This child should cover only app-data path helpers, generated local config boundaries, loopback-only FastAPI backend skeleton, read-only health/config/path/database-status endpoints, and focused tests. It should not add the React/Vite frontend, manual import UI, live watcher behavior, launcher process control, database writes beyond explicitly tested initialization/status behavior, or any production/external integrations.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/contracts/analytics_local_developer_app_shell.md
- docs/contracts/analytics_local_sqlite_schema.md
- docs/contracts/analytics_migration_loader.md
- src/mythic_edge_parser/app/analytics_migration_loader.py
- src/mythic_edge_parser/app/status_api.py
- src/mythic_edge_parser/app/config.py
- pyproject.toml
- .gitignore
- tests/test_status_api.py
- existing analytics migration/schema tests

The issue should define:
- what the first backend/config skeleton is supposed to prove
- exact in-scope endpoints
- app-data/config path behavior under temporary test roots
- FastAPI dependency and optional dependency-group recommendation
- loopback-only and CORS boundaries
- path redaction/display rules
- forbidden actions and protected surfaces
- validation evidence needed
- expected contract artifact for Codex B
- pasteable Codex B prompt
- workflow_handoff block

Do not implement code.
Do not add FastAPI, frontend, npm, package files, lockfiles, launcher behavior, manual import behavior, live watcher behavior, Google Sheets sync, Match Journal behavior, OpenAI/model-provider behavior, AI/coaching behavior, production behavior, or destructive UI actions.
Do not change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, raw logs, local JSONL artifacts, generated SQLite files, runtime status files, failed posts, workbook exports, generated data, or target main.
Do not close tracker #204.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  completed_thread: "B"
  next_thread: "A"
  source_artifact: "GitHub issue #207"
  target_artifact: "docs/contracts/analytics_local_developer_app_shell.md"
  branch: "codex/analytics-foundation"
  risk_tier: "High"
  decision: "Treat #207 as an umbrella app-shell contract and split implementation into focused child issues before Codex C code work."
  recommended_next_issue_title: "[analytics/app] Local app backend config and setup-status skeleton"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped protected-surface gate for docs/contracts/analytics_local_developer_app_shell.md"
  stop_conditions:
    - "Do not implement code from the umbrella contract directly."
    - "Do not target main unless explicitly approved."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
    - "Do not expose destructive UI actions."
```
