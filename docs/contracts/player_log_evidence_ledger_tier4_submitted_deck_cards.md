# Player.log Evidence Ledger Tier 4 Submitted-Deck Card-Content Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/159
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/151
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/157
- previous_merge_commit: b5aa1ea6b7c9d9a7cca7f7cc580bdf1acb39a24e
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier4-submitted-deck-cards
- target_artifact: docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md
- expected_next_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md
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
- docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md
- docs/contracts/parser_client_actions.md
- docs/contracts/parser_state.md
- docs/contracts/parser_models.md
- docs/contracts/parser_sheet_schema.md
- docs/decisions/ADR-0003-player-log-drift-policy.md

## Purpose

Issue #159 maps Tier 4 submitted-deck card-content provenance in the
Player.log evidence ledger.

The field in scope is:

- `submitted_deck_cards`

This field means Mythic Edge can observe submitted mainboard and sideboard
`grpId` lists from a parsed `ClientMessageType_SubmitDeckResp` payload. It is
card-content evidence, not broad deck-state truth.

This contract intentionally keeps the first mapping narrow. It authorizes one
ledger field, `submitted_deck_cards`, and allows that entry to describe tightly
related derived facets:

- normalized submitted mainboard `grpId` list shape
- normalized submitted sideboard `grpId` list shape
- derived mainboard count
- derived sideboard count
- deterministic submitted-deck signature derived from the two normalized lists
- submit-deck request context and timestamp as provenance only

Those facets are not separate ledger output fields in issue #159. They must
remain inside the `submitted_deck_cards` entry until a later contract explicitly
maps them.

This contract documents provenance metadata only. It must not change parser
behavior, submit-deck parsing behavior, card-list normalization behavior,
runtime artifact write behavior, GRP candidate scoring, parser state final
reconciliation, parser event classes, router behavior, match/game identity,
deduplication, workbook schema, webhook payload shape, Apps Script behavior,
output transport, runtime status files, generated data, failed posts, workbook
exports, production behavior, OpenAI/model-provider behavior, or
AI/analytics truth.

## Relationship To Prior Ledger Contracts

`docs/contracts/player_log_evidence_ledger_schema.md` remains authoritative for
ledger object shape, validators, vocabulary constants, privacy posture, and the
allowed `value_source`, `confidence`, `finality`, invariant, and drift
vocabularies.

`docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md`
remains authoritative for `sideboarding_entered` and `submit_deck_seen`.
Issue #159 builds on that boundary:

- `submit_deck_seen` means a submit-deck signal was observed.
- `submitted_deck_cards` means normalized submitted card-list content was
  observed from that signal.
- Empty or malformed submitted card lists can still support `submit_deck_seen`
  but must not support `submitted_deck_cards` truth.

The broad #11 contract remains authoritative for the long-term evidence
ledger. This issue seeds only one Tier 4 card-content field. It does not map
deck-state, deck deltas, submitted deck by game, deck names, deck IDs, decklist
identity, card names, archetype labels, matchup plans, sideboard-plan quality,
card-performance analytics, gameplay advice, or AI/model-provider behavior.

The top-level `source_issue` in `src/mythic_edge_parser/app/evidence_ledger.py`
may remain issue #128 as the schema origin. Issue #159 provenance should be
recorded through this contract, implementation handoff, entry notes, and
focused tests rather than by changing the top-level ledger object shape.

## Owning Layer

Owning layer: parser resilience / evidence ledger metadata.

Truth boundary:

- `src/mythic_edge_parser/parsers/client_actions.py` owns parsing and
  normalizing `ClientMessageType_SubmitDeckResp` into `submit_deck_resp`,
  `deck_cards`, `sideboard_cards`, and request context fields.
- `src/mythic_edge_parser/app/diagnostics.py` may derive local active
  submitted-deck artifacts, submitted-deck signatures, counts, and runtime
  status fields from normalized submit-deck payloads.
- `src/mythic_edge_parser/app/runtime_surfaces.py` may normalize and cache
  active submitted-deck state for local runtime surfaces.
- `src/mythic_edge_parser/app/grp_id_candidates.py` may consume submitted-deck
  snapshots for review-oriented GRP candidate workflows.
- `src/mythic_edge_parser/app/evidence_ledger.py` describes provenance,
  confidence, finality, degradation, drift, and review expectations.
