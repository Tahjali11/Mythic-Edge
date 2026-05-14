# Parser Sheet Exports Module Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/52

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/5

Agent docs:

- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Problem-representation docs read because issue #52 is the source problem
representation:

- `docs/agent_threads/problem_representation.md`
- `docs/templates/problem_representation.md`

Adjacent contracts:

- `docs/contracts/parser_sheet_schema.md`
- `docs/contracts/parser_outputs.md`
- `docs/contracts/parser_runner.md`
- `docs/contracts/parser_state.md`

Branch target: `codex/parser-module-audit-suite`

This contract describes the runtime workbook export row builder in
`src/mythic_edge_parser/app/sheet_exports.py`. It is a contract artifact only.
It does not implement code, change workbook schema, change Apps Script
behavior, or change parser/runtime behavior.

## Module

`src/mythic_edge_parser/app/sheet_exports.py`

The module converts already-produced parser/runtime artifacts into runtime
landing-sheet row dictionaries:

- Action Log rows from active match action payloads
- Deck Snapshot rows from active deck profile payloads
- Collection Snapshot rows from collection profile payloads
- Parser Status rows from the latest runtime status payload
- Card Performance rows from card performance payloads

Plain English: `sheet_exports.py` builds workbook-facing runtime rows and
suppresses repeated exports in memory. It does not define workbook headers,
post webhooks, update Apps Script, parse Player.log, decide parser truth,
reconcile final results, or own match/game identity.

## Owning Layer

Runtime export row construction inside the parser module audit suite.

Truth boundary:

- `sheet_exports.py` owns Python-side construction of runtime row dictionaries
  for the five runtime sheet families, and owns its in-memory duplicate
  suppression for those rows.
- `app/sheet_schema.py` owns row-family names, event types, scopes, and
  workbook header tuples. Sheet export work must consume those schema constants
  and must not redefine or migrate them.
- `app/analytics_sidecar.py` owns when runtime exports are requested for a
  parser event and which export flags are enabled for that event.
- `app/gameplay_actions.py` owns active match action payload generation.
- `app/card_performance.py` owns card performance payload generation.
- `app/diagnostics.py` and `app/status_api.py` own runtime status artifact
  schemas and runtime status writes.
- `app/outputs.py` owns webhook dispatch and local output archive mechanics
  after export rows are returned.
- `tools/google_apps_script/Code.gs` consumes the snake_case runtime row fields
  and maps them to workbook headers; it does not own parser truth.
- Workbook formulas, dashboard logic, Apps Script, webhook delivery, output
  transport, and AI-generated interpretation must not become sources of
  parser-owned truth through sheet export work.

## Files Owned By This Contract

- `src/mythic_edge_parser/app/sheet_exports.py`
- `tests/test_sheet_exports.py`
- `docs/contracts/parser_sheet_exports.md`

Related files whose behavior is referenced but not owned by this contract:

- `src/mythic_edge_parser/app/sheet_schema.py`
- `docs/contracts/parser_sheet_schema.md`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- `tests/test_analytics_sidecar.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/card_performance.py`
- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/app/outputs.py`
- `tests/test_app_outputs.py`
- `src/mythic_edge_parser/app/runner.py`
- `tests/test_runner.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `tests/test_diagnostics.py`
- `src/mythic_edge_parser/app/status_api.py`
- `tests/test_status_api.py`
- `tools/google_apps_script/Code.gs`

## Public Interface

### State

`SheetExportState`

- Slotted dataclass storing in-memory duplicate suppression state.
- Public fields:
  - `posted_action_keys: set[str]`
  - `last_deck_snapshot_fingerprint: str`
  - `last_collection_snapshot_fingerprint: str`
  - `last_parser_status_fingerprint: str`
  - `last_card_performance_fingerprint: str`

`EXPORT_STATE`

- Module-global `SheetExportState` instance used by
  `collect_runtime_sheet_rows()`.
- Runtime-only state. It must not be serialized into workbook rows, raw logs,
  generated data, runtime status files, failed posts, or workbook exports.

`reset_sheet_export_state() -> None`

- Clears action row keys, snapshot fingerprints, and the JSON payload cache.
- Required for deterministic tests and for runtime reset behavior.
- Does not delete runtime artifacts from disk, post webhooks, or modify parser
  state.

### Main Export API

