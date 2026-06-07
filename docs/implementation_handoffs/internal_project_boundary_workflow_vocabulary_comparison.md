# Internal Project Boundary Workflow Vocabulary Implementation Comparison

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/221

## Tracker

N/A

## Contract

`docs/contracts/internal_project_boundary_workflow_vocabulary.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

Codex D addendum: Module Fixer for the Codex E P2 finding that Future AI
Integration appeared in edited template vocabulary without the contract-required
non-authorization caveat.

## Branch And Git Status

Branch: `codex/internal-boundary-workflow-vocabulary`

Initial status:

```text
## codex/internal-boundary-workflow-vocabulary
?? docs/contracts/internal_project_boundary_workflow_vocabulary.md
```

The untracked contract is the Codex B source artifact for this pass and was
not edited by Codex C.

## Files Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/internal_project_map.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/contracts/internal_project_boundaries.md`
- `docs/contracts/internal_project_boundary_annotation_organization.md`
- `docs/contracts/internal_project_boundary_workflow_vocabulary.md`
- `docs/templates/problem_representation.md`
- `docs/templates/module_contract.md`
- `docs/templates/contract_test_report.md`
- `docs/templates/workflow_handoff.md`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- GitHub issue #221

## Current Behavior Compared To Contract

Current repo behavior already provides:

- Accepted ADR-0006 repository-boundary policy.
- `docs/internal_project_map.md` with the canonical internal project
  vocabulary.
- Existing `Project Layer` language in problem representation and GitHub issue
  templates.
- Existing `Layer Ownership` language in the PR template.
- Existing compact `workflow_handoff` shape.

Gaps found:

- `docs/templates/problem_representation.md` did not ask for internal project
  area.
- `.github/ISSUE_TEMPLATE/module_workflow.yml` did not expose the internal
  project area vocabulary.
- `docs/templates/module_contract.md` did not ask for internal project area,
  truth owner, or bridge-code status.
- `docs/templates/implementation_handoff.md` did not ask implementers to report
  internal project area, truth owner, bridge-code status, or contracted-area
  containment.
- `docs/templates/contract_test_report.md` did not ask reviewers to verify
  internal project area or bridge-code classification.
- `docs/templates/workflow_handoff.md` did not document optional
  `internal_project_area`, `truth_owner`, or `bridge_code_status` keys.
- `.github/pull_request_template.md` did not explicitly ask for internal
  project area, truth owner, bridge-code status, or downstream consumers.

## Implementation Option Chosen

Implemented the minimal docs/template-only vocabulary alignment authorized by
the contract. No optional edits were made to `docs/codex_module_workflow.md` or
`docs/internal_project_map.md` because the required gaps were resolved in the
templates and PR/issue metadata surfaces.

## Files Changed

- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- `docs/templates/problem_representation.md`
- `docs/templates/module_contract.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/contract_test_report.md`
- `docs/templates/workflow_handoff.md`
- `docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md`

Source artifact present but not edited by Codex C:

- `docs/contracts/internal_project_boundary_workflow_vocabulary.md`

## Exact Sections Changed

- `docs/templates/problem_representation.md`
  - Kept `## Project Layer`.
  - Added `## Internal Project Area` with canonical ADR-0006 values plus
    `N/A / unclear`.
  - Added the Future AI Integration deferred/non-authorization caveat.
  - Added bridge-code guidance to name source and consuming project areas.

- `docs/templates/module_contract.md`
  - Kept `## Owning Layer`.
  - Added `## Internal Project Area`.
  - Added the Future AI Integration deferred/non-authorization caveat.
  - Added `## Truth Owner`.
  - Added `## Bridge-Code Status` with the contract's five status values.
  - Added bridge-code guidance for data flow, reverse-flow, and protected
    surfaces.

- `docs/templates/implementation_handoff.md`
  - Added `## Internal Project Area`.
  - Added `## Truth Owner`.
  - Added `## Bridge-Code Status`.
  - Added `## Contracted Area Status`.

