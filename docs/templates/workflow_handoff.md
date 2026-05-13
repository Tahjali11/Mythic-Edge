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
  validation:
    - ""
  stop_conditions:
    - ""
```

Valid `next_thread` values are `A`, `B`, `C`, `D`, `E`, `F`, `G`, or `none`.

Use `tracker` for parent/tracker issues such as queue, audit-suite, or
constitution-tracking issues. Leave it empty when no tracker exists.
