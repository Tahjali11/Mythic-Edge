# Parser Feature Equity With Manasight

## Purpose

This document compares Mythic Edge against the local Manasight reference
project supplied by the user as a ZIP archive. The absolute machine-local path
is intentionally omitted from this repo artifact.

The goal is feature equity, not implementation parity. Manasight is a Rust
library and Mythic Edge is a Python parser/data pipeline, so module names and
internal architecture do not need to match. The important question is whether
Mythic Edge has the same parser building blocks needed to observe, normalize,
test, replay, and preserve the same categories of MTGA `Player.log` evidence.

This is a review artifact. It does not authorize parser behavior changes.

## Scope

This pass inspected:

- Manasight README and source files from the local zip extraction.
- Manasight `src/events.rs`, `src/router.rs`, `src/log/entry.rs`,
  `src/stream.rs`, `src/sanitize.rs`, `src/util.rs`, and `src/parsers/**`.
- Manasight parser smoke/corpus tests under `tests/`.
- Mythic Edge parser/event/router/log/app/test surfaces on the current
  `codex/repo-wide-hardening-run` lineage.
- Mythic Edge contracts, schema snapshots, parser regression fixtures, and
  repo-wide hardening docs where relevant.

This pass did not:

- Execute Manasight Rust tests.
- Run Mythic Edge against the full private local `data/match_logs/` corpus.
- Compare every field in every payload deeply.
- Copy Manasight source code into Mythic Edge.
- Decide product scope for draft, economy, inventory, or collection analytics.

## Feature Equity Standard

For this audit, a Manasight capability is considered feature-equivalent in
Mythic Edge only when Mythic Edge has the relevant combination of:

1. A parser or runtime source that recognizes the same log marker or evidence
   family.
2. A public event kind or first-class normalized output for the parsed evidence.
3. Router or stream wiring that can actually emit the event/output.
4. Focused tests or fixtures proving the parser path.
5. A contract, snapshot, or policy artifact when the surface is durable,
   protected, workbook-facing, or analytics-facing.

An event class alone is not feature equity if no parser can emit it.

## Status Legend

| Status | Meaning |
| --- | --- |
| Covered | Mythic Edge appears to have parser/event/test support for the capability. |
| Covered+ | Mythic Edge appears to exceed Manasight for this local project's needs. |
| Partial | Some building blocks exist, but parser emission, first-class normalization, or tests are incomplete. |
| Missing | Manasight has a capability that Mythic Edge does not appear to implement. |
| Needs Deep Audit | Static inspection suggests coverage, but field-level equivalence needs a contract/test pass. |
| Intentionally Different | Mythic Edge solves the need through a different local pipeline boundary. |

## Manasight Feature Inventory

### Architecture

Manasight describes its pipeline as:

```text
Player.log -> File Tailer -> Entry Buffer -> Router -> Parsers -> Event Bus
```

Major source surfaces:

| Surface | Manasight files | Notes |
| --- | --- | --- |
| Public events | `src/events.rs` | Defines `GameEvent`, metadata, event wrappers, performance classes. |
| Event bus | `src/event_bus.rs` | Async broadcast fan-out. |
| Stream | `src/stream.rs` | Public `MtgaEventStream` entrypoint. |
| Log entry buffering | `src/log/entry.rs` | Header detection, multiline accumulation, brace-depth flush, truncation marker detection. |
| Log discovery/tailer | `src/log/discovery.rs`, `src/log/tailer.rs` | Finds and polls `Player.log`; emits rotation/status signals. |
| Router | `src/router.rs` | Dispatches entries in parser priority order and tracks route/unknown/timestamp stats. |
| Sanitizer | `src/sanitize.rs`, `src/bin/scrub.rs` | Redacts PII/secrets from raw log text. |
| Utilities | `src/util.rs` | Compression, content hashing, logging helpers. |
| Parser modules | `src/parsers/**` | One module per event category. |

### Public Event Families

Manasight's public `GameEvent` variants are:

