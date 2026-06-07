# Analytics App Play/Draw And Postboard Split Views Contract

## Module

Local developer app curated play/draw and game 1/postboard split review views.

This contract covers a read-only local app surface over deterministic analytics
views already present in the local SQLite analytics database:

- `v_play_draw_splits`
- `v_sample_size_warnings`
- `v_game1_vs_postboard`

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/229
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Completed prerequisite: https://github.com/Tahjali11/Mythic-Edge/issues/225
- Completed prerequisite: https://github.com/Tahjali11/Mythic-Edge/issues/226
- Completed prerequisite: https://github.com/Tahjali11/Mythic-Edge/issues/228

Required repo authorities:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

## Branch

`codex/analytics-foundation`

## Risk Tier

High.

Reason: split summaries are easy to overread as strategy, causation, player
skill, matchup truth, or coaching advice. This slice must stay descriptive and
review-oriented. It may show "what the stored data says"; it must not say why
games were won or lost, what line was correct, or what the player should do
differently.

## Owning Layer

Primary owning layer: Local App / UI.

Supporting storage/query layer: Analytics.

Truth boundaries:

- Parser/state owns parser-managed match facts, game facts, result facts,
  play/draw labels, pre/postboard labels, match/game identity, deduplication,
  and final reconciliation.
- SQLite analytics tables own local durable storage of parser-normalized facts
  and provenance/status labels.
- Derived SQL views own deterministic read-only projections over stored facts.
- The local app backend owns fixed read-only API projections over the local
  analytics database.
- The local app frontend owns display and local interaction.
- Neither SQLite nor the UI may reinterpret raw Arena events, infer missing
  facts, claim causation, judge strategic quality, classify archetypes, label
  player mistakes, provide best-line recommendations, or become coaching truth.

Plain English: this view may show "how did my imported games split by play/draw
and by game 1 versus postboard?" It must not answer "why did that happen?" or
"what should I do next time?"

## Internal Project Area

Primary area: Local App / UI.

Bridge-code status: `bridge_code`.

Bridge details:

- source internal project area: Analytics
- consuming internal project area: Local App / UI
- allowed data flow: SQLite analytics split views to fixed local backend
  responses to frontend display
- forbidden reverse-flow: frontend/backend split views must not write back to
  SQLite, change analytics ingest, change parser facts, update workbook/runtime
  state, or feed strategic conclusions into parser/analytics truth
- protected surfaces explicitly not touched: parser behavior, analytics schema
  and migrations, analytics ingest, workbook/webhook/App Script/Sheets,
  production behavior, generated/private/local artifacts, secrets, raw logs,
  Line Tracer, and AI/coaching surfaces

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_app_play_draw_postboard_split_views.md`

Future implementation files authorized for Codex C, subject to comparison and
validation:

- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/backend.py`
- optional new helper module under `src/mythic_edge_parser/local_app/` only if
  the existing history helper becomes too large
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- focused backend tests, expected as
  `tests/test_analytics_app_play_draw_postboard_split_views.py`
- focused route inventory additions in `tests/test_analytics_local_app_backend.py`
- `docs/implementation_handoffs/analytics_app_play_draw_postboard_split_views_comparison.md`

Reference-only source surfaces:

- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_app_match_game_history_views.md`
- `docs/contracts/analytics_app_opening_hand_mulligan_views.md`
- `docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md`
- `docs/contracts/analytics_derived_sql_views.md`
- `docs/contracts/analytics_replay_view_validation_harness.md`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- current local app, analytics derived-view, replay/view, backend, and frontend
  tests

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

The local app split review response schema version is:

```text
analytics_app_play_draw_postboard_split_views.v1
```

This version is intentionally separate from match/game history, early-game
history, and action review because the row shapes are split summaries and
game-result review rows rather than direct fact-table history rows.

### Backend Endpoints

Codex C may add exactly these split review endpoints:

```text
GET /api/analytics/play-draw-splits
GET /api/analytics/game1-postboard-splits
```

Allowed query parameters:

- `limit`: optional integer, default `50`, minimum `1`, maximum `100`
- `offset`: optional integer, default `0`, minimum `0`

The play/draw split endpoint should normally return all current split groups by
using the default query. The parameters are allowed only for response-shape and
route-safety consistency with existing analytics history endpoints.

No other query parameters are authorized in this slice.

Query parameter parsing must reuse or match the existing sanitized analytics
history pagination behavior: malformed, duplicate, out-of-range, or unapproved
query parameters must produce stable error codes without echoing raw input.

Forbidden backend interface expansion:

- arbitrary SQL input
- table name, column name, order-by, where-clause, filter, search, or raw query
  input
- database browsing endpoints
- database reset/delete/vacuum/export endpoints
- schema/migration endpoints
- import behavior changes
- live Player.log watcher endpoints
- opening-line, Line Tracer, AI/OpenAI, coaching, Match Journal, Google Sheets,
  or workbook endpoints

### Response Object Names

`GET /api/analytics/play-draw-splits` must return:

```text
object: mythic_edge_local_app_play_draw_split_review
schema_version: analytics_app_play_draw_postboard_split_views.v1
```

`GET /api/analytics/game1-postboard-splits` must return:

```text
object: mythic_edge_local_app_game1_postboard_split_review
schema_version: analytics_app_play_draw_postboard_split_views.v1
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
- `degraded`: database is readable but schema is missing, unknown, outdated, or
  not safe to query for this response shape
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

Pagination is a display/API concern only. It must not change base analytics
rows or imply statistical significance.

## Backend Query Contract

### Database Access

Split review endpoints must:

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

- reuse the existing database status, pagination, payload, summary, and status
  helpers from `analytics_history.py` where practical
- query rows only when the database exists and `schema_status` is
  `schema_current`
- use `sqlite3.Row` or structured row mapping
- use `LIMIT ? OFFSET ?` with validated integers

### Allowed Tables And Views

The play/draw split endpoint may query only:

- `v_play_draw_splits`
- `v_sample_size_warnings`

The game 1/postboard split endpoint may query only:

- `v_game1_vs_postboard`

Codex C may query `game_results` directly only if the existing view is missing
a field that the current issue requires and only after documenting the reason
in the implementation handoff. Codex C must not change the schema or view
definition in this issue.

The first slice must not query:

- raw local files
- raw JSONL artifacts
- raw Player.log contents
- `fact_provenance`
- opening hand tables
- mulligan tables
- gameplay action tables
- opponent-card-observation tables
- sideboarding or deck-state tables
- rank snapshots
- annotation tables such as matchup labels, archetype labels, or game notes
- Match Journal tables or future note/label tables
- derived dashboard views such as `v_opening_lines` or
  `v_matchup_label_performance`

`v_opening_lines`, Line Tracer-style views, matchup/label summaries, note
surfaces, AI/coaching views, and future causal analysis remain deferred.

## Play/Draw Split Response

`GET /api/analytics/play-draw-splits` returns one row per stored
`v_play_draw_splits.play_draw` group.

Each row must include:

- `play_draw`
- `game_count`
- `known_result_count`
- `wins`
- `losses`
- `unknown_result_count`
- `unavailable_result_count`
- `degraded_result_count`
- `win_rate`
- `sample_size_warning`

Required row behavior:

- Missing or blank play/draw values remain grouped as `unknown` by the
  underlying view.
- `known_result_count` counts only rows whose `local_result` is `win` or
  `loss`.
- `wins` and `losses` remain separate counts.
- `unknown_result_count` remains separate from losses.
- `unavailable_result_count` remains separate from losses.
- `degraded_result_count` remains visible and must not be hidden by win-rate
  formatting.
- `win_rate` is `null` when there are no known win/loss rows.
- `sample_size_warning` must come from `v_sample_size_warnings` or be `null`
  when no matching warning row exists.

Expected summary shape:

```json
{
  "row_count": 0,
  "total_game_count": 0,
  "known_result_count": 0,
  "wins": 0,
  "losses": 0,
  "unknown_result_count": 0,
  "unavailable_result_count": 0,
  "degraded_result_count": 0,
  "small_sample_group_count": 0
}
```

The summary is a convenience rollup over response rows. It is not parser truth,
statistical truth, matchup truth, or coaching truth.

Required deterministic order:

```text
CASE play_draw WHEN 'play' THEN 0 WHEN 'draw' THEN 1 WHEN 'unknown' THEN 2 ELSE 3 END ASC,
play_draw ASC
```

## Game 1/Postboard Split Response

`GET /api/analytics/game1-postboard-splits` returns one row per stored
`v_game1_vs_postboard` row.

Each row must include:

- `game_result_id`
- `match_id`
- `game_id`
- `game_number`
- `pre_postboard_label`
- `local_result`
- `play_draw`
- `turn_count`
- `game_duration_seconds`
- `game_result_status`

`game_result_status` is a status object built from the view columns:

- `value_source`
- `confidence`
- `finality`
- `drift_status`
- `availability_status`
- `source_parser_surface`
- `source_fact_key`
- `ingest_run_id`

Required row behavior:

- `pre_postboard_label` is descriptive context only.
- `game1`, `preboard`, `postboard`, `unknown`, null, and blank values must not
  be upgraded into deck-state proof or sideboard-plan proof.
- Unknown or nonstandard `local_result` values must remain visible and must not
  be counted as losses.
- Missing `turn_count` or `game_duration_seconds` must remain null rather than
  being inferred.
- The response must not compare or explain why game 1 and postboard outcomes
  differ.

Expected summary shape:

```json
{
  "row_count": 0,
  "game1_row_count": 0,
  "postboard_row_count": 0,
  "known_result_count": 0,
  "unknown_result_count": 0,
  "degraded_row_count": 0,
  "unavailable_row_count": 0,
  "conflict_row_count": 0
}
```

Required deterministic order:

```text
match_id DESC,
game_number ASC,
game_result_id ASC
```

Codex C may use a more recent-first order only if it can do so through already
allowed data without changing schema, ingest, or parser behavior. The chosen
order must be stable and tested.

## Sample-Size Warning Policy

Sample-size warnings are descriptive display guardrails.

Required behavior:

- Use `v_sample_size_warnings.sample_size_warning` for play/draw groups.
- Preserve the current labels `small_sample` and `ok`.
- If the current view later emits `empty_sample`, the endpoint may pass it
  through without a schema change.
- If the endpoint sees an unexpected warning label, it may pass through the
  safe string as a display label, but frontend copy must not treat it as
  strategy or statistical truth.
- Empty play/draw responses may include a stable warning such as
  `split_review_no_games` if Codex C finds that clearer for UI display.

Sample-size warnings must not become:

- statistical significance claims
- matchup truth
- deck quality truth
- player skill truth
- Line Tracer readiness
- AI readiness
- coaching advice
- merge readiness or deploy readiness

## Frontend Display Contract

The frontend may add a curated Split Review section near the existing Analytics
History, Early Game History, and Action Review sections.

Required frontend behavior:

- fetch `GET /api/analytics/play-draw-splits`
- fetch `GET /api/analytics/game1-postboard-splits`
- validate response `object` and `schema_version`
- show play/draw rows with game count, known-result count, wins, losses,
  unknown-result count, unavailable-result count, degraded-result count, win
  rate, and sample-size warning
- show game 1/postboard rows with match/game identity, game number,
  pre/postboard label, local result, play/draw, turn count, duration, and
  status/provenance labels
- show loading, empty, missing, degraded, unavailable, and error states
- reuse existing analytics history visual/status patterns where practical
- preserve existing setup-status, manual-import, browser-upload, folder-upload,
  match/history, early-game history, and action review behavior
- keep all split review actions read-only
- show safe counts from `summary`
- use copy that frames rows as descriptive summaries, not recommendations

