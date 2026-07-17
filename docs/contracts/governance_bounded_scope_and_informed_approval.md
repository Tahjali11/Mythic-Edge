# Governance Bounded Scope And Informed Approval Contract

Status: Draft contract for review

Role: Codex B - Module Contract Writer

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/737>

Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Proposed ADR:
`docs/decisions/ADR-0010-bounded-scope-and-informed-approval.md`

## Module

`governance_bounded_scope_and_informed_approval`

This contract defines a durable governance policy for two linked controls:

1. workflow authority is bounded to the scope the owner and repository actually
   granted; and
2. consequential actions require approval based on understandable material
   facts, not a vague or inherited permission signal.

The policy is intentionally proportionate. A clear current request is enough
for routine, local, reversible work inside the active role and scope. Codex
must not ask the owner to repeat an approval merely to produce a preferred
phrase or packet. Stronger approval gates remain for protected, credentialed,
destructive, external-write, merge, deployment, and production actions.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: <https://github.com/Tahjali11/Mythic-Edge>
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/737>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

## Authority And Sources Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/templates/workflow_handoff.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR_TEMPLATE.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`
- `docs/decisions/ADR-0008-repo-wip-1-lane-activation-policy.md`
- `docs/decisions/ADR-0009-optional-dependency-provider-model.md`
- issue #568
- issue #713
- issue #682 and its accepted contract
- issues #650 and #652

Fresh-state checks established that issue #737 is the only matching bounded-
scope/informed-approval issue, ADR-0010 is the next unused ADR number, and
ADR-0009 remains `Proposed`.

## Owning Layer

Quality / Governance.

The policy owns workflow authority interpretation and approval boundaries. It
does not own parser truth, analytics truth, workbook truth, UI truth, AI truth,
security assurance, privacy assurance, merge readiness, deploy readiness, or
production truth.

## Internal Project Area

Quality / Governance.

## Truth Owner

Current user instructions, repository governance, active issues, active
contracts, accepted ADRs, reviewed artifacts, GitHub state, and explicit
approval evidence own workflow authority according to the existing authority
order.

This contract clarifies how to interpret that authority. It does not create a
new authority source or allow lower-priority artifacts to override current
instructions or repository governance.

## Bridge-Code Status

`not_bridge_code`

## Files Owned By This Contract

- `docs/contracts/governance_bounded_scope_and_informed_approval.md`
- `docs/decisions/ADR-0010-bounded-scope-and-informed-approval.md`
- the ADR-0010 index row in `docs/decisions/README.md`

No runtime, test, validator, CI, role, template, constitution, or machine-rule
file is owned by this Codex B pass.

## Public Interface

This contract defines governance vocabulary and decision rules for:

- authority scope;
- action classification;
- approval requirements;
- informed-approval content;
- approval lifecycle and invalidity;
- scope drift;
- role routing;
- non-claims.

It does not define a new JSON packet, database, validator, API, CLI, receipt,
token, credential, runtime status file, or external approval service.

## Bounded Authority Model

Authority for a continuing workflow action is bounded by all material
dimensions that apply:

| Dimension | Requirement |
| --- | --- |
| `authority_source` | Current user instruction, current issue, contract, accepted ADR, or other source at its existing authority level. |
| `repository` | Exact repository in which action is allowed. |
| `issue_or_purpose` | Exact issue, tracker child, or bounded purpose. |
| `role` | Active A-G or auxiliary H role and the role's permitted operation. |
| `allowed_operation` | Read, write docs, implement, review, stage, submit, merge, deploy, delete, publish, install, or another explicitly named operation. |
| `allowed_artifacts_or_surfaces` | Named artifacts, paths, interfaces, protected surfaces, external objects, or a mechanically bounded set. |
| `forbidden_operations_or_surfaces` | Material exclusions and protected boundaries. |
| `side_effects` | Local, durable, external, destructive, credentialed, deployment, production, or no side effect. |
| `lifecycle` | Current turn, active role, issue lifetime, single use, bounded reuse, expiry, or another explicit end condition. |
| `validation_and_rollback` | Required evidence and rollback or stop behavior when material. |
| `next_gate` | The next role or approval boundary; passing the current gate does not imply later authority. |

