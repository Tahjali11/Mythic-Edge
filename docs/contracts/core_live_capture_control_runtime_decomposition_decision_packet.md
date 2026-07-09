# Core Live-Capture Control Runtime Decomposition Decision Packet

Status: Draft contract for review

Role: Codex B - Module Contract Writer / Decomposition Decision Packet

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/719>

Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>

Residual promotion queue: <https://github.com/Tahjali11/Mythic-Edge/issues/715>

Evidence source: <https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161>

Target artifact:
`docs/contracts/core_live_capture_control_runtime_decomposition_decision_packet.md`

## Module

`core_live_capture_control_runtime_decomposition_decision_packet`

This contract is the Phase 5 decomposition decision packet for the live-capture
control runtime surface.

Plain English: `src/mythic_edge_parser/local_app/live_capture_control.py`
currently owns the local app's explicit start/stop capture behavior, status
payload construction, app-owned supervisor lifecycle, live parser event stream
loop, local SQLite fact writes, state-file updates, MTGA process lifecycle
checks, and public-safe diagnostics. This packet decides the smallest safe
same-repo decomposition shape. It does not implement that split.

This contract is planning-only. It does not implement code, move files, open a
PR, run ARS, run Refactor Scout, read private logs or raw `Player.log` files,
change live-capture runtime behavior, change frontend behavior, change API
payloads, change parser behavior, change parser truth ownership, change
EventBus behavior, change workbook/webhook/Apps Script behavior, change CI, or
claim readiness, reliability readiness, parser truth, security assurance, or
privacy assurance.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: <https://github.com/Tahjali11/Mythic-Edge>
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/719>
- Project roadmap / tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Broad decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>
- Residual promotion queue: <https://github.com/Tahjali11/Mythic-Edge/issues/715>
- Residual review pass: <https://github.com/Tahjali11/Mythic-Edge/issues/712>
- Residual queue: <https://github.com/Tahjali11/Mythic-Edge/issues/710>
- Evidence source issue:
  <https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161>
- Evidence source PR:
  <https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/pull/163>
- Evidence source merge commit:
  `a812321ea309aa7c3da8f726134c4783972bf484`
- Target commit:
  `9528bb3bee9c1d241268cb8a7d1a806b118471de`
- Current reviewed base:
  `origin/main` at `3710b449e685e2eb31d1927c2763334ed553cc60`

## Source Artifacts Inspected

- GitHub issue #719
- GitHub issue #568
- GitHub issue #463
- GitHub issue #715
- GitHub issue #161 and PR #163 in
  `Tahjali11/Mythic-Edge-Automation-Artifacts`
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
- `docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`
- `docs/contracts/core_event_bus_support_decomposition_decision_packet.md`
- `docs/contracts/core_analytics_ingest_residual_decomposition_decision_packet.md`
- `docs/contracts/core_frontend_app_shell_live_capture_controls_decomposition_decision_packet.md`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `tests/test_live_app_explicit_start_capture_control.py`
- `tests/test_live_app_mtga_process_lifecycle.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_live_app_parser_owned_fact_capture_sqlite.py`

No private `Player.log`, `UTC_Log`, app-data, live MTGA data, runtime status
files, failed posts, generated local artifacts, workbook exports, raw diffs,
source patches, secrets, credentials, tokens, API keys, webhook URLs, ARS run
artifacts, Refactor Scout artifacts, or private evidence were read, created,
imported, or modified.

## Owning Layer

Primary layer: Local App live-capture runtime bridge.

`src/mythic_edge_parser/local_app/live_capture_control.py` owns the local app
runtime control bridge between explicit operator controls, app-owned
live-capture supervisor state, parser-produced facts, and local analytics
SQLite writes. It does not own parser truth, frontend display truth, workbook
schema, webhook payload shape, Apps Script behavior, EventBus behavior, AI
analysis, coaching interpretation, release readiness, deploy readiness, or
production readiness.

## Internal Project Area

Local App / live-capture runtime support, with parser-state and local analytics
contacts.

The module is bridge code because it connects:

```text
explicit local app operator control
  -> app-owned supervisor lifecycle and state file
  -> parser event stream and parser-owned fact builders
  -> local analytics SQLite ingest
  -> frontend-visible status/start/stop payloads
```

Forbidden reverse flow:

