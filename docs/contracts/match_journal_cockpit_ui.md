# Match Journal Cockpit UI Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/232
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/202
- source artifact: GitHub issue #232
- target artifact: docs/contracts/match_journal_cockpit_ui.md
- intended branch: codex/analytics-foundation
- risk tier: High
- status: draft contract for Codex C implementation/comparison

## Purpose

Define the first browser-facing Match Journal cockpit UI and API safety
boundary. The cockpit should let the local React app display parser-owned
match/game context and collect human-owned Match Journal notes, labels, review
flags, and display-only correction proposals without turning the browser,
analytics database, status API, or Match Journal into parser truth.

This contract is intentionally narrow. It authorizes a local developer cockpit
surface and a browser-safe API facade only. It does not authorize production
deployment, external access, parser behavior changes, analytics truth changes,
workbook changes, Apps Script changes, or AI/coaching behavior.

## Source Artifacts Inspected

- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md
- docs/project_roadmap.md
- issue #202
- issue #203
- issue #204
- issue #207
- issue #232
- docs/contracts/match_journal_service.md
- docs/contracts/match_journal_status_api.md
- docs/implementation_handoffs/match_journal_status_api_comparison.md
- docs/contract_test_reports/match_journal_status_api.md
- src/mythic_edge_parser/app/status_api.py
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/analytics_history.py
- frontend/src/api.ts
- frontend/src/types.ts
- frontend/src/App.tsx
- frontend/src/App.test.tsx
- frontend/package.json
- tests/test_analytics_local_app_backend.py
- tests/test_match_journal_status_api.py
- tests/test_status_api.py

## Observed Current Behavior

### Match Journal Service

- `MatchJournalService` owns human journal records and exposes service methods
  for notes, opponent labels, review flags, pilot-error review, display-only
  correction proposals, experiment labels, and journal bundle lookup.
- The service contract says Match Journal records are human-owned annotations
  and review metadata. They are not parser truth, workbook truth, analytics
  truth, AI truth, or gameplay advice.
- Service methods require explicit context for attached match/game records.
  Unattached notes are supported separately and must not be silently created
  when an attached note request is malformed.

### Status API Journal Routes

- #203 added local status API journal routes:
  - `GET /journal`
  - `POST /journal/notes`
  - `POST /journal/pilot-error`
  - `POST /journal/opponent-labels`
  - `POST /journal/review-flags`
  - `POST /journal/display-corrections`
- The status API routes dispatch through `MatchJournalService`, not direct SQL.
- The status API routes fail closed when the service factory is missing or the
  status API host is not loopback.
- The status API route response object is `match_journal_api_response`.
- The status API maps malformed JSON, validation errors, not-found cases,
  conflicts, and internal service failures to safe envelopes.
- The status API currently inherits broad response CORS behavior with
  `Access-Control-Allow-Origin: *`. The #203 review explicitly carried this as
  a future hardening consideration before browser-facing use expands.

### FastAPI Local App Backend

- The local app backend already exists under
  `src/mythic_edge_parser/local_app/backend.py`.
- It exposes loopback-focused app, runtime, import, and analytics routes under
  `/api/...`.
- It uses a narrowed frontend-origin CORS policy. The default allowed frontend
  origins are loopback Vite origins, and the optional launcher environment
  override accepts only loopback HTTP origins with valid ports.
- Current local app backend tests assert no wildcard CORS, no DELETE routes,
  no generated app-data creation from read-only setup routes, and safe redaction
  of paths and secret-like configuration values.

### React/Vite Frontend

- The frontend already uses a constrained loopback API base URL through
  `getApiBaseUrl()`.
- Existing app sections display setup status, manual import status, match/game
  history, early-game review, gameplay-action review, opponent-observation
  review, and split review.
- Existing frontend tests assert read-only analytics display, safe degraded
  states, no raw backend details, no unsafe local path echo, and absence of
  destructive controls such as reset/delete/wipe/start/stop/git/sheets/ai.

### Tracker Routing

- Issue #232 remains under Match Journal tracker #202.
- Analytics tracker #204 and app-shell issue #207 are adjacent because the
  browser shell and FastAPI backend live on the analytics-foundation branch.
- #232 must not be treated as a general analytics app feature or a continuation
  of analytics tracker #204. It owns only the Match Journal cockpit UI and the
  browser API safety boundary needed by that UI.

