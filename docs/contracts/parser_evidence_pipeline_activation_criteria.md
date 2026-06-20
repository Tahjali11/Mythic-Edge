# Parser Evidence Pipeline Activation Criteria Contract

## Module

Amended activation criteria for issue #388, the parser evidence pipeline
tracker.

Plain English: this contract separates strict parser-behavior readiness from
planning-only evidence-pipeline readiness. The existing
`pipeline_activation_ready_for_issue_388` remains the strict all-family
parser-behavior gate and remains false at the current base. A new additive
planning-preconditions signal may be implemented so Codex G can later amend
#388 without forcing report-only, private-evidence, external-boundary, or
non-behavior rows into fake synthetic parser fixtures.

This contract does not implement code, edit the #388 body, close trackers,
activate #381, run private checks, promote fixtures, or claim parser behavior
readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/516
- Parent tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Pipeline tracker to amend: https://github.com/Tahjali11/Mythic-Edge/issues/388
- First pipeline child issue: https://github.com/Tahjali11/Mythic-Edge/issues/381
- Related private-evidence parent: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Latest completed #158 child: https://github.com/Tahjali11/Mythic-Edge/issues/513
- Latest completed PR: https://github.com/Tahjali11/Mythic-Edge/pull/515
- Latest merge commit: `daed7925479e27c2d61340eed4c83b47b3beda07`
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed during this Codex B pass:

- Issue #516 is open.
- Tracker #158 is open.
- Pipeline tracker #388 is open.
- Child issue #381 is open.
- Parent private-evidence issue #434 is open.
- The operating checkout was on clean `main`.
- `HEAD` and `origin/main` both pointed to
  `daed7925479e27c2d61340eed4c83b47b3beda07`.
- The operating checkout remote matched
  `https://github.com/Tahjali11/Mythic-Edge.git`.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #516, tracker #158, tracker #388, issue #381, and issue #434
- `docs/contracts/repo_scoped_workflow_handoffs.md`
- `docs/contracts/parser_corpus_readiness_metrics.md`
- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- `docs/contracts/parser_corpus_private_log_drift_status_reconciliation.md`
- `docs/contracts/parser_corpus_firewall_network_drop_status_reconciliation.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

## Observed Current Behavior

Current corpus parity CLI output:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=22, report_only=11, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Current report summary:

```yaml
total_scenario_families: 45
covered_committed: 6
covered_synthetic: 22
covered_report_only: 11
partial: 0
missing: 0
deferred: 0
blocked_private_evidence: 2
blocked_external_boundary: 4
not_applicable: 0
```

Current readiness metrics:

```yaml
classification_complete: true
parser_behavior_ready: false
parser_behavior_ready_family_count: 27
total_scenario_families: 45
committed_parser_behavior_families: 5
synthetic_parser_behavior_families: 22
report_only_families: 11
blocked_families: 6
blocked_private_evidence_families: 2
blocked_external_boundary_families: 4
missing_families: 0
partial_families: 0
deferred_families: 0
pipeline_activation_ready_for_issue_388: false
pipeline_activation_blockers:
  - "report_only_families:11"
  - "blocked_private_evidence_families:2"
  - "blocked_external_boundary_families:4"
readiness_verdict: "classification_complete_not_behavior_ready"
behavior_applicability:
  parser_behavior_applicable_family_count: 37
  parser_behavior_applicable_ready_family_count: 27
  parser_behavior_applicable_not_ready_family_count: 10
  parser_behavior_not_applicable_family_count: 8
  parser_behavior_applicability_ready: false
