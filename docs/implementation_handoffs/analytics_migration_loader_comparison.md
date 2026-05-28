# Analytics Migration Loader Implementation Handoff

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Artifact Used

Workflow handoff from Codex A for Analytics migration loader and package-data
access, represented for this pass by
`docs/contracts/analytics_migration_loader.md`.

## Contract Used

`docs/contracts/analytics_migration_loader.md`

## Branch And Git Status

Branch confirmed:

```text
codex/analytics-foundation
```

Initial status:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
?? docs/contracts/analytics_migration_loader.md
```

The untracked contract was treated as the supplied Codex B artifact. No
unrelated modified files were present at the start of this pass.

Final status after implementation:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
 M pyproject.toml
 M tests/test_analytics_schema.py
?? docs/contracts/analytics_migration_loader.md
?? docs/implementation_handoffs/analytics_migration_loader_comparison.md
?? src/mythic_edge_parser/app/analytics_migration_loader.py
?? src/mythic_edge_parser/app/analytics_migrations/__init__.py
?? tests/test_analytics_migration_loader.py
```

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/analytics_migration_loader.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_schema.py`
- `pyproject.toml`

## Current Behavior Compared To Contract

Current repo behavior already had the schema-first slice:

- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
  exists as the SQL schema source.
- `tests/test_analytics_schema.py` applies the migration to an in-memory
  SQLite database.
- `.gitignore` already ignores `data/analytics/`.

Contract gaps before this pass:

- No `analytics_migration_loader.py` module existed.
- `analytics_migrations` was not an importable package.
- `pyproject.toml` did not declare analytics SQL package data.
- Schema tests loaded SQL through a hardcoded repo-relative `Path`.
- Migration checksum/history insertion lived only in test helper code.
- No public loader API covered package-resource loading, deterministic
  discovery, idempotent reapply, checksum mismatch rejection, or open
  transaction boundaries.

## Implementation Option Chosen

Implemented the narrow package-resource migration loader authorized by the
contract:

- Added `src/mythic_edge_parser/app/analytics_migration_loader.py`.
- Added `src/mythic_edge_parser/app/analytics_migrations/__init__.py`.
- Added `pyproject.toml` package-data configuration for analytics `*.sql`.
- Added focused loader tests.
- Updated schema tests to use the loader instead of a repo-relative migration
  path.

The loader applies schema only. It does not implement live ingest, replay
ingest, a CLI, a default database opener, environment-variable path behavior,
runtime wiring, Google Sheets sync, Line Tracer, AI coaching, OpenAI runtime
integration, or production behavior.

## Files Changed

- `pyproject.toml`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/analytics_migrations/__init__.py`
- `tests/test_analytics_migration_loader.py`
- `tests/test_analytics_schema.py`
- `docs/implementation_handoffs/analytics_migration_loader_comparison.md`

Source artifact present but not edited by this implementation thread:

- `docs/contracts/analytics_migration_loader.md`

## Exact Loader, Package-Data, Test, And Doc Sections Changed

### `pyproject.toml`

Added:

```toml
[tool.setuptools.package-data]
"mythic_edge_parser.app.analytics_migrations" = ["*.sql"]
```

### `src/mythic_edge_parser/app/analytics_migrations/__init__.py`

Added a package marker so analytics SQL migrations are importable as package
resources.

### `src/mythic_edge_parser/app/analytics_migration_loader.py`

Added public constants:

- `ANALYTICS_SCHEMA_VERSION`
- `ANALYTICS_MIGRATIONS_PACKAGE`

Added public data/error shapes:

- `AnalyticsMigration`
- `AnalyticsMigrationError`

Added public functions:

- `iter_analytics_migrations()`
- `load_analytics_migration(migration_id: str)`
- `load_analytics_migration_sql(filename: str)`
- `apply_analytics_migrations(connection: sqlite3.Connection, *, applied_at: str | None = None)`

Behavior added:

