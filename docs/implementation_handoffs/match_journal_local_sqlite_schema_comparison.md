# Match Journal Local SQLite Schema Implementation Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/196>

## Source Contract

`docs/contracts/match_journal_local_sqlite_schema.md`

## Role Performed

Codex C: Module Implementer.

Codex D: Module Fixer follow-up for MJSQL-001.

## Branch And Starting State

- Branch: `codex/match-journal-foundation`
- Base: `main`
- Starting HEAD: `aebd4f8`
- `HEAD...origin/main`: `0 0`
- Live GitHub state checked: issue #196 open.
- Starting worktree contained the untracked source contract
  `docs/contracts/match_journal_local_sqlite_schema.md`.

## Implementation Summary

Compared the current repo state against the Match Journal local SQLite schema
contract. Implemented the smallest local schema layer needed for v1:

- a Match Journal migration loader mirroring the analytics loader pattern
- a source-controlled v1 SQL migration
- focused in-memory SQLite tests
- `.gitignore` coverage for local/generated Match Journal DB artifacts
- this implementation handoff

The schema keeps Match Journal data human-owned and local. Parser
`match_id`/`game_id` values are references only; unattached notes can exist
without parser identity; field overrides are display-only proposals with
`effect_scope = journal_display_only`.

No parser behavior, parser state final reconciliation, parser event classes,
match/game identity, deduplication, analytics ingest, runtime status, status
API, workbook schema, webhook payload shape, Apps Script behavior, overlay
behavior, Google Sheets sync, OpenAI/model-provider behavior, merge policy, or
deploy policy was changed.

## Files Changed

- `.gitignore`
- `pyproject.toml`
- `src/mythic_edge_parser/app/match_journal_migration_loader.py`
- `src/mythic_edge_parser/app/match_journal_migrations/__init__.py`
- `src/mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql`
- `tests/test_match_journal_schema.py`
- `docs/contract_test_reports/match_journal_local_sqlite_schema.md`
- `docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md`

Source artifact present but not edited by this thread:

- `docs/contracts/match_journal_local_sqlite_schema.md`

## Contract-To-Code Comparison

### Confirmed Matches

- Added `MATCH_JOURNAL_SCHEMA_VERSION =
  "match_journal_local_sqlite_schema.v1"`.
- Added a journal-owned default database path constant:
  `data/match_journal/mythic_edge_journal.sqlite3`.
- Added `.gitignore` coverage for `data/match_journal/`.
- Added package-data coverage for
  `mythic_edge_parser.app.match_journal_migrations = ["*.sql"]` so the
  resource-based migration loader is not source-tree-only.
- Added plain SQL migration under
  `src/mythic_edge_parser/app/match_journal_migrations/`.
- Added journal-prefixed metadata tables:
  `journal_schema_migrations` and `journal_schema_versions`.
- Added required table families:
  `journal_matches`, `journal_games`, `journal_notes`,
  `journal_labels`, `journal_review_flags`, and
  `journal_reference_values`.
- Added `journal_field_overrides` as the authorized display-only correction
  proposal table.
- Kept `journal_sheet_sync_queue` deferred; no sync/export queue behavior was
  introduced.
- Used text primary keys, lowercase snake_case names, ISO-style timestamp
  text, and CHECK constraints for bounded vocabularies.
- Avoided foreign keys to analytics or parser tables so the Journal database
  remains separable.
- Tests use in-memory SQLite and synthetic values only.
- Tests prove the Journal schema can share an in-memory connection with the
  analytics schema without table-name collisions.

### Contract Mismatches Fixed

- No Match Journal migration loader existed; added one.
- No Match Journal SQL migration package existed; added one.
- MJSQL-001: no Match Journal SQL package-data declaration existed; added the
  narrow `pyproject.toml` entry authorized by the clarified contract.
- No generated-artifact ignore rule existed for Match Journal DB files; added
  `data/match_journal/`.
- No focused Match Journal schema tests existed; added
  `tests/test_match_journal_schema.py`.

### Missing Safeguards

None blocking. The implemented schema avoids raw Player.log payload fields,
runtime status JSON, failed posts, workbook exports, secrets, webhook URLs, and
model-provider response storage.

