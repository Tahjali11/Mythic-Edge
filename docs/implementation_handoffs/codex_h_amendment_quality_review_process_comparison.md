# Codex H Amendment Quality Review Process Comparison

## Role Performed

Codex C: docs-only implementation / comparison thread, under the user's
explicit request to incorporate amendment-quality best practices into the
current constitutional review process.

## Source Context

Primary active branch:

```text
codex/codex-h-post-adoption-governance-refinements
```

Related adoption record:

- https://github.com/Tahjali11/Mythic-Edge/issues/76
- https://github.com/Tahjali11/Mythic-Edge/pull/77

Existing branch contract:

- `docs/contracts/codex_h_post_adoption_governance_refinements.md`

Best-practice research context used by the user request:

- OpenAI Model Spec chain-of-command and rule/default distinction
- NIST AI RMF govern/map/measure/manage lifecycle
- Anthropic agent autonomy guidance on meaningful oversight and intervention
- OWASP agentic AI threat framing around tool and autonomous-system risk

## What The New Review Process Is Supposed To Do

The current Codex H process already classifies feedback packet recommendations
against current repo state before amendment synthesis. This refinement adds a
second quality gate: Codex H should also judge whether a proposed amendment
would make the constitution system stronger rather than merely longer.

The added review process should:

- apply an amendment quality test before recommending adoption
- classify every proposed amendment by rule type
- assess ceremony impact before adding required process
- treat tools, plugins, connectors, MCP servers, and local skills as tool
  surfaces unless repo authority grants them a stronger role
- keep packet author burden low by making new template fields optional Codex H
  annotations

## What Changed

Docs-only governance updates:

- Updated `docs/agent_threads/constitutional_lawyer.md` with:
  - `Amendment Quality Test`
  - `Rule Type Classification`
  - `Ceremony Budget`
  - `Tool Surface Boundary`
  - expanded required output, handoff fields, checklist, and starter prompt
- Updated `docs/templates/constitution_feedback_packet.md` with optional
  Codex H-only `Later Amendment Quality Review` fields.
- Updated `docs/agent_rules.yml` with terse machine-readable labels and
  checks for amendment quality, rule type, ceremony impact, and tool-surface
  boundaries.
- Updated `docs/codex_module_workflow.md` with a short Codex H routing note.

No edits were made to `AGENTS.md` or `docs/agent_constitution.md`; the main
constitution already points to Codex H's role doc and the packet template.

## Rule Types Added

Codex H now classifies amendment proposals as:

- `hard_rule`
- `operating_default`
- `role_procedure`
- `template_field`
- `machine_rule`
- `adr_candidate`
- `watch_list`
- `no_action`

## Ceremony Impact Labels Added

Codex H now assesses ceremony impact as:

- `lower`
- `same`
- `higher_justified`
- `higher_not_justified`

## Tool Boundary Added

Tool surfaces are access or collaboration layers by default. The new guidance
names:

- local Codex skills
- MCP servers
- plugins and connectors
- GitHub, Google Drive, Google Sheets, and Google Docs connectors
- OpenAI Developer Docs or other documentation connectors
- OpenAI API runtime integrations
- browser, shell, and local automation helpers

These surfaces do not supersede repo governance docs, accepted ADRs,
parser/state truth, deterministic analytics, protected-surface gates, secret
policy, or human approval gates unless a current repo artifact explicitly says
otherwise.

## Code Changed

No runtime code changed.

## Tests Changed

No tests changed.

## Interface Changes

Governance/documentation interfaces changed only:

- Codex H synthesis now includes amendment quality, rule type, ceremony, and
  tool-surface assessments.
- Constitution feedback packets gained optional later-quality-review fields.
- The machine-readable rule index gained corresponding labels and guardrails.

No parser, workbook, webhook, Apps Script, CI gate, Pyright gate, fixture,
snapshot, drift baseline, secret, environment variable, raw log, generated
artifact, runtime status file, failed post, or workbook export interface
changed.

## Validation Run

