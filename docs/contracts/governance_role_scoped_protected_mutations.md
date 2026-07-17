# Governance Contract: Role-Scoped Protected Mutations

## Module

Role-scoped protected-mutation classification and routing policy.

## Source Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/740>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related parked review:

- <https://github.com/Tahjali11/Mythic-Edge/issues/739>

Issue #739 remains parked. It does not authorize this contract and is not
activated, replaced, or closed by this lane.

## Owning Layer

Repository coordination and agent workflow.

## Internal Project Area

Quality / Governance.

## Truth Owner

Current repository authority owns protected-surface policy and role routing.
This contract defines a proposed policy vocabulary; it does not own parser,
workbook, transport, analytics, AI, security, privacy, merge, deployment, or
production truth.

## Bridge-Code Status

`not_bridge_code`

The installed Mythic Edge Role Pool is motivating tool-surface evidence only.
This contract does not change that skill, make it repository authority, or
claim that any role is dispatchable.

## Files Owned By This Contract

- `docs/contracts/governance_role_scoped_protected_mutations.md`
- `docs/decisions/ADR-0011-role-scoped-protected-mutations.md`
- the ADR-0011 index row in `docs/decisions/README.md`

No other file is owned or authorized by this contract.

## Public Interface

This contract defines:

- the term `protected mutation`;
- four `surface_classification.level` values;
- their precedence and fail-closed behavior;
- guarded/protected semantic and forbidden-effect categories;
- current-role routing rules;
- a minimum evidence shape for artifacts that record a classification; and
- compatibility requirements for a future Role Pool implementation issue.

It creates no runtime API, schema validator, serialized packet, receipt,
database, service, CI gate, or mandatory new artifact.

## Inputs

### Current operation

The exact action the current role proposes to perform, including its intended
behavioral effect and side effects.

### Current role

One of the existing Mythic Edge workflow roles A through G, or auxiliary role
H. Role identity does not grant authority by itself.

### Current authority

The applicable user instruction, repository governance, issue, contract,
accepted ADRs, reviewed diff, validation evidence, and role-specific gate.

### Changed or inspected paths

Paths are risk signals. A guarded path requires classification, but path
contact does not by itself prove a protected mutation or grant authority.

### Semantic effect

The intended change to truth ownership, externally consumed interfaces,
private-data boundaries, irreversible live state, or workflow enforcement.

## Outputs

When an existing workflow artifact records a surface classification, it uses
this minimum shape. The shape may be embedded in the issue, contract, handoff,
review, or PR; it does not require a new packet.

```yaml
surface_classification:
  level: none | guarded_path | protected_mutation | forbidden_effect
  categories: []
  current_role_performs_mutation: false
  evidence:
    issue: ""
    contract: ""
    reviewed_diff: ""
    validation: ""
```

The enclosing artifact already identifies the current role and operation.
Empty evidence fields are allowed only when that evidence is not applicable to
the current role. They must not be used to imply missing authority.

## Definitions

### Protected mutation

A protected mutation is an intended change that alters a Mythic Edge truth
boundary, externally consumed interface, private-data boundary, irreversible
live state, or workflow-enforcement rule.

Protection attaches only to the role and operation performing that mutation.
It does not automatically attach to the repository, issue, file, topic, or
whole A-G lifecycle.

### Guarded path

A guarded path is a sensitive file or subject whose involvement requires
explicit classification and review attention. It is a warning signal, not
automatic permission, automatic rejection, or proof that the current role
performs a protected mutation.

### Forbidden effect

A forbidden effect violates an existing hard safety or authority boundary.
Examples include exposing secrets or private artifacts and performing an
unauthorized destructive, credential, live external-write, merge,
integration, deployment, or production action.

An issue, contract, passing test, protected-path warning, or lower workflow
gate cannot convert a forbidden effect into an allowed one.

## Classification Levels And Precedence

Use exactly these levels:

1. `forbidden_effect`
2. `protected_mutation`
3. `guarded_path`
4. `none`

The first matching level in that order is selected.

### `forbidden_effect`

The current operation would violate an existing hard prohibition or lacks the
exact authority required for an irreversible or externally consequential
effect. The operation stops.

