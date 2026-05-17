# Codex Skill Bundle

Mythic Edge keeps project-owned Codex skills in `docs/codex_skills/` so another
machine can install the same project workflow instructions from the repo.

These skills are helpers, not repo authority. If a skill conflicts with
`AGENTS.md`, `docs/agent_rules.yml`, `docs/agent_constitution.md`, a current
issue, a current contract, or an accepted ADR, follow the repo authority.

## Included Skills

- `mythic-edge-workflow`
- `mythic-edge-constitution-review`
- `mythic-edge-constitutional-lawyer`
- `openai-current-docs`

The bundle intentionally does not vendor Codex system skills, plugin cache
skills, or generic local skills such as PDF or browser automation helpers.

## Install On Windows

From the repo root:

```powershell
py tools\install_codex_skills.py --all
```

## Install On macOS Or Linux

From the repo root:

```bash
python3 tools/install_codex_skills.py --all
```

## Useful Commands

List bundled skills:

```bash
python3 tools/install_codex_skills.py --list
```

Preview installation:

```bash
python3 tools/install_codex_skills.py --all --dry-run
```

Install one skill:

```bash
python3 tools/install_codex_skills.py --skill mythic-edge-workflow
```

By default, installation replaces only the named repo-owned skill directories
under `$CODEX_HOME/skills` or, when `CODEX_HOME` is not set, under
`~/.codex/skills`.
