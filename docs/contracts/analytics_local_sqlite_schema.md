# Analytics Local SQLite Schema Contract

## Module

Local Analytics Foundation SQLite schema v1.

This contract defines the first broad local SQLite schema for Mythic Edge
analytics facts. It is a schema contract only; it does not implement migrations,
ingest, replay, a migration runner, or runtime behavior.

## Source Issue

Problem representation:

- `docs/problem_representations/analytics_schema_contract.md`

Parent problem representation:

- `docs/problem_representations/local_analytics_foundation.md`

Suggested issue:

- `[analytics] Define local SQLite schema contract`

Suggested tracker:

- `[analytics] Local analytics foundation`

## Related ADRs

- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`

## Owning Layer

Primary owning layer: local analytics foundation.

Truth boundaries:

- Parser/state owns parser-managed match, game, card, and gameplay facts.
- The Player.log evidence ledger owns provenance, confidence, finality, drift,
  and degradation vocabulary.
- The SQLite analytics schema owns durable local storage shape, table keys,
  migration discipline, and queryable fact structure.
- SQL views own deterministic derived query surfaces, not parser truth.
- Human annotations are downstream context, not parser truth.
- Google Sheets, Google Docs, dashboards, Line Tracer, AI coaching, OpenAI API
  runtime integration, and model-provider output are out of scope and must not
  become truth owners through this schema.

Plain English: SQLite can store parser facts and make them easier to query, but
it does not get to decide what happened in a match.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_local_sqlite_schema.md`

Future implementation files authorized by this contract, subject to Codex C
comparison and validation:

- `.gitignore`, only to ignore local/generated analytics database artifacts
- `src/mythic_edge_parser/app/analytics_migrations/*.sql`
- focused analytics schema tests, expected under `tests/test_analytics_schema*.py`
- optional test-only helpers needed to apply SQL migrations to temporary SQLite
  databases

Future implementation files that may be proposed but are not required by this
schema contract:

- `src/mythic_edge_parser/app/analytics_schema.py`
- `src/mythic_edge_parser/app/analytics_store.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`

If Codex C finds that a production migration runner, ingest module, environment
variable contract, or runtime wiring is necessary, it must stop and route to a
follow-up contract unless the user explicitly expands scope.

## Public Interface

### Generated Database Path

Default local database path:

```text
data/analytics/mythic_edge.sqlite3
```

The database file and all adjacent generated SQLite artifacts are local-only.
They must be ignored by Git.

Required ignore coverage:

```text
data/analytics/
```

The v1 schema contract does not require a new environment variable. A future
contract may add a `MYTHICEDGE_ANALYTICS_DB_PATH`-style override, but this
contract does not authorize environment-variable contract changes.

### Migration Path

Versioned plain SQL migrations must live under:

```text
src/mythic_edge_parser/app/analytics_migrations/
```

Required first migration name:

```text
0001_initial_analytics_schema.sql
```

Migration files are source-controlled schema definitions. Generated database
files are not.

### Schema Version

Logical schema version:

```text
analytics_local_sqlite_schema.v1
```

The exact version string must be recorded in either `schema_migrations`,
`parser_schema_versions`, or both.

## Observed Repo Behavior

Current parser/model behavior:

- `src/mythic_edge_parser/app/models.py` defines `MatchSummary` and
  `GameSummary` and emits parser-normalized match and game row dictionaries.
- Match/game rows expose match id, game number, results, play/draw, mulligans,
  opening hand fields, turn count, event/queue context, rank, sideboarding
  entered, and submit-deck seen fields.
- `src/mythic_edge_parser/app/state.py` owns in-memory parser state,
  match/game identity, live/final row construction, mulligan tracking, opening
  hand capture, rank snapshots, game results, and changed-field posting state.
- `src/mythic_edge_parser/app/gameplay_actions.py` builds local gameplay
  action artifacts with match/game identity, turn number, action type, card id
  hints, actor relation, zones, annotation context, and display enrichment.
- `src/mythic_edge_parser/app/opponent_card_observations.py` builds visible
  opponent-card observation payloads from gameplay action entries and carries
  value source, confidence, evidence status, degradation flags, and review
  status.
- `src/mythic_edge_parser/app/runtime_surfaces.py` writes local JSON/Markdown
  status artifacts such as match history, active match timeline, active deck
  profile, collection profile, and active match snapshot.
