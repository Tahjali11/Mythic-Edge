# Analytics Auto-Refresh After Match Completion Contract

## Module Summary

- Role performed: Codex B / Module Contract Writer
- Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/294
- Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/302
- Target branch: `codex/analytics-foundation`
- Risk tier: Medium-High
- Contract artifact: `docs/contracts/analytics_auto_refresh_after_match_completion.md`
- Implementation handoff target: `docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_comparison.md`

This contract defines a read-only auto-refresh signal for the local analytics app. The goal is to let the browser refresh analytics views after parser-owned completed match result facts arrive in SQLite without making the frontend infer match completion, win/loss, or parser truth.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- GitHub issue #294
- GitHub issue #302
- `docs/contracts/live_app_parser_owned_fact_capture_sqlite.md`
- `docs/contracts/analytics_dynamic_decision_support_dashboard.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/analytics_dashboard.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`

## Observed Current Behavior

- The frontend loads analytics views on page load.
- The frontend keeps manual refresh controls for analytics history, early-game review, gameplay/opponent review, and split review.
- The Decision Support dashboard loads through `GET /api/analytics/dashboard/modules`.
- No analytics refresh-state endpoint exists.
- No frontend polling, WebSocket, or Server-Sent Events loop exists for analytics refresh.
- Current analytics endpoints are read-only curated surfaces over local SQLite.
- SQLite already contains safe metadata that can support a refresh signal: `ingest_runs`, `matches`, `games`, `match_results`, and `game_results`.
- Issue #302 is separate. It explains why live capture may produce no rows. This issue begins after rows or safe SQLite metadata exist.

## Required Guarantee

When a parser-owned completed match result is written into SQLite through an approved analytics ingest path, the local app must be able to expose a sanitized backend-owned revision signal. The frontend may poll that signal and refresh affected analytics views when the signal changes.

The frontend must not:

- infer match completion from timers, UI state, local storage, row counts alone, or browser-side heuristics;
- infer win/loss or match result truth;
- read Player.log, SQLite files, local app state files, or private artifacts directly;
- become the source of truth for parser facts.

## Truth Ownership

- Parser/state owns event interpretation, match facts, game facts, and result facts.
- Live capture and analytics ingest own approved writes of parser-normalized facts into SQLite.
- SQLite is downstream analytics storage, not parser truth.
- The backend owns the sanitized refresh-state composition derived from SQLite.
- The frontend owns polling orchestration, display refresh, and non-authoritative UI status.
- Manual refresh buttons remain user controls, not truth surfaces.

## Backend Refresh-State Endpoint Contract

Codex C should add one read-only route unless current inspection proves an equivalent safer route already exists:

```text
GET /api/analytics/refresh-state
```

The first slice should reject query parameters. It should not accept request bodies, filters, raw SQL, table names, match ids, file paths, or local artifact references.

The response must be JSON with this shape:

```json
{
  "object": "mythic_edge_local_app_analytics_refresh_state",
  "schema_version": "analytics_auto_refresh_after_match_completion.v1",
  "status": "ok",
  "analytics_revision": "opaque-backend-owned-marker",
  "latest_completed_match_result_available": true,
  "latest_completed_match_seen_at": "2026-06-08T00:00:00Z",
  "latest_completed_ingest_finished_at": "2026-06-08T00:00:00Z",
  "row_counts": {
    "ingest_runs": 1,
    "matches": 1,
    "games": 3,
    "match_results": 1,
    "game_results": 3
  },
  "warnings": [],
  "errors": []
}
```

Required fields:

- `object`: exactly `mythic_edge_local_app_analytics_refresh_state`.
- `schema_version`: exactly `analytics_auto_refresh_after_match_completion.v1`.
- `status`: one of the status labels below.
- `analytics_revision`: opaque string or `null`.
- `latest_completed_match_result_available`: boolean.
- `latest_completed_match_seen_at`: ISO-8601 timestamp string or `null`.
- `latest_completed_ingest_finished_at`: ISO-8601 timestamp string or `null`.
- `row_counts`: high-level integer counts for safe analytics tables.
- `warnings`: safe label strings only.
- `errors`: safe label strings only.

