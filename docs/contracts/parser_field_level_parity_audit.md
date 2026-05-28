# Parser Field-Level Parity Audit Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/121
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- related_tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- source_problem_representation: GitHub issue #121
- source_feature_equity_artifact: docs/problem_representations/parser_feature_equity_with_manasight.md
- target_artifact: docs/contracts/parser_field_level_parity_audit.md
- expected_next_artifact: docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md
- branch: codex/parser-reliability-intelligence
- risk_tier: Medium
- status: contract only

Required agent docs:

- docs/agent_constitution.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md
- docs/codex_module_workflow.md

## Purpose

Mythic Edge now has event-family feature-equity evidence and a corpus ratchet,
but event-family coverage is not enough to prove that important payload fields
are represented safely. This contract defines a field-level parity audit for
already-recognized parser surfaces that were identified by the Manasight feature
inventory.

Plain English: the audit should answer whether Mythic Edge has the fields it
needs for each covered surface, whether those fields are parser-owned normalized
facts or preserved raw evidence, and which tests or snapshots protect them.

This contract does not authorize code changes. The first implementation thread
must be a comparison thread that produces a handoff report.

## Owning Layer

Parser and state interpretation.

The parser layer owns:

- event marker recognition
- event class and `kind` selection
- stable payload `type` values where present
- parser-owned normalized payload fields
- raw-evidence preservation fields
- malformed-input degradation policy

Parser state owns live and final interpretation after events exist.

Validation tools own evidence that current behavior matches contracts. They do
not own parser truth.

The following layers are downstream consumers only:

- workbook formulas
- workbook landing sheets
- dashboards and reporting tabs
- webhook transport
- Apps Script transport/upsert code
- diagnostics and corpus reports
- AI or coaching layers

## Field-Level Parity Standard

Field-level parity means Mythic Edge can show, for an already-covered parser
surface, that it has an equivalent parser-owned representation or an explicit
raw-evidence preservation policy for the important facts in that surface.

For each audited event family, Codex C must answer:

1. Does Mythic Edge detect the relevant Player.log marker, API response, GRE
   message, or connection-state payload?
2. Does the router emit the expected Mythic Edge event class and stable `kind`
   value?
3. Does the payload have stable normalized fields for facts Mythic Edge intends
   to own?
4. Does the payload preserve raw evidence for facts that are not normalized?
5. Do tests, schema snapshots, golden replay, or the feature-equity corpus
   ratchet protect the fields?
6. Are missing fields intentionally deferred, unknown, or suspected gaps?

Parity does not mean:

- copying Manasight source code
- matching Manasight Rust internals exactly
- treating Manasight as a truth owner
- adding parser fields without a scoped follow-up issue
- moving truth downstream into workbooks, Apps Script, dashboards, or AI

## Field Role Labels

Codex C must use these labels in the comparison handoff.

| Label | Meaning |
| --- | --- |
| `parser_owned_normalized` | Stable parser payload field that downstream code may consume directly as parser-owned fact. |
| `raw_evidence_preserved` | Raw or mostly raw source payload retained for diagnostics, replay, future interpretation, or evidence-ledger mapping. |
| `raw_mixed_payload` | Parsed payload is emitted directly without a stable `raw_*` wrapper or normalized field split. |
| `derived_downstream` | Value is computed later by parser state, extractors, runtime surfaces, or analytics from parser-owned events. |
| `future_backlog` | Valuable field family, but intentionally deferred to a later module issue. |
| `not_parser_truth` | User annotation, workbook formula, dashboard classification, AI output, or other downstream interpretation. |
| `unknown` | Current repo evidence is insufficient to decide. |

## Audit Status Labels

Codex C must use these labels in the audited event-family matrix.

| Status | Meaning |
| --- | --- |
| `verified` | Field shape is defined by contract or code, protected by focused tests or snapshots, and represented in golden replay or corpus evidence where relevant. |
| `documented_partial` | Field shape is defined and locally tested, but corpus/golden coverage or raw-vs-normalized policy is incomplete. |
| `raw_preserved_only` | Raw evidence is intentionally preserved and normalized field ownership is not currently claimed. |
| `suspected_gap` | Current behavior may be insufficient, under-tested, or ambiguous. |
| `unknown` | Needed context is absent or stale. |
| `out_of_scope` | Not part of issue #121. |

