# Codex H Post-Adoption Governance Refinements Comparison

## Issue / Adoption Record

Primary adoption record: https://github.com/Tahjali11/Mythic-Edge/issues/76

Related PR: https://github.com/Tahjali11/Mythic-Edge/pull/77

Follow-up issue: not yet provided. If this work is submitted, prefer a new
follow-up issue that references #76, or use `Refs #76` rather than
`Closes #76`.

## Tracker

N/A

## Contract

`docs/contracts/codex_h_post_adoption_governance_refinements.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## What The Refinement Is Supposed To Do

Codex H already exists as an auxiliary advisory governance synthesis role. This
post-adoption refinement adds one narrow guard: before Codex H proposes
amendments from feedback packets, it should compare each recommendation against
current repo state and classify whether it is active, partially satisfied,
satisfied, stale, superseded, conflicting, or watch-list.

The refinement must not re-adopt Codex H, make feedback rounds mandatory,
create raw feedback packet storage, promote E2 to permanent-role status, make
Pyright required, weaken main-target gates, or change parser/runtime behavior.

## Observed Current Repo Behavior

Current docs already preserve:

- Codex H as auxiliary and advisory.
- A-G as the normal module implementation workflow.
- Source coverage before Codex H synthesis.
- Raw feedback packets as evidence, not authority.
- Feedback rounds as optional and formal-round-only for repo storage.
- E2 as optional Codex E mode in the hardening policy.
- Pyright as advisory in the hardening policy.
- Main-target approval gates.

Observed gap against the contract:

- Codex H source coverage did not explicitly require current repo state
  classification before amendment synthesis.
- The packet template did not mention optional later synthesis status.
- `docs/agent_rules.yml` did not encode status labels or current-status source
  checks.
- `docs/codex_module_workflow.md` did not state that H should separate active,
  satisfied, stale, superseded, conflicting, and watch-list recommendations.

## What Changed

Docs-only governance refinement:

- Updated `docs/agent_threads/constitutional_lawyer.md` to require checking
  current repo governance state and classifying packet recommendations before
  proposing amendments.
- Added the status labels `active`, `partially_satisfied`, `satisfied`,
  `stale`, `superseded`, `conflict`, and `watch_list` to the Codex H role doc.
- Added `current status` to the recommended source coverage columns.
- Added an optional Codex H-only `Later Synthesis Status` annotation to
  `docs/templates/constitution_feedback_packet.md`.
- Added terse machine-readable current-status classification fields to
  `docs/agent_rules.yml`.
- Added a concise routing note to `docs/codex_module_workflow.md`.

No edits were made to `AGENTS.md` or `docs/agent_constitution.md`; the
refinement is discoverable from the Codex H role doc, packet template, rule
index, and workflow guide.

## Exact Sections Changed

- `docs/agent_threads/constitutional_lawyer.md`
  - `Do`
  - `Source Coverage Guard`
  - new `Current Status Classification`
  - `Required Output`
  - `Handoff Packet`
  - `Completion Checklist`
  - `Canonical Starter Prompt`
- `docs/templates/constitution_feedback_packet.md`
  - template body gained optional `Later Synthesis Status`
- `docs/agent_rules.yml`
  - `constitution_feedback` gained current-status requirement, labels, and
    sources
- `docs/codex_module_workflow.md`
  - `Normal Path` / H routing guidance gained a current-state classification
    sentence

## Files Changed

- `docs/agent_threads/constitutional_lawyer.md`
- `docs/templates/constitution_feedback_packet.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/implementation_handoffs/codex_h_post_adoption_governance_refinements_comparison.md`

Pre-existing source artifact present as untracked input:

- `docs/contracts/codex_h_post_adoption_governance_refinements.md`

## Code Changed

No runtime code changed.

## Tests Changed

No tests changed.

## Interface Changes

Governance/documentation interfaces changed only:

- Codex H synthesis output now includes current-status classification.
- Codex H source coverage now includes a `current status` column or note.
- Feedback packet template now includes an optional H-only later synthesis
  status annotation.

No parser, workbook, webhook, Apps Script, CI gate, Pyright gate, fixture,
snapshot, drift baseline, secret, environment variable, raw log, generated
artifact, runtime status file, failed post, or workbook export interface
changed.

## Contract Matches

- Branch target is `main`.
- Codex H remains advisory synthesis.
- A-G remains the normal module implementation path.
- Feedback rounds remain optional.
- Raw packet repo storage remains formal-round-only.
- E2 remains optional Codex E mode.
- Pyright remains advisory.
- Main-target approval gates are unchanged.
- Closed issue #76 is treated as adoption record.
- Closed issues #72 and #33 are treated as historical context.
- No raw feedback packet files or formal round folders were created.

## Contract Mismatches

None identified after the docs/template/rule updates in this pass.

## Missing Tests Or Safeguards

No Python tests were required for docs-only governance changes.

Reviewer focus:

- Verify the status labels match the contract.
- Verify status classification happens before Codex H amendment synthesis.
- Verify the template status field is optional and H-only, not a burden on raw
  packet authors.
- Verify E2 was not promoted and Pyright was not made required.
- Verify no broad authority-doc rewrite happened.

## Validation Run

```text
git status --short --branch -> ## main...origin/main; modified docs/agent_rules.yml, docs/agent_threads/constitutional_lawyer.md, docs/codex_module_workflow.md, docs/templates/constitution_feedback_packet.md; untracked source contract and implementation handoff
py -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())" -> passed with no output
git diff --check -> passed with no output
py tools\check_protected_surfaces.py --base origin/main -> passed; changed_paths: 0, forbidden: 0, warnings: 0
path-scoped protected-surface check for touched/untracked governance paths -> passed; changed_paths: 6, forbidden: 0, warnings: 4 expected workflow_authority_docs warnings authorized by contract
rg -n "\s+$" touched governance paths -> no matches
.\tools\run_repo_checks.ps1 -> 670 passed; lint checks passed
```

## Verified GitHub Context

```text
issue #76 -> CLOSED
PR #77 -> MERGED into main at 14dee482f598db9ce6629e1cf1360b8cc633aaa6
issue #72 -> CLOSED
issue #33 -> CLOSED
```

## Still Unverified

- Codex E contract-test review has not run yet.
- No follow-up issue was opened.
- No PR was opened.
- Live parser/runtime/workbook/webhook/App Script behavior was intentionally
  not exercised because this was docs-only governance work.

## Forbidden Or Protected Surfaces

No parser/runtime/workbook/webhook/App Script behavior changed. No CI gates,
Pyright gates, secrets, raw logs, generated data, runtime status files, failed
posts, workbook exports, fixtures, snapshots, or baselines were touched.

Only workflow governance surfaces changed, as authorized by the contract.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use [$mythic-edge-workflow](C:\Users\Tahj Blow\.codex\skills\mythic-edge-workflow\SKILL.md).

Act as Codex E: Module Reviewer / contract-test thread for the Codex H post-adoption governance refinements.

Source/adoption issue:
https://github.com/Tahjali11/Mythic-Edge/issues/76

Contract:
docs/contracts/codex_h_post_adoption_governance_refinements.md

Implementation handoff:
docs/implementation_handoffs/codex_h_post_adoption_governance_refinements_comparison.md

Review the implementation diff against the contract. Verify that Codex H recommendations are classified against current repo state before synthesis; labels cover active, partially_satisfied, satisfied, stale, superseded, conflict, and watch_list; E2 remains optional; Pyright remains advisory; feedback rounds remain optional; raw packet repo storage remains formal-round-only; main-target approval gates remain unchanged; Codex H remains advisory; A-G remains the normal module workflow; and parser/runtime/workbook/webhook/App Script behavior and protected data surfaces remain unchanged.

Do not edit code or docs unless explicitly asked. Do not stage, commit, open a PR, merge, or close issues.

Suggested validation:
git status --short --branch
git diff --check
py tools\check_protected_surfaces.py --base origin/main
py -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())"

Produce a contract-test report or review handoff with findings first, confirmed matches, mismatches, missing tests, residual risks, validation results, next recommended role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/76"
  tracker: "N/A"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/codex_h_post_adoption_governance_refinements.md"
  target_artifact: "docs/implementation_handoffs/codex_h_post_adoption_governance_refinements_comparison.md"
  risk_tier: "Medium"
  branch: "main"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "py tools\\check_protected_surfaces.py --base origin/main"
    - "py -c \"import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())\""
  stop_conditions:
    - "Do not reopen the broad Codex H adoption design."
    - "Do not make feedback rounds mandatory."
    - "Do not create raw feedback packet files or formal round folders."
    - "Do not weaken main-target approval gates."
    - "Do not promote E2 to permanent-role status."
    - "Do not make Pyright required."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
```
