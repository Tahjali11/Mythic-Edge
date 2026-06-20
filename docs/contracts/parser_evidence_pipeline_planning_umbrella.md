# Parser Evidence Pipeline Planning Umbrella Contract

## Module

Planning-only umbrella for issue #388, the parser evidence pipeline tracker.

Plain English: this contract defines how the parser evidence-pipeline lane may
begin as planning work without turning into private-log reading, fixture
promotion, parser-truth changes, or readiness overclaims. It keeps strict
parser-behavior readiness separate from planning readiness, preserves
`parser_behavior_ready=false`, preserves
`pipeline_activation_ready_for_issue_388=false`, and requires a fresh scoped
contract before any #381 implementation.

This contract does not implement code, open a PR, edit GitHub issue bodies,
activate #381, read private logs, run private checks, promote fixtures, or
claim parser behavior readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/518
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Potential first child issue: https://github.com/Tahjali11/Mythic-Edge/issues/381
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Recently closed corpus tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Latest completed activation issue: https://github.com/Tahjali11/Mythic-Edge/issues/516
- Latest completed PR: https://github.com/Tahjali11/Mythic-Edge/pull/517
- Latest verified commit: `e760ebdeb65eef9b2dbbc53a42a0bd1e759a7b71`
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed during this Codex B pass:

- `main` and `origin/main` are at
  `e760ebdeb65eef9b2dbbc53a42a0bd1e759a7b71`.
- Issue #518 is open.
- Tracker #158 is closed.
- Tracker #388 is open and has amended planning-only start wording.
- Child issues #381 through #387 are open.
- Issue #381 through #387 bodies still contain stale start-condition language
  requiring all 45 corpus families to have synthetic coverage or stronger.
- Parent private-evidence issue #434 is open.
- The operating checkout remote matches
  `https://github.com/Tahjali11/Mythic-Edge.git`.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- Issue #518
- Tracker #388
- Issues #381, #382, #383, #384, #385, #386, and #387
- Parent private-evidence issue #434
- Recently closed tracker #158
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
- `docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md`
- `docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/parser_corpus_readiness_metrics.md`
- `docs/contracts/parser_corpus_behavior_readiness_applicability_semantics.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

## Observed Current Behavior

The current corpus parity CLI output is:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=22, report_only=11, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Current readiness facts:

```yaml
classification_complete: true
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
readiness_verdict: "classification_complete_not_behavior_ready"
evidence_pipeline_planning:
  report_preconditions_ready_for_issue_388: true
  evidence_pipeline_planning_ready_for_issue_388: false
  readiness_verdict: "report_preconditions_ready_lifecycle_approval_pending"
  allowed_scope: "evidence_pipeline_tooling_planning_only"
behavior_applicability:
  parser_behavior_applicability_ready: false
  parser_behavior_applicable_ready_family_count: 27
  parser_behavior_applicable_not_ready_family_count: 10
