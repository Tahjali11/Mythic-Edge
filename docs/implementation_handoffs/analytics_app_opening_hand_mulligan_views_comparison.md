# Implementation Handoff: Analytics App Opening Hand And Mulligan Views

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/226

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

Completed prerequisite: https://github.com/Tahjali11/Mythic-Edge/issues/225

## Contract

`docs/contracts/analytics_app_opening_hand_mulligan_views.md`

## Internal Project Area

Local App / UI, with Analytics as the downstream storage/query support layer.

## Truth Owner

Parser/state remains the truth owner for opening hand facts, mulligan facts,
match/game identity, event interpretation, deduplication, and final
reconciliation. SQLite and the local app remain downstream storage/display
surfaces.

## Bridge-Code Status

`bridge_code`

Allowed flow: analytics SQLite early-game fact tables -> fixed read-only local
backend responses -> frontend display.

Forbidden reverse flow was preserved: no frontend/backend early-game behavior
writes back to SQLite, parser state, workbook, runtime, AI, coaching, or
production surfaces.

## Role Performed

Codex C: Module Implementer / comparison thread.

## What Changed

Implemented the read-only early-game local app history slice:

- added fixed `GET /api/analytics/opening-hands` and
  `GET /api/analytics/mulligans` endpoints with only `limit` and `offset`
- added grouped read-only SQLite query helpers over opening-hand and mulligan
  parent rows, with child card arrays fetched by selected parent ids
- added typed frontend API validation for the early-game response schema
- added a read-only Early Game History section adjacent to Analytics History
- added focused backend and frontend tests for success, empty, missing,
  degraded, query-failure, malformed-query, response-validation, safe-display,
  and read-only-boundary behavior

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_app_opening_hand_mulligan_views.md`
- `docs/contracts/analytics_app_match_game_history_views.md`
- `docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md`
- `docs/contract_test_reports/analytics_app_match_game_history_views.md`
- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_app_match_game_history_views.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_schema.py`
- `tests/test_analytics_derived_views.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `frontend/src/status.ts`

## Current Behavior Compared To Contract

Before this pass, the local app exposed fixed read-only match/game history
through #225. The backend did not expose `GET /api/analytics/opening-hands` or
`GET /api/analytics/mulligans`, and the frontend did not display opening hand
or mulligan history.

The SQLite schema already had the contracted source tables and status columns:
`opening_hands`, `opening_hand_cards`, `mulligan_events`,
`mulligan_bottomed_or_discarded_cards`, `games`, `game_results`,
`match_results`, and `match_context`. The gap was the missing fixed read-only
backend projection, frontend typed fetch/display layer, and focused tests.

## Implementation Option Chosen

Smallest contract-complete implementation:

- extend the existing #225 `analytics_history.py` helper instead of adding a
  new module
- query parent rows with fixed read-only SQL and paginate those parent rows
- query child card rows only for the selected parent ids with parameterized
  `IN` clauses
- preserve parent rows with zero child card rows as `cards: []`
- add a sibling Early Game History section instead of mixing import controls
  into the review display

## Files Changed

- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_app_opening_hand_mulligan_views.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_app_opening_hand_mulligan_views_comparison.md`

Source contract used and left otherwise unmodified:

- `docs/contracts/analytics_app_opening_hand_mulligan_views.md`

## Exact Backend Sections Changed

- `src/mythic_edge_parser/local_app/analytics_history.py`
  - added `EARLY_GAME_HISTORY_SCHEMA_VERSION`,
    `OPENING_HAND_HISTORY_OBJECT`, and `MULLIGAN_HISTORY_OBJECT`
  - added `build_opening_hand_history()` and `build_mulligan_history()`
  - added grouped parent-row history builder with child-card fetching
  - added fixed opening-hand and mulligan parent SQL projections
  - added fixed child-card queries over `opening_hand_cards` and
    `mulligan_bottomed_or_discarded_cards`
  - extended status-summary traversal to include nested child card status
    objects
  - extended payload summaries to include `card_row_count` for early-game
    responses while preserving #225 match/game summary shape
- `src/mythic_edge_parser/local_app/backend.py`
  - imported the new history builders
  - added `GET /api/analytics/opening-hands`
  - added `GET /api/analytics/mulligans`
  - reused the existing sanitized history pagination validator

## Exact Frontend Sections Changed

- `frontend/src/types.ts`
  - added early-game schema/object constants
  - added opening-hand and mulligan row/card/response types
  - added `EarlyGameHistorySummary` with `card_row_count`
- `frontend/src/api.ts`
  - added `fetchOpeningHandHistory()` and `fetchMulliganHistory()`
  - added early-game schema/object validation
  - added opening-hand and mulligan row/card shape validation
  - rejects unsupported mulligan `card_action` labels before display
