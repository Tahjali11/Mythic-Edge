# Problem Representation: Player.log Evidence Ledger And Parser Resilience

GitHub issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

## Summary

Mythic Edge depends on MTGA `Player.log` data that can change or disappear without notice. The project needs a parser evidence ledger that records which raw log signals currently support parser-managed outputs, how those outputs should degrade when evidence is missing, and how future client-update drift should be detected, reported, and refactored.

The ledger is not a replacement source of truth. It is a quality-assurance and resilience layer around the parser: it preserves what the parser believed was observable, explains why each business-critical output is trustworthy or uncertain, and creates a clear path from log-format breakage to focused GitHub issues and parser contracts.

## Background And Trigger

The motivating risk is that MTGA has already removed or reshaped data from the log before. The Manasight Arena log guide documents historical removals and format changes, including the August 2021 removal of collection, inventory, and draft endpoints, later removals of MMR/rating data and opponent display-name tags, and the broader lesson that tools built on `Player.log` should assume any field can disappear after a client patch.

Relevant external reference:

- <https://blog.manasight.gg/arena-log-format-guide/>

The project should treat the current `Player.log` output as the golden starting point, but not as a stable contract promised by Wizards. Current parser behavior should be captured now so future changes can be compared against a known-good baseline.

## What The Code Is Supposed To Do

Mythic Edge is supposed to transform raw MTGA log observations into reliable match, game, deck, card, and workbook-facing facts.

In plain English, the parser should:

- read the local MTGA `Player.log`
- identify relevant MTGA event families
- extract match, game, rank, deck, sideboarding, card, and action facts
- normalize those facts into parser-managed outputs
- post or write those outputs to downstream surfaces
- keep parser truth upstream of workbook formulas and dashboard logic
- avoid silently corrupting analytics when raw evidence is missing, ambiguous, or contradictory

The future ledger should add one more responsibility:

- explain which raw log evidence supports each business-critical parser-managed output, and what the parser should do when that evidence is gone or changed

## What It Is Actually Doing

The current parser has useful normalized outputs, focused tests, and runtime surfaces, but it does not yet have a durable evidence ledger that links parser-managed fields back to specific `Player.log` signals.

Current behavior:

- `src/mythic_edge_parser/app/models.py` defines normalized match and game row shapes.
- `src/mythic_edge_parser/app/state.py` owns parser runtime state and updates `MatchSummary` / `GameSummary` values from events.
- `src/mythic_edge_parser/app/extractors.py` contains shared extraction helpers for MTGA payloads.
- `src/mythic_edge_parser/app/sheet_schema.py` declares parser-managed workbook sync fields.
- Runtime surfaces expose match history, active match snapshots, deck profiles, collection profiles, gameplay action logs, card performance rows, and parser status.
- Tests prove selected row-shape and parser-state behavior.

Missing behavior:

- No versioned ledger maps parser outputs to raw `Player.log` event families and payload paths.
- No project-level schema snapshot records the current golden MTGA log shape.
- No standard field-level metadata says whether a parser value was `observed`, `derived`, `inferred`, `unknown`, `conflict`, or `legacy_enriched`.
- No standard confidence layer tells downstream analytics whether a value is high-confidence, medium-confidence, low-confidence, or unavailable.
- No drift report connects missing raw fields to affected parser outputs.
- No invariant report checks whether the game flow, log evidence, and parser interpretation still agree after a client update.
- No formal degradation policy says when to continue with inferred values, leave values unknown, or stop and ask for manual review.

## Why This Matters

Downstream analytics only stay useful if parser-managed facts remain accurate. If MTGA removes a raw signal and the parser quietly fills a field with a stale assumption, the workbook, dashboard, card performance logic, sideboarding lessons, and future AI-assisted analysis may all become confidently wrong.

The project specifically wants to prioritize:

- accuracy
- explicit uncertainty
- best-effort continuation when safe
- fast detection of changed or missing MTGA signals
- focused refactor issues after Arena updates
- historical compatibility when the parser's source of truth changes over time

This matters most for:

- match history
- win/loss analysis
- game-by-game sideboarding lessons
- play/draw analysis
- mulligan and opening-hand analysis
- card performance analysis
- deck identity and submitted-deck deltas
- rank and queue segmentation
- future local analytics or OpenAI-assisted summaries that depend on parser-produced facts

The ledger should prevent a bad chain like this:

1. Arena removes or changes a `Player.log` field.
2. The parser continues running without noticing.
3. A normalized parser field is populated from a weak fallback.
4. The workbook treats that field as clean truth.
5. Downstream analytics produce misleading recommendations.

The desired chain is:

1. Arena removes or changes a `Player.log` field.
2. The parser detects missing evidence or schema drift.
3. Affected parser-managed outputs are marked inferred, unknown, degraded, or conflicting.
4. Downstream analytics can filter or label the weaker data.
5. The parser emits a drift report with recommended modules/issues to review.
6. The project refactors around the new currently available data.

## Project Layer

Primary layer:

- parser and state interpretation

Supporting layers:

- MTGA raw log source
- runtime diagnostics and status surfaces
- workbook landing sheets
- dashboard / reporting tabs
- future analytics sidecars

Truth ownership:

- MTGA `Player.log` is the ultimate observable evidence source.
- The parser/state layer owns interpretation of that evidence.
- The evidence ledger supports parser quality assurance, but does not replace parser truth.
- Webhook, Apps Script, workbook formulas, dashboard tabs, and AI analytics must not become the owner of parser-managed facts.

Important wording:

- `Player.log` is not absolute game truth. The real game state lives inside Arena.
- `Player.log` is the only local observable evidence this project can inspect.
- When Arena stops emitting a fact, the parser may infer a value, but that value must not be presented as directly observed.

## First Bad Value

The first bad value is not a single broken row today. The first bad value is the absence of field-level evidence provenance for parser-managed outputs.

Right now, a downstream consumer can see a value like:

- `Match Win?`
- `Game Result`
- `Play / Draw`
- `G1 Mulligans`
- `Opening Hand`
- `MTGA Queue Type`

But it cannot reliably know:

- which raw log path supported the value
- whether the value was directly observed or inferred
- whether a fallback path was used
- whether current logs are missing evidence that older logs contained
- whether the value should be trusted after a client update
- which parser module should be audited if the value degrades

First inspection order:

1. Current parser-managed outputs in `src/mythic_edge_parser/app/models.py`.
2. Current sync fields in `src/mythic_edge_parser/app/sheet_schema.py`.
3. Current state mutation paths in `src/mythic_edge_parser/app/state.py`.
4. Current raw payload extraction paths in `src/mythic_edge_parser/app/extractors.py`.
5. Current event identity classification in `src/mythic_edge_parser/app/event_identity.py`.
6. Runtime surfaces in `src/mythic_edge_parser/app/runtime_surfaces.py`.
7. Gameplay action interpretation in `src/mythic_edge_parser/app/gameplay_actions.py`.
8. Card identity and observed `grpId` tooling in `src/mythic_edge_parser/app/arena_id_validation.py`, `src/mythic_edge_parser/app/grp_id_catalog.py`, and related card catalog modules.
9. Existing regression fixtures under `tests/fixtures/`.
10. Local-only golden logs under ignored `data/match_logs/`, if the user explicitly selects representative logs for fixture creation.

## Inputs

Primary inputs:

- current MTGA `Player.log`
- current `Player-prev.log`
- saved raw or filtered match logs under local data directories
- committed regression fixtures
- normalized parser outputs
- parser runtime status
- parser exception/failure logs

Representative raw event families to ledger:

- `matchGameRoomStateChangedEvent`
- `greToClientEvent`
- `GREMessageType_ConnectResp`
- `GREMessageType_GameStateMessage`
- `GREMessageType_QueuedGameStateMessage`
- `GREMessageType_IntermissionReq`
- `GREMessageType_SubmitDeckReq`
- `ClientMessageType_MulliganResp`
- `ClientMessageType_SelectNResp`
- `EventJoin`
- `EventEnterPairing`
- `RankGetCombinedRankInfo`
- `StartHook`
- `authenticateResponse`
- draft-related API events if draft analytics remain in scope

Representative payload areas to ledger:

- match identity and room state
- reserved players and local player/team/seat mapping
- game state identity
- game state `gameInfo`
- game state `turnInfo`
- game state `results`
- game state `zones`
- game state `gameObjects`
- game state `annotations`
- game state `actions`
- submitted deck payloads
- rank payloads
- inventory / collection / deck summaries when exposed
- timestamps from log headers and JSON payloads

Current parser-managed outputs to inspect:

- `MatchSummary`
- `GameSummary`
- `MatchLogRow`
- `GameLogRow`
- `ActionLogRow`
- `DeckSnapshotRow`
- `CollectionSnapshotRow`
- `ParserStatusRow`
- `CardPerformanceRow`
- match history JSON
- active match snapshot JSON
- active match timeline JSON
- active deck profile JSON
- collection profile JSON
- gameplay action logs

