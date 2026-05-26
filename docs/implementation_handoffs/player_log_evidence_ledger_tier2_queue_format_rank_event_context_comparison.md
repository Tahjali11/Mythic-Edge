# Player.log Evidence Ledger Tier 2 Queue / Format / Rank / Event-Context Comparison

## Metadata

- role: Codex C / Module Implementer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/167
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- source_artifact: docs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md
- target_artifact: docs/implementation_handoffs/player_log_evidence_ledger_tier2_queue_format_rank_event_context_comparison.md
- base_branch: codex/parser-reliability-intelligence
- implementation_branch: codex/player-log-evidence-ledger-tier2-context
- latest_verified_remote_commit: 9f625ea0ef31cdbaa97a827a95ba3b4808562d11
- risk_tier: Medium-High
- branch_check: `HEAD 9f625ea`, `HEAD...origin/codex/parser-reliability-intelligence` = `0 0`

## Summary

The current parser/state/model behavior already matched the contract's observed-behavior section. This pass changed
only evidence-ledger metadata and focused ledger tests.

Tier 2 `queue_format_rank_event_context` is now a `seeded_sample` family with exactly four seed fields:
`event_id`, `super_format`, `constructed_rank`, and `queue_type`.

## Confirmed Matches

- `match_state.py` already parses `event_id` from game-room config and falls back to player-level event IDs.
- `state.py` already owns event-id assignment precedence, game-info ingestion, rank snapshot storage, and pre-match
  rank carry-forward.
- `rank.py` already parses `RankGetCombinedRankInfo` fields without needing behavior changes.
- `models.py` already owns `MatchSummary.event_id`, `super_format`, `constructed_rank`, `match_win_condition`,
  `mtga_format()`, `mtga_queue_type()`, `rank_bucket()`, row serialization, and history serialization.
- `event_identity.py` already owns derived EventIdentity classifier facets.
- `runtime_surfaces.py` already consumes parser-produced history/filter context without owning truth.

## Contract Mismatches Fixed

- Tier 2 `queue_format_rank_event_context.status` was `registered_future`; it is now `seeded_sample`.
- Tier 2 `seed_fields` was empty; it is now exactly:
  - `event_id`
  - `super_format`
  - `constructed_rank`
  - `queue_type`
- Tier 2 `future_fields` listed those four fields; it is now empty.
- The ledger did not have the four required Tier 2 entries; all four now exist and validate.
- Focused tests did not pin the Tier 2 seed boundary, exact entry IDs, evidence paths, policies, degradation behavior,
  or downstream non-truth boundaries; they now do.

## Changes Made

- Updated `src/mythic_edge_parser/app/evidence_ledger.py`.
  - Changed Tier 2 family metadata to `seeded_sample`.
  - Added the four authorized Tier 2 seed fields and no others.
  - Added validating entries for `event_id`, `super_format`, `constructed_rank`, and `queue_type`.
  - Documented direct evidence from MatchState event ID, GameState superFormat, GameState matchWinCondition, and Rank
    payload fields.
  - Documented fallback/facet context for player-level event ID, parser-state event ID precedence, event-id format
    fallback, carried-forward rank snapshots, rank buckets, sideboarding/total-games queue fallback, raw condition
    pass-through, and EventIdentity classifier facets.
  - Documented value-source, confidence, finality, invariant, degradation, drift, privacy, and protected truth
    boundaries.
- Updated `tests/test_evidence_ledger.py`.
  - Added Tier 2 contracted field, entry, and forbidden-seed constants.
  - Updated exact family status expectations and exact entry-set expectations.
  - Added focused tests for the Tier 2 family seed scope and all four entries.
  - Added coverage for MatchState event ID sources, GameState format context, Rank payload/carry-forward rank context,
    queue-type derivation, EventIdentity facets, runtime filters, and downstream non-truth boundaries.

## Boundaries Preserved

