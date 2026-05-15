# GRE Turn Info Parser Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/28

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Problem-representation docs read because issue #28 is the source problem
representation:

- `docs/agent_threads/problem_representation.md`
- `docs/templates/problem_representation.md`

Adjacent contracts:

- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/parser_extractors.md`
- `docs/contracts/parser_state.md`
- `docs/contracts/parser_gre_game_result.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the parser-owned GRE turn-info payload helper in
`src/mythic_edge_parser/parsers/gre/turn_info.py`. It is a contract artifact
only. It does not implement code or change parser behavior.

## Module

`src/mythic_edge_parser/parsers/gre/turn_info.py`

The module converts the raw `turnInfo` dictionary inside a selected GRE
`gameStateMessage` dictionary into a normalized parser-owned turn context
dictionary.

Plain English: this module does not parse raw log text, dispatch GRE events,
decide match or game identity by itself, mutate runtime state, or write
workbook-facing rows. It normalizes one GRE `turnInfo` section into stable
snake_case fields for `game_state.py` and downstream parser/state consumers.

## Owning Layer

Parser and state interpretation.

`turn_info.py` owns normalized turn-context extraction from raw GRE
`gameStateMessage.turnInfo` values:

- turn number
- phase
- step
- active player seat
- decision player seat
- priority player seat
- next phase
- next step

Parser truth boundary:

- `turn_info.py` owns conversion from raw GRE `turnInfo` fields to normalized
  parser turn-info fields.
- `game_state.py` owns carrying the returned dict at
  `GameStateEvent.payload["turn_info"]`, mirroring selected fields into
  `identity` and top-level shortcuts, and preserving raw game-state evidence.
- `parsers/gre/__init__.py` owns raw GRE log dispatch and selection of current
  or queued `gameStateMessage` dictionaries before `game_state.py` calls this
  helper.
- `app/extractors.py` owns downstream hydrated identity and fallback extraction
  from normalized payload fields and preserved raw payloads.
- `app/state.py` owns live parser context, match summary mutation, turn-count
  updates, starting-player inference, opening-hand capture, and final
  reconciliation.
- `app/transforms.py`, `app/runtime_surfaces.py`, and
  `app/gameplay_actions.py` consume parser-produced turn context for rows,
  timelines, summaries, and gameplay-action sequencing.
- Workbook formulas, dashboard logic, webhook transport, Apps Script, and
  AI-generated interpretation must consume parser/state-produced facts and
  must not become the source of truth for GRE turn-info parsing.

This contract must not reopen the completed standalone `gre/game_state.py`
audit except for consumed-output compatibility.

## Files Owned By This Contract

- `src/mythic_edge_parser/parsers/gre/turn_info.py`
- `tests/test_gre_turn_info_parser.py`
- `docs/contracts/parser_gre_turn_info.md`

Related files whose behavior is referenced but not owned by this contract:

- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_game_state_parser.py`
- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `tests/test_parsers.py`
- `src/mythic_edge_parser/app/extractors.py`
- `tests/test_app_extractors.py`
- `src/mythic_edge_parser/app/state.py`
- `tests/test_state.py`
- `src/mythic_edge_parser/app/transforms.py`
- `tests/test_transforms.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `tests/test_runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `tests/test_gameplay_actions.py`
- `src/mythic_edge_parser/app/arena_id_validation.py`
- `src/mythic_edge_parser/app/grp_id_candidates.py`
- `tests/test_grp_id_candidates.py`
- `tests/test_parser_regressions.py`
- `docs/contracts/parser_gre_game_state.md`
- `docs/contracts/parser_extractors.md`
- `docs/contracts/parser_state.md`
- `docs/contracts/parser_gre_game_result.md`

## Public Interface

### Helper Function

`build_turn_info(gsm: dict[str, Any]) -> dict[str, Any]`

Public parser helper imported by
`src/mythic_edge_parser/parsers/gre/game_state.py`.

Contract status:

- Accepts a selected GRE `gameStateMessage` dictionary.
- Reads only `gsm["turnInfo"]` when it is a dictionary.
- Returns a new normalized dictionary for
  `GameStateEvent.payload["turn_info"]`.
- Does not create an event object.
- Does not inspect raw log text.
- Does not mutate `gsm` or the raw `turnInfo` dictionary.
- Has no side effects.

Input preconditions:

- `gsm` must be a dict-like object with `.get()`.
- Non-dict direct helper calls are outside the current public contract.
- GRE game-state dispatch already filters selected game-state message shapes
  to dictionaries before this helper is reached through `game_state.py`.

Underscored helpers in `turn_info.py` are implementation details:

- `_turn_info_payload(gsm)`
- `_first_present(*values)`
- `_string_field(value)`
- `_maybe_int(value)`

Their behavior is contract-covered through `build_turn_info()`, but other
modules should not import them as public API.

## Accepted Input Shape

### Selected GRE Game-State Message

Source: `game_state.py` passes the selected `gsm` dictionary to
`build_turn_info(gsm)` after GRE dispatch chooses either:

- `message["gameStateMessage"]`, when it is a dict, or
- `message["queuedGameStateMessage"]["gameStateMessage"]`, when the current
  `gameStateMessage` is not a dict and the queued nested game-state message is
  a dict.

Representative input:

```json
{
  "gameInfo": {
    "matchID": "match-42",
    "gameNumber": 2,
    "stage": "GameStage_Play"
  },
  "turnInfo": {
    "turnNumber": "3",
    "phase": "Phase_Main1",
    "step": "Step_PreCombatMain",
    "activePlayer": "2",
    "activePlayerSeatId": "1",
    "decisionPlayer": "1",
    "priorityPlayer": "2",
    "nextPhase": "Phase_Combat",
    "nextStep": "Step_BeginCombat"
  }
}
```

Accepted `turnInfo` behavior:

- Missing `turnInfo` returns `{}`.
- Non-dict `turnInfo` returns `{}`.
- Empty dict `turnInfo` returns `{}`.
- Non-empty dict `turnInfo` returns the stable normalized field set listed in
  `Outputs`.
- Unknown extra keys inside `turnInfo` are ignored.
- Nested values may be any Python value. Integer and string field behavior is
  defined below.

## Outputs

`build_turn_info()` returns either `{}` or a normalized dict with exactly the
current field set below.

When `turnInfo` is missing, non-dict, or `{}`:

```python
{}
```

When `turnInfo` is a non-empty dict:

| Output field | Source key | Type | Default | Behavior |
| --- | --- | --- | --- | --- |
| `turn_number` | `turnNumber` | `int | None` | `None` | Local `_maybe_int()` conversion. |
| `phase` | `phase` | `str` | `""` | Local `_string_field()` conversion. |
| `step` | `step` | `str` | `""` | Local `_string_field()` conversion. |
| `active_player_seat_id` | `activePlayer` then `activePlayerSeatId` | `int | None` | `None` | `_first_present()` precedence, then local `_maybe_int()`. |
| `decision_player_seat_id` | `decisionPlayer` | `int | None` | `None` | Local `_maybe_int()` conversion. |
| `priority_player_seat_id` | `priorityPlayer` | `int | None` | `None` | Local `_maybe_int()` conversion. |
| `next_phase` | `nextPhase` | `str` | `""` | Local `_string_field()` conversion. |
| `next_step` | `nextStep` | `str` | `""` | Local `_string_field()` conversion. |

Example normalized output:

```json
{
  "turn_number": 3,
  "phase": "Phase_Main1",
  "step": "Step_PreCombatMain",
  "active_player_seat_id": 2,
  "decision_player_seat_id": 1,
  "priority_player_seat_id": 2,
  "next_phase": "Phase_Combat",
  "next_step": "Step_BeginCombat"
}
```

No raw `turnInfo` object is included in this output. Raw game-state preservation
is owned by `game_state.py` through `payload["raw_game_state"]`.

## Active-Player Precedence

Observed current behavior:

- `active_player_seat_id` is sourced from `activePlayer` first.
- If `activePlayer` is `None` or `""`, the helper falls back to
  `activePlayerSeatId`.
- If `activePlayer` is any other value, including `0`, `False`, `{}`, or `[]`,
  it is treated as present and passed to `_maybe_int()`.
- If the selected active-player value cannot be converted through
  `_maybe_int()`, `active_player_seat_id` becomes `None`.

Required guarantee:

- `activePlayer` must remain higher precedence than `activePlayerSeatId` unless
  a future contract intentionally changes active-player semantics.
- The fallback condition must remain "missing or blank string" rather than
  "falsy".
- Downstream workbook, dashboard, Apps Script, webhook, and AI layers must not
  reinterpret active-player precedence.

Compatibility examples:

| Raw `activePlayer` | Raw `activePlayerSeatId` | Output |
| --- | --- | --- |
| `"2"` | `"1"` | `2` |
| `""` | `"1"` | `1` |
| `None` | `"1"` | `1` |
| `0` | `"1"` | `0` |
| `False` | `"1"` | `0` |
| `"bad"` | `"1"` | `None` |

The `"bad"` case is important: because `activePlayer` is present, the helper
does not fall back to `activePlayerSeatId` after conversion fails.

## Integer Conversion Behavior

Integer-like fields:

- `turnNumber`
- `activePlayer`
- `activePlayerSeatId`
- `decisionPlayer`
- `priorityPlayer`

Observed current behavior:

- Conversion uses local `_maybe_int(value)`.
- `_maybe_int(value)` returns `int(value)` when Python accepts the value.
- `_maybe_int(value)` returns `None` when Python raises `TypeError` or
  `ValueError`.
- Boolean values follow Python `int()` behavior:
  - `True` becomes `1`.
  - `False` becomes `0`.
- Float values follow Python `int()` behavior and truncate toward zero.
- Signed and whitespace-padded integer strings are accepted by Python `int()`.
- Fractional strings such as `"1.5"` and invalid strings become `None`.
- Missing keys and explicit `None` become `None`.

Required guarantee:

- Preserve the current local `_maybe_int()` behavior for turn-info fields until
  a new problem representation and contract deliberately change integer
  normalization across affected parser modules.
- Do not silently align this helper with
  `api_common.normalize_int_list()`. That shared list normalizer rejects bools,
  floats, signed integer strings, and whitespace-padded strings in cases where
  local `_maybe_int()` currently accepts some of them.
- If future hardening rejects bools or floats, it must be routed as a parser
  integer-normalization behavior change and validated against game-state,
  extractor, state, transform, runtime, gameplay-action, and regression tests.

Compatibility examples:

| Raw value | Output |
| --- | --- |
| `"3"` | `3` |
| `" 3 "` | `3` |
| `"-2"` | `-2` |
| `True` | `1` |
| `False` | `0` |
| `4.9` | `4` |
| `"1.5"` | `None` |
| `"bad"` | `None` |
| `None` | `None` |

## String Conversion Behavior

String-like fields:

- `phase`
- `step`
- `nextPhase`
- `nextStep`

Observed current behavior:

- Conversion uses local `_string_field(value)`.
- `_string_field(value)` returns `str(value or "")`.
- Missing keys, `None`, `""`, `False`, `0`, empty lists, and empty dicts become
  `""`.
- Truthy non-string values become their Python `str()` representation.

Required guarantee:

- Preserve the current `str(value or "")` behavior for string-like turn-info
  fields until a new contract intentionally changes it.
- Do not reinterpret raw GRE phase or step values downstream.

Compatibility examples:

| Raw value | Output |
| --- | --- |
| `"Phase_Main1"` | `"Phase_Main1"` |
| `None` | `""` |
| `""` | `""` |
| `0` | `""` |
| `False` | `""` |
| `["Phase_Main1"]` | `"['Phase_Main1']"` |

## Game-State Consumed-Output Boundary

This section defines only how `game_state.py` consumes the turn-info helper. It
does not reopen the completed `gre/game_state.py` audit.

Observed current behavior:

- `game_state.py` calls `build_turn_info(gsm)` exactly once while building a
  game-state payload.
- The returned dict is stored at `payload["turn_info"]`.
- `payload["turn_number"]` is `turn_info.get("turn_number")`.
- `payload["active_player_seat_id"]` is
  `turn_info.get("active_player_seat_id")`.
- `payload["identity"]["turn_number"]` is `turn_info.get("turn_number")`.
- `payload["identity"]["active_player_seat_id"]` is
  `turn_info.get("active_player_seat_id")`.
- `payload["identity"]["phase"]` is `turn_info.get("phase", "")`.
- `payload["identity"]["step"]` is `turn_info.get("step", "")`.
- `decision_player_seat_id`, `priority_player_seat_id`, `next_phase`, and
  `next_step` are carried inside `payload["turn_info"]` but are not mirrored
  into `game_state.py` identity or top-level shortcuts.
- If `build_turn_info(gsm)` returns `{}`, `game_state.py` leaves turn shortcuts
  as `None` and identity phase/step as `""`.

Required compatibility:

- `build_turn_info()` must keep returning a dictionary shape that `game_state.py`
  can carry directly without additional raw parsing.
- `turn_number`, `active_player_seat_id`, `phase`, and `step` must remain
  available under their current snake_case names for `game_state.py` identity
  and top-level shortcut construction.
- `game_state.py` must remain the module that carries the raw GRE message for
  downstream fallback; `turn_info.py` should not add raw-payload preservation
  unless a future contract changes that boundary.

## Downstream Consumers

### `app/extractors.py`

Extractor helpers consume normalized `turn_info` and hydrated identity:

- `_game_state_turn_info_payload(payload)`
- `_hydrate_game_state_identity(payload, context=None)`
- `_extract_turn_info(payload, context=None)`

Compatibility expectations:

- Normalized `turn_info` remains a dict.
- Extractors can read snake_case turn-info fields from normalized payloads.
- Extractors may still fall back to raw camelCase `turnInfo` fields preserved
  under `raw_game_state`, but raw fallback is extractor-owned compatibility,
  not turn-info parser ownership.
- `_extract_turn_info()` continues returning the seven-tuple
  `(match_id, game_number, turn_number, active_player_seat_id, phase, step, stage)`.

### `app/state.py`

State consumes hydrated turn info for:

- current match/game context updates
- game turn count updates
- starting-player and local-team inference through game-state payloads
- opening-hand snapshot eligibility, especially turn-one filtering
- summary first/last timestamps and game touch behavior

Compatibility expectations:

- Missing turn info must not fabricate a turn number or active player.
- Missing match/game identity remains downstream context fallback behavior, not
  `turn_info.py` behavior.
- Final reconciliation remains owned by state and is not changed here.

### `app/transforms.py`

Transforms consume hydrated turn info for:

- GameState inclusion gates
- local turn deduplication keys
- turn rows
- derived serializable identity
- human-readable GameState summaries

Compatibility expectations:

- Turn number and active-player seat remain stable primitive values or `None`.
- Phase and step remain strings.
- Workbook row shape, row deduplication, and raw/archive row behavior are not
  changed by this contract.

### `app/runtime_surfaces.py`

Runtime surfaces consume hydrated turn info for:

- active match timeline entries
- event match/game identity
- runtime-visible turn, active-player, phase, step, and stage metadata

Compatibility expectations:

- Runtime surfaces consume parser-produced turn context and must not become a
  raw GRE `turnInfo` parser.

### `app/gameplay_actions.py`

Gameplay-action observation consumes `GameStateEvent.payload["identity"]` and
extractor-readable game-state payloads for:

- turn tracking
- active-player tracking
- gameplay event context
- turn-started action emission

Compatibility expectations:

- `turn_info.py` supplies the normalized fields used by `game_state.py`
  identity.
- Gameplay-action artifacts remain downstream derived outputs, not turn-info
  truth owners.

### Diagnostics And Regression Tools

`arena_id_validation.py`, `grp_id_candidates.py`, saved-event replay,
regression fixtures, and parser regression tests can consume turn context from
normalized payloads or extractor fallback paths.

Compatibility expectations:

- Saved event payloads with existing `turn_info` shapes remain readable.
- New behavior must not require workbook formulas, dashboard logic, Apps
  Script, webhook transport, or AI interpretation to recover turn context.

## Observed Current Behavior

- `build_turn_info({})` returns `{}`.
- `build_turn_info({"turnInfo": "bad"})` returns `{}`.
- `build_turn_info({"turnInfo": {}})` returns `{}`.
- A non-empty `turnInfo` dict returns a normalized dict with the eight output
  fields listed above.
- Unknown raw `turnInfo` keys are ignored.
- Integer-like fields use permissive Python `int()` conversion through local
  `_maybe_int()`.
- String-like fields use `str(value or "")`.
- `activePlayer` takes precedence over `activePlayerSeatId` when it is not
  `None` and not `""`.
- The helper returns a new dictionary and does not mutate the raw payload.
- The helper does not preserve the raw `turnInfo` object.
- The helper does not log, write files, touch runtime state, post webhooks,
  update workbook rows, or emit events.

## Required Guarantees

- Keep `build_turn_info(gsm)` as the public helper for GRE turn-info
  normalization.
- Keep the output field names stable:
  - `turn_number`
  - `phase`
  - `step`
  - `active_player_seat_id`
  - `decision_player_seat_id`
  - `priority_player_seat_id`
  - `next_phase`
  - `next_step`
- Keep `{}` as the result for missing, non-dict, and empty-dict `turnInfo`.
- Keep full normalized field output for non-empty `turnInfo` dictionaries, even
  when individual keys are missing or malformed.
- Keep active-player precedence as `activePlayer` before
  `activePlayerSeatId`, with fallback only for `None` and `""`.
- Keep current integer conversion behavior, including bool and float handling,
  unless a future contract deliberately changes it.
- Keep current string conversion behavior, including falsy values becoming
  `""`, unless a future contract deliberately changes it.
- Keep the helper pure and side-effect free.
- Keep raw-payload preservation out of `turn_info.py`; raw GRE preservation
  remains owned by `game_state.py`.
- Keep parser-owned turn-info truth inside parser/state code, not workbook
  formulas, dashboard logic, Apps Script, webhook transport, or AI-generated
  interpretation.

## Unknowns

- Whether permissive local `_maybe_int()` behavior should continue accepting
  booleans and truncating floats forever.
- Whether `0` and `False` are semantically valid active-player seat values or
  merely current Python conversion artifacts.
- Whether `str(value or "")` should continue treating `0` and `False` as blank
  if MTGA ever sends those values for phase or step fields.
- Whether future MTGA payloads will add alternate raw keys for active,
  decision, or priority players.
- Whether `decision_player_seat_id`, `priority_player_seat_id`, `next_phase`,
  and `next_step` are future-facing evidence only or need first-class
  downstream consumers.
- Whether future diagnostics should preserve raw `turnInfo` inside the
  normalized `turn_info` dict, or continue relying on
  `game_state.py` raw-game-state preservation.

## Suspected Gaps

- Focused turn-info tests do not appear to assert active-player precedence when
  both `activePlayer` and `activePlayerSeatId` are present and convertible.
- Focused turn-info tests do not appear to assert that a present but
  unconvertible `activePlayer` does not fall back after conversion failure.
- Focused turn-info tests do not appear to lock local `_maybe_int()` bool,
  float, signed-string, and whitespace-padded string behavior.
- Focused turn-info tests do not appear to lock `_string_field()` behavior for
  `0`, `False`, and truthy non-string values.
- Focused turn-info tests do not appear to assert `{}` for empty-dict
  `turnInfo` separately from missing/non-dict `turnInfo`.
- Focused turn-info tests do not appear to assert that the helper does not
  mutate `gsm` or the raw `turnInfo` dictionary.

## Error Behavior

- Missing `turnInfo` returns `{}`.
- Non-dict `turnInfo` returns `{}`.
- Empty dict `turnInfo` returns `{}`.
- Malformed integer-like values return `None` for their output fields.
- Malformed or missing string-like values return `""` for their output fields
  when a non-empty `turnInfo` dict is otherwise being normalized.
- Unknown extra keys are ignored.
- Dict-like `gsm` inputs should not raise for missing or malformed optional
  `turnInfo` content.
- Non-dict direct helper inputs are outside the current public contract and may
  raise because the helper expects `.get()`.
- Contract ambiguity about active-player precedence, integer conversion,
  string conversion, or downstream truth ownership must route back to Codex B
  rather than being implemented silently.

## Side Effects

`build_turn_info()` has no side effects.

It must not:

- mutate `gsm`
- mutate `gsm["turnInfo"]`
- emit events
- log diagnostics
- update parser runtime state
- post webhooks
- update workbook rows
- write runtime status files
- write failed-post queues
- write raw logs
- generate card data
- export workbook files

## Dependency Order

Implementation threads should evaluate changes in this order:

1. `src/mythic_edge_parser/parsers/gre/turn_info.py`
2. `tests/test_gre_turn_info_parser.py`
3. `src/mythic_edge_parser/parsers/gre/game_state.py`, only for
   consumed-output compatibility
4. `tests/test_gre_game_state_parser.py`
5. `src/mythic_edge_parser/parsers/gre/__init__.py`, only if dispatch evidence
   contradicts the assumed selected-`gsm` boundary
6. `tests/test_parsers.py`
7. `src/mythic_edge_parser/app/extractors.py`, only if fallback consumption is
   implicated
8. `tests/test_app_extractors.py`
9. `src/mythic_edge_parser/app/state.py`, `transforms.py`,
   `runtime_surfaces.py`, `gameplay_actions.py`, and diagnostic tools only if
   focused tests prove parser-local work is insufficient

Do not start with workbook, webhook, Apps Script, dashboard, AI-layer, or
parser-state final-reconciliation changes.

## Compatibility

Compatibility surfaces that must remain stable:

- public helper name and signature:
  `build_turn_info(gsm: dict[str, Any]) -> dict[str, Any]`
- `{}` result for missing, non-dict, and empty-dict `turnInfo`
- eight normalized snake_case output fields for non-empty `turnInfo`
  dictionaries
- active-player precedence from `activePlayer` to `activePlayerSeatId`
- local `_maybe_int()` Python `int()` semantics for integer-like fields
- local `_string_field()` `str(value or "")` semantics for string-like fields
- no raw `turnInfo` preservation inside the normalized output
- no side effects
- `game_state.py` carry-through at `payload["turn_info"]`
- `game_state.py` identity and top-level shortcut compatibility for
  `turn_number`, `active_player_seat_id`, `phase`, and `step`

Breaking changes that require a new problem representation or contract:

- renaming `build_turn_info()`
- renaming output fields
- returning default-filled keys for missing, non-dict, or empty-dict
  `turnInfo`
- removing `decision_player_seat_id`, `priority_player_seat_id`, `next_phase`,
  or `next_step`
- changing active-player precedence or fallback rules
- changing bool, float, signed-string, or whitespace-string integer conversion
  behavior
- changing string conversion for falsy values
- adding raw payloads to the normalized output in a way downstream consumers
  start depending on
- moving turn-context interpretation downstream into workbook formulas,
  dashboard logic, Apps Script, webhook transport, or AI-generated
  interpretation

## Validation Obligations

Documentation-only checks for this contract:

```bash
git diff --check
```

Focused validation expected for later implementation or review:

```bash
python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_transforms.py
python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_gameplay_actions.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
python3 -m ruff check src tests
```

Before submitter opens or updates a module PR, run or verify:

```bash
python3 -m pytest -q
python3 -m ruff check src tests
```

If no behavior changes are needed, the implementation handoff should still
record why existing tests are sufficient or identify the exact missing contract
tests.

## Tests Required

Focused tests expected for Module Implementer or Module Fixer:

- Public helper basics:
  - `build_turn_info({}) == {}`
  - missing `turnInfo` returns `{}`
  - non-dict `turnInfo` returns `{}`
  - empty dict `turnInfo` returns `{}`
- Happy path:
  - all eight normalized fields are returned from expected raw keys
  - unknown extra raw keys are ignored
  - output uses snake_case names only
- Active-player precedence:
  - `activePlayer` wins over `activePlayerSeatId` when both are present
  - `activePlayer == ""` falls back to `activePlayerSeatId`
  - `activePlayer is None` falls back to `activePlayerSeatId`
  - present but unconvertible `activePlayer` does not fall back after
    conversion failure
  - `0` and `False` remain present values under current behavior
- Integer behavior:
  - valid int and digit-string values normalize to integers
  - malformed values become `None`
  - bool and float behavior is explicitly locked as current Python `int()`
    behavior
  - signed and whitespace-padded integer strings follow Python `int()` behavior
  - fractional strings become `None`
- String behavior:
  - missing, `None`, and `""` values become `""`
  - `0`, `False`, empty list, and empty dict become `""`
  - truthy non-string values become `str(value)`
- No side effects:
  - returned dict is newly constructed
  - mutating the returned dict does not mutate raw `turnInfo`
  - helper does not add, remove, or alter keys in `gsm`
- Game-state consumed-output compatibility:
  - `build_game_state_payload()` carries `turn_info` exactly as returned by
    `build_turn_info()`
  - game-state top-level `turn_number` and `active_player_seat_id` remain
    aligned with turn-info output
  - game-state identity `turn_number`, `active_player_seat_id`, `phase`, and
    `step` remain aligned with turn-info output
  - missing or malformed `turnInfo` yields neutral game-state turn shortcuts
    without changing `game_state.py` raw-payload preservation
- Downstream compatibility:
  - extractor tests continue proving normalized/top-level/raw fallback behavior
  - state tests continue proving turn count and opening-hand turn-one behavior
  - transform tests continue proving GameState inclusion and turn-row dedupe
  - runtime and gameplay-action tests continue consuming parser-produced turn
    context without parsing raw GRE as their own truth

## Acceptance Criteria

- The contract clearly names owned files and related consumer files.
- The public helper API and input preconditions are documented.
- Missing, non-dict, and empty-dict `turnInfo` behavior is documented.
- Output field names, source keys, defaults, and types are documented.
- Active-player precedence is explicit.
- Integer conversion behavior is explicit, including bool and float
  compatibility.
- String conversion behavior is explicit, including falsy-value compatibility.
- Malformed input and no-side-effect expectations are documented.
- `game_state.py` consumed-output compatibility is documented without
  reopening the completed game-state audit.
- Downstream consumers and ownership boundaries are documented without moving
  parser-owned truth downstream.
- Test obligations are specific enough for Codex C or Codex D to implement or
  verify.
- Protected surfaces remain unchanged.

## Next Workflow Action

Next role: Codex C, Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex C: Module Implementer for #28 and docs/contracts/parser_gre_turn_info.md.

Goal:
Compare the current GRE turn-info helper and focused tests against the parser GRE turn-info contract. Implement only the smallest coherent code and test changes needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/28
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/parser_gre_turn_info.md
- docs/contracts/parser_gre_game_state.md
- docs/contracts/parser_extractors.md
- docs/contracts/parser_state.md
- src/mythic_edge_parser/parsers/gre/turn_info.py
- tests/test_gre_turn_info_parser.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- tests/test_gre_game_state_parser.py
- tests/test_parsers.py
- src/mythic_edge_parser/app/extractors.py
- tests/test_app_extractors.py
- src/mythic_edge_parser/app/state.py
- tests/test_state.py
- src/mythic_edge_parser/app/transforms.py
- tests/test_transforms.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- tests/test_runtime_surfaces.py
- src/mythic_edge_parser/app/gameplay_actions.py
- tests/test_gameplay_actions.py

Do:
- Compare observed code behavior against the contract before editing.
- Preserve parser-owned turn-info truth boundaries.
- Add focused tests for contracted turn-info behavior not currently covered.
- Keep behavior changes minimal and parser-local unless the contract explicitly requires a downstream compatibility update.
- Do not reopen the completed gre/game_state.py audit except for consumed-output compatibility.
- Produce docs/implementation_handoffs/parser_gre_turn_info_comparison.md with the comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Move parser-owned turn-info truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation.
- Change parser behavior unless required by the contract and covered by focused tests.
- Target main; module PR work belongs on codex/parser-module-audit-suite.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/28"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_gre_turn_info.md"
  target_artifact: "docs/implementation_handoffs/parser_gre_turn_info_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned turn-info truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not reopen the completed gre/game_state.py audit except for consumed-output compatibility."
    - "Do not target main for module PR work."
```

