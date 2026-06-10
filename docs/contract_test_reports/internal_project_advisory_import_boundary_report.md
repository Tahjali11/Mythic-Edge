# Internal Project Advisory Import-Boundary Report

## 1. Executive Summary

Issue: `#334` (`[architecture] Advisory import-boundary report before physical reorganization`)

Contract: `docs/contracts/internal_project_advisory_import_boundary_report.md`

Verdict: advisory report produced; no source moves, package renames, import rewrites, checker, or CI gate were added.

Findings, ordered by movement risk:

| finding_id | severity | classification | finding | recommendation |
| --- | --- | --- | --- | --- |
| CT-334-001 | P1 | `move_blocker`, `package_data_coupling` | SQL migration packages are coupled to current Python package names through `pyproject.toml` package data and `importlib.resources` loaders. Moving analytics or Match Journal migration packages without a package-data/resource-loading contract could break runtime migration discovery. | Write a focused package-data/resource-loading migration contract before physical movement. |
| CT-334-002 | P1 | `move_blocker`, `bridge_expected_needs_documentation` | Local App live-capture code imports parser stream/state modules directly. That is expected in the current flat package, but it is a protected parser/runtime bridge and should not be moved casually. | Create a Local App live-capture facade or boundary contract before moving parser, stream, state, or live-capture modules. |
| CT-334-003 | P2 | `ambiguous_needs_follow_up` | `src/mythic_edge_parser/app/` currently contains parser, analytics, evidence/provenance, workbook/transport, Match Journal, and shared-support modules. The physical package layout is broader than the logical project-area map. | Do not split `app/` wholesale. Move one coherent cluster at a time under scoped contracts. |
| CT-334-004 | P2 | `bridge_expected_needs_documentation` | Match Journal service/migration modules live under `app/` while Local App modules consume them. This appears expected today, but ownership needs to be documented before any package split. | Create a Match Journal ownership/import-boundary follow-up before movement. |
| CT-334-005 | P2 | `bridge_expected_needs_documentation` | Analytics legacy JSONL adapter/import jobs bridge local artifacts and analytics ingest. This is expected for local workflows, but should be reviewed before moving analytics/local-app packages. | Write a focused analytics import-job bridge contract before movement. |

No suspected forbidden production direction was found by this import-level scan. In particular, the scan did not find parser production code importing analytics, Local App/UI, frontend, AI, workbook transport, or production release tooling to produce parser truth. This is import-graph evidence only, not a semantic proof of all runtime behavior.

## 2. Branch, Base, And Git Status At Inspection Time

Worktree: `<worktree>`

Branch inspected: `codex/advisory-import-boundary-report`

Base branch: `origin/codex/analytics-foundation`

Branch sync at inspection: `0 0`

Initial status at inspection:

```text
## codex/advisory-import-boundary-report...origin/codex/analytics-foundation
?? docs/contracts/internal_project_advisory_import_boundary_report.md
```

No source, test, tool, frontend, package metadata, parser, analytics, runtime, workbook, webhook, Apps Script, Sheets, OpenAI, AI/coaching, Line Tracer, or production files were edited by this report pass.

## 3. Source Artifacts Inspected

- GitHub issue `#334`
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/templates/contract_test_report.md`
- `docs/internal_project_map.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
- `docs/contracts/internal_project_boundaries.md`
- `docs/contracts/internal_project_boundary_annotation_organization.md`
- `docs/contracts/internal_project_boundary_workflow_vocabulary.md`
- `docs/contracts/internal_project_advisory_import_boundary_report.md`
- `pyproject.toml`
- `src/mythic_edge_parser/`
- `tests/`
- `tools/`
- `frontend/`

## 4. Analysis Method And Exact Commands Used

Read-only commands used:

```powershell
git status --short --branch --untracked-files=all
git rev-list --left-right --count HEAD...origin/codex/analytics-foundation
git diff --name-status
gh issue view 334 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body
rg -n "^(from|import) mythic_edge_parser|from mythic_edge_parser|import mythic_edge_parser" src tests tools -g "*.py" --stats
rg -n "mythic_edge_parser|from \\.|import .*" frontend -g "*.ts" -g "*.tsx" -g "*.js" -g "*.jsx" --stats
rg --files src\mythic_edge_parser
rg --files frontend\src
rg -n "importlib\.resources|files\(|read_text\(|analytics_migrations|package_data|resources" src tools tests pyproject.toml -g "*.py" -g "pyproject.toml"
```

