# Analytics Parser-Normalized Replay Ingest Contract

## Module

Local Analytics Foundation parser-normalized replay ingest into SQLite.

This contract defines how Mythic Edge may ingest already-normalized parser
outputs into the local SQLite analytics schema for replay and test scenarios.
It is not a raw Player.log parser, not a saved-event replay runner, not a live
runtime integration, not a workbook sync, and not an AI or coaching layer.

## Source Issue

Source artifact: Codex A workflow handoff for:

```text
[analytics] Define parser-normalized replay ingest into SQLite
```

Current branch:

```text
codex/analytics-foundation
```

Parent artifacts:

- `docs/problem_representations/local_analytics_foundation.md`
- `docs/problem_representations/analytics_schema_contract.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/contracts/analytics_migration_loader.md`
- `docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md`
- `docs/implementation_handoffs/analytics_local_sqlite_schema_fixer.md`
- `docs/implementation_handoffs/analytics_migration_loader_comparison.md`

Tracker: N/A in current handoff.

## Related ADRs

- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

## Owning Layer

Primary owner: local analytics foundation.

Truth boundaries:

- Parser/state owns event interpretation, match/game identity, final
  reconciliation, and parser-normalized facts.
- The analytics ingest layer owns copying parser-normalized facts into local
  SQLite tables with deterministic IDs and provenance labels.
- The analytics ingest layer must not reinterpret raw events, infer missing
  match/game truth, change parser-owned row shape, or decide strategic meaning.
- The evidence ledger owns value-source, confidence, finality, drift, and
  invariant vocabulary when field-level evidence is supplied.
- SQLite owns local queryable storage shape, not parser truth.

