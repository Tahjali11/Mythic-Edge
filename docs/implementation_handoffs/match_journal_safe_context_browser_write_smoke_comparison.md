# Match Journal Safe Context Browser Write Smoke Implementation Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/237>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/202>

## Contract

`docs/contracts/match_journal_safe_context_browser_write_smoke.md`

## Internal Project Area

Local App / UI, with Match Journal local persistence and Quality / Governance
as supporting areas.

## Truth Owner

Parser/state remains truth owner for parser facts. Match Journal owns local
human annotation rows only. The unattached smoke note and browser readback are
validation evidence, not parser truth, analytics truth, workbook truth,
deployment truth, or AI/coaching truth.

## Bridge-Code Status

`stable_bridge`: browser UI -> FastAPI local app facade -> app-owned Match
Journal service/repository -> disposable-root smoke evidence.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Current Behavior Compared To Contract

The current repo already supported the safe backend write primitive:

- `POST /api/journal/notes` accepted `note_scope = "unattached"` without a
  `context` object.
- Unattached writes rejected any supplied context.
- Successful write responses summarized the service result without echoing
  `note_text` or raw record bodies.
- First explicit journal write created only the app-owned Match Journal SQLite
  database under the selected local app-data root.

The remaining contract gaps were:

- no exact-ID compact readback route for an unattached note;
- frontend note typing treated notes as context-bound only;
- no no-context browser UI path for the contract-authorized unattached smoke
  note;
- no reload/readback proof that carried only the journal-owned note ID.

The previous #236 live-browser smoke failed at `blocked_no_safe_context` because
the disposable root had no match/game history context, and #237 explicitly
forbids inventing parser or journal match/game identity.

## Implementation Option Chosen

Implemented the contract's safe unattached-note strategy:

- add compact read-only `GET /api/journal/notes` readback by exact
  `journal_note_id` plus `note_scope = "unattached"`;
- keep readback unattached-only and reject unsupported fields, parser-context
  fields, missing IDs, repeated query params, malformed IDs, and non-unattached
  scopes;
- reduce readback output to safe metadata only, including
  `smoke_marker_present` and derived `attachment_status = "unattached"`;
- split frontend attached-note request typing from unattached smoke-note typing;
- add a no-context-only "Save Unattached Smoke Note" browser control;
- generate the required smoke prefix internally and send no `context`;
- store only the returned journal note ID in session storage;
- reload/read back by exact ID and show only compact metadata.

## Files Changed

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/match_journal_cockpit.py`
- `src/mythic_edge_parser/local_app/match_journal_runtime.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `tests/test_match_journal_cockpit_ui_backend.py`
- `docs/implementation_handoffs/match_journal_safe_context_browser_write_smoke_comparison.md`

Untracked source contract left in place:

- `docs/contracts/match_journal_safe_context_browser_write_smoke.md`

## Exact Sections Changed

- `backend.py`
  - Added `GET /api/journal/notes` route wired to the cockpit readback facade.
- `match_journal_cockpit.py`
  - Added `UNATTACHED_SMOKE_NOTE_PREFIX`.
  - Added exact-ID readback query validation.
  - Added `match_journal_note_readback_response(...)`.
  - Added `_journal_note_id(...)` safety validation.
- `match_journal_runtime.py`
  - Added `LocalAppMatchJournalService.get_unattached_note_summary(...)`.
  - Added `_is_unattached_note(...)`.
- `types.ts`
  - Added attached-note, unattached-note, and unattached-note-readback request
    types.
- `api.ts`
  - Added `fetchMatchJournalUnattachedNote(...)`.
- `App.tsx`
  - Added unattached smoke note state, submit handler, readback handler,
    session-storage ID persistence, readback notice, and no-context-only smoke
    button.
  - Kept existing context-bound note/label/flag/correction controls disabled
    when parser context is absent.
- `App.test.tsx`
  - Added no-context unattached smoke submit and reload test.
  - Cleared session storage between tests.
- `test_match_journal_cockpit_ui_backend.py`
  - Added route inventory coverage for `GET /api/journal/notes`.
  - Added exact-ID readback success coverage.
  - Added malformed/list/context query rejection coverage.
  - Added missing-database no-artifact coverage.

## Code Changed

Runtime code changed only inside the contracted local app/browser Match Journal
surface. No parser behavior, parser state final reconciliation, parser event
classes, match/game identity, deduplication, analytics schema/migrations,
workbook schema, webhook payload shape, Apps Script, Sheets, OpenAI/model
provider, AI/coaching, Line Tracer, or production behavior changed.

## Interface Changes

New browser-facing route:

```text
GET /api/journal/notes?journal_note_id=<journal_note_id>&note_scope=unattached
```

Readback rules:

- requires one exact `journal_note_id`;
- requires exactly `note_scope = "unattached"`;
- rejects unsupported fields, parser/journal match/game context fields,
  repeated query params, and malformed IDs;
- does not list notes;
- does not create app-data root or SQLite files when the database is missing;
- returns compact metadata only:
  `journal_note_id`, `note_scope`, `author_label`, `source_surface`,
  `privacy_label`, `created_at`, `updated_at`, `smoke_marker_present`,
  `attachment_status`.

Frontend request typing now distinguishes context-bound attached notes from the
contract-authorized no-context unattached smoke note.

## Tests Added Or Updated

- Backend:
  - exact-ID readback succeeds after an unattached smoke write;
  - readback response excludes `note_text` and the smoke marker string;
  - missing DB readback returns `missing` without creating app-data artifacts;
  - list/context/repeated/malformed readback queries reject before service
    calls.
- Frontend:
  - no-context UI keeps context-bound journal controls disabled;
  - no-context smoke submit sends `note_scope = "unattached"` with no
    `context`;
  - smoke note text starts with
    `MYTHIC_EDGE_SMOKE_TEST_DO_NOT_USE_AS_GAME_REVIEW`;
  - only the returned journal note ID is used for reload readback;
  - readback UI does not display the smoke marker text or raw path-like values.

## Safe Context Strategy Implemented

The strategy is explicitly `unattached` Match Journal note. It does not seed or
invent parser-visible context, `parser_match_id`, `parser_game_id`,
`journal_match_id`, or `journal_game_id`.

## Disposable-Root Smoke Status

Disposable-root browser smoke passed.

- Launcher check mode passed with the disposable root absent afterward.
- Start mode used a temp app-data root and loopback ports `18766` and `15174`.
- Backend `/api/health` returned `200`.
- Frontend returned `200`.
- Browser UI rendered `Match Journal Cockpit`.
- Browser UI exposed `Save Unattached Smoke Note` while context-bound journal
  controls remained disabled.
- Browser submit created one unattached note with journal-owned ID
  `journal_note:4c287f2d57014b309e382d6878167be8`.
- Browser readback displayed compact metadata for the note.
- After reload, the same journal-owned ID remained visible.
- The smoke marker string was not displayed.
- Raw paths, webhook/API markers, destructive controls, OpenAI/coaching,
  Line Tracer, hidden-card, and player-mistake controls were not visible in the
  smoke snapshots.
- The disposable DB had one `journal_notes` row with `note_scope =
  "unattached"`.
- Only smoke processes on ports `18766` and `15174` were stopped.
- No listen sockets remained on those ports after shutdown.

The in-app browser automation backend was unavailable, so the live browser
smoke used the connected Chrome browser automation backend against the same
loopback disposable app.

## Actual-Root Approval State

Actual-root write/read/inspection was not requested, not approved, and not run.

## Generated/Private Artifact Status

- The disposable smoke root was under `%TEMP%`, not inside the repo.
- The smoke created one app-owned generated SQLite file under the disposable
  root: `db/match_journal.sqlite3`.
- No analytics SQLite database was created by backend readback tests.
- Frontend build output `frontend/dist` was created during validation and
  removed afterward.
- No raw logs, private JSONL artifacts, failed posts, workbook exports,
  secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, or
  local-only repo artifacts were created or committed.

## Contracted Area Status

Implementation stayed inside Local App / UI and local Match Journal support.
The browser facade remains under `/api/journal/...`; no direct status API
browser write route, arbitrary SQL surface, generic database browser, delete,
reset, export, sync, or pilot-error UI control was added.

## Validation Run

```text
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_dev_app_launcher.py
npm --prefix frontend test -- --run src/App.test.tsx
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m ruff check src tests
git diff --check
```

Final results:

- `git status --short --branch --untracked-files=all` showed only the expected
  #237 modified files plus untracked contract and handoff.
- `py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
  tests\test_analytics_local_app_backend.py
  tests\test_analytics_dev_app_launcher.py` passed, 37 tests, with one
  existing FastAPI/Starlette deprecation warning.
- `npm --prefix frontend test -- --run src/App.test.tsx` passed, 34 tests.
- `npm --prefix frontend run typecheck` passed.
- `npm --prefix frontend run build` passed; `frontend/dist` removed afterward.
- `py -m ruff check src tests` passed.
- `git diff --check` passed.
- `py tools\check_agent_docs.py` passed.
- Path-scoped protected-surface scan over the 10 changed/untracked #237 paths
  passed with forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over the same 10 paths passed with
  forbidden 0, warnings 0.
- `py tools\check_secret_patterns.py --all` was also run in advisory mode and
  failed on pre-existing repo-wide findings outside this slice; it did not
  identify a #237 path-scoped regression.
