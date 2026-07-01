# Quality Ruff First Exact-Code Dry-Run Comparison

## Issue

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/599>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/567>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/596>

## Contract

- Source contract:
  `docs/contracts/quality_ruff_zero_baseline_candidate_selection.md`
- Source report:
  `docs/quality_reports/ruff_advisory/2026-06-30-51d5d83-ruff-advisory-report.json`

## Internal Project Area

Quality and validation governance.

## Truth Owner

Ruff owns only static-analysis findings for the exact command, ref or commit,
Ruff version, and scan scope used. Ruff does not own parser truth, fixture
authority, corpus status, CI promotion authority, release readiness, security
assurance, privacy assurance, analytics truth, AI truth, or coaching truth.

## Bridge-Code Status

`not_bridge_code`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

- Branch: `codex/ruff-first-exact-code-dry-run-599`
- Base branch: `main`
- Upstream/base ref: `origin/main`
- Starting commit: `8098f24aec369ec15a8ae23387a113d48c781283`
- Branch sync before implementation: `0 0`
- Initial git status:

```text
## codex/ruff-first-exact-code-dry-run-599...origin/main
```

No unrelated dirty or untracked files were present before this handoff.

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/quality_ruff_zero_baseline_candidate_selection.md`
- `docs/implementation_handoffs/quality_ruff_zero_baseline_candidate_selection_comparison.md`
- `docs/contract_test_reports/quality_ruff_zero_baseline_candidate_selection.md`
- `docs/quality_reports/ruff_advisory/2026-06-30-51d5d83-ruff-advisory-report.json`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `tools/generate_ruff_advisory_report.py`
- `tools/select_validation.py`
- `tests/test_ruff_advisory_report.py`
- `tests/test_select_validation.py`

GitHub issue context inspected:

- Issue #599
- Tracker #567
- Project roadmap #568

## Current Behavior Compared To Contract

The #596 source contract selected this exact first tranche:

```text
DTZ002, DTZ003, DTZ004, DTZ006, DTZ011, DTZ012, DTZ901
```

The source report records the selected tranche as zero-finding candidates:

| Code | Report count | Report disposition | Protected surface |
| --- | ---: | --- | --- |
| `DTZ002` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ003` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ004` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ006` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ011` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ012` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ901` | 0 | `zero_baseline_candidate` | `none` |

The source report still defers adjacent `DTZ` rules:

| Code | Report count | Report disposition | Protected surface |
| --- | ---: | --- | --- |
| `DTZ001` | 1 | `advisory` | `none` |
| `DTZ005` | 8 | `protected_surface_review_required` | `parser_truth_surface` |
| `DTZ007` | 1 | `protected_surface_review_required` | `parser_truth_surface` |

Current repo behavior remains advisory-first:

- `pyproject.toml` still has `select = ["E", "F", "I"]`.
- `.github/workflows/repo-checks.yml` still runs
  `py -m ruff check src tests tools`.
- `tools/run_repo_checks.ps1` still runs
  `py -m ruff check src tests`.
- No CI workflow, required status check, Ruff config, or repo-check helper was
  changed.

## Implementation Option Chosen

Advisory-only dry-run and docs handoff.

Issue #599 authorizes current-base exact-code validation and a durable
comparison handoff. It does not authorize a blocking gate, `pyproject.toml`
edit, CI edit, broad Ruff family, autofix, unsafe-fix, all-rules advisory
rerun, or broad cleanup. Therefore this pass intentionally made no runtime,
config, CI, test, parser, fixture, corpus, analytics, AI, coaching, or
production behavior changes.

## What Changed

Added this #599 handoff documenting:

- the exact selected DTZ tranche;
- current-base exact-code validation result;
- current repo Ruff validation result;
- confirmation that existing `E`, `F`, and `I` behavior remains intact;
- confirmation that blocking promotion remains deferred;
- protected-surface and raw-artifact boundaries;
- next recommended Codex E review route.

## Files Changed

- `docs/implementation_handoffs/quality_ruff_first_exact_code_dry_run_comparison.md`

## Code Changed

No runtime code changed.

No parser, analytics, workbook, webhook, Apps Script, AI, coaching, production,
CI, `pyproject.toml`, repo-check helper, fixture, snapshot, or corpus behavior
changed.

## Tests Added Or Updated

No tests were added or updated. The task was validation/reporting only and did
not change helper/config behavior.

## Interface Changes

None.

No function signatures, payload fields, workbook columns, environment
variables, script entrypoints, docs schemas, issue lifecycle rules, PR
lifecycle rules, CI gates, or local validation gates changed.

## Contracted Area Status

The implementation stayed inside the Quality and validation governance area.

Protected surfaces preserved:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity and deduplication;
- fixtures, snapshots, corpus status, and raw evidence promotion;
- #388 and #381 activation state;
- workbook schema;
- webhook payload shape;
- Apps Script and Google Sheets behavior;
- analytics truth;
- AI/coaching/model-provider behavior;
- production behavior;
- secrets, credentials, raw logs, generated data, runtime artifacts, failed
  posts, workbook exports, and local-only artifacts.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
# passed; branch was clean before this handoff

git rev-list --left-right --count HEAD...origin/main
# passed; 0 0

py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901
# passed; All checks passed!

py -m ruff check src tests tools
# passed; All checks passed!
```

