# Parser Corpus Behavior Readiness Applicability Semantics Comparison

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/477
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/475
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/476
- Previous merge commit: `ad222e4bad8209a6baad631f1769ad273ff031b0`
- Branch: `codex/parser-corpus-behavior-readiness-applicability-477`
- Base branch: `main`
- Source artifact:
  `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- Risk tier: High

## Contract Comparison

The contract asked for an additive applicability-aware parser-behavior
readiness metric without changing existing all-family readiness fields,
coverage statuses, corpus manifest rows, session-ledger rows, parser behavior,
or #388 / #381 activation semantics.

The implementation adds `readiness_metrics.behavior_applicability` to the
existing corpus parity report. Existing top-level report fields, `summary`,
all existing `readiness_metrics` keys, status values, matrix rows, and CLI
output remain backward compatible.

## Changes Made

- Added `parser_corpus_behavior_applicability.v1` derived metrics in
  `src/mythic_edge_parser/app/corpus_parity_report.py`.
- Added a deterministic non-behavior excluded-family mapping for the eight
  contracted non-behavior rows.
- Added focused assertions in `tests/test_corpus_parity_report.py` for:
  - 37 behavior-applicable families;
  - 19 behavior-applicable ready families;
  - 18 behavior-applicable not-ready families;
  - 8 non-behavior-applicability excluded families;
  - one applicable private blocker;
  - four applicable external-boundary blockers;
  - #388 activation remaining false.
- Added this implementation handoff.
- Added `docs/contract_test_reports/parser_corpus_behavior_readiness_applicability_semantics.md`.

## Current Derived Metrics

```yaml
readiness_metrics:
  behavior_applicability:
    schema_version: "parser_corpus_behavior_applicability.v1"
    parser_behavior_applicable_family_count: 37
    parser_behavior_applicable_ready_family_count: 19
    parser_behavior_applicable_not_ready_family_count: 18
    parser_behavior_not_applicable_family_count: 8
    parser_behavior_applicable_report_only_family_count: 13
    parser_behavior_applicable_blocked_private_evidence_family_count: 1
    parser_behavior_applicable_blocked_external_boundary_family_count: 4
    parser_behavior_applicability_ready: false
    parser_behavior_applicability_verdict: "applicable_families_not_behavior_ready"
```

Existing all-family readiness remains false:

- `parser_behavior_ready: false`
- `pipeline_activation_ready_for_issue_388: false`

## Validation Run

- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py`
  passed: 7 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  passed and printed:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=14, report_only=19, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`.
- `python3 tools/check_agent_docs.py` passed.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.
- Path-scoped secret/private marker scan passed for the changed files.
- Path-scoped protected-surface gate passed for the changed files.
- ASCII scan passed for the changed files.
- Generated SQLite artifact scan returned no files.

## Residual Risks

- Applicability-aware metrics are derived report metadata, not parser truth.
- `parser_behavior_applicability_ready` is false and must not activate #388 or
  #381 by itself.
- The legacy all-family #388 activation gate remains false.
- Report-only, private-evidence, and external-boundary rows were not promoted.
- Corpus manifest and session-ledger statuses were not changed.
- Private/live/UTC_Log/Player.log/app-data/firewall/network checks were not
  run.
- This does not claim full corpus parity, parser support, private smoke
  success, release readiness, deploy readiness, production behavior, analytics
  truth, AI truth, coaching truth, or tracker completion.

## Next Recommended Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #477, parser corpus behavior
readiness applicability semantics, under tracker #158.

Review:
- docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md
- src/mythic_edge_parser/app/corpus_parity_report.py
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_behavior_readiness_applicability_semantics_comparison.md
- docs/contract_test_reports/parser_corpus_behavior_readiness_applicability_semantics.md

Verify that the implementation adds only additive applicability-aware derived
metrics under readiness_metrics.behavior_applicability, preserves existing
summary/readiness/status/CLI behavior, preserves corpus manifest and
session-ledger statuses, keeps #388/#381 activation false, and does not change
parser behavior or parser-owned truth.

Pay special attention to the contracted current counts:
- total_scenario_families: 45
- parser_behavior_applicable_family_count: 37
- parser_behavior_applicable_ready_family_count: 19
- parser_behavior_applicable_not_ready_family_count: 18
- parser_behavior_not_applicable_family_count: 8

Do not target main directly. Do not activate #388 or #381. Do not run private
or live checks. Do not claim parser support, full corpus parity, private smoke
success, release readiness, production behavior, analytics truth, AI truth,
coaching truth, or tracker completion.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/477"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/475"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/476"
  previous_merge_commit: "ad222e4bad8209a6baad631f1769ad273ff031b0"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_behavior_readiness_applicability_semantics_comparison.md"
  report_artifact: "docs/contract_test_reports/parser_corpus_behavior_readiness_applicability_semantics.md"
  verdict: "parser_behavior_readiness_applicability_metrics_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-behavior-readiness-applicability-477"
  base_branch: "main"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  parser_behavior_applicability_ready: false
  recommended_next_role: "Codex E: Module Reviewer"
```