- No parser behavior changed.
- No event identity classifier behavior changed.
- No rank parsing behavior changed.
- No match-state parsing behavior changed.
- No parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script
  behavior, output transport, ActionLogRow shape, match/game identity, deduplication, secrets, environment variables,
  raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, analytics truth,
  AI truth, model-provider behavior, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync
  behavior, or archetype classification behavior changed.
- No seed fields were added for workbook-facing labels, EventIdentity fields, rank buckets, runtime filters, analytics
  segments, archetypes, model-provider output, or AI.
- No runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report
  changes, replay report changes, feature-equity report changes, Match Journal behavior, overlay behavior, SQLite
  behavior, or Google Sheets sync behavior was implemented.
- No raw private Player.log excerpts, raw payload values, local runtime artifacts, generated data, failed posts,
  runtime status files, workbook exports, secrets, tokens, credentials, webhook URLs, or API keys were committed.

## Validation Evidence

- `python3 -m pytest -q tests/test_evidence_ledger.py`
  - result: passed, `89 passed`
- `python3 -m pytest -q tests/test_event_identity.py`
  - result: passed, `36 passed`
- `python3 -m pytest -q tests/test_match_state_parser.py tests/test_state.py tests/test_app_models.py`
  - result: passed, `47 passed`
- `python3 -m pytest -q tests/test_runtime_surfaces.py`
  - result: passed, `7 passed`
- `python3 -m ruff check src tests tools`
  - result: passed
- `python3 -m pytest -q`
  - result: passed, `948 passed`
- `git diff --check`
  - result: passed
- `printf '<changed paths>' | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin`
  - result: passed, `changed_paths: 4`, `forbidden: 0`, `warnings: 0`

## Open Risks

- CI was not run in this local Codex C pass.
- Runtime field-evidence attachment remains out of scope.
- Drift reports, schema snapshots, invariant execution, diagnostics/replay/feature-equity report changes, and Tier 6
  or Tier 7 provenance remain deferred.
- Future analytics may need additional field-evidence payloads for `MTGA Format`, `MTGA Queue Type`, `My Rank`, or
  EventIdentity facets, but this pass intentionally kept those as facets/downstream consumers.
- The contract source artifact is untracked in this worktree and should be included by submitter if review passes.

## Next Recommended Role

Next role: Codex E / Module Reviewer in contract-test mode.

Use Codex D only if Codex E finds a concrete blocker. Use Codex F only after review passes.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #167, Tier 2 queue/format/rank/event-context provenance under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/167
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier2-context
- Contract: docs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md
- Handoff: docs/implementation_handoffs/player_log_evidence_ledger_tier2_queue_format_rank_event_context_comparison.md
- Latest verified remote commit: 9f625ea0ef31cdbaa97a827a95ba3b4808562d11

Use:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/parser_event_identity.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier2_queue_format_rank_event_context_comparison.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/event_identity.py
- src/mythic_edge_parser/parsers/match_state.py
- src/mythic_edge_parser/parsers/rank.py
- src/mythic_edge_parser/app/runtime_surfaces.py
- tests/test_event_identity.py
- tests/test_match_state_parser.py
- tests/test_state.py
- tests/test_app_models.py
- tests/test_runtime_surfaces.py

Goal:
Verify the Codex C implementation against the Tier 2 queue/format/rank/event-context provenance contract.

Confirm:
- Branch is not main and is based on the verified integration commit.
- Tier 2 queue_format_rank_event_context is seeded_sample.
- Tier 2 seed_fields is exactly ["event_id", "super_format", "constructed_rank", "queue_type"].
- Tier 2 future_fields is exactly [].
- No separate Tier 2 seed fields were added for mtga_format, mtga_queue_type, match_win_condition, my_rank, rank_bucket, constructed rank facets, limited rank facets, EventIdentity fields, runtime filter fields, analytics segments, archetypes, model-provider output, or AI.
- Entries exist and validate:
  - tier2.queue_format_rank_event_context.event_id
  - tier2.queue_format_rank_event_context.super_format
  - tier2.queue_format_rank_event_context.constructed_rank
  - tier2.queue_format_rank_event_context.queue_type
