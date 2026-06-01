# Implementation Handoff: Analytics App Match And Game History Views

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/225

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/analytics_app_match_game_history_views.md`

## Internal Project Area

Local App / UI, with Analytics as the downstream storage/query support layer.

## Truth Owner

Parser/state remains the truth owner for match facts, game facts, match/game
identity, event interpretation, deduplication, and final reconciliation. SQLite
and the local app remain downstream storage/display surfaces.

## Bridge-Code Status

`bridge_code`

Allowed flow: analytics SQLite fact tables -> fixed read-only local backend
responses -> frontend display.

Forbidden reverse flow was preserved: no frontend/backend history behavior
writes back to SQLite, parser state, workbook, runtime, or production surfaces.

## Role Performed

Codex C: Module Implementer / comparison thread.

Codex D addendum: Module Fixer for CT-225-001 and CT-225-002 from
`docs/contract_test_reports/analytics_app_match_game_history_views.md`.

## What Changed

Implemented the first curated read-only local app analytics history slice:

- added fixed `GET /api/analytics/matches` and `GET /api/analytics/games`
  endpoints with only `limit` and `offset`
- added read-only SQLite query helpers over only `matches`, `games`,
  `match_results`, `game_results`, and `match_context`
- added typed frontend API validation for the history response schema
- replaced the deferred Analytics Views panel with read-only match/game history
  summary and compact tables
- added focused backend and frontend tests for success, empty, missing,
  degraded, error, malformed, and read-only boundary behavior

Codex D fixed the contract-test findings:

- CT-225-001: moved `limit` and `offset` validation out of FastAPI's default
  integer parser and into a sanitized route-local validation path so malformed
  query values are rejected without echoing raw private input.
- CT-225-002: constrained frontend history response status labels to the
  contract's allowed labels before they can be displayed.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_app_match_game_history_views.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_schema.py`
- `tests/test_analytics_derived_views.py`

## Current Behavior Compared To Contract

Before this pass, the backend exposed setup/status, import/upload, job-status,
runtime-status, and database-status routes. It did not expose fixed match/game
history routes.

Before this pass, the frontend rendered setup-status panels and manual JSONL
import/upload flows. It still showed `Analytics Views` as deferred.

The SQLite schema already had the contracted source tables and provenance/status
columns. The gap was the missing fixed read-only API projection, frontend typed
fetch/display layer, and focused test coverage.

## Implementation Option Chosen

Smallest contract-complete implementation:

- new backend helper module rather than changing analytics schema or ingest
- fixed SQL queries with parameterized `LIMIT ? OFFSET ?`
- route-level rejection of query params outside `limit` and `offset`
- frontend response validation that fails closed before rendering rows
- compact read-only tables instead of a generic database browser

## Files Changed

- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_app_match_game_history_views.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md`

The untracked Codex B contract
`docs/contracts/analytics_app_match_game_history_views.md` was used as the
source contract and left unmodified.

## Exact Backend Sections Changed

- `src/mythic_edge_parser/local_app/analytics_history.py`
  - added `HISTORY_SCHEMA_VERSION`,
    `MATCH_HISTORY_OBJECT`, `GAME_HISTORY_OBJECT`
  - added `build_match_history()` and `build_game_history()`
  - added fixed match/game SQL projections
  - added safe database status mapping, pagination, summary counts, status
    object mapping, degraded/unavailable/conflict row counts, and stable error
    handling
- `src/mythic_edge_parser/local_app/backend.py`
  - added imports for `build_match_history` and `build_game_history`
  - added `GET /api/analytics/matches`
  - added `GET /api/analytics/games`
  - added `_reject_unknown_history_query_params()`
  - Codex D removed FastAPI default integer parsing for history pagination and
    added sanitized `_history_pagination()` / `_history_query_int()`
    validation.

## Exact Frontend Sections Changed

- `frontend/src/types.ts`
  - added history constants, error code type, status object type, database,
    pagination, summary, match row, game row, and response types
  - Codex D added the `AnalyticsHistoryStatus` allowed-label type.
- `frontend/src/api.ts`
  - added `AnalyticsHistoryApiError`
  - added `fetchMatchHistory()` and `fetchGameHistory()`
  - added schema/object/row validation for history responses
  - Codex D added top-level history status-label validation.
- `frontend/src/status.ts`
  - added `empty` tone mapping
- `frontend/src/App.tsx`
  - added history fetch state and refresh behavior
  - added read-only Analytics History section, summaries, and tables
  - removed the deferred Analytics Views panel
  - preserved setup status, manual import, browser upload, folder upload, and
    Live Watcher deferred display
- `frontend/src/App.css`
  - added Analytics History layout, summary, table, refresh button, and
    `tone-empty` styling

## Exact Test Sections Changed

- `tests/test_analytics_app_match_game_history_views.py`
  - added focused backend tests for missing DB, empty current DB, match success,
    game success, unknown schema degradation, invalid/broken DB errors, and
    unapproved query param rejection
  - Codex D added malformed, duplicate, and out-of-bounds pagination tests that
    prove raw private query values are not echoed.
- `tests/test_analytics_local_app_backend.py`
  - added the two new history endpoints to the route inventory
- `frontend/src/api.test.ts`
  - added history fetch/validation tests and malformed/incompatible response
    tests
  - Codex D added unsupported/private-marker history status validation tests.
- `frontend/src/App.test.tsx`
  - added read-only history render/refresh test
  - added empty/degraded history-state test
  - added malformed history-response display test

## Code Changed

Yes. The changed code is limited to local app backend/API helpers and local app
frontend display/API validation.

## Tests Changed

Yes. Focused backend and frontend tests were added/updated.

## Interface Changes

Added local app read-only HTTP endpoints:

- `GET /api/analytics/matches`
- `GET /api/analytics/games`

Both accept only:

- `limit`: optional integer, default `50`, minimum `1`, maximum `100`
- `offset`: optional integer, default `0`, minimum `0`

Added frontend API helpers:

- `fetchMatchHistory()`
- `fetchGameHistory()`

No SQLite schema, migration, parser, workbook, webhook, Apps Script, Sheets,
AI, Line Tracer, coaching, production, or environment-variable contract changed.

## Contracted Area Status

Stayed inside Local App / UI and Analytics bridge-code scope. The new backend
queries only the contracted tables and only through fixed read-only projections.

## Validation Run

```text
git status --short --branch -> branch codex/analytics-foundation; source contract and new files visible as local changes
py -m pytest -q tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py -> 26 passed, 1 StarletteDeprecationWarning
py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_browser_jsonl_upload.py -> 25 passed, 1 StarletteDeprecationWarning
py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py -> 22 passed
py -m ruff check src tests tools -> All checks passed
npm --prefix frontend run typecheck -> passed
npm --prefix frontend run test -- --run -> 3 files passed, 37 tests passed
npm --prefix frontend run build -> passed
```

Final checks:

```text
git diff --check -> passed
py tools\check_agent_docs.py -> passed, errors 0, warnings 0
path-scoped protected-surface scan over tracked changes plus untracked source contract/handoff/helper/test files -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan over tracked changes plus untracked source contract/handoff/helper/test files -> passed, forbidden 0, warnings 0
generated artifact status check -> ignored frontend/dist, data/status, data/runtime_logs, and data/failed_posts visible; no tracked generated artifacts added
```

## Protected-Surface Status

No parser behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema/migrations, analytics
ingest, workbook schema, webhook payload shape, Apps Script behavior, Sheets
behavior, AI/OpenAI behavior, Line Tracer, coaching, production behavior, or CI
gates were intentionally touched.

## Generated/Private Artifact Status

No repo-local SQLite database file, WAL file, SHM file, journal file, raw log,
raw JSONL artifact, runtime artifact, failed post, workbook export, secret, or
local-only artifact was intentionally created or committed. Frontend build
output remained ignored.

## Still Unverified

- Live local app browser rendering against a real operator database
- Live workbook state
- Deployed Apps Script state
- Production behavior
- Future richer analytics surfaces such as opening hands, mulligans, gameplay
  actions, opponent observations, derived dashboards, Match Journal, AI, and
  coaching

## Reviewer Focus

Ask Codex E to verify:

- the fixed SQL queries touch only contracted tables
- malformed `limit` and `offset` values return stable sanitized 422 responses
  without echoing private input
- missing/degraded/error handling does not create or mutate DB files
- frontend history response validation rejects unsupported/private-marker
  top-level status labels
- frontend validation fails closed before rendering incompatible rows
- no raw path, raw payload, raw hash, SQL, stack trace, or secret is exposed
- no destructive import/database/job/UI controls were added
- setup-status, manual import, browser upload, and folder upload behavior stayed
  compatible

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #225.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/225

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_match_game_history_views.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md

Goal:
Review the Codex C implementation against the contract. Verify the first
read-only curated match/game history local app view, backend endpoints,
frontend display, tests, privacy boundaries, and protected-surface boundaries.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/contract_test.md
- docs/agent_threads/review.md
- docs/contracts/analytics_app_match_game_history_views.md
- docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md
- src/mythic_edge_parser/local_app/analytics_history.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_app_match_game_history_views.py
- tests/test_analytics_local_app_backend.py
- frontend/src/api.ts
- frontend/src/types.ts
- frontend/src/status.ts
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/api.test.ts
- frontend/src/App.test.tsx

Review focus:
- Confirm GET /api/analytics/matches and GET /api/analytics/games match the approved schema and object names.
- Confirm only limit and offset query params are accepted.
- Confirm backend SQL is fixed, parameterized, read-only, and limited to matches, games, match_results, game_results, and match_context.
- Confirm missing DB, empty current DB, degraded/unknown schema, invalid DB, and query-failure behavior is safe and stable.
- Confirm frontend response validation fails closed on malformed or incompatible responses.
- Confirm the frontend replaced the deferred Analytics Views panel with a read-only match/game history section.
- Confirm no raw payloads, raw hashes, absolute/private paths, stack traces, SQL text, local usernames, credentials, secrets, or local artifacts are exposed.
- Confirm no destructive import/database/job/UI controls were added.
- Confirm setup-status, manual import, browser upload, and folder upload behavior remained compatible.
- Confirm no parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed.

Suggested validation:
git status --short --branch
py -m pytest -q tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation

Do not:
- edit implementation files unless explicitly asked
- stage, commit, push, open a PR, merge, close issue #225, or mark tracker #204 complete
- change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior
- change analytics schema, migrations, ingest behavior, fixtures, snapshots, generated DB files, raw logs, runtime artifacts, or local-only artifacts

Output:
- findings first, ordered by severity
- contract-test verdict
- validation run and result
- remaining risks or unverified layers
- protected-surface and secret/private-marker status
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/225"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/analytics_app_match_game_history_views.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md"
  review_artifact: "docs/contract_test_reports/analytics_app_match_game_history_views.md"
  target_artifact: "docs/contract_test_reports/analytics_app_match_game_history_views.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  findings_fixed:
    - "CT-225-001 P1: malformed limit/offset query values can echo raw private input through FastAPI default 422 responses."
    - "CT-225-002 P2: frontend validation accepts arbitrary history status labels that are later displayed directly."
  validation:
    - "py -m pytest -q tests\\test_analytics_app_match_game_history_views.py tests\\test_analytics_local_app_backend.py -> 26 passed"
    - "py -m pytest -q tests\\test_analytics_manual_jsonl_import.py tests\\test_analytics_browser_jsonl_upload.py -> 25 passed"
    - "py -m pytest -q tests\\test_analytics_schema.py tests\\test_analytics_derived_views.py tests\\test_analytics_replay_view_harness.py -> 22 passed"
    - "py -m ruff check src tests tools -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> 37 passed"
    - "npm --prefix frontend run build -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated artifact status check -> ignored local/generated directories visible; no tracked generated artifacts added"
  forbidden_scope_touched: false
  stop_conditions:
    - "Do not target main."
    - "Do not add arbitrary SQL, generic database browsing, or destructive controls."
    - "Do not change analytics schema, migrations, or ingest behavior."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```
