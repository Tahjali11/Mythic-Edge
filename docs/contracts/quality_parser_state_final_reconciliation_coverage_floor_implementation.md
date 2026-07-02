# Quality Parser-State Final-Reconciliation Coverage Floor Implementation Contract

## Module

`quality_parser_state_final_reconciliation_coverage_floor_implementation`

Plain English: this contract defines the first narrow protected-surface Python
line coverage floor for the parser state/final reconciliation surface. A
coverage floor is a threshold that fails validation when measured coverage
drops below it.

This Codex B pass writes the contract only. It does not implement tooling,
change CI, change `pyproject.toml`, run coverage, activate a floor, or change
parser behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/625
- Threshold review issue: https://github.com/Tahjali11/Mythic-Edge/issues/632
- Completed retry-gate issue: https://github.com/Tahjali11/Mythic-Edge/issues/635
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566

## Tracker

Tracker #566 remains open for the broader coverage ratchet and quality
threshold program. This contract covers only the first narrow
`parser_state_final_reconciliation` protected-surface floor.

## Owning Layer

Quality / validation tooling.

Coverage tooling owns measured execution evidence for a specific command,
commit/ref, coverage source, coverage XML, and validation configuration.
Coverage does not own parser truth, parser correctness, security assurance,
privacy assurance, release readiness, deploy readiness, production readiness,
analytics truth, AI truth, or coaching truth.

## Internal Project Area

Quality / validation gates, with protected-surface relationship to Parser.

## Truth Owner

The parser/state layer owns parser truth, final reconciliation behavior, match
facts, game facts, match/game identity, and deduplication.

The coverage checker owns only pass/fail validation for the configured coverage
thresholds. It must never become a substitute for parser contracts, parser
tests, review, corpus evidence, or behavior correctness.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
coverage XML from approved pytest-cov command
  -> global line coverage checker
  -> allow-listed parser_state_final_reconciliation file checks
  -> local and CI validation status
```

Forbidden reverse flow:

- coverage tooling must not change parser behavior;
- coverage percentages must not imply parser correctness;
- coverage failure must route to focused tests, contract review, or explicit
  threshold review, not silent parser or downstream behavior changes.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md`

Later Codex C may edit only the minimum necessary implementation files for the
floor:

- `tools/check_coverage_floor.py`
- `tests/test_check_coverage_floor.py`
- `tools/run_repo_checks.ps1`
- `.github/workflows/repo-checks.yml`
- `tools/select_validation_mappings.py`, only if the changed checker/test file
  mapping needs a narrow update
- `tests/test_run_repo_checks_script.py`, only if the local repo-check helper
  invocation must be pinned by test
- `docs/implementation_handoffs/quality_parser_state_final_reconciliation_coverage_floor_implementation_comparison.md`

Codex C must not edit parser runtime files, parser tests, fixtures, corpus
data, analytics files, workbook transport files, Apps Script, generated
coverage artifacts, or private/local artifacts unless a later contract
explicitly changes scope.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- issue #625
- issue #632
- issue #635
- tracker #566
- `docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md`
- `docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md`
- `docs/contracts/quality_parser_state_final_reconciliation_test_hardening.md`
- `docs/implementation_handoffs/quality_parser_state_final_reconciliation_test_hardening_comparison.md`
- `docs/contract_test_reports/quality_parser_state_final_reconciliation_test_hardening.md`
- `docs/contract_test_reports/quality_coverage_global_line_floor_enforcement_readiness.md`
- `docs/contract_test_reports/quality_protected_surface_coverage_floor_candidate_selection.md`
- `docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json`
- `tools/check_coverage_floor.py`
- `tools/generate_protected_surface_coverage_report.py`
- `tools/run_repo_checks.ps1`
- `tests/test_check_coverage_floor.py`
- `tests/test_protected_surface_coverage_report.py`
- `tests/test_run_repo_checks_script.py`
- `.github/workflows/repo-checks.yml`
- `pyproject.toml`

## Observed Current Behavior

Current branch inspection for this contract observed:

```yaml
branch: codex/parser-state-coverage-floor-retry-625
base_ref: origin/main
head: 27d35146d7d5eb094611d941ad8111f2981d83db
origin_main: 27d35146d7d5eb094611d941ad8111f2981d83db
branch_sync: "0 0"
target_contract_exists_on_main: false
```