```

Current #388 body still says:

```text
Do not start this tracker until #158 can show, through the repo-owned corpus parity report and review artifacts, that all 45 parser corpus families have at least covered_synthetic coverage or stronger.
```

That wording is intentionally not edited by this contract pass.

## Problem

The old #388 start condition conflates three decisions:

1. whether #158 has fully classified the corpus map;
2. whether every parser-behavior-applicable family has parser-behavior
   evidence; and
3. whether it is safe to begin local evidence-pipeline tooling/planning that
   may later generate reviewed evidence packets and fixture candidates.

The current report proves classification completeness but does not prove
strict parser-behavior readiness. Forcing all 45 rows to
`covered_synthetic` or stronger would pressure non-behavior rows,
private-evidence rows, external-boundary rows, and report-only governance
rows into the wrong evidence shape.

## Scope Decision

Implementation should proceed as an additive report metric and test update.

Codex C may add an additive planning-preconditions object under
`readiness_metrics`. The object should distinguish repo-data preconditions
from workflow lifecycle approval, because the report can inspect corpus
metadata but cannot know whether GitHub tracker #158 has received Codex G
closeout or whether the user has approved starting #388 / #381.

Codex C must preserve:

- existing `parser_behavior_ready`;
- existing `pipeline_activation_ready_for_issue_388`;
- existing `behavior_applicability`;
- existing coverage statuses;
- existing manifest/session-ledger contents;
- existing parser behavior and parser event shapes.

Codex C must not edit #388, activate #381, close trackers, create fixtures,
run private checks, promote blocked/report-only rows, or claim readiness.

## Owning Layer

Owning layer: Quality / Governance, with Corpus / Provenance support.

This contract owns workflow gate semantics for starting #388 as planning-only
evidence-pipeline work. Corpus / Provenance owns the report-derived inputs
used to calculate classification and evidence-strength preconditions.

This contract does not own parser behavior, parser state final reconciliation,
parser event classes, router semantics, match/game identity, deduplication,
golden replay fixture truth, private evidence promotion, release readiness,
production behavior, analytics truth, AI truth, coaching truth, CI gates,
merge readiness, deploy readiness, or final integration policy.

## Truth Owner

Truth owner for corpus rows and current readiness report:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for #388 workflow activation semantics:

- this contract;
- a future reviewed implementation handoff and contract-test report;
- Codex G tracker update after merge, if explicitly requested and approved.

GitHub issue bodies remain the live tracker text. This Codex B pass does not
edit #388 and does not make #388 active by itself.

## Bridge-Code Status

`not_bridge_code`

The authorized Codex C change is a derived report metric. It must not move
parser truth downstream or route downstream governance back into parser
behavior.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`

Future Codex C files authorized by this contract:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `docs/implementation_handoffs/parser_evidence_pipeline_activation_criteria_comparison.md`
- `docs/contract_test_reports/parser_evidence_pipeline_activation_criteria.md`

Files Codex C may read but must not modify in this slice:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- recent parser-corpus contracts, handoffs, and reports
- GitHub issues #158, #388, #381, #434, #510, #513, and #516

Not owned by this contract:

- parser modules;
- parser event classes;
- parser state final reconciliation;
- router semantics;
- diagnostics, golden replay, feature-equity, drift, evidence-ledger,
  workbook, webhook, Apps Script, Google Sheets, analytics, AI, coaching,
  CI, merge, deploy, production, or tracker lifecycle behavior;
- GitHub issue body edits;
- scheduled or manual private evidence execution;
- raw/private/generated/runtime artifacts.

## Public Interface

Future Codex C should add an additive nested object under
`readiness_metrics`, preserving all existing keys.

Recommended object:

```yaml
readiness_metrics:
  evidence_pipeline_planning:
    schema_version: "parser_evidence_pipeline_planning.v1"
    report_preconditions_ready_for_issue_388: true
    evidence_pipeline_planning_ready_for_issue_388: false
    readiness_verdict: "report_preconditions_ready_lifecycle_approval_pending"
    classification_complete: true
    missing_families: 0
    partial_families: 0
    deferred_families: 0
    strict_parser_behavior_gate_ready: false
    strict_gate: "pipeline_activation_ready_for_issue_388"
    report_only_families_with_rationale: 11
    blocked_private_evidence_families_with_rationale: 2
    blocked_external_boundary_families_with_rationale: 4
    lifecycle_approval_required: true
    tracker_158_closeout_required: true
    tracker_388_body_update_required: true
    user_approval_required_to_start_issue_381: true
    allowed_scope: "evidence_pipeline_tooling_planning_only"
    non_claims:
      - "parser_behavior_ready"
      - "fixture_promotion_ready"
      - "private_smoke_success"
      - "release_readiness"
      - "production_readiness"
      - "analytics_truth"
      - "ai_truth"
      - "coaching_truth"
      - "full_parser_regression_parity"
```

