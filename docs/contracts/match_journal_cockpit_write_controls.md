# Match Journal Cockpit Write Controls Contract

## Module

Match Journal cockpit write controls and CORS safety boundary.

This contract defines the next local-app slice after the Match Journal status
API bridge and first cockpit UI. It makes the existing browser-facing cockpit
write controls safe enough for routine local development by wiring them to
app-owned local Match Journal state, reporting availability, and preserving the
FastAPI facade as the only browser-facing write path.

Plain English: the cockpit should let the local web app write notes, labels,
review flags, experiment labels, and display-only correction proposals into the
local Match Journal database. It must not let the browser talk directly to the
older broad-CORS status API, and it must not turn human journal notes into
parser truth.

## Source Issue

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/234>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/202>
- Previous child issue: <https://github.com/Tahjali11/Mythic-Edge/issues/232>
- Previous PR: <https://github.com/Tahjali11/Mythic-Edge/pull/233>
- Previous merge commit: `3b839939c09e5546c248b9f1accd209cab9db7be`
- Earlier status API PR: <https://github.com/Tahjali11/Mythic-Edge/pull/231>
- Earlier status API merge commit: `b06ebad875b6b10befc3f14f91d8317c2d198730`

Current branch:

```text
codex/analytics-foundation
```

This work must not target `main`.

