# External Integration And Collaboration Surfaces Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/79

## Tracker

N/A

## Contract

`docs/contracts/external_integration_collaboration_surfaces.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Worktree

- Branch confirmed before editing: `main`
- Initial worktree state: `## main...origin/main` with only
  `docs/contracts/external_integration_collaboration_surfaces.md` untracked
- Unrelated changes: none observed
- The untracked source contract was inspected as the active contract and was
  not treated as unrelated work

## What External Surfaces Are Supposed To Own

External integrations and collaboration spaces may help Mythic Edge inspect,
research, coordinate, publish, store, transport, explain, or summarize work.
They do not own parser truth, deterministic scoring or evaluation, repo
authority, workbook schema truth, merge/deploy readiness, credential policy, or
production state by default.

Parser/state remains the MTGA event interpretation and normalized match/game
truth owner. Deterministic local code may own future scoring or evaluation only
when separately contracted. AI/LLM output may explain, enrich, recommend, or
hypothesize, but it does not own parser-managed truth.

## Current Repo Behavior Before This Pass

The repo already partially matched the contract:

- `AGENTS.md`, `docs/agent_constitution.md`, and
  `docs/codex_module_workflow.md` preserved parser truth ownership and AI as a
  downstream consumer.
- `docs/agent_rules.yml` already protected parser truth, secrets, local
  artifacts, protected surfaces, and Codex H advisory status.
- `docs/agent_threads/constitutional_lawyer.md` already treated tools,
  plugins, connectors, MCP servers, and local skills as tool surfaces unless a
  repo artifact grants authority.
- `docs/decisions/README.md` already required ADRs for persistent external
  integration, privacy, secrets, and data-retention policy.
- ADR-0001, ADR-0002, and ADR-0004 already covered parser truth, LLM
  explanation boundaries, and protected-surface authorization.

Remaining gaps before this pass:

- No dedicated external integration/collaboration surfaces ADR existed.
- Tool-surface guidance was strongest in Codex H context, not in a global
  machine-readable rule.
- Google Docs and Google Sheets collaboration boundaries were not consolidated
  in one durable policy.
- OpenAI documentation tooling and OpenAI API runtime integration were not
  separated in one external-surface decision.
- The PR template did not ask authors to disclose drift for external
  integrations or collaboration surfaces.

## What Changed

Implemented the narrow docs/ADR/rule updates authorized by issue #79 and the
contract:

- Added proposed `ADR-0005: External Integration And Collaboration Surfaces`.
- Indexed ADR-0005 in `docs/decisions/README.md`.
- Added a short entrypoint rule in `AGENTS.md` for external tools and
  collaboration surfaces.
- Added a concise constitution section for external integration and
  collaboration surfaces.
- Added a top-level `external_integration_surfaces` machine-readable rule in
  `docs/agent_rules.yml`.
- Added workflow guidance that external tools are access/collaboration
  surfaces unless current repo authority says otherwise.
- Added PR-template drift/checklist coverage for external integrations,
  collaboration surfaces, live Docs/Sheets, connector permissions, OpenAI API
  runtime behavior, and coaching evaluation.

No role docs or artifact templates beyond the PR template were changed because
the existing Codex H role doc and constitution feedback packet template already
contained the relevant tool-surface and storage guidance.

## Files Changed