Current global coverage behavior:

- `tools/check_coverage_floor.py` enforces the active global Python line floor.
- The active global Python line floor is `85.00%`.
- Branch coverage is parsed for reporting but remains advisory-only.
- `tools/run_repo_checks.ps1 -Coverage` runs the full tests with coverage XML
  under `_review_/quality_coverage_global_line_floor/run_repo_checks/` and
  invokes `tools/check_coverage_floor.py`.
- `.github/workflows/repo-checks.yml` runs the same global line floor checker
  in GitHub Actions.

Current protected-surface report behavior:

- `tools/generate_protected_surface_coverage_report.py` is advisory-only.
- Its report schema records protected-surface groups and public-safe
  percentages.
- It must remain a report helper, not the enforcement authority for this first
  floor.

Completed retry gate from #635 / PR #636:

```yaml
pr: "https://github.com/Tahjali11/Mythic-Edge/pull/636"
merge_commit: "27d35146d7d5eb094611d941ad8111f2981d83db"
global_line_coverage_percent: 87.64
branch_coverage_percent: 74.86
branch_coverage_posture: advisory_only
models_py_line_coverage_percent: 90.45
state_py_line_coverage_percent: 92.96
protected_surface_floor_activated: false
```

The retry gate is satisfied at the inspected base, but Codex C must still
verify the branch is fresh and re-run current-base coverage before activating
the floor because validation gates are sensitive to stale refs.

## Implementation Shape Decision

Codex C should extend the existing global coverage checker rather than turning
the advisory protected-surface report helper into an enforcement tool.

Decision:

```yaml
implementation_shape: extend_tools_check_coverage_floor
reason: one_repo_approved_coverage_floor_authority
do_not_enforce_from: tools/generate_protected_surface_coverage_report.py
do_not_create_second_unsynchronized_checker: true
```

Recommended checker behavior:

- Preserve existing global-only behavior when no protected-surface group is
  requested.
- Add an explicit allow-listed protected-surface group:
  `parser_state_final_reconciliation`.
- Require an exact line-only floor of `88.00%` for that group.
- Treat the group as passing only when every required candidate file is present
  in coverage XML and each file's line coverage is at or above `88.00%`.
- Report the group result using the minimum candidate-file line coverage rather
  than an average, so a strong file cannot hide erosion in a weaker file.
- Keep branch coverage advisory-only even when the coverage XML includes branch
  rates.

Allowed CLI shape for Codex C to implement:

```powershell
py tools/check_coverage_floor.py `
  --coverage-xml <local-ignored-coverage-xml> `
  --line-floor 85 `
  --protected-surface-group parser_state_final_reconciliation `
  --protected-surface-line-floor 88 `
  --command-label "<approved command label>"
