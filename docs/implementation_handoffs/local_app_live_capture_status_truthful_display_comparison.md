# Local App Live Capture Status Truthful Display Implementation Handoff

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/295
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/294

## Tracker

N/A.

## Contract

- `docs/contracts/local_app_live_capture_status_truthful_display.md`

## Internal Project Area

Local App / UI.

## Truth Owner

Truth ownership remains upstream:

- parser/state owns parser facts and final reconciliation;
- live watcher/process surfaces own watcher readiness and process-control status;
- live SQLite capture status owns whether live SQLite writes are active,
  disabled, status-only, or blocked;
- frontend owns only safe user-facing status translation and detail text.

## Bridge-Code Status

`bridge_code`

The implementation keeps the flow one-way:

```text
backend setup/live watcher/process/live SQLite capture status
  -> frontend validation/redaction
  -> first-screen Live capture card
```

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

Branch confirmed: `codex/analytics-foundation`

Current status before final validation included:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation [behind 9]
 M docs/contracts/quality_app_submit_error_report_codex_triage.md
 M docs/project_roadmap.md
 M frontend/src/App.test.tsx
 M frontend/src/App.tsx
 M frontend/src/api.ts
 M frontend/src/types.ts
 M src/mythic_edge_parser/local_app/error_reports.py
 M tests/test_analytics_local_app_backend.py
?? docs/contracts/local_app_live_capture_status_truthful_display.md
?? docs/implementation_handoffs/local_app_live_capture_status_truthful_display_comparison.md
```

Unrelated local work preserved:

- `docs/contracts/quality_app_submit_error_report_codex_triage.md`
- `docs/project_roadmap.md`
- `src/mythic_edge_parser/local_app/error_reports.py`
- `tests/test_analytics_local_app_backend.py`
- pre-existing error-report type changes in `frontend/src/types.ts`

The branch is behind `origin/codex/analytics-foundation` by 9 commits. This
implementation did not pull, rebase, stage, commit, push, or target `main`.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/local_app_live_capture_status_truthful_display.md`
- GitHub issue `#295`
- GitHub issue `#294`
- `frontend/src/App.tsx`
- `frontend/src/status.ts`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.test.tsx`
- `frontend/src/status.test.ts`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `tests/test_analytics_local_app_backend.py`

## Current Behavior Compared To Contract

The contract required the first-screen Live capture card to avoid implying
active capture when Player.log or watcher readiness is good but live SQLite
capture is disabled.

Current frontend behavior before this pass derived the compact Live capture
status from watcher readiness:

```text
watcher.running ? "capturing" : watcher.status
```

That allowed `watcher.status = "ready"` to look reassuring even when:

- `watcher.running = false`;
- parser runner was not started;
- tailing was not started;
- `sqlite_live_writes_enabled = false`;
- `live_sqlite_capture.status = "disabled"`;
- `live_sqlite_capture.mode = "status_only"`.

Backend status surfaces already exposed enough strict evidence, so no backend
route, payload-shape, ingest, watcher-process, or parser changes were needed.

## Implementation Option Chosen

Implemented the narrow frontend-only status translation option:

- derive the Live capture card from strict live capture/write evidence first;
- fail closed for missing or malformed live-capture evidence;
- preserve manual refresh as a display/query action only;
- keep watcher readiness scoped to detail text, not active capture truth.

## Files Changed

- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/local_app_live_capture_status_truthful_display_comparison.md`

The untracked contract was preserved:

- `docs/contracts/local_app_live_capture_status_truthful_display.md`

## Exact Sections Changed

### `frontend/src/App.tsx`

- Replaced the old watcher-readiness based Live capture card derivation with
  `liveCaptureStatusFromSetupPayload(...)`.
- Added `liveCaptureStatusFromSetupPayload(...)` to prioritize:
  `live_sqlite_capture`, then watcher process-control flags, then watcher
  flags, with Player.log readiness kept out of active capture truth.