Unspecified authority is false when the action is consequential or would
expand the current issue, contract, role, artifact, protected surface, external
effect, or lifecycle.

These dimensions do not need to be serialized into a new packet for every
action. For routine work they may be evident from the current request and role.
For cross-thread, high-risk, or consequential work they must be recorded in an
existing durable authority surface such as the issue, contract, handoff, PR,
review, owner comment, or current user instruction.

## Action Classification

Every proposed mutation uses exactly one class:

Classification is ordered and fail-closed. Evaluate predicates in this exact
precedence order and stop at the first match:

1. `prohibited_without_new_authority`
2. `consequential`
3. `scoped_workflow`
4. `routine_local`

An action that matches multiple descriptions takes the highest-precedence
class. An action that cannot be classified from current evidence defaults to
`prohibited_without_new_authority`; ambiguity never permits selection of a
less restrictive class. Classification considers the proposed action and its
material effects, not merely the role or existence of an issue or contract.

### `routine_local`

This class is selected only when none of the three higher-precedence classes
applies.

All of the following are true:

- the current request clearly asks for the action;
- the action is local, reversible, and within the active role;
- no protected surface, credential, private evidence, external write,
  destructive operation, merge, deployment, or production state is touched;
- scope and expected effects are ordinary and unsurprising;
- the action does not establish new durable policy beyond the current issue.

Examples include an authorized typo fix, local formatting, or a focused docs
edit that is already within the current request.

Approval rule: `current_request_sufficient`.

### `scoped_workflow`

This class is selected only when neither `prohibited_without_new_authority`
nor `consequential` applies. It takes precedence over `routine_local` when an
action also produces durable repository or workflow state.

The action is within an active issue, contract, role, and named file or
interface boundary, but it produces durable repository work or moves the
workflow to its next role.

Examples include contracted implementation edits, an independent review,
staging reviewed files, or publishing an issue explicitly requested by the
owner.

Approval rule: `existing_scoped_authority_sufficient` only for the role's
current operation. Later role gates remain separate.

### `consequential`

This class is selected only when `prohibited_without_new_authority` does not
apply. It takes precedence over `scoped_workflow` and `routine_local`, including
when an issue and contract fully bound the protected or external operation.

The action touches any of the following:

- protected parser, identity, reconciliation, schema, transport, or workflow
  policy behavior;
- credentials, permissions, secrets, environment contracts, private evidence,
  or sensitive external data;
- destructive cleanup or irreversible state;
- external writes not already explicit in the current request;
- issue closure, merge, release, package publication, installation, service
  mutation, deployment, canary, or production behavior;
- a material expansion in repository, paths, operations, side effects, reuse,
  or lifecycle.

Approval rule: `separate_exact_approval_required` before the action. A clear
current user instruction can itself be that exact approval when it contains or
follows disclosure of the material facts. No second ceremonial confirmation is
required solely because a preferred phrase was not used.

### `prohibited_without_new_authority`

This is the highest-precedence class. It also owns the default when evidence
is insufficient to classify an action safely.

The action is outside the current issue or contract, conflicts with higher
authority, moves truth ownership, lacks a required protected-surface contract,
or cannot be made sufficiently bounded and understandable.

Approval rule: `new_issue_or_contract_required` or `forbidden`, as applicable.

## Approval Requirement Vocabulary

Use exactly one value when an approval decision must be recorded:

- `current_request_sufficient`
- `existing_scoped_authority_sufficient`
- `separate_exact_approval_required`
- `new_issue_or_contract_required`
- `forbidden`

The first two values authorize only the current classified operation. They do
not authorize the next role or a different side effect.

## Informed Approval Contract

For a consequential action, the owner must be able to understand the material
decision before it occurs. Use plain English and disclose the applicable
items:

1. the action and why it is proposed;
2. the exact repository, external target, artifact, path set, or protected
   surface;