## Contract Decision

The first cockpit implementation must route browser traffic through the
FastAPI local app backend, not directly to the standard-library status API.

The FastAPI backend should expose a narrow Match Journal facade under
`/api/journal/...` and should call Match Journal service/repository wiring or
shared journal payload helpers from inside Python. The browser must not call
the status API journal routes directly in this first cockpit slice.

Reasons:

- The FastAPI local app already has a narrower loopback frontend-origin CORS
  policy.
- The status API currently emits wildcard CORS headers and was reviewed as a
  local status/control surface, not a browser-facing write surface.
- The cockpit is a local developer app UI. It should inherit the local app
  frontend API boundary, error handling, and safe display patterns already used
  by analytics and import views.
- Direct browser-to-status-API writes require a separate CORS/local-origin
  hardening contract if they are ever needed.

## Public Interface Contract

### Frontend Surface

The first cockpit UI should add a Match Journal cockpit section to the existing
React local app. It may be a new top-level section in `SetupStatusApp` or a
coherent component imported by that app.

Required UI capabilities:

- Select or receive a match/game context from existing read-only match/game
  rows.
- Display parser-owned context as read-only:
  - `match_id`
  - `game_id` when selected
  - `game_number` when selected
  - result fields when available
  - play/draw when available
  - queue, format, and event fields when available
  - provenance/status labels when already present in analytics view data
- Display a Match Journal bundle when available.
- Display unavailable/degraded service states safely when Match Journal service
  wiring is missing or returns a safe error.
- Provide first-slice human-owned edit controls for:
  - match notes
  - game notes
  - sideboarding notes
  - manual opponent archetype label
  - manual opponent tier label
  - review flags
  - experiment label
  - journal-display-only correction proposals
- Clearly label display correction proposals as proposals that affect journal
  display/review only. They must not be represented as parser corrections,
  workbook corrections, or source-of-truth changes.

Forbidden UI capabilities in this slice:

- direct status API URL entry
- arbitrary SQL
- raw JSON payload editor
- parser runner start/stop controls
- live watcher controls
- destructive reset/delete/wipe actions
- git operations
- Google Sheets or Apps Script actions
- OpenAI/model-provider actions
- AI coaching, Line Tracer, best-line, hidden-card, matchup advice, or
  player-mistake truth
- browser controls that write parser facts, analytics facts, workbook facts, or
  evidence-ledger facts

Pilot-error controls are deferred from the first cockpit UI despite existing
status API route support. Pilot-error labels have higher player-mistake-truth
risk and should return through a focused follow-up contract before becoming a
browser-facing control.

### FastAPI Backend Facade

Codex C may add backend routes under `src/mythic_edge_parser/local_app/` using
the existing FastAPI app. The route inventory should be narrow:

| Method | Route | Required purpose |
| --- | --- | --- |
| GET | `/api/journal` | Return a journal bundle for an explicit match/game context. |
| POST | `/api/journal/notes` | Record match, game, sideboarding, or unattached note through the journal service. |
| POST | `/api/journal/opponent-labels` | Set manual opponent archetype/tier labels through the journal service. |
| POST | `/api/journal/review-flags` | Add review flags through the journal service. |
| POST | `/api/journal/experiment-label` | Set a human-owned experiment label through the journal service. |
| POST | `/api/journal/display-corrections` | Record journal-display-only correction proposals through the journal service. |

`POST /api/journal/pilot-error` is not required and should remain deferred for
the first cockpit UI unless a later contract explicitly authorizes it.

The backend facade must:

- require explicit local app service wiring and fail closed when it is absent;
- call `MatchJournalService` behavior, not direct ad hoc SQL;
- preserve attached versus unattached note semantics;
- validate request bodies before calling the service;
- return safe error envelopes without raw exception details, note text echo in
  error paths, raw SQL, private local paths, secrets, or stack traces;
- preserve existing local app CORS behavior and never add wildcard CORS for
  journal routes;
- use temporary or in-memory services in tests when persistence is needed;
- avoid creating generated app-data files from read-only `GET /api/journal`
  requests.

The facade may share names and payload semantics with
`docs/contracts/match_journal_status_api.md`, but it should not require the
browser to call or know about the status API port.

### Response Shape

The browser-facing facade should use a stable object name and schema version:

- object: `mythic_edge_local_app_match_journal`
- schema_version: `match_journal_cockpit_ui.v1`

