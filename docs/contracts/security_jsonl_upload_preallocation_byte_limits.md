# Security JSONL Upload Preallocation Byte Limits Contract

## Module

`security_jsonl_upload_preallocation_byte_limits`

Plain English: this contract defines how the local app should reject oversized
browser JSONL uploads before Mythic Edge reads an entire uploaded file into a
new in-memory `bytes` object. This is an upload memory-safety hardening
contract, not an import redesign.

This is a Codex B contract artifact only. It does not implement code, change
parser truth, change analytics truth, persist raw uploaded payloads, add cloud
upload, or change workbook, webhook, Apps Script, Google Sheets, OpenAI, AI,
coaching, or production behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/459
- Parent security workflow: https://github.com/Tahjali11/Mythic-Edge/issues/330
- Recent prerequisite issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/458
- Recent prerequisite PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/624
- Contract artifact:
  `docs/contracts/security_jsonl_upload_preallocation_byte_limits.md`

## Tracker

Parent security workflow #330 remains open. This child issue must not close the
parent workflow by itself.

## Owning Layer

Local App / UI security and upload handling.

The local app backend owns whether an uploaded multipart file is accepted for
import, rejected as oversized, or rejected as malformed. Parser and analytics
layers own downstream interpretation and storage only after the upload has
passed local app request validation.

## Internal Project Area

Local App / UI.

Security is the risk lane, but the concrete code surface is the local app
browser upload endpoint.

## Truth Owner

Backend local app upload validation owns the byte-limit decision for
`POST /api/imports/jsonl/upload`.

Parser truth is unchanged. Analytics ingest truth is unchanged. Raw uploaded
JSONL bytes are local operator input and must not become durable repo,
analytics, parser, or diagnostic truth.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
browser multipart UploadFile streams
  -> local app capped upload reader
  -> BrowserJsonlUploadFile only after byte checks pass
  -> existing import_jobs validation
  -> existing legacy JSONL upload adapter and analytics ingest
```

Forbidden reverse flow:

- Parser, analytics, workbook, AI, or production logic must not decide upload
  byte-limit safety.
- Upload byte-limit changes must not reinterpret JSONL payload content.
- Upload byte-limit changes must not persist raw upload bytes.
- Upload byte-limit changes must not weaken the #458 local request guard.

## Files Owned By This Contract

- `docs/contracts/security_jsonl_upload_preallocation_byte_limits.md`

Future implementation may touch only the narrow files required to satisfy this
contract, expected to include:

- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_browser_jsonl_upload.py`
- possibly `tests/test_analytics_local_app_backend.py` if guard/order
  regression coverage is needed
- possibly a small new local app helper module if Codex C proves a helper is
  clearer than route-local functions

This contract does not authorize edits to:

- parser/state files;
- analytics schema or migration files;
- workbook, webhook, Apps Script, Google Sheets, OpenAI, AI, coaching, Line
  Tracer, production, fixture, corpus, or CI behavior;
- frontend upload UX unless Codex C discovers the existing frontend cannot
  preserve the current rejected-job response shape.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #459
