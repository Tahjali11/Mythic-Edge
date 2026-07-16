# Sites-Compatible Frontend Build Comparison

## Issue And Tracker

- Issue: current owner-authorized local implementation request; no GitHub issue
  was created.
- Tracker: none.
- Base branch: `codex/analytics-foundation`.
- Implementation branch: `codex/sites-compatible-frontend-build`.
- Base and current HEAD during implementation:
  `f24f17cca4b55d51a9e035b1436397f548461801` (`0 0` from
  `origin/codex/analytics-foundation`).

## Contract

- Problem representation:
  `docs/problem_representations/sites_compatible_frontend_build.md`
- Contract: `docs/contracts/sites_compatible_frontend_build.md`
- Contracted risk tier: High.

The problem representation, contract, and `frontend/.openai/hosting.json` were
pre-existing untracked inputs. Codex C preserved them without rewriting them.

## Internal Project Area

Local App / UI, with a build-only bridge to an external Sites-compatible
hosting surface.

## Truth Owner

The existing loopback backend API and accepted frontend contracts remain the
truth owners. The preview Worker returns only a fixed unavailable response for
API paths and does not synthesize, proxy, or persist backend data.

## Bridge-Code Status

`bridge_code`

## Role Performed

Codex C: Module Implementer.

## Intended Versus Actual Behavior

Intended behavior:

- preserve ordinary Vite development and the Windows launcher;
- type-check browser and Sites-specific source;
- emit `dist/client/index.html`, client assets, and
  `dist/server/index.js`;
- copy reviewed hosting metadata byte-for-byte to
  `dist/.openai/hosting.json`; and
- return a deterministic non-HTML `503` for `/api` and `/api/*` without
  touching assets or an external service.

Observed before implementation:

- `npm run build` used `tsc --noEmit && vite build`;
- only client files were emitted under `dist/`; and
- no Worker entry, metadata staging, Sites-specific configuration, or output
  shape test existed.

The first proven failure point was the client-only package/build interface in
`frontend/package.json` and the absence of a separate Sites build path.

## Implementation Option Chosen

The ordinary `frontend/vite.config.ts` remains unchanged. `npm run build` now
selects a separate Cloudflare Vite configuration, while `npm run dev` and
`npm run preview` preserve their prior scripts.

The Sites-only configuration:

- names the Worker and Vite environment `server`;
- uses `frontend/worker/index.ts` as the Worker entry;
- fixes compatibility date `2026-07-15`;
- binds only `ASSETS`;
- configures SPA fallback and Worker-first `/api` routing;
- disables persistent Cloudflare state, remote bindings, and observability;
  and
- declares no hosted resource, credential, route, domain, service, or
  environment binding.

The generated Wrangler metadata contains the plugin's empty default resource
collections. Focused tests require those collections to remain empty and
reject configured resource or deployment bindings.

## Files Changed

Modified:

- `.gitignore`
- `frontend/package.json`
- `frontend/package-lock.json`

Added:

- `frontend/build/sites-vite-plugin.ts`
- `frontend/tests/sites-build-shape.test.mjs`
- `frontend/tsconfig.sites.json`
- `frontend/vite.sites.config.ts`
- `frontend/worker/index.ts`
- `frontend/worker/index.test.ts`
- `docs/implementation_handoffs/sites_compatible_frontend_build_comparison.md`

Pre-existing untracked inputs preserved:

- `docs/problem_representations/sites_compatible_frontend_build.md`
- `docs/contracts/sites_compatible_frontend_build.md`
- `frontend/.openai/hosting.json`

Reference-only files confirmed byte-identical to the base:

- `frontend/vite.config.ts`
- `frontend/src/api.ts`
- `tools/dev_app/dev_app_launcher.py`
- `tests/test_analytics_dev_app_launcher.py`

## Code And Interface Changes

- `frontend/worker/index.ts` adds a stateless Worker `fetch` interface.
- `/api` and `/api/*` return the exact contracted unavailable JSON, headers,
  status, and empty HEAD body.
- Non-API requests delegate only to the original `Request` through
  `env.ASSETS.fetch`.
- Missing or failing assets return sanitized symbolic JSON with
  `preview_assets_unavailable` and no exception or request echo.
- `frontend/build/sites-vite-plugin.ts` validates the two-key null metadata
  object, replaces only generated `dist/.openai`, copies exact source bytes,
  and verifies the SHA-256 digest.
- The Node engine changes from `>=20` to `>=22.12.0`.
- `npm run build` now performs browser typecheck, Sites typecheck, Sites Vite
  build, metadata staging, and Node build-shape validation.
- `npm test` excludes the Node-native build-shape file; all Vitest source tests
  remain selected.

No frontend API, backend API, launcher, parser, analytics, database, workbook,
transport, AI, CI, deployment, or production interface changed.

## Dependency Decision

The six contract-selected build dependencies are exact and lockfile-backed:

- `@cloudflare/vite-plugin` `1.37.1`
- `wrangler` `4.92.0`
- `vite` `8.0.14`
- `@vitejs/plugin-react` `6.0.2`
- `typescript` `6.0.3`
- `@types/node` `22.19.19`