- Card identity names, collection ownership, imported decklist alignment,
  active deck identity, sideboard deltas, sideboard-plan quality, matchup-plan
  analytics, card-performance analytics, archetype classification, workbook
  formulas, dashboards, webhook transport, Apps Script, and AI output are
  downstream or separate surfaces. They must not become the source of
  submitted-deck card-content truth.

The ledger describes support for observed `grpId` card-list content. It does
not compute deck identity, prove a complete active deck state, name cards,
resolve card ownership, infer sideboard changes, infer matchup plans, infer
archetypes, or promote analytics interpretation into parser truth.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md

Future implementation files owned by this contract:

- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- docs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier4_submitted_deck_cards.md

Referenced but not silently owned:

- src/mythic_edge_parser/parsers/client_actions.py
- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/grp_id_candidates.py
- src/mythic_edge_parser/app/runner.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/sheet_schema.py
- tests/test_client_actions_parser.py
- tests/test_diagnostics.py
- tests/test_runtime_surfaces.py
- tests/test_grp_id_candidates.py
- tests/test_state.py

## Public Interface

This contract covers evidence-ledger metadata for existing parser and runtime
surfaces. It does not create a new runtime API.

Authorized ledger field:

| Ledger field | Entry ID | Meaning |
| --- | --- | --- |
| `submitted_deck_cards` | `tier4.submitted_deck_cards.submitted_deck_cards` | Observed normalized submitted mainboard and sideboard `grpId` list content from a submit-deck response. |

Authorized evidence facets inside the single entry:

| Facet | Existing surface | Contract status |
| --- | --- | --- |
| submitted mainboard list shape | `ClientActionEvent.payload["deck_cards"]` | Direct observed evidence path, no values in ledger. |
| submitted sideboard list shape | `ClientActionEvent.payload["sideboard_cards"]` | Direct observed evidence path, no values in ledger. |
| request context | `game_state_id`, `resp_id`, `request_id` | Provenance context only. |
| event timestamp | `event.metadata.timestamp` / runtime `submitted_at` | Provenance context only. |
| mainboard count | `len(deck_cards)` / runtime `mainboard_count` | Derived facet, not a separate issue #159 ledger field. |
| sideboard count | `len(sideboard_cards)` / runtime `sideboard_count` | Derived facet, not a separate issue #159 ledger field. |
| submitted-deck signature | `submitted_deck_signature(deck_cards, sideboard_cards)` | Derived facet, not a separate issue #159 ledger field. |

Fields not authorized as separate seed fields in issue #159:

- `submitted_deck_mainboard_count`
- `submitted_deck_sideboard_count`
- `submitted_deck_signature`
- `submitted_deck_timestamp`
- `submitted_deck_by_game`
- `submitted_deck_name`
- `submitted_deck_id`
- `decklist_identity`
- `sideboard_delta`

Required compatibility:

- Do not rename `submit_deck_resp`.
- Do not rename `deck_cards`.
- Do not rename `sideboard_cards`.
- Do not rename `game_state_id`, `resp_id`, or `request_id`.
- Do not change `submitted_deck_signature(...)`.
- Do not change runtime active submitted-deck artifact shape.
- Do not add workbook columns, webhook fields, Apps Script fields, parser
  events, or runtime status fields.

## Observed Current Behavior

Observed on `origin/codex/parser-reliability-intelligence` at
`b5aa1ea6b7c9d9a7cca7f7cc580bdf1acb39a24e`:

- Issue #151 seeded Tier 4 `sideboarding_and_deck_state` with
  `sideboarding_entered` and `submit_deck_seen`.
- Tier 4 `future_fields` still contains `submitted_deck_cards`.
- Tier 3 `future_fields` contains `deck_state`.
- `client_actions.try_parse(...)` recognizes `ClientMessageType_SubmitDeckResp`
  as specialized payload type `submit_deck_resp`.
- Specialized submit-deck payloads include:
  - `type == "submit_deck_resp"`
  - `deck_cards`
  - `sideboard_cards`
  - `game_state_id`
  - `resp_id`
  - `request_id`
  - `raw_client_action`
- `deck_cards` source precedence is:
  1. `submitDeckResp.deckCards`
  2. `submitDeckResp.deck.deckCards`
  3. `submitDeckResp.deck`
  4. `[]`
