# Match Journal Live-Browser And Real App-Data Readiness Contract

## Module

Match Journal live-browser smoke and real app-data readiness.

This contract defines how Mythic Edge should prove that the existing Match
Journal cockpit works through the real local developer app path and app-owned
generated state, without turning the smoke into cleanup tooling, parser
behavior changes, production behavior, direct status API CORS redesign, or
broader cockpit/overlay expansion.

Plain English: this is the proof plan. The cockpit has write controls and tests
now; this contract says how a later thread may safely launch the local app,
use the browser, submit one clearly labeled journal update, refresh, and prove
the update persisted without touching private/generated data unsafely.

## Source Issue

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/236>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/202>
- Completed prerequisite: issue #203 / PR #231, Match Journal local HTTP/status
  API bridge, merge commit `b06ebad875b6b10befc3f14f91d8317c2d198730`
- Completed prerequisite: issue #232 / PR #233, Match Journal cockpit UI and
  browser API safety boundary, merge commit
  `3b839939c09e5546c248b9f1accd209cab9db7be`
- Completed prerequisite: issue #234 / PR #235, Match Journal cockpit write
  controls and CORS safety boundary, merge commit
  `7929ae131d1fbc919f46a91e226033dcc5a068a9`

## Related Authority

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- `docs/project_roadmap.md`
- `docs/contracts/match_journal_status_api.md`
- `docs/contracts/match_journal_cockpit_ui.md`
- `docs/contracts/match_journal_cockpit_write_controls.md`
- `docs/contracts/local_artifact_manifest_environment_profiles.md`
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_app_backend_setup_status.md`

## Risk Tier

High.

Reasons:

- The smoke may launch a local browser-facing app and write human-authored
  Match Journal rows.
- The smoke may create generated app-owned SQLite state.
- The actual app-data root may already contain the user's journal data.
- The cockpit sits near parser, analytics, UI, local artifact, and status API
  boundaries.
- A failed or ambiguous smoke can hide data loss, direct status API leakage, or
  generated-artifact drift.

## Owning Layer

Primary owning layer: Local App / UI.

Supporting layers:

- Match Journal service and repository;
- app-owned generated state under the local app data root;
- developer launcher;
- FastAPI local backend;
- React/Vite frontend;
- Quality / Governance validation tooling.

The smoke is evidence about local app readiness. It does not make the local app
or browser a truth owner for parser facts, analytics facts, workbook rows,
deployment state, or AI/coaching output.

## Internal Project Area

Local App / UI.

Supporting areas:

- Generated / Local Artifacts
- Quality / Governance
- Match Journal human-annotation service boundary

## Truth Owner

- Parser/state owns parser match/game facts, parser event interpretation,
  match/game identity, and final reconciliation.
- Analytics owns local deterministic storage and views over parser-normalized
  facts.
- Match Journal owns human notes, manual labels, review flags, experiment
  labels, and display-only correction proposals.
- The FastAPI backend owns local request validation, safe service dispatch, and
  browser-safe response envelopes.
- The frontend owns display, form state, and explicit user submissions.
- This contract owns only readiness evidence and smoke-test boundaries.

## Bridge-Code Status

`stable_bridge`

Bridge from:

- Browser UI
- FastAPI local app facade
- Match Journal service/repository
- app-owned generated state

Bridge to:

- Human/Codex readiness evidence
- implementation handoff and review report

Forbidden reverse flow:

- Smoke evidence must not rewrite parser facts, analytics facts, workbook rows,
  webhook payloads, Apps Script behavior, Google Sheets state, production
  behavior, AI/model-provider output, or credential policy.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/match_journal_live_browser_real_app_data_readiness.md`

Future Codex C implementation/comparison artifact:

- `docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md`

Future Codex E review artifact:

- `docs/contract_test_reports/match_journal_live_browser_real_app_data_readiness.md`

Future implementation files Codex C may change only if the comparison proves a
readiness gap inside this contract:

- `tools/dev_app/dev_app_launcher.py`
- `tools/dev_app/start_mythic_edge_dev_app.ps1`
- `Start Mythic Edge Dev App.cmd`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/match_journal_cockpit.py`
- `src/mythic_edge_parser/local_app/match_journal_runtime.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `tests/test_match_journal_cockpit_ui_backend.py`
- `tests/test_analytics_dev_app_launcher.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`

Preferred first Codex C outcome:

- comparison/readiness handoff only, if current code and tests already satisfy
  the automated readiness requirements and the remaining gap is a manual
  smoke run;
- docs/test-only improvement, if the smoke procedure or proof harness is
  missing;
- narrow implementation only if the launcher, setup/status, or cockpit cannot
  safely support the approved smoke.

Not owned by this contract:

- parser modules;
- parser runtime behavior;
- analytics schema, migrations, ingest, or deterministic views;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- direct status API global CORS policy;
- OpenAI/model-provider runtime behavior;
- production behavior;
- generated/private/local artifacts.

## Observed Current Behavior

Observed from the current branch and prerequisite artifacts:

- The branch is `codex/analytics-foundation`.
- Issue #236 is open and still routes through tracker #202.
- Tracker #202 remains open and must not be marked complete by this contract.
- The local app backend exposes FastAPI routes under `/api/...`.
- Browser-facing Match Journal routes are:
  - `GET /api/journal`
  - `POST /api/journal/notes`
  - `POST /api/journal/opponent-labels`
  - `POST /api/journal/review-flags`
  - `POST /api/journal/experiment-label`
  - `POST /api/journal/display-corrections`
- The FastAPI local app keeps browser journal writes behind `/api/journal/...`;
  the browser is not supposed to call `status_api.py` journal routes directly.
- The direct status API remains a separate reference surface and its global
  CORS hardening remains deferred.
- `LocalAppPaths.match_journal_database` points to
  `<app_data>\db\match_journal.sqlite3`.
- `build_match_journal_write_status(...)` reports symbolic app-data paths and
  can report `not_initialized`, `ready`, `degraded`, `unavailable`, or `error`
  without exposing raw local paths.
- Journal reads and setup/status calls are tested not to create app-data
  folders or SQLite files.
- First explicit journal writes are tested to create only the app-owned Match
  Journal database under a temporary app-data root.
- The developer launcher can run a preflight check and start backend/frontend
  child processes with loopback hosts and redacted logs.
- Frontend tests cover cockpit rendering, absence of destructive and
  pilot-error controls, safe unavailable states, allowed `/api/journal/...`
  submissions, failed-submit input preservation, and setup/status display of
  `<app_data>\db\match_journal.sqlite3`.

Remaining unverified from issue #234 / PR #235:

- Manual live-browser retry flow.
- Real local app operation against the user's actual app-data root.
- Future cockpit/overlay clients.
- Direct status API global CORS hardening.

## Contract Decisions

### Disposable App-Data Smoke Is The Required Safe Baseline

The first live-browser smoke should use a disposable app-data root supplied to
the approved launcher/dev-app command.

The disposable-root smoke is the minimum required readiness proof because it:

- avoids modifying the user's existing app-data root;
- can be repeated without cleanup of real journal state;
- can create generated SQLite state only under a temporary location;
- can verify launcher, backend, frontend, setup/status, cockpit, and
  persistence behavior through the real local app path.

The disposable smoke may create app-owned generated state under the disposable
root. It must not create or stage generated files inside the repo.

### Actual App-Data Root Is Approval-Gated And Not Mandatory For First Closure

The user's actual app-data root may contain real journal data. Codex C or E
must not inspect, write, reset, clean, delete, move, rename, archive, or
sanitize actual app-data state without explicit user approval in that thread.

Actual-root readiness is optional in the first issue #236 closure.

Acceptable first closure evidence:

- disposable-root live-browser smoke passed; and
- actual-root readiness is either metadata-only user-approved and recorded, or
  explicitly listed as unverified because user approval was not requested or
  not granted.

If the user explicitly authorizes actual-root readiness, the default actual
root check should be metadata-only and symbolic-path-only. An actual-root write
smoke requires a separate explicit approval inside the Codex C/E thread.

### Safe Synthetic Entry Policy

The only approved smoke journal text prefix is:

```text
MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW
```

Required properties:

- include the prefix exactly at the beginning of the note, label, or display
  value;
- include an ISO-like timestamp or short run ID after the prefix;
- do not include private match analysis, raw local paths, raw payloads,
  credential-looking values, or real gameplay advice;
- use `source_surface = "local_app_smoke_test"` when the route supports it;
- use `privacy_label = "synthetic"` when the route supports it.

For actual-root writes, the user must approve both:

- that a synthetic entry may be written; and
- whether the entry should be unattached or attached to a visible context.

