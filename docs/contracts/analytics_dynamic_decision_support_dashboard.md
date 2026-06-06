# Analytics Dynamic Decision Support Dashboard Contract

## Module

`analytics_dynamic_decision_support_dashboard`

Plain English: this contract defines a small dynamic dashboard module surface
for the local app `Decision Support` area. The dashboard should present
chart-ready, backend-shaped analytics modules that answer narrow competitive
review questions without becoming a generic database browser, coaching system,
Line Tracer, hidden-card inference tool, or parser-truth surface.

This is a contract-writing artifact only. It does not implement code, change
analytics schema, change parser behavior, add a charting library, or expose a
custom explorer builder UI.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/283
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Branch: `codex/analytics-foundation`
- Risk tier: High
- Source artifact: GitHub issue #283

Required repo authorities:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

## Owning Layer

Primary owning layer: Local App / UI.

Supporting storage/query layer: Analytics.

Truth boundaries:

- Parser/state owns parser-managed match facts, game facts, play/draw,
  mulligan facts, opening hand facts, gameplay-action facts, opponent-card
  observations, match/game identity, deduplication, and final reconciliation.
- SQLite analytics tables and deterministic views own local queryable storage
  and fixed downstream projections of parser-normalized facts.
- The local app backend owns the chart-ready dashboard module payloads, module
  status, metric/dimension definitions, data-quality labels, and fixed query
  selection.
- The frontend owns view selection, browser-storage preferences, display,
  accessibility, safe rendering, and user-facing status translation.
- Match Journal owns human annotations only. Journal labels must be marked as
  `Journal annotation` when they appear in future explorer vocabulary.

The dashboard may summarize stored analytics facts. It must not decide what
happened in Arena, reinterpret raw Player.log evidence, infer hidden cards,
classify archetypes as truth, judge player mistakes, recommend best lines, or
produce AI/coaching truth.

## Internal Project Area

Primary area: Local App / UI.

Bridge-code status: `bridge_code`.

Bridge details:

- source internal project area: Analytics
- consuming internal project area: Local App / UI
- allowed data flow: fixed SQLite analytics views and existing local app
  analytics helpers to backend module payloads to frontend dashboard display
- forbidden reverse-flow: frontend view preferences and module labels must not
  write back to SQLite, change analytics ingest, change parser facts, update
  workbook/runtime state, or become strategic truth
- protected surfaces explicitly not touched: parser behavior, analytics schema
  and migrations, analytics ingest, Match Journal truth ownership,
  workbook/webhook/App Script/Sheets, production behavior, generated/private
  artifacts, secrets, raw logs, Line Tracer, and AI/coaching surfaces

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_dynamic_decision_support_dashboard.md`

Future implementation files authorized for Codex C, subject to comparison and
validation:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/analytics_history.py`
- optional new helper module under `src/mythic_edge_parser/local_app/`, such as
  `analytics_dashboard.py`, if it keeps module payload code clearer than
  extending `analytics_history.py`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`, only for frontend status translation if needed
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- focused backend tests, expected as
  `tests/test_analytics_dynamic_decision_support_dashboard.py`
- focused route inventory additions in `tests/test_analytics_local_app_backend.py`
- `docs/implementation_handoffs/analytics_dynamic_decision_support_dashboard_comparison.md`

Reference-only source surfaces:

- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_app_first_screen_competitive_cockpit.md`
- `docs/contracts/analytics_app_match_game_history_views.md`
- `docs/contracts/analytics_app_opening_hand_mulligan_views.md`
- `docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md`
- `docs/contracts/analytics_app_play_draw_postboard_split_views.md`
- `docs/contracts/match_journal_cockpit_ui.md`
- `docs/contracts/match_journal_cockpit_write_controls.md`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- current local app backend, analytics history, frontend, and analytics app
  tests

Not owned by this contract:

- parser modules
- parser state final reconciliation
- parser event classes
- match/game identity or deduplication
- analytics schema migrations
- analytics ingest behavior
- runtime/live watcher behavior
- workbook schema, webhook payload shape, Apps Script behavior, or Google
  Sheets behavior