Additional read-only local analysis:

- A temporary, uncommitted Python AST scan parsed repo-owned `.py` files under `src/`, `tests/`, and `tools/`.
- The scan expanded `from mythic_edge_parser.app import x` style imports into symbol-level import edges when possible.
- Counts below are approximate symbol-level edges, not unique module-pair counts.
- The analysis did not read private/generated artifacts or raw Player.log content.

## 5. Current Package/Layout Summary

Current layout remains a single Python package root:

- `src/mythic_edge_parser/app/`: broad current application package containing parser/state, analytics, migrations, evidence/provenance, workbook/transport helpers, Match Journal, config, diagnostics, runtime surfaces, and shared support.
- `src/mythic_edge_parser/local_app/`: local app backend, setup/status, import jobs, live-capture control, dashboard/cockpit helpers, error reports, and Match Journal local app surfaces.
- `src/mythic_edge_parser/parsers/`, `router.py`, `stream.py`, `tailer.py`, and related modules: parser/runtime-adjacent stream and parsing surfaces.
- `frontend/src/`: frontend-local TypeScript/React app using frontend-local imports and local app API contracts.
- `tests/`: broad quality/governance validation surface with expected cross-area imports.
- `tools/`: developer, setup, governance, and reporting tools with expected cross-area inspection imports.
- `docs/`: governance, contracts, handoffs, decisions, and contract-test reports.

This flat layout is compatible with ADR-0006 and ADR-0007. The report does not recommend a broad package split.

## 6. Import Inventory Summary

Raw Python project-import search:

- Scope: `src`, `tests`, `tools`
- Files searched: `231`
- Files with matching project imports: `117`
- Matched lines: `243`

Temporary AST scan:

- Files scanned: `231`
- Files with project imports: `116`
- Approximate symbol-level project import edges: `530`
- Production source edges: `53`
- Test edges: `467`
- Tool edges: `10`

Approximate AST edge counts by source and target area:

| source context / source area | target area | approximate edges |
| --- | --- | ---: |
| tests / Quality-Governance | Parser | 236 |
| tests / Quality-Governance | Local App / UI | 76 |
| tests / Quality-Governance | Analytics | 66 |
| tests / Quality-Governance | Shared Support | 54 |
| tests / Quality-Governance | Corpus / Provenance | 26 |
| tests / Quality-Governance | Workbook / Transport | 9 |
| production / Local App / UI | Local App / UI | 20 |
| production / Local App / UI | Analytics | 14 |
| production / Local App / UI | Parser | 7 |
| production / Local App / UI | Shared Support | 1 |
| production / Corpus / Provenance | Corpus / Provenance | 7 |
| production / Analytics | Analytics | 4 |
| tools / Quality-Governance | Corpus / Provenance | 4 |
| tools / Local App / UI | Analytics | 3 |
| tools / Local App / UI | Local App / UI | 2 |
| tools / Shared Support | Shared Support | 1 |

Frontend import search:

- Scope: `frontend`
- Files searched: `11`
- Files with frontend import text: `9`
- No frontend imports of `mythic_edge_parser` Python internals were observed.

## 7. Internal Project Area Mapping Table