Allowed `status` labels:

- `ok`: database is readable and a refresh state was computed.
- `empty`: database is readable but no completed match-result facts are available.
- `missing`: analytics database is not present.
- `unavailable`: analytics database path or connection cannot be used safely.
- `degraded`: the backend can return a partial safe response, but one or more optional metadata queries failed.
- `error`: the backend cannot compute a safe response.

The route must be read-only. A `GET` request must not create a database, run migrations, write state files, mutate analytics rows, import artifacts, start live capture, or start any external transport.

## Revision-Marker Rules

The backend owns `analytics_revision`. The frontend may compare it for equality only. The frontend must not parse it for meaning.

The revision marker must be stable when relevant SQLite metadata is unchanged and must change after a completed parser-owned match result becomes visible through the approved analytics tables.

Allowed revision inputs are safe aggregate SQLite metadata, such as:

- maximum safe `updated_at` or `finished_at` values from `ingest_runs`;
- maximum safe `updated_at` values from completed `matches`;
- maximum safe `updated_at` values from `match_results`;
- maximum safe `updated_at` values from completed `games`;
- maximum safe `updated_at` values from `game_results`;
- row counts for `ingest_runs`, `matches`, `games`, `match_results`, and `game_results`;
- schema-readiness status already exposed safely elsewhere.

The marker must not include:

- raw Player.log content;
- raw JSONL lines;
- raw SQL;
- raw file paths;
- full private local paths;
- raw hashes of private artifacts;
- generated SQLite contents;
- match result text intended for display;
- match id, game id, parser key, deck id, card name, user name, or any other row identity;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, or environment values.

If Codex C uses a digest, it may digest only the safe aggregate metadata listed above. The digest must remain an opaque implementation detail and must not be described as evidence of private file contents.

## Frontend Polling And Refresh Contract

Codex C should add a typed frontend API helper for `GET /api/analytics/refresh-state` and validate the response shape before using it.

Recommended first-slice behavior:

- Fetch refresh state on app load after or alongside initial analytics loads.
- Store the first valid `analytics_revision` as the baseline.
- Poll every 20 to 30 seconds while the document is visible.
- Pause polling while the document is hidden.
- When the document becomes visible again, perform one refresh-state check.
- If the revision changes from a prior non-null revision, refresh all in-scope analytics views.
- Keep existing manual refresh buttons visible and working.
- Do not start a new auto-refresh cycle while a prior auto-refresh cycle is in flight.
- Do not start a new auto-refresh cycle while the same affected view group is already manually loading.
- On backend errors, show degraded status and retry only on the normal interval or after manual refresh.
- Do not use WebSocket, Server-Sent Events, desktop notifications, sound, or aggressive retry loops in the first slice.

The frontend may display a subtle status such as:

```text
Analytics updated 7:42 PM
```

The frontend must avoid copy such as:

```text
You won. Dashboard refreshed.
```

The frontend may say the analytics views were refreshed. It must not say the frontend detected a match result.

## In-Scope Analytics Views

When `analytics_revision` changes, the first slice should refresh:

- match history;
- game history;
- opening hand review;
- mulligan review;
- gameplay-action review;
- opponent-card-observation review;
- play/draw split review;
- game 1/postboard split review;
- Decision Support dashboard modules.

The Match Journal may benefit indirectly from refreshed analytics context, but this contract does not change Match Journal write controls, note ownership, or journal persistence semantics.

## UI And Status Rules

The app should present auto-refresh as a quality-of-life improvement, not as a new truth source.

Allowed UI states:

- `checking`: refresh-state request is in flight.
- `up_to_date`: most recent check did not find a changed revision.
- `updated`: changed revision was found and affected views refreshed.
- `degraded`: backend refresh-state is unavailable or partial, but manual refresh still works.
- `paused`: document is hidden or polling is intentionally paused.

