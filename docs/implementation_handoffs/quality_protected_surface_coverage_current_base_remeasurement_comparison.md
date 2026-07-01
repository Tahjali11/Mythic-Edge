# Quality Protected-Surface Coverage Current-Base Remeasurement Comparison

## Role Performed

Codex C: Module Implementer / report-only measurement and comparison thread.

## Issue And Tracker

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/617
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568

## Source Artifacts Used

- GitHub issue #617
- `docs/contracts/quality_protected_surface_coverage_floor_readiness.md`
- `docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md`
- `docs/contract_test_reports/quality_protected_surface_coverage_candidate_floor_policy.md`
- `docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json`
- `tools/generate_protected_surface_coverage_report.py`
- `tools/check_coverage_floor.py`
- `tests/test_protected_surface_coverage_report.py`

## Approval Record Applied

```yaml
protected_surface_coverage_measurement_authorized: true
report_artifact_creation_authorized: true
measured_ref: "origin/main"
measured_commit: "94d337c635769c214c5beecabef93932033210f3"
raw_coverage_artifacts_committed: false
raw_coverage_artifacts_local_only: true
protected_surface_floor_authorized: false
global_line_floor_increase_authorized: false
branch_coverage_enforcement_authorized: false
ci_change_authorized: false
```

## Branch And Git Status

- Worktree: `MythicEdge-coverage-next-566`
- Branch: `codex/coverage-next-ratchet-566`
- Base ref measured: `origin/main`
- Measured commit: `94d337c635769c214c5beecabef93932033210f3`
- Branch and `origin/main` were synced at measurement time.
- Dirty set after report/handoff creation:
  - new advisory report JSON;
  - this implementation handoff.

## What Was Measured

Ran the existing approved coverage command family against current `origin/main`
and generated a public-safe protected-surface advisory report from the local
coverage XML.

The raw coverage XML and `.coverage` data were written to `%TEMP%`, used to
generate the report, and then removed. They were not committed.

## Artifact Produced

- `docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json`
- `docs/implementation_handoffs/quality_protected_surface_coverage_current_base_remeasurement_comparison.md`

## Report Summary

```yaml
report_schema: "protected_surface_coverage_advisory.v1"
overall_status: "passed_advisory"
measured_ref: "origin/main"
measured_commit: "94d337c635769c214c5beecabef93932033210f3"
global_line_coverage_percent: 87.55
global_branch_coverage_percent: 74.80
global_line_floor_status: "passed"
branch_coverage_status: "advisory_only"
protected_surface_floor_status: "not_authorized"
protected_surface_floor_authorized: false
global_line_floor_increase_authorized: false
branch_coverage_enforcement_authorized: false
ci_change_authorized: false
```

## Comparison Against Prior #605 Report

Prior report:

- `docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json`
- measured commit:
  `83d3141e953913233e3457b910c2c83ff25d44aa`

Fresh report:

- `docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json`
- measured commit:
  `94d337c635769c214c5beecabef93932033210f3`

The current-base report preserved the same top-level coverage posture:

| Field | Prior #605 report | Fresh #617 report |
| --- | --- | --- |
| Global line coverage | 87.55% | 87.55% |
| Global branch coverage | 74.80% | 74.80% |
| Global line floor status | passed | passed |
| Branch coverage status | advisory_only | advisory_only |
| Protected-surface floor status | not_authorized | not_authorized |

Measured group values also matched the prior report.

## Current Group Readiness

| Group | Files | Avg line | Min line | Route |
| --- | ---: | ---: | ---: | --- |
| `parser_state_final_reconciliation` | 2 | 90.33% | 90.21% | best narrow floor proposal candidate |
| `match_game_identity` | 28 | 97.08% | 83.08% | promising but needs overlap/file-minimum caution |
| `extractor_behavior` | 1 | 94.41% | 94.41% | watch-list; tiny one-file surface |
| `workbook_schema_and_exports` | 3 | 93.34% | 83.08% | promising but below-85 file minimum blocks simple floor |
| `parser_event_classes` | 1 | 100.00% | 100.00% | watch-list; tiny one-file surface |
| `environment_runtime_python_paths` | 1 | 100.00% | 100.00% | watch-list; tiny one-file surface |
| `local_app_security_and_artifact_safety` | 16 | 89.64% | 80.19% | focused test-hardening or subgrouping, not floor-ready |
| `webhook_payload_and_transport` | 3 | 83.73% | 76.65% | focused test-hardening, not floor-ready |
| `analytics_schema_and_ingest` | 5 | 80.62% | 45.19% | focused test-hardening / regrouping, not floor-ready |