`collect_runtime_sheet_rows(...) -> list[dict[str, Any]]`

Keyword-only payload overrides:

- `action_payload: dict[str, Any] | None = None`
- `deck_payload: dict[str, Any] | None = None`
- `collection_payload: dict[str, Any] | None = None`
- `status_payload: dict[str, Any] | None = None`
- `card_performance_payload: dict[str, Any] | None = None`

Keyword-only export flags, all defaulting to `True`:

- `post_action_rows`
- `post_deck_snapshot_rows`
- `post_collection_snapshot_rows`
- `post_parser_status_rows`
- `post_card_performance_rows`

Observed current behavior:

- Returns runtime rows in family order:
  1. Action Log
  2. Deck Snapshot
  3. Collection Snapshot
  4. Parser Status
  5. Card Performance
- Uses caller-provided payload overrides when they are not `None`.
- Loads default runtime artifacts only for families whose caller payload
  override is `None` and whose export flag is enabled.
- Does not post rows. `analytics_sidecar.py` sends returned rows to
  `outputs.submit_row_to_google_sheets()`.
- Does not mutate parser state, workbook schema, Apps Script mappings, or
  output transport state.

Required guarantee:

- The function is the only public row collection entrypoint for this module.
- A disabled family flag must prevent that family from loading its default
  artifact and must prevent that family from emitting rows.
- Returned rows must include the metadata fields supplied by
  `_base_runtime_row()`:
  - `event_family`
  - `event_type`
  - `scope`
- Returned rows must keep the snake_case field names consumed by Apps Script
  unless a future schema migration contract explicitly authorizes a change.

### Contract-Covered Internal Helpers

The following helpers are underscore-prefixed and are not new public extension
points. Their behavior is contract-covered because focused tests or the main
export API observe their results:

- `_load_json_dict(path: Path) -> dict[str, Any]`
- `_safe_int(value: Any) -> int | str`
- `_stable_fingerprint(value: Any) -> str`
- `_without_keys(payload: dict[str, Any], keys_to_remove: set[str]) -> dict[str, Any]`
- `_base_runtime_row(event_family: str, **fields: Any) -> dict[str, Any]`
- `_status_snapshot_path() -> Path`
- `_rows_fingerprint(rows: list[dict[str, Any]], transient_keys: set[str]) -> str`
- `_row_fingerprint(row: dict[str, Any], transient_keys: set[str]) -> str`
- `_snapshot_rows_if_changed(...) -> list[dict[str, Any]]`
- `_snapshot_row_if_changed(...) -> list[dict[str, Any]]`
- `_action_row(entry: dict[str, Any], generated_at: str) -> dict[str, Any]`
- `_action_row_key(row: dict[str, Any]) -> str`
- `_deck_snapshot_rows(payload: dict[str, Any]) -> list[dict[str, Any]]`
- `_collection_snapshot_row(payload: dict[str, Any]) -> dict[str, Any]`
- `_parser_status_row(payload: dict[str, Any]) -> dict[str, Any]`
- `_card_performance_rows(payload: dict[str, Any]) -> list[dict[str, Any]]`

## Inputs

### Runtime Artifact Paths

When no payload override is provided, `sheet_exports.py` reads from imported
runtime artifact sources:

| Family | Source |
| --- | --- |
| Action Log | `load_active_match_actions_payload()` |
| Deck Snapshot | `_load_json_dict(ACTIVE_DECK_PROFILE_PATH)` |
| Collection Snapshot | `_load_json_dict(COLLECTION_PROFILE_PATH)` |
| Parser Status | `_load_json_dict(STATUS_ROOT / "manasight_status_latest.json")` |
| Card Performance | `load_card_performance_payload()` |

Required guarantee:

- `sheet_exports.py` must not create, delete, or rewrite these artifacts.
- Path names, environment variables, and artifact ownership stay with
  `config.py`, `gameplay_actions.py`, `card_performance.py`, diagnostics, and
  status modules.

### JSON Payload Loading

`_load_json_dict(path)` observes these rules:

- Missing file returns `{}`.
- Invalid JSON returns `{}`.
- Valid JSON whose top-level value is not a dict returns `{}`.
- Valid top-level dict returns the dict.
- Successful loads are cached by `(str(path), stat.st_mtime_ns)`.
- Stale successful cache entries for the same path are dropped when a new mtime
  key is cached.
