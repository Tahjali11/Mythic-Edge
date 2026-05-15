# GRE GameState Parser Contract-Test Report

## Findings

No blocking findings.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/26

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_gre_game_state.md`

## Implementation Under Test

Branch: `codex/parser-module-audit-suite`

Implementation handoff:
`docs/implementation_handoffs/parser_gre_game_state_comparison.md`

Reviewed source surfaces:

- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/turn_info.py`
- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`
- `src/mythic_edge_parser/parsers/api_common.py`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`

Changed-file scope reviewed:

- `tests/test_gre_game_state_parser.py`
- `tests/test_parsers.py`
- `docs/contracts/parser_gre_game_state.md`
- `docs/implementation_handoffs/parser_gre_game_state_comparison.md`
- `docs/contract_test_reports/parser_gre_game_state.md`

Runtime implementation code was not changed.

## Contract Summary

`src/mythic_edge_parser/parsers/gre/game_state.py` must build stable
parser-owned `GameStateEvent.payload` dictionaries for regular and queued GRE
game-state messages. It owns payload type selection, message metadata
pass-through/defaults, normalized seat and diff ID lists, game-info and
turn-info consumption, identity shortcuts, shallow list/dict copy behavior,
raw GRE message preservation, dispatch precedence, queued nested fallback, and
paired game-over emission with `GameResultEvent`.

The contract does not own parser state final reconciliation, workbook schema,
webhook payload shape, Apps Script behavior, parser event class definitions,
extractor behavior, match/game identity policy beyond parsed fields,
deduplication, secrets, environment variables, raw logs, generated data,
runtime status files, failed posts, or workbook exports.

## Checks Run

```bash
python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_turn_info_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py
python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
python3 -m pytest -q
python3 -m ruff check src tests
git diff --check
git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
```

## Results

- `python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_turn_info_parser.py tests/test_parsers.py`
  -> `27 passed in 0.07s`.
- `python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py`
  -> `85 passed in 0.23s`.
- `python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py`
  -> `29 passed in 0.25s`.
- `python3 -m pytest -q` -> `476 passed in 1.15s`.
- `python3 -m ruff check src tests` -> `All checks passed!`.
- `git diff --check` -> passed with no output.
- `git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py`
  -> passed with no output.

## Contract-Test Verdict

Pass.

The Module Implementer comparison and focused test additions match the GRE
GameState parser contract. The prior suspected test gaps are covered, and no
behavior mismatch was found.

## Confirmed Contract Matches

- `build_game_state_payload()` returns the contracted payload fields,
  defaults, shallow copy/reference behavior, and `raw_game_state`
  preservation.
- Regular and queued payload type strings remain stable:
  `game_state_message` and `queued_game_state_message`.
- `message_type`, `msg_id`, and `game_state_id` remain pass-through/default
  fields.
- `game_info`, `turn_info`, `identity`, `stage`, `match_state`,
  `turn_number`, and `active_player_seat_id` align with the contracted
  sources.
- `system_seat_ids`, `diff_deleted_instance_ids`, and
  `diff_deleted_persistent_annotation_ids` use
  `api_common.normalize_int_list()` semantics.
- Local `_maybe_int()` fields preserve current Python `int()` behavior for
  bools, floats, signed strings, and whitespace-padded integer strings.
- Non-dict list members are preserved by `game_state.py`.
- Top-level list outputs are copied, while nested list item aliasing remains
  intentionally shallow.
- Direct top-level GRE messages and batched GRE messages dispatch as
  contracted.
- Current `gameStateMessage` takes precedence over queued nested game-state
  payloads.
- Queued nested fallback emits `GameStateEvent` when current
  `gameStateMessage` is missing or malformed.
- Missing or malformed selected game-state shapes emit no game-state event.
- Game-state emission remains higher precedence than connect-response emission
  on the same message.
- Game-over regular and queued game-state messages emit `GameStateEvent`
  before `GameResultEvent`.
- Emitted events preserve expected event classes, performance classes,
  dispatch timestamp, raw body bytes, and shared metadata for paired game-over
  events where contracted.
