# Player.log Evidence Ledger Tier 4 Sideboarding And Submit-Deck Signal Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/151
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/149
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/150
- previous_merge_commit: 1b264904f2712b32da03530a81b67344082a66ff
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier4-sideboarding-submit-deck
- target_artifact: docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier4_sideboarding_submit_deck_comparison.md
- risk_tier: High
- status: contract only

Required agent docs:

- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md

Related authority:

- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_participant_player_team.md
- docs/contracts/player_log_evidence_ledger_tier3_game_results.md
- docs/contracts/player_log_evidence_ledger_tier3_play_draw.md
- docs/contracts/player_log_evidence_ledger_tier3_mulligans.md
- docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md
- docs/contracts/player_log_evidence_ledger_tier3_turn_count.md
- docs/contracts/player_log_evidence_ledger_tier3_timing_duration.md
- docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md
- docs/contracts/parser_client_actions.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- docs/decisions/ADR-0003-player-log-drift-policy.md

## Purpose

Issue #151 maps Tier 4 sideboarding and submit-deck signal provenance in the
Player.log evidence ledger.

The fields in scope are parser-observed lifecycle signals:

- `sideboarding_entered`
- `submit_deck_seen`

They are not deck-state truth. They do not prove submitted deck contents,
sideboard card deltas, sideboard quality, matchup-plan correctness, archetype
classification, player intent, or AI/analytics truth.

This contract documents provenance metadata only. It must not change parser
behavior, client-action parsing behavior, parser state final reconciliation,
parser event classes, workbook schema, webhook payload shape, Apps Script
behavior, output transport, deck-state behavior, submitted-deck card capture,
runtime status files, generated data, failed posts, workbook exports, or
analytics truth.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, validators, vocabulary constants, privacy posture, and the
allowed `value_source`, `confidence`, `finality`, invariant, and drift
vocabularies.

`docs/contracts/player_log_evidence_ledger_tier3_pre_postboard.md` remains
authoritative for `Pre / Postboard`. Issue #151 must preserve the distinction
between slot-derived `Postboard` labels and observed sideboarding signals:

- `Postboard` is not sideboarding proof.
- `sideboarding_entered` is not pre/postboard truth.
- `submit_deck_seen` is not pre/postboard truth.

The top-level broad #11 contract remains authoritative for the long-term Tier
4 map. This issue seeds only the two existing signal fields. It does not map
submitted deck card contents, submitted deck signatures, deck deltas, deck-state
snapshots, sideboard quality, or analytics outputs.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #151 provenance should be
recorded through this contract, implementation handoff, entry notes, and
focused tests rather than by changing the top-level ledger object shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- `src/mythic_edge_parser/parsers/client_actions.py` owns recognition and
  normalization of `ClientAction` events, including generic
  `ClientMessageType_EnterSideboardingReq` and specialized
  `ClientMessageType_SubmitDeckResp`.
- `src/mythic_edge_parser/app/state.py` owns updating
  `MatchSummary.sideboarding_entered` and `MatchSummary.submit_deck_seen` from
  parser events.
- `src/mythic_edge_parser/app/models.py` owns boolean model fields and
  match-log row serialization to `MTGA Sideboard Entered` and
  `MTGA Submit Deck Seen`.
- `src/mythic_edge_parser/app/sheet_schema.py` lists the workbook-facing sync
  field names, but it does not own the truth of the values.
- `src/mythic_edge_parser/app/evidence_ledger.py` describes provenance,
  confidence, finality, degradation, drift, and review expectations.
- Workbook rows, Apps Script, webhook transport, dashboards, diagnostics,
  golden replay, feature-equity reports, drift reports, submitted-deck runtime
  artifacts, GRP candidate tools, sideboarding analytics, deck-state analytics,
  gameplay advice, and AI output are downstream consumers only.

The ledger describes support for parser-owned signal booleans. It must not
compute deck contents, prove sideboarding happened successfully, infer sideboard
changes, infer matchup plans, infer archetypes, or promote analytics
interpretation into parser truth.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier4_sideboarding_submit_deck_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md

Referenced but not silently owned:

- src/mythic_edge_parser/parsers/client_actions.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/runner.py
- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/grp_id_candidates.py
- tests/test_client_actions_parser.py
- tests/test_state.py
- tests/test_app_models.py
- tests/test_sheet_schema.py
- tests/fixtures/golden_replay/

