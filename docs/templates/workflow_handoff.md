# Workflow Handoff

Use this shape when another Codex role should continue the work. The handoff is
workflow evidence, not a substitute for the issue, contract, review, PR, tests,
or current GitHub/git state.

## Next Step

Plain-English next step.

## Authority And Public-Safety Notes

Name prerequisite successes that are evidence only, authority flags that remain
false, protected-surface rollout phase when relevant, and public-safe/no-echo
checks to preserve. Do not put local absolute paths or unsafe private source
values in public handoffs.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution. Act as Codex <role-id>: <role-name> for <issue-or-artifact>. Read <source-artifact> and produce <target-artifact>. <role-specific constraint>.
```

Generated local prompts may add this private machine hint outside public
`workflow_handoff` blocks:

```text
Operating repo/worktree:
`<local path supplied privately for this machine>`
```

## Machine-Readable Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "#"
  tracker: ""
  completed_thread: ""
  next_thread: ""
  source_artifact: ""
  target_artifact: ""
  risk_tier: ""
  base_branch: ""
  target_branch: ""
  branch: ""
  internal_project_area: ""
  truth_owner: ""
  bridge_code_status: ""
  authority_notes:
    prerequisite_success_is_authority: false
    protected_surface_rollout_phase: ""
    readiness_claimed: false
    security_assurance_claimed: false
    privacy_assurance_claimed: false
  lane_activation:
    repo: "Tahjali11/Mythic-Edge"
    active_issue_or_lane: ""
    lane_status: ""
    tracker_selected_next_lane: ""
    exception:
      name: ""
      blocked_active_issue_or_pr: ""
      reason: ""
      allowed_scope: ""
      expiration_condition: ""
      authorized_by: ""
      recorded_in: ""
  allowed_read_only_references:
    - repository: ""
      repository_url: ""
      purpose: ""
  freshness:
    current_branch: ""
    intended_branch: ""
    upstream_branch: ""
    branch_ahead_behind: ""
    issue_state: ""
    tracker_state: ""
    source_artifact_status: ""
    target_artifact_status: ""
    local_dirty_state: ""
    untracked_artifacts:
      - ""
    worktree_classification: ""
    freshness_verdict: ""
    recommended_route: ""
    verified_at: ""
  checkout_cleanup:
    performed: false
    repo: ""
    starting_branch: ""
    ending_branch: ""
    target_branch: ""
    merge_commit: ""
    git_status_after: ""
    remote_refs_pruned: false
    remote_source_branch_deleted: false
    local_branch_deleted: false
    temporary_worktrees_removed:
      - ""
    generated_files_removed:
      - ""
    preserved_changes:
      - ""
    unresolved_residue:
      - ""
    destructive_cleanup_used: false
    user_approval_required_for_remaining_cleanup: false
  validation:
    - ""
  stop_conditions:
    - ""
```

For medium-risk and high-risk work, add this companion block to the durable
artifact or handoff. Low-risk work may defer it when obvious, local,
reversible, and outside protected surfaces.

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: ""
  risk_tier: ""
  global_router_read: false
  repo_agents_read: false
  repo_rules_read: false
  repo_constitution_read: false
  repo_workflow_read: false
  role_doc_read: false
  issue_or_tracker_read: false
  contract_or_handoff_read: false
  accepted_adrs_read:
    - ""
  protected_surfaces:
    - ""
  authority_conflicts_found: false
  authority_conflict_notes: ""
  stop_conditions:
    - ""
```

Valid `next_thread` values are `A`, `B`, `C`, `D`, `E`, `F`, `G`, or `none`.
Use `tracker` for parent/tracker issues; leave it empty when none exists.

Use `repository` and `repository_url` to identify the public GitHub repository
that owns the handoff. Continuing threads must verify the local checkout remote
before mutation and hard stop if it does not match. Strip trailing slashes and
`.git` before comparing; normalize equivalent GitHub SSH remotes to public
HTTPS first.

Use `base_branch` for the branch the work starts from or compares against,
`target_branch` for future PR/deployer target, and `branch` for the current
working branch when useful.

Use `allowed_read_only_references` only for sibling repos that may be inspected
as reference context. It authorizes read-only inspection and summary, not edits,
staging, commits, pushes, cleanup, generated artifacts, or lifecycle changes.

Use `freshness` for implementation, review, submission, or deployer handoffs
when branch, issue, PR, artifact, or worktree state may have changed. Older
handoffs without it remain historical artifacts; continuing threads still
verify freshness live before editing or submitting work.

Use `checkout_cleanup` when `completed_thread` is `G`. It reports checkout
reconciliation, safe cleanup performed, preserved changes, unresolved residue,
and whether more user approval is needed. It does not authorize destructive
cleanup except to record verified squash-merge local branch pruning after Codex
G confirms every condition in `docs/codex_module_workflow.md`.

If repository identity is missing, ambiguous, or mismatched, stop before
reading beyond approved reference scope, editing, staging, committing, pushing,
cleaning, stashing, resetting, deleting, or otherwise mutating repository
content. Report expected repository, expected URL, observed safe remotes,
current branch, and needed user action.
