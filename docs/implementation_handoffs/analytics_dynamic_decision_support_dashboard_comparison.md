# Analytics Dynamic Decision Support Dashboard Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Issue And Tracker

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/283
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Branch: `codex/analytics-foundation`
- Risk tier: High

## Contract Used

- `docs/contracts/analytics_dynamic_decision_support_dashboard.md`

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_dynamic_decision_support_dashboard.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_app_play_draw_postboard_split_views.py`
- `tests/test_analytics_app_opening_hand_mulligan_views.py`
- `tests/test_analytics_schema.py`
- `tests/test_analytics_derived_views.py`
- `tests/test_analytics_replay_view_harness.py`
- `frontend/package.json`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`

## Current Behavior Compared To Contract

The contract requires one fixed read-only backend endpoint, exactly three
approved dashboard modules, frontend rendering inside the existing Decision
Support area, bar/table views without a charting dependency, safe browser
storage, and no custom explorer builder UI.

Before this pass, the backend already exposed fixed read-only analytics detail
endpoints and the frontend already rendered a Decision Support section. The
gap was that Decision Support was partly frontend-composed and partly
placeholder-driven. There was no backend-shaped dashboard modules endpoint, no
typed module payload, no per-module bar/table preference storage, and no
focused tests proving the dashboard stayed read-only and non-destructive.

## Implementation Option Chosen

Implemented a narrow backend projection layer in a new local app helper module,
then taught the frontend to fetch and validate that payload. The existing
history, split, opening-hand, mulligan, import, Match Journal, parser,
analytics schema, and ingest behavior were preserved.

## Files Changed

- `src/mythic_edge_parser/local_app/analytics_dashboard.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_dynamic_decision_support_dashboard.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_dynamic_decision_support_dashboard_comparison.md`

The contract file remained untracked from Codex B and was preserved:

- `docs/contracts/analytics_dynamic_decision_support_dashboard.md`

## Exact Sections Changed

Backend:

- Added `build_analytics_dashboard_modules(...)` in
  `src/mythic_edge_parser/local_app/analytics_dashboard.py`.
- Added constants for object and schema version:
  `mythic_edge_local_app_analytics_dashboard_modules` and
  `analytics_dynamic_decision_support_dashboard.v1`.
- Added exactly three stock module builders:
  `play_draw_win_rate`, `game1_postboard`, and
  `mulligan_opening_hand_outcomes`.
- Added fixed read-only SQLite query execution with `mode=ro`.
- Added safe missing, unavailable, degraded, empty, and error payload paths.
- Added deferred custom explorer vocabulary with builder/query execution
  disabled.
- Added `GET /api/analytics/dashboard/modules` in
  `src/mythic_edge_parser/local_app/backend.py`.
- Added stable rejection for dashboard query parameters.

Frontend:

- Added dashboard response and module types in `frontend/src/types.ts`.
- Added `fetchAnalyticsDashboardModules(...)` and response validation in
  `frontend/src/api.ts`.
- Replaced the old static Decision Support insight rendering path with a
  backend-provided dashboard modules renderer in `frontend/src/App.tsx`.
- Added frontend-only module view storage under
  `mythic_edge.analytics.dashboard.module_view_preferences.v1`.
- Added safe dashboard text handling and fallback modules for malformed,
  unsafe, loading, degraded, and error states.
- Added bar and table rendering using React and CSS only.
- Added CSS for module controls, bar/table views, warnings, and boundary
  labels in `frontend/src/App.css`.

Tests:

- Added backend coverage in
  `tests/test_analytics_dynamic_decision_support_dashboard.py` for missing,
  unavailable, empty, populated, degraded, invalid database, fixed route shape,
  query-parameter rejection, source metadata safety, read-only sidecar status,
  and no charting dependency.
- Updated route inventory in `tests/test_analytics_local_app_backend.py`.
- Added frontend API validation coverage in `frontend/src/api.test.ts`.
- Added frontend Decision Support rendering, storage, safe display, no custom
  builder UI, no arbitrary SQL, no hidden-card/coaching/best-line claims, and
  no destructive controls coverage in `frontend/src/App.test.tsx`.

Docs:

- Added this implementation handoff.

## Change Type

Code changed, tests changed, and one implementation handoff doc was added.
No analytics schema artifact, migration, fixture, runtime artifact, or generated
database file was added.

## Validation Run

Passed:

- `py -m pytest -q tests\test_analytics_dynamic_decision_support_dashboard.py tests\test_analytics_app_play_draw_postboard_split_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_local_app_backend.py`
- `py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py`
- `py -m ruff check src tests tools`
- `npm --prefix frontend run typecheck`
- `npm --prefix frontend run test -- --run`
- `npm --prefix frontend run build`
- `git diff --check`
- `py tools\check_agent_docs.py`
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files

Notes:

- The focused backend route tests reported an existing FastAPI TestClient
  deprecation warning.
- One full frontend test run had a transient Match Journal cockpit test miss;
  the isolated test passed immediately afterward, and a full frontend rerun
  passed 75 tests.
- `npm --prefix frontend run build` created `frontend/dist`; it was removed
  before handoff.
