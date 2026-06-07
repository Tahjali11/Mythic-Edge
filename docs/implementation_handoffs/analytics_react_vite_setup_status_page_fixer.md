# Analytics React Vite Setup-Status Page Fixer Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/209>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/204>

## Umbrella Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/207>

## Completed Backend Child

<https://github.com/Tahjali11/Mythic-Edge/issues/208>

## Contract

`docs/contracts/analytics_react_vite_setup_status_page.md`

## Review Artifact

`docs/contract_test_reports/analytics_react_vite_setup_status_page.md`

## Implementation Handoff Used

`docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md`

## Role Performed

Codex D: Module Fixer.

## Branch

`codex/analytics-foundation`

Branch relation observed:

```text
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0
```

## Finding Fixed

P1: missing required setup-status schema fields were classified as `incompatible_response` instead of `malformed_response`.

Fault category: frontend response-shape validation order.

## What Changed

`frontend/src/api.ts` now checks all required top-level setup-status fields before classifying compatibility. Missing `object`, `schema_version`, or any other required field raises `malformed_response`. A present but wrong `schema_version` still raises `incompatible_response`.

Wrong `object` values are also treated as malformed response shape, keeping `incompatible_response` reserved for unsupported schema versions.

## Files Changed By This Fixer Pass

- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `docs/implementation_handoffs/analytics_react_vite_setup_status_page_fixer.md`

Existing issue #209 frontend package files and docs remain in the working tree and were not staged.

## Code Changed

Runtime code changed: yes, frontend-only.

Behavior surface:

- added a shared `REQUIRED_SETUP_STATUS_FIELDS` list in `frontend/src/api.ts`
- moved required-field validation before schema compatibility validation
- preserved loopback-only API base URL validation
- preserved aggregate-only `/api/app/setup-status` consumption
- preserved read-only/no-control UI boundaries

No backend behavior, backend route payload shape, Python source, parser/runtime/workbook/webhook/App Script/Sheets/AI/production behavior changed.

## Tests Added Or Updated

`frontend/src/api.test.ts` now proves:

- missing `schema_version` is `malformed_response`
- missing `object` is `malformed_response`
- wrong `schema_version` remains `incompatible_response`
- wrong `object` is `malformed_response`
- non-object JSON remains `malformed_response`

## Interface Changes

None.

No package manager policy, dependency list, route names, backend payload fields, parser interfaces, workbook columns, webhook fields, environment variable contracts, or production entrypoints changed.

## Validation Run

```powershell
git status --short --branch
# codex/analytics-foundation...origin/codex/analytics-foundation

git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
# 0 0

node --version
# v24.14.0

npm --version
# blocked: npm is not on PATH

cmd /c npm --version
# blocked: npm is not on PATH

npm --prefix frontend run test -- --run frontend/src/api.test.ts
# blocked: npm is not on PATH

.\node_modules\.bin\vitest.cmd run src/api.test.ts
# before fix: failed on missing schema_version classified as incompatible_response
# after fix: 1 file passed, 5 tests passed

.\node_modules\.bin\tsc.cmd --noEmit
# passed

.\node_modules\.bin\vitest.cmd run
# 3 files passed, 12 tests passed

.\node_modules\.bin\vite.cmd build
# passed

py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
# 18 passed, 1 third-party FastAPI/Starlette deprecation warning

git diff --check
# passed

py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, changed_paths 22, forbidden 0, warnings 0

py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, scanned_paths 22, forbidden 0, warnings 0
```

Generated artifact cleanup:

- `frontend/dist/` was produced by Vite build validation and removed afterward.

## Protected-Surface Status

No forbidden protected surfaces were touched.

No changes were made to backend behavior, backend route payload shape, Python source, parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, Match Journal behavior, AI/OpenAI behavior, production behavior, secrets, environment variables, raw logs, generated local data, runtime state artifacts, retry-queue artifacts, workbook exports, or generated SQLite files.

## Secret / Private-Marker Status

No raw private path, raw log content, raw JSONL payload, secret, webhook URL, API key, token, or OAuth state was added by this fixer pass.

The path-scoped secret/private-marker scan over the issue #209 package passed with forbidden `0` and warnings `0`.

## Generated Artifact Status

- `frontend/node_modules/` exists locally and remains ignored.
- `frontend/dist/` was removed after build validation.
- `frontend/.vite/` and `frontend/coverage/` were not present after validation.
- No generated SQLite database, WAL, SHM, journal, raw log, local JSONL artifact, runtime output, retry payload, workbook export, or generated card/tier data was detected as changed or untracked.

## Still Unverified

- Exact npm commands remain unverified in this shell because `npm` is not on PATH.
- Clean reinstall via `npm --prefix frontend ci` remains for Codex F or a shell with npm available.
- Browser smoke was not rerun by this fixer thread.

## Reviewer Focus

Codex E should verify:

- missing required fields render/throw `malformed_response`
- present but wrong `schema_version` still renders/throws `incompatible_response`
- the UI's safe incompatible-response state remains for unsupported schema versions
- no backend/Python/protected production surfaces changed
- npm PATH limitation is recorded as non-blocking for this P1 fix but still a submitter validation risk

## Next Workflow Action

Next role: Codex E confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #209.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/209

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Completed backend child:
https://github.com/Tahjali11/Mythic-Edge/issues/208

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_react_vite_setup_status_page.md

Implementation handoff:
docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md

Prior review artifact:
docs/contract_test_reports/analytics_react_vite_setup_status_page.md

Fixer handoff:
docs/implementation_handoffs/analytics_react_vite_setup_status_page_fixer.md

Review only the Codex D fix for the P1 finding:
- missing required setup-status schema fields were classified as incompatible_response instead of malformed_response.

Confirm:
- missing object/schema_version/required fields are malformed_response;
- present but wrong schema_version remains incompatible_response;
- aggregate-only /api/app/setup-status consumption is preserved;
- loopback-only API base URL validation is preserved;
- no backend behavior, backend route payload shape, Python source, parser/runtime/workbook/webhook/App Script/Sheets/AI/production behavior changed;
- no new dependencies or package manager policy changes were introduced by Codex D.

Run:
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
git diff --check

If npm is unavailable, record the limitation and run the equivalent local frontend tools from frontend/node_modules/.bin if already installed.

Also run path-scoped protected-surface and secret/private-marker checks over the issue #209 package.

Route to Codex F only if the P1 is resolved and remaining validation limitations are accepted for submitter handling.
```

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/209"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_backend_child: "https://github.com/Tahjali11/Mythic-Edge/issues/208"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_react_vite_setup_status_page.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md"
  review_artifact: "docs/contract_test_reports/analytics_react_vite_setup_status_page.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_react_vite_setup_status_page_fixer.md"
  finding_fixed:
    - severity: "P1"
      summary: "Missing required schema fields were classified as incompatible_response instead of malformed_response."
  validation:
    - "branch sync -> 0 0"
    - "node --version -> v24.14.0"
    - "npm commands -> blocked because npm is not on PATH"
    - "frontend local api test -> 1 file passed, 5 tests passed"
    - "frontend local tsc -> passed"
    - "frontend local vitest -> 3 files passed, 12 tests passed"
    - "frontend local vite build -> passed; generated dist removed"
    - "backend setup-status tests -> 18 passed, 1 third-party warning"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
  forbidden_scope_touched: false
  npm_path_risk: "P2 remains; exact npm commands still need a shell with npm on PATH"
  next_thread: "E"
  next_role: "Codex E confirmation thread"
```
