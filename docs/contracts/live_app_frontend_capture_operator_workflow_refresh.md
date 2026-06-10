# Live App Frontend Capture Operator Workflow Refresh Contract

## Module

`live_app_frontend_capture_operator_workflow_refresh`

Plain English: this contract defines the v1.0 operator workflow for using live
Player.log capture from the local app Dashboard. The operator should be able to
open the app, start capture manually, play a match, see whether completed rows
were recorded, see analytics refresh state, and stop capture without using
PowerShell, raw JSON, or private artifact inspection for the normal path.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/321
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Branch: `codex/analytics-foundation`
- Role: Codex B / Module Contract Writer
- Risk tier: Medium-High if kept frontend/workflow-only; High if backend
  lifecycle, stale recovery, or automatic startup behavior changes are needed.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/templates/workflow_handoff.md`
- GitHub issue #321
- tracker issue #136
- `docs/internal_project_map.md`
- `docs/contracts/live_app_explicit_start_capture_control.md`
- `docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md`
- `docs/contracts/live_app_stale_capture_dashboard_recovery.md`
- `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`
- `docs/contracts/analytics_auto_refresh_after_match_completion.md`
- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`
- `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`
- `docs/contracts/local_app_live_capture_status_truthful_display.md`
- `docs/contracts/live_player_log_v1_supported_readiness.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/analytics_refresh_state.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/status.ts`
- `tests/test_live_app_explicit_start_capture_control.py`
- `tests/test_analytics_auto_refresh_after_match_completion.py`
- `tests/test_analytics_local_app_backend.py`

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

Tracker #136 remains open. This contract does not close the tracker and does
not claim private-local-v1 release readiness by itself.

## Owning Layer

Primary owning layer: Local App / UI operator workflow.

Supporting truth/status layers:

- backend live capture status owns capture lifecycle truth;
- backend analytics refresh state owns analytics refresh-revision truth;
- live capture heartbeat/progress owns app-owned operational metadata;
- parser/state owns match, game, event, identity, and final fact truth;
- SQLite remains downstream local analytics storage;
- frontend owns presentation, explicit operator actions, polling orchestration,
  and safe status copy only.

## Internal Project Area

Local App / UI.

Adjacent areas:

- Live Player.log Mode;
- Analytics Foundation;
- Quality / Governance.

## Truth Owner

The frontend must not own parser truth, capture lifecycle truth, SQLite write
truth, analytics truth, workbook truth, or AI truth.

For this contract:

- backend `/api/live/capture/status` owns whether capture is ready, starting,
  capturing, stopping, stopped, blocked, stale, failed, or unavailable;
- backend `/api/live/capture/start` and `/api/live/capture/stop` own accepted or
  refused lifecycle commands;
- backend `/api/analytics/refresh-state` owns the opaque analytics revision and
  whether completed match-result facts are visible in local SQLite;
- backend `/api/analytics/dashboard/modules` and existing analytics history
  routes own displayable analytics data;
- frontend may compare opaque revisions and refresh views, but it must not infer
  match completion, win/loss, row writes, or parser facts from timers, browser
  state, local storage, or UI labels.

## Bridge-Code Status

`bridge_code`

Allowed data flow:

```text
backend live capture status/start/stop results
  -> frontend Dashboard control and operator copy

backend analytics refresh-state revision
  -> frontend conservative refresh orchestration
  -> refreshed read-only analytics views
```

Forbidden reverse flow:

- frontend labels, route state, pending state, polling state, or local storage
  must not write parser state, live capture state, SQLite analytics facts,
  workbook rows, webhook payloads, Apps Script state, production state, or
  AI/coaching outputs;
- the frontend must not repair, delete, reset, restart, or clean stale capture
  state;
- the frontend must not treat successful display refresh as proof of game truth.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md`

Future Codex C implementation may touch, subject to comparison and validation:

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/src/api.ts`, only if existing API helpers need small workflow-safe
  reuse or validation coverage;
