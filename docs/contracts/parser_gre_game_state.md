# GRE Game State Parser Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/26

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Problem-representation docs read because issue #26 is the source problem
representation:

- `docs/agent_threads/problem_representation.md`
- `docs/templates/problem_representation.md`

Adjacent contracts:

- `docs/contracts/parser_state.md`
- `docs/contracts/parser_extractors.md`
- `docs/contracts/parser_gre_game_result.md`
- `docs/contracts/parser_gre_connect_resp.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the parser-owned GRE game-state payload builder in
`src/mythic_edge_parser/parsers/gre/game_state.py` and its dispatch
relationship with `src/mythic_edge_parser/parsers/gre/__init__.py`. It is a
contract artifact only. It does not implement code or change parser behavior.

## Module

`src/mythic_edge_parser/parsers/gre/game_state.py`

The module converts already extracted GRE `gameStateMessage` dictionaries and
`queuedGameStateMessage.gameStateMessage` dictionaries into normalized
`GameStateEvent.payload` dictionaries.

## Owning Layer

Parser and state interpretation.

`game_state.py` owns normalized GRE game-state payload construction:

- payload type for regular and queued game-state messages
- GRE message metadata pass-through fields
- normalized system seat IDs
- game info copy and game-state identity
- turn-info consumption and top-level turn shortcuts
- players, zones, game objects, annotations, persistent annotations, timers,
  and actions list sections
- update and diff metadata
- raw GRE message preservation

It does not own the standalone `turn_info.py` audit, live parser state final
reconciliation, workbook row shape, webhook transport, Apps Script behavior,
dashboard formulas, match identity policy outside the parsed payload, game
identity policy outside the parsed payload, deduplication, or workbook exports.

Parser truth boundary:

- `game_state.py` owns conversion from an extracted raw GRE message dictionary
  plus its selected game-state message dictionary into a normalized
  `GameStateEvent.payload`.
- `turn_info.py` owns turn-info field extraction. This contract documents only
  the `turn_info` output shape consumed and carried by `game_state.py`; it does
  not complete the future standalone `turn_info.py` audit.
- `parsers/gre/__init__.py` owns raw GRE log dispatch, selection of current
  versus queued game-state message dictionaries, event creation, and paired
  `GameResultEvent` emission.
- `game_result.py` consumes normalized `GameStateEvent.payload` for game-over
  detection and `GameResultEvent.payload` construction.
- `app/state.py` owns live/final match and game state mutation after parser
  events exist.
- `app/extractors.py` owns downstream fallback extraction from normalized
  payload fields and preserved raw payloads.
- Workbook formulas, dashboard logic, webhook transport, Apps Script, and
  AI-generated interpretation must consume parser/state-produced facts and
  must not become the source of truth for GRE game-state parsing.

## Files Owned By This Contract

- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `tests/test_gre_game_state_parser.py`
- `docs/contracts/parser_gre_game_state.md`

Related files whose behavior is referenced but not owned by this contract:

- `src/mythic_edge_parser/parsers/gre/turn_info.py`
- `tests/test_gre_turn_info_parser.py`
- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `src/mythic_edge_parser/parsers/api_common.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/arena_id_validation.py`
- `src/mythic_edge_parser/app/grp_id_candidates.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `tests/test_parsers.py`
- `tests/test_state.py`
- `tests/test_app_extractors.py`
- `tests/test_gameplay_actions.py`
- `tests/test_transforms.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_grp_id_candidates.py`
- `tests/test_parser_regressions.py`

## Public Interface

### Constant

`QUEUED_GAME_STATE_MESSAGE_TYPE`

- Value: `"GREMessageType_QueuedGameStateMessage"`.
- Contract status: public parser constant used to distinguish queued
  game-state payload type.

### Helper Function

`build_game_state_payload(message: dict[str, Any], gsm: dict[str, Any]) -> dict[str, Any]`

Public parser helper imported by `parsers/gre/__init__.py`.

Contract status:

- Accepts an already extracted GRE message dictionary and the selected
  game-state message dictionary.
- Returns a normalized payload dictionary for `GameStateEvent`.
- Does not create an event object.
- Does not inspect raw log text.
- Does not mutate `message` or `gsm`.
- Has no side effects.

Input preconditions:

- `message` must be a dict-like object with `.get()`.
- `gsm` must be a dict-like object with `.get()`.
- Non-dict direct calls are outside the current public contract.
- GRE dispatch filters batch members to dictionaries and only calls this helper
  when the selected game-state message is a dictionary.

Underscored helpers in `game_state.py` are implementation details. Their
behavior is contract-covered through `build_game_state_payload()`, but other
modules should not import them as public API.

## GRE Parser Dispatch Relationship

`src/mythic_edge_parser/parsers/gre/__init__.py` exposes:

`try_parse(entry: LogEntry, timestamp: datetime | None) -> list[GameEvent]`

Game-state dispatch is not owned by `game_state.py`, but this contract depends
on the current relationship:

- The GRE parser marker set includes:
  - `"greToClientEvent"`
  - `"queuedGameStateMessage"`
  - `"GREMessageType_GameStateMessage"`
  - `"GREMessageType_ConnectResp"`
  - `"GameStage_GameOver"`
