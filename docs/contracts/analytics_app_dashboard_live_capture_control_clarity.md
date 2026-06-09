# Analytics App Dashboard Live Capture Control Clarity Contract

## Module

`analytics_app_dashboard_live_capture_control_clarity`

Plain English: this contract defines how the Dashboard Live capture card should keep a stable, obvious start/stop control while preserving backend-owned live capture truth.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/304
- Current intended branch: `codex/analytics-foundation`
- Role: Codex B / Module Contract Writer
- Risk tier: Medium if kept frontend-only; High if backend/API lifecycle behavior changes are needed.

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/297 - explicit Start/Stop capture control, closed
- https://github.com/Tahjali11/Mythic-Edge/issues/299 - frontend information architecture, closed
- https://github.com/Tahjali11/Mythic-Edge/issues/302 - heartbeat, no-row diagnostics, and parser status blurb, open
- https://github.com/Tahjali11/Mythic-Edge/issues/294 - analytics auto-refresh after completed match result, open

## Tracker

N/A.

## Owning Layer

Primary owning layer: Local App / UI.

Supporting layer: Local app backend owns live capture lifecycle truth through the existing `/api/live/capture/*` routes.

## Internal Project Area

Primary area: Local App / UI.

## Truth Owner

The backend live capture status owns whether capture is stopped, starting, capturing, stopping, blocked, stale, failed, or unavailable.

The frontend owns presentation, control placement, accessible labels, disabled/pending UI states, and operator clarity. Frontend state may represent only a pending user command while waiting for the backend response. It must not become parser truth, capture-process truth, analytics truth, or live Player.log truth.

Parser/state remains the owner of parser facts. SQLite remains downstream analytics storage. The Dashboard may display capture status, but it must not infer match results, row writes, Player.log contents, or analytics freshness.

## Bridge-Code Status

`bridge_code`

Bridge details:

- Source internal project area: Live Player.log Mode / Local App Backend.
- Consuming internal project area: Local App / UI Dashboard.
- Allowed data flow: sanitized backend live capture status and start/stop results flow into frontend display and operator controls.
- Forbidden reverse flow: frontend route state, visual toggle state, local pending state, timers, or dashboard labels must not write parser state, live capture state, SQLite analytics facts, Match Journal records, workbook/webhook transport, production systems, or AI/coaching systems except through the existing explicit start/stop POST routes authorized by issue #297.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md`

