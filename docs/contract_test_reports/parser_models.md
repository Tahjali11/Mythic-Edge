# Parser Models Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/2

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

## Contract

`docs/contracts/parser_models.md`

Required role and workflow references:

- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`
- `docs/codex_module_workflow.md`

## Implementation Under Test

Pull request: https://github.com/Tahjali11/Mythic-Edge/pull/3

Branch under test: `codex/test-parser-models-contract-audit`

Head commit reviewed after local rebase: `17c43eb03436de5b22e861f6d83a97e9245060d5`

Base branch: `codex/parser-module-audit-suite`

Module Fixer follow-up status: blocking `set_game_mulligans()` non-finite numeric finding has been fixed locally and routed back to Module Reviewer / contract-test mode.

Changed files in the PR diff:

- `docs/contracts/parser_models.md`
- `docs/implementation_handoffs/parser_models_comparison.md`
- `src/mythic_edge_parser/app/models.py`
- `tests/test_app_models.py`
- `tests/test_sheet_schema.py`

## Contract Summary

`src/mythic_edge_parser/app/models.py` must remain the parser-owned row-shaping layer for normalized match and game facts. It must preserve stable `MatchLogRow` and `GameLogRow` workbook/webhook-facing field names, keep the `MGTA Start Time` workbook typo stable, distinguish provisional live rows from final reconciled rows, serialize unknown or malformed parser facts defensively, and avoid moving parser truth into Apps Script or workbook formulas.

## Checks Run

```powershell
gh pr view 3 --json number,title,body,headRefName,baseRefName,headRefOid,baseRefOid,state,author,url,files,commits,reviews,mergeStateStatus
gh issue view 2 --json number,title,body,state,author,url,labels
git diff --name-status origin/codex/parser-module-audit-suite...HEAD
git rev-list --left-right --count origin/codex/parser-module-audit-suite...HEAD
git merge-base --is-ancestor origin/codex/parser-module-audit-suite HEAD
python3 -m pytest -q tests/test_app_models.py tests/test_match_summary_from_match_state.py tests/test_runtime_surfaces.py tests/test_sheet_schema.py
python -m pytest -q tests/test_app_models.py tests/test_match_summary_from_match_state.py tests/test_runtime_surfaces.py tests/test_sheet_schema.py
PYTHONPATH=src python3 - <<'PY'
from mythic_edge_parser.app.models import MatchSummary
s = MatchSummary(match_id='probe')
s.set_game_mulligans(1, 2)
print('initial', repr(s.games[1].mulligans))
try:
    s.set_game_mulligans(1, float('inf'))
except Exception as exc:
    print('inf_exception', type(exc).__name__, str(exc))
else:
    print('inf_exception', 'none')
