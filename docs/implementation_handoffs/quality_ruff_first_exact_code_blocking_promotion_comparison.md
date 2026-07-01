# Quality Ruff First Exact-Code Blocking Promotion Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/601

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/567

## Project Roadmap

https://github.com/Tahjali11/Mythic-Edge/issues/568

## Contract

`docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md`

## Internal Project Area

Quality tooling and local validation.

## Truth Owner

Ruff owns static lint findings for the configured command, path scope, exact
rule selection, and Ruff version. It does not own parser truth, corpus truth,
security assurance, privacy assurance, release readiness, production behavior,
analytics truth, AI truth, or coaching truth.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Status

- Branch: `codex/ruff-first-exact-code-blocking-contract-567`
- Base: `origin/main`
- Current base verified before implementation: `cf7147554cdc3c92bfde5d38f4f7afd265bd8b46`
- Branch sync before implementation: `0 0` with `origin/main`
- Starting worktree status: one untracked contract artifact.
- Ending worktree status: implementation files modified or untracked; no files staged.

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md`
- `.github/workflows/repo-checks.yml`
- `pyproject.toml`
- `tools/run_repo_checks.ps1`
- `tools/select_validation.py`
- `tools/select_validation_mappings.py`
- `tests/test_select_validation.py`

GitHub context inspected:

- Issue #601
- Tracker #567
- Project roadmap #568

## Current Behavior Compared To Contract

The repo already had clean advisory evidence for the exact first DTZ tranche on
current `origin/main`, and CI already ran `py -m ruff check src tests tools`.
The remaining gaps were:

- `pyproject.toml` still selected only `E`, `F`, and `I`.
- `tools/run_repo_checks.ps1` linted only `src tests`, while CI linted
  `src tests tools`.
- No focused test pinned the local repo-check script to the CI-equivalent Ruff
  path scope.

The contract required promotion of only these exact DTZ codes:

- `DTZ002`
- `DTZ003`
- `DTZ004`
- `DTZ006`
- `DTZ011`
- `DTZ012`
- `DTZ901`

It explicitly did not authorize broad `DTZ`, other DTZ codes, all-rules Ruff,
autofix, unsafe-fix, CI shape changes, parser behavior changes, fixture changes,
corpus status changes, production behavior changes, analytics truth changes,
AI truth changes, or coaching truth changes.

## Implementation Option Chosen

Implemented the smallest coherent blocking-promotion path:

1. Put the exact DTZ rule ownership in `pyproject.toml`.
2. Left `.github/workflows/repo-checks.yml` unchanged because it already uses
   the canonical `py -m ruff check src tests tools` command.
3. Updated the local repo-check helper to match CI path scope.
4. Added one focused script test proving the helper invokes Ruff over
   `src tests tools`.

## Files Changed

- `pyproject.toml`
- `tools/run_repo_checks.ps1`
- `tests/test_run_repo_checks_script.py`
- `docs/implementation_handoffs/quality_ruff_first_exact_code_blocking_promotion_comparison.md`

The Codex B contract remains in scope as an untracked source artifact:

- `docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md`

## Exact Sections Changed

`pyproject.toml`

- Updated `[tool.ruff.lint].select` from `["E", "F", "I"]` to `E`, `F`, `I`,
  and the seven selected exact DTZ codes.

`tools/run_repo_checks.ps1`

- Updated the lint command from `py -m ruff check src tests` to
  `py -m ruff check src tests tools`.

`tests/test_run_repo_checks_script.py`

- Added a focused script-content test asserting the local repo-check helper
  uses the CI-equivalent Ruff path scope.

## Code Changed

No runtime product code changed.

Tooling/configuration changed:

- Ruff rule selection in `pyproject.toml`
- Local validation helper command in `tools/run_repo_checks.ps1`

## Tests Added Or Updated

- Added `tests/test_run_repo_checks_script.py`.

## Interface Changes

No runtime interfaces, parser payloads, workbook columns, API response schemas,
environment variables, or production behavior changed.

Validation interface changed:

- Ruff blocking selection now includes only the exact first DTZ tranche.
- Local repo checks now lint `tools` in addition to `src` and `tests`, matching
  CI.

## Contracted Area Status

Stayed inside the Quality tooling and local validation area.

No parser truth, corpus truth, analytics truth, security assurance, privacy
assurance, release readiness, production readiness, AI truth, coaching truth, or
product runtime behavior was touched.

## Validation Run

Passing before implementation:

```powershell
py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901
py -m ruff check src tests tools
```

Passing after implementation:

```powershell
py -m pytest -q tests\test_run_repo_checks_script.py
py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
@('pyproject.toml','tools/run_repo_checks.ps1','tests/test_run_repo_checks_script.py','docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md','docs/implementation_handoffs/quality_ruff_first_exact_code_blocking_promotion_comparison.md') | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@('pyproject.toml','tools/run_repo_checks.ps1','tests/test_run_repo_checks_script.py','docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md','docs/implementation_handoffs/quality_ruff_first_exact_code_blocking_promotion_comparison.md') | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
git status --short --branch --untracked-files=all
```

Results:

- Focused repo-check helper test passed.
- Exact DTZ Ruff command passed.
- Current configured Ruff command passed.
- `git diff --check` passed. Git emitted a line-ending notice for
  `tools/run_repo_checks.ps1`, but no whitespace errors.
- Agent docs check passed with 0 errors and 0 warnings.
- Path-scoped protected-surface scan passed with 0 forbidden findings and 1
  warning for `tools/run_repo_checks.ps1` as an environment/runtime path surface.
  The warning is inside the contract-authorized validation helper scope.
- Path-scoped secret/private-marker scan passed with 0 forbidden findings and 0
  warnings.
- Final status shows only the intended modified and untracked implementation
  files; nothing is staged.

## Still Unverified

- GitHub Actions has not rerun against this local change.
- Code review has not yet confirmed contract conformance.
- No PR was opened, no commit was created, and no tracker was closed.

## Codex D/C Current-Base Refresh Addendum

### Source Finding

- Review artifact:
  `docs/contract_test_reports/quality_ruff_first_exact_code_blocking_promotion.md`
- Finding fixed:
  `CT-601-001 P1`: current-base validation evidence was stale because the
  branch was behind `origin/main` by two commits.

### Refresh Action

- Fetched `origin`.
- Fast-forwarded `codex/ruff-first-exact-code-blocking-contract-567` from
  `cf7147554cdc3c92bfde5d38f4f7afd265bd8b46` to current `origin/main` at
  `3948e5204ae3372b6418c456297467fa8ca788bf`.
- Confirmed branch sync after refresh: `0 0` against `origin/main`.
- No conflict resolution, product behavior change, CI shape change, or Ruff
  rule-shape change was required.

### Fresh Validation On Current Base

- `py -m pytest -q tests\test_run_repo_checks_script.py`
  - passed: `1 passed`.
- `py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901`
  - passed.
- `py -m ruff check src tests tools`
  - passed.
- `py -c "<tomllib selected-rule check>"`
  - passed; selected Ruff rules exactly matched `E`, `F`, `I`, `DTZ002`,
    `DTZ003`, `DTZ004`, `DTZ006`, `DTZ011`, `DTZ012`, and `DTZ901`.

### Remaining Review Focus After Refresh

- Confirm `CT-601-001` is closed by the current-base refresh and rerun
  validation.
- Confirm the fast-forwarded upstream #597 package did not alter the #601 Ruff
  promotion shape.
- Confirm no Codex F submitter routing occurs until fresh Codex E review
  clears the branch.

## Codex D/C Current-Base Refresh Addendum 2

### Source Finding

- Review artifact:
  `docs/contract_test_reports/quality_ruff_first_exact_code_blocking_promotion.md`
- Finding fixed:
  `CT-601-001 P1`: current-base validation evidence became stale again after
  `origin/main` advanced to #595 coverage enforcement.

### Refresh Action

- Fetched `origin`.
- Fast-forwarded `codex/ruff-first-exact-code-blocking-contract-567` from
  `3948e5204ae3372b6418c456297467fa8ca788bf` to current `origin/main` at
  `024eda7d9408c0bb72d645af4d41d604539291ba`.
- Confirmed branch sync after refresh: `0 0` against `origin/main`.
- Preserved #595 coverage enforcement in `tools/run_repo_checks.ps1`.
- Preserved #601 Ruff lint scope in `tools/run_repo_checks.ps1`:
  `py -m ruff check src tests tools`.
- No product behavior change, CI shape rewrite, broad Ruff rule promotion,
  autofix, unsafe-fix, or parser/runtime behavior change was required.

### Fresh Validation On Current #595 Base

- `py -m pytest -q tests\test_run_repo_checks_script.py tests\test_check_coverage_floor.py`
  - passed: `6 passed`.
- `py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901`
  - passed.
- `py -m ruff check src tests tools`
  - passed.
- `py -c "<tomllib selected-rule check>"`
  - passed; selected Ruff rules exactly matched `E`, `F`, `I`, `DTZ002`,
    `DTZ003`, `DTZ004`, `DTZ006`, `DTZ011`, `DTZ012`, and `DTZ901`.

### Remaining Review Focus After Second Refresh

- Confirm `CT-601-001` is closed on `origin/main` commit
  `024eda7d9408c0bb72d645af4d41d604539291ba`.
- Confirm #595 coverage floor enforcement remains intact.
- Confirm #601 Ruff exact-code promotion still selects only the contracted
  first DTZ tranche.
- Confirm no Codex F submitter routing occurs until fresh Codex E review
  clears the refreshed branch.

## Protected-Surface Status

Passed with 0 forbidden findings and 1 warning for
`tools/run_repo_checks.ps1`. The warning is expected because the contract
explicitly authorized the local repo-check helper alignment.

Protected-surface posture:

- Parser/runtime behavior unchanged.
- Analytics behavior unchanged.
- Workbook, webhook, Apps Script, Sheets, OpenAI, AI, coaching, and production
  behavior unchanged.

## Secret/Private-Marker Status

Passed with 0 forbidden findings and 0 warnings over the changed path set.

No raw logs, secrets, credentials, generated data, runtime artifacts, workbook
exports, private local artifacts, or local-only scanner outputs were added.

## Reviewer Focus

Ask Codex E to verify:

- `pyproject.toml` includes exactly the selected DTZ tranche and no broad DTZ or
  unrelated Ruff rule expansion.
- CI workflow shape remains unchanged.
- `tools/run_repo_checks.ps1` now matches CI path scope.
- The focused script test is sufficient and does not overreach into full helper
  execution.
- No product behavior or protected surfaces changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #601.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/601

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Branch:
codex/ruff-first-exact-code-blocking-contract-567

Base:
origin/main

Contract:
docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_first_exact_code_blocking_promotion_comparison.md

Risk tier:
Medium quality-tooling promotion; higher only if scope expands into unrelated Ruff families, CI shape changes, or protected product behavior.

Goal:
Review the #601 implementation against the contract. Confirm that the first exact-code DTZ Ruff tranche was promoted narrowly, that current-base validation evidence is fresh, and that no unrelated Ruff rules, CI behavior, parser/runtime/analytics/corpus/AI/coaching/production behavior, or private artifact surfaces changed.

Inspect:
- git status --short --branch --untracked-files=all
- docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md
- docs/implementation_handoffs/quality_ruff_first_exact_code_blocking_promotion_comparison.md
- pyproject.toml
- .github/workflows/repo-checks.yml
- tools/run_repo_checks.ps1
- tests/test_run_repo_checks_script.py

Verify:
- pyproject.toml selects exactly E, F, I, DTZ002, DTZ003, DTZ004, DTZ006, DTZ011, DTZ012, and DTZ901.
- No broad DTZ family, all-rules advisory mode, autofix, unsafe-fix, or unrelated Ruff rule family was promoted.
- CI still runs py -m ruff check src tests tools without embedding exact-code command-line flags.
- tools/run_repo_checks.ps1 now uses py -m ruff check src tests tools.
- The focused test covers the repo-check helper scope and stays inside quality tooling.
- No parser behavior, fixtures, corpus status, production behavior, analytics truth, AI truth, coaching truth, protected surfaces, or private artifacts changed.

Run validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_run_repo_checks_script.py
py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py

Run path-scoped protected-surface and secret/private-marker scans over changed files using base origin/main. Include untracked contract and handoff paths through --paths-from-stdin if base-diff tools do not include them.

Do not:
- Stage, commit, push, open a PR, merge, close #601, or mark tracker #567 complete unless explicitly asked.
- Change CI, pyproject scope, or implementation files during review unless routed to Codex D.
- Dismiss this as complete without fresh validation.
- Change parser truth, corpus status, analytics truth, AI/coaching truth, security/privacy assurance, production behavior, secrets, raw logs, generated files, or local-only artifacts.

Final report must include:
- findings first, ordered by severity
- contract conformance verdict
- validation run and result
- protected-surface status
- secret/private-marker status
- remaining risk
- whether Codex F submitter is recommended
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/601"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "D/C"
  next_thread: "E"
  review_artifact: "docs/contract_test_reports/quality_ruff_first_exact_code_blocking_promotion.md"
  contract_artifact: "docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_first_exact_code_blocking_promotion_comparison.md"
  branch: "codex/ruff-first-exact-code-blocking-contract-567"
  base_branch: "main"
  base_ref: "origin/main"
  current_origin_main: "024eda7d9408c0bb72d645af4d41d604539291ba"
  branch_sync_after_refresh: "0 0"
  finding_fixed:
    - "CT-601-001 P1: branch fast-forwarded to current origin/main after #595 coverage enforcement and current-base validation reran."
  selected_exact_codes:
    - "DTZ002"
    - "DTZ003"
    - "DTZ004"
    - "DTZ006"
    - "DTZ011"
    - "DTZ012"
    - "DTZ901"
  implementation_verdict: "exact_dtz_blocking_promotion_refreshed_on_current_coverage_base_pending_review"
  validation:
    - "git rev-list --left-right --count HEAD...origin/main -> 0 0"
    - "py -m pytest -q tests\\test_run_repo_checks_script.py tests\\test_check_coverage_floor.py -> passed, 6 passed"
    - "py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901 -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "py -c <tomllib selected-rule check> -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed, errors 0, warnings 0"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 1 contract-authorized"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "untracked package whitespace/final-newline check -> passed"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
