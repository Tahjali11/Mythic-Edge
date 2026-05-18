# Parser Field-Level Parity Audit Comparison

## Role Performed

Codex C / Module Implementer as a comparison thread.

This pass was a contract-driven audit only. The contract explicitly says the
first implementation thread must produce a comparison handoff and must not
change parser behavior, payload fields, tests, schema snapshots, fixtures, or
corpus baselines.

## Issue And Trackers

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/121
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
- related tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- branch: `codex/parser-reliability-intelligence`

## Contract Used

- `docs/contracts/parser_field_level_parity_audit.md`

Related context inspected:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/problem_representations/parser_feature_equity_with_manasight.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_diagnostics_mode.md`
- parser module contracts for ConnectResp, EventLifecycle, ClientAction,
  MatchState, GameState, GameResult, annotation normalization, timer
  normalization, and GameState diff mechanics

## Artifact Produced

- `docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md`

## Branch And Git Status

Observed before editing:

```text
## codex/parser-reliability-intelligence...origin/codex/parser-reliability-intelligence
?? docs/contracts/parser_field_level_parity_audit.md
```

The existing untracked contract file was treated as source input for issue #121.
No unrelated modified files were absorbed.

## Field-Level Parity Purpose

Field-level parity is supposed to prove that each already-recognized Mythic Edge
parser surface has one of these:

- stable parser-owned normalized fields for facts the parser intends to own;
- explicit raw-evidence preservation for facts not yet normalized;
- focused test, schema snapshot, golden replay, or corpus evidence showing the
  current behavior is guarded;
- a clear status label for missing, deferred, or ambiguous field ownership.

This audit compares parser surfaces. It does not compare workbook formulas,
webhook posts, Apps Script behavior, dashboards, or AI analytics as truth
owners.

## Implementation Option Chosen

Docs-only comparison.

No code, test, fixture, schema snapshot, or corpus baseline change was made,
because the contract does not authorize implementation. The smallest safe output
is this handoff report with the required audited matrix and follow-up routing.

## Files Inspected

Source and routing:

- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/parsers/gre/connect_resp.py`
- `src/mythic_edge_parser/parsers/event_lifecycle.py`
- `src/mythic_edge_parser/parsers/session.py`
- `src/mythic_edge_parser/parsers/rank.py`
- `src/mythic_edge_parser/parsers/collection.py`
- `src/mythic_edge_parser/parsers/inventory.py`
- `src/mythic_edge_parser/parsers/connection_state.py`
- `src/mythic_edge_parser/parsers/connection_close.py`
- `src/mythic_edge_parser/parsers/connection_error.py`
- `src/mythic_edge_parser/parsers/match_state.py`
- `src/mythic_edge_parser/parsers/client_actions.py`
- `src/mythic_edge_parser/parsers/gre/game_state.py`
- `src/mythic_edge_parser/parsers/gre/game_result.py`

Focused tests and fixtures:

- `tests/test_event_schema_snapshots.py`
- `tests/test_feature_equity_corpus_ratchet.py`
- `tests/test_gre_connect_resp_parser.py`
- `tests/test_connection_parsers.py`
- `tests/test_collection_parser.py`
- `tests/test_parser_small_modules.py`
- `tests/test_client_actions_parser.py`
- `tests/test_match_state_parser.py`
- `tests/test_gre_game_state_parser.py`
- `tests/test_gre_game_result_parser.py`
- `tests/test_golden_replay_harness.py`
- `tests/fixtures/schema_snapshots/parser_payload_keys.json`
- `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`
- committed golden replay fixture manifests under `tests/fixtures/golden_replay/`

## Current Behavior Compared To Contract

The repo currently has three layers of relevant evidence:

- event model and router reachability in `events.py` and `router.py`;
- focused parser tests and schema snapshots for all audited surfaces;
- corpus ratchet evidence for a subset of families only.

Current non-zero corpus ratchet families:

- `Rank`
- `MatchState`
- `ClientAction`
- `GameState`
- `GameResult`

Current zero-count corpus ratchet families relevant to this audit:

- `Collection`
- `ConnectionError`
- `DeckCollection`
- `EventLifecycle`
- `Inventory`
- `MatchConnectionState`
- `Session`
- `TcpConnectionClose`
- `Truncation`
- `WebSocketClosed`

Zero corpus coverage is not itself a parser bug. It means the family is guarded
by focused tests and schema snapshots but is not yet represented in the
committed golden replay corpus baseline.

