# Security JSONL Upload Preallocation Byte Limits Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/459

## Parent Security Workflow

https://github.com/Tahjali11/Mythic-Edge/issues/330

## Contract

`docs/contracts/security_jsonl_upload_preallocation_byte_limits.md`

## Internal Project Area

Local App / UI security and upload handling.

## Truth Owner

Backend local app upload validation owns the byte-limit decision for
`POST /api/imports/jsonl/upload`.

Parser truth, analytics truth, workbook truth, Apps Script truth, OpenAI/AI
truth, and production behavior are unchanged.

## Bridge-Code Status

`shared_support`

The upload route remains a bridge from browser multipart uploads into the
existing `BrowserJsonlUploadFile` adapter input. The bridge now validates byte
budgets before constructing that adapter input.

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Artifacts Used

- GitHub issue #459
- Parent security workflow #330
- `docs/contracts/security_jsonl_upload_preallocation_byte_limits.md`
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`

## Files Inspected

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `tests/test_analytics_browser_jsonl_upload.py`
- `tests/test_analytics_local_app_backend.py`

## Current Behavior Compared To Contract

Before this implementation, `POST /api/imports/jsonl/upload` called
`await upload_file.read()` while constructing `BrowserJsonlUploadFile`. The
existing `import_jobs._validate_upload_request` then enforced per-file and
aggregate byte limits after the full uploaded content had already been read
into memory.

That matched the contract's first bad value: validation was correct as
defense-in-depth, but it happened too late to prevent preallocation of an
oversized upload.

The #458 local request guard was already attached to the upload route and was
preserved.

## Implementation Option Chosen

Implemented the contract-preferred endpoint-local capped read path in
`backend.py`.

The route still parses multipart form data through FastAPI/Starlette, then:

1. extracts the `files` form parts;
2. rejects non-file parts without echoing submitted values;
3. validates file count before reading file content;
4. reads each `UploadFile` in bounded chunks using the existing
   `import_jobs` byte-limit constants;
5. raises symbolic local errors for per-file or aggregate limit failures;
6. constructs `BrowserJsonlUploadFile` only after the file's content passes
   the capped read;
7. closes upload files and the form object on success and rejection.

The existing import job validation remains in place as defense-in-depth.

## Files Changed

- `docs/contracts/security_jsonl_upload_preallocation_byte_limits.md`
- `docs/implementation_handoffs/security_jsonl_upload_preallocation_byte_limits_comparison.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_browser_jsonl_upload.py`

## Exact Code Sections Changed

### `src/mythic_edge_parser/local_app/backend.py`

- Added an `import_jobs` module import so route-level capped reads use the same
  mutable constants as downstream validation and tests.
- Added `_BROWSER_JSONL_UPLOAD_READ_CHUNK_BYTES`.
- Added `_BrowserJsonlUploadReadError`.
- Reworked `import_jsonl_upload` to:
  - keep #458 guarded route dependencies unchanged;
  - validate form part type before content reads;
  - reject source label type errors before content reads;
  - use `_build_browser_jsonl_upload_files`;
  - return existing sanitized rejected-job payloads for upload read errors;
  - close `UploadFile` objects and form resources in `finally`.
- Added `_build_browser_jsonl_upload_files`.
- Added `_read_browser_jsonl_upload_file`.

### `tests/test_analytics_browser_jsonl_upload.py`

- Added `_RecordingUpload`, a synthetic async upload stream used only by tests.
- Added `test_upload_builder_rejects_too_many_files_before_content_reads`.
- Added `test_upload_builder_stops_single_oversized_file_before_full_read`.
- Added
  `test_upload_builder_stops_aggregate_oversized_batch_before_remaining_reads`.

## Interface Changes

No public API shape changed.

The upload route still returns the existing sanitized import-job envelope for
upload validation failures. No frontend behavior, backend route shape, request
guard header name, parser output, analytics schema, workbook schema, webhook
payload, Apps Script behavior, or production behavior changed.

Private backend helper functions were added for the route-local capped read
implementation and focused tests.

## Code Changed

Yes. Runtime code changed only in local app backend upload handling:

- `src/mythic_edge_parser/local_app/backend.py`

## Tests Changed

Yes. Focused browser-upload tests were extended:

- `tests/test_analytics_browser_jsonl_upload.py`

## Docs Changed

Yes. The Codex B contract artifact is included, and this Codex C handoff was
created:

- `docs/contracts/security_jsonl_upload_preallocation_byte_limits.md`
- `docs/implementation_handoffs/security_jsonl_upload_preallocation_byte_limits_comparison.md`

## Validation Run

```text
git fetch --prune -> passed
git rev-list --left-right --count HEAD...origin/main -> 0 2 before fast-forward; 0 0 after fast-forward
gh issue view 459 --json number,state,title,url,body --comments -> issue open
gh issue view 330 --json number,state,title,url,body -> parent open
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py -> 14 passed, 1 warning
py -m pytest -q tests\test_analytics_local_app_backend.py -> 32 passed, 1 warning
py -m ruff check src\mythic_edge_parser\local_app\backend.py -> passed
py -m ruff check src tests -> passed
git diff --check -> passed
py tools\check_agent_docs.py -> passed
path-scoped protected-surface scan over changed files -> passed, forbidden 0, warnings 0
path-scoped secret/private-marker scan over changed files -> passed, forbidden 0, warnings 0
```

## Protected-Surface Status

Protected parser/downstream surfaces were not intentionally touched.

Unaffected:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity;
- deduplication;
- analytics schema and ingest truth;
- workbook schema;
- webhook payload shape;
- Apps Script and Google Sheets behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- production behavior.

## Secret And Private-Artifact Status

No raw uploaded JSONL data, raw Player.log content, raw paths, raw hashes,
guard tokens, secrets, generated SQLite files, runtime files, workbook exports,
or local-only artifacts were added.

Oversized upload rejection remains symbolic through existing error codes:

- `upload_file_too_large`
- `upload_total_size_too_large`
- `upload_files_too_many`
- `upload_files_required`

## Remaining Risks Or Unverified Layers

- FastAPI/Starlette `request.form()` may still buffer or spool multipart data
  before route code can run. This implementation fixes the explicit unbounded
  route-level `await upload_file.read()` allocation. If framework-level request
  parsing remains an unacceptable memory risk, route back to Codex B for a
  separate middleware/request-size contract.
- GitHub CodeQL must rerun after submission before the related alert can be
  considered closed.
- No browser/frontend validation was run because no frontend files changed and
  the response envelope was preserved.

## Forbidden Scope

Forbidden scope was not touched.

No parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/
AI/coaching/production behavior changed. No app-wide request-size middleware,
cloud upload, external write, CI change, CodeQL dismissal, staging, commit,
push, PR, merge, or issue closure was performed.

## Reviewer Focus

Codex E should verify:

- the upload route still requires the #458 request guard before route behavior;
- file count validation happens before content reads;
- per-file oversized uploads stop after the byte budget plus one bounded read;
- aggregate oversized uploads stop without reading remaining file content;
- `BrowserJsonlUploadFile` is constructed only for accepted byte buffers;
- rejected responses stay sanitized;
- existing downstream validation remains defense-in-depth;
- the framework-level multipart buffering caveat is correctly classified as
  residual risk, not silently closed.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #459.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/459

Parent security workflow:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Branch:
codex/jsonl-upload-preallocation-limits-459

Contract:
docs/contracts/security_jsonl_upload_preallocation_byte_limits.md

Implementation handoff:
docs/implementation_handoffs/security_jsonl_upload_preallocation_byte_limits_comparison.md

Goal:
Review the implementation against the contract. Verify that browser JSONL
uploads are read through endpoint-local capped reads before constructing
BrowserJsonlUploadFile, while preserving the #458 local request guard,
privacy-safe rejection envelope, valid upload behavior, parser truth,
analytics truth, and all protected downstream surfaces.

Inspect:
- git status --short --branch --untracked-files=all
- docs/contracts/security_jsonl_upload_preallocation_byte_limits.md
- docs/implementation_handoffs/security_jsonl_upload_preallocation_byte_limits_comparison.md
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/import_jobs.py
- tests/test_analytics_browser_jsonl_upload.py
- tests/test_analytics_local_app_backend.py

Review focus:
- Guard failures still reject before upload route behavior.
- File count validation happens before content reads.
- Oversized single-file uploads reject as upload_file_too_large before full read.
- Aggregate oversized uploads reject as upload_total_size_too_large before reading remaining content.
- BrowserJsonlUploadFile is constructed only after capped read validation passes.
- UploadFile and form resources are closed on success and rejection.
- Rejected responses do not expose raw payloads, raw paths, raw hashes, guard tokens, temp paths, stack traces, local-only artifacts, or secrets.
- Existing valid upload behavior and rejected-job response shape are preserved.
- Framework-level multipart parser buffering is correctly left as residual risk unless a new contract addresses it.

Validation:
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m ruff check src tests
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed files with base origin/main.

Do not:
- implement fixes unless explicitly rerouted as Codex D;
- dismiss CodeQL alerts;
- stage, commit, push, open a PR, merge, close #459, or close #330;
- change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.

Output:
- findings first, ordered by severity;
- contract-test verdict;
- validation run and result;
- protected-surface status;
- secret/private-marker status;
- generated/private artifact status;
- remaining risks;
- next recommended role;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/459"
  parent_security_workflow: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/security_jsonl_upload_preallocation_byte_limits.md"
  target_artifact: "docs/implementation_handoffs/security_jsonl_upload_preallocation_byte_limits_comparison.md"
  risk_tier: "High security/local-app memory-safety risk; low parser/runtime risk"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/jsonl-upload-preallocation-limits-459"
  validation:
    - "py -m pytest -q tests\\test_analytics_browser_jsonl_upload.py -> 14 passed, 1 warning"
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py -> 32 passed, 1 warning"
    - "py -m ruff check src tests -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan over changed files -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over changed files -> passed, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not add app-wide request-size middleware without routing back to Codex B."
    - "Do not dismiss CodeQL alerts without review and explicit approval."
    - "Do not change parser truth, analytics truth, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not persist or expose raw uploaded payloads, raw paths, raw hashes, local artifacts, secrets, stack traces, guard tokens, or private content."
    - "Do not stage, commit, push, open a PR, merge, close #459, or close #330 unless explicitly asked."
```
