# Analytics Auto-Refresh After Match Completion Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/294

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/302

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

## Contract

`docs/contracts/analytics_auto_refresh_after_match_completion.md`

## Internal Project Area

Local app analytics backend/frontend support.

## Truth Owner

Parser/state and approved analytics ingest own match/game/result truth. The local app backend owns only a sanitized refresh-state signal derived from SQLite metadata. The frontend owns polling and display refresh orchestration only.

## Bridge-Code Status

shared_support

## Role Performed

Codex C: Module Implementer / comparison thread.

## Restoration Follow-Up

Codex E reported `CT-294-001`: the #294 package was absent from the active
checkout and existed only in a local stash. Codex C restored the package from
the locally matching stash label:

```text
codex-preserve-294-auto-refresh-before-302
```

The handoff-supplied stash index had drifted from `stash@{0}` to `stash@{3}`
after later preservation stashes. Restoration used the label match and inspected
stash contents before applying.

Unrelated active #307 ADR adoption docs were preserved first in:

```text
codex-preserve-307-adr-before-294-restore
```

The previous Codex E report artifact for #294 was restored selectively from:

```text
codex-preserve-unrelated-before-307-adr-adoption
```

Only `docs/contract_test_reports/analytics_auto_refresh_after_match_completion.md`
was restored from that stash; unrelated #304 and #302 artifacts remain
preserved.

## Package-Isolation Worktree Follow-Up

Codex C created an isolated worktree for #294 so Codex E can review the
auto-refresh package without the active primary checkout's unrelated package
state.

- Worktree: sibling checkout `MythicEdge-auto-refresh-294`
- Worktree branch: `codex/analytics-auto-refresh-isolation-294`
- Base: `origin/codex/analytics-foundation`

The #294 package was restored into that isolated worktree from:

```text
codex-preserve-294-before-302-restore
```

The primary `codex/analytics-foundation` checkout remains available for its
current local package state and was not mutated by this package-isolation
worktree restore.

## What Changed

Implemented the first read-only auto-refresh slice for issue #294:

- Added `GET /api/analytics/refresh-state`.
- Added sanitized backend refresh-state composition over safe aggregate SQLite metadata.
- Added typed frontend fetch/validation for the refresh-state endpoint.
- Added conservative visible-document polling in the React app.
- Refreshes existing analytics view fetchers after an opaque revision changes.
- Preserves manual refresh controls.
- Keeps issue #302 no-row diagnostics separate.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_auto_refresh_after_match_completion.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/analytics_dashboard.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_dynamic_decision_support_dashboard.py`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`

## Current Behavior Compared To Contract

Before this pass, the app already had read-only analytics history endpoints, dashboard modules, and manual refresh buttons. It did not have a backend-owned refresh-state endpoint, a typed frontend helper for that endpoint, or a conservative polling loop that refreshed analytics views after a safe revision change.

The implemented behavior now matches the contract's first slice:

- Backend returns `mythic_edge_local_app_analytics_refresh_state`.
- Schema version is `analytics_auto_refresh_after_match_completion.v1`.
- The revision is opaque and based only on safe aggregate counts/timestamps.
- The response does not expose raw paths, raw payloads, raw hashes, SQL, exception strings, match identity, or result text.
- Frontend polling pauses while the document is hidden.
- The initial baseline does not cause duplicate refresh storms.
- Changed revisions refresh match/game history, early-game history, gameplay/opponent review, split review, and Decision Support modules.
- Polling does not start another auto-refresh while one is already in flight.
- Changed revisions wait for a later tick if an affected analytics view group is already loading.

## Implementation Option Chosen

Used a small dedicated backend helper module, `analytics_refresh_state.py`, instead of expanding `backend.py`. This keeps the route thin and keeps refresh-state composition separate from analytics history/dashboard display payloads.

The frontend implementation uses `setInterval` with `document.visibilityState`, not WebSocket/SSE, and stores no refresh data in browser storage.

## Files Changed

