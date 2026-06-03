# Private Local V1 Local App Startup And Status Smoke Contract

## Module

`private_local_v1_local_app_startup_status_smoke`

This contract defines the release-readiness smoke packet for proving that the
Mythic Edge local developer app can start and report status safely for the
`private_local_v1` release profile.

Plain English: this is a proof plan, not a feature request. The next thread
should start the app in a controlled local profile, check the backend and
browser-facing status surfaces, confirm unsafe private data is not exposed, and
write a durable report.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/251
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source baseline issue: https://github.com/Tahjali11/Mythic-Edge/issues/249
- Source framework issue: https://github.com/Tahjali11/Mythic-Edge/issues/248
- Baseline artifact:
  `docs/contract_test_reports/engineering_maturity_baseline.md`

## Branch

Current intended branch:

```text
codex/analytics-foundation
```

This contract must not target `main`.

## Authority And Source Artifacts Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- GitHub issue #251
- GitHub issue #249
- GitHub tracker #136
- `docs/contracts/engineering_maturity_index_open_framework.md`
- `docs/contract_test_reports/engineering_maturity_baseline.md`
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_app_backend_setup_status.md`
- `docs/contracts/analytics_manual_jsonl_import_ui_job_status.md`
- `docs/contracts/live_app_player_log_path_watcher_status.md`
- `docs/contracts/live_app_player_log_watcher_process_control_safeguards.md`
- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`
- `docs/contracts/live_app_watcher_diagnostics.md`
- `docs/contracts/match_journal_live_browser_real_app_data_readiness.md`
- `docs/contracts/match_journal_safe_context_browser_write_smoke.md`
- `tools/dev_app/start_mythic_edge_dev_app.ps1`
- `Start Mythic Edge Dev App.cmd`
- `tools/dev_app/dev_app_launcher.py`
- `tools/check_local_environment.py`
- `docs/local_artifacts_manifest.json`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/status.ts`
- focused local app backend, launcher, and frontend tests

## Risk Tier

High.

Reasons:

- this is release-readiness evidence for the first private local app profile;
- it starts local backend and frontend processes;
- it may create app-owned generated folders, launcher logs, and SQLite files;
- it can expose private local paths, raw Player.log content, local JSONL
  payloads, raw hashes, SQL, stack traces, or secrets if the app boundary is
  wrong;
- it sits near live watcher, manual import, Match Journal, analytics storage,
  and browser action surfaces;
- a misleading pass could unblock `private_local_v1` too early.

## Owning Layer

Primary owning layer: Local App / UI release readiness.

Supporting layers:

- local app backend and launcher;
- React/Vite frontend;
- app-owned generated local state;
- analytics SQLite read-only status/views;
- Match Journal status/readiness;
- live Player.log status and watcher diagnostics.

## Internal Project Area

Local App / UI.

Supporting areas:

- Quality / Governance;
- Generated / Local Artifacts;
- Analytics Foundation;
- Match Journal;
- Live Player.log Mode.

## Truth Owner

This smoke owns readiness evidence only.

Truth ownership remains unchanged:

- Parser/state owns parser-managed match/game/event truth.
- Analytics ingest and SQLite own local deterministic storage of
  parser-normalized facts, not parser truth.
- Match Journal owns human notes and manual labels, not parser truth.
- The local app owns safe orchestration and display only.
- The browser owns display and explicit user actions only.
- AI/model-provider output owns no truth in this contract.

The smoke report must not treat UI text, status payloads, screenshots, local
database rows, or smoke observations as parser truth.

## Bridge-Code Status

`stable_bridge`

Allowed flow:

```text
approved launcher or documented commands
  -> loopback backend and frontend
  -> read-only status/API/browser checks
  -> sanitized readiness report
```

Forbidden reverse flow:

- smoke evidence must not change parser behavior;
- smoke evidence must not rewrite analytics data;
- smoke evidence must not alter Match Journal truth ownership;
- smoke evidence must not enable watcher start/stop, live ingest, workbook
  transport, webhook transport, Apps Script behavior, production behavior, or
  AI/coaching behavior.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/private_local_v1_local_app_startup_status_smoke.md`

Expected later report artifact:

- `docs/contract_test_reports/private_local_v1_local_app_startup_status_smoke.md`

The next thread may inspect or execute current code, but this contract does not
authorize code changes by itself. If the smoke exposes a concrete implementation
gap, route to a scoped Codex C or D follow-up.

## Observed Current Behavior

### Engineering Maturity Baseline

