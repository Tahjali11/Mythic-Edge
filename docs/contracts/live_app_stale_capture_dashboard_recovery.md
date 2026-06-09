# Live App Stale Capture Dashboard Recovery Contract

## Module

`live_app_stale_capture_dashboard_recovery`

Plain English: this contract defines how the Dashboard Live capture card should display and recover from stale capture state without implying that capture is ready, active, or safely restartable when the backend says it is not.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/315
- Related diagnostics issue: https://github.com/Tahjali11/Mythic-Edge/issues/302
- Related completed dashboard issue: https://github.com/Tahjali11/Mythic-Edge/issues/304
- Related merged PR: https://github.com/Tahjali11/Mythic-Edge/pull/313
- Current intended base branch: `codex/analytics-foundation`
- Working branch for this contract: `codex/live-app-stale-capture-dashboard-recovery-315`
- Risk tier: Medium if kept frontend-only; High if backend lifecycle or recovery behavior changes are needed.
- Role: Codex B / Module Contract Writer

## Tracker

N/A.

## Owning Layer

Primary owning layer: Local App / UI Dashboard.

Supporting layer: Local app backend owns live capture lifecycle truth through the existing `/api/live/capture/status`, `/api/live/capture/start`, and `/api/live/capture/stop` routes.

## Internal Project Area

Primary area: Local App / UI.

Adjacent area: Live Player.log Mode.

## Truth Owner

The backend live capture status owns whether capture is ready, stopped, starting, capturing, stopping, blocked, stale, failed, or unavailable.

The frontend owns presentation, layout stability, accessible labels, icon placement, operator copy, and temporary pending state while a backend request is in flight. The frontend must not become capture lifecycle truth, parser truth, analytics truth, live Player.log truth, or SQLite write truth.

Parser/state remains the owner of parser facts. SQLite remains downstream local analytics storage. Dashboard copy may explain capture status, but it must not infer match completion, row writes, Player.log contents, or whether a stale supervisor can be safely recovered.

## Bridge-Code Status

`bridge_code`

Allowed data flow:

```text
backend live capture status
  -> frontend Dashboard Live capture display
  -> operator-visible status/control/diagnostics affordance
```

Forbidden reverse flow:

- frontend labels, toggle styling, timers, route state, local pending state, or stale-copy mapping must not write parser state, live capture state, SQLite analytics facts, Match Journal records, workbook/webhook transport, production systems, or AI/coaching systems;
- the Dashboard must not auto-start, auto-stop, auto-restart, clean up, repair, delete, or overwrite stale capture state.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/live_app_stale_capture_dashboard_recovery.md`

Future Codex C implementation files authorized for the first slice:

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/src/api.ts`, only if validation or test injection needs a frontend-only status-display adjustment without route/schema changes
- `frontend/src/types.ts`, only if existing typed status fields need frontend-only display narrowing
- `frontend/src/status.ts`, only if existing label/tone helpers need display mapping updates
- `docs/implementation_handoffs/live_app_stale_capture_dashboard_recovery_comparison.md`

Reference-only surfaces:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `docs/contracts/analytics_app_dashboard_live_capture_control_clarity.md`
- `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`
- `docs/contracts/live_app_explicit_start_capture_control.md`

Not owned by this contract:

- backend live capture lifecycle semantics;
- parser modules;
- analytics schema, migrations, ingest, or query semantics;
- Match Journal behavior;
- workbook/webhook/App Script/Sheets behavior;
- OpenAI/model-provider or AI/coaching behavior;
- generated/private/local artifacts.

## Observed Current Behavior

Issue #304 and PR #313 completed the first Dashboard Live capture control clarity pass. The Dashboard now has a persistent live capture control area and uses backend `/api/live/capture/*` routes for start and stop behavior.

A real stale-state inspection exposed a remaining clarity gap. Backend status can report:

```json
{
  "status": "stale",
  "capture": {
    "running": false,
    "start_allowed": false,
    "stop_allowed": false,
    "reason": "capture_state_stale"
  },
  "parser_status_blurb": {
    "text": "Capture heartbeat stopped. Restart capture."
  }
}
```

