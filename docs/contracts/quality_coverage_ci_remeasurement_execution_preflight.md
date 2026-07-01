# Quality Coverage CI Remeasurement Execution Preflight Contract

## Module

`quality_coverage_ci_remeasurement_execution_preflight`

Plain English: this contract defines the approval gate that must pass before
any report-only CI-environment coverage remeasurement can run. It does not run
coverage. It decides what must be approved, named, and checked before a later
Codex C thread may collect one advisory measurement.

Coverage is execution evidence for a specific command, commit, environment,
and configuration. It can show that tests exercised code paths. It cannot
prove parser correctness, fixture validity, corpus readiness, security
assurance, privacy assurance, release readiness, deploy readiness, production
readiness, analytics truth, AI truth, or coaching truth.

This contract does not implement code, open a PR, run coverage, change CI,
create temporary workflow files, activate enforcement, set or use
`--cov-fail-under`, change parser behavior, promote fixtures, change corpus
status, run private harvest, or activate #388/#381.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/580
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Active parser evidence tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/577
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/579
- Previous merge commit: `81bad06cfdfdf7298195c3dd9b01170beb04639e`
- Prior policy issue: https://github.com/Tahjali11/Mythic-Edge/issues/575
- Prior policy PR: https://github.com/Tahjali11/Mythic-Edge/pull/576
- Prior local measurement issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/573
- Sibling Wave 1 quality lane:
  https://github.com/Tahjali11/Mythic-Edge/issues/578
- Target artifact:
  `docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md`
- Working branch:
  `codex/quality-coverage-ci-remeasurement-preflight-580`
- Risk tier: High

Observed during contract drafting:

- The primary Mythic Edge checkout was on a gone branch with unrelated
  governance/doc WIP.
- To preserve unrelated local work, this contract was written in a clean
  sibling worktree on branch
  `codex/quality-coverage-ci-remeasurement-preflight-580`.
- This continuation used the existing sibling worktree and preserved its local
  WIP.
- At reconciliation time, the branch was four commits behind current
  `origin/main`, but `HEAD` still contained
  `81bad06cfdfdf7298195c3dd9b01170beb04639e`, the previous merge commit from
  PR #579.
- Issue #580 was open.
- Tracker #566 was open.
- Project roadmap #568 was open.
- Active parser evidence tracker #388 was open and remains inactive.
- Sibling Ruff helper issue #578 is closed via merged PR #581 and remains a
  separate lane that does not authorize coverage execution.
- Current open PRs are unrelated to #580: Dependabot PR #391 and draft public
  path privacy cleanup PR #374.
- The target contract existed as untracked local WIP at the start of this
  continuation and was reconciled instead of overwritten.

Current authorization facts to preserve:

```yaml
implementation_authorized: false
acquisition_mode_approved: false
ci_change_authorized: false
temporary_workflow_creation_authorized: false
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
roadmap. This contract is the execution preflight child after #577. It does
not authorize the remeasurement itself.

## Source Artifacts Inspected

- Issue #580
- Tracker #566
- Project roadmap #568
- Issue #577 and PR #579
- `docs/contracts/quality_coverage_ci_environment_remeasurement.md`
- Issue #575 and PR #576
- `docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md`
- Issue #573 and PR #574
- `docs/implementation_handoffs/quality_coverage_baseline_measurement.md`
- `docs/contracts/quality_coverage_baseline_ratchet_design.md`
- Sibling Ruff issue #578 as Wave 1 context only
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `pyproject.toml`
- `.gitignore`
- Current open PR state

No private Player.log, UTC_Log, app-data, workbook export, SQLite file, runtime
artifact, secret, credential, token, API key, webhook URL, raw coverage output,
coverage XML, coverage database, terminal coverage log, or missing-line report
was read or imported.

## Owning Layer

Primary owning layer: Quality / Governance.

Execution preflight is validation-policy governance. It does not own parser
truth, corpus truth, fixture validity, private-evidence truth, security
assurance, privacy assurance, release readiness, deploy readiness, production
readiness, analytics truth, AI truth, or coaching truth.

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

The preflight is shared validation support. It must not create a reverse-flow
where approval to measure coverage authorizes parser behavior changes, fixture
promotion, corpus status changes, #388 activation, readiness claims, or CI
enforcement.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md`

