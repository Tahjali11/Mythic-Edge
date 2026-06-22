# ARS Refactor Constitution Learning Cycle Contract

## Module

`ars_refactor_constitution_learning_cycle`

Plain English: this contract defines a pre-execution governance lifecycle for
using Adversarial Review Scout, Refactor Scout, and Codex H constitutional
review as one controlled learning cycle across the Mythic Edge project.

This contract is planning only. It does not run Adversarial Review Scout, run
Refactor Scout, tag baselines, remediate findings, refactor code, mutate
sibling repositories, edit constitution files, create an ADR, open a PR, or
claim readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue / tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/551
- Target artifact:
  `docs/contracts/ars_refactor_constitution_learning_cycle.md`
- Base branch: `main`
- Target branch: `main`
- Latest verified commit:
  `39248f5d9245d8f0f44bd3e5aabef3c84ade1d36`
- Risk tier: High

Issue #551 is the governance tracker for this cycle. There is no separate
parent tracker for this contract.

## Related Repositories

The cycle may eventually involve these repositories:

- `Tahjali11/Mythic-Edge`
- `Tahjali11/Mythic-Edge-Automation-Artifacts`
- `Tahjali11/Mythic-Edge-Analytics`

This contract lives in `Tahjali11/Mythic-Edge` and does not authorize mutation
of either sibling repository. Later child lanes must carry their own
repo-scoped handoffs and explicit allowed read-only or write authority.

## Source Artifacts Inspected

- GitHub issue #551
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/templates/problem_representation.md`
- `docs/templates/workflow_handoff.md`
- `docs/internal_project_map.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`
- `docs/contracts/repo_wip_1_lane_activation_policy.md`
- `docs/contracts/codex_h_post_adoption_governance_refinements.md`
- `docs/contracts/refactor_scout_rs_7d23c73034_select_validation_focused_mapping_table.md`
- `docs/contracts/repo_extraction_candidate_matrix.md`
- `docs/contracts/parser_owned_fact_capture_tracker.md`

Sibling repositories were not inspected or mutated during this Codex B pass.

## Current Authorization Facts

These flags are false for this contract and must remain false until a later
child issue, contract, review path, and explicit user approval change them:

```yaml
execution_authorized: false
baseline_tagging_authorized: false
ars_execution_authorized: false
refactor_scout_execution_authorized: false
remediation_authorized: false
refactoring_authorized: false
constitutional_amendment_authorized: false
sibling_repo_mutation_authorized: false
source_repo_action_authorized: false
release_readiness_authorized: false
deploy_readiness_authorized: false
production_readiness_authorized: false
```

## Observed Current Behavior

The Mythic Edge source repository already has governance for:

- protected surfaces and schema-change authorization;
- external integration and collaboration surfaces;
- repository boundary strategy;
- proposed WIP-1 lane activation;
- Codex H advisory constitutional synthesis;
- Refactor Scout candidate handoff from non-authoritative artifact context to
  source-repo contracts;
- repo extraction candidate planning;
- parser-owned fact capture tracking.

Issue #551 now asks for a higher-level governed learning cycle that connects
three advisory systems:

```text
baseline snapshot
  -> Adversarial Review Scout full sweep
  -> modeled finding remediation / triage
  -> Refactor Scout candidate discovery
  -> one-at-a-time governed refactor workflow
  -> post-refactor Adversarial Review Scout verification
  -> before/after comparison
  -> Codex H constitutional synthesis
  -> proposed amendments and ADR candidate