```text
frontend labels, local status files, SQLite write results, heartbeat summaries,
or dashboard/control state
  -/-> parser truth
  -/-> parser event classes
  -/-> match or game identity
  -/-> final reconciliation
  -/-> EventBus behavior
  -/-> workbook/webhook/Apps Script truth
```

## Truth Owner

- Parser/state code owns parser facts, match identity, game identity, event
  interpretation, and final reconciliation.
- `live_capture_control.py` owns current local live-capture runtime control
  behavior, app-owned supervisor registry, state-file schema and sanitization,
  explicit start/stop/status result construction, heartbeat/progress/lifecycle
  diagnostics, and the bridge call into local analytics ingest.
- `backend.py` owns route binding for `/api/live/capture/status`,
  `/api/live/capture/start`, and `/api/live/capture/stop`.
- `frontend/src/api.ts` and `frontend/src/types.ts` own frontend validation and
  TypeScript payload shapes; they are referenced but not changed by this
  contract.
- `analytics_ingest.py` owns local SQLite ingest semantics for live
  parser-owned facts.
- Repo governance docs, accepted ADRs, active issues, reviewed contracts, and
  human owner decisions own workflow routing.

## Bridge-Code Status

`bridge_code`

This is not pure parser truth code and not pure frontend code. It is a
protected bridge between local app control, parser runtime facts, app-local
state, and local analytics persistence. That bridge status makes broad
decomposition risky: a careless split could preserve imports while changing
operator stop behavior, stale-state handling, no-echo sanitization, heartbeat
labels, SQLite live-write attempts, MTGA reconnect handling, or frontend API
payload semantics.

## Files Owned By This Contract

- `docs/contracts/core_live_capture_control_runtime_decomposition_decision_packet.md`

Files referenced but not owned:

- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/mtga_process_lifecycle.py`
- `src/mythic_edge_parser/local_app/setup_status.py`
- `src/mythic_edge_parser/local_app/paths.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/stream.py`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/src/app_live_capture_controls.tsx`
- `tests/test_live_app_explicit_start_capture_control.py`
- `tests/test_live_app_mtga_process_lifecycle.py`
- `tests/test_analytics_local_app_backend.py`
- `tests/test_live_app_parser_owned_fact_capture_sqlite.py`

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
private_log_read_authorized: false
raw_player_log_read_authorized: false
private_evidence_inspection_authorized: false
runtime_artifact_creation_authorized: false
live_capture_behavior_change_authorized: false
live_capture_state_schema_change_authorized: false
live_capture_start_stop_change_authorized: false
live_capture_payload_shape_change_authorized: false
supervisor_lifecycle_change_authorized: false
event_stream_behavior_change_authorized: false
sqlite_live_write_behavior_change_authorized: false
mtga_process_lifecycle_behavior_change_authorized: false
frontend_behavior_change_authorized: false
api_payload_change_authorized: false
backend_route_change_authorized: false
parser_behavior_change_authorized: false
parser_truth_ownership_change_authorized: false
parser_event_class_change_authorized: false
match_identity_change_authorized: false
game_identity_change_authorized: false
deduplication_change_authorized: false
final_reconciliation_change_authorized: false
eventbus_behavior_change_authorized: false
workbook_schema_change_authorized: false
webhook_payload_change_authorized: false
apps_script_change_authorized: false
ci_change_authorized: false
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

## Phase 5 Packet Schema And Vocabulary Binding

This packet reuses the #665 Phase 5 decision-packet field names,
false-authority flags, ARS/Refactor evidence fields, and decision vocabulary
where applicable. It is not a direct `governance_report_helper_only` packet
because the candidate is live-capture runtime bridge code.

Canonical binding:

```yaml
base_phase_5_packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
packet_schema: "core_live_capture_control_runtime_decomposition_decision_packet.v1"
schema_extension_owner: "docs/contracts/core_live_capture_control_runtime_decomposition_decision_packet.md"
schema_extension_scope: "issue_719_live_capture_control_runtime_only"
candidate_scope: "live_capture_control_runtime_only"
candidate_surface_class_source: "issue_719_extension"
```

Issue #719 adds exactly one primary `candidate_surface_class` value:

- `live_capture_runtime_bridge_surface`: a same-repo local app runtime bridge
  surface that owns explicit live-capture control and diagnostics while
  consuming parser-owned facts without becoming parser truth.

