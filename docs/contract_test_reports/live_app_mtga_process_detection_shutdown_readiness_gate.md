# Live App MTGA Process Detection, Shutdown Readiness Gate Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/337

## Tracker

No separate tracker was named for this issue.

## Contract

`docs/contracts/live_app_mtga_process_detection_shutdown_readiness_gate.md`

## Implementation Under Test

Branch/worktree package under test:

- Branch: `codex/live-mtga-process-lifecycle-gate`
- Base branch: `codex/analytics-foundation`
- Implementation handoff: `docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_comparison.md`
- Fixer handoff: `docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_fixer.md`

Changed files reviewed:

- `docs/contracts/live_app_mtga_process_detection_shutdown_readiness_gate.md`
- `docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_comparison.md`
- `src/mythic_edge_parser/local_app/mtga_process_lifecycle.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/live_watcher_process.py`
- `src/mythic_edge_parser/local_app/live_watcher_diagnostics.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `tests/test_live_app_mtga_process_lifecycle.py`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Findings

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | evidence | expected_behavior | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-337-001 | P2 | `fixed_state_followup` | Fixed. Frontend MTGA process/lifecycle validators now enforce contract vocabulary and full automation-readiness checklist coverage. | not_blocking | Original evidence: `frontend/src/api.ts` accepted any string for `mtga_process.status`, `platform`, `evidence`, `detector`, warning/error entries, `automation_readiness.status`, readiness item keys/statuses, `mtga_lifecycle.status`, `mtga_process_status`, and `shutdown_reason`. | Verification evidence: `frontend/src/api.ts` now uses explicit allowed sets for MTGA process, lifecycle, shutdown, warning/error, and readiness values. `frontend/src/api.test.ts` rejects non-contract MTGA process labels, non-contract automation-readiness labels, incomplete readiness checklists, and non-contract lifecycle labels. Focused and full frontend validation passed. | F |

## Contract Summary

The implementation must add a Windows-only `MTGA.exe` image-name process detector, sanitized `mtga_process` and `mtga_lifecycle` status fields, a backend-owned 45-second reconnect window, safe app-owned shutdown after timeout, Diagnostics-first display, and an automation readiness gate that keeps auto-start blocked. It must not expose raw process output, PIDs, command lines, environment values, raw Player.log content, private paths, generated artifacts, or protected parser/runtime/analytics/workbook/AI behavior.

## Internal Project Area Reviewed

Internal project area: Local App / UI, specifically Live Player.log Mode lifecycle.

Adjacent areas reviewed:

- Parser: protected truth owner, not changed.
- Analytics: downstream local SQLite ingestion, schema/migrations not changed.
- Frontend: display and validation only.
- Quality / Governance: tests and durable report.

## Bridge-Code Status Reviewed

Bridge-code status: `bridge_code`.

The allowed bridge is:

```text
Windows MTGA process metadata-only signal
  -> backend live lifecycle state
  -> diagnostics/capture status response
  -> frontend read-only display and allowed manual controls
```

The implementation preserves this bridge at the backend level. CT-337-001 is fixed: frontend validators now enforce the contracted vocabulary for malformed/unsafe backend payloads.

## Branch Sync Assessment

Current branch: `codex/live-mtga-process-lifecycle-gate`

Branch sync:

- `git rev-list --left-right --count HEAD...codex/analytics-foundation` -> `0 2`
- `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation` -> `0 2`

Behind commits:

- `fae5fdc` merge PR #338 from `codex/advisory-import-boundary-report`
- `5315353` docs: add advisory import-boundary report

Assessment: the branch is behind by two #334 docs-only advisory import-boundary commits. They do not affect this #337 lifecycle implementation review, but Codex F should refresh or reconcile before publication/PR work.

## Checks Run

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...codex/analytics-foundation
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
git show --name-status --oneline --no-renames HEAD..origin/codex/analytics-foundation
gh issue view 337 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body
py -m pytest -q tests
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
```

Path-scoped protected-surface and secret/private-marker scans are recorded in the validation section below.

## Results

- Full Python test suite passed.
- Frontend typecheck passed.
- Frontend tests passed.
- Frontend build passed; generated `frontend/dist` was removed.
- Ruff passed.
- Diff check passed.
- Agent docs check passed.
- Protected-surface scan passed.
- Secret/private-marker scan passed.
- CT-337-001 fixed-state confirmation passed.
- No blocking contract mismatches remain.

