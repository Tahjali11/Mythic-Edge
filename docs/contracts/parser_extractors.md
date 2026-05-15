# Parser Extractors Module Contract

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/9

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the current `src/mythic_edge_parser/app/extractors.py`
behavior and the guarantees future parser-extractor work must preserve unless a
new problem representation and module contract deliberately change them. This is
a contract artifact only. It does not implement behavior changes.

## Module

`src/mythic_edge_parser/app/extractors.py`

This module provides small extraction helpers that convert already-parsed MTGA
event payload dictionaries into primitive facts used by parser state, row
transforms, runtime surfaces, gameplay-action tracking, and local card-ID
diagnostic tools.

Plain English: this file does not parse raw log text and does not decide match
truth by itself. It safely reads facts from parser-produced payloads so the
state layer can own match/game interpretation.

## Owning Layer

Parser and state interpretation.

Extractor helpers belong to the parser truth-producing layer. They may read
normalized parser payloads and raw MTGA subpayloads preserved inside those
payloads, but they must not move truth ownership to workbook formulas, webhook
transport, dashboard logic, Apps Script, or AI interpretation.

## Files Owned By This Contract

- `src/mythic_edge_parser/app/extractors.py`
- `tests/test_app_extractors.py`
- `docs/contracts/parser_extractors.md`

Related files whose current behavior depends on this contract:

- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/arena_id_validation.py`
- `src/mythic_edge_parser/app/grp_id_candidates.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `tests/test_state.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_transforms.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_gre_game_state_parser.py`
- `tests/test_gre_game_result_parser.py`
- `tests/test_parser_regressions.py`

## Public Interface

Most functions in this module are underscore-prefixed, but the following names
are current compatibility surfaces because other app modules import them
directly:

- Safe normalization:
  - `_safe_local_player(players: list[dict[str, Any]]) -> dict[str, Any]`
  - `_first_present(*values: Any) -> Any`
  - `_maybe_int(value: Any) -> int | None`
  - `_safe_dict(value: Any) -> dict[str, Any]`
  - `_safe_list(value: Any) -> list[Any]`
- Game-state payload access:
  - `_raw_game_state_payload(payload: dict[str, Any]) -> dict[str, Any]`
  - `_raw_game_state_message(payload: dict[str, Any]) -> dict[str, Any]`
  - `_queued_game_state_message(payload: dict[str, Any]) -> dict[str, Any]`
  - `_game_state_dict_section(payload, *, top_level_key, message_key) -> dict[str, Any]`
  - `_game_state_list_section(payload, *, top_level_key, message_key) -> list[dict[str, Any]]`
  - `_queued_game_info(payload: dict[str, Any]) -> dict[str, Any]`
  - `_game_state_identity_payload(payload: dict[str, Any]) -> dict[str, Any]`
  - `_game_state_game_info(payload: dict[str, Any]) -> dict[str, Any]`
  - `_game_state_turn_info_payload(payload: dict[str, Any]) -> dict[str, Any]`
  - `_game_state_system_seat_ids(payload: dict[str, Any]) -> list[int]`
  - `_game_state_players(payload: dict[str, Any]) -> list[dict[str, Any]]`
  - `_game_state_zones(payload: dict[str, Any]) -> list[dict[str, Any]]`
  - `_game_state_objects(payload: dict[str, Any]) -> list[dict[str, Any]]`
  - `_game_state_actions(payload: dict[str, Any]) -> list[dict[str, Any]]`
  - `_game_state_annotations(payload: dict[str, Any]) -> list[dict[str, Any]]`
- Identity and turn extraction:
  - `_player_seat_id(player: dict[str, Any]) -> int | None`
  - `_player_team_id(player: dict[str, Any]) -> int | None`
  - `_hydrate_game_state_identity(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]`
  - `_extract_turn_info(payload: dict[str, Any], context: dict[str, Any] | None = None) -> tuple[Any, Any, Any, Any, Any, Any, Any]`
- Client-action and game-state player facts:
  - `_extract_starting_player_from_client_action(payload: dict[str, Any]) -> Any`
  - `_extract_local_team_from_client_action(payload: dict[str, Any]) -> Any`
  - `_extract_local_team_from_game_state(payload: dict[str, Any]) -> Any`
  - `_extract_starting_player_from_game_state(payload: dict[str, Any]) -> Any`
- Hand and GRP lookup extraction:
  - `_extract_local_private_hand_instance_ids(payload: dict[str, Any]) -> list[int]`
  - `_extract_instance_grp_lookup(payload: dict[str, Any]) -> dict[int, int]`
