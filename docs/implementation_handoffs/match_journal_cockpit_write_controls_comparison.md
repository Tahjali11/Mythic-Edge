# Match Journal Cockpit Write Controls Implementation Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/234>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/202>

## Contract

`docs/contracts/match_journal_cockpit_write_controls.md`

## Internal Project Area

Local App / UI.

## Truth Owner

Parser/state layers remain truth owner for parser-managed match/game fields.
Match Journal service/repository own local human annotations. The FastAPI
local app and React cockpit are access/display/control surfaces only.

## Bridge-Code Status

`stable_bridge`: browser UI -> FastAPI local app facade -> app-owned Match
Journal service/repository.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Current Behavior Compared To Contract

The repo already had browser-facing `/api/journal/...` facade routes from the
first cockpit UI slice. Those routes preserved compact responses, rejected
pilot-error routes, and kept the frontend pointed at the FastAPI local app
facade instead of direct `status_api.py` journal endpoints.

The remaining contract gaps were:

- normal `create_app(...)` journal routes failed closed unless tests injected a
  service factory;
- no app-owned local Match Journal SQLite path existed in `LocalAppPaths`;
- setup/status did not expose Match Journal write readiness;
- focused tests did not prove first-write initialization, injected-factory
  override, read-without-initialization, or generated-artifact boundaries;
- setup UI validation/display did not know about Match Journal readiness.

## Implementation Option Chosen

Use an app-owned Match Journal database at
`<app_data>\db\match_journal.sqlite3`, accessed through a small local-app
runtime adapter. Journal reads return missing/not found without creating the
database. The first explicit journal write creates only the app-owned Match
Journal database path and applies packaged Match Journal migrations.

This keeps setup/status read-only, preserves test injection, and avoids using
analytics SQLite tables or repo-local generated database paths.

## What Changed

- Added app-owned Match Journal database path support under the local app data
  root.
- Added `LocalAppMatchJournalService`, a per-operation adapter over the
  existing Match Journal service/repository.
- Wired normal FastAPI `create_app(...)` journal routes to the app-owned
  service factory, while preserving explicit test injection override.
- Added Match Journal setup/status readiness with symbolic paths only.
- Aligned safe journal context fields with the contract:
  `journal_match_id`, `journal_game_id`, `parser_match_id`, `parser_game_id`,
  `game_number`, and `attachment_status`.
- Updated frontend setup-status validation/display for Match Journal readiness.
- Added focused backend, setup/status, launcher, and frontend tests.

## Files Changed

- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/match_journal_runtime.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/match_journal_cockpit.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `tests/test_match_journal_cockpit_ui_backend.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`
- `tests/test_analytics_dev_app_launcher.py`
- `docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md`

Untracked source contract left in place:

- `docs/contracts/match_journal_cockpit_write_controls.md`

## Code Changed

Runtime code changed inside the contracted Local App / UI area.

- `build_local_app_paths(...)`: now exposes
  `LocalAppPaths.match_journal_database`.
- `create_app(...)`: now builds local app paths once and uses default
  app-owned Match Journal service wiring unless an injected factory is passed.
- `match_journal_cockpit.py`: now accepts the contract-approved safe context
  fields and treats journal IDs as valid attachment references.
- `match_journal_runtime.py`: new helper module for app-owned Match Journal
  service creation and setup/status inspection.
- `build_setup_status(...)`: now includes a `match_journal` section and
  `match_journal_write_controls` capability.
- Frontend setup/status validation and UI panels now include Match Journal
  readiness.

No parser behavior, parser state reconciliation, analytics schema/migrations,
workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
behavior, OpenAI/model-provider behavior, AI/coaching behavior, or production
behavior was changed.

## Tests Added Or Updated

- `tests/test_match_journal_cockpit_ui_backend.py`
  - proves route inventory still excludes pilot-error/delete controls;
  - proves loopback-only CORS remains on the FastAPI facade;
  - proves injected service factory override still fails closed;
  - proves default journal reads report missing without creating app-data;
  - proves first explicit write creates only
    `<app_data>\db\match_journal.sqlite3`;
  - proves compact write responses and sanitized failures;
  - proves contract-safe journal context references are accepted.
- `tests/test_analytics_local_app_backend.py`
  - verifies setup/status exposes Match Journal readiness with symbolic path
    and `enabled_on_first_write`.
- `tests/test_analytics_local_app_config.py`
  - verifies Match Journal status reports not initialized without creating DB
    files;
  - verifies status reads schema metadata read-only.
- `tests/test_analytics_dev_app_launcher.py`
  - verifies launcher start mode does not create the Match Journal DB.
