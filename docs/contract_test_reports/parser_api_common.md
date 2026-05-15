# Parser API Common Contract-Test Report

## Findings

No blocking findings.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/30

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_api_common.md`

## Implementation Under Test

Branch: `codex/parser-module-audit-suite`

Implementation handoff:
`docs/implementation_handoffs/parser_api_common_comparison.md`

Reviewed source surfaces:

- `src/mythic_edge_parser/parsers/api_common.py`
- `src/mythic_edge_parser/parsers/__init__.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/parsers/gre/connect_resp.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/__init__.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/parsers/connection_state.py`
- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/parsers/connection_error.py`
- `src/mythic_edge_parser/parsers/collection.py`
- `src/mythic_edge_parser/parsers/inventory.py`
- `src/mythic_edge_parser/parsers/rank.py`
- `src/mythic_edge_parser/parsers/session.py`

Changed-file scope reviewed:

- `tests/test_api_common.py`
- `docs/contracts/parser_api_common.md`
- `docs/implementation_handoffs/parser_api_common_comparison.md`
- `docs/contract_test_reports/parser_api_common.md`

Runtime implementation code was not changed.

## Contract Summary

`src/mythic_edge_parser/parsers/api_common.py` owns shared parser helper
behavior for raw Player.log JSON discovery, dict-only parser body parsing,
API request/response marker matching, and strict integer-list normalization.
Individual parser modules still own event-specific payload semantics, and
state, extractors, workbook, webhook, Apps Script, dashboard, and AI layers
must not redefine this raw-log parsing truth.

The contract intentionally preserves the difference between
`api_common.normalize_int_list()` and parser-specific scalar `_maybe_int()`
helpers. Broad integer-normalization alignment remains out of scope without a
new contract.

## Checks Run

```bash
python3 -m pytest -q tests/test_api_common.py
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_gre_connect_resp_parser.py tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_connection_parsers.py tests/test_parsers.py tests/test_parser_regressions.py
python3 -m pytest -q
python3 -m ruff check src tests
git diff --check
git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
```

## Results

- `python3 -m pytest -q tests/test_api_common.py`
  -> `17 passed in 0.17s`.
- `python3 -m pytest -q tests/test_client_actions_parser.py tests/test_gre_connect_resp_parser.py tests/test_gre_game_state_parser.py`
  -> `68 passed in 0.35s`.
- `python3 -m pytest -q tests/test_connection_parsers.py tests/test_parsers.py tests/test_parser_regressions.py`
  -> `45 passed in 1.05s`.
- `python3 -m pytest -q` -> `500 passed in 1.42s`.
- `python3 -m ruff check src tests` -> `All checks passed!`.
- `git diff --check` -> passed with no output.
- `git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py`
  -> passed with no output.

## Contract-Test Verdict

Pass.

The Module Implementer comparison and focused test additions match the parser
API common contract. The prior suspected focused-test gaps are covered, and no
behavior mismatch was found.

## Confirmed Contract Matches

- `api_common` remains exported from `mythic_edge_parser.parsers.__all__`.
- `find_json_value()` scans `{` and `[` candidate offsets left to right.
- Malformed JSON candidates are skipped before later valid JSON.
- The first decodable JSON value wins, including arrays.
- Trailing text after decoded JSON remains accepted.
- `parse_json_from_body()` returns only dict values.
- `parse_json_from_body()` returns `None` for a first decodable non-dict JSON
  value and does not skip to later dicts.
- `parse_json_from_body()` `context` remains behavior-neutral.
- `is_api_request()` and `is_api_response()` use exact, case-sensitive
  first-match marker behavior.
- Whitespace/newline marker handling and punctuation partial-capture behavior
  match the contract.
- `normalize_int_list()` returns `[]` for non-lists.
- `normalize_int_list()` rejects booleans, accepts non-bool ints, accepts
  stripped digit strings, preserves order and duplicates, returns a new list,
  and skips signed strings, floats, objects, nested containers, empty strings,
  and `None`.
- Shared `normalize_int_list()` remains stricter than parser-specific scalar
  numeric helpers.