- Downstream state, extractor, transform, gameplay-action, runtime, candidate,
  and regression tests continue consuming parser-produced GameState payloads
  without moving raw GRE truth downstream.
- No parser state final reconciliation, workbook schema, webhook payload
  shape, Apps Script behavior, parser event classes, extractor behavior,
  match/game identity, deduplication, final reconciliation, secrets,
  environment variables, raw logs, generated data, runtime status files,
  failed posts, or workbook exports changed.

## Contract Mismatches

None.

## Missing Tests

None blocking.

Focused coverage now includes:

- helper happy-path output shape and pass-through/default behavior
- missing message fields and malformed optional sections
- non-list list and diff-list defaults
- `api_common.normalize_int_list()` behavior for game-state ID lists
- local `_maybe_int()` bool, float, signed-string, and whitespace-padded string
  behavior
- non-dict list member preservation
- top-level list copy separation and shallow nested item aliasing
- direct top-level GRE game-state dispatch
- current game-state precedence over queued nested game state
- malformed selected game-state shapes returning no events
- regular `GameStateEvent` metadata, event class, performance class, raw bytes,
  and timestamp

Existing compatibility suites continue covering downstream parser-produced
payload consumption.

## Drift Notes

- No parser behavior drift found.
- No parser truth drift found; GameState interpretation remains in the parser
  layer.
- No downstream ownership drift found; downstream consumers continue using
  parser-produced fields and existing extractor surfaces.
- No parser state final reconciliation drift found in the reviewed surface.
- No workbook/webhook/App Script/runtime artifact drift found in the reviewed
  surface.
- No protected runtime-source files changed.

## Remaining Non-Blocking Gaps

- GitHub Actions were not checked because no PR exists for this module yet.
- Live workbook behavior was not checked; workbook schema and exports are out
  of scope.
- Deployed Apps Script behavior was not checked; Apps Script behavior is out
  of scope.
- Standalone `turn_info.py` ownership remains outside this audit except for the
  consumed output boundary.

## Recommendation

Approve for submitter work.

Next recommended role: Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for issue #26 and the GRE GameState parser contract audit.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/26

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_gre_game_state.md
- docs/implementation_handoffs/parser_gre_game_state_comparison.md
- docs/contract_test_reports/parser_gre_game_state.md
- tests/test_gre_game_state_parser.py
- tests/test_parsers.py

Reviewer verdict:
No blocking findings. The GRE GameState parser contract audit is ready for submitter work.

Submitter requirements:
- Verify current branch and changed-file scope.
- Stage only the reviewed GRE GameState parser audit artifacts.
- Commit and push the branch.
- Open or update a draft PR targeting codex/parser-module-audit-suite, not main.
- Do not merge, close issue #26, or mark tracker #5 complete; those are Codex G responsibilities.

Validation to run or verify:
python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_turn_info_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py
python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
python3 -m pytest -q
python3 -m ruff check src tests
git diff --check

Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not merge, close issue #26, mark tracker #5 complete, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/26"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_gre_game_state.md"
  target_artifact: "docs/contract_test_reports/parser_gre_game_state.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_gre_game_state_parser.py tests/test_gre_turn_info_parser.py tests/test_parsers.py -> 27 passed in 0.07s"
    - "python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_state.py tests/test_app_extractors.py tests/test_gameplay_actions.py -> 85 passed in 0.23s"
    - "python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py -> 29 passed in 0.25s"
    - "python3 -m pytest -q -> 476 passed in 1.15s"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "git diff --check -> passed with no output"
    - "git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py -> passed with no output"
  stop_conditions:
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not change parser state final reconciliation or GRE GameResult winner precedence from this GameState audit."
    - "Do not move parser-owned game-state truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not expand into the standalone turn_info.py audit unless a boundary conflict must be routed."
    - "Do not merge, close issue #26, or mark tracker #5 complete; route deployer work to Codex G."
    - "Do not target main unless explicitly approved."
```
