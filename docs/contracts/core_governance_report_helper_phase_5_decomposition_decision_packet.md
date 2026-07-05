# Core Governance/Report/Helper Phase 5 Decomposition Decision Packet Contract

## Module

`core_governance_report_helper_phase_5_decomposition_decision_packet`

This contract defines the Phase 5 decomposition decision-packet boundary for
core Mythic Edge governance, report, and helper surfaces. It is a contract-only
Codex B artifact for issue #665.

Plain English: before a future role moves or decomposes governance/report/helper
code or documents, the future role must show what candidate is being considered,
what owns its authority today, who consumes it, why the change should stay in
this repository first, what evidence exists, what tests preserve behavior, and
what remains forbidden.

This contract does not implement code, move files, run ARS or Refactor Scout,
inspect source repositories, create run artifacts, change behavior, change CI,
or claim readiness, parser truth, security assurance, or privacy assurance.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: https://github.com/Tahjali11/Mythic-Edge
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/665
- Project roadmap / tracker: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Related ARS gate issue: https://github.com/Tahjali11/Mythic-Edge/issues/664
- Related decomposition tracker: https://github.com/Tahjali11/Mythic-Edge/issues/463
- Related completed decomposition contract: https://github.com/Tahjali11/Mythic-Edge/issues/461
- Target artifact:
  `docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`

## Source Artifacts Inspected

