# Quality Second Protected-Surface Coverage Floor Candidate Selection Contract

## Module

`quality_second_protected_surface_coverage_floor_candidate_selection`

Plain English: this contract decides whether Mythic Edge has enough current,
public-safe coverage evidence to select a second protected-surface coverage
floor candidate after the first `parser_state_final_reconciliation` floor
landed. A coverage floor is a validation threshold that can fail a check when
coverage drops below it.

This Codex B pass writes the contract only. It does not run coverage, implement
tooling, change CI, activate a second protected-surface floor, raise the global
line floor, enforce branch coverage, or change parser behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/642
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Previous protected-surface floor issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/625
- Previous protected-surface floor PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/637
- Previous merge commit:
  `6f876a78c5294b58111f43a364596498004fc3eb`
- Contract artifact:
  `docs/contracts/quality_second_protected_surface_coverage_floor_candidate_selection.md`

## Tracker

Tracker #566 remains open for the coverage ratchet and quality-threshold
program. This child issue does not complete the tracker.

## Risk Tier

High workflow/validation-gate risk.

The risk is not runtime product behavior. The risk is using stale or overly
broad coverage evidence to add a brittle validation gate. This contract keeps
the second-floor lane in candidate-selection and remeasurement planning only.

## Owning Layer

Quality / validation tooling.

Coverage tooling owns measured execution evidence for a specific command,
commit/ref, coverage source, coverage XML, report artifact, and threshold
configuration. Coverage does not own parser truth, parser correctness, fixture
truth, corpus readiness, security assurance, privacy assurance, release
readiness, deploy readiness, production readiness, analytics truth, AI truth,
or coaching truth.

## Internal Project Area

Quality / Governance, with protected-surface relationship to Parser and Shared
Support.

## Truth Owner

The committed protected-surface advisory reports own only their measured commit
and command metadata. `tools/check_coverage_floor.py` owns the currently
implemented coverage-floor pass/fail behavior. The parser/state layer owns
parser truth and final reconciliation behavior.

This contract owns only the second-candidate selection decision and the
preconditions for any later remeasurement or implementation child.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
existing global coverage floor
  + first protected-surface floor closeout evidence
  + committed protected-surface advisory reports
  + current base freshness check
  -> second candidate selection contract
  -> later current-base remeasurement child before any floor proposal
```

Forbidden reverse flow:

- candidate selection must not change parser behavior;
- candidate selection must not add validation gates;
- candidate selection must not change CI;
- coverage numbers must not imply parser correctness;
- branch coverage must remain advisory-only;
- stale reports must not authorize a new floor.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/quality_second_protected_surface_coverage_floor_candidate_selection.md`

Future artifacts may be created only by later authorized roles:

- `docs/contract_test_reports/quality_second_protected_surface_coverage_floor_candidate_selection.md`
- a later current-base protected-surface remeasurement issue/contract;
- a later second-floor implementation contract, only if fresh evidence selects
  a candidate and the owner authorizes implementation.

This contract does not authorize edits to:

- `.github/workflows/repo-checks.yml`;
- `pyproject.toml`;
- `tools/check_coverage_floor.py`;
- `tools/generate_protected_surface_coverage_report.py`;
- `tools/run_repo_checks.ps1`;
- parser, analytics, workbook, webhook, Apps Script, Google Sheets, OpenAI,
  AI, coaching, Line Tracer, production, fixtures, corpus, or runtime code.

## Source Artifacts Inspected

- Issue #642
- Tracker #566
- Project roadmap #568
- Issue #625 and PR #637
- `docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md`
- `docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md`
- `docs/contracts/quality_parser_state_final_reconciliation_coverage_floor_implementation.md`
- `docs/contract_test_reports/quality_parser_state_final_reconciliation_coverage_floor_implementation.md`
- `docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json`
- `tools/check_coverage_floor.py`
- `tools/generate_protected_surface_coverage_report.py`
- `tests/test_check_coverage_floor.py`
- `tests/test_protected_surface_coverage_report.py`
- current branch state on `origin/main`

## Observed Current Behavior

Current base observed for this contract:

```yaml
branch: "codex/quality-second-protected-surface-coverage-candidate-642"
base_ref: "origin/main"
head_commit: "f4234ed"
head_summary: "Merge pull request #641 from Tahjali11/codex/security-quality-evidence-bundle-639"
previous_verified_merge_commit: "6f876a78c5294b58111f43a364596498004fc3eb"
```

Current coverage posture:

```yaml
global_python_line_floor_percent: 85.00
first_protected_surface_floor_group: "parser_state_final_reconciliation"
first_protected_surface_floor_percent: 88.00
first_protected_surface_floor_status: "landed"
branch_coverage_status: "advisory_only"
second_protected_surface_floor_authorized: false
global_line_floor_increase_authorized: false
branch_coverage_enforcement_authorized: false
```

