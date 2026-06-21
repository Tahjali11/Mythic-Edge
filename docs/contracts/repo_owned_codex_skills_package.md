# Repo-Owned Codex Skills Package Contract

## Module

Portable repo-owned Codex skill package for Mythic Edge workflow helpers.

Plain English: this contract defines how Mythic Edge may keep a small set of
repo-owned Codex skill source files and a local installer in the repository so
fresh clones and future machines can install current workflow helpers. The
skills are guidance and access surfaces only. They must not become authority
over GitHub issues, PRs, branch heads, merge commits, repo governance docs,
accepted ADRs, or scoped contracts.

This Codex B pass does not implement code, open a PR, install skills, mutate
local skill folders, inspect sibling repositories, create automations, or
change product behavior.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/155
- Source artifact: GitHub issue #155 Codex A refresh comment
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed during this Codex B pass:

- The operating checkout remote matched
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- `main` and `origin/main` were both
  `44b47e351adf46f9ddc754d19f06050b187efe88`.
- The checkout was clean before this contract was added.
- Issue #155 was open.
- Current `main` did not contain tracked `docs/codex_skills/` files.
- Current `main` did not contain tracked `tools/install_codex_skills.py`.
- Stale PR #65 was closed and unmerged.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/templates/workflow_handoff.md`
- `docs/internal_project_map.md`
- `docs/contracts/repo_scoped_workflow_handoffs.md`
- `docs/contracts/workflow_freshness_guard.md`
- `tools/check_workflow_freshness.py --help`
- Issue #155 and its Codex A refresh comment
- Stale PR #65 metadata and file list
- Stale PR #65 repo-owned skill files as historical source material only
- Stale PR #65 `tools/install_mythic_edge_skill.py` as historical source
  material only
- Current installed local `mythic-edge-workflow` skill as reference context

No sibling repository was inspected. No private Player.log, UTC_Log, app-data,
runtime artifact, workbook export, credential, token, API key, webhook URL, or
local-only generated artifact was read.

## Problem

Mythic Edge has active local Codex skills and current repo governance, but the
repository no longer tracks the stale PR #65 skill package or installer. The
current local workflow skill also references repo-owned installation behavior
that current `main` does not provide.

Without a fresh contract, a future implementation could:

- merge stale PR #65 material directly;
- reintroduce machine-specific path assumptions;
- let local skills outrank repo authority;
- mutate sibling repositories while summarizing workcycles;
- run cleanup, stash, reset, delete, stage, commit, push, issue, PR, tracker,
  or automation actions from a skill prompt;
- leak local absolute paths into public handoffs or docs;
- overwrite local user skill folders destructively;
- create a second workflow authority separate from current repo governance.

The first bad value is any repo-owned skill or installer behavior that mutates
repositories, GitHub state, automations, private/local artifacts, or local skill
folders beyond the explicitly requested install target, or treats local skill
text as higher authority than the current repository and live GitHub state.

## Scope Decision

This contract approves a fresh V1 repo-owned skill package for two skills:

1. `$Session Checkout`
2. `$New Workcycle`

It approves a local-user-scoped installer and a short package documentation
page. It does not approve copying PR #65 wholesale, installing skills during
Codex B, mutating local skill folders in Codex B, inspecting sibling repos in
Codex B, or changing any parser/runtime/product behavior.

V1 does not require a skills manifest. The installable skill list is derived
from directories under `docs/codex_skills/` that contain a `SKILL.md` file.
If future versioning, compatibility metadata, or install groups are needed, a
later issue may add a manifest.

V1 does not add repo-owned source for the existing local
`mythic-edge-workflow`, `mythic-edge-constitution-review`, or
`mythic-edge-constitutional-lawyer` skills. Those may be reconciled in a later
scope if needed. This slice keeps #155 focused on the two requested workflow
helper skills plus the installer and package documentation.

## Owning Layer

Owning layer: Quality / Governance.

Adjacent layer: External / Collaboration Surface, because local Codex skills
and local installer output are collaboration and access surfaces.

The package must not own parser truth, product runtime behavior, workbook
truth, analytics truth, AI truth, local app truth, CI truth, merge readiness,
deploy readiness, release readiness, production readiness, or issue lifecycle
truth.

