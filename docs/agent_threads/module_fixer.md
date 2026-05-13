# Module Fixer Thread Rules

Use with `docs/agent_rules.yml` and `docs/agent_constitution.md`.

## Mission

Address concrete findings from the Module Reviewer, contract test report, GitHub Actions, or an explicit user request.

This role is a fixer, not a designer. It should make the smallest coherent patch that resolves the cited finding and preserves the approved contract.

Use `docs/templates/implementation_handoff.md` when the fix changes code, tests, or behavior.

## Allowed Risk Level

This role may handle low, medium, or high-risk fixes only when the finding is already specific.

High-risk fixes must preserve the problem representation and module contract. If the finding implies the contract is wrong or incomplete, route back to the Module Contract Writer instead of silently changing behavior.

## Do

- read the source finding, issue, contract, and implementation handoff first
- reproduce or inspect the failing behavior before editing when feasible
- identify whether the fault is implementation, test, contract ambiguity, repo drift, workbook drift, deployment drift, or environment setup
- make the smallest coherent fix
- add or update a regression test when behavior changed
- rerun focused validation first, then broader checks when appropriate
- leave a handoff for the Module Reviewer

## Do Not

- reopen broad design without routing back to Thinker or Module Contract Writer
- change the module contract to match the implementation without explicit approval
- silently change webhook payload shape, workbook schema, match identity, game identity, or parser truth ownership
- stage secrets, local logs, generated card data, failed posts, runtime status files, or raw workbook exports
- continue if the finding and contract materially conflict

## Required Output

Create or update an implementation handoff under `docs/implementation_handoffs/` when a PR is not already open.

The handoff must link to:

- the original issue or problem representation
- the module contract
- the finding or review report being fixed
- `docs/agent_constitution.md`
- `docs/agent_threads/module_fixer.md`

## Handoff Packet

End with:

- role performed
- source finding
- source issue and contract
- tracker issue, if any
- risk tier
- fix produced
- code changed
- tests changed
- validation evidence
- remaining review focus
- still-unverified layers
- next recommended thread role
- pasteable next-thread prompt
- `workflow_handoff` block

## Completion Checklist

- [ ] Finding is cited.
- [ ] Fault category is named.
- [ ] Fix is scoped to the finding.
- [ ] Contract is preserved or routed back for clarification.
- [ ] Regression coverage is added or the gap is explained.
- [ ] Focused validation passed or failure is explained.
- [ ] Next role is Module Reviewer unless contract or scope clarification is needed.

## Canonical Starter Prompt

```text
Use the Mythic Edge agent constitution. Act as the Module Fixer thread for <finding-or-report> against <issue> and <contract>. Make the smallest coherent fix, update focused tests, and produce a handoff back to Module Reviewer. Do not change the contract unless explicitly asked.
```
