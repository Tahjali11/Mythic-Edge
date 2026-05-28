# Analytics Migration Loader Contract

## Module

Local Analytics Foundation migration loader and package-data access.

This contract defines the next narrow step after the SQLite schema v1 slice:
repo-owned code may discover, load, checksum, and apply source-controlled SQL
migrations from package resources. It does not authorize analytics ingest, a
CLI, a generated database file, Google Sheets sync, Line Tracer, AI coaching,
or runtime OpenAI integration.

## Source Issue

Source artifact: workflow handoff from Codex A / Thinker for the
`Analytics migration loader and package-data access` slice.

Parent artifacts:

- `docs/problem_representations/local_analytics_foundation.md`
- `docs/problem_representations/analytics_schema_contract.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md`
- `docs/implementation_handoffs/analytics_local_sqlite_schema_fixer.md`

GitHub tracker: N/A in current source artifacts.

## Related ADRs

- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

## Owning Layer

Primary owner: local analytics foundation.

Truth boundaries:

- Parser/state still owns parser-managed match, game, card, gameplay, and
  reconciliation truth.
- The Player.log evidence ledger still owns provenance, confidence, finality,
  and drift context.
- The SQLite analytics schema owns local storage shape and migration history.
- The migration loader owns how SQL migration resources are discovered,
  checksummed, and applied to a caller-supplied SQLite connection.
- The loader must not become an ingest layer, parser layer, workbook layer,
  webhook layer, AI layer, or analytics truth layer.

Plain English: this module may make the existing SQL schema usable from Python
and from installed packages. It may not decide new facts, read raw logs, create
the production database by itself, or send anything downstream.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_migration_loader.md`

Future implementation files allowed by this contract:

- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/analytics_migrations/__init__.py`
- `src/mythic_edge_parser/app/analytics_migrations/*.sql`
- `pyproject.toml` package-data configuration for analytics SQL migrations
- `tests/test_analytics_migration_loader.py`
- focused updates to `tests/test_analytics_schema.py` only to replace
  hardcoded repo-path migration loading with the loader when useful
- `docs/implementation_handoffs/analytics_migration_loader_comparison.md`

Files not owned by this contract:

- parser modules under `src/mythic_edge_parser/parsers/`
- parser state/model/output modules except import-only test context if needed
- workbook schema, webhook, Apps Script, runtime sidecar, live runner, saved
  event replay ingest, fixture data, generated data, and production deployment
  files

## Observed Repo Behavior

Current branch: `codex/analytics-foundation`.

Current schema slice state:

- `.gitignore` ignores `data/analytics/`.
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
  exists as the first plain SQL schema migration.
- `tests/test_analytics_schema.py` applies that migration to an in-memory
  SQLite database.
- The schema tests record migration identity and SHA-256 checksum by using a
  test-only helper, not production loader code.
- The schema tests read the SQL file through a hardcoded repo-relative
  `Path("src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql")`.
- `src/mythic_edge_parser/app/analytics_migrations/` currently contains the SQL
  file but no `__init__.py`.
- `pyproject.toml` currently defines package discovery under `src`, but no
  package-data rule for analytics SQL files was observed.
- No production migration loader, migration package resource access, generated
  SQLite database, live ingest, replay ingest, CLI, environment-variable path
  override, Google Sheets sync, Line Tracer, AI coaching, or OpenAI runtime
  integration exists.

Current adjacent behavior:

- `src/mythic_edge_parser/app/analytics_sidecar.py` handles background runtime
  surface work and optional sheet-facing artifact posting. It does not ingest
  analytics facts into SQLite.
- Existing analytics schema tests are in-memory only and do not create
  `data/analytics/mythic_edge.sqlite3`.
- Existing saved-event replay reconstructs parser events but does not write
  SQLite facts.

## Public Interface

The future implementation should expose one small importable module:

```text
mythic_edge_parser.app.analytics_migration_loader
```

Required public constants:

- `ANALYTICS_SCHEMA_VERSION = "analytics_local_sqlite_schema.v1"`
- `ANALYTICS_MIGRATIONS_PACKAGE = "mythic_edge_parser.app.analytics_migrations"`

