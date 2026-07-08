# Core Analytics Ingest Residual Decomposition Decision Packet

Status: Draft contract for review

Role: Codex B - Module Contract Writer

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/716>

Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>

Residual queue: <https://github.com/Tahjali11/Mythic-Edge/issues/710>

Residual promotion issue: <https://github.com/Tahjali11/Mythic-Edge/issues/715>

Target candidate: `src/mythic_edge_parser/app/analytics_ingest.py`

Candidate id: `analytics-ingest`

Candidate class binding: issue #716 extension, defined in
"Phase 5 Packet Schema And Vocabulary Binding" below.

Target commit: `9528bb3bee9c1d241268cb8a7d1a806b118471de`

## Module

`core_analytics_ingest_residual_decomposition_decision_packet`

This contract is the Phase 5 residual decomposition decision packet for the
local analytics ingest module.

Plain English: `src/mythic_edge_parser/app/analytics_ingest.py` receives
parser-produced facts, normalizes approved replay or live-capture payloads, and
writes rows into the local analytics SQLite database with provenance and
public-safe validation. This packet decides whether the file may later be split
into smaller same-repo modules while preserving behavior. It does not implement
that split.

This contract is planning-only. It does not implement code, move files, open a
PR, run ARS, run Refactor Scout, inspect private logs, change parser behavior,
change parser truth ownership, change SQLite schema or persisted-data behavior,
change analytics ingest behavior, change API/frontend/live-capture behavior,
change workbook/webhook/Apps Script behavior, change CI, or claim readiness,
reliability readiness, parser truth, analytics truth, AI truth, coaching truth,
security assurance, privacy assurance, release readiness, deploy readiness, or
production readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: <https://github.com/Tahjali11/Mythic-Edge>
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/716>
- Project roadmap / tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Broad decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>
- Residual queue: <https://github.com/Tahjali11/Mythic-Edge/issues/710>
- Residual promotion issue: <https://github.com/Tahjali11/Mythic-Edge/issues/715>
- Target artifact:
  `docs/contracts/core_analytics_ingest_residual_decomposition_decision_packet.md`

## Source Artifacts Inspected

- GitHub issue #716
- GitHub issue #715
- GitHub issue #710
- `AGENTS.md`
- `docs/agent_threads/module_contract.md`
- `docs/codex_module_workflow.md`
- `docs/templates/module_contract.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
- `docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`
- `docs/contracts/core_event_bus_support_decomposition_decision_packet.md`
- `docs/contracts/core_protected_surface_gate_decomposition_decision_packet.md`
- `docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md`
- `docs/contracts/parser_run_statistics_and_dropped_fact_counters.md`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_select_validation.py`

Inspection of `analytics_ingest.py` was limited to public source structure,
function names, imports/call-site references, and responsibility mapping. No
private `Player.log`, `UTC_Log`, app-data, live MTGA data, runtime status
files, failed posts, generated local artifacts, workbook exports, raw diffs,
source patches, secrets, credentials, tokens, API keys, webhook URLs, ARS run
artifacts, Refactor Scout artifacts, or private evidence were read, created,
imported, or modified.

## Owning Layer

Primary layer: Local Analytics Ingest / parser-produced fact persistence.

`src/mythic_edge_parser/app/analytics_ingest.py` owns the current mechanics for
turning approved parser-normalized replay payloads and live parser-owned fact
payloads into local analytics SQLite rows. The parser and state layer still
owns parser truth. Analytics ingest may normalize, validate, persist, count,
skip, and record provenance for parser-produced facts; it must not become the
truth owner for match facts, game facts, parser event classes, final
reconciliation, match identity, game identity, play/draw, mulligan counts,
opening hand, card actions, deck submission, workbook schema, webhook payload
shape, Apps Script behavior, AI analysis, or coaching interpretation.

## Internal Project Area

Local Analytics / parser-owned fact bridge.

The module sits downstream of parser-owned facts and upstream of local
analytics views, local app history, JSON ingest, manual import, and live
capture persistence. That bridge position makes decomposition higher risk than
a local advisory helper: a careless split could preserve import names while
changing row shape, upsert behavior, provenance, skip/warning counters, public
safety filtering, or local analytics consumer expectations.

