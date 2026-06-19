# Parser Corpus Draft With Games Behavior Uplift Handoff

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/479
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/477
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/478
- Previous merge commit: `8288dfbe7548d82eb3c02cb5f9baf1e8b8dab0f0`
- Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/400
- Branch: `codex/parser-corpus-draft-with-games-behavior-uplift-479`
- Base branch: `main`
- Source artifact:
  `docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md`
- Risk tier: High

## Contract Comparison

The contract authorized moving only `core_gameplay.draft_with_games` beyond
the #400 report-only boundary if a Mythic Edge-owned synthetic fixture could
prove draft event evidence plus completed limited game/result flow through the
normal parser and golden replay path.

That condition is satisfied for one reduced synthetic scenario:

- the new fixture emits `DraftBot`, `DraftComplete`, `MatchState`,
  `GameState`, and `GameResult`;
- final reconciliation records one game result and a match winner;
- parser-owned match and game rows are present;
- golden replay reports all expected sections as passing;
- unknown, truncation, data-loss, and degradation counts are zero.

The existing `draft_with_games_boundary_report_v1` entry from issue #400
remains report-only non-claim metadata. No parser source or parser behavior was
changed.

## Changes Made

- Added `tests/fixtures/draft_with_games_synthetic_slice.log`, a reduced
  synthetic draft-with-games replay slice.
- Added
  `tests/fixtures/golden_replay/draft_with_games_synthetic.manifest.json`.
- Added `draft_with_games_synthetic_v1` to
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.
- Added `draft_with_games_synthetic_v1` to
  `tests/fixtures/parser_corpus/session_ledger.v1.json`.
- Updated `tests/test_golden_replay_harness.py` to include the new committed
  manifest and assert the draft-with-games expected shape.
- Updated `tests/test_corpus_parity_report.py` to pin the new manifest,
  session-ledger row, matrix row, and readiness count movement.
- Codex D follow-up updated
  `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`
  and `tests/test_feature_equity_corpus_ratchet.py` so the reviewed
  count-only baseline includes the new synthetic draft-with-games manifest.
- Added this handoff.
- Added
  `docs/contract_test_reports/parser_corpus_draft_with_games_behavior_uplift.md`.

## Status Movement

Only one scenario family changed status:

| Scenario family | Before | After |
| --- | --- | --- |
| `core_gameplay.draft_with_games` | `covered_report_only` | `covered_synthetic` |

The resulting corpus parity summary is:

```yaml
total_scenario_families: 45
covered_committed: 6
covered_synthetic: 15
covered_report_only: 18
blocked_private_evidence: 2
blocked_external_boundary: 4
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
```

Applicability-aware readiness now counts 20 applicable ready families and 17
applicable not-ready families. The corpus is still not behavior-ready and does
not activate #388 or #381.

## Preserved Boundaries

- No parser behavior, parser state final reconciliation, parser event classes,
  router semantics, match/game identity, deduplication, diagnostics behavior,
  feature-equity behavior, evidence-ledger behavior, workbook schema, webhook
  payload shape, Apps Script behavior, Google Sheets sync, output transport,
  analytics truth, AI truth, coaching behavior, release readiness, production
  behavior, CI gates, merge readiness, deploy readiness, or final integration
  policy was changed.
- The existing draft-only fixture and manifest were not mutated.
- No private Player.log, UTC_Log, app-data, live MTGA, draft, network, private
  smoke, Manasight raw log, or external corpus evidence was used.
- The new fixture does not claim draft pick quality, deck construction,
  decklist truth, archetype truth, hidden-card truth, gameplay advice,
  analytics truth, AI truth, coaching truth, release readiness, production
  behavior, full corpus parity, tracker completion, or #388/#381 activation.

## Validation Run

- `PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_corpus_parity_report.py`
  passed: 21 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py`
  passed: 7 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py`
  passed: 14 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_draft_bot_parser.py tests/test_draft_human_parser.py tests/test_draft_complete_parser.py`
  passed: 115 tests.
- Codex D reran
  `PYTHONPATH=src python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py`
  after fixing the baseline drift; passed: 7 tests.
- Codex D reran
  `PYTHONPATH=src python3 -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests/fixtures/golden_replay --baseline tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`;
  passed and printed:
  `Feature-equity corpus ratchet: ok (4 manifests, 4 source files)`.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=15, report_only=18, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`.
- `python3 tools/check_agent_docs.py` passed: checked files 34,
  errors 0, warnings 0.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.
- Path-scoped secret/private-marker scan completed with exit code 0,
  forbidden 0, warnings 9. Warnings were sanitized fixture-marker lines in the
  new synthetic fixture plus pre-existing placeholder warnings in
  `tests/test_golden_replay_harness.py`; no secret or private artifact was
  committed.
- Path-scoped protected-surface scan passed: forbidden 0, warnings 0.
- ASCII scan over changed files found no non-ASCII characters.
- Generated SQLite/local DB artifact scan returned no files.
- Codex D ran `PYTHONPATH=src python3 -m pytest -q tests`; passed: 1771
  tests.

## Residual Risks

- The new evidence is synthetic and proves only one reduced completed
  draft-with-games path.
- It does not prove all Arena draft queues, BO3 draft, sideboarding, deck
  construction, draft pick quality, draft pool truth, decklists, live private
  draft behavior, private smoke success, release readiness, production
  behavior, analytics truth, AI truth, or coaching truth.
- Remaining report-only, private-evidence, and external-boundary rows keep the
  overall corpus from parser-behavior readiness.

## Next Recommended Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #479, draft-with-games behavior
uplift under tracker #158.

Review:
- docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md
- tests/fixtures/draft_with_games_synthetic_slice.log
- tests/fixtures/golden_replay/draft_with_games_synthetic.manifest.json
- tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_golden_replay_harness.py
- tests/test_corpus_parity_report.py
- tests/test_feature_equity_corpus_ratchet.py
- docs/implementation_handoffs/parser_corpus_draft_with_games_behavior_uplift_comparison.md
- docs/contract_test_reports/parser_corpus_draft_with_games_behavior_uplift.md

Verify that core_gameplay.draft_with_games is promoted only by the new owned
synthetic golden replay evidence, that draft_with_games_boundary_report_v1
remains report-only non-claim metadata, and that no parser behavior or protected
downstream surface changed.

Do not target main directly. Do not close tracker #158. Do not activate #388 or
#381. Do not run private/live checks. Do not claim full corpus parity, release
readiness, production behavior, analytics truth, AI truth, or coaching truth.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/479"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/477"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/478"
  previous_merge_commit: "8288dfbe7548d82eb3c02cb5f9baf1e8b8dab0f0"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/400"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_draft_with_games_behavior_uplift.md"
  target_artifact: "tests/fixtures/golden_replay/draft_with_games_synthetic.manifest.json; tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json"
  report_artifact: "docs/contract_test_reports/parser_corpus_draft_with_games_behavior_uplift.md"
  verdict: "draft_with_games_feature_equity_baseline_fix_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-draft-with-games-behavior-uplift-479"
  base_branch: "main"
  selected_family: "core_gameplay.draft_with_games"
  prior_status: "covered_report_only"
  current_status: "covered_synthetic"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  recommended_next_role: "Codex E: Module Reviewer"
```
