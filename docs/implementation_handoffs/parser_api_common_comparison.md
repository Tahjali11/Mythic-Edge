# Parser API Common Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/30

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_api_common.md`

## Role Performed

Codex C: Module Implementer.

## Summary

Compared `src/mythic_edge_parser/parsers/api_common.py`,
`src/mythic_edge_parser/parsers/__init__.py`, focused API common tests, and
consumer parser tests against the parser API common contract.

No parser behavior mismatch was found. The implementation matches the contract
for first-decodable JSON discovery, dict-only parser entrypoint behavior,
unused `context` compatibility, exact case-sensitive first API marker matching,
strict integer-list normalization, parser export compatibility, and
side-effect boundaries.

The comparison did find focused test gaps listed by the contract. I added
focused tests only. No runtime/parser implementation code changed.

## Confirmed Matches

- `api_common` remains exported from `mythic_edge_parser.parsers.__all__`.
- `find_json_value()` scans `{` and `[` candidate offsets from left to right.
- Malformed JSON candidates are skipped without propagating
  `json.JSONDecodeError`.
- The first decodable JSON value wins, including arrays.
- Trailing non-JSON text after a decoded JSON value is accepted.
- `find_json_value()` returns `None` when no candidate decodes.
- `parse_json_from_body()` calls `find_json_value()` and returns only dict
  values.
- `parse_json_from_body()` returns `None` for a first decodable non-dict JSON
  value and does not continue searching for a later dict.
- `parse_json_from_body()` accepts `context` but does not let it affect output.
- `is_api_request()` and `is_api_response()` use the documented request and
  response marker regexes.
- API marker matching uses `search()` and only the first regex match.
- API marker matching is exact and case-sensitive against the captured name.
- Whitespace and newlines after the marker are allowed by `\s*`.
- Captured API names are limited to `[A-Za-z0-9_]`.
- Punctuation after an allowed-name prefix produces the documented partial
  capture behavior.
- `normalize_int_list()` returns `[]` for non-list values.
- `normalize_int_list()` returns a new output list.
- Accepted integer-list members preserve input order and duplicates.
- Non-bool integer objects are accepted, including `0` and negative integers.
- Booleans are rejected before integer handling.
- Whitespace-padded digit strings and leading-zero digit strings are accepted.
- Signed strings, decimal strings, floats, objects, nested containers, empty
  strings, and `None` are skipped.
- Shared list normalization remains stricter than parser-specific scalar
  `_maybe_int()` helpers.
- Consumer parser suites continue passing without moving raw-log parsing truth
  downstream.

## Contract Mismatches

None found.

No parser behavior changes were required.

## Missing Safeguards

None found in `api_common.py`.

The contracted safeguards are present:

- ordinary malformed JSON candidates are contained and skipped
- unsupported JSON shapes return `None` from dict-only parsing
- missing or mismatched API markers return `False`
- common malformed integer-list values are skipped
- non-list integer-list inputs degrade to `[]`
- helpers do not mutate input objects or perform parser state, webhook,
  workbook, file, runtime-status, failed-post, log, or generated-data side
  effects

## Missing Or Weak Tests

The contract's suspected focused test gaps were confirmed in the pre-change
tests. They were addressed by focused additions to:

- `tests/test_api_common.py`

Tests added or strengthened:

- malformed JSON candidates before a later valid object
- first-decodable array behavior in `find_json_value()`
- first-decodable array causing `parse_json_from_body()` to return `None`
  even when a later object exists
- all malformed or missing JSON returning `None`
- trailing text after decoded JSON
- `parse_json_from_body()` `context` neutrality
- case-sensitive API marker matching
- whitespace and newline handling after API markers
- first API marker match behavior when multiple markers are present
- punctuation partial-capture behavior
- non-list integer-list values returning `[]`
- order, duplicate preservation, and output-list independence
- strict member filtering for integer-list values, including bool rejection,
  digit-string acceptance, negative integer object acceptance, signed-string
  rejection, float rejection, object rejection, and nested-container rejection

Remaining non-blocking test notes:

- Unicode digit behavior remains an explicit contract open risk. I did not add
  tests that force a behavior change for rare non-ASCII digit strings.
- No consumer parser tests were changed because no consumer behavior changed
  and existing consumer compatibility suites passed.
- Direct non-string calls to JSON or marker helpers remain outside the current
  public contract and were not hardened.

## Files Changed

- `tests/test_api_common.py`
- `docs/implementation_handoffs/parser_api_common_comparison.md`

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
python3 -m pytest -q tests/test_api_common.py
# Pass: 4 passed in 0.12s.

python3 -m pytest -q tests/test_client_actions_parser.py tests/test_gre_connect_resp_parser.py tests/test_gre_game_state_parser.py
# Pass: 68 passed in 0.19s.

python3 -m pytest -q tests/test_connection_parsers.py tests/test_parsers.py tests/test_parser_regressions.py
# Pass: 45 passed in 0.68s.
```

Checks after adding focused tests:

```bash
python3 -m pytest -q tests/test_api_common.py
# Pass: 17 passed in 0.06s.

python3 -m pytest -q tests/test_client_actions_parser.py tests/test_gre_connect_resp_parser.py tests/test_gre_game_state_parser.py
# Pass: 68 passed in 0.28s.

python3 -m pytest -q tests/test_connection_parsers.py tests/test_parsers.py tests/test_parser_regressions.py
# Pass: 45 passed in 0.53s.

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
# Pass: 500 passed in 1.51s.
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
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for issue #30:
https://github.com/Tahjali11/Mythic-Edge/issues/30

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_api_common.md
- docs/implementation_handoffs/parser_api_common_comparison.md
- src/mythic_edge_parser/parsers/api_common.py
- src/mythic_edge_parser/parsers/__init__.py
- tests/test_api_common.py
- src/mythic_edge_parser/parsers/client_actions.py
- tests/test_client_actions_parser.py
- src/mythic_edge_parser/parsers/gre/connect_resp.py
- tests/test_gre_connect_resp_parser.py
- src/mythic_edge_parser/parsers/gre/game_state.py
- tests/test_gre_game_state_parser.py
- src/mythic_edge_parser/parsers/gre/__init__.py
- src/mythic_edge_parser/parsers/match_state.py
- src/mythic_edge_parser/parsers/connection_state.py
- src/mythic_edge_parser/parsers/connection_close.py
- src/mythic_edge_parser/parsers/connection_error.py
- src/mythic_edge_parser/parsers/collection.py
- src/mythic_edge_parser/parsers/inventory.py
- src/mythic_edge_parser/parsers/rank.py
- src/mythic_edge_parser/parsers/session.py
- tests/test_connection_parsers.py
- tests/test_parsers.py
- tests/test_parser_regressions.py

Goal:
Verify the Module Implementer comparison and focused test additions against the parser API common contract.

Confirm:
- api_common remains exported from mythic_edge_parser.parsers.__all__.
- find_json_value() scans { and [ candidates left to right.
- malformed JSON candidates are skipped before later valid JSON.
- first-decodable JSON value wins, including arrays.
- trailing text after decoded JSON remains accepted.
- parse_json_from_body() returns only dict values.
- parse_json_from_body() returns None for first decodable non-dict JSON and does not skip to later dicts.
- parse_json_from_body() context remains behavior-neutral.
- is_api_request() and is_api_response() use exact, case-sensitive first-match marker behavior.
- whitespace/newline marker handling and punctuation partial-capture behavior match the contract.
- normalize_int_list() returns [] for non-lists.
- normalize_int_list() rejects booleans, accepts non-bool ints, accepts stripped digit strings, preserves order and duplicates, returns a new list, and skips signed strings, floats, objects, nested containers, empty strings, and None.
- shared normalize_int_list() remains stricter than parser-specific scalar numeric helpers.
- consumer parser tests still pass without moving raw-log parsing truth downstream.
- no parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match/game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

Validation:
Run:
python3 -m pytest -q tests/test_api_common.py
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_gre_connect_resp_parser.py tests/test_gre_game_state_parser.py
python3 -m pytest -q tests/test_connection_parsers.py tests/test_parsers.py tests/test_parser_regressions.py
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/30"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_api_common.md"
  target_artifact: "docs/implementation_handoffs/parser_api_common_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_api_common.py"
    - "python3 -m pytest -q tests/test_client_actions_parser.py tests/test_gre_connect_resp_parser.py tests/test_gre_game_state_parser.py"
    - "python3 -m pytest -q tests/test_connection_parsers.py tests/test_parsers.py tests/test_parser_regressions.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests"
    - "git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py"
    - "git diff --check"
  stop_conditions:
    - "Route to Module Contract Writer if the contract is ambiguous or inaccurate."
    - "Route to Module Fixer if reviewer finds a concrete parser behavior or focused-test mismatch."
    - "Do not change parser behavior unless required by the contract and covered by focused tests."
    - "Do not broadly align integer normalization semantics across parser modules unless routed through a new explicit contract."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned raw-log parsing truth into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation."
    - "Do not target main unless explicitly approved."
```
