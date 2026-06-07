# Private Release E2E Browser Integration Readiness Contract

## Module

`private_release_e2e_browser_integration_readiness`

Plain English: this contract defines the private-release end-to-end browser
smoke and integration-readiness gate for the current analytics/local app branch.
It should answer whether Mythic Edge is safe and usable enough for a private
local release pass, without claiming public release, production deployment,
parser correctness, analytics truth, AI coaching, or main integration
readiness.

This is a readiness contract, not a feature contract. It does not implement
code, add new analytics behavior, add new UI behavior, or authorize protected
surface changes.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/285

## Trackers

- Analytics usability and local ingest:
  https://github.com/Tahjali11/Mythic-Edge/issues/204
- Local developer app shell:
  https://github.com/Tahjali11/Mythic-Edge/issues/207
- Match Journal and cockpit foundation, context only:
  https://github.com/Tahjali11/Mythic-Edge/issues/202

## Branch

Target branch:

```text
codex/analytics-foundation
```

Observed source state for this Codex B pass:

```text
origin/codex/analytics-foundation
400b19a90169bf52f6ca5bc5af9566419f5fe3a6
```

This contract must not target `main` directly.

## Authority And Source Artifacts Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- issue #285
- tracker #204
- umbrella #207
- Match Journal tracker #202, context only
- `docs/private_local_v1_operator_guide.md`
- `docs/contracts/private_local_v1_local_app_startup_status_smoke.md`
- `docs/contract_test_reports/private_local_v1_local_app_startup_status_smoke.md`
- `docs/contracts/private_local_v1_clean_checkout_install_launch.md`
- `docs/contract_test_reports/private_local_v1_readiness_baseline_refresh.md`
- `docs/contracts/live_player_log_v1_supported_readiness.md`
- `docs/contract_test_reports/live_player_log_v1_supported_readiness.md`
- `docs/contracts/match_journal_live_browser_real_app_data_readiness.md`
- `docs/contracts/match_journal_safe_context_browser_write_smoke.md`
- `docs/contract_test_reports/match_journal_safe_context_browser_write_smoke.md`
- `docs/contracts/analytics_browser_jsonl_multi_file_upload.md`
- `docs/contracts/analytics_manual_jsonl_import_ui_job_status.md`
- `docs/contracts/analytics_dynamic_decision_support_dashboard.md`
- `docs/contract_test_reports/analytics_dynamic_decision_support_dashboard.md`
- `docs/contracts/quality_app_submit_error_report_codex_triage.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/analytics_dashboard.py`
- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/local_app/match_journal_cockpit.py`
- `src/mythic_edge_parser/local_app/match_journal_runtime.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `tools/dev_app/dev_app_launcher.py`
- `tools/dev_app/start_mythic_edge_dev_app.ps1`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tools/dev_app/private_local_v1_setup.py`
- `frontend/package.json`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/status.ts`
- `frontend/src/types.ts`
- relevant focused backend, frontend, launcher, Match Journal, import, live,
  and dashboard tests

## Risk Tier

High.

Reasons:

- this is cross-layer private-release readiness language;
- it may start backend and frontend processes;
- it may use a browser against the local app;
- it may create app-owned generated folders, logs, and SQLite files under a
  disposable app-data root;
- it may optionally inspect actual private local app-data or Player.log
  readiness only with explicit user approval;
- it touches import, analytics dashboard, Live Player.log, Match Journal, and
  error-report surfaces;
- a weak verdict could incorrectly imply parser truth, merge readiness,
  deploy readiness, public-release readiness, or privacy safety.

## Owning Layer

Primary owning layer: Quality / Governance release readiness.

Supporting layers:

- Local App / UI;
- Generated / Local Artifacts;
- Analytics Foundation;
- Match Journal;
- Live Player.log Mode;
- Operator documentation.

## Internal Project Area

Quality / Governance.

Supporting internal project areas:

- Local App / UI;
- Analytics;
- Match Journal;
- Generated / Local Artifacts;
- Live Player.log Mode.

## Truth Owner

This contract owns only readiness evidence and readiness vocabulary.

Truth ownership remains unchanged:

- Parser/state owns parser-managed event interpretation, match facts, game
  facts, parser event classes, match/game identity, deduplication, and final
  reconciliation.
- Analytics SQLite owns local deterministic storage and fixed downstream views
  over parser-normalized facts.
- Match Journal owns human notes, manual labels, review flags, experiment
  labels, and display-only correction proposals.
- Live Player.log readiness owns metadata/status evidence only unless a later
  contract runs approved live capture behavior.
