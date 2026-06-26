# Quality Coverage Baseline Interpretation And Threshold Policy Contract

## Module

`quality_coverage_baseline_interpretation_threshold_policy`

Plain English: this contract interprets the first advisory Python coverage
baseline from issue #573 and defines a candidate threshold policy for later
review. It turns a measurement into a policy proposal, not a gate.

Coverage is an execution signal: it shows which code paths ran during tests for
a specific command, commit, environment, and configuration. Coverage does not
prove parser truth, fixture validity, corpus readiness, security assurance,
privacy assurance, release readiness, deploy readiness, production behavior,
analytics truth, AI truth, or coaching truth.

This contract does not implement code, change CI, activate coverage
enforcement, set `--cov-fail-under`, change parser behavior, promote fixtures,
update corpus metadata, rerun coverage, or commit coverage outputs.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/575
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Active parser evidence tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/573
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/574
- Previous merge commit: `626bd26318de4b77ece9759582ee4c5939ae6291`
- Prior design issue: https://github.com/Tahjali11/Mythic-Edge/issues/569
- Prior design PR: https://github.com/Tahjali11/Mythic-Edge/pull/572
- Target artifact:
  `docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md`
- Working branch: `codex/quality-coverage-threshold-policy-575`
- Risk tier: High

Observed during contract drafting:

- The primary Mythic Edge checkout was on a gone branch with unrelated
  governance/doc WIP.
- To preserve unrelated local work, this contract was written in a clean
  sibling worktree on branch `codex/quality-coverage-threshold-policy-575`.
- The worktree was created from `origin/main`.
- `origin/main` includes previous merge commit
  `626bd26318de4b77ece9759582ee4c5939ae6291`.
- Issue #575 is open.
- Tracker #566 is open.
- Project roadmap #568 is open.
- Active parser evidence tracker #388 is open and remains inactive for this
  contract.

Current authorization facts to preserve:

```yaml
implementation_authorized: false
ci_change_authorized: false
coverage_enforcement_authorized: false
coverage_fail_under_authorized: false
coverage_measurement_execution_authorized: false
coverage_report_commit_authorized: false
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

Tracker #566 owns the long-term coverage ratchet and quality-threshold
enforcement roadmap. This issue is the interpretation step after measurement
and before any implementation or enforcement.

## Source Artifacts Inspected

- Issue #575
- Tracker #566
- Project roadmap #568
- Active parser evidence tracker #388
- Issue #573 and PR #574
- Issue #569 and PR #572
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- `docs/contracts/quality_coverage_baseline_ratchet_design.md`
- `docs/contract_test_reports/quality_coverage_baseline_ratchet_design.md`
- `docs/implementation_handoffs/quality_coverage_baseline_measurement.md`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `docs/contracts/parser_evidence_pipeline_activation_contract.md`
- `docs/contracts/parser_evidence_bounded_local_dry_run.md`

No private Player.log, UTC_Log, app-data, workbook export, SQLite file, runtime
artifact, secret, credential, token, API key, webhook URL, raw coverage output,
coverage XML, coverage database, terminal coverage log, or local missing-line
report was read or imported.

## Owning Layer

Primary owning layer: Quality / Governance.

Coverage thresholds are validation-policy surfaces. They may later influence
CI, local checks, and review expectations, but they do not own parser truth,
corpus truth, fixture validity, security assurance, privacy assurance, release
readiness, deploy readiness, or production readiness.

## Internal Project Area

Quality / Governance.

This contract reads parser quality tooling context, but it does not modify
Parser, Corpus / Provenance, Local App / UI, Workbook / Transport, Analytics,
or Future AI Integration behavior.

## Truth Owner

Truth owner for this contract: repo quality governance.

Coverage tools own only measured coverage for the exact test command, commit,
branch, environment, and configuration used. The Python parser/state layer
continues to own parser behavior and parser facts. Corpus / Provenance
continues to own fixture and corpus evidence.

## Bridge-Code Status

`shared_support`

Coverage threshold policy is shared validation support. It must not create a
reverse-flow where coverage numbers authorize parser behavior changes, fixture
promotion, corpus status changes, #388 activation, or readiness claims.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md`

