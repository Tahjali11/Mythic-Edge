# Implementation Handoff: Analytics Browser JSONL Multi-File Upload Fixer

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/214

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/analytics_browser_jsonl_multi_file_upload.md`

## Role Performed

Codex D: Module Fixer

## Source Finding

`docs/contract_test_reports/analytics_browser_jsonl_multi_file_upload.md`

Findings fixed:

- CT-214-001: non-file multipart `files` fields bypassed the sanitized rejected `ManualImportJob` path and could echo submitted input through FastAPI default 422 validation details.
- CT-214-002: frontend selected upload filename display did not cover all private-marker classes required by the contract/backend policy.

## What Changed

- The upload route now parses multipart form data inside the route instead of declaring `files` as a FastAPI-validated `list[UploadFile]`.
- Non-file values submitted in the `files` slot now return a sanitized rejected `ManualImportJob` with `upload_file_invalid`.
- Upload form `UploadFile` handles are closed on all route paths.
- Frontend selected upload filename display now uses the broader private-marker policy used by backend upload summaries.

## Files Changed

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `tests/test_analytics_browser_jsonl_upload.py`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_fixer.md`

## Code Changed

Runtime code changed in the local app upload boundary only:

- `backend.py`: manual multipart parsing for `POST /api/imports/jsonl/upload`.
- `import_jobs.py`: explicit rejected upload helper for sanitized route-level rejection.
- `App.tsx`: selected upload filename redaction marker list expanded.

No parser behavior, saved-event replay semantics, parser state final reconciliation, analytics schema/migrations, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, Match Journal behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, production behavior, or destructive controls were changed.

## Tests Added Or Updated

- Backend regression test for non-file multipart values in the `files` slot.
- Frontend regression test for selected upload names containing `api_key`, `apikey`, `access_token`, `bearer `, `password`, `hooks.`, and `script.google.com` private markers.

## Interface Changes

- No public payload shape change.
- No workbook/schema/webhook/deployment interface change.
- Internal helper added: `reject_browser_jsonl_upload_import(...)`.
- Upload route implementation changed from framework-validated file parameters to route-local multipart parsing to preserve the existing sanitized job response contract.

## Validation Run

```powershell
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_legacy_jsonl_artifact_adapter.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
```

Results:

- `py -m pytest -q tests\test_analytics_browser_jsonl_upload.py` -> 11 passed, 1 third-party FastAPI/Starlette warning.
- `py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_legacy_jsonl_artifact_adapter.py` -> included in combined rerun with upload tests: 40 passed, 1 third-party FastAPI/Starlette warning.
- `py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py` -> 35 passed, 1 third-party FastAPI/Starlette warning.
- `npm --prefix frontend ci` -> passed, 113 packages audited, 0 vulnerabilities.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> 3 files passed, 28 tests passed.
- `npm --prefix frontend run build` -> passed; generated `frontend/dist` was removed after validation.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- Path-scoped protected-surface scan over the #214 path set plus this fixer handoff -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over the #214 path set plus this fixer handoff -> passed, forbidden 0, warnings 0.

## Still Unverified

- Live GitHub issue/PR updates were not performed.
- No production or external workbook/webhook/App Script surfaces were exercised.
- No final submitter/deployer readiness was attempted.

## Reviewer Focus

Codex E should verify:

- non-file multipart `files` values no longer produce FastAPI 422 bodies with echoed `input`;
- sanitized rejected job shape is appropriate for `upload_file_invalid`;
- frontend marker policy is sufficiently aligned with backend private-marker classes;
- no raw upload payload, raw path, raw hash, temporary path, or internal digest exposure was introduced.

## Next Workflow Action

Next role: Codex E confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #214.

Review the Codex D fixer handoff:
docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_fixer.md

Source contract:
docs/contracts/analytics_browser_jsonl_multi_file_upload.md

Prior review artifact:
docs/contract_test_reports/analytics_browser_jsonl_multi_file_upload.md

Confirm whether CT-214-001 and CT-214-002 are fixed without forbidden scope changes. Pay special attention to sanitized rejection of non-file multipart files fields, frontend selected-upload filename private-marker redaction, raw path/payload/hash exposure, generated artifact retention, and protected-surface boundaries.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/214"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  source_artifact: "docs/contracts/analytics_browser_jsonl_multi_file_upload.md"
  review_artifact: "docs/contract_test_reports/analytics_browser_jsonl_multi_file_upload.md"
  target_artifact: "docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_fixer.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  findings_fixed:
    - "CT-214-001: non-file multipart files field now rejects through sanitized ManualImportJob response."
    - "CT-214-002: selected upload filename display now redacts broader private-marker classes."
  forbidden_scope_touched: false
```
