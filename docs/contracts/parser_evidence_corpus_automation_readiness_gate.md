# Parser Evidence Corpus Automation Readiness Gate Contract

## Module

Planning contract for issue #560, the corpus automation readiness gate for the
parser evidence pipeline under tracker #388.

Plain English: this contract defines when Mythic Edge may say the external
corpus automation side of the harvest -> sanitize -> corpus update -> metadata
ratchet -> confidence report loop is ready enough to count as part of #388's
completion criteria. It is a gate contract only. It does not implement
Mythic-Edge-Corpus automation, publish corpus packages, receive dispatch
events, run ratchets, open baseline PRs, promote fixtures, update corpus
metadata, read private evidence, or change parser behavior.

Current Codex B decision: #560 is not ready to clear the corpus automation
gate. The required Mythic-Edge-Corpus issues #1 through #6 are open and must be
completed, reviewed, and mapped back to this gate before #388 may claim the
complete Manasight-like loop exists.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/560
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/434
- Dependency issue: https://github.com/Tahjali11/Mythic-Edge/issues/558
- Dependency PR: https://github.com/Tahjali11/Mythic-Edge/pull/564
- Dependency merge commit:
  `455e4dc5e6168d79112f5164ec5eab7ecd391342`
- Base branch: `main`
- Target branch: `main`
- Working branch:
  `codex/parser-evidence-corpus-automation-readiness-560`
- Risk tier: High

Observed during this Codex B pass:

- The primary Mythic Edge checkout contained unrelated local governance edits
  and an unrelated untracked contract, so this contract was written in a clean
  issue worktree.
- The issue worktree was created from `origin/main` at
  `455e4dc5e6168d79112f5164ec5eab7ecd391342`.
- Issue #560 was open.
- Tracker #388 was open.
- Parent private-evidence issue #434 was open.
- Issue #558 was closed.
- PR #564 was merged into `main`.
- Mythic-Edge-Corpus issues #1 through #6 were open.

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

Tracker #388 remains open. This contract does not activate #388, activate
#381, authorize private harvest, authorize fixture promotion, authorize corpus
metadata movement, or claim parser behavior readiness.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #560
- Tracker #388
- Parent private-evidence issue #434
- Issue #558 and PR #564
- `docs/contracts/parser_evidence_pipeline_activation_contract.md`
- `docs/contracts/parser_evidence_bounded_local_dry_run.md`
- `docs/contracts/parser_evidence_confidence_claim_vocabulary.md`
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- `docs/contracts/parser_recovery_human_approved_parser_corpus_update_workflow.md`
- `docs/local_artifacts_manifest.json`
- Public GitHub metadata for Mythic-Edge-Corpus issues #1 through #6

No private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop,
packet, OS/router, diagnostics, drift, watcher, private smoke, workbook
export, SQLite, generated local artifact, or private corpus artifact was run,
tailed, hashed, copied, summarized, or read.

## Observed Current Behavior

Mythic Edge now has reviewed planning and helper contracts for:

- #388 pipeline activation semantics;
- #559 bounded local dry-run semantics;
- #558 confidence-claim vocabulary;
- corpus metadata diff drafts;
- human-approved parser/corpus update routing;
- candidate packets, review packets, fixture-promotion proof objects, fixture
  drafts, manifest drafts, and PR-assist packets.

Those artifacts are not enough to claim the full corpus loop. The sibling
Mythic-Edge-Corpus repository still needs the automation that can package,
validate, release, dispatch, compare, and propose baseline updates safely.