Plain English: this module can take the rows the parser already produced and
store them in SQLite so future analytics can query them. It cannot decide what
happened in the match.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_parser_normalized_replay_ingest.md`

Future implementation files allowed by this contract:

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- focused updates to `tests/test_analytics_schema.py` only if they share small
  in-memory database helpers
- focused updates to `tests/test_analytics_migration_loader.py` only if a
  shared test helper must move without behavior change
- `docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md`

Files not owned by this contract:

- parser modules
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- workbook schema, webhook, Apps Script, runtime status artifacts, generated
  databases, generated card data, raw logs, failed posts, and workbook exports

## Observed Repo Behavior

Current analytics foundation state:

- `docs/contracts/analytics_local_sqlite_schema.md` defines SQLite schema v1.
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
  creates metadata, identity, result/context, decision, gameplay, observation,
  annotation, provenance, and derived-view tables.
- `src/mythic_edge_parser/app/analytics_migration_loader.py` discovers,
  loads, checksums, and applies analytics SQL migrations to a caller-supplied
  SQLite connection.
- `pyproject.toml` declares analytics migration SQL files as package data.
- `tests/test_analytics_schema.py` validates schema tables, views, vocabulary,
  provenance columns, expected-unavailable labels, and deterministic ID
  behavior at schema level.
- `tests/test_analytics_migration_loader.py` validates package-resource
  migration loading and idempotent migration application.
- `.gitignore` ignores `data/analytics/`.

Current parser-normalized sources:

- `src/mythic_edge_parser/app/models.py` emits parser-owned `MatchLogRow` and
  `GameLogRow` dictionaries through `MatchSummary.to_match_log_row()` and
  `GameSummary.to_game_log_row()`.
- `MatchLogRow` includes match id, match result fields, game result fields,
  game play/draw fields, game mulligan fields, turn count fields, queue/format
  fields, rank context, sideboard/submit-deck flags, and sync status.
- `GameLogRow` includes match id, game number, pre/postboard label, play/draw,
  mulligans, opening hand size, serialized opening hand names, serialized
  mulliganed-away names, game result, turn count, duration, event id, and queue
  type.
- `src/mythic_edge_parser/app/gameplay_actions.py` emits local gameplay action
  entries with match/game identity, timestamps, game state id, turn number,
  action type, cast mode, instance/card identity hints, actor relation, zone
  movement, raw action labels, and annotation labels.
- `src/mythic_edge_parser/app/opponent_card_observations.py` emits visible
  opponent-card observation payloads derived from gameplay action entries.
- `src/mythic_edge_parser/app/golden_replay.py` can produce reduced
  parser-owned rows for sanitized/synthetic golden replay fixtures, but it does
  not write SQLite facts.
- `src/mythic_edge_parser/app/saved_event_replay.py` replays saved event JSONL
  files through callbacks, but it does not produce analytics database rows.

Current gap:

- No `analytics_ingest.py` module exists.
- No public API accepts parser-normalized replay rows and writes SQLite facts.
- No tests prove replay/upsert idempotency into the SQLite schema.
- No tests prove ingest-run status, row counts, provenance labels, or generated
  database artifact safety.

## Public Interface

The future implementation should expose one small module:

```text
mythic_edge_parser.app.analytics_ingest
```

Required public constants:

```text
ANALYTICS_REPLAY_INGEST_SCHEMA_VERSION = "analytics_parser_normalized_replay_ingest.v1"
```

Required public data shapes may be dataclasses, typed dicts, or plain
documented dictionaries. The contract names the semantic shape rather than
forcing one Python implementation style.

Required input shape:

```text
ParserNormalizedReplayInput
```

Required fields:

- `source_kind: str`
- `source_artifact_label: str`
- `match_log_rows: list[dict[str, object]]`
- `game_log_rows: list[dict[str, object]]`

Optional fields:

- `gameplay_action_entries: list[dict[str, object]]`
- `opponent_card_observations: list[dict[str, object]]`
- `field_evidence_entries: list[dict[str, object]]`
- `parser_commit: str`
- `parser_version: str`
- `generated_at: str`

Required output shape:

```text
AnalyticsReplayIngestResult
```

Required fields:

- `ingest_run_id: str`
- `source_kind: str`
- `source_artifact_label: str`
- `status: str`
- `row_counts: dict[str, int]`
- `warnings: list[str]`
- `skipped: dict[str, int]`

Required public function:

```text
ingest_parser_normalized_replay(
    connection: sqlite3.Connection,
    replay: Mapping[str, object],
    *,
    started_at: str | None = None,
    finished_at: str | None = None,
) -> AnalyticsReplayIngestResult
```

Allowed helper functions if useful:

```text
normalize_parser_normalized_replay(replay: Mapping[str, object]) -> ParserNormalizedReplayInput
deterministic_ingest_run_id(replay: ParserNormalizedReplayInput) -> str
```

Forbidden public interfaces in this slice:

- no CLI
- no default database opener
- no live parser sidecar wiring
- no saved-event replay runner
- no raw Player.log reader
- no Google Sheets sync
- no webhook sender
- no Apps Script interaction
- no Line Tracer, AI coaching, OpenAI runtime, or model-provider integration

## Inputs

### Replay Source Kinds

Allowed `source_kind` values:

- `sanitized_golden_replay`
- `saved_event_replay`

The schema also permits `live_parser`, but live parser ingest is out of scope
for this contract.

### MatchLogRow Input

Input type: parser-owned dictionary.

Source examples:

- `MatchSummary.to_match_log_row(final=True)`
- reduced `parser_owned_rows.match_log_row` from golden replay reports

Required key candidates:

- `match_id` or `MTGA Match ID`
- `timestamp`
- `MTGA Sync Status`
- `MGTA Start Time`
- `MTGA End Time`
- `Match Win?`
- `Match Win Flag`
- `Games Won`
- `Games Lost`
- `Total Games`
- `Game Win %`
- `MTGA Format`
- `MTGA Event ID`
- `MTGA Queue Type`
- `MTGA Rank Raw`
- `My Rank`
- `MTGA Sideboard Entered`
- `MTGA Submit Deck Seen`
- `G1 Mulligans`, `G2 Mulligans`, `G3 Mulligans`
- `G1 Play / Draw`, `G2 Play / Draw`, `G3 Play / Draw`
- `G1 Turn Count`, `G2 Turn Count`, `G3 Turn Count`
- `Game 1 Result`, `Game 2 Result`, `Game 3 Result`

### GameLogRow Input

Input type: parser-owned dictionary.

Source examples:

- `GameSummary.to_game_log_row(match)`
- reduced `parser_owned_rows.game_log_rows` from golden replay reports

Required key candidates:

- `match_id` or `MTGA Match ID`
- `timestamp`
- `Game Number`
- `Pre / Postboard`
- `Play / Draw`
- `Mulligans`
- `Opening Hand Size`
- `Opening Hand`
- `Mulliganed Away`
- `Game Result`
- `Turn Count`
- `Game Duration`
- `MTGA Format`
- `MTGA Event ID`
- `MTGA Queue Type`

### Gameplay Action Entries

Optional input type: parser-normalized dictionaries from
`gameplay_actions.py`.

Expected key candidates:

- `timestamp`
- `match_id`
- `game_number`
- `game_state_id`
- `turn_number`
- `action_type`
- `cast_mode`
- `instance_id`
- `grp_id`
- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `parent_id`
- `identity_hint_source`
- `actor_relation`
- `from_zone_type`
- `to_zone_type`
- `raw_action_types`
- `annotation_types`
- `annotation_categories`
- `visible_in_log`

### Opponent Card Observations

Optional input type: parser-normalized dictionaries from
`opponent_card_observations.py`.

Expected key candidates:

- `match_id`
- `game_number`
- `game_state_id`
- `timestamp`
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
- `value_source`
- `confidence`
- `visibility`
- `from_zone_type`
- `to_zone_type`
- `degradation_flags`
- `review_required`

### Field Evidence Entries

Optional input type: reduced provenance dictionaries.

Field evidence may provide:

- source parser surface
- source fact key
- source event kind
- source event type
- source payload path labels
- source event timestamp
- value source
- confidence
- finality
- drift flags
- invariant status
- degraded reason
- review-required flag

Field evidence must not include raw Player.log payloads or private local paths.

## Outputs

Allowed database writes:

- `ingest_runs`
- `matches`
- `games`
- `match_results`
- `game_results`
- `match_context`
- `rank_snapshots`
- `opening_hands`
- `opening_hand_cards`
- `mulligan_events`
- `mulligan_bottomed_or_discarded_cards`
- `gameplay_actions`
- `gameplay_action_cards`
- `opponent_card_observations`
- `opponent_card_observation_cards`
- `fact_provenance`

Allowed no-op or deferred tables:

- `sessions`
- `game_players`
- `deck_labels`
- `sideboarding_states`
- `submitted_deck_snapshots`
- `submitted_deck_cards`
- `turns`
- `card_movements`
- `life_totals`
- `public_zone_observations`
- human annotation tables

Those tables may remain empty in this first ingest pass unless the
parser-normalized input supplies enough safe facts without guessing.

Forbidden outputs:

- generated committed SQLite database files
- raw Player.log payloads
- raw saved-event lines
- local raw file paths
- workbook rows or workbook exports
- webhook posts
- Apps Script changes
- runtime status artifacts
- failed posts
- generated card/tier data
- AI/coaching/Line Tracer outputs

## Required Guarantees

### Schema Bootstrap

`ingest_parser_normalized_replay()` must call or require
`apply_analytics_migrations()` before writing analytics facts.

Tests must prove an empty in-memory SQLite connection can be migrated and then
ingested in one focused flow.

### Replay Idempotency

The same parser-normalized replay input ingested twice must not duplicate fact
rows.

Required behavior:

- deterministic fact IDs are used for every inserted parser fact
- repeated ingest upserts or preserves the same rows
- row counts for facts converge after repeated ingest
- replay idempotency does not depend on raw saved-event hashes
- upsert behavior must not erase stronger provenance with weaker provenance

The implementation may either:

- use a deterministic `ingest_run_id` derived from `source_kind`,
  `source_artifact_label`, and a canonical hash of parser-normalized input; or
- create a new `ingest_runs` row per replay while proving fact tables converge.

Codex C must document which option it chooses. The recommended first-pass
choice is deterministic `ingest_run_id` because it makes test evidence simpler
and keeps repeated replay visibly idempotent.

### Match And Game Identity

Required behavior:

- `match_id` must come from parser-normalized row fields.
- `game_id` must be `<match_id>:g<game_number>`.
- Missing `match_id` in a match row is an ingest error.
- Missing or invalid `game_number` in a game row is an ingest error for that
  row; it must not produce a guessed game id.
- The ingest layer must not renumber games or merge matches.
- Match/game identity and deduplication rules remain parser-owned.

### Core Fact Mapping

V1 ingest must support at least these parser-normalized mappings:

- `MatchLogRow` to `matches`
- `MatchLogRow` to `match_results`
- `MatchLogRow` to `match_context`
- `MatchLogRow` rank fields to `rank_snapshots` when present
- `GameLogRow` to `games`
- `GameLogRow` to `game_results`
- `GameLogRow` opening-hand fields to `opening_hands`
- `GameLogRow` semicolon-delimited opening hand display names to
  `opening_hand_cards` as name-only card rows
- `GameLogRow` mulligan count to `mulligan_events`
- `GameLogRow` semicolon-delimited mulliganed-away display names to
  `mulligan_bottomed_or_discarded_cards` as name-only card rows

V1 ingest may support, but is not required to fully populate:

- `gameplay_actions`
- `gameplay_action_cards`
- `opponent_card_observations`
- `opponent_card_observation_cards`

If those optional payloads are accepted, their IDs and provenance must be
deterministic and tested.

### Card Identity Boundary

Opening-hand and mulliganed-away card names from `GameLogRow` are parser-owned
display values, not durable card identity.

Required behavior:

- A semicolon-delimited display card list may be split into one child row per
  visible card name.
- Those rows must use `grp_id = NULL` unless a parser-normalized `grp_id` is
  explicitly supplied.
- Name-only card rows must carry an identity hint such as
  `identity_hint_source='name_only_from_parser_row'`.
- Name-only card rows must not be treated as confirmed card identity,
  collection matching, decklist truth, or gameplay advice.
- Placeholder or unavailable card-list values must not be guessed.

### Provenance And Status Labels

Each inserted fact row must populate the core provenance columns required by
the schema:

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

Default labels when field evidence is not supplied:

- parser-normalized row values: `value_source='derived'`
- no field-level evidence available: `confidence='unknown'`
- final match/game rows: `finality='final'` or `finality='reconciled'`
- live rows if ever supplied in test input: `finality='provisional'`
- no drift report supplied: `drift_status='not_checked'`
- present parser-normalized value: `availability_status='available'`
- empty optional value: omit the row when safe or use
  `availability_status='expected_unavailable'` only when the table policy
  expects a row

If field evidence is supplied, its labels may override defaults only when they
match the analytics schema vocabulary and do not contain raw payloads.

### Detailed Fact Provenance

V1 ingest must write focused `fact_provenance` rows for core inserted facts.

Minimum required provenance coverage:

- match identity/result row
- each game result row
- each opening hand row
- each mulligan event row
- each gameplay action row if optional action ingest is implemented
- each opponent-card observation row if optional observation ingest is
  implemented

`fact_provenance.source_payload_paths` must contain labels or JSON-pointer-like
paths only. It must not contain raw Player.log snippets, raw JSON payload
copies, webhook URLs, workbook IDs, API keys, local file paths, or secrets.

### Ingest Run Status

Each successful ingest must write or update one `ingest_runs` row with:

- `source_kind`
- `source_artifact_label`
- `started_at`
- `finished_at`
- `status='completed'`
- `parser_commit`
- `parser_version`
- `schema_version='analytics_local_sqlite_schema.v1'`
- `row_counts_json`

Failure behavior must be explicit. Codex C may choose either:

- all-or-nothing transaction with no failed `ingest_runs` row; or
- a failed `ingest_runs` row with no partial parser fact rows.

The chosen behavior must be tested for at least one malformed-input case.

## Error Behavior

Missing match id:

- Fail clearly before inserting match/game facts for that replay.

Missing source artifact label:

- Fail clearly. The ingest run must not use a blank label.

Unsupported source kind:

- Fail clearly. `live_parser` must remain out of scope for this contract.

Malformed game number:

- Fail clearly for the replay input unless Codex C documents row-level skip
  behavior and records a warning. The first implementation should fail fast.

Malformed numeric fields:

- Do not coerce arbitrary text into zero.
- Empty string means unavailable, not zero.
- Boolean values must not be accepted as integer counts.

Malformed card list:

- Do not guess identity. Preserve only safe display names when parseable.
- If parsing is ambiguous, omit child rows and record a warning.

SQLite constraint failure:

- Roll back the ingest transaction or otherwise prove no partial fact set is
  left behind.

Contract ambiguity:

- Route back to Codex B before adding live ingest, a default database path,
  raw replay parsing, schema migrations, CLI behavior, external writes, or
  analytics conclusions.

## Side Effects

Allowed future implementation side effects:

- add an ingest module
- add focused in-memory SQLite ingest tests
- write implementation handoff docs
- create temporary SQLite connections in tests
- optionally create test-managed temporary SQLite files if a specific SQLite
  behavior cannot be tested in memory

Forbidden side effects:

- create or commit `data/analytics/mythic_edge.sqlite3`
- create or commit SQLite journal/WAL/SHM files
- create or commit raw Player.log excerpts
- create or commit local saved-event JSONL from private data
- modify parser behavior
- modify parser final reconciliation
- modify parser event classes or event kind values
- modify match/game identity or deduplication
- modify workbook schema
- modify webhook payload shape
- modify Apps Script behavior
- post to webhooks or Google Sheets
- change runtime status artifacts
- change generated card/tier data
- add production behavior
- add AI, coaching, Line Tracer, or model-provider behavior

## Dependency Order

Recommended Codex C implementation order:

1. Confirm branch and worktree status on `codex/analytics-foundation`.
2. Inspect `analytics_local_sqlite_schema.md`, `analytics_migration_loader.md`,
   current SQL migration, and migration loader tests.
3. Add the smallest `analytics_ingest.py` interface.
4. Add in-memory tests that apply migrations and ingest one reduced
   parser-normalized match with one or more game rows.
5. Prove replay idempotency by ingesting the same normalized input twice.
6. Prove core provenance/status labels and `fact_provenance` rows.
7. Prove malformed input fails without partial fact rows.
8. Run focused validation and protected-surface scans.
9. Produce
   `docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md`.

## Compatibility

- Existing parser row dictionaries remain unchanged.
- Existing golden replay behavior remains unchanged.
- Existing saved-event replay behavior remains unchanged.
- Existing analytics migration loader behavior remains unchanged.
- Existing SQLite schema migration remains unchanged unless a separate schema
  amendment contract authorizes a change.
- Existing workbook row keys, sync fields, webhook payload shape, Apps Script
  behavior, and runtime status artifacts remain unchanged.
- `MGTA Start Time` keeps its current workbook-facing spelling; ingest may map
  it to `match_started_at` internally.
- The analytics ingest layer may read workbook-shaped parser rows, but it must
  not make workbook schema the source of parser truth.

## Tests Required

Future implementation should add focused tests under:

```text
tests/test_analytics_parser_normalized_replay_ingest.py
```

Required test assertions:

- an empty in-memory SQLite connection is migrated through
  `apply_analytics_migrations()` and then ingested
- a reduced parser-normalized replay with one `MatchLogRow` and at least one
  `GameLogRow` writes expected rows to `ingest_runs`, `matches`, `games`,
  `match_results`, `game_results`, and at least one decision table
- replaying the same normalized input twice does not duplicate fact rows
- row counts in the result and `ingest_runs.row_counts_json` match actual
  inserted/upserted facts
- core provenance columns are populated with safe fallback labels
- focused `fact_provenance` rows are present and contain labels/paths, not raw
  payloads
- empty optional fields are not coerced into zero/false
- name-only opening-hand rows do not claim `grp_id`
- malformed required identity fails clearly without partial fact rows
- no generated SQLite files under `data/analytics/` are created or committed

Recommended validation:

```powershell
py -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
py -m pytest -q tests/test_app_models.py tests/test_golden_replay_harness.py
py -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
py -m ruff check src tests tools
git diff --check
@'
src/mythic_edge_parser/app/analytics_ingest.py
tests/test_analytics_parser_normalized_replay_ingest.py
docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
src/mythic_edge_parser/app/analytics_ingest.py
tests/test_analytics_parser_normalized_replay_ingest.py
docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Codex C should also report a generated artifact check confirming no changed or
untracked SQLite DB/journal/WAL/SHM files exist.