## Confirmed Contract Matches

- Detector uses a fixed command vector: `tasklist /FI "IMAGENAME eq MTGA.exe" /NH`.
- Detector uses `shell=False` and a short timeout.
- Detector reports sanitized symbolic process status and does not expose raw stdout/stderr, PIDs, command lines, or environment values.
- Non-Windows detection returns `unsupported_platform` safely.
- Detector unavailable returns a sanitized unavailable/error code.
- `GET /api/live/watcher/process` adds `mtga_process` and blocked `automation_readiness`.
- `GET /api/live/watcher/diagnostics` includes Diagnostics-first MTGA process and automation blocked diagnostics.
- `GET /api/live/capture/status` includes `mtga_lifecycle`.
- Capture supervisor-owned lifecycle handles not-detected -> reconnect window -> timeout shutdown.
- Re-detection during the reconnect window continues capture without resetting parser state.
- Timeout shutdown stops only the app-owned capture supervisor path and preserves completed row-count metadata in tests.
- Player.log silence while MTGA is detected is not treated as failure; lifecycle checks occur during supervisor idle time without requiring new log rows.
- Automatic startup remains blocked: `automatic_start_allowed` / `automation_start_allowed` remain false.
- No live MTGA process was started, stopped, killed, or inspected during tests.
- No raw private Player.log content was read or exposed.
- Parser truth, parser final reconciliation, event classes, match/game identity, deduplication, analytics schema/migrations, workbook/webhook/App Script/Sheets, OpenAI/AI/coaching, Line Tracer, and production behavior were not changed.

## Contract Mismatches

### CT-337-001: Frontend validators do not enforce contracted MTGA vocabulary

Files:

- `frontend/src/api.ts`
- `frontend/src/api.test.ts`

Evidence:

- Original finding evidence: `isMtgaProcessStatus(...)`, `isAutomationReadiness(...)`, and `isMtgaLifecycle(...)` accepted arbitrary string values for contracted MTGA status/vocabulary fields.
- Fixed-state evidence: frontend validators now use explicit allowed sets for process status, platform, evidence, detector, process warning/error codes, lifecycle status, lifecycle process status, shutdown reason, lifecycle warning/error codes, automation-readiness status, item status, and exact checklist key ordering.
- Fixed-state tests now reject unsafe/non-contract MTGA process labels, readiness labels, incomplete readiness checklists, lifecycle labels, warning/error values, and `automation_start_allowed: true`.

Expected:

- `mtga_process.status` must be limited to `detected`, `not_detected`, `unsupported_platform`, `detector_unavailable`, or `unknown`.
- `mtga_process.evidence` must be limited to the approved evidence values.
- lifecycle status and shutdown reason must use the contract vocabulary.
- readiness item status must be limited to `pass`, `fail`, `blocked`, `not_proven`, `deferred`, or `not_applicable`.
- unsafe string labels should be rejected or safely redacted before UI consumption.

Blocking status:

- Fixed; no longer blocking Codex F.

## Missing Tests Or Safeguards

- No blocking missing tests remain for CT-337-001.
- Browser visual smoke was not rerun; this fixer only changed frontend API validation and fixtures, not primary UI layout.

## Privacy And Protected-Surface Assessment

Backend privacy boundary looks clean for the reviewed paths:

- no raw `tasklist` output returned;
- no PID values returned;
- no process command line or environment returned;
- no raw Player.log content returned;
- no raw private path, hash, SQL, stack trace, SQLite content, secret, endpoint value, env value, workbook export, or local-only artifact returned.

Frontend privacy boundary is strengthened by the CT-337-001 fix. Unsafe/free-form MTGA process/lifecycle/readiness strings now fail closed at API validation before UI consumption.

Protected-surface status:

- Parser/runtime truth ownership was not moved.
- Parser final reconciliation, event classes, match/game identity, deduplication, analytics schema/migrations, workbook/webhook/App Script/Sheets, output transport, production, OpenAI/model-provider, AI/coaching, Line Tracer, hidden-card inference, archetype inference, player-mistake labels, and gameplay advice were not changed.

## Drift Notes

