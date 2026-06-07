# Contract Test Report: Analytics Browser JSONL Multi-File Upload

## Findings

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-214-001 | P1 | `fixed_state_followup` | verified_fixed | not_blocking | Original evidence: `docs/contracts/analytics_browser_jsonl_multi_file_upload.md:415` requires non-file form fields in the `files` slot to reject safely, and `docs/contracts/analytics_browser_jsonl_multi_file_upload.md:599` requires sanitized rejected `ManualImportJob` responses when possible. The original route used FastAPI parameter validation before the app sanitizer could run, so a direct probe returned HTTP 422 with submitted content echoed in the default validation body. | `src/mythic_edge_parser/local_app/backend.py:86` now parses multipart form data inside the route, `src/mythic_edge_parser/local_app/backend.py:94` through `src/mythic_edge_parser/local_app/backend.py:100` routes non-file values to `reject_browser_jsonl_upload_import(...)`, and `tests/test_analytics_browser_jsonl_upload.py:277` through `tests/test_analytics_browser_jsonl_upload.py:294` covers the sanitized rejection. A direct TestClient repro now returns HTTP 200 with `status = rejected`, `errors = ["upload_file_invalid"]`, and no submitted value echo. | F |
| CT-214-002 | P2 | `fixed_state_followup` | verified_fixed | not_blocking | Original evidence: the frontend selected-upload display blocked only a narrower marker set, despite `docs/contracts/analytics_browser_jsonl_multi_file_upload.md:377` through `docs/contracts/analytics_browser_jsonl_multi_file_upload.md:391` forbidding display of API keys, access tokens, passwords, bearer strings, hook/script markers, and other private markers. | `frontend/src/App.tsx:617` through `frontend/src/App.tsx:632` now uses the broader private-marker list, and `frontend/src/App.test.tsx:194` through `frontend/src/App.test.tsx:216` verifies selected upload names with `api_key`, `apikey`, `access_token`, `bearer `, `password`, `hooks.`, and `script.google.com` render as `<selected_jsonl>` instead of raw filenames. | F |

## Issue / Tracker

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/214
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
- Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207
- Branch: `codex/analytics-foundation`
- Risk tier: High

## Contract And Handoffs Reviewed

- Contract: `docs/contracts/analytics_browser_jsonl_multi_file_upload.md`
- Implementation handoff: `docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_comparison.md`
- Fixer handoff: `docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_fixer.md`
- Role docs: `docs/agent_threads/review.md`, `docs/agent_threads/contract_test.md`
- Template: `docs/templates/contract_test_report.md`

## Report Lifecycle

`report_lifecycle`: `followup_after_fixer`

## Files Reviewed

