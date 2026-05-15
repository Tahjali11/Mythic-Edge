# Code Hardening Parser Event Schema Snapshot Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/60

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch target: `codex/code-hardening-suite`

Previous hardening context:

- Issue #58 / PR #59 added deterministic property/fuzz-style hardening tests
  for `src/mythic_edge_parser/parsers/api_common.py`.
- PR #59 merged into `codex/code-hardening-suite` at
  `3d9cee0772d24c5b04631c00ebd4a8834b8a640f`.
- Hypothesis was not added.
- Tracker #33 remains open.

Agent docs:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/problem_representation.md`
- `docs/templates/problem_representation.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Current hardening contracts read:

- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/contracts/code_hardening_pyright_advisory.md`
- `docs/contracts/code_hardening_api_common_property_fuzz_tests.md`
- `docs/contracts/parser_api_common.md`

Parser audit contracts read from `origin/main` because they are not currently
present on `codex/code-hardening-suite`:

- `docs/contracts/parser_models.md`
- `docs/contracts/parser_state.md`
- `docs/contracts/parser_outputs.md`
- `docs/contracts/parser_sheet_schema.md`
- `docs/contracts/parser_sheet_exports.md`

This contract defines a test-only hardening rollout for parser event schema and
workbook-facing row-key snapshot tests. It does not implement tests, add
snapshot files, change parser behavior, open a PR, target `main`, or mark
tracker #33 complete.

## Module

Parser event schema snapshot tests.

Target future implementation surface:

- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/`, or an equivalent stable fixture folder
  chosen by Codex C under this contract

Plain English: these tests should make accidental schema drift visible. They
should not become a second parser, should not snapshot private data, and should
not redefine parser, workbook, webhook, or Apps Script behavior.

## Owning Layer

Code Hardening test infrastructure, guarding parser and workbook-facing schema
boundaries.

Truth boundary:

- MTGA `Player.log` remains the raw observable evidence source.
- Parser modules and parser state remain the truth owners for event
  interpretation.
- `src/mythic_edge_parser/events.py` defines event representation boundaries:
  event classes, `kind` values, metadata, payload copy behavior, and
  performance class labels.
- `src/mythic_edge_parser/app/models.py` owns normalized `MatchLogRow`,
  `GameLogRow`, and legacy row serialization shapes.
- `src/mythic_edge_parser/app/sheet_schema.py` owns Python-side sync fields,
  runtime family names, event types, scopes, and landing headers.
- `src/mythic_edge_parser/app/sheet_exports.py` owns runtime export row
  construction and snake_case payload keys consumed by Apps Script.
- `src/mythic_edge_parser/app/outputs.py` transports caller-provided rows and
  must not reinterpret schema.
- `tools/google_apps_script/Code.gs` is a repo-side downstream consumer and
  upsert mapper. It does not own parser truth.
- Snapshot tests are QA/provenance guardrails. They do not authorize schema
  changes, event class changes, workbook changes, webhook changes, Apps Script
  behavior changes, or parser truth movement.

## Files Owned By This Contract

- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`

Expected future implementation files owned by this contract:

- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/*.json`
- `docs/implementation_handoffs/code_hardening_parser_event_schema_snapshots_comparison.md`
- `docs/contract_test_reports/code_hardening_parser_event_schema_snapshots.md`

Related files referenced but not owned by this contract:

- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `src/mythic_edge_parser/app/sheet_exports.py`
- `src/mythic_edge_parser/app/outputs.py`
- parser modules under `src/mythic_edge_parser/parsers/`
- `src/mythic_edge_parser/app/transforms.py`
- `tools/google_apps_script/Code.gs`
- existing parser, model, schema, export, output, transform, runtime, and
  regression tests
- existing parser regression fixtures under `tests/fixtures/`

## Observed Current Branch State

Observed during this contract pass:

- Current branch is `codex/code-hardening-suite`.
- Current HEAD is `3d9cee0772d24c5b04631c00ebd4a8834b8a640f`.
- Local branch and `origin/codex/code-hardening-suite` are aligned.
- `docs/agent_rules.yml` is present on the hardening branch.
- `docs/contracts/parser_api_common.md` is present on the hardening branch.
- The parser audit contracts for models, state, outputs, sheet schema, and
  sheet exports are absent from the hardening branch but present on
  `origin/main` and `origin/codex/parser-module-audit-suite`.
- Unrelated untracked files are present:
  - `docs/project_roadmap.md`
  - `docs/python_tooling_inventory.md`

Codex C must not absorb unrelated untracked files into this module.

## Observed Event Surfaces

### Event Metadata And Base Event

`src/mythic_edge_parser/events.py` currently defines:

- `PerformanceClass` values:
  - `InteractiveDispatch`
  - `DurablePerEvent`
  - `PostGameBatch`
- `EventMetadata` dataclass fields:
  - `timestamp`
  - `raw_bytes`
  - `raw_bytes_hash`
- `EventPayload = dict[str, Any]`
- `BaseEvent` dataclass fields:
  - `metadata`
  - `payload`
  - `performance_class`
  - `kind`