- Game-result extraction:
  - `_infer_scope_label(scope_value: Any) -> str`
  - `_is_known_winner(winner: Any) -> bool`
  - `_result_winner(result: dict[str, Any]) -> Any`
  - `_extract_game_result_scope_result(payload: dict[str, Any], scope_label: str, *, require_known_winner: bool) -> dict[str, Any] | None`
  - `_extract_game_result_identity(payload: dict[str, Any], context: dict[str, Any]) -> tuple[Any, Any, Any, Any, Any]`
  - `_has_match_scope_result(payload: dict[str, Any]) -> bool`
- Event timestamp extraction:
  - `_event_datetime(event: Any) -> datetime`
  - `_safe_iso(event: Any) -> str`

Any implementation thread that renames, removes, or changes return shapes for
these helpers must update all direct imports and the focused tests in one
coherent pass.

## Inputs

### Parsed event payload dictionaries

Type: `dict[str, Any]`.

Sources:

- `MatchStateEvent.payload` from `parsers/match_state.py`
- `GameStateEvent.payload` from `parsers/gre/game_state.py`
- `GameResultEvent.payload` from `parsers/gre/game_result.py`
- `ClientActionEvent.payload` from `parsers/client_actions.py`
- saved JSONL rows replayed through parser and diagnostic tools

Expected normalized game-state keys:

- `identity`
- `game_info`
- `turn_info`
- `system_seat_ids`
- `players`
- `zones`
- `game_objects`
- `actions`
- `annotations`
- `raw_game_state`

Expected raw game-state shapes:

- `raw_game_state.gameStateMessage`
- `raw_game_state.queuedGameStateMessage.gameStateMessage`
- `raw_game_state.systemSeatIds`

Expected game-result keys:

- `identity`
- `game_info`
- `winning_team_id`
- `result_type`
- `reason`
- `results`
- `match_state`

Expected client-action keys:

- top-level `team_id` / `teamId`
- top-level or nested starting-player seat keys such as `systemSeatId`,
  `system_seat_id`, `startingPlayerSystemSeatId`, and related variants
- `raw_client_action.payload`
- nested `chooseStartingPlayerResp`, `mulliganResp`, and `submitDeckResp`

### Parser context dictionary

Type: `dict[str, Any]`.

Primary source: `state._CONTEXT`.

Expected keys:

- `current_match_id`
- `current_game_number`
- `current_player_team`

Observed behavior: `_hydrate_game_state_identity()` treats context as optional
and uses `.get()` for fallback match/game identity. `_extract_game_result_identity()`
now coerces malformed or missing context to `{}` and uses `.get()` for fallback
match/game identity.

### Event object

Type: object with optional `metadata.timestamp`.

Observed behavior: `_event_datetime()` returns `metadata.timestamp` when it is a
`datetime`; otherwise it returns `datetime.now()`. `_safe_iso()` calls
`_event_datetime(event).isoformat()`.

## Outputs

Extractor outputs are primitive values or shallow containers only. They do not
write files, post webhooks, update workbook tabs, or mutate parser runtime
state.

Current output destinations:

- `state.py`
  - match/game identity
  - local team
  - starting player
  - game and match winners
  - opening hand instance IDs
  - instance-to-GRP lookup
  - event timestamps
- `transforms.py`
  - event inclusion and dedupe keys
  - serializable derived game-state identity
  - raw/archive sheet rows
  - human-readable summaries
- `runtime_surfaces.py`
  - active match snapshots
  - timelines
  - match history refresh triggers
- `gameplay_actions.py`
  - gameplay state identity
  - local seat
  - zones, objects, actions, and annotations
- `arena_id_validation.py` and `grp_id_candidates.py`
  - saved-log identity and card-observation scans
- `runner.py`
  - local JSONL partition timestamp via `_event_datetime()`

No extractor output is itself final workbook truth. Final match and game facts
are owned by `state.py` and `models.py` after state interpretation.

## Observed Behavior

### Safe normalization helpers

- `_safe_local_player()` returns `{}` for malformed or empty player-list input.
  If `LOCAL_PLAYER_INDEX` is in range it returns that player dictionary or `{}`;
  if the index is out of range it returns the first player dictionary or `{}`.
  Non-dictionary selected players return `{}`.
- `_first_present()` returns the first value that is not `None` and not `""`.
  Values such as `0`, `False`, `{}`, and `[]` are treated as present.
