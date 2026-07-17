# ADR-0011: Role-Scoped Protected Mutations

Status: Proposed

Date: 2026-07-16

Decision owners / workflow role:

- Owner: authorized one GitHub issue and isolated docs-only ADR-0011 lane.
- Codex A: problem representation in issue #740.
- Codex B: governance contract and proposed ADR drafting.
- Codex E: required independent reviewer before any submission decision.

Related issues:

- <https://github.com/Tahjali11/Mythic-Edge/issues/740>
- <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- <https://github.com/Tahjali11/Mythic-Edge/issues/737>
- <https://github.com/Tahjali11/Mythic-Edge/issues/739>

Issue #739 remains a parked broader ADR-health review. It is not activated or
superseded by this proposal.

Related PRs:

- None. Submission is not authorized by issue #740.

Related contracts, handoffs, or review reports:

- `docs/contracts/governance_role_scoped_protected_mutations.md`
- Independent Codex E review: pending.

Related ADRs:

- `ADR-0001: Parser Owns Truth`
- `ADR-0004: Protected Surfaces And Schema-Change Policy`
- `ADR-0005: External Integration And Collaboration Surfaces`
- `ADR-0006: Repository Boundary Strategy`
- `ADR-0008: Repo WIP-1 Lane Activation Policy`
- `ADR-0010: Bounded Scope And Informed Approval` (`Proposed`,
  non-precedential)

## Context

ADR-0004 correctly requires explicit issue, contract, review, and validation
authority before semantic changes to protected surfaces. It also establishes
that path-based warnings are review signals rather than automatic permission
or automatic rejection.

The remaining ambiguity is the unit of protection. A repository, issue, file,
or topic may involve a protected surface while the current role merely frames,
contracts, inspects, or reviews. Treating that involvement as if every role
performs the mutation spreads protection across an entire lifecycle and makes
safe planning and review unnecessarily non-poolable or dedicated.

Local Role Pool design experience made this ambiguity visible, but the skill
is a tool surface and not repository authority. The durable repo decision must
stand independently of any current skill implementation or Stage 4 design.

The first failure point is classification by repository, issue, path, topic,
or lifecycle membership instead of by the intended semantic effect of the
current operation.

## Decision

A protected mutation is an intended change that alters a Mythic Edge truth
boundary, externally consumed interface, private-data boundary, irreversible
live state, or workflow-enforcement rule.

Protection attaches only to the role and operation performing that mutation.
It does not automatically attach to the repository, issue, file, topic, or
whole A-G lifecycle.

Mythic Edge uses exactly four surface classifications in this precedence:

1. `forbidden_effect`
2. `protected_mutation`
3. `guarded_path`
4. `none`

`forbidden_effect` means the current operation violates an existing hard
safety or authority boundary, including secret/private-artifact exposure or
an unauthorized destructive, credential, external-write, merge, integration,
deployment, or production action. The operation stops.

`protected_mutation` means the current operation intentionally changes a
protected semantic boundary. ADR-0004's existing issue, contract, review,
validation, schema, snapshot, drift, and forbidden-artifact requirements
remain applicable.

`guarded_path` means a sensitive path or subject requires explicit
classification and review attention, while current evidence shows that the
operation preserves protected semantics. Path contact alone is not permission,
rejection, or proof of a protected mutation.

`none` means no guarded path, protected mutation, or forbidden effect is
involved in the current operation.

Ambiguity creates no fifth status and grants no authority. Work stops before
the uncertain effect and routes to the role that owns the missing scope,
contract, finding, review, or integration decision.

The closed guarded/protected semantic category vocabulary is:

- `truth_boundary`
- `identity_reconciliation_or_deduplication`
- `externally_consumed_interface`
- `private_data_or_credential_boundary`
- `irreversible_live_state`
- `workflow_enforcement`

The closed, disjoint forbidden-effect category vocabulary is:

- `secret_or_private_artifact_exposure`
- `unauthorized_destructive_action`
- `unauthorized_credential_or_permission_action`
- `unauthorized_external_write`
- `unauthorized_merge_integration_or_deployment`
- `unauthorized_production_action`

When an existing workflow artifact records this decision, it may embed:

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

This is an embedded evidence vocabulary, not a required new packet, schema
validator, receipt, or service.

Its cross-field derivation is exact:

- `none` requires an empty category list and a `false` mutation boolean.
- `guarded_path` requires one or more semantic categories and a `false`
  mutation boolean.
- `protected_mutation` requires one or more semantic categories and a `true`
  mutation boolean.
- `forbidden_effect` requires one or more forbidden categories. Its mutation
  boolean is `true` only when the attempted operation would itself change
  protected semantics or persistent/external state; otherwise it is `false`.
  The boolean cannot lower the forbidden classification.

Undefined, empty-when-required, mixed-vocabulary, or contradictory values fail
closed and route to the role that owns the missing scope or authority. They do
not create a fifth level.

Role interpretation is operation-specific:

- A frames but does not implement the protected mutation.
- B contracts but does not implement the protected mutation.
- C performs the mutation when its implementation changes protected semantics.
- D performs the mutation only when its concrete fix changes protected
  semantics; a guarded topic or path is not sufficient.
- E reviews but does not apply the mutation in review-only mode.
- F submits the exact accepted diff but does not become the semantic author
  merely because the topic is protected; commit, push, and PR authority remain
  separate and mandatory.
- G readiness inspection is separate from merge, closure, integration,
  cleanup, release, and deployment effects. Those actual effects retain their
  existing explicit one-operation authority.
- H remains advisory and outside the normal A-G path.

For future Role Pool compatibility, a lane should be excluded for
protected-surface reasons only when the current role would perform a protected
mutation or forbidden effect. A guarded path, protected subject, or protected
operation in an earlier or later lifecycle role does not by itself make the
current lane non-poolable.

That compatibility rule does not itself make any lane poolable or dispatchable
and does not change the current role set. C remains dedicated, actual G
merge/closeout remains dedicated and explicitly authorized, and H remains
separate. All Role Pool stage, isolation, concurrency, mutation, submission,
and readiness gates remain independent.

## Scope

This ADR governs protected-surface classification and current-role routing for
future Mythic Edge repository workflow after acceptance.

It applies when issues, contracts, implementations, fixes, reviews,
submissions, integration checks, or advisory work mention or touch protected
surfaces.

It clarifies the unit of protection while preserving the authorization path.
It is intentionally compatible with a later separately authorized Role Pool
change, but it does not implement that change.

This ADR applies only to `Tahjali11/Mythic-Edge`. Sibling repositories require
their own adoption authority.

## Non-Goals

This ADR does not:

- edit ADR-0004 or immediately change its accepted status or metadata;
- weaken any ADR-0004 issue, contract, review, validation, schema, snapshot,
  drift, or forbidden-artifact requirement;
- make guarded paths unreviewed or make path warnings authoritative;
- authorize parser, state, identity, deduplication, workbook, webhook, Apps
  Script, analytics, frontend, AI, credential, environment, runtime, or
  deployment behavior changes;
- edit authority docs, role docs, templates, workflow docs, checkers,
  validators, tests, CI, schemas, or installed skills;
- change the Role Pool, dispatch agents, create claims, leases, reservations,
  or launches, or prove parallel execution;
- authorize Stage 4, arbitrary-repository execution, repository-code
  execution, broker/verifier work, canaries, or live readiness;
- authorize commit, push, PR, submission, merge, closure, release, deployment,
  production, credential, destructive, private-data, or external-write
  effects;
- make C, actual G merge/closeout, or H part of the current Role Pool; or
- declare this proposal accepted or ADR-0004 currently superseded.

## Alternatives Considered

- Keep protection attached to any issue that mentions a protected surface.
  Rejected because framing and review do not perform the semantic mutation.
- Treat every protected path touch as a protected mutation. Rejected because
  ADR-0004 already defines warnings as review signals, and invariant-preserving
  inspection, tests, docs, and refactors need a usable path.
- Make all A-G roles dedicated whenever one lifecycle step is protected.
  Rejected because authority and effects are role-specific; the approach adds
  ceremony without protecting the actual mutation more effectively.
- Remove protected-surface gates from read-only or planning roles. Rejected
  because guarded-path classification and review attention still matter even
  when the current role does not mutate.
- Implement the Role Pool and checker changes in this ADR lane. Rejected
  because proposal acceptance, repo-policy implementation, and installed-skill
  implementation are distinct decisions requiring separate authority.
- Expand Stage 4 to solve this routing ambiguity. Rejected because arbitrary
  repository or repo-code execution isolation is a different boundary from
  role-scoped classification on defined repositories.

