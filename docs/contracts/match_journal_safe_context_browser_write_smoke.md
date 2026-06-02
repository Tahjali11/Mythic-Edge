# Match Journal Safe Context Browser Write Smoke Contract

## Module

Match Journal safe context path for browser write/persistence smoke.

Plain English: issue #237 exists because the app can launch and show the Match
Journal cockpit with a disposable app-data root, but the browser cannot yet save
and reload one test journal entry when that disposable root has no match/game
history. This contract chooses the smallest safe path: an explicitly
unattached, clearly labeled smoke note written through the local app journal
API, not a fake parser match or game.

## Source Issue

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/237>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/202>
- Source blocker from issue #236: `blocked_no_safe_context`
- Completed prerequisite: issue #236 / PR #238, merge commit
  `452cdfb395730e05a9ca45ef18bcb089ec833a1c`

## Authority And Source Artifacts

This contract is governed by:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- issue #237
- tracker #202

Issue #236 context inspected:

- `docs/contracts/match_journal_live_browser_real_app_data_readiness.md`
- `docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md`
- `docs/contract_test_reports/match_journal_live_browser_real_app_data_readiness.md`

Current implementation surfaces inspected:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/match_journal_cockpit.py`
- `src/mythic_edge_parser/local_app/match_journal_runtime.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/app/match_journal_service.py`
- `src/mythic_edge_parser/app/match_journal_repository.py`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `tests/test_match_journal_cockpit_ui_backend.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_dev_app_launcher.py`

## Risk Tier

High.

Reasons:

- The work exercises browser writes to a local SQLite journal.
- The smoke may create app-owned generated SQLite state.
- The current disposable root intentionally has no parser-owned match/game
  context.
- A careless implementation could invent parser identity, write to the actual
  app-data root, expose raw note data, or add a broad database browsing surface.
- The browser facade sits near parser, analytics, local app, local artifact,
  and CORS boundaries.

## Owning Layer

Primary owning layer: Local App / UI.

Truth ownership:

- Match Journal owns the human or synthetic journal note row created by this
  smoke.
- The local app owns browser display, request validation, and smoke evidence.
- Parser/state remains the source of truth for parser-managed facts,
  match/game identity, deduplication, and final reconciliation.
- Analytics remains a downstream deterministic storage/view layer.
- The smoke result is validation evidence only. It is not parser truth,
  analytics truth, workbook truth, production readiness, coaching truth, or AI
  truth.

## Internal Project Area

Local App / UI.

## Bridge-Code Status

`stable_bridge`

Bridge from:

- React/Vite browser UI
- FastAPI local app facade
- Match Journal service/repository
- app-owned generated SQLite state under the selected app-data root

Allowed data flow:

```text
browser UI -> /api/journal/... -> Match Journal service -> Match Journal SQLite
```

Forbidden reverse flow:

- Smoke notes must not rewrite parser facts.
- Smoke notes must not become analytics facts.
- Smoke notes must not change workbook rows, webhook payloads, Apps Script,
  Google Sheets, production behavior, AI/model-provider output, Line Tracer, or
  coaching behavior.

## Contract Decision

Issue #237 should use the explicitly safe unattached-note browser path.

Required default strategy:

1. Launch the local app with a disposable app-data root.
2. Render the Match Journal cockpit when no match/game context exists.
3. Expose only a limited browser control for an unattached smoke note.
4. Submit the note through `POST /api/journal/notes`.
5. Use `note_scope = "unattached"` and no `context` object.
6. Label the note text with:

   ```text
   MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW
   ```

7. Verify persistence after refresh/reload using only `/api/journal/...` browser
   facade behavior and journal-owned identifiers.

Synthetic visible match/game context seeding is not the default for #237.
Creating a fake parser match, parser game, analytics row, imported replay,
history row, or workbook row just to make the cockpit context-visible would
muddy parser truth ownership. If Codex C proves the unattached-note path cannot
verify reload persistence without a larger or riskier backend change, route
back to Codex B or Codex A rather than inventing parser IDs.

## Observed Current Behavior

- `backend.py` exposes browser-facing journal routes under `/api/journal/...`.
- `POST /api/journal/notes` already accepts `note_scope = "unattached"` with no
  context.
- `match_journal_cockpit.py` rejects unattached notes that include a context.
- The first explicit unattached backend write creates only
  `<app_data>\db\match_journal.sqlite3` under the selected app-data root.
- Current backend tests assert that successful write responses return compact
  `service_result` metadata without echoing full records or note text.
- `GET /api/journal` currently requires a match/game attachment reference and
  rejects requests with no attachment reference.
- Current frontend `MatchJournalNoteRequest` only allows `match`, `game`, and
  `sideboarding` note scopes.
- Current frontend disables all Match Journal write controls when no context is
  available.
- The #236 live-browser smoke reached the app and cockpit in a disposable root,
  but browser write/persistence was blocked at `blocked_no_safe_context`.
- Actual app-data readiness and actual-root write smoke remain unverified and
  approval-gated.

## Recommended Safe Context Strategy

Use an unattached smoke note.

An unattached smoke note is a Match Journal note with:

- no `parser_match_id`;
- no `parser_game_id`;
- no `journal_match_id`;
- no `journal_game_id`;
- `note_scope = "unattached"`;
- synthetic note text beginning with
  `MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW`;
- app-owned generated storage only under the disposable app-data root.

This strategy is preferred because it proves the browser write path without
pretending there is a parser-owned match or game in an empty disposable root.

## Backend Contract

### Existing Write Route

The browser write must use:

```text
POST /api/journal/notes
```

Required request body:

```json
{
  "note_scope": "unattached",
  "note_text": "MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW ...",
  "author_label": "codex_smoke_test",
  "source_surface": "local_tool",
  "privacy_label": "sanitized_fixture",
  "note_format": "plain_text",
  "priority_label": "normal"
}
```

Required request behavior:

- The request must omit `context`.
- If `context` is present for `note_scope = "unattached"`, the backend must
  reject the request with a sanitized validation error.
- The backend must not synthesize `parser_match_id`, `parser_game_id`,
  `journal_match_id`, or `journal_game_id`.
- The first explicit write may create the app-owned Match Journal database and
  apply Match Journal migrations under the selected app-data root.
- The write must not create analytics SQLite files.
- The write must not touch the actual app-data root unless a later thread gets
  explicit user approval.

Required response behavior:

- The response must keep the existing `mythic_edge_local_app_match_journal`
  object and `match_journal_cockpit_ui.v1` schema version unless Codex C proves
  a narrow backward-compatible addition is required.
- Successful responses must remain compact.
- `service_result` may include `action`, `status`, `primary_record_type`,
  `primary_record_id`, and `record_counts`.
- Successful responses must not echo full service records or raw `note_text`.
- Sanitized failures must not expose local paths, raw SQL, environment values,
  stack traces, secrets, credentials, tokens, webhook URLs, spreadsheet IDs, or
  private data.

### Persistence Readback

Refresh/reload persistence must be proved by reading a journal-owned record
after the page is reloaded. It must not rely only on pre-reload React state.

Preferred readback interface:

```text
GET /api/journal/notes?journal_note_id=<primary_record_id>&note_scope=unattached
```

Codex C may choose an equivalent `/api/journal/...` path only if it is narrower
or already available. Any readback interface must satisfy all of these rules:

- It must require an exact `journal_note_id` returned by the write response.
- It must require or enforce `note_scope = "unattached"` for this smoke.
- It must reject missing IDs, unsupported query parameters, parser context
  fields, malformed IDs, and attempts to list all notes.
- It must open the database read-only.
- A readback request must not create the app-data root or SQLite database when
  the database is missing.
- It must return `missing` or `not_found` for absent records.
- It must return only compact safe metadata, such as:
  - `journal_note_id`
  - `note_scope`
  - `author_label`
  - `source_surface`
  - `privacy_label`
  - `created_at`
  - `updated_at`
  - `smoke_marker_present`
  - `attachment_status = "unattached"` as a derived display label
- It must not return full note text.
- It must not expose raw local paths, SQLite filenames beyond symbolic
  `<app_data>` display paths, SQL, secrets, environment values, or private
  payloads.
- It must not expose generic database browsing or arbitrary SQL.

If current service/repository code cannot support this safely with the existing
Match Journal schema, Codex C should route back to Codex B rather than changing
the schema in issue #237.

## Frontend Contract

When no match/game context exists, the frontend may expose only an unattached
smoke note path.

Required no-context UI behavior:

- The page must still show that no parser-owned match/game context is available.
- Context-bound controls must stay disabled or hidden:
  - opponent labels;
  - review flags;
  - experiment labels;
  - display-only corrections;
  - pilot-error controls;
  - destructive or bulk controls.
- The only write-capable no-context control authorized by #237 is an
  unattached smoke note form.
- The note request must call `/api/journal/notes`.
- The request must use `note_scope = "unattached"`.
- The request must omit `context`.
- The request must include smoke text that begins with
  `MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW`.
- The request must use only the FastAPI local app facade, not direct
  `status_api.py` journal routes.

Allowed type/API change:

- Codex C may add a distinct frontend request type for unattached smoke notes,
  or may widen the existing note request union if the resulting type still
  prevents context-bound forms from submitting without context.
- A distinct `MatchJournalUnattachedNoteRequest` type is preferred because it
  keeps the attached-note contract obvious.

Required reload behavior:

- After successful submit, the UI or browser smoke must capture only the
  journal-owned `primary_record_id`.
- On refresh/reload, the proof must perform a new browser-side readback through
  `/api/journal/...`.
- The reloaded state must show a compact persisted-note confirmation tied to
  the same journal-owned ID.
- The proof must not depend only on React component state from before reload.
- If browser storage is used to carry the note ID across reload, it must store
  only the journal-owned ID and must not store note text, parser IDs, raw paths,
  database paths, secrets, or environment values.

## Disposable-Root Boundary

Disposable-root first remains mandatory for #237.

Codex C must use a temporary app-data root for automated or live-browser smoke
work. The disposable root may create:

- `db\match_journal.sqlite3`;
- SQLite sidecar files only if SQLite creates them during the run;
- app-owned temporary diagnostics/log folders outside the repo if the approved
  launcher creates them.

Codex C must report generated disposable-root artifacts separately from repo
artifacts. Generated files under the disposable root must not be staged or
committed.

## Actual App-Data Root Boundary

Issue #237 does not authorize actual-root writes.

Codex C must not inspect, write, delete, move, rename, archive, sanitize, copy,
upload, reset, wipe, or clean the user's actual app-data root unless the user
explicitly approves that action in a later thread.

Actual-root write smoke remains a separate approval boundary even if the
disposable-root smoke passes.

## Generated And Private Artifact Safety

Never commit:

- generated SQLite databases;
- WAL, SHM, or journal sidecar files;
- frontend build output such as `frontend/dist`;
- raw Player.log files;
- private JSONL artifacts;
- runtime logs;
- failed posts;
- workbook exports;
- secrets;
- credentials;
- tokens;
- API keys;
- webhook URLs;
- spreadsheet IDs;
- environment values;
- local-only artifacts.

The browser/API must not display raw absolute app-data paths. Setup/status may
continue using symbolic paths such as:

```text
<app_data>\db\match_journal.sqlite3
```

## Public Interfaces

Existing public interfaces preserved:

- `GET /api/journal`
- `POST /api/journal/notes`
- `POST /api/journal/opponent-labels`
- `POST /api/journal/review-flags`
- `POST /api/journal/experiment-label`
- `POST /api/journal/display-corrections`
- frontend `fetchMatchJournal`
- frontend `submitMatchJournalNote`
- Match Journal response object:
  `mythic_edge_local_app_match_journal`
- Match Journal schema version:
  `match_journal_cockpit_ui.v1`

Allowed narrow interface addition for #237:

- A compact readback route under `/api/journal/...` for exact unattached note
  verification, preferably:

  ```text
  GET /api/journal/notes?journal_note_id=<primary_record_id>&note_scope=unattached
  ```

This route is allowed only if needed to prove refresh/reload persistence
through the browser path. It must not become a general note listing, SQL,
cleanup, export, import, delete, edit, or database browsing surface.

## Inputs

### Unattached Smoke Note Submit

Source: browser UI.

Destination: `POST /api/journal/notes`.

Required fields:

- `note_scope`: exactly `"unattached"`;
- `note_text`: non-empty string beginning with
  `MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW`.

Recommended metadata fields:

- `author_label`: `"codex_smoke_test"`;
- `source_surface`: `"local_tool"`;
- `privacy_label`: `"sanitized_fixture"`;
- `note_format`: `"plain_text"`;
- `priority_label`: `"normal"`.

Forbidden fields:

- `context`;
- `parser_match_id`;
- `parser_game_id`;
- `journal_match_id`;
- `journal_game_id`;
- raw paths;
- database paths;
- SQL;
- secrets or environment values.

### Unattached Smoke Note Readback

Source: browser UI after refresh/reload.

Destination: `/api/journal/...` compact readback route.

Required fields:

- `journal_note_id`: the exact `primary_record_id` returned by the submit
  response.
- `note_scope`: `"unattached"` if the selected route accepts it.

Forbidden behavior:

- listing notes without an exact ID;
- reading by parser match/game context;
- returning full note text;
- creating database state on read when missing.

## Outputs

### Submit Response

Destination: browser UI and smoke evidence.

Required shape:

- object/schema version stay compatible with current Match Journal cockpit
  responses;
- `status = "ok"` for successful submit;
- `errors = []`;
- compact `service_result`;
- no full records;
- no `note_text`.

### Readback Response

Destination: browser UI and smoke evidence.

Required shape:

- object/schema version stay compatible with current Match Journal cockpit
  responses unless a narrow backward-compatible schema addition is documented;
- `status = "ok"` when the record is present;
- exact journal-owned ID is visible;
- `note_scope = "unattached"` is visible;
- smoke-marker presence is visible as a boolean or compact status;
- no full note text;
- no raw paths or private payloads.

## Invariants

- No parser IDs may be invented for this smoke.
- No analytics rows may be created for this smoke.
- No workbook, webhook, Apps Script, Sheets, output transport, OpenAI, AI,
  Line Tracer, coaching, production, or model-provider behavior may change.
- Browser writes must use the FastAPI local app facade under `/api/journal/...`.
- Browser code must not call direct `status_api.py` journal routes.
- Direct status API global CORS policy remains out of scope.
- Reads that prove persistence must not create the database when missing.
- Writes may create only app-owned Match Journal generated state under the
  selected disposable app-data root.
- No destructive UI controls may be added.
- No arbitrary SQL or generic database browsing may be added.
- No generated/private/local artifacts may be staged or committed.

## Error Behavior

Malformed submit payload:

- Return sanitized `validation_error` or `malformed_json`.
- Do not call the service.
- Do not create partial rows.

Unattached submit with context:

- Return sanitized `validation_error`.
- Do not write.

Missing service:

- Return sanitized `service_unavailable`.
- Preserve browser form input.

Readback missing database:

- Return sanitized `missing`, `not_found`, or equivalent compact status.
- Do not create database folders or files.

Readback missing note:

- Return sanitized `not_found`.

Unsupported readback query:

- Return sanitized validation error.
- Do not list records.

## Side Effects

Allowed side effects for Codex C:

- Add or update local app/UI code needed for the unattached smoke note path.
- Add or update focused tests.
- Add
  `docs/implementation_handoffs/match_journal_safe_context_browser_write_smoke_comparison.md`.
- During validation, create generated SQLite state only under a disposable
  app-data root.
- During frontend validation, create `frontend/dist` only transiently and remove
  it before final status.

Forbidden side effects:

- staging, committing, or pushing unless explicitly asked later;
- opening or merging a PR in Codex C unless explicitly asked later;
- writing actual app-data root;
- changing protected parser, analytics, workbook, webhook, App Script, Sheets,
  AI, or production surfaces;
- committing generated/private/local artifacts.

## Dependency Order For Codex C

1. Confirm branch and git status.
2. Compare current code to this contract.
3. Add focused backend readback support only if current code cannot prove
   reload persistence safely.
4. Add frontend unattached-smoke-note request typing and UI path.
5. Add frontend readback/reload proof behavior.
6. Add focused backend/frontend tests.
7. Run focused validation.
8. Run artifact and protected-surface scans.
9. Produce the implementation handoff.

## Compatibility

Codex C must preserve:

- current attached-context journal reads;
- current attached note/label/review/experiment/display-correction requests;
- compact successful write response behavior;
- safe failed/unavailable write behavior;
- no pilot-error browser facade route;
- no delete/reset/bulk route;
- loopback-only frontend API base URL rules;
- current Match Journal schema/migrations;
- setup/status symbolic path display.

## Unknowns

- The exact narrowest readback shape may need Codex C comparison against the
  current service/repository boundary.
- Current service code exposes bundle reads by match/game context, while
  repository code can get/list notes. Codex C should decide whether a small
  local-app adapter read method is enough or whether a service method is cleaner.
- The live-browser automation mechanism may choose browser UI assertions or
  browser-side fetch assertions after reload. Either is acceptable if the proof
  uses `/api/journal/...` and not direct Python internals.
- Actual-root readiness remains unverified and approval-gated.

## Suspected Gaps

- Frontend note types exclude `unattached`.
- Frontend disables all journal writes when no context exists.
- Current UI has no visible no-context unattached-note path.
- Current `GET /api/journal` rejects no-context readback.
- Current browser bundle summary is context-oriented and does not display an
  unattached saved-note confirmation after reload.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- parser event kind values;
- parser payload shapes;
- match identity;
- game identity;
- deduplication;
- analytics schema;
- analytics migrations;
- analytics ingest semantics;
- curated analytics views;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer;
- hidden-card inference;
- archetype inference;
- player-mistake labels;
- gameplay advice;
- direct status API global CORS policy;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, or
  environment values.

## Tests Required For Codex C

Backend tests:

- Unattached browser submit through `POST /api/journal/notes` succeeds without
  context.
- Unattached submit with any context is rejected.
- First explicit unattached write creates only
  `<app_data>\db\match_journal.sqlite3` under a temporary app-data root.
- No analytics SQLite database is created.
- The compact write response includes a safe `primary_record_id` and does not
  echo records or note text.
- Readback by exact journal-owned note ID succeeds after write.
- Readback returns only compact safe metadata and does not return full note
  text.
- Readback rejects missing ID, malformed ID, unsupported query fields, parser
  context, and list-all attempts.
- Readback against a missing database does not create app-data artifacts.
- Route inventory still has no pilot-error/delete/reset/bulk/raw SQL routes.
- Browser-facing journal routes keep loopback CORS and do not depend on direct
  status API writes.

Frontend tests:

- With no match/game context, context-bound Match Journal controls remain
  disabled or hidden.
- With no match/game context, an unattached smoke note control is available only
  for the smoke path.
- Submitting the no-context smoke note calls `/api/journal/notes` with
  `note_scope = "unattached"` and no `context`.
- Smoke text must begin with
  `MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW`.
- Successful submit stores or displays only compact safe metadata.
- Failed/unavailable submit preserves form input.
- After simulated reload/readback, the UI proves the same journal-owned ID is
  persisted through a new `/api/journal/...` read.
- Frontend code still does not call direct status API journal endpoints.
- No destructive, raw SQL, pilot-error, OpenAI, AI/coaching, Line Tracer,
  hidden-card, player-mistake, or best-line controls render.

Live or browser smoke evidence:

- Use disposable app-data root.
- Start the local app through the approved developer app path.
- Open the loopback frontend.
- Confirm setup/status and Match Journal cockpit render.
- Confirm no visible match/game context exists or note why context exists.
- Submit one unattached smoke note with the required prefix.
- Capture the returned journal-owned note ID.
- Refresh/reload the page.
- Verify the persisted note by the same journal-owned ID using browser-visible
  UI or browser-side `/api/journal/...` readback.
- Confirm generated files were limited to disposable-root artifacts and no repo
  artifacts were created or staged.
- Stop only processes started by the smoke.

## Validation Commands

Codex C should run, at minimum:

```powershell
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py tests\test_analytics_local_app_backend.py tests\test_analytics_dev_app_launcher.py
npm --prefix frontend test -- --run src/App.test.tsx
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m ruff check src tests
git diff --check
```

After any frontend build, remove generated `frontend/dist` and confirm it is
absent before handoff.

Path-scoped protected-surface scan:

```powershell
@'
docs/contracts/match_journal_safe_context_browser_write_smoke.md
docs/implementation_handoffs/match_journal_safe_context_browser_write_smoke_comparison.md
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/match_journal_cockpit.py
src/mythic_edge_parser/local_app/match_journal_runtime.py
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/src/api.ts
frontend/src/types.ts
tests/test_match_journal_cockpit_ui_backend.py
tests/test_analytics_local_app_backend.py
tests/test_analytics_dev_app_launcher.py
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Path-scoped secret/private-marker scan:

```powershell
@'
docs/contracts/match_journal_safe_context_browser_write_smoke.md
docs/implementation_handoffs/match_journal_safe_context_browser_write_smoke_comparison.md
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/match_journal_cockpit.py
src/mythic_edge_parser/local_app/match_journal_runtime.py
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/src/api.ts
frontend/src/types.ts
tests/test_match_journal_cockpit_ui_backend.py
tests/test_analytics_local_app_backend.py
tests/test_analytics_dev_app_launcher.py
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Generated artifact checks:

```powershell
Test-Path frontend\dist
Get-ChildItem -Path . -Recurse -File -Include *.sqlite,*.sqlite3,*.db,*.db-wal,*.db-shm,*.sqlite-wal,*.sqlite-shm,*.sqlite3-wal,*.sqlite3-shm -ErrorAction SilentlyContinue |
  Where-Object { $_.FullName -notmatch '\\.git\\' } |
  Select-Object FullName
```

Codex B validation for this contract:

```powershell
git diff --check
@'
docs/contracts/match_journal_safe_context_browser_write_smoke.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/match_journal_safe_context_browser_write_smoke.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

## Acceptance Criteria

This contract is accepted when:

- the safe context strategy is explicitly unattached note, not synthetic parser
  context;
- parser identity invention is forbidden;
- browser writes stay under `/api/journal/...`;
- the smoke text prefix is required;
- disposable-root-first behavior is mandatory;
- actual-root writes remain approval-gated;
- reload persistence is tied to a new read after refresh/reload, not just
  pre-reload state;