```

Codex C may choose equivalent option names only if they remain explicit,
allow-listed, documented in the implementation handoff, and covered by focused
tests. Broad free-form path thresholds, arbitrary YAML policy loading, or
repo-wide protected-surface enforcement are out of scope.

## Candidate Files And Threshold

Protected-surface group:

```yaml
group_id: parser_state_final_reconciliation
metric: line_coverage_only
floor_percent: 88.00
group_pass_rule: every_required_file_measured_and_at_or_above_floor
group_reported_percent: minimum_required_file_line_percent
branch_coverage: advisory_only
```

Required files:

| Repo-relative path | Required line floor |
| --- | ---: |
| `src/mythic_edge_parser/app/models.py` | `88.00%` |
| `src/mythic_edge_parser/app/state.py` | `88.00%` |

The `88.00%` initial floor is approved because the retry-gate evidence on the
inspected current base has a buffer above the floor:

| File | Retry-gate line evidence |
| --- | ---: |
| `src/mythic_edge_parser/app/models.py` | `90.45%` |
| `src/mythic_edge_parser/app/state.py` | `92.96%` |

No other protected-surface group, parser file, or coverage metric is included.

## Fresh-Base Preconditions

Before Codex C edits tooling or CI, it must confirm:

```yaml
branch_sync_with_origin_main: "0 0"
global_line_coverage_percent: ">= 85.00"
models_py_line_coverage_percent: ">= 90.00"
state_py_line_coverage_percent: ">= 90.00"
branch_coverage: advisory_only
raw_coverage_artifacts_committed: false
```

Codex C must use a clean full coverage run for precondition evidence. Focused
tests, stale reports, old comments, screenshots, or partial coverage runs do
not satisfy this precondition.

If `origin/main` advances before Codex C starts, Codex C must fast-forward or
stop for branch reconciliation before mutation. If either candidate file falls
below `90.00%` before implementation, Codex C must stop and route back to
Codex B or Codex A rather than lowering the threshold or implementing a weaker
floor.

## Public Interface

The public validation interface may change only by adding a narrow
protected-surface floor option to the existing coverage checker and invoking it
from the existing local and CI coverage paths.

Allowed public interface changes:

- `tools/check_coverage_floor.py` may expose an allow-listed
  `parser_state_final_reconciliation` protected-surface group.
- `tools/run_repo_checks.ps1 -Coverage` may invoke that group with an
  `88.00%` line floor after or alongside the existing global `85.00%` line
  floor.
- `.github/workflows/repo-checks.yml` may invoke the same checker args.
- Focused tests may verify pass, fail, missing XML, malformed XML, missing
  candidate-file data, and branch-advisory behavior.

Forbidden public interface changes:

- broad protected-surface floor configuration;
- arbitrary user-provided path thresholds;
- branch coverage thresholds;
- new global line floor value;
- `pyproject.toml` coverage threshold changes;
- protected-surface report helper enforcement;
- parser, analytics, workbook, webhook, Apps Script, AI, or production
  behavior changes.

## Inputs

Required input:

| Input | Source | Required fields |
| --- | --- | --- |
| Coverage XML | Approved full pytest-cov command | root `line-rate`; class entries for `models.py` and `state.py`; optional root/class `branch-rate` |
| Candidate group | allow-list in coverage checker | group id, repo-relative required files, line floor |
| Command label | local or CI invocation | public-safe label such as `tools/run_repo_checks.ps1 -Coverage` or `GitHub Actions repo checks` |

Coverage XML filename normalization should accept pytest-cov/Cobertura paths
that can be mapped to the required repo-relative paths, such as:

- `src/mythic_edge_parser/app/state.py`
- `mythic_edge_parser/app/state.py`
- `app/state.py`

The checker must not echo local absolute paths from the coverage XML, temporary
directories, or private filesystem locations.

## Outputs

Allowed output fields in command messages:

- global measured line percentage;
- global line floor;
- branch percentage, if present, with advisory-only label;
- protected-surface group id;
- protected-surface required floor;
- repo-relative candidate file paths;
- measured candidate file line percentages;
- failed command label;
- symbolic remediation guidance;
- raw-artifact warning.

Forbidden output:

- local absolute paths;
- raw coverage XML contents;
- raw terminal coverage logs;
- raw Player.log data;
- private/local artifact paths;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, or
  environment values;
- parser correctness, security/privacy, release, deploy, production, analytics,
  AI, or coaching claims.

## Failure Behavior

Exit code expectations:

| Condition | Expected exit code | Behavior |
| --- | ---: | --- |
| Global line floor passes and protected-surface floor passes | `0` | Print success message with advisory branch label. |
| Global line floor fails | `1` | Preserve existing global-floor failure behavior and message. |
| Protected-surface file falls below `88.00%` | `1` | Print public-safe protected-surface floor failure message. |
| Coverage XML missing, malformed, or unreadable | `2` | Fail closed without echoing raw path or parser details. |
| Required candidate file is missing from coverage XML | `2` | Fail closed with repo-relative required file name only. |
| Required candidate file has missing or invalid line-rate | `2` | Fail closed with symbolic missing-data message. |
| Unknown protected-surface group requested | `2` | Fail closed and name only the unsupported symbolic group id. |

Protected-surface failure message should say, in effect:

```text
Protected-surface line coverage for parser_state_final_reconciliation is below Mythic Edge's accepted 88.00% floor.
Measured minimum candidate-file line coverage: <value>.
Branch coverage is advisory-only and did not cause this failure.
Failed command: <command label>.
Add focused behavior-preserving tests, rerun the approved coverage command on the current base, or route back to Codex B if the floor or scope is stale. Do not commit raw coverage artifacts.
```

When possible, include per-file repo-relative measurements, for example:

```text
src/mythic_edge_parser/app/models.py: 90.45%
src/mythic_edge_parser/app/state.py: 87.99% (below floor 88.00%)
```

## Branch-Coverage Advisory Boundary

Branch coverage may be parsed and printed, but it must remain advisory-only.

Forbidden branch behavior:

- no branch `--cov-fail-under`;
- no branch threshold in `tools/check_coverage_floor.py`;
- no branch threshold in `tools/run_repo_checks.ps1`;
- no branch threshold in `.github/workflows/repo-checks.yml`;
- no branch-based PR failure;
- no branch coverage readiness claim.

## Global-Floor Preservation Boundary

The existing global Python line floor remains `85.00%`.

Codex C must not:

- raise or lower the global line floor;
- replace the global floor with the protected-surface floor;
- allow the protected-surface floor to run without preserving the global floor;
- use the protected-surface floor to justify lowering test coverage elsewhere.

## Raw Artifact And Privacy Rules

Coverage execution may create generated local artifacts. These must remain
ignored and uncommitted.

Do not commit:

- `.coverage` or `.coverage.*`;
- `coverage.xml`;
- HTML coverage directories such as `htmlcov/`;
- raw terminal transcripts;
- raw missing-line output copied into docs;
- local absolute paths;
- private logs;
- raw Player.log data;
- private JSONL artifacts;
- generated SQLite files;
- failed posts;
- workbook exports;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs,
  environment values, or local-only artifacts.

Allowed public-safe summaries may include percentages, repo-relative file
paths, command labels, commit SHAs, pass/fail status, and advisory-only labels.

## Protected Surfaces

This contract touches validation gates and coverage tooling. It measures a
parser protected surface, but it must not change that surface.

Protected surfaces preserved:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match identity;
- game identity;
- deduplication;
- fixtures, snapshots, corpus status, and raw evidence promotion;
- analytics schema and ingest behavior;
- workbook schema;
- webhook payload shape;
- Apps Script and Google Sheets behavior;
- OpenAI/model-provider, AI/coaching, and Line Tracer behavior;
- production behavior;
- secrets, credentials, raw logs, generated data, runtime artifacts, failed
  posts, workbook exports, and local-only artifacts.

## Tests Required

Codex C must add or update focused tests for the coverage checker.

Required coverage checker tests:

- existing global-only pass behavior remains unchanged;
- existing global-only failure behavior remains unchanged;
- protected-surface group passes when both candidate files are measured at or
  above `88.00%`;
- protected-surface group fails with exit code `1` when `models.py` is below
  `88.00%`;
- protected-surface group fails with exit code `1` when `state.py` is below
  `88.00%`;
- protected-surface group fails closed with exit code `2` when a required file
  is missing from coverage XML;
- protected-surface group fails closed with exit code `2` when a required file
  has missing or invalid line-rate;
- missing or malformed XML remains a symbolic exit code `2` failure without
  local path echo;
- branch coverage remains advisory-only and cannot cause a failure;
- unsupported protected-surface group is rejected rather than treated as a
  free-form path policy.

Required local/CI helper tests:

- `tests/test_run_repo_checks_script.py` should pin the local helper to invoke
  the protected-surface floor when `-Coverage` is used, unless Codex C provides
  a more direct focused assertion.
- If `.github/workflows/repo-checks.yml` is edited, Codex C must document the
  workflow invocation in the implementation handoff and ensure the same checker
  arguments are used as the local helper.

## Validation Requirements

Before implementation edits:

```powershell
git status --short --branch
git rev-list --left-right --count HEAD...origin/main
.\tools\run_repo_checks.ps1 -Coverage
```

Codex C must parse or report the full coverage evidence from that run:

- global line coverage percent;
- branch coverage percent and advisory-only status;
- `src/mythic_edge_parser/app/models.py` line coverage percent;
- `src/mythic_edge_parser/app/state.py` line coverage percent;
- confirmation that raw coverage artifacts remain ignored/uncommitted.

After implementation:

```powershell
py -m pytest -q tests\test_check_coverage_floor.py tests\test_run_repo_checks_script.py
.\tools\run_repo_checks.ps1 -Coverage
py -m ruff check tools\check_coverage_floor.py tests\test_check_coverage_floor.py tests\test_run_repo_checks_script.py
git diff --check
py tools\check_agent_docs.py
```

Run path-scoped protected-surface and secret/private-marker scans over changed
files:

```powershell
git diff --name-only origin/main | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --name-only origin/main | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