- Match Journal service/repository/write behavior
- raw Player.log files, private JSONL artifacts, generated SQLite files,
  frontend build output, failed posts, workbook exports, secrets, credentials,
  or local-only artifacts
- Line Tracer, AI/OpenAI, coaching, production behavior, CI gates, merge
  policy, or deploy policy

## Observed Current Behavior

Observed on `codex/analytics-foundation` during this contract pass:

- Issue #283 is open and routes through tracker #204 and umbrella #207.
- The branch is clean and even with `origin/codex/analytics-foundation`.
- The local app backend already exposes fixed read-only endpoints for:
  - `GET /api/analytics/matches`
  - `GET /api/analytics/games`
  - `GET /api/analytics/opening-hands`
  - `GET /api/analytics/mulligans`
  - `GET /api/analytics/gameplay-actions`
  - `GET /api/analytics/opponent-card-observations`
  - `GET /api/analytics/play-draw-splits`
  - `GET /api/analytics/game1-postboard-splits`
- `analytics_history.py` already has read-only builder functions and safe
  response shapes for match/game history, early-game history, action review,
  opponent observations, play/draw splits, and game 1/postboard rows.
- The SQLite schema already contains the views needed for the first two stock
  modules:
  - `v_play_draw_splits`
  - `v_sample_size_warnings`
  - `v_game1_vs_postboard`
- Opening-hand and mulligan fact tables and local app endpoints already exist,
  but there is no backend module that summarizes them as one chart-ready
  dashboard card.
- The frontend already has a `Decision Support` section with static cockpit
  insight modules.
- The current first dynamic module, `Win rate by play/draw`, is assembled in
  the frontend from split-review endpoint rows.
- The current `Matchup by archetype` and `High-performing lines` modules are
  placeholder/deferred-style modules. They are not approved as dynamic
  dashboard modules in this issue.
- The frontend already renders hand-built bar visuals in CSS and does not use a
  charting library.
- The frontend already loads detailed tables below the dashboard in a
  `Review Details` area.
- There is no single backend endpoint that returns chart-ready dashboard module
  payloads with module IDs, decision questions, metric definitions, dimensions,
  warnings, source metadata, and view affordances.
- There is no browser-storage preference for per-module `bar` versus `table`
  display.
- There is no durable contract for custom explorer dimensions/metrics.

## Contract Decision

Issue #283 should authorize a backend-led, chart-ready dashboard module API and
a frontend renderer for approved stock modules.

Approved first slice:

- add one fixed read-only backend route:
  `GET /api/analytics/dashboard/modules`;
- return chart-ready payloads for exactly three stock modules:
  - `play_draw_win_rate`
  - `game1_postboard`
  - `mulligan_opening_hand_outcomes`
- render the modules inside the existing frontend `Decision Support` area;
- support `bar` and `table` display modes without adding a charting library;
- remember per-module display mode in browser storage;
- define custom explorer vocabulary but defer custom explorer UI and query
  execution;
- keep all modules descriptive and review-oriented.

Not approved:

- arbitrary SQL;
- generic database browsing;
- custom explorer builder UI;
- charting library dependency;
- analytics schema or migration changes;
- analytics ingest changes;
- parser behavior changes;
- Match Journal write or truth-ownership changes;
- hidden-card, archetype-as-truth, best-line, player-mistake, Line Tracer, AI,
  or coaching claims.

## Public Backend Interface

### Endpoint

Codex C may add exactly this first dashboard endpoint:

```text
GET /api/analytics/dashboard/modules
```

No query parameters are authorized in the first slice.

Forbidden backend interface expansion:

- arbitrary SQL input;
- table name, column name, order-by, where-clause, filter, search, group-by, or
  raw query input;
- custom explorer query execution;
- database browsing endpoints;
- database reset/delete/vacuum/export endpoints;
- schema/migration endpoints;
- import behavior changes;
- live Player.log watcher controls;
- Match Journal write controls;
- Google Sheets, workbook, webhook, Apps Script, Line Tracer, AI/OpenAI, or
  coaching endpoints.

