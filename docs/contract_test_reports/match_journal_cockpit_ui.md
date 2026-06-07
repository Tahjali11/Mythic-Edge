# Match Journal Cockpit UI Contract-Test Report

## Role Performed

Codex E: Module Reviewer / contract-test confirmation thread.

## Findings

No remaining blocking findings.

### CT-232-001 P1: Fixed

Successful browser-facing Match Journal write responses no longer echo full
service records through `result.service_result`.

Evidence:

- Implementation: `src/mythic_edge_parser/local_app/match_journal_cockpit.py:333`
  still returns the contracted success envelope, but now passes service results
  through a compact summary.
- Implementation: `src/mythic_edge_parser/local_app/match_journal_cockpit.py:344`
  summarizes only stable service metadata and `record_counts`.
- Implementation: `src/mythic_edge_parser/local_app/match_journal_cockpit.py:350`
  redacts or drops unsafe summary values.
- Test: `tests/test_match_journal_cockpit_ui_backend.py:234` uses a real
  in-memory `MatchJournalService` write and asserts successful responses do not
  include `records`, `note_text`, Player.log markers, or webhook-like URL
  markers.
- Confirmation probe: posting a synthetic unsafe note through a real
  per-request in-memory service returned HTTP 200 with a compact
  `service_result`, no `records`, no `note_text`, and no unsafe markers in the
  serialized response.

## Issue And Tracker

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/232>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/202>

## Contract And Handoffs Reviewed

- Contract: `docs/contracts/match_journal_cockpit_ui.md`
- Implementation handoff:
  `docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md`
- Fixer handoff:
  `docs/implementation_handoffs/match_journal_cockpit_ui_fixer.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Branch sync: `HEAD...origin/codex/analytics-foundation` is `0 0`.

Reviewed files:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/match_journal_cockpit.py`
- `tests/test_match_journal_cockpit_ui_backend.py`
- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `frontend/src/api.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/src/App.css`
- `docs/contracts/match_journal_cockpit_ui.md`
- `docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md`
- `docs/implementation_handoffs/match_journal_cockpit_ui_fixer.md`
- `docs/contract_test_reports/match_journal_cockpit_ui.md`

## Report Lifecycle

`report_lifecycle`: `followup_after_fixer`

## Contract Summary

The implementation must add the first browser-facing Match Journal cockpit via
the FastAPI local app backend, not direct browser calls to the broad-CORS status
API. It must keep parser and analytics facts read-only, route journal writes
through `MatchJournalService`, preserve narrowed local-app CORS, defer
pilot-error controls, avoid destructive controls, return safe envelopes, and
avoid changing parser/runtime/analytics schema/workbook/webhook/App Script/
Sheets/OpenAI/AI/coaching/production behavior.

## Internal Project Area Reviewed

Local App / UI.

## Bridge-Code Status Reviewed

`stable_bridge`: browser UI -> FastAPI local app facade -> Match Journal
service.

## Checks Run

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
git diff -- src\mythic_edge_parser\local_app\match_journal_cockpit.py tests\test_match_journal_cockpit_ui_backend.py docs\implementation_handoffs\match_journal_cockpit_ui_fixer.md

# Confirmation probe: real per-request in-memory MatchJournalService,
# POST /api/journal/notes with unsafe synthetic note text.

py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py tests\test_match_journal_status_api.py tests\test_analytics_local_app_backend.py tests\test_status_api.py
py -m pytest -q tests\test_match_journal_service.py tests\test_match_journal_repository.py tests\test_match_journal_schema.py
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
py -m ruff check src tests
py tools\check_agent_docs.py
git diff --check

@'
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/App.tsx
frontend/src/api.test.ts
frontend/src/api.ts
frontend/src/types.ts
src/mythic_edge_parser/local_app/backend.py
docs/contracts/match_journal_cockpit_ui.md
src/mythic_edge_parser/local_app/match_journal_cockpit.py
tests/test_match_journal_cockpit_ui_backend.py
docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md
docs/contract_test_reports/match_journal_cockpit_ui.md
docs/implementation_handoffs/match_journal_cockpit_ui_fixer.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin

@'
frontend/src/App.css
frontend/src/App.test.tsx
frontend/src/App.tsx
frontend/src/api.test.ts
frontend/src/api.ts
frontend/src/types.ts
src/mythic_edge_parser/local_app/backend.py
docs/contracts/match_journal_cockpit_ui.md
src/mythic_edge_parser/local_app/match_journal_cockpit.py
tests/test_match_journal_cockpit_ui_backend.py
docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md
docs/contract_test_reports/match_journal_cockpit_ui.md
docs/implementation_handoffs/match_journal_cockpit_ui_fixer.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