- `frontend/src/types.ts`, only if existing frontend response types need
  display-safe narrowing;
- `frontend/src/status.ts`, only if status-label helpers need frontend-only
  mapping updates;
- `docs/implementation_handoffs/live_app_frontend_capture_operator_workflow_refresh_comparison.md`

Backend source files are reference surfaces for this contract. Codex C must
route back to Codex B before changing backend lifecycle semantics, stale
recovery semantics, route shapes, parser/live ingest behavior, or analytics
schema.

## Observed Current Behavior

Issue #321 records a successful real local smoke on June 9, 2026. The smoke
proved that explicit live capture can write parser-owned match/game facts from
Player.log into SQLite and that backend/frontend analytics can surface those
rows.

Relevant backend surfaces already exist:

- `GET /api/live/capture/status`
- `POST /api/live/capture/start`
- `POST /api/live/capture/stop`
- `GET /api/analytics/refresh-state`
- `GET /api/analytics/dashboard/modules`
- read-only analytics history, split, opening-hand, mulligan, gameplay-action,
  and opponent-observation routes

Relevant frontend surfaces already exist:

- typed live capture API helpers;
- typed analytics refresh-state helper;
- Dashboard Live capture card and lifecycle control;
- Diagnostics Live Capture Control panel;
- analytics auto-refresh notice and refresh-state polling behavior;
- Decision Support modules.

The remaining problem is operator workflow clarity, not parser correctness. The
user still had to coordinate PowerShell windows, direct API calls, stale-state
cleanup, raw JSON inspection, and manual refresh confirmation during the smoke.
The app should make the normal v1.0 manual workflow understandable without
turning the browser into capture truth.

## Operator Workflow Objective

The v1.0 intended workflow is:

```text
Open Mythic Edge
  -> verify Dashboard says capture is ready, blocked, stale, or unavailable
  -> click Start capture only when backend allows it
  -> play a match
  -> see a compact backend-led recording/status line
  -> see analytics views refresh or show degraded refresh state
  -> click Stop capture when backend allows it
```

The Dashboard should answer four operator questions without raw JSON:

1. Can I start capture safely right now?
2. Is capture actually running, blocked, stale, or stopped?
3. Did the most recent completed match get recorded into local analytics?
4. Are analytics views current, refreshing, paused, or degraded?

## Contract Decision

Use a manual-capture operator workflow refresh for v1.0.

Approved first implementation direction:

- keep manual capture as the default and only routine operator workflow;
- use the existing Dashboard Live capture lifecycle control;
- use backend capture status and action flags as lifecycle truth;
- show stale or blocked capture as needs-review, not ready-to-start;
- keep Diagnostics reachable for stale, blocked, failed, or unavailable states;
- use backend `parser_status_blurb`, heartbeat/progress labels, and analytics
  refresh-state only for safe display copy;
- show one compact post-match recording line when backend-owned status supports
  it;
- keep analytics auto-refresh conservative and visible-document aware;
- keep manual refresh controls available;
- add focused tests for the end-to-end browser workflow states.

Not approved for this contract:

- automatic capture startup on app launch;
- automatic stale cleanup, reset, delete, restart, or recovery behavior;
- a new backend stale recovery endpoint;
- MTGA process detection truth;
- arbitrary SQL, database browsing, raw JSON diagnostics, or private artifact
  display;
- parser, analytics schema, workbook, webhook, Apps Script, Google Sheets,
  OpenAI, AI/coaching, Line Tracer, production, or deployment behavior changes.

If Codex C finds that the existing backend cannot safely support the workflow
without new lifecycle or recovery semantics, Codex C must stop and route back to
Codex B with the exact missing backend contract requirement.

## Manual Capture Default Behavior

Manual capture remains the v1.0 default.

Required rules:

- Opening the app must not start capture.
- Loading the Dashboard must not start capture.
- Refresh-state polling must not start capture.
- Route/hash navigation must not start capture.
- Browser local storage must not start capture.
- Capture may start only after an explicit operator action against an existing
  authorized start control and only when backend `start_allowed=true`.
