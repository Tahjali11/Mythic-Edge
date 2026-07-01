# Quality Ruff Second Bug-Risk Tranche Comparison

## Issue

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/608>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/567>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Active separate issue: <https://github.com/Tahjali11/Mythic-Edge/issues/605>

## Contract

- `docs/contracts/quality_ruff_second_bug_risk_tranche.md`

## Internal Project Area

Quality / validation gates.

## Truth Owner

Ruff configuration and repo-check validation own only static-analysis gate
selection. They do not own parser truth, analytics truth, security assurance,
privacy assurance, release readiness, deploy readiness, production readiness,
AI truth, or coaching truth.

## Bridge-Code Status

`shared_support`

The Ruff gate supports the repo's quality workflow. It does not bridge parser
truth into another layer.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Base

- Branch: `codex/ruff-second-bug-tranche-567`
- Base: `origin/main`
- Start/final base commit: `83d3141e953913233e3457b910c2c83ff25d44aa`
- Final branch sync after `git fetch --prune`: `0 0` with `origin/main`

## Current Behavior Compared To Contract

Current repo behavior before this implementation:

- `pyproject.toml` selected `E`, `F`, `I`, and the first exact `DTZ` tranche.
- `.github/workflows/repo-checks.yml` already ran `py -m ruff check src tests tools`.
- `tools/run_repo_checks.ps1` already ran `py -m ruff check src tests tools`.
- `tests/test_run_repo_checks_script.py` already pinned the local helper's lint
  scope to `src tests tools`.
- Fresh current-base validation for `B006,B008,B012,B023,B904` passed before
  editing.

Gap against the contract:

- The second exact bug-risk `B` tranche was not yet selected in `pyproject.toml`.

## Implementation Option Chosen

Implemented the contract-authorized blocking exact-code promotion by adding
only these Ruff codes to `pyproject.toml`:

- `B006`
- `B008`
- `B012`
- `B023`
- `B904`

No CI workflow or local repo-check helper edit was needed because both already
use the repo-approved `src tests tools` lint scope and inherit selected rules
from `pyproject.toml`.

## Excluded Code Decision

`B909` remains excluded. This pass did not enable Ruff preview mode and did not
add any preview-only rule behavior.

## Files Changed

- `pyproject.toml`
- `docs/implementation_handoffs/quality_ruff_second_bug_risk_tranche_comparison.md`
- `docs/contracts/quality_ruff_second_bug_risk_tranche.md` is included as the
  untracked Codex B contract artifact for this issue.

## Code Changed

No runtime code changed.

Configuration changed:

- `pyproject.toml` under `[tool.ruff.lint].select` now includes exactly
  `B006`, `B008`, `B012`, `B023`, and `B904` in addition to the existing
  selected codes.

## Tests Added Or Updated

No tests were added or updated. Existing local helper scope tests already cover
the relevant `tools/run_repo_checks.ps1` lint command shape.

## Interface Changes

Validation behavior changed:

- `py -m ruff check src tests tools` now blocks future findings for exact
  rules `B006`, `B008`, `B012`, `B023`, and `B904`.

No Python API, CLI argument, payload, workbook, webhook, Apps Script, analytics,
parser, or production interface changed.

## Contracted Area Status

The implementation stayed inside the contracted Quality / validation gate area.

Issue #605 protected-surface coverage readiness was not modified or resolved by
this issue.

## Validation Run

Pre-edit validation:

```powershell
git status --short --branch --untracked-files=all
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
py -m ruff check src tests tools --select B006,B008,B012,B023,B904
py -m ruff check src tests tools
```

Results:

- Branch was `codex/ruff-second-bug-tranche-567...origin/main`.
- Branch sync was `0 0`.
- HEAD and `origin/main` were both
  `83d3141e953913233e3457b910c2c83ff25d44aa`.
- Candidate exact-code Ruff check -> `All checks passed!`
- Full current Ruff check -> `All checks passed!`

Post-edit validation completed before final handoff:

```powershell
py -m ruff check src tests tools --select B006,B008,B012,B023,B904
py -m ruff check src tests tools
py -m pytest -q tests\test_run_repo_checks_script.py
git diff --check
py tools\check_agent_docs.py
```

Results:

- Candidate exact-code Ruff check -> `All checks passed!`
- Full current Ruff check -> `All checks passed!`
- `py -m pytest -q tests\test_run_repo_checks_script.py` -> `1 passed`.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed, `errors: 0`, `warnings: 0`.

Path-scoped protected-surface scan over:

- `pyproject.toml`
- `docs/contracts/quality_ruff_second_bug_risk_tranche.md`
- `docs/implementation_handoffs/quality_ruff_second_bug_risk_tranche_comparison.md`

Result: passed, `forbidden: 0`, `warnings: 0`.

Path-scoped secret/private-marker scan over the same files:

Result: passed, `forbidden: 0`, `warnings: 0`.

## Protected-Surface Status

No parser behavior, parser state final reconciliation, parser event classes,
fixture, corpus status, analytics truth, SQLite schema, workbook schema,
webhook payload shape, Apps Script behavior, Sheets behavior, production
behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer
behavior, hidden-card inference, archetype inference, player-mistake labels, or
gameplay advice changed.

## Secret/Private-Marker Status

No secrets, credentials, raw logs, generated/private artifacts, SQLite files,
local app-data, workbook exports, runtime files, or local-only artifacts were
read, copied, generated for commit, or added by this pass.

## Still Unverified

- GitHub Actions has not run this branch/package.
- Codex E should independently verify no broad `B`, `B909`, preview mode,
  autofix, unsafe-fix, or #605 coverage changes are present.

## Codex D/C Current-Base Refresh Addendum

### Source Finding

- Review artifact:
  `docs/contract_test_reports/quality_ruff_second_bug_risk_tranche.md`
- Finding fixed:
  `CT-608-001 P1`: current-base validation evidence was stale because the
  branch was behind `origin/main` by two commits.

### Refresh Action

- Fetched `origin`.
- Fast-forwarded `codex/ruff-second-bug-tranche-567` from
  `83d3141e953913233e3457b910c2c83ff25d44aa` to current `origin/main` at
  `503239c593dc935e7864bf15df94dae70760ff7f`.
- Confirmed branch sync after refresh: `0 0` against `origin/main`.
- Preserved the #608 selected Ruff codes:
  `B006`, `B008`, `B012`, `B023`, and `B904`.
- Preserved the #608 exclusions: no broad `B`, no `B909`, no preview mode, no
  autofix, and no unsafe-fix.
- Preserved the newly merged protected-surface coverage reporting package from
  current `origin/main`; no #608 edits were made to that #609/#605 scope.

### Fresh Validation On Current Base

- `py -m ruff check src tests tools --select B006,B008,B012,B023,B904`
  - passed.
- `py -m ruff check src tests tools`
  - passed.
- `py -m pytest -q tests\test_run_repo_checks_script.py`
  - passed: `1 passed`.
- `py -m pytest -q tests\test_protected_surface_coverage_report.py`
  - passed: `8 passed`.
- `py -c "<tomllib selected-rule verification>"`
  - passed; selected Ruff rules exactly matched `E`, `F`, `I`, `B006`,
    `B008`, `B012`, `B023`, `B904`, `DTZ002`, `DTZ003`, `DTZ004`, `DTZ006`,
    `DTZ011`, `DTZ012`, and `DTZ901`.

### Remaining Review Focus After Refresh

- Confirm `CT-608-001` is closed by the current-base refresh and rerun
  validation.
- Confirm #608 still includes only `B006`, `B008`, `B012`, `B023`, and `B904`
  as the second bug-risk tranche.
- Confirm `B909`, broad `B`, preview mode, autofix, and unsafe-fix remain
  excluded.
- Confirm the fast-forwarded protected-surface coverage package remains
  upstream-only context and was not modified by #608.

