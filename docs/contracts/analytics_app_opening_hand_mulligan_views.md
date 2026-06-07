# Analytics App Opening Hand And Mulligan Views Contract

## Module

Local developer app curated opening hand and mulligan analytics views.

This contract covers the next read-only local app display for imported
early-game facts stored in the local SQLite analytics database.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/226
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Completed prerequisite: https://github.com/Tahjali11/Mythic-Edge/issues/225

Required repo authorities:

- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

## Branch

`codex/analytics-foundation`

## Risk Tier

High.

Reason: opening hand and mulligan facts are easy for a human or later UI to
overinterpret as coaching or mistake detection. This slice also touches backend
API and frontend display surfaces over local analytics data, so it must remain
fixed, read-only, private-data-safe, and downstream of parser truth.

## Owning Layer

Primary owning layer: Local App / UI.

Supporting storage/query layer: Analytics.

Truth boundaries:

- Parser/state owns parser-managed opening hand facts, mulligan facts,
  match/game identity, event interpretation, deduplication, and final
  reconciliation.
- SQLite analytics tables own local durable storage of parser-normalized
  early-game facts and provenance/status labels.
- Derived SQL views own deterministic read-only projections over stored facts.
- The local app backend owns fixed read-only API projections over the local
  analytics database.
- The local app frontend owns display and local interaction.
- Neither SQLite nor the UI may reinterpret Arena events, infer missing hand
  contents, judge keep/mulligan quality, label player mistakes, provide best
  line recommendations, infer hidden cards, classify archetypes, or become
  coaching truth.

Plain English: this view may show "what did my games start with?" It must not
answer "what should I have done?"

## Internal Project Area

Primary area: Local App / UI.

Bridge-code status: `bridge_code`.

Bridge details:

- source internal project area: Analytics
- consuming internal project area: Local App / UI
- allowed data flow: SQLite analytics opening-hand/mulligan fact tables and
  approved read-only views to fixed local backend responses to frontend display
- forbidden reverse-flow: frontend/backend early-game views must not write back
  to SQLite, change analytics ingest, change parser facts, update workbook or
  runtime state, or feed coaching conclusions into parser/analytics truth
- protected surfaces explicitly not touched: parser behavior, analytics schema
  and migrations, analytics ingest, workbook/webhook/App Script/Sheets,
  production behavior, generated/private/local artifacts, secrets, raw logs,
  and AI/coaching surfaces

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_app_opening_hand_mulligan_views.md`

Future implementation files authorized for Codex C, subject to comparison and
validation:

- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/backend.py`
- optional new helper module under `src/mythic_edge_parser/local_app/` only if
  the grouping logic becomes clearer than extending `analytics_history.py`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- focused backend tests, expected as
  `tests/test_analytics_app_opening_hand_mulligan_views.py`
- focused route inventory additions in `tests/test_analytics_local_app_backend.py`
- `docs/implementation_handoffs/analytics_app_opening_hand_mulligan_views_comparison.md`

Reference-only source surfaces:

- `docs/contracts/analytics_app_match_game_history_views.md`
- `docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md`
- `docs/contract_test_reports/analytics_app_match_game_history_views.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/contracts/analytics_derived_sql_views.md`
- `docs/contracts/analytics_replay_view_validation_harness.md`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- current analytics ingest and replay/view tests

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
  frontend build output, failed posts, workbook exports, secrets, credentials,
  or local-only artifacts
- Match Journal, Line Tracer, AI/OpenAI, coaching, production behavior, CI
  gates, merge policy, or deploy policy

## Public Interface

### Schema Version

The local app early-game response schema version is:

```text
analytics_app_opening_hand_mulligan_views.v1
```

This is intentionally separate from
`analytics_app_match_game_history_views.v1` because the row shapes include
grouped child card arrays.

### Backend Endpoints

Codex C may add exactly these first early-game endpoints:

```text
GET /api/analytics/opening-hands
GET /api/analytics/mulligans
```

Allowed query parameters:

- `limit`: optional integer, default `50`, minimum `1`, maximum `100`
- `offset`: optional integer, default `0`, minimum `0`

No other query parameters are authorized in this first slice.

Query parameter parsing must reuse or match the #225 sanitized history
pagination behavior: malformed, duplicate, out-of-range, or unapproved query
parameters must produce stable error codes without echoing raw input.