- `_maybe_int()` returns `int(value)` or `None` if Python raises `TypeError` or
  `ValueError`.
- `_safe_dict()` returns the value only when it is a `dict`; otherwise `{}`.
- `_safe_list()` returns the value only when it is a `list`; otherwise `[]`.

### Raw and queued game-state access

- `_raw_game_state_payload()` returns `payload["raw_game_state"]` only when that
  value is a dictionary.
- `_raw_game_state_message()` returns
  `raw_game_state["gameStateMessage"]` only when it is a dictionary.
- `_queued_game_state_message()` returns
  `raw_game_state["queuedGameStateMessage"]["gameStateMessage"]` only when both
  layers are dictionaries.
- `_game_state_dict_section()` prefers the normalized top-level section first,
  then the current raw `gameStateMessage`, then the queued raw
  `queuedGameStateMessage.gameStateMessage`.
- `_game_state_list_section()` uses the same fallback order and filters out
  non-dictionary list items.
- `_game_state_system_seat_ids()` prefers normalized top-level
  `system_seat_ids`; otherwise it reads raw `raw_game_state.systemSeatIds`.
  It normalizes each value through `_maybe_int()` and skips values that return
  `None`.
- `_game_state_players()`, `_game_state_zones()`, `_game_state_objects()`,
  `_game_state_actions()`, and `_game_state_annotations()` use the shared
  top-level/current-raw/queued-raw list fallback behavior.

### Game-state identity and turn info

- `_hydrate_game_state_identity()` reads match ID and game number from
  normalized `identity`, normalized or raw `game_info`, queued `gameInfo`, then
  optional context.
- Match IDs are converted to stripped strings. Missing match ID becomes `""`.
- Game number, turn number, and active player seat ID are normalized with
  `_maybe_int()`.
- Turn number can come from normalized identity, turn info keys
  `turn_number` / `turnNumber`, or top-level `payload["turn_number"]`.
- Active player can come from normalized identity, turn info keys
  `active_player_seat_id` / `activePlayer` / `activePlayerSeatId`, or top-level
  `payload["active_player_seat_id"]`.
- Phase and step come from identity, turn info, or top-level payload fallback.
- Stage comes from identity, game info, or top-level payload fallback.
- `identity_source` is `"payload"` when payload identity is complete enough,
  `"payload+context"` when payload and context combine, `"context"` when only
  context supplies match/game identity, and `"missing"` when neither supplies
  match/game identity.
- `_extract_turn_info()` returns only the seven-tuple
  `(match_id, game_number, turn_number, active_player_seat_id, phase, step, stage)`.

### Local team and starting player

- `_extract_starting_player_from_client_action()` searches a fixed list of
  starting-player seat keys at the top level, then inside
  `raw_client_action.payload`, then inside
  `raw_client_action.payload.chooseStartingPlayerResp`. It returns the original
  value, not an integer-normalized value.
- `_extract_local_team_from_client_action()` searches `team_id` / `teamId` at
  the top level, then inside `raw_client_action.payload`, then inside nested
  `chooseStartingPlayerResp`, `mulliganResp`, and `submitDeckResp`.
- `_extract_local_team_from_game_state()` treats the first normalized system
  seat ID as the local seat, finds the player with that seat ID, and returns
  that player's team ID.
- `_extract_starting_player_from_game_state()` returns `None` unless the
  hydrated turn number is exactly `1`. On turn one, it returns the active
  player's team ID when player mapping is available; otherwise it returns the
  active player seat ID.

### Local hand and instance-to-GRP lookup

- `_extract_local_private_hand_instance_ids()` looks for the first private hand
  zone in the game-state zone list.
- The hand zone must have type or zone type `ZoneType_Hand` and visibility
  `Visibility_Private`.
- When a local system seat is known, zones owned by another numeric seat are
  skipped. Zones with missing or non-integer owner seat are currently accepted.
- Object instance IDs are read from `objectInstanceIds` or
  `object_instance_ids`, normalized with `_maybe_int()`, and returned as a list.
- The helper returns the first matching hand zone only; it does not merge
  multiple hand zones.
- `_extract_instance_grp_lookup()` reads game objects and maps normalized
  `instanceId` / `instance_id` to normalized `grpId`, `grp_id`, `overlayGrpId`,
  or `overlay_grp_id`. If duplicate instance IDs appear, the last processed
  object wins.

### Game-result helpers

- `_infer_scope_label()` normalizes scope values containing `MatchScope_Game`
  or exactly `Game` to `"Game"`, and values containing `MatchScope_Match` or
  exactly `Match` to `"Match"`. Unknown scopes are returned as string text.
