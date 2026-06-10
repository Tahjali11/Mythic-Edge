# Live App MTGA Process Detection, Shutdown Lifecycle, And Automation Readiness Gate Contract

## Module

`live_app_mtga_process_detection_shutdown_readiness_gate`

Plain English: this contract defines how Mythic Edge should detect whether MTGA is running on Windows, wait briefly when MTGA disappears, shut down local live capture safely if MTGA does not return, and keep automatic capture startup blocked until a readiness checklist is proven.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/337
- Branch: `codex/live-mtga-process-lifecycle-gate`
- Base branch: `codex/analytics-foundation`
- Risk tier: High
- Role: Codex B / Module Contract Writer

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- GitHub issue #337
- `docs/contracts/live_app_explicit_start_capture_control.md`
- `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`
- `docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md`
- `docs/contracts/live_app_stale_capture_dashboard_recovery.md`
- `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`
- `docs/contracts/live_app_watcher_diagnostics.md`
- `docs/contracts/live_player_log_v1_supported_readiness.md`
- `docs/contracts/analytics_auto_refresh_after_match_completion.md`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- focused live capture, diagnostics, frontend, and local app backend tests

## Tracker

No separate tracker was named in the Codex A handoff. Related release and local-app context appears in prior live-mode issues, but this contract is scoped to issue #337.

## Owning Layer

Primary owning layer: Local App / Live Player.log Mode lifecycle.

Supporting layers:

- backend live capture control owns capture lifecycle state;
- backend MTGA process detection owns only the sanitized process-presence signal;
- backend diagnostics owns safe display of lifecycle evidence;
- parser/state owns event interpretation, match/game identity, final reconciliation, and parser-owned facts;
- analytics/SQLite remains downstream local storage;
- frontend owns display and explicit operator actions only.

## Internal Project Area

Local App / UI, with Live Player.log Mode as the specific sub-area.

Adjacent areas:

- Parser
- Analytics
- Quality / Governance

## Truth Owner

The backend owns the MTGA process-presence signal and reconnect/shutdown lifecycle state.

That signal can say whether a Windows process named `MTGA.exe` was detected by the approved local detector. It does not prove game state, match state, parser correctness, or Player.log contents.

Parser/state remains the truth owner for parser facts. The frontend must not infer MTGA process truth, parser truth, match completion, SQLite write truth, shutdown success, or automation readiness from timers, button state, local storage, or UI state.

## Bridge-Code Status

`bridge_code`

Allowed data flow:

```text
Windows MTGA process metadata-only signal
  -> backend live lifecycle state
  -> diagnostics/capture status response
  -> frontend read-only display and allowed manual controls
```

Forbidden reverse flow:

- frontend display must not start, stop, reset, or clean capture state unless a backend route explicitly authorizes that exact action;
- MTGA process presence must not change parser interpretation;
- MTGA process absence must not delete parser facts or SQLite rows;
- automation readiness labels must not enable auto-start without a future issue, contract, implementation, and review.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/live_app_mtga_process_detection_shutdown_readiness_gate.md`

Future Codex C implementation may touch, subject to comparison and validation:

- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`
- `src/mythic_edge_parser/local_app/backend.py`, only if route wiring is needed
- a new local-app helper such as `src/mythic_edge_parser/local_app/mtga_process_lifecycle.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/status.ts`
- focused backend/frontend tests
- `docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_comparison.md`

Codex C must route back to Codex B before touching parser modules, analytics schema/migrations, workbook/webhook/App Script/Sheets behavior, AI/coaching behavior, production behavior, or automatic startup behavior.

## Observed Current Behavior

Current completed live-mode work provides:

- metadata-only Player.log status;
- read-only watcher readiness and watcher process-safeguard status;
- read-only watcher diagnostics;
- explicit operator-controlled `POST /api/live/capture/start`;
- explicit operator-controlled `POST /api/live/capture/stop`;
- `GET /api/live/capture/status` with heartbeat/progress/no-row diagnostics;
- local SQLite writes for completed parser-owned match/game facts through the approved live ingest boundary;
- Dashboard and Diagnostics display of capture state and analytics refresh state.

Current code does not yet provide:

- a backend-owned Windows `MTGA.exe` process-presence signal;
- a 45-second reconnect window when `MTGA.exe` disappears;
- automatic safe capture shutdown after the reconnect window expires;
- a diagnostics-first MTGA process lifecycle display;
- an automation readiness gate that blocks future auto-start work until all manual and lifecycle proof exists.

