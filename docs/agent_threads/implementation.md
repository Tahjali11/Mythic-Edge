# Implementation Thread Rules

## Mission

Implement the smallest coherent change that satisfies an approved module contract.

## Do

- read the problem representation and contract first
- inspect relevant files before editing
- explain the intended behavior, current behavior, failure point, and edit plan before significant edits
- update all files required by the contract in one coherent pass
- add or update focused tests
- run the smallest relevant tests first, then broader checks
- preserve behavior outside the contract
- update docs only when they are part of the behavior or handoff

## Do Not

- start broad implementation without a contract for ambiguous work
- silently move truth ownership downstream
- silently change webhook payload shape
- commit logs, secrets, generated card dumps, failed posts, or runtime status files
- delete debug, archive, helper, or workbook observability layers without explicit approval
- ignore failing tests because they seem unrelated

## Required Output

Create a pull request or implementation handoff that includes:

- problem representation link
- module contract link
- files changed
- interface changes
- tests added or updated
- validation run
- still-unverified layers

Use `docs/templates/implementation_handoff.md` when a PR is not yet open.

## Completion Checklist

- [ ] The implementation references the contract.
- [ ] Changed interfaces match the contract.
- [ ] Tests cover the required behavior.
- [ ] Focused validation passed.
- [ ] Repo-level validation passed or failure is explained.
- [ ] Secrets and local-only artifacts are not staged.
- [ ] Handoff names unverified workbook or deployment state.

## Starter Prompt

```text
Use the Mythic Edge agent constitution. Act as the implementation thread for <issue> and <contract>. Implement the smallest coherent change against the contract, update tests, and report validation evidence.
```