- Capture may stop only after an explicit operator action against an existing
  authorized stop control and only when backend `stop_allowed=true`.
- Pending frontend state may disable repeated clicks, but it must reconcile from
  backend `capture_status`.

The default workflow may invite the user to start capture when safe, but it must
not start capture for them.

## Why Automatic Startup Remains Deferred

Automatic capture startup remains deferred because it adds hidden failure modes
that are not yet fully retired:

- stale capture state can block start and must remain understandable before any
  automatic retry or recovery is safe;
- duplicate supervisors could corrupt operator trust or local status if
  ownership proof is ambiguous;
- MTGA process detection and log activity are not parser truth and are not
  enough to prove capture should start;
- app launch, browser tab focus, and refresh-state polling are weak signals for
  operator intent;
- automatic start could surprise the user by reading local Player.log metadata
  or writing SQLite rows before the user intentionally enables capture;
- the successful June 9, 2026 smoke already proved explicit control works, so
  the next v1.0 improvement should make that manual workflow smooth before
  exploring opt-in automation.

Future automatic capture needs a separate issue and contract. That future
contract must define opt-in settings, stale-state recovery authority,
single-instance guarantees, privacy boundaries, validation, and rollback.

## Frontend Workflow And Status Expectations

### Dashboard Live Capture Card

The Dashboard Live capture card must:

- display the backend-owned status label and tone;
- keep Start/Stop/Needs review/Unavailable controls in a stable location;
- show `Start capture` only when backend `start_allowed=true`;
- show `Stop capture` only when backend `stop_allowed=true`;
- show pending `Starting` or `Stopping` while a POST is in flight;
- fail closed for stale, blocked, failed, crashed, degraded, unknown,
  unavailable, malformed, or contradictory status;
- keep a diagnostics affordance visible for all lifecycle states;
- not show `Ready to start` when backend state is stale and start is not
  allowed;
- not show `Capturing` unless backend status and running flags prove active
  capture.

### Post-Match Recording Line

The Dashboard may show one compact backend-led line such as:

```text
Most recent completed match was recorded.
```

This line is allowed only when backend-owned status supports it. Acceptable
sources include:

- `parser_status_blurb.code = most_recent_match_completed`;
- `progress.last_no_write_reason = rows_written` with positive
  `sqlite_rows_written`;
- `progress.last_sqlite_write_at` plus backend-safe completed-match counters;
- changed `/api/analytics/refresh-state.analytics_revision` with
  `latest_completed_match_result_available=true`.

The frontend must not derive this line from timers, button clicks, local storage
alone, page refresh alone, or raw row inspection.

Allowed degraded alternatives:

- `Capture active; waiting for completed match facts.`
- `Analytics refresh pending.`
- `Capture needs review. Open diagnostics.`
- `No completed match rows available yet.`

### Analytics Refresh Display

The frontend must keep the #294 refresh-state boundary:

- refresh state is backend-owned;
- revision is opaque and compared only for equality;
- polling is conservative and visible-document aware;
- manual refresh remains visible and working;
- refresh notices must not claim win/loss or parser truth.

The operator-facing workflow should make it clear whether analytics are
checking, up to date, updated, paused, or degraded.

### Diagnostics And Technical Details

Normal Dashboard operation should not require raw JSON inspection. Detailed
heartbeat/progress/no-row labels belong in Diagnostics or collapsed technical
details.

Diagnostics may display sanitized labels, counters, timestamps, warnings, and
errors. It must not display raw Player.log content, raw JSONL payloads, raw
private paths, raw hashes, generated SQLite contents, SQL text, stack traces,
secrets, endpoint values, environment values, app-data files, or local-only
artifacts.

## Backend Truth/Status Dependency

This contract consumes existing backend routes. It does not require new route
shapes if current payloads already support the workflow.

Required backend dependencies:

- `/api/live/capture/status` returns sanitized lifecycle status, action flags,
  heartbeat/progress, and parser status blurb;