```

Tracker #388 now has amended start wording that allows planning-only work
after #158 classification lifecycle reconciliation and explicit boundaries.
However, #388's older embedded historical handoff block still contains stale
synthetic-all-45 wording. This contract treats the current body start condition
as the active tracker text and treats the older embedded handoff text as stale
context.

Issues #381 through #387 still contain stale start-condition wording. They
must not be used directly for implementation without a refresh comment,
problem-representation update, or issue-specific contract that points to this
umbrella and the amended #388 planning-only boundary.

## Problem

The evidence pipeline is the bridge from local observable evidence to reviewed
candidate packets and, eventually, sanitized golden replay fixture drafts. That
bridge is useful, but it is high risk because it sits near raw local logs,
private evidence, fixture promotion, and parser regression truth.

The current safe state is:

- corpus classification/report preconditions are complete enough to plan;
- strict parser-behavior readiness is not complete;
- private-evidence rows remain blocked or local-only;
- #381 implementation is not authorized by #518;
- fixture promotion remains blocked until later scoped proof and review gates.

Without this umbrella, future threads could read #381's stale start condition,
read #388's historical handoff block, or overread #158 closure as permission to
start implementation, read private logs, or bulk-bless parser output.

## Scope Decision

This contract approves planning-only #388 umbrella semantics.

Implementation is not authorized by this contract. The immediate workflow
route after this contract is review of the contract-only package. After the
contract is reviewed, submitted, and deployed, the next substantive workflow
step should be a #381-specific refresh/contract before any adapter
implementation.

This contract allows future Codex A/B/G work to:

- refresh #381 start-condition wording through a comment or new scoped
  contract;
- select a #381-specific contract route;
- sequence #381 through #387 one child issue at a time;
- define local-only artifact and privacy boundaries before any private run;
- keep #434 as the parent gate for private-evidence execution.

This contract does not authorize Codex C implementation. A later Codex C may
run only after a child issue has its own contract that names exact source
classes, artifact shapes, tests, and private-evidence stop conditions.

## Owning Layer

Owning layer: Quality / Governance, with Corpus / Provenance support.

Quality / Governance owns workflow sequencing, issue refresh requirements,
role routing, stop conditions, and protected-surface boundaries.

Corpus / Provenance owns the evidence-pipeline artifact vocabulary,
candidate-review concepts, fixture-promotion proof concepts, and corpus
metadata movement rules.

Parser remains the truth owner for parser interpretation, parser events,
router semantics, parser state, match/game identity, deduplication, and final
reconciliation.

## Internal Project Area

Primary: Quality / Governance.

Supporting: Corpus / Provenance.

This contract is not a Parser module, local app module, analytics module,
workbook/transport module, AI module, coaching module, CI gate, merge gate,
deploy gate, readiness gate, production module, private-evidence execution
packet, or fixture-promotion package.

## Truth Owner

Truth owner for current corpus status and readiness metrics:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth owner for #388 planning semantics:

- current #388 body;
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`;
- this umbrella contract;
- future reviewed child contracts.

Truth owner for private-evidence execution boundaries:

- issue #434;
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`;
- `docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md`;
- `docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md`;
- any later explicit private-evidence issue, contract, privacy review, and
  user approval.

This contract does not make the evidence pipeline a truth owner for parser
facts, private log content, fixture expected output, corpus status promotion,
merge readiness, release readiness, production behavior, analytics truth, AI
truth, or coaching truth.

## Bridge-Code Status

`deferred_future_boundary`

This contract authorizes no bridge code. Future child issues may define bridge
code from local/private sources to local-only review artifacts, but only under
their own contracts.

Potential future source areas:

- Generated / Local Artifacts, for local-only source pointers, normalized
  source copies, candidate reports, review packets, proof packets, and draft
  fixture outputs.
- Corpus / Provenance, for committed sanitized fixtures, golden replay
  manifests, session-ledger entries, and corpus manifest changes after review.

Forbidden reverse flow:

- evidence-pipeline artifacts must not change parser behavior, parser event
  classes, router behavior, parser state final reconciliation, match/game
  identity, deduplication, workbook schema, webhook payload shape, Apps Script
  behavior, Google Sheets sync, output transport, analytics behavior, AI or
  coaching behavior, CI gates, merge policy, deploy policy, production
  behavior, or final integration policy.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`

Expected future review artifact:

- `docs/contract_test_reports/parser_evidence_pipeline_planning_umbrella.md`

Expected future child-contract artifacts, not created by this contract:

- `docs/contracts/parser_evidence_utc_log_source_adapter.md`
- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`
- `docs/contracts/parser_evidence_harvest_review_packets.md`
- `docs/contracts/parser_evidence_fixture_promotion_proof.md`
- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- `docs/contracts/parser_evidence_golden_replay_fixture_draft_generator.md`
- `docs/contracts/parser_evidence_pr_assist_workflow.md`

Files this contract may reference but does not authorize modification of:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- existing parser, diagnostics, golden replay, drift, evidence-ledger,
  workbook, analytics, AI, local app, and tooling code.

Not owned by this contract:

- raw `Player.log` files;
- raw or normalized `UTC_Log` files;
- local app-data;
- private harvest artifacts;
- local offset state;
- runtime status files;
- generated SQLite files;
- failed posts;
- workbook exports;
- screenshots;
- exact private paths;
- raw hashes;
- packet captures;
- network traces;
- OS/router/firewall diagnostics;
- secrets, credentials, tokens, API keys, or webhook URLs.

## Public Interface

This contract creates a workflow interface, not a runtime API.

### Activation States

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
report_preconditions_ready_for_issue_388: true
evidence_pipeline_planning_ready_for_issue_388: false
```

Meaning:

- `parser_behavior_ready=false`: strict parser-behavior evidence is not
  complete.
- `pipeline_activation_ready_for_issue_388=false`: the strict legacy
  all-family behavior gate is not complete.
- `report_preconditions_ready_for_issue_388=true`: committed report metadata
  has no missing, partial, or deferred rows and can support planning.
- `evidence_pipeline_planning_ready_for_issue_388=false`: the report itself
  cannot assert live workflow approval; #381 implementation still needs a
  scoped contract and user-approved workflow path.

### Child Issue Sequence

The planned sequence is:

1. #381: UTC_Log source adapter boundary.
2. #382: local Player.log / UTC_Log harvest candidate reports.
3. #383: human-readable harvest review packets.
4. #384: report-only fixture promotion proof generator.
5. #386: corpus metadata diff generator.
6. #385: golden replay fixture and manifest draft generator.
7. #387: PR-assist workflow for reviewed fixture promotions.

#386 is intentionally listed before #385 in this umbrella sequence so metadata
movement rules and anti-overclaim checks can be proven before any tool drafts
committable fixture files.

### Child Status Vocabulary

Future child contracts should use these planning statuses:

- `planning_not_started`: no contract has been written for the child.
- `contract_required`: child issue has stale or insufficient start conditions.
- `contract_ready_for_review`: child contract exists and is ready for Codex E.
- `implementation_authorized`: reviewed child contract authorizes Codex C.
- `private_execution_blocked`: private or live evidence would be required but
  no explicit local approval exists.
- `fixture_promotion_blocked`: generated fixture, expected output, manifest,
  or corpus metadata promotion would be required but proof/review/deployer
  gates are not complete.

### Artifact Classes

Future child issues may define these artifact classes:

- `local_source_pointer`: local-only symbolic source reference, not a raw path.
- `normalized_source_local_only`: local-only normalized copy or view.
- `candidate_harvest_report`: local-only candidate summary and scoring.
- `review_packet`: redacted human/Codex review bundle.
- `promotion_proof`: report-only proof package with pass/review/fail statuses.
- `metadata_diff_draft`: proposed corpus/session-ledger diff, not applied.
- `fixture_manifest_draft`: proposed sanitized fixture and replay manifest,
  not committed by default.
- `pr_assist_packet`: submitter helper text and file list, not merge authority.

Committed repo artifacts may use these classes only after a child contract
authorizes the exact path, shape, and redaction rules.

## Child Issue Refresh Requirements

### #381 UTC_Log Source Adapter

#381 must be refreshed before implementation. Its current body still says the
old synthetic-all-45 start condition. A refresh may be either:

- a Codex G or user-approved issue comment that points to this umbrella and
  the amended #388 start condition; or
- a Codex B #381-specific contract that states the current #381 body start
  condition is stale and superseded for planning purposes.

#381-specific contract must decide:

- whether Codex C may implement synthetic-fixture-only source adapter behavior;
- whether private source discovery is only a non-executed plan;
- whether exact user-selected file support is allowed without reading private
  content in tests;
