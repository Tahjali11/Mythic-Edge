# Contract Test Report: Code Hardening Pyright Findings Cleanup

## Findings First

No blocking findings remain.

The two prior Codex E findings are fixed:

1. `saved_event_replay.py` malformed nested-payload behavior is restored to
   pass-through/fail-fast semantics. `event_from_saved_record()` now keeps the
   typed event-kind mapping and string-kind guard, but passes
   `payload.get("payload", {})` through to the event constructor without
   converting present non-dict values to `{}` (`src/mythic_edge_parser/app/saved_event_replay.py:63`).
   The new regression test verifies present malformed nested payloads fail fast
   (`tests/test_saved_event_replay.py:313`).
2. `grp_id_candidates.py` no longer suppresses present nonblank malformed
   `runner_up_gap` values. The loader now computes a typed local
   `runner_up_gap` with direct `int(...)` conversion for present nonblank input
   (`src/mythic_edge_parser/app/grp_id_candidates.py:287`). The new regression
   test verifies malformed present values still raise
   (`tests/test_grp_id_candidates.py:400`).

## Issue And Tracker

- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/45
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33
- Branch: `codex/code-hardening-suite`
- Branch freshness: `HEAD...origin/codex/code-hardening-suite` returned `0 0`

## Role Performed

Codex E: Module Reviewer / contract-test confirmation.

## Contracts And Artifacts Reviewed

- `docs/contracts/code_hardening_pyright_advisory.md`
- `docs/implementation_handoffs/code_hardening_pyright_advisory_comparison.md`
- `docs/contract_test_reports/code_hardening_pyright_advisory.md`
- `docs/contract_test_reports/code_hardening_pyright_findings_cleanup.md`
- `docs/implementation_handoffs/code_hardening_pyright_findings_cleanup.md`
- `docs/contracts/parser_saved_event_replay.md`
- `docs/contract_test_reports/parser_saved_event_replay.md`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `tests/test_saved_event_replay.py`
- `src/mythic_edge_parser/app/grp_id_candidates.py`
- `tests/test_grp_id_candidates.py`
- broader Pyright cleanup source/test diff
- `tools/run_pyright_advisory.ps1`

## Contract Matches

- Pyright remains advisory-only. It was not added as a required or failing CI
  gate.
- Zero Pyright findings are not required by the repo workflow, though this
  cleanup currently achieves zero findings through the advisory wrapper.
- The local Pyright command uses the Python `pyright` package path and the
  Windows `py` launcher through `tools/run_pyright_advisory.ps1`.
- No npm, npx, `package.json`, or package lockfile was introduced.
- Existing default local repo checks and CI-required behavior remain tests,
  Ruff, and the protected-surface gate.
- The previous saved-event replay behavior change was corrected and covered by
  a focused regression test.
- The previous `runner_up_gap` behavior change was corrected and covered by a
  focused regression test.
- No workbook schema, webhook payload shape, Apps Script behavior, parser event
  classes, match/game identity, deduplication, final reconciliation, secrets,
  environment variables, raw logs, generated data, runtime status files, failed
  posts, or workbook exports were changed in the reviewed fixes.

## Contract Mismatches

None found in the current loopback state.

## Missing Tests

No blocking missing tests found.

The two behavior-preservation gaps from the previous review now have focused
coverage:

- present malformed nested saved-event payloads fail fast
- present nonblank malformed `runner_up_gap` values fail fast

## Protected-Surface And Scope Confirmation

Path-scoped protected-surface validation against
`origin/codex/code-hardening-suite` passed with `forbidden: 0` and three
warnings:

- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/runner.py`

Those warnings are expected for the broader Pyright cleanup scope and did not
correspond to a reviewed behavioral change. The prior concrete behavior drift
in `saved_event_replay.py` and `grp_id_candidates.py` has been corrected.

The broad check against `origin/main` also passed with `forbidden: 0` and five
warnings for existing hardening-suite workflow/governance surfaces.

## Validation Run

```powershell
git fetch --prune origin main codex/code-hardening-suite
git rev-list --left-right --count HEAD...origin/codex/code-hardening-suite
tools\run_pyright_advisory.ps1
py -m pytest -q tests\test_saved_event_replay.py tests\test_grp_id_candidates.py
py -m pytest -q tests\test_saved_event_replay.py tests\test_grp_id_candidates.py tests\test_runtime_surfaces.py tests\test_runner.py
py -m pytest -q
py -m ruff check src tests tools
git diff --check
$paths = @(); $paths += git diff --name-only; $paths += git ls-files --others --exclude-standard; $paths | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
py tools\check_protected_surfaces.py --base origin/main
```

Results:

- `git fetch --prune origin main codex/code-hardening-suite` completed.
- `git rev-list --left-right --count HEAD...origin/codex/code-hardening-suite`
  returned `0 0`.
- `tools\run_pyright_advisory.ps1` passed with `0 errors, 0 warnings, 0 informations`.
- Focused replay/candidate pytest passed: `37 passed in 1.62s`.
- Focused review slice passed: `62 passed in 2.82s`.
- Full pytest passed: `670 passed in 4.78s`.
- `py -m ruff check src tests tools` passed.
- `git diff --check` passed with non-failing CRLF warnings for several test
  files.
- Path-scoped protected-surface check against
  `origin/codex/code-hardening-suite` passed with `changed_paths: 29`,
  `forbidden: 0`, `warnings: 3`.
- Broad protected-surface check against `origin/main` passed with
  `changed_paths: 55`, `forbidden: 0`, `warnings: 5`.

## Files Changed By This Review

- `docs/contract_test_reports/code_hardening_pyright_findings_cleanup.md`

No implementation code was edited by this review.

## Remaining Risks

- GitHub Actions has not run for this exact unstaged working-tree state.
- The working tree remains unstaged and includes the broader Pyright cleanup
  scope, not just the two loopback fixes.
- Bare `pyright --project pyrightconfig.json` can still hit local interpreter
  resolution noise in this shell; `tools\run_pyright_advisory.ps1` is the
  verified local command.

## Recommendation

Approve for Codex F: Module Submitter.

Submitter should stage only the reviewed Pyright cleanup package and avoid
pulling unrelated local files into the PR.

## Pasteable Next-Thread Prompt

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex F: Module Submitter for the Pyright findings cleanup on codex/code-hardening-suite.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/45

Reviewed artifacts:
- docs/implementation_handoffs/code_hardening_pyright_findings_cleanup.md
- docs/contract_test_reports/code_hardening_pyright_findings_cleanup.md

Goal:
Submit the reviewed Pyright cleanup package as a draft PR targeting codex/code-hardening-suite. Stage only the reviewed files in the current Pyright cleanup scope. Do not target main and do not merge.

Before staging:
- inspect git status
- confirm the staged file list matches the reviewed cleanup package
- confirm no raw logs, generated data, runtime status files, failed posts, workbook exports, secrets, environment variables, or unrelated local files are staged

Validation to preserve or rerun:
- tools\run_pyright_advisory.ps1
- py -m pytest -q tests\test_saved_event_replay.py tests\test_grp_id_candidates.py
- py -m pytest -q tests\test_saved_event_replay.py tests\test_grp_id_candidates.py tests\test_runtime_surfaces.py tests\test_runner.py
- py -m pytest -q
- py -m ruff check src tests tools
- git diff --check
- path-scoped protected-surface check against origin/codex/code-hardening-suite

Do not make Pyright a required CI gate. Do not require zero Pyright findings as a repo policy. Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, final reconciliation, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports. Do not mark tracker #33 complete.

Final handoff must include branch, commit hash, PR URL, target branch, staged files, validation result, remaining risk, and next recommended role.
```

## Workflow Handoff

```yaml
workflow_handoff:
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/45"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  branch: "codex/code-hardening-suite"
  source_artifact: "docs/implementation_handoffs/code_hardening_pyright_findings_cleanup.md"
  target_artifact: "docs/contract_test_reports/code_hardening_pyright_findings_cleanup.md"
  code_changed: false
  tests_changed: false
  review_verdict: "approved_for_submitter"
  validation:
    - "git rev-list --left-right --count HEAD...origin/codex/code-hardening-suite -> 0 0"
    - "tools\\run_pyright_advisory.ps1 -> 0 errors, 0 warnings, 0 informations"
    - "py -m pytest -q tests\\test_saved_event_replay.py tests\\test_grp_id_candidates.py -> 37 passed"
    - "py -m pytest -q tests\\test_saved_event_replay.py tests\\test_grp_id_candidates.py tests\\test_runtime_surfaces.py tests\\test_runner.py -> 62 passed"
    - "py -m pytest -q -> 670 passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed with non-failing CRLF warnings"
    - "path-scoped protected-surface check against origin/codex/code-hardening-suite -> passed with 3 warnings"
    - "protected-surface check against origin/main -> passed with 5 warnings"
  remaining_risk:
    - "GitHub Actions not run for this exact working-tree state."
    - "Working tree remains unstaged and includes the broader Pyright cleanup scope."
  stop_conditions:
    - "Do not make Pyright a required CI gate unless a future contract authorizes it."
    - "Do not stage unrelated files outside the reviewed Pyright cleanup package."
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, identity, deduplication, or final reconciliation."
    - "Do not target main, merge, or mark tracker #33 complete."
```