- `src/mythic_edge_parser/app/analytics_sidecar.py` currently drives optional
  background runtime artifact and Google Sheets export work. It does not own a
  SQLite store.
- `src/mythic_edge_parser/app/saved_event_replay.py` replays supported saved
  event kinds from selected JSONL files and dedupes raw hashes within a replay
  run. It does not ingest into SQLite.
- `src/mythic_edge_parser/app/evidence_ledger.py` defines source, confidence,
  finality, drift, and Tier 1-7 provenance vocabularies, including Tier 7
  derived analytics outputs.

Current test behavior:

- `tests/test_app_models.py` covers current match/game row shapes, live vs
  final row behavior, mulligan handling, opening hand serialization, and
  workbook-facing field coverage.
- `tests/test_state.py` covers runtime state, hand snapshots, and state
  observation APIs.
- `tests/test_analytics_sidecar.py` covers sidecar export flags and optional
  work selection.
- `tests/test_runner.py` covers runner side-effect ordering and analytics
  sidecar submission calls.
- `tests/test_gameplay_actions.py` covers gameplay action artifact generation
  and action dedupe behavior.
- `tests/test_opponent_card_observations.py` covers visible opponent-card
  observation payloads, degradation, confidence, and no hidden-card guessing.
- `tests/test_saved_event_replay.py` covers saved-event replay file selection,
  event reconstruction, raw-hash dedupe, unknown-kind skip behavior, and
  malformed record behavior.
- `tests/test_event_schema_snapshots.py` covers parser event and workbook row
  snapshot surfaces, not SQLite schema.
- `tests/test_evidence_ledger.py`, `tests/test_evidence_schema_snapshot.py`,
  and `tests/test_runtime_field_evidence.py` cover ledger vocabulary,
  provenance boundaries, runtime field-evidence report shape, and that existing
  model rows do not gain field-evidence shape.

Observed gaps:

- No SQLite schema contract existed before this file.
- No analytics migration files exist.
- No local analytics database path exists in code.
- No `data/analytics/` ignore rule exists in `.gitignore`.
- No `schema_migrations` table or analytics schema test exists.
- No implementation currently proves replay idempotency into SQLite.

## Inputs

In-scope input classes for future implementation:

- parser-normalized match summaries and `MatchLogRow` dictionaries
- parser-normalized game summaries and `GameLogRow` dictionaries
- match/game identity from parser state and models
- player/team/seat mappings from parser-normalized output
- match/game results, play/draw, mulligans, opening hand snapshots, turn
  counts, pre/postboard labels, queue/context, rank, and event context
- sideboarding entered, submit-deck seen, submitted deck cards, and submitted
  deck snapshots only when parser-normalized
- gameplay action payloads produced by `gameplay_actions.py`
- visible opponent-card observation payloads produced by
  `opponent_card_observations.py`
- evidence/provenance labels from the evidence ledger or runtime field-evidence
  report surfaces
- sanitized committed replay/golden fixtures when implementation tests need
  durable replay input
- human matchup/archetype labels and game notes entered downstream

Out-of-scope inputs:

- raw Player.log payload storage
- raw local log paths
- raw local Player.log excerpts
- raw saved-event line bodies as database facts
- webhook URLs, credentials, tokens, API keys, or secrets
- generated card/tier data blobs, unless a later contract approves a sanitized
  reference table
- runtime status files as authoritative truth
- failed posts
- workbook exports
- Google Sheets or Google Docs live data
- AI-generated recommendations or coaching text as fact input

## Outputs

The v1 schema must define source-controlled plain SQL migrations that create:

- metadata and migration tables
- parser-normalized identity and context fact tables
- decision snapshot fact tables
- gameplay/action/observation fact tables
- annotation tables for the narrow v1 human annotation scope
- detailed `fact_provenance`
- deterministic SQL views for first analytics surfaces

The v1 implementation must not create or commit:

- `data/analytics/mythic_edge.sqlite3`
- SQLite journal/WAL/SHM files
- raw Player.log payloads
- local runtime artifacts
- workbook exports
- generated card data

## Shared Schema Conventions

### Table And Column Style