No cleanup or delete route is authorized. If a synthetic actual-root entry is
created, it remains a clearly labeled journal entry unless a future contract
authorizes a safe review/delete workflow.

### Context Policy

Preferred smoke context order:

1. Use a visible match/game context already shown by the local app when one is
   available and approved for the smoke.
2. Use a disposable-root synthetic context only if it is created through an
   approved synthetic setup path in the disposable root.
3. Use an explicitly unattached journal note only when the browser UI supports
   that path without inventing match/game identity.
4. If no safe visible context exists and the browser UI cannot submit an
   unattached note, record the write smoke as blocked and route a follow-up
   issue for a synthetic context seed or approved import path.

The cockpit must not invent parser match IDs or parser game IDs. It must not
infer context from display text, raw local files, analytics guesses, journal
notes, or AI output.

### UI Evidence Is Primary

For live-browser smoke, the primary evidence is user-visible local app behavior:

- setup/status page displays Match Journal readiness with symbolic paths;
- cockpit renders through the local frontend;
- journal submit uses the FastAPI `/api/journal/...` facade;
- successful response is sanitized;
- refresh/reload preserves the journal update in the UI when the UI has a
  valid context and bundle display path.

Metadata-only SQLite checks are allowed for disposable roots when they do not
dump row contents and only prove file placement or row counts. Actual-root
SQLite inspection is approval-gated and should be avoided unless the user asks
for it.

### Failed/Unavailable Retry Evidence

Failed/unavailable retry behavior should be proven by automated frontend tests
first. A live browser retry check is optional and may be run only if it can be
induced without destructive controls, broad CORS changes, process killing, raw
database manipulation, or writing invalid private data.

If a safe live retry path is not available, Codex C/E should mark live retry
as unverified and cite the automated tests instead.

### Direct Status API CORS Remains Deferred

Passing this readiness smoke does not authorize browser calls to the direct
status API, global status API CORS changes, overlay clients, public network
access, or any browser write route outside the FastAPI local app facade.

## Public Interface

### Launcher / Startup Surface

Approved launcher surfaces:

- `tools/dev_app/start_mythic_edge_dev_app.ps1`
- `tools/dev_app/dev_app_launcher.py`
- `Start Mythic Edge Dev App.cmd`

Approved disposable-root preflight command:

```powershell
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Check -AppDataRoot <temp_app_data_root>
```

Approved disposable-root live-app command for a manual smoke:

```powershell
.\tools\dev_app\start_mythic_edge_dev_app.ps1 -Start -AppDataRoot <temp_app_data_root>
```

Optional flags:

```powershell
-NoOpen
-LogToConsole
-BackendPort <loopback_port>
-FrontendPort <loopback_port>
```

Rules:

- backend and frontend hosts must remain loopback;
- the launcher must not run Git operations;
- the launcher must not delete, reset, wipe, archive, or clean app-data
  folders;
- the launcher must not create the Match Journal database in check mode or
  merely by starting the app;
- launcher logs must use symbolic or redacted paths.

### Browser Surface

Approved frontend URL pattern:

```text
http://127.0.0.1:<frontend_port>
```

`localhost` may be accepted when produced by the approved app/launcher, but
the default smoke target should be `127.0.0.1`.

Required user-visible smoke flow:

1. Confirm clean branch and no generated artifacts in the repo.
2. Create or choose a disposable temp app-data root.
3. Run launcher preflight with the disposable root.
4. Start the local app with the disposable root.
5. Open the loopback frontend.
6. Confirm backend/frontend connectivity through setup/status.
7. Confirm setup/status shows Match Journal readiness with
   `<app_data>\db\match_journal.sqlite3`.
8. Confirm the Match Journal cockpit renders without destructive controls,
   direct status API write controls, pilot-error controls, raw SQL, Sheets,
   OpenAI, AI/coaching, Line Tracer, hidden-card, player-mistake, or best-line
   controls.
9. Select or use a visible safe match/game context when available.
10. Submit one approved synthetic note, manual label, review flag, experiment
    label, or display-only correction through the browser UI.
11. Confirm successful/sanitized response.
12. Refresh or reload the page.
13. Confirm the journal update remains visible through the UI when a valid
    context is available.
14. Stop only the app processes started for the smoke.
15. Confirm no generated/private/local artifacts are inside the repo or staged
    by Git.

If steps 9 through 13 cannot run safely because no context exists, record the
blocker. Do not work around it by inventing parser IDs, editing production
data, or adding destructive controls.

