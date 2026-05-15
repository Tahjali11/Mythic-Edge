# Contract Test Report

## Issue

Link to the GitHub issue.

## Contract

Link to the module contract.

## Implementation Under Test

Link to the pull request, branch, or changed-file list.

## Contract Summary

Briefly restate the behavior that must be true.

## Checks Run

```powershell

```

## Mutation Boundary

This report should identify mismatches and route them. It should not mutate implementation files unless the user explicitly asked this thread to switch from review/contract-test mode into fixer mode.

Role-scope command when reviewing local paths:

```powershell
py tools\check_role_scope.py --role E --paths <reviewed-report-paths>
```

## Results

Pass/fail summary.

## Confirmed Contract Matches

- 

## Contract Mismatches

For each mismatch, include file, function or section, evidence, and expected behavior.

- 

## Missing Tests

- 

## Drift Notes

State whether any issue appears to be repo drift, workbook drift, deployment drift, or missing environment setup.

## Recommendation

Choose one:

- approve
- request implementation fix
- request contract clarification
- split follow-up issue

## Next Workflow Action

Next role:

Pasteable prompt:

```text

```

```yaml
workflow_handoff:
  issue: ""
  completed_thread: "E"
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
