# Live App Explicit Start Capture Control Contract-Test Report

## Findings

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | evidence | expected behavior | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-297-001 | P1 | fixed_state_confirmation | fixed | not_blocking | `src/mythic_edge_parser/local_app/live_capture_control.py` now reads and writes state-derived `warnings`, `errors`, and `last_result` through safe label/map sanitizers. Focused regression `test_capture_status_redacts_unsafe_state_warning_error_and_result_text` passed, and a synthetic temp-root API check showed the unsafe sentinel was not echoed while redaction labels were present. | Live capture status/start/stop responses must not echo unsafe strings from app-data capture state. | F after validation caveat is addressed or separated |
| CT-297-002 | P2 | fixed_state_confirmation | fixed | not_blocking | `_player_log_ready(...)` now passes only `configured_exists`, and `_configured_player_log_path(...)` no longer falls back to the detected default Player.log. Focused regression `test_start_capture_requires_configured_player_log_not_detected_default` passed, and a synthetic temp-root check showed detected-default monitor evidence remained read-only while capture start was blocked. | Start capture must require an explicit configured `player_log_path`; detected/default Player.log evidence may stay read-only monitor evidence only. | F after validation caveat is addressed or separated |
| VE-297-001 | P2 | validation_caveat | open | blocks_clean_submitter_validation | `npm --prefix frontend test -- --run src/App.test.tsx src/status.test.ts` failed: 36 existing `App.test.tsx` cases still expect older first-screen route behavior such as always-visible review/import controls. A focused #297 live-capture UI subset ran 3 passing capture-control tests and 1 non-capture route-drift failure; `status.test.ts`, typecheck, and build passed. | Current submitter validation should either update/separate the unrelated frontend route-test drift or explicitly scope #297 submission away from that dirty UI work. | D or owning frontend thread before F if full frontend test green is required |

No #297 privacy/start-precondition blocking findings remain.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/297

## Tracker

Historical trackers:

- https://github.com/Tahjali11/Mythic-Edge/issues/204
- https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/live_app_explicit_start_capture_control.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Changed-file set reviewed:

- `docs/contracts/live_app_explicit_start_capture_control.md`
- `docs/implementation_handoffs/live_app_explicit_start_capture_control_comparison.md`
- `docs/implementation_handoffs/live_app_explicit_start_capture_control_fixer.md`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_live_app_explicit_start_capture_control.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

## Report Lifecycle

`report_lifecycle`: `fixed_state_confirmation_with_validation_caveat`

## Contract Summary

Issue #297 authorizes a high-risk but local-only explicit operator control for live capture. `Start capture` must happen only through explicit local operator action, must fail closed on unsafe or incomplete preconditions, may write only approved parser-owned completed match/game facts into local SQLite, and must not expose raw Player.log content, private paths, raw hashes, generated DB contents, secrets, stack traces, or local-only artifacts. `Stop capture` must be bounded to a verified app-owned supervisor and must not become a kill/reset/delete/cleanup tool.

## Contract Matches

- Start capture remains explicit and local: no automatic watcher start, startup auto-run, hidden process control, or background auto-capture was introduced.
- Status/start/stop payloads now sanitize state-derived warning/error/result fields before API exposure.
- Detected default Player.log remains a read-only monitor signal and no longer satisfies the start precondition.
- Start succeeds only when the Player.log path is explicitly configured and other safe preconditions pass.
- Stop remains bounded to the app-owned registered supervisor path.
- No destructive capture routes or controls such as restart/reset/kill/delete/cleanup were found.
- Backend responses and frontend display use symbolic/redacted display values and do not render raw Player.log content, raw private paths, raw hashes, SQLite contents, secrets, stack traces, or local-only artifacts.
- Focused tests cover the fixed unsafe-state redaction and configured-path precondition regressions.

## Contract Mismatches

None remaining for CT-297-001 or CT-297-002.

## Missing Tests Or Safeguards

