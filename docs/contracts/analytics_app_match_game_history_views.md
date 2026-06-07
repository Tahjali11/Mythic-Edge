# Analytics App Match And Game History Views Contract

## Module

Local developer app curated analytics history views.

This contract covers the first read-only local app display for imported match
and game facts stored in the local SQLite analytics database.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/225
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

Required repo authorities:

- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

## Branch

`codex/analytics-foundation`

## Risk Tier

High.

Reason: this slice adds both backend API and frontend display surfaces over
local analytics data. The intended behavior is read-only, but the new surface
could accidentally become a generic database browser, expose local/private
data, blur parser truth boundaries, or invite destructive controls.

## Owning Layer

Primary owning layer: Local App / UI.

Supporting storage/query layer: Analytics.

Truth boundaries:

- Parser/state owns parser-managed match facts, game facts, event
  interpretation, match/game identity, deduplication, and final reconciliation.
- SQLite analytics tables own local durable storage of parser-normalized facts
  and provenance/status labels.
- The local app backend owns fixed, read-only API projections over the local
  analytics database.
- The local app frontend owns display and local interaction.
- Neither SQLite nor the UI may reinterpret Arena events, override parser
  finality, infer hidden facts, classify archetypes, label player mistakes, or
  provide coaching truth.

Plain English: this view may show "these are the match and game facts currently
stored locally." It may not decide what happened in Arena or tell the player
what to do.

## Internal Project Area

Primary area: Local App / UI.

Bridge-code status: `bridge_code`.

Bridge details:

- source internal project area: Analytics
- consuming internal project area: Local App / UI
- allowed data flow: SQLite analytics fact tables to fixed read-only backend
  responses to frontend display
- forbidden reverse-flow: frontend/backend history views must not write back to
  SQLite, change analytics ingest, change parser facts, or update workbook or
  runtime state