Not applicable under the current Python coverage source:

- `apps_script_behavior`
- `workflow_authority_docs`
- `workflow_ci_yaml`
- `local_artifact_checker_tools`
- `forbidden_local_artifact_paths`

## Route Decision

Fresh current-base evidence removes the stale-report blocker from #612. The
best next route is:

```yaml
recommended_next_route: "narrow_floor_proposal"
candidate_group: "parser_state_final_reconciliation"
route_owner: "Codex A/B"
floor_implementation_authorized_now: false
```

Plain English: if the owner wants to continue the coverage ratchet, the next
safe work item should be a narrowly scoped problem representation and contract
for a parser-state final-reconciliation floor proposal. That proposal should
still preserve branch coverage as advisory-only, document overlap with
`match_game_identity`, set a conservative line-only threshold below the
fresh measured minimum, and require Codex E review before any implementation.

Secondary routes:

- `analytics_schema_and_ingest`, `webhook_payload_and_transport`, and
  `local_app_security_and_artifact_safety` should route to focused
  test-hardening or subgrouping, not a floor.
- Tiny one-file 100% groups should remain watch-list candidates unless a later
  contract justifies a single-file floor.

## Code Changed

No runtime code changed.

No helper code changed. Existing report tooling was reused.

## Tests Changed

No tests were changed.

Focused report-tooling tests were run unchanged.

## Interface Changes

None.

No CI, coverage gate, `pyproject.toml`, branch coverage, protected-surface
floor, parser, analytics, workbook, webhook, Apps Script, Google Sheets,
OpenAI, AI, coaching, Line Tracer, or production interface changed.

## Validation Run

```text
git status --short --branch --untracked-files=all -> clean before report generation
git rev-parse origin/main -> 94d337c635769c214c5beecabef93932033210f3
py -m pytest -q tests --cov=src/mythic_edge_parser --cov-report=term-missing --cov-report=xml:<temp coverage xml> -> 2041 passed, 4 skipped, 1 warning
py tools\generate_protected_surface_coverage_report.py --coverage-xml <temp coverage xml> --measured-ref origin/main --measured-commit 94d337c635769c214c5beecabef93932033210f3 --write-report --report-date 2026-07-01 -> wrote public-safe report
py tools\check_coverage_floor.py --coverage-xml <temp coverage xml> --command-label "issue #617 current-base protected-surface coverage measurement" -> Global Python line coverage is 87.55% (floor 85.00%); branch coverage is 74.80% advisory-only
py -m pytest -q tests\test_protected_surface_coverage_report.py -> 8 passed
py -m json.tool docs\quality_reports\coverage\protected_surface\2026-07-01-94d337c-protected-surface-coverage-advisory.json -> passed
git diff --check -> passed
py tools\check_agent_docs.py -> passed
path-scoped protected-surface scan over changed files -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan over changed files -> passed, forbidden 0, warnings 0
new-file whitespace/final-newline check -> passed
raw artifact status check -> no temp coverage XML/data remains, no repo .coverage/coverage.xml/htmlcov exists
```

## Raw Artifact Status

- Raw coverage XML: created in `%TEMP%`, used, then removed.
- Raw `.coverage` data: created in `%TEMP%`, used, then removed.
- Raw terminal coverage output: not committed.
- HTML coverage output: not created.
- Raw coverage artifacts committed: false.
- Raw coverage artifacts kept in repo: false.

## Protected-Surface Status

No protected runtime or product surfaces were changed.

Protected parser, analytics, workbook, webhook, Apps Script, Google Sheets,
OpenAI, AI, coaching, Line Tracer, production, private-artifact, generated-data,
and local-only artifact boundaries were preserved.

## Remaining Risks

- The report is advisory evidence only. It does not authorize a floor.
- Branch coverage remains advisory-only.
- A future floor proposal still needs its own issue, contract, explicit owner
  approval, threshold rationale, overlap handling, rollback path, and Codex E
  review.