## Files Owned By This Contract

- docs/contracts/parser_field_level_parity_audit.md

Expected next durable artifacts:

- docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md
- docs/contract_test_reports/parser_field_level_parity_audit.md

Files and surfaces referenced by this contract:

- docs/problem_representations/parser_feature_equity_with_manasight.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/parser_diagnostics_mode.md
- docs/contracts/parser_gre_connect_resp.md
- docs/contracts/parser_event_lifecycle.md
- docs/contracts/parser_client_actions.md
- docs/contracts/parser_match_state.md
- docs/contracts/parser_gre_game_state.md
- docs/contracts/parser_gre_game_result.md
- docs/contracts/parser_annotation_normalization.md
- docs/contracts/parser_timer_normalization.md
- docs/contracts/parser_game_state_diff_mechanics.md
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/router.py
- src/mythic_edge_parser/parsers/
- tests/test_event_schema_snapshots.py
- tests/test_feature_equity_corpus_ratchet.py
- tests/fixtures/schema_snapshots/parser_payload_keys.json
- tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json

## Observed Current Behavior

### Event Model And Router

Current event classes include:

- `GameState`
- `ClientAction`
- `MatchState`
- `Truncation`
- `DraftBot`
- `DraftHuman`
- `DraftComplete`
- `EventLifecycle`
- `Session`
- `Rank`
- `Collection`
- `DeckCollection`
- `Inventory`
- `GameResult`
- `LogFileRotated`
- `DetailedLoggingStatus`
- `MatchConnectionState`
- `TcpConnectionClose`
- `WebSocketClosed`
- `ConnectionError`

The router dispatches known parser modules by `EntryHeader`. The field-level
audit must treat router dispatch as a reachability requirement: an event class
alone is not parity if no parser route can emit it.

### Schema Snapshot Coverage

`tests/test_event_schema_snapshots.py` currently snapshots parser event classes
and sample payload keys. It includes samples for the event families in this
contract.

The snapshot protects field names, not field semantics. It does not prove that
every field is populated from every real Player.log shape.

### Corpus Ratchet Coverage

The initial feature-equity corpus baseline currently includes non-zero counts
for:

- `Rank`
- `MatchState`
- `ClientAction`
- `GameState`
- `GameResult`

The same baseline currently records zero corpus events for:

- `Collection`
- `DeckCollection`
- `EventLifecycle`
- `Inventory`
- `Session`
- `MatchConnectionState`
- `TcpConnectionClose`
- `WebSocketClosed`
- `ConnectionError`
- `Truncation`

This is not a parser bug by itself. It means those surfaces are protected by
focused tests and schema snapshots, but not yet by the committed golden replay
corpus.

## Audited Event-Family Matrix

Codex C must preserve and refine this matrix in the comparison handoff.

### GRE ConnectResp

- parser module: `src/mythic_edge_parser/parsers/gre/connect_resp.py`
- event kind: `GameState`
- payload type: `connect_resp`
- detection source: GRE message with dictionary `connectResp`
- primary tests:
  - `tests/test_gre_connect_resp_parser.py`
  - `tests/test_event_schema_snapshots.py`
- current corpus ratchet coverage: `connect_resp_events == 0`

Parser-owned normalized fields:

- `type`
- `message_type`
- `msg_id`
- `game_state_id`
- `system_seat_ids`
- `deck_cards`
- `sideboard_cards`
- `settings`

Raw evidence fields:

- `raw_connect_resp`

Required audit questions:

- Confirm `system_seat_ids`, `deck_cards`, and `sideboard_cards` are normalized
  lists, not raw lists.
- Confirm `msg_id` and `game_state_id` remain pass-through fields under the
  existing contract.
- Confirm `settings` is a shallow copy.
- Confirm `raw_connect_resp` preserves the full GRE message.
- Confirm connect-response deck evidence is not promoted to active submitted
  deck truth without a separate contract.

Preliminary status: `documented_partial`.

Suspected gaps:

- Current committed corpus does not exercise `connect_resp`.
- Future fallback use of connect-response deck evidence remains uncontracted.

### EventLifecycle

- parser module: `src/mythic_edge_parser/parsers/event_lifecycle.py`
- event kind: `EventLifecycle`
- payload types:
  - `event_join`
  - `event_claim_prize`
  - `event_enter_pairing`