This contract does not authorize changing:

- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- any future protected-surface coverage checker
- source code under `src/`
- tests under `tests/`
- parser, corpus, workbook, webhook, Apps Script, analytics, AI, or runtime
  behavior

## Observed Current Behavior

Issue #573 / PR #574 recorded one sanitized advisory coverage baseline report.

Baseline values from `docs/implementation_handoffs/quality_coverage_baseline_measurement.md`:

| Metric | Value |
| --- | ---: |
| Measured commit | `f31923ec2b0da629be3eeb8e7971b21aa57fe9fc` |
| Submitted report merge commit | `626bd26318de4b77ece9759582ee4c5939ae6291` |
| Tests passed | 1,949 |
| Total line coverage | 87.56% |
| Covered statements | 22,383 |
| Total statements | 25,564 |
| Missing statements | 3,181 |
| Total branch coverage | 74.87% |
| Covered branches | 7,745 |
| Total branches | 10,344 |
| Missing branches | 2,599 |
| Measured file count | 116 |
| Measured package count | 9 |

Measurement context:

- Command ID: `quality_coverage_baseline.local_pytest_cov.v1`
- Sanitized environment label: `local-macos-python-3.14.3-arm64`
- Branch coverage: enabled by `pyproject.toml`
- Raw coverage outputs: kept local and ignored
- `--cov-fail-under`: not used

Current configuration observations:

- `pyproject.toml` enables branch coverage and sets coverage source to
  `src/mythic_edge_parser`.
- `.github/workflows/repo-checks.yml` runs `py -m pytest -q tests`, protected
  surface checks for PRs, and Ruff, but does not run coverage.
- `tools/run_repo_checks.ps1 -Coverage` runs coverage locally without an
  enforced threshold.

## Problem

The first bad value is turning the local advisory baseline directly into CI
enforcement. The baseline is useful evidence, but it was collected on a local
macOS environment while current GitHub Actions tests run on Windows with a
different Python version.

The second bad value is choosing a vanity threshold such as 90% because it
sounds strong. The first enforceable floor must be derived from measured
evidence and must leave a safety margin for environment variance and normal
reviewable changes.

The third bad value is treating line coverage and branch coverage as the same
policy. Branch coverage is enabled and valuable, but the measured branch
baseline is lower and may be more sensitive to control-flow shape. It should
remain advisory-only at first unless a later CI remeasurement and contract
explicitly prove it is stable enough to enforce.

The fourth bad value is treating a coverage gate as parser correctness,
private-evidence readiness, fixture-promotion readiness, security assurance, or
release readiness. Coverage can prevent some test-execution backsliding. It
cannot certify truth.

## Scope Decision

This contract selects an advisory-first threshold policy.

Selected policy:

```yaml
baseline_status: advisory_local_baseline_interpreted
ci_remeasurement_required_before_enforcement: true
line_coverage_candidate_floor_percent: 85.00
line_coverage_candidate_floor_status: proposal_only
branch_coverage_candidate_floor_percent: null
branch_coverage_status: advisory_only_for_first_enforcement_step
coverage_enforcement_authorized: false
coverage_fail_under_authorized: false
```

Rationale:

- The measured line baseline is 87.56%.
- A candidate 85.00% line floor leaves a 2.56 percentage-point margin below the
  local measurement.
- The candidate floor is low enough to prevent obvious backsliding while
  avoiding immediate churn from normal CI/environment variance.
- The candidate is not an accepted floor and must not be wired into CI until a
  later issue remeasures in the CI environment and reviews the result.
- Branch coverage at 74.87% should be recorded and watched, but not enforced in
  the first threshold implementation.

## Baseline Interpretation Rules

The #573 baseline is authoritative only for:

- interpreting the current advisory local measurement;
- selecting a reviewable candidate threshold;
- explaining why a later CI remeasurement is required;
- preserving the line/branch distinction;
- shaping future validation requirements.

The #573 baseline is not authoritative for:

- accepted CI floor values;
- `--cov-fail-under` activation;
- protected-surface coverage groups;
- new-code coverage gates;
- parser correctness;
- fixture validity;
- corpus readiness;
- security assurance;
- privacy assurance;
- release, deploy, or production readiness.