## Acceptance Criteria

- `docs/contracts/analytics_parser_normalized_replay_ingest.md` exists.
- The contract defines parser-normalized replay ingest only.
- The contract preserves parser truth ownership and protected surfaces.
- The implementation ingests parser-owned row dictionaries into the existing
  SQLite schema using the migration loader.
- The implementation proves replay/upsert idempotency.
- The implementation proves provenance/status labels.
- The implementation does not store raw Player.log payloads or raw saved-event
  lines.
- The implementation does not create or commit generated SQLite database files.
- The implementation does not implement live ingest, saved-event replay
  running, CLI, Google Sheets sync, workbook/webhook/App Script changes, Line
  Tracer, AI coaching, or OpenAI runtime integration.

## Unknowns

- Whether future ingest should use a deterministic `ingest_run_id` for every
  replay or create separate ingest run records for repeated identical replays.
- Whether future saved-event replay should produce the normalized input bundle
  directly or route through golden replay style reduced parser-owned output.
- Whether gameplay action and opponent observation ingest should be included in
  the first implementation or deferred to a second ingest slice.
- Whether field evidence should be required before analytics uses high
  confidence labels.
- Whether future schema versions need additional columns for normalized input
  hashes or row-level ingest status.

## Suspected Implementation Gaps

- No `analytics_ingest.py` module exists.
- No tests currently map parser-owned rows into SQLite fact tables.
- No tests currently prove replay idempotency beyond schema-level insert
  examples.
