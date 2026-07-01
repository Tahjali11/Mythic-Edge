# Quality Protected-Surface Coverage Candidate Floor Policy Contract

## Module

`quality_protected_surface_coverage_candidate_floor_policy`

Plain English: this contract interprets Mythic Edge's first advisory
protected-surface coverage report and defines how future protected-surface
coverage floors may be considered. A coverage floor is a threshold below which
a validation command could fail. This contract does not add any such floor.

This is a Codex B contract artifact only. It does not implement code, change
CI, change coverage settings, add a protected-surface floor, raise the global
85.00% line floor, enforce branch coverage, or change product behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/612
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Completed global 85.00% line floor issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/595
- Completed global 85.00% line floor PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/604
- Completed protected-surface advisory report issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/605
- Completed protected-surface advisory report PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/609
- Contract artifact:
  `docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md`

## Tracker

Tracker #566 remains open for coverage-ratchet work. This child issue does not
complete the tracker.

## Owning Layer

Quality and validation tooling.

Coverage tooling owns measured execution evidence for a specific command,
coverage source, ref/commit, report artifact, and coverage configuration.
Coverage does not own parser truth, protected-surface authorization, parser
correctness, security assurance, privacy assurance, release readiness, deploy
readiness, production readiness, analytics truth, AI truth, or coaching truth.

## Internal Project Area

Quality / validation gates.

## Truth Owner

The #605 advisory report owns only public-safe coverage measurement metadata
for the measured ref and command. `tools/check_protected_surfaces.py` owns
protected-surface path classification. The parser/state layer owns parser
truth. This contract owns only the interpretation policy for future floor
consideration.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
global coverage gate evidence
  + protected-surface advisory coverage report
  + protected-surface category vocabulary
  -> candidate-floor interpretation policy
  -> later issue-specific floor proposal, if explicitly authorized
```

Forbidden reverse flow:

- Coverage numbers must not authorize protected-surface code changes.
- Coverage numbers must not imply parser correctness.
- Coverage numbers must not imply security assurance, privacy assurance,
  release readiness, deploy readiness, production readiness, analytics truth,
  AI truth, or coaching truth.
- Candidate-floor policy must not change CI or the active global coverage gate.

## Files Owned By This Contract

- `docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md`

Future artifacts may be created only by later authorized roles:

- `docs/implementation_handoffs/quality_protected_surface_coverage_candidate_floor_policy_comparison.md`
- `docs/contract_test_reports/quality_protected_surface_coverage_candidate_floor_policy.md`

This contract does not authorize edits to:

- `.github/workflows/repo-checks.yml`
- `pyproject.toml`
- `tools/run_repo_checks.ps1`
- `tools/check_coverage_floor.py`
- `tools/generate_protected_surface_coverage_report.py`
- parser, analytics, workbook, webhook, Apps Script, Google Sheets, OpenAI,
  AI, coaching, Line Tracer, or production code.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #612
- Tracker #566
- Project roadmap #568
- Issue #595 and PR #604
- Issue #605 and PR #609
- `docs/contracts/quality_coverage_global_line_floor_enforcement_readiness.md`
- `docs/contract_test_reports/quality_coverage_global_line_floor_enforcement_readiness.md`
- `docs/contracts/quality_protected_surface_coverage_floor_readiness.md`
- `docs/implementation_handoffs/quality_protected_surface_coverage_floor_readiness_comparison.md`
- `docs/contract_test_reports/quality_protected_surface_coverage_floor_readiness.md`
- `docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json`
- `tools/generate_protected_surface_coverage_report.py`
- `tests/test_protected_surface_coverage_report.py`
- `tools/check_coverage_floor.py`
- `tools/check_protected_surfaces.py`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`

## Observed Current Behavior

Current coverage posture:

- #595 / PR #604 implemented the blocking 85.00% global Python line coverage
  floor.
- Branch coverage remains advisory-only.
- #605 / PR #609 implemented a public-safe advisory protected-surface coverage
  report.