This contract does not authorize changing:

- `.github/workflows/repo-checks.yml`
- any temporary workflow file
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

Current local helper:

- `tools/run_repo_checks.ps1 -Coverage` runs coverage locally with
  `py -m pytest --cov=src/mythic_edge_parser --cov-report=term-missing tests`;
- it does not enforce `--cov-fail-under`;
- it does not, by itself, prove CI-environment equivalence.

Current coverage configuration:

- `pytest-cov` is available as a dev dependency;
- `pyproject.toml` enables branch coverage;
- coverage source is `src/mythic_edge_parser`;
- coverage report config shows missing lines and skips covered files.

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

Prior contract from #577:

```yaml
ci_remeasurement_execution_authorized: false
ci_change_authorized: false
coverage_enforcement_authorized: false
coverage_fail_under_authorized: false
allowed_future_acquisition_modes:
  - temporary_advisory_ci_workflow_change
  - manual_windows_ci_equivalent_runner
  - existing_ci_artifact_if_available
```

## Problem

The first bad value is running local macOS coverage and calling it
CI-environment evidence. The known baseline was local macOS/Python 3.14.3,
while current CI is Windows/Python 3.13.

The second bad value is changing GitHub Actions, adding a temporary workflow,
or uploading raw coverage artifacts before the approval boundary, raw artifact
handling, cleanup expectation, and report-only status vocabulary are accepted.

The third bad value is treating preflight success, a future measurement, or a
future CI artifact as parser truth, corpus readiness, security/privacy
assurance, release readiness, deploy readiness, production readiness,
analytics truth, AI truth, or coaching truth.

The fourth bad value is treating the #575 85.00% candidate line floor or any
branch coverage number as enforcement before a later explicit enforcement
issue approves it.

## Scope Decision

This contract authorizes only execution preflight planning. A successful
preflight decision is permission to route a later execution issue, not
permission to run coverage inside #580.

Selected path:

```yaml
selected_path: coverage_ci_remeasurement_execution_preflight_contract_only
execution_preflight_contract_defined: true
ci_remeasurement_execution_authorized_by_this_issue: false
ci_workflow_change_authorized_by_this_issue: false
temporary_workflow_creation_authorized_by_this_issue: false
coverage_enforcement_authorized: false
coverage_fail_under_authorized: false
```

Future execution may proceed only after a later issue or user instruction
explicitly approves exactly one acquisition mode and names the required
preflight metadata below.

If no acquisition mode is approved, the lane must park as
`blocked_no_acquisition_mode_approved`.

## Acquisition-Mode Decision Tree

A later execution issue must choose exactly one mode.

Decision tree:

1. If a coverage artifact already exists from a current GitHub Actions run and
   it can be proven to match this contract, use
   `existing_ci_artifact_if_available`.
2. Else, if a human-approved Windows/Python environment can reproduce the
   current CI runner shape without changing GitHub Actions, use
   `manual_windows_ci_equivalent_runner`.
3. Else, if the user explicitly approves a temporary, report-only CI change,
   use `temporary_advisory_ci_workflow_change`.
4. Else, stop and park.

Mode selection must be recorded in a later issue or handoff as:

```yaml
approved_acquisition_mode: "<one mode only>"
approval_source: "<issue/comment/user instruction URL or current chat>"
measured_branch: "<branch or ref>"
measured_commit: "<full commit SHA>"
stale_ref_policy: "refresh_required | stale_ref_explicitly_accepted"
python_version: "3.13 unless current CI changed under separate approval"
runner_label: "<windows-latest or approved equivalent>"
coverage_command_id: "quality_coverage_ci_remeasurement.report_only.v1"
coverage_fail_under_used: false
branch_coverage_status: "advisory_only"
candidate_line_floor_status: "proposal_only"
raw_artifact_location: "<ignored local path or CI job artifact scope>"
sanitized_summary_artifact: "docs/implementation_handoffs/quality_coverage_ci_environment_remeasurement.md"
```