- `.github/pull_request_template.md`
- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`
- `docs/decisions/README.md`
- `docs/implementation_handoffs/external_integration_collaboration_surfaces_comparison.md`

Also present as the source artifact:

- `docs/contracts/external_integration_collaboration_surfaces.md`

## Code Changed

No runtime code changed. This pass was governance/docs-only.

## Tests Added Or Updated

No Python tests were added or updated. The change is documentation, ADR,
rule-index, and PR-template only.

## Interface Changes

No runtime API, parser event, workbook, webhook, Apps Script, environment
variable, credential, or data shape changed.

Governance/documentation interfaces changed:

- New proposed ADR file: `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`
- New ADR index row in `docs/decisions/README.md`
- New top-level rule-index key: `external_integration_surfaces`
- New PR-template drift-budget row: `External integrations / collaboration surfaces`
- New PR-template protected-surface checklist item for external integrations,
  live Docs/Sheets, connector permissions, OpenAI API runtime behavior, and
  coaching evaluation

## Contract Matches

- Parser/state remains the truth owner for parser-managed MTGA facts.
- AI/LLM output remains explanation, enrichment, recommendation, inference, or
  hypothesis only.
- Google Sheets and Google Docs remain collaboration/storage/display surfaces,
  not parser truth or repo authority by default.
- Local Codex skills, MCP servers, plugins, and connectors remain tool-access
  surfaces.
- OpenAI documentation tooling is separated from OpenAI API runtime
  integration.
- OpenAI API runtime integration remains out of scope and requires a separate
  issue and contract.
- Coaching evaluation remains out of scope and requires a separate issue and
  contract.
- Secrets, credentials, environment variables, raw logs, runtime status files,
  failed posts, generated data, workbook exports, live external writes, and
  connector permission changes remain protected.
- Human approval boundaries for live external writes, permission changes,
  credential changes, sensitive data sharing, destructive external operations,
  and production changes were preserved.

## Contract Mismatches Resolved

- Added the contracted dedicated ADR candidate for durable external
  integration/collaboration policy.
- Added global machine-readable rule-index coverage instead of leaving
  tool-surface policy only under `constitution_feedback`.
- Added narrow entrypoint, constitution, workflow, and PR-template references
  so future threads can discover the policy without reading Codex H docs first.

## Missing Safeguards Or Missing Tests

Remaining non-blocking gaps for review:

- ADR-0005 is `Proposed`; it should become durable precedent only after review
  and merge through the approved workflow.
- No connector-specific examples were added to role docs. The ADR and rule
  index now provide the general boundary, but future Google Workspace or
  OpenAI runtime work may need narrower contracts.
- No live Google Workspace sharing/permission audit was performed; the contract
  explicitly left that as a separate possible safety issue.
- No runtime tests apply because no runtime behavior changed.

## Protected Surface Status

No parser/runtime/workbook/webhook/App Script protected behavior was changed.
No secrets, credentials, environment variables, raw logs, failed posts, runtime
status files, generated data, workbook exports, fixtures, snapshots, baselines,
live Docs/Sheets, connectors, plugins, MCP authorization, or OpenAI API runtime
integration were created or modified.

## Validation Run

```powershell
git status --short --branch
```

Result: passed. Branch is `main`; intended worktree changes are the governance
docs, proposed ADR, handoff, and the in-scope untracked source contract.

```powershell
git diff --check
```

Result: passed. No whitespace errors in the tracked diff.

```powershell
py tools\check_protected_surfaces.py --base origin/main
```

Result: passed. The HEAD-based check reported `changed_paths: 0`, `forbidden:
0`, `warnings: 0`; the worktree contains unstaged/untracked docs changes, so
the path-scoped check below is the meaningful protected-surface check for this
thread.

```powershell
@('.github/pull_request_template.md','AGENTS.md','docs/agent_constitution.md','docs/agent_rules.yml','docs/codex_module_workflow.md','docs/contracts/external_integration_collaboration_surfaces.md','docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md','docs/decisions/README.md','docs/implementation_handoffs/external_integration_collaboration_surfaces_comparison.md') | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Result: passed. Reported `changed_paths: 9`, `forbidden: 0`, `warnings: 4`.
Warnings were expected workflow-authority-doc warnings for
`.github/pull_request_template.md`, `docs/agent_constitution.md`,
`docs/agent_rules.yml`, and `docs/codex_module_workflow.md`; issue #79 and the
contract authorize narrow governance changes to those surfaces.

```powershell
py -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())"
```

Result: passed. YAML parsed successfully.

```powershell
Get-ChildItem 'docs\decisions' -Filter 'ADR-*.md' | Sort-Object Name | Select-Object -ExpandProperty Name
```

Result: passed. ADR files are numbered `ADR-0001` through `ADR-0005`; no number
was reused or skipped.

```powershell
rg -n "ADR-0005|Status: Proposed|Related issues|Related PRs|Related contracts|Related ADRs|## Decision|## Non-Goals|## Protected Surfaces Touched|## Supersedes|## Superseded By" docs\decisions\README.md docs\decisions\ADR-0005-external-integration-collaboration-surfaces.md
```

Result: passed. ADR-0005 is indexed and includes the expected required fields.

```powershell
rg -n "\s+$" <touched docs>
```

Result: passed. Direct trailing-whitespace scan found no matches in tracked and
untracked touched docs.

```powershell
py tools\check_agent_docs.py
```

