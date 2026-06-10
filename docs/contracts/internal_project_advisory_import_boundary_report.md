# Internal Project Advisory Import-Boundary Report Contract

## Module

`internal_project_advisory_import_boundary_report`

## Source Issue

GitHub issue: `#334` (`[architecture] Advisory import-boundary report before physical reorganization`)

## Role And Scope

Codex B: Module Contract Writer.

This contract defines the first advisory import-boundary report Mythic Edge should produce before planning physical package moves, package splits, runtime file moves, or import rewrites.

This is a docs/governance contract only. It does not authorize source moves, package renames, import edits, runtime behavior changes, package-data rewrites, or CI gates.

## Risk Tier

Medium-High.

The report itself is read-only and advisory, but its findings are intended to guide later high-risk repository organization work. Incorrect classification could cause future Codex threads to move files across truth boundaries too early, miss hidden coupling, or accidentally convert a temporary bridge import into permanent architecture.

## Owning Layer

Quality / Governance.

The report may inspect all internal project areas, but it does not become authority over parser truth, analytics truth, Match Journal truth, workbook schema truth, local app runtime behavior, or release readiness. It is evidence for future contracts and reviews.

## Source Artifacts

The advisory report should be based on the current branch state and at least these artifacts:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/internal_project_map.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
- `docs/contracts/internal_project_boundaries.md`
- `docs/contracts/internal_project_boundary_annotation_organization.md`
- `docs/contracts/internal_project_boundary_workflow_vocabulary.md`
- `pyproject.toml`
- `src/mythic_edge_parser/`
- `tests/`
- `tools/`
- `frontend/`

The report may reference issue `#334` as the source problem representation. If it uses live GitHub issue text, it must summarize only non-secret governance context.

## Contract Artifact

This file is the contract artifact:

- `docs/contracts/internal_project_advisory_import_boundary_report.md`

The expected later advisory report artifact is:

- `docs/contract_test_reports/internal_project_advisory_import_boundary_report.md`

The later report may be produced by Codex E as a contract-test or architecture-audit report. A Codex C implementation thread is not required for the first slice unless a later issue authorizes a committed advisory checker.

## Goal

Produce a current, read-only map of Mythic Edge import boundaries before any physical reorganization work begins.

The report should answer:

- Which internal project areas currently import or depend on each other?
- Which dependencies are expected and low-risk in the current flat package layout?
- Which dependencies are bridge-code dependencies that need documentation before movement?
- Which dependencies are ambiguous and need a follow-up issue before package moves?
- Which dependencies would block physical movement unless an explicit migration contract is written?
- Which tests, tools, and frontend imports should be classified separately from production Python source imports?

The report should help future Codex threads decide what to move, what to leave flat, what to wrap behind stable interfaces, and what to defer.

## Non-Goals

This contract does not authorize:

- moving files
- renaming packages
- changing imports
- splitting repositories
- adding import-boundary enforcement
- adding CI gates
- creating failing validation checks
- changing parser behavior
- changing parser runtime state decomposition
- changing analytics schema, migrations, or ingest behavior
- changing local app behavior
- changing Match Journal behavior
- changing workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI behavior, AI/coaching behavior, Line Tracer behavior, or release behavior
- committing generated import graphs, local-only reports, caches, databases, logs, or private artifacts

## Current Observed Behavior To Preserve

Mythic Edge currently uses one Python package root under `src/mythic_edge_parser/`, with several internal project areas sharing that package. This flat layout is intentional for now.

The current docs already recognize that:

- ADR-0006 accepts a single-repo strategy while allowing future separation only through scoped contracts and reviews.
- ADR-0007 accepts parser runtime-state decomposition one cluster at a time, without broad parser rewrites or package moves.
- `docs/internal_project_map.md` names internal project areas and documents current bridge-code areas.
- `docs/contracts/internal_project_boundaries.md` requires current import graph inspection before future physical movement.
- `docs/contracts/internal_project_boundary_annotation_organization.md` intentionally did not create an import checker or import graph report.