## Consequences

Planning, contracting, review, and invariant-preserving fixes can be routed by
their actual operation instead of inheriting the highest risk of an entire
issue. This supports safe thread and Role Pool compression without weakening
the protected mutation itself.

Implementers and fixers must state whether their exact diff changes protected
semantics. Reviewers must verify that claim rather than relying only on path
names. Submitters and integrators retain their own external-effect gates.

The policy adds one classification decision when a guarded subject is
involved, but removes broader repository/issue/file/lifecycle contagion. No new
packet, service, validator, or mandatory serialized receipt is created.

Some operations will remain ambiguous until the diff or contract is clear.
Those cases stop before effect and route to A, B, D, E, or G rather than being
guessed as either safe or authorized.

## Truth Ownership Impact

This ADR changes no product truth ownership.

Parser/state continues to own event interpretation and normalized parser
facts. Workbook, webhook, Apps Script, analytics, UI, and AI retain their
existing downstream or scoped roles. Surface classification is workflow
evidence only; it is not parser truth, correctness, security assurance,
privacy assurance, readiness, merge authority, or deployment authority.

## Protected Surfaces Touched

This proposed ADR addresses the governance protected surfaces for
protected-surface policy, role routing, validation gates, and workflow
enforcement.

No runtime protected surface is changed. ADR-0004 remains the controlling
accepted policy while ADR-0011 is proposed.

This proposal does not authorize changes to parser behavior, parser state,
event classes, extraction, match/game identity, reconciliation,
deduplication, workbook schema, webhook payloads, Apps Script, secrets,
credentials, environment contracts, private data, raw logs, generated data,
runtime status, failed posts, workbook exports, external connections,
deployment, or production behavior.

## Validation Or Review Evidence

Codex A created issue #740 after confirming no exact open duplicate. Codex B
created the docs-only proposal in an isolated worktree from fresh
`origin/main@5a01b4237835f0e1edfe7f5ed16e5743987ff200` and confirmed ADR-0011
was unused.

Required local validation:

- `git diff --check`
- `py tools/check_agent_docs.py`
- path-list `py tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`
- path-list `py tools/check_secret_patterns.py --base origin/main --paths-from-stdin`
- exact three-file diff and unchanged ADR-0004 verification

Local results on 2026-07-16:

- agent-doc consistency: 54 files checked, 0 errors, 0 warnings;
- protected-surface gate: 3 changed paths, 0 forbidden, 0 warnings;
- secret/private-marker scan: 3 scanned paths, 0 forbidden, 0 warnings;
- tracked and new-file whitespace checks: no errors;
- exact changed-file, proposed-status, definition, role-binding, category,
  cross-field, unchanged ADR-0004, four-level precedence, closed-vocabulary,
  and no-fifth-status checks: passed.

Independent Codex E review remains required. This ADR remains `Proposed`, and
no validation result grants submission, acceptance, merge, deployment, Role
Pool implementation, Stage 4, or live-readiness authority.

## Supersedes

`ADR-0004: Protected Surfaces And Schema-Change Policy`, in part, only if this
ADR is later accepted.

The partial supersession is limited to the broad routing interpretation that a
protected repository, issue, path, topic, or lifecycle necessarily makes every
current role a protected mutator. ADR-0004's authorization, schema, snapshot,
drift, warning, validation, and forbidden-artifact rules remain in force.

## Superseded By

None.

## Follow-Ups

- Independent Codex E review of issue #740, the contract, this proposed ADR,
  and the index row.
- No Codex F submission unless the owner grants separate authority after E
  reports no blocking findings.
- If ADR-0011 is later accepted, use a separate reviewed lifecycle step to
  update ADR-0004's `Superseded By` metadata.
- Only after acceptance, create a separately scoped issue and contract for any
  compact authority-doc, role-doc, template, checker, or machine-rule changes.
- Treat any Role Pool adoption as a separate skill/repository contract. Do not
  couple it to Stage 4 unless that later scope actually requires arbitrary
  repository or repository-code execution.

## Notes

Issue #740's `explicit_user_override` WIP-1 exception expires when the exact
three-file proposal and validation are handed to independent Codex E. The
exception does not transfer to implementation, submission, merge, deployment,
Role Pool changes, Stage 4, or issue closure.
