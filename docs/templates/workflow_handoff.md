# Workflow Handoff

Use this shape at the end of any thread that expects another Codex role to
continue the work.

## Next Step

Plain-English next step.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution. Act as Codex <role-id>: <role-name> for <issue-or-artifact>. Read <source-artifact> and produce <target-artifact>. <role-specific constraint>.
```

## Machine-Readable Handoff

```yaml
workflow_handoff:
  issue: "#"
  tracker: ""
  completed_thread: ""
  next_thread: ""
  source_artifact: ""
  target_artifact: ""
  risk_tier: ""
  branch: ""
  internal_project_area: ""
  truth_owner: ""
  bridge_code_status: ""
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

The `freshness` block is recommended for continuing implementation, review,
submission, and deployer handoffs when branch state, issue state, worktrees, or
artifact lifecycle may have changed. Older handoffs without `freshness` remain
valid historical artifacts, but continuing threads should verify freshness live
before editing or submitting work. See
`docs/contracts/workflow_freshness_guard.md` for the advisory verdict and route
vocabulary.