- `try_parse()` parses the first dict JSON value from the raw body through
  `api_common.parse_json_from_body(body, "gre")`.
- `_extract_gre_messages()` accepts either:
  - a top-level parsed GRE message dict, or
  - `greToClientEvent.greToClientMessages` when it is a list.
- Non-dict entries inside `greToClientMessages` are ignored.
- `_message_game_state()` prefers `message["gameStateMessage"]` when it is a
  dict.
- If current `gameStateMessage` is not a dict, `_message_game_state()` falls
  back to `message["queuedGameStateMessage"]["gameStateMessage"]` when both
  nested layers are dicts.
- `_build_game_state_events()` emits a `GameStateEvent` when the selected game
  state message is a dict.
- If the resulting payload is game-over according to `game_result.is_game_over()`,
  `_build_game_state_events()` appends a paired `GameResultEvent` after the
  `GameStateEvent`.
- Connect-response fallback is skipped when any game-state event was emitted
  for the same message.

Required dispatch guarantee:

- A message with a dict `gameStateMessage` emits a regular or queued
  `GameStateEvent` payload based on the message type value.
- A message without a dict `gameStateMessage` but with a dict
  `queuedGameStateMessage.gameStateMessage` emits a `GameStateEvent`.
- A message with neither selected game-state shape emits no game-state event.
- Game-state emission remains higher precedence than connect-response
  emission for messages that contain both game-state and connect-response
  sections.
- Game-over game-state messages continue to emit `GameStateEvent` first and
  `GameResultEvent` second.

## Inputs

### Raw Log Body For GRE Dispatch

| Input | Type | Source | Required |
| --- | --- | --- | --- |
| `entry.body` | `str` | MTGA log `LogEntry` | Yes |
| `timestamp` | `datetime | None` | router timestamp extraction | No |

Malformed raw dispatch behavior:

- If no GRE marker is present, `gre.try_parse()` returns `[]`.
- If no dict JSON value can be parsed from the body, `gre.try_parse()` returns
  `[]`.
- If `greToClientEvent.greToClientMessages` exists but is not a list,
  `gre.try_parse()` returns `[]`.
- Non-dict members inside a valid `greToClientMessages` list are ignored.

### Regular GRE Game-State Message

Representative raw message input:

```json
{
  "type": "GREMessageType_GameStateMessage",
  "msgId": 7,
  "gameStateId": 42,
  "systemSeatIds": [1],
  "gameStateMessage": {
    "gameInfo": {
      "matchID": "match-42",
      "gameNumber": 2,
      "stage": "GameStage_Play",
      "matchState": "MatchState_GameInProgress"
    },
    "turnInfo": {
      "turnNumber": 3,
      "activePlayer": 2,
      "phase": "Phase_Main1",
      "step": "Step_PreCombatMain"
    },
    "players": [],
    "zones": [],
    "gameObjects": [],
    "annotations": [],
    "persistentAnnotations": [],
    "timers": [],
    "actions": []
  }
}
```

Dispatch passes the full message as `message` and the nested
`gameStateMessage` dict as `gsm`.

### Queued GRE Game-State Message

Representative raw message input:

```json
{
  "type": "GREMessageType_QueuedGameStateMessage",
  "msgId": 5,
  "gameStateId": 9,
  "systemSeatIds": [1],
  "queuedGameStateMessage": {
    "gameStateMessage": {
      "gameInfo": {
        "matchID": "queued-1",
        "gameNumber": 1,
        "stage": "GameStage_Play",
        "matchState": "MatchState_GameInProgress"
      },
      "turnInfo": {
        "turnNumber": 1,
        "activePlayer": 2
      }
    }
  }
}
```

Dispatch passes the full message as `message` and the nested
`queuedGameStateMessage.gameStateMessage` dict as `gsm`.

### Helper Input Fields

Message-level fields:

| Field | Type | Behavior |
| --- | --- | --- |
| `type` | Any | Determines payload type and is copied to `message_type`; missing defaults to `GREMessageType_GameStateMessage`. |
| `msgId` | Any | Copied to `msg_id`; missing defaults to `0`. |
| `gameStateId` | Any | Copied to `game_state_id`; missing defaults to `0`. |
| `systemSeatIds` | list | Normalized to `system_seat_ids` through `api_common.normalize_int_list()`. |

Selected `gsm` fields:

| Field | Type | Behavior |
| --- | --- | --- |
| `gameInfo` | dict | Shallow-copied to `game_info`; non-dict becomes `{}`. |
| `turnInfo` | dict | Consumed through `build_turn_info(gsm)` and carried as `turn_info`; missing/non-dict becomes `{}`. |
| `players` | list | Shallow list copy to `players`; non-list becomes `[]`. |
| `zones` | list | Shallow list copy to `zones`; non-list becomes `[]`. |
| `gameObjects` | list | Shallow list copy to `game_objects`; non-list becomes `[]`. |
| `annotations` | list | Shallow list copy to `annotations`; non-list becomes `[]`. |
| `persistentAnnotations` | list | Shallow list copy to `persistent_annotations`; non-list becomes `[]`. |
| `timers` | list | Shallow list copy to `timers`; non-list becomes `[]`. |
| `actions` | list | Shallow list copy to `actions`; non-list becomes `[]`. |
| `update` | Any | Stringified into `update`; falsey values become `""`. |
| `pendingMessageCount` | Any | Normalized with local `_maybe_int()` into `pending_message_count`. |
| `prevGameStateId` | Any | Normalized with local `_maybe_int()` into `prev_game_state_id`. |
| `diffDeletedInstanceIds` | list | Normalized with `api_common.normalize_int_list()`. |
| `diffDeletedPersistentAnnotationIds` | list | Normalized with `api_common.normalize_int_list()`. |