Current preserved readiness and authorization facts remain:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
dry_run_execution_authorized: false
implementation_authorized: false
corpus_automation_readiness_gate_cleared: false
```

Observed Mythic-Edge-Corpus gate state at contract time:

| Corpus issue | Required capability | Observed state | Gate impact |
| --- | --- | --- | --- |
| Tahjali11/Mythic-Edge-Corpus#1 | Local corpus package preview command | Open | Blocks package preview gate |
| Tahjali11/Mythic-Edge-Corpus#2 | PR validation for package safety | Open | Blocks package validation gate |
| Tahjali11/Mythic-Edge-Corpus#3 | Release publishing for reviewed packages | Open | Blocks release gate |
| Tahjali11/Mythic-Edge-Corpus#4 | Bounded `repository_dispatch` into Mythic Edge | Open | Blocks dispatch gate |
| Tahjali11/Mythic-Edge-Corpus#5 | Ratchet comparison for released packages | Open | Blocks ratchet gate |
| Tahjali11/Mythic-Edge-Corpus#6 | Draft baseline PR workflow after ratchet comparison | Open | Blocks baseline proposal gate |

## Problem

The first bad value is treating Mythic Edge helper tooling as proof that the
external corpus automation loop is complete.

The second bad value is treating future corpus automation as permission to
approve parser truth, fixture promotion, corpus metadata changes, or baseline
updates automatically.

Without this gate, #388 could appear complete because Mythic Edge can produce
candidate packets, review packets, fixture drafts, and metadata diffs, even
though the corpus repo cannot yet safely package, validate, release, dispatch,
ratchet, or draft baseline PRs.

## Scope Decision

This contract approves a docs-only readiness gate.

Selected status:

```yaml
selected_status: "blocked_external_corpus_repo_pending"
selected_claim_state: "external_boundary_blocked"
privacy_boundary: "external_reference_only"
review_requirement: "corpus_repo_contract_required"
```

This contract defines:

- the Mythic-Edge-side corpus automation readiness checklist;
- how Mythic Edge may verify corpus release, dispatch, ratchet, and baseline
  proposal evidence later;
- how generated Mythic Edge corpus metadata diffs hand off to reviewed
  Mythic-Edge-Corpus packages;
- what #388 may claim after all corpus automation gates exist;
- what #388 must still not claim after those gates exist;
- failure statuses for failed package validation, failed release, failed
  dispatch, failed ratchet, stale corpus release, or rejected baseline PR;
- validation expectations for later Codex C/E if a tiny gate-report validator
  is separately authorized.

This contract does not authorize:

- code implementation in Codex B;
- Mythic-Edge-Corpus implementation in this repo;
- source-repo mutation outside Mythic Edge;
- corpus package publication;
- release creation;
- dispatch event sending or receiving;
- ratchet execution;
- baseline PR creation;
- corpus manifest edits;
- session ledger edits;
- fixture creation;
- fixture promotion;
- private source reads;
- private harvest execution;
- parser behavior changes;
- #388 or #381 activation;
- release readiness, deploy readiness, production behavior, analytics truth,
  AI truth, or coaching truth.

## Owning Layer

Owning layer: Quality / Governance, with Corpus / Provenance support.

Quality / Governance owns:

- #388 readiness-gate semantics;
- cross-repo dependency recording;
- role routing;
- approval requirements;
- stop conditions;
- false-readiness preservation.

Corpus / Provenance owns:

- corpus package preview evidence;
- package validation evidence;
- release metadata;
- dispatch metadata;
- ratchet report metadata;
- baseline proposal metadata;
- corpus metadata diff handoff rules.

Parser remains the truth owner for parser interpretation, parser events,
router behavior, parser state, match/game identity, deduplication, and final
reconciliation.

## Internal Project Area

Primary: Quality / Governance.

Supporting: Corpus / Provenance.

This contract is not a parser behavior module, private-evidence execution
packet, corpus package implementation, release workflow, ratchet workflow,
baseline PR workflow, CI gate, merge gate, deploy gate, analytics module, AI
module, coaching module, workbook module, or production module.

## Truth Owner

This contract owns the Mythic-Edge-side corpus automation readiness gate only.

Truth owners remain:

- parser facts: parser and state layer;
- confidence vocabulary: #558 contract;
- local dry-run process status: #559 contract;
- metadata diff proposals: #386 contract;
- human approval routing: #456 contract;
- private evidence execution: #434 and later explicit private-evidence
  contracts;
- corpus package preview, validation, release, dispatch, ratchet, and baseline
  proposal behavior: the owning Mythic-Edge-Corpus issues and their later
  contracts/PRs.

This contract must not become truth for parser behavior, fixture correctness,
corpus status movement, private evidence, baseline approval, release
readiness, deploy readiness, production behavior, analytics truth, AI truth,
or coaching truth.

## Bridge-Code Status

`deferred_future_boundary`

This contract authorizes no bridge code. A later contract may authorize a
small Mythic Edge gate-report validator that consumes public GitHub/release
metadata and public-safe ratchet summaries. That later validator must not read
private evidence, mutate corpus metadata, run parser comparisons, create
baseline PRs, approve parser truth, or alter #388 readiness flags by itself.

## Files Owned By This Contract

- `docs/contracts/parser_evidence_corpus_automation_readiness_gate.md`

Potential later artifacts, if separately authorized:

- `docs/implementation_handoffs/parser_evidence_corpus_automation_readiness_gate_comparison.md`
- `docs/contract_test_reports/parser_evidence_corpus_automation_readiness_gate.md`

This contract does not authorize edits to:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- golden replay fixtures;
- expected-output files;
- feature-equity baselines;
- corpus package contents;
- Mythic-Edge-Corpus files;
- parser source;
- private evidence artifacts;
- generated local artifacts;
- GitHub issue or PR bodies.

## Public Interface

Future machine-readable gate reports, if separately authorized, should use:

```yaml
schema_version: "parser_evidence_corpus_automation_readiness_gate.v1"
object: "mythic_edge_parser_evidence_corpus_automation_readiness_gate"
gate_id: "<public-safe id>"
repository: "Tahjali11/Mythic-Edge"
repository_url: "https://github.com/Tahjali11/Mythic-Edge"
tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/560"
parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
dependency_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/558"
gate_status: "<allowed gate status>"
claim_state: "<#558-compatible claim state>"
corpus_dependencies: []
mythic_edge_consumer_requirements: []
failure_summary: []
authorization_flags:
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  dry_run_execution_authorized: false
  implementation_authorized: false
  corpus_automation_readiness_gate_cleared: false
