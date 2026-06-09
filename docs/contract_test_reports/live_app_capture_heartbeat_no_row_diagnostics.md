# Live App Capture Heartbeat No-Row Diagnostics Contract-Test Report

## Findings

No blocking findings remain.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-302-003 | P2 | fixed_state_followup | fixed | not_blocking | Prior Codex E review found `progress["sqlite_write_attempt_count"]` incremented before `_write_live_facts(...)` and again in the ingest exception handler, so one failed approved ingest call could report two attempts. | `src/mythic_edge_parser/local_app/live_capture_control.py` now increments once before the approved ingest call and does not increment again in the exception handler. `tests/test_live_app_explicit_start_capture_control.py` adds `test_failed_live_ingest_counts_one_sqlite_write_attempt_without_leaking_error_text`, which verifies `sqlite_write_attempt_count == 1`, `last_no_write_reason == "sqlite_write_failed"`, safe public blurb text, safe `errors`, and no raw exception/path/SQL text in the response. Focused backend validation passed. | F |

## Role Performed

Codex E: Module Reviewer / confirmation thread.

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/302
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/294
- Prior narrow fixer PR: https://github.com/Tahjali11/Mythic-Edge/pull/306
- Branch: `codex/live-capture-diagnostics-restore-302`
- Base branch: `origin/codex/analytics-foundation`
- Worktree: sibling checkout `MythicEdge-live-capture-diagnostics-302`

## Contract And Handoff Reviewed

