# Player.log Evidence Ledger Tier 1 Game Aggregates Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/132

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

- `docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md`
- `docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md`
- `docs/contracts/player_log_evidence_ledger_schema.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/contracts/parser_models.md`
- `docs/contracts/parser_state.md`
- `docs/contracts/parser_sheet_schema.md`

## Implementation Under Test

- branch: `codex/player-log-evidence-ledger-tier1-game-aggregates`
- base branch: `codex/parser-reliability-intelligence`
- previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/130
- previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/131
- previous merge commit: `c5e4aa9952ba2026ecf5a0778254701c521fa278`
- implementation handoff:
  `docs/implementation_handoffs/player_log_evidence_ledger_tier1_game_aggregates_comparison.md`
- implementation/test files:
  - `src/mythic_edge_parser/app/evidence_ledger.py`
  - `tests/test_evidence_ledger.py`

## Findings

No blocking findings.

The Codex C implementation satisfies the Tier 1 game-derived aggregate
provenance contract. The package expands ledger metadata and focused tests only,
preserves #128 schema/vocabulary and #130 Tier 1 lifecycle/result/sync entries,
maps the five aggregate fields, keeps per-game result provenance deferred to
Tier 3, and does not change parser/runtime/workbook behavior.

## Contract Summary

Issue #132 moves the five game-derived aggregate fields out of Tier 1
`future_fields` and into full ledger entries:

- `tier1.match_aggregates.games_won`
- `tier1.match_aggregates.games_lost`
- `tier1.match_aggregates.total_games`
- `tier1.match_aggregates.match_win_flag`
- `tier1.match_aggregates.game_win_rate`

These entries must be parser-owned, derived from `MatchSummary` surfaces, and
document dependencies, blank/degraded behavior, invariants, and future review
signals without changing aggregate math or any protected downstream surface.

## Checks Run

```bash
git fetch --prune
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_state.py
python3 -m pytest -q tests/test_golden_replay_harness.py
python3 -m pytest -q tests/test_app_models.py
python3 -m ruff check src tests tools
git diff --check
printf 'src/mythic_edge_parser/app/evidence_ledger.py\ntests/test_evidence_ledger.py\ndocs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md\ndocs/implementation_handoffs/player_log_evidence_ledger_tier1_game_aggregates_comparison.md\ndocs/contract_test_reports/player_log_evidence_ledger_tier1_game_aggregates.md\n' | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
python3 -m pytest -q
```

## Results

- `tests/test_evidence_ledger.py`: passed, 23 tests.
- `tests/test_state.py`: passed, 18 tests.
- `tests/test_golden_replay_harness.py`: passed, 13 tests.
- `tests/test_app_models.py`: passed, 16 tests.
- `ruff`: passed.
- `git diff --check`: passed.
- path-scoped protected-surface check: passed, 5 changed paths, forbidden 0,
  warnings 0.
- full pytest: passed, 882 tests.

## Confirmed Contract Matches

- The #128 `tier1.match_identity.match_id` entry is preserved.
- All #130 Tier 1 lifecycle/result/sync entries are preserved, including the
  prior GameResult `gameInfo.results[]` provenance correction.
- Tier 1 `seed_fields` includes all eleven mapped fields from #128, #130, and
  #132.
- Tier 1 `future_fields` is empty and no longer contains `games_won`,
  `games_lost`, `total_games`, `match_win_flag`, or `game_win_rate`.
- Entries exist for all five contracted aggregate IDs:
  - `tier1.match_aggregates.games_won`
  - `tier1.match_aggregates.games_lost`
  - `tier1.match_aggregates.total_games`
  - `tier1.match_aggregates.match_win_flag`
  - `tier1.match_aggregates.game_win_rate`
- Aggregate entries are `derived`, parser-owned, and reference `MatchSummary`
  model surfaces.
- Games won/lost/total games entries document game-winner, player-team, and/or
  count dependencies.
- `match_win_flag` documents its `match_wl` / match-result dependency and
  explicitly rejects inference from game totals.
- `game_win_rate` documents `game_wins` / `total_games` dependencies, expected
  blank behavior for zero completed games, division-by-zero avoidance, and rate
  invariants.
- Full per-game result provenance remains deferred to Tier 3.
- The implementation preserves existing #128/#130 vocabularies for
  value-source, confidence, finality, invariant-status, and drift-flag labels.