### `protected_mutation`

The current operation intentionally changes a protected semantic boundary.
ADR-0004's issue, contract, review, validation, schema, snapshot, drift, and
forbidden-artifact requirements remain applicable.

### `guarded_path`

The current operation touches or discusses a sensitive path or subject, but
current evidence shows that it preserves protected semantics. Review remains
required in proportion to the role; mutation authority is neither needed nor
granted solely because of the path.

### `none`

No guarded path, protected mutation, or forbidden effect is involved in the
current operation.

### Ambiguity

Ambiguity does not create a fifth level and does not default to permission.
The action stops before the uncertain effect and routes as follows:

- unclear scope or purpose routes to A;
- unclear interface, invariant, semantic boundary, or authority routes to B;
- a concrete implementation or CI finding routes to D;
- unclear reviewed-diff conformance routes to E; and
- merge, closure, integration, cleanup, or deployment ambiguity remains with
  G and requires its existing explicit authority.

## Categories

### Guarded/protected semantic categories

Use one or more of these categories when `level` is `guarded_path` or
`protected_mutation`:

- `truth_boundary`
- `identity_reconciliation_or_deduplication`
- `externally_consumed_interface`
- `private_data_or_credential_boundary`
- `irreversible_live_state`
- `workflow_enforcement`

Representative protected mutations include:

- changing parser/state truth ownership, event interpretation, normalized
  payload meaning, winner, play/draw, mulligan, or comparable parser facts;
- changing match/game identity, final reconciliation, or deduplication;
- changing workbook landing schema, webhook payload shape, or Apps Script
  receiver/upsert semantics;
- changing credential/environment contracts or private-data boundaries;
- changing branch, merge, deployment, validation, protected-surface, or other
  workflow-enforcement rules; and
- changing authorized irreversible live state.

### Forbidden-effect categories

Use one or more of these categories when `level` is `forbidden_effect`:

- `secret_or_private_artifact_exposure`
- `unauthorized_destructive_action`
- `unauthorized_credential_or_permission_action`
- `unauthorized_external_write`
- `unauthorized_merge_integration_or_deployment`
- `unauthorized_production_action`

Existing repository prohibitions define the boundary. This contract does not
weaken or exhaustively replace them.

### Cross-field derivation

The two category vocabularies are closed and disjoint. Derive the fields as
follows:

- `none` requires `categories: []` and
  `current_role_performs_mutation: false`.
- `guarded_path` requires one or more guarded/protected semantic categories
  and `current_role_performs_mutation: false`.
- `protected_mutation` requires one or more guarded/protected semantic
  categories and `current_role_performs_mutation: true`.
- `forbidden_effect` requires one or more forbidden-effect categories.
  `current_role_performs_mutation` is `true` only when the attempted operation
  would itself change protected semantics or persistent/external state; it is
  `false` for a prohibited access, inspection, disclosure, or exposure that
  performs no such mutation. This boolean never lowers the classification
  from `forbidden_effect`.

Undefined categories, an empty category list where one is required, mixed
semantic and forbidden categories, or a contradictory mutation boolean fail
closed and route to the role that owns the missing scope or authority. They do
not create a fifth level.

## Role-Scoped Decision Procedure

For every current role:

1. Name the exact current operation and its side effects.
2. Check hard prohibitions and exact consequential authority first.
3. Identify the intended semantic effect, not merely the repo, issue, topic,
   or path.
4. Determine whether the current role performs that semantic mutation.
5. Apply the classification precedence.
6. Apply all independent role, issue, contract, review, submission, merge,
   deployment, privacy, credential, and external-write gates.
7. Stop and route ambiguity before the uncertain effect.

Classification is operation-specific. A later operation in the same issue
must classify itself again; it does not inherit either permission or
prohibition from an earlier role by default.

## Role Matrix