- Local app backend owns loopback route validation and local response shaping.
- Frontend owns presentation, local browser state, and explicit user actions.
- Readiness reports own evidence, residual-risk language, and next-role
  recommendations only.

Readiness reports, screenshots, browser observations, local app UI labels,
analytics views, Match Journal notes, dashboard modules, and smoke summaries
must not become parser truth, analytics truth, Match Journal truth, gameplay
advice, hidden-card inference, archetype classification, player-mistake truth,
AI coaching, merge readiness, deploy readiness, public-release readiness, or
main integration authority.

## Bridge-Code Status

`shared_support`

Allowed flow:

```text
latest approved branch source
  -> focused validation commands
  -> disposable app-data-root backend/frontend startup
  -> loopback browser smoke
  -> sanitized readiness report
```

Optional, approval-gated flow:

```text
explicit user-approved actual private app-data or Player.log metadata checks
  -> metadata/status-only observations
  -> sanitized readiness report
```

Forbidden reverse flow:

- smoke results must not alter parser behavior;
- browser state must not rewrite parser, analytics, Match Journal, workbook,
  webhook, Apps Script, Google Sheets, production, OpenAI/model-provider, or
  AI/coaching behavior;
- readiness verdicts must not bypass normal Codex E/F/G review or deployment
  gates;
- private local evidence must not be copied into repo artifacts.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/private_release_e2e_browser_integration_readiness.md`

Expected later report artifact:

- `docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md`

Optional future implementation artifact, only if Codex C adds a helper or
discovers a narrow comparison gap:

- `docs/implementation_handoffs/private_release_e2e_browser_integration_readiness_comparison.md`

Optional helper files Codex C may add only if the comparison proves the current
manual smoke path cannot be repeated safely without a small harness:

- `tools/dev_app/private_release_e2e_smoke.py`
- `tests/test_private_release_e2e_browser_integration_readiness.py`

Existing files Codex C may inspect and execute but must not change unless a
contracted smoke-helper gap is found:

- `tools/dev_app/dev_app_launcher.py`
- `tools/dev_app/start_mythic_edge_dev_app.ps1`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tools/dev_app/private_local_v1_setup.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/*.py`
- `frontend/src/*.tsx`
- `frontend/src/*.ts`
- focused backend/frontend tests

Not owned:

- parser modules;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema, migrations, ingest semantics, or deterministic view
  definitions;
- Match Journal schema/repository/service semantics;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- output transport;
- production behavior;
- CI gate behavior;
- main integration policy;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- local private app-data contents.

## Observed Current Behavior

Observed at `origin/codex/analytics-foundation`
`400b19a90169bf52f6ca5bc5af9566419f5fe3a6`:

- issue #285 is open;
- tracker #204 is open;
- local app umbrella #207 is open;
- Match Journal tracker #202 is open and remains context only for this issue;
- the branch includes the Dynamic Decision Support dashboard from #283 / PR
  #284;
- `src/mythic_edge_parser/local_app/backend.py` exposes a FastAPI local app
  backend with loopback-oriented API routes;
- `frontend/` contains a React + TypeScript + Vite local app;
- `tools/dev_app/dev_app_launcher.py` and
  `tools/dev_app/start_mythic_edge_dev_app.ps1` define backend/frontend
  startup paths;
- `tools/dev_app/private_local_v1_setup.py` and
  `tools/dev_app/setup_private_local_v1.ps1` define private-local-v1 setup and
  proof flows;
- `docs/private_local_v1_operator_guide.md` defines private-local-v1 as a
  private Windows local operator profile, not public release or production
  readiness.

Current backend route families include:

- setup and health:
  - `GET /api/health`
  - `GET /api/app/setup-status`
  - `GET /api/app/config`
  - `GET /api/app/paths`
- analytics status, history, review, and dashboard:
  - `GET /api/analytics/database/status`
  - `GET /api/analytics/matches`
  - `GET /api/analytics/games`
  - `GET /api/analytics/opening-hands`
  - `GET /api/analytics/mulligans`
  - `GET /api/analytics/gameplay-actions`
  - `GET /api/analytics/opponent-card-observations`
  - `GET /api/analytics/play-draw-splits`
  - `GET /api/analytics/game1-postboard-splits`
  - `GET /api/analytics/dashboard/modules`
- live status and diagnostics:
  - `GET /api/live/player-log/status`
  - `GET /api/live/watcher/status`
  - `GET /api/live/watcher/process`
  - `GET /api/live/watcher/diagnostics`
  - `GET /api/live/ingest/status`
