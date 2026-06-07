# Analytics App Backend Setup-Status Contract

## Module

Local app backend config and setup-status skeleton.

This contract defines the first implementation slice under the local developer
app shell umbrella: a loopback-only FastAPI backend that can report local app
setup status, app-data path status, config status, analytics database status,
migration availability, Player.log path status, and deferred runtime status.

It does not define the frontend, bootstrapper, developer launcher, manual JSONL
import routes, live Player.log watcher routes, parser runner control, analytics
query pages, destructive local actions, Google Sheets sync, Match Journal,
OpenAI/model-provider runtime behavior, AI coaching, production behavior, or
deployment behavior.

Plain English: build the dashboard lights before wiring the controls. This
slice may say "here is what exists and what is missing"; it must not start
driving the parser or changing local data.

## Source Issue

- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/208>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Umbrella contract: `docs/contracts/analytics_local_developer_app_shell.md`

## Branch

Current intended branch:

```text
codex/analytics-foundation
```

Observed during this Codex B pass:

```text
8dfc7b7394e55120c5026aeef87d77a650c551f9
```

Local branch state:

- one commit ahead of `origin/codex/analytics-foundation`
- untracked local docs already present before this contract:
  - `docs/contracts/analytics_local_developer_app_shell.md`
  - `docs/contracts/quality_pyright_evidence_ledger_tests.md`

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
- source issue #208
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/contracts/analytics_migration_loader.md`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `pyproject.toml`
- `.gitignore`
- `tests/test_status_api.py`
- `tests/test_app_config.py`
- `tests/test_analytics_migration_loader.py`
- `tests/test_analytics_schema.py`

## Risk Tier

High.

Reasons:

- introduces a new local API route surface
- introduces a FastAPI dependency and package boundary
- introduces local app path/config semantics under a private generated folder
- may expose private paths if response shapes are loose
- may accidentally create repo-local generated files if defaults are wrong
- may accidentally start parser/runtime behavior if the route boundary is too
  broad
- can blur setup status, parser truth, analytics storage, deployment readiness,
  and UI control surfaces

## Owning Layer

Primary owner: local analytics usability / developer app backend.

Truth boundaries:

- Parser/state owns MTGA event interpretation, match/game identity, final
  reconciliation, parser event classes, and parser-managed facts.
- The Player.log evidence ledger owns provenance, confidence, finality, drift,
  degradation, invariant, and review vocabulary.
- Analytics ingest owns copying parser-normalized facts into SQLite.
- SQLite owns local queryable storage and deterministic views, not parser
  truth.
- The local app backend owns local setup/status orchestration and safe display
  API responses only.
- The future frontend, launcher, and bootstrapper are downstream access
  surfaces and are out of scope for this slice.

The backend must not become parser truth, analytics truth, evidence truth,
workbook truth, AI truth, gameplay advice, hidden-card inference, archetype
classification, player-mistake truth, merge readiness, deploy readiness, or
production authority.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_app_backend_setup_status.md`

Future Codex C implementation files authorized by this contract:

- `src/mythic_edge_parser/local_app/__init__.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_local_app_config.py`
- `tests/test_analytics_local_app_backend.py`
- `docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md`

Conditional implementation file:

- `pyproject.toml`, only to add the optional local app dependencies required
  for this backend skeleton and its tests.

Referenced but not owned:

- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- analytics schema/migration SQL
- existing status/config/analytics tests

Codex C must route back to Codex B before editing referenced-but-not-owned
source modules.

## Observed Current Behavior

Repo state:

- No reviewed FastAPI backend exists.
- No React/Vite frontend exists.
- No local app package exists under `src/mythic_edge_parser/local_app/`.
- `pyproject.toml` has runtime dependencies `beautifulsoup4` and `requests`;
  it has no FastAPI dependency and no `app` optional dependency group.
- `pyproject.toml` has a `dev` optional dependency group used by local and CI
  validation.