- `sideboard_cards` source precedence is:
  1. `submitDeckResp.sideboardCards`
  2. `submitDeckResp.deck.sideboardCards`
  3. `submitDeckResp.sideboard`
  4. `[]`
- Card-list normalization uses integer-list normalization. Malformed values
  are discarded by the normalizer.
- A truthy malformed direct source can block nested fallback and normalize to
  an empty list.
- Missing or malformed `submitDeckResp` normalizes both lists to `[]`.
- `state.py` uses submit-deck payloads to set `MatchSummary.submit_deck_seen`;
  it does not store submitted card lists on `MatchSummary`.
- `runner.py` can call `diagnostics.record_submitted_deck(...)` for
  `ClientAction` events with `type == "submit_deck_resp"`.
- `diagnostics.record_submitted_deck(...)` writes no active submitted-deck
  artifact when both normalized lists are empty.
- `diagnostics.record_submitted_deck(...)` can write a local
  `manasight_active_submitted_deck` artifact with `deck_cards`,
  `sideboard_cards`, `mainboard_count`, `sideboard_count`, `signature`,
  request context, match/game context, and timestamps.
- `diagnostics.submitted_deck_signature(...)` hashes JSON containing
  `deck_cards` and `sideboard_cards`, using compact separators, and returns
  the first 16 hex characters.
- `runtime_surfaces.py` normalizes active submitted-deck payloads and can keep
  `_ACTIVE_DECK_STATE` / `_MATCH_DECK_CONTEXTS` as local runtime state.
- `runtime_surfaces.py` can derive active deck profiles, matched collection
  deck candidates, card-name resolution status, missing-card reports, and
  collection summaries from runtime active-deck state.
- `grp_id_candidates.py` can load active submitted-deck artifacts or scan saved
  match logs for latest non-empty `submit_deck_resp` payloads, then use those
  `grpId` counters for review-oriented candidate reports.

Observed risks, not fixed by this issue:

- Submitted `grpId` lists can look like complete active deck truth, but this
  issue only maps observed submit-deck card-content evidence.
- Runtime active submitted-deck artifacts can look like source evidence, but
  they are local derived snapshots.
- Counts and signatures can look like separate durable facts, but in issue
  #159 they are only derived facets of `submitted_deck_cards`.
- A single submit-deck payload can be latest-observed without proving every
  game-specific deck state in the match.
- Empty or malformed lists can still support `submit_deck_seen` from #151, but
  they cannot support card-content truth.

## Scope Decision

Codex C should implement issue #159 as a Tier 4
`sideboarding_and_deck_state` metadata slice in the existing evidence ledger.

Required family metadata:

- Keep Tier 4 `sideboarding_and_deck_state.status` as `seeded_sample`.
- Add `submitted_deck_cards` to Tier 4 `seed_fields`.
- Remove `submitted_deck_cards` from Tier 4 `future_fields`.
- Keep Tier 3 `deck_state` deferred.
- Preserve prior Tier 4 `sideboarding_entered` and `submit_deck_seen` entries.
- Preserve all prior Tier 1 and Tier 3 seed fields and entries.
- Add notes stating that issue #159 maps card-content provenance only and does
  not change submit-deck parsing, card-list normalization, runtime artifact
  writes, runtime status fields, GRP candidate scoring, workbook sync,
  diagnostics behavior, replay behavior, drift behavior, analytics behavior,
  or field-evidence attachment behavior.

Required Tier 4 entry:

| Entry ID | Output field | Display name | Source label |
| --- | --- | --- | --- |
| `tier4.submitted_deck_cards.submitted_deck_cards` | `submitted_deck_cards` | `Submitted Deck Cards` | `observed` |

Do not add separate ledger entries for `mainboard_count`, `sideboard_count`,
`signature`, `submitted_at`, deck names, deck IDs, decklist alignment,
sideboard deltas, card names, archetypes, sideboarding advice, gameplay advice,
or AI/model output.

## Required Submitted-Deck Card Semantics

`submitted_deck_cards`:

- Means the parser observed normalized submitted card-list content from a
  `ClientAction` event with `type == "submit_deck_resp"`.
