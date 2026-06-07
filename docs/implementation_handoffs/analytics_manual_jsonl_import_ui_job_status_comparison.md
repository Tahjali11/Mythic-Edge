# Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/211

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/204

Umbrella issue: https://github.com/Tahjali11/Mythic-Edge/issues/207

## Contract

`docs/contracts/analytics_manual_jsonl_import_ui_job_status.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Status

Branch confirmed:

```text
codex/analytics-foundation
```

Starting status included pre-existing dirty work from prior local app slices:

- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_dev_app_launcher.py`
- `tools/dev_app/dev_app_launcher.py`
- untracked `docs/contracts/analytics_manual_jsonl_import_ui_job_status.md`

During this pass, an unrelated untracked `Start Mythic Edge Dev App.cmd` was present and was not absorbed into this module.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_manual_jsonl_import_ui_job_status.md`
- `docs/contracts/analytics_local_developer_app_shell.md`
- `docs/contracts/analytics_app_backend_setup_status.md`
- `docs/contracts/analytics_react_vite_setup_status_page.md`
- `docs/contracts/analytics_windows_developer_launcher_bootstrapper.md`
- `docs/contracts/analytics_legacy_jsonl_artifact_adapter.md`
- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/status.ts`
- existing focused backend/frontend/adapter/ingest tests

## Current Behavior Compared To Contract

Current repo behavior already provided the setup/status backend, React/Vite status page, Windows launcher, legacy JSONL adapter, parser-normalized ingest, gameplay-action ingest, opponent-card-observation ingest, and field-evidence ingest.

The contract gaps were present:

- no `POST /api/imports/jsonl`;
- no `GET /api/imports/jobs/{job_id}`;
- no process-local sanitized import job registry;
- no app-owned SQLite open/create path for explicit manual imports;
- setup/status still labeled manual import as disabled/deferred;
- frontend Manual Import remained a deferred placeholder;
- no focused tests proved path redaction, invalid-source rejection before DB creation, malformed JSONL safety, or destructive-route absence.

## Implementation Option Chosen

Implemented the full first-slice local manual JSONL import workflow authorized by the contract:

- explicit local `.jsonl` path input;
- backend reads the selected file in place;
- adapter path uses `adapt_legacy_jsonl_artifacts(...)`;
- SQLite writes use `ingest_parser_normalized_replay(...)`;
- app-owned database and app-data folders are created only after source validation and successful adapter replay;
- job status is synchronous and process-local in memory;
- frontend displays sanitized labels, counts, warnings, errors, and database status only.

## Files Changed

New files:

- `src/mythic_edge_parser/local_app/import_jobs.py`
- `tests/test_analytics_manual_jsonl_import.py`
- `docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md`

Modified files:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `tests/test_analytics_local_app_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/status.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`

Pre-existing dirty files preserved but not owned by this issue:

- `tests/test_analytics_dev_app_launcher.py`
- `tools/dev_app/dev_app_launcher.py`
- `Start Mythic Edge Dev App.cmd`

## Exact Sections Changed

Backend:

- Added `mythic_edge_parser.local_app.import_jobs`.
- Added `MANUAL_JSONL_IMPORT_SCHEMA_VERSION = "analytics_manual_jsonl_import_ui_job_status.v1"`.
- Added process-local bounded job registry and `get_import_job(...)`.
- Added `run_manual_jsonl_import(...)` orchestration.
- Added source validation for blank paths, URLs, UNC paths, missing files, directories, non-`.jsonl` files, and non-files.
- Added app-data directory/database creation only after source validation and adapter success.
- Added sanitized terminal job summaries with `source`, `adapter`, `ingest`, `database`, `warnings`, and `errors`.
- Wired `POST /api/imports/jsonl`.
- Wired `GET /api/imports/jobs/{job_id}`.
- Extended loopback CORS to allow `POST` and `Content-Type`.
- Updated setup/status capabilities and runtime status to show manual import as enabled.

Frontend:

- Added manual import job/request TypeScript types.
- Added manual import API submit/fetch helpers with schema validation.
- Added Manual Import UI section with path input, optional safe label input, import button, loading/error/result states, and sanitized summary.
- Cleared submitted path/label state after terminal success or error.
- Kept Analytics Views and Live Watcher deferred.
- Added status tone support for enabled/succeeded/completed/failed/rejected.

Tests:

- Added focused backend import tests for valid import, path rejection before DB creation, malformed JSONL safety, unsupported/duplicate safe summaries, unknown job safety, and destructive-route absence.
- Updated backend setup/status tests for enabled manual import and `POST` CORS.
- Added frontend API tests for manual import submit/job fetch and malformed responses.
- Added frontend UI tests for enabled workflow, sanitized result display, path clearing, API error safety, and destructive-control absence.

