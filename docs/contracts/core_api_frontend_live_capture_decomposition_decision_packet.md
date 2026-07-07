# Core API/Frontend/Live-Capture Decomposition Decision Packet

Status: Draft contract for review

Role: Codex B - Module Contract Writer

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/693>

Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>

Latest completed EventBus/support issue:
<https://github.com/Tahjali11/Mythic-Edge/issues/690>

Latest completed EventBus/support PR:
<https://github.com/Tahjali11/Mythic-Edge/pull/692>

Latest merge commit: `a7eae88a1a755f47662be5a0fc89f1b5c3a75104`

Target artifact:
`docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md`

## Module

`core_api_frontend_live_capture_decomposition_decision_packet`

This contract is the Phase 5 decomposition decision packet for the
API/frontend/live-capture surface band.

Plain English: this surface band is not one simple module. It includes the
React app shell, the TypeScript local API client, and the Python local-app live
capture control layer. Those surfaces are connected by route paths, schema
constants, payload validation, explicit start/stop controls, local request
guarding, sanitized status output, and parser-owned fact capture. This packet
decides how to split the planning work into narrower children before any code
move is considered.

This contract is planning-only. It does not implement code, move files, open a
PR, run ARS, run Refactor Scout, read private logs, change frontend behavior,
change local API payloads or schemas, change live-capture behavior, change
parser behavior or parser truth ownership, change parser event classes, change
match identity, change game identity, change deduplication, change final
reconciliation, change workbook schema, change webhook payloads, change Apps
Script behavior, change CI, deploy, release, or production behavior, or claim
readiness, reliability readiness, parser truth, analytics truth, AI truth,
coaching truth, security assurance, privacy assurance, release readiness,
deploy readiness, or production readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: <https://github.com/Tahjali11/Mythic-Edge>
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/693>
- Project roadmap / tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Broad decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>
- Latest completed decomposition issue: <https://github.com/Tahjali11/Mythic-Edge/issues/690>
- Latest completed PR: <https://github.com/Tahjali11/Mythic-Edge/pull/692>
- Target artifact:
  `docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md`

## Source Artifacts Inspected