- Consumer parser tests still pass without moving raw-log parsing truth
  downstream.
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

- malformed JSON candidates before a later valid object
- first-decodable array behavior in `find_json_value()`
- first-decodable array causing `parse_json_from_body()` to return `None`
  even when a later object exists
- all malformed or missing JSON returning `None`
- trailing text after decoded JSON
- `parse_json_from_body()` context neutrality
- case-sensitive API marker matching
- whitespace and newline handling after API markers
- first API marker behavior when multiple markers are present
- punctuation partial-capture behavior
- non-list integer-list inputs returning `[]`
- order and duplicate preservation
- output-list independence
- strict integer-list member filtering for bools, signed strings, floats,
  objects, nested containers, empty strings, and `None`
- negative integer object acceptance alongside signed-string rejection

Consumer parser compatibility is covered by the focused client-action,
GRE connect-response, GRE game-state, connection, parser smoke, and regression
suites.

## Drift Notes

- No parser behavior drift found.
- No parser truth drift found; shared raw-log helper behavior remains in the
  parser layer.
- No downstream ownership drift found; consumers continue using shared helper
  outputs rather than reimplementing raw-log parsing truth.
- No integer-normalization drift found; `normalize_int_list()` remains distinct
  from parser-specific scalar `_maybe_int()` helpers.
- No parser state final reconciliation drift found in the reviewed surface.
- No workbook/webhook/App Script/runtime artifact drift found in the reviewed
  surface.
- No protected runtime-source files changed.

## Remaining Non-Blocking Gaps

- Unicode digit behavior remains an explicit contract open risk. The contract
  does not require a behavior change or focused test that would force one.
- Direct non-string calls to JSON or marker helpers remain outside the current
  public contract.
- GitHub Actions were not checked because no PR exists for this module yet.
- Live workbook behavior was not checked; workbook schema and exports are out
  of scope.
- Deployed Apps Script behavior was not checked; Apps Script behavior is out
  of scope.

## Recommendation

Approve for submitter work.

Next recommended role: Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for issue #30 and the parser API common contract audit.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/30

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_api_common.md
- docs/implementation_handoffs/parser_api_common_comparison.md
- docs/contract_test_reports/parser_api_common.md
- tests/test_api_common.py

Reviewer verdict:
No blocking findings. The parser API common contract audit is ready for submitter work.

Submitter requirements:
- Verify current branch and changed-file scope.
- Stage only the reviewed parser API common audit artifacts.
- Commit and push the branch.
- Open or update a draft PR targeting codex/parser-module-audit-suite, not main.
- Do not merge, close issue #30, or mark tracker #5 complete; those are Codex G responsibilities.

Validation to run or verify:
python3 -m pytest -q tests/test_api_common.py
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_gre_connect_resp_parser.py tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_connection_parsers.py tests/test_parsers.py tests/test_parser_regressions.py
python3 -m pytest -q
python3 -m ruff check src tests
git diff --check

Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not merge, close issue #30, mark tracker #5 complete, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/30"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_api_common.md"
  target_artifact: "docs/contract_test_reports/parser_api_common.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_api_common.py -> 17 passed in 0.17s"
    - "python3 -m pytest -q tests/test_client_actions_parser.py tests/test_gre_connect_resp_parser.py tests/test_gre_game_state_parser.py -> 68 passed in 0.35s"
    - "python3 -m pytest -q tests/test_connection_parsers.py tests/test_parsers.py tests/test_parser_regressions.py -> 45 passed in 1.05s"
    - "python3 -m pytest -q -> 500 passed in 1.42s"
    - "python3 -m ruff check src tests -> All checks passed!"
    - "git diff --check -> passed with no output"
    - "git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py -> passed with no output"
  stop_conditions:
    - "Do not change parser behavior unless required by the contract and covered by focused tests."
    - "Do not broadly align integer normalization semantics across parser modules unless routed through a new explicit contract."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned raw-log parsing truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not merge, close issue #30, or mark tracker #5 complete; route deployer work to Codex G."
    - "Do not target main unless explicitly approved."
```
