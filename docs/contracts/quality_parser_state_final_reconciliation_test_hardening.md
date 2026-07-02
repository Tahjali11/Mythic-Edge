# Contract: Parser-State Final-Reconciliation Test Hardening

## Module

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/635
- Source threshold-review issue: https://github.com/Tahjali11/Mythic-Edge/issues/632
- Blocked source issue: https://github.com/Tahjali11/Mythic-Edge/issues/625
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566
- Role: Codex B - Module Contract Writer
- Risk tier: Medium-High workflow risk, high protected-surface sensitivity
- Expected implementation handoff: `docs/implementation_handoffs/quality_parser_state_final_reconciliation_test_hardening_comparison.md`
- Expected review report: `docs/contract_test_reports/quality_parser_state_final_reconciliation_test_hardening.md`

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- issue #635, issue #632, issue #625, tracker #566
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/posting_state.py`
- `tests/test_state.py`
- `tests/test_match_summary_from_match_state.py`
- `tests/test_app_models.py`
- `docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json`

`docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_threshold_review.md` was not present on the fresh branch. Per issue #635, this contract treats issue #635, issue #632 comments, and the stopped issue #625 precondition evidence as the durable routing authority. This contract does not lower the threshold.

## Contract Summary

Codex C may add behavior-preserving tests for parser-state final reconciliation so the blocked protected-surface floor work in issue #625 can be retried only after clean evidence proves:

- global Python line coverage is at least `85.00%`;
- `src/mythic_edge_parser/app/models.py` line coverage is at least `90.00%`;
- `src/mythic_edge_parser/app/state.py` line coverage is at least `90.00%`.

The work is test hardening only. The tests must prove existing parser-owned behavior without changing parser output, state reconciliation, match or game identity, deduplication, workbook transport, analytics truth, or coverage policy.

## Observed Current Behavior

The stopped #625 attempt reported:

- global line coverage: `84.73%`, below the active `85.00%` global floor;
- branch coverage: `72.00%`, advisory-only;
- `src/mythic_edge_parser/app/models.py`: `90.13%`, above the candidate-file precondition;
- `src/mythic_edge_parser/app/state.py`: `85.22%`, below the candidate-file precondition;
- no code, tests, tooling, CI, parser behavior, or coverage floors changed.

A prior committed protected-surface advisory report showed `parser_state_final_reconciliation` above `90%` for both candidate files on an older measured commit, but #625's fresh stopped evidence is the controlling retry signal for this contract. Codex C must remeasure from its current base rather than relying on older reports.

## Approved Test-Hardening Scope

Codex C may add focused tests in `tests/test_state.py`, `tests/test_match_summary_from_match_state.py`, and nearby parser regression tests only when the tests assert observable behavior already provided by `state.py`, `models.py`, or `posting_state.py`.

Approved behavior areas:

| Area | Approved assertions |
| --- | --- |
| Live row to final row transition | A live match or game row may be posted first, then a later final row may produce only parser-owned changed sync fields and finality status without changing identity. |
| Match-log changed-field detection | Repeated unchanged live match rows produce no update; changed parser-owned fields produce deterministic changed-field names. |
| Game-log changed-field detection | Repeated unchanged live game rows produce no update; later result-bearing game rows produce final updates. |
| Finality labels | Match finality is derived from `MatchSummary.is_ready()`; game finality is derived from nonblank game result in the emitted game row. |
| Missing summaries or identities | Missing summary, blank match id, or incomplete row identity returns no emitted row/update instead of inventing identity. |
| Invalid game-log keys | Invalid or missing game numbers are skipped safely and cannot create posted-row state entries. |
| Posted-row copy isolation | Marked match and game rows are copied on post so later caller mutation cannot alter stored posted-row state. |
| Runtime-state alias preservation | `ParserRuntimeState` reset and compatibility aliases preserve expected bridge behavior while clearing parser runtime containers. |
| Models row serialization boundaries | `MatchSummary` and `GameSummary` row builders preserve existing blank/default/final row behavior for parser-owned fields. |

Codex C should prefer tests that explain a real final-reconciliation guarantee over tests that exist only to touch lines. Coverage improvement is acceptable only as the byproduct of proving these behaviors.

## Forbidden Behavior Changes

Codex C must not:

- change parser behavior;
- change parser state final reconciliation;
- change parser event classes;
- change match identity, game identity, or deduplication;
- change workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, analytics truth, AI truth, or coaching truth;
- change CI, `pyproject.toml`, active coverage floors, protected-surface coverage floors, or branch coverage policy;
- activate issue #625's protected-surface floor;
- lower the global `85.00%` coverage floor;
- lower the `90.00%` candidate-file precondition for `models.py` or `state.py`;
- use raw Player.log excerpts, private logs, generated coverage artifacts, runtime artifacts, secrets, or local-only files as committed test inputs;
- add tests that assert private implementation details without an observable parser-state behavior reason.

## Coverage Retry Gate

Issue #625 may be retried only after Codex C produces a clean full coverage remeasurement from the same working tree/ref that contains the test-hardening changes.

Required retry evidence:

- full coverage command completes successfully;
- global Python line coverage is `>= 85.00%`;
- `src/mythic_edge_parser/app/models.py` line coverage is `>= 90.00%`;
- `src/mythic_edge_parser/app/state.py` line coverage is `>= 90.00%`;
- branch coverage remains advisory-only and is not used as a pass/fail threshold;
- no raw coverage XML, `.coverage` database, `htmlcov`, terminal transcript, generated runtime file, or local-only artifact is committed.

The retry gate is not satisfied by focused tests alone, partial coverage runs, stale reports, screenshots, or a report generated from a different ref.

## Stop Conditions

Codex C must stop and route back to Codex B or Codex A if:

- the planned tests require changing parser behavior or final reconciliation behavior;
- the only way to pass coverage is to lower thresholds or activate a different policy;
- full coverage does not complete cleanly;
- global line coverage remains below `85.00%`;
- `models.py` or `state.py` remains below `90.00%`;
- branch coverage is proposed as a blocking gate;
- tests need raw Player.log content, private local artifacts, generated SQLite files, runtime logs, workbook exports, secrets, or local-only files;
- test failures reveal a real parser behavior bug that is outside behavior-preserving test hardening;
- issue #625 scope appears stale, closed, superseded, or inconsistent with the fresh coverage evidence.

## Validation Requirements

Codex C must run, at minimum:

```powershell
git status --short --branch
py -m pytest -q tests\test_state.py tests\test_match_summary_from_match_state.py tests\test_app_models.py
.\tools\run_repo_checks.ps1 -Coverage
git diff --check
```

Codex C should also run Ruff over changed Python files and the smallest relevant source/test set. If the repo's current validation selector recommends a broader command for the changed paths, use the selector recommendation and report it.

Protected-surface and secret/private-marker scans must run over the changed file set:

```powershell
git diff --name-only origin/main | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --name-only origin/main | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

