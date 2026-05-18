# Parser Timer Normalization Contract

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/115

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/113

Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/114

Previous merge commit: `bbcd61656f2af7981936e415e6d1431f5889f012`

Branch target: `codex/parser-reliability-intelligence`

This contract defines first-class GRE GameState timer normalization for Mythic
Edge. It is a contract artifact only. It does not implement code, change parser
behavior, change workbook schema, change webhook payloads, change Apps Script,
build clock-pressure analytics, infer player mistakes, or commit raw private
`Player.log` excerpts.

## Module

Parser GRE timer normalization.

Plain English: this module turns raw GRE `GameStateMessage` timer arrays into a
stable, deterministic, parser-owned timer evidence view. It must preserve raw
timer arrays exactly as current GameState payload evidence while giving
parser-adjacent consumers one shared way to read timer IDs, names/types, direct
seat/player fields, scalar values, time-unit evidence, and malformed-input
degradation.

Risk tier: High.

The risk is high because timer evidence can easily drift from parser facts into
analytics conclusions such as clock pressure, rope usage, or mistakes. This
module may normalize timer evidence, but it must not decide why a timer changed
or whether a player played well.

## Owning Layer

Owning layer: parser and state interpretation, specifically GRE GameState
normalization support.

Truth boundary:

- MTGA `Player.log` timer arrays are local observable evidence, not absolute
  game truth.
- `src/mythic_edge_parser/parsers/gre/game_state.py` continues to own raw
  GameState payload construction and must continue preserving raw `timers`.
- The timer normalization module owns normalized timer evidence records and
  timer-derived helper summaries.
- This module does not own match identity, game identity, final reconciliation,
  deduplication, parser event class schema, workbook rows, webhook delivery,
  Apps Script behavior, output transport, clock-pressure conclusions, player
  coaching, player-mistake labels, archetype classification, decklist
  completion, or hidden-information inference.
- `turn_info.py`, annotation normalization, diagnostics mode, golden replay,
  the evidence ledger, workbook sheets, dashboards, Apps Script, output
  transport, analytics modules, and AI/model output are consumers unless a
  later contract explicitly changes ownership.

Parser truth must stay parser-owned. Workbook formulas, dashboard logic,
webhook transport, Apps Script, analytics surfaces, and AI output must not
become the source of truth for timer interpretation.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_timer_normalization.md`

Future implementation artifacts owned by this contract, if authorized by the
Codex C implementation pass:

- `src/mythic_edge_parser/parsers/gre/timers.py`
- `tests/test_gre_timers_parser.py`
- `docs/implementation_handoffs/parser_timer_normalization_comparison.md`

Narrow integration surfaces allowed only when needed to satisfy this contract:

- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_game_state_parser.py`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `tests/test_parser_diagnostics_mode.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `tests/test_golden_replay_harness.py`
- optional committed sanitized or synthetic fixture/manifest files under
  existing fixture locations, only if required by implementation tests

Referenced but not silently owned:

- `src/mythic_edge_parser/parsers/gre/turn_info.py`
- `tests/test_gre_turn_info_parser.py`
- `src/mythic_edge_parser/parsers/gre/annotations.py`
- `tests/test_gre_annotations_parser.py`
- `src/mythic_edge_parser/parsers/api_common.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/card_performance.py`
- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/parser_gre_turn_info.md`
- `docs/contracts/parser_annotation_normalization.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/problem_representations/parser_feature_equity_with_manasight.md`

## Observed Current Behavior

Observed on `codex/parser-reliability-intelligence` after PR #114:

- Issue #115 is open and belongs to tracker #47.
- Tracker #47 remains open.
- Related evidence issue #11 remains open.
- PR #114 is merged into `codex/parser-reliability-intelligence` at
  `bbcd61656f2af7981936e415e6d1431f5889f012`.
- `game_state.py` shallow-copies raw `gsm.timers` to `payload["timers"]`;
  non-list timer sections become `[]`.
