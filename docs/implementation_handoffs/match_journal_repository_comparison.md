# Match Journal Repository Implementation Comparison

## Summary

Codex C compared the current Match Journal local schema boundary against
`docs/contracts/match_journal_repository.md` for issue #198 and implemented the
smallest repository layer required by the contract. Codex D then fixed the
MJREP-E-001 get/read contract mismatch reported by Codex E.

The implementation adds a caller-owned SQLite repository API for local human
journal records. It does not change the SQL schema, analytics migrations,
parser behavior, runtime behavior, workbook/webhook/App Script surfaces,
overlay behavior, Google Sheets behavior, OpenAI/model-provider behavior, CI,
merge policy, or deploy policy.

## Findings First

- No blocking contract mismatches remain in the implemented repository scope
  after the Codex D fixer pass.
- MJREP-E-001 is fixed: missing public `get_*` reads return `None`, while
  missing mutation targets continue to raise `MatchJournalNotFoundError`.
- No Match Journal SQL schema change was needed. The existing #196 schema
  already exposed the table families required by this contract.
- `journal_sheet_sync_queue` remains deferred and is neither created nor
  written by the repository.
- The current untracked #198 slice includes the Codex B contract, Codex C
  repository implementation and handoff, Codex E contract-test report, and this
  Codex D fixer update.

## Confirmed Matches

- `MATCH_JOURNAL_REPOSITORY_VERSION` is present with value
  `match_journal_repository.v1`.
- Public errors are present:
  `MatchJournalRepositoryError`, `MatchJournalValidationError`,
  `MatchJournalNotFoundError`, and `MatchJournalConflictError`.
- `ensure_match_journal_schema(connection, applied_at=None)` delegates to the
  existing migration loader and does not open a database file.
- `MatchJournalRepository` accepts a caller-owned `sqlite3.Connection`,
  `id_factory`, and `clock`.
- Repository construction and read/write operations do not open default
  database paths, read environment variables, or create local artifacts.
- Match, game, note, label, review-flag, reference-value, and field-override
  create/read/list/update surfaces are implemented.
- Public `get_*` reads return `None` for missing rows.
- Missing update, supersede, status-change, and internal post-write read
  failures continue to raise `MatchJournalNotFoundError`.
- Attachment validation preserves parser ID boundaries:
  attached matches require an existing parser match ID, and attached games
  require an existing parser game ID.
- Unattached notes remain valid and are preserved.
- Note supersession keeps the previous note row, marks it non-current, sets
  `valid_to`, and creates a new current note with `supersedes_note_id`.
- `set_current_label` expires prior current labels for the same attachment
  identity, scope, and label type while keeping pilot-error yes/no separate
  from pilot-error reason labels.
- Reference values support upsert and active/inactive filtering.
- Field overrides are restricted to `journal_display_only`.
- Write operations reject caller-open transactions with
  `MatchJournalConflictError`.
- Parameterized SQL is used for caller-provided values.

## Changes Made

- Added `src/mythic_edge_parser/app/match_journal_repository.py`.
- Added `tests/test_match_journal_repository.py`.
- Updated `docs/contract_test_reports/match_journal_repository.md` for the
  Codex D fixer pass.
- Added this handoff:
  `docs/implementation_handoffs/match_journal_repository_comparison.md`.

## Tests Added

`tests/test_match_journal_repository.py` covers:

- repository version and schema helper behavior
- match create/get/list/update/attachment behavior
- game create/get/list/update/attachment behavior
- unattached note preservation and note supersession
- current-label replacement and pilot-error label boundaries
- review flag create/update behavior
- reference value upsert and active filtering
- journal-display-only field overrides
- validation failures without partial rows
- missing public `get_*` reads returning `None`
- missing-row and unsupported-filter errors
- caller-open transaction conflict handling
- deferred `journal_sheet_sync_queue`

## Contract Mismatches Fixed Or Still Open

Fixed:

- The repository API was missing; it now exists.
- Focused repository tests were missing; they now exist.
- MJREP-E-001: missing public `get_*` reads raised
  `MatchJournalNotFoundError`; they now return `None` while missing mutation
  targets still raise.

Still open:

- None in the #198 implementation scope.

Deferred by contract:

- Overlay UI, local HTTP/status API routes, Google Sheets sync, analytics
  joins, OpenAI/model-provider behavior, parser behavior, workbook behavior,
  webhook behavior, Apps Script behavior, and production deployment behavior.
- `journal_sheet_sync_queue`.

## Validation Run

- `python3 -m pytest -q tests/test_match_journal_repository.py`
  - Passed: 18 tests.
- `python3 -m pytest -q tests/test_match_journal_schema.py`
  - Passed: 23 tests.
- `python3 -m pytest -q tests/test_analytics_schema.py`
  - Passed: 12 tests.
- `python3 -m ruff check src tests tools`
  - Passed.
- `git diff --check`
  - Passed.
- Direct missing-get repro:
  - Passed: all public `get_*` methods returned `None` for missing IDs.
- Path-scoped secret/private marker scan:
  - Command:
    `printf '%s\n' docs/contracts/match_journal_repository.md docs/contract_test_reports/match_journal_repository.md src/mythic_edge_parser/app/match_journal_repository.py tests/test_match_journal_repository.py docs/implementation_handoffs/match_journal_repository_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`
  - Passed: scanned 5 paths, forbidden 0, warnings 0.