Successful responses should include:

- `object`
- `schema_version`
- `status`: `ok`, `degraded`, `empty`, `missing`, `unavailable`, or `error`
- `result`: journal bundle or service-result summary
- `warnings`: stable warning codes
- `errors`: stable error codes

Error responses may use HTTP status codes appropriate to the failure, but the
JSON body must still be safe and stable:

- malformed or invalid body: `400`, error code `validation_error` or
  `malformed_json`
- missing bundle: `404`, error code `not_found`
- service conflict: `409`, error code `conflict`
- missing service wiring: `503`, error code `service_unavailable`
- unexpected failure: `500`, error code `internal_error`

The response must not expose raw note text in failed responses. Successful write
responses may return service records only if they are JSON-safe and do not
contain secrets, raw local paths, raw Player.log excerpts, raw saved-event
payloads, raw hashes, webhook URLs, or stack traces.

### Request Shape

All attached journal writes should use an explicit context object. Supported
context keys are intentionally the same parser-owned identifiers already used
by the Match Journal service/status API boundary:

- `parser_match_id`
- `parser_game_id`
- `game_number`

The UI/backend may map displayed analytics `match_id` and `game_id` fields to
the service context only when those fields are already parser-normalized IDs
from backend responses. The UI must not invent match/game identity, guess
current match identity, or infer missing parser IDs from display text.

Notes:

- `note_scope` must be one of `match`, `game`, `sideboarding`, or
  `unattached`.
- Attached scopes require context.
- Unattached note requests must not include misleading match/game context.
- Invalid attached note requests must fail validation and must not silently
  become unattached notes.

Opponent labels:

- `archetype` and `tier` are manual user labels only.
- They must be displayed as human annotations, not parser classifications or
  strategic truth.

Review flags:

- `flag_type` must be a stable string from a small allowed set or a validated
  freeform-safe label if the service already supports it.
- Review flags are workflow signals only.

Experiment label:

- `experiment_label` is a human-owned grouping label only.
- It must not change parser, analytics, or workbook behavior.

Display corrections:

- `target_surface` must be constrained to journal display/review surfaces.
- `effect_scope` must remain `journal_display_only`.
- Display corrections must never rewrite parser outputs, analytics rows,
  workbook rows, raw evidence, or evidence-ledger facts.

## Truth Ownership Boundaries

Parser/state owns:

- match identity
- game identity
- match/game result
- play/draw
- parser-normalized event interpretation
- parser-managed fields already emitted to analytics or workbook surfaces

Evidence ledger owns:

- provenance
- confidence
- finality
- drift labels
- degradation status

Analytics owns:

- downstream SQLite storage and deterministic views over parser-normalized
  facts
- read-only context rows shown in the cockpit

Match Journal owns:

- human notes
- manual opponent labels
- review flags
- experiment labels
- journal-display-only correction proposals

FastAPI backend owns:

- local loopback API orchestration
- browser-safe validation and response envelopes
- service wiring and safe unavailable states

Frontend cockpit owns:

- display
- form state
- explicit user submissions to backend routes
- safe degraded/unavailable UI

The cockpit must not become parser truth, analytics truth, evidence truth,
workbook truth, merge readiness, deploy readiness, AI truth, coaching truth, or
strategic advice.

## Unavailable And Degraded Behavior

If the Match Journal service factory/repository wiring is absent, the backend
must return `service_unavailable` and the frontend must:

- show a visible unavailable/degraded state;
- keep parser/analytics context readable when available;
- disable journal write forms or prevent submission;
- avoid retry loops that spam the backend;
- avoid creating local app folders or databases merely by loading the cockpit.

If parser context is missing, the UI may still allow an explicitly unattached
note only when the user chooses the unattached-note path. It must not attach
that note to a guessed match/game.

If a bundle is not found for an explicit context, the UI should show an empty or
not-found journal state and may offer creation of allowed attached notes against
that explicit context.

## Protected Surfaces

Codex C must not change:

- parser behavior
- parser state final reconciliation
- parser event classes
- match/game identity
- deduplication
- evidence-ledger semantics
- analytics schema, migrations, or ingest behavior
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets behavior
- output transport
- production behavior
- OpenAI/model-provider behavior
- AI/coaching behavior
- Line Tracer behavior
- status API CORS behavior except by separate contract
- generated local artifact policy
- secrets, credentials, API keys, tokens, webhook URLs, or environment variable
  policy