No global package, alternate package manager, broad version range, force
install, deploy script, postinstall deployment, D1, or R2 dependency was
introduced.

## Tests Added

`frontend/worker/index.test.ts` covers:

- exact GET, POST, OPTIONS, and HEAD API behavior;
- no asset call for API paths;
- `/apiary` exclusion;
- original-request asset delegation;
- absent and failing asset bindings;
- no request, query, header, body, or exception echo;
- deterministic repeated requests;
- strict hosting metadata validation;
- exact metadata byte copy; and
- missing metadata refusal and generated-directory replacement.

`frontend/tests/sites-build-shape.test.mjs` covers:

- exact source metadata shape and byte/digest equality;
- client entry and non-empty assets;
- importable ESM Worker output;
- exact compiled API-unavailable behavior;
- no configured resource, remote, route, project, or deployment binding;
- disabled generated observability;
- no generated Drizzle output; and
- ignored generated output.

## Validation Run

Observed passing final validation:

```text
node --version
  v24.16.0
npm --version
  11.13.0
npm --prefix frontend ci
  passed; 147 packages installed
npm --prefix frontend run typecheck
  passed
npm --prefix frontend test -- --run
  passed; 4 files, 111 tests
npm --prefix frontend run build
  passed; server and client environments built; 5 shape tests passed
node --test frontend/tests/sites-build-shape.test.mjs
  passed; 5 tests
py -m pytest -q tests/test_analytics_dev_app_launcher.py
  passed; 12 tests
git diff --check
  passed
```

The exact dependency tree was also checked with `npm ls`; all six selected
versions matched the contract.

The first full Vitest run attempted to collect the Node-native build-shape
test and failed with `No test suite found`. The test script was corrected to
exclude that one file from Vitest, after which the complete 111-test Vitest
suite and the separate five-test Node suite passed.

`npm ci` reported seven dependency advisories (one low and six high). No
`npm audit fix`, forced update, or unrelated dependency remediation was run.
The advisory details and any dependency-policy response remain outside this
implementation contract.

Final governance validation after writing this handoff:

```text
py tools/check_agent_docs.py
  passed; 47 files, 0 errors, 0 warnings
py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation
  passed; base diff contained 0 committed paths, 0 forbidden, 0 warnings
py tools/check_secret_patterns.py --base origin/codex/analytics-foundation
  passed; base diff contained 0 committed paths, 0 forbidden, 0 warnings
path-fed protected-surface and secret/private-marker scans
  passed over all 13 scope paths; 0 forbidden, 0 warnings
```

## Generated And Private Artifact Status

The successful build produced and validated:

- `frontend/dist/server/index.js`
- `frontend/dist/server/wrangler.json`
- `frontend/dist/client/index.html`
- `frontend/dist/client/assets/*`
- `frontend/dist/.openai/hosting.json`

Observed source and built metadata SHA-256:

```text
d532abb65cf9ae20634b464d954cb4a08a0de9f3cd3cdf7f9c3ec8948826d947
```

The generated Worker, Wrangler metadata, client entry, and metadata were
checked for named local/private markers with no matches. After validation,
`frontend/dist/` and `frontend/.wrangler/` were removed; coverage output was
absent. `frontend/node_modules/` remains ignored local dependency state.

No raw log, JSONL, SQLite, Match Journal, runtime, import, capture,
failed-post, workbook, secret, credential, environment, or local-only data was
read, copied, emitted, staged, or committed.

## Protected-Surface Status

The implementation changed only the contracted frontend package/build bridge
and generated-artifact ignore policy. It did not change:

- ordinary local Vite development;
- the Windows launcher or loopback URL;
- frontend API paths or validation;
- backend routes, hosts, or CORS;
- parser behavior, state, identity, or reconciliation;
- analytics behavior, schema, migrations, or ingest;
- Match Journal, capture, import, or error-report behavior;
- workbook, webhook, Apps Script, Sheets, or transport;
- OpenAI, AI/coaching, or Line Tracer behavior;
- CI, deployment, or production behavior.

## Still Unverified And Non-Claims

- No Sites project or hosted version exists.
- No deployment, preview URL, Cloudflare account call, tunnel, or remote
  binding was exercised.
- Actual Sites/Cloudflare runtime behavior is unverified.
- Hosted backend compatibility and local/private data access are intentionally
  unavailable and unverified.
- The npm advisory findings remain untriaged by this contract.
- This work does not establish security, privacy, release, public, deploy, or
  production readiness.

## Reviewer Focus

Codex E should verify:

- exact API body key order, headers, HEAD behavior, and asset non-invocation;
- no API-like path can receive SPA HTML;
- no request or exception data can enter symbolic unavailable output;
- metadata validation, byte equality, and generated-directory containment;
- exact dependency versions and clean `npm ci` behavior;
- generated Wrangler resource collections remain empty;
- ordinary Vite/API/launcher sources remain base-identical; and
- all generated build/tool output is absent from final status.