## Audited Event-Family Matrix

| Family | Detection evidence | Event evidence | Normalized-field role | Raw-evidence role | Test/snapshot/corpus evidence | Status | Follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GRE ConnectResp | GRE message containing dictionary `connectResp`; routed through GRE parser path | `GameState`, payload `type=connect_resp`, interactive dispatch | `parser_owned_normalized`: `type`, `message_type`, `msg_id`, `game_state_id`, `system_seat_ids`, `deck_cards`, `sideboard_cards`, `settings` | `raw_evidence_preserved`: `raw_connect_resp`; settings shallow copied; message IDs pass through | `tests/test_gre_connect_resp_parser.py`; schema snapshot; corpus `connect_resp_events == 0` | `documented_partial` | Add future golden/corpus coverage if ConnectResp remains reliability-significant. Do not promote ConnectResp deck evidence to submitted-deck truth without a new contract. |
| EventLifecycle | Raw lifecycle request markers `EventJoin`, `EventClaimPrize`, `EventEnterPairing` | `EventLifecycle`, payload types `event_join`, `event_claim_prize`, `event_enter_pairing`, durable per-event | `parser_owned_normalized`: `type` only | `raw_evidence_preserved`: `raw_event_lifecycle` body | `tests/test_parser_small_modules.py`; schema snapshot; zero corpus coverage | `documented_partial` | Decide in a future contract whether lifecycle JSON fields should remain raw-only or gain selected normalized fields. |
| Session | Account update text, `AuthenticateResponse` / `authenticateResponse`, logout word-boundary text | `Session`, payload types `session_account_update`, `session_authenticated`, `session_logout`, durable per-event | `parser_owned_normalized`: `type`, `display_name`, `account_id`, `screen_name` where present | `raw_evidence_preserved`: `raw_session`; currently string for text markers and dict for auth response | `tests/test_parser_small_modules.py`; schema snapshot; zero corpus coverage | `documented_partial` | Consider a future raw-evidence consistency contract if mixed string/dict `raw_session` becomes hard to consume. |
| Rank | `RankGetCombinedRankInfo` API response | `Rank`, payload `type=rank_snapshot`, durable per-event | `parser_owned_normalized`: rank class, level, and percentile scalar fields | `raw_evidence_preserved`: `raw_rank` | `tests/test_parser_small_modules.py`; schema snapshot; non-zero corpus coverage | `verified` | Future evidence-ledger work can add source/confidence/carry-forward labels. Current event shape matches the field-level contract. |
| Collection | `StartHook` response with mapping `PlayerCards` | `Collection`, payload `type=collection_snapshot`, durable per-event | `parser_owned_normalized`: `type`, `player_cards` as accepted mapping | `raw_evidence_preserved`: `raw_start_hook`; nested ownership model remains raw-ish | `tests/test_collection_parser.py`; schema snapshot; zero corpus coverage | `documented_partial` | Add future corpus fixture coverage if collection snapshots become expected reliability coverage. Do not treat card ownership as gameplay/deck truth. |
| DeckCollection | `StartHook` response with `DeckSummaries` list and `Decks` mapping | `DeckCollection`, payload `type=deck_collection_snapshot`, durable per-event | `parser_owned_normalized`: `type`, correlated `decks` by `DeckId` | `raw_evidence_preserved`: `raw_start_hook`; each correlated deck keeps raw deck list under `list` | `tests/test_collection_parser.py`; schema snapshot; zero corpus coverage | `documented_partial` | Keep deck collection as enrichment evidence. Exact submitted-deck truth remains ClientAction submit-deck evidence unless a future contract says otherwise. |
| Inventory | `StartHook` response with mapping `InventoryInfo` | `Inventory`, payload `type=inventory_snapshot`, durable per-event | `parser_owned_normalized`: `type`, `inventory` as accepted mapping | `raw_evidence_preserved`: `raw_start_hook`; economy fields are not deeply normalized | `tests/test_parser_small_modules.py`; schema snapshot; zero corpus coverage | `documented_partial` | Add corpus coverage only if inventory reliability becomes a tracked parser surface. Keep inventory outside match/game truth. |
| MatchConnectionState | `STATE CHANGED` on `UNITY_CROSS_THREAD_LOGGER`; non-Unity rejected | `MatchConnectionState`, discriminator `state_changed`, interactive dispatch | `parser_owned_normalized`: `old`, `new` string transition values | `raw_mixed_payload`: payload has no `type` and no `raw_*`; metadata raw bytes preserve full body | `tests/test_connection_parsers.py`; schema snapshot; zero corpus coverage | `documented_partial` | Future contract should decide whether to add an explicit `type` and `raw_connection_state` wrapper. This pass does not authorize that payload-shape change. |
| TcpConnectionClose | `Client.TcpConnection.Close` on `UNITY_CROSS_THREAD_LOGGER`; parsed JSON payload required | `TcpConnectionClose`, discriminator `tcp_connection_close`, interactive dispatch | `raw_mixed_payload`: no separated normalized field ownership beyond event kind and stable keys present in parsed payload | `raw_mixed_payload`: parsed JSON emitted directly; metadata raw bytes preserve source body | `tests/test_connection_parsers.py`; schema snapshot; zero corpus coverage | `raw_preserved_only` | Future contract should decide whether to keep direct raw payload emission or add `type` / `raw_tcp_connection_close`. |
| WebSocketClosed | `GREConnection.HandleWebSocketClosed` on `UNITY_CROSS_THREAD_LOGGER`; parsed JSON payload required | `WebSocketClosed`, discriminator `websocket_closed`, interactive dispatch | `raw_mixed_payload`: no separated normalized field ownership beyond event kind and stable keys present in parsed payload | `raw_mixed_payload`: parsed JSON emitted directly; nested TCP payloads preserved; metadata raw bytes preserve source body | `tests/test_connection_parsers.py`; schema snapshot; zero corpus coverage | `raw_preserved_only` | Future contract should decide whether to keep direct raw payload emission or add `type` / `raw_websocket_closed`. |
| ConnectionError | Unity JSON error markers, ConnectionManager reconnect text, Matchmaking GRE lost marker | `ConnectionError`, discriminators via `error_type`, interactive dispatch | `parser_owned_normalized`: `error_type`, `result`, `outcome`, `attempts` where present | Mixed: Unity errors preserve parsed raw payload under `payload`; text-only markers rely on metadata raw bytes | `tests/test_connection_parsers.py`; schema snapshot; zero corpus coverage | `documented_partial` | Future contract should decide whether text-only connection errors need explicit raw text fields. |
| MatchState | `matchGameRoomStateChangedEvent`; wrapped and bare shapes accepted | `MatchState`, payload types `match_started`, `match_completed`, `state_changed`, interactive dispatch | `parser_owned_normalized`: `state_type`, `match_id`, `event_id`, `players`, completion reason, `game_results` | `raw_evidence_preserved`: `raw_match_state` | `tests/test_match_state_parser.py`; `tests/test_match_summary_from_match_state.py`; schema snapshot; non-zero corpus coverage | `verified` | Game-number assignment and final reconciliation remain parser-state concerns, not field-level parser changes in this audit. |
| ClientAction | `ClientToGREMessage` and `ClientToGREUIMessage` | `ClientAction`, payload types `client_ui_message`, `generic_client_action`, `mulligan_resp`, `select_n_resp`, `submit_deck_resp`, interactive dispatch | `parser_owned_normalized`: action type, message type, decision, selected IDs, deck/sideboard cards, request context for specialized payloads | `raw_evidence_preserved`: `raw_client_action` envelope | `tests/test_client_actions_parser.py`; schema snapshot; non-zero corpus coverage | `verified` | Generic payload request context and separately preserved unknown mulligan raw decision are possible future refinements only. |
| GameState limited overlap | GRE GameState message and queued GameState message parsing; ConnectResp also shares `GameState` kind | `GameState`, payload types `game_state_message`, `queued_game_state_message`, `connect_resp`, interactive dispatch | `parser_owned_normalized`: contract GameState fields plus `normalized_annotations`, `normalized_timers`, `game_state_diff_mechanics` | `raw_evidence_preserved`: raw arrays and `raw_game_state` | `tests/test_gre_game_state_parser.py`; annotation/timer/diff tests; schema snapshot; non-zero GameState corpus coverage | `verified` for completed submodules, `documented_partial` for broader GameState normalization | `docs/problem_representations/game_state_normalization_backlog.md` is absent on this branch. Route broader normalization to a future backlog/problem representation. |
| GameResult limited overlap | Game-over GRE GameState payload | `GameResult`, payload `type=game_result`, post-game batch | `parser_owned_normalized`: game-scope winner/result fields, source, stage, match state, identity, game state id, message type | `raw_evidence_preserved`: `results`, `game_info`, and copied identity from GameState payload | `tests/test_gre_game_result_parser.py`; schema snapshot; non-zero corpus coverage | `verified` | Broader source/confidence/finality provenance belongs to future evidence-ledger work. Parser state owns final match reconciliation. |

