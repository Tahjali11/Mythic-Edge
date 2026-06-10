# Live App Capture Heartbeat No-Row Diagnostics Comparison

## Role Performed

Codex C: Module Implementer / restoration-comparison thread for issue #302.

## Issue And Contract

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/302
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/294
- Prior narrow fixer PR: https://github.com/Tahjali11/Mythic-Edge/pull/306
- Contract: `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`
- Target artifact: `docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md`
- Risk tier: High

## Worktree And Branch

- Worktree: sibling checkout `MythicEdge-live-capture-diagnostics-302`
- Branch: `codex/live-capture-diagnostics-restore-302`
- Base branch: `origin/codex/analytics-foundation`
- Branch sync before restoration: `0 0`
- Primary checkout status before restoration: clean
- Generated frontend artifact before restoration: `frontend/dist` absent

## Restoration Source

Restored the clean #302 Codex C package from stash:

- `codex-preserve-302-before-304-restore`

This stash was selected because it contained only the #302 contract, #302
implementation handoff, backend/frontend live-capture diagnostics changes, and
focused tests. A separate #302 stash with a prior contract-test report was left
untouched so Codex E can perform a fresh review.

Issue #304 Dashboard live-capture control material was not restored into this
package.

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`
- `tests/test_live_app_explicit_start_capture_control.py`
- `tests/test_analytics_local_app_backend.py`
- GitHub issue #302 metadata
- GitHub PR #306 metadata

## Current Behavior Compared To Contract

The current base already includes the narrow #302 privacy/validation fixer from
PR #306. That fixer hardened unsafe timestamp and parser-status-blurb handling
but did not complete the broader #302 heartbeat/progress/no-row diagnostics
scope.

The restored package implements the broader contract additively on existing
`GET /api/live/capture/status`. The route remains read-only and keeps the
existing top-level status object and schema version:

- object: `mythic_edge_local_app_live_capture_status`
- schema version: `live_app_explicit_start_capture_control.v1`

The new nested diagnostics use:

- schema version: `live_app_capture_heartbeat_no_row_diagnostics.v1`

## Implementation Option Chosen

Restored and validated the smallest previously implemented #302 package rather
than reimplementing from scratch.

No new route was added. Issue #294 analytics auto-refresh was kept separate.
Issue #304 Dashboard live-capture control was kept separate.

## Files Changed

- `docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md`
- `docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `tests/test_live_app_explicit_start_capture_control.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`

## Exact Sections Changed

`src/mythic_edge_parser/local_app/live_capture_control.py`

- Adds the #302 nested diagnostics schema version.
- Adds heartbeat and progress vocabularies.
- Adds safe heartbeat/progress builders and sanitizers.
- Extends capture state writes with sanitized `heartbeat` and `progress`.
- Extends `GET /api/live/capture/status` payloads with top-level `heartbeat`,
  `progress`, and `parser_status_blurb`.
- Adds backend-owned parser status blurb selection from sanitized status,
  reason, and progress labels.
- Adds heartbeat updates while the supervisor is alive and waiting.
- Adds safe progress counters for parser-event routing, event-kind labels,
  match ids seen, completed game rows seen, SQLite write attempts, rows written,
  no-row reason, last event timestamp, and last SQLite write timestamp.
- Preserves GET status as read-only.

`frontend/src/types.ts`

- Adds first-class `LiveCaptureHeartbeat`, `LiveCaptureProgress`, and
  `LiveCaptureParserStatusBlurb` types.
- Requires `heartbeat`, `progress`, and `parser_status_blurb` on
  `LiveCaptureStatusResponse`.

`frontend/src/api.ts`

- Adds strict validation for heartbeat/progress nested schema versions,
  timestamps, counters, safe labels, and backend blurb text.
- Keeps unsafe blurb/path-like text rejected.

`frontend/src/App.tsx`

- Preserves direct action-result messages after start/stop clicks while still
  rendering backend-led blurb text for ordinary status fetches.

Focused tests:

- Backend tests cover read-only status defaults, healthy waiting heartbeat,
  stale heartbeat, no-row reasons, and sanitizer boundaries.
- Frontend API tests cover accepted contracted heartbeat/progress/blurb payloads
  and rejected unsafe heartbeat/progress values.
- Frontend app tests keep backend-led blurb display coverage without invented
  score/result text.

## Change Type

- Code changed: yes
- Tests changed: yes
- Frontend changed: yes
- Backend changed: yes
- Docs changed: yes
- Schema/migration changed: no
- Parser behavior changed: no
- Production behavior changed: no

## Interface Changes

Additive local-app status response fields:

- top-level `heartbeat`
- top-level `progress`
- top-level `parser_status_blurb`

No function signatures, workbook columns, environment variables, Apps Script
entrypoints, parser event classes, parser payload shapes, analytics schema, or
CI gates changed.

## Validation Run

- `git status --short --branch --untracked-files=all` -> active #302 package
  only in the isolated worktree
- `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation`
  -> `0 0`
- `py -m pytest -q tests\test_live_app_explicit_start_capture_control.py tests\test_analytics_local_app_backend.py`
  -> passed, 40 tests, 1 existing FastAPI/Starlette deprecation warning
- `git diff --check` -> passed
- `py -m ruff check src tests tools` -> passed
- `npm --prefix frontend ci` -> passed, installed local ignored dependencies
  in the isolated worktree
- `npm --prefix frontend run typecheck` -> passed
- `npm --prefix frontend run test -- --run` -> passed, 3 files, 91 tests
- `npm --prefix frontend run build` -> passed
- `frontend/dist` generated by build and removed before handoff
- `py tools\check_agent_docs.py` -> passed, checked files 47, errors 0,
  warnings 0
