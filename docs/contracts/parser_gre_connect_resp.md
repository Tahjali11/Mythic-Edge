# GRE Connect Response Parser Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/22

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Adjacent contracts:

- `docs/contracts/parser_state.md`
- `docs/contracts/parser_extractors.md`
- `docs/contracts/parser_client_actions.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the parser-owned GRE connect-response helper in
`src/mythic_edge_parser/parsers/gre/connect_resp.py` and its dispatch
relationship with `src/mythic_edge_parser/parsers/gre/__init__.py`. It is a
contract artifact only. It does not implement code or change parser behavior.

## Module

`src/mythic_edge_parser/parsers/gre/connect_resp.py`

The module normalizes raw GRE `GREMessageType_ConnectResp` message dictionaries
into `GameStateEvent.payload` dictionaries with parser-owned connect-response
facts.

## Owning Layer

Parser and state interpretation.

`connect_resp.py` owns normalized GRE connect-response fields derived from raw
GRE messages:

- connect-response payload type
- message type
- message ID
- game-state ID
- local/system seat IDs
- submitted deck and sideboard card IDs visible in `connectResp.deckMessage`
- connect-response settings
- preserved raw GRE connect-response message

It does not own live match/game summary mutation, final match reconciliation,
client-action submit-deck interpretation, active submitted deck persistence,
runtime status writes, workbook row shape, webhook transport, Apps Script
behavior, dashboard formulas, match identity, game identity, or deduplication.

Parser truth boundary:

- `connect_resp.py` owns conversion from an already extracted raw GRE message
  dict to a normalized `connect_resp` payload.
- `parsers/gre/__init__.py` owns extracting GRE message dictionaries from a raw
  log body and deciding whether a connect-response message emits a
  `GameStateEvent`.
- `src/mythic_edge_parser/events.py` owns `GameStateEvent` metadata and
  top-level payload copying.
- `src/mythic_edge_parser/app/state.py` may consume emitted `GameStateEvent`
  payloads in parser state, but it must not reinterpret raw GRE
  connect-response dictionaries as a separate truth source.
- `src/mythic_edge_parser/app/extractors.py` may read normalized
  `system_seat_ids` from connect-response events when those events flow through
  generic game-state helpers.
- Runtime surfaces, diagnostics, gameplay-action helpers, GRP candidate tools,
  workbook formulas, webhook transport, Apps Script, dashboard logic, and AI
  analysis must consume parser-produced fields rather than owning raw GRE
  connect-response parsing.

## Files Owned By This Contract

- `src/mythic_edge_parser/parsers/gre/connect_resp.py`
- `tests/test_gre_connect_resp_parser.py`
- `docs/contracts/parser_gre_connect_resp.md`

Related files whose behavior is referenced but not owned by this contract:

- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/api_common.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- `src/mythic_edge_parser/app/grp_id_candidates.py`
- `tests/test_parsers.py`
- `tests/test_gre_game_state_parser.py`
- `tests/test_state.py`
- `tests/test_app_extractors.py`
- `tests/test_gameplay_actions.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_grp_id_candidates.py`
- `tests/test_parser_regressions.py`

## Public Interface

### Helper Function

`build_connect_resp_payload(message: dict[str, Any]) -> dict[str, Any]`

Public parser helper imported by `parsers/gre/__init__.py`.

Contract status:

- Accepts an already extracted GRE message dictionary.
- Returns a normalized payload dictionary.
- Does not create an event object.
- Does not inspect raw log text.
- Does not mutate `message`.
- Does not write files, post webhooks, update state, update workbook rows, or
  emit diagnostics.

Input precondition:

- `message` must be a dict-like object with `.get()`.
- The helper is not currently required to tolerate non-dict direct calls.
- GRE dispatch filters batch members to dictionaries before calling the helper.

Underscored helpers in `connect_resp.py` are implementation details. Their
behavior is contract-covered through `build_connect_resp_payload()`, but other
modules should not import them as public API.

### GRE Parser Entrypoint Relationship

`src/mythic_edge_parser/parsers/gre/__init__.py` exposes:

`try_parse(entry: LogEntry, timestamp: datetime | None) -> list[GameEvent]`

Connect-response dispatch is not owned by `connect_resp.py`, but this contract
depends on the current relationship:

- The GRE parser marker set includes `"GREMessageType_ConnectResp"`.
- `try_parse()` parses the first dict JSON value from the raw body through
  `api_common.parse_json_from_body(body, "gre")`.
- `_extract_gre_messages()` accepts either:
  - a top-level parsed GRE message dict, or
  - `greToClientEvent.greToClientMessages` when it is a list.
- Non-dict entries inside `greToClientMessages` are ignored.
- For each message dict, GRE game-state parsing is attempted before
  connect-response parsing.
- A connect-response event is emitted only when no game-state event was emitted
  for that same message and `message.get("connectResp")` is a dict.

Required dispatch guarantee:

- A raw GRE connect-response message with a dictionary `connectResp` must emit
  exactly one `GameStateEvent` payload built by `build_connect_resp_payload()`,
  unless the same message is treated as a GRE game-state message first.
- A raw GRE message with missing or non-dict `connectResp` must not emit a
  connect-response `GameStateEvent` through GRE dispatch.

## Inputs

### Raw Log Body For GRE Dispatch

| Input | Type | Source | Required |
| --- | --- | --- | --- |
| `entry.body` | `str` | MTGA log `LogEntry` | Yes |
| `timestamp` | `datetime | None` | router timestamp extraction | No |

The GRE parser currently considers a body parseable when it contains at least
one marker from its marker tuple, including `"GREMessageType_ConnectResp"`.
Marker detection is substring-based over the raw body.

Malformed raw bodies:

- If no GRE marker is present, `try_parse()` returns `[]`.
- If no dict JSON value can be parsed from the body, `try_parse()` returns
  `[]`.
- If a GRE batch has no dict message objects, `try_parse()` returns `[]`.

### Accepted Message Shapes

#### Direct GRE Message

```json
{
  "type": "GREMessageType_ConnectResp",
  "msgId": 1,
  "gameStateId": 4,
  "systemSeatIds": [1, 2],
  "connectResp": {
    "deckMessage": {
      "deckCards": [11, 12],
      "sideboardCards": [21]
    },
    "settings": {
      "matchClockSec": 1800
    }
  }
}
```

#### GRE Batch Message

```json
{
  "greToClientEvent": {
    "greToClientMessages": [
      {
        "type": "GREMessageType_ConnectResp",
        "msgId": 1,
        "gameStateId": 4,
        "systemSeatIds": [1, 2],
        "connectResp": {
          "deckMessage": {
            "deckCards": [11, 12],
            "sideboardCards": [21]
          },
          "settings": {
            "matchClockSec": 1800
          }
        }
      }
    ]
  }
}
```

### Message Fields

| Field | Type | Behavior |
| --- | --- | --- |
| `type` | Any | Copied to `message_type`; defaults to `GREMessageType_ConnectResp`. |
| `msgId` | Any | Copied to `msg_id`; defaults to `0`. |
| `gameStateId` | Any | Copied to `game_state_id`; defaults to `0`. |
| `systemSeatIds` | list | Normalized into `system_seat_ids` through `api_common.normalize_int_list()`. |
| `connectResp` | dict | Required by GRE dispatch for event emission; optional for direct helper tolerance. |
| `connectResp.deckMessage` | dict | Source for deck and sideboard card IDs. |
| `connectResp.deckMessage.deckCards` | list | Normalized into `deck_cards`. |
| `connectResp.deckMessage.sideboardCards` | list | Normalized into `sideboard_cards`. |
| `connectResp.settings` | dict | Shallow-copied into `settings`. |

Observed direct-helper tolerance:

- If `connectResp` is missing or not a dict, the helper treats it as `{}`.
- If `connectResp.deckMessage` is missing or not a dict, deck lists default to
  `[]`.
- If `connectResp.settings` is missing or not a dict, settings default to `{}`.

Required dispatch distinction:

- Direct helper tolerance for malformed `connectResp` does not mean GRE
  dispatch emits malformed connect-response messages. Dispatch must still
  require `connectResp` to be a dict before emitting a `GameStateEvent`.

## Outputs

### Helper Payload

`build_connect_resp_payload()` returns:

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `type` | `str` | `"connect_resp"` | Stable parser event type for GRE connect responses. |
| `message_type` | Any | `"GREMessageType_ConnectResp"` | Raw GRE message type value. |
| `msg_id` | Any | `0` | Raw `msgId` pass-through value. |
| `game_state_id` | Any | `0` | Raw `gameStateId` pass-through value. |
| `system_seat_ids` | `list[int]` | `[]` | Normalized top-level `systemSeatIds`. |
| `deck_cards` | `list[int]` | `[]` | Normalized `connectResp.deckMessage.deckCards`. |
| `sideboard_cards` | `list[int]` | `[]` | Normalized `connectResp.deckMessage.sideboardCards`. |
| `settings` | `dict[str, Any]` | `{}` | Shallow copy of `connectResp.settings`. |
| `raw_connect_resp` | `dict[str, Any]` | original `message` | Preserved raw GRE message object. |

### Emitted Event

When GRE dispatch emits a connect-response event, the event is a
`GameStateEvent` from `src/mythic_edge_parser/events.py`.

Observed event properties:

- `kind == "GameState"`.
- `performance_class == PerformanceClass.INTERACTIVE_DISPATCH`.
- `metadata.timestamp` is the timestamp passed to `gre.try_parse()`.
- `metadata.raw_bytes` is `entry.body.encode()`.
- `metadata.raw_bytes_hash` is derived from the full raw log body.
- For batched GRE messages, each emitted event from the same raw log entry
  shares metadata based on the full body.
- `BaseEvent.__post_init__()` shallow-copies the top-level payload mapping.

Required event guarantee:

- The emitted payload type must remain `"connect_resp"`.
- The event family must remain `GameState` unless a new problem
  representation and contract intentionally migrate connect responses to a new
  event class.
- The payload field names above must remain stable for compatibility.

## Normalization And Defaults

### Integer List Normalization

`system_seat_ids`, `deck_cards`, and `sideboard_cards` use
`api_common.normalize_int_list()`.

Observed behavior:

- Non-list source values normalize to `[]`.
- `int` values are accepted, except `bool` values are skipped.
- String values are stripped and accepted only when `.isdigit()` is true.
- Digit strings become integers.
- Empty strings, non-digit strings, negative-number strings, floats, dicts,
  nested lists, `None`, and booleans are skipped.
- Source order is preserved for accepted values.
- Duplicates are preserved.

Required guarantee:

- These three output fields must always be lists.
- Malformed list members must not raise.
- Downstream consumers must not receive raw card-ID or seat-ID lists in these
  normalized fields.

### Pass-Through Scalar Fields

Observed behavior:

- `message_type` is `message.get("type", "GREMessageType_ConnectResp")`.
- `msg_id` is `message.get("msgId", 0)`.
- `game_state_id` is `message.get("gameStateId", 0)`.
- These fields are not coerced to integers or strings.
- String IDs remain strings.
- Malformed scalar values are preserved as provided.

Required guarantee:

- Do not silently add coercion for `msg_id` or `game_state_id` without focused
  compatibility tests, because current tests document pass-through behavior.

### Settings Copy

Observed behavior:

- If `connectResp.settings` is a dict, `settings` is `dict(settings)`.
- The copy is shallow.
- Mutating a top-level key in normalized `payload["settings"]` does not mutate
  the raw `message["connectResp"]["settings"]`.
- Nested dicts and lists inside settings may still alias the raw payload.
- Non-dict or missing settings become `{}`.

Required guarantee:

- The top-level settings mapping must remain isolated from the raw settings
  mapping.
- The contract currently requires only a shallow copy. A future deep-copy
  requirement would be a behavior change and must be covered by a new
  implementation/review pass.

### Raw Payload Preservation

Observed behavior:

- `raw_connect_resp` is the original `message` object passed to
  `build_connect_resp_payload()`.
- Focused tests assert identity preservation with `is message`.
- `GameStateEvent` shallow-copies the top-level payload dict but does not deep
  copy `raw_connect_resp`.

Required guarantee:

- `raw_connect_resp` must preserve the original raw GRE message dictionary for
  diagnostics, replay, and future extractor fallbacks.
- Current compatibility includes object identity preservation for direct helper
  callers.
- Downstream code must treat `raw_connect_resp` as read-only diagnostic
  evidence. It must not mutate the raw object to influence parser truth.

## Malformed Input Behavior

### Direct Helper Calls

For dict `message` inputs, `build_connect_resp_payload()` must not raise for:

- missing `type`
- missing `msgId`
- missing `gameStateId`
- missing or malformed `systemSeatIds`
- missing or malformed `connectResp`
- missing or malformed `connectResp.deckMessage`
- missing or malformed deck-card lists
- missing or malformed sideboard-card lists
- missing or malformed `connectResp.settings`

Neutral/default values should be used as documented above.

Direct helper calls with non-dict `message` values are outside the current
public contract.

### GRE Dispatch

`gre.try_parse()` must not raise for:

- bodies with no GRE marker
- bodies whose first JSON value is missing or not a dict
- GRE batches whose `greToClientMessages` value is not a list
- GRE batches with non-dict message members
- connect-response-looking messages with non-dict `connectResp`
- connect-response messages with malformed optional nested sections

Required no-event cases:

- No marker: `[]`.
- Unparseable JSON: `[]`.
- No dict GRE message candidate: `[]`.
- Missing or non-dict `connectResp`: no connect-response event.

Required event case:

- Dictionary GRE message with dictionary `connectResp`: one connect-response
  `GameStateEvent`, unless GRE game-state handling emitted an event for the
  same message first.

## Observed Current Behavior

- `build_connect_resp_payload()` returns a payload even when
  `message["connectResp"]` is missing or malformed.
- GRE dispatch emits connect responses only when `message.get("connectResp")`
  is a dict.
- GRE dispatch gives game-state messages precedence over connect-response
  messages in `_emit_message_events()`.
- `message_type`, `msg_id`, and `game_state_id` are pass-through/default
  fields, not normalized scalars.
- `system_seat_ids`, `deck_cards`, and `sideboard_cards` are normalized lists
  using shared API helper behavior.
- `settings` is shallow-copied.
- `raw_connect_resp` preserves the original message object by identity.
- Connect-response events are emitted as `GameStateEvent`, even though their
  payload type is `"connect_resp"`.
- Connect-response payloads do not include `identity`, `game_info`,
  `turn_info`, `players`, `zones`, `game_objects`, `actions`, or
  `annotations` unless future behavior intentionally adds them.
- Current state/runtime consumers generally treat connect-response events as
  generic `GameState` payloads. Because connect-response payloads usually lack
  match/game identity and turn information, they are often ignored by
  state, gameplay-action, and sheet-row inclusion paths unless parser context
  supplies enough identity for a generic consumer.

## Required Guarantees

- Keep connect-response parsing in the parser layer.
- Keep the helper public API and payload field names stable.
- Keep GRE dispatch gated on dictionary `connectResp` for emitted
  connect-response events.
- Keep emitted connect-response events as `GameStateEvent` unless a new
  contract migrates the event family.
- Preserve raw GRE message evidence in `raw_connect_resp`.
- Preserve top-level settings isolation with a shallow copy.
- Preserve no-raise behavior for malformed optional nested sections.
- Preserve neutral defaults for missing optional sections.
- Preserve pass-through/default behavior for `message_type`, `msg_id`, and
  `game_state_id`.
- Preserve normalized list behavior for `system_seat_ids`, `deck_cards`, and
  `sideboard_cards`.
- Do not treat connect-response deck evidence as equivalent to
  `ClientAction` `submit_deck_resp` without a new contract that covers runtime
  surfaces, diagnostics, GRP candidate tooling, and workbook-visible behavior.
- Do not move GRE connect-response truth into workbook formulas, dashboard
  logic, Apps Script, webhook transport, or AI interpretation.

## Downstream Consumers

### `state.py`

`state._update_match_summary()` consumes all `GameStateEvent` payloads through
generic game-state handling.

Compatibility expectations:

- Connect-response payloads must be safe for generic game-state extraction.
- Missing game identity must not raise.
- If no current match ID can be derived from payload or parser context, state
  ignores the event.
- `connect_resp` currently does not directly mark submit-deck state or active
  deck state.

### `extractors.py`

`_game_state_system_seat_ids()` reads normalized top-level `system_seat_ids`
when present and falls back to `raw_game_state.systemSeatIds` for game-state
payloads.

Compatibility expectations:

- Connect-response payloads should keep `system_seat_ids` as a top-level list
  of normalized ints.
- Connect-response payloads currently preserve raw data under
  `raw_connect_resp`, not `raw_game_state`; extractor fallback behavior must
  not be assumed for connect-response raw payloads unless a future contract
  changes extractor behavior.

### `gameplay_actions.py`

Gameplay-action observation consumes `GameStateEvent` payloads only when a
match ID and game number can be hydrated.

Compatibility expectations:

- Connect-response events should not require gameplay-action helpers to parse
  raw GRE connect-response payloads.
- If context supplies identity, normalized `system_seat_ids` may update local
  seat tracking, but connect-response events do not provide zones, objects, or
  actions.

### `transforms.py`

`include_event()` handles `GameStateEvent` through generic game-state inclusion
logic. `summarize()` summarizes connect-response events as generic GameState
events through `_extract_turn_info()`.

Compatibility expectations:

- Connect-response events should remain serializable through `to_serializable()`.
- Connect-response payloads should not force raw sheet-row inclusion unless
  the existing transform gates include them.
- This contract does not change workbook row shape or event inclusion gates.

### `runtime_surfaces.py` And `analytics_sidecar.py`

Runtime surfaces observe `GameStateEvent` payloads for timelines and active
match snapshots. Analytics sidecar posts deck snapshot rows from
`ClientAction submit_deck_resp`, not from GRE `connect_resp`.

Compatibility expectations:

- Connect-response deck evidence remains separate parser evidence.
- Runtime active submitted deck behavior must not change in this contract.
- Connect-response events should not be promoted to deck snapshot posts without
  a new downstream contract.

### `diagnostics.py`

Diagnostics currently records active submitted deck payloads from
`ClientAction submit_deck_resp` through runner-side handling, not from GRE
connect-response events.

Compatibility expectations:

- Connect-response `deck_cards` and `sideboard_cards` must not silently become
  active submitted deck writes in this contract.
- If future work uses connect-response deck evidence as fallback submitted-deck
  evidence, it must explicitly cover diagnostics payload shape and runtime
  status effects.

### `grp_id_candidates.py`

GRP candidate tooling currently scans saved `ClientAction submit_deck_resp`
payloads and active submitted deck artifacts for submitted-deck evidence.

Compatibility expectations:

- Connect-response deck fields must remain available as parser evidence, but
  current GRP candidate behavior is not changed by this contract.
- Future fallback use of connect-response deck lists must be explicitly
  contracted and tested.

## Ownership Boundaries

Owned by this contract:

- GRE connect-response helper API.
- Normalized connect-response payload field names and defaults.
- Raw connect-response preservation.
- Settings shallow-copy behavior.
- Malformed optional nested section behavior.
- GRE dispatch relationship for connect-response event emission.

Not owned by this contract:

- GRE game-state payload contract.
- GRE game-result contract.
- Client-action submit-deck behavior.
- Parser state final reconciliation.
- Extractor fallback behavior beyond compatibility expectations named here.
- Runtime deck snapshot writes.
- Workbook schema.
- Webhook payload shape.
- Apps Script behavior.
- Dashboard formulas.
- Match identity.
- Game identity.
- Deduplication.
- Secrets, environment variables, raw logs, generated data, runtime status
  files, failed posts, or workbook exports.

## Compatibility

Stable compatibility surfaces:

- `build_connect_resp_payload(message)`.
- GRE parser import of `build_connect_resp_payload`.
- Payload type string `"connect_resp"`.
- Output fields:
  - `message_type`
  - `msg_id`
  - `game_state_id`
  - `system_seat_ids`
  - `deck_cards`
  - `sideboard_cards`
  - `settings`
  - `raw_connect_resp`
- `GameStateEvent` event family for emitted connect-response events.
- Shallow settings copy.
- Raw message identity preservation.
- Neutral defaults for malformed nested sections.

Breaking changes that require a new problem representation or contract:

- Renaming output fields.
- Changing `connect_resp` payload type.
- Emitting a different event class.
- Requiring non-dict nested optional sections to raise.
- Deep-copying `raw_connect_resp` instead of preserving identity.
- Coercing `msg_id` or `game_state_id`.
- Treating GRE connect-response deck evidence as active submitted-deck truth.
- Moving connect-response parsing or fallback interpretation downstream.

## Unknowns

- Whether MTGA may emit additional connect-response deck-message shapes beyond
  `connectResp.deckMessage.deckCards` and `sideboardCards`.
- Whether connect-response deck evidence should eventually become fallback
  evidence for active submitted deck diagnostics.
- Whether nested settings structures should remain shallow-copied forever or
  become deep-copied for mutation isolation.
- Whether future extractor behavior should read `raw_connect_resp.systemSeatIds`
  as a fallback the same way it reads `raw_game_state.systemSeatIds`.
- Whether future GRE batches can contain a message with both a valid
  game-state message and a valid connect response that should emit both event
  types.

## Suspected Gaps

- Focused tests cover shallow settings copy but not nested settings aliasing.
- Focused tests cover malformed `deckMessage` and `settings`, but list
  normalization edge cases for bools, floats, non-list values, and negative
  strings may need explicit connect-response tests.
- GRE dispatch tests cover connect-response emission and ignored non-dict batch
  members, but may not explicitly cover missing/non-dict `connectResp` as a
  no-event case.
- Tests may not explicitly lock game-state precedence when a message contains
  both game-state and connect-response sections.
- Tests may not explicitly lock the direct-helper versus GRE-dispatch
  distinction for malformed `connectResp`.
- Downstream tests do not appear to assert that connect-response deck evidence
  does not update active submitted deck artifacts.

## Error Behavior

- Parser dispatch should return `[]` instead of raising for malformed raw GRE
  log bodies and unsupported message shapes.
- Direct helper calls should return neutral defaults instead of raising for
  malformed optional nested sections on dict inputs.
- The module should not log, write diagnostics, mutate runtime state, post
  webhooks, or update workbook rows on malformed input.
- Contract ambiguity about downstream deck evidence must route back to Codex B
  rather than being implemented silently.

## Side Effects

`build_connect_resp_payload()` has no side effects.

GRE connect-response dispatch side effects are limited to constructing
in-memory `GameStateEvent` objects. Any later state mutation, file write,
webhook post, workbook row, runtime status update, timeline write, or
diagnostic artifact is owned by downstream modules and is out of scope for this
contract.

## Dependency Order

Implementation threads should evaluate changes in this order:

1. `src/mythic_edge_parser/parsers/gre/connect_resp.py`
2. `tests/test_gre_connect_resp_parser.py`
3. `src/mythic_edge_parser/parsers/gre/__init__.py`
4. `tests/test_parsers.py`
5. `src/mythic_edge_parser/parsers/api_common.py`, only if normalization
   behavior is implicated
6. `src/mythic_edge_parser/events.py`, only if event emission shape is
   implicated
7. Downstream consumers only when focused tests prove the contract cannot be
   satisfied parser-locally

Do not start with workbook, webhook, Apps Script, dashboard, or AI-layer
changes.

## Tests Required

Focused tests expected for Module Implementer or Module Fixer:

- Helper happy path:
  - `type == "connect_resp"`
  - pass-through `message_type`
  - pass-through `msg_id`
  - pass-through `game_state_id`
  - normalized `system_seat_ids`
  - normalized `deck_cards`
  - normalized `sideboard_cards`
  - shallow-copied `settings`
  - identity-preserved `raw_connect_resp`
- Helper defaults:
  - missing `type` defaults to `GREMessageType_ConnectResp`
  - missing `msgId` defaults to `0`
  - missing `gameStateId` defaults to `0`
  - missing `systemSeatIds` defaults to `[]`
  - missing or malformed `connectResp` yields neutral nested fields on direct
    helper calls
  - missing or malformed `deckMessage` yields empty deck lists
  - missing or malformed `settings` yields `{}`
- Normalization edge cases:
  - digit strings accepted
  - bools skipped
  - floats skipped
  - non-digit strings skipped
  - non-list sources become `[]`
  - order and duplicates preserved for accepted list members
- GRE dispatch:
  - connect-response in `greToClientMessages` emits one `GameStateEvent`
  - direct top-level connect-response dict emits one `GameStateEvent`
  - non-dict messages inside a GRE batch are ignored
  - invalid `greToClientMessages` shape emits no connect-response event
  - missing/non-dict `connectResp` emits no connect-response event
  - game-state handling takes precedence when applicable
  - event metadata uses the raw body bytes
- Downstream contract checks:
  - `state.py` and extractor helpers tolerate `connect_resp` payloads without
    identity, game info, turn info, players, zones, objects, actions, or
    annotations
  - connect-response deck evidence is not silently treated as
    `ClientAction submit_deck_resp`
  - runtime active submitted deck behavior remains unchanged unless a future
    contract explicitly changes it

Suggested focused validation:

```bash
python3 -m pytest -q tests/test_gre_connect_resp_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py
python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
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

