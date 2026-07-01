# Quality Protected-Surface Coverage Candidate Floor Policy Contract Test

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/612>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/566>

## Contract

`docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md`

## Implementation Under Test

Contract-only Codex B artifact on branch
`codex/protected-surface-coverage-interpretation-566`.

Reviewed file:

- `docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md`

Primary evidence artifact interpreted by the contract:

- `docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

Issue #612 asks for interpretation policy only. The contract must explain what
the #605 protected-surface coverage advisory report means for later coverage
ratchet work, identify which groups are promising, caution, not ready, or not
applicable, and preserve the boundary that no protected-surface floor, CI
change, global line-floor increase, or branch coverage enforcement is
authorized now.

## Internal Project Area Reviewed

Quality / validation gates.

Coverage reporting is reviewed as advisory workflow evidence only. It does not
own parser truth, parser correctness, security assurance, privacy assurance,
release readiness, deploy readiness, production readiness, analytics truth, AI
truth, or coaching truth.

## Bridge-Code Status Reviewed

`shared_support`

The contract bridges prior coverage evidence into future policy discussion. It
does not authorize implementation, enforcement, protected-surface code changes,
or CI changes.

## Checks Run

```powershell
git status --short --branch --untracked-files=all
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
gh issue view 612 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body
gh issue view 566 --repo Tahjali11/Mythic-Edge --json number,title,state,url
gh issue view 568 --repo Tahjali11/Mythic-Edge --json number,title,state,url
py -m json.tool docs\quality_reports\coverage\protected_surface\2026-07-01-83d3141-protected-surface-coverage-advisory.json > $null
py - <<'PY'
import json
from pathlib import Path
p = Path("docs/quality_reports/coverage/protected_surface/2026-07-01-83d3141-protected-surface-coverage-advisory.json")
data = json.loads(p.read_text(encoding="utf-8"))
for group in data["groups"]:
    measured = [f for f in group["files"] if isinstance(f.get("line_coverage_percent"), (int, float))]
    if measured:
        avg = sum(float(f["line_coverage_percent"]) for f in measured) / len(measured)
        minimum = min(float(f["line_coverage_percent"]) for f in measured)
        print(group["group_id"], len(measured), round(avg, 2), round(minimum, 2), group["coverage_scope_status"])
    else:
        print(group["group_id"], 0, "NA", "NA", group["coverage_scope_status"])
PY
git diff --check -- docs\contracts\quality_protected_surface_coverage_candidate_floor_policy.md
Select-String -Path docs\contracts\quality_protected_surface_coverage_candidate_floor_policy.md -Pattern '[ \t]+$'
py tools\check_agent_docs.py
@'
docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

## Results

- Branch is `codex/protected-surface-coverage-interpretation-566`.
- Branch is synced with `origin/main`: `0 0`.
- Reviewed HEAD and `origin/main` are both
  `62bc9c2a61b414d5e168148cb078a44842fc42bc`.
- Issue #612, tracker #566, and project roadmap #568 are open.
- Advisory report JSON parsed successfully.
- Independent JSON summary check confirmed the measured group counts,
  averages, minimums, and not-applicable statuses used by the contract.
- `git diff --check` over the contract path passed.
- Contract trailing-whitespace scan returned no matches.
- Agent docs check passed with `errors: 0`, `warnings: 0`.
- Path-scoped protected-surface scan over the contract passed with
  `forbidden: 0`, `warnings: 0`.
- Path-scoped secret/private-marker scan over the contract passed with
  `forbidden: 0`, `warnings: 0`.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-612-000 | none | `not_reproduced` | No blocking contract mismatch found. | not_blocking | N/A | Contract, issue #612, #605 advisory report, branch state, JSON parse, group math check, docs check, protected-surface scan, and secret/private-marker scan reviewed cleanly. | F |

## Confirmed Contract Matches

- The contract is docs-only and does not authorize code, CI, coverage settings,
  coverage-floor, or product behavior changes.
- The contract explicitly states no protected-surface floor is ready to become
  blocking from the #605 advisory report.
- The contract correctly preserves `protected_surface_floor_status:
  not_authorized`.
- The contract correctly preserves branch coverage as `advisory_only`.
- The contract recognizes the #605 advisory report as stale relative to current
  `origin/main` and blocks direct floor activation from stale evidence alone.
