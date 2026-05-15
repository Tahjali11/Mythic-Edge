# GRE Turn Info Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/28

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_gre_turn_info.md`

## Implementation Under Test

Branch: `codex/parser-module-audit-suite`

Changed files reviewed:

- `docs/contracts/parser_gre_turn_info.md`
- `docs/implementation_handoffs/parser_gre_turn_info_comparison.md`
- `tests/test_gre_turn_info_parser.py`

Implementation source files inspected:

- `src/mythic_edge_parser/parsers/gre/turn_info.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- downstream consumer/test files named in the contract-test prompt

## Contract Summary

`turn_info.py` must keep parser-owned GRE turn-info normalization inside the
parser layer. `build_turn_info(gsm)` returns `{}` for missing, non-dict, or
empty `turnInfo`, and returns exactly eight snake_case fields for non-empty
`turnInfo` dictionaries. The helper must preserve active-player precedence,
current local Python `int()` conversion behavior, `str(value or "")` string
conversion behavior, no raw turn-info preservation, no input mutation, and
game-state consumed-output compatibility.

## Findings

No blocking findings.

## Checks Run

```bash
python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_parsers.py
# Pass: 38 passed in 0.07s.

python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_transforms.py
# Pass: 54 passed in 0.17s.

python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_gameplay_actions.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
# Pass: 37 passed in 0.29s.

python3 -m pytest -q
# Pass: 487 passed in 2.27s.

python3 -m ruff check src tests
# Pass: All checks passed!

git diff --check
# Pass: no whitespace errors.

git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
# Pass: no protected runtime source diffs.

gh issue view 28 --repo Tahjali11/Mythic-Edge --json number,title,state,url,labels
# Pass: issue #28 is open.

gh issue view 5 --repo Tahjali11/Mythic-Edge --json number,title,state,url
# Pass: tracker #5 is open.
```

## Results

Contract-test verdict: pass.

The Module Implementer patch satisfies the revised GRE Turn Info parser
contract. The patch is test/documentation-only for this module and does not
change parser runtime behavior.

## Confirmed Contract Matches

- `build_turn_info()` returns `{}` for missing, non-dict, and empty-dict
  `turnInfo`.
- Non-empty `turnInfo` dictionaries return the eight contracted snake_case
  fields only.
- Unknown raw `turnInfo` keys are ignored.
- `activePlayer` takes precedence over `activePlayerSeatId`.
- `activePlayer` fallback occurs only for `None` and `""`.
- Present but unconvertible `activePlayer` values do not fall back after
  conversion failure.
- Local `_maybe_int()` preserves current Python `int()` behavior for bools,
  floats, signed strings, and whitespace-padded integer strings.
- Fractional strings and invalid integer-like values become `None`.
- Local `_string_field()` preserves `str(value or "")` behavior for missing,
  falsey, and truthy non-string values.
- `build_turn_info()` does not mutate `gsm` or raw `turnInfo`.
- Raw `turnInfo` preservation remains out of `turn_info.py` and owned by
  `game_state.py` raw-game-state preservation.
- `game_state.py` carries `turn_info` exactly as returned and mirrors only
  contracted fields into identity/top-level shortcuts.
- Downstream state, extractor, transform, runtime, gameplay-action, candidate,
  and regression tests continue consuming parser-produced turn context.
- Protected runtime source diff check is empty.

## Contract Mismatches

None found.

## Missing Tests

None blocking.

The added tests in `tests/test_gre_turn_info_parser.py` cover the contract's
previously suspected weak areas: empty `turnInfo`, active-player precedence,
conversion failure without fallback, permissive integer conversion, string
conversion, input non-mutation, and game-state consumed-output compatibility.

## Drift Notes

- Repo drift: none found in reviewed scope.
- Workbook drift: not checked live; no workbook schema or workbook export files
  changed.
- Deployment drift: not checked live; no Apps Script or deployment behavior
  changed.
- Local-data drift: none found; no raw logs, generated data, runtime status
  files, failed posts, secrets, or workbook exports are included.
- Issue/tracker drift: issue #28 and tracker #5 are open at review time.
- PR lifecycle drift: no PR exists for this module yet.

## Recommendation

Approve.

Next recommended role: Codex F: Module Submitter.

## Remaining Non-Blocking Gaps

- GitHub Actions have not run because there is no module PR yet.
- Live workbook and deployed Apps Script behavior were not checked because they
  are outside this parser contract and protected surfaces were not changed.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for issue #28:
https://github.com/Tahjali11/Mythic-Edge/issues/28

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/5

Branch:
codex/parser-module-audit-suite

Use:
- docs/contracts/parser_gre_turn_info.md
- docs/implementation_handoffs/parser_gre_turn_info_comparison.md
- docs/contract_test_reports/parser_gre_turn_info.md
- tests/test_gre_turn_info_parser.py
- docs/codex_module_workflow.md
- docs/agent_threads/module_submitter.md

Goal:
Submit the reviewed GRE Turn Info parser audit package as a module PR targeting codex/parser-module-audit-suite, not main.

Reviewed files expected in scope:
- docs/contracts/parser_gre_turn_info.md
- docs/implementation_handoffs/parser_gre_turn_info_comparison.md
- docs/contract_test_reports/parser_gre_turn_info.md
- tests/test_gre_turn_info_parser.py

Before staging:
- Confirm the current branch is codex/parser-module-audit-suite.
- Confirm there are no protected runtime source diffs.
- Confirm no secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, workbook schema changes, webhook payload shape changes, Apps Script changes, parser state final reconciliation changes, parser event class changes, extractor behavior changes, match/game identity changes, or deduplication changes are included.

Validation to preserve in the PR body:
- python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_parsers.py
- python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_transforms.py
- python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_gameplay_actions.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py
- python3 -m pytest -q
- python3 -m ruff check src tests
- git diff --check

Do:
- Stage only the reviewed files for issue #28.
- Commit with a concise message referencing issue #28.
- Push to the approved branch.
- Open or update a draft PR targeting codex/parser-module-audit-suite.
- Use Refs #28 and Refs #5 unless the PR fully closes issue #28 under the repo workflow.
- Route merge, issue closure, and tracker completion to Codex G after review/CI gates are satisfied.

Do not:
- Stage unrelated files.
- Target main.
- Merge the PR.
- Close issue #28 or tracker #5.
- Change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.

Output:
- Submitted files.
- Commit hash.
- PR URL.
- Validation evidence included in the PR body.
- Any excluded local changes.
- Next recommended role: Codex G only after submitter/CI/review gates are ready for deployment.
- A workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/28"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/implementation_handoffs/parser_gre_turn_info_comparison.md"
  target_artifact: "docs/contract_test_reports/parser_gre_turn_info.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  verdict: "pass"
  validation:
    - "python3 -m pytest -q tests/test_gre_turn_info_parser.py tests/test_gre_game_state_parser.py tests/test_parsers.py"
    - "python3 -m pytest -q tests/test_state.py tests/test_app_extractors.py tests/test_transforms.py"
    - "python3 -m pytest -q tests/test_runtime_surfaces.py tests/test_gameplay_actions.py tests/test_grp_id_candidates.py tests/test_parser_regressions.py"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests"
    - "git diff --check"
    - "git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py"
  stop_conditions:
    - "Do not target main."
    - "Do not stage unrelated files."
    - "Do not merge, close issue #28, or update tracker #5 as completed from submitter role."
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, parser event classes, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
```
