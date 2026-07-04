# Code Hardening PR Drift Budget Contract-Test Report

## Findings

No blocking findings.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/39

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/33

## Contract

`docs/contracts/code_hardening_pr_drift_budget.md`

## Implementation Under Test

Branch/worktree: `codex/code-hardening-suite`

Worktree path:
`/Users/<redacted>/Documents/New project/Mythic-Edge-code-hardening-suite`

Implementation handoff:
`docs/implementation_handoffs/code_hardening_pr_drift_budget_comparison.md`

Reviewed implementation surfaces:

- `.github/pull_request_template.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/implementation_handoffs/code_hardening_pr_drift_budget_comparison.md`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `tools/check_protected_surfaces.py`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`

Changed-file scope observed for this module:

- `.github/pull_request_template.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/implementation_handoffs/code_hardening_pr_drift_budget_comparison.md`
- `docs/contract_test_reports/code_hardening_pr_drift_budget.md`

## Contract Summary

The PR drift budget is a repository workflow/template change. It adds a short
semantic drift disclosure section to `.github/pull_request_template.md` so
authors must state behavior, event-shape, workbook/webhook/App Script,
truth-ownership, fixture/evidence, protected-surface, residual-drift, and
follow-up impact. The section exposes drift for reviewers; it does not
authorize protected changes by itself.

## Checks Run

```bash
git diff --check
python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
printf ".github/pull_request_template.md\n" | python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
rg -n "## Drift Budget" .github/pull_request_template.md
rg -n "Runtime/parser behavior|Parser event shape/classes|Workbook/webhook/App Script shape|Parser truth ownership|Fixtures/evidence|Protected-surface authorization|Residual drift / accepted gaps|Follow-up required" .github/pull_request_template.md
git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py data workbook_exports exports
git ls-files --others --exclude-standard -- src tools main.py live_print_filtered_v11_match_summary.py data workbook_exports exports docs .github tests
```

## Results

- `git diff --check` -> passed with no output.
- `python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite`
  -> `changed_paths: 0`, `forbidden: 0`, `warnings: 0`, `result: passed`.
- Direct PR-template protected-surface seam:
  `printf ".github/pull_request_template.md\n" | python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin`
  -> `changed_paths: 1`, `forbidden: 0`, `warnings: 1`,
  `WARNING workflow_authority_docs .github/pull_request_template.md`, `result: passed`.
- `rg -n "## Drift Budget" .github/pull_request_template.md`
  -> `26:## Drift Budget`.
- Required-field `rg` check found all eight fields at lines 30-37.
- `git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py data workbook_exports exports`
  -> passed with no output.
- Untracked-file listing confirms unrelated live-diagnostics artifacts remain in
  the worktree and must not be absorbed into this module.

Repo-level pytest/Ruff was not run because the contract does not require it for
a PR-template-only edit and no code, tests, CI, or tooling are part of this
module's intended implementation diff.

## Contract-Test Verdict

Pass.

The Module Implementer patch satisfies the PR drift-budget contract. The
template section is present, placed correctly, contains the required labels and
fields, preserves existing PR template gates, and does not imply
template-only authorization for protected schema/truth changes.

## Confirmed Contract Matches

- `.github/pull_request_template.md` contains `## Drift Budget`.
- The section is placed after `## Layer Ownership`.
- The section is placed before `## Changes`.
- The section names all four allowed response labels:
  `No drift`, `Authorized drift`, `Residual drift`, and `N/A`.
- The section states that `Authorized drift` or `Residual drift` requires an
  issue and contract citation.
- The section includes all eight required fields:
  - `Runtime/parser behavior`
  - `Parser event shape/classes`
  - `Workbook/webhook/App Script shape`
  - `Parser truth ownership`
  - `Fixtures/evidence`
  - `Protected-surface authorization`
  - `Residual drift / accepted gaps`
  - `Follow-up required`
- Existing PR template sections remain present:
  - `## Summary`
  - `## Linked Issue And Contract`
  - `## Risk Tier`
  - `## Layer Ownership`
  - `## Changes`
  - `## Tests`
  - `## Contract Verification`
  - `## Still Unverified`
  - `## Workflow Handoff`
- Existing risk-tier, contract-verification, and workflow-handoff gates remain.
- The wording exposes semantic drift but does not authorize protected changes
  by itself.
- The direct protected-surface warning for `.github/pull_request_template.md`
  is expected and authorized by issue #39 and
  `docs/contracts/code_hardening_pr_drift_budget.md`.
- No parser behavior, workbook schema, webhook payload shape, Apps Script
  behavior, parser event classes, parser state final reconciliation,
  match/game identity, deduplication, secrets, raw logs, generated data,
  runtime status files, failed posts, or workbook exports changed for this
  module.

