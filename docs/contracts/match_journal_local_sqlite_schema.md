# Match Journal Local SQLite Schema Contract

## Module

Match Journal Foundation local SQLite schema v1.

This contract defines the first local Match Journal schema for human-entered
match context, notes, labels, review flags, experiment metadata, and future
correction annotations. It is a schema and boundary contract only. It does not
implement UI, overlay behavior, Google Sheets sync, OpenAI/runtime model
integration, parser behavior, workbook behavior, webhook behavior, or Apps
Script behavior.

Plain English: the Match Journal is where a person can write down what they
think, what they want to review, and how they want to label a match. It does
not get to decide what the parser says happened.

## Source Issue

Issue:

- https://github.com/Tahjali11/Mythic-Edge/issues/196

Completed prior tracker:

- https://github.com/Tahjali11/Mythic-Edge/issues/190

Adjacent issues that must remain separate:

- https://github.com/Tahjali11/Mythic-Edge/issues/158
- https://github.com/Tahjali11/Mythic-Edge/issues/41

Branch:

```text
codex/match-journal-foundation
```

Base:

```text
main
```

Verified prior integration:

```text
aebd4f8e121362d5b595f460068f626985c1ade0
```

## Related Authority

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`
- `docs/problem_representations/local_analytics_foundation.md`
- `docs/contracts/analytics_local_sqlite_schema.md`
- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `docs/contracts/analytics_derived_sql_views.md`
- `docs/contracts/analytics_replay_view_validation_harness.md`

## Risk Tier

Medium-High.

Reasons:

- The schema is local-only, but it stores human annotations that future UI,
  overlay, Google Sheets, analytics, and AI surfaces may want to read.
- It references parser match/game identity and therefore must not blur parser
  facts with human notes.
- It may eventually support correction-style review data, which is useful but
  dangerous if treated as parser fact replacement.
- It introduces generated SQLite artifacts that must remain ignored and
  private.

## Owning Layer And Truth Boundary

Primary owning layer: Match Journal Foundation.

The Match Journal owns:

- local human-entered notes
- local human-entered match and game labels
- local review flags and review status
- local experiment labels
- local pilot-error yes/no labels and reasons
- local sideboarding notes
- local dropdown/reference values for journal entry ergonomics
- local display-only field correction proposals, if implemented
- local export/sync readiness metadata, if implemented as an inert queue

The Match Journal does not own:

- parser event interpretation
- parser state final reconciliation
- parser match identity
- parser game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync behavior
- overlay behavior
- runtime status schema
- analytics truth
- AI truth
- OpenAI/model-provider behavior
- gameplay advice
- player-mistake labels as facts
- hidden-card inference
- archetype classification as an inferred fact
- merge readiness
- deploy readiness

Truth boundaries:

- Parser/state remains the only owner of parser-managed match/game facts.
- Local analytics SQLite owns durable deterministic storage and read-only
  derived views for parser-normalized facts.
- The Player.log evidence ledger owns provenance vocabulary and review evidence
  for parser facts.
- The Match Journal owns human-entered context and review metadata.
- Google Sheets, overlays, dashboards, Match Journal UI, OpenAI/model-provider
  output, and other collaboration surfaces may consume journal data only under
  later contracts.

Plain English: a journal row can say "I think this was a mistake" or "label this
match as Esper Control for my review." It cannot rewrite the parser's match row
or make AI coaching true.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/match_journal_local_sqlite_schema.md`

Future implementation files authorized by this contract:

- `.gitignore`, only to ignore local/generated Match Journal database artifacts
- `pyproject.toml`, only to include Match Journal SQL migrations as package
  data
- `src/mythic_edge_parser/app/match_journal_migration_loader.py`
- `src/mythic_edge_parser/app/match_journal_migrations/__init__.py`
- `src/mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql`
- `tests/test_match_journal_schema.py`
- `docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md`

Optional future implementation files, if Codex C can justify them as narrow
schema support without runtime behavior:

- `src/mythic_edge_parser/app/match_journal_schema.py`

Files not owned by this contract:

- parser modules
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_migrations/*.sql`
- workbook schema, webhook delivery, Apps Script, overlay UI, Google Sheets
  sync, OpenAI/model-provider integrations, generated SQLite databases, raw
  logs, runtime status files, failed posts, workbook exports, generated card
  data, and private/local artifacts

If Codex C finds that runtime wiring, overlay routes, Google Sheets sync,
analytics ingest changes, environment-variable contracts, OpenAI behavior, or
parser changes are necessary, it must stop and route to a new contract.

## Public Interface

### Generated Database Path

Default local Match Journal database path:

```text
data/match_journal/mythic_edge_journal.sqlite3
```

The database file and all adjacent SQLite artifacts are local-only. They must
not be committed.

Required ignore coverage:

```text
data/match_journal/
```

This contract does not authorize a new environment variable. A future contract
may add a `MYTHICEDGE_MATCH_JOURNAL_DB_PATH`-style override, but v1 should be
testable through caller-supplied SQLite connections and in-memory databases.

### Migration Path

Versioned plain SQL migrations must live under:

```text
src/mythic_edge_parser/app/match_journal_migrations/
```

Required first migration name:

```text
0001_initial_match_journal_schema.sql
```

Generated SQLite database files are not source-controlled schema definitions.
The SQL migration is the source-controlled schema definition.

### SQL Package Data

The Match Journal migration loader is a public resource-based API. Its SQL
migration files must therefore be available in installed package contexts, not
only in an editable source tree.

Required package-data entry:

```toml
[tool.setuptools.package-data]
"mythic_edge_parser.app.match_journal_migrations" = ["*.sql"]
```

This contract authorizes a narrow `pyproject.toml` change for that package-data
entry only. It does not authorize dependency changes, build-backend changes,
entry points, scripts, environment-variable contracts, package renames, runtime
wiring, or distribution policy changes.

Focused tests must cover the package-data declaration, analogous to the
analytics migration-loader test that protects
`mythic_edge_parser.app.analytics_migrations = ["*.sql"]`.

### Schema Version

Logical schema version:

```text
match_journal_local_sqlite_schema.v1
```

The version string must be recorded in a journal-owned schema metadata table.
Use journal-prefixed metadata table names so the schema can be tested in the
same in-memory SQLite connection as analytics without table-name collisions.

Recommended metadata tables:

- `journal_schema_migrations`
- `journal_schema_versions`

### Migration Loader API

Codex C may add a small migration loader matching the analytics migration
loader pattern.

Required public constant:

```text
MATCH_JOURNAL_SCHEMA_VERSION = "match_journal_local_sqlite_schema.v1"
```

Required public functions:

```text
iter_match_journal_migrations() -> tuple[MatchJournalMigration, ...]
load_match_journal_migration(migration_id: str) -> MatchJournalMigration
load_match_journal_migration_sql(migration_id: str) -> str
apply_match_journal_migrations(
    connection: sqlite3.Connection,
    *,
    applied_at: str | None = None,
) -> tuple[MatchJournalMigration, ...]
```

The exact migration dataclass name may vary, but the public behavior must be
documented and covered by focused tests.

Forbidden public interfaces in this slice:

- no CLI
- no daemon
- no status API route
- no overlay route
- no Google Sheets sync
- no workbook export
- no webhook post
- no OpenAI/model-provider call
- no parser callback
- no live default database opener required by runtime
- no environment-variable contract

## Observed Current Behavior

Repository state observed for this contract:

- Issue #196 is the active Match Journal Foundation problem representation.
- Tracker #190 is closed after the Local Analytics Foundation integration.
- Issue #158 remains open for corpus/reference expansion.
- Issue #41 remains open for downstream ML/OpenAI research.
- `docs/contracts/analytics_local_sqlite_schema.md` defines local analytics
  SQLite schema v1.
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
  creates analytics fact, annotation, provenance, and derived-view tables.
- Existing analytics annotation tables include `matchup_labels`,
  `archetype_labels`, and `game_notes`.
- Those analytics annotation tables are attached to analytics facts, not a full
  Match Journal ownership layer.
- `src/mythic_edge_parser/app/analytics_migration_loader.py` provides a
  migration-loader pattern that the Match Journal implementation can mirror.
- `.gitignore` ignores `data/analytics/`.
- No Match Journal migration package exists.
- No Match Journal migration loader exists.
- No `data/match_journal/` ignore rule exists.
- No `tests/test_match_journal_schema.py` exists.
- Runtime status and status API modules do not expose a Match Journal surface.

Observed gap:

- The repo has analytics storage and limited human annotation tables, but it
  does not yet have a durable local schema contract for broad human-entered
  Match Journal data.
- The repo does not yet define how unattached human notes survive without
  inventing parser match/game identity.
- The repo does not yet define a safe display-only boundary for future human
  field correction proposals.

## Required Schema Guarantees

### Storage Boundary

The v1 Match Journal schema should be a separate local SQLite schema with its
own migration loader and generated database path.

Reasons:

- Journal data is human-entered and mutable.
- Parser-normalized analytics facts are deterministic copies of parser output.
- Keeping the first Journal database separate prevents human notes from being
  mistaken for parser or analytics fact tables.
- Future integrations may join or export journal data, but those are separate
  contracts.

Codex C may test journal migrations in the same in-memory SQLite connection as
analytics migrations to prove table-name compatibility, but the default
generated database path must remain journal-specific.

### Table Families

The first schema must support these table families, either with the exact table
names below or with an implementation handoff explaining any narrower safe
name choice.

Required table families:

- `journal_schema_migrations`
- `journal_schema_versions`
- `journal_matches`
- `journal_games`
- `journal_notes`
- `journal_labels`
- `journal_review_flags`
- `journal_reference_values`

Conditionally authorized table families:

- `journal_field_overrides`
- `journal_sheet_sync_queue`

`journal_field_overrides` is authorized only as display-only correction
proposal metadata. It must not update parser facts, analytics facts, workbook
rows, webhook payloads, runtime status, overlay output, or Google Sheets.

`journal_sheet_sync_queue` is authorized only as inert local export/sync
readiness metadata. It must not perform Google Sheets sync, workbook export,
webhook delivery, network I/O, or Apps Script behavior.

### Common Column Rules

Journal tables that represent user-authored data should carry:

- stable text primary key
- `created_at`
- `updated_at`
- `author_label`
- `source_surface`
- `is_current`, when a table supports supersession/history
- `valid_from`
- `valid_to`
- `privacy_label`

Allowed `source_surface` values in v1:

- `manual`
- `imported_review`
- `local_tool`
- `test_fixture`

Allowed `privacy_label` values in v1:

- `local_private`
- `sanitized_fixture`
- `shareable_summary`

Default `privacy_label` for human journal data:

```text
local_private
```

No v1 migration may create a table intended to store raw Player.log payloads,
raw submitted deck payloads, runtime status JSON, failed posts, workbook
exports, API keys, tokens, credentials, webhook URLs, or model-provider
responses.

### Attachment Model

The schema must allow journal entries to attach to parser identities when those
identities are known, but it must also preserve unattached entries.

Recommended attachment columns:

- `journal_match_id`
- `journal_game_id`
- `parser_match_id`
- `parser_game_id`
- `game_number`
- `attachment_status`

Allowed `attachment_status` values:

- `attached`
- `unattached`
- `pending`
- `ambiguous`
- `detached`

Rules:

- `journal_match_id` and `journal_game_id` are journal-owned stable IDs.
- `parser_match_id` and `parser_game_id` are references to parser-owned IDs.
- Missing parser IDs must not cause data loss.
- Unattached notes must remain queryable and editable.
- The journal must not invent parser match IDs or parser game IDs.
- Attaching an existing note to a parser match/game later must be represented as
  a journal update, not a parser identity mutation.
- Detached entries must preserve prior journal history.

### Match-Level Records

`journal_matches` should represent a journal-owned match container.

Expected fields include:

- `journal_match_id`
- `parser_match_id`
- `attachment_status`
- `title`
- `experiment_id`
- `review_status`
- `created_at`
- `updated_at`
- `author_label`
- `source_surface`
- `privacy_label`

Allowed `review_status` values:

- `not_reviewed`
- `needs_review`
- `reviewing`
- `reviewed`
- `archived`

`experiment_id` is a human label. It must not become parser fact, deck identity,
matchup truth, or analytics truth without a later contract.

### Game-Level Records

`journal_games` should represent a journal-owned game container.

Expected fields include:

- `journal_game_id`
- `journal_match_id`
- `parser_match_id`
- `parser_game_id`
- `game_number`
- `attachment_status`
- `review_status`
- `created_at`
- `updated_at`
- `author_label`
- `source_surface`
- `privacy_label`

Rules:

- `game_number` is optional for unattached or ambiguous entries.
- A journal game may reference a parser game, but it must not redefine parser
  game identity.
- Deleting or archiving a journal game must not delete parser or analytics rows.

### Notes

`journal_notes` should store human-authored note text.

Expected fields include:

- `journal_note_id`
- `journal_match_id`
- `journal_game_id`
- `parser_match_id`
- `parser_game_id`
- `note_scope`
- `note_text`
- `note_format`
- `author_label`
- `source_surface`
- `privacy_label`
- `is_current`
- `supersedes_note_id`
- `valid_from`
- `valid_to`
- `created_at`
- `updated_at`

Allowed `note_scope` values:

- `match`
- `game`
- `sideboarding`
- `turn`
- `action`
- `general`
- `unattached`

Allowed `note_format` values:

- `plain_text`
- `markdown`

Notes may include human analysis or opinions. They must not be parsed back into
parser facts by this module.

### Structured Labels

`journal_labels` should store human-authored structured labels.

Expected fields include:

- `journal_label_id`
- `journal_match_id`
- `journal_game_id`
- `parser_match_id`
- `parser_game_id`
- `label_scope`
- `label_type`
- `label_value`
- `reference_id`
- `author_label`
- `source_surface`
- `privacy_label`
- `is_current`
- `valid_from`
- `valid_to`
- `created_at`
- `updated_at`

Allowed `label_scope` values:

- `match`
- `game`
- `sideboarding`
- `review`
- `experiment`
- `opponent`
- `unattached`

Allowed `label_type` values:

- `matchup_label`
- `opponent_archetype`
- `opponent_archetype_tier`
- `experiment_id`
- `pilot_error`
- `pilot_error_reason`
- `review_status`
- `sideboarding_label`
- `custom`

Allowed `pilot_error` label values:

- `yes`
- `no`
- `unknown`
- `not_reviewed`

Rules:

- Human opponent archetype and tier labels are user annotations, not automatic
  archetype classification.
- `custom` labels are local annotation labels only and must not silently become
  workbook columns, webhook fields, parser facts, or analytics truth.
- Label history should be preserved through `is_current`, `valid_from`, and
  `valid_to` rather than destructive overwrites where practical.

### Review Flags

`journal_review_flags` should store review tasks and flags.

Expected fields include:

- `journal_review_flag_id`
- `journal_match_id`
- `journal_game_id`
- `parser_match_id`
- `parser_game_id`
- `flag_type`
- `flag_status`
- `priority_label`
- `reason`
- `author_label`
- `source_surface`
- `privacy_label`
- `created_at`
- `updated_at`

Allowed `flag_type` values:

- `needs_review`
- `interesting_match`
- `suspected_parser_gap`
- `sideboarding_review`
- `pilot_error_review`
- `custom`

Allowed `flag_status` values:

- `open`
- `in_progress`
- `resolved`
- `dismissed`
- `archived`

Rules:

- `suspected_parser_gap` is a review flag, not proof of parser error.
- Review flags must not become CI truth, merge readiness, deploy readiness, or
  parser correctness truth.

### Reference Values

`journal_reference_values` should store local dropdown/reference values.

Expected fields include:

- `reference_id`
- `reference_type`
- `label`
- `description`
- `sort_order`
- `is_active`
- `created_at`
- `updated_at`

Allowed initial `reference_type` values:

- `review_status`
- `pilot_error_reason`
- `opponent_archetype_tier`
- `sideboarding_label`
- `experiment_id`
- `custom_label`

Rules:

- Reference values are local UX helpers and should be user-maintained or
  repo-seeded with generic safe values.
- This contract does not authorize scraping, external website refresh,
  archetype-list downloads, OpenAI-generated labels, card rating imports, or
  metagame classification services.

### Field Override Proposals

`journal_field_overrides`, if implemented in v1, must be display-only proposal
metadata.

Expected fields include:

- `journal_field_override_id`
- `journal_match_id`
- `journal_game_id`
- `parser_match_id`
- `parser_game_id`
- `target_surface`
- `target_field`
- `original_value_label`
- `proposed_value_label`
- `override_reason`
- `override_status`
- `effect_scope`
- `author_label`
- `source_surface`
- `privacy_label`
- `created_at`
- `updated_at`

Allowed `target_surface` values:

- `match_log_row`
- `game_log_row`
- `action_log_row`
- `analytics_view`
- `journal_display`

Allowed `override_status` values:

- `proposed`
- `accepted_for_journal_display`
- `rejected`
- `superseded`
- `archived`

Required `effect_scope` value in v1:

```text
journal_display_only
```

Rules:

- Field overrides must not update parser facts.
- Field overrides must not update analytics fact tables.
- Field overrides must not update workbook rows, webhook payloads, Apps
  Script, runtime status, overlay output, or Google Sheets.
- A field override may be useful review evidence later, but only under a new
  contract.

### Export Or Sync Queue Metadata

`journal_sheet_sync_queue`, if implemented in v1, must be inert local metadata.

Expected fields include:

- `journal_sync_queue_id`
- `journal_entity_type`
- `journal_entity_id`
- `target_surface`
- `operation`
- `status`
- `last_error_label`
- `created_at`
- `updated_at`

Allowed `target_surface` values:

- `google_sheets`
- `local_export`
- `overlay_review`

Allowed `status` values:

- `pending`
- `skipped`
- `exported`
- `failed`

Rules:

- The table may record that something is ready for a future export path.
- The implementation must not perform Google Sheets sync, workbook export,
  overlay update, webhook delivery, network I/O, Apps Script calls, or status
  API changes.
- Error labels must be sanitized labels, not raw exception dumps containing
  secrets, file paths, raw logs, or private payloads.

## Input Rules

Allowed inputs for future Codex C implementation:

- synthetic test values
- caller-supplied in-memory SQLite connections
- optional local generated Match Journal database path, if used only for
  documentation/constants and ignored artifacts
- human-entered note text
- human-entered structured labels
- human-entered review flags
- human-entered experiment IDs
- human-entered pilot-error yes/no and reason labels
- human-entered sideboarding notes
- parser `match_id` and `game_id` references, when already available from
  parser-normalized rows or local review context

Forbidden inputs in this slice:

- raw Player.log payloads
- raw private submitted deck payloads
- raw local runtime status files
- failed posts
- workbook exports
- generated card data
- secrets, credentials, API keys, tokens, and webhook URLs
- OpenAI/model-provider responses
- external website scraped archetype lists
- hidden-card inference
- AI-generated gameplay advice
- live Google Sheets data

## Output Rules

Allowed outputs:

- source-controlled SQL migration files
- source-controlled migration loader code
- source-controlled focused tests
- source-controlled implementation handoff
- generated local SQLite databases under ignored `data/match_journal/`, only if
  future local use creates them

Forbidden outputs:

- committed `.sqlite`, `.sqlite3`, `.db`, `.db-wal`, `.db-shm`, `.journal`, or
  other generated database artifacts
- committed raw Player.log excerpts
- committed local notes copied from private play sessions
- committed workbook exports
- committed runtime status files
- committed failed posts
- committed secrets, credentials, tokens, API keys, or webhook URLs
- workbook schema changes
- webhook payload changes
- Apps Script changes
- overlay changes
- Google Sheets sync changes
- OpenAI/model-provider behavior

## Compatibility Expectations

The Match Journal schema must:

- be deterministic and testable with in-memory SQLite
- apply migrations idempotently
- use text IDs rather than SQLite rowids as public identity
- use lowercase snake_case table and column names
- use CHECK constraints for bounded vocabularies where reasonable
- use ISO-8601-style timestamp text for stored times
- keep unknown, unavailable, and unattached states distinct
- preserve unattached notes without inventing parser identity
- keep human annotations distinct from parser facts
- keep display-only correction proposals distinct from applied facts
- avoid foreign-key dependencies on analytics tables in v1, because the default
  Journal database is separate
- avoid introducing runtime behavior or external sync behavior

The schema may use foreign keys among journal-owned tables.

## Unknowns

- Whether the future product should use a standalone Match Journal database,
  attach it to the analytics database at query time, or eventually co-locate
  some journal tables with analytics facts.
- Whether field override proposals should ship in the first implementation or
  wait for a dedicated correction-review contract.
- Whether `journal_sheet_sync_queue` should ship in the first implementation or
  wait for a dedicated export/sync contract.
- Which reference values should be repo-seeded versus user-created later.
- Whether future Match Journal UI will be overlay-based, CLI-based, local web
  UI-based, or another local surface.

## Suspected Gaps

- Existing analytics annotation tables are useful but too narrow to serve as a
  full Match Journal layer.
- There is no local schema for unattached notes.
- There is no journal-owned attachment status vocabulary.
- There is no safe field correction proposal boundary.
- There is no local reference/dropdown table for review labels.
- There is no generated-artifact ignore rule for Match Journal databases.

## Explicit Deferrals

Deferred to future contracts:

- overlay implementation
- local web UI implementation
- Google Sheets sync
- workbook export
- webhook delivery
- Apps Script behavior
- analytics ingest of journal labels
- analytics views that join journal labels
- Match Journal runtime status exposure
- status API routes
- OpenAI/model-provider integrations
- AI coaching
- automatic archetype classification
- external archetype-list refresh
- corpus/reference expansion from issue #158
- downstream ML/OpenAI research from issue #41
- parser behavior changes
- parser event changes
- parser state final reconciliation changes
- match/game identity changes
- deduplication changes

## Validation Obligations

Codex C or Codex D should run as applicable:

```bash
python3 -m pytest -q tests/test_match_journal_schema.py
python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py
python3 -m ruff check src tests tools
git diff --check
```

Additional validation expectations:

- Tests must use in-memory SQLite unless a specific local generated artifact is
  required and ignored.
- Tests must prove migrations apply idempotently.
- Tests must prove required tables exist.
- Tests must prove bounded vocabularies are enforced.
- Tests must prove generated database artifacts are ignored.
- Tests must prove `pyproject.toml` includes
  `mythic_edge_parser.app.match_journal_migrations = ["*.sql"]` under
  `tool.setuptools.package-data`.
- Tests must prove the Journal schema can be loaded without changing analytics
  schema behavior.
- Tests must prove unattached notes are representable without parser IDs.
- Tests must prove field override proposals, if implemented, carry
  `journal_display_only` effect scope.
- Tests must not depend on raw private Player.log excerpts, real workbook
  exports, real runtime status files, real failed posts, real secrets, real
  Google Sheets, or model-provider calls.

If an implementation or fixer thread changes schema, migration-loader, package
metadata, or tests, documentation-only checks are not sufficient; focused tests
are required.

## Acceptance Criteria

This contract is ready for Codex C when:

- `docs/contracts/match_journal_local_sqlite_schema.md` is present.
- The schema boundary is explicit: Journal stores human annotations, not parser
  truth.
- The initial table families are named.
- The default local database path is named and marked ignored/private.
- The migration package path and schema version are named.
- The SQL migration package-data requirement is named and scoped to a narrow
  `pyproject.toml` metadata change.
- The unattached-note behavior is explicitly required.
- The display-only field-override boundary is explicit.
- Protected surfaces and forbidden outputs are explicit.
- The next role has a narrow implementation or fixer path and validation
  commands.

The first implementation is acceptable only if:

- It does not implement parser behavior changes.
- It does not implement runtime behavior.
- It does not implement overlay behavior.
- It does not implement Google Sheets sync.
- It does not implement OpenAI/model-provider behavior.
- It does not commit generated/local/private artifacts.
- It keeps Match Journal human annotations separate from parser facts.

## Contract Clarification For MJSQL-001

Verdict: package-data behavior is required.

`docs/contract_test_reports/match_journal_local_sqlite_schema.md` found that
the implementation reads Match Journal SQL migrations with `importlib.resources`
from `mythic_edge_parser.app.match_journal_migrations`, but the contract did not
authorize `pyproject.toml` package-data configuration. That ambiguity is now
resolved.

Required follow-up:

- Add `mythic_edge_parser.app.match_journal_migrations = ["*.sql"]` to
  `pyproject.toml` package data.
- Add focused coverage proving that package-data declaration exists.
- Keep the fix limited to package metadata/test coverage and any necessary
  handoff/report updates.

Not authorized:

- source-tree-only migration loading as the accepted v1 behavior
- dependency or build-system changes
- runtime wiring
- parser behavior changes
- overlay, Google Sheets, workbook, webhook, Apps Script, analytics ingest,
  status API, or OpenAI/model-provider behavior changes

## Codex D Handoff Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex D: Module Fixer for issue #196, Match Journal local SQLite schema.

  Context:
  - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/196
  - Completed tracker: https://github.com/Tahjali11/Mythic-Edge/issues/190
  - Branch: codex/match-journal-foundation
  - Base: main
  - Contract: docs/contracts/match_journal_local_sqlite_schema.md
  - Contract test report: docs/contract_test_reports/match_journal_local_sqlite_schema.md
  - Previous integration commit: aebd4f8e121362d5b595f460068f626985c1ade0
  - Expected handoff artifact: docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md

  Goal:
  Fix MJSQL-001 only. The contract now requires Match Journal SQL migrations to be included as package data so the public importlib.resources-based migration loader is not source-tree-only.

  Read first:
  - AGENTS.md
  - docs/agent_rules.yml
  - docs/agent_constitution.md
  - docs/codex_module_workflow.md
  - docs/agent_threads/module_fixer.md
  - docs/contracts/match_journal_local_sqlite_schema.md
  - docs/contract_test_reports/match_journal_local_sqlite_schema.md
  - tests/test_analytics_migration_loader.py
  - tests/test_match_journal_schema.py
  - pyproject.toml
  - src/mythic_edge_parser/app/match_journal_migration_loader.py
  - src/mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql
  - .gitignore

  Implement:
  - Add the narrow pyproject package-data entry for mythic_edge_parser.app.match_journal_migrations = ["*.sql"].
  - Add focused test coverage proving that package-data declaration exists.
  - Update the implementation handoff and/or contract-test report only as needed to record the fix and validation.

  Stay within scope:
  - Fix only MJSQL-001.
  - Preserve the existing Match Journal schema and migration-loader behavior unless a direct package-data test requires a tiny import/test adjustment.
  - Keep Match Journal SQL migrations package-loadable through importlib.resources.

  Do not:
  - Target main directly.
  - Rework the Match Journal schema, loader, table design, generated database path, ignore policy, or public API beyond the package-data fix.
  - Implement overlay behavior, Google Sheets sync, workbook export, webhook delivery, Apps Script behavior, OpenAI/model-provider behavior, analytics ingest changes, runtime status changes, status API routes, parser behavior changes, parser state final reconciliation changes, parser event changes, match/game identity changes, or deduplication changes.
  - Create or commit SQLite/generated/private/runtime artifacts.
  - Store raw Player.log payloads, raw submitted-deck payloads, local private notes from real play sessions, failed posts, workbook exports, generated data, secrets, credentials, tokens, API keys, or webhook URLs.
  - Let Match Journal notes or human annotations become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching.

  Validation:
  - python3 -m pytest -q tests/test_match_journal_schema.py
  - python3 -m pytest -q tests/test_analytics_migration_loader.py
  - python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py
  - python3 -m ruff check src tests tools
  - git diff --check
  - Verify no generated SQLite/local/private artifacts are staged or committed.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/196"
  completed_thread: "B"
  next_thread: "D"
  source_artifact: "docs/contracts/match_journal_local_sqlite_schema.md"
  target_artifact: "docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md"
  verdict: "contract_clarified_package_data_required_route_to_fixer"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/match-journal-foundation"
  validation:
    - "documentation-only contract clarification"
    - "Codex D should run python3 -m pytest -q tests/test_match_journal_schema.py"
    - "Codex D should run python3 -m pytest -q tests/test_analytics_migration_loader.py"
    - "Codex D should run python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py"
    - "Codex D should run python3 -m ruff check src tests tools"
    - "Codex D should run git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Fix only MJSQL-001 unless a new finding is explicitly routed."
    - "Do not implement overlay behavior, Google Sheets sync, workbook export, webhook delivery, Apps Script behavior, OpenAI/model-provider behavior, analytics ingest changes, runtime status changes, status API routes, parser behavior changes, parser state final reconciliation changes, parser event changes, match/game identity changes, or deduplication changes."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
    - "Do not let Match Journal notes or human annotations become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching."
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/196"
  completed_thread: "B"
  next_thread: "D"
  source_artifact: "docs/contracts/match_journal_local_sqlite_schema.md"
  target_artifact: "docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md"
  verdict: "contract_clarified_package_data_required_route_to_fixer"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/match-journal-foundation"
  validation:
    - "documentation-only contract clarification"
    - "Codex D should run python3 -m pytest -q tests/test_match_journal_schema.py"
    - "Codex D should run python3 -m pytest -q tests/test_analytics_migration_loader.py"
    - "Codex D should run python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py"
    - "Codex D should run python3 -m ruff check src tests tools"
    - "Codex D should run git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Fix only MJSQL-001 unless a new finding is explicitly routed."
    - "Do not implement overlay behavior, Google Sheets sync, workbook export, webhook delivery, Apps Script behavior, OpenAI/model-provider behavior, analytics ingest changes, runtime status changes, status API routes, parser behavior changes, parser state final reconciliation changes, parser event changes, match/game identity changes, or deduplication changes."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
    - "Do not let Match Journal notes or human annotations become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching."
```