- `docs/templates/contract_test_report.md`
  - Added `## Internal Project Area Reviewed`.
  - Added `## Bridge-Code Status Reviewed`.
  - Directed reviewers to use the existing finding lifecycle table for
    vocabulary mismatches.

- `docs/templates/workflow_handoff.md`
  - Added optional `internal_project_area`, `truth_owner`, and
    `bridge_code_status` keys to the machine-readable block.
  - Documented that the keys are optional routing metadata.

- `.github/ISSUE_TEMPLATE/module_workflow.yml`
  - Kept the required `Primary project layer` dropdown.
  - Added optional `Internal project area` dropdown with canonical values and
    `N/A / unclear`.
  - Added the Future AI Integration deferred/non-authorization caveat to the
    internal-project-area field description.
  - Referenced `docs/internal_project_map.md` in the field description.

- `.github/pull_request_template.md`
  - Updated `Layer Ownership` to ask for internal project area, truth owner,
    bridge-code status, and downstream consumers.
  - Added a note that those fields are routing/review metadata and do not
    authorize protected-surface changes or replace gates.
  - Added the Future AI Integration deferred/non-authorization caveat to the
    layer-ownership note.

## Title Prefix Guidance

Title prefix guidance was preserved in this handoff rather than added as a new
gate in templates:

| Internal project area | Preferred prefix |
| --- | --- |
| Parser | `[parser]` |
| Corpus / Provenance | `[corpus/provenance]` |
| Analytics | `[analytics]` |
| Local App / UI | `[local-app]` |
| Workbook / Transport | `[workbook/transport]` |
| Quality / Governance | `[quality]` or `[governance]` |
| Architecture / boundary hygiene | `[architecture]` |
| Future AI Integration | `[ai]`, deferred/future only |
| Shared Support | Prefer the primary consumer prefix and name bridge status in the body. |
| Generated / Local Artifacts | Prefer the governing project prefix and name artifact status in the body. |
| External / Collaboration Surface | `[external-integration]` or `[governance]` |

Compatibility decisions:

- Existing issue and PR titles do not need renaming.
- `[analytics/app]` remains acceptable for existing analytics local-app
  umbrella work.
- `[parser-resilience]` remains historical tracker language.
- `[provenance]` remains acceptable as shorthand only when the body names
  `Corpus / Provenance`.
- Do not use `[bridge]` alone.

## Code, Tests, And Behavior Status

Code changed: no.

Tests changed: no.

Docs/template/governance-only change: yes.

Runtime behavior changed: no.

CI gates changed: no.

Vocabulary fields made merge-blocking: no.

## Protected-Surface Status

No parser, runtime, analytics, local app, workbook, webhook, Apps Script,
Sheets, AI, production, CI, package, import, fixture, snapshot, generated, or
local-only surfaces were intentionally touched.

## Validation Run

```powershell
git status --short --branch
git diff --check
py tools\check_agent_docs.py
py -c "from pathlib import Path; import yaml; yaml.safe_load(Path('.github/ISSUE_TEMPLATE/module_workflow.yml').read_text())"
@'
docs/contracts/internal_project_boundary_workflow_vocabulary.md
docs/templates/problem_representation.md
docs/templates/module_contract.md
docs/templates/implementation_handoff.md
docs/templates/contract_test_report.md
docs/templates/workflow_handoff.md
.github/ISSUE_TEMPLATE/module_workflow.yml
.github/pull_request_template.md
docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/internal_project_boundary_workflow_vocabulary.md
docs/templates/problem_representation.md
docs/templates/module_contract.md
docs/templates/implementation_handoff.md
docs/templates/contract_test_report.md
docs/templates/workflow_handoff.md
.github/ISSUE_TEMPLATE/module_workflow.yml
.github/pull_request_template.md
docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
git diff --name-only
```

Results:

- `git status --short --branch` -> expected tracked template edits plus
  untracked Codex B contract and Codex C handoff.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed, 0 errors, 0 warnings.
- YAML parse check for `.github/ISSUE_TEMPLATE/module_workflow.yml` -> passed.
- Path-scoped protected-surface scan -> passed, forbidden 0, warnings 7
  expected workflow-authority warnings for contract-authorized template and
  PR/issue template files.
- Path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0.
- Handoff ASCII/final-newline/trailing-whitespace check -> passed.
- `git diff --name-only` -> tracked edits limited to allowed template and
  PR/issue-template files; untracked contract and handoff are visible in
  `git status --short --branch`.

Codex D fixer validation after the Future AI Integration caveat update:

- `git status --short --branch` -> expected tracked template edits plus
  untracked contract and handoff.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed, 0 errors, 0 warnings.
- YAML parse for `.github/ISSUE_TEMPLATE/module_workflow.yml` -> passed.
- Path-scoped protected-surface scan -> passed, forbidden 0, warnings 7
  expected workflow-authority warnings.
- Path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0.
- Focused `rg` check over affected templates -> Future AI Integration caveats
  now mention deferred vocabulary, no OpenAI/model-provider runtime
  authorization, no AI-owned parser or analytics truth, no hidden-card truth,
  no gameplay correctness truth, and no strategic certainty.

## Remaining Risks Or Unverified Layers

- Codex E should verify that the Future AI Integration caveat satisfies the
  contract-required non-authorization language without making vocabulary fields
  hard gates.
- Codex E should verify that the optional handoff keys do not conflict with
  current governance docs or the agent docs checker.
- Codex E should verify that the issue template YAML remains valid.
- Codex E should decide whether title prefix guidance belongs only in the
  handoff for this issue or should later move into a durable template or
  governance note.
- Live GitHub issue form rendering was not manually inspected in a browser.
- No runtime tests were run because the diff is docs/template-only and the
  contract does not require runtime validation.

## Forbidden Scope Status

No files were moved.

No packages were renamed.

No imports were changed.

No repositories were split.

No CI gates were added.

No import boundaries were enforced.

No vocabulary fields were made merge-blocking.

No parser/runtime/analytics/local app/workbook/webhook/Apps Script/Sheets/AI or
production behavior was changed.

No secrets, raw logs, generated data, runtime artifacts, workbook exports,
local JSONL artifacts, generated SQLite files, or local-only artifacts were
touched.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #221.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/221

Branch:
codex/internal-boundary-workflow-vocabulary

Contract:
docs/contracts/internal_project_boundary_workflow_vocabulary.md

Implementation handoff:
docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md

Goal:
Review the Codex D fix for the P2 finding that Future AI Integration appeared in edited template vocabulary without the contract-required non-authorization caveat. Verify that internal project area, truth-owner, and bridge-code metadata remain advisory routing/review metadata, not gates.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/review.md
- docs/agent_threads/contract_test.md
- docs/templates/contract_test_report.md
- docs/internal_project_map.md
- docs/decisions/ADR-0006-repository-boundary-strategy.md
- docs/contracts/internal_project_boundary_workflow_vocabulary.md
- docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md
- docs/templates/problem_representation.md
- docs/templates/module_contract.md
- docs/templates/implementation_handoff.md
- docs/templates/contract_test_report.md
- docs/templates/workflow_handoff.md
- .github/ISSUE_TEMPLATE/module_workflow.yml
- .github/pull_request_template.md