- `BaseEvent.__post_init__()` shallow-copies the incoming payload mapping.
- `BaseEvent.payload_copy()` returns a shallow dict copy.

Snapshot boundary:

- Snapshot field names and class-level schema only.
- Do not snapshot actual raw bytes.
- Do not snapshot actual raw byte hashes.
- Do not snapshot actual timestamps.

### Event Classes

Observed concrete event classes, `kind` values, and performance classes:

| Class | `kind` | `performance_class` |
| --- | --- | --- |
| `GameStateEvent` | `GameState` | `InteractiveDispatch` |
| `ClientActionEvent` | `ClientAction` | `InteractiveDispatch` |
| `MatchStateEvent` | `MatchState` | `InteractiveDispatch` |
| `DraftBotEvent` | `DraftBot` | `DurablePerEvent` |
| `DraftHumanEvent` | `DraftHuman` | `DurablePerEvent` |
| `DraftCompleteEvent` | `DraftComplete` | `DurablePerEvent` |
| `EventLifecycleEvent` | `EventLifecycle` | `DurablePerEvent` |
| `SessionEvent` | `Session` | `DurablePerEvent` |
| `RankEvent` | `Rank` | `DurablePerEvent` |
| `CollectionEvent` | `Collection` | `DurablePerEvent` |
| `DeckCollectionEvent` | `DeckCollection` | `DurablePerEvent` |
| `InventoryEvent` | `Inventory` | `DurablePerEvent` |
| `GameResultEvent` | `GameResult` | `PostGameBatch` |
| `LogFileRotatedEvent` | `LogFileRotated` | `InteractiveDispatch` |
| `DetailedLoggingStatusEvent` | `DetailedLoggingStatus` | `InteractiveDispatch` |
| `MatchConnectionStateEvent` | `MatchConnectionState` | `InteractiveDispatch` |
| `TcpConnectionCloseEvent` | `TcpConnectionClose` | `InteractiveDispatch` |
| `WebSocketClosedEvent` | `WebSocketClosed` | `InteractiveDispatch` |
| `ConnectionErrorEvent` | `ConnectionError` | `InteractiveDispatch` |

Observed union:

- `GameEvent` includes all concrete event classes listed above.

Required snapshot guarantee:

- Snapshot tests should fail on event class additions, removals, renamed class
  names, changed `kind` values, changed performance classes, or a concrete
  event class missing from `GameEvent`.
- Snapshot tests must treat an event class/schema diff as a review signal, not
  as automatic approval to update snapshots.

## Observed Parser Payload Surfaces

Parser modules under `src/mythic_edge_parser/parsers/` construct top-level
event payload dictionaries. Observed payload families include:

- `ClientAction`
  - `client_ui_message`
  - `generic_client_action`
  - `mulligan_resp`
  - `select_n_resp`
  - `submit_deck_resp`
- `MatchState`
  - `match_started`
  - `match_completed`
  - `state_changed`
- `GameState`
  - `game_state_message`
  - `queued_game_state_message`
  - `connect_resp`
- `GameResult`
  - `game_result`
- connection/status events
  - `MatchConnectionState`
  - `TcpConnectionClose`
  - `WebSocketClosed`
  - `ConnectionError`
  - `DetailedLoggingStatus`
- collection/deck/inventory/rank/session/lifecycle events
  - `collection_snapshot`
  - `deck_collection_snapshot`
  - `inventory_snapshot`
  - `rank_snapshot`
  - `session_account_update`
  - `session_authenticated`
  - `session_logout`
  - `event_join`
  - `event_claim_prize`
  - `event_enter_pairing`

Known observed payload key sets from current parser builders and focused tests:

- `ClientAction.client_ui_message`
  - `type`
  - `raw_client_action`
- `ClientAction.generic_client_action`
  - `type`
  - `message_type`
  - `raw_client_action`
- `ClientAction.mulligan_resp`
  - `type`
  - `decision`
  - `game_state_id`
  - `resp_id`
  - `request_id`
  - `raw_client_action`
- `ClientAction.select_n_resp`
  - `type`
  - `selected_option_ids`
  - `selected_object_ids`
  - `game_state_id`
  - `resp_id`
  - `request_id`
  - `raw_client_action`
- `ClientAction.submit_deck_resp`
  - `type`
  - `deck_cards`
  - `sideboard_cards`
  - `game_state_id`
  - `resp_id`
  - `request_id`
  - `raw_client_action`
- `MatchState`
  - `type`
  - `state_type`
  - `match_id`
  - `event_id`
  - `players`
  - `raw_match_state`
  - optional completion keys `match_completed_reason` and `game_results`
- `GameState.game_state_message` / `GameState.queued_game_state_message`
  - `type`
  - `message_type`
  - `msg_id`
  - `game_state_id`
  - `system_seat_ids`
  - `stage`
  - `match_state`
  - `turn_number`
  - `active_player_seat_id`
  - `game_info`
  - `turn_info`
  - `identity`
  - `players`
  - `zones`
  - `game_objects`
  - `annotations`
  - `persistent_annotations`
  - `timers`
  - `actions`
  - `update`
  - `pending_message_count`
  - `prev_game_state_id`
  - `diff_deleted_instance_ids`
  - `diff_deleted_persistent_annotation_ids`
  - `raw_game_state`
