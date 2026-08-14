# Mythic Edge Issue-Wave Interface And Checkout-Family Resolution

## Summary

The issue-wave coordinator needs one coherent correction at its public input
and local-checkout boundaries. The accepted public vocabulary is
`mythicedgeissuewave`, role or segment notation such as `(A;)`, and canonical,
full-name, or documented short repository selectors. After accepting that
input, Inspect must recognize one Git checkout family rather than treating a
primary checkout and its registered task worktrees as independent clones.

## Source Issue

- <https://github.com/Tahjali11/Mythic-Edge/issues/859>
- Title: `[governance][issue-wave] Normalize invocation and resolve checkout families`
- State at framing: open on 2026-08-14.

Historical issues #855 and #857 are closed evidence only. They do not supply
current authority for this correction.

## Tracker

N/A.

## Lane Activation

```yaml
lane_activation:
  repo: "Tahjali11/Mythic-Edge"
  active_issue_or_lane: "issue #859"
  lane_status: "active_second_lane_under_explicit_user_override"
  tracker_selected_next_lane: ""
  exception:
    name: "explicit_user_override"
    blocked_active_issue_or_pr: "open PRs #374 and #391"
    reason: "The owner authorized one bounded issue-wave interface and checkout-family correction through G readiness."
    allowed_scope: "Issue-wave invocation aliases, repository aliases, read-only checkout inventory, exact coordinator rules, tests, source documentation, one guarded skill sync, one read-only Inspect, draft PR submission, and G verification."
    expiration_condition: "Issue #859 merge and closeout, explicit park/cancel/reassignment, or owner revocation."
    authorized_by: "Human owner in the current Codex task on 2026-08-14"
    recorded_in: "GitHub issue #859 and this problem representation"
```

## Intended Behavior

- `mythicedgeissuewave Inspect (A;)` is the preferred read-only invocation.
- `$mythic-edge-issue-wave` remains backward compatible.
- `repos=` and `anchor=` accept canonical owner/repository identities, full
  repository names, and the exact documented suffix after `Mythic-Edge-`.
- For each selected repository, one usable checkout family consists of Git's
  registered primary worktree and every linked worktree sharing its resolved
  Git common directory, including registered worktrees outside the workspace.
- A worktree authoritatively bound to one current issue causes the duplicate-
  work gate to exclude only that exact issue. It does not exclude other issues
  from independent WIP-1, prerequisite, authority, dependency, or scope
  checks.
- A clean historical worktree with no current active-work evidence is ignored.
- Multiple independent Git stores, missing required checkouts, or active-
  looking work without exactly one authoritative issue binding fail closed.

## Actual Behavior

The pending nomenclature implementation accepts the new command, selector,
and semicolon vocabulary, but the controller protocol still requires exactly
one local checkout and forbids the helper from reading Git. As a result, a
primary checkout plus ordinary registered task worktrees can be classified as
ambiguous before issue-level eligibility is evaluated.

## First Proven Failure Point

The controller's checkout-matching rule counts working folders instead of
grouping them by Git common-directory identity. It therefore conflates two
different conditions:

1. one Git store with several registered worktrees; and
2. several independent Git stores that happen to use the same remote.

Only the second condition is genuine checkout ambiguity.

## Project Layer

Repository coordination and agent workflow.

## Internal Project Area

Quality / Governance, with Git and GitHub as read-only evidence surfaces for
Inspect.

## Inputs

- one accepted issue-wave invocation;
- a resolved workspace root known to the coordinator;
- one or more canonical repositories selected by the invocation;
- local Git metadata from direct workspace children and Git-registered linked
  worktrees;
- current PR, issue, non-final issue-wave ledger, contract, and handoff
  evidence used by the root coordinator for binding.

## Expected Output

- the existing canonical invocation object, unchanged in schema;
- one ephemeral `mythic_edge_issue_wave_checkout_inventory.v1` object used
  only in memory;
- separate Inspect reasons for checkout identity, exact active-issue
  exclusion, WIP incompatibility, dependencies, authority, and scope;
