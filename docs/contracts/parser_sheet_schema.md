# Parser Sheet Schema Module Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/46

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Problem-representation docs read because issue #46 is the source problem
representation:

- `docs/agent_threads/problem_representation.md`
- `docs/templates/problem_representation.md`

Adjacent contracts:

- `docs/contracts/parser_models.md`
- `docs/contracts/parser_state.md`
- `docs/contracts/parser_runner.md`
- `docs/contracts/parser_outputs.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the Python-side workbook/schema registry in
`src/mythic_edge_parser/app/sheet_schema.py`. It is a contract artifact only. It
does not implement code, change workbook schema, change Apps Script behavior,
or change parser/runtime behavior.

## Module

`src/mythic_edge_parser/app/sheet_schema.py`

The module centralizes workbook-facing schema vocabulary that Python code and
Apps Script must agree on:

- Match Log sync-field names
- Game Log sync-field names
- runtime landing-sheet header tuples
- runtime row-family names
- runtime event-type names
- runtime row scopes
- `RuntimeSheetSpec` records
- lookup helpers for runtime families and sync row kinds

Plain English: this module names the columns and row families that already
constructed parser/runtime rows are expected to use. It does not build row
values, post webhooks, edit workbooks, deploy Apps Script, classify parser
events, decide match/game truth, or reconcile final results.

## Owning Layer

Workbook-facing schema boundary inside the parser module audit suite.

Truth boundary:

- `sheet_schema.py` owns Python-side schema vocabulary: sync-field tuples,
  runtime header tuples, row-family names, event-type names, scopes, row-kind
  keys, and lookup behavior.
- `app/models.py` owns Match Log and Game Log row value construction.
- `app/state.py` owns parser state, changed-field detection, posted-row
  snapshots, and live/final parser truth.
- `app/sheet_exports.py` owns runtime row value construction and export
  dedupe/fingerprint behavior.
- `app/runner.py` owns when rows are built and submitted.
- `app/outputs.py` owns output transport and local JSONL archive mechanics.
- `tools/google_apps_script/Code.gs` consumes schema names through landing
  headers and field maps; it does not own parser truth.
- Workbook formulas, dashboard logic, webhook delivery, output transport, Apps
  Script, and AI-generated interpretation must not become owners of
  parser-owned truth through schema work.

## Files Owned By This Contract

- `src/mythic_edge_parser/app/sheet_schema.py`
- `tests/test_sheet_schema.py`
- `docs/contracts/parser_sheet_schema.md`

Related files whose behavior is referenced but not owned by this contract:

- `src/mythic_edge_parser/app/models.py`
- `tests/test_app_models.py`
- `src/mythic_edge_parser/app/state.py`
- `tests/test_state.py`
- `src/mythic_edge_parser/app/sheet_exports.py`
- `tests/test_sheet_exports.py`
- `src/mythic_edge_parser/app/runner.py`
- `tests/test_runner.py`
- `src/mythic_edge_parser/app/outputs.py`
- `tests/test_app_outputs.py`
- `src/mythic_edge_parser/app/transforms.py`
- `tests/test_transforms.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `tests/test_runtime_surfaces.py`
- `tools/google_apps_script/Code.gs`
- `docs/contracts/parser_models.md`
- `docs/contracts/parser_state.md`
- `docs/contracts/parser_runner.md`
- `docs/contracts/parser_outputs.md`

## Public Interface

### Match Log Sync Fields

`MATCH_LOG_SYNC_FIELDS: tuple[str, ...]`

Observed current ordered values:

```python
(
    "Date",
    "My Rank",
    "G1 Play / Draw",
    "Game 1 Result",
    "G2 Play / Draw",
    "Game 2 Result",
    "G3 Play / Draw",
    "Game 3 Result",
    "Games Won",
    "Games Lost",
    "Match Win?",
    "Total Games",
    "Match Win Flag",
    "Game Win %",
    "MTGA Match ID",
    "MTGA Format",
    "MTGA Event ID",
    "MTGA Queue Type",
    "G1 Mulligans",
    "G2 Mulligans",
    "G3 Mulligans",
    "G1 Turn Count",
    "G2 Turn Count",
    "G3 Turn Count",
    "MGTA Start Time",
    "MTGA End Time",
    "MTGA Rank Raw",
    "MTGA Mulligans",
    "MTGA Sideboard Entered",
    "MTGA Submit Deck Seen",
    "MTGA Sync Status",
)
```

Contract status:

- Public workbook-facing compatibility tuple.
- Consumed by `state.py` changed-field detection.
- Must remain ordered and stable unless a future schema migration contract
  authorizes a change.
- Every listed field must be emitted by `MatchSummary.to_match_log_row()`.
- Apps Script `buildMatchLogFieldMap_()` must continue to expose exactly these
  field-map keys.
- `"MGTA Start Time"` is a legacy external workbook compatibility spelling and
  must not be casually corrected to `"MTGA Start Time"` without an explicit
  migration issue, workbook/App Script plan, rollback plan, and tests.

### Game Log Sync Fields

`GAME_LOG_SYNC_FIELDS: tuple[str, ...]`

Observed current ordered values:

```python
(
    "Date",
    "MTGA Format",
    "My Rank",
    "MTGA Match ID",
    "Game Number",
    "Pre / Postboard",
    "Play / Draw",
    "Mulligans",
    "Opening Hand Size",
    "Opening Hand",
    "Mulliganed Away",
    "Game Result",
    "Turn Count",
    "Game Duration",
    "MTGA Event ID",
    "MTGA Queue Type",
)
```

Contract status:

- Public workbook-facing compatibility tuple.
- Consumed by `state.py` changed-field detection.
- Must remain ordered and stable unless a future schema migration contract
  authorizes a change.
- Every listed field must be emitted by `GameSummary.to_game_log_row()` through
  `MatchSummary.to_game_sheet_rows()`.
- Apps Script `buildGameLogFieldMap_()` must continue to expose exactly these
  field-map keys.

### Runtime Landing Headers

`ACTION_LOG_HEADERS`

```python
(
    "Generated At",
    "MTGA Match ID",
    "Game Number",
    "Turn Number",
    "Timestamp",
    "Action Type",
    "Cast Mode",
    "grpId",
    "Card Name",
    "Display Name",
    "Resolution Status",
    "Actor",
    "From Zone",
    "To Zone",
    "Summary",
)
```

`DECK_SNAPSHOT_HEADERS`

```python
(
    "Generated At",
    "Submitted At",
    "MTGA Match ID",
    "Deck Signature",
    "Deck Name",
    "Deck Match Mode",
    "Deck Format",
    "Section",
    "Arena ID",
    "Count",
    "Card Name",
    "Rarity",
    "Set",
    "Type Line",
    "Colors",
    "Owned Copies",
    "Missing Copies",
)
```

`COLLECTION_SNAPSHOT_HEADERS`

```python
(
    "Generated At",
    "Collection Available",
    "Inventory Available",
    "Owned Unique Cards",
    "Owned Total Card Copies",
    "Owned By Rarity",
    "Inventory Gold",
    "Inventory Gems",
    "Wildcards Common",
    "Wildcards Uncommon",
    "Wildcards Rare",
    "Wildcards Mythic",
    "Active Deck Missing By Rarity",
    "Active Deck Completion Rate",
    "Wanted Cards",
)
```

`PARSER_STATUS_HEADERS`

```python
(
    "Updated At",
    "Status",
    "Current Match ID",
    "Current Game Number",
    "Current Player Team",
    "Last Event Kind",
    "Last Event At",
    "Webhook Successes",
    "Webhook Failures",
    "Event Failures",
    "Router Failures",
    "Active Deck Signature",
    "Active Deck Name",
    "Active Match Action Count",
)
```