## Related Authority

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/contracts/match_journal_local_sqlite_schema.md`
- `docs/contracts/match_journal_repository.md`
- `docs/contracts/match_journal_service.md`
- `docs/contracts/match_journal_status_api.md`
- `docs/contracts/match_journal_cockpit_ui.md`
- `docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md`
- `docs/contract_test_reports/match_journal_cockpit_ui.md`
- `docs/contracts/local_artifact_manifest_environment_profiles.md`

## Risk Tier

High.

Reasons:

- The browser is gaining routine local write access to human-authored Match
  Journal records.
- The repo already contains an older direct status API with wildcard CORS, so
  the browser-facing boundary must remain explicit.
- The slice touches local generated SQLite state and must avoid committing or
  exposing local/private artifacts.
- Human journal entries may be useful to future analytics, UI, or AI surfaces,
  but they must remain annotations, not parser truth.
- Failed writes can cause operator confusion if the UI silently discards
  unsaved human input.

## Owning Layer And Truth Boundary

Primary owning layer: Local App / Match Journal cockpit.

The cockpit write-controls slice owns:

- browser-facing local-app routes under `/api/journal/...`;
- local-app service wiring to the existing Match Journal service and schema;
- app-owned generated Match Journal database path selection;
- setup/status reporting for Match Journal write availability;
- safe local CORS behavior for the FastAPI local app facade;
- UI behavior for successful, unavailable, and failed writes.

It does not own:

- parser event interpretation;
- parser state final reconciliation;
- parser match or game identity;
- parser deduplication;
- analytics fact truth;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- the legacy direct status API CORS policy;
- OpenAI/model-provider behavior;
- AI coaching, Line Tracer, gameplay advice, hidden-card inference, archetype
  truth, or player-mistake truth.

Truth boundaries:

- Parser/state owns parser facts and parser identity.
- Match Journal owns human-authored notes, labels, flags, and display-only
  correction proposals.
- The local app transports user intent to the Match Journal service.
- The browser may display journal data, but it must not rewrite parser facts or
  treat journal data as proof that the parser was wrong.

## Contract Decision

Issue #234 should be treated as an operational hardening and wiring slice for
the existing cockpit controls from issue #232.

Required decisions:

- Keep the FastAPI local app routes as the only browser-facing write path.
- Wire those routes to a production-like app-owned Match Journal service by
  default when the local app is started normally.
- Keep explicit test injection for in-memory Match Journal services.
- Add local setup/status visibility for Match Journal write availability.
- Use an app-owned generated database path under the local app data root.
- Preserve existing request/response shapes from the #232 cockpit UI contract
  unless a small backward-compatible availability field is needed.
- Preserve compact successful write responses. Do not reintroduce full service
  records in `service_result`.
- Preserve safe failure behavior. Failed writes must be visible and must not
  discard unsaved browser form values.
- Do not add pilot-error browser controls in this slice.
- Do not change the direct status API CORS policy in this slice.

Deferred decisions:

- direct status API CORS hardening;
- browser-facing pilot-error write controls;
- destructive or bulk journal actions;
- Match Journal Google Sheets sync;
- analytics ingest of journal rows;
- OpenAI or coaching use of journal notes;
- production deployment behavior.

## Observed Current Behavior

Current branch and issue state:

- The current branch is `codex/analytics-foundation`.
- Issue #234 is open and routes through tracker #202.
- Issue #232 is closed after PR #233 merged the first cockpit UI.
- Issue #203 is closed after PR #231 merged the local HTTP/status API bridge.

Current local app behavior:

- `src/mythic_edge_parser/local_app/backend.py` exposes a FastAPI
  `create_app(...)` factory.
- `create_app(...)` accepts an optional `match_journal_service_factory`.
- If no Match Journal service factory is passed, the journal facade currently
  fails closed as unavailable rather than opening a real local database.
- FastAPI local app CORS is already loopback-restricted through
  `resolve_frontend_origins`.
- `MYTHIC_EDGE_LOCAL_APP_FRONTEND_ORIGIN` accepts only loopback HTTP origins
  with valid ports and no path, query, or fragment.
- The FastAPI journal routes are under `/api/journal/...`.

Current cockpit facade behavior:

- `src/mythic_edge_parser/local_app/match_journal_cockpit.py` owns the
  browser-facing Match Journal response shape.
- The object value is `mythic_edge_local_app_match_journal`.
- The schema version is `match_journal_cockpit_ui.v1`.
- Invalid requests return sanitized errors.
- Missing service wiring returns a `503 service_unavailable` response.
- Successful write responses include compact service-result metadata and do
  not echo full Match Journal records.
- Display correction writes are limited to `journal_display_only`.

Current setup/status behavior:

- `src/mythic_edge_parser/local_app/setup_status.py` reports paths, config,
  Player.log status, analytics database status, migrations, runtime, and
  capabilities.
- `build_capabilities()` currently reports local app capabilities such as
  setup status, manual import, and live watcher status.
- No Match Journal database path or Match Journal write availability appears in
  setup/status.
- Setup/status tests assert that read-only setup/status calls do not create
  app data directories or database files.

Current path behavior:

- `src/mythic_edge_parser/local_app/paths.py` defines local app generated state
  under `%LOCALAPPDATA%\MythicEdgeDev\`.
- Required local app subdirectories are `config`, `db`, `logs`, `imports`,
  `jobs`, and `diagnostics`.
- `LocalAppPaths` currently exposes the analytics database path
  `<app_data>\db\mythic_edge.sqlite3`.
- No app-owned Match Journal database path is defined yet.
- Older Match Journal schema contracts mention a repo-local
  `data/match_journal/mythic_edge_journal.sqlite3` path. For this cockpit
  slice, that repo-local path must be treated as legacy/generated local data,
  not the runtime target for the local app.

Current frontend behavior:

- `frontend/src/api.ts` calls `/api/journal/...` through the FastAPI backend
  API base URL.
- `VITE_MYTHIC_EDGE_API_BASE_URL` is restricted to loopback HTTP origins.
- The cockpit UI renders journal note, opponent label, review flag,
  experiment label, and display-correction proposal controls.
- The cockpit UI does not expose pilot-error controls.
- Frontend tests assert that journal writes use `/api/journal/...` paths and
  do not call direct status API journal endpoints.

Current direct status API behavior:

- `src/mythic_edge_parser/app/status_api.py` includes Match Journal routes.
- Its HTTP responses still use `Access-Control-Allow-Origin: *`.
- The direct status API includes a pilot-error journal route.
- Browser-facing local app code must not use direct status API journal writes.

## Files Owned By Future Implementation

Contract artifact:

- `docs/contracts/match_journal_cockpit_write_controls.md`

Future implementation files authorized by this contract:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/match_journal_cockpit.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `tests/test_match_journal_cockpit_ui_backend.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`, only if path behavior is tested
  there
- `tests/test_analytics_dev_app_launcher.py`, only if launcher/preflight
  availability is tested there
- `frontend/src/api.ts`, only if write failure or availability handling needs a
  narrow client adjustment
- `frontend/src/types.ts`, only if setup/status or journal availability types
  need a backward-compatible optional field
- `frontend/src/App.tsx`, only if failed/unavailable write state needs a narrow
  UI fix
- frontend focused tests for Match Journal cockpit write/unavailable behavior
- `docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md`

Codex C may add a small local-app helper module if it keeps the boundary
clear, for example:

- `src/mythic_edge_parser/local_app/match_journal_runtime.py`

Files and surfaces not owned by this contract:

- `src/mythic_edge_parser/app/status_api.py`, except as read-only context or
  tests proving the browser facade does not depend on it;
- parser modules;
- parser state;
- parser event classes;
- analytics schema and migrations;
- analytics ingest;
- workbook schema;
- webhook transport;
- Apps Script;
- Google Sheets;
- OpenAI/model-provider code;
- raw logs, local JSONL artifacts, generated SQLite files, runtime status
  files, failed posts, workbook exports, secrets, credentials, API keys,
  tokens, webhook URLs, and other local-only artifacts.

If implementation requires changing a non-owned surface, Codex C must stop and
route back to Codex B unless the user explicitly authorizes a new scope.

## Public Interface Requirements

### App-Owned Match Journal Database Path

The local app must define a generated Match Journal database path under the
app-owned local data root:

```text
%LOCALAPPDATA%\MythicEdgeDev\db\match_journal.sqlite3
```

Required symbolic display path:

```text
<app_data>\db\match_journal.sqlite3
```

Rules:

- The local app cockpit must not use a repo-local database path as its normal
  runtime target.
- The path must be represented symbolically in setup/status and logs.
- Raw absolute local paths must not be echoed to the browser.
- The SQLite file and sidecars are generated local artifacts and must never be
  committed.
- The path must not require a new environment variable in this slice.
- Tests must use temporary directories or in-memory services, not the user's
  real app data root.

### Service Wiring

The normal `create_app(...)` path must provide production-like Match Journal
service wiring without requiring tests to inject a service factory.

Required behavior:

- Normal local app startup must be capable of writing Match Journal rows to the
  app-owned database path.
- Explicit test injection through `match_journal_service_factory` must remain
  supported.
- The injected factory must continue to override default app-owned wiring.
- The default wiring must apply the packaged Match Journal schema before the
  first write.
- The default wiring must use the existing `MatchJournalService` and
  repository layer.
- The default wiring must not create or use analytics SQLite tables.
- The default wiring must not read raw Player.log, local JSONL artifacts,
  runtime status payloads, workbook exports, secrets, or environment variable
  values.

Read/write initialization policy:

- Setup/status and route-inventory tests must not create the Match Journal
  database.
- The first explicit journal write may create the app-owned database file and
  apply Match Journal migrations.
- A journal read may either return an empty/unavailable state without creating
  the database, or initialize the database if Codex C proves that the behavior
  is limited to explicit `/api/journal` access and documents it in the
  implementation handoff.
- Codex C must test and document the chosen read behavior.
- Any database creation must be limited to the app-owned generated database
  path or pytest temporary paths.

### Setup And Status Reporting

The local app setup/status response must expose Match Journal write
availability without becoming a setup wizard or cleanup tool.

Required status semantics:

- Add a Match Journal status section or capability entry that can report:
  `ready`, `not_initialized`, `unavailable`, `degraded`, or `error`.
- Report whether the app data root is available.
- Report whether the journal database path is app-owned and safe to use.
- Report whether write controls are enabled, unavailable, or degraded.
- Use symbolic paths only.
- Do not expose local usernames, raw absolute paths, SQLite exception dumps,
  raw SQL, note text, labels, or private payloads.
- Do not create the database, app-data folders, logs, jobs, imports, or
  diagnostics merely to answer setup/status.

Suggested capability name:

```text
match_journal_write_controls
```

The exact response placement is flexible, but Codex C must preserve the
existing setup/status required fields and avoid breaking the frontend setup
status validator.

### Browser-Facing Route Inventory

The first cockpit write-controls slice may use only these browser-facing local
app routes:

```text
GET  /api/journal
POST /api/journal/notes
POST /api/journal/opponent-labels
POST /api/journal/review-flags
POST /api/journal/experiment-label
POST /api/journal/display-corrections
```

Allowed write controls:

- match, game, sideboarding, general, or unattached notes as supported by the
  existing service facade;
- manual opponent archetype and tier labels;
- review flags;
- experiment labels;
- display-only correction proposals with
  `effect_scope = "journal_display_only"`.

Forbidden browser-facing controls in this slice:

- pilot-error yes/no controls;
- pilot-error reason controls;
- delete, purge, archive, truncate, reset, or bulk update controls;
- raw SQL or arbitrary query controls;
- database initialization buttons;
- import controls;
- export/sync controls;
- parser correction controls;
- workbook, webhook, Apps Script, Google Sheets, OpenAI, AI coaching, or Line
  Tracer controls.

### Request Shape

Issue #234 must preserve the request shape established by the cockpit UI slice
unless Codex C identifies a blocking mismatch and routes back to Codex B.

Required shared request fields:

- `context`
- `author_label`
- `source_surface`
- `privacy_label`

Allowed context fields:

- `journal_match_id`
- `journal_game_id`
- `parser_match_id`
- `parser_game_id`
- `game_number`
- `attachment_status`

Rules:

- Parser IDs are references only. The cockpit must not invent parser match IDs
  or parser game IDs.
- Missing context must be allowed for unattached notes where supported by the
  existing service.
- Invalid payloads must fail before service writes.
- Unknown fields must not be silently persisted.
- Error responses must not echo full note text or private labels.

### Response Shape

Successful journal write responses must remain compact.

Required fields:

- `object`
- `schema_version`
- `status`
- `service_result`
- `warnings`, when applicable

`service_result` may include:

- action;
- status;
- primary record type;
- primary record ID;
- record counts.

`service_result` must not include:

- full note text;
- full Match Journal records;
- raw SQLite rows;
- raw exception text;
- raw absolute paths;
- raw Player.log payloads;
- raw JSONL payloads;
- workbook exports;
- secrets, credentials, tokens, API keys, webhook URLs, or spreadsheet IDs.

Failure responses:

- malformed payloads should return client-error responses with safe labels;
- missing or unavailable service state should return a clear unavailable
  response;
- SQLite or repository failures should return sanitized operation-failed
  responses;
- failed writes must not be reported as successful;
- failed writes must not partially persist invalid input.

### Frontend Write Failure Behavior

The cockpit UI must make failed and unavailable writes visible to the user.

Required behavior:

- A failed write must show a safe error or unavailable status.
- A failed write must preserve unsent form values so the operator can retry.
- A successful write may clear only the form that was successfully persisted.
- The UI must not expose raw backend exception text.
- The UI must not offer pilot-error or destructive controls.
- The UI must continue to use the FastAPI `/api/journal/...` facade only.

## CORS And Browser Boundary

FastAPI local app journal routes must remain loopback-only.

Required guarantees:

- No FastAPI local app journal route may use wildcard CORS.
- Allowed browser origins must be loopback HTTP origins only.
- `localhost` and `127.0.0.1` are allowed with valid ports.
- LAN hosts, public hosts, `file://`, raw `*`, empty origins, origins with
  paths, origins with query strings, and origins with fragments must be
  rejected.
