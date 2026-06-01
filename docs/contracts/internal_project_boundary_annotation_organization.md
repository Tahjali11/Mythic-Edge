# Internal Project Boundary Annotation And Organization Contract

## Module

Internal project boundary annotation and organization for Mythic Edge.

Plain English: this contract defines a documentation-only pass that makes the
repo's internal project ownership easier to see without moving files, renaming
packages, changing imports, splitting repositories, adding gates, or changing
runtime behavior.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/218
- Related completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/215
- Related ADR: `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- Tracker: N/A
- Branch: `codex/internal-project-boundary-annotation`
- Risk tier: Medium

ADR-0006 prerequisite status observed during this Codex B pass:

```text
docs/decisions/ADR-0006-repository-boundary-strategy.md -> Status: Accepted
docs/decisions/README.md -> ADR-0006 row Status: Accepted
```

Observed local branch state during this Codex B pass:

```text
## codex/internal-project-boundary-annotation...origin/codex/analytics-foundation
519fec5 Accept ADR-0006 repository boundary strategy
```

The branch name matches issue #218, but the local branch currently tracks
`origin/codex/analytics-foundation`. Codex C/F/G should verify branch target
state before any submitter or PR work. This contract does not change branch
tracking.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/contracts/internal_project_boundaries.md`
- `docs/implementation_handoffs/internal_project_boundaries_comparison.md`
- `docs/contract_test_reports/internal_project_boundaries.md`
- current inventory under `docs/contracts/`
- current inventory under `docs/implementation_handoffs/`
- current inventory under `docs/contract_test_reports/`
- current inventory under `src/mythic_edge_parser/`
- current inventory under `frontend/`
- current inventory under `tools/`
- current inventory under `tests/`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- `pyproject.toml`

## Owning Layer

Primary owner: Quality / Governance.

This contract is an annotation and coordination contract. It does not create a
runtime API and does not change project truth ownership.

Truth boundaries remain:

- Parser owns MTGA event interpretation, parser event classes, parser routing,
  parser state, match identity, game identity, parser-owned deduplication,
  final reconciliation, and parser-normalized facts.
- Corpus / Provenance owns evidence, source, confidence, finality, drift,
  fixtures, replay evidence, and validation support. It must not become a
  second parser.
- Analytics owns local deterministic storage, views, summaries, and warnings
  from parser-normalized facts. It must not reinterpret raw Player.log entries
  or override parser-managed values.
- Local App / UI owns local access, display, import controls, setup status, and
  orchestration. It must not own parser truth or analytics truth.
- Workbook / Transport owns workbook-facing row contracts, sheet mappings,
  output transport, and Apps Script parity. It must not feed workbook or
  transport state back into parser truth.
- Quality / Governance owns contracts, ADRs, workflow docs, checks, validation
  selectors, and safety policy. It may inspect all layers, but must not become
  runtime product behavior.
- Future AI Integration remains deferred. It may later explain, summarize,
  classify, or propose hypotheses under separate contract, but must not own
  parser truth, analytics truth, workbook truth, hidden-card truth, gameplay
  correctness, or strategic certainty.

## Files Owned By This Contract

This Codex B contract pass may create or edit only:

- `docs/contracts/internal_project_boundary_annotation_organization.md`

Future Codex C implementation for issue #218 may create or edit only:

- `docs/internal_project_map.md`
- `docs/implementation_handoffs/internal_project_boundary_annotation_organization_comparison.md`

Future Codex E contract-test or review for issue #218 may create or edit only:

- `docs/contract_test_reports/internal_project_boundary_annotation_organization.md`

This contract does not authorize edits to:

- `README.md`
- `docs/decisions/*.md`
- `docs/contracts/README.md`
- `docs/implementation_handoffs/README.md`
- `docs/contract_test_reports/README.md`
- `docs/project_roadmap.md`
- `.github/*`
- `pyproject.toml`
- `src/**`
- `frontend/**`
- `tools/**`
- `tests/**`
- fixture, snapshot, generated, runtime, local-only, or private artifacts

If a later role concludes that README links, directory README indexes, source
comments, issue-template changes, PR-template changes, file moves, import
checks, or CI gates are needed, route to a follow-up issue or back to Codex B.

