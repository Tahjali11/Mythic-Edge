# Player.log Evidence Ledger Tier 4 Submitted-Deck Cards Comparison

## Metadata

- role: Codex C / Module Implementer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/159
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/151
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/157
- previous_merge_commit: b5aa1ea6b7c9d9a7cca7f7cc580bdf1acb39a24e
- source_artifact: docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md
- target_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier4-submitted-deck-cards
- risk_tier: High
- branch_check: `HEAD b5aa1ea`, `HEAD...origin/codex/parser-reliability-intelligence` = `0 0`

## Summary

The current parser/runtime behavior already matched the contract's observed-behavior section. This pass changed only
evidence-ledger metadata and focused ledger tests.

`submitted_deck_cards` is now a Tier 4 seeded evidence-ledger field. Counts and submitted-deck signature are documented
only as derived facets inside that single entry, not as separate top-level ledger fields.

## Confirmed Matches

- `client_actions.py` already emits `submit_deck_resp` with normalized `deck_cards`, `sideboard_cards`,
  `game_state_id`, `resp_id`, `request_id`, and `raw_client_action`.
- Existing source precedence and malformed-list normalization behavior remains unchanged.
- Existing #151 `sideboarding_entered` and `submit_deck_seen` entries remain present and validating.
- Tier 3 still defers broad `deck_state`.
- Diagnostics, runtime surfaces, and GRP candidate surfaces already exist as downstream/derived consumers.

## Contract Mismatches Fixed

- Tier 4 `sideboarding_and_deck_state.seed_fields` did not include `submitted_deck_cards`; it now does.
- Tier 4 `future_fields` still listed `submitted_deck_cards`; it is now empty.
- The ledger did not have `tier4.submitted_deck_cards.submitted_deck_cards`; it now exists and validates.
- Focused tests still treated submitted deck card contents as deferred; they now verify the new seeded metadata slice.

## Changes Made

- Updated `src/mythic_edge_parser/app/evidence_ledger.py`.
  - Added `submitted_deck_cards` to Tier 4 seed fields.
  - Added `tier4.submitted_deck_cards.submitted_deck_cards`.
  - Documented direct observed evidence from `submit_deck_resp`, `payload.deck_cards`, `payload.sideboard_cards`,
    request context, and event timestamp context.
  - Documented raw preserved payload paths, diagnostics active submitted-deck artifact, counts/signature, runtime active
    deck state, and GRP candidate snapshot only as derived or downstream fallback evidence.
  - Documented empty/malformed lists, repeated payloads, runtime fallback semantics, privacy, and protected truth
    boundaries.
- Updated `tests/test_evidence_ledger.py`.
  - Added focused coverage for Tier 4 seed/future metadata.
  - Added focused coverage for the submitted-deck cards entry shape, evidence signals, policy metadata, derived facets,
    repeated payload semantics, degradation behavior, privacy, and downstream truth rejections.
  - Updated the local artifact marker check to permit the contract-authorized symbolic surface label
    `runtime_status_counts` while still rejecting local status-file markers.

## Boundaries Preserved

- No parser behavior changed.
- No submit-deck parsing behavior or card-list normalization behavior changed.
- No runtime artifact write behavior changed.
- No GRP candidate scoring changed.
- No parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication,
  workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, environment variables,
  raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior,
  OpenAI/model-provider behavior, or AI/analytics truth changed.
- No separate top-level count/signature fields were added.
- No runtime field-evidence attachment, sideboard deltas, deck names, deck IDs, decklist identity, archetype labels,
  matchup plans, card-performance analytics, gameplay advice, player-mistake labels, card-name truth, collection
  ownership truth, or model-provider behavior was added.
- No raw private Player.log excerpts, raw submitted-deck payloads, raw decklists, local runtime active-deck artifacts,
  failed posts, runtime status files, workbook exports, API keys, tokens, credentials, webhook URLs, real submitted
  card IDs, or generated data were committed.

## Validation Evidence

- `python3 -m pytest -q tests/test_evidence_ledger.py`
  - result: passed, `68 passed`
- `python3 -m pytest -q tests/test_client_actions_parser.py tests/test_diagnostics.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py`
  - result: passed, `79 passed`
- `python3 -m pytest -q`
  - result: passed, `927 passed`
- `python3 -m ruff check src tests tools`
  - result: passed
- `git diff --check`
  - result: passed
- `python3 tools/check_protected_surfaces.py --base origin/main`
  - result: passed, `forbidden: 0`, `warnings: 12`
  - note: warnings are existing integration-branch protected-surface warnings relative to `origin/main`; this pass touched
    only `evidence_ledger.py`, `test_evidence_ledger.py`, and this handoff.

## Open Risks

- CI was not run in this local Codex C pass.
- Runtime field-evidence attachment remains out of scope.
- Counts/signature are metadata facets only; no runtime field or top-level ledger field exists for them.
- Broad deck-state, sideboard deltas, deck identity, card names, decklist alignment, collection ownership, archetypes,
  gameplay advice, and AI/model-provider interpretation remain deferred.
- The contract source artifact is currently untracked in this worktree and should be included by submitter if review
  passes.

## Next Recommended Role

