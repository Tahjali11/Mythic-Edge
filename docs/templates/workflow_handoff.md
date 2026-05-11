# Workflow Handoff

## Next Step

Plain-English next step.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution. Act as the <next-role> thread for <issue-or-artifact>. Read <source-artifact> and produce <target-artifact>. <role-specific constraint>.
```

## Machine-Readable Handoff

```yaml
workflow_handoff:
  issue: "#"
  completed_thread: ""
  next_thread: ""
  source_artifact: ""
  target_artifact: ""
  risk_tier: ""
  branch: ""
  validation:
    - ""
  stop_conditions:
    - ""
```
