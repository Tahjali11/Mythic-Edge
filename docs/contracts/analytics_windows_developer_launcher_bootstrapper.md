# Analytics Windows Developer Launcher Bootstrapper Contract

## Module

Windows developer launcher and bootstrapper setup workflow.

This contract defines the next local developer app slice under the analytics
usability umbrella: a Windows-only, existing-checkout launcher/preflight
workflow that can check prerequisites, prepare safe app-owned folders, start
the local FastAPI backend, start the Vite frontend, optionally open the browser,
and clean up only the child processes it started.

Plain English: this is the "start my local app" button, but as a careful
developer tool. It is not a public installer, not a repo updater, not live
Player.log watching, and not a place to hide destructive cleanup.

## Source Issue

- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/210>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Completed backend child: <https://github.com/Tahjali11/Mythic-Edge/issues/208>
- Completed frontend child: <https://github.com/Tahjali11/Mythic-Edge/issues/209>
- Umbrella contract: `docs/contracts/analytics_local_developer_app_shell.md`
- Backend contract: `docs/contracts/analytics_app_backend_setup_status.md`
- Frontend contract: `docs/contracts/analytics_react_vite_setup_status_page.md`

## Branch

Current intended branch:

```text
codex/analytics-foundation
```

Observed during this Codex B pass:

```text
db1638bf263048b2627f24c7a4b594a0d5dbcda5
```

Local branch state observed:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
```

`HEAD...origin/codex/analytics-foundation` was even (`0 0`) during this
contract pass. This contract does not stage, commit, push, open a PR, close
issues, or target `main`.

## Authority And Source Artifacts Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- tracker #204
- umbrella issue #207
- completed child #208
- completed child #209
- source issue #210
- `docs/project_roadmap.md`
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_app_backend_setup_status.md`
- `docs/contracts/analytics_react_vite_setup_status_page.md`
- `src/mythic_edge_parser/local_app/`
- `frontend/package.json`
- `frontend/vite.config.ts`
- `pyproject.toml`
- `.gitignore`
- `tools/auto_launcher/`
- existing backend/frontend tests and validation commands

## Risk Tier

High.

Reasons:

- may start and stop local backend/frontend processes
- may create app-owned local folders and log files
- inspects local toolchain and filesystem state
- can expose private local paths if console/log output is loose
- can accidentally grow into repo update, clone, destructive cleanup, live
  watcher, parser runner, database reset, or production behavior
- must preserve a hard boundary between launcher status and parser/analytics
  truth

## Owning Layer

Primary owner: local developer app launcher / setup orchestration.

Truth boundaries:

- Parser/state owns MTGA event interpretation, match/game identity, final
  reconciliation, parser event classes, and parser-managed facts.
- Evidence ledger owns provenance, confidence, finality, drift, degradation,
  invariant, and review vocabulary.
- SQLite analytics remains downstream local storage and query surface, not
  parser truth.
- Backend setup/status owns setup/status response semantics.
- Frontend owns setup/status display and navigation only.
- Launcher owns local process orchestration, preflight checks, app-data folder
  preparation, log placement, and browser opening only.

The launcher must not become parser truth, analytics truth, evidence truth,
workbook truth, AI truth, gameplay advice, hidden-card inference, archetype
classification, player-mistake truth, merge readiness, deploy readiness,
production authority, or repo authority.

## Contract Decision

Issue #210 should be implemented as an existing-checkout developer
launcher/preflight workflow.

Clone-from-GitHub, repo update, branch switching, shortcut creation, full
installer behavior, config writing, database initialization, manual import, live
watcher control, and packaged app mode are deferred to later issues/contracts.

