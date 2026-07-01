# Quality Protected-Surface Coverage Current-Base Remeasurement Contract Test Report

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/617
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568

## Contract

Primary issue source:

- GitHub issue #617

Policy/source contracts:

- `docs/contracts/quality_protected_surface_coverage_floor_readiness.md`
- `docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md`
- `docs/contract_test_reports/quality_protected_surface_coverage_candidate_floor_policy.md`

No separate #617-specific `docs/contracts/` artifact was present in this
package. That is non-blocking because issue #617 explicitly defines this as a
current-base, report-only remeasurement against the existing #605/#612
coverage policy artifacts.

## Implementation Under Test

- Branch: `codex/coverage-next-ratchet-566`
- Base/measured ref: `origin/main`
- Measured commit: `94d337c635769c214c5beecabef93932033210f3`
- Implementation handoff:
  `docs/implementation_handoffs/quality_protected_surface_coverage_current_base_remeasurement_comparison.md`
- Fresh advisory report:
  `docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The #617 package must provide current-base protected-surface coverage evidence
only. It must keep the global 85.00% Python line coverage floor unchanged,
keep branch coverage advisory-only, avoid creating or implying a
protected-surface floor, keep raw coverage artifacts local/untracked, and avoid
changes to parser/runtime/product behavior.

## Internal Project Area Reviewed

Quality / validation gates.

## Bridge-Code Status Reviewed

`shared_support`

Coverage evidence may inform future quality-tooling policy, but it does not
own parser truth, protected-surface authorization, security assurance, privacy
assurance, release readiness, deploy readiness, analytics truth, AI truth, or
coaching truth.

## Findings

No blocking findings.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-617-001 | P3 | `remaining_non_blocking` | No separate #617 contract artifact exists. | non_blocking | The package relies on GitHub issue #617 plus #605/#612 policy contracts. | Issue #617 contains explicit acceptance criteria and the handoff/report preserve those boundaries. | none |

## Checks Run

```text
git status --short --branch --untracked-files=all -> two expected untracked #617 artifacts before this report
git rev-list --left-right --count HEAD...origin/main -> 0 0
gh issue view 617 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body -> issue open and source criteria available
py -m json.tool docs\quality_reports\coverage\protected_surface\2026-07-01-94d337c-protected-surface-coverage-advisory.json -> passed
py -m pytest -q tests\test_protected_surface_coverage_report.py -> 8 passed
git diff --check -> passed
py tools\check_agent_docs.py -> passed, errors 0, warnings 0
new-file whitespace/final-newline check -> passed
path-scoped protected-surface scan over #617 artifacts -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan over #617 artifacts -> passed, forbidden 0, warnings 0
raw/private/local artifact path sweep -> passed after excluding policy-only textual mentions of removed `.coverage` and coverage XML artifacts
repo raw artifact check -> no repo `.coverage`, `coverage.xml`, or `htmlcov` output present
```

Codex E did not rerun the full coverage measurement. The full measurement
evidence is recorded in the implementation handoff and was reviewed as
artifact evidence.

## Results

Passed for contract-test purposes.

The fresh report records:

```yaml
schema_version: "protected_surface_coverage_advisory.v1"
repository: "Tahjali11/Mythic-Edge"
measured_ref: "origin/main"
measured_commit: "94d337c635769c214c5beecabef93932033210f3"
coverage_source: "src/mythic_edge_parser"
global_line_coverage_percent: 87.55
global_branch_coverage_percent: 74.80
global_line_floor_percent: 85.00
global_line_floor_status: "passed"
branch_coverage_status: "advisory_only"
protected_surface_floor_status: "not_authorized"
protected_surface_floor_authorized: false
global_line_floor_increase_authorized: false
branch_coverage_enforcement_authorized: false
ci_change_authorized: false
raw_artifacts_committed: false
advisory_only: true
```

## Confirmed Contract Matches

- The measured ref is `origin/main`.
- The measured commit is `94d337c635769c214c5beecabef93932033210f3`.
- Branch sync is clean against `origin/main`.
- The fresh report is public-safe JSON and uses repo-relative source paths.
- The global 85.00% Python line floor remains unchanged and passed.
- Branch coverage remains advisory-only.
- Protected-surface floor status remains `not_authorized`.
- No CI, `pyproject.toml`, repo-check helper, or coverage-gate behavior changed.
- Raw coverage artifacts are not tracked or present in the repo.
- Non-Python and out-of-current-source groups remain
  `not_applicable_current_coverage_scope`.
- The route recommendation is limited to a future narrow
  `parser_state_final_reconciliation` floor proposal discussion.
- Floor implementation is explicitly not authorized now.
- No parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/production behavior changed.

## Contract Mismatches

None.

## Missing Tests

None blocking.

Focused report-tooling tests are unchanged and passed. No implementation code
or test code changed in this #617 package.

## Drift Notes

- Repo drift: none found for this package.
- Coverage evidence drift: the prior #605 report was stale; this #617 package
  supplies the current-base advisory evidence requested by issue #617.
- Issue lifecycle drift: none. Issue #617 remains open pending submission and
  later lifecycle handling.
- Tracker drift: none reviewed as blocking. Tracker #566 remains open.
- Production/deployment/workbook/local-data drift: none found.

## Raw Artifact Status

- Raw coverage XML: not present in repo.
- `.coverage` data: not present in repo.
- HTML coverage output: not present in repo.
- Raw terminal coverage output: not committed.
- Private/local/generated artifacts: none found in the changed package.

## Protected-Surface Status

Passed. The changed package is docs/report-only and did not touch protected
runtime or product surfaces.

## Secret / Private Marker Status

Passed. The path-scoped secret/private-marker scan reported forbidden 0,
warnings 0.

## Recommendation

Approve for Codex F submitter.

Codex F should stage only:

- `docs/implementation_handoffs/quality_protected_surface_coverage_current_base_remeasurement_comparison.md`
- `docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json`
- `docs/contract_test_reports/quality_protected_surface_coverage_current_base_remeasurement.md`

After submission, the likely next planning route is Codex A/B for a narrow
`parser_state_final_reconciliation` floor proposal, if the owner wants to keep
ratcheting coverage. No floor, CI change, branch coverage enforcement, or
global floor increase is authorized by this review.

## Next Workflow Action

Next role: Codex F.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #617.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/617

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Branch:
codex/coverage-next-ratchet-566

Base / target:
main, after explicit user approval for PR submission only. Do not merge.

Codex E review artifact:
docs/contract_test_reports/quality_protected_surface_coverage_current_base_remeasurement.md

Approved files to stage:
- docs/implementation_handoffs/quality_protected_surface_coverage_current_base_remeasurement_comparison.md
- docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json
- docs/contract_test_reports/quality_protected_surface_coverage_current_base_remeasurement.md

Goal:
Stage only the reviewed #617 report-only package, commit, push, and open or
update a draft PR. Do not add a coverage floor, change CI, close #617, close
tracker #566, merge, or target production behavior.

Before committing, rerun:
- git status --short --branch --untracked-files=all
- py -m json.tool docs\quality_reports\coverage\protected_surface\2026-07-01-94d337c-protected-surface-coverage-advisory.json
- py -m pytest -q tests\test_protected_surface_coverage_report.py
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over the staged files
- path-scoped secret/private-marker scan over the staged files

Final output:
- commit hash
- PR URL
- files staged
- validation results
- raw artifact status
- next recommended role Codex G after PR checks
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/617"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/implementation_handoffs/quality_protected_surface_coverage_current_base_remeasurement_comparison.md"
  report_artifact: "docs/quality_reports/coverage/protected_surface/2026-07-01-94d337c-protected-surface-coverage-advisory.json"
  artifact_produced: "docs/contract_test_reports/quality_protected_surface_coverage_current_base_remeasurement.md"
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
    - "py -m json.tool docs\\quality_reports\\coverage\\protected_surface\\2026-07-01-94d337c-protected-surface-coverage-advisory.json -> passed"
    - "py -m pytest -q tests\\test_protected_surface_coverage_report.py -> 8 passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed, errors 0, warnings 0"
    - "new-file whitespace/final-newline check -> passed"
    - "path-scoped protected-surface scan over #617 artifacts -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over #617 artifacts -> passed, forbidden 0, warnings 0"
    - "raw/private/local artifact path sweep -> passed"
    - "repo raw artifact check -> no repo .coverage/coverage.xml/htmlcov exists"
  forbidden_scope_touched: false
  codex_f_recommended: true
  next_recommended_role: "Codex F: Module Submitter"
```
