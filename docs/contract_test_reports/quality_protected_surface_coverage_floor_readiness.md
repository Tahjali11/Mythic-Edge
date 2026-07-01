# Quality Protected-Surface Coverage Floor Readiness Contract Test

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/605>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/566>

## Contract

`docs/contracts/quality_protected_surface_coverage_floor_readiness.md`

## Implementation Under Test

- Branch: `codex/protected-surface-coverage-readiness-566`
- Base ref: `origin/main`
- Reviewed head/base: `83d3141e953913233e3457b910c2c83ff25d44aa`
- Implementation handoff:
  `docs/implementation_handoffs/quality_protected_surface_coverage_floor_readiness_comparison.md`
- Advisory report:
  `docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

Issue #605 authorizes an advisory protected-surface coverage measurement and
reporting slice only. It does not authorize a protected-surface coverage floor,
CI gate, global line-floor increase, branch coverage enforcement, coverage
source change, parser/runtime behavior change, downstream product behavior
change, or private artifact exposure.

The report may summarize protected/protected-adjacent Python source coverage by
category, file path, and internal project area using repo-relative paths and
symbolic statuses. It must keep branch coverage advisory-only and record
non-Python or out-of-current-source surfaces as not applicable instead of
inventing coverage percentages.

## Internal Project Area Reviewed

Quality / validation gates. The implementation bridges coverage reporting with
protected-surface classification as advisory support only. It does not make
coverage data the protected-surface authorization source.

## Checks Run

```powershell
git status --short --branch --untracked-files=all
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
gh issue view 605 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body
gh issue view 566 --repo Tahjali11/Mythic-Edge --json number,title,state,url
py -m pytest -q tests\test_protected_surface_coverage_report.py
py -m ruff check tools\generate_protected_surface_coverage_report.py tests\test_protected_surface_coverage_report.py
py -m json.tool docs\quality_reports\coverage\protected_surface\2026-07-01-83d3141-protected-surface-coverage-advisory.json
py tools\check_coverage_floor.py --coverage-xml _review_\quality_protected_surface_coverage\2026-07-01-83d3141-local-codex-c\coverage.xml --line-floor 85 --command-label "protected-surface advisory measurement"
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
git check-ignore -v _review_\quality_protected_surface_coverage\2026-07-01-83d3141-local-codex-c\.coverage _review_\quality_protected_surface_coverage\2026-07-01-83d3141-local-codex-c\coverage.xml
```

## Results

- Branch and base were synced: `0 0` against `origin/main`.
- Issue #605 and tracker #566 were open at review time.
- Focused protected-surface report tests passed: `8 passed`.
- Ruff on changed Python helper/test files passed.
- Advisory JSON report syntax validation passed.
- Existing coverage-floor helper confirmed global line coverage `87.55%`
  against floor `85.00%`; branch coverage `74.80%` remained advisory-only.
- `git diff --check` passed.
- Agent docs check passed with `errors: 0`, `warnings: 0`.
- Path-scoped protected-surface scan passed with `forbidden: 0`,
  `warnings: 0`.
- Path-scoped secret/private-marker scan passed with `forbidden: 0`,
  `warnings: 0`.
- Local raw coverage artifacts under `_review_/` are ignored by `.gitignore`.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-605-000 | none | `not_reproduced` | No blocking contract mismatch found. | not_blocking | N/A | Contract, helper, tests, generated advisory report, focused validation, coverage-floor corroboration, protected-surface scan, and secret/private-marker scan reviewed cleanly. | F |

## Confirmed Contract Matches

- `tools/generate_protected_surface_coverage_report.py` is advisory report
  tooling only and reads an already-produced coverage XML artifact.
- The generated report uses schema
  `protected_surface_coverage_advisory.v1`.
- The generated report records measured commit
  `83d3141e953913233e3457b910c2c83ff25d44aa`, matching the reviewed branch
  head and `origin/main`.
- The report records global line coverage `87.55%`, global branch coverage
  `74.80%`, global line floor `85.0`, global line floor status `passed`,
  branch coverage status `advisory_only`, and protected-surface floor status
  `not_authorized`.
- `protected_surface_floor_authorized`, `ci_change_authorized`,
  `global_line_floor_increase_authorized`, and
  `branch_coverage_enforcement_authorized` remain `false`.
- Measured protected/protected-adjacent Python groups use repo-relative paths
  and per-file line/branch percentages.
- Non-Python or out-of-current-source groups such as Apps Script, governance
  docs, workflow YAML, quality tools, and local artifact paths use
  `not_applicable_current_coverage_scope` without fake percentages.
- Branch coverage is labelled advisory-only per file and globally, with no
  threshold or blocking behavior.
- The implementation did not change `.github/workflows/repo-checks.yml`,
  `tools/run_repo_checks.ps1`, `pyproject.toml`, or
  `tools/check_coverage_floor.py`.
- The implementation did not change parser behavior, parser final
  reconciliation, analytics schema/ingest, workbook schema, webhook payload
  shape, Apps Script/Sheets behavior, OpenAI/model-provider behavior,
  AI/coaching behavior, Line Tracer behavior, or production behavior.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests found. Focused tests cover advisory flags, global
floor boundary preservation, repo-relative measured file rates, missing
measurable file handling without fake percentages, non-Python groups as not
applicable, missing/malformed coverage XML fail-closed behavior, default report
path naming, and output path restriction.

## Advisory Report And Schema Status

Passed. The advisory report is JSON, schema version
`protected_surface_coverage_advisory.v1`, public-safe, and repo-relative. It
does not include raw coverage XML, `.coverage` contents, HTML coverage output,
raw terminal transcripts, absolute local paths, private logs, raw Player.log
content, private JSONL artifacts, SQLite databases, workbook exports, runtime
files, failed-post queue artifacts, secrets, credentials, tokens, or webhook
URLs.

## Coverage Evidence Freshness Status

Passed for this review. The branch head, `origin/main`, and the advisory report
measured commit are all
`83d3141e953913233e3457b910c2c83ff25d44aa`. If `origin/main` advances before
submission or merge readiness, the coverage evidence should be refreshed or
explicitly accepted as stale by the next role.

## Protected-Surface Status

Passed. The only protected-adjacent source change is quality/reporting tooling
plus a focused validation mapping. Product protected surfaces were not changed.

## Secret/Private-Marker Status

Passed. Path-scoped secret/private-marker scan returned `forbidden: 0`,
`warnings: 0`.

## Generated/Private Artifact Status

- Intentional public advisory report kept under
  `docs/quality_reports/coverage/protected_surface/`.
- Raw coverage XML and `.coverage` artifacts remain ignored under `_review_/`.
- No private/generated/local artifacts were added to the tracked package.

## Drift Notes

- CI/enforcement drift: none introduced.
- Coverage policy drift: none introduced; global 85.00% line floor remains the
  only active coverage gate.
- Parser/runtime/downstream drift: none introduced.
- Issue lifecycle drift: #605 remains open pending submitter/deployer flow;
  tracker #566 remains open.

## Recommendation

Approve for Codex F submitter. Codex F should stage only the reviewed #605
files and open a draft PR. Do not close #605 or tracker #566 from the submitter
thread.

## Remaining Risk

- GitHub Actions has not run for this branch until Codex F submits it.
- Coverage evidence is current to `83d3141`; it should be refreshed if
  `origin/main` advances before merge/deployer readiness.
- Any future protected-surface floor or branch coverage enforcement still
  requires a separate issue, contract, and explicit authorization.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #605.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/605

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Branch:
codex/protected-surface-coverage-readiness-566

Base branch:
main

Reviewed contract:
docs/contracts/quality_protected_surface_coverage_floor_readiness.md

Implementation handoff:
docs/implementation_handoffs/quality_protected_surface_coverage_floor_readiness_comparison.md

Contract-test report:
docs/contract_test_reports/quality_protected_surface_coverage_floor_readiness.md

Advisory report:
docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json

Goal:
Stage only the reviewed #605 files, commit, push the branch, and open a draft
PR. Use Refs #605 and Refs #566, not Closes, unless issue closeout is
explicitly authorized later.

Before staging:
- Run git status --short --branch --untracked-files=all.
- Confirm the dirty set matches the reviewed #605 package.
- Exclude raw coverage XML, .coverage files, HTML coverage output, _review_
  artifacts, private/generated/local artifacts, and unrelated files.

Recommended validation before submit:
- py -m pytest -q tests\test_protected_surface_coverage_report.py
- py -m ruff check tools\generate_protected_surface_coverage_report.py tests\test_protected_surface_coverage_report.py
- py -m json.tool docs\quality_reports\coverage\protected_surface\2026-07-01-83d3141-protected-surface-coverage-advisory.json
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over staged/reviewed files
- path-scoped secret/private-marker scan over staged/reviewed files

Do not add CI gates, add protected-surface floors, raise the global line floor,
add branch coverage enforcement, close #605, close tracker #566, or change
parser/runtime/analytics/workbook/webhook/App Script/AI/coaching/production
behavior.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/605"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/quality_protected_surface_coverage_floor_readiness.md"
  implementation_handoff: "docs/implementation_handoffs/quality_protected_surface_coverage_floor_readiness_comparison.md"
  artifact_produced: "docs/contract_test_reports/quality_protected_surface_coverage_floor_readiness.md"
  advisory_report: "docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json"
  risk_tier: "High workflow and validation-gate policy risk; low runtime risk"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/protected-surface-coverage-readiness-566"
  reviewed_head: "83d3141e953913233e3457b910c2c83ff25d44aa"
  branch_sync: "0 0 with origin/main"
  global_line_coverage_percent: 87.55
  global_branch_coverage_percent: 74.80
  protected_surface_floor_status: "not_authorized"
  branch_coverage_status: "advisory_only"
  validation:
    - "py -m pytest -q tests\\test_protected_surface_coverage_report.py -> passed, 8 passed"
    - "py -m ruff check tools\\generate_protected_surface_coverage_report.py tests\\test_protected_surface_coverage_report.py -> passed"
    - "py -m json.tool docs\\quality_reports\\coverage\\protected_surface\\2026-07-01-83d3141-protected-surface-coverage-advisory.json -> passed"
    - "py tools\\check_coverage_floor.py --coverage-xml _review_\\quality_protected_surface_coverage\\2026-07-01-83d3141-local-codex-c\\coverage.xml --line-floor 85 --command-label \"protected-surface advisory measurement\" -> passed, line 87.55%, branch 74.80% advisory-only"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  advisory_only_status: "confirmed"
  ci_changed: false
  protected_surface_floor_authorized: false
  global_line_floor_increase_authorized: false
  branch_coverage_enforcement_authorized: false
  raw_coverage_artifacts_committed: false
  generated_private_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter"
```