| Event | Class | Evidence family |
| --- | --- | --- |
| `GameState` | Interactive | GRE `GameStateMessage`, `QueuedGameStateMessage`, `ConnectResp`. |
| `ClientAction` | Interactive | Client-to-GRE decisions: mulligan, select, submit deck, UI noise claiming. |
| `MatchState` | Interactive | `matchGameRoomStateChangedEvent`. |
| `DraftBot` | Durable | Quick Draft bot-draft pack and pick events. |
| `DraftHuman` | Durable | Premier/Traditional human draft pack and pick events. |
| `DraftComplete` | Durable | Draft completion signal. |
| `EventLifecycle` | Durable | Event join, prize claim, enter pairing. |
| `Session` | Durable | Login/account identity/logout. |
| `Rank` | Durable | `RankGetCombinedRankInfo`. |
| `DeckCollection` | Durable | `StartHook` deck summaries and deck lists. |
| `Inventory` | Durable | `StartHook` inventory info. |
| `GameResult` | Post-game | `GameStage_GameOver` from GRE. |
| `LogFileRotated` | Interactive | File tailer rotation signal. |
| `DetailedLoggingStatus` | Interactive | Detailed log enabled/disabled status. |
| `MatchConnectionState` | Interactive | `STATE CHANGED` connection-state transitions. |
| `TcpConnectionClose` | Interactive | `Client.TcpConnection.Close`. |
| `WebSocketClosed` | Interactive | `GREConnection.HandleWebSocketClosed`. |
| `ConnectionError` | Interactive | JSON and plain-text connection error markers. |
| `Truncation` | Interactive | GSM summarization/truncation marker. |

### Parser Modules And Markers

| Manasight parser | Output event | Primary markers / evidence |
| --- | --- | --- |
| `api_common.rs` | Utility | API request/response JSON discovery and method matching. |
| `client_actions.rs` | `ClientAction` | Client-to-GRE decision and UI-message families, including mulligan, selection, and submitted-deck response shapes. |
| `connection_state.rs` | `MatchConnectionState` | `STATE CHANGED`. |
| `connection_close.rs` | `TcpConnectionClose`, `WebSocketClosed` | `Client.TcpConnection.Close`, `GREConnection.HandleWebSocketClosed`. |
| `connection_error.rs` | `ConnectionError` | `TcpConnection.ProcessRead.Exception`, `Client.TcpConnection.ProcessFailure`, `GREConnection.MatchDoorConnectionError`, `TcpConnection.Close.Exception`, plus connection-manager/matchmaking error text. |
| `deck_collection.rs` | `DeckCollection` | StartHook response payloads with deck summaries and deck lists. |
| `draft/bot.rs` | `DraftBot` | `BotDraftDraftStatus`, `BotDraftDraftPick`. |
| `draft/human.rs` | `DraftHuman` | `Draft.Notify`, `EventPlayerDraftMakePick`, `LogBusinessEvents` with `PickGrpId`. |
| `draft/complete.rs` | `DraftComplete` | `DraftCompleteDraft`. |
| `event_lifecycle.rs` | `EventLifecycle` | `EventJoin`, `EventClaimPrize`, `EventEnterPairing`. |
| `gre/mod.rs` | `GameState`, `GameResult` | `greToClientEvent`, `GameStateMessage`, `QueuedGameStateMessage`, `ConnectResp`, `GameStage_GameOver`. |
| `gre/game_state.rs` | `GameState` | Zones, game objects, game info, turn info, annotations, timers, deleted instance ids. |
| `gre/connect_resp.rs` | `GameState` | Initial GRE connect response and deck/config/settings context. |
| `gre/game_result.rs` | `GameResult` | Game-over stage and match/game result scope. |
| `gre/annotations.rs` | Helper | Annotation detail extraction and typed annotation helpers. |
| `gre/turn_info.rs` | Helper | Turn number, phase, step, active/decision/priority player. |
| `inventory.rs` | `Inventory` | StartHook response payloads with inventory information. |
| `match_state.rs` | `MatchState` | Match room transitions, players, match/game results. |
| `metadata.rs` | `DetailedLoggingStatus` | `DETAILED LOGS: ENABLED`, `DETAILED LOGS: DISABLED`. |
| `rank.rs` | `Rank` | Combined rank-info response payloads. |
| `session.rs` | `Session` | Account update, authenticate response, front-door close. |
| `truncation.rs` | `Truncation` | `[Message summarized ...]`, `GameObject Count`, `Annotation Count`. |

### Manasight Test/Hardening Surfaces

