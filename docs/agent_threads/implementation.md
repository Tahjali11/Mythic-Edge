# Implementation Thread Rules

Use with `docs/agent_constitution.md`.

## Mission

Implement the smallest coherent change that satisfies an approved problem representation and, when required, a module contract.

## Allowed Risk Level

Low-risk implementation may proceed directly.

Medium-risk implementation needs a problem representation and focused tests. A module contract is required when interfaces, shared state, artifact shape, or cross-layer behavior changes.

High-risk implementation requires a problem representation, module contract, and planned contract testing before code changes.

## Do

- read the problem representation and contract first
- inspect relevant files before editing
- state the intended behavior, current behavior, failure point, and edit plan before significant edits
- update all files required by the contract in one coherent pass
- add or update focused tests
- run the smallest relevant tests first, then broader checks
- preserve behavior outside the contract
- update docs when they are part of the behavior or handoff

## Do Not

- start broad implementation without a contract for ambiguous or high-risk work
- silently move truth ownership downstream
- silently change webhook payload shape
- commit logs, secrets, generated card dumps, failed posts, or runtime status files
- delete debug, archive, helper, or workbook observability layers without explicit approval
- ignore failing tests because they seem unrelated

## Required Output

Create a pull request or implementation handoff that links to:

- the problem representation or issue
- the module contract when one exists
- `docs/agent_constitution.md`
- `docs/agent_threads/implementation.md`

Use `docs/templates/implementation_handoff.md` when a PR is not yet open.

## Handoff Packet

End with:

- role performed
- source issue and contract
- implementation produced
- risk tier
- code changed
- tests changed
- interface changes
- validation evidence
- still-unverified layers
- next recommended thread role

## Completion Checklist

- [ ] Implementation references the contract when required.
- [ ] Changed interfaces match the contract.
- [ ] Tests cover required behavior.
- [ ] Focused validation passed.
- [ ] Repo-level validation passed or failure is explained.
- [ ] Secrets and local-only artifacts are not staged.
- [ ] Handoff names unverified workbook or deployment state.

## Canonical Starter Prompt

```text
Use the Mythic Edge agent constitution. Act as the implementation thread for <issue> and <contract-if-required>. Implement the smallest coherent change against the contract, update tests, and report validation evidence.
```