3. expected durable, destructive, credentialed, external, deployment, or
   production effects;
4. material risk and the first likely failure boundary;
5. reversibility, rollback, cleanup, or why an effect is irreversible;
6. validation that will prove the requested action rather than broader
   readiness;
7. lifecycle, expiry, single-use or bounded-reuse behavior when relevant;
8. what remains unauthorized after approval;
9. any known drift that would invalidate the approval.

Do not require irrelevant fields. The goal is informed choice, not form
completion. When the current request already supplies the applicable facts,
Codex must not ask the owner to repeat them.

If inspection reveals a material effect, risk, path, protected surface, or
external target that was not reasonably apparent when the owner approved the
action, stop before that effect and request refreshed approval.

## Approval Lifecycle

When lifecycle matters, use exactly one state:

- `not_applicable`
- `active_single_use`
- `active_bounded_reuse`
- `consumed`
- `expired`
- `revoked`
- `superseded`

Rules:

- Approval is non-transferable by default across repositories, issues, roles,
  operations, target paths, protected surfaces, external targets, versions, or
  materially changed state.
- Single-use approval cannot be replayed after consumption or a failed attempt
  when its owning contract defines failure as consuming.
- Bounded reuse must name its limit and expiration condition. Silence does not
  imply reuse.
- A newer explicit user instruction may revoke, narrow, supersede, or replace
  an earlier instruction.
- A handoff may report approval but cannot manufacture or broaden it.
- Example text, placeholders, reviewer recommendations, generated values, and
  conditional future statements grant no authority.

## Invalid Authority Vocabulary

An action must fail closed when authority is:

- `missing`
- `stale`
- `expired`
- `revoked`
- `superseded`
- `consumed`
- `scope_mismatch`
- `contradictory`
- `unverifiable`

Failure means no protected, external, destructive, merge, deployment, or
production mutation occurs. The role records a symbolic reason and routes to
the owner, Codex A, or Codex B as appropriate. It must not echo credentials,
private evidence, raw paths, or sensitive payloads to prove refusal.

## Gate Separation

The following are deliberately separate:

- evidence that a precondition passed;
- permission to perform the current operation;
- readiness for the active role;
- implementation conformance;
- independent review acceptance;
- authority to stage or submit;
- merge authority;
- installation or deployment authority;
- production or canary authority;
- parser, analytics, workbook, AI, or other truth;
- security, privacy, correctness, release, deploy, or production assurance.

Passing one does not imply another. In particular:

- issue publication does not authorize implementation;
- contract completion does not authorize Codex C;
- Codex E acceptance does not authorize Codex F, merge, or deployment;
- a draft PR does not authorize Codex G to merge;
- merge does not authorize installation, canary, deployment, or production;
- a validator or test pass is evidence, not authority or assurance.

## Proportionality And Ceremony Budget

Codex must use the least ceremony that preserves the material boundary.

- Do not ask for a duplicate confirmation when the current request is already
  clear and informed for the exact action.
- Do not create a new packet, schema, receipt, lifecycle store, issue, or ADR
  when an existing authority artifact can record the boundary safely.
- Do not require exhaustive high-risk fields for routine local work.
- Do not use convenience or low risk to bypass protected-surface, credential,
  destructive, external-write, merge, deploy, or production gates.
- Repeated ambiguity or a rule that affects future modules belongs in a
  contract or ADR rather than repeated ad hoc prompts.
- A rule that adds ceremony without preventing a concrete failure should be
  simplified; a rule that prevents a concrete high-impact failure should be
  preserved.

## Workflow Routing

Use the existing workflow routes:

- Codex A when purpose, ownership, risk, or issue framing changes.
- Codex B when contract scope, authority interpretation, interface, lifecycle,
  or acceptance criteria are ambiguous or wrong.
- Codex D only for concrete implementation, test, or CI findings inside an
  accepted contract and the #682 blocker-packet boundary.
