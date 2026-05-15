## Summary

- TODO

## Linked Issue, Tracker, And Contract

- Issue:
- Tracker:
- Contract:
- Related ADRs:
- Implementation handoff:
- Review or contract-test report:
- Agent constitution: `docs/agent_constitution.md`
- Rule index: `docs/agent_rules.yml`
- Workflow: `docs/codex_module_workflow.md`

Use `Closes #...` only when this PR fully satisfies the issue. Use `Refs #...`
for partial, planning-only, contract-only, tracker, or follow-up work.

## Risk Tier

- [ ] Low
- [ ] Medium
- [ ] High

## Layer Ownership

Name the truth-producing layer and any downstream transport, workbook, display,
deployment, or workflow layers touched.

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

- TODO

## Protected Surfaces

Confirm any touched protected surfaces are explicitly authorized by the issue
and contract.

- [ ] Workbook schema unchanged or authorized.
- [ ] Webhook payload shape unchanged or authorized.
- [ ] Apps Script behavior unchanged or authorized.
- [ ] Parser event classes unchanged or authorized.
- [ ] Match/game identity unchanged or authorized.
- [ ] Deduplication unchanged or authorized.
- [ ] Final reconciliation unchanged or authorized.
- [ ] Secrets, raw logs, generated data, runtime status files, failed posts, and workbook exports are not included.

## Tests

```bash

```

## Contract Verification

- [ ] Implementation was checked against the module contract.
- [ ] Risk-tier requirements were followed.
- [ ] Provisional and final values are distinguished where relevant.
- [ ] Parser truth was not moved into workbook formulas, dashboard logic, Apps Script, webhook transport, or AI interpretation.
- [ ] Workbook, repo, deployment, issue lifecycle, PR lifecycle, and tracker drift are called out if relevant.

## PR Lifecycle

- [ ] PR is draft unless the user explicitly asked otherwise.
- [ ] Base branch is approved.
- [ ] `main` is not targeted unless explicitly approved.
- [ ] Review has no blocking findings or remaining blockers are named.
- [ ] Validation is present or explicitly explained.
- [ ] Issue close behavior is correct.
- [ ] Tracker update expectations are named.
- [ ] Merge, issue closure, and tracker completion are left for Codex G.

## Still Unverified

- TODO

## Workflow Handoff

```yaml
workflow_handoff:
  issue: ""
  tracker: ""
  completed_thread: "F"
  next_thread: "G"
  source_artifact: ""
  target_artifact: "draft_pull_request"
  risk_tier: ""
  branch: ""
  validation:
    - ""
  stop_conditions:
    - "Do not merge until Codex G verifies all merge gates and the user explicitly asks for deployer work."
```
