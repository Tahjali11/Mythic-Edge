# Match Journal Service Contract

## Module

Match Journal local service/use-case boundary v1.

This contract defines a narrow human-intent service layer over the existing
Match Journal repository. The service packages common local journal actions so
future overlay, command, review, sync, analytics, or AI-facing surfaces do not
compose low-level repository dictionaries or write direct SQL.

The service is not an overlay, local HTTP/status API, Google Sheets sync,
analytics join, OpenAI/model-provider integration, parser correction layer, or
production runtime layer.

Plain English: the repository knows how to write rows. The service knows how a
human says "add a match note", "mark pilot error", or "flag this for review",
while still keeping those human entries separate from parser truth.

## Source Issue

Issue:

- https://github.com/Tahjali11/Mythic-Edge/issues/200

Previous issue:

- https://github.com/Tahjali11/Mythic-Edge/issues/198

Previous PR:

- https://github.com/Tahjali11/Mythic-Edge/pull/199

Previous merge commit:

```text
1ac67bc61269f423131a19db0a92b935591fa5a5
```

Prior Match Journal foundation:

- https://github.com/Tahjali11/Mythic-Edge/issues/196
- https://github.com/Tahjali11/Mythic-Edge/pull/197

Tracker:

- N/A. No dedicated Match Journal tracker is currently open.

Branch:

```text
codex/match-journal-service
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
- `docs/contracts/match_journal_repository.md`
- `docs/implementation_handoffs/match_journal_repository_comparison.md`
- `docs/contract_test_reports/match_journal_repository.md`
- `docs/contracts/analytics_local_sqlite_schema.md`

## Risk Tier

Medium-High.

Reasons:

- The service becomes the local use-case boundary future UI, sync, analytics,
  and AI-facing modules are likely to call.
- It composes multiple repository writes for some human intents.
- It receives optional parser match/game references and must never invent or
  reinterpret parser identity.
- It touches private human-authored notes while remaining local-only.

## Owning Layer And Truth Boundary

Primary owning layer: Match Journal human-intent layer.

The Match Journal service owns:

- local service commands for common human journal actions
- mapping service commands to repository operations
- attachment-context normalization from caller-provided values only
- preserving unattached notes when no context is supplied
- keeping pilot-error status and pilot-error reason separately queryable
- creating manual opponent labels without classification
- creating review flags as review metadata
- creating display-only field override proposals
- returning local journal bundles for review surfaces without analytics joins

The Match Journal service does not own:

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
- player-mistake labels as facts
- merge readiness or deploy readiness

Truth boundaries:

- Parser/state owns parser facts and parser identity.
- Match Journal repository owns validated local SQLite row operations.
- Match Journal service owns local human-intent operations built from
  repository calls.
- Analytics SQLite may later read journal data only under a separate contract.
- Overlay, Google Sheets, workbook/dashboard, Apps Script, webhook transport,
  OpenAI/model-provider output, and AI coaching are downstream consumers only
  unless a later contract changes their role.

## Observed Current Behavior

Current `main` after PR #199:

- `docs/contracts/match_journal_local_sqlite_schema.md` defines the local
  SQLite schema boundary.
- `docs/contracts/match_journal_repository.md` defines the repository boundary.
- `src/mythic_edge_parser/app/match_journal_migration_loader.py` applies the
  packaged schema migration.
- `src/mythic_edge_parser/app/match_journal_repository.py` exposes a
  caller-owned `sqlite3.Connection` repository.
- Repository writes cover matches, games, notes, labels, review flags,
  reference values, and field override proposals.
- Repository reads return rows as dictionaries; public missing `get_*` methods
  return `None`.
- Repository tests cover unattached notes, current-label history,
  pilot-error label separation, active reference filtering, field override
  display-only constraints, validation failures, and transaction conflict
  behavior.
- No `match_journal_service.py` exists.
- No service-level command/result interface exists.
- No local journal bundle read helper exists.
- Future callers would need to compose repository dictionaries directly.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/match_journal_service.md`

Future implementation files authorized by this contract:

- `src/mythic_edge_parser/app/match_journal_service.py`
- `tests/test_match_journal_service.py`
- `docs/implementation_handoffs/match_journal_service_comparison.md`