| Role | Current operation | `current_role_performs_mutation` | Routing consequence |
| --- | --- | --- | --- |
| A | Frame scope, risk, and inspection order | `false` | Protected subject matter alone does not make A the mutator. A does not implement. |
| B | Define interfaces, invariants, authority, and tests | `false` | Contracting a protected change does not perform it. B does not implement. |
| C | Implement the contracted behavioral change | `true` only when the diff changes protected semantics | A protected C mutation requires the full protected workflow and dedicated implementation path. C remains outside the current Role Pool regardless. |
| D | Fix a concrete finding | Depends on the exact fix | A D fix is dedicated when it performs a protected mutation; an invariant-preserving targeted fix is not excluded merely by topic or path. |
| E | Independently inspect and review | `false` in review-only mode | Reviewing a protected diff does not apply the mutation. E must not silently fix code. |
| F | Stage and submit the exact accepted diff | `false` for semantic authorship | Protected topic alone does not make F the mutator. Commit, push, and PR effects still require exact reviewed scope and submission authority. |
| G | Inspect readiness | `false` for inspection | Readiness inspection does not merge or deploy and does not grant those effects. |
| G | Merge, close, integrate, clean up, release, or deploy | Effect-specific and consequential | Existing explicit one-operation G authority remains mandatory; actual G effects stay separate from inspection and from pooling eligibility. |
| H | Advisory governance synthesis | `false` | H remains advisory, does not edit authority, and remains outside the A-G path and current Role Pool. |

## Role Pool Compatibility Boundary

For a future separately authorized Role Pool change, protected-surface
eligibility should follow this rule:

> Exclude a lane for protected-surface reasons only when the current role
> would perform a protected mutation or forbidden effect. A guarded-path
> warning, protected subject, or earlier/later protected lifecycle operation
> does not by itself make the current lane non-poolable.

This rule does not itself make a lane poolable. Repository authority, the
current Role Pool contract, role inclusion/exclusion, issue/lane state,
dispatch readiness, isolation, concurrency, mutation, submission, and merge
gates remain separate.

In particular:

- A, B, D, E, and F remain subject to the Role Pool's independently accepted
  role and stage boundaries;
- C remains a dedicated issue implementation task;
- actual G merge/closeout remains dedicated and explicitly authorized;
- H remains separate; and
- Stage 4, arbitrary-repository execution, and repository-code execution are
  neither required nor authorized by this policy proposal.

## Worked Examples

### Guarded parser path, no semantic change

E reviews a diff in `state.py` and verifies that event interpretation and
reconciliation are unchanged.

```yaml
surface_classification:
  level: guarded_path
  categories:
    - truth_boundary
  current_role_performs_mutation: false
```

The path triggers review attention. E does not become the mutator.

### Protected parser mutation

C changes final winner reconciliation under an authorized issue and contract.

```yaml
surface_classification:
  level: protected_mutation
  categories:
    - truth_boundary
    - identity_reconciliation_or_deduplication
  current_role_performs_mutation: true
```

The full ADR-0004 authorization and validation path applies.

### Documentation about a webhook contract

B documents the existing webhook payload without changing its shape or
meaning.

```yaml
surface_classification:
  level: guarded_path
  categories:
    - externally_consumed_interface
  current_role_performs_mutation: false
```

The protected subject does not make the whole issue protected.

### Unauthorized live write

Any role attempts an unapproved live workbook write.

```yaml
surface_classification:
  level: forbidden_effect
  categories:
    - unauthorized_external_write
  current_role_performs_mutation: true
```

The operation stops. A lower-role success or passing validation cannot grant
the missing authority.

### Submitter handling an accepted protected diff

F receives exact E acceptance and separate submission authority for a
protected C diff.

The current semantic author remains C. F's operation is separately governed
by reviewed-scope, commit, push, and PR authority. Neither the protected topic
nor this classification grants F submission authority.

## Invariants

- Repository, issue, file, topic, and lifecycle membership are never
  sufficient by themselves to classify a protected mutation.
- Guarded-path warnings remain review signals, not permission or rejection.
- `current_role_performs_mutation: false` never grants authority to a later
  role or operation.
- `current_role_performs_mutation: true` never proves the mutation is
  authorized, correct, reviewed, safe, or ready.
- ADR-0004's semantic-change, schema, snapshot, drift, and forbidden-artifact
  safeguards remain in force.
- Protected classification never replaces submission, merge, deployment,
  credential, destructive, private-data, or external-write gates.