- Focused GameState parser tests protect raw timer preservation and
  malformed-section fallback behavior.
- `parser_gre_game_state.md` documents `timers` as a shallow list copy only.
- `game_state.py` now imports `normalize_annotation_arrays()` and adds
  additive `payload["normalized_annotations"]`, giving timer normalization a
  local pattern to follow.
- `parser_annotation_normalization.md` explicitly keeps timer normalization as
  a separate backlog module.
- `parser_feature_equity_with_manasight.md` identifies GRE timer normalization
  as partial coverage: raw preservation exists, but first-class timer facts do
  not.
- No dedicated `src/mythic_edge_parser/parsers/gre/timers.py` module exists
  yet.

## Required Guarantees

### Raw Evidence Preservation

- Raw `payload["timers"]` must remain present and unchanged in meaning.
- Raw timer list preservation remains shallow-copy behavior unless a later
  GameState payload contract explicitly changes it.
- Normalized timer records must not replace, delete, reorder, or mutate raw
  timer dictionaries.
- Normalized timer records should not duplicate the full raw timer dictionary
  by default. Raw evidence remains available in the preserved raw `timers`
  array and preserved `raw_game_state`.

### First-Class Normalized View

V1 should expose timer normalization through a parser-side helper module and
add an additive `GameStateEvent.payload["normalized_timers"]` field.

The additive GameState payload field is authorized by this contract because it
is parser-owned timer evidence. It must remain local parser payload data and
must not imply a workbook schema, webhook payload, Apps Script, runtime status
schema, local status artifact, or AI-facing output change.

Because parser payload keys are snapshot-protected, Codex C must update
`tests/fixtures/schema_snapshots/parser_payload_keys.json` only for the
additive `normalized_timers` key and only under this issue/contract. Any
broader snapshot, workbook, webhook, Apps Script, or runtime artifact change is
out of scope and must stop for loopback.

## Public API

Exact Python names may vary during implementation, but the public behavior must
preserve this shape:

```python
TIMER_RECORD_OBJECT = "mythic_edge_gre_timer"
TIMER_COLLECTION_OBJECT = "mythic_edge_gre_timers"
SCHEMA_VERSION = "parser_gre_timers.v1"

def normalize_timer_record(
    raw_timer: object,
    *,
    source_index: int,
) -> dict[str, object]:
    ...

def normalize_timer_array(
    timers: object,
    *,
    turn_info: Mapping[str, object] | None = None,
) -> dict[str, object]:
    ...

def timer_records_by_direct_seat(
    normalized_timers: Mapping[str, object],
) -> dict[int, list[dict[str, object]]]:
    ...
```

Required API behavior:

- Return JSON-serializable dictionaries and lists.
- Preserve input objects without mutation.
- Avoid filesystem writes.
- Avoid importing workbook, webhook, Apps Script, output transport, OpenAI, or
  model-provider surfaces.
- Never raise for malformed timer input in normal parser use. Malformed values
  must become empty normalized fields plus degradation flags.
- Use deterministic ordering based on source array order and source index.
- Treat helper functions as parser-owned evidence helpers, not analytics APIs.

## Normalized Payload Shape

### Collection Payload

Required logical shape for `payload["normalized_timers"]`:

```yaml
object: "mythic_edge_gre_timers"
schema_version: "parser_gre_timers.v1"
total_records: 2
degraded_records: 0
review_required: false
source_array: "timers"
timer_ids: [9]
timer_types: ["TimerType_GameClock"]
direct_seat_ids: [1]
time_units_seen:
  seconds: 1
  milliseconds: 1
  unknown: 0
contextual_turn_info:
  turn_number: 3
  active_player_seat_id: 1
  decision_player_seat_id: ""
  priority_player_seat_id: 2
degradation_flags: []
records:
  - normalized_timer_record
```

Collection field rules:

- `total_records` counts normalized records from the raw timer array.
- `degraded_records` counts records with nonempty `degradation_flags` or
  `evidence_status` of `degraded`, `unknown`, or `conflict`.
