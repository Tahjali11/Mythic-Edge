# Mythic Edge

Mythic Edge is a local-first MTG Arena parser and analytics foundation.

Its current job is to turn MTGA `Player.log` evidence into reliable parser-managed match, game, card, runtime, and workbook-facing facts. Its longer-term job is to support high-quality local analytics and AI-assisted coaching without letting workbook formulas, dashboards, or AI outputs become the source of truth.

At a high level, Mythic Edge:

1. Watches MTGA's `Player.log` while you play.
2. Parses useful Arena events out of noisy log output.
3. Maintains live match and game state in Python.
4. Produces normalized match, game, card, runtime, and workbook-facing rows.
5. Posts parser-managed rows to Google Sheets through a webhook.
6. Preserves local diagnostics, replay data, snapshots, and drift evidence for debugging.
7. Provides a hardened foundation for future analytics, deck-building tools, and AI-assisted coaching.

## Core Principle

The most important design rule is that parser-owned truth stays in the parser.

```text
MTGA Player.log
  -> raw observable evidence
  -> parser event stream
  -> parser/state interpretation
  -> normalized Python models and sheet schemas
  -> webhook transport
  -> workbook landing sheets
  -> helper formulas, dashboards, analytics, and AI-assisted interpretation
```

Layer ownership:

- MTGA `Player.log`: raw observable evidence only.
- Python parser/state layer: owns event interpretation, match facts, game facts, card/action facts, final reconciliation, and parser-managed outputs.
- Webhook and Apps Script: transport and upsert logic only.
- Workbook landing sheets: store parser-managed rows.
- Helper tabs and dashboards: support, display, and analysis only.
- AI analytics: summarization, classification, hypothesis generation, and coaching recommendations only.

AI output, deck-tier guesses, user annotations, helper formulas, and dashboard summaries should not silently become parser truth.

## Main Runtime Surfaces

The shortest mental model is:

- `main.py` starts the parser.
- `src/mythic_edge_parser/app/runner.py` owns the main runtime loop.
- `src/mythic_edge_parser/app/state.py` owns match and game interpretation state.
- `src/mythic_edge_parser/app/models.py` defines normalized row and summary shapes.
- `src/mythic_edge_parser/app/extractors.py` extracts structured facts from raw event payloads.
- `src/mythic_edge_parser/events.py` defines parser event classes and payload surfaces.
- `src/mythic_edge_parser/app/sheet_schema.py` defines workbook-facing sync fields and headers.
- `src/mythic_edge_parser/app/sheet_exports.py` builds runtime workbook export rows.
- `src/mythic_edge_parser/app/outputs.py` posts outbound rows.
- `tools/google_apps_script/Code.gs` receives and upserts rows in Google Sheets.

The Python-side `MATCH_LOG_SYNC_FIELDS` and `GAME_LOG_SYNC_FIELDS` contracts are authoritative for sheet sync fields. Apps Script parity should be checked against the receiver field-map builders in `tools/google_apps_script/Code.gs`.

## What To Run

Primary runtime and operator commands:

- `main.py`
  Current parser entrypoint.
- `live_print_filtered_v11_match_summary.py`
  Compatibility entrypoint kept for older local habits.
- `tools/auto_launcher/manasight_launcher_auto.py`
  Local launcher and runtime health UI.

Data refresh and repair tools:

- `sync_card_catalog.py`
  Builds the Arena-aware card catalog.
- `validate_arena_ids.py`
  Checks observed Arena IDs against the local catalog.
- `sync_tier_buckets.py`
  Refreshes tier-source snapshots and normalization data.
- `backfill_game_log_from_match_logs.py`
  Replays saved local match logs into normalized historical game rows.
- `refresh_match_history_from_match_logs.py`
  Refreshes match-history artifacts from saved logs.
- `audit_player_log_drift.py`
  Builds Player.log drift evidence for parser resilience work.

Deck, card, and hand-confirmation tools:

- `import_current_decklist.py`
- `record_hand_confirmation.py`
- `sync_hand_confirmation_file.py`
- `refresh_grp_id_overrides.py`
- `score_grp_id_candidates.py`