If Codex C changes `.github/workflows/repo-checks.yml`, include it in the
changed-file scans and call out that it is an expected workflow-surface warning
if the scanner reports it.

## Acceptance Criteria

- The existing global `85.00%` line coverage floor still passes and still
  fails independently when global line coverage is below `85.00%`.
- The new protected-surface floor is line-only, exactly `88.00%`, and scoped
  only to `parser_state_final_reconciliation`.
- The new protected-surface floor fails if either `models.py` or `state.py` is
  missing or below `88.00%`.
- The group result cannot hide a weak file behind an average.
- Branch coverage remains advisory-only.
- Local `tools/run_repo_checks.ps1 -Coverage` and GitHub Actions repo checks
  use the same floor checker and same group/floor.
- Failure output is public-safe, repo-relative, and operator-readable.
- Focused tests cover pass, fail, missing, malformed, and branch-advisory
  behavior.
- No parser/product/runtime behavior changes occur.
- Raw coverage artifacts and local-only files are not committed.

## Stop Conditions

Codex C must stop and route back to Codex B or Codex A if:

- the branch is not clean or not synchronized with `origin/main` and cannot be
  safely reconciled;
- full current-base coverage does not complete cleanly;
- global line coverage is below `85.00%`;
- `models.py` or `state.py` is below `90.00%` before implementation;
- implementing the floor would require changing parser code or parser tests;
- implementing the floor would require changing `pyproject.toml`;
- branch coverage would become a blocking threshold;
- arbitrary path thresholds or broad protected-surface groups become necessary;
- failure output would expose private paths, raw artifacts, secrets, or local
  data;