### Response Object

The endpoint must return:

```text
object: mythic_edge_local_app_analytics_dashboard_modules
schema_version: analytics_dynamic_decision_support_dashboard.v1
```

Top-level response shape:

- `object`
- `schema_version`
- `status`
- `database`
- `modules`
- `custom_explorer`
- `warnings`
- `errors`

Allowed `status` labels:

- `ok`: schema-current database queried successfully and at least one module is
  available with rows or a valid empty state
- `empty`: schema-current database queried successfully but all modules have no
  rows
- `missing`: analytics database is absent
- `unavailable`: app data root or database path is unavailable
- `degraded`: database is readable but schema is missing, unknown, outdated, or
  one or more modules cannot be safely built
- `error`: database is invalid, unreadable, or a fixed module query failed

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

## Dashboard Module Shape

Each entry in `modules` must include:

- `module_id`
- `title`
- `decision_question`
- `status`
- `tone`
- `default_view`
- `allowed_views`
- `metric`
- `dimensions`
- `rows`
- `summary`
- `warnings`
- `errors`
- `data_quality`
- `source_metadata`
- `schema_version`

Allowed module `status` labels:

- `ok`
- `empty`
- `missing`
- `unavailable`
- `degraded`
- `error`
- `deferred`

Allowed module `tone` labels:

- `ok`
- `empty`
- `limited`
- `degraded`
- `blocked`
- `deferred`

Allowed view labels:

- `bar`
- `table`

`default_view` must be one of `allowed_views`.

### Metric Shape

Each module `metric` must include:

- `metric_id`
- `label`
- `value`
- `value_kind`
- `unit`
- `display`
- `calculation_note`
- `source`

Allowed `value_kind` labels:

- `count`
- `ratio`
- `percentage`
- `text`
- `null`

The metric must be descriptive. It must not claim statistical significance,
causation, strategic quality, optimal play, matchup truth, archetype truth, or
coaching conclusions.

### Dimension Shape

Each module `dimensions` entry must include:

- `dimension_id`
- `label`
- `source`
- `value_source`
- `allowed_values`, when useful
- `annotation_boundary`, when the dimension can come from Match Journal

Allowed `value_source` labels:

- `parser_normalized`
- `analytics_derived`
- `journal_annotation`
- `display_only`

`journal_annotation` dimensions must include `annotation_boundary:
"Journal annotation"`.

### Row Shape

Each module row must include:

- `row_id`
- `label`
- `dimension_values`
- `metrics`
- `status`
- `tone`
- `sample_size`
- `warnings`
- `source_metadata`

Each row metric must include:

- `metric_id`
- `label`
- `value`
- `value_kind`
- `unit`
- `display`

Rows must not include raw SQL, raw payloads, raw paths, raw hashes, private file
identifiers, raw Player.log content, private JSONL content, or arbitrary local
artifact identifiers.

### Data Quality Shape

Each module `data_quality` object must include:

- `status`
- `sample_size_status`
- `known_result_count`
- `unknown_or_degraded_count`
- `review_required_count`
- `confidence`
- `finality`
- `notes`

Allowed `sample_size_status` labels:

- `ok`
- `small_sample`
- `empty`
- `unknown`

Data-quality labels are display guardrails only. They must not become release
readiness, merge readiness, statistical proof, or coaching truth.

### Source Metadata Shape

Each `source_metadata` object must include:

- `source_tables_or_views`
- `source_contracts`
- `source_type`
- `parser_truth_boundary`
- `analytics_truth_boundary`
- `generated_at`, optional

Allowed `source_type` labels:

- `fixed_sql_view`
- `fixed_backend_projection`
- `fixed_backend_aggregation`
- `deferred_contract_surface`

`source_tables_or_views` may name safe schema objects such as
`v_play_draw_splits`; it must not include raw SQL text or private local paths.

## First Stock Modules

### `play_draw_win_rate`

Decision question:

```text
Am I performing differently on the play versus on the draw?
```

Required source:

- `v_play_draw_splits`
- `v_sample_size_warnings`

Recommended backend reuse:

- existing `build_play_draw_split_review(...)`

Required module configuration:

- `title`: `Win Rate By Play/Draw`
- `default_view`: `bar`
- `allowed_views`: `["bar", "table"]`

Required rows:

- one row per stored play/draw group
- `play`, `draw`, and `unknown` must stay separate when present
- win rate must remain calculated over known win/loss rows only
- unknown, unavailable, and degraded counts must remain visible
- sample-size warnings must remain visible

Forbidden interpretation:

- do not claim play/draw causes the result;
- do not turn the split into mulligan, matchup, deck quality, or player skill
  truth.

### `game1_postboard`

Decision question:

```text
Are my game 1 and postboard games showing different observed results?
```

Required source:

- `v_game1_vs_postboard`

Recommended backend reuse:

- existing `build_game1_postboard_split_review(...)`

Required module configuration:

- `title`: `Game 1 / Postboard`
- `default_view`: `bar`
- `allowed_views`: `["bar", "table"]`

Required rows:

- at minimum, grouped dashboard rows for `game1`, `postboard`, and `unknown`
  when present
- known win/loss counts must remain separate from unknown/degraded rows
- row or module warnings must show when data is limited, unavailable, or
  degraded
- postboard labels are descriptive context only

Forbidden interpretation:

- do not infer sideboard plan quality;
- do not infer sideboard-delta truth;
- do not explain why postboard games changed;
- do not provide deck construction, matchup, or gameplay advice.

### `mulligan_opening_hand_outcomes`

Decision question:

```text
Are my keep and mulligan patterns associated with observed outcomes?
```

Required source:

- `opening_hands`
- `mulligan_events`
- existing opening-hand and mulligan local app projections when practical
- `games`, `game_results`, `matches`, `match_results`, and `match_context`
  only as already-approved context sources

Recommended backend reuse:

- existing `build_opening_hand_history(...)`
- existing `build_mulligan_history(...)`

Required module configuration:

- `title`: `Mulligan / Opening Hand Outcomes`
- `default_view`: `table`
- `allowed_views`: `["bar", "table"]`

Required rows:

- grouped rows by safe display buckets such as opening hand size, mulligan
  count, or keep/mulligan state
- known result counts, wins, losses, unknown/degraded counts, and sample-size
  labels
- no individual hidden card inference
- no keep/mulligan quality judgment

Forbidden interpretation:

- do not label a keep or mulligan as correct or incorrect;
- do not label player mistakes;
- do not recommend keeps, mulligans, lines, or sideboard choices;
- do not infer hidden cards or complete decklists.

## Backend Query Contract

Dashboard module generation must:

- use the app-owned local analytics database path from `build_local_app_paths`;
- open the database read-only when querying rows;
- avoid creating app folders or database files for missing-database reads;
- avoid applying migrations;
- avoid changing migration status;
- avoid writing temp tables, materialized summaries, WAL files by design, or
  runtime artifacts;
- use fixed parameterized SQL;
- close SQLite connections deterministically;
- return safe shaped status payloads for missing, empty, degraded, unavailable,
  and error states;
- reuse existing local app analytics history helpers where practical;
- fail closed when a module cannot be safely built.

Allowed first-slice tables/views:

- `v_play_draw_splits`
- `v_sample_size_warnings`
- `v_game1_vs_postboard`
- `opening_hands`
- `mulligan_events`
- `games`
- `game_results`
- `matches`
- `match_results`
- `match_context`

Allowed only through existing helper reuse when needed:

- `opening_hand_cards`
- `mulligan_bottomed_or_discarded_cards`

Forbidden first-slice sources:

- raw local files;
- raw JSONL artifacts;
- raw Player.log contents;
- arbitrary SQL;
- `fact_provenance`, unless a future contract defines provenance-rich
  dashboard modules;
- sideboarding/deck-state tables;
- rank snapshots;
- Match Journal tables for first-slice stock modules;
- `v_opening_lines`;
- `v_matchup_label_performance`;
- annotation tables such as matchup labels, archetype labels, or game notes;
- gameplay-action and opponent-observation tables for the first three stock
  modules.

