# ADR-0010: Bounded Scope And Informed Approval

Status: Proposed

Date: 2026-07-16

Decision owners / workflow role:

- Owner: authorized issue publication and Codex B contract/ADR drafting.
- Codex A: governance problem representation.
- Codex B: Module Contract Writer for issue #737.
- Codex E: required independent reviewer before submission.

Related issues:

- <https://github.com/Tahjali11/Mythic-Edge/issues/737>
- <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- <https://github.com/Tahjali11/Mythic-Edge/issues/713>
- <https://github.com/Tahjali11/Mythic-Edge/issues/682>
- <https://github.com/Tahjali11/Mythic-Edge/issues/650>
- <https://github.com/Tahjali11/Mythic-Edge/issues/652>

Related PRs:

- TBD

Related contracts, handoffs, or review reports:

- `docs/contracts/governance_bounded_scope_and_informed_approval.md`
- `docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md`
- `docs/contracts/governance_review_pattern_template_checklist_adoption.md`

Related ADRs:

- `ADR-0004: Protected Surfaces And Schema-Change Policy`
- `ADR-0005: External Integration And Collaboration Surfaces`
- `ADR-0008: Repo WIP-1 Lane Activation Policy`
- `ADR-0009: Optional Dependency Provider Model` (`Proposed`,
  non-precedential)

## Context

Mythic Edge separates problem framing, contracting, implementation, review,
submission, merge, deployment, and protected-state authority. This protects a
personal but production-adjacent data pipeline from stale prompts, accidental
scope expansion, truth-ownership drift, private-data exposure, and external or
destructive actions that the owner did not intend.

Experience across those gates also shows a second failure mode: repeating
approval language and creating new packets can become ceremony when the
current request already clearly authorizes local, reversible, bounded work.
Excess ceremony obscures the few approvals that actually protect consequential
state.

Issue #737 therefore requires one durable policy that keeps consequential
authority exact while making the low-risk path proportionate.

## Decision

Mythic Edge adopts bounded scope and informed approval as a workflow policy.

Every action is limited by its applicable repository, issue or purpose, active
role, allowed operation, allowed artifacts or surfaces, forbidden operations,
side effects, lifecycle, validation or rollback boundary, and next gate.
Unspecified consequential authority is false.

Actions are classified as:

- `routine_local`: clear current request, local, reversible, within role, and
  outside protected, credentialed, destructive, external-write, merge,
  deployment, and production surfaces;
- `scoped_workflow`: durable work already bounded by the current issue,
  contract, role, and artifacts;
- `consequential`: protected, credentialed, destructive, external-write,
  issue-closing, merge, release, publication, installation, service,
  deployment, canary, production, or materially scope-expanding work;
- `prohibited_without_new_authority`: work outside current framing or contract,
  conflicting with higher authority, moving truth ownership, or missing a
  required protected-surface gate.

Classification uses this exact highest-to-lowest precedence:

1. `prohibited_without_new_authority`
2. `consequential`
3. `scoped_workflow`
4. `routine_local`

The first matching predicate is the selected class. An action matching more
than one description therefore receives the most restrictive applicable
class. If current evidence cannot prove any class, the action defaults to
`prohibited_without_new_authority`. An issue or contract can bound an action
without reducing a protected or external action from `consequential` to
`scoped_workflow`.

A clear current request is sufficient for `routine_local` work. Existing issue
and contract authority is sufficient for only the current operation in
`scoped_workflow` work. `Consequential` work requires exact informed approval
before the effect. The current user instruction can itself be that approval
when the material action, target, effects, risks, reversibility, validation,
lifecycle, and remaining exclusions are already understandable. No magic
phrase or duplicate confirmation is required.

Approval does not transfer by default across repositories, issues, roles,
operations, paths, protected surfaces, external targets, versions, or
lifecycles. Missing, stale, expired, revoked, superseded, consumed,
scope-mismatched, contradictory, or unverifiable authority fails closed.

Evidence, permission, role readiness, implementation conformance, review
acceptance, submission authority, merge authority, deployment authority,
truth, and assurance remain separate. Passing one gate never silently grants
the next.

Use existing issues, contracts, handoffs, reviews, comments, and current user
instructions to record authority. Do not create a new packet, schema, receipt,
or validator merely to restate an existing adequate boundary.

## Scope

This ADR governs future workflow authority and approval interpretation inside
`Tahjali11/Mythic-Edge` after acceptance.

It applies to issue, contract, implementation, review, submission, merge,
checkout, external-write, credential, protected-surface, deployment, canary,
and production gates according to their existing owners.

