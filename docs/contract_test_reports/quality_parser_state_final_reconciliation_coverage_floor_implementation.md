# Contract Test Report: Parser-State Final-Reconciliation Coverage Floor

## Findings

No blocking findings.

No implementation bug, missing required test, privacy leak, parser-truth drift, branch-coverage enforcement, or coverage-policy scope expansion was found.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/625

Related:

- Threshold review issue: https://github.com/Tahjali11/Mythic-Edge/issues/632
- Retry-gate issue: https://github.com/Tahjali11/Mythic-Edge/issues/635

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/566

## Contract

`docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md`

## Implementation Under Test

- Branch: `codex/parser-state-coverage-floor-retry-625`
- Base: `origin/main`
- Branch sync at review time: `0 0`
- Implementation handoff: `docs/implementation_handoffs/quality_parser_state_final_reconciliation_coverage_floor_implementation_comparison.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The contract authorizes one narrow protected-surface Python line coverage floor:

- group: `parser_state_final_reconciliation`
- files:
  - `src/mythic_edge_parser/app/models.py`
  - `src/mythic_edge_parser/app/state.py`
- floor: `88.00%` line coverage per required file
- pass rule: every required file must be measured and at or above the floor
- reported group percent: minimum required-file line coverage, not an average
- branch coverage: advisory-only
- global Python line floor: existing `85.00%` floor preserved

The contract does not authorize parser behavior changes, parser final-reconciliation changes, other protected-surface floors, branch coverage enforcement, `pyproject.toml` changes, or production behavior changes.

## Internal Project Area Reviewed

Quality / validation gates, with a protected-surface relationship to Parser.

Coverage tooling owns validation pass/fail status for configured thresholds only. Parser/state remains the truth owner for parser behavior, match/game facts, identity, deduplication, and final reconciliation.

## Bridge-Code Status Reviewed

`shared_support`

The implementation uses the existing coverage checker as the single enforcement authority and does not turn the advisory protected-surface report helper into an enforcement path.

## Files Reviewed

- `.github/workflows/repo-checks.yml`
- `tools/check_coverage_floor.py`
- `tools/run_repo_checks.ps1`
- `tests/test_check_coverage_floor.py`
- `tests/test_run_repo_checks_script.py`
- `docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md`
- `docs/implementation_handoffs/quality_parser_state_final_reconciliation_coverage_floor_implementation_comparison.md`

## Checks Run

```powershell
git fetch --prune origin main
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
gh issue view 625 --repo Tahjali11/Mythic-Edge --json number,title,state,url
gh issue view 632 --repo Tahjali11/Mythic-Edge --json number,title,state,url
gh issue view 635 --repo Tahjali11/Mythic-Edge --json number,title,state,url
py -m pytest -q tests\test_check_coverage_floor.py tests\test_run_repo_checks_script.py
.\tools\run_repo_checks.ps1 -Coverage
py -m ruff check tools\check_coverage_floor.py tests\test_check_coverage_floor.py tests\test_run_repo_checks_script.py
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over changed files, contract, and handoff
path-scoped secret/private-marker scan over changed files, contract, and handoff
```

## Results

- Branch sync: `0 0` with `origin/main`
- Issue state: #625 open; #632 closed; #635 closed
- Focused tests: `16 passed`
- Full coverage gate: `2064 passed, 4 skipped, 1 warning`, exit code `0`
- Global Python line coverage: `87.64%` against `85.00%` floor
- Protected-surface group minimum line coverage: `90.45%` against `88.00%` floor
- `app/models.py` line coverage: `90.45%`
- `app/state.py` line coverage: `92.96%`
- Branch coverage: `74.86%`, advisory-only
- Ruff: passed
- `git diff --check`: passed with the existing PowerShell line-ending notice only
- Agent docs check: passed, errors `0`, warnings `0`

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| None | N/A | `final_approval` | no findings | not_blocking | N/A | Contract review and validation passed | F |

## Confirmed Contract Matches

- `tools/check_coverage_floor.py` remains the coverage-floor enforcement authority.
- The new protected-surface group is allow-listed as `parser_state_final_reconciliation`.
- Required files are exactly `src/mythic_edge_parser/app/models.py` and `src/mythic_edge_parser/app/state.py`.
- The protected-surface floor is line-only and set to `88.00%`.
- The pass rule requires every required file to be measured and at or above the floor.
- The group percentage is reported as the minimum required-file line coverage.
- Missing required files, invalid file line-rate values, malformed XML, missing XML, and unsupported groups fail closed.
- Failure and success messages use repo-relative candidate paths and do not echo raw coverage XML paths.
- Branch coverage is printed as advisory-only and cannot fail the check.
- `tools/run_repo_checks.ps1 -Coverage` and `.github/workflows/repo-checks.yml` use the same group and floor.
- The existing global `85.00%` floor remains present.
- `pyproject.toml` was not changed.
- No parser runtime files were changed.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests found.

Focused tests cover:

- existing global-only pass behavior;
- existing global-only failure behavior;
- protected-surface pass behavior;
- `models.py` below floor;
- `state.py` below floor;
- missing required file;
- invalid required line-rate;
- missing XML;
- malformed XML;
- unsupported group rejection;
- pytest-cov path variants;
- branch coverage advisory-only behavior;
- local and CI helper invocation wiring.

## Drift Notes

- Issue lifecycle drift: none. #625 remains open; #632 and #635 are closed as expected.
- Repo drift: none observed. Branch is synced with `origin/main`.
- Workbook, deployment, local-data, parser, analytics, AI, and production drift: not applicable to this quality-tooling package.
- GitHub Actions has not run this local branch yet.

## Protected-Surface Status

Path-scoped protected-surface scan:

- Forbidden: `0`
- Warnings: `2`
- Result: passed

The two warnings are for `.github/workflows/repo-checks.yml` and `tools/run_repo_checks.ps1`. They are contract-authorized validation-tooling changes.

## Secret / Private-Marker Status

Path-scoped secret/private-marker scan:

- Forbidden: `0`
- Warnings: `0`
- Result: passed

No raw Player.log, private paths, raw JSONL, SQLite contents, runtime artifacts, workbook exports, secrets, credentials, tokens, webhook URLs, raw coverage XML content, or local-only artifacts were added.

## Generated / Private Artifact Status

The coverage run generated local artifacts under ignored `_review_` coverage output. They did not appear in `git status` and are not part of the package.

Raw coverage artifacts committed: false.

## Forbidden Scope Touched

False.

No parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, fixtures, corpus status, analytics schema, workbook behavior, webhook behavior, Apps Script behavior, Google Sheets behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, production behavior, global floor value, branch coverage policy, or `pyproject.toml` changed.

## Recommendation

Approve for Codex F.

Codex F should stage only the reviewed #625 files and open/update the draft PR. Codex G remains responsible for any later merge, issue closure, tracker update, and CI/deployer closeout.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #625.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/625

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Branch:
codex/parser-state-coverage-floor-retry-625

Base:
origin/main

Contract:
docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md

Implementation handoff:
docs/implementation_handoffs/quality_parser_state_final_reconciliation_coverage_floor_implementation_comparison.md

Review artifact:
docs/contract_test_reports/quality_parser_state_final_reconciliation_coverage_floor_implementation.md

Goal:
Submit the reviewed #625 parser_state_final_reconciliation protected-surface coverage floor package. Stage only reviewed files, commit, push, and open/update a draft PR. Do not merge or close issues.

Reviewed files:
- .github/workflows/repo-checks.yml
- tools/check_coverage_floor.py
- tools/run_repo_checks.ps1
- tests/test_check_coverage_floor.py
- tests/test_run_repo_checks_script.py
- docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md
- docs/implementation_handoffs/quality_parser_state_final_reconciliation_coverage_floor_implementation_comparison.md
- docs/contract_test_reports/quality_parser_state_final_reconciliation_coverage_floor_implementation.md

Validation to confirm before commit:
- git status --short --branch --untracked-files=all
- py -m pytest -q tests\test_check_coverage_floor.py tests\test_run_repo_checks_script.py
- .\tools\run_repo_checks.ps1 -Coverage
- py -m ruff check tools\check_coverage_floor.py tests\test_check_coverage_floor.py tests\test_run_repo_checks_script.py
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over reviewed files
- path-scoped secret/private-marker scan over reviewed files

Do not:
- stage generated _review_ coverage artifacts;
- stage unrelated files;
- change implementation during submitter work unless routed back to Codex D/E;
- merge, close #625, close tracker #566, or target production behavior.

Final output:
- staged files
- commit hash
- PR URL
- validation results
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/625"
  threshold_review_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/632"
  retry_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/635"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md"
  implementation_handoff: "docs/implementation_handoffs/quality_parser_state_final_reconciliation_coverage_floor_implementation_comparison.md"
  review_artifact: "docs/contract_test_reports/quality_parser_state_final_reconciliation_coverage_floor_implementation.md"
  risk_tier: "Medium-High workflow/validation-gate risk; high protected-surface sensitivity"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/parser-state-coverage-floor-retry-625"
  contract_test_verdict: "passed_no_blocking_findings"
  protected_surface_floor:
    group: "parser_state_final_reconciliation"
    line_floor_percent: 88.00
    candidate_files:
      - "src/mythic_edge_parser/app/models.py"
      - "src/mythic_edge_parser/app/state.py"
    branch_coverage: "advisory_only"
    global_line_floor_percent: "85.00 unchanged"
  validation:
    - "git rev-list --left-right --count HEAD...origin/main -> 0 0"
    - "py -m pytest -q tests\\test_check_coverage_floor.py tests\\test_run_repo_checks_script.py -> 16 passed"
    - ".\\tools\\run_repo_checks.ps1 -Coverage -> 2064 passed, 4 skipped, 1 warning"
    - "global Python line coverage -> 87.64%"
    - "parser_state_final_reconciliation minimum line coverage -> 90.45%"
    - "models.py line coverage -> 90.45%"
    - "state.py line coverage -> 92.96%"
    - "branch coverage -> 74.86%, advisory-only"
    - "py -m ruff check changed Python files -> passed"
    - "git diff --check -> passed with existing PowerShell line-ending notice"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 2 contract-authorized"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  protected_surface_status: "passed, forbidden 0, warnings 2 contract-authorized validation-tooling paths"
  secret_private_marker_status: "passed, forbidden 0, warnings 0"
  raw_coverage_artifacts_committed: false
  generated_private_artifacts_kept: false
  forbidden_scope_touched: false
  remaining_risks:
    - "GitHub Actions has not run this local branch yet."
    - "Codex G still owns merge, issue closure, and tracker lifecycle after submitter work."
  next_recommended_role: "Codex F: Module Submitter"
```