- Generated-artifact sweep found no `frontend/dist` and no repo-local
  SQLite/WAL/SHM/DB files.

## Still Unverified

- Actual app-data root write/read smoke remains unverified and approval-gated.
- In-app browser automation backend was unavailable; Chrome browser automation
  was used for the live browser smoke.
- Production behavior, live workbook state, deployed Apps Script state, Sheets
  state, and AI/coaching behavior were not exercised.

## Reviewer Focus

Ask Codex E to pay special attention to:

- whether `GET /api/journal/notes` is narrow enough and cannot become a note
  listing or parser-context workaround;
- whether the frontend stores only the journal note ID and never the note text;
- whether no-context UI exposes only the unattached smoke write path;
- whether readback output stays compact and omits raw note text, raw paths, and
  parser/journal match/game identity.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #237.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/237

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Contract:
docs/contracts/match_journal_safe_context_browser_write_smoke.md

Implementation handoff:
docs/implementation_handoffs/match_journal_safe_context_browser_write_smoke_comparison.md

Goal:
Review the Codex C implementation against the contract. Lead with findings
ordered by severity. Confirm whether the safe context strategy is explicitly an
unattached Match Journal smoke note, whether browser write/readback uses
`/api/journal/...` without parser context, whether reload proof stores only the
journal-owned note ID, and whether protected surfaces remain untouched.

Review:
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/match_journal_cockpit.py
- src/mythic_edge_parser/local_app/match_journal_runtime.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/App.tsx
- frontend/src/App.test.tsx
- tests/test_match_journal_cockpit_ui_backend.py
- docs/implementation_handoffs/match_journal_safe_context_browser_write_smoke_comparison.md

Pay special attention to:
- GET /api/journal/notes exact-ID readback being unattached-only and not a
  listing or parser-context workaround.
- Unsupported parser-context fields, repeated query params, missing IDs,
  malformed IDs, and non-unattached scopes being rejected.
- Missing DB readback not creating app-data artifacts.
- Frontend no-context UI exposing only the unattached smoke note write path.
- Frontend not storing note text, raw paths, raw hashes, or parser/journal
  match/game identity in browser storage.
- Readback UI showing only safe compact metadata.
- No destructive UI actions, arbitrary SQL, generic database browsing, direct
  status API writes, pilot-error controls, OpenAI/coaching, Line Tracer,
  hidden-card inference, archetype truth, player-mistake truth, or gameplay
  advice being introduced.

Do not:
- implement fixes unless routing as Codex D is explicitly requested;
- stage, commit, push, open a PR, merge, close #237, or mark tracker #202
  complete unless explicitly asked;
- write to or inspect actual app-data root without explicit user approval;
- target main;
- change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/
  OpenAI/AI/coaching/production behavior.

Validation to run or verify:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py tests\test_analytics_local_app_backend.py tests\test_analytics_dev_app_launcher.py
npm --prefix frontend test -- --run src/App.test.tsx
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m ruff check src tests
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
py tools\check_secret_patterns.py --all

After frontend build, remove frontend/dist and confirm no generated DB files,
WAL/SHM files, frontend build output, raw logs, private JSONL artifacts, failed
posts, workbook exports, secrets, credentials, tokens, API keys, webhook URLs,
spreadsheet IDs, or local-only artifacts are present in the repo.

Final output must include:
- findings first, ordered by severity
- contract verdict
- validation run and result
- protected-surface status
- secret/private-marker status
- generated artifact status
- whether forbidden scope was touched
- whether issue #237 is ready for Codex F or needs Codex D
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/237"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/match_journal_safe_context_browser_write_smoke.md"
  target_artifact: "docs/implementation_handoffs/match_journal_safe_context_browser_write_smoke_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch --untracked-files=all -> expected #237 modified/untracked files only"
    - "py -m pytest -q tests\\test_match_journal_cockpit_ui_backend.py tests\\test_analytics_local_app_backend.py tests\\test_analytics_dev_app_launcher.py -> passed, 37 tests, one existing FastAPI/Starlette warning"
    - "npm --prefix frontend test -- --run src/App.test.tsx -> passed, 34 tests"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "py -m ruff check src tests -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated-artifact sweep -> no frontend/dist and no repo-local SQLite/WAL/SHM/DB files"
    - "disposable-root browser smoke passed using Chrome browser automation"
  stop_conditions:
    - "Do not target main."
    - "Do not implement synthetic visible parser context seeding for issue #237."
    - "Do not write to or inspect actual app-data root without explicit user approval."
    - "Do not invent parser match/game identity."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not add destructive UI controls, arbitrary SQL, generic database browsing, or direct status API journal writes."
    - "Do not create or commit generated/private/local artifacts or secrets."
```