## Contract Matches

- Event classes listed by the contract exist in `src/mythic_edge_parser/events.py`.
- Router reachability exists for audited families, with connection-specific
  routes restricted to their expected headers.
- Schema snapshots include payload-key coverage for every audited family.
- Focused parser tests cover detection, malformed-input tolerance, raw evidence,
  or normalized fields for every audited family.
- Non-zero corpus ratchet evidence exists for `Rank`, `MatchState`,
  `ClientAction`, `GameState`, and `GameResult`.
- ConnectResp integer-list fields use shared integer-list normalization, and
  `raw_connect_resp` preserves the source GRE message.
- EventLifecycle is intentionally marker-level only and preserves the raw body.
- Session trims string identity fields and degrades non-string auth fields to
  blanks.
- Rank protects scalar fields from container values and preserves `raw_rank`.
- Collection, DeckCollection, and Inventory preserve the StartHook source
  payload while exposing narrow first-level fields.
- MatchConnectionState requires string `old` and `new` transition values.
- TcpConnectionClose and WebSocketClosed preserve parsed connection JSON
  payloads directly, including richer or nested fields.
- ConnectionError distinguishes Unity JSON errors, reconnect text outcomes, and
  matchmaking lost markers.
- MatchState preserves raw match state and normalizes players/game results
  without taking over final reconciliation.