- `review_required` is true when any record or collection-level input requires
  review.
- `timer_ids` is an ordered, de-duplicated union of nonempty record
  `timer_id` values.
- `timer_types` is an ordered, de-duplicated union of nonempty record
  `timer_type` values.
- `direct_seat_ids` is an ordered, de-duplicated union of seat IDs found
  directly on timer records. It must not include contextual turn-info seats
  unless the timer itself names them.
- `time_units_seen` counts normalized time field values by unit label:
  `seconds`, `milliseconds`, and `unknown`.
- `contextual_turn_info` may carry selected `turn_info` values for local
  reporting context only. It must not assign timer ownership.

### Record Payload

Required logical shape:

```yaml
object: "mythic_edge_gre_timer"
schema_version: "parser_gre_timers.v1"
source_array: "timers"
source_index: 0
timer_id: 9
timer_type: "TimerType_GameClock"
timer_name: "GameClock"
timer_state: "running"
seat_fields:
  owner_seat_id: ""
  controller_seat_id: ""
  player_seat_id: 1
  system_seat_id: ""
  team_id: ""
  player_id: ""
direct_seat_ids: [1]
numeric_fields:
  - key: "durationMs"
    normalized_key: "duration_ms"
    value: 30000
    unit: "milliseconds"
    seconds_value: 30.0
    value_source: "observed"
string_fields:
  - key: "timerType"
    normalized_key: "timer_type"
    value: "TimerType_GameClock"
boolean_fields:
  - key: "running"
    normalized_key: "running"
    value: true
time_values:
  seconds:
    - key: "remainingSeconds"
      value: 20
  milliseconds:
    - key: "durationMs"
      value: 30000
      seconds_value: 30.0
  unknown_unit: []
unsupported_field_names: []
source_evidence: "timer"
evidence_status: "observed"
value_source: "observed"
confidence: "high"
degradation_flags: []
review_required: false
```

Required record fields:

- `object`
- `schema_version`
- `source_array`
- `source_index`
- `timer_id`
- `timer_type`
- `timer_name`
- `timer_state`
- `seat_fields`
- `direct_seat_ids`
- `numeric_fields`
- `string_fields`
- `boolean_fields`
- `time_values`
- `unsupported_field_names`
- `source_evidence`
- `evidence_status`
- `value_source`
- `confidence`
- `degradation_flags`
- `review_required`

Empty numeric or identifier values in JSON-facing payloads should use `""` for
compatibility with existing parser-adjacent payload style unless the field is
explicitly a list. Lists must use `[]`.

## Allowed Inputs

Allowed raw inputs:

- `GameStateMessage.timers`
- normalized GameState payload `timers`
- normalized GameState payload `turn_info` for optional context only
- raw timer dictionaries reachable through preserved `raw_game_state` fallback
  paths only when current extractor behavior already uses those fallback paths

Forbidden inputs:

- workbook formulas
- dashboard output
- Apps Script behavior
- webhook delivery state
- output transport state
- AI/model-provider output
- analytics or coaching output
- opponent archetype labels
- inferred or completed decklists
- hidden opponent hand/library/deck contents
- raw private logs committed to the repo
- generated runtime artifacts or failed-post artifacts

## Input Normalization Rules

### Source Array

- `timers` is accepted only when the source value is a list.
- Missing or `None` timers normalize to zero records without degradation.
- Present non-list `timers` normalize to zero records and produce collection
  degradation flag `malformed_timers_section`.
- Non-dict list entries must produce degraded placeholder records rather than
  being silently treated as timer evidence.
- Placeholder records must preserve `source_array`, `source_index`, empty
  normalized semantic fields, and `malformed_timer_record`.

### Timer IDs

- Raw `timerId`, `timer_id`, `id`, and `timerID` are accepted in that order.
- Timer ID normalization must match `api_common.normalize_int_list()` scalar
  behavior: booleans are skipped, integers are accepted, strings are stripped
  and accepted only when `.isdigit()` is true, and floats, negative-number
  strings, nested lists, dicts, empty strings, and `None` are skipped.