```powershell
git diff --check
# passed

py tools/check_agent_docs.py
# passed; errors 0, warnings 0

@'
docs/implementation_handoffs/quality_ruff_first_exact_code_dry_run_comparison.md
'@ | py tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# passed; forbidden 0, warnings 0

@'
docs/implementation_handoffs/quality_ruff_first_exact_code_dry_run_comparison.md
'@ | py tools/check_secret_patterns.py --base origin/main --paths-from-stdin
# passed; forbidden 0, warnings 0

direct new-file whitespace/final-newline check for the handoff
# passed

git status --short --branch --untracked-files=all
# one scoped untracked docs file:
# docs/implementation_handoffs/quality_ruff_first_exact_code_dry_run_comparison.md
```

## Still Unverified

- GitHub CI has not run for this local branch.
- The all-rules Ruff advisory measurement was not rerun because #599 does not
  authorize it.
- Blocking promotion of the selected exact codes remains unimplemented and
  requires a later explicitly authorized issue/contract.

## Reviewer Focus

Ask Codex E to verify:

- only the seven selected exact `DTZ` codes were dry-run validated;
- the existing repo Ruff command still passes;
- `pyproject.toml`, CI workflows, repo-check helpers, and required status
  checks were not changed;
- no broad Ruff family, all-rules output, autofix, unsafe-fix, raw output,
  source cleanup, parser behavior, fixture, corpus, CI gate, or protected
  surface change slipped in;
- this package makes no parser, release, security/privacy, analytics, AI, or
  coaching truth/readiness claims.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #599.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/599

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Branch:
codex/ruff-first-exact-code-dry-run-599

Source contract:
docs/contracts/quality_ruff_zero_baseline_candidate_selection.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_first_exact_code_dry_run_comparison.md

Review artifact:
docs/contract_test_reports/quality_ruff_first_exact_code_dry_run.md

Goal:
Review the #599 advisory-only Ruff exact-code dry-run against issue #599 and
the #596 source contract. Verify that only the selected exact DTZ tranche was
validated, existing repo Ruff behavior remains intact, and no blocking
promotion or protected-surface change slipped in.

Required checks:
- Confirm branch is codex/ruff-first-exact-code-dry-run-599.
- Inspect git status and identify unrelated dirty or untracked files.
- Read AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md,
  docs/codex_module_workflow.md, docs/agent_threads/review.md if present,
  docs/templates, issue #599, tracker #567, the source contract, and the
  implementation handoff.
- Verify current Ruff config remains select = ["E", "F", "I"].
- Verify GitHub Actions and local repo-check Ruff behavior were not changed.
- Rerun or inspect evidence for:
  py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901
  py -m ruff check src tests tools
- Run:
  git diff --check
  py tools/check_agent_docs.py
  path-scoped protected-surface scan over changed files
  path-scoped secret/private-marker scan over changed files

Do not:
- implement fixes;
- edit pyproject.toml or CI;
- promote Ruff to a blocking gate;
- run Ruff autofix or unsafe-fix;
- rerun all-rules Ruff advisory measurement unless explicitly authorized;
- change parser behavior, fixtures, corpus status, #388/#381 activation,
  production behavior, security/privacy assurance, analytics truth, AI truth,
  or coaching truth;
- stage, commit, push, open a PR, close issue #599, or close tracker #567.

Final review must include:
- findings first, ordered by severity;
- contract-test verdict;
- validation run and results;
- protected-surface status;
- raw-artifact status;
- whether blocking promotion remained deferred;
- next recommended role;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/599"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/quality_ruff_zero_baseline_candidate_selection.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_first_exact_code_dry_run_comparison.md"
  review_artifact: "docs/contract_test_reports/quality_ruff_first_exact_code_dry_run.md"
  risk_tier: "High workflow risk; low runtime risk"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/ruff-first-exact-code-dry-run-599"
  selected_first_tranche:
    - "DTZ002"
    - "DTZ003"
    - "DTZ004"
    - "DTZ006"
    - "DTZ011"
    - "DTZ012"
    - "DTZ901"
  current_base_exact_code_validation: "passed"
  existing_ruff_gate_validation: "passed"
  blocking_promotion_implemented: false
  ruff_autofix_used: false
  ruff_unsafe_fix_used: false
  all_rules_rerun_performed: false
  code_changed: false
  tests_changed: false
  docs_only: true
  validation:
    - "git rev-list --left-right --count HEAD...origin/main -> 0 0"
    - "py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901 -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan over changed files -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over changed files -> passed, forbidden 0, warnings 0"
    - "direct new-file whitespace/final-newline check -> passed"
  stop_conditions:
    - "Do not edit pyproject.toml or CI."
    - "Do not promote Ruff to a blocking gate."
    - "Do not enable broad Ruff families."
    - "Do not run Ruff autofix or unsafe-fix."
    - "Do not rerun all-rules Ruff advisory measurement."
    - "Do not change parser behavior, fixtures, corpus status, production behavior, analytics truth, AI truth, or coaching truth."
```