Reason: backend and frontend already exist. The immediate usability gap is
safe startup and status for a repo checkout that already exists. Clone/update
behavior adds remote-write and checkout-overwrite risk, so it needs its own
explicit contract before implementation.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_windows_developer_launcher_bootstrapper.md`

Future Codex C implementation files authorized by this contract:

- `tools/dev_app/dev_app_launcher.py`
- `tools/dev_app/start_mythic_edge_dev_app.ps1`
- `tests/test_analytics_dev_app_launcher.py`
- `docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md`

Conditional implementation file:

- `pyproject.toml`, only to add `uvicorn` to the optional `app` dependency group
  and to `dev` if required for committed tests and local launcher validation.

Referenced but not owned:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `frontend/package.json`
- `frontend/vite.config.ts`
- `tools/auto_launcher/`
- `.gitignore`

Codex C must route back to Codex B before editing referenced-but-not-owned
backend, frontend, parser, legacy launcher, or configuration files.

## Observed Current Behavior

Repository state:

- Backend setup/status issue #208 is complete and closed.
- Frontend setup/status issue #209 is complete and closed.
- Tracker #204 and umbrella issue #207 remain open.
- Source issue #210 is open.
- `src/mythic_edge_parser/local_app/backend.py` exposes a FastAPI app factory
  and read-only setup/status routes.
- `frontend/` contains a React + TypeScript + Vite setup/status page with npm
  scripts for `dev`, `typecheck`, `test`, `build`, and `preview`.
- `.gitignore` already ignores frontend generated artifacts.
- `pyproject.toml` includes optional FastAPI app dependencies and dev FastAPI
  test support, but it does not include `uvicorn`.
- No reviewed `tools/dev_app/` launcher exists.
- No reviewed command starts backend plus frontend together.
- No reviewed launcher creates app-data folders or local launcher logs.

Legacy launcher state:

- `tools/auto_launcher/manasight_launcher_auto.py` is a large Tkinter launcher
  with legacy naming.
- It directly manages processes, reads repo-local runtime artifacts, references
  legacy artifact paths, and exposes many helper actions.
- It should be treated as reference-only for implementation ideas. Do not copy
  it wholesale or expand its behavior under this issue.
- Existing `tools/auto_launcher/*.bat` and `*.vbs` wrappers remain legacy
  surfaces and are not owned by this contract.

Observed gap:

- A user still needs to remember separate backend/frontend commands.
- There is no dry-run preflight mode for local prerequisites.
- There is no one-command developer startup path for the local app.
- There is no launcher-owned safe log location.
- There is no tested guarantee that launcher cleanup touches only child
  processes it started.

## Public Interface

Required implementation entrypoints:

```text
tools/dev_app/start_mythic_edge_dev_app.ps1
tools/dev_app/dev_app_launcher.py
```

The PowerShell script is the Windows-friendly entrypoint. The Python helper is
the testable implementation boundary.

Required Python CLI:

```powershell
py tools\dev_app\dev_app_launcher.py check
py tools\dev_app\dev_app_launcher.py start
```

Required PowerShell wrapper behavior:

```powershell
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Start
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Start -NoOpen
```

Required shared options:

- backend port, default `8765`
- frontend port, default `5173`
- app-data root override for tests only
- no-open flag
- log-to-console flag or equivalent testable output capture

Allowed status labels:

- `ok`
- `missing`
- `unavailable`
- `warning`
- `starting`
- `running`
- `failed`
- `stopped`
- `skipped`
- `deferred`

The launcher must use stable text output that can be asserted in tests. It may
also output JSON only if Codex C keeps the human-readable mode and records the
shape in the implementation handoff.

## Dependency Decision

The launcher may require `uvicorn` because the current backend exposes an ASGI
app factory but no server runner.

Codex C may update `pyproject.toml` with:

```toml
[project.optional-dependencies]
app = [
  "fastapi>=0.115,<1",
  "uvicorn>=0.30,<1",
]
dev = [
  "fastapi>=0.115,<1",
  "httpx>=0.27,<1",
  "uvicorn>=0.30,<1",
  ...
]
```

The exact placement may differ if Codex C preserves the existing dependency
groups and explains the choice. `uvicorn` must not become a required core
parser runtime dependency.

No new Node package, npm script, frontend dependency, global package install,
or package manager change is authorized by this contract.

## Inputs

### Repo Root

Type: filesystem path.

Source:

- current working directory
- parent discovery from the script path
- explicit test override

Required repo-root markers:

- `AGENTS.md`
- `pyproject.toml`
- `src/mythic_edge_parser/local_app/backend.py`
- `frontend/package.json`

If the markers are absent, report `missing` or `failed` and do not start
processes.

### App Data Root

Type: filesystem path.

Default:

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

Behavior:

- `check` mode reports folder status without creating folders.
- `start` mode may create the required subfolders and a launcher run-log folder
  under `logs\launcher\`.
- Tests must use an explicit temporary app-data root override.

### Toolchain

Required checks:

- Windows platform
- Python via the Windows `py` launcher or current Python executable
- importable `mythic_edge_parser`
- importable `fastapi`
- importable `uvicorn`
- Node.js through `node --version`
- npm through `npm --version`
- frontend package and lockfile present
- Git through `git --version`

Git check is informational only for this first slice. The launcher must not run
`git pull`, `git push`, branch switching, reset, merge, rebase, or clone.

### Ports

Defaults:

- backend host: `127.0.0.1`
- backend port: `8765`
- frontend host: `127.0.0.1`
- frontend port: `5173`

Requirements:

- `0.0.0.0` is not authorized.
- non-loopback hosts are not authorized.
- invalid or unavailable ports should report a clear status and refuse to start
  affected child processes.
- port conflicts must not trigger process killing.

## Outputs

### Console Status

Destination: PowerShell/terminal output.

Required properties:

- concise human-readable preflight summary
- clear missing-prerequisite messages
- child process start result
- frontend URL when started
- log directory label when logs are written
- no raw private user-profile paths by default
- no secrets, tokens, webhook URLs, raw Player.log content, raw JSONL content,
  generated database content, or runtime payload dumps

### App Logs

Destination:

```text
%LOCALAPPDATA%\MythicEdgeDev\logs\launcher\<run-id>\
```

Allowed files:

- `launcher.log`
- `backend.log`
- `frontend.log`

Required guarantees:

- log directory is created only in `start` mode
- tests use temporary app-data roots
- obvious user-profile, repo-root, and app-data-root path values are redacted
  before writing launcher-managed logs
- logs must not include secrets, tokens, webhook URLs, raw Player.log lines, raw
  JSONL payloads, generated SQLite contents, failed-delivery payload contents,
  or workbook export contents

### Child Processes

Child process commands:

Backend:

```powershell
py -m uvicorn mythic_edge_parser.local_app.backend:create_app --factory --host 127.0.0.1 --port 8765
```

Frontend:

```powershell
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173
```

Frontend environment:

```text
VITE_MYTHIC_EDGE_API_BASE_URL=http://127.0.0.1:8765
```

The launcher must not add or commit `.env` files. The environment override is
process-local only.

## Invariants

- `check` mode has no filesystem writes, process starts, browser opens, or
  network side effects.
- `start` mode may create only app-data subfolders and launcher logs.
- `start` mode may start only the backend and frontend child processes defined
  by this contract.
- The launcher cleans up only child processes it started.
- The launcher never kills unrelated Python, Node, browser, shell, MTGA, or
  parser processes.
- The launcher never runs Git mutating commands.
- The launcher never reads raw Player.log contents.
- The launcher never imports JSONL artifacts.
- The launcher never creates, migrates, resets, deletes, vacuums, compacts, or
  writes SQLite databases.
- The launcher never starts live Player.log watching.
- The launcher never starts parser runner process control.
- The launcher never changes backend route payloads or frontend behavior.
- Missing prerequisites are setup statuses, not parser failures.

## Error Behavior

Missing Python/FastAPI/uvicorn:

- report a blocking prerequisite failure
- do not start frontend
- suggest the existing editable install command only as text, without running it

Missing Node/npm/frontend package:

- report a blocking prerequisite failure
- do not start backend or frontend
- suggest `npm --prefix frontend ci` only as text, without running it

Missing Git:

- report a warning for an existing checkout
- do not run clone/update behavior

Missing `%LOCALAPPDATA%`:

- in `check` mode, report unavailable
- in `start` mode, fail safely unless an explicit app-data root override is
  provided

Port in use:

- report the affected port as unavailable
- do not kill the owning process
- allow the user to choose another port by option

Backend start failure:

- report backend failed
- terminate any frontend child process the launcher already started
- write redacted logs

Frontend start failure:

- report frontend failed
- terminate backend child process the launcher started
- write redacted logs

Browser open failure:

- report a warning
- keep already started child processes running only if startup otherwise
  succeeded and the user can use the printed URL

Ctrl+C or launcher exit:

- terminate child processes started by the current launcher run
- do not scan for or kill similarly named unrelated processes

Contract conflict:

- if implementation needs clone/update, config writes, database initialization,
  persistent service installation, shortcut creation, backend route changes,
  frontend route changes, live watcher behavior, or parser runner control,
  route back to Codex B.

## Side Effects

Allowed side effects in Codex C:

- add `tools/dev_app/dev_app_launcher.py`
- add `tools/dev_app/start_mythic_edge_dev_app.ps1`
- add focused launcher tests
- add implementation handoff
- update `pyproject.toml` only for optional `uvicorn` dependency metadata

Allowed runtime side effects of the implemented launcher:

- create app-data subfolders under the configured app-data root in `start` mode
- create launcher log files under app-data in `start` mode
- start backend and frontend child processes in `start` mode
- open a browser to the local frontend unless disabled
- terminate child processes started by the current launcher run

Forbidden side effects:

- no clone/update behavior
- no Git mutating commands
- no public installer
- no shortcut creation
- no Windows service or scheduled task
- no config file writes
- no SQLite database writes or initialization
- no manual import
- no live watcher
- no parser runner process control
- no backend/frontend behavior changes
- no Google Sheets, workbook, webhook, Apps Script, Match Journal, OpenAI,
  AI/coaching, production, or deployment behavior changes
- no secrets, credentials, tokens, webhook URLs, raw logs, local JSONL
  artifacts, generated databases, runtime artifacts, failed-delivery payload
  artifacts, workbook exports, or generated card/tier data

## Dependency Order

Recommended Codex C order:

1. Confirm branch and clean worktree state.
2. Read this contract plus backend/frontend contracts.
3. Confirm backend and frontend committed surfaces still exist.
4. Decide whether `uvicorn` metadata is needed and update only optional
   dependency groups if needed.
5. Add testable Python helper with no import-time side effects.
6. Add focused tests for preflight, command construction, safe output, app-data
   creation, process tracking, and cleanup behavior.
7. Add thin PowerShell wrapper.
8. Run focused launcher tests.
9. Run backend/frontend validation.
10. Write implementation handoff.

## Compatibility

Must remain compatible with:

- backend setup/status schema version
  `analytics_app_backend_setup_status.v1`
- frontend setup/status package under `frontend/`
- existing npm validation scripts
- optional app dependency model in `pyproject.toml`
- app-data root and subfolder contract under `%LOCALAPPDATA%\MythicEdgeDev\`
- existing legacy `tools/auto_launcher/` files as reference-only artifacts

This contract does not require changing the legacy Tkinter launcher, the
stdlib `status_api.py`, FastAPI routes, frontend API client, runner, stream,
runtime surfaces, parser config, or analytics ingest.

## Tests Required

Focused launcher tests:

```powershell
py -m pytest -q tests\test_analytics_dev_app_launcher.py
```

Adjacent backend validation:

```powershell
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
```

Frontend validation:

```powershell
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
```

Static and repository checks:

```powershell
py -m ruff check src tests tools
git diff --check
```

Path-scoped protected-surface check:

```powershell
@'
pyproject.toml
tools/dev_app/dev_app_launcher.py
tools/dev_app/start_mythic_edge_dev_app.ps1
tests/test_analytics_dev_app_launcher.py
docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Path-scoped secret/private-marker scan:

```powershell
@'
pyproject.toml
tools/dev_app/dev_app_launcher.py
tools/dev_app/start_mythic_edge_dev_app.ps1
tests/test_analytics_dev_app_launcher.py
docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Optional manual smoke, only if Codex C can guarantee cleanup:

```powershell
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check
```

Do not require an automated `-Start` smoke in Codex C unless the implementation
can start and terminate child processes deterministically in the same command.

Required assertions:

- `check` mode does not create app-data folders, logs, databases, config files,
  or child processes
- `start` mode creates only app-data subfolders and launcher logs under a
  temporary root in tests
- backend and frontend command construction uses loopback hosts and expected
  ports
- frontend child receives process-local
  `VITE_MYTHIC_EDGE_API_BASE_URL`
- missing prerequisites are reported clearly
- port conflicts do not kill existing processes
- cleanup terminates only fake child processes started by the launcher
- console/log output redacts temporary roots and private path-like values
- no tests or fixtures contain secrets, webhook URLs, raw Player.log content,
  raw JSONL payloads, generated database contents, or failed-delivery payload
  contents

## Acceptance Criteria

Codex C satisfies this contract when:

- `tools/dev_app/dev_app_launcher.py` exists and is testable without starting
  real backend/frontend processes.
- `tools/dev_app/start_mythic_edge_dev_app.ps1` exists as a thin Windows
  wrapper.
- The first implementation targets an existing checkout only.
- Clone/update/install/shortcut/config/database/manual-import/live-watcher
  behavior is deferred.
- The launcher supports dry-run `check` and explicit `start` modes.
- Startup commands use `127.0.0.1` for backend and frontend.
- `start` mode creates only approved app-data folders/logs and starts only
  approved child processes.
- Cleanup touches only child processes from the current launcher invocation.
- `pyproject.toml` keeps server-runner dependencies optional if changed.
- Focused, adjacent backend, frontend, Ruff, diff, protected-surface, and
  secret/private-marker checks pass or are documented.
- Implementation handoff records exact files changed, process commands,
  dependency decisions, validation results, and unverified layers.

## Unknowns And Open Questions

- Whether a later bootstrapper should clone Mythic Edge from GitHub or only
  prepare an existing checkout.
- Whether shortcut creation should be a later script or part of a Windows
  bootstrapper.
- Whether database initialization belongs in the launcher, backend, or a
  separate setup action.
- Whether future live watcher process control should reuse this launcher
  process model or go through backend job orchestration.
- Whether packaged mode should serve built frontend assets from FastAPI later.
- Whether future setup actions should write `app_config.json`, and which layer
  should own that schema.

## Suspected Gaps

- There is no reviewed one-command startup path yet.
- `uvicorn` is not currently included in optional app dependencies.
- Existing backend has an app factory but no server-runner command.
- Existing frontend requires a backend origin override for Vite dev mode.
- Legacy `tools/auto_launcher/` contains too much behavior and should not be
  used as the first local app launcher implementation.
- No tests currently prove launcher cleanup cannot terminate unrelated
  processes.

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
- Google Sheets behavior
- Match Journal behavior
- OpenAI/model-provider behavior
- AI/coaching behavior
- production behavior
- deployment behavior
- backend route payload shape
- frontend setup/status behavior
- secrets, credentials, tokens, API keys, webhook URLs, or environment-variable
  contracts
- raw Player.log files
- private legacy JSONL artifacts
- generated SQLite database/WAL/SHM/journal files
- runtime status files
- failed-delivery payload artifacts
- workbook exports
- generated card/tier data
- clone/update/branch/merge/reset/rebase/push behavior

## Out Of Scope

- Implementation code in the Codex B pass.
- Public installer.
- macOS support.
- Packaged desktop app build.
- Clone-from-GitHub implementation.
- Git update behavior.
- Shortcut creation.
- Persistent background service installation.
- Config writes.
- Database initialization.
- Manual JSONL import UI.
- Live Player.log watching or live writes.
- Analytics dashboard pages.
- Database reset/delete/wipe actions.
- Destructive cleanup actions.
- Google Sheets sync.
- Match Journal work.
- OpenAI/model-provider runtime integration.
- AI coaching.
- Line Tracer.
- Production deployment behavior.

## Validation Expectations For This Contract

Codex B validation for this docs-only contract:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/analytics_windows_developer_launcher_bootstrapper.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/analytics_windows_developer_launcher_bootstrapper.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #210.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/210

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Completed backend child:
https://github.com/Tahjali11/Mythic-Edge/issues/208

Completed frontend child:
https://github.com/Tahjali11/Mythic-Edge/issues/209

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_windows_developer_launcher_bootstrapper.md

Goal:
Compare current repo state to the contract and implement only the Windows existing-checkout developer launcher/preflight workflow. Produce docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated local artifacts.
- State what the launcher is supposed to do, what the repo currently does, why the gap exists, and the exact minimal implementation plan.
- Confirm backend/frontend committed surfaces still exist.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/analytics_windows_developer_launcher_bootstrapper.md
- docs/contracts/analytics_local_developer_app_shell.md
- docs/contracts/analytics_app_backend_setup_status.md
- docs/contracts/analytics_react_vite_setup_status_page.md
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/paths.py
- frontend/package.json
- frontend/vite.config.ts
- pyproject.toml
- .gitignore
- tools/auto_launcher/

Implement only:
- tools/dev_app/dev_app_launcher.py
- tools/dev_app/start_mythic_edge_dev_app.ps1
- tests/test_analytics_dev_app_launcher.py
- optional pyproject.toml uvicorn dependency metadata if required by the contract
- docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md

Required behavior:
- existing-checkout only
- check mode is dry-run and has no writes/process/browser effects
- start mode may create app-data subfolders and launcher logs under app-data
- start mode may start only the FastAPI backend and Vite frontend child processes
- frontend child receives process-local VITE_MYTHIC_EDGE_API_BASE_URL
- browser open is optional and disabled by -NoOpen/--no-open
- cleanup terminates only child processes started by the current launcher run
- missing prerequisites and port conflicts are reported without destructive action
- console/log output uses safe/redacted path labels

Do not:
- implement clone/update behavior, public installer, macOS support, packaged desktop app build, shortcut creation, config writes, database initialization, manual import UI, live watcher controls, parser runner controls, analytics dashboard pages, destructive cleanup, database reset/delete/wipe, Git mutating commands, Google Sheets sync, Match Journal behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer, production behavior, or deployment behavior
- change backend behavior, backend route payload shape, frontend setup/status behavior, parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, raw logs, local JSONL artifacts, generated SQLite files, runtime status files, failed-delivery payload artifacts, workbook exports, generated data, or target main
- edit tools/auto_launcher/ except to read it as reference-only
- stage, commit, push, open a PR, close #204/#207/#210, or merge unless explicitly asked

Validation:
py -m pytest -q tests\test_analytics_dev_app_launcher.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check

Also run path-scoped protected-surface and secret/private-marker scans over touched files.

Do not require an automated -Start smoke unless the implementation can start and terminate child processes deterministically. A -Check smoke is acceptable.

Final handoff must include:
- role performed
- source issue/tracker/umbrella issue/completed children
- source contract used
- files changed
- exact launcher scripts/functions/tests changed
- uvicorn/dependency decision
- process command contract implemented
- app-data/logging behavior
- what was verified
- what remains unverified
- whether any forbidden scope was touched
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/210"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #210"
  target_artifact: "docs/contracts/analytics_windows_developer_launcher_bootstrapper.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped protected-surface gate for docs/contracts/analytics_windows_developer_launcher_bootstrapper.md"
    - "path-scoped secret/private-marker scan for docs/contracts/analytics_windows_developer_launcher_bootstrapper.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
    - "Do not expose destructive launcher or UI actions."
```
