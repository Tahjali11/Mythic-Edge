# Match Journal Service Implementation Comparison

## Summary

Codex C compared the current Match Journal state against
`docs/contracts/match_journal_service.md` for issue #200 and implemented the
smallest local service/use-case boundary required by the contract. Codex D then
fixed MJSVC-E-001, the Codex E partial-write validation blocker.

The implementation adds a human-intent service over the existing
`MatchJournalRepository`. It does not change the Match Journal SQL schema,
repository public behavior, parser behavior, runtime behavior, analytics
ingest/views, workbook/webhook/App Script surfaces, overlay behavior, Google
Sheets behavior, OpenAI/model-provider behavior, CI, merge policy, or deploy
policy.

## Findings First

- No blocking contract mismatches remain in the implemented #200 scope.
- No Match Journal schema or repository public-behavior change was needed.
- `journal_sheet_sync_queue` remains deferred and is neither created nor
  written.
- Service composite operations prevalidate service-owned command values before
  creating context containers, including invalid `note_format`, invalid common
  option enum values, invalid `flag_status`, invalid pilot-error status,
  invalid review flag type, empty notes, empty opponent labels, and invalid or
  missing display-correction values.

## Confirmed Matches

- `MATCH_JOURNAL_SERVICE_VERSION` is present with value
  `match_journal_service.v1`.
- Public service errors are present:
  `MatchJournalServiceError`, `MatchJournalServiceValidationError`,
  `MatchJournalServiceNotFoundError`, and
  `MatchJournalServiceConflictError`.
- `MatchJournalService` accepts an existing `MatchJournalRepository`.
- `MatchJournalService.from_connection` accepts a caller-owned
  `sqlite3.Connection`, optional deterministic repository seams, and explicit
  `ensure_schema=True` behavior.
- Service construction does not open the default Match Journal database path,
  read environment variables, or create files.
- Service operations do not read parser runtime state, status API state,
  local runtime artifacts, analytics tables, workbook exports, webhooks,
  Apps Script, Google Sheets, overlay state, or OpenAI/model-provider output.
- Attachment context resolution uses only caller-supplied values.
- Parser match/game IDs remain references only and are never invented.
- Parser-ID-only match/game contexts find or create journal containers, and
  duplicate parser-ID mappings raise a service conflict error.
- Explicit missing journal match/game IDs raise service not-found errors.
- Note operations cover match, game, sideboarding, and unattached notes.
- Pilot-error status and pilot-error reason remain separate current labels.
- Composite pilot-error review creates distinguishable status/reason/note rows
  when supplied.
- Opponent archetype/tier labels are manual labels only.
- Review flags are local review metadata only.
- Display corrections are constrained to `journal_display_only`.
- `get_journal_bundle` returns local repository data only, with fields:
  `match`, `games`, `notes`, `labels`, `review_flags`, `field_overrides`, and
  `warnings`.
- Service write results use the contracted semantic fields:
  `action`, `status`, `primary_record_type`, `primary_record_id`, `records`,
  and `warnings`.

## Changes Made

- Added `src/mythic_edge_parser/app/match_journal_service.py`.
- Added `tests/test_match_journal_service.py`.
- Added this handoff:
  `docs/implementation_handoffs/match_journal_service_comparison.md`.
- Codex D updated service validation to reject repository-sensitive command
  values before attachment context resolution can create journal containers.
- Codex D updated `docs/contract_test_reports/match_journal_service.md` to
  record the fixed MJSVC-E-001 state.

## Tests Added

`tests/test_match_journal_service.py` covers:

- service version and construction from repository
- construction from caller-owned connection with explicit schema ensure
- no default database path opening or environment-variable dependency
- match note behavior with parser match context
- game note behavior with parser match/game context
- sideboarding note behavior with existing game context
- unattached note preservation
- missing explicit journal match/game IDs raising service not-found
- duplicate parser match IDs raising service conflict
- experiment labels and match metadata update
- pilot-error status and reason remaining separately queryable
- pilot-error review prevalidation and distinguishable row creation
- manual opponent archetype/tier labels without classification
- review flags as local review metadata
- display-only correction proposals
- local-only journal bundles
- validation failures without partial row creation
- invalid `note_format` with parser context without partial row creation
- invalid or missing display-correction values with parser context without
  partial row creation