- `/api/live/capture/start` returns a sanitized start result with
  `capture_status`;
- `/api/live/capture/stop` returns a sanitized stop result with
  `capture_status`;
- `/api/analytics/refresh-state` returns a read-only sanitized revision signal;
- analytics history and dashboard module routes stay read-only and curated.

Codex C may add frontend validation around these fields. Codex C must not
change backend lifecycle semantics under this contract.

If current backend status says stale but the blurb text suggests restart while
`start_allowed=false`, the Dashboard must display a safer needs-review message,
not an enabled restart action.

## Relationship To Related Contracts

### Issue #297: Explicit Start Capture Control

#297 owns backend explicit Start/Stop routes, lifecycle status, app-owned
supervisor ownership, duplicate-start behavior, and raw Player.log storage
boundaries. This #321 contract consumes those routes and must not redefine
their semantics.

### Issue #304: Dashboard Live Capture Control Clarity

#304 owns stable Dashboard placement for the live capture lifecycle control.
This #321 contract may refine the workflow around that control but must not
turn frontend toggle styling into lifecycle truth.

### Issue #315: Stale Capture Dashboard Recovery

#315 owns stale display and diagnostics affordance. This #321 contract keeps
stale recovery display-only. It does not authorize reset, cleanup, delete,
restart, or recovery endpoints. If a true recovery endpoint is needed, route to
a separate high-risk Codex B contract.

### Issue #302: Heartbeat / No-Row Diagnostics

#302 owns heartbeat, progress, no-row labels, and backend-led
`parser_status_blurb` fields. This #321 contract may display those existing
fields in compact form but must not add new diagnostics counters or change
their backend semantics.

### Issue #294: Analytics Auto-Refresh

#294 owns backend refresh-state and frontend polling after completed rows exist.
This #321 contract may require the manual operator workflow to surface #294
states clearly, but it must not change refresh-state route semantics or make
the frontend infer completed match truth.

## Public Interface

Frontend may depend on:

- `fetchLiveCaptureStatus()`
- `startLiveCapture()`
- `stopLiveCapture()`
- `fetchAnalyticsRefreshState()`
- `fetchAnalyticsDashboardModules()`
- existing read-only analytics history helpers
- `LiveCaptureStatusResponse`
- `LiveCaptureStartResult`
- `LiveCaptureStopResult`
- `AnalyticsRefreshStateResponse`
- `AnalyticsDashboardModulesResponse`

Backend routes consumed:

- `GET /api/live/capture/status`
- `POST /api/live/capture/start`
- `POST /api/live/capture/stop`
- `GET /api/analytics/refresh-state`
- `GET /api/analytics/dashboard/modules`
- existing read-only analytics history routes

This contract does not authorize new public backend routes.

## Inputs

Allowed frontend inputs:

- backend live capture status object;
- backend start/stop result objects;
- backend analytics refresh-state object;
- backend analytics modules/history objects;
- sanitized warnings, errors, labels, booleans, counters, and timestamps.

Forbidden frontend inputs:

- raw Player.log content;
- raw JSONL payloads;
- raw saved-event lines;
- raw private paths;
- raw hashes;
- generated SQLite contents;
- arbitrary SQL output;
- stack traces;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs,
  environment values, endpoint values, app-data files, runtime logs, workbook
  exports, or local-only artifact contents.

## Outputs

Allowed outputs:

- Dashboard lifecycle control state and copy;
- Diagnostics route affordance;
- compact post-match recording status when backend-supported;
- analytics auto-refresh status display;
- refreshed frontend read-only analytics view state;
- focused frontend tests;
- implementation handoff.

Forbidden outputs:

- parser facts;
- analytics writes;
- SQLite schema or migration changes;
- raw/private data display;
- destructive controls;
- arbitrary SQL/database browsing;
- external submissions or writes;
- AI/coaching/Line Tracer/hidden-card/archetype/player-mistake/best-line
  claims.

## Invariants