The latest broad committed protected-surface advisory report inspected by this
contract is:

```yaml
report: "docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json"
measured_commit: "94d337c635769c214c5beecabef93932033210f3"
global_line_coverage_percent: 87.55
global_branch_coverage_percent: 74.80
global_line_floor_status: "passed"
branch_coverage_status: "advisory_only"
protected_surface_floor_status: "not_authorized"
```

The first protected-surface floor closeout for #625 / PR #637 recorded:

```yaml
global_line_coverage_percent: 87.64
parser_state_final_reconciliation_minimum_required_file_line_percent: 90.45
models_py_line_coverage_percent: 90.45
state_py_line_coverage_percent: 92.96
branch_coverage_percent: 74.86
branch_coverage_posture: "advisory_only"
```

Important freshness observation:

- The broad protected-surface report was measured at `94d337c`.
- The current base is `f4234ed`.
- Since `94d337c`, the repo has changed coverage tooling, CI workflow wiring,
  tests, local app security surfaces, extractor tests, diagnostics tests, and
  security-quality report artifacts.
- Since #625 merged at `6f876a7`, current `origin/main` also includes later
  quality/security work and test changes.

These changes are not evidence of breakage. They are enough to make the old
broad protected-surface report stale for selecting or implementing a second
floor.

## Problem Statement And First Bad Value

The first bad value would be treating the landed
`parser_state_final_reconciliation` floor as permission to add another
protected-surface floor from stale measurements.

Specific bad values:

- using the `94d337c` broad report as if it measured current `origin/main`;
- selecting a second floor while tests and coverage tooling have changed since
  the report;
- using group averages while ignoring file-level minimums;
- using branch coverage as a gate;
- raising the global `85.00%` line floor as part of this child;
- treating coverage as parser truth or readiness.

## Candidate Selection Verdict

Decision:

```yaml
candidate_status: "needs_current_base_remeasurement_first"
second_floor_candidate_selected_now: false
future_candidate_priority_recorded: true
coverage_execution_authorized_now: false
floor_implementation_authorized_now: false
ci_change_authorized_now: false
branch_coverage_enforcement_authorized_now: false
global_line_floor_increase_authorized_now: false
```

Rationale:

- Existing broad protected-surface evidence is useful for ranking and planning.
- Existing evidence is stale for selecting or activating a second floor because
  it predates later merges, tooling updates, and test changes.
- The first floor closeout proves only the first
  `parser_state_final_reconciliation` group remained healthy under its narrow
  gate. It does not remeasure all other protected-surface groups.
- A second floor should be selected only from a fresh current-base
  protected-surface advisory report.

## Candidate Status Vocabulary

Allowed statuses for this lane:

- `selected_for_future_floor_proposal`
- `needs_current_base_remeasurement_first`
- `parked_until_test_hardening`
- `not_ready`
- `superseded_by_global_floor_policy`

Meaning:

- `selected_for_future_floor_proposal`: fresh current-base evidence supports a
  narrow line-only candidate, but implementation still requires a later issue.
- `needs_current_base_remeasurement_first`: existing evidence is useful but
  stale or incomplete; remeasure before candidate selection or implementation.
- `parked_until_test_hardening`: the candidate surface is important but current
  coverage is too thin or uneven for a floor.
- `not_ready`: the group is too broad, ambiguous, low, or unsuitable for a
  floor under current policy.
- `superseded_by_global_floor_policy`: a group-specific floor would add no
  value beyond the active global line floor or a separately approved policy.

This contract sets the lane status to
`needs_current_base_remeasurement_first`.

## Evidence Freshness Rules

Fresh evidence for a second floor must satisfy all of these conditions:

1. The report is generated from the intended base branch or exact candidate
   branch after fetching `origin/main`.
2. The report records a measured commit equal to the reviewed current base or
   a commit explicitly named by the next issue.
3. The report is committed as a public-safe JSON artifact under
   `docs/quality_reports/coverage/protected_surface/`.
4. The report records `global_line_floor_status: passed`.
5. The report records `branch_coverage_status: advisory_only`.
6. The report records `protected_surface_floor_authorized: false` unless a
   later issue explicitly changes that field for implementation.
7. The report contains no raw coverage XML, local absolute paths, private
   paths, raw logs, secrets, workbook exports, SQLite data, or generated
   private artifacts.
8. The report includes all measurable groups from
   `tools/generate_protected_surface_coverage_report.py`, or explains any
   public-safe omitted group with `coverage_scope_status`.

Evidence is stale when:

- the measured commit predates a merge that changes tests, coverage tooling,
  source files in candidate groups, or CI coverage command wiring;
- the report predates activation of a prior protected-surface floor;
- the report's measured ref differs from the intended implementation base
  without a reviewer-approved explanation;
