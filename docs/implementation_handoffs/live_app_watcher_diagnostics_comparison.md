# Live App Watcher Diagnostics Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/246

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/live_app_watcher_diagnostics.md`

## Internal Project Area

Local App / Live Player.log Mode

## Truth Owner

The local app diagnostics route owns only sanitized local status composition.
Parser/state remains the truth owner for parser-managed facts. `Player.log`
remains the raw observable evidence source. SQLite remains local analytics
support, not parser truth.

## Bridge-Code Status

`bridge_code`

Allowed flow implemented:

```text
sanitized local app live status surfaces
  -> read-only watcher diagnostics JSON
  -> frontend read-only diagnostics panel
```

No reverse flow into parser behavior, live capture, workbook, webhook, Apps
Script, Sheets, AI, or production behavior was added.

## Role Performed

Codex C: Module Implementer / comparison thread

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/live_app_watcher_diagnostics.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/evidence_runtime_status.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_live_app_parser_owned_fact_capture_sqlite.py`
- `tests/test_tailer.py`
- `tests/test_parser_diagnostics_mode.py`
- `tests/test_evidence_runtime_status.py`

## Current Behavior Compared To Contract

Existing behavior already provided separate safe local app surfaces:

- `GET /api/live/player-log/status` reported symbolic Player.log metadata without reading contents.
- `GET /api/live/watcher/status` reported readiness only; it did not start tailing or capture.
- `GET /api/live/watcher/process` reported process-control safeguards and app-owned watcher state without process control.
- `GET /api/live/ingest/status` reported #244 live SQLite capture capability metadata without performing writes.

The gap was that users had to mentally combine these separate surfaces. The
contract required one consolidated read-only diagnostics/status surface, with
safe labels, source summaries, privacy/capability booleans, frontend validation,
and focused tests that prove the route does not become a runner, tailer, raw-log
reader, report generator, writer, or remediation control.

## Implementation Option Chosen

Implemented the smallest approved first slice:

- a new local app helper that composes existing sanitized status builders;
- exactly one new backend `GET /api/live/watcher/diagnostics` route;
- TypeScript constants, response types, fail-closed API validation, and a
  read-only frontend diagnostics panel;
- focused backend and frontend tests for shape, privacy, stale/malformed state,
  source composition, fail-closed validation, and absence of destructive
  controls.

The implementation deliberately leaves tailer event bridge, parser diagnostics,
and evidence runtime health as deferred or expected-but-unavailable unless a
future authorized sanitized source supplies them.

## Files Changed

- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/live_app_watcher_diagnostics_comparison.md`

Untracked contract present from Codex B:

- `docs/contracts/live_app_watcher_diagnostics.md`

## Exact Implementation Sections Changed

### Backend

- Added `build_live_watcher_diagnostics_status(paths)` in
  `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`.
- The helper composes:
  - `build_live_player_log_status(paths)`
  - `build_live_watcher_status(paths)`
  - `build_live_watcher_process_status(paths)`
  - `build_live_sqlite_capture_status(paths)`
- Added stable response identity:
  - `object = mythic_edge_local_app_live_watcher_diagnostics`
  - `schema_version = live_app_watcher_diagnostics.v1`
  - `mode = read_only_composition`
- Added diagnostic categories:
  - `player_log_metadata`
  - `watcher_readiness`
  - `watcher_process`
  - `live_capture`
  - `tailer_event_bridge`
  - `parser_evidence`
  - `privacy_boundary`
- Added source summaries for the composed and deferred sources.
- Added explicit privacy and capability booleans that fail closed to safe values.
- Added canonical Player.log label mapping so older metadata shorthand labels
  such as `stale`, `not_file`, `permission_denied`, and `metadata_unavailable`
  are exposed as contract-approved safe diagnostic labels.
- Added `GET /api/live/watcher/diagnostics` in
  `src/mythic_edge_parser/local_app/backend.py`.

### Backend Tests

- Extended `tests/test_analytics_local_app_backend.py` so the diagnostics route
  is included in the GET-route no-artifact check.
- Added assertions for required object/schema/mode, privacy flags, capability
  flags, source summaries, deferred tailer labels, and privacy boundary labels.
- Added stale Player.log metadata coverage that confirms the route reports a
  warning without exposing raw paths or file contents.
- Added malformed watcher state coverage that confirms malformed state is
  reported, not repaired, and raw paths are not exposed.
- Added a source guard test that checks the diagnostics helper source does not
  call runner, stream/tailer polling/startup, parser diagnostics report builders,
  or Player.log drift report builders.

### Frontend

- Added diagnostics constants and response types in `frontend/src/types.ts`.
- Added `fetchLiveWatcherDiagnosticsStatus(...)` and fail-closed validation in
  `frontend/src/api.ts`.
- Added independent live diagnostics state loading in `frontend/src/App.tsx`.
- Added a read-only `LiveDiagnosticsPanel` in `frontend/src/App.tsx`.
- The panel shows summary counts, privacy/capability status, and a bounded
  diagnostics preview using existing safe display helpers.
- No start, stop, restart, clear, repair, reset, delete, SQL, import, Sheets,
  AI, or remediation controls were added.

### Frontend Tests

- Added API validation coverage in `frontend/src/api.test.ts`.
- Added fail-closed diagnostics validation for unsafe capability flags and
  incompatible schema versions.
- Added rendering coverage in `frontend/src/App.test.tsx` for a safe read-only
  diagnostics summary.
- Added rendering coverage for diagnostics API errors without raw backend
  details.
- Updated existing live watcher process fixtures to reflect that #244 live
  SQLite ingest contract support is now present on this branch.

## Code Changed

Yes. Runtime code changed only inside the local app/backend and local frontend
diagnostics display surfaces:

- local backend route/helper;
- local frontend typed API reader and read-only panel.

No parser, parser state final reconciliation, event classes, match/game identity,
deduplication, analytics schema/migrations, workbook, webhook, Apps Script,
Sheets, OpenAI/AI/coaching, or production behavior was changed.

## Tests Added Or Updated

- `tests/test_analytics_local_app_backend.py`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`