Manual capture remains the v1.0 default. Auto-start capture remains out of scope.

## Contract Decision

Use a Windows-only, diagnostics-first lifecycle slice.

Approved first implementation direction:

1. Add a backend-owned Windows `MTGA.exe` process detector.
2. Add sanitized MTGA process lifecycle fields to backend status/diagnostics.
3. When active capture is running and `MTGA.exe` disappears, enter a 45-second reconnect window.
4. If `MTGA.exe` returns during the window, continue capture without unnecessary reset.
5. If `MTGA.exe` does not return before the window expires, perform a safe app-owned capture shutdown and return to a ready/stopped state.
6. Treat Player.log silence while `MTGA.exe` is detected as normal idle time, not failure.
7. Display process lifecycle in Diagnostics first.
8. Record automation readiness as blocked until a future issue and contract explicitly authorize auto-start.

Rejected for this slice:

- automatic capture startup;
- MTGA process launch or termination;
- broad process inspection;
- process command-line, environment, window-title, username, or PID display;
- killing MTGA;
- resetting parser state from process absence alone;
- SQLite schema changes;
- frontend-owned timers as lifecycle truth;
- treating quiet Player.log as capture failure while MTGA is detected;
- Google Sheets, webhook, Apps Script, workbook, production, OpenAI, AI/coaching, Line Tracer, hidden-card, archetype, player-mistake, or gameplay-advice behavior.

## Windows Process Detection Contract

### Supported Platform

This slice is Windows-only.

On non-Windows platforms, the detector must return a safe unsupported status such as:

```json
{
  "status": "unsupported_platform",
  "detected": false,
  "platform": "non_windows",
  "evidence": "not_checked"
}
```

Non-Windows unsupported status must not be treated as proof that MTGA is closed. It should block automation readiness and degrade diagnostics, but it should not stop an already-running test harness unless Codex C explicitly proves that behavior is safe in tests.

### Default Detection Approach

Preferred first implementation: a small local-app helper that uses Python standard library `subprocess.run(...)` to call Windows `tasklist` with an exact image-name filter:

```text
tasklist /FI "IMAGENAME eq MTGA.exe" /NH
```

Required detector rules:

- use a fixed command vector, not shell interpolation;
- use `shell=False`;
- use a short timeout;
- use hidden/no-window behavior where supported;
- inspect only process image-name presence;
- do not request command lines;
- do not request usernames;
- do not request environment variables;
- do not return PID values in API responses;
- do not return raw `tasklist` output in API responses, UI, logs, reports, or committed artifacts;
- expose only safe booleans, labels, counters, timestamps, and error codes.

If `tasklist` is unavailable or fails, return a safe status such as `detector_unavailable` or `unknown`, with sanitized error code only.

Do not add a new third-party dependency for process detection in this slice unless Codex C routes back to Codex B with evidence that stdlib/Windows tooling is insufficient.

### Testability

The detector must be injectable or mockable in tests. Tests must not require real MTGA, real process inspection, or real private Player.log content.

## Backend Public Interface

### Existing Routes To Preserve

Existing routes must remain compatible:

```text
GET /api/live/player-log/status
GET /api/live/watcher/status
GET /api/live/watcher/process
GET /api/live/watcher/diagnostics
GET /api/live/capture/status
POST /api/live/capture/start
POST /api/live/capture/stop
GET /api/analytics/refresh-state
```

### Route Decision

Do not add a new route in the first implementation unless Codex C proves the existing status/diagnostics routes cannot safely carry the new fields.

Preferred additive placement:

- add a sanitized `mtga_process` object to `GET /api/live/watcher/process`;
- include the same source summary in `GET /api/live/watcher/diagnostics`;
- add a sanitized `mtga_lifecycle` object to `GET /api/live/capture/status` when capture state is involved.

This keeps process presence in Diagnostics first while giving live capture enough backend-owned state to perform reconnect and shutdown.

### `mtga_process` Shape

Recommended backend shape:

```json
{
  "object": "mythic_edge_local_app_mtga_process_status",
  "schema_version": "live_app_mtga_process_detection_shutdown_readiness_gate.v1",
  "status": "detected",
  "detected": true,
  "platform": "windows",
  "process_name": "MTGA.exe",
  "evidence": "image_name_match",
  "checked_at": "2026-06-10T12:00:00Z",
  "detector": "windows_tasklist_image_name",
  "warnings": [],
  "errors": [],
  "privacy": {
    "pid_exposed": false,
    "command_line_exposed": false,
    "environment_exposed": false,
    "raw_detector_output_exposed": false
  }
}
```

Allowed `mtga_process.status` values:

- `detected`
- `not_detected`
- `unsupported_platform`
- `detector_unavailable`
- `unknown`

Allowed `evidence` values:

- `image_name_match`
- `image_name_absent`
- `not_checked`
- `detector_error`
- `unsupported_platform`

`process_name` must be exactly `MTGA.exe` for this slice. Do not make process names user-configurable in issue #337.

## Lifecycle State Vocabulary

Use this backend-owned lifecycle vocabulary:

- `ready_to_start`: capture is not running and backend preconditions allow manual start.
- `starting`: app-owned capture start is in progress.
- `capturing`: app-owned capture is running and MTGA process state is either detected or not required for a current transitional test state.
- `mtga_unavailable`: MTGA is not detected and no reconnect window is currently active.
- `reconnect_window`: MTGA disappeared while capture was running, and the 45-second reconnect timer has not expired.
- `shutting_down`: backend has begun safe shutdown after the reconnect window expired or a user stop was accepted.
- `stopped`: app-owned capture is stopped.
- `blocked`: capture cannot proceed because a required precondition failed.
- `failed`: a capture or detector error occurred and requires review.
- `unknown`: backend cannot classify lifecycle state safely.

Existing top-level status strings may remain unchanged for compatibility if Codex C keeps the new lifecycle under `mtga_lifecycle.status`. If Codex C changes the top-level `GET /api/live/capture/status.status` vocabulary, it must update frontend validators and tests in the same implementation.

## `mtga_lifecycle` Shape

Recommended additive shape for `GET /api/live/capture/status`:

```json
{
  "schema_version": "live_app_mtga_process_detection_shutdown_readiness_gate.v1",
  "status": "reconnect_window",
  "mtga_process_status": "not_detected",
  "reconnect_window_seconds": 45,
  "reconnect_started_at": "2026-06-10T12:00:00Z",
  "reconnect_deadline_at": "2026-06-10T12:00:45Z",
  "seconds_remaining": 30,
  "shutdown_reason": null,
  "last_detected_at": "2026-06-10T11:59:59Z",
  "last_checked_at": "2026-06-10T12:00:15Z",
  "automation_start_allowed": false,
  "warnings": ["mtga_reconnect_window_active"],
  "errors": []
}
```

Allowed `shutdown_reason` values:

- `mtga_unavailable_timeout`
- `operator_stop_requested`
- `supervisor_stop_requested`
- `supervisor_error`
- `unknown`
- `null`

Allowed warning/error codes include:

- `mtga_not_detected`
- `mtga_reconnect_window_active`
- `mtga_reconnected`
- `mtga_unavailable_timeout`
- `mtga_detector_unavailable`
- `mtga_process_detection_unsupported`
- `capture_shutdown_started`
- `capture_shutdown_completed`
- `capture_shutdown_failed`

All labels must remain lowercase snake_case except the fixed literal process name `MTGA.exe`.

## 45-Second Reconnect Window Contract

Required behavior:

1. When capture is not running, MTGA absence should be displayed as unavailable/degraded but should not trigger shutdown.
2. When capture is running and `MTGA.exe` is detected, continue capture normally.
3. When capture is running and `MTGA.exe` changes from detected to not detected, record `reconnect_started_at` and enter `reconnect_window`.
4. The reconnect window lasts 45 seconds.
5. If `MTGA.exe` is detected again before the deadline, clear the active reconnect state and continue capture.
6. If `MTGA.exe` is still not detected at or after the deadline, begin safe app-owned shutdown.
7. The reconnect window applies to normal close, crash, force quit, and any other disappearance. Do not distinguish cause in v1.
8. Player.log silence while `MTGA.exe` is still detected is normal idle time and must not start the reconnect window.

The reconnect timer is backend-owned. The frontend may display seconds remaining, but it must not decide when the timer expires or trigger shutdown from a browser timer.

## Safe Shutdown Sequence

When the reconnect window expires, Codex C should implement the safest shutdown sequence compatible with current code:

1. Record that `MTGA.exe` is not detected through the approved detector.
2. Record `shutdown_reason = mtga_unavailable_timeout`.
3. Move lifecycle to `shutting_down`.
4. Stop only the app-owned live capture supervisor.
5. Ask the running stream/tailer to shut down through the existing app-owned supervisor path.
6. Do not kill MTGA or any external process.
7. Do not delete, move, rename, archive, or clean app-data files.
8. Do not delete `Player.log`.
9. Do not reset parser-owned completed facts.
10. Do not change match/game identity or final reconciliation.
11. Preserve any already completed parser-owned SQLite writes.
12. If current code already has a safe in-flight write result, allow it to finish only through the approved live ingest boundary.
13. Do not invent partial match/game facts during shutdown.
14. Write sanitized app-owned state showing stopped/shutdown-completed or failed/shutdown-failed.
15. Return backend and UI status to a ready/stopped state when safe preconditions allow manual start.

If the current supervisor cannot safely stop or flush without broader behavior changes, Codex C must stop and route back to Codex B. Do not patch around unsafe shutdown by deleting state files, killing processes, or changing parser behavior.

## Player.log Silence Rule

Player.log silence while `MTGA.exe` is detected is normal idle time.

Required behavior:

- do not stop capture because no new log bytes, structured entries, parser events, completed rows, or SQLite writes appeared during a quiet period;
- continue heartbeat/progress updates according to issue #302;
- report safe idle/waiting labels such as `listening_for_events` or `waiting_for_completed_facts`;
- reserve reconnect/shutdown behavior for MTGA process absence, not quiet Player.log.

## Diagnostics-First Display Contract

First visible placement should be Diagnostics, not a new auto-start Dashboard flow.

Diagnostics may show:

- `MTGA process: detected`
- `MTGA process: not detected`
- `Reconnect window: active`
- `Reconnect window: seconds remaining`
- `Shutdown reason: MTGA unavailable timeout`
- `Automation readiness: blocked`

Dashboard may consume only compact backend-owned status if existing Dashboard code already has a safe place for it. Dashboard must not add automatic start, automatic stop, automatic restart, or hidden cleanup behavior.

The frontend must not expose:

- raw detector output;
- process IDs;
- process command lines;
- usernames;
- environment values;
- raw Player.log content;
- raw private paths;
- generated SQLite contents;
- stack traces;
- secrets or endpoint values.

## Automation Readiness Gate

Auto-start capture remains blocked.

The backend or report artifact must expose a safe readiness checklist. Recommended shape:

```json
{
  "schema_version": "live_app_mtga_process_detection_shutdown_readiness_gate.v1",
  "status": "blocked",
  "automatic_start_allowed": false,
  "items": [
    {"key": "manual_start_dashboard", "status": "pass"},
    {"key": "manual_stop_dashboard", "status": "pass"},
    {"key": "starting_cannot_dead_end", "status": "pass"},
    {"key": "capturing_persistent_stop_action", "status": "pass"},
    {"key": "stale_capture_recovery_actionable", "status": "pass"},
    {"key": "analytics_refresh_after_completed_match", "status": "pass"},
    {"key": "mtga_process_detected", "status": "not_proven"},
    {"key": "mtga_disappearance_detected", "status": "not_proven"},
    {"key": "reconnect_window_verified", "status": "not_proven"},
    {"key": "shutdown_returns_ready_to_start", "status": "not_proven"},
    {"key": "shutdown_preserves_completed_facts", "status": "not_proven"},
    {"key": "shutdown_privacy_boundary_verified", "status": "not_proven"},
    {"key": "readiness_recorded_in_contract_or_report", "status": "pass"}
  ]
}
```

Allowed item statuses:

- `pass`
- `fail`
- `blocked`
- `not_proven`
- `deferred`
- `not_applicable`

Gate rules:

- `automatic_start_allowed` must remain false in issue #337.
- A checklist with all `pass` values still does not enable auto-start by itself.
- Future auto-start requires a new issue, contract, implementation, review, and explicit user approval.
- Missing proof must be `not_proven`, not silently treated as pass.

## Backend Responsibility Boundary

The backend may:

- add a small Windows-only process detector;
- add sanitized process status fields to existing status/diagnostics payloads;
- update app-owned live capture state with reconnect-window metadata;
- use backend-owned timer logic to determine reconnect expiry;
- stop only the app-owned capture supervisor after timeout;
- preserve existing explicit start/stop behavior;
- expose safe automation readiness labels.

The backend must not:

- launch MTGA;
- kill MTGA;
- inspect process command lines;
- inspect process environment values;
- expose PIDs as trusted ownership;
- read, copy, hash, print, store, or expose raw Player.log content;
- treat Player.log silence as capture failure while MTGA is detected;
- change parser behavior;
- change analytics schema or migrations;
- start workbook/webhook/App Script/Sheets/output transport;
- add auto-start behavior;
- add destructive cleanup controls.

## Frontend Responsibility Boundary

The frontend may:

- render backend-owned MTGA process status in Diagnostics;
- render reconnect-window labels and seconds remaining supplied by the backend;
- render compact Dashboard status only if existing lifecycle control remains truthful;
- keep manual Start/Stop capture controls governed by backend `start_allowed` and `stop_allowed`;
- show automation readiness as blocked/deferred.

The frontend must not:

- run process detection in the browser;
- infer reconnect-window expiry from browser timers;
- trigger shutdown from a browser timer;
- auto-start capture;
- auto-stop capture except by explicit operator action against an approved backend stop route;
- invent parser facts, match results, SQLite write status, or shutdown success;
- expose raw/private/generated/local artifact content.

## App-Data And State-File Boundary

Allowed app-owned state:

- safe timestamps;
- lifecycle labels;
- reconnect-window metadata;
- MTGA process status labels;
- shutdown reason labels;
- safe warning/error codes;
- automation readiness checklist labels;
- existing live capture state fields.

Forbidden app-owned state:

- raw `tasklist` output;
- PIDs as durable truth;
- process command lines;
- environment values;
- raw Player.log content;
- raw parser event payloads;
- raw private paths;
- SQLite row dumps;
- stack traces;
- secrets or endpoint values.

GET routes must remain read-only except for computing in-memory response values. Any state mutation needed for reconnect/shutdown must happen only inside the already-running app-owned capture supervisor or an explicit POST lifecycle action.

## Relationship To Related Issues

### Issue #297

#297 owns explicit operator-controlled capture start/stop. This contract preserves manual capture as the v1.0 default and does not add auto-start.

### Issue #302

#302 owns heartbeat, no-row diagnostics, and parser status blurb. This contract may add MTGA lifecycle labels alongside those fields, but it must not replace no-row diagnostics or treat quiet logs as failure.

### Issue #304 / #315 / #321

These issues own Dashboard control clarity, stale-state display, and operator workflow. This contract may provide backend state for those UI surfaces, but it must not turn the Dashboard into process truth or add automatic startup.

### Issue #294

#294 owns analytics refresh after rows exist. Shutdown may request or expose refresh state only through existing read-only analytics refresh behavior. This contract does not change refresh-state route semantics.

### Future Auto-Start Issue

Future auto-start capture must remain blocked until a new issue and contract cite this readiness gate and prove every required checklist item.

## Error Behavior

Detector unavailable:

- return `mtga_process.status = detector_unavailable` or `unknown`;
- include only sanitized error code;
- do not include raw stderr/stdout;
- do not stop capture solely because the detector failed unless the implementation proves fail-closed shutdown is safer and routes that decision through review.

Unsupported platform:

- return `unsupported_platform`;
- keep automation readiness blocked;
- do not pretend MTGA is not running.

Contradictory lifecycle state:

- fail closed to `unknown`, `blocked`, or `failed`;
- keep Diagnostics reachable;
- avoid auto-start or auto-cleanup.

Shutdown failure:

- return `capture_shutdown_failed`;
- preserve safe diagnostic labels;
- do not delete state files or kill external processes as a fallback;
- require operator review.

Malformed state:

- report malformed/unknown safely;
- do not echo unsafe state content;
- do not auto-repair unless a future stale-state recovery contract authorizes it.

## Compatibility

Implementation must preserve:

- existing explicit start/stop route behavior;
- existing `GET /api/live/capture/status` fields unless intentionally extended with tests;
- existing #302 heartbeat/progress/no-row diagnostic fields;
- existing watcher process and diagnostics routes;
- existing analytics refresh-state route;
- existing Dashboard manual controls;
- existing protected-surface and private-artifact boundaries.

