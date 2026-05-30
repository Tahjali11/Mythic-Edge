# Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/212

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

Related manual import issue: https://github.com/Tahjali11/Mythic-Edge/issues/211

## Contract

`docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Implementation handoff:
`docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md`

Files reviewed:

- `docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md`
- `docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The implementation must add a reporting-only, sanitized `quality` object for
legacy JSONL manual imports. The object must distinguish blank-line skips,
duplicate raw-hash skips, unsupported-kind skips, processed kind counts,
adapter and ingest warning codes, output gaps where safely observable, and
conservative routing hints without changing parser behavior, saved-event replay
semantics, dedupe scope, SQLite schema, protected downstream surfaces, or raw
artifact retention.

## Findings

No blocking findings.

No non-blocking implementation findings were identified during this review.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| none | n/a | `not_reproduced` | no findings opened | not_blocking | Review found no contract mismatch. | Focused tests, frontend checks, Ruff, diff check, scoped protected-surface check, and scoped secret/private-marker check passed. | F |

## Confirmed Contract Matches

- `LegacyJsonlAdapterResult.quality` is present on successful adapter results.
- The quality object includes the required object value, schema version, status,
  scalar counts, mapping fields, list fields, routing hints, and privacy flags.
- Existing top-level adapter fields remain compatible: `files_processed`,
  `records_seen`, `events_processed`, `events_skipped`,
  `unsupported_kind_counts`, and `warnings`.
- `records_seen` remains nonblank JSONL records only; blank lines are counted
  separately under `blank_line_count` and `skipped_reason_counts.blank_line`.
- Duplicate raw-hash records are skipped before unsupported-kind handling, so
  duplicate unsupported records do not poison `unsupported_kind_counts`.
- Raw hash values are counted but not exposed.
- Unsupported event kinds retain sanitized kind-count behavior.
- Incomplete replay output gaps use `incomplete_summary_unclassified`, leaving
  the specific match/game output-gap keys at zero as authorized by the contract.
- Adapter warning suffixes such as dynamic match IDs are reduced to sanitized
  warning codes in the quality object.
- Failed adapter states return `quality_status = failed` with zero/default
  counters plus sanitized failure codes and routing hints.
- Manual import job responses include `adapter.quality` for terminal adapter
  states and tolerate omitted quality for `not_started`.
- Ingest warnings are copied into sanitized `ingest_warning_codes` after ingest.
- Frontend types, API validation, and Manual Import display handle the quality
  object without exposing raw paths, raw payloads, raw hashes, or destructive
  controls.
- No parser behavior, saved-event replay semantics, dedupe scope, SQLite schema
  or migrations, workbook schema, webhook payload shape, Apps Script behavior,
  Sheets behavior, Match Journal behavior, Line Tracer, OpenAI/AI/coaching, or
  production behavior changed.

## Contract Mismatches

None.

## Missing Tests Or Safeguards

No required test gap found.

Notes:

- Frontend validation intentionally checks schema/object, terminal-state quality
  presence, required broad field shape, routing-hint shape, and privacy flags
  rather than hard-coding every v1 mapping key. Backend tests assert the exact
  required v1 key sets and counts.
- Browser visual inspection was not run; frontend behavior was covered by
  TypeScript, Vitest, and production build.

## Validation Run

```powershell
git fetch --prune
# passed

git status --short --branch
# branch: codex/analytics-foundation; HEAD even with origin/codex/analytics-foundation

git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
# 0 0

py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py
# 9 passed

py -m pytest -q tests\test_analytics_manual_jsonl_import.py
# 12 passed, 1 third-party Starlette/httpx deprecation warning

py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
# 35 passed, 1 third-party Starlette/httpx deprecation warning

npm --prefix frontend ci
# passed, 0 vulnerabilities

npm --prefix frontend run typecheck
# passed

npm --prefix frontend run test -- --run
# 3 files passed, 18 tests passed

npm --prefix frontend run build
# passed; generated frontend/dist removed afterward

py -m ruff check src tests tools
# passed

git diff --check
# passed

path-scoped protected-surface check over the #212 contract, handoff, adapter,
manual import backend, focused tests, and frontend files
# passed, forbidden 0, warnings 0

path-scoped secret/private-marker check over the #212 contract, handoff,
adapter, manual import backend, focused tests, and frontend files
# passed, forbidden 0, warnings 0

py tools\check_secret_patterns.py --all
# failed on pre-existing repository-wide findings outside this touched slice

generated SQLite artifact check
# no generated SQLite artifacts found
```

## Protected-Surface Status

Protected scope was not touched.

The reviewed diff did not change parser/runtime behavior, parser state final
reconciliation, saved-event replay semantics, dedupe scope, parser event
classes, event kind values, parser payload shapes, match/game identity,
analytics SQLite schema or migrations, workbook schema, webhook payload shape,
Apps Script behavior, Google Sheets behavior, Match Journal behavior, Line
Tracer, OpenAI/AI/coaching/model-provider behavior, production behavior, or
destructive import/database/job/UI actions.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan passed with forbidden 0 and warnings 0.

The all-repo advisory secret scan failed on pre-existing findings outside the
touched #212 slice. This is residual repository state, not a new #212 leak.

No raw local JSONL artifact, raw Player.log content, raw saved-event line, raw
hash, full submitted path, stack trace, secret, credential, webhook URL,
workbook ID, generated SQLite database, runtime status file, failed-post
payload, workbook export, or generated card data was added by this slice.