Allowed read-only frontend action:

- a refresh control that re-fetches the split review endpoints

Codex C may either:

- extend the existing Analytics History refresh pattern with a split-specific
  refresh, or
- add a separate Split Review refresh inside the same read-only analytics area

Forbidden frontend behavior:

- arbitrary SQL entry
- table picker or column picker
- edit/delete/reset/vacuum/export controls
- database initialization controls
- import controls inside the split review section
- live watcher controls
- Match Journal editing
- matchup/archetype labeling or game notes editing
- Line Tracer behavior
- opening-line recommendations
- first-three-turn best-line summaries
- action quality ratings
- causal language about why games were won or lost
- hidden-card inference
- decklist completion
- sideboard-delta inference
- matchup/archetype inference
- player mistake labels
- coaching, strategic advice, or player evaluation
- raw payload, raw hash, full path, private JSONL contents, or local machine
  marker display
- AI/OpenAI or model-provider calls

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

Partial rows:

- return stored rows when optional values are null
- preserve unknown/degraded/unavailable/conflict labels and counts
- do not infer missing result labels, turn counts, duration, play/draw,
  pre/postboard labels, matchup labels, deck-state, or causation

## Side Effects

Allowed side effects:

- read-only HTTP responses
- frontend render state
- test-created temporary SQLite databases under pytest temp directories
- implementation handoff documentation

Forbidden side effects:

- parser behavior changes
- parser state final reconciliation changes
- parser event class changes
- match/game identity or deduplication changes
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
- Existing manual JSONL import, browser upload, folder upload, and import-job
  endpoints must remain unchanged.
- Existing match/game history endpoints and frontend display must remain
  compatible.
- Existing opening-hand/mulligan endpoints and frontend display must remain
  compatible.
- Existing gameplay-action/opponent-observation endpoints and frontend display
  must remain compatible.
- Existing frontend upload and folder-upload flows must remain available.
- Existing response validation for setup status, manual import, match/game
  history, early-game history, and action review must remain compatible.
- Existing analytics schema, derived views, and ingest behavior must not be
  changed in this slice.

## Observed Current Behavior

Observed on `codex/analytics-foundation` during this contract pass:

- Issue #229 is open.
- Tracker #204 is open.
- Umbrella issue #207 is open.
- `git fetch --prune` completed and the branch is clean/even with
  `origin/codex/analytics-foundation`.
- The backend currently exposes `GET /api/analytics/matches`,
  `GET /api/analytics/games`, `GET /api/analytics/opening-hands`,
  `GET /api/analytics/mulligans`, `GET /api/analytics/gameplay-actions`, and
  `GET /api/analytics/opponent-card-observations`.
- The backend does not expose `GET /api/analytics/play-draw-splits` or
  `GET /api/analytics/game1-postboard-splits`.
- The frontend currently has typed response models and API functions for
  match/game history, early-game history, and action review.
- The frontend does not yet have typed play/draw or game 1/postboard split
  review responses.
- The SQLite schema already contains `v_play_draw_splits`,
  `v_sample_size_warnings`, and `v_game1_vs_postboard`.
- `v_play_draw_splits` groups by play/draw, separates known wins/losses from
  unknown/unavailable/degraded rows, and computes win rate only over known
  win/loss rows.
- `v_sample_size_warnings` currently emits `small_sample` for groups with fewer
  than 10 games and `ok` otherwise.
- `v_game1_vs_postboard` exposes game-result rows with match/game identity,
  pre/postboard label, local result, play/draw, turn count, duration, and
  status/provenance columns.
- Existing derived-view and replay/view tests cover the underlying SQL view
  behavior, but no current tests prove local app split review endpoints or
  frontend display.

## Required Guarantees

- Backend endpoints are fixed, read-only, and parameterized.
- Backend endpoints return only safe shaped JSON with symbolic database paths.
- Backend endpoints preserve unknown/degraded/unavailable/conflict counts.
- Play/draw win rate remains calculated over known win/loss rows only.
- Sample-size warnings remain display guardrails, not strategic guidance.
- Game 1/postboard rows preserve status/provenance labels where the view
  exposes them.
