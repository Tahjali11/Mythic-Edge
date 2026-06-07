# Contract Test Report: Analytics Legacy JSONL Batch Import

## Findings

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-213-001 | P2 | `fixed_state_followup` | verified_fixed | not_blocking | `docs/contracts/analytics_legacy_jsonl_batch_import.md:414` requires non-string `source_paths` entries to reject, and `docs/contracts/analytics_legacy_jsonl_batch_import.md:862` through `docs/contracts/analytics_legacy_jsonl_batch_import.md:864` requires backend validation tests for non-string entries before database creation. `tests/test_analytics_manual_jsonl_import.py:280` through `tests/test_analytics_manual_jsonl_import.py:295` previously covered many invalid batch shapes but did not include a non-string array entry. | `tests/test_analytics_manual_jsonl_import.py:289` and `tests/test_analytics_manual_jsonl_import.py:290` now cover integer and object entries, and the test asserts safe rejection before app-data/database creation. `py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_manual_jsonl_import.py` passed with 26 tests. | F |
| CT-213-002 | P2 | `fixed_state_followup` | verified_fixed | not_blocking | `docs/contracts/analytics_legacy_jsonl_batch_import.md:849` requires adapter coverage proving a malformed one-file-in-batch failure does not produce replay rows or expose raw payload/path/hash output. Batch tests previously covered successful and degraded behavior, while malformed-file coverage was only exercised through the single-file adapter path. | `tests/test_analytics_legacy_jsonl_artifact_adapter.py:413` now invokes `adapt_legacy_jsonl_file_batch(...)` with malformed selected input and asserts no replay summaries plus no raw line, payload marker, raw hash, or full local path in the exception. The focused adapter/manual-import pytest command passed. | F |
| CT-213-003 | P2 | `fixed_state_followup` | verified_fixed | not_blocking | `docs/contracts/analytics_legacy_jsonl_batch_import.md:886` through `docs/contracts/analytics_legacy_jsonl_batch_import.md:889` require frontend coverage for batch submit, clearing raw paths, safe batch count/quality/per-file display, and rejected, failed, degraded, and succeeded batch states. Frontend tests previously covered batch success and exact-one disabling but not rejected/failed/degraded batch job states. | `frontend/src/App.test.tsx:150`, `frontend/src/App.test.tsx:171`, and `frontend/src/App.test.tsx:197` now cover rejected, failed, and degraded batch states while asserting raw submitted paths are cleared/not displayed. `npm --prefix frontend run test -- --run` passed with 24 tests. | F |

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/213

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

Related quality issue: https://github.com/Tahjali11/Mythic-Edge/issues/212

## Contract

