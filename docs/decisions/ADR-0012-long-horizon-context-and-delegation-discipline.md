# ADR-0012: Long-Horizon Context And Delegation Discipline

Status: Proposed

Date: 2026-08-03

Decision owners / workflow role:

- Owner: activated issue #801 under a scoped ADR-0008
  `explicit_user_override`.
- Codex A: problem representation in issue #801.
- Codex B: contract and proposed ADR drafting.
- Codex E: required independent reviewer before submission.

Related issues:

- <https://github.com/Tahjali11/Mythic-Edge/issues/801>
- <https://github.com/Tahjali11/Mythic-Edge/issues/746>
- <https://github.com/Tahjali11/Mythic-Edge/issues/682>

Related PRs:

- None. Submission is not authorized.

Related contracts, handoffs, or review reports:

- `docs/contracts/governance_long_horizon_context_and_delegation_discipline.md`
- `docs/contracts/governance_subagent_boundaries_e_to_d_blocker_packets_project_hygiene.md`
- Independent Codex E review: pending.

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

Mythic Edge adopts the following long-horizon discipline if this ADR is later
accepted.

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
disposition, new current evidence, changed condition, and new lifecycle,
blocking status, owner, and route. Repetition in old context or an unchanged
stale test is insufficient. Earlier evidence remains preserved.

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
workflow state for `Tahjali11/Mythic-Edge` after acceptance.

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

This proposal addresses workflow authority, lane activation, role delegation,
finding lifecycle, validation responsibility, and integration coordination.
It changes no runtime protected surface and authorizes no protected mutation.

ADR-0008 remains the controlling Accepted WIP-1 policy. ADR-0010 and ADR-0011
remain Proposed and non-precedential.

## Validation Or Review Evidence

Codex B drafted the exact three-path documentation package in a clean worktree
from `origin/main@be840bc1160678a9678d792d3cfd6074ac86ebca` after verifying:

- issue #801 and its owner activation remain current;
- ADR-0012 is unused;
- duplicate searches return only issue #801;
- PR #800 touches none of the three authorized paths; and
- ADR-0008, ADR-0010, ADR-0011, and the #682 source lifecycle are unchanged.

Required local docs, protected-surface, private-marker, validation-selection,
path, lifecycle, ASCII, whitespace, and final-newline checks are specified in
the owning contract. Independent Codex E review remains required. This ADR is
`Proposed`; validation does not make it precedent.

## Supersedes

None. ADR-0008 remains Accepted and unsuperseded.

## Superseded By

None.

## Follow-Ups

- Fresh independent Codex E review of issue #801, the contract, this proposed
  ADR, and the index row.
- Codex F submission only after E reports no blocking findings and the owner
  separately authorizes submission.
- Codex G integration only after explicit owner approval.
- Any later acceptance or governance-enforcement implementation requires its
  own reviewed lifecycle and authority.

## Notes

The #801 ADR-0008 exception expires under its activation record. It does not
transfer subagent, parallel-write, submission, merge, deployment, Role Pool,
or readiness authority.
