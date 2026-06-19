# Parser Corpus Readiness Metrics Comparison

## Metadata

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/462
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent/private-evidence gate: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/464
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/466
- Previous merge commit: `de988ffba7e960ec13d85ee13e87157be6f202e0`
- Branch: `codex/parser-corpus-readiness-metrics-462`
- Base branch: `main`
- Source artifact: `docs/contracts/parser_corpus_readiness_metrics.md`
- Risk tier: Medium-High

## Contract Comparison

The contract asks the corpus parity report to separate classification
completeness from parser-behavior readiness. The implementation adds a derived
top-level `readiness_metrics` section and updates the CLI headline so zero
missing rows are no longer the dominant readiness signal.

Existing `summary`, `status`, coverage matrix rows, privacy section,
protected-surface section, corpus manifest state, and session-ledger state are
unchanged.

## Live Count Note

The contract expected `parser_behavior_ready_family_count: 20` at the observed
base, but it also requires parser-behavior readiness to count only families
whose basis includes `parser_behavior_verified`. The live matrix has one
`covered_committed` family without that basis:
`session.ledger_metadata`.

Codex C followed the stricter derivation rule. Current derived
parser-behavior readiness is therefore 19 of 45 families:

- committed parser-behavior families: 5
- synthetic parser-behavior families: 14
- report-only families: 19
- blocked families: 6

This does not change any corpus status or fixture metadata.

## Changes Made

- Updated `src/mythic_edge_parser/app/corpus_parity_report.py`.
- Updated `tests/test_corpus_parity_report.py`.
- Added this handoff.
- Added `docs/contract_test_reports/parser_corpus_readiness_metrics.md`.

`docs/project_roadmap.md` was inspected for a narrow overclaim and left
unchanged.

Codex D follow-up: fixed ME462-E-001 by restoring the contracted generated
report limitation that corpus reports do not decide coaching truth or
production behavior. Focused coverage now asserts both non-claims in
`report["limitations"]`.

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
- Codex D reran `PYTHONPATH=src python3 -m pytest -q tests` after the
  ME462-E-001 fix; passed: 1770 tests.

## Residual Risks

- `readiness_metrics` are derived review metadata, not parser truth or release
  truth.
- Generated report limitations explicitly remain non-claims for production
  behavior, analytics truth, AI truth, and coaching truth.
- `classification_complete` is true because missing, partial, and deferred
  counts are zero; it does not imply parser-behavior readiness.
- `pipeline_activation_ready_for_issue_388` remains false.
- Issue #388 and child issue #381 were not started, mutated, or closed.
- Private/live/UTC_Log/Player.log/firewall/network checks were not run.
- No corpus manifest or session-ledger statuses were changed.

## Next Recommended Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #462, parser corpus readiness
metrics, under tracker #158.

Review:
- docs/contracts/parser_corpus_readiness_metrics.md
- src/mythic_edge_parser/app/corpus_parity_report.py
- tests/test_corpus_parity_report.py
- docs/implementation_handoffs/parser_corpus_readiness_metrics_comparison.md
- docs/contract_test_reports/parser_corpus_readiness_metrics.md

Verify that readiness metrics are derived from the existing report matrix and
summary, existing summary/status semantics remain backward compatible, corpus
manifest and session-ledger statuses did not change, parser behavior did not
change, and zero missing rows no longer imply parser-behavior readiness.

Pay special attention to the live count note: Codex C reports 19/45
parser-behavior-ready families because session.ledger_metadata lacks
parser_behavior_verified, despite the contract's example count of 20/45.

Do not target main directly. Do not start #388 or #381. Do not run private or
live checks. Do not claim full corpus parity, parser support, release
readiness, deploy readiness, production behavior, analytics truth, AI truth,
coaching truth, or tracker completion.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/462"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/464"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/466"
  previous_merge_commit: "de988ffba7e960ec13d85ee13e87157be6f202e0"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_readiness_metrics.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_readiness_metrics_comparison.md"
  report_artifact: "docs/contract_test_reports/parser_corpus_readiness_metrics.md"
  verdict: "readiness_metrics_limitations_fix_ready_for_review"
  risk_tier: "Medium-High"
  branch: "codex/parser-corpus-readiness-metrics-462"
  base_branch: "main"
  implementation_scope: "derived corpus report metrics, CLI wording, focused tests, generated limitations non-claims"
```