| internal project area | representative repo paths | notes |
| --- | --- | --- |
| Parser | `src/mythic_edge_parser/app/state.py`, `src/mythic_edge_parser/app/models.py`, `src/mythic_edge_parser/app/extractors.py`, `src/mythic_edge_parser/app/event_identity.py`, `src/mythic_edge_parser/stream.py`, `src/mythic_edge_parser/router.py`, `src/mythic_edge_parser/parsers/` | Owns parser truth, event interpretation, match/game identity, and final reconciliation. |
| Corpus / Provenance | `src/mythic_edge_parser/app/evidence_*`, `src/mythic_edge_parser/app/runtime_field_evidence.py`, `tools/dev_app/evidence_*` | Supports QA/provenance; must not become a second parser. |
| Analytics | `src/mythic_edge_parser/app/analytics_*`, analytics migrations, local analytics ingest helpers | Consumes parser-normalized facts and approved local analytics inputs. |
| Local App / UI | `src/mythic_edge_parser/local_app/`, `frontend/src/`, `tools/dev_app/private_local_v1_setup.py`, `tools/dev_app/dev_app_launcher.py` | Orchestrates local app, setup, diagnostics, import jobs, and UI. |
| Workbook / Transport | `src/mythic_edge_parser/app/outputs.py`, `src/mythic_edge_parser/app/sheet_schema.py`, `tools/google_apps_script/Code.gs` | Consumes parser row contracts and transports output. |
| Quality / Governance | `tests/`, `docs/`, validation tools, contract reports | May inspect all areas but does not authorize runtime coupling. |
| Shared Support | `src/mythic_edge_parser/app/config.py`, path/config helpers, neutral diagnostics/runtime helpers | Needs follow-up when shared support becomes too broad or truth-bearing. |
| Generated / Local Artifacts | app-data roots, runtime logs, SQLite DB files, generated reports, private logs | Out of scope for import architecture and not inspected here. |
| Future AI Integration | no approved production AI runtime area in this scan | Remains deferred unless a scoped contract authorizes it. |

## 8. Production Source Import-Edge Findings

### Parser production code

Classification: `same_area_allowed`

Risk: low for this advisory pass.

The import-level scan did not find production parser code importing analytics, Local App/UI, frontend, AI, workbook transport, or production release tooling to produce parser truth.

Move impact: parser moves still require scoped contracts because parser truth and runtime state are protected surfaces, but no immediate forbidden import direction was observed by this scan.

### Local App / UI to Analytics

Classification: `bridge_expected_documented`

Risk: medium.

Examples:

- `src/mythic_edge_parser/local_app/import_jobs.py` imports analytics ingest and legacy JSONL adapter modules.
- `src/mythic_edge_parser/local_app/live_capture_control.py` imports analytics ingest and analytics migration loader modules.
- `src/mythic_edge_parser/local_app/setup_status.py` imports the analytics migration loader.

Move impact: expected local app bridge code. Before moving analytics or local app packages, create stable bridge/facade contracts so local app orchestration can continue without hidden ownership drift.

### Local App / UI to Parser

Classification: `bridge_expected_needs_documentation`

Risk: high for physical movement, medium for current flat layout.

Examples:

- `src/mythic_edge_parser/local_app/live_capture_control.py` imports parser state and stream modules.

Move impact: this is the most sensitive production bridge. It touches parser/runtime surfaces and should block physical movement until a focused live-capture/parser-boundary contract defines what is allowed.

### Local App / UI to Shared Support

Classification: `shared_support_allowed`

Risk: low to medium.

Example:

- `src/mythic_edge_parser/local_app/setup_status.py` imports app config.

Move impact: low-risk while shared support stays neutral. Reclassify if shared support becomes truth-bearing or starts importing downstream layers.

### Corpus / Provenance same-area imports

Classification: `same_area_allowed`

Risk: low.

Evidence/provenance modules import neighboring evidence-ledger, schema snapshot, drift report, and runtime-field evidence modules.

Move impact: these modules can be considered a coherent cluster candidate only after a scoped provenance/corpus contract.

### Analytics same-area imports

Classification: `same_area_allowed`

Risk: low to medium.

Example:

- `src/mythic_edge_parser/app/analytics_json_ingest.py` imports analytics ingest helpers.

Move impact: same-area analytics imports are expected. Movement risk increases because analytics migrations are package-data coupled.

### Match Journal Local App bridge

Classification: `ambiguous_needs_follow_up`

Risk: medium.

Local App modules import Match Journal runtime/service/repository/migration helpers that currently live under the broad `app/` package.

Move impact: likely expected, but ownership is not cleanly represented by the physical layout. A Match Journal ownership/facade contract should precede movement.

## 9. Tests/Tools Import-Edge Findings

Classification: `quality_governance_inspection_allowed`, `test_tool_only`

Risk: low for current runtime, medium for future movement cost.

The largest cross-area import volume is in tests. This is expected: tests validate parser, analytics, Local App/UI, workbook/transport, shared support, and evidence/provenance behavior.

Observed test import targets:

- Parser: broad parser truth and runtime coverage.
- Local App / UI: local app backend, setup, dashboard, live capture, and frontend-adjacent API behavior.
- Analytics: ingest, migrations, refresh state, dashboards, import jobs.
- Shared Support: config and neutral support helpers.
- Corpus / Provenance: evidence/provenance checks.
- Workbook / Transport: sheet/schema/output parity checks.

Tool imports are also expected in current scope:

- Governance/evidence tools inspect provenance modules.
- Local dev app setup/launcher tools import approved local app and analytics setup surfaces.
- Shared support/card-data tools remain tool-only and should not be treated as production runtime coupling.

Move impact: tests/tools are not production architecture violations, but future package moves should include a test/tool migration plan.

## 10. Frontend Import-Edge Findings

Classification: `frontend_local_only`

Risk: low.

The frontend scan observed frontend-local imports and third-party imports. No frontend import of `mythic_edge_parser` Python internals was observed.

Move impact: frontend remains bounded by local app API surfaces in this import-level scan. Future movement should preserve API contracts rather than teaching frontend about Python internals.

## 11. Package-Data And Resource-Loading Coupling Observations

Classification: `package_data_coupling`, `move_blocker`

Risk: high for package movement.

Observed package metadata:

- `pyproject.toml` includes package data for `mythic_edge_parser.app.analytics_migrations`.
- `pyproject.toml` includes package data for `mythic_edge_parser.app.match_journal_migrations`.

Observed resource loading:

- `src/mythic_edge_parser/app/analytics_migration_loader.py` loads analytics SQL migrations through package resources.
- `src/mythic_edge_parser/app/match_journal_migration_loader.py` loads Match Journal SQL migrations through package resources.

Move impact: moving migration directories or package names without a migration/package-data contract can break runtime resource discovery even if Python imports are updated. This is a blocker before physical reorganization.

## 12. Expected Bridge-Code Dependencies

Expected bridges in the current flat layout:

- `local_app/import_jobs.py` to analytics ingest and legacy JSONL adapter.
- `local_app/live_capture_control.py` to analytics ingest, analytics migrations, parser state, and parser stream.
- `local_app/setup_status.py` to analytics migration loader and app config.
- `local_app/match_journal_*` to Match Journal service/repository/runtime helpers.
- `tools/dev_app/*` to Local App/UI and analytics setup surfaces.
- `tests/*` to all areas under Quality/Governance inspection rules.

These bridges are not immediate defects. They are movement constraints.

## 13. Ambiguous Or Risky Dependencies

- Broad `app/` package ownership: `app/` contains multiple logical areas. Classification: `ambiguous_needs_follow_up`. Risk: high for broad moves.
- Live-capture direct parser bridge: Local App imports parser stream/state. Classification: `bridge_expected_needs_documentation`. Risk: high for physical moves.
- Match Journal physical location: Match Journal modules live under `app/` while Local App consumes them. Classification: `ambiguous_needs_follow_up`. Risk: medium.
- Analytics legacy JSONL/import-job bridge: local artifacts feed analytics ingest. Classification: `bridge_expected_needs_documentation`. Risk: medium.
- Shared support modules: config, runtime surfaces, diagnostics, and status helpers may be neutral today but can become truth-bearing if broadened. Classification: `shared_support_allowed` with follow-up review before moves.

## 14. Suspected Forbidden Directions

No suspected forbidden production import direction was found by this report.

Specifically, this advisory scan did not find parser production code importing:

- Analytics
- Local App / UI
- Frontend
- Workbook / Transport
- OpenAI/AI/coaching
- Production release tooling

Caveat: this is an import-boundary scan. It does not prove every runtime behavior or semantic truth-owner boundary.

## 15. Move Blockers Before Physical Reorganization

Before physical package movement, write follow-up contracts for:

1. SQL migration package data and resource-loading compatibility.
2. Local App live-capture imports of parser `state` and `stream`.
3. Broad `app/` mixed ownership and one-cluster-at-a-time movement order.
4. Match Journal service/repository/migration ownership and Local App facade needs.
5. Analytics import jobs and legacy JSONL adapter bridge boundaries.
6. Test/tool import migration plan, so quality/governance imports do not hide runtime coupling.

## 16. Recommended Follow-Up Issue List

Recommended follow-up issues:

1. Package-data/resource-loading contract for analytics and Match Journal migrations.
2. Local App live-capture facade/import-boundary contract for parser state/stream access.
3. Match Journal ownership and import-boundary contract before movement.
4. Analytics legacy JSONL adapter and import-job bridge review.
5. Shared support ownership audit for config, diagnostics, runtime surfaces, and status helpers.
6. Optional advisory import-boundary checker proposal after this report is accepted. Keep it advisory first; do not add a CI gate without a separate contract.
7. Test/tool migration plan for any future physical package split.

## 17. Explicit No-Gate/No-Enforcement Statement

This report is advisory and non-gating.

It does not:

- implement code
- move files
- rename packages
- rewrite imports
- split packages or repositories
- add an import checker
- add a CI gate
- create failing validation checks
- authorize source or runtime behavior changes

Any future implementation work must route through a separate issue and contract.

## 18. Protected-Surface And Privacy Assessment

Protected-surface status: no protected runtime/product surface was changed by this report pass.

Privacy status: no raw/private/generated artifacts were read, copied, printed, stored, or committed. The report uses repo-relative paths and symbolic `<worktree>` notation.

Forbidden scope not touched:

- parser behavior
- parser state final reconciliation
- parser event classes
- match/game identity
- deduplication
- parser payload shape
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

## 19. Validation Evidence

Read-only import scans completed:

```powershell
rg -n "^(from|import) mythic_edge_parser|from mythic_edge_parser|import mythic_edge_parser" src tests tools -g "*.py" --stats
rg -n "mythic_edge_parser|from \\.|import .*" frontend -g "*.ts" -g "*.tsx" -g "*.js" -g "*.jsx" --stats
```

Validation run after report creation:

```powershell
git diff --check -- docs\contract_test_reports\internal_project_advisory_import_boundary_report.md
py tools\check_agent_docs.py
@'
docs/contracts/internal_project_advisory_import_boundary_report.md
docs/contract_test_reports/internal_project_advisory_import_boundary_report.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/internal_project_advisory_import_boundary_report.md
docs/contract_test_reports/internal_project_advisory_import_boundary_report.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Results:

- `git diff --check` for the report artifact: passed.
- `py tools\check_agent_docs.py`: passed, `errors: 0`, `warnings: 0`.
- Path-scoped protected-surface scan: passed, `forbidden: 0`, `warnings: 0`.
- Path-scoped secret/private-marker scan: passed, `forbidden: 0`, `warnings: 0`.

## 20. Next Recommended Role

Recommended next role: Codex F if the user wants to publish this advisory report package.

Recommended architecture follow-up: Codex A or Codex B for the specific follow-up issue selected from the move blockers above.

Do not route directly to Codex C for physical moves until a scoped follow-up contract exists.

## 21. Workflow Handoff Block

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/334"
  completed_thread: "E"
  next_thread: "F"
  role_performed: "Codex E: Module Reviewer / Contract Tester / Architecture Audit Reporter"
  source_artifact: "GitHub issue problem representation"
  contract_artifact: "docs/contracts/internal_project_advisory_import_boundary_report.md"
  target_artifact: "docs/contract_test_reports/internal_project_advisory_import_boundary_report.md"
  branch: "codex/advisory-import-boundary-report"
  base_branch: "origin/codex/analytics-foundation"
  risk_tier: "Medium-High"
  verdict: "advisory_import_boundary_report_produced_no_gate_no_moves"
  import_boundary_summary:
    - "No suspected forbidden production parser dependency direction found by import-level scan."
    - "Local App live-capture parser state/stream bridge is expected today but blocks movement until documented."
    - "Analytics and Match Journal SQL migrations are package-data/resource-loading movement blockers."
    - "Frontend imports remain frontend-local; no Python internals observed."
  recommended_follow_up:
    - "Package-data/resource-loading contract before moving migration packages."
    - "Local App live-capture facade/import-boundary contract."
    - "Match Journal ownership/import-boundary contract."
    - "Analytics legacy JSONL/import-job bridge review."
    - "Optional advisory checker proposal in a later issue; no CI gate in this slice."
  stop_conditions:
    - "Do not implement code in the advisory report pass."
    - "Do not move files, rename packages, change imports, split packages, or add CI gates."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not read, copy, print, store, or commit raw/private/generated artifacts."
```