- ClientAction preserves raw envelopes and normalizes selected IDs and deck card
  lists through shared integer-list normalization.
- GameState raw arrays remain preserved even when normalized annotation, timer,
  and diff summaries exist.
- GameResult keeps top-level winner selection game-scope-derived and does not
  promote match-scope result entries to game winner.

## Contract Mismatches

No confirmed behavior mismatch was found that the current contract authorizes
Codex C to fix.

The observed gaps below are either explicitly listed by the contract as audit
findings or require a future scoped contract before implementation:

- several audited families have focused tests and schema snapshots but zero
  corpus ratchet coverage;
- connection-state and connection-close payloads have mixed raw-evidence
  policies and no explicit `raw_*` wrapper in some cases;
- `TcpConnectionClose`, `WebSocketClosed`, and `MatchConnectionState` do not
  expose explicit payload `type` fields;
- `Session.raw_session` is intentionally mixed by subtype today;
- collection/deck/inventory payloads preserve broad raw-ish nested structures
  rather than deeply normalized models;
- broader GameState field normalization backlog is not present on this branch.

## Missing Safeguards Or Missing Tests

Recommended follow-up issues:

1. Add committed golden/corpus fixture coverage for audited zero-count families:
   ConnectResp, EventLifecycle, Session, Collection, DeckCollection, Inventory,
   MatchConnectionState, TcpConnectionClose, WebSocketClosed, and
   ConnectionError.
2. Write a connection payload policy contract deciding whether
   MatchConnectionState, TcpConnectionClose, WebSocketClosed, and selected
   ConnectionError subtypes should gain explicit `type` and `raw_*` fields.
3. Decide whether `Session.raw_session` mixed string/dict evidence is an
   accepted policy or should be normalized behind a future compatibility plan.
4. Decide whether lifecycle JSON subfields should remain raw evidence forever or
   become selected parser-owned fields later.
5. Restore, create, or explicitly defer
   `docs/problem_representations/game_state_normalization_backlog.md` before
   broad GameState normalization work.
6. Consider a future machine-readable parity matrix only after the hand-reviewed
   V1 matrix is accepted.

## Code/Test/Fixture/Tool/Doc Sections Changed

Changed:

- Added this docs-only handoff report:
  - `docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md`

Not changed:

- Parser runtime code
- Parser state final reconciliation
- Parser event classes
- Parser event kind values
- Parser payload shapes
- Tests
- Fixtures
- Schema snapshots
- Feature-equity corpus baseline
- Workbook schema
- Webhook payload shape
- Apps Script behavior
- Live workbook or deployed Apps Script state
- Runtime status files
- Failed-post files
- Generated data
- Secrets or environment variables

## Protected-Surface Status

No forbidden protected surface was intentionally touched.

This comparison pass changed documentation only. The source contract remained
untracked input and this handoff is the only new output file from Codex C.

## Validation Run