- `docs/contracts/parser_gre_connect_resp.md` exists and links issue #22,
  tracker #5, the agent constitution, the module contract role doc, and the
  module contract template.
- The contract clearly names the parser/state layer as truth owner.
- The contract clearly names owned files and related consumer files.
- The helper public API is documented.
- GRE parser dispatch behavior is documented separately from direct helper
  behavior.
- Accepted raw payload shapes and malformed input behavior are documented.
- Output fields, defaults, pass-through behavior, and list normalization rules
  are documented.
- Raw payload preservation and settings shallow-copy behavior are documented.
- Downstream consumers and ownership boundaries are documented without moving
  truth downstream.
- Focused test obligations and validation commands are listed.
- The handoff routes to Codex C: Module Implementer unless contract review
  finds a framing problem.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex C: Module Implementer for issue #22 and docs/contracts/parser_gre_connect_resp.md.

Goal:
Compare the current GRE connect-response parser implementation and focused tests against the GRE connect-response module contract. Implement only the smallest coherent code and test changes needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/22
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/parser_gre_connect_resp.md
- src/mythic_edge_parser/parsers/gre/connect_resp.py
- src/mythic_edge_parser/parsers/gre/__init__.py
- src/mythic_edge_parser/parsers/api_common.py
- src/mythic_edge_parser/events.py
- tests/test_gre_connect_resp_parser.py
- tests/test_parsers.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/extractors.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/grp_id_candidates.py
- docs/contracts/parser_state.md
- docs/contracts/parser_extractors.md
- docs/contracts/parser_client_actions.md

