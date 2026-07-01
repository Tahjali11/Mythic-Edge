# Quality Coverage Global Line Floor Enforcement Readiness Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

Codex D: Module Fixer continuation for CT-595-001 stale coverage proof.

## Issue And Tracker

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/595>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/566>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

## Contract Used

- `docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md`

## Branch And Git Status

- Branch: `codex/coverage-enforcement-readiness-566`
- Base ref: `origin/main`
- Current HEAD: `3948e5204ae3372b6418c456297467fa8ca788bf`
- `origin/main`: `3948e5204ae3372b6418c456297467fa8ca788bf`
- Branch sync: `0 0` with `origin/main`
- Initial dirty state after this continuation picked up the worktree: an active
  #595 implementation package was already present, plus an untracked Codex E
  contract-test report.
- Codex D refreshed the branch from `cf7147554cdc3c92bfde5d38f4f7afd265bd8b46`
  to current `origin/main` at `3948e5204ae3372b6418c456297467fa8ca788bf`.

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md`
- `docs/implementation_handoffs/quality_coverage_ci_environment_remeasurement.md`
- `docs/contract_test_reports/quality_coverage_ci_environment_remeasurement.md`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `tools/select_validation_mappings.py`

## Current Behavior Compared To Contract

The repository already had `pytest-cov` configured for `src/mythic_edge_parser`
with branch measurement enabled in `pyproject.toml`. The local
`tools/run_repo_checks.ps1 -Coverage` helper collected coverage but did not
enforce a floor. The GitHub Actions repo-check workflow ran tests without
coverage enforcement.

The #591 / PR #594 measurement at commit
`d9a9c335561b7af6e8e1f6745c712741267eed5d` remains useful historical evidence,
but it is stale for activation because current `origin/main` is
`3948e5204ae3372b6418c456297467fa8ca788bf`.

The first implementation continuation fast-forwarded the branch from
`5ab26801...` to `cf714755...` and proved the gate there. Codex E then found
that `origin/main` had advanced to `3948e52...`. This Codex D continuation
fast-forwarded the branch to `3948e52...` and reran the coverage helper with
the gate active on the synced current base:

```yaml
measured_commit: "3948e5204ae3372b6418c456297467fa8ca788bf"
tests_passed: 2015
tests_skipped: 4
line_coverage_percent: 87.55
branch_coverage_percent: 74.80
global_line_floor_percent: 85.00
branch_coverage_posture: advisory_only
raw_coverage_artifacts_committed: false
```

## Implementation Option Chosen

Implemented a small XML aggregate checker instead of using pytest-cov's direct
`--cov-fail-under` flag.

Reason: the repo currently enables branch measurement. In this configuration,
the terminal `TOTAL` cover display can read as a combined coverage value while
the contract authorizes only the global Python line percentage as a blocking
floor. A custom checker over coverage XML keeps the first gate aligned to the
contract: line coverage blocks at 85.00%, branch coverage is shown as
advisory-only, and no branch threshold is enforced.

## Files Changed

- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `tools/check_coverage_floor.py`
- `tests/test_check_coverage_floor.py`
- `tools/select_validation_mappings.py`
- `docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md`
- `docs/implementation_handoffs/quality_coverage_global_line_floor_enforcement_readiness_comparison.md`
- `docs/contract_test_reports/quality_coverage_global_line_floor_enforcement_readiness.md`

## Exact Sections Changed

- `.github/workflows/repo-checks.yml`
  - Replaced the plain test step with a coverage-producing test step.
  - Added `tools/check_coverage_floor.py` as the workflow line-floor gate.
  - Writes coverage artifacts only under ignored `_review_/...` paths.

- `tools/run_repo_checks.ps1`
  - Added the same 85.00% global line floor to `-Coverage`.
  - Preserved the existing non-coverage test path.
  - Keeps branch coverage advisory-only through the checker message.

- `tools/check_coverage_floor.py`
  - Added a stdlib-only coverage XML aggregate checker.
  - Enforces only `line-rate`.
  - Reports `branch-rate` as advisory-only.
  - Avoids echoing raw file paths in missing or malformed XML errors.
  - Provides contract-aligned remediation wording.
  - Codex D clarified the passing branch-coverage message so a successful run
    says branch coverage did not affect the result rather than mentioning a
    failure.

- `tests/test_check_coverage_floor.py`
  - Added focused tests for pass, fail, missing XML, malformed XML, and missing
    branch-rate behavior.
  - Updated focused expectations for the clearer successful branch advisory
    message.

- `tools/select_validation_mappings.py`
  - Added focused validation mapping for the new checker and its test file.

- `docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md`
  - Preserved the contract artifact in the implementation scope.

- `docs/implementation_handoffs/quality_coverage_global_line_floor_enforcement_readiness_comparison.md`
  - Added this implementation comparison and handoff.

## Change Type

- Code changed: yes, validation helper and workflow/helper wiring.
- Tests changed: yes, focused checker tests and validation selection mapping.
- Docs changed: yes, contract included and handoff produced.
- Coverage gate changed: yes, a blocking 85.00% global Python line floor is now
  wired through repo-approved checks.
- Branch coverage enforcement changed: no, branch coverage remains
  advisory-only.

## Validation Run

```powershell
py -m pytest -q tests\test_check_coverage_floor.py tests\test_select_validation.py
```

Result: passed, `40 passed`.

```powershell
py -m ruff check src tests tools
```

Result: passed.

```powershell
.\tools\run_repo_checks.ps1 -Coverage
```

Result: passed, `2015 passed, 4 skipped`; global Python line coverage
`87.55%`; branch coverage `74.80%` advisory-only; 85.00% line floor passed.
This was rerun after fast-forwarding to current `origin/main` at
`3948e5204ae3372b6418c456297467fa8ca788bf`.

```powershell
git diff --check
```

Result: passed. Git reported an existing line-ending normalization warning for
`tools/run_repo_checks.ps1`; no whitespace errors were found.

```powershell
direct whitespace/final-newline check over untracked package files
```

Result: passed.

```powershell
py tools\check_agent_docs.py
```

Result: passed, `errors: 0`, `warnings: 0`.

```powershell
@'
.github/workflows/repo-checks.yml
tools/run_repo_checks.ps1
tools/select_validation_mappings.py
tools/check_coverage_floor.py
tests/test_check_coverage_floor.py
docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md
docs/implementation_handoffs/quality_coverage_global_line_floor_enforcement_readiness_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Result: passed, `forbidden: 0`, `warnings: 2`. Warnings were for the
contract-authorized environment/runtime validation surfaces:
`.github/workflows/repo-checks.yml` and `tools/run_repo_checks.ps1`.
The scan also included the untracked Codex E report so the full visible
changed set was checked.