Result: not available on this branch. The command failed because
`tools\check_agent_docs.py` does not exist in the current repo checkout.

## Still Unverified

- GitHub PR/review status for a future submitter pass.
- Whether issue #79 should be closed by a future PR; Codex C did not close it.
- Whether ADR-0005 should remain `Proposed` or be changed to `Accepted` at
  merge time by a future reviewed workflow.
- Live Google Docs, Google Sheets, Drive permissions, connector permissions,
  and external retention settings were not inspected or changed.

## Reviewer Focus

Codex E should verify:

- ADR-0005 satisfies the contract without authorizing runtime or live external
  behavior.
- The new `external_integration_surfaces` rule does not conflict with existing
  authority order, ADR policy, Codex H guidance, or protected-surface rules.
- Google Docs/Sheets, local skills, MCPs, plugins, connectors, OpenAI docs
  tooling, OpenAI API runtime integration, and coaching evaluation boundaries
  remain clearly separated.
- The PR-template additions are narrow and do not create new CI gates.
- No forbidden/protected surfaces or sensitive data entered the diff.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use [$mythic-edge-workflow](C:\Users\<redacted>\.codex\skills\mythic-edge-workflow\SKILL.md).

Act as Codex E: Module Reviewer / contract-test thread for issue #79:
https://github.com/Tahjali11/Mythic-Edge/issues/79

Contract:
docs/contracts/external_integration_collaboration_surfaces.md

Implementation handoff:
docs/implementation_handoffs/external_integration_collaboration_surfaces_comparison.md

Review the diff against the issue, contract, handoff, AGENTS.md, docs/agent_constitution.md, docs/agent_rules.yml, docs/codex_module_workflow.md, docs/decisions/README.md, ADR-0001, ADR-0002, ADR-0004, ADR-0005, and .github/pull_request_template.md.

Lead with findings. Verify that the implementation:
- keeps changes governance/docs-only
- includes an appropriate proposed ADR and ADR index entry
- keeps tools, local skills, MCPs, plugins, connectors, Google Docs, Google Sheets, OpenAI docs tooling, and AI output as access/collaboration/evidence/explanation surfaces by default
- separates OpenAI docs tooling from OpenAI API runtime integration
- keeps OpenAI API runtime integration and coaching evaluation out of scope
- preserves parser truth ownership, protected surfaces, branch/merge gates, secret policy, and human approval boundaries
- avoids live Docs/Sheets edits, connector/plugin/MCP authorization changes, credential changes, runtime code changes, parser behavior changes, workbook schema changes, webhook payload changes, and Apps Script behavior changes

Validation to check or rerun:
git status --short --branch
git diff --check
py tools\check_protected_surfaces.py --base origin/main
py -c "import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())"
If present on the review branch, run the repo governance docs checker as well.

Produce a contract-test report or review verdict with findings, missing tests or safeguards, validation evidence, protected-surface status, and next recommended role.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/79"
  tracker: "N/A"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/external_integration_collaboration_surfaces.md"
  target_artifact: "docs/contract_test_reports/external_integration_collaboration_surfaces.md"
  risk_tier: "Medium"
  branch: "main"
  validation:
    - "git status --short --branch -> passed; branch main with intended governance docs/source contract changes"
    - "git diff --check -> passed"
    - "py tools\\check_protected_surfaces.py --base origin/main -> passed; HEAD-based changed_paths 0"
    - "path-scoped protected-surface gate for touched docs -> passed with expected workflow-authority-doc warnings"
    - "py -c \"import pathlib, yaml; yaml.safe_load(pathlib.Path('docs/agent_rules.yml').read_text())\" -> passed"
    - "ADR numbering and ADR-0005 section grep -> passed"
    - "direct trailing-whitespace scan over touched docs -> passed"
    - "py tools\\check_agent_docs.py -> not available on this branch"
  stop_conditions:
    - "Do not change parser/runtime/workbook/webhook/App Script behavior."
    - "Do not promote tools, skills, MCPs, plugins, connectors, Docs, Sheets, or AI output into truth or authority surfaces."
    - "Do not create, rotate, print, or modify secrets or credentials."
    - "Do not add OpenAI API runtime integration."
    - "Do not edit live Google Docs or Google Sheets."
    - "Do not implement coaching evaluation."
    - "Do not open a PR, merge, close issue #79, or target production without explicit approval."
```