- GitHub issue #665
- GitHub issue #568, especially Phase 5 decomposition guidance
- GitHub issue #664
- GitHub issue #463
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/contracts/parser_match_summary_typed_handler_decomposition.md`
- `docs/contracts/governance_review_pattern_template_checklist_adoption.md`
- `docs/contracts/repo_wide_hardening_report_generator.md`

## Owning Layer

Primary layer: repository coordination and agent workflow / Shared Support.

This contract covers governance/report/helper surfaces that support how Mythic
Edge plans, validates, reports, and hands off work. It does not cover parser
truth, EventBus behavior, API payload shape, frontend behavior, live-capture
behavior, workbook/webhook behavior, Apps Script behavior, or CI enforcement.

## Truth And Authority Boundary

Current authority owners:

- Current repository governance docs, accepted ADRs, active GitHub issues,
  reviewed contracts, reviewed PRs, and deployer-recorded merge evidence own
  workflow authority.
- Repo-local helper scripts own only their own report/check output mechanics.
- Templates and handoff docs own only the structure of future workflow
  artifacts.
- Parser/state code remains the truth owner for parser-managed facts.
- EventBus code remains the truth owner for EventBus delivery behavior.
- API/frontend/live-capture code remains the truth owner for those runtime
  surfaces.
- ARS and Refactor Scout evidence, when present, is evidence only. It is not
  authority to move files, edit code, create issues, or claim readiness.

This contract is an authority surface only for the decision-packet shape and
the issue #665 boundaries. It does not authorize implementation.

## Authorization State

The following flags remain false for issue #665 and for this Codex B pass:

- `implementation_authorized: false`
- `file_move_authorized: false`
- `ars_run_authorized: false`
- `refactor_scout_run_authorized: false`
- `source_inspection_authorized: false`
- `source_mutation_authorized: false`
- `parser_behavior_change_authorized: false`
- `eventbus_behavior_change_authorized: false`
- `api_payload_change_authorized: false`
- `frontend_behavior_change_authorized: false`
- `live_capture_behavior_change_authorized: false`
- `workbook_schema_change_authorized: false`
- `webhook_payload_change_authorized: false`
- `apps_script_change_authorized: false`
- `ci_change_authorized: false`
- `runtime_artifact_creation_authorized: false`
- `claim_creation_authorized: false`
- `readiness_claimed: false`
- `parser_truth_claimed: false`
- `reliability_readiness_claimed: false`
- `security_assurance_claimed: false`
- `privacy_assurance_claimed: false`

## Observed Current Behavior

Mythic Edge Phase 5 currently requires decomposition decision packets before
code moves across module or repository boundaries. The current roadmap order
places core Mythic Edge decomposition after cross-repo decision-packet passes
and orders core targets as follows:

1. governance/report/helper surfaces;
2. EventBus/support surfaces;
3. API/frontend/live-capture surfaces;
4. parser state and `state.py` last.

The repository already has governance docs, role docs, templates, contracts,
report-only helper scripts, advisory check helpers, validation selectors, and
quality/security report helpers. These surfaces support workflow coordination
and evidence reporting. They are lower product-blast-radius than parser,
EventBus, API, frontend, or live-capture behavior, but they can still create
false authority if their output is treated as implementation clearance,
security assurance, or readiness proof.

Issue #664 records a related ambiguity: ARS Phase 3 was cleared for routing,
but that is not proof of a fresh project-wide ARS sweep after every ARS update.
Phase 5 packets must therefore record ARS/refactor evidence status explicitly
instead of treating stale or absent evidence as clearance.

## Problem Statement And First Bad Values

The intended behavior is a small, reviewable decision packet before any
governance/report/helper decomposition or file movement.

The first bad value is treating a decision packet as implementation authority.
A packet may recommend a later route; it must not move files or change behavior.

The second bad value is treating stale, historical, absent, or mismatched ARS
or Refactor Scout evidence as current clearance.

The third bad value is broadening this issue into later Phase 5 targets:
EventBus/support, API/frontend/live-capture, or parser state. Those targets are
intentionally later and require their own contracts.

The fourth bad value is cross-repo extraction by default. Phase 5 requires
same-repo decomposition first unless a later explicit decision proves the
boundary is stable, useful, independently testable, and separately governed.

## Scope Decision

This issue defines the decision-packet contract for governance/report/helper
surfaces only.

Allowed in this contract:

- classify eligible governance/report/helper surface classes;
- define required decision-packet fields;
- define ARS/refactor evidence status vocabulary;
- define same-repo-first and cross-repo refusal rules;
- define public-safe non-claims and false-authority flags;
- define validation expectations for a later behavior-preserving change;
- recommend the next role.

Not allowed in this contract:

- implementing code;
- moving files;
- changing templates, role docs, governance docs, source code, frontend, API,
  parser, EventBus, live-capture, CI, or runtime behavior;
- running ARS, Refactor Scout, probes, module sweeps, replay audits, or private
  evidence reads;
- creating claims, run artifacts, candidate dossiers, source-repo issues, PRs,
  comments, labels, branches, commits, or status checks;
- claiming parser truth, analytics truth, AI truth, coaching truth,
  reliability readiness, release readiness, deploy readiness, production
  readiness, security assurance, or privacy assurance.

## Candidate Surface Classes

Future decision packets may classify candidates with exactly one primary class:

- `governance_doc_surface`: repo governance, constitution, ADR, workflow, or
  role documentation.
- `template_surface`: workflow templates, handoff templates, report templates,
  or issue/PR template helpers.
- `handoff_report_format_surface`: durable handoff/report format docs or
  report examples.
- `report_only_helper_surface`: repo-local scripts that assemble report-only
  Markdown, JSON, or advisory summaries from explicit inputs.
- `local_advisory_check_surface`: repo-local checks that inspect committed repo
  files and produce local advisory status.
- `workflow_status_roadmap_helper_surface`: helpers or docs that summarize
  roadmap, issue, tracker, or workflow status without changing external state.
- `contract_catalog_surface`: contracts or indexes that describe governance,
  report, helper, or validation boundaries.
- `mixed_governance_runtime_surface`: a candidate that appears to mix
  governance/report/helper behavior with runtime behavior. This class must
  route to `review_required` or `request_scope_split_child`.
- `unknown_review_required`: classification is unclear or unsupported.

Forbidden primary classes for this issue:

- `parser_truth_surface`
- `eventbus_behavior_surface`
- `api_payload_surface`
- `frontend_behavior_surface`
- `live_capture_behavior_surface`
- `workbook_webhook_surface`
- `apps_script_surface`
- `ci_enforcement_surface`
- `private_evidence_surface`

If a candidate fits any forbidden class, this issue must refuse the candidate
or split it into a later scoped child.

## Decision Vocabulary

Each candidate row must end with exactly one decision:

- `same_repo_keep_current_path`: keep the candidate where it is; no move.
- `same_repo_decomposition_candidate`: later same-repo decomposition may be
  considered after review and validation.
- `same_repo_docs_format_candidate`: later docs/template/report-format edit may
  be considered after review.
- `request_fresh_ars_refactor_evidence`: current evidence is missing, stale, or
  mismatched and fresh scoped evidence is needed before implementation.
- `request_scope_split_child`: candidate mixes governance/report/helper scope
  with a later protected surface and needs a separate issue.
- `reject_cross_repo_extraction`: cross-repo extraction is not justified.
- `defer`: no action now.
- `unsupported`: candidate is outside the issue #665 scope.
- `review_required`: human or Codex E review must decide before routing.

Forbidden decisions:

- `implementation_approved`
- `file_move_approved`
- `cross_repo_extraction_approved`
- `ars_clearance_granted`
- `refactor_scout_clearance_granted`
- `ready_for_merge`
- `ready_for_release`
- `security_assured`
- `privacy_assured`

## Required Packet Envelope

A later governance/report/helper decomposition packet must include this
envelope before any candidate rows:

| Field | Requirement |
| --- | --- |
| `packet_schema` | Literal `core_governance_report_helper_phase_5_decomposition_decision_packet.v1`. |
| `repository` | `Tahjali11/Mythic-Edge`. |
| `issue` | The active child issue URL. |
| `tracker` | `https://github.com/Tahjali11/Mythic-Edge/issues/568`. |
| `related_decomposition_tracker` | Issue #463 when relevant. |
| `related_ars_gate_issue` | Issue #664 when ARS evidence status is considered. |
| `target_commit` | Commit or branch baseline reviewed for the packet. |
| `candidate_scope` | `governance_report_helper_only`. |
| `phase_5_order_preserved` | Must be `true`. |
| `eventbus_support_deferred` | Must be `true`. |
| `api_frontend_live_capture_deferred` | Must be `true`. |
| `parser_state_deferred` | Must be `true`. |
| `implementation_authorized` | Must be `false`. |
| `file_move_authorized` | Must be `false`. |
| `ars_run_authorized` | Must be `false` unless a later issue explicitly authorizes a scoped ARS run. |
| `source_mutation_authorized` | Must be `false`. |
| `readiness_claimed` | Must be `false`. |
| `truth_or_assurance_claimed` | Must be `false`. |

