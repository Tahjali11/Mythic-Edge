# Local Analytics Foundation Problem Representation

## Summary

Mythic Edge needs a local analytics foundation that converts parser-normalized
match and game outputs into durable, queryable SQLite facts. The goal is to
store broad gameplay facts once, with provenance and schema discipline, so
future analytics such as opening-hand analysis, mulligan analysis, first-three
turn line tracing, sideboarding effectiveness, and card performance can be
derived without repeatedly redesigning the data model.

## Source Request Or Issue

Originating request: local planning discussion after completion of the
Player.log evidence ledger / parser drift protection phase.

Suggested issue title:

```text
[analytics] Local gameplay fact warehouse foundation
```

## Tracker

No tracker exists yet.

Suggested tracker:

```text
[analytics] Local analytics foundation
```

## What The Code Is Supposed To Do

The future analytics layer should read parser-owned normalized facts and
evidence/provenance metadata, then persist those facts into a local SQLite
database for deterministic analysis.

It should support both:

- live ingest from parser runtime outputs
- historical replay from saved parser-normalized artifacts

The database should store broad stable facts, not final strategic conclusions.
Strategic analytics, AI coaching, dashboards, and Google Sheets exports should
consume this local fact model rather than owning parser truth.

## What It Is Actually Doing

Today, Mythic Edge has strong parser, contract, provenance, drift, and replay
work, but it does not yet have a dedicated local gameplay fact warehouse.
Parser outputs and saved artifacts can preserve match data, but they are not
organized as a durable SQLite schema optimized for repeated analytics queries.

## Why This Matters

The user's original project goal is to turn MTGA outputs into useful match data
for improving play. After parser hardening and evidence-ledger work, the next
growth step is to make those trusted facts queryable across many games.

Without this foundation, future analytics risk becoming scattered scripts,
Google Sheets formulas, or one-off reports that are hard to validate, replay,
or extend. With this foundation, downstream tools can ask questions such as:

- Which opening hands win most often?
- Which mulligan decisions lead to losses?
- Which cards are best in opening hands?
- Which early-game lines win most often?
- Which sideboard plans improve post-board win rate?

## Project Layer

Primary layer: local analytics foundation.

Adjacent layers:

- parser and state interpretation: owns parser-managed facts
- Player.log evidence ledger: owns provenance, confidence, and drift metadata
- local SQLite analytics store: owns durable queryable analytic facts
- Google Sheets / Docs: optional collaboration and review exports only
- AI-assisted coaching: future explanation and hypothesis layer only

## First Bad Value

This is not a known bug. The first ambiguous boundary is that parser-normalized
outputs are not yet represented as a stable local fact schema.

First inspection order:

1. `docs/project_roadmap.md`
2. `docs/decisions/ADR-0001-parser-owns-truth.md`
3. `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
4. `docs/decisions/ADR-0003-player-log-drift-policy.md`
5. `docs/contracts/player_log_evidence_ledger.md`
6. `src/mythic_edge_parser/app/models.py`
7. `src/mythic_edge_parser/app/state.py`
8. `src/mythic_edge_parser/app/analytics_sidecar.py`
9. `src/mythic_edge_parser/app/runtime_surfaces.py`
10. `src/mythic_edge_parser/app/gameplay_actions.py`
11. `src/mythic_edge_parser/app/opponent_card_observations.py`
12. existing replay, golden fixture, schema snapshot, and evidence-ledger tests

## Inputs

Candidate inputs include parser-normalized outputs only:

- match summaries
- game summaries
- parser-managed match/game identity
- opening hand data
- mulligan data
- cards bottomed or discarded after mulligans when exposed and normalized
- turn numbers
- game actions
- card identity facts
- card movement or zone-change facts when normalized
- life total facts when normalized
- opponent-card observations
- sideboarding and submitted-deck facts
- evidence ledger source/confidence/finality/drift metadata
- optional human notes and labels entered downstream

Raw Player.log payloads should not be stored in the analytics database by
default.

## Expected Output

The first analytics foundation should produce a contract for a SQLite-backed
local gameplay fact warehouse.

Expected table families:

- identity tables: matches, games, players/seats, sessions, deck labels
- result tables: match results, game results, play/draw, queue/context
- decision snapshot tables: opening hands, opening hand cards, mulligans,
  bottomed/discarded cards when exposed
- gameplay fact tables: turns, game actions, card movements, life totals,
  public-zone observations, opponent-card observations
- annotation tables: match notes, game notes, turn/action notes, mulligan
  notes, sideboarding notes
- provenance tables: ingest runs, parser schema versions, source labels,
  confidence, finality, drift status
- derived views: opening-line views, play/draw splits, game 1 vs post-board
  splits, mulligan outcomes, sample-size warnings

The first implementation should store broad stable facts. It should not attempt
to answer every analytic question immediately.

## Scope

In scope:

- a SQLite schema contract for local gameplay facts
- deterministic IDs and upsert behavior
- parser-normalized output ingest boundaries
- live ingest and historical replay compatibility
- append-only fact tables plus current-state views or summaries
- event-level facts
- decision-point snapshots
- provenance, confidence, finality, and drift metadata
- human annotation boundaries
- derivation rules for initial SQL views
- validation expectations for replaying saved normalized artifacts

Out of scope:

- raw Player.log storage in SQLite
- Google Sheets sync implementation
- Google Docs integration
- AI coaching
- Line Tracer implementation
- UI or mobile app work
- workbook schema changes
- webhook payload shape changes
- Apps Script changes
- parser behavior changes
- parser state final reconciliation changes
- changes to match/game identity or deduplication
- model-provider or OpenAI API runtime behavior

## Risks And Likely Breakpoints

- Overbuilding analytics before the fact model is stable.
- Creating one giant table instead of normalized fact tables.
- Storing raw logs or private artifacts in the analytics database by accident.
- Treating analytics-derived values as parser truth.
- Duplicating facts when historical replay is run more than once.
- Losing confidence/finality/drift metadata during ingest.
- Designing first-three-turn line storage as primary truth instead of deriving
  it from stored turn/action facts.
- Letting Google Sheets become the analytics truth owner.
- Mixing human notes with parser-managed facts.
- Failing to version schema migrations.
- Depending on card names instead of durable card identity fields.

## Validation Evidence Needed

The eventual implementation should prove:

```bash
py -m pytest -q tests/test_analytics_*.py
py -m pytest -q tests/test_runner.py tests/test_analytics_sidecar.py
py -m ruff check src tests tools
git diff --check
```

Additional expected validation:

- replaying the same normalized fixture twice does not duplicate facts
- required provenance columns are present on fact tables
- low-confidence or inferred facts remain labeled
- SQL views derive opening lines from stored actions
- human annotations do not overwrite parser-managed facts
- no raw Player.log payloads, generated data, failed posts, workbook exports,
  or local-only artifacts are committed

## Open Questions

- Which existing parser-normalized artifact should be the first replay input?
- Which card-movement and life-total facts are already normalized enough for
  the first schema contract?
- Should the first implementation include only schema and replay ingest, or
  also initial SQL views?

## Resolved Schema Decisions

- Default generated database path: `data/analytics/mythic_edge.sqlite3`.
- Store schema definitions as plain versioned SQL migrations.
- A small Python migration runner may be added later, but it should apply
  inspectable SQL files rather than hiding schema definitions in Python code.
- Use deterministic text IDs for primary analytic identities where possible.
- Duplicate core provenance columns on each fact table.
- Keep a more detailed `fact_provenance` table for expanded provenance.
- Store card lists as one card per row canonically.
- Optional display JSON may be added later as a convenience cache, but not as
  canonical truth.
- Use SQL views before stored derived summary tables.
- Initial human annotations are limited to matchup/archetype labels and game
  notes.
- Replay idempotency is a hard requirement.

## Recommended Workflow

Recommended first suite:

1. Analytics Schema Contract
   - Defines SQLite tables, stable IDs, provenance columns, schema versioning,
     and ownership boundaries.
   - Problem representation:
     `docs/problem_representations/analytics_schema_contract.md`
2. Analytics Ingest Contract
   - Defines how parser-normalized outputs become database rows through live
     ingest or replay.
3. Core Fact Tables
   - Match, game, player/seat, deck/session, result, and provenance tables.
4. Decision Snapshot Tables
   - Opening hand, opening hand cards, mulligan events, bottomed/discarded
     cards if exposed, sideboard/submitted deck snapshots.
5. Gameplay Event Tables
   - Turn, game action, card movement, life total, opponent-card observation,
     public zone observation.
6. Derived View Layer
   - SQL views for opening lines, play/draw splits, game 1 vs post-board,
     mulligan outcomes, and sample-size warnings.
7. Validation And Replay Harness
   - Proves saved normalized artifacts can be replayed into the same schema
     without duplicate facts.

## Next Workflow Action

Next role: Codex B / Module Contract Writer.

Expected contract artifact:

```text
docs/contracts/analytics_local_gameplay_fact_warehouse.md
```

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex B: Module Contract Writer for the Local Analytics Foundation.

Source artifact:
docs/problem_representations/local_analytics_foundation.md

Goal:
Produce docs/contracts/analytics_local_gameplay_fact_warehouse.md. Define the
contract for a SQLite-backed local gameplay fact warehouse that stores
parser-normalized match/game/action/decision facts plus provenance metadata.
Distinguish observed repo behavior, required guarantees, unknowns, suspected
gaps, and implementation boundaries. Do not implement code.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/project_roadmap.md
- docs/problem_representations/local_analytics_foundation.md
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
- SQLite schema ownership and boundaries
- parser-normalized outputs only, not raw Player.log storage
- deterministic IDs and upsert behavior
- live ingest and historical replay compatibility
- event-level facts and decision-point snapshots
- opening hands, mulligans, bottomed/discarded cards when exposed
- game actions, card identity, card movement, life totals, opponent-card
  observations, public-zone observations
- human notes as downstream annotations, not parser truth
- provenance, confidence, finality, and drift metadata
- derived SQL views for first analytics surfaces
- validation expectations and protected surfaces

Do not:
- implement code
- create a SQLite database file
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
  source_artifact: "docs/problem_representations/local_analytics_foundation.md"
  target_artifact: "docs/contracts/analytics_local_gameplay_fact_warehouse.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "planning artifact only; no code validation expected"
  stop_conditions:
    - "Do not implement code from this problem representation."
    - "Do not store raw Player.log payloads in SQLite by default."
    - "Do not let analytics, Google Sheets, or AI own parser truth."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
```