Required docs-only validation:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/parser_field_level_parity_audit.md
docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Results:

- `git status --short --branch` passed and showed branch
  `codex/parser-reliability-intelligence...origin/codex/parser-reliability-intelligence`
  with two untracked docs artifacts:
  - `docs/contracts/parser_field_level_parity_audit.md`
  - `docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md`
- `git diff --check` passed.
- Path-scoped protected-surface gate passed:
  - `changed_paths: 2`
  - `forbidden: 0`
  - `warnings: 0`
- Direct trailing-whitespace scan over the untracked contract and handoff found
  no matches.

Optional read-only behavior checks were considered evidence-only by the
contract. They were not needed to justify a behavior change because no behavior
change was authorized.

## Remaining Unverified Layers

- Live workbook state
- Deployed Apps Script state
- Webhook transport behavior
- Production parser behavior
- Private local Player.log evidence
- Future corpus coverage for currently zero-count audited families
- Future field-level provenance/confidence/finality from the Player.log evidence
  ledger

## Forbidden Scope Touched

No.

## Next Recommended Role

Codex E / Module Reviewer as a contract-test review thread.

Codex E should independently review this handoff against
`docs/contracts/parser_field_level_parity_audit.md`, verify that no unauthorized
behavior/test/fixture/snapshot changes were made, and decide whether the
recommended follow-up list should be split into new B-thread contracts.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #121:
https://github.com/Tahjali11/Mythic-Edge/issues/121

Trackers:
- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch:
codex/parser-reliability-intelligence

Contract:
docs/contracts/parser_field_level_parity_audit.md

Implementation/comparison artifact:
docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md

Goal:
Review the Codex C comparison handoff against the field-level parity audit
contract. This is a reviewer pass, not an implementation pass.

Before reviewing:
- Confirm branch is codex/parser-reliability-intelligence.
- Inspect git status and identify unrelated or untracked files.
- Read docs/contracts/parser_field_level_parity_audit.md.
- Read docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md.
- Inspect the source, tests, schema snapshot, and corpus baseline evidence cited
  by the handoff as needed.

Review for:
- whether the event-family matrix covers every family required by the contract;
- whether parser-owned normalized fields and raw-evidence fields are classified
  correctly;
- whether status labels use only verified, documented_partial,
  raw_preserved_only, suspected_gap, unknown, or out_of_scope;
- whether focused tests, schema snapshots, golden replay, and corpus ratchet
  evidence are represented accurately;
- whether suspected gaps are routed to follow-up contracts instead of silently
  implemented;
- whether Codex C avoided unauthorized parser behavior, payload, test, fixture,
  snapshot, corpus, workbook, webhook, Apps Script, secret, and production
  changes.

Do not:
- Change parser behavior.
- Add, remove, or rename parser payload fields.
- Update tests, fixtures, schema snapshots, or corpus baselines unless a new
  user instruction explicitly authorizes a fixer pass.
- Change parser state final reconciliation, workbook schema, webhook payload
  shape, Apps Script behavior, parser event classes, match/game identity,
  deduplication, secrets, raw logs, generated data, runtime status files,
  failed posts, workbook exports, production behavior, or CI gates.
- Stage, commit, open a PR, merge, close issue #121, or mark trackers complete.

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

Final review must lead with findings ordered by severity. Include:
- role performed
- issue and trackers
- contract reviewed
- artifact reviewed
- files inspected
- findings
- contract matches confirmed
- contract gaps or review concerns
- validation run and result
- protected-surface status
- remaining unverified layers
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/121"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/parser_field_level_parity_audit.md"
  target_artifact: "docs/implementation_handoffs/parser_field_level_parity_audit_comparison.md"
  risk_tier: "Medium"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped protected-surface check for the contract and handoff"
  remaining_unverified:
    - "Live workbook state"
    - "Deployed Apps Script state"
    - "Webhook transport behavior"
    - "Production parser behavior"
    - "Private local Player.log evidence"
    - "Corpus coverage for currently zero-count audited families"
    - "Future evidence-ledger field-level provenance/confidence/finality"
  stop_conditions:
    - "Do not implement parser behavior changes from this comparison thread."
    - "Do not add, remove, or rename parser payload fields."
    - "Do not update schema snapshots, corpus baselines, fixtures, tests, or raw log slices."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, or CI gates."
    - "Do not target main."
    - "Do not mark issue #121, tracker #47, or related tracker #11 complete."
```
