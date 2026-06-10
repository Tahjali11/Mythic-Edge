# Local App Live Capture Status Truthful Display Contract

## Module

`local_app_live_capture_status_truthful_display`

Plain English: this contract makes the local app cockpit tell the truth about
Live Player.log capture. A detected Player.log file or a ready watcher
precondition must not look like active SQLite capture when no watcher/parser
process is running and live SQLite writes are disabled.

This is a contract-writing artifact only. It does not implement code, start a
watcher, change live ingest, change analytics refresh behavior, or change
parser/runtime behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/295
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/294
- Branch observed during this Codex B pass: `codex/analytics-foundation`
- Risk tier: Medium

Observed local branch state during this pass:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation [behind 9]
 M docs/project_roadmap.md
```

The existing `docs/project_roadmap.md` modification was present before this
contract-writing pass and is out of scope. Codex C must reconcile the intended
base branch and preserve unrelated local work before implementation.

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- GitHub issue `#295`
- GitHub issue `#294`
- `docs/contracts/live_app_player_log_path_watcher_status.md`
- `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`
- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`
- `docs/contracts/live_player_log_v1_supported_readiness.md`
- `docs/contracts/analytics_app_first_screen_competitive_cockpit.md`
- `docs/contracts/analytics_dynamic_decision_support_dashboard.md`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `frontend/src/App.tsx`
- `frontend/src/status.ts`
- `frontend/src/types.ts`
- `frontend/src/App.test.tsx`
- `frontend/src/status.test.ts`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_live_app_parser_owned_fact_capture_sqlite.py`

## Tracker

N/A.

Issue `#294` and this issue are post-private-local-v1 follow-up issues rather
than children that reopen closed analytics/local-app trackers.

## Owning Layer

Primary owning layer: Local App / UI status translation.

Supporting layers:

- local app backend status composition;
- live watcher readiness and process-control status;
- live SQLite capture status;
- analytics/SQLite as downstream storage;
- frontend cockpit display.

The frontend owns user-facing labels, tone mapping, details text, and default
first-screen hierarchy. It does not own parser facts, live capture truth,
watcher process truth, SQLite write truth, analytics truth, or match result
truth.

## Internal Project Area

Local App / UI.

Adjacent areas:

- Live Player.log Mode;
- Analytics;
- Quality / operator safety.

## Truth Owner

Truth ownership remains unchanged:

- Parser/state owns match/game/event truth and final reconciliation.
- Live watcher/process surfaces own only watcher readiness/process status.
- Live SQLite capture status owns whether live SQLite writes are enabled,
  disabled, status-only, or blocked.
- SQLite stores parser-normalized facts after an approved ingest path writes
  them; it does not create parser truth.
- The frontend displays and explains status only.

The cockpit must not convert Player.log readiness, watcher readiness, manual
refresh, browser state, timers, analytics query state, or optimistic UI wording
into evidence that live capture is active.

## Bridge-Code Status

`bridge_code`

Allowed data flow:

```text
backend setup/live watcher/process/live SQLite capture status
  -> frontend validation/redaction
  -> user-facing Live capture cockpit summary
  -> diagnostics/details when needed
```

Forbidden reverse flow:

- frontend labels must not rewrite backend status;
- `Refresh History` must not imply live capture occurred;
- browser state must not become parser, watcher, ingest, or analytics truth.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/local_app_live_capture_status_truthful_display.md`

Future Codex C may touch, subject to comparison and validation:

- `frontend/src/App.tsx`
- `frontend/src/status.ts`
- `frontend/src/types.ts`, only if the existing live SQLite capture type shape
  needs to be represented for display
- `frontend/src/App.test.tsx`
- `frontend/src/status.test.ts`
- optional focused backend tests only if a current backend payload is
  incomplete or inconsistent with the existing status contracts
- `docs/implementation_handoffs/local_app_live_capture_status_truthful_display_comparison.md`

Future Codex C must not change parser code, analytics schema/migrations,
analytics ingest semantics, live watcher process behavior, live capture
semantics, Match Journal truth ownership, workbook/webhook/App Script/Sheets
behavior, production behavior, OpenAI/AI/coaching behavior, or generated/private
artifacts unless a later contract explicitly authorizes that scope.

## Observed Current Behavior

Issue `#295` reports a user-facing trust drift:

- the local app backend was healthy;
- setup status was degraded;
- Player.log status was `ok`;
- live watcher readiness was `ready`;
- watcher process status was `not_initialized`;
- live capture status was `disabled`;
- parser runner was not started;
- tailing was not started;
- SQLite live writes were disabled;
- analytics database status was `ok`;
- privacy boundary was enforced.

The important distinction:

- Player.log and watcher readiness were good enough to say the app could see a
  candidate log source.
- Live capture was not actually running and writing SQLite rows.

Current frontend code shape observed in `frontend/src/App.tsx`:

```text
liveCaptureStatus = watcher.running ? "capturing" : watcher.status
```

That means `watcher.status = "ready"` can flow into the first-screen `Live
capture` card even when `watcher.running = false` and
`sqlite_live_writes_enabled = false`.

Current backend code already exposes stricter evidence:

- `build_live_sqlite_capture_status(...)` returns `status = "disabled"` and
  `mode = "status_only"`;
- live SQLite capture capabilities report supported contract boundaries but
  `process_control.sqlite_live_writes_enabled = false`;
- `build_live_watcher_status(...)` reports `mode = "readiness_only"`,
  `running = false`, `parser_runner_started = false`, `tailing_started =
  false`, and `sqlite_live_writes_enabled = false`;
- `build_live_watcher_process_status(...)` reports safeguards/process control
  without enabling start/stop routes.

## Contract Decision

Issue `#295` should authorize a narrow status-display correction.

Approved first slice:

- make the first-screen `Live capture` card derive its default summary from the
  strictest live-capture evidence available;
- distinguish Player.log readiness, watcher readiness, watcher process state,
  and live SQLite capture state;
- ensure `ready + running:false + sqlite_live_writes_enabled:false` never
  renders as active or reassuring live capture;
- keep manual refresh available, but explain that refresh cannot create rows
  when live capture is disabled;
- add focused frontend tests for the misleading status case.

Not approved:

- implement or change live parser ingest;
- start or stop watcher processes;
- add watcher controls;
- change live SQLite capture semantics;
- change analytics auto-refresh behavior from issue `#294`;
- change backend route shapes unless Codex C finds a small display-blocking
  omission and routes it explicitly;
- change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/
  OpenAI/AI/coaching/production behavior.

## Status Source Priority

The first-screen `Live capture` card must evaluate status in this priority
order:

1. `live_sqlite_capture.status`, `mode`, and
   `process_control.sqlite_live_writes_enabled`;
2. `live_watcher_process.process_control` flags, especially
   `parser_runner_started`, `tailing_started`, and
   `sqlite_live_writes_enabled`;
3. `live_watcher.watcher.running`, `tailing_started`,
   `parser_runner_started`, and `sqlite_live_writes_enabled`;
4. `live_watcher.watcher.status` as readiness-only detail;
5. `live_player_log.player_log.status` as Player.log source detail only.

Rules:

- `live_sqlite_capture.status = "disabled"` must make the card say not
  capturing, limited, disabled, or equivalent.
- `live_sqlite_capture.mode = "status_only"` must not display as active
  capture.
- `watcher.status = "ready"` must not override
  `sqlite_live_writes_enabled = false`.
- `watcher.running = false` must not display as active capture.
- Player.log `configured_exists` or `detected_exists` may support a Player.log
  monitor label, not a live capture label.
- Unknown or missing capture fields must fail closed to `Needs review`,
  `Limited data`, `Not capturing`, or equivalent, not `Ready` or `Capturing`.

## Status Vocabulary

Approved first-screen Live capture labels:

- `Capturing`
- `Not capturing`
- `Waiting for Arena activity`
- `Capture disabled`
- `Setup needed`
- `Needs review`
- `Blocked`
- `Limited data`
- `Unavailable`

`Capturing` is allowed only when supported evidence says all of these are true:

- a watcher/capture source is running;
- parser runner or approved live capture path is active;
- tailing or approved capture input is active;
- SQLite live writes are enabled or a successful live write was reported by
  the approved live capture status surface.

Current known issue `#295` state must display as `Not capturing`, `Capture
disabled`, or `Limited data`, not `Ready` and not `Capturing`.

The generic label `Ready` should not appear on the first-screen `Live capture`
card when:

- `sqlite_live_writes_enabled = false`;
- `live_sqlite_capture.status = "disabled"`;
- `mode = "status_only"`;
- watcher mode is `readiness_only`;
- process-control mode is `safeguards_only`;
- watcher is not running.

