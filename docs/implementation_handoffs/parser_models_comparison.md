# Parser Models Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/2

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

The implementation comparison originally used `docs/contracts/parser_models.md`, which records that issue #2 was already read when the contract was drafted. The Module Fixer follow-up verified GitHub access for issue #2, tracker issue #5, and PR #3.

## Contract

`docs/contracts/parser_models.md`

## Role Performed

Implementation / comparison thread.

This pass compared the current `src/mythic_edge_parser/app/models.py` implementation and focused tests against the parser models contract. It did not assume a known bug.

## What The Code Is Supposed To Do

`models.py` is supposed to hold parser-owned match and game summary objects after `state.py` has interpreted MTGA events. Its serializers turn those parser facts into stable workbook-facing rows and runtime-history payloads.

Plain English: `models.py` should shape already-known facts. It should not parse raw logs, post webhooks, edit Google Sheets, or make workbook formulas responsible for parser truth.

## Current Behavior Summary

The implementation is broadly aligned with the contract:

- `GAME_NUMBERS` is fixed to games 1, 2, and 3.
- `MatchSummary` owns match-level facts and nested `GameSummary` objects.
- Invalid game numbers return `None` or no-op through `MatchSummary.game()`.
- Missing result, play/draw, and optional parser facts generally serialize as blanks.
- Exact card-list workbook fields are blank when unresolved placeholder cards are present.
- `MatchSummary.to_match_log_row()` emits the normalized `MatchLogRow` shape.
- `GameSummary.to_game_log_row()` emits the normalized `GameLogRow` shape.
- `MatchSummary.to_history_item()` exposes normalized event identity fields used by runtime surfaces.
- `state.py` uses `MATCH_LOG_SYNC_FIELDS` and `GAME_LOG_SYNC_FIELDS` to detect live/final row changes.
- `tools/google_apps_script/Code.gs` still accepts both normalized `MatchLogRow` and `GameLogRow` payloads.

## Contract Matches

- Fixed game slots: `GAME_NUMBERS = (1, 2, 3)` and `_default_games()` create exactly three game slots.
- Event-type boundary: `models.py` accepts normalized values and does not import raw event classes, webhook outputs, workbook code, or runtime I/O.
- Game-number safety: invalid or missing game numbers do not create new game slots.
- Timestamp tolerance: duration parsing returns blank on invalid timestamps and clamps negative durations to zero.
- Team/result behavior: result and play/draw labels stay blank when required team inputs are missing.
- Card-list behavior: unresolved placeholders are preserved internally for debug use but suppressed from exact workbook fields.
- Event identity: `event_identity()` delegates to `classify_event_identity()`, and `to_history_item()` exposes runtime filter fields.
- Legacy bridge: `to_sheet_row()` still emits `event_family == "MatchSummary"` for the old summary feed path.
- Match landing row: `to_match_log_row(final=True)` emits `Final`; `final=False` emits `Live` and leaves `MTGA End Time` blank.
- Game landing row: `to_game_sheet_rows()` emits only games with summary data.
- Schema coverage: a one-off comparison found no missing `MATCH_LOG_SYNC_FIELDS` keys in `to_match_log_row()` and no missing `GAME_LOG_SYNC_FIELDS` keys in an emitted `GameLogRow`.
- Apps Script field names: `buildMatchLogFieldMap_()` and `buildGameLogFieldMap_()` use the same visible field names as the Python sync-field constants, including the intentional `MGTA Start Time` spelling.

## Contract Mismatches

The Module Fixer follow-up addressed one concrete contract-test finding from Codex E:
`MatchSummary.set_game_mulligans()` raised `OverflowError` for `float("inf")` because the normalization guard did not catch non-finite numeric conversion failures.

The earlier implementation follow-up also addressed one review gap from Codex E:
`MatchSummary.set_game_mulligans()` accepted fractional numeric values because `int(1.5)` silently truncated to `1`.

No workbook schema, webhook payload shape, Apps Script behavior, parser event interpretation, extractor behavior, secrets, environment variables, raw logs, generated card data, runtime status files, live workbook state, or `MGTA Start Time` field name changed.

## Missing Safeguards

These are not proven bugs from the focused comparison, but they are worth protecting before future behavior changes:

- Resolved before this follow-up: `MatchSummary.touch("")` now ignores blank timestamps the way `GameSummary.touch("")` does.
- Resolved in the implementation follow-up: `set_game_mulligans()` now rejects booleans, negative values, invalid strings, arbitrary objects, and non-integral numeric values such as `1.5` before mutating game state.
- Resolved in the Module Fixer follow-up: `set_game_mulligans()` now rejects non-finite numeric values such as `float("inf")` before mutating game state, and integer-like string input `"2"` remains accepted and normalized to integer `2`.
- `played_date()` returns the first 10 characters of an invalid timestamp. This is tolerant, but it can hide malformed upstream timestamps.
- `mtga_queue_type()` can infer provisional queue labels from sideboarding or observed game count. That is useful, but it means live labels may depend on partial match state.
- Later-game starting-player inference only looks at the immediately previous game's winner. Common cases are tested; unusual retirements or missing intermediate game data are not.

## Missing Tests

Resolved in the current worktree:

- Direct `MATCH_LOG_SYNC_FIELDS` coverage for `MatchSummary(...).to_match_log_row()`.
- Direct `GAME_LOG_SYNC_FIELDS` coverage for emitted `GameLogRow` dictionaries.
- Apps Script `buildMatchLogFieldMap_()` and `buildGameLogFieldMap_()` field-name agreement with Python sync-field constants.
- Blank `MatchSummary.touch("")` regression coverage.
- Mulligan input guard coverage, including the fractional numeric follow-up case.
- Mulligan non-finite numeric coverage, including `float("inf")`.
- Mulligan integer-like string coverage for the intended `"2"` normalization behavior.

