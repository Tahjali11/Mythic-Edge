# Implementation Handoff: Parser-State Final-Reconciliation Coverage Floor

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/625

Related:

- Threshold review: https://github.com/Tahjali11/Mythic-Edge/issues/632
- Retry-gate completion: https://github.com/Tahjali11/Mythic-Edge/issues/635

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/566

## Contract

`docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md`

## Internal Project Area

Quality / validation gates, with a protected-surface relationship to Parser.

## Truth Owner

The parser/state layer owns parser truth, final reconciliation behavior, match
facts, game facts, match/game identity, and deduplication.

Coverage tooling owns only pass/fail validation for configured coverage
thresholds. It does not prove parser correctness.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Artifacts Used

- Issue #625
- Issue #632
- Issue #635
- Tracker #566
- `docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md`
- `docs/implementation_handoffs/quality_parser_state_final_reconciliation_test_hardening_comparison.md`
- `docs/contract_test_reports/quality_parser_state_final_reconciliation_test_hardening.md`
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`

## Branch And Git Status

Branch:

```text
codex/parser-state-coverage-floor-retry-625
```

Base:

```text
origin/main
```

Current base commit at implementation time:

```text
27d35146d7d5eb094611d941ad8111f2981d83db
```

Branch sync before implementation:

```text
git rev-list --left-right --count HEAD...origin/main -> 0 0
```

Starting status:

```text
## codex/parser-state-coverage-floor-retry-625...origin/main
?? docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md
```

## Files Inspected

- `tools/check_coverage_floor.py`
- `tools/run_repo_checks.ps1`
- `.github/workflows/repo-checks.yml`
- `tests/test_check_coverage_floor.py`
- `tests/test_run_repo_checks_script.py`
- `tests/test_protected_surface_coverage_report.py`
- `pyproject.toml`
- `docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md`
- `docs/implementation_handoffs/quality_parser_state_final_reconciliation_test_hardening_comparison.md`
- `docs/contract_test_reports/quality_parser_state_final_reconciliation_test_hardening.md`

## Current Behavior Compared To Contract

Before this implementation:

- `tools/check_coverage_floor.py` enforced only the global Python line floor.
- The global line floor was `85.00%`.
- Branch coverage was parsed and reported as advisory-only.
- `tools/run_repo_checks.ps1 -Coverage` invoked the global floor checker.
- `.github/workflows/repo-checks.yml` invoked the same global floor checker.
- No protected-surface floor existed for `parser_state_final_reconciliation`.

The contract required one additional allow-listed, line-only protected-surface
floor:

- group: `parser_state_final_reconciliation`
- candidate files:
  - `src/mythic_edge_parser/app/models.py`
  - `src/mythic_edge_parser/app/state.py`
- floor: `88.00%` per required file
- pass rule: every required file must be measured and at or above the floor
- group reported percent: minimum required-file line coverage
- branch coverage: advisory-only

## Fresh-Base Preconditions

Codex C reran a clean full coverage command before implementation:

```powershell
.\tools\run_repo_checks.ps1 -Coverage
```

Pre-implementation result:

- tests: `2054 passed, 4 skipped, 1 warning`
- global Python line coverage: `87.64%`
- branch coverage: `74.86%`, advisory-only
- `src/mythic_edge_parser/app/models.py` line coverage: `90.45%`
- `src/mythic_edge_parser/app/state.py` line coverage: `92.96%`

The contract preconditions were satisfied:

- global line coverage `>= 85.00%`: yes
- `models.py >= 90.00%`: yes
- `state.py >= 90.00%`: yes
- branch coverage remained advisory-only: yes

## Implementation Option Chosen

Implemented the contract's preferred option:

```yaml
implementation_shape: extend_tools_check_coverage_floor
single_enforcement_authority: tools/check_coverage_floor.py
advisory_report_helper_changed: false
global_floor_changed: false
branch_coverage_enforced: false
```

## Files Changed

- `.github/workflows/repo-checks.yml`
- `tools/check_coverage_floor.py`
- `tools/run_repo_checks.ps1`
- `tests/test_check_coverage_floor.py`
- `tests/test_run_repo_checks_script.py`
- `docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md`
  - preserved as the Codex B contract artifact.
- `docs/implementation_handoffs/quality_parser_state_final_reconciliation_coverage_floor_implementation_comparison.md`

## Exact Sections Changed

### `tools/check_coverage_floor.py`

Added:

- `DEFAULT_PROTECTED_SURFACE_LINE_FLOOR = 88.0`
- allow-listed group `parser_state_final_reconciliation`
- required file list for `models.py` and `state.py`
- coverage XML class filename normalization for:
  - `src/mythic_edge_parser/app/state.py`
  - `mythic_edge_parser/app/state.py`
  - `app/state.py`
- protected-surface group evaluation using the minimum required-file line
  percentage
- fail-closed handling for:
  - unsupported group
  - missing required file
  - missing or invalid required file line-rate
- public-safe failure messages that use repo-relative paths and do not echo raw
  coverage XML paths
- CLI options:
  - `--protected-surface-group`
  - `--protected-surface-line-floor`

Preserved:

- existing global-only behavior when no protected-surface group is requested
- global `85.00%` line floor behavior
- branch coverage advisory-only status
- missing/malformed XML symbolic failures

### `tools/run_repo_checks.ps1`

Added:

- `$ProtectedSurfaceCoverageGroup = "parser_state_final_reconciliation"`
- `$ProtectedSurfaceCoverageFloorPercent = "88"`
- protected-surface CLI args to the existing `-Coverage` checker invocation

The local command now checks:

```powershell
py tools/check_coverage_floor.py `
  --coverage-xml $CoverageXml `
  --line-floor $CoverageFloorPercent `
  --protected-surface-group $ProtectedSurfaceCoverageGroup `
  --protected-surface-line-floor $ProtectedSurfaceCoverageFloorPercent `
  --command-label "tools/run_repo_checks.ps1 -Coverage"
```