- The broad frontend `App.test.tsx` suite currently has route/navigation expectation drift in this dirty worktree. That is not a reproduced #297 capture-control privacy or start-precondition regression, but it blocks a clean all-suggested-validation claim.
- Real/private Player.log smoke, live browser smoke, and long-running real MTGA session behavior remain unverified and intentionally out of scope for this confirmation.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
git diff --name-status
gh issue view 297 --json number,state,title,url
py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py tests\test_live_app_parser_owned_fact_capture_sqlite.py
py -m pytest -q tests\test_runner.py tests\test_tailer.py
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run src/App.test.tsx src/status.test.ts
npm --prefix frontend test -- --run src/status.test.ts
npm --prefix frontend test -- --run src/App.test.tsx -t "live capture|Start capture|Stop capture|watcher readiness|capture ownership"
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over the #297 package
path-scoped secret/private-marker scan over the #297 package
synthetic temp-root unsafe-state redaction check
synthetic temp-root detected-default start-precondition check
```

Results:

- Branch: `codex/analytics-foundation`, even with `origin/codex/analytics-foundation`.
- Issue #297: open.
- Worktree: mixed dirty state, including unrelated error-report files and frontend route/IA dirt. This is a submitter/staging risk.
- Focused backend/live pytest: passed, 44 tests, 1 existing FastAPI/Starlette deprecation warning.
- Runner/tailer pytest: passed, 26 tests.
- Frontend typecheck: passed on rerun.
- Frontend broad `App.test.tsx` plus `status.test.ts`: failed, 36 `App.test.tsx` route/navigation expectation failures; `status.test.ts` passed.
- Focused live-capture UI subset: 3 capture-control tests passed; 1 non-capture route-drift assertion failed because the old `Refresh History` control is no longer first-screen visible.
- Frontend build: passed; `frontend/dist` was removed.
- Ruff: passed.
- `git diff --check`: passed.
- Agent docs check: passed.
- Path-scoped protected-surface scan over 13 #297 paths: passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over 13 #297 paths: passed, forbidden 0, warnings 0.
- Synthetic unsafe-state API check: unsafe sentinel echoed false; warning/error redaction present true; no raw private value echoed. The safe schema field `raw_path_exposed` remains expected metadata.
- Synthetic detected-default API check: monitor reported detected evidence, capture status was blocked, `start_allowed` false, start accepted false, not-configured reason present, and no detected path value echoed.

## Protected-Surface Status

Path-scoped protected-surface scan over the #297 package, including this report, passed with forbidden 0 and warnings 0.

No implementation review evidence showed changes to parser behavior, parser final reconciliation, analytics schema/migrations outside the approved live-capture control scope, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, hidden-card inference, archetype inference, player-mistake labels, or gameplay advice.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan over the #297 package, including this report, passed with forbidden 0 and warnings 0.

The confirmed D fix removes the previously reproduced state-derived warning/error/result echo path from status/start/stop responses.

## Generated Artifact Status

`frontend/dist` was created by build validation and removed. No generated SQLite database, raw Player.log, app-data file, runtime artifact, workbook export, or local-only artifact was intentionally retained in the repo by this review.

## Forbidden Scope

Forbidden scope was not touched by this Codex E review. No implementation files were edited, no real watcher was started or stopped, no real/private Player.log content was read, copied, hashed, summarized, or exposed, and no staging, commit, push, PR, merge, issue closure, or main-targeting action was performed.

## Recommendation

For #297 itself, CT-297-001 and CT-297-002 are fixed and no additional #297 Codex D work is required for those findings.

Do not route to Codex F as a clean submitter handoff until the current frontend route/test drift is either fixed by the owning frontend thread or explicitly separated from the #297 submission. If full frontend validation is required for this branch state, route VE-297-001 to Codex D or the owning frontend IA thread first. If F can stage only the clean #297 package and leave unrelated frontend dirt out, route to Codex F with the validation caveat visible.

## Next Workflow Action

Next role: Codex F only after the validation caveat is resolved or intentionally separated; otherwise Codex D / owning frontend thread for VE-297-001.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/297"
  completed_thread: "E"
  next_thread: "F_or_D"
  branch: "codex/analytics-foundation"
  source_artifact: "docs/contracts/live_app_explicit_start_capture_control.md"
  prior_review_artifact: "docs/contract_test_reports/live_app_explicit_start_capture_control.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_explicit_start_capture_control_fixer.md"
  report_updated: "docs/contract_test_reports/live_app_explicit_start_capture_control.md"
  fixed_findings_confirmed:
    - "CT-297-001 P1: status/start/stop responses no longer echo unsafe warning/error/last_result strings from app-data capture state."
    - "CT-297-002 P2: start capture now requires explicit configured player_log_path; detected default Player.log remains read-only monitor evidence."
  validation:
    - "focused backend/live pytest -> passed, 44 passed, 1 existing warning"
    - "runner/tailer pytest -> passed, 26 passed"
    - "frontend typecheck -> passed on rerun"
    - "frontend build -> passed; frontend/dist removed"
    - "ruff, git diff --check, agent docs -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "synthetic unsafe-state check -> unsafe sentinel not echoed; redaction labels present"
    - "synthetic detected-default check -> start blocked without explicit configured player_log_path"
  validation_caveat:
    - "broad frontend App.test.tsx route/navigation expectations currently fail in dirty worktree; not a reproduced #297 privacy/start-precondition regression, but blocks clean submitter validation unless resolved or separated"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex F if unrelated frontend validation drift is separated; otherwise Codex D/owning frontend thread for VE-297-001"
```