`Ready` may remain valid for the separate Player.log monitor or setup detail
when it is clearly scoped to readiness.

## Frontend Display Rules

The first-screen `Live capture` card must:

- display a user-facing label from the approved vocabulary;
- set `liveActive` true only when the label is `Capturing` and strict capture
  evidence supports it;
- include detail text that explains disabled or waiting states without telling
  the user to trust missing analytics rows;
- keep diagnostics/details reachable for the raw readiness/process labels;
- preserve `safeDisplayValue(...)` or equivalent redaction for all values.

Required detail text behavior:

- If live capture is disabled:
  - explain that Player.log may be detected while live SQLite capture is not
    running.
  - explain that manual refresh can only show rows already stored in SQLite.
- If watcher readiness is ready but process/capture is not running:
  - explain that the app is ready to monitor but is not currently collecting
    live analytics.
- If capture is blocked:
  - point the user to setup/live diagnostics.
- If capture is active:
  - use concise wording such as `Live capture is active.`

Forbidden first-screen implications:

- do not say or imply that analytics will update after a match unless live
  SQLite writes are active or a successful live write is visible;
- do not imply `Refresh History` causes capture;
- do not display raw backend labels such as `readiness_only`,
  `safeguards_only`, `status_only`, `sqlite_live_writes_enabled`, `tailing`, or
  `parser_runner_started` in the compact first-screen card unless inside a
  diagnostics/details surface.

## Backend Contract

No backend route changes are required by this contract if current setup status
already includes:

- `live_watcher`;
- `live_watcher_process`;
- `live_sqlite_capture`;
- safe booleans for running/tailing/parser-runner/SQLite-write state.

Codex C may add backend fields or tests only if current payloads cannot support
the truthful display rules. Any backend addition must be backward-compatible,
read-only, sanitized, loopback/local-app scoped, and status-only.

Backend must not:

- start or stop watcher processes;
- tail, read, copy, hash, or store raw Player.log content;
- write SQLite rows from GET routes;
- expose raw local paths, raw hashes, SQL text, generated database contents,
  stack traces, secrets, credentials, tokens, API keys, webhook URLs,
  spreadsheet IDs, environment values, runtime logs, or local-only artifacts.

## Relationship To Issue #294

Issue `#294` is downstream and separate.

This issue answers:

- does the UI honestly tell the operator that live capture is disabled or not
  writing rows?

Issue `#294` answers:

- when SQLite does receive new parser-owned facts, can the UI auto-refresh
  analytics views?

Codex C must not implement the `#294` polling/refresh-state endpoint in this
issue unless the user explicitly combines the scopes through a new contract.

## Inputs

Allowed frontend inputs:

- validated setup status payloads;
- `live_sqlite_capture.status`;
- `live_sqlite_capture.mode`;
- `live_sqlite_capture.process_control.sqlite_live_writes_enabled`;
- `live_watcher_process.process_control` disabled/running flags;
- `live_watcher.watcher.status`;
- `live_watcher.watcher.mode`;
- `live_watcher.watcher.running`;
- `live_watcher.watcher.parser_runner_started`;
- `live_watcher.watcher.tailing_started`;
- `live_watcher.watcher.sqlite_live_writes_enabled`;
- `live_player_log.player_log.status`;
- sanitized warnings and errors.

Forbidden frontend inputs:

- raw Player.log content;
- raw log lines;
- raw JSONL payloads;
- raw private paths;
- raw hashes from private files;
- generated SQLite contents outside approved API responses;
- arbitrary SQL output;
- secrets, credentials, tokens, endpoint values, spreadsheet IDs, environment
  values, stack traces, local usernames, or local-only artifact contents.

## Outputs

Allowed outputs:

- frontend status labels;
- frontend detail text;
- frontend-only status helper behavior;
- focused frontend tests;
- implementation handoff.

Forbidden outputs:

- new parser facts;
- new analytics facts;
- raw/private data display;
- watcher controls;
- live capture controls;
- generated database files;
- runtime files;
- committed frontend build output;
- public/production/AI/coaching/Line Tracer claims.

## Invariants

- Parser truth stays upstream.
- SQLite capture state must not be inferred from Player.log readiness alone.
- Watcher readiness must not be displayed as active capture.
- `disabled`, `status_only`, `readiness_only`, and `safeguards_only` must not
  become `Ready` on the Live capture card.
