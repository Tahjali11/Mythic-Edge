# Quality Ruff Second Bug-Risk Tranche Contract Test

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/608>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/567>

## Project Roadmap

<https://github.com/Tahjali11/Mythic-Edge/issues/568>

## Active Separate Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/605>

Issue #605 was closed before this confirmation review. It remains outside the
#608 Ruff tranche scope.

## Contract

`docs/contracts/quality_ruff_second_bug_risk_tranche.md`

## Implementation Under Test

- Branch: `codex/ruff-second-bug-tranche-567`
- Base ref: `origin/main`
- Reviewed head: `503239c593dc935e7864bf15df94dae70760ff7f`
- Current `origin/main`: `503239c593dc935e7864bf15df94dae70760ff7f`
- Branch sync during confirmation review: `0 0`
- Implementation handoff:
  `docs/implementation_handoffs/quality_ruff_second_bug_risk_tranche_comparison.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

Issue #608 authorizes promotion of exactly these Ruff bug-prevention codes:
`B006`, `B008`, `B012`, `B023`, and `B904`.

The implementation must preserve existing selected Ruff rules, keep lint scope
at `src tests tools`, exclude broad `B`, exclude `B909`, avoid preview mode,
avoid autofix/unsafe-fix, avoid all-rules advisory remeasurement, avoid issue
#605 coverage-policy work, and avoid parser/runtime/product behavior changes.

## Internal Project Area Reviewed

Quality / validation gates. Ruff configuration owns static-analysis rule
selection only. It does not own parser truth, analytics truth, security
assurance, privacy assurance, release readiness, deploy readiness, production
readiness, AI truth, or coaching truth.

## Checks Run

```powershell
git status --short --branch --untracked-files=all
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
gh issue view 608 --repo Tahjali11/Mythic-Edge --json number,title,state,url
gh issue view 567 --repo Tahjali11/Mythic-Edge --json number,title,state,url
py -m ruff check src tests tools --select B006,B008,B012,B023,B904
py -m ruff check src tests tools
py -m pytest -q tests\test_run_repo_checks_script.py
py -c "<tomllib selected-rule verification>"
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

## Results

- Issue #608 was open at confirmation review time.
- Tracker #567 was open at confirmation review time.
- Branch was refreshed onto current `origin/main`: `0 0`.
- `HEAD` and `origin/main` were both
  `503239c593dc935e7864bf15df94dae70760ff7f`.
- Candidate exact-code Ruff check passed.
- Full Ruff check passed.
- `tests\test_run_repo_checks_script.py` passed: `1 passed`.
- TOML selected-rule verification passed with exactly:
  `E`, `F`, `I`, `B006`, `B008`, `B012`, `B023`, `B904`, `DTZ002`, `DTZ003`,
  `DTZ004`, `DTZ006`, `DTZ011`, `DTZ012`, and `DTZ901`.
- `git diff --check` passed.
- Agent docs check passed with `errors: 0`, `warnings: 0`.
- Path-scoped protected-surface scan passed with `forbidden: 0`,
  `warnings: 0`.
- Path-scoped secret/private-marker scan passed with `forbidden: 0`,
  `warnings: 0`.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-608-001 | P1 | `fixed_state_followup` | Fixed. Branch freshness now satisfies the contract's current-base validation requirement. | not_blocking | Initial Codex E review found `git rev-list --left-right --count HEAD...origin/main` returned `0 2`; local `HEAD` was `83d3141e953913233e3457b910c2c83ff25d44aa`, while `origin/main` was `503239c593dc935e7864bf15df94dae70760ff7f`. | Confirmation review found `HEAD` and `origin/main` both at `503239c593dc935e7864bf15df94dae70760ff7f` with `0 0`; exact-code Ruff, full Ruff, repo-check helper test, diff check, docs check, protected-surface scan, and secret/private-marker scan all passed. | F |

## Confirmed Contract Matches

- `pyproject.toml` adds exactly `B006`, `B008`, `B012`, `B023`, and `B904`.
- Existing selected codes remain present.
- Broad `B` is not selected.
- `B909` is not selected.
- `ALL` is not selected.
- Ruff preview mode is not enabled.
- No autofix or unsafe-fix configuration was introduced.
- `.github/workflows/repo-checks.yml` keeps lint command
  `py -m ruff check src tests tools`.
- `tools/run_repo_checks.ps1` keeps lint command
  `py -m ruff check src tests tools`.
- `tests/test_run_repo_checks_script.py` still pins local helper lint scope to
  `src tests tools`.
- No #605 coverage-policy files or coverage artifacts were changed.
- No parser/runtime/product behavior changed.

## Contract Mismatches

None remain.

## Missing Tests

No blocking missing test was found for the local helper scope. The existing
test still covers the repo-check helper lint command shape.

## Drift Notes

- Repo drift: resolved by current-base refresh.
- CI drift: none observed in reviewed files.
- #605 lane drift: none introduced; #605 was not changed by this branch.
- Parser/runtime/downstream drift: none introduced.

## Recommendation

Approve for Codex F submitter. Codex F should stage only the reviewed #608
files and open a draft PR. Do not close #608 or tracker #567 from the submitter
thread.

## Remaining Risk

- GitHub Actions has not run for this branch until Codex F submits it.
- If `origin/main` advances again before submission or merge readiness, refresh
  evidence again.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #608.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/608

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Branch:
codex/ruff-second-bug-tranche-567

Base branch:
main

Reviewed contract:
docs/contracts/quality_ruff_second_bug_risk_tranche.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_second_bug_risk_tranche_comparison.md

Contract-test report:
docs/contract_test_reports/quality_ruff_second_bug_risk_tranche.md

Goal:
Stage only the reviewed #608 files, commit, push the branch, and open a draft
PR. Use Refs #608 and Refs #567, not Closes, unless issue closeout is
explicitly authorized later.

Before staging:
- Run git status --short --branch --untracked-files=all.
- Confirm the dirty set matches the reviewed #608 package.
- Exclude unrelated files, raw logs, generated/private artifacts, local-only
  artifacts, coverage artifacts, and issue #605 coverage-policy work.

Recommended validation before submit:
- py -m ruff check src tests tools --select B006,B008,B012,B023,B904
- py -m ruff check src tests tools
- py -m pytest -q tests\test_run_repo_checks_script.py
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over staged/reviewed files
- path-scoped secret/private-marker scan over staged/reviewed files

Do not add broad B, add B909, enable preview mode, run autofix or unsafe-fix,
rerun all-rules Ruff advisory measurement, close #608, mark tracker #567
complete, change #605, or change parser/runtime/product behavior.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/608"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/quality_ruff_second_bug_risk_tranche.md"
  implementation_handoff: "docs/implementation_handoffs/quality_ruff_second_bug_risk_tranche_comparison.md"
  artifact_produced: "docs/contract_test_reports/quality_ruff_second_bug_risk_tranche.md"
  risk_tier: "Medium-High workflow risk; low runtime risk"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/ruff-second-bug-tranche-567"
  reviewed_head: "503239c593dc935e7864bf15df94dae70760ff7f"
  branch_sync: "0 0 with origin/main"
  fixed_findings:
    - "CT-608-001 P1 fixed: branch refreshed onto current origin/main and current-base validation reran."
  candidate_codes_promoted:
    - "B006"
    - "B008"
    - "B012"
    - "B023"
    - "B904"
  excluded_codes:
    - "B909"
  validation:
    - "py -m ruff check src tests tools --select B006,B008,B012,B023,B904 -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "py -m pytest -q tests\\test_run_repo_checks_script.py -> passed, 1 passed"
    - "selected-rule TOML verification -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter"
```
