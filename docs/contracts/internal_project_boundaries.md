# Internal Project Boundaries Contract

## Module

Internal project boundaries for Mythic Edge.

Plain English: Mythic Edge is still one repository and one Python package, but
it now contains several distinct project areas. This contract names those
areas, defines what each one owns, and records allowed and forbidden dependency
directions before any future package split, file move, or repository split.

This is a contract-writing artifact only. It does not implement code, move
files, rename packages, change imports, add CI gates, open a PR, target `main`,
or change runtime behavior.

## Source Issue

- Source issue: <https://github.com/Tahjali11/Mythic-Edge/issues/215>
- Tracker: N/A
- Current branch: `codex/analytics-foundation`
- Observed local branch state during this Codex B pass:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
```

- Observed commit during this Codex B pass:

```text
7b2ad89
```

## Authority And Source Artifacts Read

- issue #215
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- current contract inventory under `docs/contracts/`
- module inventory under `src/mythic_edge_parser/`
- frontend inventory under `frontend/src/`
- tool inventory under `tools/`
- test import inventory under `tests/`
- `pyproject.toml`

ADR-0006 is currently marked `Proposed`. This contract may use it as relevant
architecture context, but it must not treat ADR-0006 as accepted authority until
the repo workflow accepts or supersedes it.

## Risk Tier

Medium-High.

The immediate artifact is documentation-only, but the topic can easily lead to
high-risk physical reorganizations. Future work based on this contract can
touch import graphs, package data, test layout, CI behavior, local app behavior,
parser behavior, workbook transport, or future AI surfaces if it is not
carefully scoped.

## Owning Layer

Primary owner: Quality / Governance.

Truth boundary:

- Parser/state owns MTGA event interpretation, parser event classes, match and
  game identity, parser-owned deduplication, final reconciliation, and
  parser-normalized match/game/card/action facts.
- Corpus / Provenance owns evidence, confidence, source, finality, drift,
  fixtures, replay harnesses, and validation support. It does not become a
  second parser.
- Analytics owns local deterministic storage, views, summaries, warnings, and
  query surfaces from parser-normalized facts. It does not own parser truth.
- Local App / UI owns local access, display, import controls, setup status, and
  orchestration. It does not own truth.
- Workbook / Transport owns row contracts, transport shape, sheet mappings, and
  Apps Script parity. It consumes parser-normalized outputs and does not own
  parser truth.
- Quality / Governance owns checks, contracts, ADRs, workflow docs, and repo
  safety policy. It may inspect all layers, but it must not become runtime
  product behavior.
- AI Integration is future/deferred. It may later explain, summarize, classify,
  or propose hypotheses only under separate contract. It must not own parser
  truth, analytics truth, workbook truth, hidden-card truth, gameplay
  correctness, or strategic certainty.

## Files Owned By This Contract

This contract owns only:

- `docs/contracts/internal_project_boundaries.md`

Future Codex C comparison work may create:

- `docs/implementation_handoffs/internal_project_boundaries_comparison.md`

Future implementation work may propose narrow changes to governance docs,
labels, validation tooling, or docs organization only after a scoped contract
or follow-up issue authorizes them.

This contract does not authorize edits to parser code, analytics code, local
app code, frontend code, workbook code, Apps Script code, test fixtures,
snapshots, generated data, package names, imports, or runtime configuration.

## Public Interface

This contract defines repository architecture vocabulary and dependency
boundaries. It does not define a runtime API.

The public governance interface is:

- internal project names;
- owner responsibilities;
- observed module ownership map;
- allowed dependency directions;
- forbidden dependency directions;
- truth-ownership boundaries;
- contract naming/grouping guidance;
- test naming and future test layout guidance;
- issue prefix guidance;
- criteria for future file moves;
- criteria for future package splits;
- criteria for any later separate repository split;
- validation and enforcement options.

## Required Internal Projects

### Parser

Owns:

- MTGA log entry parsing;
- parser event classes and event schemas;
- parser routing;
- parser state;
- match identity;
- game identity;
- parser-owned deduplication;
- final reconciliation;
- parser-normalized match facts;
- parser-normalized game facts;
- parser-normalized card identity facts;
- parser-normalized gameplay actions;
- parser-normalized opponent-card observations when directly supported by
  Player.log evidence;
- parser diagnostics that describe parser behavior or parser degradation.

Must not depend on analytics, local app/UI, workbook transport, Apps Script, or
future AI integration.

### Corpus / Provenance

Owns:

- Player.log evidence ledger schema and validation;
- source, confidence, finality, drift, and evidence-status vocabulary;
- runtime field evidence reports;
- evidence schema snapshots and drift reports;
- evidence invariant execution;
- golden replay harnesses;
- saved-event replay utilities when used for parser QA;
- feature-equity corpus reports;
- sanitized golden fixtures and drift baselines;
- log drift sensor behavior and reports.

Supports parser reliability but must not become a second parser, fix parser
facts downstream, or treat fixtures as broader truth than their provenance
allows.

### Analytics

Owns:

- local SQLite schema and migrations;
- analytics migration loading;
- parser-normalized replay ingest;
- gameplay-action ingest from parser-normalized inputs;
- opponent-card-observation ingest from parser-normalized inputs;
- field-evidence ingest from approved ledger outputs;
- deterministic SQL views;
- local query helpers;
- sample-size and confidence warnings;
- analytics-facing summaries and local database status.

Reads parser-normalized facts and provenance metadata. It must not reinterpret
raw Player.log entries, override parser-managed values, or treat analytics
labels as parser truth.

### Local App / UI

Owns:

- FastAPI local backend;
- React/Vite frontend;
- local developer launcher;
- setup/status display;
- upload and manual import controls;
- sanitized import job status;
- local analytics display and navigation;
- local-only orchestration between browser, backend, and analytics services.

This is an access, display, and orchestration surface. It must not correct
parser facts, own analytics truth, expose destructive actions without explicit
contract, or retain raw uploads unless separately authorized.

### Workbook / Transport

Owns:

- workbook-facing row contracts;
- sheet schema field lists;
- sheet export mappings;
- webhook payload shape;
- Apps Script parity checks;
- workbook sync boundaries;
- failed-post and transport diagnostics when separately authorized.

Consumes parser-normalized outputs. It must not feed workbook formulas,
webhook state, or Apps Script behavior back into parser truth.

### Quality / Governance

Owns:

- protected-surface checks;
- secret and private-marker scans;
- validation selectors;
- advisory hardening reports;
- contract, handoff, and review artifacts;
- ADRs and decision indexes;
- workflow docs and templates;
- branch, PR, and issue lifecycle conventions;
- repo maturity tracking.

May inspect all layers. Must not become runtime product behavior or silently
authorize protected-surface changes.

### Future AI Integration

Deferred project. It does not currently own a runtime module.

May later own, only after separate issue and contract:

- summaries;
- explanations;
- coaching hypotheses;
- matchup memo drafts;
- sideboard guide drafts;
- model-provider integration boundaries;
- AI-output provenance, review, and retention rules.

Must not own parser truth, analytics truth, hidden-card inference, gameplay
correctness, player-mistake labels, workbook schema, webhook shape, Apps Script
behavior, model-provider truth, or strategic certainty.

### Shared Support And Bridge Code

Some current modules support more than one project area. Until a future
contract physically reorganizes code, these modules should be classified by
their nearest truth owner and treated as shared support or bridge code.

Examples:

- card catalog and `grp_id` helpers support parser card identity, provenance,
  and analytics, but they do not override parser truth;
- legacy JSONL adapters bridge local artifacts into parser-normalized replay
  input, but they do not turn legacy derived fields into parser truth;
- setup/status modules may read parser/runtime/config state for local display,
  but they do not own runtime behavior;
- CLI and tool wrappers may call project modules for validation, but the
  wrapper does not own the underlying truth.

Bridge code must be documented at the contract level when it crosses project
boundaries.

## Observed Current Behavior

Observed repository shape:

- The repo is a monorepo with one Python package named `mythic-edge-parser`.
- Most Python code lives under `src/mythic_edge_parser/`.
- `src/mythic_edge_parser/app/` currently contains parser truth modules,
  analytics modules, provenance modules, replay/corpus tools, card helpers,
  workbook outputs, runtime surfaces, diagnostics, and status helpers.
- `src/mythic_edge_parser/parsers/` contains event parser modules and GRE
  parser submodules.
- `src/mythic_edge_parser/events.py`, `router.py`, `stream.py`, `event_bus.py`,
  and `log/` support parser event lifecycle and stream handling.
- `src/mythic_edge_parser/local_app/` contains local app backend, setup status,
  import job, path, and config code.
- `frontend/src/` contains the React/Vite local app UI and frontend tests.
- `tools/` contains quality/governance scripts, evidence report entrypoints,
  developer app launcher tooling, Google Apps Script code, card-data tooling,
  and automation wrappers.
- `tests/` is a flat test directory with naming prefixes that already signal
  parser, evidence, analytics, local app, workbook, and tool ownership.
- `docs/contracts/` is a flat contract directory whose prefixes already signal
  project ownership in practice.
- `pyproject.toml` packages migrations as data inside
  `mythic_edge_parser.app.analytics_migrations`, confirming analytics is still
  physically inside the existing parser package.

Observed import behavior:

- Tests and tools import across many project areas for validation.
- `local_app` imports analytics ingest, analytics legacy JSONL adapter, and
  analytics migration loader for local import/setup behavior.
- Analytics tests import parser-normalized modules such as gameplay actions and
  opponent-card observations to prove ingest behavior.
- Evidence tools import evidence modules through small command wrappers.
- Parser tests primarily import parser events, router, parsers, state, models,
  transforms, and sheet schema.

This contract records intended ownership and dependency direction without
claiming the current physical package layout already enforces it.

## Current Module Ownership Map

### Parser-owned Or Parser-core Modules

- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/event_bus.py`
- `src/mythic_edge_parser/log/`
- `src/mythic_edge_parser/parsers/`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/event_identity.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/opponent_card_observations.py`
- `src/mythic_edge_parser/app/hand_confirmations.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/runner.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- parser-focused tests such as `tests/test_state.py`,
  `tests/test_app_models.py`, `tests/test_parsers.py`, parser-specific GRE
  tests, draft parser tests, router tests, stream tests, and regression tests.