Get-ChildItem -Recurse -File -Include *.sqlite,*.sqlite3,*.db,*.db-wal,*.db-shm,*.journal,*.sqlite-wal,*.sqlite-shm,*.sqlite-journal | Where-Object { $_.FullName -notmatch '\\.git\\' } | Select-Object -ExpandProperty FullName
```

## Results

The original P1 finding is fixed. Focused validation and safety scans passed.
Route to Codex F for submitter work.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-232-001 | P1 | `fixed_state_followup` | fixed | not_blocking | Successful write responses returned full `service_result.records`, allowing private note text and unsafe markers to echo to the browser. | D replaced full service records with a compact summary; real-service probe and focused regression confirm `records`, `note_text`, Player.log markers, and webhook-like URL markers are absent from successful write responses. | F |

## Confirmed Contract Matches

- The browser API helpers use `/api/journal/...`, not direct status API
  `/journal/...` routes.
- `/api/journal/pilot-error` was not added, and pilot-error cockpit controls
  remain absent.
- The backend route inventory uses FastAPI local app routes and preserves the
  existing local-app CORS policy; no wildcard CORS was introduced.
- Missing Match Journal service wiring fails closed with `service_unavailable`.
- Malformed and invalid backend requests do not call the service in focused
  tests.
- Attached note context and unattached note validation are kept separate.
- Display correction requests preserve `journal_display_only` and reject
  `parser_truth`.
- Frontend context is sourced from existing match/game history rows and is
  submitted as parser-owned context only.
- Successful write responses now return compact service summaries instead of
  full service records.
- Destructive controls, raw SQL/browser DB controls, direct Sheets/App Script
  actions, OpenAI/model-provider calls, coaching, Line Tracer, hidden-card
  claims, best-line advice, and player-mistake truth controls were not added.
- No parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/
  OpenAI/AI/coaching/production behavior changes were found.

## Contract Mismatches

None remaining.

## Missing Tests Or Safeguards

No missing tests remain for CT-232-001.

Still-unverified layers are listed below and should remain non-blocking for the
module submitter handoff.

## Drift Notes

- Branch sync: `HEAD...origin/codex/analytics-foundation` is `0 0`.
- Issue #232 is open and still references tracker #202.
- No workbook, deployed Apps Script, production, or local-data drift was
  inspected beyond the protected-surface and generated-artifact checks.
- `npm --prefix frontend run build` created `frontend/dist`; it was removed
  after validation so no generated frontend build artifact remains.

## Validation Results

- Confirmation probe for the original unsafe note echo -> fixed; HTTP 200
  response contains compact service metadata only.
- `py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py` -> 9
  passed, 1 existing Starlette/httpx deprecation warning.
- `py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py tests\test_match_journal_status_api.py tests\test_analytics_local_app_backend.py tests\test_status_api.py`
  -> 44 passed, 1 existing Starlette/httpx deprecation warning.
- `py -m pytest -q tests\test_match_journal_service.py tests\test_match_journal_repository.py tests\test_match_journal_schema.py`
  -> 63 passed.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run test -- --run` -> 3 files passed, 59 tests passed.
- `npm --prefix frontend run build` -> passed; generated `frontend/dist`
  removed afterward.
- `py -m ruff check src tests` -> passed.
- `py tools\check_agent_docs.py` -> passed.
- `git diff --check` -> passed.
- Path-scoped secret/private-marker scan including the fixer handoff -> passed,
  forbidden 0, warnings 0.
- Path-scoped protected-surface scan including the fixer handoff -> passed,
  forbidden 0, warnings 0.
- Generated SQLite/database artifact check -> no output outside `.git`.

## Protected-Surface Status

Path-scoped protected-surface scan passed with forbidden 0, warnings 0. The
reviewed fix does not change parser behavior, parser state final
reconciliation, parser event classes, match/game identity, deduplication,
analytics schema/migrations/ingest, workbook schema, webhook payload shape,
Apps Script behavior, Google Sheets behavior, output transport, OpenAI/model-
provider behavior, AI/coaching behavior, or production behavior.

## Secret/Private-Marker Status

Path-scoped scan passed with forbidden 0, warnings 0. The original successful
write-response echo was not reproduced after the D fix.

Full all-repo secret scan was not rerun in this confirmation pass; the initial
review recorded pre-existing unrelated repo-wide findings outside the touched
slice.

## Generated Artifact Status

No SQLite DB/WAL/SHM/journal artifacts were found. `frontend/dist` was produced
by the build command and removed before this report was finalized.

## Whether Forbidden Scope Was Touched

No forbidden parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/
coaching/production scope was touched. The D fix stayed inside the approved
local app Match Journal facade response-shaping boundary.

## Remaining Risks