- Table and column names must be lowercase `snake_case`.
- Primary analytic identities must be deterministic text IDs where possible.
- Timestamps must be ISO-8601 text when present.
- Boolean values must be stored as integer `0` or `1`, or as constrained text
  labels when a tri-state is required.
- Unknown or unavailable values must not be silently collapsed into empty
  strings when a label is needed for analytics.
- JSON is allowed only for non-canonical convenience metadata. Canonical card
  lists and fact relationships must be normalized into child rows.

### Core Provenance Columns

Every parser fact table, annotation table, and derived analytics materialization
authorized by this contract must include these columns unless explicitly marked
`not_applicable` in the migration comments and tests:

- `value_source`
- `confidence`
- `finality`
- `drift_status`
- `parser_schema_version`
- `ingest_run_id`
- `source_parser_surface`
- `source_fact_key`
- `availability_status`
- `created_at`
- `updated_at`

Required value-source labels:

- `observed`
- `derived`
- `inferred`
- `unknown`
- `conflict`
- `legacy_enriched`
- `human_annotation`

`human_annotation` is allowed only for annotation tables and must not be used for
parser-owned facts.

Required confidence labels:

- `high`
- `medium`
- `low`
- `unknown`
- `human`

`human` is allowed only for user-entered annotations. It means "human-supplied",
not "objectively true."

Required finality labels:

- `live`
- `provisional`
- `final`
- `reconciled`
- `annotation_current`
- `annotation_historical`

Required drift-status labels:

- `none`
- `not_checked`
- `degraded`
- `conflict`
- `missing_expected_evidence`
- `redacted`

Detailed drift flags belong in `fact_provenance`, not in a single duplicated
core column.

Required availability-status labels:

- `available`
- `expected_unavailable`
- `not_applicable`
- `not_observed`
- `withheld_private`
- `not_yet_supported`

These labels distinguish "this did not happen" from "the parser expected this
fact but the normalized evidence is unavailable." For example, a final parser
mulligan count of `0` is different from a missing mulligan source that cannot be
trusted.

### Minimal Parser-Truth Lineage

The schema must preserve enough lineage for analytics review without storing raw
evidence:

- `source_parser_surface` names the parser surface, such as
  `MatchSummary.to_match_log_row`, `GameSummary.to_game_log_row`,
  `gameplay_action_entry`, or `opponent_card_observation`.
- `source_fact_key` names the normalized field or field group, such as
  `match_id`, `game1_mulligans`, `opening_hand_cards`, or `action_type`.
- `parser_schema_version` records the parser/schema surface version available
  at ingest time.
- `ingest_run_id` links to the local ingest run.
- `fact_provenance` stores path labels, ledger entry ids, and drift flags
  without raw payload values.

The schema must not store raw log bodies, raw saved-event lines, raw private
Player.log excerpts, local source file paths, webhook URLs, workbook IDs, or
credential material.

## Required Table Families

### Migration And Ingest Metadata

Required tables:

- `schema_migrations`
- `ingest_runs`
- `parser_schema_versions`

`schema_migrations` must record:

- migration id
- migration filename
- checksum or hash
- applied timestamp
- schema version after migration

`ingest_runs` must record:

- deterministic or generated `ingest_run_id`
- source kind, such as `live_parser`, `saved_event_replay`, or
  `sanitized_golden_replay`
- source artifact label, without raw local paths
- started/finished timestamps
- status: `started`, `completed`, `failed`, or `aborted`
- parser commit or version when available
- schema version
- row counts by table, as summary metadata only

`parser_schema_versions` must record:

- parser schema version id
- parser code version or commit when available
- relevant source surfaces, such as `MatchLogRow`, `GameLogRow`,
  `gameplay_action_entry`, `opponent_card_observation`, and field-evidence
  schema version
- created timestamp

### Identity Tables

Required tables:

- `matches`
- `games`
- `game_players`
- `sessions`
- `deck_labels`

`matches` must use parser `match_id` as the stable primary identity when
available. It must not invent a final match id when parser state cannot provide
one.

`games` must use deterministic `game_id`:

```text
<match_id>:g<game_number>
```

`game_players` must preserve parser-known seat/team/player-relation facts. It
must not use human labels, archetype labels, or workbook guesses to decide local
vs opponent identity.