### Corpus / Provenance-owned Modules

- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/evidence_schema_snapshot.py`
- `src/mythic_edge_parser/app/evidence_schema_drift_report.py`
- `src/mythic_edge_parser/app/evidence_invariant_execution.py`
- `src/mythic_edge_parser/app/evidence_runtime_status.py`
- `src/mythic_edge_parser/app/evidence_validation_report_wiring.py`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- `src/mythic_edge_parser/app/golden_replay.py`
- `src/mythic_edge_parser/app/saved_event_replay.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py`
- evidence, drift, golden replay, schema snapshot, and feature-equity tests;
- sanitized fixture, snapshot, and drift report policy artifacts.

### Analytics-owned Modules

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/analytics_migrations/`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- `src/mythic_edge_parser/app/card_performance.py`
- analytics schema, migration, ingest, replay view, field evidence, legacy
  adapter, derived view, and local database tests.

`analytics_legacy_jsonl_adapter.py` is bridge code. It may read local legacy
artifact shapes and produce parser-normalized replay input under its contract,
but it must not treat legacy derived fields as parser truth or store raw
Player.log payloads in SQLite.

### Shared Card / Deck Support Modules

- `src/mythic_edge_parser/app/card_catalog.py`
- `src/mythic_edge_parser/app/card_catalog_refresh.py`
- `src/mythic_edge_parser/app/arena_id_validation.py`
- `src/mythic_edge_parser/app/decklists.py`
- `src/mythic_edge_parser/app/grp_id_catalog.py`
- `src/mythic_edge_parser/app/grp_id_candidates.py`
- `src/mythic_edge_parser/app/tier_sync.py`