- Added `booleanField(...)` for safe optional boolean extraction.
- Live capture card now sets `liveActive` true only for strict `Capturing`.
- Disabled capture detail now explains that Player.log may be detected while
  live SQLite capture is not running and manual refresh only shows rows already
  stored in SQLite.

### `frontend/src/api.ts`

- Loosened frontend validation for live watcher/process booleans from exact
  `false` to `boolean`, so active-capture test payloads and future read-only
  status payloads can validate without changing backend behavior.
- Preserved fixed false constraints for start/stop/UI control fields.

### `frontend/src/types.ts`

- Updated live watcher/process summary types so running, parser-runner, tailing,
  SQLite-write, and PID booleans can represent true or false evidence.
- Added `LiveSqliteCaptureStatusResponse`.
- Added optional `live_sqlite_capture` to `SetupStatusResponse`.

Note: the bottom error-report type changes visible in this file were unrelated
local work and are not part of issue `#295`.

### `frontend/src/App.test.tsx`

- Added focused tests proving:
  - watcher readiness plus disabled SQLite writes does not render `Ready` or
    `Capturing`;
  - disabled/status-only live SQLite capture renders as `Capture disabled`;
  - strict running/parser/tailing/SQLite-write evidence is required for
    `Capturing`;
  - malformed or missing strict fields fail closed;
  - manual refresh remains present but is not described as starting capture or
    creating rows.
- Added safe test payload helpers for live SQLite capture status.

## Code Changed

Yes. Frontend runtime code changed only.

No backend code was changed for this issue. The modified backend file visible in
the working tree is unrelated local work and was left untouched.

## Tests Added Or Updated

Yes. Focused frontend tests were added in `frontend/src/App.test.tsx`.

No backend tests were changed because current backend setup status already
provides the required live watcher/process/live SQLite capture evidence.

## Interface Changes

No backend route shapes or payload shapes were changed.

Frontend-only TypeScript display types were extended to include the already
existing `live_sqlite_capture` setup-status section and to model live
capture/process booleans as booleans instead of exact `false` literals.

## Contracted Area Status

Stayed inside the Local App / UI status translation surface.

No parser truth, live ingest semantics, live SQLite capture semantics, analytics
schema/migrations, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/
coaching behavior, Line Tracer behavior, or production behavior was changed.

## Validation Run

Passed:

```powershell
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run src/App.test.tsx src/status.test.ts
py -m pytest -q tests/test_analytics_local_app_backend.py
npm --prefix frontend run build
```

Notes:

- The first Vitest attempt used paths relative to the repo root with
  `--prefix frontend` and found no files. The corrected command above passed.
- `npm --prefix frontend run build` created `frontend/dist`; generated build
  output was removed before handoff.
- `py -m pytest -q tests/test_analytics_local_app_backend.py` passed with one
  existing FastAPI TestClient deprecation warning.

Final repository validation was run after writing this handoff:

```powershell
git diff --check -> passed
py tools\check_agent_docs.py -> passed
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin -> passed, forbidden 0, warnings 0
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin -> passed, forbidden 0, warnings 0
```

## Protected Surface Status

Passed for the #295 path-scoped scan set.

Touched-path scan set:

```text
docs/contracts/local_app_live_capture_status_truthful_display.md
docs/implementation_handoffs/local_app_live_capture_status_truthful_display_comparison.md
frontend/src/App.tsx
frontend/src/types.ts
frontend/src/api.ts
frontend/src/App.test.tsx
```

## Secret / Private Marker Status

Passed for the #295 path-scoped scan set: forbidden 0, warnings 0.

No raw Player.log content, raw JSONL payloads, raw private paths, raw hashes,
generated SQLite contents, stack traces, secrets, credentials, endpoint values,
spreadsheet IDs, environment values, runtime files, transport-failure artifacts,
workbook exports, frontend build output, app-data files, or local-only artifacts
were intentionally read, printed, stored, or committed.

## Generated / Private Artifact Status

- `frontend/dist` was produced by the frontend build and removed.
- No generated SQLite database files were created or committed by this pass.
- No watcher process was started or stopped.

## Still Unverified

- Browser/manual visual smoke was not run.
- Branch freshness remains unresolved because the branch is behind origin by 9
  commits.
