# Workflow Handoff

## Next Step

Plain-English next step.

## Pasteable Next-Thread Prompt

```text
Use $mythic-edge-workflow. If older context conflicts with the skill, AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, the current GitHub issue, or the current contract, prefer the current repo artifacts. Act as the <next-role> thread for <issue-or-artifact>. Read <source-artifact> and produce <target-artifact>. <role-specific constraint>.
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
  role_scope:
    - ""
  authorized_paths:
    - ""
  stop_conditions:
    - ""
```
