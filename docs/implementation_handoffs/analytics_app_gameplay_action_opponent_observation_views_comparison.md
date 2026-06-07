# Analytics App Gameplay Action And Opponent Observation Views Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/228

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md`

## Internal Project Area

Local App / UI.

## Truth Owner

Parser/state remains the truth owner for gameplay-action facts,
opponent-card-observation facts, event interpretation, match/game identity,
deduplication, and final reconciliation. SQLite analytics remains downstream
local storage. The local app backend and frontend added here are fixed
read-only review/display surfaces.

## Bridge-Code Status

`bridge_code`

Source internal project area: Analytics.

Consuming internal project area: Local App / UI.

Allowed data flow: SQLite analytics gameplay-action and
opponent-card-observation fact tables to fixed local backend responses to
frontend display.

Forbidden reverse-flow preserved: no frontend/backend write-back, parser fact
changes, analytics ingest changes, workbook/runtime updates, Line Tracer, or
coaching conclusions.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Current Behavior Compared To Contract

Before this pass, the repo already had:

- read-only local app safety patterns for match/game and early-game history
- fixed `limit`/`offset` pagination validation
- symbolic analytics database paths
- SQLite tables for `gameplay_actions`, `gameplay_action_cards`,
  `opponent_card_observations`, and `opponent_card_observation_cards`
- derived views `v_gameplay_action_review` and
  `v_opponent_card_observation_review`
- frontend response validation and read-only display patterns for prior
  analytics history sections

Remaining gap:

- no backend route exposed gameplay-action review rows
- no backend route exposed opponent-observation review rows
- no frontend types/API/display existed for these review responses
- no focused route/frontend tests covered grouped parent rows, child-card
  arrays, linked actions, degradation flags, review-required counts, or safe
  malformed-query behavior for this slice

## Implementation Option Chosen

Implemented the narrow contract option:

- use base tables directly for parent action/observation queries so pagination
  is over grouped parent rows, not child rows
- fetch child-card rows with fixed parameterized `IN` queries keyed by selected
  parent ids
- join only allowed match/game result and match context tables
- include compact linked gameplay-action context only when a stored link exists
- keep malformed `degradation_flags` safe by returning `[]` plus a stable
  warning code, without echoing raw stored text

No new helper module was needed.

## What Changed

- added fixed read-only backend builders for `GET /api/analytics/gameplay-actions`
  and `GET /api/analytics/opponent-card-observations`
- added route handlers that reuse the existing sanitized history pagination
- added grouped action/observation child-card response shaping
- added action-review response schema/object constants and typed frontend API
  validation
- added read-only frontend "Action Review" section with Gameplay Actions and
  Opponent Observations tables
- added focused backend and frontend tests
- updated route inventory

## Files Changed

- `docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md`
  - source contract from Codex B; untracked before this C pass and left
    unmodified
- `docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md`
  - this handoff
- `src/mythic_edge_parser/local_app/analytics_history.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_app_gameplay_action_opponent_observation_views.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`

## Code Changed

Runtime code changed only in the local app backend/frontend surfaces authorized
by the contract.

Backend:

- `analytics_history.py`
  - added `ACTION_REVIEW_SCHEMA_VERSION`
  - added gameplay-action and opponent-observation response object names
  - added `build_gameplay_action_review()`
  - added `build_opponent_card_observation_review()`
  - extended child-row history builder with optional row warnings and
    `review_required_row_count`
  - added fixed read-only parent SQL over allowed base tables
  - added fixed child-card SQL over allowed child tables
  - added row mappers for gameplay actions, gameplay action cards, opponent
    observations, linked action context, and observation cards
  - added safe `degradation_flags` parsing and malformed-warning behavior
- `backend.py`
  - added `GET /api/analytics/gameplay-actions`
  - added `GET /api/analytics/opponent-card-observations`

Frontend:

- `types.ts`
  - added action-review schema/object constants
  - added gameplay-action row/card/response types
  - added opponent-observation row/card/linked-action/response types
  - added `ActionReviewSummary`
- `api.ts`
  - added `fetchGameplayActionReview()`
  - added `fetchOpponentCardObservationReview()`
  - added response validation for action-review schema/object/summary/rows
  - added row/card/linked-action validation
- `App.tsx`
  - added action-review state/loading/refresh behavior
  - added `ActionReviewSection`
  - added summary panels and tables for Gameplay Actions and Opponent
    Observations
  - added safe display summaries for action rows, child cards, degradation
    flags, linked action context, and observation evidence labels

## Tests Added Or Updated

- `tests/test_analytics_app_gameplay_action_opponent_observation_views.py`
  - missing database with no artifact creation
  - empty schema-current database
  - grouped gameplay action rows with child-card arrays and zero-card groups
  - grouped opponent-observation rows with child-card arrays, linked action
    context, zero-card groups, degradation flags, and review-required counts
  - malformed `degradation_flags` redaction/warning behavior
  - unknown schema degradation
  - fixed query failure safe error behavior
  - malformed, duplicate, out-of-range, and unapproved query parameter rejection
- `tests/test_analytics_local_app_backend.py`
  - added the two new read-only analytics review routes to route inventory
- `frontend/src/api.test.ts`
  - added action-review fetch/validation tests
  - added malformed action-review response tests
- `frontend/src/App.test.tsx`
  - added Action Review render/refresh test
  - added empty/degraded action-review state test
  - added malformed action-review error display test

## Interface Changes

New backend endpoints:

- `GET /api/analytics/gameplay-actions`
- `GET /api/analytics/opponent-card-observations`

Allowed query parameters remain only:

- `limit`
- `offset`

New response schema:

- `schema_version: analytics_app_gameplay_action_opponent_observation_views.v1`

New response objects:

- `mythic_edge_local_app_gameplay_action_review`
- `mythic_edge_local_app_opponent_card_observation_review`

No workbook columns, webhook payload fields, parser event shapes, environment
variables, imports outside local app/frontend/tests, CI gates, or database
migrations changed.

## Contracted Area Status

Stayed inside the contracted Local App / UI bridge-code area.

No parser behavior, gameplay-action extraction/classification,
opponent-observation extraction/classification, analytics schema/migration,
analytics ingest, workbook/webhook/App Script/Sheets, Line Tracer, AI/coaching,
or production behavior was changed.

## Validation Run

```text
git status --short --branch -> ## codex/analytics-foundation...origin/codex/analytics-foundation plus intended #228 modified/untracked files
gh issue view 228 --json number,state,title,url -> OPEN
gh issue view 204 --json number,state,title,url -> OPEN
gh issue view 207 --json number,state,title,url -> OPEN
py -m pytest -q tests\test_analytics_app_gameplay_action_opponent_observation_views.py -> 22 passed, 1 existing FastAPI/Starlette warning
py -m pytest -q tests\test_analytics_app_gameplay_action_opponent_observation_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py -> 69 passed, 1 existing FastAPI/Starlette warning
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py -> 70 passed
py -m ruff check src tests tools -> passed
npm --prefix frontend run typecheck -> passed
npm --prefix frontend run test -- --run -> 47 passed
npm --prefix frontend run build -> passed; generated frontend/dist removed afterward
git diff --check -> passed
py tools\check_agent_docs.py -> passed
new-file whitespace/ascii/final-newline check -> passed
path-scoped protected-surface scan -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0
generated artifact status check -> frontend/dist and local SQLite database paths absent
```

## Protected-Surface Status

No forbidden parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching
or production surfaces were touched.

No arbitrary SQL input, generic database browsing, destructive database routes,
destructive job controls, destructive launcher controls, or destructive UI
controls were added.

`GET /api/analytics/opening-lines` remains deferred and unexposed.

## Generated / Private Artifact Status

No SQLite database files, WAL files, SHM files, journal files, raw logs, raw
JSONL files, failed posts, workbook exports, runtime artifacts, local-only
artifacts, secrets, credentials, raw payloads, raw hashes, full local paths,
stack traces, local usernames, Line Tracer claims, hidden-card claims,
best-line labels, archetype labels, or player mistake labels were added.

`npm --prefix frontend run build` produced `frontend/dist`, and that generated
directory was removed after the build check.

## Still Unverified

- live workbook state
- deployed Apps Script state
- production behavior
- actual local UI visual inspection in a browser against a populated database
- future first-three-turn/opening-line review behavior, which remains out of
  scope and deferred

## Reviewer Focus

Ask Codex E to pay special attention to:

- fixed endpoint/object/schema/version names
- only `limit` and `offset` query parameters accepted
- parent-row pagination, not child-card pagination
- zero-child gameplay-action and opponent-observation rows preserved
- malformed `degradation_flags` cannot echo raw stored values
- no `GET /api/analytics/opening-lines`
- no arbitrary SQL/database browser/destructive controls
- no coaching, Line Tracer, hidden-card, archetype, player-mistake, best-line,
  or strategic-advice wording
- no parser, analytics ingest, migration, workbook, webhook, Apps Script,
  Sheets, AI/OpenAI, or production behavior changes

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #228.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/228

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md

Implementation handoff:
docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md

Changed files to review:
- docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md
- docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md
- src/mythic_edge_parser/local_app/analytics_history.py
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_app_gameplay_action_opponent_observation_views.py
- tests/test_analytics_local_app_backend.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/App.tsx
- frontend/src/api.test.ts
- frontend/src/App.test.tsx

Goal:
Review the #228 implementation against the contract with fresh context. Lead with findings, ordered by severity. Confirm whether the two read-only review endpoints and frontend Action Review section satisfy the contract without expanding into arbitrary SQL, destructive controls, opening-lines, Line Tracer, coaching, hidden-card inference, archetype inference, player-mistake labels, best-line labels, parser behavior, analytics schema/migration/ingest behavior, workbook/webhook/App Script/Sheets, AI/OpenAI, or production behavior.

Validation to rerun or inspect:
py -m pytest -q tests\test_analytics_app_gameplay_action_opponent_observation_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py
py -m ruff check src tests tools
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over touched files
path-scoped secret/private-marker scan over touched files

Do not stage, commit, push, open a PR, merge, close issue #228, or mark tracker #204/umbrella #207 complete unless explicitly asked.

Final report must include:
- findings first, if any
- contract match/mismatch summary
- validation run and result
- protected-surface status
- generated/private artifact status
- whether forbidden scope was touched
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/228"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/analytics_app_gameplay_action_opponent_observation_views.md"
  target_artifact: "docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_analytics_app_gameplay_action_opponent_observation_views.py -> 22 passed"
    - "py -m pytest -q tests\\test_analytics_app_gameplay_action_opponent_observation_views.py tests\\test_analytics_app_opening_hand_mulligan_views.py tests\\test_analytics_app_match_game_history_views.py tests\\test_analytics_local_app_backend.py -> 69 passed"
    - "py -m pytest -q tests\\test_analytics_gameplay_action_ingest.py tests\\test_analytics_opponent_card_observation_ingest.py tests\\test_analytics_schema.py tests\\test_analytics_derived_views.py tests\\test_analytics_replay_view_harness.py -> 70 passed"
    - "py -m ruff check src tests tools -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> 47 passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed afterward"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "new-file whitespace/ascii/final-newline check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated artifact status check -> frontend/dist and local SQLite database paths absent"
  stop_conditions:
    - "Do not target main."
    - "Do not expose arbitrary SQL, generic database browsing, or destructive database/UI controls."
    - "Do not expose GET /api/analytics/opening-lines in this slice."
    - "Do not turn gameplay-action or opponent-observation rows into Line Tracer, coaching, hidden-card, archetype, player-mistake, best-line, or strategic-advice truth."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not change analytics schema, migrations, or ingest behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```