This value is allowed only when all of the following are true:

- `packet_schema` is
  `core_live_capture_control_runtime_decomposition_decision_packet.v1`;
- `schema_extension_scope` is `issue_719_live_capture_control_runtime_only`;
- `candidate_id` is `live-capture-control-runtime`;
- `current_path` is
  `src/mythic_edge_parser/local_app/live_capture_control.py`;
- all authorization and claim flags in this contract remain false.

Supporting metadata fields may use these non-authoritative labels:

- `live_capture_status_payload_contact`
- `app_owned_supervisor_contact`
- `state_file_sanitization_contact`
- `parser_truth_adjacent_contact`
- `local_analytics_ingest_contact`
- `mtga_process_lifecycle_contact`
- `frontend_api_payload_contact`

Forbidden primary classes for this issue:

- `parser_truth_surface`
- `parser_state_surface`
- `eventbus_behavior_surface`
- `api_payload_surface`
- `frontend_behavior_surface`
- `workbook_webhook_surface`
- `apps_script_surface`
- `ci_enforcement_surface`
- `private_evidence_surface`

If a future packet or implementation plan classifies this candidate as a
forbidden primary class, it must route back to Codex A or Codex B before
implementation.

Allowed `final_decision` values for this packet are:

- `same_repo_keep_current_path`
- `same_repo_decomposition_candidate`
- `request_fresh_ars_refactor_evidence`
- `request_owner_exception`
- `request_scope_split_child`
- `reject_cross_repo_extraction`
- `defer`
- `review_required`

Forbidden decisions:

- `implementation_approved`
- `file_move_approved`
- `same_repo_decomposition_authorized`
- `cross_repo_extraction_approved`
- `ars_clearance_granted`
- `refactor_scout_clearance_granted`
- `live_capture_behavior_confirmed`
- `parser_truth_confirmed`
- `ready_for_merge`
- `ready_for_release`
- `security_assured`
- `privacy_assured`

## Packet Envelope

```yaml
base_phase_5_packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
packet_schema: "core_live_capture_control_runtime_decomposition_decision_packet.v1"
schema_extension_owner: "docs/contracts/core_live_capture_control_runtime_decomposition_decision_packet.md"
schema_extension_scope: "issue_719_live_capture_control_runtime_only"
repository: "Tahjali11/Mythic-Edge"
repository_url: "https://github.com/Tahjali11/Mythic-Edge"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/719"
tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
residual_promotion_queue: "https://github.com/Tahjali11/Mythic-Edge/issues/715"
evidence_source_issue: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161"
evidence_source_pr: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/pull/163"
evidence_source_merge_commit: "a812321ea309aa7c3da8f726134c4783972bf484"
target_commit: "9528bb3bee9c1d241268cb8a7d1a806b118471de"
current_origin_main: "3710b449e685e2eb31d1927c2763334ed553cc60"
candidate_scope: "live_capture_control_runtime_only"
candidate_id: "live-capture-control-runtime"
candidate_surface_class_source: "issue_719_extension"
candidate_surface_class: "live_capture_runtime_bridge_surface"
candidate_surface_contacts:
  - "live_capture_status_payload_contact"
  - "app_owned_supervisor_contact"
  - "state_file_sanitization_contact"
  - "parser_truth_adjacent_contact"
  - "local_analytics_ingest_contact"
  - "mtga_process_lifecycle_contact"
  - "frontend_api_payload_contact"
current_path: "src/mythic_edge_parser/local_app/live_capture_control.py"
current_loc: 1813
loc_band: "1500_to_3000"
phase_5_blocker: false
final_decision: "same_repo_decomposition_candidate"
same_repo_first: true
recommended_first_slice: "extract_pure_status_state_payload_helpers"
implementation_authorized: false
file_move_authorized: false
same_repo_decomposition_authorized: false
cross_repo_extraction_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
private_log_read_authorized: false
raw_player_log_read_authorized: false
source_mutation_authorized: false
live_capture_behavior_change_authorized: false
frontend_behavior_change_authorized: false
api_payload_change_authorized: false
parser_behavior_change_authorized: false
eventbus_behavior_change_authorized: false
ci_change_authorized: false
readiness_claimed: false
reliability_readiness_claimed: false
parser_truth_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
truth_or_assurance_claimed: false
```