- Manual capture remains the default operator workflow.
- Automatic startup remains deferred.
- Capture starts only from explicit operator action and backend permission.
- Capture stops only from explicit operator action and backend permission.
- Backend live capture status remains lifecycle truth.
- Backend analytics refresh state remains revision truth.
- Parser/state remains fact truth.
- SQLite remains downstream storage.
- Stale, blocked, failed, unavailable, malformed, or contradictory status fails
  closed.
- Dashboard copy must not require or expose raw JSON in the normal workflow.
- Manual refresh remains available.
- No raw/private/local artifact content is displayed, committed, or persisted by
  this slice.

## Error Behavior

Malformed live capture payload:

- show `Unavailable` or `Needs review`;
- no Start/Stop action;
- keep Diagnostics reachable;
- do not display raw payload details.

Start/stop failure:

- show safe failure copy;
- reconcile from `capture_status` when available;
- do not retry automatically;
- do not auto-clean stale state.

Stale capture state:

- show stale/needs-review copy;
- do not show enabled Start, Stop, or Restart unless backend explicitly allows
  the action;
- route to Diagnostics for safe details.

Analytics refresh-state failure:

- show degraded non-blocking refresh copy;
- keep manual refresh controls;
- do not infer row state or match truth.

Conflicting backend signals:

- blocked/degraded/stale/unsafe signals outrank ready copy;
- active capture requires consistent backend proof;
- post-match recording copy requires backend-owned evidence.

## Side Effects

Allowed future Codex C side effects:

- frontend render-state changes;
- frontend route/hash navigation to existing Diagnostics route;
- explicit user-triggered POST calls to existing start/stop routes;
- existing frontend polling of refresh-state;
- focused frontend tests;
- implementation handoff documentation.

Forbidden side effects:

- new backend route shapes;
- backend lifecycle semantic changes;
- stale cleanup/reset/delete/restart/recovery behavior;
- automatic startup;
- parser behavior changes;
- analytics schema, migration, or ingest changes;
- SQLite writes from frontend actions outside existing capture routes;
- workbook/webhook/App Script/Sheets/output transport changes;
- production behavior changes;
- OpenAI/model-provider or AI/coaching behavior;
- generated/private/local artifacts committed to Git;
- issue closure, PR creation, staging, commit, push, merge, or deployment unless
  explicitly requested in a later role.

## Compatibility

Implementation must preserve:

- existing explicit start/stop route behavior;
- existing live capture status response validation;
- existing stale-state fail-closed behavior;
- existing heartbeat/progress/no-row diagnostic shapes;
- existing analytics refresh-state endpoint shape;
- existing manual refresh buttons;
- existing Dashboard modules;
- existing Diagnostics route availability;
- existing safe display/redaction behavior;
- existing frontend hash navigation;
- existing no-destructive-controls posture.

## Tests Required

Codex C must add or update focused frontend tests proving:

- opening/loading the Dashboard does not call `startLiveCapture`;
- `Start capture` appears only when backend `start_allowed=true`;
- clicking `Start capture` calls the existing start helper once, disables repeat
  clicks while pending, and reconciles from `capture_status`;
- `Stop capture` appears only when backend `stop_allowed=true`;
- clicking `Stop capture` calls the existing stop helper once, disables repeat
  clicks while pending, and reconciles from `capture_status`;
- stale capture state does not show enabled Start, Stop, or Restart and keeps
  Diagnostics reachable;
- backend blurb text suggesting restart is displayed safely when action flags do
  not allow restart;
- a backend-supported recorded-match state can render one compact success line;
- analytics refresh-state updated/degraded/paused/checking states remain visible
  without claiming win/loss or match truth;
- manual refresh controls remain available;
- malformed capture or refresh payloads fail closed;
- no raw/private values, arbitrary SQL, destructive controls, external writes,
  AI/coaching claims, hidden-card claims, archetype truth, player-mistake labels,
  or best-line advice are introduced.

If Codex C changes API/type validation, frontend API tests must cover the new
safe shape. If Codex C changes Python/backend files, it must first confirm the
change is not backend lifecycle semantics; otherwise route back to Codex B.

