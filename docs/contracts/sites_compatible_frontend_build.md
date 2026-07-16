# Sites-Compatible Frontend Build Contract

## Module

Sites-compatible UI preview-shell build for the existing Mythic Edge React/Vite
frontend.

This contract authorizes a local build adaptation only. It does not authorize a
Sites project, packaging archive, hosted version, deployment, backend exposure,
or any external write.

## Source And Authority

- Source problem representation:
  [`docs/problem_representations/sites_compatible_frontend_build.md`](../problem_representations/sites_compatible_frontend_build.md)
- Agent constitution:
  [`docs/agent_constitution.md`](../agent_constitution.md)
- Codex B role:
  [`docs/agent_threads/module_contract.md`](../agent_threads/module_contract.md)
- Contract template:
  [`docs/templates/module_contract.md`](../templates/module_contract.md)
- Internal project map:
  [`docs/internal_project_map.md`](../internal_project_map.md)
- Local app umbrella contract:
  [`docs/contracts/analytics_local_developer_app_shell.md`](analytics_local_developer_app_shell.md)
- Windows launcher contract:
  [`docs/contracts/analytics_windows_developer_launcher_bootstrapper.md`](analytics_windows_developer_launcher_bootstrapper.md)

Related accepted decisions:

- [`ADR-0004: Protected Surfaces And Schema-Change Policy`](../decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md)
- [`ADR-0005: External Integration And Collaboration Surfaces`](../decisions/ADR-0005-external-integration-collaboration-surfaces.md)
- [`ADR-0006: Repository Boundary Strategy`](../decisions/ADR-0006-repository-boundary-strategy.md)

Implementation references, not repo authority:

- [Cloudflare Vite plugin static-assets reference](https://developers.cloudflare.com/workers/vite-plugin/reference/static-assets/)
- [Cloudflare static-assets routing and binding reference](https://developers.cloudflare.com/workers/static-assets/binding/)
- [Cloudflare Vite plugin programmatic-configuration reference](https://developers.cloudflare.com/workers/vite-plugin/reference/programmatic-configuration/)
- Bundled OpenAI Sites starter and packaging helper installed with the local
  Sites plugin. These are compatibility references only and do not grant
  deployment authority.

## Source Issue And Tracker

GitHub issue: not created.

The current user request and the source problem representation are the scoped
authority for this contract-writing pass. Creating an issue would be an
external write and is not authorized here.

Tracker: none. Issue #648 is local-app product context, not cloud or deployment
authority for this slice.

## Branch And Observed State

Contract branch:

```text
codex/analytics-foundation
```

Observed during Codex B on 2026-07-15:

- `HEAD` and `origin/codex/analytics-foundation` both resolve to
  `f24f17cca4b55d51a9e035b1436397f548461801`.
- The source problem representation is untracked.
- `frontend/.openai/hosting.json` is also an untracked pre-existing file and
  contains only `d1: null` and `r2: null`.
- These pre-existing files are preserved. Codex B edits only this contract.
- `frontend/package.json` currently declares Node `>=20`, while its resolved
  Vite `8.0.14` already requires Node `^20.19.0 || >=22.12.0`.
- The local toolchain is Node `24.16.0` and npm `11.13.0`.
- The bundled Sites compatibility reference pins
  `@cloudflare/vite-plugin` `1.37.1` and `wrangler` `4.92.0`; Wrangler requires
  Node `>=22.0.0`.
- The user approved treating a Node update as acceptable. The effective common
  minimum for this build is therefore Node `>=22.12.0`.

The implementation should use a dedicated branch created from the approved
integration branch. Recommended name:

```text
codex/sites-compatible-frontend-build
```

Codex C must preserve unrelated dirty or untracked files and must not target
`main`.

## Risk Tier

High.

The runtime behavior added is narrow, but this touches durable frontend build
dependencies and a deployment-shaped external integration surface. Under
ADR-0004, package, build, and deployment-boundary drift must be explicit and
reviewed. Under ADR-0005, Sites and Cloudflare remain external access/hosting
surfaces rather than project truth or deployment authority. Under ADR-0006,
Local App / UI stays in the primary repo and continues to consume the local
backend contract without creating a new hosted backend boundary.

## Contract Decision

The first implementation is a **Sites-compatible UI preview shell**.

It must:

1. build the existing React application without changing its UI behavior;
2. preserve the ordinary local Vite development and launcher path;
3. use a separate Sites-only Vite configuration during `npm run build`;
4. emit `frontend/dist/server/index.js`;
5. emit `frontend/dist/.openai/hosting.json` as an exact copy of the reviewed
   source metadata;
6. emit static browser assets, including the SPA entry document;
7. route `/api` and `/api/*` to an explicit non-HTML unavailable response;
8. perform no backend proxying, localhost tunneling, external fetch, durable
   storage, deployment, or external write; and
9. leave parser, analytics, schema, transport, backend host, CORS, and local
   launcher behavior unchanged.

Passing this build contract proves only local package-shape compatibility. It
does not prove that a Sites project can be created, that a hosted version can
be saved, that deployment will succeed, or that the local Mythic Edge app is
functional from a hosted origin.

## Owning Layer

Primary owner: Local App / UI.

Supporting owner: Quality / Governance for build-shape validation.

External bridge: Local App / UI -> Sites/Cloudflare hosting compatibility.

## Internal Project Area

`Local App / UI`

## Truth Owner

The existing loopback FastAPI backend and its accepted route contracts remain
the truth owners for local status, controls, parser-owned facts, and
analytics-owned projections.

The frontend remains a display and orchestration consumer. The preview Worker
owns only one deployment-shell fact: the private local backend is unavailable
through this hosted build boundary. It must not synthesize backend responses,
parser facts, analytics rows, journal state, capture state, or setup state.

## Bridge-Code Status

`bridge_code`

- Source area: Local App / UI.
- Consumer surface: external Sites-compatible packaging.
- Allowed flow: committed frontend source -> deterministic local build ->
  generated preview-shell artifacts.
- Forbidden reverse flow: hosted Worker, Sites metadata, or deployment state ->
  local backend, parser, analytics, config, SQLite, launcher, or repo authority.
- Protected surfaces explicitly not changed: parser truth, analytics truth,
  schema, transport, credentials, backend hosts/CORS, production, and external
  resources.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/sites_compatible_frontend_build.md`

Permitted future Codex C implementation scope:

- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/tsconfig.node.json`, only to include the Sites build config or its
  Node-side helper types
- `frontend/tsconfig.sites.json`, new
- `frontend/vite.sites.config.ts`, new
- `frontend/build/sites-vite-plugin.ts`, new
- `frontend/worker/index.ts`, new
- `frontend/worker/index.test.ts`, new
- `frontend/tests/sites-build-shape.test.mjs`, new
- `frontend/.openai/hosting.json`, currently untracked and subject to the exact
  metadata contract below
- `.gitignore`, only for Sites-generated local artifacts
- `docs/implementation_handoffs/sites_compatible_frontend_build_comparison.md`,
  new

Reference-only surfaces that Codex C must not change in this slice:

- `frontend/vite.config.ts`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- `src/mythic_edge_parser/local_app/`
- `tools/dev_app/`
- parser, analytics, migration, workbook, webhook, Apps Script, and transport
  modules

If implementation requires changing a reference-only surface, Codex C must
stop and route the scope conflict to Codex B or Codex A.

## Public Interface

### Local Development And Launcher

The following local command remains semantically unchanged:

```powershell
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173
```

Required preservation:

- the `dev` script remains ordinary Vite using `frontend/vite.config.ts`;
- the Cloudflare plugin is not loaded by the ordinary `dev` script;
- the Windows launcher continues to start the same Vite command and loopback
  URL;
- no tunnel, remote binding, hosted origin, or deployment behavior is added to
  the launcher; and
- local frontend API requests continue to use the existing loopback-only API
  base contract.

The existing `preview` script must not be repurposed as a deployment command.
A Sites-specific preview script is deferred unless Codex C proves it is needed
for the required local tests and keeps it local-only.

### Sites Build

`npm --prefix frontend run build` becomes the deterministic Sites-compatible
build entry point. Its required logical sequence is:

```text
browser typecheck
Sites Worker/build-config typecheck
Vite build using vite.sites.config.ts
hosting metadata copy
build-shape validation
```

The command may be expressed through package scripts, but every invoked script
must be deterministic, non-interactive, local-only, and lockfile-backed.

The build must not call:

- `wrangler deploy`;
- any Sites project/version/deployment API;
- any Cloudflare account API;
- GitHub, Google, OpenAI API, or another external write surface;
- a localhost tunnel;
- a remote binding; or
- the Mythic Edge local backend.

### Worker Interface

The Worker entry has the Cloudflare-compatible shape:

```typescript
interface SitesPreviewAssets {
  fetch(request: Request): Promise<Response>;
}

interface SitesPreviewEnv {
  ASSETS: SitesPreviewAssets;
}

interface SitesPreviewWorker {
  fetch(request: Request, env: SitesPreviewEnv): Promise<Response>;
}
```

The default export must implement this interface without importing frontend API
helpers or Python/backend internals.

## Dependency And Runtime Contract

The effective frontend Node engine becomes:

```json
{
  "node": ">=22.12.0"
}
```

This is a toolchain compatibility correction, not a launcher redesign. Codex C
must not edit launcher or setup behavior merely to enforce it. If the existing
setup/launcher path cannot continue to run after the lockfile update, stop and
route back to Codex B rather than expanding scope.

Sites build dependencies must use exact package.json versions, not caret,
tilde, tag, URL, or workspace ranges:

| Package | Exact version | Reason |
| --- | --- | --- |
| `@cloudflare/vite-plugin` | `1.37.1` | Bundled Sites compatibility reference |
| `wrangler` | `4.92.0` | Exact peer required by the selected plugin line |
| `vite` | `8.0.14` | Existing resolved frontend build version |
| `@vitejs/plugin-react` | `6.0.2` | Existing resolved React/Vite adapter |
| `typescript` | `6.0.3` | Existing resolved typechecker |
| `@types/node` | `22.19.19` | Node-side build helper/config typing reference |

Rules:

- `frontend/package-lock.json` must be regenerated only through npm and must
  preserve exact resolved versions and integrity fields.
- npm remains the package manager.
- `npm ci` remains the reproducible install path.
- No global package installation is allowed.
- No dependency may add a deploy script, postinstall deployment, credential
  lookup, tunnel, telemetry configuration, D1/R2 resource, or remote service.
- Existing React runtime dependencies and application code are not upgraded in
  this slice.
- If npm resolves a different selected version or a peer/engine conflict, stop
  and route back to Codex B. Do not loosen ranges to make installation pass.

## Sites Build Configuration

`frontend/vite.sites.config.ts` is separate from the ordinary
`frontend/vite.config.ts`.

The Sites configuration must use the official Cloudflare Vite plugin and must
bind these semantics:

```text
Worker name: server
Vite environment name: server
Worker entry: ./worker/index.ts
compatibility date: 2026-07-15
asset binding: ASSETS
not_found_handling: single-page-application
run_worker_first: /api and /api/*
remote bindings: false
persistent local Cloudflare state: false
tunnel: false
```

The exact plugin API syntax may follow the selected pinned version, but the
resulting behavior and generated output must match this contract.

The configuration must not declare:

- D1 databases;
- R2 buckets;
- Durable Objects;
- Queues;
- KV namespaces;
- service bindings;
- secrets or vars;
- routes, custom domains, account IDs, project IDs, or deployment IDs;
- remote bindings;
- tunnels; or
- auxiliary Workers.

The Cloudflare Vite plugin may generate build-local Wrangler metadata inside
`frontend/dist/`. Generated metadata is not deployment authority and must not
contain credentials, project IDs, remote resource bindings, or private local
values.

## Hosting Metadata Contract

The committed source metadata is exactly one JSON object with exactly these
keys and values:

```json
{
  "d1": null,
  "r2": null
}
```

Rules:

- `project_id` is absent.
- Unknown keys are forbidden.
- Strings, empty strings, binding names, IDs, URLs, credentials, and
  environment-derived values are forbidden.
- No migration directory is produced because D1 is absent.
- The build copies the source bytes to
  `frontend/dist/.openai/hosting.json`.
- The source and built metadata SHA-256 digests must match.
- Missing, malformed, expanded, or non-matching metadata fails the build-shape
  check.

The metadata-copy helper is build-only. It may replace only the generated
`frontend/dist/.openai/` directory. It must not edit source metadata, another
source file, a user directory, a Sites project, or an external system.

## Routing Contract

### API-Unavailable Route

The API path predicate is exact:

```text
pathname == "/api" OR pathname starts with "/api/"
```

It is case-sensitive. Paths such as `/apiary` are not API paths.

For every HTTP method on an API path, the Worker returns:

- status: `503 Service Unavailable`;
- `Content-Type: application/json; charset=utf-8`;
- `Cache-Control: no-store`;
- `X-Content-Type-Options: nosniff`;
- no CORS allow-origin header;
- no redirect; and
- no call to `env.ASSETS.fetch`, global `fetch`, a backend, or another service.

The canonical JSON object is:

```json
{
  "schema_version": "sites_preview_api_unavailable.v1",
  "object": "mythic_edge_sites_preview_api_unavailable",
  "status": "unavailable",
  "reason": "local_backend_required"
}
```

JSON serialization must use that key order and no extra fields. A `HEAD`
request uses the same status and headers with an empty body.

The response must not include:

- HTML;
- a backend or frontend host;
- a private path;
- raw Player.log, JSONL, SQLite, Match Journal, status, import, capture, log, or
  error-report data;
- a credential, token, environment value, endpoint value, or stack trace;
- a project/deployment identifier; or
- advice to weaken CORS or expose localhost.

### Static And Navigation Routes

All non-API requests are delegated only to the `ASSETS` binding. The Worker
must pass the original request without constructing an external URL.

SPA navigation fallback is owned by the configured static-assets behavior. It
must not be implemented by returning `index.html` for API paths.

If the assets binding is absent or throws, the Worker must return a sanitized
`503` JSON response with reason `preview_assets_unavailable`; it must not echo
the exception, request body, headers, URL query, path, or environment.

## Inputs

Allowed implementation inputs:

- committed frontend source and package metadata;
- the reviewed source metadata object;
- synthetic `Request` objects created by focused tests;
- an in-memory stub `ASSETS.fetch` implementation;
- local Node/npm version output;
- package-lock resolution and integrity metadata;
- local generated `frontend/dist/` output; and
- public Cloudflare plugin documentation and the bundled Sites compatibility
  reference.

Forbidden inputs:

- raw Player.log content;
- private JSONL files or payloads;
- SQLite contents or generated databases;
- Match Journal records;
- runtime logs or status files;
- failed posts or error-report artifacts;
- workbook exports;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs,
  endpoint values, or environment values;
- arbitrary local files or private paths;
- Sites project, account, deployment, or source-write credentials; and
- hosted backend or remote binding data.

## Outputs

Required local generated build shape:

```text
frontend/dist/
  client/
    index.html
    assets/...
  server/
    index.js
    wrangler.json
  .openai/
    hosting.json
```

`wrangler.json` is listed as expected generated plugin metadata, not a new
source-of-truth config. If the pinned plugin emits a different generated
metadata filename while still producing `dist/server/index.js`, Codex C must
record that observed difference; it must not invent or rename generated
metadata merely to satisfy this illustrative tree.

Required durable source outputs from Codex C are limited to the reviewed source
and test files listed in this contract plus the implementation handoff.

Generated output rules:

- `frontend/dist/`, `frontend/node_modules/`, `frontend/.vite/`, and
  `frontend/.wrangler/` are local generated artifacts and must remain ignored.
- `.dev.vars` and `.dev.vars.*` under `frontend/` must remain ignored and must
  not be created by this slice.
- No build archive is created.
- No generated build output is staged or committed.
- No source map, generated config, or build report may contain private/local
  data or credentials.

## Invariants

1. `frontend/vite.config.ts` remains the ordinary local Vite config.
2. `npm run dev` and the Windows launcher remain loopback-local and do not load
   the Sites build path.
3. `frontend/src/api.ts` remains loopback-only and unchanged.
4. `/api` and `/api/*` never receive SPA HTML from the preview Worker.
5. The preview Worker never proxies or invents local backend data.
6. The Worker performs no external network call or persistent write.
7. No Sites project, version, deployment, D1, R2, tunnel, or remote binding is
   created or accessed.
8. `dist/server/index.js` and `dist/.openai/hosting.json` are required build
   artifacts.
9. Source and built hosting metadata are byte-identical.
10. Build dependencies are exact and lockfile-backed.
11. Parser, analytics, schema, migration, workbook, webhook, Apps Script,
    Sheets, transport, OpenAI/AI, and production behavior remain unchanged.
12. A successful local build is not deployment, functional-hosting, security,
    privacy, release, or production readiness evidence.

## Error Behavior

- Unsupported Node or npm: stop before dependency or build work and report the
  version mismatch without changing launcher code.
- Lockfile drift, integrity mismatch, or unexpected package version: fail
  closed; do not use `--force`, `--legacy-peer-deps`, broad ranges, or an
  alternate package manager.
- Missing or invalid source hosting metadata: fail before claiming build-shape
  success.
- Missing `dist/server/index.js`, client `index.html`, or built hosting
  metadata: build-shape failure.
- API route returning HTML, redirecting, reaching assets, or reaching external
  fetch: blocking contract failure.
- Asset binding failure: sanitized `503` with no exception echo.
- Partial build: generated `dist/` may be removed and rebuilt; no source or
  external cleanup is authorized.
- Any required backend host, CORS, environment, launcher, API client, parser,
  analytics, schema, or transport change: stop and route to Codex B/A.
- Any request to create or deploy a Sites project: stop and require a separate
  issue, contract, explicit owner approval, independent review, and deployment
  role.

## Side Effects

Authorized later for Codex C:

- lockfile-backed dependency installation under `frontend/node_modules/`;
- source edits limited to the files owned by this contract;
- local generated build output under `frontend/dist/`;
- ordinary local npm/Vite caches already covered by ignore policy; and
- creation of the implementation handoff document.

Not authorized:

- external writes or runtime network calls; lockfile-backed package-registry
  reads needed for the exact npm dependency install are the only allowed
  network access in this slice;
- Sites or Cloudflare project creation;
- version saving or deployment;
- source-repository push, PR, issue, or comment creation;
- account, credential, permission, sharing, CORS, or environment changes;
- local backend startup as part of the Sites Worker;
- persistent hosted or local application data;
- D1/R2 or other Cloudflare resources;
- parser, analytics, schema, transport, workbook, or production writes.

## Dependency Order

Codex C must implement in this order:

1. Reconcile branch/status and preserve pre-existing untracked files.
2. Add focused Worker routing tests before changing the build script.
3. Add the Worker entry and satisfy routing/no-echo tests.
4. Add and test the exact hosting metadata-copy helper.
5. Add the separate Sites Vite and TypeScript configurations.
6. Pin the build dependencies and Node engine, then update the lockfile.
7. Wire `npm run build` to the Sites configuration without changing `dev`.
8. Add the built-output shape test.
9. Run focused tests, the complete frontend suite/build, launcher regression
   tests, and repository checks.
10. Remove generated `dist/`, `.wrangler/`, coverage, or temporary files before
    reporting status.
11. Produce the implementation handoff and route to independent Codex E.

## Compatibility

Preserved:

- React UI source and behavior;
- `frontend/src/api.ts` endpoint paths, request methods, response validators,
  error mapping, request guards, and loopback-only API-base policy;
- FastAPI route, host, and CORS behavior;
- `npm run dev` and the Windows launcher command path;
- local app setup/status, imports, analytics, Match Journal, live capture, and
  error-report behavior;
- parser and analytics truth ownership; and
- the monorepo boundary from ADR-0006.

Intentional compatibility correction:

- the declared Node minimum becomes `>=22.12.0`, matching the selected build
  toolchain. This machine already satisfies that minimum.

Not preserved because it is not an authorized interface:

- client-only `npm run build` output shape. It is replaced by the contracted
  Sites-compatible build shape.

## Tests Required

### Worker Routing Tests

Focused Vitest coverage must prove:

- `/api` and representative `/api/*` GET requests return exact `503` JSON;
- POST, OPTIONS, and HEAD API requests remain unavailable and side-effect free;
- API responses have the required headers and never call the assets binding;
- `/apiary` is not classified as an API route;
- navigation and static-asset requests call only the stub assets binding;
- asset binding absence/rejection becomes sanitized
  `preview_assets_unavailable` without raw exception text;
- repeated requests are deterministic and create no mutable state; and
- bodies, query strings, private labels, and arbitrary headers are never echoed.

### Metadata And Build-Shape Tests

Focused tests must prove:

- source hosting metadata has exactly `d1` and `r2`, both `null`;
- missing, malformed, expanded, or non-null metadata fails;
- built metadata bytes and digest equal the source metadata;
- `dist/server/index.js` exists and is importable as ESM;
- the client SPA entry and emitted assets exist;
- importing the built Worker and invoking an API route produces the same exact
  unavailable contract;
- API output is not HTML;
- no `.openai/drizzle` output exists;
- no D1/R2/remote/tunnel/project/deployment binding appears in generated
  build metadata; and
- build output is ignored and absent from the Git diff.

### Regression And Repository Validation

Codex C must run:

```powershell
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
```

Codex C must also run path-scoped protected-surface and secret/private-marker
scans over every changed source, config, test, contract, and handoff path.

If the repository-wide scans report pre-existing findings, Codex C must report
them separately and prove the changed-path scan is clean. It must not broaden
this slice into unrelated remediation.

Codex C must not run a deploy command, Sites connector, package-site archive
helper, tunnel, remote binding, or live backend exposure test.

## Acceptance Criteria

- The ordinary local Vite config and launcher paths are unchanged.
- The selected Node and build dependencies are exact and lockfile-backed.
- `npm run build` succeeds from a clean lockfile install.
- `frontend/dist/server/index.js` exists.
- `frontend/dist/.openai/hosting.json` exists and exactly matches the reviewed
  source metadata.
- The SPA client entry and assets exist.
- `/api` and `/api/*` always return the exact non-HTML unavailable response.
- Non-API navigation uses the local assets binding and SPA fallback.
- No backend host, CORS, API client, parser, analytics, schema, transport,
  workbook, Apps Script, AI, or production behavior changes.
- No project ID, credential, environment value, D1/R2 resource, tunnel, remote
  binding, deployment, packaging archive, or external write is introduced.
- Focused routing/build-shape tests and the existing frontend/launcher tests
  pass.
- Generated build and tool artifacts remain ignored and uncommitted.
- The implementation handoff states that this is a package-compatible preview
  shell only and makes no deployment or hosted-functionality claim.

## Rollback Plan

Rollback is source-only and behavior-preserving:

1. restore the prior `frontend/package.json` and lockfile;
2. remove only the Sites-specific source/config/test files introduced by this
   slice;
3. retain the unchanged ordinary `frontend/vite.config.ts` and launcher files;
4. remove generated `frontend/dist/`, `frontend/.wrangler/`, and temporary test
   output; and
5. rerun the prior frontend typecheck, tests, and client-only build command if
   rollback is exercised.

Rollback must not delete user data, local app data, SQLite files, logs, imports,
journal records, config, credentials, or another worktree's files.

## Protected-Surface Assessment

Protected categories touched later by implementation:

- frontend build/package dependency surface;
- Local App / UI bridge code;
- external integration/hosting compatibility;
- deployment-shaped build output; and
- ignored/generated artifact policy.

Protected categories not authorized or changed:

- parser behavior or parser state final reconciliation;
- parser event classes, payloads, match/game identity, or deduplication;
- analytics behavior, SQLite schema, migrations, or ingest truth;
- backend route shapes, host binding, or CORS;
- frontend API paths, payloads, validators, or request guards;
- Match Journal, live capture, imports, or error-report behavior;
- workbook schema, webhook payloads, Apps Script, Sheets, or output transport;
- secrets, credentials, environment contracts, or external permissions;
- OpenAI/model-provider runtime, AI/coaching, or Line Tracer behavior;
- CI, release, deployment, or production behavior; and
- raw/private/generated/local artifact content.

ADR-0004 requires issue/contract/review/validation agreement before deployment
behavior can change. This contract stops before deployment. ADR-0005 keeps
Sites an external hosting surface without repo or truth authority. ADR-0006
keeps the UI and orchestration boundary in this repository and forbids a hosted
shell from reaching backward into parser or analytics truth.

## Non-Claims

This contract and any passing implementation must not claim:

- a Sites project exists;
- deployment, release, production, or public readiness;
- hosted backend compatibility;
- local/private data accessibility from a hosted origin;
- parser or analytics correctness;
- security or privacy assurance;
- CORS or network readiness;
- D1/R2 readiness;
- remote control of live capture, imports, Match Journal, or error reports; or
- permission to package, publish, save, deploy, share, or expose the build.

## Open Risks And Stop Conditions

- Exact Cloudflare plugin behavior is pinned but still must be proven by the
  focused built-output tests.
- Raising the Node minimum is acceptable for this toolchain, but any required
  setup/launcher code change is outside this contract.
- The source problem representation and hosting metadata are currently
  untracked. Codex C must preserve and explicitly account for their lifecycle;
  Codex F must not stage either unless independent review includes them.
- No GitHub issue or deployment tracker exists. Contract completion may route
  to local implementation and review, but external submission or deployment
  requires separate explicit authority.
- If output cannot be made `dist/server/index.js` without replacing Vite,
  converting frameworks, or changing local dev behavior, stop and route to
  Codex B/A.
- If the hosted shell would need real data, synthetic demo data, auth,
  persistence, CORS expansion, backend proxying, or localhost tunneling, create
  a separate problem representation and contract.

## Next Workflow Action

Next role: Codex C, Module Implementer.

Readiness for Codex C means the implementation boundary is defined. It does
not start or independently authorize Codex C; implementation begins only when
the owner explicitly invokes that role on the approved branch.

Expected implementation handoff:

```text
docs/implementation_handoffs/sites_compatible_frontend_build_comparison.md
```

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer.

Source problem representation:
docs/problem_representations/sites_compatible_frontend_build.md

Contract:
docs/contracts/sites_compatible_frontend_build.md

Base branch:
codex/analytics-foundation

Recommended implementation branch:
codex/sites-compatible-frontend-build

Goal:
Implement the narrow Sites-compatible UI preview-shell build exactly as
contracted. Preserve the existing local Vite development and Windows launcher
path. Produce frontend/dist/server/index.js and
frontend/dist/.openai/hosting.json, and make /api plus /api/* return the exact
non-HTML local-backend-unavailable response.

Before editing:
- Confirm branch, HEAD, and full git status.
- Preserve the pre-existing untracked problem representation and
  frontend/.openai metadata.
- Compare package, Vite, TypeScript, launcher, API-base, ignore, and current
  frontend test surfaces against the contract.
- Write docs/implementation_handoffs/sites_compatible_frontend_build_comparison.md.

Implement only:
- the exact pinned Node/build dependency and lockfile changes;
- a separate Sites-only Vite/TypeScript configuration;
- the minimal no-persistence Worker entry;
- exact hosting metadata staging;
- focused Worker-routing and build-shape tests;
- generated artifact ignore rules; and
- the implementation handoff.

Do not:
- change frontend/vite.config.ts, frontend/src/api.ts, App behavior, backend
  routes, backend hosts, CORS, launcher behavior, parser behavior, analytics,
  schema, migrations, workbook/webhook/Apps Script/Sheets, transport,
  OpenAI/AI/coaching, CI, deployment, or production behavior;
- create or deploy a Sites project;
- run wrangler deploy, a tunnel, a remote binding, a Sites connector, or an
  external write;
- add D1, R2, hosted persistence, auth, environment values, credentials, or a
  backend proxy;
- read or expose raw Player.log, JSONL, SQLite, Match Journal, runtime, import,
  capture, log, failed-post, workbook, secret, or local-only data;
- create a package archive;
- stage, commit, push, open a PR, or target main.

Validation:
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

Run path-scoped protected-surface and secret/private-marker scans for every
changed path. Remove generated dist/.wrangler/coverage/temp artifacts before
final status inspection.

Final output:
- intended versus actual behavior;
- first proven failure point;
- exact implementation;
- files changed;
- dependency and Node decisions;
- local dev/launcher preservation evidence;
- Worker routing evidence;
- build-shape evidence;
- validation results;
- protected-surface and private-marker results;
- remaining risks and non-claims;
- next recommended role: Codex E;
- pasteable Codex E prompt; and
- workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex B: Module Contract Writer"
  issue: "current user request; GitHub issue not yet created"
  tracker: ""
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/problem_representations/sites_compatible_frontend_build.md"
  contract_artifact: "docs/contracts/sites_compatible_frontend_build.md"
  target_artifact: "docs/implementation_handoffs/sites_compatible_frontend_build_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  recommended_implementation_branch: "codex/sites-compatible-frontend-build"
  internal_project_area: "Local App / UI"
  truth_owner: "existing loopback backend API and accepted frontend contracts"
  bridge_code_status: "bridge_code"
  related_adrs:
    - "ADR-0004"
    - "ADR-0005"
    - "ADR-0006"
  ready_for_codex_c: true
  implementation_authorized: false
  deployment_authorized: false
  external_writes_authorized: false
  validation:
    - "git diff --check"
    - "py tools/check_agent_docs.py"
    - "path-scoped protected-surface scan"
    - "path-scoped secret/private-marker scan"
  stop_conditions:
    - "Do not create, package, save, or deploy a Sites project or version."
    - "Do not change ordinary Vite dev, launcher, backend host/CORS, or API-base behavior."
    - "Do not proxy or expose local/private data or controls."
    - "Do not add D1, R2, auth, credentials, environment values, tunnels, or remote bindings."
    - "Do not change parser, analytics, schema, migration, workbook, webhook, Apps Script, Sheets, transport, AI, CI, deployment, or production behavior."
    - "Route any scope expansion, dependency mismatch, or ADR conflict back to Codex B/A."
```