`sessions` may group ingest runs or play sessions, but it must not depend on raw
local log paths.

`deck_labels` is allowed only for downstream deck/session labels, not parser
deck truth. Exact submitted-deck facts belong in submitted-deck tables.

### Result And Context Tables

Required tables:

- `match_results`
- `game_results`
- `match_context`
- `rank_snapshots`

`match_results` must store match result, winner team, games won/lost, total
games, match win flag, and game win rate as parser-derived facts.

`game_results` must store game winner, local result, pre/postboard label,
play/draw, turn count, game timing, and game duration when available.

`match_context` must store queue, format, event id, match win condition, and
event-identity classifier facets as parser-normalized context.

`rank_snapshots` must store rank fields and rank source as parser-normalized
context. Carried-forward or stale rank values must keep source/confidence
labels.

### Decision Snapshot Tables

Required tables:

- `opening_hands`
- `opening_hand_cards`
- `mulligan_events`
- `mulligan_bottomed_or_discarded_cards`
- `sideboarding_states`
- `submitted_deck_snapshots`
- `submitted_deck_cards`

`opening_hands` must store one row per game opening-hand snapshot. It may store
size even when exact card names are unavailable.

`opening_hand_cards` must store exact opening hand cards one row per visible
card slot/copy. It must not use delimited strings or JSON as canonical card
list truth.

`mulligan_events` must store parser-normalized mulligan counts or decisions
only when normalized evidence exists. Missing decision detail must be labeled
`expected_unavailable` or `not_yet_supported`, not guessed.

`mulligan_bottomed_or_discarded_cards` must store one card per row when exposed
and normalized. It must not infer hidden bottomed cards.

`sideboarding_states` may store sideboarding lifecycle and submit-deck seen
signals. It must not claim exact sideboard deltas unless submitted-deck card
evidence exists.

`submitted_deck_snapshots` and `submitted_deck_cards` must represent submitted
deck evidence. Deck names, collection matches, and card catalog names are
enrichment context and must not override submitted grpId evidence.

### Gameplay Fact Tables

Required tables:

- `turns`
- `gameplay_actions`
- `gameplay_action_cards`
- `card_movements`
- `life_totals`
- `public_zone_observations`
- `opponent_card_observations`
- `opponent_card_observation_cards`

`turns` must use parser-normalized turn numbers only.

`gameplay_actions` must store the broad gameplay-action fact as currently
normalized: timestamp, match id, game number, game state id, turn number, action
type, actor relation, zone context, annotation context, and source status. It
must not infer player mistakes, strategy, hidden cards, or decklists.

`gameplay_action_cards` must store one row per card associated with a gameplay
action. It must preserve `grp_id`, `observed_grp_id`, `overlay_grp_id`,
`object_source_grp_id`, `identity_hint_source`, name resolution status, and
enrichment labels when available.

`card_movements`, `life_totals`, and `public_zone_observations` are required
schema families but may begin as `not_yet_supported` or empty until parser-
normalized inputs exist. They must not be populated from raw logs by the
analytics layer.

`opponent_card_observations` must store only visible/degraded opponent-card
observations emitted by the parser observation surface. It must preserve source,
confidence, review-required, visibility, and degradation labels.

`opponent_card_observation_cards` is required when an observation can involve
more than one card. For current single-card observations, it may mirror the
single observed card in normalized child-row form or remain empty with tests
documenting the one-card current behavior.

### Human Annotation Tables

Required tables:

- `matchup_labels`
- `archetype_labels`
- `game_notes`

V1 human annotation scope is limited to matchup labels, archetype labels, and
game notes.

Annotation tables must:

- clearly use `value_source='human_annotation'`
- never overwrite parser-managed fact tables
- preserve author/source label when available without requiring personal
  account identifiers
- support current and historical annotation states
- link to parser fact ids such as `match_id` or `game_id`

Out of scope for v1 annotation tables:

- player mistake labels
- coaching verdicts
- sideboard advice
- Line Tracer labels
- AI-generated recommendations
- model-provider output

### Detailed Provenance Table

Required table:

- `fact_provenance`

Required logical columns:

- `fact_provenance_id`
- `fact_table`
- `fact_id`
- `fact_field`
- `ledger_entry_id`
- `source_parser_surface`
- `source_fact_key`
- `source_event_kind`
- `source_event_type`
- `source_payload_paths`
- `source_event_timestamp`
- `value_source`
- `confidence`
- `finality`
- `drift_flags`
- `invariant_status`
- `degraded_reason`
- `review_required`
- `ingest_run_id`
- `created_at`

`source_payload_paths` and `drift_flags` may be stored as JSON text arrays if
tests validate they contain labels/paths only and no raw payload values.

`fact_provenance` must support multiple provenance rows per fact and per field.
It must not be reduced to one row per match or one row per game.

### Derived Views

Required initial view families:

- opening-hand card views
- opening-line views
- mulligan outcome views
- game 1 vs post-board views
- play/draw split views
- sample-size and confidence-warning views
- matchup/archetype performance views using human labels only as downstream
  filters

View names should use the `v_` prefix.

Recommended v1 views:

- `v_opening_hand_cards`
- `v_opening_lines`
- `v_mulligan_outcomes`
- `v_game1_vs_postboard`
- `v_play_draw_splits`
- `v_sample_size_warnings`
- `v_matchup_label_performance`

Stored summary tables are out of scope for v1 unless a future contract explains
why a view is insufficient.

## Deterministic ID And Idempotency Policy

Primary analytic fact IDs must be deterministic text IDs where source facts have
stable parser identity.

Required recipes:

- `match_id`: parser match id.
- `game_id`: `<match_id>:g<game_number>`.
- `game_player_id`: `<game_id>:team<team_id>` or `<game_id>:seat<seat_id>`
  depending on the strongest parser-normalized identity available.
- `opening_hand_id`: `<game_id>:opening_hand`.
- `opening_hand_card_id`: `<opening_hand_id>:slot<position>`.
- `mulligan_event_id`: `<game_id>:mulligan:<ordinal_or_count>`.
- `submitted_deck_snapshot_id`: `<game_id>:submitted_deck`.
- `submitted_deck_card_id`: `<submitted_deck_snapshot_id>:<section>:<grp_id_or_card_key>:<ordinal_or_quantity_key>`.
- `gameplay_action_id`: a stable text hash or normalized tuple based on
  match id, game number, game state id, turn number, action type, instance id,
  actor relation, source/destination zones, and canonical card id fields.
- `opponent_card_observation_id`: a stable text hash or normalized tuple based
  on the source gameplay action id plus observation card identity and visibility
  fields.

Hash-based IDs are allowed when the normalized tuple would be too long, but the
hash input must be sorted, deterministic, and covered by tests.

Replay idempotency requirements:

- Replaying the same parser-normalized fixture twice must not duplicate fact
  rows.
- Replaying the same saved-event-derived normalized facts twice may create a
  second `ingest_runs` row, but fact tables must converge to the same fact row
  set.
- `INSERT OR REPLACE`, `ON CONFLICT DO UPDATE`, or equivalent upsert behavior
  must not erase stronger provenance with weaker provenance unless a later
  contract defines reconciliation rules.
- Raw-hash replay dedupe is scoped to saved-event replay. SQLite fact
  idempotency must rely on deterministic fact IDs, not raw saved-event hashes.

## Migration Policy

Migrations must be plain SQL files with monotonic numeric prefixes.

Required migration behavior:

- apply cleanly to an empty SQLite database
- create `schema_migrations` first or inside the first migration
- record migration filename and checksum
- be inspectable without running Python code generation
- avoid destructive table drops in v1
- use `CREATE TABLE IF NOT EXISTS` only when doing so does not hide schema drift
  from tests
- declare indexes for common joins by match id, game id, ingest run, and fact
  provenance lookup
- use foreign keys where practical, with `PRAGMA foreign_keys = ON` in tests

The first implementation may test migrations by reading and executing SQL files
directly against a temporary SQLite database. A production migration runner is a
later implementation concern unless separately authorized.

If SQL migrations are packaged with the Python distribution, Codex C must also
account for package-data loading. If packaging is not implemented in the first
pass, the handoff must state that the migration files are repo-local source
artifacts only.

## Expected-But-Unavailable Fact Policy

The schema must represent facts that are expected by the analytics model but
unavailable from current normalized parser output.

Required behavior:

- Use `availability_status='expected_unavailable'` when the fact is expected
  for analytics but the source evidence is missing or degraded.