non_claims: []
verdict: "<public-safe verdict>"
```

Gate reports are workflow metadata only. They must not be consumed by runtime
parser code, workbook sync code, analytics code, AI/coaching systems, release
tooling, deploy tooling, or production systems as truth.

## Gate Status Vocabulary

Allowed gate statuses:

- `blocked_external_corpus_repo_pending`
- `blocked_package_preview_missing`
- `blocked_package_validation_missing`
- `blocked_release_publishing_missing`
- `blocked_dispatch_bridge_missing`
- `blocked_ratchet_comparison_missing`
- `blocked_baseline_proposal_missing`
- `blocked_corpus_package_validation_failed`
- `blocked_corpus_release_failed`
- `blocked_dispatch_failed`
- `blocked_ratchet_failed`
- `blocked_stale_corpus_release`
- `blocked_rejected_baseline_pr`
- `blocked_unreviewed_corpus_pr`
- `blocked_forbidden_content`
- `blocked_missing_human_review`
- `blocked_overclaim`
- `ready_for_human_gate_review`
- `ready_for_corpus_loop_claim_after_review`

The strongest status this Codex B contract may claim is:

```yaml
gate_status: "blocked_external_corpus_repo_pending"
```

`ready_for_corpus_loop_claim_after_review` may be used only after every
required corpus dependency is complete, evidence refs are public-safe,
validation summaries are reviewed, and Codex E/F/G routing has accepted the
gate update.

## Required Corpus Dependency Gates

The complete corpus automation gate requires all of these sibling-repo
capabilities to be reviewed and linked.

### Gate 1: Package Preview

Required source: Tahjali11/Mythic-Edge-Corpus#1.

Required evidence:

- merged PR or equivalent reviewed implementation reference;
- deterministic preview command name and version;
- package inventory summary shape;
- safety scan summary;
- manifest/session metadata consistency check summary;
- explicit forbidden-content stop behavior.

Mapped claim state: `corpus_package_validated` is not allowed yet. Before PR
validation exists, this gate may support only `external_boundary_blocked` or
`coverage_deferred`.

### Gate 2: Package PR Validation

Required source: Tahjali11/Mythic-Edge-Corpus#2.

Required evidence:

- reviewed PR validation workflow or equivalent validation contract;
- preview command integrated into PR validation;
- fail-closed behavior for private/generated/runtime artifacts;
- manifest/session metadata checks;
- evidence that validation reports actionable failures without rewriting
  contributor branches.

Mapped claim state: package validation can support `corpus_package_validated`
only for the exact reviewed package scope.

### Gate 3: Reviewed Release Publishing

Required source: Tahjali11/Mythic-Edge-Corpus#3.

Required evidence:

- release artifact shape;
- release tag or version rule;
- package checksum or equivalent integrity metadata;
- release-to-validation provenance link;
- default-branch release rule;
- non-claim text preserving parser truth and readiness boundaries.

Mapped claim state: a reviewed release may feed `corpus_package_validated`.
It must not feed `ratchet_passed` until the Mythic Edge consuming workflow
runs a ratchet comparison.

### Gate 4: Bounded Dispatch Into Mythic Edge

Required source: Tahjali11/Mythic-Edge-Corpus#4 and paired Mythic Edge
receiving contract if needed.

Required evidence:

- dispatch event name;
- bounded payload schema;
- allowed payload fields;
- least-privilege token/secret handling summary without secret values;
- receiving workflow expectation in Mythic Edge;
- failure and retry semantics;
- explicit statement that dispatch is notification only.

Mapped claim state: dispatch may route to ratchet review. It must not update
baselines, mutate parser code, or claim readiness.

### Gate 5: Ratchet Comparison

Required source: Tahjali11/Mythic-Edge-Corpus#5 and Mythic Edge consumer
contract/PR if needed.

Required evidence:

- released package input ref;
- baseline ref;
- deterministic comparison command or workflow ref;
- report shape for passes, failures, missing families, changed outputs, and
  degraded evidence;
- privacy and forbidden-content scan summary;
- review routing for new failures or changed outputs.

Mapped claim state: a passing scoped ratchet report may support
`ratchet_passed`. It must not support `coverage_confirmed` without committed
sanitized evidence, reviewed metadata, and the owning scoped contract.

### Gate 6: Draft Baseline PR Proposal

Required source: Tahjali11/Mythic-Edge-Corpus#6 and Mythic Edge consumer
contract/PR if needed.

Required evidence:

- draft PR creation rules;
- allowed branch and title shape;
- PR body evidence requirements;
- changed output summary requirements;
- validation summary requirements;
- human/Codex review gates;
- no-auto-merge rule;
- rejected-baseline handling.

Mapped claim state: a draft baseline PR may route to review. It must not
approve baseline updates, parser truth, fixture truth, or readiness.

## Mythic Edge Consumer Requirements

Before #388 may claim the corpus-loop portion is complete, Mythic Edge must
also have reviewed consumer-side evidence for:

- receiving or verifying a corpus package release reference;
- preserving package refs in public-safe workflow metadata;
- running or consuming a ratchet report through a reviewed command or workflow;
- mapping ratchet output to #558 confidence states without overclaiming;
- rejecting stale, failed, unsafe, or unreviewed releases;
- preserving human review before baseline changes;
- preserving Codex E/F/G routing before committed metadata or baseline changes;
- preserving `parser_behavior_ready=false` unless a separate parser-behavior
  contract proves otherwise.

## Handoff Between Mythic Edge And Mythic-Edge-Corpus

The intended safe handoff is:

```text
Mythic Edge candidate/review/proof/draft/diff metadata
  -> human-approved parser/corpus update workflow
  -> reviewed public-safe corpus package input
  -> Mythic-Edge-Corpus package preview
  -> Mythic-Edge-Corpus PR validation
  -> Mythic-Edge-Corpus reviewed release
  -> bounded dispatch into Mythic Edge
  -> Mythic Edge ratchet comparison
  -> draft baseline PR proposal
  -> Codex E/F/G review and merge path
