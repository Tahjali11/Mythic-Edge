# Player.log Evidence Ledger Tier 5 Card Identity Comparison

## Metadata

- role: Codex C / Module Implementer; Codex D / Module Fixer follow-up
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/163
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- source_artifact: docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- target_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier5_card_identity_comparison.md
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier5-card-identity
- latest_verified_remote_commit: 2a96d5701f6939fd7a78d71383c35d43095d69c0
- risk_tier: High
- branch_check: `HEAD 2a96d57`, `HEAD...origin/codex/parser-reliability-intelligence` = `0 0`

## Summary

The current parser, gameplay-action, opponent-observation, catalog, and runtime behavior already matched the
contract's behavior boundary. Codex C changed only evidence-ledger metadata and focused ledger tests. Codex D
followed up on the Codex E metadata blocker without changing runtime behavior.

Tier 5 `card_identity_and_gameplay_actions` is now a `seeded_sample` family with exactly one seed field:
`grp_id`. Gameplay-action provenance and opponent-card-observation provenance remain future Tier 5 work.
The `opponent_card_observation.grp_id` evidence metadata now preserves observed/high and derived/medium
source-confidence paths instead of collapsing opponent observations to fixed `derived`/`medium`.

## Confirmed Matches

- `gameplay_actions.py` already normalizes GameState object identity into `grp_id`, `observed_grp_id`,
  `overlay_grp_id`, `object_source_grp_id`, `parent_id`, and `identity_hint_source`.
- Existing canonical `grp_id` selection already distinguishes direct object identity from object-source, parent,
  prior-instance, replacement-chain, and overlay fallback context.
- `opponent_card_observations.py` already carries `grp_id`, raw/fallback ID fields, identity hint source,
  resolution status, visibility, confidence, value source, degradation flags, and review-required status.
- `grp_id_catalog.py`, `card_catalog.py`, and `grp_id_candidates.py` already own enrichment, display, candidate,
  contradiction, layout, and card-face metadata outside parser truth.
- Tier 4 `submitted_deck_cards` remains observed submitted `grpId` list-content provenance only.
- Tier 3 opening-hand entries remain path-only provenance dependencies and are not redefined by Tier 5.
- Tier 4 deck-state boundary notes from issue #161 remain preserved.

## Contract Mismatches Fixed

- Tier 5 `card_identity_and_gameplay_actions.status` was `registered_future`; it is now `seeded_sample`.
- Tier 5 `seed_fields` was empty; it is now exactly `["grp_id"]`.
- Tier 5 `future_fields` included `grp_id`; it now keeps only `gameplay_action` and
  `opponent_card_observation`.
- The ledger did not have `tier5.card_identity.grp_id`; it now exists and validates.
- Focused tests did not pin the Tier 5 seed boundary, evidence paths, policies, degradation language, or
  non-truth boundaries; they now do.
- Codex E found that `opponent_card_observation.grp_id` collapsed source/confidence metadata to fixed
  `derived`/`medium`; Codex D fixed the metadata to document observed/high preservation and derived/medium
  visible-action preservation.
- Focused tests did not assert the opponent-observation source/confidence mirror semantics; Codex D added
  regression coverage that fails if the metadata collapses back to fixed `derived`/`medium`.

## Changes Made

- Updated `src/mythic_edge_parser/app/evidence_ledger.py`.
  - Changed Tier 5 family metadata to `seeded_sample`.
  - Added exactly one Tier 5 seed field, `grp_id`.
  - Preserved `gameplay_action` and `opponent_card_observation` as future fields.
  - Added `tier5.card_identity.grp_id`.
  - Documented direct evidence from GameState object `grpId`, direct gameplay-action canonical `grp_id`, and
    opponent-card observation `grp_id` context.
  - Updated opponent-card observation direct evidence so observed gameplay-action source keeps `observed` and
    `high`, while derived visible-action evidence keeps `derived` and `medium` with visibility/degradation
    context.
  - Documented fallback and enrichment context for `object_source_grp_id`, `overlay_grp_id`, parent chain,
    prior-instance, replacement chain, submitted `grpId` lists, opening-hand resolution paths, GRP catalog lookup,
    active deck display context, and GRP candidate review context.
  - Documented value-source, confidence, finality, invariant, degradation, drift, privacy, and protected truth
    boundaries for the single `grp_id` entry.
