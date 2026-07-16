# Sites-Compatible Frontend Build Contract-Test Report

## Findings

No blocking findings remain.

### SITES-BUILD-E-001 (P2): fixed-state confirmation

The original review found that correct static-asset delegation behavior lacked
a durable focused regression test. Codex D added a representative
`/assets/app.js` case to `frontend/worker/index.test.ts`. Independent Codex E
validation confirms that the test passes the original `Request` to the stub
`ASSETS.fetch` exactly once and returns the same `Response` object.

The focused Worker suite now passes 13 tests, and the complete frontend suite
passes 112 tests. No implementation code changed for this fix.

## Issue

Current owner-authorized local request. No GitHub issue was created.

## Tracker

None. Issue #648 is contextual only and grants no hosting or deployment
authority for this slice.

## Contract

`docs/contracts/sites_compatible_frontend_build.md`

## Implementation Under Test

- Branch: `codex/sites-compatible-frontend-build`
- Base: `origin/codex/analytics-foundation`
- Reviewed HEAD/base commit:
  `f24f17cca4b55d51a9e035b1436397f548461801`
- Implementation handoff:
  `docs/implementation_handoffs/sites_compatible_frontend_build_comparison.md`
- Scope: 3 modified files and 10 untracked contract/source/test/handoff files

## Report Lifecycle

`report_lifecycle: final_approval`

## Contract Summary

The implementation must produce a deterministic local Sites-compatible preview
shell while preserving the ordinary Vite development path, Windows launcher,
loopback API contract, backend behavior, and protected parser/analytics
surfaces. API paths must fail closed with exact symbolic JSON; non-API paths
may use only the `ASSETS` binding. No deployment or external write is
authorized.

## Internal Project Area Reviewed

`Local App / UI`, with Quality / Governance support for build-shape validation.

## Bridge-Code Status Reviewed

`bridge_code`: existing frontend source to local Sites-compatible generated
output only. No reverse authority into backend, parser, analytics, config,
SQLite, deployment, or external resources was introduced.

