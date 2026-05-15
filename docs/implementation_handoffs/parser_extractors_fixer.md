# Parser Extractors Module Fixer Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/9

## Contract

`docs/contracts/parser_extractors.md`

## Source Finding

`docs/contract_test_reports/parser_extractors.md`

## Role Performed

Module Fixer thread (D).

This pass addressed the parser-extractor contract-test report findings with focused tests first. Production code was changed only where those focused tests confirmed malformed optional inputs should degrade to neutral fallback values.

## What Changed

- Added focused extractor tests for malformed safe-player inputs, primitive helper edge cases, game-result identity fallback behavior, match-scope result filtering, starting-player return-shape semantics, local private hand owner-seat behavior, gameplay actions/annotations fallback behavior, and timestamp helpers.
- Added small neutral-fallback guards in `src/mythic_edge_parser/app/extractors.py`:
  - `_safe_local_player()` now returns `{}` for non-list inputs and non-dictionary selected players.
  - `_extract_game_result_identity()` now coerces malformed `game_info` and `context` values through safe dictionary handling.
  - `_has_match_scope_result()` now skips non-dictionary `results` entries.

## Files Changed

- `src/mythic_edge_parser/app/extractors.py`
- `tests/test_app_extractors.py`
- `docs/implementation_handoffs/parser_extractors_fixer.md`

## Interface Changes

None.

No function names, signatures, payload fields, workbook columns, model row fields, Apps Script entrypoints, environment variables, state ownership, or raw parser modules changed.

## Tests Added Or Updated

- `tests/test_app_extractors.py`
  - `_safe_local_player()` configured-index, fallback, and malformed-input coverage.
  - `_first_present()`, `_maybe_int()`, `_safe_dict()`, and `_safe_list()` edge coverage.
  - `_maybe_int()` bool and float behavior documentation.
  - `_extract_game_result_identity()` malformed `game_info` and missing-context-key fallback coverage.
  - `_has_match_scope_result()` non-dictionary result-entry coverage.
  - `_extract_starting_player_from_client_action()` raw return-shape coverage.
  - `_extract_starting_player_from_game_state()` team-ID versus seat-ID behavior coverage.
  - `_extract_local_private_hand_instance_ids()` malformed owner-seat and first matching private hand coverage.
  - `_game_state_actions()` and `_game_state_annotations()` fallback coverage.
  - `_event_datetime()` and `_safe_iso()` timestamp coverage.

## Validation Run

```powershell
py -m pytest -q tests/test_app_extractors.py
py -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_gre_game_result_parser.py tests/test_gre_game_state_parser.py tests/test_parser_regressions.py
py -m ruff check src tests
py -m pytest -q
```

Results:

```text
28 passed in 0.15s
50 passed in 0.95s
All checks passed!
356 passed in 3.34s
```

## Forbidden Scope

Forbidden scope was not touched.

This pass did not change workbook schema, webhook payload shape, deployed Apps Script behavior, row field names in `models.py`, state ownership in `state.py`, raw parser modules, secrets, environment variables, live workbook state, debug/archive/helper/runtime layers, or observability layers.

## Still Unverified

- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- GitHub Actions were not checked from this local thread.
- Full PR state and branch publication were not checked.

## Remaining Review Focus

- Confirm that accepting current `_maybe_int()` bool and float behavior as documented test coverage is acceptable for issue #9.
- Confirm that local private hand behavior for malformed owner seats and first matching private hand zones should remain current behavior.
- Confirm that `_event_datetime()` nondeterministic local fallback remains acceptable for runner partitioning.

## Next Recommended Thread Role

Module Reviewer (E).