These modules should remain explicitly scoped by their contracts and tests.
They may support parser, provenance, and analytics work, but must not become a
hidden analytics-to-parser feedback path.

### Local App / UI-owned Modules

- `src/mythic_edge_parser/local_app/`
- `frontend/`
- `tools/dev_app/`
- `Start Mythic Edge Dev App.cmd`
- local app backend, setup-status, launcher, browser upload, manual import,
  and frontend tests.

### Workbook / Transport-owned Modules

- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `src/mythic_edge_parser/app/sheet_exports.py`
- `tools/google_apps_script/Code.gs`
- workbook, sheet schema, sheet export, output, webhook payload, Apps Script,
  and protected-surface parity tests.

### Runtime / Configuration Support Modules

- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/app/diagnostics.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/status_api.py`
- `src/mythic_edge_parser/sanitize.py`
- `src/mythic_edge_parser/util.py`

These are support modules. Their owner must be named by the contract that
changes them. They must not become a shortcut for moving truth between parser,
workbook, analytics, local app, or AI layers.

### Quality / Governance-owned Areas

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/`
- `docs/templates/`
- `docs/decisions/`
- `docs/contracts/`
- `docs/implementation_handoffs/`
- `docs/contract_test_reports/`
- `tools/check_*.py`
- `tools/run_*.py`
- `tools/select_validation.py`
- `.github/workflows/`
- `.github/pull_request_template.md`
- repository-wide hardening reports and governance tests.

