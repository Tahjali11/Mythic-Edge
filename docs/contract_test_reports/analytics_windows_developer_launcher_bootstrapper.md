# Analytics Windows Developer Launcher Bootstrapper Contract-Test Report

report_lifecycle: final_approval
finding_lifecycle: fixed_state_followup

## Findings

No blocking findings remain.

### issue-210-p1-child-logs-bypass-redaction

- severity: P1
- finding_lifecycle: fixed_state_followup
- finding_status: fixed_state_followup
- blocking_status: resolved
- next_route: F
- verification_evidence: `tests/test_analytics_dev_app_launcher.py:170` to `tests/test_analytics_dev_app_launcher.py:207`; `tools/dev_app/dev_app_launcher.py:91` to `tools/dev_app/dev_app_launcher.py:101`; `tools/dev_app/dev_app_launcher.py:234` to `tools/dev_app/dev_app_launcher.py:256`; `tools/dev_app/dev_app_launcher.py:365` to `tools/dev_app/dev_app_launcher.py:385`; validation listed below.

Original finding: child process output bypassed redaction before durable writes to `backend.log` and `frontend.log`.

Verified fixed state: backend and frontend child log streams now go through a launcher-owned redacting writer before durable writes. Fake launchers receive the same `RedactingBinaryLog` wrapper used by start mode, and the focused regression proves synthetic repo-root, app-data-root, and home-like paths emitted by fake backend/frontend children are not written raw to `backend.log` or `frontend.log`.

The real subprocess path no longer binds child stdout/stderr directly to raw durable log file descriptors. `launch_process(...)` captures stdout/stderr with `stdout=subprocess.PIPE` and drains the pipe into the redacting writer on a background thread. Cleanup joins launcher-owned log-drain threads before closing child log handles.

## Issue And Scope

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/210>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Completed backend child: <https://github.com/Tahjali11/Mythic-Edge/issues/208>
- Completed frontend child: <https://github.com/Tahjali11/Mythic-Edge/issues/209>
- Branch: `codex/analytics-foundation`
- Contract: `docs/contracts/analytics_windows_developer_launcher_bootstrapper.md`
- Implementation handoff: `docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md`
- Fixer handoff: `docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_fixer.md`

## Contract Matches

- Branch is `codex/analytics-foundation` and is even with `origin/codex/analytics-foundation`.
- `uvicorn>=0.30,<1` remains scoped to optional `app` and `dev` dependency groups.
- The implementation scope remains limited to `pyproject.toml`, `tools/dev_app/`, focused launcher tests, issue #210 contract/handoff/report artifacts, and the fixer handoff.
- `check` mode reports preflight status and did not create app-data folders, logs, databases, config files, child processes, browser opens, or network-start side effects in validation.
- `start` mode test coverage uses temporary app-data roots.
- `start` mode creates only approved app-data subfolders and launcher log files in tests.
- Backend and frontend command construction uses loopback hosts and expected default ports.
- The frontend child receives process-local `VITE_MYTHIC_EDGE_API_BASE_URL`.
- No `.env` files are written.
- Port conflicts are reported without launching children or creating logs.
- Cleanup remains scoped to the launcher-owned `ManagedChild` list.
- The PowerShell wrapper remains thin and routes to the Python helper.
- `launcher.log`, `backend.log`, and `frontend.log` redaction coverage now includes launcher-written status lines and child process output written through the launcher.
- No clone/update, Git mutating command, shortcut creation, config write, database initialization, live watcher, parser runner control, destructive cleanup, or production behavior was found.

## Contract Mismatches

None found after the Codex D fixer pass.

## Missing Tests Or Safeguards

No missing blocker-level tests remain for the original P1. The new regression directly covers fake backend and frontend child output redaction for repo-root, app-data-root, and home-like path values.

Residual coverage note: manual long-running launcher behavior with live backend/frontend child processes remains unverified. The real subprocess path was inspected and the launcher dry-run plus fake-child start-mode tests passed.

## Validation Run

- `git status --short --branch` -> branch is `codex/analytics-foundation`; changed scope is issue #210 package files and `pyproject.toml`.
- `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation` -> `0 0`.
- `.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check` -> passed with redacted dry-run output.
- `py -m pytest -q tests\test_analytics_dev_app_launcher.py` -> 9 passed.
- `py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py` -> 18 passed, 1 third-party Starlette/FastAPI deprecation warning.
- `npm --prefix frontend ci` -> passed, 113 packages, 0 vulnerabilities.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> 3 files passed, 12 tests passed.
- `npm --prefix frontend run build` -> passed.
- `py -m ruff check src tests tools` -> passed.
- `py tools\check_agent_docs.py` -> passed, errors 0, warnings 0.
- `git diff --check` -> passed.
- Path-scoped protected-surface check over issue #210 files -> forbidden 0, warnings 0, passed.
- Path-scoped secret/private-marker scan over issue #210 files -> forbidden 0, warnings 0, passed.
- Generated `frontend/dist/`, `tools/dev_app/__pycache__/`, and `tests/__pycache__/` were removed after validation.

