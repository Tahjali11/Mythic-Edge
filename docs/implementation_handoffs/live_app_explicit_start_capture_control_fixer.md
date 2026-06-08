# Live App Explicit Start Capture Control Fixer Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/297

## Branch

`codex/analytics-foundation`

## Source Artifacts

- `docs/contracts/live_app_explicit_start_capture_control.md`
- `docs/implementation_handoffs/live_app_explicit_start_capture_control_comparison.md`
- `docs/contract_test_reports/live_app_explicit_start_capture_control.md`

## Role Performed

Codex D: Module Fixer.

## Findings Fixed

- CT-297-001 P1: live capture responses could echo unsafe warning/error strings read from app-data capture state.
- CT-297-002 P2: Start capture could proceed from an auto-detected default Player.log without an explicit configured `player_log_path`.

## Files Changed

- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `tests/test_live_app_explicit_start_capture_control.py`
- `docs/implementation_handoffs/live_app_explicit_start_capture_control_fixer.md`

Pre-existing #297 implementation files and unrelated dirty files were preserved and not reverted.

## Fix Summary

State-derived warning and error lists are now treated as untrusted API input. Safe snake-case operational labels remain visible, unsafe strings are replaced with deterministic redaction labels, and state-derived `last_result` is narrowed to safe status, count maps, skipped maps, and safe warnings only.

Capture start readiness now requires the Player.log path to be explicitly configured and present. The read-only Player.log monitor may still report a detected default Player.log, but that detected default no longer satisfies the Start capture precondition.

## Tests Added

- `test_capture_status_redacts_unsafe_state_warning_error_and_result_text`
- `test_start_capture_requires_configured_player_log_not_detected_default`

## Validation

- `py -m pytest -q tests\test_live_app_explicit_start_capture_control.py` -> 8 passed, 1 existing Starlette/httpx warning.
- `py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py tests\test_live_app_parser_owned_fact_capture_sqlite.py` -> 44 passed, 1 existing Starlette/httpx warning.
- `py -m pytest -q tests\test_runner.py tests\test_tailer.py` -> 26 passed.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend test -- --run src/App.test.tsx src/status.test.ts` -> 54 passed.
- `npm --prefix frontend run build` -> passed; generated `frontend/dist` removed.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- Supplemental `git diff --check --no-index` over untracked #297 files -> no whitespace diagnostics.
- `py tools\check_agent_docs.py` -> passed.

Path-scoped protected-surface and secret/private-marker scans were run over the #297 package after this handoff was added.

## Forbidden Scope Status

Forbidden scope touched: false.

No parser interpretation, parser final reconciliation, parser event classes, analytics schema/migrations, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, OpenAI/model-provider behavior, AI/coaching behavior, or production deployment behavior was changed.

## Generated Artifact Status

No generated frontend build artifact was kept. No SQLite database, WAL/SHM/journal, raw log, runtime status, failed post, workbook export, secret, credential, or local-only runtime artifact was intentionally created or kept.

## Remaining Risks

- Full manual/browser smoke of the local app live capture panel was not performed in this fixer pass.
- Full repository pytest was not run; validation stayed scoped to the reviewed backend/live, parser-adjacent, frontend, lint, docs, and path-safety checks.

## Next Recommended Role

Codex E confirmation thread for issue #297.

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/297"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/analytics-foundation"
  source_artifact: "docs/contract_test_reports/live_app_explicit_start_capture_control.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_explicit_start_capture_control_fixer.md"
  findings_fixed:
    - "CT-297-001 P1: live capture responses no longer echo unsafe warning/error/last_result strings read from app-data capture state."
    - "CT-297-002 P2: Start capture now requires explicit configured player_log_path; detected default Player.log remains read-only monitor evidence only."
  validation:
    - "focused backend/live pytest -> passed"
    - "parser runner/tailer pytest -> passed"
    - "frontend typecheck/tests/build -> passed; frontend/dist removed"
    - "ruff, git diff --check, agent docs -> passed"
    - "path-scoped protected-surface and secret/private-marker scans -> passed"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
```
