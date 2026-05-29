# Analytics Derived SQL Views Contract Test Report

## Findings

### Blocking

None remaining after the Codex D fixer pass.

### Resolved By Codex D

#### ADEV-001: `v_matchup_label_performance` hid current labels with no `match_results` row from `match_count`

- Severity: high
- Finding lifecycle: `fixed_state_followup`
- Finding status: verified fixed
- Blocking status: not_blocking
- Route: Codex F: Module Submitter

Original evidence:

- The contract requires `v_matchup_label_performance` to use current human matchup labels, count known wins/losses separately, and avoid treating unknown results as losses (`docs/contracts/analytics_derived_sql_views.md`, Matchup Label Performance Views). It also requires summary views not to erase unknown/degraded rows from the denominator.
- The view counts `COUNT(DISTINCT mr.match_id) AS match_count` after a `LEFT JOIN` from `matchup_labels` to `match_results` (`src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql:1466`).
- A direct in-memory probe with a current `matchup_labels` row and no corresponding `match_results` row returned:

```text
{'matchup_label': 'missing_result_label', 'match_count': 0, 'known_match_result_count': 0, 'match_wins': 0, 'match_losses': 0, 'unknown_match_result_count': 1, 'match_win_rate': None}
```

Expected behavior:

- The current human label should remain counted as one labeled match even when match-result evidence is absent.
- The row should preserve `known_match_result_count = 0`, `match_wins = 0`, `match_losses = 0`, `unknown_match_result_count = 1`, and `match_win_rate = NULL`.
- `match_count` should not depend on the joined `match_results` row existing.

Fix evidence:

- `v_matchup_label_performance` now counts `COUNT(DISTINCT ml.match_id)` so the denominator follows current human labels rather than the optional joined result row.
- `tests/test_analytics_derived_views.py` now includes a focused current-label/no-`match_results` regression test. The expected row has `match_count = 1`, `known_match_result_count = 0`, `match_wins = 0`, `match_losses = 0`, `unknown_match_result_count = 1`, and `match_win_rate = NULL`.

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/191>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/190>

## Contract

`docs/contracts/analytics_derived_sql_views.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Changed files reviewed:

- `docs/contracts/analytics_derived_sql_views.md`
- `docs/implementation_handoffs/analytics_derived_sql_views_comparison.md`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_derived_views.py`
- `tests/test_analytics_schema.py`

## Report Lifecycle

`report_lifecycle`: `followup_after_fixer`

## Contract Summary

The implementation must provide deterministic, read-only local SQLite analytics views over already-ingested parser/local analytics facts. The views may summarize local database rows but must not become parser truth, workbook truth, AI truth, coaching truth, merge readiness, or deploy readiness. Unknown, degraded, unavailable, and human-entered values must remain visible to reviewers rather than being collapsed into clean wins/losses or omitted from denominators.

## Checks Run

```bash
python3 -m pytest -q tests/test_analytics_derived_views.py
python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' \
  src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql \
  tests/test_analytics_schema.py \
  tests/test_analytics_derived_views.py \
  docs/contracts/analytics_derived_sql_views.md \
  docs/implementation_handoffs/analytics_derived_sql_views_comparison.md \
  docs/contract_test_reports/analytics_derived_sql_views.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
printf '%s\n' \
  src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql \
  tests/test_analytics_schema.py \
  tests/test_analytics_derived_views.py \
  docs/contracts/analytics_derived_sql_views.md \
  docs/implementation_handoffs/analytics_derived_sql_views_comparison.md \
  docs/contract_test_reports/analytics_derived_sql_views.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
python3 -m pytest -q
```

## Results

- `tests/test_analytics_derived_views.py`: 7 passed.
- `tests/test_analytics_schema.py tests/test_analytics_migration_loader.py`: 27 passed.
- Analytics ingest adjacent suite: 101 passed.
- `python3 -m ruff check src tests tools`: passed.
- `git diff --check`: passed.
- Path-scoped secret/private marker scan: passed, 6 scanned paths, 0 forbidden, 0 warnings.
- Path-scoped protected-surface gate: passed, 6 changed paths, 0 forbidden, 0 warnings.
- Full pytest: 1347 passed.