## Outputs

`build_game_state_payload()` returns:

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `type` | `str` | `"game_state_message"` | `"queued_game_state_message"` only when `message.type` equals `QUEUED_GAME_STATE_MESSAGE_TYPE`. |
| `message_type` | Any | `"GREMessageType_GameStateMessage"` | Raw message type pass-through/default. |
| `msg_id` | Any | `0` | Raw `msgId` pass-through/default. |
| `game_state_id` | Any | `0` | Raw `gameStateId` pass-through/default. |
| `system_seat_ids` | `list[int]` | `[]` | Normalized message-level system seat IDs. |
| `stage` | `str` | `""` | Shortcut from `identity.stage`, sourced from `game_info.stage`. |
| `match_state` | `str` | `""` | `str(game_info.matchState or "")`. |
| `turn_number` | `int | None` | `None` | Shortcut from `turn_info.turn_number`. |
| `active_player_seat_id` | `int | None` | `None` | Shortcut from `turn_info.active_player_seat_id`. |
| `game_info` | `dict[str, Any]` | `{}` | Shallow copy of `gsm.gameInfo`. |
| `turn_info` | `dict[str, Any]` | `{}` | Output from `turn_info.build_turn_info(gsm)`. |
| `identity` | `dict[str, Any]` | keys below | Identity built from `game_info` and `turn_info`. |
| `players` | `list[Any]` | `[]` | Shallow list copy of `gsm.players`. |
| `zones` | `list[Any]` | `[]` | Shallow list copy of `gsm.zones`. |
| `game_objects` | `list[Any]` | `[]` | Shallow list copy of `gsm.gameObjects`. |
| `annotations` | `list[Any]` | `[]` | Shallow list copy of `gsm.annotations`. |
| `persistent_annotations` | `list[Any]` | `[]` | Shallow list copy of `gsm.persistentAnnotations`. |
| `timers` | `list[Any]` | `[]` | Shallow list copy of `gsm.timers`. |
| `actions` | `list[Any]` | `[]` | Shallow list copy of `gsm.actions`. |
| `update` | `str` | `""` | Stringified `gsm.update` when truthy. |
| `pending_message_count` | `int | None` | `None` | Local integer conversion of `pendingMessageCount`. |
| `prev_game_state_id` | `int | None` | `None` | Local integer conversion of `prevGameStateId`. |
| `diff_deleted_instance_ids` | `list[int]` | `[]` | Normalized deleted instance IDs. |
| `diff_deleted_persistent_annotation_ids` | `list[int]` | `[]` | Normalized deleted persistent annotation IDs. |
| `raw_game_state` | `dict[str, Any]` | original `message` | Preserved raw GRE message object. |

### Identity Output

`identity` always has these keys:

| Key | Type | Source/default |
| --- | --- | --- |
| `match_id` | `str` | `str(game_info.matchID or "").strip()` |
| `game_number` | `int | None` | local `_maybe_int(game_info.gameNumber)` |
| `turn_number` | `int | None` | `turn_info.turn_number` |
| `active_player_seat_id` | `int | None` | `turn_info.active_player_seat_id` |
| `phase` | `str` | `turn_info.phase` or `""` |
| `step` | `str` | `turn_info.step` or `""` |
| `stage` | `str` | `str(game_info.stage or "")` |

Observed behavior:

- `identity` does not use parser context. Context fallback is downstream
  extractor/state behavior.
- `identity` does not include `identity_source`; that key is added by
  `app.extractors._hydrate_game_state_identity()` when downstream consumers
  hydrate payload identity.
- Top-level `stage` is the same as `identity.stage`.
- Top-level `match_state` is not part of `identity`.

### Turn-Info Consumption

`game_state.py` calls `turn_info.build_turn_info(gsm)` and carries that returned
dict at `payload["turn_info"]`.

Current consumed/carry-through keys from `turn_info.py`:

- `turn_number`
- `phase`
- `step`
- `active_player_seat_id`
- `decision_player_seat_id`
- `priority_player_seat_id`
- `next_phase`
- `next_step`

`game_state.py` uses only these turn-info keys to build identity and top-level
shortcuts:

- `turn_number`
- `active_player_seat_id`
- `phase`
- `step`

Standalone `turn_info.py` behavior is out of scope except for these
compatibility expectations:

- missing or non-dict `turnInfo` currently yields `{}`.
- `activePlayer` is preferred over `activePlayerSeatId` by `build_turn_info()`.
- turn-info integer fields use `turn_info.py` local `_maybe_int()` behavior.
- turn-info string fields use `str(value or "")`.

## Copy And Default Rules

### Dict Sections

`game_info`:

- If `gsm.gameInfo` is a dict, output `game_info` is `dict(gsm["gameInfo"])`.
- If missing or not a dict, output `game_info` is `{}`.
- The copy is shallow. Nested structures inside `gameInfo` may still alias the
  raw input.

