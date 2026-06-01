# Analytics Browser JSONL Folder Upload Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Issue / Tracker / Umbrella

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/223
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract Used

- `docs/contracts/analytics_browser_jsonl_folder_upload.md`

## Branch And Git Status

- Branch confirmed: `codex/analytics-browser-jsonl-folder-upload`
- Local branch base: `origin/codex/analytics-foundation` is present; no remote branch named `origin/codex/analytics-browser-jsonl-folder-upload` was present locally.
- Pre-edit status: `frontend` was clean; contract file was untracked.
- Post-implementation status includes:
  - modified `frontend/src/App.tsx`
  - modified `frontend/src/App.test.tsx`
  - untracked `docs/contracts/analytics_browser_jsonl_folder_upload.md`
  - added `docs/implementation_handoffs/analytics_browser_jsonl_folder_upload_comparison.md`

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_browser_jsonl_folder_upload.md`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`
- `frontend/package.json`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `tests/test_analytics_browser_jsonl_upload.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`

## Current Behavior Compared To Contract

### Already Matched

- Backend upload route already exists at `POST /api/imports/jsonl/upload`.
- Frontend API request shape already uses `ManualImportUploadRequest { files: File[]; source_artifact_label?: string }`.
- Existing multi-file upload control remains available.
- Backend upload route already validates extension, count, per-file size, total size, empty files, and invalid multipart entries.
- Backend upload/import tests already prove uploaded raw JSONL files are not retained in app data.
- Backend and adapter tests already prove upload summaries do not expose raw payloads, raw hashes, or path-like uploaded names.

### Gaps Found

- The frontend only exposed normal multi-file selection.
- There was no browser folder-selection control using `webkitdirectory` or equivalent.
- Folder-returned mixed file lists were not filtered client-side before upload.
- Tests did not cover folder selection, mixed non-JSONL filtering, or the non-use of `webkitRelativePath` for visible display.

## Implementation Option Chosen

Frontend-only folder selection over the existing browser upload route.

The implementation treats browser folder selection as a flat file-list convenience. It does not add a backend route, backend directory traversal, a new request type, path-based import, parser behavior, schema behavior, or any production/runtime integration.

## Files Changed

- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_browser_jsonl_folder_upload_comparison.md`

The Codex B contract remains untracked as source context:

- `docs/contracts/analytics_browser_jsonl_folder_upload.md`

## Exact Sections Changed

### `frontend/src/App.tsx`

- Added folder-selection state for ignored non-JSONL count and safe no-JSONL message.
- Added `handleUploadFolderFilesChange` to filter folder-selected candidates to case-insensitive `.jsonl` filenames.
- Added a folder-picker input labeled `Upload JSONL folder`.
- Set `webkitdirectory` and `directory` as DOM attributes through a narrow ref callback, avoiding a broader TypeScript or API shape change.
- Updated upload clearing to reset both file and folder inputs.
- Added safe helper functions for ignored-file count display and `.jsonl` extension matching.

### `frontend/src/App.test.tsx`

- Added a focused folder-selection test covering:
  - `webkitdirectory` attribute presence
  - mixed folder files
  - case-insensitive `.jsonl` acceptance
  - non-JSONL filtering before upload
  - safe display that omits `webkitRelativePath` folder segments
  - existing `uploaded_file_batch` job summary preservation
- Added a focused no-JSONL folder-selection test covering:
  - ignored non-JSONL count
  - safe no-JSONL message
  - disabled upload action
  - no upload submission
  - no folder/path display

### Handoff

- Added this comparison handoff.

## Change Classification

- Code changed: yes, frontend only.
- Tests changed: yes, focused frontend tests only.
- Docs changed: yes, implementation handoff only.
- Backend changed: no.
- Parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior changed: no.

## Validation Run And Result

- `npm --prefix frontend run test -- --run` -> passed, 3 files / 30 tests.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run build` -> passed.
- `py -m pytest -q tests\test_analytics_browser_jsonl_upload.py tests\test_analytics_manual_jsonl_import.py tests\test_analytics_legacy_jsonl_artifact_adapter.py` -> passed, 40 tests; one existing FastAPI/Starlette deprecation warning from dependency stack.
- `git diff --check` -> passed.
- Path-scoped protected-surface scan with `--paths-from-stdin` against `origin/codex/analytics-foundation` -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan with `--paths-from-stdin` against `origin/codex/analytics-foundation` -> passed, forbidden 0, warnings 0.
- Full protected-surface scan against `origin/codex/analytics-foundation` -> passed, changed_paths 0 because local edits are not committed.
- Full secret/private-marker scan against `origin/codex/analytics-foundation` -> passed, changed-files mode found no committed diff.

Note: initial attempts using unsupported repeated `--path` arguments were corrected to the repo-supported `--paths-from-stdin` form.

## Protected-Surface Status

No protected parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production surfaces were edited.

## Secret / Private-Marker Status

Path-scoped secret/private-marker scan passed with forbidden 0 and warnings 0 for:

- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `docs/contracts/analytics_browser_jsonl_folder_upload.md`

## Generated Artifact Status

- No SQLite database files were created as tracked or untracked repo changes.
- No raw JSONL artifacts, raw Player.log excerpts, runtime payloads, retry-queue payloads, workbook exports, or local-only private artifacts were added.
- `git status --short --ignored frontend\dist data\analytics data\status data\runtime_logs data\failed_posts` showed ignored local/generated directories including `frontend/dist/`, `data/status/`, `data/runtime_logs/`, and `data/failed_posts/`. These remain ignored and unstaged.

## Safety Confirmations

- Uploaded raw JSONL files are not retained by this frontend change.
- No raw payloads, raw paths, raw hashes, temporary paths, stack traces, secrets, webhook URLs, API keys, or private local artifacts are displayed by the new folder-selection UI.
- `webkitRelativePath` is not used for import identity, source labels, job status, display text, evidence, or analytics facts.
- Folder hierarchy is ignored; selected JSONL files are treated as a flat browser file batch.
- No destructive import, database, job, launcher, or UI actions were added.
- Existing #214 multi-file upload behavior was preserved.
- Existing #213 explicit `source_paths` batch import behavior was preserved.
- Existing #212 import-quality reporting was preserved.

## Remaining Unverified

- Manual browser smoke test in a real browser with an actual folder picker was not run.
- Browser support differences for `webkitdirectory` remain an accepted contract unknown.
- No remote CI was run from this local thread.

## Forbidden Scope Touched

No forbidden scope was touched.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #223.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/223

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-browser-jsonl-folder-upload

Contract:
docs/contracts/analytics_browser_jsonl_folder_upload.md

Implementation handoff:
docs/implementation_handoffs/analytics_browser_jsonl_folder_upload_comparison.md

Goal:
Review the Codex C folder-upload implementation against the contract. Confirm that the browser folder picker is a frontend-only convenience over the existing upload route, that mixed folder selections are filtered to JSONL before upload, that folder paths and webkitRelativePath are not displayed or used as provenance, and that existing multi-file upload, batch import, import-quality reporting, backend request shape, and privacy boundaries are preserved.

Review:
- frontend/src/App.tsx
- frontend/src/App.test.tsx
- docs/contracts/analytics_browser_jsonl_folder_upload.md
- docs/implementation_handoffs/analytics_browser_jsonl_folder_upload_comparison.md
- existing backend/upload/import tests if needed:
  - tests/test_analytics_browser_jsonl_upload.py
  - tests/test_analytics_manual_jsonl_import.py
  - tests/test_analytics_legacy_jsonl_artifact_adapter.py

Do not:
- target main
- add backend directory traversal
- add a new backend route
- retain uploaded raw JSONL files
- expose raw payloads, raw paths, raw hashes, temporary paths, stack traces, secrets, webhook URLs, API keys, or private local artifacts
- add destructive import/database/job/launcher/UI actions
- change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior
- stage, commit, push, open a PR, merge, close issue #223, or mark tracker #204 complete unless explicitly asked

Validation to run:
- git status --short --branch
- npm --prefix frontend run test -- --run
- npm --prefix frontend run typecheck
- npm --prefix frontend run build
- py -m pytest -q tests\test_analytics_browser_jsonl_upload.py tests\test_analytics_manual_jsonl_import.py tests\test_analytics_legacy_jsonl_artifact_adapter.py
- git diff --check
- path-scoped protected-surface scan over touched files
- path-scoped secret/private-marker scan over touched files
- generated artifact status check

Final review must lead with findings, ordered by severity. If no blocking findings, say so clearly. Include validation run, remaining risks, protected-surface status, whether forbidden scope was touched, and next recommended role.
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex C: Module Implementer / comparison thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/223"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  branch: "codex/analytics-browser-jsonl-folder-upload"
  source_artifact: "docs/contracts/analytics_browser_jsonl_folder_upload.md"
  target_artifact: "docs/implementation_handoffs/analytics_browser_jsonl_folder_upload_comparison.md"
  files_changed:
    - "frontend/src/App.tsx"
    - "frontend/src/App.test.tsx"
    - "docs/implementation_handoffs/analytics_browser_jsonl_folder_upload_comparison.md"
  validation:
    - "npm --prefix frontend run test -- --run -> passed, 3 files / 30 tests"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run build -> passed"
    - "py -m pytest -q tests\\test_analytics_browser_jsonl_upload.py tests\\test_analytics_manual_jsonl_import.py tests\\test_analytics_legacy_jsonl_artifact_adapter.py -> passed, 40 tests, 1 existing dependency warning"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  protected_surface_status: "No protected parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production surfaces touched."
  forbidden_scope_touched: false
  remaining_unverified:
    - "Manual real-browser folder-picker smoke test"
    - "Remote CI"
  next_recommended_role: "Codex E: Module Reviewer / contract-test thread"
```