## Required Human Approval Questions

Before any later Codex C may run coverage, the approval record must answer:

1. Which acquisition mode is approved?
2. Which branch and exact commit will be measured?
3. Who or what will run the command: GitHub Actions, a manual Windows runner,
   or an already-existing artifact?
4. If the measurement branch is behind `origin/main`, must it be refreshed
   before measurement, or is the stale ref explicitly accepted as the target?
5. Is any CI workflow edit authorized? If yes, is it temporary, report-only,
   non-enforcing, and scoped to this measurement?
6. Where may raw coverage outputs exist, and when must they be removed,
   ignored, or discarded?
7. Is committing a sanitized summary artifact authorized?
8. What path will hold the sanitized summary?
9. What validation commands must pass before the summary is reviewed?
10. What stop conditions require returning to Codex A/B instead of measuring?
11. Does the approval explicitly preserve no `--cov-fail-under`, no
    enforcement, branch coverage advisory-only, and the 85.00% line floor as
    proposal-only?

If any answer is missing, ambiguous, or contradictory, Codex C must not run
coverage.

## Acquisition Mode 1: Existing CI Artifact If Available

Mode ID: `existing_ci_artifact_if_available`

Use this only when a coverage artifact already exists before the later
execution issue begins.

Required preflight proof:

- artifact came from GitHub Actions for `Tahjali11/Mythic-Edge`;
- artifact was produced from the approved branch and exact commit;
- runner was Windows or otherwise explicitly accepted as CI-equivalent;
- Python version matches current CI or is explicitly accepted;
- command shape is equivalent to the #577 report-only command;
- no `--cov-fail-under` was used;
- artifact is available without adding or changing CI;
- artifact can be summarized without committing raw coverage XML, database,
  terminal logs, HTML, JSON, or file-by-file missing-line output.

Stop if:

- the artifact was produced by a local macOS run;
- the artifact source ref is unclear;
- the command includes enforcement;
- raw output would need to be committed;
- the artifact contains local paths, private markers, raw logs, secrets,
  tokens, API keys, webhook URLs, or generated private artifacts.

## Acquisition Mode 2: Manual Windows CI-Equivalent Runner

Mode ID: `manual_windows_ci_equivalent_runner`

Use this when a human-approved Windows/Python environment can closely match
current GitHub Actions without editing CI.

Required preflight proof:

- clean checkout or clean sibling worktree;
- verified remote is `https://github.com/Tahjali11/Mythic-Edge`;
- exact measured commit is named before running;
- runner is Windows, or the approval explicitly states why it is
  CI-equivalent;
- Python version is `3.13` unless current CI changed separately;
- dependencies are installed with the same shape as CI:
  `py -m pip install -e .[dev]`;
- command uses the #577 report-only command shape;
- raw coverage outputs go under ignored `_review_/` or another approved
  temporary local-only location;
- no raw output is staged or committed;
- sanitized summary path is approved.

Stop if:

- the runner is local macOS or Linux without explicit CI-equivalence approval;
- the checkout is dirty in a way that could affect measurement;
- exact commit cannot be pinned;
- dependency install differs materially from CI;
- the command needs `--cov-fail-under`;
- raw output handling is not approved.

## Acquisition Mode 3: Temporary Advisory CI Workflow Change

Mode ID: `temporary_advisory_ci_workflow_change`

Use this only if the user explicitly approves a temporary, report-only CI
workflow change in a later issue.

Required preflight proof:

- approval explicitly authorizes CI workflow modification;
- exact workflow file or workflow step path is named;
- branch/PR used for the temporary change is named;
- measurement command is non-enforcing;
- the workflow cannot fail because coverage is below the candidate floor;
- `--cov-fail-under` is absent;
- branch coverage remains advisory-only;
- raw artifact upload is either disabled or explicitly approved as temporary
  and non-public beyond the normal CI artifact scope;