- `.gitignore` ignores repo-local generated data roots such as
  `data/analytics/`, `data/status/`, runtime logs, failed posts, bad events,
  oracle data, tier sources, and local review artifacts.
- The intended local app generated root is outside the repo:
  `%LOCALAPPDATA%\MythicEdgeDev\`.

Adjacent runtime/status behavior:

- `src/mythic_edge_parser/app/status_api.py` exposes a small stdlib HTTP status
  API with routes such as `/health`, `/status`, `/match-history`, and
  `/actions`.
- `status_api.py` is a reference surface, not the new reviewed FastAPI app
  shell.
- `status_api.py` currently sends wildcard CORS (`Access-Control-Allow-Origin:
  *`). The new FastAPI backend must not copy that default.
- `src/mythic_edge_parser/app/config.py` is environment-driven and currently
  defaults generated parser/runtime outputs into repo `data/` paths.
- `config.py` contains a Windows default `Player.log` path. The local app must
  not expose full private local paths by default.
- `src/mythic_edge_parser/app/runtime_surfaces.py` reads and writes parser
  runtime surface artifacts under existing repo-configured paths. This first
  backend slice must not invoke runtime-surface writes.

Adjacent analytics behavior:

- `src/mythic_edge_parser/app/analytics_migration_loader.py` can discover,
  checksum, load, and apply source-controlled SQL migrations to a
  caller-supplied SQLite connection.
- `apply_analytics_migrations(...)` writes to the supplied SQLite connection.
  It must not be called against the app database by read-only setup-status
  routes in this slice.
- Existing analytics migration/schema tests use in-memory SQLite databases.
- Existing analytics code does not require creating
  `%LOCALAPPDATA%\MythicEdgeDev\`.

## Contract Decisions

### Package Boundary

The first local app backend package should live under:

```text
src/mythic_edge_parser/local_app/
```

Reason: `src/mythic_edge_parser/app/` is already the parser application layer.
Keeping the local web app under `local_app` avoids blending parser runtime
modules with developer UI/API orchestration modules.

### Dependency Strategy

FastAPI must not become a core parser runtime dependency in this slice.

Codex C may add a new optional dependency group:

```toml
[project.optional-dependencies]
app = [
  "fastapi>=0.115,<1",
]
```

If focused backend tests require FastAPI's test client dependencies, Codex C
may add the smallest required test dependency to `dev`, for example `httpx`,
with an explanation in the handoff.

Because current repo checks normally install `.[dev]`, the `dev` group must
remain sufficient to run all committed tests after the new backend tests are
added. Codex C may duplicate the FastAPI dependency in `dev` if that is the
simplest reliable approach.

Deferred dependency work:

- no `uvicorn` in this slice unless Codex C proves it is required for tests;
  starting a real server is not required here
- no frontend dependencies
- no Node.js, npm, package files, package lockfiles, or Vite
- no global tool requirement

### Read-Only First Slice

All first-slice endpoints must be read-only.

The first slice must not:

- create app-data folders from a GET route
- write `app_config.json`
- create or migrate the app SQLite database
- import JSONL
- start a parser runner
- start or stop a live watcher
- start the legacy status API
- delete, reset, wipe, or overwrite anything

Future explicit setup, config-write, import, database-initialize, launcher, or
watcher actions require separate child issues/contracts.

## App Data Root And Path Contract

Default app data root:

```text
%LOCALAPPDATA%\MythicEdgeDev\
```

Required app-data subfolders:

- `config\`
- `db\`
- `logs\`
- `imports\`
- `jobs\`
- `diagnostics\`

Required generated config path:

```text
%LOCALAPPDATA%\MythicEdgeDev\config\app_config.json
```

Required default local app database path:

```text
%LOCALAPPDATA%\MythicEdgeDev\db\mythic_edge.sqlite3
```

Implementation requirements:

- Path helper functions must accept an explicit app-data root override for
  tests.
- Tests must use temporary directories, not real `%LOCALAPPDATA%`.
- No environment-variable contract is authorized in this slice.
- No folder creation is allowed at import time.
- GET routes must not create folders.
- Path status must use display labels such as `<app_data>\config` or
  `%LOCALAPPDATA%\MythicEdgeDev\config`, not full private user paths.
- The backend must not default generated app files into the repo.

If `%LOCALAPPDATA%` is unavailable and no explicit test/root override is
provided, the backend should report app-data status as unavailable rather than
falling back into the repo.

## Generated Config Contract

The first slice may read a generated local config file if it exists under the
app-data config folder.

Allowed config path:

```text
<app_data>\config\app_config.json
```

Allowed config fields for read-only status:

- `player_log_path`
- `analytics_database_path`
- `backend_host`
- `backend_port`
- `frontend_origin`

The first slice must not write this file.

Config status values:

- `missing`
- `present`
- `invalid_json`
- `invalid_shape`
- `unreadable`

Required privacy behavior:

- Do not echo raw config file content.
- Do not return secrets, webhook URLs, API keys, tokens, or credentials if they
  appear unexpectedly in config.
- Do not return full private paths by default.
- Report path fields as booleans plus redacted/display labels.
- Malformed JSON errors must not include the raw config body.

## Player.log Path Status Contract

The first backend slice may report Player.log status, but it must not read raw
Player.log contents.

Allowed evidence:

- configured path exists or does not exist
- configured path is a file or is not a file
- likely default MTGA Player.log candidate exists or does not exist
- config is missing or invalid

Forbidden evidence:

- raw Player.log lines
- file snippets
- event counts
- parser interpretation
- live tailing
- file hashing
- copying Player.log into app-data

Required status labels:

- `configured_exists`
- `configured_missing`
- `detected_exists`
- `missing`
- `invalid_config`
- `unavailable`

Required display behavior:

- Return safe labels such as `<configured_player_log>`,
  `<detected_mtga_player_log>`, or symbolic Windows paths.
- Do not return `C:\Users\<name>\...` style private paths in default route
  payloads.

## Analytics Database Status Contract

The first backend slice may report analytics database status for the local app
database path.

It must not create, migrate, reset, delete, compact, vacuum, import into, or
write to the database.

Required status labels:

- `missing`
- `present`
- `unreadable`
- `invalid_sqlite`
- `schema_unknown`
- `schema_current`
- `schema_outdated`
- `migration_error`

Allowed behavior:

- If the database file is missing, report `missing`.
- If the database file exists, open it read-only if possible.
- If opened read-only, inspect only schema metadata such as
  `schema_migrations`.
- Compare recorded migration IDs/checksums against
  `iter_analytics_migrations()` when safe.
- Report the local app database path as a display label only.

Forbidden behavior:

- no `apply_analytics_migrations(...)` call against the app database
- no implicit `sqlite3.connect(path)` that creates a missing database
- no generated SQLite database, WAL, SHM, or journal files in the repo
- no broad SQL browser endpoint
- no analytics fact reads beyond schema/status metadata in this slice

## Migration Loader Status Contract

The backend may report whether source-controlled analytics migrations are
available.

Allowed behavior:

- call `iter_analytics_migrations()`
- report migration IDs, filenames, schema version after, and checksum presence
- report migration loader errors as safe error codes/messages

Forbidden behavior:

- do not apply migrations from a GET route
- do not expose full local package paths
- do not write migration status artifacts
- do not modify migration SQL

Migration status labels:

- `available`
- `missing`
- `error`

## Runtime Status Contract

The first backend slice may expose a local-app runtime status endpoint, but it
must be explicitly non-controlling.

Required first-slice behavior:

- report the FastAPI backend as running because the request reached it
- report parser runner control as `deferred`
- report live watcher status as `deferred`
- report manual import status as `deferred`
- report legacy `status_api.py` as `separate_reference_surface`

Forbidden first-slice behavior:

- do not start or stop `runner.py`
- do not start or stop `status_api.py`
- do not tail Player.log
- do not read or write runtime status files
- do not call `runtime_surfaces.bootstrap_runtime_surfaces()`
- do not call runtime-surface write helpers

Future runtime-artifact reading or live watcher status requires a later
contract.

## Backend Public Interface

Recommended module surfaces:

```text
mythic_edge_parser.local_app.paths
mythic_edge_parser.local_app.config
mythic_edge_parser.local_app.setup_status
mythic_edge_parser.local_app.backend
```

Required constants:

```text
LOCAL_APP_SCHEMA_VERSION = "analytics_app_backend_setup_status.v1"
LOCAL_APP_OBJECT_PREFIX = "mythic_edge_local_app"
LOCAL_APP_DIR_NAME = "MythicEdgeDev"
REQUIRED_APP_SUBDIRS = ("config", "db", "logs", "imports", "jobs", "diagnostics")
DEFAULT_ANALYTICS_DB_FILENAME = "mythic_edge.sqlite3"
DEFAULT_BACKEND_HOST = "127.0.0.1"
```

Recommended public data shapes may be dataclasses, typed dictionaries, or
documented dictionaries:

```text
LocalAppPaths
PathStatus
LocalAppConfigStatus
PlayerLogPathStatus
AnalyticsDatabaseStatus
MigrationLoaderStatus
RuntimeStatus
SetupStatus
```

Recommended public functions:

```python
build_local_app_paths(app_data_root: Path | None = None) -> LocalAppPaths
build_path_status(paths: LocalAppPaths) -> dict[str, object]
load_local_app_config_status(paths: LocalAppPaths) -> dict[str, object]
build_player_log_path_status(paths: LocalAppPaths) -> dict[str, object]
build_analytics_database_status(paths: LocalAppPaths) -> dict[str, object]
build_migration_loader_status() -> dict[str, object]
build_runtime_status() -> dict[str, object]
build_setup_status(paths: LocalAppPaths) -> dict[str, object]
create_app(*, app_data_root: Path | None = None) -> FastAPI
```

Names may differ if Codex C records why, but the semantic surfaces must remain
available and focused.

Import side effects:

- importing these modules must not create files or folders
- importing these modules must not start servers
- importing these modules must not read raw Player.log
- importing these modules must not open SQLite databases unless an explicit
  status function is called

## Endpoint Contract

All first-slice endpoints are `GET` endpoints.

Required route prefix:

```text
/api
```

Required endpoint inventory:

```text
GET /api/health
GET /api/app/setup-status
GET /api/app/config
GET /api/app/paths
GET /api/analytics/database/status
GET /api/runtime/status
```

No `POST`, `PUT`, `PATCH`, or `DELETE` endpoints are authorized in this slice.

### Shared Response Requirements

Every response must include:

- `object`
- `schema_version`
- `status`

Allowed top-level status labels:

- `ok`
- `degraded`
- `missing`
- `unavailable`
- `error`

All responses must be JSON serializable and deterministic enough for focused
tests.

Responses must not include:

- raw Player.log contents
- raw JSONL artifacts
- secrets
- webhook URLs
- API keys
- tokens
- OAuth state
- full private user paths by default
- generated SQLite file content
- runtime status file content
- failed-post payloads

### `GET /api/health`

Purpose: prove the backend app is importable and request handling works.

Required response fields:

- `object = "mythic_edge_local_app_health"`
- `schema_version = "analytics_app_backend_setup_status.v1"`
- `status = "ok"`
- `mode = "setup_status_only"`
- `capabilities`

Required first-slice capabilities:

```text
setup_status: enabled
config_write: disabled
database_init: disabled
manual_import: disabled
live_watcher: disabled
parser_runner_control: disabled
frontend: deferred
```

### `GET /api/app/setup-status`

Purpose: provide one combined setup-status summary for future UI display.

Required sections:

- `paths`
- `config`
- `player_log`
- `analytics_database`
- `migrations`
- `runtime`
- `capabilities`

The combined status should be:

- `ok` when required app path information is available and no section reports
  `error`
- `degraded` when optional pieces are missing, such as config or database
- `unavailable` when app-data root cannot be resolved
- `error` only for unexpected unreadable/invalid state

### `GET /api/app/config`

Purpose: report generated local config file status.

Required response fields:

- `object = "mythic_edge_local_app_config_status"`
- `schema_version`
- `status`
- `config_file`
- `allowed_fields`
- `loaded_fields`
- `errors`

Required behavior:

- missing config is not an error; it is expected before setup writes exist
- invalid JSON returns `invalid_json` section status without echoing content
- unexpected fields may be reported by name only if they are safe labels
- secret-like field names must be counted/redacted, not echoed with values

### `GET /api/app/paths`

Purpose: report app-data root and required subfolder status.

Required response fields:

- `object = "mythic_edge_local_app_paths_status"`
- `schema_version`
- `status`
- `app_data_root`
- `subfolders`
- `redaction_policy`

Each path status should include:

- `key`
- `display_path`
- `exists`
- `kind`
- `required`
- `status`

Allowed `kind` values:

- `directory`
- `file`
- `unknown`

### `GET /api/analytics/database/status`

Purpose: report local app analytics database status without writing to it.

Required response fields:

- `object = "mythic_edge_local_app_analytics_database_status"`
- `schema_version`
- `status`
- `database`
- `migrations`
- `errors`

Required database fields:

- display-only path label
- existence
- file/directory classification
- schema status
- applied migration IDs if safely readable

### `GET /api/runtime/status`

Purpose: report that this slice does not yet control parser runtime behavior.

Required response fields:

- `object = "mythic_edge_local_app_runtime_status"`
- `schema_version`
- `status`
- `backend`
- `parser_runner`
- `live_watcher`
- `manual_import`
- `legacy_status_api`

Required first-slice values:

- `parser_runner.status = "deferred"`
- `live_watcher.status = "deferred"`
- `manual_import.status = "deferred"`
- `legacy_status_api.status = "separate_reference_surface"`

## Loopback And CORS Policy

The first backend implementation should expose an app factory and focused route
tests. It does not need to start a real network server.

Any run/server helper introduced in this or a future slice must:

- bind to `127.0.0.1` by default
- reject `0.0.0.0` unless a future contract explicitly authorizes broader bind
  behavior
- avoid wildcard CORS
- use explicit local development origins only, such as:
  - `http://127.0.0.1:<frontend_port>`
  - `http://localhost:<frontend_port>`