## Expected Output

The expected output of this problem representation is not an immediate code change. The expected output is a durable design and workflow foundation for a future module contract.

Recommended artifact path for the next thread:

- `docs/contracts/player_log_evidence_ledger.md`

Recommended future implementation areas, subject to contract:

- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/schema_snapshot.py`
- `src/mythic_edge_parser/app/drift_report.py`
- `src/mythic_edge_parser/app/invariants.py`
- changes to `models.py`, `state.py`, `extractors.py`, `runtime_surfaces.py`, and status outputs only after the contract is written

The ledger design should eventually define:

- business-critical parser-managed output families
- raw evidence dependencies for each output family
- source/fallback rules for each output family
- confidence labels
- finality labels
- drift flags
- schema snapshot format
- invariant checks
- degradation behavior
- downstream compatibility expectations
- validation fixtures and tests
- issue-generation or issue-suggestion format after drift

## Business-Critical Parser-Managed Output Families

### Tier 0: Evidence And Quality Metadata

These fields should eventually exist beside every business-critical parser output, even if they are not all exposed to the workbook at first.

Purpose:

- let downstream systems tell clean observed truth from derived or inferred values
- make client-update drift visible
- support historical parser-version comparisons
- prevent inferred data from silently becoming trusted analytics

Recommended fields:

- `parser_version`
- `parser_commit_sha`
- `log_schema_snapshot_id`
- `ledger_version`
- `source_log_session_id`
- `source_log_file`
- `source_event_kind`
- `source_event_type`
- `source_payload_paths`
- `source_event_timestamp`
- `value_source`
- `confidence`
- `degraded_reason`
- `finality`
- `drift_flags`
- `invariant_status`
- `review_required`

Recommended `value_source` vocabulary:

- `observed`: directly read from current log evidence
- `derived`: computed from multiple observed facts
- `inferred`: best-effort fallback from indirect evidence
- `unknown`: unavailable or not safely recoverable
- `conflict`: multiple evidence paths disagree
- `legacy_enriched`: enriched from older retained metadata that is not currently emitted

Recommended `confidence` vocabulary:

- `high`: directly observed or derived from stable observed facts
- `medium`: inferred from a known fallback with strong support
- `low`: inferred from weak or incomplete support
- `unknown`: no trustworthy evidence

Recommended `finality` vocabulary:

- `live`: still updating during active parsing
- `provisional`: likely but not reconciled
- `final`: emitted after final result evidence
- `reconciled`: final value updated by later stronger evidence

Critical rule:

- Field-level metadata must not be treated as decorative. Downstream analytics should be able to filter, group, warn, or exclude lower-confidence values.

### Tier 1: Match Identity And Lifecycle

These are the highest-risk parser-managed outputs. If these break, almost every downstream table can become unreliable.

Recommended fields:

- `match_id`
- `match_started_at`
- `match_finished_at`
- `match_sync_status`
- `current_game_number`
- `player_team`
- `player_seat_id`
- `opponent_team`
- `opponent_seat_id`
- `match_winner_team`
- `match_result`
- `match_result_type`
- `match_result_reason`
- `games_won`
- `games_lost`
- `total_games`
- `match_win_flag`
- `game_win_rate`

Current row/schema surfaces:

- `MTGA Match ID`
- `MGTA Start Time`
- `MTGA End Time`
- `MTGA Sync Status`
- `Match Win?`
- `Games Won`
- `Games Lost`
- `Total Games`
- `Match Win Flag`
- `Game Win %`

Evidence dependencies to map:

- match room state events
- game room config
- reserved player seat/team data
- current context in parser state
- GRE game result payloads
- match completion payloads
- final match result payloads

Required degradation behavior:

- Missing `match_id` should block final match-level row identity.
- Missing local team/seat should block or downgrade win/loss and play/draw interpretation.
- Missing match winner should prevent final match result from being marked final.
- Conflicting match winner sources should produce `conflict` metadata and require review.
- Live/provisional rows may exist, but final rows must not pretend unknown winner data is known.

Invariant examples:

- A final match row must have one stable `match_id`.
- A final match winner must map to a known participant/team when participants are known.
- `games_won + games_lost` must equal `total_games`.
- `match_win_flag` must agree with `match_result`.
- A match should not become final before a final result source is seen.

### Tier 2: Queue, Format, Rank, And Event Context

These fields decide which analytical bucket a match belongs to. A correct win/loss result in the wrong queue or format can poison comparisons.

Recommended fields:

- `event_id`
- `super_format`
- `match_win_condition`
- `mtga_format`
- `mtga_queue_type`
- `rank_match_type`
- `play_mode_family`
- `event_family`
- `queue_subtype`
- `rank_eligible`
- `is_ranked_match`
- `is_unranked_match`
- `is_constructed_match`
- `is_limited_match`
- `is_draft_match`
- `is_sealed_match`
- `is_ladder_match`
- `is_special_event_match`
- `is_event_match`
- `constructed_rank_raw`
- `constructed_rank_class`
- `constructed_rank_level`
- `constructed_rank_percentile`
- `rank_bucket`
- `rank_source`
- future `limited_rank_raw`, `limited_rank_class`, `limited_rank_level`, `limited_rank_source` if Limited analytics become important

Current row/schema surfaces:

- `MTGA Event ID`
- `MTGA Format`
- `MTGA Queue Type`
- `My Rank`
- `MTGA Rank Raw`

Evidence dependencies to map:

- `EventJoin`
- `EventEnterPairing`
- match room config event identifiers
- game info `superFormat`
- game info `matchWinCondition`
- rank API responses
- parser event identity classifier

Required degradation behavior:

- If raw event ID disappears but game info still exposes format/win condition, derive format and queue with metadata.
- If rank response disappears, mark rank unknown rather than carrying stale rank indefinitely.
- If queue classification falls back to `event_id` string matching, mark source as derived or inferred.
- If Bo3 is inferred from sideboarding or multiple games, mark queue confidence lower than direct `matchWinCondition`.

Invariant examples:

- `Best of 1` should not contain postboard game rows.
- Sideboarding evidence implies Bo3 or another multi-game match mode.
- Ranked-only analytics should not include unranked or unknown-rank-eligibility matches unless explicitly allowed.

### Tier 3: Game-Level Facts

These fields are central to sideboarding lessons and game-by-game analysis.

Recommended fields:

- `game_number`
- `pre_postboard`
- `game_started_at`
- `game_finished_at`
- `game_duration`
- `game_winner_team`
- `game_result`
- `starting_player`
- `play_draw`
- `turn_count`
- `mulligan_count`
- `opening_hand_size`
- `opening_hand`
- `mulliganed_away`

Current row/schema surfaces:

- `Game Number`
- `Pre / Postboard`
- `Play / Draw`
- `Game Result`
- `Turn Count`
- `Game Duration`
- `G1 Play / Draw`
- `G2 Play / Draw`
- `G3 Play / Draw`
- `Game 1 Result`
- `Game 2 Result`
- `Game 3 Result`
- `G1 Mulligans`
- `G2 Mulligans`
- `G3 Mulligans`
- `G1 Turn Count`
- `G2 Turn Count`
- `G3 Turn Count`
- `Opening Hand Size`
- `Opening Hand`
- `Mulliganed Away`

Evidence dependencies to map:

- game state identity payloads
- game info result payloads
- turn info payloads
- local team/player seat mapping
- client mulligan responses
- local private hand zone/object data
- game object `grpId` / instance ID lookup
- timestamps from event metadata

Required degradation behavior:

- If game number is unknown, game-level facts should not be attached to a guessed game without low-confidence metadata.
- If game winner is missing, game result should be unknown rather than inferred from match result unless the match structure makes the inference safe and labeled.
- If starting player is missing, play/draw may be inferred from prior game winner only when match rules and game sequence support it.
- If opening hand card names cannot be resolved, preserve hand size if available and mark exact card list unknown or partially resolved.
- If mulligan events disappear, opening hand size may be inferred only with clear confidence metadata.

Invariant examples:

- Game numbers should progress within a match and should not randomly reset without a new match.
- `Preboard` should normally map to game 1; later games should normally be `Postboard`.
- `play_draw` must agree with local player/team and starting player.
- A game winner should be one of the known teams or should be unknown.
- `game_duration` should not be negative.
- `turn_count` should not decrease for a game once observed.

### Tier 4: Sideboarding And Deck State

This tier is especially important for the user's sideboarding lessons. Current lifecycle flags are useful, but the future ledger should promote per-game submitted-deck identity and sideboard deltas into parser-managed facts.

Recommended fields:

- `sideboarding_entered`
- `submit_deck_seen`
- `submitted_deck_signature_by_game`
- `submitted_deck_timestamp_by_game`
- `mainboard_cards_by_game`
- `sideboard_cards_by_game`
- `sideboard_delta_g1_to_g2`
- `sideboard_delta_g2_to_g3`
- `cards_brought_in`
- `cards_taken_out`
- `deck_signature`
- `deck_name`
- `deck_id`
- `deck_match_mode`
- `deck_format`
- `mainboard_count`
- `sideboard_count`
- `deck_identity_confidence`

Current row/schema/runtime surfaces:

- `MTGA Sideboard Entered`
- `MTGA Submit Deck Seen`
- active deck profile JSON
- match history deck brief
- submitted deck signature
- deck collection matching
- deck snapshot rows

Evidence dependencies to map:

- submit deck client action payloads
- sideboarding/intermission GRE messages
- active submitted deck payloads
- deck collection payloads
- StartHook deck summaries if available
- local card catalog lookup

Required degradation behavior:

- If submit deck data disappears, sideboarding may still be detected from intermission or multi-game flow, but exact card deltas become unknown.
- If deck collection data disappears, active submitted deck signature can remain observed while deck name/id become unknown or legacy enriched.
- If sideboard delta cannot be computed, do not fabricate cards brought in/out from later gameplay alone.
- If per-game deck signatures disagree with expected sideboard flow, flag conflict.

Invariant examples:

- A submitted deck for game 2 or 3 implies a prior game in the same match.
- Sideboard deltas should compare submitted deck states, not inferred game actions.
- Mainboard and sideboard counts should remain plausible for the format.
- `deck_name` must not be required for deck identity; signature is stronger than name.

### Tier 5: Card Identity And Gameplay Actions

This tier powers card performance, action review, and richer game analysis. It is important but more fragile than match/game facts because it depends on object identity, card ID mapping, zones, annotations, and partial state diffs.

Recommended fields:

- `grp_id`
- `instance_id`
- `observed_grp_id`
- `overlay_grp_id`
- `object_source_grp_id`
- `parent_id`
- `identity_hint_source`
- `card_name`
- `display_name`
- `resolution_status`
- `layout`
- `card_faces`
- `actor_relation`
- `turn_number`
- `game_state_id`
- `action_type`
- `cast_mode`
- `from_zone`
- `to_zone`
- `raw_action_types`
- `annotation_types`
- `annotation_categories`
- `visible_in_log`

Current row/schema/runtime surfaces:

- `ActionLogRow`
- `CardPerformanceRow`
- active match action JSON/Markdown
- active match timeline
- observed `grpId` catalog reports
- card catalog resolution outputs

Evidence dependencies to map:

- game object fields
- zone fields
- object instance IDs
- `grpId`, `overlayGrpId`, `objectSourceGrpId`
- annotations
- action arrays
- object replacement annotations
- local/opponent seat mapping
- card catalog lookup
- active deck identity index

Required degradation behavior:

- `instance_id` should remain game-local and not become durable historical card identity.
- `grp_id` should record resolution status and hint source.
- Card names are resolved enrichment, not raw `Player.log` truth.
- If a card identity is ambiguous, preserve the observed ID and mark name resolution uncertain.
- If action type is inferred from zone transitions, mark it inferred rather than directly observed.
- Opponent/private hidden information should not be reconstructed beyond what the log exposes.

Invariant examples:

- One object instance should not map to unrelated canonical cards within the same game without an object replacement explanation.
- A visible gameplay action should have enough identity/action data to be useful.
- Actor relation should be local, opponent, or unknown; it should not be guessed silently.
- Zone transitions should be plausible against prior known state.

### Tier 6: Runtime Health And Drift Detection

This tier tells the user whether the parser can still be trusted and whether a client update likely broke evidence assumptions.

Recommended fields:

- `detailed_logging_enabled`
- `current_match_id`
- `current_game_number`
- `current_player_team`
- `last_event_kind`
- `last_event_type`
- `last_event_at`
- `webhook_successes`
- `webhook_failures`
- `event_failures`
- `router_failures`
- `active_deck_signature`
- `active_deck_name`
- `active_match_action_count`
- `missing_expected_signals`
- `new_unknown_signals`
- `changed_signal_types`
- `changed_signal_paths`
- `degraded_outputs`
- `invariant_failures`
- `recommended_review_modules`
- `recommended_github_issue_titles`

Current row/schema/runtime surfaces:

- `ParserStatusRow`
- runtime status JSON
- active match snapshot
- active match timeline
- failed posts and bad event logs

Evidence dependencies to map:

- log watcher health
- detailed logging status
- router unknown/failure counters
- event parsing failures
- webhook post failures
- schema snapshot comparison
- invariant check results

Required degradation behavior:

- If detailed logging is disabled, parser-managed gameplay outputs should be unavailable rather than inferred.
- If expected event families disappear, parser status should show drift and list affected outputs.
- If new unknown event families appear, preserve enough samples for review without treating them as trusted parser inputs.
- Transport failures must be separated from parser interpretation failures.

Invariant examples:

- A healthy parser should see expected event kinds during a match.
- If active match action count remains zero through a full game, action parsing may be degraded even if match result parsing works.
- Webhook failure does not imply parser truth failure.
- Parser truth failure does not imply workbook failure.

### Tier 7: Derived Analytics Outputs

These outputs are valuable, but they should inherit trust from parser-managed facts rather than becoming parser truth themselves.

Recommended analytics outputs:

- `seen_win_rate`
- `opening_hand_win_rate`
- `cast_win_rate`
- `postboard_cast_win_rate`
- `mulligan_tax`
- `top_matchups`
- `top_packages`
- sideboarding recommendations
- matchup notes
- card-performance summaries

Required rule:

- Derived analytics should expose the minimum confidence of their ingredients.

Example:

- `opening_hand_win_rate` depends on opening hand identity, game result, match/game identity, deck context, and card identity resolution.
- If opening hand data is inferred or partially resolved, the metric should carry that lower confidence or be excluded from clean-truth dashboards.

## Fields Not Treated As Parser-Managed Truth

These fields may be user annotations, workbook classifications, external enrichment, or downstream analytics, but they should not define parser truth:

- `Experiment ID`
- `Deck Code`
- `Opponent Archetype`
- `Opponent Variant`
- `Deck Tier`
- `Valid?`
- `General Analysis?`
- `Primary Comparison Analysis?`
- `Reason Tag`
- `Pilot Error?`
- `One-line note`
- `Rank Group`
- `Mythic Split`
- `Queue Bucket (Auto)`
- `Primary Comparison (Auto)`
- manually assigned matchup labels
- manually assigned sideboarding lesson labels
- external metagame tier labels
- AI-generated summaries, classifications, or recommendations

These fields can consume parser facts. They can enrich user-facing analysis. They must not overwrite parser-owned match/game/card truth.

Special cases:

- `Deck Tier` may be useful for analysis, but it belongs to metagame enrichment.
- `Opponent Archetype` may eventually be inferred by a classifier, but it should be labeled as inferred/enriched unless directly user-assigned.
- AI recommendations can explain patterns, but they must not become the source of match result, game result, play/draw, mulligan, opening hand, card action, or deck submission truth.

## Desired Ledger Shape

The future contract should decide the exact format, but the problem representation recommends a row-oriented or entry-oriented ledger with records shaped like this:

```yaml
ledger_entry:
  output_family: "game_result"
  output_field: "Game Result"
  parser_owner: "src/mythic_edge_parser/app/state.py"
  model_surface: "GameSummary.to_game_log_row"
  downstream_surfaces:
    - "Game Log"
    - "Match Log"
    - "match_history"
    - "card_performance"
  direct_evidence:
    - event_kind: "GameResult"
      payload_path: "gameStateMessage.gameInfo.results[].winningTeamId"
      required: true
  fallback_evidence:
    - event_kind: "MatchState"
      payload_path: "gameRoomInfo.finalMatchResult.resultList[]"
      source_label: "derived"
  value_source_policy:
    direct: "observed"
    fallback: "derived"
    missing: "unknown"
    contradiction: "conflict"
  confidence_policy:
    direct: "high"
    fallback: "medium"
    missing: "unknown"
    contradiction: "low"
  invariants:
    - "winner_team must map to local or opponent team when teams are known"
    - "game_result must agree with winner_team and player_team"
  degradation_behavior:
    - "leave Game Result blank when winner is unknown"
    - "emit degraded output metadata"
    - "recommend parser_state/extractors review"
  tests:
    - "tests/test_state.py"
    - "tests/test_gre_game_result_parser.py"
    - "tests/fixtures/parser_regression_match_expected.json"
