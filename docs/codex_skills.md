# Repo-Owned Codex Skills

Mythic Edge keeps a small repo-owned Codex skill package so a fresh clone can
install current workflow helpers from repository source.

The skills are access and collaboration surfaces only. They help a Codex thread
inspect state, summarize handoffs, and route the next workflow role. They are
not authority over GitHub issues, PRs, branch heads, merge commits, repo docs,
accepted ADRs, scoped contracts, parser truth, merge readiness, deploy
readiness, or production behavior.

## Skills

Installable skill source lives under:

```text
docs/codex_skills/
```

V1 includes:

- `session-checkout`: summarize the current checkout before workflow work.
- `new-workcycle`: summarize explicitly supplied Mythic Edge repositories using
  read-only metadata and repo-scoped handoffs.

V1 does not include a skills manifest. The installer discovers directories
under `docs/codex_skills/` that contain `SKILL.md`.

## Install Commands

List available repo-owned skills without writing files:

```bash
python3 tools/install_codex_skills.py --list
```

Preview installation without writing files:

```bash
python3 tools/install_codex_skills.py --dry-run --all
python3 tools/install_codex_skills.py --dry-run --skill session-checkout
```

Install into the local Codex skills target:

```bash
python3 tools/install_codex_skills.py --all
python3 tools/install_codex_skills.py --skill session-checkout
```

For tests or an explicit temporary target:

```bash
python3 tools/install_codex_skills.py --codex-home <temporary-codex-home> --all
python3 tools/install_codex_skills.py --repo-root <repo-root> --list
```

The default target is `$CODEX_HOME/skills` when `CODEX_HOME` is set. Otherwise
the target is the current user's default Codex home under the user's home
directory. Local terminal output may show local target paths; committed docs,
issues, PR bodies, templates, and handoffs must not include local absolute
paths.

## Safe Refresh Behavior

The installer is non-destructive by default:

- missing target skill directory: copy the repo-owned skill;
- identical target skill directory: report `unchanged`;
- differing target skill directory: refuse by default;
- dry-run mode: report planned actions without writing files;
- list mode: report available skills without writing files.

V1 does not overwrite, replace, delete, prune, or back up existing local skill
folders. Future overwrite or backup behavior requires a separate issue and
contract.

## Public Handoff Boundary

Public `workflow_handoff` blocks must include:

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
```

Do not include local absolute paths in public handoff blocks. Generated local
prompts may include an operating worktree hint outside the public handoff block
when that helps the local Codex session.

## Stale PR 65

Stale PR #65 is historical source material only. Do not merge it directly and
do not copy its old machine-specific assumptions into the V1 skill package.

## Non-Claims

Installing or using these skills does not authorize:

- sibling repository mutation;
- cleanup, stash, reset, delete, stage, commit, push, issue, PR, tracker, or
  automation actions;
- private MTGA logs, app-data, runtime artifact, workbook export, or secret
  reads;
- parser/runtime/workbook/webhook/App Script/analytics/AI/coaching behavior
  changes;
- merge readiness, deploy readiness, release readiness, production readiness,
  or tracker completion.
