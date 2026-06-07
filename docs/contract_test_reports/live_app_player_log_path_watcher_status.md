# Contract Test Report: Live App Player.log Path And Watcher Status

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/240

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

## Umbrella Issue

https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/live_app_player_log_path_watcher_status.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Implementation handoff:
`docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md`

Reviewed files:

- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_local_app_config.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/status.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `frontend/src/status.test.ts`
- `docs/contracts/live_app_player_log_path_watcher_status.md`
- `docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md`

## Report Lifecycle

`report_lifecycle`: `initial_contract_test`

## Contract Summary

Issue #240 authorizes only read-only local app status surfaces for MTGA
`Player.log` path metadata and future live watcher readiness. The slice may add
local app GET routes, setup-status aggregate sections, frontend types/API
helpers/display, and focused tests. It must not start a watcher, call parser
runner/tailer entrypoints, read raw log contents, expose raw absolute paths,
write config, create live SQLite ingest, write runtime artifacts, or change
parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/
production behavior.

## Internal Project Area Reviewed

Local App / UI.

## Bridge-Code Status Reviewed

`bridge_code`: local app config/path metadata -> backend status payloads ->
browser-visible readiness display. This remains status/display only and does
not become parser truth, analytics truth, workbook truth, deployment truth, or
AI/coaching truth.

## Findings

No blocking findings.

## Checks Run

```bash
git status --short --branch --untracked-files=all
git fetch --prune origin
gh issue view 240 --json number,title,state,url,body
gh issue view 204 --json number,title,state,url
gh issue view 207 --json number,title,state,url
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts
py -m pytest -q tests\test_runner.py tests\test_tailer.py
npm --prefix frontend run typecheck
py -m ruff check src tests
git diff --check
<path list> | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
<path list> | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
<generated SQLite/database artifact check>
Test-Path frontend\dist
```

## Results

Passed.

- Issue #240 is open.
- Tracker #204 is open.
- Umbrella issue #207 is open.
- Branch sync: `0 0`.
- Backend/local app focused pytest: `29 passed, 1 StarletteDeprecationWarning`.
- Frontend focused Vitest: `3 files passed, 65 tests passed`.
- Runner/tailer regression slice: `26 passed`.
- Frontend typecheck: passed.
- Ruff: passed.
- `git diff --check`: passed.
- Path-scoped protected-surface scan: passed, `forbidden: 0`, `warnings: 0`.
- Path-scoped secret/private-marker scan: passed, `forbidden: 0`, `warnings: 0`.
- Generated SQLite/database artifact check: no artifacts found.
- `frontend/dist`: absent.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-240-000 | none | `original_finding` | no findings | not_blocking | Review found no contract-blocking mismatch. | Focused backend/frontend tests, runner/tailer tests, typecheck, Ruff, `git diff --check`, protected-surface scan, and secret/private-marker scan passed. | F |

## Confirmed Contract Matches

- `GET /api/live/player-log/status` and `GET /api/live/watcher/status` were added as read-only local app routes.
- `GET /api/app/setup-status` was extended with backward-compatible `live_player_log` and `live_watcher` aggregate sections.
- Player.log status uses metadata-only checks and returns symbolic display paths only.
- Player.log status returns `contents_read = false` and `tailing_started = false`.
- Watcher status returns readiness-only fields with `running = false`, `start_allowed = false`, `stop_allowed = false`, `parser_runner_started = false`, `tailing_started = false`, and `sqlite_live_writes_enabled = false`.
- The local app implementation does not call `runner.main()`, `MtgaEventStream.start(...)`, or `FileTailer.open_from_end(...)`.
- No watcher start/stop controls or destructive UI actions were added.
- Frontend display routes status details through `safeDisplayValue(...)` and tests raw-path redaction for live Player.log display data.
- Direct frontend live API helpers validate schema/object shape and reject malformed watcher responses where controlling fields become true.
- Focused tests cover configured existing, configured missing, configured directory/not-file, invalid config, default detection, unavailable app-data root, no-artifact GET behavior, readiness-only watcher flags, frontend rendering/redaction, API validation, and status-tone mapping.

## Contract Mismatches

None found.

## Missing Tests Or Safeguards

No blocking missing tests or safeguards found.

Non-blocking notes:

- Real Windows permission-denied behavior remains unverified; the handoff also records this as still unverified.
- The implementation emits `detected_missing` for the default missing path case. That matches the approved `detected_missing` vocabulary, but the `missing` / `source = "none"` vocabulary remains unused in this slice because a default path candidate is always checked.
- Live browser/manual visual inspection was not rerun by Codex E; focused frontend tests and typecheck were run instead.

## Drift Notes

- No branch drift detected against `origin/codex/analytics-foundation`.
- No workbook, deployed Apps Script, production, parser truth, analytics schema, actual Player.log root, or live watcher process state was inspected or changed.

## Protected-Surface Status

Passed. Path-scoped protected-surface scan over the contract, handoff, touched
backend/frontend/test files, and report package returned `forbidden: 0`,
`warnings: 0`.

## Secret/Private-Marker Status

Passed. Path-scoped secret/private-marker scan over the contract, handoff,
touched backend/frontend/test files, and report package returned `forbidden: 0`,
`warnings: 0`.

## Generated Artifact Status

No generated SQLite/database artifacts were found. `frontend/dist` was absent.

## Forbidden Scope

Forbidden scope was not touched during review. The implementation did not start
or stop a live watcher, did not tail/read/copy/hash/store raw Player.log
contents, did not expose raw absolute paths in the backend/frontend status path,
did not write config, did not create live SQLite ingest, and did not change
parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/
coaching/production behavior.

## Verdict

Approved against the contract.

## Recommendation

Route to Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #240.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/240

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Reviewed artifact:
docs/contract_test_reports/live_app_player_log_path_watcher_status.md

Contract:
docs/contracts/live_app_player_log_path_watcher_status.md

Implementation handoff:
docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md

Submit the reviewed #240 package only. Inspect git status, confirm unrelated work is not staged, stage only the intended #240 files, commit, push, and open or update the draft PR targeting the approved integration branch. Do not target main, close issue #240, mark tracker #204 complete, start or stop a live watcher, tail/read/copy/hash/store raw Player.log contents, expose raw absolute paths or secrets, or change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/240"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/live_app_player_log_path_watcher_status.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_player_log_path_watcher_status_comparison.md"
  target_artifact: "docs/contract_test_reports/live_app_player_log_path_watcher_status.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_analytics_local_app_config.py tests\\test_analytics_local_app_backend.py -> 29 passed, 1 warning"
    - "npm --prefix frontend test -- --run App.test.tsx api.test.ts status.test.ts -> 65 passed"
    - "py -m pytest -q tests\\test_runner.py tests\\test_tailer.py -> 26 passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "py -m ruff check src tests -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated artifact checks -> no SQLite/database artifacts and no frontend/dist"
  stop_conditions:
    - "Do not target main."
    - "Do not start or stop a live watcher."
    - "Do not tail, read, copy, hash, or store raw Player.log contents."
    - "Do not expose raw absolute paths, secrets, environment values, or private artifacts."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