## Public Interface

This contract covers evidence-ledger metadata for existing public parser
surfaces:

| Surface | Existing field | Meaning |
| --- | --- | --- |
| `MatchSummary` | `sideboarding_entered: bool` | Parser has observed a sideboarding-entry client action for the current match. |
| `MatchSummary` | `submit_deck_seen: bool` | Parser has observed a submit-deck client action for the current match. |
| `MatchSummary.to_debug_dict()` | `sideboarding_entered` / `submit_deck_seen` | Debug snapshot booleans. |
| `MatchSummary.to_sheet_row()` | `sideboarding_entered` / `submit_deck_seen` | Internal sheet row booleans. |
| `MatchSummary.to_history_item()` | `sideboarding_entered` / `submit_deck_seen` | Match-history booleans. |
| `MatchSummary.to_match_log_row(final=...)` | `MTGA Sideboard Entered` / `MTGA Submit Deck Seen` | Workbook-facing `Yes`, `No`, or blank signal display. |
| `MATCH_LOG_SYNC_FIELDS` | `MTGA Sideboard Entered` / `MTGA Submit Deck Seen` | Existing sync field names. |

Existing row-value semantics:

- `Yes`: the corresponding parser signal boolean is true.
- `No`: the row is final and the corresponding parser signal boolean is false.
- blank: the row is live and the corresponding parser signal boolean is false.

Required compatibility:

- Do not rename `sideboarding_entered`.
- Do not rename `submit_deck_seen`.
- Do not rename `MTGA Sideboard Entered`.
- Do not rename `MTGA Submit Deck Seen`.
- Do not change literal `Yes`, `No`, or blank live-row behavior.
- Do not add workbook columns, webhook fields, status fields, or parser events.

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` at
`1b264904f2712b32da03530a81b67344082a66ff`:

- The Tier 3 `game_level_facts` family is already `seeded_sample`.
- The Tier 3 family still lists broad future fields `sideboarding` and
  `deck_state`.
- The Tier 4 `sideboarding_and_deck_state` family is `registered_future`.
- Tier 4 currently lists future fields `sideboarding_entered`,
  `submit_deck_seen`, and `submitted_deck_cards`.
- `client_actions.try_parse(...)` recognizes GRE client-action envelopes.
- Unknown GRE client-action message types become `generic_client_action`.
- `ClientMessageType_EnterSideboardingReq` is emitted as a generic
  client-action payload with `message_type`.
- `ClientMessageType_SubmitDeckResp` is emitted as specialized
  `submit_deck_resp` when recognized by the payload builder.
- Specialized submit-deck payloads include `deck_cards`, `sideboard_cards`,
  `game_state_id`, `resp_id`, `request_id`, and `raw_client_action`.
- Missing or malformed submit-deck card lists normalize to empty lists while
  still preserving the submit-deck signal when the message type is recognized.
- `state.py` ignores `ClientAction` events when there is no current match ID.
- `state.py` sets `MatchSummary.sideboarding_entered = True` when a generic
  `ClientMessageType_EnterSideboardingReq` is observed for the current match.
- `state.py` sets `MatchSummary.submit_deck_seen = True` when a specialized
  `submit_deck_resp` or generic `ClientMessageType_SubmitDeckResp` is observed
  for the current match.
- Duplicate signals are idempotent because the parser stores booleans, not
  counts.
- `MatchSummary.to_match_log_row(final=True)` serializes false booleans as
  `No`.
- `MatchSummary.to_match_log_row(final=False)` serializes false booleans as
  blank.
- `MatchSummary.mtga_queue_type()` can use `sideboarding_entered` as a queue
  heuristic fallback. This issue does not change or map queue provenance.
- Runtime submitted-deck artifacts and GRP candidate tooling can consume
  submit-deck card lists. This issue does not map those card-list artifacts or
  their truth.

Observed risks, not fixed by this issue:

- `sideboarding_entered` can look like proof that sideboarding changed deck
  contents, but it only proves the parser saw an enter-sideboarding signal.
- `submit_deck_seen` can look like proof of submitted deck contents, but this
  field only proves the parser saw a submit-deck signal.
- A final `No` is a parser/model row value produced from absence of the
  boolean in current state. It is not absolute proof that the source log never
  contained the signal if the log was truncated, malformed, incomplete, or
  routed differently.
- A submit-deck signal with empty `deck_cards` and `sideboard_cards` can still
  support `submit_deck_seen`; it cannot support card-content truth.

## Scope Decision

Codex C should implement issue #151 as a Tier 4
`sideboarding_and_deck_state` metadata slice in the existing evidence ledger.

Required family metadata:

- Change Tier 4 `sideboarding_and_deck_state.status` from
  `registered_future` to `seeded_sample`.
- Add these Tier 4 seed fields:
  - `sideboarding_entered`
  - `submit_deck_seen`
- Remove those two fields from Tier 4 `future_fields`.
- Keep `submitted_deck_cards` deferred as a Tier 4 future field.
- Keep broader deck-state work deferred.
- Remove broad Tier 3 future field `sideboarding` after Tier 4 owns the
  signal-family provenance.
- Keep Tier 3 `deck_state` deferred.
- Preserve all prior Tier 1 and Tier 3 seed fields and entries.
- Add notes stating that issue #151 maps signal provenance only and does not
  change client-action parsing, parser state updates, model serialization,
  queue heuristics, submitted-deck card capture, runtime artifacts, workbook
  sync, diagnostics, replay, drift, analytics, or field-evidence attachment
  behavior.

Required Tier 4 entries:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier4.sideboarding_submit_deck.sideboarding_entered` | `sideboarding_entered` | `MTGA Sideboard Entered` | `observed` |
| `tier4.sideboarding_submit_deck.submit_deck_seen` | `submit_deck_seen` | `MTGA Submit Deck Seen` | `observed` |

