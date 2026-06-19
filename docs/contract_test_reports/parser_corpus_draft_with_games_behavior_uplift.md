# Parser Corpus Draft With Games Behavior Uplift Report

## Verdict

`core_gameplay.draft_with_games` has one reduced synthetic parser-behavior
uplift ready for Codex E review.

The new evidence is narrow. It proves a Mythic Edge-owned synthetic
draft-with-games path through golden replay and the normal parser path. It does
not claim broad draft support, private draft behavior, release readiness,
production behavior, analytics truth, AI truth, coaching truth, tracker
completion, or #388/#381 activation.

## Evidence Added

- Synthetic fixture:
  `tests/fixtures/draft_with_games_synthetic_slice.log`
- Golden replay manifest:
  `tests/fixtures/golden_replay/draft_with_games_synthetic.manifest.json`
- Corpus manifest entry:
  `draft_with_games_synthetic_v1`
- Session-ledger entry:
  `draft_with_games_synthetic_v1`
- Codex D feature-equity baseline update:
  `tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json`

The #400 entry `draft_with_games_boundary_report_v1` remains present and
report-only.

## Parser-Owned Evidence

The new golden replay manifest expects and verifies:

- `DraftBot`: 1
- `DraftComplete`: 1
- `MatchState`: 1
- `GameState`: 2
- `GameResult`: 1
- unknown entries: 0
- truncation events: 0
- parser failures: 0
- match winner team: 1
- game results: one game with result `W`
- match-log row present
- one game-log row present

The parser-owned row evidence keeps format/queue context limited to the
existing parser outputs:

- `MTGA Format`: `Limited`
- `MTGA Queue Type`: `Best of 1`

## Corpus Status Effect

Before issue #479:

```yaml
core_gameplay.draft_with_games:
  coverage_status: "covered_report_only"
  coverage_basis:
    - "fixture_metadata_only"
```

After issue #479:

```yaml
core_gameplay.draft_with_games:
  coverage_status: "covered_synthetic"
  coverage_basis:
    - "fixture_metadata_only"
    - "parser_behavior_verified"
  mythic_edge_entries:
    - "draft_with_games_boundary_report_v1"
    - "draft_with_games_synthetic_v1"
```

Current overall corpus summary:

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

## Privacy And Protected Boundaries

- No private Player.log, UTC_Log, app-data, live MTGA, private smoke, firewall,
  network, Manasight raw log, or external corpus input was used.
- No parser behavior, parser state final reconciliation, parser event classes,
  router semantics, match/game identity, deduplication, workbook schema,
  webhook payload shape, Apps Script behavior, Google Sheets sync, output
  transport, analytics truth, AI truth, coaching behavior, release readiness,
  production behavior, CI gates, merge readiness, deploy readiness, or final
  integration policy changed.
- The current draft-only fixture was not mutated.

## Non-Claims

This report does not claim:

- all Arena draft queues;
- BO3 draft support;
- sideboarding support;
- draft deck construction truth;
- draft pick quality;
- draft pool truth;
- submitted decklist truth;
- archetype truth;
- hidden-card truth;
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
- `python3 tools/check_agent_docs.py` passed.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.
- Path-scoped secret/private-marker scan completed with exit code 0,
  forbidden 0, warnings 9. Warnings were sanitized fixture-marker lines in the
  new synthetic fixture plus pre-existing placeholder warnings in
  `tests/test_golden_replay_harness.py`.
- Path-scoped protected-surface scan passed with forbidden 0 and warnings 0.
- ASCII scan over changed files found no non-ASCII characters.
- Generated SQLite/local DB artifact scan returned no files.
- Codex D ran `PYTHONPATH=src python3 -m pytest -q tests`; passed: 1771
  tests.
