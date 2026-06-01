# Analytics App Gameplay Action And Opponent Observation Views Contract

## Module

Local developer app curated gameplay-action and opponent-card-observation
review views.

This contract covers a read-only local app surface over gameplay-action and
opponent-card-observation facts already stored in the local SQLite analytics
database.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/228
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Completed prerequisite: https://github.com/Tahjali11/Mythic-Edge/issues/225
- Completed prerequisite: https://github.com/Tahjali11/Mythic-Edge/issues/226

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

Reason: gameplay-action and opponent-observation rows are close to future Line
Tracer, coaching, hidden-card, archetype, and best-line surfaces. This slice
must stay read-only and observational. It may show stored parser-normalized
facts and degradation labels, but it must not infer what happened beyond the
stored rows or tell the player what should have happened.

## Owning Layer

Primary owning layer: Local App / UI.

Supporting storage/query layer: Analytics.

Truth boundaries:

- Parser/state owns parser-managed gameplay-action facts, opponent-card
  observation facts, event interpretation, match/game identity, deduplication,
  and final reconciliation.
- SQLite analytics tables own local durable storage of parser-normalized facts
  and provenance/status labels.
- Derived SQL views own deterministic read-only projections over stored facts.
- The local app backend owns fixed read-only API projections over the local
  analytics database.
- The local app frontend owns display and local interaction.
- Neither SQLite nor the UI may reinterpret Arena events, infer hidden cards,
  infer decklists, classify archetypes, label player mistakes, provide best-line
  recommendations, or become coaching truth.

Plain English: this view may show "these are the stored in-game action and
visible opponent-card observation rows." It must not answer "what should I have
done?" or "what is in the opponent's hand/deck?"

## Internal Project Area

Primary area: Local App / UI.

Bridge-code status: `bridge_code`.

Bridge details:

- source internal project area: Analytics
- consuming internal project area: Local App / UI
- allowed data flow: SQLite analytics gameplay-action and
  opponent-observation fact tables and approved read-only views to fixed local
  backend responses to frontend display
- forbidden reverse-flow: frontend/backend review views must not write back to
  SQLite, change analytics ingest, change parser facts, update workbook/runtime
  state, or feed coaching conclusions into parser/analytics truth
- protected surfaces explicitly not touched: parser behavior, analytics schema
  and migrations, analytics ingest, workbook/webhook/App Script/Sheets,
  production behavior, generated/private/local artifacts, secrets, raw logs,
  Line Tracer, and AI/coaching surfaces

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md`

Future implementation files authorized for Codex C, subject to comparison and
validation:

- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/backend.py`
- optional new helper module under `src/mythic_edge_parser/local_app/` only if
  the existing history helper becomes too large
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- focused backend tests, expected as
  `tests/test_analytics_app_gameplay_action_opponent_observation_views.py`
- focused route inventory additions in `tests/test_analytics_local_app_backend.py`
- `docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md`

Reference-only source surfaces:

- `docs/contracts/analytics_app_match_game_history_views.md`
- `docs/contracts/analytics_app_opening_hand_mulligan_views.md`
- `docs/contracts/analytics_gameplay_action_ingest.md`
- `docs/contracts/analytics_opponent_card_observation_ingest.md`
- `docs/contracts/analytics_derived_sql_views.md`
- `docs/contracts/player_log_evidence_ledger_tier5_gameplay_action.md`
- `docs/contracts/player_log_evidence_ledger_tier5_opponent_card_observation.md`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- existing local app, analytics ingest, derived-view, and replay/view tests

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

The local app gameplay/observation review response schema version is:

```text
analytics_app_gameplay_action_opponent_observation_views.v1
```

This version is intentionally separate from match/game history and early-game
history because these row shapes include action/observation-specific child card
arrays and visibility/degradation labels.

### Backend Endpoints

Codex C may add exactly these review endpoints:

```text
GET /api/analytics/gameplay-actions
GET /api/analytics/opponent-card-observations
```

Allowed query parameters:

- `limit`: optional integer, default `50`, minimum `1`, maximum `100`
- `offset`: optional integer, default `0`, minimum `0`

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
- opening-line, first-three-turn, Line Tracer, AI/OpenAI, coaching, Match
  Journal, Google Sheets, or workbook endpoints

### Deferred Endpoint

`GET /api/analytics/opening-lines` is not authorized in this slice.

`v_opening_lines` may be named in documentation as an existing SQLite view, but
Codex C must not expose it through the local app for issue #228. A future issue
may decide whether first-three-turn review can be shown safely without becoming
Line Tracer or best-line analysis.

### Response Object Names

`GET /api/analytics/gameplay-actions` must return:

```text
object: mythic_edge_local_app_gameplay_action_review
schema_version: analytics_app_gameplay_action_opponent_observation_views.v1
```

`GET /api/analytics/opponent-card-observations` must return:

```text
object: mythic_edge_local_app_opponent_card_observation_review
schema_version: analytics_app_gameplay_action_opponent_observation_views.v1
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

Expected `summary` shape:

```json
{
  "row_count": 0,
  "card_row_count": 0,
  "degraded_row_count": 0,
  "unavailable_row_count": 0,
  "conflict_row_count": 0,
  "review_required_row_count": 0
}
```

`row_count` counts grouped action or observation rows. `card_row_count` counts
child card rows included inside those grouped rows. These counts are display
and review signals only, not parser truth, coaching conclusions, or evidence of
hidden-card certainty.

## Backend Query Contract

### Database Access

Review endpoints must:

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
  object helpers from `analytics_history.py` where practical
- query rows only when the database exists and `schema_status` is
  `schema_current`
- use `sqlite3.Row` or structured row mapping
- paginate grouped parent rows, not child card rows
- perform child-card fetching with fixed parameterized queries keyed by the
  selected parent ids

### Allowed Tables And Views

The gameplay-action endpoint may query only:

- `gameplay_actions`
- `gameplay_action_cards`
- `games`
- `matches`
- `game_results`
- `match_results`
- `match_context`
- `v_gameplay_action_review`, when it does not hide parent action rows that
  have zero child cards

The opponent-card-observation endpoint may query only:

- `opponent_card_observations`
- `opponent_card_observation_cards`
- `gameplay_actions`, only for deterministic linked-action context
- `games`
- `matches`
- `game_results`
- `match_results`
- `match_context`
- `v_opponent_card_observation_review`, only when Codex C groups duplicated
  parent rows deterministically and preserves zero-child observation rows

The first slice must not query:

- raw local files
- raw JSONL artifacts
- raw Player.log contents
- `fact_provenance`
- rank snapshots
- sideboarding or deck-state tables
- opening-hand or mulligan tables
- annotation tables such as matchup labels, archetype labels, or game notes
- derived dashboard views such as `v_opening_lines`, `v_play_draw_splits`,
  `v_sample_size_warnings`, or `v_matchup_label_performance`

`v_opening_lines`, Line Tracer-style views, sample-size summaries, and
dashboard summaries are explicitly deferred. Row-level game/result/context may
be shown only as context and must not become causal claims or recommendations.

## Gameplay Action Rows

`GET /api/analytics/gameplay-actions` returns one grouped row per stored
`gameplay_actions` row.

Each gameplay action row must include:

- `gameplay_action_id`
- `match_id`
- `game_id`
- `game_number`
- `timestamp`
- `game_state_id`
- `turn_number`
- `action_type`
- `actor_relation`
- `from_zone_type`
- `to_zone_type`
- `source_status`
- `annotation_context_label`
- `raw_action_type_labels`
- `annotation_type_labels`
- `visible_in_log`
- `card_count`
- `grp_ids`
- `local_result`
- `play_draw`
- `pre_postboard_label`
- `match_result`
- `match_win`
- `queue_name`
- `format_name`
- `event_id`
- `cards`
- `gameplay_action_status`
- `game_status`
- `game_result_status`
- `match_result_status`
- `context_status`

`cards` is an array ordered by `card_ordinal`. Each gameplay action card row
must include:

- `gameplay_action_card_id`
- `card_ordinal`
- `instance_id`
- `grp_id`
- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `identity_hint_source`
- `card_name`
- `display_name`
- `name_resolution_status`
- `enrichment_status`
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

If a `gameplay_actions` row exists with zero child card rows, the endpoint must
return the action group with `cards: []`.

Required deterministic order:

```text
COALESCE(gameplay_actions.timestamp, games.game_completed_at, game_results.game_completed_at, games.game_started_at, games.updated_at) DESC,
gameplay_actions.match_id DESC,
gameplay_actions.game_number ASC,
gameplay_actions.turn_number ASC,
gameplay_actions.gameplay_action_id ASC
```

Rows with `turn_number` null must still be returned. Their relative order after
the timestamp/game ordering may use `gameplay_action_id ASC` and must be
stable.

## Opponent Card Observation Rows

`GET /api/analytics/opponent-card-observations` returns one grouped row per
stored `opponent_card_observations` row.

Each opponent-card observation row must include:

- `opponent_card_observation_id`
- `gameplay_action_id`
- `match_id`
- `game_id`
- `game_number`
- `timestamp`
- `game_state_id`
- `turn_number`
- `actor_relation`
- `actor_seat_id`
- `local_seat_id`
- `instance_id`
- `grp_id`
- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `parent_id`
- `identity_hint_source`
- `card_name`
- `display_name`
- `resolution_status`
- `name_resolution_source`
- `action_type`
- `cast_mode`
- `source_evidence`
- `evidence_status`
- `visibility`
- `from_zone_type`
- `to_zone_type`
- `degradation_flags`
- `review_required`
- `linked_gameplay_action`
- `local_result`
- `play_draw`
- `pre_postboard_label`
- `match_result`
- `match_win`
- `queue_name`
- `format_name`
- `event_id`
- `cards`
- `opponent_card_observation_status`
- `linked_gameplay_action_status`
- `game_status`
- `game_result_status`
- `match_result_status`
- `context_status`

`degradation_flags` must be returned as a safe string-array value. If the stored
value is malformed JSON, the endpoint must not echo the raw malformed text. It
should return an empty array plus a degraded row status or a stable warning code
such as `opponent_observation_degradation_flags_malformed`.

`linked_gameplay_action` is null when no linked action exists. When present, it
may include only compact context from the linked row:

- `gameplay_action_id`
- `turn_number`
- `action_type`
- `actor_relation`
- `from_zone_type`
- `to_zone_type`
- `visible_in_log`

It must not create a synthetic action when the foreign key is null.

`cards` is an array ordered by `card_ordinal`. Each opponent observation child
card row must include:

- `opponent_card_observation_card_id`
- `card_ordinal`
- `grp_id`
- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `identity_hint_source`
- `card_name`
- `resolution_status`
- `visibility`
- `card_status`

If an `opponent_card_observations` row exists with zero child card rows, the
endpoint must return the observation group with `cards: []` and preserve the
parent `degradation_flags`, `review_required`, `evidence_status`, `visibility`,
`confidence`, and `drift_status` labels.

Required deterministic order:

```text
COALESCE(opponent_card_observations.timestamp, games.game_completed_at, game_results.game_completed_at, games.game_started_at, games.updated_at) DESC,
opponent_card_observations.match_id DESC,
opponent_card_observations.game_number ASC,
opponent_card_observations.turn_number ASC,
opponent_card_observations.opponent_card_observation_id ASC
```

Rows with `turn_number` null must still be returned. Their relative order after
the timestamp/game ordering may use `opponent_card_observation_id ASC` and must
be stable.

## Row Status Summaries

For response `summary` counts, a grouped row is degraded when any included
parent, linked action, context, result, game, or child-card status object has:

- `drift_status` in `degraded`, `conflict`, `missing_expected_evidence`, or
  `redacted`
- `value_source` equal to `conflict`
- `confidence` equal to `low` or `unknown`

A grouped row is unavailable when any included status object has
`availability_status` not equal to `available`.

A grouped row is conflict when any included status object has:

- `drift_status` equal to `conflict`
- `value_source` equal to `conflict`

For opponent-card observations, a grouped row is review-required when
`review_required` is true or when its parsed `degradation_flags` array is
non-empty.

These counts are review signals only. They must not change stored facts, imply
strategic quality, or promote degraded rows into hidden-card certainty.

## Frontend Display Contract

The frontend may add Gameplay Actions and Opponent Observations to the existing
Analytics History area or a clearly adjacent read-only analytics review section.

Required frontend behavior:

- fetch `GET /api/analytics/gameplay-actions`
- fetch `GET /api/analytics/opponent-card-observations`
- validate response `object` and `schema_version`
- show gameplay actions grouped by match/game/turn where practical
- show gameplay action child card rows when present
- show opponent observations grouped by match/game/turn where practical
- show opponent observation child card rows when present
- show linked gameplay-action context only when a stored deterministic link
  exists
- show loading, empty, missing, degraded, unavailable, and error states
- reuse existing analytics history visual/status patterns where practical
- preserve existing setup-status, manual-import, browser-upload, folder-upload,
  match-history, game-history, opening-hand, and mulligan behavior
- keep all gameplay/observation review actions read-only
- show source/confidence/finality/drift/availability/status labels as compact
  review labels where useful
- show `visibility`, `evidence_status`, `degradation_flags`, and
  `review_required` as audit labels for observations
- show safe counts from `summary`
- avoid display text that presents downstream SQLite/UI data as parser truth,
  coaching truth, hidden-card truth, archetype truth, or strategic advice

Allowed read-only frontend action:

- a refresh control that re-fetches the analytics review endpoints

Codex C may either:

- extend the existing Analytics History refresh to fetch all history/review
  endpoints together, or
- add a separate gameplay/observation refresh inside the same read-only
  analytics area

The implementation must not cause import/upload controls to become destructive
or intermingled with analytics review actions.

Forbidden frontend behavior:

- arbitrary SQL entry
- table picker or column picker
- edit/delete/reset/vacuum/export controls
- database initialization controls
- import controls inside the gameplay/observation review section
- live watcher controls
- Match Journal editing
- matchup/archetype labeling or game notes editing
- Line Tracer behavior
- opening-line recommendations
- first-three-turn best-line summaries
- action quality ratings
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

Partial data:

- return stored parent rows even when optional context/result/child rows are
  absent
- represent missing optional joined rows with `null` or empty child arrays
- preserve source/confidence/finality/drift/availability labels
- do not fill missing card identities, action links, game results, match
  results, or context by inference

Malformed stored `degradation_flags`:

- do not echo raw malformed text
- either return a stable warning code with `degradation_flags: []`, or mark the
  response `degraded` if Codex C determines the row shape cannot be trusted
- preserve the parent row when the rest of the observation is safe to display

## Side Effects

Allowed side effects:

- read-only HTTP responses
- frontend render state
- test-created temporary SQLite databases under pytest temp directories
- implementation handoff documentation

Forbidden side effects:

- parser behavior changes
- gameplay-action extraction/classification changes
- opponent-card-observation extraction/classification changes
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
- Existing frontend upload and folder-upload flows must remain available.
- Existing response validation for setup status, manual import, match/game
  history, and early-game history must remain compatible.
- Existing analytics schema, derived views, and ingest behavior must not be
  changed in this slice.

## Observed Current Behavior

Observed on `codex/analytics-foundation` during this contract pass:

- Issue #228 is open.
- Tracker #204 is open.
- Umbrella issue #207 is open.
- Issues #225 and #226 are complete; issue #226 is closed.
- The backend currently exposes `GET /api/analytics/matches`,
  `GET /api/analytics/games`, `GET /api/analytics/opening-hands`, and
  `GET /api/analytics/mulligans`.
- The backend does not expose `GET /api/analytics/gameplay-actions` or
  `GET /api/analytics/opponent-card-observations`.
- The frontend currently has typed response models and API functions for
  match/game history and early-game history.
- The frontend does not yet have typed gameplay-action or opponent-observation
  review responses.
- The SQLite schema already contains `gameplay_actions`,
  `gameplay_action_cards`, `opponent_card_observations`, and
  `opponent_card_observation_cards`.
- The SQLite schema already contains `v_gameplay_action_review` and
  `v_opponent_card_observation_review`.
- `v_gameplay_action_review` is a parent action review view with child card
  count and grouped `grp_ids`.
- `v_opponent_card_observation_review` joins observation rows to child card
  rows, so it can duplicate observation parent rows when multiple child cards
  exist and must be grouped carefully by the local app endpoint.
- Existing analytics ingest contracts define gameplay-action and
  opponent-card-observation storage as parser-normalized facts downstream of
  parser ownership.
- Existing derived-view and replay/view tests cover SQL view behavior, but no
  current tests prove local app gameplay-action or opponent-observation review
  endpoints or frontend display.

## Required Guarantees

- Backend endpoints are fixed, read-only, and parameterized.
- Backend endpoints return only safe shaped JSON with symbolic database paths.
- Backend endpoints paginate grouped parent rows, not child card rows.
- Gameplay-action rows preserve parser-normalized action fields and child card
  identity hints without reinterpreting them.
- Opponent-observation rows preserve visibility, evidence status, confidence,
  finality, drift, degradation, and review-required labels.
- Linked gameplay-action context appears only when a stored link exists.
- Missing child rows are represented as empty arrays, not inferred identities.
- Degraded/conflict/unavailable/review-required labels remain visible.
- Frontend display is read-only and validates object/schema versions.
- Frontend display avoids coaching, hidden-card, archetype, best-line,
  player-mistake, Line Tracer, and AI/model-provider claims.
- Existing local app and analytics history surfaces continue to work.

## Unknowns

- The best final UI layout for action-heavy rows is not yet proven. Codex C may
  use compact tables, grouped rows, expandable row details, or small review
  cards as long as the display remains read-only and scannable.
- It is unknown whether future filters by match, game, turn, actor, action
  type, visibility, or review status will be needed. This contract authorizes
  only `limit` and `offset`.
- It is unknown whether `v_opponent_card_observation_review` should remain the
  preferred backend source once multi-card observation rows become common.
  Codex C may query base tables directly when that better preserves grouped
  parent rows.
- It is unknown whether future first-three-turn or opening-line review belongs
  beside these rows. This contract defers that question.

## Suspected Gaps

- Backend: no fixed read-only gameplay-action query helper exists yet.
- Backend: no fixed read-only opponent-observation query helper exists yet.
- Backend: no route tests cover missing, empty, schema-current, schema-degraded,
  query-failure, partial child-row, malformed degradation flags, or safe
  malformed-query behavior for these endpoints.
- Backend: the route inventory needs additive endpoint expectations.
- Frontend: no typed gameplay-action or opponent-observation response models
  exist yet.
- Frontend: no API functions exist for the new endpoints.
- Frontend: no tests cover grouped gameplay/observation review display,
  empty/degraded states, malformed responses, safe display, or read-only
  boundaries.

## Validation Requirements

Codex C should run:

```powershell
py -m pytest -q tests\test_analytics_app_gameplay_action_opponent_observation_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
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
  labels, archetype labels, or player mistake labels appear in endpoint
  responses or UI output
