# Mythic Edge Internal Project Map

## Scope

This map names the current internal project ownership boundaries inside the
Mythic Edge monorepo. It is a human and Codex routing aid for issue #218. It
does not move files, rename packages, change imports, split repositories, add
CI gates, enforce import boundaries, or change runtime behavior.

## Authority Note

This map is governed by:

- issue #218: https://github.com/Tahjali11/Mythic-Edge/issues/218
- issue #215: https://github.com/Tahjali11/Mythic-Edge/issues/215
- `docs/contracts/internal_project_boundary_annotation_organization.md`
- `docs/contracts/internal_project_boundaries.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`

ADR-0006 is accepted repository-boundary policy. This map helps apply that
policy to current repo paths, but it does not supersede `AGENTS.md`,
`docs/agent_rules.yml`, `docs/agent_constitution.md`, active issues, active
contracts, accepted ADRs, or reviewed PRs.

## How To Use This Map

Use this map before opening or reviewing a scoped issue when a path sits in a
broad directory such as `src/mythic_edge_parser/app/`, `tests/`, `tools/`, or a
flat governance artifact directory.

For each path, identify:

- the primary internal project area;
- whether the path is clear-owner, shared support, bridge code, ambiguous, or
  generated/excluded;
- the truth owner for facts flowing through the path;
- allowed consumers or readers;
- the boundary rule that prevents reverse-flow or downstream truth ownership.

If this map conflicts with a current contract, accepted ADR, or source code
behavior, treat the conflict as a follow-up issue. Do not "fix" it by moving
files or changing imports inside issue #218.

## Internal Project Vocabulary

| Project | Owns | Must Not Own |
| --- | --- | --- |
| Parser | MTGA log parsing, parser events, routing, parser state, match/game identity, deduplication, final reconciliation, parser-normalized facts. | Analytics truth, workbook truth, UI truth, AI truth, or downstream corrections. |
| Corpus / Provenance | Evidence, source, confidence, finality, drift, fixtures, replay evidence, golden replay, drift reports, validation support. | Parser truth or corrected parser facts. |
| Analytics | Local SQLite schema, migrations, deterministic views, ingest from parser-normalized facts, warnings, summaries. | Raw Player.log interpretation or parser-managed fact overrides. |
| Local App / UI | FastAPI backend, React/Vite frontend, setup/status display, import controls, local orchestration. | Parser truth, analytics truth, workbook truth, destructive actions without contract authority. |
| Workbook / Transport | Workbook row contracts, sheet schema, outputs, webhook payload shape, Apps Script parity, transport diagnostics. | Parser truth or formula-driven reconstruction of parser-owned facts. |
| Quality / Governance | Contracts, handoffs, reviews, ADRs, workflow docs, protected-surface checks, secret scans, validation selectors. | Runtime product behavior or implicit protected-surface authorization. |
| Future AI Integration | Deferred future summaries, explanations, hypotheses, and coaching text under separate contract. | Parser truth, analytics truth, workbook truth, hidden-card truth, model-provider truth, or strategic certainty. |
| Shared Support | Helpers used by more than one internal project without owning upstream truth. | A hidden downstream-to-upstream feedback path. |
| Generated / Local Artifacts | Ignored, local, generated, private, or non-authoritative artifacts. | Committed source truth or repo authority. |
| External / Collaboration Surface | GitHub, Google Workspace, connectors, plugins, browser helpers, and other access/collaboration surfaces. | Repo authority, parser truth, credential policy, merge readiness, or deployment authority by default. |

## Current Flat-Layout Policy

The repo intentionally stays physically flat for issue #218:

- `src/mythic_edge_parser/` remains one package root.
- `src/mythic_edge_parser/app/` remains broad.
- `src/mythic_edge_parser/parsers/` remains parser-owned.
- `src/mythic_edge_parser/local_app/` remains local-app owned.
- `docs/contracts/`, `docs/implementation_handoffs/`, and
  `docs/contract_test_reports/` remain flat and prefix-based.
- `tests/` remains flat and filename-based.
- `frontend/` remains the local app UI surface.
- `tools/` remains mixed tooling classified by purpose.
- The package name remains `mythic-edge-parser`.
- The import root remains `mythic_edge_parser`.
- Package data layout in `pyproject.toml` remains unchanged.
- Fixture and snapshot locations remain unchanged.

Flat layout means ownership is documented here and in contracts, not enforced by
directory structure.

## Ownership Table