```

The target contract did not exist before this Codex B pass.

The primary local checkout had unrelated local work, so this contract was
written in a clean `main` worktree at the verified commit. No unrelated files
were edited.

## Problem Statement

Mythic Edge now has enough advisory automation and governance maturity that
running tools one at a time is less valuable than using them in a deliberate
learning cycle. The project needs a contract that says what order the cycle
uses, which gates must be satisfied before each execution step, how artifacts
are stored, how findings are interpreted, and what the final constitutional
review may propose.

Without a contract, later work could accidentally treat a planning tracker as
permission to run tools, treat advisory findings as source truth, treat a clean
ARS pass as security assurance, treat a Refactor Scout candidate as
implementation authority, run multiple source-refactor lanes in parallel, or
let Codex H rewrite authority docs directly.

## First Bad Value

The first bad value is any issue, contract, handoff, report, run artifact,
claim file, refactor candidate, review finding, PR body, tracker update, or
constitutional packet that implies one of these without a later explicit child
lane:

- baseline tags may be created;
- ARS may run;
- Refactor Scout may run;
- source repositories may be mutated;
- remediation may begin;
- refactoring may begin;
- a Refactor Scout candidate is implementation authority;
- an ARS result is source truth;
- a clean sweep proves security or privacy assurance;
- Codex H output directly edits governance docs;
- release readiness, deploy readiness, production readiness, parser truth,
  analytics truth, AI truth, or coaching truth is established.

## Scope Decision

This contract approves only a lifecycle and child-lane gate definition.

In scope:

- lifecycle shape;
- WIP-1 exception compatibility;
- child lane sequence;
- baseline snapshot model;
- generated artifact layout;
- ARS sweep gates;
- finding status vocabulary;
- Refactor Scout advisory boundary;
- one-at-a-time refactor promotion rules;
- post-refactor ARS verification gate;
- before/after comparison requirements;
- Codex H synthesis requirements;
- stop conditions;
- validation expectations for later child lanes.

Out of scope:

- creating Git tags;
- writing baseline snapshot artifacts;
- running ARS;
- running Refactor Scout;
- running private or live checks;
- creating remediation issues;
- fixing findings;
- changing source code;
- refactoring code;
- mutating sibling repositories;
- opening PRs;
- editing constitution, workflow docs, or ADR files;
- creating the future ADR candidate;
- changing parser, runtime, workbook, webhook, Apps Script, analytics, AI,
  release, deploy, or production behavior.

## Owning Layer

Repository coordination and agent workflow governance.

## Internal Project Area

Primary area: Quality / Governance.

Adjacent read-only context areas:

- External / Collaboration Surface, because GitHub issues, PRs, ARS reports,
  Refactor Scout artifacts, and Codex H packets are collaboration and evidence
  surfaces.
- Generated / Local Artifacts, because future run outputs and snapshot bundles
  are generated evidence, not source truth.
- Shared Support, because the cycle may inspect all internal project areas
  without owning their runtime behavior.

## Truth Owner

This contract owns only governance sequencing and artifact semantics.

Truth ownership remains unchanged:

- Parser/state owns parser-managed facts.
- Analytics owns only separately contracted deterministic analytics behavior.
- Automation Artifacts owns generated advisory automation artifacts.
- Codex H output is advisory synthesis and proposed governance change, not
  accepted authority by itself.
- ARS findings are modeled advisory evidence, not source truth or security
  assurance.
- Refactor Scout candidates are advisory decomposition opportunities, not
  implementation authority.

## Bridge-Code Status

`shared_support`

This is governance support across repositories and tools. It does not bridge
runtime product data and does not authorize downstream-to-upstream truth flow.

Allowed information flow:

```text
repo refs, issue/PR metadata, advisory findings, candidate metadata,
reviewed remediation evidence, validation evidence
  -> cycle reports and governance synthesis
  -> proposed follow-up issues, amendments, and ADR candidate
```

Forbidden reverse flow:

```text
cycle report or advisory artifact
  -/-> parser truth
  -/-> analytics truth
  -/-> source mutation authority
  -/-> remediation authority
  -/-> refactor authority
  -/-> release/deploy/production readiness
  -/-> accepted constitution or ADR change
```

## WIP-1 Exception Compatibility

The user and issue #551 name this cycle as:

```yaml
wip_exception: "security_refactor_constitution_cycle"
```

Current repo governance and proposed ADR-0008 list canonical exception names
that do not include `security_refactor_constitution_cycle`. To preserve both
the user-supplied label and WIP-1 compatibility, future public handoffs should
record:

```yaml
lane_activation:
  repo: "Tahjali11/Mythic-Edge"
  active_issue_or_lane: "https://github.com/Tahjali11/Mythic-Edge/issues/551"
  lane_status: "active"
  exception:
    name: "explicit_user_override"
    blocked_active_issue_or_pr: ""
    reason: "Governed cross-repo ARS, refactor, and constitutional learning cycle."
    allowed_scope: "Issue #551 and explicitly created child lanes only; source changes remain one-at-a-time through the owning repo workflow."
    expiration_condition: "Final cycle report, proposed constitutional amendments, and ADR candidate are produced, or issue #551 is explicitly parked or closed."
    authorized_by: "Current user handoff and GitHub issue #551"
    recorded_in: "docs/contracts/ars_refactor_constitution_learning_cycle.md"
  cycle_identifier: "security_refactor_constitution_cycle"
