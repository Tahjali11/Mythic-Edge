# Sites-Compatible Frontend Build

## Summary

The existing React/Vite frontend builds only browser assets, while OpenAI Sites
packaging requires a Cloudflare Worker-compatible server entry at
`frontend/dist/server/index.js` plus copied Sites metadata. Adapt the existing
frontend build without replacing the local-first application architecture or
claiming that the hosted shell can use the private local backend.

This problem representation is governed by:

- [`docs/agent_constitution.md`](../agent_constitution.md)
- [`docs/agent_threads/problem_representation.md`](../agent_threads/problem_representation.md)
- [`docs/templates/problem_representation.md`](../templates/problem_representation.md)
- [`docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`](../decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md)
- [`docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`](../decisions/ADR-0005-external-integration-collaboration-surfaces.md)
- [`docs/decisions/ADR-0006-repository-boundary-strategy.md`](../decisions/ADR-0006-repository-boundary-strategy.md)

## Source Request Or Issue

Current user request: make the existing Vite frontend emit the server output
required by Sites.

GitHub issue: not created. Creating an issue is a live external write and
requires explicit user approval.

## Tracker

No deployment tracker currently authorizes this work. Issue #648 is related
local-app product context, but it explicitly excludes cloud and production
deployment behavior and therefore is not implementation authority for this
change.

## What The Code Is Supposed To Do

`frontend/npm run build` should:

- preserve the existing React single-page application;
- type-check the browser and Worker source;
- emit browser assets;
- emit a Cloudflare Worker-compatible ESM entry at
  `frontend/dist/server/index.js`;
- copy `frontend/.openai/hosting.json` to
  `frontend/dist/.openai/hosting.json`;
- preserve the current local launcher and `npm run dev` behavior; and
- produce a package that passes the local Sites packaging shape check.

The first adaptation should make the UI shell package-compatible only. It must
not publish a site, create hosted resources, expose local data, or claim that
the complete Mythic Edge application is functional when hosted.

## What It Is Actually Doing

Observed on 2026-07-15:

```text
npm run build -> passed
dist/index.html
dist/assets/index-ByoKOreJ.css
dist/assets/index-kY-RhArW.js
```

The build does not produce:

```text
dist/server/index.js
dist/.openai/hosting.json
```

The Sites packaging helper therefore stops with
`Missing dist/server/index.js`.

There is a second, separate compatibility boundary: the browser API client
uses same-origin `/api/...` requests when no API base is provided and otherwise
accepts only an HTTP loopback origin. The FastAPI backend and local
configuration likewise permit only local frontend origins. A hosted shell
therefore has no authorized hosted API and must report backend unavailability
rather than silently treating an `/api/...` request as a single-page-app route.

## Why This Matters

Without the Worker entry and packaged metadata, Sites cannot validate or save
the build. Without an explicit API boundary, a technically deployable UI shell
could be mistaken for a fully working hosted Mythic Edge application or could
encourage unsafe exposure of private local data.

## Project Layer

- Primary layer: Local App / UI
- Supporting layer: repository build and deployment coordination
- External surface: OpenAI Sites / Cloudflare-compatible hosting

Sites is an access and hosting surface. It does not own frontend behavior,
backend truth, privacy policy, or deployment readiness.

## Internal Project Area

- Primary area: Local App / UI
- Bridge: Local App / UI -> External / Collaboration Surface
- Bridge status: `bridge_code`
- Truth owner: the existing local backend remains the owner of its API output;
  the hosted Worker must not invent or replace those responses

## First Bad Value

The first proven failure point is the build interface:

1. `frontend/package.json` runs `tsc --noEmit && vite build`.
2. `frontend/vite.config.ts` configures only the React client build.
3. Vite therefore emits a client-only `dist/` tree.
4. The Sites packaging contract requires `dist/server/index.js` and packaged
   hosting metadata, so packaging cannot begin.

The next boundary is functional rather than structural:

1. `frontend/src/api.ts` defaults to same-origin `/api/...` requests.
2. Configured API bases are restricted to local loopback HTTP origins.
3. `src/mythic_edge_parser/local_app/backend.py` permits local frontend
   origins by default.
4. No current contract authorizes a hosted backend, proxy, CORS expansion, or
   private local-data bridge.

## Inputs

- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/vite.config.ts`
- `frontend/tsconfig.json`
- `frontend/tsconfig.node.json`
- `frontend/.openai/hosting.json`
- `frontend/src/api.ts`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/config.py`
- OpenAI Sites requirement for `dist/server/index.js`
- Cloudflare Vite SPA and Worker build conventions

## Expected Output

The implementation contract should define a narrow, two-part build:

1. Keep the ordinary local Vite development server unchanged.
2. Make `npm run build` use a Sites-specific Vite configuration that:
   - uses the official Cloudflare Vite plugin;
   - names the entry Worker `server`, yielding
     `dist/server/index.js`;
   - emits browser assets under the build's client output;
   - uses single-page-application asset fallback for navigation routes;
   - routes `/api/*` to a minimal Worker response that clearly reports that the
     local backend is unavailable, rather than returning `index.html`;
   - reuses the Sites template's metadata-copy plugin to create
     `dist/.openai/hosting.json`; and
   - declares no D1 or R2 resources.