## Code/Test/Doc Status

Code changed: yes.

Tests changed: yes.

Docs changed: yes, handoff only. The source contract was pre-existing from Codex B and remains untracked in this worktree.

Frontend-only changes: yes.

Backend-only changes: yes.

Import-support-only changes: yes.

Schema changes: no SQLite migration or schema SQL changed.

Adapter stat decision: no adapter code changed. Duplicate raw hashes remain represented in `events_skipped`, and unsupported event kinds remain represented in `unsupported_kind_counts`. No raw hash values are exposed.

## Database Creation And Migration Behavior

`POST /api/imports/jsonl` now:

1. validates request shape and selected source path;
2. rejects invalid URL/UNC/missing/directory/non-JSONL sources before app-data or database creation;
3. adapts the JSONL through `adapt_legacy_jsonl_artifacts(...)`;
4. creates app-owned folders under the supplied/default app-data root only after adapter success;
5. opens `%LOCALAPPDATA%\MythicEdgeDev\db\mythic_edge.sqlite3` or the test override equivalent;
6. calls `ingest_parser_normalized_replay(...)`, which applies existing analytics migrations and writes parser-normalized facts.

No repo-local SQLite database files are created by tests.

## Job Status Schema Implemented

Terminal job summaries include:

- `object`
- `schema_version`
- `job_id`
- `status`
- `phase`
- `created_at`
- `started_at`
- `finished_at`
- `source`
- `adapter`
- `ingest`
- `database`
- `warnings`
- `errors`

Implemented status outcomes:

- `succeeded`
- `degraded`
- `failed`
- `rejected`

`queued` and `running` remain reserved for future background execution and are not used by the synchronous backend route.

## Validation Run

```powershell
git status --short --branch
# -> ## codex/analytics-foundation...origin/codex/analytics-foundation
# -> showed intended files plus pre-existing dirty launcher/CORS work and unrelated untracked Start Mythic Edge Dev App.cmd

py -m pytest -q tests\test_analytics_manual_jsonl_import.py
# -> 8 passed, 1 Starlette/httpx deprecation warning

py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
# -> 43 passed, 1 Starlette/httpx deprecation warning

py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_field_evidence_ingest.py
# -> 77 passed

npm --prefix frontend ci
# -> initially failed with EPERM on a Rolldown native file because a repo-local Vite process was still running
# -> stopped only that repo-local Vite process
# -> rerun passed, 113 packages audited, 0 vulnerabilities

npm --prefix frontend run typecheck
# -> passed

npm --prefix frontend run test -- --run
# -> 3 test files passed, 18 tests passed

npm --prefix frontend run build
# -> passed

py -m ruff check src tests tools
# -> All checks passed

git diff --check
# -> passed

@'
docs/contracts/analytics_manual_jsonl_import_ui_job_status.md
docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md
src/mythic_edge_parser/local_app/import_jobs.py
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/setup_status.py
tests/test_analytics_manual_jsonl_import.py
tests/test_analytics_local_app_backend.py
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/status.ts
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/api.test.ts
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# -> passed, forbidden 0, warnings 0

@'
docs/contracts/analytics_manual_jsonl_import_ui_job_status.md
docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md
src/mythic_edge_parser/local_app/import_jobs.py
src/mythic_edge_parser/local_app/backend.py
src/mythic_edge_parser/local_app/setup_status.py
tests/test_analytics_manual_jsonl_import.py
tests/test_analytics_local_app_backend.py
frontend/src/App.tsx
frontend/src/api.ts
frontend/src/types.ts
frontend/src/status.ts
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/api.test.ts
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# -> passed, forbidden 0, warnings 0

py tools\check_secret_patterns.py --all
# -> failed with pre-existing repository-wide findings outside this touched path
# -> summary: forbidden 541, warnings 890
# -> path-scoped scan for #211 touched files passed cleanly

git diff --check
# -> rerun after handoff passed
```

## Protected-Surface Status

No parser behavior, parser state final reconciliation, saved-event replay semantics, parser event classes, event kind values, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, Match Journal behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior, deployment behavior, or production behavior was changed.

## Secret/Private-Marker Status

The implementation uses synthetic test JSONL only. No private JSONL artifact, raw Player.log excerpt, webhook URL, secret, credential, generated DB, runtime artifact, failed-delivery payload, workbook export, screenshot, or local-only private artifact was intentionally added.