- detection source: raw lifecycle request markers
- primary tests:
  - `tests/test_parser_small_modules.py`
  - `tests/test_event_schema_snapshots.py`
- current corpus ratchet coverage: zero

Parser-owned normalized fields:

- `type`

Raw evidence fields:

- `raw_event_lifecycle`

Required audit questions:

- Confirm lifecycle parsing is intentionally marker-level only.
- Confirm lifecycle JSON fields are not normalized today.
- Confirm raw body preservation is sufficient for future field-level work.
- Confirm current prefix, case, whitespace, and precedence behavior remains
  governed by `parser_event_lifecycle.md`.

Preliminary status: `documented_partial`.

Suspected gaps:

- It is unknown whether lifecycle JSON payload fields should remain raw-only
  forever.
- No committed golden replay corpus coverage exists for lifecycle markers.

### Session

- parser module: `src/mythic_edge_parser/parsers/session.py`
- event kind: `Session`
- payload types:
  - `session_account_update`
  - `session_authenticated`
  - `session_logout`
- detection source:
  - account update text
  - `AuthenticateResponse` / `authenticateResponse`
  - logout word-boundary text
- primary tests:
  - `tests/test_parser_small_modules.py`
  - `tests/test_event_schema_snapshots.py`
- current corpus ratchet coverage: zero

Parser-owned normalized fields:

- `type`
- `display_name`
- `account_id`
- `screen_name`

Raw evidence fields:

- `raw_session`

Required audit questions:

- Confirm account/auth fields are trimmed strings.
- Confirm non-string auth fields degrade to blank strings.
- Confirm `raw_session` is a raw string for text markers and a parsed dict for
  auth response.
- Confirm no session fields become workbook identity truth without a separate
  contract.

Preliminary status: `documented_partial`.

Suspected gaps:

- The raw-evidence type for `raw_session` is mixed string/dict by event type.
- No committed golden replay corpus coverage exists for session events.

### Rank

- parser module: `src/mythic_edge_parser/parsers/rank.py`
- event kind: `Rank`
- payload type: `rank_snapshot`
- detection source: `RankGetCombinedRankInfo`
- primary tests:
  - `tests/test_parser_small_modules.py`
  - `tests/test_event_schema_snapshots.py`
  - `tests/test_feature_equity_corpus_ratchet.py`
- current corpus ratchet coverage: non-zero `Rank` count

Parser-owned normalized fields:

- `type`
- `constructed_class`
- `constructed_level`
- `limited_class`
- `limited_level`
- `constructed_percentile`
- `limited_percentile`

Raw evidence fields:

- `raw_rank`

Required audit questions:

- Confirm container values degrade to defaults.
- Confirm scalar rank values are preserved without downstream workbook
  reinterpretation.
- Confirm parser state owns any carry-forward or match association behavior,
  not `rank.py`.

Preliminary status: `verified`.

Suspected gaps:

- Rank carry-forward confidence/source labels belong to the future evidence
  ledger and are not represented in the rank event payload today.

### Collection

- parser module: `src/mythic_edge_parser/parsers/collection.py`
- event kind: `Collection`
- payload type: `collection_snapshot`
- detection source: `StartHook` response with `PlayerCards`
- primary tests:
  - `tests/test_collection_parser.py`
  - `tests/test_event_schema_snapshots.py`
- current corpus ratchet coverage: zero

Parser-owned normalized fields:

- `type`
- `player_cards`

Raw evidence fields:

- `raw_start_hook`

Required audit questions:

- Confirm `player_cards` requires a mapping.
- Confirm the raw StartHook payload is preserved.
- Confirm card ownership data remains collection evidence, not gameplay or
  decklist truth.

Preliminary status: `documented_partial`.

Suspected gaps:

- No committed golden replay corpus coverage exists for collection snapshots.
- `player_cards` is a preserved mapping rather than a deeply normalized card
  ownership model.

### DeckCollection

- parser module: `src/mythic_edge_parser/parsers/collection.py`
- event kind: `DeckCollection`
- payload type: `deck_collection_snapshot`
- detection source: `StartHook` response with `DeckSummaries` and `Decks`
- primary tests:
  - `tests/test_collection_parser.py`
  - `tests/test_event_schema_snapshots.py`
- current corpus ratchet coverage: zero