`report_preconditions_ready_for_issue_388` is a repo-data signal. It may be
true when the corpus report has no missing, partial, or deferred rows and all
remaining report-only, private-evidence, and external-boundary rows have
committed rationale/status metadata.

`evidence_pipeline_planning_ready_for_issue_388` is the full workflow gate. It
must remain false in the generated report until a later implementation has a
repo-owned way to verify the non-report lifecycle requirements, or until Codex
G applies those requirements in tracker commentary after merge. The report
must not pretend to know live GitHub lifecycle approval by itself.

The existing `pipeline_activation_ready_for_issue_388` remains the strict
parser-behavior gate and must remain false at the current base.

## Gate Semantics

### Strict Parser-Behavior Gate

Field:

```yaml
pipeline_activation_ready_for_issue_388: false
```

Meaning:

- all 45 corpus families have parser-behavior-ready evidence;
- no report-only, private-evidence, external-boundary, partial, missing, or
  deferred blockers remain;
- this is the legacy strict all-family gate.

Current value: false.

This field must not be repurposed for planning-only #388 activation.

### Report-Local Planning Preconditions

Recommended field:

```yaml
readiness_metrics.evidence_pipeline_planning.report_preconditions_ready_for_issue_388
```

Meaning:

- classification is complete;
- missing, partial, and deferred counts are zero;
- report-only rows remain visible;
- blocked private/external rows remain visible;
- each residual row has an explicit status rationale or delegated follow-up
  home in committed contracts/review notes;
- evidence-pipeline work, if later started, is limited to tooling/planning.

Current expected value: true.

This field is not enough to start #388 / #381.

### Full Planning Workflow Gate

Recommended field:

```yaml
readiness_metrics.evidence_pipeline_planning.evidence_pipeline_planning_ready_for_issue_388
```

Meaning:

#388 may begin only as evidence-pipeline tooling/planning when all of these
are true:

1. report-local planning preconditions are true;
2. #158 has a Codex G classification lifecycle closeout or explicit
   reconciliation comment after the amended criteria are merged;
3. #388 body/start condition has been amended by Codex G after merge;
4. the user explicitly approves starting #388 or selecting a child issue such
   as #381;
5. the selected work is limited to evidence-pipeline tooling/planning;
6. the selected work does not run private checks, promote fixtures, upgrade
   blocked/report-only rows, or claim parser behavior readiness by default.

Current generated-report value: false, because the report cannot observe
GitHub lifecycle approval and this contract pass does not edit #388 or
activate #381.

## Proposed #388 Tracker Wording

Codex G may apply wording equivalent to the following only after this contract
and any authorized implementation/review package are merged:

```text
This tracker may begin only as evidence-pipeline tooling/planning after tracker #158 has completed classification lifecycle reconciliation and the repo-owned corpus parity report shows no missing, partial, or deferred rows. All report-only, private-evidence, and external-boundary rows must have explicit status rationale or delegated follow-up homes.

Starting this tracker does not mean parser_behavior_ready, strict pipeline_activation_ready_for_issue_388, fixture-promotion readiness, private smoke success, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full corpus parity.

Child issues under this tracker must not run private checks, read private logs, promote fixtures, or upgrade blocked/report-only rows unless a later explicit issue, contract, privacy review, and user approval authorize that exact work.
```

This contract does not edit #388 directly.

## Inputs

Allowed inputs:

- committed repo docs, contracts, reports, fixture metadata, source code, and
  tests;
- GitHub issue/PR metadata for #158, #388, #381, #434, #510, #513, #515, and
  #516;
- current corpus parity report output;
- committed corpus manifest and session-ledger metadata.

Forbidden inputs:

- raw private `Player.log` or `UTC_Log` content;
- private app-data contents;
- private smoke outputs;
- private drift reports;
- local-only offset windows or evidence packets;
- exact private paths, exact offsets, exact file sizes, raw hashes, raw log
  lines, screenshots, SQLite files, workbook exports, runtime artifacts,
  failed posts, credentials, tokens, API keys, webhook URLs, decklists, card
  choices, private strategy notes, IP/network traces, packet captures,
  OS/router diagnostics, firewall logs, Wi-Fi logs, or external corpus
  contents.