The advisory report must preserve this current posture: measure first, classify second, and defer movement until a later scoped issue authorizes it.

## Internal Project Areas

The report should classify imports using the vocabulary in `docs/internal_project_map.md`:

- Parser
- Corpus / Provenance
- Analytics
- Local App / UI
- Workbook / Transport
- Quality / Governance
- Future AI Integration
- Shared Support
- Generated / Local Artifacts
- External / Collaboration Surface

If a file does not fit cleanly, the report should mark it as `ambiguous_needs_follow_up` rather than forcing a false classification.

## Import Edge Classification Model

Each meaningful edge should be classified with this shape:

- `source_file`: file containing the import
- `source_area`: internal project area for the source file
- `imported_module_or_file`: imported module or file target
- `target_area`: internal project area for the imported target, when known
- `layer_context`: one of `production_src`, `tests`, `tools`, `frontend`, `docs`, `package_metadata`, or `unknown`
- `import_kind`: `python_runtime`, `python_test`, `python_tool`, `typescript_frontend`, `package_data`, `documentation_reference`, or `unknown`
- `classification`: one of the classifications below
- `confidence`: `high`, `medium`, or `low`
- `risk`: `info`, `low`, `medium`, or `high`
- `move_impact`: what this edge means for future file movement
- `recommended_follow_up`: none, document bridge, add facade, split later contract, block movement, or investigate

The report does not need one table row for every identical import if grouping is clearer. It may summarize repeated test imports or same-area imports, but it must preserve enough examples for future implementers to find the coupling.

## Required Classifications

Use these classification labels:

- `same_area_allowed`: source and target are in the same internal project area.
- `downstream_consumes_upstream_allowed`: a downstream layer consumes parser-owned or analytics-owned facts without taking over truth.
- `quality_governance_inspection_allowed`: tests, reports, governance tools, or validation tools inspect another area.
- `shared_support_allowed`: both areas use stable shared support such as config, paths, package-data access, or small neutral helpers.
- `bridge_expected_documented`: a cross-area dependency is expected and already documented as bridge code.
- `bridge_expected_needs_documentation`: a cross-area dependency appears necessary today but needs explicit bridge labeling before movement.
- `test_tool_only`: a dependency exists only in tests or local tooling and should not be treated as a production runtime direction.
- `frontend_local_only`: a frontend import is within the frontend package and does not import Python internals directly.
- `package_data_coupling`: package metadata or resource loading couples runtime behavior to current package layout.
- `ambiguous_needs_follow_up`: the import direction or ownership is unclear.
- `suspected_forbidden_direction`: the dependency appears to violate current truth or layer ownership rules and needs a follow-up before movement.
- `move_blocker`: the dependency must be resolved or explicitly preserved before a physical move can proceed.
- `out_of_scope_generated_or_local`: the path is generated, local-only, private, or otherwise not part of repo-owned import architecture.

## Direction Rules

The report should apply these direction rules conservatively:

- Parser code may depend on parser modules, standard library, approved third-party libraries, and neutral shared support. Parser code must not depend on analytics, local app UI, workbook transport, frontend, AI, or future release tooling to produce parser truth.
- Corpus / Provenance code may support parser QA and evidence ledgers, but must not become a second parser or override parser truth.
- Analytics code may consume parser-normalized facts, evidence-ledger fields, migrations, and local analytics helpers. Analytics must not reinterpret raw Player.log lines or parser internals into alternate truth.
- Local App backend code may orchestrate approved local app, analytics, live watcher, Match Journal, and setup surfaces. Imports that touch parser stream/state/live capture should be classified as bridge code and reviewed before movement.
- Frontend code should communicate through local app APIs and frontend-local TypeScript types/status helpers. It must not import Python package internals.
- Workbook / Transport code may consume parser row contracts and transport outputs. It must not own parser, analytics, local app, or AI truth.
- Quality / Governance code may inspect every area for validation, reports, and contracts, but those imports do not authorize runtime coupling.
- Future AI Integration remains deferred. Any AI imports or model-provider boundaries should be marked for separate governance unless already explicitly authorized.

