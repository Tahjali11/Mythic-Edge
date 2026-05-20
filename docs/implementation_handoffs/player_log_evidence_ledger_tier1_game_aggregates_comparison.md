# Player.log Evidence Ledger Tier 1 Game Aggregates Comparison

## Metadata

- role: Codex C / Module Implementer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/132
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/130
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/131
- previous_merge_commit: c5e4aa9952ba2026ecf5a0778254701c521fa278
- source_artifact: docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- existing_schema_contract: docs/contracts/player_log_evidence_ledger_schema.md
- existing_lifecycle_contract: docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- implementation_branch: codex/player-log-evidence-ledger-tier1-game-aggregates
- base_branch: codex/parser-reliability-intelligence
- risk_tier: High

## Summary

The current ledger matched the issue #128 schema slice and preserved all issue
#130 Tier 1 lifecycle/result/sync entries. The issue #132 mismatch was exactly
the expected one: `games_won`, `games_lost`, `total_games`, `match_win_flag`,
and `game_win_rate` were still Tier 1 future fields with no full ledger entries.

This implementation expands metadata and focused tests only. It does not change
parser behavior, parser state reconciliation, parser event classes, workbook
schema, webhook payload shape, Apps Script behavior, output transport,
match/game identity, deduplication, runtime artifacts, raw logs, workbook
exports, or AI/analytics truth.

## Confirmed Matches Before Editing

- The #128 public constants, validators, schema version, ledger version,
  vocabulary constants, and `match_id` anchor entry were present and valid.
- The #130 entries for `match_started_at`, `match_finished_at`,
  `match_winner_team`, `match_result`, and `match_sync_status` were present and
  valid.
- The #130 GameResult match-winner raw path fix was present:
  `greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId`.
- `src/mythic_edge_parser/app/models.py` already owns the aggregate math:
  `game_wins`, `game_losses`, `total_games`, `match_win_flag`, and
  `game_win_rate`.
- Existing model/state/golden replay tests already cover current emitted row
  behavior for the aggregate fields.

## Contract Mismatches Found

- Tier 1 `match_identity_and_lifecycle.future_fields` still contained the five
  game-derived aggregate fields.
- Tier 1 `seed_fields` did not include those five aggregate fields.
- The ledger did not have entries for:
  - `tier1.match_aggregates.games_won`
  - `tier1.match_aggregates.games_lost`
  - `tier1.match_aggregates.total_games`
  - `tier1.match_aggregates.match_win_flag`
  - `tier1.match_aggregates.game_win_rate`
- Focused tests still asserted aggregate deferral instead of mapped aggregate
  provenance.

## Changes Made

- Updated `src/mythic_edge_parser/app/evidence_ledger.py` so Tier 1 seed fields
  now include all eleven mapped fields from #128, #130, and #132.
- Cleared Tier 1 `future_fields`, with notes preserving that full per-game fact
  provenance remains deferred to Tier 3.
- Added metadata-only aggregate entries for:
  - `games_won` / `Games Won`
  - `games_lost` / `Games Lost`
  - `total_games` / `Total Games`
  - `match_win_flag` / `Match Win Flag`
  - `game_win_rate` / `Game Win %`
- Each aggregate entry is marked derived, references `MatchSummary` model
  surfaces, and documents dependency signals, expected blank behavior,
  invariant names, degradation behavior, and future review triggers.
- Updated `tests/test_evidence_ledger.py` to assert:
  - eleven Tier 1 entries are mapped
  - aggregate fields moved out of `future_fields`
  - aggregate entries are derived `MatchSummary` metadata
  - game count entries reference game-winner/player-team/count dependencies
  - `match_win_flag` depends on `match_wl` and the mapped match-result entry
  - `game_win_rate` depends on `game_wins` and `total_games`
  - expected blank and invariant language is present
  - existing validation, privacy, copy-safety, and deterministic serialization
    behavior still passes

## Missing Safeguards

No missing safeguards remain for the issue #132 metadata-only scope. The ledger
continues to validate duplicate IDs, unknown vocabulary, absolute paths,
raw-log-like text, webhook-like text, and secret-like text. The new entries use
only repo-relative or symbolic paths and existing value-source, confidence,
finality, invariant-status, and drift-flag vocabulary.

## Missing Or Weak Tests

- Fixed: focused tests now cover expanded aggregate entries, source policy,
  dependency signals, expected blank behavior, and invariants.
- Existing adjacent tests remain the behavioral proof for actual aggregate row
  output; this pass intentionally does not change those outputs.
- Still intentionally absent: runtime field-evidence attachment tests, drift
  report tests, schema snapshot tests, invariant execution tests, diagnostics
  report tests, replay report-shape tests, and feature-equity report tests.

## Validation Evidence

- `python3 -m pytest -q tests/test_evidence_ledger.py`
  - passed: 23 tests in 0.07s
- `python3 -m pytest -q tests/test_state.py`
  - passed: 18 tests in 0.22s
- `python3 -m pytest -q tests/test_golden_replay_harness.py`
  - passed: 13 tests in 0.28s
- `python3 -m pytest -q tests/test_app_models.py`
  - passed: 16 tests in 0.05s
- `python3 -m ruff check src tests tools`
  - passed