## Validation Requirements

Codex C should run:

```powershell
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools/check_agent_docs.py
```

If Python/backend files are changed, Codex C must also run focused backend tests
for live capture and refresh state, likely:

```powershell
py -m pytest -q tests/test_live_app_explicit_start_capture_control.py tests/test_analytics_auto_refresh_after_match_completion.py tests/test_analytics_local_app_backend.py
py -m ruff check src tests tools
```

Codex C and Codex E must run path-scoped protected-surface and
secret/private-marker scans over changed files:

```powershell
@'
<changed file paths>
'@ | py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

@'
<changed file paths>
'@ | py tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

If `npm --prefix frontend run build` creates `frontend/dist`, remove generated
build output before handoff unless a later contract explicitly authorizes
committing it.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md`.
- Manual capture remains the default operator workflow.
- Automatic startup remains explicitly deferred.
- Dashboard workflow uses backend status/start/stop/refresh truth.
- Start/Stop controls are explicit, local-only, accessible, and governed by
  backend action flags.
- Stale/blocked states do not appear ready, restartable, or automatically
  recoverable.
- Post-match recording copy is backend-led and compact.
- Analytics refresh state is visible without frontend inference of match truth.
- Existing Diagnostics and manual refresh remain available.
- Protected parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/
  OpenAI/AI/coaching/production surfaces remain untouched.
- No raw/private/local artifact content is exposed or committed.
- Codex B made no implementation changes.

## Open Questions For Codex C

- Does the current Dashboard already satisfy enough of the #321 workflow that
  only tests and copy polish are needed?
- Is the existing `parser_status_blurb` safe and sufficient for the post-match
  success line, or should Codex C show the line only when
  `analytics_refresh_state.latest_completed_match_result_available=true` after a
  revision change?
- Are current manual refresh controls still visible enough after the Dashboard
  workflow polish?
- Does stale-state user copy point clearly to Diagnostics without implying
  cleanup or restart?

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match identity;
- game identity;
- deduplication;
- analytics schema or migrations;
- live ingest semantics;
- manual JSONL import semantics;
- saved-event replay semantics;
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
- archetype inference as truth;
- player-mistake labels;
- gameplay advice;
- credential policy or environment-variable contracts;
- secrets, credentials, API keys, tokens, webhook URLs, spreadsheet IDs,
  endpoint values, environment values, raw logs, generated SQLite files,
  runtime files, transport retry artifacts, workbook exports, frontend build
  output, app-data files, generated data, or local-only artifacts.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #321.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/321

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md

Target artifact:
docs/implementation_handoffs/live_app_frontend_capture_operator_workflow_refresh_comparison.md

Risk tier:
Medium-High if kept frontend/workflow-only; High if backend lifecycle, stale recovery, or automatic startup behavior changes are needed.

Goal:
Compare the current local app Dashboard capture workflow against the contract and implement only the smallest scoped operator-workflow refresh. Preserve the v1.0 decision that manual capture is the default and automatic startup remains deferred.

Before editing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and identify unrelated dirty or untracked files.
- Read the contract before changing anything.
- Read AGENTS.md, docs/agent_constitution.md, docs/agent_rules.yml, docs/codex_module_workflow.md, docs/agent_threads/implementation.md, and docs/templates/implementation_handoff.md.
- Inspect issue #321, tracker #136, related contracts #297/#304/#315/#302/#294, frontend live capture/analytics refresh code and tests, and backend live capture/refresh-state routes as reference.
- State what the operator workflow is supposed to do, what the app currently does, what gap remains, and the exact minimal implementation plan.

