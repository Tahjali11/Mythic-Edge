# Analytics Replay/View Validation Harness Contract Test Report

## Findings

No blocking findings.

No non-blocking implementation findings were identified.

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/193>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/190>

## Contract

`docs/contracts/analytics_replay_view_validation_harness.md`

## Implementation Under Test

Branch: `codex/analytics-foundation`

Changed files reviewed:

- `docs/contracts/analytics_replay_view_validation_harness.md`
- `docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md`
- `tests/test_analytics_replay_view_harness.py`

Reference surfaces reviewed:

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `tests/test_analytics_derived_views.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_analytics_opponent_card_observation_ingest.py`
- `tests/test_analytics_field_evidence_ingest.py`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The implementation must add a narrow, test-only replay-to-view validation harness. The harness must use inline sanitized/synthetic parser-normalized replay input, ingest it into in-memory SQLite through `ingest_parser_normalized_replay(...)`, query deterministic derived SQL views, prove repeated-ingest idempotency, and preserve identity/provenance/degradation/review labels where current view shapes expose them. It must not add production interfaces, generated databases, raw Player.log storage, parser/runtime/workbook/webhook/App Script behavior, Match Journal/overlay/Google Sheets behavior, AI/OpenAI behavior, CI gates, merge/deploy authority, gameplay advice, or parser/analytics truth claims.

## Checks Run

```bash
python3 -m pytest -q tests/test_analytics_replay_view_harness.py
python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_derived_views.py
python3 -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py
python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' \
  docs/contracts/analytics_replay_view_validation_harness.md \
  tests/test_analytics_replay_view_harness.py \
  docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
printf '%s\n' \
  docs/contracts/analytics_replay_view_validation_harness.md \
  tests/test_analytics_replay_view_harness.py \
  docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
find data -type f \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*-wal' -o -name '*-shm' -o -name '*-journal' \) -print
git diff --no-index --check /dev/null docs/contracts/analytics_replay_view_validation_harness.md
git diff --no-index --check /dev/null tests/test_analytics_replay_view_harness.py
git diff --no-index --check /dev/null docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md
python3 -m pytest -q
```

## Results

- `tests/test_analytics_replay_view_harness.py`: 2 passed.
- Parser-normalized replay ingest plus derived-view suite: 32 passed.
- Gameplay-action, opponent-observation, and field-evidence ingest suite: 77 passed.
- Schema and migration loader suite: 27 passed.
- `python3 -m ruff check src tests tools`: passed.
- `git diff --check`: passed.
- Path-scoped secret/private marker scan: passed, 3 scanned paths, 0 forbidden, 0 warnings.
- Path-scoped protected-surface gate: passed, 3 changed paths, 0 forbidden, 0 warnings.
- SQLite artifact scan: passed with no output.
- No-index whitespace checks for the three untracked files produced no whitespace-error output; exit status `1` was the expected diff-present status for added files.
- Full pytest: 1350 passed.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| none | none | none | none | not_blocking | No findings recorded. | Focused, adjacent, safety, artifact, and full-suite validation passed. | F |

## Confirmed Contract Matches

- The implementation is test-only: no production module, CLI, environment-variable contract, default database opener, runtime ingest path, saved replay runner change, golden replay change, webhook sender, Apps Script interaction, Match Journal/overlay integration, Google Sheets sync, OpenAI/model-provider interface, CI gate, merge-policy gate, or deploy-policy gate was added.
- The harness uses `sqlite3.connect(":memory:")` and inline synthetic replay data.
- The replay uses the contracted safe labels: `source_kind = "sanitized_golden_replay"` and `source_artifact_label = "analytics_replay_view_harness_v1"`.
- The primary test calls `ingest_parser_normalized_replay(...)` and then queries derived views. It does not insert parser fact rows directly into source tables.
- The representative replay covers one synthetic match with two games, preboard/postboard labels, play/draw labels, one known win, one known loss, opening-hand card names, one observed mulligan count of `1`, one observed mulligan count of `0`, turn counts, durations, queue/format/event/sync labels, two gameplay actions, one linked opponent observation, and one canonical field-evidence entry.
- The harness queries the required views: `v_opening_hand_cards`, `v_opening_lines`, `v_gameplay_action_review`, `v_mulligan_outcomes`, `v_game1_vs_postboard`, `v_play_draw_splits`, `v_sample_size_warnings`, and `v_opponent_card_observation_review`.
- The harness verifies opening-hand identity/provenance, mulligan zero-vs-observed semantics, opening-line filtering, broader gameplay-action review coverage, game1/postboard context, play/draw split math, deterministic sample-size warnings, opponent-observation degradation/review context, and field-evidence preservation.
- The idempotency test ingests the same replay twice and verifies stable `ingest_run_id`, `row_counts`, fact table counts, selected view snapshots, nonduplicated field-evidence rows, and a single `ingest_runs` row.
- The harness keeps human matchup-label performance out of the parser-normalized replay path, which matches the contract because human annotations are not required replay input and remain covered by `tests/test_analytics_derived_views.py`.
- No raw Player.log payloads, local log paths, generated SQLite artifacts, runtime artifacts, failed posts, workbook exports, secrets, credentials, tokens, webhook URLs, hidden-card inference, decklist completion, archetype classification, player-mistake labels, gameplay advice, coaching text, parser truth claims, analytics truth claims, merge-readiness claims, or deploy-readiness claims were introduced.

## Contract Mismatches

- None.

## Missing Tests

- None blocking.

## Drift Notes

- Worktree is on `codex/analytics-foundation`.
- Before this report, the only changed/untracked files were the expected contract, handoff, and test harness files.
- After this report, the added report file is the only additional Codex E artifact.
- No repo drift, workbook drift, deployment drift, local-data drift, issue lifecycle drift, PR lifecycle drift, or tracker drift was found.

## Remaining Risks

- GitHub Actions were not run locally.
- The harness is representative validation evidence only. It does not decide parser truth, analytics truth, merge readiness, deploy readiness, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, or AI coaching.
- Future historical replay fixtures and broader analytics consumers remain deferred to later contracts.

## Recommendation

Approve for Codex F submission.

## Next Workflow Action

Next role: Codex F: Module Submitter.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/193"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/190"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/analytics_replay_view_validation_harness.md"
  target_artifact: "Codex F submission package for issue #193"
  verdict: "no_blocking_findings_ready_for_codex_f"
  risk_tier: "Medium"
  branch: "codex/analytics-foundation"
  validation:
    - "python3 -m pytest -q tests/test_analytics_replay_view_harness.py -> 2 passed"
    - "python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_derived_views.py -> 32 passed"
    - "python3 -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py -> 77 passed"
    - "python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py -> 27 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "path-scoped secret/private marker scan -> passed"
    - "path-scoped protected-surface gate -> passed"
    - "SQLite artifact scan -> passed with no output"
    - "no-index whitespace checks for untracked contract/test/handoff files -> no whitespace-error output"
    - "python3 -m pytest -q -> 1350 passed"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #190 or issue #193."
    - "Do not create or commit SQLite database files, WAL, SHM, journal files, raw logs, generated data, runtime artifacts, failed posts, workbook exports, secrets, credentials, API keys, tokens, or webhook URLs."
    - "Do not store raw Player.log payloads in SQLite."
    - "Do not change parser/runtime/workbook/webhook/App Script/AI/OpenAI/Match Journal/overlay/Google Sheets behavior."
    - "Do not let analytics views or analytics harnesses become parser truth, merge readiness, deploy readiness, gameplay advice, player-mistake labels, hidden-card inference, archetype classification, or AI coaching."
```
