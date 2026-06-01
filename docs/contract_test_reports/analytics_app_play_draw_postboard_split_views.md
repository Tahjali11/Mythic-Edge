# Contract Test Report: Analytics App Play/Draw And Postboard Split Views

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/229

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/analytics_app_play_draw_postboard_split_views.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Changed files reviewed:

- `frontend/src/App.test.tsx`
- `frontend/src/App.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_app_play_draw_postboard_split_views.py`
- `tests/test_analytics_local_app_backend.py`
- `docs/contracts/analytics_app_play_draw_postboard_split_views.md`
- `docs/implementation_handoffs/analytics_app_play_draw_postboard_split_views_comparison.md`
- `docs/contract_test_reports/analytics_app_play_draw_postboard_split_views.md`

Governance artifacts used:

- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The implementation must add read-only local analytics backend and frontend views
for play/draw split summaries and game 1/postboard split rows. The endpoints
must use only existing SQLite views, expose only sanitized curated payloads,
preserve existing local-app flows, and avoid parser, runtime, workbook, webhook,
Apps Script, Sheets, Line Tracer, AI, coaching, production, schema, migration,
and ingest behavior changes.

## Internal Project Area Reviewed

Analytics local app. The reviewed package stays downstream of parser-owned truth
and uses existing SQLite analytics views as read-only display inputs.

## Bridge-Code Status Reviewed

Not bridge code. The implementation adds local analytics app display/query
surfaces and does not move parser truth, workbook truth, or AI truth boundaries.

## Checks Run

```bash
git status --short --branch
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
gh issue view 229 --json number,title,state,body
rg -n "play-draw-splits|game1-postboard-splits|Line Tracer|best line|mistake|advice|causation|hidden card|archetype|coaching|coach|delete|reset|vacuum|export|arbitrary SQL|table picker|column picker|SELECT \*|raw hash|stack trace|Player\.log|webhook|OpenAI|\bAI\b" src\mythic_edge_parser\local_app frontend\src tests\test_analytics_app_play_draw_postboard_split_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_app_play_draw_postboard_split_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_app_play_draw_postboard_split_views.py tests\test_analytics_app_gameplay_action_opponent_observation_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py tests\test_analytics_schema.py
py -m ruff check src tests tools
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
```

Path-scoped protected-surface and secret/private-marker scans were also run over
the contract, handoff, report, backend files, focused tests, and frontend files.

## Results

No blocking findings.

Validation passed after stopping a repo-local Vite dev server that held a
Windows file lock in `frontend/node_modules` during the first `npm ci` attempt.
The second `npm ci` passed, and frontend typecheck, tests, and build passed.
The generated `frontend/dist` build output was removed after validation.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-229-000 | none | `not_reproduced` | no findings identified | not_blocking | Review against issue #229, contract, handoff, diff, and tests. | Focused backend tests, adjacent analytics app tests, derived/schema tests, Ruff, frontend typecheck/tests/build, diff check, agent docs check, and path-scoped protected-surface/secret scans passed. | F |

## Confirmed Contract Matches

- Backend exposes exactly the two contracted read-only split endpoints:
  `GET /api/analytics/play-draw-splits` and
  `GET /api/analytics/game1-postboard-splits`.
- Query parameters are limited to sanitized `limit` and `offset`; unexpected,
  malformed, duplicate, and out-of-bounds query values are rejected without
  echoing raw private input.
- The play/draw endpoint reads only from `v_play_draw_splits` and
  `v_sample_size_warnings`.
- The game 1/postboard endpoint reads only from `v_game1_vs_postboard`.
- Response object names and schema version match the contract.
- Play/draw rows and summary fields match the contract and keep unknown,
  unavailable, degraded, known-result, win, loss, win-rate, and small-sample
  values separate.
- Game 1/postboard rows and summary fields match the contract and preserve
  game-level context, result status, play/draw, turn count, duration, and
  provenance/status metadata without causal claims.
- Frontend API validation fails closed on malformed split-review responses.
- Frontend UI copy is descriptive and does not add coaching, Line Tracer,
  best-line, mistake, hidden-card, archetype, or causal recommendation claims.
- Existing setup, manual import, upload, match/game history, opening-hand,
  mulligan, gameplay-action, and opponent-observation flows remain covered by
  adjacent tests.
- No parser behavior, parser state final reconciliation, analytics migration,
  ingest behavior, workbook schema, webhook payload shape, Apps Script behavior,
  Google Sheets behavior, Match Journal behavior, Line Tracer behavior, AI or
  model-provider behavior, production behavior, destructive controls, raw logs,
  generated data, secrets, retry payloads, workbook exports, or generated SQLite
  artifacts were introduced in the reviewed diff.