- `Capturing` requires direct supported capture evidence.
- Manual refresh remains a display/query action, not a capture action.
- Unknown/malformed/missing status must fail closed.
- Raw/private values remain redacted or excluded.

## Error Behavior

Malformed or incompatible setup/live status payload:

- display `Needs review`, `Limited data`, or `Unavailable`;
- keep manual refresh available when safe;
- do not display `Ready` or `Capturing`;
- route details to diagnostics if safe.

Missing `live_sqlite_capture` field:

- use watcher/process flags only as fallback;
- if no strict live-write flag is available, do not display active capture.

Conflicting status:

- blocked/error values outrank ready values;
- disabled/status-only values outrank watcher readiness;
- active capture requires consistent running/write evidence.

Unsafe display value:

- use existing redaction behavior;
- show safe fallback text;
- never echo the unsafe value.

## Side Effects

Codex B may write only this contract.

Future Codex C may edit frontend source/tests and create an implementation
handoff. Backend edits are allowed only if strictly necessary for display
truthfulness and must remain read-only/status-only.

Forbidden side effects:

- process start/stop/spawn/kill;
- Player.log tail/read/hash/copy/store;
- SQLite ingest changes;
- analytics schema or migration changes;
- generated/private/runtime/local artifact creation or commits;
- workbook/webhook/App Script/Sheets/output transport/production/OpenAI/AI/
  coaching/Line Tracer behavior changes;
- issue closure, staging, commit, push, PR creation, merge, or deployment unless
  explicitly requested in a later role.

## Compatibility

Implementation must preserve:

- existing setup-status route compatibility;
- existing live Player.log status route compatibility;
- existing live watcher status route compatibility;
- existing watcher process-control route compatibility;
- existing live ingest status route compatibility;
- existing analytics history and Decision Support behavior;
- existing manual refresh buttons;
- existing diagnostics/details availability;
- existing safe display/redaction behavior;
- existing no-destructive-controls posture.

## Tests Required

Codex C must add or update frontend tests proving:

- `ready + running:false + sqlite_live_writes_enabled:false` does not render
  the first-screen Live capture card as `Ready` or `Capturing`;
- `live_sqlite_capture.status = "disabled"` and `mode = "status_only"` render
  as disabled/not-capturing/limited;
- `liveActive` is false when watcher readiness is ready but live SQLite writes
  are disabled;
- `Capturing` appears only when strict running/write evidence is supplied by
  approved status fields;
- manual refresh remains available but is not described as starting capture;
- diagnostics/details still expose safe technical context when needed;
- unsafe values remain redacted;
- unknown/malformed payloads fail closed.

If backend payload code is touched, Codex C must add or update backend tests
proving:

- setup status includes enough strict live capture fields for frontend display;
- GET status routes remain read-only and do not create generated/private files;
- no raw paths, Player.log contents, raw hashes, secrets, SQL, or generated DB
  contents appear in responses.

Recommended validation:

```powershell
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run frontend/src/App.test.tsx frontend/src/status.test.ts
py -m pytest -q tests/test_analytics_local_app_backend.py
git diff --check
py tools/check_agent_docs.py
```

If Codex C changes frontend build-sensitive files:

```powershell
npm --prefix frontend run build
```

If `npm --prefix frontend run build` creates `frontend/dist`, Codex C must
remove generated build output before final handoff unless a later contract
explicitly authorizes committing it.

Codex C/E must run path-scoped protected-surface and secret/private-marker
scans over changed files.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/local_app_live_capture_status_truthful_display.md`.
- Contract distinguishes Player.log readiness, watcher readiness, watcher
  process state, live SQLite capture state, and analytics refresh.
- Contract defines backend field priority rules for the first-screen Live
  capture card.
- Contract defines user-facing status vocabulary.
- Contract forbids `Ready` or `Capturing` for the known disabled-capture state.
- Contract preserves manual refresh while clarifying it cannot create missing
  live rows.
- Contract defines focused frontend tests.
- Contract preserves parser/runtime/analytics/workbook/webhook/App Script/
  Sheets/OpenAI/AI/coaching/production protected surfaces.
- Contract routes next to Codex C.

## Open Questions

- Whether the final implementation should add a dedicated frontend helper such
  as `cockpitLiveCaptureStatusFromSetupPayload(...)` or keep the logic inside
  the existing cockpit summary builder.
- Whether backend setup status should eventually expose one precomputed
  `live_capture_summary` object. That is not required for this issue if the
  frontend can derive a truthful label from existing fields.
- Whether issue `#294` should later reuse the same status vocabulary to avoid
  auto-refresh making disabled capture look active.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity;
