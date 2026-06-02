# Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/232

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/202

## Contract

`docs/contracts/match_journal_cockpit_ui.md`

## Review Artifact

`docs/contract_test_reports/match_journal_cockpit_ui.md`

## Role Performed

Codex D: Module Fixer.

## Finding Fixed

CT-232-001 P1: successful Match Journal cockpit write responses could echo
unsafe full service records through `result.service_result`.

## What Changed

Added a focused backend regression using a real in-memory `MatchJournalService`
write with local-path and Apps-Script-like markers in note text. The test proves
that successful `/api/journal/notes` responses preserve useful success metadata
while dropping persisted service-record values such as `records.note.note_text`.

Updated the local app Match Journal cockpit facade to return a deterministic
service-result summary instead of the full service result. The summary contains:

- `action`
- `status`
- `primary_record_type`
- `primary_record_id`
- `record_counts`

The full `records` object is no longer returned in successful browser-facing
write responses.

## Files Changed

- `src/mythic_edge_parser/local_app/match_journal_cockpit.py`
- `tests/test_match_journal_cockpit_ui_backend.py`
- `docs/implementation_handoffs/match_journal_cockpit_ui_fixer.md`

## Code Changed Or Tests Only

Code and tests changed. The code change is limited to local app response
shaping for Match Journal cockpit write successes.

No Match Journal service, repository, parser, analytics schema, workbook,
webhook, Apps Script, Sheets, OpenAI, AI/coaching, or production behavior was
changed.

## Tests Added Or Updated

- Added `test_successful_journal_write_response_summarizes_service_result_without_echoing_record_values`.
- The test posts an unattached note through a real in-memory Match Journal
  service and asserts:
  - HTTP 200 still returns `service_result`.
  - `service_result` is a compact summary.
  - `records` is not returned.
  - `note_text`, `Player.log`, `script.google.com`, and the full unsafe note
    text are not echoed in the JSON response.

## Validation Run

```powershell
py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
# 9 passed, 1 StarletteDeprecationWarning

py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py tests\test_match_journal_status_api.py tests\test_analytics_local_app_backend.py tests\test_status_api.py
# 44 passed, 1 StarletteDeprecationWarning

py -m pytest -q tests\test_match_journal_service.py tests\test_match_journal_repository.py tests\test_match_journal_schema.py
# 63 passed

npm --prefix frontend run typecheck
# passed

npm --prefix frontend run test -- --run
# 3 files passed, 59 tests passed

py -m ruff check src tests
# passed

py tools\check_agent_docs.py
# passed

git diff --check
# passed

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
# passed, forbidden 0, warnings 0

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
# passed, forbidden 0, warnings 0

Get-ChildItem -Recurse -File -Include *.sqlite,*.sqlite3,*.db,*.db-wal,*.db-shm,*.journal,*.sqlite-wal,*.sqlite-shm,*.sqlite-journal | Where-Object { $_.FullName -notmatch '\\.git\\' } | Select-Object -ExpandProperty FullName
# no output
```

## Protected-Surface Status

Path-scoped protected-surface scan passed with forbidden 0 and warnings 0. No
forbidden scope was intentionally touched.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan passed with forbidden 0 and warnings 0.
The focused regression confirms the CT-232-001 unsafe response echo is fixed.

## Generated Artifact Status

No generated artifacts were intentionally created or kept.

## Remaining Risks

- Live local app backend plus browser manual flow was not rerun in this D pass.
- GitHub Actions / PR checks were not run locally.
- Full all-repo secret scan was not rerun; Codex E previously reported
  pre-existing unrelated all-repo findings outside this slice.

## Forbidden Scope Status

Forbidden scope touched: false.

## Next Workflow Action

Next recommended role: Codex E confirmation thread.

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/232"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  branch: "codex/analytics-foundation"
  source_artifact: "docs/contract_test_reports/match_journal_cockpit_ui.md"
  target_artifact: "docs/implementation_handoffs/match_journal_cockpit_ui_fixer.md"
  finding_fixed:
    - "CT-232-001 P1: successful write responses no longer echo unsafe full service records through result.service_result."
  files_changed:
    - "src/mythic_edge_parser/local_app/match_journal_cockpit.py"
    - "tests/test_match_journal_cockpit_ui_backend.py"
    - "docs/implementation_handoffs/match_journal_cockpit_ui_fixer.md"
  code_changed_or_tests_only: "code+tests"
  forbidden_scope_touched: false
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
```