- runtime health/status route:
  - `GET /api/runtime/status`
- local error-report preview:
  - `POST /api/feedback/error-report/preview`
- Match Journal browser facade:
  - `GET /api/journal`
  - `GET /api/journal/notes`
  - `POST /api/journal/notes`
  - `POST /api/journal/opponent-labels`
  - `POST /api/journal/review-flags`
  - `POST /api/journal/experiment-label`
  - `POST /api/journal/display-corrections`
- manual import:
  - `POST /api/imports/jsonl`
  - `POST /api/imports/jsonl/upload`
  - `GET /api/imports/jobs/{job_id}`

Observed frontend surfaces include:

- `Mythic Edge Cockpit`;
- cockpit health/status rail;
- `Decision Support`;
- `Review Details`;
- `Setup Status`;
- `Player.log monitor`;
- Live Player.log, watcher, process, and diagnostics display;
- Match Journal cockpit, including no-context unattached smoke note behavior;
- manual import and browser upload controls;
- error-report preview controls;
- dashboard module bar/table display preferences.

Observed prior readiness evidence:

- #251 disposable-root local app startup/status smoke passed as
  degraded-acceptable.
- #237 Match Journal safe no-context browser write/read smoke passed with an
  unattached smoke note strategy.
- #275 Live Player.log readiness report found implementation support ready but
  blocked the final `supported` claim pending an explicitly approved
  real/private Player.log smoke.
- #270 refreshed the private-local-v1 readiness baseline and found no active
  blockers in the original baseline areas, while preserving public-release,
  production, all-repo scanner, Pyright, and package-footprint non-claims.
- #283 Dynamic Decision Support dashboard contract-test report approved the
  fixed read-only dashboard module surface.

## Contract Decision

The next workflow should be a hybrid readiness pass:

1. automated or scripted checks for deterministic backend/frontend/test
   evidence;
2. browser-assisted manual smoke against a disposable app-data root;
3. optional actual-private-root or real/private Player.log checks only with
   explicit user approval;
4. a durable sanitized readiness report.

Default Codex C outcome should be report-first. Codex C may add a tiny
local-only smoke helper only if it proves the current launcher/browser
procedure cannot produce repeatable evidence safely. Codex C should not add new
product behavior to make the smoke pass.

## Public Interface

Readiness report artifact:

```text
docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md
```

Required report metadata:

- issue: `https://github.com/Tahjali11/Mythic-Edge/issues/285`;
- trackers: #204, #207, and #202 context;
- branch and commit under test;
- local platform;
- smoke mode;
- app-data-root mode;
- backend URL;
- frontend URL;
- dependency/install command results;
- focused backend/frontend validation results;
- backend route matrix;
- frontend browser matrix;
- import/readiness evidence;
- dashboard evidence;
- Match Journal evidence;
- Live Player.log evidence;
- error-report evidence;
- generated/private artifact sweep;
- secret/private-marker and protected-surface scan results;
- readiness verdict;
- acceptable degradation;
- residual risks;
- explicit non-claims;
- next recommended role.

Recommended schema label for report front matter or summary:

```text
private_release_e2e_browser_integration_readiness.v1
```

Optional helper interface, if Codex C adds a harness:

```text
python3 tools/dev_app/private_release_e2e_smoke.py --app-data-root <disposable-root> --report-json <temp-output>
```

A helper, if added, must be local-only, must write no repo artifacts by
default, and must not replace browser-assisted observation.

## Inputs

### Required Inputs

- Latest source from `origin/codex/analytics-foundation`.
- Repo-local dependency manifests:
  - `pyproject.toml`
  - `frontend/package.json`
  - `frontend/package-lock.json`
- Current local app backend and frontend source.
- Existing focused tests.
- A disposable app-data root outside the repository.
- Loopback backend and frontend ports.
- Browser session against the local frontend.

### Optional Inputs

Synthetic/sanitized local input:

- a tiny parser-normalized or legacy JSONL smoke payload generated in a
  disposable temp directory; or
- an existing committed sanitized fixture that is already safe for this branch.

Actual private app-data root:

- allowed only after explicit user approval in the active thread;
- must be treated as private local evidence;
- report must use symbolic path labels only;
- report must not include raw note text, raw analytics rows, raw database
  contents, local path values, raw Player.log excerpts, or private payloads.

Actual private Player.log:

- allowed only after explicit user approval in the active thread;
- metadata/status only;
- must not read, copy, paste, hash-display, store, upload, commit, or summarize
  raw log contents.