Still recommended for the next contract-test thread:

- Add queue-type edge cases for provisional live rows.
- Add later-game starting-player inference edge cases with missing game data or unusual match endings.
- Add a history payload stability test that locks the runtime filter keys exposed by `to_history_item()`.

## Stale Or Bridge-Code Areas

- `MatchSummary.to_sheet_row()` remains a legacy `MTGA Match Summary Feed` bridge while Apps Script still accepts `event_family == "MatchSummary"`.
- `GameSummary.to_sheet_row()` exists as a `GameSummary` row serializer, but the inspected focused tests and current normalized update path use `GameLogRow` instead.
- Apps Script field maps still contain fallback logic for legacy keys such as `g1_result`, `g1_mulligans`, `my_rank`, and `total_mulligans`.
- The workbook field typo `MGTA Start Time` is intentionally preserved as part of the current interface.

## Files Changed

- `docs/contracts/parser_models.md`
- `docs/implementation_handoffs/parser_models_comparison.md`
- `src/mythic_edge_parser/app/models.py`
- `tests/test_app_models.py`
- `tests/test_sheet_schema.py`

## Code Changed

Implementation follow-up changed Python code and focused tests:

- `MatchSummary.set_game_mulligans()` now validates normalized mulligan counts before assigning them.
- `MatchSummary.set_game_mulligans()` now treats non-finite numeric values as invalid input without raising from the model path.
- `tests/test_app_models.py` now covers fractional numeric input, non-finite numeric input, and integer-like string input.

## Interface Changes

None.

No function signatures, payload fields, workbook columns, environment variables, Apps Script entrypoints, match identity rules, game identity rules, deduplication behavior, or reconciliation behavior changed.

## Tests Added Or Updated

- `test_set_game_mulligans_ignores_non_integer_values()` now covers `1.5` as an invalid value that must not overwrite a previous valid mulligan count.
- `test_set_game_mulligans_ignores_non_finite_numeric_values()` covers `float("inf")`, `float("-inf")`, and `float("nan")` as invalid values that must not overwrite a previous valid mulligan count.
- `test_set_game_mulligans_accepts_integer_like_string_value()` covers the intended `"2"` normalization behavior.

## Validation Run

```powershell
python3 -m pytest -q tests/test_app_models.py tests/test_sheet_schema.py
python3 -m pytest -q tests/test_app_models.py tests/test_match_summary_from_match_state.py tests/test_runtime_surfaces.py tests/test_sheet_schema.py
python3 -m ruff check src tests
python3 -m pytest -q
```

Result:

```text
21 passed in 0.04s
35 passed in 0.12s
All checks passed!
1 failed, 323 passed in 0.85s
```

Full-suite failure is outside the Module Fixer scope and matches the prior local-environment caveat:
`tests/test_runner.py::test_startup_status_fields_sanitize_paths_and_webhook` expected a Windows-style mocked log path to sanitize to `Player.log`, but the local Python path handling returned the full mocked path.

Additional local comparison checks:

- `to_match_log_row()` contained every field in `MATCH_LOG_SYNC_FIELDS`.
- An emitted `GameLogRow` contained every field in `GAME_LOG_SYNC_FIELDS`.
- Apps Script match/game field maps were inspected for field-name agreement with the Python sync-field constants.

## Still Unverified

- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Parser replay fixture snapshots outside the focused tests were not rerun.

## Reviewer Focus

Ask the next Module Reviewer / contract-test thread to verify the focused `set_game_mulligans()` fix against the Codex E finding and confirm the `"2"` behavior is acceptable under the current parser models contract. The sync-field subset and Python-vs-Apps-Script field-map safeguards already exist and should be checked, not recreated.

## Next Recommended Thread Role

Module Reviewer in contract-test mode.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution. Act as the Module Reviewer thread in contract-test mode for PR #3, docs/implementation_handoffs/parser_models_comparison.md, docs/contract_test_reports/parser_models.md, and docs/contracts/parser_models.md. Verify the Module Fixer changes for set_game_mulligans(): non-finite numeric values such as float("inf") must be rejected without mutating state or raising, and integer-like string "2" must remain accepted and normalized to integer 2. Confirm no workbook schema, webhook payload shape, Apps Script behavior, parser event interpretation, extractor behavior, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/2"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/parser_models.md"
  target_artifact: "docs/implementation_handoffs/parser_models_comparison.md"
  risk_tier: "High"
  branch: "codex/test-parser-models-contract-audit"
  validation:
    - "python3 -m pytest -q tests/test_app_models.py tests/test_sheet_schema.py -> 21 passed in 0.04s"
    - "python3 -m pytest -q tests/test_app_models.py tests/test_match_summary_from_match_state.py tests/test_runtime_surfaces.py tests/test_sheet_schema.py -> 35 passed in 0.12s"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "python3 -m pytest -q -> 1 failed, 323 passed in 0.85s; failure outside Module Fixer scope in tests/test_runner.py path sanitization"
  stop_conditions:
    - "Do not change implementation beyond set_game_mulligans() and focused tests without a new contract or user approval."
    - "Do not change workbook schema, webhook payload shape, Apps Script behavior, match identity, game identity, or final reconciliation behavior."
    - "If integer-like string mulligan behavior is contract-ambiguous, route to Module Contract Writer before changing the contract."
```