## Required Dependency Direction

Default allowed direction:

```text
Parser -> shared stdlib/package support only
Corpus / Provenance -> parser outputs/events/fixtures plus shared support
Analytics -> parser-normalized facts, approved provenance, migrations, shared support
Local App / UI -> backend/import/analytics/status services and display models
Workbook / Transport -> parser-normalized row contracts and transport support
AI Integration -> approved analytics/provenance/UI context only
Quality / Governance -> may inspect all layers without becoming runtime behavior
```

Primary non-negotiable rule:

```text
Parser must not depend on Analytics, Local App / UI, Workbook / Transport, or AI Integration.
```

Other required rules:

- Corpus / Provenance may read parser facts and evidence; it must not write
  corrected parser facts back into parser state.
- Analytics may read parser-normalized facts and approved provenance; it must
  not read raw private Player.log payloads as its own source of truth.
- Local App / UI may call backend and analytics services; it must not implement
  parser corrections, analytics truth overrides, or workbook schema logic in
  UI state.
- Workbook / Transport may consume parser-normalized row contracts; it must not
  use workbook formulas, webhook responses, or Apps Script state as upstream
  parser truth.
- Quality / Governance may inspect all layers; it must not silently turn a
  check or report into a required CI gate without a scoped contract or user
  approval.
- Future AI Integration may read approved downstream facts; it must not write
  parser facts, analytics facts, workbook facts, credentials, or production
  state.

## Forbidden Dependency Directions

Forbidden unless a future contract explicitly authorizes a narrow bridge:

- Parser importing analytics modules.
- Parser importing `local_app` modules.
- Parser importing frontend-generated code or UI state.
- Parser importing workbook transport modules for interpretation decisions.
- Parser importing future AI/model-provider modules.
- Analytics importing raw Player.log parsers to create alternative truth paths.
- Analytics writing parser state, parser events, workbook schemas, or Apps
  Script logic.
- Local App / UI importing parser internals directly for browser-side truth
  decisions.
- Frontend code depending on Python internals except through documented
  backend API shapes.
- Workbook / Transport importing analytics, local UI, or AI code.
- Provenance code overwriting parser truth or treating fixtures as complete
  game truth.