`turn_info`:

- Output is the dict returned by `build_turn_info(gsm)`.
- Missing or non-dict `gsm.turnInfo` currently yields `{}`.
- It is not a raw `turnInfo` dict copy.

`identity`:

- Output is a new dict built from `game_info` and `turn_info`.

### List Sections

List-section outputs use local `_safe_list_copy()`:

- If the source value is a list, output is `list(source)`.
- If missing or not a list, output is `[]`.
- The list copy is shallow.
- Nested dict/list items inside the list may still alias raw input items.
- Non-dict list items are preserved by `game_state.py`; downstream extractor
  helpers filter non-dict list items when they read these sections.

List sections covered by this rule:

- `players`
- `zones`
- `game_objects`
- `annotations`
- `persistent_annotations`
- `timers`
- `actions`

### Raw Payload Preservation

Observed behavior:

- `raw_game_state` is the original `message` object passed to
  `build_game_state_payload()`.
- Focused tests assert identity preservation with `is message`.
- `GameStateEvent` shallow-copies the top-level payload mapping but does not
  deep-copy `raw_game_state`.

Required guarantee:

- `raw_game_state` must preserve the full raw GRE message dictionary for
  diagnostics, replay, queued fallback extraction, local hand extraction, and
  future parser compatibility.
- Current compatibility includes object identity preservation for direct helper
  callers.
- Downstream code must treat `raw_game_state` as read-only evidence. It must
  not mutate the raw object to influence parser truth.

## Integer And String Normalization

### `api_common.normalize_int_list()` Fields

These fields use `api_common.normalize_int_list()`:

- `system_seat_ids`
- `diff_deleted_instance_ids`
- `diff_deleted_persistent_annotation_ids`

Observed behavior:

- Non-list source values normalize to `[]`.
- `int` values are accepted, except `bool` values are skipped.
- String values are stripped and accepted only when `.isdigit()` is true.
- Digit strings become integers.
- Empty strings, non-digit strings, negative-number strings, floats, dicts,
  nested lists, `None`, and booleans are skipped.
- Source order is preserved for accepted values.
- Duplicates are preserved.

### Local `_maybe_int()` Fields

These game-state fields use `game_state.py` local `_maybe_int()`:

- `identity.game_number`
- `pending_message_count`
- `prev_game_state_id`

The carried `turn_info` fields use `turn_info.py` local `_maybe_int()`:

- `turn_number`
- `active_player_seat_id`
- `decision_player_seat_id`
- `priority_player_seat_id`

Observed behavior:

- `_maybe_int(value)` returns `int(value)`.
- It returns `None` only when Python raises `TypeError` or `ValueError`.
- Booleans are accepted by Python `int()` as `1` / `0`.
- Floats are accepted and truncated by Python `int()`.
- Numeric strings accepted by Python `int()` are accepted, including
  whitespace-padded and signed integer strings.
- Non-integer strings such as `"bad"` or `"1.5"` return `None`.

Required guarantee:

- Do not silently align local `_maybe_int()` behavior with
  `api_common.normalize_int_list()` without a new contract, because they
  intentionally differ in current observed behavior.
- Any future bool/float hardening must cover `game_state.py`, `turn_info.py`,
  extractor compatibility, and focused tests together.

### String Fields

Observed behavior:

- `identity.match_id` is `str(game_info.matchID or "").strip()`.
- `identity.stage` and top-level `stage` are `str(game_info.stage or "")`.
- `match_state` is `str(game_info.matchState or "")`.
- `update` is `str(gsm.update or "")`.
- Falsey values such as `0`, `False`, `None`, and `""` become `""` for
  `stage`, `match_state`, and `update`.

## Payload Type Behavior

`_payload_type(message)` returns:

- `"queued_game_state_message"` when
  `message.get("type") == "GREMessageType_QueuedGameStateMessage"`.
- `"game_state_message"` for all other message type values, including missing
  type and malformed type.

Important distinction:

- Payload type is based on the raw message type, not on whether dispatch found
  the selected `gsm` under `gameStateMessage` or
  `queuedGameStateMessage.gameStateMessage`.
- If a future MTGA payload mixes current and queued sections oddly, current
  dispatch still prefers current `gameStateMessage` for `gsm` but payload type
  remains based on `message.type`.

## Emitted Event

When GRE dispatch emits a game-state event, the event is a `GameStateEvent`
from `src/mythic_edge_parser/events.py`.

Observed event properties:

- `kind == "GameState"`.
- `performance_class == PerformanceClass.INTERACTIVE_DISPATCH`.
- `metadata.timestamp` is the timestamp passed to `gre.try_parse()`.
- `metadata.raw_bytes` is `entry.body.encode()`.
- `metadata.raw_bytes_hash` is derived from the full raw log body.
- For batched GRE messages, each emitted event from the same raw log entry
  uses metadata based on the full body.
- For game-over messages, the paired `GameStateEvent` and `GameResultEvent`
  currently share the same `EventMetadata` object.
- `BaseEvent.__post_init__()` shallow-copies the top-level payload mapping.

Required event guarantee:

- Regular and queued game-state payloads must continue to emit as
  `GameStateEvent`.