Do:
- Keep manual capture as the default operator workflow.
- Use existing backend GET /api/live/capture/status, POST /api/live/capture/start, POST /api/live/capture/stop, GET /api/analytics/refresh-state, and GET /api/analytics/dashboard/modules behavior.
- Keep backend live capture status as lifecycle truth and backend refresh-state as analytics revision truth.
- Make the Dashboard workflow understandable without PowerShell, raw JSON, or private artifact inspection for the normal path.
- Keep stale/blocked/failed/unavailable states fail-closed and route to Diagnostics.
- Add or update focused frontend tests for explicit start/stop, stale state, post-match recording copy, analytics refresh status, manual refresh availability, malformed payload handling, and privacy boundaries.
- Produce docs/implementation_handoffs/live_app_frontend_capture_operator_workflow_refresh_comparison.md.
- Preserve unrelated worktree changes.

Do not:
- Add automatic capture startup.
- Add stale cleanup, reset, delete, restart, recovery, or backend lifecycle behavior unless routed back through a new contract.
- Change backend route shapes or lifecycle semantics unless the contract is amended.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest semantics, manual JSONL import, saved-event replay, Match Journal truth ownership, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, hidden-card inference, archetype truth, player-mistake labels, or gameplay advice.
- Expose raw Player.log content, raw JSONL payloads, raw saved-event lines, raw private paths, raw hashes, generated SQLite contents, SQL text, stack traces, secrets, credentials, endpoint values, spreadsheet IDs, environment values, runtime files, transport retry artifacts, workbook exports, frontend build output, app-data files, generated data, or local-only artifacts.
- Add arbitrary SQL/database browsing, destructive controls, external writes, PR creation, issue closure, staging, commit, push, merge, or deployment unless explicitly asked.
- Target main.

Validation:
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools/check_agent_docs.py

If Python/backend files change, also run:
py -m pytest -q tests/test_live_app_explicit_start_capture_control.py tests/test_analytics_auto_refresh_after_match_completion.py tests/test_analytics_local_app_backend.py
py -m ruff check src tests tools

Run path-scoped protected-surface and secret/private-marker scans over changed files.
If npm build creates frontend/dist, remove generated build output before final handoff unless a later contract explicitly authorizes committing it.

Final handoff must include:
- role performed
- issue/tracker
- contract used
- branch and git status
- files inspected
- current behavior compared to contract
- implementation option chosen
- files changed
- exact frontend/backend/test/doc sections changed
- whether code changed, tests changed, docs-only, frontend-only, backend-only, or workflow-only
- validation run and result
- protected-surface status
- secret/private-marker status
- generated/private artifact status
- confirmation that manual capture remains default and automatic startup remains deferred
- confirmation that no backend lifecycle/stale recovery semantics changed unless routed back through contract authority
- confirmation that no parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed
- what remains unverified
- whether forbidden scope was touched
- next recommended role, likely Codex E: Module Reviewer / contract-test thread
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/321"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #321"
  contract_artifact: "docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md"
  target_artifact: "docs/implementation_handoffs/live_app_frontend_capture_operator_workflow_refresh_comparison.md"
  risk_tier: "Medium-High if kept frontend/workflow-only; High if backend lifecycle, stale recovery, or automatic startup behavior changes are needed"
  branch: "codex/analytics-foundation"
  internal_project_area: "Local App / UI"
  truth_owner: "Backend live capture status and analytics refresh-state own lifecycle/revision truth; frontend owns display/orchestration only"
  bridge_code_status: "bridge_code"
  decision: "Manual capture remains the v1.0 default operator workflow; automatic capture startup and stale recovery semantics remain deferred."
  validation:
    - "Codex B docs-only validation: git diff --check"
    - "Codex B docs-only validation: py tools\\check_agent_docs.py"
    - "Codex B docs-only validation: path-scoped protected-surface scan for the contract"
    - "Codex B docs-only validation: path-scoped secret/private-marker scan for the contract"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not add automatic capture startup."
    - "Do not add stale cleanup/reset/delete/restart/recovery behavior under issue #321."
    - "Do not change backend lifecycle semantics unless routed back through a new contract."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not expose raw/private/local artifacts, secrets, arbitrary SQL, destructive controls, external writes, or frontend-owned capture truth."
    - "Do not target main."
```