`docs/contracts/analytics_legacy_jsonl_batch_import.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Implementation handoff: `docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md`

Fixer handoff: `docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_fixer.md`

Files reviewed:

- `docs/contracts/analytics_legacy_jsonl_batch_import.md`
- `docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/src/App.css`
- `frontend/src/status.ts`

## Report Lifecycle

`report_lifecycle`: `followup_after_fixer`

## Contract Summary

Issue #213 adds local developer-app support for importing an explicit batch of legacy generated JSONL event archives as one parser-normalized replay/import unit. The feature must preserve parser truth ownership, avoid trusting legacy derived fields, avoid raw path/payload/hash exposure, keep imports local and non-destructive, avoid SQLite schema changes, and reuse the #212 quality summary shape.

## Checks Run

```powershell
git fetch --prune
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
git status --short --branch
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
Remove-Item -Recurse -Force frontend\dist
py -m ruff check src tests tools
git diff --check
<changed-paths> | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
<changed-paths> | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
py tools\check_secret_patterns.py --all
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
Remove-Item -Recurse -Force frontend\dist
py -m ruff check src tests tools
```

## Results

- Branch check: `codex/analytics-foundation`; `HEAD...origin/codex/analytics-foundation` was `0 0`.
- `py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py` -> 11 passed.
- `py -m pytest -q tests\test_analytics_manual_jsonl_import.py` -> 14 passed, with one third-party deprecation warning.
- `py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py` -> 35 passed, with one third-party deprecation warning.
- `npm --prefix frontend ci` -> passed, 113 packages, 0 vulnerabilities.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> 3 files passed, 21 tests passed.
- `npm --prefix frontend run build` -> passed; generated `frontend/dist` was removed after validation.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- Path-scoped protected-surface check -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0.
- Repository-wide secret/private-marker scan -> failed on pre-existing findings outside the #213 touched slice.
- Follow-up after Codex D:
  - `py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_manual_jsonl_import.py` -> 26 passed, 1 third-party Starlette/httpx deprecation warning.
  - `py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py` -> 35 passed, 1 third-party Starlette/httpx deprecation warning.
  - `npm --prefix frontend ci` -> passed, 113 packages, 0 vulnerabilities.
  - `npm --prefix frontend run typecheck` -> passed.
  - `npm --prefix frontend run test -- --run` -> 3 files passed, 24 tests passed.
  - `npm --prefix frontend run build` -> passed; generated `frontend/dist` was removed after validation.
  - `py -m ruff check src tests tools` -> passed.

## Confirmed Contract Matches

- Backend accepts explicit `source_paths` while preserving single-file `source_path` support.
- Backend enforces exact-one validation for `source_path` versus `source_paths`.
- Backend validates batch source lists before app-data and SQLite setup.
- Adapter exposes `ANALYTICS_LEGACY_JSONL_BATCH_IMPORT_SCHEMA_VERSION` and `adapt_legacy_jsonl_file_batch(...)`.
- Adapter sorts accepted files deterministically and uses one parser-state replay scope for the batch.
- Adapter deduplicates nonblank raw hashes across the full batch and does not expose raw hashes.
- Adapter returns safe `source_mode`, file counts, source artifact summaries, and aggregate #212 quality.
- Manual import calls ingest once for a successful batch and preserves idempotent re-import behavior.
- Frontend request types model exact-one single-file versus batch-source requests.
- Frontend supports batch entry without browser file upload and clears raw path input after terminal results.
- No SQLite schema or migration file was changed.
- No parser behavior, saved-event replay semantics, workbook schema, webhook payload shape, Apps Script behavior, Sheets behavior, Match Journal behavior, OpenAI/AI/coaching behavior, or production behavior was changed by this slice.

## Contract Mismatches

- None remaining after Codex D follow-up.

## Missing Tests

- None remaining for the CT-213 findings. Full repository test suite and GitHub Actions remain unverified.

## Drift Notes

- Issue lifecycle: issue #213 is open.
- Branch lifecycle: local branch was even with `origin/codex/analytics-foundation` during review.
- Working tree includes unrelated launcher dirt from earlier work: `tests/test_analytics_dev_app_launcher.py`, `tools/dev_app/dev_app_launcher.py`, and `Start Mythic Edge Dev App.cmd`. These are outside the #213 contract scope and should not be staged with this module unless separately authorized.
- Repository-wide secret scan has pre-existing findings outside the #213 touched slice. The path-scoped scan for #213 passed.

## Protected-Surface Status

Protected-surface status: clean for the reviewed #213 path set. No forbidden parser/runtime/workbook/webhook/App Script/Sheets/AI/production surfaces were touched by the #213 slice.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan passed with forbidden 0 and warnings 0 for the #213 path set. The repository-wide scan still reports pre-existing findings outside this slice.

## Generated Artifact Status

Frontend build output generated during validation was removed. No generated SQLite database, WAL, SHM, journal, raw log, runtime, failed-post, generated-data, or workbook-export artifacts were found as part of this review.

## Recommendation

Approve for Codex F.

Codex D added the missing contract-required tests without changing production code. The CT-213 findings are verified fixed, protected-surface and secret checks remain clean for the path-scoped slice, and the next role should submit the reviewed module work while excluding unrelated launcher dirt.

## Next Workflow Action

Next role: Codex F: Module Submitter

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #213.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/213

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_legacy_jsonl_batch_import.md

Artifacts:
- docs/contracts/analytics_legacy_jsonl_batch_import.md
- docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md
- docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_fixer.md
- docs/contract_test_reports/analytics_legacy_jsonl_batch_import.md

Task:
Stage only the reviewed #213 legacy JSONL batch import files, commit them, push the branch, and open or update a draft PR targeting the agreed integration branch for the analytics foundation work. Exclude unrelated launcher dirt unless separately authorized.

Reviewed #213 files include:
- docs/contracts/analytics_legacy_jsonl_batch_import.md
- docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md
- docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_fixer.md
- docs/contract_test_reports/analytics_legacy_jsonl_batch_import.md
- src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py
- src/mythic_edge_parser/local_app/import_jobs.py
- tests/test_analytics_legacy_jsonl_artifact_adapter.py
- tests/test_analytics_manual_jsonl_import.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/api.test.ts
- frontend/src/App.tsx
- frontend/src/App.test.tsx
- frontend/src/App.css

Do not stage unrelated launcher files:
- tests/test_analytics_dev_app_launcher.py
- tools/dev_app/dev_app_launcher.py
- Start Mythic Edge Dev App.cmd

Suggested pre-submit validation:
git status --short --branch
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
Run path-scoped protected-surface and secret/private-marker scans over staged #213 paths.

Do not target main, close issues, merge, deploy, change production behavior, or stage unrelated/generated/private artifacts unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/213"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/analytics_legacy_jsonl_batch_import.md"
  review_artifact: "docs/contract_test_reports/analytics_legacy_jsonl_batch_import.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_legacy_jsonl_batch_import_fixer.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  findings_fixed:
    - "CT-213-001: backend non-string source_paths coverage verified fixed."
    - "CT-213-002: adapter batch malformed-file failure coverage verified fixed."
    - "CT-213-003: frontend rejected/failed/degraded batch-state coverage verified fixed."
  validation:
    - "adapter/manual import pytest -> 26 passed, 1 third-party warning"
    - "adjacent analytics/backend pytest -> 35 passed, 1 third-party warning"
    - "frontend npm ci/typecheck/test/build -> passed; generated dist removed"
    - "ruff -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
  forbidden_scope_touched: false
  route: "Codex F submitter"
  stop_conditions:
    - "Do not target main."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior."
    - "Do not change saved-event replay semantics or SQLite schema/migrations."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
    - "Do not stage unrelated launcher files."
```
