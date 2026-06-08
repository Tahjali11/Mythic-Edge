# Quality App Error Report GitHub Submission Contract-Test Report

## Findings

No blocking findings remain.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-298-001 | P1 | `fixed_state_followup` | Fixed. `previewErrorReport(...)` now accepts ready-preview responses with `external_submission_enabled: true` while malformed preview responses remain rejected. | not_blocking | Initial review found `src/mythic_edge_parser/local_app/error_reports.py` returned ready previews with `external_submission_enabled: true`, while `frontend/src/api.ts` rejected any preview where that value was not exactly `false`. | `frontend/src/api.ts` now requires `external_submission_enabled` to be a boolean. `frontend/src/api.test.ts` adds `accepts ready error-report previews when external submission is enabled`. Validation: focused frontend API/App tests, full frontend tests, typecheck, and build passed. | F |
| CT-298-002 | P2 | `fixed_state_followup` | Fixed. The real `GhCliIssueSubmitter` command/temp-file boundary now has mocked regression coverage without live GitHub issue creation. | not_blocking | Initial review found backend tests exercised an injected fake submitter but did not mock `subprocess.run` / `shutil.which` around `GhCliIssueSubmitter` itself. | `tests/test_analytics_local_app_backend.py` now covers auth/label argument-list commands, fixed `--repo Tahjali11/Mythic-Edge`, `shell=False`, body-file creation, temp body cleanup after success and failure, missing `gh`, unauthenticated `gh`, wrong repo, missing labels, and generic submission failure. Validation: backend pytest passed with 29 tests. | F |

## Role Performed

Codex E: Module Reviewer / confirmation thread.

## Issue And Related Prior Issue

- Issue reviewed: https://github.com/Tahjali11/Mythic-Edge/issues/298
- Related prior issue: https://github.com/Tahjali11/Mythic-Edge/issues/281
- Issue state checked during this pass: open.

## Contract And Handoff Reviewed

- Contract: `docs/contracts/quality_app_error_report_github_submission.md`
- Prior review artifact: `docs/contract_test_reports/quality_app_error_report_github_submission.md`
- Fixer handoff: `docs/implementation_handoffs/quality_app_error_report_github_submission_fixer.md`
- Prior contract context: `docs/contracts/quality_app_submit_error_report_codex_triage.md`

## Files Reviewed

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`
- `docs/contracts/quality_app_error_report_github_submission.md`
- `docs/contract_test_reports/quality_app_error_report_github_submission.md`
- `docs/implementation_handoffs/quality_app_error_report_github_submission_fixer.md`
- `src/mythic_edge_parser/local_app/error_reports.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The #298 slice may add explicit local GitHub Issue submission only after the operator previews a sanitized report. The backend must rebuild the preview server-side, run the privacy guard before any external write, invoke local `gh issue create` through a fixed-repo argument list, return only safe structured statuses, and preserve copy fallback. Automated tests must mock GitHub submission and must not create live GitHub issues.

## Fixed-State Verdict

- CT-298-001: fixed.
- CT-298-002: fixed.

The #298 package is ready to route to Codex F for submitter work, subject to F staging only the reviewed #298 files and preserving unrelated worktree state.

## Contract Matches

- `POST /api/feedback/error-report/submit` exists and is local-app scoped.
- Submit rebuilds the preview server-side and refuses invalid or privacy-blocked previews before calling GitHub tooling.
- The frontend preview API now accepts the #298 ready-preview capability value and still validates malformed responses.
- The frontend submit flow remains preview-first, explicit, and local-operator initiated only.
- `Submit report to GitHub` is shown only after a ready preview with external submission enabled.
- Copy fallback remains available after ready preview and failed submission states.
- Automated tests use mocked submitters and mocked CLI subprocess boundaries; no live GitHub issue was created.
- The real CLI wrapper uses argument-list subprocess execution with `shell=False`, fixed `--repo Tahjali11/Mythic-Edge`, safe `--body-file`, timeout, and no raw stdout/stderr returned to API responses.
- The temporary issue body file is covered by tests for cleanup after success and failure.
- Missing `gh`, unauthenticated `gh`, wrong repo, unavailable labels, privacy-blocked requests, invalid requests, and generic submission failures return safe statuses/fallbacks.
- No GitHub tokens are stored, no labels are created dynamically, and no attachments/screenshots are introduced.
- Parser/runtime/analytics schema/ingest/live watcher/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior was not changed.

## Remaining Mismatches

None found in this confirmation pass.

## Missing Tests Or Safeguards

None blocking. Live GitHub submission remains intentionally unverified because the contract forbids live issue creation in automated tests and this prompt did not authorize a manual live submission smoke.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
# branch codex/analytics-foundation; #298 files modified/untracked; no staging performed