- `frontend/src/api.test.ts`
  - verifies setup-status validation includes Match Journal;
  - verifies journal context fields serialize through `/api/journal`.
- `frontend/src/App.test.tsx`
  - verifies Match Journal setup/status path is visible.

## Interface Changes

- `LocalAppPaths` now has `match_journal_database: Path | None`.
- Setup/status response now includes a `match_journal` section.
- Setup/status capabilities now include `match_journal_write_controls`.
- Frontend `SetupStatusResponse` now requires `match_journal`.
- Frontend `MatchJournalContext` now includes optional
  `journal_match_id`, `journal_game_id`, and `attachment_status`.

No route inventory expansion occurred. The only browser-facing journal routes
remain:

- `GET /api/journal`
- `POST /api/journal/notes`
- `POST /api/journal/opponent-labels`
- `POST /api/journal/review-flags`
- `POST /api/journal/experiment-label`
- `POST /api/journal/display-corrections`

## Contracted Area Status

Implementation stayed inside the contracted Local App / UI and focused test
surfaces. Match Journal rows remain local annotations, not parser truth,
analytics truth, workbook truth, gameplay advice, hidden-card inference,
archetype truth, player-mistake truth, Line Tracer truth, or AI/coaching
truth.

## Generated Artifact Status

Focused tests created only pytest temporary SQLite files under temporary test
directories. Frontend build produced ignored `frontend/dist` output during
validation; that output was removed after the build. Git status shows no
tracked or untracked SQLite database files, SQLite sidecars, raw logs, local
JSONL artifacts, runtime logs, failed posts, workbook exports, secrets, or
local-only artifacts from this slice.

## Live-Browser Smoke Procedure And Status

Manual live-browser smoke was not run in this Codex C pass.

Suggested disposable smoke procedure for Codex E or a later manual check:

1. Start the local app with a disposable app-data root, not the user's real
   local app data.
2. Open the React app at the local Vite URL.
3. Confirm setup/status shows Match Journal readiness using only
   `<app_data>\db\match_journal.sqlite3`.
4. Submit a synthetic unattached journal note or a note tied to synthetic
   journal/parser IDs.
5. Confirm the write succeeds through `/api/journal/...`.
6. Confirm failed/unavailable writes preserve form values.
7. Confirm no pilot-error, delete, reset, raw SQL, import, export, sync, or
   direct status API write controls appear.

## Validation Run

```powershell
git status --short --branch
# ## codex/analytics-foundation...origin/codex/analytics-foundation
# modified #234 implementation files and untracked contract/runtime helper

py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
# 12 passed, 1 Starlette/FastAPI testclient deprecation warning

py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
# 23 passed, 1 Starlette/FastAPI testclient deprecation warning

py -m pytest -q tests\test_match_journal_service.py tests\test_match_journal_repository.py tests\test_match_journal_schema.py
# 63 passed

py -m pytest -q tests\test_analytics_dev_app_launcher.py
# 10 passed

npm --prefix frontend test -- --run
# 3 test files passed, 60 tests passed

npm --prefix frontend run typecheck
# passed

npm --prefix frontend run build
# passed; generated frontend/dist output removed afterward

py -m ruff check src tests tools
# passed

git diff --check
# passed

py tools\check_agent_docs.py
# passed

@'
docs/contracts/match_journal_cockpit_write_controls.md
docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/match_journal_cockpit.py
src/mythic_edge_parser/local_app/match_journal_runtime.py
src/mythic_edge_parser/local_app/paths.py
src/mythic_edge_parser/local_app/setup_status.py
frontend/src/App.test.tsx
frontend/src/App.tsx
frontend/src/api.test.ts
frontend/src/api.ts
frontend/src/types.ts
tests/test_analytics_dev_app_launcher.py
tests/test_analytics_local_app_backend.py
tests/test_analytics_local_app_config.py
tests/test_match_journal_cockpit_ui_backend.py
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, forbidden 0, warnings 0

@'
docs/contracts/match_journal_cockpit_write_controls.md
docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/match_journal_cockpit.py
src/mythic_edge_parser/local_app/match_journal_runtime.py
src/mythic_edge_parser/local_app/paths.py
src/mythic_edge_parser/local_app/setup_status.py
frontend/src/App.test.tsx
frontend/src/App.tsx
frontend/src/api.test.ts
frontend/src/api.ts
frontend/src/types.ts
tests/test_analytics_dev_app_launcher.py
tests/test_analytics_local_app_backend.py
tests/test_analytics_local_app_config.py
tests/test_match_journal_cockpit_ui_backend.py
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, forbidden 0, warnings 0

git status --short --branch --untracked-files=all
# modified #234 implementation files and untracked contract/handoff/runtime helper only
```