- No code currently writes `ingest_runs` from parser-normalized replay input.
- No code currently writes `fact_provenance` for analytics facts.
- No code currently maps name-only opening-hand display rows without claiming
  durable card identity.

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
- generated SQLite database files
- runtime status files
- failed posts
- workbook exports
- local-only artifacts

## Validation Expectations For This Contract

This Codex B pass is documentation-only. Runtime tests are not required because
no runtime code should change.

Minimum contract-writer validation:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/analytics_parser_normalized_replay_ingest.md
'@ | py tools\check_secret_patterns.py --base HEAD --paths-from-stdin
@'
docs/contracts/analytics_parser_normalized_replay_ingest.md
'@ | py tools\check_protected_surfaces.py --base HEAD --paths-from-stdin
```

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for the Analytics parser-normalized replay ingest contract.

Branch:
codex/analytics-foundation

Source artifacts:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/analytics_local_sqlite_schema.md
- docs/contracts/analytics_migration_loader.md
- docs/contracts/analytics_parser_normalized_replay_ingest.md
- docs/implementation_handoffs/analytics_migration_loader_comparison.md
- src/mythic_edge_parser/app/analytics_migration_loader.py
- src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- tests/test_analytics_schema.py
- tests/test_analytics_migration_loader.py

Goal:
Compare the current repo to docs/contracts/analytics_parser_normalized_replay_ingest.md, then implement only the narrow parser-normalized replay ingest path into SQLite.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what parser-normalized replay ingest is supposed to do, what current code actually does, why ingest is missing, and the exact minimal implementation plan.

Do:
- Add a small analytics ingest module that accepts already-normalized parser row dictionaries and writes to the existing SQLite schema through a caller-supplied sqlite3.Connection.
- Use the existing analytics migration loader before writes.
- Ingest core MatchLogRow and GameLogRow facts into the existing schema.
- Preserve parser truth ownership.
- Add focused in-memory SQLite tests for migration plus ingest, idempotent replay/upsert, provenance/status labels, malformed required identity, and no generated database artifacts.
- Produce docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md.

Do not:
- parse raw Player.log
- run saved-event replay
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status artifacts, generated card/tier data, secrets, raw logs, failed posts, workbook exports, production behavior, AI coaching, Line Tracer, OpenAI runtime integration, or model-provider behavior
- create or commit data/analytics/mythic_edge.sqlite3 or any SQLite journal/WAL/SHM file
- target main
- stage, commit, push, open a PR, or merge unless explicitly asked

Validation:
py -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
py -m pytest -q tests/test_app_models.py tests/test_golden_replay_harness.py
py -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py
py -m ruff check src tests tools
git diff --check
Run path-scoped secret/private-marker and protected-surface checks over changed files with base origin/codex/analytics-foundation.
Confirm no generated SQLite DB/journal/WAL/SHM artifacts are changed or untracked.

Final handoff must include:
- role performed
- source artifacts used
- files changed
- exact ingest/test sections changed
- observed matches and remaining gaps against the contract
- validation run
- generated SQLite artifact status
- protected-surface status
- what remains unverified
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "Codex A workflow handoff for [analytics] Define parser-normalized replay ingest into SQLite"
  target_artifact: "docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md"
  contract_artifact: "docs/contracts/analytics_parser_normalized_replay_ingest.md"
  branch: "codex/analytics-foundation"
  risk_tier: "Medium"
  validation:
    - "docs-only contract; runtime tests not required"
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped secret/private-marker check for docs/contracts/analytics_parser_normalized_replay_ingest.md"
    - "path-scoped protected-surface check for docs/contracts/analytics_parser_normalized_replay_ingest.md"
  stop_conditions:
    - "Do not target main."
    - "Do not create or commit SQLite database files."
    - "Do not parse raw Player.log or run saved-event replay in this ingest slice."
    - "Do not implement live ingest, CLI, Google Sheets sync, Line Tracer, AI coaching, OpenAI runtime integration, or production behavior."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
```
