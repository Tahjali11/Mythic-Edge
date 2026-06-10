# Local App Live Capture Status Truthful Display Contract-Test Report

## Findings

| id | severity | status | finding | evidence | routing |
| --- | --- | --- | --- | --- | --- |
| CT-295-001 | P1 | fixed_state_followup | Disabled/status-only live SQLite capture evidence now outranks active-looking watcher/process booleans. | `frontend/src/App.tsx` checks blocked/unavailable/disabled/status-only/direct SQLite-write-disabled evidence at lines 3666-3696 before computing or returning `Capturing` at lines 3697-3705. `frontend/src/App.test.tsx` includes the conflicting disabled/status-only regression at lines 163-186. Focused frontend tests pass with 51 tests. | Route to Codex F. |

No blocking findings remain.

## Role Performed

Codex E: Module Reviewer / confirmation thread for issue #295.

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Issue Reviewed

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/295
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/294
- Branch: `codex/analytics-foundation`
- Risk tier: Medium

## Contract And Handoff Reviewed

- Contract: `docs/contracts/local_app_live_capture_status_truthful_display.md`
- Implementation handoff: `docs/implementation_handoffs/local_app_live_capture_status_truthful_display_comparison.md`
- Fixer handoff: `docs/implementation_handoffs/local_app_live_capture_status_truthful_display_fixer.md`

## Files Reviewed

- `docs/contracts/local_app_live_capture_status_truthful_display.md`
- `docs/implementation_handoffs/local_app_live_capture_status_truthful_display_comparison.md`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- `frontend/src/status.test.ts`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `tests/test_analytics_local_app_backend.py`

## Contract Matches

- The default local-app setup/status backend still reports live capture as readiness/status-only and does not start a watcher, tail Player.log, or enable SQLite live writes.
- The frontend no longer uses watcher readiness alone as proof of active capture in the known issue #295 case where SQLite writes are disabled.
- The added frontend tests cover the main regression: watcher readiness plus disabled SQLite writes does not become `Capturing`.
- The Codex D regression covers the stricter CT-295-001 conflict: disabled/status-only live SQLite capture wins even when watcher/process booleans look active.
- The frontend also covers strict active-capture evidence and malformed/missing live fields failing closed.
- No reviewed code path renders raw Player.log contents, raw private paths, generated DB contents, secrets, environment values, runtime artifacts, or local-only artifacts.
- Setup/status and diagnostics remain reachable without adding live watcher start/stop controls or destructive UI behavior.

## Contract Mismatches

None remaining for the reviewed #295 contract scope.

## Missing Tests Or Safeguards

- No missing focused test was identified for CT-295-001 after the Codex D regression.
- Manual browser/visual smoke was not run in this confirmation pass; this is a non-blocking residual review gap because the DOM-level frontend tests cover the contract behavior.

## Validation Run

| command | result |
| --- | --- |
| `git status --short --branch --untracked-files=all` | Branch is `codex/analytics-foundation`, behind origin by 9 commits. Worktree has mixed dirty files, including #295 frontend/report files and unrelated #281/error-report/roadmap changes. |
| `git diff --name-status` | Reviewed touched #295 files and noted unrelated dirty files remained present. |
| `gh issue view 295 --json number,state,title,url` | Issue #295 is open. |
| `gh issue view 294 --json number,state,title,url` | Related issue #294 is open. |
| `npm --prefix frontend run typecheck` | Passed. |
| `npm --prefix frontend test -- --run src/App.test.tsx src/status.test.ts` | Passed: 2 files, 51 tests. |
| `py -m pytest -q tests\test_analytics_local_app_backend.py` | Passed: 24 tests, 1 existing third-party deprecation warning. |
| `npm --prefix frontend run build` | Passed. |
| `git diff --check` | Passed. |
| `py tools\check_agent_docs.py` | Passed: 46 checked files, 0 errors, 0 warnings. |

## Protected-Surface Status

Path-scoped protected-surface scan over the #295 contract, report, fixer handoff, and touched frontend files passed with forbidden 0 and warnings 0.

Protected parser/runtime/analytics schema/live watcher/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production surfaces were not intentionally changed by this review.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan over the #295 contract, report, fixer handoff, and touched frontend files passed with forbidden 0 and warnings 0.

No raw Player.log contents, private paths, secrets, environment values, generated DB contents, runtime artifacts, workbook exports, or local-only artifacts were copied into this report.

## Generated Artifact Status

`frontend/dist` was created by build validation and removed before handoff.

## Forbidden Scope

Forbidden scope was not touched by this Codex E review. No implementation files were edited by this confirmation pass, no watcher was started or controlled, no private Player.log content was inspected, and no issues or branches were closed, staged, committed, pushed, merged, or targeted at main.

## Recommendation

Route to Codex F. CT-295-001 is confirmed fixed for the reviewed contract scope.

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / confirmation thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/295"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/local_app_live_capture_status_truthful_display.md"
  implementation_handoff: "docs/implementation_handoffs/local_app_live_capture_status_truthful_display_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/local_app_live_capture_status_truthful_display_fixer.md"
  review_artifact: "docs/contract_test_reports/local_app_live_capture_status_truthful_display.md"
  findings:
    - "CT-295-001 P1 fixed: disabled/status-only live SQLite capture evidence now outranks active-looking watcher/process booleans."
  validation:
    - "frontend typecheck -> passed"
    - "focused frontend tests -> passed, 51 tests"
    - "focused backend setup-status/local-app backend tests -> passed, 24 tests, 1 existing third-party warning"
    - "frontend build -> passed; frontend/dist removed"
    - "git diff --check -> passed"
    - "agent docs check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  recommendation: "Route to Codex F for reviewed submitter work."
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
```
