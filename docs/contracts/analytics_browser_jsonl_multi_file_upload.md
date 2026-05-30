# Analytics Browser JSONL Multi-File Upload Contract

## Module

Browser-based multi-file legacy JSONL upload for the local developer app.

Plain English: this contract lets the local app accept several user-selected
`.jsonl` files from a browser file picker, send their contents to the
loopback backend, replay them through the existing legacy JSONL adapter and
analytics ingest path, then return the same sanitized manual import job shape.
It is an access and transport surface only. It does not make the browser,
backend upload route, SQLite, or frontend the owner of parser truth.

This is a contract-writing pass only. It does not implement code.

## Source Issue

- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/214>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Related manual import issue: <https://github.com/Tahjali11/Mythic-Edge/issues/211>
- Related quality issue: <https://github.com/Tahjali11/Mythic-Edge/issues/212>
- Related batch import issue: <https://github.com/Tahjali11/Mythic-Edge/issues/213>

## Branch

Current intended branch:

```text
codex/analytics-foundation
```

Observed during this Codex B pass:

```text
ea4fffd Add dev app launcher shortcut cleanup
```

Local branch state observed:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
```

`HEAD...origin/codex/analytics-foundation` was even (`0 0`) during this
contract pass. This contract does not stage, commit, push, open a PR, close
issues, or target `main`.

## Authority And Source Artifacts Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- tracker #204
- umbrella issue #207
- source issue #214
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_manual_jsonl_import_ui_job_status.md`
- `docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md`
- `docs/contracts/analytics_legacy_jsonl_batch_import.md`
- `docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`
- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `tests/test_analytics_manual_jsonl_import.py`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- frontend focused tests under `frontend/src/`

## Risk Tier

High.

Reasons:

- browser upload moves raw legacy JSONL bytes through the frontend/backend
  boundary;
- multipart parsing may require temporary backend buffers or files;
- uploaded file names can contain private, misleading, or unsafe text;
- the workflow can accidentally retain raw uploaded JSONL after import;
- the workflow can accidentally expose raw payloads, raw paths, raw hashes,
  stack traces, local temporary paths, or private artifact labels;
- the workflow can blur browser upload transport, parser replay, adapter
  quality reporting, and SQLite ingest identity;
- it is a state-changing local app route that can write parser-normalized facts
  into app-owned SQLite.

## Owning Layer

Primary owner: local analytics usability / manual historical import loop.

Truth boundaries:

- Parser/state owns MTGA event interpretation, match/game identity, final
  reconciliation, parser event classes, and parser-managed facts.
- The legacy JSONL adapter owns safe adaptation of supported saved-event JSONL
  records into parser-normalized replay input.
- `analytics_ingest.py` owns writing already-normalized parser facts into local
  SQLite.
- The local backend owns loopback-only upload validation, temporary staging
  cleanup, import orchestration, and sanitized job-status responses.
- The frontend owns file selection, upload submission, transient progress
  state, and safe display only.

The upload workflow may say "these uploaded legacy JSONL files were replayed
as one batch and produced these parser-normalized analytics rows." It must not
decide what happened in Arena by trusting browser state, uploaded file names,
legacy `derived` labels, raw payload text, SQLite joins, or frontend display.

## Contract Decision

Implement browser upload as a separate route and source mode.

Required first-slice behavior:

1. Preserve existing path-based single-file and explicit `source_paths` batch
   import on `POST /api/imports/jsonl`.
2. Add a new multipart upload route:

   ```text
   POST /api/imports/jsonl/upload
   ```

3. Accept one or more uploaded `.jsonl` files from a browser file input.
4. Treat uploaded files as raw transient transport only.
5. Do not store raw uploaded JSONL in SQLite.
6. Do not copy uploaded JSONL into the repo.
7. Do not retain uploaded raw JSONL files after the job succeeds, degrades,
   fails, or is rejected.
8. Replay accepted files in one parser-state replay scope.
9. Deduplicate nonblank saved-event `raw_bytes_hash` values across the uploaded
   batch without exposing hash values.
10. Return the existing sanitized `ManualImportJob` response shape where
    possible.
11. Reuse the #212 import-quality object and #213 source-artifact summary
    vocabulary.
12. Keep job storage process-local and in memory.

