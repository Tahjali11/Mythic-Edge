# Match Journal Live-Browser Real App-Data Readiness Implementation Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/236>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/202>

## Contract

`docs/contracts/match_journal_live_browser_real_app_data_readiness.md`

## Internal Project Area

Local App / UI, with Generated / Local Artifacts and Quality / Governance as
supporting areas.

## Truth Owner

Parser/state remains truth owner for parser facts. Analytics remains a local
deterministic storage/view layer. Match Journal owns human annotations only.
The browser smoke is readiness evidence, not parser, analytics, workbook,
deployment, or AI truth.

## Bridge-Code Status

`stable_bridge`: browser UI -> FastAPI local app facade -> app-owned Match
Journal service/repository -> readiness evidence.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Current Behavior Compared To Contract

The current app already satisfied several automated readiness requirements:

- FastAPI exposes browser-facing Match Journal routes through `/api/journal/...`.
- Setup/status uses symbolic app-data display paths, including
  `<app_data>\db\match_journal.sqlite3`.
- Journal reads and setup/status calls do not create app-data directories or
  SQLite files.
- The first explicit backend journal write creates only the app-owned Match
  Journal database under the selected app-data root.
- Frontend tests cover cockpit rendering, safe unavailable states,
  failed-submit input preservation, and absence of pilot-error/destructive
  controls.

The implementation gap was in the live launcher path: `-AppDataRoot` controlled
launcher preflight/log folders, but the Uvicorn-created backend still resolved
its default app-data root from process environment defaults. That made the
approved disposable-root smoke unsafe, because the backend could drift toward
the user's actual local app root instead of the supplied disposable root.

The browser smoke then reached setup/status and cockpit rendering safely, but
write/persistence steps were blocked by the contract's context policy. The
empty disposable root had no visible match/game history context, and the
current browser UI does not expose an unattached-note submission path. I did
not invent parser IDs or use direct backend writes to force a browser write.

## Implementation Option Chosen

Implement the smallest launcher/backend handoff needed for the approved
disposable-root smoke:

- add a local app-data root environment bridge from the developer launcher to
  the backend child process;
- make backend default path resolution honor that bridge when `create_app(...)`
  is called by Uvicorn without explicit arguments;
- pass the resolved backend root to import helpers so local app routes stay on
  the same selected app-data root;
- add focused tests proving status and first write use the launcher-selected
  root and do not fall back to `%LOCALAPPDATA%\MythicEdgeDev`.

This keeps `-AppDataRoot` as the operator-facing interface and limits the new
environment variable to local launcher/backend process wiring.

## Files Changed

- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tools/dev_app/dev_app_launcher.py`
- `tests/test_analytics_dev_app_launcher.py`
- `tests/test_analytics_local_app_backend.py`
- `docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md`

Untracked source contract left in place:

- `docs/contracts/match_journal_live_browser_real_app_data_readiness.md`

## Code Changed

Runtime code changed only inside the contracted Local App / UI launcher/backend
surface.

- `paths.py`
  - Added `LOCAL_APP_DATA_ROOT_ENV =
    "MYTHIC_EDGE_LOCAL_APP_DATA_ROOT"`.
  - Updated `build_local_app_paths(..., env=...)` so the backend can resolve a
    launcher-supplied app-data root before falling back to `LOCALAPPDATA`.
- `backend.py`
  - Builds local app paths with the passed environment mapping.
  - Uses `resolved_app_data_root` for manual/browser import helpers, keeping
    route behavior on the same selected app-data root.
- `dev_app_launcher.py`
  - Passes `MYTHIC_EDGE_LOCAL_APP_DATA_ROOT` to the backend child process when
    `LauncherConfig.app_data_root` is available.
  - Removes that child-process env value when app-data root is unavailable, so
    stale parent values do not leak into an unavailable-root launch.

No parser behavior, parser state reconciliation, analytics schema/migrations,
analytics ingest/views, workbook schema, webhook payload shape, Apps Script,
Sheets, direct status API global CORS, OpenAI/model-provider, AI/coaching, or
production behavior changed.

## Tests Added Or Updated

- `tests/test_analytics_dev_app_launcher.py`
  - Verifies start mode passes `MYTHIC_EDGE_LOCAL_APP_DATA_ROOT` to the backend
    child process.
- `tests/test_analytics_local_app_backend.py`
  - Verifies Uvicorn-style backend default wiring uses the launcher app-data
    root for setup/status.
  - Verifies first journal write creates
    `<app_data>\db\match_journal.sqlite3` under the launcher root.
  - Verifies the `%LOCALAPPDATA%\MythicEdgeDev` fallback root is not created.

## Interface Changes

- Internal local launcher/backend bridge variable:
  `MYTHIC_EDGE_LOCAL_APP_DATA_ROOT`.
- `build_local_app_paths(...)` now accepts an optional keyword-only `env`
  mapping while preserving the existing positional `app_data_root` override.

The operator-facing command remains:

```powershell
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Start -AppDataRoot <temp_app_data_root>
```

No browser route inventory, backend payload shape, workbook schema, webhook
shape, parser interface, analytics schema, or production interface changed.

## Disposable-Root Smoke Status

Disposable root class: `disposable`.

Approved preflight command:

```powershell
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check -AppDataRoot <temp_app_data_root> -BackendPort 18765 -FrontendPort 15173 -NoOpen
```

Result:

- preflight passed;
- root did not exist after check mode;
- backend/frontend ports were accepted as loopback.

Approved live-app command:

```powershell
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Start -AppDataRoot <temp_app_data_root> -BackendPort 18765 -FrontendPort 15173 -NoOpen -LogToConsole
```

Result:

- backend `/api/health` returned `200`;
- frontend returned `200`;
- setup/status Match Journal status was `not_initialized`;
- in-app browser opened `http://127.0.0.1:15173`;
- browser title was `Mythic Edge Local Status`;
- page displayed Match Journal and Match Journal Cockpit;
- page displayed `<app_data>\db\match_journal.sqlite3`;
- no visible raw SQL, destructive controls, OpenAI/coaching/Line Tracer,
  hidden-card, player-mistake, or best-line controls were detected;