## Outputs

Allowed output for this Codex B pass:

- this contract file;
- workflow handoff to Codex C;
- pasteable next-thread prompt.

Future Codex C output authorized by this contract:

- additive report metric and focused tests;
- implementation handoff;
- contract-test report.

Forbidden output:

- #388 body edits before merge/deployer approval;
- #381 activation;
- tracker closure;
- changed parser behavior;
- changed coverage status vocabulary;
- changed corpus manifest or session-ledger contents;
- fixtures or fixture-promotion packets;
- private evidence artifacts;
- generated data;
- runtime artifacts;
- readiness claims.

## Required Guarantees

- `pipeline_activation_ready_for_issue_388` remains the strict all-family
  parser-behavior gate.
- `parser_behavior_ready` remains false at the current base.
- `pipeline_activation_ready_for_issue_388` remains false at the current base.
- The new planning object must not remove or reinterpret existing metrics.
- Planning preconditions must not hide report-only, private-evidence, or
  external-boundary blockers.
- Planning preconditions must not promote any row.
- #388 and #381 remain inactive unless Codex G and the user explicitly approve
  a later start under the amended gate.
- Private-evidence rows remain gated by #434 and local-only privacy contracts.
- Evidence-pipeline tooling must not bulk-bless parser output as golden truth.

## Unknowns

- Whether Codex G will amend #388 immediately after this package merges or
  wait for a separate #158 lifecycle closeout.
- Whether #388 should start with #381 or with a narrower umbrella contract
  after the amended wording is applied.
- Whether future tooling should expose workflow lifecycle state in a committed
  status artifact. This contract does not authorize that.

## Suspected Gaps

- The current strict metric is safe but too broad for deciding whether
  evidence-pipeline tooling/planning can start.
- The corpus report currently has no explicit planning-preconditions object,
  so humans must infer the difference from several adjacent metrics.
- #388 body text is stale relative to the post-#462/#477/#510/#513 workflow
  model.

## Error Behavior

If implementation would need corpus manifest/session-ledger changes, route
back to Codex B.

If implementation would need private/live data, stop.

If implementation would edit #388 body or activate #381, stop and route to
Codex G after merge.

If implementation would mark strict `pipeline_activation_ready_for_issue_388`
true at the current base, stop and route back to Codex B.

If any artifact claims parser behavior readiness, fixture-promotion readiness,
private smoke success, release readiness, production readiness, analytics
truth, AI truth, coaching truth, or full parser regression parity, stop and
route back to Codex B or Codex E.

## Side Effects

Contract pass side effect:

- adds `docs/contracts/parser_evidence_pipeline_activation_criteria.md`

Future Codex C side effects authorized only if implementation is selected:

- updates derived report metrics and focused tests;
- creates implementation handoff and contract-test report.

No runtime side effects are authorized.

## Compatibility

Backward compatibility requirements:

- existing `summary` keys stay unchanged;
- existing `readiness_metrics` keys stay unchanged;
- existing `readiness_metrics.behavior_applicability` keys stay unchanged;
- existing `status` values stay unchanged;
- existing coverage matrix rows stay unchanged;
- existing coverage status vocabulary stays unchanged;
- existing CLI exit-code behavior stays unchanged.

Adding `readiness_metrics.evidence_pipeline_planning` is an additive report
schema extension. If Codex C decides the readiness metrics schema version must
change, it must state that in the implementation handoff and keep existing
consumers backward compatible.

## Tests Required

For this contract-only pass:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' docs/contracts/parser_evidence_pipeline_activation_criteria.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_pipeline_activation_criteria.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Future Codex C must run:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' docs/contracts/parser_evidence_pipeline_activation_criteria.md src/mythic_edge_parser/app/corpus_parity_report.py tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_evidence_pipeline_activation_criteria_comparison.md docs/contract_test_reports/parser_evidence_pipeline_activation_criteria.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_pipeline_activation_criteria.md src/mythic_edge_parser/app/corpus_parity_report.py tests/test_corpus_parity_report.py docs/implementation_handoffs/parser_evidence_pipeline_activation_criteria_comparison.md docs/contract_test_reports/parser_evidence_pipeline_activation_criteria.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Future Codex C focused assertions:

- existing `parser_behavior_ready` remains false;
- existing `pipeline_activation_ready_for_issue_388` remains false;
- new report-local planning preconditions are true at the current base;
- new full planning workflow gate remains false at the current base;
- #388 / #381 are not activated by report generation;
- existing behavior-applicability metrics remain unchanged.

## Acceptance Criteria

- `docs/contracts/parser_evidence_pipeline_activation_criteria.md` exists.
- The contract distinguishes strict parser-behavior readiness from
  planning-only evidence-pipeline readiness.
- The contract preserves `parser_behavior_ready=false` at the current base.
- The contract preserves strict
  `pipeline_activation_ready_for_issue_388=false` at the current base.
- The contract recommends only additive report metrics.
- The contract defines proposed #388 wording for Codex G after merge.
- The contract does not edit #388 or activate #381.
- The contract preserves private-evidence, report-only, external-boundary,
  parser truth, fixture-promotion, analytics, AI, coaching, release,
  production, and tracker lifecycle non-claims.

## Next Workflow Action

Recommended next role: Codex C: Module Implementer.

Codex C should implement only the additive report metric and focused tests.
Codex G, not Codex C, owns any later #388 body update after merge and explicit
approval.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #516.

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

Related private-evidence parent:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Base branch:
main

Target branch:
main

Contract:
docs/contracts/parser_evidence_pipeline_activation_criteria.md

Goal:
Implement the smallest additive corpus parity report/test change needed to expose evidence-pipeline planning preconditions separately from strict parser-behavior readiness.

Do:
- Compare current report implementation against the contract before editing.
- Preserve existing `parser_behavior_ready`, `pipeline_activation_ready_for_issue_388`, `behavior_applicability`, summary, matrix, status, and CLI behavior.
- Add `readiness_metrics.evidence_pipeline_planning` or an equivalent clearly named additive object.
- Keep `report_preconditions_ready_for_issue_388` true at the current base if the committed report data satisfies the contract.
- Keep full `evidence_pipeline_planning_ready_for_issue_388` false at the current base because tracker #158 closeout, #388 wording update, and user approval are not report-observable.
- Add focused tests in `tests/test_corpus_parity_report.py`.
- Write `docs/implementation_handoffs/parser_evidence_pipeline_activation_criteria_comparison.md`.
- Write `docs/contract_test_reports/parser_evidence_pipeline_activation_criteria.md`.

Do not:
- Edit #388 body.
- Close #158, #388, or #434.
- Activate #381.
- Change corpus manifest or session-ledger contents.
- Change parser behavior, parser event classes, parser state final reconciliation, router semantics, match/game identity, deduplication, golden replay behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, CI gates, merge readiness, deploy readiness, production behavior, or final integration policy.
- Promote report-only, private-evidence, blocked, or external-boundary rows.
- Create fixtures or fixture-promotion packets.
- Run private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, or private smoke checks.
- Claim parser_behavior_ready, strict pipeline activation readiness, fixture promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity.

Validation:
- `PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py`
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
- `python3 tools/check_agent_docs.py`
- `python3 -m ruff check src tests tools`
- `git diff --check`
- path-scoped secret/private-marker scan
- path-scoped protected-surface scan
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
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/513"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/515"
  previous_merge_commit: "daed7925479e27c2d61340eed4c83b47b3beda07"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_evidence_pipeline_activation_criteria.md"
  target_artifact: "docs/implementation_handoffs/parser_evidence_pipeline_activation_criteria_comparison.md"
  expected_review_artifact: "docs/contract_test_reports/parser_evidence_pipeline_activation_criteria.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  selected_gate: "evidence_pipeline_planning"
  strict_gate: "pipeline_activation_ready_for_issue_388"
  strict_gate_current_status: false
  parser_behavior_ready: false
  recommended_implementation: "additive_report_metric_only"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface scan"
  stop_conditions:
    - "Do not edit #388 body in Codex C."
    - "Do not close #158, #388, or #434."
    - "Do not activate #381."
    - "Do not read private logs or run private checks."
    - "Do not promote blocked, report-only, private-evidence, or external-boundary rows."
    - "Do not claim parser_behavior_ready, strict pipeline activation readiness, fixture promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