## Reviewer Focus

Please verify:

- `pyproject.toml` adds exactly `B006`, `B008`, `B012`, `B023`, and `B904`.
- Existing selected codes remain present.
- No broad `B`, `B909`, preview mode, autofix, unsafe-fix, or all-rules
  advisory measurement was introduced.
- CI and local repo-check lint scope remains `src tests tools`.
- Issue #605 was not modified or resolved in this package.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #608.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/608

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Active separate issue:
https://github.com/Tahjali11/Mythic-Edge/issues/605

Branch:
codex/ruff-second-bug-tranche-567

Contract:
docs/contracts/quality_ruff_second_bug_risk_tranche.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_second_bug_risk_tranche_comparison.md

Goal:
Review the #608 Ruff second bug-risk exact-code promotion against the contract. Confirm that only B006, B008, B012, B023, and B904 were promoted, that existing selected rules remain intact, and that no broad B family, B909, preview mode, autofix, unsafe-fix, all-rules advisory rerun, CI redesign, product behavior change, or #605 coverage-policy work was included.

Review:
- Confirm branch freshness against origin/main.
- Inspect pyproject.toml, .github/workflows/repo-checks.yml, tools/run_repo_checks.ps1, tests/test_run_repo_checks_script.py, the contract, and the handoff.
- Lead with findings ordered by severity.
- If no findings, state that clearly and name any residual risks.

Suggested validation:
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
py -m ruff check src tests tools --select B006,B008,B012,B023,B904
py -m ruff check src tests tools
py -m pytest -q tests\test_run_repo_checks_script.py
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed files.

Do not stage, commit, push, open a PR, merge, close #608, mark tracker #567 complete, change #605, or alter parser/runtime/product behavior unless explicitly asked.

Final output must include:
- role performed
- issue/tracker reviewed
- contract and handoff reviewed
- files reviewed
- findings ordered by severity
- validation run and result
- protected-surface status
- secret/private-marker status
- confirmation that B909/preview/broad B were not included
- confirmation that #605 was not modified
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/608"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  active_separate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/605"
  completed_thread: "D/C"
  next_thread: "E"
  review_artifact: "docs/contract_test_reports/quality_ruff_second_bug_risk_tranche.md"
  source_artifact: "docs/contracts/quality_ruff_second_bug_risk_tranche.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_second_bug_risk_tranche_comparison.md"
  risk_tier: "Medium-High workflow risk; low runtime risk"
  base_branch: "main"
  target_branch: "main_after_explicit_user_approval"
  branch: "codex/ruff-second-bug-tranche-567"
  current_origin_main: "503239c593dc935e7864bf15df94dae70760ff7f"
  branch_sync_after_refresh: "0 0"
  finding_fixed:
    - "CT-608-001 P1: branch fast-forwarded to current origin/main and current-base validation reran."
  candidate_codes_promoted:
    - "B006"
    - "B008"
    - "B012"
    - "B023"
    - "B904"
  excluded_codes:
    - "B909"
  validation:
    - "git rev-list --left-right --count HEAD...origin/main -> 0 0"
    - "py -m ruff check src tests tools --select B006,B008,B012,B023,B904 -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "py -m pytest -q tests\\test_run_repo_checks_script.py -> passed, 1 passed"
    - "py -m pytest -q tests\\test_protected_surface_coverage_report.py -> passed, 8 passed"
    - "py -c <tomllib selected-rule verification> -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed, errors 0, warnings 0"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "untracked package whitespace/final-newline check -> passed"
  stop_conditions:
    - "Do not include issue #605 coverage work."
    - "Do not add broad B, preview mode, or B909."
    - "Do not run Ruff autofix or unsafe-fix."
    - "Do not rerun all-rules Ruff advisory measurement."
    - "Do not change parser behavior, fixtures, corpus status, production behavior, security/privacy assurance, analytics truth, AI truth, or coaching truth."
    - "Do not target main directly without explicit user approval."
```