Forbidden backend interface expansion:

- arbitrary SQL input
- table name, column name, order-by, where-clause, filter, search, or raw query
  input
- database browsing endpoints
- database reset/delete/vacuum/export endpoints
- schema/migration endpoints
- import behavior changes
- live Player.log watcher endpoints
- Google Sheets, Match Journal, Line Tracer, AI/OpenAI, or coaching endpoints

### Response Object Names

`GET /api/analytics/opening-hands` must return:

```text
object: mythic_edge_local_app_opening_hand_history
schema_version: analytics_app_opening_hand_mulligan_views.v1
```

`GET /api/analytics/mulligans` must return:

```text
object: mythic_edge_local_app_mulligan_history
schema_version: analytics_app_opening_hand_mulligan_views.v1
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

- `ok`: schema-current database queried successfully and at least one grouped
  row was returned
- `empty`: schema-current database queried successfully and zero grouped rows
  were returned
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

The `display_path` must remain symbolic and must not reveal an absolute local
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
  "card_row_count": 0,
  "degraded_row_count": 0,
  "unavailable_row_count": 0,
  "conflict_row_count": 0
}
```

`row_count` counts grouped opening-hand or mulligan rows. `card_row_count`
counts child card rows included inside those grouped rows. These counts are
display/review signals only, not parser truth or coaching conclusions.

## Backend Query Contract

### Database Access

Early-game endpoints must:

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

- reuse the #225 database status, pagination, payload, and summary helpers
  where possible
- query rows only when the database exists and `schema_status` is
  `schema_current`
- use `sqlite3.Row` or structured row mapping
- paginate grouped parent rows, not child card rows
- perform child-card fetching with fixed parameterized queries keyed by the
  selected parent ids

### Allowed Tables And Views

The first slice may query only:

- `opening_hands`
- `opening_hand_cards`
- `mulligan_events`
- `mulligan_bottomed_or_discarded_cards`
- `games`
- `matches`
- `game_results`
- `match_results`
- `match_context`
- `v_opening_hand_cards`, only as a read-only source when it does not hide
  opening-hand groups that have zero child cards
- `v_mulligan_outcomes`, only as a read-only source for mulligan/event context

The first slice must not query:

- raw local files
- raw JSONL artifacts
- raw Player.log contents
- `fact_provenance`
- rank snapshots
- sideboarding or deck-state tables
- gameplay action tables
- opponent-card-observation tables
- annotation tables such as matchup labels, archetype labels, or game notes
- derived dashboard views such as `v_opening_lines`,
  `v_play_draw_splits`, `v_sample_size_warnings`, or
  `v_matchup_label_performance`

`v_opening_lines`, Line Tracer-style views, and sample-size/dashboard summaries
are explicitly deferred. Row-level play/draw and result context may be shown,
but this slice must not produce causal claims or recommendations.

### Opening Hand Rows

`GET /api/analytics/opening-hands` returns one grouped row per stored
`opening_hands` row.

Each opening hand row must include:

- `opening_hand_id`
- `match_id`
- `game_id`
- `game_number`
- `hand_size`
- `exact_card_count`
- `local_result`
- `play_draw`
- `pre_postboard_label`
- `match_result`
- `match_win`
- `queue_name`
- `format_name`
- `event_id`
- `cards`
- `opening_hand_status`
- `game_status`
- `game_result_status`
- `match_result_status`
- `context_status`

`cards` is an array ordered by `card_position`. Each opening hand card row must
include:

- `opening_hand_card_id`
- `card_position`
- `grp_id`
- `card_name`
- `identity_hint_source`
- `name_resolution_status`
- `card_status`

Status objects include:

- `value_source`
- `confidence`
- `finality`
- `drift_status`
- `availability_status`
- `source_parser_surface`
- `source_fact_key`
- `ingest_run_id`

If an optional joined row does not exist, its data fields must be `null` and
its status object must be `null`. The endpoint must not invent unknown game
result, match result, context, or card rows.

If an `opening_hands` row exists with zero child card rows, the endpoint must
return the opening hand group with `cards: []`.

Required deterministic order:

```text
COALESCE(games.game_completed_at, game_results.game_completed_at, games.game_started_at, games.updated_at) DESC,
opening_hands.match_id DESC,
opening_hands.game_number ASC,
opening_hands.opening_hand_id ASC
```

