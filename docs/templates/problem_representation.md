# Problem Representation

## Summary

One or two sentences describing the bug, feature, audit target, or confusing
behavior.

## Source Request Or Issue

Link to the originating request or GitHub issue.

## Tracker

Link to the tracker issue, if any.

## What The Code Is Supposed To Do

Describe the intended behavior in plain English.

## What It Is Actually Doing

Describe the current behavior. Include the exact bad output, missing output, or
confusing state if known.

## Why This Matters

Explain the user impact, debugging impact, workbook impact, or downstream
analytics impact.

## Project Layer

Choose the main layer:

- MTGA raw log source
- parser and state interpretation
- webhook / transport layer
- workbook landing sheets
- helper formulas
- dashboard / reporting tabs
- AI analysis
- repository coordination and agent workflow

## Internal Project Area

Choose the main ADR-0006/internal-project-map area when it helps route the
work:

- Parser
- Corpus / Provenance
- Analytics
- Local App / UI
- Workbook / Transport
- Quality / Governance
- Future AI Integration
- Shared Support
- Generated / Local Artifacts
- External / Collaboration Surface
- N/A / unclear

Future AI Integration is deferred vocabulary only. Naming it does not authorize
OpenAI or model-provider runtime integration, AI coaching evaluation, AI-owned
parser truth, AI-owned analytics truth, hidden-card truth, gameplay correctness
truth, or strategic certainty.

If this is bridge-code work, name both the source project area and the
consuming project area.

## First Bad Value

Name the first observed place where the data becomes wrong or ambiguous.

If unknown, list the places to inspect in order.

## Inputs

List representative logs, payloads, fixture rows, workbook tabs, docs, prompts,
or commands involved.

## Expected Output

List the final parser-managed fields, webhook rows, workbook columns, visible
dashboard effect, docs artifact, or workflow decision expected.

## Scope

In scope:

- TODO

Out of scope:

- TODO

## Risks And Likely Breakpoints

List likely import, shared state, interface, workbook, deployment, issue,
tracker, PR lifecycle, or data drift risks.

## Validation Evidence Needed

List the smallest checks that would prove the issue is fixed or the artifact is
complete.

```bash

```

## Open Questions

- TODO

## Next Workflow Action

Next role:

Pasteable prompt:

```text

```

```yaml
workflow_handoff:
  repository: ""
  repository_url: ""
  issue: ""
  tracker: ""
  completed_thread: "A"
  next_thread: "B"
  source_artifact: ""
  target_artifact: ""
  risk_tier: ""
  base_branch: ""
  target_branch: ""
  branch: ""
  validation:
    - ""
  stop_conditions:
    - ""
```