`v_opening_lines`, matchup label performance, gameplay-action summaries,
opponent-observation summaries, and Journal-backed dimensions remain custom
explorer vocabulary only until a later issue authorizes a module or builder.

## Frontend Interface And Rendering Boundary

The frontend may:

- fetch `GET /api/analytics/dashboard/modules`;
- validate `object` and `schema_version`;
- render approved modules inside the existing `Decision Support` area;
- render `bar` and `table` views using plain React/CSS;
- preserve existing detailed table sections below the dashboard;
- translate backend module statuses into user-facing labels;
- show empty, missing, unavailable, degraded, error, small-sample, and
  review-required states clearly;
- show warnings and data-quality labels without turning them into strategy;
- remember per-module preferred view in browser storage.

The frontend must not:

- compute canonical module rows from raw tables when the backend module
  endpoint is available;
- become the analytics engine;
- write SQLite directly;
- execute SQL;
- expose custom explorer builder UI;
- add a charting library;
- infer hidden cards, archetypes, mistakes, best lines, or coaching
  conclusions;
- convert Journal labels, UI labels, or browser storage values into parser or
  analytics truth;
- expose raw/private/generated/local artifact values.

### Bar View Requirements

Bar views must:

- use stable dimensions and responsive constraints;
- include text labels and numeric display values;
- avoid color-only meaning;
- avoid negative letter spacing and viewport-width font scaling;
- handle zero/null values without layout shifts;
- clearly label limited, unknown, or degraded data.

### Table View Requirements

Table views must:

- show row labels, dimensions, metrics, status, and warnings;
- remain read-only;
- preserve safe display/redaction behavior;
- avoid raw backend error details;
- not expose arbitrary database columns.

## Browser Storage Contract

The frontend may store only module view preferences in browser storage.

Recommended key:

```text
mythic_edge.analytics.dashboard.module_view_preferences.v1
```

Allowed stored shape:

```json
{
  "play_draw_win_rate": "bar",
  "game1_postboard": "bar",
  "mulligan_opening_hand_outcomes": "table"
}
```

Rules:

- Store only module IDs and selected view labels.
- Ignore unknown module IDs.
- Ignore unknown view labels.
- Fall back to the backend `default_view` when storage is unavailable,
  malformed, or unsupported.
- Do not store rows, metrics, raw data, private paths, Player.log content,
  JSONL contents, SQL, secrets, local artifact identifiers, hashes, or
  generated database values.
- Browser-storage failures must not block dashboard rendering.

## Custom Explorer Contract

This contract defines vocabulary only. It does not authorize a custom explorer
builder UI or custom query execution.

Allowed future dimension vocabulary:

- `date_time_bucket`
- `play_draw`
- `game1_postboard`
- `match_result`
- `game_result`
- `mulligan_count`
- `opening_hand_size`
- `queue`
- `format`
- `event`
- `card_name`
- `grp_id`
- `gameplay_action_type`
- `opponent_observed_card`
- `journal_matchup_label`
- `journal_archetype_label`

Allowed future metrics vocabulary:

- `games_played`
- `matches_played`
- `wins`
- `losses`
- `win_rate`
- `known_result_count`
- `unknown_degraded_count`
- `sample_size_warning_count`
- `review_required_count`

Journal-backed dimensions must be labeled as `Journal annotation`.

Forbidden or deferred custom explorer behavior:

- arbitrary SQL;
- freeform table/column picker;
- hidden cards;
- complete opponent decklists;
- opponent archetype as parser truth;
- best line or correct play;
- mistake or punt labels;
- strategic quality;
- coaching conclusions;
- AI-generated advice;
- raw Player.log contents;
- private JSONL payloads;
- raw hashes or private artifact identifiers;
- browser-side analytics truth.

## Journal Annotation Boundary

Match Journal labels may be future custom explorer dimensions only when all of
the following are true:

- the value is clearly marked as `Journal annotation`;
- the value is displayed as a human-entered label;
- the value does not become parser truth, analytics truth, matchup truth,
  archetype truth, hidden-card truth, coaching truth, or release readiness;