- Missing IDs produce `timer_id: ""` and are not degraded by themselves because
  not all timer shapes are known to include a stable ID.
- Present but malformed IDs produce `malformed_timer_id`.

### String Fields

Recognized string fields:

- `type`
- `timerType`
- `timer_type`
- `timerName`
- `timer_name`
- `name`
- `state`
- `timerState`
- `timer_state`
- `phase`
- `step`

Rules:

- String field values must be strings to participate as trusted string
  evidence.
- Values are stripped.
- Empty strings are ignored.
- Non-string values for recognized string fields produce
  `malformed_timer_string_field`.
- `timer_type` is selected from `timerType`, `timer_type`, then `type`.
- `timer_name` is selected from `timerName`, `timer_name`, then `name`.
- `timer_state` is selected from `timerState`, `timer_state`, then `state`.
- Unknown scalar string fields may be included in `string_fields`, but must not
  become semantic timer type/name/state fields without a later contract.

### Boolean Fields

Rules:

- Boolean fields preserve only actual booleans.
- Strings such as `"true"` and `"false"` are not booleans in v1.
- Numeric `0` and `1` are not booleans in v1.
- Recognized boolean-like field names with non-boolean values produce
  `malformed_timer_boolean_field`.
- Booleans must not be accepted as numeric timer values or identifier values.

Recognized boolean-like field names include names beginning with `is` or `has`
and common state fields such as `running`, `paused`, `expired`, `enabled`, and
`active`.

### Numeric Fields

Timer numeric values use two policies:

1. Identifier and seat/player/team fields use integer ID normalization.
2. Time/count fields use numeric value normalization.

Identifier and seat/player/team fields:

- follow the same scalar behavior as timer IDs;
- reject booleans and floats;
- reject negative-number strings;
- use `""` when missing or malformed.

Time/count fields:

- accept integers except booleans;
- accept finite floats;
- accept stripped numeric strings for integer or decimal values;
- may accept signed numeric strings, but negative values must add
  `negative_timer_value`;
- reject booleans, non-finite floats, empty strings, dicts, and lists;
- preserve the source key and normalized key in `numeric_fields`;
- do not infer a timer unit from magnitude.

Malformed numeric values in recognized numeric/time fields produce
`malformed_timer_numeric_field`.

### Nested Or Unsupported Fields

- Nested dict/list values must not be copied wholesale into normalized timer
  records.
- The record may include their field names in `unsupported_field_names`.
- Nested or unsupported values should add `unsupported_timer_field_shape` when
  they appear under a key that looks timer-related.
- Unknown scalar fields may be carried as generic string, boolean, or numeric
  field entries, but must not gain semantic meaning without a later contract.

## Seat, Player, And Owner Field Policy

Direct timer ownership fields are accepted only when present on the raw timer
record.

Recognized direct fields:

- `ownerSeatId`, `owner_seat_id`
- `controllerSeatId`, `controller_seat_id`
- `playerSeatId`, `player_seat_id`
- `seatId`, `seat_id`
- `systemSeatId`, `system_seat_id`
- `teamId`, `team_id`
- `playerId`, `player_id`

Rules:

- `owner_seat_id`, `controller_seat_id`, `player_seat_id`,
  `system_seat_id`, `team_id`, and `player_id` are normalized with identifier
  and seat/player/team field rules.
- `seatId` and `seat_id` populate `player_seat_id` only when a more specific
  `playerSeatId`/`player_seat_id` is absent.
- `direct_seat_ids` is the ordered de-duplicated union of direct owner,
  controller, player, seat, and system seat IDs.
- Missing direct seat/player fields must remain unknown.
- `turn_info.active_player_seat_id`, `decision_player_seat_id`, and
  `priority_player_seat_id` may be carried in collection-level
  `contextual_turn_info`, but must not be copied into record `seat_fields` or
  `direct_seat_ids`.
