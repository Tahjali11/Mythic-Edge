# Match Journal Cockpit Write Controls Contract-Test Report

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/234>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/202>

## Contract

`docs/contracts/match_journal_cockpit_write_controls.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Implementation handoffs:

- `docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md`
- `docs/implementation_handoffs/match_journal_cockpit_write_controls_fixer.md`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Findings

No blocking findings remain.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-234-001 | P1 | `fixed_state_followup` | Fixed. Failed/unavailable Match Journal submit envelopes no longer clear unsaved frontend form input. | not_blocking | Initial review: `frontend/src/api.ts` returned sanitized non-OK envelopes while the old form handlers cleared state unconditionally after `await`. | `frontend/src/App.tsx` now returns a success boolean from journal mutations and clears note, opponent-label, experiment-label, and display-correction form values only after that boolean is true. `frontend/src/App.test.tsx` covers resolved `status: "unavailable"` envelopes preserving note, label, experiment, and display-correction inputs. | F |
| CT-234-002 | P2 | `fixed_state_followup` | Fixed. The failed-submit preservation regression now waits for enabled journal controls before submitting. | not_blocking | Prior E confirmation: `npm --prefix frontend test -- --run src/App.test.tsx` failed once because `submitJournalNote` had not been called before timeout, then passed on rerun. The test was racing async journal/history readiness. | `frontend/src/App.test.tsx` now waits for the relevant controls and submit buttons to be enabled before firing submit events. Three consecutive focused runs passed, and the full frontend suite passed. | F |

## Contract Matches

- Branch is `codex/analytics-foundation`; local branch and origin are even (`0 0`).
- Normal `create_app(...)` journal routes remain wired through the default app-owned Match Journal service.
- Explicit `match_journal_service_factory` injection still overrides default wiring.
- App-owned Match Journal database path remains `<app_data>\db\match_journal.sqlite3`.
- Setup/status and default journal reads remain non-creating.
- First explicit write remains limited to the app-owned Match Journal database, not analytics tables.
- Backend write responses remain compact and sanitized.
- FastAPI journal routes remain loopback-CORS only; no wildcard FastAPI CORS was introduced.
- Direct `status_api.py` CORS policy remains unchanged, matching the deferred contract decision.
- Browser route inventory remains limited to allowed `/api/journal/...` routes.
- No pilot-error, destructive, raw SQL, import/export/sync, database reset, AI/coaching, workbook, webhook, Apps Script, Sheets, or production controls were added.
- Failed/unavailable write input is preserved for retry and uses safe "not saved" copy.

## Contract Mismatches

- None found in this confirmation pass.

## Missing Tests Or Safeguards

- No blocking missing tests remain.
- A dedicated assertion that successful `ok` submit envelopes clear only the saved form would strengthen coverage, but current code review and existing successful-submit coverage are sufficient for this fixer confirmation.

## Files Reviewed

- `docs/contracts/match_journal_cockpit_write_controls.md`
- `docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md`
- `docs/implementation_handoffs/match_journal_cockpit_write_controls_fixer.md`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/match_journal_cockpit.py`
- `src/mythic_edge_parser/local_app/match_journal_runtime.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/App.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/App.test.tsx`
- `tests/test_match_journal_cockpit_ui_backend.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_analytics_local_app_config.py`
- `tests/test_analytics_dev_app_launcher.py`

## Validation Run

```powershell
git status --short --branch --untracked-files=all
# ## codex/analytics-foundation...origin/codex/analytics-foundation
# #234 implementation files, contract, handoffs, runtime helper, and this report are unstaged

git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
# 0 0

for ($i = 1; $i -le 3; $i++) { npm --prefix frontend test -- --run src/App.test.tsx }
# three consecutive focused runs passed, 33 tests each

npm --prefix frontend run typecheck
# passed

py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
# 12 passed, 1 Starlette/FastAPI testclient deprecation warning

py -m pytest -q tests\test_analytics_dev_app_launcher.py
# 10 passed

py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
# 23 passed, 1 Starlette/FastAPI testclient deprecation warning

py -m pytest -q tests\test_match_journal_service.py tests\test_match_journal_repository.py tests\test_match_journal_schema.py
# 63 passed

npm --prefix frontend test -- --run
# 3 files passed, 61 tests passed

npm --prefix frontend run build
# passed; generated frontend/dist removed afterward

py -m ruff check src tests tools
# passed

py tools\check_agent_docs.py
# passed, errors 0, warnings 0

git diff --check
# passed
```

## Protected-Surface Status

Path-scoped protected-surface scan passed for the contract, review report,
implementation handoffs, and changed #234 code/test files: forbidden 0,
warnings 0.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan passed for the contract, review report,
implementation handoffs, and changed #234 code/test files: forbidden 0,
warnings 0.