- Covers both top-level normalized `deck_cards` and `sideboard_cards`.
- Requires at least one non-empty normalized list to support card-content
  truth.
- Is event-scoped evidence first. Runtime active-deck state is latest-observed
  local derived state, not proof of per-game deck state.
- May describe derived mainboard count, sideboard count, and signature as
  facets of the observed lists.
- Does not mean every card ID has been resolved to a card name.
- Does not mean the submitted deck has been matched to a named decklist.
- Does not mean the active deck state is complete for every game.
- Does not mean sideboard changes or sideboard deltas are known.
- Does not mean sideboarding was strategically correct.
- Does not mean the deck archetype, matchup plan, gameplay advice, or player
  mistake label can be inferred.

For empty or malformed lists:

- `submit_deck_seen` from #151 can remain supported by the submit-deck signal.
- `submitted_deck_cards` must be unknown or degraded.
- Runtime active submitted-deck artifacts should not be treated as present when
  `diagnostics.record_submitted_deck(...)` returns `None`.

For repeated submit-deck payloads:

- The direct parser event remains event-scoped.
- Runtime active submitted-deck surfaces may represent the latest observed
  non-empty payload.
- The ledger must not claim per-game or final deck-state truth from a latest
  observed runtime snapshot.
- Any future runtime field-evidence attachment must preserve event timestamp,
  request context, and source surface before comparing repeated payloads.

## Source Evidence Priority

`submitted_deck_cards` evidence priority:

1. `ClientAction` specialized payload with `type == "submit_deck_resp"` and a
   non-empty normalized `deck_cards` or `sideboard_cards` list.
2. `ClientAction` raw preserved payload paths for
   `raw_client_action.payload.submitDeckResp.deckCards`,
   `raw_client_action.payload.submitDeckResp.deck.deckCards`,
   `raw_client_action.payload.submitDeckResp.sideboardCards`, and
   `raw_client_action.payload.submitDeckResp.deck.sideboardCards`, path-only
   and review-only.
3. Request context from `game_state_id`, `resp_id`, and `request_id` as
   provenance context only.
4. Event timestamp and parser match/game context as provenance context only.
5. `diagnostics._submitted_deck_payload(...)` / active submitted-deck artifact
   paths as derived fallback evidence only.
6. `runtime_surfaces._normalize_active_deck_payload(...)` and
   `_ACTIVE_DECK_STATE` paths as derived fallback evidence only.
7. `grp_id_candidates.SubmittedDeckSnapshot` paths as downstream review
   evidence only.

Forbidden evidence for this entry:

- `MatchSummary.submit_deck_seen` as card-content truth
- `MTGA Submit Deck Seen` row value as card-content truth
- `sideboarding_entered`
- `Pre / Postboard`
- deck collection names, deck IDs, or deck formats
- imported decklist alignment
- sideboard deltas
- card-name resolution
- collection ownership
- GRP candidate scores
- mana signatures or card fingerprints
- card-performance analytics
- matchup plans
- archetype labels
- workbook formulas
- Apps Script code
- webhook delivery success
- diagnostics pass/fail labels
- golden replay status
- OpenAI/model-provider output
- AI or analytics interpretation

## Entry Metadata Requirements

The entry must satisfy the existing schema required fields and use privacy
class `path_only_no_values` for all direct and fallback evidence signals.

Recommended entry details:

| Field | Value |
| --- | --- |
| `entry_id` | `tier4.submitted_deck_cards.submitted_deck_cards` |
| `tier` | `4` |
| `output_family` | `sideboarding_and_deck_state` |
| `output_field` | `submitted_deck_cards` |
| `display_name` | `Submitted Deck Cards` |
| `coverage_status` | `seeded_sample` |
| `parser_owner` | `src/mythic_edge_parser/parsers/client_actions.py` |
| `model_surface` | `ClientActionEvent.payload.deck_cards + ClientActionEvent.payload.sideboard_cards` |
| `downstream_surfaces` | `active_submitted_deck_artifact`, `runtime_active_deck_state`, `active_deck_profile`, `grp_id_candidate_report`, `runtime_status_counts` |
| `parser_managed_truth` | `true` |

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

- `direct`: `high` when a specialized `submit_deck_resp` payload contains a
  non-empty normalized `deck_cards` or `sideboard_cards` list.
