# GRE Turn Info Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/28

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_gre_turn_info.md`

## Role Performed

Codex C: Module Implementer.

## Summary

Compared `src/mythic_edge_parser/parsers/gre/turn_info.py`,
`src/mythic_edge_parser/parsers/gre/game_state.py`, downstream consumer tests,
and focused parser tests against the GRE Turn Info parser contract.

No parser behavior mismatch was found. The implementation matches the contract
for helper API shape, missing/non-dict/empty-dict behavior, eight-field
normalized output, active-player precedence, local integer conversion,
string-field conversion, no raw turn-info preservation, no side effects, and
game-state consumed-output compatibility.

The comparison did find focused test gaps listed by the contract. I added
focused tests only. No runtime/parser implementation code changed.

## Confirmed Matches

- `build_turn_info(gsm)` remains the public parser helper imported by
  `game_state.py`.
- The helper reads only `gsm["turnInfo"]` when that value is a dictionary.
- Missing, non-dict, and empty-dict `turnInfo` return `{}`.
- Non-empty `turnInfo` dictionaries return exactly the contracted snake_case
  output field set.
- Unknown extra raw `turnInfo` keys are ignored.
- `active_player_seat_id` uses `activePlayer` before `activePlayerSeatId`.
- `activePlayer` falls back to `activePlayerSeatId` only when the raw
  `activePlayer` value is `None` or `""`.
- Present but unconvertible `activePlayer` values do not fall back after
  conversion failure.
- Integer-like fields use local Python `int()` conversion and return `None`
  only for `TypeError` or `ValueError`.
- Boolean, float, signed-string, and whitespace-padded integer-string behavior
  matches the contract's current compatibility rule.
- String-like fields use `str(value or "")`.
- Falsy string-like values become `""`; truthy non-string values become their
  Python `str()` representation.
- The helper returns a new normalized dict and does not mutate `gsm` or the raw
  `turnInfo` dict.
- The helper does not preserve raw `turnInfo`; raw game-state evidence remains
  owned by `game_state.py`.
- `game_state.py` carries the helper return value at `payload["turn_info"]`.
- `game_state.py` mirrors only `turn_number`, `active_player_seat_id`, `phase`,
  and `step` into identity/top-level shortcuts as contracted.
- Downstream state, extractor, transform, runtime, gameplay-action, candidate,
  and regression tests continue consuming parser-produced turn context.

## Contract Mismatches

None found.

No parser behavior changes were required.

## Missing Safeguards

None found in `turn_info.py`.

The contracted safeguards are present:

- malformed or absent optional `turnInfo` values degrade to neutral outputs
- unsupported direct non-dict helper inputs remain outside the public contract
- conversion failures become `None` for integer-like fields
- missing/malformed string-like fields become `""`
- helper output does not include raw payloads
- the helper has no event, state, webhook, workbook, file, or runtime side
  effects

## Missing Or Weak Tests

The contract's suspected focused test gaps were confirmed in the pre-change
tests. They were addressed by focused additions to:

- `tests/test_gre_turn_info_parser.py`

Tests added or strengthened:

- empty-dict `turnInfo` returning `{}`
- unknown extra raw keys ignored by exact output equality
- `activePlayer` winning over `activePlayerSeatId` when both are present
- `activePlayer == ""` and `activePlayer is None` fallback behavior
- present `activePlayer` values `0`, `False`, `"bad"`, `[]`, and `{}` not
  falling back after selection
- local integer conversion for whitespace-padded strings, signed strings,
  booleans, floats, fractional strings, objects, and invalid strings
- string conversion for `0`, `False`, empty list, empty dict, and truthy
  non-string values
- no input mutation when mutating the returned normalized dict
- `game_state.py` consumed-output compatibility, including carry-through at
  `payload["turn_info"]` and identity/top-level shortcut alignment

Remaining non-blocking test notes:

- No runtime or downstream tests were changed because no downstream behavior
  changed and existing downstream compatibility suites passed.
- Direct non-dict calls to `build_turn_info()` remain outside the public
  contract and were not hardened.
- Any future decision to reject bools/floats, change active-player fallback,
  or preserve raw `turnInfo` inside helper output requires a new problem
  representation and contract.

## Files Changed

- `tests/test_gre_turn_info_parser.py`
- `docs/implementation_handoffs/parser_gre_turn_info_comparison.md`

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
python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_parsers.py
# Pass: 27 passed in 0.12s.

python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_transforms.py
# Pass: 54 passed in 0.17s.

python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_gameplay_actions.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
# Pass: 37 passed in 0.30s.
```

Checks after adding focused tests:

```bash
python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_parsers.py
# Pass: 38 passed in 0.07s.

python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_transforms.py
# Pass: 54 passed in 0.20s.

python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_gameplay_actions.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
# Pass: 37 passed in 0.61s.

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
# Pass: 487 passed in 1.23s.
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
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #28:
https://github.com/Tahjali11/Mythic-Edge/issues/28

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_gre_turn_info.md
- docs/implementation_handoffs/parser_gre_turn_info_comparison.md
- src/mythic_edge_parser/parsers/gre/turn_info.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- tests/test_gre_turn_info_parser.py
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
- tests/test_grp_id_candidates.py
- tests/test_parser_regressions.py

Goal:
Verify the Module Implementer comparison and focused test additions against the GRE Turn Info parser contract.

Confirm:
- build_turn_info() returns {} for missing, non-dict, and empty-dict turnInfo.
- non-empty turnInfo returns exactly the eight contracted snake_case fields.
- unknown raw turnInfo keys are ignored.
- activePlayer takes precedence over activePlayerSeatId.
- activePlayer fallback happens only for None and "".
- present but unconvertible activePlayer values do not fall back after conversion failure.
- local _maybe_int() preserves current Python int() behavior for bools, floats, signed strings, and whitespace-padded integer strings.
- fractional strings and invalid integer-like values become None.
- local _string_field() preserves str(value or "") behavior for missing, falsey, and truthy non-string values.
- build_turn_info() does not mutate gsm or raw turnInfo.
- raw turnInfo preservation remains out of turn_info.py and owned by game_state.py raw_game_state preservation.
- game_state.py carries turn_info exactly as returned and mirrors only contracted fields into identity/top-level shortcuts.
- downstream state, extractor, transform, runtime, gameplay-action, candidate, and regression tests still consume parser-produced turn context without moving raw GRE truth downstream.
- no parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match/game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

Validation:
Run:
python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_transforms.py
python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_gameplay_actions.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/28"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_gre_turn_info.md"
  target_artifact: "docs/implementation_handoffs/parser_gre_turn_info_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_parsers.py"
    - "python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_transforms.py"
    - "python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_gameplay_actions.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests"
    - "git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py"
    - "git diff --check"
  stop_conditions:
    - "Route to Module Contract Writer if the contract is ambiguous or inaccurate."
    - "Route to Module Fixer if reviewer finds a concrete parser behavior or focused-test mismatch."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned turn-info truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not reopen the completed gre/game_state.py audit except for consumed-output compatibility."
    - "Do not target main unless explicitly approved."
```