- protected-surface scan results for changed paths
- secret/private-marker scan results for changed paths

Contract-writer validation is docs-only:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Because `git diff --check` does not inspect untracked files, Codex B should also
run an explicit new-file whitespace/final-newline check before handoff.

## Acceptance Criteria

- `docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md`
  exists.
- `GET /api/analytics/gameplay-actions` is specified with the approved response
  object and schema version.
- `GET /api/analytics/opponent-card-observations` is specified with the
  approved response object and schema version.
- The contract keeps `GET /api/analytics/opening-lines` deferred.
- The contract defines allowed query parameters and rejects arbitrary SQL,
  generic database browsing, and destructive controls.
- The contract defines grouped gameplay-action row shape and child card row
  shape.
- The contract defines grouped opponent-observation row shape, linked action
  context, child card rows, degradation flags, and review-required behavior.
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

Act as Codex C: Module Implementer / comparison thread for issue #228.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md

Prerequisite context:
Issues #225 and #226 are complete. Reuse the fixed read-only local app history safety pattern from src/mythic_edge_parser/local_app/analytics_history.py and the match/game plus early-game contracts where practical.

Goal:
Compare the current local app backend, frontend, analytics schema/views, and tests against the contract. Implement only the read-only gameplay-action and opponent-card-observation review view slice and focused tests. Produce docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md.