- protected surfaces explicitly not touched: parser behavior, analytics schema
  and migrations, analytics ingest, workbook/webhook/App Script/Sheets,
  production behavior, generated/private/local artifacts, secrets, raw logs,
  and AI/coaching surfaces

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_app_match_game_history_views.md`

Future implementation files authorized for Codex C, subject to comparison and
validation:

- `src/mythic_edge_parser/local_app/backend.py`
- optional new helper module under `src/mythic_edge_parser/local_app/`, such as
  `analytics_history.py`, for fixed read-only query helpers
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- focused backend tests, expected as
  `tests/test_analytics_app_match_game_history_views.py` or focused additions
  to `tests/test_analytics_local_app_backend.py`
- `docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md`

Reference-only source surfaces:

- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- current analytics ingest and import tests

Not owned by this contract:

- parser modules
- parser state final reconciliation
- parser event classes
- match/game identity or deduplication
- analytics schema migrations
- analytics ingest behavior
- runtime status artifacts
- workbook schema, webhook payload shape, Apps Script behavior, or Google
  Sheets behavior
- raw Player.log files, private JSONL artifacts, generated SQLite files,
  failed posts, workbook exports, secrets, credentials, or local-only artifacts
- Match Journal, Line Tracer, AI/OpenAI, coaching, production behavior, CI
  gates, merge policy, or deploy policy

## Public Interface

### Schema Version

The local app history response schema version is:

```text
analytics_app_match_game_history_views.v1
```

### Backend Endpoints

Codex C may add exactly these first history endpoints:

```text
GET /api/analytics/matches
GET /api/analytics/games
```

Allowed query parameters:

- `limit`: optional integer, default `50`, minimum `1`, maximum `100`
- `offset`: optional integer, default `0`, minimum `0`

No other query parameters are authorized in this first slice.

Forbidden backend interface expansion:

- arbitrary SQL input
- table name, column name, order-by, where-clause, filter, or raw query input
- database browsing endpoints
- database reset/delete/vacuum/export endpoints
- schema/migration endpoints
- import endpoints beyond existing manual import/upload routes
- live Player.log watcher endpoints
- Google Sheets, Match Journal, Line Tracer, AI/OpenAI, or coaching endpoints

### Response Object Names

`GET /api/analytics/matches` must return:

```text
object: mythic_edge_local_app_match_history
schema_version: analytics_app_match_game_history_views.v1
```

`GET /api/analytics/games` must return:

```text
object: mythic_edge_local_app_game_history
schema_version: analytics_app_match_game_history_views.v1
```

### Top-Level Response Shape

Both endpoints return a JSON object with:

- `object`
- `schema_version`
- `status`
- `database`
- `pagination`
- `summary`
- `rows`
- `warnings`
- `errors`

Allowed `status` labels:

- `ok`: schema-current database queried successfully and at least one row was
  returned
- `empty`: schema-current database queried successfully and zero rows were
  returned
- `missing`: analytics database is absent
- `unavailable`: app data root or database path is unavailable
- `degraded`: database is readable but schema is missing, unknown, outdated,
  or not safe to query for this response shape
- `error`: database is invalid, unreadable, or a fixed query failed

Expected `database` shape:

```json
{
  "display_path": "<app_data>\\db\\mythic_edge.sqlite3",
  "exists": true,
  "schema_status": "schema_current",
  "status": "ok"
}
```

The `display_path` must remain symbolic. It must not reveal an absolute local
path.

Expected `pagination` shape:

```json
{
  "limit": 50,
  "offset": 0,
  "returned": 0
}
```

Expected `summary` shape:

```json
{
  "row_count": 0,
  "degraded_row_count": 0,
  "unavailable_row_count": 0,
  "conflict_row_count": 0
}
```

The summary counts describe row status labels only. They are not parser truth
and must not be used to rewrite parser-managed facts.

## Backend Query Contract

### Database Access

History endpoints must:

- use the app-owned local analytics database path from `build_local_app_paths`
- open the database read-only when querying rows
- avoid creating app folders or database files for missing-database reads
- avoid applying migrations
- avoid changing migration status
- avoid writing temp tables, materialized summaries, WAL files by design, or
  runtime artifacts
- use fixed parameterized SQL
- close SQLite connections deterministically
- return safe shaped status payloads for expected missing/degraded/error states

Recommended implementation pattern:

- call existing database status logic or equivalent read-only checks first
- query rows only when the database exists and `schema_status` is
  `schema_current`
- use `sqlite3.Row` or structured row mapping
- use `LIMIT ? OFFSET ?` with validated integers

### Allowed Tables

The first slice may query only these table families:

- `matches`
- `games`
- `match_results`
- `game_results`
- `match_context`

The first slice must not query:

- raw local files
- raw JSONL artifacts
- raw Player.log contents
- `fact_provenance`
- opening hand tables
- mulligan tables
- sideboarding or deck-state tables
- gameplay action tables
- opponent-card-observation tables
- rank snapshots
- annotation tables such as matchup labels, archetype labels, or game notes
- derived dashboard views such as `v_opening_lines`,
  `v_play_draw_splits`, or `v_matchup_label_performance`

Those richer analytics surfaces remain deferred to later contracts.

### Match History Rows

Each match history row must include:

- `match_id`
- `parser_match_key`
- `match_started_at`
- `match_completed_at`
- `match_result`
- `match_win`
- `games_won`
- `games_lost`
- `total_games`
- `game_win_rate`
- `queue_name`
- `format_name`
- `event_id`
- `match_status`
- `result_status`
- `context_status`

`match_status`, `result_status`, and `context_status` are provenance/status
objects. Each status object includes:

- `value_source`
- `confidence`
- `finality`
- `drift_status`
- `availability_status`
- `source_parser_surface`
- `source_fact_key`
- `ingest_run_id`

If a joined optional row does not exist, the corresponding data fields must be
`null` and the corresponding status object must be `null`. The endpoint must
not invent unknown result or context rows.

Allowed match query joins:

```text
matches
LEFT JOIN match_results ON match_results.match_id = matches.match_id
LEFT JOIN match_context ON match_context.match_id = matches.match_id
```

Required deterministic order:

```text
COALESCE(matches.match_completed_at, matches.match_started_at, matches.updated_at) DESC,
matches.match_id DESC
```

### Game History Rows

Each game history row must include:

- `game_id`
- `match_id`
- `game_number`
- `game_started_at`
- `game_completed_at`
- `local_result`
- `winner_team_id`
- `pre_postboard_label`
- `play_draw`
- `turn_count`
- `game_duration_seconds`
- `queue_name`
- `format_name`
- `event_id`
- `game_status`
- `result_status`
- `context_status`

`game_status`, `result_status`, and `context_status` follow the same
provenance/status object rules as match rows.

If a joined optional result or context row does not exist, the corresponding
fields and status object must be `null`.

Allowed game query joins:

```text
games
LEFT JOIN game_results ON game_results.game_id = games.game_id
LEFT JOIN match_context ON match_context.match_id = games.match_id
```

Required deterministic order:

```text
COALESCE(games.game_completed_at, game_results.game_completed_at, games.game_started_at, games.updated_at) DESC,
games.match_id DESC,
games.game_number ASC
```

### Row Status Summaries

For response `summary` counts, a row is degraded when any included status
object has:

- `drift_status` in `degraded`, `conflict`, `missing_expected_evidence`, or
  `redacted`
- `value_source` equal to `conflict`
- `confidence` equal to `low` or `unknown`

A row is unavailable when any included status object has
`availability_status` not equal to `available`.

A row is conflict when any included status object has:

- `drift_status` equal to `conflict`
- `value_source` equal to `conflict`

These counts are UI review signals only. They must not change stored facts.

## Frontend Display Contract

The frontend may replace the deferred `Analytics Views` panel with a first
read-only Analytics section.

Required frontend behavior:

- fetch `GET /api/analytics/matches` and `GET /api/analytics/games`
- validate response `object` and `schema_version`
- show match history and game history as compact tables, tabs, or review cards
- show loading, empty, missing, degraded, and error states
- preserve existing setup-status and manual-import behavior
- keep the existing JSONL import/upload workflow available
- keep all history actions read-only
- show provenance/status labels where useful as compact status pills or text
- show safe counts from `summary`
- avoid display text that presents downstream SQLite/UI data as parser truth

Allowed read-only frontend action:

- a refresh control that re-fetches the two history endpoints

Forbidden frontend behavior:

- arbitrary SQL entry
- table picker or column picker
- edit/delete/reset/vacuum/export controls
- database initialization controls
- import controls inside the Analytics history section
- live watcher controls
- Match Journal editing
- matchup/archetype labeling or game notes editing
- opening-hand, mulligan, gameplay-action, opponent-observation, or derived
  dashboard pages in this slice
- raw payload, raw hash, full path, private JSONL contents, or local machine
  marker display
- AI/OpenAI, coaching, strategic advice, mistake labels, or hidden-card
  inference

Frontend API validation must fail closed. A malformed or incompatible response
should render a safe error state and must not display raw backend error
details.

## Error Behavior

Missing database:

- return `status = "missing"`
- return `rows = []`
- return a symbolic database display path
- do not create folders or database files

Unavailable app data root:

- return `status = "unavailable"`
- return `rows = []`
- do not create folders or database files

Unmigrated, unknown, or outdated schema:

- return `status = "degraded"`
- return `rows = []`
- include a stable warning code such as `analytics_schema_not_current`
- do not run row queries against an unsafe schema
- do not apply migrations

Empty schema-current database:

- return `status = "empty"`
- return `rows = []`
- return empty summary counts

Invalid SQLite, unreadable database, or query failure:

- return `status = "error"`
- return `rows = []`
- include stable error codes only
- do not expose exception strings, SQL text, absolute paths, raw payloads, raw
  hashes, stack traces, secrets, or local usernames

Malformed query parameters:

- reject safely with stable error status or HTTP 422 behavior
- do not interpolate raw parameter values into SQL or unsafe display strings

## Side Effects

Allowed side effects:

- read-only HTTP responses
- frontend render state
- test-created temporary SQLite databases under pytest temp directories
- implementation handoff documentation

Forbidden side effects:

- parser behavior changes
- analytics schema or migration changes
- analytics ingest changes
- generated repo-local SQLite files
- raw log, raw JSONL, runtime status, failed-post, workbook export, or local
  artifact writes
- workbook/webhook/App Script/Sheets writes
- external network calls beyond the local backend/frontend loopback in tests
- OpenAI/model-provider calls
- issue closure, tracker closure, PR creation, staging, commit, push, merge, or
  deploy actions unless explicitly requested in a later role

## Compatibility

- Existing setup status endpoints must remain unchanged unless Codex C proves a
  narrow additive compatibility field is required.
- Existing manual JSONL import and browser upload endpoints must remain
  unchanged.
- Existing frontend upload and folder-upload flows must remain available.
- Existing `analytics_app_backend_setup_status.v1` and
  `analytics_manual_jsonl_import_ui_job_status.v1` response validation must
  remain compatible.
- Existing analytics schema and derived views must not be changed in this
  slice.

## Observed Current Behavior

- Issue #225 is open.
- Tracker #204 is open.
- Umbrella issue #207 is open.
- The branch is `codex/analytics-foundation`.
- The local app backend currently exposes setup/status routes, manual JSONL
  import routes, browser JSONL upload, and import job status.
- The only analytics backend route currently present is
  `GET /api/analytics/database/status`.
- The backend route inventory does not include
  `GET /api/analytics/matches` or `GET /api/analytics/games`.
- The frontend currently renders setup-status panels, manual import controls,
  browser JSONL upload, and browser folder upload.
- The frontend still renders `Analytics Views` as a deferred panel.
- The SQLite schema already contains `matches`, `games`, `match_results`,
  `game_results`, and `match_context` tables with core provenance/status
  columns.
- Tests already cover local app setup/status routes, manual import, browser
  upload privacy/safety, analytics schema, derived SQL views, and replay/view
  harness behavior.
- No current tests prove a curated match/game history backend API or frontend
  display.

## Unknowns

- The best final UI layout for compact match/game history is not yet proven.
  Codex C may choose tabs, stacked tables, or compact review cards as long as
  the display remains read-only and curated.
- It is unknown whether future pagination, filtering, or search will be needed.
  This contract authorizes only `limit` and `offset`.
- It is unknown whether match/game context fields will be sufficient for the
  user's first review workflow. Opening hands, mulligans, gameplay actions,
  opponent observations, and dashboards remain deferred.
- It is unknown whether row-level status summary counts should later include
  `fact_provenance` detail. This first slice must not query `fact_provenance`.

## Suspected Gaps

- Backend: no fixed read-only history query helper exists yet.
- Backend: no route tests cover missing, empty, schema-current, schema-degraded,
  or query-failure history responses.
- Backend: current route inventory tests will need additive endpoint
  expectations.
- Frontend: no typed history response models or API functions exist yet.
- Frontend: the analytics section is still deferred.
- Frontend: no tests cover history loading, empty/degraded/error states, safe
  display, or read-only action boundaries.

## Validation Requirements

Codex C should run:

```powershell
py -m pytest -q tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
```

If frontend dependencies are absent, Codex C may run `npm --prefix frontend ci`
before frontend validation.

Codex C and Codex E must also report:

- no generated SQLite files, WAL files, SHM files, journal files, raw logs,
  raw JSONL files, failed posts, workbook exports, runtime artifacts, or
  secrets were created or committed
- no arbitrary SQL, database browsing, or destructive routes were added
- no raw payloads, raw hashes, private paths, exception strings, stack traces,
  local usernames, or credentials appear in endpoint responses or UI output
- protected-surface scan results for changed paths
- secret/private-marker scan results for changed paths

## Acceptance Criteria

- `GET /api/analytics/matches` exists and returns the approved response shape.
- `GET /api/analytics/games` exists and returns the approved response shape.
- Both endpoints use fixed parameterized read-only queries.
- Both endpoints handle missing, unavailable, unmigrated/degraded,
  schema-current-empty, schema-current-with-rows, invalid database, and query
  failure cases safely.
- Neither endpoint creates a database or applies migrations.
- Neither endpoint exposes arbitrary SQL, full local paths, raw payloads, raw
  hashes, secrets, or local machine markers.
- The frontend replaces the deferred Analytics Views panel with a curated
  read-only match/game history section.
- The frontend validates history response object/schema versions.
- The frontend shows loading, empty, missing, degraded, and error states.
- Existing setup-status, manual import, upload, and folder upload workflows
  continue to work.
- Focused backend and frontend tests prove the contract behavior.
- The implementation handoff documents observed matches, gaps, files changed,
  validation, protected-surface status, remaining risk, and next recommended
  role.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #225.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_match_game_history_views.md

Goal:
Compare the current local app backend, frontend, analytics schema, and tests against the contract. Implement only the first read-only curated match/game history view slice and focused tests. Produce docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md.

Before editing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what the history view is supposed to do, what the app currently does, what gap remains, and the exact minimal implementation plan.

Do:
- Add fixed read-only backend endpoints GET /api/analytics/matches and GET /api/analytics/games.
- Query only matches, games, match_results, game_results, and match_context.
- Use read-only SQLite access and fixed parameterized SQL.
- Return the approved typed response shapes with safe status/error handling.
- Replace the deferred frontend Analytics Views panel with a curated read-only match/game history section.
- Add focused backend and frontend tests for success, empty/missing/degraded/error states, response validation, safe display, and read-only boundaries.
- Preserve existing setup-status, manual import, browser upload, and folder-upload behavior.
- Produce the implementation handoff.

Do not:
- add arbitrary SQL, generic database browsing, or destructive database/UI controls
- create or apply migrations
- change analytics schema or ingest behavior
- query raw Player.log, raw JSONL, fact_provenance, opening hands, mulligans, gameplay actions, opponent observations, annotation tables, or derived dashboard views in this slice
- expose raw payloads, raw hashes, full paths, exception strings, stack traces, secrets, credentials, or local machine markers
- create or commit generated SQLite files, raw logs, JSONL artifacts, runtime files, failed posts, workbook exports, or local-only artifacts
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, output transport, production behavior, AI/OpenAI, Line Tracer, or coaching behavior
- target main
- close tracker #204 or umbrella #207
- stage, commit, push, open a PR, merge, or deploy unless explicitly asked

Validation:
py -m pytest -q tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check

Final handoff must include role performed, source issue/tracker, contract used, files changed, exact backend/frontend/test sections changed, validation run, protected-surface status, generated/private artifact status, remaining risk, next recommended role, and workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex B: Module Contract Writer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/225"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #225 and current local app/analytics implementation"
  target_artifact: "docs/contracts/analytics_app_match_game_history_views.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "Codex B docs-only validation required: git status --short --branch"
    - "Codex B docs-only validation required: git diff --check"
    - "Codex B docs-only validation required: protected-surface and secret/private-marker scans on the contract"
    - "Codex C should run backend, frontend, schema/view, ruff, and generated-artifact checks"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not add arbitrary SQL, generic database browsing, or destructive controls."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not change analytics schema, migrations, or ingest behavior in this slice."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```
