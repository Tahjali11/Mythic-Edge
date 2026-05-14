# GRE Game Result Parser Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/24

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
- `docs/contracts/parser_match_state.md`
- `docs/contracts/parser_gre_connect_resp.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the parser-owned GRE game-result helper in
`src/mythic_edge_parser/parsers/gre/game_result.py` and its dispatch
relationship with `src/mythic_edge_parser/parsers/gre/__init__.py`. It is a
contract artifact only. It does not implement code or change parser behavior.

## Module

`src/mythic_edge_parser/parsers/gre/game_result.py`

The module detects game-over GRE game-state payloads and builds normalized
`GameResultEvent.payload` dictionaries from parser-produced GRE
`GameStateEvent.payload` dictionaries.

## Owning Layer

Parser and state interpretation.

`game_result.py` owns parser conversion from normalized GRE game-state payloads
to normalized GRE game-result payloads:

- game-over detection
- game-result payload type/source
- stage and match-state fields copied from `game_info`
- top-level game-winner/result/reason fields from the latest known game-scope
  result
- match-scope result preservation inside `results`
- shallow copied output views of `game_info`, `identity`, and `results`
- neutral/default degradation for malformed optional sections

It does not own live match summary mutation, parser state final
reconciliation, workbook row shape, webhook transport, Apps Script behavior,
dashboard formulas, match identity, game identity, deduplication, or workbook
exports.

Parser truth boundary:

- `parsers/gre/game_state.py` owns building the normalized
  `GameStateEvent.payload` that feeds this helper.
- `game_result.py` owns deciding whether that normalized payload is game-over
  and building the normalized `GameResultEvent.payload`.
- `parsers/gre/__init__.py` owns raw GRE log dispatch and paired event
  emission.
- `events.py` owns the `GameResultEvent` class shape, event kind, performance
  class, and metadata hashing.
- `app/state.py` owns final live/final match and game reconciliation from
  already parsed events.
- `app/extractors.py` owns shared scope and identity helper behavior consumed
  by state, transforms, and runtime surfaces.
- Workbook formulas, webhook transport, Apps Script, dashboards, and AI notes
  must consume parser/state-produced game-result facts. They must not become
  the source of game-over detection, winner precedence, or final
  reconciliation.

## Files Owned By This Contract

- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `tests/test_gre_game_result_parser.py`
- `docs/contracts/parser_gre_game_result.md`

Related files whose behavior is referenced but not owned by this contract:

- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/api_common.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `tests/test_parsers.py`
- `tests/test_state.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_app_extractors.py`
- `tests/test_transforms.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_parser_regressions.py`

## Public Interface

### `is_game_over()`

`is_game_over(game_state_payload: dict[str, Any]) -> bool`

Public parser helper imported by `parsers/gre/__init__.py`.

Contract status:

- Accepts a normalized GRE game-state payload dictionary.
- Returns `True` only when the selected stage text is exactly
  `"GameStage_GameOver"`.
- Returns `False` for all other stage values and malformed optional sections.
- Does not create events.
- Does not mutate input.
- Has no side effects.

Input precondition:

- `game_state_payload` must be a dict-like object with `.get()`.
- Non-dict direct calls are outside the current public contract.

### `build_game_result_payload()`

`build_game_result_payload(game_state_payload: dict[str, Any]) -> dict[str, Any]`

Public parser helper imported by `parsers/gre/__init__.py`.

Contract status:

- Accepts a normalized GRE game-state payload dictionary.
- Returns a normalized `GameResultEvent.payload` dictionary.
- Does not create an event object.
- Does not inspect raw log text.
- Does not mutate `game_state_payload`.
- Has no side effects.

Input precondition:

- `game_state_payload` must be a dict-like object with `.get()`.
- The helper is designed for payloads already produced by
  `build_game_state_payload()`, not raw GRE message dictionaries.

Underscored functions in `game_result.py` are implementation details. Their
behavior is contract-covered through `is_game_over()` and
`build_game_result_payload()`, but other modules should not import them as
public API.

## GRE Parser Dispatch Relationship

`src/mythic_edge_parser/parsers/gre/__init__.py` exposes:

`try_parse(entry: LogEntry, timestamp: datetime | None) -> list[GameEvent]`

Game-result dispatch is not owned by `game_result.py`, but this contract
depends on the current relationship:

- The GRE parser marker set includes `"GameStage_GameOver"`.
- `try_parse()` parses the first dict JSON value from the raw body through
  `api_common.parse_json_from_body(body, "gre")`.
- `_extract_gre_messages()` accepts either:
  - a top-level parsed GRE message dict, or
  - `greToClientEvent.greToClientMessages` when it is a list.
- Non-dict entries inside `greToClientMessages` are ignored.
- For each message dict, GRE game-state parsing is attempted before
  connect-response parsing.
- `_build_game_state_events()` calls `build_game_state_payload(message, gsm)`
  when `gameStateMessage` or `queuedGameStateMessage.gameStateMessage` is a
  dict.
- `_build_game_state_events()` always emits the `GameStateEvent` first.
- If `is_game_over(game_state_payload)` is true, a paired `GameResultEvent` is
  appended after the `GameStateEvent`.
- Both paired events share `EventMetadata` built from the same raw log body and
  timestamp.
- Connect-response fallback is skipped when any game-state events were emitted
  for the message.

Required dispatch guarantee:

- A parseable GRE game-state payload whose selected stage is
  `"GameStage_GameOver"` must emit paired events in this order:
  `GameStateEvent`, then `GameResultEvent`.
- A parseable GRE game-state payload whose selected stage is not
  `"GameStage_GameOver"` must emit only `GameStateEvent`.
- A malformed or missing game-state message must not emit a `GameResultEvent`.
- Dispatch must not emit a `GameResultEvent` without the paired preceding
  `GameStateEvent` for the same GRE message.

## Inputs

### Raw Log Body For GRE Dispatch

| Input | Type | Source | Required |
| --- | --- | --- | --- |
| `entry.body` | `str` | MTGA log `LogEntry` | Yes |
| `timestamp` | `datetime | None` | router timestamp extraction | No |

The GRE parser currently considers a body parseable when it contains at least
one marker from `_MARKERS`, including `"GameStage_GameOver"`. Marker detection
is substring-based over the raw body.

Malformed raw bodies:

- If no GRE marker is present, `try_parse()` returns `[]`.
- If no dict JSON value can be parsed from the body, `try_parse()` returns
  `[]`.
- If a GRE batch has no dict message objects, `try_parse()` returns `[]`.

### Accepted GRE Game-State Input Shape

`build_game_result_payload()` consumes the normalized `GameStateEvent.payload`
shape produced by `build_game_state_payload()`.

Representative normalized input:

```json
{
  "type": "game_state_message",
  "message_type": "GREMessageType_GameStateMessage",
  "game_state_id": 42,
  "stage": "GameStage_GameOver",
  "match_state": "MatchState_GameComplete",
  "game_info": {
    "matchID": "match-1",
    "gameNumber": 2,
    "stage": "GameStage_GameOver",
    "matchState": "MatchState_GameComplete",
    "results": [
      {
        "scope": "MatchScope_Game",
        "winningTeamId": 1,
        "result": "ResultType_WinLoss",
        "reason": "ResultReason_Game"
      },
      {
        "scope": "MatchScope_Match",
        "winningTeamId": 1,
        "result": "ResultType_WinLoss",
        "reason": "ResultReason_Match"
      }
    ]
  },
  "identity": {
    "match_id": "match-1",
    "game_number": 2,
    "stage": "GameStage_GameOver"
  }
}
```

Accepted direct helper fields:

| Field | Type | Behavior |
| --- | --- | --- |
| `game_info` | dict | Source for stage, match state, and nested results. Non-dict becomes `{}`. |
| `game_info.stage` | Any | Source for output `stage` and first source for `is_game_over()`. |
| `game_info.matchState` | Any | Source for output `match_state`. |
| `game_info.results` | list | Source for output `results` and game-scope winner selection. |
| `identity` | dict | Shallow-copied to output `identity`; non-dict becomes `{}`. |
| `game_state_id` | Any | Passed through to output `game_state_id`; missing becomes `None`. |
| `message_type` | Any | Passed through to output `message_type`; missing becomes `""`. |
| `stage` | Any | Fallback only for `is_game_over()`, not for output `stage`. |

Not accepted by this helper as direct truth sources:

- raw GRE message dictionaries
- `raw_game_state.gameStateMessage.gameInfo`
- top-level `match_state` for output `match_state`
- top-level `winning_team_id`, `result_type`, or `reason`
- snake_case result winner keys for parser top-level game-winner selection

## Game-Over Detection

Observed behavior:

- `is_game_over()` first shallow-normalizes `game_state_payload["game_info"]`
  to `{}` when it is not a dict.
- It chooses stage text with:
  `game_info.get("stage") or game_state_payload.get("stage") or ""`.
- The chosen value is converted with `str(...)`.
- It returns `True` only when the result is exactly `"GameStage_GameOver"`.
- If `game_info.stage` is a truthy non-game-over value, top-level `stage` is
  not consulted.
- If `game_info.stage` is missing or falsey, top-level `stage` may make the
  event game-over.

Required guarantee:

- Keep `game_info.stage` precedence over top-level `stage`.
- Keep top-level `stage` fallback for game-over detection.
- Do not infer game-over from `match_state`, result lists, winners, or result
  reasons without a new contract.

Important distinction:

- `is_game_over()` may use top-level `stage` fallback, but
  `build_game_result_payload()` currently writes output `stage` only from
  `game_info.stage`. This is observed behavior and must not be changed
  silently.

## Outputs

`build_game_result_payload()` returns:

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `type` | `str` | `"game_result"` | Stable parser event type. |
| `source` | `str` | `"gre_game_state"` | Source marker for GRE-derived results. |
| `stage` | `str` | `""` | `str(game_info.stage or "")`. |
| `match_state` | `str` | `""` | `str(game_info.matchState or "")`. |
| `winning_team_id` | Any | `0` | `winningTeamId` from latest known game-scope result. |
| `result_type` | Any | `""` | `result` from latest known game-scope result. |
| `reason` | Any | `""` | `reason` from latest known game-scope result. |
| `results` | `list[Any]` | `[]` | Shallow list copy of `game_info.results` when it is a list. |
| `game_info` | `dict[str, Any]` | `{}` | Shallow dict copy of input `game_info`. |
| `identity` | `dict[str, Any]` | `{}` | Shallow dict copy of input `identity`. |
| `game_state_id` | Any | `None` | Pass-through input `game_state_id`. |
| `message_type` | Any | `""` | Pass-through input `message_type`. |

### Emitted Event

When GRE dispatch emits a game-result event, the event is a `GameResultEvent`
from `src/mythic_edge_parser/events.py`.

Observed event properties:

- `kind == "GameResult"`.
- `performance_class == PerformanceClass.POST_GAME_BATCH`.
- `metadata.timestamp` is the timestamp passed to `gre.try_parse()`.
- `metadata.raw_bytes` is `entry.body.encode()`.
- `metadata.raw_bytes_hash` is derived from the full raw log body.
- Paired game-state and game-result events from one GRE message share the same
  metadata object.
- `BaseEvent.__post_init__()` shallow-copies the top-level payload mapping.

Required event guarantee:

- The emitted payload type must remain `"game_result"`.
- The emitted event class must remain `GameResultEvent` unless a new problem
  representation and contract intentionally migrates the event family.
- Paired event order must remain `GameStateEvent` before `GameResultEvent`.

## Copy And Default Rules

### `game_info`

Observed behavior:

- If input `game_info` is a dict, output `game_info` is `dict(game_info)`.
- If input `game_info` is missing or not a dict, output `game_info` is `{}`.
- The copy is shallow.
- Nested values inside `game_info`, including the original `results` list, may
  still alias the input.

### `results`

Observed behavior:

- If copied `game_info["results"]` is a list, output `results` is
  `list(results)`.
- If `results` is missing or not a list, output `results` is `[]`.
- The output list is a shallow list copy.
- Non-dict list members are preserved in output `results`.
- Dict result entries are not copied; they may alias input result dicts.
- Result entry order is preserved.

### `identity`

Observed behavior:

- If input `identity` is a dict, output `identity` is `dict(identity)`.
- If input `identity` is missing or not a dict, output `identity` is `{}`.
- The copy is shallow.

### Scalars

Observed behavior:

- `stage` and `match_state` are stringified from `game_info` only.
- `game_state_id` is passed through as-is and defaults to `None` when missing.
- `message_type` is passed through as-is and defaults to `""` when missing.
- Top-level winner/result fields are read from the selected game-scope result
  only.
- Missing selected result fields default to:
  - `winning_team_id: 0`
  - `result_type: ""`
  - `reason: ""`

Required guarantee:

- Do not add deep-copy guarantees without a new contract and focused tests.
- Do not coerce `game_state_id`, `message_type`, `winning_team_id`,
  `result_type`, or `reason` without a new contract and focused tests.
- Preserve neutral defaults for malformed optional sections.

## Result Scope Normalization

Observed parser helper behavior:

- Scope values are converted with `str(scope_value or "")`.
- Values containing `"MatchScope_Game"` or exactly equal to `"Game"` normalize
  to `"Game"`.
- Values containing `"MatchScope_Match"` or exactly equal to `"Match"`
  normalize to `"Match"`.
- Unknown scope values return their string text.
- Falsey values normalize to `""`.

Required guarantee:

- Game-scope and match-scope entries must remain distinguishable.
- Match-scope results must not be promoted into top-level game-winner fields.
- Game-scope results must not be rewritten into match-scope results.
- Result list order must remain available for latest-result selection and
  downstream reconciliation.

## Known Winner Semantics

Observed known-winner behavior:

- `None` is unknown.
- `""` is unknown.
- Boolean values are unknown.
- Numeric zero is unknown, including `0` and `0.0`.
- String zero after stripping is unknown, including `"0"` and `" 0 "`.
- Empty string after stripping is unknown.
- Other values are treated as known by the current helper.

Required guarantee:

- `None`, `""`, `0`, and `"0"` must remain unknown winner values.
- Booleans must remain unknown winner values.
- Unknown winners must not be selected as the top-level game winner.
- Unknown winners must not overwrite known game or match winners downstream.
- Do not hard-code known winner values to only `1` or `2`; non-zero future
  Arena team IDs must remain representable.

## Top-Level Game-Winner Precedence

Observed behavior:

- `build_game_result_payload()` scans output `results` in list order.
- It ignores non-dict entries.
- It ignores entries whose scope does not normalize to `"Game"`.
- It ignores game-scope entries whose `winningTeamId` is unknown.
- It selects the latest game-scope entry with a known `winningTeamId`.
- Top-level `winning_team_id`, `result_type`, and `reason` are copied from that
  selected game-scope entry.
- If no game-scope entry with a known `winningTeamId` exists, top-level
  `winning_team_id` is `0`, `result_type` is `""`, and `reason` is `""`.
- A later game-scope result with an unknown winner does not erase an earlier
  known game-scope result.
- `winningTeamId` is the parser-selected winner key. A snake_case
  `winning_team_id` key in a raw result entry is not currently used for
  parser top-level game-winner selection.
- `result` and `reason` are the parser-selected result metadata keys. A
  snake_case `result_type` key in a raw result entry is not currently used for
  parser top-level result type selection.

Required guarantee:

- Top-level `winning_team_id`, `result_type`, and `reason` in GRE
  parser-produced `GameResult` payloads must represent the latest known
  game-scope result only.
- Match-scope results must remain preserved in `results`, but must not be
  promoted into top-level game-winner fields.
- Do not fall back from missing game-scope results to match-scope results,
  top-level game-state fields, workbook formulas, dashboard logic, Apps Script,
  webhook transport, or AI interpretation.

## Match-Scope Preservation

Observed behavior:

- `build_game_result_payload()` does not build top-level match-winner fields.
- Match-scope result entries remain in output `results` exactly as list
  members.
- Non-dict result entries also remain in output `results`; downstream helpers
  skip them when reading scopes.
- Result dict key names are not normalized by this helper.

Required guarantee:

- Match-scope result entries must remain available in `results` for
  `state.py` final reconciliation.
- Match-scope `winningTeamId`, `result`, and `reason` must not be lost,
  filtered, or rewritten by this parser helper.
- Final match-winner precedence remains owned by `state.py` and
  `docs/contracts/parser_state.md`.
- This parser contract must remain compatible with the state contract:
  - game winner from latest known game-scope result
  - match winner from latest known match-scope result when present
  - top-level match winner fallback only when no known match-scope winner
    exists and `match_state == "MatchState_MatchComplete"`
  - `None`, `""`, `0`, and `"0"` unknown

## Malformed Input Behavior

For dict-like `game_state_payload` inputs, helpers must not raise for:

- missing `game_info`
- non-dict `game_info`
- missing `game_info.stage`
- missing `game_info.matchState`
- missing `game_info.results`
- non-list `game_info.results`
- non-dict entries in `results`
- missing or unknown result `scope`
- missing or unknown result `winningTeamId`
- missing result `result`
- missing result `reason`
- missing or non-dict `identity`
- missing `game_state_id`
- missing `message_type`

Neutral/default values should be used as documented above.

Direct helper calls with non-dict `game_state_payload` values are outside the
current public contract.

GRE dispatch malformed behavior:

- no GRE marker: `[]`
- unparseable JSON or non-dict first JSON value: `[]`
- invalid `greToClientMessages` shape: `[]`
- non-dict batch message members: ignored
- missing/non-dict game-state message: no game-state event and no game-result
  event
- game-state payload that is not game-over: no `GameResultEvent`

## Observed Current Behavior

- `is_game_over()` uses `game_info.stage` first and top-level `stage` as a
  fallback.
- `build_game_result_payload()` uses `game_info.stage` and
  `game_info.matchState` only for output `stage` and `match_state`.
- `game_info`, `identity`, and `results` output views are shallow copies.
- Top-level game-winner fields come from the latest known game-scope result.
- Match-scope results are preserved in `results` but are not promoted into
  top-level game-winner fields.
- Unknown winners are filtered out during game-scope selection.
- GRE dispatch emits `GameStateEvent` before `GameResultEvent` for game-over
  game-state payloads.
- Both paired events share metadata from the same raw log body.

## Required Guarantees

- Keep game-result parsing in the parser layer.
- Keep `is_game_over()` and `build_game_result_payload()` as public helper APIs
  for GRE parser dispatch.
- Keep the paired event order `GameStateEvent`, then `GameResultEvent`.
- Keep the emitted event class as `GameResultEvent`.
- Keep payload type/source values stable:
  - `type == "game_result"`
  - `source == "gre_game_state"`
- Keep output field names stable.
- Keep top-level game-winner fields game-scope-derived only.
- Keep match-scope result entries preserved in `results`.
- Keep unknown winner semantics aligned with parser-state and extractor
  contracts.
- Keep no-raise behavior for malformed optional sections.
- Keep shallow-copy behavior unless a future contract intentionally changes it.
- Do not change parser state final reconciliation, workbook schema, webhook
  payload shape, Apps Script behavior, parser event classes, match/game
  identity, deduplication, secrets, raw logs, generated data, runtime status
  files, failed posts, or workbook exports.

## Downstream Consumers

### `state.py`

`state._update_match_summary()` consumes `GameResultEvent.payload` for final
game and match reconciliation.

Compatibility expectations:

- Top-level `winning_team_id`, `result_type`, and `reason` from this parser are
  game-scope fields.
- `results` must preserve match-scope entries for final match reconciliation.
- `identity` and `game_info` must remain available for match ID and game number
  fallback.
- Unknown winners must remain neutral and must not overwrite existing state.
- Final reconciliation precedence belongs to `parser_state.md`; this parser
  contract supplies the payload shape it depends on.

### `extractors.py`

Game-result extractors read:

- `identity`
- `game_info`
- top-level `winning_team_id`
- top-level `result_type`
- top-level `reason`
- nested `results[].scope`
- nested `results[].winningTeamId`
- nested `results[].winning_team_id`
- nested `results[].result`
- nested `results[].reason`

Compatibility expectations:

- Parser result scopes must remain readable by `_infer_scope_label()`.
- Parser output `results` must remain a list when present.
- Non-dict result entries may exist and must remain safe to skip.
- Top-level parser winner fields must remain game-scope-derived.

### `transforms.py`

Transforms include `GameResult` events and build raw sheet rows from
`_extract_game_result_identity()` and `_has_match_scope_result()`.

Compatibility expectations:

- `GameResultEvent.payload` must remain JSON serializable through
  `to_serializable()`.
- The parser must not move row finality or workbook shape decisions into
  `game_result.py`.
- This contract does not change raw sheet row shape or dedupe behavior.

### `runtime_surfaces.py`

Runtime surfaces use `GameResultEvent` payloads for timeline entries and active
match snapshots.

Compatibility expectations:

- `identity`, top-level winner/result/reason fields, and `game_info` must
  remain available for timeline summaries.
- Runtime surfaces consume parser-produced fields; they must not parse raw GRE
  result lists as their own truth source.

### `events.py`

`GameResultEvent` is the event class for emitted GRE game-result payloads.

Compatibility expectations:

- `kind == "GameResult"`.
- `performance_class == PerformanceClass.POST_GAME_BATCH`.
- Top-level payload is shallow-copied by `BaseEvent`.
- Event class changes are out of scope for this contract.

### Workbook, Webhook, Apps Script, Dashboard, And AI Layers

These layers are downstream consumers only.

Compatibility expectations:

- They must not reconstruct game-over detection, game winner, match winner,
  result type, or result reason from raw GRE payloads.
- They must not become fallback error handlers for parser bugs.
- This contract does not change workbook schema, webhook payload shape, Apps
  Script behavior, dashboard formulas, or AI-generated interpretation.

## Ownership Boundaries

Owned by this contract:

- `is_game_over()` behavior.
- `build_game_result_payload()` output shape and defaults.
- Game-scope top-level winner precedence.
- Match-scope result preservation.
- Known-winner semantics inside parser game-scope selection.
- GRE dispatch relationship for paired game-over emissions.
- Shallow copy/default behavior for game-result payload views.

Not owned by this contract:

- GRE game-state payload construction beyond accepted input compatibility.
- Parser state final reconciliation implementation.
- Extractor implementation details beyond compatibility requirements.
- Transform row shape and dedupe.
- Runtime status files or timeline write behavior.
- Match identity.
- Game identity.
- Deduplication.
- Workbook schema.
- Webhook payload shape.
- Apps Script behavior.
- Secrets, environment variables, raw logs, generated data, failed posts, or
  workbook exports.

## Compatibility

Stable compatibility surfaces:

- `is_game_over(game_state_payload)`.
- `build_game_result_payload(game_state_payload)`.
- GRE parser import of both helpers.
- Payload type string `"game_result"`.
- Payload source string `"gre_game_state"`.
- Payload fields:
  - `stage`
  - `match_state`
  - `winning_team_id`
  - `result_type`
  - `reason`
  - `results`
  - `game_info`
  - `identity`
  - `game_state_id`
  - `message_type`
- `GameResultEvent` event family and `POST_GAME_BATCH` performance class.
- Paired `GameStateEvent` before `GameResultEvent` ordering.
- Unknown winner values `None`, `""`, `0`, and `"0"`.
- Shallow copied `game_info`, `identity`, and `results` output views.

Breaking changes that require a new problem representation or contract:

- Renaming output fields.
- Emitting a different event class.
- Changing game-over detection away from exact `"GameStage_GameOver"`.
- Removing top-level `stage` fallback from `is_game_over()`.
- Promoting match-scope results into top-level game-winner fields.
- Dropping match-scope results from `results`.
- Treating `0` or `"0"` as known winners.
- Deep-copying nested output structures as a new guarantee.
- Moving winner precedence into workbook formulas, dashboard logic, Apps
  Script, webhook transport, or AI interpretation.

## Unknowns

- Whether MTGA can emit additional game-over stage spellings or result-list
  shapes.
- Whether future GRE result entries may use snake_case winner/result keys
  before reaching this parser helper.
- Whether top-level `stage` fallback in `is_game_over()` should remain forever
  or become unnecessary once GRE game-state parsing is fully contracted.
- Whether `build_game_result_payload()` should ever copy top-level `stage` or
  `match_state` as fallback output fields. It does not do so now.
- Whether nested `game_info`, `identity`, and result-entry aliasing should
  remain acceptable or become deep-copy protected.
- Whether permissive substring scope matching should become stricter in a
  future parser hardening pass.

## Suspected Gaps

- Focused parser tests do not yet explicitly cover `None`, `""`, `0`, `"0"`,
  and boolean winners inside `build_game_result_payload()` selection.
- Focused parser tests do not yet cover a later unknown game-scope winner after
  an earlier known game-scope winner.
- Focused parser tests do not yet cover exact `"Game"` / `"Match"` scope
  aliases separately from MTGA `"MatchScope_*"` values.
- Focused parser tests do not yet cover non-list `game_info.results`.
- Focused parser tests do not yet cover queued game-state messages that are
  also game-over.
- Focused dispatch tests do not yet assert paired event metadata identity or
  equality for game-over messages.
- The top-level `stage` fallback can make `is_game_over()` return `True` while
  `build_game_result_payload()` still emits `stage == ""` if `game_info` lacks
  a stage.
- Shallow copies protect top-level container mutation but not nested
  dictionaries/lists.

## Error Behavior

- Parser dispatch should return `[]` instead of raising for malformed raw GRE
  log bodies and unsupported message shapes.
- Direct helper calls should return neutral defaults instead of raising for
  malformed optional sections on dict-like inputs.
- Non-dict entries in `results` should remain in output `results` but be
  skipped by game-scope selection.
- The module should not log, write diagnostics, mutate runtime state, post
  webhooks, update workbook rows, or write runtime artifacts on malformed
  input.
- Contract ambiguity about winner precedence, unknown winner values, or final
  reconciliation must route back to Codex B rather than being implemented
  silently.

## Side Effects

`is_game_over()` and `build_game_result_payload()` have no side effects.

GRE game-result dispatch side effects are limited to constructing in-memory
event objects. Any later state mutation, file write, webhook post, workbook
row, runtime status update, timeline write, or diagnostic artifact is owned by
downstream modules and is out of scope for this contract.

## Dependency Order

Implementation threads should evaluate changes in this order:

1. `src/mythic_edge_parser/parsers/gre/game_result.py`
2. `tests/test_gre_game_result_parser.py`
3. `src/mythic_edge_parser/parsers/gre/__init__.py`
4. `tests/test_parsers.py`
5. `src/mythic_edge_parser/parsers/gre/game_state.py`, only if accepted input
   shape is implicated
6. `src/mythic_edge_parser/events.py`, only if event emission shape is
   implicated
7. `src/mythic_edge_parser/app/extractors.py`, only if scope/winner helper
   compatibility is implicated
8. `src/mythic_edge_parser/app/state.py`, only if final reconciliation
   compatibility is implicated and the state contract allows it
9. `src/mythic_edge_parser/app/transforms.py` and
   `src/mythic_edge_parser/app/runtime_surfaces.py`, only if downstream tests
   prove parser-local work is insufficient

Do not start with workbook, webhook, Apps Script, dashboard, or AI-layer
changes.

## Tests Required

Focused tests expected for Module Implementer or Module Fixer:

- `is_game_over()`:
  - returns true for `game_info.stage == "GameStage_GameOver"`
  - returns true for top-level `stage == "GameStage_GameOver"` when
    `game_info.stage` is missing/falsey
  - returns false when `game_info.stage` is a truthy non-game-over value
  - returns false for malformed `game_info` and non-game-over fallback stage
  - does not infer game-over from `match_state` or result list alone
- `build_game_result_payload()` happy path:
  - emits `type == "game_result"`
  - emits `source == "gre_game_state"`
  - copies `stage` from `game_info.stage`
  - copies `match_state` from `game_info.matchState`
  - passes through `game_state_id`
  - passes through `message_type`
  - shallow-copies `game_info`, `identity`, and top-level `results`
- Defaults and malformed sections:
  - malformed/missing `game_info` yields `{}`, `stage == ""`,
    `match_state == ""`, `results == []`
  - malformed/missing `identity` yields `{}`
  - non-list `game_info.results` yields `[]`
  - missing selected result fields yield `winning_team_id == 0`,
    `result_type == ""`, and `reason == ""`
- Result selection:
  - latest known `MatchScope_Game` result wins top-level
    `winning_team_id`, `result_type`, and `reason`
  - earlier known game-scope result survives a later unknown game-scope result
  - match-scope result is not promoted into top-level game-winner fields
  - non-dict result entries are skipped for selection but preserved in
    `results`
  - exact `"Game"` scope alias is accepted
  - exact `"Match"` scope alias remains match scope and is not promoted
  - unknown scopes are ignored for top-level game-winner selection
  - `None`, `""`, `0`, `"0"`, and booleans are unknown winners
- Dispatch:
  - game-over GRE game-state message emits `GameStateEvent` then
    `GameResultEvent`
  - non-game-over GRE game-state message emits only `GameStateEvent`
  - queued game-state game-over message emits the paired events
  - paired events have expected metadata from raw body bytes and timestamp
  - malformed GRE batches do not emit game-result events
- Downstream compatibility:
  - state tests continue proving game winner from latest game-scope result
  - state tests continue proving match winner/result/reason from nested
    match-scope result when present
  - state tests continue proving top-level match-winner fallback only for
    `MatchState_MatchComplete`
  - extractor tests continue proving scope normalization and unknown winner
    semantics
  - transform/runtime regression tests continue consuming parser-produced
    `GameResult` payloads without raw GRE reinterpretation

Suggested focused validation:

```bash
python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_app_extractors.py
python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py
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