- a later contract changed candidate vocabulary or group membership.

## Existing Evidence Interpretation

The `94d337c` report remains useful planning evidence. It must not be used as
current-base proof for a second floor.

Planning summary from the stale report:

| Group | Files | Average line | Minimum line | Current contract interpretation |
| --- | ---: | ---: | ---: | --- |
| `parser_event_classes` | 1 | 100.00% | 100.00% | `watch_list_single_file` |
| `parser_state_final_reconciliation` | 2 | 90.33% | 90.21% | `already_has_floor` |
| `extractor_behavior` | 1 | 94.41% | 94.41% | `provisional_priority_after_remeasurement` |
| `match_game_identity` | 28 | 97.08% | 83.08% | `promising_but_broad_needs_subgroup_or_hardening` |
| `workbook_schema_and_exports` | 3 | 93.34% | 83.08% | `parked_until_transforms_hardening_or_subgrouping` |
| `webhook_payload_and_transport` | 3 | 83.73% | 76.65% | `parked_until_test_hardening` |
| `environment_runtime_python_paths` | 1 | 100.00% | 100.00% | `watch_list_single_file` |
| `analytics_schema_and_ingest` | 5 | 80.62% | 45.19% | `not_ready` |
| `local_app_security_and_artifact_safety` | 16 | 89.64% | 80.19% | `parked_until_subgrouping_or_hardening` |

The non-measurable groups remain outside the current Python coverage source:

- `apps_script_behavior`
- `workflow_authority_docs`
- `workflow_ci_yaml`
- `local_artifact_checker_tools`
- `forbidden_local_artifact_paths`

## Provisional Candidate Priority

If a fresh current-base remeasurement confirms the old ordering, the next
candidate discussion should start with:

```yaml
first_remeasurement_priority: "extractor_behavior"
candidate_posture: "single_file_line_only_candidate_requires_explicit_rationale"
candidate_file: "src/mythic_edge_parser/app/extractors.py"
stale_report_line_coverage_percent: 94.41
suggested_status_after_fresh_confirmation: "selected_for_future_floor_proposal"
```

Why `extractor_behavior` is the provisional first priority:

- it maps to a protected parser surface;
- the stale report shows strong line coverage;
- it has a clear owning file and a clear protected-surface category;
- it does not add another broad overlapping group before the repo proves the
  second-floor workflow can handle a single additional surface cleanly.

Why it is not selected now:

- it is a one-file group, so it needs explicit single-file-floor rationale;
- extractor tests changed after the report commit, so the stale percentage is
  not current evidence;
- a fresh report may change the line percentage or reveal grouping drift.

Watch-list alternatives after fresh remeasurement:

- `parser_event_classes`: high stale coverage but one-file surface, and a
  floor may add little beyond existing tests.
- `environment_runtime_python_paths`: high stale coverage but one-file config
  surface; should be considered only if runtime path safety is explicitly
  selected.
- `match_game_identity`: important and broad, but should be split or hardened
  before a floor because the stale minimum is only `83.08%` and the group
  overlaps with already floored parser state surfaces.

## Overlap Handling

Second-floor selection must handle overlap explicitly:

- A file already protected by the first floor must not be counted as new second
  floor protection unless the new group adds clear distinct value.
- `state.py` is already part of the first
  `parser_state_final_reconciliation` floor.
- `transforms.py` appears in multiple broad groups and has lower stale line
  coverage than several group averages; it must not be hidden by averages.
- Broad groups such as `match_game_identity` should prefer subgrouping or
  file-minimum hardening before floor activation.

Future candidate contracts must list:

- candidate group ID;
- candidate required files;
- files already covered by prior protected-surface floors;
- shared files across candidate groups;
- whether the floor adds new signal beyond existing gates;
- whether the pass rule uses every-file minimum, group minimum, or both.

## Allowed Metric Scope

Allowed for future second-floor discussion:

- Python line coverage only;
- per-file minimum line coverage;
- group reported percentage as the minimum required-file line coverage;
- public-safe repo-relative file paths;
- branch coverage displayed as advisory-only.

Forbidden in this lane:

- branch coverage enforcement;
- global line floor increase;
- arbitrary path threshold policy loading;
- broad protected-surface floor activation;
- non-Python coverage floors;
- docs, workflow YAML, Apps Script, local artifact, or generated artifact
  coverage floors.

## Stop Conditions Before Implementation

Stop before any later Codex C implementation if:

- no fresh current-base protected-surface advisory report exists;
- the fresh report does not pass the global `85.00%` line floor;
- branch coverage is not explicitly advisory-only;
- the selected candidate has any required file below the later contract's
  minimum precondition;
- the selected candidate depends on files already covered by the first floor
  without a clear new-signal rationale;