- The event_id entry distinguishes game-room config evidence from player-level fallback and parser-state precedence context.
- The super_format entry distinguishes raw GameState superFormat evidence from row-facing MTGA Format fallback labels.
- The constructed_rank entry distinguishes direct Rank payload evidence from carried_forward_pre_match rank snapshots and My Rank bucket facets.
- The queue_type entry documents MTGA Queue Type as parser-derived, with matchWinCondition as observed dependency and weaker event-id / sideboarding / total-games fallbacks.
- EventIdentity classifier outputs remain derived facets, not separate seed fields or workbook/AI truth.
- Runtime history filters remain downstream consumers, not truth owners.
- Path-only privacy is preserved.
- Prior Tier 1, Tier 3, Tier 4, and Tier 5 seed fields and entries remain unchanged.
- No parser behavior, event identity classifier behavior, rank parsing behavior, match-state parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, analytics truth, AI truth, model-provider behavior, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, or archetype classification behavior changed.

Validation:
Run:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_event_identity.py
- python3 -m pytest -q tests/test_match_state_parser.py tests/test_state.py tests/test_app_models.py
- python3 -m pytest -q tests/test_runtime_surfaces.py
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
- Change parser behavior, event identity classifier behavior, rank parsing behavior, match-state parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, analytics truth, AI truth, model-provider behavior, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, or archetype classification behavior.
- Stage, commit, push, merge, close issue #11, close issue #167, or target main.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/167"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier2_queue_format_rank_event_context_comparison.md"
  verdict: "tier2_queue_format_rank_event_context_metadata_ready_for_contract_review"
  risk_tier: "Medium-High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier2-context"
  latest_verified_remote_commit: "9f625ea0ef31cdbaa97a827a95ba3b4808562d11"
  authorized_seed_fields:
    - "event_id"
    - "super_format"
    - "constructed_rank"
    - "queue_type"
  authorized_seed_entries:
    - "tier2.queue_format_rank_event_context.event_id"
    - "tier2.queue_format_rank_event_context.super_format"
    - "tier2.queue_format_rank_event_context.constructed_rank"
    - "tier2.queue_format_rank_event_context.queue_type"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py - passed, 89 passed"
    - "python3 -m pytest -q tests/test_event_identity.py - passed, 36 passed"
    - "python3 -m pytest -q tests/test_match_state_parser.py tests/test_state.py tests/test_app_models.py - passed, 47 passed"
    - "python3 -m pytest -q tests/test_runtime_surfaces.py - passed, 7 passed"
    - "python3 -m ruff check src tests tools - passed"
    - "python3 -m pytest -q - passed, 948 passed"
    - "git diff --check - passed"
    - "printf '<changed paths>' | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin - passed, changed_paths 4, forbidden 0, warnings 0"
  changed_files:
    - "src/mythic_edge_parser/app/evidence_ledger.py"
    - "tests/test_evidence_ledger.py"
    - "docs/implementation_handoffs/player_log_evidence_ledger_tier2_queue_format_rank_event_context_comparison.md"
  untracked_source_artifacts:
    - "docs/contracts/player_log_evidence_ledger_tier2_queue_format_rank_event_context.md"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #11 or issue #167."
    - "Do not change parser behavior, event identity classifier behavior, rank parsing behavior, match-state parsing behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production behavior, analytics truth, AI truth, model-provider behavior, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, or archetype classification behavior."
    - "Do not add seed fields for workbook-facing labels, EventIdentity fields, rank buckets, runtime filter fields, analytics segments, archetypes, model-provider output, or AI."
    - "Do not implement runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, feature-equity report changes, Match Journal behavior, overlay behavior, SQLite behavior, or Google Sheets sync changes."
    - "Do not commit raw private Player.log excerpts, raw payload values, local runtime artifacts, generated data, failed posts, runtime status files, workbook exports, secrets, tokens, credentials, webhook URLs, or API keys."
```
