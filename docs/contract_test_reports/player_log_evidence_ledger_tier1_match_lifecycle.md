# Player.log Evidence Ledger Tier 1 Match Lifecycle Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/130

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

- `docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md`
- `docs/contracts/player_log_evidence_ledger_schema.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/contracts/parser_state.md`
- `docs/contracts/parser_models.md`
- `docs/contracts/parser_sheet_schema.md`

## Implementation Under Test

- branch: `codex/player-log-evidence-ledger-tier1-match-lifecycle`
- base branch: `codex/parser-reliability-intelligence`
- implementation handoff:
  `docs/implementation_handoffs/player_log_evidence_ledger_tier1_match_lifecycle_comparison.md`
- changed implementation/test files:
  - `src/mythic_edge_parser/app/evidence_ledger.py`
  - `tests/test_evidence_ledger.py`
- new docs under review:
  - `docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md`
  - `docs/implementation_handoffs/player_log_evidence_ledger_tier1_match_lifecycle_comparison.md`

## Findings

No blocking findings.

Codex D resolved the prior Codex E metadata-provenance blocker. The
`game_result.results.match_scope_winner` direct evidence path now points to the
parser-produced raw shape under
`greToClientMessages[].gameStateMessage.gameInfo.results[].winningTeamId`, and
focused tests assert both the direct GameResult match-scope winner path and the
top-level match-complete fallback path.

## Contract Summary

The issue #130 package must expand the #128 Player.log evidence ledger from the
single `tier1.match_identity.match_id` seed entry to the Tier 1 match lifecycle
slice. The implementation should add metadata and focused tests only, preserve
existing schema/vocabulary/match ID behavior, add five new entries for
`match_started_at`, `match_finished_at`, `match_winner_team`, `match_result`,
and `match_sync_status`, keep aggregate fields deferred, and avoid parser,
runtime, workbook, webhook, Apps Script, transport, or AI truth changes.

## Checks Run

