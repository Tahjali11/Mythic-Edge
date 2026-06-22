# Parser Recovery Human-Approved Parser/Corpus Update Workflow Contract

## Module

Human-approved parser/corpus update workflow for parser recovery planning.

Plain English: this contract defines how Mythic Edge may later move from
review-only recovery draft metadata into a scoped parser or corpus update
lane. A human approval record may select one recovery candidate and one
allowed action type for the next A-G workflow step. It must not itself change
parser behavior, create fixtures, edit corpus metadata, run private harvest,
create GitHub issues or PRs, open branches, write files beyond the authorized
contract artifact, or activate #388 or #381.

This Codex B pass writes only this contract. It does not implement code, open
a PR, create issues, create branches, create commits, run private checks,
write recovery artifacts, edit corpus metadata, change parser behavior, or
claim parser recovery.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/456
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/455
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/547
- Previous merge commit: `e705558aac679fe101856d0f973211fdf5ce34e7`
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed during this Codex B pass:

- The primary checkout was on a deleted #455 branch with an unrelated modified
  `docs/project_roadmap.md` edit.
- To preserve unrelated local work, this contract was written in a clean
  sibling worktree:
  `codex/parser-recovery-human-approved-update-workflow-456`.
- The clean worktree was created from `origin/main`.
- `HEAD` was `e705558aac679fe101856d0f973211fdf5ce34e7`.
- The requested previous merge commit
  `e705558aac679fe101856d0f973211fdf5ce34e7` was present.
- Issue #456 was open.
- Pipeline tracker #388 was open and inactive.
- Parent private-evidence issue #434 was open.
- Previous issue #455 was closed.
- PR #547 was merged into `main`.
- The target contract did not exist before this pass.

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- Issue #456 and Codex A reconciliation comment
- Pipeline tracker #388
- Parent private-evidence issue #434
- Issue #455 and PR #547
- `docs/contracts/parser_recovery_issue_fixture_draft_generator.md`
- `docs/implementation_handoffs/parser_recovery_issue_fixture_draft_generator_comparison.md`
- `src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py`
- `docs/contracts/parser_recovery_candidate_packet_generator.md`
- `docs/contracts/parser_recovery_field_evidence_comparison_report.md`
- `docs/contracts/parser_recovery_field_recovery_matrix.md`
- `docs/contracts/parser_recovery_local_watcher_offset_window_monitor.md`
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`
- Relevant #381 through #387 contracts as workflow context only

No private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop,
packet, OS/router, diagnostics, drift, watcher, tailer, private smoke, or
private harvest evidence was run, tailed, hashed, copied, summarized, or read.

## Observed Current Behavior

The #388 recovery planning lane now has a staged, public-safe chain:

1. #451 Field Recovery Matrix
   - classifies parser-owned fields and recovery categories.
2. #452 local watcher / offset-window monitor
   - models synthetic/source-window metadata boundaries without private reads.
3. #453 field-evidence comparison report
   - compares expected evidence with reduced public-safe current evidence.
4. #454 recovery candidate packet generator
   - creates in-memory public-safe recovery candidate packets.
5. #455 issue/fixture/manifest draft generator
   - creates in-memory review-only issue, fixture summary, manifest summary,
     and checklist draft metadata.

The #455 implementation preserves:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
file_writing_authorized: false
implementation_authorized: false
issue_creation_authorized: false
pr_creation_authorized: false
```

The draft generator is intentionally in-memory and review-only. It does not
write issue draft files, fixture files, manifest files, corpus metadata, PR
assist artifacts, local artifacts, or GitHub issues/PRs. It does not change
parser behavior or activate #388/#381.

No workflow contract currently defines what a human approval record must
contain before a reviewer may route one generated draft/candidate into a
future parser/corpus update lane.

## Problem

The recovery chain can now produce review-only draft metadata. The next risk
is mistaking that metadata for permission to act.

Without a human-approved parser/corpus update workflow contract, a future
thread could accidentally:

- treat a generated issue draft as permission to create a GitHub issue;
- treat a fixture summary as permission to create or promote a fixture;
- treat a manifest summary as permission to edit golden replay manifests;
- treat a candidate packet as parser behavior authority;
- treat private-gated or external-gated candidates as ready for action;
- flip readiness or authorization flags through wording instead of workflow;
- use `Closes` or similar lifecycle text in a planning-only issue or PR;
- bypass Codex A/B/C/E/F/G role boundaries;
- create parser changes, corpus metadata changes, branches, commits, PRs, or
  tracker updates without a scoped issue, contract, validation, review, and
  explicit user/deployer approval.

The first bad value is any approval field, workflow status, generated draft,
review checklist, issue text, fixture summary, manifest summary, handoff, or
next-role prompt that moves parser behavior, fixture creation, corpus
metadata, private harvest, GitHub issue/PR lifecycle, or readiness flags
forward without explicit human approval plus the owning repo's scoped A-G
workflow.

## Scope Decision

This contract defines a planning-only human approval and role-routing
workflow.

It authorizes no code implementation by itself. If the user later explicitly
authorizes Codex C, a future implementation may add a deterministic,
side-effect-free validator for human approval metadata and route decisions.
That future helper must remain in-memory and must not create files, issues,
PRs, branches, commits, fixtures, manifests, corpus edits, or parser changes.

This contract authorizes the following workflow concept:

1. A #455 draft remains review-only.
2. A human selects exactly one recovery candidate and one action type.
3. The approval record names allowed scope and expiration.
4. Codex A frames a new problem representation if the action needs a new
   parser/corpus update lane.
5. Codex B writes an update-specific contract.
6. Codex C implements only the scoped change after that contract explicitly
   authorizes implementation.
7. Codex E reviews against the contract.
8. Codex F submits a draft PR only after review.
9. Codex G merges/closes/updates trackers only after explicit deployer
   approval and merge gates.

This contract does not authorize:

- code implementation in Codex B;
- private source discovery;
- private source reads;
- exact private offset, size, timestamp, path, hash, or payload collection;
- watcher startup;
- tailer startup;
- diagnostics or drift execution;
- local or committed artifact writing beyond this contract;
- GitHub issue creation;
- GitHub PR creation;
- branch creation, staging, commits, pushes, PR comments, issue comments, or
  tracker updates;
- fixture creation or promotion;
- golden replay manifest writing;
- corpus manifest/session-ledger edits;
- parser behavior changes;
- parser event changes;
- router changes;
- parser state final reconciliation changes;
- match/game identity or deduplication changes;
- workbook/webhook/App Script changes;
- analytics, AI, or coaching changes;
- #388 or #381 activation;
- `parser_behavior_ready=true`;
- `pipeline_activation_ready_for_issue_388=true`;
- `file_writing_authorized=true`;
- `private_harvest_authorized=true`;
- `fixture_promotion_authorized=true`;
- `corpus_status_change_authorized=true`;
- `issue_creation_authorized=true`;
- `pr_creation_authorized=true`.

## Owning Layer

Primary owner: Quality / Governance.

Supporting owner: Corpus / Provenance.

Quality / Governance owns:

- human approval metadata;
- allowed action-type vocabulary;
- role routing;
- lifecycle wording;
- stop conditions;
- protected-surface checks;
- privacy/secret checks;
- issue/PR lifecycle non-claims;
- false readiness and authorization flags.

Corpus / Provenance owns:

- recovery candidate identity vocabulary;
- fixture/corpus promotion vocabulary;
- fixture/manifest review prerequisites;
- corpus metadata movement gates;
- evidence traceability.

Parser remains the only owner of parser facts, parser behavior, parser events,
router semantics, parser state final reconciliation, match/game identity,
deduplication, and parser-owned output values.

## Internal Project Area

Primary: Quality / Governance.

Supporting: Corpus / Provenance and Generated / Local Artifacts boundaries.

This contract sits in Quality / Governance because it defines approval,
handoff, lifecycle, and role-routing semantics. It uses Corpus / Provenance
vocabulary from the recovery chain, but it does not move corpus metadata,
write fixtures, or restore parser behavior.

## Truth Owner

This contract owns only:

- human approval workflow vocabulary;
- approval metadata shape;
- role-routing status vocabulary;
- issue/PR lifecycle wording rules;
- fail-closed policy;
- validation expectations for a future approval metadata validator.

It does not own:

- parser facts;
- private evidence;
- fixture expected output;
- corpus status;
- golden replay truth;
- diagnostics or drift truth;
- readiness metrics;
- analytics truth;
- AI truth;
- coaching truth;
- issue lifecycle;
- PR lifecycle;
- tracker completion;
- merge readiness;
- deploy readiness.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
#451 Field Recovery Matrix
  + #452 symbolic offset-window metadata
  + #453 field-evidence comparison rows
  + #454 recovery candidate packets
  + #455 review-only issue/fixture/manifest drafts
  + explicit human approval metadata
  -> workflow route decision
  -> next scoped A-G workflow lane
```

Forbidden reverse flow:

```text
human approval metadata or route decision
  -/-> parser behavior
  -/-> parser state final reconciliation
  -/-> router behavior
  -/-> fixture files
  -/-> golden replay manifests
  -/-> corpus manifest/session ledger edits
  -/-> GitHub issue or PR creation
  -/-> private harvest execution
  -/-> tracker status changes
  -/-> #388/#381 activation
```

No parser/runtime/workbook/webhook/App Script/local-app/analytics/AI surface is
allowed to consume this workflow metadata as truth.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/parser_recovery_human_approved_parser_corpus_update_workflow.md`

If later explicitly authorized for implementation, this contract may own:

- `src/mythic_edge_parser/app/recovery_update_workflow_approval.py`
- `tests/test_recovery_update_workflow_approval.py`
- `docs/implementation_handoffs/parser_recovery_human_approved_parser_corpus_update_workflow_comparison.md`

This contract does not own:

- parser modules;
- recovery draft generator modules;
- recovery candidate packet modules;
- field recovery matrix modules;
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`;
- `tests/fixtures/parser_corpus/session_ledger.v1.json`;
- golden replay fixtures;
- golden replay manifests;
- expected-output files;
- issue comments;
- pull requests;
- tracker comments;
- local draft artifacts;
- private evidence artifacts.

## Public Interface

This contract defines future in-memory workflow metadata only. The interface
must not be implemented until explicitly authorized by a later user prompt or
workflow artifact.

Recommended constants:

```python
RECOVERY_UPDATE_APPROVAL_OBJECT = (
    "mythic_edge_parser_recovery_human_approval"
)
RECOVERY_UPDATE_ROUTE_DECISION_OBJECT = (
    "mythic_edge_parser_recovery_update_route_decision"
)
RECOVERY_UPDATE_APPROVAL_SCHEMA_VERSION = (
    "parser_recovery_human_approved_update_workflow.v1"
)
```

Recommended future helper functions:

```python
validate_recovery_update_approval(...)
build_recovery_update_route_decision(...)
validate_recovery_update_route_decision(...)
```

No CLI, environment variable, runtime service, diagnostics section, drift
report section, runtime status field, workbook column, webhook payload, Apps
Script surface, corpus metadata field, fixture schema, golden replay manifest,
GitHub issue, GitHub PR, branch, commit, or parser event is authorized by this
interface.

## Human Approval Metadata Shape

A human approval record is an in-memory mapping:

| Field | Required | Meaning |
| --- | --- | --- |
| `object` | yes | `mythic_edge_parser_recovery_human_approval` |
| `schema_version` | yes | `parser_recovery_human_approved_update_workflow.v1` |
| `approval_id` | yes | Deterministic public-safe ID |
| `approval_status` | yes | Approval status vocabulary below |
| `approved_by` | yes | Public-safe human or role label |
| `approved_at_utc` | yes | UTC timestamp or `not_recorded` |
| `approval_source` | yes | Public-safe source, such as issue comment URL |
| `selected_candidate_packet_id` | yes | #454 packet ID or #455 draft group source |
| `selected_draft_group_id` | optional | #455 draft group ID |
| `selected_field_id` | yes | Field Recovery Matrix field ID |
| `selected_action_type` | yes | Allowed action type vocabulary below |
| `owning_layer` | yes | Parser, Corpus / Provenance, or Quality / Governance |
| `allowed_artifact_classes` | yes | Explicit allowed artifact classes |
| `forbidden_artifact_classes` | yes | Explicit forbidden artifact classes |
| `allowed_scope` | yes | Short public-safe statement |
| `expiration_condition` | yes | Expiration condition vocabulary below |
| `target_role` | yes | Next A-G role |
| `target_issue` | optional | Existing GitHub issue URL if already created by authorized workflow |
| `target_branch` | optional | Branch name only when separately authorized |
| `required_contract` | optional | Future contract path or `not_yet_created` |
| `non_claims` | yes | Required non-claims |

Approval IDs must use only public-safe symbolic fields. They must not include
raw values, local paths, private offsets, private timestamps, hashes, raw event
payloads, decklists, card choices, strategy notes, secrets, credentials, or
webhook URLs.

## Approval Status Vocabulary

Allowed `approval_status` values:

- `approved_for_problem_framing`
- `approved_for_contract`
- `approved_for_review_only`
- `review_required`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `blocked_authorization`
- `expired`
- `invalid_input`

Meaning:

- `approved_for_problem_framing` routes to Codex A only.
- `approved_for_contract` routes to Codex B only when Codex A framing already
  exists or the approval explicitly names an existing issue.
- `approved_for_review_only` permits human/Codex review of existing metadata
  only.
- No approval status permits Codex C implementation, file writing, issue
  creation, PR creation, private harvest, fixture promotion, corpus status
  change, parser behavior change, #388 activation, or #381 activation by
  itself.

## Allowed Action Type Vocabulary

Allowed `selected_action_type` values:

- `frame_parser_recovery_issue`
- `write_parser_recovery_contract`
- `review_existing_recovery_candidate`
- `review_existing_draft_metadata`
- `plan_fixture_promotion_prerequisite`
- `plan_corpus_metadata_prerequisite`
- `plan_private_evidence_prerequisite`
- `no_action`

These are route labels only. They do not authorize the underlying action.

Forbidden `selected_action_type` values:

- `implement_parser_change`
- `create_fixture`
- `promote_fixture`
- `edit_corpus_manifest`
- `edit_session_ledger`
- `run_private_harvest`
- `read_private_log`
- `create_issue`
- `create_pr`
- `create_branch`
- `commit_changes`
- `push_branch`
- `merge_pr`
- `close_tracker`
- `activate_388`
- `activate_381`

Any forbidden action type must fail closed.

## Allowed Artifact Classes

The approval record may allow only planning/review artifact classes unless a
later explicit contract changes this.

Allowed in this contract:

- `problem_representation_metadata`
- `contract_metadata`
- `review_checklist_metadata`
- `non_claim_text`
- `validation_plan_metadata`
- `workflow_handoff_metadata`

Forbidden in this contract:

- `parser_code`
- `parser_event_classes`
- `router_code`
- `parser_state_code`
- `fixture_file`
- `golden_replay_manifest`
- `expected_output_file`
- `corpus_manifest`
- `session_ledger`
- `private_log`
- `private_evidence_packet`
- `local_generated_artifact`
- `github_issue`
- `github_pr`
- `git_branch`
- `git_commit`
- `git_push`
- `tracker_comment`
- `runtime_status`
- `workbook_schema`
- `webhook_payload`
- `apps_script`
- `analytics_behavior`
- `ai_or_coaching_output`

## Expiration Conditions

Allowed `expiration_condition` values:

- `expires_when_target_issue_created`
- `expires_when_contract_created`
- `expires_when_source_candidate_changes`
- `expires_when_base_branch_changes`
- `expires_when_tracker_388_status_changes`
- `expires_when_parent_434_status_changes`
- `expires_at_named_utc_time`
- `manual_reapproval_required`

An expired approval must fail closed and route to Codex A or human review.

## Route Decision Shape

A route decision is an in-memory mapping:

| Field | Required | Meaning |
| --- | --- | --- |
| `object` | yes | `mythic_edge_parser_recovery_update_route_decision` |
| `schema_version` | yes | `parser_recovery_human_approved_update_workflow.v1` |
| `route_decision_id` | yes | Deterministic public-safe ID |
| `approval_id` | yes | Source approval ID |
| `route_status` | yes | Route status vocabulary below |
| `next_role` | yes | A-G role or `human_review` |
| `route_reason` | yes | Symbolic reason code |
| `required_next_artifact` | yes | Expected artifact path or `not_applicable` |
| `allowed_actions` | yes | Explicit allowed actions for next role |
| `forbidden_actions` | yes | Explicit forbidden actions |
| `false_readiness_flags` | yes | All readiness flags false |
| `false_authorization_flags` | yes | All authorization flags false unless the next scoped issue owns one exact flag |
| `issue_lifecycle_policy` | yes | `refs_only` unless a later deployer action authorizes closure |
| `privacy_status` | yes | Public-safe privacy status |
| `protected_surface_assertions` | yes | All protected-surface booleans false |
| `non_claims` | yes | Required non-claims |

Allowed `route_status` values:

- `route_to_codex_a_problem_representation`
- `route_to_codex_b_contract`
- `route_to_human_review`
- `route_to_no_action`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `blocked_authorization`
- `blocked_expired_approval`
- `blocked_overclaim`
- `blocked_unsupported_action_type`
- `invalid_input`
- `fail_closed`

No route status may route directly to Codex C, Codex F, or Codex G unless a
separate scoped issue/contract/review package already exists and the route
decision explicitly preserves all relevant false flags.

## A-G Role Routing After Approval

Allowed routing:

1. Codex A may create or update a problem representation when approval status
   is `approved_for_problem_framing`.
2. Codex B may write a contract when approval status is
   `approved_for_contract` and an issue/problem representation exists.
3. Codex C may implement only after the new issue-specific contract explicitly
   authorizes implementation and names owned files/tests.
4. Codex E reviews implementation against the new contract.
5. Codex F submits only reviewed implementation scope.
6. Codex G merges, closes, or updates trackers only after explicit deployer
   approval and merge gates.

Forbidden routing:

- Codex B must not route directly from this contract to parser implementation.
- Codex C must not implement parser/corpus changes from a #455 draft alone.
- Codex F must not stage or open a PR from generated draft metadata alone.
- Codex G must not merge, close, or update tracker state from generated draft
  metadata alone.

## Issue Lifecycle Wording Rules

Generated or approved workflow text must default to `Refs` wording.

Allowed wording:

- `Refs #456`
- `Refs #388`
- `Refs #434`
- `Related to #455`
- `Follow-up to #455`

