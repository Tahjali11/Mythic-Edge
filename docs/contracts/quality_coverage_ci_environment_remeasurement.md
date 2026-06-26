# Quality Coverage CI-Environment Remeasurement Contract

## Module

`quality_coverage_ci_environment_remeasurement`

Plain English: this contract defines how Mythic Edge should later collect one
advisory coverage measurement in a CI-equivalent environment before any
coverage enforcement or `--cov-fail-under` gate is considered.

Coverage is execution evidence for a specific command, commit, environment,
and configuration. It can show that tests exercised code paths. It cannot
prove parser correctness, fixture validity, corpus readiness, security
assurance, privacy assurance, release readiness, deploy readiness, production
readiness, analytics truth, AI truth, or coaching truth.

This contract does not run coverage, change CI, add a workflow step, activate
enforcement, set or use `--cov-fail-under`, change parser behavior, promote
fixtures, update corpus metadata, or activate #388/#381.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/577
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Active parser evidence tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/575
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/576
- Previous merge commit: `bf6a58b1b345a8d7f83d711a3cf291821a5c3599`
- Prior measurement issue: https://github.com/Tahjali11/Mythic-Edge/issues/573
- Prior measurement PR: https://github.com/Tahjali11/Mythic-Edge/pull/574
- Target artifact:
  `docs/contracts/quality_coverage_ci_environment_remeasurement.md`
- Working branch: `codex/quality-coverage-ci-remeasurement-577`
- Risk tier: High

Observed during contract drafting:

- The primary Mythic Edge checkout was on a gone branch with unrelated
  governance/doc WIP.
- To preserve unrelated local work, this contract was written in a clean
  sibling worktree on branch `codex/quality-coverage-ci-remeasurement-577`.
- The worktree was created from `origin/main`.
- `origin/main` includes previous merge commit
  `bf6a58b1b345a8d7f83d711a3cf291821a5c3599`.
- Issue #577 is open.
- Tracker #566 is open.
- Project roadmap #568 is open.
- Active parser evidence tracker #388 is open and remains inactive.
- PR #571 for the parallel Ruff advisory zero-baseline lane under tracker #567
  has merged to `origin/main` and is not a blocker for this contract.

Current authorization facts to preserve:

```yaml
implementation_authorized: false
ci_change_authorized: false
coverage_measurement_execution_authorized: false
coverage_report_commit_authorized: false
coverage_enforcement_authorized: false
coverage_fail_under_authorized: false
parser_behavior_change_authorized: false
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
security_assurance_claim_authorized: false
privacy_assurance_claim_authorized: false
release_readiness_claim_authorized: false
```

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/566

Tracker #566 owns the coverage ratchet and quality-threshold enforcement
roadmap. This contract defines the advisory CI-environment remeasurement
boundary after #575 and before any future enforcement child.

## Source Artifacts Inspected

- Issue #577
- Tracker #566
- Project roadmap #568
- Issue #575 and PR #576
- `docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md`
- Issue #573 and PR #574
- `docs/implementation_handoffs/quality_coverage_baseline_measurement.md`
- `docs/contracts/quality_coverage_baseline_ratchet_design.md`
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `pyproject.toml`
- Current open PR state and the merged PR #571 parallel Ruff Phase 0 lane

No private Player.log, UTC_Log, app-data, workbook export, SQLite file, runtime
artifact, secret, credential, token, API key, webhook URL, raw coverage output,
coverage XML, coverage database, terminal coverage log, or missing-line report
was read or imported.

## Owning Layer

Primary owning layer: Quality / Governance.

CI-environment remeasurement is validation-policy evidence. It does not own
parser truth, corpus truth, fixture validity, security assurance, privacy
assurance, release readiness, deploy readiness, production readiness, analytics
truth, AI truth, or coaching truth.

## Internal Project Area

Quality / Governance.

This contract reads CI and coverage tooling context, but it does not modify
Parser, Corpus / Provenance, Local App / UI, Workbook / Transport, Analytics,
or Future AI Integration behavior.

## Truth Owner

Truth owner for this contract: repo quality governance.

Coverage tools own only measured coverage for the exact command, commit,
branch, runner, Python version, dependency set, and coverage configuration.
The parser/state layer remains the truth owner for parser behavior and
parser-owned facts. Corpus / Provenance remains the truth owner for fixture
and corpus evidence.