- `derived_count_or_signature`: `medium` when counts or signature are derived
  from the observed normalized lists.
- `runtime_snapshot`: `medium` when a local active submitted-deck artifact or
  runtime active-deck state is used as a derived latest-observed snapshot.
- `raw_payload_review`: `low` when only raw preserved payload paths are being
  reviewed and top-level normalized lists are empty or unavailable.
- `missing`: `unknown`.
- `contradiction`: `low` and review-required.

Recommended `finality_policy`:

- `live`: parsed submit-deck event observed during active parsing.
- `provisional`: active submitted-deck runtime artifact or runtime surface
  latest-observed snapshot.
- `final`: event-scoped evidence preserved in a saved event/log row or future
  field-evidence record. This is not final deck-state truth.
- `reconciled`: only if a later evidence-ledger slice attaches stronger
  source evidence to an existing final field-evidence record.

The implementation does not need runtime field-evidence attachment in issue
#159. The policies above are entry metadata for future consumers.

## Invariants

Required invariant names for `submitted_deck_cards`:

- `submitted_deck_cards_requires_submit_deck_resp_event`
- `submitted_deck_cards_requires_non_empty_normalized_card_list`
- `submitted_deck_cards_uses_deck_cards_and_sideboard_cards_paths`
- `submitted_deck_cards_preserves_request_context_as_provenance_only`
- `submitted_deck_cards_counts_and_signature_are_derived_facets_only`
- `submitted_deck_cards_runtime_artifacts_are_derived_fallbacks_only`
- `submitted_deck_cards_empty_or_malformed_lists_are_unknown_or_degraded`
- `submitted_deck_cards_not_submit_deck_seen_boolean_truth`
- `submitted_deck_cards_not_sideboarding_or_pre_postboard_truth`
- `submitted_deck_cards_not_deck_state_or_deck_identity_truth`
- `submitted_deck_cards_not_sideboard_delta_or_plan_quality_truth`
- `submitted_deck_cards_not_card_name_or_collection_ownership_truth`
- `submitted_deck_cards_not_archetype_matchup_plan_gameplay_advice_or_ai_truth`
- `submitted_deck_cards_privacy_path_only_no_values`

Shared invariants:

- Ledger entries must not include raw private log excerpts.
- Ledger entries must not include raw submitted card IDs or raw payload values.
- Ledger entries must not include local active-deck artifact contents.
- Ledger entries must not add workbook, webhook, Apps Script, runtime status,
  failed-post, generated-data, export, or model-provider side effects.
- Ledger entries must not change parser-owned submit-deck behavior.

## Degradation Behavior

The entry must document degradation behavior for:

- no `ClientAction` event because the raw log line is malformed or unrouted
- parsed `ClientAction` event whose `type` is not `submit_deck_resp`
- `submit_deck_resp` with both `deck_cards` and `sideboard_cards` empty
- missing or malformed `submitDeckResp`
- truthy malformed direct source blocking nested fallback and normalizing to
  empty lists
- non-list, boolean, object, or otherwise malformed card-list values discarded
  by integer-list normalization
- raw preserved payload paths present but top-level normalized lists empty
- local active submitted-deck artifact missing because both lists were empty
- runtime active-deck snapshot present but disconnected from a source event row
  or current match context
- repeated submit-deck payloads where the latest-observed snapshot differs from
  earlier event-scoped evidence
- mismatch between parser event lists, active submitted-deck artifact counts,
  runtime active-deck state, and GRP candidate snapshot
- source log truncation, summarization, rotation, or unrouted evidence hiding a
  submit-deck payload
- card IDs unresolved to names
- downstream decklist matching or GRP candidate scoring disagreeing with
  submitted `grpId` evidence

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

- Use repo-relative paths, symbolic payload paths, list-shape descriptions, or
  field names only.
- Do not include raw `Player.log` lines.
- Do not include raw `raw_client_action` payload values.
- Do not include real submitted deck card IDs.
- Do not include raw decklists.
- Do not include local active submitted-deck artifact contents.
- Do not include local runtime status file contents.
- Do not include deck names, deck IDs, decklist names, collection contents,
  card names, or card ownership data.
- Do not include secrets, tokens, webhook URLs, environment variable values,
  failed post bodies, generated data, workbook exports, private diagnostics
  artifacts, or model-provider data.