Recommended upload source mode:

```text
uploaded_file_batch
```

Drag-and-drop, folder picker or `webkitdirectory`, recursive folder upload,
persistent import history, copied import retention, cancellation, retries,
job deletion, database reset/delete/wipe, live Player.log watching, analytics
dashboards, Match Journal, Google Sheets sync, Line Tracer, OpenAI/model
runtime, and AI/coaching behavior remain out of scope.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_browser_jsonl_multi_file_upload.md`

Future Codex C implementation files authorized by this contract:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`, only for upload UI state and safe summary display
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`
- `tests/test_analytics_browser_jsonl_upload.py`
- focused additions to `tests/test_analytics_manual_jsonl_import.py`
- focused additions to `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_comparison.md`

Conditional dependency file:

- `pyproject.toml`, only to add a reviewed multipart parser dependency such as
  `python-multipart>=0.0.9,<1` to the existing `app` and `dev` optional
  dependency groups if FastAPI multipart form parsing requires it.

Referenced but not owned:

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/analytics_migrations/*.sql`
- generated SQLite database files
- raw local legacy JSONL artifacts

Codex C must route back to Codex B before changing parser behavior, saved-event
replay semantics, parser event classes, match/game identity, deduplication
semantics, analytics schema/migrations, raw artifact retention, persistent job
history, destructive actions, or frontend behavior outside manual import
selection/status display.

## Observed Current Behavior

Current backend behavior:

- `POST /api/imports/jsonl` accepts JSON requests with exactly one of
  `source_path` or `source_paths`.
- `source_path` imports one explicit local `.jsonl` file by path.
- `source_paths` imports several explicit local `.jsonl` file paths in one
  job.
- `GET /api/imports/jobs/{job_id}` returns a process-local sanitized job
  summary.
- The route validates paths before app-data/database creation.
- The route rejects URLs, UNC paths, directories, missing files, non-`.jsonl`
  files, duplicate paths, empty file lists, and too many paths.
- The route reads selected path-based files in place and does not copy them
  into app-data.
- No route accepts `multipart/form-data`.
- No upload route exists.

Current adapter behavior:

- `adapt_legacy_jsonl_artifacts(source, source_artifact_label=None)` supports a
  path-based file or directory input.
- `adapt_legacy_jsonl_file_batch(sources, source_artifact_label=None)` supports
  explicit path-based batch input.
- Batch replay processes selected files in deterministic path order.
- Batch replay uses one parser-state replay scope.
- Batch replay deduplicates nonblank saved-event `raw_bytes_hash` values across
  the selected batch.
- Adapter results include sanitized `quality`, `source_mode`,
  `files_selected`, `files_accepted`, `files_rejected`, and
  `source_artifacts`.
- No adapter interface accepts uploaded file objects, in-memory text streams,
  or temporary upload sources without durable paths.

Current frontend behavior:

- The Manual Import UI has a text input for one path and a textarea for
  explicit path-list batch import.
- The frontend submits JSON to `POST /api/imports/jsonl`.
- The frontend validates and displays the existing manual import job shape,
  including import quality and source-artifact summaries.
- The frontend clears raw entered paths after terminal result or error.
- No browser file input, upload API client, `FormData` request, or upload mode
  exists.

Observed gap:

- The local app cannot import multiple files selected through the browser file
  picker.
- The user still needs explicit local paths for day-folder archives.
- Browser file inputs cannot safely reveal absolute local paths, so upload must
  be a separate source surface.
- No tests prove raw uploaded JSONL cleanup after success and failure.

## Public Interface

### Backend Route

Required route:

```text
POST /api/imports/jsonl/upload
```

Content type:

```text
multipart/form-data
```

Required form fields:

- `files`: repeated file part, one or more uploaded `.jsonl` files.

Optional form fields:

- `source_artifact_label`: safe label using the existing adapter/manual import
  label policy.

Response:

- JSON `ManualImportJob` object using the existing
  `analytics_manual_jsonl_import_ui_job_status.v1` schema unless Codex C proves
  a local-app-only schema bump is necessary.

Forbidden upload route behavior:

- no `DELETE` route;
- no upload cancellation route;
- no import deletion route;
- no job deletion route;
- no database reset/wipe/clear/export route;
- no broad SQL route;
- no live watcher route;
- no parser runner process-control route;
- no Google Sheets, Match Journal, OpenAI, AI, production, or deployment route.

