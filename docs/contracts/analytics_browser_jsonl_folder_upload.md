# Analytics Browser JSONL Folder Upload Contract

## Role And Scope

role: Codex B / Module Contract Writer
issue: https://github.com/Tahjali11/Mythic-Edge/issues/223
tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
umbrella_issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
branch: codex/analytics-browser-jsonl-folder-upload
risk_tier: High
target_artifact: docs/contracts/analytics_browser_jsonl_folder_upload.md

This contract defines the first browser-folder-selection enhancement for the local analytics app JSONL upload flow. It is a UI selection contract over the existing browser multi-file upload/import route, not a backend filesystem traversal feature.

## Source Artifacts Inspected

- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/project_roadmap.md
- docs/internal_project_map.md
- docs/contracts/analytics_local_developer_app_shell.md
- docs/contracts/analytics_manual_jsonl_import_ui_job_status.md
- docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md
- docs/contracts/analytics_legacy_jsonl_batch_import.md
- docs/contracts/analytics_browser_jsonl_multi_file_upload.md
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/import_jobs.py
- src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
- frontend/src/App.tsx
- frontend/src/api.ts
- frontend/src/types.ts
- frontend/src/App.test.tsx
- frontend/src/api.test.ts
- tests/test_analytics_browser_jsonl_upload.py
- tests/test_analytics_manual_jsonl_import.py
- tests/test_analytics_legacy_jsonl_artifact_adapter.py
- GitHub issue #223

## Observed Current Behavior

- The local analytics backend exposes `POST /api/imports/jsonl/upload` for browser-selected multipart JSONL files.
- The upload route accepts repeated `files` form parts plus an optional `source_artifact_label`.
- The upload route starts a manual import job through `run_browser_jsonl_upload_import`.
- Upload import jobs use `uploaded_file_batch` source mode and do not persist uploaded raw JSONL files after import processing.
- Upload validation already enforces server-side limits:
  - at least one file
  - at most 100 files
  - `.jsonl` file extension
  - non-empty file body
  - at most 25 MiB per file
  - at most 250 MiB total
- The legacy JSONL adapter already sanitizes uploaded display names, strips path separators, avoids private marker display, deduplicates by raw hash inside the uploaded batch, and reports privacy metadata showing raw payloads, raw hashes, and private paths are not exposed.
- The frontend currently supports manual JSONL upload with a normal multi-file input using `multiple` and `accept=".jsonl"`.
- The current frontend selection display sanitizes selected basenames and does not intentionally display full paths, raw hashes, or payload contents.
- The existing browser multi-file upload contract intentionally left folder picker support out of scope; issue #223 is the follow-up contract for that missing UI convenience.

## Contract Decision

Mythic Edge may add browser folder selection for JSONL import as a thin frontend convenience over the existing multi-file upload route.

The folder picker must not create a new truth source, import source mode, backend directory traversal feature, raw path collection mechanism, or retained raw artifact class. The backend must continue to receive only browser-provided file parts and must continue to treat them as an uploaded file batch.

## Public Interfaces

### Existing Backend Interface

The approved backend interface remains:

```text
POST /api/imports/jsonl/upload
multipart/form-data:
  files: one or more .jsonl uploaded file parts
  source_artifact_label: optional display/source label
```

No new backend route is required for the folder-upload pass.

No backend request field may contain a local absolute directory path, browser relative path, folder name, raw payload excerpt, raw hash, or machine-specific path.

### Existing Frontend API Interface

The approved frontend API shape remains:

```ts
ManualImportUploadRequest {
  files: File[]
  source_artifact_label?: string
}
```

Folder selection may populate the same `files` array after client-side filtering. A new request type is not required.

### Browser UI Interface

Codex C may add a folder selection control using browser file input capabilities such as `webkitdirectory` when supported.

The existing multi-file upload control must remain available. Unsupported browsers must still be able to use the existing multi-file upload flow.

If TypeScript or React does not expose a first-class `webkitdirectory` input attribute, Codex C may add a narrow local typing workaround in frontend code or tests. That workaround must not broaden the upload API or backend schema.

## Required Guarantees

### Folder Selection Behavior

- Folder selection is a browser-side file selection convenience.
- The selected folder itself is not uploaded.
- The backend must not receive a directory path and must not walk the local filesystem.
- Returned browser `FileList` values may include files from nested folders if the browser provides them recursively.
- Mythic Edge must treat the browser-returned `FileList` as a flat candidate set.
- Folder hierarchy must not be preserved, displayed, sent to the backend, used for deduplication, or treated as provenance.
- The implementation must not rely on `webkitRelativePath` for import identity, source labels, job status, display text, evidence, or analytics facts.

### File Filtering