- the query path is fixed and separately contracted.

Issue #283 does not authorize Match Journal-backed stock modules.

## Error Behavior

Missing database:

- return top-level `status = "missing"`;
- return `modules` with empty or unavailable module states;
- return a symbolic database display path;
- do not create folders or database files.

Unavailable app data root:

- return `status = "unavailable"`;
- return no module rows;
- do not create folders or database files.

Unmigrated, unknown, or outdated schema:

- return `status = "degraded"`;
- return no module rows or degraded module states;
- include stable warning code such as `analytics_schema_not_current`;
- do not run row queries against unsafe schema;
- do not apply migrations.

Empty schema-current database:

- return `status = "empty"`;
- return the three module entries with empty rows and clear empty-state
  summaries.

Invalid SQLite, unreadable database, or fixed query failure:

- return `status = "error"` or per-module `status = "error"`;
- include stable error codes only;
- do not expose exception strings, SQL text, absolute paths, raw payloads, raw
  hashes, stack traces, secrets, or local usernames.

Malformed frontend response:

- frontend validation must fail closed;
- show a safe dashboard unavailable/degraded state;
- do not display raw backend details.

Browser-storage failure:

- ignore stored preferences;
- use backend defaults;
- do not block dashboard rendering.

## Side Effects

Allowed side effects:

- read-only HTTP responses;
- frontend render state;
- browser-storage writes containing only module view preferences;
- test-created temporary SQLite databases under pytest temp directories;
- implementation handoff documentation.

Forbidden side effects:

- parser behavior changes;
- parser state final reconciliation changes;
- parser event class changes;
- match/game identity or deduplication changes;
- analytics schema or migration changes;
- analytics ingest changes;
- generated repo-local SQLite files;
- raw log, raw JSONL, runtime status, failed-post, workbook export, frontend
  build output, or local artifact writes;
- workbook/webhook/App Script/Sheets writes;
- external network calls beyond local backend/frontend loopback in tests;
- OpenAI/model-provider calls;
- issue closure, tracker closure, PR creation, staging, commit, push, merge, or
  deploy actions unless explicitly requested in a later role.

## Compatibility

Implementation must preserve:

- existing setup/status endpoints;
- existing manual import, upload, folder upload, and import-job behavior;
- existing match/game history endpoints and frontend display;
- existing opening-hand/mulligan endpoints and frontend display;
- existing gameplay-action/opponent-observation endpoints and frontend display;
- existing play/draw and game 1/postboard split endpoints and frontend
  detailed tables;
- existing Match Journal cockpit behavior;
- existing error-report preview behavior;
- existing frontend API base URL loopback validation;
- existing redaction/safe-display behavior;
- existing no-chart-library posture.

The new dashboard endpoint may reuse existing helper functions, but it must not
break their existing response objects or schema versions.

## Unknowns

- The best visual density for the three module cards is not yet proven.
  Codex C may choose compact cards, segmented controls, or small table
  toggles as long as the module payload and view boundaries remain intact.
- The exact aggregation for `mulligan_opening_hand_outcomes` may need to be
  conservative if current data has sparse rows. Empty or limited-data states
  are acceptable.
- Future custom explorer UX is intentionally unresolved. This contract defines
  vocabulary only.
- It is unknown whether future dashboard modules should use gameplay-action or
  opponent-observation rows. Those are deferred.
- It is unknown whether Journal-backed matchup/archetype labels should become
  dashboard dimensions. This must remain a later contract.

## Suspected Gaps

- Backend: no dashboard module response builder exists.
- Backend: no route tests prove dashboard module payload shape, degraded
  database states, empty module states, or privacy-safe source metadata.
- Frontend: `Decision Support` modules are partly frontend-composed and partly
  placeholder/deferred.
- Frontend: no typed dashboard module response model exists.
- Frontend: no module-level `bar`/`table` preference storage exists.
- Frontend: no tests prove custom explorer builder UI is absent while explorer
  vocabulary is documented.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity;