### Backend Module Surface

Recommended public constant:

```text
MAX_BROWSER_JSONL_UPLOAD_FILES = 100
MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES = 25 * 1024 * 1024
MAX_BROWSER_JSONL_UPLOAD_TOTAL_BYTES = 250 * 1024 * 1024
BROWSER_JSONL_UPLOAD_SOURCE_MODE = "uploaded_file_batch"
```

Codex C may choose smaller size limits if tests and the implementation handoff
explain the safety tradeoff. It must not choose larger limits without routing
back to Codex B.

Recommended backend function:

```python
run_browser_jsonl_upload_import(
    files: Sequence[object],
    *,
    source_artifact_label: str | None = None,
    app_data_root: Path | None = None,
    now: Callable[[], str] | None = None,
    job_id_factory: Callable[[], str] | None = None,
) -> dict[str, object]
```

Names may differ, but route handlers must stay small and the upload validation,
temporary staging, cleanup, adapter call, and job-summary construction must be
unit-testable outside the FastAPI decorator body.

### Adapter Surface

Preferred adapter helper:

```python
adapt_legacy_jsonl_upload_batch(
    sources: Sequence[LegacyJsonlUploadSource],
    *,
    source_artifact_label: str | None = None,
) -> LegacyJsonlAdapterResult
```

Recommended upload source shape:

```python
@dataclass(frozen=True, slots=True)
class LegacyJsonlUploadSource:
    display_name: str
    content_bytes: bytes
    size_bytes: int
    original_index: int
```

Equivalent stream-based or temporary-file-backed shapes are allowed if they
preserve this contract's privacy, cleanup, deterministic ordering, and replay
semantics.

If Codex C uses temporary files instead of an in-memory adapter helper, it must
use a request-scoped temporary staging directory and delete every uploaded raw
JSONL byte in a `finally` path after success, degraded success, failure, or
rejection. Tests must prove cleanup.

### Frontend Surface

The Manual Import UI may add:

- a browser file input:

  ```text
  type="file"
  multiple
  accept=".jsonl"
  ```

- an upload submit action separate from path-based import;
- upload progress/submitting state;
- safe uploaded file count display;
- sanitized selected file display names;
- upload result summary using the existing Manual Import job display;
- API/types for multipart upload.

The frontend must not:

- parse JSONL into facts;
- inspect or display raw JSONL line contents;
- store selected `File` objects in `localStorage`, `sessionStorage`, query
  strings, logs, screenshots, snapshots, or persistent app state;
- display browser fake paths such as `C:\fakepath\...`;
- display absolute local paths;
- display raw payloads, raw saved-event lines, raw hashes, stack traces,
  secrets, webhook URLs, workbook IDs, tokens, API keys, or private markers;
- expose destructive import, database, job, launcher, Git, Sheets, AI,
  production, or live-watcher controls.

## Upload Request Contract

`POST /api/imports/jsonl/upload` request fields:

```text
files=<uploaded JSONL file part>
files=<uploaded JSONL file part>
source_artifact_label=optional_safe_label
```

Required file validation:

- reject no files;
- reject more than `MAX_BROWSER_JSONL_UPLOAD_FILES`;
- reject zero-byte files;
- reject files larger than `MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES`;
- reject total request file bytes larger than
  `MAX_BROWSER_JSONL_UPLOAD_TOTAL_BYTES`;
- reject missing or blank file names;
- reject file names whose final extension is not `.jsonl`;
- reject non-file form fields in the `files` slot;
- treat browser MIME types as advisory only and never as proof of safety;
- validate every file before opening app-data folders or SQLite;
- fail the whole request when any selected file is invalid.

Allowed MIME types are advisory and may include:

- `application/jsonl`
- `application/x-ndjson`
- `application/json`
- `application/octet-stream`
- blank or browser-specific values

Extension validation remains required because browser MIME values vary and can
be spoofed.

Client-supplied file names are untrusted. They may be used only after
sanitization. They must not be treated as source paths.

## Upload Ordering

Uploaded files must be processed in deterministic internal order.

Required ordering:

1. assign each file an `original_index` from the multipart part order;
2. derive a safe display name from the client-supplied file name;
3. compute internal ordering metadata without exposing it;
4. sort by:

   ```text
   (safe display name casefolded, size_bytes, internal content digest, original_index)
   ```

5. use the sorted order for parser replay, raw-hash dedupe, source-artifact
   summaries, and tests.

The internal content digest is allowed only for ordering and cleanup-safe
dedupe support. It must never be returned, logged, stored in SQLite, stored in
job summaries, displayed in the UI, or written to app-data.

## Temporary Staging And Retention

Preferred implementation:

- process uploaded files in memory or through stream objects;
- do not create raw upload files on disk.

Allowed fallback:

- use an app-owned request-scoped temporary directory under:

  ```text
  %LOCALAPPDATA%\MythicEdgeDev\imports\tmp\
  ```

  or a test-injected temporary app-data root;
- write uploaded bytes there only long enough to reuse existing path-based
  adapter code;
- delete the request-scoped temporary directory in a `finally` path.

Required guarantees:

- no raw uploaded JSONL file remains after success, degraded success, adapter
  failure, ingest failure, validation rejection, or unexpected exception;
- no raw uploaded JSONL file is created inside the repo;
- no raw uploaded JSONL file is committed;
- no uploaded raw payload is stored in SQLite;
- no raw upload path or temporary path is exposed in API responses, UI, logs,
  tests, docs, screenshots, or diagnostics;
- FastAPI or Starlette upload/spool objects must be closed when the request
  ends.

Persistent raw import retention requires a later explicit contract. This
contract does not authorize it.

## Source And Adapter Summary Fields

The returned job `source` object must include:

- `source_kind = "saved_event_replay"`
- `source_mode = "uploaded_file_batch"`
- `source_artifact_label`
- `source_display_label`, such as `3 uploaded JSONL files`
- `source_file_extension = ".jsonl"`
- `path_echoed = false`
- `files_selected`
- `files_accepted`
- `files_rejected`
- `source_group_label`
- `source_artifacts`

The returned job `adapter` object must include:

- existing adapter status/count/warning fields;
- existing #212 `quality` object;
- `source_mode = "uploaded_file_batch"`
- `files_selected`
- `files_accepted`
- `files_rejected`
- safe `source_artifacts`.

Per-file source-artifact summaries must reuse the #213 safe shape where
possible:

```json
{
  "batch_index": 0,
  "source_artifact_label": "legacy_jsonl_uploaded_file:0",
  "source_display_label": "events_a.jsonl",
  "status": "processed",
  "records_seen": 10,
  "events_processed": 8,
  "events_skipped": 2,
  "processed_kind_counts": {"MatchState": 1},
  "unsupported_kind_counts": {},
  "skipped_reason_counts": {
    "blank_line": 0,
    "duplicate_raw_hash": 2,
    "unsupported_kind": 0
  },
  "adapter_warning_codes": []
}
```

Per-file summaries must not include:

- browser fake paths;
- absolute paths;
- raw file names when unsafe;
- temporary staging paths;
- raw JSONL lines;
- raw payloads;
- raw `raw_bytes_hash` values;
- internal content digests;
- SQL statements;
- stack traces;
- secrets, tokens, API keys, webhook URLs, workbook IDs, or private markers.

## Source Artifact Label Policy

If `source_artifact_label` is supplied, use the existing safe-label validation.

If no label is supplied, generate a safe deterministic label:

```text
legacy_jsonl_uploaded_batch:<file_count>:<opaque_suffix>
```

The opaque suffix may be derived from sanitized metadata such as safe display
labels, file sizes, count, and sorted order. It must not expose raw paths, raw
payloads, saved-event raw hashes, temporary file paths, or full content hashes.

## Replay, Dedupe, And Ingest Semantics

Upload import must preserve #213 batch semantics:

- validate all files first;
- replay all accepted uploaded files in one parser-state replay scope;
- seed parser replay exactly as the existing adapter does;
- process files in deterministic upload order;
- maintain one `seen_raw_hashes` set across the whole uploaded batch;
- skip duplicate nonblank saved-event `raw_bytes_hash` values after the first
  processed record;