- The module must not guess timer ownership from active player, priority
  player, decision player, controller, matchup, or game state context.

## Time-Unit Policy

The normalized time-unit vocabulary is:

- `seconds`
- `milliseconds`
- `unknown`

Unit detection rules:

- Field names ending in `Ms`, `MS`, `Millis`, `Milliseconds`, or
  `_milliseconds` map to `milliseconds`.
- Field names ending in `Sec`, `Secs`, `Seconds`, or `_seconds` map to
  `seconds`.
- Field names containing `time`, `timer`, `duration`, `elapsed`, `remaining`,
  `timeout`, `deadline`, `rope`, or `clock` but without an explicit unit map to
  `unknown`.
- Counts such as `turnNumber`, `priorityCount`, or `ropeCount` are numeric
  evidence but not time evidence unless the field name also carries a time-unit
  suffix.
- The implementation must not infer seconds versus milliseconds from numeric
  magnitude.

Conversion rules:

- Millisecond values may include a derived `seconds_value` equal to
  `value / 1000.0`.
- Seconds values may include `seconds_value` equal to the original value.
- Unknown-unit values must not include `seconds_value`.
- Negative time values must be preserved but flagged with
  `negative_timer_value` and lower confidence.
- Non-finite numeric values must be rejected and flagged as malformed.

## Evidence Vocabulary

### `source_evidence`

Allowed values:

- `timer`
- `mixed`
- `unknown`

Records from `timers` use `timer`. Collection-level summaries spanning timer
records plus contextual `turn_info` may use `mixed` only if the summary field
explicitly names both sources.

### `evidence_status`

Allowed values:

- `observed`
- `degraded`
- `unknown`
- `conflict`

Rules:

- Well-formed raw timer scalar fields normalize to `observed`.
- Malformed raw fields that still produce a record normalize to `degraded`.
- Records with no trusted timer value normalize to `unknown` unless a
  malformed source is clearly degraded.
- Contradictory direct fields, such as two direct seat fields that cannot be
  reconciled by the record shape, may use `conflict` and must require review.

### `value_source`

Allowed values:

- `observed`
- `derived`
- `unknown`
- `conflict`

Rules:

- Raw timer IDs, type/name/state strings, direct seat/player fields, booleans,
  and numeric values are `observed`.
- Unit labels and `seconds_value` conversions are `derived` from observed field
  names and values.
- Missing or unusable values are `unknown`.
- Contradictory values are `conflict`.

### `confidence`

Allowed values:

- `high`
- `medium`
- `low`
- `unknown`

Rules:

- Well-formed raw timer fields with explicit units may use `high`.
- Well-formed raw timer fields with unknown units should use `medium` unless
  other degradation exists.
- Contextual turn-info fields are context only and should not raise record
  confidence.
- Malformed, negative, unsupported, or contradictory records use `low`.
- Records with no trusted timer value use `unknown`.

### Degradation Flags

Required v1 degradation flags:

- `malformed_timers_section`
- `malformed_timer_record`
- `malformed_timer_id`
- `malformed_timer_string_field`
- `malformed_timer_boolean_field`
- `malformed_timer_numeric_field`
- `malformed_timer_seat_field`
- `unsupported_timer_field_shape`
- `negative_timer_value`
- `unknown_timer_time_unit`
- `conflicting_timer_seat_fields`
- `truncation_or_data_loss_evidence`

The implementation may add narrower flags, but tests must protect the required
flags above when their conditions occur.

## Consumer Relationships

### GameState Payloads

Required v1 GameState behavior:

- Add `normalized_timers` as an additive payload field produced from raw
  `timers` and optional `turn_info` context.
- Preserve existing raw `timers` exactly in name and meaning.
- Preserve `normalized_annotations` behavior.
- Preserve `raw_game_state` behavior.
- Do not add a new event class.
- Do not change GRE dispatch.
- Do not change game-result emission.
- Do not change parser state final reconciliation, match identity, game
  identity, or deduplication.

### `turn_info.py`