Do not add entries for `submitted_deck_cards`, submitted deck signatures, deck
lists, sideboard deltas, archetypes, sideboarding advice, queue type, or
pre/postboard labels.

## Required Signal Semantics

`sideboarding_entered`:

- Means the parser observed a current-match `ClientAction` signal with
  `message_type == "ClientMessageType_EnterSideboardingReq"`.
- Does not mean the user changed any card.
- Does not mean a deck was submitted.
- Does not mean the submitted deck contents are known.
- Does not mean the match is Best-of-Three by itself, although existing queue
  heuristics may consume the boolean separately.
- Does not prove sideboard quality, sideboard plan, matchup-plan correctness,
  player intent, or analytics truth.

`submit_deck_seen`:

- Means the parser observed a current-match `ClientAction` signal with
  `type == "submit_deck_resp"` or generic
  `message_type == "ClientMessageType_SubmitDeckResp"`.
- Does not mean submitted main-deck or sideboard card IDs are mapped into the
  evidence ledger.
- Does not mean the submitted deck contents are complete, trusted, named,
  diffed against a prior deck, or workbook-visible.
- Does not mean sideboarding was entered.
- Does not prove sideboard quality, sideboard plan, matchup-plan correctness,
  player intent, archetype, or analytics truth.

For both fields:

- A true boolean is an observed parser signal after state ingestion.
- A final row `Yes` is a derived row rendering of a true boolean.
- A final row `No` is a derived row rendering of a false boolean, not absolute
  source-log absence proof.
- A live row blank is provisional absence, not a final negative claim.
- Missing, malformed, truncated, or unrouted source evidence must degrade
  provenance rather than invent stronger claims.

## Source Evidence Priority

`sideboarding_entered` evidence priority:

1. `ClientAction` generic payload with
   `message_type == "ClientMessageType_EnterSideboardingReq"`.
2. `raw_client_action.payload.type` showing
   `ClientMessageType_EnterSideboardingReq`, path-only, no raw values.
3. `MatchSummary.sideboarding_entered`.
4. `MatchSummary.to_match_log_row(...).["MTGA Sideboard Entered"]`.
5. `MatchSummary.to_debug_dict()["sideboarding_entered"]`,
   `MatchSummary.to_sheet_row()["sideboarding_entered"]`, and
   `MatchSummary.to_history_item()["sideboarding_entered"]` as derived
   downstream model surfaces.

`submit_deck_seen` evidence priority:

1. `ClientAction` specialized payload with `type == "submit_deck_resp"`.
2. `ClientAction` generic payload with
   `message_type == "ClientMessageType_SubmitDeckResp"` if generic fallback is
   encountered.
3. `raw_client_action.payload.type` showing `ClientMessageType_SubmitDeckResp`,
   path-only, no raw values.
