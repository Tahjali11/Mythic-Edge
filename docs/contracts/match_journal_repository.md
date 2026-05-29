# Match Journal Repository Contract

## Module

Match Journal local repository/write-read boundary v1.

This contract defines the Python-facing repository layer over the existing
Match Journal local SQLite schema. The repository owns deterministic local
create, read, update, and list behavior for human-entered journal records. It
does not implement overlay UI, local HTTP/status API routes, Google Sheets
sync, analytics joins, OpenAI/model-provider behavior, parser behavior,
workbook behavior, webhook behavior, Apps Script behavior, or production
deployment behavior.

Plain English: future product surfaces should talk to the Match Journal through
one small local repository API instead of writing direct SQL. That API stores
human notes and labels; it does not correct or replace parser facts.

## Source Issue

Issue:

- https://github.com/Tahjali11/Mythic-Edge/issues/198

Previous issue:

- https://github.com/Tahjali11/Mythic-Edge/issues/196

Previous PR:

- https://github.com/Tahjali11/Mythic-Edge/pull/197

Previous merge commit:

```text
f07f4a7849c8522a3efd7d19c073d6742596973f
```

Tracker:

- N/A. No Match Journal tracker is currently open.

Branch:

```text
codex/match-journal-repository
```

Base:

```text
main
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
- `docs/contracts/match_journal_local_sqlite_schema.md`
- `docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md`
- `docs/contract_test_reports/match_journal_local_sqlite_schema.md`
- `docs/contracts/analytics_local_sqlite_schema.md`

## Risk Tier

Medium-High.

Reasons:

- The repository becomes the local write/read boundary for human annotations.
- Future overlay, Google Sheets, analytics, and AI-facing modules may depend on
  this API.
- A weak repository boundary could silently bypass attachment rules, drop
  unattached notes, or make human review data look like parser truth.
- The module is local-only, but it touches private human-authored notes and
  generated SQLite state.

## Owning Layer And Truth Boundary

Primary owning layer: Match Journal human annotation layer.

The repository owns:

- validating and writing local Match Journal records
- reading and listing local Match Journal records
- preserving unattached human notes
- preserving journal-owned stable IDs
- attaching journal records to existing parser IDs without inventing parser IDs
- keeping note and label history through current/validity fields
- exposing deterministic seams for IDs and timestamps
- keeping display-only field override proposals display-only

The repository does not own:

- parser event interpretation
- parser state final reconciliation
- parser match identity
- parser game identity
- parser deduplication
- parser-owned row shape
- workbook schema
- webhook payload shape
- Apps Script behavior
- output transport
- runtime status schema
- overlay behavior
- Google Sheets sync behavior
- analytics ingest or analytics SQL views
- OpenAI/model-provider behavior
- AI coaching or gameplay advice
- hidden-card inference
- archetype classification as inferred fact
- merge readiness or deploy readiness

Truth boundaries:

- Parser/state owns parser facts and parser identity.
- Match Journal owns human-authored context, labels, review flags, and
  display-only correction proposals.
- Analytics SQLite owns deterministic downstream storage of parser-normalized
  facts and analytics views.
- Evidence ledger owns provenance vocabulary for parser facts.
- Overlay, Google Sheets, workbook/dashboard, Apps Script, webhook transport,
  OpenAI/model-provider output, and AI coaching are downstream consumers only
  unless a later contract changes their role.

## Observed Current Behavior

Current `main` after PR #197:

- `src/mythic_edge_parser/app/match_journal_migration_loader.py` exposes a
  public resource-based migration loader.
- `src/mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql`
  creates the local Match Journal schema.
- `pyproject.toml` includes SQL package data for
  `mythic_edge_parser.app.match_journal_migrations = ["*.sql"]`.
- `.gitignore` ignores `data/match_journal/`.
- `tests/test_match_journal_schema.py` covers schema shape, package data,
  migration idempotency, unattached notes, parser ID references,
  display-only field overrides, bounded vocabularies, and analytics-schema
  coexistence.
- There is no `match_journal_repository.py`.
- No public repository API exists for creating, reading, updating, or listing
  journal rows.
- Future callers would need to write direct SQL unless this repository layer is
  implemented.

Current schema table families:

- `journal_matches`
- `journal_games`
- `journal_notes`
- `journal_labels`
- `journal_review_flags`
- `journal_reference_values`
- `journal_field_overrides`

Deferred by prior schema contract:

- `journal_sheet_sync_queue`

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/match_journal_repository.md`

