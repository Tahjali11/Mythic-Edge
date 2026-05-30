# Analytics Manual JSONL Import UI Job-Status Contract-Test Report

report_lifecycle: final_approval
finding_lifecycle: fixed_state_followup

## Findings

No blocking findings remain.

### issue-211-p1-non-object-post-body-can-echo-raw-input

- severity: P1
- finding_lifecycle: fixed_state_followup
- finding_status: fixed_state_followup
- blocking_status: resolved
- next_route: F
- verification_evidence: `src/mythic_edge_parser/local_app/backend.py:73` to `src/mythic_edge_parser/local_app/backend.py:75`; `src/mythic_edge_parser/local_app/import_jobs.py:216` to `src/mythic_edge_parser/local_app/import_jobs.py:222`; `tests/test_analytics_manual_jsonl_import.py:221` to `tests/test_analytics_manual_jsonl_import.py:246`; direct reproduction and validation listed below.

Original finding: non-object `POST /api/imports/jsonl` bodies could echo raw submitted input through FastAPI default 422 validation details before the sanitizer ran.

Verified fixed state: the route now accepts the request body as `object` and passes it to `run_manual_jsonl_import(...)`. Scalar, list, and numeric bodies are handled by the import sanitizer as sanitized `rejected` job summaries with `source_request_invalid`, do not echo path-like submitted values, and do not create app-data folders or database files.

## Issue And Scope

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/211>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/204>
- Umbrella issue: <https://github.com/Tahjali11/Mythic-Edge/issues/207>
- Branch: `codex/analytics-foundation`
- Contract: `docs/contracts/analytics_manual_jsonl_import_ui_job_status.md`
- Implementation handoff: `docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md`
- Fixer handoff: `docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_fixer.md`
- Risk tier: High

## Contract Matches

- Branch is `codex/analytics-foundation` and is even with `origin/codex/analytics-foundation`.
- `POST /api/imports/jsonl` and `GET /api/imports/jobs/{job_id}` exist.
- The backend uses `adapt_legacy_jsonl_artifacts(...)` and `ingest_parser_normalized_replay(...)` rather than reinterpreting parser facts.
- Valid synthetic JSONL import writes parser-normalized rows to a temporary app-owned SQLite database under app-data.
- Invalid blank, URL, UNC, missing, directory, non-JSONL, and now non-object request bodies are rejected before app-data or database creation.
- Malformed JSONL returns a safe adapter error category without echoing the raw line, payload, or source path in the focused test.
- Unsupported event kinds and duplicate raw hashes are summarized with safe counts/categories and do not expose raw hash values.
- Job status is process-local and in memory.
- Unknown jobs return 404 without revealing existing job IDs.
- No destructive DELETE routes were added for imports or jobs.
- Frontend Manual Import controls exist, submit to the import API, render sanitized job summaries, clear the raw path after terminal success/error, and keep destructive controls absent in tests.
- Setup/status now labels manual import as enabled while keeping live watcher/parser runner deferred or disabled.
- No SQLite migration/schema SQL changed.
- No adapter behavior, analytics ingest semantics, parser behavior, or parser replay semantics changed.

## Contract Mismatches

None found after the Codex D fixer pass.

## Missing Tests Or Safeguards

No missing blocker-level tests remain for the original P1. The focused backend suite now covers scalar path-like bodies, list path-like bodies, and numeric non-object bodies, including no raw submitted path echo and no app-data/database creation.

## Validation Run

- `git status --short --branch` -> branch is `codex/analytics-foundation`; working tree includes issue #211 changes plus pre-existing dirty launcher files and unrelated untracked `Start Mythic Edge Dev App.cmd`.
- `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation` -> `0 0`.
- Direct reproduction of old P1 shape -> scalar/list/numeric bodies returned HTTP 200 sanitized `rejected` jobs with `source_request_invalid`, raw path not present, app-data root not created.
- `py -m pytest -q tests\test_analytics_manual_jsonl_import.py` -> 12 passed, 1 third-party Starlette/FastAPI deprecation warning.
- `py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py` -> 43 passed, 1 third-party Starlette/FastAPI deprecation warning.
- `py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_field_evidence_ingest.py` -> 77 passed.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> 3 files passed, 18 tests passed.
- `npm --prefix frontend run build` -> passed.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- Path-scoped protected-surface check over issue #211 files -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over issue #211 files -> passed, forbidden 0, warnings 0.

Repo-wide secret/private-marker note: the earlier initial review ran `py tools\check_secret_patterns.py --all` and it failed on pre-existing repository-wide findings outside the touched issue #211 path set. The D confirmation used path-scoped scans, which passed cleanly.

## Protected-Surface Status

No parser behavior, saved-event replay semantics, parser state final reconciliation, parser event classes, event kind values, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, Match Journal behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, deployment behavior, or production behavior change was found.

The D fix stayed inside the authorized local app import route/request-sanitization surface.

## Secret And Private-Marker Status