| path_or_family | primary_project | classification | truth_owner | allowed_consumers_or_readers | notes_or_boundary |
| --- | --- | --- | --- | --- | --- |
| `AGENTS.md` | Quality / Governance | clear_owner | Repo authority | All workflow roles | Entry point for repo-local instructions. |
| `README.md` | Quality / Governance | shared_support | Repo docs authority | Users, contributors, Codex roles | Project overview, not runtime truth. |
| `docs/agent_rules.yml` | Quality / Governance | clear_owner | Governance rule index | Codex roles and checks | Machine-readable governance surface. |
| `docs/agent_constitution.md` | Quality / Governance | clear_owner | Governance constitution | Codex roles | Human-readable role and authority rules. |
| `docs/codex_module_workflow.md` | Quality / Governance | clear_owner | Workflow policy | Codex roles | Defines A-G routing and artifact flow. |
| `docs/agent_threads/` | Quality / Governance | clear_owner | Role procedure docs | Codex roles | Role-specific process, not product behavior. |
| `docs/templates/` | Quality / Governance | clear_owner | Artifact shape guidance | Codex roles | Template guidance, not authority above current issue/contract. |
| `docs/decisions/` | Quality / Governance | clear_owner | Accepted ADR precedent | Issues, contracts, reviews, PRs | ADRs record durable policy below active repo authority. |
| `docs/contracts/` | Quality / Governance | clear_owner | Contract artifacts | Codex B/C/E/F/G | Flat directory; use prefixes for owner signals. |
| `docs/implementation_handoffs/` | Quality / Governance | clear_owner | Handoff artifacts | Codex C/D/E/F/G | Flat directory; should mirror source contract prefix. |
| `docs/contract_test_reports/` | Quality / Governance | clear_owner | Review artifacts | Codex E/F/G | Flat directory; should mirror source contract prefix. |
| `docs/problem_representations/` | Quality / Governance | clear_owner | Problem framing | Codex A/B/C/E | Source framing, not implementation authority without contract. |
| `docs/project_roadmap.md` | Quality / Governance | clear_owner | Roadmap routing | Codex roles and user | Roadmap guidance yields to active issues/contracts. |
| `src/mythic_edge_parser/events.py` | Parser | clear_owner | Parser event model | Parser, tests, tooling | Parser event surface; downstream consumers must not mutate truth. |
| `src/mythic_edge_parser/router.py` | Parser | clear_owner | Parser routing | Parser, tests | Routes parsed log entries; not analytics or UI truth. |
| `src/mythic_edge_parser/stream.py` | Parser | clear_owner | Parser stream handling | Parser, tests | Stream lifecycle support. |
| `src/mythic_edge_parser/event_bus.py` | Parser | clear_owner | Parser event dispatch | Parser, tests | Parser event bus support. |
| `src/mythic_edge_parser/log/` | Parser | clear_owner | Log entry and tailing support | Parser, tests | Handles log input shape, not analytics truth. |
| `src/mythic_edge_parser/parsers/` | Parser | clear_owner | Parser modules | Parser, tests | Event-family parsers. |
| `src/mythic_edge_parser/parsers/gre/` | Parser | clear_owner | GRE parser modules | Parser, tests | GRE parsing, game state, and related parser facts. |
| `src/mythic_edge_parser/app/state.py` | Parser | clear_owner | Parser state truth | Parser, tests, outputs | Owns live/final reconciliation and parser-managed facts. |
| `src/mythic_edge_parser/app/models.py` | Parser | clear_owner | Parser-normalized rows | Parser, workbook/transport, analytics | Owns match/game model serialization. |
| `src/mythic_edge_parser/app/extractors.py` | Parser | clear_owner | Parser extraction logic | Parser, tests | Parser truth extraction from state/events. |
| `src/mythic_edge_parser/app/event_identity.py` | Parser | clear_owner | Parser identity helpers | Parser, tests | Identity/dedup support. |
| `src/mythic_edge_parser/app/gameplay_actions.py` | Parser | clear_owner | Parser-normalized gameplay actions | Parser, analytics, tests | Analytics may ingest outputs but must not reinterpret raw logs. |
| `src/mythic_edge_parser/app/opponent_card_observations.py` | Parser | clear_owner | Parser-normalized opponent-card observations | Parser, analytics, tests | Downstream analytics consumes parser-normalized entries. |
| `src/mythic_edge_parser/app/hand_confirmations.py` | Parser | clear_owner | Parser hand confirmation support | Parser, tests | Parser-managed evidence surface. |
| `src/mythic_edge_parser/app/transforms.py` | Parser | clear_owner | Parser transform support | Parser, tests | Parser-owned normalization support. |
| `src/mythic_edge_parser/app/runner.py` | Parser | clear_owner | Parser runtime entry support | Parser, local app status readers | Runtime orchestration must not be changed by this map. |
| `src/mythic_edge_parser/app/parser_diagnostics.py` | Parser | clear_owner | Parser diagnostics | Parser, Quality / Governance | Diagnostics describe parser behavior. |
| Parser diagnostics and runtime parser support under `src/mythic_edge_parser/app/` | Parser | shared_support | Parser | Parser, local status, tests | Classify by nearest parser truth owner unless a contract says otherwise. |
| Evidence-ledger, replay, drift, golden fixture, and corpus support under `src/mythic_edge_parser/app/` | Corpus / Provenance | clear_owner | Corpus / Provenance | Parser QA, analytics, Quality / Governance | Supports reliability and provenance, not parser truth. |
| Analytics storage, migration, ingest, views, and sidecar support under `src/mythic_edge_parser/app/` | Analytics | clear_owner | Analytics | Local App / UI, tests | Reads parser-normalized facts and approved provenance. |
| Workbook/output/schema/export support under `src/mythic_edge_parser/app/` | Workbook / Transport | clear_owner | Parser row contracts and transport shape | Parser, Apps Script, tests | Transports parser facts; does not own parser truth. |
| Card catalog and `grp_id` support under `src/mythic_edge_parser/app/` | Shared Support | shared_support | Parser for parser-managed card identity; contracts for other uses | Parser, Corpus / Provenance, Analytics | Shared helpers must not create analytics-to-parser feedback. |
| `src/mythic_edge_parser/local_app/` | Local App / UI | clear_owner | Local App / UI orchestration | Browser UI, analytics services, setup/status | Access and orchestration surface, not parser or analytics truth. |
| `frontend/` | Local App / UI | clear_owner | Frontend display/control surface | Local users and backend API | Browser UI must use backend API shapes, not Python internals. |
| `tools/` | Quality / Governance | shared_support | Depends on tool purpose | Codex roles, developers | Mixed wrappers; classify individual tools by purpose. |
| `tools/google_apps_script/Code.gs` | Workbook / Transport | bridge_code | Workbook / Transport | Workbook, Apps Script, parser row contracts | Transport parity surface; not parser truth. |
| `tests/` | Quality / Governance | shared_support | Test evidence | Codex roles and CI | Tests may cross boundaries to validate contracts. |
| `tests/fixtures/` | Corpus / Provenance | shared_support | Fixture provenance | Parser QA, drift tests, snapshots | Fixtures are evidence/support, not complete game truth. |
| `.github/ISSUE_TEMPLATE/module_workflow.yml` | Quality / Governance | external_or_generated_excluded | Workflow issue template | GitHub issue creation | GitHub collaboration surface; no edit in issue #218. |
| `.github/pull_request_template.md` | Quality / Governance | external_or_generated_excluded | PR template | PR authors and reviewers | GitHub collaboration surface; no edit in issue #218. |
| `pyproject.toml` | Quality / Governance | shared_support | Packaging metadata | Build/test tooling | Package data currently keeps analytics migrations under existing package root. |
| `data/` | Generated / Local Artifacts | external_or_generated_excluded | Local runtime/data only | Local runtime only | Do not commit raw/generated/private data from this family. |
| SQLite database outputs | Generated / Local Artifacts | external_or_generated_excluded | Local analytics runtime | Local app/runtime only | Generated DB files are not source artifacts. |
| JSONL artifacts | Generated / Local Artifacts | external_or_generated_excluded | Local import evidence only | Local adapter/import flow | Do not commit private JSONL artifacts. |
| Raw logs | Generated / Local Artifacts | external_or_generated_excluded | MTGA observable evidence | Local parser/runtime only | Raw logs are local/private unless explicitly sanitized and authorized. |
| Runtime status artifacts | Generated / Local Artifacts | external_or_generated_excluded | Runtime diagnostics | Local runtime only | Do not commit local runtime status files. |
| Workbook exports | Generated / Local Artifacts | external_or_generated_excluded | Exported downstream data | Local review only | Do not commit raw workbook exports. |
| Local-only artifacts | Generated / Local Artifacts | external_or_generated_excluded | Local machine state | Local user only | Local-only machine artifacts remain excluded. |