```

The contract should decide whether the ledger lives as:

- Markdown only
- YAML/JSON plus Markdown summary
- Python dataclasses plus generated docs
- a hybrid of code-owned structured definitions and docs-owned explanation

Recommendation:

- Use a structured machine-readable format for the ledger entries.
- Generate or maintain a Markdown summary for humans and Codex threads.
- Keep raw local logs out of Git.
- Use redacted committed fixtures for tests.

## Drift Report Requirements

When current logs diverge from the ledger, the parser should eventually produce a drift report.

The drift report should include:

- run timestamp
- parser version / commit
- ledger version
- schema snapshot compared
- observed event families
- missing expected event families
- missing expected payload paths
- changed field types
- new unknown event families
- parser outputs affected
- output confidence downgrades
- invariants that failed
- fallback paths used
- unrecoverable facts
- recommended modules to audit
- suggested GitHub issue titles

Example output:

```text
Drift detected: Game result evidence changed

Missing expected paths:
- greToClientEvent.greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId

Still available:
- matchGameRoomStateChangedEvent.gameRoomInfo.finalMatchResult.resultList[]

Affected parser outputs:
- GameLogRow.Game Result
- MatchLogRow.Game 1 Result
- MatchSummary.match_wl
- CardPerformanceRow opening-hand/cast win rates