Required public data shape:

```text
AnalyticsMigration
```

`AnalyticsMigration` may be a frozen dataclass or equivalent typed structure
with these fields:

- `migration_id: str`
- `filename: str`
- `schema_version_after: str`
- `checksum_sha256: str`
- `sql: str`

Required public functions:

```text
iter_analytics_migrations() -> tuple[AnalyticsMigration, ...]
load_analytics_migration(migration_id: str) -> AnalyticsMigration
load_analytics_migration_sql(filename: str) -> str
apply_analytics_migrations(
    connection: sqlite3.Connection,
    *,
    applied_at: str | None = None,
) -> tuple[AnalyticsMigration, ...]
```

Allowed implementation details:

- `iter_analytics_migrations()` may discover `*.sql` files through
  `importlib.resources.files(ANALYTICS_MIGRATIONS_PACKAGE)` and a small
  version metadata map.
- `load_analytics_migration_sql()` must read from package resources, not from a
  repo-relative path.
- `apply_analytics_migrations()` may apply migrations to a caller-supplied
  `sqlite3.Connection`.
- The function may use the current UTC timestamp when `applied_at` is `None`,
  but tests must be able to pass a deterministic timestamp.

Forbidden interface expansion in this slice:

- no CLI command
- no default database opener
- no default write to `data/analytics/mythic_edge.sqlite3`
- no environment-variable path contract
- no live parser event ingest
- no saved-event replay ingest
- no row-mapping API from parser summaries to analytics facts
- no Google Sheets, webhook, Apps Script, Line Tracer, AI, or OpenAI API
  runtime interface

## Inputs

Migration resource inputs:

- Type: source-controlled SQL resource
- Source: `src/mythic_edge_parser/app/analytics_migrations/*.sql`
- Required first file:
  `0001_initial_analytics_schema.sql`
- Encoding: UTF-8
- Naming: monotonic numeric prefix plus descriptive suffix,
  `<four-digit-id>_<description>.sql`

Connection input:

- Type: `sqlite3.Connection`
- Source: caller-created connection
- Requirement: caller chooses in-memory, temporary-file, or future generated DB
  connection. This contract only authorizes tests to use in-memory or
  test-managed temporary databases.
- Requirement: loader must enable or preserve `PRAGMA foreign_keys = ON` before
  applying migrations.

Timestamp input:

- Type: optional string
- Source: explicit test value or loader-generated UTC timestamp
- Use: `schema_migrations.applied_at`

Out-of-scope inputs:

- raw Player.log payloads
- raw saved-event lines
- local raw log paths
- webhook URLs, workbook IDs, credentials, tokens, API keys, or secrets
- generated card data
- runtime status files
- failed-post queues
- workbook exports
- AI or LLM output

## Outputs

Loader outputs:

- `AnalyticsMigration` objects containing exact SQL text and SHA-256 checksum.
- Applied migration records in the caller-supplied database table
  `schema_migrations`.
- The unchanged table/view/index schema defined by the SQL migration files.

Package outputs:

- Analytics migration SQL files must be loadable through Python package
  resources in local editable/dev execution.
- The project packaging configuration must include analytics `*.sql` resources
  so later installed-package execution can find them.

Forbidden outputs:

- no `data/analytics/mythic_edge.sqlite3`
- no SQLite journal/WAL/SHM files committed to the repo
- no raw Player.log or raw saved-event storage
- no workbook/webhook payload changes
- no runtime status or failed-post artifacts
- no analytics reports, coaching text, or Line Tracer outputs

## Required Guarantees

### Package-Data Access

The migration directory must become an importable package resource location.

Required behavior:

- `mythic_edge_parser.app.analytics_migrations` must be importable or otherwise
  loadable through `importlib.resources`.
- The first migration SQL must be readable without referencing the repository
  root.
- `pyproject.toml` must declare the analytics SQL files as package data, such
  as by including `*.sql` for
  `mythic_edge_parser.app.analytics_migrations`.
- Tests must fail if the loader falls back to a hardcoded repo-relative path.

### Migration Discovery And Ordering