- cleanup/removal/parking expectation is recorded before the change is made;
- the temporary change cannot be mistaken for permanent enforcement.

Stop if:

- approval says only "run coverage" but does not authorize CI edits;
- a workflow file would be created without an explicit path and cleanup plan;
- the proposed workflow uploads raw path-rich artifacts publicly;
- the workflow changes required checks or enforcement policy;
- the workflow includes `--cov-fail-under`;
- the workflow changes parser, tests, dependency policy, protected-surface
  gates, release behavior, deploy behavior, secrets, or production behavior.

## Canonical Report-Only Command Shape

The future execution command remains the #577 command shape.

```powershell
$env:COVERAGE_FILE = "_review_/quality_coverage_ci_remeasurement/<run-id>/.coverage"
py -m pytest -q tests `
  --cov=src/mythic_edge_parser `
  --cov-report=term-missing `
  --cov-report="xml:_review_/quality_coverage_ci_remeasurement/<run-id>/coverage.xml"
Remove-Item Env:\COVERAGE_FILE
```

Command invariants:

- install with `py -m pip install -e .[dev]`;
- use Python `3.13` unless current CI changed under separate approval;
- keep branch coverage enabled through `pyproject.toml`;
- use coverage source `src/mythic_edge_parser`;
- do not pass `--cov-fail-under`;
- do not activate enforcement;
- do not treat the 85.00% candidate floor as a CI threshold;
- do not treat branch coverage as enforceable;
- do not commit raw coverage outputs.

## Required Preflight Checklist

Before execution, a future Codex C must verify and record:

- repository remote matches `https://github.com/Tahjali11/Mythic-Edge`;
- working tree or CI ref is clean enough for measurement;
- issue #580, tracker #566, and roadmap #568 are referenced;
- #388 and #381 remain inactive;
- exact branch/ref and commit SHA are pinned;
- stale-ref policy is recorded when the measured branch is behind
  `origin/main`;
- previous #577 contract is present;
- acquisition mode is exactly one of the three allowed modes;
- approval source is recorded;
- runner label and Python version are recorded;
- command shape is recorded;
- `--cov-fail-under` is absent;
- raw artifact location is ignored, temporary, or CI-scoped;
- sanitized summary artifact path is recorded;
- no parser behavior, fixture promotion, corpus status, CI enforcement, or
  readiness/truth/assurance claim is implied.

## Raw Artifact Handling And Retention

Raw coverage artifacts include:

- `.coverage` databases;
- `coverage.xml`;
- coverage JSON;
- coverage HTML directories;
- raw terminal coverage logs;
- file-by-file missing-line reports;
- unredacted command output that includes local paths.

Rules:

- raw artifacts must remain uncommitted;
- local raw artifacts should live under ignored `_review_/` unless a later
  contract approves another ignored path;
- CI raw artifacts may exist only in normal CI job scope or explicitly approved
  temporary artifact retention;
- raw artifacts must not be copied into docs, issues, PR bodies, comments, or
  handoffs;
- raw artifacts must not include private logs, app-data, workbook exports,
  SQLite files, runtime artifacts, secrets, credentials, tokens, API keys,
  webhook URLs, or generated private artifacts;
- if raw artifacts are required to parse aggregate values, the parser must
  extract only aggregate counts and percentages for the public summary.

Retention vocabulary:

- `local_ignored_until_review_complete`
- `ci_artifact_default_retention`
- `discard_after_summary`
- `cleanup_required_before_submission`
- `retention_unsupported`

## Sanitized Summary Artifact

If later authorized, the committed summary should be:

- `docs/implementation_handoffs/quality_coverage_ci_environment_remeasurement.md`

Required fields:

- repository and repository URL;
- issue, tracker, and roadmap;
- acquisition mode;
- approval source;
- measured branch/ref;
- measured commit SHA;
- runner label;
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
- comparison to #575 proposal-only 85.00% line floor;
- explicit branch coverage advisory-only statement;
- raw artifact handling and retention statement;
- validation commands;
- non-claims.

