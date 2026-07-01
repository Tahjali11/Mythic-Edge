# Quality Ruff Second Bug-Risk Tranche Contract

## Role And Scope

Role performed: Codex B: Module Contract Writer.

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/608

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568

Active separate issue: https://github.com/Tahjali11/Mythic-Edge/issues/605

Branch: `codex/ruff-second-bug-tranche-567`

Base: `origin/main`

Contract artifact: `docs/contracts/quality_ruff_second_bug_risk_tranche.md`

Issue #608 names `docs/contracts/quality_ruff_second_bug_prevention_candidate_selection.md` as the expected artifact, but the current user instruction names `docs/contracts/quality_ruff_second_bug_risk_tranche.md`. This contract follows the current user instruction and treats this file as the authoritative Codex B artifact for issue #608 unless a later workflow thread renames or supersedes it.

This contract defines the second exact-code Ruff bug-risk promotion tranche for Mythic Edge. Ruff is a Python linter, meaning a tool that checks source files for known bug patterns, style issues, and maintainability risks. This tranche is limited to exact Ruff rule codes that currently have zero findings and are intended to prevent bug-prone Python patterns from entering the repo later.

This contract does not implement the promotion, edit Ruff configuration, change CI, run autofix, or change product behavior.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #608
- Tracker #567
- Roadmap #568
- Active separate issue #605
- `docs/contracts/quality_ruff_advisory_zero_baseline_design.md`
- `docs/contracts/quality_ruff_current_advisory_measurement_report.md`
- `docs/contracts/quality_ruff_zero_baseline_candidate_selection.md`
- `docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md`
- `docs/contract_test_reports/quality_ruff_zero_baseline_candidate_selection.md`
- `docs/contract_test_reports/quality_ruff_first_exact_code_dry_run.md`
- `docs/contract_test_reports/quality_ruff_first_exact_code_blocking_promotion.md`
- `docs/quality_reports/ruff_advisory/2026-06-30-51d5d83-ruff-advisory-report.json`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `tests/test_run_repo_checks_script.py`
- `tools/select_validation_mappings.py`

## Observed Current Behavior

- Tracker #567 remains open for earned Ruff rule promotion.
- Issue #608 is open for the second bug-prevention exact-code candidate tranche.
- Issue #605 is open under a different tracker for protected-surface coverage floor readiness. It is not part of this Ruff tranche.
- #601 / PR #606 completed the first exact Ruff blocking promotion for the selected `DTZ` codes.
- `pyproject.toml` currently selects `E`, `F`, `I`, `DTZ002`, `DTZ003`, `DTZ004`, `DTZ006`, `DTZ011`, `DTZ012`, and `DTZ901`.
- `.github/workflows/repo-checks.yml` runs `py -m ruff check src tests tools` and relies on `pyproject.toml` for selected rule codes.
- `tools/run_repo_checks.ps1` also runs `py -m ruff check src tests tools`.
- `tests/test_run_repo_checks_script.py` pins the local helper's lint scope to `src tests tools`.
- The sanitized Ruff advisory report records all five proposed rules as count `0`, disposition `zero_baseline_candidate`, and protected-surface impact `none`.
- Current-base validation passed in this Codex B thread:
  `py -m ruff check src tests tools --select B006,B008,B012,B023,B904`.

## Contract Summary

The second bug-risk Ruff tranche should promote only these exact rule codes after Codex C repeats current-base validation:

- `B006`
- `B008`
- `B012`
- `B023`
- `B904`

The tranche must not enable the broad `B` family. It must not include preview rule `B909`. It must not run Ruff autofix or unsafe-fix. It must not perform broad cleanup. It must not mix in #605 coverage policy work.

If Codex C finds the branch stale, a candidate rule no longer has zero findings, or the repo-check/CI lint scope has drifted, Codex C must stop and produce a comparison handoff instead of forcing promotion.

## Candidate Code Decision

The following exact rule codes are approved as the candidate second bug-risk tranche, subject to fresh Codex C validation:

| Rule | Decision | Reason |
| --- | --- | --- |
| `B006` | Candidate for blocking promotion | Prevents mutable default argument bugs, where one default object can be shared across calls. |
| `B008` | Candidate for blocking promotion | Prevents function calls in default arguments, which run at definition/import time instead of each call. |
| `B012` | Candidate for blocking promotion | Prevents control-flow statements in `finally` blocks that can suppress exceptions or expected returns. |
| `B023` | Candidate for blocking promotion | Prevents late-binding closure bugs where a function captures the changing loop variable instead of the intended value. |
| `B904` | Candidate for blocking promotion | Requires explicit exception chaining inside exception handlers so root causes remain visible. |

These rules are bug-prevention and correctness-oriented. They are not style-only cleanup. Because the current repo has zero findings for them over `src tests tools`, adding them as exact selected codes should prevent future regressions without requiring cleanup churn.

## Excluded Code Decision

`B909` must remain excluded from this tranche.

Reasons:

- Issue #608 identifies `B909` as a preview candidate, not a regular stable promotion candidate.
- The current repo posture does not enable Ruff preview mode.
- A rule that has no practical effect without preview mode is not a useful blocking gate in this tranche.
- Enabling preview mode would be broader than an exact-code promotion and would require a separate contract.

Future reconsideration of `B909` requires a separate issue or contract proving that the rule is stable or that preview-mode adoption is explicitly authorized, safe, and validated.

## Recommended Promotion Posture

This tranche is ready to proceed to Codex C as a blocking-promotion implementation, not another advisory dry-run, if and only if current-base validation still passes.

Codex C may implement the promotion by adding exactly `B006`, `B008`, `B012`, `B023`, and `B904` to the Ruff selected-code list in `pyproject.toml`.

Codex C should avoid changing `.github/workflows/repo-checks.yml` because it already runs `py -m ruff check src tests tools` and should inherit the selected rules from `pyproject.toml`.

Codex C may change `tools/run_repo_checks.ps1` or `tests/test_run_repo_checks_script.py` only if fresh inspection finds they have drifted from the repo-approved lint scope or need a minimal assertion update caused by an authorized implementation detail. No such drift was observed in this Codex B pass.

If current-base validation fails, Codex C must not add the rules to the blocking selection. It should route back to Codex B or Codex A with the first failing rule, command output summary, and branch freshness state.

## Required Guarantees

The implementation must guarantee:

- Only exact rule codes `B006`, `B008`, `B012`, `B023`, and `B904` are added.
- Existing selected rules remain intact.
- No broad `B`, `ALL`, preview mode, autofix, unsafe-fix, or cleanup mode is introduced.
- `B909` remains excluded.
- The blocking Ruff command continues to cover `src tests tools`.
- CI and local repo-check behavior remain aligned.
- #605 protected-surface coverage readiness remains separate.
- No product, parser, analytics, security, privacy, AI, coaching, fixture, corpus, or production-readiness claim is made from this lint promotion.

## Unknowns And Suspected Gaps

Unknowns:

- Whether `origin/main` will advance again before Codex C, E, F, or G handles the tranche.
- Whether a concurrent branch introduces new `B006`, `B008`, `B012`, `B023`, or `B904` findings before merge.
- Whether GitHub CI will surface environment-specific issues not visible in this local contract pass.

Suspected gaps:

- No blocking gap was found in the candidate set during Codex B inspection.
- The main risk is validation freshness, not rule suitability.

## Local And CI Validation Requirements

Codex C must run these before implementation:

```powershell
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
py -m ruff check src tests tools --select B006,B008,B012,B023,B904
py -m ruff check src tests tools
```

Codex C must run these after implementation:

```powershell
py -m ruff check src tests tools --select B006,B008,B012,B023,B904
py -m ruff check src tests tools
py -m pytest -q tests\test_run_repo_checks_script.py
git diff --check
py tools\check_agent_docs.py
```

Codex C must also run path-scoped protected-surface and secret/private-marker scans over the files it changes, using the current base branch:

```powershell
@'
pyproject.toml
tools/run_repo_checks.ps1
tests/test_run_repo_checks_script.py
docs/contracts/quality_ruff_second_bug_risk_tranche.md
docs/implementation_handoffs/quality_ruff_second_bug_risk_tranche_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin

@'
pyproject.toml
tools/run_repo_checks.ps1
tests/test_run_repo_checks_script.py
docs/contracts/quality_ruff_second_bug_risk_tranche.md
docs/implementation_handoffs/quality_ruff_second_bug_risk_tranche_comparison.md
'@ | py tools\check_secret_patterns.py --paths-from-stdin
```

Codex C should omit nonexistent paths from path-scoped scans when a listed file is not changed or not created.

Codex E must confirm:

- The changed Ruff selection contains exactly the existing selected codes plus `B006`, `B008`, `B012`, `B023`, and `B904`.
- No broad `B` family or preview mode was enabled.
- `B909` was not included.
- Local and CI lint scopes still cover `src tests tools`.
- Validation was run on a fresh enough base.
- The implementation did not touch #605 coverage policy.

## Protected-Surface Assessment

This Codex B contract is docs-only and does not touch protected runtime surfaces.

Future Codex C work may touch validation/workflow surfaces such as `pyproject.toml`, `tools/run_repo_checks.ps1`, and `tests/test_run_repo_checks_script.py`. Those are allowed only for the exact Ruff promotion described here.

Forbidden protected-surface changes:

- Parser behavior
- Parser state final reconciliation
- Parser event classes
- Fixture, corpus, schema snapshot, or baseline status
- Analytics truth or SQLite schema
- Security or privacy assurance claims
- Workbook schema
- Webhook payload shape
- Apps Script or Google Sheets behavior
- Output transport or production behavior
- OpenAI, AI, Line Tracer, coaching, hidden-card, archetype, player-mistake, or gameplay advice behavior

## Out Of Scope

- Issue #605 protected-surface coverage floor readiness
- Branch coverage enforcement
- Global coverage floor changes
- Any Ruff autofix or unsafe-fix
- Broad Ruff family promotion
- Preview mode
- `B909`
- All-rules Ruff advisory remeasurement
- Cleanup of existing Ruff findings outside this exact zero-baseline tranche
- CI gate redesign
- Parser, analytics, workbook, webhook, Apps Script, Sheets, OpenAI, AI, coaching, production, fixture, corpus, or privacy behavior changes
- Main-targeting or merge work without explicit user approval

