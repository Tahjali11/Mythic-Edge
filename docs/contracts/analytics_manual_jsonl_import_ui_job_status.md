# Analytics Manual JSONL Import UI Job-Status Contract

## Module

Manual JSONL import UI and job-status workflow for the local developer app.

This contract defines the first safe state-changing local app workflow after the
backend setup/status page, React/Vite setup/status page, and Windows developer
launcher are complete.

Plain English: this slice lets the user intentionally point the local app at a
supported legacy `.jsonl` artifact, replay it through the existing legacy JSONL
adapter, ingest parser-normalized facts into the app-owned SQLite database, and
see a sanitized import/job summary. It does not make the UI a parser, does not
store raw JSONL in SQLite, and does not add live Player.log watching or
destructive controls.

## Source Issue

- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/211>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Completed backend child: <https://github.com/Tahjali11/Mythic-Edge/issues/208>
- Completed frontend child: <https://github.com/Tahjali11/Mythic-Edge/issues/209>
- Completed launcher child: <https://github.com/Tahjali11/Mythic-Edge/issues/210>
- Umbrella contract: `docs/contracts/analytics_local_developer_app_shell.md`
- Backend contract: `docs/contracts/analytics_app_backend_setup_status.md`
- Frontend contract: `docs/contracts/analytics_react_vite_setup_status_page.md`
- Launcher contract:
  `docs/contracts/analytics_windows_developer_launcher_bootstrapper.md`
- Legacy adapter contract:
  `docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`
- Parser-normalized ingest contract:
  `docs/contracts/analytics_parser_normalized_replay_ingest.md`

## Branch

Current intended branch:

```text
codex/analytics-foundation
```

Observed during this Codex B pass:

```text
afb8033b364823b9ce131cd75293347f3dfe2203
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
- source issue #211
- `docs/project_roadmap.md`
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_app_backend_setup_status.md`
- `docs/contracts/analytics_react_vite_setup_status_page.md`
- `docs/contracts/analytics_windows_developer_launcher_bootstrapper.md`
- `docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`
- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `docs/contracts/analytics_gameplay_action_ingest.md`
- `docs/contracts/analytics_opponent_card_observation_ingest.md`
- `docs/contracts/analytics_field_evidence_ingest.md`
- `src/mythic_edge_parser/local_app/`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `tools/dev_app/`
- `frontend/`
- existing backend/frontend/adapter/ingest/launcher tests

## Risk Tier

High.

Reasons:

- this is the first local app route that intentionally writes analytics facts
  to SQLite;
- it reads private local JSONL artifacts selected by the user;
- it may create app-owned generated folders and a generated SQLite database;
- it introduces job-status semantics that must not leak raw paths, raw
  payloads, stack traces, secrets, or private artifact contents;
- it can accidentally trust legacy `derived` fields, blur parser truth, or grow
  into live Player.log watching;
- it can accidentally expose destructive import/database/job actions if the
  first UI is not constrained.

## Owning Layer

Primary owner: local analytics usability / manual historical import loop.

Truth boundaries:

- Parser/state owns MTGA event interpretation, match/game identity, final
  reconciliation, parser event classes, and parser-managed facts.
- `analytics_legacy_jsonl_adapter.py` owns adapting generated legacy JSONL
  event archives into parser-normalized replay input by replaying supported
  records through current parser/state logic.
- `analytics_ingest.py` owns writing already-normalized parser facts into local
  SQLite.
- SQLite owns local queryable storage and deterministic views, not parser
  truth.
- The local backend owns import orchestration, app-owned database access, and
  sanitized job-status responses.
- The frontend owns user input, loading/error states, and safe display only.

The import workflow must not become parser truth, analytics truth, evidence
truth, workbook truth, AI truth, hidden-card inference, archetype
classification, player-mistake truth, gameplay advice, merge readiness, deploy
readiness, or production authority.

## Contract Decision

The first implementation should use a local path input, not browser file upload.

Required first-slice behavior:

1. Frontend asks the user for a local `.jsonl` path.
2. Frontend submits that path to a loopback-only backend route.
3. Backend reads the selected file in place.
4. Backend does not copy the raw JSONL file into the repo or app-data folder.
5. Backend adapts the file through `adapt_legacy_jsonl_artifacts(...)`.
6. Backend opens the app-owned SQLite database under app-data, applies
   migrations through the existing ingest path, and writes parser-normalized
   facts through `ingest_parser_normalized_replay(...)`.
7. Backend stores only an in-memory sanitized job summary for the current
   process.
8. Frontend displays only sanitized labels, counts, statuses, warning
   categories, and row counts.

Reason: the current adapter is path-oriented, and path input avoids adding a
raw upload/copy/retention policy in this first state-changing app slice.

Browser file upload, drag/drop import, copied imports under app-data, import
history browsing, background workers, persistent job metadata, cancellation,
retry queues, and job deletion are deferred.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_manual_jsonl_import_ui_job_status.md`

Future Codex C implementation files authorized by this contract:

- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/paths.py`, only for app-data directory
  creation helpers if needed by import
- `tests/test_analytics_manual_jsonl_import.py`
- frontend source/test files under `frontend/src/`
- `docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md`

Conditional implementation file:

- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`, only to add
  backward-compatible sanitized stats needed by job status, such as
  `duplicate_raw_hash_count`, without changing adapter replay semantics.

Referenced but not owned:

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `tools/dev_app/`
- `frontend/package.json`
- `frontend/package-lock.json`
- `.gitignore`
- existing adapter, ingest, backend, frontend, and launcher tests

Codex C must route back to Codex B before changing parser behavior, analytics
schema, migration SQL, saved-event replay semantics, workbook/webhook/App
Script behavior, or frontend/backend behavior outside this contract.

## Observed Current Behavior

Completed local app foundation:

- backend setup/status routes exist under `src/mythic_edge_parser/local_app/`;
- frontend setup/status page exists under `frontend/`;
- Windows developer launcher exists under `tools/dev_app/`;
- app-owned generated folder contract is
  `%LOCALAPPDATA%\MythicEdgeDev\`;
- `frontend/node_modules/`, `frontend/dist/`, `frontend/.vite/`,
  `frontend/coverage/`, and repo `data/analytics/` are ignored.

Current backend behavior:

- `create_app(...)` exposes only read-only `GET` setup/status routes.
- `build_capabilities()` reports `manual_import: disabled`.
- `build_runtime_state()` reports `manual_import.status = deferred`.
- setup/status routes do not create app-data folders, write config, initialize
  the database, import JSONL, or start parser runtime behavior.

Current frontend behavior:

- the first screen is a setup/status page.
- Manual Import, Analytics Views, and Live Watcher panels are disabled/deferred
  placeholders.
- The frontend has no path input, import submit action, job-status API client,
  or import quality display.
- Frontend tests assert no action controls exist.

Current adapter/ingest behavior:

- `adapt_legacy_jsonl_artifacts(source, source_artifact_label=None)` accepts a
  file or directory path and returns a `LegacyJsonlAdapterResult`.
- The adapter uses current parser/state replay, not legacy `derived` values as
  parser truth.
- The adapter returns safe replay input with `source_kind = saved_event_replay`.
- The adapter reports files processed, records seen, events processed, events
  skipped, unsupported kind counts, and warnings.
- `ingest_parser_normalized_replay(connection, replay, ...)` applies analytics
  migrations and writes parser-normalized facts into a caller-supplied SQLite
  connection.
- Existing ingest includes gameplay actions, opponent-card observations, and
  field evidence slices.

Observed gap:

- no backend route accepts a JSONL import request;
- no app-owned SQLite database open/create path exists for the local app import
  workflow;
- no job-status model exists for local app imports;
- no UI lets the user submit a supported legacy JSONL path;
- no tests prove manual import avoids raw path/payload leakage.

## Public Interface

### Backend routes

Required new route:

```text
POST /api/imports/jsonl
```

Required new route:

```text
GET /api/imports/jobs/{job_id}
```

No other import routes are required in this first slice.

Forbidden first-slice routes:

- no `DELETE /api/imports/...`
- no database reset/wipe/clear routes
- no job deletion routes
- no broad SQL browser routes
- no live Player.log watcher routes
- no parser runner process-control routes
- no upload route
- no import-history list route unless Codex C routes back with a contract need

### Backend module surface

Recommended module:

```text
mythic_edge_parser.local_app.import_jobs
```

Required public constant:

```text
MANUAL_JSONL_IMPORT_SCHEMA_VERSION = "analytics_manual_jsonl_import_ui_job_status.v1"
```

Recommended public functions:

```python
run_manual_jsonl_import(
    request: Mapping[str, object],
    *,
    app_data_root: Path | None = None,
    now: Callable[[], str] | None = None,
    job_id_factory: Callable[[], str] | None = None,
) -> dict[str, object]