- `frontend/src/App.tsx`
  - added early-game fetch state, refresh behavior, and safe display counts
  - added read-only Early Game History summary panels and compact tables
  - preserved the existing setup, import, upload, folder-upload, and
    match/game history sections
  - renamed the existing history refresh control to `Refresh History` and
    added `Refresh Early Game`

## Exact Test Sections Changed

- `tests/test_analytics_app_opening_hand_mulligan_views.py`
  - added focused backend tests for missing DB, empty current DB, opening-hand
    grouping, zero-card opening-hand groups, mulligan card grouping, child
    status summaries, unknown schema degradation, fixed-query failure, and
    malformed/duplicate/out-of-range query parameter rejection
- `tests/test_analytics_local_app_backend.py`
  - added the two new early-game endpoints to route inventory
- `frontend/src/api.test.ts`
  - added early-game fetch/validation tests
  - added malformed response and unsupported mulligan card-action tests
- `frontend/src/App.test.tsx`
  - added read-only early-game render/refresh test
  - added empty/degraded and malformed early-game state tests
  - updated the #225 refresh assertion for the renamed history refresh button

## Code Changed

Yes. Runtime code changed only in the local app backend/API helper and local app
frontend display/API validation surfaces.

## Tests Changed

Yes. Focused backend and frontend tests were added/updated.

## Interface Changes

Added local app read-only HTTP endpoints:

- `GET /api/analytics/opening-hands`
- `GET /api/analytics/mulligans`

Both accept only:

- `limit`: optional integer, default `50`, minimum `1`, maximum `100`
- `offset`: optional integer, default `0`, minimum `0`

Added frontend API helpers:

- `fetchOpeningHandHistory()`
- `fetchMulliganHistory()`

Added response schema:

- `schema_version: analytics_app_opening_hand_mulligan_views.v1`
- `object: mythic_edge_local_app_opening_hand_history`
- `object: mythic_edge_local_app_mulligan_history`

No SQLite schema, migration, analytics ingest, parser, workbook, webhook,
Apps Script, Sheets, AI, Line Tracer, coaching, production, or
environment-variable contract changed.

## Contracted Area Status

Stayed inside Local App / UI and Analytics bridge-code scope. The backend
queries only the contracted tables and does not query raw files, raw JSONL,
raw Player.log, `fact_provenance`, rank snapshots, sideboarding/deck-state,
gameplay-action, opponent-observation, annotation, or dashboard-derived views.

## Validation Run

```text
git status --short --branch -> ## codex/analytics-foundation...origin/codex/analytics-foundation; local #226 changes plus untracked #226 contract/handoff/test
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0
gh issue view 226 -> OPEN
gh issue view 204 -> OPEN tracker
gh issue view 207 -> OPEN umbrella
gh issue view 225 -> CLOSED prerequisite
py -m pytest -q tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py -> 47 passed, 1 existing FastAPI/Starlette warning
py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_browser_jsonl_upload.py -> 25 passed, 1 existing FastAPI/Starlette warning
py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py -> 22 passed
py -m ruff check src tests tools -> passed
npm --prefix frontend run typecheck -> passed
npm --prefix frontend run test -- --run -> 42 passed
npm --prefix frontend run build -> passed
frontend/dist cleanup -> removed generated build output
git diff --check -> passed
py tools\check_agent_docs.py -> passed, errors 0, warnings 0
new/untracked file whitespace-ascii-final-newline check -> passed
path-scoped protected-surface scan over touched and untracked #226 files -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan over touched and untracked #226 files -> passed, forbidden 0, warnings 0
generated artifact status check -> ignored data/status, data/runtime_logs, and data/failed_posts already visible; frontend/dist absent; no tracked generated artifacts added
```

## Protected-Surface Status

No parser behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema/migrations, analytics
ingest, workbook schema, webhook payload shape, Apps Script behavior, Sheets
behavior, Match Journal, Line Tracer, AI/OpenAI behavior, coaching, production
behavior, or CI gates were intentionally touched.

## Generated/Private Artifact Status

No repo-local SQLite database file, WAL file, SHM file, journal file, raw log,
raw JSONL artifact, runtime artifact, failed post, workbook export, secret, or
local-only artifact was intentionally created or committed. Frontend build
output was generated by validation and removed.

## Still Unverified

- Live local app browser rendering against a real operator database
- Live workbook state
- Deployed Apps Script state
- Production behavior
- Remote CI
- Future richer analytics surfaces such as gameplay actions, opponent
  observations, derived dashboards, Match Journal, AI, and coaching

## Reviewer Focus

