# Match Journal Status API Contract

## Module

Match Journal local HTTP/status API bridge v1.

This contract defines a narrow loopback-only JSON API over the existing Match
Journal service. It authorizes future Codex C work to expose local journal read
and write commands through the existing status API surface without changing
parser behavior, runtime output, analytics ingest, workbook/webhook/App Script
behavior, local app UI behavior, Google Sheets behavior, OpenAI/model-provider
behavior, or production behavior.

Plain English: this API is a local doorway into the Match Journal service. It
can pass a human note or label to the service, then return the service result.
It must not become a parser, an analytics engine, a workbook sync path, or a
coaching layer.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/203

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/202

Routing decision:

- Issue #203 still routes through tracker #202, Match Journal and cockpit
  foundation.
- Tracker #204 and umbrella issue #207 are analytics/local-app work and
  explicitly keep Match Journal/status API work separate unless later
  instructed.

## Related Authority

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- `docs/contracts/match_journal_local_sqlite_schema.md`
- `docs/contracts/match_journal_repository.md`
- `docs/contracts/match_journal_service.md`
- `docs/implementation_handoffs/match_journal_service_comparison.md`
- `docs/contract_test_reports/match_journal_service.md`

## Risk Tier

High.

Reasons:

- This adds local HTTP write routes.
- It sits near runtime/status API code that is currently read-oriented.
- It touches private human-authored notes and generated local SQLite state.
- It must preserve parser truth ownership and avoid exposing raw paths,
  secrets, local artifacts, or destructive database controls.

## Owning Layer

Primary owning layer: Local App / UI bridge over the Match Journal
human-intent layer.

`src/mythic_edge_parser/app/status_api.py` remains bridge code: it transports
local status and journal service results. It does not own parser truth, journal
truth, analytics truth, workbook truth, merge readiness, deploy readiness, or
credential policy.

## Truth Owner

- Parser/state owns parser match/game facts and parser IDs.
- Match Journal service owns human-intent journal commands and result shapes.
- Match Journal repository owns local SQLite row validation and persistence.
- Status API owns only local HTTP request parsing, response shaping, and safe
  service dispatch.

## Bridge-Code Status

`bridge_code`

Bridge from:

- Match Journal human-intent service

Bridge to:

- local loopback HTTP/status API clients

Allowed data flow:

- JSON request -> safe route validation -> `MatchJournalService` command ->
  sanitized JSON response

Forbidden reverse-flow:

- HTTP clients must not rewrite parser facts, analytics facts, workbook rows,
  webhook payloads, Apps Script behavior, runtime status artifacts, Google
  Sheets state, or production behavior.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/match_journal_status_api.md`

Future implementation files authorized by this contract:

- `src/mythic_edge_parser/app/status_api.py`
- `tests/test_status_api.py`
- `tests/test_match_journal_status_api.py`, if Codex C chooses a focused new
  test file
- `docs/implementation_handoffs/match_journal_status_api_comparison.md`

Existing files Codex C may read but should not change unless a direct import
or narrow test seam requires it:

- `src/mythic_edge_parser/app/match_journal_service.py`
- `src/mythic_edge_parser/app/match_journal_repository.py`
- `src/mythic_edge_parser/app/match_journal_migration_loader.py`
- `tests/test_match_journal_service.py`
- `tests/test_match_journal_repository.py`
- `tests/test_match_journal_schema.py`
- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`

Not owned by this contract:

- parser modules
- parser state final reconciliation
- parser event classes
- match/game identity or deduplication
- analytics schema, migrations, ingest, or views
- local app/frontend UI
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- OpenAI/model-provider behavior
- generated SQLite database files
- runtime status files
- failed posts
- raw logs
- workbook exports
- secrets, credentials, tokens, API keys, webhook URLs, or environment
  variable policy changes

If implementation requires a new database path contract, new environment
variable contract, analytics join, UI change, workbook sync, parser lookup, or
production behavior, Codex C must stop and route back to Codex B or A.

## Observed Current Behavior

- `status_api.py` exposes GET routes for local status, active match, timeline,
  actions, active deck, match history, collection, and card performance.
