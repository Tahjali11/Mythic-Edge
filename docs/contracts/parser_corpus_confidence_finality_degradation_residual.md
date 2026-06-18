# Parser Corpus Confidence/Finality/Degradation Residual Contract

## Metadata

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/430>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/158>
- Previous issue: <https://github.com/Tahjali11/Mythic-Edge/issues/428>
- Previous PR: <https://github.com/Tahjali11/Mythic-Edge/pull/429>
- Previous merge commit: `8617cb36908c2b9263bfcb610ed2b450ad295af9`
- Base branch: `codex/parser-parity`
- Target artifact: `docs/contracts/parser_corpus_confidence_finality_degradation_residual.md`
- Expected implementation handoff:
  `docs/implementation_handoffs/parser_corpus_confidence_finality_degradation_residual_comparison.md`
- Expected contract-test report:
  `docs/contract_test_reports/parser_corpus_confidence_finality_degradation_residual.md`
- Risk tier: High

## Role And Scope

This contract is for Codex B: Module Contract Writer.

This is corpus parity residual metadata work. It defines whether the
`mythic_edge.confidence_finality_degradation` corpus family may move beyond
count-ratchet partial coverage, and what evidence is required if it does.

This contract does not authorize parser behavior changes, evidence-ledger
behavior changes, runtime field-evidence behavior changes, workbook changes,
analytics behavior changes, AI behavior, release readiness decisions, tracker
completion, or private evidence collection.

## Observed Current Behavior

On `origin/codex/parser-parity`, PR #429 is present at
`8617cb36908c2b9263bfcb610ed2b450ad295af9`.

The current corpus parity report is generated from committed Mythic Edge-owned
metadata:

```text
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

The current report summary is:

- `status`: `partial_coverage_map_ready`
- `total_scenario_families`: 45
- `covered_committed`: 6
- `covered_synthetic`: 14
- `covered_report_only`: 16
- `partial`: 2
- `missing`: 0
- `blocked_private_evidence`: 2
- `blocked_external_boundary`: 5

The current target row is:

| scenario_family | coverage_status | coverage_basis | entry |
| --- | --- | --- | --- |
| `mythic_edge.confidence_finality_degradation` | `partial` | `count_ratchet_only` | `feature_equity_corpus_baseline_v1` |

The current count-ratchet basis proves that committed baseline metadata exists.
It does not prove representative coverage of value-source, confidence,
finality, degradation, drift, invariant status, review-required semantics, or
runtime field-evidence behavior across parser-owned fields and downstream
review surfaces.

The already committed evidence-ledger provenance row
`evidence_ledger_provenance_report_reference_v1` provides report-only evidence
for deterministic evidence-ledger scaffolding, including schema snapshots,
schema drift reports, invariant execution, runtime field-evidence mapping,
validation report wiring, and runtime health summary boundaries. That row
explicitly does not claim confidence/finality/degradation coverage, workbook
row coverage, parser correctness for every entry, or universal runtime
field-evidence attachment.

## Scope Decision

`mythic_edge.confidence_finality_degradation` is approved to move from
`partial` to `covered_report_only` if Codex C adds a dedicated committed
metadata-only corpus entry and session-ledger entry that prove the vocabulary
and review-boundary are documented, stable, and locally validated.

The approved status is not `covered_committed` or `covered_synthetic`.

The approved basis is:

- `evidence_ledger_only`
- `fixture_metadata_only`

`count_ratchet_only` is not sufficient for the target row after this contract.
Codex C may leave historical count-ratchet evidence on other rows, but the
target row should have a dedicated report-only boundary entry rather than
inheriting partial coverage from `feature_equity_corpus_baseline_v1`.

If Codex C discovers that the committed manifest/session-ledger schema cannot
represent the boundary without source-code changes or broader semantics, Codex C
must stop and route back to Codex B or Codex A instead of widening the scope.

## Owning Layer And Truth Boundary

The owning layer is the parser corpus parity metadata/report layer.

The evidence-ledger contracts and runtime field-evidence contracts own their
own vocabulary definitions and review surfaces. This corpus slice may reference
those committed docs and tests as report-only evidence, but it does not become
the authority for evidence-ledger behavior.

This slice may say:

- Mythic Edge has committed metadata describing the value-source, confidence,
  finality, degradation, drift, invariant-status, and review-required boundary.
- The corpus parity report has a dedicated report-only row for that boundary.
- The row is based on committed metadata and deterministic local validation.

This slice must not say:

- parser behavior is correct for every confidence/finality/degradation field;
- every parser-owned field has runtime field-evidence attached;
- every downstream report consumes field evidence;
- workbook rows are covered;
- private Player.log evidence has been reviewed;
- Mythic Edge has full corpus parity;
- release, deploy, production, analytics, AI, or coaching readiness is proven.

## Public Interfaces

Codex C is authorized to update only corpus metadata, focused tests, and
handoff/report docs needed to satisfy this contract.

### Manifest Entry

Codex C should add a dedicated manifest entry with this identity unless a
focused implementation comparison shows an existing equivalent entry is safer:

```text
confidence_finality_degradation_boundary_report_v1
```

Required manifest properties:

- `scenario_families`: exactly `["mythic_edge.confidence_finality_degradation"]`
- `status`: `covered_report_only`
- `coverage_basis`: exactly `["evidence_ledger_only", "fixture_metadata_only"]`
- `entry_type`: `session_ledger_entry`
- `source_kind`: a report-only or metadata-only committed source kind already
  accepted by the manifest vocabulary
- `commit_status`: `committed`
- `privacy_class`: committed metadata only; no private or raw evidence
- `sanitization_status`: not applicable to raw logs because no raw logs are used
- `parser_event_families`: empty

Recommended `parser_claim_families`:

- `value_source_vocabulary`
- `confidence_vocabulary`
- `finality_vocabulary`
- `degradation_vocabulary`
- `drift_flag_vocabulary`
- `invariant_status_vocabulary`
- `review_required_policy`
- `field_evidence_review_boundary`
- `downstream_truth_non_claim`

Recommended path references:

- `docs/contracts/player_log_evidence_ledger_schema.md`
- `docs/contracts/player_log_evidence_ledger.md`
- `docs/contracts/player_log_evidence_ledger_runtime_field_evidence.md`
- `docs/contracts/player_log_evidence_ledger_invariant_execution.md`
- `docs/contracts/player_log_evidence_ledger_validation_report_wiring.md`
- `tests/test_evidence_ledger.py`
- `tests/test_runtime_field_evidence.py`
- `tests/test_evidence_invariant_execution.py`
- `tests/test_corpus_parity_report.py`

### Session Ledger Entry

Codex C should add a matching session-ledger entry with the same ID:

```text
confidence_finality_degradation_boundary_report_v1
```

The session entry should summarize committed metadata and test-backed boundary
coverage without embedding raw evidence reports. It may include count-like or
availability-like fields under `parser_coverage`, such as:

- `value_source_vocabulary`: `available`
- `confidence_vocabulary`: `available`
- `finality_vocabulary`: `available`
- `degradation_vocabulary`: `available`
- `drift_flag_vocabulary`: `available`
- `invariant_status_vocabulary`: `available`
- `review_required_policy`: `available`
- `representative_field_runtime_attachment_claims`: 0
- `parser_behavior_claims`: 0
- `workbook_row_claims`: 0
- `unknown_entries`: 0
- `truncation_count`: 0

The session ledger must not include raw Player.log lines, raw runtime field
evidence, full schema snapshots, full drift diffs, full invariant reports,
private reports, workbook exports, local runtime artifacts, generated data, or
external corpus contents.

### Existing Feature-Equity Baseline Entry

Codex C should stop using `feature_equity_corpus_baseline_v1` as the source of
coverage for `mythic_edge.confidence_finality_degradation`.

The existing baseline may continue covering other rows such as
`mythic_edge.workbook_row_coverage` and any already-authorized count-ratchet
family, but the target row should resolve through the new dedicated entry.

## Required Guarantees

After implementation:

- `mythic_edge.confidence_finality_degradation` is `covered_report_only`.
- Its coverage basis is report-only metadata/evidence-ledger boundary evidence,
  not count-ratchet-only evidence.
- `parser_event_families` for the target row remains empty.
- No `parser_behavior_verified` basis is added for the target row.
- No private evidence is required or claimed.
- No raw logs, private smoke output, generated artifacts, runtime artifacts,
  workbook exports, secrets, credentials, tokens, API keys, or webhook URLs are
  added.
- The corpus parity report remains `partial_coverage_map_ready`.
- `mythic_edge.workbook_row_coverage` remains deferred/unchanged by this issue.
- Private-evidence rows and external-boundary rows remain unchanged by this
  issue.

Expected report summary after the narrow implementation:

- `total_scenario_families`: 45
- `covered_committed`: 6
- `covered_synthetic`: 14
- `covered_report_only`: 17
- `partial`: 1
- `missing`: 0
- `blocked_private_evidence`: 2
- `blocked_external_boundary`: 5

If the exact counts differ because of already-merged upstream changes, Codex C
must explain the drift and prove the target row behavior directly.

## Unknowns And Suspected Gaps

Unknowns:

- Whether every current parser-owned output field eventually needs a dedicated
  field-evidence attachment test.
- Whether downstream diagnostics, golden replay, feature-equity, runtime
  status, workbook, or analytics surfaces will later need representative
  confidence/finality/degradation fixtures.
- Whether workbook row coverage should be promoted by a separate residual issue.

Suspected gaps:

- The current corpus map has vocabulary-level evidence, not representative
  end-to-end field attachment across all parser facts.
- Some downstream consumers may display facts without field-evidence sidecars.
- Count-ratchet evidence is too broad to explain confidence/finality/
  degradation semantics by itself.

These gaps must remain explicit non-claims in Codex C output.

## Validation Obligations

Codex C must run focused documentation and corpus validation. Minimum expected
commands:

```text
python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