## Public Interface

The public interface is the future documentation artifact:

```text
docs/internal_project_map.md
```

The map is a human and Codex routing aid. It is not an import boundary checker,
not a CI gate, not a package layout, not an ADR, and not permission to move
files.

The map must expose:

- internal project ownership vocabulary;
- path-family ownership entries;
- bridge-code labels;
- ambiguous-module labels;
- docs artifact grouping guidance while directories stay flat;
- implementation handoff and contract-test report grouping guidance while
  directories stay flat;
- test naming guidance while `tests/` stays flat;
- source ownership guidance while `src/` stays flat;
- protected-surface reminders;
- deferred item #3 scope.

## Observed Current Behavior

- The repo remains a monorepo with one Python package named
  `mythic-edge-parser`.
- `pyproject.toml` uses `src` layout and packages analytics migrations as data
  under `mythic_edge_parser.app.analytics_migrations`.
- Most Python code remains under `src/mythic_edge_parser/`.
- `src/mythic_edge_parser/app/` contains parser, provenance, analytics,
  workbook/transport, runtime/status, and bridge modules.
- `src/mythic_edge_parser/parsers/` and `src/mythic_edge_parser/parsers/gre/`
  contain parser-family modules.
- `src/mythic_edge_parser/local_app/` contains local app backend, setup status,
  import job, path, and config code.
- `frontend/` contains the React/Vite local app UI.
- `tools/` contains quality/governance scripts, evidence/report builders,
  developer-app launcher tooling, Google Apps Script code, card-data tooling,
  and automation wrappers.
- `tests/` is flat and already relies on filename prefixes.
- `docs/contracts/`, `docs/implementation_handoffs/`, and
  `docs/contract_test_reports/` are flat and rely on filename prefixes.
- Existing issue #215 comparison and review artifacts were produced before
  ADR-0006 was accepted; they remain useful historical evidence, but current
  work should treat ADR-0006 as accepted precedent.

## Required Guarantees

### Documentation-Only Scope

Issue #218 implementation must be documentation-only.

Allowed documentation behavior:

- create a central ownership map;
- document current flat layout;
- document project ownership vocabulary;
- document bridge-code and ambiguous-module classification rules;
- document naming and grouping guidance;
- document future review and validation expectations;
- document deferred physical organization work.

Forbidden behavior:

- moving files;
- renaming packages;
- changing imports;
- splitting repositories;
- adding CI gates;
- enforcing import boundaries in code;
- adding a boundary checker;
- changing parser, analytics, local app, workbook, transport, Apps Script,
  Sheets, AI, or production behavior.

### Ownership Map Path

The central ownership map path for issue #218 must be:

```text
docs/internal_project_map.md
```

Reason: the map should be easy to find from the docs root and should not imply
that Mythic Edge already has a larger architecture-docs hierarchy.

Do not create `docs/architecture/` in this issue. A future architecture-docs
directory may be considered only if the documentation set grows enough to
justify it.

### Ownership Map Required Structure

`docs/internal_project_map.md` must include these sections:

- title and scope;
- authority note citing issue #218, issue #215, and ADR-0006;
- "How To Use This Map";
- internal project vocabulary;
- current flat-layout policy;
- ownership table for major path families;
- bridge-code table;
- ambiguous-module policy;
- docs artifact grouping guidance;
- test naming guidance;
- source ownership guidance;
- deferred item #3 scope;
- protected surfaces;
- validation expectations;
- follow-up questions.

The ownership table must use repo-relative paths only. Do not include local
absolute paths, private local file names, raw payloads, raw hashes, credentials,
tokens, webhook URLs, or machine-specific artifacts.

The ownership table must include at least these fields:

- `path_or_family`
- `primary_project`
- `classification`
- `truth_owner`
- `allowed_consumers_or_readers`
- `notes_or_boundary`

Allowed `primary_project` values:

- `Parser`
- `Corpus / Provenance`
- `Analytics`
- `Local App / UI`
- `Workbook / Transport`
- `Quality / Governance`
- `Future AI Integration`
- `Shared Support`
- `Generated / Local Artifacts`
- `External / Collaboration Surface`

