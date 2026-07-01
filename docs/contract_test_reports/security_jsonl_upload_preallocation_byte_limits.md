# Security JSONL Upload Preallocation Byte Limits Contract Test Report

## Findings

No blocking findings.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-459-001 | N/A | `not_reproduced` | The implementation satisfies the contract's route-level capped-read requirements. | not_blocking | The contract required upload validation before unbounded route-level `UploadFile.read()` allocation. | `src/mythic_edge_parser/local_app/backend.py` uses guarded route dependencies, validates file parts, calls `_build_browser_jsonl_upload_files`, and closes upload/form resources. `_read_browser_jsonl_upload_file` reads at most the remaining byte budget plus one bounded chunk and raises symbolic errors. Focused tests prove too-many, per-file, and aggregate rejection before full content reads. | F |

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/459

## Parent Security Workflow

https://github.com/Tahjali11/Mythic-Edge/issues/330

## Contract

`docs/contracts/security_jsonl_upload_preallocation_byte_limits.md`

## Implementation Under Test

- Branch: `codex/jsonl-upload-preallocation-limits-459`
- Base: `origin/main`
- Implementation handoff:
  `docs/implementation_handoffs/security_jsonl_upload_preallocation_byte_limits_comparison.md`
- Changed files reviewed:
  - `docs/contracts/security_jsonl_upload_preallocation_byte_limits.md`
  - `docs/implementation_handoffs/security_jsonl_upload_preallocation_byte_limits_comparison.md`
  - `src/mythic_edge_parser/local_app/backend.py`
  - `tests/test_analytics_browser_jsonl_upload.py`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

`POST /api/imports/jsonl/upload` must reject oversized browser JSONL uploads
before route code reads an entire uploaded file into a new in-memory `bytes`
object. The route must preserve the #458 local request guard, use existing
import size constants, keep rejection responses symbolic and privacy-safe, keep
valid upload behavior compatible, and avoid parser, analytics, workbook,
webhook, Apps Script, Sheets, OpenAI, AI, coaching, Line Tracer, and production
behavior changes.

## Internal Project Area Reviewed

Local App / UI security and upload handling.

## Bridge-Code Status Reviewed

`shared_support`

The upload route remains a bridge from browser multipart uploads into the
existing `BrowserJsonlUploadFile` adapter input. The reviewed implementation
adds route-local byte-budget validation before constructing that adapter input.

## Checks Run

```powershell
git fetch --prune origin
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
git rev-parse HEAD
git rev-parse origin/main
gh issue view 459 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m ruff check src tests
git diff --check
py tools\check_agent_docs.py
@'
docs/contracts/security_jsonl_upload_preallocation_byte_limits.md
docs/implementation_handoffs/security_jsonl_upload_preallocation_byte_limits_comparison.md
src/mythic_edge_parser/local_app/backend.py
tests/test_analytics_browser_jsonl_upload.py
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/security_jsonl_upload_preallocation_byte_limits.md
docs/implementation_handoffs/security_jsonl_upload_preallocation_byte_limits_comparison.md
src/mythic_edge_parser/local_app/backend.py
tests/test_analytics_browser_jsonl_upload.py
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
new-file whitespace/final-newline check over untracked #459 docs artifacts
```

## Results

- Branch/worktree: correct #459 checkout.
- Branch freshness: `HEAD` and `origin/main` both resolve to
  `ed82d3f29b2bccb2c6882c9b5a0ce6b0afb88804`; sync is `0 0`.
- Issue #459: open.
- Focused browser JSONL upload tests: passed, `14 passed`, `1 warning`.
- Adjacent local app backend tests: passed, `32 passed`, `1 warning`.
- Ruff: passed.
- `git diff --check`: passed.
- Agent docs: passed.
- Path-scoped protected-surface scan: passed, `forbidden 0`, `warnings 0`.
- Path-scoped secret/private-marker scan: passed, `forbidden 0`,
  `warnings 0`.
- New-file whitespace/final-newline check: passed.

Warnings were the existing FastAPI/Starlette `TestClient` deprecation warning.

## Confirmed Contract Matches

- The upload route remains guarded by the #458 local request guard dependency:
  `src/mythic_edge_parser/local_app/backend.py` lines 284-285.
- Existing guard coverage verifies every guarded mutating POST route rejects
  missing, blank, or invalid guard values before route behavior:
  `tests/test_analytics_local_app_backend.py` lines 183-214.
- Non-file form parts and invalid labels return symbolic rejected-job payloads
  without raw submitted value echo:
  `src/mythic_edge_parser/local_app/backend.py` lines 294-317.
- Upload files and form resources are closed in a `finally` block after success
  or route-level rejection:
  `src/mythic_edge_parser/local_app/backend.py` lines 318-321.
- File count validation happens before content reads:
  `src/mythic_edge_parser/local_app/backend.py` lines 339-343 and
  `tests/test_analytics_browser_jsonl_upload.py` lines 158-168.
- `BrowserJsonlUploadFile` is constructed only after capped read validation
  returns accepted bytes:
  `src/mythic_edge_parser/local_app/backend.py` lines 345-356.
- Per-file and aggregate reads use existing `import_jobs` constants, read at
  the smaller of chunk size or remaining budget plus one byte, and raise
  symbolic errors:
  `src/mythic_edge_parser/local_app/backend.py` lines 360-382.
- Single-file oversized behavior stops before full read and returns
  `upload_file_too_large`:
  `tests/test_analytics_browser_jsonl_upload.py` lines 171-182.
- Aggregate oversized behavior stops before reading remaining file content and
  returns `upload_total_size_too_large`:
  `tests/test_analytics_browser_jsonl_upload.py` lines 185-201.