### Mulligan Rows

`GET /api/analytics/mulligans` returns one grouped row per stored
`mulligan_events` row.

Each mulligan row must include:

- `mulligan_event_id`
- `match_id`
- `game_id`
- `game_number`
- `ordinal_or_count`
- `mulligan_count`
- `decision_detail`
- `local_result`
- `play_draw`
- `pre_postboard_label`
- `match_result`
- `match_win`
- `queue_name`
- `format_name`
- `event_id`
- `cards`
- `mulligan_status`
- `game_status`
- `game_result_status`
- `match_result_status`
- `context_status`

`cards` is an array ordered by `card_position`. Each mulligan child card row
must include:

- `mulligan_card_id`
- `card_position`
- `card_action`
- `grp_id`
- `card_name`
- `identity_hint_source`
- `card_status`

Allowed `card_action` labels are the existing schema labels:

- `bottomed`
- `discarded`
- `unknown`

If a `mulligan_events` row exists with zero child card rows, the endpoint must
return the mulligan group with `cards: []`.

Required deterministic order:

```text
COALESCE(games.game_completed_at, game_results.game_completed_at, games.game_started_at, games.updated_at) DESC,
mulligan_events.match_id DESC,
mulligan_events.game_number ASC,
mulligan_events.ordinal_or_count ASC,
mulligan_events.mulligan_event_id ASC
```

### Row Status Summaries

For response `summary` counts, a grouped row is degraded when any included
parent, context, result, game, or child-card status object has:

- `drift_status` in `degraded`, `conflict`, `missing_expected_evidence`, or
  `redacted`
- `value_source` equal to `conflict`
- `confidence` equal to `low` or `unknown`

A grouped row is unavailable when any included status object has
`availability_status` not equal to `available`.

A grouped row is conflict when any included status object has:

- `drift_status` equal to `conflict`
- `value_source` equal to `conflict`

These counts are review signals only. They must not change stored facts or
imply strategic quality.

## Frontend Display Contract

The frontend may add Opening Hands and Mulligans to the existing Analytics
History area or a clearly adjacent read-only analytics section.

Required frontend behavior:

- fetch `GET /api/analytics/opening-hands` and
  `GET /api/analytics/mulligans`
- validate response `object` and `schema_version`
- show opening hands grouped by game
- show opening hand cards when available
- show mulligan events grouped by game
- show bottomed/discarded mulligan card rows when available
- show loading, empty, missing, degraded, and error states
- reuse #225 history visual/status patterns where practical
- preserve existing setup-status, manual-import, browser-upload,
  folder-upload, match-history, and game-history behavior
- keep all early-game history actions read-only
- show provenance/status labels as compact review labels where useful
- show safe counts from `summary`
- avoid display text that presents downstream SQLite/UI data as parser truth,
  coaching truth, or strategic advice

Allowed read-only frontend action:

- a refresh control that re-fetches the analytics history endpoints

Codex C may either:

- extend the existing Analytics History refresh to fetch match/game/opening
  hand/mulligan data together, or
- add a separate early-game refresh inside the same read-only analytics area

The implementation must not cause import/upload controls to become destructive
or intermingled with analytics review actions.

Forbidden frontend behavior:

- arbitrary SQL entry
- table picker or column picker
- edit/delete/reset/vacuum/export controls
- database initialization controls
- import controls inside the early-game review section
- live watcher controls
- Match Journal editing
- matchup/archetype labeling or game notes editing
- gameplay-action dashboards
- opponent-card-observation dashboards
- Line Tracer behavior
- best keep recommendations
- mulligan mistake labels
- opening line recommendations
- hidden-card inference
- matchup/archetype inference
- raw payload, raw hash, full path, private JSONL contents, or local machine
  marker display
- AI/OpenAI, coaching, strategic advice, or player evaluation

Frontend API validation must fail closed. A malformed or incompatible response
must render a safe error state and must not display raw backend error details.

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

Partial data:

- return stored parent rows even when optional context/result/child rows are
  absent
- represent missing optional joined rows with `null` or empty child arrays
- preserve source/confidence/finality/drift/availability labels
- do not fill missing cards, mulligan decisions, game results, match results,
  or context by inference

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
- raw log, raw JSONL, runtime status, failed-post, workbook export, frontend
  build output, or local artifact writes
