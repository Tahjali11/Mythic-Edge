# Quality Coverage CI Environment Remeasurement

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/591

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/566

## Roadmap

https://github.com/Tahjali11/Mythic-Edge/issues/568

## Source Contract

`docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md`

## Role Performed

Codex C: Module Implementer / report-only measurement executor.

## Acquisition Mode

```yaml
approved_acquisition_mode: "manual_windows_ci_equivalent_runner"
approval_source: "owner chat approval on 2026-07-01, refreshed after origin/main advanced"
measured_branch_ref: "origin/main"
measured_commit: "d9a9c335561b7af6e8e1f6745c712741267eed5d"
stale_ref_policy: "current origin/main accepted after refresh"
runner_label: "owner_main_windows_machine_or_clean_windows_worktree"
python_version: "3.13.7"
install_shape: "py -m pip install -e .[dev]"
coverage_command_id: "quality_coverage_ci_remeasurement.report_only.v1"
coverage_fail_under_used: false
coverage_enforcement_authorized: false
branch_coverage_status: "advisory_only"
candidate_line_floor_status: "proposal_only"
```

## Command Shape

The coverage measurement used the approved report-only shape:

```powershell
$env:COVERAGE_FILE = "_review_/quality_coverage_ci_remeasurement/<run-id>/.coverage"
py -m pytest -q tests `
  --cov=src/mythic_edge_parser `
  --cov-report=term-missing `
  --cov-report="xml:_review_/quality_coverage_ci_remeasurement/<run-id>/coverage.xml"
Remove-Item Env:\COVERAGE_FILE
```

No `--cov-fail-under` flag was used.

## Sanitized Coverage Summary

```yaml
coverage_command_exit_code: 0
tests_passed: 1986
tests_skipped: 4
warnings: 1
line_coverage_percent: 87.55
covered_statements: 22384
total_statements: 25568
missing_statements: 3184
branch_coverage_percent: 74.80
covered_branches: 7737
total_branches: 10344
missing_branches: 2607
measured_package_count: 9
measured_file_count: 116
```

The warning was an existing third-party FastAPI/Starlette/httpx deprecation
warning observed during tests. It is not treated as a coverage failure in this
report-only measurement.

## Baseline Comparison

Prior advisory local baseline from issue #573:

```yaml
measured_commit: "f31923ec2b0da629be3eeb8e7971b21aa57fe9fc"
environment_label: "local-macos-python-3.14.3-arm64"
tests_passed: 1949
line_coverage_percent: 87.56
branch_coverage_percent: 74.87
```

Current manual Windows CI-equivalent measurement:

```yaml
measured_commit: "d9a9c335561b7af6e8e1f6745c712741267eed5d"
environment_label: "manual-windows-python-3.13.7"
tests_passed: 1986
line_coverage_percent: 87.55
branch_coverage_percent: 74.80
```

Delta from the prior advisory local baseline:

```yaml
tests_passed_delta: 37
line_coverage_delta_points: -0.01
branch_coverage_delta_points: -0.07
```

The #575 candidate global line floor remains proposal-only:

```yaml
candidate_line_floor_percent: 85.00
current_line_coverage_margin_points: 2.55
candidate_line_floor_enforced: false
```

## Raw Artifact Handling

Raw coverage artifacts were written only under ignored `_review_/` storage.
They were not copied into this summary, GitHub comments, PR text, or tracked
repository files.

Raw artifacts not committed:

- `.coverage` database
- `coverage.xml`
- raw terminal coverage output
- raw missing-line table

The sanitized summary omits local absolute paths, raw XML, raw terminal logs,
raw missing-line details, private data, secrets, credentials, generated
private artifacts, workbook exports, SQLite contents, runtime artifacts, and
local-only artifacts.

## Current Behavior Compared To Contract

The contract required exactly one approved acquisition mode before execution.
Issue #591 first pinned `0b4a3ff32d924feb2fa434717bf9427b34945eea`, then the
owner explicitly approved refreshing to current `origin/main` after the ref
advanced. The measured commit is therefore
`d9a9c335561b7af6e8e1f6745c712741267eed5d`.

The measurement matched the allowed manual Windows CI-equivalent mode:

- clean sibling worktree
- remote verified as `https://github.com/Tahjali11/Mythic-Edge.git`
- Python 3.13.7 available
- dependencies installed with `py -m pip install -e .[dev]`
- no CI workflow edits
- no temporary workflow
- no `--cov-fail-under`
- raw artifacts local and ignored
- sanitized summary artifact authorized by the owner

