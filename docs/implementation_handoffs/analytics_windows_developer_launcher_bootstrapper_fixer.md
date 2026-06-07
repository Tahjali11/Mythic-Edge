# Analytics Windows Developer Launcher Bootstrapper Fixer Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/210>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/204>

## Umbrella Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/207>

## Contract

`docs/contracts/analytics_windows_developer_launcher_bootstrapper.md`

## Review Artifact

`docs/contract_test_reports/analytics_windows_developer_launcher_bootstrapper.md`

## Implementation Handoff Used

`docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md`

## Role Performed

Codex D: Module Fixer.

## Branch

`codex/analytics-foundation`

Branch relation observed:

```text
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0
```

## Finding Fixed

P1: child process output bypassed redaction before durable writes to `backend.log` and `frontend.log`.

Fault category: launcher-managed durable log privacy safeguard gap.

## What Changed

Child stdout/stderr is now routed through the launcher redactor before it reaches durable child log files. Fake process launchers used by tests receive the same redacting binary writer as the real launcher path. The real `launch_process(...)` path now captures child stdout/stderr through a pipe and drains it to the redacting writer in a background thread instead of handing the child process a raw log file descriptor.

## Files Changed By This Fixer Pass

- `tools/dev_app/dev_app_launcher.py`
- `tests/test_analytics_dev_app_launcher.py`
- `docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_fixer.md`

Existing issue #210 package files remain in the working tree and were not staged.

## Code Changed

Runtime code changed: yes, launcher-only under `tools/dev_app/dev_app_launcher.py`.

Behavior surface:

- added `RedactingBinaryLog`
- wrapped backend and frontend child log writers with the launcher redactor
- changed real subprocess output handling to `stdout=subprocess.PIPE`
- added a background child-output drain that writes redacted bytes to the durable log
- joins launcher-owned log drain threads before closing child log handles

Preserved:

- `launcher.log` redaction
- check-mode no-write/no-process/no-browser behavior
- start-mode app-data and log folder boundaries
- backend/frontend command construction
- process-local frontend `VITE_MYTHIC_EDGE_API_BASE_URL`
- cleanup limited to launcher-owned children

## Tests Added Or Updated

`tests/test_analytics_dev_app_launcher.py` now proves backend and frontend child output containing synthetic repo-root, app-data-root, and home-like path values is not written raw to `backend.log` or `frontend.log`.

The focused regression failed before the implementation fix and passed afterward.

## Interface Changes

None.

No CLI flags, PowerShell parameters, backend route payloads, frontend API shapes, parser interfaces, workbook columns, webhook fields, environment-variable contracts, dependency policy, or production entrypoints changed.

## Validation Run

```powershell
git status --short --branch
# codex/analytics-foundation...origin/codex/analytics-foundation

git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
# 0 0

py -m pytest -q tests\test_analytics_dev_app_launcher.py
# before fix: failed on raw repo path in backend.log
# after fix: 9 passed

.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check
# passed

py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
# 18 passed, 1 third-party FastAPI/Starlette deprecation warning

npm --version
# 11.13.0

npm --prefix frontend ci
# passed, 113 packages, 0 vulnerabilities

npm --prefix frontend run typecheck
# passed

npm --prefix frontend run test -- --run
# 3 files passed, 12 tests passed

npm --prefix frontend run build
# passed

py -m ruff check src tests tools
# passed

git diff --check
# passed

py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, changed_paths 8, forbidden 0, warnings 0

py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, scanned_paths 8, forbidden 0, warnings 0
```

Generated artifact cleanup:

- `frontend/dist/` was produced by build validation and removed afterward.
- `tools/dev_app/__pycache__/` was removed after validation.

## Protected-Surface Status

No forbidden protected surfaces were touched.

No changes were made to backend behavior, frontend setup/status behavior, parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, Match Journal behavior, OpenAI/model-provider behavior, AI/coaching behavior, production behavior, deployment behavior, secrets, environment variables, raw logs, generated local data, runtime state artifacts, retry-queue artifacts, workbook exports, or generated SQLite files.

## Secret / Private-Marker Status

The fix is a runtime redaction safeguard for launcher-managed logs. No raw private path, raw log content, raw JSONL content, secret, webhook URL, API key, token, or OAuth state was added by this fixer pass.

The path-scoped secret/private-marker scan over the issue #210 package passed with forbidden `0` and warnings `0`.

## Generated Artifact Status

- `frontend/node_modules/` exists locally and remains ignored.
- `frontend/dist/` was removed after build validation.
- `tools/dev_app/__pycache__/` was removed after validation.
- No generated SQLite database, WAL, SHM, journal, raw log, local JSONL artifact, runtime output, retry artifact, workbook export, or generated card/tier data was detected as changed or untracked.

## Still Unverified

- Full repository test suite was not run.
- Manual long-running launcher behavior with real backend/frontend child processes was not exercised beyond the dry-run and fake-child start-mode tests.

## Reviewer Focus

Codex E should verify:

- fake backend child output is redacted before durable `backend.log` writes
- fake frontend child output is redacted before durable `frontend.log` writes
- real subprocess output no longer receives a raw file descriptor for durable log output
- launcher check mode remains no-write/no-process/no-browser
- start-mode folder/log boundaries and process cleanup remain scoped
- no backend/frontend/parser/runtime/workbook/webhook/App Script/Sheets/AI/production behavior changed

## Next Workflow Action

Next role: Codex E confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #210.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/210

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_windows_developer_launcher_bootstrapper.md

Implementation handoff:
docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md

Prior review artifact:
docs/contract_test_reports/analytics_windows_developer_launcher_bootstrapper.md

Fixer handoff:
docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_fixer.md

Review only the Codex D fix for the P1 finding:
- child process output bypassed redaction before durable writes to backend.log and frontend.log.

Confirm:
- synthetic repo-root, app-data-root, and home-like path values emitted by fake backend/frontend children are not written raw to backend.log or frontend.log;
- real child stdout/stderr is piped through the redacting writer rather than bound directly to raw durable log handles;
- launcher.log redaction is preserved;
- check-mode no-write/no-process/no-browser behavior is preserved;
- start-mode app-data/log folder boundaries, command construction, process-local frontend environment, and launcher-owned cleanup remain preserved;
- no backend/frontend/parser/runtime/workbook/webhook/App Script/Sheets/AI/production behavior changed.

Run:
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check
py -m pytest -q tests\test_analytics_dev_app_launcher.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check

Also run path-scoped protected-surface and secret/private-marker checks over the issue #210 package.

Route to Codex F only if the P1 is resolved and no new blocking findings remain.
```

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/210"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_windows_developer_launcher_bootstrapper.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_comparison.md"
  review_artifact: "docs/contract_test_reports/analytics_windows_developer_launcher_bootstrapper.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_windows_developer_launcher_bootstrapper_fixer.md"
  finding_fixed:
    - severity: "P1"
      summary: "Child process output bypassed redaction before durable writes to backend.log and frontend.log."
  validation:
    - "branch sync -> 0 0"
    - "launcher tests -> 9 passed"
    - "launcher -Check -> passed"
    - "backend setup-status tests -> 18 passed, 1 third-party warning"
    - "npm --version -> 11.13.0"
    - "frontend npm ci/typecheck/test/build -> passed"
    - "ruff -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
    - "generated frontend dist and tools/dev_app pycache removed"
  forbidden_scope_touched: false
  next_thread: "E"
  next_role: "Codex E confirmation thread"
```