- path-scoped protected-surface scan over the restored #302 package -> passed,
  forbidden 0, warnings 0
- path-scoped secret/private-marker scan over the restored #302 package ->
  passed, forbidden 0, warnings 0
- direct trailing-whitespace/final-newline check for new contract and handoff
  docs -> passed

Final status remains ready for Codex E review.

## Protected-Surface Status

No parser behavior, parser state final reconciliation, parser event classes,
match identity, game identity, deduplication, analytics schema/migrations,
workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
behavior, output transport, production behavior, OpenAI/model-provider
behavior, AI/coaching behavior, Line Tracer behavior, hidden-card inference,
archetype inference, player-mistake labels, or gameplay advice was
intentionally changed.

The backend records app-owned operational metadata only. It does not change
parser truth ownership.

## Generated And Private Artifact Status

- No raw Player.log content was read, copied, printed, hashed, stored, or
  exposed.
- No raw JSONL payloads, raw hashes, private paths, SQL text, stack traces,
  secrets, endpoint values, spreadsheet IDs, environment values, generated
  SQLite contents, runtime logs, workbook exports, or local-only artifacts were
  added.
- `frontend/dist` was removed after the frontend build.
- `frontend/node_modules` was created by `npm ci` as ignored local dependency
  state in this isolated worktree and is not part of the package.

## Remaining Risks And Unverified Layers

- This implementation counts safe milestones visible to the existing live
  capture supervisor. `log_chunks_seen` remains `0` because the current stream
  boundary does not expose a separate safe chunk counter.
- Current match game-win/game-loss fields remain `null` because this slice did
  not add or reinterpret parser-owned current-match score data.
- Live browser smoke with a real Arena session was not run in this thread.
- Issue #294 analytics auto-refresh remains separate and was not implemented
  here.
- Issue #304 Dashboard live-capture control remains separate and was not
  restored here.

## Forbidden Scope

Forbidden scope was not intentionally touched.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #302.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/302

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/294

Prior narrow fixer PR:
https://github.com/Tahjali11/Mythic-Edge/pull/306

Branch:
codex/live-capture-diagnostics-restore-302

Base branch:
origin/codex/analytics-foundation

Contract:
docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md

Implementation handoff:
docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md

Risk tier:
High

Goal:
Review the restored Codex C implementation against the #302 contract. Verify that existing GET /api/live/capture/status was extended additively with app-owned heartbeat/progress diagnostics, no-row reason labels, and one backend-led parser/capture blurb, while keeping issue #294 auto-refresh and issue #304 Dashboard control separate.

Review focus:
- Confirm the top-level live capture object and schema version remain backward-compatible.
- Confirm nested heartbeat and progress use schema version live_app_capture_heartbeat_no_row_diagnostics.v1.
- Confirm GET /api/live/capture/status remains read-only and does not create app-data directories, SQLite files, migrations, diagnostics files, or live capture side effects.
- Confirm heartbeat/progress/blurb fields are sanitized and do not expose raw Player.log content, raw payloads, raw private paths, raw hashes, SQL text, stack traces, secrets, endpoint values, spreadsheet IDs, environment values, or generated SQLite contents.
- Confirm progress counters are app-owned operational metadata only, not parser truth or analytics truth.
- Confirm parser behavior, parser state final reconciliation, event classes, match/game identity, deduplication, analytics schema/migrations, workbook/webhook/App Script/Sheets/output transport/production/OpenAI/AI/coaching behavior were not changed.
- Confirm frontend validates the contracted nested response shapes and renders backend-led blurb text without inventing current match score or match-result copy.
- Confirm start/stop control visibility remains governed by backend start_allowed and stop_allowed flags.
- Confirm #304 Dashboard live-capture control files are not included in this package.

Validation:
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
git diff --check
py -m pytest -q tests/test_live_app_explicit_start_capture_control.py tests/test_analytics_local_app_backend.py
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
py tools/check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed files.

If npm build creates frontend/dist, remove generated build output before final handoff unless explicitly authorized.

Do not:
- Implement issue #294 analytics auto-refresh.
- Restore or review issue #304 Dashboard control as part of #302.
- Change parser behavior or parser truth ownership.
- Change analytics schema/migrations or ingest semantics beyond reviewing the additive app-owned metadata.
- Read, copy, hash, store, print, or expose raw Player.log content or private artifacts.
- Stage, commit, push, open a PR, merge, close issue #302, or deploy unless explicitly asked.

Final output:
- findings first, ordered by severity
- contract compliance summary
- validation run and result
- protected-surface/privacy status
- generated artifact status
- remaining risk
- whether to route to Codex D or Codex F
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/302"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  prior_narrow_fixer_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/306"
  completed_thread: "C"
  next_thread: "E"
  worktree: "MythicEdge-live-capture-diagnostics-302"
  branch: "codex/live-capture-diagnostics-restore-302"
  base_branch: "origin/codex/analytics-foundation"
  contract_artifact: "docs/contracts/live_app_capture_heartbeat_no_row_diagnostics.md"
  implementation_handoff: "docs/implementation_handoffs/live_app_capture_heartbeat_no_row_diagnostics_comparison.md"
  risk_tier: "High"
  restoration_source: "stash label codex-preserve-302-before-304-restore"
  verdict: "restored_active_ready_for_contract_review"
  issue_294_status: "separate; not implemented here"
  issue_304_status: "separate; not restored here"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
