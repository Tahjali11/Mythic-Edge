# Life Total Parser Coverage Problem Representation

## Summary

Historical saved JSONL data contains exposed life-total evidence in GRE
`GameState` player payloads, but Mythic Edge does not yet normalize that
evidence into parser-managed life-total outputs, life-total timelines, or
analytics-ready deltas.

Plain English: the parser is keeping the raw player records that contain life
totals, but it is not yet turning those values into a clean feature the rest of
the project can depend on.

## Source Request Or Issue

Source request: local Codex thread after the historical replay quality report.

No GitHub issue was opened in this pass.

## Tracker

N/A.

This should become a child issue under the future parser drift/evidence ledger
or analytics foundation tracker, depending on when it is implemented.

## Current Evidence

Read-only inspection found:

- `payload.raw_game_state.gameStateMessage.players[].lifeTotal`
- `payload.raw_game_state.gameStateMessage.players[].startingLifeTotal`
- `payload.players[].lifeTotal`
- `payload.players[].startingLifeTotal`

The local historical replay quality report counted:

- latest-per-day records with life total evidence: `3457`
- latest-per-day life total field hits: `5972`
- latest-per-day records with starting life total evidence: `3457`
- latest-per-day starting life total field hits: `5991`

The report is local/generated under `data/status/` and should not be committed
as source truth.

## What The Code Is Supposed To Do

The future life-total modules should:

- read exposed life totals from parser-owned `GameState` payloads
- map each life total to match, game, game state, timestamp, turn, seat, team,
  and local/opponent relation when available
- distinguish current life total from starting life total
- derive deltas only from observed consecutive values within the same game and
  seat
- label value source as observed or derived, never guessed
- produce local analytics-ready evidence without changing workbook schema or
  webhook payloads unless a later contract explicitly approves that surface

## What It Is Actually Doing

Current code preserves life-total evidence passively:

- `src/mythic_edge_parser/parsers/gre/game_state.py` copies `gsm.players` into
  top-level `payload["players"]`.
- The same module preserves the original message under
  `payload["raw_game_state"]`.
- `src/mythic_edge_parser/app/extractors.py` can read game-state players for
  team/seat mapping.

Current code does not appear to provide:

- a dedicated life-total parser module
- a normalized extractor for player life totals
- a life-total event or runtime surface
- life-total deltas
- tests asserting life-total extraction behavior
- analytics-ready life-total rows or summaries

## Why This Matters

Life totals are foundational for future analytics and coaching because they can
support questions like:

- which turns produce the largest life swings
- how often a deck stabilizes from low life
- whether low-curve matchups pressure life totals before key turns
- whether removal, blockers, or sideboard cards are changing the race
- whether a player is winning after falling behind or losing after early leads

If this remains only raw nested payload data, downstream analytics will either
ignore it or repeatedly reimplement fragile ad hoc extraction.

## Project Layer

Primary layer: parser and state interpretation.

Supporting layer: local analytics foundation.

Truth boundaries:

- MTGA `Player.log` / saved parser JSONL remains evidence.
- Parser/state owns normalized interpretation.
- A life-total module should own observed life-total extraction and derived
  deltas.
- Analytics may consume life totals, but analytics should not become the source
  of parser truth.
- Workbook, webhook, Apps Script, dashboard, Google Workspace, and AI coaching
  must remain downstream unless a later contract changes the interface.

## First Bad Value

The first missing value is not in raw data ingestion. It occurs after
`GameState` payload construction:

1. `GameState` contains `players[].lifeTotal` and
   `players[].startingLifeTotal`.
2. The parser preserves those player records.
3. No module normalizes those fields into stable parser-managed life-total
   records.

## Inputs

Representative inputs:

- saved parser JSONL records under `data/match_logs/`
- `GameState` payloads produced by
  `src/mythic_edge_parser/parsers/gre/game_state.py`
- player rows in `payload["players"]`
- fallback raw player rows in
  `payload["raw_game_state"]["gameStateMessage"]["players"]`

Relevant code to inspect:

- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- tests around GRE game state, extractors, gameplay actions, runtime surfaces,
  saved replay, and historical fixtures

## Expected Output

The expected v1 output should probably be local and parser-owned, not workbook
or webhook-facing.

Likely module set:

1. `life_totals` extractor helpers:
   - normalize player life rows from current and raw `GameState` payload shapes
   - preserve seat/team/local-opponent mapping where available

2. life-total runtime store:
   - track latest observed life total per match/game/seat
   - compute observed transitions and derived deltas
   - dedupe repeated identical observations from duplicate or unchanged game
     states

3. life-total local surface:
   - write ignored local status artifacts such as active-match and per-match
     life-total timelines
   - include source labels and confidence/finality metadata

4. historical validation report:
   - replay saved JSONL and count life-total extraction coverage
   - report missing identity, missing seat, malformed values, and delta quality
   - avoid embedding raw logs or private values in committed artifacts

