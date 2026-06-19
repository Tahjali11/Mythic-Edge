# Parser Corpus Behavior Readiness Applicability Semantics Report

## Verdict

`readiness_metrics.behavior_applicability` is implemented and ready for Codex E
review.

This report does not claim full corpus parity, parser support, private smoke
success, release readiness, deploy readiness, production behavior, analytics
truth, AI truth, coaching truth, tracker completion, or activation of issue
#388 or issue #381.

## Evidence Summary

- Source contract:
  `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- Additive report section:
  `readiness_metrics.behavior_applicability`
- Existing report `summary`: preserved.
- Existing all-family `readiness_metrics`: preserved.
- Existing report `status`: preserved.
- Existing CLI output: preserved.
- Existing corpus manifest statuses: unchanged.
- Existing session-ledger statuses: unchanged.

## Current Derived Applicability Metrics

- schema_version: `parser_corpus_behavior_applicability.v1`
- parser_behavior_applicable_family_count: 37
- parser_behavior_applicable_ready_family_count: 19
- parser_behavior_applicable_not_ready_family_count: 18
- parser_behavior_not_applicable_family_count: 8
- parser_behavior_applicable_report_only_family_count: 13
- parser_behavior_applicable_blocked_private_evidence_family_count: 1
- parser_behavior_applicable_blocked_external_boundary_family_count: 4
- parser_behavior_applicability_ready: false
- parser_behavior_applicability_verdict:
  `applicable_families_not_behavior_ready`

## Preserved Legacy Readiness

- classification_complete: true
- parser_behavior_ready: false
- parser_behavior_ready_family_count: 19
- total_scenario_families: 45
- committed_parser_behavior_families: 5
- synthetic_parser_behavior_families: 14
- report_only_families: 19
- blocked_families: 6
- blocked_private_evidence_families: 2
- blocked_external_boundary_families: 4
- missing_families: 0
- partial_families: 0
- deferred_families: 0
- pipeline_activation_ready_for_issue_388: false
- readiness_verdict: `classification_complete_not_behavior_ready`

## Non-Behavior Applicability Exclusions

The eight excluded rows remain visible in the corpus matrix and are not counted
in the applicability-aware parser-behavior denominator:

- `manifest.metadata`
- `session.ledger_metadata`
- `mythic_edge.evidence_ledger_provenance`
- `mythic_edge.confidence_finality_degradation`
- `mythic_edge.workbook_row_coverage`
- `mythic_edge.live_diagnostics`
- `mythic_edge.private_log_report_only_drift`
- `mythic_edge.analytics_readiness_labels`

## Validation

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

## Non-Claims

The new metrics are advisory derived report metadata. They do not:

- change parser behavior;
- change parser-owned truth;
- change corpus manifest or session-ledger statuses;
- promote report-only, private-evidence, or external-boundary rows;
- create fixtures;
- start issue #388 or issue #381;
- run private or live checks;
- certify release, deploy, production, analytics, AI, coaching, or tracker
  readiness.