- Journal write routes must not be reachable from arbitrary origins through
  local app CORS.
- Frontend code must not call `src/mythic_edge_parser/app/status_api.py`
  journal endpoints directly.

Direct status API decision:

- This contract does not require changing the direct status API wildcard CORS.
- Direct status API CORS hardening is deferred to a separate issue because it
  may affect existing local status clients.
- The browser safety boundary for this slice is achieved by keeping browser
  journal writes behind the FastAPI local app facade.

## Generated Artifact Boundary

Allowed generated artifacts:

- local app Match Journal SQLite database under the app-owned local data root;
- SQLite WAL/SHM/journal sidecars adjacent to that generated database;
- pytest temporary SQLite files in temporary directories;
- local app logs generated only by explicit launcher/start flows.

Forbidden committed artifacts:

- `.sqlite`, `.sqlite3`, `.db`, `.db-wal`, `.db-shm`, `.journal`;
- raw Player.log files or excerpts;
- local JSONL artifacts;
- raw runtime status files;
- failed posts;
- workbook exports;
- generated card data;
- local app logs;
- diagnostics;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, or
  local-only artifacts.

Implementation must verify that no generated/private/local artifacts are
staged or committed.

## Protected Surfaces

Implementation must not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- parser event kind values;
- parser payload shapes;
- match/game identity;
- deduplication;
- analytics schema, migrations, ingest, or deterministic fact storage;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI coaching;
- Line Tracer;
- raw logs;
- generated data;
- runtime status files;
- failed posts;
- workbook exports;
- secrets, credentials, API keys, tokens, webhook URLs, spreadsheet IDs, or
  environment-variable policy.