## Observed Current Behavior

`src/mythic_edge_parser/local_app/live_capture_control.py` currently combines
these responsibility groups:

- public live-capture object names, schema versions, state file name, lock file
  name, stale thresholds, heartbeat thresholds, supervisor kind, and source
  kind;
- explicit public entrypoints:
  `build_live_capture_status(paths)`, `start_live_capture(paths)`, and
  `stop_live_capture(paths)`;
- process-local supervisor registry guarded by `_REGISTRY_LOCK` and
  `_SUPERVISORS`;
- `LocalAppLiveCaptureSupervisor`, which owns a daemon thread, stop event,
  async event-stream loop, parser runtime reset, parser event processing,
  completed match/game row detection, local SQLite live writes, and MTGA
  process lifecycle ticks;
- app-data state-file reads and writes for `live_capture_state.json` and
  `live_capture_lock.json`;
- status, start-result, and stop-result payload construction for backend and
  frontend consumers;
- public-safe heartbeat, progress, parser status blurb, MTGA lifecycle,
  warning/error, and last-result sanitizers;
- player-log readiness, analytics database readiness, and start precondition
  evaluation;
- configured Player.log path lookup from local app config;
- live fact persistence through `ingest_live_parser_owned_facts`.

`backend.py` imports only the three public entrypoints and binds them to the
local app live capture routes. Current tests cover the explicit start/stop
control boundary, no-echo sanitization, stale state behavior, supervisor
ownership checks, MTGA process lifecycle transitions, live SQLite fact writes,
and route behavior.

## Problem Statement And First Bad Values

The intended workflow is:

1. use this packet to decide whether the live-capture control runtime can be
   decomposed safely;
2. preserve current public entrypoints and backend route behavior;
3. keep parser truth ownership in parser/state code;
4. keep the first implementation slice small enough to review as a
   behavior-preserving move;
5. require Codex E review and explicit later owner routing before Codex C.

The first bad value is treating this contract as implementation authority.

The second bad value is changing live-capture runtime behavior while calling
the change decomposition.

The third bad value is extracting the supervisor loop before the pure
status/state helper boundary is stable and tested.

The fourth bad value is changing frontend-visible payload shape, schema
versions, status strings, warning/error codes, heartbeat/progress fields,
precondition keys, or no-echo redaction behavior during a decomposition.

The fifth bad value is letting local status files, SQLite ingest results,
dashboard labels, or AI/analytics interpretation become parser truth.

The sixth bad value is treating #161 evidence as ARS clearance, implementation
approval, readiness, security assurance, privacy assurance, or parser-truth
proof.

## Public Interface To Preserve

This contract does not change the live-capture control public interface. A
later behavior-preserving implementation must preserve at least:

- module import path:
  `mythic_edge_parser.local_app.live_capture_control`;
- public constants:
  `LIVE_CAPTURE_STATUS_OBJECT`, `LIVE_CAPTURE_START_RESULT_OBJECT`,
  `LIVE_CAPTURE_STOP_RESULT_OBJECT`, `LIVE_CAPTURE_SCHEMA_VERSION`,
  `LIVE_CAPTURE_DIAGNOSTICS_SCHEMA_VERSION`, `LIVE_CAPTURE_STATE_FILENAME`,
  `LIVE_CAPTURE_LOCK_FILENAME`, `LIVE_CAPTURE_SOURCE_KIND`, and
  `LIVE_CAPTURE_SUPERVISOR_KIND`;
- public function `build_live_capture_status(paths: LocalAppPaths)`;
- public function `start_live_capture(paths: LocalAppPaths)`;
- public function `stop_live_capture(paths: LocalAppPaths)`;
- public class `LocalAppLiveCaptureSupervisor`;
- public route behavior in `backend.py`;
- returned object names, schema versions, status values, accepted flags,
  `capture_status` nesting, `capture`, `preconditions`, `state`,
  `last_result`, `heartbeat`, `progress`, `mtga_lifecycle`,
  `parser_status_blurb`, `warnings`, and `errors` fields;
- current no-echo behavior for unsafe state warning/error/result text,
  timestamps, labels, local paths, and private-looking values;
- explicit configured Player.log requirement for capture start;
- external transport disabled and raw Player.log storage disabled flags;
- current app-owned supervisor ownership and stale-state behavior.