If future measurements disagree with #573:

- treat the disagreement as environment or drift evidence first;
- do not lower or raise thresholds automatically;
- route to Codex A/B for issue and contract review when the difference would
  affect enforcement;
- record the measured commit, command, environment label, line coverage, branch
  coverage, and degraded/missing/malformed report status.

## Threshold Vocabulary

`baseline`

- A measured coverage result from an approved command, commit, and environment.
- Baselines may be local advisory, CI advisory, or accepted enforcement
  baselines.

`advisory_baseline`

- A sanitized baseline artifact used for planning only.
- It never fails CI and never implies readiness.

`candidate_floor`

- A proposed threshold for review.
- It may appear in contracts, issue comments, or PR descriptions.
- It must not be passed to `--cov-fail-under` or any checker.

`accepted_floor`

- A threshold approved by a later issue, contract, review, submitter, and
  deployer path.
- It may be enforced only after CI/local command behavior and exception rules
  are explicit.

`freeze`

- A decision to keep the current accepted floor while gathering more evidence.
- A freeze must name the reason and expiration or revisit condition.

`raise`

- A decision to increase an accepted floor after sustained evidence or cleanup.
- Raises require their own issue or explicit child scope.

`exception`

- A scoped allowance for a change that should not be judged by the normal
  threshold policy.
- Exceptions must name issue/PR, category, affected surface, allowed scope, and
  expiration condition.

`temporary_lowering`

- A time-limited lowering of an accepted floor.
- It must be explicit, reviewed, and recorded with rollback/revisit conditions.

`rollback`

- Reverting a threshold change or enforcement wiring when the gate produces
  incorrect or excessive blocking behavior.

## Candidate Line-Coverage Policy

Candidate first global line floor:

```yaml
candidate_floor_kind: global_line_coverage
candidate_floor_percent: 85.00
source_baseline_percent: 87.56
safety_margin_percentage_points: 2.56
status: proposal_only
```

This candidate may be used in later issue framing and review discussion. It
must not be enforced by this contract.

Before this candidate can become an accepted floor, a later issue must:

1. run a CI-environment advisory coverage measurement or an explicitly approved
   CI-like measurement;
2. confirm the command uses the same source and branch coverage configuration
   expected by enforcement;
3. record sanitized aggregate line and branch coverage values;
4. compare CI-environment line coverage to the #573 local baseline;
5. explain whether 85.00% remains fair;
6. define exact exception handling;
7. define rollback/freeze behavior;
8. pass Codex E review;
9. route any CI/local command edits through Codex C/E/F/G.

CI remeasurement guard:

- If CI-environment line coverage is at least 87.00%, 85.00% remains the
  preferred candidate floor.
- If CI-environment line coverage is between 85.00% and 86.99%, do not enforce
  by default. Route back to Codex B to decide whether the margin is still safe.
- If CI-environment line coverage is below 85.00%, do not enforce. Record the
  discrepancy and route to Codex A/B for a new policy decision.

Accepted floor rule:

- The first accepted global line floor must be less than or equal to the
  reviewed CI-environment measurement minus an explicit safety margin.
- The first accepted global line floor must not exceed 85.00% unless a later
  contract proves the repo can sustain a higher floor without blocking
  legitimate scoped work.

## Branch-Coverage Policy

Branch coverage baseline:

```yaml
advisory_branch_baseline_percent: 74.87
branch_coverage_status: advisory_only
first_enforcement_authorized: false
```

Branch coverage should remain advisory-only for the first enforcement step.

Reasons:

- Branch coverage was measured and should continue to be visible.
- The branch baseline is materially lower than line coverage.
- Branch coverage can be sensitive to error handling, guards, protocol
  fallbacks, and defensive branches that are valuable even when not yet fully
  covered.
- Enforcing branch coverage before a CI remeasurement and path-group review
  risks incentivizing superficial tests or unsafe branch removal.

Later branch-floor work must be separate and must include:

- at least one CI-environment advisory branch measurement;
- path or module review for branch-heavy protected surfaces;
- explicit exception handling for defensive branches, generated code, and
  deliberately unreachable safety guards;