- local-only output root policy;
- redaction and private path policy;
- whether `UTC_Log` normalization may feed existing parser/replay paths
  without becoming a second parser.

No #381 implementation may run before that contract exists.

### #382 Harvest Candidate Reports

#382 requires either:

- completed #381 adapter support; or
- an explicit `Player.log`-only bypass decision in a #382 contract.

#382 must not read private logs by default. It may implement synthetic-fixture
tests and local-only report shape only after its own contract authorizes the
interfaces.

### #383 Review Packets

#383 consumes candidate reports, not raw logs. Its contract must define:

- redacted packet schema;
- `reviewer_decision` status vocabulary;
- privacy report statuses;
- Codex-consumable summary shape;
- hard rejection of raw private excerpts and exact private paths.

### #384 Promotion Proof

#384 is report-only. It may explain whether an already approved candidate
would strengthen parser evidence, but it must not create fixtures, apply
metadata diffs, update baselines, open PRs, or decide truth.

### #386 Metadata Diff

#386 drafts corpus manifest and session-ledger diffs only after #384 proof
rules exist. Its contract must prevent accidental row promotion, unrelated
family movement, and report-only/private/external-boundary overclaims.

### #385 Fixture And Manifest Drafts

#385 is the first child that may eventually draft committable sanitized
fixture files. It must wait until #384 proof rules and #386 metadata-diff
rules exist. It requires its own privacy, minimization, expected-output,
golden replay, and review gates.

### #387 PR Assist

#387 must remain last. It may prepare draft PR text and file lists for Codex F,
but it must not stage, commit, push, merge, close issues, update trackers as
complete, or bypass Codex F/G boundaries.

## Inputs

Allowed inputs for this umbrella:

- committed repo docs, contracts, source code, tests, fixture metadata, and
  reports;
- GitHub issue and PR metadata for #158, #381 through #388, #434, #516, #517,
  and #518;
- current corpus parity report output;
- current corpus manifest and session-ledger metadata.

Allowed future child-contract inputs:

- committed sanitized fixtures;
- synthetic fixtures;
- existing local-only/private-evidence contracts;
- public GitHub issue metadata;
- current repo source and tests.

Forbidden inputs for this umbrella and for future child work unless a later
explicit contract and user approval authorize the exact operation:

- raw private `Player.log` content;
- raw or normalized private `UTC_Log` content;
- private app-data contents;
- private smoke outputs;
- local-only offset windows;
- private drift reports;
- private harvest packets;
- exact private paths;
- exact offsets or exact file sizes;
- raw hashes;
- raw log lines;
- screenshots;
- SQLite files;
- workbook exports;
- runtime artifacts;
- failed posts;
- credentials, tokens, API keys, webhook URLs, or secrets;
- decklists, card choices, private strategy notes;
- IP/network traces, packet captures, OS/router diagnostics, firewall logs,
  or Wi-Fi logs;
- external raw corpus contents.

## Outputs

Allowed output for this Codex B pass:

- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`;
- a pasteable next-thread prompt;
- workflow handoff block.

Allowed future child outputs only after scoped contracts:

- local-only source pointers;
- local-only normalized source artifacts;
- local-only candidate reports;
- local-only review packets;
- report-only promotion proofs;
- proposed corpus metadata diffs;
- draft sanitized fixtures and manifests;
- PR-assist packets.

Forbidden output:

- #381 implementation;
- private log reads;
- private/live checks;
- changed parser behavior;
- changed parser event classes;
- changed parser state final reconciliation;
- changed router semantics;
- changed workbook schema, webhook payload shape, Apps Script behavior,
  Google Sheets sync, or output transport;
- changed corpus status vocabulary;
- manifest/session-ledger promotion;
- committed raw/private/generated/runtime artifacts;
- fixture promotion without proof/review/deployer approval;
- readiness claims.

## Required Guarantees

- `parser_behavior_ready` remains false.
- `pipeline_activation_ready_for_issue_388` remains false.
- `report_preconditions_ready_for_issue_388` may be true as a report-local
  planning signal only.
- `evidence_pipeline_planning_ready_for_issue_388` remains false unless a
  later contract and workflow update define a repo-owned way to verify
  lifecycle approval.
- #381 through #387 must be refreshed or contracted before implementation.
- #381 is not activated for implementation by this umbrella.
- #434 remains the parent gate for private-evidence rows and private evidence
  execution.
- The evidence pipeline prepares evidence; it does not bless parser truth.
- Golden replay expected output remains review-governed and must not be
  bulk-generated into committed truth.
- Codex F submitter and Codex G deployer boundaries remain intact.

## Unknowns

- Whether #381 should be refreshed by an issue comment or a replacement
  issue-specific contract. This contract recommends a #381-specific contract.
- Whether #382 should support a `Player.log`-only bypass before #381. This
  requires a #382-specific contract.
- Whether future child implementations should share one local artifact schema
  or define separate schemas per child. This umbrella recommends per-child
  contracts first.
- Whether `evidence_pipeline_planning_ready_for_issue_388` should ever become
  true in generated reports, or remain a lifecycle-only human/Codex G
  decision. This contract does not change that field.

## Suspected Gaps

- #381 through #387 issue bodies still carry stale synthetic-all-45 language.
- #388 body is amended, but its historical embedded handoff block is stale.
- The current repo has readiness metrics but no umbrella artifact explaining
  how to use them to sequence child evidence-pipeline work.
- The boundary between local-only harvest artifacts and future committed
  fixture drafts needs to be enforced one child issue at a time.

## Error Behavior

If a future thread tries to implement #381 directly from its current body,
stop and route to Codex B for a #381-specific contract.

If a future thread needs private or live data, stop unless the active issue,
contract, privacy review, and user approval authorize that exact data source,
window, and artifact class.

If a future thread would promote a report-only, blocked-private, or
external-boundary row, stop unless a dedicated proof/review/deployer gate has
authorized that exact promotion.

If a future thread would treat a generated fixture draft as expected truth,
stop and route to Codex E or Codex B.

If a future thread would change parser behavior, parser events, parser state,
router semantics, workbook/webhook/App Script surfaces, analytics behavior, AI
behavior, coaching behavior, CI gates, merge policy, deploy policy, production
behavior, or final integration policy, stop and require a separate scoped
issue and contract.

## Side Effects

Side effect of this Codex B pass:

- adds `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`.

No code, tests, corpus metadata, fixture files, private artifacts, issue
bodies, trackers, PRs, or runtime files are changed by this contract.

Future side effects require child-specific contracts.

## Dependency Order

1. Review and submit this umbrella contract.
2. Deploy/merge the contract through Codex F/G only after review and explicit
   user direction.
3. Refresh #381 start-condition authority with a #381-specific contract or
   approved issue comment.
4. Contract and implement #381, if still selected.
5. Contract and implement #382, optionally with a `Player.log`-only bypass if
   #381 is explicitly bypassed.
6. Contract and implement #383.
7. Contract and implement #384.
8. Contract and implement #386.
9. Contract and implement #385.
10. Contract and implement #387.

## Compatibility

This contract is compatible with:

- current `readiness_metrics` keys;
- current `behavior_applicability` keys;
- current `evidence_pipeline_planning` keys;
- current corpus manifest/session-ledger status vocabulary;
- current #388 body start condition;
- current private-evidence contracts;
- current golden replay and fixture policy contracts.

This contract intentionally supersedes stale start-condition wording in #381
through #387 only for future planning interpretation. It does not edit those
issue bodies.

## Tests Required

For this contract-only pass:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' docs/contracts/parser_evidence_pipeline_planning_umbrella.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_pipeline_planning_umbrella.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_pipeline_planning_umbrella.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

No focused pytest is required for this contract-only pass beyond the corpus
report command, because this contract does not change code.

Future child contracts must define their own focused unit, integration,
golden replay, private-artifact, secret/private-marker, protected-surface, and
review checks.

## Acceptance Criteria

- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md` exists.
- The contract distinguishes planning-only #388 work from strict
  parser-behavior readiness.