- loads SQL through `importlib.resources`
- discovers approved `*.sql` migration resources deterministically
- rejects invalid or unsupported migration filenames
- rejects duplicate migration ids
- computes SHA-256 from exact UTF-8 SQL text
- applies migrations to caller-supplied SQLite connections
- records migration history in `schema_migrations`
- skips already-applied migrations with matching checksums
- rejects checksum mismatches without overwriting the stored checksum
- rejects application while the caller connection already has an open
  transaction
- rolls back its migration transaction if migration SQL is malformed before a
  history row is recorded

Transaction behavior:

- The loader rejects open caller transactions so it does not commit a caller's
  broader transaction.
- For each unapplied migration, the loader opens its own transaction, executes
  SQL statements, inserts the migration-history row, and commits that migration
  transaction.
- On SQLite errors, the loader rolls back its migration transaction and raises
  `AnalyticsMigrationError` with migration context.
- On loader-detected SQL parsing errors, the loader also rolls back its
  migration transaction and leaves migration history unrecorded.

### `tests/test_analytics_migration_loader.py`

Added focused tests for:

- package-resource loading through `importlib.resources`
- package-data configuration in `pyproject.toml`
- deterministic migration discovery and ordering
- SQL loading from package resources from a non-repo current working directory
- stable checksum shape
- migration application to an in-memory database
- schema table/view creation and history recording
- idempotent reapply
- preexisting same-checksum acceptance
- checksum mismatch rejection without overwrite
- missing package error behavior
- missing first migration error behavior
- invalid filename error behavior
- duplicate migration id error behavior
- open caller transaction rejection
- malformed SQL rollback without migration-history creation

### `tests/test_analytics_schema.py`

Updated the test-only migration helper to call `apply_analytics_migrations()`
and replaced hardcoded repo-path SQL reads with
`load_analytics_migration_sql()`.

### `docs/implementation_handoffs/analytics_migration_loader_comparison.md`

Added this handoff.

## Code Changed, Tests Changed, Docs-Only, Or Package-Data-Only

Code, tests, package-data config, and docs changed.

Runtime parser behavior did not change. The new Python code is an importable
analytics schema support module and is not wired into live runtime paths.

## Interface Changes

New local analytics support API:

```text
mythic_edge_parser.app.analytics_migration_loader
```

Public constants:

- `ANALYTICS_SCHEMA_VERSION`
- `ANALYTICS_MIGRATIONS_PACKAGE`

Public data/error shapes:

- `AnalyticsMigration`
- `AnalyticsMigrationError`

Public functions:

- `iter_analytics_migrations()`
- `load_analytics_migration(migration_id: str)`
- `load_analytics_migration_sql(filename: str)`
- `apply_analytics_migrations(connection: sqlite3.Connection, *, applied_at: str | None = None)`

No parser payloads, workbook fields, webhook payloads, Apps Script entrypoints,
environment variables, CLI commands, or runtime surfaces changed.

## Contract Matches

- Migration directory is importable as `mythic_edge_parser.app.analytics_migrations`.
- SQL migration is readable via `importlib.resources`, not a repo-relative
  path.
- `pyproject.toml` declares analytics `*.sql` package data.
- Loader discovers the approved migration set deterministically.
- Loader computes SHA-256 checksums from exact UTF-8 SQL.
- Loader applies the schema to a caller-supplied SQLite connection.
- Loader records `migration_id`, `migration_filename`, `checksum_sha256`,
  `applied_at`, and `schema_version_after`.
- Reapplying the same migration is idempotent.
- Preexisting same-checksum history is accepted.
- Preexisting different-checksum history is rejected without overwrite.
- Missing package/resource, invalid filename, duplicate migration id, and open
  transaction cases fail clearly.
- Malformed migration SQL rolls back without creating migration history.
- Existing schema tests still prove the schema behavior through the loader.
- No generated SQLite database files were created or committed.
- No live ingest, replay ingest, CLI, Google Sheets sync, Line Tracer, AI
  coaching, OpenAI runtime integration, parser behavior change, workbook schema
  change, webhook payload change, Apps Script change, or production behavior
  was introduced.

## Contract Mismatches

None known after this implementation.

## Missing Safeguards Or Tests

