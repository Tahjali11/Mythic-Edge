# Codex H Constitutional Lawyer Adoption Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/76

## Tracker

N/A

## Contract

`docs/contracts/codex_h_constitutional_lawyer_adoption.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## What Codex H Adoption Is Supposed To Do

Codex H is an auxiliary governance synthesis role. It inventories constitution
feedback packets, produces source coverage before synthesis when multiple
packets are supplied, and proposes amendments, consolidations, unresolved
conflicts, and watch-list items.

Codex H is advisory only. It does not directly rewrite authority docs, replace
the normal A-G module workflow, make raw feedback packet repo storage
mandatory, promote E2 to permanent-role status, or change parser/runtime
behavior.

## Observed Current Repo Behavior

Before this pass, the repo already had A-G workflow docs, ADR policy, accepted
ADRs, workflow handoff templates, and implementation/review role docs.

Observed gaps against the contract:

- `docs/templates/constitution_feedback_packet.md` did not exist.
- `docs/agent_threads/constitutional_lawyer.md` did not exist.
- `AGENTS.md`, `docs/agent_constitution.md`, `docs/agent_rules.yml`, and
  `docs/codex_module_workflow.md` did not expose Codex H as an auxiliary
  governance synthesis role.
- Formal raw feedback packet storage was not documented as opt-in and
  authorized-only in committed repo docs.
- The Codex H source coverage table guard was not represented in committed
  role docs.

## What Changed

Docs-only governance adoption:

- Created `docs/templates/constitution_feedback_packet.md`.
- Created `docs/agent_threads/constitutional_lawyer.md`.
- Added concise Codex H references to `AGENTS.md`.
- Added a short auxiliary governance role section and feedback packet storage
  note to `docs/agent_constitution.md`.
- Added machine-readable auxiliary role and constitution feedback entries to
  `docs/agent_rules.yml`.
- Added concise Codex H routing and packet-template guidance to
  `docs/codex_module_workflow.md`.

No optional `docs/constitution_feedback/README.md` was added. The template and
role doc document the storage policy without creating raw packet folders or
making repo storage mandatory.

## Exact Sections Changed

- `AGENTS.md`: active rule package list; short Codex H auxiliary role note
  after the A-G role list.
- `docs/agent_constitution.md`: `Thread Roles` section gained
  `Auxiliary Governance Role`; `Artifact-First Handoffs` gained a raw feedback
  packet storage note.
- `docs/agent_rules.yml`: `document_architecture`; new `auxiliary_roles.H`;
  new `constitution_feedback`.
- `docs/codex_module_workflow.md`: `Thread Roles`; `Normal Path`; `Handoff
  Rule`.
- `docs/agent_threads/constitutional_lawyer.md`: new role doc with mission,
  do/do-not rules, source coverage guard, storage policy, outputs, checklist,
  and starter prompt.
- `docs/templates/constitution_feedback_packet.md`: new compact feedback
  packet template with redaction warning, authority/confidence/routing fields,
  and storage recommendation.

## Files Changed

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/constitutional_lawyer.md`
- `docs/templates/constitution_feedback_packet.md`
- `docs/implementation_handoffs/codex_h_constitutional_lawyer_adoption_comparison.md`

Pre-existing source artifact present as untracked input:

- `docs/contracts/codex_h_constitutional_lawyer_adoption.md`

## Code Changed

No runtime code changed.

## Tests Changed

No tests changed.

## Interface Changes

Governance/documentation interfaces changed only:

- Added a committed Codex H role doc.
- Added a committed constitution feedback packet template.
- Added machine-readable auxiliary role metadata and feedback packet storage
  policy.

No parser, workbook, webhook, Apps Script, CI gate, fixture, snapshot, drift
baseline, secret, environment variable, or runtime interface changed.

## Contract Matches

- Branch target is `main`.
- A-G remains the normal module workflow.
- Codex H is represented as auxiliary and advisory.
- Raw feedback packets default to issue comments or pasteable output.
- Formal raw packet repo storage is opt-in and requires explicit issue and
  contract authorization.
- The source coverage table guard is documented before Codex H synthesis.
- E2 was not promoted to permanent-role status.
- No ADR was added for this narrow adoption.

## Contract Mismatches

None identified after the docs/template/rule updates in this pass.

## Missing Tests Or Safeguards

No Python tests were required for docs-only governance changes.

Remaining review focus:

- Verify Codex H was not inserted into the A-G normal path.
- Verify raw feedback packet storage is not mandatory.
- Verify source coverage is required before multi-packet synthesis.
- Verify local skills, chat history, memory, and raw packets remain evidence
  rather than repo authority.
- Verify protected runtime/data surfaces remain untouched.

## Validation Run

```text
git status --short --branch -> ## main...origin/main; modified AGENTS.md, docs/agent_constitution.md, docs/agent_rules.yml, docs/codex_module_workflow.md; untracked Codex H docs/template/handoff and source contract
py -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())" -> passed with no output
git diff --check -> passed with no output
py tools\check_protected_surfaces.py --base origin/main -> passed; changed_paths: 0, forbidden: 0, warnings: 0
path-scoped protected surface check for touched files -> passed; changed_paths: 8, forbidden: 0, warnings: 5 expected workflow_authority_docs warnings authorized by issue #76 and contract
.\tools\run_repo_checks.ps1 -> 670 passed; lint checks passed
```

## Still Unverified

- Codex E contract-test review has not run yet.
- No PR was opened.
- Issue #76 remains open.
- Live parser/runtime/workbook/webhook/App Script behavior was intentionally
  not exercised because this was docs-only governance adoption.

## Forbidden Or Protected Surfaces

No parser/runtime/workbook/webhook/App Script behavior changed. No secrets,
raw logs, generated data, runtime status files, failed posts, workbook exports,
fixtures, snapshots, or baselines were touched.

Only workflow governance surfaces changed, as authorized by issue #76 and the
contract.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use [$mythic-edge-workflow](C:\Users\Tahj Blow\.codex\skills\mythic-edge-workflow\SKILL.md).

Act as Codex E: Module Reviewer / contract-test thread for issue #76.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/76

Branch target:
main

Contract:
docs/contracts/codex_h_constitutional_lawyer_adoption.md

Implementation handoff:
docs/implementation_handoffs/codex_h_constitutional_lawyer_adoption_comparison.md

Review the implementation diff against the contract. Verify that Codex H is adopted only as an auxiliary advisory governance synthesis role, A-G remains the normal module workflow, raw feedback packet repo storage remains opt-in/formal-round-only, the source coverage table guard exists, E2 is not promoted to permanent-role status, and protected parser/runtime/data surfaces remain unchanged.

Do not edit code or docs unless explicitly asked. Do not stage, commit, open a PR, merge, or close issue #76.

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
  source_artifact: "docs/contracts/codex_h_constitutional_lawyer_adoption.md"
  target_artifact: "docs/implementation_handoffs/codex_h_constitutional_lawyer_adoption_comparison.md"
  risk_tier: "Medium"
  branch: "main"
  validation:
    - "git status --short --branch"
    - "py -c \"import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())\""
    - "git diff --check"
    - "py tools\\check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not rewrite authority docs broadly."
    - "Do not create raw feedback packet files or feedback round packet folders."
    - "Do not make raw packet repo storage mandatory."
    - "Do not promote E2 to permanent-role status."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior or protected runtime/data surfaces."
    - "Do not stage, commit, open a PR, merge, or close issue #76 unless explicitly asked."
```