Initial Codex E validation passed before the blocker was identified. Codex D reran validation after fixing ADEV-001, and Codex E verified the fixer pass with the same validation set:

- `tests/test_analytics_derived_views.py`: 8 passed.
- `tests/test_analytics_schema.py tests/test_analytics_migration_loader.py`: 27 passed.
- Analytics ingest adjacent suite: 101 passed.
- `python3 -m ruff check src tests tools`: passed.
- `git diff --check`: passed.
- Path-scoped secret/private marker scan: passed, 6 scanned paths, 0 forbidden, 0 warnings.
- Path-scoped protected-surface gate: passed, 6 changed paths, 0 forbidden, 0 warnings.
- Full pytest: 1348 passed.
- Direct Codex E repro probe: current label with no `match_results` row returned `match_count = 1`, `known_match_result_count = 0`, `match_wins = 0`, `match_losses = 0`, `unknown_match_result_count = 1`, and `match_win_rate = NULL`.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADEV-001 | high | `fixed_state_followup` | verified fixed | not_blocking | `v_matchup_label_performance` counted `mr.match_id`; a current label with no `match_results` row returned `match_count = 0` while `unknown_match_result_count = 1`. | `v_matchup_label_performance` now counts `ml.match_id`; focused test coverage passes for a current label with no `match_results` row, and a direct Codex E repro probe returns `match_count = 1`, unknown result count `1`, and `match_win_rate = NULL`. | F |

## Confirmed Contract Matches

- The implementation keeps the seven existing approved views and adds only the two approved review views: `v_gameplay_action_review` and `v_opponent_card_observation_review`.
- The view definitions remain deterministic `CREATE VIEW` statements in the active analytics migration and do not add triggers, materialized tables, runtime APIs, network calls, or model calls.
- `v_play_draw_splits` groups blank/missing play-draw values as `unknown`, separates known wins/losses from unknown results, and computes win rate over known win/loss outcomes only.
- `v_sample_size_warnings` produces deterministic labels for visible play/draw split groups.
- Row-level review views preserve row identity and provenance labels needed for local review.
- No parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, Match Journal behavior, overlay behavior, CI gate, merge policy, deploy policy, model-provider behavior, or AI/coaching behavior changed in the reviewed diff.

## Contract Mismatches

- None remaining after Codex E re-review of the Codex D fixer pass.

## Missing Tests

- Added focused coverage for a current `matchup_labels` row with no corresponding `match_results` row. The expected summary counts the labeled match, preserves zero known wins/losses, counts the result as unknown, and returns `NULL` match win rate.

## Drift Notes

- Worktree is on `codex/analytics-foundation`.
- Changed/untracked files match the expected implementation slice.
- No unrelated runner, parser, workbook, webhook, Apps Script, runtime artifact, raw log, generated data, failed-post, workbook export, CI, or model-provider changes were observed in the reviewed file set.

## Recommendation

Approve for Codex F submission.

## Next Workflow Action

Next role: Codex F: Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/191"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/190"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/analytics_derived_sql_views.md"
  target_artifact: "Codex F submission package for issue #191"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  verdict: "no_blocking_findings_ready_for_codex_f"
  validation:
    - "python3 -m pytest -q tests/test_analytics_derived_views.py -> 8 passed"
    - "python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py -> 27 passed"
    - "python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py -> 101 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped secret/private marker scan -> passed"
    - "path-scoped protected-surface gate -> passed"
    - "python3 -m pytest -q -> 1348 passed"
  fixed_findings:
    - "ADEV-001 verified fixed: v_matchup_label_performance now counts current human labels even when no match_results row exists."
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #190 or issue #191."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, workbook schema, webhook payload shape, Apps Script behavior, output transport, Match Journal behavior, overlay behavior, CI gates, merge policy, deploy policy, model-provider behavior, or AI/coaching truth."
    - "Do not add broad analytics families, runtime APIs, triggers, materialized tables, generated SQLite databases, raw Player.log artifacts, runtime status files, failed posts, workbook exports, network calls, or model calls."
```