- `status_api.py` currently does not implement POST, JSON body parsing,
  journal routes, or Match Journal service wiring.
- Existing status API tests exercise server start/stop, GET payload routing,
  query parsing, and health shape preservation.
- `config.py` defaults `STATUS_API_HOST` to `127.0.0.1`,
  `STATUS_API_PORT` to `6843`, and `ENABLE_STATUS_API` to true.
- The Match Journal service exists and exposes local human-intent operations
  for notes, experiment labels, pilot-error status/reason, manual opponent
  labels, review flags, display-only corrections, and journal bundles.
- The service accepts caller-owned repository/connections and must not open
  default database files or read parser/status runtime state.
- `.gitignore` ignores `data/match_journal/`.
- Issue #203 remains open and #202 remains the correct tracker.
- Issue #204/#207 context says Match Journal/status API work is separate from
  the analytics local app work.

## Required Guarantees

### Local-Only HTTP Boundary

- Journal routes must be loopback-only.
- Supported loopback host values are `127.0.0.1`, `localhost`, and `::1`.
- If future implementation cannot prove the server is bound to a loopback host,
  write-capable journal routes must fail closed.
- No route may expose arbitrary SQL, database browser behavior, filesystem
  browsing, cleanup commands, destructive database actions, live workbook
  actions, Google Sheets actions, webhook posts, Apps Script calls, OpenAI
  calls, or production deployment actions.

### Thin Service Dispatch

- HTTP routes must call `MatchJournalService` methods.
- HTTP route code must not write direct SQL.
- HTTP route code must not infer parser match/game IDs from runtime state.
- HTTP route code must not parse note text into facts.
- HTTP route code must not classify archetypes, infer hidden cards, label
  gameplay mistakes, produce strategic advice, or call AI/model providers.
- Parser IDs in requests are references only.

### Explicit Service Wiring

Future implementation must make Match Journal service availability explicit and
testable.

Allowed implementation choices:

- inject a service factory into status API route helpers for tests and local
  runtime startup; or
- add a small status API configuration seam that constructs a service from an
  explicitly supplied caller-owned SQLite connection.

Forbidden implementation choices:

- silently open a default Match Journal database file from route helpers;
- read a new environment variable without a separate config contract;
- create generated database files during unit tests;
- hide unavailable service wiring by pretending journal writes succeeded.

If the service is not configured, journal routes must return a sanitized
`503 Service Unavailable` response.

## Public Interface

### Existing Routes

The existing GET routes must remain available and backward compatible:

- `GET /`
- `GET /health`
- `GET /status`
- `GET /active-match`
- `GET /timeline`
- `GET /actions`
- `GET /active-deck`
- `GET /match-history`
- `GET /collection`
- `GET /card-performance`

Adding journal routes must not change these route payload shapes except that
the root route may include the new journal route names in its route inventory.

### New Route Inventory

Required new routes:

- `GET /journal`
- `POST /journal/notes`
- `POST /journal/pilot-error`
- `POST /journal/opponent-labels`
- `POST /journal/review-flags`
- `POST /journal/display-corrections`

Optional route, if Codex C keeps it as a thin alias:

- `POST /journal/experiment-label`

If omitted, experiment labeling remains available later through a separate UI
or API contract.

### GET /journal

Purpose:

- Return one local Match Journal bundle from `MatchJournalService`.

Accepted query fields:

- `journal_match_id`
- `journal_game_id`
- `parser_match_id`
- `parser_game_id`
- `game_number`

Rules:

- At least one query field must be supplied.
- `game_number`, when supplied, must parse as a positive integer.
- The route must not fall back to active runtime match state.
- If the service returns no bundle, return `404` with a sanitized error code.
- If multiple journal records match the supplied parser ID, return `409`.

Successful response result:

```json
{
  "object": "match_journal_api_response",
  "ok": true,
  "result": {
    "bundle": {}
  },
  "warnings": []
}
```

### POST /journal/notes

Purpose:

- Record match, game, sideboarding, or explicitly unattached notes.

Required JSON body fields:

- `note_text`: non-empty string
- `note_scope`: one of `match`, `game`, `sideboarding`, `unattached`