- Route-level rejected oversize uploads preserve the rejected-job envelope and
  do not create app-data folders or SQLite files:
  `tests/test_analytics_browser_jsonl_upload.py` lines 368-406.
- Valid upload behavior, duplicate/hash privacy, malformed upload privacy, and
  no destructive route additions remain covered by the focused browser upload
  tests.
- Existing downstream `import_jobs._validate_upload_request` byte-limit checks
  remain as defense-in-depth.
- No raw uploaded JSONL payloads, raw paths, raw hashes, guard tokens, temp
  paths, stack traces, local-only artifacts, or secrets were introduced in the
  reviewed response paths or artifacts.
- No parser truth, analytics schema, workbook schema, webhook payload, Apps
  Script, Sheets, OpenAI, AI, coaching, Line Tracer, CI, or production behavior
  changes were found.

## Contract Mismatches

None.

## Missing Tests

None blocking.

The contract's framework-level multipart buffering caveat remains outside this
implementation slice. The current tests prove the explicit route-level
`UploadFile.read()` allocation is capped, not that Starlette/FastAPI multipart
parsing itself cannot buffer or spool before route code runs.

## Drift Notes

- Repo drift: none found.
- Local-data drift: none found.
- Issue lifecycle drift: none found; #459 remains open.
- PR lifecycle drift: no PR was inspected or created in this Codex E pass.
- GitHub CodeQL closure: not claimed. Local validation is clean, but GitHub
  CodeQL or code-scanning closure remains unverified until submitted and rerun.

## Protected-Surface Status

Passed. Path-scoped protected-surface scan returned `forbidden 0`,
`warnings 0`.

## Secret And Private-Artifact Status

Passed. Path-scoped secret/private-marker scan returned `forbidden 0`,
`warnings 0`.

No generated/private/local artifacts were staged or committed by this review.

## Remaining Risks

- Framework-level multipart parsing may still buffer or spool request data
  before route code can enforce byte budgets. The contract explicitly leaves
  that as a route-back-to-B question if it becomes unacceptable.
- GitHub CodeQL/code-scanning closure is unverified until a PR is pushed and
  GitHub reruns the relevant checks.
- CI was not run in this local Codex E pass.

## Recommendation

Approve for Codex F submitter routing.

Codex F should stage only the reviewed #459 files and this report, commit,
push, and open a draft PR. Codex F/G should not claim CodeQL closure until
GitHub reruns code scanning.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #459.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/459

Parent security workflow:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Branch:
codex/jsonl-upload-preallocation-limits-459

Base / PR target:
origin/main

Contract:
docs/contracts/security_jsonl_upload_preallocation_byte_limits.md

Implementation handoff:
docs/implementation_handoffs/security_jsonl_upload_preallocation_byte_limits_comparison.md

Review artifact:
docs/contract_test_reports/security_jsonl_upload_preallocation_byte_limits.md

Goal:
Submit the reviewed #459 local-app upload byte-limit hardening package. Stage
only the reviewed files, commit, push, and open a draft PR. Preserve the
route-local capped-read scope and do not claim GitHub CodeQL closure until
GitHub reruns code scanning.

Reviewed files:
- docs/contracts/security_jsonl_upload_preallocation_byte_limits.md
- docs/implementation_handoffs/security_jsonl_upload_preallocation_byte_limits_comparison.md
- docs/contract_test_reports/security_jsonl_upload_preallocation_byte_limits.md
- src/mythic_edge_parser/local_app/backend.py
- tests/test_analytics_browser_jsonl_upload.py

Validation before submit:
git fetch --prune origin
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/main
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_local_app_backend.py
py -m ruff check src tests
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over reviewed files
path-scoped secret/private-marker scan over reviewed files

Do not:
- stage unrelated files;
- dismiss CodeQL alerts;
- close #459 or #330;
- merge PRs;
- change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/Line Tracer/production behavior;
- expose or commit raw uploaded JSONL, raw paths, raw hashes, secrets, local artifacts, SQLite files, runtime logs, or generated/private artifacts.

Final output:
- branch, commit, and draft PR URL
- validation run and result
- protected-surface status
- secret/private-marker status
- generated/private artifact status
- whether forbidden scope was touched
- workflow_handoff block routing to Codex G after draft PR creation
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/459"
  parent_security_workflow: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/security_jsonl_upload_preallocation_byte_limits.md"
  implementation_handoff: "docs/implementation_handoffs/security_jsonl_upload_preallocation_byte_limits_comparison.md"
  review_artifact: "docs/contract_test_reports/security_jsonl_upload_preallocation_byte_limits.md"
  risk_tier: "High security/local-app memory-safety risk; low parser/runtime risk"
  base_branch: "origin/main"
  target_branch: "main_after_review_and_explicit_merge_approval"
  branch: "codex/jsonl-upload-preallocation-limits-459"
  verdict: "approved_for_codex_f_submitter"
  validation:
    - "py -m pytest -q tests\\test_analytics_browser_jsonl_upload.py -> 14 passed, 1 warning"
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py -> 32 passed, 1 warning"
    - "py -m ruff check src tests -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  generated_private_artifacts_kept: false
  forbidden_scope_touched: false
  remaining_risks:
    - "Framework-level multipart parsing may still buffer or spool before route code; contract leaves this as a separate B-thread question if unacceptable."
    - "GitHub CodeQL/code-scanning closure is not claimed until PR submission and GitHub rerun evidence."
    - "CI not run locally."
  next_recommended_role: "Codex F: Module Submitter"
```
