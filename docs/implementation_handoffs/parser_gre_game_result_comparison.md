# GRE GameResult Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/24

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_gre_game_result.md`

## Role Performed

Codex C: Module Implementer.

## Summary

Compared `src/mythic_edge_parser/parsers/gre/game_result.py`,
`src/mythic_edge_parser/parsers/gre/__init__.py`, downstream consumer
expectations, and focused tests against the GRE GameResult parser contract.

No parser behavior mismatch was found. The implementation matches the contract
for game-over detection, output payload shape, shallow copy/default behavior,
known-winner semantics, latest known game-scope winner precedence,
match-scope preservation, paired GRE dispatch, and side-effect boundaries.

The comparison did find missing focused tests required by the contract. I added
focused tests only. No runtime/parser implementation code changed.

## Confirmed Matches

- `is_game_over()` uses `game_info.stage` first, falls back to top-level
  `stage` only when `game_info.stage` is falsey, and returns true only for
  exact `"GameStage_GameOver"`.
- `is_game_over()` does not infer game over from `match_state`, result lists,
  winners, or result reasons.
- `build_game_result_payload()` emits stable `type == "game_result"` and
  `source == "gre_game_state"`.
- Output `stage` and `match_state` are copied only from `game_info.stage` and
  `game_info.matchState`.
- `game_state_id` and `message_type` pass through as-is with contracted
  defaults.
- `game_info`, `identity`, and top-level `results` output views are shallow
  copies.
- Non-list `game_info.results` yields `results == []`.
- Non-dict result entries are preserved in output `results` and skipped during
  game-scope winner selection.
- Scope labels containing `MatchScope_Game` and exact `"Game"` normalize to
  game scope for parser top-level winner selection.
- Scope labels containing `MatchScope_Match` and exact `"Match"` remain match
  scope and are not promoted into top-level game-winner fields.
- Unknown scopes are ignored for parser top-level game-winner selection.
- `None`, `""`, numeric zero, string zero, and booleans remain unknown winners.
- Top-level `winning_team_id`, `result_type`, and `reason` come from the
  latest known game-scope result only.
- A later game-scope result with an unknown winner does not erase an earlier
  known game-scope result.
- Snake-case `winning_team_id` / `result_type` keys in result entries are not
  parser-selected as top-level game winner/result fields.
- Match-scope result entries remain preserved in `results` for state final
  reconciliation.
- GRE dispatch emits `GameStateEvent` before `GameResultEvent` for game-over
  game-state payloads.
- Queued game-state game-over messages also emit paired
  `GameStateEvent` / `GameResultEvent` events.
- Paired events share the same metadata object built from the raw body and
  timestamp.
- `GameResultEvent` remains the emitted event family and keeps
  `POST_GAME_BATCH` performance class.
- Downstream state/extractor/transform/runtime tests continue consuming
  parser-produced GameResult payload fields without moving truth downstream.

## Contract Mismatches

None found.

No parser behavior changes were required.

## Missing Safeguards

None found in `game_result.py` or GRE dispatch.

The contracted safeguards are present:

- malformed optional sections degrade to neutral defaults
- non-dict result entries are safe and preserved
- unknown winners are skipped for game-scope selection
- match-scope results are never promoted into top-level game-winner fields
- dispatch never emits a `GameResultEvent` without a paired preceding
  `GameStateEvent` for the same game-over game-state payload
- helpers are side-effect free

## Missing Or Weak Tests

The contract's suspected test gaps were confirmed in the pre-change tests. They
were addressed by focused additions to:

- `tests/test_gre_game_result_parser.py`
- `tests/test_parsers.py`

Tests added or strengthened:

- no game-over inference from `match_state` or result lists alone
- happy-path output payload fields, defaults, and pass-through fields
- shallow-copy limits for nested `game_info`, `identity`, and result entries
- non-list `game_info.results` yielding empty output `results`
- missing selected game result `result` and `reason` defaults
- top-level `stage` fallback being detection-only, not output `stage`
- unknown winner values: `None`, `""`, `0`, `0.0`, `"0"`, `" 0 "`,
  `False`, and `True`
- earlier known game-scope winner surviving a later unknown game-scope winner
- exact `"Game"` scope alias and exact `"Match"` non-promotion
- unknown-scope ignoring and non-dict result preservation
- snake-case result winner/result keys ignored for parser top-level selection
- dispatch metadata, event class, performance class, raw bytes, and event order
- queued game-state game-over paired event emission

Remaining non-blocking test notes:

- No new state/extractor/transform/runtime tests were added because no
  downstream behavior changed and existing downstream contract suites passed.
- Deep-copy isolation for nested result entries remains intentionally outside
  the current contract.
- Future stricter scope matching or snake-case parser support would require a
  new problem representation and contract.

## Files Changed

- `tests/test_gre_game_result_parser.py`
- `tests/test_parsers.py`
- `docs/implementation_handoffs/parser_gre_game_result_comparison.md`

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
python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_parsers.py
# Pass: 20 passed in 0.05s.

python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_app_extractors.py
# Pass: 54 passed in 0.12s.

python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py
# Pass: 17 passed in 0.14s.
```