- Updated `tests/test_evidence_ledger.py`.
  - Added Tier 5 contracted field, entry, deferred-field, and forbidden-seed constants.
  - Updated exact family status expectations and exact entry-set expectations.
  - Added focused tests for Tier 5 family seed scope.
  - Added focused tests for the `grp_id` entry shape, direct/fallback evidence paths, policies, degradation,
    privacy, and protected boundaries.
  - Added focused regression coverage for opponent-card-observation source/confidence mirroring so metadata cannot
    collapse to fixed `derived`/`medium`.
  - Added coverage proving Tier 3 opening-hand, Tier 4 submitted-deck cards, and Tier 4 deck-state boundaries
    remain intact.

## Boundaries Preserved

- No parser behavior changed.
- No card identity parsing behavior, GRP normalization behavior, gameplay action behavior, opponent-card observation
  behavior, parser state final reconciliation, parser event classes, router behavior, match/game identity,
  deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets,
  environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production
  behavior, OpenAI/model-provider behavior, or AI/analytics truth changed.
- No runtime field-evidence attachment was added.
- No card-name truth, card ownership truth, decklist identity, archetype labels, matchup plans, card-performance
  analytics, gameplay advice, player-mistake labels, or model-provider behavior was added.
- No raw private Player.log excerpts, raw payloads, local runtime artifacts, failed posts, runtime status files,
  workbook exports, API keys, tokens, credentials, webhook URLs, real private card lists, or generated data were
  committed.

## Validation Evidence

- `python3 -m pytest -q tests/test_evidence_ledger.py`
  - Codex C result: passed, `76 passed`
  - Codex D result: passed, `77 passed`
- `python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_grp_id_catalog.py tests/test_card_catalog.py`
  - Codex D result: passed, `47 passed`
- `python3 -m ruff check src tests tools`
  - Codex D result: passed, `All checks passed!`
- `git diff --check`
  - Codex D result: passed
- `printf '<changed paths>' | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin`
  - Codex D result: passed, `changed_paths: 5`, `forbidden: 0`, `warnings: 0`
- `python3 -m pytest -q`
  - Codex D result: passed, `936 passed`

## Open Risks

- CI was not run in the local Codex C or Codex D passes.
- Future Tier 5 gameplay-action provenance and opponent-card-observation provenance remain deferred.
- Future card-name, display-label, resolution-status, catalog, deck identity, collection ownership, sideboard-delta,
  analytics, and AI boundaries still require separate contracts before any seed fields or behavior changes.
- The contract source artifact is untracked in this worktree and should be included by submitter if review passes.

## Next Recommended Role

Next role: Codex E / Module Reviewer in contract-test mode.

Use Codex D only if Codex E finds a concrete blocker. Use Codex F only after review passes.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #163, Tier 5 card identity provenance under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/163
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier5-card-identity
- Contract: docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- Handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier5_card_identity_comparison.md
- Latest verified remote commit: 2a96d5701f6939fd7a78d71383c35d43095d69c0

Use:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/player_log_evidence_ledger_tier5_card_identity.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger_tier4_deck_state_boundary.md
- docs/contracts/player_log_evidence_ledger_tier4_submitted_deck_cards.md
- docs/contracts/player_log_evidence_ledger_tier3_opening_hand.md
- docs/contracts/parser_opponent_card_observations.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier5_card_identity_comparison.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/app/gameplay_actions.py
- src/mythic_edge_parser/app/opponent_card_observations.py
- src/mythic_edge_parser/app/grp_id_catalog.py
- src/mythic_edge_parser/app/card_catalog.py
- src/mythic_edge_parser/app/grp_id_candidates.py
- tests/test_gameplay_actions.py
- tests/test_opponent_card_observations.py
- tests/test_grp_id_catalog.py
- tests/test_card_catalog.py

Goal:
Verify the Codex C implementation against the Tier 5 card identity provenance contract.
Also verify the Codex D fixer pass for the Codex E blocker: opponent-card-observation `grp_id` metadata must
preserve observed/high and derived/medium source-confidence semantics instead of collapsing to fixed
`derived`/`medium`.

