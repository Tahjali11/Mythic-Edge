# Analytics Schema Contract Problem Representation

## Summary

Mythic Edge needs a dedicated analytics schema contract before implementing the
local SQLite gameplay fact warehouse. The contract should define the broad
SQLite schema, migration policy, deterministic identity rules, provenance
columns, table families, and non-goals for converting parser-normalized facts
into durable local analytics data.

## Source Request Or Issue

Originating request: item 1 of the Local Analytics Foundation workflow,
"Analytics Schema Contract."

Parent planning artifact:

```text
docs/problem_representations/local_analytics_foundation.md
```

Suggested issue title:

```text
[analytics] Define local SQLite schema contract
```

## Tracker

No GitHub tracker exists yet.

Suggested tracker:

```text
[analytics] Local analytics foundation
```

## What The Code Is Supposed To Do

Future analytics code should persist parser-normalized match, game, action,
decision, observation, and annotation facts into a local SQLite database.

The schema should support both live ingest and historical replay. It should be
broad enough to support future analytics without repeated redesign, while still
making clear which tables can only be populated when normalized parser input
exists.

The schema should store parser-normalized facts and minimal parser-truth
lineage. It should not store raw Player.log payloads or become a second parser.

## What It Is Actually Doing

Mythic Edge currently has parser-managed summaries, gameplay-action artifacts,
opponent-card observation artifacts, evidence-ledger provenance, drift
contracts, replay tooling, and an analytics sidecar context. It does not yet
have a reviewed SQLite schema contract for the local analytics warehouse.

Without this contract, future analytics implementation could accidentally mix
parser truth, derived analytics, human annotations, Google Sheets exports, or AI
coaching concepts into one unstable storage model.

## Why This Matters

The analytics foundation should let Mythic Edge answer questions such as:

- Which opening hands win most often?
- Which mulligan decisions lead to losses?
- Which cards are best in opening hands?
- Which early-game lines win most often?
- Which sideboard plans improve post-board win rate?

Those questions require a stable fact model. The schema contract should make
facts queryable without weakening parser truth ownership, losing uncertainty
labels, duplicating rows during replay, or storing private raw data.

## Project Layer

Primary layer: local analytics foundation.

Truth and authority boundaries:

- parser/state owns parser-managed match, game, card, and gameplay facts
- Player.log evidence ledger owns provenance, confidence, finality, and drift
  context
- SQLite analytics schema owns local durable storage and queryable fact
  structure
- SQL views own deterministic derived query surfaces, not parser truth
- human labels and game notes are downstream annotations, not parser truth
- Google Sheets, Google Docs, dashboards, and AI coaching are downstream
  consumers

## First Bad Value

This is not a bug in existing code. The first ambiguous value is the missing
contract boundary for how parser-normalized outputs become SQLite tables,
columns, keys, views, and migrations.

First inspection order for Codex B:

1. `docs/problem_representations/local_analytics_foundation.md`
2. `docs/project_roadmap.md`
3. `docs/decisions/ADR-0001-parser-owns-truth.md`
4. `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
5. `docs/decisions/ADR-0003-player-log-drift-policy.md`
6. `docs/contracts/player_log_evidence_ledger.md`
7. `src/mythic_edge_parser/app/models.py`
8. `src/mythic_edge_parser/app/state.py`
9. `src/mythic_edge_parser/app/analytics_sidecar.py`
10. `src/mythic_edge_parser/app/runtime_surfaces.py`
11. `src/mythic_edge_parser/app/gameplay_actions.py`
12. `src/mythic_edge_parser/app/opponent_card_observations.py`
13. existing tests for models, runner, analytics sidecar, evidence ledger,
    gameplay actions, opponent-card observations, golden replay, and schema
    snapshots

## Inputs

In-scope input classes:

- parser-normalized match summaries
- parser-normalized game summaries
- match/game identity
- player/team/seat mappings
- match and game results
- play/draw
- queue, rank, format, and session context
- opening hand snapshots
- mulligan counts and mulligan decision facts
- cards bottomed or discarded after mulligans when exposed and normalized
- sideboarding and submitted-deck facts
- gameplay actions
- card identity facts
- card movement or zone-change facts when normalized
- life total facts when normalized
- public-zone observations when normalized
- opponent-card observations
- evidence/provenance labels
- matchup/archetype labels entered by the user
- game notes entered by the user

Out-of-scope inputs:

- raw Player.log payload storage
- raw local log paths
- webhook URLs, credentials, tokens, API keys, or secrets
- generated card/tier data blobs unless a later contract explicitly approves
  a sanitized reference table
- workbook exports
- failed posts
- runtime status files
- AI-generated recommendations as fact input

## Expected Output

Codex B should produce a schema contract:

```text
docs/contracts/analytics_local_sqlite_schema.md
```

The contract should define the expected SQLite schema at the table-family level
and, where appropriate, table/column-level requirements.

Required design decisions:

- default generated database path: `data/analytics/mythic_edge.sqlite3`
- the database file is local/generated and must be ignored by Git
- migrations use plain versioned SQL files
- a small Python migration runner may be added later, but schema definitions
  should remain inspectable SQL
- deterministic text IDs are the primary identity model
- replaying the same normalized match/game data must be idempotent
- broad schema v1 should be defined now, even when some tables begin empty
  until normalized input exists
- each core fact table should duplicate core provenance columns
- detailed provenance should also be supported by a `fact_provenance` table
- one-card-per-row is the canonical representation for card lists
- display JSON may be added later as a convenience cache, but not as canonical
  truth
- initial human annotations are limited to matchup/archetype labels and game
  notes
- SQL views are preferred before stored derived summary tables

## Required Table Families

The schema contract should cover these families.

Identity and ingest:

- `schema_migrations`
- `ingest_runs`
- `parser_schema_versions` or equivalent schema/version metadata
- `matches`
- `games`
- `players` or `game_players`
- `sessions`
- deck/session label tables

Results and context:

- match results
- game results
- play/draw
- queue, rank, format, event, and context facts

Decision snapshots:

- opening hands
- opening hand cards
- mulligan events
- mulligan bottomed/discarded cards when exposed and normalized
- sideboarding state
- submitted deck snapshots
- submitted deck cards

Gameplay facts:

- turns
- gameplay actions
- gameplay action cards, if the action can involve more than one card
- card movements or zone changes when normalized
- life totals when normalized
- public-zone observations when normalized
- opponent-card observations
- opponent-card observation cards, if needed

Human annotations:

- matchup/archetype labels
- game notes

Provenance:

- `fact_provenance`
- core provenance columns duplicated on fact rows:
  - `value_source`
  - `confidence`
  - `finality`
  - `drift_status`
  - `parser_schema_version`
  - `ingest_run_id`
  - `source_parser_surface`
  - `source_fact_key`

Derived views:

- opening-line views
- opening-hand card views
- mulligan outcome views
- game 1 vs post-board views
- play/draw split views
- sample-size and confidence-warning views

## Scope

In scope:

- schema contract only
- broad SQLite table-family design
- deterministic text ID policy
- upsert/idempotency requirements
- plain SQL migration policy
- generated/local database path policy
- Git ignore expectations for local database artifacts
- core provenance columns on every fact table
- `fact_provenance` detail table requirements
- one-card-per-row canonical card-list modeling
- expected-but-unavailable fact modeling
- SQL views before stored derived summary tables
- v1 human annotation scope: matchup/archetype labels and game notes
- validation expectations for future implementation

Out of scope:

- implementing migrations
- creating a SQLite database file
- creating a migration runner
- adding SQL files
- changing parser behavior
- changing parser state final reconciliation
- changing parser event classes
- changing match/game identity or deduplication
- changing workbook schema
- changing webhook payload shape
- changing Apps Script behavior
- changing output transport
- adding Google Sheets sync
- adding Google Docs integration
- adding AI coaching
- implementing Line Tracer
- storing raw Player.log payloads
- committing local analytics database files

## Risks And Likely Breakpoints

- Schema v1 becomes too narrow and forces redesign before analytics are useful.
- Schema v1 becomes too broad and implies unsupported parser facts are already
  available.
- Fact tables lose provenance metadata, causing downstream analytics to treat
  inferred or degraded values as clean truth.
- Replay ingest duplicates facts because IDs are not deterministic.
- One-card-per-row modeling is bypassed with JSON blobs, making card analytics
  hard to query.
- Human matchup labels and game notes accidentally overwrite parser-managed
  facts.
- SQL views are treated as parser truth instead of deterministic derived
  analytics.
- The generated SQLite database is accidentally committed.
- Plain SQL migrations drift from Python migration runner behavior when the
  runner is added later.
- Future Google Sheets or AI layers treat analytics outputs as parser truth.

## Validation Evidence Needed

The contract itself is documentation-only. Future implementation should prove:

```bash
py -m pytest -q tests/test_analytics_schema*.py
py -m pytest -q tests/test_analytics_ingest*.py
py -m ruff check src tests tools
git diff --check
```

Expected implementation validation:

- all SQL migrations apply to an empty SQLite database
- `schema_migrations` records applied migrations
- required tables and views exist
- required fact tables include core provenance columns
- `fact_provenance` can associate detailed provenance with fact rows
- deterministic IDs are stable across repeated replay
- replaying the same normalized fixture twice does not duplicate rows
- expected-but-unavailable facts can be represented distinctly from
  did-not-happen facts
- card lists are queryable one card per row
- matchup/archetype labels and game notes remain downstream annotations
- generated database files are ignored by Git
- no raw Player.log payloads, raw logs, generated data, failed posts, workbook
  exports, secrets, or local runtime artifacts are committed

## Open Questions For Codex B

- Which exact repo path should hold versioned SQL migrations?
- Should `parser_schema_version` be a free text value on rows, a foreign key to
  a schema-version table, or both?
- What is the minimum useful deterministic ID recipe for each table family?
- Should `confidence` be stored as a categorical label, numeric score, or both?
- Which currently normalized card-movement and life-total facts are safe to
  include as v1 populated tables, and which should be schema-only until later
  ingest work?
- Should expected-but-unavailable facts use a shared `availability_status`
  vocabulary?

## Next Workflow Action

Next role: Codex B / Module Contract Writer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex B: Module Contract Writer for the Analytics Schema Contract.

Source artifact:
docs/problem_representations/analytics_schema_contract.md

Parent artifact:
docs/problem_representations/local_analytics_foundation.md

Goal:
Produce docs/contracts/analytics_local_sqlite_schema.md. Define the contract
for the first broad SQLite schema in the Local Analytics Foundation. Distinguish
observed repo behavior, required guarantees, unknowns, suspected gaps, table
families, migration policy, validation expectations, and protected surfaces.
Do not implement code.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/project_roadmap.md
- docs/problem_representations/local_analytics_foundation.md
- docs/problem_representations/analytics_schema_contract.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/contracts/player_log_evidence_ledger.md
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/analytics_sidecar.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- relevant replay, golden fixture, schema snapshot, evidence-ledger, runner,
  and analytics-sidecar tests

Contract focus:
- broad SQLite schema v1 for local analytics facts
- default local database path: data/analytics/mythic_edge.sqlite3
- local/generated database files must be ignored by Git
- plain SQL migrations
- deterministic text IDs and replay idempotency
- parser-normalized outputs only, not raw Player.log storage
- minimal parser-truth lineage without raw-evidence reference logs
- core provenance columns duplicated on each fact table
- detailed fact_provenance table
- expected-but-unavailable facts
- one-card-per-row canonical card-list modeling
- SQL views before stored summary tables
- initial human annotations limited to matchup/archetype labels and game notes
- Google Sheets, AI coaching, Line Tracer, UI, and OpenAI runtime out of scope

Do not:
- implement code
- create migration files
- create a SQLite database file
- create a migration runner
- store raw Player.log payloads
- change parser behavior
- change parser state final reconciliation
- change parser event classes
- change match/game identity or deduplication
- change workbook schema, webhook payload shape, Apps Script behavior, output
  transport, production behavior, AI truth, model-provider behavior, secrets,
  environment variables, raw logs, generated data, runtime status files, failed
  posts, workbook exports, or local runtime artifacts
- implement Google Sheets sync
- implement AI coaching
- implement Line Tracer
- target main without explicit approval

Final output must include:
- role performed
- source artifact used
- contract artifact path
- observed behavior summary
- required guarantees
- table-family requirements
- migration policy
- unknowns and suspected gaps
- protected surfaces
- validation expectations
- next recommended role
- pasteable Codex C prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "not yet opened"
  tracker: "not yet opened"
  completed_thread: "A"
  next_thread: "B"
  source_artifact: "docs/problem_representations/analytics_schema_contract.md"
  target_artifact: "docs/contracts/analytics_local_sqlite_schema.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "planning artifact only; no code validation expected"
  stop_conditions:
    - "Do not implement code from this problem representation."
    - "Do not create migration files or a SQLite database in Codex B."
    - "Do not store raw Player.log payloads in SQLite by default."
    - "Do not let analytics, Google Sheets, or AI own parser truth."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
```