## Bridge-Code Status

`shared_support`

CI-environment remeasurement is shared validation support. It must not create
a reverse-flow where a coverage percentage authorizes parser behavior changes,
fixture promotion, corpus status changes, #388 activation, or readiness
claims.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/quality_coverage_ci_environment_remeasurement.md`

This contract does not authorize changing:

- `.github/workflows/repo-checks.yml`
- `pyproject.toml`
- `tools/run_repo_checks.ps1`
- source files under `src/`
- tests under `tests/`
- future protected-surface coverage checkers
- parser, corpus, workbook, webhook, Apps Script, analytics, AI, or runtime
  behavior

## Observed Current Behavior

Current GitHub Actions repo checks:

- run on `windows-latest`;
- use `actions/setup-python@v5` with Python `3.13`;
- install the package with dev dependencies;
- run `py -m pytest -q tests`;
- run the protected-surface gate for pull requests;
- run `py -m ruff check src tests tools`;
- do not run coverage;
- do not enforce coverage.

Current coverage configuration:

- `pytest-cov` is available as a dev dependency.
- `pyproject.toml` enables branch coverage.
- coverage source is `src/mythic_edge_parser`.
- coverage report config shows missing lines and skips covered files.

Current local helper:

- `tools/run_repo_checks.ps1 -Coverage` runs coverage locally with
  `py -m pytest --cov=src/mythic_edge_parser --cov-report=term-missing tests`.
- It does not enforce `--cov-fail-under`.

Prior advisory local baseline from #573:

```yaml
measured_commit: "f31923ec2b0da629be3eeb8e7971b21aa57fe9fc"
sanitized_environment_label: "local-macos-python-3.14.3-arm64"
tests_passed: 1949
line_coverage_percent: 87.56
branch_coverage_percent: 74.87
coverage_fail_under_used: false
```

Prior policy from #575:

```yaml
candidate_line_floor_percent: 85.00
candidate_line_floor_status: proposal_only
branch_coverage_status: "advisory_only"
ci_remeasurement_required_before_enforcement: true
coverage_enforcement_authorized: false
coverage_fail_under_authorized: false
```

## Problem

The first bad value is treating a local macOS coverage result as directly
enforceable in GitHub Actions. Current CI uses a Windows runner and Python
3.13, so environment variance must be measured before a future threshold can
be accepted.

The second bad value is changing CI or adding `--cov-fail-under` before the
remeasurement packet shape is defined. A remeasurement should produce advisory
evidence first, not a blocking gate.

The third bad value is committing raw coverage artifacts or terminal logs.
Coverage outputs may include local path information, file-by-file missing-line
details, and environment information that should not be copied into public
artifacts without sanitization.

The fourth bad value is using a CI coverage result to claim parser truth,
corpus readiness, fixture validity, security/privacy assurance, or release
readiness. Coverage remains execution evidence only.

## Scope Decision

This contract authorizes only the contract boundary for a future
CI-environment remeasurement.

Selected path:

```yaml
selected_path: advisory_ci_environment_remeasurement_contract_only
ci_remeasurement_execution_authorized_by_this_issue: false
ci_workflow_change_authorized_by_this_issue: false
coverage_enforcement_authorized: false
coverage_fail_under_authorized: false
```

The narrowest safe later path is a separate child issue that explicitly
authorizes one advisory CI-environment measurement packet. That later issue
must choose one of these acquisition modes:

- `temporary_advisory_ci_workflow_change`: a reviewed, temporary or
  non-enforcing CI change that runs coverage and records only sanitized
  aggregate evidence;
- `manual_windows_ci_equivalent_runner`: a clean Windows/Python 3.13 runner
  that matches the current CI command shape closely enough to be reviewed as
  CI-equivalent;
- `existing_ci_artifact_if_available`: only if a future workflow already
  produces coverage artifacts before the later issue starts.

If none of those modes is explicitly authorized, Codex C must not run the
remeasurement.

## CI-Environment Measurement Command Shape

The future CI-environment command must be advisory and non-enforcing.

Canonical Windows/GitHub Actions command shape:

```powershell
$env:COVERAGE_FILE = "_review_/quality_coverage_ci_remeasurement/<run-id>/.coverage"
py -m pytest -q tests `
  --cov=src/mythic_edge_parser `
  --cov-report=term-missing `
  --cov-report="xml:_review_/quality_coverage_ci_remeasurement/<run-id>/coverage.xml"
Remove-Item Env:\COVERAGE_FILE
```