## Checks Run

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
node --version
npm --version
npm --prefix frontend ci
npm --prefix frontend test -- --run worker/index.test.ts
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run
npm --prefix frontend run build
node --test frontend/tests/sites-build-shape.test.mjs
py -m pytest -q tests/test_analytics_dev_app_launcher.py
npm --prefix frontend ls @cloudflare/vite-plugin@1.37.1 wrangler@4.92.0 vite@8.0.14 @vitejs/plugin-react@6.0.2 typescript@6.0.3 @types/node@22.19.19 --depth=0
git diff --check
py tools/check_agent_docs.py
py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools/check_secret_patterns.py --base origin/codex/analytics-foundation
# Both scanners were also run with --paths-from-stdin over all 13 reviewed paths.
# A synthetic post-build Worker probe covered API methods, navigation,
# static assets, case sensitivity, exact bodies, and ASSETS call boundaries.
```

## Results

- Branch sync: `0 0` against `origin/codex/analytics-foundation`.
- Runtime: Node `v24.16.0`; npm `11.13.0`.
- Clean lockfile install: passed; 147 packages installed.
- Exact dependency tree: all six contracted versions matched.
- Browser typecheck: passed.
- Focused Worker suite: 1 file, 13 tests passed.
- Vitest: 4 files, 112 tests passed.
- Sites build: passed; server/client output and 5 build-shape tests passed.
- Separate Node build-shape run: 5 tests passed.
- Launcher regression: 12 tests passed.
- Independent Worker probe: passed for GET, POST, PUT, PATCH, DELETE, OPTIONS,
  HEAD, navigation, static assets, `/apiary`, and case-sensitive `/API`.
- Hosting metadata source/build SHA-256 matched:
  `d532abb65cf9ae20634b464d954cb4a08a0de9f3cd3cdf7f9c3ec8948826d947`.
- Generated Wrangler resource collections were empty; no project, deployment,
  route, tunnel, remote binding, D1, R2, credential, or environment binding was
  configured.
- `git diff --check` and agent-doc validation passed.
- `frontend/dist`, `frontend/.wrangler`, and coverage output were absent after
  verified cleanup.
- `npm ci` reported 7 dependency advisories (1 low, 6 high). They remain an
  untriaged residual risk outside this implementation contract.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SITES-BUILD-E-001 | P2 | `fixed_state_followup` | `fixed_confirmed` | non-blocking, closed | Contract lines 623-633 require navigation and static-asset requests to call only the stub assets binding; the initial review found no durable `/assets/app.js` case. | `frontend/worker/index.test.ts` now verifies original-request identity, exactly one `ASSETS.fetch` call, and response pass-through; 13 focused and 112 full Vitest tests passed independently. | Codex F recommendation |

## Confirmed Contract Matches

- `/api` and `/api/*` return exact ordered non-HTML 503 JSON for all reviewed
  methods, with the required headers, empty HEAD body, no CORS header, and no
  asset invocation or input echo.
- Non-API requests preserve and delegate the original `Request` only through
  `ASSETS`; absent or rejected assets fail closed with symbolic JSON.
- Source hosting metadata is the exact two-key null object and is copied
  byte-for-byte into generated output after strict validation.
- The build emits importable `dist/server/index.js`, client entry/assets,
  generated Wrangler metadata, and no Drizzle directory.
- Node and all six selected build packages are exact and lockfile-backed.
- `frontend/vite.config.ts`, frontend API/type/status sources, launcher, and
  launcher tests remain byte-identical to the base.
- No backend route, host/CORS, parser, analytics, schema, migration, workbook,
  transport, AI, CI, deployment, or production behavior changed.
- No Sites project, hosted version, tunnel, remote binding, account action, or
  external write was performed.

## Contract Mismatches

None remaining.

## Missing Tests

None identified in the reviewed scope.

## Protected-Surface Status

Path-fed protected-surface scan over all 13 reviewed paths passed with
`forbidden: 0`, `warnings: 0`. Reference-only local app, backend, parser,
analytics, transport, and launcher surfaces were unchanged.

## Secret And Private-Marker Status

Path-fed secret/private-marker scan over all 13 reviewed paths passed with
`forbidden: 0`, `warnings: 0`. Generated output contained no raw absolute local
path, credential, token, or private artifact value. Existing public-safe UI
labels such as `Player.log` and symbolic `%LOCALAPPDATA%` placeholders are not
raw evidence.

## Generated Artifact Status

The review generated only ignored local build/tool output. The verified
`frontend/dist` and `frontend/.wrangler` trees were removed after inspection;
coverage output was absent. No generated artifact is retained or staged.

## Drift Notes

No repository drift was observed: branch and base are synchronized at the same
commit. No deployment, local-data, issue, PR, or tracker state was created or
mutated. The lack of a GitHub issue remains an explicit contract limitation,
not hidden lifecycle evidence.

## Recommendation

`approve for Codex F submission review`

`SITES-BUILD-E-001` is independently closed. Codex F is recommended to stage
only the 14 reviewed paths, verify the intended non-main base, and prepare the
submission lifecycle if separately invoked. Deployment, Sites project
creation, and external writes remain unauthorized.

## Next Workflow Action

Next role: Codex F, Module Submitter, only when separately invoked by the
owner.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for the Sites-compatible frontend build.

Branch: codex/sites-compatible-frontend-build
Contract: docs/contracts/sites_compatible_frontend_build.md
Review: docs/contract_test_reports/sites_compatible_frontend_build.md

Confirm the branch and approved non-main base, inspect the full status, and
stage only the 14 paths reviewed by Codex E. Verify the report remains
`final_approval`, validation evidence is current, generated output is absent,
and no unrelated file is included. Commit, push, and open or update a draft PR
only when explicitly authorized by this Codex F invocation. Do not deploy,
create a Sites project, perform an external write, target main, or claim hosted
compatibility or readiness. Route merge or deployment consideration to Codex G.
```

```yaml
workflow_handoff:
  issue: "current owner-authorized local request; no GitHub issue created"
  tracker: ""
  completed_thread: "E_confirmation"
  next_thread: "F"
  source_artifact: "docs/contracts/sites_compatible_frontend_build.md"
  implementation_handoff: "docs/implementation_handoffs/sites_compatible_frontend_build_comparison.md"
  target_artifact: "docs/contract_test_reports/sites_compatible_frontend_build.md"
  risk_tier: "High"
  branch: "codex/sites-compatible-frontend-build"
  finding_status:
    SITES-BUILD-E-001: "fixed_confirmed"
  validation:
    - "npm ci, 13 focused Worker tests, typecheck, 112 Vitest tests, Sites build, 5 build-shape tests, and 12 launcher tests passed"
    - "protected-surface scan passed, forbidden 0, warnings 0"
    - "secret/private-marker scan passed, forbidden 0, warnings 0"
  deployment_authorized: false
  external_writes_authorized: false
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  ready_for_codex_f: true
  next_recommended_role: "Codex F: Module Submitter, only when separately invoked"
```