| Surface | Notes |
| --- | --- |
| Parser smoke tests | `tests/smoke_parsers.rs` runs parser-attribution over real logs when `MANASIGHT_TEST_LOGS` is set. |
| Smoke ratchet | `tests/smoke_ratchet.rs` compares counts against `smoke-baseline.json`. |
| Router/stream smoke | `tests/smoke_router.rs`, `tests/smoke_stream.rs`, `tests/stream_integration.rs`. |
| Corpus flush timing | `tests/corpus_flush_timing.rs`. |
| Prev GameState ID corpus | `tests/corpus_prev_game_state_id.rs`. |
| Truncation integration | `tests/truncation_integration.rs`. |
| Game-over annotations | `tests/game_over_annotations_integration.rs`. |

## Mythic Edge Feature Inventory

### Architecture

Mythic Edge's current pipeline is broader than the Manasight library surface:

```text
Player.log
  -> log entry buffer / tailer / stream
  -> router
  -> parser modules
  -> event objects
  -> parser state and runtime surfaces
  -> normalized match/game/action/deck/collection rows
  -> local status artifacts and optional Google Sheets transport
```

Major source surfaces:

| Surface | Mythic Edge files | Notes |
| --- | --- | --- |
| Public events | `src/mythic_edge_parser/events.py` | Event dataclasses, metadata hash, performance classes. |
| Event bus | `src/mythic_edge_parser/event_bus.py` | Local subscriber fan-out. |
| Stream | `src/mythic_edge_parser/stream.py` | Tailer/router/event bus orchestration; rotation and detailed-log status. |
| Log entry buffering | `src/mythic_edge_parser/log/entry.py` | Header detection and multiline accumulation. |
| Tailer | `src/mythic_edge_parser/log/tailer.py` | File polling and rotation support. |
| Router | `src/mythic_edge_parser/router.py` | Header-scoped parser dispatch and router stats. |
| Sanitizer | `src/mythic_edge_parser/sanitize.py`, `src/mythic_edge_parser/bin/scrub.py` | Raw log redaction. |
| Utilities | `src/mythic_edge_parser/util.py` | Compression/content hashing utilities. |
| Parser modules | `src/mythic_edge_parser/parsers/**` | Python parser modules for core event families. |
| Parser state | `src/mythic_edge_parser/app/state.py` | Match/game interpretation state and final summary rows. |
| Runtime surfaces | `src/mythic_edge_parser/app/runtime_surfaces.py` | Deck, collection, inventory, rank, match history, timelines. |
| Gameplay actions | `src/mythic_edge_parser/app/gameplay_actions.py` | Card/object/action observation and local action rows. |
| Workbook/schema outputs | `models.py`, `sheet_schema.py`, `sheet_exports.py`, `outputs.py` | Workbook-facing normalized row contracts. |
| Drift/hardening | `log_drift_sensor.py`, schema snapshots, golden fixtures, hardening tools | Stronger repo-governance and drift tooling than Manasight's library scope. |

### Public Event Families

Mythic Edge currently defines these event classes:

| Event class | Kind | Notes |
| --- | --- | --- |
| `GameStateEvent` | `GameState` | Emitted by GRE parser for `GameStateMessage`, `QueuedGameStateMessage`, and `ConnectResp`. |
| `ClientActionEvent` | `ClientAction` | Emitted for client-to-GRE decisions and UI channel claims. |
| `MatchStateEvent` | `MatchState` | Emitted for match room state changes. |
| `DraftBotEvent` | `DraftBot` | Event class exists, but no parser module/routing was found. |
| `DraftHumanEvent` | `DraftHuman` | Event class exists, but no parser module/routing was found. |
| `DraftCompleteEvent` | `DraftComplete` | Event class exists, but no parser module/routing was found. |
| `EventLifecycleEvent` | `EventLifecycle` | Emitted by `event_lifecycle.py`. |
| `SessionEvent` | `Session` | Emitted by `session.py`. |
| `RankEvent` | `Rank` | Emitted by `rank.py`. |
| `CollectionEvent` | `Collection` | Mythic-specific `StartHook` player-card collection snapshot. |
| `DeckCollectionEvent` | `DeckCollection` | Emitted by `collection.py`. |
| `InventoryEvent` | `Inventory` | Emitted by `inventory.py`. |
| `GameResultEvent` | `GameResult` | Emitted alongside game-over `GameState`. |
| `LogFileRotatedEvent` | `LogFileRotated` | Emitted by stream/tailer path. |
| `DetailedLoggingStatusEvent` | `DetailedLoggingStatus` | Emitted by metadata parser and stream status path. |
| `MatchConnectionStateEvent` | `MatchConnectionState` | Emitted by `connection_state.py`. |
| `TcpConnectionCloseEvent` | `TcpConnectionClose` | Emitted by `connection_close.py`. |
| `WebSocketClosedEvent` | `WebSocketClosed` | Emitted by `connection_close.py`. |
| `ConnectionErrorEvent` | `ConnectionError` | Emitted by `connection_error.py`. |