- Game-over dispatch must continue to emit `GameStateEvent` before
  `GameResultEvent`.
- Parser event classes are out of scope for this contract.

## Malformed Input Behavior

For dict-like `message` and `gsm` inputs, `build_game_state_payload()` must not
raise for:

- missing `message.type`
- missing `msgId`
- missing `gameStateId`
- missing or malformed `systemSeatIds`
- missing or non-dict `gameInfo`
- missing or non-dict `turnInfo`
- missing or non-list list sections
- missing `update`
- missing or invalid string values for `_maybe_int()` fields
- missing or malformed diff-deleted ID lists

Neutral/default values should be used as documented above.

Direct helper calls with non-dict `message` or non-dict `gsm` values are
outside the current public contract.

GRE dispatch malformed behavior:

- No GRE marker: `[]`.
- Unparseable JSON or non-dict first JSON value: `[]`.
- Invalid `greToClientMessages` shape: `[]`.
- Non-dict batch message members: ignored.
- Missing/non-dict `gameStateMessage` and missing/non-dict queued fallback: no
  game-state event.
- Missing/non-dict current `gameStateMessage` with valid queued nested
  game-state message: emit from queued nested payload.
- Game-state message that is not game-over: no `GameResultEvent`.

## Observed Current Behavior

- `build_game_state_payload()` produces stable regular and queued
  `GameStateEvent.payload` field names.
- `message_type`, `msg_id`, and `game_state_id` are pass-through/default
  fields, not scalar-normalized.
- `system_seat_ids` and diff-deleted ID lists use shared integer-list
  normalization that rejects booleans and floats.
- `identity.game_number`, pending count, previous game-state ID, and turn-info
  integer fields use local Python `int()` conversion behavior.
- `game_info` is a shallow dict copy.
- `turn_info` is a normalized dict returned by `turn_info.build_turn_info()`,
  not a raw turn-info copy.
- `identity` is built only from game info and normalized turn-info. It does
  not read downstream context.
- List-section outputs are shallow list copies and preserve non-dict members.
- `raw_game_state` preserves the original raw GRE message object.
- GRE dispatch prefers current `gameStateMessage` over queued nested
  `gameStateMessage`.
- GRE dispatch emits queued payload type only when the raw message type equals
  `GREMessageType_QueuedGameStateMessage`.
- GRE dispatch emits paired `GameStateEvent` / `GameResultEvent` for game-over
  regular and queued game-state messages.

## Required Guarantees

- Keep game-state parsing in the parser layer.
- Keep `build_game_state_payload(message, gsm)` as the public helper API for
  GRE game-state payload construction.
- Keep `QUEUED_GAME_STATE_MESSAGE_TYPE` stable.
- Keep regular and queued game-state payload type strings stable:
  - `game_state_message`
  - `queued_game_state_message`
- Keep output field names stable.
- Keep `raw_game_state` preservation.
- Keep `game_info`, list-section, and raw payload shallow-copy/reference
  semantics unless a new contract intentionally changes them.
- Keep identity and top-level shortcut fields aligned with `game_info` and
  `turn_info` output.
- Keep `turn_info.py` as an adjacent dependency, not part of this standalone
  audit beyond consumed output shape.
- Keep game-over paired emission order compatible with
  `parser_gre_game_result.md`.
- Do not change parser state final reconciliation, workbook schema, webhook
  payload shape, Apps Script behavior, parser event classes, match/game
  identity, deduplication, secrets, raw logs, generated data, runtime status
  files, failed posts, or workbook exports.

## Downstream Consumers

### `game_result.py`

`game_result.is_game_over()` consumes:

- `game_info.stage`
- top-level `stage` fallback

`game_result.build_game_result_payload()` consumes:

- `game_info`
- `identity`
- `game_state_id`
- `message_type`

Compatibility expectations:

- Game-over stage must remain available at `game_info.stage` and top-level
  `stage`.
- `game_info.results` must remain preserved inside `game_info` for game-result
  payload construction.
- `identity`, `game_state_id`, and `message_type` must remain stable.
- Game-state contract must not redefine game-result winner precedence.

### `state.py`

`state._update_match_summary()` consumes all `GameStateEvent` payloads through
extractor helpers.

Compatibility expectations:

- Missing match ID means the event is ignored unless context fallback supplies
  one through extractors.
- `game_info` updates summary MTGA format and queue inputs.
- Local team can be corrected from `system_seat_ids` and `players`.
- Starting player and turn count depend on hydrated turn info.
- Opening-hand evidence depends on local private hand zones and game objects.
- Final reconciliation remains owned by state and is not changed here.

### `extractors.py`

Extractor helpers consume:

- normalized top-level sections
- `raw_game_state.gameStateMessage`
- `raw_game_state.queuedGameStateMessage.gameStateMessage`
- `raw_game_state.systemSeatIds`

Compatibility expectations:

- Normalized top-level fields should remain preferred by extractors.
- Preserved raw payload should remain available for current and queued fallback
  extraction.
- `system_seat_ids` must remain a top-level normalized list.
- `players`, `zones`, `game_objects`, `actions`, and `annotations` must remain
  present as top-level list fields.
- Extractors may filter non-dict list items; game_state.py does not.

### `transforms.py`

Transforms use GameState payloads for inclusion gates, raw/archive rows,
derived serializable identity, turn rows, and summaries.