- Failed loads are not cached.
- An `OSError` while statting uses a `None` mtime cache key.

Required guarantee:

- The loader is a best-effort dict loader, not a schema validator.
- It must not surface missing files or invalid JSON as runtime export crashes.
- It must not preserve non-dict top-level JSON as row data.

Unknown:

- The current code does not define a separate cache invalidation strategy for
  filesystems with unchanged `st_mtime_ns` after content changes. Any stronger
  invalidation rule requires a follow-up contract loopback.

### Accepted Action Payload Shape

Accepted top-level shape:

```python
{
    "generated_at": "2026-05-06T04:14:48+00:00",
    "entries": [
        {
            "match_id": "match-1",
            "game_number": 1,
            "turn_number": 3,
            "timestamp": "2026-05-06T00:14:48+00:00",
            "action_type": "cast",
            "cast_mode": "normal",
            "grp_id": 123,
            "card_name": "Duress",
            "display_name": "Duress",
            "resolution_status": "resolved",
            "actor_relation": "self",
            "from_zone_type": "ZoneType_Hand",
            "to_zone_type": "ZoneType_Stack",
            "summary": "cast Duress",
        }
    ],
}
```

Observed current behavior:

- `generated_at` is converted to a stripped string.
- `entries` defaults to `[]` when absent or falsey.
- Non-dict entries are skipped.
- Each dict entry produces at most one Action Log row, subject to action key
  deduplication.

### Accepted Deck Payload Shape

Accepted top-level shape:

```python
{
    "generated_at": "2026-05-06T04:14:48+00:00",
    "submitted_at": "2026-05-06T00:10:40+00:00",
    "match_id": "match-1",
    "signature": "deck-signature-1",
    "matched_decks": [
        {
            "name": "Azban Midrange",
            "match_mode": "same_pool_sideboarded",
            "format": "TraditionalStandard",
        }
    ],
    "mainboard": [{"arena_id": 77508, "count": 2, "name": "Duress"}],
    "sideboard": [],
}
```

Observed current behavior:

- Only the first dict in `matched_decks` contributes deck name, match mode, and
  format.
- Non-list `matched_decks` or an empty `matched_decks` list behaves like no
  matched deck.
- `mainboard` and `sideboard` default to `[]` when absent or falsey.
- Non-list board sections are skipped.
- Non-dict cards are skipped.
- Each dict card in `mainboard` or `sideboard` emits one Deck Snapshot row.

### Accepted Collection Payload Shape

Accepted top-level shape:

```python
{
    "generated_at": "2026-05-06T04:14:48+00:00",
    "collection_available": True,
    "inventory_available": True,
    "owned_unique_cards": 100,
    "owned_total_card_copies": 250,
    "owned_by_rarity": {"rare": 30},
    "inventory": {
        "gold": 1250,
        "gems": 400,
        "wildcards": {
            "common": 10,
            "uncommon": 8,
            "rare": 2,
            "mythic": 1,
        },
    },
    "active_deck_missing_by_rarity": {"rare": 1},
    "active_deck_completion": {"completion_rate": 0.94},
    "wanted_cards": [],
}
```

Observed current behavior:

- One Collection Snapshot row is built when the payload is truthy.
- Missing or falsey `inventory` defaults to `{}`.
- Missing or falsey `active_deck_completion` defaults to `{}`.
- `owned_by_rarity`, `active_deck_missing_by_rarity`, and `wanted_cards`
  preserve their payload values or default to `{}` / `[]`.

Accepted shape limit:

- Truthy `inventory` and `active_deck_completion` values are expected to be
  dict-like. Handling truthy non-dict values in those slots is not currently
  defined by tests and should not be broadened without explicit loopback.

### Accepted Parser Status Payload Shape

Accepted top-level shape:

```python
{
    "updated_at": "2026-05-06T04:14:48+00:00",
    "status": "running",
    "current_match_id": "match-1",
    "current_game_number": 1,
    "current_player_team": 1,
    "last_event_kind": "GameState",
    "last_event_at": "2026-05-06T00:14:48+00:00",
    "webhook_successes": 3,
    "webhook_failures": 0,
    "event_failures": 0,
    "router_failures": 0,
    "active_deck_signature": "deck-signature-1",
    "active_deck_name": "Azban Midrange",
    "active_match_action_count": 1,
}
```