- `GameState.connect_resp`
  - `type`
  - `message_type`
  - `msg_id`
  - `game_state_id`
  - `system_seat_ids`
  - `deck_cards`
  - `sideboard_cards`
  - `settings`
  - `raw_connect_resp`
- `GameResult.game_result`
  - `type`
  - `source`
  - `stage`
  - `match_state`
  - `winning_team_id`
  - `result_type`
  - `reason`
  - `results`
  - `game_info`
  - `identity`
  - `game_state_id`
  - `message_type`
- `Collection.collection_snapshot`
  - `type`
  - `player_cards`
  - `raw_start_hook`
- `DeckCollection.deck_collection_snapshot`
  - `type`
  - `decks`
  - `raw_start_hook`
- `Inventory.inventory_snapshot`
  - `type`
  - `inventory`
  - `raw_start_hook`
- `Rank.rank_snapshot`
  - `type`
  - `constructed_class`
  - `constructed_level`
  - `limited_class`
  - `limited_level`
  - `constructed_percentile`
  - `limited_percentile`
  - `raw_rank`
- `Session.session_account_update`
  - `type`
  - `display_name`
  - `account_id`
  - `raw_session`
- `Session.session_authenticated`
  - `type`
  - `display_name`
  - `account_id`
  - `screen_name`
  - `raw_session`
- `Session.session_logout`
  - `type`
  - `raw_session`
- `EventLifecycle`
  - `type`
  - `raw_event_lifecycle`
- `DetailedLoggingStatus`
  - `enabled`
- `MatchConnectionState`
  - `old`
  - `new`
- `TcpConnectionClose` / `WebSocketClosed`
  - top-level keys are preserved from parsed connection JSON and may vary by
    source line
- `ConnectionError`
  - `error_type`
  - optional `payload`
  - optional `result`
  - optional `outcome`
  - optional `attempts`

Required snapshot guarantee:

- Future snapshots should store observed top-level payload key sets grouped by
  event `kind` and stable payload discriminator when available, usually the
  payload `type` value.
- Snapshot tests may include shallow type categories for top-level keys, such
  as `str`, `int`, `list`, `dict`, `bool`, `none`, or `unknown`, only when the
  type category is stable and useful.
- Snapshot tests must not store full raw payload values or nested raw source
  objects.

## Observed Workbook-Facing Row Surfaces

### Match Log Row

`MatchSummary.to_match_log_row(final=True|False)` currently emits a
`MatchLogRow` dictionary with stable metadata:

- `event_family`: `MatchLogRow`
- `event_type`: `match_log_row`
- `scope`: `Match`

Observed key order:

```text
event_family
event_type
scope
match_id
timestamp
Date
Experiment ID
Deck Code
Opponent Archetype
Opponent Variant
My Rank
Opponent Rank
Deck Tier
G1 Play / Draw
Game 1 Result
G2 Play / Draw
Game 2 Result
G3 Play / Draw
Game 3 Result
Games Won
Games Lost
Match Win?
Valid?
General Analysis?
Primary Comparison Analysis?
Reason Tag
Pilot Error?
One-line note
Rank Group
Mythic Split
Total Games
Match Win Flag
Game Win %
Queue Bucket (Auto)
Primary Comparison (Auto)
Event Round
MTGA Match ID
MTGA Format
MTGA Event ID
MTGA Queue Type
G1 Mulligans
G2 Mulligans
G3 Mulligans
G1 Turn Count
G2 Turn Count
G3 Turn Count
MGTA Start Time
MTGA End Time
MTGA Rank Raw
MTGA Mulligans
MTGA Sideboard Entered
MTGA Submit Deck Seen
MTGA Sync Status
```

The current workbook compatibility spelling is `MGTA Start Time`. Snapshot
tests must preserve that exact spelling unless a future workbook migration
contract explicitly changes it.

### Game Log Row

`GameSummary.to_game_log_row(match)` currently emits a `GameLogRow` dictionary
with stable metadata:

- `event_family`: `GameLogRow`
- `event_type`: `game_log_row`
- `scope`: `Game`

Observed key order:

```text
event_family
event_type
scope
match_id
timestamp
Date
MTGA Format
My Rank
MTGA Match ID
Game Number
Pre / Postboard
Play / Draw
Mulligans
Opening Hand Size
Opening Hand
Mulliganed Away
Game Result
Turn Count
Game Duration
MTGA Event ID
MTGA Queue Type
```

### Legacy Rows

Legacy workbook/runtime rows still exist and may be included in snapshots if
Codex C keeps them separate from current landing rows:

- `MatchSummary.to_sheet_row()`
  - `event_family`: `MatchSummary`
  - `event_type`: `match_summary`
  - `scope`: `Match`
- `GameSummary.to_sheet_row(match)`
  - `event_family`: `GameSummary`
  - `event_type`: `game_summary`
  - `scope`: `Game`

Required snapshot guarantee:

- Current `MatchLogRow` and `GameLogRow` key sets must be snapshotted.
- Key order should be snapshotted for workbook-facing row dictionaries because
  row order is meaningful for review and diff readability, even though Apps
  Script writes by header names.
- Snapshot tests must assert `MATCH_LOG_SYNC_FIELDS` is a subset of
  `MatchLogRow` keys.
- Snapshot tests must assert `GAME_LOG_SYNC_FIELDS` is a subset of
  `GameLogRow` keys.
- Snapshot tests must keep legacy row snapshots in a named legacy section if
  included, so future retirement is an explicit migration decision rather than
  silent deletion.

## Observed Sheet Schema Surfaces

`src/mythic_edge_parser/app/sheet_schema.py` currently defines:

- ordered `MATCH_LOG_SYNC_FIELDS`
- ordered `GAME_LOG_SYNC_FIELDS`
- ordered runtime landing headers:
  - `ACTION_LOG_HEADERS`
  - `DECK_SNAPSHOT_HEADERS`
  - `COLLECTION_SNAPSHOT_HEADERS`
  - `PARSER_STATUS_HEADERS`
  - `CARD_PERFORMANCE_HEADERS`
- frozen slotted `RuntimeSheetSpec`
- runtime row family constants:
  - `ActionLogRow`
  - `DeckSnapshotRow`
  - `CollectionSnapshotRow`
  - `ParserStatusRow`
  - `CardPerformanceRow`
- `RUNTIME_SHEET_SPECS`
- `SYNC_FIELDS_BY_ROW_KIND`
- lookup helpers:
  - `runtime_sheet_spec(event_family)`
  - `runtime_sheet_headers(event_family)`
  - `sync_fields(row_kind)`

Required snapshot guarantee:

- Snapshot tests should include ordered sync-field tuples.
- Snapshot tests should include every runtime family, its `event_type`, its
  `scope`, and its ordered landing headers.
- Snapshot tests should include `SYNC_FIELDS_BY_ROW_KIND` row-kind keys.
- Unknown-family and unknown-row-kind `KeyError` behavior should stay covered
  by focused tests, not necessarily by snapshot content.

## Observed Runtime Export Row Surfaces

`src/mythic_edge_parser/app/sheet_exports.py` currently emits five runtime row
families through `collect_runtime_sheet_rows()`:

| `event_family` | `event_type` | `scope` |
| --- | --- | --- |
| `ActionLogRow` | `action_log_row` | `Match` |
| `DeckSnapshotRow` | `deck_snapshot_row` | `Deck` |
| `CollectionSnapshotRow` | `collection_snapshot_row` | `Collection` |
| `ParserStatusRow` | `parser_status_row` | `Runtime` |
| `CardPerformanceRow` | `card_performance_row` | `Card` |

Observed runtime row key sets:

- `ActionLogRow`
  - `event_family`
  - `event_type`
  - `scope`
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
- `DeckSnapshotRow`
  - `event_family`
  - `event_type`
  - `scope`
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
- `CollectionSnapshotRow`
  - `event_family`
  - `event_type`
  - `scope`
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
- `ParserStatusRow`
  - `event_family`
  - `event_type`
  - `scope`
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
- `CardPerformanceRow`
  - `event_family`
  - `event_type`
  - `scope`
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

Required snapshot guarantee:

- Snapshot tests should include runtime row metadata and row key sets.
- Snapshot tests should assert runtime row `event_family`, `event_type`, and
  `scope` come from `sheet_schema.runtime_sheet_spec()`.
- Snapshot tests must not include actual runtime export values, generated
  timestamps, counters, deck names, collection totals, card names, or local
  status paths.

## Apps Script Parity Boundaries

Safe repo-side assertions:

- Static assertions may read `tools/google_apps_script/Code.gs` from the repo.
- Static assertions may compare Python runtime landing headers with
  `WORKBOOK_SCHEMA.landingHeaders`.
- Static assertions may compare `MATCH_LOG_SYNC_FIELDS` with keys returned by
  `buildMatchLogFieldMap_(data)`.
- Static assertions may compare `GAME_LOG_SYNC_FIELDS` with keys returned by
  `buildGameLogFieldMap_(data)`.
- Static assertions may check that Apps Script dispatch handles current Python
  row families:
  - `MatchLogRow`
  - `GameLogRow`
  - `ActionLogRow`
  - `DeckSnapshotRow`
  - `CollectionSnapshotRow`
  - `ParserStatusRow`
  - `CardPerformanceRow`
  - legacy `MatchSummary`
- Static assertions may compare runtime build-object output headers with
  `sheet_schema.py` header tuples.
- Static assertions may compare Apps Script snake_case data keys with
  `sheet_exports.py` runtime row keys.

Unsafe assertions:

- Do not assert live workbook state.
- Do not assert deployed Apps Script state.
- Do not call Apps Script.
- Do not snapshot `spreadsheetId`, `deploymentTag`, webhook URLs, secrets, or
  environment values.
- Do not rewrite `Code.gs` during this issue.
- Do not treat Apps Script fallback aliases as parser truth.

Required boundary wording:

- Repo-side Apps Script parity tests prove only that committed Python and
  committed Apps Script source agree. They do not prove the live workbook or
  deployed Apps Script matches the repo.

## Snapshot Content Policy

Allowed snapshot content:

- stable schema snapshot version, for example `schema_snapshot_version: 1`
- event class names
- event `kind` values
- event `performance_class` values
- `PerformanceClass` value list
- dataclass field names for `EventMetadata`, `BaseEvent`, and
  `RuntimeSheetSpec`
- `GameEvent` union membership by concrete class name
- parser payload top-level key sets grouped by event kind and payload type
- optional shallow type categories for stable top-level payload keys
- stable payload discriminator values such as `type`
- workbook row key order for `MatchLogRow` and `GameLogRow`
- stable row metadata values:
  - `event_family`
  - `event_type`
  - `scope`
- ordered sync-field tuples
- runtime family names, event types, scopes, and ordered header tuples
- runtime export row key sets
- repo-side Apps Script dispatch family names and static field-map/header keys

Forbidden or volatile snapshot content:

- actual raw log lines
- `EventMetadata.raw_bytes`
- actual `raw_bytes_hash` values
- timestamps, `generated_at`, `updated_at`, `last_event_at`, or current dates
- local absolute paths
- runtime status file contents
- failed-post contents
- webhook URLs
- API keys, tokens, credentials, environment variable values, or secrets
- workbook exports
- raw workbook IDs, spreadsheet IDs, deployment tags, or live workbook state
- generated card data, generated tier data, or local cache contents
- full nested raw source payloads under keys such as:
  - `raw_client_action`
  - `raw_match_state`
  - `raw_game_state`
  - `raw_connect_resp`
  - `raw_start_hook`
  - `raw_rank`
  - `raw_session`
  - `raw_event_lifecycle`
- values from parser regression fixture rows unless the value is itself a
  stable schema value such as `event_family`, `event_type`, `scope`, or a key
  name

## Snapshot Storage Policy

Preferred storage folder:

```text
tests/fixtures/schema_snapshots/
```

Preferred first snapshot files:

- `parser_event_classes.json`
- `parser_payload_keys.json`
- `workbook_row_keys.json`
- `sheet_schema_surfaces.json`
- `runtime_export_row_keys.json`
- `apps_script_repo_parity.json`

Codex C may combine these into fewer files if that makes review clearer, but
it must keep sections named so reviewers can tell which surface changed.

Required JSON formatting:

- UTF-8 text.
- Two-space indentation.
- Trailing newline.
- Deterministic key order.
- Lists sorted only when order is not contract meaningful.
- Preserve list order when order is contract meaningful:
  - workbook row keys
  - sync fields
  - runtime headers
  - event class table order if derived from `events.py`

Generated update behavior:

- Tests should compare current generated schema data to committed JSON
  snapshots.
- If a helper can update snapshots, it must be opt-in only.
- Recommended opt-in guard:

```powershell
$env:MYTHIC_EDGE_UPDATE_SCHEMA_SNAPSHOTS = "1"
py -m pytest -q tests\test_event_schema_snapshots.py
Remove-Item Env:\MYTHIC_EDGE_UPDATE_SCHEMA_SNAPSHOTS
```

- Snapshot update mode must never be the default.
- Snapshot tests should fail with a message that tells future agents not to
  auto-update snapshots without issue/contract approval.
- Snapshot update mode must not read raw logs, local runtime files, failed
  posts, workbook exports, generated card data, secrets, or live workbook
  state.

## Snapshot Update Approval Rule

Snapshot updates require explicit approval.

A snapshot diff may be approved only when all are true:

- A GitHub issue or contract authorizes the schema/event/row surface drift.
- The PR drift budget names the drift as `Authorized drift` or records
  accepted residual drift with a follow-up.
- Codex E review or contract-test report confirms the snapshot diff is
  intentional.
- Protected-surface gate output is recorded and any warnings are explicitly
  cited.
- The update does not include forbidden volatile content.

Not enough for approval:

- "Tests pass."
- "Snapshot changed after refactor."
- "AI/codegen updated it."
- "The update command produced this diff."
- "Workbook accepted the payload."

If a snapshot diff shows a changed event class, changed `kind`, changed row
key, changed sync field, changed runtime family, changed Apps Script field map,
or changed snake_case payload key without explicit authorization, Codex C/E/F/G
must stop and route back to Codex B or Codex A rather than update the snapshot.

## Existing Coverage

Observed focused coverage:

- `tests/test_events.py`
  - covers `EventMetadata.empty()`
  - covers event payload shallow-copy behavior
  - does not inventory every event class, kind, performance class, or union
    member
- parser-specific tests
  - cover many concrete payload values and malformed inputs for client
    actions, collection, connection, GRE connect response, GRE game state,
    GRE game result, GRE turn info, match state, rank, inventory, session, and
    lifecycle parsing
  - do not provide one global parser payload key inventory
- `tests/test_app_models.py`
  - covers representative `MatchSummary`, `MatchLogRow`, `GameLogRow`, live
    rows, opening-hand serialization, and some queue/rank behavior
  - does not snapshot full row key order or every row serializer key set in one
    schema artifact
