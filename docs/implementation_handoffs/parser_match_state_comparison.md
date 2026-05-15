# Parser Match State Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/16

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Issue #16 is a high-risk parser module audit for
`src/mythic_edge_parser/parsers/match_state.py`. The issue names
match-state parsing as parser-owned truth and keeps parser state, workbook,
webhook, Apps Script, dashboard, and final reconciliation behavior out of scope
for this module unless a later contract explicitly changes them.

## Contract

`docs/contracts/parser_match_state.md`

## Role Performed

Module Implementer / comparison thread.

This pass compared the current match-state parser implementation, focused
parser tests, parser smoke tests, and named downstream consumers against the
parser match-state contract.

## Current Behavior Summary

`match_state.py` is aligned with the contract. It detects
`matchGameRoomStateChangedEvent` bodies, accepts wrapped and bare
`gameRoomInfo` payload shapes when the marker is present, emits
`MatchStateEvent` with stable normalized payload fields, preserves raw
match-state payloads, preserves final result scopes and order, and degrades
malformed nested data to contracted defaults.

No parser code change was needed. This implementation pass added focused tests
for missing contract obligations and edge cases.

## Confirmed Matches

- `MATCH_STATE_MARKER` is the public candidate marker.
- `try_parse(entry, timestamp)` returns `None` for non-candidates,
  unparseable JSON, and parsed JSON with no supported state-event dict.
- `try_parse()` emits `MatchStateEvent` with the passed timestamp and encoded
  raw body when parsing succeeds.
- Wrapped payloads are preferred when the wrapper value is a dict.
- Bare `gameRoomInfo` payloads are accepted when the marker is present and the
  parsed root has a dict `gameRoomInfo`.
- `build_payload(state_event)` always produces the contracted base fields:
  `type`, `state_type`, `match_id`, `event_id`, `players`, and
  `raw_match_state`.
- State type mapping matches the contract:
  `MatchGameRoomStateType_Playing` becomes `match_started`,
  `MatchGameRoomStateType_MatchCompleted` becomes `match_completed`, and
  unknown values become `state_changed`.
- Player source precedence matches the contract: non-empty
  `gameRoomConfig.reservedPlayers` wins, otherwise `gameRoomInfo.players` is
  used.
- Non-list player containers normalize to `[]`; non-dict player entries are
  skipped; valid player order is preserved; missing player fields use the
  contracted defaults.
- Event ID precedence matches the contract: trimmed config `eventId` wins,
  then first selected-player `eventId`, then `""`.
- Final result extraction matches the contract: a non-empty dict
  `finalMatchResult` adds `match_completed_reason` and `game_results`;
  malformed or missing final result omits those fields.
- `resultList` values that are not lists normalize to `game_results: []` when
  the final result is otherwise present.
- Non-dict result entries are skipped, valid result order is preserved, and
  missing result fields use contracted defaults including
  `winning_team_id == 0`.
- Match-scope and game-scope result entries stay distinguishable through the
  normalized `scope` field.
- The module has no file I/O, webhook submission, workbook mutation, Apps
  Script mutation, parser-state mutation, environment access, raw-log writes,
  generated-data refresh, runtime status writes, failed-post access, or
  workbook export access.

## Contract Mismatches

No contract mismatches were found.

No parser behavior changed. No workbook schema, webhook payload shape, Apps
Script behavior, parser state final reconciliation, extractor behavior, match
identity, game identity, deduplication, secrets, raw logs, generated data,
runtime status files, failed posts, or workbook exports changed.

## Missing Or Weak Tests

Resolved in this implementation pass:

- Added coverage that successful parses preserve `metadata.timestamp`,
  `metadata.raw_bytes`, `performance_class`, and `raw_match_state`.
- Added coverage for no-marker bodies returning `None`.
- Added coverage for marker-present malformed JSON returning `None`.
- Added coverage for parsed payloads with no supported state-event dict
  returning `None`.
- Added coverage for non-dict wrapper values falling through to bare
  `gameRoomInfo` validation.
- Added coverage for unknown `stateType` values mapping to `state_changed`.
- Added coverage for mixed player lists skipping non-dict entries and using
  missing-field defaults.
- Added coverage for blank config event IDs falling back to selected-player
  event IDs.
- Added coverage for config event IDs taking precedence over player event IDs.
- Added coverage for empty `reservedPlayers` falling back to
  `gameRoomInfo.players`.
- Added coverage for non-list `resultList` producing `game_results == []`.
- Added coverage for mixed/partial result lists skipping non-dict entries,
  preserving order, preserving scope, and using result defaults.

Remaining non-blocking gaps:

- The parser still does not infer explicit game numbers from
  `finalMatchResult.resultList`. This is documented as an unknown/contract risk,
  and no such source field is currently contracted.
- `raw_match_state` remains shallow-copied through the event payload copy. The
  contract explicitly tells callers to treat it as read-only.
- Future MTGA payload-shape drift remains a normal parser audit risk.

## Files Changed

- `tests/test_match_state_parser.py`
- `docs/implementation_handoffs/parser_match_state_comparison.md`

## Code Changed

None.

## Tests Changed

Focused tests were added to `tests/test_match_state_parser.py` only. They
exercise contract-required parser behavior and malformed-shape tolerance without
changing implementation behavior.

## Interface Changes

None.

No function signatures, event classes, payload field names, workbook columns,
environment variables, Apps Script entrypoints, match identity rules, game
identity rules, deduplication behavior, final reconciliation behavior, or
runtime artifact shapes changed.

## Validation Evidence

Static inspection:

- Reviewed `docs/agent_constitution.md`.
- Reviewed `docs/agent_threads/implementation.md`.
- Reviewed `docs/codex_module_workflow.md`.
- Reviewed GitHub issue #16 and tracker #5.
- Compared `docs/contracts/parser_match_state.md`.
- Compared `src/mythic_edge_parser/parsers/match_state.py`.
- Compared `tests/test_match_state_parser.py`.
- Compared `tests/test_parsers.py`.
- Inspected downstream MatchState consumers in `state.py`, `transforms.py`,
  and `analytics_sidecar.py`.
- Inspected `api_common.parse_json_from_body()` and `MatchStateEvent`
  metadata/performance-class behavior.

Focused parser validation:

```bash
python3 -m pytest -q tests/test_match_state_parser.py tests/test_parsers.py
```

Result:

```text
24 passed in 0.04s
```

Related consumer validation:

```bash
python3 -m pytest -q tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py
```

Result:

```text
22 passed in 0.11s
```

Lint:

```bash
python3 -m ruff check src tests
```

Result:

```text
All checks passed!
```

Full repo validation:

```bash
python3 -m pytest -q
```

Result:

```text
396 passed in 0.97s
```

## Still Unverified

- Live MTGA log replay with newly observed payload variants was not performed.
- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Webhook dispatch was not exercised.
- Runtime dashboard/UI behavior was not manually inspected.

## Reviewer Focus

Ask the Module Reviewer to verify:

- New tests exactly cover the contract rather than expanding behavior.
- Wrapped and bare payload compatibility remains intact.
- Non-dict wrapper fallback to bare `gameRoomInfo` is an intentional current
  behavior and not a downstream truth leak.
- `raw_match_state` remains parser/debug payload data and does not become
  workbook-facing schema.
- Game-scope and match-scope result entries remain distinguishable and are not
  reconciled in `match_state.py`.
- No parser state, workbook, webhook, Apps Script, extractor, final
  reconciliation, match identity, game identity, deduplication, secrets, raw
  logs, generated data, runtime status files, failed posts, or workbook exports
  changed.

## Next Recommended Role

Module Reviewer in contract-test mode.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #16, docs/contracts/parser_match_state.md, and docs/implementation_handoffs/parser_match_state_comparison.md.

Review the match-state parser implementation and Module Implementer changes in:
- src/mythic_edge_parser/parsers/match_state.py
- tests/test_match_state_parser.py
- tests/test_parsers.py
- docs/contracts/parser_match_state.md
- docs/implementation_handoffs/parser_match_state_comparison.md

Verify the implementation against the parser match-state contract. Confirm marker/JSON behavior, wrapped and bare payload compatibility, normalized output fields, state-type mapping, player normalization, event-id precedence, final-result extraction, malformed-shape tolerance, raw payload preservation, and parser truth boundaries. Confirm no workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, extractor behavior, match identity, game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

Produce docs/contract_test_reports/parser_match_state.md with findings first if any, contract-test verdict, validation evidence, remaining gaps, next recommended role, and a workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/16"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/implementation_handoffs/parser_match_state_comparison.md"
  target_artifact: "docs/contract_test_reports/parser_match_state.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_match_state_parser.py tests/test_parsers.py (24 passed)"
    - "python3 -m pytest -q tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py (22 passed)"
    - "python3 -m ruff check src tests (All checks passed)"
    - "python3 -m pytest -q (396 passed)"
  stop_conditions:
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, parser state final reconciliation, extractor behavior, match identity, game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned match-state truth into workbook formulas, dashboard logic, Apps Script, or AI-generated interpretation."
    - "Do not target main for module PR work."
```
