# Quality Protected-Surface Coverage Floor Candidate Selection Contract Test Report

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/622
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568

## Contract

- `docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md`

## Implementation Under Test

- Branch: `codex/protected-surface-coverage-floor-candidate-622`
- Base: `origin/main`
- Changed file:
  `docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The #622 contract must decide whether
`parser_state_final_reconciliation` is the first reasonable future
protected-surface line-floor candidate, using the current-base #617 advisory
coverage report as evidence. It must not implement or authorize a floor,
change CI, raise the global 85.00% line floor, enforce branch coverage, run new
coverage measurements, or change parser/runtime/product behavior.

## Internal Project Area Reviewed

Quality / validation gates.

## Bridge-Code Status Reviewed

`shared_support`

Coverage evidence may support future validation-gate design, but it does not
own parser truth, protected-surface authorization, security assurance, privacy
assurance, release readiness, deploy readiness, production readiness,
analytics truth, AI truth, or coaching truth.

## Findings

No blocking findings.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-622-001 | none | `not_reproduced` | No contract mismatch found. | not_blocking | Codex E reviewed the #622 issue, contract, #617 advisory report, #617 handoff/report, and #612 candidate-floor policy. | Candidate selection matches #617 evidence; floor implementation remains explicitly unauthorized; docs and safety checks passed. | F |

## Checks Run

```text
git status --short --branch --untracked-files=all -> expected untracked #622 contract only before this report
git rev-parse HEAD -> 87919283dd7837e2a905caa82ae758d41667e5ab
git rev-parse origin/main -> 87919283dd7837e2a905caa82ae758d41667e5ab
git rev-list --left-right --count HEAD...origin/main -> 0 0
gh issue view 622 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body -> issue open and source criteria available
py -m json.tool docs\quality_reports\coverage\protected_surface\2026-07-01-94d337c-protected-surface-coverage-advisory.json -> passed
git diff --check -- docs\contracts\quality_protected_surface_coverage_floor_candidate_selection.md -> passed
py tools\check_agent_docs.py -> passed, errors 0, warnings 0
contract whitespace/final-newline check -> passed
path-scoped protected-surface scan over contract and source evidence -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan over contract and source evidence -> passed, forbidden 0, warnings 0
raw/private/local artifact sweep over contract and source report -> passed
repo raw artifact check -> no repo `.coverage`, `coverage.xml`, or `htmlcov` output present
```

Codex E did not rerun coverage. This review is for the contract-only candidate
selection package. New coverage measurement remains out of scope for #622.

## Results

Passed. The #622 contract satisfies the issue and policy boundaries and is
ready for Codex F submission.

## Evidence Confirmed

The #617 advisory report records:

```yaml
schema_version: "protected_surface_coverage_advisory.v1"
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
raw_artifacts_committed: false
```

For `parser_state_final_reconciliation`, the reviewed report data supports the
contract's candidate decision:

| File | Line coverage |
| --- | ---: |
| `src/mythic_edge_parser/app/models.py` | 90.45% |
| `src/mythic_edge_parser/app/state.py` | 90.21% |

Summary:

```yaml
files: 2
average_line_coverage_percent: 90.33
minimum_line_coverage_percent: 90.21
```

## Confirmed Contract Matches

- The contract selects `parser_state_final_reconciliation` as the first future
  protected-surface line-only floor candidate.
- The selected candidate is supported by #617 current-base evidence.
- The contract keeps `floor_implementation_authorized_now: false`.
- The contract keeps `ci_change_authorized_now: false`.
- The contract keeps `branch_coverage_enforcement_authorized_now: false`.
- The contract keeps `global_line_floor_increase_authorized_now: false`.
- The recommended future threshold range is explicitly non-binding.
- The contract requires fresh current-base measurement before any future floor
  implementation.
- The contract requires branch coverage to remain advisory-only.
- The contract explains overlap with `match_game_identity` without treating
  this as a match/game identity floor.
- Broader, one-file, uneven, and not-applicable groups are deferred with
  reasons consistent with the #617 report and #612 policy.
- The contract forbids raw coverage artifacts, private/local paths, secrets,
  generated artifacts, local-only artifacts, and product/runtime changes.
- No implementation files, CI files, coverage settings, parser files,
  fixtures, or runtime/product files changed in this package.

## Contract Mismatches

None.

## Missing Tests

None blocking.

This is a docs-only candidate-selection contract. No implementation code or
test code changed, and no new coverage measurement was authorized.

## Drift Notes

- Branch drift: none; local HEAD and `origin/main` are both
  `87919283dd7837e2a905caa82ae758d41667e5ab`.
- Coverage evidence drift: acknowledged and controlled. The selected evidence
  report was measured at `94d337c635769c214c5beecabef93932033210f3`, while a
  later implementation must remeasure the then-current intended base.
- Issue lifecycle drift: none. #622 remains open pending submission and later
  lifecycle handling.
- Tracker drift: none reviewed as blocking. Tracker #566 remains open.
- Production/deployment/workbook/local-data drift: none found.

## Protected-Surface Status

Passed. The path-scoped protected-surface scan reported forbidden 0, warnings
0. No protected parser/runtime/product surfaces were touched.

## Secret / Private Marker Status

Passed. The path-scoped secret/private-marker scan reported forbidden 0,
warnings 0. No raw/private/generated/local artifacts were added.

## Raw / Generated Artifact Status

- Raw coverage XML: not present in repo.
- `.coverage` data: not present in repo.
- HTML coverage output: not present in repo.
- Raw terminal coverage output: not committed.
- Private/local/generated artifacts: none found in the changed package.

## Recommendation

Approve for Codex F.

Codex F should stage only:

- `docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md`
- `docs/contract_test_reports/quality_protected_surface_coverage_floor_candidate_selection.md`

After submitter/deployer lifecycle work, #622 can close as a candidate-selection
contract issue if the PR merges cleanly. That closure must not imply that a
protected-surface floor has been implemented or authorized.

A future implementation issue is reasonable if the owner wants to continue the
coverage ratchet, but it must include explicit approval for the next gate
shape and must remeasure the current intended base before changing CI or
coverage tooling.

## Next Workflow Action

Next role: Codex F.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #622.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/622

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Branch:
codex/protected-surface-coverage-floor-candidate-622

Base / target:
origin/main / main after explicit user approval for PR submission only. Do not merge.

Contract:
docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md

Codex E review artifact:
docs/contract_test_reports/quality_protected_surface_coverage_floor_candidate_selection.md

Approved files to stage:
- docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md
- docs/contract_test_reports/quality_protected_surface_coverage_floor_candidate_selection.md

Goal:
Stage only the reviewed #622 contract-only package, commit, push, and open or
update a draft PR. Do not implement a protected-surface floor, change CI, raise
the global 85.00% line floor, enforce branch coverage, run coverage, close
#622, close tracker #566, or merge.

Before committing, rerun:
- git status --short --branch --untracked-files=all
- git rev-list --left-right --count HEAD...origin/main
- py -m json.tool docs\quality_reports\coverage\protected_surface\2026-07-01-94d337c-protected-surface-coverage-advisory.json
- git diff --check -- docs\contracts\quality_protected_surface_coverage_floor_candidate_selection.md docs\contract_test_reports\quality_protected_surface_coverage_floor_candidate_selection.md
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over staged files
- path-scoped secret/private-marker scan over staged files

Final output:
- commit hash
- PR URL
- files staged
- validation results
- protected-surface status
- secret/private-marker status
- next recommended role Codex G after PR checks
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/622"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/quality_protected_surface_coverage_floor_candidate_selection.md"
  target_artifact: "docs/contract_test_reports/quality_protected_surface_coverage_floor_candidate_selection.md"
  risk_tier: "Medium-High workflow/validation-gate risk; low runtime/product risk"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/protected-surface-coverage-floor-candidate-622"
  candidate_group: "parser_state_final_reconciliation"
  decision: "Selected as first future protected-surface line-only floor candidate; implementation not authorized."
  floor_authorized_now: false
  ci_change_authorized: false
  branch_coverage_enforcement_authorized: false
  validation:
    - "branch sync -> passed, 0 0 with origin/main"
    - "py -m json.tool #617 advisory report -> passed"
    - "git diff --check -- #622 contract -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "contract whitespace/final-newline check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "raw/private/local artifact sweep -> passed"
    - "repo raw artifact check -> no repo .coverage/coverage.xml/htmlcov exists"
  protected_surface_status: "passed, forbidden 0, warnings 0"
  secret_private_marker_status: "passed, forbidden 0, warnings 0"
  raw_coverage_artifacts_committed: false
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  codex_f_recommended: true
  next_recommended_role: "Codex F: Module Submitter"
```
