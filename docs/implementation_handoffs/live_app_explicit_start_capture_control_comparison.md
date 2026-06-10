# Live App Explicit Start Capture Control Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/297

## Tracker

Historical trackers:

- https://github.com/Tahjali11/Mythic-Edge/issues/204
- https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/live_app_explicit_start_capture_control.md`

## Internal Project Area

Local app / live capture control / analytics support.

## Truth Owner

Parser/state remains the owner of event interpretation and final match/game facts. The local app owns only explicit local control state and safe display. SQLite remains a downstream local analytics store, not parser truth.

## Bridge-Code Status

`shared_support`

The implementation bridges local app controls to parser-owned final fact ingest, but does not move truth ownership into the frontend, backend routes, or SQLite.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/live_app_explicit_start_capture_control.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/log/tailer.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_live_app_parser_owned_fact_capture_sqlite.py`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/App.test.tsx`

## Current Behavior Compared To Contract

The repository already had read-only setup, Player.log, watcher readiness, watcher process-safeguard, watcher diagnostics, and live SQLite ingest status surfaces. Those surfaces could say the app was ready, degraded, or not capturing, but could not explicitly start an app-owned capture loop.

The broad parser runner can tail Player.log, but it also owns runtime output and transport surfaces. The contract did not allow wiring that broad runner directly into the local app. The current lower-level stream, parser state, and analytics ingest helpers were sufficient to build a narrower local-app supervisor.

The approved live SQLite ingest boundary already accepts parser-owned final match and game facts through `ingest_live_parser_owned_facts`. The gap was the explicit local control layer that starts a safe supervisor, blocks stale/ambiguous ownership, and exposes frontend controls only when backend flags allow them.

## Implementation Option Chosen

Implemented a new local-app capture supervisor under `src/mythic_edge_parser/local_app/` instead of invoking the broad legacy runner. The supervisor uses `MtgaEventStream`, parser state update/build helpers, and the existing live SQLite ingest adapter for completed parser-owned match/game facts only.

Read-only status stays no-write. State directories, lock files, and SQLite migration/open checks are created only during explicit `POST /api/live/capture/start`.

## Files Changed

- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_live_app_explicit_start_capture_control.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/live_app_explicit_start_capture_control_comparison.md`

Unrelated pre-existing dirty files were preserved and not reverted:

- `docs/contracts/quality_app_submit_error_report_codex_triage.md`
- `src/mythic_edge_parser/local_app/error_reports.py`
- `tests/test_analytics_local_app_backend.py`

Some frontend files already had unrelated local edits from adjacent local-app work; the #297 changes in those files are limited to live capture control types, API calls, display state, styling, and tests.

## Exact Sections Changed

Backend:

- Added `live_capture_control.py` with:
  - `GET` status payload builder for `mythic_edge_local_app_live_capture_status`.
  - explicit `start_live_capture`.
  - bounded `stop_live_capture`.
  - app-data-root-scoped state and lock file helpers.
  - app-owned supervisor registry with supervisor token evidence.
  - stale/ambiguous state blockers.
  - lower-level parser stream loop that writes only completed parser-owned match/game facts through `ingest_live_parser_owned_facts`.
- Added backend routes in `backend.py`:
  - `GET /api/live/capture/status`
  - `POST /api/live/capture/start`
  - `POST /api/live/capture/stop`

Frontend:

- Added live capture status/start/stop response constants and types in `types.ts`.
- Added API wrappers and response validation in `api.ts`.
- Added `LiveCaptureControlPanel`, status derivation, and start/stop handlers in `App.tsx`.
- Added `captureControlPanel` and `captureControlActions` styling in `App.css`.
- Added focused App tests for allowed start, allowed app-owned stop, and blocked ownership control display.

Tests:

- Added `tests/test_live_app_explicit_start_capture_control.py` covering read-only GET, explicit POST start, duplicate start, app-owned stop, missing Player.log block, stale ownership block, and no destructive routes.
- Updated frontend test fixtures/assertions for the new explicit capture-control response shape.

## Code Changed

Yes. Backend and frontend runtime code changed.

