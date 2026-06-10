# Contract Test Report: Live App Frontend Capture Operator Workflow Refresh

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/321

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

## Contract

`docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Changed files reviewed:

- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md`
- `docs/implementation_handoffs/live_app_frontend_capture_operator_workflow_refresh_comparison.md`

Reference surfaces inspected:

- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `frontend/src/api.test.ts`
- GitHub issue #321 and tracker #136
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/review.md`
- `docs/templates/contract_test_report.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Findings

No blocking findings.

## Contract Summary

The #321 contract requires a frontend-only operator workflow refresh for manual
live capture. The Dashboard may expose explicit Start/Stop controls only through
existing backend-authorized local routes, must fail closed for stale, blocked,
unavailable, malformed, and contradictory states, must keep Diagnostics and
manual refresh reachable, and must not claim parser, row-write, analytics,
workbook, AI, or production truth that the backend has not supplied.

## Internal Project Area Reviewed

Local App / UI, with bridge-code consumption of backend live-capture status and
analytics refresh-state. No parser, workbook, webhook, Apps Script, Sheets,
AI/coaching, Line Tracer, or production truth ownership moved.

## Bridge-Code Status Reviewed

The contract labels this slice `bridge_code`. The implementation handoff labels
it `shared_support`, but the handoff's truth-owner text and actual diff stay
within the frontend display/control surface. This vocabulary mismatch is
non-blocking because it does not create scope, truth-owner, or protected-surface
ambiguity in the reviewed implementation.

## Checks Run

```text
git fetch --prune origin
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
gh issue view 321 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body
gh issue view 136 --repo Tahjali11/Mythic-Edge --json number,title,state,url
git diff --name-status
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over #321 contract, handoff, report, and touched frontend files
path-scoped secret/private-marker scan over #321 contract, handoff, report, and touched frontend files
```

## Results

- Branch confirmed: `codex/analytics-foundation`
- Branch sync: `0 0` against `origin/codex/analytics-foundation`
- Issue #321 state: open
- Tracker #136 state: open
- `npm --prefix frontend run typecheck`: passed
- `npm --prefix frontend run test -- --run`: passed, 3 files and 96 tests
- `npm --prefix frontend run build`: passed
- `frontend/dist`: removed after build validation
- `git diff --check`: passed
- `py tools\check_agent_docs.py`: passed, errors 0, warnings 0
- Path-scoped protected-surface scan: passed, forbidden 0, warnings 0
- Path-scoped secret/private-marker scan: passed, forbidden 0, warnings 0

## Finding Lifecycle Summary

No findings recorded.

## Confirmed Contract Matches

- Dashboard load does not call `startCapture` or `stopCapture`; the updated test
  pins this at `frontend/src/App.test.tsx`.
- Dashboard Start/Stop controls remain explicit operator actions and are
  selected from backend `capture.status`, `capture.running`,
  `capture.start_allowed`, and `capture.stop_allowed`.
- Pending start and stop states disable repeat clicks while the POST is in
  flight and reconcile from returned backend `capture_status`.
- Stale capture state remains `Needs review`, does not become Ready or
  Capturing, does not expose enabled Start/Stop/Restart, and keeps the
  Diagnostics link reachable.
- The Dashboard Live capture tile now preserves the exact backend-led
  `Most recent completed match was recorded.` line instead of collapsing it to
  generic active-capture copy.
- The recorded-match test verifies the tile does not invent score text or
  current-match score text.
- Backend reference code still emits the recorded-match blurb only for
  `capturing` status with positive SQLite rows written.
- Frontend API validation still rejects unsafe live-capture blurb text containing
  private paths or unsafe local markers.
- No backend route shapes, parser runtime behavior, analytics schema or ingest,
  live watcher behavior, workbook/webhook/App Script/Sheets behavior,
  OpenAI/AI/coaching behavior, Line Tracer behavior, or production behavior
  changed in the reviewed diff.
- No raw Player.log contents, raw JSONL payloads, raw private paths, raw hashes,
  generated SQLite contents, runtime artifacts, workbook exports, secrets,
  endpoint values, environment values, or local-only artifacts are rendered by
  the changed code.

