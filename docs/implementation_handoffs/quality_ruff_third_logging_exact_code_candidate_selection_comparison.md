# Quality Ruff Third Logging Exact-Code Candidate Selection Comparison

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/618>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/567>

## Project Roadmap

<https://github.com/Tahjali11/Mythic-Edge/issues/568>

## Contract

`docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md`

## Internal Project Area

Quality / Governance, with CI / Tooling as the affected validation surface.

## Truth Owner

Repo quality governance owns which exact Ruff rules are eligible for blocking
validation. Ruff does not own parser truth, runtime behavior, analytics truth,
security assurance, privacy assurance, release readiness, deploy readiness,
AI truth, or coaching truth.

## Bridge-Code Status

`not_bridge_code`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Status

- Branch: `codex/ruff-next-tranche-567`
- Base: `origin/main`
- `HEAD`: `94d337c635769c214c5beecabef93932033210f3`
- `origin/main`: `94d337c635769c214c5beecabef93932033210f3`
- Branch sync before implementation: `0 0`

Git status before implementation showed the Codex B contract as untracked and
no unrelated dirty files:

```text
## codex/ruff-next-tranche-567...origin/main
?? docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md
```

Git status after implementation:

```text
## codex/ruff-next-tranche-567...origin/main
 M pyproject.toml
?? docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md
?? docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md
```

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md`
- `docs/quality_reports/ruff_advisory/2026-07-01-62bc9c2-ruff-advisory-report.json`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `tests/test_run_repo_checks_script.py`

## Current Behavior Compared To Contract

The repo already had the first two Ruff exact-code tranches selected in
`pyproject.toml`: broad baseline `E`, `F`, and `I`; exact `B` codes; and exact
`DTZ` codes. CI and the local repo-check helper already used the approved lint
scope:

```powershell
py -m ruff check src tests tools
```

Fresh current-base validation passed for the third exact logging/runtime
visibility candidate set before editing. No source cleanup, helper change, CI
change, autofix, unsafe-fix, broad family enablement, or preview mode was
needed.

## Implementation Option Chosen

Implemented the smallest coherent config-only promotion authorized by the
contract: add exactly the selected third-tranche Ruff codes to
`[tool.ruff.lint].select` in `pyproject.toml`.

## Files Changed

- `pyproject.toml`
- `docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md`

The Codex B contract remains untracked and preserved as part of this issue
scope:

- `docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md`

## Exact Sections Changed

### `pyproject.toml`

Updated `[tool.ruff.lint].select` to add exactly:

- `G001`
- `G002`
- `G003`
- `G004`
- `G010`
- `G101`
- `G201`
- `G202`
- `LOG001`
- `LOG002`
- `LOG007`
- `LOG009`
- `LOG014`
- `LOG015`

Preserved the existing selected codes:

- `E`
- `F`
- `I`
- `B006`
- `B008`
- `B012`
- `B023`
- `B904`
- `DTZ002`
- `DTZ003`
- `DTZ004`
- `DTZ006`
- `DTZ011`
- `DTZ012`
- `DTZ901`

### Excluded Code Decision

`LOG004` remains excluded. The contract records that selecting it has no effect
without Ruff preview mode, and preview mode is not authorized for this tranche.

### CI And Local Helper Scope

No changes were made to:

- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `tests/test_run_repo_checks_script.py`

Both CI and the local helper remain scoped to:

```powershell
py -m ruff check src tests tools
```

## Code Changed

Runtime code did not change. This was a Ruff configuration-only validation
surface change.

## Tests Added Or Updated

No tests were added or updated. The existing repo-check helper test already
covers the local lint command scope, and no helper or CI command changed.

## Interface Changes

No runtime, parser, API, workbook, webhook, Apps Script, analytics schema,
SQLite, AI, coaching, environment-variable, or production interface changed.

The only validation contract change is that the existing Ruff command now
enforces the additional selected exact codes through `pyproject.toml`.

## Contracted Area Status

The implementation stayed inside Quality / Governance and CI / Tooling
configuration. No downstream product behavior, parser truth ownership, or
protected runtime surface was touched.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
py -m ruff check src tests tools --select G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015
py -m ruff check src tests tools
py -m pytest -q tests\test_run_repo_checks_script.py
git diff --check
py tools\check_agent_docs.py
@'
docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md
pyproject.toml
docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md
pyproject.toml
docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

Results:

- Branch sync: passed, `0 0`
- Exact candidate Ruff check: passed
- Repo Ruff check: passed
- Repo-check helper test: passed, `1 passed`
- `git diff --check`: passed
- Agent docs check: passed
- Path-scoped protected-surface scan: passed, forbidden `0`, warnings `0`
- Path-scoped secret/private-marker scan: passed, forbidden `0`, warnings `0`

## Protected-Surface Status

Passed: path-scoped protected-surface scan reported forbidden `0`, warnings
`0`. Intended protected surfaces were not touched: parser behavior, parser
state final reconciliation, parser event classes, match/game identity,
deduplication, analytics schema, workbook schema, webhook payload shape, Apps
Script, Google Sheets, output transport, production behavior,
OpenAI/model-provider behavior, AI/coaching, fixtures, corpus status, and
private evidence workflows.

## Secret And Private-Marker Status

Passed: path-scoped secret/private-marker scan reported forbidden `0`,
warnings `0`. No raw Ruff JSON, raw terminal logs, private paths, secrets,
credentials, tokens, webhook URLs, spreadsheet IDs, environment values,
generated artifacts, or local-only files were added.

## Generated Artifact Status

No generated artifacts were created or kept.

## Still Unverified

- GitHub Actions has not run on this branch after the config update.
- Code review has not yet verified that the selected codes are exact-only and
  that broad `G`, broad `LOG`, `ALL`, `LOG004`, and preview mode remain
  excluded.

## Reviewer Focus

Codex E should verify:

- `pyproject.toml` adds exactly the 14 approved codes.
- `LOG004`, broad `G`, broad `LOG`, `ALL`, and preview mode remain excluded.
- Existing `E`, `F`, `I`, `B`, and `DTZ` selections remain intact.
- CI and local helper lint scope remain `src tests tools`.
- No autofix, unsafe-fix, broad cleanup, product behavior, parser behavior,
  protected surface, security/privacy assurance, release readiness, deploy
  readiness, or production readiness claim was introduced.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #618.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/618

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Branch:
codex/ruff-next-tranche-567

Base:
origin/main

Contract:
docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md

Expected review artifact:
docs/contract_test_reports/quality_ruff_third_logging_exact_code_candidate_selection.md

Review goal:
Verify that Codex C implemented the third Ruff logging/runtime visibility exact-code promotion exactly as contracted.

Check:
- Branch freshness against origin/main.
- `pyproject.toml` adds exactly G001, G002, G003, G004, G010, G101, G201, G202, LOG001, LOG002, LOG007, LOG009, LOG014, and LOG015.
- Existing selected E, F, I, B006, B008, B012, B023, B904, DTZ002, DTZ003, DTZ004, DTZ006, DTZ011, DTZ012, and DTZ901 remain intact.
- LOG004 remains excluded.
- Broad G, broad LOG, ALL, preview mode, autofix, unsafe-fix, and broad cleanup were not introduced.
- `.github/workflows/repo-checks.yml` and `tools/run_repo_checks.ps1` still use `py -m ruff check src tests tools`.
- No runtime/product/protected-surface behavior changed.

Validation:
git status --short --branch --untracked-files=all
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
py -m ruff check src tests tools --select G001,G002,G003,G004,G010,G101,G201,G202,LOG001,LOG002,LOG007,LOG009,LOG014,LOG015
py -m ruff check src tests tools
py -m pytest -q tests\test_run_repo_checks_script.py
git diff --check
py tools\check_agent_docs.py

Run path-scoped protected-surface and secret/private-marker scans over changed files.

Do not:
- Add LOG004.
- Enable broad G, broad LOG, ALL, or preview mode.
- Run autofix or unsafe-fix.
- Change CI beyond reviewing the existing lint command.
- Change parser behavior, fixtures, corpus status, analytics truth, AI truth, coaching truth, workbook behavior, Apps Script/Sheets behavior, production behavior, security/privacy assurance, release readiness, or deploy readiness.
- Stage, commit, push, open or merge a PR, close #618, or close tracker #567 unless explicitly asked.

Final report must include findings first, validation evidence, protected-surface status, secret/private-marker status, remaining risk, next recommended role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/618"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/quality_reports/ruff_advisory/2026-07-01-62bc9c2-ruff-advisory-report.json"
  contract_artifact: "docs/contracts/quality_ruff_third_logging_exact_code_candidate_selection.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_third_logging_exact_code_candidate_selection_comparison.md"
  risk_tier: "Medium workflow risk; low runtime risk"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/ruff-next-tranche-567"
  promoted_codes:
    - "G001"
    - "G002"
    - "G003"
    - "G004"
    - "G010"
    - "G101"
    - "G201"
    - "G202"
    - "LOG001"
    - "LOG002"
    - "LOG007"
    - "LOG009"
    - "LOG014"
    - "LOG015"
  excluded_codes:
    - "LOG004"
  validation:
    - "branch sync -> passed, 0 0"
    - "exact candidate Ruff check -> passed"
    - "repo Ruff check -> passed"
    - "repo-check helper test -> passed"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  protected_surfaces_touched: false
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