If Codex C configures CORS in this slice, tests must prove that wildcard CORS
is not used.

## Path Redaction Rules

Route payloads and logs must use safe display labels.

Allowed display examples:

- `%LOCALAPPDATA%\MythicEdgeDev`
- `<app_data>\config`
- `<app_data>\db\mythic_edge.sqlite3`
- `<configured_player_log>`
- `<detected_mtga_player_log>`
- `<repo>`

Forbidden default response examples:

- `C:\Users\<real-user>\...`
- raw temp directories from tests
- full private Player.log path
- webhook URL
- API key
- token

Tests must assert that response payloads do not include the temporary app-data
root string.

## Invariants

- Importing local app backend modules has no filesystem, server, database,
  parser, network, workbook, webhook, Apps Script, OpenAI, or Google Sheets
  side effects.
- GET routes are read-only.
- App-data defaults are outside the repo.
- Tests use temporary app-data roots.
- Missing config/database/app folders are setup statuses, not parser errors.
- Status endpoints do not own parser truth or analytics truth.
- Existing `status_api.py` remains separate.
- Existing parser config behavior remains unchanged.
- Existing analytics migration loader behavior remains unchanged.

## Error Behavior

Missing app-data root:

- report `unavailable`
- do not fall back into repo paths

Missing config file:

- report `missing`
- do not create it

Malformed config:

- report `invalid_json` or `invalid_shape`
- do not echo raw content

Missing database:

- report `missing`
- do not create it

Unreadable or invalid database:

- report `unreadable` or `invalid_sqlite`
- do not overwrite it

Migration discovery failure:

- report `migration_error`
- do not apply migrations

Invalid host or CORS configuration:

- report `error` in setup/config status
- do not start a server

Conflicting implementation need:

- if Codex C needs to write config, create folders, initialize databases,
  start a server, start runtime behavior, or read runtime artifacts, stop and
  route back to Codex B for a contract amendment.

## Side Effects

Allowed side effects in Codex C:

- add source files under `src/mythic_edge_parser/local_app/`
- add focused tests
- update `pyproject.toml` dependency metadata only as authorized above
- create
  `docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md`

Forbidden side effects:

- no generated app-data folders
- no SQLite database/WAL/SHM/journal files
- no config file writes
- no raw Player.log or JSONL reads/copies
- no parser runner start/stop
- no status API start/stop
- no runtime status file reads/writes
- no Google Sheets, workbook, webhook, Apps Script, Match Journal, OpenAI,
  model-provider, AI/coaching, or production behavior changes
- no Git staging, commit, push, PR, issue closure, or tracker completion unless
  a later role explicitly authorizes it