```text
git status --short --branch -> ## codex/codex-h-post-adoption-governance-refinements...origin/codex/codex-h-post-adoption-governance-refinements; modified governance docs and untracked implementation handoff
py -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())" -> passed with no output
git diff --check -> passed with no output
py tools\check_protected_surfaces.py --base origin/main -> passed; changed_paths: 6, forbidden: 0, warnings: 4 expected workflow_authority_docs warnings
'docs/implementation_handoffs/codex_h_amendment_quality_review_process_comparison.md' | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin -> passed; changed_paths: 1, forbidden: 0, warnings: 0
py tools\check_agent_docs.py -> not run; tool is not present on this branch
```

## Still Unverified

- Codex E has not reviewed these additions yet.
- No follow-up issue was opened.
- No PR was opened or updated in this thread.
- Live parser/runtime/workbook/webhook/App Script behavior was intentionally
  not exercised because this was docs-only governance work.

## Protected Surface Status

No parser/runtime/workbook/webhook/App Script behavior changed. No CI gates,
Pyright gates, secrets, raw logs, generated data, runtime status files, failed
posts, workbook exports, fixtures, snapshots, or baselines were touched.

Only workflow governance surfaces changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use [$mythic-edge-workflow](C:\Users\Tahj Blow\.codex\skills\mythic-edge-workflow\SKILL.md).

Act as Codex E: Module Reviewer / contract-test thread for the Codex H amendment quality review process additions on branch codex/codex-h-post-adoption-governance-refinements.

Review these artifacts:
- docs/contracts/codex_h_post_adoption_governance_refinements.md
- docs/implementation_handoffs/codex_h_post_adoption_governance_refinements_comparison.md
- docs/implementation_handoffs/codex_h_amendment_quality_review_process_comparison.md
- docs/agent_threads/constitutional_lawyer.md
- docs/templates/constitution_feedback_packet.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/agent_constitution.md

Review goals:
1. Verify that Codex H still classifies recommendations against current repo state before synthesis.
2. Verify that the new amendment quality test helps reject bloat and improves amendment quality.
3. Verify every proposed amendment can now be classified by rule type.
4. Verify the ceremony budget protects low-risk escape hatches.
5. Verify the tool-surface boundary treats skills, MCPs, plugins, connectors, Google Workspace, OpenAI docs, and OpenAI runtime integrations as access/collaboration layers unless repo authority says otherwise.
6. Verify the packet template additions are optional Codex H annotations and do not burden raw packet authors.
7. Verify Codex H remains advisory, A-G remains the normal module workflow, feedback rounds remain optional, raw packet repo storage remains formal-round-only, E2 remains optional, Pyright remains advisory, and main-target approval gates remain unchanged.

Suggested validation:
git status --short --branch
git diff --check
git diff --name-status origin/main...HEAD
git diff origin/main...HEAD -- docs/agent_threads/constitutional_lawyer.md docs/templates/constitution_feedback_packet.md docs/agent_rules.yml docs/codex_module_workflow.md docs/agent_constitution.md
py tools\check_protected_surfaces.py --base origin/main
py -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())"

Do not edit files unless explicitly asked.
Do not stage, commit, push, open a PR, merge, close issues, or alter runtime/parser/workbook/webhook/App Script behavior.

Output findings first. If there are no blocking findings, say so clearly. Include contract matches, mismatches, missing tests or safeguards, validation results, residual risks, next recommended role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/76"
  tracker: "N/A"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "current user request plus docs/contracts/codex_h_post_adoption_governance_refinements.md"
  target_artifact: "docs/implementation_handoffs/codex_h_amendment_quality_review_process_comparison.md"
  risk_tier: "Medium"
  branch: "codex/codex-h-post-adoption-governance-refinements"
  validation:
    - "git status --short --branch"
    - "py -c \"import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())\""
    - "git diff --check"
    - "py tools\\check_protected_surfaces.py --base origin/main"
  stop_conditions:
    - "Do not make Codex H an implementation role."
    - "Do not make feedback rounds mandatory."
    - "Do not burden raw packet authors with mandatory quality fields."
    - "Do not weaken main-target approval gates."
    - "Do not promote E2 to permanent-role status."
    - "Do not make Pyright required."
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
```