- deduplication;
- analytics schema, migrations, or ingest semantics;
- live watcher behavior;
- Match Journal service/repository/write behavior;
- Match Journal truth ownership;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- hidden-card inference;
- archetype inference as truth;
- player-mistake labels;
- gameplay advice;
- secrets, credentials, tokens, endpoint values, spreadsheet IDs, or
  environment values;
- raw logs, private JSONL artifacts, generated SQLite databases, SQLite sidecar
  files, runtime files, transport-failure artifacts, workbook exports,
  frontend build output, app-data files, generated data, or local-only
  artifacts.

## Tests Required

Codex C must add or update backend tests proving:

- `GET /api/analytics/dashboard/modules` is present;
- unknown query parameters are rejected or ignored according to one stable
  documented behavior, without enabling arbitrary filters;
- missing database returns a safe `missing` response;
- unavailable app data returns a safe `unavailable` response;
- non-current schema returns a safe `degraded` response;
- schema-current empty database returns three empty module entries;
- schema-current populated database returns the three required module IDs;
- each module includes required fields, metric shape, dimension shape, row
  shape, data-quality shape, and source metadata;
- source metadata does not contain SQL text, absolute paths, raw payloads,
  hashes, secrets, or private local artifact identifiers;
- module generation uses read-only database access and does not apply
  migrations.

Codex C must add or update frontend tests proving:

- the `Decision Support` area renders backend-provided dashboard modules;
- all three first stock modules appear;
- `bar` and `table` views are available where allowed;
- per-module view preferences persist in browser storage as module ID to view
  label only;
- malformed or unsupported stored preferences are ignored safely;
- no charting library dependency is required;
- no custom explorer builder UI is visible;
- no arbitrary SQL/database browsing is visible;
- empty, degraded, unavailable, error, and small-sample states render safely;
- Journal-backed labels, if ever named in explorer vocabulary, are displayed
  only as deferred/annotation vocabulary and not as active parser truth;
- hidden-card, coaching, best-line, archetype-truth, player-mistake, and Line
  Tracer claims are absent;
- destructive controls remain absent;
- unsafe values remain redacted.

Recommended Codex C validation:

```powershell
py -m pytest -q tests\test_analytics_dynamic_decision_support_dashboard.py tests\test_analytics_app_play_draw_postboard_split_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
```

Codex C and Codex E must also report:

- no generated SQLite files, WAL files, SHM files, journal files, raw logs,
  raw JSONL files, failed posts, workbook exports, runtime artifacts, frontend
  build output, or secrets were created or committed;
- no arbitrary SQL, database browsing, destructive routes, charting library, or
  destructive UI controls were added;
- no raw payloads, raw hashes, private paths, exception strings, stack traces,
  local usernames, credentials, coaching advice, hidden-card claims, best-line
  labels, archetype-truth labels, causation claims, or player mistake labels
  appear in endpoint responses or UI output;
- protected-surface scan results for changed paths;
- secret/private-marker scan results for changed paths.

If `npm --prefix frontend run build` creates `frontend/dist`, generated build
output must be removed before final handoff unless a later contract explicitly
authorizes committing it.

## Acceptance Criteria

- `docs/contracts/analytics_dynamic_decision_support_dashboard.md` exists.
- The contract defines `GET /api/analytics/dashboard/modules`.
- The contract defines the dashboard response object and schema version.
- The contract defines module fields, metric fields, dimension fields, row
  fields, warning/error fields, data-quality fields, and source metadata.
- The contract defines the three stock modules and maps each to current
  analytics data.
- The contract defines default and allowed views for each module.
- The contract defines backend ownership versus frontend rendering ownership.
- The contract defines browser-storage preference boundaries.
- The contract defines custom explorer vocabulary while deferring builder UI
  and query execution.
- The contract preserves Journal annotation boundaries.
- The contract forbids arbitrary SQL, charting library dependency, custom
  explorer builder UI, hidden-card inference, coaching claims, and parser-truth
  changes.
- No implementation, parser, analytics schema/migration/ingest, workbook,
  webhook, Apps Script, runtime, generated-data, OpenAI/AI, Line Tracer,
  coaching, or production behavior changes are made in the contract-writing
  pass.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #283.

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