## Folder Map

### Root

- `README.md`
  This project overview.
- `AGENTS.md`
  Short Codex entrypoint and non-negotiable repo rules.
- `pyproject.toml`
  Python package metadata, runtime dependencies, optional development dependencies, and tool configuration.
- `CONTRIBUTING.md`
  Contributor workflow guidance.

### Parser Package

- `src/mythic_edge_parser/app/`
  App-level parser logic, state, models, outputs, diagnostics, runtime surfaces, card performance, sheet exports, drift sensors, and repair helpers.
- `src/mythic_edge_parser/parsers/`
  Individual MTGA event and API parsers.
- `src/mythic_edge_parser/parsers/gre/`
  GRE-specific game-state, connection, turn, and result parsers.
- `src/mythic_edge_parser/log/`
  Log entry parsing, tailing, and buffering utilities.
- `src/mythic_edge_parser/events.py`
  Parser event classes and payload behavior.
- `src/mythic_edge_parser/router.py`
  Event routing.
- `src/mythic_edge_parser/stream.py`
  Stream integration helpers.
- `src/mythic_edge_parser/sanitize.py`
  Redaction and scrub support.

### Tests And Snapshots

- `tests/`
  Unit, integration, regression, parser, workbook-facing schema, and hardening tests.
- `tests/fixtures/parser_regression_*.json`
  Regression fixtures for saved parser behavior.
- `tests/fixtures/schema_snapshots/`
  Approved snapshots for parser event classes, parser payload keys, workbook row keys, sheet schema surfaces, runtime export row keys, and Apps Script repo parity.

Snapshot updates are intentionally controlled. Do not auto-update schema snapshots just because a test fails. A snapshot change should be tied to an issue, contract, review, and explicit approval.

### Workflow And Governance Docs

- `docs/agent_constitution.md`
  Human-readable Codex constitution and truth-ownership rules.
- `docs/codex_skills/`
  Repo-owned Codex skill source for workflow, constitution feedback packets, and Codex H synthesis.
- `docs/agent_rules.yml`
  Terse machine-readable workflow and safety index.
- `docs/codex_module_workflow.md`
  Module workflow guide.
- `docs/agent_threads/`
  Role-specific instructions for Codex A through F plus review and contract-test variants.
- `docs/templates/`
  Problem representation, contract, implementation handoff, review, and workflow handoff templates.
- `docs/contracts/`
  Module and hardening contracts.
- `docs/implementation_handoffs/`
  Implementation comparison and handoff artifacts.
- `docs/contract_test_reports/`
  Review and contract-test reports.
- `docs/decisions/`
  Architecture Decision Record policy and template.

ADRs are for durable cross-project decisions. They do not replace issue-scoped contracts and do not authorize protected-surface changes by implication.

### Tools

- `tools/auto_launcher/`
  Local launcher app and operator-facing health checks.
- `tools/google_apps_script/`
  Google Sheets webhook receiver code.
- `tools/check_protected_surfaces.py`
  Guardrail for detecting risky changes to protected parser, workbook, webhook, schema, local artifact, and generated-data surfaces.
- `tools/run_repo_checks.ps1`
  Windows PowerShell repo validation helper.
- `tools/run_touched_file_checks.ps1`
  Focused Windows PowerShell validation helper for changed Python files.
- `tools/scryfall_parser/`
  Card-catalog sync wrapper.

### Local Data

Most `data/` content is local or generated. Treat it as evidence and diagnostics, not normal source code.

- `data/match_logs/`
  Saved local JSONL match/game event logs.
- `data/runtime_logs/`
  Runtime logs.
- `data/status/`
  Latest runtime status and active match snapshots.
- `data/failed_posts/`
  Rows that failed to post to Google Sheets.
- `data/bad_events/`
  Event or router failures captured for debugging.
- `data/oracle_data/`
  Generated card catalog outputs.
- `data/tier_sources/`
  Tier-source snapshots and normalization data.

