# GRE GameState Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/26

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_gre_game_state.md`

## Role Performed

Codex C: Module Implementer.

## Summary

Compared `src/mythic_edge_parser/parsers/gre/game_state.py`,
`src/mythic_edge_parser/parsers/gre/__init__.py`,
`src/mythic_edge_parser/parsers/gre/turn_info.py`, downstream consumer tests,
and focused parser tests against the GRE GameState parser contract.

No parser behavior mismatch was found. The implementation matches the contract
for regular and queued payload construction, output field names, defaults,
identity and turn-info consumption, shallow copy/reference behavior, integer
normalization boundaries, raw GRE payload preservation, malformed optional
sections, dispatch precedence, queued fallback, connect-response precedence,
and game-over paired event emission.

The comparison did find focused test gaps listed by the contract. I added
focused tests only. No runtime/parser implementation code changed.

## Confirmed Matches

- `QUEUED_GAME_STATE_MESSAGE_TYPE` is
  `"GREMessageType_QueuedGameStateMessage"`.
- `build_game_state_payload(message, gsm)` remains the public helper imported
  by GRE dispatch.
- The helper does not create event objects, inspect raw log text, mutate parser
  state, post webhooks, write logs, or perform workbook/export side effects.
- Payload `type` is `"queued_game_state_message"` only when
  `message.type == "GREMessageType_QueuedGameStateMessage"`; otherwise it is
  `"game_state_message"`.
- `message_type`, `msg_id`, and `game_state_id` pass through from the raw GRE
  message with documented defaults.
- `system_seat_ids`, `diff_deleted_instance_ids`, and
  `diff_deleted_persistent_annotation_ids` use
  `api_common.normalize_int_list()`.
- `game_info` is a shallow dict copy when `gsm.gameInfo` is a dict, otherwise
  `{}`.
- `turn_info` comes from `turn_info.build_turn_info(gsm)` and is not a raw
  `turnInfo` copy.
- `identity` is a new dict built from `game_info` and `turn_info`.
- Top-level `stage`, `match_state`, `turn_number`, and
  `active_player_seat_id` align with the contracted identity/game-info/
  turn-info sources.
- List sections use shallow list copies and preserve non-dict members at the
  parser layer.
- `update` stringifies truthy values and maps falsey values to `""`.
- `pending_message_count`, `prev_game_state_id`, and `identity.game_number`
  use local Python `int()` conversion behavior.
- `raw_game_state` preserves the original raw GRE message object.
- GRE dispatch parses top-level GRE message dicts and
  `greToClientEvent.greToClientMessages` lists.
- Non-dict batch members are ignored.
- Invalid `greToClientMessages` shape returns `[]`.
- Current `gameStateMessage` takes precedence over queued nested game-state
  payloads when both are present.
- Missing/non-dict current `gameStateMessage` falls back to dict
  `queuedGameStateMessage.gameStateMessage`.
- Missing or malformed selected game-state payloads emit no game-state event.
- Game-state payload emission takes precedence over connect-response emission
  for a message containing both sections.
- Regular and queued game-state dispatch emits `GameStateEvent` with
  `INTERACTIVE_DISPATCH` performance class.
- Game-over regular and queued game-state dispatch emits `GameStateEvent`
  before `GameResultEvent`, sharing metadata from the full raw log body.
- Downstream state, extractor, transform, gameplay-action, runtime, candidate,
  and regression tests continue consuming parser-produced GameState payloads.

## Contract Mismatches

None found.

No parser behavior changes were required.

## Missing Safeguards

None found in `game_state.py` or GRE dispatch.

The contracted safeguards are present:

- malformed optional dict/list sections degrade to neutral defaults
- non-list ID sections normalize to `[]`
- non-dict list items are preserved at the parser layer
- raw GRE message evidence remains available through `raw_game_state`
- game-state emission remains higher precedence than connect-response emission
- game-over paired event ordering remains stable
- the helper remains side-effect free

## Missing Or Weak Tests

The contract's suspected focused test gaps were confirmed in the pre-change
tests. They were addressed by focused additions to:

- `tests/test_gre_game_state_parser.py`
- `tests/test_parsers.py`

Tests added or strengthened:

- full happy-path helper payload fields and pass-through/default behavior
- missing message fields defaulting to regular payload type and default message
  type
- missing/non-dict `turnInfo` neutral output and top-level turn shortcuts
- missing/non-list list sections returning `[]`
- missing/non-list diff ID fields returning `[]`
- `api_common.normalize_int_list()` behavior for game-state ID lists,
  including bool/float/signed-string rejection and digit-string acceptance
- local `_maybe_int()` behavior for bools, floats, signed strings, and
  whitespace-padded integer strings
- non-dict list members preserved by `game_state.py`
- top-level list copies separated from raw list length mutation
- nested list item aliasing remains visible and intentionally shallow
- direct top-level GRE `gameStateMessage` dispatch
- current `gameStateMessage` precedence over queued nested game state
- malformed selected game-state shapes returning no game-state event
- regular `GameStateEvent` metadata, event class, performance class, raw
  bytes, and dispatch timestamp

Remaining non-blocking test notes:

- No standalone `turn_info.py` behavior was changed; its existing focused tests
  continue covering the adjacent helper.
- No new downstream state/extractor/transform/gameplay/runtime tests were
  added because no downstream behavior changed and existing downstream
  compatibility suites passed.
- Deep-copy isolation for nested list/dict entries remains intentionally
  outside the current contract.
- Any future decision to reject bools/floats in local `_maybe_int()` or to
  change `msg_id` / `game_state_id` pass-through behavior requires a new
  problem representation and contract.

## Files Changed

- `tests/test_gre_game_state_parser.py`
- `tests/test_parsers.py`
- `docs/implementation_handoffs/parser_gre_game_state_comparison.md`

## Code Changed

No runtime code changed.

No parser behavior, parser state final reconciliation, workbook schema, webhook
payload shape, Apps Script behavior, parser event classes, extractor behavior,
match/game identity, deduplication, secrets, environment variables, raw logs,
generated data, runtime status files, failed posts, or workbook exports
changed.

## Validation Evidence

Baseline checks before adding tests:

```bash
python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_turn_info_parser.py tests/test_parsers.py
# Pass: 21 passed in 0.06s.

