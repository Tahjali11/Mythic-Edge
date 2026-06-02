# Live App Player.log Watcher Process-Control Safeguards Contract

## Module

Local app live Player.log watcher process-control safeguards.

Plain English: before Mythic Edge lets the browser start or stop a live
Player.log watcher, the backend must be able to say whether doing so would be
safe, what is blocking it, and which parts are intentionally still disabled.

This contract defines a safeguards/status slice. It does not authorize starting
or stopping a watcher, tailing `Player.log`, running the parser, writing live
facts to SQLite, or exposing routine frontend start/stop controls.

## Source Issue

- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/242>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Predecessor issue: <https://github.com/Tahjali11/Mythic-Edge/issues/240>
- Predecessor PR: <https://github.com/Tahjali11/Mythic-Edge/pull/241>
- Predecessor merge commit:
  `536dca57808ccc48bc4785b9ae51b12a737d2d55`

## Branch

Intended branch:

```text
codex/analytics-foundation
```

Observed during this Codex B pass:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
```

This contract does not target `main`.

## Authority And Source Artifacts Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- issue #242
- tracker #204
- umbrella issue #207
- issue #240
- PR #241 context
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/live_app_player_log_path_watcher_status.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/status_api.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- local app backend/live-status tests as adjacent validation surfaces

## Risk Tier

High.

Reasons:

- live watcher process control can accidentally become real live capture;
- starting the existing parser runner can trigger runtime logging, status API,
  analytics sidecar behavior, webhook dispatching, or sheet posting depending
  on configuration;
- a process supervisor can leak private local paths, environment values,
  command lines, PIDs, logs, or raw Player.log content;
- duplicate watcher processes can corrupt local state or create confusing
  parser output;
- browser controls can look safer than they are unless backend safeguards are
  explicit first.

## Internal Project Area

Primary area: local app / live mode.

Adjacent areas:

- parser runtime and event stream, reference-only for this slice;
- local app setup-status;
- frontend status display;
- future live parser-owned analytics ingest.

## Bridge-Code Status

bridge_code

This surface bridges local app status to future parser process control. It
must not become parser truth, analytics truth, workbook truth, deployment
truth, AI truth, or an implicit authorization to control external transports.

## Ownership And Truth Boundaries

Truth owners:

- MTGA `Player.log` remains the observable raw evidence source.
- `src/mythic_edge_parser/app/runner.py`,
  `src/mythic_edge_parser/stream.py`, and
  `src/mythic_edge_parser/log/tailer.py` own actual parser/tailer behavior.
- Parser/state modules own event interpretation, match/game identity, final
  reconciliation, and parser-managed facts.
- The local app owns only local safety/status reporting and, in future
  contracts, local developer process supervision.
- SQLite analytics remains downstream storage and receives no live writes in
  this slice.
- The frontend displays status only.

This contract must not move truth ownership to:

- local app process-status payloads;
- browser UI state;
- app-owned state or lock files;
- analytics rows;
- workbook formulas;
- webhook or Apps Script transport;
- AI or model-provider output.

## Observed Current Behavior

### Local App Live Status

Issue #240 added read-only live status routes:

```text
GET /api/live/player-log/status
GET /api/live/watcher/status
```

Observed backend behavior:

- `build_live_player_log_status(paths)` reads local app config and checks a
  configured or default Player.log candidate with metadata-only filesystem
  calls.
- Player.log display paths are symbolic, such as `<configured_player_log>` or
  `<detected_mtga_player_log>`.
- Player.log contents are not read.
- `build_live_watcher_status(paths)` maps Player.log readiness into a watcher
  readiness payload.
- Current watcher status is `mode = "readiness_only"`.
- Current watcher payloads report:
  - `running = false`
  - `start_allowed = false`
  - `stop_allowed = false`
  - `parser_runner_started = false`
  - `tailing_started = false`
  - `sqlite_live_writes_enabled = false`
- `build_capabilities()` reports `live_watcher = "disabled"` and
  `parser_runner_control = "disabled"`.

Observed frontend behavior:

- The frontend can fetch and render live Player.log and watcher readiness.
- Existing status display must preserve symbolic/sanitized path rendering.
- Existing UI must distinguish readiness from active capture.

### Parser Runtime Boundary

`runner.py` is not a safe direct target for local-app browser process control
in this slice.

Observed runtime behavior:

- `runner.py` imports production-facing configuration, including Player.log
  path, webhook URL, sheet-posting toggles, match-log roots, status paths, and
  analytics settings.
- `runner.py` can start runtime logging, update runtime status files, start
  the parser status API, start the analytics sidecar, start webhook dispatch,
  and submit rows to Google Sheets depending on configuration.
- `runner.py` starts `MtgaEventStream.start(LOG_PATH)`.
- `MtgaEventStream.start(log_path)` opens a `FileTailer` from the end of the
  file and begins a polling pipeline.
- `FileTailer.poll_once()` reads raw bytes from `Player.log`.

Therefore, Codex C must not call `runner.main()`,
`MtgaEventStream.start(...)`, `FileTailer.open_from_start(...)`,
`FileTailer.open_from_end(...)`, or tailer polling methods for issue #242.

## Contract Decision

Issue #242 should implement backend-first process-control safeguards and
browser-visible safety status only.

Approved first slice:

- report whether process control is uninitialized, blocked, ready-for-future
  implementation, or deferred;
- report why start/stop is not currently allowed;
- define the process state vocabulary and single-instance guard policy;
- keep current readiness route compatibility;
- optionally add a new GET route for process-control safeguard status;
- optionally render the new process-control status in the frontend as disabled
  or informational.

Not approved for issue #242:

- real watcher start;
- real watcher stop;
- process spawning;
- process termination;
- live tailing;
- raw Player.log reads, hashes, snippets, or copies;
- parser runner start;
- live parser-owned SQLite writes;
- routine browser start/stop controls;
- global CORS redesign;
- Google Sheets, webhook, Apps Script, production, OpenAI, AI, coaching, Line
  Tracer, hidden-card, archetype, player-mistake, or gameplay-advice behavior.

## Public Interface Contract

### Route Inventory

Existing routes must remain compatible:

```text
GET /api/live/player-log/status
GET /api/live/watcher/status
```

Codex C may add exactly one read-only process-control safeguards route:

```text
GET /api/live/watcher/process
```

This route must be local-app loopback-only under the existing FastAPI app and
existing local-app CORS boundary.

Codex C must not add these routes in issue #242:

```text
POST /api/live/watcher/start
POST /api/live/watcher/stop
PUT /api/live/watcher/*
PATCH /api/live/watcher/*
DELETE /api/live/watcher/*
```

If implementation inspection shows that disabled/no-op POST routes are needed
for a browser harness, route back to Codex B. Do not silently add them.

### Process Safeguards Response Shape

`GET /api/live/watcher/process` must return a JSON object with:

- `object = "mythic_edge_local_app_live_watcher_process_status"`
- `schema_version =
  "live_app_player_log_watcher_process_control_safeguards.v1"`
- `status`: one approved process-control status
- `process_control`: object
- `watcher`: object
- `player_log`: sanitized nested summary or reference status
- `preconditions`: list of objects
- `state`: object
- `warnings`: list of sanitized codes
- `errors`: list of sanitized codes

Required `process_control` fields:

- `mode = "safeguards_only"`
- `implementation_status`: `not_implemented`, `state_only`, or `deferred`
- `start_allowed = false`
- `stop_allowed = false`
- `start_route_enabled = false`
- `stop_route_enabled = false`
- `ui_controls_allowed = false`
- `automatic_start_enabled = false`
- `parser_runner_started = false`
- `tailing_started = false`
- `sqlite_live_writes_enabled = false`
- `external_transport_allowed = false`
- `reason`: sanitized code or `null`

Required `watcher` fields:

- `status`: approved watcher process-control status
- `running = false` for this slice
- `pid_verified = false`
- `single_instance_guard`: `not_initialized`, `ready`, `blocked`,
  `stale`, `orphaned`, `unknown`, or `deferred`
- `supervisor_boundary`: `not_implemented`, `local_app_supervisor_deferred`,
  or `unknown`

Required `state` fields:

- `source`: `none`, `app_data_state_file`, `synthetic_test_state`,
  `unavailable`, or `deferred`
- `exists`: boolean
- `status`: approved watcher process-control status
- `stale`: boolean
- `pid_present`: boolean
- `pid_verified = false`
- `supervisor_token_present`: boolean
- `display_path`: symbolic app path or `null`
- `raw_path_exposed = false`

Required `preconditions` objects must include:

- `key`: stable precondition key
- `status`: `pass`, `fail`, `warning`, `not_checked`, or `deferred`
- `reason`: sanitized code or `null`

Required precondition keys:

- `player_log_ready`
- `app_data_root_available`
- `state_directory_available`
- `single_instance_guard_available`
- `supervisor_target_defined`
- `external_transport_disabled`
- `live_sqlite_ingest_contract_present`
- `frontend_controls_authorized`

The process-control response may reuse the sanitized `player_log` summary from
`build_live_watcher_status(paths)`, but it must not include raw absolute paths,
raw Player.log content, raw hashes, command lines, environment values, tokens,
spreadsheet IDs, webhook URLs, or local usernames.

### Status Vocabulary

Approved top-level process-control statuses:

- `not_initialized`: no app-owned process state exists yet.
- `not_configured`: process control cannot be evaluated because local setup is
  incomplete.
- `ready`: safeguards say future process control could be implemented, but no
  start route is enabled in this slice.
- `blocked`: one or more required preconditions failed.
- `blocked_missing_log`: Player.log candidate is missing.
- `blocked_unreadable_log`: metadata access is denied or unavailable.
- `blocked_invalid_config`: local app config prevents safe evaluation.
- `blocked_transport_enabled`: implementation cannot prove external workbook,
  webhook, Apps Script, or production-facing transport is disabled.
- `deferred`: process control is intentionally not implemented yet.
- `stopped`: future status only; not expected unless a local-app supervisor
  state model exists and does not imply active capture.
- `starting`: future status only.
- `running`: future status only; must not be returned by #242 unless Codex C
  routes back to Codex B with evidence of an existing authorized supervisor.
- `stopping`: future status only.
- `crashed`: future status for a supervised watcher failure.
- `stale`: app-owned process state is too old to trust.
- `orphaned`: state suggests a process once existed, but ownership cannot be
  verified.
- `unknown`: status cannot be safely classified.

`ready` means "ready for a future process-control implementation," not
"capturing" and not "safe to click start now."

## State, Lock, Log, And Diagnostic Boundaries

Allowed for issue #242:

- inspect whether app-owned state paths would be available;
- read a test-created app-owned state file under a disposable `app_data_root`
  in focused tests;
- report missing app-owned state as `not_initialized`;
- report stale or malformed app-owned state as `stale`, `unknown`, or
  `blocked`;
- define future app-owned paths symbolically.

Forbidden for issue #242:

- create app-data state files from GET routes;
- create app-data folders from GET routes;
- write PID files, lock files, logs, diagnostics, SQLite files, WAL/SHM files,
  runtime status files, failed posts, workbook exports, or local artifacts;
- read, hash, copy, sanitize, or tail raw Player.log content;
- store raw absolute paths or command lines in response payloads;
- terminate a process;
- trust an arbitrary PID from a file;
- kill a stale or orphaned process.

Future app-owned state paths, if implemented in a later contract, should be
under the local app data root, such as:

```text
<app_data_root>/jobs/live_watcher_state.json
<app_data_root>/jobs/live_watcher_lock.json
<app_data_root>/diagnostics/live_watcher_status.json
<app_data_root>/logs/live_watcher_supervisor.log
```

For #242, those paths are policy references only. They must be represented in
browser payloads with symbolic display values, not raw local paths.

## Single-Instance Guard Policy

Issue #242 must define, but not exercise, the guard needed before any future
start action.

Required guard semantics:

- A future start action must fail closed if another verified local-app watcher
  is starting or running.
- PID alone is not sufficient proof of ownership.
- Future ownership proof must include an app-owned supervisor token, state
  record, launch mode, and app-data root association.
- Stale state must be reported, not cleaned automatically.
- Orphaned state must be reported, not killed automatically.
- Unknown process state must block start rather than guess.
- A future stop action may stop only a process that the local app can prove it
  started and still owns.

Codex C may encode this policy in docs, response labels, and tests around
synthetic state. Codex C must not spawn or terminate processes.

## Existing Runner Boundary

The existing parser runner is not an approved start target for #242.

Codex C must not call or wrap:

- `runner.main()`
- `MtgaEventStream.start(...)`
- `FileTailer.open_from_start(...)`
- `FileTailer.open_from_end(...)`
- `FileTailer.poll(...)`
- `FileTailer.poll_once(...)`
- webhook dispatcher startup
- parser status API startup
- analytics sidecar startup

Future process-control work needs either:

- a new local-app watcher supervisor/harness with explicit no-transport
  guarantees; or
- a proven no-transport parser runner mode created under a separate contract.

Until then, process-control status must report `supervisor_target_defined` as
`deferred`, `fail`, or `not_checked`, and `start_allowed` must remain `false`.

## Backend Contract

Codex C may:

- add a narrow local-app helper module for process-control status, such as
  `src/mythic_edge_parser/local_app/live_watcher_process.py`;
- add `GET /api/live/watcher/process`;
- reuse `build_live_player_log_status(paths)` and
  `build_live_watcher_status(paths)`;
- add backward-compatible setup-status or capability fields if useful;
- add tests with disposable temporary app-data roots and synthetic app-owned
  state files.

Codex C must:

- keep all new behavior report-only;
- keep GET routes free of side effects;
- keep `start_allowed`, `stop_allowed`, `start_route_enabled`,
  `stop_route_enabled`, and `ui_controls_allowed` false;
- keep output sanitized and symbolic;
- fail closed on malformed synthetic state;
- avoid importing heavy runtime modules into the local app helper unless needed
  only for constant-free type references.

Codex C must not:

- start a process;
- call parser runtime/tailer startup;
- write generated artifacts;
- read raw Player.log content;
- add external transport behavior;
- make local setup mutate files.

## Frontend Contract

Codex C may:

- add a frontend API reader for `GET /api/live/watcher/process`;
- add TypeScript response types for process-control safeguard status;
- render an informational "Live Watcher Process" or similar panel;
- show blocked/deferred/ready-for-future statuses;
- show disabled controls as status indicators only if labels make clear that
  controls are unavailable.

Codex C must:

- preserve path redaction through `safeDisplayValue(...)` or equivalent;
- distinguish readiness from active capture;
- distinguish process-control safeguards from live capture;
- avoid showing `ready` as "running";
- avoid displaying raw local paths, raw state-file paths, command lines, PIDs
  as trusted process ownership, environment values, or secrets.

Codex C must not:

- add clickable start/stop controls;
- add destructive controls;
- add arbitrary SQL/database browsing;
- add config write behavior;
- add file picker behavior;
- imply live parser ingest is active.

## Generated And Private Artifact Safety

This slice must not create or commit:

- raw `Player.log` files;
- private JSONL artifacts;
- generated SQLite databases;
- SQLite WAL/SHM/journal files;
- runtime logs;
- app-data state files;
- PID files;
- lock files;
- diagnostics files;
- failed posts;
- workbook exports;
- secrets;
- credentials;
- tokens;
- API keys;
- webhook URLs;
- spreadsheet IDs;
- environment values;
- frontend build output;
- local-only artifacts.

Tests may use temporary directories and synthetic files only. Synthetic files
must not contain raw Player.log excerpts, private paths, real credentials, real
spreadsheet IDs, or real webhook URLs.

## Validation Requirements For Codex C

Backend tests must prove:

- `GET /api/live/watcher/process` returns the approved object and schema
  version;
- missing state reports `not_initialized`, `deferred`, or another approved
  non-running status;
- process-control flags are all disabled:
  - `start_allowed = false`
  - `stop_allowed = false`
  - `start_route_enabled = false`
  - `stop_route_enabled = false`
  - `ui_controls_allowed = false`
  - `automatic_start_enabled = false`
  - `parser_runner_started = false`
  - `tailing_started = false`
  - `sqlite_live_writes_enabled = false`
  - `external_transport_allowed = false`
- Player.log readiness blockers are mapped into process-control blockers;
- malformed synthetic app-owned state fails closed;
- stale synthetic app-owned state does not become `running`;
- raw local paths and Player.log strings are not leaked;
- GET routes do not create app-data folders or files;
- `POST /api/live/watcher/start` and `POST /api/live/watcher/stop` are absent
  or unsupported, not partially implemented;
- implementation does not call `runner.main()`, `MtgaEventStream.start(...)`,
  `FileTailer.open_from_*`, or tailer polling.

Frontend tests must prove, if frontend display changes are made:

- process-control status renders without exposing raw paths;
- disabled/deferred state is visible;
- no clickable start/stop controls are rendered;
- malformed process-control payloads fail safely;
- existing live Player.log and watcher readiness panels remain correct.

Validation commands expected for Codex C, adjusted only if files differ:

```powershell
py -m pytest -q tests/test_analytics_local_app_backend.py
py -m pytest -q tests/test_analytics_local_app_config.py tests/test_runner.py tests/test_tailer.py
npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
@'
docs/contracts/live_app_player_log_watcher_process_control_safeguards.md
docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/setup_status.py
src/mythic_edge_parser/local_app/live_watcher_process.py
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/status.ts
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/live_app_player_log_watcher_process_control_safeguards.md
docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/setup_status.py
src/mythic_edge_parser/local_app/live_watcher_process.py
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/status.ts
'@ | py tools\check_secret_patterns.py --paths-from-stdin
```

If frontend dependencies are unavailable, Codex C must report that explicitly
instead of claiming frontend validation passed.

## Acceptance Criteria

- Codex C produces
  `docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md`.
- Process-control status exists only as read-only safeguards/status.
- `GET /api/live/watcher/status` remains compatible with #240.
- If added, `GET /api/live/watcher/process` returns only sanitized
  safeguards/status data.
- No POST start/stop route is implemented.
- No frontend routine start/stop controls are implemented.
- No process is spawned, stopped, killed, or inspected through unsafe command
  lines.
- No raw Player.log content is read, copied, hashed, tailed, stored, or
  committed.
- No generated/private/runtime/local artifacts are committed.
- No parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/
  coaching/production behavior changes occur.
- Required focused validation passes or failures are explained with cause.

## Unknowns

- Whether a future local-app watcher should use a new supervisor harness or a
  no-transport parser runner mode.
- Whether process state should eventually live in JSON files, SQLite job
  tables, in-memory app state, or a combination.
- Whether actual-root live watcher controls should require a separate explicit
  approval step beyond disposable-root smoke validation.
- Whether Windows process ownership can be verified safely without exposing
  command lines or environment values.
- Whether future live SQLite writes should be tied to the same supervisor or a
  separate ingest service.

## Suspected Gaps

- Current live watcher status is readiness-only and cannot distinguish
  process-control safeguards from actual capture readiness.
- Current local app has no app-owned watcher supervisor, state file, lock file,
  or single-instance guard.
- Current frontend can show live readiness but cannot explain process-control
  blockers beyond the #240 readiness summary.
- Existing parser runner startup has too many production-facing side effects to
  be safely controlled from the browser without a narrower future contract.

## Protected Surfaces

Codex C and later roles must not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema, migrations, ingest semantics, or curated analytics views;
- Match Journal truth ownership;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- hidden-card inference;
- archetype inference;
- player-mistake labels;
- gameplay advice;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, or
  environment values.

## Out Of Scope

- Actual live watcher process start/stop.
- Parser-owned live fact writes to SQLite.
- Reading or tailing Player.log contents.
- Writing app-owned process state outside tests.
- Actual app-data-root process-control smoke.
- Production deployment.
- Global CORS redesign.
- UI redesign beyond a narrow informational status panel.
- Any cleanup, move, rename, or deletion of local artifacts.

## Codex C Implementation Scope

Codex C should compare current code to this contract and then implement only
the smallest safe safeguards/status slice.

Recommended implementation direction:

1. Add a local-app process-control status helper that consumes existing #240
   live watcher readiness and returns the approved safeguards payload.
2. Add `GET /api/live/watcher/process`.
3. Keep all control flags false.
4. Add focused backend tests proving no side effects, no raw leakage, and no
   runtime/tailer calls.
5. Add frontend display/types only if the backend status is stable and the UI
   remains informational.
6. Produce the implementation handoff.

If Codex C believes start/stop POST routes, a real process supervisor, or
actual app-data writes are required, stop and route back to Codex B.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #242:

https://github.com/Tahjali11/Mythic-Edge/issues/242

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_player_log_watcher_process_control_safeguards.md

Goal:
Compare the current local app live Player.log watcher status implementation
against the process-control safeguards contract, then implement only the
approved read-only safeguards/status slice.

Before editing:
- Confirm branch and git status.
- Inspect issue #242, tracker #204, umbrella #207, the contract, #240 live
  status contract/report/handoff, backend routes, setup-status live watcher
  behavior, runner/stream/tailer boundaries, frontend live status display, and
  relevant tests.
- State what the code is supposed to do, what it currently does, what gap
  remains, and the exact minimal implementation plan.

Allowed:
- Add a read-only process-control safeguards helper.
- Add GET /api/live/watcher/process.
- Keep GET /api/live/watcher/status compatible.
- Add focused backend tests.
- Add narrow frontend types/API/display only if informational and safe.
- Produce docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md.

Forbidden:
- Do not add POST /api/live/watcher/start or POST /api/live/watcher/stop.
- Do not start, stop, spawn, kill, or inspect live watcher processes through
  unsafe command lines.
- Do not call runner.main(), MtgaEventStream.start(...), FileTailer.open_from_*,
  FileTailer.poll(...), or FileTailer.poll_once(...).
- Do not read, copy, hash, tail, sanitize, store, or commit raw Player.log
  contents.
- Do not create app-data state files from GET routes.
- Do not expose routine frontend start/stop controls.
- Do not change parser behavior, parser state final reconciliation, parser
  event classes, match/game identity, deduplication, analytics schema,
  migrations, ingest semantics, curated analytics views, Match Journal truth
  ownership, workbook schema, webhook payload shape, Apps Script behavior,
  Google Sheets behavior, output transport, production behavior, OpenAI/model
  provider behavior, AI/coaching behavior, Line Tracer, hidden-card inference,
  archetype inference, player-mistake labels, or gameplay advice.
- Do not create or commit generated/private/runtime/local artifacts or secrets.
- Do not target main.

Validation:
py -m pytest -q tests/test_analytics_local_app_backend.py
py -m pytest -q tests/test_analytics_local_app_config.py tests/test_runner.py tests/test_tailer.py
npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
Run protected-surface and secret scans for the contract, implementation
handoff, and touched source/test/frontend files.

Final handoff must include:
- role performed
- issue/tracker/umbrella reviewed
- contract used
- files changed
- exact backend/frontend/test sections changed
- validation run
- protected surfaces touched or not touched
- remaining risks
- next recommended role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/242"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #242 and current local app live status implementation"
  target_artifact: "docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md"
  contract_artifact: "docs/contracts/live_app_player_log_watcher_process_control_safeguards.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  stop_conditions:
    - "Do not add watcher start/stop routes or routine frontend controls in issue #242."
    - "Do not start, stop, spawn, kill, tail, or inspect live watcher processes beyond read-only safe status."
    - "Do not read, copy, hash, tail, store, or commit raw Player.log contents."
    - "Do not create app-data state files from GET routes."
    - "Do not change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime/local artifacts or secrets."
    - "Do not target main."
```