The Dashboard can still present operator-facing copy that looks like `Ready to start` or can replace the action area with a larger diagnostics fallback. That makes the user-facing state ambiguous: the operator cannot quickly tell whether capture is merely stopped, stale, blocked, or safely restartable.

Current frontend code already treats `payload.state.stale` and `status=stale` as blocked for action selection. The remaining gap is display clarity and control consistency, not backend capture truth.

## Contract Decision

Use a persistent toggle-like lifecycle control plus a separate compact diagnostics icon.

Approved model:

- keep one stable Live capture card control area on the Dashboard;
- keep one stable lifecycle control in that area;
- keep a small diagnostics gear/icon affordance visible in the Live capture card;
- use explicit lifecycle labels for actions and accessible names;
- show stale as a needs-review/stale state, not `Ready to start`;
- do not show `Start capture`, `Stop capture`, or `Restart capture` for stale state unless the backend explicitly sets the corresponding safe action flag;
- do not let the frontend clear, repair, reset, or recover stale state.

Rejected for this slice:

- a true browser-owned on/off switch;
- a toggle that flips local truth before backend confirmation;
- replacing the main lifecycle control with a large `View diagnostics` fallback;
- hiding diagnostics when the lifecycle action is available;
- treating stale state as stopped or ready;
- adding a recovery endpoint, cleanup route, supervisor reset, or backend restart behavior.

## Public Interface

Existing backend/API interface to consume:

- `GET /api/live/capture/status`
- `POST /api/live/capture/start`
- `POST /api/live/capture/stop`
- `LiveCaptureStatusResponse`
- `LiveCaptureStartResult`
- `LiveCaptureStopResult`

Required frontend surface:

- Dashboard Live capture card with stable status, lifecycle control, and compact diagnostics affordance.

Optional display source:

- `parser_status_blurb.text`, if present and safe. Dashboard may map backend stale copy into a less action-implying message when backend action flags disallow restart.

## Inputs

### LiveCaptureStatusResponse

Source: backend `GET /api/live/capture/status`.

Fields this contract may use:

- `status`
- `capture.running`
- `capture.start_allowed`
- `capture.stop_allowed`
- `capture.reason`
- `capture.parser_runner_started`
- `capture.tailing_started`
- `capture.sqlite_live_writes_enabled`
- `capture.external_transport_allowed`
- `capture.raw_player_log_storage_enabled`
- `state.stale`
- `heartbeat.status`
- `progress.last_no_write_reason`
- `parser_status_blurb.code`
- `parser_status_blurb.text`
- `parser_status_blurb.tone`
- `warnings`
- `errors`

All warning, error, reason, heartbeat, and blurb values must be treated as safe labels or safe display strings only. The frontend must not display raw backend payloads, raw paths, raw Player.log content, raw hashes, stack traces, SQL, SQLite row contents, secrets, endpoint values, or environment values.

### Local Pending Action

Source: frontend state set after an explicit operator click and before backend response.

Allowed values:

- `start`
- `stop`
- none

Local pending state may disable repeated clicks and show `Starting` or `Stopping`. It must not mark capture as running, stopped, stale, or recovered after the backend response contradicts it.

## Outputs

### Dashboard Live Capture Card

Destination: local app Dashboard.

Required visible elements:

- label: `Live capture`;
- current state label from the state matrix below;
- compact plain-English status detail;
- stable lifecycle control;
- compact diagnostics gear/icon affordance;
- accessible action names for lifecycle and diagnostics controls.

The card must not show raw diagnostic payloads. Detailed counters, stale reasons, and no-row details belong in Diagnostics or issue #302 surfaces.

### Diagnostics Gear/Icon

Destination: Live capture card.

Required behavior:

- visible in the Live capture card across all lifecycle states;
- small and secondary to the lifecycle control;
- keyboard reachable;
- accessible name such as `View live capture diagnostics` or `Open live capture diagnostics`;
- routes to `#diagnostics` or the existing diagnostics route;
- does not start, stop, restart, reset, clear, delete, repair, upload, or inspect private files.