Required behavior:

- Discover only files matching the approved migration filename pattern.
- Apply migrations in ascending numeric-prefix order.
- Reject duplicate migration ids.
- Reject unexpected non-SQL resources if the implementation would otherwise
  treat them as migrations.
- Keep discovery deterministic across platforms.

The current approved migration set contains exactly:

```text
0001_initial_analytics_schema.sql
```

Future migrations are allowed only under future contracts.

### Checksum And History

Required behavior:

- Compute SHA-256 from the exact UTF-8 SQL text loaded from package resources.
- Record `migration_id`, `migration_filename`, `checksum_sha256`,
  `applied_at`, and `schema_version_after` in `schema_migrations`.
- If a migration is already recorded with the same checksum, skip reapplying it
  and return it as already satisfied.
- If a migration is already recorded with a different checksum, fail fast with
  a clear migration error.
- Do not overwrite an existing migration history row with a new checksum.

### Idempotency

Required behavior:

- Applying migrations once to an empty in-memory database creates the schema and
  records the migration.
- Applying migrations twice to the same connection converges to one
  `schema_migrations` row for `0001_initial_analytics_schema`.
- Reapplication must not duplicate tables, views, indexes, or migration rows.
- Reapplication must not hide schema drift by blindly swallowing SQL errors.

### Transaction And Failure Behavior

Required behavior:

- Malformed SQL must raise a clear exception.
- Missing migration resources must raise a clear exception.
- Checksum mismatch must raise a clear exception.
- Duplicate or out-of-order migration metadata must raise a clear exception.
- The loader must not record a migration as applied unless its SQL was applied
  successfully.
- The loader should avoid committing the caller's broader transaction. If
  SQLite limitations require a specific transaction behavior, Codex C must
  document it in the implementation handoff and cover the behavior with tests.

### Truth Ownership

Required behavior:

- The loader applies schema only. It does not turn parser outputs into facts.
- The loader must not generate SQL schema definitions in Python.
- The loader must not reinterpret parser facts, evidence-ledger labels, or
  analytics annotations.
- The loader must not store raw evidence; it records only migration metadata.

## Error Behavior

Missing migration package:

- Raise a loader-specific error or `RuntimeError` with a message that names the
  missing package/resource.

Missing first migration:

- Raise a clear error naming `0001_initial_analytics_schema.sql`.

Invalid filename:

- Ignore only clearly non-migration package metadata if unavoidable.
- Fail if a `*.sql` file has an invalid migration filename.

Checksum mismatch:

- Fail before applying later migrations.
- Do not alter the existing `schema_migrations` row.

SQL apply failure:

- Propagate the original SQLite error with enough context to identify the
  migration id or filename.
- Do not insert a success row into `schema_migrations`.

Contract ambiguity:

- Route back to Codex B before adding ingest, default DB creation, CLI,
  environment-variable behavior, or schema-changing SQL.

## Side Effects

Allowed side effects in future implementation:

- add the loader module
- make the migrations directory importable
- add package-data metadata for analytics SQL resources
- add focused loader tests
- update schema tests to use the loader
- create in-memory SQLite databases in tests
- create test-managed temporary SQLite databases only when needed for package
  access or idempotency proof
- write implementation handoff docs

Forbidden side effects:

- create or commit `data/analytics/mythic_edge.sqlite3`
- create or commit SQLite journal/WAL/SHM files
- change existing SQL table/view/index schema except where explicitly required
  by a future schema contract
- implement live ingest
- implement saved-event replay ingest
- implement a CLI
- implement environment-variable path configuration
- change parser behavior, parser state final reconciliation, parser events,
  match/game identity, deduplication, workbook schema, webhook payload shape,
  Apps Script behavior, output transport, production behavior, AI behavior, or
  model-provider behavior

## Dependency Order

Recommended Codex C implementation order:

1. Confirm branch and status on `codex/analytics-foundation`.
2. Inspect current SQL migration and schema tests.
3. Add `src/mythic_edge_parser/app/analytics_migrations/__init__.py`.
4. Add package-data configuration for analytics `*.sql` resources.
5. Add the minimal migration loader module.
6. Add focused loader tests for resource loading, ordering, checksum recording,
   idempotent reapply, and checksum mismatch.
