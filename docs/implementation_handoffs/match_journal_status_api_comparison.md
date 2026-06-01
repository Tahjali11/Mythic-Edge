# Match Journal Status API Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/203

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/202

## Contract

`docs/contracts/match_journal_status_api.md`

## Internal Project Area

Local App / UI bridge over the Match Journal human-intent layer.

## Truth Owner

The Match Journal service owns human-intent journal commands and service result
shapes. Parser/state remains the owner of parser match and game facts. The
status API added here is transport and response shaping only.

## Bridge-Code Status

`bridge_code`

Bridge from:

- `MatchJournalService`

Bridge to:

- local loopback HTTP/status API clients

## Role Performed

Codex C: Module Implementer / comparison thread.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/match_journal_status_api.md`
- `docs/contracts/match_journal_service.md`
- `docs/contracts/match_journal_repository.md`
- `docs/contracts/match_journal_local_sqlite_schema.md`
- `docs/implementation_handoffs/match_journal_service_comparison.md`
- `docs/contract_test_reports/match_journal_service.md`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/app/match_journal_service.py`
- `src/mythic_edge_parser/app/match_journal_repository.py`
- `src/mythic_edge_parser/app/config.py`
- `tests/test_status_api.py`
- `tests/test_match_journal_service.py`
- `tests/test_match_journal_repository.py`
- `tests/test_match_journal_schema.py`

## Current Behavior Compared To Contract

Current repo behavior before this implementation:

- `status_api.py` exposed read-oriented GET routes and a root route inventory.
- `status_api.py` had no POST support, JSON request parsing, Match Journal
  service seam, or journal route error envelopes.
- `MatchJournalService` already owned the required journal operations:
  notes, pilot-error status/reason, manual opponent labels, review flags,
  display-only corrections, and journal bundle reads.
- Existing tests covered GET status routes and Match Journal service behavior,
  but not route-level Match Journal dispatch.

Contract gaps closed in this pass:

- Added explicit Match Journal route inventory.
- Added explicit service-factory wiring for local route dispatch.
- Added loopback-host fail-closed behavior for journal routes.
- Added sanitized journal success and failure envelopes.
- Added JSON body parsing and invalid payload handling.
- Added route dispatch to `MatchJournalService` methods.
- Added focused tests for route inventory, success paths, method errors,
  malformed JSON, missing service wiring, loopback protection, unattached-note
  behavior, context-required note scopes, pilot-error status/reason separation,
  manual labels, review flags, display-only corrections, service error mapping,
  and JSON-safe in-memory service rows.

## Implementation Option Chosen

Implemented the smallest direct status API bridge inside
`src/mythic_edge_parser/app/status_api.py`.

I chose a service-factory seam, `configure_match_journal_service_factory(...)`,
instead of opening a default database path or adding an environment variable.
That keeps service availability explicit and testable, preserves caller-owned
SQLite behavior, and avoids generated database files in tests.

## Files Changed

- `src/mythic_edge_parser/app/status_api.py`
- `tests/test_match_journal_status_api.py`
- `docs/implementation_handoffs/match_journal_status_api_comparison.md`

Untracked source artifact present from Codex B:

- `docs/contracts/match_journal_status_api.md`

## Exact Code Sections Changed

`src/mythic_edge_parser/app/status_api.py`

- Added Match Journal service imports and route constants.
- Added `configure_match_journal_service_factory(...)` for explicit testable
  service wiring.
- Added journal request helpers for loopback checks, JSON parsing, context
  validation, required/optional text validation, service error mapping, and
  JSON-safe response shaping.
- Added `GET /journal` dispatch to `get_journal_bundle(...)`.
- Added POST dispatch for:
  - `/journal/notes`
  - `/journal/pilot-error`
  - `/journal/opponent-labels`
  - `/journal/review-flags`
  - `/journal/display-corrections`
- Added `do_POST(...)` and extracted `_send_json_response(...)`.
- Preserved existing GET route handling and existing response shapes.

`tests/test_match_journal_status_api.py`

- Added focused fake-service route tests for journal route inventory and method
  boundaries.