- journal write buttons were disabled because no safe visible context existed;
- context source: `blocked_no_safe_context`;
- route family used live: setup/status and app history routes only; browser
  `/api/journal/...` write was not submitted due to missing safe context;
- synthetic entry prefix used: not used because write was blocked;
- submit result: not run, contract-consistent blocker;
- refresh persistence: not run, contract-consistent blocker;
- app processes started for the smoke were stopped, with no remaining process
  on ports `18765` or `15173`.

Disposable-root generated artifact status:

- the disposable root was created under `%TEMP%`;
- top-level disposable-root folders were `config`, `db`, `diagnostics`,
  `imports`, `jobs`, and `logs`;
- no `mythic_edge.sqlite3` database was created;
- no `match_journal.sqlite3` database was created;
- no generated artifacts were created inside the repo by the smoke.

## Actual-Root Readiness Status

Actual-root readiness was not run. Actual-root write smoke was not run.

Approval state: no explicit approval was requested or granted in this Codex C
thread to inspect, write, reset, clean, delete, move, rename, archive, or
sanitize actual app-data contents.

## Failed/Unavailable Retry Status

Automated frontend tests continue to cover failed/unavailable state handling and
input preservation. A live retry check was not run because no safe live context
or safe browser-only failure trigger existed in the disposable-root app.

## Generated Artifact Status

Frontend build produced `frontend/dist` during validation. The resolved path was
verified inside the repo and then removed. Git status shows no repo build output
from this slice.

The disposable smoke root under `%TEMP%` remains as external smoke evidence and
is reported separately from repo artifacts. It was not staged or committed.

## Protected-Surface Status

No parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/
AI/coaching/production behavior was changed. No direct status API global CORS
policy was changed. No destructive import/database/job/UI action was added.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
# ## codex/analytics-foundation...origin/codex/analytics-foundation
# modified local app/launcher/test files plus untracked #236 contract

py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
# 12 passed, 1 Starlette/FastAPI testclient deprecation warning

py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
# 34 passed, 1 Starlette/FastAPI testclient deprecation warning

npm --prefix frontend test -- --run src/App.test.tsx
# 1 test file passed, 33 tests passed

npm --prefix frontend run typecheck
# passed

npm --prefix frontend run build
# passed; generated frontend/dist removed afterward

py -m ruff check src tests tools
# passed

git diff --check
# passed
```

Final governance and artifact checks:

```powershell
py tools\check_agent_docs.py
# passed, errors 0, warnings 0

@'
docs/contracts/match_journal_live_browser_real_app_data_readiness.md
docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/paths.py
tools/dev_app/dev_app_launcher.py
tests/test_analytics_dev_app_launcher.py
tests/test_analytics_local_app_backend.py
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, forbidden 0, warnings 0

@'
docs/contracts/match_journal_live_browser_real_app_data_readiness.md
docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/paths.py
tools/dev_app/dev_app_launcher.py
tests/test_analytics_dev_app_launcher.py
tests/test_analytics_local_app_backend.py
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, forbidden 0, warnings 0

git status --short --branch --untracked-files=all
# ## codex/analytics-foundation...origin/codex/analytics-foundation
# modified local app/launcher/test files plus untracked #236 contract and handoff