- The #605 report records:
  - `schema_version: protected_surface_coverage_advisory.v1`;
  - `measured_commit: 83d3141e953913233e3457b910c2c83ff25d44aa`;
  - `global_line_coverage_percent: 87.55`;
  - `global_branch_coverage_percent: 74.80`;
  - `global_line_floor_status: passed`;
  - `branch_coverage_status: advisory_only`;
  - `protected_surface_floor_status: not_authorized`;
  - `protected_surface_floor_authorized: false`;
  - `global_line_floor_increase_authorized: false`;
  - `branch_coverage_enforcement_authorized: false`;
  - `advisory_only: true`.
- The current branch is synced with `origin/main` at `62bc9c2`.
- The #605 advisory report remains keyed to `83d3141`, so it is valid
  committed evidence but stale for direct floor activation on current
  `origin/main`.

## Report Interpretation Model

The #605 advisory report should be interpreted as:

- public-safe measurement evidence;
- a grouping map for protected/protected-adjacent surfaces;
- a source of candidate-floor discussion;
- a way to identify weak or uneven areas;
- not a floor proposal by itself;
- not approval to change CI or coverage settings;
- not proof of parser correctness, security assurance, privacy assurance, or
  release readiness.

Allowed interpretation labels:

- `promising`: measured line coverage is strong enough to consider future
  candidate-floor work after fresh evidence and review.
- `caution`: measured evidence is useful but too small, overlapping, uneven, or
  close to the current global floor for direct promotion.
- `not_ready`: current evidence should not support a floor proposal without
  remediation, regrouping, or more focused tests.
- `not_applicable`: Python line coverage is not the right evidence model for
  this group.
- `insufficient_evidence`: the report does not provide enough current,
  measured, or stable data to classify readiness.

These labels are advisory. They must not fail CI or block work by themselves.

## Candidate Floor Readiness Verdict

No protected-surface floor is ready to become blocking from the #605 report.

The report is strong enough to define future policy and to identify promising
candidate inputs. It is not strong enough to authorize any protected-surface
floor because:

- the evidence is now stale relative to current `origin/main`;
- several groups are tiny one-file samples;
- several groups overlap through shared files such as `state.py` and
  `transforms.py`;
- some broader groups have low outliers;
- branch coverage remains too uneven and must stay advisory-only;
- non-Python and outside-source groups need other evidence models.

Recommended posture:

```yaml
protected_surface_floor_status: "not_authorized"
future_floor_policy_status: "candidate_policy_defined"
next_floor_implementation_status: "deferred_to_later_issue_and_explicit_approval"
line_coverage_floor_input: "allowed_for_future_candidates"
branch_coverage_floor_input: "not_allowed_advisory_only"
```

## Promising Groups

Promising groups may be used as inputs to a future candidate-floor discussion,
but not as direct blocking gates from this contract.

| Group | Evidence | Policy interpretation |
| --- | --- | --- |
| `parser_state_final_reconciliation` | 2 files, average line 90.33%, minimum line 90.21% | Best future candidate for a small protected parser-state floor, after fresh-base remeasurement and overlap review. |
| `match_game_identity` | 28 files, average line 97.08%, minimum line 83.08% | Strong broad parser group, but any floor must handle file-level outliers and overlap with `state.py`/`transforms.py`. |
| `extractor_behavior` | 1 file, line 94.41% | Good single-file signal; too small for a group floor without explicit single-file rationale. |
| `workbook_schema_and_exports` | 3 files, average line 93.34%, minimum line 83.08% | Promising for transport/schema visibility, but `transforms.py` makes the minimum low enough to require caution. |

Future policy for promising groups:

- prefer conservative group-level line floors only after repeated current-base
  evidence;
- require a file-minimum review so group averages do not hide weak files;
- require explicit overlap handling when the same file appears in multiple
  groups;
- require Codex E review before any floor proposal reaches implementation.

## Caution Groups

Caution groups are useful measurement surfaces, but current evidence is not
enough for a blocking floor proposal.