Forbidden summary content:

- raw XML;
- raw terminal logs;
- raw missing-line tables;
- local absolute paths;
- private or live data;
- secrets or credential-like values;
- source patches;
- parser truth, readiness, assurance, release, deploy, production, analytics,
  AI, or coaching claims.

## Status Vocabulary

Allowed preflight statuses:

- `preflight_passed_execution_mode_approved`
- `preflight_blocked_no_acquisition_mode_approved`
- `preflight_blocked_missing_human_approval`
- `preflight_blocked_wrong_runner`
- `preflight_blocked_wrong_python_version`
- `preflight_blocked_wrong_commit`
- `preflight_blocked_stale_ref_policy_missing`
- `preflight_blocked_dirty_checkout`
- `preflight_blocked_unauthorized_ci_change`
- `preflight_blocked_temporary_workflow_missing_cleanup_plan`
- `preflight_blocked_fail_under_requested`
- `preflight_blocked_raw_artifact_policy_missing`
- `preflight_blocked_summary_artifact_not_authorized`
- `preflight_blocked_private_marker_or_secret`
- `preflight_blocked_local_path_leak`
- `preflight_blocked_readiness_or_truth_claim`
- `preflight_inconclusive_needs_reframing`

Forbidden statuses:

- `coverage_run_authorized_by_contract`
- `coverage_enforced`
- `fail_under_enabled`
- `branch_coverage_enforced`
- `parser_truth_confirmed`
- `corpus_ready`
- `security_assured`
- `privacy_assured`
- `release_ready`
- `deploy_ready`
- `production_ready`
- `analytics_truth_confirmed`
- `ai_truth_confirmed`
- `coaching_truth_confirmed`

## Stop Conditions

Stop and route back to Codex A/B if:

- approval does not name one acquisition mode;
- local macOS coverage is proposed as CI evidence;
- the runner, Python version, branch, commit, or command differs from the
  approved mode;
- the branch is behind `origin/main` and no stale-ref policy is recorded;
- coverage output is missing or malformed;
- `--cov-fail-under` is requested or present;
- any CI change is needed but not explicitly approved;
- a temporary workflow lacks a cleanup/removal/parking plan;
- raw coverage output would be committed;
- public summary would include local absolute paths, raw missing-line details,
  private markers, secrets, tokens, credentials, API keys, webhook URLs, raw
  logs, workbook exports, SQLite files, runtime artifacts, or generated
  private artifacts;
- parser behavior change, fixture promotion, corpus status change, #388/#381
  activation, private harvest, enforcement, release/deploy/production
  readiness, security/privacy assurance, analytics truth, AI truth, or
  coaching truth is implied.

## Side Effects

This Codex B scope may write:

- `docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md`

This Codex B scope must not:

- implement code;
- open a PR;
- run coverage;
- change CI;
- create temporary workflow files;
- set or use `--cov-fail-under`;
- activate enforcement;
- commit coverage reports;
- change parser behavior;
- promote fixtures;
- update corpus status;
- activate #388 or #381;
- close issues or trackers.

## Dependency Order For Later Work

1. Issue #580: write this execution preflight contract.
2. Codex E/F/G: review, submit, and merge this contract if accepted.
3. Later Codex A: create or select one exact report-only execution issue and
   name one acquisition mode.
4. Later Codex B, if needed: refine execution details when the approval mode
   is still ambiguous.
5. Later Codex C: run only the approved report-only measurement and commit only
   the sanitized summary artifact, if authorized.
6. Later Codex E/F/G: review and merge the sanitized summary.
7. Later Codex A/B: decide whether the candidate global line floor can move
   toward implementation.
8. Later implementation: enforce only after a separate accepted floor contract
   authorizes CI/local helper changes.

## Compatibility

Existing behavior remains valid:

- GitHub Actions continues to run `py -m pytest -q tests`.
- `tools/run_repo_checks.ps1 -Coverage` remains non-enforcing.
- `pyproject.toml` coverage settings remain unchanged.
- The #575 85.00% line floor remains proposal-only.
- Branch coverage remains advisory-only.
- #388 and #381 remain inactive.
- Sibling Ruff issue #578 remains completed and separate; it does not
  authorize coverage execution.