### Forbidden Inputs

- raw Player.log payloads or excerpts;
- private JSON/JSONL artifact contents in repo files;
- generated SQLite databases or SQLite sidecars;
- runtime logs;
- failed delivery artifacts or retry queues;
- workbook exports;
- generated card/tier data;
- secrets, credentials, tokens, API keys, webhook URLs, or environment values;
- OpenAI/model-provider responses;
- external website archetype lists;
- hidden-card guesses;
- unapproved actual app-data root contents.

## Required Smoke Paths

### 1. Source And Branch Hygiene

Codex C must verify:

- current worktree or clean sibling worktree is based on
  `origin/codex/analytics-foundation`;
- issue #285 is open;
- tracker #204 is open;
- umbrella #207 is open;
- tracker #202 is context only and must not be closed;
- no untracked generated/private artifacts are introduced;
- unrelated dirty worktree changes are not overwritten or staged.

If the primary analytics worktree is dirty or behind, Codex C should use a
clean sibling worktree or detached inspection of `origin/codex/analytics-foundation`
and report that choice.

### 2. Static And Focused Validation

Required validation evidence:

- focused local app backend tests;
- focused private-local-v1 setup/launcher tests;
- focused Match Journal browser facade tests;
- focused manual import/upload tests;
- focused Dynamic Decision Support dashboard tests;
- frontend typecheck;
- frontend tests;
- frontend build, with generated build output removed afterward;
- Ruff over relevant source/tests/tools;
- `git diff --check`;
- agent docs checker;
- path-scoped protected-surface scan;
- path-scoped secret/private-marker scan;
- generated/private artifact sweep.

### 3. Disposable App-Data Backend Startup

Codex C must start or exercise the backend with a disposable app-data root
outside the repository.

Required backend evidence:

- backend binds only to loopback;
- `GET /api/health` returns safe JSON;
- `GET /api/app/setup-status` returns all expected sections;
- setup/config/path responses use symbolic app-data labels and do not expose
  raw temp paths;
- GET status routes do not create app-data artifacts unless their existing
  contract explicitly allows it;
- app-data creation is limited to approved generated folders and SQLite files
  only when a contracted write/import smoke is intentionally exercised.

### 4. Frontend Browser Load

Codex C must load the frontend in a browser against the local backend.

Required browser evidence:

- `Mythic Edge Cockpit` heading renders;
- cockpit lead/status rail renders;
- navigation or sections for Dashboard, Analytics/Review Details, Import,
  Match Journal, setup/status, Live Player.log, and diagnostics are visible or
  reachable;
- browser console/runtime does not show blocking app errors;
- frontend uses a loopback API base URL only;
- unsafe values are redacted or absent;
- no destructive watcher, parser-runner, database reset, upload-to-cloud,
  external-submit, OpenAI, coaching, or production controls are visible.

Screenshots are optional and should not be committed by default. If screenshots
are used as evidence, they must be sanitized, stored outside the repo, and
summarized in the report without private payloads or local path values.

### 5. Analytics And Dashboard Smoke

Required route/browser evidence:

- `GET /api/analytics/database/status`;
- `GET /api/analytics/dashboard/modules`;
- the frontend `Decision Support` section renders exactly the approved
  dashboard module family:
  - `play_draw_win_rate`;
  - `game1_postboard`;
  - `mulligan_opening_hand_outcomes`;
- dashboard modules display `missing`, `empty`, `degraded`, or populated state
  honestly;
- dashboard does not expose SQL text, raw paths, raw payloads, hidden-card
  inference, best-line ranking, player-mistake labels, archetype truth, Line
  Tracer truth, or AI/coaching text;
- frontend dashboard view preferences remain browser-local display state only.

### 6. Import Or Data Recognition Smoke

The default readiness path must prove import/readiness without using private
files.

Accepted evidence options:

1. safer minimum: browser/manual import controls render; invalid or empty input
   is rejected with sanitized job/error labels and no database creation beyond
   existing route behavior;
2. stronger preferred option: import a tiny synthetic/sanitized JSONL smoke
   payload created in a disposable temp location, then verify sanitized import
   job status and analytics dashboard/database status without committing the
   payload or generated database;
3. actual private import: approval-gated only, not required for the baseline
   verdict.

The report must state which option was used.

The import smoke must not store raw Player.log payloads in SQLite, copy private
JSONL into the repo, retain raw upload contents, expose raw hashes, expose raw
paths, or treat legacy/imported `derived` labels as parser truth.

### 7. Match Journal Browser Smoke

Required disposable-root evidence:

- Match Journal cockpit renders;
- no parser match/game identity is invented when no context exists;
- no-context smoke uses the contracted unattached smoke note path;
- browser write goes through `POST /api/journal/notes`;
- request uses `note_scope = "unattached"` and omits `context`;
- note text begins with
  `MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW`;
- readback uses `GET /api/journal/notes` by exact journal-owned note ID;
- browser/session storage stores only the journal-owned note ID;
- app-data artifacts are limited to the Match Journal SQLite database under
  the disposable root;
- analytics SQLite is not created by the Match Journal smoke.

Actual app-data-root Match Journal write/read smoke is optional and requires
explicit user approval. Without approval, the report must say actual-root write
smoke was not run and whether that blocks the chosen verdict.

### 8. Live Player.log Readiness Smoke

Required disposable-root evidence:

- `GET /api/live/player-log/status`;
- `GET /api/live/watcher/status`;
- `GET /api/live/watcher/process`;
- `GET /api/live/watcher/diagnostics`;
- `GET /api/live/ingest/status`;
- frontend Live Player.log and diagnostics panels render safe status labels;
- watcher start/stop and parser-runner controls remain unavailable/disabled;
- raw Player.log contents are not read, copied, displayed, committed, or stored
  in SQLite;
- final Live Player.log support claim remains blocked unless the #275-required
  real/private smoke has been explicitly approved and completed.

Actual private Player.log readiness smoke is optional and approval-gated. It
may upgrade residual-risk confidence but must not be silently required by this
baseline contract.

### 9. Error Report Preview Smoke

Required evidence:

- error-report preview UI or route is reachable;
- `POST /api/feedback/error-report/preview` returns a sanitized Markdown packet
  for a synthetic issue description;
- `external_submission_enabled` remains `false`;
- the preview excludes raw Player.log contents, raw paths, SQLite contents,
  stack traces with private paths, secrets, credentials, workbook exports, and
  private note bodies unless the user intentionally typed them into the test
  form.

### 10. Cleanup And Artifact Sweep

Required evidence after the smoke:

- backend/frontend dev processes stopped;
- loopback ports are clear or any remaining listeners are identified and
  explicitly cleaned up if repo-owned;
- disposable app-data root removed or recorded as deleted;
- `frontend/dist` removed after build;
- no SQLite database, SQLite sidecar, app-data folder, runtime log, local
  import artifact, private JSON/JSONL artifact, raw log, failed delivery
  artifact, workbook export, or generated card/tier data is present as an
  untracked/staged repo artifact;
- git status lists only intended docs/report/helper changes.

## Optional Actual-Private-Root Checks

Actual private app-data or actual private Player.log checks are not part of
the default smoke. They are optional because they can touch private local data.

They require explicit user approval and a before/after statement:

```text
approval_scope: actual_app_data_readiness_status_only
approval_scope: actual_player_log_metadata_status_only
approval_scope: actual_match_journal_unattached_smoke_write
```

Rules:

- status/readiness checks should be read-only whenever possible;
- write checks must use a clearly labeled synthetic smoke note or synthetic
  import and must not alter parser facts;
- reports must use symbolic labels such as `<actual_app_data>` and
  `<configured_player_log>`;
- raw local paths and raw payloads must not be copied into the repo;
- the user may decline, and decline must produce
  `blocked_pending_user_smoke` only when actual-root evidence is required for
  the desired claim.

## Verdict Vocabulary

Allowed top-level verdicts:

- `private_release_ready`
- `ready_with_acceptable_degradation`
- `blocked_pending_user_smoke`
- `blocked_pending_dependency_or_startup`
- `not_ready_privacy_blocked`
- `not_ready_functional_blocker`

Definitions:

- `private_release_ready`: all required disposable-root validation and browser
  smoke paths pass; optional actual-private-root checks were either not
  requested or passed; no privacy/protected-surface blocker exists; residual
  risks are non-blocking and explicitly listed.
- `ready_with_acceptable_degradation`: required smoke paths pass, but expected
  empty/missing/degraded states remain, such as no analytics database, no
  actual Player.log smoke, or missing private data; the report explains why
  the degradation is acceptable for a private local release pass.
- `blocked_pending_user_smoke`: automated and disposable-root evidence is
  adequate, but an explicitly approval-gated actual private check is required
  before the user can rely on the claim being requested.
- `blocked_pending_dependency_or_startup`: dependency install, backend startup,
  frontend startup, or browser load cannot complete.