| Group | Evidence | Caution reason |
| --- | --- | --- |
| `parser_event_classes` | 1 file, line 100.00% | Tiny one-file surface. A floor could be useful later, but it would mostly pin one existing file. |
| `environment_runtime_python_paths` | 1 file, line 100.00% | Tiny one-file surface. Useful as regression visibility, not enough for a broader policy. |
| `local_app_security_and_artifact_safety` | 16 files, average line 89.64%, minimum line 80.19% | Broad and useful, but uneven. Several files sit near 80-86%, so a floor needs remediation or subgrouping. |
| `webhook_payload_and_transport` | 3 files, average line 83.73%, minimum line 76.65% | Important surface, but currently below or near the global floor; should not receive a blocking floor yet. |

Caution groups should route to one of:

- focused test-hardening issue;
- subgroup definition issue;
- repeat advisory measurement after related work;
- watch-list status if a floor would add more ceremony than protection.

## Not-Ready Groups

| Group | Evidence | Not-ready reason |
| --- | --- | --- |
| `analytics_schema_and_ingest` | 5 files, average line 80.62%, minimum line 45.19% | Too uneven for a floor. `analytics_sidecar.py` at 45.19% makes a candidate floor premature. |

Future work for not-ready groups should start with interpretation/remediation,
not a gate. The goal should be to understand whether the low file is thin glue,
legacy/deferred behavior, missing tests, or an incorrectly grouped surface.

## Not-Applicable Groups

These groups must not receive Python line coverage floors under the current
coverage source:

| Group | Reason |
| --- | --- |
| `apps_script_behavior` | Apps Script is not Python and is outside `src/mythic_edge_parser`. |
| `workflow_authority_docs` | Governance docs are not executable Python coverage targets. |
| `workflow_ci_yaml` | GitHub workflow YAML is not Python coverage. |
| `local_artifact_checker_tools` | Current Python coverage source is `src/mythic_edge_parser`, while these tools are under `tools/`. |
| `forbidden_local_artifact_paths` | Local/generated/private artifact paths are not source coverage targets and must not be committed. |

Not-applicable groups need other evidence:

- Apps Script tests or deployment review for Apps Script behavior;
- docs checks and contract review for authority docs;
- workflow validation and GitHub Actions evidence for CI YAML;
- tool-specific pytest and Ruff validation for `tools/`;
- protected-surface and secret/private-marker scans for forbidden local
  artifacts.

## Future Floor Shape Policy

No floor shape is authorized now.

If a later issue proposes a protected-surface floor, the preferred order is:

1. Group-level line floor for a small, stable, clearly owned group.
2. Group-level floor plus file-minimum guard for larger groups.
3. Single-file floor only for a critical, stable, explicitly owned file.
4. Per-internal-project-area floor only after multiple group reports show
   stable ownership and low noise.

Avoid first:

- repo-wide protected-surface mega-floor;
- broad internal-project-area floors;
- branch coverage floors;
- floor proposals driven by one stale report;
- floors for not-applicable groups;
- floors that would require changing the coverage source in `pyproject.toml`.

## Line Coverage Policy

Line coverage is the only metric allowed for future protected-surface floor
candidates in the next policy step.

Requirements:

- use the same coverage source family as the current global gate unless a
  later contract explicitly changes it;
- measure current intended base before floor proposal;
- name group average, group minimum, file count, and missing-file count;
- keep raw artifacts local/ignored;
- use public-safe committed summaries only;
- distinguish `measured`, `missing_from_coverage_xml`, and
  `not_applicable_current_coverage_scope`.

No future line floor may be proposed from a stale report alone.

## Branch Coverage Policy

Branch coverage remains advisory-only.

Branch coverage may be shown in reports, reviewed as a risk signal, and used to
prioritize tests. It must not:

- fail CI;
- define a threshold;
- serve as a protected-surface floor input;
- override line coverage status;
- block PRs;
- imply parser correctness, security assurance, privacy assurance, release
  readiness, deploy readiness, production readiness, analytics truth, AI truth,
  or coaching truth.

## Minimum Evidence Before Future Floor

A later protected-surface floor proposal requires all of the following:

1. A new scoped issue and Codex B contract.
2. Explicit user approval for any blocking or CI behavior.
3. Fresh advisory report on the intended base ref/commit.
4. Current global 85.00% line floor still passing.
5. Candidate group has `coverage_scope_status: measured`.
6. Candidate group has no missing measurable files unless each missing file has
   a documented exclusion.
