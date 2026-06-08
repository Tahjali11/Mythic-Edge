# Live App Explicit Start Capture Control Contract

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/297
- Historical trackers: https://github.com/Tahjali11/Mythic-Edge/issues/204 and https://github.com/Tahjali11/Mythic-Edge/issues/207
- Branch: `codex/analytics-foundation`
- Role: Codex B / Module Contract Writer
- Risk tier: High
- Expected next role: Codex C / Module Implementer

## Purpose

Mythic Edge needs an explicit, operator-controlled way to start live Player.log capture from the local app after the app has already proven that Player.log is configured and live capture is ready. The control must start only a safe local capture supervisor, write only parser-owned completed facts into local SQLite through the approved analytics ingest boundary, and leave external transport, AI, coaching, and production-facing behavior disabled.

This contract defines the smallest approved control surface for issue #297:

- visible `Start capture` behavior in the local app;
- a bounded `Stop capture` behavior for the same app-owned supervisor;
- local loopback-only backend routes;
- single-instance and stale-state safeguards;
- truthful status vocabulary;
- privacy and generated-artifact boundaries.

## Observed Current Behavior

The current local app has read-only live Player.log status, watcher readiness status, watcher process safeguard status, watcher diagnostics, and live ingest readiness/status routes. Those surfaces report readiness and blockers, but they do not start live capture.

The frontend now distinguishes a ready-but-not-running state from active capture. A ready app may show copy such as `Ready to start`, while `Capturing` is reserved for cases where the backend proves that the app-owned capture loop is running, tailing has started, and SQLite live writes are enabled.

The analytics live ingest adapter already defines a downstream SQLite write boundary for parser-normalized completed match and game facts with `source_kind=live_parser`. That adapter is the approved write path for this first live-control slice.

The legacy parser runner can tail Player.log, but it also carries broader runtime and transport surfaces. It is not an approved local app control target for issue #297 unless Codex C proves a no-transport harness that avoids workbook, webhook, Apps Script, and production-facing behavior.

## Required Guarantees

### Start Capture Definition

`Start capture` means:

1. the operator explicitly requests live capture from the local app;
2. the backend verifies all required preconditions;
3. the backend starts exactly one app-owned local capture supervisor;
4. the supervisor tails Player.log only through the approved local boundary;
5. completed parser-owned match/game facts are written to SQLite through the approved live ingest adapter;
6. status changes from ready/stopped to starting, capturing, blocked, failed, or stale based on observed supervisor state.

`Start capture` does not mean automatic app launch capture, production parser execution, external posting, workbook sync, AI analysis, coaching, arbitrary database access, or raw Player.log storage.

### Stop Capture Definition

Issue #297 may include a bounded `Stop capture` route because starting a long-running local supervisor without a same-scope stop path creates local process and stale-state risk.

`Stop capture` may stop only a supervisor that the local app can prove it owns. Ownership proof must use app-data-root-scoped state such as a supervisor token, state file identity, and process metadata. A process id by itself is not enough.

`Stop capture` must not become a kill/reset/cleanup tool. It must not delete app data, delete databases, clear diagnostics, clean stale locks, terminate unrelated processes, or modify Player.log.

### Automatic Start Boundary

Automatic start remains out of scope. Opening the local app must not begin live capture. The frontend may invite the user to start capture only when the backend says `start_allowed=true`.

### Parser Truth Ownership

The parser/state layer remains the owner of event interpretation and final match/game facts. The local app owns only control state, status display, and local operator workflow. SQLite stores downstream analytics facts; it does not become parser truth.

The frontend must not infer facts from control state. It may display whether capture is ready, running, blocked, or degraded, but it must not invent match identity, game identity, results, play/draw, mulligans, card actions, opponent observations, or analytics conclusions.

## Route Inventory

Codex C should preserve existing read-only status routes and may add the following local loopback-only routes:

- `GET /api/live/capture/status`
- `POST /api/live/capture/start`
- `POST /api/live/capture/stop`

`GET /api/live/ingest/status` should remain compatible with existing live ingest status behavior. It may reference capture status, but it must not require callers to use new routes for read-only status checks.

Do not add restart, reset, kill, cleanup, delete, arbitrary SQL, database browsing, external upload, or production transport routes.

## Response Shape

### Capture Status

The status route should return a stable object shaped like:

```json
{
  "object": "mythic_edge_local_app_live_capture_status",
  "schema_version": "live_app_explicit_start_capture_control.v1",
  "status": "ready_to_start",
  "mode": "explicit_operator_control",
  "capture": {
    "running": false,
    "start_allowed": true,
    "stop_allowed": false,
    "parser_runner_started": false,
    "tailing_started": false,
    "sqlite_live_writes_enabled": false,
    "external_transport_allowed": false,
    "raw_player_log_storage_enabled": false,
    "supervisor_kind": "local_app_capture_supervisor",
    "source_kind": "live_parser"
  },
  "preconditions": [],
  "state": {},
  "last_result": null,
  "warnings": [],
  "errors": []
}
```

Allowed `status` values:

- `unavailable`
- `blocked`
- `ready_to_start`
- `starting`
- `capturing`
- `degraded`
- `stopping`
- `stopped`
- `failed`
- `crashed`
- `stale`
- `unknown`

The API may include safe counters and timestamps, such as `started_at`, `updated_at`, `last_write_at`, `last_completed_fact_at`, `row_counts`, and `warning_count`. It must not include raw Player.log content, raw saved-event content, raw private paths, sensitive local values, database row dumps, or external endpoint values.

### Start Result

The start route should return:

```json
{
  "object": "mythic_edge_local_app_live_capture_start_result",
  "schema_version": "live_app_explicit_start_capture_control.v1",
  "status": "starting",
  "accepted": true,
  "capture_status": {},
  "warnings": [],
  "errors": []
}
```

Allowed start result statuses:

- `starting`
- `capturing`
- `already_running`
- `blocked`
- `failed`

A duplicate start request for an already app-owned running supervisor should not start another supervisor. It should return `already_running` with current status.

### Stop Result

The stop route should return:

```json
{
  "object": "mythic_edge_local_app_live_capture_stop_result",
  "schema_version": "live_app_explicit_start_capture_control.v1",
  "status": "stopping",
  "accepted": true,
  "capture_status": {},
  "warnings": [],
  "errors": []
}
```

Allowed stop result statuses:

- `stopping`
- `stopped`
- `not_running`
- `blocked`
- `failed`

Stop must be refused when the backend cannot prove that the supervisor is app-owned.

## Backend Contract

### Supervisor Target

Codex C should prefer a new local-app capture supervisor or harness, for example under `src/mythic_edge_parser/local_app/`, rather than calling the broad legacy runner directly.

The supervisor may reuse lower-level parser, stream, or tailing components only when the implementation proves:

- external transport is disabled;
- runtime posting is disabled;
- workbook/webhook/App Script behavior cannot be reached;
- no raw Player.log content is stored in SQLite, reports, committed files, or API responses;
- only parser-owned completed match/game facts flow into the approved live SQLite ingest adapter.

If Codex C cannot find or build that safe no-transport path without changing parser truth or transport behavior, it must stop and route back to Codex B instead of wiring the legacy runner.

### Start Preconditions

The backend must fail closed unless all required preconditions are satisfied:

- app data root is available;
- allowed local state/diagnostic directories are available or can be created by the explicit POST request;
- Player.log path is configured, points to a file, and is readable at the metadata/access level needed for capture;
- analytics database can be opened and the existing migration path can verify the expected schema;
- no verified app-owned capture supervisor is already starting or running;
- no stale, orphaned, or ambiguous supervisor state blocks ownership;
- external transport is disabled;
- approved live SQLite ingest adapter is available;
- frontend controls are authorized by this contract;
- the control request came through the local loopback app boundary.

Read-only GET routes should remain no-write. Any directory or state creation needed for control must happen only during explicit POST handling.

### Single-Instance Guard

The supervisor must use app-data-root-scoped state, such as:

- `jobs/live_capture_state.json`
- `jobs/live_capture_lock.json`
- supervisor token or ownership id;
- process id or thread id as supporting evidence only;
- `started_at` and heartbeat/update timestamps;
- current status and last safe result.

Process id alone is not sufficient. Ambiguous or stale state must produce a blocked/stale status and a manual-review message. The first implementation must not auto-kill, auto-delete, or auto-clean unknown state.

### SQLite Write Boundary

Live capture may write only through the approved analytics live ingest path for completed parser-owned match/game facts.

In scope for issue #297:

- completed or final parser-normalized match facts already supported by the live ingest contract;
- completed or final parser-normalized game facts already supported by the live ingest contract;
- deterministic upsert behavior already defined by the analytics ingest layer;
- safe row counts and timestamps.

Out of scope for issue #297:

- provisional live facts;
- gameplay-action live writes;
- opponent-card-observation live writes;
- field-evidence live writes;
- schema or migration changes;
- manual JSONL import behavior changes;
- analytics auto-refresh behavior from issue #294.

### Waiting For Events

If the supervisor is running and tailing Player.log but MTGA has not produced a completed fact yet, the status may be `capturing` with a safe `waiting_for_events` warning or informational note. The app must not treat the absence of new facts as a failure unless a timeout, crash, unreadable file, database error, or explicit blocker is observed.