UI status must be compact and non-blocking. It must not hide manual refresh controls, block normal navigation, or create an alarm-style notification.

## Relationship To Issue #302

Issue #294 handles automatic refresh after safe SQLite metadata changes. Issue #302 handles live capture heartbeat/progress diagnostics when SQLite rows do not exist.

Codex C must not implement #302 behavior in this slice unless it already exists and needs only to be read as an input. This contract must not add no-row diagnostic counters, parser heartbeat fields, capture progress counters, or parser status blurbs.

## Out Of Scope

Do not include in this issue:

- parser behavior changes;
- parser state final reconciliation changes;
- parser event class changes;
- match/game identity changes;
- deduplication changes;
- live ingest semantic changes;
- analytics schema or migration changes;
- manual JSONL import semantic changes;
- Match Journal write behavior changes;
- workbook schema changes;
- webhook payload shape changes;
- Apps Script behavior changes;
- Google Sheets behavior changes;
- output transport changes;
- production behavior changes;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer;
- hidden-card inference;
- archetype inference;
- player-mistake labels;
- gameplay advice;
- arbitrary SQL or database browsing;
- custom polling settings;
- WebSockets or Server-Sent Events;
- desktop notifications or sounds.

## Privacy And Local Artifact Rules

The endpoint, frontend state, tests, screenshots, logs, reports, and handoffs must not expose:

- raw Player.log content;
- raw JSONL payloads;
- full private paths;
- raw hashes of private artifacts;
- generated SQLite contents;
- runtime logs;
- failed posts;
- workbook exports;
- secrets;
- credentials;
- API keys;
- tokens;
- webhook URLs;
- spreadsheet IDs;
- environment values;
- local app data files;
- generated artifacts.

Local generated files created by frontend build or test commands must remain untracked and should be removed before handoff when practical.

## Implementation Expectations For Codex C

Codex C should:

1. Confirm branch and dirty worktree state before editing.
2. Preserve unrelated current worktree changes.
3. Compare the current backend/frontend behavior to this contract.
4. Add the smallest read-only backend helper/route for refresh state.
5. Add typed frontend API support and response validation.
6. Add conservative visible-document polling.
7. Refresh the in-scope view groups when the revision changes.
8. Keep manual refresh controls.
9. Add focused backend and frontend tests.
10. Produce an implementation handoff at `docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_comparison.md`.

## Validation Requirements

Backend validation should cover:

- `GET /api/analytics/refresh-state` with missing database.
- `GET /api/analytics/refresh-state` with empty database.
- `GET /api/analytics/refresh-state` with completed match/game/result rows.
- Revision marker stays stable when safe metadata is unchanged.
- Revision marker changes when completed match-result metadata changes.
- Route rejects unsupported query parameters.
- Route does not write files, create a database, run migrations, import data, or start live capture.
- Response contains no raw/private values.

Frontend validation should cover:

- API helper validates response object and schema version.
- Initial baseline does not cause duplicate refresh storms.
- Polling runs while visible.
- Polling pauses while hidden.
- Visibility return triggers one check.
- Changed revision refreshes all in-scope view groups and dashboard modules.
- Unchanged revision does not refetch all views.
- Manual refresh buttons still work.
- Backend failure produces degraded non-blocking status.
- No frontend text claims match result truth or win/loss detection.

Suggested commands for Codex C/E, adjusted as needed by the final diff:

```powershell
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_dynamic_decision_support_dashboard.py
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
@'
docs/contracts/analytics_auto_refresh_after_match_completion.md
docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/analytics_auto_refresh_after_match_completion.md
docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_comparison.md
'@ | py tools\check_secret_patterns.py --paths-from-stdin
```

If `npm --prefix frontend run build` creates `frontend/dist`, Codex C/F should remove that generated output before handoff unless the repo explicitly expects it.

## Acceptance Criteria