## Files Changed

- `docs/implementation_handoffs/quality_coverage_ci_environment_remeasurement.md`

## Code Changed

No runtime code changed.

## Tests Changed

No tests changed.

## Interface Changes

None.

## Validation Run

```text
gh issue view 591 --repo Tahjali11/Mythic-Edge --comments --json number,title,state,url,body,comments -> issue open; manual Windows CI-equivalent approval present
gh issue view 566 --repo Tahjali11/Mythic-Edge --comments --json number,title,state,url,body,comments -> tracker open; #591 approval recorded
git fetch --prune origin -> origin/main advanced to d9a9c335561b7af6e8e1f6745c712741267eed5d
git worktree add -b codex/quality-coverage-ci-remeasurement-591 <local-worktree> origin/main -> worktree created at d9a9c335561b7af6e8e1f6745c712741267eed5d
git status --short --branch --untracked-files=all -> clean on codex/quality-coverage-ci-remeasurement-591 tracking origin/main
git remote -v -> origin https://github.com/Tahjali11/Mythic-Edge.git
py -V -> Python 3.13.7
py -0p -> Python 3.13 is active; Python 3.11 also installed
git check-ignore -v _review_ _review_/quality_coverage_ci_remeasurement/run/coverage.xml -> _review_ artifacts ignored by .gitignore
py -m pip install -e .[dev] -> installed editable package with dev dependencies
py -m pytest -q tests --cov=src/mythic_edge_parser --cov-report=term-missing --cov-report="xml:_review_/quality_coverage_ci_remeasurement/<run-id>/coverage.xml" -> 1986 passed, 4 skipped, 1 warning; coverage command exit code 0
git diff --check -> passed
py tools/check_agent_docs.py -> passed; checked_files: 52; errors: 0; warnings: 0
path-scoped protected-surface scan over docs/implementation_handoffs/quality_coverage_ci_environment_remeasurement.md -> passed; forbidden: 0; warnings: 0
path-scoped secret/private-marker scan over docs/implementation_handoffs/quality_coverage_ci_environment_remeasurement.md -> passed; forbidden: 0; warnings: 0
git status --short --branch --untracked-files=all -> only docs/implementation_handoffs/quality_coverage_ci_environment_remeasurement.md is untracked on codex/quality-coverage-ci-remeasurement-591
git status --short --ignored _review_ -> _review_/ is ignored
local-path/raw-output sweep over the handoff -> no local absolute paths, raw missing-line table, or local user profile path found; only approved symbolic _review_ artifact references were present
```

## Protected Surface Status

No parser behavior, parser state final reconciliation, parser event classes,
match identity, game identity, deduplication, analytics schema, workbook
schema, webhook payload shape, Apps Script behavior, Google Sheets behavior,
OpenAI/model-provider behavior, AI/coaching behavior, production behavior,
fixture promotion, corpus status, #388 activation, or #381 activation changed.

## Secret And Private Artifact Status

No secrets, credentials, raw local logs, private coverage output, SQLite files,
runtime artifacts, workbook exports, raw missing-line tables, raw terminal
coverage logs, or local-only artifacts were added to tracked files.

## Non-Claims

This measurement does not claim:

- parser truth
- parser behavior readiness
- tracker #388 activation readiness
- issue #381 activation readiness
- fixture promotion readiness
- corpus readiness
- private smoke success
- security assurance
- privacy assurance
- release readiness
- deploy readiness
- production readiness
- analytics truth
- AI truth
- coaching truth

## Still Unverified

- GitHub Actions did not run this exact coverage measurement because CI
  workflow edits and temporary workflow creation remain unauthorized.