```

Forbidden shortcut:

```text
metadata diff or corpus automation
  -/-> parser truth
  -/-> fixture promotion approval
  -/-> corpus metadata mutation
  -/-> automatic baseline update
  -/-> #388 completion
  -/-> release or production readiness
```

Generated corpus metadata diffs from Mythic Edge remain proposals until a
human-approved workflow and reviewed PR path accepts them. Mythic-Edge-Corpus
packages remain external corpus artifacts until Mythic Edge consumes them
through a reviewed dispatch/ratchet path.

## What #388 May Claim After All Gates Exist

After all required corpus gates are complete, reviewed, and mapped back to
this contract, #388 may claim only scoped process readiness such as:

- reviewed corpus package preview exists;
- corpus package PR validation exists;
- reviewed corpus release publishing exists;
- bounded dispatch from corpus releases to Mythic Edge exists;
- deterministic ratchet comparison exists for reviewed corpus packages;
- draft baseline PR proposal workflow exists;
- corpus-loop process evidence can be reviewed using #558 confidence states.

Even then, any claim must name the exact release/package/baseline scope and
must preserve the relevant non-claims.

## What #388 Must Still Not Claim

#388 must not claim, from corpus automation alone:

- parser behavior readiness;
- fixture-promotion readiness;
- private smoke success;
- full corpus parity;
- full parser regression parity;
- parser support for every represented scenario;
- automatic corpus metadata approval;
- automatic baseline update approval;
- release readiness;
- deploy readiness;
- production behavior;
- analytics truth;
- AI truth;
- coaching truth;
- security/privacy assurance.

## Failure Behavior

Corpus automation readiness must fail closed.

Required failure statuses:

- Package preview missing:
  `blocked_package_preview_missing`.
- Package validation missing:
  `blocked_package_validation_missing`.
- Package validation failed:
  `blocked_corpus_package_validation_failed`.
- Release publishing missing:
  `blocked_release_publishing_missing`.
- Release publishing failed:
  `blocked_corpus_release_failed`.
- Dispatch missing:
  `blocked_dispatch_bridge_missing`.
- Dispatch failed:
  `blocked_dispatch_failed`.
- Ratchet comparison missing:
  `blocked_ratchet_comparison_missing`.
- Ratchet comparison failed:
  `blocked_ratchet_failed`.
- Corpus release stale:
  `blocked_stale_corpus_release`.
- Baseline proposal missing:
  `blocked_baseline_proposal_missing`.
- Baseline PR rejected:
  `blocked_rejected_baseline_pr`.
- Unreviewed corpus PR:
  `blocked_unreviewed_corpus_pr`.
- Forbidden private/generated/runtime content:
  `blocked_forbidden_content`.
- Any stronger claim without review:
  `blocked_overclaim`.

Failure statuses may route to `coverage_deferred`,
`external_boundary_blocked`, or `coverage_rejected` under the #558 vocabulary.
They must not route to `coverage_confirmed` or readiness claims.

## Allowed Inputs

Allowed for this Codex B pass:

- public GitHub issue and PR metadata for Mythic Edge issues #388, #434, #558,
  #560, and PR #564;
- public GitHub issue metadata for Mythic-Edge-Corpus issues #1 through #6;
- committed Mythic Edge governance docs;
- committed Mythic Edge #388 contracts and implementation handoffs;
- committed validation-tool references.

Allowed for a future gate-report validator, if separately authorized:

- public GitHub issue/PR metadata for the named repos;
- public release metadata for reviewed corpus packages;
- public-safe package preview summaries;
- public-safe PR validation summaries;
- public-safe dispatch payload summaries;
- public-safe ratchet report summaries;
- public-safe draft baseline PR metadata;
- repo-relative refs to committed reports.

## Forbidden Inputs

Forbidden for this contract and any default gate-report validator:

- raw Player.log;
- raw UTC_Log;
- private app-data contents;
- live MTGA data;
- private diagnostics;
- private drift output;
- network, firewall/drop, packet, OS/router, or watcher evidence;
- raw log excerpts;
- exact private local paths;
- raw file hashes;
- screenshots;
- workbook exports;
- SQLite databases;
- credentials, tokens, API keys, webhook URLs, or secrets;
- decklists, card choices, private strategy notes, or player notes;
- external raw corpora;
- Manasight raw logs, compressed logs, parser source, hash lists, byte-size
  lists, capture-date rows, or raw session payloads;
- raw corpus package contents unless a later review path proves they are
  public-safe committed artifacts.

## Side Effects

Allowed side effect in Codex B:

- create this contract file.

Side effects not allowed:

- code implementation;
- private evidence reads;
- local dry-run execution;
- corpus package preview execution;
- package release;
- dispatch send/receive;
- ratchet execution;
- baseline PR creation;
- fixture creation;
- fixture promotion;
- corpus metadata edits;
- issue creation;
- PR creation;
- commits;
- pushes;
- scheduled automation;
- production-facing changes.

## Invariants

- #560 cannot clear until each required corpus gate has a reviewed evidence
  ref.
- Corpus automation cannot approve parser truth.
- Corpus automation cannot approve fixture promotion.
- Corpus automation cannot approve corpus metadata mutation.
- Corpus automation cannot approve baseline updates.
- `coverage_confirmed` remains scoped and requires committed sanitized evidence
  plus reviewed metadata and ratchet evidence for that exact subject.
- Local/private evidence must stay local/private unless a later explicit
  contract and review path produces public-safe derived evidence.
- Dispatch payloads are notifications, not truth.
- Ratchet reports are review evidence, not parser truth.
- Draft baseline PRs are review helpers, not approval.
- Every stronger claim must map to #558 vocabulary and preserve false
  readiness flags.

## Compatibility

This contract preserves existing schema and status vocabulary from:

- `parser_evidence_confidence_claim.v1`;
- `parser_evidence_bounded_local_dry_run.v1`;
- `parser_evidence_corpus_metadata_diff.v1`;
- `parser_evidence_fixture_promotion_proof.v1`;
- `parser_evidence_harvest_review_packet.v1`;
- `parser_evidence_harvest_candidate_summary.v1`;
- `parser_owned_fact_target_matrix.v1`;
- `parser_feature_equity_corpus_ratchet_report.v1`.

Existing report-only, synthetic-only, private-evidence, and external-boundary
states remain in their original confidence classes unless a later reviewed
contract authorizes a transition.

## Validation Requirements

Contract validation for this artifact:

```bash
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' docs/contracts/parser_evidence_corpus_automation_readiness_gate.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_corpus_automation_readiness_gate.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_evidence_corpus_automation_readiness_gate.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