Allowed `classification` values:

- `clear_owner`
- `shared_support`
- `bridge_code`
- `ambiguous_pending_follow_up`
- `deferred_future_boundary`
- `external_or_generated_excluded`

### Required Internal Project Vocabulary

The map must use the vocabulary accepted by ADR-0006 and the issue #215
boundary package:

- Parser
- Corpus / Provenance
- Analytics
- Local App / UI
- Workbook / Transport
- Quality / Governance
- Future AI Integration

The map may use `Shared Support` for helpers that intentionally support more
than one project area without owning upstream truth.

The map may use `Generated / Local Artifacts` for paths or patterns that must
remain ignored, local, generated, or non-authoritative.

The map may use `External / Collaboration Surface` for tools or spaces that
provide access, evidence, transport, collaboration, or explanation but do not
own repo authority or project truth.

### Path Families That Must Be Covered

The map must cover these path families:

- `AGENTS.md`
- `README.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/`
- `docs/templates/`
- `docs/decisions/`
- `docs/contracts/`
- `docs/implementation_handoffs/`
- `docs/contract_test_reports/`
- `docs/problem_representations/`
- `docs/project_roadmap.md`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/event_bus.py`
- `src/mythic_edge_parser/log/`
- `src/mythic_edge_parser/parsers/`
- `src/mythic_edge_parser/parsers/gre/`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/event_identity.py`
- parser diagnostics and runtime parser support under
  `src/mythic_edge_parser/app/`
- evidence-ledger, replay, drift, golden fixture, and corpus support under
  `src/mythic_edge_parser/app/`
- analytics storage, migration, ingest, views, and sidecar support under
  `src/mythic_edge_parser/app/`
- workbook/output/schema/export support under `src/mythic_edge_parser/app/`
- card catalog and `grp_id` support under `src/mythic_edge_parser/app/`
- `src/mythic_edge_parser/local_app/`
- `frontend/`
- `tools/`
- `tools/google_apps_script/Code.gs`
- `tests/`
- `tests/fixtures/`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- `pyproject.toml`
- generated or local data path families such as `data/`, SQLite database
  outputs, JSONL artifacts, raw logs, runtime status artifacts, workbook
  exports, and local-only artifacts.

This required coverage is about classification, not file edits.

### Bridge-Code Definition

Bridge code is code or documentation that intentionally sits between two or
more internal project areas and translates, exposes, orchestrates, validates, or
routes data across those areas without becoming the truth owner for the
upstream layer.

Bridge-code entries must name:

- source project area;
- consuming project area;
- primary truth owner;
- permitted dependency or data-flow direction;
- forbidden reverse-flow or truth-ownership shortcut;
- whether the bridge is stable, provisional, or ambiguous.

### Bridge-Code Labeling Rules

Bridge-code labels are documentation labels in `docs/internal_project_map.md`.
They are not source-code comments, decorators, constants, pytest markers, or
runtime metadata in this issue.

Allowed bridge-code fields:

- `bridge_from`
- `bridge_to`
- `primary_truth_owner`
- `input_boundary`
- `output_boundary`
- `forbidden_interpretation`
- `status`
- `notes`

Allowed bridge-code statuses:

- `stable_bridge`
- `provisional_bridge`
- `ambiguous_pending_follow_up`
- `deferred_future_boundary`

Required bridge-code candidate families to classify:

- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/card_catalog.py`
- `src/mythic_edge_parser/app/card_catalog_refresh.py`
- `src/mythic_edge_parser/app/arena_id_validation.py`
- `src/mythic_edge_parser/app/grp_id_catalog.py`
- `src/mythic_edge_parser/app/grp_id_candidates.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `tools/dev_app/`
- `tools/google_apps_script/Code.gs`
- validation and hardening tools under `tools/`

Codex C may classify additional bridge-code candidates discovered during
inspection, but must not edit the source files to annotate them.

### Ambiguous Module Classification Policy

When ownership is unclear, the map must prefer explicit uncertainty over false
certainty.

Use `ambiguous_pending_follow_up` when:

- the same file supports multiple project areas;
- current contracts disagree or are stale;
- a path has both runtime and validation uses;
- a path appears to transport data between layers without clearly owning truth;
- classification would imply a future file move, import rule, or package split.

Ambiguous entries must include:

- current best primary project, if known;
- known consumers or callers, if known from current docs or light inventory;
- why classification is ambiguous;
- which future issue type should resolve it.

Ambiguous entries must not:

- authorize a file move;
- authorize import changes;
- authorize source comments;
- authorize runtime behavior changes;
- treat the map as stronger than accepted ADRs, current contracts, or code.

### Docs Grouping And Index Expectations

For issue #218, docs grouping must remain content-only inside
`docs/internal_project_map.md`.

Do not create or edit directory index files in this issue, including:

- `docs/contracts/README.md`
- `docs/implementation_handoffs/README.md`
- `docs/contract_test_reports/README.md`

The map must document the current filename-prefix grouping convention while the
directories remain flat.

Required grouping prefixes to mention where present:

- `parser_*`
- `player_log_evidence_ledger_*`
- `analytics_*`
- `code_hardening_*`
- `repo_wide_*`
- `quality_*`
- `governance_*`
- `external_integration_*`
- `internal_project_*`
- `adr_*`
- `codex_h_*`

The map may recommend future prefixes, but must label them as future guidance
only. Future directory reorganization belongs to item #3 or a later scoped
issue.

### Implementation Handoff And Report Grouping Expectations

The map must state that implementation handoffs and contract-test reports stay
flat for now.

Required convention:

- implementation handoff for this issue:
  `docs/implementation_handoffs/internal_project_boundary_annotation_organization_comparison.md`
- future contract-test report for this issue:
  `docs/contract_test_reports/internal_project_boundary_annotation_organization.md`

The map may document that handoffs and reports should use the same module
prefix as their source contract, but must not move existing artifacts.

### Test Naming Guidance

Tests stay flat under `tests/` for issue #218.

The map must document current and future test filename guidance without
renaming tests.

Suggested filename prefixes by project area:

- Parser: `test_parser_*`, `test_*_parser.py`, `test_router_*`,
  `test_state.py`, `test_app_models.py`
- Corpus / Provenance: `test_evidence_*`, `test_golden_*`,
  `test_log_drift_*`, `test_feature_equity_*`
- Analytics: `test_analytics_*`
- Local App / UI: `test_analytics_local_app_*`,
  `test_analytics_*_ui_*` when applicable, and frontend tests under
  `frontend/src/*.test.ts*`
- Workbook / Transport: `test_sheet_*`, `test_webhook_*`,
  `test_workbook_*`, `test_app_outputs.py`
- Quality / Governance: `test_check_*`, `test_select_validation.py`,
  `test_hardening_*`, `test_pyright_*`, `test_*agent_docs*`

This is guidance only. Do not rename existing tests in issue #218.

### Source Ownership Guidance While `src/` Stays Flat

The map must document source ownership by path family and truth boundary, not by
moving or editing files.

Required guidance:

- Parser-core files must remain classified as Parser-owned.
- Evidence-ledger and drift-provenance files must remain classified as
  Corpus / Provenance or bridge support, not parser truth.
- Analytics files must remain classified as Analytics or parser-normalized
  ingest bridge code, not parser truth.
- Local app backend and frontend files must remain classified as Local App / UI
  or access/orchestration bridge code, not parser truth or analytics truth.
- Workbook output and Apps Script code must remain classified as
  Workbook / Transport or transport bridge code, not parser truth.
- Quality tools must remain classified as Quality / Governance, not runtime
  behavior.
- Future AI Integration must remain deferred unless a separate issue and
  contract authorize a concrete AI integration surface.

Source comments are not authorized in issue #218. If a future thread believes
a source-level bridge-code comment is necessary, it must route to a follow-up
contract that names the exact file and comment purpose.

## What Stays Flat For Now

These locations stay physically flat or unchanged in issue #218:

- `src/mythic_edge_parser/`
- `src/mythic_edge_parser/app/`
- `src/mythic_edge_parser/parsers/`
- `src/mythic_edge_parser/local_app/`
- `docs/contracts/`
- `docs/implementation_handoffs/`
- `docs/contract_test_reports/`
- `tests/`
- `frontend/`
- `tools/`
- package name `mythic-edge-parser`
- import root `mythic_edge_parser`
- package data layout in `pyproject.toml`
- fixture and snapshot locations