5. later analytics integration:
   - consume normalized life-total timelines for race/stabilization/comeback
     analysis after the local analytics storage contract exists

## Scope

In scope for the future implementation:

- life-total extraction from `GameState` player payloads
- current and starting life total fields
- seat, team, local/opponent relation, match, game, turn, timestamp, game state
  id, source, confidence, and finality metadata
- local status/report artifacts only, unless a later interface contract expands
  the surface
- focused tests built from synthetic sanitized payloads
- read-only historical replay validation against local saved JSONL

Out of scope:

- changing raw MTGA parsing beyond existing `GameState` payload preservation
- changing parser event classes unless a contract explicitly requires it
- changing parser state final reconciliation
- changing match identity, game identity, or deduplication
- changing workbook schema
- changing webhook payload shape
- changing Apps Script behavior
- writing live workbook rows
- committing raw local logs or generated local status artifacts
- treating inferred combat damage, inferred damage sources, or AI commentary as
  parser truth

## Risks And Likely Breakpoints

- `players[].lifeTotal` may be present only in some `GameState` records.
- `startingLifeTotal` may duplicate across many records and should not be
  interpreted as a life-change event.
- Seat/team mapping may be missing or inconsistent in partial game states.
- Duplicate saved records can create false repeated observations if dedupe is
  not scoped correctly.
- Life deltas can be derived from consecutive observations, but damage source
  attribution is a separate harder problem.
- Analytics may be tempted to treat missing life totals as zero. That must be
  forbidden.
- Workbook/webhook surfaces should not expand accidentally while building local
  parser evidence.
- Historical validation must not commit raw log values or private local files.

## Validation Evidence Needed

Focused future validation should include:

```powershell
py -m pytest -q tests\test_app_extractors.py
py -m pytest -q tests\test_gre_game_state_parser.py
py -m pytest -q tests\test_runtime_surfaces.py
py -m pytest -q tests\test_saved_event_replay.py
py -m ruff check src tests
git diff --check
```

If a local report tool is added, also validate it in read-only mode against a
small sanitized fixture before running it against `data/match_logs/`.

## Open Questions

- Should life-total output live in a new `app/life_totals.py` module, or should
  it initially extend `runtime_surfaces.py`?
- Should life-total timelines be status-only JSON/Markdown first, or should
  they wait for the analytics storage layer?
- Should deltas be emitted only when both previous and current values are
  observed?
- Should local/opponent relation use `systemSeatIds[0]`, team mapping, or both?
- Should the module track starting life total changes as drift/conflict
  evidence?
- Should damage/life-change source attribution be a separate future module?

## Recommended Next Workflow Action

Next role: Codex B: Module Contract Writer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex B: Module Contract Writer for the life-total parser coverage
module suite.

Branch:
codex/life-total-parser-coverage

Source artifact:
docs/problem_representations/life_total_parser_coverage.md

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md
- docs/problem_representations/life_total_parser_coverage.md
- src/mythic_edge_parser/parsers/gre/game_state.py
- src/mythic_edge_parser/app/extractors.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/saved_event_replay.py
- tests/test_gre_game_state_parser.py
- tests/test_app_extractors.py
- tests/test_gameplay_actions.py
- tests/test_runtime_surfaces.py
- tests/test_saved_event_replay.py

Goal:
Produce docs/contracts/parser_life_totals.md for a first-class life-total
coverage module suite. Distinguish observed behavior, required guarantees,
unknowns, suspected gaps, validation evidence, protected surfaces, and
out-of-scope behavior changes.

The contract should define the smallest safe v1 design for extracting observed
life totals from GameState players, mapping them to match/game/seat/team/local
relation, deriving deltas only from observed consecutive values, and exposing
the data locally without changing workbook schema, webhook payload shape, Apps
Script behavior, parser state final reconciliation, match/game identity, or
production behavior.

Do not implement code.
Do not open a PR.
Do not commit raw logs, generated data, runtime status files, failed posts, or
workbook exports.
Do not target main.
```

```yaml
workflow_handoff:
  issue: "N/A - local problem representation branch"
  tracker: "future parser drift/evidence ledger or analytics foundation tracker"
  completed_thread: "A"
  next_thread: "B"
  source_artifact: "read-only historical replay quality report and code inspection"
  target_artifact: "docs/contracts/parser_life_totals.md"
  risk_tier: "Medium"
  branch: "codex/life-total-parser-coverage"
  validation:
    - "rg search found no first-class life-total module or tests"
    - "read-only local field-path scan found lifeTotal and startingLifeTotal in GameState player payloads"
  stop_conditions:
    - "Do not commit raw local logs or generated status artifacts."
    - "Do not change workbook schema, webhook payload shape, or Apps Script behavior."
    - "Do not change parser state final reconciliation, match identity, game identity, or production deduplication."
    - "Do not treat inferred damage source attribution as parser truth."
```