### `.github/workflows/repo-checks.yml`

Added the same protected-surface group and floor to the GitHub Actions repo
checks coverage step:

```powershell
py tools/check_coverage_floor.py `
  --coverage-xml $coverageXml `
  --line-floor 85 `
  --protected-surface-group parser_state_final_reconciliation `
  --protected-surface-line-floor 88 `
  --command-label "GitHub Actions repo checks"
```

### `tests/test_check_coverage_floor.py`

Added focused coverage checker tests for:

- protected-surface pass when both required files are measured at or above
  `88.00%`
- pytest-cov filename variants
- `models.py` below floor
- `state.py` below floor
- missing required file
- invalid required file line-rate
- branch coverage remaining advisory-only
- unsupported protected-surface group rejected without private path echo

Existing global-only tests remained in place.

### `tests/test_run_repo_checks_script.py`

Added assertions that:

- local `tools/run_repo_checks.ps1 -Coverage` invokes the new group/floor
- GitHub Actions repo checks invoke the same group/floor
- the global `85.00%` floor remains present

## Code Changed

Runtime/product code changed: no.

Quality tooling changed: yes.

Coverage enforcement changed: yes, narrowly. The existing global line floor is
unchanged, and a single allow-listed protected-surface line floor is now added
to local and CI coverage checks.

## Tests Changed

Yes.

- `tests/test_check_coverage_floor.py`
- `tests/test_run_repo_checks_script.py`

## Interface Changes

Checker CLI additions:

- `--protected-surface-group`
- `--protected-surface-line-floor`

No parser interfaces, payload fields, workbook columns, environment variables,
runtime APIs, or product routes changed.

## Contracted Area Status

The implementation stayed inside Quality / validation tooling. It measures a
parser protected surface but does not alter parser code or parser behavior.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
# before implementation:
# ## codex/parser-state-coverage-floor-retry-625...origin/main
# ?? docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md

git rev-list --left-right --count HEAD...origin/main
# 0 0

.\tools\run_repo_checks.ps1 -Coverage
# pre-implementation: 2054 passed, 4 skipped, 1 warning
# pre-implementation: global line 87.64%; branch 74.86% advisory-only
# pre-implementation XML parse:
#   src/mythic_edge_parser/app/models.py line 90.45%
#   src/mythic_edge_parser/app/state.py line 92.96%

py -m pytest -q tests\test_check_coverage_floor.py tests\test_run_repo_checks_script.py
# 16 passed in 0.59s

.\tools\run_repo_checks.ps1 -Coverage
# post-implementation: 2064 passed, 4 skipped, 1 warning
# post-implementation: global line 87.64%; branch 74.86% advisory-only
# post-implementation protected-surface minimum: 90.45%
# post-implementation candidate measurements:
#   src/mythic_edge_parser/app/models.py line 90.45%
#   src/mythic_edge_parser/app/state.py line 92.96%

py -m ruff check tools\check_coverage_floor.py tests\test_check_coverage_floor.py tests\test_run_repo_checks_script.py
# All checks passed!

git diff --check
# passed

py tools\check_agent_docs.py
# passed: checked_files 52, errors 0, warnings 0

@'
.github/workflows/repo-checks.yml
tools/check_coverage_floor.py
tools/run_repo_checks.ps1
tests/test_check_coverage_floor.py
tests/test_run_repo_checks_script.py
docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md
docs/implementation_handoffs/quality_parser_state_final_reconciliation_coverage_floor_implementation_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
# passed: forbidden 0, warnings 2
# warnings are contract-authorized environment/runtime path warnings for:
#   .github/workflows/repo-checks.yml
#   tools/run_repo_checks.ps1

@'
.github/workflows/repo-checks.yml
tools/check_coverage_floor.py
tools/run_repo_checks.ps1
tests/test_check_coverage_floor.py
tests/test_run_repo_checks_script.py
docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md
docs/implementation_handoffs/quality_parser_state_final_reconciliation_coverage_floor_implementation_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
# passed: forbidden 0, warnings 0

changed-file whitespace/final-newline check
# passed
```

