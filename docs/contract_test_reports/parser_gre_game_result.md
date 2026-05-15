# GRE Game Result Parser Contract-Test Report

## Findings

No blocking findings.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/24

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_gre_game_result.md`

## Implementation Under Test

Branch: `codex/parser-module-audit-suite`

Implementation handoff:
`docs/implementation_handoffs/parser_gre_game_result_comparison.md`

Changed implementation surface reviewed:

- `tests/test_gre_game_result_parser.py`
- `tests/test_parsers.py`
- `docs/contracts/parser_gre_game_result.md`
- `docs/implementation_handoffs/parser_gre_game_result_comparison.md`

## Contract Summary

`src/mythic_edge_parser/parsers/gre/game_result.py` must detect game-over GRE
game-state payloads and build stable parser-owned `GameResultEvent.payload`
dictionaries. Game-over detection must use `game_info.stage` first, allow
top-level `stage` fallback, and avoid inferring game over from match state or
result lists. Top-level winner/result/reason fields must come only from the
latest known game-scope result, while match-scope result entries remain
preserved in `results` for state final reconciliation.

## Checks Run

```bash
python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_app_extractors.py
python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py
python3 -m pytest -q
python3 -m ruff check src tests
git diff --check
```

## Results

- `python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_parsers.py`
  -> `38 passed in 0.04s`.
- `python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_app_extractors.py`
  -> `54 passed in 0.11s`.
- `python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py`
  -> `17 passed in 0.12s`.
- `python3 -m pytest -q` -> `470 passed in 0.92s`.
- `python3 -m ruff check src tests` -> `All checks passed!`.
- `git diff --check` -> passed with no output.

## Confirmed Contract Matches

- `is_game_over()` uses `game_info.stage` first, falls back to top-level
  `stage` when needed, and does not infer game over from `match_state`,
  result lists, winners, result types, or reasons.
- `build_game_result_payload()` returns the contracted payload fields:
  `type`, `source`, `stage`, `match_state`, `winning_team_id`, `result_type`,
  `reason`, `results`, `game_info`, `identity`, `game_state_id`, and
  `message_type`.
- Output `game_info`, `identity`, and `results` are shallow output views as
  contracted; nested values may alias input objects.
- Missing or malformed optional sections degrade to neutral/default values.
- Non-list `game_info.results` yields `results == []`, and non-dict result
  entries are preserved in output `results` while being skipped for selection.
- Top-level `winning_team_id`, `result_type`, and `reason` come only from the
  latest known game-scope result.
- Match-scope results remain preserved in `results` and are not promoted into
  top-level game-winner fields.
- `None`, `""`, `0`, `0.0`, `"0"`, `" 0 "`, and booleans remain unknown
  winner values.
- A later unknown game-scope winner does not erase an earlier known game-scope
  winner.
- Exact `"Game"` / `"Match"` aliases and MTGA `MatchScope_*` labels behave
  according to the contract.
- Snake-case `winning_team_id` and `result_type` result-entry keys are not used
  for parser top-level game-winner/result selection.
- GRE dispatch emits `GameStateEvent` then `GameResultEvent` for game-over
  payloads, including queued game-state game-over payloads.
- Paired events preserve expected event classes, performance classes,
  timestamp, raw body bytes, and shared metadata.
- Focused tests cover the contract-required game-over detection, result
  selection, malformed/default, copy, scope, unknown-winner, and dispatch
  behavior.
- Downstream state, extractor, transform, runtime, and regression tests still
  consume parser-produced `GameResult` payloads without raw GRE
  reinterpretation.
- No parser state final reconciliation, workbook schema, webhook payload shape,
  Apps Script behavior, parser event classes, extractor behavior,
  match/game identity, deduplication, final reconciliation, secrets,
  environment variables, raw logs, generated data, runtime status files, failed
  posts, or workbook exports changed.

## Contract Mismatches

None.

## Missing Tests

None blocking.

The focused additions cover the contract's prior suspected gaps for game-over
non-inference, output shape/defaults, shallow-copy limits, non-list results,
missing selected-result metadata, detection-only top-level stage fallback,
unknown winner values, later-unknown game-scope behavior, scope aliases,
unknown scopes, non-dict result preservation, snake-case key non-selection,
paired event metadata, and queued game-over dispatch.

## Drift Notes

- No parser behavior drift found.
- No downstream ownership drift found; raw GRE game-result interpretation
  remains in the parser layer.
- No parser-state final reconciliation drift found in the reviewed surface.
- No workbook/webhook/App Script/runtime artifact drift found in the reviewed
  surface.

## Recommendation

Approve for submitter work.

Next recommended role: Codex F: Module Submitter.

## Remaining Non-Blocking Gaps

- GitHub Actions were not checked because no PR exists yet.
- Live workbook and deployed Apps Script behavior were not checked; no workbook
  schema or Apps Script changes are in scope.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for issue #24 and the GRE GameResult parser contract audit.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/24

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_gre_game_result.md
- docs/implementation_handoffs/parser_gre_game_result_comparison.md
- docs/contract_test_reports/parser_gre_game_result.md
- tests/test_gre_game_result_parser.py
- tests/test_parsers.py

Reviewer verdict:
No blocking findings. The GRE GameResult parser contract audit is ready for submitter work.

Submitter requirements:
- Verify current branch and changed-file scope.
- Stage only the reviewed GRE GameResult parser audit artifacts.
- Commit and push the branch.
- Open or update a draft PR targeting codex/parser-module-audit-suite, not main.
- Do not merge, close issue #24, or mark tracker #5 complete; those are Codex G responsibilities.

Validation to run or verify:
python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_parsers.py
python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_app_extractors.py
python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py
python3 -m pytest -q
python3 -m ruff check src tests
git diff --check

Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not merge or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/24"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_gre_game_result.md"
  target_artifact: "docs/contract_test_reports/parser_gre_game_result.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_parsers.py -> 38 passed in 0.04s"
    - "python3 -m pytest -q tests/test_state.py tests/test_match_summary_from_match_state.py tests/test_app_extractors.py -> 54 passed in 0.11s"
    - "python3 -m pytest -q tests/test_transforms.py tests/test_runtime_surfaces.py tests/test_parser_regressions.py -> 17 passed in 0.12s"
    - "python3 -m pytest -q -> 470 passed in 0.92s"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "git diff --check -> passed with no output"
  stop_conditions:
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not promote match-scope results into top-level game-winner fields."
    - "Do not treat None, \"\", 0, or \"0\" as known winners."
    - "Do not merge, close issue #24, or mark tracker #5 complete; route deployer work to Codex G."
    - "Do not target main unless explicitly approved."
```