## Uvicorn And Dependency Assessment

The dependency metadata remains scoped correctly. `uvicorn` is optional app/dev support and did not become a core parser runtime dependency.

## Dry-Run And Start-Mode Side-Effect Assessment

Dry-run `check` behavior is side-effect free in validation. Start-mode tests confirm approved app-data folder/log creation, expected command construction, process-local frontend environment, port-conflict refusal, child-log redaction, and no database file creation.

## Process Cleanup Assessment

Cleanup remains scoped to the `ManagedChild` objects supplied to `cleanup_children(...)`. Tests prove an unrelated fake process is not touched and that an immediate frontend child exit terminates the started backend child. The fixer also joins launcher-owned output-drain threads before closing child log handles.

## Protected-Surface Status

No backend route payload shape, frontend setup/status behavior, parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, Match Journal behavior, OpenAI/model-provider behavior, AI/coaching behavior, production behavior, or deployment behavior changed.

## Secret And Private-Marker Status

Path-scoped scanner passed with forbidden 0 and warnings 0. The original runtime privacy safeguard gap was fixed by routing child log output through redaction before durable writes.

## Generated Artifact Status

- `frontend/node_modules/` exists locally and is ignored.
- `frontend/dist/` was produced by build validation and removed.
- `tools/dev_app/__pycache__/` and `tests/__pycache__/` were produced by validation and removed.
- No generated SQLite database, WAL, SHM, journal, raw log, local JSONL artifact, runtime output, retry artifact, workbook export, or generated card/tier data was detected as changed or untracked.

## Forbidden Scope

Forbidden scope was not touched. The fix stayed inside the authorized launcher/logging surface.

## Verdict

Ready for Codex F. The original P1 is resolved, no new blocking findings were found, and the issue #210 package is ready for submitter handling without targeting `main` or closing tracker #204.

## Next Recommended Role

Codex F: Module Submitter.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #210 on branch codex/analytics-foundation.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/210

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Contract:
docs/contracts/analytics_windows_developer_launcher_bootstrapper.md

Implementation handoff:
docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md

Fixer handoff:
docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_fixer.md

Review artifact:
docs/contract_test_reports/analytics_windows_developer_launcher_bootstrapper.md

Goal:
Submit the reviewed issue #210 package to a draft PR targeting the correct integration branch. Do not target main.

Before staging:
- Confirm branch is codex/analytics-foundation and is even with origin/codex/analytics-foundation.
- Inspect git status and stage only issue #210 files:
  - pyproject.toml
  - docs/contracts/analytics_windows_developer_launcher_bootstrapper.md
  - docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md
  - docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_fixer.md
  - docs/contract_test_reports/analytics_windows_developer_launcher_bootstrapper.md
  - tests/test_analytics_dev_app_launcher.py
  - tools/dev_app/dev_app_launcher.py
  - tools/dev_app/start_mythic_edge_dev_app.ps1
- Do not stage generated/private/local artifacts such as frontend/dist, node_modules, __pycache__, SQLite DB/WAL/SHM/journal files, raw logs, runtime files, failed posts, workbook exports, generated data, credentials, or local-only artifacts.

Validation to rerun or confirm:
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check
py -m pytest -q tests\test_analytics_dev_app_launcher.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
path-scoped protected-surface and secret/private-marker checks over the issue #210 package

After build validation, remove generated frontend/dist and any __pycache__ artifacts before staging.

Submitter actions:
- Commit only the reviewed issue #210 package.
- Push the branch.
- Open or update a draft PR targeting the non-main integration branch required by the tracker/workflow.
- Link issue #210, tracker #204, and umbrella issue #207.
- Do not merge, close issues, mark tracker #204 complete, target main, or change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior.
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / confirmation thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/210"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_windows_developer_launcher_bootstrapper.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_fixer.md"
  review_artifact: "docs/contract_test_reports/analytics_windows_developer_launcher_bootstrapper.md"
  findings:
    - severity: "P1"
      status: "fixed_state_followup"
      summary: "Child process output is now redacted before durable writes to backend.log and frontend.log."
  validation:
    - "branch sync -> 0 0"
    - "launcher -Check -> passed"
    - "launcher tests -> 9 passed"
    - "backend setup-status tests -> 18 passed, 1 third-party warning"
    - "frontend npm ci/typecheck/test/build -> passed"
    - "ruff -> passed"
    - "agent docs check -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
  generated_artifacts: "frontend/dist, tools/dev_app/__pycache__, and tests/__pycache__ removed after validation; no SQLite/raw/runtime/workbook artifacts found"
  forbidden_scope_touched: false
  verdict: "ready_for_codex_f"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
```