Checks after adding focused tests:

```bash
python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_parsers.py
# Pass: 38 passed in 0.09s.

python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_app_extractors.py
# Pass: 54 passed in 0.16s.

python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py
# Pass: 17 passed in 0.16s.

python3 -m ruff check src tests
# Pass: All checks passed!
```

Final documentation/worktree validation:

```bash
git diff --check
# Pass: no whitespace errors.

git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
# Pass: no runtime implementation files changed.

python3 -m pytest -q
# Pass: 470 passed in 0.94s.
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
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #24:
https://github.com/Tahjali11/Mythic-Edge/issues/24

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_gre_game_result.md
- docs/implementation_handoffs/parser_gre_game_result_comparison.md
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

Goal:
Verify the Module Implementer comparison and focused test additions against the GRE GameResult parser contract.

Confirm:
- is_game_over() uses game_info.stage first, allows top-level stage fallback, and does not infer game-over from match_state or result lists.
- build_game_result_payload() returns the contracted payload fields, defaults, shallow copy behavior, result list preservation, and pass-through fields.
- top-level winning_team_id, result_type, and reason come only from the latest known game-scope result.
- match-scope results remain preserved in results and are not promoted into top-level game-winner fields.
- None, "", 0, "0", booleans, and equivalent zero values remain unknown winners.
- later unknown game-scope winners do not erase earlier known game-scope winners.
- exact Game/Match scope aliases and MTGA MatchScope_* labels behave according to the contract.
- GRE dispatch emits GameStateEvent then GameResultEvent for game-over payloads, including queued game-state game-over payloads.
- paired events preserve expected event classes, performance classes, timestamp, raw body bytes, and metadata sharing.
- focused tests cover the contract-required game-over detection, result selection, malformed/default, copy, scope, unknown-winner, and dispatch behavior.
- downstream state, extractor, transform, runtime, and regression tests still consume parser-produced GameResult payloads without raw GRE reinterpretation.
- no parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match/game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

Validation:
Run:
python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_app_extractors.py
python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/24"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_gre_game_result.md"
  target_artifact: "docs/implementation_handoffs/parser_gre_game_result_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_parsers.py"
    - "python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_app_extractors.py"
    - "python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests"
    - "git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py"
    - "git diff --check"
  stop_conditions:
    - "Route to Module Contract Writer if the contract is ambiguous or inaccurate."
    - "Route to Module Fixer if reviewer finds a concrete parser behavior or focused-test mismatch."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not promote match-scope results into top-level game-winner fields."
    - "Do not treat None, \"\", 0, or \"0\" as known winners."
    - "Do not target main unless explicitly approved."
```