If any required false-authority field is absent, true, ambiguous, caller
provided without verification, or contradicted by prose, the packet must fail
closed.

## Required Candidate Row Fields

Each candidate row must include:

| Field | Requirement |
| --- | --- |
| `candidate_id` | Stable symbolic ID for the candidate row. |
| `candidate_surface_class` | One allowed class from this contract. |
| `current_path` | Repo-relative path or symbolic path group. No local absolute paths. |
| `current_behavior` | Plain-English description of what the candidate does today. |
| `truth_or_authority_owner` | Current owner of workflow authority, report semantics, or helper output. |
| `upstream_dependencies` | Explicit inputs or docs the candidate depends on. |
| `downstream_consumers` | Humans, roles, scripts, templates, reports, or workflows that consume it. |
| `protected_surface_contact` | `none`, `read_only_reference`, or `mixed_review_required`. |
| `proposed_destination` | Same path, same repo new module/path, or deferred. |
| `why_not_keep_local` | Required if proposing any move or split. |
| `why_not_move_to_existing_repo` | Required for any cross-repo thought experiment. |
| `why_not_create_new_repo` | Required for any cross-repo thought experiment. |
| `new_public_interface_needed` | `none`, `private_same_repo`, or `review_required`. |
| `new_public_interface_description` | Required unless `none`. |
| `behavior_preservation_tests` | Focused checks needed before and after a later implementation. |
| `rollback_plan` | How a later implementation can revert without data migration or truth changes. |
| `ars_refactor_evidence_status` | Required status block defined below. |
| `non_claims` | Explicit forbidden claims retained for the row. |
| `final_decision` | One decision from this contract. |

## ARS And Refactor Evidence Status

Every candidate row must include:

| Field | Allowed values / requirement |
| --- | --- |
| `prior_ars_evidence_found` | `yes`, `no`, or `not_applicable`. |
| `prior_refactor_scout_evidence_found` | `yes`, `no`, or `not_applicable`. |
| `reviewed_repo` | Repo name or `none`. |
| `reviewed_scope` | Module/path/surface reviewed or `none`. |
| `reviewed_commit` | Commit reviewed or `none`. |
| `ars_version_contract_bundle` | Symbolic version/contract/bundle or `none`. |
| `current_target_commit` | Commit used for the packet. |
| `relevant_changes_since_review` | `none_known`, `yes`, `unknown`, or `not_applicable`. |
| `evidence_status` | One of the statuses below. |
| `fresh_scoped_evidence_needed` | `yes`, `no`, or `review_required`. |
| `reason` | Plain-English reason. |

Allowed `evidence_status` values:

- `current_matching_scope`
- `historical_only`
- `stale_mismatched_commit`
- `stale_mismatched_scope`
- `absent`
- `not_needed_for_contract_only`
- `fresh_scoped_evidence_required_before_implementation`
- `blocked_by_gate_ambiguity`
- `review_required`
- `unsupported`

Rules:

- Historical evidence must not be called current unless it matches the current
  target commit, repository, scope, ARS/refactor version or contract bundle, and
  current decomposition question.
- Absence of ARS/refactor evidence may be acceptable for this contract-only
  packet only when the row explicitly says why the candidate is low-risk,
  same-repo, public-safe, and not touching protected runtime behavior.
- Fresh scoped evidence must be requested before implementation if the
  candidate touches helper code that reads protected-surface files, security
  scan outputs, CI configuration, private/public disclosure boundaries, runtime
  behavior, source mutation, artifact creation, or ambiguous mixed scope.
- Issue #664 remains a related gate. This contract does not close #664 or claim
  project-wide ARS completion.

## Same-Repo-First Rule

The default decision for eligible candidates is same-repo first.

Same-repo decomposition may mean:

- split a large helper into smaller same-repo helper modules;
- split a report generator into same-repo parsing, validation, and rendering
  helpers;
- split docs/template guidance into clearer same-repo documents;
- keep a stable caller entrypoint while moving private helper functions behind
  it in the same repository.

Cross-repo extraction is not authorized by this contract. A later contract may
consider cross-repo extraction only if it proves all of the following:

- the boundary is stable;
- the boundary is useful outside this repository;
- the boundary is independently testable;
- the boundary is separately governed;
- a new public interface is explicitly reviewed;
- no parser truth, EventBus behavior, API payload, frontend behavior,
  live-capture behavior, workbook/webhook behavior, Apps Script behavior, CI
  gate, private evidence surface, or source mutation authority is moved by
  implication.

## Phase 5 Target Order Preservation

This contract covers only the first core Phase 5 target class:
governance/report/helper surfaces.

The following remain later targets and must not be included in candidate rows
except as downstream consumers or protected-surface references:

- EventBus/support surfaces;
- API/frontend/live-capture surfaces;
- parser state and `state.py`;
- parser event classes;
- parser final reconciliation;
- match identity;
- game identity;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- CI gate behavior.

If a candidate cannot be evaluated without changing one of those surfaces, the
decision must be `request_scope_split_child`, `defer`, or `review_required`.

## Public-Safe And No-Echo Rules

Decision packets and later reports must use repo-relative paths and symbolic
evidence categories.

Packets must not include:

- local absolute paths;
- usernames or machine-specific paths;
- raw private logs;
- raw source snippets when not necessary for public review;
- raw diffs or patches;
- secrets, credentials, tokens, API keys, webhook URLs, workbook IDs, or
  provider outputs;
- private evidence contents;
- exact private validation data;
- unreviewed security detail;
- readiness, truth, or assurance claims.

If a source value is unsafe, the packet must use a symbolic category such as
`private_marker_redacted`, `local_path_redacted`, `raw_payload_omitted`, or
`review_required` instead of echoing the unsafe value.

## Example Candidate Rows

These examples are public-safe and illustrative only. They do not authorize
implementation.