- generated/private artifact rules are explicit;
- backend and frontend scopes are narrow;
- protected surfaces and out-of-scope behavior are named;
- validation expectations are explicit;
- Codex C has a pasteable handoff prompt.

Issue #237 implementation is acceptable only if:

- no parser, analytics schema, workbook, webhook, Apps Script, Sheets,
  OpenAI/AI/coaching, Line Tracer, production, or direct status API CORS
  behavior changes;
- no fake parser match/game context is created;
- no actual-root write or inspection occurs without explicit approval;
- no generated/private/local artifacts are staged or committed;
- the browser write/persistence smoke either passes under disposable root or is
  marked blocked with a contract-consistent reason and routed back.

## Expected Codex C Implementation Scope

Codex C may change only:

- `src/mythic_edge_parser/local_app/backend.py`, if a narrow readback route is
  needed;
- `src/mythic_edge_parser/local_app/match_journal_cockpit.py`, for request
  validation/response shaping for the narrow readback;
- `src/mythic_edge_parser/local_app/match_journal_runtime.py`, for read-only
  access to exact unattached note summaries if needed;
- `frontend/src/api.ts`, for an unattached submit/readback API helper if
  needed;
- `frontend/src/types.ts`, for narrow unattached note/request/readback types;
- `frontend/src/App.tsx`, for no-context unattached smoke UI and reload
  readback behavior;