python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py
# Pass: 85 passed in 0.16s.

python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
# Pass: 29 passed in 0.17s.
```

Checks after adding focused tests:

```bash
python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_turn_info_parser.py tests/test_parsers.py
# Pass: 27 passed in 0.07s.

python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py
# Pass: 85 passed in 0.15s.

python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
# Pass: 29 passed in 0.16s.

python3 -m ruff check src tests
# Pass: All checks passed!
```

Protected runtime-source diff check:

```bash
git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
# Pass: no runtime implementation files changed.
```

Final documentation/worktree validation:

```bash
git diff --check
# Pass: no whitespace errors.

python3 -m pytest -q
# Pass: 476 passed in 0.96s.
```

## Still-Unverified Layers

- Live workbook behavior was not checked; no workbook schema or workbook export
  behavior was in scope.
- Deployed Apps Script behavior was not checked; no Apps Script behavior was in
  scope.
- GitHub Actions were not checked because no PR exists for this module yet.

## Next Recommended Role

Codex E: Module Reviewer in contract-test mode.

No Codex D fixer pass is recommended because no behavior mismatch or failing
validation remains after the focused test additions.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #26:
https://github.com/Tahjali11/Mythic-Edge/issues/26

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_gre_game_state.md
- docs/implementation_handoffs/parser_gre_game_state_comparison.md
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

Goal:
Verify the Module Implementer comparison and focused test additions against the GRE GameState parser contract.

Confirm:
- build_game_state_payload() returns the contracted payload fields, defaults, shallow copy/reference behavior, and raw_game_state preservation.
- regular and queued payload type strings stay stable.
- message_type, msg_id, and game_state_id remain pass-through/default fields.
- game_info, turn_info, identity, stage, match_state, turn_number, and active_player_seat_id align with the contracted sources.
- system_seat_ids and diff ID lists use api_common.normalize_int_list() semantics.
- local _maybe_int() fields preserve current Python int() behavior for bools, floats, signed strings, and whitespace-padded integer strings.
- non-dict list members are preserved by game_state.py and nested list item aliasing remains shallow.
- direct top-level GRE messages and batched GRE messages dispatch as contracted.
- current gameStateMessage takes precedence over queued nested game-state payloads.
- queued nested fallback emits GameStateEvent when current gameStateMessage is missing or malformed.
- malformed selected game-state shapes emit no game-state event.
- game-state emission remains higher precedence than connect-response emission on the same message.
- game-over regular and queued game-state messages emit GameStateEvent before GameResultEvent.
- emitted events preserve expected event classes, performance classes, timestamp, raw body bytes, and metadata sharing where contracted.
- downstream state, extractor, transform, gameplay-action, runtime, candidate, and regression tests still consume parser-produced GameState payloads without moving raw GRE truth downstream.
- no parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match/game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

Validation:
Run:
python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_turn_info_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py
python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
python3 -m pytest -q
python3 -m ruff check src tests
git diff --check

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not stage, commit, merge, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/26"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_gre_game_state.md"
  target_artifact: "docs/implementation_handoffs/parser_gre_game_state_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_turn_info_parser.py tests/test_parsers.py"
    - "python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py"
    - "python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests"
    - "git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py"
    - "git diff --check"
  stop_conditions:
    - "Route to Module Contract Writer if the contract is ambiguous or inaccurate."
    - "Route to Module Fixer if reviewer finds a concrete parser behavior or focused-test mismatch."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned game-state truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not expand into the standalone turn_info.py audit unless a boundary conflict must be routed."
    - "Do not target main unless explicitly approved."
```
