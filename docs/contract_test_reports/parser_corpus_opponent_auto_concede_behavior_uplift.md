# Parser Corpus Opponent Auto-Concede Behavior Uplift Report

## Verdict

`gameplay_stress.opponent_auto_concede` has one reduced synthetic
parser-behavior uplift ready for Codex E review.

The evidence is narrow. It proves a Mythic Edge-owned synthetic early game-end
result/reconciliation path through golden replay and the normal parser path. It
does not claim opponent intent, hidden-action absence, no-action truth,
timeout/disconnect reason, private smoke success, readiness, analytics truth,
AI truth, coaching truth, tracker completion, or #388/#381 activation.

## Evidence Added

- Synthetic fixture:
  `tests/fixtures/opponent_auto_concede_early_game_end_synthetic_slice.log`
- Golden replay manifest:
  `tests/fixtures/golden_replay/opponent_auto_concede_early_game_end_synthetic.manifest.json`
- Corpus manifest entry:
  `opponent_auto_concede_early_game_end_synthetic_v1`
- Session-ledger entry:
  `opponent_auto_concede_early_game_end_synthetic_v1`
- Codex D feature-equity baseline update:
  `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`

The #406 entry `opponent_auto_concede_boundary_report_v1` remains present and
report-only.

## Parser-Owned Evidence

The new golden replay manifest expects and verifies:

- `MatchState`: 1
- `GameState`: 2
- `GameResult`: 1
- event kind sequence: `MatchState`, `GameState`, `GameState`, `GameResult`
- unknown entries: 0
- truncation events: 0
- parser failures: 0
- match winner team: 1
- match result reason: `ResultReason_Concede`
- game results: one game with result `W`
- match-log row present
- one game-log row present

The parser-owned row evidence keeps the claim to existing parser outputs:

- `MTGA Format`: `Standard`
- `MTGA Queue Type`: `Best of 1`
- `Match Win?`: `W`
- `Game 1 Result`: `W`
- `G1 Turn Count`: 1
- `G1 Play / Draw`: `Draw`

## Corpus Status Effect

Before issue #482:

```yaml
gameplay_stress.opponent_auto_concede:
  coverage_status: "covered_report_only"
  coverage_basis:
    - "fixture_metadata_only"
  mythic_edge_entries:
    - "opponent_auto_concede_boundary_report_v1"
```

After issue #482:

```yaml
gameplay_stress.opponent_auto_concede:
  coverage_status: "covered_synthetic"
  coverage_basis:
    - "fixture_metadata_only"
    - "parser_behavior_verified"
  mythic_edge_entries:
    - "opponent_auto_concede_boundary_report_v1"
    - "opponent_auto_concede_early_game_end_synthetic_v1"
```

Current overall corpus summary:

```yaml
total_scenario_families: 45
covered_committed: 6
covered_synthetic: 16
covered_report_only: 17
blocked_private_evidence: 2
blocked_external_boundary: 4
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
```

## Privacy And Protected Boundaries

- No private Player.log, UTC_Log, app-data, live MTGA, private smoke, network,
  Manasight raw log, or external corpus input was used.
- No parser behavior, parser state final reconciliation, parser event classes,
  router semantics, match/game identity, deduplication, diagnostics behavior,
  feature-equity behavior, evidence-ledger behavior, workbook schema, webhook
  payload shape, Apps Script behavior, Google Sheets sync, output transport,
  analytics truth, AI truth, coaching behavior, release readiness, production
  behavior, CI gates, merge readiness, deploy readiness, or final integration
  policy changed.
- The #406 report-only row was preserved.

## Non-Claims

This report does not claim:

- opponent intent;
- concession motive;
- hidden-action absence;
- no-action truth;
- timeout reason;
- disconnection reason;
- network behavior;
- player mistakes;
- archetype truth;
- hidden-card truth;
- decklist truth;
- gameplay advice;
- analytics truth;
- AI truth;
- coaching truth;
- private smoke success;
- release readiness;
- production behavior;
- full corpus parity;
- tracker completion;
- #388 or #381 activation.

## Validation

- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_golden_replay_harness.py`
  passed: 22 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py`
  passed: 7 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_harness.py`
  passed: 15 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_gre_game_result_parser.py tests/test_gre_game_state_parser.py tests/test_state.py`
  passed: 49 tests.
- Codex D reran
  `PYTHONPATH=src python3 -m pytest -q tests/test_feature_equity_corpus_ratchet.py`
  after fixing the baseline drift; passed: 7 tests.
- Codex D reran
  `PYTHONPATH=src python3 -m mythic_edge_parser.app.feature_equity_corpus_ratchet tests/fixtures/golden_replay --baseline tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`;
  passed and printed:
  `Feature-equity corpus ratchet: ok (5 manifests, 5 source files)`.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=16, report_only=17, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay`
  passed and printed:
  `Golden replay: pass (5 manifests, 5 pass, 0 degraded, 0 review, 0 diff, 0 fail)`.
- `python3 tools/check_agent_docs.py` passed.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.
- Path-scoped secret/private-marker scan completed with exit code 0,
  forbidden 0, warnings 7. Warnings were the expected sanitized fixture-marker
  lines in the synthetic Player.log-shaped fixture plus pre-existing placeholder
  warnings in `tests/test_golden_replay_harness.py`; no secret or private
  artifact was committed.
- Path-scoped protected-surface scan passed: forbidden 0, warnings 0.
- ASCII scan over changed files passed.
- Trailing-whitespace scan over changed files passed.
- Generated SQLite/local DB artifact scan returned no files.
- Codex D ran `PYTHONPATH=src python3 -m pytest -q tests`; passed: 1772
  tests.

## Residual Risks

- The new evidence is synthetic and proves one reduced early game-end
  result/reconciliation path only.
- It does not prove real Arena opponent auto-concede behavior, opponent
  intent, hidden-action absence, no-action truth, timeout cause, disconnect
  cause, live private behavior, analytics truth, AI truth, coaching truth,
  release readiness, production behavior, or full corpus parity.
- Overall corpus readiness remains blocked by report-only, private-evidence,
  and external-boundary rows.