Future implementation files authorized by this contract:

- `src/mythic_edge_parser/app/match_journal_repository.py`
- `tests/test_match_journal_repository.py`
- `docs/implementation_handoffs/match_journal_repository_comparison.md`

Existing files that Codex C may read but should not change unless a direct,
minimal test import requires it:

- `src/mythic_edge_parser/app/match_journal_migration_loader.py`
- `src/mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql`
- `tests/test_match_journal_schema.py`
- `pyproject.toml`
- `.gitignore`

Files and surfaces not owned by this contract:

- parser modules
- parser state
- parser event classes
- `src/mythic_edge_parser/app/analytics_ingest.py`
- analytics migrations and analytics views
- runtime status modules
- status API modules
- overlay UI
- Google Sheets sync
- workbook schema
- webhook transport
- Apps Script
- OpenAI/model-provider code
- generated SQLite databases
- raw logs
- runtime artifacts
- failed posts
- workbook exports
- secrets, credentials, API keys, tokens, or webhook URLs

If implementation requires changes outside the owned files, Codex C must stop
and route back to Codex B unless the change is strictly documentation/handoff
wording for this issue.

## Public Interface

Future implementation must add:

```text
mythic_edge_parser.app.match_journal_repository
```

Required public constant:

```python
MATCH_JOURNAL_REPOSITORY_VERSION = "match_journal_repository.v1"
```

Required error classes:

```python
class MatchJournalRepositoryError(ValueError): ...
class MatchJournalValidationError(MatchJournalRepositoryError): ...
class MatchJournalNotFoundError(MatchJournalRepositoryError): ...
class MatchJournalConflictError(MatchJournalRepositoryError): ...
```

Required helper:

```python
ensure_match_journal_schema(
    connection: sqlite3.Connection,
    *,
    applied_at: str | None = None,
) -> None
```

`ensure_match_journal_schema` may delegate to
`apply_match_journal_migrations`. It must be explicit; repository construction
and normal write/read operations must not silently open a default database file
or perform hidden runtime setup.

Required repository class:

```python
class MatchJournalRepository:
    def __init__(
        self,
        connection: sqlite3.Connection,
        *,
        id_factory: Callable[[str], str] | None = None,
        clock: Callable[[], str] | None = None,
    ) -> None: ...
```

Rules:

- The repository accepts an existing `sqlite3.Connection`.
- The repository must not open `data/match_journal/mythic_edge_journal.sqlite3`
  by default.
- The repository must not read environment variables.
- The repository must not create files.
- The repository may expose dataclasses, typed dictionaries, or documented
  dictionaries for records. The public semantic fields below are required even
  if the Python representation varies.
- The `id_factory` and `clock` seams must make tests deterministic. Callers
  may also provide explicit IDs and timestamps in operation requests.

### Required Operations

The exact method names may vary only if the implementation handoff explains the
mapping. The required behavior is fixed.

Match operations:

```python
create_match(request: Mapping[str, object]) -> Mapping[str, object]
get_match(journal_match_id: str) -> Mapping[str, object] | None
list_matches(filters: Mapping[str, object] | None = None) -> tuple[Mapping[str, object], ...]
update_match(journal_match_id: str, updates: Mapping[str, object]) -> Mapping[str, object]
update_match_attachment(journal_match_id: str, request: Mapping[str, object]) -> Mapping[str, object]
```

Game operations:

```python
create_game(request: Mapping[str, object]) -> Mapping[str, object]
get_game(journal_game_id: str) -> Mapping[str, object] | None
list_games(filters: Mapping[str, object] | None = None) -> tuple[Mapping[str, object], ...]
update_game(journal_game_id: str, updates: Mapping[str, object]) -> Mapping[str, object]
update_game_attachment(journal_game_id: str, request: Mapping[str, object]) -> Mapping[str, object]
```

Note operations:

```python
create_note(request: Mapping[str, object]) -> Mapping[str, object]
get_note(journal_note_id: str) -> Mapping[str, object] | None
list_notes(filters: Mapping[str, object] | None = None) -> tuple[Mapping[str, object], ...]
supersede_note(journal_note_id: str, request: Mapping[str, object]) -> Mapping[str, object]
```