## Dependency Order

Recommended Codex C order:

1. Confirm branch and worktree state, preserving unrelated untracked contracts.
2. Add the optional app dependency strategy in `pyproject.toml` only if needed
   for FastAPI imports/tests.
3. Add `src/mythic_edge_parser/local_app/` path/config/status helpers with no
   import side effects.
4. Add FastAPI app factory and read-only route handlers.
5. Add focused tests with temporary app-data roots and no real Player.log.
6. Run focused and adjacent validation.
7. Write the implementation handoff.

## Compatibility

Must remain compatible with:

- current parser/runtime modules
- current stdlib `status_api.py`
- current `config.py` environment behavior
- current analytics migration loader API
- current analytics schema/migration tests
- current `.gitignore` generated-artifact protections

This contract does not require changing existing status API route shapes or
legacy Manasight-named runtime artifact names.

## Tests Required

Focused tests:

```powershell
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
```

Adjacent regression tests:

```powershell
py -m pytest -q tests\test_status_api.py tests\test_app_config.py tests\test_analytics_migration_loader.py tests\test_analytics_schema.py
```

Static and repository checks:

```powershell
py -m ruff check src tests tools
git diff --check
py tools\check_secret_patterns.py --all
```

Path-scoped protected-surface check:

```powershell
@'
pyproject.toml
src/mythic_edge_parser/local_app/__init__.py
src/mythic_edge_parser/local_app/paths.py
src/mythic_edge_parser/local_app/config.py
src/mythic_edge_parser/local_app/setup_status.py
src/mythic_edge_parser/local_app/backend.py
tests/test_analytics_local_app_config.py
tests/test_analytics_local_app_backend.py
docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Required assertions:

- app-data helpers use temp roots in tests
- no route response includes a temp root, real home path, raw Player.log text,
  secrets, or webhook-like strings
- missing config/database folders are reported without writes
- database status does not create missing SQLite files
- migration status calls discovery only, not application
- runtime status reports parser/live/import behavior as deferred
- FastAPI app can be created without starting a real server
- CORS is absent or explicitly local-only; wildcard CORS is not introduced

## Acceptance Criteria

Codex C satisfies this contract when:

- the local app backend package boundary exists
- FastAPI dependency changes are optional and explained
- the required read-only endpoints exist and have tested response shapes
- local app path/config/database/status helpers are tested with temporary
  roots
- no GET route creates folders, writes config, creates databases, imports
  files, starts runtime behavior, or exposes destructive actions
- path redaction tests prove private/temp paths are not returned
- focused and adjacent tests pass
- Ruff and whitespace checks pass
- secret/private-marker and protected-surface checks pass or any warnings are
  documented as non-blocking and scoped
- implementation handoff records exact files changed and forbidden surfaces not
  touched

## Open Questions

- Whether future setup initialization should create app-data folders from a
  `POST /api/app/setup/initialize` route or from the Windows bootstrapper only.
- Whether future config editing should allow full path display only in an
  explicit local configuration screen.
- Whether future database lifecycle should initialize the app database from the
  backend or bootstrapper.
- Whether future runtime status should read existing repo runtime artifacts or
  only app-owned job/watcher state.
- Whether `uvicorn` belongs in an `app` optional dependency group during a
  later launcher/server slice.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for the analytics/app backend config and setup-status skeleton.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Source issue:
https://github.com/Tahjali11/Mythic-Edge/issues/208

Source contract:
docs/contracts/analytics_app_backend_setup_status.md

Branch:
codex/analytics-foundation

Goal:
Compare current repo state to the contract and implement only the local app backend config/setup-status skeleton. Produce docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated local artifacts, especially docs/contracts/analytics_local_developer_app_shell.md and docs/contracts/quality_pyright_evidence_ledger_tests.md if they are still untracked.
- State what the backend setup-status slice is supposed to do, what the repo currently does, why the gap exists, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/analytics_app_backend_setup_status.md
- docs/contracts/analytics_local_developer_app_shell.md
- docs/contracts/analytics_migration_loader.md
- docs/contracts/analytics_local_sqlite_schema.md
- src/mythic_edge_parser/app/analytics_migration_loader.py
- src/mythic_edge_parser/app/status_api.py
- src/mythic_edge_parser/app/config.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- pyproject.toml
- .gitignore
- tests/test_status_api.py
- tests/test_app_config.py
- tests/test_analytics_migration_loader.py
- tests/test_analytics_schema.py

Implement only:
- src/mythic_edge_parser/local_app/ package for path/config/setup-status helpers and FastAPI app factory
- read-only endpoints:
  - GET /api/health
  - GET /api/app/setup-status
  - GET /api/app/config
  - GET /api/app/paths
  - GET /api/analytics/database/status
  - GET /api/runtime/status
- optional FastAPI dependency metadata as authorized by the contract
- tests/test_analytics_local_app_config.py
- tests/test_analytics_local_app_backend.py
- docs/implementation_handoffs/analytics_app_backend_setup_status_comparison.md

Do not:
- implement frontend, npm, package files, lockfiles, launcher behavior, bootstrapper behavior, manual import behavior, live watcher behavior, parser runner process control, job queue behavior, analytics query pages, database reset/delete/wipe/init actions, Google Sheets sync, Match Journal behavior, OpenAI/model-provider behavior, AI/coaching behavior, production behavior, or destructive UI actions
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, raw logs, local JSONL artifacts, generated SQLite files, runtime status files, failed posts, workbook exports, generated data, or target main
- edit src/mythic_edge_parser/app/status_api.py, src/mythic_edge_parser/app/config.py, src/mythic_edge_parser/app/runtime_surfaces.py, or src/mythic_edge_parser/app/analytics_migration_loader.py unless the contract proves insufficient and you route back to Codex B
- stage, commit, push, open a PR, close #204/#207/#208, or merge

Validation:
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_status_api.py tests\test_app_config.py tests\test_analytics_migration_loader.py tests\test_analytics_schema.py
py -m ruff check src tests tools
git diff --check
py tools\check_secret_patterns.py --all

Also run the path-scoped protected-surface check for the files you touched.

Final handoff must include:
- role performed
- source issue/tracker/umbrella issue
- source contract used
- files changed
- exact modules/functions/endpoints/tests changed
- FastAPI dependency decision
- what was verified
- what remains unverified
- whether any forbidden scope was touched
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/208"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #208"
  target_artifact: "docs/contracts/analytics_app_backend_setup_status.md"
  branch: "codex/analytics-foundation"
  risk_tier: "High"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped protected-surface gate for docs/contracts/analytics_app_backend_setup_status.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main unless explicitly approved."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
    - "Do not expose destructive UI actions."
```
