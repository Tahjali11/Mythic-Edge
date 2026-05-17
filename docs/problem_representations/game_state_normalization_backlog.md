# GameState Normalization Backlog Problem Representation

## Summary

Mythic Edge currently preserves broad GRE `GameState` payload sections, but many
observed fields are not yet promoted into first-class parser-managed outputs.
Before the analytics suite begins, the project should run a dedicated
normalization workflow across every observed GameState data family so analytics
can consume stable parser-owned facts instead of raw nested payloads.

Plain English: keeping the raw `players`, `gameObjects`, `actions`,
`annotations`, and `timers` arrays is useful, but it is not the same thing as
normalizing them. A future analytics layer should not have to rediscover raw
Arena field meanings on its own.

## Source Request Or Issue

Source request: local Codex thread after historical replay inspection.

No GitHub issue was opened in this pass.

## Tracker

N/A.

Recommended future tracker:

- `[parser-foundation] GameState normalization coverage suite`

This tracker should sit before the analytics foundation suite.

## Definition Of First-Class Normalization

For this backlog, a GameState field is considered first-class normalized only
when the repo has a stable parser-owned interface for it, such as:

- a dedicated parser/extractor/runtime module
- a documented contract
- focused tests for the normalized shape
- an explicit output vocabulary
- source/confidence/finality metadata where needed
- a stable local artifact, row, state object, report, or analytics-ready table

A field is not considered first-class normalized merely because
`parsers/gre/game_state.py` copied it into `payload["players"]`,
`payload["game_objects"]`, `payload["actions"]`, or `payload["raw_game_state"]`.

## Evidence Inspected

Read-only local inspection used:

- `data/match_logs/`
- latest `_vN_` JSONL file per date folder
- 17 latest-per-day files
- 18,766 observed `GameState` records

No raw log values were committed or embedded in this artifact. The counts below
are shape evidence only.

Repo surfaces inspected:

- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/turn_info.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/transforms.py`
- existing parser, extractor, gameplay action, runtime surface, and snapshot
  tests

## What The Code Is Supposed To Do

The parser should eventually expose every useful observed `GameState` data
family as parser-managed, normalized evidence before downstream analytics rely
on it.

The desired end state:

- raw GameState evidence is preserved
- each observed payload family has a contract
- every normalized output has source/confidence/finality semantics where useful
- analytics reads stable parser-owned facts
- AI coaching reads analytics and parser facts, not raw GameState blobs
- workbook/webhook/App Script surfaces remain unchanged unless explicitly
  contracted later

## What It Is Actually Doing

Current code already does valuable partial normalization:

- `game_state.py` preserves top-level `GameState` identity, `game_info`,
  `turn_info`, `players`, `zones`, `game_objects`, `annotations`,
  `persistent_annotations`, `timers`, `actions`, diff ids, and raw message
  shape.
- `turn_info.py` normalizes turn number, phase, step, active player, decision
  player, priority player, next phase, and next step.
- `extractors.py` provides compatibility helpers for GameState identity,
  player/team/seat mapping, local private hand extraction, instance-to-grpId
  lookup, and result identity.
- `state.py` uses GameState and GameResult payloads to maintain match/game
  summaries.
- `gameplay_actions.py` derives selected card/action rows from zones,
  gameObjects, annotations, and actions.
- `runtime_surfaces.py` emits active timelines and match/deck/collection status
  surfaces.

But many observed GameState fields remain raw, partially used, or implicit.
They are not yet normalized as durable parser-managed outputs.

## Why This Matters

The analytics suite will be strongest if it depends on explicit parser-owned
facts instead of repeatedly walking raw Arena payloads.

If GameState data remains raw:

- analytics modules may duplicate fragile extraction logic
- different modules may interpret the same raw field differently
- drift detection cannot easily say which analytic outputs degraded
- AI coaching may receive incomplete or inconsistently labeled facts
- future refactors may miss high-value signals that were present all along

## Project Layer

Primary layer:

- parser and state interpretation

Supporting future layer:

- local analytics foundation

Truth boundaries:

- MTGA `Player.log` and saved parser JSONL are local observable evidence.
- Parser/state modules own normalized interpretation.
- The GameState normalization suite must not move truth ownership into
  workbook formulas, Apps Script, webhook transport, dashboards, Google
  Workspace, or AI output.
- First-class normalization may create new local parser artifacts, but workbook
  schema and webhook payloads require separate contracts.

## First Bad Value

The first bad value is a missing normalized output, not a corrupted raw value.

The raw `GameState` payload contains fields such as life totals, timers, combat
state, action costs, annotation details, persistent annotations, object status,
and diff mechanics. Current parser modules preserve much of that raw data, but
only selected parts are promoted into stable outputs.

## Observed GameState Field Inventory

Counts are per latest-per-day local saved JSONL corpus.

### Top-Level `gameStateMessage`

| Field | Records | Current status |
| --- | ---: | --- |
| `type` | 18,766 | Preserved; not a dedicated analytics output. |
| `gameStateId` | 18,766 | Partially normalized as `game_state_id`; used in action entries. |
| `prevGameStateId` | 18,766 | Preserved; no first-class diff-chain module. |
| `update` | 18,766 | Preserved; no update-type module. |
| `actions` | 18,753 | Partially used by gameplay actions; full action details not normalized. |
| `annotations` | 18,179 | Partially used; full annotation taxonomy not normalized. |
| `turnInfo` | 17,882 | Normalized into `turn_info`; only partial first-class outputs. |
| `timers` | 10,767 | Preserved; no timer/clock module. |
| `zones` | 4,801 | Partially used by gameplay actions; no zone snapshot module. |
| `gameObjects` | 4,793 | Partially used by gameplay/card identity; no complete object-state module. |
| `players` | 3,457 | Partially used for team/seat/mulligan; no full player-state module. |
| `persistentAnnotations` | 3,065 | Preserved; no persistent-effect module. |
| `diffDeletedPersistentAnnotationIds` | 2,711 | Preserved; no persistent-annotation diff module. |
| `pendingMessageCount` | 2,585 | Preserved; no queue/backlog module. |
| `diffDeletedInstanceIds` | 2,065 | Preserved; no object-delete/diff module. |
| `gameInfo` | 831 | Partially used for identity/result/context; not fully normalized. |
| `teams` | 376 | Preserved; no dedicated team-state module. |

### `gameInfo`

| Field | Records | Current status |
| --- | ---: | --- |
| `matchID` | 831 | Used for match identity. |
| `gameNumber` | 831 | Used for game identity. |
| `stage` | 831 | Used for stage/game-over logic. |
| `type` | 831 | Preserved; not first-class. |
| `variant` | 831 | Preserved; no variant module. |
| `matchState` | 831 | Preserved/partially surfaced; no state-transition module. |
| `matchWinCondition` | 831 | Partially useful for Bo1/Bo3 classification; no complete context module. |
| `maxTimeoutCount` | 831 | Preserved; no timer policy module. |
| `maxPipCount` | 831 | Preserved; no pip policy module. |
| `timeoutDurationSec` | 831 | Preserved; no timer policy module. |
| `superFormat` | 831 | Partially used for format context. |
| `deckConstraintInfo` | 831 | Preserved; no deck-constraint module. |
| `mulliganType` | 828 | Preserved; no mulligan-rule context module. |
| `results` | 671 | Used for result extraction; full provenance/shape not isolated. |
| `sideboardLoadingEnabled` | 15 | Preserved; no sideboarding-capability module. |

`gameInfo.results[]` observed fields:

- `scope`
- `result`
- `reason`
- `winningTeamId`

`deckConstraintInfo` observed fields:

- `minDeckSize`
- `maxDeckSize`
- `maxSideboardSize`

### `teams[]`

Observed fields:

- `id`
- `playerIds`
- `status`

Current status:

- Preserved in raw GameState shape.
- Not normalized into a first-class team-state surface.

### `turnInfo`

| Field | Records | Current status |
| --- | ---: | --- |
| `turnNumber` | 17,790 | Normalized and used for game rows/action rows. |
| `activePlayer` | 17,882 | Normalized as active player seat. |
| `phase` | 17,790 | Normalized and used in timelines. |
| `step` | 13,757 | Normalized and used in timelines. |
| `priorityPlayer` | 17,789 | Normalized in payload but no priority timeline module. |
| `decisionPlayer` | 14,057 | Normalized in payload but no decision-pressure module. |
| `nextPhase` | 17,774 | Normalized in payload but no progression module. |
| `nextStep` | 13,541 | Normalized in payload but no progression module. |

### `players[]`

| Field | Records | Current status |
| --- | ---: | --- |
| `systemSeatNumber` | 5,991 | Used for mapping. |
| `teamId` | 5,991 | Used for mapping/result interpretation. |
| `status` | 5,991 | Preserved; no player-status module. |
| `maxHandSize` | 5,991 | Preserved; no hand-size rule module. |
| `timerIds` | 5,991 | Preserved; no player-timer join module. |
| `controllerSeatId` | 5,991 | Preserved; no controller mapping module. |
| `controllerType` | 5,991 | Preserved; no controller-type module. |
| `startingLifeTotal` | 5,991 | Preserved; no life-total module. |
| `lifeTotal` | 5,972 | Preserved; no life-total timeline/delta module. |
| `turnNumber` | 5,602 | Preserved; no player-turn-state module. |
| `timeoutCount` | 3,322 | Preserved; no timeout-pressure module. |
| `pipCount` | 3,142 | Preserved; no pip module. |
| `mulliganCount` | 1,178 | Partially used for local summaries; no full per-player timeline. |
| `pendingMessageType` | 221 | Preserved; no pending-decision module. |
| `manaPool` | 10 | Preserved; no mana-pool module. |

`manaPool[]` observed fields:

- `manaId`
- `color`
- `srcInstanceId`
- `abilityGrpId`
- `count`
- `specs`

### `zones[]`

Observed fields:

- `zoneId`
- `type`
- `visibility`
- `objectInstanceIds`
- `ownerSeatId`
- `viewers`

Current status:

- Partially used for private-hand extraction and gameplay action zone
  transitions.
- Not normalized as stable zone snapshots, zone membership history, or
  visibility/accessibility evidence.

### `gameObjects[]`

Observed identity and card fields:

- `instanceId`
- `grpId`
- `overlayGrpId`
- `objectSourceGrpId`
- `parentId`
- `othersideGrpId`
- `type`
- `name`
- `cardTypes`
- `superTypes`
- `subtypes`
- `color`
- `skinCode`
- `baseSkinCode`
- `viewers`
- `visibility`
- `ownerSeatId`
- `controllerSeatId`
- `zoneId`
- `isCopy`

Observed characteristics and status fields:

- `power.value`
- `toughness.value`
- `damage`
- `loyalty`
- `loyaltyUsed`
- `isTapped`
- `hasSummoningSickness`
- `uniqueAbilities`
- `abilityOriginalCardGrpIds`

Observed combat fields:

- `attackState`
- `attackInfo.targetId`
- `attackInfo.damageAssigned`
- `attackInfo.orderedBlockers`
- `blockState`
- `blockInfo.attackerIds`
- `blockInfo.damageAssigned`
- `blockInfo.orderedAttackers`

Current status:

- Partially normalized by gameplay action/card identity code.
- Not normalized into a complete object snapshot, permanent state, combat
  state, ability state, or board-state timeline.

### `actions[]`

Outer observed fields:

- `seatId`
- `action`

Inner observed fields:

- `actionType`
- `instanceId`
- `abilityGrpId`
- `manaCost`
- `sourceId`
- `alternativeGrpId`
- `alternativeSourceZcid`

`manaCost[]` observed fields:

- `color`
- `count`
- `abilityGrpId`

Current status:

- `actionType` and `instanceId` are partially used by gameplay actions.
- Ability ids, alternative choices, source ids, and mana costs are not
  first-class normalized.

### `annotations[]`

Observed fields:

- `id`
- `affectedIds`
- `type`
- `details`
- `affectorId`

`details[]` observed fields:

- `key`
- `type`
- `valueInt32`
- `valueString`

Current status:

- Selected annotations are used for zone transfers, object replacement, and
  resolution hints.
- Full annotation taxonomy, affector links, typed detail rows, and
  annotation-to-object/action joins are not normalized.

### `persistentAnnotations[]`

Observed fields:

- `id`
- `affectedIds`
- `type`
- `details`
- `affectorId`

`details[]` observed fields:

- `key`
- `type`
- `valueInt32`
- `valueString`

Current status:

- Preserved in the GameState payload.
- No first-class persistent-effect or continuous-state module exists.

### `timers[]`

Observed fields:

- `timerId`
- `type`
- `durationSec`
- `behavior`
- `warningThresholdSec`
- `elapsedMs`
- `elapsedSec`
- `running`

Current status:

- Preserved in the GameState payload.
- No first-class timer/clock/rope/priority-pressure module exists.

## Required Normalization Backlog

This is the comprehensive queue of GameState payload families that do not yet
have complete first-class normalized outputs.

### 0. GameState Coverage Matrix And Contract Harness

Purpose:

- create the master contract/testing pattern for this suite
- define what “fully normalized” means for GameState payload data
- prevent analytics from starting before the suite coverage status is explicit

Input fields:

- all observed GameState sections and keys listed above

Expected output:

- `docs/contracts/parser_game_state_normalization_coverage.md`
- a machine-readable coverage matrix, if approved by contract
- report-only validation that says each observed GameState field is
  normalized, intentionally raw-only, or explicitly out of scope

Why first:

- without this, each child module can accidentally define “normalized”
  differently

### 1. GameState Envelope, Diff, And Update Mechanics

Input fields:

- `type`
- `gameStateId`
- `prevGameStateId`
- `update`
- `pendingMessageCount`
- `diffDeletedInstanceIds`
- `diffDeletedPersistentAnnotationIds`

Expected first-class outputs:

- game-state envelope records
- diff-chain continuity checks
- deleted object and deleted persistent-annotation evidence
- pending-message/backlog evidence
- update-type vocabulary

Risk tier: Medium.

Protected surfaces:

- parser state final reconciliation
- deduplication
- runtime status files

### 2. GameInfo Rules, Result Context, And Deck Constraints

Input fields:

- `matchID`
- `gameNumber`
- `stage`
- `type`
- `variant`
- `matchState`
- `matchWinCondition`
- `superFormat`
- `mulliganType`
- `sideboardLoadingEnabled`
- `maxTimeoutCount`
- `maxPipCount`
- `timeoutDurationSec`
- `deckConstraintInfo.minDeckSize`
- `deckConstraintInfo.maxDeckSize`
- `deckConstraintInfo.maxSideboardSize`
- `results[].scope`
- `results[].result`
- `results[].reason`
- `results[].winningTeamId`

Expected first-class outputs:

- game rules/context snapshot
- match/game result provenance from GameState `gameInfo`
- deck constraint context
- sideboarding-capability evidence
- timeout/pip policy context
- mulligan-rule context

Risk tier: High if result interpretation changes; Medium if report-only.

Protected surfaces:

- match identity
- game identity
- winner fields
- final reconciliation

### 3. Team State

Input fields:

- `teams[].id`
- `teams[].playerIds`
- `teams[].status`

Expected first-class outputs:

- team-state snapshots
- team status history
- team/player join evidence
- conflict checks against `players[].teamId`

Risk tier: Medium.

Protected surfaces:

- player/team mapping
- winner interpretation

### 4. Turn, Priority, Decision, And Phase Progression

Input fields:

- `turnNumber`
- `activePlayer`
- `priorityPlayer`
- `decisionPlayer`
- `phase`
- `step`
- `nextPhase`
- `nextStep`

Expected first-class outputs:

- turn/phase timeline
- priority-player timeline
- decision-player timeline
- phase/step transition records
- active-player progression checks

Current partial support:

- `turn_info.py` already normalizes these into `turn_info`
- runtime surfaces only expose a subset

Risk tier: Medium.

Protected surfaces:

- turn count
- play/draw interpretation
- future action timing analytics

### 5. Player State, Life Totals, And Per-Seat Counters

Input fields:

- `systemSeatNumber`
- `teamId`
- `status`
- `maxHandSize`
- `timerIds`
- `controllerSeatId`
- `controllerType`
- `startingLifeTotal`
- `lifeTotal`
- `turnNumber`
- `timeoutCount`
- `pipCount`
- `mulliganCount`
- `pendingMessageType`

Expected first-class outputs:

- per-seat player-state snapshots
- life-total timeline
- observed life-total deltas
- max-hand-size evidence
- per-player mulligan count timeline
- timeout/pip count timeline
- pending-message evidence
- local/opponent relation metadata

Current partial support:

- team/seat mapping is used
- local mulligan summaries exist
- life totals are preserved but not normalized

Risk tier: Medium, High if it changes existing mulligan/play-draw behavior.

Protected surfaces:

- mulligan counts
- player/team mapping
- parser state final reconciliation

### 6. Player Mana Pool

Input fields:

- `manaPool[].manaId`
- `manaPool[].color`
- `manaPool[].srcInstanceId`
- `manaPool[].abilityGrpId`
- `manaPool[].count`
- `manaPool[].specs`

Expected first-class outputs:

- observed mana-pool snapshots
- mana source links
- mana color/count state
- clear low-confidence handling because observed sample count is small

Risk tier: Medium.

Protected surfaces:

- gameplay action interpretation
- future mana-efficiency analytics

### 7. Timer And Clock Pressure

Input fields:

- `timerId`
- `type`
- `durationSec`
- `behavior`
- `warningThresholdSec`
- `elapsedMs`
- `elapsedSec`
- `running`

Expected first-class outputs:

- timer snapshot records
- timer-to-player joins through `players[].timerIds`
- rope/clock pressure timeline
- timeout-risk events
- parser confidence labels for missing joins

Risk tier: Medium.

Protected surfaces:

- runtime status artifacts
- player-state joins

### 8. Zone Snapshot And Visibility State

Input fields:

- `zoneId`
- `type`
- `visibility`
- `objectInstanceIds`
- `ownerSeatId`
- `viewers`

Expected first-class outputs:

- zone snapshots
- zone membership history
- visibility/accessibility labels
- owner/viewer evidence
- private/public/hidden information boundaries

Current partial support:

- private hand extraction
- zone transition action inference

Risk tier: Medium to High, depending on hidden-information policy.

Protected surfaces:

- opening hand
- gameplay action inference
- opponent/private information boundaries

### 9. Game Object Identity And Card Snapshot State

Input fields:

- `instanceId`
- `grpId`
- `overlayGrpId`
- `objectSourceGrpId`
- `parentId`
- `othersideGrpId`
- `type`
- `name`
- `cardTypes`
- `superTypes`
- `subtypes`
- `color`
- `skinCode`
- `baseSkinCode`
- `viewers`
- `visibility`
- `ownerSeatId`
- `controllerSeatId`
- `zoneId`
- `isCopy`

Expected first-class outputs:

- object snapshot records
- instance-to-card identity evidence
- canonical grpId candidate chain
- owner/controller relation
- zone/object join
- visibility/viewer labels
- card face/alternate side identity evidence
- copy/token-like evidence when available

Current partial support:

- gameplay actions normalize selected identity fields
- card catalog and grpId tooling use some observations

Risk tier: High.

Protected surfaces:

- card identity
- hidden information
- gameplay actions
- card performance

### 10. Permanent Characteristics, Damage, Loyalty, And Ability State

Input fields:

- `power.value`
- `toughness.value`
- `damage`
- `loyalty`
- `loyaltyUsed`
- `isTapped`
- `hasSummoningSickness`
- `uniqueAbilities`
- `abilityOriginalCardGrpIds`

Expected first-class outputs:

- object characteristic snapshots
- tapped/untapped state
- summoning-sickness state
- damage-marked state
- loyalty state
- ability presence/origin evidence
- derived characteristic deltas only when consecutive observed values support
  them

Risk tier: High.

Protected surfaces:

- board-state interpretation
- combat analytics
- card performance analytics

### 11. Combat State

Input fields:

- `attackState`
- `attackInfo.targetId`
- `attackInfo.damageAssigned`
- `attackInfo.orderedBlockers`
- `blockState`
- `blockInfo.attackerIds`
- `blockInfo.damageAssigned`
- `blockInfo.orderedAttackers`

Expected first-class outputs:

- attackers
- blockers
- attack targets
- assigned damage
- combat pairings
- combat state transitions
- combat confidence labels where data is partial

Risk tier: High.

Protected surfaces:

- gameplay action interpretation
- damage/life-total analytics
- source attribution boundaries

### 12. Raw Action Detail, Ability, Cost, And Source State

Input fields:

- `actions[].seatId`
- `actions[].action.actionType`
- `actions[].action.instanceId`
- `actions[].action.abilityGrpId`
- `actions[].action.manaCost[].color`
- `actions[].action.manaCost[].count`
- `actions[].action.manaCost[].abilityGrpId`
- `actions[].action.sourceId`
- `actions[].action.alternativeGrpId`
- `actions[].action.alternativeSourceZcid`

Expected first-class outputs:

- action intent records
- ability id records
- mana-cost records
- source/alternative action links
- action-to-object joins
- action-to-seat/team/local relation

Current partial support:

- gameplay actions use `actionType` and `instanceId`

Risk tier: High.

Protected surfaces:

- gameplay actions
- card performance
- future tactical analytics

### 13. Annotation Taxonomy And Detail Records

Input fields:

- `annotations[].id`
- `annotations[].affectedIds`
- `annotations[].type`
- `annotations[].affectorId`
- `annotations[].details[].key`
- `annotations[].details[].type`
- `annotations[].details[].valueInt32`
- `annotations[].details[].valueString`

Expected first-class outputs:

- annotation event records
- annotation type vocabulary
- typed detail records
- affector/affected joins
- object/action annotation links
- explicit allowlist of annotations used for derived facts

Current partial support:

- selected annotation categories are used for zone transfer, object id changes,
  and resolution hints

Risk tier: High.

Protected surfaces:

- gameplay actions
- object identity replacement
- zone transitions
- future rules/invariant checks

### 14. Persistent Annotation And Continuous Effect State

Input fields:

- `persistentAnnotations[].id`
- `persistentAnnotations[].affectedIds`
- `persistentAnnotations[].type`
- `persistentAnnotations[].affectorId`
- `persistentAnnotations[].details[].key`
- `persistentAnnotations[].details[].type`
- `persistentAnnotations[].details[].valueInt32`
- `persistentAnnotations[].details[].valueString`
- `diffDeletedPersistentAnnotationIds`

Expected first-class outputs:

- persistent annotation snapshots
- persistent effect lifecycle records
- created/updated/deleted persistent annotation events
- affected object/player links
- explicit separation from one-shot annotations

Risk tier: High.

Protected surfaces:

- board-state interpretation
- object characteristic interpretation
- future combat/effect analytics

### 15. Historical GameState Normalization Quality Report

Purpose:

- run read-only checks across saved JSONL
- prove which GameState families are covered after each module lands
- report observed/missing/malformed/unsupported field coverage
- remain local/generated unless sanitized and approved

Input fields:

- all observed GameState fields

Expected first-class outputs:

- local report under ignored `data/status/`
- optional committed sanitized fixture report later
- coverage status by module family

Risk tier: Medium.

Protected surfaces:

- raw logs
- generated status files
- fixture policy

## Recommended Workflow Queue

Recommended order before analytics:

1. GameState coverage matrix and contract harness.
2. GameState envelope/diff/update mechanics.
3. GameInfo rules/result context/deck constraints.
4. Team state.
5. Turn, priority, decision, and phase progression.
6. Player state, life totals, and per-seat counters.
7. Timer and clock pressure.
8. Zone snapshot and visibility state.
9. Game object identity and card snapshot state.
10. Permanent characteristics, damage, loyalty, and ability state.
11. Combat state.
12. Raw action detail, ability, cost, and source state.
13. Annotation taxonomy and detail records.
14. Persistent annotation and continuous effect state.
15. Player mana pool.
16. Historical GameState normalization quality report.

Rationale:

- Start with the coverage matrix so the suite has one definition of
  completion.
- Normalize identity/context before stateful per-seat/per-object facts.
- Normalize zones and objects before combat/actions/annotations because those
  later modules depend on stable object and zone joins.
- Keep the rare mana-pool surface after broader player/action modules unless a
  current analytics need raises its priority.

## Scope

In scope:

- every observed GameState payload field family in the local latest-per-day
  saved JSONL corpus
- first-class parser-owned normalization design
- module-by-module workflow routing
- local read-only validation reports
- source/confidence/finality metadata expectations

Out of scope for this problem-representation pass:

- implementing any parser module
- changing parser behavior
- changing parser event classes
- changing parser state final reconciliation
- changing workbook schema
- changing webhook payload shape
- changing Apps Script behavior
- committing raw local logs
- committing generated `data/status/` reports
- starting analytics implementation
- claiming this list covers future MTGA fields not present in the current
  local corpus

## Risks And Likely Breakpoints

- Some fields are sparse and should not be overfit from low counts.
- Some values may be present only in full GameState snapshots, not diffs.
- Some fields are stable raw evidence but hard to interpret safely.
- Zone/object/action/annotation modules are tightly coupled and need strict
  contracts to avoid inconsistent joins.
- Hidden/private information boundaries matter; normalization must not infer
  unavailable opponent information.
- Damage and combat attribution are high-risk because life changes, damage
  markings, combat assignment, and card/action causes are related but not
  identical facts.
- Workbook/webhook schema should not expand until the local parser-owned
  surfaces are stable.
- Analytics should remain blocked until the coverage matrix says which
  GameState families are normalized and which are intentionally excluded.

## Validation Evidence Needed

For this docs-only problem representation:

```powershell
git diff --check
```

For future module contracts and implementations, likely focused checks:

```powershell
py -m pytest -q tests\test_gre_game_state_parser.py
py -m pytest -q tests\test_app_extractors.py
py -m pytest -q tests\test_gameplay_actions.py
py -m pytest -q tests\test_runtime_surfaces.py
py -m pytest -q tests\test_saved_event_replay.py
py -m ruff check src tests
git diff --check
```

Future report validation should also include a read-only local run over
`data/match_logs/` that writes only ignored `data/status/` artifacts.

## Open Questions

- Should each queue item get its own GitHub child issue, or should small
  tightly coupled pairs be grouped?
- Should the GameState coverage matrix be Markdown-only, YAML/JSON, or
  Python-owned structured data with generated docs?
- Which normalized surfaces should be local JSON only versus future workbook
  rows?
- Should object, action, and annotation modules share one common normalized
  event id/key scheme?
- How strict should analytics gating be: block analytics entirely until every
  family is normalized, or allow analytics over explicitly completed families?
- Should rare surfaces like player `manaPool` be implemented now for
  completeness or registered as intentionally low-priority but still covered?

## Next Workflow Action

Next role: Codex B: Module Contract Writer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex B: Module Contract Writer for the GameState normalization coverage
suite.

Branch:
codex/game-state-normalization-backlog

Source artifact:
docs/problem_representations/game_state_normalization_backlog.md

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md
- docs/problem_representations/game_state_normalization_backlog.md
- src/mythic_edge_parser/parsers/gre/game_state.py
- src/mythic_edge_parser/parsers/gre/turn_info.py
- src/mythic_edge_parser/app/extractors.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/transforms.py
- docs/problem_representations/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger.md if present on this branch
- existing parser event schema snapshots and GameState-related tests

Goal:
Produce docs/contracts/parser_game_state_normalization_coverage.md.

The contract should define:
- what counts as first-class GameState normalization
- the required coverage matrix format
- the observed GameState field families that must be tracked
- how each field family is classified: already normalized, partially normalized,
  requires module, intentionally raw-only, or out of scope
- how child issues should be generated for each required module family
- protected surfaces
- validation evidence needed before analytics can rely on each family
- stop conditions for workbook/webhook/App Script/parser-state-finality changes

Do not implement code.
Do not change parser behavior.
Do not create raw fixtures.
Do not commit raw logs, generated data, runtime status files, failed posts, or
workbook exports.
Do not open a PR unless explicitly asked.
Do not target main.
```

```yaml
workflow_handoff:
  issue: "N/A - local planning branch"
  tracker: "recommended future tracker: [parser-foundation] GameState normalization coverage suite"
  completed_thread: "A"
  next_thread: "B"
  source_artifact: "read-only latest-per-day local GameState field inventory"
  target_artifact: "docs/contracts/parser_game_state_normalization_coverage.md"
  risk_tier: "High"
  branch: "codex/game-state-normalization-backlog"
  validation:
    - "read-only local shape inventory over 17 latest-per-day files and 18,766 GameState records"
    - "git diff --check"
  stop_conditions:
    - "Do not implement parser behavior from the planning thread."
    - "Do not change parser state final reconciliation, parser event classes, match identity, game identity, workbook schema, webhook payload shape, Apps Script behavior, or production behavior."
    - "Do not commit raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not begin analytics implementation until the coverage contract defines the gating policy."
```