Compatibility expectations:

- `_extract_turn_info()` must continue to read enough identity and turn data
  from GameState payloads.
- `GameStage_GameOver` game-state rows are skipped by `_game_state_rows()`.
- Turn row dedupe depends on match/game/turn identity.
- This contract does not change workbook row shape, raw row shape, or dedupe
  behavior.

### `gameplay_actions.py`

Gameplay-action observation consumes GameState payloads for:

- match/game identity
- local seat from `system_seat_ids`
- zones
- game objects
- annotations
- actions
- game-state ID
- turn context

Compatibility expectations:

- `game_state_id` or `msg_id` must remain available for gameplay action
  context.
- Zone/object/action/annotation list sections must remain stable.
- Parser-owned game-state truth must not move into gameplay-action derived
  artifacts.

### `runtime_surfaces.py`

Runtime surfaces use GameState payloads for timeline entries, active match
snapshots, and runtime-visible turn/stage summaries.

Compatibility expectations:

- `identity`, `turn_info`, and extractor-readable raw fallback fields must
  remain available.
- Runtime surfaces consume parser-produced values and must not become a raw GRE
  parser.

### `arena_id_validation.py` And `grp_id_candidates.py`

These tools scan saved GameState rows for card and GRP evidence.

Compatibility expectations:

- `raw_game_state` remains available for saved-log replay and fallback scans.
- Normalized and raw payload structures remain compatible with existing
  extractor helpers.
- Generated data and reports are not changed by this contract.

### `runner.py`, `events.py`, And `saved_event_replay.py`

Runner may post full GameState debug rows when configured and writes local
JSONL event records. `events.py` owns event classes and metadata. Saved-event
replay reconstructs `GameStateEvent` from saved rows.

Compatibility expectations:

- `GameStateEvent` event family and metadata behavior remain unchanged.
- `GameStateEvent.payload` remains JSON-serializable when raw payloads are
  serializable.
- This contract does not change runtime status files, local logs, failed
  posts, or workbook exports.

## Ownership Boundaries

Owned by this contract:

- `build_game_state_payload()` helper API.
- Regular versus queued game-state payload type behavior.
- Output field names, defaults, and shallow copy/reference behavior.
- Identity and top-level shortcut construction from game info and turn-info
  output.
- List-section handling.
- Integer normalization differences between shared list normalization and local
  `_maybe_int()` conversion.
- Raw payload preservation.
- GRE dispatch relationship for regular and queued `GameStateEvent` emission.
- Compatibility with paired game-result emission.

Not owned by this contract:

- Standalone `turn_info.py` audit beyond consumed output compatibility.
- GRE game-result winner precedence.
- Connect-response parsing.
- Parser state final reconciliation.
- Extractor fallback implementation beyond compatibility expectations.
- Transform row shape and dedupe.
- Gameplay-action derived artifact design.
- Runtime status files.
- Match identity policy beyond parsed payload fields.
- Game identity policy beyond parsed payload fields.
- Workbook schema.
- Webhook payload shape.
- Apps Script behavior.
- Secrets, environment variables, raw logs, generated data, failed posts, or
  workbook exports.

## Compatibility

Stable compatibility surfaces:

- `QUEUED_GAME_STATE_MESSAGE_TYPE`.
- `build_game_state_payload(message, gsm)`.
- GRE parser import of `build_game_state_payload`.
- Payload type strings:
  - `game_state_message`
  - `queued_game_state_message`
- Payload field names listed in `Outputs`.
- `GameStateEvent` event family and `INTERACTIVE_DISPATCH` performance class.
- Paired `GameStateEvent` before `GameResultEvent` ordering for game-over
  payloads.
- `raw_game_state` identity preservation.
- Top-level `system_seat_ids`, `game_info`, `turn_info`, `identity`, list
  sections, and diff lists.
- Current shallow-copy behavior.

Breaking changes that require a new problem representation or contract:

- Renaming output fields.
- Emitting a different event class.
- Collapsing queued payload type into regular payload type.
- Removing queued nested fallback from GRE dispatch.
- Deep-copying nested list/dict sections as a new guarantee.
- Coercing `msg_id` or `game_state_id`.
- Changing local `_maybe_int()` bool/float behavior.
- Filtering non-dict list-section members inside `game_state.py`.
- Removing `raw_game_state` or changing it from the full raw message object.
- Moving raw GRE game-state interpretation downstream.

## Unknowns

- Whether local `_maybe_int()` should continue accepting booleans and
  truncating floats, or eventually align with `api_common.normalize_int_list()`.
- Whether `msg_id` and `game_state_id` should stay pass-through forever or
  normalize to integers in a future contract.
- Whether list-section non-dict members should continue to be preserved by
  `game_state.py` and filtered only downstream.
- Whether nested list/dict aliasing should remain acceptable or be replaced
  with deeper copy guarantees.
- Whether `queued_game_state_message` should remain first-class in all
  downstream surfaces.
- Which additional turn-info fields should be contracted in the future
  standalone `turn_info.py` audit.
- Whether future MTGA payloads will add new current/queued game-state nesting
  shapes.

## Suspected Gaps

- Focused `game_state.py` tests do not appear to lock bool/float behavior for
  local `_maybe_int()` fields.