print('after_inf', repr(s.games[1].mulligans))
s.set_game_mulligans(1, '2')
print('after_string_2', repr(s.games[1].mulligans))
PY
python3 -m pytest -q
python3 -m ruff check src tests
ruff check src tests
rm -rf /tmp/mythic-edge-pr3-venv
python3 -m venv /tmp/mythic-edge-pr3-venv
/tmp/mythic-edge-pr3-venv/bin/python -m pip install -q -e '.[dev]'
/tmp/mythic-edge-pr3-venv/bin/python -m ruff check src tests
/tmp/mythic-edge-pr3-venv/bin/python -m pytest -q
```

## Results

Module Fixer follow-up completed.

Focused contract checks passed:

```text
35 passed in 0.13s
```

Ruff passed through the PATH-installed `ruff` command:

```text
All checks passed!
```

Full pytest in the isolated temp virtualenv found one failure outside the PR diff:

```text
1 failed, 321 passed in 3.84s
```

The failing test was `tests/test_runner.py::test_startup_status_fields_sanitize_paths_and_webhook`, where a Windows-style `LOG_PATH` was not reduced to `Player.log` in the local macOS/POSIX temp environment. PR #3 did not touch `tests/test_runner.py` or `src/mythic_edge_parser/app/runner.py`, so this is recorded as local environment or pre-existing repo drift rather than a parser-models contract failure.

Before `ruff` was added to PATH, bare system Python could not run full validation because project/dev dependencies were missing:

- `python3 -m pytest -q` failed collection on missing `bs4`.
- `python3 -m ruff check src tests` failed because `ruff` was not installed.

After adding required local dependencies, the focused contract suite and Ruff passed with those commands. Full-suite validation still exposes the known unrelated `tests/test_runner.py::test_startup_status_fields_sanitize_paths_and_webhook` local path-sanitization failure outside the parser-models diff.

## Confirmed Contract Matches

- `MatchSummary.touch("")` now ignores blank timestamps after a valid timestamp instead of erasing `last_event_time`. Covered by `tests/test_app_models.py`.
- `to_match_log_row()` contains every Python `MATCH_LOG_SYNC_FIELDS` field.
- Emitted `GameLogRow` dictionaries contain every Python `GAME_LOG_SYNC_FIELDS` field.
- Apps Script `buildMatchLogFieldMap_()` and `buildGameLogFieldMap_()` visible field names match Python sync-field constants.
- The workbook-facing typo `MGTA Start Time` is preserved in Python and Apps Script.
- `to_match_log_row(final=False)` still emits `MTGA Sync Status == "Live"`, leaves `MTGA End Time` blank, and keeps unobserved sideboard, submit-deck, and zero-mulligan values provisional.
- `to_match_log_row(final=True)` still emits final row fields through the existing `Final` path.
- Exact card-list workbook fields still hide unresolved placeholder card lists while preserving debug/internal lists.
- `MatchSummary.set_game_mulligans()` now rejects non-finite numeric values such as `float("inf")`, `float("-inf")`, and `float("nan")` without mutating state or raising.
- Integer-like string input `"2"` remains accepted and normalized to integer `2`.
- No workbook schema, webhook payload shape, Apps Script behavior, parser event interpretation, extractor behavior, secrets, environment variables, raw logs, generated card data, runtime status files, failed posts, or workbook exports were changed in the PR diff.

## Contract Mismatches

Resolved by Module Fixer follow-up:

- `src/mythic_edge_parser/app/models.py:275` - `MatchSummary.set_game_mulligans()` previously raised for `float("inf")` instead of treating it as invalid input. The guard now catches `OverflowError` along with `TypeError` and `ValueError`.

Post-fix probe output:

```text
after_inf 2
after_string_2 2 int
```

No remaining blocking parser-models contract mismatch is recorded in this report after the Module Fixer pass.

## Missing Tests

- Resolved: focused coverage now asserts `float("inf")`, `float("-inf")`, and `float("nan")` are rejected safely without overwriting a previous valid mulligan count.
- Resolved: focused coverage now locks the intended integer-like string `"2"` behavior as accepted and normalized to integer `2`.
- Keep the already-noted follow-up gaps for future coverage unless they are split out: queue-type edge cases for provisional live rows, later-game starting-player inference with missing game data or unusual match endings, and runtime history payload key stability for `to_history_item()`.

## Drift Notes

- Repo/workflow drift resolved locally: PR #3 was rebased onto `origin/codex/parser-module-audit-suite` after the initial review. `git rev-list --left-right --count origin/codex/parser-module-audit-suite...HEAD` now returns `0 1`, and `git merge-base --is-ancestor origin/codex/parser-module-audit-suite HEAD` exits `0`.
- Handoff drift: `docs/implementation_handoffs/parser_models_comparison.md` has stale reviewer-focus wording. It asks the next contract-test thread to turn missing sync-field and Apps Script field-map checks into executable safeguards, but those checks now exist in `tests/test_app_models.py` and `tests/test_sheet_schema.py`. Its `Files Changed` section also omits `docs/contracts/parser_models.md` and `tests/test_sheet_schema.py`, both of which are in PR #3.
- Workbook drift: live workbook state was not inspected.
- Deployment drift: deployed Apps Script state was not inspected.
- Local environment drift: bare system Python initially lacked `ruff` and still lacks at least `bs4`; isolated temp-venv validation exposed one unrelated full-suite failure in untouched runner path-sanitization code.

## Recommendation

Route back to Module Reviewer / contract-test mode.

The parser row-shape and provisional/final behavior remain broadly aligned with the contract. The non-finite mulligan input path is fixed and the `"2"` behavior is locked by focused tests. Reviewer should verify the fixer diff and confirm no forbidden surfaces changed.

## Next Workflow Action

Next role: Module Reviewer / contract-test mode.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as the Module Reviewer thread in contract-test mode for PR #3, Issue #2, tracker issue #5, docs/contracts/parser_models.md, docs/implementation_handoffs/parser_models_comparison.md, and docs/contract_test_reports/parser_models.md. Verify the Module Fixer changes for set_game_mulligans(): non-finite numeric values such as float("inf"), float("-inf"), and float("nan") must be rejected without mutating state or raising, and integer-like string "2" must remain accepted and normalized to integer 2. Confirm no workbook schema, webhook payload shape, Apps Script behavior, parser event interpretation, extractor behavior, match identity, game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.
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