## Protected-Surface Status

Passed with contract-authorized warnings.

Path-scoped scan over changed files and the untracked contract/handoff:

- forbidden: `0`
- warnings: `2`
- result: passed

Warnings:

- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`

Assessment:

- The warnings are expected because the contract explicitly authorizes local
  and CI validation-command wiring.
- No parser runtime files changed.
- No parser state final reconciliation behavior changed.

## Secret / Private-Marker Status

Passed.

Path-scoped scan over changed files and the untracked contract/handoff:

- forbidden: `0`
- warnings: `0`
- result: passed

No raw Player.log data, private paths, raw JSONL, SQLite contents, runtime
artifacts, workbook exports, secrets, credentials, tokens, webhook URLs, or
local-only artifacts were added.

## Generated / Private Artifact Status

`.\tools\run_repo_checks.ps1 -Coverage` generated local coverage artifacts
under ignored `_review_/quality_coverage_global_line_floor/run_repo_checks/`.

Those artifacts did not appear in `git status` and are not part of the package.

No raw coverage XML, `.coverage` file, HTML coverage output, private logs,
runtime files, or local-only artifacts were committed.

## Still Unverified

- GitHub Actions has not run this branch.
- Codex E has not yet independently reviewed the contract match.
- The protected-surface scan produced two expected warnings for contract-
  authorized validation-tooling paths; Codex E should verify those warnings are
  acceptable.

## Reviewer Focus

Codex E should verify:

- the new protected-surface floor is exactly scoped to
  `parser_state_final_reconciliation`;
- the group requires every candidate file to be present and at or above
  `88.00%`;
- the reported group percentage is the minimum required-file line coverage,
  not an average;
- branch coverage remains advisory-only;
- global `85.00%` line floor behavior is preserved;
- local and CI coverage invocations use the same group and floor;
- failure output is public-safe and repo-relative;
- no parser behavior, parser final reconciliation behavior, or product runtime
  behavior changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #625.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/625

Threshold review issue:
https://github.com/Tahjali11/Mythic-Edge/issues/632

Retry-gate issue:
https://github.com/Tahjali11/Mythic-Edge/issues/635

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Branch:
codex/parser-state-coverage-floor-retry-625

Contract:
docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md

Implementation handoff:
docs/implementation_handoffs/quality_parser_state_final_reconciliation_coverage_floor_implementation_comparison.md

Risk tier:
Medium-High workflow/validation-gate risk; high protected-surface sensitivity.

Goal:
Review the Codex C implementation of the first narrow parser_state_final_reconciliation protected-surface line coverage floor against the contract.

Review focus:
- Confirm fresh-base preconditions were satisfied before implementation:
  - global Python line coverage >= 85.00%;
  - src/mythic_edge_parser/app/models.py line coverage >= 90.00%;
  - src/mythic_edge_parser/app/state.py line coverage >= 90.00%;
  - branch coverage advisory-only.
- Confirm tools/check_coverage_floor.py remains the single coverage-floor enforcement authority.
- Confirm the new protected-surface floor is allow-listed only for parser_state_final_reconciliation.
- Confirm both candidate files must be measured and each must be at or above 88.00%.
- Confirm the protected-surface group reports the minimum required-file line coverage, not an average.
- Confirm missing/malformed XML, missing candidate files, invalid line-rate, and unsupported group fail closed with public-safe messages.
- Confirm branch coverage remains advisory-only and cannot fail validation.
- Confirm tools/run_repo_checks.ps1 -Coverage and .github/workflows/repo-checks.yml use the same group/floor.
- Confirm no parser behavior, parser state final reconciliation behavior, parser event classes, match/game identity, deduplication, analytics behavior, workbook/webhook/App Script/Sheets behavior, OpenAI/AI/coaching behavior, Line Tracer behavior, or production behavior changed.
- Confirm no raw coverage artifacts, private logs, generated files, secrets, or local-only artifacts are included.

Suggested validation:
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
py -m pytest -q tests\test_check_coverage_floor.py tests\test_run_repo_checks_script.py
.\tools\run_repo_checks.ps1 -Coverage
py -m ruff check tools\check_coverage_floor.py tests\test_check_coverage_floor.py tests\test_run_repo_checks_script.py
git diff --check
py tools\check_agent_docs.py
git diff --name-only origin/main | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --name-only origin/main | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin

Do not:
- Edit implementation files in Codex E unless explicitly asked.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics schema, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, OpenAI/AI/coaching behavior, Line Tracer behavior, or production behavior.
- Raise or lower the global 85.00% line floor.
- Enforce branch coverage.
- Add any other protected-surface floor.
- Change pyproject.toml.
- Stage, commit, push, open a PR, merge, or close issues unless explicitly asked.

Final output must include:
- findings first, ordered by severity;
- contract-test verdict;
- validation run and results;
- protected-surface and secret/private-marker status;
- raw/generated artifact status;
- whether #625 can route to Codex F or needs Codex D/B/A;
- next recommended role;
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/625"
  threshold_review_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/632"
  retry_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/635"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "Issue #625 plus #635 retry-gate completion evidence"
  contract_artifact: "docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md"
  target_artifact: "docs/implementation_handoffs/quality_parser_state_final_reconciliation_coverage_floor_implementation_comparison.md"
  risk_tier: "Medium-High workflow/validation-gate risk; high protected-surface sensitivity"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/parser-state-coverage-floor-retry-625"
  current_base_commit: "27d35146d7d5eb094611d941ad8111f2981d83db"
  candidate_group: "parser_state_final_reconciliation"
  candidate_files:
    - "src/mythic_edge_parser/app/models.py"
    - "src/mythic_edge_parser/app/state.py"
  floor_policy:
    metric: "line_coverage_only"
    protected_surface_floor_percent: "88.00"
    global_line_floor_percent: "85.00 unchanged"
    branch_coverage: "advisory_only"
    pass_rule: "every required candidate file measured and at or above floor"
    reported_percent: "minimum required-file line coverage"
  validation:
    - "git rev-list --left-right --count HEAD...origin/main -> 0 0"
    - ".\\tools\\run_repo_checks.ps1 -Coverage pre-implementation -> 2054 passed, 4 skipped, 1 warning"
    - "precondition global Python line coverage -> 87.64%"
    - "precondition branch coverage -> 74.86%, advisory-only"
    - "precondition models.py line coverage -> 90.45%"
    - "precondition state.py line coverage -> 92.96%"
    - "py -m pytest -q tests\\test_check_coverage_floor.py tests\\test_run_repo_checks_script.py -> 16 passed"
    - ".\\tools\\run_repo_checks.ps1 -Coverage post-implementation -> 2064 passed, 4 skipped, 1 warning"
    - "post-implementation protected-surface minimum line coverage -> 90.45%"
    - "post-implementation branch coverage -> 74.86%, advisory-only"
    - "py -m ruff check changed Python files -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 2 contract-authorized validation-tooling paths"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "changed-file whitespace/final-newline check -> passed"
  stop_conditions:
    - "Do not change parser behavior or parser state final reconciliation."
    - "Do not change parser event classes, match/game identity, deduplication, analytics, workbook/webhook/App Script/Sheets, OpenAI/AI/coaching, Line Tracer, or production behavior."
    - "Do not raise or lower the global 85.00% line floor."
    - "Do not enforce branch coverage."
    - "Do not add any other protected-surface floor."
    - "Do not change pyproject.toml."
    - "Do not commit raw coverage artifacts, private logs, generated files, secrets, or local-only artifacts."
```
