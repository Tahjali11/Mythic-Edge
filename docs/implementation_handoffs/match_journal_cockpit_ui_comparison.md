# Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/232

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/202

## Contract

`docs/contracts/match_journal_cockpit_ui.md`

## Internal Project Area

Local App / UI.

## Truth Owner

Parser/state layers remain truth owner for parser-managed match/game fields.
Match Journal service/repository own local journal annotations. The local app
backend and frontend are access/display/control surfaces only.

## Bridge-Code Status

`stable_bridge`: browser UI -> FastAPI local app facade -> Match Journal service.

## Role Performed

Codex C: Module Implementer / comparison thread.

## What Changed

Implemented the first browser-facing Match Journal cockpit slice through a
local app FastAPI facade under `/api/journal/...`. The browser never calls the
legacy status API routes directly, and the first cockpit slice does not expose
pilot-error controls, destructive controls, raw SQL, parser runners, live
watchers, Sheets, Apps Script, OpenAI, coaching, hidden-card, best-line, or
player-mistake controls.

The backend facade requires explicit Match Journal service wiring and fails
closed with a safe `service_unavailable` envelope when the service is absent.
The frontend renders read-only parser/analytics context, displays journal bundle
counts, handles unavailable/degraded states, and exposes only match/game/
sideboarding notes, manual opponent labels, review flags, experiment label, and
journal-display-only correction proposal controls.

## Files Changed

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/match_journal_cockpit.py`
- `tests/test_match_journal_cockpit_ui_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md`

Untracked source contract preserved:

- `docs/contracts/match_journal_cockpit_ui.md`

## Code Changed

Runtime code changed in the Local App / UI area only:

- `backend.py`: added optional keyword-only `match_journal_service_factory`
  injection and registered `/api/journal`, `/api/journal/notes`,
  `/api/journal/opponent-labels`, `/api/journal/review-flags`,
  `/api/journal/experiment-label`, and `/api/journal/display-corrections`.
- `match_journal_cockpit.py`: added local app facade validation, safe response
  envelopes, service dispatch, safe error mapping, and JSON-safe service result
  conversion.
- `types.ts` / `api.ts`: added Match Journal cockpit schema constants, request
  and response types, API helpers, and response validation for `/api/journal/...`.
- `App.tsx` / `App.css`: added Match Journal cockpit UI, read-only context
  summary, bundle summary, unavailable-state handling, allowed first-slice
  forms, and responsive form styling.

No parser, parser state reconciliation, analytics schema/migration, workbook,
webhook, Apps Script, Sheets, OpenAI, AI/coaching, or production behavior was
changed.

## Tests Added Or Updated

- `tests/test_match_journal_cockpit_ui_backend.py`: added route inventory,
  CORS/no-wildcard, missing-service fail-closed, validation/no-service-call,
  bundle read/no artifact creation, service dispatch, display-only correction,
  and safe-envelope tests.
- `frontend/src/api.test.ts`: added Match Journal API helper tests proving
  helpers use `/api/journal/...` routes, parse safe unavailable envelopes, and
  reject incompatible response schemas.
- `frontend/src/App.test.tsx`: added cockpit rendering, unavailable disabled
  forms, allowed mutation context, and safe error tests; adjusted one existing
  history text assertion to allow the same read-only match id in the cockpit.

## Interface Changes

- New FastAPI local app routes:
  - `GET /api/journal`
  - `POST /api/journal/notes`
  - `POST /api/journal/opponent-labels`
  - `POST /api/journal/review-flags`
  - `POST /api/journal/experiment-label`
  - `POST /api/journal/display-corrections`
- Explicitly not added: `POST /api/journal/pilot-error`.
- New local app Match Journal response envelope:
  - `object: mythic_edge_local_app_match_journal`
  - `schema_version: match_journal_cockpit_ui.v1`
  - `status`
  - `result`
  - `warnings`
  - `errors`
- `create_app(...)` gained optional keyword-only
  `match_journal_service_factory` for explicit test/local wiring.

No environment variables, workbook columns, webhook payload fields, Apps Script
entrypoints, CI gates, or parser payload shapes changed.

## Contracted Area Status

Implementation stayed inside Local App / UI plus focused tests and handoff
documentation. The Match Journal service is used as the write boundary; the
frontend does not call status API `/journal/...` routes directly and does not
gain browser access to raw SQL or destructive operations.

## Validation Run

```bash
git status --short --branch --untracked-files=all
# ## codex/analytics-foundation...origin/codex/analytics-foundation
# modified frontend/local-app files plus untracked contract/facade/test/handoff

py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
# 8 passed, 1 StarletteDeprecationWarning

py -m ruff check src\mythic_edge_parser\local_app\match_journal_cockpit.py src\mythic_edge_parser\local_app\backend.py tests\test_match_journal_cockpit_ui_backend.py
# passed

npm --prefix frontend run typecheck
# passed

npm --prefix frontend run test -- --run src/api.test.ts src/App.test.tsx
# 56 passed

py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py tests\test_match_journal_status_api.py tests\test_analytics_local_app_backend.py tests\test_status_api.py
# 43 passed, 1 StarletteDeprecationWarning

py -m pytest -q tests\test_match_journal_service.py tests\test_match_journal_repository.py tests\test_match_journal_schema.py
# 63 passed

npm --prefix frontend run build
# passed; generated frontend/dist is gitignored

git diff --check
# passed

