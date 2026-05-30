# Analytics Manual JSONL Import UI Job-Status Fixer Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/211>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/204>

## Umbrella Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/207>

## Contract

`docs/contracts/analytics_manual_jsonl_import_ui_job_status.md`

## Review Artifact

`docs/contract_test_reports/analytics_manual_jsonl_import_ui_job_status.md`

## Implementation Handoff Used

`docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md`

## Role Performed

Codex D: Module Fixer.

## Branch

`codex/analytics-foundation`

Branch relation observed:

```text
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0
```

## Finding Fixed

P1: non-object `POST /api/imports/jsonl` bodies could echo raw submitted input through FastAPI's default 422 validation details before the import sanitizer ran.

Fault category: route-level request validation happened before the contract-owned sanitizer boundary.

## What Changed

`POST /api/imports/jsonl` now accepts the raw JSON request body as `object` and passes it into `run_manual_jsonl_import(...)`. The import job sanitizer then handles scalar, list, and otherwise non-mapping bodies as a sanitized rejected job with `source_request_invalid`.

This keeps invalid non-object bodies inside the existing sanitized job response shape and avoids FastAPI's default validation detail echo.

## Files Changed By This Fixer Pass

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_fixer.md`

Existing dirty issue #211 files remain in the working tree and were not staged. Pre-existing dirty launcher files and the untracked `Start Mythic Edge Dev App.cmd` were left untouched.

## Code Changed

Runtime code changed: yes, limited to the local app manual import route and request sanitizer type boundary.

Behavior surface:

- changed route body annotation from `dict[str, object]` to `object`
- widened `run_manual_jsonl_import(...)` and `_validate_source_request(...)` input type to `object`
- preserved the existing `Mapping` check inside `_validate_source_request(...)`
- preserved object-shaped valid and invalid import behavior
- preserved app-data/database creation only after source validation and adapter success

No parser behavior, adapter replay semantics, analytics ingest semantics, SQLite schema, workbook schema, webhook payload shape, Apps Script behavior, Sheets/Match Journal/OpenAI/AI/coaching/production behavior, or deployment behavior changed.

## Tests Added Or Updated

`tests/test_analytics_manual_jsonl_import.py` now proves scalar path-like bodies, list path-like bodies, and numeric non-object bodies:

- return a sanitized rejected job;
- use only `source_request_invalid` as the error category;
- do not echo the raw submitted path-like value;
- do not create app-data folders or SQLite database files.

The focused regression failed before the implementation fix and passed afterward.

## Interface Changes

None.

No route path, response schema, frontend API shape, parser interface, analytics schema, workbook column, webhook field, environment variable contract, dependency policy, or production entrypoint changed.

## Validation Run

```powershell
git status --short --branch
# codex/analytics-foundation...origin/codex/analytics-foundation

git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
# 0 0

py -m pytest -q tests\test_analytics_manual_jsonl_import.py
# before fix: failed on FastAPI 422 for scalar/list/non-object request bodies
# after fix: 12 passed, 1 third-party FastAPI/Starlette deprecation warning

py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
# 43 passed, 1 third-party FastAPI/Starlette deprecation warning

py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_field_evidence_ingest.py
# 77 passed

npm --prefix frontend run typecheck
# passed

npm --prefix frontend run test -- --run
# 3 files passed, 18 tests passed

npm --prefix frontend run build
# passed

py -m ruff check src tests tools
# passed

git diff --check
# passed

py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, changed_paths 16, forbidden 0, warnings 0

py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, scanned_paths 16, forbidden 0, warnings 0
```

Generated artifact cleanup:

- `frontend/dist/` was produced by build validation and removed afterward.
- `src/mythic_edge_parser/local_app/__pycache__/` and `tests/__pycache__/` were removed after validation.

## Protected-Surface Status

No forbidden protected surfaces were touched.

No changes were made to parser behavior, adapter replay semantics, analytics ingest semantics, SQLite schema/migrations, parser state final reconciliation, parser event classes, event kind values, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, Match Journal behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, production behavior, deployment behavior, secrets, environment variables, generated local data, runtime state artifacts, retry-queue artifacts, workbook exports, or generated SQLite files.

## Secret / Private-Marker Status

The fix is a runtime response-sanitization safeguard. No raw private path, raw log content, raw JSONL content, secret, webhook URL, API key, token, or OAuth state was added by this fixer pass.

The path-scoped secret/private-marker scan over the issue #211 package passed with forbidden `0` and warnings `0`.

## Generated Artifact Status

- `frontend/node_modules/` exists locally and remains ignored.
- `frontend/dist/` was removed after build validation.
- local Python cache folders produced by validation were removed.
- No generated SQLite database, WAL, SHM, journal, raw JSONL artifact, runtime output, retry artifact, workbook export, screenshot, or generated data artifact was detected as changed or untracked.

## Still Unverified

- Full repository test suite was not run.
- Repo-wide secret/private-marker scan was not rerun because the review already recorded out-of-scope pre-existing findings; this fixer pass uses path-scoped scans.

## Reviewer Focus

Codex E should verify:

- scalar/list/non-object `POST /api/imports/jsonl` request bodies no longer receive FastAPI default 422 validation details;
- path-like submitted scalar/list values are not echoed in the response;
- rejected non-object request bodies do not create app-data folders or database files;
- object-shaped valid and invalid import behavior remains unchanged;
- no parser/adapter/ingest/schema/frontend protected behavior changed beyond this route sanitizer boundary.

## Next Workflow Action

Next role: Codex E confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #211.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/211

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_manual_jsonl_import_ui_job_status.md

Implementation handoff:
docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md

Prior review artifact:
docs/contract_test_reports/analytics_manual_jsonl_import_ui_job_status.md

Fixer handoff:
docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_fixer.md

Review only the Codex D fix for the P1 finding:
- non-object POST /api/imports/jsonl bodies could echo raw submitted input through FastAPI default 422 validation details before the sanitizer ran.

Confirm:
- scalar/list/non-object request bodies are handled by the import sanitizer or safe route-level response, not FastAPI default validation details;
- synthetic path-like submitted values are not echoed;
- invalid non-object bodies do not create app-data folders or database files;
- object-shaped valid and invalid import behavior is preserved;
- no parser behavior, adapter replay semantics, analytics ingest semantics, SQLite schema, workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior, or deployment behavior changed.

Run:
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
py -m ruff check src tests tools
git diff --check

Also run path-scoped protected-surface and secret/private-marker checks over the issue #211 touched files.

Route to Codex F only if the P1 is resolved and no new blocking findings remain.
```

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/211"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_manual_jsonl_import_ui_job_status.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md"
  review_artifact: "docs/contract_test_reports/analytics_manual_jsonl_import_ui_job_status.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_fixer.md"
  finding_fixed:
    - severity: "P1"
      summary: "Non-object POST /api/imports/jsonl bodies could echo raw submitted input through FastAPI default 422 validation details before the sanitizer ran."
  validation:
    - "branch sync -> 0 0"
    - "manual import backend tests -> 12 passed, 1 third-party warning"
    - "adapter/ingest/backend slice -> 43 passed, 1 third-party warning"
    - "gameplay/opponent/field-evidence ingest slice -> 77 passed"
    - "frontend npm typecheck/test/build -> passed"
    - "ruff -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
    - "generated frontend dist and Python cache artifacts removed"
  forbidden_scope_touched: false
  next_thread: "E"
  next_role: "Codex E confirmation thread"
```