Next role: Codex E / Module Reviewer in contract-test mode.

Use Codex D only if Codex E finds a concrete blocker. Use Codex F only after review passes.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #159, Tier 4 submitted-deck card-content provenance under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/159
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/151
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/157
- Previous merge commit: b5aa1ea6b7c9d9a7cca7f7cc580bdf1acb39a24e
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier4-submitted-deck-cards
- Contract: docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md
- Handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md

Use:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md
- docs/contracts/player_log_evidence_ledger_tier4_sideboarding_submit_deck.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/parsers/client_actions.py
- src/mythic_edge_parser/app/diagnostics.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- src/mythic_edge_parser/app/grp_id_candidates.py
- tests/test_client_actions_parser.py
- tests/test_diagnostics.py
- tests/test_runtime_surfaces.py
- tests/test_grp_id_candidates.py

Goal:
Verify the Codex C implementation against the Tier 4 submitted-deck card-content provenance contract.

Confirm:
- Tier 4 sideboarding_and_deck_state remains seeded_sample.
- Tier 4 seed_fields include sideboarding_entered, submit_deck_seen, and submitted_deck_cards.
- Tier 4 future_fields no longer include submitted_deck_cards.
- Tier 3 future_fields still include deck_state.
- Existing #151 sideboarding_entered and submit_deck_seen entries remain present.
- Entry tier4.submitted_deck_cards.submitted_deck_cards exists and validates.
- The submitted-deck entry uses parser owner src/mythic_edge_parser/parsers/client_actions.py.
- Direct evidence documents submit_deck_resp, payload.deck_cards, payload.sideboard_cards, request context, and timestamp context.
- Fallback evidence documents raw preserved payload paths, active submitted-deck artifact, runtime active deck state, and GRP candidate snapshot only as derived/downstream fallback surfaces.
- Value-source policy is direct observed, fallback derived, missing unknown, contradiction conflict.
- Counts and signature are derived facets inside submitted_deck_cards, not separate top-level ledger fields.
- Repeated payload semantics are event-scoped direct evidence plus latest-observed runtime fallback.
- Empty/malformed lists are unknown or degraded card-content evidence while #151 submit_deck_seen semantics remain preserved.
- The entry rejects sideboard deltas, deck names, deck IDs, decklist identity, card names, collection ownership, GRP scoring, pre/postboard labels, sideboarding signals, workbook formulas, Apps Script, analytics, and AI truth as evidence.
- All direct/fallback evidence signals use path_only_no_values.
- No parser behavior, submit-deck parsing behavior, card-list normalization behavior, runtime artifact write behavior, GRP candidate scoring, parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, OpenAI/model-provider behavior, or AI/analytics truth changed.

Validation:
Run:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_client_actions_parser.py tests/test_diagnostics.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py
- python3 -m ruff check src tests tools
- git diff --check

If feasible, run:
- python3 -m pytest -q
- python3 tools/check_protected_surfaces.py --base origin/main

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F if no blocking findings, otherwise Codex D or Codex B.
- workflow_handoff block.

Do not:
- Change code in review-only mode.
- Change parser behavior, submit-deck parsing behavior, card-list normalization behavior, runtime artifact write behavior, GRP candidate scoring, parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, OpenAI/model-provider behavior, or AI/analytics truth.
- Stage, commit, push, merge, close issue #11, close issue #159, or target main.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/159"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/151"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/157"
  previous_merge_commit: "b5aa1ea6b7c9d9a7cca7f7cc580bdf1acb39a24e"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md"
  verdict: "tier4_submitted_deck_card_content_metadata_ready_for_contract_review"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier4-submitted-deck-cards"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py - passed, 68 passed"
    - "python3 -m pytest -q tests/test_client_actions_parser.py tests/test_diagnostics.py tests/test_runtime_surfaces.py tests/test_grp_id_candidates.py - passed, 79 passed"
    - "python3 -m pytest -q - passed, 927 passed"
    - "python3 -m ruff check src tests tools - passed"
    - "git diff --check - passed"
    - "python3 tools/check_protected_surfaces.py --base origin/main - passed, forbidden 0, warnings 12"
  changed_files:
    - "src/mythic_edge_parser/app/evidence_ledger.py"
    - "tests/test_evidence_ledger.py"
    - "docs/implementation_handoffs/player_log_evidence_ledger_tier4_submitted_deck_cards_comparison.md"
  stop_conditions:
    - "Do not close issue #11."
    - "Do not target main directly."
    - "Do not change parser behavior, submit-deck parsing behavior, card-list normalization behavior, runtime artifact write behavior, GRP candidate scoring, parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, OpenAI/model-provider behavior, or AI/analytics truth."
    - "Do not add separate top-level count/signature fields, runtime field-evidence attachment, sideboard deltas, deck names, deck IDs, decklist identity, archetype labels, matchup plans, card-performance analytics, gameplay advice, player-mistake labels, card-name truth, collection ownership truth, or model-provider behavior."
    - "Do not commit raw private Player.log excerpts, raw submitted-deck payloads, raw decklists, local runtime active-deck artifacts, failed posts, runtime status files, workbook exports, API keys, tokens, credentials, webhook URLs, real submitted card IDs, or generated data."
```