## Internal Project Area

Primary: Quality / Governance.

Supporting:

- External / Collaboration Surface, for local Codex skill installation and
  guidance.
- Generated / Local Artifacts, for user-local installed skill copies outside
  the repo.

This contract is not a parser contract, runtime contract, workbook/transport
contract, analytics contract, AI/model-provider contract, automation contract,
or production readiness contract.

## Truth Owner

Truth ownership remains with current source systems:

- GitHub issues, PRs, comments, labels, branches, and merge commits own live
  workflow and lifecycle state.
- `AGENTS.md`, `docs/agent_rules.yml`, `docs/agent_constitution.md`,
  `docs/codex_module_workflow.md`, `docs/agent_threads/`, `docs/templates/`,
  accepted ADRs, and scoped contracts own repo governance.
- `git status`, `git remote`, `git branch`, `git rev-parse`, and related Git
  commands own local checkout evidence.
- `docs/contracts/repo_scoped_workflow_handoffs.md` owns repo-scoped public
  handoff identity rules.
- `docs/contracts/workflow_freshness_guard.md` and
  `tools/check_workflow_freshness.py` own workflow freshness vocabulary.

The repo-owned skills may summarize and route based on those sources after
verification. They must not replace them.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
repo governance docs + live Git/GitHub metadata + explicit user prompt
  -> local Codex skill guidance
  -> advisory status summary / next prompt / handoff block
```

Forbidden reverse flow:

```text
local skill text or local installed skill state
  -/-> repo authority
  -/-> parser truth
  -/-> issue closure
  -/-> PR creation or merge
  -/-> tracker completion
  -/-> cleanup, stash, reset, delete, stage, commit, push
  -/-> automation creation or update
  -/-> private/live data read authorization