Label operations:

```python
set_current_label(request: Mapping[str, object]) -> Mapping[str, object]
get_label(journal_label_id: str) -> Mapping[str, object] | None
list_labels(filters: Mapping[str, object] | None = None) -> tuple[Mapping[str, object], ...]
```

Review-flag operations:

```python
create_review_flag(request: Mapping[str, object]) -> Mapping[str, object]
get_review_flag(journal_review_flag_id: str) -> Mapping[str, object] | None
list_review_flags(filters: Mapping[str, object] | None = None) -> tuple[Mapping[str, object], ...]
update_review_flag(journal_review_flag_id: str, updates: Mapping[str, object]) -> Mapping[str, object]
```

Reference-value operations:

```python
upsert_reference_value(request: Mapping[str, object]) -> Mapping[str, object]
get_reference_value(reference_id: str) -> Mapping[str, object] | None
list_reference_values(filters: Mapping[str, object] | None = None) -> tuple[Mapping[str, object], ...]
set_reference_value_active(reference_id: str, is_active: bool) -> Mapping[str, object]
```

Field-override proposal operations:

```python
propose_field_override(request: Mapping[str, object]) -> Mapping[str, object]
get_field_override(journal_field_override_id: str) -> Mapping[str, object] | None
list_field_overrides(filters: Mapping[str, object] | None = None) -> tuple[Mapping[str, object], ...]
update_field_override_status(
    journal_field_override_id: str,
    request: Mapping[str, object],
) -> Mapping[str, object]
```

Forbidden public interfaces in this slice:

- CLI
- daemon
- default database opener
- environment-variable contract
- runtime status writer
- status API route
- overlay route
- Google Sheets sync/export
- workbook export
- webhook post
- Apps Script call
- analytics ingest or analytics view join
- OpenAI/model-provider call
- parser callback

## Inputs

All write requests are mappings with synthetic/testable values and safe labels.
The implementation may normalize them into dataclasses internally.

### Common Request Fields

Common optional fields:

- `author_label: str`
- `source_surface: str`
- `privacy_label: str`
- `created_at: str`
- `updated_at: str`

Defaults:

- `source_surface = "manual"`
- `privacy_label = "local_private"`
- timestamps come from the repository `clock` when not provided
- IDs come from explicit request values or the repository `id_factory`

Allowed `source_surface` values:

- `manual`
- `imported_review`
- `local_tool`
- `test_fixture`

Allowed `privacy_label` values:

- `local_private`
- `sanitized_fixture`
- `shareable_summary`

Rules:

- Required text fields must be non-empty after trimming unless the schema marks
  them nullable.
- `note_text` must be preserved as human-authored text; it must not be parsed
  into parser facts.
- Error messages must not echo full private note text, raw payloads, secrets,
  local filesystem paths, or URLs.

### Attachment Fields

Attachment-related fields:

- `journal_match_id: str | None`
- `journal_game_id: str | None`
- `parser_match_id: str | None`
- `parser_game_id: str | None`
- `game_number: int | None`
- `attachment_status: str`

Allowed `attachment_status` values:

- `attached`
- `unattached`
- `pending`
- `ambiguous`
- `detached`

Rules:

- `attached` match records require a non-empty `parser_match_id`.
- `attached` game records require a non-empty `parser_game_id`.
- The repository must not generate parser IDs.
- The repository must not look up parser state or runtime status to infer
  parser IDs.
- Unattached records must be accepted and queryable.
- `detached` records must not be deleted or converted into parser mutations.

### Match Requests

Accepted match fields:

- `journal_match_id`
- `parser_match_id`
- `attachment_status`
- `title`
- `experiment_id`
- `review_status`
- common request fields

Allowed `review_status` values:

- `not_reviewed`
- `needs_review`
- `reviewing`
- `reviewed`
- `archived`

### Game Requests

Accepted game fields:

- `journal_game_id`
- `journal_match_id`
- `parser_match_id`
- `parser_game_id`
- `game_number`
- `attachment_status`
- `review_status`
- common request fields

Rules:

- `journal_match_id` may be null to preserve game-level or unattached review
  work when match attachment is unknown.
- `game_number` may be null for unattached or ambiguous records.
- `game_number`, when present, must be a positive integer.

### Note Requests

Accepted note fields:

- `journal_note_id`
- `journal_match_id`
- `journal_game_id`
- `parser_match_id`
- `parser_game_id`
- `note_scope`
- `note_text`
- `note_format`
- `is_current`
- `supersedes_note_id`
- `valid_from`
- `valid_to`
- common request fields

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

Rules:

- Unattached notes must be supported with no `journal_match_id`,
  `journal_game_id`, `parser_match_id`, or `parser_game_id`.
- Updating note content must use `supersede_note` rather than destructive text
  overwrite.
- `supersede_note` must set the previous note `is_current = 0` and `valid_to`
  while creating a new current note that references `supersedes_note_id`.

### Label Requests

Accepted label fields:

- `journal_label_id`
- `journal_match_id`
- `journal_game_id`
- `parser_match_id`
- `parser_game_id`
- `label_scope`
- `label_type`
- `label_value`
- `reference_id`
- `is_current`
- `valid_from`
- `valid_to`
- common request fields

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

- `set_current_label` must expire prior current labels with the same
  journal/parser attachment identity, `label_scope`, and `label_type`.
- Pilot-error yes/no and pilot-error reason must remain separately queryable.
  The repository must not collapse them into one text blob.
- Opponent archetype and tier labels are human annotations, not automatic
  classifier output.

### Review Flag Requests

Accepted review flag fields:

- `journal_review_flag_id`
- `journal_match_id`
- `journal_game_id`
- `parser_match_id`
- `parser_game_id`
- `flag_type`
- `flag_status`
- `priority_label`
- `reason`
- common request fields

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

- `suspected_parser_gap` is review metadata only.
- Review flags must not become parser correctness truth, CI truth, merge
  readiness, or deploy readiness.

### Reference Value Requests

Accepted reference value fields:

- `reference_id`
- `reference_type`
- `label`
- `description`
- `sort_order`
- `is_active`
- `created_at`
- `updated_at`

Allowed `reference_type` values:

- `review_status`
- `pilot_error_reason`
- `opponent_archetype_tier`
- `sideboarding_label`
- `experiment_id`
- `custom_label`

Rules:

- Reference values are local dropdown/list helpers.
- `list_reference_values({"is_active": true})` must return only active values.
- No external website refresh, archetype-list scraping, or OpenAI-generated
  reference data is authorized.

### Field Override Proposal Requests

Accepted field override fields:

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
- common request fields

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

Required `effect_scope` value:

```text
journal_display_only
```

Rules:

- Field override proposals must never update parser facts, analytics facts,
  workbook rows, webhook payloads, Apps Script, runtime status, overlay output,
  or Google Sheets.
- `accepted_for_journal_display` means accepted only for future Journal display
  surfaces, not accepted as parser truth.

## Outputs

Repository read operations return records from Match Journal tables as plain
safe local data.

Required output rules:

- Return keys must match schema column names unless the implementation clearly
  documents an equivalent dataclass field mapping.
- Boolean SQLite fields such as `is_current` and `is_active` may be returned as
  integers or booleans, but tests must document the chosen behavior.
- List operations must return deterministic ordering.
- Default order for notes and labels should be `created_at`, then stable ID.
- Default order for reference values should be `sort_order`, then `label`, then
  `reference_id`.
- Write operations return the row after write.
- Missing `get_*` operations return `None`.
- Missing `update_*` targets raise `MatchJournalNotFoundError`.

Forbidden outputs:

- generated SQLite files committed to the repo
- raw Player.log payloads
- runtime status files
- failed posts
- workbook exports
- Google Sheets writes
- webhook calls
- Apps Script writes
- overlay output
- OpenAI/model-provider output
- parser row mutations
- analytics fact mutations

## Invariants

- The repository must not mutate parser-owned facts.
- The repository must not mutate analytics fact tables or analytics views.
- The repository must not create parser match IDs or parser game IDs.
- The repository must preserve unattached notes.
- The repository must preserve journal-owned IDs.
- The repository must keep note content changes history-preserving through
  supersession.
- The repository must keep current labels history-preserving through
  `is_current`, `valid_from`, and `valid_to`.
- Pilot-error yes/no and pilot-error reason must be independently queryable.
- Reference value active/inactive state must be queryable.
- Field overrides must always carry `effect_scope = "journal_display_only"`.
- `journal_sheet_sync_queue` remains deferred and must not be written in this
  slice.