get_import_job(job_id: str) -> dict[str, object] | None
```

Names may differ, but Codex C must keep the route handler small and keep the
testable orchestration logic outside the FastAPI decorator body.

### Frontend surface

The frontend may add:

- a Manual Import page, section, or tab;
- a local path input;
- a submit button;
- disabled/during-import state;
- final job summary display;
- warning/error display;
- API helpers and TypeScript types for import requests and job status.

The first implementation may keep the setup/status page as the shell and add a
Manual Import section below or beside it. It does not need a router dependency.

## Request Contract

`POST /api/imports/jsonl` request body:

```json
{
  "source_path": "Z:\\synthetic\\events_v1.jsonl",
  "source_artifact_label": "optional_safe_label"
}
```

Required fields:

- `source_path`: non-empty string path to a local `.jsonl` file.

Optional fields:

- `source_artifact_label`: safe adapter label, using the existing adapter label
  rules.

Required `source_path` handling:

- reject blank values;
- reject URLs;
- reject UNC/network paths in v1;
- reject non-`.jsonl` paths;
- reject missing paths;
- reject directories in this UI workflow, even though the adapter library still
  supports directories;
- resolve and read the file in place;
- never copy the raw file into the repo or app-data folder;
- never return the full raw path in the response.

Reason for file-only route: the UI first slice should be simple and deliberate.
Directory/bundle import can be a later issue because it changes the user mental
model and import quality display.

The raw path may exist only in:

- the user's editable browser input;
- the backend request body;
- local process memory while the route runs.

The raw path must not be stored in job summaries, frontend state after the
terminal result, backend logs, app-data files, SQLite, committed tests, docs,
screenshots, or diagnostics.

## Job Status Schema

Every import job response must be JSON and include:

- `object = "mythic_edge_local_app_manual_jsonl_import_job"`
- `schema_version = "analytics_manual_jsonl_import_ui_job_status.v1"`
- `job_id`
- `status`
- `phase`
- `created_at`
- `started_at`
- `finished_at`
- `source`
- `adapter`
- `ingest`
- `database`
- `warnings`
- `errors`

Allowed `status` values:

- `queued`
- `running`
- `succeeded`
- `degraded`
- `failed`
- `rejected`

Allowed `phase` values:

- `received`
- `validating_source`
- `adapting_jsonl`
- `opening_database`
- `ingesting_sqlite`
- `completed`
- `failed`

`POST /api/imports/jsonl` may execute synchronously and return a terminal job
summary. `queued` and `running` are reserved for the in-memory job model and
future background execution; they do not require a background worker in this
slice.

`job_id` must be opaque and must not be derived from a local path or raw payload
body. A UUID-style generated ID is acceptable. Tests should inject a stable job
ID factory rather than requiring deterministic IDs in production.

## Job Source Fields

`source` must include:

- `source_kind = "saved_event_replay"`
- `source_artifact_label`
- `source_display_label`
- `source_file_extension = ".jsonl"`
- `path_echoed = false`

`source_display_label` rules:

- default to `<selected_jsonl>`;
- may include a sanitized basename only if it contains no path separators,
  private markers, URL fragments, or secret-like text;
- must never include the full absolute path;
- must never include raw Player.log snippets, raw JSONL payload snippets,
  secrets, tokens, API keys, workbook IDs, or URLs.

## Adapter Summary Fields

`adapter` must include:

- `status`
- `files_processed`
- `records_seen`
- `events_processed`
- `events_skipped`
- `unsupported_kind_counts`
- `warnings`
- `duplicate_raw_hash_count`, when the adapter exposes it

Required behavior:

- unsupported event kinds should degrade a successful import rather than fail
  if parser-normalized rows were produced;
- duplicate raw hashes should be counted or included in skipped totals without
  exposing hash values;
- adapter warnings must be safe labels/categories, not raw payload text;
- legacy `derived` fields remain diagnostic only and must not become parser
  truth.

If current adapter stats are insufficient for a required display field, Codex C
may add backward-compatible sanitized stat fields to
`LegacyJsonlAdapterResult`. It must not change replay semantics, file
selection semantics, or parser interpretation.

## Ingest Summary Fields

`ingest` must include:

- `status`
- `ingest_run_id`, when ingest starts successfully
- `source_kind`
- `source_artifact_label`
- `row_counts`
- `warnings`
- `skipped`

Required behavior:

- use `ingest_parser_normalized_replay(...)` as the only SQLite fact writer;
- preserve the ingest layer's deterministic replay/upsert policy;
- expose touched-table row counts from ingest when available;
- do not reinterpret match/game/action/observation facts in the local app
  backend;
- do not store raw JSONL records, raw payloads, or raw saved-event lines in
  SQLite.

## Database Behavior

Default app database path:

```text
%LOCALAPPDATA%\MythicEdgeDev\db\mythic_edge.sqlite3
```

`POST /api/imports/jsonl` is allowed to create generated app-data folders and
the app-owned SQLite database only after the user explicitly submits an import.

Required order:

1. validate source request shape;
2. validate the selected source path exists and is a `.jsonl` file;
3. adapt the JSONL into parser-normalized replay input;
4. create required app-data folders if needed;
5. open the app-owned SQLite database;
6. call `ingest_parser_normalized_replay(...)`.

Reason: invalid path/adapter failures should not create a database solely by
being submitted.

Allowed database side effects:

- create `%LOCALAPPDATA%\MythicEdgeDev\` and required subfolders when missing;
- create `%LOCALAPPDATA%\MythicEdgeDev\db\mythic_edge.sqlite3`;
- allow SQLite to create local WAL/SHM/journal files under the app-data `db`
  folder when SQLite needs them;
- apply source-controlled analytics migrations through the existing ingest
  path;
- insert/upsert parser-normalized analytics facts.

Forbidden database side effects:

- no database creation inside the repo;
- no database reset, wipe, clear, delete, compact, vacuum, export, or broad SQL
  execution;
- no raw JSONL payload storage;
- no raw Player.log storage;
- no schema migration changes in this slice.

If `%LOCALAPPDATA%` is unavailable and no explicit app-data root test override
is supplied, the route must fail safely with an `app_data_unavailable` error
category. It must not fall back into the repo.

## Job Storage Policy

First version job status should be process-local and in memory.

Required behavior:

- store sanitized job summaries in a bounded in-memory registry;
- support `GET /api/imports/jobs/{job_id}` for jobs created during the current
  backend process;
- return `404` or a safe `not_found` response for unknown/expired jobs;
- do not write job summaries under `%LOCALAPPDATA%\MythicEdgeDev\jobs\` in this
  slice;
- do not create persistent import history;
- do not store raw paths or raw payloads in memory after the terminal job
  summary is built.

Persistent app-data job metadata may be considered later after a separate
retention/privacy contract.

## Frontend UI Contract

The Manual Import UI may include:

- a text input for a local `.jsonl` path;
- optional safe source label input only if it uses the adapter's safe-label
  validation expectations;
- an Import button;
- disabled state while a request is in flight;
- backend unavailable state;
- validation/rejected state;
- succeeded/degraded/failed job summary;
- adapter counts and warnings;
- ingest row counts and warnings;
- safe database status label.

The frontend must not:

- parse JSONL itself;
- read local files through browser APIs in v1;
- upload raw JSONL content;
- store the source path in localStorage, sessionStorage, query strings, logs,
  screenshots, snapshots, or test fixtures;
- render the submitted raw path in job-status cards after the request
  completes;
- display raw JSONL lines, payload snippets, raw Player.log lines, stack
  traces, secrets, tokens, API keys, workbook IDs, URLs, or full private paths;
- expose cancel, retry queue, delete job, clear jobs, delete import, reset
  database, wipe app data, Git, Sheets, AI, production, or live watcher
  controls.

It is acceptable for the raw path to be visible in the editable input while the
user is typing. After a terminal result, the UI should clear the input or make
clear that the path is user-entered and not part of the stored job summary.

Existing setup/status panels may remain. Manual Import should become an enabled
section, while Analytics Views and Live Watcher remain deferred/read-only
placeholders.

## Capability And Setup Status Changes

This contract authorizes the narrow backend/frontend status change needed to
show manual import is available.

After implementation:

- `build_capabilities()["manual_import"]` may change from `disabled` to
  `enabled`.
- runtime manual import status may change from `deferred` to `enabled` or
  `available`.
- `database_init` must remain disabled as a standalone action, because database
  creation is allowed only as part of an explicit import in this slice.
- `live_watcher`, `parser_runner_control`, config write, analytics dashboard,
  Sheets, Match Journal, OpenAI/AI, and production capabilities remain disabled
  or deferred.

Existing backend/frontend tests that asserted no controls existed must be
updated only to allow the new Manual Import controls. They should continue to
assert that destructive controls and deferred future controls are absent.

## Error Behavior

Request validation failure:

- return a `rejected` job or safe 4xx response;
- include only safe error code/category text;
- do not run adapter or create database files.

Missing source file:

- return `rejected` with `source_missing`;
- do not echo the submitted full path.

Path is a directory, URL, UNC/network path, non-JSONL file, or unsupported
shape:

- return `rejected`;
- do not run adapter or create database files.

Adapter invalid JSON, malformed record, unsupported-only file, or no ingestable
rows:

- return `failed`;
- include safe adapter error category/message;
- do not echo raw line, payload, or source path;
- do not create a database if adaptation failed before ingest.

Unsupported event kinds or duplicate hashes with otherwise successful replay:

- return `degraded` if ingest completes and warnings/skips are nonzero;
- return `succeeded` if ingest completes with no warnings/skips.

Database unavailable, migration failure, or ingest failure:

- return `failed`;
- roll back fact writes when ingest raises;
- do not expose SQL statements, stack traces, local paths, or raw payloads;
- a migrated empty database may exist only if failure happened after the
  explicit import reached the database phase.

Unknown job ID:

- return a safe not-found response;
- do not reveal any existing job IDs.

Contract conflict:

- route back to Codex B if implementation needs file upload, background
  workers, persistent job metadata, import history, database reset/delete,
  schema migrations, parser changes, saved-event replay semantic changes,
  frontend routing dependencies, or live watcher behavior.

## Invariants

- Manual import is explicit and user-triggered.
- JSONL files are read in place and not copied by default.
- The UI/backend do not parse JSONL into facts outside the existing adapter.
- Legacy `derived` values never become parser truth.
- SQLite receives parser-normalized facts only.
- App-generated database files live under app-data, not the repo.
- Job summaries are sanitized and process-local in v1.
- Full private paths are not echoed in job responses.
- Raw JSONL payloads and raw Player.log lines are never displayed, logged,
  committed, or stored in SQLite.
- No destructive controls are exposed.
- Manual import stays separate from live Player.log watching.

## Side Effects

Allowed future implementation side effects:

- add local backend import/job code;
- add frontend Manual Import UI/API code;
- add focused backend/frontend tests;
- update setup/status manual-import capability labels;
- read explicitly supplied local `.jsonl` files;
- create app-data folders and app-owned SQLite database during explicit import;
- apply analytics migrations through existing ingest;
- write parser-normalized analytics facts to app-owned SQLite;
- write implementation handoff documentation.

Forbidden side effects:

- no code implementation in this Codex B pass;
- no upload/copy/retention of raw JSONL files;
- no committed private JSONL artifacts, raw logs, generated SQLite files, WAL,
  SHM, journal files, runtime artifacts, failed-delivery artifacts, workbook exports,
  generated data, screenshots with private paths, secrets, credentials, tokens,
  API keys, or webhook URLs;
- no parser behavior changes;
- no parser state final reconciliation changes;
- no parser event class or event kind changes;
- no match/game identity or deduplication changes;
- no workbook schema, webhook payload, Apps Script, Google Sheets, Match
  Journal, OpenAI/model-provider, AI/coaching, Line Tracer, production, or
  deployment behavior changes;
- no Git mutating commands from the UI/backend.

## Dependency Order

Recommended Codex C order:

1. Confirm branch is `codex/analytics-foundation` and inspect worktree state.
2. Read this contract plus backend/frontend/launcher/adapter/ingest contracts.
3. Compare current backend capabilities and frontend deferred Manual Import
   panel against this contract.
4. Add backend import orchestration and in-memory job registry with tests first.
5. Add app-owned database path/open behavior only inside explicit import.
6. Add Manual Import frontend API types/client and UI tests.
7. Update existing setup/status/frontend tests for enabled manual import while
   preserving destructive-control absence.
8. Run focused backend/adapter/ingest/frontend validation.
9. Run path-scoped protected-surface and secret/private-marker scans.
10. Write the implementation handoff.

## Compatibility

Must remain compatible with:

- existing backend setup/status endpoint schema version
  `analytics_app_backend_setup_status.v1`, except for the explicitly
  authorized manual-import capability/status labels;
- existing React/Vite frontend package and npm validation scripts;
- existing Windows developer launcher process model;
- existing legacy JSONL adapter semantics;
- existing parser-normalized ingest semantics and SQLite schema;
- existing analytics migration loader;
- existing `.gitignore` generated-artifact protections.

This contract does not require changing CLI behavior, packaged mode, backend
static file serving, live status API behavior, or legacy `tools/auto_launcher/`
behavior.

## Unknowns And Open Questions

- Whether future versions should support browser file upload instead of local
  path input.
- Whether future versions should import directories/bundles as a UI workflow.
- Whether persistent import history should live in app-data JSON, SQLite
  metadata, or both.
- Whether long-running imports need background workers, polling, cancellation,
  progress streaming, or retry queues.
- Whether user-friendly file picking is possible without raw upload/copy
  retention.
- Whether `duplicate_raw_hash_count` should become a stable adapter stat or
  remain folded into `events_skipped`.
- How much path display is acceptable in a future explicit configuration
  screen.

## Suspected Gaps

- No `src/mythic_edge_parser/local_app/import_jobs.py` module exists.
- `create_app(...)` exposes no import routes.
- `build_capabilities()` still reports `manual_import: disabled`.
- `build_runtime_state()` still reports Manual Import as deferred.
- Frontend Manual Import is a disabled placeholder with no controls.
- Frontend tests currently assert no buttons exist.
- No backend tests prove explicit import creates only app-owned DB files and no
  repo-local generated artifacts.
- Adapter stats do not currently expose a dedicated duplicate raw hash count.
- No tests prove job responses omit submitted full paths.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior
- saved-event replay semantics, except for optional sanitized adapter stats
  that do not alter replay behavior
- parser state final reconciliation
- parser event classes
- event kind values
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
- Line Tracer behavior
- production behavior
- deployment behavior
- secrets, credentials, tokens, API keys, webhook URLs, or environment-variable
  contracts
- raw Player.log files
- private legacy JSONL artifacts
- generated SQLite database/WAL/SHM/journal files inside the repo
- runtime status files
- failed-delivery payload artifacts
- workbook exports
- generated card/tier data
- destructive import/database/job/launcher/UI actions

## Out Of Scope

- Implementation code in this Codex B pass.
- Opening a PR or targeting `main`.
- Browser file upload, drag/drop, or raw-content upload.
- Copying JSONL files into app-data.
- Sanitizing, fixture-izing, or committing real private JSONL artifacts.
- Persistent job history.
- Import deletion, job deletion, retries, cancellation, or queue management.
- Database reset, wipe, delete, compact, vacuum, export, broad SQL, or generic
  database browser behavior.
- Live Player.log watching or live parser writes.
- Live watcher process control.
- Analytics dashboard pages.
- Match Journal UI/API.
- Google Sheets sync.
- OpenAI/model-provider runtime integration.
- AI coaching.
- Line Tracer.
- Gameplay advice, hidden-card inference, complete-decklist inference,
  sideboard-delta truth, archetype classification, or player-mistake labels.
- Production deployment behavior.

## Tests Required

Focused backend tests:

```powershell
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
```

Required backend coverage:

- valid synthetic JSONL path imports into a temporary app-owned SQLite database;
- POST response includes a terminal job summary with safe source, adapter,
  ingest, database, warning, and error sections;
- GET job-status route returns the same sanitized in-memory summary for the
  current process;
- submitted full path is not echoed in job summary JSON;
- invalid path/non-JSONL/URL/UNC/directory requests are rejected before DB
  creation;
- malformed JSONL fails without raw line or payload echoing;
- unsupported event kinds and duplicate hashes are summarized safely;
- legacy `derived` values do not become parser truth;
- generated SQLite files are created only under a temporary app-data root in
  tests;
- no repo `data/analytics/` database files are created;
- no destructive routes or DELETE methods are present.

Adjacent backend/adapter/ingest validation:

```powershell
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_field_evidence_ingest.py
```

Frontend validation:

```powershell
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
```

Required frontend coverage:

- Manual Import UI renders an enabled path-input workflow;
- submitting a path calls `POST /api/imports/jsonl`;
- success, degraded, failed, rejected, backend-unavailable, malformed response,
  and unsafe API base states render safely;
- job summaries display counts/warnings without raw paths or raw payloads;
- the raw submitted path is not rendered in summary cards after completion;
- no reset/delete/wipe/cancel/retry/live-watcher/Schedule/Git/Sheets/AI
  controls appear.

Static and repository checks:

```powershell
py -m ruff check src tests tools
git diff --check
py tools\check_secret_patterns.py --all
```

Path-scoped protected-surface check:

```powershell
@'
docs/contracts/analytics_manual_jsonl_import_ui_job_status.md
src/mythic_edge_parser/local_app/import_jobs.py
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/setup_status.py
src/mythic_edge_parser/local_app/paths.py
src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
tests/test_analytics_manual_jsonl_import.py
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/status.ts
frontend/src/App.css
docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Path-scoped secret/private-marker scan:

```powershell
@'
docs/contracts/analytics_manual_jsonl_import_ui_job_status.md
src/mythic_edge_parser/local_app/import_jobs.py
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/setup_status.py
src/mythic_edge_parser/local_app/paths.py
src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
tests/test_analytics_manual_jsonl_import.py
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/status.ts
frontend/src/App.css
docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Generated artifact check:

- Codex C/E should report `git status --short` and confirm no generated
  SQLite DB/WAL/SHM/journal files, raw JSONL artifacts, runtime artifacts,
  failed-delivery artifacts, workbook exports, screenshots with private data, or
  `node_modules/` files are changed or untracked.

## Acceptance Criteria

Codex C satisfies this contract when:

- `POST /api/imports/jsonl` exists and accepts an explicit local `.jsonl` path.
- `GET /api/imports/jobs/{job_id}` returns a sanitized process-local job
  summary.
- The backend reads the selected JSONL in place and does not copy or persist
  raw JSONL.
- The backend uses `adapt_legacy_jsonl_artifacts(...)` and
  `ingest_parser_normalized_replay(...)` rather than reinterpreting facts.
- App-owned SQLite files are created only under app-data during explicit
  import.
- Job summaries include safe adapter, ingest, database, row-count, warning, and
  error categories.
- Job summaries do not echo full paths, raw payloads, raw lines, secrets, URLs,
  stack traces, or SQL internals.
- Frontend Manual Import controls exist and future/destructive controls remain
  absent.
- Focused backend, adjacent analytics, frontend, Ruff, diff, protected-surface,
  secret/private-marker, and generated-artifact checks pass or any failures are
  documented with routing.
- No parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI
  coaching/production behavior changes occur.

## Validation Expectations For This Contract

Codex B validation for this docs-only contract:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/analytics_manual_jsonl_import_ui_job_status.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/analytics_manual_jsonl_import_ui_job_status.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #211.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/211

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_manual_jsonl_import_ui_job_status.md

Goal:
Compare current repo state to the contract and implement only the Manual JSONL import UI and job-status workflow for the local developer app. Produce docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated local artifacts.
- State what the manual import workflow is supposed to do, what current code actually does, why the gap exists, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/analytics_manual_jsonl_import_ui_job_status.md
- docs/contracts/analytics_local_developer_app_shell.md
- docs/contracts/analytics_app_backend_setup_status.md
- docs/contracts/analytics_react_vite_setup_status_page.md
- docs/contracts/analytics_windows_developer_launcher_bootstrapper.md
- docs/contracts/analytics_legacy_jsonl_artifact_adapter.md
- docs/contracts/analytics_parser_normalized_replay_ingest.md
- src/mythic_edge_parser/local_app/
- src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
- src/mythic_edge_parser/app/analytics_ingest.py
- src/mythic_edge_parser/app/analytics_migration_loader.py
- frontend/src/
- tests/test_analytics_legacy_jsonl_artifact_adapter.py
- tests/test_analytics_parser_normalized_replay_ingest.py
- tests/test_analytics_local_app_backend.py
- frontend/src/App.test.tsx

Implement only:
- backend POST /api/imports/jsonl
- backend GET /api/imports/jobs/{job_id}
- process-local sanitized import job summaries
- local path input validation for explicit .jsonl files only
- import orchestration through adapt_legacy_jsonl_artifacts(...) and ingest_parser_normalized_replay(...)
- app-owned SQLite creation/migration/write only during explicit import
- frontend Manual Import UI with safe status/count/warning/error display
- focused backend and frontend tests
- narrow capability/status updates showing manual import enabled
- docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md

Do not:
- implement file upload, drag/drop import, copied imports, directory import UI, persistent job history, cancellation, retry queues, job deletion, database reset/delete/wipe/clear/export/browser routes, live Player.log watching, live watcher controls, parser runner controls, analytics dashboard pages, Match Journal behavior, Google Sheets sync, OpenAI/model-provider runtime integration, AI/coaching behavior, Line Tracer, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, production behavior, deployment behavior, Git mutating commands, or destructive UI/backend actions
- change parser behavior, saved-event replay semantics except optional sanitized adapter stats, parser state final reconciliation, parser event classes, event kind values, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, credentials, environment-variable contracts, raw logs, private JSONL artifacts, generated SQLite files inside the repo, runtime status files, failed-delivery artifacts, workbook exports, generated data, or target main
- commit node_modules, frontend/dist, frontend/.vite, coverage, .env files, raw JSONL, screenshots with private data, generated databases, WAL/SHM/journal files, or secrets
- stage, commit, push, open a PR, close #204/#207/#211, or merge unless explicitly asked

Validation:
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_field_evidence_ingest.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools\check_secret_patterns.py --all

Also run path-scoped protected-surface and secret/private-marker scans over the files touched by this issue. Report generated SQLite/local artifact status.

Final handoff must include:
- role performed
- source issue/tracker/umbrella issue
- source contract used
- files changed
- exact backend routes/functions/tests changed
- exact frontend modules/components/tests changed
- adapter stat decision, if any
- database creation/migration behavior
- job status schema implemented
- what was verified
- what remains unverified
- whether any forbidden scope was touched
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/211"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #211"
  target_artifact: "docs/contracts/analytics_manual_jsonl_import_ui_job_status.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped protected-surface gate for docs/contracts/analytics_manual_jsonl_import_ui_job_status.md"
    - "path-scoped secret/private-marker scan for docs/contracts/analytics_manual_jsonl_import_ui_job_status.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
    - "Do not expose destructive import, database, job, launcher, or UI actions."
```