- The unrelated local modifications listed above remain outside this module.

## Forbidden Scope

Forbidden scope was not intentionally touched:

- no issue `#294` auto-refresh implementation;
- no watcher start/stop controls;
- no live parser ingest or live SQLite capture semantic changes;
- no parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/
  AI/coaching/production behavior changes;
- no staging, commit, push, PR, merge, deployment, or issue closure.

## Reviewer Focus

Codex E should pay special attention to:

- whether the Live capture card fails closed for disabled/status-only capture;
- whether `Ready` is kept off the first-screen Live capture card in the known
  issue `#295` state;
- whether `Capturing` requires strict running/parser/tailing/SQLite-write
  evidence;
- whether the TypeScript boolean validator loosening is frontend-display safe
  and does not enable controls;
- whether unrelated local changes remain excluded from this contract review.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #295.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/295

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/294

Branch:
codex/analytics-foundation

Contract:
docs/contracts/local_app_live_capture_status_truthful_display.md

Implementation handoff:
docs/implementation_handoffs/local_app_live_capture_status_truthful_display_comparison.md

Risk tier:
Medium

Goal:
Review the Codex C implementation against the contract. Verify that the local
app first-screen Live capture card truthfully distinguishes Player.log/watcher
readiness from active live SQLite capture and cannot display Ready or Capturing
for the disabled/status-only issue #295 state.

Before reviewing:
- Confirm branch and git status.
- Identify unrelated dirty files and keep them out of the review findings.
- Read the contract and implementation handoff.
- Inspect frontend/src/App.tsx, frontend/src/api.ts, frontend/src/types.ts,
  frontend/src/App.test.tsx, frontend/src/status.ts, frontend/src/status.test.ts,
  and relevant backend setup/live watcher/live SQLite capture status surfaces.

Review focus:
- Verify live_sqlite_capture status/mode/write flags outrank watcher readiness.
- Verify ready + running:false + sqlite_live_writes_enabled:false does not
  render as Ready or Capturing.
- Verify live_sqlite_capture.status disabled and mode status_only render as
  disabled/not-capturing/limited.
- Verify liveActive is true only for strict Capturing evidence.
- Verify manual refresh remains available but does not imply capture, starting a
  watcher, or creating rows.
- Verify unknown/malformed/missing status fails closed.
- Verify no backend route shape, parser behavior, live ingest semantics,
  analytics schema/migrations, workbook/webhook/App Script/Sheets/OpenAI/AI/
  coaching/production behavior, or generated/private artifact behavior changed.

Validation:
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run src/App.test.tsx src/status.test.ts
py -m pytest -q tests/test_analytics_local_app_backend.py
git diff --check
py tools/check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed
files.

If npm build is run and creates frontend/dist, remove generated build output
before final handoff unless a later contract explicitly authorizes committing it.

Output:
- findings first, ordered by severity, with file/line references;
- contract match/mismatch summary;
- validation run and result;
- protected-surface and secret/private-marker status;
- generated artifact status;
- whether forbidden scope was touched;
- next recommended role, likely Codex F if no blocking findings or Codex D if
  fixes are needed;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/295"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/local_app_live_capture_status_truthful_display.md"
  target_artifact: "docs/contract_test_reports/local_app_live_capture_status_truthful_display.md"
  implementation_handoff: "docs/implementation_handoffs/local_app_live_capture_status_truthful_display_comparison.md"
  risk_tier: "Medium"
  branch: "codex/analytics-foundation"
  validation:
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend test -- --run src/App.test.tsx src/status.test.ts -> passed"
    - "py -m pytest -q tests/test_analytics_local_app_backend.py -> passed with existing FastAPI TestClient deprecation warning"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not implement issue #294 auto-refresh in issue #295."
    - "Do not start or stop watcher processes."
    - "Do not change live parser ingest or live SQLite capture semantics."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not expose raw Player.log content, raw private paths, raw hashes, secrets, generated SQLite contents, runtime artifacts, frontend build output, or local-only artifacts."
```