`turn_info.py` remains the owner of normalized turn context. Timer
normalization may consume `payload["turn_info"]` only as context.

Required boundary:

- Timer normalization must not change `turn_info.py`.
- Timer normalization must not reinterpret active-player precedence.
- Missing timer ownership must not be guessed from active, decision, or
  priority player.
- Contextual turn-info values must be labeled separately from direct timer
  fields.

### Annotation Normalization

Timer normalization and annotation normalization are sibling GRE GameState
normalization helpers.

Required boundary:

- `timers.py` must not import `annotations.py` unless a later implementation
  proves a narrow helper need.
- `annotations.py` must not be reopened for timer semantics.
- Timer records must not infer timer meaning from annotation markers.
- Annotation records must not infer annotation meaning from timer fields.

### Diagnostics Mode

Diagnostics may report timer normalization health after Codex C adds
parser-owned `normalized_timers`.

Allowed diagnostics facts:

- timer record count
- degraded timer record count
- time-unit counts
- malformed timer degradation flags
- direct seat ID counts
- truncation/data-loss interaction

Forbidden diagnostics behavior:

- reconstructing missing timers from truncation markers
- deciding clock pressure, rope usage severity, player mistakes, or gameplay
  advice
- creating recovered game objects, zones, actions, match identity, game
  identity, winners, final reconciliation facts, or opponent facts
- making diagnostics output parser truth

### Golden Replay

Golden replay may compare reduced expected timer facts only after Codex C adds
a parser-owned normalized timer output.

Allowed manifest expectations:

- selected `normalized_timers` summary fields
- selected record counts
- selected time-unit counts
- selected degradation flags
- selected direct seat IDs from sanitized or synthetic fixtures

Forbidden manifest behavior:

- broad raw timer snapshots unless explicitly justified and sanitized
- automatic expected-output blessing
- raw private `Player.log` excerpts
- inferred missing GameState facts
- player-mistake or clock-pressure labels

### Evidence Ledger

The evidence ledger may later reference normalized timer records as parser
evidence for future clock, turn, priority, or diagnostics facts.

Required relationship:

- The timer normalizer supplies evidence and confidence labels.
- The ledger describes which parser-managed facts depend on that evidence.
- The ledger must not become a second parser or override normalized timer
  semantics.
- Future clock-pressure analytics must inherit the lowest confidence of their
  required timer and context ingredients and must remain downstream analytics,
  not parser truth.

## Unknowns

- Arena may emit timer payload shapes not represented in current tests.
- Current committed golden replay fixtures do not appear to carry timer-focused
  expected facts.
- Common timer field names and units may vary by game mode, priority state, or
  client version.
- Direct timer ownership fields may be absent.
- The exact relationship between timers, priority player, decision player, and
  active player is not contractually established.
- GameState diff/update/deletion mechanics remain a separate backlog module.

## Suspected Gaps

- Current GameState payloads preserve raw timer arrays but do not expose a
  stable normalized timer view.
- No shared malformed-input policy exists for timer dictionaries.
- Diagnostics and golden replay do not have dedicated timer degradation
  summaries.
- Future analytics could accidentally infer clock pressure or player mistakes
  from ambiguous timer evidence without a parser-owned evidence contract.

## Fixture And Validation Strategy

Codex C should prefer synthetic fixtures for timer unit tests. Sanitized
`Player.log` slices are allowed only when they are necessary for parser-path
coverage and pass existing privacy/sanitization policy.

Required focused test coverage:

- raw timer arrays remain preserved in `GameStateEvent.payload`
- `normalized_timers` is additive and JSON-serializable
- missing or `None` timers produce zero records without degradation
- non-list `timers` produce collection degradation without raising
- non-dict timer entries produce degraded placeholder records
- timer ID normalization follows `api_common.normalize_int_list()` scalar
  behavior
- recognized string fields normalize only from strings
- boolean fields accept only actual booleans and never become numeric values
- identifier and seat/player/team fields reject booleans and floats
- time/count numeric fields accept finite numbers and numeric strings
- explicit second and millisecond fields are classified by field-name unit
  suffix