## Acceptance Criteria

Codex C work satisfies this contract when:

- `docs/implementation_handoffs/quality_ruff_second_bug_risk_tranche_comparison.md` exists.
- `pyproject.toml` adds exactly `B006`, `B008`, `B012`, `B023`, and `B904` to the selected Ruff codes.
- Existing selected codes remain present.
- No broad `B` family, preview mode, `B909`, autofix, unsafe-fix, or all-rules rerun is introduced.
- `py -m ruff check src tests tools --select B006,B008,B012,B023,B904` passes.
- `py -m ruff check src tests tools` passes.
- Local repo-check helper scope remains aligned with CI.
- Path-scoped protected-surface and secret/private-marker scans pass or report only contract-authorized validation-surface warnings.
- The final handoff explicitly states that #605 was not changed or resolved by this issue.

## Pasteable Codex C Prompt

Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer.

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

Base:
origin/main

Contract:
docs/contracts/quality_ruff_second_bug_risk_tranche.md

Goal:
Compare the current Ruff configuration, CI lint command, local repo-check helper, and prior Ruff artifacts against the contract. If current-base validation still passes, implement the second bug-risk exact-code Ruff blocking promotion for exactly `B006`, `B008`, `B012`, `B023`, and `B904`.

Before editing:
- Confirm branch and git status.
- Confirm whether the branch is even with `origin/main`.
- Run `py -m ruff check src tests tools --select B006,B008,B012,B023,B904`.
- Run `py -m ruff check src tests tools`.
- Inspect `pyproject.toml`, `.github/workflows/repo-checks.yml`, `tools/run_repo_checks.ps1`, and `tests/test_run_repo_checks_script.py`.

Do:
- Create `docs/implementation_handoffs/quality_ruff_second_bug_risk_tranche_comparison.md`.
- If validation is fresh and passing, add exactly `B006`, `B008`, `B012`, `B023`, and `B904` to the Ruff selected-code list in `pyproject.toml`.
- Preserve existing selected codes.
- Keep CI and local lint scope at `src tests tools`.
- Update local repo-check helper tests only if a scoped implementation change requires it.
- State clearly that issue #605 coverage work remains separate.

Do not:
- Add broad `B`.
- Add `B909`.
- Enable preview mode.
- Run Ruff autofix or unsafe-fix.
- Rerun all-rules Ruff advisory measurement.
- Change CI unless inspection proves the existing CI lint command has drifted from the repo-approved path scope.
- Change coverage policy, protected-surface coverage policy, parser behavior, fixtures, corpus status, production behavior, security/privacy assurance, analytics truth, AI truth, or coaching truth.
- Target main directly without explicit user approval.

Validation:
```powershell
py -m ruff check src tests tools --select B006,B008,B012,B023,B904
py -m ruff check src tests tools
py -m pytest -q tests\test_run_repo_checks_script.py
git diff --check
py tools\check_agent_docs.py
```

Also run path-scoped protected-surface and secret/private-marker scans over changed files.

Final handoff must include:
- role performed
- issue/tracker/roadmap
- contract artifact used
- implementation handoff produced
- files changed
- candidate codes promoted
- excluded code decision for `B909`
- validation results
- protected-surface status
- secret/private-marker status
- confirmation that #605 was not modified
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/608"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  active_separate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/605"
  completed_thread: "B"
  next_thread: "C"
  source_artifacts:
    - "GitHub issue #608"
    - "docs/quality_reports/ruff_advisory/2026-06-30-51d5d83-ruff-advisory-report.json"
    - "docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md"
    - "docs/contract_test_reports/quality_ruff_first_exact_code_blocking_promotion.md"
  contract_artifact: "docs/contracts/quality_ruff_second_bug_risk_tranche.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_second_bug_risk_tranche_comparison.md"
  risk_tier: "Medium-High workflow risk; low runtime risk"
  branch: "codex/ruff-second-bug-tranche-567"
  base: "origin/main"
  target_branch: "main_after_explicit_user_approval"
  candidate_codes:
    - "B006"
    - "B008"
    - "B012"
    - "B023"
    - "B904"
  excluded_codes:
    - "B909"
  recommended_promotion_posture: "blocking exact-code promotion after fresh Codex C validation"
  validation:
    - "git status --short --branch --untracked-files=all -> clean/even with origin/main before contract creation"
    - "py -m ruff check src tests tools --select B006,B008,B012,B023,B904 -> passed"
  stop_conditions:
    - "Do not include issue #605 coverage work."
    - "Do not add broad B, preview mode, or B909."
    - "Do not run Ruff autofix or unsafe-fix."
    - "Do not rerun all-rules Ruff advisory measurement."
    - "Do not change parser behavior, fixtures, corpus status, production behavior, security/privacy assurance, analytics truth, AI truth, or coaching truth."
    - "Do not target main directly without explicit user approval."
```