Any proposed change to these items is outside this decision packet and must
route back to Codex B.

## Decomposition Decision

Decision: `same_repo_decomposition_candidate`

Same-repo decomposition is appropriate for later consideration because the
module mixes pure payload/state helpers with runtime supervisor behavior and
parser/SQLite bridge behavior. Cross-repo extraction is rejected. This surface
is too tightly coupled to the local app backend, parser runtime state,
configured local paths, app-owned state files, EventBus stream consumption, and
focused tests to become a separately governed package.

Keeping the current file is also acceptable if a later implementer cannot
prove behavior preservation. Size alone is not a Phase 5 blocker.

## Recommended First Implementation Slice

If Codex E accepts this contract and the owner later authorizes Codex C, the
first implementation slice should be:

`extract_pure_status_state_payload_helpers`

The slice should keep `live_capture_control.py` as the stable public facade and
move only pure or nearly pure helper clusters behind it. Good first candidates
are:

- heartbeat/progress defaulting and sanitization helpers;
- safe label, warning/error, last-result, integer-map, timestamp, and duration
  helpers;
- status/start/stop payload construction helpers;
- MTGA lifecycle payload derivation helpers that do not perform process checks
  or mutate state;
- precondition row construction helpers that do not perform writes.

The first slice must not move:

- `build_live_capture_status()`;
- `start_live_capture()`;
- `stop_live_capture()`;
- `_REGISTRY_LOCK` or `_SUPERVISORS`;
- `LocalAppLiveCaptureSupervisor` thread/async lifecycle;
- `_run_async()` event stream loop;
- `_tick_mtga_lifecycle()` stop-event behavior;
- parser calls such as `_update_match_summary()`,
  `build_match_log_row()`, `build_game_summary_rows()`,
  `get_context_snapshot()`, or `reset_runtime_state()`;
- SQLite live write behavior;
- configured Player.log path reads;
- app-data state-file read/write behavior;
- backend route binding or frontend payload validators.

The reason for starting with pure helpers is reviewability: a move-only helper
slice can be checked by focused tests without changing process lifecycle,
event streaming, parser fact generation, or local SQLite writes.

## Candidate Row

| Field | Value |
| --- | --- |
| `candidate_id` | `live-capture-control-runtime` |
| `candidate_surface_class` | `live_capture_runtime_bridge_surface` |
| `current_path` | `src/mythic_edge_parser/local_app/live_capture_control.py` |
| `current_behavior` | Explicit local live-capture status/start/stop control, app-owned supervisor lifecycle, state-file sanitization, heartbeat/progress diagnostics, MTGA process lifecycle checks, parser event-stream processing, and live SQLite parser-owned fact writes |
| `truth_or_authority_owner` | Live-capture control owns local app runtime control mechanics only; parser/state remains parser truth owner; repo issues/contracts/human owner decisions own workflow authority |
| `upstream_dependencies` | `LocalAppPaths`, local app config, configured Player.log path, `MtgaEventStream`, parser state helpers, analytics ingest helper, MTGA process lifecycle helper, setup status helper, current backend route binding |
| `downstream_consumers` | `backend.py` live-capture routes, frontend API validators, frontend live-capture controls, focused Python tests, local analytics SQLite consumers |
| `protected_surface_contact` | `mixed_review_required`; this packet reads source and tests as reference only and does not mutate runtime behavior |
| `proposed_destination` | Same repository, stable public facade at `src/mythic_edge_parser/local_app/live_capture_control.py`, optional private same-repo helper modules only after explicit implementation authorization |
| `why_not_keep_local` | Keeping local remains valid, but the current file mixes public facade, status payload, sanitization, supervisor runtime, parser event processing, MTGA lifecycle, and SQLite bridge behavior. A first pure-helper split may reduce review burden. |
| `why_not_move_to_existing_repo` | Adjacent repos do not own local app runtime control behavior, parser-state contacts, or local SQLite live writes. |
| `why_not_create_new_repo` | A new repo would add version skew around protected local runtime behavior and parser-truth-adjacent bridge code. |
| `new_public_interface_needed` | `private_same_repo` |
| `new_public_interface_description` | Public import paths and backend route payloads remain unchanged; any extracted helper should be private same-repo support imported by the facade. |
| `behavior_preservation_tests` | Focused live-capture control tests, MTGA process lifecycle tests, backend route tests, live SQLite capture tests, import checks, no-echo checks, and before/after payload comparison for synthetic public-safe states |
| `rollback_plan` | Revert the implementation commit; restore helper functions to `live_capture_control.py`; remove any private helper module; do not migrate data, rewrite state files, change payload shapes, change parser/EventBus/backend/frontend behavior, or alter CI. |
| `ars_refactor_evidence_status` | `current_matching_scope`; #161 observed no-write scoped evidence at the target commit and current path metadata shows no target path changes through `origin/main`. |
| `non_claims` | No implementation approval, file-move approval, live-capture behavior approval, parser truth, readiness, reliability readiness, release readiness, deploy readiness, production readiness, security assurance, privacy assurance, ARS clearance, or Refactor Scout clearance |
| `final_decision` | `same_repo_decomposition_candidate` |