git diff --name-status
# #298 backend/frontend/test files modified; #298 contract/report/handoffs untracked

gh issue view 298 --json number,title,state,url
# open; [quality/app] Submit sanitized error reports to GitHub Issues

py -m pytest -q tests\test_analytics_local_app_backend.py
# 29 passed, 1 existing Starlette/httpx deprecation warning

npm --prefix frontend run typecheck
# passed

npm --prefix frontend test -- --run src/api.test.ts src/App.test.tsx
# 2 files passed, 82 tests passed

npm --prefix frontend test -- --run
# 3 files passed, 86 tests passed

npm --prefix frontend run build
# passed; frontend/dist removed after build

py -m ruff check src tests tools
# All checks passed

git diff --check
# passed

py tools\check_agent_docs.py
# passed
```

## Protected-Surface Status

Path-scoped protected-surface scan over the #298 contract, report, fixer handoff, backend, frontend, and test files passed with `forbidden: 0` and `warnings: 0`.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan over the #298 contract, report, fixer handoff, backend, frontend, and test files passed with `forbidden: 0` and `warnings: 0`.

## Generated Artifact Status

`npm --prefix frontend run build` created `frontend/dist`; it was removed before this report update. No generated frontend build artifact is intended for commit.

## Forbidden Scope

Forbidden scope was not touched during this Codex E confirmation pass. No implementation files were edited, no staging/commit/push/PR/merge/issue close was performed, no live GitHub issue submission was run, no GitHub labels were created, and no main-target work occurred.

## Recommendation

Approve for Codex F: Module Submitter.

Codex F should stage only the reviewed #298 package and open/update a draft PR targeting `codex/analytics-foundation`. Codex F should not close issue #298 or perform deployer/tracker lifecycle work.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #298.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/298

Related prior issue:
https://github.com/Tahjali11/Mythic-Edge/issues/281

Branch:
codex/analytics-foundation

Contract:
docs/contracts/quality_app_error_report_github_submission.md

Review artifact:
docs/contract_test_reports/quality_app_error_report_github_submission.md

Implementation handoffs:
- docs/implementation_handoffs/quality_app_error_report_github_submission_comparison.md
- docs/implementation_handoffs/quality_app_error_report_github_submission_fixer.md

Goal:
Stage only the reviewed #298 files, commit them, push a module branch, and open/update a draft PR targeting codex/analytics-foundation. Do not merge, close issues, create live GitHub issues, create labels, or target main.

Reviewed files to stage:
- docs/contracts/quality_app_error_report_github_submission.md
- docs/implementation_handoffs/quality_app_error_report_github_submission_comparison.md
- docs/implementation_handoffs/quality_app_error_report_github_submission_fixer.md
- docs/contract_test_reports/quality_app_error_report_github_submission.md
- src/mythic_edge_parser/local_app/error_reports.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_local_app_backend.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/api.test.ts
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx

Validation to confirm before submit:
- git status --short --branch --untracked-files=all
- py -m pytest -q tests\test_analytics_local_app_backend.py
- npm --prefix frontend run typecheck
- npm --prefix frontend test -- --run
- npm --prefix frontend run build
- py -m ruff check src tests tools
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface and secret/private-marker scans over staged #298 files
- remove frontend/dist after build validation if created

Do not:
- stage unrelated files
- create live GitHub issues
- run live external submission
- store GitHub tokens
- create labels dynamically
- expose raw/private/generated/local artifacts
- change parser/runtime/analytics schema/ingest/live watcher/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior
- merge, close #298, or target main

Final output:
- role performed
- branch and commit
- PR URL and target branch
- files staged
- validation run and result
- protected-surface and secret/private-marker status
- generated artifact status
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/298"
  related_prior_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/281"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/quality_app_error_report_github_submission.md"
  review_artifact: "docs/contract_test_reports/quality_app_error_report_github_submission.md"
  implementation_handoffs:
    - "docs/implementation_handoffs/quality_app_error_report_github_submission_comparison.md"
    - "docs/implementation_handoffs/quality_app_error_report_github_submission_fixer.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  fixed_findings_confirmed:
    - "CT-298-001 P1: frontend API preview validation accepts ready-preview external_submission_enabled true."
    - "CT-298-002 P2: real GhCliIssueSubmitter command/temp-file boundary has mocked regression coverage."
  validation:
    - "gh issue view 298 -> open"
    - "backend pytest -> 29 passed, 1 existing warning"
    - "frontend typecheck -> passed"
    - "focused frontend tests -> 82 passed"
    - "full frontend tests -> 86 passed"
    - "frontend build -> passed; frontend/dist removed"
    - "ruff -> passed"
    - "git diff --check -> passed"
    - "agent docs check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter"
```