py -m ruff check src tests
# passed

npm --prefix frontend run test -- --run
# 59 passed

py tools\check_agent_docs.py
# passed

py tools\check_secret_patterns.py --all
# failed on pre-existing all-repo forbidden/warning findings outside this slice

@'
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/App.tsx
frontend/src/api.test.ts
frontend/src/api.ts
frontend/src/types.ts
src/mythic_edge_parser/local_app/backend.py
docs/contracts/match_journal_cockpit_ui.md
src/mythic_edge_parser/local_app/match_journal_cockpit.py
tests/test_match_journal_cockpit_ui_backend.py
docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed before handoff was added; rerun recommended after this handoff

@'
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/App.tsx
frontend/src/api.test.ts
frontend/src/api.ts
frontend/src/types.ts
src/mythic_edge_parser/local_app/backend.py
docs/contracts/match_journal_cockpit_ui.md
src/mythic_edge_parser/local_app/match_journal_cockpit.py
tests/test_match_journal_cockpit_ui_backend.py
docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed before handoff was added; rerun recommended after this handoff
```

## Still Unverified

- Live local app backend + frontend manual browser flow.
- Real Match Journal service wiring against an on-disk local app database.
- Production behavior, which is out of scope.
- GitHub Actions / PR checks.
- Whether Codex E wants a follow-up for the pre-existing all-repo
  `check_secret_patterns.py --all` findings.

## Reviewer Focus

Ask Codex E to pay special attention to:

- Browser API helpers and UI controls use only `/api/journal/...`, never direct
  status API `/journal/...`.
- Missing service wiring fails closed and does not create local app artifacts
  on read-only bundle lookup.
- Pilot-error cockpit controls remain absent in this first slice.
- Display correction controls are clearly journal-display-only and do not imply
  parser, analytics, workbook, or AI truth.
- Existing local CORS policy remains loopback-only and no wildcard origin is
  introduced.
- Safe envelopes do not leak exception detail, raw note text, stack traces, SQL,
  private paths, secrets, or raw payloads.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #232.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/232

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Contract:
docs/contracts/match_journal_cockpit_ui.md

Implementation handoff:
docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md

Goal:
Review the Codex C implementation against the contract. Focus on the browser API safety boundary, the FastAPI `/api/journal/...` facade, Match Journal service dispatch, unavailable/degraded behavior, frontend cockpit controls, and tests.

Review expectations:
- Lead with findings ordered by severity.
- Confirm whether the browser ever calls direct status API `/journal/...` routes.
- Confirm `/api/journal/pilot-error` and pilot-error browser controls remain absent.
- Confirm existing CORS remains loopback-only and no wildcard CORS was introduced.
- Confirm missing Match Journal service wiring fails closed with safe envelopes.
- Confirm invalid bodies do not call the service.
- Confirm attached note context and unattached note semantics remain separate.
- Confirm display corrections remain journal-display-only.
- Confirm no destructive controls, raw SQL, raw paths, raw payloads, stack traces, secrets, Sheets/App Script/OpenAI/AI/coaching/Line Tracer/best-line/hidden-card/player-mistake truth controls were added.
- Confirm no parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed.

Recommended validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py tests\test_match_journal_status_api.py tests\test_analytics_local_app_backend.py tests\test_status_api.py
py -m pytest -q tests\test_match_journal_service.py tests\test_match_journal_repository.py tests\test_match_journal_schema.py
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests
git diff --check
@'
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/App.tsx
frontend/src/api.test.ts
frontend/src/api.ts
frontend/src/types.ts
src/mythic_edge_parser/local_app/backend.py
docs/contracts/match_journal_cockpit_ui.md
src/mythic_edge_parser/local_app/match_journal_cockpit.py
tests/test_match_journal_cockpit_ui_backend.py
docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/App.tsx
frontend/src/api.test.ts
frontend/src/api.ts
frontend/src/types.ts
src/mythic_edge_parser/local_app/backend.py
docs/contracts/match_journal_cockpit_ui.md
src/mythic_edge_parser/local_app/match_journal_cockpit.py
tests/test_match_journal_cockpit_ui_backend.py
docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

Note:
`py tools\check_secret_patterns.py --all` was run by Codex C and failed on pre-existing all-repo findings outside this slice; the touched-path secret scan passed before the handoff was added. Re-run path-scoped scans including the handoff.

Do not stage, commit, push, open a PR, merge, close issue #232, or mark tracker #202 complete unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/232"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/match_journal_cockpit_ui.md"
  target_artifact: "docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "focused backend cockpit tests -> passed"
    - "status API/local app/status API adjacency tests -> passed"
    - "Match Journal service/repository/schema tests -> passed"
    - "frontend typecheck -> passed"
    - "frontend focused App/API tests -> passed"
    - "frontend full test run -> passed"
    - "frontend build -> passed; frontend/dist ignored"
    - "ruff src tests -> passed"
    - "git diff --check -> passed"
    - "agent docs check -> passed"
    - "protected-surface path scan -> passed before handoff add; rerun recommended"
    - "secret/private path scan -> passed before handoff add; rerun recommended"
    - "all-repo secret scan -> failed on pre-existing findings outside this slice"
  stop_conditions:
    - "Do not call the status API directly from the browser."
    - "Do not change status API CORS without a separate contract."
    - "Do not add pilot-error browser controls in the first cockpit slice."
    - "Do not change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```