Codex C must not create or commit:

- raw Player.log files
- private JSONL artifacts
- generated SQLite databases
- WAL/SHM/journal files
- runtime logs/status files
- failed posts
- workbook exports
- generated/private/local-only artifacts
- secrets or credentials

## Out Of Scope

- direct browser-to-status-API writes
- broad status API CORS hardening
- public network access
- production deployment
- packaged app mode
- overlay UI
- Google Sheets integration
- Apps Script integration
- workbook edits
- analytics schema changes
- analytics ingest changes
- parser/runtime behavior changes
- pilot-error browser controls
- AI coaching
- OpenAI runtime integration
- hidden-card inference
- archetype-as-truth classification
- matchup advice
- player mistake labels as facts
- best-line or Line Tracer behavior
- destructive database or job controls

## Unknowns

- Exact production-like Match Journal service factory wiring for the FastAPI
  local app is not yet implemented in the inspected code.
- The first cockpit UI may need a small context-selection affordance from
  existing match/game rows; the exact component split is left to Codex C.
- It is unknown whether `experiment_label` has an existing status API route.
  The service supports experiment labels, so the FastAPI facade may expose it
  directly if service wiring is available.
- It is unknown whether #202 will later require direct status API use for an
  overlay or non-React client. That should remain a follow-up contract.

## Suspected Gaps

- There is no browser-facing Match Journal facade in the FastAPI backend.
- There are no frontend types, validators, fetch helpers, or tests for Match
  Journal cockpit responses.
- There is no UI section for journal bundle display or journal write forms.
- Current status API wildcard CORS is not appropriate as the first browser
  write path.
- There is no local app backend test asserting Match Journal routes preserve
  narrowed CORS and fail closed when service wiring is absent.
- There is no frontend test asserting the cockpit avoids direct status API
  calls and disables writes when the backend reports service unavailable.

## Required Test Coverage

### Backend Tests

Codex C should add focused FastAPI backend tests that prove:

- route inventory includes required `/api/journal/...` routes and still has no
  DELETE routes;
- journal routes do not add wildcard CORS;
- disallowed non-loopback origins are not allowed;
- missing service wiring returns a safe `service_unavailable` response;
- malformed JSON or invalid payloads do not call the service;
- attached notes require explicit context;
- invalid attached note requests do not become unattached notes;
- opponent labels, review flags, experiment labels, and display corrections
  dispatch to the expected service methods;
- display correction requests preserve `journal_display_only` scope;
- service exceptions map to safe envelopes without raw exception details or raw
  note text in failed responses;
- read-only bundle lookup does not create generated app-data artifacts.

### Frontend Tests

Codex C should add focused frontend tests that prove:

- the cockpit renders read-only parser/analytics context;
- the cockpit renders a journal bundle when the backend returns one;
- unavailable/degraded Match Journal states are safe and disable write forms;
- allowed forms call only `/api/journal/...` FastAPI routes;
- the UI never calls direct `/journal/...` status API routes;
- parser context fields are displayed as read-only and not editable;
- display correction controls are clearly display-only;
- pilot-error controls are not present in the first cockpit slice;
- destructive controls are absent;
- raw backend details, raw private paths, raw SQL, stack traces, AI/coaching
  language, hidden-card claims, and player-mistake truth language are absent.

### Existing Coverage To Preserve

- `tests/test_match_journal_status_api.py` should remain valid.
- `tests/test_analytics_local_app_backend.py` should continue to prove narrowed
  CORS and non-destructive local app behavior.
- `frontend/src/App.test.tsx` should continue to prove safe display and no
  destructive controls across existing sections.

## Validation Requirements

Minimum Codex C validation:

```powershell
py -m pytest -q tests/test_match_journal_status_api.py tests/test_analytics_local_app_backend.py tests/test_status_api.py
py -m pytest -q tests/test_match_journal_service.py tests/test_match_journal_repository.py tests/test_match_journal_schema.py
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests
git diff --check
```

If Codex C adds a new focused backend or frontend test file, include it in the
focused pytest/vitest command list.

Recommended safety scans:

```powershell
py tools/check_secret_patterns.py --all
py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation
```

Codex E should verify the same focused slices plus any broader selector output
recommended by `tools/select_validation.py` if it covers local app, frontend, or
Match Journal surfaces.