- build one combined parser-normalized replay;
- call `ingest_parser_normalized_replay(...)` once for the combined replay;
- preserve existing SQLite replay/upsert idempotency;
- report duplicate raw-hash counts but never expose hash values.

Upload import must not:

- replay each uploaded file separately and concatenate rows if that would lose
  state continuity;
- dedupe per file only;
- change parser match/game identity;
- change parser-owned deduplication;
- change saved-event event class mapping;
- change analytics SQLite schema or migrations;
- reinterpret raw payloads in the backend or frontend.

## Error Behavior

Request validation failures:

- return a sanitized rejected `ManualImportJob` response when possible;
- do not create app-data folders;
- do not create or open SQLite;
- do not write temporary raw upload files if validation can fail before
  buffering;
- clean any framework or temporary buffers already created;
- do not expose file contents, raw names when unsafe, paths, hashes, or stack
  traces.

Required upload error categories to consider:

- `upload_files_required`
- `upload_files_too_many`
- `upload_file_empty`
- `upload_file_too_large`
- `upload_total_too_large`
- `upload_file_name_required`
- `upload_file_extension_not_allowed`
- `upload_file_invalid`
- `source_artifact_label_invalid`
- `upload_temp_staging_failed`
- `upload_temp_cleanup_failed`

The exact code set may differ, but tests must prove invalid upload requests
are rejected safely and cleanup is attempted.

Adapter failure:

- malformed selected files fail the whole uploaded batch safely;
- failed batches must not write partial SQLite facts;
- failed job summaries may include sanitized failure categories and file
  counts;
- failed job summaries must not include raw lines, raw payloads, raw paths, raw
  hashes, internal digests, stack traces, or SQL internals;
- temporary files must be cleaned after failure.

Degraded success:

- unsupported event kinds, duplicate saved-event raw hashes, blank lines,
  stale legacy-derived mismatch warnings, incomplete summary output gaps, and
  ingest warnings may produce a `degraded` status when parser-normalized rows
  are still ingested.

Cleanup failure:

- cleanup failure is high risk and must be visible as a sanitized warning or
  failure category;
- the response must still avoid exposing temp paths;
- Codex C must route to review if cleanup cannot be proven on Windows.

## Dependency Policy

If FastAPI multipart parsing requires `python-multipart`, Codex C may add only
this focused dependency to `pyproject.toml`:

```text
python-multipart>=0.0.9,<1
```

Allowed placement:

- `[project.optional-dependencies].app`
- `[project.optional-dependencies].dev`

No other runtime, frontend, parser, database, or upload dependency is
authorized by this contract. If implementation needs a different dependency,
route back to Codex B.

## Side Effects

Allowed future implementation side effects:

- add a loopback-only upload endpoint;
- add upload orchestration and cleanup code;
- add a stream or temporary-source adapter path;
- add frontend file input and upload API code;
- add synthetic backend/adapter/frontend tests;
- add the focused multipart dependency if needed;
- create app-data folders and app-owned SQLite database only after a valid
  upload has been accepted and adapter replay succeeds enough to ingest;
- write parser-normalized analytics facts to app-owned SQLite through existing
  ingest;
- write implementation handoff documentation.

Forbidden side effects:

- no implementation code in this Codex B pass;
- no retained raw uploaded JSONL files after import;
- no raw JSONL copied into the repo;
- no raw JSONL stored in SQLite;
- no persistent upload/import history;
- no raw Player.log storage;
- no generated database committed to the repo;
- no analytics SQLite schema or migration change;
- no parser behavior change;
- no parser state final reconciliation change;
- no parser event class or event kind change;
- no match/game identity or parser-owned deduplication change;
- no workbook schema, webhook payload, Apps Script, Google Sheets, Match
  Journal, OpenAI/model-provider, AI/coaching, Line Tracer, production, or
  deployment behavior change;
- no destructive import/database/job/launcher/UI actions.

## Compatibility

Codex C must preserve:

- existing `POST /api/imports/jsonl` single-file path import;
- existing `POST /api/imports/jsonl` explicit path-list batch import;
- existing `GET /api/imports/jobs/{job_id}` behavior;
- existing process-local job storage behavior;
- existing `ManualImportJob` schema unless a schema bump is explicitly
  justified and updated across backend/frontend tests;