It clarifies how much approval evidence is necessary. It does not replace the
A-G workflow, current authority order, issues, contracts, protected-surface
rules, or role-specific gates.

## Non-Goals

This ADR does not:

- require a serialized approval packet for every action;
- require a second confirmation when the current request is already clear and
  informed;
- create a validator, token, receipt, approval service, database, or runtime
  state;
- authorize implementation, authority-doc edits, template edits, CI changes,
  protected-surface changes, credentials, private evidence, external writes,
  destructive operations, submission, merge, release, deployment, canary, or
  production activity;
- weaken parser truth ownership, protected-surface contracts, Codex E review,
  Codex D blocker packets, Codex F staging, Codex G merge/deploy gates, or
  checkout-cleanup protections;
- decide legal consent, security assurance, privacy assurance, correctness,
  release readiness, deploy readiness, or production readiness;
- accept, reject, or supersede proposed ADR-0009.

## Alternatives Considered

- Require a complete approval packet for every mutation. Rejected because it
  adds high ceremony to ordinary local work and makes meaningful approvals
  harder to distinguish.
- Treat any user request as unlimited authority for the whole workflow.
  Rejected because implementation, review, submission, merge, deployment, and
  protected effects are different decisions.
- Use approval keywords as the validity test. Rejected because informed scope
  and material effects matter more than a magic phrase.
- Leave approval boundaries issue-specific. Rejected because the same
  scope-expansion and redundant-confirmation failures recur across modules.
- Build a machine validator immediately. Rejected because natural-language
  intent and current authority order require judgment, and no evidence yet
  justifies a new mandatory gate.

## Consequences

Clear low-risk requests can proceed without duplicate confirmation. Codex must
still stop when inspection reveals a material effect the owner did not
reasonably approve.

Consequential actions gain a consistent plain-English disclosure boundary.
Approvals become easier to review because they name the current action and
what remains unauthorized.

The policy adds some documentation burden to high-risk cross-thread work, but
reuses existing issues, contracts, handoffs, and comments rather than creating
a parallel approval system.

Future reviewers must classify whether an action is routine, scoped,
consequential, or prohibited. Ambiguity that changes the required approval
routes to Codex A or B instead of being guessed.

## Truth Ownership Impact

This ADR changes no product truth ownership.

Parser/state continues to own event interpretation and normalized parser
facts. Analytics, workbook, transport, UI, AI, and collaboration surfaces
retain their existing downstream or scoped ownership. Approval evidence is
workflow evidence only; it is not parser truth, analytics truth, security
assurance, privacy assurance, or readiness truth.

## Protected Surfaces Touched

Workflow authority, issue/PR lifecycle, branch/merge policy, and validation
gates are governance protected surfaces addressed by this proposed policy.

No runtime protected surface is changed. This ADR does not authorize parser,
state, identity, deduplication, analytics, SQLite, workbook, webhook, Apps
Script, frontend, credential, environment, external integration, deployment,
or production changes.

ADR-0004 remains the controlling protected-surface policy. ADR-0005 remains the
controlling external-integration boundary. ADR-0008 remains the controlling
WIP-1 and named-exception policy.

## Validation Or Review Evidence

Codex B created the proposed ADR on a clean isolated branch at fresh
`origin/main`, confirmed ADR-0010 was unused, and confirmed issue #737 was the
only exact duplicate-search match.

Required docs validation and independent Codex E review are recorded in
`docs/contracts/governance_bounded_scope_and_informed_approval.md`.

This ADR remains `Proposed`. No runtime validation, implementation authority,
merge authority, deployment authority, or acceptance is implied by its
existence.

## Supersedes

None.

## Superseded By

None.

## Follow-Ups

- Independent Codex E review of issue #737, its contract, this ADR, and the ADR
  index row.
- Codex F submission only after review has no blocking findings.
- Codex G integration only after explicit owner approval.
- After merge, use the current ADR lifecycle policy to record `Accepted` in a
  separately reviewed repository change.
- Only after acceptance, create a separately scoped issue if compact changes
  to authority docs, role docs, templates, skills, or machine rules are needed.
- Do not create an approval validator unless repeated concrete failures justify
  its own issue, contract, and proportionality review.

## Notes

Issue #713 remains the checkout-reconciliation lane. Issue #682 remains the
E-to-D blocker-packet and helper-agent lane. Issues #650/#652 remain the
review-template adoption lane. This ADR clarifies their common authority
principle without replacing their narrower mechanics.