Observed current behavior:

- One Parser Status row is built when the payload is truthy.
- String-like fields are converted to stripped strings.
- Count-like fields are normalized with `_safe_int()`.

### Accepted Card Performance Payload Shape

Accepted top-level shape:

```python
{
    "generated_at": "2026-05-06T04:14:48+00:00",
    "cards": [
        {
            "card_key": "Duress|123",
            "grp_id": 123,
            "card_name": "Duress",
            "display_name": "Duress",
            "resolution_status": "resolved",
            "layout": "normal",
            "card_faces": [],
            "games_seen": 10,
            "seen_in_game_games": 5,
            "seen_in_game_win_rate": 0.6,
            "opening_hand_games": 2,
            "opening_hand_win_rate": 0.5,
            "cast_games": 4,
            "cast_win_rate": 0.75,
            "postboard_cast_games": 1,
            "postboard_cast_win_rate": 1.0,
            "mulliganed_away_games": 1,
            "mulligan_tax": -0.1,
            "top_matchups": [],
            "top_packages": [],
        }
    ],
}
```

Observed current behavior:

- `generated_at` is converted to a stripped string.
- `cards` defaults to `[]` when absent or falsey.
- Non-dict card entries are skipped.
- Each dict card entry emits one Card Performance row.
- `card_faces`, `top_matchups`, and `top_packages` are converted with
  `list(value or [])`.

Compatibility note:

- The runtime row and Apps Script field currently use `mulligan_tax`. Do not
  rename this field or substitute another card-performance producer field
  without a schema and Apps Script migration contract.

## Outputs

Every emitted row is a `dict[str, Any]` with runtime metadata plus
family-specific snake_case fields.

### Runtime Metadata

`_base_runtime_row(event_family, **fields)` prepends metadata from
`runtime_sheet_spec(event_family)`:

| Family constant | `event_family` | `event_type` | `scope` |
| --- | --- | --- | --- |
| `ACTION_LOG_FAMILY` | `ActionLogRow` | `action_log_row` | `Match` |
| `DECK_SNAPSHOT_FAMILY` | `DeckSnapshotRow` | `deck_snapshot_row` | `Deck` |
| `COLLECTION_SNAPSHOT_FAMILY` | `CollectionSnapshotRow` | `collection_snapshot_row` | `Collection` |
| `PARSER_STATUS_FAMILY` | `ParserStatusRow` | `parser_status_row` | `Runtime` |
| `CARD_PERFORMANCE_FAMILY` | `CardPerformanceRow` | `card_performance_row` | `Card` |

Required guarantee:

- These metadata values must come from `sheet_schema.py`; `sheet_exports.py`
  must not duplicate schema truth.
- Unknown event families currently raise `KeyError` through
  `runtime_sheet_spec()`. Do not silently coerce unknown families in this
  module without a schema contract loopback.

### Action Log Row

Fields consumed by Apps Script:

- `generated_at`
- `match_id`
- `game_number`
- `turn_number`
- `timestamp`
- `action_type`
- `cast_mode`
- `grp_id`
- `card_name`
- `display_name`
- `resolution_status`
- `actor_relation`
- `from_zone_type`
- `to_zone_type`
- `summary`

Apps Script compatibility:

- `Code.gs` maps these snake_case fields to Action Log workbook headers.
- The Apps Script upsert key uses workbook-visible values corresponding to:
  - `match_id`
  - `game_number`
  - `timestamp`
  - `action_type`
  - `grp_id`
  - `from_zone_type`
  - `to_zone_type`

### Deck Snapshot Row

Fields consumed by Apps Script:

- `generated_at`
- `submitted_at`
- `match_id`
- `deck_signature`
- `deck_name`
- `deck_match_mode`
- `deck_format`
- `section`
- `arena_id`
- `count`
- `card_name`
- `rarity`
- `set`
- `type_line`
- `colors`
- `owned_copies`
- `missing_copies`

Apps Script compatibility:

- `Code.gs` maps these snake_case fields to Deck Snapshot workbook headers.
- The Apps Script upsert key uses workbook-visible values corresponding to:
  - `deck_signature`
  - `section`
  - `arena_id`

### Collection Snapshot Row

Fields consumed by Apps Script:

- `generated_at`
- `collection_available`
- `inventory_available`
- `owned_unique_cards`
- `owned_total_card_copies`
- `owned_by_rarity`
- `inventory_gold`
- `inventory_gems`
- `wildcards_common`
- `wildcards_uncommon`
- `wildcards_rare`
- `wildcards_mythic`
- `active_deck_missing_by_rarity`
- `active_deck_completion_rate`
- `wanted_cards`

Apps Script compatibility:

- `Code.gs` maps these snake_case fields to Collection Snapshot workbook
  headers.
- The Apps Script upsert key uses workbook-visible `generated_at`.

### Parser Status Row

Fields consumed by Apps Script:

- `updated_at`
- `status`
- `current_match_id`
- `current_game_number`
- `current_player_team`
- `last_event_kind`
- `last_event_at`
- `webhook_successes`
- `webhook_failures`
- `event_failures`
- `router_failures`
- `active_deck_signature`
- `active_deck_name`
- `active_match_action_count`

Apps Script compatibility:

- `Code.gs` maps these snake_case fields to Parser Status workbook headers.
- The Apps Script upsert key uses workbook-visible `updated_at`.

### Card Performance Row

Fields consumed by Apps Script:

- `generated_at`
- `card_key`
- `grp_id`
- `card_name`
- `display_name`
- `resolution_status`
- `layout`
- `card_faces`
- `games_seen`
- `seen_in_game_games`
- `seen_in_game_win_rate`
- `opening_hand_games`
- `opening_hand_win_rate`
- `cast_games`
- `cast_win_rate`
- `postboard_cast_games`
- `postboard_cast_win_rate`
- `mulliganed_away_games`
- `mulligan_tax`
- `top_matchups`
- `top_packages`

Apps Script compatibility:

- `Code.gs` maps these snake_case fields to Card Performance workbook headers.
- The Apps Script upsert key uses workbook-visible values corresponding to:
  - `generated_at`
  - `card_key`

## Normalization Rules

### String Fields

Observed current behavior:

- String-like row fields are usually built with `str(value).strip()`.
- Missing string fields usually become `""`.
- Existing non-string scalar values in string slots are stringified rather than
  rejected.

Required guarantee:

- This module may normalize row-value representation, but it must not interpret
  parser facts. For example, it may stringify an action `summary`; it must not
  reinterpret the action into a different action type.

### Integer Fields

`_safe_int(value)` observes these rules:

- `bool` values return `""`.
- Values accepted by `int(value)` return the resulting integer.
- `TypeError` and `ValueError` return `""`.
- Float values accepted by `int()` are truncated by Python's normal `int()`
  behavior.
- Numeric strings accepted by `int()` are converted.

Required guarantee:

- Boolean values must not leak into workbook integer columns as `0` or `1`.
- Unknown or unparseable numeric values must become blank strings, not guessed
  numbers.

Unknown:

- Overflow-like values that raise exceptions other than `TypeError` or
  `ValueError` are not covered by current focused tests.

### List and Object Fields

Observed current behavior:

- Some structured fields are preserved as dicts or lists for Apps Script to
  stringify or render:
  - `owned_by_rarity`
  - `active_deck_missing_by_rarity`
  - `wanted_cards`
  - `colors`
  - `card_faces`
  - `top_matchups`
  - `top_packages`
- `colors`, `card_faces`, `top_matchups`, and `top_packages` are converted with
  `list(value or [])`.

Required guarantee:

- Structured payload fields must remain raw workbook-facing values and must
  not be flattened, summarized, or schema-migrated in `sheet_exports.py`
  without a separate contract.

## Duplicate Suppression

### Action Rows

`_action_row_key(row)` builds an in-memory action key by joining these row
values with `||`:

- `match_id`
- `game_number`
- `timestamp`
- `action_type`
- `grp_id`
- `from_zone_type`
- `to_zone_type`

Observed current behavior:

- A row whose key is already in `EXPORT_STATE.posted_action_keys` is suppressed.
- A new key is added to `posted_action_keys` before the row is returned.
- `generated_at`, `turn_number`, `cast_mode`, `card_name`, `display_name`,
  `resolution_status`, `actor_relation`, and `summary` do not affect this
  export dedupe key.
- The key is used only inside the current Python process and reset state.
- The current `not key.strip()` check does not suppress a row whose joined key
  contains only separators from blank key fields.

