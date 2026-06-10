# Current Status Summary

Use this compact shape when the user asks for current repo, issue, or PR
status. Verify live GitHub state with `gh` or GitHub when status freshness
matters.

```yaml
repo_status:
  branch: ""
  open_issues:
    - number: ""
      title: ""
      purpose: ""
      next_action: ""
  open_prs:
    - number: ""
      title: ""
      base: ""
      draft: ""
      checks: ""
      next_action: ""
  recently_merged:
    - pr: ""
      merge_commit: ""
      issue_closed: ""
      tracker_updated: ""
  active_tracker: ""
  freshness_summary:
    branch: ""
    upstream: ""
    ahead_behind: ""
    worktree_count: ""
    dirty_paths:
      - ""
    untracked_candidate_artifacts:
      - ""
    stale_or_closed_issue_worktrees:
      - ""
    active_open_issues:
      - ""
    freshness_risks:
      - ""
    next_safe_route: ""
  next_recommended_action: ""
```

The `freshness_summary` section is advisory reporting metadata. It helps
separate local checkout/worktree drift from project truth before another Codex
role continues work. It is not a product schema and is not a CI gate.