- Validators, privacy checks, copy safety, and deterministic serialization pass.
- No parser behavior, parser state final reconciliation, parser event classes,
  workbook schema, webhook payload shape, Apps Script behavior, output
  transport, match/game identity, deduplication, secrets, raw logs, generated
  data, runtime status files, failed posts, workbook exports, or AI/analytics
  truth changes were found.

## Contract Mismatches

None found.

## Missing Tests

None blocking.

Focused tests cover the expanded Tier 1 entry set, aggregate deferral removal,
derived source policy, dependency signals, expected blank behavior, invariant
names, validation, privacy, copy safety, and deterministic serialization.

## Remaining Non-Blocking Gaps

- The ledger schema still does not include an `allowed_types` label for `float`,
  while `MatchSummary.game_win_rate` returns a numeric ratio when
  `total_games > 0`. The implementation preserves the existing schema labels
  and documents numeric rate behavior through dependencies, invariants, and
  degradation text. This is acceptable for #132 and remains a possible later
  schema cleanup.
- Full per-game result provenance is intentionally deferred to a later Tier 3
  game-level facts issue.
- Runtime field-evidence attachment, drift reports, schema snapshots,
  invariant execution, diagnostics reports, replay report-shape changes, and
  feature-equity report-shape changes remain out of scope.

## Drift Notes

- Repo drift: none found.
- Workbook schema drift: none found.
- Webhook/App Script drift: none found.
- Parser/runtime behavior drift: none found.
- Local-data drift: none found.
- Tracker drift: none found in reviewed scope; tracker #11 remains open by
  design.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #132, Tier 1 game-derived aggregate
provenance under tracker #11.

Use:
- docs/contracts/player_log_evidence_ledger_tier1_game_aggregates.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier1_game_aggregates_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier1_game_aggregates.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py

Goal:
Submit the reviewed issue #132 package as a draft PR from
codex/player-log-evidence-ledger-tier1-game-aggregates to
codex/parser-reliability-intelligence.

Confirm before staging:
- Only issue #132 docs, evidence ledger metadata, focused evidence-ledger tests,
  and the Codex E contract-test report are included.
- No parser behavior, parser state final reconciliation, parser event classes,
  workbook schema, webhook payload shape, Apps Script behavior, output
  transport, match/game identity, deduplication, secrets, raw logs, generated
  data, runtime status files, failed posts, workbook exports, or AI/analytics
  truth changed.
- Do not target main directly.
- Do not close issue #11.

Validation to record:
- python3 -m pytest -q tests/test_evidence_ledger.py -> 23 passed
- python3 -m pytest -q tests/test_state.py -> 18 passed
- python3 -m pytest -q tests/test_golden_replay_harness.py -> 13 passed
- python3 -m pytest -q tests/test_app_models.py -> 16 passed
- python3 -m ruff check src tests tools -> passed
- git diff --check -> passed
- path-scoped protected-surface check -> passed, 5 changed paths, forbidden 0, warnings 0
- python3 -m pytest -q -> 882 passed

Open or update a draft PR against codex/parser-reliability-intelligence.
Use Refs #132 and Refs #11 unless the PR fully satisfies issue #132 and the
repo workflow authorizes closing the child issue from this PR. Do not merge,
mark ready, close issues, or update tracker #11 as complete; route those steps
to Codex G after review/CI.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/132"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/130"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/131"
  previous_merge_commit: "c5e4aa9952ba2026ecf5a0778254701c521fa278"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/player_log_evidence_ledger_tier1_game_aggregates.md"
  target_artifact: "draft PR from codex/player-log-evidence-ledger-tier1-game-aggregates to codex/parser-reliability-intelligence"
  verdict: "no_blocking_findings_ready_for_codex_f"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier1-game-aggregates"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py -> 23 passed"
    - "python3 -m pytest -q tests/test_state.py -> 18 passed"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py -> 13 passed"
    - "python3 -m pytest -q tests/test_app_models.py -> 16 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check -> passed, 5 changed paths, forbidden 0, warnings 0"
    - "python3 -m pytest -q -> 882 passed"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, or AI/analytics truth."
    - "Do not reconstruct missing GameState data or infer facts that the Player.log did not provide."
    - "Do not implement runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, or feature-equity report changes."
    - "Do not commit raw private Player.log excerpts."
    - "Codex F may submit a draft PR but must not merge, mark ready, close issues, or mark tracker #11 complete."
```