- generated coverage artifacts appear as non-ignored files in `git status`;
- the issue lifecycle changes and #625 is closed, superseded, or no longer the
  active lane.

## Out Of Scope

- Raising or lowering the global `85.00%` Python line floor.
- Enforcing branch coverage.
- Adding any other protected-surface coverage floor.
- Adding broad protected-surface coverage policy loading.
- Changing `pyproject.toml`.
- Changing parser behavior.
- Changing parser state final reconciliation.
- Changing parser event classes.
- Changing match/game identity or deduplication.
- Changing fixtures, corpus status, analytics behavior, workbook behavior,
  webhook behavior, Apps Script behavior, Google Sheets behavior,
  OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior,
  or production behavior.
- Claiming parser correctness, security assurance, privacy assurance, release
  readiness, deploy readiness, production readiness, analytics truth, AI truth,
  or coaching truth from coverage numbers.

## Open Questions And Contract Risks

- The exact option names in `tools/check_coverage_floor.py` may be adjusted by
  Codex C if tests and handoff clearly document the final CLI shape.
- The implementation must normalize coverage XML file paths without making the
  checker depend on the advisory report helper as a runtime enforcement
  dependency.
- If `origin/main` advances before Codex C starts, the #635 retry evidence
  becomes historical and Codex C must remeasure before proceeding.
- Workflow-surface scanner warnings are possible if CI files change; those
  warnings are expected only when the changes remain exactly within this
  contract.

## Next Workflow Action

Next recommended role: Codex C: Module Implementer / comparison thread.

Codex C should compare current coverage tooling to this contract, confirm
fresh-base preconditions, implement the smallest floor-checker/local/CI
changes, add focused tests, and produce the implementation handoff. If
fresh-base preconditions fail, Codex C must stop and report the block instead
of changing thresholds.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/625

Related threshold issue:
https://github.com/Tahjali11/Mythic-Edge/issues/632

Completed retry-gate issue:
https://github.com/Tahjali11/Mythic-Edge/issues/635

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Contract:
docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md

Goal:
Implement the first narrow protected-surface line coverage floor for
parser_state_final_reconciliation.

Approved candidate files:
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py

Approved floor:
- 88.00% line coverage, required per candidate file
- group status passes only when every required file is measured and at or above 88.00%
- branch coverage remains advisory-only
- global 85.00% Python line floor remains unchanged

