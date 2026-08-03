# ADR-0012: Long-Horizon Context And Delegation Discipline

Status: Accepted

Date: 2026-08-03

Decision owners / workflow role:

- Owner: activated issue #801 for proposal work and issue #805 for the
  separate acceptance lifecycle.
- Codex A: problem representation in issue #801 and acceptance framing in
  issue #805.
- Codex B: contract and proposed ADR drafting.
- Codex C: mechanical acceptance lifecycle implementation for issue #805.
- Codex E: independent source-package review completed; fresh independent
  review of the acceptance package remains required before submission.

Related issues:

- <https://github.com/Tahjali11/Mythic-Edge/issues/801>
- <https://github.com/Tahjali11/Mythic-Edge/issues/805>
- <https://github.com/Tahjali11/Mythic-Edge/issues/746>
- <https://github.com/Tahjali11/Mythic-Edge/issues/682>

Related PRs:

- <https://github.com/Tahjali11/Mythic-Edge/pull/802> - merged the original
  proposed package as `5b83dc33f933c6e58895277fb8bd9dfb5ab641bb`.
- <https://github.com/Tahjali11/Mythic-Edge/pull/804> - merged the reviewed
  finding-lifecycle correction as
  `4275dae6540f58827bf32e580b000846c5f021e4`.

Neither source PR accepted this ADR; both intentionally preserved its
`Proposed` status pending the separate issue #805 lifecycle.

Related contracts, handoffs, or review reports:

- `docs/contracts/governance_long_horizon_context_and_delegation_discipline.md`
- `docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md`
- `docs/contract_test_reports/governance_long_horizon_context_and_delegation_discipline.md`
- `docs/implementation_handoffs/governance_adr_0012_acceptance_lifecycle.md`
- Fresh independent Codex E review of the issue #805 acceptance package:
  pending.

Related ADRs:

- `ADR-0008: Repo WIP-1 Lane Activation Policy` (`Accepted`)
- `ADR-0010: Bounded Scope And Informed Approval` (`Proposed`)
- `ADR-0011: Role-Scoped Protected Mutations` (`Proposed`)

## Context

Mythic Edge work can continue across long conversations, interrupted tasks,
role handoffs, multiple worktrees, contract revisions, reviews, and merges.
Current governance already establishes WIP-1, durable artifacts, authority
precedence, fresh-context review, finding lifecycle, and bounded helper-agent
concepts. Those safeguards are distributed across several sources.

Issue #801 identified a consolidation gap: a future role can follow each
source independently yet miss their combined rule after material context or
lifecycle change. The gap concerns workflow authority and evidence, not
runtime behavior or proof that current work is unsafe.

## Decision

Mythic Edge adopts the following long-horizon discipline.

### 1. Material authority refresh

The active role refreshes current authority after resume or material context
separation, role handoff, merge, rebase, branch/base/head change, contract or
review revision, issue/PR/tracker/lane/finding state change, and immediately
before a consequential effect. Routine reads in one unchanged task do not
require repeated refresh.

Refresh proportionately revalidates repository and worktree identity, active
lane and ADR-0008 exception, current issue/PR state, governing contract and
accepted ADRs, finding dispositions, allowed and forbidden scope, unknowns,
and stop conditions. Ambiguity stops before effect.

### 2. Bounded current-context packet

The active role carries the smallest source-linked current packet needed for
its operation: repository and lane, role and risk, governing artifacts,
current findings, allowed and forbidden effects, verified facts, unknowns,
and stop conditions. Existing handoff and `instruction_context` structures may
carry it; no new schema is required.

Historical prompts, summaries, handoffs, local notes, worktrees, subagent
output, chat history, and model memory remain evidence. Presence in context
does not promote them to current authority.

### 3. Optional read-heavy subagents

Subagents are optional, primarily read-heavy evidence helpers for bounded
inspection, comparison, reproduction, coverage, or review lenses. The active
A-G/H role owns scope, authority interpretation, synthesis, judgment,
routing, validation, and the durable artifact. Material helper claims must be
verified against current sources.

Subagents do not become workflow roles, consume authority, change finding
lifecycle, widen scope, or make readiness decisions.

### 4. Exceptional parallel-write admission

Parallel writes are exceptional. Before they begin, current authority must
record disjoint file and semantic/interface ownership, absence of ambiguous
shared protected surfaces, named integration ownership and order, compatible
validation and overlap detection, conflict behavior, role boundaries, and
ADR-0008 compatibility. A second repository lane requires a named scoped
ADR-0008 exception.

Overlap, stale bases, unclear integration, or expired authority stops the
affected work. One successful parallel run creates no future permission.

### 5. Evidence-based finding reactivation

A fixed, superseded, deferred, rejected, not-reproduced, or closed finding can
become current only when a durable artifact records the finding ID, prior
disposition, new current evidence, either a changed condition or an explicit
correction basis showing that the prior disposition was erroneous because the
exact predicate remained unsatisfied, and the new lifecycle, blocking status,
owner, and route. Repetition in old context or an unchanged stale test is
insufficient. A correction uses the existing finding ID and does not claim that
the defect disappeared and later recurred. Earlier evidence remains preserved.