- focused tests for any custom branch checker;
- non-claims preserving parser truth and readiness boundaries.

## Exception Categories

Allowed future exception categories:

- `docs_only`
- `contract_only`
- `generated_file`
- `fixture_metadata_only`
- `fixture_safe_synthetic_only`
- `report_only_boundary`
- `private_evidence_blocked`
- `external_boundary_blocked`
- `deferred_lane`
- `parked_lane`
- `legacy_bridge_pending_contract`
- `tooling_bootstrap`
- `ci_environment_drift`
- `human_approved_temporary_exception`

Exception records must include:

- issue or PR reference;
- exception category;
- affected coverage policy layer: global line floor, branch advisory posture,
  protected-surface floor, new-code expectation, or all;
- reason;
- allowed scope;
- forbidden scope;
- expiration or revisit condition;
- reviewer expectation;
- non-claims.

Exceptions must not hide raw/private artifacts, secrets, parser truth gaps,
corpus status changes, fixture-promotion gaps, or readiness claims.

## Future Threshold Change Representation

Future threshold changes must be represented as:

1. GitHub issue or issue comment selecting the single threshold lane.
2. Codex B contract defining the exact policy.
3. Codex C implementation only if code or CI changes are explicitly
   authorized.
4. Codex E review or contract test.
5. Codex F draft PR submission.
6. Codex G merge/close/tracker update only after explicit user approval and
   passing gates.

Each future threshold issue must include:

- source baseline artifact;
- candidate floor;
- accepted floor, if any;
- environment and command;
- changed files;
- exception vocabulary;
- validation evidence;
- rollback/freeze plan;
- non-claims.

## Future Implementation Boundaries

Later implementation may only proceed under a separate issue and contract.

Possible future implementation surfaces:

- `pyproject.toml` only if adding or documenting accepted coverage behavior;
- `.github/workflows/repo-checks.yml` only if CI coverage execution or
  enforcement is explicitly authorized;
- `tools/run_repo_checks.ps1` only if local coverage helper behavior must match
  the accepted policy;
- a future path-group checker under `tools/` only after a protected-surface
  contract defines groups, thresholds, failure behavior, and tests.

This contract does not authorize those edits.

## Required Validation Before Future Enforcement

Before any future enforcement PR, the workflow must provide:

- clean checkout or clean sibling worktree status;
- exact commit SHA measured;
- exact measurement command;
- exact enforcement command proposal;
- sanitized local and CI-environment aggregate coverage values;
- proof raw coverage outputs are ignored and not staged;
- `git diff --check`;
- secret/private-marker scan of changed public artifacts;
- protected-surface scan of changed public artifacts;
- validation selector output, if relevant;
- focused tests for any new checker or command wrapper;
- rollback or freeze instructions;
- explicit statement that #388/#381 remain unaffected unless a separate parser
  evidence issue says otherwise.

## Error Behavior

Future threshold tooling or policy must fail closed when:

- the coverage report is missing;
- the coverage report is malformed;
- the report comes from the wrong commit, branch, command, source path, or
  environment;
- a public artifact contains local absolute paths;
- raw coverage XML, raw terminal logs, `.coverage`, HTML, JSON, or line-by-line
  missing reports are staged;
- a threshold is missing in enforcement mode;
- a threshold is non-numeric or outside 0-100;
- an exception lacks issue/PR reference or expiration condition;
- branch coverage enforcement is attempted before a branch-floor contract
  exists;
- `--cov-fail-under` appears before an accepted floor is approved;
- parser truth, fixture promotion, corpus readiness, security assurance,
  privacy assurance, release readiness, analytics truth, AI truth, or coaching
  truth is claimed from coverage.

For this contract-only issue, failure behavior is advisory: record the problem
and stop. Do not patch CI or run coverage.

## Side Effects

This Codex B scope may write:

- `docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md`

This Codex B scope must not:

- implement code;
- run coverage;
- change CI;
- activate `--cov-fail-under`;
- change `pyproject.toml`;
- change `.github/workflows/repo-checks.yml`;
- change `tools/run_repo_checks.ps1`;
- create a protected-surface coverage checker;
- commit raw coverage outputs;
- change parser behavior;
- promote fixtures;
- update corpus metadata;
- activate #388 or #381;
- close issues or trackers;
- open a PR.