The first build must be described as a **Sites-compatible UI preview shell**,
not as a hosted replacement for the local Mythic Edge application.

## Scope

In scope:

- Sites-compatible frontend build output;
- a minimal Cloudflare Worker entry with no persistence or external calls;
- explicit SPA versus `/api/*` routing;
- Sites metadata staging;
- focused build-shape and Worker-routing tests;
- preservation of existing local development and launcher behavior.

Out of scope:

- creating a Sites project or `project_id`;
- saving or deploying a Sites version;
- public, shared, private, staging, or production deployment;
- credentials, secrets, OAuth, or environment-contract changes;
- D1, R2, hosted analytics, or remote persistence;
- deploying or proxying the FastAPI backend;
- expanding backend hosts or CORS origins;
- tunneling into localhost or exposing local files, logs, SQLite data, imports,
  journal writes, capture controls, or error-report submission;
- parser, analytics, schema, transport, Apps Script, or truth-ownership changes;
- converting the application to Next.js or vinext;
- splitting the frontend into another repository.

## Risks And Likely Breakpoints

- Deployment behavior is a high-risk protected surface under current repo
  governance, even when the immediate edit is only local build configuration.
- Adding the Cloudflare plugin to the ordinary dev path could change launcher
  startup behavior; the Sites build configuration should therefore remain
  separate from the local dev configuration.
- SPA fallback can incorrectly turn `/api/*` failures into `200 index.html`
  responses unless API routing is explicit.
- A passing package-shape check does not prove a functional hosted product.
- Dependency versions must be pinned and reviewed because they become durable
  build infrastructure.
- Generated `.wrangler`, `.dev.vars*`, `dist/`, archives, credentials, and
  deployment IDs must remain uncommitted.
- The current branch contains the untracked `frontend/.openai/` addition; later
  submitter work must stage only reviewed files.

## Validation Evidence Needed

```powershell
Set-Location frontend
npm test -- --run
npm run build
Test-Path dist/server/index.js
Test-Path dist/.openai/hosting.json
node --test <focused-built-worker-test>
git diff --check
py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools/check_secret_patterns.py --all
```

Required behavioral evidence:

- existing frontend tests still pass;
- `npm run dev` remains compatible with the current launcher contract;
- a navigation request can receive the SPA shell;
- `/api/*` receives a non-HTML unavailable response when no hosted API exists;
- the required Sites files exist in `dist/`;
- no project, deployment, hosted resource, credential, or external data write
  occurs.

## Open Questions

- Should the first hosted artifact remain a UI-only preview shell, or should a
  later issue define a synthetic-data demo? The safe default for this issue is
  the UI-only shell.
- Which exact Cloudflare plugin and Wrangler versions should the contract pin?
  The bundled Sites starter versions should be the initial compatibility
  reference, with dependency review before implementation.
- Which approved integration branch should receive the eventual draft PR? The
  current checkout is `codex/analytics-foundation`, but no issue currently
  records the target.
- A functional hosted Mythic Edge product would require a separate problem
  representation covering backend placement, privacy, authorization, local
  controls, data retention, failure recovery, and rollback.

## Next Workflow Action

Next role: Codex B, Module Contract Writer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex B: Module Contract Writer
for docs/problem_representations/sites_compatible_frontend_build.md. Define the
narrow contract for a Sites-compatible UI preview-shell build that preserves
the existing local Vite development and launcher path. Require
dist/server/index.js, dist/.openai/hosting.json, explicit non-HTML /api/*
unavailable behavior, pinned build dependencies, focused routing/build-shape
tests, and zero deployment or external writes. Do not implement code, create a
Sites project, deploy, change CORS/backend hosts, expose local data, add D1/R2,
or change parser/analytics/schema/transport behavior. Cite ADR-0004, ADR-0005,
and ADR-0006, and produce docs/contracts/sites_compatible_frontend_build.md
plus a handoff to Codex C.
```

```yaml
workflow_handoff:
  issue: "current user request; GitHub issue not yet created"
  tracker: ""
  completed_thread: "A"
  next_thread: "B"
  source_artifact: "docs/problem_representations/sites_compatible_frontend_build.md"
  target_artifact: "docs/contracts/sites_compatible_frontend_build.md"
  risk_tier: "high"
  branch: "codex/analytics-foundation; dedicated implementation branch pending"
  internal_project_area: "Local App / UI"
  truth_owner: "existing local backend API and frontend contracts"
  bridge_code_status: "bridge_code"
  validation:
    - "npm run build currently passes but omits dist/server/index.js"
    - "dist/.openai/hosting.json is currently missing"
    - "frontend API and backend origin contracts are local-only"
  stop_conditions:
    - "Do not implement without the module contract."
    - "Do not create or deploy a Sites project."
    - "Do not change backend host, CORS, credentials, or environment contracts."
    - "Do not expose local logs, SQLite data, imports, journal data, or controls."
    - "Route scope expansion or an ADR conflict back to Codex A."
```