- Parent issue #330
- Completed issue #458
- PR #624
- `docs/contracts/security_local_request_guard_mutating_loopback_routes.md`
- `docs/contracts/analytics_browser_jsonl_multi_file_upload.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `tests/test_analytics_browser_jsonl_upload.py`
- `tests/test_analytics_local_app_backend.py`

## Observed Current Behavior

Current route shape:

```text
POST /api/imports/jsonl/upload
```

The route is already guarded by the #458 local request guard dependency.

Observed upload path:

1. `backend.py` calls `await request.form()`.
2. It extracts `files` form parts and validates that they are `UploadFile`
   instances.
3. It builds `BrowserJsonlUploadFile` values.
4. During that build, it calls `content_bytes=await upload_file.read()`.
5. `import_jobs._validate_upload_request` later enforces:
   - `MAX_BROWSER_JSONL_UPLOAD_FILES`;
   - `MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES`;
   - `MAX_BROWSER_JSONL_UPLOAD_TOTAL_BYTES`.

The problem is step 4: the route reads the complete uploaded file into memory
before the per-file and aggregate byte limits are enforced.

Existing tests prove that oversize upload requests reject before database
creation. They do not prove that the backend stops reading before full
allocation.

## Required Guarantee

`POST /api/imports/jsonl/upload` must fail closed before Mythic Edge allocates
an entire oversized uploaded file as a `bytes` object.

Required guarantees:

1. The #458 local request guard runs before upload parsing or route-specific
   upload behavior.
2. File count validation happens before reading upload content.
3. Each uploaded file is read through a bounded/capped read path.
4. A single file larger than `MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES` is rejected
   as `upload_file_too_large` without reading the rest of that file.
5. A request whose cumulative accepted bytes exceed
   `MAX_BROWSER_JSONL_UPLOAD_TOTAL_BYTES` is rejected as
   `upload_total_size_too_large` without reading remaining upload content.
6. The route never constructs `BrowserJsonlUploadFile(content_bytes=...)` for a
   file that has already exceeded the allowed per-file or total byte budget.
7. All `UploadFile` objects and form resources are closed on success,
   rejection, and exception paths.
8. Rejected responses remain privacy-safe and do not include raw payloads, raw
   paths, raw hashes, internal digests, temporary paths, stack traces, local
   artifact paths, secrets, or guard tokens.

## Byte-Limit Enforcement Policy

The first implementation should enforce byte limits in the backend upload
route before creating `BrowserJsonlUploadFile` values.

Allowed enforcement shape:

```text
request guard
  -> multipart form extraction
  -> file part type/count validation
  -> capped async reads from each UploadFile
  -> construct BrowserJsonlUploadFile only for accepted byte buffers
  -> existing run_browser_jsonl_upload_import validation and import flow