Human journal data must not become:

- parser truth;
- analytics truth;
- workbook truth;
- merge readiness;
- deploy readiness;
- hidden-card inference;
- archetype classification truth;
- player-mistake truth;
- gameplay advice;
- AI coaching truth.

## Unknowns

- Whether journal reads should initialize the app-owned database or return
  `not_initialized` until the first write.
- Whether the local app should eventually support a dedicated journal database
  initialization route. This contract does not authorize one.
- Whether direct status API CORS should be hardened globally in a future issue.
- Whether pilot-error browser controls should be implemented after separate
  safety review.
- Whether Match Journal rows should later be joined into analytics views or
  Google Sheets exports.
- Whether a manual live-browser smoke test should use the user's real local
  app data root or a disposable temp app-data root. This contract prefers temp
  generated state unless the user explicitly authorizes real local data.

## Suspected Gaps

- Normal `create_app(...)` journal routes are not yet wired to a real
  app-owned Match Journal service.
- No app-owned Match Journal database path exists in `LocalAppPaths`.
- Setup/status does not report Match Journal write readiness.
- Local app preflight does not mention Match Journal write availability.
- Existing backend tests use injected/in-memory services and do not prove
  production-like on-disk wiring.
- Manual live-browser smoke evidence has not been recorded for the cockpit.
- The older direct status API still has wildcard CORS, so browser code must
  continue to avoid it.

