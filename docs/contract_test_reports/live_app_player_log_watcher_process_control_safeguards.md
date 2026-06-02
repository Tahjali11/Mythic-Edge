# Contract Test Report: Live App Player.log Watcher Process-Control Safeguards

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/242

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

## Umbrella Issue

https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Implementation handoff:
`docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md`

Fixer handoff:
`docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_fixer.md`

Reviewed files:

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
- `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`
- `docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md`
- `docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_fixer.md`

## Report Lifecycle

`report_lifecycle`: `followup_after_fixer`

## Contract Summary

Issue #242 authorizes backend-first, read-only process-control safeguards for a
future live Player.log watcher. The implementation may add
`GET /api/live/watcher/process`, setup-status aggregation, frontend
informational display, and focused tests. It must not add start/stop routes,
spawn/kill processes, call parser runner or tailer entrypoints, read/tail/copy/
hash/store raw Player.log content, create app-data artifacts from GET routes,
write live SQLite facts, or change parser/runtime/workbook/webhook/App Script/
Sheets/OpenAI/AI/coaching/production behavior.

## Internal Project Area Reviewed

Local App / live mode.

## Bridge-Code Status Reviewed

`bridge_code`: local app readiness/status metadata -> process-control safeguard
payload -> browser-visible status display. This remains status/reporting only
and does not become parser truth, analytics truth, workbook truth, deployment
truth, AI truth, or external-transport authorization.

## Findings

No blocking findings remain.

### CT-242-001 fixed_state_followup: Process preconditions now use the contract-required list of keyed objects

Original finding: `GET /api/live/watcher/process` returned `preconditions` as a
keyed map, while the contract requires a deterministic list of objects with
`key`, `status`, and `reason`.

Confirmed fixed after Codex D:

- Backend now emits `preconditions` as the return value from
  `_build_preconditions(...)`, and that helper returns a list of keyed objects
  with `key`, `status`, and `reason`
  (`src/mythic_edge_parser/local_app/live_watcher_process.py`, lines 58 and
  182-215).
- Internal process-status evaluation still builds a temporary map from that
  list for local logic only; the public response remains list-shaped
  (`src/mythic_edge_parser/local_app/live_watcher_process.py`, lines 218-245).
- Frontend types now model `LiveWatcherProcessPrecondition` and
  `preconditions: LiveWatcherProcessPrecondition[]`
  (`frontend/src/types.ts`, lines 131-144).
- Frontend API validation now rejects non-list `preconditions` and requires the
  contract keys in deterministic order (`frontend/src/api.ts`, lines 1568-1584).
- Frontend tests reject the old map shape and reject missing required
  precondition entries (`frontend/src/api.test.ts`, lines 155-177).
- Backend/config tests assert list shape, deterministic key order, and required
  `key`, `status`, and `reason` fields
  (`tests/test_analytics_local_app_backend.py`, lines 25-31;
  `tests/test_analytics_local_app_config.py`, lines 34-40).

## Checks Run

```bash
git status --short --branch --untracked-files=all
git fetch --prune origin
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_runner.py tests\test_tailer.py
npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
<path list> | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
<path list> | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
<generated SQLite/database artifact check>
Test-Path frontend\dist
```

## Results

Validation passed and CT-242-001 is confirmed fixed.

- Issue #242 was not closed.
- Tracker #204 was not marked complete.
- Umbrella issue #207 was not closed.
- Branch sync: `0 0`.
- Backend/config pytest:
  `py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py`
  -> `34 passed, 1 warning`.
- Runner/tailer pytest:
  `py -m pytest -q tests\test_runner.py tests\test_tailer.py`
  -> `26 passed`.
- Frontend focused Vitest:
  `npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts`
  -> `3 files passed, 65 tests passed`.
- Frontend typecheck: passed.
- Frontend build: passed; generated `frontend/dist` removed after build.
- Ruff: passed.
- `git diff --check`: passed.
- Agent docs check: passed, `errors: 0`, `warnings: 0`.
- Path-scoped protected-surface scan: passed, `forbidden: 0`, `warnings: 0`.
- Path-scoped secret/private-marker scan: passed, `forbidden: 0`, `warnings: 0`.
- Generated SQLite/database artifact check: no artifacts found.
- `frontend/dist`: absent after cleanup.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-242-001 | P1 | `fixed_state_followup` | fixed | not_blocking | Contract requires `preconditions` as a list of keyed objects; initial implementation returned a keyed map and frontend accepted the map shape. | Backend now returns a list, frontend types and validators require list shape, backend/frontend tests reject the old shape or missing required entries, and focused validation passed. | F |