- `docs/contracts/analytics_auto_refresh_after_match_completion.md`
- `docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_comparison.md`
- `src/mythic_edge_parser/local_app/analytics_refresh_state.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_auto_refresh_after_match_completion.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

## Exact Sections Changed

- Backend route inventory: added `/api/analytics/refresh-state`.
- Backend helper: added refresh-state object/schema constants, read-only SQLite metadata queries, opaque revision hashing, safe status payloads, and stable warning/error labels.
- Backend tests: added missing/current/completed/error/query-param refresh-state coverage and route inventory assertion.
- Frontend types/API: added refresh-state constants, response type, endpoint path, fetch helper, and response validation.
- Frontend app: added auto-refresh display state, visible-document polling, in-flight/loading guards, changed-revision analytics refetch orchestration, and compact status notice rendering.
- Frontend tests: added API validation tests and polling/revision-change refresh test.
- Frontend CSS: added compact auto-refresh notice styling.

## Code Changed

Yes. Backend local app code and frontend local app code changed. No parser behavior, analytics schema, ingest semantics, workbook/webhook/App Script/Sheets, AI, Line Tracer, or production behavior changed.

## Tests Added Or Updated

- Added `tests/test_analytics_auto_refresh_after_match_completion.py`.
- Updated `tests/test_analytics_local_app_backend.py`.
- Updated `frontend/src/api.test.ts`.
- Updated `frontend/src/App.test.tsx`.

## Interface Changes

Added local-only read-only endpoint:

```text
GET /api/analytics/refresh-state
```

Response object:

```text
mythic_edge_local_app_analytics_refresh_state
```

Schema:

```text
analytics_auto_refresh_after_match_completion.v1
```

No workbook, webhook, Apps Script, parser, analytics schema, environment-variable, or production interface changed.

## Contracted Area Status

Stayed inside local app analytics backend/frontend support. The change is additive and read-only on the backend. It does not write SQLite, create database files, run migrations, start capture, import logs, inspect raw Player.log, or query private/raw artifact surfaces.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_analytics_auto_refresh_after_match_completion.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_dynamic_decision_support_dashboard.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
```

Results before final hygiene scans:

- Focused backend refresh/local app/dashboard tests: passed, 42 passed, 1 pre-existing FastAPI/Starlette warning.
- Ruff: passed after one line-wrap fix.
- Frontend typecheck: passed.
- Frontend tests: passed, 90 passed.
- Frontend build: passed; generated `frontend/dist` was removed before handoff.
- `git diff --check`: passed.
- `py tools\check_agent_docs.py`: passed.
- Path-scoped protected-surface scan over touched files: passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over touched files: passed, forbidden 0, warnings 0.
- New-file trailing-whitespace and final-newline checks: passed.

Package-isolation worktree validation:

- `npm --prefix frontend ci` -> passed, 113 packages installed in the isolated worktree, 0 vulnerabilities
- `py -m pytest -q tests\test_analytics_auto_refresh_after_match_completion.py tests\test_analytics_local_app_backend.py tests\test_analytics_dynamic_decision_support_dashboard.py` -> passed, 42 tests, 1 existing FastAPI/Starlette deprecation warning
- `py -m ruff check src tests tools` -> passed
- `npm --prefix frontend run typecheck` -> passed
- `npm --prefix frontend run test -- --run` -> passed, 3 files, 90 tests
- `npm --prefix frontend run build` -> passed
- `frontend/dist` generated by build and removed before handoff
- `git diff --check` -> passed
- `py tools/check_agent_docs.py` -> passed
- path-scoped protected-surface scan over #294 files -> passed, forbidden 0, warnings 0
- path-scoped secret/private-marker scan over #294 files -> passed, forbidden 0, warnings 0
- Codex C restoration follow-up validation:
  - `py -m pytest -q tests\test_analytics_auto_refresh_after_match_completion.py tests\test_analytics_local_app_backend.py tests\test_analytics_dynamic_decision_support_dashboard.py` -> passed, 42 passed, 1 existing FastAPI/Starlette warning
  - `py -m ruff check src tests tools` -> passed
  - `npm --prefix frontend run typecheck` -> passed
  - `npm --prefix frontend run test -- --run` -> passed, 3 files / 90 tests
  - `npm --prefix frontend run build` -> passed
  - `frontend/dist` cleanup -> removed generated build output
  - `git diff --check` -> passed
  - `py tools\check_agent_docs.py` -> passed
  - path-scoped protected-surface scan over active #294 files plus the restored #294 E report -> passed, forbidden 0, warnings 0
  - path-scoped secret/private-marker scan over active #294 files plus the restored #294 E report -> passed, forbidden 0, warnings 0

## Protected-Surface Status

Path-scoped protected-surface scan over touched files passed with forbidden 0 and warnings 0. Touched surfaces do not include parser truth, parser state final reconciliation, analytics schema/migrations, workbook/webhook/App Script/Sheets, AI, Line Tracer, or production behavior.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan over touched files passed with forbidden 0 and warnings 0. The new endpoint and tests intentionally avoid raw paths, raw payloads, raw hashes, generated SQLite contents, secrets, endpoint values, spreadsheet IDs, environment values, and local-only artifacts.