- Use `path_only_no_values` for all evidence signals.

Synthetic example IDs in existing tests may remain in tests that already cover
parser behavior, but Codex C should not add raw private payload fixtures for
this metadata-only ledger slice.

## Compatibility Expectations

Codex C must preserve:

- existing `client_actions.py` parser behavior
- existing `deck_cards` and `sideboard_cards` normalization behavior
- existing `submit_deck_resp` payload shape
- existing `state.py` `submit_deck_seen` behavior
- existing `diagnostics.record_submitted_deck(...)` write behavior
- existing `diagnostics.submitted_deck_signature(...)` behavior
- existing `runtime_surfaces.py` active-deck normalization and artifact
  behavior
- existing `grp_id_candidates.py` scan/load/resolve behavior
- existing workbook, webhook, Apps Script, runtime status, output transport,
  diagnostics, golden replay, feature-equity, drift, and analytics behavior
- all prior evidence-ledger entries and tests

Codex C must not:

- add separate top-level count or signature fields in issue #159
- change submit-deck parser source precedence
- change malformed-list fallback behavior
- change runtime artifact write conditions
- write new runtime status fields
- attach runtime field-evidence records
- infer sideboard deltas, deck identity, decklist alignment, card names,
  archetypes, matchup plans, gameplay advice, or AI truth
- use workbook formulas, Apps Script, webhook transport, dashboards, analytics,
  or AI output as parser truth

## Test Obligations For Codex C

Focused tests in `tests/test_evidence_ledger.py` should prove:

- Tier 4 `sideboarding_and_deck_state` remains `seeded_sample`.
- Tier 4 `seed_fields` include `sideboarding_entered`, `submit_deck_seen`, and
  `submitted_deck_cards`.
- Tier 4 `future_fields` no longer include `submitted_deck_cards`.
- Tier 3 `future_fields` still include `deck_state`.
- Existing #151 Tier 4 signal entries remain present.
- Entry `tier4.submitted_deck_cards.submitted_deck_cards` exists and validates.
- The submitted-deck entry uses parser owner
  `src/mythic_edge_parser/parsers/client_actions.py`.
- Direct evidence documents `submit_deck_resp`, `payload.deck_cards`,
  `payload.sideboard_cards`, and request-context paths.
- Fallback evidence documents raw preserved submit-deck payload paths as
  path-only review evidence.
- Fallback evidence documents active submitted-deck artifact, runtime active
  deck state, and GRP candidate snapshot only as derived/downstream fallback
  surfaces.
- The entry uses `value_source_policy` with direct `observed`, fallback
  `derived`, missing `unknown`, and contradiction `conflict`.
- The entry documents counts and signature as derived facets only, not
  separate ledger fields.
- The entry documents repeated submit-deck payload semantics as event-scoped
  direct evidence plus latest-observed runtime fallback.
- The entry documents empty/malformed lists as unknown or degraded card-content
  evidence while preserving #151 `submit_deck_seen` semantics.
- The entry rejects sideboard deltas, deck names, deck IDs, decklist identity,
  card names, collection ownership, GRP scoring, pre/postboard labels,
  sideboarding signals, workbook formulas, Apps Script, analytics, and AI truth
  as evidence.
- All direct and fallback evidence signals use `path_only_no_values`.
- No raw private log text, raw payload values, real card IDs, local runtime
  artifacts, secrets, or generated data are serialized into the ledger.
- Prior Tier 1, Tier 3, and #151 Tier 4 entries remain present and validating.

Optional existing-behavior tests may be inspected but should not require code
changes:

- `tests/test_client_actions_parser.py`
- `tests/test_diagnostics.py`
- `tests/test_runtime_surfaces.py`
- `tests/test_grp_id_candidates.py`
- `tests/test_state.py`

Expected implementation validation:

```bash
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m ruff check src tests tools
```

Optional adjacent validation if Codex C touches or suspects adjacent behavior:

```bash
python3 -m pytest -q tests/test_client_actions_parser.py tests/test_diagnostics.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py
```

Documentation-only validation for this contract:

```bash
git diff --check
```

## Acceptance Criteria

- `docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md`
  exists and is committed in the module PR.
- The contract authorizes exactly one new Tier 4 ledger field:
  `submitted_deck_cards`.