## Contract Mismatches

None.

## Missing Tests

None blocking.

The contract requires command-based validation rather than focused tests for
this PR-template-only edit. The required `rg`, `git diff --check`, and
protected-surface checks passed.

## Drift Notes

- No parser/runtime behavior drift found.
- No parser event shape/class drift found.
- No workbook/webhook/App Script shape drift found.
- No parser truth ownership drift found.
- No fixture/evidence drift found in this module.
- Authorized workflow-authority drift: `.github/pull_request_template.md`
  changed under issue #39 and
  `docs/contracts/code_hardening_pr_drift_budget.md`.
- `docs/agent_rules.yml` remains absent on this hardening branch, as recorded
  by the contract.
- The protected-surface gate's normal branch-diff run reports `changed_paths: 0`
  because it compares committed refs and does not scan uncommitted/untracked
  files. The direct `--paths-from-stdin` seam verified the expected PR-template
  warning.

## Unrelated Worktree Files

The following untracked files are present but outside this issue #39 review
scope:

```text
docs/contract_test_reports/code_hardening_live_diagnostics_mode.md
docs/contracts/code_hardening_live_diagnostics_mode.md
docs/implementation_handoffs/code_hardening_live_diagnostics_mode_comparison.md
src/mythic_edge_parser/app/live_diagnostics.py
tests/test_live_diagnostics.py
```

Codex F should stage only the issue #39 drift-budget files, or otherwise split
module submissions so unrelated live-diagnostics artifacts are not absorbed.

## Remaining Non-Blocking Gaps

- GitHub Actions/Windows CI was not run.
- The drift budget has not yet been filled in a real PR body.
- Tracker #33 remains open and must not be marked complete by Codex E or Codex
  F.
- Submitter must keep this module isolated from unrelated live-diagnostics
  artifacts in the mixed worktree.

## Recommendation

Approve for submitter work.

Next recommended role: Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for issue #39 and the Code Hardening PR drift budget section.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/39

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch:
codex/code-hardening-suite

Use:
- docs/contracts/code_hardening_pr_drift_budget.md
- docs/implementation_handoffs/code_hardening_pr_drift_budget_comparison.md
- docs/contract_test_reports/code_hardening_pr_drift_budget.md
- .github/pull_request_template.md
- docs/contracts/code_hardening_protected_surface_gate.md
- tools/check_protected_surfaces.py

Goal:
Submit the PR drift-budget template package for review, without targeting main.

Confirm:
- Codex E found no blocking findings.
- `.github/pull_request_template.md` contains `## Drift Budget`.
- The section is placed after `## Layer Ownership` and before `## Changes`.
- The section includes all eight required fields and the four allowed response labels.
- Existing PR template sections and gates remain present.
- The wording exposes semantic drift but does not authorize protected changes by itself.
- The protected-surface warning on `.github/pull_request_template.md` is expected and authorized by issue #39 and the contract.
- No parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports are included.
- Unrelated live-diagnostics files are not staged or absorbed into this drift-budget module.

Validation:
Run or cite fresh validation:
git diff --check
python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
printf ".github/pull_request_template.md\n" | python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
rg -n "## Drift Budget" .github/pull_request_template.md
rg -n "Runtime/parser behavior|Parser event shape/classes|Workbook/webhook/App Script shape|Parser truth ownership|Fixtures/evidence|Protected-surface authorization|Residual drift / accepted gaps|Follow-up required" .github/pull_request_template.md

Output:
- Submitter verdict.
- Intended staged files.
- PR/branch status.
- Validation evidence.
- Protected-surface confirmation.
- Next recommended role: Codex G only after PR checks pass and review is ready.
- A workflow_handoff block.

Do not merge, close issue #39, mark tracker #33 complete, target main, weaken protected-surface review, or change parser/runtime/workbook/App Script behavior.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/39"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/code_hardening_pr_drift_budget.md"
  target_artifact: "PR for Code Hardening PR drift budget section"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check -> passed with no output"
    - "python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite -> result: passed, changed_paths: 0"
    - "printf \".github/pull_request_template.md\\n\" | python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin -> result: passed, warning: workflow_authority_docs .github/pull_request_template.md"
    - "rg -n \"## Drift Budget\" .github/pull_request_template.md -> 26:## Drift Budget"
    - "required-field rg check -> all eight required fields present at lines 30-37"
    - "git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py data workbook_exports exports -> no output"
  stop_conditions:
    - "Do not weaken protected-surface review or imply template-only authorization for schema/truth changes."
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not absorb unrelated untracked live-diagnostics files into this module."
    - "Do not target main; hardening PR work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
