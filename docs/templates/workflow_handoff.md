# Workflow Handoff

Use this shape at the end of any thread that expects another Codex role to
continue the work.

## Next Step

Plain-English next step.

## Authority And Public-Safety Notes

Name any prerequisite success that is evidence only, any explicit authority
that is still false, the protected-surface rollout phase if relevant, and any
public-safe/no-echo checks the next role should preserve. Do not put local
absolute paths or unsafe private source values in public handoffs.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution. Act as Codex <role-id>: <role-name> for <issue-or-artifact>. Read <source-artifact> and produce <target-artifact>. <role-specific constraint>.
```

Generated local prompts may add this machine-local hint outside public
`workflow_handoff` blocks:

```text
Operating repo/worktree:
`<local path supplied privately for this machine>`
```

Do not copy local absolute paths into public GitHub issues, PR bodies,
committed templates, committed docs, or machine-readable handoff blocks.

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

Valid `next_thread` values are `A`, `B`, `C`, `D`, `E`, `F`, `G`, or `none`.

Use `tracker` for parent/tracker issues such as queue, audit-suite, or
constitution-tracking issues. Leave it empty when no tracker exists.

The `internal_project_area`, `truth_owner`, and `bridge_code_status` keys are
optional routing metadata. Leave them empty or omit them when the source
artifact predates ADR-0006 vocabulary.

The `lane_activation` block is optional routing metadata for the repo WIP-1
policy. Use it to record the repo active slot, whether the lane is active,
parked, deferred, tracker-selected, blocked, cancelled, or complete, and any
named exception that allows a second active lane. Exception records should name
scope and expiration; local worktree names or local status indexes are not
enough by themselves.

Use `repository` and `repository_url` to identify the public GitHub repository
that owns the handoff. Continuing threads must normalize the local checkout
remote before mutation and hard stop if it does not match `repository_url`.
Strip trailing slashes and a trailing `.git` suffix when comparing. Treat
equivalent GitHub SSH remotes as matching only after converting them to the
same public HTTPS URL.

Use `base_branch` for the branch the work starts from or compares against,
`target_branch` for the branch future PR or deployer work should target, and
`branch` for the current working branch when useful. Preserve `branch` for
compatibility, but do not rely on it when base and target differ.

Use `allowed_read_only_references` only when a sibling repository may be
inspected as reference context. It authorizes read-only inspection and summary,
not edits, staging, commits, pushes, cleanup, generated artifacts, or lifecycle
changes in that sibling repository.

The `freshness` block is recommended for continuing implementation, review,
submission, and deployer handoffs when branch state, issue state, worktrees, or
artifact lifecycle may have changed. Older handoffs without `freshness` remain
valid historical artifacts, but continuing threads should verify freshness live
before editing or submitting work. See
`docs/contracts/workflow_freshness_guard.md` for the advisory verdict and route
vocabulary.

The `checkout_cleanup` block is required when `completed_thread` is `G`.
Codex G should use it to report checkout reconciliation, safe cleanup performed,
preserved changes, unresolved residue, and whether more user approval is needed.
It must not be used to justify destructive cleanup, except to record
auto-pruned verified squash-merge local branch residue after Codex G confirms
the branch is the head branch of the PR just merged or live-verified as merged,
the PR is `MERGED`, the local branch tip equals the merged/reviewed PR head
SHA, the merge commit is recorded, the branch is not current/main/an
integration branch/a protected long-lived branch, and no dirty worktree is
attached. Meaningful, unrelated, ambiguous, or user-authored changes must be
preserved and reported.

If repository identity is missing, ambiguous, or mismatched, stop before
reading beyond approved reference scope, editing, staging, committing, pushing,
cleaning, stashing, resetting, deleting, or otherwise mutating repository
content. Report the expected repository, expected `repository_url`, observed
safe remotes, current branch, and the user action needed to provide the correct
checkout or repo-scoped handoff.
