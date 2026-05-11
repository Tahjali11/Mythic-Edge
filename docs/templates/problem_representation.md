# Problem Representation

## Summary

One or two sentences describing the bug, feature, or confusing behavior.

## What The Code Is Supposed To Do

Describe the intended behavior in plain English.

## What It Is Actually Doing

Describe the current behavior. Include the exact bad output, missing output, or confusing state if known.

## Why This Matters

Explain the user impact, debugging impact, workbook impact, or downstream analytics impact.

## Project Layer

Choose the main layer:

- MTGA raw log source
- parser and state interpretation
- webhook / transport layer
- workbook landing sheets
- helper formulas
- dashboard / reporting tabs

## First Bad Value

Name the first observed place where the data becomes wrong or ambiguous.

If unknown, list the places to inspect in order.

## Inputs

List representative logs, payloads, fixture rows, workbook tabs, or commands involved.

## Expected Output

List the final parser-managed fields, webhook rows, workbook columns, or visible dashboard effect expected.

## Scope

In scope:

- 

Out of scope:

- 

## Risks And Likely Breakpoints

List likely import, shared state, interface, workbook, deployment, or data drift risks.

## Validation Evidence Needed

List the smallest checks that would prove the issue is fixed.

```powershell

```

## Open Questions

- 

## Next Workflow Action

Next role:

Pasteable prompt:

```text

```

```yaml
workflow_handoff:
  issue: ""
  completed_thread: "A"
  next_thread: "B"
  source_artifact: ""
  target_artifact: ""
  risk_tier: ""
  branch: ""
  validation:
    - ""
  stop_conditions:
    - ""
```