- unknown-unit time fields remain unknown-unit and do not gain
  `seconds_value`
- millisecond values may include derived seconds values
- negative values are preserved with degradation
- direct seat fields populate `direct_seat_ids`
- turn-info context is carried separately and does not populate
  `direct_seat_ids`
- unsupported nested fields are not copied wholesale
- existing GameState, turn-info, annotation, diagnostics, golden replay, and
  parser-regression tests remain stable
- schema snapshot update is limited to the additive `normalized_timers`
  parser payload key

Suggested implementation validation:

```bash
python3 -m pytest -q tests/test_gre_timers_parser.py
python3 -m pytest -q tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_gre_turn_info_parser.py
python3 -m pytest -q tests/test_gre_annotations_parser.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_parser_regressions.py
python3 -m ruff check src tests
git diff --check
```

If Codex C changes a parser payload shape beyond the additive
`normalized_timers` field, it must also run the relevant protected-surface
checks and route back for a contract loopback before continuing.

## Protected Surfaces And Stop Conditions

Do not:

- target `main` directly;
- close tracker #47;
- close related issue #11;
- change workbook schema;
- change webhook payload shape;
- change Apps Script behavior;
- change output transport behavior;
- change parser state final reconciliation;
- change parser event classes;
- change match identity, game identity, or deduplication policy;
- add or change secrets, environment variables, API keys, model defaults, or
  webhook URLs;
- commit raw private `Player.log` excerpts;
- commit generated data, runtime status files, failed posts, or workbook
  exports;
- build clock-pressure analytics, gameplay advice, player-mistake labels,
  hidden-card inference, decklist completion, archetype classification,
  OpenAI/model-provider behavior, or AI/analytics truth;
- move parser truth into workbook formulas, dashboard logic, webhook
  transport, Apps Script, AI output, or analytics surfaces;
- solve GameState diff/update/deletion mechanics in this module;
- copy Manasight source code.

Stop and route back to Codex B or Codex A if:

- implementation requires a workbook, webhook, Apps Script, runtime status, or
  output schema migration;
- implementation requires changing parser event classes;
- implementation requires changing final reconciliation, match identity, game
  identity, or deduplication behavior;
- raw timer preservation would be weakened;
- timer ownership would need to be guessed from turn context;
- clock-pressure, mistake-label, coaching, or analytics output appears
  necessary;
- sanitized fixtures are insufficient and private raw logs would be needed.

## Acceptance Criteria

- `docs/contracts/parser_timer_normalization.md` defines the durable contract
  for the module.
- The contract clearly names the parser-owned module path and related files.
- The contract preserves raw timer arrays.
- The contract defines normalized collection and record shapes.
- The contract defines input, malformed-input, string, boolean, numeric,
  direct-seat, time-unit, source-evidence, confidence, and degradation rules.
- The contract defines downstream consumer boundaries.
- The contract defines validation obligations for Codex C and Codex E.
- The contract does not implement behavior changes.

## Workflow Decision

Verdict: ready for Codex C: Module Implementer.

A Thinker/problem-representation loopback is not required before implementation
because issue #115 already contains a complete Codex A problem representation,
and this contract resolves the v1 design choice: implement a parser-side timer
helper and add an additive `normalized_timers` GameState payload field while
preserving raw timer arrays.

## Pasteable Prompt For Codex C

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #115: GameState timer normalization module.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/115
- Related evidence/resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Branch/base: codex/parser-reliability-intelligence
- Previous completed issue: #113 Annotation normalization
- Previous PR: #114
- Previous merge commit: bbcd61656f2af7981936e415e6d1431f5889f012
- Contract: docs/contracts/parser_timer_normalization.md

Goal:
Implement the smallest coherent parser-owned GRE timer normalization module that satisfies the contract. Preserve raw GameState timer arrays while adding the additive normalized timer view required by the contract.