4. `MatchSummary.submit_deck_seen`.
5. `MatchSummary.to_match_log_row(...).["MTGA Submit Deck Seen"]`.
6. `MatchSummary.to_debug_dict()["submit_deck_seen"]`,
   `MatchSummary.to_sheet_row()["submit_deck_seen"]`, and
   `MatchSummary.to_history_item()["submit_deck_seen"]` as derived downstream
   model surfaces.

Forbidden evidence for these two entries:

- submitted main-deck card IDs
- submitted sideboard card IDs
- submitted deck names or signatures
- deck snapshot artifacts
- collection snapshot artifacts
- GRP candidate reports
- pre/postboard labels
- queue type
- match format
- game number
- game result
- turn count
- opening hand
- mulligans
- workbook formulas
- Apps Script code
- webhook delivery success
- diagnostics labels
- golden replay status
- analytics or AI interpretation

## Entry Metadata Requirements

Each entry must satisfy the existing schema required fields and use privacy
class `path_only_no_values` for all direct and fallback evidence signals.

Recommended entry details:

| Field | `sideboarding_entered` | `submit_deck_seen` |
| --- | --- | --- |
| `tier` | `4` | `4` |
| `output_family` | `sideboarding_and_deck_state` | `sideboarding_and_deck_state` |
| `coverage_status` | `seeded_sample` | `seeded_sample` |
| `parser_owner` | `src/mythic_edge_parser/app/state.py` | `src/mythic_edge_parser/app/state.py` |
| `model_surface` | `MatchSummary.sideboarding_entered` | `MatchSummary.submit_deck_seen` |
| `downstream_surfaces` | `MatchLogRow`, `match_history`, `state_snapshots`, `MATCH_LOG_SYNC_FIELDS` | `MatchLogRow`, `match_history`, `state_snapshots`, `MATCH_LOG_SYNC_FIELDS` |
| `parser_managed_truth` | `true` | `true` |

Recommended `value_source_policy`:

```json
{
  "direct": "observed",
  "fallback": "derived",
  "missing": "unknown",
  "contradiction": "conflict"
}
```

Recommended `confidence_policy`:

- `direct`: `high` when the matching current-match client-action signal is
  present.
- `model_boolean`: `high` when the boolean is true after normal state
  ingestion.
- `row_yes`: `high` when the final or live row renders `Yes`.
- `final_no`: `medium` when a final row renders `No` and no data-loss warning is
  present.
- `weak_fallback`: `low` when only downstream row/model surfaces are available
  or when raw client-action evidence is unavailable.
- `missing`: `unknown`.

Recommended `finality_policy`:

- `live`: live row blank or live row `Yes` before match finalization.
- `provisional`: parser state boolean before final match row emission.
- `final`: final match row rendering of `Yes` or `No`.
- `reconciled`: only if a later evidence-ledger slice attaches stronger
  source evidence to an existing final field-evidence record.

The implementation does not need runtime field-evidence attachment in issue
#151. The policies above are entry metadata for future consumers.

## Invariants

Required invariant names for `sideboarding_entered`:

- `sideboarding_entered_requires_current_match_context`
- `sideboarding_entered_observed_from_enter_sideboarding_client_action`
- `sideboarding_entered_boolean_is_idempotent_signal`
- `sideboarding_entered_yes_no_blank_row_semantics_preserved`
- `sideboarding_entered_not_pre_postboard_truth`
- `sideboarding_entered_not_submit_deck_truth`
- `sideboarding_entered_not_submitted_deck_contents`
- `sideboarding_entered_not_sideboard_quality_or_plan_truth`
- `sideboarding_entered_not_queue_format_or_ai_truth`

Required invariant names for `submit_deck_seen`:

- `submit_deck_seen_requires_current_match_context`
- `submit_deck_seen_observed_from_submit_deck_client_action`
- `submit_deck_seen_boolean_is_idempotent_signal`
- `submit_deck_seen_yes_no_blank_row_semantics_preserved`
- `submit_deck_seen_not_sideboarding_entered_truth`
- `submit_deck_seen_not_submitted_deck_contents`
- `submit_deck_seen_allows_empty_or_malformed_card_lists`
- `submit_deck_seen_not_sideboard_quality_or_plan_truth`
- `submit_deck_seen_not_archetype_or_ai_truth`

Shared invariants:

- Ledger entries must not include raw private log excerpts.
- Ledger entries must not include submitted card IDs or raw payload values.
- Ledger entries must not add workbook, webhook, Apps Script, runtime status,
  failed-post, generated-data, or export side effects.