Future Codex C implementation files authorized for the frontend-first slice:

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/src/api.ts`, only if existing live capture API helpers need display-safe reuse or test injection changes without route/schema changes
- `frontend/src/types.ts`, only if existing typed status fields need frontend-only display narrowing
- `frontend/src/status.ts`, only if existing label/tone helpers need display mapping updates
- `docs/implementation_handoffs/analytics_app_dashboard_live_capture_control_clarity_comparison.md`

Reference-only surfaces:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `docs/contracts/live_app_explicit_start_capture_control.md`
- `docs/contracts/analytics_app_frontend_information_architecture.md`

Not owned by this contract:

- parser modules
- analytics schema, migrations, ingest, or query semantics
- backend route inventory or response schemas
- live capture supervisor semantics
- Match Journal behavior
- workbook/webhook/App Script/Sheets behavior
- OpenAI/model-provider or AI/coaching behavior
- generated/private/local artifacts

## Observed Current Behavior

Issue #304 is open and asks for a stable Dashboard Live capture control pattern.

Current code already has:

- `GET /api/live/capture/status`
- `POST /api/live/capture/start`
- `POST /api/live/capture/stop`
- frontend helpers `fetchLiveCaptureStatus()`, `startLiveCapture()`, and `stopLiveCapture()`
- `LiveCaptureControlPanel` rendering `Start capture` or `Stop capture` based on backend `start_allowed` and `stop_allowed`
- tests that prove explicit backend control and no raw private data exposure for issue #297 behavior

The current Dashboard cockpit status rail has a `Live capture` status card, but the full explicit control panel is rendered only in the Diagnostics route. That means the Dashboard can show a state such as `Capturing` without keeping the operator's start/stop affordance in the same visible Dashboard card.

The expected #302 contract artifact is not present on the current branch during this pass. The #302 issue and current frontend types/code do reference heartbeat/progress and `parser_status_blurb` fields. This contract treats those fields as optional display dependencies only and does not implement or require the #302 diagnostic scope.

The current worktree also has an unrelated untracked contract artifact for issue #307. Future roles must preserve unrelated local files.

## Contract Decision

Use a persistent toggle-like lifecycle control, not a true frontend-owned on/off switch.

Approved model:

- one stable Dashboard Live capture card control area;
- one stable action slot in that area;
- visual treatment may look toggle-like if polished and clear;
- semantics remain lifecycle-button semantics, not independent switch truth;
- accessible action labels must be `Start capture`, `Stop capture`, or equivalent explicit lifecycle labels;
- the control's available action comes from backend `start_allowed` and `stop_allowed`;
- the displayed current state comes from backend `status` and `capture.running`;
- pending local UI state is temporary and must be reconciled with the backend result.

Rejected for this first slice:

- a true browser-owned toggle that flips local state before backend confirmation;
- a checkbox/switch ARIA role unless the implementation can truthfully satisfy binary switch semantics for all states;
- separate controls that appear and disappear in different card locations;
- hiding the stop action after successful start when backend `stop_allowed=true`;
- adding backend lifecycle fields or route behavior under this issue.

## Public Interface

Existing backend/API interface to consume:

- `GET /api/live/capture/status`
- `POST /api/live/capture/start`
- `POST /api/live/capture/stop`
- `LiveCaptureStatusResponse`
- `LiveCaptureStartResult`
- `LiveCaptureStopResult`

Required frontend surface:

- Dashboard Live capture card with persistent status and lifecycle control.

The Dashboard control may reuse the existing `LiveCaptureControlPanel` logic or introduce a smaller Dashboard-specific component, but it must keep behavior consistent with the Diagnostics control.

## Inputs

### LiveCaptureStatusResponse

Source: backend `GET /api/live/capture/status`.

Fields the frontend may use for this contract:

- `status`
- `capture.running`
- `capture.start_allowed`
- `capture.stop_allowed`
- `capture.parser_runner_started`
- `capture.tailing_started`
- `capture.sqlite_live_writes_enabled`
- `capture.external_transport_allowed`
- `capture.raw_player_log_storage_enabled`
- `capture.reason`
- `preconditions`
- `state.stale`
- `parser_status_blurb.text`, if present
- `warnings`
- `errors`

The frontend must treat all warning/error strings as safe labels only. It must not display raw stack traces, raw paths, raw Player.log content, SQL text, SQLite row contents, environment values, endpoint values, secrets, or generated artifact contents.

### Local pending action

Source: frontend state set immediately after an explicit button click and before backend response.

Allowed values:

- `start`
- `stop`
- none

Local pending state may disable repeated clicks and show `Starting` or `Stopping` copy. It must not mark capture as running or stopped after the backend response contradicts it.

## Outputs

### Dashboard Card

Destination: local app Dashboard.

Required visible elements:

- heading or label: `Live capture`
- current state label from the state vocabulary below
- compact plain-English detail text
- stable lifecycle control area
- accessible action name when an action is available
- disabled/pending state when a start or stop request is in flight
- route or details affordance to Diagnostics when blocked, unavailable, stale, failed, or needs review

The Dashboard card must not show raw diagnostic payloads. Detailed counters and no-row reasons belong to #302 or Diagnostics.

### Diagnostic Control Compatibility

The existing Diagnostics `Live Capture Control` may remain. If Codex C factors shared helpers, Dashboard and Diagnostics must agree on status labels and action availability.

## State Vocabulary

The UI must represent these operator-facing states:

| UI state | Backend source | Action behavior |
| --- | --- | --- |
| `stopped` | `status` is `ready_to_start` or `stopped`, `capture.running=false`, `start_allowed=true` | show stable `Start capture` action |
| `starting` | backend `status=starting` or local pending `start` | show disabled pending action; do not allow repeated clicks |
| `capturing` | `status=capturing` and `capture.running=true` | show stable `Stop capture` action when `stop_allowed=true`; otherwise show active state plus diagnostics route |
| `stopping` | backend `status=stopping` or local pending `stop` | show disabled pending action; do not allow repeated clicks |
| `blocked` | backend `status` is `blocked`, `failed`, `crashed`, `stale`, `degraded`, `unknown`, or contradictory fields are detected | show no misleading start/stop action; route to Diagnostics |
| `unavailable` | no status payload, backend unavailable, incompatible response, or backend `status=unavailable` | show no start/stop action; route to Diagnostics |

The implementation may display `Needs review` as user-facing copy for stale, degraded, unknown, or contradictory states, but the contract-level behavior is `blocked`: no misleading action until backend truth is safe enough.

`Capturing` requires backend proof. Frontend pending state alone is not enough.

## Frontend Control Model

The Dashboard should use one persistent control area whose size and placement remain stable across state changes.

Recommended shape:

- a compact state pill or label;
- one action button slot;
- `Start capture` in stopped state;
- `Starting...` disabled while start is pending;
- `Stop capture` in capturing state when allowed;
- `Stopping...` disabled while stop is pending;
- `View diagnostics` or equivalent non-destructive route action for blocked/unavailable states.

The control may be styled like a toggle only if:

- it does not use misleading binary switch semantics;
- it keeps explicit start/stop labels available to screen readers;
- it does not move, resize dramatically, or vanish when the state changes;
- it respects backend `start_allowed` and `stop_allowed`.

The action area must not disappear after Start Capture succeeds. If capture is active and backend says stop is allowed, the same area must present Stop Capture.

## Backend Lifecycle/Status Dependency

This issue should not change backend route behavior.

Codex C may rely on existing backend guarantees from `live_app_explicit_start_capture_control.md`:

- start is explicit and operator-controlled;
- stop is bounded to an app-owned supervisor;
- duplicate starts do not create duplicate supervisors;
- stale or ambiguous state blocks instead of being silently cleaned;
- active capture requires supervisor running, tailing started, and SQLite live writes enabled;
- external transport remains disabled;
- raw Player.log storage remains disabled.

If Codex C finds that current backend status cannot truthfully support the Dashboard control, Codex C must stop and route back to Codex B instead of changing backend lifecycle semantics under this contract.

## Accessibility Requirements

Codex C must ensure:

- the control is keyboard reachable;
- buttons use real `<button>` elements or equivalent accessible semantics;
- available actions have accessible names such as `Start capture` and `Stop capture`;
- pending actions expose disabled state and visible text such as `Starting` or `Stopping`;
- status is not conveyed by color alone;
- the current status has an accessible text label;
- control layout remains stable at supported desktop and mobile widths;
- focus does not jump unexpectedly after start/stop responses;
- blocked/unavailable states have an accessible route or explanation for next inspection;
- any toggle-like styling does not rely on ARIA `switch` unless all switch semantics are truthful.

## Pending, Blocked, And Unavailable Behavior

Pending:

- disable the active lifecycle action while the request is in flight;
- keep the control in place;
- show `Starting` or `Stopping`;
- do not fire duplicate requests;
- after response, reconcile from `result.capture_status`.

Blocked:

- do not show Start or Stop unless backend flags explicitly allow the action;
- show safe copy such as `Capture blocked` or `Needs review`;
- provide route to Diagnostics;
- do not auto-clean, reset, delete, or repair state.

Unavailable:

- show `Unavailable` or `Checking` as appropriate;
- do not show Start or Stop;
- preserve Dashboard readability;
- keep Diagnostics reachable;
- do not dump raw backend error details.

Contradictory payloads:

- fail closed to blocked/needs-review display;
- do not mark capture active when `status=capturing` but `capture.running=false`;
- do not mark capture stopped when a pending stop has not been confirmed by the backend.

## Scope Boundary With Related Issues

### Issue #297

#297 owns the existing backend explicit Start/Stop control routes and lifecycle safety semantics. This contract consumes those routes and does not redefine supervisor ownership, start preconditions, stop ownership proof, SQLite write path, or external transport boundaries.

### Issue #302

#302 owns heartbeat/progress diagnostics, no-row reason vocabulary, and parser/capture status blurb semantics. This contract may display a backend-provided `parser_status_blurb.text` if present, but it must not add counters, no-row reason fields, heartbeat storage, or diagnostic endpoint behavior.

If `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md` remains absent during implementation, Codex C must use issue #302 and current code as context only and avoid implementing #302 under this issue.

### Issue #294

#294 owns analytics auto-refresh after completed match results. This contract must not implement polling refresh-state, auto-refresh history/modules, or win/loss refresh claims. The Dashboard Live capture card may say capture is active or stopped, but it must not claim analytics views have refreshed.

### Issue #299

#299 owns app-shell information architecture. This contract fits inside the Dashboard cockpit created there and may refine the Live capture card. It must not reopen the broader shell redesign.

## Privacy And Protected Surface Rules

Do not expose in UI, API responses, tests, reports, screenshots, committed files, or durable artifacts:

- raw Player.log content;
- raw JSONL payloads;
- raw saved-event lines;
- raw hashes;
- private local paths;
- generated SQLite contents;
- SQL text;
- runtime logs;
- app-data files;
- failed posts;
- workbook exports;
- secrets;
- credentials;
- tokens;
- API keys;
- webhook URLs;
- spreadsheet IDs;
- environment values;
- local-only artifacts.

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- live capture backend lifecycle semantics;
- analytics schema, migrations, ingest, or query semantics;
- Match Journal truth ownership;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport or production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- hidden-card inference;
- archetype inference;
- player-mistake labels;
- gameplay advice.

## Error Behavior

Malformed status payload:

- frontend validation must fail closed;
- Dashboard shows unavailable or needs-review status;
- no raw response content is displayed.

Start/stop failure:

- show safe failure copy;
- preserve last safe status if available;
- do not retry automatically;
- keep Diagnostics reachable.

Backend unavailable:

- show unavailable status;
- do not expose stack traces or endpoint details;
- do not create local artifacts.

Missing #302 fields:

- omit parser blurb or use existing safe capture detail;
- do not block #304 implementation.

## Side Effects

Allowed side effects:

- frontend render state;
- local pending start/stop UI state;
- user-triggered calls to existing `/api/live/capture/start` and `/api/live/capture/stop`;
- URL hash/route navigation to Diagnostics;
- frontend tests;
- implementation handoff documentation.

Forbidden side effects:

- backend schema or route changes;
- parser changes;
- live capture supervisor behavior changes;
- SQLite schema/migration/ingest changes;
- analytics auto-refresh behavior;
- external writes;
- local app data cleanup/reset/delete/repair actions;
- arbitrary SQL/database browsing;
- generated/private/local artifacts committed to Git;
- PR creation, issue closure, or tracker changes unless a later role is explicitly asked.

## Tests Required

Codex C must add or update frontend tests proving:

- Dashboard Live capture card renders a persistent control area.
- Stopped/ready state shows `Start capture` in the stable action slot.
- Starting state disables repeat clicks and shows pending copy.
- Capturing state shows `Stop capture` in the same action slot when `stop_allowed=true`.
- Stopping state disables repeat clicks and shows pending copy.
- Blocked state shows no misleading Start/Stop action and provides a diagnostics route or equivalent next step.
- Unavailable or malformed status shows no Start/Stop action.
- `status=capturing` with `capture.running=false` fails closed instead of showing active capture.
- Start and Stop calls use existing API helpers and reconcile from `capture_status`.
- Accessible names exist for current status and available action.
- No destructive controls, arbitrary SQL, raw-log viewing, private-path display, AI/coaching claims, hidden-card claims, player-mistake labels, or best-line claims are introduced.

Recommended validation:

```powershell
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
```

Codex C and Codex E must run path-scoped protected-surface and secret/private-marker scans over changed files:

```powershell
@'
<changed file paths>
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