- `tests/test_sheet_schema.py`
  - currently covers Action Log runtime spec and `sync_fields("game_log")`
  - does not snapshot every runtime family, sync tuple, row-kind key, or Apps
    Script parity surface
- `tests/test_sheet_exports.py`
  - covers all runtime families emit at least once and some duplicate
    suppression behavior
  - does not snapshot every runtime row key set or Apps Script snake_case
    mapping
- `tests/test_app_outputs.py`
  - covers webhook transport and dispatcher behavior around existing row
    metadata
  - does not own schema interpretation
- `tests/test_transforms.py`
  - covers event-to-row transformation slices for event family/type/scope
  - does not own parser event class or workbook schema snapshots
- `tests/test_parser_regressions.py`
  - compares full expected snapshots for two sanitized parser regression
    slices
  - already captures many event traces and row values, but it is fixture/value
    oriented rather than a small schema inventory

## Suspected Gaps

- No single focused test inventories every concrete event class, `kind`,
  performance class, and `GameEvent` union member.
- No single focused test inventories parser payload key sets by event kind and
  payload type.
- No focused schema snapshot locks `MatchLogRow` and `GameLogRow` key order.
- No focused schema snapshot locks runtime export row key sets for all five
  runtime families.
- Current schema tests do not appear to lock every runtime family spec,
  event type, scope, and ordered header tuple.
- Current Apps Script parity tests are not comprehensive for runtime
  snake_case data keys and runtime landing headers.
- Existing regression fixtures are useful but too value-heavy to be the only
  schema drift guardrail.
- There is no explicit test failure message telling future Codex threads not
  to auto-update snapshots without approval.
- Parser audit contracts for models/state/outputs/sheet schema/sheet exports
  are not currently present on the hardening branch, so Codex C should keep
  referencing `origin/main` or sync explicitly if implementation needs those
  contracts locally.

## Required Guarantees

### Parser Event Schema Snapshots

Snapshot tests must guarantee:

- Every concrete event class in `events.py` has the expected class name,
  `kind`, and `performance_class`.
- Every concrete event class appears in `GameEvent`.
- `EventMetadata`, `BaseEvent`, and `RuntimeSheetSpec` field names remain
  stable.
- `BaseEvent` payload shallow-copy behavior remains covered by focused tests.
- Parser payload key snapshots are grouped clearly by event kind and payload
  type or other stable discriminator.
- Parser payload snapshots exclude raw nested source payload values.
- Parser payload snapshots do not create new parser semantics.

### Workbook-Facing Row Key Snapshots

Snapshot tests must guarantee:

- `MatchLogRow` row keys stay stable and ordered.
- `GameLogRow` row keys stay stable and ordered.
- Stable row metadata values stay stable:
  - `MatchLogRow` / `match_log_row` / `Match`
  - `GameLogRow` / `game_log_row` / `Game`
- `MATCH_LOG_SYNC_FIELDS` remains a subset of `MatchLogRow` keys.
- `GAME_LOG_SYNC_FIELDS` remains a subset of `GameLogRow` keys.
- `"MGTA Start Time"` remains present until a workbook migration contract
  changes it.
- Legacy row snapshots, if included, are separated from current workbook
  landing row snapshots.

### Runtime Export Row Key Snapshots

Snapshot tests must guarantee:

- Each runtime export family has the expected `event_family`, `event_type`,
  `scope`, and row key set.
- Runtime export metadata comes from `sheet_schema.py`, not duplicated test
  constants.
- Runtime export row key snapshots align with Apps Script build-object
  snake_case consumers.
- Transient runtime values are excluded.

### Sheet Schema Snapshots

Snapshot tests must guarantee:

- Ordered match/game sync fields stay stable.
- Runtime sheet specs stay stable for all runtime families.
- Runtime landing headers stay stable and ordered.
- `SYNC_FIELDS_BY_ROW_KIND` row-kind names stay stable.
- Unknown-key fail-fast behavior remains covered by ordinary focused tests.

### Apps Script Repo Parity Snapshots

Snapshot tests must guarantee from committed repo code only:

- Apps Script dispatch recognizes Python-emitted row families.
- Apps Script Match Log field-map keys match Python match sync fields.
- Apps Script Game Log field-map keys match Python game sync fields.
- Apps Script runtime landing headers match Python runtime header tuples by
  exact order.
- Apps Script runtime build-object functions consume snake_case keys emitted
  by `sheet_exports.py`.

Snapshot tests must explicitly state that they do not verify live workbook or
deployed Apps Script state.

## Out Of Scope

This issue does not authorize:

- parser behavior changes
- parser state final reconciliation changes
- parser event class changes
- event `kind` changes
- parser payload shape changes
- workbook schema changes
- webhook payload shape changes
- Apps Script behavior changes
- match identity changes
- game identity changes
- deduplication changes
- output transport changes
- runtime status file schema changes
- failed-post schema changes
- local raw log fixture creation from private logs
- generated card/tier data changes
- workbook export changes
- changing dependency/tooling strategy
- opening or merging a PR
- targeting `main`
- marking tracker #33 complete

