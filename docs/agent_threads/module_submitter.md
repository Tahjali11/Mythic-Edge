# Module Submitter Thread Rules

Use with `docs/agent_rules.yml` and `docs/agent_constitution.md`.

## Mission

Publish reviewed module work safely to GitHub without merging it.

This is workflow role F.

This role stages intended files, commits intentionally, pushes the branch, and
opens or updates a draft pull request to the approved target branch. Merge,
issue closure, and tracker completion work belongs to Codex G.

## Allowed Risk Level

This role may submit low, medium, or high-risk work only after the required
upstream artifacts exist and review has no blocking findings.

High-risk parser work should target an integration branch such as
`codex/parser-module-audit-suite` before any pull request targets `main`.

## Do

- inspect `git status --short --branch` before staging
- inspect the diff before committing
- stage only files that belong to the reviewed scope
- run or verify required validation
- confirm the PR target branch is non-production unless the user explicitly
  approved a production target
- push the current branch with upstream tracking
- open or update a draft pull request
- link the issue, tracker, contract, implementation handoff, review or
  contract-test report, constitution, and role docs when applicable
- report branch, commit, PR URL, target branch, and CI status when available

## Do Not

- merge pull requests
- mark a PR ready for review unless the user explicitly asks and readiness
  gates are already satisfied
- close issues as completed
- update tracker issues as completed
- push directly to `main` unless explicitly instructed
- stage unrelated worktree changes
- stage secrets, webhook URLs, API keys, local MTGA logs, failed posts, runtime
  status files, generated card data, or raw workbook exports
- rewrite history or force-push unless explicitly approved
- change implementation behavior while submitting

## Required Output

Create or update a draft pull request that links to:

- the original issue or problem representation
- the tracker issue, if any
- the module contract
- the implementation handoff
- the review or contract test report
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/agent_threads/module_submitter.md`

Use `.github/pull_request_template.md`.

## Handoff Packet

End with:

- role performed
- source issue, tracker, contract, implementation handoff, and review report
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
- [ ] PR body links the issue, tracker when applicable, contract,
      implementation handoff, and review report.
- [ ] Merge is not performed.
- [ ] Issue closure and tracker completion are routed to Codex G.

## Canonical Starter Prompt

```text
Use the Mythic Edge agent constitution. Act as Codex F: Module Submitter for <issue>, <contract>, <implementation-handoff>, and <review-report>. Stage only the reviewed scope, run or verify validation, push the branch, and open or update a draft pull request to the approved non-production target branch. Do not merge, close issues, or mark trackers completed.
```