# Generated artifact sweep:
# frontend/dist absent
# frontend package files not dirty
# no repo SQLite artifacts found by rg --files --no-ignore for *.sqlite3 sidecars
```

## Still Unverified

- Browser journal write/persistence with a valid visible app context.
- Browser unattached-note submission, because the current UI does not expose
  that path in the empty disposable root.
- Actual-root metadata-only readiness, because no approval was requested or
  granted.
- Actual-root write smoke, because it requires separate explicit approval.
- Direct status API global CORS hardening, which remains deferred.
- Future cockpit/overlay clients.

## Reviewer Focus

Codex E should review:

- whether `MYTHIC_EDGE_LOCAL_APP_DATA_ROOT` is acceptable as a narrow
  launcher/backend bridge under this contract;
- whether the browser write blocker should route to a follow-up synthetic
  context seed/unattached-note UI issue;
- whether import helpers now correctly follow the backend-resolved app-data
  root;
- whether the disposable smoke evidence is sufficient for #236 first closure
  despite write/persistence being blocked by context policy.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #236:
Match Journal live-browser smoke and real app-data readiness.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/236

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Contract:
docs/contracts/match_journal_live_browser_real_app_data_readiness.md

Implementation handoff:
docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md

Risk tier:
High

Goal:
Review the Codex C implementation and readiness evidence against the contract.
Focus on whether the launcher/backend app-data-root handoff is narrow,
whether the disposable-root smoke stayed safe, and whether the browser write
step was correctly marked blocked_no_safe_context instead of being forced with
invented parser IDs or direct backend writes.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/review.md
- docs/templates/contract_test_report.md
- docs/contracts/match_journal_live_browser_real_app_data_readiness.md
- docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md
- tools/dev_app/dev_app_launcher.py
- tools/dev_app/start_mythic_edge_dev_app.ps1
- src/mythic_edge_parser/local_app/paths.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_dev_app_launcher.py
- tests/test_analytics_local_app_backend.py
- tests/test_match_journal_cockpit_ui_backend.py
- frontend/src/App.tsx
- frontend/src/App.test.tsx

Review expectations:
- Lead with findings, ordered by severity.
- Confirm whether `MYTHIC_EDGE_LOCAL_APP_DATA_ROOT` is an acceptable local
  launcher/backend bridge under the contract.
- Confirm setup/status and first write now use the launcher-selected app-data
  root when Uvicorn creates the backend app.
- Confirm the disposable-root browser smoke did not touch actual app-data and
  did not create repo artifacts.
- Confirm no browser write was forced when no safe visible context existed.
- Confirm no parser/runtime/analytics schema/workbook/webhook/App Script/
  Sheets/OpenAI/AI/coaching/production behavior changed.
- If findings exist, route to Codex D with exact fixes.
- If no blocking findings exist, produce
  docs/contract_test_reports/match_journal_live_browser_real_app_data_readiness.md.

Validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
npm --prefix frontend test -- --run src/App.test.tsx
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check

Run path-scoped protected-surface and secret/private-marker scans over changed
files. Remove expected frontend build output after validation if the build
creates frontend/dist, verifying the resolved path is inside the repo first.

Do not:
- target main;
- run actual-root readiness or actual-root write smoke without explicit user
  approval;
- delete, reset, wipe, rename, move, archive, clean, sanitize, copy, upload, or
  commit local app-data or private/generated artifacts;
- invent parser IDs or force a browser write with direct backend calls;
- change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/
  OpenAI/AI/coaching/production behavior;
- change direct status API global CORS policy;
- stage, commit, push, open a PR, merge, close issue #236, or mark tracker #202
  complete unless explicitly asked.

Final report must include:
- findings first;
- issue/tracker/contract/handoff reviewed;
- files reviewed;
- validation run and result;
- disposable-root smoke status;
- blocked_no_safe_context assessment;
- actual-root readiness approval state;
- generated/private artifact status;
- protected-surface status;
- whether forbidden scope was touched;
- next recommended role;
- pasteable next-role prompt if needed;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/236"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/match_journal_live_browser_real_app_data_readiness.md"
  target_artifact: "docs/contract_test_reports/match_journal_live_browser_real_app_data_readiness.md"
  implementation_handoff: "docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_match_journal_cockpit_ui_backend.py -> passed"
    - "py -m pytest -q tests\\test_analytics_dev_app_launcher.py tests\\test_analytics_local_app_backend.py tests\\test_analytics_local_app_config.py -> passed"
    - "npm --prefix frontend test -- --run src/App.test.tsx -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed afterward"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated artifact sweep -> frontend/dist absent; no repo SQLite artifacts found"
  stop_conditions:
    - "Do not target main."
    - "Do not run actual-root readiness or actual-root write smoke without explicit user approval."
    - "Do not delete, reset, wipe, rename, move, archive, clean, sanitize, copy, upload, or commit local app-data or private/generated artifacts."
    - "Do not invent parser IDs or force a browser write with direct backend calls."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not change direct status API global CORS policy."
```
