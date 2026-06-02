# Live App Player.log Watcher Process-Control Safeguards Fixer Handoff

## Role Performed

Codex D: Module Fixer.

## Source Issue And Tracker

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/242>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>

## Source Contract And Review

- Contract:
  `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`
- Implementation handoff:
  `docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md`
- Review artifact:
  `docs/contract_test_reports/live_app_player_log_watcher_process_control_safeguards.md`
- Constitution: `docs/agent_constitution.md`
- Module fixer rules: `docs/agent_threads/module_fixer.md`

## Finding Fixed

CT-242-001 P1: process preconditions used a map instead of the
contract-required list of keyed objects.

Fault category: public response-shape mismatch. The backend, TypeScript type,
frontend validator, and fixtures agreed with each other, but they did not match
the contract-required `preconditions: [{ key, status, reason }, ...]` list.

## Fix Produced

`GET /api/live/watcher/process` now returns `preconditions` as a deterministic
list of objects. Each precondition entry includes:

- `key`
- `status`
- `reason`

The deterministic order is:

- `player_log_ready`
- `app_data_root_available`
- `state_directory_available`
- `single_instance_guard_available`
- `supervisor_target_defined`
- `external_transport_disabled`
- `live_sqlite_ingest_contract_present`
- `frontend_controls_authorized`

The backend still uses an internal local lookup for process-status decisions.
All process-control flags remain false, and no start/stop/process/tailer/parser
behavior was added.

Frontend `LiveWatcherProcessStatusResponse` now uses the list shape. The API
validator rejects the old map shape and rejects entries missing required
fields. The app-side type guard also requires list entries with `key`,
`status`, and `reason`.

## Files Changed

- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_fixer.md`

## Code Changed Or Tests Only

Code and tests changed. The code change is limited to the local app process
status response shape and frontend validation/type handling for that shape.

No parser behavior, parser runtime, analytics schema, workbook schema, webhook
payload, Apps Script, Sheets, OpenAI, AI/coaching, production behavior,
watcher start/stop route, process spawn/kill, live tailing, Player.log content
read, raw log storage, or generated app-data state creation was added.

## Tests Added Or Updated

- Backend route tests now assert `preconditions` is a list and contains the
  required keys in deterministic order.
- Lower-level process-status tests now assert each list entry includes
  `key`, `status`, and `reason`.
- Frontend API tests now reject the old precondition map shape.
- Frontend API tests now reject a precondition entry missing a required field.
- Frontend fixtures now use the contract-required list shape.

## Validation Evidence

```powershell
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
# failed before production fix: 2 failed, 32 passed

py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
# passed after backend fix: 34 passed, 1 Starlette/FastAPI testclient warning

npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts
# 3 files passed, 65 tests passed

npm --prefix frontend run typecheck
# passed

py -m pytest -q tests\test_analytics_local_app_backend.py
# 15 passed, 1 Starlette/FastAPI testclient warning

py -m pytest -q tests\test_analytics_local_app_config.py tests\test_runner.py tests\test_tailer.py
# 45 passed

npm --prefix frontend run build
# passed; generated frontend/dist removed afterward

py -m ruff check src tests tools
# passed

py tools\check_agent_docs.py
# passed, errors 0, warnings 0

git diff --check
# passed
```

## Pending Final Safety Checks

Completed after this handoff file was present:

```powershell
path-scoped protected-surface scan
# passed, forbidden 0, warnings 0

path-scoped secret/private-marker scan
# passed, forbidden 0, warnings 0

generated SQLite/database artifact sweep
# no output

Test-Path frontend\dist
# False
```

## Remaining Review Focus

Codex E should confirm:

- `preconditions` is a list, not a map;
- every precondition entry has `key`, `status`, and `reason`;
- frontend validation rejects the old map shape and malformed list entries;
- all process-control flags remain false;
- no start/stop route, frontend start/stop control, runner/tailer call,
  Player.log content read, live SQLite write, external transport, or production
  behavior was added.

## Still Unverified

- Manual browser view of the process-status panel.
- GitHub Actions.
- Any future real process supervisor behavior, intentionally out of scope.

## Forbidden Scope Status

Forbidden scope touched: false.

## Next Recommended Role

Codex E: Module Reviewer / confirmation thread.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #242.

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

Review artifact:
docs/contract_test_reports/live_app_player_log_watcher_process_control_safeguards.md

Fixer handoff:
docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_fixer.md

Confirm the Codex D fix for CT-242-001:
- GET /api/live/watcher/process returns preconditions as a deterministic list of keyed objects.
- Frontend types and validators require the list shape.
- Frontend validation rejects old map-shaped preconditions and missing required precondition fields.
- All process-control flags remain false and no start/stop, runner, tailer, Player.log content read, live SQLite write, external transport, or production behavior was added.

Lead with findings ordered by severity. If no blockers remain, recommend the next workflow role.
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/242"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  branch: "codex/analytics-foundation"
  source_artifact: "docs/contract_test_reports/live_app_player_log_watcher_process_control_safeguards.md"
  contract: "docs/contracts/live_app_player_log_watcher_process_control_safeguards.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_comparison.md"
  target_artifact: "docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_fixer.md"
  finding_fixed:
    - "CT-242-001 P1: process preconditions now use the contract-required list of keyed objects."
  files_changed:
    - "src/mythic_edge_parser/local_app/live_watcher_process.py"
    - "tests/test_analytics_local_app_backend.py"
    - "tests/test_analytics_local_app_config.py"
    - "frontend/src/types.ts"
    - "frontend/src/api.ts"
    - "frontend/src/App.tsx"
    - "frontend/src/api.test.ts"
    - "frontend/src/App.test.tsx"
    - "docs/implementation_handoffs/live_app_player_log_watcher_process_control_safeguards_fixer.md"
  code_changed_or_tests_only: "code+tests"
  validation:
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py tests\\test_analytics_local_app_config.py -> 34 passed, 1 warning"
    - "npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts -> 65 passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py -> 15 passed, 1 warning"
    - "py -m pytest -q tests\\test_analytics_local_app_config.py tests\\test_runner.py tests\\test_tailer.py -> 45 passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed afterward"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated SQLite/database artifact sweep -> no output"
    - "Test-Path frontend\\dist -> False"
  forbidden_scope_touched: false
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
```