- Added validation tests for malformed JSON, unsupported/missing service
  wiring, non-loopback fail-closed behavior, query context parsing, attached
  note context requirements, and explicit unattached notes.
- Added route dispatch tests for note scopes, pilot-error status/reason,
  manual opponent labels, review flags, and display-only corrections.
- Added sanitized service-error envelope tests.
- Added an in-memory `MatchJournalService` test to prove SQLite rows returned
  through the route helper are JSON-safe without creating generated database
  files.

## Code Changed

Yes. Runtime code changed only in `src/mythic_edge_parser/app/status_api.py`.

Behavior surface changed:

- The local status API can now dispatch configured Match Journal journal routes
  when an explicit service factory is supplied and the configured host is a
  loopback host.

Behavior surfaces not changed:

- Parser behavior
- Parser state final reconciliation
- Parser event classes
- Match/game identity
- Deduplication
- Analytics schema, migrations, ingest, and views
- Workbook schema
- Webhook payload shape
- Apps Script behavior
- Google Sheets behavior
- Frontend/local app UI behavior
- OpenAI/model-provider behavior
- AI/coaching behavior
- Production behavior

## Tests Added Or Updated

Added:

- `tests/test_match_journal_status_api.py`

Existing tests were not edited.

## Interface Changes

Added local status API route support:

- `GET /journal`
- `POST /journal/notes`
- `POST /journal/pilot-error`
- `POST /journal/opponent-labels`
- `POST /journal/review-flags`
- `POST /journal/display-corrections`

Added helper seam:

- `configure_match_journal_service_factory(factory)`

No workbook columns, webhook fields, Apps Script functions, parser payload
fields, environment variables, SQLite schema, migrations, CLI entrypoints, or
frontend APIs changed.

## Contracted Area Status

The implementation stayed inside the contracted status API bridge area. It
dispatches to `MatchJournalService` and does not write direct SQL, infer parser
IDs from runtime state, read raw logs, read runtime status artifacts for journal
context, or create generated database files.

## Validation Run

Completed:

```powershell
py -m pytest -q tests\test_match_journal_status_api.py
# 18 passed

py -m pytest -q tests\test_match_journal_status_api.py tests\test_status_api.py
# 22 passed

py -m pytest -q tests\test_match_journal_status_api.py tests\test_status_api.py tests\test_match_journal_service.py
# 43 passed

py -m pytest -q tests\test_match_journal_schema.py tests\test_match_journal_repository.py tests\test_match_journal_service.py tests\test_status_api.py
# 66 passed

py -m ruff check src\mythic_edge_parser\app\status_api.py tests\test_match_journal_status_api.py
# passed

py -m ruff check src tests tools
# passed

py tools\check_agent_docs.py
# passed, checked_files 46, errors 0, warnings 0

git diff --check
# passed

new-file whitespace/ascii/final-newline check
# passed

@'
docs/contracts/match_journal_status_api.md
src/mythic_edge_parser/app/status_api.py
tests/test_match_journal_status_api.py
docs/implementation_handoffs/match_journal_status_api_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, scanned_paths 4, forbidden 0, warnings 0

@'
docs/contracts/match_journal_status_api.md
src/mythic_edge_parser/app/status_api.py
tests/test_match_journal_status_api.py
docs/implementation_handoffs/match_journal_status_api_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed, changed_paths 4, forbidden 0, warnings 0

Get-ChildItem -Recurse -File -Include *.sqlite,*.sqlite3,*.db,*.db-wal,*.db-shm,*.journal,*.sqlite-wal,*.sqlite-shm,*.sqlite-journal
# no output outside .git

git status --short --branch --untracked-files=all
# ## codex/analytics-foundation...origin/codex/analytics-foundation
#  M src/mythic_edge_parser/app/status_api.py
# ?? docs/contracts/match_journal_status_api.md
# ?? docs/implementation_handoffs/match_journal_status_api_comparison.md
# ?? tests/test_match_journal_status_api.py
```

## Protected-Surface Status

No protected parser/runtime/workbook/webhook/App Script/Sheets/analytics/UI/AI
or production surface was changed beyond the contracted local status API bridge.

## Generated Artifact Status