Remaining follow-up scope intentionally not implemented:

- No default database opener.
- No CLI.
- No production bootstrap command.
- No environment-variable path behavior.
- No live parser ingest.
- No saved-event replay ingest into SQLite.
- No future multi-migration manifest.

## Validation Run

Completed:

```text
py -m pytest -q tests/test_analytics_migration_loader.py tests/test_analytics_schema.py -> 27 passed
py -m pytest -q tests/test_analytics_sidecar.py tests/test_saved_event_replay.py -> 31 passed
py -m ruff check src tests tools -> All checks passed!
py -m build --version -> build 1.5.0 available
py -m build --wheel --outdir <temp> -> passed; wheel output included mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
```

The optional wheel-build command emitted pre-existing setuptools deprecation
warnings about `project.license` table/classifier metadata. The warnings were
not caused by this migration-loader change.

Final local gates after handoff creation:

```text
git status --short --branch -> showed intended changed files plus the supplied untracked contract
git diff --check -> passed
py tools/check_agent_docs.py -> passed; errors 0, warnings 0
path-scoped secret/private-marker scan over touched files -> forbidden 0, warnings 1
path-scoped protected-surface check over touched files -> forbidden 0, warnings 0
generated SQLite artifact status check -> no changed or untracked SQLite DB/journal/WAL/SHM artifacts found
```

## Protected-Surface Status

Local analytics loader/package-data/test/docs changes only.

Path-scoped protected-surface gate over touched files passed with forbidden 0
and warnings 0. No parser/runtime/workbook/webhook/App Script/protected
surfaces were intentionally touched.

## Secret And Private-Marker Status

Path-scoped secret/private-marker scan over touched files returned forbidden 0
and warnings 1. The warning is in the supplied contract's protected-surface
wording for failed-post payloads, not in executable code or generated data.

No secrets, raw logs, webhook URLs, workbook IDs, deployment IDs, generated
data, local runtime artifacts, workbook exports, or local source paths were
intentionally added.

## Generated SQLite Artifact Status

No changed or untracked SQLite database files, journal files, WAL files, SHM
files, or DB files were found. Tests use in-memory SQLite connections only.

The optional wheel build created local build scratch output, which was removed
after the validation command completed.

## Ingest, CLI, And Runtime Integration Status

No ingest, CLI, default database opener, runtime integration, Google Sheets
sync, Line Tracer, AI coaching, OpenAI runtime integration, or production
behavior was added.

## Still Unverified

- GitHub Actions were not run locally.
- Installed wheel was built and observed to include SQL, but it was not
  installed into a clean environment and imported from that wheel.
- Future multiple-migration behavior remains unimplemented beyond current
  duplicate/order/error checks.
- Live workbook state was not checked.
- Deployed Apps Script state was not checked.
- Production behavior was not checked.

## Forbidden Scope Touched

No forbidden scope was intentionally touched.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for the Analytics migration loader and package-data access implementation.

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_migration_loader.md

Implementation handoff:
docs/implementation_handoffs/analytics_migration_loader_comparison.md

Expected changed files:
- pyproject.toml
- src/mythic_edge_parser/app/analytics_migration_loader.py
- src/mythic_edge_parser/app/analytics_migrations/__init__.py
- tests/test_analytics_migration_loader.py
- tests/test_analytics_schema.py
- docs/implementation_handoffs/analytics_migration_loader_comparison.md

Source artifact present:
- docs/contracts/analytics_migration_loader.md

Task:
Review the implementation against docs/contracts/analytics_migration_loader.md. Lead with findings ordered by severity. Verify that the loader is local schema support only, uses package resources rather than repo-relative paths, preserves the existing SQL schema behavior, and does not add ingest, CLI, runtime integration, parser behavior, workbook/webhook/App Script changes, or production behavior.