7. Candidate group has a stable deterministic mapping covered by focused tests.
8. Candidate group has group average, group minimum, file count, branch
   advisory data, and outlier notes.
9. Candidate threshold is lower than the measured minimum or has a documented
   remediation issue for each below-threshold file.
10. Overlapping files are documented so one weak file is not hidden or double
    counted.
11. Raw coverage artifacts are ignored/local and not committed.
12. Failure messaging explains the floor, measured value, stale-ref policy,
    branch advisory-only status, and remediation route.
13. Codex E verifies no readiness, security/privacy, parser-truth, analytics,
    AI, coaching, deploy, release, or production claims are being made.
14. Codex G requires fresh CI or current-base validation before merge.

## Explicit Blockers For Floor Promotion

Any one of these blocks a future protected-surface floor proposal:

- stale measurement without owner-approved use as historical context only;
- branch coverage used as the threshold;
- proposed floor for `not_applicable_current_coverage_scope` groups;
- proposed floor for `analytics_schema_and_ingest` without remediation or
  regrouping;
- proposed floor for `webhook_payload_and_transport` without addressing the
  76.65% minimum file and 83.73% group average;
- group average used without file-minimum review;
- group map changed without focused tests;
- raw coverage XML, `.coverage`, HTML coverage output, or raw terminal logs
  included in tracked files;
- coverage source changed in `pyproject.toml` without a separate contract;
- CI workflow changed without explicit authorization;
- protected-surface checker or secret/private-marker scanner weakened;
- parser, analytics, workbook, webhook, Apps Script, Sheets, OpenAI, AI,
  coaching, Line Tracer, or production behavior changed to satisfy coverage;
- claims of parser correctness, security assurance, privacy assurance, release
  readiness, deploy readiness, production readiness, analytics truth, AI truth,
  or coaching truth based on coverage.

## Validation Requirements

For this Codex B contract:

```powershell
git diff --check -- docs\contracts\quality_protected_surface_coverage_candidate_floor_policy.md
py tools\check_agent_docs.py
@'
docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

For a later Codex C policy-comparison or implementation thread:

- confirm branch/ref freshness;
- parse the #605 advisory report JSON;
- confirm no raw coverage artifacts are tracked;
- confirm no CI, coverage settings, or helper behavior changes unless a later
  issue explicitly authorizes them;
- produce a comparison handoff;
- if any code/report-helper change is authorized later, run focused tests,
  Ruff on changed Python files, JSON validation for generated reports,
  `git diff --check`, `py tools/check_agent_docs.py`, and path-scoped
  protected-surface and secret/private-marker scans.

For Codex E:

- review that the interpretation labels match the measured report;
- verify no floor or CI change was introduced;
- verify stale-report caveats are preserved;
- verify branch coverage remains advisory-only;
- verify non-claims are present.

For Codex G:

- require current-base evidence before any future floor merge;
- confirm tracker #566 remains open unless the whole coverage queue is
  complete;
- do not close a future floor issue as implemented from policy text alone.

## Protected-Surface Assessment

This contract is docs-only and does not touch protected runtime surfaces.

Protected surfaces preserved:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity and deduplication;
- analytics schema and ingest behavior;
- workbook schema;
- webhook payload shape;
- Apps Script and Google Sheets behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- production behavior;
- fixtures, corpus status, raw logs, generated data, runtime files, failed
  posts, workbook exports, secrets, credentials, private paths, and local-only
  artifacts.

Workflow validation surfaces remain protected. Future CI or coverage-gate work
requires a separate issue, contract, implementation handoff, review, and
explicit user approval.

## Acceptance Criteria

- Contract artifact exists at
  `docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md`.
- The #605 advisory report is interpreted as advisory evidence only.
- The contract classifies promising, caution, not-ready, and not-applicable
  groups.
- No protected-surface floor is authorized.
- Line coverage is the only allowed future floor metric input.
- Branch coverage remains advisory-only.
- Minimum future evidence is defined.
- Explicit blockers for floor promotion are defined.
- Validation expectations are defined for Codex C/E/G.
- Protected-surface and non-claim boundaries are preserved.

## Next Workflow Action

Next recommended role: Codex E for contract-test review, or Codex A for a new
follow-up issue if the owner wants to pursue one specific candidate group.

No immediate Codex C floor implementation is appropriate from this contract.
If the owner explicitly asks for a later implementation-style comparison
thread, use the prompt below as a comparison-only Codex C handoff.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison-only thread.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/612

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Contract:
docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md

Primary evidence:
docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json

Goal:
Compare the current protected-surface coverage advisory report, helper, tests,
global coverage gate, and CI configuration against the candidate-floor policy
contract. Produce:
docs/implementation_handoffs/quality_protected_surface_coverage_candidate_floor_policy_comparison.md

This is comparison-only unless the user explicitly authorizes a new
implementation slice.

Do:
- Confirm branch and git status.
- Parse the advisory report and verify the contract classifications.
- Confirm the global 85.00% line floor remains unchanged.
- Confirm branch coverage remains advisory-only.
- Confirm no protected-surface floor is active.
- Identify the most sensible next issue route, if any.

Do not:
- Change CI.
- Add a protected-surface coverage floor.
- Raise the global 85.00% line floor.
- Enforce branch coverage.
- Change pyproject.toml coverage settings.
- Change the protected-surface coverage report helper unless a later issue explicitly authorizes it.
- Run coverage unless explicitly authorized.
- Commit raw coverage artifacts.
- Change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.
- Claim parser correctness, security assurance, privacy assurance, release readiness, deploy readiness, production readiness, analytics truth, AI truth, or coaching truth from coverage numbers.

Validation:
- py -m json.tool docs\quality_reports\coverage\protected_surface\2026-07-01-83d3141-protected-surface-coverage-advisory.json
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- advisory report interpreted
- group classifications confirmed or corrected
- floor readiness verdict
- validation results
- protected-surface status
- raw artifact status
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/612"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "E_or_A"
  source_artifact: "docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json"
  contract_artifact: "docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md"
  optional_target_artifact: "docs/implementation_handoffs/quality_protected_surface_coverage_candidate_floor_policy_comparison.md"
  risk_tier: "High workflow and validation-gate policy risk; low runtime risk"
  branch: "codex/protected-surface-coverage-interpretation-566"
  base_branch: "main"
  target_branch: "main_after_explicit_user_approval"
  decision: "No protected-surface coverage floor is ready to become blocking from the #605 advisory report. Candidate policy is defined; implementation is deferred to a later issue and explicit authorization."
  line_coverage_policy: "line coverage is the only allowed future floor input"
  branch_coverage_policy: "advisory_only"
  promising_groups:
    - "parser_state_final_reconciliation"
    - "match_game_identity"
    - "extractor_behavior"
    - "workbook_schema_and_exports"
  caution_groups:
    - "parser_event_classes"
    - "environment_runtime_python_paths"
    - "local_app_security_and_artifact_safety"
    - "webhook_payload_and_transport"
  not_ready_groups:
    - "analytics_schema_and_ingest"
  not_applicable_groups:
    - "apps_script_behavior"
    - "workflow_authority_docs"
    - "workflow_ci_yaml"
    - "local_artifact_checker_tools"
    - "forbidden_local_artifact_paths"
  validation:
    - "git diff --check -- docs\\contracts\\quality_protected_surface_coverage_candidate_floor_policy.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan"
    - "path-scoped secret/private-marker scan"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not change CI."
    - "Do not add a protected-surface coverage floor."
    - "Do not raise the global 85.00% line floor."
    - "Do not enforce branch coverage."
    - "Do not change pyproject.toml coverage settings."
    - "Do not change the existing protected-surface coverage report helper."
    - "Do not commit raw coverage artifacts."
    - "Do not claim parser correctness, security assurance, privacy assurance, release readiness, deploy readiness, production readiness, analytics truth, AI truth, or coaching truth from coverage numbers."
    - "Do not change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