No SQLite database, WAL, SHM, journal file, raw log, failed post, runtime status
artifact, workbook export, secret, credential, webhook URL, local JSONL artifact,
or local-only artifact was created by this implementation pass.

## Still Unverified

- Live local HTTP startup with an actual production-like Match Journal service
  factory remains unconfigured and unverified.
- Future cockpit or overlay clients remain out of scope.
- Google Sheets sync/export remains out of scope.
- Live workbook state, deployed Apps Script state, OpenAI/model-provider state,
  and production behavior were not exercised.

## Reviewer Focus

Codex E should pay special attention to:

- Whether service-factory wiring is explicit enough for future runtime startup
  without creating a default database path in this slice.
- Whether journal routes fail closed strongly enough when not loopback-bound.
- Whether failure envelopes are sanitized and avoid raw note text, raw paths,
  raw payloads, secrets, and local artifacts.
- Whether `GET /journal` should treat empty bundles from service lookups as
  successful empty bundles or as not found under a future contract refinement.
- Whether `attachment_status` should remain excluded from route-level context
  until explicitly authorized.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #203:
Match Journal local HTTP/status API bridge.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/203

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Contract:
docs/contracts/match_journal_status_api.md

Implementation handoff:
docs/implementation_handoffs/match_journal_status_api_comparison.md

Review:
- src/mythic_edge_parser/app/status_api.py
- tests/test_match_journal_status_api.py
- tests/test_status_api.py
- tests/test_match_journal_service.py
- tests/test_match_journal_repository.py
- tests/test_match_journal_schema.py

Goal:
Review the implementation against docs/contracts/match_journal_status_api.md.
Lead with findings, ordered by severity. Confirm whether the implementation is
a thin loopback-only status API bridge over MatchJournalService, preserves
existing GET status API behavior, avoids direct SQL and default database files,
uses sanitized response envelopes, and does not change protected parser,
analytics, workbook, webhook, Apps Script, Sheets, UI, AI, or production
behavior.

Validation to run:
- py -m pytest -q tests\test_match_journal_status_api.py tests\test_status_api.py
- py -m pytest -q tests\test_match_journal_schema.py tests\test_match_journal_repository.py tests\test_match_journal_service.py tests\test_status_api.py
- py -m ruff check src tests tools
- git diff --check
- path-scoped protected-surface and secret/private-marker scans over changed
  files

Do not:
- Fix code unless explicitly routed as Codex D.
- Stage, commit, push, open a PR, merge, close issue #203, or mark tracker #202
  complete unless explicitly asked.
- Change parser/runtime/workbook/webhook/App Script/Sheets/analytics/UI/AI or
  production behavior.
- Create or commit SQLite/generated/private/runtime artifacts.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/203"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/match_journal_status_api.md"
  target_artifact: "docs/contract_test_reports/match_journal_status_api.md"
  implementation_handoff: "docs/implementation_handoffs/match_journal_status_api_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "py -m pytest -q tests\\test_match_journal_status_api.py -> 18 passed"
    - "py -m pytest -q tests\\test_match_journal_status_api.py tests\\test_status_api.py -> 22 passed"
    - "py -m pytest -q tests\\test_match_journal_status_api.py tests\\test_status_api.py tests\\test_match_journal_service.py -> 43 passed"
    - "py -m pytest -q tests\\test_match_journal_schema.py tests\\test_match_journal_repository.py tests\\test_match_journal_service.py tests\\test_status_api.py -> 66 passed"
    - "py -m ruff check src\\mythic_edge_parser\\app\\status_api.py tests\\test_match_journal_status_api.py -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "new-file whitespace/ascii/final-newline check -> passed"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "generated SQLite/database artifact check -> no output outside .git"
  stop_conditions:
    - "Do not target main."
    - "Do not change parser/runtime/workbook/webhook/App Script/Sheets/analytics/UI/AI/production behavior."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
    - "Do not expose arbitrary SQL, destructive database controls, raw paths, raw payloads, secrets, Google Sheets sync, workbook export, webhook posts, Apps Script calls, OpenAI calls, hidden-card inference, archetype classification, player-mistake truth, gameplay advice, merge readiness, or deploy readiness."
```
