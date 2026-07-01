# Quality Coverage Global Line Floor Enforcement Readiness Contract

## Module

`quality_coverage_global_line_floor_enforcement_readiness`

This contract defines Mythic Edge's first readiness decision for a possible
global Python line coverage floor. A coverage floor is a threshold below which a
future validation command may fail. This contract does not enable that failure
behavior by itself.

## Source Artifacts

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/595>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/566>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Source measurement issue: <https://github.com/Tahjali11/Mythic-Edge/issues/591>
- Source measurement PR: <https://github.com/Tahjali11/Mythic-Edge/pull/594>
- Prior contracts:
  - `docs/contracts/quality_coverage_baseline_ratchet_design.md`
  - `docs/contracts/quality_coverage_baseline_interpretation_threshold_policy.md`
  - `docs/contracts/quality_coverage_ci_environment_remeasurement.md`
  - `docs/contracts/quality_coverage_ci_remeasurement_execution_preflight.md`
- Source measurement artifact:
  - `docs/implementation_handoffs/quality_coverage_ci_environment_remeasurement.md`
- Source review artifact:
  - `docs/contract_test_reports/quality_coverage_ci_environment_remeasurement.md`
- Current coverage configuration:
  - `pyproject.toml`
  - `tools/run_repo_checks.ps1`
  - `.github/workflows/repo-checks.yml`

## Role And Scope

Role performed: Codex B / Module Contract Writer.

This is a contract-only artifact. It does not implement code, change CI,
activate `--cov-fail-under`, run coverage, change parser behavior, change
fixtures, promote corpus status, or change production, security/privacy,
analytics, AI, or coaching truth.

## Truth Ownership

Coverage tooling owns only a measured coverage result for an exact command,
commit, branch/ref, dependency set, runner shape, and coverage configuration.

Coverage does not own parser truth, fixture authority, corpus readiness,
security/privacy assurance, release readiness, production readiness, analytics
truth, AI truth, or coaching truth. Parser-owned facts remain owned by the
parser/state layer and related parser contracts.

## Observed Current Behavior

Current Python coverage configuration:

- `pytest-cov` is available as a development dependency.
- `pyproject.toml` sets `branch = true`.
- `pyproject.toml` sets coverage source to `src/mythic_edge_parser`.
- `pyproject.toml` reports missing lines and skips fully covered files.
- `tools/run_repo_checks.ps1 -Coverage` runs:

```powershell
py -m pytest --cov=src/mythic_edge_parser --cov-report=term-missing tests
```

- The local helper does not pass `--cov-fail-under`.
- `.github/workflows/repo-checks.yml` currently runs the test suite without
  coverage enforcement.

Recorded Windows CI-equivalent advisory measurement from #591 / PR #594:

```yaml
measured_ref: origin/main
measured_commit: d9a9c335561b7af6e8e1f6745c712741267eed5d
tests_passed: 1986
tests_skipped: 4
line_coverage_percent: 87.55
branch_coverage_percent: 74.80
coverage_fail_under_used: false
coverage_enforcement_authorized: false
raw_coverage_artifacts_committed: false
```

Current inspection for this contract observed `origin/main` at
`cf7147554cdc3c92bfde5d38f4f7afd265bd8b46`, which is newer than the measured
commit. Therefore the #591 / PR #594 number is valid historical evidence, but
it is stale for direct activation on current `origin/main` until remeasured or
reconfirmed by a later implementation/review thread.

## Readiness Verdict

Mythic Edge is ready to propose a first global Python line coverage gate, but it
is not ready to enable the gate directly from this contract.

The recommended first gate posture is:

```yaml
recommended_posture: blocking_global_python_line_floor_after_fresh_validation
accepted_floor_candidate_percent: 85.00
branch_coverage_posture: advisory_only
activation_authorized_by_this_contract: false
```

Plain English: the 85.00% global line floor is reasonable because the latest
approved Windows CI-equivalent measurement was 87.55%, but the measurement was
taken at an older commit. A later Codex C thread must compare current repo state
to this contract and either remeasure the current base or prove an equivalent
fresh CI result before wiring a blocking gate.

## Gate Posture Decision