The baseline scored `Local app runtime and usability` as:

- current score: `3`
- target for `private_local_v1`: `4`
- release-profile blocker: `private_local_v1`

Observed baseline rationale:

- the app is beyond prototype;
- backend, frontend, launcher, import, analytics views, Match Journal, live
  status, watcher process, diagnostics, and live SQLite capture contracts/tests
  exist;
- private local v1 still needs a focused startup/status smoke packet proving
  the app starts and explains status in a selected local profile.

### Launcher

Observed launcher surfaces:

- `tools/dev_app/start_mythic_edge_dev_app.ps1` supports `-Check`, `-Start`,
  `-NoOpen`, `-LogToConsole`, `-BackendPort`, `-FrontendPort`, and
  `-AppDataRoot`.
- `tools/dev_app/dev_app_launcher.py` owns preflight, backend/frontend command
  construction, app-data directory creation in start mode, child process
  cleanup, loopback host/port checks, and launcher log redaction.
- The approved backend command is equivalent to:

  ```powershell
  py -m uvicorn mythic_edge_parser.local_app.backend:create_app --factory --host 127.0.0.1 --port 8765
  ```

- The approved frontend command is equivalent to:

  ```powershell
  npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173
  ```

- `Start Mythic Edge Dev App.cmd` is a user-facing root shortcut that routes to
  the PowerShell wrapper.
- Launcher tests assert start mode creates only app subdirectories and
  launcher logs, not analytics or Match Journal SQLite files.

### Backend Status Surfaces

Observed backend route inventory includes:

```text
GET  /api/health
GET  /api/app/setup-status
GET  /api/app/config
GET  /api/app/paths
GET  /api/analytics/database/status
GET  /api/runtime/status
GET  /api/live/player-log/status
GET  /api/live/watcher/status
GET  /api/live/watcher/process
GET  /api/live/watcher/diagnostics
GET  /api/live/ingest/status
GET  /api/analytics/matches
GET  /api/analytics/games
GET  /api/analytics/opening-hands
GET  /api/analytics/mulligans
GET  /api/analytics/gameplay-actions
GET  /api/analytics/opponent-card-observations
GET  /api/analytics/play-draw-splits
GET  /api/analytics/game1-postboard-splits
GET  /api/journal
GET  /api/journal/notes
GET  /api/imports/jobs/{job_id}
POST /api/imports/jsonl
POST /api/imports/jsonl/upload
POST /api/journal/notes
POST /api/journal/opponent-labels
POST /api/journal/review-flags
POST /api/journal/experiment-label
POST /api/journal/display-corrections
```

Observed safety properties:

- CORS is limited to loopback frontend origins.
- Read-only setup/status GET routes do not create local app artifacts.
- Config and path status responses use symbolic display paths such as
  `<app_data>` and `<configured_player_log>`.
- Live Player.log status performs metadata checks only; it does not read
  Player.log contents.
- Live watcher process/status endpoints report safeguards only and keep start,
  stop, parser runner, tailing, external transport, and live SQLite write flags
  disabled.
- Live watcher diagnostics reports privacy and capability booleans proving raw
  log content, raw paths, raw hashes, SQL, stack traces, and environment values
  are excluded.
- Analytics database status reports missing/current/degraded/error status
  without creating the database.

### Frontend Status Surfaces

Observed frontend surfaces and tests cover:

- setup/status rendering;
- backend reachability;
- live Player.log, live watcher, live watcher process, and diagnostics panels;
- manual JSONL import controls;
- read-only analytics history;
- opening hand and mulligan history;
- gameplay action and opponent observation review;
- play/draw and game 1/postboard split review;
- Match Journal cockpit and unattached smoke-note support;
- unsafe display-value redaction;
- absence of destructive controls such as reset/delete/wipe/start/stop where
  the contracts forbid them.

## Contract Decision

Issue #251 should produce a report-only smoke packet. It should not implement
features.

Required smoke outcome:

- prove the local app can pass preflight;
- prove backend and frontend can start through an approved path;
- prove required status/readiness surfaces respond or render safely;
- classify missing local data as degraded-but-acceptable when the app explains
  the state safely;
- fail immediately on unsafe data exposure, destructive controls, unintended
  imports, live watcher start, live tailing, production transport, or generated
  artifact commits.

## Startup And Status Smoke Definition

The smoke has five phases:

1. `preflight`: verify local toolchain, repo markers, app-data root, ports, and
   frontend lockfile without creating app data.
2. `startup`: start backend and frontend through the approved launcher or a
   documented equivalent command pair.
