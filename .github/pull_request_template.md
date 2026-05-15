## Summary

- 

## Linked Issue And Contract

- Issue:
- Contract:
- Related ADRs:
- Agent constitution: `docs/agent_constitution.md`
- Implementation rules: `docs/agent_threads/implementation.md`
- Fixer rules: `docs/agent_threads/module_fixer.md`
- Reviewer rules: `docs/agent_threads/review.md`
- Contract test rules: `docs/agent_threads/contract_test.md`
- Submitter rules: `docs/agent_threads/module_submitter.md`

## Risk Tier

- [ ] Low
- [ ] Medium
- [ ] High

## Layer Ownership

Name the truth-producing layer and any downstream transport or display layers touched.

## Drift Budget

Use `No drift`, `Authorized drift`, `Residual drift`, or `N/A`. For any `Authorized drift` or `Residual drift`, cite the issue and contract that allow it.

- Runtime/parser behavior:
- Parser event shape/classes:
- Workbook/webhook/App Script shape:
- Parser truth ownership:
- Fixtures/evidence:
- Protected-surface authorization:
- Residual drift / accepted gaps:
- Follow-up required:

## Changes

- 

## Authorized Scope

- Authorized changed paths:
- Role scope check:
- Validation matrix command:

## Tests

```powershell

```

## Contract Verification

- [ ] Implementation was checked against the module contract.
- [ ] Risk-tier requirements were followed.
- [ ] Validation was selected from `docs/validation_matrix.json` or the exception is explained.
- [ ] Role scope matched the active workflow thread or the exception is explained.
- [ ] Provisional and final values are distinguished where relevant.
- [ ] Parser truth was not moved into workbook formulas or dashboard-only logic.
- [ ] Workbook, repo, and deployed Apps Script drift are called out if relevant.

## Still Unverified

- 

## Workflow Handoff

```yaml
workflow_handoff:
  issue: ""
  completed_thread: "F"
  next_thread: "none"
  source_artifact: ""
  target_artifact: ""
  risk_tier: ""
  branch: ""
  validation:
    - ""
  stop_conditions:
    - ""
```