`CARD_PERFORMANCE_HEADERS`

```python
(
    "Generated At",
    "Card Key",
    "grpId",
    "Card Name",
    "Display Name",
    "Resolution Status",
    "Layout",
    "Card Faces",
    "Games Seen",
    "Seen In Game",
    "Seen Win Rate",
    "Opening Hand Games",
    "Opening Hand Win Rate",
    "Cast Games",
    "Cast Win Rate",
    "Postboard Cast Games",
    "Postboard Cast Win Rate",
    "Mulliganed Away Games",
    "Mulligan Tax",
    "Top Matchups",
    "Top Packages",
)
```

Contract status:

- Public runtime landing-header tuples.
- Header order is part of the public contract.
- Each tuple must match the corresponding
  `WORKBOOK_SCHEMA.landingHeaders.<family>` array in Apps Script by exact
  order, not only set membership.
- Header tuple changes are workbook schema changes and require explicit
  migration authorization.

### Runtime Sheet Spec

`RuntimeSheetSpec`

Observed shape:

```python
@dataclass(frozen=True, slots=True)
class RuntimeSheetSpec:
    family: str
    event_type: str
    scope: str
    headers: tuple[str, ...]
```

Contract status:

- Public immutable dataclass value used by `sheet_exports.py`.
- The dataclass fields and meaning must remain stable.
- `family` is the webhook/runtime row `event_family`.
- `event_type` is the runtime row `event_type`.
- `scope` is the runtime row `scope`.
- `headers` is the exact workbook landing-header tuple.

### Runtime Family Constants

Observed current values:

| Constant | Value |
| --- | --- |
| `ACTION_LOG_FAMILY` | `"ActionLogRow"` |
| `DECK_SNAPSHOT_FAMILY` | `"DeckSnapshotRow"` |
| `COLLECTION_SNAPSHOT_FAMILY` | `"CollectionSnapshotRow"` |
| `PARSER_STATUS_FAMILY` | `"ParserStatusRow"` |
| `CARD_PERFORMANCE_FAMILY` | `"CardPerformanceRow"` |

Contract status:

- Public row-family vocabulary consumed by `sheet_exports.py`, `outputs.py`
  quiet logging, Apps Script dispatch, and workbook landing logic.
- Values must remain stable unless a schema/App Script migration contract
  explicitly changes all consumers together.

### Runtime Sheet Specs

`RUNTIME_SHEET_SPECS: dict[str, RuntimeSheetSpec]`

Observed current mapping:

| Family | Event type | Scope | Headers |
| --- | --- | --- | --- |
| `ActionLogRow` | `action_log_row` | `Match` | `ACTION_LOG_HEADERS` |
| `DeckSnapshotRow` | `deck_snapshot_row` | `Deck` | `DECK_SNAPSHOT_HEADERS` |
| `CollectionSnapshotRow` | `collection_snapshot_row` | `Collection` | `COLLECTION_SNAPSHOT_HEADERS` |
| `ParserStatusRow` | `parser_status_row` | `Runtime` | `PARSER_STATUS_HEADERS` |
| `CardPerformanceRow` | `card_performance_row` | `Card` | `CARD_PERFORMANCE_HEADERS` |

Contract status:

- Public runtime sheet family registry.
- Keys must match the corresponding `RuntimeSheetSpec.family` values.
- Event types and scopes are public row vocabulary.
- Adding, removing, or renaming a family is a schema/App Script change and
  requires a migration contract.

### Sync Field Registry

`SYNC_FIELDS_BY_ROW_KIND: dict[str, tuple[str, ...]]`

Observed current mapping:

| Row kind | Tuple |
| --- | --- |
| `"match_log"` | `MATCH_LOG_SYNC_FIELDS` |
| `"game_log"` | `GAME_LOG_SYNC_FIELDS` |

Contract status:

- Public row-kind vocabulary for sync-field lookup.
- Adding, removing, or renaming row kinds requires a contract and tests.

