# Security CWE-Mapped Local Validation Profile Advisory Report Contract Test

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/603>

## Parent Security Workflow

<https://github.com/Tahjali11/Mythic-Edge/issues/330>

## Contract

`docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md`

## Implementation Under Test

- Branch: `codex/cwe-profile-advisory-report-603`
- Base ref: `origin/main`
- Reviewed head/base: `024eda7d9408c0bb72d645af4d41d604539291ba`
- Implementation handoff:
  `docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_report_comparison.md`
- Generated report:
  `docs/quality_reports/security/cwe_mapped_local_validation_profile/2026-07-01-024eda7-cwe-profile-advisory-report.json`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

Issue #603 authorizes a public-safe advisory JSON report helper for the
CWE-mapped local validation profile. The helper may consume only the profile
manifest, the existing profile validator result, and public Git/repo metadata.
It must not aggregate scanner outputs, read raw SARIF or CodeQL API responses,
mutate CodeQL alerts, enable CI enforcement, claim security/privacy assurance,
claim release or deploy readiness, or touch parser/runtime/downstream product
behavior.

## Internal Project Area Reviewed

Security/quality advisory tooling. No mismatch against the reviewed issue,
contract, handoff, or changed files created parser, analytics, workbook,
production, AI/coaching, or CodeQL-lifecycle ambiguity.

## Checks Run