Do not commit raw local logs, secrets, webhook URLs, runtime status files, failed posts, generated card data, or workbook exports unless there is an explicit issue and redaction plan.

## Runtime Health And Troubleshooting

When the parser is running, start troubleshooting from:

- `data/status/manasight_status_latest.json`
  Fast status snapshot for parser health, last event, active context, and webhook state.
- `data/runtime_logs/<MM_DD_YY>/manasight_runtime.log`
  Human-readable runtime log.
- `data/failed_posts/<MM_DD_YY>/failed_posts_<MM_DD_YY>.jsonl`
  Rows that failed to reach the Google Sheets webhook.
- `data/bad_events/<MM_DD_YY>/bad_events_<MM_DD_YY>.jsonl`
  Per-event parser or router failures.

The auto launcher surfaces much of this in its runtime health panel: parser status, last event, active match/game context, webhook success/failure counts, and shortcuts to status, logs, failed posts, and bad events.

## Google Sheets Design

The workbook is organized around normalized parser rows rather than raw-event dumping.

Landing sheets:

- `Match Log`
  One parser-managed row per match.
- `Game Log`
  One parser-managed row per game.
- `Webhook Debug`
  Transport/debug observability.

Support and display sheets:

- `Helper Table`
  Formula support, dropdowns, tier buckets, and classifications.
- `Tier Source Data`
  Hidden support data for external tier-source snapshots.
- `Dashboard`
  Reporting and review views.
- `Experiments`
  Experiment definitions and comparison configuration.

For workbook-connected changes, keep these states distinct:

- repository code state
- deployed Apps Script state
- live workbook state

If they differ, label the problem as repo drift, deployment drift, workbook drift, or combined drift.

## Card Data

The project uses Arena-aware card identity. MTGA logs often expose Arena-facing identifiers such as `grpId`, not only card names or Oracle-style IDs.

When card identity matters, distinguish:

- Arena `grpId`
- `instance_id`
- `overlayGrpId`
- `objectSourceGrpId`
- card name or display name
- Scryfall or local catalog identity

## Player.log Drift And Evidence Ledger Direction

`Player.log` is the ultimate observable evidence source for the local parser, but it is not absolute game truth. The real game state lives inside Arena; the parser only sees what Arena emits.

The project direction is to maintain drift-aware parser outputs and evidence-ledger support so that future Arena log changes are visible, explicit, and recoverable where possible.

Important value-source labels:

- `observed`: directly from current log evidence
- `derived`: computed from observed facts
- `inferred`: best-effort fallback
- `unknown`: unavailable
- `conflict`: evidence disagrees
- `legacy_enriched`: enriched from older retained metadata

The ledger and drift tooling should support parser QA, provenance, and degradation reporting. They should not become a second parser, a workbook workaround, or an excuse to hide uncertainty.

## Analytics And AI Boundary

Future analytics should be built on deterministic local outputs first:

- matchup performance
- game-one versus post-board performance
- play/draw outcomes
- mulligan outcomes
- opening-hand patterns
- sideboarding lifecycle and submitted deck state
- card inclusion and exclusion signals
- sample-size and confidence warnings
- parser drift and data-quality metadata

AI-assisted coaching can then explain, summarize, compare, classify, and suggest hypotheses from parser-produced facts. It should not decide match result, game result, play/draw, mulligan count, opening hand, card actions, deck submission, webhook row identity, workbook schema, or parser-managed fields.

Plainly: local deterministic code should decide; AI may explain and recommend with labels.

## Codex And GitHub Workflow

For non-trivial work, Mythic Edge uses an artifact-first Codex workflow. The durable artifact matters more than chat history.

Current role path:

```text
A Thinker
  -> B Module Contract Writer
  -> C Module Implementer
  -> E Module Reviewer
  -> F Module Submitter
  -> G Integration Deployer
```

Use D Module Fixer only after a concrete review, contract-test, or CI finding.

Role summary:

- A Thinker: problem representation, scope, risk, first inspection order, and GitHub issue.
- B Module Contract Writer: module contract, guarantees, unknowns, suspected gaps, and test obligations.
- C Module Implementer: implementation or comparison against the contract, focused tests, and handoff.
- D Module Fixer: narrow fixes for concrete findings only.
- E Module Reviewer: findings-first review against issue, contract, handoff, diff, and validation.
- F Module Submitter: stage intended files, commit, push, and open or update a draft PR.
- G Integration Deployer: integration readiness, merge readiness, tracker updates, issue closure, and branch sync after explicit approval.
- H Constitutional Lawyer: special governance synthesis role for constitution feedback packets, amendment proposals, minority reports, and watch lists.

H is not part of the normal module implementation path. Use it after major suites, before major governance changes, or after serious workflow failures.

Common non-production integration branches:

- `codex/parser-module-audit-suite`
- `codex/code-hardening-suite`

Do not merge to `main`, deploy, change production workbook behavior, or alter external connections without explicit approval.

## Code Hardening Guardrails

The hardening suite is intended to make the project safer to change before major analytics and coaching work.

Current guardrail themes include:

- protected-surface checks
- PR drift budgets
- advisory Pyright type-checking
- deterministic fuzz-style tests for shared parser helpers
- parser event/schema snapshot tests
- ADR policy for durable architecture decisions
- agent docs consistency checks
- content-based secret scanning
- role-scope checks for workflow threads
- validation command selection from `docs/validation_matrix.json`
- local artifact reporting from `docs/local_artifacts_manifest.json`
- read-only workbook/App Script state probing
- repo-owned Codex skill installation

Useful focused commands:

```powershell
py -m pytest -q tests\test_api_common.py
py -m pytest -q tests\test_event_schema_snapshots.py
py -m pytest -q tests
py -m ruff check src tests
pyright
py tools\check_protected_surfaces.py --base origin/main
py tools\check_agent_docs.py
py tools\check_secret_patterns.py --all
py tools\select_validation.py --changed --base origin/main
py tools\check_role_scope.py --role E --paths docs\contract_test_reports\example.md
py tools\check_local_environment.py --profile clean_clone
py tools\report_workbook_state.py
```

When Pyright is advisory, record findings without treating nonzero output as a release blocker unless a later contract escalates that requirement.

To install or refresh the repo-owned Codex skills on a machine:

```powershell
py tools\install_mythic_edge_skill.py --all
```

After that, local constitution feedback threads can start with:

```text
Use $mythic-edge-constitution-review.
```

Codex H synthesis threads can start with:

```text
Use $mythic-edge-workflow and $mythic-edge-constitutional-lawyer.
```

## Local Setup

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -e ".[dev]"
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Small validation loop:

```powershell
py -m pytest -q tests
py -m ruff check src tests
git diff --check
```

Windows repo-level helper:

```powershell
.\tools\run_repo_checks.ps1
.\tools\run_repo_checks.ps1 -Coverage
```

Focused touched-file helper:

```powershell
.\tools\run_touched_file_checks.ps1 src\mythic_edge_parser\app\models.py tests\test_app_models.py
```

## Current Engineering Direction

The project has moved from "make the parser work" toward "make the parser trustworthy enough to build analytics on top of it."

The practical sequence is:

1. Parser module audit suite.
   Clarify contracts and tests for parser modules.
2. Code hardening suite.
   Add guardrails that make future changes safer to review.
3. Player.log evidence ledger and drift protection.
   Make log-format changes visible and preserve explicit uncertainty.
4. Local deterministic analytics.
   Build reliable statistics from parser-managed outputs.
5. AI-assisted coaching.
   Use AI to explain, compare, and suggest hypotheses from trusted local facts and curated strategy sources.

That order matters because analytics and coaching are only as useful as the parser-managed facts underneath them.

## Notes

- `__pycache__` and `.pytest_cache` are normal Python byproducts.
- The parser is designed to tolerate partial live updates and reconcile final values later.
- Treat provisional live values differently from final reconciled values.
- Schema snapshots are protective tests, not casual golden files.
- Use issues, contracts, handoffs, reports, PRs, and ADRs as durable project memory.
