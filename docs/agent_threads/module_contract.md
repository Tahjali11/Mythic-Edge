# Module Contract Thread Rules

## Mission

Convert an approved problem representation into a concrete contract that implementation and testing threads can share.

Use `docs/templates/module_contract.md`.

## Do

- name the owning truth layer
- list files owned by the contract
- define public functions, payload fields, scripts, tabs, or columns
- define inputs and outputs
- distinguish provisional live values from final reconciled values
- define invariants
- define error behavior
- define side effects
- name dependency order across files and layers
- list required tests
- preserve legacy compatibility when needed

## Do Not

- implement the feature
- change unrelated code
- hide uncertainty
- define a contract that moves parser truth downstream without calling it out
- treat workbook formulas as the error handler for parser bugs

## Required Output

Create or update a contract under `docs/contracts/`.

The contract should link back to the problem representation or GitHub issue.

## Completion Checklist

- [ ] The truth-owning layer is named.
- [ ] Inputs are typed and sourced.
- [ ] Outputs and destinations are listed.
- [ ] Interfaces and signatures are clear.
- [ ] Side effects are named.
- [ ] Error behavior is specified.
- [ ] Tests are required by behavior, not just by file.
- [ ] Acceptance criteria are testable.

## Starter Prompt

```text
Use the Mythic Edge agent constitution. Act as the module contract thread for <issue-or-problem-doc>. Produce a module contract. Do not implement code except for tiny discovery spikes.
```