- the selected group is broad and hides weak file-level coverage behind a high
  average;
- the proposed implementation would edit parser behavior, fixtures, corpus
  metadata, workbook/webhook/App Script behavior, analytics, OpenAI/runtime,
  production behavior, or private artifacts;
- the proposed implementation would change CI, `pyproject.toml`, or
  `tools/check_coverage_floor.py` without a later issue explicitly authorizing
  that implementation.

## Validation Evidence Required Before Later Implementation

Before any later implementation child may be framed, a current-base
remeasurement child must produce:

- a committed public-safe protected-surface advisory report for current
  `origin/main` or the explicitly named implementation base;
- a contract-test report reviewing that advisory report;
- a selected candidate status from fresh evidence;
- a candidate file list and minimum file line coverage;
- branch coverage marked advisory-only;
- raw coverage artifacts confirmed local/ignored/uncommitted;
- protected-surface and secret/private-marker scans for committed report files.

Suggested later validation commands must be defined by that later issue. This
contract does not authorize running them now.

## Protected Boundaries

This contract preserves:

- existing global line floor: `85.00%`;
- first protected-surface floor:
  `parser_state_final_reconciliation` at `88.00%`;
- branch coverage as advisory-only;
- no second protected-surface floor authorization;
- no CI change authorization;
- no parser behavior change authorization;
- no production readiness, deploy readiness, release readiness, parser truth,
  corpus readiness, security assurance, privacy assurance, analytics truth,
  AI truth, or coaching truth claims.

## Future Candidate Handoff Policy

The next workflow should not route directly to implementation. It should route
to either:

1. Codex E review of this contract; then
2. Codex A for a current-base protected-surface remeasurement child, if the
   contract is approved.

Only after that remeasurement child lands may a later child select or implement
the second floor.

## Acceptance Criteria

- The contract sets the current lane status to
  `needs_current_base_remeasurement_first`.
- The contract records why existing reports are useful but stale.
- The contract records provisional candidate priority without selecting a
  second floor now.
- The contract preserves global and first protected-surface floors unchanged.
- The contract keeps branch coverage advisory-only.
- The contract forbids implementation, coverage execution, CI changes, and
  parser behavior changes in this pass.
- Validation confirms the contract is public-safe and whitespace clean.

## Next Workflow Action

Next role: Codex E reviewer.

Codex E should review whether the freshness decision is correct and whether
the provisional `extractor_behavior` priority is safe to preserve as planning
guidance without selecting a floor.

Pasteable Codex E prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for issue #642.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/642

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/625

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/637

Artifact to review:
docs/contracts/quality_second_protected_surface_coverage_floor_candidate_selection.md

Review focus:
- whether `needs_current_base_remeasurement_first` is the correct decision;
- whether existing reports are correctly treated as stale planning evidence;
- whether provisional `extractor_behavior` priority is safe and non-authorizing;
- whether branch coverage remains advisory-only;
- whether global floor, first protected-surface floor, CI, parser behavior, and protected surfaces remain unchanged;
- whether the next route should be Codex A for a current-base remeasurement child after review.

Protected boundaries:
- Do not implement code.
- Do not run coverage.
- Do not change CI.
- Do not activate a second protected-surface floor.
- Do not raise the global line floor.
- Do not enforce branch coverage.
- Do not change parser behavior or parser truth ownership.
- Do not claim readiness, assurance, or parser truth.

Expected output:
- Findings first, if any.
- Review verdict.
- Validation evidence reviewed.
- Recommended next role.
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/642"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/625"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/637"
  completed_thread: "B"
  next_thread: "E"
  verdict: "second_protected_surface_candidate_selection_contract_needs_current_base_remeasurement_first"
  risk_tier: "High"
  base_branch: "main"
  branch: "codex/quality-second-protected-surface-coverage-candidate-642"
  target_artifact: "docs/contracts/quality_second_protected_surface_coverage_floor_candidate_selection.md"
  candidate_status: "needs_current_base_remeasurement_first"
  provisional_candidate_priority: "extractor_behavior"
  implementation_authorized: false
  coverage_execution_authorized: false
  ci_change_authorized: false
  second_protected_surface_floor_authorized: false
  global_line_floor_increase_authorized: false
  branch_coverage_enforcement_authorized: false
  parser_behavior_change_authorized: false
  validation:
    - "python3 tools/check_agent_docs.py"
    - "python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin < target artifact"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "git diff --check"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not run coverage."
    - "Do not change CI or pyproject.toml."
    - "Do not activate a second protected-surface floor."
    - "Do not raise the global line floor."
    - "Do not enforce branch coverage."
    - "Do not change parser behavior or parser truth ownership."
    - "Do not commit raw coverage XML, local artifacts, private paths, raw logs, secrets, workbook exports, or generated private artifacts."
```