- GitHub issue #693
- GitHub issue #568
- GitHub issue #463
- GitHub issue #690 and PR #692 as the immediate predecessor lane
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `docs/decisions/ADR-0007-parser-runtime-state-decomposition-strategy.md`
- `docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`
- `docs/contracts/core_protected_surface_gate_decomposition_decision_packet.md`
- `docs/contracts/core_event_bus_support_decomposition_decision_packet.md`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`
- `tests/test_live_app_explicit_start_capture_control.py`
- `tests/test_live_app_mtga_process_lifecycle.py`

No private `Player.log`, `UTC_Log`, app-data, live MTGA data, runtime status
files, failed posts, generated local artifacts, workbook exports, raw diffs,
source patches, secrets, credentials, tokens, API keys, webhook URLs, ARS run
artifacts, Refactor Scout artifacts, or private evidence were read, created,
imported, or modified.

## Owning Layer

Primary layer: Local App / UI bridge.

This band bridges three responsibilities:

- the frontend app shell displays local setup, analytics, import, journal,
  diagnostics, privacy, and live-capture controls;
- the frontend API client owns local endpoint paths, loopback-only base URL
  selection, request-guard use, fetch helpers, and strict public-safe payload
  validation;
- the backend live-capture control layer owns explicit local start/stop/status
  behavior for app-owned live capture and hands parser-owned completed facts to
  local analytics ingest.

The parser and state layer still owns parser truth. The frontend and local API
client display or validate parser-produced and backend-produced payloads; they
do not own match facts, game facts, parser event classes, final reconciliation,
workbook schema, webhook payload shape, or Apps Script behavior.

## Internal Project Area

Local App / UI, with parser runtime and analytics ingest bridge contact.

This packet intentionally keeps Workbook / Transport, parser state, parser
event classes, and parser evidence decomposition out of scope. Parser state and
`state.py` remain last in the Phase 5 order unless a later owner decision
changes that sequence.

## Truth Owner

- `frontend/src/App.tsx` owns current React composition, local UI state,
  route/hash behavior, dashboard/live-capture controls, safe display labels,
  and form orchestration.
- `frontend/src/api.ts` owns current frontend endpoint constants, loopback API
  base URL restrictions, local request-guard use for mutating calls, fetch
  helper behavior, frontend-side payload validators, and safe error mapping.
- `frontend/src/types.ts` owns current TypeScript payload constants and type
  shapes used by the frontend.
- `src/mythic_edge_parser/local_app/backend.py` owns current FastAPI route
  binding between `/api/live/capture/*` endpoints and local-app functions.
- `src/mythic_edge_parser/local_app/live_capture_control.py` owns current
  explicit local live-capture status/start/stop behavior, supervisor lifecycle,
  state-file shape, heartbeat/progress diagnostics, parser-owned fact capture,
  local SQLite ingest calls, redaction, and no-external-transport flags.
- Parser state and parser model code own parser facts consumed by live capture.
- Repo governance docs, accepted ADRs, active issues, and reviewed contracts
  remain authoritative for workflow routing and protected-surface authority.

## Bridge-Code Status

`bridge_code`

Source internal project area: Local App / UI.

Consuming and contacted areas:

- parser runtime/state, because live capture calls parser update and summary
  builders;
- analytics ingest, because completed parser-owned rows can be written into
  the local analytics database;
- frontend UI, because users see and control live capture through React;
- local API transport, because the browser talks to FastAPI endpoints.

Allowed data flow:

```text
parser-owned facts and local-app status
  -> backend route payloads
  -> frontend API validators
  -> React display and explicit operator controls
```

Forbidden reverse flow:

```text
frontend display state or workbook/dashboard interpretation
  -/-> parser truth
  -/-> parser event classes
  -/-> match or game identity
  -/-> final reconciliation
  -/-> workbook/webhook/Apps Script truth
```

## Files Owned By This Contract

- `docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md`

Files referenced but not owned:

- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`
- `frontend/src/App.test.tsx`
- `frontend/src/api.test.ts`
- `tests/test_live_app_explicit_start_capture_control.py`
- `tests/test_live_app_mtga_process_lifecycle.py`
- `tests/test_analytics_local_app_backend.py`

## Authorization State

The following flags are false for this contract:

```yaml
implementation_authorized: false
file_move_authorized: false
same_repo_decomposition_authorized: false
cross_repo_extraction_authorized: false
frontend_behavior_change_authorized: false
api_payload_change_authorized: false
api_route_change_authorized: false
request_guard_change_authorized: false
live_capture_behavior_change_authorized: false
live_capture_status_schema_change_authorized: false
live_capture_start_stop_change_authorized: false
live_capture_supervisor_change_authorized: false
live_capture_state_file_change_authorized: false
live_capture_sqlite_ingest_change_authorized: false
parser_behavior_change_authorized: false
parser_truth_ownership_change_authorized: false
parser_event_class_change_authorized: false
match_identity_change_authorized: false
game_identity_change_authorized: false
deduplication_change_authorized: false
final_reconciliation_change_authorized: false
workbook_schema_change_authorized: false
webhook_payload_change_authorized: false
apps_script_change_authorized: false
ci_change_authorized: false
deployment_change_authorized: false
release_change_authorized: false
production_behavior_change_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
private_log_read_authorized: false
source_mutation_authorized: false
runtime_artifact_creation_authorized: false
readiness_claimed: false
reliability_readiness_claimed: false
parser_truth_claimed: false
analytics_truth_claimed: false
ai_truth_claimed: false
coaching_truth_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
truth_or_assurance_claimed: false
```

Any future handoff, review, evidence packet, or implementation plan that flips
one of these flags without a separate reviewed issue and explicit owner
approval must fail closed.

## Schema Vocabulary Reconciliation

This packet consumes the Phase 5 decision-packet shape from
`docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`
where that shared shape applies. It also defines issue-local descriptive
surface kinds for the API/frontend/live-capture band.

Canonical shared fields:

- `packet_schema` remains
  `core_governance_report_helper_phase_5_decomposition_decision_packet.v1`.
- `candidate_surface_class` uses `mixed_governance_runtime_surface` for the
  band-level row because the shared #665 schema does not define a dedicated
  API/frontend/live-capture class.
- Descriptive values such as `frontend_api_client_surface` may appear only in
  the issue-local `candidate_surface_kind` field and must not replace
  `candidate_surface_class`.
- `final_decision` uses only #665 decision vocabulary:
  `request_scope_split_child`, `request_fresh_ars_refactor_evidence`,
  `same_repo_decomposition_candidate`, `defer`, or `review_required`.
- Same-repo decomposition remains preferred in prose only. It is not
  implementation authority.
- Cross-repo extraction remains rejected for this band.
- ARS/refactor evidence blocks use the #665 required fields and allowed
  values.

Issue-local `candidate_surface_kind` values:

- `api_frontend_live_capture_band`
- `frontend_api_client_surface`
- `frontend_app_shell_surface`
- `local_app_live_capture_control_surface`
- `backend_route_binding_surface`
- `types_contract_surface`

## Codex E Blocker Reconciliation

This continuation resolves the Codex E blocker packet for:

- `API-LIVECAP-DECOMP-E-001`: candidate-row schema ambiguity.
- `API-LIVECAP-DECOMP-E-002`: validation command ambiguity.

Schema clarification:

- A compact routing table is not a canonical #665 candidate row unless it also
  carries every required #665 row field.
- Canonical rows in this packet are the YAML blocks under `Band Row` and
  `First Recommended Child Row`.
- A later role must not copy the routing summary table as implementation input
  unless it expands each row with `current_behavior`,
  `truth_or_authority_owner`, `upstream_dependencies`, `downstream_consumers`,
  `protected_surface_contact`, `proposed_destination`, `why_not_keep_local`,
  `why_not_move_to_existing_repo`, `why_not_create_new_repo`,
  `new_public_interface_needed`, `new_public_interface_description`,
  `behavior_preservation_tests`, `rollback_plan`,
  `ars_refactor_evidence_status`, `non_claims`, and `final_decision`.
- Every canonical row must explicitly keep `ars_refactor_evidence_status` as
  `fresh_scoped_evidence_required_before_implementation` unless a later
  issue-scoped owner exception is recorded.
- Every canonical row must include non-claims. Absence of non-claims is a
  schema failure, not a harmless omission.

Validation clarification:

- The current `tools/check_secret_patterns.py` command does not accept a direct
  file path argument. Contract validation must pass the path through
  `--paths-from-stdin` with `--base origin/main`, or use `--all` when broader
  scanning is appropriate.
- Because Codex B leaves new contract files untracked, plain `git diff --check`
  may not inspect the new file body. Codex B must also run a direct new-file
  whitespace check such as `git diff --no-index --check -- /dev/null <path>`
  and treat exit code `1` from the file difference as non-failure when there are
  no whitespace errors.
- `tools/check_protected_surfaces.py --base origin/main` is still useful as a
  protected-surface smoke check, but if it reports `changed_paths: 0` because
  the contract file is untracked, that output must be described as limited and
  not represented as proof that the new file was included in the protected
  surface diff.

## Packet Envelope

```yaml
packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
repository: "Tahjali11/Mythic-Edge"
repository_url: "https://github.com/Tahjali11/Mythic-Edge"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/693"
tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
source_contract: "docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md"
latest_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/690"
latest_completed_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/692"
latest_merge_commit: "a7eae88a1a755f47662be5a0fc89f1b5c3a75104"
target_commit: "a7eae88a1a755f47662be5a0fc89f1b5c3a75104"
candidate_scope: "api_frontend_live_capture_band"
candidate_id: "api_frontend_live_capture"
candidate_surface_class: "mixed_governance_runtime_surface"
candidate_surface_kind: "api_frontend_live_capture_band"
current_path:
  - "frontend/src/App.tsx"
  - "frontend/src/api.ts"
  - "src/mythic_edge_parser/local_app/live_capture_control.py"
target_artifact: "docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md"
phase_5_order_preserved: true
governance_report_helper_phase_complete: true
eventbus_support_phase_complete: true
api_frontend_live_capture_active: true
parser_state_deferred: true
final_decision: "request_scope_split_child"
implementation_authorized: false
file_move_authorized: false
cross_repo_extraction_authorized: false
frontend_behavior_change_authorized: false
api_payload_change_authorized: false
live_capture_behavior_change_authorized: false
parser_behavior_change_authorized: false
parser_event_class_change_authorized: false
workbook_webhook_change_authorized: false
ci_change_authorized: false
ars_run_authorized: false
refactor_scout_run_authorized: false
source_mutation_authorized: false
readiness_claimed: false
reliability_readiness_claimed: false
parser_truth_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
truth_or_assurance_claimed: false
```

## Observed Current Behavior

### Frontend App Shell

`frontend/src/App.tsx` is currently about 5,984 lines. It:

- imports many API helpers and type contracts from `frontend/src/api.ts` and
  `frontend/src/types.ts`;
- owns the `SetupStatusApp` React component and route/hash behavior;
- loads setup, analytics history, dashboard modules, analytics refresh state,
  live diagnostics, live capture status, Match Journal state, manual import
  state, and error-report preview/submission state;
- renders dashboard, analytics, review, import, diagnostics, privacy, journal,
  feedback, and technical-details views;
- renders live-capture dashboard and detailed control panels;
- calls `startCapture` and `stopCapture` only through injected API helpers;
- fails closed when live capture control is unavailable, stale, malformed, or
  ownership-blocked;
- displays sanitized labels and avoids exposing raw backend details or unsafe
  path-like strings.

### Frontend API Client

`frontend/src/api.ts` is currently about 3,000 lines. It:

- defines local API endpoint constants such as `/api/live/capture/status`,
  `/api/live/capture/start`, and `/api/live/capture/stop`;
- restricts API base URLs to empty or loopback HTTP origins;
- obtains and uses a local request guard for mutating helpers;
- fetches setup status, live status, live capture control, analytics history,
  dashboard modules, manual import, Match Journal, and error-report payloads;
- validates required object names, schema versions, status vocabularies,
  public-safe labels, and no-echo fields;
- maps backend/network/malformed responses to safe API error classes;
- rejects malformed live capture heartbeat, progress, lifecycle, parser status
  blurb, state, and precondition payloads.

### Live-Capture Control

`src/mythic_edge_parser/local_app/live_capture_control.py` is currently about
1,813 lines. It:

- exposes `build_live_capture_status`, `start_live_capture`, and
  `stop_live_capture`;
- owns live-capture object and schema constants also mirrored by frontend
  types;
- controls a registered app-owned supervisor through an in-memory registry;
- writes and reads a sanitized local capture state file under the app-data jobs
  directory;
- checks configured Player.log readiness, analytics database readiness, state
  directory readiness, single-instance guard status, and frontend control
  authorization;
- starts a live parser event stream only after explicit operator control;
- resets parser runtime state for the capture session, updates parser match
  summary state from streamed events, builds parser-owned match/game rows, and
  writes completed rows to local analytics ingest;
- emits heartbeat/progress diagnostics and parser-status blurbs without raw log
  content, local paths, private exception text, or external transport;
- preserves `external_transport_allowed: false` and
  `raw_player_log_storage_enabled: false`.

### Backend Route Binding

`src/mythic_edge_parser/local_app/backend.py` binds:

- `GET /api/live/capture/status` to `build_live_capture_status`;
- `POST /api/live/capture/start` to `start_live_capture`;
- `POST /api/live/capture/stop` to `stop_live_capture`.

Start and stop routes use guarded mutation dependencies. This contract does
not authorize route changes, guard changes, method changes, or payload shape
changes.

## Problem Statement And First Bad Values

The intended workflow is:

1. use this packet to decide the first narrow child for future decomposition;
2. preserve frontend display behavior, local API payload contracts, and live
   capture runtime behavior;
3. require Codex E review before any submitter or implementation route;
4. require fresh scoped ARS or Refactor Scout evidence before implementation
   unless the owner records an explicit issue-scoped exception;
5. keep any future split same-repo-first.

The first bad value is treating this decision packet as implementation
authority.

The second bad value is splitting all three large files in one implementation
issue. They are related, but they do not have the same risk profile.

The third bad value is changing API payload shape, schema constants, local
request guard behavior, route paths, safe-label validators, or frontend control
semantics while calling the work behavior-preserving.

The fourth bad value is changing live-capture supervisor ownership, state-file
shape, heartbeat/progress vocabulary, parser-owned fact capture, SQLite ingest
behavior, raw-log storage, or external-transport flags during a decomposition.

The fifth bad value is letting frontend display state, dashboard labels, or API
client validation become parser truth.

The sixth bad value is bundling parser state or `state.py` decomposition into
this issue. Parser state remains deferred.

## Decision Summary

Decision: `request_scope_split_child`

The API/frontend/live-capture band should split into narrower child issues
before any implementation. The band is too broad for one behavior-preserving
decomposition pass because it crosses React UI composition, TypeScript API
validation, FastAPI route binding, local runtime supervision, parser state
contact, and local analytics ingest.

Recommended first concrete child after Codex E review and owner routing:

```yaml
first_child_candidate_id: "frontend_api_client_boundary"
first_child_surface_kind: "frontend_api_client_surface"
recommended_route: "same_repo_decomposition_candidate_after_fresh_evidence"
current_path: "frontend/src/api.ts"
stable_public_facade_to_preserve: "frontend/src/api.ts"
possible_private_destination_family: "frontend/src/api/*"
implementation_authorized_now: false
fresh_scoped_ars_or_refactor_evidence_required_before_implementation: true
```

Why this child first:

- it is narrower than `frontend/src/App.tsx`;
- it has focused tests in `frontend/src/api.test.ts`;
- it can preserve the existing `./api` public import facade while moving
  private validation or endpoint families later;
- it can reduce review risk for later app-shell decomposition;
- it avoids touching Python live-capture runtime behavior first.

Deferred children:

- `frontend_app_shell`: defer until the API client boundary is reviewed or the
  owner explicitly selects UI composition as the first child.
- `live_capture_control`: defer until the frontend/API client boundary is
  stable and fresh scoped evidence exists. This is higher risk because it
  touches parser state contact, local runtime control, state files, heartbeat,
  progress, and SQLite ingest.
- `backend_route_binding`: keep local and unchanged unless a later API route
  contract explicitly authorizes a change.

Cross-repo extraction is rejected for this band. Local App / UI remains in the
primary `Tahjali11/Mythic-Edge` repository by ADR-0006 default, and this band
depends on repo-local backend routes, TypeScript contracts, parser runtime
contacts, and frontend tests. A new repo or existing sibling repo would add
versioning and coordination risk without proving a safer boundary.

## Candidate Split Summary And Canonical Rows

The table below is a split-routing summary. It is not, by itself, a canonical
#665 candidate-row payload for every listed placeholder. Canonical rows in this
packet are the detailed YAML rows that follow the table. Any future role that
promotes a deferred placeholder must create its own complete candidate row with
all required #665 fields, including `ars_refactor_evidence_status` and
`non_claims`.

| candidate_id | candidate_surface_class | candidate_surface_kind | current_path | final_decision |
| --- | --- | --- | --- | --- |
| `api_frontend_live_capture` | `mixed_governance_runtime_surface` | `api_frontend_live_capture_band` | `frontend/src/App.tsx`; `frontend/src/api.ts`; `src/mythic_edge_parser/local_app/live_capture_control.py` | `request_scope_split_child` |
| `frontend_api_client_boundary` | `mixed_governance_runtime_surface` | `frontend_api_client_surface` | `frontend/src/api.ts` | `request_fresh_ars_refactor_evidence` |
| `frontend_app_shell` | `mixed_governance_runtime_surface` | `frontend_app_shell_surface` | `frontend/src/App.tsx` | `defer` |
| `live_capture_control_boundary` | `mixed_governance_runtime_surface` | `local_app_live_capture_control_surface` | `src/mythic_edge_parser/local_app/live_capture_control.py` | `defer` |
| `backend_route_binding` | `mixed_governance_runtime_surface` | `backend_route_binding_surface` | `src/mythic_edge_parser/local_app/backend.py` | `review_required` |

### Band Row

```yaml
candidate_id: "api_frontend_live_capture"
candidate_surface_class: "mixed_governance_runtime_surface"
candidate_surface_kind: "api_frontend_live_capture_band"
current_path:
  - "frontend/src/App.tsx"
  - "frontend/src/api.ts"
  - "src/mythic_edge_parser/local_app/live_capture_control.py"
current_behavior: "Coordinates frontend UI state, local API client validation, and explicit live-capture backend control."
truth_or_authority_owner: "Local App / UI bridge; parser facts remain parser-owned."
upstream_dependencies:
  - "frontend/src/types.ts"
  - "src/mythic_edge_parser/local_app/backend.py"
  - "src/mythic_edge_parser/local_app/live_capture_control.py"
  - "src/mythic_edge_parser/app/state.py"
  - "src/mythic_edge_parser/stream.py"
  - "src/mythic_edge_parser/app/analytics_ingest.py"
downstream_consumers:
  - "React local app UI"
  - "frontend API tests"
  - "backend local app tests"
  - "manual operator live-capture workflow"
  - "local analytics database ingest path"
protected_surface_contact: "mixed_review_required"
proposed_destination: "split_into_narrower_same_repo_children"
why_not_keep_local: "The three-file band is too broad for one implementation issue; narrow children reduce review risk."
why_not_move_to_existing_repo: "Local App / UI remains primary-repo owned and depends on repo-local backend, parser, and frontend contracts."
why_not_create_new_repo: "No stable independently versioned interface exists; extraction would add coordination risk."
new_public_interface_needed: "review_required"
new_public_interface_description: "No public interface change is allowed by this packet; later children must preserve existing facades."
behavior_preservation_tests:
  - "frontend/src/api.test.ts"
  - "frontend/src/App.test.tsx"
  - "tests/test_live_app_explicit_start_capture_control.py"
  - "tests/test_live_app_mtga_process_lifecycle.py"
ars_refactor_evidence_status: "fresh_scoped_evidence_required_before_implementation"
non_claims:
  - "not_implementation_authority"
  - "not_file_move_authority"
  - "not_frontend_behavior_change"
  - "not_api_payload_change"
  - "not_live_capture_behavior_change"
  - "not_parser_behavior_change"
  - "not_workbook_webhook_change"
  - "not_apps_script_change"
  - "not_ci_change"
  - "not_ars_clearance"
  - "not_refactor_scout_clearance"
  - "not_readiness"
  - "not_reliability_readiness"
  - "not_parser_truth"
  - "not_security_assurance"
  - "not_privacy_assurance"
rollback_plan: "Revert any later same-repo private-module extraction while preserving frontend/src/api.ts, frontend/src/App.tsx, backend routes, and live_capture_control.py public entry points."
final_decision: "request_scope_split_child"
```

### First Recommended Child Row

```yaml
candidate_id: "frontend_api_client_boundary"
candidate_surface_class: "mixed_governance_runtime_surface"
candidate_surface_kind: "frontend_api_client_surface"
current_path: "frontend/src/api.ts"
current_behavior: "Owns local endpoint constants, loopback base URL policy, request guard use, fetch helpers, payload validation, and safe API error mapping."
truth_or_authority_owner: "Frontend API client owns browser-side validation and error mapping only; backend and parser remain truth owners for payload contents."
upstream_dependencies:
  - "frontend/src/types.ts"
  - "src/mythic_edge_parser/local_app/backend.py"
  - "backend payload contracts"
downstream_consumers:
  - "frontend/src/App.tsx"
  - "frontend/src/api.test.ts"
  - "future frontend components"
protected_surface_contact: "mixed_review_required"
proposed_destination: "same_repo_private_modules_behind_frontend_src_api_ts_facade"
why_not_keep_local: "api.ts mixes endpoint constants, request guard, fetch helpers, validators, and domain families; private same-repo modules may reduce review risk."
why_not_move_to_existing_repo: "The API client is app-specific and tied to repo-local type constants and backend routes."
why_not_create_new_repo: "No stable versioned package boundary exists, and a new repo would not improve behavior preservation."
new_public_interface_needed: "private_same_repo"
new_public_interface_description: "Preserve imports from frontend/src/api.ts; any private modules remain implementation detail."
behavior_preservation_tests:
  - "npm --prefix frontend test -- --run frontend/src/api.test.ts"
  - "npm --prefix frontend run typecheck"
  - "python3 tools/check_secret_patterns.py --all"
  - "python3 tools/check_protected_surfaces.py --base origin/main"
ars_refactor_evidence_status: "fresh_scoped_evidence_required_before_implementation"
non_claims:
  - "not_implementation_authority"
  - "not_file_move_authority"
  - "not_frontend_behavior_change"
  - "not_api_payload_change"
  - "not_live_capture_behavior_change"
  - "not_parser_behavior_change"
  - "not_workbook_webhook_change"
  - "not_apps_script_change"
  - "not_ci_change"
  - "not_ars_clearance"
  - "not_refactor_scout_clearance"
  - "not_readiness"
  - "not_reliability_readiness"
  - "not_parser_truth"
  - "not_security_assurance"
  - "not_privacy_assurance"
rollback_plan: "Keep frontend/src/api.ts as the public facade so private module extraction can be reverted by collapsing helpers back into the facade."
final_decision: "request_fresh_ars_refactor_evidence"
```

## ARS And Refactor Evidence Status

```yaml
prior_ars_evidence_found: "no"
prior_refactor_scout_evidence_found: "no"
reviewed_repo: "none"
reviewed_scope: "none"
reviewed_commit: "none"
ars_version_contract_bundle: "none"
current_target_commit: "a7eae88a1a755f47662be5a0fc89f1b5c3a75104"
relevant_changes_since_review: "not_applicable"
evidence_status: "fresh_scoped_evidence_required_before_implementation"
fresh_scoped_evidence_needed: "yes"
reason: "The exact API/frontend/live-capture decomposition question has no current scoped ARS or Refactor Scout evidence, and the band touches user-visible UI, API payload validation, local runtime control, parser-owned fact capture, and no-echo/private-boundary behavior."
```

Fresh scoped evidence is not required to review this contract. It is required
before any later implementation unless the owner records an explicit,
issue-scoped exception. That exception must not be represented as ARS clearance
or Refactor Scout clearance.

## Public Interfaces To Preserve

A later implementation child must preserve all public interfaces in its scoped
surface unless a new contract explicitly authorizes a change.

Frontend API client interfaces:

- `frontend/src/api.ts` import path and named exports currently consumed by
  `frontend/src/App.tsx` and tests;
- local endpoint constants and their effective paths, including
  `/api/live/capture/status`, `/api/live/capture/start`, and
  `/api/live/capture/stop`;
- `getApiBaseUrl` loopback-only policy;
- local request guard flow for mutating helpers;
- `fetchLiveCaptureStatus`, `startLiveCapture`, and `stopLiveCapture`;
- API error classes and safe error-code mapping;
- payload validators for setup, live watcher, live capture, analytics, manual
  import, Match Journal, and error-report responses.

Frontend app interfaces:

- `SetupStatusApp` props used by tests and dependency injection;
- hash route behavior and safe fallback to dashboard;
- live-capture dashboard and detail control behavior;
- no raw backend details, stack traces, unsafe local paths, or private markers
  in rendered UI.

Backend and live-capture interfaces:

- FastAPI route paths and methods for `/api/live/capture/*`;
- guarded mutation requirement for start/stop;
- `build_live_capture_status`, `start_live_capture`, and
  `stop_live_capture` return shapes;
- live-capture object names and schema versions;
- `mode: "explicit_operator_control"`;
- `external_transport_allowed: false`;
- `raw_player_log_storage_enabled: false`;
- heartbeat, progress, MTGA lifecycle, precondition, state, warning, error,
  and parser-status blurb vocabularies;
- parser-owned fact capture via parser state and local analytics ingest.

## Invariants

- Parser facts remain parser-owned.
- Frontend state must not invent parser truth.
- API validators must reject malformed, incompatible, private-marker, unsafe,
  or non-contract labels safely.
- Start and stop remain explicit operator controls.
- Start and stop remain guarded local mutations.
- Live capture status GET remains read-only.
- Live capture must not expose raw `Player.log` content, raw local paths,
  private exception text, raw detector output, credentials, tokens, API keys,
  webhook URLs, or stack traces.
- Live capture must preserve local-only behavior; this packet does not
  authorize external transport.
- Existing backend route paths, object names, schema versions, and public
  payload fields remain unchanged.
- Frontend behavior, API payload shape, live-capture behavior, parser behavior,
  workbook/webhook behavior, Apps Script behavior, CI, deployment, release,
  and production behavior remain unchanged.

## Error Behavior

Contract ambiguity must fail closed to Codex B or Codex E review.

Malformed or unsafe future implementation proposals must fail closed when they:

- remove the `frontend/src/api.ts` facade without a public-interface contract;
- change endpoint paths, HTTP methods, request guard behavior, object names, or
  schema versions;
- weaken API validation or no-echo behavior;
- change React control enablement, stale-state handling, or ownership-blocked
  behavior;
- change live-capture supervisor state, start/stop semantics, state-file shape,
  heartbeat/progress vocabulary, SQLite ingest behavior, or parser-state
  contact;
- treat source inspection, ARS evidence, Refactor Scout evidence, tests, or
  reviewer acceptance as implementation authority.

## Behavior-Preservation Validation Plan

Docs-only validation for this contract:

```bash
printf '%s\n' docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
git diff --no-index --check -- /dev/null docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md
```

If the contract file is still untracked, `git diff --check` and
`check_protected_surfaces.py --base origin/main` may report no changed paths.
In that state, Codex B must rely on the direct secret-pattern stdin scan and
direct new-file no-index whitespace check for the new file body, and must say
that protected-surface validation will become fully meaningful only after the
file is tracked or staged by a later submitter role.

Future implementation validation for a frontend API client child should include
at minimum:

```bash
npm --prefix frontend test -- --run frontend/src/api.test.ts
npm --prefix frontend run typecheck
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
```

Future implementation validation for a frontend app shell child should include
at minimum:

```bash
npm --prefix frontend test -- --run frontend/src/App.test.tsx frontend/src/api.test.ts
npm --prefix frontend run typecheck
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
```

Future implementation validation for a live-capture control child should
include at minimum:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_live_app_explicit_start_capture_control.py tests/test_live_app_mtga_process_lifecycle.py tests/test_analytics_local_app_backend.py
npm --prefix frontend test -- --run frontend/src/api.test.ts frontend/src/App.test.tsx
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
```

Broader test selection may be required if a later implementation touches
additional imports, route bindings, parser state contact, analytics ingest,
frontend components, or shared TypeScript types.

## Acceptance Criteria

- This packet identifies the API/frontend/live-capture candidate band.
- This packet recommends splitting the band into narrower children.
- This packet names `frontend_api_client_boundary` as the first preferred
  later child after review, owner routing, and fresh scoped evidence.
- This packet preserves same-repo-first decomposition and rejects cross-repo
  extraction.
- This packet records ARS/Refactor evidence status as absent and fresh scoped
  evidence required before implementation.
- This packet preserves parser truth ownership, frontend behavior, API payload
  shape, live-capture behavior, workbook/webhook behavior, Apps Script
  behavior, and CI boundaries.
- This packet does not authorize implementation, file movement, behavior
  changes, private evidence reads, ARS/Refactor execution, source mutation, CI
  changes, or readiness/truth/assurance claims.

## Stop Conditions

Stop and route back to Codex B, Codex A, or owner decision if any later request
asks to:

- implement code from this packet alone;
- move files from this packet alone;
- open a PR from Codex B;
- run ARS or Refactor Scout;
- read private logs, app-data, runtime artifacts, raw diffs, source patches, or
  workbook exports;
- change frontend behavior;
- change API payloads, endpoint paths, schema constants, object names, or local
  request guard behavior;
- change live-capture behavior, supervisor semantics, state-file shape,
  heartbeat/progress vocabulary, SQLite ingest behavior, external transport, or
  raw-log storage policy;
- change parser behavior, parser truth ownership, parser event classes, match
  identity, game identity, deduplication, or final reconciliation;
- change workbook schema, webhook payloads, Apps Script behavior, CI,
  deployment, release, or production behavior;
- claim readiness, reliability readiness, parser truth, analytics truth, AI
  truth, coaching truth, security assurance, privacy assurance, release
  readiness, deploy readiness, or production readiness.

## Recommended Next Role

Recommended next role: Codex E contract reviewer for Mythic Edge issue #693.

Codex E should review whether this packet:

- preserves the Phase 5 order and keeps parser state deferred;
- correctly classifies this band as bridge code;
- uses the shared Phase 5 decision vocabulary without inventing schema values;
- recommends a narrower first child without authorizing implementation;
- keeps `frontend/src/api.ts` as the stable public frontend API facade for any
  later private-module extraction;
- requires fresh scoped ARS or Refactor Scout evidence before implementation;
- preserves frontend/API/live-capture/parser/workbook/webhook/Apps Script/CI
  boundaries and non-claims.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Contract Reviewer for Mythic Edge issue #693.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/693

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Target artifact:
docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md

Review the API/frontend/live-capture Phase 5 decomposition decision packet.
Confirm whether it correctly treats frontend/src/App.tsx, frontend/src/api.ts,
and src/mythic_edge_parser/local_app/live_capture_control.py as a high-risk
bridge band, recommends splitting into narrower children, selects
frontend_api_client_boundary as the first later candidate only after review and
fresh scoped evidence, preserves same-repo-first and cross-repo rejection,
uses accepted Phase 5 schema vocabulary, and avoids implementation, file
movement, behavior changes, ARS/Refactor execution, private evidence reads,
CI changes, protected-surface changes, truth claims, readiness claims, and
assurance claims.

Expected output:
Findings first, verdict, validation run, remaining risks, recommended next role,
and workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/693"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  latest_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/690"
  latest_completed_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/692"
  latest_merge_commit: "a7eae88a1a755f47662be5a0fc89f1b5c3a75104"
  completed_thread: "B"
  next_thread: "E"
  verdict: "api_frontend_live_capture_decomposition_decision_packet_ready_for_review"
  target_artifact: "docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md"
  decision: "request_scope_split_child"
  first_recommended_child: "frontend_api_client_boundary"
  fresh_scoped_ars_or_refactor_evidence_required_before_implementation: true
  implementation_authorized: false
  file_move_authorized: false
  same_repo_decomposition_authorized: false
  cross_repo_extraction_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  frontend_behavior_change_authorized: false
  api_payload_change_authorized: false
  live_capture_behavior_change_authorized: false
  parser_behavior_change_authorized: false
  parser_truth_ownership_change_authorized: false
  workbook_webhook_change_authorized: false
  apps_script_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
  analytics_truth_claimed: false
  ai_truth_claimed: false
  coaching_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
