# Code Hardening API Common Property/Fuzz Tests Contract-Test Report

## Findings

No blocking findings.

### Non-Blocking Submitter Scope Note: Do Not Stage Unrelated Untracked Docs

`docs/python_tooling_inventory.md` and `docs/project_roadmap.md` remain
untracked and outside the reviewed issue #58 artifact set. Neither file is
present on `origin/main` or `origin/codex/code-hardening-suite`.

`docs/python_tooling_inventory.md` mentions Hypothesis as a local tooling
candidate while this issue intentionally uses deterministic table-driven tests
with no dependency changes.

Review impact:

- This does not block the issue #58 implementation.
- This is not a parser behavior issue.
- This is not a protected runtime/workbook/App Script surface change.
- Codex F must not stage either unrelated doc for the issue #58 PR unless the
  user separately authorizes it through an issue/contract.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/58

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

## Contract

- `docs/contracts/code_hardening_api_common_property_fuzz_tests.md`
- Supporting parser contract: `docs/contracts/parser_api_common.md`

## Implementation Under Test

Branch: `codex/code-hardening-suite`

Implementation handoffs:

- `docs/implementation_handoffs/code_hardening_api_common_property_fuzz_tests_comparison.md`
- `docs/implementation_handoffs/code_hardening_api_common_property_fuzz_tests_cleanup.md`

Changed files reviewed for issue #58:

- `docs/agent_rules.yml`
- `docs/contracts/parser_api_common.md`
- `docs/implementation_handoffs/parser_api_common_comparison.md`
- `docs/contract_test_reports/parser_api_common.md`
- `docs/contracts/code_hardening_api_common_property_fuzz_tests.md`
- `docs/implementation_handoffs/code_hardening_api_common_property_fuzz_tests_comparison.md`
- `docs/implementation_handoffs/code_hardening_api_common_property_fuzz_tests_cleanup.md`
- `docs/contract_test_reports/code_hardening_api_common_property_fuzz_tests.md`
- `tests/test_api_common.py`

Runtime implementation surface reviewed:

- `src/mythic_edge_parser/parsers/api_common.py`

## Contract Summary

Issue #58 is a test-only Code Hardening rollout for
`src/mythic_edge_parser/parsers/api_common.py`.

The accepted implementation direction is deterministic-first:

- add table-driven fuzz-style tests
- do not add Hypothesis
- do not add dependencies
- do not change parser behavior

The tests harden:

- first-decodable JSON discovery
- dict-only JSON body parsing
- exact, case-sensitive API request/response marker matching
- strict list-valued integer normalization
- parser consumer compatibility through existing parser test suites

The contract does not authorize parser behavior changes, parser state changes,
runtime dependency changes, workbook schema changes, webhook payload changes,
Apps Script behavior changes, parser event class changes, match/game identity
changes, deduplication changes, secrets or environment-variable changes, raw
logs, generated data, runtime status files, failed posts, workbook exports,
targeting `main`, or closing tracker #33.

## Checks Run

```powershell
git fetch --prune origin main codex/code-hardening-suite
git rev-list --left-right --count HEAD...origin/codex/code-hardening-suite
git diff -- pyproject.toml
py -m pytest -q tests\test_api_common.py
py -m pytest -q tests\test_api_common.py tests\test_client_actions_parser.py tests\test_gre_connect_resp_parser.py tests\test_gre_game_state_parser.py
py -m pytest -q tests\test_parsers.py tests\test_match_state_parser.py
py -m pytest -q tests\test_connection_parsers.py tests\test_parser_regressions.py
py -m ruff check src tests tools
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
$paths = @(); $paths += git diff --name-only; $paths += git ls-files --others --exclude-standard; $paths | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
py -m pytest -q
```

## Results

- `git fetch --prune origin main codex/code-hardening-suite` -> fetched target
  refs.
- `git rev-list --left-right --count HEAD...origin/codex/code-hardening-suite`
  -> `0 0`.
- `git diff -- pyproject.toml` -> no output; `pyproject.toml` is clean.
- `py -m pytest -q tests\test_api_common.py` -> `37 passed in 0.51s`.
- `py -m pytest -q tests\test_api_common.py tests\test_client_actions_parser.py tests\test_gre_connect_resp_parser.py tests\test_gre_game_state_parser.py`
  -> `50 passed in 0.56s`.