- focused backend/frontend tests;
- `docs/implementation_handoffs/match_journal_safe_context_browser_write_smoke_comparison.md`.

Codex C must not implement synthetic visible context seeding in #237.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #237:

https://github.com/Tahjali11/Mythic-Edge/issues/237

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Contract:
docs/contracts/match_journal_safe_context_browser_write_smoke.md

Goal:
Compare the current local app backend, Match Journal cockpit facade, frontend,
and focused tests against the contract. Implement only the narrow unattached
browser smoke path needed to submit and verify one clearly labeled unattached
Match Journal smoke note through `/api/journal/...` with a disposable app-data
root. Produce
docs/implementation_handoffs/match_journal_safe_context_browser_write_smoke_comparison.md.

Before editing:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what the browser write/persistence smoke is supposed to prove.
- State what current code already supports.
- State why the current path fails with blocked_no_safe_context.
- State the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/match_journal_safe_context_browser_write_smoke.md
- docs/contracts/match_journal_live_browser_real_app_data_readiness.md
- docs/implementation_handoffs/match_journal_live_browser_real_app_data_readiness_comparison.md
- docs/contract_test_reports/match_journal_live_browser_real_app_data_readiness.md
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/match_journal_cockpit.py
- src/mythic_edge_parser/local_app/match_journal_runtime.py
- src/mythic_edge_parser/local_app/paths.py
- src/mythic_edge_parser/local_app/setup_status.py
- src/mythic_edge_parser/app/match_journal_service.py
- src/mythic_edge_parser/app/match_journal_repository.py
- frontend/src/App.tsx
- frontend/src/App.test.tsx
- frontend/src/api.ts
- frontend/src/types.ts
- tests/test_match_journal_cockpit_ui_backend.py
- tests/test_analytics_local_app_backend.py
- tests/test_analytics_dev_app_launcher.py

