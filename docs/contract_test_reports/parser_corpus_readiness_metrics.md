# Parser Corpus Readiness Metrics Report

## Verdict

`readiness_metrics` are implemented and ready for Codex E review.

This report does not claim full corpus parity, parser support, private smoke
success, release readiness, deploy readiness, production behavior, analytics
truth, AI truth, coaching truth, tracker completion, or activation of issue
#388 or issue #381.

## Evidence Summary

- Source contract: `docs/contracts/parser_corpus_readiness_metrics.md`
- Report section added: `readiness_metrics`
- Existing report `summary`: preserved
- Existing report `status`: preserved
- Existing corpus manifest statuses: unchanged
- Existing session-ledger statuses: unchanged
- CLI output now includes committed, synthetic, report-only, blocked, private
  blocked, external blocked, missing, and parser-behavior-ready fields.

## Codex D Fixer Addendum

ME462-E-001 is fixed. The generated report `limitations` now explicitly state
that corpus reports do not decide coaching truth or production behavior, and
focused tests assert both non-claims remain present.

## Current Derived Metrics

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

## Competitive Core

- schema_version: `parser_corpus_competitive_core.v1`
- status: `classification_complete_not_behavior_ready`
- total_families: 16
- parser_behavior_ready_family_count: 8
- report_only_family_count: 5
- blocked_family_count: 3

## Count Mismatch Note

The contract example listed 20 parser-behavior-ready families, but the live
matrix has 19 when applying the contract's own strict rule that a family must
include `parser_behavior_verified` in its coverage basis. The difference is
`session.ledger_metadata`, which is `covered_committed` metadata but not
parser-behavior evidence.

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
- Codex D reran `PYTHONPATH=src python3 -m pytest -q tests` after the
  ME462-E-001 fix; passed: 1770 tests.

## Non-Claims

The new metrics are advisory report metadata. They do not:

- change parser behavior
- change parser-owned truth
- change corpus manifest or session-ledger statuses
- promote fixtures
- start issue #388 or issue #381
- run private or live checks
- certify release, deploy, production, analytics, AI, coaching, or tracker
  readiness
- decide coaching truth or production behavior through generated report
  limitations
