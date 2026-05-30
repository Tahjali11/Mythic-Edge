# Analytics Windows Developer Launcher Bootstrapper Comparison

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/210>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/204>

## Umbrella Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/207>

## Completed Children

- Backend setup/status: <https://github.com/Tahjali11/Mythic-Edge/issues/208>
- Frontend setup/status page: <https://github.com/Tahjali11/Mythic-Edge/issues/209>

## Contract

`docs/contracts/analytics_windows_developer_launcher_bootstrapper.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Risk Tier

High.

## Branch And Git Status

Branch confirmed: `codex/analytics-foundation`.

Initial status:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
?? docs/contracts/analytics_windows_developer_launcher_bootstrapper.md
```

Remote relation:

```text
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0
```

Issue state checked with GitHub CLI:

- #210: OPEN
- #204: OPEN
- #207: OPEN

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_windows_developer_launcher_bootstrapper.md`
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_app_backend_setup_status.md`
- `docs/contracts/analytics_react_vite_setup_status_page.md`
- `docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md`
- `docs/contract_test_reports/analytics_react_vite_setup_status_page.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `frontend/package.json`
- `frontend/vite.config.ts`
- `pyproject.toml`
- `.gitignore`
- `tools/auto_launcher/`

## Current Behavior Compared To Contract

Contract matches before implementation:

- The backend setup/status package exists.
- The frontend setup/status package exists under `frontend/`.
- `frontend/package.json` has the required Vite scripts.
- `.gitignore` already excludes frontend generated artifacts.
- Legacy `tools/auto_launcher/` exists and remains reference-only.

Contract gaps closed:

- Added reviewed `tools/dev_app/` launcher surface.
- Added dry-run `check` mode.
- Added explicit `start` mode with approved backend/frontend child commands.
- Added app-data folder and launcher-log creation only in `start` mode.
- Added process-local frontend backend-origin override.
- Added cleanup constrained to children started by the current launcher call.
- Added focused launcher tests.
- Added optional `uvicorn` metadata to app/dev dependency groups.
- Added thin PowerShell wrapper.

## Implementation Option Chosen

Implemented the existing-checkout developer launcher/preflight workflow only.

Deferred, per contract:

- clone/update behavior
- shortcut creation
- installer behavior
- config writes
- database initialization
- manual import
- live watcher controls
- parser runner controls
- production or deployment behavior

## Files Changed

- `pyproject.toml`
- `tools/dev_app/dev_app_launcher.py`
- `tools/dev_app/start_mythic_edge_dev_app.ps1`
- `tests/test_analytics_dev_app_launcher.py`
- `docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md`

Existing untracked source contract left in place:

- `docs/contracts/analytics_windows_developer_launcher_bootstrapper.md`

## Exact Sections Changed

`pyproject.toml`:

- Added `uvicorn>=0.30,<1` to optional `app`.
- Added `uvicorn>=0.30,<1` to `dev` so committed launcher/backend checks can
  validate the server-runner dependency.

`tools/dev_app/dev_app_launcher.py`:

- Added repo-root discovery and required marker checks.
- Added app-data root discovery and dry-run folder status reporting.
- Added tool/module preflight checks for Windows, Python, package imports,
  Node.js, npm, Git, frontend package, and frontend lockfile.
- Added loopback host and port option validation.
- Added `start_dev_app(...)` orchestration for backend and frontend children.
- Added app-data subfolder and launcher-log creation only in `start` mode.
- Added backend command construction for `uvicorn`.
- Added frontend command construction with process-local
  `VITE_MYTHIC_EDGE_API_BASE_URL`.
- Added child cleanup limited to the supplied launcher-owned child list.
- Added redacted status/log formatting.

`tools/dev_app/start_mythic_edge_dev_app.ps1`:

- Added thin Windows wrapper for `-Check`, `-Start`, `-NoOpen`,
  `-LogToConsole`, `-BackendPort`, `-FrontendPort`, and `-AppDataRoot`.

`tests/test_analytics_dev_app_launcher.py`:

- Added dry-run no-write coverage.
- Added start-mode app-data/log creation coverage.
- Added backend/frontend command and process-local environment coverage.
- Added port-conflict no-launch coverage.
- Added child cleanup boundary coverage.
- Added redacted launcher-log coverage.
- Added PowerShell wrapper scope coverage.
- Added immediate child-exit cleanup coverage.

## Code Changed

Runtime code changed: yes, launcher-only under `tools/dev_app/`.

Tests changed: yes.

Docs changed: yes, this handoff.

Dependency metadata changed: yes, optional `uvicorn` only.

Backend behavior changed: no.

Frontend behavior changed: no.

Parser behavior changed: no.

## Interface Changes

New Python CLI:

```powershell
py tools\dev_app\dev_app_launcher.py check
py tools\dev_app\dev_app_launcher.py start
```

New PowerShell wrapper:

```powershell
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Start
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Start -NoOpen
```

Supported local options:

- `--backend-port` / `-BackendPort`
- `--frontend-port` / `-FrontendPort`
- `--app-data-root` / `-AppDataRoot`
- `--no-open` / `-NoOpen`
- `--log-to-console` / `-LogToConsole`

No backend route shape, frontend API shape, parser output field, workbook
column, webhook field, Apps Script entrypoint, repo update command, or
production interface changed.

## Uvicorn Dependency Decision

`uvicorn` was added only to optional `app` and `dev` dependency groups because
the approved backend child command is:

```powershell
py -m uvicorn mythic_edge_parser.local_app.backend:create_app --factory --host 127.0.0.1 --port 8765
```

`uvicorn` was installed locally through:

```powershell
py -m pip install -e ".[dev,app]"
```

Recorded local version:

```text
uvicorn -> 0.48.0
```

It did not become a core parser runtime dependency.

## Process Command Contract Implemented

Backend command:

```powershell
py -m uvicorn mythic_edge_parser.local_app.backend:create_app --factory --host 127.0.0.1 --port 8765
```

Frontend command:

```powershell
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173
```

Frontend process-local environment:

```text
VITE_MYTHIC_EDGE_API_BASE_URL=http://127.0.0.1:8765
```

The launcher does not write `.env` files.

## App-Data And Logging Behavior

`check` mode:

- does not create folders
- does not create logs
- does not start processes
- does not open a browser

`start` mode:

- may create app-data subfolders
- may create launcher logs under the app-data launcher-log folder
- may start only the backend and frontend child processes
- may open the browser unless disabled
- cleans up only child processes it started

Launcher-managed logs:

- `launcher.log`
- `backend.log`
- `frontend.log`

Status/log formatting redacts repo and app-data root values before writing
launcher-managed status lines.

## Validation Run

```text
git status --short --branch -> codex/analytics-foundation, changed #210 contract/package/launcher/test/handoff files
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0
GitHub CLI issue checks -> #210/#204/#207 open
py -m pip install -e ".[dev,app]" -> passed, installed uvicorn 0.48.0
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check -> passed, redacted dry-run output
py -m pytest -q tests\test_analytics_dev_app_launcher.py -> 8 passed
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py -> 18 passed, 1 third-party warning
npm --prefix frontend ci -> passed, 113 packages, 0 vulnerabilities
npm --prefix frontend run typecheck -> passed
npm --prefix frontend run test -- --run -> passed, 3 files, 12 tests
npm --prefix frontend run build -> passed
py -m ruff check src tests tools -> passed
git diff --check -> passed
path-scoped protected-surface check -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0
```

Generated build/cache cleanup after validation:

- removed `frontend/dist/`
- removed `tools/dev_app/__pycache__/`
- removed `tests/__pycache__/`

## Protected-Surface Status

No parser behavior, parser state final reconciliation, backend route payload
shape, frontend setup/status behavior, workbook schema, webhook payload shape,
Apps Script behavior, Google Sheets behavior, Match Journal behavior,
OpenAI/model-provider behavior, AI/coaching behavior, production behavior, or
deployment behavior changed.

## Secret/Private-Marker Status

Path-scoped secret/private-marker validation passed with `forbidden 0,
warnings 0`.

The implementation uses synthetic temp roots in tests and does not add secrets,
credentials, raw logs, local JSONL artifacts, generated DB contents, webhook
URLs, API keys, tokens, or OAuth state.

## Generated Artifact Status

Generated local artifacts were not committed.

Current expected ignored local artifact:

- `frontend/node_modules/`

Removed after validation:

- `frontend/dist/`
- Python `__pycache__` folders from this pass

No SQLite database, WAL, SHM, journal, raw log, local JSONL artifact, runtime
output, retry payload, workbook export, or generated card/tier data was added.

## Forbidden Scope

Forbidden scope touched: no.

No destructive launcher or UI actions were exposed.

No parser/runtime/workbook/webhook/App Script/Sheets/Match
Journal/OpenAI/AI/coaching/production behavior changed.

## Still Unverified

- Real `-Start` smoke with live backend and frontend processes.
- Browser-open success in a real launcher session.
- Future clone/update/bootstrapper behavior, which is out of scope.
- Future database initialization/setup actions, which are out of scope.
- Production behavior, which is out of scope.

## Reviewer Focus

Codex E should review:

- Whether `uvicorn` dependency metadata is correctly optional.
- Whether dry-run `check` is truly side-effect free.
- Whether `start` writes only approved app-data folders/logs.
- Whether process command construction exactly matches the contract.
- Whether process-local frontend environment is safe and non-persistent.
- Whether cleanup is limited to launcher-owned child processes.
- Whether the wrapper is thin enough and contains no hidden destructive actions.

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #210.

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

Implementation handoff:
docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md

Risk tier:
High

Review goal:
Review Codex C's Windows existing-checkout developer launcher/preflight implementation against the contract. Lead with findings. Confirm check mode is dry-run, start mode is narrowly scoped, cleanup only touches launcher-owned child processes, and no parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior changed.

Before reviewing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and identify unrelated dirty or untracked files.
- Confirm issue #210, tracker #204, and umbrella issue #207 are open if GitHub CLI is available.
- Read the contract and implementation handoff.
- Inspect pyproject.toml, tools/dev_app/dev_app_launcher.py, tools/dev_app/start_mythic_edge_dev_app.ps1, tests/test_analytics_dev_app_launcher.py, and the handoff.
- Treat tools/auto_launcher/ as reference-only and do not require parity with it.

Review checks:
- Confirm uvicorn is optional app/dev dependency metadata only.
- Confirm no backend route, frontend setup/status, parser, workbook, webhook, Apps Script, Sheets, Match Journal, OpenAI/AI/coaching, production, or deployment behavior changed.
- Confirm check mode performs no filesystem writes, child-process starts, browser opens, or network starts.
- Confirm start mode may create only approved app-data subfolders and launcher logs.
- Confirm backend and frontend child commands use loopback hosts and configured ports.
- Confirm frontend receives process-local VITE_MYTHIC_EDGE_API_BASE_URL and no .env files are written.
- Confirm missing prerequisites and port conflicts do not start processes or kill existing processes.
- Confirm cleanup terminates only child processes supplied by the launcher-owned child list.
- Confirm console/log status uses safe redacted path labels and no private values.
- Confirm the PowerShell wrapper is thin and has no destructive hidden behavior.

Validation:
py -m pytest -q tests\test_analytics_dev_app_launcher.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check

Also run path-scoped protected-surface and secret/private-marker checks over:
- pyproject.toml
- docs/contracts/analytics_windows_developer_launcher_bootstrapper.md
- docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md
- tools/dev_app/dev_app_launcher.py
- tools/dev_app/start_mythic_edge_dev_app.ps1
- tests/test_analytics_dev_app_launcher.py

Optional smoke:
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check

Do not:
- edit code in review mode
- run -Start unless you can guarantee cleanup
- target main
- change backend behavior, frontend behavior, parser behavior, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, Match Journal behavior, AI behavior, production behavior, secrets, raw logs, generated data, local JSONL artifacts, generated database artifacts, or deployment behavior
- expose destructive launcher or UI actions
- stage, commit, push, open a PR, merge, or close issues

Final report must include:
- role performed
- issue/tracker/umbrella issue/completed children
- contract and handoff reviewed
- findings first, ordered by severity with file/line references
- validation run and result
- uvicorn/dependency assessment
- dry-run and start-mode side-effect assessment
- process cleanup assessment
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/210"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/analytics_windows_developer_launcher_bootstrapper.md"
  target_artifact: "docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pip install -e \".[dev,app]\" -> passed, installed uvicorn 0.48.0"
    - ".\\tools\\dev_app\\start_mythic_edge_dev_app.ps1 -Check -> passed"
    - "py -m pytest -q tests\\test_analytics_dev_app_launcher.py -> 8 passed"
    - "py -m pytest -q tests\\test_analytics_local_app_config.py tests\\test_analytics_local_app_backend.py -> 18 passed, 1 third-party warning"
    - "npm --prefix frontend ci -> passed, 113 packages, 0 vulnerabilities"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> passed, 3 files, 12 tests"
    - "npm --prefix frontend run build -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not target main."
    - "Do not change backend/frontend/parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
    - "Do not expose destructive launcher or UI actions."
    - "Do not stage, commit, push, open a PR, merge, or close issues unless explicitly asked."
```