```

`security_refactor_constitution_cycle` is the cycle identifier for this issue.
It must not be treated as a new canonical WIP-1 exception name unless a later
governance issue and ADR path accepts that policy change.

## Files Owned By This Contract

This Codex B pass owns:

- `docs/contracts/ars_refactor_constitution_learning_cycle.md`

This contract does not own source code, tests, ARS implementation files,
Refactor Scout implementation files, sibling repository files, issue comments,
PRs, tags, runtime artifacts, generated run artifacts, constitution files,
workflow docs, or ADR files.

Expected later artifacts, each requiring its own child lane:

- baseline snapshot contract;
- baseline snapshot bundle in the Automation Artifacts repository;
- ARS full-sweep authorization contract or run packet;
- ARS finding remediation tracker or issue set;
- Refactor Scout run contract or claim packet;
- one-at-a-time refactor candidate source-repo contracts;
- post-refactor ARS verification packet;
- before/after comparison report;
- Codex H constitution feedback packet;
- proposed ADR candidate.

## Public Interface

This contract defines the lifecycle vocabulary and gates that future child
issues must use. It does not define a runtime API.

### Cycle Status Vocabulary

Allowed cycle-level statuses:

- `contract_only`: lifecycle is defined but no execution has begun.
- `baseline_planned`: a baseline snapshot child lane exists.
- `baseline_recorded`: baseline refs and snapshot bundle are complete.
- `ars_sweep_planned`: ARS sweep authorization child exists.
- `ars_sweep_complete`: ARS sweep artifacts exist and preserve non-claims.
- `findings_in_remediation`: findings are being handled through scoped lanes.
- `findings_resolved_or_triaged`: blocking/advisory findings are resolved or
  watch-listed with links.
- `refactor_scout_planned`: Refactor Scout run child exists.
- `refactor_candidates_recorded`: candidate discovery is complete.
- `refactor_in_progress`: exactly one candidate is active in an owning repo.
- `post_refactor_verification_planned`: post-refactor ARS verification child
  exists.
- `post_refactor_verification_complete`: post-refactor verification artifacts
  exist.
- `comparison_ready`: before/after comparison is complete.
- `codex_h_ready`: Codex H has enough evidence to synthesize.
- `constitutional_synthesis_complete`: Codex H output exists.
- `cycle_complete`: final cycle report, amendment proposals, and ADR candidate
  exist, with non-claims preserved.
- `parked`: issue #551 is intentionally paused.
- `blocked`: a prerequisite or authority gap prevents progress.

### Child Lane Status Vocabulary

Allowed child-lane statuses:

- `not_started`
- `planned`
- `authorized_for_contract`
- `authorized_for_execution`
- `blocked_authority_gap`
- `blocked_prerequisite_missing`
- `in_progress`
- `review_required`
- `complete`
- `parked`
- `cancelled`

### Finding Status Vocabulary

Allowed ARS finding statuses:

- `blocking_deterministic`
- `advisory`
- `watch_list`
- `false_positive_accepted`
- `expected_probe_behavior`
- `remediated`
- `triaged_to_issue`
- `deferred_with_reason`
- `blocked_needs_human_decision`

No finding status may claim security assurance, privacy assurance, or complete
absence of defects.

### Refactor Candidate Status Vocabulary

Allowed Refactor Scout candidate statuses:

- `candidate_recorded`
- `candidate_rejected`
- `candidate_watch_list`
- `candidate_selected_one_at_a_time`
- `source_contract_required`
- `source_contract_ready`
- `implementation_in_review`
- `merged_behavior_preserving`
- `post_refactor_verification_required`
- `post_refactor_verification_complete`

No candidate status may authorize source mutation by itself.

## Inputs

Allowed inputs for future child lanes:

- repo names and public repository URLs;
- branch names, commit refs, and optional approved tag names;
- clean/dirty status summaries;
- public issue, PR, review, and merge metadata;
- current governance docs and accepted/proposed ADRs;
- ARS registry, contracts, claim files, run manifests, probe summaries, and
  finding summaries from the Automation Artifacts repository;
- Refactor Scout registry, candidates, claims, and run summaries from the
  Automation Artifacts repository;
- owning-repo contracts, implementation handoffs, review reports, validation
  summaries, PR links, and merge commits;
- Codex H feedback packets and before/after comparison artifacts;
- public-safe module inventory and size/complexity metrics.

Forbidden inputs unless a later explicit child lane allows a narrower form:

- raw Player.log or UTC_Log content;
- private app-data;
- private logs;
- local absolute paths in public artifacts;
- secrets, credentials, tokens, API keys, webhook URLs, OAuth material, or
  environment values;
- generated private artifacts;
- local runtime status files;
- workbook exports;
- raw external-provider payloads;
- screenshots containing private data;
- source patches generated by ARS or Refactor Scout without source-repo
  contract authority;
- any data that a sibling repository contract forbids.

## Outputs

Allowed future cycle outputs:

- source-repo child issues;
- source-repo contracts;
- source-repo implementation handoffs;
- source-repo reviews or contract-test reports;
- draft PRs through the owning repository workflow;
- Automation Artifacts snapshot and run bundles;
- before/after comparison report;
- Codex H constitutional synthesis packet;
- proposed amendments;
- proposed ADR candidate.

Forbidden outputs in this Codex B pass:

- tags;
- ARS run artifacts;
- Refactor Scout run artifacts;
- source-code changes;
- remediation commits;
- refactor commits;
- constitution edits;
- ADR files;
- PRs;
- sibling-repo edits;
- runtime/generated/private artifacts.

## Lifecycle And Gates

### 0. Governance Contract

Current lane: issue #551 and this contract.

Allowed:

- define lifecycle;
- define gates;
- define stop conditions;
- route next child lane.

Forbidden:

- execute the cycle.

Exit criteria:

- this contract exists;
- validation is recorded;
- next role is Codex E for contract review or Codex A for the first child
  problem representation.

### 1. Baseline Snapshot Planning

Goal: define the exact baseline snapshot packet before any tags or generated
bundles are created.

Required contract decisions:

- repos included;
- branch/ref per repo;
- whether tags are allowed;
- tag naming pattern if allowed;
- snapshot bundle path in Automation Artifacts;
- public-safe metadata schema;
- private/local artifact exclusions;
- dirty worktree reporting rules;
- validation commands;
- stop behavior on mismatched remotes or dirty state.

This child may not run ARS or Refactor Scout.

### 2. Baseline Snapshot Execution

Goal: capture commit refs and a public-safe before snapshot.

Allowed only after explicit user approval and a baseline execution contract.

This child may create approved tags only if the baseline contract authorizes
tagging and names the exact repositories and tag pattern.

### 3. ARS Full-Sweep Authorization

Goal: authorize the first full ARS sweep only after ARS module-sweep
prerequisites are complete enough for the requested repos/modules.

Required checks:

- ARS bundle registry and module-sweep status;
- scheduled/manual/repo-aware execution authority;
- source-repo read-only or write authority;
- claim key format;
- output artifact path;
- forbidden input scan;
- non-claims.

This child may not claim security assurance or privacy assurance.

### 4. ARS Finding Remediation / Triage

Goal: handle modeled findings without letting the automation own source truth.

Required flow:

1. Classify findings as blocking deterministic, advisory, watch-list,
   expected probe behavior, false positive accepted, or human-decision-needed.
2. For each source-repo change, create or route to an owning repo issue.
3. Write a contract before implementation.
4. Use the normal A-G workflow in the owning repo.
5. Record validation and merge evidence.

Watch-list findings may become issues. They must not be silently treated as
resolved.

### 5. Refactor Scout Discovery

Goal: discover behavior-preserving decomposition candidates after ARS findings
are resolved or triaged.

Required gates:

- baseline snapshot complete;
- ARS sweep complete;
- blocking deterministic findings remediated or explicitly parked by the user;
- advisory findings remediated, accepted as expected behavior, or triaged;
- Refactor Scout claim/cooldown/duplicate rules checked on fetched
  `origin/main` of the artifact repository;
- source repos remain read-only unless a later owning-repo issue authorizes
  mutation.

Refactor Scout outputs remain advisory.

### 6. One-At-A-Time Refactor Candidate Workflow

Goal: move at most one selected candidate at a time through the owning repo's
normal workflow.

Required gates:

- candidate selected by human or contract-authorized process;
- owning repository issue exists;
- source-repo contract defines behavior-preservation proof;
- implementation is reviewed before submitter work;
- PR targets the approved branch;
- merge requires Codex G and explicit user approval where policy requires it.

No module is categorically off-limits for evaluation, but every refactor needs
a scoped contract and validation plan.

### 7. Post-Refactor ARS Verification

Goal: rerun ARS against affected modules or all modules after refactoring.

Required gates:

- refactor PR merged or parked;
- source branch and merge commit recorded;
- verification scope defined;
- expected findings and non-claims listed;
- no source mutation by verification unless a later contract authorizes it.

Verification can say modeled findings were resolved or unchanged. It cannot
say the repository is secure or production-ready.

### 8. Before/After Comparison

Goal: compare the baseline and final state.

Required sections:

- repo refs before and after;
- ARS finding summary before and after;
- privacy/protected-surface risk summary;
- Refactor Scout candidate and selected candidate summary;
- source changes and PR links;
- validation evidence;
- tests added or changed;
- complexity or size deltas where available;
- workflow failures, false starts, and rework;
- unresolved risks;
- non-claims.

### 9. Codex H Constitutional Synthesis

Goal: turn the cycle evidence into proposed governance improvements.

Required inputs:

- baseline snapshot;
- ARS sweep and remediation evidence;
- Refactor Scout run evidence;
- refactor candidate workflow evidence;
- post-refactor ARS verification;
- before/after comparison;
- current governance docs and ADRs.

Codex H must:

- produce a source coverage table;
- classify recommendations against current repo state;
- identify satisfied, stale, superseded, active, conflicting, and watch-list
  recommendations;
- propose amendments only as recommendations;
- propose an ADR candidate only as a draft follow-up;
- route implementation through A/B/C/E/F/G.

Codex H must not directly rewrite authority docs.

### 10. Final Cycle Report

Goal: close the learning loop without overclaiming.

Allowed completion claim:

```text
The project completed a governed ARS/refactor/constitutional learning cycle,
resolved or triaged modeled findings, and produced proposed workflow
improvements based on evidence.
```

Forbidden completion claims:

- security assurance;
- privacy assurance;
- release readiness;
- deploy readiness;
- production readiness;
- parser truth;
- analytics truth;
- AI truth;
- coaching truth;
- complete absence of vulnerabilities;
- proof that automated tools found every issue.

## Artifact Layout

Generated cycle artifacts should live in the Automation Artifacts repository
by default, under a path like:

```text
automations/governance-cycles/ars-refactor-constitution-YYYY-MM-DD/
  baseline_snapshot/
  ars_full_sweep/
  finding_remediation/
  refactor_scout_selection/
  refactor_workflow_results/
  post_refactor_ars_verification/
  before_after_comparison.md
  constitution_feedback_packet.md
  proposed_adr.md
  final_cycle_report.md