The first enforcement slice should not be advisory dry-run only if fresh
validation still shows a stable margin above 85.00%. It may proceed to a
blocking 85.00% global Python line floor only when all prerequisites below are
satisfied.

The first enforcement slice must be deferred when:

- current-base coverage cannot be measured or confirmed;
- the measurement commit is stale and no fresh result exists;
- current global line coverage is below 85.00%;
- current global line coverage is between 85.00% and 86.99% and reviewer
  judgment finds the margin too narrow or noisy;
- the implementation would require branch coverage enforcement;
- the implementation would commit raw coverage artifacts;
- the implementation would make coverage a proxy for parser correctness,
  security/privacy assurance, or release readiness;
- CI failure messaging cannot clearly explain the floor and remediation path.

Advisory dry-run remains an allowed fallback if Codex C or Codex E finds
environment drift, stale-ref risk, or insufficient failure-message clarity.

## Global Line Floor Policy

The only first gate allowed by this contract is:

```yaml
metric: global_python_line_coverage_percent
scope: src/mythic_edge_parser
floor_percent: 85.00
runner_family: repo_approved_python_test_runner
branch_coverage_enforcement: false
frontend_coverage_enforcement: false
```

The floor must be implemented through one coherent repo-approved path. Do not
create a second unsynchronized coverage authority. If a later implementation
chooses `--cov-fail-under=85`, that value must match this contract exactly and
must apply only to the global Python line percentage.

The floor must not be raised above 85.00% in this issue. A higher ratchet needs
a later measurement, contract, and explicit approval.

## Branch Coverage Advisory-Only Policy

Branch coverage may continue to be collected and summarized because
`pyproject.toml` enables branch measurement. It must not fail CI or local repo
checks in the first enforcement slice.

Allowed branch coverage fields:

- measured branch percentage;
- runner/ref metadata;
- advisory label;
- comparison to prior advisory measurements.

Forbidden first-slice branch coverage behavior:

- `--cov-fail-under` for branch coverage;
- custom branch-coverage failure script;
- required branch coverage badge, gate, or threshold;
- blocking PRs based on branch percentage;
- treating branch coverage as parser, security, privacy, or release truth.

## Preconditions Before Enabling `--cov-fail-under`

Before any later thread enables `--cov-fail-under`, it must prove:

1. The measured branch/ref and commit are the same as the intended enforcement
   base, or the difference is explicitly accepted by Codex E/G with fresh CI
   evidence.
2. The coverage command uses the existing Python coverage scope:
   `src/mythic_edge_parser`.
3. The full Python test suite passes under the same command family.
4. The current global Python line coverage is at least 85.00%.
5. Branch coverage remains advisory-only.
6. Raw coverage artifacts remain uncommitted and ignored.
7. The gate failure message names:
   - the required line floor, `85.00%`;
   - the measured line percentage;
   - that branch coverage is advisory-only;
   - the command or workflow that failed;
   - the expected remediation path: add focused tests, adjust scope through a
     later contract, or route to Codex B if the gate is wrong.
8. The implementation does not change parser behavior, parser state final
   reconciliation, fixtures, corpus status, protected surfaces, production
   behavior, analytics truth, AI truth, or coaching truth.

## Stale-Ref Policy

The #591 / PR #594 measurement at
`d9a9c335561b7af6e8e1f6745c712741267eed5d` is historical after `origin/main`
advanced to `cf7147554cdc3c92bfde5d38f4f7afd265bd8b46`.

Later roles must apply these rules:

- If the intended base commit differs from the recorded measurement commit,
  the old coverage numbers may be cited only as historical context.
- Codex C must remeasure the intended base or cite a fresh CI-equivalent result
  before implementing a blocking gate.
- Codex E must treat any gate implementation without fresh-base evidence as a
  blocking contract mismatch.
- Codex G must not merge or close #595 as enforcement-ready if the branch was
  rebased, merged, or otherwise moved after the last successful coverage proof
  and no fresh CI/check evidence exists.
- Any report must name both the measured commit and the current base commit.
- No workflow output may imply that stale measurements prove current readiness.

## Raw Artifact And Privacy Rules