- Contract: `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`
- Implementation handoff: `docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md`
- Prior review artifact: `docs/contract_test_reports/live_app_capture_heartbeat_no_row_diagnostics.md`
- Fixer handoff: `docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_fixer.md`
- Repo authority: `AGENTS.md`, `docs/agent_rules.yml`, `docs/agent_constitution.md`, `docs/codex_module_workflow.md`, `docs/agent_threads/contract_test.md`, `docs/templates/contract_test_report.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

Issue #302 extends existing `GET /api/live/capture/status` additively with app-owned heartbeat, progress, no-row reason, and backend-led parser-status blurb metadata. The status route must stay read-only and privacy-safe. The feature must not implement #294 analytics auto-refresh, change parser truth ownership, change analytics schema/migrations, or touch workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.

## Files Reviewed

- `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`
- `docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md`
- `docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_fixer.md`
- `docs/contract_test_reports/live_app_capture_heartbeat_no_row_diagnostics.md`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `tests/test_live_app_explicit_start_capture_control.py`
- Adjacent validation-only tests: `tests/test_analytics_local_app_backend.py`, `tests/test_live_app_parser_owned_fact_capture_sqlite.py`, `tests/test_stream_unit.py`

## Fixed-State Verdict

CT-302-003 is fixed. Failed live SQLite ingest attempts now count the actual approved ingest call once, preserve `last_no_write_reason == "sqlite_write_failed"`, and do not expose raw exception text, SQL text, private paths, raw Player.log content, SQLite contents, secrets, env values, runtime artifacts, or local-only artifacts.

## Contract Matches

- Existing `GET /api/live/capture/status` remains the extended route; no new route was added.
- The top-level live-capture object keeps `live_app_explicit_start_capture_control.v1`; nested heartbeat/progress objects use `live_app_capture_heartbeat_no_row_diagnostics.v1`.
- GET status remains read-only in the reviewed implementation and focused tests still cover no app-data/SQLite creation for ready-state status checks.
- Heartbeat/progress/blurb fields are sanitized through backend state readers/writers before persistence or response exposure.
- Progress metadata is app-owned operational metadata; parser match/game truth ownership remains with parser/state.
- The failed-ingest counter now matches the approved #244 ingest-call boundary.
- The frontend validates required heartbeat/progress/blurb objects and renders backend-led blurb text without inventing match score or result copy.
- Start/stop controls remain governed by backend `start_allowed` and `stop_allowed`.
- #294 analytics auto-refresh and #304 Dashboard control are not implemented by this package.
- No parser event classes, parser final reconciliation, match/game identity, deduplication, analytics schema/migrations, workbook schema, webhook payload shape, Apps Script/Sheets, OpenAI/AI/coaching, Line Tracer, or production behavior changes were found.

## Remaining Mismatches

None found in this confirmation pass.

## Missing Tests Or Safeguards

- No missing required regression remains for CT-302-003; the failed-ingest counter and privacy boundary are covered.
- Live/private MTGA smoke was not run and is not required for this contract-test confirmation.

## Validation Run

- `git status --short --branch --untracked-files=all` -> active isolated #302 package on `codex/live-capture-diagnostics-restore-302`; expected modified/restored package files, no generated `frontend/dist`.
- `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation` -> `0 0`.
- `git diff --name-status` -> #302 contract/report/handoffs plus backend/frontend/test files.
- `py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py` -> 41 passed, 1 existing third-party warning.
- `py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_stream_unit.py` -> 12 passed.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> 3 files passed, 91 tests passed.
- `npm --prefix frontend run build` -> passed; `frontend/dist` removed after build.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed.
- Path-scoped protected-surface scan over #302 contract/report/handoffs and changed files -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over #302 contract/report/handoffs and changed files -> passed, forbidden 0, warnings 0.

## Protected-Surface Status

Path-scoped protected-surface scan passed with forbidden 0 and warnings 0. Review found no changes to parser truth, parser final reconciliation, parser event classes, match/game identity, deduplication, analytics schema/migrations, workbook/webhook/App Script/Sheets, OpenAI/AI/coaching, Line Tracer, or production behavior.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan over #302 contract/report/handoffs and changed files passed with forbidden 0 and warnings 0. No raw Player.log contents, raw JSONL payloads, raw private paths, raw hashes, SQL text, stack traces, secrets, env values, generated SQLite contents, runtime artifacts, workbook exports, or local-only artifacts were added by the reviewed package.

## Generated/Private Artifact Status

`frontend/dist` was created by build validation and removed. No generated database, runtime, raw log, Player.log, workbook export, failed-post, credential, or local-only artifacts were retained.

## Drift Notes

- Issue #294 analytics auto-refresh remains separate and was not implemented here.
- Issue #304 Dashboard live-capture control remains separate and was not restored here.
- No repo/workbook/deployment/local-data drift was identified inside the reviewed #302 package.

## Recommendation

Approve for Codex F submission. This does not authorize merge, issue closure, tracker updates, production behavior, live workbook changes, Apps Script changes, or real/private Player.log smoke.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #302.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/302

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/294

Prior narrow fixer PR:
https://github.com/Tahjali11/Mythic-Edge/pull/306

Worktree:
sibling checkout MythicEdge-live-capture-diagnostics-302

Source branch:
codex/live-capture-diagnostics-restore-302

Target branch:
codex/analytics-foundation

Reviewed contract:
docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md

Implementation handoff:
docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md

Fixer handoff:
docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_fixer.md

Review artifact:
docs/contract_test_reports/live_app_capture_heartbeat_no_row_diagnostics.md

Goal:
Submit the reviewed #302 live-capture heartbeat/no-row diagnostics package as a draft PR to codex/analytics-foundation. Stage only the reviewed #302 files and preserve unrelated local work.

Files expected in the reviewed package:
- docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md
- docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md
- docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_fixer.md
- docs/contract_test_reports/live_app_capture_heartbeat_no_row_diagnostics.md
- src/mythic_edge_parser/local_app/live_capture_control.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/api.test.ts
- frontend/src/App.tsx
- frontend/src/App.test.tsx
- tests/test_live_app_explicit_start_capture_control.py

Before staging:
- Confirm branch is codex/live-capture-diagnostics-restore-302.
- Confirm branch is even with origin/codex/analytics-foundation or clearly report if not.
- Confirm frontend/dist is absent.
- Confirm no raw Player.log, raw JSONL, SQLite DB, runtime artifact, workbook export, failed post, secret, credential, env file, or local-only artifact is present in the staged package.

Validation to rerun or cite from Codex E if unchanged:
py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_stream_unit.py
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over staged/reviewed files.
Remove frontend/dist after build validation if created.

Do not:
- stage unrelated files
- implement #294 auto-refresh
- start, stop, restart, tail, or control a real live watcher
- read, copy, hash, summarize, store, or expose raw Player.log contents
- expose raw/private/generated/local artifacts
- merge, close #302, close #294, update trackers as complete, target main, or deploy
- change parser truth, parser final reconciliation, parser event classes, match/game identity, analytics schema/migrations, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/production behavior

Open or update a draft PR targeting codex/analytics-foundation. Use Refs #302 unless the PR fully satisfies issue #302 closure criteria and the user explicitly approves stronger lifecycle language.

Final output:
- role performed
- branch and target branch
- files staged/committed
- commit hash
- PR URL
- validation run/result
- protected-surface status
- secret/private-marker status
- generated/private artifact status
- forbidden scope touched true/false
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / confirmation thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/302"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  prior_narrow_fixer_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/306"
  completed_thread: "E"
  next_thread: "F"
  worktree: "MythicEdge-live-capture-diagnostics-302"
  branch: "codex/live-capture-diagnostics-restore-302"
  base_branch: "origin/codex/analytics-foundation"
  contract_artifact: "docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_fixer.md"
  review_artifact: "docs/contract_test_reports/live_app_capture_heartbeat_no_row_diagnostics.md"
  findings_confirmed_fixed:
    - "CT-302-003 P2: failed SQLite ingest attempts no longer double-count sqlite_write_attempt_count."
  validation:
    - "backend/live focused tests -> 41 passed, 1 existing warning"
    - "live SQLite/stream tests -> 12 passed"
    - "frontend typecheck -> passed"
    - "frontend tests -> 91 passed"
    - "frontend build -> passed; frontend/dist removed"
    - "ruff -> passed"
    - "git diff --check -> passed"
    - "agent docs -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  recommendation: "Route to Codex F for draft PR submission."
```