## Generated Artifact Status

`npm --prefix frontend run build` generated `frontend/dist`; it was removed before handoff. No SQLite databases or local app runtime artifacts were committed.

## Unrelated Worktree State

Unrelated issue #304 frontend/doc changes were preserved before this pass in stash:

```text
stash@{0}: On codex/analytics-foundation: codex-preserve-304-dashboard-control-before-294
```

Unrelated untracked files left untouched:

- `docs/contract_test_reports/analytics_app_dashboard_live_capture_control_clarity.md`
- `docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md`

## Still Unverified

- Live browser smoke was not run in this pass.
- Real local app database changes from a live completed match were not exercised.
- The polling cadence was tested with fake timers, not an extended real-time browser session.

## Reviewer Focus

Codex E should pay special attention to:

- Whether the backend refresh-state response is sufficiently sanitized.
- Whether `analytics_revision` is opaque and changes only from safe aggregate metadata.
- Whether frontend polling properly pauses while hidden and avoids duplicate/in-flight refresh storms.
- Whether changed revisions refresh all in-scope analytics view groups.
- Whether issue #302 no-row diagnostics remained separate.
- Whether manual refresh controls remain available.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #294.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/294

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/302

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_auto_refresh_after_match_completion.md

Implementation handoff:
docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_comparison.md

Risk tier:
Medium-High

Goal:
Review the implementation against the contract. Verify the backend-owned sanitized analytics refresh-state endpoint, frontend typed response validation, conservative visible-document polling, changed-revision analytics view refresh behavior, manual refresh preservation, and separation from issue #302 no-row diagnostics.

Review focus:
- Confirm `GET /api/analytics/refresh-state` is read-only and rejects query params.
- Confirm the response object/schema match the contract exactly.
- Confirm `analytics_revision` is opaque and based only on safe aggregate metadata.
- Confirm no raw Player.log content, raw JSONL payloads, raw paths, raw hashes, SQL, stack traces, secrets, endpoint values, spreadsheet IDs, generated SQLite contents, or local-only artifacts are exposed.
- Confirm frontend polling pauses when hidden, performs one check when visible again, and does not create duplicate refresh storms.
- Confirm changed revisions refresh match/game history, opening hand/mulligan, gameplay/opponent observation, play/draw/game1-postboard split, and Decision Support dashboard modules.
- Confirm manual refresh controls remain available.
- Confirm parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior was not changed.

Validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_analytics_auto_refresh_after_match_completion.py tests\test_analytics_local_app_backend.py tests\test_analytics_dynamic_decision_support_dashboard.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed files.
If npm build creates frontend/dist, remove it before final handoff unless explicitly authorized.

Do not:
- Target main.
- Change parser behavior.
- Change analytics schema or ingest semantics.
- Change live watcher or issue #302 no-row diagnostics.
- Change workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.
- Expose raw/private/generated/local artifacts or secrets.
- Stage, commit, push, open a PR, merge, close #294, or deploy unless explicitly asked.

Final output:
- findings first, ordered by severity
- contract matches and mismatches
- validation run and result
- protected/private surface status
- whether Codex D is needed
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/302"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "GitHub issue #294 and docs/contracts/analytics_auto_refresh_after_match_completion.md"
  target_artifact: "docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_comparison.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-auto-refresh-isolation-294"
  base_branch: "origin/codex/analytics-foundation"
  package_isolation_worktree: "sibling checkout MythicEdge-auto-refresh-294"
  package_isolation_source: "stash label codex-preserve-294-before-302-restore"
  decision: "Added backend-owned sanitized analytics refresh-state endpoint plus conservative visible-document frontend polling; kept manual refresh buttons and kept #302 no-row diagnostics separate."
  validation:
    - "py -m pytest -q tests\\test_analytics_auto_refresh_after_match_completion.py tests\\test_analytics_local_app_backend.py tests\\test_analytics_dynamic_decision_support_dashboard.py -> passed, 42 passed, 1 pre-existing warning"
    - "py -m ruff check src tests tools -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> passed, 90 passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan over touched files -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over touched files -> passed, forbidden 0, warnings 0"
    - "new-file trailing-whitespace/final-newline checks -> passed"
  unrelated_worktree_preserved:
    - "stash@{0}: codex-preserve-304-dashboard-control-before-294"
    - "docs/contract_test_reports/analytics_app_dashboard_live_capture_control_clarity.md"
    - "docs/contracts/adr_0007_parser_runtime_state_decomposition_strategy.md"
  forbidden_scope_touched: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