- `docs/contracts/parser_gre_game_result.md` exists and links issue #24,
  tracker #5, the agent constitution, the module contract role doc, the module
  contract template, and adjacent parser contracts.
- The contract clearly names parser and state interpretation as the truth
  layer.
- The contract clearly names owned files and related consumer files.
- Public helper APIs are documented.
- GRE parser dispatch and paired `GameStateEvent` / `GameResultEvent` emission
  are documented.
- Game-over detection and top-level stage fallback are documented.
- Accepted input shape from `game_state.py` is documented.
- Output fields, default values, and type/shape expectations are documented.
- Shallow copy behavior for `game_info`, `identity`, and `results` is
  documented.
- Result-scope normalization and known-winner semantics are documented,
  including `None`, `""`, `0`, and `"0"` as unknown.
- Top-level game-winner precedence is documented as latest known game-scope
  only.
- Match-scope result preservation for `state.py` is documented.
- Malformed input behavior and no-side-effect expectations are documented.
- Focused test obligations and validation commands are listed.
- The handoff routes to Codex C: Module Implementer unless contract review
  finds a framing problem.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex C: Module Implementer for issue #24 and docs/contracts/parser_gre_game_result.md.

Goal:
Compare the current GRE game-result parser implementation and focused tests against the GRE game-result module contract. Implement only the smallest coherent code and test changes needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/24
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/parser_gre_game_result.md
- docs/contracts/parser_state.md
- docs/contracts/parser_extractors.md
- docs/contracts/parser_match_state.md
- docs/contracts/parser_gre_connect_resp.md
- src/mythic_edge_parser/parsers/gre/game_result.py
- src/mythic_edge_parser/parsers/gre/__init__.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/extractors.py
- src/mythic_edge_parser/app/transforms.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- tests/test_gre_game_result_parser.py
- tests/test_parsers.py
- tests/test_state.py
- tests/test_match_summary_from_match_state.py
- tests/test_app_extractors.py
- tests/test_transforms.py
- tests/test_runtime_surfaces.py
- tests/test_parser_regressions.py