- `git diff --check`
  - passed after handoff creation
- Path-scoped protected-surface check for changed files
  - passed: 4 changed paths, forbidden 0, warnings 0
- `python3 -m pytest -q`
  - passed: 882 tests in 1.88s

## Open Risks

- The #128 `allowed_types` labels do not include `float`, while
  `MatchSummary.game_win_rate` can return a numeric ratio. To preserve the
  existing schema vocabulary, the `game_win_rate` entry uses existing symbolic
  type labels and documents numeric-rate behavior through invariants and
  degradation text. A later schema cleanup can add a clearer numeric type label
  if desired.
- Aggregate confidence depends on per-game winner and player-team provenance
  that remains only dependency-level metadata in this issue. Full per-game
  result provenance is still deferred to a later Tier 3 issue.
- Unknown-like per-game winner values can affect aggregate math if they reach
  `GameSummary.winner_team`; this issue records the risk but does not authorize
  behavior changes.

## Still-Unverified Layers

- Runtime field-evidence attachment remains unimplemented by design.
- Drift reports, invariant execution, schema snapshots, diagnostics reports,
  replay reports, and feature-equity reports remain out of scope.
- Workbook/Apps Script/webhook deployment behavior was not changed or verified
  as live infrastructure.

## Next Recommended Role

Codex E: Module Reviewer in contract-test mode.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for issue #132, Tier 1
game-derived aggregate provenance under tracker #11.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/11
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/132
- Previous child issue: https://github.com/Tahjali11/Mythic-Edge/issues/130
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/131
- Previous merge commit: c5e4aa9952ba2026ecf5a0778254701c521fa278
- Base branch: codex/parser-reliability-intelligence
- Implementation branch: codex/player-log-evidence-ledger-tier1-game-aggregates

Use:
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/parser_models.md
- docs/contracts/parser_state.md
- docs/contracts/parser_sheet_schema.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier1_game_aggregates_comparison.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- src/mythic_edge_parser/app/models.py
- src/mythic_edge_parser/app/state.py
- src/mythic_edge_parser/app/sheet_schema.py
- src/mythic_edge_parser/app/golden_replay.py
- tests/test_state.py
- tests/test_app_models.py
- tests/test_golden_replay_harness.py

Goal:
Verify the Codex C implementation against the Tier 1 game-derived aggregate
evidence ledger contract. Confirm the registry expands only metadata and
focused tests, preserves #128 schema/vocabulary and all #130 entries, maps the
five aggregate fields, keeps per-game result provenance deferred to Tier 3, and
does not change parser/runtime/workbook behavior.

Confirm:
- The #128 `tier1.match_identity.match_id` entry is preserved.
- All #130 Tier 1 lifecycle/result/sync entries are preserved.
- Tier 1 `seed_fields` includes all eleven mapped fields.
- Tier 1 `future_fields` no longer contains `games_won`, `games_lost`,
  `total_games`, `match_win_flag`, or `game_win_rate`.
- Entries exist for `tier1.match_aggregates.games_won`,
  `tier1.match_aggregates.games_lost`,
  `tier1.match_aggregates.total_games`,
  `tier1.match_aggregates.match_win_flag`, and
  `tier1.match_aggregates.game_win_rate`.
- All aggregate entries are derived, parser-owned, and reference `MatchSummary`
  model surfaces.
- Games won/lost/total games entries document game-winner and player-team or
  count dependencies.
- `match_win_flag` documents its `match_wl` / match-result dependency and does
  not claim game-total inference.
- `game_win_rate` documents `game_wins` / `total_games` dependency, expected
  blank behavior for zero completed games, and rate invariants.
- Full per-game result provenance remains deferred to Tier 3.
- Existing validators, privacy checks, copy safety, and deterministic
  serialization still pass.
- No parser behavior, parser state final reconciliation, parser event classes,
  workbook schema, webhook payload shape, Apps Script behavior, output
  transport, match/game identity, deduplication, secrets, raw logs, generated
  data, runtime status files, failed posts, workbook exports, or AI/analytics
  truth changed.

Validation:
- python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m pytest -q tests/test_state.py
- python3 -m pytest -q tests/test_golden_replay_harness.py
- python3 -m pytest -q tests/test_app_models.py
- python3 -m ruff check src tests tools
- git diff --check
- path-scoped protected-surface check for changed files
- python3 -m pytest -q

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F if no blocking findings, otherwise Codex D or
  Codex B.
- workflow_handoff block.

Do not target main directly.
Do not close issue #11.
Do not stage, commit, push, or open a PR unless explicitly asked.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/132"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/130"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/131"
  previous_merge_commit: "c5e4aa9952ba2026ecf5a0778254701c521fa278"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md"
  target_artifact: "docs/implementation_handoffs/player_log_evidence_ledger_tier1_game_aggregates_comparison.md"
  verdict: "ready_for_module_reviewer"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier1-game-aggregates"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m pytest -q tests/test_state.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q tests/test_app_models.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped protected-surface check for changed files"
    - "python3 -m pytest -q"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, or AI/analytics truth."
    - "Do not reconstruct missing GameState data or infer facts that the Player.log did not provide."
    - "Do not implement runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, or feature-equity report changes."
    - "Do not commit raw private Player.log excerpts."
```