- workbook/webhook/App Script/Sheets writes
- external network calls beyond local backend/frontend loopback in tests
- OpenAI/model-provider calls
- issue closure, tracker closure, PR creation, staging, commit, push, merge, or
  deploy actions unless explicitly requested in a later role

## Compatibility

- Existing setup-status endpoints must remain unchanged.
- Existing manual JSONL import and browser upload endpoints must remain
  unchanged.
- Existing match/game history endpoints and frontend display must remain
  compatible.
- Existing frontend upload and folder-upload flows must remain available.
- Existing `analytics_app_match_game_history_views.v1`,
  `analytics_app_backend_setup_status.v1`, and
  `analytics_manual_jsonl_import_ui_job_status.v1` response validation must
  remain compatible.
- Existing analytics schema, derived views, and ingest behavior must not be
  changed in this slice.

## Observed Current Behavior

- Issue #226 is open.
- Tracker #204 is open.
- Umbrella issue #207 is open.
- Issue #225 is closed.
- `docs/contracts/analytics_app_match_game_history_views.md`,
  `docs/implementation_handoffs/analytics_app_match_game_history_views_comparison.md`,
  and `docs/contract_test_reports/analytics_app_match_game_history_views.md`
  exist on the branch.
- The branch is `codex/analytics-foundation`.
- The backend currently exposes `GET /api/analytics/matches` and
  `GET /api/analytics/games` through fixed read-only helpers in
  `src/mythic_edge_parser/local_app/analytics_history.py`.
- The backend does not expose `GET /api/analytics/opening-hands` or
  `GET /api/analytics/mulligans`.
- The frontend currently renders an Analytics History section with match and
  game history plus a refresh control.
- The frontend does not yet render opening hand or mulligan history.
- The SQLite schema already contains `opening_hands`,
  `opening_hand_cards`, `mulligan_events`, and
  `mulligan_bottomed_or_discarded_cards` tables with core
  provenance/status columns.
- The SQLite schema already contains `v_opening_hand_cards` and
  `v_mulligan_outcomes`.
- `v_opening_hand_cards` is an inner-join card-row view, so it may hide
  opening-hand groups that have no child card rows.
- `v_mulligan_outcomes` preserves mulligan outcome context but does not include
  bottomed/discarded child card rows.
- Existing tests prove derived view behavior and replay/view harness coverage,
  but no current tests prove local app early-game history endpoints or
  frontend display.

## Unknowns

- The best final UI layout for compact early-game review is not yet proven.
  Codex C may choose tabs, stacked tables, expandable groups, or compact review
  cards as long as the display remains read-only and curated.
- It is unknown whether the user will prefer opening hands and mulligans in the
  same Analytics History section or a sibling Early Game section.
- It is unknown whether later filters by match, format, or play/draw will be
  needed. This contract authorizes only `limit` and `offset`.
- It is unknown whether future opening-line or sample-size summaries should be
  displayed next to early-game rows. This contract defers those summaries.

## Suspected Gaps

- Backend: no fixed read-only early-game query helpers exist yet.
- Backend: no route tests cover missing, empty, schema-current, schema-degraded,
  query-failure, partial child-row, or safe malformed-query behavior for
  opening hand and mulligan responses.
- Backend: the route inventory needs additive endpoint expectations.
- Frontend: no typed opening hand or mulligan response models exist yet.
- Frontend: no API functions exist for the new endpoints.
- Frontend: no tests cover grouped early-game history display, empty/degraded
  states, malformed responses, safe display, or read-only action boundaries.

## Validation Requirements

Codex C should run:

```powershell
py -m pytest -q tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
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
  raw JSONL files, failed posts, workbook exports, runtime artifacts, frontend
  build output, or secrets were created or committed
- no arbitrary SQL, database browsing, or destructive routes were added
- no raw payloads, raw hashes, private paths, exception strings, stack traces,
  local usernames, credentials, coaching advice, best-keep labels, or player
  mistake labels appear in endpoint responses or UI output
- protected-surface scan results for changed paths
- secret/private-marker scan results for changed paths

## Acceptance Criteria

- `GET /api/analytics/opening-hands` exists and returns the approved response
  shape.
- `GET /api/analytics/mulligans` exists and returns the approved response
  shape.
- Both endpoints use fixed parameterized read-only queries.
- Both endpoints paginate grouped parent rows, not child card rows.
- Opening hand responses include one grouped row per stored `opening_hands`
  row and include child `opening_hand_cards` rows when present.
- Mulligan responses include one grouped row per stored `mulligan_events` row
  and include child `mulligan_bottomed_or_discarded_cards` rows when present.
- Missing child rows produce empty child arrays rather than inferred content.
- Both endpoints handle missing, unavailable, unmigrated/degraded,
  schema-current-empty, schema-current-with-rows, invalid database, fixed query
  failure, and malformed query parameter cases safely.
- Neither endpoint creates a database or applies migrations.
- Neither endpoint exposes arbitrary SQL, full local paths, raw payloads, raw
  hashes, secrets, coaching labels, strategic advice, or local machine markers.
- The frontend displays read-only opening hand and mulligan history inside or
  adjacent to Analytics History.
- The frontend validates early-game response object/schema versions.
- The frontend shows loading, empty, missing, degraded, and error states.
- Existing setup-status, manual import, upload, folder upload, match history,
  and game history workflows continue to work.
- Focused backend and frontend tests prove the contract behavior.
- The implementation handoff documents observed matches, gaps, files changed,
  validation, protected-surface status, remaining risk, and next recommended
  role.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #226.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_opening_hand_mulligan_views.md

Prerequisite context:
Issue #225 is complete. Reuse the fixed read-only local app history safety pattern from docs/contracts/analytics_app_match_game_history_views.md and src/mythic_edge_parser/local_app/analytics_history.py where practical.

Goal:
Compare the current local app backend, frontend, analytics schema/views, and tests against the contract. Implement only the read-only opening hand and mulligan history view slice and focused tests. Produce docs/implementation_handoffs/analytics_app_opening_hand_mulligan_views_comparison.md.

Before editing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what the early-game view is supposed to do, what the app currently does, what gap remains, and the exact minimal implementation plan.

Do:
- Add fixed read-only backend endpoints GET /api/analytics/opening-hands and GET /api/analytics/mulligans.
- Query only the allowed opening-hand, mulligan, match/game result, match context, and approved view surfaces from the contract.
- Use read-only SQLite access and fixed parameterized SQL.
- Paginate grouped parent rows, not child card rows.
- Return grouped opening hand rows with child card arrays.
- Return grouped mulligan rows with bottomed/discarded child card arrays.
- Return the approved typed response shapes with safe status/error handling.
- Add read-only frontend display for opening hands and mulligans inside or adjacent to Analytics History.
- Add focused backend and frontend tests for success, empty, missing, degraded, error, partial child rows, malformed query params, response validation, safe display, and read-only boundaries.
- Preserve existing setup-status, manual import, browser upload, folder upload, match-history, and game-history behavior.
- Produce the implementation handoff.

Do not:
- add arbitrary SQL, generic database browsing, or destructive database/UI controls
- create or apply migrations
- change analytics schema or ingest behavior
- query raw Player.log, raw JSONL, fact_provenance, rank snapshots, sideboarding/deck-state tables, gameplay action tables, opponent observation tables, annotation tables, or derived dashboard views in this slice
- add Line Tracer, opening-line recommendations, sample-size/dashboard summaries, coaching, best-keep advice, mulligan mistake labels, hidden-card inference, archetype inference, or player evaluation
- expose raw payloads, raw hashes, full paths, exception strings, stack traces, secrets, credentials, or local machine markers
- create or commit generated SQLite files, frontend build output, raw logs, JSONL artifacts, runtime files, failed posts, workbook exports, or local-only artifacts
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, output transport, production behavior, AI/OpenAI, Line Tracer, or coaching behavior
- target main
- close tracker #204 or umbrella #207
- stage, commit, push, open a PR, merge, or deploy unless explicitly asked

Validation:
py -m pytest -q tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/226"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #226 and current local app/analytics history implementation"
  target_artifact: "docs/contracts/analytics_app_opening_hand_mulligan_views.md"
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
    - "Do not add arbitrary SQL, generic database browsing, Line Tracer behavior, coaching, or destructive controls."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not change analytics schema, migrations, or ingest behavior in this slice."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```