Forbidden wording until Codex G explicitly owns lifecycle closure:

- `Closes`
- `Close`
- `Closed by`
- `Fixes`
- `Fix`
- `Resolves`
- `Resolve`
- `Done by`
- `Completes`
- `Completed by`

This rule applies to issue text, PR text, handoffs, branch descriptions,
commit messages, generated review checklists, suggested tracker updates, and
future route decisions unless a later deployer-scoped contract explicitly
authorizes closing language.

## Parser-Change Gate

Parser changes remain blocked until a later issue-specific contract names:

- parser-owned fields or behavior to change;
- source evidence supporting the change;
- exact parser files owned;
- expected parser event/state/model impacts;
- final reconciliation impact;
- match/game identity and deduplication impact;
- focused tests;
- protected-surface checks;
- non-claims and rollback route.

This contract does not authorize parser behavior changes.

## Fixture-Promotion Gate

Fixture creation or promotion remains blocked until a later issue-specific
contract names:

- fixture evidence class;
- fixture source class;
- privacy review result;
- public-safe fixture body shape;
- expected-output shape;
- golden replay manifest changes;
- session ledger and corpus manifest changes, if any;
- proof object requirements;
- review and submitter/deployer gates.

This contract does not authorize fixture creation or promotion.

## Corpus-Status Gate

Corpus status changes remain blocked until a later issue-specific contract
names:

- scenario family;
- current status and target status;
- evidence basis;
- corpus manifest entry changes;
- session ledger entry changes;
- compatibility report behavior;
- validation commands;
- reviewer acceptance criteria.