- Ledger entries must not change parser-owned signal behavior.

## Degradation Behavior

Each entry must document degradation behavior for:

- missing current match ID causing `state.py` to ignore the `ClientAction`
- malformed or unparsable client-action JSON causing no parser event
- generic client action missing `message_type`
- UI client message that is not a GRE sideboarding or submit-deck signal
- duplicate sideboarding or submit-deck signals collapsing to one boolean
- final `No` representing parser-state absence rather than absolute source-log
  absence
- live blank representing provisional absence
- source log truncation or summarization that could hide a client-action signal
- submit-deck signal with empty normalized `deck_cards` or `sideboard_cards`
- submit-deck signal without a prior observed sideboarding-entered signal
- sideboarding-entered signal without a later observed submit-deck signal
- disagreement between raw client-action signal, model boolean, and row
  serialization

Recommended drift flags:

- `missing_expected_event_family`
- `missing_expected_payload_path`
- `changed_signal_type`
- `new_unknown_event_family`
- `new_unknown_payload_path`
- `fallback_used`
- `weak_fallback_used`
- `conflicting_evidence`
- `fixture_gap`
- `parser_exception`
- `sensitive_evidence_redacted`

## Privacy And Serialization Rules

The ledger must remain local, deterministic, and safe to commit.

Required:

- Use repo-relative paths, symbolic payload paths, or field names only.
- Do not include raw `Player.log` lines.
- Do not include raw `raw_client_action` payload values.
- Do not include submitted deck card IDs, sideboard card IDs, deck names, deck
  signatures, collection data, or local file paths.
- Do not include secrets, tokens, webhook URLs, environment variable values,
  failed post bodies, runtime status artifacts, generated data, workbook
  exports, or private diagnostics artifacts.
- Use `path_only_no_values` for all evidence signals.

## Compatibility Expectations

Codex C must preserve:

- existing `client_actions.py` parser behavior
- existing `state.py` signal updates
- existing `MatchSummary` field names and defaults
- existing `to_match_log_row(final=...)` `Yes`, `No`, blank behavior
- existing `MATCH_LOG_SYNC_FIELDS`
- existing runtime submitted-deck artifact behavior
- existing GRP candidate behavior
- existing diagnostics, golden replay, feature-equity, and drift behavior
- all prior evidence-ledger entries and tests

Codex C must not:

- add submitted deck card provenance in this issue
- change `submit_deck_resp` payload shape
- change `deck_cards` or `sideboard_cards` normalization
- change sideboarding or submit-deck state behavior
- count duplicate sideboarding or submit-deck events
- infer sideboard changes, sideboard quality, or deck deltas
- infer hidden cards, decklists, archetypes, or player intent
- use workbook formulas, Apps Script, webhook transport, dashboards, analytics,
  or AI output as parser truth

## Test Obligations For Codex C

Focused tests in `tests/test_evidence_ledger.py` should prove:

- Tier 4 `sideboarding_and_deck_state` becomes `seeded_sample`.
- Tier 4 `seed_fields` include `sideboarding_entered` and `submit_deck_seen`.
- Tier 4 `future_fields` no longer include `sideboarding_entered` or
  `submit_deck_seen`.
- Tier 4 `future_fields` still include `submitted_deck_cards`.
- Tier 3 `future_fields` no longer include broad `sideboarding`.
- Tier 3 `future_fields` still include `deck_state`.
- Existing Tier 1 and Tier 3 seed fields and entries remain present.
- Entry `tier4.sideboarding_submit_deck.sideboarding_entered` exists and
  validates.
- Entry `tier4.sideboarding_submit_deck.submit_deck_seen` exists and validates.
- Direct evidence for sideboarding documents
  `ClientMessageType_EnterSideboardingReq`, `MatchSummary.sideboarding_entered`,
  and `MTGA Sideboard Entered`.
- Direct evidence for submit-deck documents `submit_deck_resp`,
  `ClientMessageType_SubmitDeckResp`, `MatchSummary.submit_deck_seen`, and
  `MTGA Submit Deck Seen`.
- Both entries use `value_source_policy` with direct `observed`, fallback
  `derived`, missing `unknown`, and contradiction `conflict`.
- Both entries document final `No` as a derived row value, not absolute source
  absence proof.
- Both entries reject submitted deck contents, sideboard deltas,
  pre/postboard labels, queue type, workbook formulas, Apps Script, analytics,
  and AI truth as evidence.