- Client-side folder selection must filter candidates to `.jsonl` filenames before submit.
- Extension matching should be case-insensitive.
- Non-JSONL selected files must not be uploaded.
- The UI may show a safe count of ignored non-JSONL files.
- If filtering leaves zero JSONL files, the upload action must not start and the UI must present a safe, non-path-specific message.
- Server-side validation remains authoritative; backend rejection behavior must still protect direct or malformed requests.

### Limits And Rejections

- Existing backend limits remain authoritative:
  - maximum file count: 100
  - maximum per-file size: 25 MiB
  - maximum total size: 250 MiB
- The frontend may preflight count or extension problems, but any frontend preflight must match existing backend semantics.
- Backend rejection payloads must not echo raw payloads, raw hashes, full local paths, relative folder paths, or private machine markers.
- Job status should keep the existing accepted/rejected/skipped/warning style from the browser multi-file upload and manual import contracts.

### Safe Display Rules

- UI display may include:
  - selected JSONL count
  - ignored non-JSONL count
  - a small list of sanitized basenames
  - generic labels such as selected folder files or uploaded batch
- UI display must not include:
  - absolute paths
  - drive letters
  - UNC paths
  - local user profile names
  - folder hierarchy
  - `webkitRelativePath`
  - raw JSONL payloads
  - raw Player.log excerpts
  - raw hashes
  - stack traces
  - secret or credential-like values
- Existing basename sanitization must continue to be used for visible filenames.

### Import Semantics

- Folder-selected JSONL files must use the existing browser upload import path.
- The source mode remains `uploaded_file_batch`.
- Existing source artifact label behavior remains valid.
- Existing per-record adapter rules remain valid:
  - no raw Player.log storage in SQLite
  - no raw JSONL payload retention
  - no raw hash exposure in UI/status payloads
  - legacy derived fields are not parser truth
  - parser-normalized outputs remain downstream facts only when accepted by existing analytics ingest contracts
- Existing uploaded-batch deduplication scope remains an uploaded batch, not a folder, path, day, or local machine scope.

### Truth Ownership

- Browser folder selection is not parser truth.
- Folder names are not evidence ledger truth.
- JSONL file names are not parser truth.
- Legacy JSONL derived fields are not parser truth.
- Analytics ingest remains downstream of parser-normalized or legacy-adapted records and must not reinterpret raw Player.log semantics.
- AI, coaching, Match Journal, Google Sheets, workbook formulas, and Apps Script remain out of scope.

## Allowed Implementation Surface For Codex C

Codex C may make narrow changes in:

- frontend/src/App.tsx
- frontend/src/App.css, only if needed for folder-upload UI state
- frontend/src/types.ts, only if needed for a narrow frontend type helper
- frontend/src/App.test.tsx
- frontend/src/api.test.ts, only if API-level no-path behavior needs a focused regression
- tests/test_analytics_browser_jsonl_upload.py, only for backend regression coverage proving existing upload safety still holds
- docs/implementation_handoffs/analytics_browser_jsonl_folder_upload_comparison.md

Backend behavior changes are not expected. If Codex C discovers that existing backend upload sanitization leaks folder-relative paths or unsafe filenames, it must stop and route back to Codex B or A unless the fix is a narrow test-only clarification. This contract does not authorize broad backend behavior changes.

## Forbidden Scope

Do not:

- add backend directory traversal
- add path-based import from browser-selected folders
- add recursive filesystem reading on the backend
- retain uploaded raw JSONL files after import processing
- display or persist absolute paths, relative paths, folder names, raw hashes, or raw payloads
- create generated/private/runtime artifacts
- create SQLite database files
- change parser behavior
- change parser state final reconciliation
- change parser event classes
- change match/game identity or deduplication
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- change Google Sheets, Match Journal, OpenAI, AI, coaching, or production behavior
- add destructive import, database, job, launcher, or UI actions
- target main

## Unknowns

- Browser support for `webkitdirectory` is not uniform across all browsers.
- The exact ordering returned by folder selection may vary by browser.
- Some browser implementations may populate `webkitRelativePath`; the first implementation must ignore it for display, API payload metadata, provenance, and identity.
- It is unknown whether TypeScript definitions in the current frontend stack directly accept `webkitdirectory`.
- It is unknown whether large folder selections need extra frontend UX beyond backend limit errors; this contract allows safe count/error display but does not require a richer import preview.

## Suspected Gaps

- The current frontend only exposes individual multi-file selection, so selecting many day-folder JSONL files is unnecessarily tedious.
- The current frontend likely does not client-filter mixed folder selections before upload because normal file picker `accept=".jsonl"` is only a picker hint.
- Existing tests likely cover multi-file upload but not a folder-selection path, recursive/mixed-file client filtering, or non-use of `webkitRelativePath`.
- Existing backend tests may not explicitly prove that path-like uploaded filenames are sanitized in the browser upload job summary.