Implementation may use a gear icon only if the current frontend stack provides an appropriate icon system. If no icon library is already available, Codex C may use a simple text/icon treatment that remains accessible and visually compact.

## State Matrix

| Backend state | Required Dashboard label | Lifecycle control | Diagnostics affordance | Notes |
| --- | --- | --- | --- | --- |
| loading/checking | `Checking` | disabled checking control | visible when route is available | Do not show ready/start until backend status arrives. |
| `ready_to_start` or `stopped`, `running=false`, `start_allowed=true` | `Ready to start` or `Stopped` | enabled `Start capture` | visible | Capture is off but backend says start is safe. |
| local pending start or backend `starting` | `Starting` | disabled pending `Starting` | visible | Prevent duplicate clicks. |
| `capturing`, `running=true`, `stop_allowed=true` | `Capturing` | enabled `Stop capture` | visible | Only backend proof may produce active capture display. |
| local pending stop or backend `stopping` | `Stopping` | disabled pending `Stopping` | visible | Prevent duplicate clicks. |
| `stale` or `state.stale=true` | `Needs review` or `Stale` | disabled needs-review control unless backend explicitly allows an action | visible | Must not show `Ready to start`, `Start capture`, or `Restart capture` when `start_allowed=false`. |
| `blocked` | `Blocked` | disabled needs-review control unless backend explicitly allows an action | visible | Keep diagnostics available. |
| `failed` or `crashed` | `Failed` | disabled needs-review control unless backend explicitly allows an action | visible | Do not auto-retry. |
| `degraded`, `unknown`, contradictory fields, malformed payload | `Needs review` | disabled needs-review control | visible | Fail closed. |
| `unavailable` or API unavailable | `Unavailable` | disabled unavailable/checking control | visible if possible | Do not expose raw error details. |

Contradictory examples that must fail closed:

- `status=capturing` with `capture.running=false`;
- `status=ready_to_start` with `capture.running=true`;
- stale state with `start_allowed=false` but blurb text suggesting restart;
- missing capture flags;
- unsafe or malformed response shape.

## Stale-State Behavior

Stale state means the app-owned live capture heartbeat or state file stopped updating, or ownership is ambiguous. It does not mean the frontend may restart capture.

Required Dashboard stale copy:

- The status pill must not say `Ready to start`.
- The compact detail should say something close to: `Capture heartbeat stopped. Open diagnostics before starting again.`
- The lifecycle control should remain in place but disabled, with visible copy such as `Needs review` or `Stale`.
- The diagnostics gear/icon must remain visible.

Backend blurb handling:

- If backend blurb text says `Capture heartbeat stopped. Restart capture.` while `start_allowed=false`, the Dashboard must not render that as a direct `Restart capture` action.
- The Dashboard may render a safer paraphrase such as `Capture heartbeat stopped. Open diagnostics before starting again.`
- The Diagnostics route may show the backend-led blurb as long as it remains sanitized and does not become an enabled action.

Future recovery behavior:

- A stale-state cleanup, reset, restart, or recovery endpoint requires a separate issue and contract.
- This contract may identify the missing recovery path as a follow-up, but must not implement it.

## Frontend Control Model

Use one stable control area whose size and placement do not jump between start, stop, stale, blocked, and diagnostics states.

Recommended structure:

- status pill or label;
- primary lifecycle button/control slot;
- adjacent compact diagnostics icon/link.

The lifecycle control may be styled like a toggle if:

- it still uses explicit accessible names such as `Start capture`, `Stop capture`, `Starting capture`, `Stopping capture`, `Capture needs review`, or `Capture unavailable`;
- it does not use `role="switch"` unless the binary switch semantics are truthful for all supported states;
- it does not visually imply that stale capture is off and safe to start;
- it is disabled for stale/blocked/unavailable states unless backend action flags explicitly allow an action.

## Backend Lifecycle/Status Dependency

This issue should not change backend route behavior.

Codex C may rely on the existing backend guarantees:

- start is explicit and operator-controlled;
- stop is bounded to an app-owned supervisor;
- duplicate starts do not create duplicate supervisors;
- stale or ambiguous state blocks start/stop instead of being silently cleaned;
- active capture requires backend proof;
- external transport remains disabled;
- raw Player.log storage remains disabled.

If Codex C finds that the backend cannot distinguish stopped from stale, or cannot provide the needed action flags, Codex C must stop and route back to Codex B instead of changing backend lifecycle semantics under this contract.

## Accessibility Requirements

Codex C must ensure:

- lifecycle and diagnostics controls are keyboard reachable;
- lifecycle controls use real `<button>` elements when they trigger start or stop;
- diagnostics uses a real link or button with a clear accessible name;
- disabled states are visible and programmatically disabled where appropriate;
- stale state has text, not color alone;
- focus does not jump unexpectedly after start/stop responses;
- the diagnostics icon has a tooltip or visible/accessible label;
- the control layout fits mobile and desktop widths without overlapping text;
- no icon-only control lacks an accessible name.

## Scope Boundary With Related Issues

### Issue #302

#302 owns heartbeat/progress diagnostics, no-row reason vocabulary, and parser/capture status blurb semantics. This contract may display existing #302 fields and may refine stale display copy, but it must not add counters, new backend fields, state-file writes, no-row reasons, or diagnostic endpoint behavior.

### Issue #304

#304 owns the first persistent Dashboard control pass. This contract is a follow-up that corrects stale-state display and diagnostics affordance clarity. It should not reopen the whole dashboard control design.

### Issue #294

#294 owns analytics auto-refresh after completed match results. This contract must not implement analytics refresh-state polling, auto-refresh history/modules, or row-created detection.

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
- backend live capture lifecycle semantics;
- live capture state cleanup or recovery behavior;
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

- fail closed to `Needs review` or `Unavailable`;
- keep diagnostics reachable;
- do not show Start, Stop, or Restart;
- do not display raw payload details.

Start/stop failure:

- show safe failure copy;
- reconcile from backend response when available;
- preserve last safe state if available;
- do not retry automatically.

Missing #302 fields:

- use existing status, capture flags, and state stale flags;
- do not block #315 implementation.

## Side Effects

Allowed side effects:

- frontend render state;
- local pending start/stop UI state;
- explicit user-triggered calls to existing start/stop routes;
- URL hash/route navigation to Diagnostics;
- frontend tests;
- implementation handoff documentation.

Forbidden side effects:

- backend route or schema changes;
- parser changes;
- live capture supervisor behavior changes;
- stale state cleanup/reset/restart behavior;
- SQLite schema/migration/ingest changes;
- analytics auto-refresh behavior;
- external writes;
- local app data cleanup/reset/delete/repair actions;
- arbitrary SQL/database browsing;
- generated/private/local artifacts committed to Git;
- PR creation, issue closure, or tracker updates unless a later role is explicitly asked.

## Tests Required

Codex C must add or update focused frontend tests proving:

- stale capture status with `running=false`, `start_allowed=false`, `stop_allowed=false`, and `reason=capture_state_stale` does not show `Ready to start`;
- stale capture status does not show enabled `Start capture`, `Stop capture`, or `Restart capture`;
- stale capture status keeps the lifecycle control area visible with `Needs review` or `Stale` copy;
- stale capture status shows a compact diagnostics gear/icon affordance with accessible name and route;
- non-stale ready/stopped status still shows `Start capture`;
- capturing status still shows `Stop capture` when backend allows stop;
- blocked, failed, unavailable, malformed, and contradictory payloads fail closed while keeping diagnostics reachable;
- the diagnostics affordance remains visible in ready, capturing, stale, blocked, and unavailable states;
- no destructive controls, arbitrary SQL, raw-log viewing, private-path display, AI/coaching claims, hidden-card claims, player-mistake labels, or best-line claims are introduced.

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

## Acceptance Criteria

