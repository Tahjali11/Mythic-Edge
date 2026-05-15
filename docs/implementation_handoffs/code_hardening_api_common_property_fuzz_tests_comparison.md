# Code Hardening API Common Property/Fuzz Tests Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/58

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

## Contract

- `docs/contracts/code_hardening_api_common_property_fuzz_tests.md`
- Supporting behavior contract: `docs/contracts/parser_api_common.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Baseline Status

Branch used:

```text
codex/code-hardening-suite
```

Branch check:

```text
HEAD...origin/codex/code-hardening-suite: 0 ahead / 0 behind
```

At the start of this pass, the prior Codex G sync artifacts were already present
in the working tree:

- `docs/agent_rules.yml`
- `docs/contracts/parser_api_common.md`
- `docs/implementation_handoffs/parser_api_common_comparison.md`
- `docs/contract_test_reports/parser_api_common.md`
- expanded deterministic `tests/test_api_common.py` baseline from `origin/main`

Those files are still working-tree changes relative to branch `HEAD`. This pass
treated them as the local synced baseline and added only issue #58 deterministic
hardening tests on top.

## What The Code Is Supposed To Do

`src/mythic_edge_parser/parsers/api_common.py` owns shared parser helper
behavior for:

- first-decodable JSON discovery in noisy Player.log text
- dict-only JSON body parsing
- exact, case-sensitive API request/response marker matching
- strict list-valued integer normalization

Plain English: these helpers make raw parser input easier for individual parser
modules to consume. They do not emit events, mutate parser state, change
workbook rows, or own downstream match/game interpretation.

## Current Behavior Compared To Contract

The current implementation matches the parser API common contract:

- `find_json_value()` scans `{` and `[` candidates left to right and returns the
  first decodable JSON value.
- `parse_json_from_body()` returns only dict values and returns `None` for an
  earlier decodable array, even if a later dict exists.
- `is_api_request()` and `is_api_response()` compare the first regex-captured
  API name exactly and case-sensitively.
- `normalize_int_list()` returns a new list, rejects bools, accepts non-bool
  ints and stripped digit strings, skips malformed members, and preserves order
  and duplicates.

No runtime contract mismatch was found.

## Implementation Decision

Used deterministic table-driven fuzz-style tests.

Hypothesis was not added because the contracted behavior is a small pure-helper
surface and the first hardening rollout can cover the required invariants with
bounded parameterized examples. No dependency changed.

## What Changed

Added focused parameterized tests in `tests/test_api_common.py` for issue #58:

- `test_find_json_value_property_bounded_malformed_strings_do_not_raise`
- `test_find_json_value_property_valid_json_after_noise_round_trips`
- `test_parse_json_from_body_property_dict_only_return_values`
- `test_api_marker_property_exact_ascii_names_match`
- `test_normalize_int_list_property_returns_only_non_bool_ints`

The new tests cover bounded malformed JSON-like strings, malformed candidates
before valid JSON values, valid arrays as JSON discovery outputs, dict-only
parsing, first non-dict parsing behavior, context neutrality, exact ASCII API
names with whitespace/newline markers, mismatch and case-sensitive marker
behavior, and strict int-list normalization.

## Files Changed

- `tests/test_api_common.py`
- `docs/implementation_handoffs/code_hardening_api_common_property_fuzz_tests_comparison.md`

Pre-existing working-tree sync artifacts were present before this pass and were
not authored by this C-thread implementation:

- `docs/agent_rules.yml`
- `docs/contracts/parser_api_common.md`
- `docs/implementation_handoffs/parser_api_common_comparison.md`
- `docs/contract_test_reports/parser_api_common.md`
- `docs/contracts/code_hardening_api_common_property_fuzz_tests.md`
- `docs/contract_test_reports/code_hardening_api_common_property_fuzz_tests.md`
- `docs/python_tooling_inventory.md`

## Code Changed

Test-only plus this handoff.

No parser runtime code changed.

## Tests Changed

`tests/test_api_common.py` now has deterministic table-driven fuzz-style tests
on top of the synced 17-test parser API common baseline.

Focused count moved from:

```text
17 passed
```

to:

```text
37 passed
```

## Interface Changes

None.

No helper signatures, parser event classes, parser payload shapes, workbook
columns, webhook payloads, Apps Script entrypoints, environment variables,
runtime status files, match/game identity, deduplication behavior, or final
reconciliation behavior changed.

## Contract Matches

- Correct branch target used: `codex/code-hardening-suite`.
- Parser API common sync baseline is present in the working tree.
- The implementation preserves `api_common.py` behavior.
- Property/fuzz coverage is deterministic, bounded, and table-driven.
- No Hypothesis dependency or other dependency was added.
- No parser state, workbook, webhook, Apps Script, event class, match/game
  identity, deduplication, secret, raw-log, generated-data, runtime-status,
  failed-post, or workbook-export surface was touched.
- Consumer parser compatibility checks passed.

## Contract Mismatches

None found in the current implementation.

Workflow note: the baseline sync artifacts are present locally but remain
working-tree changes relative to `HEAD`. A submitter should account for those
separately when staging and publishing.

## Missing Tests Or Open Test Risks

No issue #58 required deterministic helper gap remains known after this pass.

Intentionally not added:

- Hypothesis property tests
- non-ASCII digit behavior tests
- parser behavior changes for rare Unicode digit edge cases
- broad consumer property tests outside `api_common.py`

Unicode digit behavior remains an open risk documented by
`docs/contracts/parser_api_common.md`, not a required behavior change in this
issue.

## Validation Run

Baseline focused check before issue #58 additions:

```powershell
py -m pytest -q tests\test_api_common.py
```

Result:

```text
17 passed in 0.40s
```

Focused check after issue #58 additions:

```powershell
py -m pytest -q tests\test_api_common.py
```

Result:

```text
37 passed in 0.45s
```

Required related consumer slice:

```powershell
py -m pytest -q tests\test_api_common.py tests\test_client_actions_parser.py tests\test_gre_connect_resp_parser.py tests\test_gre_game_state_parser.py
```

Result:

```text
50 passed in 0.48s
```

Additional contract-named parser slice:

```powershell
py -m pytest -q tests\test_parsers.py tests\test_match_state_parser.py
```

Result:

```text
17 passed in 0.50s
```

Additional synced-branch parser slice:

```powershell
py -m pytest -q tests\test_connection_parsers.py tests\test_parser_regressions.py
```

Result:

```text
27 passed in 0.51s
```

Lint:

```powershell
py -m ruff check src tests
```

Result:

```text
All checks passed!
```

Diff whitespace:

```powershell
git diff --check
```

Result:

```text
passed with no output
```

Protected surface gate requested by the issue #58 prompt:

```powershell
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Result:

```text
Protected Surface Gate
base: origin/codex/code-hardening-suite
head: HEAD
changed_paths: 0
forbidden: 0
warnings: 0

result: passed
```

## Still Unverified

- Full `py -m pytest -q` was not run in this C thread.
- Pyright was not run; issue #58 keeps Pyright advisory-only and the current
  user validation did not require zero Pyright findings.
- GitHub Actions were not checked because this implementer thread did not open
  a PR.
- Live workbook state, deployed Apps Script state, raw local logs, generated
  data, runtime status files, failed posts, and workbook exports were not
  inspected.

## Reviewer Focus

Ask Codex E to verify:

- the deterministic table-driven tests satisfy issue #58 without needing
  Hypothesis
- the new tests preserve the parser API common contract rather than redefining
  behavior
- no parser runtime or protected downstream surface changed
- the working-tree sync artifacts are understood before any submitter stages
  files for PR work

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and the mythic-edge-workflow skill.

Act as Codex E: Module Reviewer / contract-test thread for issue #58.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/58

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch:
codex/code-hardening-suite

Source artifacts:
- docs/contracts/code_hardening_api_common_property_fuzz_tests.md
- docs/contracts/parser_api_common.md
- docs/implementation_handoffs/code_hardening_api_common_property_fuzz_tests_comparison.md
- tests/test_api_common.py
- src/mythic_edge_parser/parsers/api_common.py

Goal:
Review the issue #58 implementation against the hardening contract. Verify that the added deterministic table-driven fuzz-style tests cover the required JSON discovery, dict-only parsing, API marker matching, and integer-list normalization invariants without changing parser behavior or adding dependencies.

Review focus:
- findings first, ordered by severity
- contract matches and mismatches
- missing tests
- whether deterministic tests are enough for this first rollout
- whether any protected parser/runtime/workbook/App Script surface changed
- validation evidence and remaining unverified layers

Do not:
- change parser behavior
- add Hypothesis or any dependency
- require zero Pyright findings
- change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports
- target main
- mark tracker #33 complete
- stage, commit, open a PR, or merge unless explicitly asked

Suggested validation:
py -m pytest -q tests\test_api_common.py
py -m pytest -q tests\test_api_common.py tests\test_client_actions_parser.py tests\test_gre_connect_resp_parser.py tests\test_gre_game_state_parser.py
py -m pytest -q tests\test_parsers.py tests\test_match_state_parser.py
py -m pytest -q tests\test_connection_parsers.py tests\test_parser_regressions.py
py -m ruff check src tests
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite

Produce or update:
docs/contract_test_reports/code_hardening_api_common_property_fuzz_tests.md
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/58"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/code_hardening_api_common_property_fuzz_tests.md"
  target_artifact: "docs/contract_test_reports/code_hardening_api_common_property_fuzz_tests.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "py -m pytest -q tests\\test_api_common.py -> 37 passed in 0.45s"
    - "py -m pytest -q tests\\test_api_common.py tests\\test_client_actions_parser.py tests\\test_gre_connect_resp_parser.py tests\\test_gre_game_state_parser.py -> 50 passed in 0.48s"
    - "py -m pytest -q tests\\test_parsers.py tests\\test_match_state_parser.py -> 17 passed in 0.50s"
    - "py -m pytest -q tests\\test_connection_parsers.py tests\\test_parser_regressions.py -> 27 passed in 0.51s"
    - "py -m ruff check src tests -> All checks passed"
    - "git diff --check -> passed with no output"
    - "py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite -> passed"
  stop_conditions:
    - "Do not change parser behavior."
    - "Do not add Hypothesis or dependencies for this pass."
    - "Do not require zero Pyright findings."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not target main."
    - "Do not mark tracker #33 complete."
```