If Codex C changes response schemas, it must update frontend validators and focused tests in the same implementation.

## Tests Required

Codex C must add or update focused backend tests for:

- Windows detector returns `detected` when mocked `tasklist` output includes `MTGA.exe`;
- Windows detector returns `not_detected` when mocked output excludes `MTGA.exe`;
- detector unavailable produces safe `detector_unavailable` or `unknown`;
- non-Windows platform returns `unsupported_platform`;
- detector response exposes no PID, command line, environment, raw stdout, or raw stderr;
- Diagnostics includes MTGA process status;
- capture status includes `mtga_lifecycle` when appropriate;
- Player.log silence while MTGA is detected does not stop capture;
- MTGA disappearance during capture enters a 45-second reconnect window;
- MTGA return inside 45 seconds continues capture without reset;
- MTGA absence after 45 seconds runs safe app-owned shutdown;
- shutdown leaves backend in stopped/ready status without stale capturing state;
- shutdown preserves already completed parser-owned SQLite writes;
- shutdown does not invent partial parser facts;
- automation readiness remains blocked and `automatic_start_allowed=false`;
- GET routes do not create files or mutate app-data state.

Codex C must add or update focused frontend tests if frontend display changes:

- Diagnostics renders detected/not-detected/reconnect/shutdown labels safely;
- Dashboard still uses backend lifecycle/action flags;
- no automatic start occurs on app load, route navigation, refresh-state polling, or MTGA detected status;
- reconnect countdown display is backend-led and does not trigger browser-owned shutdown;
- malformed lifecycle payloads fail closed;
- unsafe detector values are rejected or redacted.

## Validation Requirements

Recommended Codex C validation, adjusted to touched files:

```powershell
py -m pytest -q tests/test_live_app_explicit_start_capture_control.py tests/test_analytics_local_app_backend.py
py -m pytest -q tests/test_analytics_auto_refresh_after_match_completion.py
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools/check_agent_docs.py
```

Codex C and Codex E must run path-scoped protected-surface and secret/private-marker scans over changed files:

```powershell
@'
<changed file paths>
'@ | py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

@'
<changed file paths>
'@ | py tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

If frontend build creates `frontend/dist`, remove generated build output before final handoff unless a later contract explicitly authorizes committing it.

## Acceptance Criteria

- Contract exists at `docs/contracts/live_app_mtga_process_detection_shutdown_readiness_gate.md`.
- Contract preserves manual capture as the default v1.0 workflow.
- Contract defines Windows-only `MTGA.exe` process detection semantics.
- Contract forbids exposing PIDs, command lines, environment values, raw detector output, and raw/private artifacts.
- Contract defines the 45-second reconnect window.
- Contract defines safe shutdown sequence and stop conditions.
- Contract states Player.log silence while MTGA is detected is normal idle time.
- Contract defines Diagnostics-first display.
- Contract defines automation readiness gate and keeps auto-start blocked.
- Contract defines backend/frontend boundaries.
- Contract defines focused validation and tests.
- Protected parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production surfaces remain untouched.
- Codex B changes no implementation code.

## Unknowns

- Whether current `LocalAppLiveCaptureSupervisor` can stop cleanly after an MTGA timeout without race conditions.
- Whether shutdown should reuse `stop_live_capture(...)` internally or a narrower supervisor method to avoid ownership re-entry issues.
- Whether `tasklist` output parsing should treat multiple `MTGA.exe` rows as `detected` with a safe `multiple_detected` warning or simply `detected`.
- Whether the Diagnostics panel or capture status panel is the best first UI placement for reconnect-window details.
- Whether real/private live testing is needed immediately after Codex C or can wait for Codex E.

## Suspected Gaps

- Existing `live_watcher_process.py` is safeguards-only and does not inspect operating-system processes.
- Existing live capture state has heartbeat/progress but no MTGA process lifecycle fields.
- Existing shutdown is operator-driven; timeout-driven safe shutdown may require careful ownership handling.
- Existing frontend may need new validators for `mtga_process` and `mtga_lifecycle`.
- Existing tests mock stream shutdown but likely do not cover MTGA disappearance/reconnect/timeout behavior.

## Out Of Scope

- automatic capture startup;
- launching MTGA;
- killing MTGA;
- monitoring process command lines;
- distinguishing crash, force quit, and normal close;
- stopping capture because Player.log is quiet while MTGA is detected;
- changing parser behavior;
- changing parser state final reconciliation;
- changing parser event classes;
- changing match/game identity or deduplication;
- changing analytics schema or migrations;
- changing live fact families beyond completed parser-owned match/game facts;
- changing Match Journal truth ownership;
- changing workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, or production behavior;
- OpenAI/model-provider runtime integration;
- AI/coaching, Line Tracer, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice;
- destructive UI controls;
- arbitrary SQL or database browsing;
- committing generated/private/runtime/local artifacts.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #337.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/337

Branch:
codex/live-mtga-process-lifecycle-gate

Base branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_mtga_process_detection_shutdown_readiness_gate.md

Target artifact:
docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_comparison.md

Goal:
Compare current live capture/process/diagnostics/frontend behavior against the contract, then implement the smallest safe Windows-only MTGA process detection, 45-second reconnect window, safe shutdown lifecycle, Diagnostics-first display, and automation readiness gate. Keep manual capture as the v1.0 default and keep auto-start blocked.

Before editing:
- Confirm branch and git status.
- Confirm the branch is based on origin/codex/analytics-foundation.
- Identify unrelated dirty/untracked files and preserve them.
- Read issue #337, the contract, live capture control, watcher process, watcher diagnostics, backend routes, frontend API/types/App/status, and focused tests.
- State what the lifecycle is supposed to do, what current code already does, what gaps remain, and the exact minimal implementation plan.

Do:
- Add a backend-owned Windows-only detector for MTGA.exe using safe metadata-only process image-name detection.
- Do not expose PIDs, command lines, environment values, raw detector output, raw Player.log content, or private/local artifacts.
- Add sanitized mtga_process and mtga_lifecycle fields to existing status/diagnostics surfaces as contracted.
- Enter a 45-second reconnect window when MTGA.exe disappears during active capture.
- Continue capture without reset if MTGA.exe returns within 45 seconds.
- Run safe app-owned capture shutdown if MTGA.exe remains absent after 45 seconds.
- Treat Player.log silence while MTGA.exe is detected as normal idle time.
- Put MTGA process lifecycle in Diagnostics first.
- Keep automatic_start_allowed=false and record automation readiness as blocked.
- Add focused backend/frontend tests.
- Produce docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_comparison.md.

Do not:
- implement automatic capture startup;
- launch or kill MTGA;
- inspect process command lines or environment values;
- stop capture because Player.log is quiet while MTGA is detected;
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations, live fact families beyond approved completed match/game facts, Match Journal truth ownership, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice;
- expose raw/private/generated/local artifacts;
- add destructive UI controls or arbitrary SQL/database browsing;
- target main.

Validation:
- Run focused backend tests for live capture/process/diagnostics lifecycle behavior.
- Run focused frontend tests if frontend display/types change.
- Run npm typecheck/test/build if frontend changes.
- Run py -m ruff check src tests tools.
- Run git diff --check.
- Run py tools/check_agent_docs.py.
- Run path-scoped protected-surface and secret/private-marker scans over changed files.
- Remove frontend/dist if build creates it.

Final output must include:
- role performed;
- issue and contract used;
- branch and git status;
- current behavior compared to contract;
- implementation summary;
- files changed;
- tests changed;
- validation run and results;
- protected-surface status;
- secret/private-marker status;
- generated/private artifact status;
- confirmation that manual capture remains default and auto-start remains blocked;
- remaining risks;
- next recommended role;
- pasteable Codex E prompt;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/337"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue problem representation"
  contract_artifact: "docs/contracts/live_app_mtga_process_detection_shutdown_readiness_gate.md"
  target_artifact: "docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_comparison.md"
  branch: "codex/live-mtga-process-lifecycle-gate"
  base_branch: "codex/analytics-foundation"
  risk_tier: "High"
  decision: "Windows-only MTGA.exe process detection, 45-second reconnect window, safe app-owned shutdown after timeout, Diagnostics-first display, and automation readiness gate. Manual capture remains default; auto-start remains blocked."
  stop_conditions:
    - "Do not implement automatic capture startup."
    - "Do not launch or kill MTGA."
    - "Do not expose process command lines, environment values, PIDs, raw detector output, raw Player.log content, or private/local artifacts."
    - "Do not stop capture merely because Player.log is quiet while MTGA is detected."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not target main."
```