7. Update schema tests to use the loader only if it reduces duplicate test-only
   migration logic.
8. Run focused analytics tests and protected-surface checks.
9. Write `docs/implementation_handoffs/analytics_migration_loader_comparison.md`.

## Compatibility

- Existing `0001_initial_analytics_schema.sql` remains the SQL schema source of
  truth.
- Existing analytics schema table, view, index, and vocabulary behavior must
  remain unchanged unless Codex C discovers a contract conflict and routes back.
- Existing schema tests should continue to prove the same schema guarantees.
- Existing parser row dictionaries remain unchanged.
- Existing workbook row keys remain unchanged.
- Existing webhook payload shape remains unchanged.
- Existing Apps Script behavior remains unchanged.
- Existing `analytics_sidecar.py` runtime behavior remains unchanged.
- Existing saved-event replay behavior remains unchanged.
- Existing evidence-ledger behavior remains unchanged.

## Tests Required

Future implementation should add focused tests under:

```text
tests/test_analytics_migration_loader.py
```

Required assertions:

- migration package can be loaded through `importlib.resources`
- `iter_analytics_migrations()` returns the first migration in deterministic
  order
- `load_analytics_migration_sql("0001_initial_analytics_schema.sql")` returns
  the source SQL text and not an empty string
- checksum is a stable 64-character lowercase hexadecimal SHA-256 digest
- applying migrations to an empty in-memory database creates required schema
  tables/views and records one `schema_migrations` row
- applying migrations twice to the same connection is idempotent
- a preexisting `schema_migrations` row with the same checksum is accepted
- a preexisting `schema_migrations` row with a different checksum is rejected
- missing package resource or missing first migration fails clearly
- tests do not create `data/analytics/` or committed SQLite files
- package-data configuration includes analytics SQL resources

Recommended validation:

```powershell
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
```

Optional validation if build tooling is available without adding a new required
dependency:

```powershell
py -m build --wheel
```

If optional wheel validation is skipped because `build` is not installed,
Codex C must say so in the handoff.

## Acceptance Criteria

- `docs/contracts/analytics_migration_loader.md` exists.
- The contract names package-data access and migration loading as the only
  authorized new behavior.
- Codex C implements a small loader that reads SQL migrations through package
  resources, not hardcoded repo paths.
- Analytics SQL migrations are included as package data.
- Applying the loader to an in-memory SQLite database creates the existing v1
  schema and records migration history.
- Applying the loader twice is idempotent.
- Checksum mismatches are rejected.
- The existing schema remains unchanged unless separately authorized.
- No generated SQLite database files are created or committed.
- No live ingest, replay ingest, CLI, Google Sheets sync, Line Tracer, AI
  coaching, OpenAI runtime integration, parser behavior change, workbook schema
  change, webhook payload change, Apps Script change, or production behavior is
  introduced.
- Codex C produces
  `docs/implementation_handoffs/analytics_migration_loader_comparison.md`.

## Unknowns

- Whether the loader should own transaction boundaries or leave them entirely
  to future database-open/bootstrap code.
- Whether future migrations should use a separate manifest file once there are
  multiple schema versions.
- Whether installed-wheel validation should become required later.
- Whether the eventual default database opener belongs in a separate
  `analytics_database.py`, `analytics_store.py`, or CLI contract.
- Whether future ingest should call the loader automatically or require an
  explicit bootstrap command.

## Suspected Implementation Gaps

- No migration loader module exists.
- The migration directory is not currently an importable package.
- Analytics SQL files are not currently declared as package data.
- Current schema tests load SQL through a hardcoded repo-relative path.
- Current migration history insertion is test-only helper behavior, not
  production loader behavior.
- No tests prove installed-package or package-resource access.
- No tests prove idempotent loader reapplication.
- No tests prove checksum mismatch rejection through a public loader API.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior
- parser state final reconciliation
- parser event classes
- event kind values
- parser payload shapes
- match identity
- game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- output transport
- live workbook state
- deployed Apps Script state
- production behavior
- AI truth
- model-provider behavior
- OpenAI API runtime integration
- Google Sheets sync
- Line Tracer behavior
- secrets, credentials, tokens, API keys, webhook URLs, or environment-variable
  contracts