Codex C should also perform a small direct row inspection confirming:

- `mythic_edge.confidence_finality_degradation`: `covered_report_only`
- `mythic_edge.workbook_row_coverage`: unchanged from the pre-implementation
  contract baseline unless a later contract explicitly authorizes it
- private-evidence rows: unchanged
- external-boundary rows: unchanged
- `missing`: remains 0

Codex E should verify the same row-level behavior and confirm that no protected
surface was touched.

Codex F/G should not treat zero missing rows or this row's promotion as tracker
completion, parser support, release readiness, deploy readiness, production
readiness, analytics truth, AI truth, or coaching truth.

## Protected Surfaces

Codex C must not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- router semantics;
- diagnostics behavior;
- drift behavior;
- golden replay behavior;
- feature-equity behavior;
- evidence-ledger behavior;
- runtime field-evidence behavior;
- match/game identity;
- deduplication;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- output transport;
- analytics truth;
- AI truth;
- coaching behavior;
- CI gates;
- merge readiness;
- deploy readiness;
- production behavior;
- final integration policy.

Codex C must not import, copy, mirror, or commit Manasight raw logs, compressed
corpus files, parser source, external corpus contents, private Player.log
excerpts, private local logs, private smoke outputs, generated/private/runtime
artifacts, workbook exports, credentials, tokens, API keys, webhook URLs,
decklists, card choices, strategy notes, or private reports.

## Acceptance Criteria

This contract is satisfied when:

- `docs/contracts/parser_corpus_confidence_finality_degradation_residual.md`
  exists;
- Codex C has a narrow, metadata-only implementation route;
- the route has explicit non-claims and protected-surface boundaries;
- validation expectations are concrete;
- `mythic_edge.workbook_row_coverage`, private-evidence rows, and
  external-boundary rows are deferred;
- a pasteable Codex C prompt and workflow handoff are present.