Notably absent from `events.py`:

- `TruncationEvent`

### Parser Modules And Markers

| Mythic Edge parser | Output event | Primary markers / evidence |
| --- | --- | --- |
| `api_common.py` | Utility | API request/response JSON discovery and normalization helpers. |
| `client_actions.py` | `ClientAction` | Client-to-GRE decision and UI-message families, including mulligan, selection, and submitted-deck payloads. |
| `collection.py` | `Collection`, `DeckCollection` | StartHook response payloads with player cards, deck summaries, and deck lists. |
| `connection_state.py` | `MatchConnectionState` | `STATE CHANGED`. |
| `connection_close.py` | `TcpConnectionClose`, `WebSocketClosed` | `Client.TcpConnection.Close`, `GREConnection.HandleWebSocketClosed`. |
| `connection_error.py` | `ConnectionError` | JSON error markers plus `ConnectionManager` and `Matchmaking` markers. |
| `event_lifecycle.py` | `EventLifecycle` | `EventJoin`, `EventClaimPrize`, `EventEnterPairing`. |
| `gre/__init__.py` | `GameState`, `GameResult` | GRE message extraction, `GameStateMessage`, `QueuedGameStateMessage`, `ConnectResp`. |
| `gre/game_state.py` | `GameState` | Preserves game info, turn info, players, zones, game objects, annotations, persistent annotations, timers, actions, diff deletion ids. |
| `gre/connect_resp.py` | `GameState` | Connect response payload shaping. |
| `gre/game_result.py` | `GameResult` | Game-over result payload shaping and match/game result precedence. |
| `gre/turn_info.py` | Helper | Turn/phase/step/player fields. |
| `inventory.py` | `Inventory` | StartHook response payloads with inventory information. |
| `match_state.py` | `MatchState` | `matchGameRoomStateChangedEvent`, players, final result payloads. |
| `metadata.py` | `DetailedLoggingStatus` | `DETAILED LOGS` status. |
| `rank.py` | `Rank` | Combined rank-info response payloads. |
| `session.py` | `Session` | Account update, authenticate response, logout. |

No parser module found for:

- `DraftBot`
- `DraftHuman`
- `DraftComplete`
- `Truncation`

## Feature Equity Matrix