## Production, Test, Tool, And Frontend Separation

The report must not mix all imports into one undifferentiated risk pile.

It must separate:

- production Python source imports under `src/`
- tests under `tests/`
- tools under `tools/`
- frontend imports under `frontend/`
- package metadata and package-data coupling in `pyproject.toml`
- documentation references in `docs/`

Test and tool imports may intentionally cross boundaries for validation, fixture generation, advisory inspection, or developer workflow. They can still reveal future movement costs, but they are not automatically production architecture violations.

Frontend imports should be evaluated as local UI imports unless they reference Python package internals or backend implementation details. Browser-facing behavior remains bounded by local app APIs.

## Required Report Sections

The later advisory report must include:

1. Executive summary.
2. Branch, base, and git status at inspection time.
3. Source artifacts inspected.
4. Analysis method and exact commands used.
5. Current package/layout summary.
6. Import inventory summary, including approximate counts and scanned scopes.
7. Internal project area mapping table.
8. Production source import-edge findings.
9. Tests/tools import-edge findings.
10. Frontend import-edge findings.
11. Package-data and resource-loading coupling observations.
12. Expected bridge-code dependencies.
13. Ambiguous or risky dependencies.
14. Suspected forbidden directions, if any.
15. Move blockers before physical reorganization.
16. Recommended follow-up issue list.
17. Explicit no-gate/no-enforcement statement.
18. Protected-surface and privacy assessment.
19. Validation evidence.
20. Next recommended role.
21. Workflow handoff block.

## Analysis Method

The first report should use read-only inspection and simple repository searches.

Minimum command family:

```powershell
git status --short --branch
rg -n "^(from|import) mythic_edge_parser|from mythic_edge_parser|import mythic_edge_parser" src tests tools -g "*.py" --stats
rg -n "mythic_edge_parser|from \\.|import .*" frontend -g "*.ts" -g "*.tsx" -g "*.js" -g "*.jsx" --stats
```

The report may use additional `rg`, `git grep`, or short local analysis commands if needed. Temporary local scripts are allowed for analysis only if they are not committed and do not read private/generated artifacts.

The first slice should not add a committed checker. If a later issue wants repeatable advisory tooling, that should be a separate contract.

## Evidence Rules

The report should quote or summarize only repo-owned source, docs, and issue text needed for architecture classification.

The report must not include:

- raw Player.log content
- private JSONL payloads
- generated SQLite contents
- raw runtime logs
- private retry-queue request bodies
- workbook exports
- secrets, credentials, API keys, tokens, webhook URLs, spreadsheet IDs, or environment values
- raw local absolute private paths except where already intentionally documented as public repo examples

Use symbolic names such as `<repo>`, `<worktree>`, `<app-data-root>`, or `<local-artifact>` when path examples are needed.

## Protected Surfaces

The advisory report must not change or authorize changes to:

- parser behavior
- parser state final reconciliation
- parser event classes
- match/game identity
- deduplication
- parser payload shapes
- analytics schema, migrations, or ingest semantics
- local app runtime behavior
- Match Journal truth ownership
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets behavior
- output transport
- production behavior
- OpenAI/model-provider behavior
- AI/coaching behavior
- Line Tracer behavior
- hidden-card, archetype, player-mistake, or gameplay-advice behavior
- CI gate behavior
- package layout, imports, or module names

Any suspected need to touch these surfaces must be routed to a follow-up issue and contract.

## Acceptance Criteria

The later advisory report is acceptable when it:

- identifies the current branch/base/status used for inspection
- distinguishes production source imports from tests, tools, frontend, package metadata, and docs
- classifies observed import edges using the labels in this contract
- names expected bridge-code dependencies without treating them as immediate defects
- identifies ambiguous or risky edges that would matter before physical movement
- identifies package-data or resource-loading assumptions that could break during reorganization
- recommends follow-up issues without making source changes
- explicitly states that it is advisory and non-gating
- preserves parser truth ownership and protected-surface rules
- contains no raw/private/generated artifact data
- includes validation evidence