### Missing Or Weak Tests

No blocking gaps for this contract. Focused tests cover:

- migration package resource loading
- package-data declaration for Match Journal SQL migrations
- deterministic migration discovery and checksum
- SQL loading from any current working directory
- default generated DB path and ignore rule
- schema/history creation
- required tables, indexes, and columns
- idempotent migration application
- checksum mismatch rejection
- open transaction rejection
- invalid migration resource failure
- unattached notes without parser identity
- attached journal references without parser-table dependencies
- reference values and pilot-error vocabulary
- review flags as review tasks
- display-only field override proposals
- bounded vocabulary enforcement
- coexistence with analytics migrations in one in-memory SQLite connection

## Interface Changes

New local schema/migration-loader interface:

- `MATCH_JOURNAL_SCHEMA_VERSION`
- `MATCH_JOURNAL_MIGRATIONS_PACKAGE`
- `DEFAULT_MATCH_JOURNAL_DATABASE_PATH`
- `MatchJournalMigrationError`
- `MatchJournalMigration`
- `iter_match_journal_migrations()`
- `load_match_journal_migration(migration_id)`
- `load_match_journal_migration_sql(migration_id)`
- `apply_match_journal_migrations(connection, applied_at=None)`

No CLI, runtime route, status API route, environment variable, default database
opener, overlay route, Google Sheets sync, workbook export, webhook sender,
Apps Script interaction, parser callback, or model-provider interface was
added.

## Validation Run

```bash
python3 -m pytest -q tests/test_match_journal_schema.py
python3 -m pytest -q tests/test_analytics_migration_loader.py
python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py
python3 -m ruff check src tests tools
git diff --check
find data -type f \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*-wal' -o -name '*-shm' -o -name '*-journal' \) -print
```

Results recorded during implementation:

- `tests/test_match_journal_schema.py`: `23 passed`
- `tests/test_analytics_migration_loader.py`: `15 passed`
- analytics schema and replay-view harness suite: `14 passed`
- Ruff: `All checks passed!`
- `git diff --check`: passed with no output
- SQLite artifact scan: passed with no output

Additional validation to run after this handoff is written:

```bash
git diff --no-index --check /dev/null docs/contracts/match_journal_local_sqlite_schema.md
git diff --no-index --check /dev/null docs/contract_test_reports/match_journal_local_sqlite_schema.md
git diff --no-index --check /dev/null src/mythic_edge_parser/app/match_journal_migration_loader.py
git diff --no-index --check /dev/null src/mythic_edge_parser/app/match_journal_migrations/__init__.py
git diff --no-index --check /dev/null src/mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql
git diff --no-index --check /dev/null tests/test_match_journal_schema.py
git diff --no-index --check /dev/null docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md
printf '%s\n' \
  .gitignore \
  pyproject.toml \
  docs/contracts/match_journal_local_sqlite_schema.md \
  docs/contract_test_reports/match_journal_local_sqlite_schema.md \
  docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md \
  src/mythic_edge_parser/app/match_journal_migration_loader.py \
  src/mythic_edge_parser/app/match_journal_migrations/__init__.py \
  src/mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql \
  tests/test_match_journal_schema.py \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  .gitignore \
  pyproject.toml \
  docs/contracts/match_journal_local_sqlite_schema.md \
  docs/contract_test_reports/match_journal_local_sqlite_schema.md \
  docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md \
  src/mythic_edge_parser/app/match_journal_migration_loader.py \
  src/mythic_edge_parser/app/match_journal_migrations/__init__.py \
  src/mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql \
  tests/test_match_journal_schema.py \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 -m pytest -q
```

Additional validation results:

- no-index whitespace checks for the untracked contract, contract-test report,
  loader, migration package, SQL migration, test, and handoff files: passed
  with no output;
  `git diff --no-index` returned the expected diff-present status for added
  files
- Secret/private marker scan: `scanned_paths: 9`, `forbidden: 0`,
  `warnings: 2`, `result: warning`
- Secret scan warnings were both in the untracked contract's forbidden-input
  prose, referencing failed-post/payload artifacts as stop-condition text; no
  live secret or private artifact was reported.