3. `backend_status`: call required loopback backend GET routes and inspect
   sanitized response shapes.
4. `frontend_render`: open the frontend and verify required panels/statuses
   render without unsafe text or forbidden controls.
5. `artifact_safety`: inspect git state and local generated-artifact posture
   before writing the final report.

## Approved Startup Paths

### Required Preflight

The next thread must run the launcher preflight first:

```powershell
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check -AppDataRoot <smoke_app_data_root>
```

Preflight may return degraded or missing app-data subdirectory entries. It must
not create app-data folders in `-Check` mode.

### Preferred Startup

Preferred startup path:

```powershell
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Start -NoOpen -AppDataRoot <smoke_app_data_root>
```

The execution thread must run this in a controlled process/session that can be
stopped cleanly after the smoke. The process lifetime, ports, and cleanup
method must be recorded in the report.

### Documented Command Fallback

If the PowerShell wrapper is unsuitable for automated smoke execution because
it blocks in a way the execution harness cannot manage, the thread may use the
launcher-equivalent commands directly:

```powershell
$env:MYTHIC_EDGE_LOCAL_APP_DATA_ROOT="<smoke_app_data_root>"
$env:MYTHIC_EDGE_LOCAL_APP_FRONTEND_ORIGIN="http://127.0.0.1:<frontend_port>"
py -m uvicorn mythic_edge_parser.local_app.backend:create_app --factory --host 127.0.0.1 --port <backend_port>
```

```powershell
$env:VITE_MYTHIC_EDGE_API_BASE_URL="http://127.0.0.1:<backend_port>"
npm --prefix frontend run dev -- --host 127.0.0.1 --port <frontend_port>
```

Fallback requirements:

- record why the launcher path was not used for startup;
- still run launcher `-Check`;
- use loopback hosts only;
- use non-conflicting ports;
- clean up only processes started by the smoke;
- do not broaden the fallback into a new launcher contract.

The root `Start Mythic Edge Dev App.cmd` may be cited as the manual user-facing
launcher, but automated evidence should prefer the PowerShell wrapper or direct
documented commands above.

## Required Backend Checks

All backend checks must use loopback URLs. The report may show loopback URLs and
ports. It must not show private absolute paths.

| Area | Required route or evidence | Required behavior |
| --- | --- | --- |
| Health | `GET /api/health` | HTTP 200 JSON; `status` is `ok`; capabilities remain non-production and parser-runner control remains disabled. |
| Setup aggregate | `GET /api/app/setup-status` | HTTP 200 JSON with paths, config, player_log, live_player_log, live_watcher, live_watcher_process, live_sqlite_capture, analytics_database, match_journal, migrations, runtime, and capabilities sections. |
| Config | `GET /api/app/config` | Sanitized config status; unexpected/secret-like fields are counted or labeled, not echoed. |
| Paths | `GET /api/app/paths` | App-data and database paths use symbolic display values. |
| Analytics DB | `GET /api/analytics/database/status` | Missing or empty DB is degraded/acceptable if reported safely; invalid DB is fail unless explained as an isolated local artifact outside the repo. |
| Runtime | `GET /api/runtime/status` | Backend may be running; parser runner and live watcher remain deferred/non-controlling. |
| Live Player.log | `GET /api/live/player-log/status` | Metadata-only response; `contents_read = false`; `tailing_started = false`; symbolic display path only. |
| Live watcher | `GET /api/live/watcher/status` | Readiness-only response; running/start/stop/parser/tailing/live-write flags remain false. |
| Watcher process | `GET /api/live/watcher/process` | Safeguards-only response; no start/stop route is enabled. |
| Watcher diagnostics | `GET /api/live/watcher/diagnostics` | Read-only composition; privacy booleans exclude raw content, raw paths, raw hashes, SQL, stack traces, secrets, and environment values. |
| Live SQLite capture | `GET /api/live/ingest/status` | Status-only response; no live writes occur during this smoke. |
| Analytics views | `GET` each `/api/analytics/...` view listed in this contract | `ok`, `empty`, `missing`, or `degraded` is acceptable when safely explained; malformed JSON or raw SQL/stack trace is fail. |
| Match Journal | setup-status `match_journal` section, plus `GET /api/journal` only when a safe existing context is available | No fake parser match/game identity may be created. No journal write is required for this issue. |
| Manual import | setup/status capability plus frontend/manual import reachability | No private path import or browser upload is required. A synthetic missing `GET /api/imports/jobs/<id>` check is optional and must be sanitized if used. |