- All direct and fallback evidence signals use `path_only_no_values`.
- Notes mention that submitted deck card contents remain deferred.
- No raw private log text, raw payload values, local runtime artifacts, secrets,
  or generated data are serialized into the ledger.

Optional existing-behavior tests may be inspected but should not require code
changes:

- `tests/test_client_actions_parser.py`
- `tests/test_state.py`
- `tests/test_app_models.py`
- `tests/test_sheet_schema.py`

Expected implementation validation:

```bash
py -m pytest -q tests/test_evidence_ledger.py
py -m ruff check src tests
```

Documentation-only validation for this contract:

```bash
git diff --check
```

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
  exists and is committed in the module PR.
- The contract clearly identifies `sideboarding_entered` and `submit_deck_seen`
  as parser-observed signals.
- The contract clearly rejects deck-state, submitted-deck contents,
  sideboarding quality, matchup-plan, archetype, and AI/analytics truth.
- Codex C is routed to update only evidence-ledger metadata, focused tests, and
  the implementation handoff.
- No parser behavior or protected downstream surface is changed by the contract
  writer pass.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #151, Tier 4 sideboarding and submit-deck signal provenance under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/151
- Previous completed issue: #149
- Previous PR: #150
- Previous merge commit: 1b264904f2712b32da03530a81b67344082a66ff
- Base branch: codex/parser-reliability-intelligence
- Contract: docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md
- Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier4_sideboarding_submit_deck_comparison.md

Goal:
Compare the current evidence-ledger implementation and focused tests against the Tier 4 sideboarding/submit-deck signal contract. Implement only the smallest coherent metadata and test changes needed to satisfy the contract.

Do:
- Verify you are working from codex/parser-reliability-intelligence, not main.
- Read AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, docs/agent_threads/implementation.md, and the contract.
- Update src/mythic_edge_parser/app/evidence_ledger.py so Tier 4 sideboarding_and_deck_state becomes seeded_sample for sideboarding_entered and submit_deck_seen only.
- Add entries tier4.sideboarding_submit_deck.sideboarding_entered and tier4.sideboarding_submit_deck.submit_deck_seen.
- Keep submitted_deck_cards deferred.
- Remove broad Tier 3 sideboarding from future_fields now that Tier 4 owns the signal provenance.
- Keep deck_state deferred.
- Add focused tests in tests/test_evidence_ledger.py for family metadata, entry shape, direct/fallback evidence, value-source policy, confidence/finality policy, degradation behavior, privacy, and protected truth boundaries.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_tier4_sideboarding_submit_deck_comparison.md with comparison, files changed, validation, open risks, and next recommended role.

Do not:
- Change parser behavior, client-action parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, deck-state behavior, submitted-deck card capture, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, diagnostics, replay, drift, schema snapshot, invariant execution, runtime field-evidence attachment, or AI/analytics truth.
- Add submitted deck card provenance, sideboard deltas, deck signatures, deck names, sideboard quality labels, matchup-plan labels, archetype classification, hidden-card inference, gameplay advice, or model-provider behavior.
- Commit raw private Player.log excerpts, raw payload values, submitted deck card IDs, local diagnostics artifacts, generated data, runtime artifacts, secrets, or workbook exports.
- Target main directly.
- Close issue #11.
- Stage or commit unless explicitly asked.

Validation:
- py -m pytest -q tests/test_evidence_ledger.py
- py -m ruff check src tests
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/151"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/149"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/150"
  previous_merge_commit: "1b264904f2712b32da03530a81b67344082a66ff"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier4_sideboarding_submit_deck_comparison.md"
  verdict: "tier4_sideboarding_submit_deck_signal_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier4-sideboarding-submit-deck"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not close issue #11."
    - "Do not target main directly."
    - "Do not change parser behavior, client-action parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, deck-state behavior, submitted-deck card capture, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, diagnostics, replay, drift, schema snapshot, invariant execution, runtime field-evidence attachment, or AI/analytics truth."
    - "Do not add submitted deck card provenance, sideboard deltas, deck signatures, deck names, sideboard quality labels, matchup-plan labels, archetype classification, hidden-card inference, gameplay advice, or model-provider behavior."
    - "Do not commit raw private Player.log excerpts, raw payload values, submitted deck card IDs, local diagnostics artifacts, generated data, runtime artifacts, secrets, or workbook exports."
```