- Branch drift: branch is behind `origin/codex/analytics-foundation` by two docs-only #334 commits. This is not a #337 blocker for review, but it is a publication/submitter freshness risk.
- Issue lifecycle drift: issue #337 remains open, as expected.
- Local artifact drift: `frontend/node_modules/` may exist as an ignored dependency directory from validation; it is not part of the implementation package.
- Generated artifact drift: `frontend/dist` was removed after build.

## Validation Evidence

- `py -m pytest -q tests` -> `1757 passed, 1 skipped, 1 warning`.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> `3 files passed, 96 tests passed`.
- `npm --prefix frontend run build` -> passed.
- `frontend/dist` cleanup -> removed.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed, `errors: 0`, `warnings: 0`.

Fixed-state confirmation validation:

- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run src/api.test.ts src/App.test.tsx` -> `2 files passed`, `95 tests passed`.
- `npm --prefix frontend run test -- --run` -> `3 files passed`, `99 tests passed`.
- `npm --prefix frontend run build` -> passed.
- `frontend/dist` cleanup -> removed.
- `py -m pytest -q tests\test_live_app_mtga_process_lifecycle.py tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py tests\test_analytics_auto_refresh_after_match_completion.py` -> `54 passed`, `1 warning`.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed, `errors: 0`, `warnings: 0`.

## Recommendation

Recommendation: approve for Codex F.

Next role: Codex F / Module Submitter.

Fixed-state verdict:

- CT-337-001 is fixed.
- No blocking findings remain.

Codex F should preserve the note that this branch is behind `origin/codex/analytics-foundation` by two #334 docs-only commits and refresh/reconcile as part of submitter hygiene before publication.

## Next Workflow Action

Next role: Codex F / Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #337.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/337

Branch:
codex/live-mtga-process-lifecycle-gate

Base branch:
codex/analytics-foundation

Contract:
docs/contracts/live_app_mtga_process_detection_shutdown_readiness_gate.md

Review artifact:
docs/contract_test_reports/live_app_mtga_process_detection_shutdown_readiness_gate.md

Implementation handoffs:
docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_comparison.md
docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_fixer.md

Goal:
Submit the reviewed #337 package. Stage only the reviewed files, commit, push, and open or update a draft PR to the approved base branch. Preserve the branch-sync note: this branch was behind origin/codex/analytics-foundation by two #334 docs-only commits during review, so refresh/reconcile before PR publication if needed.

Review focus:
- Stage only the #337 contract, implementation handoffs, review report, backend/frontend files, and focused tests.
- Do not stage unrelated local/generated files.
- Keep auto-start blocked.
- Do not target main.
- Do not close #337; route lifecycle closeout to Codex G after PR review/merge readiness.

Suggested validation:
git status --short --branch --untracked-files=all
git diff --check
py tools/check_agent_docs.py

Do not:
- edit implementation unless explicitly asked
- start, stop, restart, tail, or control a real live watcher
- start, stop, kill, or control MTGA or unrelated local processes
- read/copy/hash/tail/summarize raw Player.log contents
- expose raw/private/generated/local artifacts or secrets
- merge, close #337, or target main
- change parser behavior, parser final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations/ingest, workbook/webhook/App Script/Sheets behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice

Final output:
- branch, commit, PR URL, target branch
- files staged
- validation result
- generated/private artifact status
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/337"
  completed_thread: "E"
  next_thread: "F"
  role_performed: "Codex E: Module Reviewer / confirmation thread"
  contract_artifact: "docs/contracts/live_app_mtga_process_detection_shutdown_readiness_gate.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/live_app_mtga_process_detection_shutdown_readiness_gate_fixer.md"
  review_artifact: "docs/contract_test_reports/live_app_mtga_process_detection_shutdown_readiness_gate.md"
  branch: "codex/live-mtga-process-lifecycle-gate"
  base_branch: "codex/analytics-foundation"
  findings_fixed:
    - "CT-337-001 P2: frontend MTGA process/lifecycle validators now enforce contracted process/lifecycle/readiness vocabulary and full checklist coverage."
  validation:
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run src/api.test.ts src/App.test.tsx -> passed, 95 tests"
    - "npm --prefix frontend run test -- --run -> passed, 99 tests"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "focused backend lifecycle/local-app pytest -> passed, 54 tests, 1 existing warning"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  branch_sync_note: "branch is behind origin/codex/analytics-foundation by two #334 docs-only commits"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter"
```
