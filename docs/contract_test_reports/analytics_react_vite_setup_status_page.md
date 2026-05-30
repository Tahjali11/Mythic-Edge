# Analytics React Vite Setup-Status Page Contract-Test Report

report_lifecycle: final_approval
finding_lifecycle: fixed_state_followup

## Findings

No blocking findings remain after the Codex D fixer pass.

### issue-209-p1-missing-required-schema-field-classified-as-incompatible

- severity: P1
- finding_lifecycle: fixed_state_followup
- finding_status: fixed
- blocking_status: not_blocking
- next_route: F

Original finding: the contract requires missing required fields to render the safe malformed-response state, while only a wrong `schema_version` should render the incompatible-response state. The split is specified in `docs/contracts/analytics_react_vite_setup_status_page.md:426` to `docs/contracts/analytics_react_vite_setup_status_page.md:427`.

Verification: `frontend/src/api.ts:86` to `frontend/src/api.ts:100` now validates required fields before schema compatibility, reports missing fields as `malformed_response`, preserves wrong `schema_version` as `incompatible_response`, and treats wrong object identity as malformed shape. `frontend/src/api.test.ts:27` to `frontend/src/api.test.ts:52` covers missing `schema_version`, missing `object`, wrong schema version, wrong object, and non-object JSON.

### issue-209-p2-npm-not-on-review-shell-path

- severity: P2
- finding_lifecycle: remaining_non_blocking
- finding_status: validation_limited
- blocking_status: non_blocking_for_submitter
- next_route: F

`npm` is still unavailable on PATH in this review shell, including through `cmd /c npm --version`. Local installed frontend tool equivalents pass, but Codex F should rerun the exact npm commands in an environment where npm is available before submission.

## Issue And Scope

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/209>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Completed backend child: <https://github.com/Tahjali11/Mythic-Edge/issues/208>
- Branch: `codex/analytics-foundation`
- Contract: `docs/contracts/analytics_react_vite_setup_status_page.md`
- Implementation handoff: `docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md`
- Fixer handoff: `docs/implementation_handoffs/analytics_react_vite_setup_status_page_fixer.md`

## Contract Matches

- Branch is `codex/analytics-foundation` and is even with `origin/codex/analytics-foundation`.
- Changed scope is limited to `.gitignore`, `frontend/`, and issue #209 docs/handoffs/report.
- No root `package.json`, root lockfile, workspace, or alternate package manager was added.
- `frontend/package.json` includes the required `dev`, `typecheck`, `test`, `build`, and `preview` scripts.
- `frontend/package.json` includes `engines.node` with `>=20`.
- Direct runtime dependencies are limited to `react` and `react-dom`.
- Direct development dependencies are limited to the contract-authorized frontend tooling set.
- `frontend/package-lock.json` exists.
- `.gitignore` ignores `frontend/node_modules/`, `frontend/dist/`, `frontend/.vite/`, and `frontend/coverage/`.
- Frontend source lives under `frontend/`.
- The API client and UI reference only the aggregate `/api/app/setup-status` endpoint for main setup-status data.
- API base URL override remains constrained to empty or loopback HTTP origins with a valid port.
- Missing required setup-status fields are now `malformed_response`.
- Present but wrong `schema_version` remains `incompatible_response`.
- The UI has loading, backend unavailable, malformed, incompatible, ready/degraded, unsafe-display-redacted, and deferred states.
- Safe path labels render, and synthetic unsafe path-like display values are redacted.
- Manual import, analytics views, and live watcher sections remain display-only placeholders.
- No buttons, inputs, file pickers, import controls, start/stop controls, reset/delete/wipe controls, Sheets controls, AI controls, Git controls, or production controls were found in the implemented UI.
- Backend behavior and backend route payload shape were not changed.
- Parser/runtime/workbook/webhook/App Script/Sheets/AI/production behavior was not changed.

## Contract Mismatches

None remaining after the Codex D fixer pass.

## Missing Tests Or Safeguards

None remaining for the original P1. Codex D added the required malformed-vs-incompatible response classification coverage.

## Validation Run

- `git fetch --prune` -> passed.
- `git status --short --branch` -> branch is `codex/analytics-foundation`; changed scope is `.gitignore`, `frontend/`, and issue #209 docs/handoffs/report.
- `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation` -> `0 0`.
- `node --version` -> `v24.14.0`.
- `npm --version` -> failed; `npm` not available on PATH in this review shell.
- `cmd /c npm --version` -> failed; `npm` not available on PATH in this review shell.
- `.\node_modules\.bin\vitest.cmd run src/api.test.ts` from `frontend/` -> 1 file passed, 5 tests passed.
- `.\node_modules\.bin\tsc.cmd --noEmit` from `frontend/` -> passed.
- `.\node_modules\.bin\vitest.cmd run` from `frontend/` -> 3 files passed, 12 tests passed.
- `.\node_modules\.bin\vite.cmd build` from `frontend/` -> passed.
- Generated `frontend/dist/` was removed after build validation.
- `py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py` -> 18 passed, 1 third-party deprecation warning.
- `git diff --check` -> passed.
- Path-scoped protected-surface check over issue #209 files -> forbidden 0, warnings 0, passed.
- Path-scoped secret/private-marker scan over issue #209 files -> forbidden 0, warnings 0, passed.
- Browser smoke was not rerun in this confirmation thread. Codex C previously reported the Vite page rendered the safe backend-unavailable state without a backend.