## Contract Mismatches

None blocking.

Non-blocking note: the implementation handoff's `Bridge-Code Status` value is
`shared_support` while the contract uses `bridge_code`. The reviewed code and
tests still follow the contract's frontend-only bridge boundary.

## Missing Tests

No blocking missing tests.

Residual non-blocking gap: no live browser smoke was run in this Codex E pass.
The review relied on DOM/unit tests and production build validation. The Codex C
handoff also marked live browser smoke as unverified.

## Drift Notes

- Repo drift: none found in the reviewed #321 scope.
- Workbook/deployment/local-data drift: not applicable; this was a frontend-only
  local app review and did not inspect or mutate live workbook, deployment, or
  private app-data state.
- Issue lifecycle drift: none. Issue #321 and tracker #136 remain open, as
  expected for Codex E.
- PR lifecycle drift: no PR was reviewed in this thread.

## Protected-Surface Assessment

Protected parser/runtime/analytics schema/live watcher/backend route/workbook/
webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/production surfaces
were not touched by the reviewed implementation diff.

## Privacy Assessment

The changed code is frontend display/test-only and does not add raw private
artifact rendering. Existing API validation and frontend tests continue to
guard against raw Player.log content, raw private paths, raw hashes, unsafe
diagnostic details, arbitrary SQL/database browsing, and local-only artifact
exposure.

## Generated Artifact Status

`frontend/dist` was created by build validation and removed afterward. No
generated frontend build artifacts are kept.

## Forbidden Scope

Forbidden scope touched: false.

## Recommendation

Approve for Codex F / Module Submitter.

The reviewed package satisfies the #321 contract as a frontend-only operator
workflow refresh. Codex F should stage only:

- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md`
- `docs/implementation_handoffs/live_app_frontend_capture_operator_workflow_refresh_comparison.md`
- `docs/contract_test_reports/live_app_frontend_capture_operator_workflow_refresh.md`

Codex F should not close #321 or tracker #136; lifecycle closeout belongs to
Codex G after PR review, merge readiness, and merge evidence.

## Next Workflow Action

Next role: Codex F / Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #321.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/321

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Reviewed contract:
docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md

Implementation handoff:
docs/implementation_handoffs/live_app_frontend_capture_operator_workflow_refresh_comparison.md

Codex E review artifact:
docs/contract_test_reports/live_app_frontend_capture_operator_workflow_refresh.md

Goal:
Submit the reviewed #321 frontend-only operator workflow refresh package. Stage
only the reviewed #321 files, commit them, push the branch or an appropriate
topic branch if required by current repo branch policy, and open/update a draft
PR targeting the approved non-main integration branch.

Reviewed files to stage only:
- frontend/src/App.tsx
- frontend/src/App.test.tsx
- docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md
- docs/implementation_handoffs/live_app_frontend_capture_operator_workflow_refresh_comparison.md
- docs/contract_test_reports/live_app_frontend_capture_operator_workflow_refresh.md

Validation evidence from Codex E:
- frontend typecheck passed
- full frontend tests passed, 96 tests
- frontend build passed; frontend/dist removed
- git diff --check passed
- agent docs check passed
- path-scoped protected-surface scan passed
- path-scoped secret/private-marker scan passed

Do not:
- stage unrelated files
- target main
- close issue #321 or tracker #136
- merge the PR
- change backend route shapes, parser behavior, analytics schema/ingest, live watcher behavior, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/production behavior
- expose raw/private/generated/local artifacts

Final output must include branch, commit hash, PR URL, target branch, validation status, generated artifact status, forbidden-scope confirmation, next recommended role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/321"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "E"
  next_thread: "F"
  role_performed: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/live_app_frontend_capture_operator_workflow_refresh.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_frontend_capture_operator_workflow_refresh_comparison.md"
  review_artifact: "docs/contract_test_reports/live_app_frontend_capture_operator_workflow_refresh.md"
  branch: "codex/analytics-foundation"
  branch_sync: "0 0"
  findings: []
  verdict: "approved_for_codex_f"
  validation:
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> passed, 3 files, 96 tests"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed, errors 0, warnings 0"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  browser_smoke: "not_run"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter"
```