- `py -m pytest -q tests\test_parsers.py tests\test_match_state_parser.py`
  -> `17 passed in 0.50s`.
- `py -m pytest -q tests\test_connection_parsers.py tests\test_parser_regressions.py`
  -> `27 passed in 0.62s`.
- `py -m ruff check src tests tools` -> `All checks passed!`.
- `git diff --check` -> passed with no output.
- `py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite`
  -> `changed_paths: 0; forbidden: 0; warnings: 0; result: passed`.
- Full working-tree path check including untracked files ->
  `changed_paths: 10; forbidden: 0; warnings: 1; result: passed`.
- The single warning was `workflow_authority_docs docs/agent_rules.yml`, which
  is expected for the synced workflow-authority baseline file.
- `py -m pytest -q` -> `402 passed in 3.83s`.

## Cleanup Confirmation

- `pyproject.toml` is clean.
- No Hypothesis dependency was added.
- No dependency file remains modified.
- `docs/python_tooling_inventory.md` and `docs/project_roadmap.md` remain
  untracked and should not be staged for issue #58 unless separately
  authorized.
- `tests/test_api_common.py` remains the only tracked source/test diff.
- The issue #58 docs and parser API common baseline artifacts remain working
  tree changes for Codex F to stage intentionally.

## Confirmed Contract Matches

- Current branch is `codex/code-hardening-suite`.
- `HEAD` is even with `origin/codex/code-hardening-suite`.
- The parser API common baseline artifacts required by the contract are present
  in the working tree.
- The expanded deterministic parser API common baseline is present in
  `tests/test_api_common.py`.
- The test implementation uses deterministic table-driven fuzz-style tests.
- `src/mythic_edge_parser/parsers/api_common.py` was not changed by issue #58.
- JSON discovery tests cover bounded malformed strings, malformed candidates
  before valid JSON, valid object/array round-trips after noise, array outputs,
  no-candidate fallback, and trailing text acceptance.
- Dict-only parsing tests cover dict return values, first non-dict return
  `None`, no decodable JSON return `None`, and context neutrality.
- API marker tests cover exact ASCII names, whitespace and newline after
  markers, case sensitivity, first-match behavior, mismatch behavior, and
  punctuation partial-capture behavior.
- Integer-list normalization tests cover non-list fallback, bool rejection,
  non-bool int acceptance including negative integer objects, ASCII digit
  string acceptance after stripping, signed-string and float rejection, object
  and nested-container skipping, order and duplicate preservation, and new list
  output behavior.
- Consumer compatibility slices passed.
- Full pytest and Ruff passed.
- No parser runtime behavior changed.
- No parser state final reconciliation, workbook schema, webhook payload shape,
  Apps Script behavior, parser event class, match/game identity, deduplication,
  secret, environment variable, raw log, generated data, runtime status, failed
  post, or workbook export surface was changed.
- Pyright remains advisory; zero Pyright findings were not required.

## Contract Mismatches

None found after cleanup.

## Missing Tests

No blocking missing test coverage in `tests/test_api_common.py`.

Intentionally not added in this rollout:

- Hypothesis property tests.
- Non-ASCII digit behavior tests.
- Direct non-string JSON or marker helper tests.
- Broad property tests in consumer parser modules.

These omissions match the contract and deterministic-first implementation
decision. Unicode digit behavior remains an explicit open risk from
`docs/contracts/parser_api_common.md`, not a required issue #58 behavior change.

## Drift Notes

- Repo drift from the earlier stale hardening branch was addressed by the local
  targeted baseline sync artifacts.
- The previous dependency/tooling drift in `pyproject.toml` has been cleaned
  up.
- `docs/python_tooling_inventory.md` and `docs/project_roadmap.md` remain
  untracked and outside issue #58 scope.
- No parser behavior drift found.
- No parser truth ownership drift found.
- No workbook drift inspected or found.
- No deployed Apps Script drift inspected or found.
- No live workbook state inspected.
- No local-data drift found in the reviewed issue #58 test artifacts.

## Recommendation

Approve for Codex F: Module Submitter.

No Codex D fixer pass is recommended after this cleanup confirmation.