Optional JSON body fields:

- `context`: attachment context object
- `author_label`
- `source_surface`
- `privacy_label`
- `note_format`
- `created_at`
- `updated_at`
- `valid_from`

Rules:

- `note_scope = "match"` maps to `record_match_note`.
- `note_scope = "game"` maps to `record_game_note`.
- `note_scope = "sideboarding"` maps to `record_sideboarding_note`.
- `note_scope = "unattached"` maps to `record_unattached_note`.
- Missing context is allowed only for `note_scope = "unattached"`.
- For `match`, `game`, and `sideboarding`, missing context must return `400`
  instead of silently creating an unattached note.
- The route must not echo full note text in error responses.

### POST /journal/pilot-error

Purpose:

- Record pilot-error review metadata.

Required JSON body fields:

- `context`: attachment context object
- `status`: one of `yes`, `no`, `unknown`, `not_reviewed`

Optional JSON body fields:

- `reason`: non-empty string
- `note_text`: non-empty string
- common service options

Rules:

- The route maps to `record_pilot_error_review` when `reason` or `note_text`
  is present.
- A status-only request may map to `set_pilot_error_status`.
- Pilot-error status and reason must remain separately queryable service rows.
- Pilot-error data is human review metadata, not parser truth, player-mistake
  truth, merge readiness, deploy readiness, AI coaching, or gameplay advice.

### POST /journal/opponent-labels

Purpose:

- Store manual opponent labels.

Required JSON body fields:

- `context`: attachment context object
- at least one of `archetype` or `tier`

Rules:

- The route maps to `set_opponent_labels`.
- Labels are manual annotations only.
- The route must not classify archetypes from cards, actions, decklists,
  external websites, model output, or hidden information.

### POST /journal/review-flags

Purpose:

- Store local review flags.

Required JSON body fields:

- `context`: attachment context object
- `flag_type`

Optional JSON body fields:

- `flag_status`
- `priority_label`
- `reason`
- common service options

Rules:

- The route maps to `flag_for_review`.
- `suspected_parser_gap` is review metadata only, not proof of parser error.
- Review flags must not become CI truth, merge readiness, deploy readiness, or
  parser correctness truth.

### POST /journal/display-corrections

Purpose:

- Store display-only field correction proposals.

Required JSON body fields:

- `context`: attachment context object
- `target_surface`
- `target_field`
- `proposed_value_label`

Optional JSON body fields:

- `original_value_label`
- `override_reason`
- `override_status`
- common service options

Rules:

- The route maps to `propose_display_correction`.
- `effect_scope` must be forced to or validated as `journal_display_only`.
- A display correction must never update parser facts, analytics facts,
  workbook rows, webhook payloads, Apps Script, runtime status, local app UI
  state, Google Sheets, or OpenAI/model-provider output.

## JSON Response Contract

All journal routes must return a consistent sanitized envelope.

Successful response:

```json
{
  "object": "match_journal_api_response",
  "ok": true,
  "result": {},
  "warnings": []
}
```

Failure response:

```json
{
  "object": "match_journal_api_response",
  "ok": false,
  "error": {
    "code": "validation_error",
    "message": "request validation failed"
  },
  "warnings": []
}
```

Required error codes:

- `malformed_json`
- `validation_error`
- `not_found`
- `conflict`
- `service_unavailable`
- `method_not_allowed`
- `not_found_route`
- `internal_error`

Required HTTP statuses:

- `200` for successful reads and writes
- `400` for malformed JSON and validation errors
- `404` for missing bundle or unknown route
- `405` for unsupported methods on known routes
- `409` for service conflicts
- `503` when Match Journal service wiring is unavailable
- `500` for unexpected internal errors with sanitized messages

Sanitization rules:

- Failure responses must not include raw note text, raw payload dumps, raw
  local paths, raw hashes, raw Player.log data, runtime status file content,
  failed posts, workbook exports, secrets, credentials, tokens, API keys,
  webhook URLs, or model-provider responses.
- Unexpected exception messages must be reduced to stable labels or short safe
  summaries.

## Inputs

Allowed inputs:

- JSON request bodies supplied by a local loopback client
- query strings for `GET /journal`
- caller-provided attachment context values
- human-authored note text and labels
- synthetic test requests
- an injected `MatchJournalService` or service factory

Forbidden inputs:

- raw Player.log payloads
- raw local artifact paths as request data
- raw saved-event JSONL payloads
- runtime status JSON as an implicit attachment source
- failed posts
- workbook exports
- secrets, credentials, tokens, API keys, webhook URLs
- OpenAI/model-provider responses
- external website data

## Outputs

Allowed outputs:

- HTTP JSON responses on the local loopback status API
- Match Journal service writes to caller-owned local SQLite connections when
  explicitly configured
- focused tests and implementation handoff documentation in future Codex C work

Forbidden outputs:

- committed SQLite database files, WAL, SHM, journal, or DB artifacts
- committed raw logs
- committed runtime status files
- committed failed posts
- committed workbook exports
- committed secrets or credentials
- webhook posts
- Apps Script calls
- Google Sheets writes
- OpenAI/model-provider calls
- parser row mutations
- analytics fact mutations
- arbitrary SQL output

## Invariants

- Journal API routes are transport only.
- Journal API routes must use Match Journal service methods.
- Journal API routes must not write direct SQL.
- Journal API routes must not create parser match IDs or parser game IDs.
- Journal API routes must not read parser runtime state to infer context.
- Missing context for attached note scopes must fail rather than silently
  creating unattached notes.
- Explicit unattached notes must remain supported.
- Pilot-error status and reason must remain separately queryable.
- Opponent labels must remain manual human annotations.
- Display corrections must remain `journal_display_only`.
- Existing GET status route behavior must remain backward compatible.
- Tests must use synthetic note text and in-memory SQLite or explicitly
  injected test services.
- No generated/private/local artifacts may be committed.

## Invalid Payload Behavior

Malformed JSON:

- Return `400` with `malformed_json`.
- Do not call the service.

Unsupported fields:

- Return `400` with `validation_error`.
- Do not call the service unless Codex C proves the service itself rejects
  unsupported fields before writes.

Invalid enum or type:

- Return `400` with `validation_error`.
- Convert `game_number` only when it is an integer-like request value.
- Reject booleans and fractional values for `game_number`.

Service validation error:

- Return `400`.

Service not found:

- Return `404`.

Service conflict:

- Return `409`.

Unexpected exception:

- Return `500` with a sanitized `internal_error`.
- Do not expose raw exception details.

## Unattached-Note Behavior

- `POST /journal/notes` with `note_scope = "unattached"` must preserve an
  unattached note with no parser or journal context.
- `POST /journal/notes` with `note_scope` of `match`, `game`, or
  `sideboarding` must require context.
- The API must never silently convert a failed attached-note request into an
  unattached note.
- The API must never invent parser IDs to attach a note.

## Side Effects

Allowed side effects in future implementation:

- local HTTP response generation
- calls to an injected Match Journal service
- journal service writes to caller-owned local SQLite connections
- in-memory SQLite state in tests
- implementation handoff documentation

Forbidden side effects:

- parser behavior changes
- parser state final reconciliation changes
- parser event class changes
- match/game identity or deduplication changes
- analytics schema, migration, ingest, or view changes
- runtime status artifact writes from journal routes
- workbook schema changes
- webhook payload changes
- Apps Script changes
- Google Sheets writes
- frontend/local app UI changes
- OpenAI/model-provider calls
- generated database files in the repo
- raw/private/local artifact writes in the repo

## Dependency Order

Recommended Codex C order:

1. Confirm branch and git status.
2. Compare current `status_api.py`, Match Journal service, and tests against
   this contract.
3. Add route-helper seams for POST JSON parsing and journal service dispatch.
4. Add test-only service injection or factory wiring.
5. Add focused tests for route inventory, success paths, invalid payloads,
   service unavailable, unattached notes, context-required note scopes,
   conflict/not-found mapping, and existing GET route compatibility.
6. Implement the smallest status API changes needed to pass those tests.
7. Add the implementation handoff.
8. Run validation and artifact scans.

## Compatibility

Must remain compatible with:

- `match_journal_service.v1`
- `match_journal_repository.v1`
- `match_journal_local_sqlite_schema.v1`
- existing `status_api.py` GET routes and response shapes
- existing status API server start/stop helpers
- local loopback status API defaults

Must not require:

- a frontend UI
- a default database opener in route helpers
- a new environment variable
- parser runtime state lookup
- analytics joins
- Google Sheets sync
- OpenAI/model-provider runtime integration
- production deployment changes

## Unknowns

- Whether the eventual local cockpit will call these routes from the existing
  local app backend, directly from a browser, or through a later API facade.
- Whether a future database path/config contract should add an explicit Match
  Journal database opener for local runtime use.
- Whether journal route naming should eventually move from `status_api.py` to a
  local app backend module.
- Whether write routes need stronger local authorization once a UI exists.

## Suspected Gaps

- `status_api.py` has no POST handling today.
- There is no configured Match Journal service seam in status API.
- There are no tests for JSON request parsing or write-route error mapping.
- There is no explicit service-unavailable behavior for journal routes.
- Existing status API CORS behavior is broad for GET routes; write routes need
  loopback-only protection before any browser-facing use.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior
- parser state final reconciliation
- parser event classes
- parser event kind values
- parser payload shapes
- match identity
- game identity
- deduplication
- analytics schema, migrations, ingest, or views
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets behavior
- frontend/local app UI behavior
- output transport
- production behavior
- AI/model-provider behavior
- secrets, credentials, API keys, tokens, webhook URLs, environment variable
  policy, raw logs, generated data, runtime status artifacts, failed posts,
  workbook exports, local JSONL artifacts, generated SQLite files, or
  local-only artifacts

## Tests Required

Codex C must add or update focused tests for:

- root route inventory includes journal routes without removing existing GET
  routes;
- existing GET `/health`, `/status`, `/match-history`, and `/actions` behavior
  remains compatible;
- known POST journal routes reject unsupported methods correctly;
- malformed JSON returns `400` and does not call the service;
- missing service wiring returns `503`;
- `GET /journal` maps query context to `get_journal_bundle`;
- `POST /journal/notes` maps note scopes to the correct service methods;
- attached note scopes require context;
- explicit unattached note scope works without context;
- pilot-error route preserves separate status/reason behavior through service
  result shape;
- opponent labels remain manual service calls;
- review flags remain local review metadata;
- display corrections force or preserve `journal_display_only`;
- validation, not-found, conflict, and unexpected errors map to safe HTTP
  envelopes;
- response envelopes do not expose raw paths, secrets, raw payloads, or full
  private note text;
- no generated SQLite/local/private artifacts are created by tests.

Recommended validation commands:

```powershell
py -m pytest -q tests/test_status_api.py tests/test_match_journal_service.py
py -m pytest -q tests/test_match_journal_status_api.py
py -m pytest -q tests/test_match_journal_schema.py tests/test_match_journal_repository.py tests/test_match_journal_service.py tests/test_status_api.py
py -m ruff check src tests tools
git diff --check
@'
docs/contracts/match_journal_status_api.md
src/mythic_edge_parser/app/status_api.py
tests/test_status_api.py
tests/test_match_journal_status_api.py
docs/implementation_handoffs/match_journal_status_api_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/match_journal_status_api.md
src/mythic_edge_parser/app/status_api.py
tests/test_status_api.py
tests/test_match_journal_status_api.py
docs/implementation_handoffs/match_journal_status_api_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
git status --short --branch --untracked-files=all
```

If Codex C does not create `tests/test_match_journal_status_api.py`, it should
omit that path from path-scoped commands and explain where focused route tests
were added.

## Acceptance Criteria

This contract is ready for Codex C when:

- `docs/contracts/match_journal_status_api.md` exists.
- The route inventory is explicit.
- JSON request and response envelopes are explicit.
- Service wiring and service-unavailable behavior are explicit.
- Invalid payload behavior is explicit.
- Unattached-note behavior is explicit.
- Local-only/privacy boundaries are explicit.
- Generated-artifact boundaries are explicit.
- Protected surfaces are explicit.
- Validation expectations are explicit.