Do:
- Compare observed code behavior against the contract before editing.
- Preserve parser-owned truth boundaries.
- Add focused tests for contracted parser behavior not currently covered.
- Keep behavior changes minimal and parser-local unless the contract explicitly requires a downstream update.
- Produce docs/implementation_handoffs/parser_gre_game_result_comparison.md with the comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Move parser-owned game-result truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation.
- Promote match-scope results into top-level game-winner fields.
- Treat None, "", 0, or "0" as known winners.
- Target main; module PR work belongs on codex/parser-module-audit-suite.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/24"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_gre_game_result.md"
  target_artifact: "docs/implementation_handoffs/parser_gre_game_result_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned game-result truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not promote match-scope results into top-level game-winner fields."
    - "Do not treat None, \"\", 0, or \"0\" as known winners."
    - "Do not target main for module PR work."
```

## Handoff Packet

Role performed: Codex B, Module Contract Writer.

Source problem representation: GitHub issue #24, tracked by parser module
audit tracker #5.

Contract produced: `docs/contracts/parser_gre_game_result.md`

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/5

Risk tier: High.

Owning truth layer: parser and state interpretation.

Public interface:

- `is_game_over(game_state_payload: dict[str, Any]) -> bool`
- `build_game_result_payload(game_state_payload: dict[str, Any]) -> dict[str, Any]`
- GRE dispatch through `parsers/gre/__init__.py`
- emitted `GameResultEvent.payload` fields documented above

Invariants:

- Game-over GRE game-state dispatch emits `GameStateEvent` then
  `GameResultEvent`.
- Payload type remains `game_result`.
- Payload source remains `gre_game_state`.
- Top-level winner/result/reason fields are game-scope-derived only.
- Match-scope results remain preserved in `results`.
- `None`, `""`, `0`, and `"0"` remain unknown winners.
- Helper functions have no side effects.

Required tests: focused helper, dispatch, copy/default, scope normalization,
known-winner, top-level precedence, match-scope preservation, malformed-input,
and downstream compatibility obligations listed in `Tests Required`.

Acceptance criteria: listed above.

Open questions or contract risks:

- Future MTGA result-list shape drift may require new accepted payload shapes.
- Snake_case result winner keys are not currently consumed by parser top-level
  game-winner selection.
- Top-level `stage` fallback can detect game-over while output `stage` remains
  blank if `game_info.stage` is absent.
- Shallow output copies allow nested aliasing.
- Scope matching is substring-permissive rather than strict enum matching.

Next recommended thread role: Codex C, Module Implementer.