Later Codex C validation, if a gate-report validator is separately
authorized:

```bash
python3 -m pytest -q tests/test_parser_evidence_corpus_automation_readiness_gate.py
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
```

Codex C must also verify that no corpus package execution, release creation,
dispatch event, ratchet execution, baseline PR creation, private evidence
read, fixture promotion, corpus metadata update, parser behavior change, or
readiness claim was introduced.

## Acceptance Criteria

- The contract exists at
  `docs/contracts/parser_evidence_corpus_automation_readiness_gate.md`.
- It lists the required Mythic-Edge-Corpus issue states before #388 may claim
  the corpus-loop portion is complete.
- It records the current #560 gate state as blocked on external corpus repo
  dependencies.
- It defines how Mythic Edge may later verify corpus release, dispatch,
  ratchet, and baseline proposal evidence.
- It preserves human/Codex approval for fixture promotion, corpus metadata
  updates, and baseline changes.
- It maps gate outcomes to #558 confidence vocabulary.
- It defines failure statuses and fail-closed behavior.
- It preserves non-claims and false readiness flags.

## Next Workflow Action

Next role: Codex E for contract review.

Codex C implementation is not the next default role. A later validator may be
useful, but only after review determines the docs-only gate needs
machine-readable enforcement.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #560.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/560

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Dependency issue:
https://github.com/Tahjali11/Mythic-Edge/issues/558