### 6. Durable workflow state

Current issues, contracts, ADRs, handoffs, reports, PRs, merge records,
trackers, and explicitly owned status artifacts carry workflow state. Chat
length, context retention, model memory, local summaries, and worktree names
do not. A mismatch is resolved by refreshing current durable sources and
recording the discrepancy.

### 7. Capability non-claim

Stronger models, larger context windows, successful subagent output,
successful parallel execution, or improved tools do not establish authority,
correctness, finding closure, review acceptance, submission or merge
readiness, deployment readiness, or permission to widen scope.

## Scope

This ADR governs long-horizon authority refresh, context handoff, subagent
delegation, parallel-write admission, finding reactivation, and durable
workflow state for `Tahjali11/Mythic-Edge`.

It extends ADR-0008's WIP-1 policy without superseding it. Sibling repositories
require their own adoption authority.

## Non-Goals

This ADR does not:

- make refresh mandatory before every trivial read;
- require subagents, parallel execution, or a new workflow role;
- create a packet schema, validator, context database, scheduler, broker,
  service, receipt, or enforcement engine;
- authorize parallel writes, protected mutations, external effects, or
  another active lane by implication;
- edit or accept ADR-0010 or ADR-0011;
- rewrite the #682 contract or historical findings;
- change parser, state, analytics, frontend, workbook, transport, credential,
  runtime, Role Pool, CI, release, deployment, or production behavior; or
- authorize submission, merge, issue closure, deployment, or readiness.

## Alternatives Considered

- Keep the rules distributed. Rejected because their combined application can
  be missed after material transitions.
- Require full-history replay on every resume. Rejected because it increases
  ceremony and can promote stale evidence over current authority.
- Require subagents for long tasks. Rejected because delegation is optional
  and capability does not establish need or authority.
- Ban all parallel writes. Rejected because ADR-0008 already permits explicit
  scoped exceptions; this decision defines a safer exceptional admission.
- Build enforcement now. Rejected because no current evidence justifies a new
  validator, schema, service, or execution system.

## Consequences

Long-running tasks gain finite refresh points and smaller, more reliable
handoffs. Historical evidence remains available without silently controlling
current work. Helper agents and parallel writes receive clearer boundaries,
and closed findings cannot return without evidence.

The cost is added revalidation at material transitions and more explicit
coordination for parallel writes. Routine unchanged work remains unaffected,
and existing artifacts are reused rather than replaced.

## Truth Ownership Impact

This ADR changes no product truth ownership. Parser/state, analytics,
workbook, transport, UI, AI, and collaboration boundaries remain unchanged.
Context packets, subagent output, and finding transitions are workflow
evidence only.

## Protected Surfaces Touched

This ADR addresses workflow authority, lane activation, role delegation,
finding lifecycle, validation responsibility, and integration coordination.
It changes no runtime protected surface and authorizes no protected mutation.

ADR-0008 remains the controlling Accepted WIP-1 policy. ADR-0010 and ADR-0011
remain Proposed and non-precedential.

## Validation Or Review Evidence

Codex B drafted the original exact three-path package from
`origin/main@be840bc1160678a9678d792d3cfd6074ac86ebca`. Independent Codex E
review accepted the source package. PR #802 merged it as
`5b83dc33f933c6e58895277fb8bd9dfb5ab641bb` with all six checks passing while
preserving `Proposed` status.

PR #804 merged the independently reviewed finding-lifecycle correction as
`4275dae6540f58827bf32e580b000846c5f021e4`, again with all six checks
passing. The #801 closeout records all five review threads across PRs #802 and
#804 resolved, closes #801 as completed, and clears its WIP-1 lane. Neither
merge accepted ADR-0012.

Issue #805 owns the separate mechanical acceptance lifecycle. The owner
explicitly activated its exact three-file Codex C implementation from current
`origin/main@4275dae6540f58827bf32e580b000846c5f021e4`. The implementation
changes only lifecycle status and completed provenance; it leaves the source
contract and historical review report unchanged. Fresh independent Codex E
review remains required before submission of this acceptance package.

## Supersedes

None. ADR-0008 remains Accepted and unsuperseded.

## Superseded By

None.

## Follow-Ups

- Fresh independent Codex E review of the exact issue #805 acceptance package.
- Codex F submission only after E reports no blocking findings and the owner
  separately authorizes submission.
- Codex G integration and issue closeout only after explicit owner approval.
- Any governance-enforcement implementation requires its own issue, contract,
  review, and authority.

## Notes

The #801 ADR-0008 exception expired when its proposal and correction work
merged and issue #801 closed. Issue #805 records only the separate acceptance
lifecycle and does not transfer subagent, parallel-write, enforcement,
submission, merge, deployment, Role Pool, or readiness authority. Issue #803
remains queued and inactive.