Review focus:
- `Project Layer` remains separate from `Internal Project Area`.
- The issue template keeps the existing project-layer field and adds only an optional internal-project-area field.
- The module contract template asks for internal project area, truth owner, and bridge-code status.
- The implementation handoff template carries internal project area, truth owner, bridge-code status, and contracted-area status.
- The contract-test report template asks reviewers to verify internal project area and bridge-code classification without creating a new finding lifecycle category.
- The workflow handoff template documents optional `internal_project_area`, `truth_owner`, and `bridge_code_status` keys while preserving older handoff compatibility.
- The PR template asks for internal project area, truth owner, bridge-code status, and downstream consumers without adding merge authority.
- Future AI Integration wording is clearly deferred and does not authorize OpenAI/model-provider runtime integration, AI coaching evaluation, AI-owned truth, hidden-card truth, gameplay correctness truth, or strategic certainty.
- Title prefix guidance is preserved without forcing historical issue/PR renames.
- No docs wording makes vocabulary fields merge-blocking or authorizes protected-surface changes.
- No forbidden runtime, source, test, tool, package, CI, fixture, snapshot, generated, local-only, secret, raw log, workbook, webhook, Apps Script, Sheets, AI, or production surfaces were touched.

Validation to run or verify:
git status --short --branch
git diff --check
py tools\check_agent_docs.py
py -c "from pathlib import Path; import yaml; yaml.safe_load(Path('.github/ISSUE_TEMPLATE/module_workflow.yml').read_text())"
@'
docs/contracts/internal_project_boundary_workflow_vocabulary.md
docs/templates/problem_representation.md
docs/templates/module_contract.md
docs/templates/implementation_handoff.md
docs/templates/contract_test_report.md
docs/templates/workflow_handoff.md
.github/ISSUE_TEMPLATE/module_workflow.yml
.github/pull_request_template.md
docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/internal_project_boundary_workflow_vocabulary.md
docs/templates/problem_representation.md
docs/templates/module_contract.md
docs/templates/implementation_handoff.md
docs/templates/contract_test_report.md
docs/templates/workflow_handoff.md
.github/ISSUE_TEMPLATE/module_workflow.yml
.github/pull_request_template.md
docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin

Do not edit implementation unless explicitly asked.
Do not move files, rename packages, change imports, split repositories, add CI gates, enforce import boundaries, or make vocabulary fields merge-blocking.
Do not change parser/runtime/analytics/local app/workbook/webhook/Apps Script/Sheets/AI/production behavior.
Do not touch secrets, raw logs, generated data, runtime artifacts, workbook exports, local JSONL artifacts, generated SQLite files, or local-only artifacts.
Do not stage, commit, push, open a PR, merge, close issue #221, or target main.

Output:
- findings first, ordered by severity
- contract matches
- validation run and result
- protected-surface and secret/private-marker status
- whether forbidden scope was touched
- recommendation: approve, request Codex D fix, request Codex B clarification, or split follow-up
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/221"
  tracker: "N/A"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/internal_project_boundary_workflow_vocabulary.md"
  implementation_handoff: "docs/implementation_handoffs/internal_project_boundary_workflow_vocabulary_comparison.md"
  target_artifact: "docs/contract_test_reports/internal_project_boundary_workflow_vocabulary.md"
  risk_tier: "Medium"
  branch: "codex/internal-boundary-workflow-vocabulary"
  internal_project_area: "Quality / Governance"
  truth_owner: "Governance templates and workflow metadata"
  bridge_code_status: "not_bridge_code"
  finding_fixed:
    - "P2: Future AI Integration appeared in edited template vocabulary without the contract-required non-authorization caveat."
  validation:
    - "git status --short --branch -> expected tracked template edits plus untracked contract and handoff"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed, 0 errors, 0 warnings"
    - "YAML parse for .github/ISSUE_TEMPLATE/module_workflow.yml -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 7 expected workflow-authority warnings"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "focused rg caveat check -> affected template wording now includes deferred/non-authorization caveat"
  stop_conditions:
    - "Do not move files, rename packages, change imports, split repositories, add CI gates, enforce import boundaries, or make vocabulary fields merge-blocking."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/Apps Script/Sheets/AI/production behavior."
    - "Do not touch secrets, raw logs, generated data, runtime artifacts, workbook exports, local JSONL artifacts, generated SQLite files, or local-only artifacts."
```