## Required Tests For Codex C

Backend and wiring tests should prove:

- `create_app(...)` can service Match Journal write routes without an injected
  service factory when given a temporary app data root or equivalent local app
  path override.
- The first explicit write creates or opens only the app-owned Match Journal
  database path.
- Setup/status and route-inventory checks do not create Match Journal database
  files.
- Injected test service factories still override default wiring.
- Successful writes return compact `service_result` data only.
- Failed service writes return sanitized errors.
- Invalid payloads do not call the service and do not create partial writes.
- Unattached notes remain possible when context is missing or unavailable.
- Display corrections remain `journal_display_only`.
- Pilot-error routes are not exposed through the FastAPI browser facade.
- Frontend-facing journal routes have loopback CORS and no wildcard origin.
- Invalid local app frontend origins are rejected.
- Browser-facing code paths do not call direct status API journal endpoints.

Setup/status tests should prove:

- Match Journal capability/status is reported with symbolic paths only.
- Missing app data root produces unavailable/degraded status without raw paths.
- Missing Match Journal database can be reported without creating it.
- Status output does not expose note text, raw SQL, raw paths, or secrets.

Frontend tests should prove, if frontend code changes:

- Failed writes preserve form input.
- Successful writes may clear only the successfully submitted form.
- Unavailable service state is visible.
- No pilot-error or destructive controls are rendered.
- Journal writes still call only `/api/journal/...`.