Existing files that Codex C may read but should not change unless a direct,
minimal import or test adjustment is required:

- `src/mythic_edge_parser/app/match_journal_repository.py`
- `src/mythic_edge_parser/app/match_journal_migration_loader.py`
- `src/mythic_edge_parser/app/match_journal_migrations/0001_initial_match_journal_schema.sql`
- `tests/test_match_journal_repository.py`
- `tests/test_match_journal_schema.py`

Files and surfaces not owned by this contract:

- parser modules
- parser state
- parser event classes
- analytics ingest
- analytics migrations
- analytics views
- runtime status modules
- status API modules
- overlay UI
- Google Sheets sync
- `journal_sheet_sync_queue`
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

If implementation requires repository API changes, schema changes, analytics
changes, runtime changes, or downstream integration changes, Codex C must stop
and route back to Codex B.

## Public Interface

Future implementation must add:

```text
mythic_edge_parser.app.match_journal_service
```

Required public constant:

```python
MATCH_JOURNAL_SERVICE_VERSION = "match_journal_service.v1"
```

Required public error classes:

```python
class MatchJournalServiceError(ValueError): ...
class MatchJournalServiceValidationError(MatchJournalServiceError): ...
class MatchJournalServiceNotFoundError(MatchJournalServiceError): ...
class MatchJournalServiceConflictError(MatchJournalServiceError): ...
```

Service errors may wrap repository errors, but public service callers should not
need to import repository errors for normal service use.

Required service class:

```python
class MatchJournalService:
    def __init__(self, repository: MatchJournalRepository) -> None: ...

    @classmethod
    def from_connection(
        cls,
        connection: sqlite3.Connection,
        *,
        id_factory: Callable[[str], str] | None = None,
        clock: Callable[[], str] | None = None,
        ensure_schema: bool = False,
        applied_at: str | None = None,
    ) -> MatchJournalService: ...
```

Rules:

- Construction from an existing `MatchJournalRepository` is the primary path.
- `from_connection` is allowed as a convenience wrapper over the repository.
- `from_connection(..., ensure_schema=True)` may call
  `ensure_match_journal_schema` explicitly.
- Service construction must not open the default Match Journal database path.
- Service construction must not read environment variables.
- Service operations must not read parser runtime state, status API state, or
  local runtime artifacts.
- Service operations must not create files.

### Attachment Context Shape

All intent-level operations that can attach to a match or game accept an
optional attachment context mapping:

```python
AttachmentContext = Mapping[str, object]
```

Accepted fields:

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

- The context is caller-provided only.
- The service must not query parser state to discover active match/game IDs.
- The service must not call the status API to discover active match/game IDs.
- The service must not infer missing parser IDs from journal IDs.
- If a `journal_match_id` or `journal_game_id` is provided, the service must
  use the existing journal record or fail with a not-found service error.
- If only `parser_match_id` is provided, the service may find or create one
  journal match container referencing that parser ID.
- If only `parser_game_id` is provided, the service may find or create one
  journal game container referencing that parser ID. If `parser_match_id` is
  also present, it may create or use the corresponding journal match.
- If multiple journal records match one parser ID, the service must fail with a
  conflict error instead of choosing silently.
- If no context is supplied for note recording, the service must create an
  unattached note rather than dropping it.
- Parser IDs remain references only. The service never creates parser IDs.

### Result Shape

All successful service write operations return a documented result mapping or
dataclass with these semantic fields:

- `action`
- `status`
- `primary_record_type`
- `primary_record_id`
- `records`
- `warnings`

Required successful `status` value:

- `completed`

Rules:

- Successful operations return `status = "completed"`.
- Not-found, conflict, and validation failures should raise typed service
  errors by default. If implementation also supports non-completed result
  objects for a narrow caller need, the behavior and status vocabulary must be
  documented and tested without hiding errors as successful completion.
- `records` maps stable names to repository rows, such as `note`, `match`,
  `game`, `pilot_error_label`, `pilot_error_reason_label`, `review_flag`, or
  `field_override`.
- Result shapes must not include raw Player.log payloads, local paths, raw
  runtime artifacts, secrets, workbook exports, model-provider responses, or
  hidden-card guesses.

### Required Intent Operations

The implementation must expose at least the method names below. Additional
thin aliases are allowed only when the implementation handoff maps them
clearly and tests the contracted names.