- Quality tooling changing production behavior as a side effect of validation.
- Future AI code importing or mutating parser state, workbook schemas, webhook
  payloads, credentials, runtime files, or generated database files.

## Truth Ownership Rules

The following ownership rules must remain stable:

- MTGA `Player.log` is the ultimate observable raw evidence source, but not
  absolute game truth.
- Parser/state owns interpretation of Player.log evidence.
- `MatchSummary`, `GameSummary`, and parser-normalized event/action outputs own
  parser-managed facts.
- Evidence ledger owns provenance, drift, uncertainty, and validation metadata.
- Analytics reads downstream parser-normalized facts and provenance.
- Local App / UI displays, imports, filters, and orchestrates local workflows.
- Workbook / Transport transports and displays parser-normalized rows.
- Google Sheets, formulas, dashboards, AI outputs, user annotations, and
  coaching notes are downstream analysis or collaboration surfaces.
- Future AI output is inference, enrichment, explanation, or recommendation
  only.

Any future change that moves truth ownership between these layers must stop and
route through a new issue, contract, and review.

## Docs And Contract Organization Strategy

Current required behavior:

- Keep `docs/contracts/` flat unless a later contract authorizes a physical
  docs reorganization.
- Preserve current filenames and links.
- Use stable prefixes to signal owner:
  - `parser_*`
  - `player_log_evidence_ledger_*`
  - `analytics_*`
  - `external_integration_*`
  - `governance_*`
  - `quality_*`
  - `code_hardening_*`
  - `repo_wide_*`
  - future `workbook_transport_*`
  - future `local_app_*` when a contract is not already under `analytics_*`
  - future `ai_*`
- Keep contracts as the durable boundary artifacts for workflow threads.
- Keep implementation handoffs and contract-test reports separate from source
  contracts.

Future optional behavior:

- A later contract may propose `docs/contracts/parser/`,
  `docs/contracts/analytics/`, `docs/contracts/provenance/`, or similar
  subdirectories only after references, templates, and workflows are audited.
- Any docs move must preserve old links or include an explicit migration note.

## Test Naming And Future Test Layout Strategy

Current required behavior:

- Keep the existing flat `tests/` layout.
- Use file prefixes and names that identify project ownership:
  - `test_parser_*` or parser-module names for Parser;
  - `test_evidence_*`, `test_runtime_field_evidence.py`,
    `test_golden_replay_*`, and drift/corpus names for Corpus / Provenance;
  - `test_analytics_*` for Analytics and local analytics app slices;
  - `test_sheet_*`, `test_webhook_*`, and Apps Script parity names for
    Workbook / Transport;
  - `test_agent_*`, `test_repo_wide_*`, `test_quality_*`, and tool names for
    Quality / Governance.
- Tests may import across boundaries to validate contracts, but should name the
  boundary under test clearly.

Future optional behavior:

- A later contract may propose grouped test directories such as
  `tests/parser/`, `tests/provenance/`, `tests/analytics/`,
  `tests/local_app/`, `tests/workbook_transport/`, and `tests/governance/`.
- Any test layout move must be a behavior-preserving move first, with focused
  test discovery validation before any logic change.

## Issue Prefix And Label Strategy

Recommended issue title prefixes:

- `[parser]`
- `[evidence-ledger]`
- `[corpus]`
- `[analytics]`
- `[analytics/app]`
- `[local-app]`
- `[workbook]`
- `[transport]`
- `[quality]`
- `[governance]`
- `[repo-wide]`
- `[architecture]`
- `[ai]`

Recommended label families, if the repo later adopts labels:

- `area:parser`
- `area:provenance`
- `area:corpus`
- `area:analytics`
- `area:local-app`
- `area:workbook-transport`
- `area:quality`
- `area:governance`
- `area:architecture`
- `area:ai`
- `risk:low`, `risk:medium`, `risk:medium-high`, `risk:high`
- `workflow:problem`, `workflow:contract`, `workflow:implementation`,
  `workflow:review`, `workflow:submitter`, `workflow:integration`