| Capability | Manasight support | Mythic Edge support | Status | Equity judgment / next action |
| --- | --- | --- | --- | --- |
| Public event metadata with raw payload hash | `EventMetadata` with timestamp, raw bytes, SHA-256 hash. | `EventMetadata` with timestamp, raw bytes, SHA-256 hash. | Covered | Equivalent building block exists. |
| Performance classes | `InteractiveDispatch`, `DurablePerEvent`, `PostGameBatch`. | Same performance class labels in Python enum. | Covered | Equivalent event-class metadata exists. |
| Event bus fan-out | `tokio::broadcast` event bus. | Local `EventBus`. | Covered | Implementation differs appropriately by language/runtime. |
| Public stream entrypoint | `MtgaEventStream`. | `MtgaEventStream` and app runner. | Covered+ | Mythic Edge adds app-level runtime/state surfaces. |
| Log discovery | `log/discovery.rs`, Windows known folders. | Configured local path/runtime entrypoints; no direct static parity confirmed in this pass. | Needs Deep Audit | Compare discovery/fallback behavior if laptop/installer polish becomes a goal. |
| Tailer polling | `log/tailer.rs`. | `log/tailer.py`. | Covered | Both have tailer surfaces; field-level behavior not compared here. |
| Log rotation event | `LogFileRotated` emitted by stream/tailer path. | `LogFileRotatedEvent` emitted by stream path. | Covered | Equivalent building block exists. |
| Detailed logging status | Metadata parser plus stream timeout status. | Metadata parser plus stream status path. | Covered | Equivalent building block exists. |
| Entry buffering | Header detection, multiline accumulation, brace-depth flush. | Header detection and multiline accumulation. | Partial | Mythic Edge does not appear to model truncation marker headers; brace-depth semantics should be compared separately if not already covered. |
| GSM truncation marker | `EntryHeader::TruncationMarker`, `TruncationEvent`, parser and integration tests. | No `TruncationEvent`, no truncation parser, no truncation header policy found. | Missing | Create workflow item: GSM truncation marker parser and event. Important for explicit data-loss detection. |
| Router dispatch and unknown stats | Parser priority order plus routed/unknown/timestamp-failure stats. | Header-scoped dispatch plus routed/unknown/timestamp anomaly stats. | Covered | Equivalent building block exists. |
| Parser smoke/corpus ratchet | `smoke_parsers.rs`, `smoke_ratchet.rs`, `smoke-baseline.json`. | Golden fixtures, parser regressions, schema snapshots, hardening reports; no exact full-corpus parser ratchet equivalent in this artifact. | Partial | Existing hardening is strong, but a feature-equity corpus ratchet may be useful for Manasight-style parity. |
| API request/response utilities | `api_common.rs`. | `api_common.py`. | Covered | Equivalent utility exists and has focused tests/hardening. |
| GRE `GameStateMessage` | `gre/game_state.rs`. | `gre/game_state.py`. | Covered | Mythic preserves many raw arrays. First-class subfield normalization is governed by the GameState backlog. |
| GRE `QueuedGameStateMessage` | Supported by GRE parser/game-state builder. | Supported by GRE parser/game-state builder. | Covered | Equivalent building block exists. |
| GRE `ConnectResp` | `gre/connect_resp.rs`. | `gre/connect_resp.py`. | Covered | Equivalent building block exists; field-level contract should confirm deck/settings parity. |
| GRE game-over result | `gre/game_result.rs`, emits `GameState` before `GameResult`. | `gre/game_result.py`, emits `GameState` and then `GameResult`. | Covered | Equivalent building block exists; Mythic has deeper final reconciliation contracts. |
| GRE turn info | `gre/turn_info.rs`. | `gre/turn_info.py`. | Covered | Equivalent building block exists. |
| GRE annotations helper | `gre/annotations.rs` has explicit typed annotation extraction helpers. | GameState parser preserves `annotations` and `persistent_annotations`; `gameplay_actions.py` interprets some annotations. | Partial | Mythic has raw preservation and gameplay interpretation, but no dedicated parser module equivalent to Manasight `gre/annotations.rs`. This should merge with the GameState normalization backlog. |
| GRE timers | Smoke tests track timer counts. | GameState parser preserves `timers`; GameState backlog identifies timer module. | Partial | Preserve exists; first-class timer normalization still needs module workflow. |
| GRE diff deleted instance ids | Smoke tests track diff-deleted IDs. | GameState parser preserves `diff_deleted_instance_ids` and persistent annotation deletion ids. | Partial | Preserve exists; first-class diff/update mechanics still need module workflow. |
| Client actions: mulligan/select/submit deck | `client_actions.rs`. | `client_actions.py` with submit deck runtime surface integration. | Covered+ | Mythic likely exceeds Manasight for submitted-deck downstream usage. |
| ClientToGREUIMessage noise claiming | Manasight claims low-value UI noise as client action/noise. | Mythic parser recognizes `ClientToGREUIMessage` and classifies message channel. | Covered | Equivalent building block exists. |
| Match state | `match_state.rs`. | `match_state.py` plus `state.py` final reconciliation. | Covered+ | Mythic has broader parser-owned match/game summary state. |
| Event lifecycle | `EventJoin`, `EventClaimPrize`, `EventEnterPairing`. | `event_lifecycle.py` handles same family. | Covered | Equivalent building block exists; field-level prize/pairing parity can be audited. |
| Session | Account update, authenticate response, front-door close. | `session.py` handles account update, authenticate response, logout. | Covered | Equivalent building block exists. |
| Rank | `RankGetCombinedRankInfo`. | `rank.py`; `state.py` rank carry-forward; sheet fields. | Covered+ | Mythic likely exceeds Manasight for workbook/rank downstream context. |
| Deck collection | `DeckCollection` from `StartHook` deck summaries/decks. | `DeckCollection` from `StartHook`; runtime deck profile and collection snapshot surfaces. | Covered+ | Mythic likely exceeds Manasight by maintaining local deck/collection profiles. |
| Player card collection | Not a separate Manasight event; Manasight deck collection focuses `DeckSummaries`/`Decks`. | Separate `CollectionEvent` for `PlayerCards`. | Covered+ | Mythic has an additional useful collection snapshot surface. |
| Inventory | `InventoryInfo` from `StartHook`. | `inventory.py` and collection profile snapshot. | Covered | Equivalent building block exists. |
| Bot draft | `draft/bot.rs`, `DraftBot`, `BotDraftDraftStatus`, `BotDraftDraftPick`. | `DraftBotEvent` class exists; no parser module or router wiring found. | Missing | Create workflow item: Quick Draft bot draft parser. |
| Human draft | `draft/human.rs`, `DraftHuman`, `Draft.Notify`, `EventPlayerDraftMakePick`, `LogBusinessEvents` with `PickGrpId`. | `DraftHumanEvent` class exists; no parser module or router wiring found. | Missing | Create workflow item: human draft parser. |
| Draft completion | `draft/complete.rs`, `DraftCompleteDraft`. | `DraftCompleteEvent` class exists; no parser module or router wiring found. | Missing | Create workflow item: draft completion parser. |
| Match connection state | `STATE CHANGED`. | `connection_state.py`. | Covered | Equivalent building block exists. |
| TCP close | `Client.TcpConnection.Close`. | `connection_close.py`. | Covered | Equivalent building block exists. |
| WebSocket close | `GREConnection.HandleWebSocketClosed`. | `connection_close.py`. | Covered | Equivalent building block exists. |
| Connection errors | JSON and text markers, including `ConnectionManager` and `Matchmaking`. | `connection_error.py` includes Unity, ConnectionManager, and Matchmaking parsers. | Covered | Equivalent building block exists. |
| Sanitizer CLI | `scrub` binary and `sanitize.rs`. | `mythicedge-scrub` / `manasight-scrub`, `sanitize.py`. | Covered | Equivalent building block exists. |
| Compression utility | `compress_log`. | `util.py` contains compression/content-hash utilities. | Covered | Equivalent building block exists. |
| Content hash utility | `content_hash`. | `util.py` contains content-hash utilities. | Covered | Equivalent building block exists. |
| Workbook/schema outputs | Not Manasight parser-library scope. | `models.py`, `sheet_schema.py`, `sheet_exports.py`, `outputs.py`, Apps Script parity snapshots. | Covered+ | Mythic adds project-specific downstream output contracts. |
| Parser state/final summary ownership | Not Manasight parser-library scope. | `state.py`, `models.py`, contracts, fixtures. | Covered+ | Mythic goes beyond parser-library event emission into normalized match/game facts. |
| Local card/gameplay action extraction | Not Manasight parser-library scope in inspected zip. | `gameplay_actions.py`, card catalog, card performance. | Covered+ | Mythic has additional analytics-oriented groundwork. |
| Drift/evidence ledger governance | Manasight has smoke baseline and parser ratchet. | Evidence ledger contracts, drift sensor, schema snapshots, golden fixture policy. | Covered+ | Mythic has stronger governance artifacts; a Manasight-style corpus ratchet remains worth considering. |