The changed behavior is local-only live capture control. It does not change parser event interpretation, parser final reconciliation, analytics schema/migrations, workbook/webhook/App Script/Sheets, output transport, AI/coaching, or production behavior.

## Tests Added Or Updated

- Added `tests/test_live_app_explicit_start_capture_control.py`.
- Updated focused frontend tests in `frontend/src/App.test.tsx`.

## Interface Changes

Added local loopback-only backend route surface:

- `GET /api/live/capture/status`
- `POST /api/live/capture/start`
- `POST /api/live/capture/stop`

Added frontend typed response objects:

- `mythic_edge_local_app_live_capture_status`
- `mythic_edge_local_app_live_capture_start_result`
- `mythic_edge_local_app_live_capture_stop_result`

No workbook columns, webhook payloads, Apps Script interfaces, environment-variable contracts, analytics schema, or parser event interfaces changed.

## Contracted Area Status

The implementation stayed inside the contracted local app live capture control area. Parser/state and analytics ingest helpers are reused as downstream dependencies but not behaviorally changed. Workbook/webhook/App Script/Sheets/output transport and AI/coaching surfaces were not touched.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
# passed; branch codex/analytics-foundation with unrelated pre-existing dirty files plus #297 changes

py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py tests\test_live_app_parser_owned_fact_capture_sqlite.py
# passed: 42 passed, 1 existing FastAPI/Starlette deprecation warning

py -m pytest -q tests\test_runner.py tests\test_tailer.py
# passed: 26 passed

py -m ruff check src tests tools
# passed

npm --prefix frontend run typecheck
# passed

npm --prefix frontend run test -- --run src/App.test.tsx
# passed: 50 passed

npm --prefix frontend run build
# passed; generated frontend/dist was removed before handoff

git diff --check
# passed

py tools\check_agent_docs.py
# passed: errors 0, warnings 0

@'
docs/contracts/live_app_explicit_start_capture_control.md
docs/implementation_handoffs/live_app_explicit_start_capture_control_comparison.md
src/mythic_edge_parser/local_app/live_capture_control.py
src/mythic_edge_parser/local_app/backend.py
tests/test_live_app_explicit_start_capture_control.py
frontend/src/types.ts
frontend/src/api.ts
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed: forbidden 0, warnings 0