## Interface Changes

Added one local app read-only backend route:

```text
GET /api/live/watcher/diagnostics
```

Added one frontend API reader:

```ts
fetchLiveWatcherDiagnosticsStatus(...)
```

Added one TypeScript response contract:

```ts
LiveWatcherDiagnosticsResponse
```

No POST/PUT/PATCH/DELETE watcher routes were added. No environment variables,
workbook columns, webhook payload fields, Apps Script entrypoints, SQLite
schema/migration files, or parser interfaces were changed.

## Contracted Area Status

The implementation stayed inside Local App / Live Player.log Mode and its
frontend status display bridge. Downstream parser, analytics schema, workbook,
webhook, Apps Script, Sheets, AI, and production boundaries were not touched.

## Generated/Private Artifact Status

No generated SQLite files, WAL/SHM/journal files, diagnostics files, runtime
status files, logs, watcher state files, local JSONL artifacts, raw Player.log
fixtures, frontend build output, secrets, credentials, or local-only artifacts
were created or committed by the implementation.

## Protected-Surface Status

No protected parser/runtime/workbook/webhook/App Script/Sheets/AI/production
surface was intentionally changed. Final protected-surface validation is listed
below.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_tailer.py tests\test_parser_diagnostics_mode.py tests\test_evidence_runtime_status.py
npm --prefix frontend test -- --run api.test.ts App.test.tsx
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run
py -m ruff check src tests tools
py tools\check_agent_docs.py
py tools\check_secret_patterns.py --all
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
@'
docs/contracts/live_app_watcher_diagnostics.md
docs/implementation_handoffs/live_app_watcher_diagnostics_comparison.md
src/mythic_edge_parser/local_app/live_watcher_diagnostics.py
src/mythic_edge_parser/local_app/backend.py
tests/test_analytics_local_app_backend.py
frontend/src/types.ts
frontend/src/api.ts
frontend/src/App.tsx
frontend/src/api.test.ts
frontend/src/App.test.tsx
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/live_app_watcher_diagnostics.md
docs/implementation_handoffs/live_app_watcher_diagnostics_comparison.md
src/mythic_edge_parser/local_app/live_watcher_diagnostics.py
src/mythic_edge_parser/local_app/backend.py
tests/test_analytics_local_app_backend.py
frontend/src/types.ts
frontend/src/api.ts
frontend/src/App.tsx
frontend/src/api.test.ts
frontend/src/App.test.tsx
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
direct trailing-whitespace, final-newline, and ASCII checks for new untracked files
git diff --check
```

Results:

- `git status --short --branch --untracked-files=all` -> branch
  `codex/analytics-foundation`; expected modified implementation/test/frontend
  files and untracked #246 contract, handoff, and diagnostics helper.
- `py -m pytest -q tests\test_analytics_local_app_backend.py` -> passed,
  18 passed, 1 existing FastAPI/Starlette deprecation warning.
- `py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_tailer.py tests\test_parser_diagnostics_mode.py tests\test_evidence_runtime_status.py`
  -> passed, 43 passed.
- `npm --prefix frontend test -- --run api.test.ts App.test.tsx` -> passed,
  2 files and 65 tests.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend test -- --run` -> passed, 3 files and 68 tests.
- `py -m ruff check src tests tools` -> passed after wrapping three long
  diagnostic message strings.
- `py tools\check_agent_docs.py` -> passed.
- `py tools\check_secret_patterns.py --all` -> failed on pre-existing all-repo
  advisory findings outside this slice; no #246 touched-path finding was
  identified by the path-scoped rerun.
- Path-scoped secret/private-marker scan over the 10 touched #246 paths ->
  passed, forbidden 0, warnings 0.
- `py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation`
  -> passed with changed_paths 0 because untracked files are outside the base
  diff.
- Path-scoped protected-surface scan over the 10 touched #246 paths -> passed,
  forbidden 0, warnings 0.
- Direct trailing-whitespace, final-newline, and ASCII checks for the new
  untracked files -> passed.
- `git diff --check` -> passed.

## Still Unverified