The backend smoke must not call:

- `POST /api/imports/jsonl`
- `POST /api/imports/jsonl/upload`
- `POST /api/journal/...`
- any live watcher start/stop/restart route
- any endpoint outside loopback local app routes

Exception: if the execution thread explicitly combines #251 with an already
approved write-smoke contract, it must name that contract and keep evidence
separate. By default, #251 is read-only after startup.

## Required Frontend Checks

The frontend smoke must open the local Vite app at:

```text
http://127.0.0.1:<frontend_port>
```

Required visible checks:

- app loads without an unhandled error;
- `Setup Status` is visible;
- backend reachability/status is visible;
- `Live Player.log` is visible;
- `Live Watcher` is visible;
- `Live Watcher Process` is visible;
- `Live Diagnostics` is visible or a sanitized unavailable/degraded message is
  visible;
- manual import surface is visible without executing an import;
- read-only analytics history surfaces are visible or safely empty/degraded:
  - `Analytics History`
  - `Early Game History`
  - `Action Review`
  - `Split Review`
- `Match Journal Cockpit` or a safe Match Journal unavailable/no-context state
  is visible;
- frontend display redacts unsafe values to symbolic labels such as
  `<redacted_path>` when applicable;
- no forbidden browser controls are exposed:
  - reset
  - delete
  - wipe
  - clear database
  - arbitrary SQL
  - start watcher
  - stop watcher
  - restart watcher
  - Sheets/webhook/App Script transport
  - AI/coaching/Line Tracer controls

Refresh controls for read-only views are allowed. Import and Match Journal
write controls may be visible if already authorized by earlier contracts, but
the #251 smoke must not use them unless a separate approved smoke scope is
explicitly invoked.

## Pass, Degraded, And Fail Criteria

### Pass

The smoke may report `pass` when all are true:

- preflight has no blocking missing dependencies;
- backend and frontend start through an approved path;
- required backend GET routes return JSON and required privacy/capability flags;
- frontend renders the required status/readiness surfaces;
- missing Player.log, missing config, missing/empty analytics DB, no import
  jobs, no Match Journal context, stopped watcher, and disabled live capture are
  explained safely;
- no raw/private/generated data appears in responses, UI, logs, screenshots, or
  the committed report;
- git status after the smoke shows no generated/local/private artifacts staged
  or tracked.

### Degraded But Acceptable

The smoke may report `degraded_acceptable` when the app starts and explains one
or more local readiness gaps safely, such as:

- Player.log is missing, stale, unreadable, or not configured;
- app config is missing;
- analytics DB is missing, empty, or schema status is not current;
- Match Journal is not initialized or has no safe context;
- watcher is stopped, blocked, deferred, or not initialized;
- live SQLite capture status is disabled/status-only;
- local environment checker reports warnings that do not involve committed
  private artifacts or unsafe exposure.

Degraded results can still satisfy #251 if the report explains why the degraded
state is acceptable for `private_local_v1` startup/status readiness.

### Fail Or Blocker

The smoke must report `fail` or `blocked` when any are true:

- backend or frontend cannot start through either approved path;
- preflight has a blocking missing dependency and no safe workaround exists;
- a required backend route returns malformed JSON, persistent 500, raw SQL, a
  stack trace, or an unsafe payload;
- frontend cannot render the setup/status page;
- raw Player.log contents, private JSONL payloads, raw hashes, secrets,
  credentials, tokens, API keys, webhook URLs, spreadsheet IDs, environment
  values, generated database contents, retry payloads, stack traces, arbitrary
  SQL, or private local artifacts are exposed;
- a watcher starts, tails Player.log, or writes live facts during the smoke;
- manual import reads a private JSONL file during the smoke;
- workbook, webhook, Apps Script, Sheets, production, OpenAI/model-provider,
  AI/coaching, Line Tracer, hidden-card, archetype, player-mistake, or gameplay
  advice behavior is touched;
- generated app-data, SQLite, WAL/SHM/journal, runtime, launcher log, frontend
  build, local JSONL, raw Player.log, workbook export, or local-only artifacts
  are staged or committed.

## Privacy And Redaction Rules

Allowed in the report:

- loopback URLs, such as `http://127.0.0.1:<port>`;
- symbolic display paths, such as `<app_data>`,
  `<app_data>\db\mythic_edge.sqlite3`, `<configured_player_log>`,
  `<detected_mtga_player_log>`, and `<redacted_path>`;