## Highest-Priority Feature Equity Gaps

### 1. GSM Truncation Marker Parser

Manasight treats Arena's GameStateMessage summarization marker as first-class
evidence. This is important because the missing GSM body is not recoverable
from `Player.log`; the parser can only surface the data-loss signal.

Mythic Edge should add:

- `TruncationEvent` or equivalent parser-owned data-loss event.
- `EntryHeader` or line-buffer support for truncation marker blocks.
- Parser module for `GameObject Count` and `Annotation Count`.
- Tests proving marker detection, no false positives, and router emission.
- Evidence ledger / drift metadata language showing this is a data-loss signal,
  not recovered game truth.

### 2. DraftBot Parser

Mythic Edge already has `DraftBotEvent`, but static inspection found no parser
module or router wiring that can emit it.

Add a workflow item for:

- `BotDraftDraftStatus`
- `BotDraftDraftPick`
- pack presentation payloads
- pick confirmation payloads
- card GRP ID normalization
- draft event identity and pack/pick indexes

### 3. DraftHuman Parser

Mythic Edge already has `DraftHumanEvent`, but static inspection found no parser
module or router wiring that can emit it.

Add a workflow item for:

- `Draft.Notify`
- `EventPlayerDraftMakePick`
- `LogBusinessEvents` with `PickGrpId`
- pack cards
- picked card
- draft/event identity
- pack/pick indexes

