# Contract Test Report: Live App Watcher Diagnostics

## Findings

No blocking findings.

No non-blocking findings requiring Codex D were identified in this review. The
implementation matches the approved read-only diagnostics/status slice for
issue #246.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/246

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

## Umbrella Issue

https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/live_app_watcher_diagnostics.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Implementation handoff:
`docs/implementation_handoffs/live_app_watcher_diagnostics_comparison.md`

Reviewed files:

- `docs/contracts/live_app_watcher_diagnostics.md`
- `docs/implementation_handoffs/live_app_watcher_diagnostics_comparison.md`
- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`

## Report Lifecycle

`report_lifecycle`: `initial_contract_test`

## Contract Summary

Issue #246 authorizes one read-only local-app route,
`GET /api/live/watcher/diagnostics`, plus a safe frontend diagnostics summary.
The route may compose existing sanitized Player.log metadata, watcher readiness,
watcher process safeguards, and live ingest status. It must not read, tail, copy,
hash, or store raw Player.log content; start/stop/control a watcher; call parser
diagnostics or drift builders against live/private logs; create SQLite,
diagnostics, runtime, app-data, or generated artifacts from GET routes; or alter
parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/
coaching/production behavior.

## Internal Project Area Reviewed

Local App / live mode diagnostics.

## Bridge-Code Status Reviewed

`bridge_code`: sanitized local app live status surfaces -> read-only diagnostics
JSON -> browser-visible diagnostics summary. This remains metadata/status
display only and does not become parser truth, analytics truth, evidence truth,
workbook truth, deployment truth, AI truth, or external-transport authorization.

## Checks Run

```bash
git status --short --branch --untracked-files=all
git fetch --prune origin
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
gh issue view 246 --json number,title,state,url,body
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_tailer.py tests\test_parser_diagnostics_mode.py tests\test_evidence_runtime_status.py
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
py -m ruff check src tests tools
py tools\check_agent_docs.py
py tools\check_secret_patterns.py --all
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
git diff --check
rg -n "/api/live/watcher" src/mythic_edge_parser/local_app/backend.py frontend/src/api.ts frontend/src/App.tsx tests/test_analytics_local_app_backend.py
rg -n "POST|PUT|PATCH|DELETE|@app\.post|@app\.put|@app\.patch|@app\.delete|runner\.main|MtgaEventStream\.start|FileTailer\.open_from_start|FileTailer\.open_from_end|FileTailer\.poll|FileTailer\.poll_once|build_parser_diagnostics_report|write_parser_diagnostics_report|build_player_log_drift_report|write_player_log_drift_report|read_text|write_text|mkdir|sqlite3|connect\(" src/mythic_edge_parser/local_app/live_watcher_diagnostics.py src/mythic_edge_parser/local_app/backend.py
<path list> | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
<path list> | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
<generated SQLite/database artifact check>
Test-Path frontend\dist
```

## Results

Validation passed for the reviewed slice.

- Issue #246 is open.
- Tracker #204 was not marked complete.
- Umbrella issue #207 was not closed.
- Branch sync against `origin/codex/analytics-foundation`: `0 0`.
- `git status --short --branch --untracked-files=all` showed expected #246
  modified frontend/backend/test files and untracked #246 contract, handoff, and
  diagnostics helper.
- Backend focused pytest:
  `py -m pytest -q tests\test_analytics_local_app_backend.py` ->
  `18 passed, 1 warning`.
- Related live/parser diagnostics pytest:
  `py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_tailer.py tests\test_parser_diagnostics_mode.py tests\test_evidence_runtime_status.py`
  -> `43 passed`.
- Frontend Vitest: `npm --prefix frontend test -- --run` -> `3 files passed,
  68 tests passed`.
- Frontend typecheck: passed.
- Ruff: passed.
- Agent docs check: passed, `errors: 0`, `warnings: 0`.
- `git diff --check`: passed.
- Full all-repo advisory secret/private-marker scan failed on pre-existing
  repository-wide findings outside the #246 touched slice: `forbidden: 540`,
  `warnings: 898`.
- Base-diff protected-surface and secret/private-marker scans against
  `origin/codex/analytics-foundation` returned `changed_paths: 0` because this
  slice still includes untracked files. Path-scoped scans over the actual
  reviewed file set were therefore used for meaningful scope validation.
- Path-scoped protected-surface scan over the #246 contract, handoff, touched
  implementation/frontend/test files, and this report passed with
  `forbidden: 0`, `warnings: 0`.
- Path-scoped secret/private-marker scan over the same file set passed with
  `forbidden: 0`, `warnings: 0`.
- Generated artifact check found `frontend/dist` absent and no SQLite database
  artifacts under `data`.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-246-000 | N/A | `not_reproduced` | no findings | not_blocking | Codex E reviewed for route expansion, raw/private data exposure, forbidden helper calls, frontend destructive controls, generated artifacts, and protected-surface drift. | Focused tests, frontend tests/typecheck, Ruff, agent docs, diff check, route/forbidden-call scans, generated-artifact check, and path-scoped protected/secret scans passed. | F |

## Confirmed Contract Matches

- Added exactly one watcher diagnostics route:
  `GET /api/live/watcher/diagnostics`.
- No `POST`, `PUT`, `PATCH`, or `DELETE` route was added under
  `/api/live/watcher/*`.
- `build_live_watcher_diagnostics_status(paths)` composes existing sanitized
  local app status builders only: live Player.log status, watcher readiness,
  watcher process safeguards, and live SQLite capture status.
- The helper does not call `runner.main(...)`, `MtgaEventStream.start(...)`,
  `FileTailer.open_from_start(...)`, `FileTailer.open_from_end(...)`,
  `FileTailer.poll(...)`, `FileTailer.poll_once(...)`, parser diagnostics report
  builders, or Player.log drift report builders.
- The response object, schema version, `read_only_composition` mode, summary
  counters, diagnostic entries, stable source summaries, privacy booleans,
  capability booleans, warnings, and errors match the contract shape.
- Privacy booleans and capability booleans are fail-closed to safe values:
  raw log content, raw paths, raw hashes, SQL, stack traces, secrets/env values,
  watcher starts/stops, tailing, SQLite writes, diagnostics-file writes, and
  external transport are all disabled.
- Top-level status classification follows the contract rules: blocked/error
  diagnostics produce `blocked`, warning/degraded diagnostics produce
  `degraded`, unknown diagnostics produce `unknown`, and info-only diagnostics
  produce `ok`.
- Stale Player.log metadata is reported as safe metadata-only diagnostics
  without exposing raw paths or file contents.
- Malformed watcher state is reported as blocked and is not repaired or echoed.
- Tailer rotation/truncation/duplication, parser diagnostics, and evidence
  runtime health remain deferred or expected-but-unavailable rather than being
  generated from live/private logs.
- Frontend adds a typed API reader and read-only Live Diagnostics panel.
- Frontend API validation rejects incompatible diagnostics schemas and unsafe
  capability flags.
- Frontend rendering uses safe display protections for diagnostic category,
  severity, status, evidence label, and message values.
- No destructive or remediation UI controls were added.
- GET status routes did not create app-data folders/files in focused tests.
- No parser behavior, parser final reconciliation, runtime behavior, analytics
  schema, workbook schema, webhook payload, Apps Script, Google Sheets,
  OpenAI/AI/coaching, production behavior, or #244 live capture semantics
  changed.

## Contract Mismatches

None found.

## Missing Tests Or Safeguards

No blocking missing tests or safeguards were identified.

Non-blocking residual risk: frontend diagnostics validation rejects malformed
shape, incompatible schema, and unsafe capability/privacy flags, while backend
tests and helper constants cover the approved status/severity/evidence labels.
The browser validator does not independently enumerate every approved
status/severity/evidence vocabulary value. Because the route is same-repo
backend controlled, safe display redaction is applied before rendering, and the
contract emphasis is fail-closed for unsafe capabilities and unsupported shapes,
this is not a blocker.

## Drift Notes

- No branch drift detected against `origin/codex/analytics-foundation`.
- Base-diff scans saw `changed_paths: 0` because the #246 contract, handoff, and
  diagnostics helper are still untracked. Path-scoped scans were used to avoid
  treating untracked-file state as clean evidence.
- No workbook drift, deployed Apps Script drift, production drift, parser truth
  drift, analytics schema drift, actual Player.log state, or live watcher
  process state was inspected or changed.

## Protected-Surface Status

Passed. Path-scoped protected-surface scan over the contract, implementation
handoff, touched backend/frontend/test files, and this report returned
`forbidden: 0`, `warnings: 0`.

## Secret/Private-Marker Status

Passed for the #246 slice. Path-scoped secret/private-marker scan over the
contract, implementation handoff, touched backend/frontend/test files, and this
report returned `forbidden: 0`, `warnings: 0`.

The all-repo advisory scan still fails on pre-existing repository-wide findings
outside this slice.

## Generated Artifact Status

No generated frontend build output was retained. No SQLite database, WAL, SHM,
journal, diagnostics, runtime status, raw log, workbook export, failed-post, or
local-only private artifacts were found in the reviewed slice.

## Forbidden Scope

Forbidden scope was not touched. This review found no watcher start/stop/control
behavior, no raw Player.log read/tail/hash/store behavior, no parser diagnostics
generation against live/private logs, no GET-created local artifacts, and no
protected parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/
OpenAI/AI/coaching/production behavior changes.

## Recommendation

Approve this slice for Codex F.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #246.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/246

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_watcher_diagnostics.md

Implementation handoff:
docs/implementation_handoffs/live_app_watcher_diagnostics_comparison.md

Contract-test report:
docs/contract_test_reports/live_app_watcher_diagnostics.md

Submit only the reviewed #246 files. Inspect git status first and stage only:
- docs/contracts/live_app_watcher_diagnostics.md
- docs/implementation_handoffs/live_app_watcher_diagnostics_comparison.md
- docs/contract_test_reports/live_app_watcher_diagnostics.md
- src/mythic_edge_parser/local_app/live_watcher_diagnostics.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_local_app_backend.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/App.tsx
- frontend/src/api.test.ts
- frontend/src/App.test.tsx

Before committing, rerun or verify:
- git status --short --branch --untracked-files=all
- py -m pytest -q tests\test_analytics_local_app_backend.py
- py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_tailer.py tests\test_parser_diagnostics_mode.py tests\test_evidence_runtime_status.py
- npm --prefix frontend test -- --run
- npm --prefix frontend run typecheck
- py -m ruff check src tests tools
- py tools\check_agent_docs.py
- git diff --check
- path-scoped protected-surface and secret/private-marker scans over the staged #246 files

Do not target main. Do not start, stop, restart, kill, inspect, or control a watcher process. Do not read, copy, hash, tail, store, or expose raw Player.log content. Do not generate parser diagnostics reports against live/private logs. Do not create local/generated/private/runtime artifacts from diagnostics GET routes. Do not change parser/runtime/analytics schema/#244 capture/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.

Open or update a draft PR only if that is the current Codex F workflow for this branch, and keep the target on the approved non-production integration branch. Do not close issue #246, tracker #204, or umbrella #207 unless explicitly asked.
```

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / contract-test thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/246"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/live_app_watcher_diagnostics.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_watcher_diagnostics_comparison.md"
  target_artifact: "docs/contract_test_reports/live_app_watcher_diagnostics.md"
  branch: "codex/analytics-foundation"
  verdict: "approved_for_codex_f"
  findings:
    - "No blocking findings."
    - "No Codex D loopback required."
  validation:
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py -> 18 passed, 1 existing warning"
    - "py -m pytest -q tests\\test_live_app_parser_owned_fact_capture_sqlite.py tests\\test_tailer.py tests\\test_parser_diagnostics_mode.py tests\\test_evidence_runtime_status.py -> 43 passed"
    - "npm --prefix frontend test -- --run -> 3 files passed, 68 tests passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "py tools\\check_secret_patterns.py --all -> failed on pre-existing all-repo advisory findings outside this slice"
  protected_surface_status: "passed for reviewed #246 path scope"
  secret_private_marker_status: "passed for reviewed #246 path scope; all-repo advisory scan still has pre-existing unrelated findings"
  generated_artifact_status: "frontend/dist absent; no SQLite database artifacts under data"
  forbidden_scope_touched: false
  stop_conditions:
    - "Do not target main."
    - "Do not start, stop, restart, kill, inspect, or control a watcher process."
    - "Do not read, copy, hash, tail, store, or expose raw Player.log content."
    - "Do not generate parser diagnostics reports against live/private logs."
    - "Do not create local/generated/private/runtime artifacts from diagnostics GET routes."
    - "Do not change parser/runtime/analytics schema/#244 capture/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