- Protected-surface gate: `changed_paths: 9`, `forbidden: 0`, `warnings: 0`,
  `result: passed`
- Full pytest: `1373 passed`

## Still Unverified

- GitHub Actions were not run.
- No generated Match Journal SQLite database was created or opened.
- No live overlay, Google Sheets, workbook, webhook, Apps Script, runtime
  status, status API, OpenAI/model-provider, merge, or deploy behavior was
  checked.
- `journal_sheet_sync_queue` remains deferred to a future export/sync contract.
- Installed-wheel build inclusion was not separately verified because the local
  environment lacks the `build` module; the required setuptools package-data
  declaration is now present and covered by a focused test.

## Reviewer Focus

Codex E should focus on:

- whether the v1 schema keeps human annotations separate from parser and
  analytics facts
- whether unattached notes remain representable without invented parser IDs
- whether `journal_field_overrides` is safely constrained to
  `journal_display_only`
- whether the absence of `journal_sheet_sync_queue` is acceptable for this
  first schema slice
- whether MJSQL-001 is satisfied by the new `pyproject.toml` package-data entry
  and focused test coverage
- whether tests prove migration idempotency, bounded vocabularies, ignore-rule
  safety, and analytics-schema coexistence

## Next Recommended Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for issue #196, Match Journal local SQLite schema.

Context:
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/196
- Branch: codex/match-journal-foundation
- Base: main
- Source contract: docs/contracts/match_journal_local_sqlite_schema.md
- Implementation handoff: docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md
- Risk tier: Medium-High

Review:
- Verify the diff against the issue, contract, handoff, and tests.
- Lead with findings, if any.
- Confirm whether the implementation stays limited to local schema, migration loader, ignore rule, tests, and handoff documentation.
- Confirm whether Match Journal human annotations remain separate from parser facts and analytics truth.
- Confirm whether unattached notes can exist without parser match/game IDs.
- Confirm whether field override proposals are constrained to journal_display_only.
- Confirm whether bounded vocabularies, migration idempotency, generated-artifact ignore coverage, and analytics coexistence are sufficiently tested.
- Confirm whether MJSQL-001 is fixed: pyproject package data includes mythic_edge_parser.app.match_journal_migrations = ["*.sql"], with focused test coverage.

Suggested validation:
- python3 -m pytest -q tests/test_match_journal_schema.py
- python3 -m pytest -q tests/test_analytics_migration_loader.py
- python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py
- python3 -m ruff check src tests tools
- git diff --check

Do not:
- Fix code silently in review-only mode.
- Target main directly.
- Implement overlay behavior, Google Sheets sync, workbook export, webhook delivery, Apps Script behavior, OpenAI/model-provider behavior, analytics ingest changes, runtime status changes, status API routes, parser behavior changes, parser state final reconciliation changes, parser event changes, match/game identity changes, or deduplication changes.
- Create or commit SQLite/generated/private/runtime artifacts.
- Let Match Journal notes or human annotations become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/196"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/match_journal_local_sqlite_schema.md"
  target_artifact: "docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md"
  verdict: "mjsql_001_package_data_fixed_ready_for_module_review"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/match-journal-foundation"
  validation:
    - "python3 -m pytest -q tests/test_match_journal_schema.py -> 23 passed"
    - "python3 -m pytest -q tests/test_analytics_migration_loader.py -> 15 passed"
    - "python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py -> 14 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "SQLite artifact scan -> passed with no output"
    - "no-index whitespace checks for untracked contract/report/loader/migration/test/handoff files -> passed with no output"
    - "path-scoped secret/private marker scan -> warning only: scanned paths 9, forbidden 0, warnings 2 in contract stop-condition prose"
    - "path-scoped protected-surface gate -> passed, changed paths 9"
    - "python3 -m pytest -q -> 1373 passed"
  stop_conditions:
    - "Do not target main directly."
    - "Do not implement overlay behavior, Google Sheets sync, workbook export, webhook delivery, Apps Script behavior, OpenAI/model-provider behavior, analytics ingest changes, runtime status changes, status API routes, parser behavior changes, parser state final reconciliation changes, parser event changes, match/game identity changes, or deduplication changes."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
    - "Do not let Match Journal notes or human annotations become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching."
```