## Acceptance Criteria

- The contract remains docs-only until Codex C.
- The first cockpit browser path goes through FastAPI local app routes, not
  direct status API routes.
- FastAPI journal routes use Match Journal service behavior and safe envelopes.
- Existing status API journal behavior is preserved.
- The frontend cockpit displays parser/analytics context as read-only.
- First-slice journal writes are limited to notes, manual opponent labels,
  review flags, experiment labels, and journal-display-only correction
  proposals.
- Pilot-error browser controls remain deferred.
- Missing service wiring degrades safely without destructive side effects.
- Tests cover backend safety, frontend safety, and direct-status-API avoidance.
- No parser, runtime, analytics schema, workbook, webhook, Apps Script, Sheets,
  AI, production, or generated-artifact surfaces are changed.

## Stop Conditions

Stop and route back to Codex B or A if implementation requires:

- browser-to-status-API writes;
- status API CORS changes;
- pilot-error browser controls;
- analytics schema or migration changes;
- parser/runtime behavior changes;
- new truth ownership for frontend/backend/analytics;
- external network access;
- production deployment;
- generated/private artifact commits;
- secret, credential, or environment variable policy changes;
- AI/coaching/model-provider behavior;
- destructive UI or API controls.

## Codex C Handoff Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #232:
https://github.com/Tahjali11/Mythic-Edge/issues/232

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Source contract:
docs/contracts/match_journal_cockpit_ui.md

Goal:
Compare the current local app backend, status API, Match Journal service, and
React frontend against the cockpit UI contract. Then implement only the narrow
first browser-facing Match Journal cockpit slice authorized by the contract.

Before editing:
- Confirm branch and git status.
- State what the cockpit is supposed to do.
- State what the code currently does.
- State why the first browser path must use the FastAPI backend instead of
  direct status API writes.
- State the exact minimal implementation plan.

Expected implementation scope:
- Add a FastAPI `/api/journal/...` facade that uses Match Journal service
  behavior and safe local app response envelopes.
- Preserve narrowed local app CORS; do not add wildcard CORS.
- Add frontend types, validators, fetch helpers, and UI for the first cockpit
  slice.
- Display parser/analytics context read-only.
- Allow only first-slice journal writes: match/game/sideboarding notes, manual
  opponent labels, review flags, experiment labels, and journal-display-only
  correction proposals.
- Show safe unavailable/degraded states when journal service wiring is absent.
- Add focused backend and frontend tests.

Do not:
- call the status API directly from the browser;
- change status API CORS;
- add pilot-error browser controls;
- change parser behavior, parser state final reconciliation, parser event
  classes, match/game identity, deduplication, analytics schema, migrations,
  ingest behavior, workbook schema, webhook payload shape, Apps Script behavior,
  Sheets behavior, output transport, production behavior, OpenAI/model-provider
  behavior, AI/coaching behavior, Line Tracer behavior, or generated-artifact
  policy;
- create or commit raw logs, private JSONL artifacts, generated SQLite DB/WAL/
  SHM/journal files, runtime artifacts, failed posts, workbook exports, secrets,
  credentials, API keys, tokens, webhook URLs, or local-only artifacts;
- target main, stage, commit, push, open a PR, or close issues unless explicitly
  asked.

Validation:
py -m pytest -q tests/test_match_journal_status_api.py tests/test_analytics_local_app_backend.py tests/test_status_api.py
py -m pytest -q tests/test_match_journal_service.py tests/test_match_journal_repository.py tests/test_match_journal_schema.py
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests
git diff --check
py tools/check_secret_patterns.py --all
py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract artifact used
- files changed
- exact backend/frontend/test sections changed
- what was verified
- what remains unverified
- whether forbidden scope was touched
- next recommended role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/232"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/match_journal_cockpit_ui.md"
  target_artifact: "docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch --untracked-files=all"
    - "git diff --check"
    - "py tools/check_agent_docs.py"
    - "path-scoped secret/private marker scan for docs/contracts/match_journal_cockpit_ui.md"
    - "path-scoped protected-surface scan for docs/contracts/match_journal_cockpit_ui.md"
  stop_conditions:
    - "Do not call the status API directly from the browser."
    - "Do not change status API CORS without a separate contract."
    - "Do not add pilot-error browser controls in the first cockpit slice."
    - "Do not change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```