## Deferred To Item #3 Or Later

The following are out of scope for issue #218 and should be deferred to item #3
or a later scoped issue:

- moving Python modules;
- creating new subpackages by internal project area;
- changing imports;
- renaming packages;
- splitting repositories;
- moving tests into subdirectories;
- moving contracts, handoffs, or reports into subdirectories;
- creating directory README indexes;
- adding source comments, decorators, constants, or metadata for ownership;
- adding pytest ownership markers;
- adding compatibility shims;
- changing package-data layout;
- adding a boundary checker;
- adding import graph tooling as a required gate;
- changing `.github` issue templates or PR templates;
- changing ADR-0006 status or materially amending ADR-0006;
- changing `README.md` or project roadmap links;
- changing any runtime, parser, analytics, local app, workbook, transport,
  Apps Script, Sheets, AI, or production behavior.

## Unknowns

- The local branch is named for issue #218 but currently tracks
  `origin/codex/analytics-foundation`; submitter/deployer roles should verify
  intended PR target and remote branch setup before publishing.
- Whether a future `docs/architecture/` directory should exist remains
  unresolved and is deferred.
- Whether README links should point to the ownership map is deferred.
- Whether source-level comments are useful for selected bridge modules is
  deferred.
- Whether `.github/ISSUE_TEMPLATE/module_workflow.yml` should include boundary
  map prompts is deferred.
- Whether `tools/google_apps_script/Code.gs` should be labeled purely
  Workbook / Transport or bridge code should be documented in the map based on
  current evidence, with uncertainty allowed.
- Whether `runtime_surfaces.py` and `status_api.py` are Local App / UI bridge
  code, parser runtime support, or shared support should be documented in the
  map with uncertainty allowed.
- Whether future local app contracts should keep the `analytics_*` prefix or
  shift toward `local_app_*` remains deferred.

## Suspected Gaps

- No central `docs/internal_project_map.md` exists yet.
- Current flat docs directories are discoverable by filename prefix, but there
  is no single place that explains those prefixes.
- Existing issue #215 comparison and review artifacts still mention ADR-0006
  as proposed because they predate ADR acceptance.
- Bridge-code modules are currently understood from contracts, imports, and
  naming rather than one central map.
- The repo has no import graph report or boundary checker, which is correct for
  this issue but may become useful later.

## Protected Surfaces And Forbidden Side Effects

Do not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- parser event kind values;
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
- CI gates;
- Pyright gate behavior;
- production behavior;
- AI/model-provider behavior;
- package name;
- imports;
- file layout.

Do not create, commit, expose, print, or modify:

- secrets;
- credentials;
- API keys;
- tokens;
- webhook URLs;
- environment variables;
- raw local logs;
- generated data;
- runtime status artifacts;
- transport failure payload artifacts;
- workbook exports;
- local JSONL artifacts;
- generated SQLite files;
- local-only artifacts.

## Validation Requirements

Codex B validation for this contract:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/internal_project_boundary_annotation_organization.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/internal_project_boundary_annotation_organization.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

`origin/codex/analytics-foundation` is used as the validation base because the
local issue #218 branch currently tracks that remote branch and no
`origin/codex/internal-project-boundary-annotation` branch was observed during
this Codex B pass.

Future Codex C validation:

```powershell
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
```

Codex C must confirm that `git diff --name-only` contains no files outside the
contract, map, and implementation handoff unless the user explicitly authorizes
a follow-up scope change.

Runtime tests are not required for issue #218 if the diff is documentation-only
and stays inside the allowed files. If source, tests, tooling, `.github`,
package metadata, fixtures, snapshots, generated data, or local-only artifacts
change, stop and route back to Codex B or the user.

## Acceptance Criteria

The issue #218 implementation satisfies this contract when:

- `docs/internal_project_map.md` exists and follows the required structure;
- the map cites issue #218, issue #215, and accepted ADR-0006;
- the map documents the required internal project vocabulary;
- the map documents current flat-layout policy;
- the map covers required path families;
- the map classifies bridge-code candidates or marks ambiguous candidates
  explicitly;