Codex C must report:

- exact global line coverage percent;
- exact branch coverage percent with advisory-only label;
- exact `models.py` line coverage percent;
- exact `state.py` line coverage percent;
- whether any generated coverage artifacts were created locally and confirmed uncommitted;
- whether issue #625 is authorized to retry or remains blocked.

## Acceptance Criteria

- Behavior-preserving tests are added only for parser-state/final-reconciliation behavior covered by this contract.
- No parser, model, state, identity, deduplication, workbook, analytics, AI, CI, or coverage policy behavior changes are made.
- Focused parser-state/model tests pass.
- Full coverage passes the active global floor and proves both candidate files meet the `90.00%` retry precondition.
- Validation output is summarized in the implementation handoff without committing raw local artifacts.
- The handoff clearly says whether #625 can retry.

## Next Recommended Role

Codex C: Module Implementer / comparison thread.

Codex C should compare current tests against this contract, add only behavior-preserving tests, remeasure coverage, and produce the implementation handoff. If the retry gate fails, Codex C should stop with evidence instead of attempting the #625 floor implementation.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/635

Source issues:
- Threshold review: https://github.com/Tahjali11/Mythic-Edge/issues/632
- Blocked source issue: https://github.com/Tahjali11/Mythic-Edge/issues/625
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566