- raw Player.log files or raw private Player.log excerpts
- generated card/tier data
- runtime status files
- failed posts
- workbook exports
- local-only artifacts

Allowed protected-surface-adjacent changes:

- `pyproject.toml` may be changed only to package analytics SQL migration
  resources.
- `src/mythic_edge_parser/app/analytics_migrations/__init__.py` may be added
  only to support package-resource loading.

## Validation Expectations For This Contract

This Codex B pass is documentation-only. Runtime tests are not required because
no runtime code should change.

Minimum contract-writer validation:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/analytics_migration_loader.md
'@ | py tools\check_secret_patterns.py --base HEAD --paths-from-stdin
@'
docs/contracts/analytics_migration_loader.md
'@ | py tools\check_protected_surfaces.py --base HEAD --paths-from-stdin
```

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for the Analytics migration loader and package-data access slice.

Branch:
codex/analytics-foundation

Source artifacts:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/analytics_local_sqlite_schema.md
- docs/contracts/analytics_migration_loader.md
- docs/implementation_handoffs/analytics_local_sqlite_schema_comparison.md
- docs/implementation_handoffs/analytics_local_sqlite_schema_fixer.md
- src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
- tests/test_analytics_schema.py
- pyproject.toml

Goal:
Compare the current repo to docs/contracts/analytics_migration_loader.md, then implement only the narrow migration-loader/package-data pieces needed for local analytics SQL migrations.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes.
- State what the migration loader is supposed to do, what current tests/code actually do, why package-data access is missing, and the exact minimal implementation plan.

Do:
- Make analytics SQL migrations loadable through importlib.resources/package data.
- Add a small migration loader module for discovering, loading, checksumming, and applying migrations to a caller-supplied sqlite3.Connection.
- Preserve the existing v1 SQL schema behavior.
- Add focused tests for package-resource loading, deterministic migration discovery, checksum recording, idempotent reapply, and checksum mismatch rejection.
- Update schema tests to use the loader if that removes hardcoded repo-path migration loading cleanly.
- Produce docs/implementation_handoffs/analytics_migration_loader_comparison.md.

Do not:
- create or commit data/analytics/mythic_edge.sqlite3 or any SQLite journal/WAL/SHM file
- implement live ingest, replay ingest, a CLI, a default database opener, environment-variable path behavior, Google Sheets sync, Line Tracer, AI coaching, OpenAI runtime integration, or production behavior
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts
- target main
- stage, commit, push, or open a PR unless explicitly asked

Validation:
py -m pytest -q tests/test_analytics_migration_loader.py tests/test_analytics_schema.py
py -m pytest -q tests/test_analytics_sidecar.py tests/test_saved_event_replay.py
py -m ruff check src tests tools
git diff --check
Run path-scoped secret and protected-surface checks over changed files with base origin/codex/analytics-foundation.

Final handoff must include:
- role performed
- source artifacts used
- files changed
- exact loader/package/test sections changed
- observed matches and remaining gaps against the contract
- validation run
- generated database artifact status
- protected-surface status
- what remains unverified
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "workflow handoff from Codex A for Analytics migration loader and package-data access"
  target_artifact: "docs/implementation_handoffs/analytics_migration_loader_comparison.md"
  branch: "codex/analytics-foundation"
  risk_tier: "Medium"
  validation:
    - "docs-only contract; runtime tests not required"
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped secret/private-marker check for docs/contracts/analytics_migration_loader.md"
    - "path-scoped protected-surface check for docs/contracts/analytics_migration_loader.md"
  stop_conditions:
    - "Do not target main."
    - "Do not create or commit SQLite database files."
    - "Do not implement live ingest, replay ingest, CLI, Google Sheets sync, Line Tracer, AI coaching, OpenAI runtime integration, or production behavior."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
    - "Do not change the existing schema SQL beyond separately authorized schema-contract work."
```