- The contract preserves `parser_behavior_ready=false`.
- The contract preserves `pipeline_activation_ready_for_issue_388=false`.
- The contract preserves `evidence_pipeline_planning_ready_for_issue_388=false`.
- The contract treats `report_preconditions_ready_for_issue_388=true` as a
  report-local planning signal only.
- The contract identifies #381 through #387 stale start-condition language.
- The contract requires #381 refresh or a #381-specific contract before
  implementation.
- The contract sequences #381, #382, #383, #384, #386, #385, and #387.
- The contract blocks private log reads, private checks, fixture promotion,
  parser-truth changes, and readiness overclaims.
- The contract routes next to review, not implementation.

## Next Workflow Action

Recommended next role: Codex E: Module Reviewer / Contract Tester.

Codex C is not needed for this issue unless review finds a missing docs/report
scaffold that requires implementation. After review, submitter/deployer work
may merge the contract if the user asks. After merge, the next substantive
planning role should be Codex B for a #381-specific contract, or Codex A if
the user wants to rewrite/split #381 first.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for issue #518.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/518

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Potential first child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/381

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Recently closed tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Contract:
docs/contracts/parser_evidence_pipeline_planning_umbrella.md

Goal:
Review the #518 umbrella contract for correctness, completeness, and safety. Confirm it preserves planning-only #388 semantics without authorizing #381 implementation, private-log reads, fixture promotion, parser behavior changes, or readiness overclaims.

Review focus:
- The contract distinguishes strict parser-behavior readiness from planning-only evidence-pipeline work.
- `parser_behavior_ready=false`, `pipeline_activation_ready_for_issue_388=false`, and `evidence_pipeline_planning_ready_for_issue_388=false` are preserved.
- `report_preconditions_ready_for_issue_388=true` is treated only as a report-local planning signal.
- #381 through #387 stale start-condition wording is handled without editing issue bodies.
- The child sequence #381, #382, #383, #384, #386, #385, #387 is coherent.
- Private-evidence, fixture-promotion, parser-truth, golden-replay, Codex F/G, and readiness boundaries are intact.

Validation:
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
- `python3 tools/check_agent_docs.py`
- `git diff --check`
- path-scoped secret/private-marker scan for the contract
- path-scoped protected-surface scan for the contract

Do not:
- Implement code.
- Edit GitHub issue bodies.
- Open a PR.
- Activate #381.
- Run private/live checks.
- Read private logs.
- Promote fixtures or corpus statuses.
- Claim parser behavior readiness, strict pipeline readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity.

Expected output:
- Findings first, if any.
- Contract-test verdict.
- Validation evidence.
- Remaining risks.
- Next recommended role.
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/518"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  related_child_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/381"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  recently_closed_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue problem representation"
  target_artifact: "docs/contract_test_reports/parser_evidence_pipeline_planning_umbrella.md"
  produced_artifact: "docs/contracts/parser_evidence_pipeline_planning_umbrella.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  report_preconditions_ready_for_issue_388: true
  evidence_pipeline_planning_ready_for_issue_388: false
  recommended_after_review: "Codex F/G for contract-only submission, then Codex B or A for #381 refresh."
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface scan"
    - "path-scoped validation selector"
  stop_conditions:
    - "Do not implement code from this umbrella contract."
    - "Do not edit GitHub issue bodies in Codex B/E."
    - "Do not activate #381 for implementation."
    - "Do not read private logs or run private/live checks."
    - "Do not promote blocked, report-only, private-evidence, or external-boundary rows."
    - "Do not create fixtures or fixture-promotion packets."
    - "Do not claim parser_behavior_ready, strict pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
