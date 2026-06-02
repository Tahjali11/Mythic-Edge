# Live App Player.log Watcher Process-Control Safeguards Implementation Comparison

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/242>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/204>

## Umbrella Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/207>

## Contract

`docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`

## Internal Project Area

Local app / UI.

## Truth Owner

Parser/state remains the truth owner for parser-managed facts, event
interpretation, match/game identity, and final reconciliation. This slice only
adds local app process-control safeguards and browser-visible status metadata.

## Bridge-Code Status

`bridge_code`

The new process status surface bridges local app readiness metadata, an
app-owned synthetic state marker, and frontend display. It does not own parser
truth, analytics truth, workbook truth, deployment truth, or AI/coaching truth.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Artifacts Used

- GitHub issue #242
- tracker #204
- umbrella issue #207
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`
- issue #240 contract and implementation handoff for prerequisite live status

## Current Behavior Compared To Contract

Current repo behavior before this pass:

- `GET /api/live/player-log/status` reported metadata-only Player.log status.
- `GET /api/live/watcher/status` reported readiness-only watcher status.
- `/api/app/setup-status` included `live_player_log` and `live_watcher`.
- The frontend displayed live Player.log and watcher readiness without controls.
- No local app watcher supervisor, process-state status surface, or
  single-instance guard status existed.

Contract gaps:

- No `GET /api/live/watcher/process` endpoint.
- No process-control safeguards object or schema version.
- No process-control status flags proving start/stop/UI/runner/tailer/live
  SQLite/external transport were disabled.
- No app-owned synthetic state marker classification for missing, malformed, or
  stale state.
- No frontend process-control display panel.
- No tests proving POST start/stop routes are absent or unsupported.
- No tests proving process status does not call runner or tailer entrypoints.

## Implementation Option Chosen

Implemented the narrow read-only safeguards path authorized by the contract:

- added a local app process-status builder for
  `mythic_edge_local_app_live_watcher_process_status`;
- added one GET-only route: `GET /api/live/watcher/process`;
- included `live_watcher_process` in setup status for frontend display;
- added frontend types, API validation, and a display-only process panel;
- added focused backend and frontend tests for disabled controls, raw-path
  redaction, state failure modes, absent POST controls, and forbidden runner or
  tailer calls.

No start/stop route, process supervisor, parser runner invocation, tailer
startup, Player.log content read, live SQLite write, workbook/webhook/App
Script/Sheets/OpenAI/AI/coaching/production behavior, or generated artifact was
added.

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`
- `docs/contracts/live_app_player_log_path_watcher_status.md`
- `docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/config.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/log/tailer.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/status.ts`
- `frontend/src/types.ts`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/status.test.ts`

## Files Changed

- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/status.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `frontend/src/status.test.ts`
- `docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md`

Untracked source contract from Codex B:

- `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`

## Exact Sections Changed

Backend:

- Added `live_watcher_process.py` with:
  - process-control object/schema constants;
  - `build_live_watcher_process_status(paths)`;
  - metadata-only state-file classification for missing, malformed, stale, and
    deferred synthetic state;
  - required process-control flags, all false;
  - required preconditions map;
  - sanitized player-log summary;
  - no runner/tailer/process-control imports.
- Added `GET /api/live/watcher/process` in `backend.py`.
- Added `live_watcher_process` to `build_setup_status(paths)` in
  `setup_status.py`.

Frontend:

- Added `LIVE_WATCHER_PROCESS_OBJECT` and
  `LIVE_WATCHER_PROCESS_SCHEMA_VERSION` in `types.ts`.
- Added process-control response types in `types.ts`.
- Added `fetchLiveWatcherProcessStatus()` and validation in `api.ts`.
- Added display-only `Live Watcher Process` panel in `App.tsx`.
- Extended `statusTone()` mappings for `not_initialized`, `blocked`, `stale`,
  `crashed`, and `orphaned`.

Tests:

- Backend route inventory includes `/api/live/watcher/process`.
- Backend GET no-artifact loop includes `/api/live/watcher/process`.
- Backend route tests assert every process-control flag is false.
- Backend tests assert missing Player.log maps to `blocked_missing_log`.
- Config/status tests assert missing state is non-running, malformed state fails
  closed, stale synthetic state stays non-running, and raw paths/log bodies do
  not leak.
- Static regression test asserts process-status code does not reference runner
  or tailer entrypoints.
- Frontend API tests validate the process response and reject enabled controls.
- Frontend app tests render the process panel and continue rejecting start/stop
  or destructive controls.
- Frontend status tests cover the new vocabulary.

## Code Changed

Yes.

Runtime code changed only for local app backend GET status and frontend display.
The route is read-only and no behavior outside the contracted local app / UI
area was changed.

## Tests Changed

Yes.

Focused backend and frontend tests were added/updated for the contracted status
shape, failure modes, and no-control boundaries.

## Interface Changes

Added local app read-only backend endpoint:

```text
GET /api/live/watcher/process
```

Added setup-status aggregate section:

```text
live_watcher_process
```

Added frontend API helper:

```text
fetchLiveWatcherProcessStatus()
```

No workbook columns, webhook payload fields, parser event classes, parser
output rows, environment variables, CI gates, or production entrypoints were
changed.

## Validation Run

```text
git status --short --branch --untracked-files=all -> branch codex/analytics-foundation, only #242 contract untracked before edits
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0
gh issue view 242 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body -> OPEN
gh issue view 204 --repo Tahjali11/Mythic-Edge --json number,title,state,url -> OPEN
gh issue view 207 --repo Tahjali11/Mythic-Edge --json number,title,state,url -> OPEN
py -m pytest -q tests\test_analytics_local_app_backend.py -> 15 passed, 1 StarletteDeprecationWarning
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_runner.py tests\test_tailer.py -> 45 passed
npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts -> 65 passed
npm --prefix frontend run typecheck -> passed
npm --prefix frontend run build -> passed; frontend/dist removed afterward
py -m ruff check src tests tools -> passed
```

Final hygiene scans after writing this handoff:

```text
git diff --check -> passed
py tools\check_agent_docs.py -> passed, errors 0, warnings 0
path-scoped protected-surface scan over touched files -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan over touched files -> passed, forbidden 0, warnings 0
generated artifact status check -> frontend/dist absent, no SQLite/WAL/SHM artifacts found
git status --short --branch --untracked-files=all -> expected modified source/test files plus untracked contract, handoff, and new local_app module
```

## Protected-Surface Status

No parser behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema/migrations/ingest/views,
Match Journal truth ownership, workbook schema, webhook payload shape, Apps
Script behavior, Google Sheets behavior, output transport, production behavior,
OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer,
hidden-card inference, archetype inference, player-mistake labels, gameplay
advice, or global CORS policy was changed.

## Secret / Private Marker Status

The process-status payload returns symbolic app paths only, such as:

```text
<app_data>\jobs\live_watcher_state.json
```

No raw Player.log contents, raw log lines, raw absolute paths, environment
values, secrets, webhook URLs, spreadsheet IDs, generated SQLite files, runtime
status files, failed posts, or workbook exports were added.

## Generated Artifact Status

`npm --prefix frontend run build` created `frontend/dist`; it was removed after
build validation. No generated build output or SQLite artifact is intended to
remain in the worktree.

## Forbidden Scope Status

Forbidden scope was not touched.

Specifically:

- no watcher start/stop/restart route was added;
- no process was spawned or killed;
- no runner/tailer entrypoint was called;
- no raw Player.log content was read, tailed, copied, hashed, stored, or
  exposed;
- no browser start/stop controls were exposed;
- no live parser facts were written to SQLite;
- no external transport was enabled.

## Still Unverified

- Real private Player.log behavior on the user's actual machine/app-data root.
- Real process supervisor behavior, intentionally deferred.
- Actual start/stop controls, intentionally absent.
- Live Player.log capture and live SQLite ingest, intentionally deferred.
- Live workbook state.
- Deployed Apps Script state.
- Production behavior.

## Reviewer Focus

Codex E should pay special attention to:

- whether `GET /api/live/watcher/process` fully matches the contract schema and
  status vocabulary;
- whether the state-file read is acceptable for synthetic app-owned test state
  and does not create files/folders;
- whether `not_initialized`, `blocked`, `stale`, and `deferred` mappings are
  contract-safe;
- whether all process-control flags are false in backend and frontend
  validation;
- whether setup-status aggregation is acceptable for frontend display;
- whether the static runner/tailer no-call test is enough contract evidence;
- whether any secret/private marker warnings are policy wording rather than
  actual leaks.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #242.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/242

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_player_log_watcher_process_control_safeguards.md

Implementation handoff:
docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md

Goal:
Review the implementation against the contract. Verify that the local app adds
only read-only watcher process-control safeguards/status and does not add
watcher start/stop behavior, parser runner/tailer calls, raw Player.log reads,
live SQLite writes, or destructive/browser process controls.

Review these changed files:
- src/mythic_edge_parser/local_app/live_watcher_process.py
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/setup_status.py
- tests/test_analytics_local_app_backend.py
- tests/test_analytics_local_app_config.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/App.tsx
- frontend/src/status.ts
- frontend/src/api.test.ts
- frontend/src/App.test.tsx
- frontend/src/status.test.ts
- docs/contracts/live_app_player_log_watcher_process_control_safeguards.md
- docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md

Pay special attention to:
- GET /api/live/watcher/process object/schema/status shape;
- all process-control flags remaining false;
- POST /api/live/watcher/start and /api/live/watcher/stop absent or unsupported;
- malformed and stale synthetic state failing closed;
- no raw local paths, Player.log contents, raw command lines, env values, secrets, or private artifacts exposed;
- no runner.main(), MtgaEventStream.start(...), FileTailer.open_from_*, or tailer polling calls;
- frontend display has no clickable start/stop controls and rejects enabled-control payloads;
- no parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed.

Suggested validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_runner.py tests\test_tailer.py
npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
path-scoped protected-surface scan over touched files
path-scoped secret/private-marker scan over touched files
generated artifact status check

Do not:
- edit code in review mode unless explicitly asked;
- target main;
- start or stop a live watcher;
- tail, read, copy, hash, or store raw Player.log contents;
- expose raw absolute paths, secrets, environment values, or private artifacts;
- change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior;
- stage, commit, push, open a PR, merge, close #242, or mark tracker #204 complete unless explicitly asked.

Final output:
- findings first, ordered by severity;
- verdict against the contract;
- validation run and result;
- protected-surface status;
- secret/private-marker status;
- generated artifact status;
- remaining risks or unverified layers;
- next recommended role;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/242"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "GitHub issue #242 and docs/contracts/live_app_player_log_watcher_process_control_safeguards.md"
  target_artifact: "docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md"
  contract_artifact: "docs/contracts/live_app_player_log_watcher_process_control_safeguards.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py -> 15 passed, 1 StarletteDeprecationWarning"
    - "py -m pytest -q tests\\test_analytics_local_app_config.py tests\\test_runner.py tests\\test_tailer.py -> 45 passed"
    - "npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts -> 65 passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed afterward"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan over touched files -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over touched files -> passed, forbidden 0, warnings 0"
    - "generated artifact status check -> frontend/dist absent, no SQLite/WAL/SHM artifacts found"
  stop_conditions:
    - "Do not target main."
    - "Do not start or stop a live watcher."
    - "Do not tail, read, copy, hash, or store raw Player.log contents."
    - "Do not expose raw absolute paths, secrets, environment values, or private artifacts."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
