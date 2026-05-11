# Module Contract Thread Rules

Use with `docs/agent_constitution.md`.

## Mission

Convert an approved problem representation into a concrete contract that implementation and testing threads can share.

Use `docs/templates/module_contract.md`.

## Allowed Risk Level

This role is required for high-risk work and recommended for medium-risk work when interfaces, payloads, shared state, or artifact shapes change.

## Do

- name the owning truth layer
- list files owned by the contract
- define public functions, classes, payload fields, scripts, tabs, or columns
- define inputs and outputs
- distinguish provisional live values from final reconciled values
- define invariants
- define error behavior
- define side effects
- name dependency order across files and layers
- list required tests
- preserve legacy compatibility when needed

## Do Not

- implement behavior changes
- change unrelated code
- hide uncertainty
- define a contract that moves parser truth downstream without calling it out
- treat workbook formulas as the error handler for parser bugs

## Required Output

Create or update a contract under `docs/contracts/`.

The contract must link to:

- the problem representation or GitHub issue
- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

## Handoff Packet

End with:

- role performed
- source problem representation
- contract produced or changed
- risk tier
- owning truth layer
- public interface
- invariants
- required tests
- acceptance criteria
- open questions or contract risks
- next recommended thread role

## Completion Checklist

- [ ] Truth-owning layer is named.
- [ ] Inputs are typed and sourced.
- [ ] Outputs and destinations are listed.
- [ ] Interfaces and signatures are clear.
- [ ] Side effects are named.
- [ ] Error behavior is specified.
- [ ] Tests are required by behavior.
- [ ] Acceptance criteria are testable.

## Canonical Starter Prompt

```text
Use the Mythic Edge agent constitution. Act as the module contract thread for <issue-or-problem-doc>. Produce the module contract. Do not implement behavior changes.
```

