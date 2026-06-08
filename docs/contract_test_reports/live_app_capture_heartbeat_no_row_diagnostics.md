# Live App Capture Heartbeat No-Row Diagnostics Contract-Test Report

## Findings

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-302-001 | P1 | fixed_state_followup | fixed for the available D scope | not_blocking for narrow fixer submission | Prior E finding reported unsafe persisted timestamp-like live-capture state fields could echo through `GET /api/live/capture/status`. | `src/mythic_edge_parser/local_app/live_capture_control.py` now parses `started_at` and `updated_at` as timestamps before persisting or exposing them; `_safe_state_summary(...)` exposes only sanitized state fields. `tests/test_live_app_explicit_start_capture_control.py` covers unsafe timestamp-like state values returning `null` and not echoing. Focused backend validation passed. | F for narrow fixer patch; B/C still required for full #302 diagnostics |
| CT-302-002 | P2 | fixed_state_followup | fixed | not_blocking | Prior E finding reported unsafe `parser_status_blurb.text` could be accepted by frontend API validation. | `frontend/src/api.ts` now validates optional parser-status blurbs with safe label/text patterns and local-marker rejection. `frontend/src/api.test.ts` covers unsafe blurb rejection without echoing the unsafe text. Full frontend tests passed. | F |
| CT-302-ARTIFACT-001 | P2 | remaining_non_blocking | artifact lifecycle gap | blocking for full #302 acceptance, not for the narrow D confirmation | The prompt-named contract, comparison handoff, and prior report paths are absent locally and were not found in the current git history by exact path. GitHub issue #302 still names `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md` as the expected contract artifact. | This report was created from the issue body, D handoff, current diff, and validation evidence. The full #302 contract-comparison chain remains absent. | B/C or artifact recovery before claiming full #302 completion |
| CT-302-SCOPE-001 | P2 | deferred_followup | full heartbeat/progress diagnostics still not implemented in this patch | blocking for full #302 acceptance, not for the narrow D confirmation | Issue #302 asks for heartbeat/progress metadata, safe no-row reasons, and a parser-status blurb. | The current D patch fixes the privacy/validation findings only. Backend status still does not provide first-class heartbeat/progress diagnostics fields, and D handoff explicitly records this as remaining scope. | B/C for the full diagnostics slice |

## Role Performed

Codex E: Module Reviewer / confirmation thread.

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/302
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/294
- Branch: `codex/analytics-foundation`

## Contract And Handoff Reviewed

- Contract requested: `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`
- Prior report requested: `docs/contract_test_reports/live_app_capture_heartbeat_no_row_diagnostics.md`
- Fixer handoff reviewed: `docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_fixer.md`
- GitHub issue #302 reviewed because the requested contract artifact is absent locally.

## Files Reviewed

- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `tests/test_live_app_explicit_start_capture_control.py`
- `tests/test_live_app_parser_owned_fact_capture_sqlite.py`
- `tests/test_stream_unit.py`
- `docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_fixer.md`

## Fixed-State Verdict

CT-302-001 is fixed for the available persisted-state timestamp exposure path. Unsafe persisted `started_at` and `updated_at` values are parsed as timestamps or reduced to `null`, and unknown persisted heartbeat/progress keys are not surfaced by the current backend status payload. This confirms the narrow privacy fix but does not prove the full heartbeat/progress diagnostics feature.

CT-302-002 is fixed. The frontend live-capture API rejects unsafe `parser_status_blurb.text` before React can render it, while valid backend-led blurbs remain usable.

## Contract Matches

- Live capture start/stop behavior remains explicit and local.
- The D patch did not start, stop, restart, tail, or control a real watcher during review.
- Unsafe persisted state warnings, errors, last-result text, and timestamp-like state values are not echoed as raw/private strings through status responses.
- The frontend rejects unsafe parser-status blurbs and keeps valid backend-led blurbs available.
- `#294` analytics auto-refresh remains unimplemented.
- No parser truth, parser final reconciliation, analytics schema/migration, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer, or production behavior changed.

## Remaining Mismatches

- The requested #302 contract, comparison handoff, and prior review artifact are absent from the current branch and exact-path git history.
- Full #302 heartbeat/progress diagnostics are not present as first-class backend response fields in this patch. That is outside the narrow D fixes, but it blocks claiming issue #302 complete.

## Missing Tests Or Safeguards

- No test currently proves first-class heartbeat/progress timestamp fields are accepted only when safe because those fields are not implemented in the backend status payload.
- No test currently proves no-row reason vocabulary across tailing, parser-event routing, match-id detection, completed-row building, and SQLite-write attempts because that broader diagnostic slice remains deferred.
- No real/private MTGA smoke was run in this confirmation thread.

## Validation Run

- `git status --short --branch --untracked-files=all` -> on `codex/analytics-foundation`; #302 D files modified and fixer handoff untracked.
- `git diff --name-status` -> modified frontend API/types/tests, backend live capture control, live capture backend tests.
- `py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py` -> 38 passed, 1 existing third-party warning.
- `py -m pytest -q tests\test_live_app_parser_owned_fact_capture_sqlite.py tests\test_stream_unit.py` -> 12 passed.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> 3 files passed, 87 tests passed.
- `npm --prefix frontend run build` -> passed.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed.
- Path-scoped protected-surface scan over #302 report/fixer/code/test files -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over #302 report/fixer/code/test files -> passed, forbidden 0, warnings 0.

## Protected-Surface Status

Path-scoped protected-surface scan passed with forbidden 0 and warnings 0. Code inspection found no parser truth, analytics schema/migration, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer, or production behavior changes.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan passed with forbidden 0 and warnings 0. No raw Player.log contents, private app-data contents, generated database contents, credentials, tokens, webhook URLs, or local-only artifacts were exposed in this report.

## Generated/Private Artifact Status

`frontend/dist` was created by frontend build validation and removed. No generated database, runtime, raw log, Player.log, workbook export, failed-post, credential, or local-only artifacts were retained.

## Forbidden Scope

Forbidden scope touched: false.

## Recommendation

Route to Codex F only if the intended package is the narrow D privacy/validation fixer patch. Do not claim full issue #302 completion yet. Full #302 heartbeat/progress/no-row diagnostics still needs the missing Codex B contract/comparison chain restored or recreated, then a Codex C implementation slice.

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / confirmation thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/302"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md"
  contract_artifact_status: "missing locally and not found by exact path in git history"
  review_artifact: "docs/contract_test_reports/live_app_capture_heartbeat_no_row_diagnostics.md"
  fixer_handoff: "docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_fixer.md"
  findings_confirmed_fixed:
    - "CT-302-001 P1 fixed for persisted state timestamp exposure in the available D scope."
    - "CT-302-002 P2 fixed; unsafe parser_status_blurb.text is rejected by frontend validation."
  remaining_scope:
    - "Full #302 heartbeat/progress diagnostics and no-row reason vocabulary remain unimplemented."
    - "Contract/comparison/prior-report artifact lifecycle gap remains."
  validation:
    - "backend/live focused tests -> 38 passed, 1 existing warning"
    - "live SQLite/stream tests -> 12 passed"
    - "frontend typecheck -> passed"
    - "frontend tests -> 87 passed"
    - "frontend build -> passed; frontend/dist removed"
    - "ruff -> passed"
    - "git diff --check -> passed"
    - "agent docs -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  recommendation: "Codex F for narrow fixer patch only; Codex B/C for full #302 diagnostics completion."
```