Before editing:
- Confirm branch and git status.
- Confirm branch is synchronized with origin/main.
- Read issue #625, #632, #635, tracker #566, and the contract.
- Inspect tools/check_coverage_floor.py, tools/run_repo_checks.ps1, .github/workflows/repo-checks.yml, tests/test_check_coverage_floor.py, tests/test_run_repo_checks_script.py, and pyproject.toml.
- Run a clean full coverage precondition check with .\tools\run_repo_checks.ps1 -Coverage.
- Confirm global line >= 85.00%, models.py >= 90.00%, state.py >= 90.00%, and branch coverage advisory-only before implementation.

Do:
- Extend tools/check_coverage_floor.py as the single enforcement authority for the global floor plus the allow-listed parser_state_final_reconciliation protected-surface floor.
- Keep tools/generate_protected_surface_coverage_report.py advisory-only.
- Wire the same protected-surface floor into tools/run_repo_checks.ps1 -Coverage and GitHub Actions repo checks.
- Add focused tests for pass, fail, missing XML, malformed XML, missing candidate-file data, invalid line-rate, unsupported group, and branch-advisory behavior.
- Produce docs/implementation_handoffs/quality_parser_state_final_reconciliation_coverage_floor_implementation_comparison.md.

Do not:
- Change parser behavior or parser state final reconciliation.
- Change parser event classes, match/game identity, deduplication, fixtures, corpus status, analytics behavior, workbook behavior, webhook behavior, Apps Script behavior, Sheets behavior, OpenAI/AI/coaching behavior, Line Tracer behavior, or production behavior.
- Change pyproject.toml.
- Raise or lower the global 85.00% line floor.
- Enforce branch coverage.
- Add any other protected-surface floor.
- Commit raw coverage artifacts, coverage XML, .coverage files, htmlcov, private logs, generated files, secrets, or local-only artifacts.

Validation:
git status --short --branch
git rev-list --left-right --count HEAD...origin/main
.\tools\run_repo_checks.ps1 -Coverage
py -m pytest -q tests\test_check_coverage_floor.py tests\test_run_repo_checks_script.py
py -m ruff check tools\check_coverage_floor.py tests\test_check_coverage_floor.py tests\test_run_repo_checks_script.py
git diff --check
py tools\check_agent_docs.py
Run changed-file protected-surface and secret/private-marker scans.

Final output must include:
- role performed
- issue/tracker reviewed
- contract used
- current base commit and precondition evidence
- files changed
- implementation shape
- exact CLI/failure behavior
- validation results
- protected-surface and secret/private-marker status
- raw artifact status
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/625"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "Issue #625 plus #635 retry-gate completion evidence"
  target_artifact: "docs/implementation_handoffs/quality_parser_state_final_reconciliation_coverage_floor_implementation_comparison.md"
  contract_artifact: "docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md"
  risk_tier: "Medium-High workflow/validation-gate risk; high protected-surface sensitivity"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/parser-state-coverage-floor-retry-625"
  candidate_group: "parser_state_final_reconciliation"
  candidate_files:
    - "src/mythic_edge_parser/app/models.py"
    - "src/mythic_edge_parser/app/state.py"
  floor_policy:
    metric: "line_coverage_only"
    protected_surface_floor_percent: "88.00"
    global_line_floor_percent: "85.00 unchanged"
    branch_coverage: "advisory_only"
  implementation_shape: "extend tools/check_coverage_floor.py with allow-listed protected-surface group and wire it into local/CI repo checks"
  validation:
    - "git status --short --branch"
    - "git rev-list --left-right --count HEAD...origin/main"
    - ".\\tools\\run_repo_checks.ps1 -Coverage before and after implementation"
    - "py -m pytest -q tests\\test_check_coverage_floor.py tests\\test_run_repo_checks_script.py"
    - "py -m ruff check changed Python files"
    - "git diff --check"
    - "py tools\\check_agent_docs.py"
    - "changed-file protected-surface scan"
    - "changed-file secret/private-marker scan"
  stop_conditions:
    - "Do not implement if global line coverage is below 85.00%."
    - "Do not implement if models.py or state.py is below 90.00% before implementation."
    - "Do not change parser behavior, final reconciliation, match/game identity, deduplication, pyproject.toml, global floor, or branch coverage policy."
    - "Do not add any other protected-surface floor."
    - "Do not commit raw coverage artifacts, private logs, generated files, secrets, or local-only artifacts."
```