- The contract uses line coverage as the only allowed future floor input.
- The contract classifies measured groups consistently with the advisory JSON:
  - `parser_state_final_reconciliation`: 2 files, average 90.33%, minimum
    90.21%, promising.
  - `match_game_identity`: 28 files, average 97.08%, minimum 83.08%,
    promising with file-minimum/overlap caution.
  - `extractor_behavior`: 1 file, 94.41%, promising but tiny.
  - `workbook_schema_and_exports`: 3 files, average 93.34%, minimum 83.08%,
    promising with caution.
  - `parser_event_classes`: 1 file, 100.00%, caution due tiny sample.
  - `environment_runtime_python_paths`: 1 file, 100.00%, caution due tiny
    sample.
  - `local_app_security_and_artifact_safety`: 16 files, average 89.64%,
    minimum 80.19%, caution due unevenness.
  - `webhook_payload_and_transport`: 3 files, average 83.73%, minimum 76.65%,
    caution and not floor-ready.
  - `analytics_schema_and_ingest`: 5 files, average 80.62%, minimum 45.19%,
    not ready.
- The contract correctly treats Apps Script, workflow docs, workflow YAML,
  checker tools, and forbidden local artifact paths as not applicable to the
  current Python coverage source.
- The contract defines future floor evidence requirements, explicit blockers,
  stale-evidence policy, raw artifact boundaries, and Codex C/E/G validation
  expectations.
- The contract preserves non-claims for parser correctness, security/privacy
  assurance, release/deploy/production readiness, analytics truth, AI truth,
  and coaching truth.

## Contract Mismatches

None found.

## Missing Tests

No tests are required for this contract-only slice. Future implementation or
report-helper changes must add focused tests under their own issue/contract.

## Drift Notes

- Issue lifecycle drift: none. Issue #612 is open.
- Tracker drift: none. Tracker #566 remains open, as required.
- Coverage evidence drift: intentionally acknowledged. The #605 advisory
  report remains committed evidence, but it is stale relative to current
  `origin/main` and the contract treats it as policy input only, not activation
  evidence.
- CI/enforcement drift: none. No CI, coverage setting, floor, or branch
  coverage enforcement change is present.
- Parser/runtime/downstream drift: none.

## Recommendation

Approve for Codex F as a contract-only package. Codex F should stage only the
#612 contract and this review artifact, use `Refs #612` and `Refs #566`, and
avoid any `Closes` wording unless issue lifecycle closeout is explicitly
approved later.

Optional future route after submission: Codex A may open a new follow-up issue
for one specific candidate group if the owner wants to pursue actual floor
proposal work.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #612.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/612

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Branch:
codex/protected-surface-coverage-interpretation-566

Base branch:
main

Reviewed contract:
docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md

Contract-test report:
docs/contract_test_reports/quality_protected_surface_coverage_candidate_floor_policy.md

Goal:
Submit the contract-only #612 package. Stage only the reviewed contract and
contract-test report, commit, push the branch, and open a draft PR. Use
Refs #612 and Refs #566, not Closes, unless issue closeout is explicitly
authorized later.

Before staging:
- Run git status --short --branch --untracked-files=all.
- Confirm the dirty set contains only the reviewed #612 contract/report files.
- Exclude raw coverage artifacts, _review_ files, generated local artifacts,
  private artifacts, runtime files, logs, and unrelated files.

Recommended validation before submit:
- git diff --check -- docs\contracts\quality_protected_surface_coverage_candidate_floor_policy.md docs\contract_test_reports\quality_protected_surface_coverage_candidate_floor_policy.md
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over staged/reviewed files
- path-scoped secret/private-marker scan over staged/reviewed files

Do not add CI gates, add protected-surface floors, raise the global line floor,
add branch coverage enforcement, change coverage settings, close #612, close
tracker #566, or change parser/runtime/analytics/workbook/webhook/App Script/
Sheets/OpenAI/AI/coaching/production behavior.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/612"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/quality_protected_surface_coverage_candidate_floor_policy.md"
  artifact_produced: "docs/contract_test_reports/quality_protected_surface_coverage_candidate_floor_policy.md"
  risk_tier: "High workflow and validation-gate policy risk; low runtime risk"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/protected-surface-coverage-interpretation-566"
  reviewed_head: "62bc9c2a61b414d5e168148cb078a44842fc42bc"
  branch_sync: "0 0 with origin/main"
  verdict: "contract_policy_clean_for_submitter"
  protected_surface_floor_authorized: false
  global_line_floor_increase_authorized: false
  branch_coverage_enforcement_authorized: false
  validation:
    - "py -m json.tool docs\\quality_reports\\coverage\\protected_surface\\2026-07-01-83d3141-protected-surface-coverage-advisory.json -> passed"
    - "independent protected-surface coverage group math check -> matched contract classifications"
    - "git diff --check -- docs\\contracts\\quality_protected_surface_coverage_candidate_floor_policy.md -> passed"
    - "contract trailing-whitespace scan -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  raw_coverage_artifacts_committed: false
  generated_private_artifacts_kept: false
  forbidden_scope_touched: false
  codex_f_recommended: true
  next_recommended_role: "Codex F: Module Submitter"
```
