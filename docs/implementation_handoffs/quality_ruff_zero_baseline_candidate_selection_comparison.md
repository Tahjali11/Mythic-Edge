# Quality Ruff Zero-Baseline Candidate Selection Comparison

## Issue

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/596>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/567>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

## Contract

- Contract used:
  `docs/contracts/quality_ruff_zero_baseline_candidate_selection.md`
- Source report used:
  `docs/quality_reports/ruff_advisory/2026-06-30-51d5d83-ruff-advisory-report.json`

## Internal Project Area

Quality and validation governance.

## Truth Owner

Ruff owns only static-analysis findings for the exact command, ref or commit,
Ruff version, and scan scope used. Ruff does not own parser truth, corpus
status, fixture authority, release readiness, security assurance, privacy
assurance, analytics truth, AI truth, or coaching truth.

## Bridge-Code Status

`not_bridge_code`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

- Branch: `codex/ruff-zero-baseline-readiness-567`
- Upstream/base: `origin/main`
- Branch sync before implementation: `0 0`
- Initial git status:

```text
## codex/ruff-zero-baseline-readiness-567...origin/main
?? docs/contracts/quality_ruff_zero_baseline_candidate_selection.md
```

The untracked Codex B contract was preserved and included in this comparison
scope.

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/quality_ruff_zero_baseline_candidate_selection.md`
- `docs/quality_reports/ruff_advisory/2026-06-30-51d5d83-ruff-advisory-report.json`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `tools/generate_ruff_advisory_report.py`
- `tools/select_validation.py`
- `tests/test_ruff_advisory_report.py`
- `tests/test_select_validation.py`

GitHub issue context inspected:

- Issue #596
- Tracker #567

## Current Behavior Compared To Contract

The contract selects a first tranche of exact Ruff `DTZ` zero-baseline
candidates:

```text
DTZ002, DTZ003, DTZ004, DTZ006, DTZ011, DTZ012, DTZ901
```

The current repo still has the narrow blocking Ruff configuration:

```toml
[tool.ruff.lint]
select = ["E", "F", "I"]
```

The current GitHub Actions repo check still runs:

```powershell
py -m ruff check src tests tools
```

The current local repo-check helper still runs:

```powershell
py -m ruff check src tests
```

No current committed config promotes the selected `DTZ` exact codes.

The source report was measured at commit
`51d5d8352c10204663d904765a8820bb464a52ac`, while this implementation pass ran
on synced `origin/main` at `5ab26801fa2713537f538c6f43b3bd38d2e5a6f1`.
Therefore the source report remains authoritative historical #588 evidence,
but current-base exact-code validation was required before any next-step
promotion discussion.

The source report classifies the selected and deferred `DTZ` codes as:

| Code | Report count | Report disposition | Protected surface |
| --- | ---: | --- | --- |
| `DTZ002` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ003` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ004` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ006` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ011` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ012` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ901` | 0 | `zero_baseline_candidate` | `none` |
| `DTZ001` | 1 | `advisory` | `none` |
| `DTZ005` | 8 | `protected_surface_review_required` | `parser_truth_surface` |
| `DTZ007` | 1 | `protected_surface_review_required` | `parser_truth_surface` |

## Implementation Option Chosen

Docs-only comparison and validation handoff.

No Ruff promotion was implemented because the Codex B contract and current
handoff explicitly state:

```yaml
blocking_promotion_authorized_by_codex_b: false
```

That means this pass could validate the exact selected codes on the current
base, but it could not edit `pyproject.toml`, CI, or repo-check tooling to make
them blocking.

## What Changed

Added this implementation handoff documenting:

- current Ruff behavior;
- current-base exact-code validation;
- deferral of blocking promotion;
- protected-surface and raw-artifact boundaries;
- reviewer instructions for Codex E.

## Files Changed

- `docs/contracts/quality_ruff_zero_baseline_candidate_selection.md`
  - Existing untracked Codex B contract preserved in scope.
- `docs/implementation_handoffs/quality_ruff_zero_baseline_candidate_selection_comparison.md`
  - New Codex C comparison handoff.

## Code Changed

No runtime code changed.

No parser, analytics, workbook, webhook, Apps Script, AI, coaching, production,
CI, `pyproject.toml`, repo-check helper, fixture, snapshot, or corpus behavior
changed.

## Tests Added Or Updated

No tests were added or updated. The contract did not authorize helper/config
behavior changes, and no Python or frontend behavior changed.

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
# passed; branch was synced and only the untracked contract was present before this handoff

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
docs/contracts/quality_ruff_zero_baseline_candidate_selection.md
docs/implementation_handoffs/quality_ruff_zero_baseline_candidate_selection_comparison.md
'@ | py tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# passed; forbidden 0, warnings 0

@'
docs/contracts/quality_ruff_zero_baseline_candidate_selection.md
docs/implementation_handoffs/quality_ruff_zero_baseline_candidate_selection_comparison.md
'@ | py tools/check_secret_patterns.py --base origin/main --paths-from-stdin
# passed; forbidden 0, warnings 0

direct new-file whitespace/final-newline check for the contract and handoff
# passed

git status --short --branch --untracked-files=all
# two scoped untracked docs files:
# docs/contracts/quality_ruff_zero_baseline_candidate_selection.md
# docs/implementation_handoffs/quality_ruff_zero_baseline_candidate_selection_comparison.md
```