### 4. DraftComplete Parser

Mythic Edge already has `DraftCompleteEvent`, but static inspection found no
parser module or router wiring that can emit it.

Add a workflow item for:

- `DraftCompleteDraft`
- draft id extraction
- event name extraction
- bot/human draft completion metadata
- direct request/response variations

### 5. Dedicated Annotation Normalization

Mythic Edge preserves `annotations` and `persistent_annotations` in GameState
payloads and has gameplay action interpretation, but Manasight has a dedicated
`gre/annotations.rs` helper layer with explicit annotation-type handling.

This should not necessarily become a direct port. It should be handled through
the GameState normalization backlog as first-class annotation outputs:

- zone transfer
- object id changed
- damage dealt
- counter added
- target specification
- modified life
- power/toughness modification
- triggering object
- mana paid
- user action taken
- scry
- shuffle
- designation

### 6. Manasight-Style Corpus Ratchet

Mythic Edge has stronger repo hardening than Manasight in several areas, but
Manasight's smoke ratchet is specifically useful for feature-equity protection:
it counts parser claims and event types over a corpus and flags regressions.

Mythic Edge should consider a report-only corpus ratchet after the current
repo-wide hardening suite:

- Run against sanitized fixture corpora first.
- Optionally run locally against private logs without committing private data.
- Track event-kind counts, parser-claim counts, unknown entries, timestamp
  anomalies, and selected GameState subfield counts.
- Keep report-only until a future contract promotes any part of it to a gate.

## Suggested Workflow Queue

These should go through the normal A-G workflow before analytics suite work
depends on them:

1. `TruncationEvent` and GSM truncation marker parser.
2. DraftBot parser.
3. DraftHuman parser.
4. DraftComplete parser.
5. Annotation normalization module under the GameState normalization backlog.
6. GameState timer normalization module.
7. GameState diff/update/deletion mechanics module.
8. Feature-equity corpus ratchet/report.
9. Field-level parity audit for ConnectResp, EventLifecycle, Session, Rank,
   DeckCollection, Inventory, and connection-error payload shapes.

## Recommended Codex A Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex A: Thinker for a parser feature-equity child issue:

GSM truncation marker parser and event

Context:
- Source artifact: docs/problem_representations/parser_feature_equity_with_manasight.md
- External reference: local Manasight zip inspection identified Manasight's
  Truncation event and parser as a missing Mythic Edge feature-equity item.
- Current integration branch should be the agreed parser/drift foundation branch,
  not main, unless explicitly approved.

Goal:
Create a problem representation for adding first-class Mythic Edge support for
Arena's GameStateMessage truncation marker. Refer to the Manasight reference
parser's `truncation.rs` tests for the exact marker text; do not paste raw
private log excerpts into the issue.

Define:
- what the marker means
- why it is a data-loss signal rather than recoverable game truth
- the event kind / payload shape to contract
- line-buffer and router implications
- evidence ledger and drift/provenance implications
- focused tests and fixtures needed
- protected surfaces and out-of-scope behavior changes
- next Codex B prompt

Do not implement code.
Do not copy Manasight code.
Do not change parser behavior, workbook schema, webhook payload shape, Apps
Script behavior, match/game identity, deduplication, secrets, raw logs,
generated data, runtime status files, failed posts, or workbook exports.
```

## Workflow Handoff

```yaml
workflow_handoff:
  source_artifact: "docs/problem_representations/parser_feature_equity_with_manasight.md"
  completed_thread: "local feature-equity audit"
  next_thread: "A"
  target_artifact: "GitHub child issue for GSM truncation marker parser and event"
  risk_tier: "Medium"
  branch: "codex/manasight-feature-equity-audit"
  validation:
    - "static inspection only"
  stop_conditions:
    - "Do not treat event class existence as parser feature equity."
    - "Do not copy Manasight code into Mythic Edge."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior from this audit artifact."
    - "Do not commit raw logs or private local data."
```
