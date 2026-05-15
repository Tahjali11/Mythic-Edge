# Code Hardening ADR Policy Contract-Test Report

## Findings

No blocking findings.

No non-blocking contract findings were found in the ADR policy implementation.

## Open Questions Or Assumptions

- `docs/contracts/code_hardening_adr_policy.md` is still untracked in this
  working tree, but it is the source contract for this module and appears
  intended for the eventual submitter package.
- `docs/project_roadmap.md` and `docs/python_tooling_inventory.md` remain
  unrelated untracked files. They should not be staged or included in this
  module unless a separate issue authorizes them.
- Runtime parser tests were not run because this review is docs-only and no
  Python parser/runtime files changed.

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/62

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

## Contract

`docs/contracts/code_hardening_adr_policy.md`

Related contracts:

- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`

## Implementation Under Test

Branch: `codex/code-hardening-suite`

Changed files reviewed:

- `.github/pull_request_template.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/contracts/code_hardening_adr_policy.md`
- `docs/decisions/ADR_TEMPLATE.md`
- `docs/decisions/README.md`
- `docs/implementation_handoffs/code_hardening_adr_policy_comparison.md`

## Contract Summary

Issue #62 authorizes a docs-only ADR policy rollout for the code-hardening
suite. The implementation may add an ADR README, an ADR template, a comparison
handoff, and narrow references in active governance docs and the PR template.
It must not create seed ADRs or numbered ADR files, loosen protected-surface
requirements, treat ADRs as implementation authorization, change runtime
parser/workbook/webhook/App Script behavior, target `main`, or mark tracker
#33 complete.

## Checks Run

```powershell
git fetch --prune origin main codex/code-hardening-suite
git rev-list --left-right --count HEAD...origin/codex/code-hardening-suite
gh issue view 62 --repo Tahjali11/Mythic-Edge --json number,title,state,body,comments
gh issue view 33 --repo Tahjali11/Mythic-Edge --comments
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
rg -n "Architecture Decision Records|ADR|docs/decisions|Related ADRs" docs\agent_constitution.md docs\agent_rules.yml docs\codex_module_workflow.md .github\pull_request_template.md docs\decisions\README.md docs\decisions\ADR_TEMPLATE.md
$paths = @(); $paths += git diff --name-only; $paths += git ls-files --others --exclude-standard; $paths | Sort-Object -Unique | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
py -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text(encoding='utf-8')); print('docs/agent_rules.yml parsed')"
rg --files docs\decisions | rg "ADR-[0-9]{4}"
```

## Results

- Branch freshness: `HEAD...origin/codex/code-hardening-suite` returned `0 0`.
- `git diff --check` passed with no output.
- Normal protected-surface gate passed with `changed_paths: 0`,
  `forbidden: 0`, `warnings: 0`. This is expected because the gate's normal
  mode compares committed diff paths and this review is still in an
  uncommitted working tree.
- Supplemental working-tree path-list protected-surface check passed with
  `changed_paths: 11`, `forbidden: 0`, `warnings: 4`. The four warnings were
  expected `workflow_authority_docs` warnings for:
  - `.github/pull_request_template.md`
  - `docs/agent_constitution.md`
  - `docs/agent_rules.yml`
  - `docs/codex_module_workflow.md`
- The ADR reference `rg` check found the expected README, template,
  constitution, rules, workflow, and PR-template references.
- `docs/agent_rules.yml` parsed successfully as YAML.
- No numbered ADR files were found under `docs/decisions/`.

## Confirmed Contract Matches

- `docs/decisions/README.md` defines ADR purpose and authority, including that
  ADRs do not replace current user instructions, issues, contracts, review
  reports, protected-surface checks, or PR drift budgets
  (`docs/decisions/README.md:1`, `docs/decisions/README.md:5`).
- ADR authority is below active governing docs and current issue/contract
  authority, above handoffs/reports that do not supersede ADRs by themselves,
  and above stale memory/chat history (`docs/decisions/README.md:13`,
  `docs/decisions/README.md:16`, `docs/decisions/README.md:18`,
  `docs/decisions/README.md:22`).
- ADRs are explicitly not automatic protected-surface authorization
  (`docs/decisions/README.md:24`, `docs/decisions/ADR_TEMPLATE.md:59`,
  `docs/agent_constitution.md:259`, `docs/codex_module_workflow.md:9`).
- Required and not-required ADR categories are present
  (`docs/decisions/README.md:26`, `docs/decisions/README.md:44`).
- Lifecycle statuses match the contract: `Proposed`, `Accepted`,
  `Superseded`, `Deprecated`, and `Rejected`
  (`docs/decisions/README.md:59`).
- Naming rules use the contracted `ADR-0001-short-kebab-title.md` pattern and
  state that `ADR_TEMPLATE.md` is not a decision record and does not consume a
  number (`docs/decisions/README.md:71`, `docs/decisions/README.md:88`).
- Required ADR fields are listed in the README and represented in the template
  (`docs/decisions/README.md:90`, `docs/decisions/ADR_TEMPLATE.md:1`,
  `docs/decisions/ADR_TEMPLATE.md:3`, `docs/decisions/ADR_TEMPLATE.md:7`,
  `docs/decisions/ADR_TEMPLATE.md:19`, `docs/decisions/ADR_TEMPLATE.md:27`,
  `docs/decisions/ADR_TEMPLATE.md:65`).
- Supersession/update policy and citation guidance are present
  (`docs/decisions/README.md:117`, `docs/decisions/README.md:125`).
- The README index correctly says no numbered ADRs exist yet and reserves seed
  ADRs for a later issue (`docs/decisions/README.md:131`).
- The constitution received a narrow ADR subsection only
  (`docs/agent_constitution.md:255`).
- `docs/agent_rules.yml` adds ADR document architecture, authority placement,
  conflict routing, status values, and protected-surface conflict behavior
  without removing existing protected-surface or workflow rules
  (`docs/agent_rules.yml:12`, `docs/agent_rules.yml:16`,
  `docs/agent_rules.yml:53`, `docs/agent_rules.yml:146`).
- `docs/codex_module_workflow.md` adds narrow ADR citation/routing language
  without changing the A/B/C/E/F workflow (`docs/codex_module_workflow.md:9`,
  `docs/codex_module_workflow.md:67`).
- `.github/pull_request_template.md` adds `Related ADRs:` while preserving
  linked issue/contract, risk tier, layer ownership, drift budget, changes,
  tests, contract verification, still-unverified, and workflow handoff sections
  (`.github/pull_request_template.md:5`, `.github/pull_request_template.md:9`,
  `.github/pull_request_template.md:17`, `.github/pull_request_template.md:23`,
  `.github/pull_request_template.md:27`, `.github/pull_request_template.md:50`,
  `.github/pull_request_template.md:58`, `.github/pull_request_template.md:62`).
- `docs/implementation_handoffs/code_hardening_adr_policy_comparison.md`
  records the unrelated untracked docs and warns they must remain outside this
  module (`docs/implementation_handoffs/code_hardening_adr_policy_comparison.md:18`).

## Contract Mismatches

- None found.

## Missing Safeguards Or Missing Tests

- No automated ADR linter exists yet for required fields, monotonic numbering,
  status values, or README index consistency. This is a non-blocking residual
  risk because the contract did not require a linter for issue #62.
- The protected-surface gate's normal `--base` mode does not inspect untracked
  files. The supplemental path-list check covered the local working tree for
  this review, but Codex F should rerun validation after staging only the
  intended module files.
- GitHub PR rendering of the new `Related ADRs:` field remains unverified
  until submitter work opens or updates a PR.

## Drift Notes

- Repo drift: none found within the reviewed ADR policy scope.
- Workbook drift: not applicable.
- Deployment drift: not applicable.
- Local-data drift: two unrelated untracked docs remain present and should stay
  out of this module unless separately authorized.
- Protected-surface drift: four workflow authority docs changed, and those
  changes are explicitly authorized by issue #62 and
  `docs/contracts/code_hardening_adr_policy.md`.

## Recommendation

Approve for Codex F: Module Submitter. The final working-tree validation was
rerun after this report file was added.

Next role: Codex F: Module Submitter.

## Next Workflow Action

Pasteable prompt:

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex F: Module Submitter for the Code Hardening child issue: ADR policy and constitutional amendment.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/62

Branch target:
codex/code-hardening-suite

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_threads/module_submitter.md
- docs/contracts/code_hardening_adr_policy.md
- docs/implementation_handoffs/code_hardening_adr_policy_comparison.md
- docs/contract_test_reports/code_hardening_adr_policy.md
- .github/pull_request_template.md
- docs/decisions/README.md
- docs/decisions/ADR_TEMPLATE.md
- issue #33
- issue #62

Task:
Submit the reviewed docs-only ADR policy implementation. Inspect the working tree, stage only the intended issue #62 files, commit, push, and open a draft PR targeting codex/code-hardening-suite. Do not stage unrelated untracked docs.

Intended files:
- .github/pull_request_template.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/contracts/code_hardening_adr_policy.md
- docs/decisions/README.md
- docs/decisions/ADR_TEMPLATE.md
- docs/implementation_handoffs/code_hardening_adr_policy_comparison.md
- docs/contract_test_reports/code_hardening_adr_policy.md

Do not stage:
- docs/project_roadmap.md
- docs/python_tooling_inventory.md

Before commit, rerun:
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite

Because the normal protected-surface gate checks committed branch diffs, also run a staged/intended-path check before opening the PR if the files are still uncommitted:
git diff --cached --name-only | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin

Do not create seed ADRs or numbered ADR files. Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production deployment behavior, or merge-to-main policy. Do not treat ADRs as automatic authorization for protected-surface changes. Do not target main. Do not mark tracker #33 complete. Do not merge.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/62"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  source_artifact: "docs/contracts/code_hardening_adr_policy.md"
  target_artifact: "draft PR targeting codex/code-hardening-suite"
  implementation_artifact: "docs/implementation_handoffs/code_hardening_adr_policy_comparison.md"
  review_artifact: "docs/contract_test_reports/code_hardening_adr_policy.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check -> passed with no output"
    - "py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite -> passed; changed_paths 0, forbidden 0, warnings 0"
    - "supplemental working-tree path-list protected-surface check -> passed; changed_paths 11, forbidden 0, warnings 4 expected workflow authority warnings"
    - "rg ADR reference check -> passed"
    - "docs/agent_rules.yml YAML parse -> passed"
    - "rg --files docs\\decisions | rg \"ADR-[0-9]{4}\" -> no numbered ADR files found"
  stop_conditions:
    - "Do not stage docs/project_roadmap.md or docs/python_tooling_inventory.md unless separately authorized."
    - "Do not create seed ADRs or numbered ADR files under issue #62."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production deployment behavior, or merge-to-main policy."
    - "Do not treat ADRs as automatic authorization for protected-surface changes."
    - "Do not target main; hardening work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
    - "Do not merge."
```