## Tests And Validation Required

This docs-only contract package requires validation:

```bash
printf '%s\n' docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

Because this is a new untracked file, also validate whitespace with:

```bash
git diff --check --no-index /dev/null docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md
```

Do not run coverage for this Codex B contract, review, or submission package.

Future execution validation, if separately authorized, must include:

- acquisition-mode approval evidence;
- exact commit SHA;
- exact command;
- runner and Python version;
- raw artifact retention evidence;
- coverage command exit code;
- sanitized aggregate summary;
- proof raw outputs are not committed;
- secret/private-marker scan;
- protected-surface scan;
- `git diff --check`;
- explicit no-enforcement and non-claim statements.

## Acceptance Criteria

- The contract defines a preflight gate before report-only CI coverage
  remeasurement.
- The contract names the three allowed acquisition modes.
- The contract requires exactly one approved acquisition mode before execution.
- The contract defines human approval questions.
- The contract defines raw artifact handling and retention expectations.
- The contract defines sanitized summary fields.
- The contract preserves no coverage run, no CI change, no temporary workflow,
  no enforcement, and no `--cov-fail-under` in Codex B.
- The contract keeps the 85.00% candidate line floor proposal-only.
- The contract keeps branch coverage advisory-only.
- The contract preserves #388/#381 inactive.
- The contract makes no readiness, truth, assurance, release, deploy,
  production, analytics, AI, or coaching claims.

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

Codex C execution is not recommended yet because this contract does not approve
an acquisition mode or coverage execution.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer / Contract Tester for issue #580.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/580

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/577

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/579

Previous merge commit:
81bad06cfdfdf7298195c3dd9b01170beb04639e

Contract:
docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md

Goal:
Review the CI coverage remeasurement execution preflight contract. Lead with
findings, if any. Verify that it defines only the approval gate and
acquisition-mode decision tree before any report-only measurement can run.
Confirm it does not authorize code implementation, PR creation, coverage
execution, CI changes, temporary workflow creation, coverage enforcement,
--cov-fail-under, parser behavior changes, fixture promotion, corpus status
changes, #388/#381 activation, or readiness/truth/assurance claims.

Suggested validation:
- Inspect `docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md`.
- Run `printf '%s\n' docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`.
- Run `printf '%s\n' docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`.
- Run `git diff --check`.

Do not implement code.
Do not open a PR.
Do not run coverage.
Do not change CI.
Do not create temporary workflow files.
Do not use or activate `--cov-fail-under`.
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/580"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  active_parser_evidence_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/577"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/579"
  previous_merge_commit: "81bad06cfdfdf7298195c3dd9b01170beb04639e"
  completed_thread: "B"
  next_thread: "E"
  verdict: "coverage_ci_remeasurement_execution_preflight_contract_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/quality-coverage-ci-remeasurement-preflight-580"
  target_artifact: "docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md"
  acquisition_mode_approved: false
  ci_remeasurement_execution_authorized: false
  implementation_authorized: false
  ci_change_authorized: false
  temporary_workflow_creation_authorized: false
  coverage_enforcement_authorized: false
  coverage_fail_under_authorized: false
  parser_behavior_change_authorized: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  validation:
    - "printf '%s\\n' docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "git diff --check"
    - "focused public-Markdown scan for local absolute paths, secret assignment shapes, raw coverage XML, trailing whitespace, non-ASCII text, and final newline"
  stop_conditions:
    - "Do not implement code."
    - "Do not open a PR."
    - "Do not run coverage."
    - "Do not change CI or create temporary workflow files."
    - "Do not use or activate --cov-fail-under."
    - "Do not activate coverage enforcement."
    - "Do not activate #388 or #381."
    - "Do not change parser behavior, promote fixtures, change corpus status, run private harvest, or claim readiness/truth/assurance."
```
