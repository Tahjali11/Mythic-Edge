# Analytics App Play/Draw And Postboard Split Views Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/229

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/analytics_app_play_draw_postboard_split_views.md`

## Internal Project Area

Local App / UI.

## Truth Owner

Parser/state remains the truth owner for match facts, game facts, result facts,
play/draw labels, pre/postboard labels, match/game identity, deduplication, and
final reconciliation. SQLite analytics remains downstream local storage. The
derived SQL views remain deterministic read-only projections. The local app
backend and frontend added here are fixed read-only review/display surfaces.

## Bridge-Code Status

`bridge_code`

Source internal project area: Analytics.

Consuming internal project area: Local App / UI.

Allowed data flow: SQLite analytics split views to fixed local backend
responses to frontend display.

Forbidden reverse-flow preserved: no frontend/backend write-back, parser fact
changes, analytics ingest changes, workbook/runtime updates, Line Tracer,
coaching, causation, hidden-card, archetype, player-mistake, or best-line
claims.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

Branch confirmed: `codex/analytics-foundation`.

Initial status before implementation:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
?? docs/contracts/analytics_app_play_draw_postboard_split_views.md
```

The untracked contract artifact came from Codex B and was used as the source
contract. It was not rewritten by this pass.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_app_play_draw_postboard_split_views.md`
- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_local_app_backend.py`
- adjacent local app backend tests for match/game, early-game, and action review
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `frontend/package.json`
- `frontend/vite.config.ts`

GitHub issue checks:

- Issue #229: open
- Tracker #204: open
- Umbrella issue #207: open

## Current Behavior Compared To Contract

Before this pass, the repo already had:

- read-only local app safety patterns for match/game history, early-game
  history, and action review
- fixed `limit`/`offset` pagination validation with stable HTTP 422 errors for
  malformed, duplicate, out-of-range, or unapproved query parameters
- symbolic analytics database display paths
- SQLite views `v_play_draw_splits`, `v_sample_size_warnings`, and
  `v_game1_vs_postboard`
- derived-view tests covering the underlying SQL behavior
- frontend response validation and read-only display patterns for previous
  analytics sections

Remaining gap:

- no backend route exposed play/draw split review rows
- no backend route exposed game 1/postboard split review rows
- no frontend types/API/display existed for the split review responses
- no focused backend/frontend tests covered safe split review responses,
  sample-size warning display, unknown/unavailable/degraded/conflict counts,
  malformed query parameters, malformed frontend responses, or read-only UI
  boundaries for this slice

## Implementation Option Chosen

Implemented the narrow contract option:

- add fixed read-only backend builders over `v_play_draw_splits`,
  `v_sample_size_warnings`, and `v_game1_vs_postboard`
- reuse the existing local app database status, symbolic path, pagination, and
  safe payload helpers
- extend the existing history payload helper only enough to support
  endpoint-specific summaries
- add exact backend routes and route inventory entries
- add typed frontend fetch/validation functions and a read-only Split Review
  section using existing analytics history visual patterns
- add synthetic temp-database tests only

No fallback query to `game_results` was needed. No schema, migration, view,
ingest, parser, workbook, webhook, Apps Script, Sheets, AI, or production
behavior changed.

## Files Changed

- `docs/implementation_handoffs/analytics_app_play_draw_postboard_split_views_comparison.md`
  - this handoff
- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_app_play_draw_postboard_split_views.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`

Source artifact present but not modified by Codex C:

- `docs/contracts/analytics_app_play_draw_postboard_split_views.md`

## Exact Backend Sections Changed

`src/mythic_edge_parser/local_app/analytics_history.py`

- added `SPLIT_REVIEW_SCHEMA_VERSION`
- added `PLAY_DRAW_SPLIT_REVIEW_OBJECT`
- added `GAME1_POSTBOARD_SPLIT_REVIEW_OBJECT`
- added `build_play_draw_split_review()`
- added `build_game1_postboard_split_review()`
- extended `_build_history()` and `_payload()` with optional custom summary
  support
- added play/draw split row mapping and summary rollup
- added game 1/postboard split row mapping and summary rollup
- added `_int_value()` for numeric summary coercion from SQLite rows
- added fixed `_PLAY_DRAW_SPLIT_REVIEW_QUERY` over only
  `v_play_draw_splits` and `v_sample_size_warnings`
- added fixed `_GAME1_POSTBOARD_SPLIT_REVIEW_QUERY` over only
  `v_game1_vs_postboard`

`src/mythic_edge_parser/local_app/backend.py`

- added `GET /api/analytics/play-draw-splits`
- added `GET /api/analytics/game1-postboard-splits`
- both routes reuse `_history_pagination()` and `build_local_app_paths()`

## Exact Frontend Sections Changed

`frontend/src/types.ts`

- added split review schema/object constants
- added play/draw split summary, row, and response types
- added game 1/postboard split summary, row, and response types

`frontend/src/api.ts`

- added endpoint paths for the two split review routes
- added `fetchPlayDrawSplitReview()`
- added `fetchGame1PostboardSplitReview()`
- added split review response validation for object, schema version, summary,
  pagination, database, rows, warnings, and errors
- validation fails closed through `AnalyticsHistoryApiError`

`frontend/src/App.tsx`

- added split review fetch props and state
- added initial load and refresh behavior for the two split endpoints
- added `Split Review` read-only section
- added summary panels for play/draw and game 1/postboard summaries
- added read-only tables for play/draw rows and game 1/postboard rows
- added safe display helpers for numeric table cells and win-rate/duration
  labels
- kept split copy descriptive and non-causal

## Exact Test Sections Changed

`tests/test_analytics_app_play_draw_postboard_split_views.py`

- added missing-database tests that verify no app-data artifact is created
- added empty schema-current database tests
- added play/draw split success coverage for sample warnings, unknown counts,
  unavailable counts, degraded counts, deterministic order, and win-rate
  behavior over known win/loss rows
- added game 1/postboard success coverage for status/provenance objects,
  nonstandard result labels, null turn/duration values, unavailable rows, and
  conflict rows
- added unknown-schema degradation coverage
- added invalid/broken database safe-error coverage
- added malformed, duplicate, out-of-range, and unapproved query parameter
  rejection coverage

`tests/test_analytics_local_app_backend.py`

- added the two new routes to the read-only endpoint inventory

`frontend/src/api.test.ts`

- added split review fetch/validation tests
- added malformed split review response tests for schema, object, summary, and
  rows

`frontend/src/App.test.tsx`

- added Split Review render/refresh test
- added empty/degraded split review state test
- added malformed split review error display test
- added no-destructive-control and no-coaching/Line-Tracer/causation copy
  assertions

## Interface Changes

New backend endpoints:

- `GET /api/analytics/play-draw-splits`
- `GET /api/analytics/game1-postboard-splits`

Allowed query parameters remain only:

- `limit`
- `offset`

New response schema:

- `schema_version: analytics_app_play_draw_postboard_split_views.v1`

New response objects:

- `mythic_edge_local_app_play_draw_split_review`
- `mythic_edge_local_app_game1_postboard_split_review`

No workbook columns, webhook payload fields, parser event shapes, SQLite
schema/migration definitions, environment variables, CI gates, or database
imports changed.

## Whether Code Changed

Code changed in the local app backend/frontend surfaces authorized by the
contract.

Tests changed in focused backend/frontend tests authorized by the contract.

Docs changed only by adding this implementation handoff. The source contract
artifact was left as provided.

## Validation Run

```text
git branch --show-current -> codex/analytics-foundation
git status --short --branch -> ## codex/analytics-foundation...origin/codex/analytics-foundation plus intended #229 files and the untracked source contract
gh issue view 229 --json number,state,title,url -> OPEN
gh issue view 204 --json number,state,title,url -> OPEN
gh issue view 207 --json number,state,title,url -> OPEN
py -m pytest -q tests\test_analytics_app_play_draw_postboard_split_views.py tests\test_analytics_local_app_backend.py -> 33 passed, 1 existing FastAPI/Starlette warning
py -m pytest -q tests\test_analytics_app_play_draw_postboard_split_views.py tests\test_analytics_app_gameplay_action_opponent_observation_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py -> 92 passed, 1 existing FastAPI/Starlette warning
py -m pytest -q tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py tests\test_analytics_schema.py -> 22 passed
py -m ruff check src tests tools -> passed
npm --prefix frontend run typecheck -> passed
npm --prefix frontend run test -- --run src/api.test.ts src/App.test.tsx -> 49 passed
npm --prefix frontend run test -- --run -> 52 passed
npm --prefix frontend run build -> passed
frontend/dist cleanup -> removed generated build output after validation
git diff --check -> passed
py tools\check_agent_docs.py -> passed
path-scoped protected-surface scan over contract, handoff, backend, frontend, and tests -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan over contract, handoff, backend, frontend, and tests -> passed, forbidden 0, warnings 0
direct ASCII/trailing-whitespace/final-newline checks for new contract, handoff, and test file -> passed
git status --short --ignored frontend\dist data\analytics data\status data\runtime_logs data\failed_posts -> no frontend/dist, no data/analytics; ignored pre-existing data/status, data/runtime_logs, and data/failed_posts directories present
Browser smoke check on loopback temp app-data backend and Vite frontend -> Setup Status and Split Review rendered; Refresh Splits present; empty split states shown; no destructive buttons
temporary loopback backend/frontend servers -> stopped after smoke check
```

## Protected-Surface Status

Path-scoped protected-surface scan passed with forbidden 0 and warnings 0.

No protected parser/runtime/workbook/webhook/App Script/Sheets/AI/production
surface was touched.

Touched implementation surfaces are limited to:

- local app backend route/response code
- local app frontend display/API/types
- focused tests
- implementation handoff documentation

## Secret And Private-Marker Status

Path-scoped secret/private-marker scan passed with forbidden 0 and warnings 0.

The implementation uses synthetic test identifiers and temp directories only.
Endpoint and frontend displays use symbolic database paths and stable error
codes. No raw Player.log payloads, raw JSONL contents, raw hashes, webhook
URLs, secrets, credentials, stack traces, local usernames, or absolute private
paths were added.

## Generated Artifact Status

`npm --prefix frontend run build` generated ignored `frontend/dist/` output as
part of validation. The generated `frontend/dist/` directory was verified
inside the repo and removed before final status checks.

No generated SQLite database file, WAL file, SHM file, journal file, raw log,
raw JSONL artifact, runtime status file, failed-post payload, workbook export,
or local-only artifact is intended for staging.

Final generated-artifact status check showed no `frontend/dist` and no
`data/analytics` output. Ignored `data/status`, `data/runtime_logs`, and
`data/failed_posts` directories are present as pre-existing local generated
surfaces and were not touched by this slice.

## Contracted Boundaries Preserved

- no arbitrary SQL input
- no database browsing endpoint
- no destructive database route
- no destructive UI control
- no schema/migration/view/ingest change
- no parser behavior change
- no parser final reconciliation change
- no parser event class, match/game identity, or deduplication change
- no workbook schema, webhook payload, Apps Script, Sheets, or transport change
- no Match Journal, Line Tracer, OpenAI/model-provider, AI/coaching, or
  production behavior change
- no sample-size significance, coaching, causation, hidden-card inference,
  archetype inference, player-mistake label, or best-line recommendation added

## What Remains Unverified

- live workbook state
- deployed Apps Script state
- production behavior
- browser smoke test against a populated real local analytics database
- future split filters by match, format, queue, event, date, matchup, or notes
- future Line Tracer/opening-line/coaching surfaces, which remain deferred and
  out of scope

## Forbidden Scope Touched

No forbidden scope was touched.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #229.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/229

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_play_draw_postboard_split_views.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_play_draw_postboard_split_views_comparison.md

Goal:
Review Codex C's implementation against the contract. Lead with findings. Confirm the new split review endpoints and frontend display are fixed, read-only, descriptive, and scoped only to v_play_draw_splits, v_sample_size_warnings, and v_game1_vs_postboard.

Review focus:
- Verify GET /api/analytics/play-draw-splits and GET /api/analytics/game1-postboard-splits return the approved object names, schema version, top-level shape, row shape, summaries, status behavior, and symbolic database path.
- Verify backend queries are fixed and parameterized, allow only limit/offset, reject malformed/duplicate/out-of-range/unapproved query params safely, and do not expose raw SQL/input/errors/paths.
- Verify the play/draw endpoint preserves wins, losses, unknown, unavailable, degraded, win_rate, and sample_size_warning without treating unknown/unavailable as losses.
- Verify the game 1/postboard endpoint preserves pre_postboard_label, local_result, play_draw, null turn/duration, and game_result_status/provenance without inferring deck-state, causation, sideboard plan, or strategy.
- Verify frontend response validation fails closed for malformed/incompatible responses.
- Verify frontend copy/actions stay read-only and descriptive, with no arbitrary SQL, destructive controls, import controls inside split review, Line Tracer, coaching, hidden-card, archetype, player-mistake, best-line, causation, or statistical-significance claims.
- Verify existing setup-status, manual import, browser/folder upload, match/game history, opening-hand, mulligan, gameplay-action, and opponent-observation behavior remains compatible.
- Verify no parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed.
- Verify no analytics schema, migration, derived-view definition, or ingest behavior changed.
- Verify generated/private/runtime artifacts are not staged or left as intended files.

Suggested validation:
git status --short --branch
git diff --check
py -m pytest -q tests\test_analytics_app_play_draw_postboard_split_views.py tests\test_analytics_app_gameplay_action_opponent_observation_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py tests\test_analytics_schema.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation

Do not:
- change implementation unless routing concrete findings to Codex D
- target main
- stage, commit, push, open a PR, merge, close issue #229, or mark tracker #204 complete unless explicitly asked
- change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior
- add arbitrary SQL, destructive controls, schema/migration/ingest changes, Line Tracer, coaching, causation, hidden-card, archetype, player-mistake, best-line, or statistical-significance claims

Final response must include findings first, validation run, protected-surface status, generated/private artifact status, whether the module is ready for Codex F or needs Codex D, and a workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/229"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/analytics_app_play_draw_postboard_split_views.md"
  artifact_produced: "docs/implementation_handoffs/analytics_app_play_draw_postboard_split_views_comparison.md"
  branch: "codex/analytics-foundation"
  risk_tier: "High"
  validation:
    - "py -m pytest -q tests\\test_analytics_app_play_draw_postboard_split_views.py tests\\test_analytics_local_app_backend.py -> 33 passed, 1 existing FastAPI/Starlette warning"
    - "py -m pytest -q tests\\test_analytics_app_play_draw_postboard_split_views.py tests\\test_analytics_app_gameplay_action_opponent_observation_views.py tests\\test_analytics_app_opening_hand_mulligan_views.py tests\\test_analytics_app_match_game_history_views.py tests\\test_analytics_local_app_backend.py -> 92 passed, 1 existing FastAPI/Starlette warning"
    - "py -m pytest -q tests\\test_analytics_derived_views.py tests\\test_analytics_replay_view_harness.py tests\\test_analytics_schema.py -> 22 passed"
    - "py -m ruff check src tests tools -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run src/api.test.ts src/App.test.tsx -> 49 passed"
    - "npm --prefix frontend run test -- --run -> 52 passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed afterward"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "direct ASCII/trailing-whitespace/final-newline checks for new contract, handoff, and test -> passed"
    - "browser smoke check on loopback temp app-data backend and Vite frontend -> Setup Status and Split Review rendered; no destructive buttons"
  remaining_unverified:
    - "Codex E contract review"
    - "browser smoke test against populated local analytics data"
    - "live workbook state"
    - "deployed Apps Script state"
    - "production behavior"
  stop_conditions:
    - "Do not target main."
    - "Do not expose arbitrary SQL or destructive database/UI controls."
    - "Do not turn split rows into Line Tracer, coaching, causation, hidden-card, archetype, player-mistake, or best-line truth."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not change analytics schema, migrations, derived SQL views, or ingest behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```
