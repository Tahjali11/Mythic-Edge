# Analytics Legacy JSONL Batch Import Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Issue And Contract

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/213
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Related quality issue: https://github.com/Tahjali11/Mythic-Edge/issues/212
- Contract: `docs/contracts/analytics_legacy_jsonl_batch_import.md`
- Branch: `codex/analytics-foundation`
- Risk tier: High

## Branch And Worktree Status

Confirmed branch: `codex/analytics-foundation`.

Initial unrelated/untracked worktree items observed and preserved:

- `tests/test_analytics_dev_app_launcher.py`
- `tools/dev_app/dev_app_launcher.py`
- `Start Mythic Edge Dev App.cmd`
- untracked source contract `docs/contracts/analytics_legacy_jsonl_batch_import.md`

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_legacy_jsonl_batch_import.md`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`

## Current Behavior Compared To Contract

### Contract Matches Already Present

- Existing manual import route was already `POST /api/imports/jsonl`.
- Existing single-file `source_path` request behavior worked and preserved sanitized job status.
- Existing adapter used one parser-state scope and one `seen_raw_hashes` set for selected files.
- Existing adapter preserved directory selection through `saved_event_replay.latest_jsonl_files(...)`.
- Existing import-quality reporting from issue #212 was present, including aggregate quality status, skip reasons, warning codes, routing hints, and privacy flags.
- Existing frontend cleared the single raw path after terminal success/failure and did not use browser storage.
- Existing backend imported parser-normalized replay into local SQLite without changing parser truth ownership.

### Contract Gaps Found

- Backend did not accept explicit `source_paths`.
- Backend did not enforce exact-one-of `source_path` / `source_paths`.
- Backend did not validate explicit selected-file batches before app-data and SQLite creation.
- Adapter had no public explicit-file batch entry point.
- Job and adapter summaries did not expose batch metadata: `source_mode`, selected/accepted/rejected file counts, or safe per-file source summaries.
- Frontend request type and UI only supported one path.
- Focused tests did not cover shuffled selected-file ordering, cross-file duplicate hash counting, batch request validation, batch idempotence, or frontend batch submission/display.

## Implementation Option Chosen

Implemented the smallest scoped batch-import path authorized by the contract:

- Keep the existing route and schema version.
- Preserve existing single-file request behavior.
- Add additive batch metadata to the existing job payload instead of introducing a new route or response object.
- Add a public adapter batch helper while keeping `adapt_legacy_jsonl_artifacts(Path(...))` compatible.
- Keep all test data synthetic and temporary.

## Files Changed

- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md`

## Exact Sections Changed

### Adapter

- Added `ANALYTICS_LEGACY_JSONL_BATCH_IMPORT_SCHEMA_VERSION`.
- Added `adapt_legacy_jsonl_file_batch(...)`.
- Refactored the existing replay loop into shared selected-file processing.
- Added explicit-file deterministic sorting.
- Added safe per-file source summaries with:
  - `batch_index`
  - `source_artifact_label`
  - `source_display_label`
  - `status`
  - record/event counts
  - processed/unsupported kind counts
  - skipped reason counts
  - adapter warning codes
- Preserved existing single-file and directory behavior.

### Backend

- Added `MAX_LEGACY_JSONL_BATCH_FILES = 100`.
- Added exact-one-of validation for `source_path` and `source_paths`.
- Added `source_paths` validation for blank entries, duplicates after resolution, URL/UNC paths, missing files, directories, non-JSONL files, non-files, and too many files.
- Added batch adapter dispatch through `adapt_legacy_jsonl_file_batch(...)`.
- Added safe additive source and adapter metadata fields:
  - `source_mode`
  - `files_selected`
  - `files_accepted`
  - `files_rejected`
  - `source_group_label`
  - `source_artifacts`

### Frontend

- Extended `ManualImportRequest` to an exact-one union:
  - single `source_path`
  - batch `source_paths`
- Added optional batch metadata and source-artifact types.
- Added response validation for adapter `source_artifacts`.
- Added batch textarea input while preserving single-path input.
- Disabled submit when both single and batch inputs are filled.
- Cleared both single and batch raw path inputs after success or error.
- Added safe source-file summary display.
- Added CSS support for textarea and source-file summary section.

### Tests

- Added adapter batch tests for deterministic ordering and split replay reconstruction.
- Added adapter batch test for cross-file duplicate raw hash aggregation without exposing raw hashes.
- Added backend batch success and idempotence test.
- Added backend batch validation rejection tests before app-data creation.
- Added frontend API request test for `source_paths`.
- Added frontend UI tests for batch submission, sanitized display, cleared raw paths, and exact-one UI mode disabling.

## Code/Test/Docs Status

- Code changed: yes, scoped to local analytics adapter/backend/frontend surfaces.
- Tests changed: yes, focused synthetic tests only.
- Frontend changed: yes, local manual import UI only.
- Docs changed: yes, this handoff only.
- SQLite schema changed: no.
- SQLite database files created or committed: no repo-tracked DB files; validation used temp app-data only.

## Protected And Forbidden Scope Confirmation

No intentional changes were made to:

- parser behavior
- parser state final reconciliation
- saved-event replay semantics
- parser event classes
- match/game identity
- deduplication semantics outside the batch adapter's already scoped raw-hash skip set
- analytics SQLite schema or migrations
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets behavior
- Match Journal behavior
- OpenAI/model-provider behavior
- AI/coaching behavior
- Line Tracer behavior
- production behavior

No private local JSONL artifact was copied, sanitized, fixtured, committed, or raw-dumped.

No raw Player.log payloads or raw saved-event lines are stored in SQLite or exposed in durable job/source summaries.

No destructive import, database, job, launcher, or UI action was added.

## Validation Run

- `py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py` -> passed, 11 tests.
- `py -m pytest -q tests\test_analytics_manual_jsonl_import.py` -> passed, 14 tests, 1 existing FastAPI/Starlette deprecation warning.
- `py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py` -> passed, 35 tests, 1 existing FastAPI/Starlette deprecation warning.
- `npm --prefix frontend ci` -> passed, 0 vulnerabilities.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> passed, 3 test files, 21 tests.
- `npm --prefix frontend run build` -> passed.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- Path-scoped protected-surface scan over contract, handoff, adapter/backend/frontend/test files -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over contract, handoff, adapter/backend/frontend/test files -> passed, forbidden 0, warnings 0.

## Generated Artifact Status

- `npm --prefix frontend run build` produced ignored frontend build output only.
- No generated SQLite database file was added to the repo.
- No runtime status, failed-post, raw-log, workbook export, private JSONL, or local-only artifact was added.

## Remaining Risks Or Unverified Layers

- Live/manual operator import against a real private local JSONL artifact was not run.
- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Production behavior was not exercised.
- The frontend was not manually browser-inspected; validation was automated through typecheck, tests, and build.
- Existing unrelated launcher worktree changes remain outside this module.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #213.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/213

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Related quality issue:
https://github.com/Tahjali11/Mythic-Edge/issues/212

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_legacy_jsonl_batch_import.md

Implementation handoff:
docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md

Risk tier:
High

Goal:
Review the #213 implementation against docs/contracts/analytics_legacy_jsonl_batch_import.md. Lead with findings ordered by severity. Verify that explicit `source_paths` batch import support is scoped, safe, additive, and contract-compliant. Do not implement fixes unless explicitly asked; route concrete findings to Codex D.

Review focus:
- Existing single-file `source_path` behavior remains compatible.
- Existing adapter directory/latest-file selection semantics remain compatible.
- `source_path` and `source_paths` are exact-one request modes.
- Batch path validation rejects unsafe/invalid paths before app-data or SQLite creation.
- Batch replay uses deterministic internal ordering, one parser-state scope, and one cross-file raw-hash dedupe set.
- Per-file source summaries and aggregate quality are safe and do not expose raw paths, raw payloads, raw hashes, stack traces, secrets, or local artifacts.
- Import-quality reporting from issue #212 is preserved.
- Batch re-import is idempotent at the SQLite facts layer.
- Frontend supports batch request/display while clearing raw paths after terminal success/failure and exposing no destructive UI actions.
- No parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/Line Tracer/production behavior changed.

Read:
- docs/contracts/analytics_legacy_jsonl_batch_import.md
- docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md
- src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
- src/mythic_edge_parser/local_app/import_jobs.py
- tests/test_analytics_legacy_jsonl_artifact_adapter.py
- tests/test_analytics_manual_jsonl_import.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx
- frontend/src/api.test.ts
- adjacent #211/#212 handoffs or reports if needed

Validation to rerun or sample:
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
Run path-scoped protected-surface and secret/private-marker scans over the contract, handoff, and touched adapter/backend/frontend/test files.

Do not:
- Target main.
- Change parser behavior.
- Change parser state final reconciliation.
- Change saved-event replay semantics.
- Change parser event classes, match/game identity, or deduplication outside the scoped adapter batch raw-hash skip behavior.
- Change analytics SQLite schema or migrations.
- Change workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, Match Journal behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, or production behavior.
- Commit, copy, sanitize, fixture, or raw-dump private local JSONL artifacts.
- Store raw Player.log payloads or raw saved-event lines.
- Expose raw payloads, raw paths, raw hashes, stack traces, secrets, webhook URLs, API keys, or private local artifacts.
- Add destructive import, database, job, launcher, or UI actions.
- Stage, commit, push, open a PR, merge, close issue #213, or mark tracker #204 complete unless explicitly asked.

Final review report must include:
- role performed
- issue/tracker/umbrella/related quality issue
- contract and handoff reviewed
- findings first, ordered by severity with file/line references
- contract matches
- contract mismatches
- missing safeguards or missing tests
- validation run and result
- protected-surface status
- secret/private-marker status
- generated artifact status
- whether forbidden scope was touched
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/213"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  related_quality_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/212"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  contract_artifact: "docs/contracts/analytics_legacy_jsonl_batch_import.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md"
  branch: "codex/analytics-foundation"
  risk_tier: "High"
  validation:
    - "py -m pytest -q tests\\test_analytics_legacy_jsonl_artifact_adapter.py -> passed, 11 tests"
    - "py -m pytest -q tests\\test_analytics_manual_jsonl_import.py -> passed, 14 tests, 1 existing FastAPI/Starlette deprecation warning"
    - "py -m pytest -q tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_local_app_backend.py -> passed, 35 tests, 1 existing FastAPI/Starlette deprecation warning"
    - "npm --prefix frontend ci -> passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> passed, 3 files, 21 tests"
    - "npm --prefix frontend run build -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan over contract, handoff, adapter/backend/frontend/test files -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over contract, handoff, adapter/backend/frontend/test files -> passed, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not target main."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/Line Tracer/production behavior."
    - "Do not change saved-event replay semantics or latest-file directory selection."
    - "Do not change analytics SQLite schema or migrations."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
    - "Do not expose raw payloads, raw paths, raw hashes, stack traces, or destructive import/database/job actions."
```