This contract does not authorize corpus manifest edits, session ledger edits,
or corpus status changes.

## Private-Harvest Gate

Private harvest remains blocked until a later issue-specific contract and
explicit human approval name:

- exact source class;
- source window;
- local-only artifact class;
- redaction rules;
- retention rules;
- public summary policy;
- stop behavior;
- no raw-content commit guarantee.

This contract does not authorize private Player.log, UTC_Log, app-data, live
MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, watcher,
tailer, or private smoke checks.

## Privacy And Protected-Surface Invariants

Every approval record and route decision must preserve:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
implementation_authorized: false
file_writing_authorized: false
issue_creation_authorized: false
pr_creation_authorized: false
```

Every approval record and route decision must reject or fail closed if it
contains:

- raw/private Player.log or UTC_Log content;
- exact private local paths;
- app-data paths;
- source-window offsets;
- file sizes;
- hashes;
- raw payload values;
- private timestamps;
- private decklists;
- strategy notes;
- runtime artifacts;
- generated local artifacts;
- workbook exports;
- secrets;
- credentials;
- API keys;
- tokens;
- webhook URLs;
- caller-provided readiness claims;
- caller-provided parser support claims;
- caller-provided corpus status promotion claims;
- hidden authorization flags;
- source-action instruction text such as "open PR", "merge", "deploy", or
  "close tracker".

Forbidden values must not be echoed in validation errors or summaries.

## Required Non-Claims

Every approval record and route decision must include:

- `not_parser_truth`
- `not_issue_creation_authority`
- `not_pr_creation_authority`
- `not_file_writing_authorization`
- `not_field_recovery_readiness`
- `not_private_harvest_authorization`
- `not_fixture_promotion`
- `not_corpus_status_change`
- `not_parser_behavior_readiness`
- `not_pipeline_activation_readiness`
- `not_watcher_correctness`
- `not_private_smoke_success`
- `not_merge_readiness`
- `not_deploy_readiness`
- `not_release_readiness`
- `not_production_behavior`
- `not_analytics_truth`
- `not_ai_truth`
- `not_coaching_truth`

## Error Behavior

Fail closed when:

- required approval metadata is missing;
- approval is expired;
- approval selects multiple candidates;
- approval selects a forbidden action type;
- approval attempts to flip readiness or authorization flags;
- approval includes private/local/generated/secrets markers;
- approval includes source-action instructions;
- approval asks for parser, fixture, corpus, private-harvest, issue/PR, or
  #388/#381 activation work without a separate scoped issue and contract;
- current issue/tracker/parent state is ambiguous;
- WIP-1 active-lane interpretation conflicts with the requested route.

Fail-closed output may include public-safe symbolic reason codes only. It must
not echo caller-provided private values, paths, hashes, offsets, timestamps,
payload fragments, branch instructions, or issue/PR body text.

## Side Effects

Allowed in this Codex B pass:

- write this contract artifact only.

Forbidden in this Codex B pass:

- code implementation;
- tests implementation;
- branch publication;
- commit;
- PR creation;
- issue creation;
- issue comments;
- tracker comments;
- private reads;
- fixture/corpus/parser changes;
- local/generated artifact writing.

Future implementation, if explicitly authorized, must be side-effect-free and
in-memory unless a later contract grants one exact file-writing surface.

## Compatibility

This contract must remain compatible with:

- #451 Field Recovery Matrix field IDs and recovery categories;
- #452 symbolic offset-window metadata;
- #453 comparison report statuses;
- #454 recovery candidate packet statuses;
- #455 issue/fixture/manifest draft statuses;
- #381 through #387 planning contracts;
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`;
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`;
- current `Refs`-first issue lifecycle policy.

Compatibility does not mean older draft metadata can authorize action. Any
metadata without explicit human approval must route to `blocked_authorization`
or `review_required`.

## Tests Required

If a later contract authorizes Codex C implementation, focused tests must
cover:

- valid approval metadata routes to Codex A only for
  `approved_for_problem_framing`;
- valid approval metadata routes to Codex B only for `approved_for_contract`;
- implementation, fixture, corpus, private-harvest, issue creation, PR
  creation, branch, commit, merge, and deploy action types fail closed;
- multiple selected candidates fail closed;
- expired approval fails closed;
- missing candidate/field/action metadata fails closed;
- private markers, local paths, offsets, sizes, timestamps, hashes, payload
  fragments, secrets, and source-action instructions fail closed without value
  echo;
- `Refs` wording remains the default and closing keywords are rejected;
- all readiness and authorization flags remain false;
- route decisions cannot point directly to Codex C/F/G without a separate
  issue/contract/review package;
- blocked-private and blocked-external candidates remain blocked;
- generated route decisions contain required non-claims.

Suggested future validation:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_recovery_update_workflow_approval.py
python3 -m ruff check src/mythic_edge_parser/app/recovery_update_workflow_approval.py tests/test_recovery_update_workflow_approval.py
python3 -m py_compile src/mythic_edge_parser/app/recovery_update_workflow_approval.py
git diff --check
python3 tools/check_agent_docs.py
```