Labels and prefixes are routing aids only. They do not override contracts,
accepted ADRs, protected-surface rules, or user instructions.

## Future File-Move Criteria

A future physical file move is allowed only when all of the following are true:

1. A GitHub issue or problem representation names the move.
2. A contract defines the intended owner, public interface, import path policy,
   compatibility policy, and validation plan.
3. The current import graph has been inspected.
4. The move can be made in a behavior-preserving first pass.
5. Tests prove old behavior still works after the move.
6. Any compatibility shim, re-export, or deprecation path is explicit.
7. Protected surfaces are checked before and after.
8. Generated files, raw logs, secrets, database files, workbook exports, and
   local-only artifacts are not moved or committed.
9. Codex C reports exact files moved and exact imports changed.
10. Codex E reviews for accidental truth-boundary changes.

Recommended two-pass approach:

1. Move or re-export without behavior changes.
2. Make behavior improvements only under a separate scoped contract after the
   move is stable.

## Future Package-Split Criteria

A future package split is allowed only when all file-move criteria are met and
the following additional conditions are satisfied:

- The package public API is named and tested.
- Package data access is defined, especially SQL migrations and fixtures.
- Runtime entrypoints are identified.
- Cross-package imports are acyclic.
- Test selection still works from a clean checkout.
- Build and packaging metadata are updated under a scoped contract.
- Compatibility expectations are documented for existing scripts and tools.
- CI impact is known and reviewed before any required/failing gate is added.
- The split has an approved issue, contract, implementation handoff, and
  review report.

Package splitting must not happen as a side effect of unrelated parser,
analytics, UI, or workbook work.

## Future Separate-Repository Criteria

A separate repository split is out of scope for this issue.

Any future separate-repository split requires:

- explicit user approval;
- a dedicated issue and contract;
- an accepted or superseding ADR;
- stable public API and versioning strategy;
- cross-repo CI and release strategy;
- sanitized fixture and data-retention policy;
- secret and credential policy;
- rollback plan;
- documentation migration plan;
- clear maintainer workflow for issues, PRs, and trackers.

Candidate extraction order must be justified by current repo state. The
proposed ADR-0006 context suggests corpus/provenance first, parser second,
analytics later, and AI last, but this remains non-binding until accepted or
superseded.

## Validation And Enforcement Options

Approved first posture:

- advisory reports before failing gates;
- docs-only comparison before import refactors;
- narrow protected-surface checks;
- narrow secret/private-marker checks;
- focused import-boundary inspection with `rg`;
- targeted validation selected through existing workflow contracts.

Possible later tools:

- `tools/check_internal_project_boundaries.py` as an advisory report first;
- import graph reports grouped by internal project;
- contract-aware validation selection in `tools/select_validation.py`;
- CI artifact reports that do not fail until explicitly escalated;
- future failing gates only after a contract, review evidence, low false
  positive rate, and user-approved escalation.

No immediate failing CI gate is authorized by this contract.

## Required Guarantees

- The repo remains a monorepo during this contract.
- The Python package name and import paths remain unchanged during this
  contract.
- No runtime behavior changes during this contract.
- Parser truth ownership remains unchanged.
- Analytics remains downstream of parser-normalized facts.
- Corpus / Provenance remains QA/provenance support, not a second parser.
- Local App / UI remains access/display/orchestration.
- Workbook / Transport remains output transport and sync shape.
- Quality / Governance remains advisory/control-plane unless separately
  authorized.
- Future AI Integration remains deferred and non-authoritative.
- Any future boundary enforcement starts report-only unless separately
  authorized.

## Unknowns

- Whether the repo will adopt ADR-0006 as written, revise it, or supersede it.
- Whether future physical organization should prioritize packages,
  subpackages, docs grouping, test grouping, or only advisory tooling.