- Codex E for independent verification and finding classification.
- Codex F only for reviewed files and an approved submission target.
- Codex G only after explicit merge, closeout, or integration routing and its
  existing gates.
- The owner when a consequential action needs exact approval or policy choice.

The policy does not create a new workflow role or bypass A-G.

## Compatibility And Overlap Boundaries

### ADR-0008 And Active Lanes

ADR-0008 remains the accepted WIP-1 policy. Its named, scoped, expiring
exceptions are an application of bounded authority. ADR-0010 does not change
its exception vocabulary or active-lane rules.

### Issue #713

Issue #713 remains the narrower source for Codex G checkout reconciliation and
cleanup responsibility. Existing exact approval for destructive cleanup and
the verified squash-merge residue exception remain unchanged.

### Issue #682

Issue #682 remains the source for helper-agent boundaries and durable E-to-D
blocker packets. ADR-0010 does not weaken Codex E finding ownership, Codex D
patch ownership, or blocker-packet requirements.

### Issues #650 And #652

The adopted review-template and checklist mechanics remain in force. This
contract does not duplicate their fields or authorize template edits.

### ADR-0009

ADR-0009 remains `Proposed` and non-precedential. ADR-0010 neither accepts nor
supersedes it.

## Inputs

Allowed inputs:

- current user instructions;
- current repository governance;
- live GitHub issue, PR, branch, and tracker state;
- active issues, contracts, accepted ADRs, reviews, handoffs, and validation;
- public-safe approval evidence already authorized for the workflow.

Forbidden as independent authority:

- stale prompts or chat memory;
- local worktree names or status indexes;
- example or placeholder approvals;
- subagent output;
- reviewer-authored approval values;
- generated authority flags;
- unverified copied handoffs;
- credentials, private evidence, raw logs, or local artifacts used to broaden
  authority.

## Outputs

This Codex B pass produces:

- this contract;
- proposed ADR-0010;
- the proposed ADR index row;
- a handoff to independent Codex E review.

No implementation, validator, runtime, CI, issue closure, PR, merge,
deployment, or production output is authorized.

## Invariants

- Current user instructions remain above repository docs in the existing
  authority order.
- No magic approval phrase is required when intent and material scope are
  already clear.
- Consequential action never relies on inferred or inherited authority.
- Authority cannot silently expand across role, repository, path, operation,
  side effect, target, version, or lifecycle.
- Unspecified consequential authority is false.
- Low-risk work retains a simple, reversible path.
- Protected surfaces retain issue, contract, review, and validation gates.
- Evidence, permission, readiness, truth, and assurance remain distinct.
- Existing #713, #682, #650/#652, and ADR-0008 mechanics remain authoritative
  in their narrower scopes.
- ADR-0009 remains proposed.

## Error Behavior

Stop before mutation and report the narrow reason when:

- action classification is ambiguous and the difference changes approval;
- a consequential action lacks informed approval;
- issue, contract, role, repository, path, operation, side effect, or lifecycle
  is outside the authority boundary;
- protected-surface authority is absent;
- approval is invalid under the closed vocabulary;
- branch, issue, PR, target, or artifact drift changes the approved action;
- instructions conflict and the conflict cannot be resolved by current
  authority order;
- a lower-authority source appears to grant broader permission;
- the requested action would move truth ownership or create an unframed durable
  policy.

Routine assumptions may continue only when they are low risk and cannot
materially change scope, behavior, protected state, external state, or owner
intent.

## Governance Review Checklist

- Every status and route used by this contract is defined above.
- Private values are not required in public approval records.
- Approval evidence is necessary but not sufficient for later role gates.
- Unknown or extra authority is rejected rather than inferred.
- Examples cannot grant authority.
- No authorization flag is pre-enabled by this contract.
- No protected-surface enforcement, CI gate, validator, or runtime behavior is
  introduced.

## Side Effects

Authorized side effects of this Codex B pass:

- create the contract;
- create the proposed ADR;
- add one proposed ADR index row;
- preserve issue #737 as the source problem representation.

No other repository, GitHub, external, local runtime, service, credential,
private artifact, or production state is changed.