### Lookup Helpers

`runtime_sheet_spec(event_family: str) -> RuntimeSheetSpec`

- Returns `RUNTIME_SHEET_SPECS[event_family]`.
- Unknown `event_family` raises direct `KeyError`.

`runtime_sheet_headers(event_family: str) -> tuple[str, ...]`

- Returns `runtime_sheet_spec(event_family).headers`.
- Unknown `event_family` raises direct `KeyError` through
  `runtime_sheet_spec()`.

`sync_fields(row_kind: str) -> tuple[str, ...]`

- Returns `SYNC_FIELDS_BY_ROW_KIND[row_kind]`.
- Unknown `row_kind` raises direct `KeyError`.

Contract status:

- Direct `KeyError` is fail-fast schema validation. Do not soften unknown-key
  behavior without an explicit contract and tests.
- These helpers do not normalize case, trim whitespace, invent defaults, or
  return empty tuples for unknown values.

## Inputs

### Schema Lookup Inputs

| Input | Type | Source | Accepted values |
| --- | --- | --- | --- |
| `event_family` | `str` | `sheet_exports.py`, tests, future runtime callers | Runtime family constants listed above. |
| `row_kind` | `str` | tests or future sync callers | `"match_log"`, `"game_log"`. |

Malformed or unknown values raise `KeyError`.

### Row Value Inputs From Adjacent Modules

`sheet_schema.py` does not read row values, but its constants constrain adjacent
row builders:

- `MatchSummary.to_match_log_row()` must emit every `MATCH_LOG_SYNC_FIELDS`
  key.
- `GameSummary.to_game_log_row()` through `MatchSummary.to_game_sheet_rows()`
  must emit every `GAME_LOG_SYNC_FIELDS` key.
- `sheet_exports.py` runtime rows must use event family, event type, and scope
  values from `RuntimeSheetSpec`.
- Apps Script build-object functions must map runtime row data keys into the
  display headers named by the corresponding runtime header tuple.

### Apps Script Schema Inputs

Relevant Apps Script surfaces:

- `WORKBOOK_SCHEMA.landingHeaders.actionLog`
- `WORKBOOK_SCHEMA.landingHeaders.deckSnapshot`
- `WORKBOOK_SCHEMA.landingHeaders.collectionSnapshot`
- `WORKBOOK_SCHEMA.landingHeaders.parserStatus`
- `WORKBOOK_SCHEMA.landingHeaders.cardPerformance`
- `buildMatchLogFieldMap_(data)`
- `buildGameLogFieldMap_(data)`
- runtime row dispatch on `data.event_family`

Contract:

- Python runtime header tuples must align with Apps Script landing headers by
  exact order.
- Python sync-field tuples must align with Apps Script Match Log and Game Log
  field-map keys.
- Apps Script data-key mapping remains Apps Script-owned and sheet-export-owned;
  `sheet_schema.py` owns display header vocabulary, not snake_case payload key
  construction.

## Outputs

### Sync Field Tuples

Destination:

- `app/state.py` changed-field detection
- `tests/test_app_models.py`
- Apps Script alignment tests
- future schema-drift tests

Behavior:

- State iterates sync fields in tuple order when producing changed-field
  lists.
- On first post, fields whose normalized row value is blank are not included in
  changed fields.
- On later posts, any normalized value change for a listed field is included.
- These state comparison rules are state-owned; `sheet_schema.py` owns only the
  field list.

### Runtime Sheet Specs

Destination:

- `app/sheet_exports.py` `_base_runtime_row()`
- runtime rows posted through runner/output transport
- Apps Script `event_family` dispatch
- workbook landing sheets

Behavior:

- Runtime rows receive `event_family`, `event_type`, and `scope` from the spec.
- Header tuples define workbook landing headers but do not build row values.
- Successful webhook transport does not prove workbook schema alignment unless
  Apps Script and workbook landing headers still match these tuples.

