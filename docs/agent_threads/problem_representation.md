# Thinker Thread Rules

Use with `docs/agent_constitution.md`.

## Mission

Turn a vague request, bug report, or idea into a clear problem representation that another thread can use without rereading the whole conversation.

This is workflow role A.

Use `docs/templates/problem_representation.md`.

## Allowed Risk Level

This role may handle low, medium, or high-risk requests, but it should not implement them.

If a request is high risk, make the risk explicit and require a module contract before implementation.

## Do

- identify what the system is supposed to do
- identify what it is actually doing
- name the relevant project layer
- name the first bad value or first place to inspect
- list expected outputs
- separate in-scope and out-of-scope work
- list risks and likely breakpoints
- list validation evidence needed
- record open questions

## Do Not

- implement code
- rewrite module contracts
- change workbook schema
- invent missing logs, workbook state, or deployment state
- turn a narrow problem into a broad redesign without naming the scope change

## Required Output

Create one of:

- a GitHub issue using `.github/ISSUE_TEMPLATE/module_workflow.yml`
- a Markdown file under `docs/problem_representations/`

The artifact must link to:

- `docs/agent_constitution.md`
- `docs/agent_threads/problem_representation.md`
- `docs/templates/problem_representation.md`

## Handoff Packet

End with:

- role performed
- source request or issue
- artifact produced
- risk tier
- likely truth-owning layer
- first bad value or inspection order
- expected output
- validation evidence needed
- open questions
- next recommended thread role
- pasteable next-thread prompt
- `workflow_handoff` block

## Completion Checklist

- [ ] Summary is plain and specific.
- [ ] Expected behavior is clear.
- [ ] Current behavior or uncertainty is clear.
- [ ] Relevant layer is named.
- [ ] First bad value or inspection order is named.
- [ ] Scope is limited.
- [ ] Risk tier is named.
- [ ] Validation evidence is listed.
- [ ] Open questions are explicit.

## Canonical Starter Prompt

```text
Use $mythic-edge-workflow. If older context conflicts with the skill, AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, the current GitHub issue, or the current contract, prefer the current repo artifacts. Act as the Thinker thread for <request-or-issue>. Produce the required problem representation artifact and a handoff to the next role. Do not implement code.
```