```powershell
git status --short --branch --untracked-files=all
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
gh issue view 603 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body
gh issue view 330 --repo Tahjali11/Mythic-Edge --json number,title,state,url
py -m pytest -q tests\test_cwe_mapped_local_validation_profile.py tests\test_cwe_profile_advisory_report.py
py -m json.tool docs\security\cwe_mapped_local_validation_profile.v1.json
py tools\check_cwe_mapped_local_validation_profile.py docs\security\cwe_mapped_local_validation_profile.v1.json
py tools\generate_cwe_profile_advisory_report.py --write-report --report-date 2026-07-01
py -m json.tool docs\quality_reports\security\cwe_mapped_local_validation_profile\2026-07-01-024eda7-cwe-profile-advisory-report.json
py -m ruff check tools\generate_cwe_profile_advisory_report.py tests\test_cwe_profile_advisory_report.py
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

## Results

- Branch and base were synced: `0 0` against `origin/main`.
- Issue #603 and parent #330 were open at review time.
- Focused CWE profile/report tests passed: `32 passed`.
- Profile manifest JSON syntax validation passed.
- Existing profile validator passed: `families: 7`, `errors: 0`,
  `warnings: 0`.
- Report helper regenerated the expected public repo report artifact.
- Generated report JSON syntax validation passed.
- Ruff on changed Python helper/test files passed.
- `git diff --check` passed.
- Agent docs check passed with `errors: 0`, `warnings: 0`.
- Path-scoped protected-surface scan passed with `forbidden: 0`,
  `warnings: 0`.
- Path-scoped secret/private-marker scan passed with `forbidden: 0`,
  `warnings: 0`.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-603-000 | none | `not_reproduced` | No blocking contract mismatch found. | not_blocking | N/A | Contract, helper, tests, generated JSON report, focused validation, protected-surface scan, and secret/private-marker scan reviewed cleanly. | F |

## Confirmed Contract Matches

- `tools/generate_cwe_profile_advisory_report.py` consumes the default
  `docs/security/cwe_mapped_local_validation_profile.v1.json`, the existing
  `tools/check_cwe_mapped_local_validation_profile.py` validator result, and
  public Git metadata only.
- Non-default profile paths are blocked without echoing the raw supplied path.
- Unsupported modes return symbolic blocked advisory reports.
- The generated JSON report uses schema version
  `security_cwe_mapped_local_validation_profile_advisory_report.v1`.
- The generated report uses `run_mode: manifest_validator_advisory`,
  `overall_status: passed_advisory`, `profile_status: advisory_profile`,
  `profile_family_count: 7`, and validator result `passed` with zero errors
  and warnings.
- Family entries remain symbolic and repo-public: family IDs, CWE IDs/titles,
  CodeQL rule IDs, detector IDs, rollout status, reporting policy, and
  non-claims.
- Required non-claims are present, including no CodeQL alert mutation, no
  CodeQL zero-alert proof, no formal CWE compliance, no security assurance, no
  privacy assurance, no release readiness, no deploy readiness, no CI
  enforcement, and no parser/analytics/AI/coaching truth claim.
- Advisory-only booleans remain safe:
  `advisory_only: true`, `enforcement_authorized: false`,
  `ci_change_authorized: false`,
  `codeql_alert_mutation_authorized: false`,
  `security_assurance_claimed: false`, and
  `privacy_assurance_claimed: false`.
- The implementation did not change CI workflows, CodeQL alert state,
  `pyproject.toml`, parser/runtime behavior, analytics schema, workbook/webhook
  behavior, Apps Script/Sheets behavior, OpenAI/model-provider behavior,
  AI/coaching behavior, Line Tracer behavior, or production behavior.

## Contract Mismatches

None found.

## Missing Tests

No blocking missing tests found. Focused tests cover successful report
generation, schema/flag expectations, symbolic family entries, validator error
and warning preservation, unsupported mode blocking, non-default profile path
blocking without raw path echo, deterministic path naming, and no mutation of
the loaded profile.

## Advisory-Only Status

Confirmed. The implementation and generated report are advisory-only. They do
not claim CodeQL closure, security assurance, privacy assurance, release
readiness, deploy readiness, CI enforcement, parser truth, analytics truth, AI
truth, or coaching truth.

## Public-Safe Report Status

Confirmed. The generated report is repo-relative and symbolic. The review did
not find raw local paths, raw private values, raw SARIF, CodeQL API payloads,
raw logs, SQLite contents, workbook exports, secrets, endpoint values, runtime
artifacts, or local-only scanner outputs in the generated report.

## Drift Notes

- CodeQL lifecycle drift: none introduced. GitHub CodeQL closure remains
  outside this local advisory report.
- CI/enforcement drift: none introduced.
- Parser/runtime/downstream drift: none introduced.
- Issue lifecycle drift: #603 remains open pending submitter/deployer flow;
  parent #330 remains open.

## Recommendation

Approve for Codex F submitter. Codex F should stage only the reviewed #603
files and open a draft PR. Codex G, not this report, owns any future issue or
tracker closeout after PR review and merge gates.

## Remaining Risk

- GitHub Actions has not run for this local branch until Codex F submits it.
- The generated report is intentional and public-safe, but Codex F should stage
  only the reviewed report artifact and not any unrelated local outputs.
- Future scanner-summary aggregation remains deferred to a separate issue and
  contract.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #603.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/603

Parent security workflow:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Branch:
codex/cwe-profile-advisory-report-603

Base branch:
main

Reviewed contract:
docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md

Implementation handoff:
docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_report_comparison.md

Contract-test report:
docs/contract_test_reports/security_cwe_mapped_local_validation_profile_advisory_report.md

Generated advisory report:
docs/quality_reports/security/cwe_mapped_local_validation_profile/2026-07-01-024eda7-cwe-profile-advisory-report.json

Goal:
Stage only the reviewed #603 files, commit, push the branch, and open a draft
PR to the approved base. Do not merge, close #603, close parent #330, mutate
CodeQL alerts, enable CI enforcement, claim security/privacy assurance, or
target production behavior.

Before staging:
- Run git status --short --branch --untracked-files=all.
- Confirm the dirty set matches the reviewed #603 package.
- Exclude unrelated files and local/generated artifacts outside the reviewed
  advisory JSON report.

Recommended validation before submit:
- py -m pytest -q tests\test_cwe_mapped_local_validation_profile.py tests\test_cwe_profile_advisory_report.py
- py -m ruff check tools\generate_cwe_profile_advisory_report.py tests\test_cwe_profile_advisory_report.py
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over staged/reviewed files
- path-scoped secret/private-marker scan over staged/reviewed files

Open a draft PR using Refs #603 and Refs #330, not Closes, unless issue
closure has been explicitly authorized.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/603"
  parent_security_workflow: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/security_cwe_mapped_local_validation_profile_advisory_report.md"
  implementation_handoff: "docs/implementation_handoffs/security_cwe_mapped_local_validation_profile_advisory_report_comparison.md"
  artifact_produced: "docs/contract_test_reports/security_cwe_mapped_local_validation_profile_advisory_report.md"
  generated_report: "docs/quality_reports/security/cwe_mapped_local_validation_profile/2026-07-01-024eda7-cwe-profile-advisory-report.json"
  risk_tier: "High workflow and security-communication risk; low runtime risk"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/cwe-profile-advisory-report-603"
  reviewed_head: "024eda7d9408c0bb72d645af4d41d604539291ba"
  branch_sync: "0 0 with origin/main"
  validation:
    - "py -m pytest -q tests\\test_cwe_mapped_local_validation_profile.py tests\\test_cwe_profile_advisory_report.py -> passed, 32 passed"
    - "py -m json.tool docs\\security\\cwe_mapped_local_validation_profile.v1.json -> passed"
    - "py tools\\check_cwe_mapped_local_validation_profile.py docs\\security\\cwe_mapped_local_validation_profile.v1.json -> passed, families 7, errors 0, warnings 0"
    - "py tools\\generate_cwe_profile_advisory_report.py --write-report --report-date 2026-07-01 -> passed"
    - "py -m json.tool docs\\quality_reports\\security\\cwe_mapped_local_validation_profile\\2026-07-01-024eda7-cwe-profile-advisory-report.json -> passed"
    - "py -m ruff check tools\\generate_cwe_profile_advisory_report.py tests\\test_cwe_profile_advisory_report.py -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  advisory_only_status: "confirmed"
  public_safe_report_status: "confirmed"
  codeql_closure_claimed: false
  enforcement_authorized: false
  ci_changed: false
  codeql_alert_mutation_authorized: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  forbidden_scope_touched: false
  generated_private_artifacts_kept: false
  next_recommended_role: "Codex F: Module Submitter"
```