- zero to three dependency-safe lanes, with zero remaining valid when the
  independent gates genuinely exclude every issue.

## Scope

In scope:

- the pending invocation and repository-alias package;
- a bounded `inventory-checkouts` helper operation;
- checkout-family and issue-binding protocol rules;
- temporary real-Git contract tests;
- the current issue-wave contract, source instructions, metadata, repo skill
  documentation, implementation handoff, and independent review report;
- one exact, rollback-capable synchronization of only the installed
  `mythic-edge-issue-wave` after E approval;
- one source-loaded and one installed read-only Inspect;
- exact-package F submission and G readiness verification.

Out of scope:

- a user-facing path option or persistent checkout mapping;
- independent clones outside the workspace search boundary;
- the legacy Role Pool, any R0-bound file, installer implementation, saved-run
  schemas, Dispatch authority, credentials, deployment, production behavior,
  issue closure, merge, or unrelated cleanup.

## Governance And Truth Boundaries

The helper owns only deterministic local Git inventory. It does not own issue
identity, active-work truth, WIP policy, eligibility, dependency completion,
scope safety, selection, or authority. The root coordinator binds worktrees
using current GitHub and durable repo evidence, then applies the independent
gates.

Branch and folder issue numbers are query hints only. They are never an
authoritative issue binding by themselves.

## Risks And Likely Breakpoints

- raw remote URLs could leak embedded credentials;
- a read-only-looking Git command could refresh an index or alter optional
  locks;
- one family could be split when the primary and linked worktrees use path
  aliases;
- two independent clones could be merged merely because their remotes match;
- a dirty or ahead worktree could be treated as historical without a binding;
- issue-level duplicate exclusion could accidentally waive WIP-1 or scope
  conflicts for unrelated issues;
- checkout inventory could drift into saved-run or public handoff schemas.

## Validation Evidence Needed

- contract-first failures at the missing inventory operation and binding rule;
- real Git repositories covering internal and external linked worktrees,
  dirty/untracked/ahead/detached state, independent clones, fetch/push
  mismatch, missing repositories, path aliases, stale registrations, failures,
  timeouts, credential-safe remotes, and before/after byte identity;
- complete issue-wave and installer suites, lint, agent-document,
  protected-surface, secret-pattern, and diff checks;
- source-loaded live Inspect with unchanged local and GitHub state;
- fresh independent E approval before installation or submission;
- source/installed byte equality and installed read-only Inspect;
- F package binding and G checks/review-thread/issue/WIP verification.

## Open Questions

The draft PR base remains undecided. Targeting `main` requires the explicit
permission required by current repository authority; implementation and E
review can proceed without assuming that permission.

## Next Workflow Action

Next role: Codex B, Module Contract Writer.

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "#859"
  tracker: "N/A"
  completed_thread: "A"
  next_thread: "B"
  source_artifact: "docs/problem_representations/mythic_edge_issue_wave_interface_checkout_resolution.md"
  target_artifact: "docs/contracts/mythic_edge_issue_wave_interface_checkout_resolution.md"
  risk_tier: "high workflow risk; no product-runtime change"
  base_branch: "main"
  target_branch: "undecided; main requires explicit approval"
  branch: "codex/issue-wave-nomenclature"
  validation:
    - "Nine contract-first checkout and binding tests fail at the missing operation, CLI, schema, and contract boundaries."
  stop_conditions:
    - "Any saved-run schema or Dispatch behavior must change."
    - "Any legacy Role Pool, R0-bound, installer, deployment, or production edit."
    - "Any unapproved main-targeting or merge."
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "A"
  risk_tier: "high workflow risk; no product-runtime change"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read:
    - "ADR-0008"
    - "ADR-0012"
  protected_surfaces:
    - "workflow invocation and Dispatch admission vocabulary"
    - "local checkout identity and active-work exclusion"
    - "legacy Role Pool and R0-bound files (forbidden)"
  authority_conflicts_found: false
  authority_conflict_notes: "Issue #859 records the narrow explicit_user_override; main-targeting and merge remain separately gated."
```