## Dependency Order

1. Codex B writes the contract and proposed ADR on fresh `origin/main`.
2. Codex E independently reviews issue #737, the contract, ADR, and index row.
3. Concrete documentation defects route to Codex D; policy ambiguity routes
   to Codex B; framing errors route to Codex A.
4. Codex F may submit only the exact reviewed docs package.
5. Codex G may merge only after explicit owner approval and normal gates.
6. ADR-0010 remains `Proposed` until a later reviewed repository change records
   its accepted lifecycle after merge.
7. Any authority-doc, role-doc, template, machine-rule, skill, validator, or CI
   adoption requires a separately scoped implementation issue and contract.

## Compatibility

This policy clarifies existing authority behavior. It does not supersede the
constitution, authority order, ADR-0004, ADR-0005, ADR-0008, issue #713, issue
#682, or issues #650/#652.

Historical approvals and completed actions are not retroactively invalidated.
Future actions must use current authority and the policy once ADR-0010 becomes
accepted.

## Tests Required

Codex B validation:

```powershell
git diff --check
py tools/check_agent_docs.py
@'
docs/contracts/governance_bounded_scope_and_informed_approval.md
docs/decisions/ADR-0010-bounded-scope-and-informed-approval.md
docs/decisions/README.md
'@ | py tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/governance_bounded_scope_and_informed_approval.md
docs/decisions/ADR-0010-bounded-scope-and-informed-approval.md
docs/decisions/README.md
'@ | py tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

Codex E must review at least these cases:

| Case | Expected result |
| --- | --- |
| Clear typo or formatting request in current scope | `routine_local`; no duplicate confirmation. |
| Contracted code edit within named files | `scoped_workflow`; implementation authority only, not submission or merge. |
| Explicit request to publish one named GitHub issue | Current request may satisfy exact external-write approval; no second ceremonial confirmation. |
| Merge request without explicit merge approval | Stop and request owner approval under existing Codex G gates. |
| Destructive cleanup with only general cleanup wording | Stop unless #713's exact standing exception applies. |
| Approval copied from an example or stale handoff | Reject as `unverifiable` or `stale`. |
| Approved path set expands during inspection | Stop as `scope_mismatch` and request refreshed authority. |
| Review passes but deploy was not approved | Deployment remains unauthorized. |
| New protected-surface behavior appears | Route to A/B for issue and contract authority. |
| Reviewer identifies a concrete in-contract defect | Use #682 packet and route E to D. |

Codex E must also verify the complete pairwise precedence matrix:

| Matching predicates | Required selected class |
| --- | --- |
| `prohibited_without_new_authority` and `consequential` | `prohibited_without_new_authority` |
| `prohibited_without_new_authority` and `scoped_workflow` | `prohibited_without_new_authority` |
| `prohibited_without_new_authority` and `routine_local` | `prohibited_without_new_authority` |
| `consequential` and `scoped_workflow` | `consequential` |
| `consequential` and `routine_local` | `consequential` |
| `scoped_workflow` and `routine_local` | `scoped_workflow` |
| No class can be proven from current evidence | `prohibited_without_new_authority` |

## Acceptance Criteria

- Issue #737 is the sole exact governance issue for this policy.
- ADR-0010 is the next unused ADR number and remains `Proposed`.
- Contract, ADR, and ADR index agree on scope and status.
- Action and approval vocabularies are closed and coherent.
- The exact precedence rule selects one class for every overlap and defaults
  unclassifiable actions to `prohibited_without_new_authority`.
- A clear current request is sufficient for routine work and may itself be the
  exact informed approval for a consequential action when material facts are
  present.
- Consequential authority fails closed on missing, stale, expired, revoked,
  superseded, consumed, mismatched, contradictory, or unverifiable authority.
- No later workflow gate is implied by an earlier gate.
- #713, #682, #650/#652, ADR-0008, and ADR-0009 status are preserved.
- No runtime, CI, validator, parser, analytics, workbook, webhook, Apps Script,
  frontend, AI, credential, external-service, deployment, or production
  behavior changes.
- Independent Codex E review is the next role.

## Open Questions And Risks

- A later implementation issue must decide the smallest authority-doc and
  template wording needed after ADR acceptance. This contract does not assume
  every governance surface needs duplicate language.
- The repository should avoid machine-validating natural-language approval
  unless repeated concrete failures justify a separate validator contract.
- ADR lifecycle promotion from `Proposed` to `Accepted` must follow current ADR
  policy and should not be inferred solely from a PR merge comment.

## Non-Claims

This contract and proposed ADR do not claim or grant:

- implementation authority;
- authority-doc, role-doc, template, skill, validator, or CI edit authority;
- protected-surface behavior authority;
- credential or permission authority;
- destructive-operation authority;
- external-write authority beyond the already completed issue publication;
- submission, merge, release, installation, deployment, canary, or production
  authority;
- parser, analytics, workbook, AI, or coaching truth;
- correctness, legal consent, security assurance, privacy assurance, release
  readiness, deploy readiness, or production readiness.

## Next Workflow Action

Next role: Codex E - Module Reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Independent Module Reviewer.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/737

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Branch:
codex/bounded-scope-informed-approval-737

Review:
- docs/contracts/governance_bounded_scope_and_informed_approval.md
- docs/decisions/ADR-0010-bounded-scope-and-informed-approval.md
- the ADR-0010 row in docs/decisions/README.md

Review goal:
Verify that the policy makes authority scope and informed approval explicit
without adding duplicate confirmation for clear low-risk requests. Confirm
that consequential actions still fail closed, approval cannot silently expand
or transfer, workflow gates remain separate, ADR-0008 and issues #713/#682/
#650/#652 are preserved, ADR-0009 remains proposed, and no runtime, protected,
external, merge, deploy, or production authority is granted.

Lead with findings. Route concrete docs defects to Codex D, policy ambiguity
to Codex B, framing errors to Codex A, and a clean reviewed package to Codex F.
Do not implement or submit changes during review.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/737"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue #737"
  target_artifact: "docs/contracts/governance_bounded_scope_and_informed_approval.md and proposed ADR-0010"
  risk_tier: "High workflow risk; no runtime behavior change"
  base_branch: "origin/main"
  target_branch: "main_after_independent_review_and_explicit_merge_approval"
  branch: "codex/bounded-scope-informed-approval-737"
  internal_project_area: "Quality / Governance"
  truth_owner: "repository coordination and workflow authority"
  bridge_code_status: "not_bridge_code"
  implementation_authorized: false
  authority_doc_edits_authorized: false
  template_edits_authorized: false
  ci_changes_authorized: false
  protected_surface_changes_authorized: false
  external_writes_authorized: false
  merge_authorized: false
  deployment_authorized: false
  readiness_claimed: false
  truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  validation:
    - "Fresh origin/main and live issue state revalidated."
    - "ADR-0010 confirmed as the next unused number."
    - "Docs-only validation recorded in the Codex B handoff."
  stop_conditions:
    - "Do not implement, submit, merge, deploy, or edit outside the reviewed docs package."
    - "Do not infer authority from approval evidence, review success, or proposed ADR status."
    - "Do not weaken existing protected-surface, E-to-D, checkout, WIP-1, or merge gates."
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "High workflow risk; no runtime behavior change"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "ADR-0004"
    - "ADR-0005"
    - "ADR-0008"
  proposed_adrs_read:
    - "ADR-0009"
  protected_surfaces:
    - "workflow authority"
    - "issue and PR lifecycle"
    - "branch and merge policy"
    - "validation and approval gates"
  authority_conflicts_found: false
  authority_conflict_notes: "No conflict; #737 records an explicit_user_override WIP-1 exception for this docs-only lane."
  stop_conditions:
    - "No runtime or protected-surface behavior changes."
    - "No authority-doc, role-doc, template, validator, CI, merge, or deploy changes."
    - "ADR-0010 remains Proposed pending independent review and integration."
```