Note operations:

```python
record_match_note(context: Mapping[str, object] | None, note_text: str, **options) -> Result
record_game_note(context: Mapping[str, object] | None, note_text: str, **options) -> Result
record_sideboarding_note(context: Mapping[str, object] | None, note_text: str, **options) -> Result
record_unattached_note(note_text: str, **options) -> Result
```

Label operations:

```python
set_experiment_label(context: Mapping[str, object] | None, experiment_id: str, **options) -> Result
set_pilot_error_status(context: Mapping[str, object] | None, status: str, **options) -> Result
set_pilot_error_reason(context: Mapping[str, object] | None, reason: str, **options) -> Result
set_opponent_labels(
    context: Mapping[str, object] | None,
    *,
    archetype: str | None = None,
    tier: str | None = None,
    **options,
) -> Result
```

Composite review operation:

```python
record_pilot_error_review(
    context: Mapping[str, object] | None,
    *,
    status: str,
    reason: str | None = None,
    note_text: str | None = None,
    **options,
) -> Result
```

Review flag operation:

```python
flag_for_review(context: Mapping[str, object] | None, flag_type: str, **options) -> Result
```

Display-only correction proposal operation:

```python
propose_display_correction(context: Mapping[str, object] | None, request: Mapping[str, object]) -> Result
```

Read operation:

```python
get_journal_bundle(context: Mapping[str, object]) -> Mapping[str, object] | None
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
- `journal_sheet_sync_queue` writer
- workbook export
- webhook post
- Apps Script call
- analytics ingest or analytics view join
- OpenAI/model-provider call
- parser callback

## Inputs

All service inputs are local, caller-provided command values.

Common option fields:

- `author_label`
- `source_surface`
- `privacy_label`
- `note_format`
- `priority_label`
- `reference_id`
- `created_at`
- `updated_at`
- `valid_from`

Defaults should follow repository defaults unless the service operation has a
clearer semantic default:

- `source_surface = "manual"`
- `privacy_label = "local_private"`
- `note_format = "plain_text"`
- `flag_status = "open"`

Allowed `source_surface` values:

- `manual`
- `imported_review`
- `local_tool`
- `test_fixture`

Allowed `privacy_label` values:

- `local_private`
- `sanitized_fixture`
- `shareable_summary`

Forbidden inputs:

- raw Player.log payloads
- raw local log paths
- raw runtime status JSON
- failed posts
- workbook exports
- generated card data
- secrets, credentials, tokens, API keys, or webhook URLs
- OpenAI/model-provider responses
- external website scraped archetype lists
- hidden-card guesses
- inferred opponent decklists
- parser runtime state as an implicit lookup source
- status API state as an implicit lookup source

### Note Input Rules

- `note_text` is required and must be non-empty after trimming.
- `record_match_note` creates a `note_scope = "match"` note.
- `record_game_note` creates a `note_scope = "game"` note.
- `record_sideboarding_note` creates a `note_scope = "sideboarding"` note.
- `record_unattached_note` creates a `note_scope = "unattached"` note with no
  parser or journal attachment unless explicit options say otherwise.
- Notes are human-authored text. The service must not parse notes into parser
  facts, analytics labels, or AI/coaching conclusions.

### Experiment Input Rules

- `experiment_id` is a human label.
- The service should store experiment metadata through repository-supported
  label behavior, and may update a journal match's `experiment_id` only when a
  journal match container is resolved.
- Experiment metadata must not become deck identity, parser truth, analytics
  truth, or AI truth.

### Pilot-Error Input Rules

Allowed pilot-error status values:

- `yes`
- `no`
- `unknown`
- `not_reviewed`

Rules:

- `set_pilot_error_status` writes a current label with
  `label_type = "pilot_error"`.
- `set_pilot_error_reason` writes a current label with
  `label_type = "pilot_error_reason"`.
- `record_pilot_error_review` may write status, reason, and note rows as one
  service use case, but the status and reason must remain independently
  queryable.
- Pilot-error records are review annotations. They are not parser facts,
  gameplay advice, player-mistake truth, merge readiness, deploy readiness, or
  AI coaching.

### Opponent Label Input Rules

Allowed service inputs:

- manually selected `archetype`
- manually selected `tier`

Rules:

- `archetype` writes `label_type = "opponent_archetype"`.
- `tier` writes `label_type = "opponent_archetype_tier"`.
- The service must not classify archetypes automatically.
- The service must not infer archetypes from cards, decklists, actions,
  external websites, model-provider output, or hidden information.

### Review Flag Input Rules

Allowed `flag_type` values match the repository:

- `needs_review`
- `interesting_match`
- `suspected_parser_gap`
- `sideboarding_review`
- `pilot_error_review`
- `custom`

Rules:

- Review flags are local review metadata only.
- `suspected_parser_gap` is not proof of parser error.
- Review flags must not become CI truth, merge readiness, deploy readiness, or
  parser correctness truth.

### Display Correction Input Rules

`propose_display_correction` accepts:

- `target_surface`
- `target_field`
- `original_value_label`
- `proposed_value_label`
- `override_reason`
- `override_status`

Required rule:

```text
effect_scope = journal_display_only
```

Allowed `target_surface` values:

- `match_log_row`
- `game_log_row`
- `action_log_row`
- `analytics_view`
- `journal_display`

Rules:

- The service may create a field override proposal through the repository.
- It must never apply the proposed value to parser facts, analytics facts,
  workbook rows, webhook payloads, Apps Script, runtime status, overlay output,
  or Google Sheets.

## Outputs

### Service Results

Write operations return service result objects as described above. Results are
local review outputs, not parser truth.

Required output properties:

- They must name the performed action.
- They must include primary record ID and type when a row is created or
  updated.
- They must expose all repository rows created by a composite action.
- They must keep note rows, label rows, review flag rows, and field override
  rows distinguishable.
- They must not hide partial-write errors as successful completion.
- They must not contain raw private artifacts or secrets.

### Journal Bundle

`get_journal_bundle` returns local journal context for one journal or parser
match reference.

Required bundle fields:

- `match`
- `games`
- `notes`
- `labels`
- `review_flags`
- `field_overrides`
- `warnings`

Rules:

- The bundle reads only Match Journal repository data.
- The bundle must not join analytics tables.
- The bundle must not query parser state or runtime status.
- The bundle must not include workbook, webhook, Apps Script, overlay, Google
  Sheets, or OpenAI/model-provider data.
- If no matching journal match exists, the service may return `None` or an
  empty bundle, but the behavior must be documented and tested.
- If a parser ID maps to multiple journal matches, the service must fail with a
  conflict error instead of choosing silently.

## Invariants

- The service must not mutate parser-owned facts.
- The service must not mutate analytics fact tables or analytics views.
- The service must not create parser match IDs or parser game IDs.
- The service must not read parser runtime state to infer attachment context.
- The service must preserve unattached notes.
- The service must preserve note, label, flag, and override row boundaries.
- Pilot-error status and reason must remain separately queryable.
- Manual opponent labels must remain human annotations.
- Field corrections must remain `journal_display_only`.
- Composite operations must not silently ignore failed subactions.
- Service results must not be parser truth, analytics truth, merge readiness,
  deploy readiness, gameplay advice, hidden-card inference, archetype
  classification, player-mistake truth, or AI coaching.
- Service tests must use in-memory SQLite unless a future contract explicitly
  authorizes filesystem DB tests.

## Error Behavior

Required service error behavior:

- Missing required values raise `MatchJournalServiceValidationError`.
- Invalid pilot-error status raises `MatchJournalServiceValidationError`.
- Empty note text raises `MatchJournalServiceValidationError`.
- Opponent label calls with neither `archetype` nor `tier` raise
  `MatchJournalServiceValidationError`.
- Display correction calls that try to set `effect_scope` away from
  `journal_display_only` raise `MatchJournalServiceValidationError`.
- Missing explicit journal match/game IDs raise `MatchJournalServiceNotFoundError`
  when an operation requires an existing journal record.
- Multiple journal records for one parser ID raise `MatchJournalServiceConflictError`.
- Repository validation, not-found, and conflict errors should be translated or
  re-raised as service-level errors with safe messages.
- Error messages must not include full private note text, raw payloads, local
  absolute paths, secrets, credentials, tokens, API keys, or webhook URLs.

Composite operation policy:

- Service code must validate all required command values before performing the
  first repository write.
- A service operation must not return `status = "completed"` unless all
  intended subactions completed.
- If Codex C determines that a required service operation cannot satisfy this
  policy with the current repository transaction model, it must stop and route
  back to Codex B rather than adding ad hoc direct SQL or silently accepting
  partial writes.

## Side Effects

Allowed side effects:

- repository writes to caller-owned local SQLite connections
- repository reads from caller-owned local SQLite connections
- explicit schema ensure only through `from_connection(..., ensure_schema=True)`
- in-memory SQLite state in tests
- implementation handoff documentation

Forbidden side effects:

- opening the default Match Journal database path
- creating generated SQLite files during tests
- writing runtime status files
- writing failed posts
- writing workbook exports
- mutating parser state
- mutating analytics facts or views
- posting webhooks
- calling Apps Script
- writing Google Sheets
- changing overlay state
- calling OpenAI/model providers
- creating GitHub issues, PRs, comments, or tracker updates from service code

## Dependency Order

Codex C should implement in this order:

1. Add `src/mythic_edge_parser/app/match_journal_service.py` with version,
   service errors, result helpers, and construction.
2. Add tests proving construction from repository and caller-owned connection
   without default DB opening.
3. Add attachment-context resolution tests and implementation.
4. Add note intent operations, including unattached notes.
5. Add experiment, pilot-error, and opponent-label operations.
6. Add review flag and display correction operations.
7. Add journal bundle read helper if it can be implemented from repository
   reads without analytics joins or runtime state.
8. Add composite-operation tests for pilot-error status, reason, and note.
9. Add implementation handoff.
10. Run focused validation and protected-surface checks.

## Compatibility

The service must remain compatible with:

- `match_journal_local_sqlite_schema.v1`
- `match_journal_repository.v1`
- caller-owned SQLite connections
- repository `id_factory` and `clock` seams
- repository row dictionaries
- in-memory SQLite tests

The service must not require:

- a new schema migration
- a generated database file
- a default DB opener
- an environment variable
- parser runtime state
- status API state
- analytics ingest
- overlay/status API/Google Sheets/AI callers

Deferred compatibility:

- `journal_sheet_sync_queue` remains deferred.
- Google Sheets export/sync compatibility is deferred.
- analytics joins that read journal data are deferred.
- overlay UI compatibility is deferred.
- local HTTP/status API compatibility is deferred.
- OpenAI/model-provider explanation over Journal notes is deferred.

## Tests Required

Codex C must add focused tests in:

```text
tests/test_match_journal_service.py
```

Required test behaviors:

- Service version and construction are public.
- Service can be constructed from an existing repository.
- Service can be constructed from a caller-owned connection with explicit
  schema ensure.
- Service construction does not open the default database path or read
  environment variables.
- `record_match_note` writes a match-scope note using provided journal or
  parser context.
- `record_game_note` writes a game-scope note using provided journal or parser
  context.
- `record_sideboarding_note` writes a sideboarding note.
- `record_unattached_note` preserves a note with no parser or journal context.
- Parser ID context is stored as references only and never invented.
- Multiple journal matches for one parser ID raise a service conflict error.
- `set_experiment_label` writes human experiment metadata.
- `set_pilot_error_status` and `set_pilot_error_reason` remain separately
  queryable.
- `record_pilot_error_review` creates distinguishable status/reason/note rows
  when supplied.
- `set_opponent_labels` writes manual opponent archetype/tier labels and does
  not classify automatically.
- `flag_for_review` creates local review metadata only.
- `propose_display_correction` creates a `journal_display_only` field override
  and rejects any other effect scope.
- `get_journal_bundle` returns only local journal repository data, or the
  tested empty/not-found behavior.
- Validation failures do not create partial rows.
- Composite operations do not report success when any subaction fails.
- No `journal_sheet_sync_queue` behavior is created or written.
- No generated SQLite/local/private artifacts are created or committed.

Validation commands:

```bash
python3 -m pytest -q tests/test_match_journal_schema.py
python3 -m pytest -q tests/test_match_journal_repository.py
python3 -m pytest -q tests/test_match_journal_service.py
python3 -m pytest -q tests/test_analytics_schema.py
python3 -m ruff check src tests tools
git diff --check
```

Protected checks for Codex C/E/F:

```bash
printf '%s\n' \
  docs/contracts/match_journal_service.md \
  src/mythic_edge_parser/app/match_journal_service.py \
  tests/test_match_journal_service.py \
  docs/implementation_handoffs/match_journal_service_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin

printf '%s\n' \
  docs/contracts/match_journal_service.md \
  src/mythic_edge_parser/app/match_journal_service.py \
  tests/test_match_journal_service.py \
  docs/implementation_handoffs/match_journal_service_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

## Acceptance Criteria

The contract is implementation-ready when:

- The owning layer is named as Match Journal human-intent layer.
- The service module and public service API are named.
- The service is explicitly repository/caller-connection based.
- Default DB opening, environment variables, runtime wiring, overlay behavior,
  Google Sheets sync, analytics joins, parser behavior, and AI behavior are
  out of scope.
- Attachment context behavior is explicit.
- Unattached-note behavior is explicit.
- Pilot-error status and reason remain separately queryable.
- Manual opponent labels remain human annotations only.
- Display-only field correction behavior is explicit.
- Bundle read boundaries are explicit.
- Tests and protected-surface checks are named.
- The next role is Codex C.

Implementation is acceptable only if:

- It changes only service implementation, focused tests, and handoff docs.
- It does not change Match Journal schema or repository public behavior unless
  a blocking mismatch routes back to Codex B.
- It does not create or commit generated/local/private artifacts.
- It does not change parser/runtime/workbook/webhook/App Script/overlay/
  Google Sheets/analytics/OpenAI behavior.
- It does not make Match Journal service results parser truth, analytics truth,
  merge readiness, deploy readiness, gameplay advice, hidden-card inference,
  archetype classification, player-mistake labels, or AI coaching.

