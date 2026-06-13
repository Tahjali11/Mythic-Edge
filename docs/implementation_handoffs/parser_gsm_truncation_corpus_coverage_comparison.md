# Parser GSM Truncation Corpus Coverage Implementation Comparison

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/351
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- source_artifact: docs/contracts/parser_gsm_truncation_corpus_coverage.md
- target_artifact: docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md
- branch: codex/gsm-truncation-corpus-coverage
- role: Codex C / Module Implementer
- risk_tier: High
- verdict: implementation_ready_for_module_review
- Related ADRs: N/A

## Comparison Summary

The current corpus parity package already had the schema vocabulary needed for
this issue: `covered_synthetic`, `parser_behavior_verified`,
`fixture_metadata_only`, `diagnostics_only`, and the
`drift_debug.gsm_truncation` scenario family. No corpus-report source change
was required.

Before implementation, the corpus parity report showed:

- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 1
- partial: 4
- missing: 28
- blocked_external_boundary: 6
- `drift_debug.gsm_truncation`: `partial`
- GSM row entries: `feature_equity_corpus_baseline_v1`
- GSM row basis: `count_ratchet_only`

After implementation, the corpus parity report shows:

- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 2
- partial: 3
- missing: 28
- blocked_external_boundary: 6
- `drift_debug.gsm_truncation`: `covered_synthetic`
- GSM row entries:
  - `feature_equity_corpus_baseline_v1`
  - `gsm_truncation_marker_synthetic_v1`
- GSM row basis:
  - `count_ratchet_only`
  - `diagnostics_only`
  - `fixture_metadata_only`
  - `parser_behavior_verified`

This is still report metadata only. It does not claim recovered GameState data,
real-log corpus coverage, parser correctness, merge readiness, deploy
readiness, tracker completion, analytics truth, workbook truth, or AI truth.

## Changes Made

- Added `gsm_truncation_marker_synthetic_v1` to
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.
- Added matching session-ledger metadata to
  `tests/fixtures/parser_corpus/session_ledger.v1.json`.
- Updated `tests/test_corpus_parity_report.py` to validate the new manifest and
  session entry, the summary delta, and the exact GSM truncation report row.
- Added this handoff at
  `docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md`.

## Protected Boundaries Preserved

- No parser behavior changes.
- No `TruncationEvent` shape changes.
- No router, diagnostics, golden replay, replay, final reconciliation, workbook,
  webhook, Apps Script, Google Sheets, output transport, analytics, AI, local
  app, or production behavior changes.
- No raw/private Player.log excerpts, external corpus files, local logs,
  generated data, runtime artifacts, SQLite artifacts, workbook exports,
  credentials, tokens, keys, or webhook URLs were added.
- The GSM truncation entry stays `covered_synthetic`, not `covered_committed`.
- The new session ledger entry explicitly records zero game rows and states that
  truncation coverage does not recover omitted game facts.

## Validation Run

- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  - passed
- `python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gsm_truncation_parser.py`
  - passed: 14 passed
- `python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_entry_buffer_edges.py tests/test_router_unit.py`
  - passed: 38 passed
- `python3 -m ruff check src tests tools`
  - passed
- `python3 tools/check_agent_docs.py`
  - passed
- `git diff --check`
  - passed with no output for tracked local modifications
- untracked docs whitespace check with `git diff --no-index --check`
  - passed with no whitespace output for the untracked contract and handoff
- `git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`
  - passed with scanned_paths: 0 because this Codex C work is uncommitted
- `git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`
  - passed with changed_paths: 0 because this Codex C work is uncommitted
- `git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin`
  - selection_status: ok with zero_changed_paths advisory
- explicit changed-file secret/private marker scan:
  - passed: scanned_paths: 5, forbidden: 0, warnings: 0
- explicit changed-file protected-surface gate:
  - passed: changed_paths: 5, forbidden: 0, warnings: 0
- explicit changed-file validation selector:
  - selection_status: ok
  - required checks: focused corpus test, Ruff, diff check,
    secret/private-marker scan, protected-surface gate
  - recommended check: agent docs checker

## Remaining Risks

- The broader corpus parity tracker remains incomplete; many scenario families
  are still missing, partial, or blocked by external-boundary constraints.
- This issue does not add a golden replay truncation fixture or update the
  feature-equity baseline. Future work may choose either path under a separate
  contract.
- A future sanitized real-log fixture would require separate provenance and
  privacy review before any `covered_committed` status could be justified.
- `git diff --name-only origin/main...HEAD` reflects committed branch
  differences only. Because this Codex C work is intentionally unstaged and
  uncommitted, explicit changed-file scans are needed for actual local edits.

## Still-Unverified Layers

- No CI run was inspected.
- No PR was opened.
- No tracker update was performed.
- No runtime, workbook, Apps Script, analytics, AI, local app, or production
  behavior was exercised because those layers are outside this contract.

## Next Recommended Role

Codex E / Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #351 under tracker #158.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/351

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Branch:
codex/gsm-truncation-corpus-coverage

Contract:
docs/contracts/parser_gsm_truncation_corpus_coverage.md

Implementation handoff:
docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md

Review focus:
- Verify the implementation is metadata/test-only.
- Verify `drift_debug.gsm_truncation` is `covered_synthetic`, not
  `covered_committed`.
- Verify the GSM row combines the feature-equity baseline and
  `gsm_truncation_marker_synthetic_v1` entry.
- Verify no parser behavior, TruncationEvent shape, router, diagnostics,
  golden replay, replay, workbook, webhook, Apps Script, analytics, AI, or
  production behavior changed.
- Verify no raw/private logs, external corpus files, generated artifacts,
  SQLite files, workbook exports, credentials, tokens, keys, or webhook URLs
  were added.
- Verify report wording keeps truncation as data-loss evidence only and does
  not claim recovered GameState truth.

Validation to review or rerun:
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gsm_truncation_parser.py
- python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_entry_buffer_edges.py tests/test_router_unit.py
- python3 -m ruff check src tests tools
- python3 tools/check_agent_docs.py
- git diff --check
- path-scoped secret/private-marker and protected-surface checks for changed files
- path-scoped validation selector for changed files

Do not:
- Target main directly.
- Change parser behavior or protected downstream surfaces.
- Add raw/private/external/generated/local artifacts.
- Mark tracker #158 complete.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/351"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_gsm_truncation_corpus_coverage.md"
  target_artifact: "docs/implementation_handoffs/parser_gsm_truncation_corpus_coverage_comparison.md"
  verdict: "implementation_ready_for_module_review"
  risk_tier: "High"
  branch: "codex/gsm-truncation-corpus-coverage"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_gsm_truncation_parser.py"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_entry_buffer_edges.py tests/test_router_unit.py"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan for changed files"
    - "path-scoped protected-surface gate for changed files"
    - "path-scoped validation selector for changed files"
  stop_conditions:
    - "Do not change parser behavior, TruncationEvent shape, router behavior, diagnostics behavior, replay behavior, workbook schema, webhook payload shape, Apps Script behavior, analytics truth, AI truth, or production behavior."
    - "Do not commit raw/private Player.log excerpts, external raw corpora, local logs, generated data, runtime artifacts, SQLite files, workbook exports, credentials, tokens, keys, or webhook URLs."
    - "Do not reconstruct missing GameState data from truncation markers."
    - "Do not broaden this issue beyond GSM truncation/data-loss corpus coverage."
    - "Do not close tracker #158."
```