- Focused tests do not appear to lock bool/float rejection for
  `system_seat_ids` and diff ID list fields at the game-state layer.
- Focused tests do not appear to assert that non-dict list-section members are
  preserved by `game_state.py`.
- Focused tests do not appear to assert that list-section item dictionaries
  alias raw items while the top-level list is copied.
- Focused tests do not appear to cover a message containing both current
  `gameStateMessage` and queued nested game state where current takes
  precedence.
- Focused tests do not appear to cover missing `message.type` defaulting to
  regular `game_state_message` and `message_type ==
  "GREMessageType_GameStateMessage"`.
- Focused tests do not appear to cover direct malformed diff-list non-list
  values.

## Error Behavior

- Parser dispatch should return `[]` instead of raising for malformed raw GRE
  log bodies and unsupported message shapes.
- Direct helper calls should return neutral defaults instead of raising for
  malformed optional sections on dict-like inputs.
- Non-dict direct helper inputs are outside the current public contract.
- The module should not log, write diagnostics, mutate parser state, post
  webhooks, update workbook rows, write runtime status files, or generate data
  on malformed input.
- Contract ambiguity about turn-info ownership, identity semantics, or
  downstream truth ownership must route back to Codex B rather than being
  implemented silently.

## Side Effects

`build_game_state_payload()` has no side effects.

GRE game-state dispatch side effects are limited to constructing in-memory
event objects. Any later state mutation, local JSONL append, webhook post,
workbook row, runtime status update, timeline write, gameplay-action artifact,
diagnostic artifact, or generated report is owned by downstream modules and is
out of scope for this contract.

## Dependency Order

Implementation threads should evaluate changes in this order:

1. `src/mythic_edge_parser/parsers/gre/game_state.py`
2. `tests/test_gre_game_state_parser.py`
3. `src/mythic_edge_parser/parsers/gre/__init__.py`
4. `tests/test_parsers.py`
5. `src/mythic_edge_parser/parsers/gre/turn_info.py`, only if a consumed
   output boundary issue is proven and routed narrowly
6. `tests/test_gre_turn_info_parser.py`, only for consumed-output compatibility
7. `src/mythic_edge_parser/parsers/gre/game_result.py`, only if paired
   game-over emission compatibility is implicated
8. `src/mythic_edge_parser/app/extractors.py`, only if fallback consumption is
   implicated
9. `src/mythic_edge_parser/app/state.py`, `transforms.py`,
   `gameplay_actions.py`, and `runtime_surfaces.py`, only if focused tests
   prove parser-local work is insufficient

Do not start with workbook, webhook, Apps Script, dashboard, or AI-layer
changes.

## Tests Required

Focused tests expected for Module Implementer or Module Fixer:

- Helper happy path:
  - regular `message.type` emits `type == "game_state_message"`
  - queued message type emits `type == "queued_game_state_message"`
  - `message_type`, `msg_id`, and `game_state_id` pass through/default as
    documented
  - `system_seat_ids` normalizes through `api_common.normalize_int_list()`
  - `game_info`, `turn_info`, `identity`, top-level `stage`, `match_state`,
    `turn_number`, and `active_player_seat_id` align
  - list sections are shallow list copies
  - `raw_game_state is message`
- Defaults and malformed sections:
  - missing/non-dict `gameInfo` yields `{}` and neutral identity/stage/match
    state fields
  - missing/non-dict `turnInfo` yields `{}` and neutral turn shortcuts
  - non-list list sections yield `[]`
  - missing `message.type` defaults to regular payload type and default
    message type
  - missing `msgId` and `gameStateId` default to `0`
  - missing or non-list diff ID lists become `[]`
- Integer behavior:
  - `system_seat_ids` and diff lists accept ints and digit strings
  - `system_seat_ids` and diff lists skip booleans, floats, non-digit strings,
    and non-list values
  - local `_maybe_int()` fields document/lock current bool and float behavior
    if implementer touches integer conversion
  - signed or whitespace-padded integer strings for local `_maybe_int()` fields
    follow Python `int()` behavior
- List-section behavior:
  - top-level list copy mutation does not mutate raw list length
  - nested item mutation aliasing remains understood or explicitly changed by
    a new contract
  - non-dict list members are preserved by `game_state.py`
- Dispatch:
  - regular `gameStateMessage` emits one `GameStateEvent`
  - queued nested `gameStateMessage` emits one `GameStateEvent`
  - current `gameStateMessage` takes precedence over queued nested message
  - non-dict batch messages are ignored
  - invalid `greToClientMessages` shape emits no game-state event
  - missing/non-dict selected game-state messages emit no game-state event
  - game-state payload takes precedence over connect response on same message
  - game-over regular and queued messages emit `GameStateEvent` then
    `GameResultEvent`
  - emitted metadata uses the full raw body bytes and dispatch timestamp
- Downstream compatibility:
  - extractor tests continue proving top-level/current-raw/queued-raw fallback
  - state tests continue proving context fallback, local team correction,
    starting player, turn count, and opening-hand behavior
  - transform tests continue proving turn row inclusion/dedupe and derived
    identity serialization
  - gameplay-action tests continue consuming zones, objects, actions, and
    annotations
  - runtime and candidate/regression tests continue consuming parser-produced
    game-state payloads without raw GRE truth moving downstream