- Frontend display is read-only and validates object/schema versions.
- Frontend display avoids coaching, causation, hidden-card, archetype,
  best-line, player-mistake, Line Tracer, and AI/model-provider claims.
- Existing local app analytics surfaces continue to work.

## Unknowns

- The best final UI layout for split summaries is not yet proven. Codex C may
  use compact tables, small summary panels, or simple non-causal count bars as
  long as the display remains read-only and descriptive.
- It is unknown whether future filters by match, format, queue, event, or date
  will be needed. This contract authorizes only `limit` and `offset`.
- It is unknown whether future analytics should split play/draw by game 1,
  postboard, matchup labels, archetype labels, or notes. This contract defers
  those combinations.
- `v_play_draw_splits` does not expose per-group core provenance status objects
  beyond review counts. This is acceptable for the first UI slice; future
  provenance-rich aggregate views need a separate contract.

## Suspected Gaps

- Backend: no fixed read-only split review query helper exists yet.
- Backend: no route tests cover missing, empty, schema-current, schema-degraded,
  query-failure, partial row, or safe malformed-query behavior for split review
  endpoints.
- Backend: the route inventory needs additive endpoint expectations.
- Frontend: no typed play/draw split or game 1/postboard response models exist
  yet.
- Frontend: no API functions exist for the new endpoints.
- Frontend: no tests cover split review display, empty/degraded states,
  malformed responses, safe copy, or read-only boundaries.

## Validation Requirements

Codex C should run:

```powershell
py -m pytest -q tests\test_analytics_app_play_draw_postboard_split_views.py tests\test_analytics_app_gameplay_action_opponent_observation_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py tests\test_analytics_schema.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
```

If frontend dependencies are absent, Codex C may run
`npm --prefix frontend ci` before frontend validation.

Codex C and Codex E must also report:

- no generated SQLite files, WAL files, SHM files, journal files, raw logs, raw
  JSONL files, failed posts, workbook exports, runtime artifacts, frontend
  build output, or secrets were created or committed
- no arbitrary SQL, database browsing, destructive routes, or destructive UI
  controls were added
- no raw payloads, raw hashes, private paths, exception strings, stack traces,
  local usernames, credentials, coaching advice, hidden-card claims, best-line
  labels, archetype labels, causation claims, or player mistake labels appear
  in endpoint responses or UI output
- protected-surface scan results for changed paths
- secret/private-marker scan results for changed paths