- `not_ready_privacy_blocked`: raw/private artifacts, unsafe paths, secrets, or
  private payloads are exposed, committed, or at risk of being committed.
- `not_ready_functional_blocker`: one or more required smoke paths fail in a
  way that blocks private local use.

Forbidden verdicts:

- `production_ready`;
- `public_release_ready`;
- `main_ready`;
- `deploy_ready`;
- `merge_ready`;
- `parser_truth_verified`;
- `analytics_truth_verified`;
- `ai_ready`;
- `coaching_ready`.

## Required Report Shape

The report must include:

```text
schema_version: private_release_e2e_browser_integration_readiness.v1
issue: #285
branch_under_test:
commit_under_test:
platform:
smoke_mode:
app_data_root_mode:
backend_url:
frontend_url:
verdict:
```

Required sections:

- Role Performed
- Source Issue And Trackers
- Branch And Commit
- Contract Used
- Smoke Mode
- Validation Matrix
- Backend Route Matrix
- Browser Smoke Matrix
- Import/Data Recognition Evidence
- Analytics Dashboard Evidence
- Match Journal Evidence
- Live Player.log Evidence
- Error Report Preview Evidence
- Optional Actual-Private-Root Evidence
- Generated And Private Artifact Sweep
- Secret / Private Marker Status
- Protected-Surface Status
- Acceptable Degradation
- Residual Risks
- Explicit Non-Claims
- Next Recommended Role
- Workflow Handoff

The report must not include:

- raw Player.log excerpts;
- raw JSON/JSONL lines;
- raw note bodies from actual user data;
- raw SQLite rows;
- raw SQL text;
- raw local paths;
- raw hashes;
- screenshots containing private payloads;
- secrets or environment values.

## Error Behavior

- If GitHub or branch state cannot be verified, report
  `blocked_pending_dependency_or_startup` or route back to Codex A/B depending
  on ambiguity.
- If dependency installation fails, report the command and sanitized failure
  label; do not patch dependencies unless the contract and next role authorize
  it.
- If backend or frontend startup fails, stop process cleanup safely, record
  sanitized logs/labels, and do not continue to browser smoke.
- If browser automation is unavailable, Codex C may perform manual browser
  observation with the available browser tool or route to Codex E with
  `blocked_pending_user_smoke`; do not fake browser evidence from unit tests.
- If the smoke creates unexpected repo artifacts, stop, preserve the worktree
  state for inspection, and report `not_ready_privacy_blocked` or
  `not_ready_functional_blocker` as appropriate.
- If actual private-root approval is not granted, skip that slice and record it
  explicitly.
- If raw/private data appears in any report candidate, remove the unsafe text
  before finalizing and record a privacy finding.

## Side Effects

Allowed side effects during Codex C/E smoke execution:

- creating a disposable app-data root outside the repo;
- creating approved generated folders under that disposable root;
- creating disposable local SQLite files under that disposable root;
- launching backend and frontend loopback dev servers;
- opening a local browser session;
- browser session/local storage for safe smoke IDs and display preferences;
- creating `frontend/dist` during build, then removing it;
- creating a readiness report under `docs/contract_test_reports/`;
- optionally adding a small smoke helper and focused tests if needed.

Forbidden side effects:

- committing generated/private/runtime artifacts;
- writing actual private app-data without explicit approval;
- reading/copying raw Player.log contents;
- storing raw Player.log payloads in SQLite;
- changing parser behavior;
- changing analytics schema/migrations/ingest;
- changing Match Journal service semantics;
- posting webhooks;
- calling Apps Script;
- writing Google Sheets;
- calling OpenAI/model providers;
- creating or updating GitHub issues/PRs from app code;
- changing CI gates or main integration policy.

## Dependency Order

1. Verify source branch and issue/tracker state.
2. Run static/focused validation.
3. Prepare disposable app-data root.
4. Start backend and frontend on loopback.
5. Run backend route matrix.
6. Run browser load and frontend matrix.
7. Run analytics/dashboard smoke.
8. Run import/data-recognition smoke using safe input strategy.
9. Run Match Journal unattached smoke.
10. Run Live Player.log readiness smoke.
11. Run error-report preview smoke.
12. Stop processes and clean generated artifacts.
13. Run artifact sweeps and path-scoped safety checks.
14. Write readiness report.
15. Route to Codex E for review if no implementation changes were needed, or
    Codex E after Codex C implementation/review handoff if a helper was added.

## Compatibility

This contract must remain compatible with:

- current private-local-v1 operator guide;
- current Windows-first setup/launcher command shapes;
- current FastAPI backend route names;
- current React/Vite frontend app;
- current Match Journal no-context unattached smoke path;
- current Live Player.log status/readiness vocabulary;
- current Dynamic Decision Support dashboard module IDs;
- current manual import/upload job-status contract;
- current secret/private-marker and protected-surface tooling.

This contract must not require:

- public release packaging;
- production deployment;
- main branch integration;
- a release tag;
- actual private app-data access by default;
- actual Player.log content inspection;
- Google Sheets sync;
- OpenAI/model-provider integration;
- CI gate changes;
- Pyright as a required failing gate.

## Tests And Validation Required

Minimum Codex C validation:

```bash
python3 -m pytest -q tests/test_analytics_local_app_backend.py tests/test_analytics_local_app_config.py
python3 -m pytest -q tests/test_private_local_v1_setup.py
python3 -m pytest -q tests/test_match_journal_cockpit_ui_backend.py tests/test_match_journal_status_api.py
python3 -m pytest -q tests/test_analytics_browser_jsonl_upload.py tests/test_analytics_manual_jsonl_import.py
python3 -m pytest -q tests/test_analytics_dynamic_decision_support_dashboard.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
python3 -m ruff check src tests tools
git diff --check
python3 tools/check_agent_docs.py
```

Required safety scans:

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation
python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation
printf '%s\n' <changed-files> | python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
printf '%s\n' <changed-files> | python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Required generated/private artifact sweep:

```bash
find . -path './.git' -prune -o \
  \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' \
     -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' \
     -o -name '*.sqlite-journal' -o -path './frontend/dist' \) -print
```

Browser smoke evidence is required. If Codex C cannot use a browser automation
tool, it must record that as a blocker or perform explicitly described manual
browser observations. Unit tests alone are not enough for the #285 verdict.

## Acceptance Criteria

- Contract artifact exists at
  `docs/contracts/private_release_e2e_browser_integration_readiness.md`.
- Owning truth layer is named as release-readiness evidence only.
- Required disposable-root smoke paths are explicit.
- Optional actual-private-root checks are approval-gated.
- Generated/private artifact boundaries are explicit.
- Verdict vocabulary is explicit and prevents overclaiming.
- Required report shape is explicit.
- Validation evidence is explicit.
- Residual-risk reporting is required.
- Next role is routed with a pasteable prompt and workflow handoff.

## Open Questions And Contract Risks

- A full Windows private-local-v1 launch proof may be stronger than a macOS or
  Linux Codex smoke. If the next thread runs on a non-Windows platform, it must
  record platform as residual risk and must not overclaim Windows operator
  readiness unless current Windows evidence is reused and still applicable.
- The strongest import smoke may require a tiny synthetic JSONL payload. Codex
  C must keep it in a disposable temp location and delete it, or use an
  already committed sanitized fixture if one exists.
- Actual private app-data readiness may be valuable, but it is optional and
  approval-gated because it can expose private notes, analytics data, and local
  paths.
- The #275 final Live Player.log `supported` claim remains blocked until
  explicitly approved real/private smoke evidence exists. This #285 contract
  may still produce `ready_with_acceptable_degradation` if that blocker is
  named clearly.
- Browser tool availability can vary. The report must distinguish actual
  browser evidence from frontend unit-test evidence.

## Expected Codex C Scope

Preferred scope:

- execute the hybrid readiness smoke;
- add
  `docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md`;
- add
  `docs/implementation_handoffs/private_release_e2e_browser_integration_readiness_comparison.md`
  only if implementation/helper work is needed.

Conditional helper scope:

- add a tiny local-only smoke helper under `tools/dev_app/`;
- add focused tests for that helper;
- keep helper output out of repo by default;
- do not change product behavior to satisfy the smoke.

Forbidden Codex C scope:

- no parser behavior changes;
- no analytics schema/migration/ingest changes;
- no Match Journal semantics changes;
- no production, workbook, webhook, Apps Script, Sheets, OpenAI, AI/coaching,
  CI gate, main integration, or public-release behavior changes;
- no generated/private/runtime artifact commits.

## Next Workflow Action

Next role: Codex C: Module Implementer / Readiness Executor.

