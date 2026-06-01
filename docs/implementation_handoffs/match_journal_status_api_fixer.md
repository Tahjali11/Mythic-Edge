# Match Journal Status API Fixer Handoff

## Role Performed

Codex D: Module Fixer.

## Issue And Tracker

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/203
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/202

## Source Artifacts

- Contract: `docs/contracts/match_journal_status_api.md`
- Review artifact: `docs/contract_test_reports/match_journal_status_api.md`
- Implementation handoff:
  `docs/implementation_handoffs/match_journal_status_api_comparison.md`
- Constitution: `docs/agent_constitution.md`
- Role rules: `docs/agent_threads/module_fixer.md`

## Findings Fixed

- CT-203-001: actual unsupported HTTP verbs on known journal routes returned
  the `BaseHTTPRequestHandler` default `501` HTML response instead of the
  contracted `405` JSON `method_not_allowed` envelope.
- CT-203-002: `GET /journal` advertised `parser_game_id` as accepted query
  context, but real `MatchJournalService` bundle lookup returned `404` for
  parser-game-only context even when a matching journal game existed.

## Fault Category

Implementation mismatches with the accepted status API and Match Journal
service contracts.

CT-203-002 did not require routing back to Codex B. The service contract
already allows parser-game context, and the status API contract explicitly
lists `parser_game_id` for `GET /journal`.

## Fix Produced

- Added actual HTTP handler coverage for `PUT /journal/notes`.
- Added unsupported-method handling for known journal routes so `PUT`, `PATCH`,
  `DELETE`, and `OPTIONS` route through the existing journal JSON envelope and
  return `405 method_not_allowed`.
- Preserved existing non-journal unsupported-method behavior.
- Added real in-memory service coverage for `GET /journal?parser_game_id=...`.
- Updated `MatchJournalService.get_journal_bundle()` to resolve game context
  for bundle reads and filter repository bundle rows by `journal_game_id` or
  `parser_game_id` when game context is supplied.

## Files Changed

- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/app/match_journal_service.py`
- `tests/test_match_journal_status_api.py`
- `tests/test_match_journal_service.py`
- `docs/implementation_handoffs/match_journal_status_api_fixer.md`

## Code Changed

Runtime code changed: yes.

Runtime behavior changed only inside the approved local Match Journal/status
API bridge and Match Journal service read-model behavior.

No parser behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics schema/migrations/ingest/views,
workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
behavior, frontend/local app UI behavior, output transport, production
behavior, OpenAI/model-provider behavior, AI/coaching behavior, or environment
variable policy changed.

## Tests Changed

- Added route-level unsupported-verb regression coverage for the actual HTTP
  handler.
- Added status API regression coverage for `GET /journal` with
  `parser_game_id` using a real in-memory `MatchJournalService`.
- Added service regression coverage for parser-game-only bundle reads.

## Validation Evidence

```text
py -m pytest -q tests\test_match_journal_status_api.py tests\test_match_journal_service.py
-> 42 passed

py -m pytest -q tests\test_match_journal_status_api.py tests\test_status_api.py
-> 24 passed

py -m pytest -q tests\test_match_journal_schema.py tests\test_match_journal_repository.py tests\test_match_journal_service.py tests\test_status_api.py
-> 67 passed

py -m ruff check src tests tools
-> passed

py tools\check_agent_docs.py
-> passed

git diff --check
-> passed

new-file whitespace/final-newline check
-> passed

path-scoped protected-surface scan over touched issue #203 files
-> passed, forbidden 0, warnings 0

path-scoped secret/private-marker scan over touched issue #203 files
-> passed, forbidden 0, warnings 0

generated SQLite/database artifact check
-> no output outside .git
```

## Protected-Surface Status

No forbidden parser/runtime/workbook/webhook/App Script/Sheets/analytics/UI/AI
or production surfaces were intentionally touched.

## Secret/Private-Marker Status

No secrets, credentials, API keys, tokens, webhook URLs, raw local paths, note
payloads, exception details, SQLite files, raw logs, workbook exports, local
JSONL artifacts, or local-only artifacts were intentionally added.

## Generated Artifact Status

Focused tests used in-memory SQLite only. No generated SQLite database, WAL,
SHM, journal file, runtime status artifact, raw log, workbook export,
generated data, secret, credential, webhook URL, local JSONL artifact, or
local-only artifact was intentionally created or kept.

## Remaining Review Focus

- Confirm actual unsupported HTTP methods on known journal routes return the
  contracted JSON `405 method_not_allowed` envelope.
- Confirm parser-game-only `GET /journal` bundle lookup is now supported
  through the real service without parser/runtime state lookup.
- Confirm the service bundle read remains local repository data only and does
  not become analytics, workbook, AI, or parser truth.
- Confirm non-journal unsupported method behavior was not broadened into a new
  API contract.

## Still-Unverified Layers

- Live local HTTP startup with a production-like Match Journal service factory.
- Future cockpit or overlay clients.
- Workbook, webhook, Apps Script, Google Sheets, OpenAI/model-provider,
  AI/coaching, and production behavior.

## Next Recommended Role

Codex E confirmation thread.

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/203"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  source_artifact: "docs/contract_test_reports/match_journal_status_api.md"
  target_artifact: "docs/implementation_handoffs/match_journal_status_api_fixer.md"
  branch: "codex/analytics-foundation"
  findings_fixed:
    - "CT-203-001: unsupported HTTP verbs on known journal routes now return 405 JSON method_not_allowed."
    - "CT-203-002: GET /journal with parser_game_id now resolves through the real MatchJournalService bundle path."
  validation:
    - "focused API/service pytest -> 42 passed"
    - "status API focused pytest -> 24 passed"
    - "schema/repository/service/status pytest -> 67 passed"
    - "ruff -> passed"
    - "agent docs check -> passed"
    - "git diff --check -> passed"
    - "new-file whitespace/final-newline check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated SQLite/database artifact check -> no output outside .git"
  forbidden_scope_touched: false
  next_recommended_role: "Codex E confirmation thread"
```