- existing #212 `adapter.quality` shape;
- existing #213 source-artifact summary vocabulary;
- existing adapter path-based file and directory behavior;
- existing analytics ingest behavior and SQLite schema;
- existing generated artifact ignore protections.

## Unknowns And Open Questions

- Whether upload should use pure in-memory adapter sources or request-scoped
  temporary files in the first implementation.
- Whether 100 files and 250 MiB total is too large for some machines. Codex C
  may choose smaller limits, but not larger, without routing back.
- Whether browser-selected duplicate names with identical sizes should display
  generic labels or indexed duplicate labels.
- Whether future folder picker support should preserve safe relative folder
  labels. This contract defers folder picker support.
- Whether upload progress needs polling or streaming. This contract allows a
  synchronous first slice.
- Whether persistent sanitized upload/import history should later live in
  app-data. This contract forbids it.

## Suspected Gaps

- No multipart upload endpoint exists.
- `pyproject.toml` currently lists FastAPI and Uvicorn but not a multipart
  parser dependency.
- No backend helper accepts `UploadFile` objects or equivalent uploaded file
  streams.
- No adapter helper accepts in-memory uploaded sources.
- No tests prove temporary uploaded raw JSONL cleanup on success and failure.
- No frontend file input or upload API exists.
- No tests prove browser fake paths, raw payloads, raw hashes, or temporary
  staging paths are absent from upload responses.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- saved-event replay event mapping or latest-file directory selection;
- parser state final reconciliation;
- parser event classes;
- event kind values;
- match/game identity;
- parser-owned deduplication semantics;
- analytics SQLite schema or migration SQL;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- output transport;
- Google Sheets behavior;
- Match Journal behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- production behavior;
- deployment behavior;
- secrets, credentials, tokens, API keys, webhook URLs, OAuth state, or
  environment-variable contracts;
- raw Player.log files;
- private legacy JSONL artifacts;
- raw uploaded JSONL retention after import;
- raw payloads, raw saved-event lines, raw hashes, temporary paths, or raw
  paths in responses/logs/tests/docs;
- generated SQLite database/WAL/SHM/journal files inside the repo;
- runtime status files;
- failed-delivery payload artifacts;
- workbook exports;
- generated card/tier data;
- destructive import/database/job/launcher/UI actions.

## Out Of Scope

- Implementation code in this Codex B pass.
- Opening a PR or targeting `main`.
- Changing parser behavior.
- Changing saved-event replay semantics.
- Changing analytics SQLite schema/migrations.
- Adding, editing, sanitizing, fixture-izing, or committing real private JSONL
  artifacts.
- Storing raw uploaded JSONL or raw Player.log payloads in SQLite.
- Retaining uploaded raw JSONL after import.
- Drag-and-drop import.
- Folder picker or `webkitdirectory` import.
- Recursive folder import.
- Persistent import history.
- Import deletion, job deletion, retries, cancellation, queue management, or
  database reset/wipe/clear.
- Live Player.log watching or watcher process control.
- Curated analytics dashboard pages beyond the Manual Import result panel.
- Google Sheets sync, workbook export, webhook posting, Apps Script changes,
  Match Journal, Line Tracer, AI/OpenAI/coaching behavior, gameplay advice,
  hidden-card inference, archetype classification, or production deployment.

## Tests Required

Focused backend upload tests:

```powershell
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
```

Required backend coverage:

- two synthetic uploaded `.jsonl` files import as one uploaded batch;
- upload response uses `source_mode = "uploaded_file_batch"`;
- upload response reuses `ManualImportJob` and #212 quality fields;
- upload response includes safe per-file source-artifact summaries;
- uploaded files are replayed in deterministic order even when multipart order
  is shuffled;
- duplicate saved-event raw hashes across uploaded files are counted but not
  exposed;
- re-uploading the same synthetic batch into the same app-owned SQLite
  database is idempotent for fact rows;
- no files, too many files, zero-byte files, oversized file, oversized total,
  blank filename, non-`.jsonl` filename, and unsafe label are rejected safely;
- invalid upload requests reject before database creation where feasible;
- malformed uploaded JSONL fails without raw line, raw payload, raw hash,
  temporary path, or stack trace exposure;
- temporary uploaded raw JSONL files are cleaned after success, degraded
  success, adapter failure, ingest failure, and validation rejection;
