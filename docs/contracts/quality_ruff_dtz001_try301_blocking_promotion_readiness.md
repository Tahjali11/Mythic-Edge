# Quality Ruff DTZ001 / TRY301 Blocking-Promotion Readiness Contract

## Module

`quality_ruff_dtz001_try301_blocking_promotion_readiness`

Plain English: this contract decides whether the two exact Ruff rule codes
cleaned by #638, `DTZ001` and `TRY301`, are ready for a later
blocking-promotion implementation. Blocking means the normal local or CI Ruff
check would fail if one of the selected exact rule codes appears.

This Codex B pass writes the contract only. It does not run Ruff, edit
`pyproject.toml`, change CI, promote Ruff rules, enable preview mode, run
autofix, run unsafe-fix, clean other findings, or change parser/runtime
behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/643
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/567
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Previous Ruff cleanup issue: https://github.com/Tahjali11/Mythic-Edge/issues/638
- Previous Ruff cleanup PR: https://github.com/Tahjali11/Mythic-Edge/pull/640
- Previous merge commit:
  `3f571ec3abd2800c2df2d6a8e79cec1a0f5896ce`
- Contract artifact:
  `docs/contracts/quality_ruff_dtz001_try301_blocking_promotion_readiness.md`

## Tracker

Tracker #567 remains open for the Ruff ratchet. This issue does not complete
the tracker.

## Risk Tier

Medium workflow risk; low runtime risk if later implementation remains
exact-code/config-only.

The risk is not parser behavior. The risk is accidentally turning a successful
cleanup into broad Ruff promotion, preview-mode behavior, autofix churn, CI
drift, or a false readiness/security claim.

## Owning Layer

Quality / validation tooling.

Ruff owns static-analysis evidence for exact commands, rule codes, Ruff
version, scan scope, and commit/ref. Ruff does not own parser truth, runtime
truth, fixture truth, corpus status, security assurance, privacy assurance,
release readiness, deploy readiness, production readiness, analytics truth, AI
truth, or coaching truth.

## Internal Project Area

Quality / Governance, with shared-support validation-gate impact.

## Truth Owner

`pyproject.toml` owns configured blocking Ruff rule selection once a rule is
promoted. GitHub Actions and `tools/run_repo_checks.ps1` own how the normal
repo lint command is invoked. This contract owns only the readiness decision
for a later exact-code promotion.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
#638 exact-code cleanup evidence
  + current-base drift check
  + current Ruff config and repo-check command shape
  -> readiness contract
  -> later exact-code promotion implementation, if reviewed and authorized
```

Forbidden reverse flow:

- Ruff promotion must not change parser behavior.
- Ruff promotion must not infer security, privacy, parser, release, deploy, or
  production readiness.
- A passing cleanup check must not authorize broad `DTZ`, broad `TRY`,
  preview, `ALL`, autofix, unsafe-fix, or unrelated rule cleanup.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/quality_ruff_dtz001_try301_blocking_promotion_readiness.md`

Future artifacts may be created only by later authorized roles:

- `docs/implementation_handoffs/quality_ruff_dtz001_try301_blocking_promotion_readiness_comparison.md`
- `docs/contract_test_reports/quality_ruff_dtz001_try301_blocking_promotion_readiness.md`

Likely later Codex C implementation files, if Codex E approves this contract
and the owner authorizes implementation:

- `pyproject.toml`
- `docs/implementation_handoffs/quality_ruff_dtz001_try301_blocking_promotion_readiness_comparison.md`

Later Codex C should not need to edit `.github/workflows/repo-checks.yml` or
`tools/run_repo_checks.ps1` because both already use:

```powershell
py -m ruff check src tests tools
```

Codex C must route back to Codex B before changing CI, repo-check scripts,
selector tooling, Ruff helper tools, parser code, tests for unrelated behavior,
or any broad rule-selection policy.

## Source Artifacts Inspected

- Issue #643
- Tracker #567
- Project roadmap #568
- Issue #638
- PR #640
- `docs/contracts/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md`
- `docs/contract_test_reports/quality_ruff_low_churn_exact_code_cleanup_candidate_selection.md`
- `docs/implementation_handoffs/quality_ruff_low_churn_exact_code_cleanup_candidate_selection_comparison.md`
- `docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md`
- `docs/contracts/quality_ruff_zero_baseline_candidate_selection.md`
- `docs/contracts/quality_ruff_stable_runtime_security_watchlist_crosscheck.md`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- current branch state on `origin/main`

## Observed Current Behavior

Current base observed for this contract:

```yaml
branch: "codex/quality-ruff-dtz001-try301-promotion-readiness-643"
base_ref: "origin/main"
head_commit: "f4234ed"
head_summary: "Merge pull request #641 from Tahjali11/codex/security-quality-evidence-bundle-639"
previous_completed_merge_commit: "3f571ec3abd2800c2df2d6a8e79cec1a0f5896ce"
```

Current drift since #640:

```yaml
files_changed_after_638_merge:
  - "docs/contract_test_reports/security_quality_current_evidence_bundle.md"
  - "docs/contracts/security_quality_current_evidence_bundle.md"
  - "docs/implementation_handoffs/security_quality_current_evidence_bundle_comparison.md"
  - "docs/quality_reports/security/cwe_mapped_local_validation_profile/2026-07-02-3f571ec-cwe-profile-advisory-report.json"
  - "docs/quality_reports/security/security_quality_summary/2026-07-02-3f571ec-security-quality-summary.json"
selected_cleanup_source_files_changed_after_638: false
ruff_config_changed_after_638: false
ci_or_repo_check_command_changed_after_638: false
```

#638 closeout evidence records:

```yaml
selected_cleaned_codes:
  - "DTZ001"
  - "TRY301"
deferred_candidate_codes:
  - "PERF403"
  - "RUF022"
  - "RUF059"
ruff_version: "ruff 0.15.12"
selected_code_ruff_result: "passed for DTZ001,TRY301"
focused_tests: "42 passed"
full_ruff: "passed"
pyproject_changed: false
ci_changed: false
promotion_changed: false
preview_mode_changed: false
autofix_used: false
unsafe_fix_used: false
```

Current `pyproject.toml` already blocks earlier exact-code tranches, including
selected `DTZ002`, `DTZ003`, `DTZ004`, `DTZ006`, `DTZ011`, `DTZ012`,
`DTZ901`, selected `B` codes, selected `G` codes, and selected `LOG` codes.
It does not currently select `DTZ001` or `TRY301`.

Current local and CI Ruff command shape:

```powershell
py -m ruff check src tests tools
```

This means an exact-code promotion can live in `pyproject.toml` without
duplicating rule codes in workflow YAML or PowerShell scripts, provided Codex C
revalidates the exact codes before editing config.

## Problem Statement And First Bad Value

The first bad value would be treating #638 cleanup as permission to edit
`pyproject.toml` or CI immediately, without a contract.

Other bad values:

- promoting broad `DTZ` or broad `TRY` instead of exact `DTZ001` and `TRY301`;
- promoting `PERF403`, `RUF022`, `RUF059`, or any deferred rule;
- running preview mode, autofix, or unsafe-fix;
- adding command-line `--select` duplication to CI while also editing config;
- using stale evidence after selected files or Ruff config changed;
- turning Ruff lint success into parser truth, readiness, or assurance.

## Readiness Verdict

Decision:

```yaml
readiness_status: "ready_for_exact_code_blocking_promotion_implementation"
additional_dry_run_issue_required_before_codex_c: false
codex_c_current_base_exact_code_validation_required: true
selected_exact_codes:
  - "DTZ001"
  - "TRY301"
allowed_promotion_shape: "pyproject_exact_codes_only"
ci_change_expected: false
repo_check_script_change_expected: false
pyproject_change_authorized_by_this_contract: false
ruff_blocking_promotion_authorized_by_this_contract: false
```

Rationale:

- #638 cleaned only `DTZ001` and `TRY301`.
- #638 recorded fresh selected-code Ruff pass evidence after cleanup.
- #638 full Ruff passed.
- #638 did not change `pyproject.toml`, CI, preview mode, autofix, unsafe-fix,
  or deferred rules.
- Current `origin/main` is a descendant of #640.
- Later commits after #640 did not touch the cleaned selected-code source,
  test, or tool files, and did not change Ruff configuration or lint command
  shape.
- The first exact-code promotion precedent allows later Codex C to revalidate
  the exact codes on the current base before editing config, rather than
  requiring a separate dry-run issue when the reviewed cleanup evidence is a
  direct ancestor and no relevant drift is observed.

Important: this contract says the lane is ready for a later implementation
thread after review. It does not itself promote the rules.

## Exact-Code Scope

Only these exact rule codes are in scope:

| Code | Meaning in this lane | Promotion-readiness status |
| --- | --- | --- |
| `DTZ001` | Naive `datetime()` construction cleanup was completed in #638 | ready for later exact-code implementation after current-base validation |
| `TRY301` | Raise-in-try cleanup was completed in #638 | ready for later exact-code implementation after current-base validation |

Forbidden under this issue:

- broad `DTZ`;
- broad `TRY`;
- `ALL`;
- preview-mode rules;
- `PERF403`;
- `RUF022`;
- `RUF059`;
- any rule not named `DTZ001` or `TRY301`.

## Allowed Promotion Shape For Later Codex C

If Codex E approves this contract and the user authorizes Codex C
implementation, Codex C should implement only this shape:

1. Revalidate current-base exact-code cleanliness:

   ```powershell
   py -m ruff check src tests tools --select DTZ001,TRY301
   ```

2. If the command passes, edit `pyproject.toml` only to add exact `DTZ001` and
   exact `TRY301` to `[tool.ruff.lint].select`.
3. Preserve existing local and CI command shape:

   ```powershell
   py -m ruff check src tests tools
   ```

4. Do not edit `.github/workflows/repo-checks.yml` or
   `tools/run_repo_checks.ps1` unless Codex C discovers a concrete command
   parity bug and routes back for contract clarification.
5. Do not add `per-file-ignores`, broad ignores, broad family selection,
   preview mode, helper wrappers, autofix, unsafe-fix, or suppression comments.

## Fresh Evidence Requirements

Codex C must stop before editing config unless all are true:

- branch is current with `origin/main`;
- Ruff version is recorded;
- exact selected-code command passes:

  ```powershell
  py -m ruff check src tests tools --select DTZ001,TRY301
  ```

- normal repo Ruff command passes before config edit:

  ```powershell
  py -m ruff check src tests tools
  ```

- no selected-code findings appear in any path;
- no new selected-code finding would require cleanup;
- deferred codes remain out of scope;
- no private artifacts, raw Ruff JSON, local absolute paths, or generated
  local files are committed.

If the exact selected-code command fails, Codex C must not edit
`pyproject.toml`. Route to Codex A or B for a dry-run/cleanup issue depending
on the finding surface.

## Advisory Versus Blocking Boundary

Current status:

- `DTZ001` and `TRY301` are cleaned and promotion-ready by contract.
- They remain non-blocking until a later reviewed implementation adds the
  exact codes to `pyproject.toml`.
- `PERF403`, `RUF022`, `RUF059`, and all other rules remain advisory or
  deferred.

After a future implementation, blocking must mean only:

- normal Ruff validation fails when `DTZ001` or `TRY301` appears.

Blocking must not mean:

- all `DTZ` rules are enforced;
- all `TRY` rules are enforced;
- preview-mode rules are enforced;
- autofix or unsafe-fix is allowed;
- Ruff output proves parser correctness, security, privacy, release,
  deployment, production, analytics, AI, or coaching readiness.

## Local Versus CI Parity

Current parity is acceptable for a pyproject-only promotion:

| Surface | Command |
| --- | --- |
| GitHub Actions | `py -m ruff check src tests tools` |
| `tools/run_repo_checks.ps1` | `py -m ruff check src tests tools` |

Future implementation must preserve this parity. Rule selection should live in
`pyproject.toml`, not duplicated in CI YAML or the PowerShell helper.

If Codex C finds local/CI command drift, it must route back to Codex B unless
the drift is purely documentation/handoff wording.

## Failure Output Contract

Native Ruff output is acceptable for this promotion if it reports:

- repo-relative path;
- line and column;
- exact rule code;
- clear rule message;
- no raw private path;
- no raw Ruff JSON;
- no local-only artifact content;
- no secrets, credentials, tokens, webhook URLs, spreadsheet IDs, raw logs,
  generated SQLite content, failed-post queue artifacts, workbook exports, or
  private payloads.

Codex C must not create custom failure-report tooling for this exact-code
promotion unless native output violates this contract and Codex B/E approve a
new helper.

## Stop Conditions

Stop before implementation if:

- current-base exact-code validation fails;
- implementation would require cleanup before promotion;
- implementation would touch parser runtime/source behavior;
- implementation would touch tests unrelated to promotion mechanics;
- implementation would edit CI, repo-check scripts, or Ruff helper tooling
  without a concrete contract update;
- implementation would promote broad `DTZ`, broad `TRY`, `ALL`, preview
  rules, or any rule other than `DTZ001` and `TRY301`;
- implementation would use autofix, unsafe-fix, fix-only, broad ignores, or
  suppression comments;
- implementation would commit raw Ruff JSON, raw terminal logs, `_review_`
  artifacts, private paths, raw logs, secrets, tokens, credentials, workbook
  exports, generated private artifacts, or private reports.

## Deferred Rules Preserved

The following remain deferred/nonzero and must not be cleaned or promoted in
this lane:

- `PERF403`
- `RUF022`
- `RUF059`

If Codex C or E observes these rules are now clean or different, that is
planning evidence for a later issue only. It must not expand #643.