Contract:
docs/contracts/quality_parser_state_final_reconciliation_test_hardening.md

Goal:
Add behavior-preserving parser-state final-reconciliation tests so #625 can retry only if a clean full coverage run proves:
- global line coverage >= 85.00%;
- src/mythic_edge_parser/app/models.py >= 90.00%;
- src/mythic_edge_parser/app/state.py >= 90.00%.

Before editing:
- Confirm branch and git status.
- Inspect issue #635, issue #632, issue #625, and tracker #566.
- Read the contract, state.py, models.py, posting_state.py, tests/test_state.py, tests/test_match_summary_from_match_state.py, tests/test_app_models.py, and nearby parser regression tests.
- Identify unrelated dirty files and preserve them.

Do:
- Add only behavior-preserving tests for existing parser-state/final-reconciliation behavior.
- Prefer tests covering live-to-final row transitions, changed-field detection, finality labels, missing identity no-ops, invalid game-log key handling, posted-row copy isolation, runtime alias/reset behavior, and model row serialization boundaries.
- Keep branch coverage advisory-only.
- Produce docs/implementation_handoffs/quality_parser_state_final_reconciliation_test_hardening_comparison.md with exact coverage evidence and whether #625 may retry.

Do not:
- Change parser behavior.
- Change parser state final reconciliation.
- Change parser event classes.
- Change match/game identity or deduplication.
- Change CI, pyproject.toml, coverage thresholds, branch coverage policy, or activate the #625 protected-surface floor.
- Lower the 85.00% global floor or 90.00% candidate-file preconditions.
- Commit raw coverage artifacts, private logs, generated files, secrets, or local-only artifacts.

Validation:
git status --short --branch
py -m pytest -q tests\test_state.py tests\test_match_summary_from_match_state.py tests\test_app_models.py
.\tools\run_repo_checks.ps1 -Coverage
git diff --check
Run Ruff over changed Python files or the selector-recommended validation.
Run changed-file protected-surface and secret/private-marker scans.

Final output must include:
- role performed
- issue/tracker reviewed
- contract used
- implementation handoff path
- tests added and behavior each proves
- coverage evidence: global line, branch advisory, models.py line, state.py line
- whether #625 can retry or remains blocked
- validation results
- protected-surface and secret/private-marker status
- remaining risks
- next recommended role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex B: Module Contract Writer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/635"
  threshold_review_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/632"
  blocked_source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/625"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  completed_thread: "B"
  next_thread: "C"
  contract_artifact: "docs/contracts/quality_parser_state_final_reconciliation_test_hardening.md"
  target_artifact: "docs/implementation_handoffs/quality_parser_state_final_reconciliation_test_hardening_comparison.md"
  risk_tier: "Medium-High workflow risk; high protected-surface sensitivity"
  retry_gate:
    global_line_coverage_percent: ">= 85.00"
    models_py_line_coverage_percent: ">= 90.00"
    state_py_line_coverage_percent: ">= 90.00"
    branch_coverage: "advisory-only"
  decision: "Authorize behavior-preserving test hardening only; do not retry #625 protected-surface floor until clean full coverage evidence meets the retry gate."
  stop_conditions:
    - "Do not change parser behavior or parser state final reconciliation."
    - "Do not change match/game identity, deduplication, CI, pyproject.toml, coverage floors, or branch coverage policy."
    - "Do not activate the #625 protected-surface floor in the test-hardening slice."
    - "Do not commit raw coverage artifacts, private logs, generated files, secrets, or local-only artifacts."
  next_recommended_role: "Codex C: Module Implementer / comparison thread"
```
