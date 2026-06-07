# Internal Project Boundary Annotation And Organization Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Issue And Contract

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/218
- Tracker: N/A
- Contract:
  `docs/contracts/internal_project_boundary_annotation_organization.md`
- Source artifact:
  GitHub issue problem representation for internal project boundary annotation
  and organization
- Branch: `codex/internal-project-boundary-annotation`
- Risk tier: Medium

## Branch And Git Status

Initial status:

```text
## codex/internal-project-boundary-annotation...origin/codex/analytics-foundation
?? docs/contracts/internal_project_boundary_annotation_organization.md
```

The untracked contract was treated as the Codex B source artifact. No unrelated
dirty or untracked files were absorbed into this implementation pass.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/internal_project_boundary_annotation_organization.md`
- `docs/contracts/internal_project_boundaries.md`
- `docs/implementation_handoffs/internal_project_boundaries_comparison.md`
- `docs/contract_test_reports/internal_project_boundaries.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/decisions/README.md`
- `docs/project_roadmap.md`
- `pyproject.toml`
- `src/mythic_edge_parser/`
- `frontend/`
- `tools/`
- `tests/`
- `docs/contracts/`
- `docs/implementation_handoffs/`
- `docs/contract_test_reports/`
- `.github/`
- GitHub issue #218

## Current Behavior Compared To Contract

### What The Annotation/Organization Pass Is Supposed To Own

Issue #218 is supposed to make internal project ownership discoverable without
changing the physical repo layout. The contract authorizes a central docs map
that names project ownership, path-family classification, bridge-code labels,
ambiguous module policy, flat docs/test/source conventions, deferred physical
organization work, protected surfaces, and validation expectations.

### What The Repo Already Provides

- Accepted ADR-0006 defines monorepo-first repository-boundary strategy.
- Issue #215 and its contract/test package already define the internal project
  vocabulary and dependency direction.
- `docs/contracts/`, `docs/implementation_handoffs/`, and
  `docs/contract_test_reports/` are already flat and prefix-based.
- `tests/` is already flat and mostly filename-prefix based.
- `src/mythic_edge_parser/local_app/` and `frontend/` already make local app/UI
  ownership more visible than the broad `app/` namespace.
- `pyproject.toml` confirms the single package name and current package-data
  layout.
- Existing governance and ADR docs already preserve parser truth ownership and
  protected-surface boundaries.

### Gap Remaining

No central `docs/internal_project_map.md` existed. Ownership for broad path
families and bridge-code candidates was spread across the #215 contract, ADRs,
handoffs, review reports, and naming conventions. That made the repo safe but
not yet easy to scan.

## Implementation Option Chosen

Docs-only map plus implementation handoff.

No source comments, README links, directory README indexes, test markers,
boundary checker, import graph gate, file moves, package changes, import
changes, CI gates, or runtime behavior changes were implemented.

## Files Changed

- `docs/internal_project_map.md`
- `docs/implementation_handoffs/internal_project_boundary_annotation_organization_comparison.md`

Untracked source artifact preserved:

- `docs/contracts/internal_project_boundary_annotation_organization.md`

## Exact Docs/Map/Governance Sections Changed

### `docs/internal_project_map.md`

Created with these contract-required sections:

- scope;
- authority note citing issue #218, issue #215, and ADR-0006;
- "How To Use This Map";
- internal project vocabulary;
- current flat-layout policy;
- ownership table for required path families;
- bridge-code table;
- ambiguous-module policy;
- docs artifact grouping guidance;
- test naming guidance;
- source ownership guidance;
- deferred item #3 scope;
- protected surfaces;
- validation expectations;
- follow-up questions.

The ownership table uses repo-relative paths only and includes:

- `path_or_family`;
- `primary_project`;
- `classification`;
- `truth_owner`;
- `allowed_consumers_or_readers`;
- `notes_or_boundary`.

The bridge-code table classifies the contract-required candidates and includes:

- `bridge_from`;
- `bridge_to`;
- `primary_truth_owner`;
- `input_boundary`;
- `output_boundary`;
- `forbidden_interpretation`;
- `status`;
- `notes`.

### `docs/implementation_handoffs/internal_project_boundary_annotation_organization_comparison.md`

Created this implementation handoff with comparison, scope confirmation,
validation, reviewer focus, pasteable Codex E prompt, and workflow handoff.

## Code/Test/Interface Status

- Code changed: no.
- Tests changed: no.
- Docs-only: yes.
- Governance-only: yes.
- Map-only plus handoff: yes.
- Runtime interface changes: none.
- Package/import changes: none.
- CI gates added: no.
- Boundaries enforced: no.

## Protected And Forbidden Scope Confirmation

No files were moved. No packages were renamed. No imports were changed. No
repositories were split. No CI gates were added. No import boundaries were
enforced.

No intentional changes were made to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- event kind values;
- parser payload shapes;
- extractor behavior;
- match identity;
- game identity;
- deduplication;
- analytics behavior;
- SQLite schema or migrations;
- local app/backend behavior;
- frontend UI behavior;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- AI/model-provider behavior;
- package name;
- runtime artifacts;
- fixtures;
- snapshots;
- generated data;
- local-only artifacts.

No directory README indexes, source comments, test markers, boundary checkers,
import graph gates, `.github` edits, `README.md` edits, ADR edits, package
metadata edits, source edits, frontend edits, tool edits, test edits, fixture
edits, or generated artifact edits were made.

## Validation Run

- `git status --short --branch` -> on
  `codex/internal-project-boundary-annotation...origin/codex/analytics-foundation`;
  untracked files are the contract, this handoff, and
  `docs/internal_project_map.md`.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed; checked 46 files, errors 0,
  warnings 0.
- Path-scoped protected-surface scan over the contract, map, and handoff ->
  passed; forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over the contract, map, and handoff
  -> passed; forbidden 0, warnings 0.
- `git diff --name-only` -> no output because all changed files are untracked.
- `git ls-files --others --exclude-standard` -> only the contract, map, and
  handoff are untracked.
- Direct ASCII/trailing-whitespace/final-newline checks for the new map and
  handoff -> passed.
- Generated artifact status check for SQLite, database, JSONL, Player.log,
  WAL/SHM/journal markers in `git status --short --ignored=matching` -> no
  matches.

## Generated Artifact Status

No generated SQLite database files, raw logs, local JSONL artifacts, runtime
status files, transport failure artifacts, workbook exports, frontend build
outputs, or local-only artifacts were intentionally created or modified by this
pass.

## Remaining Risks Or Unverified Layers

- The map is a docs snapshot and can become stale as modules move or new
  contracts land.
- Ambiguous bridge areas remain intentionally unresolved until future scoped
  contracts.
- No source-level annotations were added by design.
- No import-boundary checker or import graph report was added by design.
- Live workbook state was not inspected.
- Deployed Apps Script state was not inspected.
- Production behavior was not exercised.

## Reviewer Focus

Codex E should verify:

- `docs/internal_project_map.md` follows the contract-required structure.
- Required path families are covered at the path-family level.
- Bridge-code candidates are classified or explicitly marked ambiguous.
- Ambiguous entries do not imply file moves, import changes, or runtime
  behavior changes.
- Docs grouping guidance remains inside the map only.
- No forbidden files outside the allowed contract/map/handoff set changed.
- Secret/private-marker warnings, if any, are policy wording rather than
  exposed secret or private data.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #218.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/218

Tracker:
N/A

Branch:
codex/internal-project-boundary-annotation

Contract:
docs/contracts/internal_project_boundary_annotation_organization.md

Implementation handoff:
docs/implementation_handoffs/internal_project_boundary_annotation_organization_comparison.md

Primary artifact:
docs/internal_project_map.md

Risk tier:
Medium

Task:
Review the internal project boundary annotation and organization implementation against the contract. Lead with findings ordered by severity. Verify that the pass stayed docs-only and created only the authorized map and handoff artifacts.

Review focus:
- docs/internal_project_map.md follows the contract-required structure.
- The map cites issue #218, issue #215, and accepted ADR-0006.
- The map uses the accepted internal project vocabulary.
- The map documents current flat-layout policy.
- The ownership table covers required path families using repo-relative paths.
- The bridge-code table classifies required candidates or marks ambiguity explicitly.
- Docs grouping, test naming, source ownership, deferred item #3 scope, protected surfaces, validation expectations, and follow-up questions are present.
- The implementation did not create directory README indexes, source comments, test markers, boundary checkers, import graph gates, source edits, tooling edits, .github edits, package metadata edits, fixture edits, snapshot edits, or generated artifacts.
- No parser/runtime/analytics/local app/workbook/webhook/Apps Script/Sheets/AI/production behavior changed.

Validation:
git status --short --branch
git diff --check
py tools\check_agent_docs.py
@'
docs/contracts/internal_project_boundary_annotation_organization.md
docs/internal_project_map.md
docs/implementation_handoffs/internal_project_boundary_annotation_organization_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/internal_project_boundary_annotation_organization.md
docs/internal_project_map.md
docs/implementation_handoffs/internal_project_boundary_annotation_organization_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
git diff --name-only

Do not:
- Move files.
- Rename packages.
- Change imports.
- Split repositories.
- Add CI gates.
- Enforce import boundaries.
- Create directory README indexes.
- Add source comments.
- Add test markers.
- Add boundary checkers.
- Add import graph gates.
- Change parser/runtime/analytics/local app/workbook/webhook/Apps Script/Sheets/AI/production behavior.
- Touch secrets, raw logs, generated data, runtime artifacts, transport failure payloads, workbook exports, local JSONL artifacts, generated SQLite files, fixtures, snapshots, drift baselines, or local-only artifacts.
- Stage, commit, push, open a PR, merge, close issue #218, or mark any tracker complete unless explicitly asked.

Final report must include:
- role performed
- issue reviewed
- contract/handoff/map reviewed
- findings ordered by severity
- validation run and result
- protected-surface status
- secret/private-marker status
- generated artifact status
- forbidden scope status
- recommendation: route to D, B/A, F, or accept/no-op
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/218"
  tracker: "N/A"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/internal_project_boundary_annotation_organization.md"
  target_artifact: "docs/contract_test_reports/internal_project_boundary_annotation_organization.md"
  implementation_handoff: "docs/implementation_handoffs/internal_project_boundary_annotation_organization_comparison.md"
  primary_artifact: "docs/internal_project_map.md"
  risk_tier: "Medium"
  branch: "codex/internal-project-boundary-annotation"
  validation:
    - "git status --short --branch -> scoped untracked contract/map/handoff only"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "git diff --name-only -> no output because files are untracked"
    - "git ls-files --others --exclude-standard -> contract/map/handoff only"
    - "direct ASCII/trailing-whitespace/final-newline checks -> passed"
    - "generated artifact status check -> no SQLite/DB/JSONL/Player.log/WAL/SHM/journal matches"
  stop_conditions:
    - "Do not move files, rename packages, change imports, split repositories, add CI gates, or enforce import boundaries."
    - "Do not create directory README indexes, source comments, test markers, boundary checkers, or import graph gates in issue #218."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/Apps Script/Sheets/AI/production behavior."
```