Current fallback:
- match winner may be derived from finalMatchResult
- per-game winner is unknown unless game-scoped resultList entries remain available

Recommended issue:
- Audit game result extraction after MTGA log drift
```

## Scope

In scope:

- defining business-critical parser-managed outputs
- defining field-level provenance and confidence requirements
- defining how to treat missing `Player.log` evidence
- defining schema snapshot and drift-report expectations
- defining invariant-engine goals
- defining golden fixture requirements
- distinguishing parser truth from workbook/user/AI enrichment
- producing a future module contract for the evidence ledger
- planning validation that compares old golden logs against new logs

Out of scope:

- implementing the ledger in this thread
- changing parser behavior in this thread
- changing workbook schema in this thread
- changing webhook payload shape in this thread
- adding OpenAI API analytics in this thread
- importing or implementing a full MTG rules engine
- assuming missing private data can be perfectly recovered
- committing raw local MTGA logs
- generating GitHub issues automatically before the contract decides the format

## Non-Goals

The ledger should not:

- simulate a full game of Magic
- become a full MTGA rules engine
- treat inferred values as observed values
- hide uncertainty from downstream analytics
- use workbook formulas as parser error handlers
- treat AI or external analytics as truth-producing
- preserve private or sensitive identity fields unnecessarily
- promise recovery of data Arena no longer emits

## Risks And Likely Breakpoints

High-risk parser breakpoints:

- match identity
- game identity
- player/team/seat mapping
- match winner
- game winner
- result scope
- play/draw
- mulligan counts
- opening hand identity
- sideboard transition detection
- submit deck payload extraction
- deck identity matching
- card `grpId` resolution
- object instance replacement
- full state versus incremental game-state merges
- batched GRE messages
- timestamp parsing
- deduplication keys
- live versus final reconciliation

Likely log-drift risks:

- raw fields disappear
- event families disappear
- field nesting changes
- field types change from int to string or string to int
- payloads become string-encoded where parsed objects were expected
- batched messages change shape
- identity fields become redacted
- rank data disappears or moves
- inventory/collection/deck data disappears or moves
- result scope changes
- card object identity fields change
- private zone data becomes less available

Implementation risks:

- adding too much metadata to workbook-facing rows too early
- making the ledger too manual to maintain
- duplicating parser logic in the ledger
- creating a second source of truth
- treating historical enrichment as current evidence
- overfitting to one local log sample
- failing to distinguish parser drift from transport/workbook/deployment drift
- bloating every row with metadata before deciding which surfaces need it
- causing old dashboards to break by changing row shape without a migration plan

Workflow risks:

- starting implementation before the ledger contract exists
- failing to create representative golden fixtures
- using raw local logs as committed fixtures without redaction
- letting downstream analytics consume inferred fields without warning
- creating GitHub issues too broad to fix cleanly after an Arena update

## Validation Evidence Needed

The first implementation contract should define exact checks. At the problem-representation level, the required evidence should include:

Focused contract validation:

```powershell
py -m pytest -q tests/test_app_models.py tests/test_sheet_schema.py
py -m pytest -q tests/test_state.py tests/test_app_extractors.py
```

Regression validation:

```powershell
py -m pytest -q tests/test_parser_regressions.py
```

Runtime-surface validation:

```powershell
py -m pytest -q tests/test_runtime_surfaces.py
```

Gameplay/action validation:

```powershell
py -m pytest -q tests/test_gameplay_actions.py
```

Repo-level validation:

```powershell
.\tools\run_repo_checks.ps1
```

Future ledger-specific validation should prove:

- every Tier 1 field has at least one direct or explicit fallback evidence rule
- every Tier 2 field has a classification source and degradation rule
- every Tier 3 field has source/confidence/finality behavior
- every Tier 4 sideboarding field distinguishes lifecycle detection from exact deck delta evidence
- every Tier 5 card/action field records identity confidence or resolution status
- every Tier 6 drift/status output distinguishes parser drift from transport failure
- non-parser-managed fields are not allowed to overwrite parser-owned truth
- committed fixtures do not contain sensitive raw identity data
- golden fixture outputs remain stable under the current parser
- drift reports identify affected output fields when evidence is removed from a synthetic fixture

## Golden Fixture Requirements

The project should create a small but representative golden corpus from current working logs.

Recommended fixture categories:

- Bo1 match win
- Bo1 match loss
- Bo3 match win
- Bo3 match loss
- sideboarding between games
- game 1 on the play
- game 1 on the draw
- mulligan to six or lower
- opening hand captured with exact card names
- opening hand partially unresolved, if available
- concede
- timeout or disconnect, if available
- ranked constructed
- unranked constructed
- limited or draft, if in scope
- deck submission / submit deck response
- rank snapshot before or during a match
- game result and match result with both game-scope and match-scope result entries

Each golden fixture should preserve:

- redacted raw log slice or compact structured event fixture
- expected normalized `MatchLogRow`
- expected normalized `GameLogRow` rows
- expected match history item
- expected action/card outputs if relevant
- schema snapshot ID
- parser commit/version
- known caveats
- privacy redaction notes

Raw local logs should not be committed directly unless they are intentionally redacted and approved.

## Open Questions

- Should ledger entries be authored as YAML/JSON, Python dataclasses, Markdown tables, or a hybrid?
- Which downstream surfaces need field-level metadata immediately: internal JSON only, workbook rows, or both?
- Should confidence metadata be per field, per row, or both?
- Should degraded parser outputs be posted to the workbook, held locally, or posted with warnings?
- Should drift reports create GitHub issues automatically, or only suggest issue titles and bodies for manual review?
- Which raw logs should become the first golden fixtures, and what redaction rules should apply?
- Should the first implementation focus only on Tier 1 to Tier 3 before expanding to sideboarding/card actions?
- Should historical records be backfilled with `value_source=observed` where current fixtures prove the source, or should metadata begin only from the ledger implementation date?
- How should the parser promote a new inferred source of truth after a client update and refactor?
- Should `legacy_enriched` values be visible to downstream analytics by default, or opt-in only?

## Recommended First Contract Scope

The first module contract should avoid trying to solve all seven tiers at once. Recommended v1 contract:

1. Define the ledger entry schema.
2. Define the source/confidence/finality vocabulary.
3. Map Tier 1 match identity/lifecycle fields.
4. Map Tier 2 queue/format/rank/event-context fields.
5. Map Tier 3 core game-level fields.
6. Define how Tier 4 to Tier 7 will be represented later.
7. Define one synthetic drift test for missing game-result evidence.
8. Define one synthetic drift test for missing rank evidence.
9. Define one synthetic drift test for missing submit-deck evidence.

The first implementation should not change workbook row shape unless the contract explicitly chooses that as the migration path.

## Next Workflow Action

Next role:

- Module Contract Writer (B)

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as the Module Contract Writer thread for docs/problem_representations/player_log_evidence_ledger.md. Produce docs/contracts/player_log_evidence_ledger.md. Define the v1 contract for a Player.log evidence ledger that maps business-critical parser-managed outputs to raw log evidence, value source labels, confidence labels, finality labels, drift flags, invariant checks, degradation behavior, and validation requirements. Use the seven output tiers from the problem representation. Distinguish required v1 behavior, future tiers, unknowns, and suspected implementation gaps. Do not implement behavior changes.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "A"
  next_thread: "B"
  source_artifact: "docs/problem_representations/player_log_evidence_ledger.md"
  target_artifact: "docs/contracts/player_log_evidence_ledger.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "Docs-only problem representation; validation not run."
  stop_conditions:
    - "Stop before implementation if the contract would change workbook row shape, webhook payload shape, committed fixture policy, or parser final reconciliation behavior."
    - "Stop if raw local MTGA logs are needed as fixtures before redaction rules are approved."
```