```

This contract does not create that directory. A later Automation Artifacts
child lane must authorize any generated artifact writes.

Source repositories should receive only:

- repo-scoped issues;
- repo-scoped contracts;
- normal implementation handoffs, review reports, and PRs;
- approved tags or refs only when a baseline contract authorizes them.

## Snapshot Model

The preferred snapshot uses both Git refs and a public-safe snapshot bundle.

Git refs provide reproducibility. The bundle provides human-readable context.

Each repo snapshot should include:

- repository name;
- repository URL;
- branch/ref;
- commit hash;
- clean/dirty status summary;
- active issue/lane;
- open PRs relevant to the cycle;
- ARS readiness state;
- Refactor Scout readiness state;
- module inventory summary;
- validation evidence available at baseline;
- governance docs and ADR refs;
- false readiness and non-authorization flags.

Snapshot bundles must not include raw logs, private data, local absolute paths,
secrets, raw diffs containing private content, generated runtime artifacts, or
source patches unless separately authorized.

## Stop Conditions

Stop and route back to Codex A or the user if any lane attempts to:

- create tags before a baseline tagging contract and explicit approval;
- run ARS before ARS prerequisites and explicit approval;
- run Refactor Scout before baseline and ARS remediation gates;
- mutate a sibling repository without repo-scoped authorization;
- treat ARS findings as source truth;
- treat Refactor Scout candidates as implementation authority;
- start more than one refactor candidate at a time;
- bypass the owning repo's A-G workflow;
- skip Codex E review for implementation work;
- skip Codex F/G boundaries for PR submission or merge;
- edit constitution, workflow docs, or ADRs before Codex H synthesis and
  normal workflow authorization;
- commit secrets, local/private data, raw logs, generated private artifacts,
  runtime artifacts, workbook exports, or local-only files;
- claim security assurance, privacy assurance, release readiness, deploy
  readiness, production readiness, parser truth, analytics truth, AI truth,
  coaching truth, or complete vulnerability coverage.

## Protected Surfaces

This contract explicitly does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match identity;
- game identity;
- deduplication;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- runtime status schema;
- diagnostics report shape;
- analytics behavior;
- local app behavior;
- OpenAI or model-provider behavior;
- AI/coaching behavior;
- CI gates;
- release policy;
- deploy policy;
- production behavior;
- secrets or credential policy;
- raw/private/generated artifacts.

## Validation Requirements

Codex B validation for this contract:

```bash
git diff --check
printf '%s\n' docs/contracts/ars_refactor_constitution_learning_cycle.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_agent_docs.py
```

Later child lanes should add validation appropriate to the child. Examples:

- baseline child: remote normalization, clean/dirty status capture, JSON or
  Markdown artifact checks, forbidden-content scans;
- ARS child: ARS registry and claim validation, run-manifest validation,
  forbidden-content scan, non-claim scan;
- remediation child: focused tests for the owning repo plus protected-surface
  and secret scans;
- Refactor Scout child: registry/claim validation and duplicate/cooldown
  checks;
- refactor child: behavior-preservation tests and before/after comparison;
- Codex H child: source coverage table and current-state classification.

## Acceptance Criteria

- This contract exists at
  `docs/contracts/ars_refactor_constitution_learning_cycle.md`.
- It cites issue #551 and repo governance authority.
- It keeps all execution and mutation authorization flags false.
- It defines the lifecycle stages and gates.
- It records WIP-1 compatibility using `explicit_user_override` plus the
  `security_refactor_constitution_cycle` cycle identifier.
- It defines artifact layout without creating artifacts.
- It defines ARS and Refactor Scout as advisory.
- It preserves one-at-a-time refactor promotion.
- It preserves Codex H as advisory synthesis.
- It includes validation expectations and a handoff.

## Open Questions

- Whether a future ADR should accept `security_refactor_constitution_cycle` as
  a canonical WIP-1 exception name or keep it as a cycle identifier under
  `explicit_user_override`.
- Whether baseline snapshot tags should be lightweight tags, annotated tags, or
  commit refs only. This contract does not decide or authorize tagging.
- Whether ARS first runs affected modules only or all modules across all three
  repos. Issue #551 prefers full sweep, but a later ARS authorization contract
  must verify current ARS readiness.
- Whether Refactor Scout should run once across all repos or one repo at a
  time. A later Refactor Scout child must decide based on artifact-repo claim
  and cooldown rules.

## Next Workflow Action

Recommended next role: Codex E for contract review, or Codex A if the user
wants to create the first baseline-snapshot child issue before review.

Recommended next child after review: Codex A problem representation for the
baseline snapshot planning lane.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #551.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/551

Contract:
docs/contracts/ars_refactor_constitution_learning_cycle.md

Base branch:
main

Goal:
Review the ARS/refactor/constitution learning cycle contract for scope,
WIP-1 compatibility, child-lane gates, protected-surface boundaries,
non-claims, and validation expectations.

Do not implement code.
Do not run ARS.
Do not run Refactor Scout.
Do not create tags.
Do not mutate sibling repositories.
Do not edit constitution, workflow docs, or ADR files.
Do not claim security assurance, privacy assurance, release readiness, deploy
readiness, production readiness, parser truth, analytics truth, AI truth, or
coaching truth.

Expected output:
- findings first, if any;
- contract-test report or review summary;
- validation evidence;
- recommended next role;
- workflow_handoff block.
```