- Real private `Player.log` watcher behavior; this pass deliberately did not
  read, tail, hash, or inspect real log contents.
- Actual supervised watcher process operation; no process control was added.
- Sanitized upstream parser/evidence health source integration; this remains
  deferred unless a future contract supplies an authorized source.
- Live browser smoke against a running local app.
- Live workbook state, deployed Apps Script state, Google Sheets behavior, and
  production behavior.

## Reviewer Focus

Codex E should pay special attention to:

- whether `GET /api/live/watcher/diagnostics` is the only new watcher
  diagnostics route;
- whether the helper composes existing sanitized status builders only;
- whether privacy/capability booleans prove no raw Player.log content, raw
  paths, raw hashes, SQL, stack traces, secrets, writes, tailing, watcher
  starts/stops, or external transport are exposed;
- whether stale/malformed watcher state is reported without repair;
- whether frontend API validation fails closed on unsafe capabilities or schema
  mismatch;
- whether the frontend panel exposes no destructive or remediation controls;
- whether #244 live capture semantics and protected parser/runtime/workbook
  surfaces remain unchanged.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #246.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/246

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_watcher_diagnostics.md

Implementation handoff:
docs/implementation_handoffs/live_app_watcher_diagnostics_comparison.md

Goal:
Review the Codex C implementation of the read-only live watcher diagnostics surface against the contract. Lead with findings. Verify that the new diagnostics route and frontend panel stay sanitized, read-only, non-destructive, and do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.

Review focus:
- Confirm `GET /api/live/watcher/diagnostics` is the only new watcher diagnostics route.
- Confirm the backend helper composes only existing sanitized status builders and does not call runner, stream/tailer startup or polling, parser diagnostics report builders, or Player.log drift report builders.
- Confirm raw Player.log content, raw paths, raw hashes, SQL, stack traces, secrets, command lines, and private local artifacts are not exposed.
- Confirm GET routes do not create SQLite files, WAL/SHM/journal files, diagnostics files, runtime status files, logs, watcher state files, or generated app-data artifacts.
- Confirm stale/malformed watcher state is reported, not repaired.
- Confirm frontend API validation fails closed for unsafe capabilities and incompatible schema versions.
- Confirm the frontend panel is read-only and exposes no start/stop/restart/clear/delete/repair/reset/remediation controls.
- Confirm #244 live parser-owned fact capture semantics remain unchanged.

Validation to run:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_tailer.py tests\test_parser_diagnostics_mode.py tests\test_evidence_runtime_status.py
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
py -m ruff check src tests tools
py tools\check_agent_docs.py
py tools\check_secret_patterns.py --all
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
git diff --check

Do not:
- Start, stop, restart, kill, inspect, or control a watcher process.
- Read, copy, hash, tail, store, or expose raw Player.log content.
- Generate parser diagnostics reports against live/private logs.
- Add destructive/remediation controls.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations, #244 live capture semantics, manual import semantics, replay ingest semantics, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, AI/OpenAI/model-provider behavior, Line Tracer, coaching, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice.
- Stage, commit, push, open a PR, merge, close issue #246, or mark tracker #204 complete unless explicitly asked.

Final review report must include:
- role performed
- issue/tracker/umbrella reviewed
- contract and handoff reviewed
- findings first, ordered by severity
- validation run and result
- protected-surface status
- secret/private-marker status
- generated/private artifact status
- whether forbidden scope was touched
- whether this should route to Codex D, Codex B, or Codex F
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/246"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/live_app_watcher_diagnostics.md"
  target_artifact: "docs/implementation_handoffs/live_app_watcher_diagnostics_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch --untracked-files=all -> expected modified/untracked #246 files on codex/analytics-foundation"
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py -> passed, 18 passed, 1 existing warning"
    - "py -m pytest -q tests\\test_live_app_parser_owned_fact_capture_sqlite.py tests\\test_tailer.py tests\\test_parser_diagnostics_mode.py tests\\test_evidence_runtime_status.py -> passed, 43 passed"
    - "npm --prefix frontend test -- --run api.test.ts App.test.tsx -> passed, 65 tests"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend test -- --run -> passed, 68 tests"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "py tools\\check_secret_patterns.py --all -> failed on pre-existing all-repo advisory findings outside this slice"
    - "path-scoped secret/private-marker scan over touched #246 paths -> passed, forbidden 0, warnings 0"
    - "py tools\\check_protected_surfaces.py --base origin/codex/analytics-foundation -> passed with changed_paths 0"
    - "path-scoped protected-surface scan over touched #246 paths -> passed, forbidden 0, warnings 0"
    - "direct trailing-whitespace/final-newline/ASCII checks for new untracked files -> passed"
    - "git diff --check -> passed"
  stop_conditions:
    - "Do not start, stop, restart, kill, inspect, or control a watcher process."
    - "Do not read, copy, hash, tail, store, or expose raw Player.log content."
    - "Do not generate parser diagnostics reports against live/private logs."
    - "Do not create local/generated/private/runtime artifacts from diagnostics GET routes."
    - "Do not expose destructive/remediation controls."
    - "Do not change parser/runtime/analytics schema/#244 capture/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
