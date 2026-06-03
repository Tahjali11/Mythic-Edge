# Private Local V1 Local App Startup And Status Smoke Report

## Findings

No blocking findings.

### CT-251-001 P2: Disposable-root smoke passed as degraded-acceptable, not full actual-root readiness

- finding_lifecycle: `original_finding`
- finding_status: `verified_degraded_acceptable`
- blocking_status: `not_blocking`
- evidence: launcher preflight had no blockers; backend and frontend started on loopback; required backend routes returned JSON; Playwright observed all required frontend panels; privacy checks found no unsafe backend routes, unsafe frontend markers, or forbidden watcher controls.
- degraded items: disposable app config, analytics DB, analytics views, watcher process state, and local data were missing/not initialized as expected for a clean disposable app-data root.
- next_route: Codex F for #251. Keep #253 open for clean-checkout install/launch proof and any actual-root readiness work.

### CT-251-002 P3: Smoke cleanup required targeted Vite child-process cleanup

- finding_lifecycle: `original_finding`
- finding_status: `cleaned_up`
- blocking_status: `not_blocking`
- evidence: the bounded smoke used the launcher API with `wait_for_exit=False`; after process cleanup, the frontend port still had a repo-owned Vite listener. The reviewer stopped only the repo frontend dev-server process and rechecked both loopback ports.
- risk: future automated smoke harnesses should remember that the frontend dev server may outlive the immediate launcher-managed child.
- next_route: no immediate Codex D route for #251; include this in #253 or a future launcher harness polish issue if it repeats.

### CT-251-003 P3: Local environment checker still reports `.env*` ignore-coverage uncertainty

- finding_lifecycle: `deferred_followup`
- finding_status: `known_baseline_gap`
- blocking_status: `not_blocking_for_251`
- evidence: `py tools\check_local_environment.py --profile local_developer_app --app-data-root <smoke_app_data_root>` returned `status: warning`, with `env_files` reported as `missing_not_ignored`.
- next_route: already covered by #252.

## Role Performed

Codex E: Governance Reviewer / Baseline Auditor.

## Issue / Tracker / Source Baseline

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/251
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source baseline issue: https://github.com/Tahjali11/Mythic-Edge/issues/249
- Source framework issue: https://github.com/Tahjali11/Mythic-Edge/issues/248

## Branch And Commit

- Branch: `codex/analytics-foundation`
- Commit reviewed: `8cc52a6`

## Contract / Source Artifacts Reviewed

- `docs/contracts/private_local_v1_local_app_startup_status_smoke.md`
- `docs/contract_test_reports/engineering_maturity_baseline.md`
- GitHub issue #251
- GitHub issue #249
- GitHub tracker #136

## Files And Evidence Reviewed

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`
- `docs/project_roadmap.md`
- `tools/dev_app/start_mythic_edge_dev_app.ps1`
- `tools/dev_app/dev_app_launcher.py`
- `tools/check_local_environment.py`
- `docs/local_artifacts_manifest.json`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `frontend/package.json`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/status.ts`
- focused backend, launcher-adjacent, local-app, frontend, and Match Journal tests

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

Issue #251 must prove that the local developer app can start in a controlled
`private_local_v1` profile, report setup/status safely, render the expected
frontend panels, and leave no generated/private/local artifacts committed. The
smoke must not read raw Player.log contents, start watcher control, run manual
imports, write live SQLite facts, touch workbook/webhook/App Script/Sheets/AI
behavior, or expose raw paths, raw hashes, secrets, SQL, stack traces, or
private artifacts.

## Startup Mode

- Preflight: `.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check -AppDataRoot <smoke_app_data_root>`
- Startup: launcher API equivalent of the approved PowerShell launcher path, using `no_open` and bounded `wait_for_exit=False`.
- App-data mode: disposable root.
- Backend URL: `http://127.0.0.1:8765`
- Frontend URL: `http://127.0.0.1:5173`
- Browser evidence: Playwright CLI session against the local Vite app.
- Cleanup method: launcher child cleanup, targeted stop of repo-owned Vite listener when it remained on the frontend port, Playwright session close, disposable root removal, and final port checks.

## Backend Endpoint Matrix