## Codex D Fixer Addendum

Role performed: Codex D: Module Fixer.

Review artifact used:
`docs/contract_test_reports/analytics_app_gameplay_action_opponent_observation_views.md`

Finding addressed:

- CT-228-001 P1: valid JSON-array `degradation_flags` values could expose
  path-shaped, URL-shaped, or private-marker strings in the backend response.

Fix implemented:

- Added a focused backend regression test proving valid JSON-array
  `degradation_flags` keep benign labels but do not echo unsafe path/URL-like
  values.
- Updated `src/mythic_edge_parser/local_app/analytics_history.py` so parsed
  `degradation_flags` are filtered through a safe label check before response
  serialization.
- Unsafe parsed entries collapse to the stable marker
  `opponent_observation_degradation_flag_redacted`.
- Existing malformed stored-value behavior is preserved: malformed
  `degradation_flags` still return `[]` with the stable
  `opponent_observation_degradation_flags_malformed` warning.

Files changed by this D pass:

- `src/mythic_edge_parser/local_app/analytics_history.py`
- `tests/test_analytics_app_gameplay_action_opponent_observation_views.py`
- `docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md`

Validation run:

```text
py -m pytest -q tests\test_analytics_app_gameplay_action_opponent_observation_views.py -> 23 passed, 1 existing FastAPI/Starlette warning
py -m pytest -q tests\test_analytics_app_gameplay_action_opponent_observation_views.py tests\test_analytics_app_opening_hand_mulligan_views.py tests\test_analytics_app_match_game_history_views.py tests\test_analytics_local_app_backend.py -> 70 passed, 1 existing FastAPI/Starlette warning
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_schema.py tests\test_analytics_derived_views.py tests\test_analytics_replay_view_harness.py -> 70 passed
py -m ruff check src tests tools -> passed
npm --prefix frontend run typecheck -> passed
npm --prefix frontend run test -- --run -> 47 passed
git diff --check -> passed
py tools\check_agent_docs.py -> passed
path-scoped protected-surface scan over #228 files -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan over #228 files -> passed, forbidden 0, warnings 0
generated artifact status check -> no frontend/dist or data/analytics output; ignored runtime data directories were left untouched
```