Manual or automated smoke evidence:

- Codex C should add a documented live-browser smoke procedure to the
  implementation handoff.
- If feasible, Codex C should run the smoke with a disposable temp app-data
  root, synthetic journal context, and no raw private data.
- If live-browser smoke is not run, the handoff must clearly mark it
  unverified for Codex E or a later manual pass.

## Validation Commands

Focused validation for Codex C:

```powershell
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_match_journal_service.py tests\test_match_journal_repository.py tests\test_match_journal_schema.py
```

Frontend validation if frontend files change:

```powershell
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
npm --prefix frontend run build
```

General validation:

```powershell
py -m ruff check src tests tools
git diff --check
```

Path-scoped protected-surface scan:

```powershell
@'
docs/contracts/match_journal_cockpit_write_controls.md
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/match_journal_cockpit.py
src/mythic_edge_parser/local_app/paths.py
src/mythic_edge_parser/local_app/setup_status.py
tests/test_match_journal_cockpit_ui_backend.py
tests/test_analytics_local_app_backend.py
tests/test_analytics_local_app_config.py
docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Path-scoped secret/private-marker scan:

```powershell
@'
docs/contracts/match_journal_cockpit_write_controls.md
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/match_journal_cockpit.py
src/mythic_edge_parser/local_app/paths.py
src/mythic_edge_parser/local_app/setup_status.py
tests/test_match_journal_cockpit_ui_backend.py
tests/test_analytics_local_app_backend.py
tests/test_analytics_local_app_config.py
docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Generated artifact check:

```powershell
git status --short --branch --untracked-files=all
```

Codex C must report whether any SQLite database, SQLite sidecar, runtime log,
failed post, local app diagnostic, workbook export, raw log, local JSONL,
secret, credential, or generated artifact was created.

## Acceptance Criteria

The contract is implementation-ready when:

- The app-owned local Match Journal database path is explicit.
- The FastAPI facade remains the only browser-facing write path.
- Direct status API CORS hardening is explicitly deferred.
- Pilot-error browser controls are explicitly deferred.
- Existing allowed write controls are named.
- Setup/status readiness requirements are named.
- Write failure and unavailable-state behavior is named.
- Generated/local/private artifact boundaries are explicit.
- Validation and smoke expectations are explicit.
- The next role is Codex C.

Implementation is acceptable only if:

- It does not implement code outside the authorized local-app/UI/test/handoff
  scope.
- It does not change parser behavior, analytics truth, workbook schema,
  webhook payload shape, Apps Script behavior, Google Sheets behavior,
  OpenAI/model-provider behavior, or production behavior.
- It does not expose direct browser writes to the wildcard-CORS status API.
- It does not expose pilot-error controls.
- It does not commit generated/local/private artifacts.
- It preserves human journal data as local annotation data only.

## Expected Codex C Implementation Scope

Codex C should compare current code against this contract, then implement only:

- app-owned Match Journal database path support;
- default local app Match Journal service wiring;
- setup/status Match Journal write availability reporting;
- focused backend and setup/status tests;
- frontend failure/unavailable behavior only if current UI loses user input or
  hides write failures;
- implementation handoff with smoke procedure and verification status.

Codex C should not implement pilot-error controls, direct status API CORS
changes, new journal action families, analytics ingest, Google Sheets sync,
OpenAI behavior, Line Tracer, parser behavior, or production deployment
behavior.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #234.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/234

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Contract:
docs/contracts/match_journal_cockpit_write_controls.md