## Evidence Status

The #161 evidence source is accepted as scoped decomposition planning evidence
for this contract, not as implementation authority.

```yaml
prior_ars_evidence_found: "yes"
prior_refactor_scout_evidence_found: "yes"
reviewed_repo: "Tahjali11/Mythic-Edge"
reviewed_scope: "src/mythic_edge_parser/local_app/live_capture_control.py"
reviewed_commit: "9528bb3bee9c1d241268cb8a7d1a806b118471de"
ars_version_contract_bundle: "residual_phase_5_batch1_exact_scoped_evidence_execution_authority_contract.v1"
current_target_commit: "9528bb3bee9c1d241268cb8a7d1a806b118471de"
current_origin_main: "3710b449e685e2eb31d1927c2763334ed553cc60"
relevant_changes_since_review: "none_known"
evidence_status: "current_matching_scope"
fresh_scoped_evidence_needed: "no"
reason: "Issue #161 recorded no-write scoped evidence observed for live-capture-control-runtime at the target commit. Issue #719 records that target commit is an ancestor of current origin/main and no Batch 1 target paths changed between target commit and origin/main. A local quiet path check for this file also reported unchanged. This evidence informs planning only and does not authorize implementation."
```

Evidence constraints:

- source file content read was reviewed as authorized only for the #161
  evidence action;
- this Codex B packet did not run ARS or Refactor Scout;
- this Codex B packet did not read raw diffs;
- this Codex B packet did not read private logs, raw Player.log files, private
  evidence, runtime app-data, secrets, or local-only artifacts;
- evidence success remains prerequisite evidence only.

Fresh scoped ARS or Refactor Scout evidence is not required before Codex E
reviews this contract. A later Codex C implementation may proceed only after
Codex E review and explicit owner authorization. If the target path changes
before Codex C starts, the implementation route must stop and either refresh
path-level evidence or return to Codex B.

## Same-Repo Module Boundaries

A later implementation may split internal code only if these boundaries
preserve behavior exactly:

- Public facade:
  `live_capture_control.py` remains the import path for public constants,
  `build_live_capture_status()`, `start_live_capture()`,
  `stop_live_capture()`, and `LocalAppLiveCaptureSupervisor`.
- Payload/status helper layer:
  safe private helper extraction may preserve `_status_payload()`,
  `_start_result()`, `_stop_result()`, `_capture_summary()`,
  `_safe_state_summary()`, heartbeat/progress helpers, safe-label helpers,
  parser blurb helpers, and MTGA lifecycle payload helpers behind the facade.
- Runtime supervisor layer:
  thread start/stop behavior, daemon name, stop-event semantics,
  `_run_thread()`, `_run_async()`, event-stream loop timing, parser runtime
  reset, match/game row detection, and stream shutdown behavior remain in the
  original facade for the first slice.
- State-file layer:
  `live_capture_state.json` and `live_capture_lock.json` filenames,
  write timing, field names, safe payload construction, display path behavior,
  stale-state behavior, raw path suppression, and lock token behavior remain
  unchanged.
- Preconditions layer:
  configured Player.log requirement, app-data availability, state directory
  handling, analytics database availability, external transport disabled, and
  frontend-controls authorization semantics remain unchanged.
- Parser truth layer:
  parser calls and parser-owned result semantics remain unchanged.
- Local analytics layer:
  live SQLite ingest call shape, source labels, row counting, warnings,
  skipped counts, and write-failure behavior remain unchanged.