## Observed Current Behavior

- `sheet_schema.py` has no file, network, workbook, runtime-state, or webhook
  side effects at import time.
- Sync-field values are tuples.
- Runtime header values are tuples.
- `RuntimeSheetSpec` is a frozen, slotted dataclass.
- `RUNTIME_SHEET_SPECS` and `SYNC_FIELDS_BY_ROW_KIND` are mutable dictionaries
  despite containing public schema values.
- Lookup helpers are direct dict lookups and raise `KeyError` for unknown keys.
- Existing focused tests cover:
  - Action Log runtime sheet spec fields.
  - `sync_fields("game_log")`.
  - `sync_fields("match_log")`.
  - Apps Script Match Log field-map keys matching Python match sync fields by
    set.
  - Apps Script Game Log field-map keys matching Python game sync fields by
    set.
- Existing model tests cover that representative Match Log and Game Log rows
  contain every Python sync field.
- Existing sheet export tests cover that runtime rows can emit all five runtime
  row families.
- The current Apps Script `WORKBOOK_SCHEMA.landingHeaders` arrays match the
  Python runtime header tuples by exact observed order.
- The current Apps Script Match Log parser-managed headers include
  `"MGTA Start Time"`, matching the Python sync field and model row spelling.

## Required Guarantees

### Schema Registry Boundary

- `sheet_schema.py` must remain a schema-vocabulary registry.
- It must not build semantic row values.
- It must not parse MTGA logs.
- It must not decide match/game identity, winners, play/draw, mulligans,
  opening hands, rank buckets, final reconciliation, or deduplication truth.
- It must not post webhooks, write local JSONL files, edit workbooks, call Apps
  Script, or mutate runtime status files.

### Workbook Schema Stability

- Header strings and header order are protected compatibility surfaces.
- Runtime family strings, event types, and scopes are protected compatibility
  surfaces.
- Match Log and Game Log sync-field tuples are protected compatibility
  surfaces.
- Any schema change requires an explicit issue/contract that names affected
  Python row builders, state changed-field behavior, Apps Script field maps,
  landing headers, workbook tabs, tests, rollback/migration plan, and PR drift
  budget.

### Apps Script Alignment

- Runtime landing headers in Python must match Apps Script
  `WORKBOOK_SCHEMA.landingHeaders` by exact order.
- Match Log sync fields in Python must match Apps Script
  `buildMatchLogFieldMap_()` keys.
- Game Log sync fields in Python must match Apps Script
  `buildGameLogFieldMap_()` keys.
- Apps Script dispatch on `event_family` must remain compatible with the
  runtime family constants.
- This contract does not authorize changing deployed Apps Script behavior.

### Model/State/Export Alignment

- `MatchSummary.to_match_log_row()` must continue to include every
  `MATCH_LOG_SYNC_FIELDS` key.
- `GameSummary.to_game_log_row()` must continue to include every
  `GAME_LOG_SYNC_FIELDS` key.
- `state.py` changed-field output must continue to use only the fields from the
  corresponding sync-field tuple.
- `sheet_exports.py` runtime rows must continue to use
  `RuntimeSheetSpec.family`, `.event_type`, and `.scope` for row metadata.
- Runtime row value keys and Apps Script build-object data-key mapping are
  adjacent contracts; schema work must not silently reshape webhook payloads.

### Legacy Header Compatibility

- `"MGTA Start Time"` is an observed external compatibility value, not a typo to
  fix during routine cleanup.
- Renaming it is a workbook schema and Apps Script migration, not a spelling
  cleanup.
- Until a migration is explicitly authorized, Python sync fields, model rows,
  Apps Script field maps, and parser-managed header lists must preserve this
  exact spelling.

### Fail-Fast Unknowns

- Unknown runtime `event_family` values must continue to raise `KeyError` from
  `runtime_sheet_spec()` and `runtime_sheet_headers()`.