### Backend Route Surface

Approved browser-facing routes remain:

```text
GET  /api/journal
POST /api/journal/notes
POST /api/journal/opponent-labels
POST /api/journal/review-flags
POST /api/journal/experiment-label
POST /api/journal/display-corrections
```

Forbidden browser-facing routes in this readiness slice:

```text
POST /api/journal/pilot-error
DELETE /api/journal/...
PUT /api/journal/...
PATCH /api/journal/...
```

Forbidden browser/API capabilities:

- arbitrary SQL;
- generic database browsing;
- raw row dumps;
- cleanup, reset, delete, wipe, truncate, vacuum, or archive controls;
- parser runner controls;
- live watcher controls;
- import/export/sync controls outside already contracted import surfaces;
- Google Sheets, Apps Script, webhook, OpenAI, model-provider, AI/coaching,
  Line Tracer, hidden-card, player-mistake, best-line, or production controls.

## Inputs

Allowed inputs:

- current repo code and tests;
- GitHub issue #236 and tracker #202;
- approved local app launcher commands;
- loopback backend and frontend URLs;
- disposable temp app-data root;
- symbolic setup/status response fields;
- synthetic smoke note or label text using the approved prefix;
- visible app UI context when available;
- explicit user approval for any actual-root metadata check or write.

Forbidden inputs:

- raw Player.log contents;
- private JSONL payloads;
- workbook exports;
- failed-post payloads;
- runtime status payload bodies;
- SQLite row dumps from the actual app-data root;
- raw local paths in committed docs/tests/logs;
- secrets, credentials, tokens, API keys, webhook URLs, OAuth values, or
  environment variable values;
- model-provider or AI output.

## Outputs

Allowed outputs:

- this contract;
- Codex C implementation/comparison handoff;
- Codex E review or contract-test report;
- command-result validation evidence;
- live-browser smoke notes in the handoff/report using symbolic paths only;
- disposable-root generated files outside the repo;
- optional screenshots only if they do not contain raw local paths, private
  notes, raw payloads, secrets, or credential-like values.

Forbidden outputs:

- committed SQLite databases, WAL, SHM, or journal files;
- committed frontend build output;
- committed raw logs, runtime logs, failed posts, workbook exports, JSONL
  artifacts, runtime status files, generated/private/local-only artifacts, or
  secrets;
- public or GitHub-hosted screenshots containing private/local data;
- cleanup scripts or destructive controls;
- changed parser, analytics, workbook, webhook, Apps Script, Sheets, OpenAI,
  AI/coaching, or production behavior.

## Invariants

- The smoke proves local app readiness, not parser correctness.
- Match Journal annotations remain human-owned local annotations.
- Parser facts remain read-only in the cockpit.
- The FastAPI `/api/journal/...` facade remains the only browser-facing write
  path.
- Direct status API browser writes remain forbidden/deferred.
- Disposable-root smoke comes before any actual-root work.
- Actual-root inspection or writes require explicit user approval.
- Setup/status and journal reads must not create app-data files.
- First journal writes may create only the app-owned Match Journal database in
  the selected app-data root.
- Browser failed/unavailable submit paths must preserve unsaved form input.
- No destructive cleanup action is authorized.
- No generated/private/local artifacts may be staged or committed.

## Error Behavior

Launcher preflight blocker:

- report the blocker;
- do not start the app;
- do not create app-data folders in check mode;
- route to Codex C/D only if a narrow launcher issue is proven.

Port conflict:

- report unavailable port;
- do not kill unrelated processes;
- either choose another loopback port with user-visible evidence or mark the
  live smoke blocked.

Backend/frontend unavailable:

- report the unavailable component;
- do not claim browser smoke passed;
- preserve any generated artifact check evidence.

Missing visible journal context:

- do not invent parser IDs;
- do not write to actual app-data without approval;
- mark write persistence as blocked or route a follow-up for synthetic context
  setup.

Write returns sanitized non-ok envelope:

- UI must show a not-saved/unavailable/error state;
- unsaved form values must remain present;
- do not report the update as persisted.

Unexpected app-data or generated artifact in repo:

- stop before staging or submitter work;
- classify as generated/private/local artifact drift;
- do not delete it unless the user explicitly approves cleanup.

Actual-root approval not granted:

- leave actual-root readiness as unverified, not failed;
- record the approval boundary in the handoff/report.

## Side Effects

Codex B side effects authorized:

- create this contract only.

Codex C side effects authorized only when needed:

- create or update the implementation handoff;
- update focused tests or docs for smoke/readiness proof;
- run a disposable-root launcher/browser smoke if feasible;
- create generated app-owned files only under the disposable temp root during
  the smoke;
- stop only app processes started by the smoke.

Codex C side effects not authorized:

- no actual-root writes without explicit user approval;
- no app-data cleanup or deletion;
- no parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/
  OpenAI/AI/coaching/production changes;
- no direct status API CORS redesign;
- no generated/private/local artifact commits.

## Dependency Order

Recommended Codex C order:

1. Confirm branch and git status.
2. Compare current launcher, backend, frontend, setup/status, and tests against
   this contract.
3. Decide whether the pass is comparison-only, docs/test-only, or narrow
   implementation.
4. If code/test changes are needed, add focused tests first where practical.
5. Preserve disposable-root-first and actual-root-approval-gated behavior.
6. Run automated validation.
7. If feasible and safe, run disposable-root live-browser smoke.
8. Do not run actual-root readiness or actual-root write smoke without explicit
   approval.
9. Write implementation handoff with smoke status and remaining unverified
   layers.

## Compatibility

Must remain compatible with:

- `match_journal_status_api.md`;
- `match_journal_cockpit_ui.md`;
- `match_journal_cockpit_write_controls.md`;
- local app setup/status schema version
  `analytics_app_backend_setup_status.v1`;
- Match Journal cockpit response schema version
  `match_journal_cockpit_ui.v1`;
- current app-owned Match Journal database path
  `<app_data>\db\match_journal.sqlite3`;
- current loopback FastAPI frontend-origin policy;
- current developer launcher command surfaces.

Must not require:

- a production deployment;
- Google Sheets sync;
- workbook or Apps Script changes;
- direct status API browser writes;
- pilot-error browser controls;
- arbitrary SQL or database browser UI;
- OpenAI/model-provider runtime behavior;
- AI coaching or Line Tracer behavior;
- actual app-data root writes for first closure.

## Unknowns

- Whether the user's actual app-data root currently contains visible match/game
  context suitable for a real-root smoke.
- Whether a disposable root can produce a visible cockpit context through
  already-approved import/setup paths without new implementation.
- Whether a future synthetic context seed helper is needed for repeatable
  browser write smoke.
- Whether a live unavailable/retry path can be induced safely without adding
  behavior.
- Whether future cockpit/overlay clients need direct status API CORS hardening.

## Suspected Gaps

- Manual live-browser smoke has not been recorded after #234.
- Real-root readiness has not been recorded.
- The browser write smoke may be blocked in an empty disposable root if the UI
  needs visible match/game context before enabling journal forms.
- There is no dedicated durable smoke report artifact beyond the future
  implementation handoff/review report.
- Direct status API broad CORS remains a future hardening issue and should not
  be hidden by passing FastAPI smoke evidence.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- parser event kind values;
- parser payload shapes;
- extractor behavior;
- match identity;
- game identity;
- deduplication;
- analytics schema, migrations, ingest, or deterministic views;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- direct status API global CORS policy;
- pilot-error browser controls;
- production behavior;
- OpenAI/model-provider behavior;
- AI coaching;
- Line Tracer;
- hidden-card inference;
- archetype classification truth;
- player-mistake truth;
- gameplay advice;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs,
  OAuth values, or environment variable policy;
- raw logs, generated data, runtime status files, failed posts, workbook
  exports, private JSONL artifacts, SQLite database files, WAL/SHM/journal
  files, frontend build output, or local-only artifacts.

## Tests And Validation Required

Minimum automated validation for Codex C comparison or implementation:

```powershell
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
npm --prefix frontend test -- --run src/App.test.tsx
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
```

Recommended adjacent validation if code changed:

```powershell
py -m pytest -q tests\test_match_journal_status_api.py tests\test_status_api.py
py -m pytest -q tests\test_match_journal_service.py tests\test_match_journal_repository.py tests\test_match_journal_schema.py
npm --prefix frontend test -- --run
```

Required path-scoped protected-surface scan for changed files:

```powershell
@'
docs/contracts/match_journal_live_browser_real_app_data_readiness.md
docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md
tools/dev_app/dev_app_launcher.py
tools/dev_app/start_mythic_edge_dev_app.ps1
Start Mythic Edge Dev App.cmd
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/match_journal_cockpit.py
src/mythic_edge_parser/local_app/match_journal_runtime.py
src/mythic_edge_parser/local_app/paths.py
src/mythic_edge_parser/local_app/setup_status.py
frontend/src/api.ts
frontend/src/types.ts
frontend/src/App.tsx
frontend/src/App.test.tsx
tests/test_match_journal_cockpit_ui_backend.py
tests/test_analytics_dev_app_launcher.py
tests/test_analytics_local_app_backend.py
tests/test_analytics_local_app_config.py
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Required path-scoped secret/private-marker scan for changed files:

```powershell
@'
docs/contracts/match_journal_live_browser_real_app_data_readiness.md
docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md
tools/dev_app/dev_app_launcher.py
tools/dev_app/start_mythic_edge_dev_app.ps1
Start Mythic Edge Dev App.cmd
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/match_journal_cockpit.py
src/mythic_edge_parser/local_app/match_journal_runtime.py
src/mythic_edge_parser/local_app/paths.py
src/mythic_edge_parser/local_app/setup_status.py
frontend/src/api.ts
frontend/src/types.ts
frontend/src/App.tsx
frontend/src/App.test.tsx
tests/test_match_journal_cockpit_ui_backend.py
tests/test_analytics_dev_app_launcher.py
tests/test_analytics_local_app_backend.py
tests/test_analytics_local_app_config.py
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Generated artifact sweep:

```powershell
git status --short --branch --untracked-files=all
Get-ChildItem -Recurse -File -Include *.sqlite,*.sqlite3,*.db,*.db-wal,*.db-shm,*.journal,*.sqlite-wal,*.sqlite-shm,*.sqlite-journal |
  Where-Object { $_.FullName -notmatch '\\.git\\' } |
  Select-Object -ExpandProperty FullName
Test-Path frontend\dist
```

Expected smoke evidence fields in Codex C/E handoff:

- branch and sync status;
- launcher command used;
- app-data root class: `disposable`, `actual_metadata_only`, or
  `actual_write_approved`;
- whether browser opened;
- backend/frontend connectivity status;
- setup/status symbolic Match Journal path status;
- cockpit render status;
- context source: `visible_app_context`, `synthetic_disposable_context`,
  `unattached`, or `blocked_no_safe_context`;
- route family used: `/api/journal/...`;
- synthetic entry prefix used;
- submit result status;
- refresh/reload persistence status;
- failed/unavailable retry status;
- generated artifact status;
- actual-root status and approval state;
- remaining unverified layers.

## Acceptance Criteria

This contract is accepted when:

- the disposable-root smoke baseline is explicit;
- actual-root work is explicitly approval-gated and not mandatory for first
  closure;
- synthetic entry text policy is explicit;
- visible-context, unattached-note, and blocked-no-context behavior are
  explicit;
- UI evidence versus metadata-only SQLite evidence is explicit;
- failed/unavailable retry expectations are explicit;
- direct status API CORS remains deferred;
- protected surfaces and local artifact boundaries are explicit;
- validation commands and smoke evidence fields are explicit;
- a pasteable Codex C prompt and workflow handoff are included.

Issue #236 implementation/review is acceptable only if:

- Codex C creates the comparison handoff;
- any code/test changes stay within the authorized local app/UI/test/handoff
  surfaces;
- disposable-root live-browser smoke is run and passed, or clearly marked
  blocked with a contract-consistent reason;
- actual-root readiness is either user-approved and metadata-only, or listed as
  unverified due to approval boundary;
- no generated/private/local artifacts are staged or committed;
- no parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/
  OpenAI/AI/coaching/production behavior is changed.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #236:
Match Journal live-browser smoke and real app-data readiness.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/236

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Contract:
docs/contracts/match_journal_live_browser_real_app_data_readiness.md

Goal:
Compare the current launcher, FastAPI local app backend, Match Journal cockpit,
setup/status, frontend, and focused tests against the contract. Produce
docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md.
Keep the pass readiness-focused. Implement only narrow docs/tests/launcher/UI
fixes if the comparison proves current behavior cannot satisfy the contracted
smoke safely.