Context:
- Issue #232 / PR #233 merged the first Match Journal cockpit UI.
- Issue #203 / PR #231 merged the local Match Journal HTTP/status API bridge.
- The current cockpit facade exists, but normal create_app(...) journal routes still need production-like app-owned Match Journal service wiring.
- Direct browser-to-status API writes remain forbidden/deferred.
- Pilot-error browser controls remain deferred.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what the cockpit write controls are supposed to do, what current code already does, what gaps remain, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/match_journal_cockpit_write_controls.md
- docs/contracts/match_journal_cockpit_ui.md
- docs/contracts/match_journal_status_api.md
- docs/contracts/match_journal_service.md
- docs/contracts/match_journal_repository.md
- docs/contracts/match_journal_local_sqlite_schema.md
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/match_journal_cockpit.py
- src/mythic_edge_parser/local_app/paths.py
- src/mythic_edge_parser/local_app/setup_status.py
- src/mythic_edge_parser/app/match_journal_service.py
- src/mythic_edge_parser/app/match_journal_repository.py
- src/mythic_edge_parser/app/status_api.py
- frontend/src/api.ts
- frontend/src/types.ts
- frontend/src/App.tsx
- tests/test_match_journal_cockpit_ui_backend.py
- tests/test_analytics_local_app_backend.py
- tests/test_analytics_local_app_config.py
- frontend focused tests for the Match Journal cockpit

Implement only:
- app-owned Match Journal database path support under the local app data root;
- default FastAPI local app Match Journal service wiring for normal create_app(...) usage;
- setup/status Match Journal write availability reporting with symbolic paths only;
- focused backend/setup/status tests proving safe default wiring, no setup/status DB creation, compact write responses, loopback-only CORS, and no direct status API browser dependency;
- narrow frontend failed/unavailable write handling only if current UI loses input or hides failures;
- docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md.

Do not:
- target main;
- open a PR, stage, commit, or push unless explicitly asked;
- change parser behavior, parser state final reconciliation, parser event classes, parser event kind values, parser payload shapes, match/game identity, deduplication, analytics schema/migrations/ingest/fact truth, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, Line Tracer, or coaching behavior;
- change direct status API CORS policy in this slice;
- expose direct browser writes to src/mythic_edge_parser/app/status_api.py journal endpoints;
- add pilot-error browser controls;
- add destructive, bulk, raw SQL, import, export, sync, cleanup, or database reset controls;
- create or commit raw Player.log files, local JSONL artifacts, generated SQLite databases, WAL/SHM/journal files, runtime logs, failed posts, workbook exports, generated data, secrets, credentials, API keys, tokens, webhook URLs, spreadsheet IDs, or local-only artifacts;
- turn Match Journal notes, labels, review flags, or correction proposals into parser truth, analytics truth, workbook truth, gameplay advice, hidden-card inference, archetype truth, player-mistake truth, Line Tracer truth, or AI/coaching truth.

Validation:
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_match_journal_service.py tests\test_match_journal_repository.py tests\test_match_journal_schema.py
If frontend files change:
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
Run path-scoped protected-surface and secret/private-marker scans over changed files.
Report git status and confirm no generated/private/local artifacts were staged or committed.
Document a live-browser smoke procedure and whether it was run.

Final handoff must include role performed, issue/tracker reviewed, contract used, files changed, exact function/test sections changed, validation run, generated/private artifact status, protected-surface status, secret/private-marker status, live-browser smoke status, remaining risks, next recommended role, and workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/234"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #234"
  target_artifact: "docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md"
  contract_artifact: "docs/contracts/match_journal_cockpit_write_controls.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "Codex B should run git diff --check"
    - "Codex B should run path-scoped protected-surface scan for docs/contracts/match_journal_cockpit_write_controls.md"
    - "Codex B should run path-scoped secret/private-marker scan for docs/contracts/match_journal_cockpit_write_controls.md"
    - "Codex C should run focused backend/setup/status/Match Journal validation"
    - "Codex C should run frontend validation if frontend files change"
    - "Codex C should document live-browser smoke procedure and status"
  stop_conditions:
    - "Do not target main."
    - "Do not change direct status API CORS policy in this slice."
    - "Do not expose direct browser writes to status_api.py journal endpoints."
    - "Do not add pilot-error browser controls."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/analytics truth/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/local artifacts or secrets."
    - "Do not turn Match Journal human annotations into parser truth, analytics truth, workbook truth, gameplay advice, hidden-card inference, archetype truth, player-mistake truth, Line Tracer truth, or AI/coaching truth."
```