Goal:
Compare the current local app backend, frontend, analytics schema/views, and tests against the contract. Implement only the dynamic Decision Support dashboard modules slice and focused tests. Produce docs/implementation_handoffs/analytics_dynamic_decision_support_dashboard_comparison.md.

Before editing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what the dashboard modules are supposed to do, what the app currently does, what gap remains, and the exact minimal implementation plan.

Do:
- Add fixed read-only GET /api/analytics/dashboard/modules.
- Return object mythic_edge_local_app_analytics_dashboard_modules with schema_version analytics_dynamic_decision_support_dashboard.v1.
- Build exactly the first three stock modules: play_draw_win_rate, game1_postboard, and mulligan_opening_hand_outcomes.
- Reuse existing local app analytics history/split helpers where practical.
- Use only fixed read-only SQLite queries over the allowed tables/views.
- Preserve unknown, unavailable, degraded, conflict, sample-size, source, confidence, finality, and data-quality labels where available.
- Render the modules inside the existing Decision Support area.
- Support bar and table views without adding a charting library.
- Store only module ID to selected view labels in browser storage.
- Define custom explorer vocabulary in code/types/docs only as needed for response display; do not expose builder UI.
- Add focused backend and frontend tests for success, empty, missing, degraded, error, response validation, browser-storage preference behavior, no charting dependency, no custom explorer UI, safe display, and read-only boundaries.
- Produce the implementation handoff.

Do not:
- add a charting library
- implement custom explorer builder UI
- add arbitrary SQL, generic database browsing, or destructive database/UI controls
- create or apply migrations
- change analytics schema, derived SQL view definitions, or ingest behavior
- query raw Player.log, raw JSONL, fact_provenance, sideboarding/deck-state tables, rank snapshots, Match Journal tables, annotation tables, v_opening_lines, v_matchup_label_performance, gameplay-action tables, or opponent-observation tables for this first dashboard slice
- add Line Tracer, opening-line recommendations, first-three-turn best-line summaries, sample-size significance claims, coaching, hidden-card inference, complete decklist inference, sideboard-delta inference, archetype inference as truth, action quality ratings, causation claims, player mistake labels, strategic advice, or player evaluation
- expose raw payloads, raw hashes, full paths, exception strings, stack traces, secrets, credentials, or local machine markers
- create or commit generated SQLite files, frontend build output, raw logs, JSONL artifacts, runtime files, failed posts, workbook exports, or local-only artifacts
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, live watcher behavior, Match Journal truth ownership, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, output transport, production behavior, AI/OpenAI, Line Tracer, or coaching behavior
- target main
- close tracker #204 or umbrella #207
- stage, commit, push, open a PR, merge, or deploy unless explicitly asked

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
If npm build creates frontend/dist, remove generated build output before final handoff unless a later contract explicitly authorizes committing it.

Final handoff must include role performed, source issue/tracker, contract used, files changed, exact backend/frontend/test sections changed, validation run, protected-surface status, generated/private artifact status, remaining risk, next recommended role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/283"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #283"
  target_artifact: "docs/implementation_handoffs/analytics_dynamic_decision_support_dashboard_comparison.md"
  contract_artifact: "docs/contracts/analytics_dynamic_decision_support_dashboard.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "Codex B docs-only validation: git diff --check"
    - "Codex B docs-only validation: py tools\\check_agent_docs.py"
    - "Codex B docs-only validation: path-scoped protected-surface scan for the contract"
    - "Codex B docs-only validation: path-scoped secret/private-marker scan for the contract"
    - "Codex C should run backend, frontend, schema/view, ruff, generated-artifact, protected-surface, and secret/private-marker checks"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not add a charting library."
    - "Do not implement custom explorer builder UI."
    - "Do not expose arbitrary SQL or destructive database/UI controls."
    - "Do not turn dashboard modules into Line Tracer, coaching, causation, hidden-card, archetype, player-mistake, or best-line truth."
    - "Do not change parser/runtime/analytics schema/analytics ingest/live watcher/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```