## Codex D Fixer Update

Role performed: Codex D, Module Fixer.

Source finding:

- `SITES-BUILD-E-001`: the implementation had correct static-asset delegation
  behavior, but lacked a durable focused Vitest regression for a representative
  static asset path.

Fault category: missing contract safeguard test. No runtime code defect was
observed and no implementation code was changed.

Fix produced:

- Added `frontend/worker/index.test.ts` coverage for
  `https://preview.invalid/assets/app.js`.
- The test proves static asset requests receive the original `Request`, call
  the stub `ASSETS.fetch` exactly once, and pass through the returned
  `Response`.
- Existing navigation, `/apiary`, API-unavailable, metadata, build, launcher,
  and generated-artifact behavior was preserved.

Validation after the D fix:

```text
npm --prefix frontend test -- --run frontend/worker/index.test.ts
  setup/filter error; Vitest runs from frontend and found no repo-root-relative file
npm --prefix frontend test -- --run worker/index.test.ts
  passed; 1 file, 13 tests
npm --prefix frontend run typecheck
  passed
npm --prefix frontend test -- --run
  passed; 4 files, 112 tests
npm --prefix frontend run build
  passed; server/client build and 5 build-shape tests passed
node --test frontend/tests/sites-build-shape.test.mjs
  passed; 5 tests
py -m pytest -q tests/test_analytics_dev_app_launcher.py
  passed; 12 tests
npm --prefix frontend ci
  passed; 147 packages installed; npm reported 7 advisories, unchanged residual risk
npm --prefix frontend test -- --run worker/index.test.ts
  passed after npm ci; 1 file, 13 tests
git diff --check
  passed
py tools/check_agent_docs.py
  passed; 47 files, 0 errors, 0 warnings
py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation
  passed; changed_paths 0, forbidden 0, warnings 0
py tools/check_secret_patterns.py --base origin/codex/analytics-foundation
  passed; scanned_paths 0, forbidden 0, warnings 0
path-fed protected-surface scan over 14 scoped paths
  passed; forbidden 0, warnings 0
path-fed secret/private-marker scan over 14 scoped paths
  passed; forbidden 0, warnings 0
```

Generated artifact status after the D fix:

- `frontend/dist/`, `frontend/.wrangler/`, and `frontend/coverage/` were
  removed if present after build validation.
- No generated artifact, deployment output, local backend output, private data,
  or external write was retained.

## Next Workflow Action

Next role: Codex E, Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread.

Source problem representation:
docs/problem_representations/sites_compatible_frontend_build.md

Contract:
docs/contracts/sites_compatible_frontend_build.md

Implementation handoff:
docs/implementation_handoffs/sites_compatible_frontend_build_comparison.md

Branch:
codex/sites-compatible-frontend-build

Goal:
Independently review the Sites-compatible frontend preview-shell build against
the contract. Verify exact Worker routing, metadata containment and byte
identity, dependency pins, generated build shape, ordinary local-dev and
launcher preservation, generated-artifact cleanup, and all non-claims.

Do not create or deploy a Sites project, use a Sites connector, run a tunnel,
enable remote bindings, add D1/R2, start the local backend, or perform an
external write. Do not stage, commit, push, open a PR, or target main.

Run:
git status --short --branch --untracked-files=all
node --version
npm --version
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run
npm --prefix frontend run build
node --test frontend/tests/sites-build-shape.test.mjs
py -m pytest -q tests/test_analytics_dev_app_launcher.py
git diff --check
py tools/check_agent_docs.py
py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools/check_secret_patterns.py --base origin/codex/analytics-foundation

Run path-fed protected-surface and secret/private-marker scans over every
changed path. Remove generated dist/.wrangler/coverage/temp output after
review. Record the npm advisory summary as residual risk without broadening
into dependency remediation.

Produce:
docs/contract_test_reports/sites_compatible_frontend_build.md

Lead with findings by severity. If no blocking findings remain, route to
Codex F only as a recommendation; submission and all deployment remain
unauthorized.
```

```yaml
workflow_handoff:
  role_performed: "Codex C: Module Implementer"
  issue: "current owner-authorized local request; no GitHub issue created"
  tracker: ""
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/problem_representations/sites_compatible_frontend_build.md"
  contract_artifact: "docs/contracts/sites_compatible_frontend_build.md"
  implementation_handoff: "docs/implementation_handoffs/sites_compatible_frontend_build_comparison.md"
  review_artifact: "docs/contract_test_reports/sites_compatible_frontend_build.md"
  risk_tier: "High"
  branch: "codex/sites-compatible-frontend-build"
  base_branch: "codex/analytics-foundation"
  implementation_status: "local_preview_shell_build_implemented"
  deployment_authorized: false
  external_writes_authorized: false
  generated_artifacts_kept: false
  remaining_risks:
    - "Actual Sites/Cloudflare runtime and deployment remain unverified and unauthorized."
    - "npm ci reports seven dependency advisories; remediation was outside scope."
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
