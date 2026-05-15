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
  next_recommended_action: ""
```