Codex C must also run a path-scoped secret/private-marker scan and
protected-surface scan for changed files.

## Acceptance Criteria

- The contract exists at
  `docs/contracts/parser_recovery_human_approved_parser_corpus_update_workflow.md`.
- The contract cites #456, #455/PR #547, #388, #434, and prior recovery
  contracts.
- The contract defines human approval metadata shape and route-decision shape.
- The contract defines approval status, action type, artifact class,
  expiration, and route status vocabularies.
- The contract preserves false readiness and authorization flags.
- The contract forbids private reads, file-writing beyond the contract,
  automatic issue/PR creation, fixture promotion, corpus status changes,
  parser changes, and pipeline activation.
- The contract defines `Refs` versus closing keyword rules.
- The contract routes future parser/corpus update work through A-G roles.
- `git diff --check` passes.
- `python3 tools/check_agent_docs.py` passes.

## Next Workflow Action

Next role: Codex E for contract review, or Codex F only if the user chooses to
submit this docs-only contract without an implementation pass.

Implementation is not authorized by this contract pass. Codex C should only
run after a later explicit user prompt or workflow artifact authorizes an
in-memory approval validator.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #456.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/456

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/455

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/547

Contract:
docs/contracts/parser_recovery_human_approved_parser_corpus_update_workflow.md

Goal:
Review the #456 planning-only contract. Verify that it defines human approval
and A-G role routing without authorizing parser changes, fixture promotion,
corpus status changes, private harvest, file writing beyond the contract,
GitHub issue/PR creation, or #388/#381 activation.

Focus:
- human approval metadata shape;
- action-type and artifact-class vocabulary;
- false readiness and authorization flags;
- Refs-versus-closing wording rules;
- fail-closed privacy/protected-surface behavior;
- route boundaries for Codex A/B/C/E/F/G;
- compatibility with #451 through #455 and #381 through #387 contracts.

Do not implement code, open a PR, run private checks, create issues/PRs,
promote fixtures, edit corpus metadata, change parser behavior, or activate
#388/#381.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/456"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/455"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/547"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue #456 Codex A reconciliation comment"
  target_artifact: "docs/contracts/parser_recovery_human_approved_parser_corpus_update_workflow.md"
  verdict: "human_approved_parser_corpus_update_workflow_contract_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/parser-recovery-human-approved-update-workflow-456"
  previous_merge_commit: "e705558aac679fe101856d0f973211fdf5ce34e7"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: false
  file_writing_authorized: false
  issue_creation_authorized: false
  pr_creation_authorized: false
  validation:
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
  stop_conditions:
    - "Do not activate #388 or #381."
    - "Do not close #388 or #434."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, diagnostics, drift, watcher, or private smoke checks."
    - "Do not create GitHub issues, PRs, branches, commits, recovery packet files, fixture-promotion packets, fixtures, manifests, expected-output files, corpus metadata edits, or local/generated artifacts."
    - "Do not authorize parser changes, private harvest execution, file-writing beyond the contract, fixture promotion, corpus status changes, PR creation, issue creation, or pipeline activation."
    - "Do not claim parser behavior readiness, pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, or coaching truth."
```