## Generated Artifact Status

`npm --prefix frontend run build` generated ignored `frontend/dist` output
during validation; it was removed afterward. Generated SQLite/database artifact
sweep returned no files outside `.git`. `Test-Path frontend\dist -> False`.

## Remaining Risks

- Manual live-browser retry flow with a disposable app-data root was not run.
- Real local app operation against the user's actual app-data root remains unverified.
- Direct status API global CORS hardening remains intentionally deferred.
- Pilot-error browser controls remain intentionally deferred.
- GitHub Actions were not run locally.

## Recommendation

Approve for Codex F: Module Submitter.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #234.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/234

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Contract:
docs/contracts/match_journal_cockpit_write_controls.md

Review artifact:
docs/contract_test_reports/match_journal_cockpit_write_controls.md

Implementation handoffs:
- docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md
- docs/implementation_handoffs/match_journal_cockpit_write_controls_fixer.md

Goal:
Stage only the reviewed #234 files, commit, push, and open or update a draft PR targeting the approved integration branch. Do not merge, close issue #234, or mark tracker #202 complete.

Before staging:
- Confirm branch is codex/analytics-foundation and is even with origin/codex/analytics-foundation.
- Inspect git status and separate unrelated files from reviewed #234 scope.
- Verify frontend/dist, generated SQLite files, raw logs, runtime artifacts, failed posts, workbook exports, secrets, and local-only artifacts are not staged.

Reviewed files expected for #234:
- docs/contracts/match_journal_cockpit_write_controls.md
- docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md
- docs/implementation_handoffs/match_journal_cockpit_write_controls_fixer.md
- docs/contract_test_reports/match_journal_cockpit_write_controls.md
- src/mythic_edge_parser/local_app/backend.py
- src/mythic_edge_parser/local_app/match_journal_cockpit.py
- src/mythic_edge_parser/local_app/match_journal_runtime.py
- src/mythic_edge_parser/local_app/paths.py
- src/mythic_edge_parser/local_app/setup_status.py
- tests/test_match_journal_cockpit_ui_backend.py
- tests/test_analytics_local_app_backend.py
- tests/test_analytics_local_app_config.py
- tests/test_analytics_dev_app_launcher.py
- frontend/src/api.ts
- frontend/src/api.test.ts
- frontend/src/types.ts
- frontend/src/App.tsx
- frontend/src/App.test.tsx

Do not stage unrelated work. Do not target main. Do not change parser/runtime/analytics truth/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior. Do not create or commit generated/private/local artifacts or secrets.

Validation already reviewed by Codex E:
- focused App.test.tsx passed three consecutive runs
- full frontend tests/typecheck/build passed
- focused backend/service/launcher pytest slices passed
- ruff, agent docs, git diff --check, protected-surface scan, and secret/private-marker scan passed

Final handoff must include branch, commit hash, PR URL, PR target branch, staged files, validation evidence, remaining risks, issue/tracker closure status, and next role Codex G only after PR exists.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/234"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/match_journal_cockpit_write_controls.md"
  implementation_handoff: "docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/match_journal_cockpit_write_controls_fixer.md"
  review_artifact: "docs/contract_test_reports/match_journal_cockpit_write_controls.md"
  branch: "codex/analytics-foundation"
  risk_tier: "High"
  findings:
    - "No blocking findings remain."
    - "CT-234-001 P1 fixed: failed/unavailable Match Journal submit responses no longer clear unsaved frontend form input."
    - "CT-234-002 P2 fixed: failed-submit preservation regression now waits for enabled journal controls before submitting."
  validation:
    - "git rev-list --left-right --count HEAD...origin/codex/analytics-foundation -> 0 0"
    - "npm --prefix frontend test -- --run src/App.test.tsx -> 33 passed on three consecutive focused runs"
    - "npm --prefix frontend run typecheck -> passed"
    - "py -m pytest -q tests\\test_match_journal_cockpit_ui_backend.py -> 12 passed, 1 warning"
    - "py -m pytest -q tests\\test_analytics_dev_app_launcher.py -> 10 passed"
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py tests\\test_analytics_local_app_config.py -> 23 passed, 1 warning"
    - "py -m pytest -q tests\\test_match_journal_service.py tests\\test_match_journal_repository.py tests\\test_match_journal_schema.py -> 63 passed"
    - "npm --prefix frontend test -- --run -> 61 passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed afterward"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated SQLite/database artifact sweep -> no output"
    - "Test-Path frontend\\dist -> False"
  remaining_unverified:
    - "manual live-browser retry flow with disposable app-data root"
    - "real local app operation against user app-data root"
    - "GitHub Actions"
  forbidden_scope_touched: false
  next_recommended_role: "Codex F: Module Submitter"
```