- Repository operations must be deterministic under injected ID and clock
  providers.
- The repository must use parameterized SQL.
- The repository must not store raw Player.log payloads.

## Error Behavior

Repository errors must be safe, typed, and local.

Required behavior:

- Unknown enum values raise `MatchJournalValidationError`.
- Missing required fields raise `MatchJournalValidationError`.
- Empty required text fields raise `MatchJournalValidationError`.
- Attached match requests without `parser_match_id` raise
  `MatchJournalValidationError`.
- Attached game requests without `parser_game_id` raise
  `MatchJournalValidationError`.
- Missing rows for update/supersede/status changes raise
  `MatchJournalNotFoundError`.
- Attempts to set a field override `effect_scope` other than
  `journal_display_only` raise `MatchJournalValidationError`.
- SQLite integrity errors should be wrapped as `MatchJournalRepositoryError` or
  a narrower repository error with sanitized messages.
- Repository write operations must avoid partial writes on validation failure.
- Error messages must not include raw private note text, raw payloads, local
  absolute paths, secrets, credentials, tokens, API keys, or webhook URLs.

Transaction policy:

- `ensure_match_journal_schema` may use the migration loader's transaction
  behavior.
- Normal repository write operations should be atomic per operation.
- The implementation may either reject caller-open transactions or support
  caller-managed transactions, but it must document the choice and test it.
- The implementation must not silently commit or roll back a caller-owned open
  transaction without a documented and tested policy.

## Side Effects

Allowed side effects:

- writes to existing journal-owned SQLite tables on a caller-supplied
  connection
- explicit schema migration through `ensure_match_journal_schema`
- in-memory SQLite state in tests
- documentation handoff artifact for implementation

Forbidden side effects:

- opening the default database path by default
- creating generated SQLite database files during tests
- writing runtime status files
- writing failed posts
- writing workbook exports
- changing parser state
- changing analytics facts or views
- posting webhooks
- calling Apps Script
- writing Google Sheets
- changing overlay state
- calling OpenAI/model providers
- creating GitHub issues, PRs, comments, or tracker updates from repository code

## Dependency Order

Codex C should implement in this order:

1. Add `src/mythic_edge_parser/app/match_journal_repository.py` with errors,
   constants, `ensure_match_journal_schema`, and repository construction.
2. Add focused in-memory tests for schema ensure, deterministic ID/clock seams,
   and validation errors.
3. Add match and game create/read/list/update/attachment behavior.
4. Add note create/list/supersession behavior, especially unattached notes.
5. Add label current-setting behavior, including separate pilot-error and
   reason labels.
6. Add review-flag, reference-value, and field-override proposal behavior.
7. Add the implementation handoff.
8. Run focused validation and protected-surface checks.

## Compatibility

The repository must remain compatible with:

- `match_journal_local_sqlite_schema.v1`
- `MATCH_JOURNAL_SCHEMA_VERSION`
- existing table names and column names from
  `0001_initial_match_journal_schema.sql`
- package-data loading for Match Journal SQL migrations
- in-memory SQLite tests
- analytics schema coexistence in the same in-memory SQLite connection

The repository must not require:

- a second schema migration
- a generated database file
- a default DB opener
- an environment variable
- parser runtime state
- analytics ingest
- overlay/status API/Google Sheets/AI callers

Deferred compatibility:

- `journal_sheet_sync_queue` remains deferred.
- Google Sheets export/sync compatibility is deferred.
- analytics joins that read journal data are deferred.
- overlay UI compatibility is deferred.
- OpenAI/model-provider explanation over Journal notes is deferred.

## Tests Required

Codex C must add focused tests in:

```text
tests/test_match_journal_repository.py
```

Required test behaviors:

- `ensure_match_journal_schema` applies migrations to an in-memory connection.
- Repository construction accepts an existing SQLite connection and does not
  open a default database file.
- Deterministic `id_factory` and `clock` are used when explicit IDs/timestamps
  are not provided.
- Match create/get/list/update preserves journal IDs and parser references.
- Match attachment requires parser match ID for attached status and never
  invents one.
- Game create/get/list/update preserves journal IDs and parser references.
- Game attachment requires parser game ID for attached status and never invents
  one.