## Bridge-Code Table

| bridge_entry | bridge_from | bridge_to | primary_truth_owner | input_boundary | output_boundary | forbidden_interpretation | status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py` | Local legacy JSONL artifact shape | Analytics parser-normalized replay ingest | Parser for parser facts; Analytics for ingest compatibility | Synthetic or operator-selected legacy artifacts | Parser-normalized replay input | Legacy derived fields are not parser truth and raw saved-event lines must not be stored. | stable_bridge | Compatibility adapter from local artifact evidence to analytics-safe input. |
| `src/mythic_edge_parser/app/analytics_ingest.py` | Parser-normalized rows and approved provenance | SQLite analytics tables | Parser for facts; Analytics for storage | Match/game/action/observation/evidence rows | Local analytics records | Analytics must not reinterpret raw Player.log or override parser-managed values. | stable_bridge | Core analytics ingest bridge. |
| `src/mythic_edge_parser/app/card_catalog.py` | Shared card identity data | Parser, Corpus / Provenance, Analytics | Parser when used for parser-managed identity | Catalog lookups | Card identity support | Catalog helpers must not override parser facts from downstream analytics. | provisional_bridge | Shared support across several layers. |
| `src/mythic_edge_parser/app/card_catalog_refresh.py` | External card data refresh inputs | Shared card catalog | Shared Support | Approved card data source | Local catalog artifacts | Refresh tooling must not create parser truth without parser contract. | provisional_bridge | Shared support; validate generated data policy before changes. |
| `src/mythic_edge_parser/app/arena_id_validation.py` | Card/group identifiers | Parser and analytics validation | Parser for parser-managed identity | `grp_id` and related identifiers | Validation results | Validation findings are not downstream truth overrides. | provisional_bridge | Shared validation support. |
| `src/mythic_edge_parser/app/grp_id_catalog.py` | Card/group catalog data | Parser, Corpus / Provenance, Analytics | Parser when used for parser-managed card identity | Catalog data | Lookup support | Do not use analytics labels to rewrite parser identity. | provisional_bridge | Shared support. |
| `src/mythic_edge_parser/app/grp_id_candidates.py` | Candidate card identifiers | Parser, Corpus / Provenance, Analytics | Parser when used for parser-managed identity | Candidate identifiers | Candidate support | Candidate lists are support data, not confirmed parser truth. | provisional_bridge | Shared support. |
| `src/mythic_edge_parser/app/runtime_surfaces.py` | Parser/runtime status | Quality / Governance and Local App / UI status | Parser/runtime owns status source | Runtime status structures | Status display or reports | Status display must not change runtime behavior. | ambiguous_pending_follow_up | Could be parser runtime support or local-app bridge depending on future contract. |
| `src/mythic_edge_parser/app/status_api.py` | Parser/runtime diagnostics | Local App / UI or status consumers | Parser/runtime owns source facts | Runtime/config/status data | API/status output | Status API must not become parser truth or deployment authority. | ambiguous_pending_follow_up | Keep uncertainty visible until a future status/API contract classifies it. |
| `src/mythic_edge_parser/app/config.py` | Configuration values | Parser runtime and Local App / UI setup/status | Owning contract for each config surface | Repo/local config | Runtime or status configuration | Config display must not change environment or credential policy. | ambiguous_pending_follow_up | Support module; owner depends on scoped config contract. |
| `src/mythic_edge_parser/app/diagnostics.py` | Parser/runtime diagnostic signals | Parser, Local App / UI, Quality / Governance | Parser/runtime owns diagnostic source | Diagnostic inputs | Diagnostic display/report | Diagnostics do not authorize behavior changes. | ambiguous_pending_follow_up | Shared diagnostics support. |
| `src/mythic_edge_parser/local_app/import_jobs.py` | Local App / UI upload/import controls | Analytics import services | Parser and analytics own facts; Local App owns orchestration | User-selected files or upload temp files | Sanitized job status and analytics ingest calls | UI/job state must not expose raw payloads or rewrite facts. | stable_bridge | Local orchestration bridge. |
| `src/mythic_edge_parser/local_app/setup_status.py` | Parser/config/analytics setup signals | Local App / UI setup display | Source layer owns each signal | Repo/package/config status | Setup status response | Setup display is not runtime behavior authority. | stable_bridge | Local display bridge. |
| `tools/dev_app/` | Developer shell/launcher | Local App / UI backend/frontend startup | Local App / UI | Local dev environment | Developer convenience commands | Launcher must not add destructive actions or production behavior. | stable_bridge | Developer convenience only. |
| `tools/google_apps_script/Code.gs` | Parser-normalized row contracts | Google Sheets / Apps Script transport | Workbook / Transport | Webhook rows and sheet mappings | Workbook upsert behavior | Apps Script must not reinterpret parser truth. | stable_bridge | Workbook/transport bridge, not parser truth. |
| Validation and hardening tools under `tools/` | Repo files and reports | Quality / Governance validation evidence | Quality / Governance | Git diff, docs, code, tests, artifacts | Advisory or configured validation output | Tools must not silently become runtime behavior or failing gates without contract. | stable_bridge | Includes protected-surface, secret, agent-doc, selector, and advisory-report tools. |

## Ambiguous-Module Policy

Use `ambiguous_pending_follow_up` when:

- one file supports multiple internal project areas;
- current contracts disagree or are stale;
- a path has both runtime and validation uses;
- a path transports data between layers without clearly owning truth;
- classification would imply a future file move, package split, import rule, or
  CI gate.

Ambiguous entries should name the current best project, known consumers, why the
classification is uncertain, and what kind of future issue should resolve it.
Ambiguity never authorizes source comments, import changes, file moves, package
renames, runtime behavior changes, or CI enforcement.

Known ambiguous or provisional areas:

- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- shared card catalog and `grp_id` support
- future local app contract prefixes currently using `analytics_*`
- `.github/` collaboration templates that may later need boundary vocabulary
  updates

## Docs Artifact Grouping Guidance

The docs artifact directories stay flat for now. Use filenames and prefixes as
the grouping signal:

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

Future prefixes such as `workbook_transport_*`, `local_app_*`, and `ai_*` are
allowed as future guidance only. Do not create directory README indexes or move
existing artifacts in issue #218.

The implementation handoff for this issue is:

```text
docs/implementation_handoffs/internal_project_boundary_annotation_organization_comparison.md
```

The expected future contract-test report for this issue is:

```text
docs/contract_test_reports/internal_project_boundary_annotation_organization.md
```

Handoffs and reports should use the same module prefix as their source
contract.

## Test Naming Guidance

Tests stay flat under `tests/` for issue #218. Do not rename tests or add test
markers in this issue.

Suggested filename signals:

- Parser: `test_parser_*`, `test_*_parser.py`, `test_router_*`,
  `test_state.py`, `test_app_models.py`
- Corpus / Provenance: `test_evidence_*`, `test_golden_*`,
  `test_log_drift_*`, `test_feature_equity_*`
- Analytics: `test_analytics_*`
- Local App / UI: `test_analytics_local_app_*`,
  `test_analytics_*_ui_*`, and frontend tests under `frontend/src/*.test.ts*`
- Workbook / Transport: `test_sheet_*`, `test_webhook_*`,
  `test_workbook_*`, `test_app_outputs.py`
- Quality / Governance: `test_check_*`, `test_select_validation.py`,
  `test_hardening_*`, `test_pyright_*`, `test_*agent_docs*`

Cross-boundary test imports are allowed when they validate a contract. They do
not imply production dependency direction.

## Source Ownership Guidance

While `src/` stays flat:

- Parser-core files remain Parser-owned.
- Evidence-ledger and drift-provenance files remain Corpus / Provenance-owned
  or bridge support, not parser truth.
- Analytics files remain Analytics-owned or parser-normalized ingest bridge
  code, not parser truth.
- Local app backend and frontend files remain Local App / UI-owned or
  access/orchestration bridge code, not parser truth or analytics truth.
- Workbook output and Apps Script code remain Workbook / Transport-owned or
  transport bridge code, not parser truth.
- Quality tools remain Quality / Governance-owned, not runtime behavior.
- Future AI Integration remains deferred until a separate issue and contract
  authorizes a concrete AI integration surface.

Source comments are not authorized in issue #218. If a later thread needs a
source-level bridge-code comment, it must name the exact file and purpose in a
new contract.

## Deferred Item #3 Scope

These actions are deferred to item #3 or a later scoped issue:

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
- changing parser, runtime, analytics, local app, workbook, transport,
  Apps Script, Sheets, AI, or production behavior.

## Protected Surfaces

This map does not authorize changes to:

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
- file layout;
- secrets, credentials, API keys, tokens, webhook URLs, environment variables,
  raw local logs, generated data, runtime status artifacts, transport failure
  artifacts, workbook exports, local JSONL artifacts, generated SQLite files,
  or local-only artifacts.

## Validation Expectations

For issue #218, validation should prove docs consistency and scope control:

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

Runtime tests are not required when the diff stays documentation-only and
within the authorized files.

## Follow-Up Questions

- Should a future issue add a `docs/architecture/` directory once architecture
  docs grow beyond this single map?
- Should a future issue add README links to this map after review?
- Should future local app contracts shift from `analytics_*` to `local_app_*`
  prefixes?
- Should `.github` issue and PR templates learn the accepted internal project
  vocabulary?
- Should `runtime_surfaces.py`, `status_api.py`, `config.py`, and
  `diagnostics.py` get source-level bridge comments under a later contract?
- Should a future advisory import-boundary report exist before any physical
  package or test-layout work?
