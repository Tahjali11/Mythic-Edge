# Repo-Owned Codex Skills Package - Implementation Handoff

## Context

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: `https://github.com/Tahjali11/Mythic-Edge/issues/155`
- Contract: `docs/contracts/repo_owned_codex_skills_package.md`
- Risk tier: High
- Branch used: `codex/repo-owned-codex-skills-package-155`

## Comparison Summary

The contract requested a portable repo-owned Codex skill package for
`session-checkout` and `new-workcycle`, plus a local-user-scoped installer,
focused tests, and package documentation.

Implemented:

- Added `docs/codex_skills/session-checkout/SKILL.md`.
- Added `docs/codex_skills/new-workcycle/SKILL.md`.
- Added `docs/codex_skills.md`.
- Added `tools/install_codex_skills.py`.
- Added `tests/test_install_codex_skills.py`.
- Preserved the rule that skills are access/collaboration surfaces only.
- Preserved GitHub issues, PRs, merge commits, branch heads, repo governance
  docs, accepted ADRs, and scoped contracts as authority.
- Kept V1 manifest-free. Skills are discovered from
  `docs/codex_skills/*/SKILL.md`.
- Implemented list, dry-run all, dry-run one, install all, install one,
  `--repo-root`, and `--codex-home`.
- Kept default installer behavior non-destructive. Differing existing target
  skill directories are refused by default.
- Fixed SKILLS-E-001 by making existing-target equality byte-for-byte across
  full directory trees. The installer now compares relative path sets,
  directory/file types, and file bytes instead of relying on shallow file
  metadata.
- Fixed SKILLS-E-002 by refusing target-side symlink escapes before reporting
  an existing target as unchanged or copying into a missing target. The
  installer now rejects target skill directories that resolve outside the
  selected skills root and target `skills` roots that resolve outside the
  selected Codex home.

Not implemented, by contract:

- No install into the user's real Codex home.
- No overwrite, replace, prune, delete, or backup mode.
- No skills manifest.
- No sibling repository mutation.
- No issue, PR, tracker, automation, parser, runtime, workbook, webhook,
  Apps Script, analytics, AI, coaching, release, deploy, or production behavior
  changes.

## Files Changed

- `docs/contracts/repo_owned_codex_skills_package.md`
- `docs/codex_skills/session-checkout/SKILL.md`
- `docs/codex_skills/new-workcycle/SKILL.md`
- `docs/codex_skills.md`
- `tools/install_codex_skills.py`
- `tests/test_install_codex_skills.py`
- `docs/implementation_handoffs/repo_owned_codex_skills_package_comparison.md`

## Tests Added

`tests/test_install_codex_skills.py` covers:

- discovery only from directories with `SKILL.md`;
- `--list` no-write behavior;
- `--dry-run --all` no-write behavior;
- `--dry-run --skill session-checkout` no-write behavior;
- installing a missing skill into a temporary Codex home;
- identical target reporting `unchanged`;
- same-size and same-mtime but byte-different targets being refused as
  `target_differs`;
- target skill symlink escapes being refused as `target_symlink_escape` even
  when the external target bytes match the repo-owned skill;
- target root symlink escapes being refused before installing into the
  external directory;
- differing target refusal by default;
- unknown selected skill handling;
- missing package-root handling;
- symlink escape source rejection;
- source skill text avoiding local path and private marker literals.

## Validation Run

Passed:

```bash
python3 tools/install_codex_skills.py --list
python3 tools/install_codex_skills.py --dry-run --all
python3 tools/install_codex_skills.py --dry-run --skill session-checkout
PYTHONPATH=src python3 -m pytest -q tests/test_install_codex_skills.py
python3 -m ruff check tools/install_codex_skills.py tests/test_install_codex_skills.py
python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' \
  docs/contracts/repo_owned_codex_skills_package.md \
  docs/codex_skills/session-checkout/SKILL.md \
  docs/codex_skills/new-workcycle/SKILL.md \
  docs/codex_skills.md \
  tools/install_codex_skills.py \
  tests/test_install_codex_skills.py \
  docs/implementation_handoffs/repo_owned_codex_skills_package_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/repo_owned_codex_skills_package.md \
  docs/codex_skills/session-checkout/SKILL.md \
  docs/codex_skills/new-workcycle/SKILL.md \
  docs/codex_skills.md \
  tools/install_codex_skills.py \
  tests/test_install_codex_skills.py \
  docs/implementation_handoffs/repo_owned_codex_skills_package_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' \
  docs/contracts/repo_owned_codex_skills_package.md \
  docs/codex_skills/session-checkout/SKILL.md \
  docs/codex_skills/new-workcycle/SKILL.md \
  docs/codex_skills.md \
  tools/install_codex_skills.py \
  tests/test_install_codex_skills.py \
  docs/implementation_handoffs/repo_owned_codex_skills_package_comparison.md \
  | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

The validation selector reported required checks satisfied and Pyright as
advisory only. Pyright advisory was not run because the contract did not
require it and focused/full Ruff plus focused tests passed.

Codex D fixer validation for SKILLS-E-001:

```bash
python3 -m pytest -q tests/test_install_codex_skills.py
# 9 passed in 0.03s

python3 tools/install_codex_skills.py --list
# result: passed

python3 tools/install_codex_skills.py --dry-run --all
# result: passed

python3 tools/install_codex_skills.py --dry-run --skill session-checkout
# result: passed

python3 -m ruff check tools/install_codex_skills.py tests/test_install_codex_skills.py
# All checks passed!

python3 -m ruff check src tests tools
# All checks passed!