- Raw coverage artifacts remain local ignored review artifacts and should be
  discarded or left ignored according to reviewer preference before submitter
  work.
- The candidate 85.00% line floor remains proposal-only until a later contract
  authorizes enforcement.

## Reviewer Focus

Codex E should verify:

- the measurement used the approved refreshed `origin/main` commit
- the command omitted `--cov-fail-under`
- the summary contains only aggregate coverage values
- raw coverage artifacts are ignored and untracked
- the report makes no readiness, truth, assurance, release, deploy,
  production, analytics, AI, or coaching claims

## Next Workflow Action

Next role: Codex E: Module Reviewer / Contract Tester.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer / Contract Tester for issue #591.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/591

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Source contract:
docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md

Implementation handoff:
docs/implementation_handoffs/quality_coverage_ci_environment_remeasurement.md

Branch:
codex/quality-coverage-ci-remeasurement-591

Measured commit:
d9a9c335561b7af6e8e1f6745c712741267eed5d

Goal:
Review the report-only manual Windows CI-equivalent coverage remeasurement
against the #580/#591 contract and owner approval. Lead with findings, if any.

Verify:
- acquisition mode was manual_windows_ci_equivalent_runner
- measured ref was current origin/main after owner-approved refresh
- measured commit was d9a9c335561b7af6e8e1f6745c712741267eed5d
- Python was 3.13.7
- install shape was py -m pip install -e .[dev]
- coverage command omitted --cov-fail-under
- branch coverage and the 85.00% line floor remain advisory/proposal-only
- raw coverage artifacts are ignored and untracked
- the sanitized summary contains only aggregate coverage values
- no parser behavior, CI workflow, enforcement, fixture promotion, corpus
  status, #388/#381 activation, or readiness/truth/assurance claim was added

Suggested validation:
- git status --short --branch --untracked-files=all
- git diff --check
- py tools/check_agent_docs.py
- path-scoped protected-surface scan over the handoff artifact
- path-scoped secret/private-marker scan over the handoff artifact

Do not run another coverage measurement unless explicitly asked.
Do not stage, commit, push, open a PR, merge, close #591, or mark tracker #566
complete unless explicitly asked.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/591"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  active_parser_evidence_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/580"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/589"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md"
  target_artifact: "docs/implementation_handoffs/quality_coverage_ci_environment_remeasurement.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/quality-coverage-ci-remeasurement-591"
  verdict: "manual_windows_ci_equivalent_coverage_remeasurement_summary_ready_for_review"
  approved_acquisition_mode: "manual_windows_ci_equivalent_runner"
  measured_branch_ref: "origin/main"
  measured_commit: "d9a9c335561b7af6e8e1f6745c712741267eed5d"
  coverage_command_exit_code: 0
  tests_passed: 1986
  tests_skipped: 4
  line_coverage_percent: 87.55
  branch_coverage_percent: 74.80
  coverage_fail_under_used: false
  coverage_enforcement_authorized: false
  branch_coverage_status: "advisory_only"
  candidate_line_floor_status: "proposal_only"
  raw_artifacts_committed: false
  ci_change_authorized: false
  temporary_workflow_creation_authorized: false
  parser_behavior_change_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  validation:
    - "py -m pytest -q tests --cov=src/mythic_edge_parser --cov-report=term-missing --cov-report=\"xml:_review_/quality_coverage_ci_remeasurement/<run-id>/coverage.xml\" -> 1986 passed, 4 skipped, 1 warning; exit code 0"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan over handoff -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over handoff -> passed, forbidden 0, warnings 0"
    - "git status --short --ignored _review_ -> _review_/ ignored"
  stop_conditions:
    - "Do not use --cov-fail-under."
    - "Do not activate coverage enforcement."
    - "Do not change CI or create temporary workflow files."
    - "Do not commit raw coverage artifacts."
    - "Do not activate #388 or #381."
    - "Do not change parser behavior, promote fixtures, change corpus status, run private harvest, or claim readiness/truth/assurance."
```