## Dependency And Lockfile Assessment

The dependency and lockfile shape matches the contract. The only remaining validation limitation is local tool availability: npm is not on PATH in this review shell, so clean `npm --prefix frontend ci` remains for Codex F to rerun in an npm-capable environment.

## API Consumption Assessment

The frontend uses only `/api/app/setup-status` for main setup-status data. The API base URL override remains loopback-only. The original missing-required-field classification mismatch is fixed.

## UI State And No-Control Assessment

The setup-status page remains the first screen and is read-only. Required panels and deferred placeholders are present. No action controls were found.

## Protected-Surface Status

No backend behavior, backend route payload shape, parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, AI behavior, production behavior, deployment behavior, or generated local-data behavior changed.

## Secret And Private-Marker Status

Path-scoped secret/private-marker scan passed with forbidden 0 and warnings 0. Frontend tests use synthetic unsafe path-like values and do not include raw private machine paths, raw log contents, raw JSONL payloads, secrets, webhook URLs, API keys, or tokens.

## Generated Artifact Status

- `frontend/node_modules/` exists locally and is ignored.
- `frontend/dist/` was produced by build validation and removed afterward.
- `frontend/.vite/` and `frontend/coverage/` are absent.
- No generated SQLite database, WAL, SHM, journal, raw log, local JSONL artifact, runtime output, retry payload, workbook export, or generated card/tier data was detected as changed or untracked.

## Forbidden Scope

Forbidden scope was not touched.

## Verdict

Ready for Codex F with npm PATH caution. Codex F should stage only the reviewed issue #209 package and rerun exact npm validation commands in an environment where npm is available before submission.

## Next Recommended Role

Codex F: Module Submitter.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #209 on branch codex/analytics-foundation.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/209

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Completed backend child:
https://github.com/Tahjali11/Mythic-Edge/issues/208

Contract:
docs/contracts/analytics_react_vite_setup_status_page.md

Implementation handoff:
docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md

Fixer handoff:
docs/implementation_handoffs/analytics_react_vite_setup_status_page_fixer.md

Review artifact:
docs/contract_test_reports/analytics_react_vite_setup_status_page.md

Goal:
Submit the reviewed issue #209 React + TypeScript + Vite setup-status page package only if intended-file staging and npm validation are safe.

Before staging:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and identify unrelated dirty/untracked files.
- Recheck HEAD...origin/codex/analytics-foundation.
- Rerun exact npm validation commands in an environment where npm is available.
- Do not target main unless explicitly approved.

Intended issue #209 files include:
- .gitignore
- docs/contracts/analytics_react_vite_setup_status_page.md
- docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md
- docs/implementation_handoffs/analytics_react_vite_setup_status_page_fixer.md
- docs/contract_test_reports/analytics_react_vite_setup_status_page.md
- frontend/package.json
- frontend/package-lock.json
- frontend/index.html
- frontend/vite.config.ts
- frontend/tsconfig.json
- frontend/tsconfig.node.json
- frontend/src/main.tsx
- frontend/src/App.tsx
- frontend/src/api.ts
- frontend/src/types.ts
- frontend/src/status.ts
- frontend/src/App.css
- frontend/src/vite-env.d.ts
- frontend/src/test/setup.ts
- frontend/src/api.test.ts
- frontend/src/status.test.ts
- frontend/src/App.test.tsx

Do not stage frontend/node_modules, frontend/dist, frontend/.vite, frontend/coverage, generated/private/local artifacts, secrets, raw logs, local JSONL artifacts, generated SQLite files, runtime status, retry payloads, workbook exports, or unrelated files.

Run:
git status --short --branch
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py
git diff --check

Also rerun path-scoped protected-surface and secret/private-marker checks over the issue #209 package.

If safe, stage only reviewed issue #209 files, commit, push, and open or update the appropriate draft PR against the approved integration target. If npm remains unavailable, stop and report the validation blocker instead of submitting.
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / confirmation thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/209"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_backend_child: "https://github.com/Tahjali11/Mythic-Edge/issues/208"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_react_vite_setup_status_page.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_react_vite_setup_status_page_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_react_vite_setup_status_page_fixer.md"
  review_artifact: "docs/contract_test_reports/analytics_react_vite_setup_status_page.md"
  findings:
    - severity: "P1"
      status: "fixed_state_followup"
      summary: "Missing required schema fields now classify as malformed_response while wrong schema_version remains incompatible_response."
    - severity: "P2"
      status: "remaining_non_blocking"
      summary: "npm is not available on PATH in this review shell; local frontend tool equivalents passed."
  validation:
    - "branch sync -> 0 0"
    - "node --version -> v24.14.0"
    - "npm validation commands -> blocked because npm is not on PATH"
    - "frontend local api test -> 1 file passed, 5 tests passed"
    - "frontend local tsc -> passed"
    - "frontend local vitest -> 3 files passed, 12 tests passed"
    - "frontend local vite build -> passed; generated dist removed"
    - "backend setup-status tests -> 18 passed, 1 third-party warning"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
  forbidden_scope_touched: false
  npm_path_risk: "Exact npm commands still need a shell with npm on PATH before submitter work completes."
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
```