- Path-scoped protected-surface gate:
  - Command:
    `printf '%s\n' docs/contracts/match_journal_repository.md docs/contract_test_reports/match_journal_repository.md src/mythic_edge_parser/app/match_journal_repository.py tests/test_match_journal_repository.py docs/implementation_handoffs/match_journal_repository_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`
  - Passed: changed paths 5, forbidden 0, warnings 0.
- No-index whitespace checks for untracked files:
  - Ran `git diff --no-index --check /dev/null <path>` for the contract,
    contract-test report, repository module, repository tests, and handoff.
  - Exit code was 1 as expected for file differences against `/dev/null`;
    no whitespace-error output was produced.
- Local SQLite/generated artifact scan:
  - Command:
    `find . -path './.git' -prune -o \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' \) -print`
  - Passed: no matching artifacts printed.
- `python3 -m pytest -q`
  - Passed: 1391 tests.

## Remaining Risks And Unverified Layers

- The repository is covered by focused unit tests but has not been exercised by
  a future overlay, local HTTP route, Google Sheets sync path, or Match Journal
  UI.
- No integration was added to analytics ingest or derived views; this is
  intentional for #198.
- No generated SQLite database artifact was created or committed.
- Human notes and labels remain local human annotation truth, not parser truth,
  analytics truth, gameplay advice, merge readiness, deploy readiness, or AI
  coaching.

## Next Recommended Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #198, Match Journal repository.

Context:
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/198
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/196
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/197
- Branch: codex/match-journal-repository
- Source contract: docs/contracts/match_journal_repository.md
- Implementation handoff: docs/implementation_handoffs/match_journal_repository_comparison.md
- Implemented files:
  - src/mythic_edge_parser/app/match_journal_repository.py
  - tests/test_match_journal_repository.py

Goal:
Review the #198 implementation and Codex D MJREP-E-001 fix against the Match
Journal repository contract. Focus on contract fidelity, missing public
`get_*` read behavior, SQLite transaction behavior, privacy/local-only
boundaries, test strength, and whether any schema or parser surface changed
unexpectedly.

Do:
- Read the contract and handoff first.
- Review src/mythic_edge_parser/app/match_journal_repository.py.
- Review tests/test_match_journal_repository.py.
- Confirm the SQL schema was not changed.
- Confirm repository operations do not open default database files, read
  environment variables, create generated artifacts, or treat human journal
  records as parser/analytics truth.
- Confirm missing public `get_*` operations return `None`.
- Confirm missing update/supersede/status-change targets still raise
  `MatchJournalNotFoundError`.
- Run or verify:
  - python3 -m pytest -q tests/test_match_journal_schema.py
  - python3 -m pytest -q tests/test_match_journal_repository.py
  - python3 -m pytest -q tests/test_analytics_schema.py
  - python3 -m ruff check src tests tools
  - git diff --check
  - path-scoped secret/private marker and protected-surface checks
- Produce review findings first, then validation evidence, residual risks, and
  next recommended role.

Do not:
- Target main directly.
- Change the Match Journal SQL schema unless a blocking mismatch routes back to
  Codex B.
- Create or commit SQLite/generated/private/runtime artifacts.
- Implement overlay, local HTTP/status API, Google Sheets sync, analytics
  joins, OpenAI/model-provider behavior, AI coaching, external website refresh,
  parser behavior, workbook/webhook/App Script behavior, or production
  behavior.
- Let Match Journal records become parser truth, analytics truth, gameplay
  advice, hidden-card inference, archetype classification, player-mistake
  labels, merge readiness, deploy readiness, or AI coaching.
- Stage or commit unless explicitly asked.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/198"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/196"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/197"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/match_journal_repository.md"
  target_artifact: "docs/implementation_handoffs/match_journal_repository_comparison.md"
  verdict: "mjrep_e_001_get_read_contract_mismatch_fixed_ready_for_module_review"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/match-journal-repository"
  validation:
    - "python3 -m pytest -q tests/test_match_journal_repository.py -> 18 passed"
    - "python3 -m pytest -q tests/test_match_journal_schema.py -> 23 passed"
    - "python3 -m pytest -q tests/test_analytics_schema.py -> 12 passed"
    - "direct missing-get repro -> all public get_* methods returned None"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped secret/private marker scan passed, scanned paths 5"
    - "path-scoped protected-surface gate passed, changed paths 5"
    - "no SQLite/generated database artifacts found"
    - "python3 -m pytest -q -> 1391 passed"
  fixed_findings:
    - "MJREP-E-001: missing public get_* operations now return None, while missing mutation targets still raise MatchJournalNotFoundError."
  stop_conditions:
    - "Do not target main directly."
    - "Do not change the Match Journal SQL schema unless a blocking mismatch routes back to Codex B."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
    - "Do not implement overlay, local HTTP/status API, Google Sheets sync, analytics joins, OpenAI/model-provider behavior, AI coaching, external website refresh, parser behavior, workbook/webhook/App Script behavior, or production behavior."
    - "Do not let Match Journal records become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching."
```