## Truth Owner

- Parser/state and parser model surfaces own parser-managed facts and value
  meaning.
- `analytics_ingest.py` owns current ingest API behavior, replay/live payload
  normalization, deterministic ingest run IDs, local SQLite upserts, fact-family
  row handling, provenance writes, table counts, warnings, skips, and live
  public-safety rejection behavior.
- Analytics schema and migration files own table definitions and derived view
  shape. This contract does not change those files.
- Local app backend, import jobs, JSON ingest, dashboard/history helpers, and
  tests consume analytics ingest behavior. They do not gain authority to
  reinterpret parser truth.
- Repo governance docs, active issues, accepted ADRs, reviewed contracts, and
  human owner decisions remain authoritative for workflow routing.

## Bridge-Code Status

`bridge_code`

Source internal project area: Parser-produced fact payloads.

Consuming internal project area: Local Analytics and Local App.

Allowed data flow:

```text
parser-owned facts / approved replay summaries / live parser-owned fact payloads
  -> analytics ingest normalization and validation
  -> local analytics SQLite rows and provenance
  -> local analytics views, local app history, and dashboard consumers
```

Forbidden reverse flow:

```text
analytics storage, local app display, workbook/dashboard interpretation, or AI output
  -/-> parser truth
  -/-> parser event classes
  -/-> match or game identity
  -/-> final reconciliation
  -/-> workbook/webhook/Apps Script truth
```

## Files Owned By This Contract

- `docs/contracts/core_analytics_ingest_residual_decomposition_decision_packet.md`

Files referenced but not owned:

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_json_ingest.py`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/analytics_dashboard.py`
- `src/mythic_edge_parser/local_app/analytics_history.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_analytics_opponent_card_observation_ingest.py`
- `tests/test_analytics_field_evidence_ingest.py`
- `tests/test_live_app_parser_owned_fact_capture_sqlite.py`
- `tests/test_analytics_json_ingest_cli.py`
- `tests/test_analytics_replay_view_harness.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_select_validation.py`

## Authorization State

The following flags are false for this contract:

```yaml
implementation_authorized: false
file_move_authorized: false
same_repo_decomposition_authorized: false
cross_repo_extraction_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
source_mutation_authorized: false
private_log_inspection_authorized: false
private_evidence_inspection_authorized: false
parser_behavior_change_authorized: false
parser_truth_ownership_change_authorized: false
parser_event_class_change_authorized: false
match_identity_change_authorized: false
game_identity_change_authorized: false
final_reconciliation_change_authorized: false
sqlite_schema_change_authorized: false
sqlite_persisted_data_behavior_change_authorized: false
analytics_ingest_behavior_change_authorized: false
analytics_schema_change_authorized: false
analytics_view_change_authorized: false
provenance_semantics_change_authorized: false
warning_skip_semantics_change_authorized: false
public_safety_filter_change_authorized: false
api_behavior_change_authorized: false
frontend_behavior_change_authorized: false
live_capture_behavior_change_authorized: false
workbook_webhook_appsscript_behavior_change_authorized: false
ci_change_authorized: false
runtime_artifact_creation_authorized: false
readiness_claimed: false
reliability_readiness_claimed: false
parser_truth_claimed: false
analytics_truth_claimed: false
truth_or_assurance_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
release_readiness_claimed: false
deploy_readiness_claimed: false
production_readiness_claimed: false
```

Any future handoff, evidence packet, review, or implementation plan that flips
one of these flags without a separate reviewed issue and explicit owner
approval must fail closed.

## Codex E Schema And Vocabulary Reconciliation

This section resolves:

- `ANALYTICS-INGEST-DECOMP-E-001`

The original draft used the primary `candidate_surface_class` value
`parser_analytics_ingest_surface` before clearly binding that value to the
shared Phase 5 decision-packet vocabulary. That was ambiguous because the
shared #665 contract is scoped to governance/report/helper surfaces, while
`analytics_ingest.py` is parser-produced-fact persistence and local analytics
ingest bridge code.

Canonical correction:

- this packet is not a direct instance of the #665
  `core_governance_report_helper_phase_5_decomposition_decision_packet.v1`
  schema, because #665 requires `candidate_scope:
  governance_report_helper_only`;
- this packet is an issue #716 schema extension that reuses the shared Phase 5
  field names, false-authority flags, ARS/Refactor evidence status fields, and
  decision vocabulary where applicable;
- `parser_analytics_ingest_surface` is introduced only as an issue #716
  primary class by the extension section below;
- analytics-specific labels such as `sqlite_persistence_contact` and
  `provenance_contact` are secondary metadata only, not canonical Phase 5
  primary classes;
- a validator or future workflow role that understands only #665 must fail
  closed on this packet instead of silently coercing it into a
  governance/report/helper row.

## Phase 5 Packet Schema And Vocabulary Binding

Base vocabulary reused from #665:

- `final_decision` values:
  `same_repo_keep_current_path`, `same_repo_decomposition_candidate`,
  `request_fresh_ars_refactor_evidence`, `request_scope_split_child`,
  `reject_cross_repo_extraction`, `defer`, and `review_required`;
- ARS/Refactor evidence fields:
  `prior_ars_evidence_found`, `prior_refactor_scout_evidence_found`,
  `reviewed_repo`, `reviewed_scope`, `reviewed_commit`,
  `ars_version_contract_bundle`, `current_target_commit`,
  `relevant_changes_since_review`, `evidence_status`,
  `fresh_scoped_evidence_needed`, and `reason`;
- false-authority fields such as `implementation_authorized`,
  `file_move_authorized`, `ars_run_authorized`, `refactor_scout_run_authorized`,
  `source_mutation_authorized`, `readiness_claimed`, and
  `truth_or_assurance_claimed`.

Issue #716 extension:

```yaml
base_phase_5_packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
packet_schema: "core_analytics_ingest_residual_decomposition_decision_packet.v1"
schema_extension_owner: "docs/contracts/core_analytics_ingest_residual_decomposition_decision_packet.md"
schema_extension_scope: "issue_716_analytics_ingest_residual_only"
candidate_scope: "analytics_ingest_residual_only"
candidate_surface_class_source: "issue_716_extension"
```

The extension adds exactly one primary `candidate_surface_class` value:

- `parser_analytics_ingest_surface`: a parser-produced-fact persistence surface
  that normalizes approved payloads into local analytics storage without owning
  parser truth.

This value is allowed only when all of the following are true:

- `packet_schema` is
  `core_analytics_ingest_residual_decomposition_decision_packet.v1`;
- `schema_extension_scope` is `issue_716_analytics_ingest_residual_only`;
- `candidate_id` is `analytics-ingest`;
- `current_path` is `src/mythic_edge_parser/app/analytics_ingest.py`;
- `implementation_authorized`, `file_move_authorized`,
  `parser_behavior_change_authorized`,
  `parser_truth_ownership_change_authorized`,
  `sqlite_schema_change_authorized`,
  `analytics_ingest_behavior_change_authorized`, `readiness_claimed`,
  `parser_truth_claimed`, `analytics_truth_claimed`, and
  `truth_or_assurance_claimed` are all false.

This contract does not add `parser_analytics_ingest_surface` to the #665
governance/report/helper schema, any project-wide registry, or any later Phase
5 packet by implication.

## Decision Vocabulary

This contract defines the following issue #716 decision values:

- `same_repo_keep_current_path`: keep the module intact; no split.
- `same_repo_decomposition_candidate`: later same-repo decomposition may be
  considered after review, fresh evidence or owner exception, and validation.
- `request_fresh_ars_refactor_evidence`: fresh scoped ARS or Refactor Scout
  evidence is required before implementation routing.
- `request_owner_exception`: explicit owner acceptance may substitute for
  fresh evidence only if it names issue #716, target commit, candidate ID,
  allowed scope, and still keeps implementation/file movement unauthorized.
- `request_scope_split_child`: the candidate is too broad and must be split
  into a narrower decision issue.
- `reject_cross_repo_extraction`: cross-repo extraction is not justified.
- `defer`: leave the candidate in the residual queue.
- `review_required`: human or Codex E review must decide before routing.

Forbidden decisions:

- `implementation_approved`
- `file_move_approved`
- `same_repo_decomposition_authorized`
- `cross_repo_extraction_approved`
- `ars_clearance_granted`
- `refactor_scout_clearance_granted`
- `analytics_truth_confirmed`
- `parser_truth_confirmed`
- `ready_for_merge`
- `ready_for_release`
- `security_assured`
- `privacy_assured`

## Candidate Surface Vocabulary

Allowed issue #716 primary candidate surface class, introduced by the schema
extension above:

- `parser_analytics_ingest_surface`: a parser-produced-fact persistence surface
  that normalizes approved payloads into local analytics storage without owning
  parser truth.

Supporting metadata fields may use these non-authoritative labels:

- `sqlite_persistence_contact`
- `local_app_bridge_contact`
- `parser_truth_adjacent_contact`
- `public_safety_validation_contact`
- `provenance_contact`

Forbidden primary classes for this issue:

- `parser_truth_surface`
- `parser_state_surface`
- `eventbus_behavior_surface`
- `api_payload_surface`
- `frontend_behavior_surface`
- `live_capture_behavior_surface`
- `workbook_webhook_surface`
- `apps_script_surface`
- `ci_enforcement_surface`
- `private_evidence_surface`

If a later packet or implementation plan classifies `analytics-ingest` as a
forbidden primary class, it must route back to Codex A or Codex B for scope
repair before implementation.

## Packet Envelope

```yaml
base_phase_5_packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
packet_schema: "core_analytics_ingest_residual_decomposition_decision_packet.v1"
schema_extension_owner: "docs/contracts/core_analytics_ingest_residual_decomposition_decision_packet.md"
schema_extension_scope: "issue_716_analytics_ingest_residual_only"
repository: "Tahjali11/Mythic-Edge"
repository_url: "https://github.com/Tahjali11/Mythic-Edge"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/716"
tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
residual_queue: "https://github.com/Tahjali11/Mythic-Edge/issues/710"
residual_promotion_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/715"
source_contract: "docs/contracts/core_analytics_ingest_residual_decomposition_decision_packet.md"
target_commit: "9528bb3bee9c1d241268cb8a7d1a806b118471de"
candidate_scope: "analytics_ingest_residual_only"
candidate_id: "analytics-ingest"
candidate_surface_class_source: "issue_716_extension"
candidate_surface_class: "parser_analytics_ingest_surface"
candidate_surface_contacts:
  - "sqlite_persistence_contact"
  - "local_app_bridge_contact"
  - "parser_truth_adjacent_contact"
  - "public_safety_validation_contact"
  - "provenance_contact"
