# Live App Capture Heartbeat No-Row Diagnostics Fixer Handoff

## Role

Codex D: Module Fixer.

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/302
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/294
- Branch used: `codex/analytics-foundation`

## Source Context

Codex E routed two findings back to D:

- CT-302-001 P1: persisted heartbeat/progress/state timestamp-like fields could echo unsafe app-data strings through `GET /api/live/capture/status`.
- CT-302-002 P2: frontend validation could accept and render arbitrary `parser_status_blurb.text` from malformed live-capture status payloads.

The handoff reported an observed branch mismatch. The worktree was clean, the expected branch existed, and the relevant code paths matched, so D switched to `codex/analytics-foundation` before editing.

The named #302 contract and review artifacts were not present in this checkout:

- `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`
- `docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md`
- `docs/contract_test_reports/live_app_capture_heartbeat_no_row_diagnostics.md`

This fixer pass stayed anchored to issue #302 and the concrete E findings.

## Fix Summary

- Backend live capture state now exposes and persists `started_at` and `updated_at` only when they parse as timestamps.
- Unsafe timestamp-like persisted state strings are converted to `null` in status payloads and do not echo through status/start/stop envelopes.
- Frontend live-capture API validation now rejects unsafe optional `parser_status_blurb` payloads before React can render them.
- Frontend live-capture state validation now treats `started_at` and `updated_at` as timestamp fields rather than arbitrary strings.
- Added the missing `LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION` export already referenced by the existing #302 frontend test.

## Files Changed

- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `tests/test_live_app_explicit_start_capture_control.py`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/types.ts`
- `docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_fixer.md`

## Tests Added

- `test_capture_status_redacts_unsafe_state_timestamp_fields`
  - proves unsafe persisted `started_at` and `updated_at` values are not echoed and are returned as `null`.
- Frontend API regression inside malformed live-status response coverage
  - proves path-shaped `parser_status_blurb.text` is rejected as `malformed_response` and not included in the thrown error text.

## Validation Run

- `py -m pytest -q tests\test_live_app_explicit_start_capture_control.py`
  - passed: 9 passed, 1 existing third-party warning.
- `npm --prefix frontend test -- --run src/api.test.ts`
  - passed: 32 passed.
- `py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py tests\test_live_app_parser_owned_fact_capture_sqlite.py`
  - passed: 49 passed, 1 existing third-party warning.
- `npm --prefix frontend run typecheck`
  - passed.
- `npm --prefix frontend test -- --run src/api.test.ts src/App.test.tsx`
  - passed: 83 passed.
- `npm --prefix frontend run build`
  - passed; generated `frontend/dist` was removed after validation.
- `py -m ruff check src tests tools`
  - passed.
- `py tools\check_agent_docs.py`
  - passed.
- `git diff --check`
  - passed after this handoff artifact was added.
- Path-scoped protected-surface scan over changed files
  - passed: forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over changed files
  - passed: forbidden 0, warnings 0.

## Forbidden Scope Status

Forbidden scope touched: false.

No parser behavior, parser final reconciliation, analytics schema/migrations, workbook/webhook/App Script/Sheets behavior, production behavior, OpenAI/AI behavior, real Player.log handling, real watcher control, generated database artifacts, raw logs, secrets, or external transport behavior were changed.

## Generated Artifact Status

`frontend/dist` was created by build validation and removed.

## Remaining Risks

- The #302 contract/comparison/report artifacts named by the handoff were absent locally, so this D pass could not verify wording against those documents.
- Full heartbeat/progress diagnostics are not implemented by this patch; this pass only fixes the two privacy/validation findings routed by Codex E.
- A real private MTGA smoke remains operator-owned and was not run.

## Next Recommended Role

Codex E confirmation thread.

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/302"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/analytics-foundation"
  source_artifact: "docs/contract_test_reports/live_app_capture_heartbeat_no_row_diagnostics.md"
  produced_artifact: "docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_fixer.md"
  findings_fixed:
    - "CT-302-001 P1: unsafe persisted timestamp-like live-capture state fields no longer echo through GET /api/live/capture/status."
    - "CT-302-002 P2: unsafe parser_status_blurb.text payloads are rejected by frontend live-capture API validation."
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex E confirmation thread"
```
