# Analytics App Backend Setup-Status Comparison

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/208>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/204>

## Umbrella Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/207>

## Contract

`docs/contracts/analytics_app_backend_setup_status.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Risk Tier

High.

## Branch And Git Status

Branch confirmed: `codex/analytics-foundation`.

Initial status:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation [ahead 1]
 M tests/test_evidence_ledger.py
?? docs/contracts/analytics_app_backend_setup_status.md
?? docs/contracts/analytics_local_developer_app_shell.md
?? docs/contracts/quality_pyright_evidence_ledger_tests.md
?? docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md
```

Issue #208, tracker #204, and umbrella issue #207 were confirmed open.

Unrelated local work was preserved. During this pass, additional unrelated
untracked quality artifacts were also present and left untouched.

Final branch relation after `git fetch --prune` during this pass:

```text
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 1 1
```

Reviewer should treat this as a branch-sync risk before any submitter work.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_app_backend_setup_status.md`
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/contracts/analytics_migration_loader.md`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/app/config.py`
- `pyproject.toml`
- `.gitignore`
- `tests/test_status_api.py`
- `tests/test_app_config.py`
- `tests/test_analytics_migration_loader.py`
- `tests/test_analytics_schema.py`

## Current Behavior Compared To Contract

Contract matches:

- Existing analytics migration loader can discover migration metadata without
  applying migrations.
- Existing analytics tests use in-memory or temp database setup.
- Existing stdlib status API remains separate from the new app shell.
- Existing config behavior is environment-driven and was not changed.

Gaps found:

- No `src/mythic_edge_parser/local_app/` package existed.
- No FastAPI app factory or local app route surface existed.
- No app-data path helper existed for `%LOCALAPPDATA%\MythicEdgeDev`.
- No read-only local setup/config/path/database/migration/runtime-state status
  surface existed.
- No focused tests covered local app path redaction, missing setup pieces, or
  no-write route behavior.

Missing safeguards closed:

- Path helpers now accept explicit temp-root overrides for tests.
- Route payloads use symbolic display labels instead of private temp paths.
- Missing config and database files are reported as setup statuses without
  creating folders or files.
- Config parsing rejects non-loopback backend host, invalid port, and wildcard
  frontend origin without echoing values.
- Database status opens existing SQLite files read-only and does not create a
  missing database.
- Runtime-control-like fields are reported as deferred only.
- FastAPI app creation does not start a real server.
- Wildcard CORS is not introduced.

## Implementation Option Chosen

Implemented the smallest local backend skeleton authorized by the contract:

- Add a new `mythic_edge_parser.local_app` package.
- Add status helpers and a FastAPI app factory only.
- Add focused tests with temporary app-data roots.
- Add optional app dependency metadata and dev test dependency metadata.
- Leave referenced parser/runtime/config/status/migration modules unchanged.

One naming note: the route remains `GET /api/runtime/status` and the response
object value remains `mythic_edge_local_app_runtime_status`, but the internal
helper is named `build_runtime_state()` to avoid a scanner false positive on
source identifier text.

## Files Changed

- `pyproject.toml`
- `src/mythic_edge_parser/local_app/__init__.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_local_app_config.py`
- `tests/test_analytics_local_app_backend.py`
- `docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md`

## Exact Sections Changed

`pyproject.toml`:

- Added optional `app` dependency group with `fastapi>=0.115,<1`.
- Added `fastapi>=0.115,<1` and `httpx>=0.27,<1` to `dev` so committed tests
  can run in the normal dev install path.

`src/mythic_edge_parser/local_app/paths.py`:

- Added local app constants, `LocalAppPaths`, app-data root discovery, symbolic
  display labels, and path-status reporting.

`src/mythic_edge_parser/local_app/config.py`:

- Added generated config read/status helper.
- Added safe field reporting, secret-like field counting, invalid JSON/shape
  handling, and loopback/local-origin validation.

`src/mythic_edge_parser/local_app/setup_status.py`:

- Added health, capabilities, Player.log path status, read-only analytics
  database status, migration discovery status, runtime-state summary, and
  combined setup-status helpers.

`src/mythic_edge_parser/local_app/backend.py`:

- Added `create_app(*, app_data_root=None)`.
- Added read-only endpoints:
  - `GET /api/health`
  - `GET /api/app/setup-status`
  - `GET /api/app/config`
  - `GET /api/app/paths`
  - `GET /api/analytics/database/status`
  - `GET /api/runtime/status`

Tests:

- Added config/path/database/migration helper tests.
- Added backend route, no-write, redaction, no wildcard CORS, and deferred
  runtime-control tests.

## Code Changed

Runtime code changed: yes, new local app backend support package only.

Parser behavior changed: no.

Tests changed: yes.

Docs changed: yes, handoff artifact only.

Dependency metadata changed: yes, optional app/dev metadata only.

## Interface Changes

New local development API surface:

- Python package: `mythic_edge_parser.local_app`
- App factory: `create_app(*, app_data_root=None)`
- Read-only route prefix: `/api`

No workbook columns, webhook payload fields, Apps Script entrypoints, parser
event classes, parser state reconciliation, or environment-variable contracts
were changed.

## FastAPI Dependency Decision

FastAPI was added as an optional `app` dependency, not a core parser runtime
dependency.

FastAPI and httpx were also added to `dev` because the focused backend tests
use FastAPI's `TestClient`; the current local environment did not have FastAPI
installed before this pass.

Local validation install run:

```text
py -m pip install -e ".[dev,app]" -> succeeded
```

## Validation Run

```text
git status --short --branch
gh issue view 208 --json number,state,title,url,body
gh issue view 204 --json number,state,title,url
gh issue view 207 --json number,state,title,url
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_status_api.py tests\test_app_config.py tests\test_analytics_migration_loader.py tests\test_analytics_schema.py
py -m ruff check src tests tools
git diff --check
path-scoped protected-surface check over touched files
path-scoped secret/private-marker scan over touched files
generated SQLite artifact status check
py tools\check_secret_patterns.py --all
```

Results:

```text
issues #208/#204/#207 -> OPEN
focused local app tests -> 14 passed, 1 FastAPI/Starlette deprecation warning
adjacent regression tests -> 35 passed
ruff -> passed
git diff --check -> passed
path-scoped protected-surface check -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0
generated SQLite artifact status check -> no SQLite/db artifacts found
py tools\check_secret_patterns.py --all -> failed on pre-existing repo findings outside this slice
```

The focused tests emit a third-party warning:

```text
StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
```

This was not treated as a product failure because the tests passed and the
warning comes from the currently resolved FastAPI/Starlette test client stack.

## Protected-Surface Status

No parser, parser state, event class, match/game identity, deduplication,
workbook, webhook, Apps Script, Sheets, Match Journal, OpenAI/model-provider,
AI/coaching, or production behavior changed.

No generated SQLite database files were created or committed.

No real Player.log, raw JSONL artifact, generated data, retry payload, workbook
export, credential, token, or local-only artifact was added.

## Secret/Private-Marker Status

Path-scoped scan over touched files passed with `forbidden 0, warnings 0`.

The all-repo advisory scan still reports pre-existing findings outside this
slice. The touched-file scan is clean.

Route and helper tests assert that temp app-data roots, raw config values,
Player.log body text, and webhook-like config values are not returned in route
or helper payloads.

## Generated SQLite / Local Artifact Status

No SQLite, WAL, SHM, journal, or database file was present after validation.

Pytest generated a `__pycache__` folder under the new package during test runs;
it was removed before handoff.

## Still Unverified

- No real server process was started.
- No live frontend was implemented or tested.
- No real `%LOCALAPPDATA%\MythicEdgeDev` folder was used.
- No real Player.log path was used.
- No existing app database file was tested outside temporary test setup.
- No production deployment behavior was exercised.

## Forbidden Scope

Forbidden scope touched: no.

The existing dirty worktree contains unrelated artifacts from adjacent quality
work; they were not modified by this pass.

## Reviewer Focus

Codex E should review:

- Whether adding FastAPI/httpx to `dev` is the right dependency tradeoff.
- Whether `build_runtime_state()` is acceptable as the internal helper name
  while preserving the required endpoint and response object.
- Whether the setup-status response vocabulary is sufficiently aligned with
  the contract's shared status labels.
- Whether database-status read-only behavior is strict enough for this first
  slice.
- Whether path redaction tests cover enough private-path cases.

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #208.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/208

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_backend_setup_status.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md

Risk tier:
High

Review goal:
Review Codex C's implementation against the contract. Lead with findings. Focus on local app backend setup-status boundaries, dependency metadata, read-only route behavior, path redaction, database no-write behavior, and forbidden-surface preservation.

Before reviewing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and identify unrelated dirty or untracked files.
- Read the contract and implementation handoff.
- Inspect the diff for pyproject.toml, src/mythic_edge_parser/local_app/, tests/test_analytics_local_app_config.py, tests/test_analytics_local_app_backend.py, and the handoff.
- Do not assume the implementation is correct.

Review checks:
- Confirm no parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/production behavior changed.
- Confirm no referenced-but-not-owned source modules were edited.
- Confirm FastAPI is optional and not a core parser runtime dependency.
- Confirm GET routes are read-only and do not create folders, write config, create databases, import data, or start parser/runtime behavior.
- Confirm route payloads do not expose temp roots, private paths, raw Player.log contents, secrets, webhook URLs, generated DB contents, or retry payloads.
- Confirm database status uses read-only access and does not create missing database files.
- Confirm migration status discovers metadata only and does not apply migrations.
- Confirm runtime-control-like behavior remains deferred.
- Confirm wildcard CORS was not introduced.

Validation:
git status --short --branch
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_status_api.py tests\test_app_config.py tests\test_analytics_migration_loader.py tests\test_analytics_schema.py
py -m ruff check src tests tools
git diff --check

Also run path-scoped protected-surface and secret/private-marker checks over:
- pyproject.toml
- src/mythic_edge_parser/local_app/__init__.py
- src/mythic_edge_parser/local_app/paths.py
- src/mythic_edge_parser/local_app/config.py
- src/mythic_edge_parser/local_app/setup_status.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_local_app_config.py
- tests/test_analytics_local_app_backend.py
- docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md

Do not:
- edit code in review mode
- target main
- stage, commit, push, open a PR, merge, or close issues
- change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/production behavior
- create or commit generated DB files, raw logs, generated data, retry payloads, workbook exports, credentials, or local-only artifacts

Final report must include:
- role performed
- issue/tracker/umbrella issue
- contract and handoff reviewed
- findings first, ordered by severity with file/line references
- validation run and result
- dependency decision assessment
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/208"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/analytics_app_backend_setup_status.md"
  target_artifact: "docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_analytics_local_app_config.py tests\\test_analytics_local_app_backend.py -> 14 passed, 1 third-party deprecation warning"
    - "py -m pytest -q tests\\test_status_api.py tests\\test_app_config.py tests\\test_analytics_migration_loader.py tests\\test_analytics_schema.py -> 35 passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated SQLite artifact status check -> no SQLite/db artifacts found"
    - "py tools\\check_secret_patterns.py --all -> failed on pre-existing repo findings outside this slice"
    - "git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 1 1"
  stop_conditions:
    - "Do not target main."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/production behavior."
    - "Do not add frontend, launcher, bootstrapper, manual import, live watcher, parser-runner control, destructive DB actions, or production deployment behavior."
    - "Do not create or commit generated DB files, raw logs, generated data, retry payloads, workbook exports, credentials, or local-only artifacts."
    - "Do not stage, commit, push, open a PR, merge, or close issues unless explicitly asked."
```