- Whether shared card/deck support should eventually become parser-owned,
  provenance-owned, analytics-owned, or its own support package.
- Whether local app contracts should continue under `analytics_*` prefixes or
  move to `local_app_*` prefixes after the analytics foundation stabilizes.
- Whether Apps Script parity checks should remain under Workbook / Transport
  or get a more specific transport/tooling sub-boundary.
- Whether a future AI integration will live in this repo, a separate package,
  or a separate repository.

## Suspected Gaps

- `src/mythic_edge_parser/app/` is currently too broad to communicate project
  ownership by path alone.
- Analytics, provenance, parser truth, workbook export, and runtime support
  modules share the same `app` namespace.
- Existing tests rely on naming conventions instead of physical test grouping.
- Existing contracts rely on prefixes instead of subdirectories.
- Bridge modules are not always marked as bridge code in file names.
- Boundary validation is not yet automated.
- Future agents may mistake proposed ADR-0006 for accepted authority if they
  do not check ADR status.
- A nested or mirror-like tree under `.github/` should be classified before any
  future repository cleanup or file-move pass changes it.

These gaps do not require immediate code changes. They are inputs for future
Codex C comparison, review, and possible governance/tooling work.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- event kind values;
- parser payload shapes;
- match identity;
- game identity;
- parser-owned deduplication;
- analytics behavior;
- SQLite schema or migrations;
- local app backend behavior;
- frontend behavior;
- workbook schema;
- workbook row field names;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- AI/model-provider behavior;
- OpenAI runtime integration;
- secrets, credentials, tokens, API keys, webhook URLs, or environment
  variables;
- raw Player.log files;
- local JSONL artifacts;
- generated SQLite database files;
- runtime status files;
- failed posts;
- workbook exports;
- generated data;
- local-only artifacts.

## Error Behavior

If future boundary comparison finds an import or ownership mismatch:

- report it as an observation first;
- classify it as current behavior, bridge code, suspected gap, or contract
  violation;
- do not move files or edit imports without a scoped follow-up contract;
- route ambiguous truth-boundary conflicts back to Codex B;
- route problem-framing conflicts back to Codex A;
- route governance-authority conflicts through Codex H or the normal workflow.

If a future enforcement tool produces noisy results:

- keep it advisory;
- do not make it a failing gate;
- document false positives and missing categories;
- require a later contract before escalation.

## Side Effects

Allowed side effect in this Codex B pass:

- create `docs/contracts/internal_project_boundaries.md`.

Forbidden side effects:

- moving files;
- renaming packages;
- changing imports;
- creating subpackages;
- creating a new repository;
- adding CI gates;
- editing parser/runtime/analytics/UI/workbook/webhook/App Script behavior;
- writing generated data or local artifacts;
- staging, committing, pushing, opening a PR, merging, or closing issues.

## Validation Requirements

Codex B validation for this contract:

```powershell
git status --short --branch
git diff --check
@'
docs/contracts/internal_project_boundaries.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/internal_project_boundaries.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Recommended Codex C comparison validation:

```powershell
git status --short --branch
rg -n "^from mythic_edge_parser|^import mythic_edge_parser" src tests tools -g "*.py"
rg -n "mythic_edge_parser\.(local_app|app\.analytics|app\.evidence|app\.sheet|app\.outputs|parsers|router|events)" src tests tools -g "*.py"
git diff --check
```

Codex C must not treat these import scans as failing gates. They are evidence
for a comparison report.

## Acceptance Criteria

- `docs/contracts/internal_project_boundaries.md` exists.
- The contract names the required internal projects.
- The contract defines owner responsibilities for each project.
- The contract includes a current module ownership map.
- The contract defines allowed dependency directions.
- The contract defines forbidden dependency directions.
- The contract restates truth-ownership boundaries.
- The contract recommends docs/contract naming strategy.
- The contract recommends test naming and future layout strategy.
- The contract recommends issue prefixes and possible labels.
- The contract defines criteria for future file moves.
- The contract defines criteria for future package splits.
- The contract defines criteria for any later separate repository split.
- The contract defines validation and enforcement options.
- The contract preserves protected surfaces and explicitly forbids behavior
  changes in this pass.
- Validation is reported in the final handoff.

## Next Workflow Action

Next recommended role: Codex C: Module Implementer / comparison thread.

Codex C should compare current repo organization, docs, tests, and imports
against this contract and produce a comparison artifact. Codex C should not
move files, rename packages, change imports, or implement behavior changes
unless the user explicitly authorizes a later implementation issue.

Pasteable Codex C prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #215.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/215

Branch:
codex/analytics-foundation

Source contract:
docs/contracts/internal_project_boundaries.md

Task:
Compare the current repo organization, imports, docs/contracts naming, tests,
tools, frontend, and package metadata against the internal project boundaries
contract. Produce:

docs/implementation_handoffs/internal_project_boundaries_comparison.md

Keep this pass comparison-focused unless the user explicitly authorizes
implementation.

Before editing:
- confirm the branch is codex/analytics-foundation;
- inspect git status and exclude unrelated changes;
- state what the boundary contract is supposed to do, what the current repo
  already does, what gaps remain, and the exact minimal comparison plan.

Do:
- compare current module ownership against the contract;
- identify bridge code and ambiguous ownership areas;
- identify observed import directions and suspected boundary risks;
- compare docs/contracts prefixes against the contract;
- compare test naming and future layout needs against the contract;
- compare issue prefix/label guidance against current usage if available;
- identify whether a future ADR, advisory import-boundary report, or docs
  organization follow-up is warranted;
- preserve parser truth ownership and protected surfaces.

Do not:
- move files;
- split repositories;
- rename packages;
- change imports;
- add CI gates;
- edit parser/runtime/analytics/UI/workbook/webhook/App Script behavior;
- change parser state final reconciliation;
- change parser event classes, event kind values, parser payload shapes,
  match/game identity, deduplication, SQLite schema/migrations, workbook schema,
  webhook payload shape, Apps Script behavior, Google Sheets behavior, output
  transport, production behavior, AI/model-provider behavior, secrets, raw
  logs, generated data, runtime status files, failed posts, workbook exports,
  local JSONL artifacts, generated SQLite files, or local-only artifacts;
- target main;
- close issue #215 unless explicitly asked;
- stage, commit, push, open a PR, or merge unless explicitly asked.

Validation:
git status --short --branch
rg -n "^from mythic_edge_parser|^import mythic_edge_parser" src tests tools -g "*.py"
rg -n "mythic_edge_parser\\.(local_app|app\\.analytics|app\\.evidence|app\\.sheet|app\\.outputs|parsers|router|events)" src tests tools -g "*.py"
git diff --check
@'
docs/contracts/internal_project_boundaries.md
docs/implementation_handoffs/internal_project_boundaries_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/internal_project_boundaries.md
docs/implementation_handoffs/internal_project_boundaries_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin

Final handoff must include:
- role performed;
- issue reviewed;
- source contract used;
- comparison artifact produced;
- current branch;
- observed matches;
- gaps and suspected risks;
- whether parser truth ownership remains protected;
- whether any forbidden scope was touched;
- validation results;
- next recommended role;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/215"
  tracker: ""
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #215"
  target_artifact: "docs/implementation_handoffs/internal_project_boundaries_comparison.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "docs/contracts/internal_project_boundaries.md path-scoped protected-surface check"
    - "docs/contracts/internal_project_boundaries.md path-scoped secret/private-marker check"
  stop_conditions:
    - "Do not move files."
    - "Do not split repositories."
    - "Do not rename packages."
    - "Do not change imports."
    - "Do not change parser/runtime/analytics/UI/workbook/webhook/App Script/Sheets/AI/production behavior."
    - "Do not add CI gates."
    - "Do not target main."
```