```

The capped reader must use the existing import limit constants from
`import_jobs.py` unless Codex C proves a narrow import is needed to avoid a
cycle:

- `MAX_BROWSER_JSONL_UPLOAD_FILES`
- `MAX_BROWSER_JSONL_UPLOAD_FILE_BYTES`
- `MAX_BROWSER_JSONL_UPLOAD_TOTAL_BYTES`

The capped reader should read in bounded chunks. A reasonable first chunk size
is implementation detail, but it must be small enough that failure memory is
bounded by:

```text
already accepted bytes up to total limit + one read chunk
```

The reader may use framework-provided `UploadFile.size` only as an advisory
early rejection optimization. It must not rely on `size` as the only guard
because that field may be absent, stale, or framework-dependent.

## Allowed Implementation Strategy

Preferred strategy:

- Add a narrow backend helper, either route-local in `backend.py` or in a small
  local app helper module, that reads an `UploadFile` with:
  - per-file byte budget;
  - remaining aggregate byte budget;
  - chunked async reads;
  - explicit sanitized failure code.
- Keep `BrowserJsonlUploadFile` as the downstream in-memory adapter input only
  after a file passes capped read validation.
- Keep `_validate_upload_request` in `import_jobs.py` as defense-in-depth.
- Preserve existing import job response shape where feasible.

Codex C may choose a small new helper module if that makes tests clearer, but
it must not introduce a broad upload framework, storage service, middleware
stack, or generic file-management abstraction.

## Forbidden Implementation Strategies

Do not use these in the first #459 slice:

- app-wide request-size middleware as the primary solution, unless Codex C
  proves endpoint-local capped reads cannot satisfy the contract;
- broad FastAPI/Starlette middleware that changes unrelated route behavior;
- frontend-only size checks as a replacement for backend enforcement;
- reading the full upload into `bytes` and checking size afterward;
- writing uploaded raw JSONL to repo, app-data, temp staging, SQLite, logs, or
  diagnostics just to check size;
- returning raw filenames, raw paths, raw payload snippets, raw hashes,
  internal digests, local temp paths, framework stack traces, or guard values;
- changing the manual path-based import route;
- changing analytics schema, ingest semantics, parser behavior, parser state
  final reconciliation, match/game identity, deduplication, workbook/webhook
  behavior, Apps Script behavior, production behavior, OpenAI/model-provider
  behavior, AI/coaching behavior, or Line Tracer behavior.

## Middleware And Framework Boundary

This contract does not require an app-wide request/body-size middleware in the
first implementation.

Reason: the immediate issue is the route's explicit
`await upload_file.read()` before size validation. A targeted capped read fixes
that first bad value with less blast radius.

If Codex C discovers that Starlette/FastAPI multipart parsing stores uploaded
content in a way that still violates the security goal before route code can
run, Codex C must stop and route back to Codex B. App-wide request-size
middleware changes route semantics beyond this first contract and need a
separate implementation decision.

## Privacy-Safe Error Contract

The first implementation should preserve the existing local app import job
rejection envelope where feasible:

```json
{
  "object": "mythic_edge_local_app_manual_jsonl_import_job",
  "status": "rejected",
  "phase": "failed",
  "source": {
    "source_mode": "uploaded_file_batch",
    "path_echoed": false,
    "files_selected": 1,
    "files_accepted": 0,
    "files_rejected": 0
  },
  "errors": ["upload_file_too_large"]
}
```

Allowed error codes:

- `upload_files_required`
- `upload_files_too_many`
- `upload_file_invalid`
- `source_artifact_label_invalid`
- `upload_file_too_large`
- `upload_total_size_too_large`

Existing code currently uses `upload_total_size_too_large`; Codex C should
preserve that code for compatibility unless a contract-test finding proves it
must be renamed. Do not introduce a second spelling such as
`upload_total_too_large` in this issue.

HTTP status policy:

- Guard failures keep #458 statuses: `401`, `403`, or `503`.
- Upload validation failures may keep the existing `200` rejected-job response
  shape to avoid frontend churn.
- If Codex C proposes `413 Payload Too Large`, it must preserve a compatible
  sanitized JSON body and update frontend/tests accordingly. That is allowed
  only if it remains endpoint-local and does not change unrelated route
  behavior.

The response must not include:

- raw uploaded JSONL content;
- raw saved-event lines;
- raw `raw_bytes_hash` values;
- full local paths or browser fake paths;
- temporary paths;
- internal content digests;
- stack traces;
- SQL details;
- request guard token or header value;
- secrets, credentials, tokens, API keys, webhook URLs, spreadsheet IDs, or
  environment values.

## Relationship To #458 Local Request Guard

#459 inherits the #458 guard posture.

Required order:

1. Host/origin safety checks.
2. Guard header presence.
3. Guard header value comparison.
4. Route-specific multipart parsing and capped upload reads.
5. Existing import job validation/import behavior.

Route-specific behavior must not run when the guard fails. Oversized upload
handling must not weaken guard behavior, bypass the guarded route dependency,
or return guard token details in rejection responses.

## Backend Responsibility Boundary

Backend in scope:

- enforce file count before content reads;
- cap per-file reads;
- cap aggregate reads;
- close `UploadFile` and form resources;
- reuse existing constants and safe import job response vocabulary;
- preserve no-database-created behavior for rejected uploads;
- provide focused tests that prove the read path stops at the byte limit.

Backend out of scope:

- raw upload retention;
- upload quarantine;
- app-wide upload middleware unless routed back through B;
- cloud upload;
- endpoint authentication beyond the #458 local request guard;
- import schema redesign;
- persistent upload history;
- retry queues, cancellation, deletion, or destructive import controls.

## Frontend Responsibility Boundary

Frontend changes are not required if the backend preserves the existing
rejected-job response shape and error codes.

Frontend may be updated only if Codex C changes the upload failure status
handling in a narrow, compatible way. The frontend must not become the source
of truth for size enforcement; browser-side file-size checks are advisory UI
convenience only.

## Tests Required

Codex C must add or update focused tests proving:

1. Missing or invalid local request guard values still reject before upload
   route behavior.
2. Too many files reject before content reads where feasible.
3. A single oversized file rejects as `upload_file_too_large` before reading
   the whole file into memory.
4. Aggregate oversized uploads reject as `upload_total_size_too_large` before
   reading remaining file content.
5. Rejected oversized upload responses stay privacy-safe.
6. Rejected oversized uploads do not create app-data folders or SQLite files.
7. Valid upload behavior remains unchanged.
8. Existing malformed-upload privacy tests remain passing.

Test strategy:

- Keep or extend `tests/test_analytics_browser_jsonl_upload.py`.
- Use synthetic JSONL data only.
- For "before full allocation" proof, prefer a narrow fake async upload stream
  or helper-level unit test that records read calls and proves the helper stops
  after the allowed budget plus one bounded chunk.
- Do not use real private JSONL artifacts, raw Player.log excerpts, real local
  paths, private hashes, or generated app-data files as fixtures.

Required focused commands for Codex C:

```powershell
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m ruff check src tests
git diff --check
```

Codex C should also run path-scoped protected-surface and secret/private-marker
scans over changed files.

## Acceptance Criteria

- `POST /api/imports/jsonl/upload` remains guarded by #458 local request guard.
- The route no longer calls `await upload_file.read()` in a way that can read
  an unbounded full upload before byte validation.
- Per-file limit rejection happens before constructing
  `BrowserJsonlUploadFile` for the oversized file.
- Aggregate limit rejection stops reading once the total budget is exceeded.
- Existing safe error codes and response privacy rules are preserved.
- Valid uploaded JSONL behavior remains unchanged.
- Rejected uploads do not create app-data folders or SQLite files.
- No raw upload payloads, raw paths, raw hashes, internal digests, temp paths,
  stack traces, local-only artifacts, secrets, or guard values are exposed.
- No parser, analytics schema, workbook, webhook, Apps Script, Google Sheets,
  OpenAI, AI, coaching, Line Tracer, or production behavior changes occur.

## Validation For This Contract

Docs-only validation:

```powershell
git diff --check -- docs\contracts\security_jsonl_upload_preallocation_byte_limits.md
py tools\check_agent_docs.py
@'
docs/contracts/security_jsonl_upload_preallocation_byte_limits.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/security_jsonl_upload_preallocation_byte_limits.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