### Failure Behavior

The backend must report safe, typed blockers for:

- missing Player.log;
- unreadable Player.log;
- invalid configured path;
- app data root unavailable;
- analytics database unavailable;
- migration/schema unavailable;
- duplicate start attempt;
- stale supervisor state;
- ambiguous ownership;
- crash detected;
- tailer failure;
- SQLite write failure;
- external transport not provably disabled;
- unsupported legacy runner path.

Error responses must use stable codes and safe summaries. They must not include raw Player.log lines, private local path strings beyond approved symbolic summaries, stack traces with sensitive values, database row dumps, or external endpoint values.

## Frontend Contract

The first frontend implementation may expose:

- a `Start capture` button when status is `ready_to_start` or `stopped` and `start_allowed=true`;
- a progress state while the start request is accepted and status is `starting`;
- a `Capturing` state only after the backend proves active app-owned capture;
- a `Stop capture` button only when `stop_allowed=true` for the app-owned supervisor;
- blocked/degraded messages with safe next actions;
- polling after start until `capturing`, `blocked`, `failed`, `stale`, or timeout.

The frontend must not expose:

- automatic start on page load;
- restart/reset/kill/delete controls;
- arbitrary SQL or database browsing;
- raw log viewing;
- private path dumps;
- upload or external submission behavior;
- coaching, hidden-card inference, archetype inference, player-mistake labels, best-line advice, or Line Tracer claims.

The UI may show that analytics views need manual refresh or later auto-refresh work. It must not implement issue #294 unless that issue is explicitly routed into the same implementation.

## Local Artifact Boundaries

Allowed local generated state for the future implementation:

- app-data-root-scoped capture state under a `jobs` area;
- app-data-root-scoped safe diagnostics under a diagnostics area;
- local SQLite files already authorized by analytics contracts;
- safe counters, timestamps, statuses, and warning/error codes.

Forbidden in repo, API responses, UI reports, committed files, and durable artifacts:

- raw Player.log content;
- raw saved-event content;
- private JSONL payloads;
- generated SQLite database contents;
- SQLite sidecar files;
- runtime logs with private content;
- transport-failure payload artifacts;
- workbook exports;
- secret values;
- private endpoint values;
- spreadsheet ids;
- local-only machine artifacts.

Generated local files must remain ignored by Git. Codex C must not commit generated app data, local databases, runtime outputs, frontend build output, private inputs, or local-only artifacts.

## Relationship To Earlier Live Contracts

This contract builds on:

- `live_app_player_log_path_watcher_status.md`: read-only Player.log path and watcher readiness;
- `live_app_player_log_watcher_process_control_safeguards.md`: process-control vocabulary and fail-closed safeguards;
- `live_app_parser_owned_fact_capture_sqlite.md`: approved live SQLite ingest boundary for completed parser-owned facts;
- `local_app_live_capture_status_truthful_display.md`: truthful display of ready/not-running versus active capture;
- `live_player_log_v1_supported_readiness.md`: private-local-v1 support evidence and privacy-safe live smoke expectations.

This contract does not replace those contracts. It authorizes the first explicit operator-controlled start/stop path that connects the readiness surfaces to the live ingest boundary.

## Protected Surfaces

Codex C must not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema or migrations;
- manual JSONL import semantics;
- replay ingest semantics;
- Match Journal truth ownership;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport behavior;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- hidden-card inference;
- archetype inference;
- player-mistake labels;
- gameplay advice.

## Acceptance Criteria

Codex C implementation is acceptable when:

1. the new capture-control routes exist and are local loopback-only;
2. start is explicit, operator-controlled, and never automatic;
3. stop is bounded to an app-owned supervisor;
4. duplicate starts cannot create duplicate supervisors;
5. stale or ambiguous state blocks instead of being silently cleaned;
6. active capture status requires supervisor running, tailing started, and SQLite live writes enabled;
7. SQLite writes go only through the approved live ingest adapter;
8. completed match/game facts are the only live facts written in this slice;
9. the broad legacy runner is not used unless a no-transport harness is proven;
10. frontend controls are visible only when backend flags allow them;
11. no raw Player.log content or private artifacts appear in UI, API responses, reports, tests, or committed files;
12. workbook/webhook/App Script/Sheets/output transport remains unreachable from the local app capture path;
13. validation covers success, blocked, duplicate, stale, crash/error, stop-owned, and privacy cases.

## Validation Expectations

Codex C should run the smallest focused validations first, then broaden as needed:

```powershell
py -m pytest -q tests/test_analytics_local_app_backend.py tests/test_live_app_parser_owned_fact_capture_sqlite.py
py -m pytest -q tests/test_runner.py tests/test_tailer.py
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools/check_agent_docs.py
```

Codex C should also run path-scoped protected-surface and secret/private-marker scans over changed files:

```powershell
@'
<changed file paths>
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

@'
<changed file paths>
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

If frontend build creates `frontend/dist`, Codex C must remove that generated output before handoff unless a later contract explicitly authorizes committing it.

A real/private Player.log smoke is useful before private-local-v1 support is claimed, but Codex C must not read, print, copy, store, or commit raw Player.log content. Any private smoke must be explicit, local-only, and summarized with safe status/counter evidence.

## Suspected Gaps

- The current code may not yet have a safe parser-to-final-fact loop that excludes the broad runner's transport behavior.
- The frontend may need a small API wrapper and state machine for start/stop polling.
- Tests may need a mocked supervisor to avoid real Player.log access.
- Stale state handling may require a durable local-app state shape that existing read-only safeguards only sketched.
- Issue #294 analytics auto-refresh may still be needed after capture writes facts, but it should not block this contract unless the UI cannot show updated status without it.

## Out Of Scope

- automatic live capture on app launch;
- live capture from the actual private app-data root without explicit user approval;
- real Player.log smoke execution in this contract-writing thread;
- gameplay-action, opponent-observation, or field-evidence live writes;
- analytics schema or migration changes;
- manual import changes;
- arbitrary SQL access;
- generated database browsing;
- workbook/webhook/App Script/Sheets transport;
- OpenAI/API/model-provider integration;
- AI coaching, Line Tracer, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice;
- production readiness claims;
- public release claims.

## Codex C Handoff Prompt

Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #297.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/297

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_explicit_start_capture_control.md

Goal:
Compare the current local app live Player.log status/process/ingest code against the contract, then implement the smallest safe explicit Start capture control and bounded app-owned Stop capture control. Preserve parser truth ownership and keep all behavior local-only.

Before editing:
- Confirm branch and git status.
- Identify unrelated dirty files and do not revert them.
- Read the contract and the related live status/process/ingest contracts.
- Inspect backend routes, live watcher process/status modules, analytics live ingest helpers, frontend status UI/types/API, and existing tests.
- State the minimal implementation plan.

Required behavior:
- Add local loopback-only capture status/start/stop behavior as contracted.
- Start must be explicit and operator-controlled, never automatic.
- Stop may stop only a verified app-owned supervisor.
- Use a safe local-app supervisor/harness; do not call the broad legacy runner unless a no-transport harness is proven.
- Write only completed parser-owned match/game facts through the approved live ingest adapter.
- Keep external transport disabled.
- Do not store or expose raw Player.log content.
- Add focused backend/frontend tests for allowed, blocked, duplicate, stale, owned-stop, and privacy-safe behavior.

Do not:
- change parser behavior, parser final reconciliation, parser event classes, match/game identity, analytics schema/migrations, manual import semantics, replay ingest semantics, Match Journal truth ownership, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice;
- implement automatic start;
- add arbitrary SQL or database browsing;
- commit generated databases, runtime outputs, frontend build output, private logs, private JSONL artifacts, local app data, or local-only artifacts;
- target main.

Validation:
- Run focused backend and frontend tests for the changed surfaces.
- Run `git diff --check`.
- Run `py tools/check_agent_docs.py`.
- Run path-scoped protected-surface and secret/private-marker scans over changed files.
- Remove generated frontend build output before handoff if created.

Final output:
- role performed;
- issue and contract used;
- files changed;
- implementation summary;
- validation run;
- privacy/protected-surface status;
- remaining risks;
- next recommended role;
- workflow_handoff block.

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex B: Module Contract Writer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/297"
  historical_trackers:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/204"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  current_branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/live_app_explicit_start_capture_control.md"
  risk_tier: "High"
  decision: "Authorize explicit operator-controlled Start capture plus bounded app-owned Stop capture; no automatic start; no broad legacy runner unless no-transport harness is proven."
  protected_surfaces:
    - "parser behavior"
    - "parser state final reconciliation"
    - "parser event classes"
    - "match/game identity and deduplication"
    - "analytics schema and migrations"
    - "manual JSONL import and replay ingest semantics"
    - "workbook schema"
    - "webhook payload shape"
    - "Apps Script and Google Sheets behavior"
    - "output transport and production behavior"
    - "OpenAI/model-provider, AI/coaching, Line Tracer, hidden-card, archetype, player-mistake, and gameplay-advice behavior"
  next_recommended_role: "Codex C: Module Implementer"
```