- `_is_known_winner()` rejects `None`, `""`, booleans, numeric zero, and string
  zero after stripping. Other values are treated as known.
- `_result_winner()` reads `winningTeamId` before `winning_team_id`.
- `_extract_game_result_scope_result()` scans `payload["results"]`, skips
  non-dictionary items, filters by normalized scope label, optionally requires a
  known winner, and returns the latest matching result.
- `_extract_game_result_identity()` reads match ID from `identity.match_id`,
  `game_info.matchID`, or context; game number from `identity.game_number`,
  `game_info.gameNumber`, or context; and top-level winner/result/reason from
  `winning_team_id`, `result_type`, and `reason`. Malformed `game_info` or
  context values degrade to neutral fallbacks.
- `_has_match_scope_result()` skips non-dictionary result entries and returns
  `True` when any dictionary result has normalized scope `"Match"`.

### Timestamp helpers

- `_event_datetime()` returns an event metadata timestamp only when it is a
  `datetime`.
- If the event has no metadata timestamp, `_event_datetime()` returns
  `datetime.now()`.
- `_safe_iso()` returns the ISO string for `_event_datetime(event)`.

## Required Guarantees

- Extractors must remain parser-owned helpers. They must not post webhooks,
  write workbook tabs, mutate `state.RUNTIME_STATE`, change row schemas, or own
  final match/game truth.
- The compatibility surfaces listed above must remain importable or be replaced
  with an intentional migration that updates all call sites and tests together.
- For parsed event payload dictionaries, malformed optional sections must
  degrade to neutral values such as `{}`, `[]`, `None`, or `""` rather than
  poisoning parser state.
- Top-level normalized game-state fields must take precedence over raw current
  game-state message fields, and raw current message fields must take
  precedence over queued message fallback fields.
- Queued game-state fallback must remain available for partial current messages
  so turn info, hand zones, and game objects can still be extracted.
- Context fallback for game-state identity must remain available for partial
  GameState payloads that arrive after a MatchState established current match
  and game identity.
- Game-scope and match-scope results must remain distinguishable. Match-scope
  winners must not be promoted into game winners by extractor behavior.
- Local private hand extraction must prefer local private hand zones when
  system seat IDs are available and must normalize instance IDs to integers.
- Instance-to-GRP lookup extraction must preserve both primary `grpId` and
  overlay GRP fallback behavior because opening-hand resolution and GRP
  diagnostic tools depend on both.
- Timestamp extraction must continue to return a `datetime` object for
  `runner.append_local_jsonl()` partitioning.
- Extractor behavior changes that affect match identity, game identity,
  local team, starting player, winners, opening hand, mulliganed-away cards, or
  GRP diagnostics must be validated with focused extractor tests plus the
  dependent state/transform/runtime tests listed below.

## Invariants

- Extractor helpers are pure with respect to project state: they return values
  and do not mutate module-level state, runtime state, workbook state, or files.
- Returned hand instance IDs are integers.
- Returned instance-to-GRP lookup keys and values are integers.
- `_extract_turn_info()` always returns a seven-item tuple in the order consumed
  by `state.py`, `transforms.py`, `runtime_surfaces.py`, validation tools, and
  candidate tools.
- `_hydrate_game_state_identity()` always returns the keys:
  `match_id`, `game_number`, `turn_number`, `active_player_seat_id`, `phase`,
  `step`, `stage`, and `identity_source`.
- Missing game-state identity must not create a false match ID. Missing match ID
  is represented as `""`.
- Unknown, blank, boolean, and zero winners are not known winners.
- Extractors do not decide row finality. Live/provisional versus final
  reconciliation remains owned by `state.py` and `models.py`.

## Error Behavior

- Expected malformed optional sections are coerced by helper functions:
  non-dict sections become `{}`, non-list sections become `[]`, and invalid
  integer conversions become `None`.
- Non-dictionary items in game-state list sections are ignored.
- Non-dictionary items in `_extract_game_result_scope_result()` results are
  ignored.
- `_event_datetime()` uses current local time when event metadata timestamp is
  absent or not a `datetime`.
- Post-fix behavior: `_safe_local_player()`,
  `_extract_game_result_identity()`, and `_has_match_scope_result()` guard the
  malformed optional inputs identified by the contract-test report and return
  neutral fallbacks instead of raising.

## Side Effects

None intended.

Observed non-mutating external dependency:

- `_safe_local_player()` reads `LOCAL_PLAYER_INDEX` from `app.config`.

Observed nondeterminism:

- `_event_datetime()` falls back to `datetime.now()` when metadata timestamp is
  missing or invalid.

## Dependency Order

Data flow:

1. Raw MTGA log lines are parsed by parser modules into event payloads.
2. `extractors.py` reads normalized payload fields and preserved raw subpayloads.
3. `state.py` uses extractor outputs to update `MatchSummary` parser truth.
4. `transforms.py` uses extractor outputs for event inclusion, archive/debug
   rows, serializable derived identity, and summaries.
5. `runtime_surfaces.py`, `gameplay_actions.py`, `arena_id_validation.py`, and
   `grp_id_candidates.py` consume extractor outputs for local diagnostics and
   runtime artifacts.
6. `models.py`, `outputs.py`, Apps Script, workbook tabs, helper formulas, and
   dashboards consume parser-owned facts after state/model serialization.

If extractor behavior changes, edit and verify in this order:

1. `src/mythic_edge_parser/app/extractors.py`
2. `tests/test_app_extractors.py`
3. dependent tests for state, transforms, runtime surfaces, and parser payloads
4. diagnostic tool tests if GRP or hand extraction changes
5. broader parser regression tests

## Compatibility

- Underscore-prefixed extractor helpers are legacy private-style names but are
  currently compatibility surfaces because app modules import them directly.
- Existing top-level normalized payload keys from parser modules must remain
  supported.
- Existing raw MTGA preserved payload shapes under `raw_game_state` and
  `raw_client_action` must remain supported.
- Existing camelCase and snake_case key alternatives must remain supported where
  current helpers already check both.
- Existing `grpId` / `overlayGrpId` lookup fallback must remain supported.
- Existing current-message-then-queued-message fallback must remain supported.

## Unknowns

- It is unknown whether underscore-prefixed helpers should remain the permanent
  public interface or be replaced later by non-underscored wrapper names.
- It is unknown whether `_maybe_int()` should continue accepting booleans and
  silently truncating fractional numeric values in identity and card-ID paths.
- It is unknown whether `_event_datetime()` should continue using local
  `datetime.now()` fallback or move to a deterministic/UTC fallback contract.
- It is unknown whether `_extract_starting_player_from_game_state()` should
  always return team ID, always return seat ID, or continue returning team ID
  when player mapping exists and seat ID otherwise.
- It is unknown whether local hand extraction should reject private hand zones
  with malformed owner seat when a local seat is known.
- It is unknown whether duplicate game object instance IDs should remain
  last-write-wins or become first-write-wins / conflict-detected.
- It is unknown whether live workbook state or deployed Apps Script behavior has
  drifted from repository code. This contract did not inspect either layer.

## Suspected Gaps

- `_maybe_int()` currently accepts booleans and truncates floats through
  Python's `int()` behavior. Focused tests now lock this as current behavior,
  but it may be too permissive for identity, team, seat, instance, and GRP
  fields.
- `_extract_starting_player_from_client_action()` returns raw values while
  game-state starting-player extraction usually returns normalized integers.
  Current call sites tolerate this, and focused tests now lock the current mixed
  return shape.
- `_extract_starting_player_from_game_state()` has mixed seat/team semantics:
  it returns team ID when player mapping exists and active seat ID otherwise.
  Focused tests now lock this current behavior.
- Local private hand extraction accepts zones with malformed owner seat as local
  when local system seat is known. Focused tests now lock this current behavior.
- Local private hand extraction returns only the first matching zone. Focused
  tests now lock this current behavior.
- `_extract_instance_grp_lookup()` keeps `0` as a GRP ID if present; it is not
  tested whether zero should be rejected like unknown winner zero.
- `_event_datetime()` fallback is nondeterministic. Focused tests now confirm
  the fallback returns a current local `datetime`.

## Tests Required

Focused extractor checks:

```powershell
py -m pytest -q tests/test_app_extractors.py
```

Relevant parser-state and transform checks when extractor behavior changes:

```powershell
py -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py
```

Related parser payload checks when game-result or game-state behavior changes:

```powershell
py -m pytest -q tests/test_gre_game_result_parser.py tests/test_gre_game_state_parser.py tests/test_parser_regressions.py
```

Full repo check before submitter opens or updates a module PR:

```powershell
.\tools\run_repo_checks.ps1
```

Recommended contract-test additions before behavior changes:

- Decide whether `_maybe_int()` should keep accepting bool and fractional
  values; focused tests currently lock existing Python `int()` behavior.
- Decide whether malformed local private hand owner seats should remain accepted
  as local when a local system seat is known; focused tests currently lock
  existing behavior.
- Decide whether `_extract_instance_grp_lookup()` should keep GRP ID `0` if
  present or reject it like unknown winner zero.

## Acceptance Criteria

- `docs/contracts/parser_extractors.md` exists.
- The contract links to issue #9, the constitution, the Module Contract Writer
  role rules, and the module contract template.
- The contract names parser and state interpretation as the owning truth layer.
- All current extractor compatibility surfaces imported by app modules are
  listed.
- Inputs and outputs are typed and sourced.
- Raw, queued, and normalized payload fallback order is explicit.
- Game-state identity, client-action local team, starting-player, hand,
  instance-to-GRP, game-result scope, and timestamp behavior are covered.
- Observed behavior, required guarantees, unknowns, and suspected gaps are
  explicitly separated.
- No runtime behavior changes are made in this contract thread.

## Next Workflow Action

Next role: Module Implementer (C)

Pasteable prompt:

````text
Use the Mythic Edge agent constitution. Act as the Module Implementer thread for https://github.com/Tahjali11/Mythic-Edge/issues/9.

Source artifacts:
- `docs/agent_constitution.md`
- `docs/agent_threads/implementation.md`
- `docs/contracts/parser_extractors.md`
- `docs/templates/implementation_handoff.md`

Task:
Compare the current `src/mythic_edge_parser/app/extractors.py` implementation, call sites, and focused tests against `docs/contracts/parser_extractors.md`.

Produce `docs/implementation_handoffs/parser_extractors_comparison.md`.

Do not assume there is a known bug. This is a contract audit / implementation comparison pass.

Required workflow:
1. Inspect `src/mythic_edge_parser/app/extractors.py`.
2. Inspect current direct call sites in `src/mythic_edge_parser/app/state.py`, `src/mythic_edge_parser/app/transforms.py`, `src/mythic_edge_parser/app/runtime_surfaces.py`, `src/mythic_edge_parser/app/gameplay_actions.py`, `src/mythic_edge_parser/app/arena_id_validation.py`, `src/mythic_edge_parser/app/grp_id_candidates.py`, and `src/mythic_edge_parser/app/runner.py`.
3. Inspect focused tests:
   - `tests/test_app_extractors.py`
   - `tests/test_state.py`
   - `tests/test_match_summary_from_match_state.py`
   - `tests/test_transforms.py`
   - `tests/test_runtime_surfaces.py`
   - `tests/test_gre_game_result_parser.py`
   - `tests/test_gre_game_state_parser.py`
   - `tests/test_parser_regressions.py`
4. Compare current behavior to the contract.
5. Identify contract matches, contract mismatches, missing safeguards, missing tests, stale bridge code, and unknowns.
6. Only implement code or test changes if the contract reveals a clear mismatch or missing safeguard that is safe and local.
7. Do not change workbook schema, webhook payload shape, deployed Apps Script behavior, row field names in `models.py`, state ownership in `state.py`, raw parser modules, secrets, environment variables, live workbook state, debug/archive/helper/runtime layers, or observability layers.

Validation:
Run the smallest focused check first:

```powershell
py -m pytest -q tests/test_app_extractors.py
```

If extractor behavior changes, also run:

```powershell
py -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py
```

If game-result or game-state payload behavior changes, also run:

```powershell
py -m pytest -q tests/test_gre_game_result_parser.py tests/test_gre_game_state_parser.py tests/test_parser_regressions.py
```

Final handoff must include:
- role performed
- issue and contract used
- artifact produced
- files changed
- code changed or docs-only
- contract matches
- contract mismatches
- missing tests
- validation run and result
- still-unverified layers
- whether forbidden scope was touched
- next recommended thread role
````

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/9"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_extractors.md"
  target_artifact: "docs/implementation_handoffs/parser_extractors_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "py -m pytest -q tests/test_app_extractors.py (11 passed)"
    - "py -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_gre_game_result_parser.py tests/test_gre_game_state_parser.py tests/test_parser_regressions.py (50 passed)"
  stop_conditions:
    - "Do not implement behavior changes unless the contract comparison finds a clear mismatch or missing safeguard."
    - "Do not change workbook schema, webhook payload shape, Apps Script deployment behavior, state ownership, or raw parser modules."
    - "Stop if the implementation would move parser-owned truth downstream."
```