- The contract explicitly keeps counts and signature as derived facets inside
  the `submitted_deck_cards` entry, not separate fields.
- The contract clearly states that submitted `grpId` lists are observed
  parser payload content, not deck-state truth.
- The contract clearly rejects deck-state, sideboard deltas, deck names, deck
  IDs, decklist identity, card names, archetype labels, matchup plans,
  sideboard quality, gameplay advice, player-mistake labels, and
  AI/model-provider truth.
- Codex C is routed to update only evidence-ledger metadata, focused tests,
  and the implementation handoff.
- No parser behavior or protected downstream surface is changed by the
  contract writer pass.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #159, Tier 4 submitted-deck card-content provenance under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/159
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/151
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/157
- Previous merge commit: b5aa1ea6b7c9d9a7cca7f7cc580bdf1acb39a24e
- Base branch: codex/parser-reliability-intelligence
- Contract: docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md
- Expected handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md

Goal:
Compare the current evidence-ledger implementation and focused tests against the Tier 4 submitted-deck card-content contract. Implement only the smallest coherent metadata and test changes needed to satisfy the contract.

Do:
- Verify you are working from codex/parser-reliability-intelligence, not main.
- Read AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, docs/agent_threads/implementation.md, and the contract.
- Update src/mythic_edge_parser/app/evidence_ledger.py so Tier 4 sideboarding_and_deck_state seeds submitted_deck_cards in addition to sideboarding_entered and submit_deck_seen.
- Add entry tier4.submitted_deck_cards.submitted_deck_cards.
- Keep counts and signature as derived facets inside the submitted_deck_cards entry; do not create separate top-level count/signature ledger fields.
- Remove submitted_deck_cards from Tier 4 future_fields.
- Keep Tier 3 deck_state deferred.
- Preserve the #151 sideboarding_entered and submit_deck_seen entries.
- Add focused tests in tests/test_evidence_ledger.py for family metadata, entry shape, direct/fallback evidence, value-source policy, confidence/finality policy, degradation behavior, privacy, derived count/signature facet boundaries, repeated payload semantics, and protected truth boundaries.
- Produce docs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md with comparison, files changed, validation, open risks, and next recommended role.

Do not:
- Change parser behavior, submit-deck parsing behavior, card-list normalization behavior, runtime artifact write behavior, GRP candidate scoring, parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, OpenAI/model-provider behavior, or AI/analytics truth.
- Add separate top-level count/signature fields, runtime field-evidence attachment, sideboard deltas, deck names, deck IDs, decklist identity, archetype labels, matchup plans, card-performance analytics, gameplay advice, player-mistake labels, card-name truth, collection ownership truth, or model-provider behavior.
- Commit raw private Player.log excerpts, raw submitted-deck payloads, raw decklists, local runtime active-deck artifacts, failed posts, runtime status files, workbook exports, API keys, tokens, credentials, webhook URLs, real submitted card IDs, or generated data.
- Target main directly.
- Close issue #11.
- Stage or commit unless explicitly asked.

Validation:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m ruff check src tests tools
- Optional if adjacent behavior is touched or suspected: python3 -m pytest -q tests/test_client_actions_parser.py tests/test_diagnostics.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/159"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/151"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/157"
  previous_merge_commit: "b5aa1ea6b7c9d9a7cca7f7cc580bdf1acb39a24e"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md"
  verdict: "tier4_submitted_deck_card_content_contract_ready_for_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier4-submitted-deck-cards"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not close issue #11."
    - "Do not target main directly."
    - "Do not change parser behavior, submit-deck parsing behavior, card-list normalization behavior, runtime artifact write behavior, GRP candidate scoring, parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, OpenAI/model-provider behavior, or AI/analytics truth."
    - "Do not add separate top-level count/signature fields, runtime field-evidence attachment, sideboard deltas, deck names, deck IDs, decklist identity, archetype labels, matchup plans, card-performance analytics, gameplay advice, player-mistake labels, card-name truth, collection ownership truth, or model-provider behavior."
    - "Do not commit raw private Player.log excerpts, raw submitted-deck payloads, raw decklists, local runtime active-deck artifacts, failed posts, runtime status files, workbook exports, API keys, tokens, credentials, webhook URLs, real submitted card IDs, or generated data."
```