- Use `availability_status='not_yet_supported'` when the table exists for
  future schema stability but no parser-normalized source is implemented yet.
- Use `availability_status='not_applicable'` when the fact does not apply, such
  as a third game in a two-game match.
- Use `availability_status='not_observed'` when the parser-normalized evidence
  indicates the event did not happen.
- Do not turn unavailable facts into zeros, blanks, or false labels unless the
  parser-normalized fact says the value is truly zero/false.

## Canonical Card-List Modeling

Canonical card lists must use child rows, not semicolon strings, delimited text,
or display JSON.

Opening hands and mulliganed-away card lists must use one row per observed card
slot/copy.

Submitted-deck cards should use one row per submitted card identity per section
with `quantity` when the source is count-based. If analytics needs copy-level
deck rows later, a view may expand quantities into copy rows.

Card display names, candidate names, layouts, and faces are enrichment context.
Durable card identity must prefer parser-normalized `grp_id` or documented
identity fields and must preserve unresolved/degraded status.

## Error Behavior

Malformed migration SQL:

- Future tests must fail fast and not create committed database artifacts.

Missing migration files:

- Future schema tests must fail with a clear missing-migration message.

Missing parser-normalized source facts:

- The schema must allow expected-but-unavailable rows or omit rows according to
  the table policy, but it must not guess facts.

Conflicting provenance:

- Store `value_source='conflict'`, `confidence='low'`, and
  `drift_status='conflict'`; detailed flags belong in `fact_provenance`.

Contract ambiguity:

- Route back to Codex B before Codex C creates a narrower or incompatible schema
  than this contract describes.

Raw/private input pressure:

- Stop before storing raw Player.log payloads, raw saved-event lines, absolute
  local source paths, webhook URLs, workbook IDs, or secrets.

## Side Effects

Allowed future implementation side effects:

- add source-controlled SQL migration files
- add focused schema tests
- add `.gitignore` coverage for `data/analytics/`
- create temporary SQLite databases under test-managed temporary directories
- create docs handoffs and review reports

Forbidden side effects without a later contract:

- create or commit `data/analytics/mythic_edge.sqlite3`
- create a production migration runner
- wire the schema into live parser runtime
- ingest live parser events into SQLite
- change parser output shape
- change workbook or webhook shape
- post analytics data to Google Sheets
- add OpenAI API or model-provider runtime integration
- implement AI coaching or Line Tracer
- store raw Player.log payloads

## Dependency Order

Recommended future implementation order:

1. Add `data/analytics/` to `.gitignore`.
2. Add plain SQL migration directory and `0001_initial_analytics_schema.sql`.
3. Add schema tests that apply migrations to a temporary SQLite database.
4. Assert required tables, columns, constraints, indexes, and views exist.
5. Assert required fact tables include core provenance columns.
6. Assert `fact_provenance` can represent field-level provenance without raw
   payload values.
7. Add deterministic-ID and replay-idempotency tests using reduced
   parser-normalized fixtures only if schema-only tests are not enough.
8. Route to a separate analytics ingest contract before live or replay ingest is
   implemented.

## Compatibility

- Existing parser/model row dictionaries remain unchanged.
- Existing workbook row keys remain unchanged.
- Existing webhook payload shape remains unchanged.
- Existing Apps Script behavior remains unchanged.
- Existing runtime JSON artifacts remain unchanged.
- Existing `analytics_sidecar.py` behavior remains unchanged.
- Existing saved-event replay behavior remains unchanged.
- Existing evidence-ledger and runtime field-evidence shapes remain unchanged.
- Historical records without evidence metadata may be ingested later only with
  explicit `unknown`, `not_checked`, or `legacy_enriched` labels as appropriate.
- `MGTA Start Time` keeps its current spelling in workbook-facing surfaces; the
  SQLite schema may use clear internal names such as `match_started_at` while
  preserving source fact keys.

## Tests Required

Future schema implementation should add focused tests under
`tests/test_analytics_schema*.py`.

Required validation:

```powershell
py -m pytest -q tests/test_analytics_schema*.py
py -m pytest -q tests/test_analytics_sidecar.py tests/test_saved_event_replay.py
py -m pytest -q tests/test_app_models.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
py -m pytest -q tests/test_evidence_ledger.py tests/test_runtime_field_evidence.py
py -m ruff check src tests tools
git diff --check
@'
.gitignore
src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
tests/test_analytics_schema.py
docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md
'@ | py tools\check_secret_patterns.py --base HEAD --paths-from-stdin
```

Expected test assertions:

- migrations apply to an empty temporary SQLite database
- `schema_migrations` records migration identity and checksum
- default database path is documented and generated DB files are ignored
- required tables exist
- required views exist
- required fact tables include core provenance columns
- `fact_provenance` supports multiple rows per fact/field
- value-source, confidence, finality, drift-status, and availability labels are
  constrained or validated
- no canonical card list is stored only as delimited text or JSON
- expected-but-unavailable facts can be represented distinctly from did-not-
  happen facts
- deterministic fact IDs are stable across repeated normalized replay
- no raw Player.log payloads, local paths, webhook URLs, workbook IDs, secrets,
  generated data, runtime status artifacts, failed-post artifacts, or workbook exports
  are committed

## Acceptance Criteria

- `docs/contracts/analytics_local_sqlite_schema.md` exists.
- The contract names the local analytics foundation as the schema owner and
  preserves parser/state truth ownership.
- The contract defines `data/analytics/mythic_edge.sqlite3` as the default local
  generated database path.
- The contract requires generated analytics database files to be ignored by Git.
- The contract defines plain SQL migration policy and the first migration path.
- The contract defines deterministic text ID and replay-idempotency rules.
- The contract forbids raw Player.log payload storage in SQLite.
- The contract defines minimal parser-truth lineage without raw-evidence logs.
- The contract requires core provenance columns on each fact table.
- The contract defines `fact_provenance`.
- The contract defines expected-but-unavailable fact handling.
- The contract defines one-card-per-row canonical card-list modeling.
- The contract prefers SQL views before stored summary tables.
- The contract limits v1 human annotations to matchup/archetype labels and game
  notes.
- The contract keeps Google Sheets, AI coaching, Line Tracer, UI, and OpenAI API
  runtime integration out of scope.
- No behavior changes are implemented in the contract-writing pass.

## Unknowns

- Whether the first implementation should include only SQL migration files and
  schema tests, or also a small source module that exposes migration paths.
- Whether migration SQL should be packaged for installed-wheel execution in the
  first implementation or treated as repo-local source artifacts.
- Which exact parser-normalized fixture should be used first for deterministic
  replay-idempotency tests.
- Whether future ingest should read `MatchSummary`/`GameSummary` objects,
  workbook row dictionaries, runtime JSON artifacts, or a new normalized
  analytics DTO.
- Whether card movements, life totals, and public-zone observations should
  remain empty schema-only tables until their own ingest contract.
- Whether `confidence` should later gain numeric scores in addition to labels.
- Whether human annotations should support audit history in v1 or only current
  labels/notes plus timestamps.
- Whether the broad schema should include draft-specific tables in v1 or defer
  them to a draft analytics contract.

## Suspected Implementation Gaps

- No SQLite database path, migration directory, or migration file exists.
- `.gitignore` does not currently ignore `data/analytics/`.
- No schema tests exist for SQLite migrations, tables, constraints, or views.
- No code maps parser-normalized rows into analytic fact IDs.
- No replay-to-SQLite idempotency test exists.
- No `fact_provenance` table exists.
- No expected-but-unavailable fact vocabulary exists in code.
- Existing runtime artifacts are JSON/Markdown, not SQLite facts.
- Existing card-performance artifacts are derived analytics reports, not a
  normalized local analytics warehouse.
- Existing saved-event replay reconstructs events but does not produce
  parser-normalized analytics database rows.
- Existing evidence-ledger metadata is not attached to current model rows and
  should remain separate unless a future contract changes that.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior
- parser state final reconciliation
- parser event classes
- event kind values
- parser payload shapes
- match identity
- game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- output transport
- live workbook state
- deployed Apps Script state
- production behavior
- AI truth
- model-provider behavior
- OpenAI API runtime integration
- Google Sheets sync
- Line Tracer behavior
- secrets, credentials, tokens, API keys, webhook URLs, or environment-variable
  contracts
- raw Player.log files or raw private Player.log excerpts
- generated card/tier data
- runtime status files
- failed posts
- workbook exports
- local runtime artifacts