- the map keeps docs grouping/index guidance inside the map only;
- the map keeps tests and source layout flat;
- the map does not authorize README, source, test, tooling, `.github`, package,
  fixture, snapshot, runtime, generated, or local-only edits;
- validation passes or any failure is explained as unrelated or blocking;
- no protected surfaces are touched;
- no secrets, raw logs, generated data, runtime artifacts, workbook exports,
  local JSONL artifacts, generated SQLite files, or local-only artifacts are
  introduced.

## Stop Conditions

Stop and route back to Codex B or the user if:

- implementation would require changing files outside the allowed file list;
- the map would require source comments or source metadata;
- a classification would imply a file move, package rename, import change,
  repository split, or CI gate;
- ADR-0006 status or README/index updates appear necessary;
- a protected surface would be touched;
- a raw/private/local/generated artifact would be introduced;
- branch target or PR base is unclear during submitter/deployer work.

## Expected Codex C Handoff

Codex C should produce:

- `docs/internal_project_map.md`
- `docs/implementation_handoffs/internal_project_boundary_annotation_organization_comparison.md`

Codex C should not produce source changes, tests, tooling, `.github` edits,
README/index edits, generated artifacts, or CI gates.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #218.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/218

Branch:
codex/internal-project-boundary-annotation

Contract:
docs/contracts/internal_project_boundary_annotation_organization.md

Goal:
Implement the docs-only internal project boundary annotation and organization pass authorized by the contract.

Before editing:
- Confirm the current branch and upstream target.
- Inspect git status and exclude unrelated changes.
- Read the contract, issue #218, issue #215 artifacts, ADR-0006, and current repo inventories.
- State what the map is supposed to do, what the repo currently does, what discoverability gap remains, and the exact minimal docs-only plan.

Do:
- Create docs/internal_project_map.md following the contract structure.
- Classify required path families using the accepted ADR-0006 vocabulary.
- Document bridge-code candidates and ambiguous entries without changing source files.
- Keep docs grouping/index, handoff/report grouping, test naming, and source ownership guidance documentation-only inside the map.
- Produce docs/implementation_handoffs/internal_project_boundary_annotation_organization_comparison.md.

Do not:
- Move files.
- Rename packages.
- Change imports.
- Split repositories.
- Add CI gates.
- Enforce import boundaries in code.
- Create directory README indexes.
- Edit README.md, ADRs, .github files, pyproject.toml, source files, frontend files, tools, tests, fixtures, snapshots, generated files, runtime artifacts, or local-only artifacts.
- Change parser/runtime/analytics/local app/workbook/webhook/Apps Script/Sheets/AI/production behavior.
- Touch secrets, raw logs, generated data, runtime status artifacts, transport failure payload artifacts, workbook exports, local JSONL artifacts, generated SQLite files, or local-only artifacts.
- Target main, stage, commit, push, open a PR, merge, or close issue #218 unless explicitly asked.

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

Final handoff must include:
- role performed
- issue reviewed
- contract used
- artifacts produced
- central ownership map path
- bridge-code rules applied
- ambiguous entries
- allowed files changed
- forbidden scope status
- validation results
- remaining risks
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/218"
  tracker: "N/A"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue problem representation for internal project boundary annotation and organization"
  target_artifact: "docs/internal_project_map.md"
  contract_artifact: "docs/contracts/internal_project_boundary_annotation_organization.md"
  risk_tier: "Medium"
  branch: "codex/internal-project-boundary-annotation"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped protected-surface scan for contract"
    - "path-scoped secret/private-marker scan for contract"
  stop_conditions:
    - "Do not move files, rename packages, change imports, split repositories, add CI gates, or enforce import boundaries."
    - "Do not create directory README indexes, source comments, test markers, boundary checkers, or import graph gates in issue #218."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/Apps Script/Sheets/AI/production behavior."
    - "Do not touch secrets, raw logs, generated data, runtime artifacts, workbook exports, local JSONL artifacts, generated SQLite files, or local-only artifacts."
```