- `pyproject.toml`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `tests/test_analytics_browser_jsonl_upload.py`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/src/App.css`

## Contract Matches

- Existing `POST /api/imports/jsonl` single-file and `source_paths` behavior remains present.
- `POST /api/imports/jsonl/upload` exists and accepts multipart uploads.
- Upload jobs use `source_mode = "uploaded_file_batch"`.
- Upload validation covers no files, too many files, per-file size, total size, blank names, non-`.jsonl` names, zero-byte files, non-file form fields, and unsafe source labels.
- Accepted uploaded files are adapted in memory through `LegacyJsonlUploadSource`, not copied into repo or app-data as raw JSONL files.
- Uploaded files replay through one adapter batch with deterministic ordering and cross-file saved-event raw-hash dedupe.
- Upload responses reuse the existing `ManualImportJob` object, issue #212 quality fields, and issue #213 source-artifact summary shape.
- `python-multipart>=0.0.9,<1` was added only to the existing `app` and `dev` optional dependency groups.
- Frontend selected-upload-file display now redacts the private-marker classes expected by the contract/backend policy.
- No destructive import, database, job, launcher, watcher, Sheets, AI, production, reset, wipe, retry, or delete route/control was added.
- No analytics SQLite schema or migration file was changed.

## Contract Mismatches

- None remaining after Codex D follow-up.

## Missing Tests Or Safeguards

- None remaining for CT-214 findings. Full repository test suite and GitHub Actions remain unverified.

## Validation Run

```powershell
git status --short --branch
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
<direct TestClient probe for non-file files form field>
py -m pytest -q tests\test_analytics_browser_jsonl_upload.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_legacy_jsonl_artifact_adapter.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
Remove-Item -Recurse -Force frontend\dist
py -m ruff check src tests tools
git diff --check
<path-scoped protected-surface scan>
<path-scoped secret/private-marker scan>
```

Results:

- Branch: `codex/analytics-foundation`; `HEAD...origin/codex/analytics-foundation` was `0 0`.
- Direct TestClient probe for a non-file `files` form field -> HTTP 200 sanitized rejected `ManualImportJob`, `errors = ["upload_file_invalid"]`, no submitted value echo.
- `py -m pytest -q tests\test_analytics_browser_jsonl_upload.py` -> 11 passed, 1 third-party FastAPI/Starlette warning.
- `py -m pytest -q tests\test_analytics_manual_jsonl_import.py tests\test_analytics_legacy_jsonl_artifact_adapter.py` -> 29 passed, 1 third-party FastAPI/Starlette warning.
- `py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py` -> 35 passed, 1 third-party FastAPI/Starlette warning.
- `npm --prefix frontend ci` -> passed, 113 packages, 0 vulnerabilities.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> 3 files passed, 28 tests passed.
- `npm --prefix frontend run build` -> passed; generated `frontend/dist` removed after validation.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- Path-scoped protected-surface scan after report update -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan after report update -> passed, forbidden 0, warnings 0.

## Protected-Surface Status

Path-scoped protected-surface scan passed for the #214 touched path set plus this report. The reviewed diff did not change parser behavior, saved-event replay semantics, parser state final reconciliation, parser event classes, analytics migrations, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, Match Journal behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, production behavior, or destructive controls.

## Secret / Private-Marker Status

Path-scoped secret/private-marker scan passed for the reviewed #214 path set plus this report. The previous behavioral privacy findings are verified fixed by code-path reproduction and regression tests.

## Generated Artifact Status

`npm --prefix frontend run build` generated ignored frontend build output, and it was removed. `git status --short --branch` shows no changed or untracked generated SQLite DB/WAL/SHM/journal files, raw JSONL artifacts, raw Player.log files, runtime status files, failed-post payloads, workbook exports, screenshots, or `node_modules` files in the #214 working-tree diff.

## Forbidden Scope

Forbidden scope touched: false.

## Recommendation

Approve for Codex F.

Codex D fixed the two review findings without changing parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior. The next role should submit only the reviewed #214 files.

## Next Workflow Action

Next role: Codex F: Module Submitter

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #214.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/214

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Artifacts:
- docs/contracts/analytics_browser_jsonl_multi_file_upload.md
- docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_comparison.md
- docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_fixer.md
- docs/contract_test_reports/analytics_browser_jsonl_multi_file_upload.md

Task:
Stage only the reviewed #214 browser JSONL multi-file upload files, commit them, push the branch, and open or update a draft PR targeting the agreed analytics integration branch. Exclude unrelated/generated/private artifacts.

Reviewed #214 files include:
- pyproject.toml
- src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/import_jobs.py
- tests/test_analytics_browser_jsonl_upload.py
- tests/test_analytics_legacy_jsonl_artifact_adapter.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/api.test.ts
- frontend/src/App.tsx
- frontend/src/App.test.tsx
- frontend/src/App.css
- docs/contracts/analytics_browser_jsonl_multi_file_upload.md
- docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_comparison.md
- docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_fixer.md
- docs/contract_test_reports/analytics_browser_jsonl_multi_file_upload.md

Suggested pre-submit validation:
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
Run path-scoped protected-surface and secret/private-marker scans over the staged #214 paths.

Do not target main, close issues, merge, deploy, change production behavior, or stage unrelated/generated/private artifacts unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/214"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/analytics_browser_jsonl_multi_file_upload.md"
  review_artifact: "docs/contract_test_reports/analytics_browser_jsonl_multi_file_upload.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_browser_jsonl_multi_file_upload_fixer.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  findings_fixed:
    - "CT-214-001: non-file multipart files field sanitized rejection verified fixed."
    - "CT-214-002: frontend selected upload filename private-marker redaction verified fixed."
  validation:
    - "direct non-file multipart repro -> sanitized rejected ManualImportJob, no submitted value echo"
    - "browser upload pytest -> 11 passed, 1 third-party warning"
    - "manual import + legacy adapter pytest -> 29 passed, 1 third-party warning"
    - "parser-normalized ingest + backend pytest -> 35 passed, 1 third-party warning"
    - "frontend npm ci/typecheck/test/build -> passed; generated dist removed"
    - "ruff -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
  forbidden_scope_touched: false
  recommendation: "Route to Codex F."
  stop_conditions:
    - "Do not target main."
    - "Do not retain uploaded raw JSONL files after import."
    - "Do not expose raw payloads, raw paths, raw hashes, internal content digests, temporary paths, stack traces, secrets, webhook URLs, API keys, or private local artifacts."
    - "Do not add destructive import, database, job, launcher, or UI actions."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
```