- MTGA process lifecycle layer:
  reconnect window behavior, timeout shutdown behavior, shutdown reason,
  warnings, `automation_start_allowed: false`, and automation readiness payload
  remain unchanged.
- Frontend/API layer:
  backend route paths, HTTP method behavior, object names, schema version,
  payload shape, safe labels, and frontend validators remain unchanged.

Candidate helper module names are intentionally not fixed. A future Codex C
should inspect imports and choose names that make ownership obvious, such as a
private status/payload helper module, without adding public API commitments.

## Stop Conditions For Later Implementation

Codex C must stop and route back to Codex B or Codex A if any later
implementation requires:

- changing public constants, public function names, public class names, or
  backend route bindings;
- changing frontend-visible payload field names, status strings, schema
  versions, warning/error codes, or no-echo behavior;
- moving `LocalAppLiveCaptureSupervisor` or the async event loop in the first
  slice;
- changing parser event processing, parser state reset, match/game row
  detection, or local SQLite write behavior;
- changing MTGA process reconnect or shutdown behavior;
- reading private logs, raw Player.log files, raw diffs, secrets, runtime
  app-data, or private evidence;
- adding external dependencies;
- changing CI;
- creating runtime artifacts outside existing test temp directories;
- claiming readiness, parser truth, reliability readiness, security assurance,
  privacy assurance, release readiness, deploy readiness, or production
  readiness.

## Validation Plan For Later Implementation

Minimum validation for a later approved first slice:

```bash
git diff --check
python3 -m py_compile src/mythic_edge_parser/local_app/live_capture_control.py
python3 -m pytest -q tests/test_live_app_explicit_start_capture_control.py
python3 -m pytest -q tests/test_live_app_mtga_process_lifecycle.py
python3 -m pytest -q tests/test_analytics_local_app_backend.py
python3 -m pytest -q tests/test_live_app_parser_owned_fact_capture_sqlite.py
```

Additional checks when feasible:

```bash
python3 -m ruff check src/mythic_edge_parser/local_app tests/test_live_app_explicit_start_capture_control.py tests/test_live_app_mtga_process_lifecycle.py
python3 -m pytest -q
```

Behavior-preservation expectations:

- compare before/after synthetic status payloads for ready, blocked, starting,
  capturing, stale, failed, stopped, reconnect-window, and timeout-shutdown
  states;
- verify unsafe state labels, timestamps, warnings, errors, and last-result
  values still redact or fail closed without echoing unsafe text;
- verify start remains explicit local-only and duplicate safe;
- verify stop still requires app-owned supervisor token match;
- verify configured Player.log is still required to start capture;
- verify MTGA disappearance/reconnect/timeout behavior remains unchanged;
- verify backend route tests still consume the same payload shape;
- verify live SQLite write tests still prove final parser-owned facts only.

Validation must not:

- run ARS or Refactor Scout;
- read private logs or raw Player.log files;
- read raw diffs as validation evidence;
- collect live MTGA data;
- create durable runtime artifacts outside normal test temp paths;
- change CI;
- claim readiness, parser truth, reliability readiness, security assurance, or
  privacy assurance.

## Rollback Expectations

Later behavior-preserving implementation must be rollback-safe:

- keep existing public entrypoints in `live_capture_control.py`;
- avoid data migrations and state-file format migrations;
- avoid new external dependencies;
- avoid cross-repo version coupling;
- keep backend/frontend payload format stable;
- make rollback possible through reverting the implementation commit and
  removing any private helper module introduced by the implementation.

## Acceptance Criteria For This Contract

- The artifact exists at
  `docs/contracts/core_live_capture_control_runtime_decomposition_decision_packet.md`.
- The packet names issue #719, roadmap #568, decomposition tracker #463, and
  evidence source #161.
- The packet preserves the #161 evidence as planning evidence only.
- The packet records `phase_5_blocker: false`.
- The packet recommends same-repo-first decomposition and rejects cross-repo
  extraction.
- The packet identifies the first safe implementation slice as pure
  status/state/payload helper extraction, not supervisor-loop extraction.
- The packet defines false-authority flags and explicit non-claims.
- The packet defines validation expectations for a later implementation.
- The packet routes next to Codex E for contract review.

## Non-Claims

This contract does not claim:

- implementation authorization;
- file movement authorization;
- same-repo decomposition authorization;
- cross-repo extraction authorization;
- ARS clearance;
- Refactor Scout clearance;
- live-capture behavior readiness;
- reliability readiness;
- parser truth;
- analytics truth;
- AI truth;
- coaching truth;
- release readiness;
- deploy readiness;
- production readiness;
- security assurance;
- privacy assurance.

## Recommended Next Role

Codex E - Module Reviewer.

Codex E should review this packet against issue #719, #161 evidence wording,
the Phase 5 packet vocabulary, and current live-capture control runtime tests.
Review should focus on whether the schema extension is clear, whether #161
evidence is bounded correctly, whether the first slice is small enough, and
whether protected runtime behavior is sufficiently fenced off.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge issue #719.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/719

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Evidence source:
https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161

Target artifact:
docs/contracts/core_live_capture_control_runtime_decomposition_decision_packet.md

Review the Codex B decomposition decision packet for
src/mythic_edge_parser/local_app/live_capture_control.py. Verify that it keeps
the packet contract-only, preserves the #161 evidence boundary, uses coherent
Phase 5 schema/vocabulary, recommends only a behavior-preserving same-repo
first slice, protects public live-capture status/start/stop entrypoints, and
does not authorize implementation, file movement, ARS/Refactor execution,
private log reads, live-capture behavior changes, parser behavior changes,
frontend/API payload changes, EventBus changes, CI changes, or
readiness/truth/assurance claims.

Expected output:
Findings first, ordered by severity. If the contract is ready, say so and route
to Codex F only if docs-only submission is appropriate. If blocked, route back
to Codex B with exact finding ids, contract sections, expected correction, and
a workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/719"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  residual_promotion_queue: "https://github.com/Tahjali11/Mythic-Edge/issues/715"
  evidence_source_issue: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/161"
  evidence_source_pr: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/pull/163"
  evidence_source_merge_commit: "a812321ea309aa7c3da8f726134c4783972bf484"
  completed_thread: "B"
  next_thread: "E"
  verdict: "live_capture_control_runtime_decomposition_decision_packet_ready_for_contract_review"
  risk_tier: "High"
  target_commit: "9528bb3bee9c1d241268cb8a7d1a806b118471de"
  current_origin_main: "3710b449e685e2eb31d1927c2763334ed553cc60"
  target_artifact: "docs/contracts/core_live_capture_control_runtime_decomposition_decision_packet.md"
  candidate_id: "live-capture-control-runtime"
  candidate_surface: "src/mythic_edge_parser/local_app/live_capture_control.py"
  base_phase_5_packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
  packet_schema: "core_live_capture_control_runtime_decomposition_decision_packet.v1"
  schema_extension_scope: "issue_719_live_capture_control_runtime_only"
  candidate_scope: "live_capture_control_runtime_only"
  candidate_surface_class_source: "issue_719_extension"
  candidate_surface_class: "live_capture_runtime_bridge_surface"
  phase_5_blocker: false
  final_decision: "same_repo_decomposition_candidate"
  recommended_first_slice: "extract_pure_status_state_payload_helpers"
  evidence_status: "current_matching_scope"
  fresh_scoped_evidence_needed_before_implementation: false
  same_repo_first: true
  implementation_authorized: false
  file_move_authorized: false
  same_repo_decomposition_authorized: false
  cross_repo_extraction_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  private_log_read_authorized: false
  raw_player_log_read_authorized: false
  private_evidence_inspection_authorized: false
  runtime_artifact_creation_authorized: false
  source_mutation_authorized: false
  live_capture_behavior_change_authorized: false
  live_capture_state_schema_change_authorized: false
  live_capture_start_stop_change_authorized: false
  live_capture_payload_shape_change_authorized: false
  supervisor_lifecycle_change_authorized: false
  event_stream_behavior_change_authorized: false
  sqlite_live_write_behavior_change_authorized: false
  mtga_process_lifecycle_behavior_change_authorized: false
  frontend_behavior_change_authorized: false
  api_payload_change_authorized: false
  backend_route_change_authorized: false
  parser_behavior_change_authorized: false
  parser_truth_ownership_change_authorized: false
  eventbus_behavior_change_authorized: false
  workbook_webhook_change_authorized: false
  apps_script_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
  analytics_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  truth_or_assurance_claimed: false
  ready_for_codex_c: false
```