Command invariants:

- Use the same package install path as repo checks: `py -m pip install -e .[dev]`.
- Use Python `3.13` unless current CI has changed before the later issue.
- Use `windows-latest` or a documented CI-equivalent Windows environment.
- Keep branch coverage enabled through `pyproject.toml`.
- Use coverage source `src/mythic_edge_parser`.
- Do not pass `--cov-fail-under`.
- Do not publish raw coverage reports as committed artifacts.
- Store raw outputs under ignored `_review_/` or CI job artifacts that are not
  committed to the repo.

If a future authorized CI workflow cannot write `_review_/`, it must write to
a CI workspace path that is not committed and must still publish only a
sanitized aggregate summary.

## Public-Safe Remeasurement Summary Shape

A later Codex C report may commit only a sanitized summary artifact, likely:

- `docs/implementation_handoffs/quality_coverage_ci_environment_remeasurement.md`

Required public-safe fields:

- repository;
- issue and tracker;
- measured commit SHA;
- base branch or source ref;
- run ID;
- acquisition mode;
- CI runner label or CI-equivalent environment label;
- Python version;
- command ID;
- command shape without local absolute paths;
- coverage command exit code;
- tests passed count;
- line coverage percent;
- covered statements;
- total statements;
- missing statements;
- branch coverage percent;
- covered branches;
- total branches;
- missing branches;
- measured file count, if available;
- measured package count, if available;
- comparison to #573 local advisory baseline;
- comparison to #575 candidate 85.00% line floor;
- branch coverage advisory-only statement;
- raw output handling statement;
- non-claims.

Forbidden committed content:

- `.coverage` databases;
- raw `coverage.xml`;
- coverage JSON;
- coverage HTML directories;
- raw terminal coverage logs;
- local absolute paths;
- unredacted file-by-file missing-line reports;
- private Player.log or UTC_Log content;
- app-data, workbook exports, SQLite files, runtime artifacts, secrets,
  credentials, tokens, API keys, webhook URLs, or generated private artifacts.

## Comparison Rules

The future CI-environment report must compare CI-environment values to the
local #573 baseline without treating the comparison as enforcement.

Local advisory baseline:

```yaml
line_coverage_percent: 87.56
branch_coverage_percent: 74.87
tests_passed: 1949
```

Candidate floor policy from #575:

```yaml
candidate_line_floor_percent: 85.00
candidate_line_floor_status: proposal_only
branch_coverage_status: "advisory_only"
```

Comparison vocabulary:

- `ci_remeasurement_matches_local_band`: CI line coverage is at least 87.00%.
- `ci_remeasurement_margin_review_required`: CI line coverage is at least
  85.00% and below 87.00%.
- `ci_remeasurement_below_candidate_floor`: CI line coverage is below 85.00%.
- `ci_remeasurement_inconclusive`: coverage data is missing, malformed,
  partial, or from the wrong command/environment.
- `ci_remeasurement_blocked`: the run cannot proceed without changing
  authorization, touching protected surfaces, or exposing raw/private data.

Interpretation rules:

- If CI line coverage is at least 87.00%, later Codex A/B may consider a
  global line-floor implementation child using the 85.00% candidate.
- If CI line coverage is 85.00% to 86.99%, later Codex A/B must decide whether
  the margin is safe before any enforcement issue proceeds.
- If CI line coverage is below 85.00%, enforcement must remain blocked and the
  discrepancy must be treated as environment/drift evidence.
- Branch coverage must remain advisory-only regardless of the CI value unless
  a later branch-floor contract explicitly changes that status.

## Remeasurement Status Vocabulary

Allowed future report statuses:

- `passed_advisory_ci_remeasurement`
- `passed_with_margin_review_required`
- `blocked_below_candidate_floor`
- `blocked_missing_coverage_output`
- `blocked_malformed_coverage_output`
- `blocked_wrong_commit_or_command`
- `blocked_unsafe_raw_artifact`
- `blocked_private_marker_or_secret`
- `blocked_authorization_gap`
- `inconclusive_environment_mismatch`
- `inconclusive_partial_data`