## Still Unverified

- No current-base all-rules Ruff advisory scan was rerun. The contract did not
  authorize rerunning the all-rules advisory measurement.
- No CI or `pyproject.toml` promotion was performed. A later contract or prompt
  must explicitly authorize any blocking promotion.
- Codex E has not yet reviewed whether this docs-only outcome satisfies #596.

## Reviewer Focus

Ask Codex E to verify:

- the exact selected DTZ codes pass on current base;
- existing `E`, `F`, and `I` Ruff behavior remains intact;
- no broad Ruff family, all-rules output, autofix, unsafe-fix, raw output,
  source cleanup, parser behavior, fixture, corpus, CI gate, or protected
  surface change slipped in;
- the handoff accurately defers blocking promotion because it was not
  authorized.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #596.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/596

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Branch:
codex/ruff-zero-baseline-readiness-567

Contract:
docs/contracts/quality_ruff_zero_baseline_candidate_selection.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_zero_baseline_candidate_selection_comparison.md

Review artifact:
docs/contract_test_reports/quality_ruff_zero_baseline_candidate_selection.md

Goal:
Review the #596 Codex C comparison against the contract. Verify that the
selected exact DTZ tranche was validated on current base and that no blocking
promotion, broad Ruff family, autofix, unsafe-fix, raw output, parser behavior,
fixture, corpus, CI gate, or protected-surface change slipped in.

Required checks:
- Confirm branch is codex/ruff-zero-baseline-readiness-567.
- Inspect git status and identify unrelated dirty or untracked files.
- Read AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md,
  docs/codex_module_workflow.md, docs/agent_threads/review.md if present,
  docs/templates, the contract, the source Ruff advisory report, and the
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
- stage, commit, push, open a PR, close issue #596, or close tracker #567.

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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/596"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/quality_reports/ruff_advisory/2026-06-30-51d5d83-ruff-advisory-report.json"
  contract_artifact: "docs/contracts/quality_ruff_zero_baseline_candidate_selection.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_zero_baseline_candidate_selection_comparison.md"
  review_artifact: "docs/contract_test_reports/quality_ruff_zero_baseline_candidate_selection.md"
  risk_tier: "High"
  base_branch: "origin/main"
  branch: "codex/ruff-zero-baseline-readiness-567"
  selected_first_tranche:
    - "DTZ002"
    - "DTZ003"
    - "DTZ004"
    - "DTZ006"
    - "DTZ011"
    - "DTZ012"
    - "DTZ901"
  current_base_exact_code_validation: "passed"
  blocking_promotion_authorized_by_codex_b: false
  blocking_promotion_implemented: false
  ruff_autofix_authorized: false
  ruff_unsafe_fix_authorized: false
  all_rules_rerun_authorized: false
  code_changed: false
  tests_changed: false
  docs_only: true
  forbidden_scope_touched: false
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
    - "Do not edit pyproject.toml or CI unless separately authorized."
    - "Do not promote Ruff to a blocking gate from this C pass."
    - "Do not run Ruff autofix or unsafe-fix."
    - "Do not rerun all-rules Ruff advisory measurement without separate authorization."
    - "Do not change parser behavior, fixtures, corpus status, #388/#381 activation, production behavior, security/privacy assurance, analytics truth, AI truth, or coaching truth."
```