Parser-owned normalized fields:

- `type`
- `decks`

Raw evidence fields:

- `raw_start_hook`

Required audit questions:

- Confirm deck summaries are correlated to deck payloads by `DeckId`.
- Confirm orphaned or malformed deck summaries are skipped.
- Confirm each correlated deck keeps summary fields and a raw deck list under
  `list`.
- Confirm deck collection evidence is enrichment and does not replace
  submitted-deck evidence.

Preliminary status: `documented_partial`.

Suspected gaps:

- The `decks` field is correlated but still contains raw deck-list structures.
- No committed golden replay corpus coverage exists for deck collection.

### Inventory

- parser module: `src/mythic_edge_parser/parsers/inventory.py`
- event kind: `Inventory`
- payload type: `inventory_snapshot`
- detection source: `StartHook` response with `InventoryInfo`
- primary tests:
  - `tests/test_parser_small_modules.py`
  - `tests/test_event_schema_snapshots.py`
- current corpus ratchet coverage: zero

Parser-owned normalized fields:

- `type`
- `inventory`

Raw evidence fields:

- `raw_start_hook`

Required audit questions:

- Confirm `InventoryInfo` must be a mapping.
- Confirm the parser preserves inventory payload content without claiming
  workbook economy analytics truth.
- Confirm inventory fields remain out of match/game parser truth.

Preliminary status: `documented_partial`.

Suspected gaps:

- The `inventory` field is raw mapping preservation, not field-by-field
  economy normalization.
- No committed golden replay corpus coverage exists for inventory snapshots.

### MatchConnectionState

- parser module: `src/mythic_edge_parser/parsers/connection_state.py`
- event kind: `MatchConnectionState`
- payload discriminator: current schema snapshot labels this as
  `state_changed`
- detection source: `STATE CHANGED` on `UNITY_CROSS_THREAD_LOGGER`
- primary tests:
  - `tests/test_connection_parsers.py`
  - `tests/test_event_schema_snapshots.py`
- current corpus ratchet coverage: zero

Parser-owned normalized fields:

- `old`
- `new`

Raw evidence fields:

- event metadata raw bytes only

Required audit questions:

- Confirm both transition values must be strings.
- Confirm non-Unity headers do not emit connection-state events.
- Decide whether metadata raw bytes are sufficient raw evidence or whether a
  future `raw_connection_state` payload field is needed.

Preliminary status: `documented_partial`.

Suspected gaps:

- This payload has no explicit `type` field.
- This payload has no explicit `raw_*` field.

### TcpConnectionClose

- parser module: `src/mythic_edge_parser/parsers/connection_close.py`
- event kind: `TcpConnectionClose`
- payload discriminator: current schema snapshot labels this as
  `tcp_connection_close`
- detection source: `Client.TcpConnection.Close`
- primary tests:
  - `tests/test_connection_parsers.py`
  - `tests/test_event_schema_snapshots.py`
- current corpus ratchet coverage: zero

Parser-owned normalized fields:

- none beyond event `kind` and any stable keys present in the parsed payload

Raw evidence fields:

- parsed JSON payload is emitted directly
- event metadata raw bytes

Required audit questions:

- Confirm current behavior intentionally emits the parsed JSON payload directly.
- Confirm richer payload fields such as host, port, reason, status, and nested
  activity are preserved when present.
- Decide whether this should remain `raw_mixed_payload` or gain an additive
  `type` / `raw_tcp_connection_close` wrapper in a future issue.

Preliminary status: `raw_preserved_only`.

Suspected gaps:

- This payload has no explicit `type` field.
- This payload has no explicit `raw_*` field.
- Stable normalized fields are not separated from raw payload content.

### WebSocketClosed

- parser module: `src/mythic_edge_parser/parsers/connection_close.py`
- event kind: `WebSocketClosed`
- payload discriminator: current schema snapshot labels this as
  `websocket_closed`
- detection source: `GREConnection.HandleWebSocketClosed`
- primary tests:
  - `tests/test_connection_parsers.py`
  - `tests/test_event_schema_snapshots.py`
- current corpus ratchet coverage: zero

Parser-owned normalized fields:

- none beyond event `kind` and any stable keys present in the parsed payload

Raw evidence fields:

- parsed JSON payload is emitted directly
- event metadata raw bytes