Forbidden statuses:

- `coverage_enforced`
- `fail_under_enabled`
- `parser_truth_confirmed`
- `corpus_ready`
- `security_assured`
- `privacy_assured`
- `release_ready`
- `production_ready`

## Future Implementation Boundaries

Any future implementation or execution issue must name:

- acquisition mode;
- exact branch and commit;
- exact command;
- runner and Python version;
- raw artifact location and retention behavior;
- committed summary artifact path;
- validation commands;
- stop conditions;
- whether a temporary CI workflow change is authorized.

If the future issue authorizes a temporary advisory CI workflow change, that
change must be:

- non-enforcing;
- reviewable as a temporary measurement path;
- removed, parked, or explicitly converted before any enforcement work;
- unable to fail CI because coverage is below a candidate floor;
- unable to upload raw coverage artifacts publicly unless a later contract
  explicitly permits sanitized artifact publication.

This contract does not authorize that future CI change.

## Error Behavior

Future remeasurement must fail closed when:

- coverage output is missing;
- coverage XML is malformed;
- coverage output was produced from the wrong commit or branch;
- coverage command differs materially from the approved command shape;
- Python version or runner does not match the authorized environment;
- raw coverage output would be committed;
- public summary contains local absolute paths;
- public summary contains private markers, secrets, tokens, credentials, API
  keys, webhook URLs, raw logs, workbook exports, or generated private
  artifacts;
- `--cov-fail-under` is present;
- branch coverage enforcement is attempted;
- CI or local helper edits are needed but not authorized;
- #388/#381 activation, fixture promotion, corpus status change, or parser
  behavior change is implied;
- readiness, truth, or assurance claims appear.

For this contract-only issue, failure behavior is advisory: record the problem
and stop. Do not patch CI, run coverage, or reinterpret the contract.

## Side Effects

This Codex B scope may write:

- `docs/contracts/quality_coverage_ci_environment_remeasurement.md`

This Codex B scope must not:

- implement code;
- open a PR;
- run coverage;
- change CI;
- set or use `--cov-fail-under`;
- activate enforcement;
- commit raw coverage reports;
- change parser behavior;
- promote fixtures;
- update corpus metadata;
- activate #388 or #381;
- close issues or trackers.

## Dependency Order For Later Work

1. Issue #577: write this CI-environment remeasurement contract.
2. Later Codex E/F/G: review, submit, and merge this contract.
3. Later Codex A: create the exact advisory remeasurement execution issue.
4. Later Codex B: define execution details if the execution issue needs more
   specificity.
5. Later Codex C: run only the authorized advisory measurement and commit only
   the sanitized summary artifact.
6. Later Codex E/F/G: review and merge the advisory remeasurement report.
7. Later Codex A/B: decide whether global line-floor implementation can proceed.
8. Later Codex C/E/F/G: implement enforcement only after a separate accepted
   floor contract authorizes CI/local helper changes.

## Compatibility

Existing behavior must remain valid:

- GitHub Actions continues to run `py -m pytest -q tests` until a later issue
  authorizes a CI coverage step.
- `tools/run_repo_checks.ps1 -Coverage` remains non-enforcing.
- `pyproject.toml` coverage configuration remains advisory configuration.
- The #575 85.00% line floor remains proposal-only.
- Branch coverage remains advisory-only.
- #388 and #381 remain inactive.

## Tests And Validation Required

This docs-only contract package requires validation:

```bash
printf '%s\n' docs/contracts/quality_coverage_ci_environment_remeasurement.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/quality_coverage_ci_environment_remeasurement.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

Because this is a new untracked file, also validate whitespace with:

```bash
git diff --check --no-index /dev/null docs/contracts/quality_coverage_ci_environment_remeasurement.md
```

Do not run coverage for this Codex B contract, review, or submission package.

Future execution validation, if separately authorized, must include:

- proof of clean checkout or CI ref;
- exact commit SHA;
- exact command;
- runner and Python version;
- coverage command exit code;
- sanitized aggregate summary;
- proof raw outputs are not committed;
- secret/private-marker scan;
- protected-surface scan;
- `git diff --check`;
- explicit no-enforcement and non-claim statements.

## Acceptance Criteria

- The contract defines the CI-environment remeasurement purpose and non-claims.
- The contract defines a future advisory, non-enforcing command shape.
- The contract separates local baseline, CI remeasurement evidence, candidate
  threshold policy, and future enforcement.
- The contract preserves the 85.00% candidate line floor as proposal-only.
- The contract keeps branch coverage advisory-only.
- The contract defines public-safe summary fields and forbidden raw artifacts.
- The contract defines comparison and status vocabulary for future reports.
- The contract routes any CI change, coverage run, or enforcement to later
  explicit issues only.
- The contract preserves #388/#381 inactive.
- The contract makes no parser truth, corpus-readiness, release-readiness,
  security/privacy-assurance, analytics-truth, AI-truth, or coaching-truth
  claims.

## Non-Claims

This contract does not claim:

- parser truth;
- parser behavior readiness;
- tracker #388 activation readiness;
- issue #381 activation readiness;
- fixture promotion readiness;
- corpus readiness;
- private smoke success;
- security assurance;
- privacy assurance;
- release readiness;
- deploy readiness;
- production readiness;
- analytics truth;
- AI truth;
- coaching truth.

## Recommended Next Role

Recommended next role: Codex E review.

Codex C implementation is not recommended yet because execution and CI changes
remain unauthorized.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer / Contract Tester for issue #577.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/577

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/575

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/576

Previous merge commit:
bf6a58b1b345a8d7f83d711a3cf291821a5c3599

Contract:
docs/contracts/quality_coverage_ci_environment_remeasurement.md

Goal:
Review the CI-environment coverage remeasurement contract. Lead with findings,
if any. Verify that the contract defines only an advisory future
remeasurement boundary, does not authorize coverage execution, CI changes,
enforcement, or --cov-fail-under, preserves the 85.00% line floor as
proposal-only, keeps branch coverage advisory-only, and preserves all
parser/corpus/readiness/security/privacy non-claims.

Suggested validation:
- Inspect `docs/contracts/quality_coverage_ci_environment_remeasurement.md`.
- Run `printf '%s\n' docs/contracts/quality_coverage_ci_environment_remeasurement.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`.
- Run `printf '%s\n' docs/contracts/quality_coverage_ci_environment_remeasurement.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`.
- Run `git diff --check`.

Do not implement code.
Do not change CI.
Do not run coverage.
Do not use or activate `--cov-fail-under`.
Do not commit raw coverage outputs, terminal logs, local absolute paths, or
missing-line reports.
Do not activate #388 or #381.
Do not claim parser truth/readiness, corpus readiness, release readiness,
deploy readiness, production readiness, security assurance, privacy assurance,
analytics truth, AI truth, or coaching truth.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/577"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/575"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/576"
  previous_merge_commit: "bf6a58b1b345a8d7f83d711a3cf291821a5c3599"
  completed_thread: "B"
  next_thread: "E"
  verdict: "coverage_ci_environment_remeasurement_contract_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/quality-coverage-ci-remeasurement-577"
  target_artifact: "docs/contracts/quality_coverage_ci_environment_remeasurement.md"
  advisory_line_baseline_percent: 87.56
  candidate_line_floor_percent: 85.00
  advisory_branch_baseline_percent: 74.87
  branch_coverage_status: "advisory_only"
  ci_remeasurement_contract_defined: true
  ci_remeasurement_execution_authorized: false
  implementation_authorized: false
  ci_change_authorized: false
  coverage_enforcement_authorized: false
  coverage_fail_under_authorized: false
  parser_behavior_change_authorized: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  validation:
    - "printf '%s\\n' docs/contracts/quality_coverage_ci_environment_remeasurement.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/quality_coverage_ci_environment_remeasurement.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "git diff --check"
  stop_conditions:
    - "Do not implement code."
    - "Do not change CI."
    - "Do not run coverage."
    - "Do not use or activate --cov-fail-under."
    - "Do not commit raw coverage outputs, terminal logs, local absolute paths, or missing-line reports."
    - "Do not activate #388 or #381."
    - "Do not change parser behavior, promote fixtures, change corpus status, run private harvest, or claim readiness/truth/assurance."
```