- In-app browser smoke was not completed because the browser execution tool was
  not available after tool discovery in this session.

## Protected-Surface Status

No parser behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema/migrations/ingest, live
watcher behavior, Match Journal truth ownership, workbook schema, webhook
payload shape, Apps Script behavior, Sheets behavior, output transport,
production behavior, AI/OpenAI, Line Tracer, or coaching behavior was changed.

The new backend route is read-only, rejects query parameters, and uses fixed
queries only.

## Generated And Private Artifact Status

- `frontend/dist` was created by build validation and removed.
- No generated SQLite database files were added to the repo.
- No raw logs, JSONL artifacts, runtime files, failed posts, workbook exports,
  secrets, credentials, endpoint values, raw payloads, raw hashes, or local-only
  artifacts were added.

## Remaining Risks Or Unverified Layers

- Browser visual smoke was not completed in this thread because the browser
  JavaScript execution tool was unavailable after discovery.
- The module visual density and exact long-term dashboard layout remain product
  UX questions for later review.
- The custom explorer remains vocabulary only; builder UI and query execution
  are intentionally deferred.

## Forbidden Scope

Forbidden scope was not touched. No charting library, arbitrary SQL surface,
generic database browser, destructive UI control, migration, parser change,
ingest change, Match Journal truth change, workbook/webhook/App Script/Sheets
change, AI/coaching behavior, PR, commit, merge, deploy, tracker closure, or
issue closure was added.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #283.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/283

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_dynamic_decision_support_dashboard.md

Implementation handoff:
docs/implementation_handoffs/analytics_dynamic_decision_support_dashboard_comparison.md

Goal:
Review the implementation against the contract. Lead with findings ordered by
severity. Verify the fixed read-only GET /api/analytics/dashboard/modules
endpoint, response object/schema version, exactly three stock modules,
bar/table frontend rendering, browser-storage boundary, safe display behavior,
custom explorer deferral, and no charting/custom-builder/arbitrary-SQL or
destructive UI behavior.

Review:
- Inspect git status and identify unrelated dirty or untracked files.
- Read the contract and implementation handoff.
- Inspect src/mythic_edge_parser/local_app/analytics_dashboard.py,
  src/mythic_edge_parser/local_app/backend.py,
  tests/test_analytics_dynamic_decision_support_dashboard.py,
  tests/test_analytics_local_app_backend.py,
  frontend/src/types.ts, frontend/src/api.ts, frontend/src/App.tsx,
  frontend/src/App.css, frontend/src/api.test.ts, and frontend/src/App.test.tsx.
- Confirm the endpoint uses fixed read-only SQLite queries and does not create
  folders, database files, migrations, WAL/SHM/journal sidecars, or runtime
  artifacts for missing/unavailable reads.
- Confirm the frontend stores only module ID to selected view labels and does
  not expose raw payloads, raw hashes, full paths, exception strings, stack
  traces, secrets, arbitrary SQL, custom explorer builder UI, charting
  dependency, hidden-card claims, coaching, player-mistake labels, best-line
  claims, or destructive controls.
- Confirm parser/runtime/analytics schema/analytics ingest/live watcher/Match
  Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production
  behavior was not changed.

Validation:
py -m pytest -q tests\test_analytics_dynamic_decision_support_dashboard.py tests\test_analytics_app_play_draw_postboard_split_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed files.
If npm build creates frontend/dist, remove generated build output before final
report unless a later contract explicitly authorizes committing it.

Do not stage, commit, push, open a PR, merge, deploy, close issue #283, close
tracker #204, or close umbrella #207 unless explicitly asked.

Final report must include findings first, validation results, protected-surface
status, generated/private artifact status, remaining risk, next recommended
role, and a workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex C: Module Implementer / comparison thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/283"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "C"
  next_thread: "E"
  contract_artifact: "docs/contracts/analytics_dynamic_decision_support_dashboard.md"
  artifact_produced: "docs/implementation_handoffs/analytics_dynamic_decision_support_dashboard_comparison.md"
  branch: "codex/analytics-foundation"
  risk_tier: "High"
  implementation_summary:
    - "Added fixed read-only GET /api/analytics/dashboard/modules."
    - "Added exactly play_draw_win_rate, game1_postboard, and mulligan_opening_hand_outcomes modules."
    - "Rendered backend-provided modules in Decision Support with bar/table views and safe browser-storage preferences."
    - "Kept custom explorer vocabulary deferred and builder/query execution disabled."
  validation:
    - "Focused dashboard/backend tests passed."
    - "Existing analytics schema/view harness passed."
    - "Ruff passed."
    - "Frontend typecheck, tests, and build passed."
    - "git diff --check passed."
    - "py tools/check_agent_docs.py passed."
    - "Path-scoped protected-surface scan passed, forbidden 0, warnings 0."
    - "Path-scoped secret/private-marker scan passed, forbidden 0, warnings 0."
    - "frontend/dist build output removed after validation."
  protected_surfaces_touched: false
  forbidden_scope_touched: false
  remaining_risk:
    - "Browser visual smoke was not completed because browser JavaScript execution tooling was unavailable."
    - "Final path-scoped protected-surface and secret/private-marker scans should be checked in Codex E."
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
