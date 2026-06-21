# ADR-0008: Repo WIP-1 Lane Activation Policy

Status: Proposed

Date: 2026-06-21

Decision owners / workflow role:

- Codex H: Constitutional Lawyer synthesis for issue #543.
- Codex B: Module Contract Writer for
  `docs/contracts/repo_wip_1_lane_activation_policy.md`.
- Codex C: Module Implementer for this proposed docs-only governance package.

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/543

Related PRs:

- TBD

Related contracts, handoffs, or review reports:

- `docs/contracts/repo_wip_1_lane_activation_policy.md`
- `docs/implementation_handoffs/repo_wip_1_lane_activation_policy_comparison.md`

Related ADRs:

- `ADR-0004: Protected Surfaces And Schema-Change Policy`
- `ADR-0005: External Integration And Collaboration Surfaces`
- `ADR-0006: Repository Boundary Strategy`

## Context

Mythic Edge uses role-scoped Codex threads, GitHub issues, PRs, contracts,
handoffs, local worktrees, and occasional sibling repositories. That workflow
has enough moving parts that multiple lanes can look valid at the same time:
a stale prompt, parked worktree, tracker-selected next item, open PR, or local
status note can all appear to be the current lane.

Issue #543 identified the coordination risk: silent parallel lane activation
creates stale handoffs, duplicate prompts, unclear ownership, and cleanup
burden. Current governance already protects role boundaries, issue lifecycle,
PR lifecycle, tracker hygiene, repository identity, and protected surfaces, but
it does not define a repo-level active work slot.

This proposed ADR records a WIP-1 default for Mythic Edge repository work while
preserving narrow, named exceptions for urgent or explicitly authorized
parallel work.

## Decision

Each Mythic Edge repository defaults to one active issue or lane at a time.

The active slot is repository scoped, not worktree scoped. GitHub issue state,
PR state, branch heads, merge commits, current contracts, accepted ADRs, and
repo governance docs outrank local workflow indexes, parked notes, stale
prompts, local Codex skills, chat memory, and local worktree names.

A second active lane may start only when a named exception is recorded with the
repository, reason, allowed scope, linked active or blocked issue or PR when
applicable, authorization source, record location, and expiration condition.

The canonical exception names are:

- `security_hotfix`
- `privacy_or_raw_log_leak`
- `data_loss_or_corruption`
- `ci_blocking_all_work`
- `dependency_security_update`
- `blocked_lane_unblocker`
- `repo_bootstrap_or_split`
- `explicit_user_override`

Parked or deferred issues do not count as active WIP only when the no-current
work state is explicit and no active PR, implementation, review, submission,
deployment, or closeout work is expected.

A tracker-selected next lane is queued work. It does not occupy the active slot
until a user or current workflow artifact starts it or explicitly assigns it
the active slot.

An active PR normally keeps the source lane active until the PR is merged,
closed, or explicitly parked or deferred.

## Scope

This ADR governs repository coordination and agent workflow for
`Tahjali11/Mythic-Edge`.

It applies to future issues, contracts, handoffs, reviews, PR descriptions,
tracker comments, and local prompts that activate, park, defer, unblock, or
close a Mythic Edge lane.

The wording is intentionally portable to sibling Mythic Edge repositories, but
this ADR does not adopt the policy inside any sibling repository.

## Non-Goals

This ADR does not:

- change parser behavior
- change parser state final reconciliation
- change parser event classes
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- change analytics behavior
- change OpenAI or model-provider behavior
- change AI or coaching behavior
- change CI gates
- change release, deploy, merge, or production behavior
- create sibling-repo adoption issues or PRs
- rewrite historical issue comments, PR bodies, or old handoffs
- make local worktrees, local status indexes, local skills, stale prompts, or
  chat memory authoritative over GitHub and repo governance
- make WIP-1 an unbreakable hard stop for urgent safety or explicit user
  override cases

## Alternatives Considered

- Keep relying on informal tracker and handoff discipline. Rejected because it
  does not prevent stale prompts or local worktrees from silently acting like
  repo authority.
- Ban all parallel work with no exceptions. Rejected because security,
  privacy, data-loss, CI-blocking, dependency-security, unblocker, bootstrap,
  and direct user-override cases need a safe escape hatch.
- Treat a local worktree as the active lane. Rejected because local checkout
  names are machine-local evidence, not repository authority.
- Adopt sibling repositories in the same change. Rejected because each
  repository needs its own repo-scoped handoff or explicit authorization.

## Consequences

Future threads have a start gate before activating new repo work. They should
identify the active lane, decide whether a queued item is only queued, and
record exceptions when a second lane is necessary.

The benefit is less duplicate work, fewer stale handoffs, clearer ownership,
and safer cross-repo coordination. The cost is added intake ceremony for
high-risk workflow lanes. That cost is justified because WIP drift can lead to
wrong branches, wrong issues, accidental sibling-repo mutation, and stale
review or submission prompts.

## Truth Ownership Impact

This ADR clarifies workflow authority only. It does not change parser truth,
workbook truth, analytics truth, AI truth, merge readiness, deploy readiness,
or production truth.

Repo authority for lane activation remains with current user instructions,
`AGENTS.md`, `docs/agent_rules.yml`, `docs/agent_constitution.md`, current
GitHub issues, current contracts, accepted ADRs, reviewed PRs, and merge
evidence.

## Protected Surfaces Touched

No runtime protected surfaces are touched by this ADR.

This ADR does not authorize changes to parser behavior, parser state final
reconciliation, parser event classes, workbook schema, webhook payload shape,
Apps Script behavior, analytics behavior, AI/model-provider behavior, CI
gates, release policy, deploy policy, production behavior, secrets, raw logs,
generated artifacts, private artifacts, or local-only files.

## Validation Or Review Evidence

This ADR adoption slice is docs-only. Runtime tests are not required because no
runtime code changed.

Expected implementation validation is recorded in
`docs/implementation_handoffs/repo_wip_1_lane_activation_policy_comparison.md`.

## Supersedes

None.

## Superseded By

None.

## Follow-Ups

- Review this proposed ADR through the normal Codex E, F, and G path before
  treating it as accepted durable precedent.
- Consider a later inventory pass for currently open lanes after adoption.
- Consider future sibling-repo adoption issues only after this repo policy is
  reviewed and merged.
- Consider a future warning tool for WIP-1 conflicts, but keep GitHub and repo
  governance authoritative.

## Notes

The `explicit_user_override` exception is intentionally valid, but it still
needs scope, record location, and expiration metadata so it does not become
silent parallelization.