@'
<changed file paths>
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

If `npm --prefix frontend run build` creates `frontend/dist`, generated build output must be removed before handoff unless a later contract explicitly authorizes committing it.

If Codex C changes Python/backend files, it must stop first unless the change is a narrow test-injection or type-support necessity that does not alter backend route behavior. Any backend lifecycle or schema change must route back to Codex B.

## Acceptance Criteria

- `docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md` exists.
- Contract chooses a persistent toggle-like lifecycle control, not a true frontend-owned switch.
- Dashboard Live capture card keeps stable status and control placement across stopped, starting, capturing, stopping, blocked, and unavailable states.
- Backend status remains the source of lifecycle truth.
- Frontend pending state is temporary and reconciles from backend result.
- Blocked/unavailable states do not show misleading start/stop controls.
- Accessibility requirements are explicit and testable.
- Scope boundaries with #302 diagnostics and #294 auto-refresh are explicit.
- Protected surfaces remain untouched.
- No implementation changes are made in Codex B.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #304.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/304

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md

Goal:
Implement the frontend-first Dashboard Live capture persistent control clarity slice. Use a stable toggle-like lifecycle control area on the Dashboard, while preserving backend-owned live capture lifecycle truth and existing start/stop API behavior.

Before editing:
- Confirm branch and git status.
- Identify unrelated dirty or untracked files and preserve them, including any issue #307 contract artifact.
- Read the contract, issue #304, issue #297, issue #302, issue #294, and the frontend/backend files named in the contract.
- Inspect current Dashboard Live capture card, Diagnostics Live Capture Control panel, API helpers, types, status helpers, and tests.
- State the minimal implementation plan.

