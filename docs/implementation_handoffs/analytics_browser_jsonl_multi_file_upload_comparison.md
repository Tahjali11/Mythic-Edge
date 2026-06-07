# Analytics Browser JSONL Multi-File Upload Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Issue And Contract

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/214
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Contract: `docs/contracts/analytics_browser_jsonl_multi_file_upload.md`
- Branch: `codex/analytics-foundation`
- Risk tier: High

## Branch And Worktree Status

Confirmed branch: `codex/analytics-foundation`.

Initial unrelated/untracked worktree items observed and preserved:

- untracked source contract `docs/contracts/analytics_browser_jsonl_multi_file_upload.md`

Post-implementation worktree contains only the scoped #214 contract, backend,
adapter, frontend, tests, dependency metadata, and this handoff.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_browser_jsonl_multi_file_upload.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`

## Current Behavior Compared To Contract

### Contract Matches Already Present

- Existing path-based manual import route was already `POST /api/imports/jsonl`.
- Existing `source_path` single-file and issue #213 `source_paths` batch import behavior was present and preserved.
- Existing manual import job responses already used sanitized `ManualImportJob` status data.
- Existing issue #212 import-quality object and issue #213 source-artifact summaries were present.
- Existing frontend displayed manual import job, quality, and source-file summaries without retaining submitted raw path text.
- Existing analytics ingest wrote parser-normalized facts to local SQLite without changing parser truth ownership.

### Contract Gaps Found

- No multipart browser upload route existed.
- No backend helper accepted browser-uploaded file bytes.
- No adapter helper accepted in-memory uploaded JSONL sources.
- No upload source mode existed.
- No upload validation covered file count, per-file size, total size, blank file names, zero-byte files, or upload-specific safe labels.
- No focused tests proved uploaded raw JSONL bytes were not retained in app-data after success, degradation, failure, or rejection.
- No frontend `FormData` API helper or multi-file input existed.

## Implementation Option Chosen

Implemented the smallest scoped browser-upload path authorized by the contract:

- Keep existing `POST /api/imports/jsonl` JSON route and path-based behavior unchanged.
- Add separate `POST /api/imports/jsonl/upload` multipart route.
- Process uploaded JSONL bytes in memory instead of temporary raw files.
- Add a public in-memory adapter helper for uploaded sources.
- Reuse the existing manual import job schema, issue #212 quality object, issue #213 source-artifact vocabulary, and analytics ingest path.
- Add focused synthetic tests only; no private JSONL artifacts were copied, sanitized, fixtured, or committed.

## Files Changed

- `pyproject.toml`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `tests/test_analytics_browser_jsonl_upload.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_comparison.md`

## Exact Sections Changed

### Dependency Metadata

- Added `python-multipart>=0.0.9,<1` to existing `app` and `dev` optional dependency groups because FastAPI multipart form parsing requires it.

### Adapter

- Added `BROWSER_JSONL_UPLOAD_SOURCE_MODE = "uploaded_file_batch"`.
- Added `LegacyJsonlUploadSource`.
- Added `adapt_legacy_jsonl_upload_batch(...)`.
- Refactored selected JSONL replay into a shared input helper that supports path-backed and in-memory uploaded sources.
- Preserved one parser-state replay scope and one raw-hash dedupe set across the uploaded batch.
- Added deterministic uploaded-file ordering by safe display name, size, internal content digest, and original index.
- Kept internal content digest private; it is not returned, logged, stored, or displayed.
- Added safe uploaded source labels and per-file source-artifact summaries.

### Backend

- Added `BrowserJsonlUploadFile`.
- Added upload limits:
  - `MAX_BROWSER_JSONL_UPLOAD_FILES = 100`
  - `MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES = 25 * 1024 * 1024`
  - `MAX_BROWSER_JSONL_UPLOAD_TOTAL_BYTES = 250 * 1024 * 1024`
- Added `run_browser_jsonl_upload_import(...)`.
- Added upload validation for no files, too many files, blank names, non-JSONL extension, zero-byte files, per-file size, total size, and unsafe source labels.
- Added adapter dispatch for `uploaded_file_batch`.
- Added `POST /api/imports/jsonl/upload` and closed FastAPI upload objects after reading.
- Did not add `DELETE`, reset, wipe, retry, cancellation, parser runner, watcher, Sheets, AI, or production routes.

### Frontend

- Added `ManualImportUploadRequest`.
- Added `submitManualJsonlUpload(...)` using `FormData` and `POST /api/imports/jsonl/upload`.
- Added multi-file browser input with `multiple` and `accept=".jsonl"`.
- Added separate upload submit action from path-based import.
- Added safe transient selected-file summary.
- Cleared selected files and source label after terminal upload result or upload API error.
- Reused existing sanitized manual import job, quality, and per-file summary display.
- Added upload UI CSS only for upload form separation and selected-file summary layout.

### Tests

- Added backend upload tests for success, deterministic ordering, idempotent re-upload, cross-file duplicate hash counting, invalid upload rejection, size/count limits, malformed JSONL failure, no raw JSONL retention, and no destructive routes.
- Added adapter upload tests for deterministic in-memory source ordering, cross-file duplicate raw-hash counting, safe source summaries, and malformed JSONL privacy boundaries.
- Added frontend API test for multipart `FormData` submission without explicit `Content-Type`.
- Added frontend UI tests for browser file selection, upload submission, safe display, result rendering, selected-file cleanup, API error cleanup, and absence of destructive controls.
- Preserved existing path-based manual import and legacy adapter regression tests.

## Code/Test/Docs Status

- Code changed: yes, scoped to local analytics adapter/backend/frontend upload support.
- Tests changed: yes, focused synthetic tests only.
- Frontend changed: yes, local Manual Import UI/API only.
- Docs changed: yes, this implementation handoff.
- SQLite schema changed: no.
- SQLite database files created or committed: no repo-tracked DB files; tests used temp app-data only.

## Upload Cleanup And Privacy Notes

- Uploaded bytes are processed in memory through `LegacyJsonlUploadSource`; no request-scoped raw JSONL temp files are written by the implementation.
- Backend validation rejects invalid uploads before app-data or SQLite creation where feasible.
- FastAPI `UploadFile` objects are closed in a `finally` block after bytes are read.
- Source summaries use sanitized display labels and safe artifact labels only.
- Responses do not include raw uploaded payloads, raw paths, raw hashes, internal content digests, or temp paths.
- Frontend file objects are kept only in component state long enough to submit and are cleared after terminal success or API error.

## Job Response Shape

Upload jobs reuse the existing `ManualImportJob` object and include:

- `source.source_mode = "uploaded_file_batch"`
- `source.source_display_label`, such as `2 uploaded JSONL files`
- `source.path_echoed = false`
- selected/accepted/rejected file counts
- safe source group label
- safe `source_artifacts`
- `adapter.source_mode = "uploaded_file_batch"`
- issue #212 `adapter.quality`
- issue #213 per-file source-artifact summaries

## Protected And Forbidden Scope Confirmation

No intentional changes were made to:

- parser behavior
- saved-event replay semantics
- parser state final reconciliation
- parser event classes
- event kind values
- match/game identity
- parser-owned deduplication semantics
- analytics SQLite schema or migrations
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets behavior
- Match Journal behavior
- OpenAI/model-provider behavior
- AI/coaching behavior
- Line Tracer behavior
- production or deployment behavior

No private local JSONL artifact was copied, sanitized, fixtured, committed, or raw-dumped.

No raw Player.log payloads or raw saved-event lines are stored in SQLite or exposed in durable job/source summaries.

No destructive import, database, job, launcher, or UI action was added.

## Validation Run

- `git status --short --branch` -> confirmed `codex/analytics-foundation`; scoped modified/untracked files only.
- `py -m pytest -q tests\test_analytics_browser_jsonl_upload.py tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_manual_jsonl_import.py` -> passed, 39 tests, 1 existing FastAPI/Starlette deprecation warning.
- `py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py` -> passed, 35 tests, 1 existing FastAPI/Starlette deprecation warning.
- `npm --prefix frontend ci` -> passed, 0 vulnerabilities.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> passed, 3 files, 27 tests.
- `npm --prefix frontend run build` -> passed.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- Path-scoped protected-surface scan over contract, handoff, backend/import/adapter/frontend/test files, and `pyproject.toml` -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over contract, handoff, backend/import/adapter/frontend/test files, and `pyproject.toml` -> passed, forbidden 0, warnings 0.
- `py tools\check_secret_patterns.py --all` -> failed on pre-existing all-repo advisory findings outside the #214 touched-file scope; the relevant #214 path-scoped secret/private-marker scan passed as listed above.

## Generated Artifact Status

- `npm --prefix frontend run build` produced ignored frontend build output only.
- `npm --prefix frontend ci` produced ignored `frontend/node_modules/` only.
- No generated SQLite database, WAL, SHM, or journal file is changed or untracked in the repo.
- No raw JSONL artifact, raw Player.log, runtime status file, failed-post payload, workbook export, screenshot, or local-only artifact is changed or untracked.

## Remaining Risks Or Unverified Layers

- Live/manual operator import against real private local JSONL artifacts was not run.
- Browser behavior was validated by automated frontend tests and build, not by a manual browser session.
- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Production behavior was not exercised.
- All-repo secret scan still reports pre-existing advisory findings outside this module; the relevant #214 scope should be judged by path-scoped scans.

## Reviewer Focus

Codex E should verify:

- `POST /api/imports/jsonl/upload` preserves existing path-based import behavior.
- Uploaded raw JSONL bytes are never retained after terminal success, degradation, failure, or rejection.
- Internal content digests and saved-event raw hashes are not exposed.
- The frontend does not expose raw paths, fake paths, raw payloads, raw hashes, temp paths, stack traces, or destructive controls.
- The new `python-multipart` optional dependency is appropriate for `app` and `dev`.
- Existing issue #212 quality reporting and issue #213 explicit `source_paths` batch behavior remain intact.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #214.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/214

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_browser_jsonl_multi_file_upload.md

Implementation handoff:
docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_comparison.md

Risk tier:
High

Task:
Review the implementation against the browser JSONL multi-file upload contract. Lead with findings ordered by severity. Verify that the upload route, adapter helper, import job orchestration, frontend UI/API, tests, dependency change, and handoff satisfy the contract without expanding scope.

Review focus:
- Existing POST /api/imports/jsonl single-file and source_paths behavior remains compatible.
- POST /api/imports/jsonl/upload accepts multipart uploaded JSONL files and uses source_mode uploaded_file_batch.
- Upload validation covers file count, per-file size, total size, blank names, non-.jsonl names, zero-byte files, and unsafe labels.
- Uploaded files replay in one parser-state scope with deterministic ordering and cross-file raw-hash dedupe.
- Uploaded raw JSONL bytes are not retained after success, degradation, failure, or rejection.
- Responses and UI do not expose raw payloads, raw paths, raw hashes, internal content digests, temporary paths, stack traces, secrets, webhook URLs, API keys, or private local artifacts.
- Issue #212 import-quality reporting and issue #213 source-artifact summaries are preserved.
- No destructive import/database/job/launcher/UI routes or controls were added.
- No parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior changed.

Validation to run:
git status --short --branch
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_legacy_jsonl_artifact_adapter.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check

Also run path-scoped protected-surface and secret/private-marker scans over the contract, implementation handoff, pyproject.toml, touched backend/import/adapter/frontend/test files, and report generated artifact status.

Do not:
- Change implementation unless routing to Codex D with concrete findings.
- Target main.
- Stage, commit, push, open a PR, merge, close issue #214, or mark tracker #204 complete unless explicitly asked.
- Retain uploaded raw JSONL files.
- Expose raw payloads, paths, hashes, internal digests, temp paths, stack traces, secrets, or private artifacts.
- Change parser behavior, saved-event replay semantics, parser state final reconciliation, analytics schema/migrations, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, Match Journal, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, production behavior, or destructive controls.

Final review report must include:
- role performed
- issue/tracker/umbrella
- contract and implementation handoff reviewed
- files reviewed
- findings ordered by severity
- validation run and result
- protected-surface status
- secret/private-marker status
- generated artifact status
- whether forbidden scope was touched
- recommendation: route to D for fixes, F for submitter, B/A for contract/problem changes, or no-op if accepted
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/214"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/analytics_browser_jsonl_multi_file_upload.md"
  target_artifact: "docs/contract_test_reports/analytics_browser_jsonl_multi_file_upload.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_analytics_browser_jsonl_upload.py tests\\test_analytics_legacy_jsonl_artifact_adapter.py tests\\test_analytics_manual_jsonl_import.py -> passed"
    - "py -m pytest -q tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_local_app_backend.py -> passed"
    - "npm --prefix frontend ci -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> passed"
    - "npm --prefix frontend run build -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "py tools\\check_secret_patterns.py --all -> failed on pre-existing all-repo findings outside #214 scope"
  stop_conditions:
    - "Do not target main."
    - "Do not retain uploaded raw JSONL files after import."
    - "Do not expose raw payloads, raw paths, raw hashes, internal content digests, temporary paths, stack traces, secrets, webhook URLs, API keys, or private local artifacts."
    - "Do not add destructive import, database, job, launcher, or UI actions."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not stage, commit, push, open a PR, merge, close issue #214, or mark tracker #204 complete unless explicitly asked."
```