| candidate_id | candidate_surface_class | current_path | current_behavior | evidence_status | final_decision |
| --- | --- | --- | --- | --- | --- |
| `agent_doc_consistency_check` | `local_advisory_check_surface` | `tools/check_agent_docs.py` | Checks repo governance docs for consistency signals. | `absent` | `review_required` |
| `workflow_handoff_template` | `template_surface` | `docs/templates/workflow_handoff.md` | Provides durable handoff structure for workflow roles. | `not_needed_for_contract_only` | `same_repo_docs_format_candidate` |
| `report_generator_family` | `report_only_helper_surface` | `tools/generate_*_report.py` | Generates report-only advisory artifacts from explicit repo-local inputs. | `review_required` | `request_fresh_ars_refactor_evidence` |

## Validation Expectations For Later Implementation

This contract does not authorize a later implementation. If a later issue does
authorize a behavior-preserving governance/report/helper decomposition, Codex C
must choose validation based on the candidate row.

Minimum validation expectations:

- `git diff --check`
- focused tests for any changed helper script or report generator;
- parser tests only if a candidate unexpectedly touches parser-adjacent code,
  in which case the work should usually stop and route to a narrower contract;
- `python3 -m py_compile` for changed Python helper scripts when applicable;
- focused pytest files for changed helper behavior when tests exist or are
  added;
- repo-owned governance-doc checks when governance docs, role docs, or
  templates change;
- repo-owned secret/private-marker checks for public artifacts;
- protected-surface checks when any candidate references protected surfaces;
- before/after report comparison for report generators;
- stable output ordering checks for deterministic reports.

Validation must not:

- run private evidence;
- run ARS, Refactor Scout, probes, module sweeps, replay audits, or live
  capture;
- change CI;
- create durable runtime artifacts unless separately authorized;
- claim readiness, parser truth, reliability readiness, security assurance, or
  privacy assurance.

## Rollback Expectations

Later behavior-preserving decompositions must be rollback-safe:

- keep existing public entrypoints where possible;
- avoid data migrations;
- avoid new external dependencies unless separately contracted;
- avoid cross-repo version coupling;
- keep output formats stable unless a later contract explicitly approves a
  format change;
- make rollback possible through reverting the implementation commit or
  restoring the previous same-repo file layout.

## Non-Claims

This contract does not claim:

- parser truth;
- parser behavior readiness;
- analytics truth;
- AI truth;
- coaching truth;
- EventBus reliability readiness;
- release readiness;
- deploy readiness;
- production readiness;
- security assurance;
- privacy assurance;
- ARS completion;
- Refactor Scout completion;
- implementation readiness;
- merge readiness.

## Recommended Next Role

Codex E: review this contract against issue #665, #568 Phase 5, #664, and the
protected boundaries. If accepted, Codex E may route to Codex F for a docs-only
submitter pass. If the evidence vocabulary or candidate classes are still
ambiguous, Codex E should route back to Codex B with a concrete finding.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Contract Reviewer for Mythic-Edge issue #665.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/665

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related ARS gate issue:
https://github.com/Tahjali11/Mythic-Edge/issues/664

Target artifact:
docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md

Goal:
Review the Phase 5 core governance/report/helper decomposition decision packet
contract. Confirm that it preserves the same-repo-first rule, records ARS and
Refactor Scout evidence status without treating stale evidence as clearance,
keeps EventBus/support, API/frontend/live-capture, and parser state as later
targets, and does not authorize implementation, file movement, ARS runs,
source mutation, CI changes, behavior changes, readiness claims, parser truth
claims, security assurance, or privacy assurance.

Protected boundaries:
Do not implement code, move files, open a PR, run ARS, run Refactor Scout,
inspect or mutate source repos, change parser/EventBus/API/frontend/live-capture
behavior, change CI, or claim readiness/truth/assurance.

Expected output:
Findings first, validation evidence reviewed, whether the contract is ready for
Codex F, any required Codex B fixes, and a workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/665"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  completed_thread: "B"
  next_thread: "E"
  verdict: "core_governance_report_helper_phase_5_decomposition_decision_packet_contract_ready_for_review"
  risk_tier: "High"
  target_artifact: "docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md"
  implementation_authorized: false
  file_move_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  source_inspection_authorized: false
  source_mutation_authorized: false
  parser_behavior_change_authorized: false
  eventbus_behavior_change_authorized: false
  api_payload_change_authorized: false
  frontend_behavior_change_authorized: false
  live_capture_behavior_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  parser_truth_claimed: false
  reliability_readiness_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