| Area | Route | Result |
| --- | --- | --- |
| Health | `/api/health` | HTTP 200, `status: ok`; parser-runner control disabled, live watcher disabled. |
| Setup aggregate | `/api/app/setup-status` | HTTP 200, `status: degraded`; required sections present. |
| Config | `/api/app/config` | HTTP 200, `status: missing`; sanitized missing-config state. |
| Paths | `/api/app/paths` | HTTP 200, `status: ok`; symbolic app-data reporting. |
| Analytics DB | `/api/analytics/database/status` | HTTP 200, `status: missing`; no DB creation required. |
| Runtime state | local runtime route | HTTP 200, `status: ok`; non-controlling state. |
| Live Player.log | `/api/live/player-log/status` | HTTP 200, `status: ok`; `contents_read: false`, `tailing_started: false`. |
| Live watcher | `/api/live/watcher/status` | HTTP 200, `status: ready`; running/start/stop/tailing/live-write flags false. |
| Watcher process | `/api/live/watcher/process` | HTTP 200, `status: not_initialized`; no start/stop route enabled. |
| Watcher diagnostics | `/api/live/watcher/diagnostics` | HTTP 200, `status: degraded`; raw content/path/hash/SQL/stack-trace privacy booleans false. |
| Live SQLite capture | `/api/live/ingest/status` | HTTP 200, `status: disabled`; live writes false. |
| Analytics views | `/api/analytics/*` read-only view routes | HTTP 200 with `status: missing`; acceptable for disposable root. |

`GET /api/journal` was not called because no safe parser-owned match/game
context existed. No POST routes were called.

## Frontend Render Matrix

Playwright snapshot evidence found all required surfaces:

- `Setup Status`
- `Backend Reachability`
- `Live Player.log`
- `Live Watcher`
- `Live Watcher Process`
- `Live Diagnostics`
- `Analytics History`
- `Early Game History`
- `Action Review`
- `Split Review`
- `Match Journal Cockpit`

Frontend smoke checks found:

- missing required panel text: none
- forbidden watcher/destructive control markers: none
- unsafe frontend marker count: 0

## Contract / Baseline Matches

- Launcher preflight completed with no blocking missing dependencies.
- Backend and frontend started on loopback ports.
- Required backend GET routes returned JSON with safe status labels.
- Missing local config, DB, analytics rows, and watcher state were explained as degraded/missing/disabled rather than treated as passed data.
- Live Player.log status was metadata-only.
- Watcher/process/live-ingest control flags remained disabled or false.
- Frontend rendered the required readiness panels.
- No manual import, browser upload, Match Journal write, watcher start/stop, parser runner, Player.log tailing, live SQLite write, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching, or production behavior was invoked.
- Disposable app-data artifacts and frontend build output were removed after validation.

## Contract / Baseline Mismatches

None blocking.

The only mismatch-like observation is CT-251-002: the bounded launcher API
cleanup did not fully clear the Vite child process without targeted cleanup.
Final cleanup succeeded, ports were clear, and no repo artifacts remained.

## Missing Tests Or Safeguards

- No dedicated automated test currently proves that a bounded launcher smoke can kill frontend grandchild processes without targeted cleanup.
- Actual default app-data root readiness remains unverified by design and still requires explicit approval before inspection.
- Clean-checkout install/launch proof remains owned by #253.
- `.env*` ignore-coverage uncertainty remains owned by #252.

## Validation Run And Result