## Still Unverified

- Manual live-browser smoke with a disposable app-data root.
- Real local app operation against the user's actual local app data root.
- Direct status API global CORS hardening, intentionally deferred.
- Pilot-error browser controls, intentionally deferred.
- Future analytics or Google Sheets consumption of Match Journal rows,
  intentionally out of scope.

## Reviewer Focus

Codex E should pay special attention to:

- whether default journal writes are limited to
  `<app_data>\db\match_journal.sqlite3`;
- whether journal reads and setup/status remain non-creating;
- whether successful write responses stay compact and do not echo note text,
  raw paths, raw SQL, raw rows, or secrets;
- whether the browser still uses only `/api/journal/...` and never direct
  `status_api.py` journal endpoints;
- whether Match Journal annotations remain local annotations only.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #234.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/234

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Contract:
docs/contracts/match_journal_cockpit_write_controls.md

Implementation handoff:
docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md

Goal:
Review the Codex C implementation against the contract. Lead with findings ordered by severity. Verify that browser-facing Match Journal write controls are safely wired through the FastAPI local app facade, use only the app-owned Match Journal database path, preserve compact/sanitized responses, preserve setup/status read-only behavior, and do not cross protected surfaces.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/review.md
- docs/contracts/match_journal_cockpit_write_controls.md
- docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/match_journal_cockpit.py
- src/mythic_edge_parser/local_app/match_journal_runtime.py
- src/mythic_edge_parser/local_app/paths.py
- src/mythic_edge_parser/local_app/setup_status.py
- frontend/src/api.ts
- frontend/src/types.ts
- frontend/src/App.tsx
- tests/test_match_journal_cockpit_ui_backend.py
- tests/test_analytics_local_app_backend.py
- tests/test_analytics_local_app_config.py
- tests/test_analytics_dev_app_launcher.py
- frontend/src/api.test.ts
- frontend/src/App.test.tsx

Review focus:
- Confirm normal create_app(...) journal writes work without injected service factories.
- Confirm injected match_journal_service_factory still overrides default wiring.
- Confirm setup/status and journal reads do not create Match Journal DB files.
- Confirm the first explicit journal write creates only <app_data>\db\match_journal.sqlite3 and not analytics DB tables.
- Confirm successful write responses remain compact and do not expose note text, full records, raw rows, raw paths, raw SQL, raw payloads, or secrets.
- Confirm failure responses are sanitized and failed writes do not discard frontend form values.
- Confirm no pilot-error, destructive, raw SQL, import/export/sync, database init/reset, or direct status API browser write controls were added.
- Confirm direct status API CORS policy was not changed.
- Confirm parser/runtime/workbook/webhook/App Script/Sheets/analytics truth/OpenAI/AI/coaching/production behavior was not changed.

Suggested validation:
git status --short --branch
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_match_journal_service.py tests\test_match_journal_repository.py tests\test_match_journal_schema.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py
npm --prefix frontend test -- --run
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
Run path-scoped protected-surface and secret/private-marker scans over changed files.
Optionally run a live-browser smoke with a disposable app-data root; if not run, leave it clearly unverified.

Do not stage, commit, push, open a PR, merge, close issue #234, or mark tracker #202 complete unless explicitly asked.

Final output must include findings first, validation run, protected-surface status, generated/private artifact status, whether live-browser smoke was run, next recommended role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/234"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/match_journal_cockpit_write_controls.md"
  target_artifact: "docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_match_journal_cockpit_ui_backend.py -> passed"
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py tests\\test_analytics_local_app_config.py -> passed"
    - "py -m pytest -q tests\\test_match_journal_service.py tests\\test_match_journal_repository.py tests\\test_match_journal_schema.py -> passed"
    - "py -m pytest -q tests\\test_analytics_dev_app_launcher.py -> passed"
    - "npm --prefix frontend test -- --run -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run build -> passed, generated frontend/dist removed afterward"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "git status --short --branch --untracked-files=all -> modified #234 files and untracked contract/handoff/runtime helper only"
  remaining_unverified:
    - "manual live-browser smoke with disposable app-data root"
    - "real local app operation against user app-data root"
    - "direct status API global CORS hardening, deferred"
    - "pilot-error browser controls, deferred"
  stop_conditions:
    - "Do not target main."
    - "Do not change direct status API CORS policy in this slice."
    - "Do not expose direct browser writes to status_api.py journal endpoints."
    - "Do not add pilot-error browser controls."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/analytics truth/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/local artifacts or secrets."
```
