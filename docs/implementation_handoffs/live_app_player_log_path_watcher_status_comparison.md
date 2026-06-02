# Live App Player.log Path And Watcher Status Implementation Comparison

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/240>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/204>

## Umbrella Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/207>

## Contract

`docs/contracts/live_app_player_log_path_watcher_status.md`

## Internal Project Area

Local app / UI.

## Truth Owner

Parser/state remains the truth owner for parser-managed facts, event
interpretation, match/game identity, and final reconciliation. This slice only
adds local app readiness/status reporting and browser display.

## Bridge-Code Status

`bridge_code`

The new status surfaces bridge local app config/path metadata into a
browser-visible readiness panel. They do not own parser truth, analytics truth,
workbook truth, deployment truth, or AI/coaching truth.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Artifacts Used

- GitHub issue #240
- tracker #204
- umbrella issue #207
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/live_app_player_log_path_watcher_status.md`

## Current Behavior Compared To Contract

Current repo behavior before this pass:

- `build_player_log_path_status()` reported coarse configured/detected/missing
  Player.log state.
- `/api/app/setup-status` exposed setup sections and runtime status.
- `/api/runtime/status` exposed `live_watcher: deferred`.
- The frontend displayed setup-status panels and a hardcoded deferred Live
  Watcher panel.
- Existing tests already checked some symbolic path and no-body-read behavior.

Contract gaps:

- No dedicated `GET /api/live/player-log/status`.
- No dedicated `GET /api/live/watcher/status`.
- Player.log status lacked source, path kind, metadata access, existence,
  metadata-only activity fields, diagnostics, warnings, and errors.
- Watcher readiness did not map Player.log blockers to readiness-only status.
- Frontend did not display backend-provided live readiness.
- Frontend API helpers did not validate the new live status response shapes.

## Implementation Option Chosen

Implemented the narrow read-only status surface authorized by the contract:

- metadata-only backend helpers using `Path.stat()` and mode checks;
- two new FastAPI GET routes under `/api/live/...`;
- backward-compatible setup-status aggregate additions:
  - `live_player_log`
  - `live_watcher`
- frontend typed response shapes and API helpers for direct route access;
- frontend setup-status display panels for `Live Player.log` and
  `Live Watcher` from the aggregate live sections;
- focused backend and frontend tests.

No watcher process control, parser runner calls, file tailing, raw log reads,
config writes, SQLite live ingest, workbook/webhook/App Script/Sheets/AI, or
production behavior was added.

## Files Changed

- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_local_app_config.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/status.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `frontend/src/status.test.ts`
- `docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md`

Untracked source contract present from Codex B:

- `docs/contracts/live_app_player_log_path_watcher_status.md`

## Exact Sections Changed

Backend:

- Added live status constants and metadata dataclasses in
  `local_app/setup_status.py`.
- Added `build_live_player_log_status(paths)`.
- Added `build_live_watcher_status(paths)`.
- Updated `build_player_log_path_status(paths)` to reuse live Player.log
  metadata while preserving the existing setup-status section object/schema.
- Extended `build_setup_status(paths)` with `live_player_log` and
  `live_watcher`.
- Added route handlers for:
  - `GET /api/live/player-log/status`
  - `GET /api/live/watcher/status`

Frontend:

- Added live status constants and response types in `frontend/src/types.ts`.
- Added `LiveStatusApiError`, `fetchLivePlayerLogStatus()`,
  `fetchLiveWatcherStatus()`, and validators in `frontend/src/api.ts`.
- Replaced the hardcoded deferred Live Watcher panel with backend-provided
  setup aggregate panels in `frontend/src/App.tsx`.
- Added `ready`, `running`, `blocked_*`, `not_configured`, and `stopped`
  status-tone mappings in `frontend/src/status.ts`.

Tests:

- Added backend metadata/readiness tests in
  `tests/test_analytics_local_app_config.py`.
- Added backend route/no-artifact/readiness-only tests in
  `tests/test_analytics_local_app_backend.py`.
- Added frontend API helper tests in `frontend/src/api.test.ts`.
- Added frontend live panel/redaction tests in `frontend/src/App.test.tsx`.
- Added status-tone vocabulary tests in `frontend/src/status.test.ts`.

## Code Changed

Yes.

Runtime behavior changed only for the local app backend GET status surface and
frontend display. Parser runtime, parser state, tailer behavior, analytics
schema/ingest, workbook/webhook/App Script/Sheets, OpenAI/AI/coaching, and
production behavior were not changed.

## Tests Added Or Updated

Yes.

Focused backend and frontend tests were added/updated for:

- configured existing Player.log metadata with symbolic path only;
- configured missing Player.log;
- configured directory/not-file path;
- invalid `player_log_path` shape;
- app-data root unavailable;
- monkeypatched default Player.log detection;
- read-only live endpoint inventory;
- no local app artifacts created by GET status routes;
- watcher readiness-only flags;
- frontend live status rendering;
- frontend raw-path redaction;
- frontend API shape validation and malformed response handling;
- status-tone mapping for watcher readiness vocabulary.

## Interface Changes

Added local app read-only backend endpoints:

```text
GET /api/live/player-log/status
GET /api/live/watcher/status
```

Added setup-status aggregate sections:

```text
live_player_log
live_watcher
```

No existing setup-status fields were removed or renamed.

Added frontend API helpers:

```text
fetchLivePlayerLogStatus()
fetchLiveWatcherStatus()
```

No workbook columns, webhook payload fields, parser event classes, parser
output rows, environment variables, CI gates, or production entrypoints were
changed.

## Contracted Area Status

Stayed inside the contracted local app / UI area.

The implementation uses parser runtime/tailer files only as boundaries by not
calling them. It does not start `runner.main()`, `MtgaEventStream.start(...)`,
or `FileTailer.open_from_end(...)`.

## Validation Run

Completed before writing this handoff:

```text
git status --short --branch --untracked-files=all -> branch codex/analytics-foundation, only Codex B contract untracked before edits
gh issue view 240 --json number,title,state,body,url,labels -> issue #240 OPEN
gh issue view 204 --json number,title,state,url -> tracker #204 OPEN
gh issue view 207 --json number,title,state,url -> umbrella #207 OPEN
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py -> 29 passed, 1 StarletteDeprecationWarning
npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts -> 65 passed
py -m pytest -q tests\test_runner.py tests\test_tailer.py -> 26 passed
npm --prefix frontend run typecheck -> passed
py -m ruff check src tests -> passed after one line-length fix
npm --prefix frontend run build -> passed; generated frontend/dist removed afterward
```

Completed after writing this handoff:

```text
git diff --check -> passed
py tools\check_agent_docs.py -> passed, errors 0, warnings 0
path-scoped protected-surface scan over touched files -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan over touched files -> passed, forbidden 0, warnings 0
untracked doc whitespace/ascii/final-newline check -> passed
generated frontend/dist status check -> not present
generated SQLite/WAL/SHM artifact status check -> no matches
git status --short --branch --untracked-files=all -> branch codex/analytics-foundation with expected modified source/test files and untracked contract/handoff docs
```

## Protected-Surface Status

No parser behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema/migrations/ingest/views,
Match Journal write semantics, workbook schema, webhook payload shape, Apps
Script behavior, Google Sheets behavior, output transport, production
behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer,
hidden-card inference, archetype inference, player-mistake labels, or gameplay
advice was changed.

## Secret / Private Marker Status

The implementation returns symbolic display paths only:

- `<configured_player_log>`
- `<detected_mtga_player_log>`
- `<player_log_unavailable>`

No raw Player.log contents, raw log lines, raw absolute paths, environment
values, secrets, webhook URLs, spreadsheet IDs, generated SQLite files,
runtime status files, failed posts, or workbook exports were added.

## Generated Artifact Status

`npm --prefix frontend run build` created `frontend/dist`; it was removed after
the build validation. No generated build output is intended to remain in the
worktree.

## Still Unverified

- Real local MTGA Player.log permission-denied behavior on a protected file.
- Real default Windows Player.log state on the user's app-data root.
- Live watcher process-control behavior, intentionally out of scope.
- Live Player.log capture and parser-owned fact writes to SQLite, intentionally
  out of scope.
- Live workbook state.
- Deployed Apps Script state.
- Production behavior.

## Reviewer Focus

Codex E should check:

- whether the setup-status aggregate use of `live_player_log` / `live_watcher`
  satisfies the frontend display contract alongside direct API helpers;
- whether metadata-only `Path.stat()` behavior is narrow enough for the
  contract;
- whether stale/activity metadata should be warning-level now or deferred;
- whether default Player.log detection should produce `detected_missing` as
  implemented when the default path is absent;
- whether the frontend title `Live Player.log` is acceptable safe display text.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #240.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/240

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_player_log_path_watcher_status.md

Implementation handoff:
docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md

Goal:
Review the implementation against the contract. Verify that the local app adds
only read-only Player.log path status and watcher readiness status, with safe
frontend display and focused tests.

Review these changed files:
- src/mythic_edge_parser/local_app/setup_status.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_local_app_config.py
- tests/test_analytics_local_app_backend.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/App.tsx
- frontend/src/status.ts
- frontend/src/api.test.ts
- frontend/src/App.test.tsx
- frontend/src/status.test.ts
- docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md
- docs/contracts/live_app_player_log_path_watcher_status.md

Pay special attention to:
- no raw absolute paths or raw Player.log contents returned/rendered;
- no calls to runner.main(), MtgaEventStream.start(), or FileTailer.open_from_end();
- no watcher start/stop controls or destructive UI actions;
- no config writes, SQLite live ingest, generated artifacts, runtime status writes, or parser behavior changes;
- direct live API helpers and setup aggregate live sections matching the contract;
- watcher readiness-only fields staying false/non-controlling;
- frontend redaction and malformed live-status handling;
- focused tests covering required contract cases.

Suggested validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts
py -m pytest -q tests\test_runner.py tests\test_tailer.py
npm --prefix frontend run typecheck
py -m ruff check src tests
git diff --check
path-scoped protected-surface scan over touched files
path-scoped secret/private-marker scan over touched files

Do not:
- edit code in review mode unless explicitly asked;
- target main;
- start or stop a live watcher;
- tail, read, copy, hash, or store raw Player.log contents;
- expose raw absolute paths, secrets, environment values, or private artifacts;
- change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior;
- stage, commit, push, open a PR, merge, close #240, or mark tracker #204 complete unless explicitly asked.

Final output:
- findings first, ordered by severity;
- verdict against the contract;
- validation run and result;
- protected-surface status;
- secret/private-marker status;
- remaining risks or unverified layers;
- next recommended role;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/240"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "GitHub issue #240 and docs/contracts/live_app_player_log_path_watcher_status.md"
  target_artifact: "docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md"
  contract_artifact: "docs/contracts/live_app_player_log_path_watcher_status.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_analytics_local_app_config.py tests\\test_analytics_local_app_backend.py -> 29 passed, 1 StarletteDeprecationWarning"
    - "npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts -> 65 passed"
    - "py -m pytest -q tests\\test_runner.py tests\\test_tailer.py -> 26 passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "py -m ruff check src tests -> passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed afterward"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan over touched files -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over touched files -> passed, forbidden 0, warnings 0"
    - "untracked doc whitespace/ascii/final-newline check -> passed"
    - "generated frontend/dist and SQLite artifact status checks -> no generated artifacts present"
  stop_conditions:
    - "Do not target main."
    - "Do not start or stop a live watcher."
    - "Do not tail, read, copy, hash, or store raw Player.log contents."
    - "Do not expose raw absolute paths, secrets, environment values, or private artifacts."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