## Handoff Packet

Role performed: Codex B, Module Contract Writer.

Source problem representation: GitHub issue #28, tracked by parser module
audit tracker #5.

Contract produced: `docs/contracts/parser_gre_turn_info.md`

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/5

Risk tier: High.

Owning truth layer: parser and state interpretation.

Public interface:

- `build_turn_info(gsm: dict[str, Any]) -> dict[str, Any]`

Invariants:

- Missing, non-dict, and empty-dict `turnInfo` returns `{}`.
- Non-empty `turnInfo` dictionaries return the eight documented snake_case
  fields.
- `activePlayer` takes precedence over `activePlayerSeatId` unless it is
  `None` or `""`.
- Integer-like fields use current local Python `int()` behavior through
  `_maybe_int()`.
- String-like fields use `str(value or "")`.
- The helper does not mutate input and has no side effects.
- Raw turn-info preservation remains out of this helper and is handled through
  game-state raw-payload preservation.

Required tests: focused helper, active-player precedence, integer conversion,
string conversion, no-side-effect, game-state consumed-output compatibility,
and downstream compatibility obligations listed in `Tests Required`.

Acceptance criteria: listed above.

Open questions or contract risks:

- Current local `_maybe_int()` accepts bools and truncates floats.
- Current `_string_field()` turns `0` and `False` into `""`.
- It is unknown whether `0` or `False` can be semantically valid active-player
  seat values.
- Future MTGA turn-info payloads may add alternate keys for active, decision,
  or priority players.
- `decision_player_seat_id`, `priority_player_seat_id`, `next_phase`, and
  `next_step` may be future-facing evidence with limited downstream
  consumption today.

Next recommended thread role: Codex C, Module Implementer.
