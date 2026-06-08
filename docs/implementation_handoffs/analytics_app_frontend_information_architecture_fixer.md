# Analytics App Frontend Information Architecture Fixer Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/299

## Branch

`codex/analytics-foundation`

## Source Artifacts

- `docs/contracts/analytics_app_frontend_information_architecture.md`
- `docs/implementation_handoffs/analytics_app_frontend_information_architecture_comparison.md`
- `docs/contract_test_reports/analytics_app_frontend_information_architecture.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/module_fixer.md`

## Role Performed

Codex D: Module Fixer / dependency-isolation thread.

## Source Finding

CT-299-001 P1: the route-gated cockpit behavior passed focused review, but the dirty worktree was not submitter-ready because full frontend validation failed in `frontend/src/api.test.ts`.

CT-299-002 P3: browser/mobile visual smoke was not run. This remains unverified.

## Fault Category

Frontend API-boundary validation drift.

The read-only live watcher status contract says `/api/live/watcher/status` is readiness-only and must not report a running watcher. The frontend validator accepted `watcher.running: true`, which made `frontend/src/api.test.ts` fail its malformed-response regression.

## Fix Produced

- Tightened the `fetchLiveWatcherStatus` response validator so readiness-only watcher payloads require:
  - `running: false`
  - `parser_runner_started: false`
  - `tailing_started: false`
  - `sqlite_live_writes_enabled: false`
- Narrowed the `LiveWatcherSummary` TypeScript type to match that readiness-only contract.
- Updated the active live-capture test fixture so active evidence comes from process/capture surfaces, not from `/api/live/watcher/status`.

The approved #299 route-gated information architecture behavior was preserved.

## Files Changed

- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_app_frontend_information_architecture_fixer.md`

## Package Boundary Status

The current checkout still contains adjacent #297 live-capture frontend/backend work and #299 route-shell work together. This fixer made the combined dirty frontend package validation-clean. It does not prove that #299 is standalone-submit-ready without #297 dependencies.

Recommended submitter posture: route back to Codex E to confirm whether the intended package should be submitted as a deliberate combined #297/#299 package or whether #297 should be submitted first and #299 rebased/isolated afterward.

## Validation

- `npm --prefix frontend test -- --run src/api.test.ts` -> 30 passed.
- `npm --prefix frontend test -- --run` -> 86 passed.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run build` -> passed; generated `frontend/dist` removed.
- `py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py` -> 33 passed, 1 existing Starlette/httpx warning.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed.

Path-scoped protected-surface and secret/private-marker scans were run over the final intended frontend package after this handoff was added.

## Forbidden Scope Status

Forbidden scope touched: false.

No parser behavior, parser final reconciliation, analytics schema/migrations, manual import semantics, replay ingest semantics, Match Journal truth ownership, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, secrets, raw logs, raw JSONL payloads, generated runtime artifacts, workbook exports, or local-only runtime artifacts were changed.

## Generated Artifact Status

`frontend/dist` was created by build validation and removed. No generated artifact was intentionally kept.

## Remaining Risks

- Browser/mobile visual smoke remains unverified.
- The dirty worktree is still mixed with #297 and other adjacent local-app work; Codex E should confirm package ordering before Codex F.
- Full repository pytest was not run because the finding was frontend API/package validation scoped.

## Next Recommended Role

Codex E confirmation thread for issue #299.

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/299"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/analytics-foundation"
  source_artifact: "docs/contract_test_reports/analytics_app_frontend_information_architecture.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_app_frontend_information_architecture_fixer.md"
  findings_fixed:
    - "CT-299-001 P1: full frontend suite now passes; fetchLiveWatcherStatus rejects readiness-only watcher payloads that claim running/parser/tailing/SQLite-write activity."
  remaining_findings:
    - "CT-299-002 P3: browser/mobile visual smoke still not run."
  validation:
    - "npm --prefix frontend test -- --run src/api.test.ts -> 30 passed"
    - "npm --prefix frontend test -- --run -> 86 passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "adjacent backend/live pytest -> 33 passed, 1 existing warning"
    - "ruff, git diff --check, agent docs -> passed"
    - "path-scoped protected-surface and secret/private-marker scans -> passed"
  intended_package_status: "combined #297/#299 frontend package is validation-clean; standalone #299 isolation still needs E/F ordering decision"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
```