Dependency PR:
https://github.com/Tahjali11/Mythic-Edge/pull/564

Contract artifact:
docs/contracts/parser_evidence_corpus_automation_readiness_gate.md

Review goal:
Review the corpus automation readiness gate contract. Confirm it correctly
keeps #560 blocked on external Mythic-Edge-Corpus issues #1 through #6,
maps future package/validation/release/dispatch/ratchet/baseline evidence to
#558 confidence states, preserves human/Codex approval for fixture promotion,
corpus metadata updates, and baseline changes, and avoids claims of parser
behavior readiness, pipeline activation readiness, private harvest
authorization, fixture-promotion authorization, release readiness, production
behavior, analytics truth, AI truth, or coaching truth.

Validation:
- python3 tools/check_agent_docs.py
- git diff --check
- printf '%s\n' docs/contracts/parser_evidence_corpus_automation_readiness_gate.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
- printf '%s\n' docs/contracts/parser_evidence_corpus_automation_readiness_gate.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
- printf '%s\n' docs/contracts/parser_evidence_corpus_automation_readiness_gate.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin

Expected output:
- Findings first, if any.
- Contract verdict.
- Validation reviewed or run.
- Remaining risks and non-claims.
- Recommended next role.
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/560"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  dependency_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/558"
  dependency_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/564"
  completed_thread: "B"
  next_thread: "E"
  verdict: "corpus_automation_readiness_gate_contract_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/parser-evidence-corpus-automation-readiness-560"
  target_artifact: "docs/contracts/parser_evidence_corpus_automation_readiness_gate.md"
  selected_status: "blocked_external_corpus_repo_pending"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  dry_run_execution_authorized: false
  implementation_authorized: false
  corpus_automation_readiness_gate_cleared: false
  validation:
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "printf '%s\\n' docs/contracts/parser_evidence_corpus_automation_readiness_gate.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_evidence_corpus_automation_readiness_gate.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/parser_evidence_corpus_automation_readiness_gate.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin"
  stop_conditions:
    - "Do not duplicate Mythic-Edge-Corpus automation in Mythic Edge."
    - "Do not claim the complete Manasight-like loop until package, validation, release, dispatch, ratchet, and baseline proposal gates are reviewed."
    - "Do not let corpus automation approve parser truth."
    - "Do not let corpus automation approve fixture promotion."
    - "Do not let corpus automation approve corpus metadata mutation or baseline updates."
    - "Do not run private Player.log or UTC_Log files."
    - "Do not promote fixtures or update corpus metadata."
    - "Do not claim parser_behavior_ready, pipeline activation readiness, release readiness, production behavior, analytics truth, AI truth, coaching truth, or full corpus parity."
```