- no raw uploaded JSONL file remains in repo or app-data after terminal result;
- no destructive routes or `DELETE` methods are added.

Focused adapter tests:

```powershell
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py
```

Required adapter coverage:

- uploaded/in-memory source helper, if added, preserves explicit batch replay
  semantics;
- uploaded source helper sorts deterministically;
- uploaded source helper preserves #212 quality fields and #213
  source-artifact summaries;
- uploaded source helper never exposes internal content digests, raw hashes,
  raw payloads, or temp paths;
- existing path-based single-file, path-based explicit batch, and directory
  latest-file selection behavior still pass.

Focused manual import regression tests:

```powershell
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
```

Required regression coverage:

- existing path-based single-file import still works;
- existing `source_paths` explicit batch import still works;
- existing process-local job status still works;
- existing path redaction remains intact.

Frontend validation:

```powershell
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
```

Required frontend coverage:

- file input supports multiple `.jsonl` files;
- upload API sends `FormData` to `POST /api/imports/jsonl/upload`;
- path-based JSON import API remains unchanged;
- upload UI clears selected files after terminal result or failure;
- upload UI displays safe file count, aggregate quality, and per-file
  summaries;
- upload UI handles rejected, failed, degraded, succeeded, backend-unavailable,
  malformed-response, and incompatible-response states;
- upload UI does not render fake paths, absolute paths, raw payloads, raw
  hashes, stack traces, or destructive controls.

Adjacent checks:

```powershell
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
git diff --check
py tools\check_secret_patterns.py --all
```

Path-scoped protected-surface check:

```powershell
@'
docs/contracts/analytics_browser_jsonl_multi_file_upload.md
docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_comparison.md
pyproject.toml
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/import_jobs.py
src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
tests/test_analytics_browser_jsonl_upload.py
tests/test_analytics_manual_jsonl_import.py
tests/test_analytics_legacy_jsonl_artifact_adapter.py
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/api.test.ts
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Path-scoped secret/private-marker check:

```powershell
@'
docs/contracts/analytics_browser_jsonl_multi_file_upload.md
docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_comparison.md
pyproject.toml
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/import_jobs.py
src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
tests/test_analytics_browser_jsonl_upload.py
tests/test_analytics_manual_jsonl_import.py
tests/test_analytics_legacy_jsonl_artifact_adapter.py
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/api.test.ts
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Generated artifact check:

- Codex C/E must report `git status --short --branch`.
- Codex C/E must confirm no raw JSONL artifacts, raw Player.log files,
  temporary uploaded JSONL files, generated SQLite DB/WAL/SHM/journal files
  inside the repo, runtime artifacts, failed-delivery artifacts, workbook
  exports, screenshots with private data, or `node_modules/` files are changed
  or untracked.

## Acceptance Criteria

Codex C satisfies this contract when:

- `POST /api/imports/jsonl/upload` exists and accepts multipart uploaded
  `.jsonl` files.
- Existing `POST /api/imports/jsonl` path and explicit path-list behavior is
  preserved.
- Upload request validation enforces file count, file size, total size,
  extension, nonempty files, and safe label rules.
- Upload import uses `source_mode = "uploaded_file_batch"`.
- Uploaded files are replayed in one parser-state scope with deterministic
  internal ordering.
- Duplicate saved-event raw hashes are deduped across the uploaded batch and
  counted without exposure.
- Upload import writes parser-normalized facts through existing analytics
  ingest only.
- Upload responses reuse the existing sanitized manual import job response,
  #212 quality object, and #213 source-artifact summary vocabulary.
- Uploaded raw JSONL bytes are not retained after terminal success,
  degradation, failure, or rejection.
- No raw payloads, raw paths, raw hashes, internal content digests, temporary
  paths, secrets, stack traces, generated private artifacts, or destructive
  controls are exposed.
- Synthetic backend, adapter, frontend, path-based regression, Ruff, diff,
  protected-surface, secret/private-marker, and generated-artifact checks are
  recorded.
- No parser, saved-event replay, SQLite schema, workbook, webhook, Apps
  Script, Google Sheets, OpenAI/AI, Line Tracer, Match Journal, production, or
  destructive-action behavior changes are made.