```

## Files Owned By This Contract

This contract owns:

- `docs/contracts/repo_owned_codex_skills_package.md`

Codex C may add or update:

- `docs/codex_skills/session-checkout/SKILL.md`
- `docs/codex_skills/new-workcycle/SKILL.md`
- `docs/codex_skills.md`
- `tools/install_codex_skills.py`
- `tests/test_install_codex_skills.py`
- `docs/implementation_handoffs/repo_owned_codex_skills_package_comparison.md`

Codex C must not add or update:

- parser source modules;
- workbook or Apps Script files;
- runtime status files;
- local installed skill folders outside the repo;
- automations;
- sibling repositories;
- stale PR #65 files wholesale;
- `docs/codex_skills/skills_manifest.json` unless a later issue authorizes a
  manifest.

## Public Interface

### Repo-Owned Skill Directory

V1 installable skill source root:

```text
docs/codex_skills/
```

Each installable skill must live in a directory:

```text
docs/codex_skills/<skill-folder>/SKILL.md
```

Each `SKILL.md` must include front matter:

```yaml
---
name: <skill-name>
description: <short trigger description>
---
```

Skill names must be lowercase kebab-case and match the folder name.

V1 skill folders:

- `session-checkout`
- `new-workcycle`

### Documentation Page

V1 documentation path:

```text
docs/codex_skills.md
```

The documentation must cover:

- package purpose;
- authority boundary;
- installed-skill target behavior;
- install commands;
- dry-run/list behavior;
- how local prompts may include operating worktree hints;
- how public handoffs must avoid local absolute paths;
- how to refresh local skills safely;
- why stale PR #65 is historical source material only.

### Installer

V1 installer path:

```text
tools/install_codex_skills.py
```

Required CLI interface:

```bash
python3 tools/install_codex_skills.py --list
python3 tools/install_codex_skills.py --dry-run --all
python3 tools/install_codex_skills.py --dry-run --skill session-checkout
python3 tools/install_codex_skills.py --all
python3 tools/install_codex_skills.py --skill session-checkout
```

Optional testing/customization arguments:

```bash
python3 tools/install_codex_skills.py --repo-root .
python3 tools/install_codex_skills.py --codex-home <temporary-codex-home>
```

The installer must be local-user scoped. Target root is:

```text
$CODEX_HOME/skills
```

when `CODEX_HOME` is set, otherwise:

```text
<current user home>/.codex/skills
```

The installer may print local target paths to terminal output because that
output is local and user-facing. It must not write those paths into committed
docs, public handoffs, issues, PR bodies, or templates.

## `$Session Checkout` Skill Contract

Purpose: help a fresh Codex thread understand the current operating checkout
before doing any workflow work.

Required behavior:

- verify the current Git repository root;
- verify remote identity against any provided `repository_url`;
- summarize current branch and upstream status;
- summarize ahead/behind state;
- summarize dirty tracked files and untracked files;
- identify likely workflow artifacts, stale artifacts, and unrelated files;
- summarize active issue, tracker, PR, source artifact, target artifact, and
  workflow handoff when supplied;
- report whether local workflow status indexes are present and whether they
  appear convenience-only;
- recommend safe next-role routing;
- produce a public-safe `workflow_handoff` block when useful;
- keep local absolute paths out of public handoff blocks;
- explain cleanup options without performing cleanup.

Forbidden behavior:

- no cleaning, stashing, resetting, deleting, staging, committing, pushing,
  branch switching, issue updates, PR updates, tracker updates, automation
  changes, or filesystem cleanup;
- no private Player.log, UTC_Log, app-data, runtime artifact, workbook export,
  credential, token, API key, webhook URL, or local-only artifact reads;
- no sibling repository inspection unless explicitly supplied as an
  `allowed_read_only_references` entry or prompt-scoped read-only target;
- no parser/runtime/workbook/webhook/analytics/AI behavior changes.

Output shape:

- compact status summary;
- freshness risks;
- dirty/untracked artifact summary;
- source/target artifact state;
- recommended next role;
- optional pasteable next prompt;
- optional repo-scoped `workflow_handoff` block.

## `$New Workcycle` Skill Contract

Purpose: help the user start or resume a Mythic Edge workcycle across one or
more explicitly configured Mythic Edge repositories without mutating them.

Default behavior:

- summarize only the operating repository unless the prompt supplies an
  explicit repository list or `allowed_read_only_references`;
- verify each referenced repository's public identity before local inspection;
- use GitHub/Git live state as authoritative when available;
- summarize active issues, PRs, branches, source artifacts, target artifacts,
  and likely next Codex roles;
- preserve repo-scoped stop conditions and handoff metadata;
- identify whether the next step is A, B, C, E, F, G, or no action;
- produce public-safe next prompts.

Configured repo-list behavior:

- A repo entry must include `repository` and `repository_url`.
- Local worktree paths may appear only in the user prompt or generated local
  prompt hints, never in public handoff blocks.
- If a repo cannot be verified, the skill must report it as unavailable or
  mismatch and skip mutation.
- Read-only sibling repo inspection is limited to Git/GitHub metadata, status,
  issue/PR state, and requested public artifacts.

Forbidden behavior:

- no sibling repo mutation;
- no source-repo issue creation, PR creation, cleanup, staging, committing,
  pushing, branch switching, reset, stash, deletion, or automation changes;
- no private/live data reads;
- no scheduled automation creation or update;
- no parser/runtime/workbook/webhook/analytics/AI behavior changes.

Output shape:

- per-repo status table;
- authoritative issue/PR/branch state summary;
- next-role recommendation per repo;
- public-safe prompts;
- repo-scoped `workflow_handoff` blocks as needed.

## Installer Semantics

### Skill Discovery

The installer must discover skills by scanning
`docs/codex_skills/*/SKILL.md`.

Discovery must ignore:

- directories without `SKILL.md`;
- hidden directories;
- files outside `docs/codex_skills/`;
- symlinks that resolve outside the repo-owned skill source root.

### Install Modes

Required modes:

- `--list`: print available skill names and source paths, no writes.
- `--dry-run`: print planned actions, no writes.
- `--skill <name>`: install or dry-run one skill.
- `--all`: install or dry-run all discovered skills.
- `--codex-home <path>`: override target root for tests or explicit local
  installs.
- `--repo-root <path>`: override source repo root for tests.

Default install behavior:

- if target skill directory does not exist, copy it;
- if target skill directory exists and is byte-for-byte identical, report
  `unchanged`;
- if target skill directory exists and differs, refuse by default and report a
  clear status;
- V1 does not authorize overwrite, replace, delete, prune, or backup behavior.

Future overwrite or backup behavior requires a new issue or contract amendment.

### Exit Codes

Recommended exit codes:

- `0`: success, dry-run success, list success, installed, or unchanged;
- `1`: validation or usage error;
- `2`: source package or selected skill missing;
- `3`: target exists and differs, refused by default;
- `4`: unsafe path, symlink escape, or checkout mismatch;
- `5`: unexpected install failure.

### Installer Output

Installer output must include:

- package name;
- mode;
- source repo root;
- target Codex home;
- skill names;
- action per skill: `would_install`, `installed`, `unchanged`, `refused`,
  `missing`, or `unsafe`;
- result: `passed`, `refused`, or `failed`.

The installer must not print file contents, secrets, raw logs, or private data.

## Inputs

Allowed inputs:

- repo governance docs listed in this contract;
- issue #155 and stale PR #65 metadata;
- current local installed skill files when explicitly used as reference
  context;
- live Git/GitHub metadata for the operating repository;
- explicitly supplied read-only sibling repository metadata for future
  `$New Workcycle` use;
- `$CODEX_HOME` environment variable value for install target resolution;
- optional `--codex-home` and `--repo-root` test paths.

Forbidden inputs:

- raw Player.log or UTC_Log contents;
- app-data paths or contents;
- runtime logs, failed post queues, SQLite files, workbook exports,
  generated/private artifacts, private reports, screenshots;
- secrets, credentials, tokens, API keys, webhook URLs;
- private decklists or private strategy notes;
- sibling repository source files unless explicitly authorized by a
  repo-scoped read-only reference;
- stale PR #65 as a direct merge source.

## Outputs

Committed outputs authorized for Codex C:

- two `SKILL.md` files under `docs/codex_skills/`;
- `docs/codex_skills.md`;
- `tools/install_codex_skills.py`;
- focused installer tests;
- implementation handoff.

Local outputs authorized only when the user or Codex C validation runs the
installer:

- installed skill folders under the selected Codex home;
- terminal output describing installed/refused/unchanged skills.

No public committed artifact may include the user's local absolute worktree
path or local Codex home path.

## Invariants

- Repo governance remains authoritative over local skills.
- GitHub issues, PRs, branch heads, and merge commits remain authoritative over
  workflow lifecycle state.
- Skills are collaboration/routing surfaces only.
- Public `workflow_handoff` blocks include `repository` and `repository_url`.
- Public handoffs do not include local absolute paths.
- Generated local prompts may include an `Operating repo/worktree:` hint
  outside the public handoff block.
- Checkout mismatch hard-stops before mutation.
- Sibling repositories are out of scope unless explicitly listed as read-only.
- Installer writes only inside the selected Codex skills target root.
- Installer refuses differing existing target skills by default.
- Installer does not delete, prune, overwrite, stash, reset, stage, commit,
  push, create issues, open PRs, close issues, update trackers, or update
  automations.
- `docs/codex_skills/` source content must not include machine-specific local
  paths.
- Stale PR #65 is historical reference only.

## Error Behavior

The skills and installer must fail safe:

- missing repo root: stop and ask for a valid checkout;
- remote mismatch: stop before mutation and report expected vs observed repo;
- missing `repository` or `repository_url` in a mutation-intended handoff:
  stop before mutation;
- sibling repo requested without read-only authorization: skip and report;
- dirty or untracked repo state: summarize and recommend options, no cleanup;
- missing skill source directory: installer exits with source-missing status;
- selected skill not found: installer exits with selected-skill-missing status;
- symlink escapes source root or target root: installer refuses;
- target skill exists and differs: installer refuses by default;
- invalid CLI arguments: installer exits with usage/validation error;
- private marker found in repo-owned skill source: validation fails.

Error messages must not echo secrets, raw private values, or long local paths
into public artifacts. Local terminal output may show explicit local install
paths, but committed docs and handoffs must use placeholders.

## Side Effects

Codex B side effects:

- Add this contract only.

Authorized future Codex C side effects:

- Add repo-owned skill source files.
- Add package documentation.
- Add installer.
- Add focused tests.
- Add implementation handoff.
- Run installer only in dry-run or test-target mode unless explicitly
  authorized.

Not authorized:

- editing local installed skill folders during Codex B;
- installing skills into the user's real Codex home during Codex C unless the
  user explicitly asks;
- mutating sibling repositories;
- changing parser/runtime/workbook/webhook/Apps Script/analytics/AI behavior;
- changing CI gates;
- creating/updating automations;
- staging, committing, pushing, opening PRs, or closing issues in Codex B/C
  without separate role authorization.

## Dependency Order

If implementation proceeds:

1. Add `docs/codex_skills/session-checkout/SKILL.md`.
2. Add `docs/codex_skills/new-workcycle/SKILL.md`.
3. Add `docs/codex_skills.md`.
4. Add `tools/install_codex_skills.py`.
5. Add `tests/test_install_codex_skills.py`.
6. Run dry-run/list focused validation against a temporary Codex home.
7. Run governance, secret, protected-surface, validation selector, and
   whitespace checks.
8. Write
   `docs/implementation_handoffs/repo_owned_codex_skills_package_comparison.md`.
9. Route to Codex E.

## Compatibility

The V1 package must be compatible with:

- current `AGENTS.md`;
- current `docs/agent_rules.yml`;
- current `docs/agent_constitution.md`;
- current `docs/codex_module_workflow.md`;
- `docs/contracts/repo_scoped_workflow_handoffs.md`;
- `docs/contracts/workflow_freshness_guard.md`;
- current skill-loading convention of directory plus `SKILL.md`.

Stale PR #65 compatibility is informational only. PR #65 must not be merged
directly, and its Windows-specific path hints must not be copied into V1 skill
source.

## Tests Required

Codex C should add focused tests for the installer:

- discovers only directories with `SKILL.md`;
- `--list` performs no writes;
- `--dry-run --all` performs no writes;
- `--dry-run --skill session-checkout` performs no writes;
- installs a missing skill into a temporary Codex home;
- reports identical target as `unchanged`;
- refuses differing target by default;
- rejects unknown skill names;
- rejects symlink escape source entries;
- handles missing package root cleanly;
- keeps repo-owned skill source free of local absolute paths and private
  markers.

Recommended validation commands:

```bash
python3 tools/install_codex_skills.py --list
python3 tools/install_codex_skills.py --dry-run --all
python3 tools/install_codex_skills.py --dry-run --skill session-checkout
PYTHONPATH=src python3 -m pytest -q tests/test_install_codex_skills.py
python3 -m ruff check tools/install_codex_skills.py tests/test_install_codex_skills.py
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

Codex E should also inspect:

- whether skills are guidance only and do not perform hidden actions;
- whether the installer is non-destructive by default;
- whether public docs avoid local absolute paths;
- whether stale PR #65 content was modernized rather than copied blindly;
- whether sibling repo boundaries are read-only and explicit.

## Acceptance Criteria

- Contract exists at `docs/contracts/repo_owned_codex_skills_package.md`.
- V1 skill package layout is explicit.
- Manifest decision is explicit: no manifest in V1.
- `$Session Checkout` behavior and forbidden actions are explicit.
- `$New Workcycle` behavior and forbidden actions are explicit.
- Public handoff vs local prompt path rules are explicit.
- Installer discovery, install, list, dry-run, and refusal semantics are
  explicit.
- Default refusal for differing local target skills is explicit.
- Checkout mismatch and sibling-repo stop behavior are explicit.
- Validation obligations for Codex C/E are explicit.
- Skills remain collaboration/access surfaces, not repo authority.

## Open Questions / Contract Risks

- A future issue may need to decide whether existing local skills
  (`mythic-edge-workflow`, `mythic-edge-constitution-review`, and
  `mythic-edge-constitutional-lawyer`) should also be repo-owned.
- A future issue may add a manifest if install groups, versions, or
  compatibility metadata become necessary.
- A future issue may authorize explicit overwrite/backup behavior for local
  installed skill updates. V1 refuses differing targets by default.
- `$New Workcycle` can summarize multiple repositories only through explicit
  read-only references. It must not become a broad local filesystem crawler.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Codex C should implement the repo-owned skill package, installer, tests, and
implementation handoff described here. It should not install into the user's
real Codex home unless explicitly asked.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #155.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/155

Base branch:
main

Target branch:
main

Contract:
docs/contracts/repo_owned_codex_skills_package.md

Goal:
Implement the portable repo-owned Codex skills package for `$Session Checkout`
and `$New Workcycle`, plus the local-user-scoped installer and focused tests.

Expected implementation artifacts:
- docs/codex_skills/session-checkout/SKILL.md
- docs/codex_skills/new-workcycle/SKILL.md
- docs/codex_skills.md
- tools/install_codex_skills.py
- tests/test_install_codex_skills.py
- docs/implementation_handoffs/repo_owned_codex_skills_package_comparison.md

Implementation scope:
- Keep skills as access/collaboration surfaces only.
- Do not make skills authoritative over GitHub issues, PRs, merge commits,
  branch heads, repo docs, ADRs, or contracts.
- Do not add a skills manifest in V1.
- Implement installer list, dry-run, install-one, install-all, temporary
  Codex home override, repo-root override, and default refusal when a target
  skill exists and differs.
- Run installer validation only in dry-run or temporary test-target mode unless
  the user explicitly asks to install into the real Codex home.

Protected boundaries:
- Do not open a PR.
- Do not mutate sibling repositories.
- Do not clean, stash, reset, delete, stage, commit, push, close issues, update
  trackers, or update automations.
- Do not read private Player.log, UTC_Log, app-data, live MTGA, private logs,
  runtime artifacts, workbook exports, secrets, credentials, tokens, API keys,
  or webhook URLs.
- Do not install into the user's real Codex home unless explicitly asked.
- Do not change parser behavior, parser state final reconciliation, parser
  event classes, router semantics, match/game identity, deduplication,
  workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, analytics truth, AI truth, coaching truth, release
  readiness, production readiness, deploy readiness, or final integration
  policy.

Validation:
- Run the focused installer tests and commands required by the contract.
- Run ruff on the installer and tests.
- Run agent-doc, secret-pattern, protected-surface, validation-selector, and
  whitespace checks on the touched paths.

Expected output:
- Implementation summary.
- Validation run.
- Remaining risks.
- Recommended next role.
- workflow_handoff block with repository and repository_url.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/155"
  tracker: ""
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #155 Codex A refresh comment"
  target_artifact: "docs/contracts/repo_owned_codex_skills_package.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  internal_project_area: "Quality / Governance; External / Collaboration Surface"
  truth_owner: "GitHub issues, PRs, merge commits, branch heads, repo docs, ADRs, and contracts remain authoritative; skills are local guidance/access surfaces only."
  bridge_code_status: "shared_support"
  validation:
    - "Verified operating checkout remote matches https://github.com/Tahjali11/Mythic-Edge."
    - "Verified main and origin/main at 44b47e351adf46f9ddc754d19f06050b187efe88."
    - "Inspected issue #155 and stale PR #65 as historical source material only."
    - "Inspected governance docs, repo-scoped workflow handoff contract, workflow freshness guard, current local workflow skill, and absence of tracked docs/codex_skills or tools/install_codex_skills.py."
  stop_conditions:
    - "Do not treat local Codex skills as authoritative over GitHub issues, PRs, merge commits, branch heads, repo docs, ADRs, or contracts."
    - "Do not mutate sibling repositories unless explicitly authorized by a repo-scoped handoff."
    - "Do not clean, stash, reset, delete, stage, commit, push, close issues, update trackers, or update automations without explicit role/user authority."
    - "Do not read private logs, private app-data, runtime artifacts, workbook exports, secrets, tokens, credentials, API keys, or webhook URLs."
    - "Do not install into the user's real Codex home unless explicitly asked."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics truth, AI truth, coaching truth, release readiness, production readiness, deploy readiness, or final integration policy."
```