Suggested focused validation:

```bash
python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_turn_info_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py
python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
python3 -m ruff check src tests
```

Before submitter work, run or verify:

```bash
python3 -m pytest -q
python3 -m ruff check src tests
```

Documentation-only validation for this contract:

```bash
git diff --check
```

## Acceptance Criteria

- `docs/contracts/parser_gre_game_state.md` exists and links issue #26,
  tracker #5, the agent constitution, module contract role doc, module
  contract template, and adjacent contracts.
- The contract clearly names parser and state interpretation as the truth
  layer.
- The contract clearly names owned files and related consumer files.
- The public helper API and queued-message constant are documented.
- GRE parser dispatch behavior for regular and queued game-state messages is
  documented.
- Accepted raw message and selected `gsm` input shapes are documented.
- Output fields, default values, and type/shape expectations are documented.
- Identity and turn-info consumption are documented without completing the
  standalone `turn_info.py` audit.
- Copy/default, list-section, integer-normalization, and raw payload
  preservation rules are documented.
- Malformed input behavior and no-side-effect expectations are documented.
- Downstream consumers and ownership boundaries are documented without moving
  truth downstream.
- Focused test obligations and validation commands are listed.
- The handoff routes to Codex C: Module Implementer unless contract review
  finds a framing problem.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex C: Module Implementer for issue #26 and docs/contracts/parser_gre_game_state.md.

Goal:
Compare the current GRE game-state parser implementation and focused tests against the GRE game-state module contract. Implement only the smallest coherent code and test changes needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/26
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/parser_gre_game_state.md
- docs/contracts/parser_state.md
- docs/contracts/parser_extractors.md
- docs/contracts/parser_gre_game_result.md
- docs/contracts/parser_gre_connect_resp.md
- src/mythic_edge_parser/parsers/gre/game_state.py
- src/mythic_edge_parser/parsers/gre/turn_info.py
- src/mythic_edge_parser/parsers/gre/__init__.py
- src/mythic_edge_parser/parsers/gre/game_result.py
- src/mythic_edge_parser/parsers/api_common.py
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/extractors.py
- src/mythic_edge_parser/app/transforms.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- tests/test_gre_game_state_parser.py
- tests/test_gre_turn_info_parser.py
- tests/test_parsers.py
- tests/test_gre_game_result_parser.py
- tests/test_state.py
- tests/test_app_extractors.py
- tests/test_gameplay_actions.py
- tests/test_transforms.py
- tests/test_runtime_surfaces.py
- tests/test_grp_id_candidates.py
- tests/test_parser_regressions.py

Do:
- Compare observed code behavior against the contract before editing.
- Preserve parser-owned truth boundaries.
- Add focused tests for contracted parser behavior not currently covered.
- Keep behavior changes minimal and parser-local unless the contract explicitly requires a downstream update.
- Produce docs/implementation_handoffs/parser_gre_game_state_comparison.md with the comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Move parser-owned game-state truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation.
- Expand into the standalone turn_info.py audit unless a boundary conflict must be routed.
- Target main; module PR work belongs on codex/parser-module-audit-suite.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/26"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_gre_game_state.md"
  target_artifact: "docs/implementation_handoffs/parser_gre_game_state_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned game-state truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not expand into the standalone turn_info.py audit unless a boundary conflict must be routed."
    - "Do not target main for module PR work."
```

## Handoff Packet

Role performed: Codex B, Module Contract Writer.

Source problem representation: GitHub issue #26, tracked by parser module
audit tracker #5.

Contract produced: `docs/contracts/parser_gre_game_state.md`

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/5

Risk tier: High.

Owning truth layer: parser and state interpretation.

Public interface:

- `QUEUED_GAME_STATE_MESSAGE_TYPE`
- `build_game_state_payload(message: dict[str, Any], gsm: dict[str, Any]) -> dict[str, Any]`
- GRE dispatch through `parsers/gre/__init__.py`
- emitted `GameStateEvent.payload` fields documented above

Invariants:

- Regular game-state dispatch emits `GameStateEvent`.
- Queued game-state dispatch emits `GameStateEvent` with
  `type == "queued_game_state_message"`.
- Game-over game-state dispatch emits `GameStateEvent` before
  `GameResultEvent`.
- Output field names remain stable.
- `system_seat_ids` and diff ID fields are normalized lists.
- `game_info`, list sections, and raw payload preservation follow the
  documented shallow-copy/reference rules.
- `raw_game_state` preserves the raw message object.
- The helper has no side effects.

Required tests: focused helper, dispatch, identity/turn-info consumption,
copy/default, list-section, integer-normalization, raw payload preservation,
malformed-input, and downstream compatibility obligations listed in
`Tests Required`.

Acceptance criteria: listed above.

Open questions or contract risks:

- Local `_maybe_int()` accepts bools and truncates floats while shared
  integer-list normalization rejects them.
- `msg_id` and `game_state_id` remain pass-through values.
- List-section item dictionaries currently alias raw items.
- Non-dict list-section members are preserved by `game_state.py`.
- `turn_info.py` still needs a future standalone audit.
- Future MTGA payload-shape drift may add new current/queued nesting forms.

Next recommended thread role: Codex C, Module Implementer.