Codex B validation for this docs-only contract:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/analytics_browser_jsonl_multi_file_upload.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/analytics_browser_jsonl_multi_file_upload.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #214.

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

Goal:
Compare the current local app backend, import job orchestration, legacy JSONL
adapter, frontend Manual Import UI/API, and focused tests against the contract.
Implement only browser-based multi-file legacy JSONL upload. Produce
docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_comparison.md.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated local/generated artifacts.
- State what browser upload is supposed to do, what current path-based import
  already does, what gap remains, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/analytics_browser_jsonl_multi_file_upload.md
- docs/contracts/analytics_manual_jsonl_import_ui_job_status.md
- docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md
- docs/contracts/analytics_legacy_jsonl_batch_import.md
- docs/contracts/analytics_legacy_jsonl_artifact_adapter.md
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/import_jobs.py
- src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/App.tsx
- tests/test_analytics_manual_jsonl_import.py
- tests/test_analytics_legacy_jsonl_artifact_adapter.py
- frontend focused tests

Implement only:
- POST /api/imports/jsonl/upload multipart upload endpoint;
- upload request validation for file count, size, total size, .jsonl extension,
  nonempty files, and safe source labels;
- source_mode = "uploaded_file_batch";
- transient upload processing with guaranteed cleanup after success,
  degradation, failure, and rejection;
- one parser replay scope across uploaded files;
- deterministic uploaded-file ordering;
- raw saved-event hash dedupe across the uploaded batch without hash exposure;
- reuse of #212 quality and #213 source-artifact summaries;
- frontend multi-file picker and FormData upload API;
- focused synthetic backend/adapter/frontend tests;
- optional focused python-multipart dependency if FastAPI multipart parsing
  requires it;
- docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_comparison.md.

Do not:
- retain uploaded raw JSONL files after import;
- expose raw payloads, raw paths, raw hashes, internal content digests,
  temporary paths, stack traces, secrets, webhook URLs, API keys, or private
  local artifacts;
- change existing POST /api/imports/jsonl path or explicit source_paths
  behavior except compatible shared helper reuse;
- change parser behavior, saved-event replay semantics, latest-file directory
  selection, parser state final reconciliation, parser event classes, event
  kind values, match/game identity, parser-owned deduplication, analytics
  SQLite schema/migrations, workbook schema, webhook payload shape, Apps Script
  behavior, Google Sheets behavior, Match Journal behavior, OpenAI/model
  runtime, AI/coaching behavior, Line Tracer behavior, production behavior,
  deployment behavior, credential/environment contracts, or target main;
- add drag/drop, folder picker, webkitdirectory, recursive folder import,
  persistent import history, import deletion, job deletion, retries,
  cancellation, database reset/wipe/clear/export, live watcher behavior,
  destructive UI/backend actions, or generated/private/runtime artifacts;
- stage, commit, push, open a PR, close issues, or mark tracker #204 complete
  unless explicitly asked.

Validation:
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_legacy_jsonl_artifact_adapter.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools\check_secret_patterns.py --all

Also run path-scoped protected-surface and secret/private-marker scans over the
contract, implementation handoff, touched backend/import/adapter/frontend/test
files, and pyproject.toml if dependency changes. Report generated SQLite/local
artifact status and upload temp cleanup evidence.

Final handoff must include:
- role performed
- issue/tracker/umbrella reviewed
- contract used
- files changed
- exact backend route/functions/tests changed
- exact adapter helper/tests changed
- exact frontend modules/components/tests changed
- dependency decision
- upload temporary staging and cleanup behavior
- job response/source_mode/quality/source-artifact shape implemented
- validation results
- generated/private/runtime artifact status
- whether any forbidden scope was touched
- remaining unverified layers
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/214"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #214"
  target_artifact: "docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_comparison.md"
  contract_artifact: "docs/contracts/analytics_browser_jsonl_multi_file_upload.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped protected-surface scan for docs/contracts/analytics_browser_jsonl_multi_file_upload.md"
    - "path-scoped secret/private-marker scan for docs/contracts/analytics_browser_jsonl_multi_file_upload.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not retain uploaded raw JSONL files after import unless a later contract explicitly authorizes it."
    - "Do not expose raw payloads, raw paths, raw hashes, temporary paths, or destructive import/database/job actions."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```