Coverage execution may create local or CI-scoped generated artifacts. These
must remain uncommitted unless a later contract explicitly authorizes a
sanitized summary artifact.

Do not commit:

- `.coverage` or `.coverage.*`;
- `coverage.xml`;
- coverage JSON files;
- HTML coverage directories such as `htmlcov/`;
- raw terminal transcripts;
- full missing-line reports copied from raw output;
- local absolute paths;
- private/local artifacts, raw logs, secrets, credentials, tokens, webhook URLs,
  spreadsheet IDs, environment values, generated SQLite files, failed posts, or
  workbook exports.

Allowed public-safe summaries may include aggregate percentages, test counts,
runner labels, command labels, commit SHAs, and advisory/blocking status.

## Failure Message Contract

If a later implementation activates a blocking line floor, the failing output
must be understandable without reading a long contract. It should say, in
effect:

```text
Global Python line coverage is below Mythic Edge's accepted 85.00% floor.
Branch coverage is advisory-only and did not cause this failure.
Rerun the approved coverage command on the current base, add focused tests for
the changed behavior, or route back to Codex B if the floor/scope is stale.
Do not commit raw coverage artifacts.
```

The message must not claim parser correctness, security/privacy assurance,
private-local-v1 readiness, production readiness, or AI/coaching readiness.

## Protected Surfaces

This contract touches workflow and validation policy only.

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
- production behavior;
- secrets, credentials, raw logs, generated data, runtime artifacts, failed
  posts, workbook exports, and local-only artifacts.

CI and validation gates are workflow protected surfaces. This contract may
authorize a later scoped Codex C implementation to compare and propose the
smallest coverage-gate edit, but Codex B does not edit CI or activate the gate.

## Validation Requirements

For this Codex B contract:

```powershell
git status --short --branch
git diff --check -- docs\contracts\quality_coverage_global_line_floor_enforcement_readiness.md
py tools\check_agent_docs.py
@'
docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

Do not run coverage for this Codex B pass.

For later Codex C implementation, if the user authorizes moving from readiness
contract to implementation:

- confirm branch and base commit;
- remeasure or cite fresh CI-equivalent coverage on the intended base;
- prove global Python line coverage is at least 85.00%;
- implement only the smallest coherent line-floor gate;
- keep branch coverage advisory-only;
- keep raw artifacts untracked;
- run focused tests for any helper or message changes;
- run the approved coverage command with the gate enabled;
- run repo docs/checks appropriate to the files changed;
- run protected-surface and secret/private-marker scans on the changed paths;
- produce
  `docs/implementation_handoffs/quality_coverage_global_line_floor_enforcement_readiness_comparison.md`.

For Codex E review:

- verify implementation against this contract;
- verify fresh-ref coverage evidence;
- verify no branch coverage enforcement;
- verify failure-message clarity;
- verify no raw artifacts were committed;
- verify protected surfaces remain untouched;
- produce
  `docs/contract_test_reports/quality_coverage_global_line_floor_enforcement_readiness.md`.

For Codex G integration:

- verify PR target and base freshness;
- verify CI/check status after any rebase or merge-base change;
- verify issue #595 and tracker #566 are updated without overclaiming release,
  parser, security/privacy, analytics, AI, or coaching readiness;
- do not close tracker #566 unless the tracker itself is complete.

## Acceptance Criteria

- This contract records the #591 / PR #594 measurement as historical evidence.
- This contract records that current `origin/main` has advanced beyond the
  measured commit.
- This contract selects a conditional blocking 85.00% global Python line floor
  as the recommended first gate posture.
- This contract keeps branch coverage advisory-only.
- This contract defines stale-ref, raw-artifact, and failure-message rules.
- This contract defines validation expectations for Codex C, Codex E, and
  Codex G.
- This contract does not implement code or CI changes.

## Unknowns And Suspected Gaps

- Current-base coverage after `origin/main` advanced to
  `cf7147554cdc3c92bfde5d38f4f7afd265bd8b46` is unknown in this Codex B pass.
- The exact implementation location for the future gate is intentionally left
  to Codex C comparison. Likely candidates are the existing repo check helper,
  GitHub Actions workflow, or both, but only one coherent authority should own
  the blocking behavior.
- It is unknown whether a future gate failure message needs a small helper
  wrapper or whether pytest-cov's built-in message plus repo docs is sufficient.
- It is unknown whether the 2.55 point historical margin remains after current
  main changes.

## Out Of Scope

- Running coverage in Codex B.
- Editing CI in Codex B.
- Activating `--cov-fail-under` in Codex B.
- Adding branch coverage enforcement.
- Adding frontend coverage enforcement.
- Changing parser behavior or tests solely to raise coverage.
- Changing fixtures, snapshots, corpus status, or raw evidence promotion.
- Claiming security/privacy, parser correctness, release readiness, production
  readiness, analytics truth, AI truth, or coaching truth.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/595

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract:
docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md

Goal:
Compare current repo coverage configuration, helper scripts, CI workflows, and
the #591 / PR #594 measurement artifact against the contract. If fresh-base
validation supports it, implement the smallest coherent 85.00% global Python
line coverage floor. Keep branch coverage advisory-only.

Before editing:
- Confirm branch and git status.
- Confirm current base commit and compare it to the recorded #591 measurement
  commit d9a9c335561b7af6e8e1f6745c712741267eed5d.
- Treat the #591 measurement as historical if the current base differs.
- Inspect pyproject.toml, tools/run_repo_checks.ps1, .github/workflows/, and
  prior coverage contracts/reports.
- State whether a fresh coverage measurement is required before implementing.

Do:
- Produce docs/implementation_handoffs/quality_coverage_global_line_floor_enforcement_readiness_comparison.md.
- If and only if fresh validation supports it, implement the smallest coherent
  global Python line floor at 85.00%.
- Keep branch coverage advisory-only.
- Keep raw coverage artifacts uncommitted.
- Make failure messaging clear about the 85.00% line floor, advisory-only
  branch coverage, stale-ref handling, and remediation path.

Do not:
- Change parser behavior.
- Change fixtures, snapshots, corpus status, production behavior, security/privacy assurance,
  analytics truth, AI truth, or coaching truth.
- Add branch coverage enforcement.
- Add frontend coverage enforcement.
- Commit .coverage, coverage.xml, HTML coverage output, raw terminal logs,
  local absolute paths, secrets, credentials, raw logs, generated data, or
  local-only artifacts.
- Target main directly.
- Close tracker #566.

Validation:
- git status --short --branch
- fresh-base coverage validation or explicit blocked/deferred rationale
- focused tests for any helper/message changes
- approved coverage command with the 85.00% line floor if implemented
- py tools/check_agent_docs.py
- git diff --check
- protected-surface scan on changed paths
- secret/private-marker scan on changed paths

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- current base commit and measurement freshness decision
- implementation or deferral decision
- files changed
- validation run and results
- protected-surface status
- raw-artifact status
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/595"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/implementation_handoffs/quality_coverage_ci_environment_remeasurement.md"
  contract_artifact: "docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md"
  target_artifact: "docs/implementation_handoffs/quality_coverage_global_line_floor_enforcement_readiness_comparison.md"
  risk_tier: "Medium-High"
  branch: "codex/coverage-enforcement-readiness-566"
  readiness_verdict: "ready_to_propose_blocking_85_global_python_line_floor_after_fresh_validation"
  recommended_gate_posture: "conditional_blocking_85_global_line_floor"
  branch_coverage_posture: "advisory_only"
  stale_ref_policy: "source measurement d9a9c335 is historical because origin/main observed at cf714755; Codex C must remeasure or cite fresh CI-equivalent evidence before activation"
  validation:
    - "git diff --check -- docs\\contracts\\quality_coverage_global_line_floor_enforcement_readiness.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan"
    - "path-scoped secret/private-marker scan"
  stop_conditions:
    - "Do not implement CI changes in Codex B."
    - "Do not activate --cov-fail-under without fresh-base validation."
    - "Do not add branch coverage enforcement."
    - "Do not commit raw coverage artifacts."
    - "Do not change parser behavior, fixtures, corpus status, production behavior, security/privacy assurance, analytics truth, AI truth, or coaching truth."
```