current_path: "src/mythic_edge_parser/app/analytics_ingest.py"
current_loc: 2375
loc_band: "1500_to_3000"
phase_5_blocker: false
final_decision: "request_fresh_ars_refactor_evidence"
same_repo_first: true
cross_repo_extraction_authorized: false
implementation_authorized: false
file_move_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
source_mutation_authorized: false
parser_behavior_change_authorized: false
parser_truth_ownership_change_authorized: false
sqlite_schema_change_authorized: false
analytics_ingest_behavior_change_authorized: false
ci_change_authorized: false
readiness_claimed: false
reliability_readiness_claimed: false
parser_truth_claimed: false
analytics_truth_claimed: false
truth_or_assurance_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
```

## Observed Current Behavior

The current file combines these responsibility groups:

- public constants for replay ingest and live parser-owned fact capture schema
  version labels;
- public error/result/input types:
  `AnalyticsReplayIngestError`, `ParserNormalizedReplayInput`, and
  `AnalyticsReplayIngestResult`;
- public normalization functions:
  `normalize_parser_normalized_replay()` and
  `normalize_live_parser_owned_facts()`;
- deterministic ingest run ID generation through
  `deterministic_ingest_run_id()`;
- public ingest entrypoints:
  `ingest_parser_normalized_replay()` and
  `ingest_live_parser_owned_facts()`;
- shared transaction and table-count orchestration in
  `_ingest_normalized_replay()`;
- match and game row persistence through `_ingest_match_log_rows()` and
  `_ingest_game_log_rows()`;
- gameplay action row normalization, card identity rows, and provenance;
- opponent card observation row normalization, row IDs, source relation checks,
  and provenance;
- field evidence row normalization, safe label validation, target fact checks,
  and provenance;
- opening hand and mulligan ingest helpers;
- ingest run and fact provenance upserts;
- shared SQLite upsert/core column helpers and table count helpers;
- public-safe live payload rejection helpers for forbidden fields, unsafe row
  payloads, private-looking values, missing final rows, warnings, and skip
  summaries.

The public entrypoints are imported by local app live capture, import jobs,
JSON ingest, legacy JSONL adapter tests, and focused analytics ingest tests.

## Responsibility Map

| Responsibility | Current owner | Future split candidate | Notes |
| --- | --- | --- | --- |
| Public entrypoints and compatibility facade | `analytics_ingest.py` | Keep in `analytics_ingest.py` | The current import path should remain stable for later same-repo work. |
| Replay/live payload normalization | `analytics_ingest.py` | `analytics_ingest_normalization.py` | Candidate only; must preserve result dataclasses and defaults. |
| Deterministic ingest run ID | `analytics_ingest.py` | Normalization or run metadata helper | Must preserve exact ID behavior for repeat ingest/upsert tests. |
| SQLite transaction/upsert/table counts | `analytics_ingest.py` | `analytics_ingest_sqlite_core.py` | Must not change schema, row shape, conflict behavior, or commit behavior. |
| Match and game row ingest | `analytics_ingest.py` | Fact-family helper | Must preserve parser-owned finality/value-source semantics. |
| Gameplay action ingest and card provenance | `analytics_ingest.py` | Fact-family helper | Must preserve card identity fallback and enrichment status behavior. |
| Opponent observation ingest | `analytics_ingest.py` | Fact-family helper | Must preserve observation IDs, relation checks, and numeric/card identity rules. |
| Field evidence ingest | `analytics_ingest.py` | Fact-family helper | Must preserve safe label validation and target fact requirements. |
| Opening hand and mulligan ingest | `analytics_ingest.py` | Fact-family helper | Must preserve current optional/deferred handling. |
| Provenance writes | `analytics_ingest.py` | `analytics_ingest_provenance.py` | Candidate only; provenance meaning and row shape cannot change. |
| Live public-safety filtering | `analytics_ingest.py` | `analytics_ingest_public_safety.py` | Candidate only; no-echo/private-value rejection must be preserved. |

## Decomposition Decision

This contract records `analytics-ingest` as a same-repo-first decomposition
candidate, but it does not authorize implementation or file movement.

Recommended future direction:

1. Keep `src/mythic_edge_parser/app/analytics_ingest.py` as the stable public
   facade for existing imports.
2. Consider private same-repo helper modules only after fresh scoped evidence
   or an explicit owner exception is recorded.
3. Split by behavior family, not by convenience:
   normalization, SQLite core/upsert helpers, provenance helpers, public-safety
   validation, and fact-family ingest helpers.
4. Do not create a new repository or move analytics ingest outside Mythic Edge.
   The boundary is parser-produced-fact-adjacent, local SQLite-adjacent, and
   not proven stable as an independent package.
5. Do not treat size alone as a blocker. The reason for later decomposition is
   mixed responsibility plus parser-truth-adjacent persistence risk.

## ARS And Refactor Evidence Status

```yaml
prior_ars_evidence_found: "no"
prior_refactor_scout_evidence_found: "no"
reviewed_repo: "Tahjali11/Mythic-Edge"
reviewed_scope: "src/mythic_edge_parser/app/analytics_ingest.py"
reviewed_commit: "none"
ars_version_contract_bundle: "none"
current_target_commit: "9528bb3bee9c1d241268cb8a7d1a806b118471de"
relevant_changes_since_review: "unknown"
evidence_status: "fresh_scoped_evidence_required_before_implementation"
fresh_scoped_evidence_needed: "yes"
reason: "The candidate is parser-truth-adjacent and local SQLite persistence-adjacent. Contract-only review can proceed, but implementation needs fresh scoped ARS or Refactor Scout evidence unless a later owner exception explicitly names this issue, target commit, candidate ID, and allowed scope."
```

Fresh evidence success is prerequisite evidence only. It must not be treated as
implementation authority, file-move authority, merge readiness, parser truth,
analytics truth, security assurance, privacy assurance, or production
readiness.

## Owner Exception Rule

A later owner exception may substitute for fresh scoped ARS/Refactor evidence
only if it is explicit, issue-scoped, and public-safe.

The exception must name:

- issue #716;
- candidate ID `analytics-ingest`;
- current path `src/mythic_edge_parser/app/analytics_ingest.py`;
- exact target commit or branch;
- whether the exception covers Codex C implementation planning only or a
  reviewed behavior-preserving implementation attempt;
- continued false flags for parser behavior changes, parser truth ownership
  changes, SQLite schema changes, analytics ingest behavior changes, API,
  frontend, live-capture, workbook, webhook, Apps Script, CI, readiness,
  truth, and assurance claims.

Ambiguous approval such as "approved", "run it", "decompose analytics", or
"continue" is not enough to override the fresh-evidence requirement.

## Public Interface Preservation

A later implementation must preserve these public imports and behaviors unless
a separate contract explicitly changes them:

- `ANALYTICS_REPLAY_INGEST_SCHEMA_VERSION`
- `LIVE_PARSER_OWNED_FACT_CAPTURE_SCHEMA_VERSION`
- `AnalyticsReplayIngestError`
- `ParserNormalizedReplayInput`
- `AnalyticsReplayIngestResult`
- `normalize_parser_normalized_replay()`
- `normalize_live_parser_owned_facts()`
- `deterministic_ingest_run_id()`
- `ingest_parser_normalized_replay()`
- `ingest_live_parser_owned_facts()`

Compatibility requirement: existing callers should continue importing from
`mythic_edge_parser.app.analytics_ingest`. New private helper modules, if later
authorized, should stay behind that facade unless a separate interface contract
approves a caller migration.

## Invariants

- Parser/state remains the truth owner for parser-managed facts.
- Analytics ingest remains a persistence and validation layer, not a truth
  correction layer.
- Replay ingest and live parser-owned fact ingest must preserve current row
  shape, upsert behavior, warnings, skips, table counts, and result fields.
- SQLite schema, migration files, table names, primary keys, and derived view
  shape must not change under this contract.
- Provenance rows must continue to describe source, value-source, and
  fact-family context without echoing private log content or local paths.
- Live payload public-safety filters must continue to fail closed on forbidden
  fields, private-looking values, and unsafe row payloads.
- Existing tests and validation selector behavior must continue to identify
  analytics ingest focused checks.
- Cross-repo extraction remains rejected unless a later contract proves a
  stable, independently testable, separately governed interface.

## Error Behavior

Contract ambiguity, stale evidence, missing owner authority, unknown decision
vocabulary, unknown candidate class, contradicted false-authority flags, or
implementation language inside a no-implementation handoff must fail closed and
route back to Codex B or Codex E.

A later implementation must preserve current runtime error behavior for
malformed replay payloads, malformed live payloads, missing required labels,
invalid enum values, unsafe live row fields, unsafe private-looking row values,
missing referenced fact rows, and duplicate/upsert cases. This contract does
not define new runtime errors.

## Behavior-Preservation Validation Required Later

A later Codex C implementation, if separately authorized, must run at minimum:

```bash
python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py
python3 -m pytest -q tests/test_live_app_parser_owned_fact_capture_sqlite.py tests/test_analytics_json_ingest_cli.py tests/test_analytics_replay_view_harness.py tests/test_analytics_local_app_backend.py
python3 -m pytest -q tests/test_select_validation.py -k analytics_ingest
git diff --check
```

Broader validation may be required if the implementation touches imports,
local-app callers, JSON ingest, analytics views, migration loader behavior,
frontend/API/live-capture boundaries, or shared parser-owned fact vocabulary.

## Acceptance Criteria

- The decision packet uses issue #716, candidate ID `analytics-ingest`, target
  commit `9528bb3bee9c1d241268cb8a7d1a806b118471de`, and target artifact
  exactly.
- The packet names #665 as the base Phase 5 vocabulary source and names
  `core_analytics_ingest_residual_decomposition_decision_packet.v1` as an
  issue #716 extension before using `parser_analytics_ingest_surface`.
- The packet treats analytics-specific contact labels as secondary metadata,
  not primary Phase 5 class vocabulary.
- The packet records `phase_5_blocker: false`.
- The packet names parser truth ownership and analytics ingest's downstream
  persistence role.
- The packet identifies same-repo-first split candidates without authorizing
  implementation or file movement.
- The packet requires fresh scoped ARS/Refactor evidence before implementation
  unless a later exact owner exception is recorded.
- The packet preserves public imports, SQLite row/upsert/provenance semantics,
  public-safety validation, and local analytics consumers.
- The packet rejects cross-repo extraction and any readiness/truth/assurance
  claims.

## Remaining Risks

- No current ARS or Refactor Scout evidence was reviewed for this exact
  candidate and target commit.
- The current responsibility map is structural, not a behavioral proof.
- Focused tests exist, but this contract did not run runtime tests because no
  code changed.
- Later implementation must be careful not to change private helper ordering,
  transaction boundaries, deterministic IDs, or warning/skip aggregation while
  moving code.

## Recommended Next Role

Codex E: review this contract against issue #716, issue #715, issue #710, the
repo governance rules, and the current analytics ingest public interface.

If Codex E finds no blockers, route to an evidence-authority lane or Codex A
to frame fresh scoped ARS/Refactor evidence for `analytics-ingest`. Do not route
directly to Codex C unless a later owner exception explicitly substitutes for
fresh evidence and still preserves the no-behavior-change boundary.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Contract Reviewer for Mythic-Edge issue #716.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/716

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Residual queue:
https://github.com/Tahjali11/Mythic-Edge/issues/710

Residual promotion issue:
https://github.com/Tahjali11/Mythic-Edge/issues/715

Target artifact:
docs/contracts/core_analytics_ingest_residual_decomposition_decision_packet.md

Goal:
Review the contract-only analytics-ingest residual decomposition decision packet. Verify that it preserves parser truth ownership, local analytics ingest behavior, SQLite/provenance/public-safety boundaries, same-repo-first routing, fresh-evidence requirements, false-authority flags, and non-claims.

Protected boundaries:
Do not implement code, move files, open a PR, run ARS, run Refactor Scout, inspect private logs, change parser behavior, change parser truth ownership, change SQLite schema or persisted-data behavior, change analytics ingest behavior, change API/frontend/live-capture behavior, change workbook/webhook/Apps Script behavior, change CI, or claim readiness/security/privacy/parser truth/analytics truth.

Expected output:
Findings first. If blockers exist, route back to Codex B with finding IDs and exact contract sections to fix. If no blockers exist, recommend the next evidence-authority or owner-exception lane before any Codex C implementation.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/716"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  residual_queue: "https://github.com/Tahjali11/Mythic-Edge/issues/710"
  residual_promotion_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/715"
  completed_thread: "B"
  next_thread: "E"
  verdict: "analytics_ingest_residual_decomposition_decision_packet_ready_for_contract_review"
  risk_tier: "High"
  target_commit: "9528bb3bee9c1d241268cb8a7d1a806b118471de"
  target_artifact: "docs/contracts/core_analytics_ingest_residual_decomposition_decision_packet.md"
  candidate_id: "analytics-ingest"
  candidate_surface: "src/mythic_edge_parser/app/analytics_ingest.py"
  base_phase_5_packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
  packet_schema: "core_analytics_ingest_residual_decomposition_decision_packet.v1"
  schema_extension_scope: "issue_716_analytics_ingest_residual_only"
  candidate_scope: "analytics_ingest_residual_only"
  candidate_surface_class_source: "issue_716_extension"
  candidate_surface_class: "parser_analytics_ingest_surface"
  phase_5_blocker: false
  final_decision: "request_fresh_ars_refactor_evidence"
  fresh_scoped_evidence_needed_before_implementation: true
  same_repo_first: true
  implementation_authorized: false
  file_move_authorized: false
  same_repo_decomposition_authorized: false
  cross_repo_extraction_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  private_log_inspection_authorized: false
  source_mutation_authorized: false
  parser_behavior_change_authorized: false
  parser_truth_ownership_change_authorized: false
  sqlite_schema_change_authorized: false
  analytics_ingest_behavior_change_authorized: false
  api_behavior_change_authorized: false
  frontend_behavior_change_authorized: false
  live_capture_behavior_change_authorized: false
  workbook_webhook_appsscript_behavior_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  parser_truth_claimed: false
  analytics_truth_claimed: false
```