The later implementation may create a new local SQLite schema surface only
inside the files and side effects authorized by this contract.

## Validation Expectations For This Contract

Contract-writer validation:

```powershell
git status --short --branch
git diff --check
```

Because this contract is a new untracked file until staged, Codex B should also
use an equivalent new-file whitespace check.

No runtime tests are required for this docs-only contract pass.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for the Analytics Local SQLite Schema Contract.

Source artifact:
docs/contracts/analytics_local_sqlite_schema.md

Parent artifacts:
- docs/problem_representations/analytics_schema_contract.md
- docs/problem_representations/local_analytics_foundation.md

Branch:
codex/analytics-foundation

Goal:
Compare the current repo to docs/contracts/analytics_local_sqlite_schema.md, then implement only the narrow schema-first pieces needed for the first local analytics SQLite schema: Git ignore coverage, plain SQL migration file(s), focused schema tests, and an implementation handoff. Do not implement live ingest, replay ingest, a production migration runner, Google Sheets sync, AI coaching, Line Tracer, or OpenAI runtime integration.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/problem_representations/local_analytics_foundation.md
- docs/problem_representations/analytics_schema_contract.md
- docs/contracts/analytics_local_sqlite_schema.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/analytics_sidecar.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- tests/test_app_models.py
- tests/test_analytics_sidecar.py
- tests/test_saved_event_replay.py
- tests/test_gameplay_actions.py
- tests/test_opponent_card_observations.py
- tests/test_evidence_ledger.py
- tests/test_runtime_field_evidence.py

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what the schema is supposed to do, what current repo behavior already provides, what is missing, and the exact minimal implementation plan.

Allowed implementation scope:
- Add data/analytics/ to .gitignore.
- Add plain SQL migration files under src/mythic_edge_parser/app/analytics_migrations/.
- Add focused schema tests under tests/test_analytics_schema*.py.
- Add test-only helpers or a tiny migration-path helper only if needed to make migration tests maintainable.
- Produce docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md.

Do not:
- create or commit data/analytics/mythic_edge.sqlite3 or any SQLite journal/WAL/SHM file
- create a production migration runner unless the user explicitly expands scope
- implement live ingest or replay ingest
- store raw Player.log payloads or raw saved-event lines in SQLite
- change parser behavior
- change parser state final reconciliation
- change parser event classes
- change match/game identity or deduplication
- change workbook schema, webhook payload shape, Apps Script behavior, or output transport
- change production behavior, AI truth, model-provider behavior, secrets, environment variables, raw logs, generated data, runtime status files, failed-post artifacts, workbook exports, or local runtime artifacts
- implement Google Sheets sync
- implement AI coaching
- implement Line Tracer
- target main without explicit approval
- stage, commit, push, open a PR, merge, or close issues unless explicitly asked

Validation:
git status --short --branch
py -m pytest -q tests/test_analytics_schema*.py
py -m pytest -q tests/test_analytics_sidecar.py tests/test_saved_event_replay.py
py -m pytest -q tests/test_app_models.py tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
py -m pytest -q tests/test_evidence_ledger.py tests/test_runtime_field_evidence.py
py -m ruff check src tests tools
git diff --check
@'
.gitignore
src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
tests/test_analytics_schema.py
docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md
'@ | py tools\check_secret_patterns.py --base HEAD --paths-from-stdin

Final handoff must include:
- role performed
- source contract used
- files changed
- exact schema/migration/test sections changed
- observed matches and gaps
- validation run
- protected-surface status
- whether any generated/local artifacts were created and removed or never created
- what remains unverified
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "not yet opened"
  tracker: "not yet opened"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/analytics_local_sqlite_schema.md"
  target_artifact: "docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "docs-only contract; runtime tests not required"
    - "git status --short --branch"
    - "git diff --check"
  stop_conditions:
    - "Do not implement live ingest, replay ingest, or a production migration runner without a follow-up contract or explicit user authorization."
    - "Do not create or commit SQLite database files."
    - "Do not store raw Player.log payloads in SQLite."
    - "Do not let analytics, Google Sheets, Line Tracer, OpenAI runtime, model-provider output, or AI own parser truth."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
    - "Do not target main without explicit approval."
```