- endpoint names;
- schema/object names;
- status labels, warning codes, error codes, counts, and booleans;
- sanitized screenshots only when they contain no private paths, payloads,
  secrets, raw hashes, raw SQL, stack traces, or local artifact contents.

Forbidden in the report, UI screenshots, logs included in the report, and issue
comments:

- raw Player.log contents or excerpts;
- raw private JSONL payloads;
- full private absolute paths;
- raw hashes derived from private artifacts;
- generated database row contents unless already parser-normalized and safely
  summarized;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, OAuth
  or environment values;
- stack traces or raw SQL;
- local app generated artifact contents;
- private Match Journal note text, unless it is the explicitly approved
  synthetic smoke marker from a separate write-smoke contract.

## Generated And Local Artifact Rules

The smoke may create local generated state only under the selected app-data
root and only as a consequence of startup or already-authorized status
surfaces.

Allowed local-only artifacts during execution:

- app-data subfolders under the selected app-data root:
  - `config`
  - `db`
  - `logs`
  - `imports`
  - `jobs`
  - `diagnostics`
- launcher logs under `<app_data>\logs\launcher\...`;
- SQLite files created by existing app behavior only when the smoke explicitly
  uses a state-changing route already authorized by another contract;
- frontend development cache/build output if produced by validation commands.

These artifacts must remain out of git. The report must include a git status
check after the smoke and must call out any generated or local-only path that
appears in the worktree.

The #251 smoke should prefer a disposable app-data root for automated proof. If
the thread inspects the actual default app-data root, it must be read-only,
explicitly approved by the user for that thread, and sanitized in the report.

## Evidence Packet Requirements

The later execution thread should produce:

```text
docs/contract_test_reports/private_local_v1_local_app_startup_status_smoke.md
```

Required report fields:

- role performed;
- issue and tracker;
- branch and commit;
- startup mode:
  - launcher preflight;
  - launcher start or documented-command fallback;
  - app-data mode: disposable root or approved actual-root observation;
- commands run, with private paths redacted;
- backend port and frontend port;
- app process cleanup method;
- backend endpoint matrix with status, schema/object, and pass/degraded/fail;
- frontend render matrix with required panels and unsafe-control checks;
- privacy scan summary;
- generated/local artifact summary;
- git status before and after smoke;
- pass/degraded/fail verdict;
- explanation for every degraded item;
- follow-up routing for every fail/blocker;
- explicit statement that forbidden protected surfaces were not touched.

The report must not paste full backend JSON payloads or full browser DOM dumps.
Summaries and selected safe fields are enough.

## Validation Requirements For Later Execution

Minimum recommended validation for the smoke execution thread:

```powershell
git status --short --branch --untracked-files=all
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check -AppDataRoot <smoke_app_data_root>
py tools\check_local_environment.py --profile local_developer_app --app-data-root <smoke_app_data_root>
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_dev_app_launcher.py
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
npm --prefix frontend run build
git status --short --branch --untracked-files=all
git diff --check
py tools\check_agent_docs.py
```

Required live smoke evidence:

- backend and frontend started and stopped cleanly;
- required backend route checks completed;
- browser/frontend render checks completed;
- no forbidden private data exposure observed;
- no generated/private/local artifact committed.

Recommended report validation after the report is written:

```powershell
git diff --check
@'
docs/contracts/private_local_v1_local_app_startup_status_smoke.md
docs/contract_test_reports/private_local_v1_local_app_startup_status_smoke.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/private_local_v1_local_app_startup_status_smoke.md
docs/contract_test_reports/private_local_v1_local_app_startup_status_smoke.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

If `npm --prefix frontend run build` creates `frontend/dist`, the execution
thread must remove that generated output before handoff unless a later contract
explicitly authorizes committing it.

## Stop Conditions And Failure Routing

Stop the smoke immediately and preserve only sanitized evidence when:

- raw/private data appears in a response, UI, log, screenshot, or report draft;
- backend/frontend startup starts live watcher, parser runner, Player.log
  tailing, live SQLite ingest, or external transport unexpectedly;
- a private JSONL import or browser upload starts unexpectedly;
- app-data artifacts appear inside the repo;
- a destructive UI control appears;
- the process cleanup cannot safely stop only the processes started by the
  smoke.

Recommended follow-up routing:

- startup/tooling failure with no code change needed: route to #253 or a
  focused install/readiness issue;
- concrete launcher/backend/frontend bug: route to Codex D or Codex C with a
  focused fix issue;
- unsafe private data exposure: open a high-priority security/local-artifact
  safety issue and do not publish unsafe evidence;
- ambiguous contract expectation: route back to Codex B;
- broader release-readiness uncertainty: route to Codex A.

Suggested failure issue title pattern:

```text
[fix] Private-local-v1 local app startup/status smoke failure: <surface>
```

Suggested unsafe-exposure title pattern:

```text
[security] Local app startup/status smoke exposed private artifact data
```

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema, migrations, or ingest semantics;
- local app/backend/frontend behavior;
- Match Journal truth ownership;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer;
- hidden-card inference;
- archetype inference;
- player-mistake labels;
- gameplay advice;
- CI gates;
- Pyright required/failing behavior;
- secrets, credentials, environment variable contracts, raw logs, generated
  data, runtime status files, failed posts, workbook exports, local JSONL
  artifacts, generated SQLite files, or local-only artifacts.

## Unknowns

- Whether the future smoke executor should use the actual default app-data root
  or stay disposable-root-only for #251. This contract recommends disposable
  root by default and actual-root observation only with explicit user approval.
- Whether #251 alone is enough to raise the local app runtime/usability maturity
  score to `4`, because #253 still owns clean-checkout install and launch path
  proof.
- Whether the current local machine has all frontend/backend dependencies
  installed at execution time.
- Whether local ports `8765` and `5173` are available during execution.

## Suspected Gaps

- The launcher `-Start` command is designed for an interactive long-running
  session; the execution thread may need a careful process harness or direct
  documented-command fallback to collect bounded smoke evidence.
- The report format for private-local-v1 startup smoke does not yet exist.
- Real actual-root readiness remains approval-gated and may stay unverified
  after a disposable-root smoke.
- #253 remains necessary for clean-checkout install/startup proof and should not
  be closed by #251.

## Acceptance Criteria

- Contract artifact exists at
  `docs/contracts/private_local_v1_local_app_startup_status_smoke.md`.
- Smoke objective is defined.
- Approved startup/preflight paths are defined.
- Required backend checks are defined.
- Required frontend checks are defined.
- Pass/degraded/fail criteria are defined.
- Privacy and redaction requirements are defined.
- Generated/local artifact boundaries are defined.
- Evidence packet shape is defined.
- Validation requirements are defined.
- Stop conditions and follow-up routing are defined.
- Parser, analytics, local app, workbook, and AI truth boundaries are preserved.

## Next Workflow Action

Next recommended role: Codex E / Contract-Test Smoke Executor.

Use Codex C only if the smoke executor first identifies a concrete code or test
gap that must be implemented before the smoke can run safely.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Contract-Test Smoke Executor for issue #251.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/251

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_local_app_startup_status_smoke.md

Goal:
Execute the private-local-v1 local app startup/status smoke and produce:
docs/contract_test_reports/private_local_v1_local_app_startup_status_smoke.md

Do not implement code unless the smoke is blocked by a concrete scoped defect and the user explicitly authorizes a Codex C/D fix loop.

Required:
- confirm branch and git status before starting;
- run launcher preflight with a disposable app-data root;
- start backend/frontend through the approved launcher or documented fallback commands;
- verify required backend GET routes;
- verify required frontend status panels/rendering;
- verify no raw/private/generated data exposure;
- verify no generated/local/private artifacts are staged or committed;
- stop only processes started by the smoke;
- classify result as pass, degraded_acceptable, blocked, or fail;
- include follow-up routing for any failure.

Do not start live Player.log watching, import private JSONL files, expose raw Player.log or private artifact data, write to production, change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI behavior, create CI gates, make Pyright required/failing, target main, or close #136.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/251"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue #251 and engineering maturity baseline #249"
  target_artifact: "docs/contract_test_reports/private_local_v1_local_app_startup_status_smoke.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "py tools/check_agent_docs.py"
    - "path-scoped protected-surface scan for contract/report artifacts"
    - "path-scoped secret/private-marker scan for contract/report artifacts"
  stop_conditions:
    - "Do not implement code in the smoke executor unless a scoped fix is explicitly authorized."
    - "Do not start live Player.log watching or import private JSONL files."
    - "Do not expose raw paths, raw Player.log content, private JSONL payloads, raw hashes, secrets, generated database contents, retry payloads, stack traces, arbitrary SQL, or private local artifacts."
    - "Do not commit generated app-data, SQLite, WAL/SHM/journal, runtime, frontend build, local JSONL, raw Player.log, workbook export, or local-only artifacts."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior."
    - "Do not target main or close tracker #136."
```