Do:
- Keep this frontend-first unless a true backend blocker is found.
- Add or refactor a stable Dashboard Live capture control area.
- Use existing GET /api/live/capture/status, POST /api/live/capture/start, and POST /api/live/capture/stop helpers.
- Render stopped, starting, capturing, stopping, blocked, and unavailable states clearly.
- Keep Start/Stop controls in a stable location and reconcile all results from backend capture_status.
- Disable repeat clicks during pending start/stop.
- Fail closed for blocked, unavailable, malformed, stale, failed, or contradictory status.
- Keep Diagnostics reachable for blocked/unavailable states.
- Add/update focused frontend tests.
- Produce docs/implementation_handoffs/analytics_app_dashboard_live_capture_control_clarity_comparison.md.

Do not:
- change parser behavior, parser final reconciliation, parser event classes, match/game identity, deduplication, backend live capture lifecycle semantics, analytics schema/migrations/ingest, analytics auto-refresh from #294, heartbeat/no-row diagnostics from #302, Match Journal truth ownership, workbook schema, webhook payload shape, Apps Script/Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice;
- expose raw Player.log content, raw JSONL, private paths, raw hashes, SQLite contents, SQL text, secrets, credentials, endpoint values, spreadsheet IDs, environment values, app-data files, generated/private/local artifacts, arbitrary SQL, database browsing, destructive controls, or external writes;
- target main, stage, commit, push, open a PR, merge, or close issue #304 unless explicitly asked.