## Confirmed Contract Matches

- Added exactly one new read-only process-control safeguards route:
  `GET /api/live/watcher/process`.
- No `POST /api/live/watcher/start`, `POST /api/live/watcher/stop`, PUT,
  PATCH, or DELETE process-control route was added.
- Process-control flags remain false in backend payloads and frontend
  validators: `start_allowed`, `stop_allowed`, `start_route_enabled`,
  `stop_route_enabled`, `ui_controls_allowed`, `automatic_start_enabled`,
  `parser_runner_started`, `tailing_started`, `sqlite_live_writes_enabled`,
  and `external_transport_allowed`.
- `preconditions` now matches the contract-required deterministic list of
  objects with `key`, `status`, and `reason`.
- The helper reports missing, malformed, and stale synthetic state without
  treating it as running or verified.
- The helper does not call `runner.main()`, `MtgaEventStream.start(...)`,
  `FileTailer.open_from_*`, `FileTailer.poll(...)`, or
  `FileTailer.poll_once(...)`.
- GET status routes did not create app-data folders/files in focused tests.
- Frontend adds an informational process panel and no clickable start/stop
  controls.
- Frontend validator rejects process-control payloads where a control flag such
  as `start_allowed` becomes true.
- Path-scoped protected-surface and secret/private-marker scans passed.

## Contract Mismatches

None remaining.

## Missing Tests Or Safeguards

No blocking missing tests remain.

Non-blocking residual: the setup-status panel type guard checks that
`preconditions` is an array of entries with `key`, `status`, and `reason`, while
the direct process API validator enforces the exact required keys and order. The
panel does not render `preconditions`, and the direct route contract is covered
by stricter validation and tests, so this is not a blocker.

## Drift Notes

- No branch drift detected against `origin/codex/analytics-foundation`.
- No workbook, deployed Apps Script, production, parser truth, analytics schema,
  actual Player.log root, or live watcher process state was inspected or
  changed.

## Protected-Surface Status

Passed. Path-scoped protected-surface scan over the contract, handoffs, touched
backend/frontend/test files, and report package returned `forbidden: 0`,
`warnings: 0`.

## Secret/Private-Marker Status

Passed. Path-scoped secret/private-marker scan over the contract, handoffs,
touched backend/frontend/test files, and report package returned `forbidden: 0`,
`warnings: 0`.

## Generated Artifact Status

No generated SQLite/database artifacts were found. `frontend/dist` was created
by the frontend build and removed afterward.

## Forbidden Scope

Forbidden scope was not touched during review or fixer confirmation. The
implementation did not start or stop a live watcher, did not spawn or kill
processes, did not tail/read/copy/hash/store raw Player.log contents, did not
expose routine start/stop controls, did not create generated app-data artifacts
from GET routes, and did not change parser/runtime/analytics schema/workbook/
webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.

## Verdict

Approved after Codex D fix. CT-242-001 is confirmed fixed and no blocking
contract-test findings remain.

## Recommendation

Route to Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #242.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/242

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Reviewed artifact:
docs/contract_test_reports/live_app_player_log_watcher_process_control_safeguards.md

Contract:
docs/contracts/live_app_player_log_watcher_process_control_safeguards.md

Implementation handoff:
docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md

Fixer handoff:
docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_fixer.md

Submit the reviewed #242 package only. Inspect git status, confirm unrelated work is not staged, stage only the intended #242 files, commit, push, and open or update the draft PR targeting the approved integration branch. Do not target main, close issue #242, mark tracker #204 complete, add watcher start/stop routes or controls, start/stop/spawn/kill/tail watcher processes, read/hash/store raw Player.log contents, or change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/242"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/live_app_player_log_watcher_process_control_safeguards.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_fixer.md"
  target_artifact: "docs/contract_test_reports/live_app_player_log_watcher_process_control_safeguards.md"
  finding_confirmed_fixed:
    - "CT-242-001 P1: process preconditions now use the contract-required list of keyed objects."
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py tests\\test_analytics_local_app_config.py -> 34 passed, 1 warning"
    - "py -m pytest -q tests\\test_runner.py tests\\test_tailer.py -> 26 passed"
    - "npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts -> 65 passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated artifact checks -> no SQLite/database artifacts and no frontend/dist"
  stop_conditions:
    - "Do not target main."
    - "Do not add watcher start/stop routes or routine frontend controls."
    - "Do not start, stop, spawn, kill, tail, or inspect live watcher processes beyond read-only safe status."
    - "Do not read, copy, hash, tail, store, or commit raw Player.log contents."
    - "Do not create app-data state files from GET routes."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