- Unknown sync `row_kind` values must continue to raise `KeyError` from
  `sync_fields()`.
- Do not change unknown-key behavior to return blank values, empty tuples, or
  fallback specs without a new contract.

## Unknowns And Suspected Gaps

- Current focused tests cover only the Action Log runtime sheet spec directly.
  Other runtime families need direct spec tests for family, event type, scope,
  and headers.
- Current Apps Script sync-field tests compare sets, not ordered tuples.
  Because state changed-field lists are ordered, order should be tested.
- Current tests do not appear to assert exact ordered runtime header alignment
  between Python and Apps Script landing headers.
- Current tests do not appear to assert `runtime_sheet_headers()` behavior.
- Current tests do not appear to assert `KeyError` for unknown runtime family
  or row kind.
- Current tests do not appear to assert that `"MGTA Start Time"` remains present
  across Python sync fields, model rows, and Apps Script field maps.
- Current tests do not appear to verify Apps Script runtime build-object keys
  cover every runtime landing header.
- Current tests do not snapshot all schema constants in one place. A future
  code-hardening schema snapshot issue may be useful, but that is outside this
  contract writer pass.

These are test obligations and review targets. They are not authorization to
change schema behavior during contract writing.

## Error Behavior

- Unknown `event_family` raises `KeyError`.
- Unknown `row_kind` raises `KeyError`.
- Non-string inputs are not normalized by `sheet_schema.py`; direct dict lookup
  semantics apply.
- The module does not catch or wrap errors from consumers.
- The module does not validate Apps Script alignment at runtime.
- The module does not validate workbook tabs at runtime.

Required behavior:

- Preserve direct fail-fast lookup behavior unless a future contract changes
  it.
- Keep schema validation in tests/review, not in workbook formulas or
  transport fallbacks.

## Side Effects

Observed current side effects:

- None at import time.
- No files written.
- No runtime state mutated.
- No webhooks posted.
- No workbook tabs updated.
- No Apps Script calls made.

Forbidden side effects for this contract:

- Do not change parser behavior.
- Do not change parser state final reconciliation.
- Do not change workbook schema.
- Do not change webhook payload shape.
- Do not change Apps Script behavior.
- Do not change parser event classes.
- Do not change match/game identity.
- Do not change deduplication semantics.
- Do not change secrets or environment variables.
- Do not commit raw logs, generated data, runtime status files, failed posts, or
  workbook exports.
- Do not open a module PR from the contract writer pass.
- Do not mark tracker #5 complete.

## Dependency Order

Future implementation or fixer work should proceed in this order:

1. Compare current `sheet_schema.py` constants and helpers to this contract.
2. Add or update focused tests for current contracted behavior.
3. Verify Python sync fields against model row keys.
4. Verify Python sync fields against Apps Script field-map keys, including
   order where order is meaningful.
5. Verify Python runtime headers against Apps Script landing headers by exact
   order.
6. Verify runtime family/event-type/scope vocabulary for every family.
7. Verify unknown-key `KeyError` behavior.
8. Produce the implementation handoff.
9. Route to Codex E for contract-test review.

If satisfying a test requires changing a header, family, event type, scope,
Apps Script mapping, workbook row shape, or parser-owned fact, stop and route
back to Codex B or A instead of implementing a schema migration silently.

## Compatibility

Compatibility surfaces that must remain stable:

- `MATCH_LOG_SYNC_FIELDS`
- `GAME_LOG_SYNC_FIELDS`
- all runtime header tuples
- `RuntimeSheetSpec` fields
- runtime family constants
- `RUNTIME_SHEET_SPECS`
- `SYNC_FIELDS_BY_ROW_KIND`
- lookup helper names and direct `KeyError` behavior
- Apps Script runtime landing header names and order
- Apps Script Match Log and Game Log field-map keys
- `"MGTA Start Time"` spelling

Breaking changes requiring a new or amended contract:

- adding, removing, renaming, or reordering sync fields
- adding, removing, renaming, or reordering runtime landing headers
- changing runtime family strings
- changing runtime event types
- changing runtime scopes
- changing unknown-key behavior
- changing Apps Script dispatch or field maps
- changing workbook tabs, workbook formulas, workbook schema, or webhook
  payload shape

## Tests Required

Contract-writer validation:

```bash
git diff --check
```

Focused implementation validation:

```bash
python3 -m pytest -q tests/test_sheet_schema.py
python3 -m pytest -q tests/test_app_models.py tests/test_sheet_exports.py tests/test_runtime_surfaces.py
python3 -m pytest -q tests/test_state.py tests/test_runner.py tests/test_app_outputs.py tests/test_transforms.py
python3 -m ruff check src tests
git diff --check
```

Required focused test coverage for Codex C:

- Every `RUNTIME_SHEET_SPECS` entry has the expected family, event type, scope,
  and exact header tuple.
- `runtime_sheet_headers(family)` returns the same tuple as the corresponding
  spec.
- Unknown `runtime_sheet_spec()`, `runtime_sheet_headers()`, and
  `sync_fields()` inputs raise `KeyError`.
- `SYNC_FIELDS_BY_ROW_KIND` maps exactly `"match_log"` and `"game_log"` to the
  public sync-field tuples.
- `MATCH_LOG_SYNC_FIELDS` and `GAME_LOG_SYNC_FIELDS` order is stable.
- Apps Script Match Log and Game Log field-map keys match Python sync fields.
- Runtime Python header tuples match Apps Script `WORKBOOK_SCHEMA.landingHeaders`
  arrays by exact order.
- Representative model-produced Match Log and Game Log rows include every
  sync-field key.
- `"MGTA Start Time"` is present in the Match Log sync tuple, model row, and
  Apps Script field map.
- Runtime row families emitted by `sheet_exports.py` remain exactly:
  `ActionLogRow`, `DeckSnapshotRow`, `CollectionSnapshotRow`,
  `ParserStatusRow`, and `CardPerformanceRow`.

Before submitter opens or updates a module PR:

```bash
python3 -m pytest -q
python3 -m ruff check src tests
```

Protected-surface sanity should also record a name-only diff showing no
unauthorized raw logs, generated data, runtime status files, failed posts,
workbook exports, secrets, environment changes, parser event class changes,
parser state final reconciliation changes, workbook schema changes, webhook
payload shape changes, or Apps Script behavior changes.

## Acceptance Criteria

- `docs/contracts/parser_sheet_schema.md` exists.
- The contract names `sheet_schema.py` as the Python-side workbook/schema
  registry.
- The contract lists public constants, helper functions, row-family vocabulary,
  event types, scopes, row kinds, sync fields, and runtime headers.
- The contract separates schema vocabulary from parser truth, row construction,
  output transport, Apps Script behavior, and workbook formulas.
- The contract preserves direct `KeyError` behavior for unknown family/row-kind
  lookups.
- The contract records `"MGTA Start Time"` as legacy compatibility spelling.
- The contract defines Apps Script, model/state, and sheet-export alignment
  expectations.
- The contract lists suspected test gaps and validation obligations.
- The contract routes next work to Codex C on
  `codex/parser-module-audit-suite`.

## Handoff Packet

Role performed: Codex B: Module Contract Writer

Source problem representation: https://github.com/Tahjali11/Mythic-Edge/issues/46

Contract produced: `docs/contracts/parser_sheet_schema.md`

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/5

Risk tier: High

Owning truth layer: workbook-facing schema boundary inside the parser module
audit suite

Public interface:

- `MATCH_LOG_SYNC_FIELDS`
- `GAME_LOG_SYNC_FIELDS`
- runtime header tuples
- `RuntimeSheetSpec`
- runtime family constants
- `RUNTIME_SHEET_SPECS`
- `SYNC_FIELDS_BY_ROW_KIND`
- `runtime_sheet_spec()`
- `runtime_sheet_headers()`
- `sync_fields()`