## Dependency Order For Later Work

1. Issue #575: interpret the advisory baseline and propose candidate policy.
2. Later CI advisory measurement issue: remeasure in CI or CI-like environment
   without enforcement.
3. Later global line-floor contract: decide whether 85.00% or another floor is
   accepted.
4. Later global line-floor implementation: update CI/local helper only after
   review and approval.
5. Later branch-coverage advisory/reporting issue: decide whether branch
   coverage should remain advisory or get a separate floor.
6. Later protected-surface coverage contract: define path groups and thresholds.
7. Later protected-surface checker implementation and tests.
8. Later ratchet raise/freeze/lower policy based on sustained evidence.

## Compatibility

Existing behavior must remain valid:

- `py -m pytest -q tests` remains the current CI test command.
- `py -m ruff check src tests tools` remains the current CI lint command.
- `tools/run_repo_checks.ps1 -Coverage` remains non-enforcing.
- `pyproject.toml` coverage config remains advisory configuration.
- #388 and #381 remain inactive unless their own issues and contracts authorize
  action.

## Tests And Validation Required

This docs-only contract package requires validation:

```bash
printf '%s\n' docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

Because this is a new untracked file, also validate whitespace with:

```bash
git diff --check --no-index /dev/null docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md
```

Do not run coverage for this docs-only contract, review, or submission package.

Later enforcement implementation validation should include focused tests for:

- accepted global floor pass/fail behavior;
- missing coverage report;
- malformed coverage report;
- wrong commit or wrong source path;
- exception handling;
- branch coverage advisory-only behavior;
- rollback or freeze configuration, if implemented.

## Acceptance Criteria

- The contract interprets the #573 baseline without overstating authority.
- The contract separates advisory baseline, candidate floor, accepted floor,
  and enforcement.
- The contract proposes a conservative 85.00% global line-coverage candidate
  floor without activating it.
- The contract keeps branch coverage advisory-only for the first enforcement
  step.
- The contract requires CI-environment remeasurement before enforcement.
- The contract defines ratchet vocabulary and exception vocabulary.
- The contract routes CI or command changes to later issues only.
- The contract preserves #388/#381 inactive.
- The contract makes no parser truth, fixture-promotion, corpus-readiness,
  release-readiness, security-assurance, privacy-assurance, analytics-truth,
  AI-truth, or coaching-truth claims.

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

Codex C implementation is not recommended yet because this contract selects
policy semantics only and keeps enforcement unauthorized.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer / Contract Tester for issue #575.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/575

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Active parser evidence tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/573

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/574

Previous merge commit:
626bd26318de4b77ece9759582ee4c5939ae6291

Contract:
docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md

Goal:
Review the coverage baseline interpretation and candidate threshold policy
contract. Lead with findings, if any. Verify that the contract interprets the
#573 advisory baseline without turning it into enforcement, keeps the 85.00%
line floor as proposal-only, keeps branch coverage advisory-only, requires
CI-environment remeasurement before enforcement, and preserves all
parser/corpus/readiness/security/privacy non-claims.

Suggested validation:
- Inspect `docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md`.
- Run `printf '%s\n' docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`.
- Run `printf '%s\n' docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`.
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/575"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  active_parser_evidence_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/573"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/574"
  previous_merge_commit: "626bd26318de4b77ece9759582ee4c5939ae6291"
  completed_thread: "B"
  next_thread: "E"
  verdict: "coverage_baseline_interpretation_threshold_policy_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/quality-coverage-threshold-policy-575"
  target_artifact: "docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md"
  advisory_line_baseline_percent: 87.56
  candidate_line_floor_percent: 85.00
  advisory_branch_baseline_percent: 74.87
  branch_coverage_status: "advisory_only"
  ci_remeasurement_required_before_enforcement: true
  implementation_authorized: false
  ci_change_authorized: false
  coverage_enforcement_authorized: false
  coverage_fail_under_authorized: false
  coverage_measurement_execution_authorized: false
  parser_behavior_change_authorized: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  validation:
    - "printf '%s\\n' docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
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