Required guarantee:

- In-memory action dedupe must remain parser-local export behavior. Do not move
  this key into workbook formulas, Apps Script, output transport, or AI
  interpretation.
- Changing the key fields is a behavior change and must be justified by a
  contract update because it affects which action rows can be emitted.

Suspected gap:

- The all-blank action-key behavior is probably not useful, but changing it
  would alter export behavior. Route that through a Thinker or contract
  loopback before a fixer implements it.

### Snapshot Rows

Deck Snapshot, Collection Snapshot, Parser Status, and Card Performance use
stable fingerprints for in-memory repeated-export suppression.

Fingerprint behavior:

- `_stable_fingerprint(value)` serializes with
  `json.dumps(sort_keys=True, ensure_ascii=False, default=str)` and hashes the
  result with SHA-1.
- `_without_keys()` removes only top-level transient keys.
- `_rows_fingerprint()` fingerprints an ordered list of row dicts after
  top-level transient-key removal.
- `_row_fingerprint()` fingerprints a single row dict after top-level
  transient-key removal.
- The original row or row list is returned when the fingerprint changes. The
  helpers do not deep-copy rows.

Transient keys by family:

| Family | Transient keys ignored for export fingerprint |
| --- | --- |
| Deck Snapshot | `generated_at` |
| Collection Snapshot | `generated_at` |
| Parser Status | `updated_at`, `last_event_at`, `webhook_successes`, `webhook_failures`, `active_match_action_count` |
| Card Performance | `generated_at` |

Observed current behavior:

- Empty row lists and empty row dicts emit no rows and do not update the saved
  fingerprint.
- A changed non-transient value emits the family rows and stores the new
  fingerprint.
- Repeated payloads that differ only by transient keys are suppressed.
- List order affects row fingerprints. Reordering equivalent deck or card rows
  can emit rows again.

Required guarantee:

- Snapshot duplicate suppression is process-local export behavior. It must not
  be treated as workbook truth, final reconciliation truth, or durable
  cross-process deduplication.
- Transient-key changes listed above must not cause repeated snapshot exports.
- Non-transient payload changes must remain eligible for re-export.

## Malformed and Missing Input Behavior

Observed current behavior:

- Missing JSON artifacts loaded by `_load_json_dict()` degrade to `{}` and emit
  no rows for that family.
- Invalid JSON and non-dict top-level JSON loaded by `_load_json_dict()` degrade
  to `{}` and emit no rows for that family.
- Missing optional scalar fields usually degrade to `""`.
- Missing optional numeric fields usually degrade to `""`.
- Missing optional list sections usually degrade to `[]`.
- Non-dict entries in action, deck-card, and card-performance lists are skipped.

Accepted behavior boundary:

- Top-level payload overrides supplied directly to `collect_runtime_sheet_rows`
  are expected to be dict-like when not `None`.
- Truthy non-dict nested values in some slots are not uniformly defended
  against by current code or focused tests.

Required guarantee:

- Module work may add tests that document current accepted shapes and graceful
  degradation inside those shapes.
- Module work must not silently broaden accepted malformed shapes if that
  changes emitted row behavior, suppresses rows that currently emit, or hides
  errors from upstream producers without a contract update.

## Side Effects

Allowed side effects:

- Read runtime artifacts through the configured sources listed in this
  contract.
- Update in-memory `EXPORT_STATE`.
- Update in-memory `_JSON_DICT_CACHE`.

Forbidden side effects:

- Do not post webhooks.
- Do not write workbook exports.
- Do not mutate workbook schema constants.
- Do not edit Apps Script mappings.
- Do not write parser state final reconciliation.
- Do not write runtime status files.
- Do not write failed posts or failed events.
- Do not write raw logs or generated parser data.
- Do not stage, commit, open PRs, or update tracker issues from a contract
  writer pass.

## Downstream Consumers

Primary downstream runtime consumer:

- `analytics_sidecar.py` calls `collect_runtime_sheet_rows()` with export flags
  derived from parser events and sends returned rows to
  `submit_row_to_google_sheets()`.

Primary downstream transport consumer:

- `outputs.py` accepts the returned row dicts for webhook delivery and local
  output mechanics. It must not reinterpret runtime row truth.

Primary downstream Apps Script consumer:

- `tools/google_apps_script/Code.gs` maps the snake_case fields to workbook
  headers and performs workbook upserts.

Compatibility expectation:

- `sheet_exports.py` must preserve the snake_case field names currently
  consumed by Apps Script.
- Workbook-visible header strings and header order remain owned by
  `sheet_schema.py` and Apps Script, not by this module.

## Protected Surfaces

Sheet export work must not change:

- parser behavior outside runtime export row construction
- parser state final reconciliation
- workbook schema constants
- webhook payload shape
- Apps Script behavior or mappings
- parser event classes
- match identity
- game identity
- deduplication outside this module's in-memory runtime export suppression
- secrets or environment variables
- raw logs
- generated data
- runtime status files
- failed posts
- workbook exports

Schema constants and Apps Script mappings may change only through an explicit
schema migration contract loopback.

## Required Guarantees

- `collect_runtime_sheet_rows()` remains the public API for runtime sheet row
  collection.
- Family flags gate both default artifact loading and row emission.
- Runtime row metadata is sourced from `sheet_schema.runtime_sheet_spec()`.
- Runtime row field names remain Apps Script-compatible snake_case names.
- `_safe_int()` treats booleans as unknown, not numeric values.
- Missing, invalid, or non-dict JSON loaded from disk by `_load_json_dict()`
  degrades to `{}`.
- Duplicate suppression remains in-memory and process-local.
- Snapshot fingerprints ignore only the documented top-level transient keys.
- The module never posts rows or writes runtime/workbook artifacts.

## Observed Current Behavior

- The module already builds all five runtime families.
- Current focused tests cover:
  - boolean handling in `_safe_int()`
  - one-pass emission for all runtime families
  - suppression of repeated action and snapshot rows
  - parser-status suppression when only selected transient fields change
  - parser-status re-export when core context changes
  - deck snapshot suppression when only `generated_at` changes
- Current tests do not exhaustively cover malformed direct payload overrides,
  cache behavior, collection/card-performance fingerprinting, every row field,
  or Apps Script field-map compatibility.

## Suspected Gaps

These are not authorized behavior changes in this contract writer pass:

- All-blank action keys are not currently suppressed because the joined key
  still contains separators.
- Some truthy non-dict nested payload fields can reach `.get()` or iterable
  conversion paths that are not explicitly tested.
- `_safe_int()` does not document every exception class that can arise from
  unusual numeric-like values.
- `_load_json_dict()` relies on mtime-keyed cache invalidation and does not
  detect same-mtime content changes.
- There is no focused test asserting every Apps Script snake_case field remains
  present for each emitted family.

Any change to these behaviors should be routed through a Thinker/problem
representation or contract loopback if the change would alter emitted rows,
accepted inputs, workbook-visible results, or compatibility boundaries.

## Dependency Order

For future implementation work:

1. Read this contract and `docs/contracts/parser_sheet_schema.md`.
2. Compare `sheet_exports.py` and `tests/test_sheet_exports.py` against this
   contract.
3. Add focused tests for contract guarantees that are currently uncovered.
4. Make only the smallest parser-local changes required by an explicit contract
   guarantee.
5. If a desired fix would change workbook schema, Apps Script mapping, output
   transport, parser truth, or accepted malformed-input behavior, stop and
   route back to contract/problem representation.

## Compatibility

- Runtime family names, event types, and scopes are schema-owned compatibility
  values.
- Runtime row snake_case field names are Apps Script compatibility values.
- `mulligan_tax` is the current Card Performance row field consumed by Apps
  Script.
- Action Log export dedupe key fields are runtime behavior compatibility
  values.
- Snapshot transient-key sets are runtime behavior compatibility values.
- JSON artifact path ownership remains outside this module.

## Tests Required

Documentation-only validation for this contract:

```bash
git diff --check -- docs/contracts/parser_sheet_exports.md
python -m pytest -q tests/test_sheet_exports.py
```

Focused implementation tests expected for Codex C or Codex D:

- `reset_sheet_export_state()` clears all fingerprints, posted action keys, and
  JSON cache state.
- `_load_json_dict()` handles missing files, invalid JSON, non-dict JSON, cache
  reuse for unchanged mtimes, and cache refresh for changed mtimes.
- `_safe_int()` converts valid ints/numeric strings, blanks invalid values, and
  blanks booleans.