- Parser/state retains truth ownership.
- The most restrictive applicable classification wins.
- Ambiguity stops before effect and routes to the role that owns the missing
  decision.
- No status in this contract claims Role Pool dispatchability, Stage 4
  acceptance, security assurance, privacy assurance, live readiness, merge
  readiness, or deployment readiness.

## Error Behavior

- Missing current operation: stop and route to A.
- Missing or conflicting issue/contract authority: stop and route to B.
- Unknown semantic effect: stop before mutation; inspect or route to B.
- Protected mutation without ADR-0004 evidence: stop before implementation or
  submission.
- Forbidden effect: refuse the operation and name the applicable hard
  boundary without echoing sensitive content.
- Guarded-path warning without semantic analysis: do not classify the entire
  issue as protected; complete the analysis first.
- Later-role attempt to inherit earlier authority: fail closed and require the
  current role's own gate.
- Proposed ADR treated as accepted authority: fail closed; ADR-0011 remains
  non-precedential until accepted through the repository workflow.

## Governance Review Checklist

Independent E review must verify:

- all four levels and their precedence agree across issue, contract, ADR, and
  index summary;
- examples use only defined levels and categories;
- protected-mutation classification is semantic-effect-based and
  current-role-scoped;
- no path, repo, issue, topic, or lifecycle contagion remains;
- ADR-0004 safeguards are preserved;
- F/G effects retain separate authority;
- the Role Pool section is compatibility guidance, not implementation or
  readiness evidence;
- ADR-0004 is unchanged and ADR-0011 remains proposed;
- #739 remains parked;
- exactly the three authorized files changed; and
- no runtime, checker, validator, skill, Stage 4, CI, submission, merge, or
  deployment change occurred.

## Side Effects

Authorized side effects for this lane:

- one GitHub issue, #740, already created by the owner-authorized A step;
- one isolated local worktree and branch;
- the three docs changes named under Files Owned By This Contract; and
- local read-only validation output.

Not authorized:

- commit, push, PR, issue closure, tracker mutation, merge, deployment, or
  production activity;
- authority-doc, role-doc, template, checker, validator, CI, runtime, or skill
  changes; or
- claims of ADR acceptance or Role Pool readiness.

## Dependency Order

1. Publish issue #740 with the bounded WIP-1 exception.
2. Write this contract.
3. Write proposed ADR-0011 from this contract.
4. Add only the ADR-0011 index row.
5. Run local governance and documentation checks.
6. Hand the exact three-file diff to independent E review.

## Compatibility

This contract preserves:

- accepted ADR-0004's authorization and safety requirements;
- accepted ADR-0008's WIP-1 policy and recorded exception;
- proposed ADR-0010 as non-precedential context only;
- existing A-G and H role ownership;
- parser/state truth ownership;
- path-based protected warnings;
- secret/private/local artifact prohibitions; and
- separate submission, merge, deployment, and external-effect authority.

If ADR-0011 is later accepted, it partially supersedes only ADR-0004's broad
routing interpretation. It does not supersede ADR-0004's issue, contract,
review, validation, schema, snapshot, drift, or forbidden-artifact rules.

ADR-0004 must remain unchanged in this lane. Its `Superseded By` metadata may
be updated only through a later explicitly authorized lifecycle step after
ADR-0011 acceptance.

## Tests Required

No runtime tests are required because this lane changes no runtime behavior.

Required local checks:

```powershell
git diff --check
py tools/check_agent_docs.py
@'
docs/contracts/governance_role_scoped_protected_mutations.md
docs/decisions/ADR-0011-role-scoped-protected-mutations.md
docs/decisions/README.md
'@ | py tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/governance_role_scoped_protected_mutations.md
docs/decisions/ADR-0011-role-scoped-protected-mutations.md
docs/decisions/README.md
'@ | py tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

Local validation on 2026-07-16 against
`origin/main@5a01b4237835f0e1edfe7f5ed16e5743987ff200`:

- `git diff --check` -> exit 0;
- no-index `--check` for each new Markdown file -> no whitespace errors
  (`git diff --no-index` exit 1 is expected because each new file differs from
  `/dev/null`);
- `py tools/check_agent_docs.py` -> 54 files checked, 0 errors, 0 warnings;
- protected-surface path-list check -> 3 changed paths, 0 forbidden, 0
  warnings;
- secret/private-marker path-list check -> 3 scanned paths, 0 forbidden, 0
  warnings;
- exact changed-file, proposed-status, definition, role-binding, category,
  cross-field, and unchanged ADR-0004 mechanical check -> passed; and
- four-level precedence, closed-vocabulary, and no-fifth-status mechanical
  check -> passed.

Mechanical review must also confirm:

- exactly three changed files;
- ADR-0011 is the next unused number on fresh `origin/main`;
- ADR-0011 status is `Proposed`;
- ADR-0004 has no diff;
- the contract and ADR contain the same definition and precedence; and
- prohibited downstream scopes remain false.

## Acceptance Criteria

- The protected-mutation definition is exact and effect-based.
- Classification follows the current operation and current role.
- Exactly four levels exist with the required precedence.
- Guarded/protected semantic and forbidden categories are closed, disjoint,
  and mechanically consistent with the level and mutation boolean.
- Ambiguity fails closed without inventing a fifth status.
- The role matrix preserves A/B/E review and planning, identifies C/D
  mutation behavior, and keeps F/G/H boundaries explicit.
- Guarded paths do not contaminate a repo, issue, topic, or lifecycle.
- ADR-0004 safety gates remain intact.
- Role Pool guidance grants no dispatch, mutation, Stage 4, submission, merge,
  deployment, or readiness authority.
- Only the three authorized docs files change.
- Local validation passes or any failure is reported without submission.
- Independent E review is the next role.

## Next Workflow Action

Next role: Codex E, independent Module Reviewer.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: independent Module Reviewer for issue #740.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/740

Branch/worktree:
codex/role-scoped-protected-mutations-740

Contract:
docs/contracts/governance_role_scoped_protected_mutations.md

Proposed ADR:
docs/decisions/ADR-0011-role-scoped-protected-mutations.md

Review only the three-file diff against fresh origin/main. Verify the exact
four-level classification, precedence, closed category vocabularies,
cross-field derivation, role-scoped mutation rule, role matrix, ADR-0004
compatibility, ADR-0011 proposed status, unchanged ADR-0004, parked #739
boundary, and all non-claims. Confirm that path/topic/issue/lifecycle
involvement does not itself classify a protected mutation and that no
submission, Role Pool implementation, Stage 4, runtime, checker, CI, merge, or
deployment authority is implied. Do not edit files, submit, commit, push, open
a PR, merge, close issues, or implement downstream changes.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/740"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue #740"
  target_artifact: "independent review of the three-file ADR-0011 proposal"
  risk_tier: "High workflow/governance risk; no runtime behavior change"
  base_branch: "origin/main"
  target_branch: "codex/role-scoped-protected-mutations-740"
  validation:
    - "git diff --check"
    - "py tools/check_agent_docs.py"
    - "protected-surface path-list check"
    - "secret-pattern path-list check"
  stop_conditions:
    - "Review only; do not edit."
    - "Do not commit, push, open a PR, submit, merge, close, or deploy."
    - "Do not change ADR-0004, authority docs, checkers, skills, Role Pool behavior, Stage 4, or runtime behavior."
  implementation_authorized: false
  submission_authorized: false
  merge_authorized: false
  deployment_authorized: false
  role_pool_change_authorized: false
  stage4_authorized: false
  live_ready: false
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "B"
  risk_tier: "High workflow/governance risk; no runtime behavior change"
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
    - "ADR-0008"
  protected_surfaces:
    - "workflow protected-surface policy"
    - "role routing"
    - "validation and authorization gates"
  authority_conflicts_found: false
  authority_conflict_notes: "Issue #740 explicitly authorizes the proposed ADR-0011 lane while preserving ADR-0004 until later acceptance."
  stop_conditions:
    - "Exactly three docs files may change."
    - "ADR-0011 remains Proposed and ADR-0004 remains unchanged."
    - "No downstream implementation or submission."
```
