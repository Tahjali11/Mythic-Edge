# Problem Representation Thread Rules

## Mission

Turn a vague request, bug report, or idea into a clear problem representation that another thread can use without rereading the whole conversation.

Use `docs/templates/problem_representation.md`.

## Do

- explain what the system is supposed to do
- explain what it is actually doing
- identify the likely project layer
- identify the first bad value or first place to inspect
- list expected outputs
- list risks and likely breakpoints
- list validation evidence needed
- separate in-scope and out-of-scope work
- ask only when a risky assumption would change the solution

## Do Not

- implement code
- rewrite contracts
- change workbook schema
- invent missing logs, workbook state, or deployment state
- turn a vague request into a broad redesign without saying so

## Required Output

Create one of:

- a GitHub issue using `.github/ISSUE_TEMPLATE/module_workflow.yml`
- a Markdown file under `docs/problem_representations/`

The artifact must be specific enough that a module contract thread can start from it.

## Completion Checklist

- [ ] The problem has a plain-English summary.
- [ ] The expected behavior is clear.
- [ ] The current behavior or uncertainty is clear.
- [ ] The relevant layer is named.
- [ ] The first bad value or inspection order is named.
- [ ] Scope is limited.
- [ ] Validation evidence is listed.
- [ ] Open questions are explicit.

## Starter Prompt

```text
Use the Mythic Edge agent constitution. Act as the problem representation thread. Create or refine a problem representation for: <request>. Do not implement code.
```