- `collect_runtime_sheet_rows()` honors every export flag without loading or
  emitting the disabled family.
- Every emitted family includes `event_family`, `event_type`, and `scope`
  sourced from `sheet_schema.py`.
- Each row family emits the snake_case fields consumed by Apps Script.
- Action row dedupe uses the documented key fields and ignores documented
  non-key fields.
- Snapshot row dedupe ignores only documented transient keys and re-emits on
  non-transient changes.
- Non-dict entries in accepted list sections are skipped.
- Missing/invalid file-loaded payloads emit no rows without crashing.

Suggested commands for implementation validation:

```bash
python -m pytest -q tests/test_sheet_exports.py tests/test_analytics_sidecar.py
python -m ruff check src tests
```

Broader validation may include `tests/test_runner.py`, `tests/test_app_outputs.py`,
and Apps Script-oriented checks only if implementation touches adjacent
integration behavior. Schema or Apps Script changes are out of scope unless a
new contract explicitly authorizes them.

## Acceptance Criteria

- The contract names `sheet_exports.py`, `tests/test_sheet_exports.py`, and this
  document as the owned artifacts.
- The contract keeps schema constants and Apps Script mappings outside this
  module's authority.
- The contract defines public APIs, helper behavior, accepted payload shapes,
  row outputs, normalization, duplicate suppression, malformed-input behavior,
  protected surfaces, and test obligations.
- The contract separates observed current behavior from future behavior-change
  candidates.
- No parser behavior, workbook schema, webhook payload shape, Apps Script
  behavior, parser state final reconciliation, match/game identity,
  deduplication outside this module, secrets, raw logs, generated data,
  runtime status files, failed posts, or workbook exports are changed by this
  contract writer pass.

## Next Workflow Action

Next recommended role: Codex C: Module Implementer.

Codex C should compare the current implementation and tests against this
contract, add focused tests for uncovered guarantees, and make only the
smallest parser-local code changes required by the contract. If implementation
would change protected surfaces or broaden accepted malformed-input behavior,
Codex C should stop and route back to a Thinker/problem-representation pass.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer for issue #52 and docs/contracts/parser_sheet_exports.md.

Goal:
Compare the current sheet exports implementation and focused tests against the parser sheet exports module contract. Implement only the smallest coherent code and test changes needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/52
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/parser_sheet_exports.md
- docs/contracts/parser_sheet_schema.md
- docs/contracts/parser_outputs.md
- src/mythic_edge_parser/app/sheet_exports.py
- tests/test_sheet_exports.py
- src/mythic_edge_parser/app/analytics_sidecar.py
- tests/test_analytics_sidecar.py
- tools/google_apps_script/Code.gs

Do:
- Compare observed code behavior against the contract before editing.
- Preserve parser-owned truth boundaries and schema/App Script ownership boundaries.
- Add focused tests for contracted sheet export behavior not currently covered.
- Keep behavior changes minimal and parser-local unless the contract explicitly requires a downstream update.
- Produce docs/implementation_handoffs/parser_sheet_exports_comparison.md with the comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Change parser behavior outside sheet export contract requirements.
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match identity, game identity, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Change schema constants or Apps Script mappings unless a contract loopback explicitly authorizes a schema migration.
- Move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, output transport, or AI-generated interpretation.
- Target main; module PR work belongs on codex/parser-module-audit-suite.
- Stage or commit unless explicitly asked.

If a desired fix would alter protected surfaces, broaden accepted malformed-input behavior, or change workbook-visible row compatibility, stop and route back to Codex A or Codex B for problem framing or contract update.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/52"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/5"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_sheet_exports.md"
  target_artifact: "docs/implementation_handoffs/parser_sheet_exports_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check -- docs/contracts/parser_sheet_exports.md"
    - "python -m pytest -q tests/test_sheet_exports.py"
  stop_conditions:
    - "Do not change parser behavior outside sheet export contract requirements."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match identity, game identity, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not change schema constants or Apps Script mappings unless a contract loopback explicitly authorizes a schema migration."
    - "Do not move parser-owned truth into workbook formulas, dashboard logic, Apps Script, webhook delivery, output transport, or AI-generated interpretation."
    - "Do not target main for module PR work."
    - "Do not mark tracker #5 complete."
```