```powershell
@'
.github/workflows/repo-checks.yml
tools/run_repo_checks.ps1
tools/select_validation_mappings.py
tools/check_coverage_floor.py
tests/test_check_coverage_floor.py
docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md
docs/implementation_handoffs/quality_coverage_global_line_floor_enforcement_readiness_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

Result: passed, `forbidden: 0`, `warnings: 0`.
The scan also included the untracked Codex E report so the full visible
changed set was checked.

## Protected-Surface Status

Path-scoped protected-surface scan passed with `forbidden: 0` and two
contract-authorized warnings for `.github/workflows/repo-checks.yml` and
`tools/run_repo_checks.ps1`.

No parser behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, fixtures, corpus status, analytics schema,
workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
behavior, OpenAI/model-provider behavior, AI/coaching behavior, production
behavior, or privacy/security scanner policy was intentionally changed.

## Raw Artifact Status

Coverage execution created local generated coverage artifacts only under
ignored `_review_/...` paths. No raw coverage XML, `.coverage` files, terminal
transcripts, HTML coverage output, local absolute paths, private artifacts,
secrets, raw logs, generated SQLite files, failed posts, workbook exports, or
local-only artifacts were added to the tracked change set.

## Remaining Risk

- GitHub Actions has not yet run this new workflow step after the local
  implementation.
- If `origin/main` moves before merge/readiness, Codex E or Codex G should
  require fresh CI-equivalent coverage evidence again.
- The first floor has a 2.55 point line-coverage margin on the measured base;
  future feature work may need focused tests to preserve the floor.

## What Remains Unverified

- Actual GitHub Actions execution of the updated repo-check workflow.
- Post-rebase or post-merge coverage if the base advances beyond
  `3948e5204ae3372b6418c456297467fa8ca788bf`.

## Forbidden Scope

Forbidden scope was not intentionally touched.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #595.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/595

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Branch:
codex/coverage-enforcement-readiness-566

Contract:
docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md

Implementation handoff:
docs/implementation_handoffs/quality_coverage_global_line_floor_enforcement_readiness_comparison.md

Expected review artifact:
docs/contract_test_reports/quality_coverage_global_line_floor_enforcement_readiness.md

Goal:
Review the #595 implementation against the contract. Verify that current-base
coverage evidence exists before enforcement, the implemented gate enforces only
the 85.00% global Python line coverage floor, branch coverage remains
advisory-only, raw coverage artifacts remain untracked, and no protected
parser/corpus/production/security/privacy/analytics/AI/coaching behavior was
changed.

Inspect:
- git status --short --branch --untracked-files=all
- docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md
- docs/implementation_handoffs/quality_coverage_global_line_floor_enforcement_readiness_comparison.md
- pyproject.toml
- .github/workflows/repo-checks.yml
- tools/run_repo_checks.ps1
- tools/check_coverage_floor.py
- tests/test_check_coverage_floor.py
- tools/select_validation_mappings.py
- current ignored/generated coverage artifact status

Validation:
- py -m pytest -q tests\test_check_coverage_floor.py tests\test_select_validation.py
- py -m ruff check src tests tools
- .\tools\run_repo_checks.ps1 -Coverage
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over changed files with base origin/main
- path-scoped secret/private-marker scan over changed files with base origin/main

Review requirements:
- Lead with findings, ordered by severity.
- Treat any branch coverage enforcement as blocking.
- Treat stale-base enforcement without fresh coverage evidence as blocking.
- Treat committed raw coverage artifacts as blocking.
- Do not dismiss issue #595 or close tracker #566.
- Do not stage, commit, push, merge, or deploy.

Final output must include:
- role performed
- issue/tracker reviewed
- contract and handoff reviewed
- findings
- fresh-base coverage evidence status
- line-floor enforcement status
- branch advisory-only status
- raw-artifact status
- validation run and result
- protected-surface status
- secret/private-marker status
- remaining risk
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/595"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "D"
  next_thread: "E"
  branch: "codex/coverage-enforcement-readiness-566"
  base_ref: "origin/main"
  current_head: "3948e5204ae3372b6418c456297467fa8ca788bf"
  contract_artifact: "docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md"
  implementation_handoff: "docs/implementation_handoffs/quality_coverage_global_line_floor_enforcement_readiness_comparison.md"
  review_artifact: "docs/contract_test_reports/quality_coverage_global_line_floor_enforcement_readiness.md"
  implemented_gate: "blocking_85_00_percent_global_python_line_coverage_floor"
  branch_coverage_posture: "advisory_only"
  fresh_measurement:
    measured_commit: "3948e5204ae3372b6418c456297467fa8ca788bf"
    line_coverage_percent: 87.55
    branch_coverage_percent: 74.80
    tests_passed_after_gate: 2015
    tests_skipped_after_gate: 4
  stale_measurement:
    historical_commit: "d9a9c335561b7af6e8e1f6745c712741267eed5d"
    status: "historical_only_not_activation_evidence"
  validation:
    - "py -m pytest -q tests\\test_check_coverage_floor.py tests\\test_select_validation.py -> passed, 40 passed"
    - "py -m ruff check src tests tools -> passed"
    - ".\\tools\\run_repo_checks.ps1 -Coverage -> passed, 2015 passed, 4 skipped, line 87.55%, branch 74.80% advisory-only"
    - "git diff --check -> passed, line-ending warning only"
    - "direct whitespace/final-newline check over untracked package files -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 2 contract-authorized validation surfaces"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  protected_surfaces_touched: false
  raw_coverage_artifacts_committed: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