## Open Questions And Contract Risks

- `request.form()` may itself perform framework-level buffering or spooling.
  This contract fixes the explicit full `UploadFile.read()` allocation. If
  framework parsing remains a meaningful unbounded-memory risk, route back to B
  for middleware/request-size policy.
- Existing response behavior appears to use `200` with a rejected job payload.
  This contract preserves compatibility unless Codex C proves `413` is needed.
- Existing `import_jobs._validate_upload_request` remains useful
  defense-in-depth, but it must no longer be the first byte-limit check.

## Next Workflow Action

Next recommended role: Codex C: Module Implementer.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/459

Parent security workflow:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Contract:
docs/contracts/security_jsonl_upload_preallocation_byte_limits.md

Current intended base branch:
main

Goal:
Implement bounded/capped browser JSONL upload reads so
POST /api/imports/jsonl/upload rejects oversized uploads before allocating full
uploaded files into memory.

Before editing:
- Confirm branch/worktree status.
- Read issue #459, parent #330, and the contract.
- Inspect src/mythic_edge_parser/local_app/backend.py,
  src/mythic_edge_parser/local_app/import_jobs.py,
  tests/test_analytics_browser_jsonl_upload.py, and
  tests/test_analytics_local_app_backend.py.

Implement only:
- endpoint-local capped/chunked UploadFile reads before constructing
  BrowserJsonlUploadFile;
- per-file and aggregate rejection before full allocation;
- resource cleanup on success and rejection;
- focused tests proving oversize single-file and aggregate uploads stop early;
- privacy-safe rejection assertions.

Do not:
- change parser behavior or parser truth;
- change analytics schema or ingest truth;
- persist raw uploaded JSONL;
- expose raw payloads, raw paths, raw hashes, local artifacts, secrets, stack
  traces, guard tokens, or private content;
- add cloud upload or external writes;
- change workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior;
- add app-wide request-size middleware unless you route back to Codex B first.

Validation:
- py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
- py -m pytest -q tests\test_analytics_local_app_backend.py
- py -m ruff check src tests
- git diff --check
- path-scoped protected-surface scan over changed files
- path-scoped secret/private-marker scan over changed files

Final handoff:
- role performed
- issue/parent reviewed
- contract used
- implementation shape
- tests changed
- validation results
- protected-surface status
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/459"
  parent_security_workflow: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #459"
  target_artifact: "docs/implementation_handoffs/security_jsonl_upload_preallocation_byte_limits_comparison.md"
  contract_artifact: "docs/contracts/security_jsonl_upload_preallocation_byte_limits.md"
  risk_tier: "High security/local-app memory-safety risk; low parser/runtime risk"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/jsonl-upload-preallocation-limits-459"
  decision: "Use endpoint-local capped UploadFile reads before constructing BrowserJsonlUploadFile; preserve #458 request guard and existing privacy-safe import job response shape."
  validation:
    - "git diff --check -- docs\\contracts\\security_jsonl_upload_preallocation_byte_limits.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan over contract"
    - "path-scoped secret/private-marker scan over contract"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not add app-wide request-size middleware without routing back to Codex B."
    - "Do not change parser truth or analytics truth."
    - "Do not persist or expose raw uploaded payloads, raw paths, raw hashes, local artifacts, secrets, stack traces, guard tokens, or private content."
    - "Do not change workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
