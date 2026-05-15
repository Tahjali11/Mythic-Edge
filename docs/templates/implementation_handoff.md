# Implementation Handoff

## Issue

Link to the GitHub issue.

## Contract

Link to the module contract.

## What Changed

Plain-English summary of the implementation.

## Files Changed

-

## Authorized Scope

List the files or path groups the issue and contract authorized this implementation thread to change.

-

## Scope Budget

- Production files changed:
- Test files changed:
- Documentation or handoff files changed:
- Files intentionally not touched:

If this implementation changed more files than the issue or contract named, explain why the additional paths were necessary.

## Contract Clauses Satisfied

Map each changed file to the contract clause or acceptance criterion it satisfies.

-

## Protected Surfaces Not Touched

Name any protected surfaces that were intentionally left unchanged, especially parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status, failed posts, and workbook exports.

- 

## Interface Changes

List changed function signatures, payload fields, workbook columns, environment variables, or script entrypoints.

## Tests Added Or Updated

- 

## Validation Run

```powershell

```

## Validation Selection

Record the output or reasoning from:

```powershell
py tools\select_validation.py --changed --base origin/<target-branch>
```

## Still Unverified

- 

## Reviewer Focus

Ask the contract test thread to pay special attention to:

- 

## Next Workflow Action

Next role:

Pasteable prompt:

```text

```

```yaml
workflow_handoff:
  issue: ""
  completed_thread: "C"
  next_thread: "E"
  source_artifact: ""
  target_artifact: ""
  risk_tier: ""
  branch: ""
  validation:
    - ""
  stop_conditions:
    - ""
```