Forbidden scope status:

- No parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching or
  production behavior was touched.
- No analytics schema, migration, ingest, generated-data, raw-log, workbook
  export, runtime-status, or secret-bearing surface was intentionally changed.

Remaining risks:

- Live UI visual inspection against a populated local analytics database remains
  unverified in this D pass.
- Existing ignored runtime data directories are local generated state and were
  not modified or cleaned up.

Next recommended role: Codex E confirmation thread.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/228"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/analytics-foundation"
  source_artifact: "docs/contract_test_reports/analytics_app_gameplay_action_opponent_observation_views.md"
  target_artifact: "docs/implementation_handoffs/analytics_app_gameplay_action_opponent_observation_views_comparison.md"
  finding_fixed:
    - "CT-228-001 P1: valid JSON-array degradation_flags can expose private path/private-marker strings in the backend response."
  validation:
    - "focused #228 pytest -> 23 passed"
    - "adjacent local app history/backend pytest -> 70 passed"
    - "analytics ingest/schema/replay pytest -> 70 passed"
    - "ruff -> passed"
    - "frontend typecheck -> passed"
    - "frontend vitest -> 47 passed"
    - "git diff --check -> passed"
    - "agent docs check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  forbidden_scope_touched: false
  generated_artifacts_kept: false
```