@'
docs/contracts/live_app_explicit_start_capture_control.md
docs/implementation_handoffs/live_app_explicit_start_capture_control_comparison.md
src/mythic_edge_parser/local_app/live_capture_control.py
src/mythic_edge_parser/local_app/backend.py
tests/test_live_app_explicit_start_capture_control.py
frontend/src/types.ts
frontend/src/api.ts
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed: forbidden 0, warnings 0
```

## Protected-Surface Status

Final path-scoped protected-surface scan over the #297 touched files passed with forbidden 0 and warnings 0. Implementation intentionally did not change parser behavior, parser state final reconciliation, parser event classes, match/game identity, analytics schema/migrations, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, output transport, AI/coaching, or production behavior.

## Secret/Private-Marker Status

Final path-scoped secret/private-marker scan over the #297 touched files passed with forbidden 0 and warnings 0. The implementation uses symbolic display paths such as `<app_data>` and does not expose raw Player.log content, raw private paths, raw hashes, endpoint values, generated SQLite contents, or app-data files.

## Generated/Private Artifact Status

`npm --prefix frontend run build` created `frontend/dist`; it was removed before handoff. No generated SQLite databases, app-data files, raw logs, private JSONL artifacts, workbook exports, runtime outputs, secrets, or local-only artifacts were committed or intentionally retained in the repo.

## Still Unverified

- No real/private Player.log smoke was run.
- No live browser smoke was run.
- Long-running supervisor behavior was validated through focused mocked-supervisor tests, not an actual MTGA session.
- Issue #294 auto-refresh remains out of scope; analytics views may still need manual refresh after capture writes facts.

## Reviewer Focus

Ask Codex E to focus on:

- Whether the new supervisor path truly avoids broad runner/output transport behavior.
- Whether `start_live_capture` creates state only on explicit POST.
- Whether stale/ambiguous state blocks instead of being cleaned or killed.
- Whether stop is limited to registered app-owned supervisors.
- Whether active `Capturing` requires running, tailing, and SQLite write evidence.
- Whether frontend buttons are visible only when backend flags allow them.
- Whether the response shape is stable enough for the local app without exposing private data.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #297.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/297

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_explicit_start_capture_control.md

Implementation handoff:
docs/implementation_handoffs/live_app_explicit_start_capture_control_comparison.md

Risk tier:
High

Goal:
Review the Codex C implementation against the contract. Lead with findings ordered by severity. Verify that explicit Start capture and bounded app-owned Stop capture are local-only, sanitized, non-destructive, and do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.

Review focus:
- Confirm GET /api/live/capture/status is read-only and does not create app-data state.
- Confirm POST /api/live/capture/start is explicit-only, checks preconditions, blocks stale/ambiguous state, prevents duplicate supervisors, and uses a safe local-app supervisor rather than the broad runner.
- Confirm POST /api/live/capture/stop only stops a verified app-owned supervisor and does not kill/reset/delete/cleanup unrelated state.
- Confirm active Capturing requires supervisor running, tailing started, and SQLite live writes enabled.
- Confirm completed parser-owned match/game facts are the only live facts written, through the approved live ingest adapter.
- Confirm frontend Start capture and Stop capture controls appear only when backend start_allowed/stop_allowed flags allow them.
- Confirm API/UI/tests do not expose raw Player.log content, raw JSONL payloads, raw private paths, raw hashes, secrets, stack traces, generated SQLite contents, app-data files, or local-only artifacts.
- Confirm no destructive controls, automatic start, arbitrary SQL/database browsing, workbook/webhook/App Script/Sheets/output transport, OpenAI/AI/coaching, Line Tracer, hidden-card inference, archetype inference, player-mistake labels, gameplay advice, or production behavior were added.

Validation to run or review:
- git status --short --branch --untracked-files=all
- py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py tests\test_live_app_parser_owned_fact_capture_sqlite.py
- py -m pytest -q tests\test_runner.py tests\test_tailer.py
- py -m ruff check src tests tools
- npm --prefix frontend run typecheck
- npm --prefix frontend run test -- --run src/App.test.tsx
- npm --prefix frontend run build
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files

If npm build creates frontend/dist, remove it before final handoff unless a later contract explicitly authorizes committing it.

Do not stage, commit, push, open a PR, merge, close issue #297, target main, run real/private Player.log smoke, or mutate the real default app-data root unless explicitly asked.

Final output must include:
- findings first, ordered by severity
- contract match/mismatch summary
- validation run and result
- protected-surface status
- secret/private-marker status
- generated/private artifact status
- remaining risks
- whether Codex D is needed or the module can route to Codex F
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/297"
  historical_trackers:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/204"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/live_app_explicit_start_capture_control.md"
  target_artifact: "docs/implementation_handoffs/live_app_explicit_start_capture_control_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  implementation_summary:
    - "Added local loopback-only live capture status/start/stop routes."
    - "Added app-owned local capture supervisor using lower-level stream/state helpers and approved live SQLite ingest."
    - "Added frontend explicit Start capture and bounded Stop capture display/actions behind backend allow flags."
    - "Added focused backend/frontend tests for explicit start, duplicate start, app-owned stop, blocked/stale state, privacy, and no destructive routes."
  validation:
    - "py -m pytest -q tests\\test_live_app_explicit_start_capture_control.py tests\\test_analytics_local_app_backend.py tests\\test_live_app_parser_owned_fact_capture_sqlite.py -> passed, 42 passed, 1 existing warning"
    - "py -m pytest -q tests\\test_runner.py tests\\test_tailer.py -> passed, 26 passed"
    - "py -m ruff check src tests tools -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run src/App.test.tsx -> passed, 50 passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not target main."
    - "Do not run private Player.log smoke or mutate the real default app-data root without explicit approval."
    - "Do not add automatic capture start."
    - "Do not add destructive stop/kill/reset/delete/wipe/import/database controls."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
