---
name: session-checkout
description: Inspect the current Mythic Edge checkout before workflow work, summarize safe status, and route the next role without mutating state.
---

# Session Checkout

Use this skill when starting or resuming work in a Mythic Edge repository and
the user wants the current checkout, handoff, branch, issue, PR, or dirty-state
context summarized before action.

This skill is an access and collaboration surface only. It never outranks
GitHub issues, PRs, merge commits, branch heads, `AGENTS.md`,
`docs/agent_rules.yml`, `docs/agent_constitution.md`,
`docs/codex_module_workflow.md`, accepted ADRs, or active contracts.

## Required Checks

1. Resolve the repository root from the current checkout.
2. Verify the remote identity when the prompt provides `repository_url`.
3. Inspect `git status --short --branch`.
4. Inspect branch and upstream state without changing branches.
5. Summarize dirty tracked files and untracked files.
6. Identify likely workflow artifacts, stale artifacts, and unrelated files.
7. Summarize supplied issue, tracker, PR, source artifact, target artifact, and
   workflow handoff state.
8. Treat workflow status indexes as convenience summaries only.
9. Recommend the next Codex role and the safest route.

## Forbidden Actions

Do not clean, stash, reset, delete, stage, commit, push, switch branches,
create or update issues, update PRs, update trackers, change automations, read
private logs, read app-data, inspect sibling repositories, install skills, or
change parser/runtime/workbook/webhook/App Script/analytics/AI/coaching
behavior.

Sibling repositories are out of scope unless the prompt explicitly supplies an
`allowed_read_only_references` entry or a prompt-scoped read-only target.

## Output Shape

Return a compact checkout summary with:

- repository identity and remote match status;
- branch, upstream, ahead/behind, dirty tracked files, and untracked files;
- source and target artifact state;
- freshness or checkout mismatch risks;
- recommended next role;
- optional pasteable next prompt;
- optional public-safe `workflow_handoff` block.

Public `workflow_handoff` blocks must include `repository` and
`repository_url`. Do not include local absolute paths in public handoff blocks.
Generated local prompts may include an operating worktree hint outside the
public handoff block.