If a snapshot test exposes a real behavior/schema mismatch, Codex C must stop
and route to the correct workflow role instead of fixing behavior in this
issue.

## Protected Surfaces

Do not change under this issue:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- event `kind` values
- parser payload shapes
- match identity
- game identity
- deduplication
- sync field names
- runtime family names
- runtime `event_type` values
- runtime `scope` values
- secrets
- environment variables
- raw logs
- generated data
- runtime status files
- failed posts
- workbook exports

Allowed hardening surfaces:

- this contract
- future focused snapshot tests
- future committed schema snapshot fixtures that contain only allowed stable
  schema content
- future implementation handoff and contract-test report artifacts

## Error Behavior

Expected snapshot-test behavior:

- Missing snapshot files should fail with a clear message unless update mode is
  explicitly enabled.
- Snapshot content mismatch should fail with a clear path and section name.
- Volatile or forbidden snapshot content should fail the focused snapshot test
  if Codex C can implement a simple guard without overbuilding.
- Parser behavior mismatch discovered by snapshots must be reported, not
  silently fixed.
- Snapshot update mode must be opt-in and must not run in CI by default.

Expected implementation behavior:

- Tests should be deterministic from a clean clone.
- Tests should not require network access.
- Tests should not require local raw logs, local runtime files, failed posts,
  workbook exports, generated card data, secrets, or live workbook access.
- Tests should not depend on the current date or absolute local paths.

## Validation Requirements

Contract-writer validation:

```powershell
git diff --check
```

Focused implementation validation:

```powershell
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_events.py tests\test_app_models.py tests\test_sheet_schema.py tests\test_sheet_exports.py tests\test_app_outputs.py
py -m pytest -q tests\test_client_actions_parser.py tests\test_gre_connect_resp_parser.py tests\test_gre_game_state_parser.py tests\test_gre_game_result_parser.py tests\test_match_state_parser.py tests\test_parser_small_modules.py tests\test_connection_parsers.py tests\test_collection_parser.py tests\test_parser_regressions.py
py -m ruff check src tests
git diff --check
```

Hardening validation:

```powershell
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Before Codex F submitter work:

```powershell
py -m pytest -q
py -m ruff check src tests tools
pyright --project pyrightconfig.json
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
git diff --check
```

Interpretation:

- Pyright remains advisory under issue #45 / PR #57.
- Zero Pyright findings is not required by this issue.
- Snapshot tests and related parser/schema tests should pass.
- If unrelated existing failures appear, Codex C/E must name them and avoid
  broadening the fix.

## Dependency Order

Codex C should proceed in this order:

1. Confirm branch is `codex/code-hardening-suite`.
2. Confirm current branch is at or after PR #59 merge commit `3d9cee0`.
3. Inspect unrelated untracked files and exclude them from this module.
4. Read this contract and issue #60.
5. Compare current code/tests against the contract before editing.
6. Decide exact snapshot file layout.
7. Implement test-only snapshot generation helpers in
   `tests/test_event_schema_snapshots.py`.
8. Add only stable JSON snapshot fixtures under the approved fixture folder.
9. Add explicit failure/update-policy messaging.
10. Run focused snapshot validation.
11. Run related event/parser/model/schema/export/output validation.
12. Run Ruff, diff check, and protected-surface gate.
13. Produce the implementation handoff.
14. Route to Codex E for contract-test review.

Stop and route back if satisfying this contract requires production code
changes or protected surface changes.

## Acceptance Criteria

- `docs/contracts/code_hardening_parser_event_schema_snapshots.md` exists.
- The contract defines test-only parser event/schema snapshot hardening.
- The contract distinguishes observed current surfaces from required
  guarantees.
- The contract defines parser event class snapshots.
- The contract defines parser payload key snapshots.
- The contract defines workbook-facing row key snapshots.
- The contract defines runtime export row key snapshots.
- The contract defines sheet schema snapshots.
- The contract defines repo-side Apps Script parity boundaries.
- The contract defines allowed and forbidden snapshot content.
- The contract defines stable snapshot storage and update policy.
- The contract requires explicit approval for snapshot updates.
- The contract names existing test coverage and suspected gaps.
- The contract preserves protected surfaces and forbids behavior changes.
- The contract routes next work to Codex C on `codex/code-hardening-suite`.

## Handoff Packet

Role performed: Codex B: Module Contract Writer.

Source problem representation: https://github.com/Tahjali11/Mythic-Edge/issues/60

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/33

Contract produced:
`docs/contracts/code_hardening_parser_event_schema_snapshots.md`

Risk tier: Medium for test-only hardening. Escalate to High if implementation
requires parser behavior, event class, payload shape, workbook schema, webhook
shape, Apps Script, match/game identity, deduplication, or final reconciliation
changes.

Owning truth layer: Code Hardening test infrastructure guarding parser and
workbook-facing schema boundaries.

Public interface:

- No runtime interface changes.
- Future test surface: `tests/test_event_schema_snapshots.py`.
- Future fixture surface: `tests/fixtures/schema_snapshots/*.json`.

Invariants:

- Snapshot stable schema only.
- Exclude raw, local, generated, secret, runtime, and volatile content.
- Keep snapshots deterministic and clean-clone safe.
- Snapshot updates require explicit issue/contract/review approval.
- Parser truth remains parser/state owned.
- Apps Script parity is repo-side only, not live deployment proof.
- Hardening work targets `codex/code-hardening-suite`, not `main`.

Required tests and validation: listed above.

Acceptance criteria: listed above.

Open questions or contract risks:

- Whether Codex C should split snapshots into the preferred six JSON files or
  combine related surfaces into fewer files for readability.
- Whether parser payload key snapshots should use AST-derived key inventory,
  deterministic synthetic parser calls, existing parser fixtures, or a small
  combination. The implementation must avoid raw-value snapshots either way.
- Whether legacy `MatchSummary` / `GameSummary` row snapshots should be
  included in v1 or only current `MatchLogRow` / `GameLogRow` snapshots.
- Whether Apps Script static parsing should be implemented with a small parser
  helper in the test file or with focused regex extraction. Either is allowed
  if deterministic and narrow.
- Parser audit contracts for models/state/outputs/sheet schema/sheet exports
  are still absent locally on the hardening branch; Codex C should keep
  referencing `origin/main` or route to an explicit branch-sync step if local
  contract presence becomes necessary.

Next recommended thread role: Codex C: Module Implementer / comparison thread.

Pasteable next-thread prompt:

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer / comparison thread for the Code Hardening child issue: Parser event schema snapshot tests.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/60

Branch target:
codex/code-hardening-suite

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/contracts/code_hardening_protected_surface_gate.md
- docs/contracts/code_hardening_pr_drift_budget.md
- docs/contracts/code_hardening_pyright_advisory.md
- docs/contracts/code_hardening_api_common_property_fuzz_tests.md
- parser audit contracts from origin/main or origin/codex/parser-module-audit-suite if absent locally, especially parser_models, parser_state, parser_outputs, parser_sheet_schema, and parser_sheet_exports
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/app/sheet_exports.py
- src/mythic_edge_parser/app/outputs.py
- src/mythic_edge_parser/app/transforms.py
- parser modules under src/mythic_edge_parser/parsers/
- tools/google_apps_script/Code.gs
- tests that assert event payloads, row keys, schema fields, parser regressions, and workbook-facing exports

Goal:
Compare the current code and tests against docs/contracts/code_hardening_parser_event_schema_snapshots.md. Implement only the smallest test-only schema snapshot suite needed to satisfy the contract, then produce docs/implementation_handoffs/code_hardening_parser_event_schema_snapshots_comparison.md.

Before editing:
- Confirm the branch is codex/code-hardening-suite.
- Confirm the branch is at or after PR #59 merge commit 3d9cee0.
- Inspect git status and exclude unrelated untracked files.
- State what schema snapshots are supposed to protect, what existing tests already cover, what is missing, and the exact minimal test/fixture plan.

Do:
- Add focused deterministic schema snapshot tests.
- Add only stable schema snapshot fixtures with allowed content.
- Prefer tests/test_event_schema_snapshots.py and tests/fixtures/schema_snapshots/.
- Snapshot event class names, kind values, performance classes, parser payload key sets, MatchLogRow/GameLogRow key sets, sync fields, runtime row families, runtime row key sets, and repo-side Apps Script parity surfaces as defined by the contract.
- Exclude raw bytes, raw hashes, timestamps, local paths, secrets, raw logs, generated data, runtime status, failed posts, workbook exports, workbook IDs, deployment tags, and full raw payload values.
- Add an explicit opt-in update policy if snapshot update helpers are implemented.
- Run focused and related validation.
- Produce the implementation handoff with files changed, snapshots added, update policy, validation, protected-surface status, and next recommended role.

Do not:
- Change parser behavior.
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Add snapshot files containing volatile/private/generated data.
- Auto-update snapshots without explicit issue/contract/review approval.
- Target main.
- Mark tracker #33 complete.
- Stage, commit, open a PR, or merge unless explicitly asked.

Validation:
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests\test_events.py tests\test_app_models.py tests\test_sheet_schema.py tests\test_sheet_exports.py tests\test_app_outputs.py
py -m pytest -q tests\test_client_actions_parser.py tests\test_gre_connect_resp_parser.py tests\test_gre_game_state_parser.py tests\test_gre_game_result_parser.py tests\test_match_state_parser.py tests\test_parser_small_modules.py tests\test_connection_parsers.py tests\test_collection_parser.py tests\test_parser_regressions.py
py -m ruff check src tests
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
git diff --check
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/60"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/code_hardening_parser_event_schema_snapshots.md"
  target_artifact: "docs/implementation_handoffs/code_hardening_parser_event_schema_snapshots_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not change parser behavior."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not add snapshot files containing volatile/private/generated data."
    - "Do not auto-update snapshots without explicit issue/contract/review approval."
    - "Do not absorb unrelated untracked files into this module."
    - "Do not target main; hardening work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
