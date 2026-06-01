# Match Journal Status API Contract-Test Report

## Role Performed

Codex E: Module Reviewer / contract-test confirmation thread.

## Findings

No remaining blocking findings.

### CT-203-001 P2: Fixed

Unsupported HTTP verbs on known journal routes now return the contracted JSON
`405 method_not_allowed` envelope.

Evidence:

- Implementation: `src/mythic_edge_parser/app/status_api.py:613` adds actual
  `PUT` handler coverage and `src/mythic_edge_parser/app/status_api.py:625`
  routes unsupported journal methods through the journal JSON envelope.
- Test: `tests/test_match_journal_status_api.py:147` verifies the actual HTTP
  handler returns `405` JSON for `PUT /journal/notes`.
- Runtime probe in this confirmation pass returned `405`,
  `application/json; charset=utf-8`, and error code `method_not_allowed`.

### CT-203-002 P2: Fixed

`GET /journal?parser_game_id=...` now resolves through the real
`MatchJournalService` bundle path.

Evidence:

- Implementation: `src/mythic_edge_parser/app/match_journal_service.py:364`
  keeps bundle lookup read-only with `allow_create=False` and game-preferred
  context resolution.
- Implementation: `src/mythic_edge_parser/app/match_journal_service.py:380`
  adds game and parser-game bundle filters.
- Implementation: `src/mythic_edge_parser/app/match_journal_service.py:391`
  resolves the parent match without direct SQL in the route layer.
- Tests: `tests/test_match_journal_service.py:347` and
  `tests/test_match_journal_status_api.py:406` verify parser-game-only bundle
  lookup through service and route-helper paths.
- Runtime probe in this confirmation pass created an in-memory game note, then
  returned a `200` bundle for `GET /journal` with only `parser_game_id`.

## Issue And Tracker

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/203>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/202>

## Contract And Handoffs Reviewed

- Contract: `docs/contracts/match_journal_status_api.md`
- Initial implementation handoff:
  `docs/implementation_handoffs/match_journal_status_api_comparison.md`
- Fixer handoff:
  `docs/implementation_handoffs/match_journal_status_api_fixer.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Branch sync: `HEAD...origin/codex/analytics-foundation` is `0 0`.

Reviewed changed files:

- `docs/contracts/match_journal_status_api.md`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/app/match_journal_service.py`
- `tests/test_match_journal_status_api.py`
- `tests/test_match_journal_service.py`
- `docs/implementation_handoffs/match_journal_status_api_comparison.md`
- `docs/implementation_handoffs/match_journal_status_api_fixer.md`
- `docs/contract_test_reports/match_journal_status_api.md`

## Report Lifecycle

`report_lifecycle`: `followup_after_fixer`

## Contract Summary

The implementation must expose a narrow loopback-only JSON API bridge over
`MatchJournalService`, preserve existing status API GET behavior, avoid direct
SQL/default database creation, keep responses sanitized, and avoid changing
parser/runtime/workbook/webhook/App Script/Sheets/analytics/UI/AI/production
behavior.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-203-001 | P2 | `fixed_state_followup` | fixed | not_blocking | Actual HTTP handler returned BaseHTTPRequestHandler `501` HTML for `PUT /journal/notes`; contract required `405` JSON `method_not_allowed`. | `status_api.py` now implements unsupported journal method handling; actual runtime probe returned `405` JSON; focused tests passed. | F |
| CT-203-002 | P2 | `fixed_state_followup` | fixed | not_blocking | `GET /journal?parser_game_id=...` returned `404` through the real service despite an existing parser-game row. | `MatchJournalService.get_journal_bundle()` now supports game filters without create-on-read; runtime probe returned `200` with the expected parser-game bundle; focused tests passed. | F |

## Confirmed Contract Matches

- The D fix stays within the Match Journal/status API bridge and service
  read-model scope authorized by the contract.
- Unsupported methods on known journal routes now return the journal JSON
  envelope instead of default HTML.
- `parser_game_id` bundle lookup is supported through `MatchJournalService`,
  not through direct SQL in `status_api.py`.
- The bundle read path remains local repository data only and uses
  `allow_create=False`.
- Non-journal unsupported method behavior was not broadened into a new journal
  API contract.
- Tests cover the actual HTTP handler, route-helper path, and real in-memory
  service path.
- No generated SQLite database, raw log, workbook export, secret, credential,
  webhook URL, runtime status artifact, failed post, or local-only artifact was
  kept.

## Contract Mismatches

None remaining.

## Missing Tests Or Safeguards

No missing tests remain for the two original findings.

The inherited broad CORS behavior remains a future hardening consideration for
any browser-facing cockpit/overlay, but it was present before this D fix and
was not required to change under this contract.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
# ## codex/analytics-foundation...origin/codex/analytics-foundation
#  M src/mythic_edge_parser/app/match_journal_service.py
#  M src/mythic_edge_parser/app/status_api.py
#  M tests/test_match_journal_service.py
# ?? docs/contract_test_reports/match_journal_status_api.md
# ?? docs/contracts/match_journal_status_api.md
# ?? docs/implementation_handoffs/match_journal_status_api_comparison.md
# ?? docs/implementation_handoffs/match_journal_status_api_fixer.md
# ?? tests/test_match_journal_status_api.py

git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
# 0 0

# Runtime probe: PUT /journal/notes through actual HTTP handler
# -> 405, application/json; charset=utf-8, error code method_not_allowed

# Runtime probe: GET /journal with parser_game_id through real in-memory service
# -> 200, expected parser-game bundle returned

py -m pytest -q tests\test_match_journal_status_api.py tests\test_match_journal_service.py
# 42 passed

py -m pytest -q tests\test_match_journal_status_api.py tests\test_status_api.py
# 24 passed