## Validation Expectations

For this contract artifact, Codex B should run:

```powershell
git diff --check -- docs\contracts\internal_project_advisory_import_boundary_report.md
py tools\check_agent_docs.py
@'
docs/contracts/internal_project_advisory_import_boundary_report.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/internal_project_advisory_import_boundary_report.md
'@ | py tools\check_secret_patterns.py --paths-from-stdin
```

For the later advisory report, Codex E should run the same checks over:

```text
docs/contract_test_reports/internal_project_advisory_import_boundary_report.md
```

Codex E should also run the read-only import scan commands listed in the Analysis Method section.

## Expected Next Role

Recommended next role: Codex E: Module Reviewer / Contract Tester / Architecture Audit Reporter.

Reason: the next artifact is an advisory report under `docs/contract_test_reports/`, and the first slice requires read-only evidence classification rather than implementation.

Route to Codex C only if a later issue authorizes a committed advisory checker, docs template update, or workflow tooling change.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester / Architecture Audit Reporter.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/334

Branch:
codex/advisory-import-boundary-report

Contract:
docs/contracts/internal_project_advisory_import_boundary_report.md

Goal:
Produce the advisory import-boundary report before any physical package moves.

Expected report artifact:
docs/contract_test_reports/internal_project_advisory_import_boundary_report.md

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/internal_project_map.md
- docs/decisions/ADR-0006-repository-boundary-strategy.md
- docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md
- docs/contracts/internal_project_boundaries.md
- docs/contracts/internal_project_boundary_annotation_organization.md
- docs/contracts/internal_project_boundary_workflow_vocabulary.md
- docs/contracts/internal_project_advisory_import_boundary_report.md
- pyproject.toml
- src/mythic_edge_parser/
- tests/
- tools/
- frontend/

Inspect first:
- git status --short --branch
- gh issue view 334

Run read-only import scans:
- rg -n "^(from|import) mythic_edge_parser|from mythic_edge_parser|import mythic_edge_parser" src tests tools -g "*.py" --stats
- rg -n "mythic_edge_parser|from \\.|import .*" frontend -g "*.ts" -g "*.tsx" -g "*.js" -g "*.jsx" --stats

Task:
Create docs/contract_test_reports/internal_project_advisory_import_boundary_report.md. Classify current import edges by internal project area, production/test/tool/frontend context, bridge status, ambiguity, and movement risk. Identify blockers and follow-up issues before physical package moves.

Do not implement code.
Do not move files.
Do not rename packages.
Do not change imports.
Do not add a checker or CI gate.
Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.
Do not read, copy, print, or commit raw/private/generated artifacts.

Validation:
- git diff --check -- docs\contract_test_reports\internal_project_advisory_import_boundary_report.md
- py tools\check_agent_docs.py
- path-scoped protected-surface scan for the report file
- path-scoped secret/private-marker scan for the report file

Final output must include:
- role performed
- issue reviewed
- contract used
- report artifact produced
- import-boundary summary
- ambiguous/risky edges
- move blockers
- recommended follow-up issues
- validation results
- protected-surface status
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/334"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue problem representation"
  contract_artifact: "docs/contracts/internal_project_advisory_import_boundary_report.md"
  target_artifact: "docs/contract_test_reports/internal_project_advisory_import_boundary_report.md"
  branch: "codex/advisory-import-boundary-report"
  risk_tier: "Medium-High"
  decision: "Produce a read-only advisory import-boundary report before planning physical package moves; do not add an import checker or gate in the first slice."
  stop_conditions:
    - "Do not implement code in the advisory report pass."
    - "Do not move files, rename packages, change imports, split packages, or add CI gates."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not read, copy, print, store, or commit raw/private/generated artifacts."
```