## Pasteable Codex C Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #430.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/430

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Previous issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/428

  Previous PR:
  https://github.com/Tahjali11/Mythic-Edge/pull/429

  Previous merge commit:
  8617cb36908c2b9263bfcb610ed2b450ad295af9

  Base branch:
  codex/parser-parity

  Contract:
  docs/contracts/parser_corpus_confidence_finality_degradation_residual.md

  Goal:
  Implement the narrow metadata-only corpus parity residual update for
  mythic_edge.confidence_finality_degradation. Promote only this row from
  count-ratchet partial coverage to a dedicated covered_report_only vocabulary
  and review-boundary entry, if the current repo still matches the contract.

  Expected implementation artifacts:
  - tests/fixtures/parser_corpus/corpus_manifest.v1.json
  - tests/fixtures/parser_corpus/session_ledger.v1.json
  - tests/test_corpus_parity_report.py, only if focused expectations need to be
    updated
  - docs/implementation_handoffs/parser_corpus_confidence_finality_degradation_residual_comparison.md
  - docs/contract_test_reports/parser_corpus_confidence_finality_degradation_residual.md

  Required behavior:
  - Add a dedicated report-only manifest/session-ledger entry for
    mythic_edge.confidence_finality_degradation.
  - Use coverage_status covered_report_only.
  - Use evidence-ledger/fixture-metadata boundary evidence rather than
    count_ratchet_only as the target row basis.
  - Keep parser_event_families empty for the new row.
  - Do not add parser_behavior_verified.
  - Leave mythic_edge.workbook_row_coverage, private-evidence rows, and
    external-boundary rows unchanged.
  - Keep the report status partial_coverage_map_ready.

  Validation:
  - python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
  - python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
  - PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
  - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
  - python3 tools/check_agent_docs.py
  - python3 -m ruff check src tests tools
  - git diff --check

  Do not:
  - Implement parser behavior changes.
  - Change evidence-ledger behavior, runtime field-evidence behavior, workbook
    schema, analytics truth, AI truth, coaching behavior, CI gates, merge
    readiness, deploy readiness, production behavior, or final integration
    policy.
  - Touch mythic_edge.workbook_row_coverage, private-evidence rows, or
    external-boundary rows except to confirm they remain unchanged.
  - Run private app-data, Player.log, firewall/drop, network, live MTGA, or
    private smoke checks.
  - Import or commit Manasight raw logs, compressed corpus files, parser source,
    external corpus contents, private logs, generated/runtime artifacts,
    workbook exports, secrets, tokens, API keys, webhook URLs, decklists, or
    private reports.
  - Claim full corpus parity, parser support, release readiness, production
    readiness, analytics truth, AI truth, or coaching truth.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/430"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/428"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/429"
  previous_merge_commit: "8617cb36908c2b9263bfcb610ed2b450ad295af9"
  completed_thread: "B"
  next_thread: "C"
  verdict: "contract_ready_for_metadata_only_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-parity"
  target_artifact: "docs/implementation_handoffs/parser_corpus_confidence_finality_degradation_residual_comparison.md"
  contract: "docs/contracts/parser_corpus_confidence_finality_degradation_residual.md"
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not mark tracker #158 complete."
    - "Do not claim full corpus parity, parser support, release readiness, production readiness, analytics truth, AI truth, or coaching truth."
    - "Do not change parser behavior, evidence-ledger behavior, runtime field-evidence behavior, workbook schema, analytics truth, AI truth, coaching behavior, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy."
    - "Do not touch mythic_edge.workbook_row_coverage, private-evidence rows, or external-boundary rows except to confirm they remain unchanged."
    - "Do not run or commit private Player.log, app-data, firewall/drop, network, live MTGA, or private smoke evidence."
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/430"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/428"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/429"
  previous_merge_commit: "8617cb36908c2b9263bfcb610ed2b450ad295af9"
  completed_thread: "B"
  next_thread: "C"
  verdict: "contract_ready_for_metadata_only_implementation"
  risk_tier: "High"
  base_branch: "codex/parser-parity"
  contract: "docs/contracts/parser_corpus_confidence_finality_degradation_residual.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_confidence_finality_degradation_residual_comparison.md"
  validation:
    - "Contract writer inspected issue #430, tracker #158, issue #428, PR #429, corpus parity report, manifest/session ledger, evidence-ledger provenance contract/report, and current corpus report state."
    - "Contract writer verified origin/codex/parser-parity contains 8617cb36908c2b9263bfcb610ed2b450ad295af9."
    - "Documentation-only contract pass; no implementation validation expected beyond contract file checks."
  stop_conditions:
    - "Do not target main."
    - "Do not close tracker #158."
    - "Do not mark tracker #158 complete."
    - "Do not claim full corpus parity, parser support, release readiness, production readiness, analytics truth, AI truth, or coaching truth."
    - "Do not change parser behavior, evidence-ledger behavior, runtime field-evidence behavior, workbook schema, analytics truth, AI truth, coaching behavior, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy."
    - "Do not touch mythic_edge.workbook_row_coverage, private-evidence rows, or external-boundary rows except to confirm they remain unchanged."
    - "Do not run or commit private Player.log, app-data, firewall/drop, network, live MTGA, or private smoke evidence."
```
