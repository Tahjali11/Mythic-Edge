# Parser Evidence Pipeline Planning Umbrella Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/518

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

Related child issue: https://github.com/Tahjali11/Mythic-Edge/issues/381

Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434

Recently closed tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_evidence_pipeline_planning_umbrella.md`

## Implementation Under Test

Contract-only package:

- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`

No code, fixture, corpus manifest, session ledger, private artifact, GitHub issue
body, tracker, runtime, workbook, webhook, Apps Script, analytics, AI, coaching,
CI, merge, deploy, or production behavior is under test.

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The contract defines a planning-only umbrella for #388. It allows future
evidence-pipeline planning to start only as scoped governance/contract work while
preserving these current activation facts:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
report_preconditions_ready_for_issue_388: true
evidence_pipeline_planning_ready_for_issue_388: false
```

It does not authorize #381 implementation, private-log reads, private/live
checks, fixture promotion, parser behavior changes, issue-body edits, readiness
claims, or downstream protected-surface changes.

## Internal Project Area Reviewed

Primary: Quality / Governance.

Supporting: Corpus / Provenance.

The contract keeps parser-owned truth, corpus/provenance planning, private
evidence execution, and downstream analytics/AI/coaching boundaries separate.

## Bridge-Code Status Reviewed

`deferred_future_boundary`

No bridge code is authorized by this contract. Future child issues must define
their own source classes, artifact shapes, tests, redaction rules, and stop
conditions before implementation.

## Checks Run

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' docs/contracts/parser_evidence_pipeline_planning_umbrella.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_pipeline_planning_umbrella.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_pipeline_planning_umbrella.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

Additional review checks:

```bash
gh issue view 518 --repo Tahjali11/Mythic-Edge --json number,state,title
gh issue view 388 --repo Tahjali11/Mythic-Edge --json number,state,title,body
gh issue view 381 --repo Tahjali11/Mythic-Edge --json number,state,title,body
gh issue view 382 --repo Tahjali11/Mythic-Edge --json number,state,title,body
gh issue view 383 --repo Tahjali11/Mythic-Edge --json number,state,title,body
gh issue view 384 --repo Tahjali11/Mythic-Edge --json number,state,title,body
gh issue view 385 --repo Tahjali11/Mythic-Edge --json number,state,title,body
gh issue view 386 --repo Tahjali11/Mythic-Edge --json number,state,title,body
gh issue view 387 --repo Tahjali11/Mythic-Edge --json number,state,title,body
gh issue view 434 --repo Tahjali11/Mythic-Edge --json number,state,title
gh issue view 158 --repo Tahjali11/Mythic-Edge --json number,state,title
```

## Results

All required checks passed.

- Corpus parity report output remains:
  `Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=22, report_only=11, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)`
- `python3 tools/check_agent_docs.py`: passed, 34 checked files, 0 errors, 0 warnings.
- `git diff --check`: passed.
- Path-scoped secret/private-marker scan: passed, 1 scanned path, 0 forbidden, 0 warnings.
- Path-scoped protected-surface gate: passed, 1 changed path, 0 forbidden, 0 warnings.
- Path-scoped validation selector: passed with `selection_status: ok`.
- Live GitHub issue states observed during review:
  - #518 open.
  - #388 open.
  - #381 through #387 open.
  - #434 open.
  - #158 closed.
- `HEAD` and `origin/main` both resolve to
  `e760ebdeb65eef9b2dbbc53a42a0bd1e759a7b71`.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| none | none | `final_approval` | no findings | not_blocking | Contract-only package reviewed. | Validation passed and review found no contract mismatches. | F |

## Confirmed Contract Matches

- The contract distinguishes planning-only #388 work from strict parser-behavior
  readiness.
- `parser_behavior_ready=false` is preserved.
- `pipeline_activation_ready_for_issue_388=false` is preserved.
- `evidence_pipeline_planning_ready_for_issue_388=false` is preserved.
- `report_preconditions_ready_for_issue_388=true` is treated only as a
  report-local planning signal.
- #381 through #387 stale start-condition wording is identified without editing
  issue bodies.
- The child sequence is coherent and intentionally orders #386 before #385:
  #381, #382, #383, #384, #386, #385, #387.
- #381 implementation remains blocked until a refresh comment or #381-specific
  contract exists.
- #434 remains the parent gate for private-evidence rows and private-evidence
  execution.
- Private logs, private/live checks, fixture promotion, parser-truth changes,
  golden-replay expected-output blessing, Codex F/G bypasses, and readiness
  overclaims remain explicitly blocked.

## Contract Mismatches

None.

## Missing Tests

None for this contract-only package. The contract correctly limits validation to
corpus parity report output, agent-doc checks, diff formatting, and scoped
secret/protected-surface checks. Future child contracts must define their own
focused tests before implementation.

## Drift Notes

Issue lifecycle drift is present but handled: #381 through #387 still contain
stale synthetic-all-45 start-condition wording, and #388 still includes an older
embedded historical handoff block. The contract explicitly classifies that
wording as stale context and requires child refresh or child-specific contracts
before implementation.

No repo drift, workbook drift, deployment drift, private-data drift, PR lifecycle
drift, tracker closure drift, parser-truth drift, or protected-surface drift was
introduced by this package.

## Recommendation

Approve for Codex F contract-only submission.

After Codex F/G submission and deployment, the next substantive planning role
should be Codex B for a #381-specific contract, unless the user chooses Codex A
to rewrite or split #381 first.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #518.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/518

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Reviewed artifacts:
- docs/contracts/parser_evidence_pipeline_planning_umbrella.md
- docs/contract_test_reports/parser_evidence_pipeline_planning_umbrella.md

Goal:
Submit the contract-only planning umbrella package as a draft PR targeting main.

Validation already passed in Codex E:
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- git diff --check
- path-scoped secret/private-marker scan
- path-scoped protected-surface scan
- path-scoped validation selector

Do not implement code, edit GitHub issue bodies, activate #381, run private/live
checks, read private logs, promote fixtures or corpus statuses, or claim parser
behavior readiness, strict pipeline readiness, release readiness, production
readiness, analytics truth, AI truth, coaching truth, or full parser regression
parity.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/518"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  related_child_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/381"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  recently_closed_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_evidence_pipeline_planning_umbrella.md"
  target_artifact: "docs/contract_test_reports/parser_evidence_pipeline_planning_umbrella.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  report_preconditions_ready_for_issue_388: true
  evidence_pipeline_planning_ready_for_issue_388: false
  verdict: "no_blocking_findings_ready_for_submitter"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface scan"
    - "path-scoped validation selector"
  stop_conditions:
    - "Do not implement code from this umbrella contract."
    - "Do not edit GitHub issue bodies."
    - "Do not activate #381 for implementation."
    - "Do not read private logs or run private/live checks."
    - "Do not promote blocked, report-only, private-evidence, or external-boundary rows."
    - "Do not create fixtures or fixture-promotion packets."
    - "Do not claim parser_behavior_ready, strict pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