py -m pytest -q tests\test_match_journal_schema.py tests\test_match_journal_repository.py tests\test_match_journal_service.py tests\test_status_api.py
# 67 passed

py -m ruff check src tests tools
# All checks passed

py tools\check_agent_docs.py
# passed, errors 0, warnings 0

git diff --check
# passed

path-scoped secret/private-marker scan over issue #203 files
# passed, forbidden 0, warnings 0

path-scoped protected-surface scan over issue #203 files
# passed, forbidden 0, warnings 0

generated SQLite/database artifact check
# no output outside .git
```

## Protected-Surface Status

No forbidden parser/runtime/workbook/webhook/App Script/Sheets/analytics/UI/AI
or production surface was touched. The only runtime code changes are the
approved local status API bridge and Match Journal service read-model lookup.

## Secret/Private-Marker Status

Path-scoped secret/private-marker scan passed with forbidden 0, warnings 0.
The confirmation probes and tests used synthetic note text and in-memory
SQLite only.

## Generated Artifact Status

No generated SQLite database, WAL, SHM, journal file, raw log, failed post,
runtime status artifact, workbook export, local JSONL artifact, secret,
credential, webhook URL, or local-only artifact was found outside `.git`.

## Remaining Risks

- Live local HTTP startup with a production-like Match Journal service factory
  remains unverified.
- Future cockpit or overlay clients remain out of scope.
- Workbook, webhook, Apps Script, Google Sheets, OpenAI/model-provider,
  AI/coaching, and production behavior were not exercised.
- Broad inherited CORS behavior should be revisited before these local write
  routes become browser-facing beyond the approved local developer surface.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #203.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/203

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Reviewed artifact:
docs/contract_test_reports/match_journal_status_api.md

Contract:
docs/contracts/match_journal_status_api.md

Implementation handoffs:
- docs/implementation_handoffs/match_journal_status_api_comparison.md
- docs/implementation_handoffs/match_journal_status_api_fixer.md

Goal:
Stage only the reviewed issue #203 files, commit them, push the branch, and
open or update a draft PR targeting the correct non-main integration path.
Do not target main unless explicitly approved.

Reviewed files to stage:
- docs/contracts/match_journal_status_api.md
- src/mythic_edge_parser/app/status_api.py
- src/mythic_edge_parser/app/match_journal_service.py
- tests/test_match_journal_status_api.py
- tests/test_match_journal_service.py
- docs/implementation_handoffs/match_journal_status_api_comparison.md
- docs/implementation_handoffs/match_journal_status_api_fixer.md
- docs/contract_test_reports/match_journal_status_api.md

Before staging:
- Confirm branch is codex/analytics-foundation.
- Inspect git status and identify unrelated changes.
- Confirm HEAD is even with origin/codex/analytics-foundation or record the
  branch-sync risk.
- Stage only the reviewed issue #203 files.

Suggested validation before submit:
- py -m pytest -q tests\test_match_journal_status_api.py tests\test_match_journal_service.py
- py -m pytest -q tests\test_match_journal_status_api.py tests\test_status_api.py
- py -m pytest -q tests\test_match_journal_schema.py tests\test_match_journal_repository.py tests\test_match_journal_service.py tests\test_status_api.py
- py -m ruff check src tests tools
- py tools\check_agent_docs.py
- git diff --check
- path-scoped secret/private-marker and protected-surface scans over the staged issue #203 files

Do not:
- Stage unrelated files.
- Change parser behavior, parser state final reconciliation, parser event
  classes, match/game identity, deduplication, analytics schema/migrations/
  ingest/views, workbook schema, webhook payload shape, Apps Script behavior,
  Google Sheets behavior, frontend/local app UI behavior, output transport,
  production behavior, OpenAI/model-provider behavior, AI/coaching behavior,
  or environment variable policy.
- Create or commit SQLite database files, WAL/SHM/journal files, raw logs,
  generated data, runtime status artifacts, failed posts, workbook exports,
  secrets, credentials, API keys, tokens, webhook URLs, local JSONL artifacts,
  or local-only artifacts.
- Close issue #203, close tracker #202, merge, deploy, or target main unless
  explicitly asked.

Final handoff should include branch, commit hash, PR URL, target branch,
files staged, validation, protected-surface/secret status, generated artifact
status, and next recommended role.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/203"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contract_test_reports/match_journal_status_api.md"
  target_artifact: "draft PR for issue #203"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  findings_confirmed_fixed:
    - "CT-203-001: unsupported HTTP verbs on known journal routes return 405 JSON method_not_allowed."
    - "CT-203-002: GET /journal with parser_game_id resolves through the real MatchJournalService bundle path."
  validation:
    - "runtime probe PUT /journal/notes -> 405 JSON method_not_allowed"
    - "runtime probe GET /journal?parser_game_id=parser-game-1 -> 200 with expected real service bundle"
    - "py -m pytest -q tests\\test_match_journal_status_api.py tests\\test_match_journal_service.py -> 42 passed"
    - "py -m pytest -q tests\\test_match_journal_status_api.py tests\\test_status_api.py -> 24 passed"
    - "py -m pytest -q tests\\test_match_journal_schema.py tests\\test_match_journal_repository.py tests\\test_match_journal_service.py tests\\test_status_api.py -> 67 passed"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated SQLite/database artifact check -> no output outside .git"
  forbidden_scope_touched: false
  remaining_risks:
    - "Live local HTTP startup with a production-like Match Journal service factory remains unverified."
    - "Future cockpit or overlay clients remain out of scope."
    - "Inherited broad CORS behavior should be revisited before browser-facing use expands."
  stop_conditions:
    - "Do not target main unless explicitly approved."
    - "Stage only reviewed issue #203 files."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/analytics/UI/AI/production behavior."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
```