Ask Codex E to verify:

- the fixed backend queries touch only contracted tables
- grouped parent-row pagination happens before child card fetching
- parent rows with zero child cards are preserved with `cards: []`
- nested child card statuses contribute to degraded/unavailable/conflict
  summary counts
- malformed query parameters return stable sanitized 422 responses
- frontend response validation rejects incompatible schema/object/row/card
  shapes before display
- no raw paths, raw payloads, raw hashes, SQL text, stack traces, credentials,
  coaching labels, best-keep labels, player mistake labels, or local artifacts
  are exposed
- no destructive import/database/job/UI controls were added
- setup-status, manual import, browser upload, folder upload, match history,
  and game history behavior stayed compatible

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #226.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/226

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Completed prerequisite:
https://github.com/Tahjali11/Mythic-Edge/issues/225

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_opening_hand_mulligan_views.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_opening_hand_mulligan_views_comparison.md

Goal:
Review the Codex C implementation against the contract. Verify the read-only
opening hand and mulligan local app views, backend endpoints, frontend display,
tests, privacy boundaries, and protected-surface boundaries.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/contract_test.md
- docs/agent_threads/review.md
- docs/contracts/analytics_app_opening_hand_mulligan_views.md
- docs/implementation_handoffs/analytics_app_opening_hand_mulligan_views_comparison.md
- src/mythic_edge_parser/local_app/analytics_history.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_app_opening_hand_mulligan_views.py
- tests/test_analytics_app_match_game_history_views.py
- tests/test_analytics_local_app_backend.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/api.test.ts
- frontend/src/App.test.tsx

Review focus:
- Confirm GET /api/analytics/opening-hands and GET /api/analytics/mulligans match the approved schema and object names.
- Confirm only limit and offset query params are accepted.
- Confirm backend SQL is fixed, parameterized, read-only, and limited to the contract-approved early-game, match/game result, and match context tables.
- Confirm grouped parent rows are paginated before child card rows are fetched.
- Confirm opening hand rows with zero child cards return cards: [].
- Confirm mulligan rows with zero child cards return cards: [].
- Confirm nested child card status objects contribute to degraded/unavailable/conflict summary counts.
- Confirm missing DB, empty current DB, degraded/unknown schema, invalid DB, fixed-query failure states, and malformed query params are safe and stable.
- Confirm frontend response validation fails closed on malformed or incompatible early-game responses.
- Confirm the frontend adds a read-only Early Game History section adjacent to Analytics History.
- Confirm no raw payloads, raw hashes, absolute/private paths, temporary paths, stack traces, SQL text, local usernames, credentials, secrets, coaching labels, best-keep labels, player mistake labels, strategic advice, or local artifacts are exposed.
- Confirm no destructive import/database/job/UI controls were added.
- Confirm setup-status, manual import, browser upload, folder upload, match history, and game history behavior remained compatible.
- Confirm no parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/Line Tracer/OpenAI/AI/coaching/production behavior changed.

Suggested validation:
git status --short --branch
py -m pytest -q tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
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
- stage, commit, push, open a PR, merge, close issue #226, or mark tracker #204 complete
- target main
- add arbitrary SQL, generic database browsing, Line Tracer behavior, coaching, best-keep advice, mulligan mistake labels, hidden-card inference, or destructive controls
- change analytics schema, migrations, or ingest behavior
- change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior
- create or commit generated/private/runtime artifacts or secrets

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
  role_performed: "Codex C: Module Implementer / comparison thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/226"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_prerequisite: "https://github.com/Tahjali11/Mythic-Edge/issues/225"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/analytics_app_opening_hand_mulligan_views.md"
  target_artifact: "docs/implementation_handoffs/analytics_app_opening_hand_mulligan_views_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_analytics_app_opening_hand_mulligan_views.py tests\\test_analytics_app_match_game_history_views.py tests\\test_analytics_local_app_backend.py -> 47 passed"
    - "py -m pytest -q tests\\test_analytics_manual_jsonl_import.py tests\\test_analytics_browser_jsonl_upload.py -> 25 passed"
    - "py -m pytest -q tests\\test_analytics_schema.py tests\\test_analytics_derived_views.py tests\\test_analytics_replay_view_harness.py -> 22 passed"
    - "py -m ruff check src tests tools -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> 42 passed"
    - "npm --prefix frontend run build -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated artifact status check -> ignored local/generated directories visible; frontend/dist absent; no tracked generated artifacts added"
  stop_conditions:
    - "Do not target main."
    - "Do not add arbitrary SQL, generic database browsing, Line Tracer behavior, coaching, or destructive controls."
    - "Do not change analytics schema, migrations, or ingest behavior."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```