Required audit questions:

- Confirm current behavior intentionally emits the parsed JSON payload directly.
- Confirm nested TCP payloads are preserved.
- Decide whether this should remain `raw_mixed_payload` or gain an additive
  `type` / `raw_websocket_closed` wrapper in a future issue.

Preliminary status: `raw_preserved_only`.

Suspected gaps:

- This payload has no explicit `type` field.
- This payload has no explicit `raw_*` field.
- Stable normalized fields are not separated from raw payload content.

### ConnectionError

- parser module: `src/mythic_edge_parser/parsers/connection_error.py`
- event kind: `ConnectionError`
- payload discriminators:
  - Unity JSON errors with `error_type` and `payload`
  - connection-manager reconnect results
  - matchmaking GRE connection lost
- primary tests:
  - `tests/test_connection_parsers.py`
  - `tests/test_event_schema_snapshots.py`
- current corpus ratchet coverage: zero

Parser-owned normalized fields:

- `error_type`
- `result`
- `outcome`
- `attempts`

Raw evidence fields:

- `payload` for Unity JSON error markers
- event metadata raw bytes for text-only markers

Required audit questions:

- Confirm Unity JSON error markers preserve parsed raw error payload under
  `payload`.
- Confirm connection-manager text markers normalize result/outcome/attempts.
- Confirm matchmaking GRE lost marker emits only `error_type`.
- Decide whether text-only connection errors need explicit raw text fields or
  whether metadata raw bytes are sufficient.

Preliminary status: `documented_partial`.

Suspected gaps:

- Raw evidence policy differs by connection-error subtype.
- Text-only connection errors do not expose a `raw_*` payload field.
- No committed golden replay corpus coverage exists for connection errors.

### MatchState

- parser module: `src/mythic_edge_parser/parsers/match_state.py`
- event kind: `MatchState`
- payload types:
  - `match_started`
  - `match_completed`
  - `state_changed`
- detection source: `matchGameRoomStateChangedEvent`
- primary tests:
  - `tests/test_match_state_parser.py`
  - `tests/test_match_summary_from_match_state.py`
  - `tests/test_event_schema_snapshots.py`
  - `tests/test_feature_equity_corpus_ratchet.py`
- current corpus ratchet coverage: non-zero `MatchState` count

Parser-owned normalized fields:

- `type`
- `state_type`
- `match_id`
- `event_id`
- `players`
- `match_completed_reason`
- `game_results`

Raw evidence fields:

- `raw_match_state`

Required audit questions:

- Confirm game-scope and match-scope result entries remain distinguishable.
- Confirm `players` and `game_results` shapes match the contract.
- Confirm parser state, not this parser, owns final match/game reconciliation.

Preliminary status: `verified`.

Suspected gaps:

- Any explicit game-number assignment for MatchState game results remains a
  parser-state/final-reconciliation issue, not a field-level parser issue.

### ClientAction

- parser module: `src/mythic_edge_parser/parsers/client_actions.py`
- event kind: `ClientAction`
- payload types:
  - `client_ui_message`
  - `generic_client_action`
  - `mulligan_resp`
  - `select_n_resp`
  - `submit_deck_resp`
- detection source: `ClientToGREMessage` and `ClientToGREUIMessage`
- primary tests:
  - `tests/test_client_actions_parser.py`
  - `tests/test_event_schema_snapshots.py`
  - `tests/test_feature_equity_corpus_ratchet.py`
- current corpus ratchet coverage: non-zero `ClientAction` count

Parser-owned normalized fields:

- `type`
- `message_type`
- `decision`
- `selected_option_ids`
- `selected_object_ids`
- `deck_cards`
- `sideboard_cards`
- `game_state_id`
- `resp_id`
- `request_id`

Raw evidence fields:

- `raw_client_action`

Required audit questions:

- Confirm UI, generic, and specialized payloads preserve raw client-action
  envelopes.
- Confirm selected IDs and deck card lists use shared integer-list
  normalization.
- Confirm generic fallback preserves future message types.
- Confirm submit-deck evidence remains separate from ConnectResp deck evidence.

Preliminary status: `verified`.

Suspected gaps:

- Generic payloads do not currently include request context fields.
- Unknown mulligan decisions are not preserved separately from normalized
  `decision`.

### GameState Limited Overlap