Invariants:

- Schema constants remain stable unless a migration contract authorizes change.
- Parser truth remains parser/state owned.
- Apps Script and workbook consumers must align with Python schema vocabulary
  without becoming parser truth owners.
- Unknown lookup keys remain fail-fast `KeyError`s.
- `"MGTA Start Time"` remains a protected legacy compatibility spelling.

Required tests:

- `tests/test_sheet_schema.py`
- `tests/test_app_models.py`
- `tests/test_sheet_exports.py`
- `tests/test_runtime_surfaces.py`
- relevant state/runner/output/transform regression checks
- Ruff and `git diff --check`

Acceptance criteria:

- Add missing tests for current contracted schema behavior.
- Do not change schema, Apps Script, parser truth, workbook shape, webhook
  payload shape, or protected artifacts.
- Produce implementation handoff and route to Codex E.

Open questions or contract risks:

- Runtime landing-header order currently appears aligned with Apps Script but
  should be covered by focused tests.
- Existing sync-field Apps Script tests are set-based and should be reviewed
  for order sensitivity.
- A future hardening schema snapshot issue may be useful, but this module
  contract does not create that workflow.

Next recommended thread role: Codex C: Module Implementer

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer for issue #46 and docs/contracts/parser_sheet_schema.md.

Goal:
Compare the current sheet_schema.py workbook/schema registry and focused tests against the parser sheet-schema contract. Implement only the smallest coherent test and documentation changes needed to satisfy the contract, preserving current schema behavior.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/46
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/parser_sheet_schema.md
- docs/contracts/parser_models.md
- docs/contracts/parser_state.md
- docs/contracts/parser_runner.md
- docs/contracts/parser_outputs.md
- src/mythic_edge_parser/app/sheet_schema.py
- tests/test_sheet_schema.py
- src/mythic_edge_parser/app/models.py
- tests/test_app_models.py
- src/mythic_edge_parser/app/state.py
- tests/test_state.py
- src/mythic_edge_parser/app/sheet_exports.py
- tests/test_sheet_exports.py
- src/mythic_edge_parser/app/outputs.py
- tests/test_app_outputs.py
- src/mythic_edge_parser/app/transforms.py
- tests/test_transforms.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- tests/test_runtime_surfaces.py
- tools/google_apps_script/Code.gs

Do:
- Compare current code/tests against the contract before editing.
- Preserve sheet_schema.py as schema vocabulary, not parser truth or row construction.
- Add focused tests for contracted behavior not currently covered.
- Preserve exact header strings, header order, row-family strings, event types, scopes, row kinds, and direct KeyError behavior unless the contract is routed back for amendment.
- Preserve the legacy "MGTA Start Time" spelling.
- Produce docs/implementation_handoffs/parser_sheet_schema_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, output transport, or AI-generated interpretation.
- Change schema constants or Apps Script mappings unless a contract loopback explicitly authorizes a schema migration.
- Target main; module PR work belongs on codex/parser-module-audit-suite.
- Mark tracker #5 complete.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/46"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_sheet_schema.md"
  target_artifact: "docs/implementation_handoffs/parser_sheet_schema_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "python3 -m pytest -q tests/test_sheet_schema.py"
    - "python3 -m pytest -q tests/test_app_models.py tests/test_sheet_exports.py tests/test_runtime_surfaces.py"
    - "python3 -m pytest -q tests/test_state.py tests/test_runner.py tests/test_app_outputs.py tests/test_transforms.py"
    - "python3 -m ruff check src tests"
    - "git diff --check"
  stop_conditions:
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, output transport, or AI-generated interpretation."
    - "Do not change schema constants or Apps Script mappings unless a contract loopback explicitly authorizes a schema migration."
    - "Do not target main; module PR work belongs on codex/parser-module-audit-suite."
    - "Do not mark tracker #5 complete."
```