- Contracted backend refresh-state endpoint exists and is read-only.
- Response shape is stable, versioned, sanitized, and tested.
- Revision marker follows the backend-owned opaque-marker rules.
- Frontend polling is conservative, visible-document aware, and bounded.
- Manual refresh remains available.
- In-scope analytics views and Decision Support modules refresh on changed revision.
- No frontend code infers match completion, win/loss, or parser truth.
- No raw/private/local artifact content is exposed.
- Protected parser, analytics schema, workbook, webhook, Apps Script, Sheets, AI, and production surfaces remain untouched.

## Unknowns And Suspected Gaps

- The exact helper module for backend refresh-state composition is not yet chosen. Codex C may keep it in `backend.py` only if it remains small; otherwise a narrow local app helper module is acceptable.
- Existing SQLite indexes may be sufficient for a private-local app. Add no indexes in this slice unless a later schema contract authorizes it.
- Browser polling may interact with existing loading state in `App.tsx`; Codex C should keep the implementation simple and avoid parallel refresh storms.
- Issue #302 may later provide richer capture status, but #294 should not wait on it if SQLite revision signals are already possible.

## Next Recommended Role

Codex C: Module Implementer.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #294.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/294

Contract:
docs/contracts/analytics_auto_refresh_after_match_completion.md

Current intended branch:
codex/analytics-foundation

Goal:
Compare the current backend/frontend analytics refresh behavior to the contract, then implement the smallest safe read-only auto-refresh slice. Add `GET /api/analytics/refresh-state` or the contract-approved equivalent, typed frontend API support, conservative visible-document polling, affected analytics view refresh on changed backend revision, and focused tests. Keep manual refresh buttons.

Before editing:
- Confirm `git status --short --branch`.
- Preserve unrelated dirty files and untracked artifacts.
- Read issue #294, issue #302, the contract, backend analytics endpoints, analytics SQLite schema, frontend API/types/App/status/tests, and relevant analytics tests.

Do:
- Keep the backend refresh signal read-only and sanitized.
- Keep the frontend from inferring match completion, win/loss, or parser truth.
- Refresh match/game history, early-game review, gameplay/opponent review, split review, and Decision Support modules on changed revision.
- Keep manual refresh controls.
- Add focused backend and frontend tests.
- Produce `docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_comparison.md`.

Do not:
- Implement issue #302 no-row diagnostics in this slice.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, live ingest semantics, analytics schema/migrations, Match Journal write behavior, workbook/webhook/App Script/Sheets/output transport/production/OpenAI/AI/coaching behavior.
- Expose raw Player.log content, raw JSONL payloads, full private paths, raw hashes of private artifacts, generated SQLite contents, secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, environment values, local app data files, or generated artifacts.
- Add WebSockets/SSE, arbitrary SQL, destructive controls, or desktop notifications.
- Target main.

Validation:
- Run focused backend tests for refresh-state behavior.
- Run focused frontend tests for API validation and polling behavior.
- Run frontend typecheck/test/build as appropriate.
- Run Ruff, `git diff --check`, agent docs check, path-scoped protected-surface scan, and path-scoped secret/private-marker scan.

Final output must include:
- role performed
- issue and contract used
- branch and git status
- comparison summary
- files changed
- tests changed
- validation results
- protected-surface status
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/294"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/302"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #294"
  contract_artifact: "docs/contracts/analytics_auto_refresh_after_match_completion.md"
  target_artifact: "docs/implementation_handoffs/analytics_auto_refresh_after_match_completion_comparison.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  decision: "Use a backend-owned sanitized analytics refresh-state endpoint plus conservative visible-document frontend polling. Keep manual refresh buttons and keep #302 no-row diagnostics separate."
  stop_conditions:
    - "Do not implement issue #302 no-row diagnostics in this slice."
    - "Do not make frontend polling, browser state, local storage, or UI status into parser truth."
    - "Do not infer match completion, win/loss, or parser truth in the frontend."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not expose raw/private/local artifacts."
```