The path-scoped secret/private-marker scan over issue #211 touched files passed with forbidden 0 and warnings 0. The original runtime response-sanitization bug was fixed by routing non-object request bodies through the import sanitizer instead of FastAPI's default body-shape validation response.

## Generated Artifact Status

- `frontend/node_modules/` exists locally and is ignored.
- `frontend/dist/` was produced by frontend build validation and removed.
- `src/mythic_edge_parser/local_app/__pycache__/` and `tests/__pycache__/` were produced by validation and removed.
- No generated SQLite database, WAL, SHM, journal, raw JSONL artifact, runtime artifact, failed-delivery artifact, workbook export, screenshot, or generated data artifact was found as changed or untracked after cleanup.

## Dirty Scope Notes

Pre-existing dirty launcher files remain in the worktree and should not be staged as part of issue #211 unless separately authorized:

- `tests/test_analytics_dev_app_launcher.py`
- `tools/dev_app/dev_app_launcher.py`
- untracked `Start Mythic Edge Dev App.cmd`

Issue #211 submitter scope should stay limited to the manual import backend/frontend/test/handoff/report paths plus any already-reviewed setup/status files. Codex F must inspect `git status` and stage only the reviewed issue #211 package.

## Verdict

Ready for Codex F. The original P1 is resolved, no new blocking findings were found, and the issue #211 package is ready for submitter handling without targeting `main`, closing issue #211, or marking tracker #204 complete.

## Next Recommended Role

Codex F: Module Submitter.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #211 on branch codex/analytics-foundation.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/211

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue:
https://github.com/Tahjali11/Mythic-Edge/issues/207

Contract:
docs/contracts/analytics_manual_jsonl_import_ui_job_status.md

Implementation handoff:
docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md

Fixer handoff:
docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_fixer.md

Review artifact:
docs/contract_test_reports/analytics_manual_jsonl_import_ui_job_status.md

Goal:
Submit the reviewed issue #211 package to a draft PR targeting the correct non-main integration branch. Do not target main.

Before staging:
- Confirm branch is codex/analytics-foundation and is even with origin/codex/analytics-foundation.
- Inspect git status and stage only issue #211 files:
  - docs/contracts/analytics_manual_jsonl_import_ui_job_status.md
  - docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md
  - docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_fixer.md
  - docs/contract_test_reports/analytics_manual_jsonl_import_ui_job_status.md
  - src/mythic_edge_parser/local_app/import_jobs.py
  - src/mythic_edge_parser/local_app/backend.py
  - src/mythic_edge_parser/local_app/setup_status.py
  - tests/test_analytics_manual_jsonl_import.py
  - tests/test_analytics_local_app_backend.py
  - frontend/src/App.tsx
  - frontend/src/api.ts
  - frontend/src/types.ts
  - frontend/src/status.ts
  - frontend/src/App.css
  - frontend/src/App.test.tsx
  - frontend/src/api.test.ts
- Do not stage unrelated dirty launcher files unless separately authorized:
  - tests/test_analytics_dev_app_launcher.py
  - tools/dev_app/dev_app_launcher.py
  - Start Mythic Edge Dev App.cmd
- Do not stage generated/private/local artifacts such as frontend/dist, node_modules, __pycache__, SQLite DB/WAL/SHM/journal files, raw logs, runtime files, failed posts, workbook exports, generated data, credentials, or local-only artifacts.

Validation to rerun or confirm:
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_field_evidence_ingest.py
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
path-scoped protected-surface and secret/private-marker checks over the issue #211 package

After build validation, remove generated frontend/dist and any __pycache__ artifacts before staging.

Submitter actions:
- Commit only the reviewed issue #211 package.
- Push the branch.
- Open or update a draft PR targeting the non-main integration branch required by the tracker/workflow.
- Link issue #211, tracker #204, and umbrella issue #207.
- Do not merge, close issues, mark tracker #204 complete, target main, or change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior.
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / confirmation thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/211"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_manual_jsonl_import_ui_job_status.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_fixer.md"
  review_artifact: "docs/contract_test_reports/analytics_manual_jsonl_import_ui_job_status.md"
  findings:
    - severity: "P1"
      status: "fixed_state_followup"
      summary: "Non-object POST /api/imports/jsonl bodies now route through sanitized rejected job handling without raw input echo."
  validation:
    - "branch sync -> 0 0"
    - "direct old-P1 reproduction -> sanitized rejected jobs; raw path not echoed; app-data not created"
    - "manual import backend tests -> 12 passed, 1 third-party warning"
    - "adapter/ingest/backend slice -> 43 passed, 1 third-party warning"
    - "gameplay/opponent/field-evidence ingest slice -> 77 passed"
    - "frontend npm typecheck/test/build -> passed"
    - "ruff -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
  generated_artifacts: "frontend/dist and Python cache artifacts removed; no SQLite/raw/runtime/workbook artifacts found"
  forbidden_scope_touched: false
  verdict: "ready_for_codex_f"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
```
