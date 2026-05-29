# Analytics Derived SQL Views Implementation Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/191>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/190>

## Source Contract

`docs/contracts/analytics_derived_sql_views.md`

## Role Performed

- Codex C: Module Implementer.
- Codex D: Module Fixer follow-up for ADEV-001.

## Branch And Starting State

- Branch: `codex/analytics-foundation`
- Starting HEAD: `77a4cd3`
- `HEAD...origin/codex/analytics-foundation`: `0 0`
- Live GitHub state checked: issue #191 open, tracker #190 open.
- Starting worktree contained the untracked source contract
  `docs/contracts/analytics_derived_sql_views.md`.

## Implementation Summary

Compared the analytics v1 SQL view definitions and focused analytics tests
against the derived SQL views contract. Implemented the smallest SQL/test
changes needed to make the view layer deterministic, review-oriented, and
truth-boundary-preserving.

The implementation keeps the existing seven view names available and adds only
the two contract-approved review views:

- `v_gameplay_action_review`
- `v_opponent_card_observation_review`

No parser behavior, runtime behavior, workbook schema, webhook payload shape,
Apps Script behavior, output transport, Match Journal behavior, overlay
behavior, Google Sheets behavior, AI/OpenAI behavior, CI gates, merge policy,
or deploy policy was changed.

## Files Changed

- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_schema.py`
- `tests/test_analytics_derived_views.py`
- `docs/implementation_handoffs/analytics_derived_sql_views_comparison.md`
- `docs/contract_test_reports/analytics_derived_sql_views.md`

Source artifact present but not edited by this thread:

- `docs/contracts/analytics_derived_sql_views.md`

## Contract-To-Code Comparison

### Confirmed Matches

- Views remain read-only SQL `CREATE VIEW` definitions in the source-controlled
  v1 analytics schema migration.
- Existing seven view names remain available.
- The two added views are limited to the contract-approved review surfaces.
- No stored summary tables, triggers, runtime APIs, Python callbacks, network
  calls, model calls, or materialized analytics outputs were added.
- Tests use in-memory SQLite databases only.
- View assertions use synthetic parser-normalized labels and ids, not raw
  Player.log payloads or local private artifacts.

### Contract Mismatches Fixed

- `v_play_draw_splits` previously treated every non-win row as a loss in
  `win_rate`. It now counts known wins/losses separately, counts unknown,
  unavailable, and degraded rows separately, and computes `win_rate` only over
  known win/loss outcomes.
- `v_matchup_label_performance` previously folded unknown match results into
  the denominator. It now reports known wins/losses and unknown match results
  separately, using only current human labels.
- Codex D fixed ADEV-001: `v_matchup_label_performance` now counts current
  human-label matches from `matchup_labels.match_id`, so labels remain counted
  when match-result evidence is absent.
- `v_opening_hand_cards`, `v_opening_lines`, `v_mulligan_outcomes`, and
  `v_game1_vs_postboard` now expose stronger row identity and provenance or
  availability context required for local review.
- Missing gameplay-action and opponent-observation row-level review views were
  added as `v_gameplay_action_review` and
  `v_opponent_card_observation_review`.
- Focused behavioral tests were added; the prior coverage was mainly
  existence-oriented.

### Missing Safeguards

None blocking for this contract. The implementation did not introduce raw log
storage, generated SQLite artifacts, external IO, downstream truth ownership,
or AI/model-provider behavior.

### Missing Or Weak Tests

None blocking. New focused tests prove:

- approved views exist after migration
- opening-hand card rows preserve identity and provenance labels
- opening-line filtering remains limited to known turns `<= 3`
- all-action review does not widen opening-line semantics
- mulligan review distinguishes `0` from unknown/unavailable detail
- game review preserves pre/postboard and duration context
- play/draw splits do not treat unknowns as losses
- sample-size warning threshold behavior is deterministic
- matchup-label performance uses current human labels and preserves unknown
  results
- matchup-label performance counts a current human label with no
  `match_results` row, preserves zero known wins/losses, counts the result as
  unknown, and returns `NULL` win rate
- opponent-observation review preserves child-card and degradation context

## Interface Changes

View interface changes only:

- Added columns to existing views for row identity, provenance, finality,
  drift, parser schema, ingest run, source surface, source fact key, and
  availability context where applicable.
- Added `v_gameplay_action_review`.
- Added `v_opponent_card_observation_review`.
- Added `v_play_draw_splits` summary columns:
  `known_result_count`, `losses`, `unknown_result_count`,
  `unavailable_result_count`, and `degraded_result_count`.
- Added `v_matchup_label_performance` summary columns:
  `known_match_result_count`, `match_losses`, and
  `unknown_match_result_count`.

No table names, table primary keys, parser row shapes, workbook columns,
webhook payloads, environment variables, runtime routes, or production
interfaces changed.

## Validation Run

```bash
python3 -m pytest -q tests/test_analytics_derived_views.py
python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py
python3 -m ruff check src tests tools
git diff --check
```

Results recorded during implementation:

- `tests/test_analytics_derived_views.py`: `7 passed`
- schema and migration loader suite: `27 passed`
- parser-normalized/action/opponent/field-evidence ingest suite:
  `101 passed`
- Ruff: `All checks passed!`
- `git diff --check`: passed with no output
- no-index whitespace checks for new untracked test/handoff files: passed with
  no output

Additional contract-recommended local checks:

```bash
printf '%s\n' \
  src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql \
  tests/test_analytics_schema.py \
  tests/test_analytics_derived_views.py \
  docs/contracts/analytics_derived_sql_views.md \
  docs/implementation_handoffs/analytics_derived_sql_views_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin

printf '%s\n' \
  src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql \
  tests/test_analytics_schema.py \
  tests/test_analytics_derived_views.py \
  docs/contracts/analytics_derived_sql_views.md \
  docs/implementation_handoffs/analytics_derived_sql_views_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

These were run because both tools exist on the branch.

Results:

- Secret/private marker scan: `forbidden: 0`, `warnings: 0`,
  `result: passed`
- Protected-surface gate: `forbidden: 0`, `warnings: 0`,
  `result: passed`

Codex D focused rerun after ADEV-001 fix:

- `tests/test_analytics_derived_views.py`: `8 passed`
- schema and migration loader suite: `27 passed`
- parser-normalized/action/opponent/field-evidence ingest suite:
  `101 passed`
- Ruff: `All checks passed!`
- `git diff --check`: passed with no output
- Secret/private marker scan: `forbidden: 0`, `warnings: 0`,
  `result: passed`
- Protected-surface gate: `forbidden: 0`, `warnings: 0`,
  `result: passed`
- Full pytest: `1348 passed`

## Still Unverified

- GitHub Actions were not run.
- No live SQLite database, Match Journal, overlay, Google Sheets, workbook,
  webhook, Apps Script, AI/OpenAI, CI, merge, or deploy behavior was checked.
- Future analytics consumers remain undefined; this slice only defines local
  deterministic SQL views.
- Future migration versioning after the analytics v1 schema is merged remains
  deferred.

## Reviewer Focus

Codex E should focus on:

- whether ADEV-001 is fully resolved by counting current labels from
  `matchup_labels.match_id` and the no-result-row regression test
- whether added view columns preserve compatibility while satisfying the
  contract
- whether `v_play_draw_splits` and `v_matchup_label_performance` avoid treating
  unknown/degraded rows as clean losses
- whether `v_gameplay_action_review` and
  `v_opponent_card_observation_review` stay review-only and do not infer hidden
  cards, archetypes, advice, or player mistakes
- whether tests prove behavior rather than only view existence
- whether the diff remains limited to authorized SQL/test/handoff scope

## Next Recommended Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for issue #191, Analytics
derived SQL views, under tracker #190.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/190
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/191
- Branch: codex/analytics-foundation
- Contract: docs/contracts/analytics_derived_sql_views.md
- Implementation handoff: docs/implementation_handoffs/analytics_derived_sql_views_comparison.md
- Risk tier: Medium-High

Review:
- docs/contracts/analytics_derived_sql_views.md
- docs/implementation_handoffs/analytics_derived_sql_views_comparison.md
- src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql
- tests/test_analytics_schema.py
- tests/test_analytics_derived_views.py
- tests/test_analytics_migration_loader.py
- tests/test_analytics_parser_normalized_replay_ingest.py
- tests/test_analytics_gameplay_action_ingest.py
- tests/test_analytics_opponent_card_observation_ingest.py
- tests/test_analytics_field_evidence_ingest.py

Confirm:
- existing seven view names remain available
- only approved new views were added: v_gameplay_action_review and v_opponent_card_observation_review
- view definitions are deterministic, read-only, and local-only
- unknown, unavailable, degraded, and non-win/loss results are not silently treated as clean losses
- matchup labels remain human annotations, not parser or archetype truth
- analytics views do not become parser truth, AI truth, merge readiness, deploy readiness, gameplay advice, player-mistake labels, hidden-card inference, or coaching output
- tests prove representative behavior, not only view existence
- no generated SQLite/local/private artifacts, raw Player.log payloads, secrets, runtime artifacts, retry-queue artifacts, or workbook exports are included

Validation:
- python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
- python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py
- python3 -m pytest -q tests/test_analytics_derived_views.py
- python3 -m ruff check src tests tools
- git diff --check

Output findings first, then verdict, validation results, remaining gaps,
recommended next role, and workflow_handoff block.

Do not edit implementation code in review-only mode.
Do not target main directly.
Do not change parser behavior, parser state final reconciliation, parser event
classes, runtime behavior, workbook schema, webhook payload shape, Apps Script
behavior, output transport, Match Journal behavior, overlay behavior, Google
Sheets behavior, AI/OpenAI behavior, CI gates, merge policy, or deploy policy.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/191"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/190"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/analytics_derived_sql_views.md"
  target_artifact: "src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql; tests/test_analytics_derived_views.py; docs/implementation_handoffs/analytics_derived_sql_views_comparison.md; docs/contract_test_reports/analytics_derived_sql_views.md"
  verdict: "blocking_finding_fixed_ready_for_contract_review"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "python3 -m pytest -q tests/test_analytics_derived_views.py -> 8 passed"
    - "python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py -> 27 passed"
    - "python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py -> 101 passed"
    - "python3 -m ruff check src tests tools -> All checks passed"
    - "git diff --check -> passed"
    - "path-scoped secret/private marker check for SQL, tests, contract, report, and handoff -> passed"
    - "path-scoped protected-surface check for SQL, tests, contract, report, and handoff -> passed"
    - "python3 -m pytest -q -> 1348 passed"
  stop_conditions:
    - "Do not target main directly."
    - "Do not store raw Player.log payloads or commit SQLite/local/generated/private artifacts."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, runtime behavior, workbook schema, webhook payload shape, Apps Script behavior, output transport, AI/OpenAI behavior, Match Journal behavior, overlay behavior, Google Sheets behavior, CI gates, merge policy, or deploy policy."
    - "Do not let analytics views become parser truth, merge readiness, deploy readiness, gameplay advice, player-mistake labels, hidden-card inference, archetype classification, or AI coaching."
```