## Generated Artifact Status

`npm --prefix frontend run build` generated `frontend/dist`; it was removed
after validation.

No SQLite database, journal, WAL, or SHM files were found in the working tree
outside ignored dependency/cache areas.

## Drift Notes

- `tests/test_analytics_dev_app_launcher.py`,
  `tools/dev_app/dev_app_launcher.py`, and untracked
  `Start Mythic Edge Dev App.cmd` are unrelated dirty launcher artifacts from
  another slice. Codex F should keep them out of the issue #212 package unless
  separately authorized.
- `docs/contracts/analytics_legacy_jsonl_batch_import.md` is also untracked and
  outside the reviewed #212 quality-breakdown package. Codex F should exclude
  it unless separately authorized.
- The contract and handoff for issue #212 are untracked and should be included
  with this reviewed slice.
- GitHub Actions were not run in this local review.
- Live workbook state, deployed Apps Script state, and production behavior were
  not inspected, as expected for this local reporting-only slice.
- Manual import against a real private local JSONL artifact was not run.

## Recommendation

Approve for Codex F submitter work.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #212.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/212

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Related manual import issue:
https://github.com/Tahjali11/Mythic-Edge/issues/211

Branch:
codex/analytics-foundation

Reviewed contract:
docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md

Implementation handoff:
docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md

Review artifact:
docs/contract_test_reports/analytics_legacy_jsonl_import_quality_breakdown.md

Goal:
Stage only the reviewed issue #212 package, commit it, push the branch, and open
or update the draft PR to the appropriate non-main integration target. Do not
stage unrelated launcher artifacts unless separately authorized.

Reviewed issue #212 paths:
- docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md
- docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md
- docs/contract_test_reports/analytics_legacy_jsonl_import_quality_breakdown.md
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

Known unrelated dirty paths to exclude unless separately authorized:
- tests/test_analytics_dev_app_launcher.py
- tools/dev_app/dev_app_launcher.py
- Start Mythic Edge Dev App.cmd
- docs/contracts/analytics_legacy_jsonl_batch_import.md

Validation reviewed by Codex E:
- adapter pytest: 9 passed
- manual import pytest: 12 passed, 1 third-party warning
- parser-normalized replay + local app backend pytest: 35 passed, 1 third-party warning
- frontend npm ci/typecheck/test/build: passed
- Ruff: passed
- git diff --check: passed
- path-scoped protected-surface scan: passed
- path-scoped secret/private-marker scan: passed
- generated SQLite artifact check: clean
- all-repo secret scan still fails on pre-existing out-of-scope findings

Stop conditions:
- Do not target main.
- Do not stage unrelated launcher files or untracked command files.
- Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/Line Tracer/production behavior.
- Do not change saved-event replay semantics or dedupe scope.
- Do not change analytics SQLite schema or migrations.
- Do not create or commit generated/private/runtime artifacts or secrets.
- Do not expose raw payloads, raw paths, raw hashes, stack traces, or destructive import/database/job actions.
- Do not close issues or mark tracker #204 complete unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/212"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  related_manual_import_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/211"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/analytics_legacy_jsonl_import_quality_breakdown.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_legacy_jsonl_import_quality_breakdown_comparison.md"
  review_artifact: "docs/contract_test_reports/analytics_legacy_jsonl_import_quality_breakdown.md"
  risk_tier: "Medium"
  branch: "codex/analytics-foundation"
  verdict: "approved_for_submitter"
  findings:
    - "No blocking findings."
    - "No non-blocking implementation findings."
  validation:
    - "py -m pytest -q tests\\test_analytics_legacy_jsonl_artifact_adapter.py -> 9 passed"
    - "py -m pytest -q tests\\test_analytics_manual_jsonl_import.py -> 12 passed, 1 third-party warning"
    - "py -m pytest -q tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_local_app_backend.py -> 35 passed, 1 third-party warning"
    - "npm --prefix frontend ci -> passed, 0 vulnerabilities"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> 3 files passed, 18 tests passed"
    - "npm --prefix frontend run build -> passed; generated frontend/dist removed afterward"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker check -> passed, forbidden 0, warnings 0"
    - "py tools\\check_secret_patterns.py --all -> failed on pre-existing out-of-scope repository findings"
    - "generated SQLite artifact check -> no generated SQLite artifacts found"
  protected_scope_touched: false
  forbidden_scope_touched: false
  residual_risks:
    - "GitHub Actions were not run."
    - "Manual import against a real private local JSONL artifact was not run."
    - "Live workbook, deployed Apps Script, and production behavior were not inspected."
    - "Unrelated launcher dirty files remain present and must be excluded from issue #212 staging unless separately authorized."
    - "Untracked docs/contracts/analytics_legacy_jsonl_batch_import.md is outside the reviewed #212 package and must be excluded unless separately authorized."
  stop_conditions:
    - "Do not target main."
    - "Do not stage unrelated launcher files or untracked command files."
    - "Do not stage docs/contracts/analytics_legacy_jsonl_batch_import.md unless separately authorized."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/Line Tracer/production behavior."
    - "Do not change saved-event replay semantics or dedupe scope."
    - "Do not change analytics SQLite schema or migrations."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
    - "Do not close issues or mark tracker #204 complete unless explicitly asked."
```