## Validation Requirements For Later Codex C

Required before config edit:

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
py -m ruff --version
py -m ruff check src tests tools --select DTZ001,TRY301
py -m ruff check src tests tools
```

Required after config edit:

```powershell
py -m ruff check src tests tools --select DTZ001,TRY301
py -m ruff check src tests tools
git diff --check
py tools/check_agent_docs.py
```

Required path-scoped safety checks over changed files:

```powershell
git diff --name-only --diff-filter=ACMRTUXB origin/main...HEAD |
  py tools/check_protected_surfaces.py --base origin/main --paths-from-stdin

git diff --name-only --diff-filter=ACMRTUXB origin/main...HEAD |
  py tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

Codex C should not run broad all-rules measurement, preview measurement,
autofix, unsafe-fix, or cleanup commands.

## Protected Surfaces And Non-Claims

Protected surfaces preserved:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity and deduplication;
- fixtures, snapshots, corpus status, and raw evidence promotion;
- workbook schema;
- webhook payload shape;
- Apps Script and Google Sheets behavior;
- analytics truth;
- AI/coaching/model-provider behavior;
- Line Tracer behavior;
- production behavior;
- secrets, credentials, raw logs, generated data, runtime artifacts,
  failed-post queue artifacts, workbook exports, and local-only artifacts.

Non-claims:

- no parser truth claim;
- no runtime truth claim;
- no security assurance;
- no privacy assurance;
- no release readiness;
- no deploy readiness;
- no production readiness;
- no analytics truth;
- no AI truth;
- no coaching truth.

## Acceptance Criteria

- The readiness status is
  `ready_for_exact_code_blocking_promotion_implementation`.
- The selected exact codes are only `DTZ001` and `TRY301`.
- The contract does not authorize implementation by itself.
- The allowed later implementation shape is pyproject exact-code-only.
- No CI or repo-check script edit is expected.
- Current-base exact-code validation is required before any config edit.
- Deferred rules remain deferred.
- Validation confirms the contract is public-safe and whitespace clean.

## Next Workflow Action

Next role: Codex E reviewer.

Codex E should review whether this contract safely routes to a later exact-code
Codex C implementation without requiring a separate dry-run issue.

Pasteable Codex E prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for issue #643.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/643

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/638

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/640

Artifact to review:
docs/contracts/quality_ruff_dtz001_try301_blocking_promotion_readiness.md

Review focus:
- whether `ready_for_exact_code_blocking_promotion_implementation` is justified;
- whether a separate dry-run issue is unnecessary given #638 evidence and no relevant post-#640 drift;
- whether scope is limited to exact `DTZ001` and `TRY301`;
- whether pyproject-only implementation shape is safe;
- whether CI/repo-check scripts remain unchanged;
- whether all deferred rules and non-claims are preserved.

Protected boundaries:
- Do not implement code.
- Do not run Ruff measurement unless review explicitly needs a read-only check.
- Do not edit pyproject.toml.
- Do not change CI.
- Do not promote any Ruff rule.
- Do not run autofix or unsafe-fix.
- Do not change parser/runtime behavior.

Expected output:
- Findings first, if any.
- Review verdict.
- Recommended next role.
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/643"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/638"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/640"
  completed_thread: "B"
  next_thread: "E"
  verdict: "dtz001_try301_blocking_promotion_readiness_contract_ready_for_review"
  risk_tier: "Medium workflow risk; low runtime risk if kept exact-code/config-only"
  base_branch: "main"
  branch: "codex/quality-ruff-dtz001-try301-promotion-readiness-643"
  target_artifact: "docs/contracts/quality_ruff_dtz001_try301_blocking_promotion_readiness.md"
  readiness_status: "ready_for_exact_code_blocking_promotion_implementation"
  selected_exact_codes:
    - "DTZ001"
    - "TRY301"
  implementation_authorized: false
  ruff_measurement_authorized: false
  pyproject_change_authorized: false
  ci_change_authorized: false
  ruff_blocking_promotion_authorized: false
  ruff_autofix_authorized: false
  ruff_unsafe_fix_authorized: false
  parser_behavior_change_authorized: false
  validation:
    - "python3 tools/check_agent_docs.py"
    - "python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin < target artifact"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "git diff --check"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not run Ruff measurement."
    - "Do not edit pyproject.toml."
    - "Do not change CI or repo-check scripts."
    - "Do not promote DTZ001, TRY301, broad DTZ, broad TRY, ALL, or any Ruff rule."
    - "Do not enable preview mode, autofix, or unsafe-fix."
    - "Do not clean deferred rules."
    - "Do not change parser behavior or parser truth ownership."
```
