# Contract Test Report

## Issue

Link to the GitHub issue.

## Tracker

Link to the tracker issue, if any.

## Contract

Link to the module contract.

## Implementation Under Test

Link to the pull request, branch, or changed-file list.

## Report Lifecycle

`report_lifecycle`: choose one.

- `initial_contract_test`
- `followup_after_fixer`
- `contract_clarification_review`
- `final_approval`

`final_approval` is invalid while any finding has
`finding_lifecycle: remaining_blocker`.

## Contract Summary

Briefly restate the behavior or documentation package that must be true.

## Checks Run

```bash

```

## Results

Pass/fail summary.

## Finding Lifecycle Summary

Use this table for active findings and for historical findings that changed
state after Codex D/C fixes or Codex B contract clarification. Preserve
original evidence unless it is actively misleading; mark superseded findings
explicitly instead of deleting them silently.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TODO | TODO | `original_finding` / `fixed_state_followup` / `superseded` / `remaining_blocker` / `remaining_non_blocking` / `deferred_followup` / optional `not_reproduced` | TODO | blocking / non_blocking / not_blocking | TODO | TODO | D / B / A / F / G / follow-up issue / none |

Fixed findings should use `fixed_state_followup` only after Codex E has
verification evidence. A Codex D handoff may state that a fix was attempted,
but Codex E owns the verified fixed-state label.

Superseded findings must cite the revised contract, issue comment, scope
decision, or other artifact that superseded them.

## Confirmed Contract Matches

- TODO

## Contract Mismatches

For each mismatch, include file, function or section, evidence, and expected
behavior.

- TODO

## Missing Tests

- TODO

## Drift Notes

State whether any issue appears to be repo drift, workbook drift, deployment
drift, local-data drift, issue lifecycle drift, PR lifecycle drift, or tracker
drift.

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
  tracker: ""
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