Codex F should stage only the reviewed issue #58 package and must not stage
`docs/python_tooling_inventory.md` or `docs/project_roadmap.md` unless
separately authorized.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and the mythic-edge-workflow skill.

Act as Codex F: Module Submitter for issue #58.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/58

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch:
codex/code-hardening-suite

Reviewed artifacts:
- docs/agent_rules.yml
- docs/contracts/parser_api_common.md
- docs/implementation_handoffs/parser_api_common_comparison.md
- docs/contract_test_reports/parser_api_common.md
- docs/contracts/code_hardening_api_common_property_fuzz_tests.md
- docs/implementation_handoffs/code_hardening_api_common_property_fuzz_tests_comparison.md
- docs/implementation_handoffs/code_hardening_api_common_property_fuzz_tests_cleanup.md
- docs/contract_test_reports/code_hardening_api_common_property_fuzz_tests.md
- tests/test_api_common.py

Reviewer verdict:
No blocking findings after cleanup. Issue #58 deterministic table-driven fuzz-style tests are ready for submitter work.

Submitter scope warning:
Do not stage docs/python_tooling_inventory.md or docs/project_roadmap.md for this PR unless the user separately authorizes them through an issue/contract. They are untracked and outside the reviewed issue #58 artifact set.

Submitter tasks:
1. Verify current branch and working-tree status.
2. Confirm pyproject.toml is clean and no dependency changes are staged.
3. Stage only the reviewed issue #58 files.
4. Commit with a concise issue-linked message.
5. Push the branch.
6. Open or update a draft PR targeting codex/code-hardening-suite, not main.
7. Do not merge, close tracker #33, or target main.

Validation already checked by Codex E:
- py -m pytest -q tests\test_api_common.py -> 37 passed
- py -m pytest -q tests\test_api_common.py tests\test_client_actions_parser.py tests\test_gre_connect_resp_parser.py tests\test_gre_game_state_parser.py -> 50 passed
- py -m pytest -q tests\test_parsers.py tests\test_match_state_parser.py -> 17 passed
- py -m pytest -q tests\test_connection_parsers.py tests\test_parser_regressions.py -> 27 passed
- py -m pytest -q -> 402 passed
- py -m ruff check src tests tools -> All checks passed
- git diff --check -> passed
- py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite -> passed
- full working-tree protected-surface path check -> passed with expected docs/agent_rules.yml warning

Do not change parser behavior, add Hypothesis, add dependencies, require zero Pyright findings, change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/58"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contract_test_reports/code_hardening_api_common_property_fuzz_tests.md"
  target_artifact: "draft PR targeting codex/code-hardening-suite"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git fetch --prune origin main codex/code-hardening-suite -> fetched target refs"
    - "git rev-list --left-right --count HEAD...origin/codex/code-hardening-suite -> 0 0"
    - "git diff -- pyproject.toml -> no output"
    - "py -m pytest -q tests\\test_api_common.py -> 37 passed in 0.51s"
    - "py -m pytest -q tests\\test_api_common.py tests\\test_client_actions_parser.py tests\\test_gre_connect_resp_parser.py tests\\test_gre_game_state_parser.py -> 50 passed in 0.56s"
    - "py -m pytest -q tests\\test_parsers.py tests\\test_match_state_parser.py -> 17 passed in 0.50s"
    - "py -m pytest -q tests\\test_connection_parsers.py tests\\test_parser_regressions.py -> 27 passed in 0.62s"
    - "py -m ruff check src tests tools -> All checks passed"
    - "git diff --check -> passed with no output"
    - "py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite -> passed"
    - "working-tree protected-surface path check including untracked files -> passed with expected workflow_authority_docs warning for docs/agent_rules.yml"
    - "py -m pytest -q -> 402 passed in 3.83s"
  stop_conditions:
    - "Do not stage docs/python_tooling_inventory.md or docs/project_roadmap.md for issue #58 unless separately authorized."
    - "Do not reintroduce pyproject.toml dependency changes."
    - "Do not add Hypothesis or dependencies for this pass."
    - "Do not change parser behavior."
    - "Do not require zero Pyright findings."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not target main."
    - "Do not mark tracker #33 complete."
```