- The current evidence supports only a narrow candidate discussion for
  `parser_state_final_reconciliation`, not a broad protected-surface floor.

## Next Recommended Role

Immediate next role: Codex E to review this measurement/handoff.

Likely follow-up after clean E review: Codex A/B for a narrow
`parser_state_final_reconciliation` floor proposal, if the owner wants to
continue.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #617.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/617

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Branch:
codex/coverage-next-ratchet-566

Implementation handoff:
docs/implementation_handoffs/quality_protected_surface_coverage_current_base_remeasurement_comparison.md

Fresh report:
docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json

Prior report:
docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json

Source contracts/reports:
- docs/contracts/quality_protected_surface_coverage_floor_readiness.md
- docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md
- docs/contract_test_reports/quality_protected_surface_coverage_candidate_floor_policy.md

Goal:
Review the #617 current-base protected-surface coverage remeasurement. Verify
the report was produced from current origin/main, raw coverage artifacts were
not committed, no gate or CI behavior changed, and the recommended next route
is supported by the evidence.

Validation:
- git status --short --branch --untracked-files=all
- py -m json.tool docs\quality_reports\coverage\protected_surface\2026-07-01-94d337c-protected-surface-coverage-advisory.json
- py -m pytest -q tests\test_protected_surface_coverage_report.py
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files
- verify no raw coverage XML, .coverage data, HTML output, private logs, local-only artifacts, secrets, or generated runtime files are tracked

Review focus:
- measured ref is origin/main;
- measured commit is 94d337c635769c214c5beecabef93932033210f3;
- global 85.00% line floor remains unchanged and passed;
- branch coverage remains advisory-only;
- protected-surface floor remains not authorized;
- report output is public-safe and repo-relative;
- route recommendation is no broader than the evidence supports.

Output:
- findings first;
- validation results;
- raw-artifact status;
- protected-surface status;
- next recommended role;
- workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/617"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "GitHub issue #617 and current origin/main coverage measurement"
  report_artifact: "docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json"
  target_artifact: "docs/implementation_handoffs/quality_protected_surface_coverage_current_base_remeasurement_comparison.md"
  risk_tier: "Medium-High workflow/validation-gate risk; low runtime/product risk"
  base_branch: "main"
  target_branch: "main_after_explicit_user_approval"
  branch: "codex/coverage-next-ratchet-566"
  measured_ref: "origin/main"
  measured_commit: "94d337c635769c214c5beecabef93932033210f3"
  report_overall_status: "passed_advisory"
  global_line_coverage_percent: 87.55
  global_branch_coverage_percent: 74.80
  global_line_floor_status: "passed"
  branch_coverage_status: "advisory_only"
  protected_surface_floor_status: "not_authorized"
  route_decision: "narrow_floor_proposal_candidate"
  candidate_group: "parser_state_final_reconciliation"
  floor_authorized_now: false
  ci_change_authorized: false
  raw_coverage_artifacts_committed: false
  raw_coverage_artifacts_kept: false
  validation:
    - "py -m pytest -q tests --cov=src/mythic_edge_parser --cov-report=term-missing --cov-report=xml:<temp coverage xml> -> 2041 passed, 4 skipped, 1 warning"
    - "py tools\\generate_protected_surface_coverage_report.py --coverage-xml <temp coverage xml> --measured-ref origin/main --measured-commit 94d337c635769c214c5beecabef93932033210f3 --write-report --report-date 2026-07-01 -> wrote report"
    - "py tools\\check_coverage_floor.py --coverage-xml <temp coverage xml> --command-label \"issue #617 current-base protected-surface coverage measurement\" -> passed, line 87.55%, branch 74.80% advisory-only"
    - "py -m pytest -q tests\\test_protected_surface_coverage_report.py -> 8 passed"
    - "py -m json.tool docs\\quality_reports\\coverage\\protected_surface\\2026-07-01-94d337c-protected-surface-coverage-advisory.json -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan over changed files -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over changed files -> passed, forbidden 0, warnings 0"
    - "new-file whitespace/final-newline check -> passed"
    - "raw artifact status check -> no temp coverage XML/data remains, no repo .coverage/coverage.xml/htmlcov exists"
  forbidden_scope_touched: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