Check especially:
- analytics_migrations is importable as a package resource location.
- pyproject.toml includes package data for analytics *.sql files.
- iter_analytics_migrations returns the approved migration set in deterministic order.
- load_analytics_migration_sql reads package resources and not hardcoded repo paths.
- checksums are exact SHA-256 digests of UTF-8 SQL text.
- apply_analytics_migrations records migration history and is idempotent.
- matching preexisting checksums are accepted.
- mismatched preexisting checksums are rejected without overwrite.
- missing package/resource, invalid filename, duplicate id, SQL failure, and open caller transaction behavior are clear and safe.
- tests do not create data/analytics/mythic_edge.sqlite3 or SQLite journal/WAL/SHM files.
- no raw Player.log payloads, raw saved-event lines, secrets, generated data, local runtime artifacts, workbook exports, or local-only artifacts were added.

Suggested validation:
git status --short --branch
py -m pytest -q tests/test_analytics_migration_loader.py tests/test_analytics_schema.py
py -m pytest -q tests/test_analytics_sidecar.py tests/test_saved_event_replay.py
py -m ruff check src tests tools
git diff --check
@'
src/mythic_edge_parser/app/analytics_migration_loader.py
src/mythic_edge_parser/app/analytics_migrations/__init__.py
src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
tests/test_analytics_migration_loader.py
tests/test_analytics_schema.py
pyproject.toml
docs/implementation_handoffs/analytics_migration_loader_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
src/mythic_edge_parser/app/analytics_migration_loader.py
src/mythic_edge_parser/app/analytics_migrations/__init__.py
src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
tests/test_analytics_migration_loader.py
tests/test_analytics_schema.py
pyproject.toml
docs/implementation_handoffs/analytics_migration_loader_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

Do not edit implementation in the review thread. Do not stage, commit, push, open a PR, merge, target main, create SQLite database files, or close issues unless explicitly asked.

Final output must include:
- role performed
- contract and handoff reviewed
- findings first
- contract matches
- contract mismatches
- missing safeguards or tests
- validation run and result
- protected-surface status
- secret/private-marker status
- generated SQLite artifact status
- remaining risks
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  role_performed: "Codex C: Module Implementer / comparison thread"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "workflow handoff from Codex A for Analytics migration loader and package-data access"
  contract_artifact: "docs/contracts/analytics_migration_loader.md"
  target_artifact: "docs/implementation_handoffs/analytics_migration_loader_comparison.md"
  branch: "codex/analytics-foundation"
  risk_tier: "Medium"
  files_changed:
    - "pyproject.toml"
    - "src/mythic_edge_parser/app/analytics_migration_loader.py"
    - "src/mythic_edge_parser/app/analytics_migrations/__init__.py"
    - "tests/test_analytics_migration_loader.py"
    - "tests/test_analytics_schema.py"
    - "docs/implementation_handoffs/analytics_migration_loader_comparison.md"
  source_artifact_present:
    - "docs/contracts/analytics_migration_loader.md"
  code_changed: true
  tests_changed: true
  docs_changed: true
  package_data_changed: true
  sqlite_database_files_created_or_committed: false
  ingest_or_cli_added: false
  validation:
    - "py -m pytest -q tests/test_analytics_migration_loader.py tests/test_analytics_schema.py -> 27 passed"
    - "py -m pytest -q tests/test_analytics_sidecar.py tests/test_saved_event_replay.py -> 31 passed"
    - "py -m ruff check src tests tools -> All checks passed!"
    - "py -m build --wheel --outdir <temp> -> passed; SQL included in wheel; temp output removed"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed; errors 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 1 on supplied contract protected-surface wording"
    - "path-scoped protected-surface check -> forbidden 0, warnings 0"
    - "generated SQLite artifact status check -> no changed or untracked SQLite DB/journal/WAL/SHM artifacts found"
  still_unverified:
    - "GitHub Actions"
    - "installed wheel import in clean environment"
    - "future multiple-migration manifest"
    - "live workbook state"
    - "deployed Apps Script state"
    - "production behavior"
  forbidden_scope_touched: false
  stop_conditions:
    - "Do not target main."
    - "Do not create or commit SQLite database files."
    - "Do not implement live ingest, replay ingest, CLI, Google Sheets sync, Line Tracer, AI coaching, OpenAI runtime integration, or production behavior."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
```