- Unattached note creation works without journal or parser IDs.
- Note supersession marks the old note not current and creates a new current
  note with `supersedes_note_id`.
- `set_current_label` expires prior current labels of the same label identity.
- Pilot-error yes/no and pilot-error reason remain separately queryable.
- Active reference-value filtering works.
- Review flag status updates are local review metadata only.
- Field override proposals always use `journal_display_only`; invalid effect
  scopes fail.
- Invalid enum values fail with repository validation errors.
- Missing rows fail with repository not-found errors.
- Validation failures do not leave partial rows.
- `journal_sheet_sync_queue` is not created or written by repository tests.
- No generated SQLite/local/private artifacts are created or committed.

Validation commands:

```bash
python3 -m pytest -q tests/test_match_journal_schema.py
python3 -m pytest -q tests/test_match_journal_repository.py
python3 -m pytest -q tests/test_analytics_schema.py
python3 -m ruff check src tests tools
git diff --check
```

Protected checks for Codex C/E/F:

```bash
printf '%s\n' \
  docs/contracts/match_journal_repository.md \
  src/mythic_edge_parser/app/match_journal_repository.py \
  tests/test_match_journal_repository.py \
  docs/implementation_handoffs/match_journal_repository_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin

printf '%s\n' \
  docs/contracts/match_journal_repository.md \
  src/mythic_edge_parser/app/match_journal_repository.py \
  tests/test_match_journal_repository.py \
  docs/implementation_handoffs/match_journal_repository_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

## Acceptance Criteria

The contract is implementation-ready when:

- The owning layer is named as Match Journal human annotation layer.
- The repository module and public API are named.
- The repository is explicitly caller-connection based.
- Default DB opening, environment variables, runtime wiring, overlay behavior,
  Google Sheets sync, analytics joins, parser behavior, and AI behavior are
  out of scope.
- Attachment behavior is explicit.
- Unattached-note behavior is explicit.
- Note and label history behavior is explicit.
- Pilot-error yes/no and reason remain separately queryable.
- Display-only field override behavior is explicit.
- Tests and protected-surface checks are named.
- The next role is Codex C.

Implementation is acceptable only if:

- It changes only repository implementation, focused tests, and handoff docs.
- It uses the existing schema without schema migration changes.
- It does not create or commit generated/local/private artifacts.
- It does not change parser/runtime/workbook/webhook/App Script/overlay/
  Google Sheets/analytics/OpenAI behavior.
- It does not make Match Journal records parser truth, analytics truth, merge
  readiness, deploy readiness, gameplay advice, hidden-card inference,
  archetype classification, player-mistake labels, or AI coaching.

## Open Questions And Contract Risks

- The transaction policy is deliberately left as a documented implementation
  choice because the repository may need either simple per-operation atomicity
  or future batch writes. Codex C must choose and test one policy.
- The exact Python record representation is left flexible. Codex C may use
  dataclasses, typed dictionaries, or documented dictionaries as long as schema
  field semantics are preserved.
- No filesystem database test is required in this slice. If Codex C finds that
  temporary filesystem DB coverage is necessary, it must keep artifacts in
  temporary directories and out of the repo.
- `journal_sheet_sync_queue` remains deferred even though sync/export readiness
  is a plausible future need.

## Codex C Handoff Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #198, Match Journal local repository/write-read boundary.

  Context:
  - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/198
  - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/196
  - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/197
  - Previous merge commit: f07f4a7849c8522a3efd7d19c073d6742596973f
  - Branch: codex/match-journal-repository
  - Base: main
  - Contract: docs/contracts/match_journal_repository.md
  - Expected handoff artifact: docs/implementation_handoffs/match_journal_repository_comparison.md

  Goal:
  Compare current main against the Match Journal repository contract. Implement only the smallest local repository/write-read API and focused tests needed to satisfy the contract.

  Read first:
  - AGENTS.md
  - docs/agent_rules.yml
  - docs/agent_constitution.md
  - docs/codex_module_workflow.md
  - docs/agent_threads/implementation.md
  - docs/contracts/match_journal_repository.md
  - docs/contracts/match_journal_local_sqlite_schema.md
  - docs/implementation_handoffs/match_journal_local_sqlite_schema_comparison.md
  - docs/contract_test_reports/match_journal_local_sqlite_schema.md
  - src/mythic_edge_parser/app/match_journal_migration_loader.py
  - src/mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql
  - tests/test_match_journal_schema.py
  - docs/contracts/analytics_local_sqlite_schema.md
  - src/mythic_edge_parser/app/analytics_ingest.py
  - tests/test_analytics_schema.py

  Implement:
  - src/mythic_edge_parser/app/match_journal_repository.py
  - tests/test_match_journal_repository.py
  - docs/implementation_handoffs/match_journal_repository_comparison.md

  Required behavior:
  - Repository accepts an existing sqlite3.Connection.
  - Repository exposes explicit schema ensure behavior without opening a default DB.
  - Repository supports create/read/update/list operations for journal matches, games, notes, labels, review flags, reference values, and display-only field override proposals.
  - Repository preserves unattached notes without parser IDs.
  - Repository treats parser match/game IDs as references only and never invents them.
  - Repository keeps note supersession and current-label history.
  - Repository keeps pilot-error yes/no and pilot-error reason separately queryable.
  - Repository keeps field overrides journal_display_only.
  - Tests use in-memory SQLite and deterministic ID/timestamp seams.

  Do not:
  - Open a PR or commit unless explicitly asked.
  - Target main directly.
  - Change the Match Journal SQL schema unless a blocking mismatch routes back to Codex B.
  - Create or commit SQLite database files, WAL, SHM, journal files, raw logs, generated data, runtime artifacts, failed posts, workbook exports, secrets, credentials, API keys, tokens, or webhook URLs.
  - Store raw Player.log payloads in SQLite.
  - Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, analytics ingest, analytics views, production behavior, Google Sheets sync behavior, overlay behavior, OpenAI/model-provider behavior, or AI/coaching behavior.
  - Let Match Journal notes, labels, review flags, or field override proposals become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching.

  Validation:
  - python3 -m pytest -q tests/test_match_journal_schema.py
  - python3 -m pytest -q tests/test_match_journal_repository.py
  - python3 -m pytest -q tests/test_analytics_schema.py
  - python3 -m ruff check src tests tools
  - git diff --check
  - Run path-scoped secret/private marker and protected-surface checks for changed files.
  - Verify no generated SQLite/local/private artifacts are staged or committed.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/198"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/196"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/197"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/match_journal_repository.md"
  target_artifact: "docs/implementation_handoffs/match_journal_repository_comparison.md"
  verdict: "contract_ready_for_module_implementer"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/match-journal-repository"
  validation:
    - "documentation-only contract writer pass"
    - "Codex C should run python3 -m pytest -q tests/test_match_journal_schema.py"
    - "Codex C should run python3 -m pytest -q tests/test_match_journal_repository.py"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_schema.py"
    - "Codex C should run python3 -m ruff check src tests tools"
    - "Codex C should run git diff --check"
    - "Codex C should run path-scoped secret/private marker and protected-surface checks"
  stop_conditions:
    - "Do not target main directly."
    - "Do not change the Match Journal SQL schema unless a blocking mismatch routes back to Codex B."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
    - "Do not implement overlay, local HTTP/status API, Google Sheets sync, analytics joins, OpenAI/model-provider behavior, AI coaching, external website refresh, parser behavior, workbook/webhook/App Script behavior, or production behavior."
    - "Do not let Match Journal records become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching."
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/198"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/196"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/197"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/match_journal_repository.md"
  target_artifact: "docs/implementation_handoffs/match_journal_repository_comparison.md"
  verdict: "contract_ready_for_module_implementer"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/match-journal-repository"
  validation:
    - "documentation-only contract writer pass"
    - "Codex C should run python3 -m pytest -q tests/test_match_journal_schema.py"
    - "Codex C should run python3 -m pytest -q tests/test_match_journal_repository.py"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_schema.py"
    - "Codex C should run python3 -m ruff check src tests tools"
    - "Codex C should run git diff --check"
    - "Codex C should run path-scoped secret/private marker and protected-surface checks"
  stop_conditions:
    - "Do not target main directly."
    - "Do not change the Match Journal SQL schema unless a blocking mismatch routes back to Codex B."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
    - "Do not implement overlay, local HTTP/status API, Google Sheets sync, analytics joins, OpenAI/model-provider behavior, AI coaching, external website refresh, parser behavior, workbook/webhook/App Script behavior, or production behavior."
    - "Do not let Match Journal records become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching."
```