Confirm:
- Branch is not main and is based on the verified integration commit.
- Tier 5 card_identity_and_gameplay_actions is seeded_sample.
- Tier 5 seed_fields is exactly ["grp_id"].
- Tier 5 future_fields keeps gameplay_action and opponent_card_observation.
- No separate Tier 5 seed fields were added for observed_grp_id, overlay_grp_id, object_source_grp_id, parent_id, instance_id, identity_hint_source, card_name, display_name, resolution_status, layout, card_faces, candidate_names, deck names, deck IDs, decklist identity, collection ownership, gameplay_action, opponent_card_observation, analytics, model-provider output, or AI.
- Entry tier5.card_identity.grp_id exists and validates.
- The grp_id entry uses parser owner src/mythic_edge_parser/app/gameplay_actions.py.
- Direct evidence documents GameState object grpId, direct canonical gameplay-action grp_id, and opponent-card observation grp_id context.
- Opponent-card-observation grp_id direct evidence preserves observed/high and derived/medium source-confidence
  paths using opponent observation value_source, confidence, visibility, and degradation context.
- Fallback evidence documents object-source ID, overlay ID, parent-chain ID, prior-instance ID, replacement-chain ID, submitted grpId lists, opening-hand resolution path context, GRP catalog enrichment, active deck display context, and GRP candidate review context.
- Catalog, active deck, local decklist, card-name, display-label, layout, card-face, and candidate information stays legacy_enriched/review context and not parser truth.
- Value-source, confidence, finality, degradation, drift, privacy, and invariant metadata match the contract.
- Tier 3 opening-hand, Tier 4 submitted-deck card-content, and Tier 4 deck-state boundary behavior remain unchanged.
- No parser behavior, card identity parsing behavior, GRP normalization behavior, gameplay action behavior, opponent-card observation behavior, parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, OpenAI/model-provider behavior, or AI/analytics truth changed.

Validation:
Run:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_grp_id_catalog.py tests/test_card_catalog.py
- python3 -m ruff check src tests tools
- git diff --check

If feasible, run:
- python3 -m pytest -q
- python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F if no blocking findings, otherwise Codex D or Codex B.
- workflow_handoff block.

Do not:
- Change code in review-only mode.
- Change parser behavior, card identity parsing behavior, GRP normalization behavior, gameplay action behavior, opponent-card observation behavior, parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, OpenAI/model-provider behavior, or AI/analytics truth.
- Stage, commit, push, merge, close issue #11, close issue #163, or target main.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/163"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/player_log_evidence_ledger_tier5_card_identity.md"
  target_artifact: "src/mythic_edge_parser/app/evidence_ledger.py; tests/test_evidence_ledger.py; docs/implementation_handoffs/player_log_evidence_ledger_tier5_card_identity_comparison.md"
  verdict: "fixer_pass_ready_for_module_reviewer"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier5-card-identity"
  latest_verified_remote_commit: "2a96d5701f6939fd7a78d71383c35d43095d69c0"
  authorized_seed_fields:
    - "grp_id"
  authorized_seed_entries:
    - "tier5.card_identity.grp_id"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py - passed, 77 passed"
    - "python3 -m pytest -q tests/test_gameplay_actions.py tests/test_opponent_card_observations.py tests/test_grp_id_catalog.py tests/test_card_catalog.py - passed, 47 passed"
    - "python3 -m ruff check src tests tools - passed"
    - "git diff --check - passed"
    - "printf '<changed paths>' | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin - passed, changed_paths 5, forbidden 0, warnings 0"
    - "python3 -m pytest -q - passed, 936 passed"
  changed_files:
    - "src/mythic_edge_parser/app/evidence_ledger.py"
    - "tests/test_evidence_ledger.py"
    - "docs/implementation_handoffs/player_log_evidence_ledger_tier5_card_identity_comparison.md"
  untracked_source_artifacts:
    - "docs/contracts/player_log_evidence_ledger_tier5_card_identity.md"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11 or issue #163."
    - "Do not change parser behavior, card identity parsing behavior, GRP normalization behavior, gameplay action behavior, opponent-card observation behavior, parser state final reconciliation, parser event classes, router behavior, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, OpenAI/model-provider behavior, or AI/analytics truth."
    - "Do not add runtime field-evidence attachment, card-name truth, card ownership truth, decklist identity, archetype labels, matchup plans, card-performance analytics, gameplay advice, player-mistake labels, or model-provider behavior."
    - "Do not commit raw private Player.log excerpts, raw payloads, local runtime artifacts, failed posts, runtime status files, workbook exports, API keys, tokens, credentials, webhook URLs, real private card lists, or generated data."
```