The implementation is acceptable only if:

- It changes only status API route code, focused tests, and implementation
  handoff documentation unless Codex C routes back for a contract update.
- It remains a thin HTTP bridge over `MatchJournalService`.
- It does not change parser/runtime/workbook/webhook/App Script/Sheets/
  analytics/UI/AI/production behavior.
- It does not create or commit SQLite/generated/private/runtime artifacts.
- It does not expose raw private data, raw paths, secrets, arbitrary SQL,
  destructive database actions, or production actions.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #203:
Match Journal local HTTP/status API bridge.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/203

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Current branch:
codex/analytics-foundation

Contract:
docs/contracts/match_journal_status_api.md

Goal:
Compare the current status API, Match Journal service, and focused tests
against the contract. Implement only the smallest local loopback-only JSON
route bridge over MatchJournalService needed to satisfy the contract, then
produce docs/implementation_handoffs/match_journal_status_api_comparison.md.

Before editing:
- Confirm branch and git status.
- Confirm #203 still routes through tracker #202 and has not been rerouted
  under #204/#207.
- State what the API is supposed to do, what current code already does, what
  gaps remain, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/match_journal_status_api.md
- docs/contracts/match_journal_service.md
- docs/contracts/match_journal_repository.md
- docs/contracts/match_journal_local_sqlite_schema.md
- src/mythic_edge_parser/app/status_api.py
- src/mythic_edge_parser/app/match_journal_service.py
- src/mythic_edge_parser/app/match_journal_repository.py
- src/mythic_edge_parser/app/config.py
- tests/test_status_api.py
- tests/test_match_journal_service.py
- tests/test_match_journal_repository.py
- tests/test_match_journal_schema.py

Implement:
- Add loopback-only Match Journal route handling over MatchJournalService.
- Preserve all existing GET status API behavior.
- Add focused route tests for success paths, invalid payloads, missing service
  wiring, unattached-note behavior, context-required note scopes, and safe
  error envelopes.
- Add docs/implementation_handoffs/match_journal_status_api_comparison.md.

Do not:
- Target main.
- Change parser behavior, parser state final reconciliation, parser event
  classes, match/game identity, deduplication, analytics schema/migrations/
  ingest/views, workbook schema, webhook payload shape, Apps Script behavior,
  Google Sheets behavior, frontend/local app UI behavior, output transport,
  production behavior, OpenAI/model-provider behavior, AI/coaching behavior, or
  environment variable policy.
- Create or commit SQLite database files, WAL/SHM/journal files, raw logs,
  generated data, runtime status artifacts, failed posts, workbook exports,
  secrets, credentials, API keys, tokens, webhook URLs, local JSONL artifacts,
  or local-only artifacts.
- Open arbitrary SQL, destructive database actions, Google Sheets sync,
  workbook export, webhook posts, Apps Script calls, OpenAI calls, hidden-card
  inference, archetype classification, player-mistake truth, gameplay advice,
  merge readiness, or deploy readiness.
- Stage, commit, push, open a PR, merge, or close issues unless explicitly
  asked.

Validation:
- py -m pytest -q tests/test_status_api.py tests/test_match_journal_service.py
- py -m pytest -q tests/test_match_journal_status_api.py, if created
- py -m pytest -q tests/test_match_journal_schema.py tests/test_match_journal_repository.py tests/test_match_journal_service.py tests/test_status_api.py
- py -m ruff check src tests tools
- git diff --check
- path-scoped secret/private marker and protected-surface checks for changed
  files
- git status --short --branch --untracked-files=all
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/203"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/match_journal_status_api.md"
  target_artifact: "docs/implementation_handoffs/match_journal_status_api_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "Codex B documentation-only validation required before handoff"
  stop_conditions:
    - "Do not target main."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/analytics/UI/AI/production behavior."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
    - "Do not expose arbitrary SQL, destructive database controls, raw paths, raw payloads, secrets, Google Sheets sync, workbook export, webhook posts, Apps Script calls, OpenAI calls, hidden-card inference, archetype classification, player-mistake truth, gameplay advice, merge readiness, or deploy readiness."
```