## Contract Mismatches

- None found.

## Missing Tests

- No blocking missing tests found.
- Remaining non-blocking coverage limit: this review exercised synthetic local
  SQLite fixtures and frontend unit/render tests, not a live user database or
  production app session.

## Drift Notes

- Branch drift: `HEAD...origin/codex/analytics-foundation` was `0 0` during
  review.
- Local generated artifact drift: `frontend/dist` was created by build
  validation and removed afterward.
- Issue lifecycle drift: tracker #204, umbrella #207, and issue #229 remain
  open; this report does not authorize issue or tracker closure.
- No repo, workbook, deployment, local-data, schema, or production drift was
  identified from the reviewed diff.

## Recommendation

approve

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #229.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/229

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Review artifact:
docs/contract_test_reports/analytics_app_play_draw_postboard_split_views.md

Contract:
docs/contracts/analytics_app_play_draw_postboard_split_views.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_play_draw_postboard_split_views_comparison.md

Task:
Submit the reviewed #229 package. Inspect git status, confirm branch sync, stage only the intended #229 files, commit with a concise message, push codex/analytics-foundation, and open or update the draft PR toward the correct non-production integration target. Do not target main, merge, close issue #229, mark tracker #204 complete, or change production behavior unless explicitly approved.

Reviewed files expected:
- frontend/src/App.test.tsx
- frontend/src/App.tsx
- frontend/src/api.test.ts
- frontend/src/api.ts
- frontend/src/types.ts
- src/mythic_edge_parser/local_app/analytics_history.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_app_play_draw_postboard_split_views.py
- tests/test_analytics_local_app_backend.py
- docs/contracts/analytics_app_play_draw_postboard_split_views.md
- docs/implementation_handoffs/analytics_app_play_draw_postboard_split_views_comparison.md
- docs/contract_test_reports/analytics_app_play_draw_postboard_split_views.md

Validation already confirmed by Codex E:
- focused #229 backend tests passed
- adjacent analytics app tests passed
- derived/replay/schema tests passed
- Ruff passed
- npm ci/typecheck/test/build passed after stopping a stale repo-local Vite dev-server lock
- git diff --check passed
- agent docs check passed
- path-scoped protected-surface and secret/private-marker scans passed
- generated frontend dist output was removed

Stop conditions:
- Do not stage unrelated files.
- Do not target main.
- Do not add destructive import/database/job/launcher/UI controls.
- Do not expose raw payloads, raw paths, raw hashes, internal digests, temp paths, stack traces, secrets, or private artifacts.
- Do not change parser behavior, saved-event replay semantics, parser state final reconciliation, analytics schema/migrations, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, Match Journal, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, production behavior, or issue/tracker closure state.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/229"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/analytics_app_play_draw_postboard_split_views.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_app_play_draw_postboard_split_views_comparison.md"
  target_artifact: "docs/contract_test_reports/analytics_app_play_draw_postboard_split_views.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_analytics_app_play_draw_postboard_split_views.py tests\\test_analytics_local_app_backend.py -> 33 passed, 1 third-party warning"
    - "py -m pytest -q tests\\test_analytics_app_play_draw_postboard_split_views.py tests\\test_analytics_app_gameplay_action_opponent_observation_views.py tests\\test_analytics_app_opening_hand_mulligan_views.py tests\\test_analytics_app_match_game_history_views.py tests\\test_analytics_local_app_backend.py -> 92 passed, 1 third-party warning"
    - "py -m pytest -q tests\\test_analytics_derived_views.py tests\\test_analytics_replay_view_harness.py tests\\test_analytics_schema.py -> 22 passed"
    - "py -m ruff check src tests tools -> passed"
    - "npm --prefix frontend ci -> passed after stopping stale repo-local Vite dev-server lock"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> 3 files passed, 52 tests passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed afterward"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed"
    - "path-scoped secret/private-marker scan -> passed"
  findings: "No blocking or non-blocking implementation findings."
  forbidden_scope_touched: false
  generated_artifacts_kept: false
  next_recommended_role: "Codex F: Module Submitter"
  stop_conditions:
    - "Do not target main."
    - "Do not stage unrelated files."
    - "Do not add destructive controls or expose private/raw/local artifacts."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/Line Tracer/OpenAI/AI/coaching/production behavior."
    - "Do not close issue #229, tracker #204, or umbrella #207 unless explicitly approved."
```