- invalid `flag_status` and invalid common option values without partial row
  creation
- deferred `journal_sheet_sync_queue`

## Contract Mismatches Fixed Or Still Open

Fixed:

- The service module was missing; it now exists.
- Focused service tests were missing; they now exist.
- MJSVC-E-001 was fixed: service validation failures no longer create partial
  journal containers before invalid note, flag, common option, or
  display-correction values are rejected.

Still open:

- None in the #200 implementation scope.

Deferred by contract:

- Overlay UI, local HTTP/status API routes, Google Sheets sync/export,
  `journal_sheet_sync_queue`, analytics joins, OpenAI/model-provider behavior,
  AI coaching, external website refresh, parser behavior,
  workbook/webhook/App Script behavior, and production behavior.

## Validation Run

- `python3 -m pytest -q tests/test_match_journal_service.py`
  - Passed: 21 tests.
- `python3 -m pytest -q tests/test_match_journal_schema.py`
  - Passed: 23 tests.
- `python3 -m pytest -q tests/test_match_journal_repository.py`
  - Passed: 18 tests.
- `python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py`
  - Passed: 14 tests.
- Direct partial-write repro:
  - Passed: invalid `note_format` and invalid `target_surface` both raised
    `MatchJournalServiceValidationError` with `journal_matches before=0 after=0`.
- `python3 -m ruff check src tests tools`
  - Passed.
- `git diff --check`
  - Passed with no output.
- Local SQLite/generated artifact scan:
  - Command:
    `find . -path './.git' -prune -o \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' -o -name '*.sqlite-journal' \) -print`
  - Passed: no matching artifacts printed.
- Path-scoped secret/private marker scan:
  - Command:
    `printf '%s\n' docs/contracts/match_journal_service.md docs/contract_test_reports/match_journal_service.md docs/implementation_handoffs/match_journal_service_comparison.md src/mythic_edge_parser/app/match_journal_service.py tests/test_match_journal_service.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`
  - Passed: scanned 5 paths, forbidden 0, warnings 0.
- Path-scoped protected-surface gate:
  - Command:
    `printf '%s\n' docs/contracts/match_journal_service.md docs/contract_test_reports/match_journal_service.md docs/implementation_handoffs/match_journal_service_comparison.md src/mythic_edge_parser/app/match_journal_service.py tests/test_match_journal_service.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`
  - Passed: changed paths 5, forbidden 0, warnings 0.
- No-index whitespace checks for untracked files:
  - Passed with no whitespace-error output for the contract, contract-test
    report, handoff, service module, and service tests.
- `git diff --cached --name-only`
  - Passed: no staged files printed.
- `python3 -m pytest -q`
  - Passed: 1412 tests.

## Remaining Risks And Unverified Layers

- The service is covered by focused in-memory SQLite tests but has not been
  wired to overlay UI, local HTTP/status API routes, Google Sheets sync/export,
  analytics joins, workbook/webhook/App Script surfaces, or OpenAI/model
  provider flows. This is intentional for #200.
- Composite operations are implemented with service-level prevalidation over
  repository operations. The repository still owns its own per-write
  transaction boundary, and the service does not add direct SQL or redesign
  repository transactions.
- `get_journal_bundle` is a local repository read model only. It does not join
  analytics tables or read runtime/parser state.
- Match Journal notes, labels, review flags, service results, and bundles
  remain human annotation outputs, not parser truth, analytics truth, gameplay
  advice, hidden-card inference, archetype classification, player-mistake
  truth, merge readiness, deploy readiness, or AI coaching.

## Next Recommended Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #200, Match Journal local service/use-case boundary.

