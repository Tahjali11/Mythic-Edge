# Parser Evidence Pipeline Activation Criteria Implementation Handoff

## Metadata

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/516
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Related child issue: https://github.com/Tahjali11/Mythic-Edge/issues/381
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Contract: `docs/contracts/parser_evidence_pipeline_activation_criteria.md`
- Risk tier: High
- Base branch: `main`
- Target branch: `main`

## Role Performed

Codex C: Module Implementer.

## Comparison Summary

The contract authorizes only an additive report metric that separates strict
parser-behavior activation from planning-only evidence-pipeline preconditions.

Implemented:

- Added `readiness_metrics.evidence_pipeline_planning` to the corpus parity report.
- Preserved existing `parser_behavior_ready`, `pipeline_activation_ready_for_issue_388`, `behavior_applicability`, summary, matrix, status, and CLI summary behavior.
- Kept `report_preconditions_ready_for_issue_388` true at the current base because the committed report data has no missing, partial, or deferred rows and all residual report-only/private/external rows have matrix rationale.
- Kept full `evidence_pipeline_planning_ready_for_issue_388` false because tracker #158 closeout, #388 wording update, and user approval for #388/#381 are not report-observable.
- Added focused test coverage in `tests/test_corpus_parity_report.py`.
- Added `docs/contract_test_reports/parser_evidence_pipeline_activation_criteria.md`.

Not changed:

- #388 body was not edited.
- #158, #388, #381, and #434 were not closed or activated.
- Corpus manifest and session-ledger contents were not changed.
- Parser behavior, parser events, parser state reconciliation, router semantics, match/game identity, deduplication, golden replay, workbook/webhook/App Script/Sheets/output, analytics, AI, coaching, CI, merge, deploy, production, and final integration policy were not changed.
- No private/live checks were run, and no fixture promotion packet was created.

## Files Changed

- `src/mythic_edge_parser/app/corpus_parity_report.py`
  - Added `EVIDENCE_PIPELINE_PLANNING_SCHEMA_VERSION`.
  - Added derived `evidence_pipeline_planning` readiness metrics.
  - Added helpers for residual-family rationale counts and planning verdict.
- `tests/test_corpus_parity_report.py`
  - Added exact expected object assertions and focused gate checks.
- `docs/contract_test_reports/parser_evidence_pipeline_activation_criteria.md`
  - Added contract-test evidence for the additive metric.
- `docs/implementation_handoffs/parser_evidence_pipeline_activation_criteria_comparison.md`
  - Added this implementation handoff.

The contract file was present as an untracked Codex B artifact when this pass
began and was not modified by this implementation pass.

## Validation Run

Completed:

- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py` passed: 7 tests.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json` passed with unchanged CLI summary:
  - `partial_coverage_map_ready`
  - `45 families`
  - `committed=6`
  - `synthetic=22`
  - `report_only=11`
  - `blocked=6 [private=2, external=4]`
  - `missing=0`
  - `parser_behavior_ready=no`
- `python3 tools/check_agent_docs.py` passed: 34 checked files, 0 errors, 0 warnings.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed.
- Path-scoped secret/private-marker scan passed: 5 scanned paths, 0 forbidden, 0 warnings.
- Path-scoped protected-surface gate passed: 5 changed paths, 0 forbidden, 0 warnings.
- Direct trailing-whitespace scan over tracked and untracked changed files passed.

## Remaining Risks

- The report-local planning precondition is derived from committed matrix rows and their rationale notes. It does not observe live GitHub lifecycle state.
- The full planning gate remains false by design until Codex G applies tracker reconciliation and the user explicitly approves starting #388 or #381.
- Future #388 work still needs a separate scoped issue/contract before creating evidence-pipeline tooling, promoting fixtures, or touching private-evidence workflows.

## Next Recommended Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #516, parser evidence pipeline activation criteria.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/516

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Related child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/381

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract:
docs/contracts/parser_evidence_pipeline_activation_criteria.md

Implementation handoff:
docs/implementation_handoffs/parser_evidence_pipeline_activation_criteria_comparison.md

Contract-test report:
docs/contract_test_reports/parser_evidence_pipeline_activation_criteria.md

Review goal:
Review whether the implementation adds only the authorized additive corpus parity report metric and preserves the strict/non-strict #388 activation distinction.

Review focus:
- Confirm existing parser_behavior_ready remains false at the current base.
- Confirm existing pipeline_activation_ready_for_issue_388 remains false and still means the strict all-family parser-behavior gate.
- Confirm readiness_metrics.evidence_pipeline_planning is additive and schema-versioned.
- Confirm report_preconditions_ready_for_issue_388 is true only as a report-local data signal.
- Confirm evidence_pipeline_planning_ready_for_issue_388 remains false because #158 closeout, #388 wording update, and user approval are not report-observable.
- Confirm CLI summary/status behavior did not change.
- Confirm corpus manifest/session-ledger contents did not change.
- Confirm #388 body, #381 activation, tracker lifecycle, parser behavior, protected downstream surfaces, fixtures, private checks, analytics truth, AI truth, coaching truth, release readiness, and production behavior were not changed or claimed.

Suggested validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- python3 -m ruff check src tests tools
- git diff --check
- path-scoped secret/private-marker scan
- path-scoped protected-surface scan

Do not:
- Edit #388 body.
- Close #158, #388, #381, or #434.
- Activate #381.
- Change corpus manifest or session-ledger contents.
- Promote report-only, private-evidence, blocked, or external-boundary rows.
- Create fixtures or fixture-promotion packets.
- Run private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, or private smoke checks.
- Claim parser_behavior_ready, strict pipeline activation readiness, fixture promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity.
- Stage, commit, push, or open a PR unless explicitly asked.

End with:
- findings first, ordered by severity
- validation run
- remaining risks
- recommended next role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/516"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  related_child_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/381"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_evidence_pipeline_activation_criteria.md"
  target_artifact: "docs/implementation_handoffs/parser_evidence_pipeline_activation_criteria_comparison.md"
  contract_test_report: "docs/contract_test_reports/parser_evidence_pipeline_activation_criteria.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  recommended_implementation: "additive_report_metric_only"
  strict_gate: "pipeline_activation_ready_for_issue_388"
  strict_gate_current_status: false
  report_preconditions_ready_for_issue_388: true
  evidence_pipeline_planning_ready_for_issue_388: false
  parser_behavior_ready: false
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface gate"
    - "direct trailing-whitespace scan over tracked and untracked changed files"
  stop_conditions:
    - "Do not edit #388 body in Codex C."
    - "Do not close #158, #388, or #434."
    - "Do not activate #381."
    - "Do not read private logs or run private checks."
    - "Do not promote blocked, report-only, private-evidence, or external-boundary rows."
    - "Do not claim parser_behavior_ready, strict pipeline activation readiness, fixture promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