Validation:
- npm --prefix frontend run typecheck
- npm --prefix frontend run test -- --run
- npm --prefix frontend run build
- git diff --check
- py tools/check_agent_docs.py
- path-scoped protected-surface and secret/private-marker scans over changed files
- remove frontend/dist before final handoff if build created it

Final output:
- role performed
- issue and contract used
- branch and git status
- files changed
- implementation summary
- validation run and results
- protected-surface/private-artifact status
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/304"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #304"
  contract_artifact: "docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md"
  target_artifact: "docs/implementation_handoffs/analytics_app_dashboard_live_capture_control_clarity_comparison.md"
  risk_tier: "Medium frontend-only; High if backend/API lifecycle changes are needed"
  branch: "codex/analytics-foundation"
  decision: "Use a persistent toggle-like lifecycle control in the Dashboard; backend capture status remains lifecycle truth."
  validation:
    - "Codex B docs-only validation: git diff --check"
    - "Codex B docs-only validation: py tools\\check_agent_docs.py"
    - "Codex B docs-only validation: path-scoped protected-surface scan for the contract"
    - "Codex B docs-only validation: path-scoped secret/private-marker scan for the contract"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not change backend lifecycle semantics under issue #304."
    - "Do not implement issue #302 heartbeat/no-row diagnostics under this slice."
    - "Do not implement issue #294 analytics auto-refresh under this slice."
    - "Do not change parser/runtime/analytics schema/analytics ingest/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not expose raw/private/local artifacts, secrets, arbitrary SQL, destructive controls, or frontend-owned capture truth."
    - "Do not target main."
```