## Generated Artifact Status

`frontend/dist` was created by `npm --prefix frontend run build` and removed afterward.

Expected ignored dependency folder:

- `frontend/node_modules/` exists and is ignored.

Generated/local artifact check after final validation:

- `frontend/dist` absent
- `frontend/.vite` absent
- `frontend/coverage` absent
- `src/mythic_edge_parser/local_app/__pycache__` absent
- `tests/__pycache__` absent
- `data/analytics` absent

## Forbidden Scope

Forbidden scope touched: no.

No destructive import, database, job, launcher, or UI actions were exposed.

No file upload, drag/drop import, copied import retention, directory import UI, persistent job history, cancellation, retry queue, job deletion, database reset/delete/wipe/clear/export/browser route, live Player.log watcher, parser runner control, Match Journal behavior, Sheets sync, OpenAI/model-provider runtime integration, AI/coaching behavior, Line Tracer, or production behavior was added.

## Still Unverified

- Manual import against a real private local JSONL artifact was not run.
- Long-running import/background execution is not implemented and remains deferred.
- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Production behavior was not exercised.
- Browser visual inspection was not run in this pass; frontend behavior was verified through Vitest/typecheck/build.

## Reviewer Focus

Codex E should focus on:

- whether rejected/failed job responses satisfy the contract's exact schema expectations;
- whether returning HTTP 200 with `status = rejected` for invalid source requests is acceptable under the contract's "rejected job or safe 4xx" allowance;
- whether job warnings are sufficiently informative while remaining sanitized;
- whether clearing the path input after terminal import satisfies the frontend raw-path retention rule;
- whether setup/status manual-import enabled labels are narrow enough and preserve existing backend schema compatibility;
- whether the pre-existing dirty launcher/CORS files should be reviewed separately from #211 before submitter work.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #211.

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

Risk tier:
High

Review the implementation against the issue, contract, handoff, and diff. Lead with findings ordered by severity. Verify that the manual JSONL import UI/job-status workflow stays local, explicit, sanitized, non-destructive, and downstream of parser-owned truth.

Pay special attention to:
- POST /api/imports/jsonl and GET /api/imports/jobs/{job_id}
- process-local job summary schema and sanitization
- invalid source handling before DB creation
- malformed JSONL handling without raw line/path/payload echo
- app-owned SQLite creation under app-data only
- use of adapt_legacy_jsonl_artifacts(...) and ingest_parser_normalized_replay(...)
- frontend raw path clearing after terminal result
- absence of destructive import/database/job/launcher/UI actions
- absence of parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production changes
- pre-existing dirty launcher/CORS files that may need submitter separation

Do not modify code in review mode. If findings are concrete, route to Codex D. If the contract is ambiguous or wrong, route to Codex B. If clean, recommend Codex F.

Suggested validation:
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_analytics_legacy_jsonl_artifact_adapter.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_local_app_backend.py
py -m pytest -q tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_field_evidence_ingest.py
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests tools
git diff --check
py tools\check_secret_patterns.py --all

Also run path-scoped protected-surface and secret/private-marker scans over the touched files, and confirm no generated SQLite/runtime/frontend build artifacts are present.

Final report should include findings, contract matches, contract mismatches, missing tests, validation run, protected-surface status, secret/private-marker status, generated artifact status, and routing recommendation.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/211"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  umbrella_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/207"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/analytics_manual_jsonl_import_ui_job_status.md"
  target_artifact: "docs/implementation_handoffs/analytics_manual_jsonl_import_ui_job_status_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_analytics_manual_jsonl_import.py -> 8 passed, 1 warning"
    - "py -m pytest -q tests\\test_analytics_legacy_jsonl_artifact_adapter.py tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_local_app_backend.py -> 43 passed, 1 warning"
    - "py -m pytest -q tests\\test_analytics_gameplay_action_ingest.py tests\\test_analytics_opponent_card_observation_ingest.py tests\\test_analytics_field_evidence_ingest.py -> 77 passed"
    - "npm --prefix frontend ci -> passed after stopping one repo-local Vite process that locked node_modules"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> 18 passed"
    - "npm --prefix frontend run build -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "py tools\\check_secret_patterns.py --all -> failed with pre-existing repository-wide findings outside touched path"
    - "generated artifact check -> frontend/dist absent, data/analytics absent, local __pycache__ cleaned"
  stop_conditions:
    - "Do not target main."
    - "Do not expose destructive import, database, job, launcher, or UI actions."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/Match Journal/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
    - "Do not stage, commit, push, open a PR, merge, or close issues unless explicitly asked."
```