Before editing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what the live-browser readiness smoke is supposed to prove.
- State what the current code already supports.
- State what remains unverified or blocked.
- State the exact minimal comparison or implementation plan.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/match_journal_live_browser_real_app_data_readiness.md
- docs/contracts/match_journal_status_api.md
- docs/contracts/match_journal_cockpit_ui.md
- docs/contracts/match_journal_cockpit_write_controls.md
- docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md
- docs/contract_test_reports/match_journal_cockpit_write_controls.md
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/match_journal_cockpit.py
- src/mythic_edge_parser/local_app/match_journal_runtime.py
- src/mythic_edge_parser/local_app/paths.py
- src/mythic_edge_parser/local_app/setup_status.py
- frontend/src/api.ts
- frontend/src/types.ts
- frontend/src/App.tsx
- frontend/src/App.test.tsx
- tools/dev_app/dev_app_launcher.py
- tools/dev_app/start_mythic_edge_dev_app.ps1
- Start Mythic Edge Dev App.cmd
- tests/test_match_journal_cockpit_ui_backend.py
- tests/test_analytics_dev_app_launcher.py
- tests/test_analytics_local_app_backend.py
- tests/test_analytics_local_app_config.py

Required comparison:
- Confirm disposable-root launcher preflight/start support.
- Confirm setup/status uses symbolic Match Journal path.
- Confirm journal reads/setup-status remain non-creating.
- Confirm first explicit journal write creates only app-owned Match Journal DB
  under the selected app-data root.
- Confirm browser UI uses only /api/journal/... routes.
- Confirm no pilot-error, destructive, raw SQL, direct status API write,
  Sheets, OpenAI, AI/coaching, Line Tracer, hidden-card, player-mistake, or
  best-line controls are exposed.
- Confirm failed/unavailable write tests preserve unsaved input.
- Decide whether a disposable-root live-browser smoke can be run safely.
- Do not run actual-root readiness or actual-root write smoke unless the user
  explicitly approves it in this thread.

Optional live smoke:
- If feasible and non-destructive, run a disposable app-data root live-browser
  smoke through the approved launcher and frontend.
- Use only synthetic text beginning with
  MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW.
- If no safe visible context exists, do not invent parser IDs. Mark the write
  smoke blocked and recommend the narrow follow-up needed.
- Stop only processes started by this smoke.

Do not:
- target main;
- stage, commit, push, open a PR, merge, close issue #236, or mark tracker #202
  complete unless explicitly asked;
- inspect, write, delete, move, reset, archive, sanitize, or clean actual
  app-data root contents without explicit user approval;
- change parser behavior, parser state final reconciliation, parser event
  classes, parser payload shapes, match/game identity, deduplication, analytics
  schema/migrations/ingest/views, workbook schema, webhook payload shape, Apps
  Script behavior, Google Sheets behavior, output transport, direct status API
  global CORS policy, production behavior, OpenAI/model-provider behavior,
  AI/coaching behavior, Line Tracer behavior, hidden-card inference, archetype
  truth, player-mistake truth, or gameplay advice;
- create or commit raw Player.log files, private JSONL artifacts, generated
  SQLite databases, WAL/SHM/journal files, frontend build output, runtime logs,
  failed posts, workbook exports, secrets, credentials, tokens, API keys,
  webhook URLs, spreadsheet IDs, environment variable values, or local-only
  artifacts.

Validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
npm --prefix frontend test -- --run src/App.test.tsx
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
Run path-scoped protected-surface and secret/private-marker scans over changed
files.
Run generated artifact checks and report any disposable-root artifacts
separately from repo artifacts.

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- files changed
- exact comparison/test/code sections changed, if any
- disposable-root smoke status
- actual-root readiness status and approval state
- failed/unavailable retry status
- generated/private artifact status
- protected-surface status
- secret/private-marker status
- validation run
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/236"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue problem representation for Match Journal live-browser smoke and real app-data readiness"
  target_artifact: "docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md"
  contract_artifact: "docs/contracts/match_journal_live_browser_real_app_data_readiness.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch --untracked-files=all"
    - "git diff --check"
    - "path-scoped protected-surface scan for docs/contracts/match_journal_live_browser_real_app_data_readiness.md"
    - "path-scoped secret/private-marker scan for docs/contracts/match_journal_live_browser_real_app_data_readiness.md"
  stop_conditions:
    - "Do not target main."
    - "Do not run actual-root readiness or actual-root write smoke without explicit user approval."
    - "Do not delete, reset, wipe, rename, move, archive, clean, sanitize, copy, upload, or commit local app-data or private/generated artifacts."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not change direct status API global CORS policy."
    - "Do not create or commit generated/private/local artifacts or secrets."
```