- Live local app backend plus browser manual flow was not rerun.
- Real on-disk Match Journal service wiring remains unverified.
- GitHub Actions / PR checks were not run locally.
- Full all-repo secret scan still has known pre-existing unrelated findings
  from the initial review context.

## Recommendation

Approve for Codex F: Module Submitter.

Next role: Codex F: Module Submitter.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #232.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/232

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Contract:
docs/contracts/match_journal_cockpit_ui.md

Reviewed artifact:
docs/contract_test_reports/match_journal_cockpit_ui.md

Implementation handoffs:
- docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md
- docs/implementation_handoffs/match_journal_cockpit_ui_fixer.md

Goal:
Stage only the reviewed issue #232 files, commit them, push the branch, and
open or update a draft PR targeting the correct non-main integration path.
Do not target main unless explicitly approved.

Reviewed files to stage:
- docs/contracts/match_journal_cockpit_ui.md
- docs/implementation_handoffs/match_journal_cockpit_ui_comparison.md
- docs/implementation_handoffs/match_journal_cockpit_ui_fixer.md
- docs/contract_test_reports/match_journal_cockpit_ui.md
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/match_journal_cockpit.py
- tests/test_match_journal_cockpit_ui_backend.py
- frontend/src/types.ts
- frontend/src/api.ts
- frontend/src/api.test.ts
- frontend/src/App.tsx
- frontend/src/App.test.tsx
- frontend/src/App.css

Before staging:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and identify unrelated changes.
- Confirm HEAD is even with origin/codex/analytics-foundation or record the
  branch-sync risk.
- Stage only the reviewed issue #232 files.
- Confirm generated frontend build output, SQLite files, raw logs, runtime
  artifacts, failed posts, workbook exports, local JSONL artifacts, and secrets
  are not staged.

Suggested validation before submit:
- py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py tests\test_match_journal_status_api.py tests\test_analytics_local_app_backend.py tests\test_status_api.py
- py -m pytest -q tests\test_match_journal_service.py tests\test_match_journal_repository.py tests\test_match_journal_schema.py
- npm --prefix frontend run typecheck
- npm --prefix frontend run test -- --run
- npm --prefix frontend run build
- py -m ruff check src tests
- py tools\check_agent_docs.py
- git diff --check
- path-scoped secret/private-marker and protected-surface scans over the staged issue #232 files

Do not:
- Stage unrelated files.
- Call the status API directly from the browser.
- Change status API CORS.
- Add pilot-error browser controls.
- Change parser behavior, parser state final reconciliation, parser event
  classes, match/game identity, deduplication, analytics schema/migrations/
  ingest behavior, workbook schema, webhook payload shape, Apps Script
  behavior, Google Sheets behavior, output transport, production behavior,
  OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer behavior,
  or generated-artifact policy.
- Create or commit raw logs, private JSONL artifacts, generated SQLite DB/WAL/
  SHM/journal files, runtime artifacts, failed posts, workbook exports,
  secrets, credentials, API keys, tokens, webhook URLs, or local-only artifacts.
- Close issue #232, close tracker #202, target main, merge, or deploy unless
  explicitly asked.

Final handoff should include branch, commit hash, PR URL, target branch, files
staged, validation, protected-surface/secret status, generated artifact status,
and next recommended role.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/232"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contract_test_reports/match_journal_cockpit_ui.md"
  target_artifact: "draft PR for issue #232"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  findings_confirmed_fixed:
    - "CT-232-001 P1: successful write responses no longer echo unsafe full service records through result.service_result."
  validation:
    - "confirmation probe POST /api/journal/notes with unsafe synthetic note -> 200 compact service_result, no records/note_text/unsafe markers"
    - "py -m pytest -q tests\\test_match_journal_cockpit_ui_backend.py -> 9 passed, 1 existing warning"
    - "py -m pytest -q tests\\test_match_journal_cockpit_ui_backend.py tests\\test_match_journal_status_api.py tests\\test_analytics_local_app_backend.py tests\\test_status_api.py -> 44 passed, 1 existing warning"
    - "py -m pytest -q tests\\test_match_journal_service.py tests\\test_match_journal_repository.py tests\\test_match_journal_schema.py -> 63 passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run test -- --run -> 59 passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "py -m ruff check src tests -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "generated SQLite/database artifact check -> no output outside .git"
  forbidden_scope_touched: false
  remaining_risks:
    - "Live local app backend plus browser manual flow was not rerun."
    - "Real on-disk Match Journal service wiring remains unverified."
    - "GitHub Actions / PR checks were not run locally."
  stop_conditions:
    - "Do not target main unless explicitly approved."
    - "Stage only reviewed issue #232 files."
    - "Do not call the status API directly from the browser."
    - "Do not change status API CORS or add pilot-error browser controls."
    - "Do not change parser/runtime/analytics schema/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime artifacts or secrets."
```