## Open Questions And Contract Risks

- Composite operations may require careful validation because repository writes
  are atomic per operation. This contract requires prevalidation and forbids
  false success, but it does not authorize ad hoc direct SQL or repository
  transaction redesign.
- The exact Python result representation is flexible. Codex C may use
  dataclasses, typed dictionaries, or documented dictionaries as long as
  semantic fields are preserved.
- `get_journal_bundle` is included in v1 only as a local repository read model.
  If Codex C finds that useful bundles require analytics joins or runtime
  state, it must defer the bundle or route back to Codex B.
- No filesystem database test is required. If Codex C needs one, it must use a
  temporary directory and keep generated artifacts out of the repo.

## Codex C Handoff Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #200, Match Journal local service/use-case boundary.

  Context:
  - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/200
  - Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/198
  - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/199
  - Previous merge commit: 1ac67bc61269f423131a19db0a92b935591fa5a5
  - Prior Match Journal foundation: issue #196 / PR #197
  - Branch: codex/match-journal-service
  - Base: main
  - Contract: docs/contracts/match_journal_service.md
  - Expected handoff artifact: docs/implementation_handoffs/match_journal_service_comparison.md

  Goal:
  Compare current main against the Match Journal service contract. Implement only the smallest local service/use-case API and focused tests needed to satisfy the contract.

  Read first:
  - AGENTS.md
  - docs/agent_rules.yml
  - docs/agent_constitution.md
  - docs/codex_module_workflow.md
  - docs/agent_threads/implementation.md
  - docs/contracts/match_journal_service.md
  - docs/contracts/match_journal_repository.md
  - docs/implementation_handoffs/match_journal_repository_comparison.md
  - docs/contract_test_reports/match_journal_repository.md
  - docs/contracts/match_journal_local_sqlite_schema.md
  - src/mythic_edge_parser/app/match_journal_repository.py
  - src/mythic_edge_parser/app/match_journal_migration_loader.py
  - tests/test_match_journal_repository.py
  - tests/test_match_journal_schema.py

  Implement:
  - src/mythic_edge_parser/app/match_journal_service.py
  - tests/test_match_journal_service.py
  - docs/implementation_handoffs/match_journal_service_comparison.md

  Required behavior:
  - Service accepts an existing MatchJournalRepository and may provide explicit from_connection construction over caller-owned SQLite connections.
  - Service never opens the default database path, reads environment variables, reads parser runtime state, calls status API state, or creates generated artifacts.
  - Service supports intent-level operations for match/game/sideboarding/unattached notes, experiment labels, pilot-error status, pilot-error reason, manual opponent archetype/tier labels, review flags, display-only corrections, and local journal bundles where possible.
  - Service preserves unattached notes without parser IDs.
  - Service treats parser match/game IDs as references only and never invents them.
  - Service keeps pilot-error status and reason separately queryable.
  - Service keeps opponent labels manual and non-inferred.
  - Service keeps field corrections journal_display_only.
  - Tests use in-memory SQLite and deterministic repository seams.

  Do not:
  - Open a PR or commit unless explicitly asked.
  - Target main directly.
  - Change Match Journal schema or repository public behavior unless a blocking mismatch routes back to Codex B.
  - Create or commit SQLite database files, WAL, SHM, journal files, raw logs, generated data, runtime artifacts, failed posts, workbook exports, secrets, credentials, API keys, tokens, or webhook URLs.
  - Store raw Player.log payloads in SQLite.
  - Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, analytics ingest, analytics views, production behavior, Google Sheets sync behavior, overlay behavior, OpenAI/model-provider behavior, or AI/coaching behavior.
  - Let Match Journal notes, labels, review flags, field override proposals, service result shapes, or bundles become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching.

  Validation:
  - python3 -m pytest -q tests/test_match_journal_schema.py
  - python3 -m pytest -q tests/test_match_journal_repository.py
  - python3 -m pytest -q tests/test_match_journal_service.py
  - python3 -m pytest -q tests/test_analytics_schema.py
  - python3 -m ruff check src tests tools
  - git diff --check
  - Run path-scoped secret/private marker and protected-surface checks for changed files.
  - Verify no generated SQLite/local/private artifacts are staged or committed.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/200"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/198"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/199"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/match_journal_service.md"
  target_artifact: "docs/implementation_handoffs/match_journal_service_comparison.md"
  verdict: "contract_ready_for_module_implementer"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/match-journal-service"
  validation:
    - "documentation-only contract writer pass"
    - "Codex C should run python3 -m pytest -q tests/test_match_journal_schema.py"
    - "Codex C should run python3 -m pytest -q tests/test_match_journal_repository.py"
    - "Codex C should run python3 -m pytest -q tests/test_match_journal_service.py"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_schema.py"
    - "Codex C should run python3 -m ruff check src tests tools"
    - "Codex C should run git diff --check"
    - "Codex C should run path-scoped secret/private marker and protected-surface checks"
  stop_conditions:
    - "Do not target main directly."
    - "Do not change Match Journal schema or repository public behavior unless a blocking mismatch routes back to Codex B."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
    - "Do not implement overlay, local HTTP/status API, Google Sheets sync/export, journal_sheet_sync_queue, analytics joins, OpenAI/model-provider behavior, AI coaching, external website refresh, parser behavior, workbook/webhook/App Script behavior, or production behavior."
    - "Do not let Match Journal records, service result shapes, or bundles become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching."
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/200"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/198"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/199"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/match_journal_service.md"
  target_artifact: "docs/implementation_handoffs/match_journal_service_comparison.md"
  verdict: "contract_ready_for_module_implementer"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/match-journal-service"
  validation:
    - "documentation-only contract writer pass"
    - "Codex C should run python3 -m pytest -q tests/test_match_journal_schema.py"
    - "Codex C should run python3 -m pytest -q tests/test_match_journal_repository.py"
    - "Codex C should run python3 -m pytest -q tests/test_match_journal_service.py"
    - "Codex C should run python3 -m pytest -q tests/test_analytics_schema.py"
    - "Codex C should run python3 -m ruff check src tests tools"
    - "Codex C should run git diff --check"
    - "Codex C should run path-scoped secret/private marker and protected-surface checks"
  stop_conditions:
    - "Do not target main directly."
    - "Do not change Match Journal schema or repository public behavior unless a blocking mismatch routes back to Codex B."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
    - "Do not implement overlay, local HTTP/status API, Google Sheets sync/export, journal_sheet_sync_queue, analytics joins, OpenAI/model-provider behavior, AI coaching, external website refresh, parser behavior, workbook/webhook/App Script behavior, or production behavior."
    - "Do not let Match Journal records, service result shapes, or bundles become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching."
```