Before editing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what the gameplay/observation review views are supposed to do, what the app currently does, what gap remains, and the exact minimal implementation plan.

Do:
- Add fixed read-only backend endpoints GET /api/analytics/gameplay-actions and GET /api/analytics/opponent-card-observations.
- Query only the allowed gameplay-action, opponent-observation, match/game result, match context, linked action, and approved view surfaces from the contract.
- Use read-only SQLite access and fixed parameterized SQL.
- Paginate grouped parent rows, not child card rows.
- Return grouped gameplay-action rows with child card arrays.
- Return grouped opponent-observation rows with child card arrays and linked gameplay-action context when a stored link exists.
- Preserve source/confidence/finality/drift/availability, visibility, evidence_status, degradation_flags, and review_required labels.
- Return the approved typed response shapes with safe status/error handling.
- Add read-only frontend display for gameplay actions and opponent observations inside or adjacent to Analytics History.
- Add focused backend and frontend tests for success, empty, missing, degraded, error, partial child rows, malformed degradation flags, malformed query params, response validation, safe display, and read-only boundaries.
- Preserve existing setup-status, manual import, browser upload, folder upload, match/game history, opening-hand, and mulligan behavior.
- Produce the implementation handoff.

Do not:
- add arbitrary SQL, generic database browsing, or destructive database/UI controls
- expose GET /api/analytics/opening-lines in this slice
- create or apply migrations
- change analytics schema or ingest behavior
- query raw Player.log, raw JSONL, fact_provenance, rank snapshots, sideboarding/deck-state tables, opening-hand/mulligan tables, annotation tables, or derived dashboard views in this slice
- add Line Tracer, opening-line recommendations, first-three-turn best-line summaries, sample-size/dashboard summaries, coaching, hidden-card inference, complete decklist inference, sideboard-delta inference, archetype inference, action quality ratings, player mistake labels, strategic advice, or player evaluation
- expose raw payloads, raw hashes, full paths, exception strings, stack traces, secrets, credentials, or local machine markers
- create or commit generated SQLite files, frontend build output, raw logs, JSONL artifacts, runtime files, failed posts, workbook exports, or local-only artifacts
- change parser behavior, gameplay-action extraction/classification, opponent-observation extraction/classification, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, output transport, production behavior, AI/OpenAI, Line Tracer, or coaching behavior
- target main
- close tracker #204 or umbrella #207
- stage, commit, push, open a PR, merge, or deploy unless explicitly asked

Validation:
py -m pytest -q tests\test_analytics_app_gameplay_action_opponent_observation_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check

Final handoff must include role performed, source issue/tracker, contract used, files changed, exact backend/frontend/test sections changed, validation run, protected-surface status, generated/private artifact status, remaining risk, next recommended role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/228"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #228 and current local app/analytics history implementation"
  target_artifact: "docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md"
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
    - "Do not expose GET /api/analytics/opening-lines in this slice."
    - "Do not turn gameplay-action or opponent-observation rows into Line Tracer, coaching, hidden-card, archetype, player-mistake, or best-line truth."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not change analytics schema, migrations, or ingest behavior in this slice."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```
