---
name: new-workcycle
description: Start or resume a Mythic Edge workcycle across explicitly supplied repositories using read-only metadata and repo-scoped handoffs.
---

# New Workcycle

Use this skill when the user asks to start a new Mythic Edge workcycle, resume
several lanes, or orient across explicitly supplied Mythic Edge repositories.

This skill is an access and collaboration surface only. GitHub issues, PRs,
merge commits, branch heads, repo docs, accepted ADRs, and contracts remain
authoritative.

## Default Scope

By default, summarize only the operating repository. Inspect additional
repositories only when the prompt supplies an explicit repository list or
`allowed_read_only_references`.

Each repository entry must include:

- `repository`
- `repository_url`

Verify the repository identity before local inspection. If identity cannot be
verified, report the mismatch or unavailable repo and skip mutation.

## Allowed Read-Only Summary

For each authorized repository, summarize:

- verified repository identity;
- current branch and upstream state;
- active issue, tracker, PR, source artifact, and target artifact when supplied;
- likely next Codex role;
- repo-scoped stop conditions;
- public-safe next prompt or `workflow_handoff` when useful.

Live GitHub and Git state are authoritative when available. Local workflow
indexes are convenience summaries only.

## Forbidden Actions

Do not mutate sibling repositories, create issues, create PRs, clean, stash,
reset, delete, stage, commit, push, switch branches, update automations, read
private/live data, inspect broad filesystem locations, install skills, or
change parser/runtime/workbook/webhook/App Script/analytics/AI/coaching
behavior.

Do not treat generated next prompts, local skill text, or local workflow
indexes as authority over GitHub and repo governance.

## Output Shape

Return a concise per-repo status summary with:

- repository and remote verification;
- branch and dirty-state summary;
- authoritative issue/PR/branch state;
- next-role recommendation;
- public-safe next prompts;
- repo-scoped `workflow_handoff` blocks when useful.

Public `workflow_handoff` blocks must include `repository` and
`repository_url`. Local absolute worktree paths belong only in generated local
prompt hints outside public handoff blocks.