Do:
- Compare observed code behavior against the contract before editing.
- Preserve parser-owned truth boundaries.
- Add focused tests for contracted parser behavior not currently covered.
- Keep behavior changes minimal and parser-local unless the contract explicitly requires a downstream update.
- Produce docs/implementation_handoffs/parser_gre_connect_resp_comparison.md with the comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser state, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, final reconciliation, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Move parser-owned GRE connect-response truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation.
- Treat GRE connect-response deck evidence as active submitted-deck truth unless the contract and focused tests explicitly require it.
- Target main; module PR work belongs on codex/parser-module-audit-suite.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/22"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_gre_connect_resp.md"
  target_artifact: "docs/implementation_handoffs/parser_gre_connect_resp_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not change parser state, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, final reconciliation, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned GRE connect-response truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not treat GRE connect-response deck evidence as active submitted-deck truth unless the contract and focused tests explicitly require it."
    - "Do not target main for module PR work."
```

## Handoff Packet

Role performed: Codex B, Module Contract Writer.

Source problem representation: GitHub issue #22, tracked by parser module
audit tracker #5.

Contract produced: `docs/contracts/parser_gre_connect_resp.md`

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/5

Risk tier: High.

Owning truth layer: parser and state interpretation.

Public interface:

- `build_connect_resp_payload(message: dict[str, Any]) -> dict[str, Any]`
- GRE dispatch through `parsers/gre/__init__.py`
- emitted `GameStateEvent.payload` fields documented above

Invariants:

- Successful GRE connect-response dispatch emits `GameStateEvent`.
- Payload type remains `connect_resp`.
- Payload field names remain stable.
- `system_seat_ids`, `deck_cards`, and `sideboard_cards` are normalized lists.
- `settings` is a shallow copy.
- `raw_connect_resp` preserves the raw message object.
- The helper has no side effects.

Required tests: focused parser, dispatch, normalization, malformed-input, raw
payload preservation, settings copy, and downstream compatibility obligations
listed in `Tests Required`.

Acceptance criteria: listed above.

Open questions or contract risks:

- Future MTGA payload-shape drift may add new deck-message shapes.
- Connect-response deck evidence may need a future fallback contract.
- Nested settings aliasing is currently allowed by shallow-copy behavior.
- Extractor fallback from `raw_connect_resp` is not currently contracted.
- Game-state precedence over connect response should be locked if uncovered.

Next recommended thread role: Codex C, Module Implementer.