- parser modules:
  - `src/mythic_edge_parser/parsers/gre/game_state.py`
  - `src/mythic_edge_parser/parsers/gre/annotations.py`
  - `src/mythic_edge_parser/parsers/gre/timers.py`
  - `src/mythic_edge_parser/parsers/gre/game_state_diff.py`
- event kind: `GameState`
- payload types:
  - `game_state_message`
  - `queued_game_state_message`
  - `connect_resp`
- primary tests:
  - `tests/test_gre_game_state_parser.py`
  - `tests/test_gre_annotations_parser.py`
  - `tests/test_gre_timers_parser.py`
  - `tests/test_gre_game_state_diff_parser.py`
  - `tests/test_event_schema_snapshots.py`
  - `tests/test_feature_equity_corpus_ratchet.py`
- current corpus ratchet coverage: non-zero `GameState` count

Parser-owned normalized fields:

- fields listed in `docs/contracts/parser_gre_game_state.md`
- `normalized_annotations`
- `normalized_timers`
- `game_state_diff_mechanics`

Raw evidence fields:

- `players`
- `zones`
- `game_objects`
- `annotations`
- `persistent_annotations`
- `timers`
- `actions`
- `raw_game_state`

Required audit questions:

- Confirm this audit does not re-open the completed annotation, timer, or
  diff-mechanics contracts.
- Confirm raw arrays remain preserved even when normalized summaries exist.
- Confirm GameState field gaps that require broader normalization are routed to
  a future GameState normalization backlog item.

Preliminary status: `verified` for completed module fields,
`documented_partial` for broader GameState normalization.

Suspected gaps:

- `docs/problem_representations/game_state_normalization_backlog.md` is absent
  on the current branch.
- Current committed corpus has GameState coverage but does not deeply exercise
  every GameState subfield category.

### GameResult Limited Overlap

- parser module: `src/mythic_edge_parser/parsers/gre/game_result.py`
- event kind: `GameResult`
- payload type: `game_result`
- detection source: game-over GRE GameState payload
- primary tests:
  - `tests/test_gre_game_result_parser.py`
  - `tests/test_event_schema_snapshots.py`
  - `tests/test_feature_equity_corpus_ratchet.py`
- current corpus ratchet coverage: non-zero `GameResult` count

Parser-owned normalized fields:

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

Raw evidence fields:

- `results`
- `game_info`
- nested data preserved from normalized GameState payload

Required audit questions:

- Confirm top-level winner/result fields remain game-scope-derived.
- Confirm match-scope results remain preserved in `results`.
- Confirm parser state owns final match reconciliation.

Preliminary status: `verified`.

Suspected gaps:

- Broader field-level provenance belongs to the future evidence ledger.

## Out-Of-Scope Event Families

The following are not part of the issue #121 field-level parity audit:

- DraftBot
- DraftHuman
- DraftComplete
- full draft parser support
- full GameState normalization backlog implementation
- workbook row parity
- webhook payload parity
- Apps Script parity changes
- coaching evaluation
- AI analytics

`Truncation` is already covered by its own reliability module and may be cited
as related data-loss evidence, but this audit must not change truncation
behavior.

## Required Codex C Comparison Behavior

Codex C must produce:

- docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md

The comparison must be docs-focused. It must not implement parser behavior,
add fields, add fixtures, update snapshots, or modify tests unless the user
explicitly authorizes a new implementation scope after the comparison.

The comparison report must include:

- files inspected
- audited event-family matrix
- observed parser-owned normalized fields
- observed raw-evidence fields
- test/snapshot/replay/corpus evidence per family
- current status label per family
- suspected gaps
- unknowns
- recommended follow-up issues, if any
- protected-surface status
- validation run
- next recommended role

If Codex C finds that a current module contract is wrong or stale, it must route
back to Codex B rather than silently revising behavior.

If Codex C finds that parser behavior is missing but the contract does not
authorize implementation, it must record a follow-up recommendation rather than
implementing the behavior.

## Required Evidence Per Family

For each audited family, Codex C must record at least one item in each column:

| Evidence column | Acceptable evidence |
| --- | --- |
| detection evidence | source parser marker, API method, GRE message type, or router dispatch path |
| event evidence | event class, `kind`, performance class, and payload discriminator |
| normalized-field evidence | contract section, code field list, or focused test assertion |
| raw-evidence evidence | `raw_*` field, emitted raw/mixed payload policy, or metadata raw bytes |
| test evidence | focused parser tests, snapshot tests, golden replay, corpus ratchet, or explicit missing-test note |
| boundary evidence | contract or code statement that downstream surfaces do not own truth |

## Unknowns

- The GameState normalization backlog problem representation was not present on
  this branch during this contract pass.
- It is unknown whether EventLifecycle should remain marker-level only or later
  normalize selected JSON fields.
- It is unknown whether connection close/state/error payloads should gain
  explicit `type` and `raw_*` fields in a future additive module.
- It is unknown whether local private Player.log evidence should ever be used
  for a field-level parity matrix. It must not be used in this V1 audit.
- It is unknown whether the parity matrix should become machine-readable in a
  future issue.
- It is unknown whether future golden replay fixtures should be added to cover
  durable parser surfaces currently absent from the corpus baseline.

## Suspected Gaps

- Several audited surfaces have focused tests and schema snapshots but zero
  feature-equity corpus coverage.
- Connection state/close/error payloads use inconsistent raw-evidence policies:
  metadata-only raw bytes, direct parsed JSON payloads, and `payload` nested
  raw data depending on subtype.
- `TcpConnectionClose` and `WebSocketClosed` do not currently have payload
  `type` fields.
- `MatchConnectionState`, `TcpConnectionClose`, and `WebSocketClosed` do not
  currently expose explicit `raw_*` payload fields.
- `Session.raw_session` is string for text events and dict for auth responses.
- Collection, deck collection, and inventory fields preserve broad raw-ish
  structures rather than fully normalized nested field models.
- The first corpus baseline does not exercise ConnectResp, EventLifecycle,
  Session, Collection, DeckCollection, Inventory, or connection payloads.

These are audit findings to confirm, not authorization to change code.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior
- parser state final reconciliation
- parser event classes
- parser event kind values
- parser payload shapes
- match identity
- game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- live workbook state
- deployed Apps Script state
- output transport behavior
- runtime status file shape
- failed-post files
- generated card/tier/oracle data
- raw logs
- private local logs
- committed fixture data
- schema snapshots
- corpus ratchet baseline
- secrets
- credentials
- environment variables
- production behavior

Codex C may recommend follow-up implementation issues for these surfaces, but
must not change them in the comparison thread.

## Validation Requirements

### Contract Writer Validation

For this Codex B pass:

```powershell
git diff --check
@'
docs/contracts/parser_field_level_parity_audit.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
```

### Codex C Comparison Validation