```bash
git fetch --prune
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_state.py
python3 -m ruff check src tests tools
git diff --check
printf 'docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md\ndocs/implementation_handoffs/player_log_evidence_ledger_tier1_match_lifecycle_comparison.md\ndocs/contract_test_reports/player_log_evidence_ledger_tier1_match_lifecycle.md\nsrc/mythic_edge_parser/app/evidence_ledger.py\ntests/test_evidence_ledger.py\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

## Results

- `tests/test_evidence_ledger.py`: passed, 20 tests.
- `tests/test_state.py`: passed, 18 tests.
- `ruff`: passed.
- `git diff --check`: passed.
- protected-surface path gate: passed, 5 changed paths, forbidden 0,
  warnings 0.

## Confirmed Contract Matches

- The Tier 1 `match_identity_and_lifecycle` output family lists the six
  contracted seed fields:
  - `match_id`
  - `match_started_at`
  - `match_finished_at`
  - `match_winner_team`
  - `match_result`
  - `match_sync_status`
- The #128 `tier1.match_identity.match_id` anchor entry is preserved.
- New entries exist for:
  - `tier1.match_lifecycle.match_started_at`
  - `tier1.match_lifecycle.match_finished_at`
  - `tier1.match_result.match_winner_team`
  - `tier1.match_result.match_result`
  - `tier1.match_lifecycle.match_sync_status`
- The new entries use existing value-source, confidence, finality,
  invariant-status, and drift-flag vocabulary.
- `MGTA Start Time` preserves the legacy workbook spelling.
- `MTGA End Time` documents live-row blank behavior.
- `match_winner_team` documents nested match-scope precedence, top-level
  match-complete fallback, unknown winner values, and no game-level aggregation
  inference.
- `game_result.results.match_scope_winner` and
  `game_result.top_level_match_complete_winner` now both document the
  parser-produced `gameStateMessage.gameInfo.results[]` raw shape.
- `match_result` is documented as derived from match winner plus local player
  team.
- `match_sync_status` is documented as parser-state derived rather than
  raw-log or transport-derived.
- Derived aggregate fields remain deferred rather than fully mapped:
  `games_won`, `games_lost`, `total_games`, `match_win_flag`, and
  `game_win_rate`.
- Validators, privacy checks, copy safety, deterministic serialization, and
  existing parser-state tests pass.
- No parser behavior, parser state final reconciliation, parser event classes,
  workbook schema, webhook payload shape, Apps Script behavior, output
  transport, match/game identity, deduplication, secrets, raw logs, generated
  data, runtime status files, failed posts, workbook exports, or AI/analytics
  truth changes were found.

## Contract Mismatches

None found.

Resolved by Codex D:

- The prior `game_result.results.match_scope_winner` raw path mismatch was
  corrected from `gameStateMessage.results[]` to
  `gameStateMessage.gameInfo.results[]`.

## Missing Tests

None blocking.

Resolved by Codex D:

- `tests/test_evidence_ledger.py` now asserts GameResult direct and fallback
  winner evidence raw paths.

## Drift Notes

- Repo drift: none found.
- Workbook drift: none found.
- Webhook/App Script drift: none found.
- Parser/runtime behavior drift: none found.
- Local-data drift: none found.
- Evidence-ledger metadata drift: prior blocker resolved.

## Recommendation

Approve for Codex F: Module Submitter.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #130, Tier 1 match lifecycle
evidence ledger expansion under tracker #11.

Use:
- docs/contracts/player_log_evidence_ledger_tier1_match_lifecycle.md
- docs/implementation_handoffs/player_log_evidence_ledger_tier1_match_lifecycle_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_tier1_match_lifecycle.md
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py

Goal:
Submit the reviewed issue #130 package as a draft PR from
codex/player-log-evidence-ledger-tier1-match-lifecycle to
codex/parser-reliability-intelligence.

Confirm before staging:
- Only the issue #130 docs, evidence ledger metadata, focused evidence-ledger
  tests, and Codex E contract-test report are included.
- No parser behavior, parser state final reconciliation, parser event classes,
  workbook schema, webhook payload shape, Apps Script behavior, output
  transport, match/game identity, deduplication, secrets, raw logs, generated
  data, runtime status files, failed posts, workbook exports, or AI/analytics
  truth changed.
- Do not target main directly.
- Do not close issue #11.

Validation to record:
- python3 -m pytest -q tests/test_evidence_ledger.py -> 20 passed
- python3 -m pytest -q tests/test_state.py -> 18 passed
- python3 -m ruff check src tests tools -> passed
- git diff --check -> passed
- path-scoped protected-surface check -> passed, forbidden 0, warnings 0

Open or update a draft PR against codex/parser-reliability-intelligence.
Use Refs #130 and Refs #11 unless the PR fully satisfies issue #130 and the
repo workflow authorizes closing the child issue from this PR. Do not merge,
mark ready, close issues, or update tracker #11 as complete; route those steps
to Codex G after review/CI.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/130"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/128"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/129"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/player_log_evidence_ledger_tier1_match_lifecycle.md"
  target_artifact: "draft PR from codex/player-log-evidence-ledger-tier1-match-lifecycle to codex/parser-reliability-intelligence"
  verdict: "no_blocking_findings_ready_for_codex_f"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-tier1-match-lifecycle"
  validation:
    - "python3 -m pytest -q tests/test_evidence_ledger.py -> 20 passed"
    - "python3 -m pytest -q tests/test_state.py -> 18 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check -> passed, 5 changed paths, forbidden 0, warnings 0"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #11."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, or AI/analytics truth."
    - "Do not reconstruct missing GameState data or infer facts that the Player.log did not provide."
    - "Do not implement runtime field-evidence attachment, drift reports, schema snapshots, invariant execution, diagnostics report changes, replay report changes, or feature-equity report changes."
    - "Do not commit raw private Player.log excerpts."
    - "Codex F may submit a draft PR but must not merge, mark ready, close issues, or mark tracker #11 complete."
```