Pasteable prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer / Readiness Executor for issue #285, private-release end-to-end browser smoke and integration readiness.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/285

  Trackers / umbrellas:
  - #204 Analytics usability and local ingest
  - #207 Local developer app shell
  - #202 Match Journal and cockpit foundation, context only

  Branch:
  codex/analytics-foundation

  Contract:
  docs/contracts/private_release_e2e_browser_integration_readiness.md

  Goal:
  Compare the current branch to the contract, execute the smallest safe hybrid readiness pass, and produce docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md. Add a tiny local-only smoke helper and focused tests only if the current launcher/browser workflow cannot produce repeatable evidence safely.

  First:
  - Fetch and verify origin/codex/analytics-foundation.
  - Use a clean worktree if the primary analytics worktree is dirty or behind.
  - Verify issue #285, tracker #204, umbrella #207, and context tracker #202 state.
  - Do not target main directly.

  Required smoke:
  - Run focused backend/local app/private-local-v1/Match Journal/import/dashboard tests.
  - Run frontend npm ci, typecheck, tests, and build; remove generated build output afterward.
  - Start backend and frontend on loopback with a disposable app-data root.
  - Load the React/Vite app in a browser and verify the cockpit, dashboard, analytics/review details, import, Match Journal, Live Player.log, diagnostics, setup/status, and error-report surfaces render safely.
  - Exercise analytics/dashboard status, import/data-recognition, Match Journal unattached smoke note write/read, Live Player.log readiness/status, and error-report preview paths.
  - Use only synthetic/sanitized or disposable data unless the user explicitly approves an actual private app-data or Player.log check.
  - Stop processes, remove generated build/app-data artifacts, and run generated/private artifact sweeps.
  - Run path-scoped secret/private-marker and protected-surface checks.

  Report:
  - Write docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md.
  - Use the contract's verdict vocabulary.
  - List acceptable degradation and residual risks explicitly.
  - Distinguish actual browser evidence from unit-test evidence.
  - Include the workflow_handoff block for Codex E review, or route back if blocked.

  Do not:
  - Open a PR or commit unless explicitly asked.
  - Target main directly.
  - Commit raw logs, private JSON/JSONL artifacts, generated SQLite databases, runtime artifacts, failed delivery artifacts, workbook exports, secrets, credentials, tokens, API keys, webhook URLs, generated card/tier data, or private local app-data contents.
  - Store raw Player.log payloads in SQLite.
  - Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, CI gate behavior, or main integration policy.
  - Let readiness reports, local app UI, analytics views, Match Journal notes, dashboard modules, or smoke-test summaries become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, AI coaching, merge readiness, deploy readiness, public-release readiness, or production readiness.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/285"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  related_match_journal_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/private_release_e2e_browser_integration_readiness.md"
  target_artifact: "docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md"
  optional_handoff_artifact: "docs/implementation_handoffs/private_release_e2e_browser_integration_readiness_comparison.md"
  verdict: "contract_ready_for_hybrid_readiness_execution"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "Codex B docs-only validation pending in current thread."
    - "Codex C must run focused backend/frontend validation, browser smoke, artifact sweep, and path-scoped safety scans."
  stop_conditions:
    - "Do not target main directly."
    - "Do not open a PR or commit unless explicitly asked."
    - "Do not use actual private app-data or Player.log checks without explicit user approval."
    - "Do not commit generated/private/runtime artifacts or secrets."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not claim merge readiness, deploy readiness, public-release readiness, production readiness, parser truth, analytics truth, or AI/coaching readiness."
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/285"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  related_match_journal_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/private_release_e2e_browser_integration_readiness.md"
  target_artifact: "docs/contract_test_reports/private_release_e2e_browser_integration_readiness.md"
  optional_handoff_artifact: "docs/implementation_handoffs/private_release_e2e_browser_integration_readiness_comparison.md"
  verdict: "contract_ready_for_hybrid_readiness_execution"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  verified_source_commit: "400b19a90169bf52f6ca5bc5af9566419f5fe3a6"
  validation:
    - "Documentation-only contract writer pass."
    - "Codex C must run focused backend/frontend validation, browser smoke, artifact sweep, and path-scoped safety scans."
  stop_conditions:
    - "Do not target main directly."
    - "Do not open a PR or commit unless explicitly asked."
    - "Do not use actual private app-data or Player.log checks without explicit user approval."
    - "Do not commit raw logs, private JSON/JSONL artifacts, generated SQLite databases, runtime artifacts, failed delivery artifacts, workbook exports, secrets, credentials, tokens, API keys, webhook URLs, generated card/tier data, or private local app-data contents."
    - "Do not store raw Player.log payloads in SQLite."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, CI gate behavior, or main integration policy."
    - "Do not let readiness reports, local app UI, analytics views, Match Journal notes, dashboard modules, or smoke-test summaries become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, AI coaching, merge readiness, deploy readiness, public-release readiness, or production readiness."
```