Context:
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/200
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/198
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/199
- Branch: codex/match-journal-service
- Base: main
- Source contract: docs/contracts/match_journal_service.md
- Implementation handoff: docs/implementation_handoffs/match_journal_service_comparison.md
- Implemented files:
  - src/mythic_edge_parser/app/match_journal_service.py
  - tests/test_match_journal_service.py

Goal:
Review the #200 implementation against the Match Journal service contract.
Focus on contract fidelity, service API shape, attachment-context resolution,
composite operation prevalidation, privacy/local-only boundaries, bundle read
boundaries, test strength, and whether any schema, repository, parser,
analytics, runtime, overlay, Google Sheets, workbook/webhook/App Script, or AI
surface changed unexpectedly.

Do:
- Read the contract and handoff first.
- Review src/mythic_edge_parser/app/match_journal_service.py.
- Review tests/test_match_journal_service.py.
- Confirm the Match Journal SQL schema was not changed.
- Confirm repository public behavior was not changed.
- Confirm service construction does not open default database files, read
  environment variables, create generated artifacts, read parser/runtime/status
  state, or call external surfaces.
- Confirm parser IDs remain caller-provided references only.
- Confirm pilot-error status/reason remain separately queryable.
- Confirm opponent labels are manual annotations only.
- Confirm display corrections remain journal_display_only.
- Confirm get_journal_bundle is local-repository-only and does not join
  analytics/runtime/parser/overlay/Sheets/AI data.
- Run or verify:
  - python3 -m pytest -q tests/test_match_journal_schema.py
  - python3 -m pytest -q tests/test_match_journal_repository.py
  - python3 -m pytest -q tests/test_match_journal_service.py
  - python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py
  - python3 -m ruff check src tests tools
  - git diff --check
  - path-scoped secret/private marker and protected-surface checks
- Produce review findings first, then validation evidence, residual risks, and
  next recommended role.

Do not:
- Target main directly.
- Change Match Journal schema or repository public behavior unless a blocking
  mismatch routes back to Codex B.
- Create or commit SQLite/generated/private/runtime artifacts.
- Implement overlay, local HTTP/status API, Google Sheets sync/export,
  journal_sheet_sync_queue, analytics joins, OpenAI/model-provider behavior,
  AI coaching, external website refresh, parser behavior,
  workbook/webhook/App Script behavior, or production behavior.
- Let Match Journal records, service result shapes, or bundles become parser
  truth, analytics truth, gameplay advice, hidden-card inference, archetype
  classification, player-mistake labels, merge readiness, deploy readiness, or
  AI coaching.
- Stage or commit unless explicitly asked.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/200"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/198"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/199"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/match_journal_service.md"
  target_artifact: "docs/implementation_handoffs/match_journal_service_comparison.md"
  verdict: "mjsvc_e_001_fixed_ready_for_module_review"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/match-journal-service"
  validation:
    - "python3 -m pytest -q tests/test_match_journal_service.py -> 21 passed"
    - "python3 -m pytest -q tests/test_match_journal_schema.py -> 23 passed"
    - "python3 -m pytest -q tests/test_match_journal_repository.py -> 18 passed"
    - "python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py -> 14 passed"
    - "direct partial-write repro -> validation errors with journal_matches before=0 after=0"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed with no output"
    - "path-scoped secret/private marker scan -> passed, scanned 5 paths"
    - "path-scoped protected-surface gate -> passed, changed paths 5"
    - "no SQLite/generated database artifacts found"
    - "git diff --cached --name-only -> no staged files"
    - "python3 -m pytest -q -> 1412 passed"
  stop_conditions:
    - "Do not target main directly."
    - "Do not change Match Journal schema or repository public behavior unless a blocking mismatch routes back to Codex B."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
    - "Do not implement overlay, local HTTP/status API, Google Sheets sync/export, journal_sheet_sync_queue, analytics joins, OpenAI/model-provider behavior, AI coaching, external website refresh, parser behavior, workbook/webhook/App Script behavior, or production behavior."
    - "Do not let Match Journal records, service result shapes, or bundles become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching."
```