python3 tools/check_agent_docs.py
# result: passed

git diff --check
# passed with no output

python3 -m pytest -q
# 1899 passed in 24.63s
```

The path-scoped secret/private marker scan and protected-surface gate both
passed with `forbidden: 0` and `warnings: 0`. A fixed-string local marker check
found only the contract's own `Player.log` boundary prohibitions.

Codex D fixer validation for SKILLS-E-002:

```bash
python3 -m pytest -q tests/test_install_codex_skills.py
# 11 passed in 0.05s

python3 -m ruff check tools/install_codex_skills.py tests/test_install_codex_skills.py
# All checks passed!

python3 tools/install_codex_skills.py --list
# result: passed

python3 tools/install_codex_skills.py --dry-run --all
# result: passed

python3 tools/install_codex_skills.py --dry-run --skill session-checkout
# result: passed

python3 -m ruff check src tests tools
# All checks passed!

python3 tools/check_agent_docs.py
# result: passed

git diff --check
# passed with no output

python3 -m pytest -q
# 1901 passed in 24.73s
```

The direct target-symlink repro now exits `4` and reports
`reason=target_symlink_escape`. The path-scoped secret/private marker scan and
protected-surface gate both passed with `forbidden: 0` and `warnings: 0`.

## Remaining Risks / Non-Claims

- The installer was not run in write mode against the user's real Codex home.
- V1 refuses differing target skills; it does not provide backup or overwrite
  behavior.
- Existing local skills such as `mythic-edge-workflow` remain outside this V1
  package.
- `new-workcycle` remains read-only and prompt-scoped; it is not a broad
  filesystem crawler.
- The package does not authorize parser truth, analytics truth, AI truth,
  coaching truth, merge readiness, deploy readiness, production readiness, or
  issue lifecycle changes.

## Recommended Next Role

Codex E: Module Reviewer / Contract Tester.

Review focus:

- installer non-destructive behavior;
- target-path and symlink safety;
- no real Codex home writes in validation;
- skill text remains guidance-only;
- public docs and handoffs avoid local absolute paths;
- stale PR #65 was not copied wholesale;
- no sibling repo mutation or authority drift.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #155.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/155

Contract:
docs/contracts/repo_owned_codex_skills_package.md

Implementation handoff:
docs/implementation_handoffs/repo_owned_codex_skills_package_comparison.md

Branch:
codex/repo-owned-codex-skills-package-155

Goal:
Adversarially review the repo-owned Codex skills package and installer against
the contract. Confirm the skills remain guidance-only collaboration surfaces,
the installer is local-user-scoped and non-destructive by default, and no
authority or mutation boundaries drifted.

Review:
- docs/contracts/repo_owned_codex_skills_package.md
- docs/codex_skills/session-checkout/SKILL.md
- docs/codex_skills/new-workcycle/SKILL.md
- docs/codex_skills.md
- tools/install_codex_skills.py
- tests/test_install_codex_skills.py
- docs/implementation_handoffs/repo_owned_codex_skills_package_comparison.md

Check especially:
- skills do not claim authority over GitHub issues, PRs, branch heads, merge
  commits, repo docs, ADRs, or contracts;
- skills do not perform cleanup, stash, reset, delete, stage, commit, push,
  issue, PR, tracker, automation, private-data, parser, runtime, workbook,
  webhook, analytics, AI, coaching, release, deploy, or production actions;
- public handoff guidance includes repository and repository_url and avoids
  local absolute paths;
- installer discovers only docs/codex_skills/*/SKILL.md;
- installer list and dry-run perform no writes;
- installer copies missing skills only under the selected Codex skills target;
- identical targets report unchanged;
- same-size and same-mtime but byte-different targets are refused by
  byte-for-byte comparison;
- differing targets are refused by default;
- target skill and target root symlink escapes are refused before comparison
  or install;
- symlink escape sources are rejected;
- stale PR #65 material was modernized, not copied directly.

Validation:
- python3 tools/install_codex_skills.py --list
- python3 tools/install_codex_skills.py --dry-run --all
- python3 tools/install_codex_skills.py --dry-run --skill session-checkout
- PYTHONPATH=src python3 -m pytest -q tests/test_install_codex_skills.py
- python3 -m ruff check tools/install_codex_skills.py tests/test_install_codex_skills.py
- python3 tools/check_agent_docs.py
- git diff --check
- path-scoped secret/private marker scan
- path-scoped protected-surface scan
- path-scoped validation selector

Do not:
- Install into the user's real Codex home.
- Mutate sibling repositories.
- Clean, stash, reset, delete, stage, commit, push, close issues, update
  trackers, update PRs, or update automations.
- Read private logs, app-data, runtime artifacts, workbook exports, secrets,
  credentials, tokens, API keys, or webhook URLs.
- Change parser/runtime/workbook/webhook/App Script/analytics/AI/coaching/
  release/deploy/production behavior.
- Stage or commit unless explicitly asked.

End with:
- findings first, ordered by severity;
- validation run;
- residual risks;
- recommendation for next role;
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/155"
  tracker: ""
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/repo_owned_codex_skills_package.md"
  target_artifact: "tools/install_codex_skills.py; tests/test_install_codex_skills.py; docs/implementation_handoffs/repo_owned_codex_skills_package_comparison.md"
  fixed_finding_id: "SKILLS-E-001"
  finding_id: "SKILLS-E-002"
  verdict: "target_symlink_escape_fix_ready_for_module_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/repo-owned-codex-skills-package-155"
  internal_project_area: "Quality / Governance; External / Collaboration Surface"
  bridge_code_status: "shared_support"
```