- `git status --short --branch --untracked-files=all` -> branch `codex/analytics-foundation`; untracked #251 contract before this report.
- `gh issue view 251` -> open.
- `gh issue view 249` -> closed source baseline issue.
- `gh issue view 136` -> open tracker.
- `.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check -AppDataRoot <smoke_app_data_root>` -> passed, no blockers.
- `py tools\check_local_environment.py --profile local_developer_app --app-data-root <smoke_app_data_root>` -> `status: warning`, blocked 0, errors 0, warnings 1 for `.env*` ignore coverage.
- Controlled live startup/status/browser smoke -> passed as `degraded_acceptable`.
- `py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py` -> 37 passed, 1 third-party warning.
- `py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_match_journal_status_api.py` -> 34 passed, 1 third-party warning.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend test -- --run` -> 3 files passed, 68 tests passed.
- `npm --prefix frontend run build` -> passed; `frontend/dist` removed afterward.
- `py -m ruff check src tests tools` -> passed.
- Final loopback port checks -> backend and frontend ports not listening after cleanup.

## Protected-Surface Status

No protected parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/
OpenAI/AI/coaching/production behavior was changed. The smoke used only
loopback local app startup, read-only backend GET routes, frontend rendering,
and generated-artifact cleanup.

## Secret / Private-Marker Status

No raw Player.log contents, private JSONL payloads, raw hashes, secrets,
credentials, environment values, SQL, stack traces, generated DB contents, retry
payloads, workbook exports, or local-only artifact contents were included in
this report.

The smoke response scan found no unsafe backend routes and no unsafe frontend
markers. Path-scoped report validation is still required after this report is
written.

## Generated Artifact Status

- Disposable smoke app-data root was created outside the repo, then removed.
- Smoke-created app-data subfolders were limited to `config`, `db`,
  `diagnostics`, `imports`, `jobs`, and `logs`.
- Playwright `.playwright-cli` artifacts created during browser automation were removed.
- `frontend/dist` was created by the build and removed.
- Final git status before report writing showed no generated app-data, DB,
  runtime, failed-post, workbook export, raw-log, frontend build, or local-only
  artifacts in the worktree.

## Forbidden Scope

Forbidden scope was not touched. This audit did not implement fixes, start or
stop a live watcher, tail/read/hash/copy raw Player.log contents, inspect real
private app-data contents, change parser/runtime/analytics schema/workbook/
webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior, stage files,
open a PR, merge, target main, or close issues.

## Verdict

`degraded_acceptable`

Issue #251 satisfies the startup/status smoke requirement for a disposable
`private_local_v1` local-app profile. It does not close the broader
private-local-v1 readiness work owned by #252 and #253.

## Recommendation

Route to Codex F to submit the #251 contract and this report.

Do not route to Codex D unless the team wants to treat CT-251-002 as a launcher
cleanup polish bug. Do not route to Codex B; the contract was sufficiently clear.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #251.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/251

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Reviewed artifacts:
- docs/contracts/private_local_v1_local_app_startup_status_smoke.md
- docs/contract_test_reports/private_local_v1_local_app_startup_status_smoke.md

Submit only the reviewed docs-only #251 startup/status smoke artifacts. Before staging, inspect git status and verify no generated/private/local artifacts are included.

Run or verify:
- git status --short --branch --untracked-files=all
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over the #251 contract and report
- path-scoped secret/private-marker scan over the #251 contract and report

Do not implement fixes, stage unrelated files, target main, close #251, close #249, close #252, close #253, or close tracker #136 unless explicitly asked. Preserve parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production boundaries.
```

```yaml
workflow_handoff:
  role_performed: "Codex E: Governance Reviewer / Baseline Auditor"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/251"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  source_baseline_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/249"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/private_local_v1_local_app_startup_status_smoke.md"
  target_artifact: "docs/contract_test_reports/private_local_v1_local_app_startup_status_smoke.md"
  verdict: "degraded_acceptable"
  findings:
    - "No blocking findings."
    - "CT-251-001: disposable-root smoke passed as degraded-acceptable, not actual-root readiness."
    - "CT-251-002: bounded launcher API cleanup required targeted Vite child-process cleanup."
    - "CT-251-003: .env* ignore-coverage warning remains deferred to #252."
  validation:
    - "launcher preflight with disposable app-data root -> passed, no blockers"
    - "local_developer_app environment check -> warning, blocked 0, errors 0, warnings 1"
    - "controlled live startup/status/browser smoke -> passed as degraded_acceptable"
    - "backend/frontend focused pytest -> passed"
    - "frontend typecheck/test/build -> passed; frontend/dist removed"
    - "ruff -> passed"
    - "final loopback port checks -> backend/frontend ports not listening"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  remaining_risks:
    - "Actual default app-data root was not inspected."
    - "Clean-checkout install/launch proof remains owned by #253."
    - "Private-artifact scanner/env posture remains owned by #252."
  stop_conditions:
    - "Do not implement fixes in Codex F."
    - "Do not stage generated/private/local artifacts."
    - "Do not target main."
    - "Do not close #251 or tracker #136 unless explicitly asked."
```