Contract-writer validation is docs-only:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/analytics_app_play_draw_postboard_split_views.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/analytics_app_play_draw_postboard_split_views.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
py tools\check_agent_docs.py
```

Because `git diff --check` does not inspect untracked files, Codex B should also
run an explicit new-file whitespace/final-newline check before handoff.

## Acceptance Criteria

- `docs/contracts/analytics_app_play_draw_postboard_split_views.md` exists.
- `GET /api/analytics/play-draw-splits` is specified with the approved response
  object and schema version.
- `GET /api/analytics/game1-postboard-splits` is specified with the approved
  response object and schema version.
- The contract requires `v_play_draw_splits`, `v_sample_size_warnings`, and
  `v_game1_vs_postboard` to remain read-only source views.
- The contract defines allowed query parameters and rejects arbitrary SQL,
  generic database browsing, and destructive controls.
- The contract defines play/draw split row fields, game 1/postboard row fields,
  summaries, status behavior, and sample-size warning policy.
- The contract preserves parser truth ownership and protected surfaces.
- The contract requires focused backend/frontend tests and compatibility tests.
- No implementation, migration, parser, analytics ingest, workbook, webhook,
  Apps Script, runtime, generated-data, OpenAI/AI, Line Tracer, coaching, or
  production behavior changes are made in the contract-writing pass.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #229.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_play_draw_postboard_split_views.md

Prerequisite context:
Issues #225, #226, and #228 are complete. Reuse the fixed read-only local app history safety pattern from src/mythic_edge_parser/local_app/analytics_history.py and the existing analytics app contracts where practical.

Goal:
Compare the current local app backend, frontend, analytics schema/views, and tests against the contract. Implement only the read-only play/draw and game 1/postboard split review view slice and focused tests. Produce docs/implementation_handoffs/analytics_app_play_draw_postboard_split_views_comparison.md.

Before editing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what the split review views are supposed to do, what the app currently does, what gap remains, and the exact minimal implementation plan.

Do:
- Add fixed read-only backend endpoints GET /api/analytics/play-draw-splits and GET /api/analytics/game1-postboard-splits.
- Query only v_play_draw_splits, v_sample_size_warnings, and v_game1_vs_postboard unless the contract's narrow documented fallback is needed.
- Use read-only SQLite access and fixed parameterized SQL.
- Return the approved typed response shapes with safe status/error handling.
- Preserve unknown, unavailable, degraded, conflict, sample-size, and provenance/status labels where available.
- Add read-only frontend display for play/draw and game 1/postboard split review near existing analytics views.
- Keep copy descriptive and non-causal.
- Add focused backend and frontend tests for success, empty, missing, degraded, error, partial rows, malformed query params, response validation, safe display, and read-only boundaries.
- Preserve existing setup-status, manual import, browser upload, folder upload, match/game history, opening-hand, mulligan, gameplay-action, and opponent-observation behavior.
- Produce the implementation handoff.

Do not:
- add arbitrary SQL, generic database browsing, or destructive database/UI controls
- create or apply migrations
- change analytics schema, derived SQL view definitions, or ingest behavior
- query raw Player.log, raw JSONL, fact_provenance, opening-hand/mulligan tables, gameplay-action tables, opponent-observation tables, sideboarding/deck-state tables, rank snapshots, annotation tables, Match Journal tables, or derived dashboard views outside the contracted set
- add Line Tracer, opening-line recommendations, first-three-turn best-line summaries, sample-size significance claims, coaching, hidden-card inference, complete decklist inference, sideboard-delta inference, archetype inference, action quality ratings, causation claims, player mistake labels, strategic advice, or player evaluation
- expose raw payloads, raw hashes, full paths, exception strings, stack traces, secrets, credentials, or local machine markers
- create or commit generated SQLite files, frontend build output, raw logs, JSONL artifacts, runtime files, failed posts, workbook exports, or local-only artifacts
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, output transport, production behavior, AI/OpenAI, Line Tracer, or coaching behavior
- target main
- close tracker #204 or umbrella #207
- stage, commit, push, open a PR, merge, or deploy unless explicitly asked

Validation:
py -m pytest -q tests\test_analytics_app_play_draw_postboard_split_views.py tests\test_analytics_app_gameplay_action_opponent_observation_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py tests\test_analytics_schema.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py

Final handoff must include role performed, source issue/tracker, contract used, files changed, exact backend/frontend/test sections changed, validation run, protected-surface status, generated/private artifact status, remaining risk, next recommended role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/229"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_prerequisites:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/225"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/226"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/228"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #229 and current local app/analytics split view implementation context"
  target_artifact: "docs/contracts/analytics_app_play_draw_postboard_split_views.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "Codex B docs-only validation required: git status --short --branch"
    - "Codex B docs-only validation required: git diff --check"
    - "Codex B docs-only validation required: explicit new-file whitespace/final-newline check"
    - "Codex B docs-only validation required: protected-surface and secret/private-marker scans on the contract"
    - "Codex C should run backend, frontend, schema/view, ruff, and generated-artifact checks"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not expose arbitrary SQL or destructive database/UI controls."
    - "Do not turn split rows into Line Tracer, coaching, causation, hidden-card, archetype, player-mistake, or best-line truth."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not change analytics schema, migrations, derived SQL views, or ingest behavior in this slice."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```