- deduplication;
- live ingest semantics;
- analytics schema or migrations;
- analytics query semantics beyond current display refresh;
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
- secrets, credentials, tokens, endpoint values, spreadsheet IDs, environment
  values, raw logs, generated SQLite files, runtime files, failed posts,
  workbook exports, frontend build output, app-data files, generated data, or
  local-only artifacts.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #295.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/295

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/294

Branch:
codex/analytics-foundation

Contract:
docs/contracts/local_app_live_capture_status_truthful_display.md

Goal:
Compare the current local app frontend/backend status behavior against the contract and implement the smallest safe fix so the first-screen Live capture card cannot imply active capture when live SQLite capture is disabled.

Before editing:
- Confirm branch and git status.
- Reconcile the local branch if it is behind origin and preserve any unrelated local docs/project_roadmap.md edit before pulling, switching, or overwriting files.
- Inspect issue #295, issue #294, the contract, frontend/src/App.tsx, frontend/src/status.ts, frontend/src/types.ts, frontend/src/App.test.tsx, frontend/src/status.test.ts, src/mythic_edge_parser/local_app/setup_status.py, src/mythic_edge_parser/local_app/live_watcher_process.py, and relevant backend tests.
- State what the UI is supposed to communicate, what it currently communicates, why the current mapping is misleading, and the exact minimal implementation plan.

Do:
- Make the Live capture cockpit card prioritize live_sqlite_capture status/mode/write flags over watcher readiness.
- Ensure ready + running:false + sqlite_live_writes_enabled:false does not render as Ready or Capturing.
- Ensure live_sqlite_capture.status disabled and mode status_only render as disabled/not-capturing/limited.
- Keep manual refresh available but do not describe it as starting capture or creating missing live rows.
- Preserve diagnostics/details and safe display/redaction.
- Add focused frontend tests for truthful Live capture display.
- Produce docs/implementation_handoffs/local_app_live_capture_status_truthful_display_comparison.md.

Do not:
- Implement issue #294 auto-refresh.
- Start or stop watcher processes.
- Add watcher controls.
- Implement or change live parser ingest.
- Change live SQLite capture semantics.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest, analytics query semantics, Match Journal truth ownership, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice.
- Expose raw Player.log content, raw JSONL payloads, raw private paths, raw hashes, generated SQLite contents, stack traces, secrets, credentials, endpoint values, spreadsheet IDs, environment values, runtime files, transport-failure artifacts, workbook exports, frontend build output, app-data files, or local-only artifacts.
- Target main.

Validation:
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run frontend/src/App.test.tsx frontend/src/status.test.ts
py -m pytest -q tests/test_analytics_local_app_backend.py
git diff --check
py tools/check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed files.
If npm build is run and creates frontend/dist, remove generated build output before final handoff unless a later contract explicitly authorizes committing it.

Final handoff must include:
- role performed
- issue and related issue reviewed
- contract used
- files changed
- exact frontend/backend/test sections changed
- validation run
- protected-surface status
- generated/private artifact status
- remaining risks
- next recommended role
- workflow_handoff block routing to Codex E
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/295"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #295"
  target_artifact: "docs/implementation_handoffs/local_app_live_capture_status_truthful_display_comparison.md"
  contract_artifact: "docs/contracts/local_app_live_capture_status_truthful_display.md"
  risk_tier: "Medium"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch --untracked-files=all showed branch behind origin by 9 and pre-existing docs/project_roadmap.md modification."
    - "Codex B docs-only validation: git diff --check"
    - "Codex B docs-only validation: py tools/check_agent_docs.py"
    - "Codex B docs-only validation: path-scoped protected-surface scan for the contract"
    - "Codex B docs-only validation: path-scoped secret/private-marker scan for the contract"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not implement issue #294 auto-refresh in issue #295."
    - "Do not start or stop watcher processes."
    - "Do not change live parser ingest or live SQLite capture semantics."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not expose raw Player.log content, raw private paths, raw hashes, secrets, generated SQLite contents, runtime artifacts, frontend build output, or local-only artifacts."
```