Implement only if needed:
- no-context frontend unattached smoke note UI;
- `POST /api/journal/notes` request with note_scope="unattached" and no context;
- required smoke text prefix:
  MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW;
- narrow compact readback under `/api/journal/...` by exact journal-owned
  note ID if current code cannot prove refresh/reload persistence safely;
- focused backend/frontend tests;
- implementation handoff.

Do not:
- target main;
- stage, commit, push, open a PR, merge, close #237, or mark #202 complete unless explicitly asked;
- write to, inspect, clean, delete, move, rename, archive, copy, upload, or sanitize the actual app-data root without explicit user approval;
- invent parser_match_id, parser_game_id, journal_match_id, or journal_game_id for the smoke;
- implement synthetic visible context seed in #237;
- change parser behavior, parser state final reconciliation, parser event classes, parser event kind values, parser payload shapes, match/game identity, deduplication, analytics schema, migrations, ingest semantics, curated analytics views, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer, hidden-card inference, archetype inference, player-mistake labels, gameplay advice, or direct status API global CORS policy;
- add destructive UI controls, arbitrary SQL, generic database browsing, delete/reset/bulk/export/sync controls, pilot-error browser controls, or direct status API journal writes;
- create or commit generated SQLite files, WAL/SHM/journal files, frontend build output, raw logs, private JSONL artifacts, failed posts, workbook exports, secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, environment values, or local-only artifacts.

Validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py tests\test_analytics_local_app_backend.py tests\test_analytics_dev_app_launcher.py
npm --prefix frontend test -- --run src/App.test.tsx
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m ruff check src tests
git diff --check

Run path-scoped protected-surface and secret/private-marker scans over changed
files. Remove frontend/dist after build and confirm no generated DB files are
inside the repo.

If feasible, run a disposable-root live-browser smoke:
- launch local app through the approved developer path with a temp app-data root;
- open loopback frontend;
- submit one unattached smoke note through the browser UI;
- capture the journal-owned note ID;
- refresh/reload;
- verify persistence via browser-visible UI or browser-side `/api/journal/...`
  readback;
- stop only processes started by the smoke.

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- files changed
- exact function/test sections changed
- safe context strategy implemented
- disposable-root smoke status
- actual-root approval state
- generated/private artifact status
- protected-surface status
- secret/private-marker status
- validation run
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/237"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #237"
  target_artifact: "docs/implementation_handoffs/match_journal_safe_context_browser_write_smoke_comparison.md"
  contract_artifact: "docs/contracts/match_journal_safe_context_browser_write_smoke.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch --untracked-files=all"
    - "git diff --check"
    - "path-scoped protected-surface scan for docs/contracts/match_journal_safe_context_browser_write_smoke.md"
    - "path-scoped secret/private-marker scan for docs/contracts/match_journal_safe_context_browser_write_smoke.md"
  stop_conditions:
    - "Do not target main."
    - "Do not implement synthetic visible parser context seeding for issue #237."
    - "Do not write to or inspect actual app-data root without explicit user approval."
    - "Do not invent parser match/game identity."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not add destructive UI controls, arbitrary SQL, generic database browsing, or direct status API journal writes."
    - "Do not create or commit generated/private/local artifacts or secrets."
```