For a docs-only comparison:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/parser_field_level_parity_audit.md
docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
```

If Codex C chooses to run behavior checks as read-only evidence, the suggested
focused set is:

```powershell
py -m pytest -q tests/test_event_schema_snapshots.py
py -m pytest -q tests/test_gre_connect_resp_parser.py tests/test_connection_parsers.py tests/test_collection_parser.py tests/test_parser_small_modules.py
py -m pytest -q tests/test_client_actions_parser.py tests/test_match_state_parser.py tests/test_gre_game_state_parser.py tests/test_gre_game_result_parser.py
py -m pytest -q tests/test_feature_equity_corpus_ratchet.py tests/test_golden_replay_harness.py
```

These tests are evidence only for the comparison thread. Failing tests must be
reported and routed; Codex C must not fix them unless the user explicitly
authorizes implementation.

## Acceptance Criteria

This contract is complete when:

- `docs/contracts/parser_field_level_parity_audit.md` exists.
- The contract links issue #121, tracker #47, related tracker #11, the agent
  constitution, the Module Contract Writer rules, and the module contract
  template.
- The parser/state truth layer is named.
- The field-level parity standard is defined.
- Field role labels and audit status labels are defined.
- The audited event-family matrix includes ConnectResp, EventLifecycle,
  Session, Rank, Collection, DeckCollection, Inventory, connection-state,
  connection-close, connection-error, MatchState, ClientAction, limited
  GameState overlap, and limited GameResult overlap.
- Parser-owned normalized fields and raw-evidence fields are listed per family.
- Required evidence and validation expectations are defined.
- Unknowns and suspected gaps are explicit.
- Protected surfaces and out-of-scope behavior are explicit.
- The next role is Codex C for a docs-focused comparison report.
- No behavior changes are implemented by this contract thread.

## Next Workflow Action

Next role: Codex C / Module Implementer as comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #121:
https://github.com/Tahjali11/Mythic-Edge/issues/121

Trackers:
- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/11

Current integration branch:
codex/parser-reliability-intelligence

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/parser_field_level_parity_audit.md
- docs/problem_representations/parser_feature_equity_with_manasight.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/parser_diagnostics_mode.md
- docs/contracts/parser_gre_connect_resp.md
- docs/contracts/parser_event_lifecycle.md
- docs/contracts/parser_client_actions.md
- docs/contracts/parser_match_state.md
- docs/contracts/parser_gre_game_state.md
- docs/contracts/parser_gre_game_result.md
- docs/contracts/parser_annotation_normalization.md
- docs/contracts/parser_timer_normalization.md
- docs/contracts/parser_game_state_diff_mechanics.md
- src/mythic_edge_parser/events.py
- src/mythic_edge_parser/router.py
- src/mythic_edge_parser/parsers/
- tests/test_event_schema_snapshots.py
- tests/test_feature_equity_corpus_ratchet.py
- focused parser tests named by the contract

Goal:
Compare the current parser contracts, source, focused tests, schema snapshots, golden replay evidence, and feature-equity corpus ratchet evidence against docs/contracts/parser_field_level_parity_audit.md. Produce docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md.

Before editing:
- Confirm the branch is codex/parser-reliability-intelligence and even with origin.
- Inspect git status and exclude unrelated changes.
- State what the field-level parity audit is supposed to prove, what the repo already proves, what gap remains, why the gap exists, and the exact minimal comparison plan.

Do:
- Keep this pass docs-focused.
- Build the audited event-family matrix required by the contract.
- Distinguish parser-owned normalized fields from raw-evidence fields.
- Record test, schema snapshot, golden replay, and corpus ratchet evidence per family.
- Classify each family as verified, documented_partial, raw_preserved_only, suspected_gap, unknown, or out_of_scope.
- Identify follow-up issues for missing fields, missing tests, raw-evidence policy gaps, or missing corpus coverage.
- Produce docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md with files inspected, observed matches, gaps, protected-surface status, validation, remaining risks, and next recommended role.

Do not:
- Implement parser behavior changes.
- Add, remove, or rename parser payload fields.
- Update schema snapshots.
- Update feature-equity corpus baselines.
- Add fixtures or raw log slices.
- Copy Manasight source code.
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, fixtures, snapshots, production behavior, or CI gates.
- Target main.
- Mark #47 or #11 complete.
- Stage, commit, open a PR, or merge unless explicitly asked.

Validation:
git status --short --branch
git diff --check
@'
docs/contracts/parser_field_level_parity_audit.md
docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin

Optional read-only evidence checks:
py -m pytest -q tests/test_event_schema_snapshots.py
py -m pytest -q tests/test_gre_connect_resp_parser.py tests/test_connection_parsers.py tests/test_collection_parser.py tests/test_parser_small_modules.py
py -m pytest -q tests/test_client_actions_parser.py tests/test_match_state_parser.py tests/test_gre_game_state_parser.py tests/test_gre_game_result_parser.py
py -m pytest -q tests/test_feature_equity_corpus_ratchet.py tests/test_golden_replay_harness.py

Final handoff must include:
- role performed
- issue and trackers used
- contract used
- artifact produced
- files changed
- code changed or docs-only
- event-family matrix summary
- observed matches
- suspected gaps
- unknowns
- validation run
- remaining unverified layers
- whether forbidden scope was touched
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/121"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #121 and docs/problem_representations/parser_feature_equity_with_manasight.md"
  contract_artifact: "docs/contracts/parser_field_level_parity_audit.md"
  target_artifact: "docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md"
  risk_tier: "Medium"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "git diff --check"
    - "path-scoped protected-surface check for docs/contracts/parser_field_level_parity_audit.md"
  stop_conditions:
    - "Do not implement parser behavior changes in the comparison thread."
    - "Do not add, remove, or rename parser payload fields."
    - "Do not update schema snapshots, corpus baselines, fixtures, or raw log slices."
    - "Do not copy Manasight source code."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or CI gates."
    - "Do not target main."
    - "Do not mark #47 or #11 complete."
```