Pasteable Codex A prompt for the first child lane:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex A: Thinker for the first child issue under #551.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/551

Source contract:
docs/contracts/ars_refactor_constitution_learning_cycle.md

Goal:
Create the problem representation for the baseline snapshot planning lane.
This lane should define how to capture public-safe before-state metadata for
Tahjali11/Mythic-Edge, Tahjali11/Mythic-Edge-Automation-Artifacts, and
Tahjali11/Mythic-Edge-Analytics without creating tags, writing generated
snapshot bundles, running ARS, running Refactor Scout, remediating findings,
refactoring code, mutating sibling repositories, or editing constitution/ADR
files in Codex A.

Required decisions:
- whether baseline execution should use commit refs only or propose tags for a
  later approval-gated child;
- repo/ref metadata shape;
- public-safe snapshot bundle shape;
- Automation Artifacts output path proposal;
- forbidden local/private/generated inputs;
- validation evidence needed for Codex B;
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/551"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/551"
  completed_thread: "B"
  next_thread: "E_or_A"
  source_artifact: "GitHub issue #551"
  target_artifact: "docs/contracts/ars_refactor_constitution_learning_cycle.md"
  verdict: "pre_execution_governance_contract_ready"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  latest_verified_commit: "39248f5d9245d8f0f44bd3e5aabef3c84ade1d36"
  internal_project_area: "Quality / Governance"
  truth_owner: "repository coordination and agent workflow governance"
  bridge_code_status: "shared_support"
  lane_activation:
    repo: "Tahjali11/Mythic-Edge"
    active_issue_or_lane: "https://github.com/Tahjali11/Mythic-Edge/issues/551"
    lane_status: "active"
    exception:
      name: "explicit_user_override"
      blocked_active_issue_or_pr: ""
      reason: "Governed cross-repo ARS, refactor, and constitutional learning cycle."
      allowed_scope: "Issue #551 and explicitly created child lanes only; source changes remain one-at-a-time through the owning repo workflow."
      expiration_condition: "Final cycle report, proposed constitutional amendments, and ADR candidate are produced, or issue #551 is explicitly parked or closed."
      authorized_by: "Current user handoff and GitHub issue #551"
      recorded_in: "docs/contracts/ars_refactor_constitution_learning_cycle.md"
    cycle_identifier: "security_refactor_constitution_cycle"
  allowed_read_only_references:
    - repository: "Tahjali11/Mythic-Edge-Automation-Artifacts"
      repository_url: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts"
      purpose: "future child lanes may inspect advisory artifact provenance only when explicitly scoped"
    - repository: "Tahjali11/Mythic-Edge-Analytics"
      repository_url: "https://github.com/Tahjali11/Mythic-Edge-Analytics"
      purpose: "future child lanes may inspect analytics repo metadata only when explicitly scoped"
  execution_authorized: false
  baseline_tagging_authorized: false
  ars_execution_authorized: false
  refactor_scout_execution_authorized: false
  remediation_authorized: false
  refactoring_authorized: false
  constitutional_amendment_authorized: false
  validation:
    - "git diff --check"
    - "printf '%s\\n' docs/contracts/ars_refactor_constitution_learning_cycle.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "python3 tools/check_agent_docs.py"
  stop_conditions:
    - "Do not create tags."
    - "Do not run ARS."
    - "Do not run Refactor Scout."
    - "Do not start remediation or refactoring."
    - "Do not mutate sibling repositories."
    - "Do not edit constitution, workflow docs, or ADR files."
    - "Do not claim security assurance, privacy assurance, release readiness, deploy readiness, production readiness, parser truth, analytics truth, AI truth, coaching truth, or complete vulnerability coverage."
```
