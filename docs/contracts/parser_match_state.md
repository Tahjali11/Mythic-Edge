# Parser Match State Module Contract

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/16

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Adjacent contracts:

- `docs/contracts/parser_state.md`
- `docs/contracts/parser_extractors.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the parser-owned match-state event parser in
`src/mythic_edge_parser/parsers/match_state.py`. It is a contract artifact
only. It does not implement code or change parser behavior.

## Module

`src/mythic_edge_parser/parsers/match_state.py`

The module recognizes MTGA `matchGameRoomStateChangedEvent` log bodies and
normalizes match-room state payloads into `MatchStateEvent` objects.

## Owning Layer

Parser and state interpretation.

`match_state.py` owns the first normalized parser representation of
match-room state changes. It does not own final match/game reconciliation,
deduplication, workbook schema, webhook payload transport, Apps Script behavior,
dashboard interpretation, or generated workbook exports.

Parser truth boundary:

- `match_state.py` owns recognition of match-room state log entries.
- `match_state.py` owns the normalized `MatchStateEvent.payload` field names
  emitted from those entries.
- `match_state.py` owns preserving game-scope and match-scope final result
  entries without collapsing them together.
- `src/mythic_edge_parser/app/state.py` owns live runtime state, match summary
  mutation, local player-team correction, game-winner assignment, match-winner
  assignment, and final reconciliation.
- Workbook formulas, dashboard logic, Apps Script, webhook transport, and AI
  review notes must consume parser-produced facts rather than reinterpreting
  raw match-room state payloads.

## Files Owned By This Contract

- `src/mythic_edge_parser/parsers/match_state.py`
- `tests/test_match_state_parser.py`
- `docs/contracts/parser_match_state.md`

Related files whose behavior is referenced but not owned by this contract:

- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/parsers/api_common.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- `tests/test_parsers.py`
- `tests/test_match_summary_from_match_state.py`
- `docs/contracts/parser_state.md`
- `docs/contracts/parser_extractors.md`

## Public Interface

### Constants

`MATCH_STATE_MARKER`

- Value: `"matchGameRoomStateChangedEvent"`.
- Contract status: public parser marker used to identify candidate log bodies.

### Functions

`try_parse(entry: LogEntry, timestamp: datetime | None) -> GameEvent | None`

- Public parser entrypoint.
- Returns a `MatchStateEvent` when `entry.body` contains a parseable
  match-room state payload.
- Returns `None` when the body is not a match-state candidate or cannot be
  reduced to a dict match-state event.

`build_payload(state_event: dict[str, Any]) -> dict[str, Any]`

- Public/testable payload builder.
- Accepts the selected match-room state event dict.
- Returns the normalized `MatchStateEvent.payload`.

Underscored helpers in this module are implementation details. Their observed
behavior is contract-covered through `try_parse()` and `build_payload()`, but
callers should not import them as public API.

### Event Type

Successful parses emit `MatchStateEvent` from `src/mythic_edge_parser/events.py`.

Observed event properties:

- `kind == "MatchState"`.
- `performance_class == PerformanceClass.INTERACTIVE_DISPATCH`.
- `metadata.timestamp` is the timestamp passed to `try_parse()`.
- `metadata.raw_bytes` is `entry.body.encode()`.

## Inputs

### `try_parse()` Input

| Input | Type | Source | Required |
| --- | --- | --- | --- |
| `entry.body` | `str` | MTGA log `LogEntry` | Yes |
| `timestamp` | `datetime | None` | log reader timestamp extraction | No |

Candidate detection is marker-based: the body must contain
`matchGameRoomStateChangedEvent`.

The JSON body may appear in either supported shape:

- wrapped: `{"matchGameRoomStateChangedEvent": {"gameRoomInfo": ...}}`
- bare: `{"gameRoomInfo": ...}`

Observed parser extraction uses `api_common.parse_json_from_body()`. This module
does not own generic JSON scanning behavior.

### `build_payload()` Input

`state_event` must be a dict selected from the wrapped or bare payload.

Recognized nested fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `gameRoomInfo.stateType` | object/string | Raw MTGA match-room state enum. |
| `gameRoomInfo.gameRoomConfig.matchId` | object/string | MTGA match ID. |
| `gameRoomInfo.gameRoomConfig.eventId` | object/string | MTGA event/queue ID. |
| `gameRoomInfo.gameRoomConfig.reservedPlayers` | list[dict] | Preferred player source when non-empty. |
| `gameRoomInfo.players` | list[dict] | Fallback player source. |
| `gameRoomInfo.finalMatchResult.matchCompletedReason` | object/string | Raw final match completion reason. |
| `gameRoomInfo.finalMatchResult.resultList` | list[dict] | Raw final result entries. |

Recognized player fields:

- `userId`
- `playerName`
- `systemSeatId`
- `teamId`
- `eventId`, used only as an event-ID fallback

Recognized final result fields:

- `scope`
- `result`
- `winningTeamId`
- `reason`

## Outputs

### Non-Parse Output

`try_parse()` returns `None` when:

- `entry.body` does not contain `MATCH_STATE_MARKER`.
- `api_common.parse_json_from_body()` returns `None`.
- The parsed JSON does not contain a dict
  `matchGameRoomStateChangedEvent`.
- The parsed JSON is not the bare supported shape with a dict `gameRoomInfo`.

### `MatchStateEvent.payload`

Successful payloads always include:

| Field | Type | Observed value source | Meaning |
| --- | --- | --- | --- |
| `type` | `str` | derived from `state_type` | Normalized event type. |
| `state_type` | object/string | `gameRoomInfo.stateType` or `""` | Raw MTGA match-room state enum. |
| `match_id` | object/string | `gameRoomConfig.matchId` or `""` | MTGA match ID. |
| `event_id` | `str` | config/player fallback | MTGA event ID when known. |
| `players` | list[dict] | selected player source | Normalized player summaries. |
| `raw_match_state` | dict | selected state event | Raw selected match-state payload. |

`type` allowed values:

| `state_type` | `type` |
| --- | --- |
| `MatchGameRoomStateType_Playing` | `match_started` |
| `MatchGameRoomStateType_MatchCompleted` | `match_completed` |
| any other value, missing value, or malformed value | `state_changed` |

Required guarantees:

- Unknown or novel `state_type` values must degrade to `state_changed`.
- `type` must remain one of `match_started`, `match_completed`, or
  `state_changed` unless a future contract expands the allowed set.
- The parser must not require downstream consumers to inspect raw
  `state_type` to distinguish started/completed match-state events.

### Player Output

`players` is built from `gameRoomConfig.reservedPlayers` when that field is a
non-empty list of dicts. Otherwise it is built from `gameRoomInfo.players` when
that field is a list of dicts.

Each normalized player dict has this shape:

| Field | Source | Missing default |
| --- | --- | --- |
| `user_id` | `userId` | `""` |
| `player_name` | `playerName` | `""` |
| `system_seat_id` | `systemSeatId` | `0` |
| `team_id` | `teamId` | `0` |

Required guarantees:

- Non-list player containers must normalize to an empty player list.
- Non-dict player entries must be skipped.
- Reserved players remain the preferred source when present.
- Player order from the selected source must be preserved.
- Player data remains parser-produced context only. Local-player truth may be
  corrected later by parser state from client actions and game-state evidence.

### Event ID Output

`event_id` selection order:

1. Trimmed non-empty `gameRoomConfig.eventId`.
2. First trimmed non-empty `eventId` found in the selected player source.
3. `""`.

Required guarantees:

- Blank, missing, or falsey config event IDs must not block player fallback.
- Event ID fallback must use the same selected player source used for
  `players`.
- Event ID extraction must not classify rankedness or event family. That truth
  belongs to downstream parser identity classification.

### Final Result Output

When `gameRoomInfo.finalMatchResult` is a non-empty dict, payloads also include:

| Field | Type | Source | Missing default |
| --- | --- | --- | --- |
| `match_completed_reason` | object/string | `finalMatchResult.matchCompletedReason` | `""` |
| `game_results` | list[dict] | `finalMatchResult.resultList` | `[]` |

Each normalized `game_results` entry has this shape:

| Field | Source | Missing default |
| --- | --- | --- |
| `scope` | `scope` | `""` |
| `result` | `result` | `""` |
| `winning_team_id` | `winningTeamId` | `0` |
| `reason` | `reason` | `""` |

Observed behavior:

- `game_results` is omitted entirely when `finalMatchResult` is missing,
  falsey, or not a dict.
- `resultList` values that are not lists normalize to `game_results: []` when
  `finalMatchResult` itself is a non-empty dict.
- Non-dict result entries are skipped.
- Result entry order is preserved.
- `winningTeamId` is copied as-is when present; missing values default to `0`.
- This parser does not infer explicit game numbers from `resultList`.

Required guarantees:

- `MatchScope_Game` and `MatchScope_Match` entries must remain distinguishable
  through the normalized `scope` field.
- Match-scope result entries must not be promoted into game-scope result
  entries by this parser.
- Game-scope result entries must not be promoted into match-scope result
  entries by this parser.
- The parser must preserve raw result ordering because current state handling
  assigns MatchState game-scope results sequentially.
- `0` remains the parser's observed missing-winner default for omitted
  `winningTeamId` in this payload shape. The decision whether `0` is an
  unknown winner or a valid team value belongs to parser-state final
  reconciliation contracts.
- Final reconciliation winner precedence belongs to `state.py`, not to
  `match_state.py`.

### Raw Payload Output

`raw_match_state` contains the selected state event dict.

Required guarantees:

- `raw_match_state` must be present on successful payloads for inspection and
  replay/debug surfaces.
- Callers must treat `raw_match_state` as read-only. The current event payload
  copy is shallow, so this contract does not guarantee deep-copy isolation of
  nested raw objects.

## Observed Behavior

- Marker matching is a simple substring check against `entry.body`.
- Wrapped payloads are preferred when
  `parsed["matchGameRoomStateChangedEvent"]` is a dict.
- Bare payloads are accepted only when `parsed["gameRoomInfo"]` is a dict.
- Missing or malformed nested dicts degrade to blank strings, `0`, empty lists,
  omitted final-result fields, or `state_changed`.
- Successful events store the original encoded log body in metadata.
- `build_payload()` can be called directly in tests with a selected
  `state_event` dict.

## Required Guarantees

- Keep `try_parse()` side-effect free.
- Keep `build_payload()` side-effect free.
- Do not write files, mutate parser runtime state, post webhooks, update
  workbook rows, refresh status files, or touch generated data from this module.
- Do not change workbook schema, webhook payload shape, Apps Script behavior,
  parser state behavior, extractor behavior, match identity, game identity,
  deduplication, final reconciliation, secrets, raw logs, generated data,
  runtime status files, failed posts, or workbook exports from this module.
- Do not infer match winner, game winner, local player, play/draw, mulligans,
  event family, rank eligibility, or dashboard facts in this parser.
- Preserve current public field names unless a future contract explicitly
  updates every downstream consumer.
- Preserve fallback behavior for malformed MTGA payloads; novel MTGA shapes
  should not crash parser ingestion.

## Unknowns

- Whether every MTGA `matchGameRoomStateChangedEvent` shape includes
  `gameRoomConfig` for all queues and formats.
- Whether future MTGA payloads include explicit game numbers in final
  `resultList` entries.
- Whether `winningTeamId: 0` can ever be a valid MTGA team identifier in this
  event family. Current parser output uses `0` as the missing-value default;
  parser-state contracts should treat unknown-winner semantics explicitly.
- Whether `reservedPlayers` order always places the local player first. Current
  parser behavior preserves order but does not claim local-player truth.
- Whether bare payload shape without the wrapper marker still appears in live
  logs or is only preserved for compatibility.

## Suspected Gaps

- Focused tests do not yet cover invalid JSON or marker-present malformed JSON
  returning `None`.
- Focused tests do not yet cover unknown `stateType` mapping to
  `state_changed`.
- Focused tests do not yet cover non-dict wrapped payloads falling through to
  bare payload validation.
- Focused tests do not yet cover mixed valid/non-dict player lists.
- Focused tests do not yet cover malformed `resultList` values, skipped
  non-dict result entries, or result-order preservation independently.
- Focused tests do not yet assert `raw_match_state` presence and metadata raw
  bytes for successful parses.
- Current state behavior assigns MatchState game-scope final results by list
  order rather than explicit game numbers. This contract preserves parser order
  but does not bless that downstream assignment as complete final truth.

## Invariants

- `try_parse()` either returns `None` or a `MatchStateEvent`.
- Every successful payload includes `type`, `state_type`, `match_id`,
  `event_id`, `players`, and `raw_match_state`.
- `players` is always a list.
- `game_results`, when present, is always a list.
- `game_results` entries always use normalized snake_case
  `winning_team_id`, not raw `winningTeamId`.
- Raw `scope`, `result`, and `reason` values are preserved as payload facts.
- Result scopes must stay visible to downstream parser state.
- MatchState payloads are normalized parser facts, not workbook rows.
- The parser must remain tolerant of missing optional fields and malformed
  nested payload sections.

## Error Behavior

- Non-candidate bodies return `None`.
- Candidate bodies with no parseable JSON return `None`.
- Parsed JSON with no supported state-event dict returns `None`.
- Malformed nested dict fields degrade to empty dict behavior.
- Malformed player lists degrade to `[]`.
- Malformed final-result payloads omit final-result output fields.
- Malformed result lists degrade to `game_results: []` when final result is
  otherwise present.
- The parser should not raise for missing optional MTGA fields under normal
  ingestion.

## Side Effects

None.

This module must not mutate runtime parser state, environment variables,
secrets, raw logs, generated data, runtime status files, failed-post queues,
workbook exports, or webhook/App Script/workbook surfaces.

## Dependency Order

For future implementation work, inspect and update in this order:

1. `docs/contracts/parser_match_state.md`
2. `src/mythic_edge_parser/parsers/match_state.py`
3. `tests/test_match_state_parser.py`
4. `tests/test_parsers.py`
5. `docs/contracts/parser_state.md`, only if payload semantics change across
   the parser/state boundary.
6. Downstream app modules, only with an explicit problem representation and
   contract when behavior ownership changes.

## Compatibility

Must remain compatible with:

- Wrapped and bare match-room state JSON payload shapes.
- Existing payload keys: `type`, `state_type`, `match_id`, `event_id`,
  `players`, `raw_match_state`, `match_completed_reason`, `game_results`.
- Existing normalized event-type strings: `match_started`,
  `match_completed`, `state_changed`.
- Existing player key names: `user_id`, `player_name`, `system_seat_id`,
  `team_id`.
- Existing result key names: `scope`, `result`, `winning_team_id`, `reason`.
- Existing default values: blank strings for missing text, `0` for missing
  player team/seat IDs, `0` for missing result winner IDs, and empty lists for
  malformed list sources.
- `tests/test_parsers.py::test_match_state_parse`, which exercises the parser
  through the broader parser smoke-test surface.

Changing any of these compatibility surfaces requires a new or revised
contract that names affected parser state, transform, runtime surface, workbook,
webhook, and Apps Script expectations.

## Tests Required

Focused parser tests should cover:

- Wrapped payload parse for `MatchGameRoomStateType_Playing`.
- Bare payload parse compatibility.
- Completed-state parse with `finalMatchResult.resultList`.
- Config `eventId` preference over player `eventId`.
- Player `eventId` fallback when config `eventId` is missing or blank.
- `reservedPlayers` preference over `gameRoomInfo.players`.
- Fallback to `gameRoomInfo.players` when `reservedPlayers` is missing or
  empty.
- Malformed nested payload tolerance for non-dict config and final result.
- No-marker body returns `None`.
- Marker-present malformed JSON returns `None`.
- Parsed payload with no supported state-event dict returns `None`.
- Unknown `stateType` maps to `state_changed`.
- Mixed player lists skip non-dict entries and preserve valid player order.
- Missing player scalar fields use contracted defaults.
- Missing config/player event IDs produce `event_id == ""`.
- Non-list `resultList` produces `game_results == []` when final result exists.
- Mixed result lists skip non-dict entries and preserve valid result order.
- Missing result fields use contracted defaults, including
  `winning_team_id == 0`.
- Successful parse includes `raw_match_state`, metadata timestamp, and encoded
  raw bytes.

Focused state/consumer checks should continue to cover:

- MatchState final results populate game and match summaries through
  `state.py`.
- MatchState event rows are emitted only for `match_started` and
  `match_completed` event types.
- Analytics sidecar refresh/status gates continue to treat
  `type == "match_completed"` as the MatchState completion signal.

Recommended validation commands:

```powershell
py -m pytest -q tests/test_match_state_parser.py tests/test_parsers.py
py -m pytest -q tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py
py -m ruff check src tests
```

Documentation-only contract edits may use:

```powershell
git diff --check
```

## Acceptance Criteria

- The contract names `match_state.py` as the owner of match-room state event
  parsing and payload normalization.
- The contract names `state.py` as the owner of runtime state mutation and
  final reconciliation.
- Public parser interfaces and payload fields are explicit.
- Inputs, outputs, fallback behavior, side effects, and compatibility
  expectations are explicit.
- Game-scope and match-scope result preservation is required.
- Unknowns and suspected gaps are visible instead of hidden.
- Test obligations are concrete enough for Module Implementer to compare
  current code against the contract.
- No behavior, workbook schema, webhook shape, Apps Script behavior, parser
  state, extractor behavior, secrets, logs, generated data, runtime status
  files, failed posts, or workbook exports are changed by this contract thread.

## Next Workflow Action

Next role: Module Implementer (C)

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex C: Module Implementer for issue #16 and docs/contracts/parser_match_state.md.

Goal:
Compare the current match-state parser implementation and focused tests against the parser match-state module contract. Implement only the smallest coherent code and test changes needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/16
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- docs/agent_constitution.md
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/parser_match_state.md
- src/mythic_edge_parser/parsers/match_state.py
- tests/test_match_state_parser.py
- tests/test_parsers.py
- docs/contracts/parser_state.md
- docs/contracts/parser_extractors.md

Do:
- Compare observed code behavior against the contract before editing.
- Preserve parser-owned truth boundaries.
- Add focused tests for any contracted parser behavior not currently covered.
- Keep behavior changes minimal and parser-local unless the contract explicitly requires a downstream update.
- Produce docs/implementation_handoffs/parser_match_state_comparison.md with the comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, extractor behavior, match identity, game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Move parser-owned match-state truth into workbook formulas, dashboard logic, Apps Script, or AI-generated interpretation.
- Target main; module PR work belongs on codex/parser-module-audit-suite.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "#16"
  tracker: "#5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_match_state.md"
  target_artifact: "docs/implementation_handoffs/parser_match_state_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, extractor behavior, match identity, game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned match-state truth into workbook formulas, dashboard logic, Apps Script, or AI-generated interpretation."
    - "Do not target main for module PR work."
```

## Handoff Packet

Role performed: Module Contract Writer (B)

Source problem representation: GitHub issue #16, tracked under parser module
audit tracker #5.

Contract produced: `docs/contracts/parser_match_state.md`

Risk tier: High

Owning truth layer: parser and state interpretation. `match_state.py` owns
match-room state event recognition and payload normalization; `state.py` owns
runtime mutation and final reconciliation.

Public interface:

- `MATCH_STATE_MARKER`
- `try_parse(entry, timestamp)`
- `build_payload(state_event)`
- `MatchStateEvent.payload` fields documented above

Key invariants:

- Successful parses emit `MatchStateEvent`.
- Base payload fields are always present.
- Result scopes remain distinguishable.
- Final reconciliation is not performed in this parser.
- No side effects.

Required tests: focused parser tests listed in `Tests Required`, plus existing
consumer coverage for MatchState summary updates and row/status gates.

Acceptance criteria: listed above.

Open questions or contract risks:

- `winningTeamId: 0` semantics remain an explicit parser-state reconciliation
  concern.
- MatchState result list order is preserved because current state handling
  depends on it, but explicit game-number truth is not available in the current
  parser payload.
- Local-player identity cannot be trusted from player order alone.

Next recommended thread role: Module Implementer (C).