Read first:
1. AGENTS.md
2. docs/agent_constitution.md
3. docs/agent_rules.yml
4. docs/codex_module_workflow.md
5. docs/agent_threads/implementation.md
6. docs/contracts/parser_timer_normalization.md
7. docs/contracts/parser_gre_game_state.md
8. src/mythic_edge_parser/parsers/gre/game_state.py
9. tests/test_gre_game_state_parser.py
10. docs/contracts/parser_gre_turn_info.md
11. src/mythic_edge_parser/parsers/gre/turn_info.py
12. tests/test_gre_turn_info_parser.py
13. docs/contracts/parser_annotation_normalization.md
14. src/mythic_edge_parser/parsers/gre/annotations.py
15. tests/test_gre_annotations_parser.py
16. docs/contracts/parser_diagnostics_mode.md
17. docs/contracts/parser_golden_replay_harness.md
18. docs/contracts/player_log_evidence_ledger.md

Do:
- Create src/mythic_edge_parser/parsers/gre/timers.py.
- Add focused tests, expected at tests/test_gre_timers_parser.py.
- Add the additive GameState payload field normalized_timers.
- Preserve payload timers, normalized_annotations, turn_info, and raw_game_state behavior.
- Update parser_payload_keys snapshot only for the additive normalized_timers key.
- Prefer synthetic fixtures over sanitized Player.log slices.
- Produce docs/implementation_handoffs/parser_timer_normalization_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Target main directly.
- Close tracker #47.
- Close related issue #11.
- Change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Build clock-pressure analytics, gameplay advice, player-mistake labels, hidden-card inference, decklist completion, archetype classification, OpenAI/model-provider behavior, or AI/analytics truth.
- Solve GameState diff/update/deletion mechanics in this module.
- Copy Manasight source code or commit raw private Player.log excerpts.
- Stage or commit unless explicitly asked.

Suggested validation:
python3 -m pytest -q tests/test_gre_timers_parser.py
python3 -m pytest -q tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_gre_turn_info_parser.py
python3 -m pytest -q tests/test_gre_annotations_parser.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_parser_regressions.py
python3 -m ruff check src tests
git diff --check
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/115"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/113"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/114"
  previous_merge_commit: "bbcd61656f2af7981936e415e6d1431f5889f012"
  completed_thread: "B"
  next_thread: "C"
  verdict: "ready_for_module_implementation"
  branch: "codex/parser-reliability-intelligence"
  source_artifact: "docs/contracts/parser_timer_normalization.md"
  target_artifact: "docs/implementation_handoffs/parser_timer_normalization_comparison.md"
  risk_tier: "High"
  validation:
    - "tmpfile=$(mktemp); git diff --no-index --check /dev/null docs/contracts/parser_timer_normalization.md >\"$tmpfile\" 2>&1; rc=$?; cat \"$tmpfile\"; rm -f \"$tmpfile\"; test \"$rc\" -le 1"
    - "if LC_ALL=C rg -n '[^[:ascii:]]' docs/contracts/parser_timer_normalization.md; then exit 1; else test $? -eq 1; fi"
    - "documentation contract only; no parser tests required for Codex B"
  recommended_implementation_validation:
    - "python3 -m pytest -q tests/test_gre_timers_parser.py"
    - "python3 -m pytest -q tests/test_gre_game_state_parser.py"
    - "python3 -m pytest -q tests/test_gre_turn_info_parser.py"
    - "python3 -m pytest -q tests/test_gre_annotations_parser.py"
    - "python3 -m pytest -q tests/test_event_schema_snapshots.py"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q tests/test_parser_regressions.py"
    - "python3 -m ruff check src tests"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, output transport, parser state final reconciliation, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not build clock-pressure analytics, gameplay advice, player-mistake labels, hidden-card inference, decklist completion, archetype classification, OpenAI/model-provider behavior, or AI/analytics truth."
    - "Do not solve GameState diff/update/deletion mechanics in this module."
    - "Do not copy Manasight source code or commit raw private Player.log excerpts."
```