## Validation Requirements

Codex C should run the smallest relevant checks first, then broaden:

```powershell
npm --prefix frontend run test -- --run
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py tests\test_analytics_manual_jsonl_import.py tests\test_analytics_legacy_jsonl_artifact_adapter.py
git diff --check
```

If Python backend tests are changed or backend upload behavior is touched, also run:

```powershell
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_browser_jsonl_upload.py tests\test_analytics_manual_jsonl_import.py
py -m ruff check src tests tools
```

Codex C and Codex E must also report:

- no SQLite database files created or committed
- no raw JSONL fixtures copied or committed
- no raw Player.log excerpts added
- no raw path, raw hash, credential, or secret exposure in new UI/status/test fixtures
- protected-surface scan results for changed paths

## Acceptance Criteria

- A user can choose a folder of JSONL artifacts from the browser UI when the browser supports folder selection.
- The existing multi-file upload path still works.
- Folder selection filters to JSONL files before upload.
- Mixed folder selections do not upload non-JSONL files.
- Nested folder selections are treated as a flat browser file batch.
- UI/status output does not expose folder paths, relative paths, raw payloads, or raw hashes.
- The backend upload route and request schema remain unchanged unless a later contract explicitly authorizes a change.
- Existing browser upload source mode, limits, privacy summary, row count, warning, and skipped/rejected behavior remain intact.
- Focused frontend tests cover folder selection, mixed-file filtering, and safe display.
- Focused backend or adapter tests cover upload privacy/sanitization if the existing coverage is insufficient.
- A comparison handoff documents files inspected, matches, gaps, protected-surface status, validation, remaining risk, and next recommended role.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #223.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-browser-jsonl-folder-upload

Contract:
docs/contracts/analytics_browser_jsonl_folder_upload.md

Goal:
Compare the current local analytics app JSONL upload UI, upload API, backend route, import job behavior, and tests against the folder-upload contract. Implement only the narrow browser folder-selection UI enhancement and focused tests needed by the contract. Produce docs/implementation_handoffs/analytics_browser_jsonl_folder_upload_comparison.md.

Before editing, confirm branch and git status. State what folder upload is supposed to do, what the current UI already does, what gap remains, and the exact minimal implementation plan.

Do:
- Preserve the existing multi-file upload route and request shape.
- Add browser folder selection as a frontend convenience over the existing upload route.
- Treat browser-returned folder files as a flat selected file set.
- Filter to .jsonl files before upload.
- Avoid displaying, sending, or relying on folder paths, relative paths, raw hashes, or raw payloads.
- Add focused frontend tests for folder selection, mixed-file filtering, and safe display.
- Add focused backend privacy/sanitization tests only if existing coverage is insufficient.
- Produce the comparison handoff.

Do not:
- add backend directory traversal
- add a new backend route unless the contract is routed back and amended
- retain uploaded raw JSONL files
- expose raw payloads, raw paths, raw hashes, secrets, or local machine markers
- change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior
- create SQLite files or generated/private/runtime artifacts
- target main
- close tracker #204 or umbrella #207
- stage, commit, push, open a PR, or merge unless explicitly asked

Validation:
npm --prefix frontend run test -- --run
npm --prefix frontend run typecheck
npm --prefix frontend run build
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py tests\test_analytics_manual_jsonl_import.py tests\test_analytics_legacy_jsonl_artifact_adapter.py
git diff --check

If backend upload behavior is touched, also run:
py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_browser_jsonl_upload.py tests\test_analytics_manual_jsonl_import.py
py -m ruff check src tests tools

Final handoff must include role performed, source issue/tracker, files changed, exact UI/API/test sections changed, validation run, protected-surface status, remaining risk, next recommended role, and workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex B: Module Contract Writer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/223"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  branch: "codex/analytics-browser-jsonl-folder-upload"
  source_artifact: "GitHub issue #223 and current analytics browser upload implementation"
  target_artifact: "docs/contracts/analytics_browser_jsonl_folder_upload.md"
  risk_tier: "High"
  next_recommended_role: "Codex C: Module Implementer / comparison thread"
  validation:
    - "Codex B docs-only validation required: git status --short --branch"
    - "Codex B docs-only validation required: git diff --check"
    - "Codex C should run frontend tests/typecheck/build and focused browser upload/import tests"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not add backend directory traversal or path-based folder import."
    - "Do not retain uploaded raw JSONL files after import processing."
    - "Do not expose raw payloads, raw paths, raw hashes, secrets, or local machine markers."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior."
    - "Do not create SQLite files or generated/private/runtime artifacts."
    - "Do not target main."
```