- `docs/contracts/live_app_stale_capture_dashboard_recovery.md` exists.
- Contract creates or uses focused issue #315.
- Contract keeps backend live capture status as lifecycle truth.
- Contract requires stale state to display as stale/needs-review, not ready-to-start.
- Contract requires a stable lifecycle control area and compact diagnostics gear/icon.
- Contract forbids frontend-owned restart/recovery behavior.
- Contract keeps #302 diagnostics and #294 auto-refresh separate.
- Protected surfaces remain untouched.
- No implementation code is changed by Codex B.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #315.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/315

Related issues:
- https://github.com/Tahjali11/Mythic-Edge/issues/302
- https://github.com/Tahjali11/Mythic-Edge/issues/304
- https://github.com/Tahjali11/Mythic-Edge/issues/294

Branch/base:
codex/analytics-foundation

Contract:
docs/contracts/live_app_stale_capture_dashboard_recovery.md

Goal:
Implement the frontend-focused stale capture Dashboard recovery/clarity slice. Keep backend live capture status as truth, show stale capture as needs-review/stale instead of ready-to-start, keep a stable lifecycle control area, and add a compact diagnostics gear/icon affordance.

Before editing:
- Confirm branch and git status.
- Identify unrelated dirty/untracked files and preserve them.
- Read issue #315, the contract, #302, #304, #294, frontend live capture code/tests/styles, and backend live_capture_control.py as reference only.
- State the minimal implementation plan.

Do:
- Keep this frontend-only unless a true contract blocker is found.
- Use existing GET /api/live/capture/status and existing start/stop helpers.
- Keep backend status and capture flags as lifecycle truth.
- Render stale state as Needs review/Stale, not Ready to start.
- Do not show Start, Stop, or Restart for stale state when backend start_allowed/stop_allowed are false.
- Keep the lifecycle control area stable.
- Add a compact diagnostics gear/icon link or button with accessible name.
- Keep diagnostics reachable in ready, capturing, stale, blocked, unavailable, malformed, and contradictory states.
- Add/update focused frontend tests.
- Produce docs/implementation_handoffs/live_app_stale_capture_dashboard_recovery_comparison.md.

Do not:
- change backend live capture lifecycle semantics, add stale recovery/reset/restart behavior, implement #302 diagnostics, implement #294 auto-refresh, change parser behavior, parser final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest, Match Journal truth ownership, workbook schema, webhook payload shape, Apps Script/Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice;
- expose raw Player.log content, raw JSONL, private paths, raw hashes, SQLite contents, SQL text, secrets, credentials, endpoint values, spreadsheet IDs, environment values, app-data files, generated/private/local artifacts, arbitrary SQL, database browsing, destructive controls, or external writes;
- target main, stage, commit, push, open a PR, merge, or close issue #315 unless explicitly asked.

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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/315"
  related_issues:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/302"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/304"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #315"
  contract_artifact: "docs/contracts/live_app_stale_capture_dashboard_recovery.md"
  target_artifact: "docs/implementation_handoffs/live_app_stale_capture_dashboard_recovery_comparison.md"
  risk_tier: "Medium frontend-only; High if backend lifecycle or recovery behavior changes are needed"
  branch: "codex/analytics-foundation"
  decision: "Use a stable Dashboard lifecycle control plus compact diagnostics gear/icon; stale state must show needs-review/stale copy and must not expose Start/Stop/Restart unless backend action flags explicitly allow it."
  validation:
    - "Codex B docs-only validation: git diff --check for the contract"
    - "Codex B docs-only validation: py tools\\check_agent_docs.py"
    - "Codex B docs-only validation: path-scoped protected-surface scan for the contract"
    - "Codex B docs-only validation: path-scoped secret/private-marker scan for the contract"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not change backend lifecycle semantics or add stale recovery/reset/restart behavior under issue #315."
    - "Do not implement issue #302 diagnostics or issue #294 auto-refresh under this slice."
    - "Do not treat frontend toggle styling as capture truth."
    - "Do not expose raw/private/local artifacts, secrets, arbitrary SQL, destructive controls, or external writes."
    - "Do not change parser/runtime/analytics schema/analytics ingest/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not target main."
```
