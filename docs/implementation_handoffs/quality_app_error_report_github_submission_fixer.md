# Quality App Error Report GitHub Submission Fixer Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/298

## Related Prior Issue

https://github.com/Tahjali11/Mythic-Edge/issues/281

## Contract

`docs/contracts/quality_app_error_report_github_submission.md`

## Review Artifact

`docs/contract_test_reports/quality_app_error_report_github_submission.md`

## Role Performed

Codex D: Module Fixer.

## Branch

`codex/analytics-foundation`

## Findings Fixed

- CT-298-001 P1: frontend API preview validation rejected the backend's ready-preview `external_submission_enabled: true` capability value.
- CT-298-002 P2: real `GhCliIssueSubmitter` command/temp-file boundary tests were incomplete.

## What The Contract Says

The local app may submit a GitHub Issue only after the operator has a sanitized ready preview. The backend must rebuild the preview server-side, keep the privacy guard in front of the external write, call local `gh issue create` through an argument-list subprocess targeting only `Tahjali11/Mythic-Edge`, and return only structured safe statuses. Automated tests must mock GitHub tooling and must not create a live issue.

The sanitized report is triage evidence only. It is not parser truth, analytics truth, live watcher truth, Match Journal truth, workbook truth, production readiness, or AI/coaching truth.

## What Changed In This D Pass

- Updated the frontend API preview validator to accept `external_submission_enabled` as a boolean, so the ready-preview response with `true` is compatible with the #298 submit capability.
- Added a frontend API regression for `previewErrorReport(...)` accepting a ready preview with `external_submission_enabled: true`.
- Extended backend tests for safe fallback statuses from missing/unauthenticated GitHub CLI, wrong-repo issue URL, generic submission failure, and missing baseline labels.
- Added focused tests around the real `GhCliIssueSubmitter` with mocked `shutil.which` and `subprocess.run`, proving:
  - auth and label checks use argument-list subprocess calls with `shell=False`;
  - label listing targets `--repo Tahjali11/Mythic-Edge`;
  - `gh issue create` targets `--repo Tahjali11/Mythic-Edge`;
  - the body is written to a temporary `issue-body.md`;
  - the temporary body file is removed after success and failure;
  - missing `gh`, unauthenticated `gh`, unavailable/wrong repo, and submission failure map to safe internal statuses.

## Files Changed By This D Pass

- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `tests/test_analytics_local_app_backend.py`
- `docs/implementation_handoffs/quality_app_error_report_github_submission_fixer.md`

The worktree already contained the broader #298 Codex C implementation package before this D pass. Those pre-existing modified/untracked #298 files were preserved and not reverted.

## Code Changed

Yes, but only one runtime line in the frontend API validator changed in this D pass:

- `frontend/src/api.ts`: `validateErrorReportPreviewResponse(...)` now requires `external_submission_enabled` to be boolean instead of requiring the old copy-only value `false`.

No backend production code changed in this D pass.

## Tests Added Or Updated

- `frontend/src/api.test.ts`: added a ready-preview API validation regression for `external_submission_enabled: true`.
- `tests/test_analytics_local_app_backend.py`: added safe GitHub-tool fallback coverage and real `GhCliIssueSubmitter` command/temp-file boundary tests with mocked subprocess/filesystem boundary.

## Interface Changes

No new interface changes were introduced by this D pass. It aligns frontend validation with the already-implemented #298 preview capability model.

## Contracted Area Status

Stayed inside the contracted Local App / UI and Quality / Developer Workflow surface. No parser, analytics schema/migration/ingest, live watcher behavior, live capture semantics, Match Journal truth ownership, workbook, webhook, Apps Script, Sheets, OpenAI, AI/coaching, Line Tracer, production, credential policy, or generated-artifact behavior was changed.

## Validation Run

```powershell
py -m pytest -q tests\test_analytics_local_app_backend.py
# 29 passed, 1 existing Starlette/httpx deprecation warning

npm --prefix frontend test -- --run src/api.test.ts
# 1 file passed, 32 tests passed

npm --prefix frontend run typecheck
# passed

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

Path-scoped protected-surface scan over the #298 package and this fixer artifact passed with `forbidden: 0` and `warnings: 0`.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan over the #298 package and this fixer artifact passed with `forbidden: 0` and `warnings: 0`.

## Generated Artifact Status

`npm --prefix frontend run build` created `frontend/dist`; it was removed before handoff. No generated build artifact is intended to be kept.

## Forbidden Scope

Forbidden scope was not touched. No live GitHub issue was created, no GitHub labels were created, and no staging, commit, push, PR, merge, issue close, or main-target action was performed.

## Still Unverified

- No manual live GitHub submission smoke was run, by contract.
- Codex E should re-review the dirty #298 package as a whole because this D pass intentionally did not isolate or submit files.

## Reviewer Focus

Codex E should confirm:

- the real `previewErrorReport(...)` path now accepts the backend ready-preview capability value;
- `GhCliIssueSubmitter` tests cover the required command/temp-file boundary without creating a live issue;
- no raw command output, private markers, local paths, tokens, or generated artifacts are exposed.

## Next Workflow Action

Next role: Codex E confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #298.

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

Fixer handoff:
docs/implementation_handoffs/quality_app_error_report_github_submission_fixer.md

Goal:
Confirm the D-pass fixes for CT-298-001 and CT-298-002 only. Verify the frontend API preview validator accepts the backend ready-preview external submission capability, and verify the mocked real GhCliIssueSubmitter boundary tests cover argument-list execution, fixed repo, temp body cleanup, unauthenticated gh, wrong repo, and generic failure without live GitHub issue creation.

Do not stage, commit, push, open a PR, merge, close issues, create GitHub labels, create a live GitHub Issue, target main, or broaden scope beyond #298 confirmation.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/298"
  related_prior_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/281"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/quality_app_error_report_github_submission.md"
  review_artifact: "docs/contract_test_reports/quality_app_error_report_github_submission.md"
  implementation_handoff: "docs/implementation_handoffs/quality_app_error_report_github_submission_fixer.md"
  findings_fixed:
    - "CT-298-001 P1: frontend API preview validation now accepts ready-preview external_submission_enabled true."
    - "CT-298-002 P2: real GhCliIssueSubmitter command/temp-file boundary now has mocked regression coverage."
  generated_artifacts_kept: false
  forbidden_scope_touched: false
```
