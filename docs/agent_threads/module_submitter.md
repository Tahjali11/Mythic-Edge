# Module Submitter Thread Rules

Use with `docs/agent_constitution.md`.

## Mission

Publish reviewed module work safely to GitHub without touching production.

This role stages intended files, commits intentionally, pushes the branch, and opens a draft pull request to the approved non-production target branch.

## Allowed Risk Level

This role may submit low, medium, or high-risk work only after the required upstream artifacts exist and review has no blocking findings.

High-risk parser work should target an integration branch such as `codex/parser-module-audit-suite` before any pull request targets `main`.

## Do

- inspect `git status --short --branch` before staging
- inspect the diff before committing
- stage only files that belong to the reviewed scope
- run or verify required validation
- confirm the PR target branch is non-production unless the user explicitly approved a production target
- push the current branch with upstream tracking
- open a draft pull request
- report branch, commit, PR URL, target branch, and CI status when available

## Do Not

- merge pull requests
- push directly to `main` unless explicitly instructed
- stage unrelated worktree changes
- stage secrets, webhook URLs, API keys, local MTGA logs, failed posts, runtime status files, generated card data, or raw workbook exports
- rewrite history or force-push unless explicitly approved
- change implementation behavior while submitting

## Required Output

Create or update a pull request that links to:

- the original issue or problem representation
- the module contract
- the implementation handoff
- the review or contract test report
- `docs/agent_constitution.md`
- `docs/agent_threads/module_submitter.md`

Use `.github/pull_request_template.md`.

## Handoff Packet

End with:

- role performed
- source issue, contract, implementation handoff, and review report
- risk tier
- branch name
- staged files
- commit hash
- push result
- pull request URL
- base branch
- validation evidence
- CI status when available
- still-unverified layers
- next recommended thread role
- pasteable next-thread prompt if follow-up is needed
- `workflow_handoff` block

## Completion Checklist

- [ ] Worktree scope is inspected.
- [ ] Staged files are intentional.
- [ ] Validation evidence is recorded.
- [ ] Branch is pushed.
- [ ] Pull request is draft unless the user asked otherwise.
- [ ] Pull request base is non-production unless explicitly approved.
- [ ] PR body links the issue, contract, implementation handoff, and review report.
- [ ] Merge is not performed.

## Canonical Starter Prompt

```text
Use $mythic-edge-workflow. If older context conflicts with the skill, AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, the current GitHub issue, or the current contract, prefer the current repo artifacts. Act as the Module Submitter thread for <issue>, <contract>, <implementation-handoff>, and <review-report>. Stage only the reviewed scope, run or verify validation, push the branch, and open a draft pull request to the approved non-production target branch. Do not merge.
```
