# Core Frontend App Shell Live-Capture Controls Decomposition Decision Packet

Status: Draft contract for review

Role: Codex B - Module Contract Writer

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/708>

Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>

Source decision packet: <https://github.com/Tahjali11/Mythic-Edge/issues/697>

Latest completed frontend decomposition issue:
<https://github.com/Tahjali11/Mythic-Edge/issues/706>

Latest completed frontend decomposition PR:
<https://github.com/Tahjali11/Mythic-Edge/pull/707>

Latest merge commit: `10cd9820926786b33a7a64596753001ed303dffb`

Target artifact:
`docs/contracts/core_frontend_app_shell_live_capture_controls_decomposition_decision_packet.md`

## Module

`core_frontend_app_shell_live_capture_controls_decomposition_decision_packet`

This contract is the Phase 5 decomposition decision packet for the
live-capture controls currently embedded in `frontend/src/App.tsx`.

Plain English: this is the user-facing slice that lets the operator start or
stop local live capture and inspect live capture status without making the
frontend a parser, backend, workbook, webhook, or production truth owner. The
future split must preserve current controls exactly before it may reduce the
size of `frontend/src/App.tsx`.

This contract is planning-only. It does not implement code, move files, open a
PR, run ARS, run Refactor Scout, read private logs, change frontend behavior,
change route/hash behavior, change visible controls, change API payload shape,
change live-capture behavior, change backend routes, change parser behavior,
change workbook/webhook/Apps Script behavior, change CI, or claim readiness,
parser truth, reliability readiness, security assurance, or privacy assurance.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: <https://github.com/Tahjali11/Mythic-Edge>
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/708>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>
- Source app-shell decision issue:
  <https://github.com/Tahjali11/Mythic-Edge/issues/697>
- Latest completed frontend decomposition issue:
  <https://github.com/Tahjali11/Mythic-Edge/issues/706>
- Latest completed frontend decomposition PR:
  <https://github.com/Tahjali11/Mythic-Edge/pull/707>
- Latest merge commit: `10cd9820926786b33a7a64596753001ed303dffb`

## Source Artifacts Inspected

- GitHub issue #708
- GitHub PR #707
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md`
- `docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/package.json`

No private `Player.log`, `UTC_Log`, app-data, live MTGA data, runtime status
files, failed posts, generated local artifacts, workbook exports, raw diffs,
source patches, secrets, credentials, tokens, API keys, webhook URLs, ARS run
artifacts, Refactor Scout artifacts, or private evidence were read, created,
imported, or modified.

## Owning Layer

Primary layer: Local App / UI.

`frontend/src/App.tsx` owns the current React composition, injected frontend API
helpers, local live-capture control state, route/hash placement, safe display
labels, explicit start/stop event handlers, and diagnostics/dashboard control
placement.

It does not own backend live-capture runtime behavior, API payload shape,
parser fact capture, parser truth, workbook schema, webhook payloads, Apps
Script behavior, deployment behavior, or production behavior.

## Internal Project Area

Local App / UI, with read-only contact to backend-owned live-capture payloads
and parser-owned facts through the frontend API client.

## Truth Owner

- `src/mythic_edge_parser/local_app/live_capture_control.py` owns explicit
  local live-capture status/start/stop semantics and app-owned supervisor
  behavior.
- `src/mythic_edge_parser/local_app/backend.py` owns route binding for
  `/api/live/capture/status`, `/api/live/capture/start`, and
  `/api/live/capture/stop`.
- `frontend/src/api.ts` owns browser-side fetch helpers, local request guard
  use, strict payload validation, and safe error mapping.
- `frontend/src/types.ts` owns frontend TypeScript payload constants and shapes.
- `frontend/src/App.tsx` owns visible composition, safe labels, current local
  UI state, route/hash placement, and explicit operator controls.
- Parser/state code owns parser facts consumed by live capture.
- Repo governance docs, accepted ADRs, active issues, reviewed contracts,
  reviewed PRs, and deployer-recorded merge evidence own workflow authority.

The frontend live-capture controls are a display and explicit-control surface.
They must not become a truth owner for parser facts, live-capture lifecycle
semantics, backend route payloads, workbook/webhook behavior, or strategic
analytics conclusions.

## Bridge-Code Status

`bridge_code`

Source internal project area: Local App / UI.

Contacted areas:

- frontend API client, because `SetupStatusApp` receives default and
  test-injected live-capture helpers;
- local app backend, because visible state originates from local FastAPI
  payloads;
- parser runtime/state, because live-capture status references parser-owned
  fact capture;
- local analytics ingest, because live capture can write completed parser-owned
  rows into local SQLite.

Allowed data flow:

```text
parser-owned facts and backend-owned live-capture status
  -> backend route payloads
  -> frontend API validators
  -> React live-capture display and explicit operator controls
```

Forbidden reverse flow:

```text
React route state, display labels, control labels, disabled states, or dashboard text
  -/-> parser truth
  -/-> backend live-capture semantics
  -/-> API payload shape
  -/-> workbook, webhook, or Apps Script truth
```

## Files Owned By This Contract

- `docs/contracts/core_frontend_app_shell_live_capture_controls_decomposition_decision_packet.md`

Files referenced but not owned:

- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/src/api.ts`
- `frontend/src/types.ts`
- `frontend/package.json`
- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/live_capture_control.py`

## Authorization State

The following flags are false for this contract:

```yaml
implementation_authorized: false
file_move_authorized: false
same_repo_decomposition_authorized: false
cross_repo_extraction_authorized: false
frontend_behavior_change_authorized: false
route_hash_behavior_change_authorized: false
visible_control_change_authorized: false
aria_label_change_authorized: false
dashboard_tile_behavior_change_authorized: false
diagnostics_panel_behavior_change_authorized: false
api_payload_change_authorized: false
api_endpoint_change_authorized: false
request_guard_change_authorized: false
frontend_api_helper_change_authorized: false
live_capture_behavior_change_authorized: false
live_capture_status_schema_change_authorized: false
live_capture_start_stop_change_authorized: false
backend_route_change_authorized: false
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
runtime_artifact_creation_authorized: false
source_mutation_authorized: false
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

Any future handoff, review, implementation plan, or validation output that flips
one of these flags without a separate reviewed issue and explicit owner
approval must fail closed.

## Candidate Boundary Summary

This table is a planning summary. It is not implementation authority.

| candidate_id | candidate_surface_class | candidate_surface_kind | current_path | final_decision |
| --- | --- | --- | --- | --- |
| `frontend_live_capture_controls` | `mixed_frontend_runtime_control_surface` | `frontend_live_capture_controls_surface` | `frontend/src/App.tsx` live-capture control state, controls, handlers, and fail-closed helpers | `contract_ready_for_review` |

Compatibility note: if a project-wide inventory schema requires the older
shared value `mixed_governance_runtime_surface`, this candidate may be mapped
to that compatibility value only for inventory export. The issue-local
classification remains `mixed_frontend_runtime_control_surface`.

## Scope Decision

Decision: `same_repo_private_module_decomposition_preferred_after_review`

Cross-repo extraction is rejected. A new package or repository would add
versioning and coordination risk without a stable independently versioned
public interface.

The safest future implementation path is a two-pass same-repo split:

1. First pass: extract pure live-capture control components, action selection,
   status projection helpers, and display text helpers into a private frontend
   module behind the `frontend/src/App.tsx` facade.
2. Later pass only if separately scoped: extract async fetch effects,
   start/stop handlers, or a live-capture controller hook.

The first pass is preferred because it can reduce `App.tsx` size without
changing async flow, dependency injection, API helper boundaries, route/hash
behavior, or backend start/stop semantics.

## Recommended Same-Repo Module Boundary

A later implementation may introduce a private module such as:

```text
frontend/src/app_live_capture_controls.tsx
```

The exact filename is not prescribed, but the module must stay under
`frontend/src/`, remain repo-local, and sit behind the stable
`frontend/src/App.tsx` public facade.

Allowed first-pass extraction candidates:

- `LiveCaptureControlState` type, if exported only for `App.tsx` and tests;
- `DashboardLiveCaptureAction` type;
- `DashboardLiveCaptureControl`;
- `LiveCaptureControlPanel`;
- `liveCaptureStartAllowed`;
- `dashboardLiveCaptureAction`;
- `dashboardLiveCaptureBlockedAction`;
- `liveCaptureDashboardBlocked`;
- `liveCaptureDashboardStatus`;
- `liveCaptureDashboardDetail`;
- `liveCaptureControlPayload`;
- `liveCaptureStatusLabel`;
- `liveCaptureTone`;
- `liveCaptureControlDetail`;
- `liveCaptureBlurbText`;
- `liveCaptureControlMessage`;
- compact live-capture display helpers needed by the cockpit tile, if moving
  them does not change `CockpitStatusRail` item ordering or labels.

Conditionally allowed only if tests prove identical DOM and state behavior:

- the live-capture slot inside `CockpitStatusRail`;
- pure helper wiring from `buildCockpitStatusItems` into the live-capture
  dashboard tile.

Deferred to a later contract or explicit Codex C sub-scope:

- `useEffect` blocks that call `fetchLiveDiagnostics` or `fetchLiveCapture`;
- `useState` ownership for `liveDiagnosticsState` or
  `liveCaptureControlState`;
- `handleStartCapture`;
- `handleStopCapture`;
- full `LiveDiagnosticsPanel` extraction;
- API helper implementation in `frontend/src/api.ts`;
- backend live-capture route or runtime control code.

## Responsibilities That Must Remain In `App.tsx` Initially

The first future implementation should keep `frontend/src/App.tsx` as the
facade and owner of:

- `SetupStatusApp` named export and default export behavior;
- `SetupStatusAppProps`, including the injected `fetchLiveDiagnostics`,
  `fetchLiveCapture`, `startCapture`, and `stopCapture` props;
- route/hash reading and updates;
- placement of the dashboard cockpit rail and diagnostics panel;
- async fetch effect scheduling and cleanup;
- start/stop handler call sequencing;
- local app composition across dashboard, diagnostics, Match Journal, manual
  import, feedback, privacy, and analytics surfaces.

If a later implementation wants to move handler/effect logic into a hook, that
must be scoped as a second pass and must preserve every invariant in this
contract.

## Public Interface To Preserve

Frontend public exports:

- `frontend/src/App.tsx` import path;
- named `SetupStatusApp` export;
- default export behavior;
- `SetupStatusAppProps` behavior and injection points used by tests.

Frontend API helper boundary:

- `fetchLiveCaptureStatus`;
- `startLiveCapture`;
- `stopLiveCapture`;
- `fetchLiveWatcherDiagnosticsStatus`;
- `LiveStatusApiError` safe error mapping;
- `/api/live/capture/status`;
- `/api/live/capture/start`;
- `/api/live/capture/stop`;
- local request guard behavior for mutating calls.

Visible UI and route surfaces:

- dashboard cockpit rail placement;
- `Live capture` tile label;
- `Live capture lifecycle control` accessible label;
- `Start capture` button label;
- `Stop capture` button label;
- `Starting capture` pending label;
- `Stopping capture` pending label;
- `Live capture needs review` blocked label;
- `View live capture diagnostics` link label, title, and `href="#diagnostics"`;
- diagnostics-route `Live Capture Control` heading;
- diagnostics-route `Explicit local control` eyebrow;
- status pill labels and tones for live capture.

## Inputs

Primary inputs:

- `LiveCaptureStatusResponse` from the validated frontend API helper.
- `LiveCaptureStartResult` from the injected/default `startCapture` helper.
- `LiveCaptureStopResult` from the injected/default `stopCapture` helper.
- `LiveWatcherDiagnosticsResponse` from the injected/default diagnostics helper.
- `SetupStatusResponse` from the setup status payload, used only as fallback
  cockpit tile context when a control payload is unavailable.

Allowed input source:

```text
backend route payload -> frontend API validator -> SetupStatusApp injected/default helper -> UI state
```

Forbidden input source:

```text
raw local logs
private app-data files
runtime state files
raw Player.log content
unvalidated fetch response
workbook formula output
dashboard interpretation
model-generated interpretation
```

## Outputs

Allowed outputs:

- React elements already present in the current dashboard and diagnostics
  route;
- local component state transitions inside the browser;
- explicit calls to the injected/default `startCapture` and `stopCapture`
  helpers only when current payload permissions allow them.

Forbidden outputs:

- changed backend payloads;
- changed API route paths;
- changed request payloads;
- new parser facts;
- workbook or webhook writes;
- Apps Script changes;
- raw log display;
- source file or local path disclosure;
- readiness, reliability, parser truth, security, or privacy assurance claims.

## Preserved Control Invariants

A later behavior-preserving implementation must keep these invariants true:

- Start and stop remain explicit user actions.
- Start calls only the injected/default `startCapture` helper.
- Stop calls only the injected/default `stopCapture` helper.
- Start is unavailable while the state is submitting.
- Stop is unavailable while the state is submitting.
- Start is unavailable unless the current validated payload has
  `capture.start_allowed`.
- Stop is unavailable unless the current validated payload has
  `capture.stop_allowed`.
- Duplicate clicks on pending `Starting capture` or `Stopping capture` controls
  must not create additional API calls.
- Start success reconciles from `result.capture_status`.
- Stop success reconciles from `result.capture_status`.
- API errors are represented through safe `LiveStatusApiError` codes/messages
  or existing backend-unavailable fallbacks.
- Unknown non-`LiveStatusApiError` failures remain safe generic unavailable
  messages.

## Preserved Dashboard Invariants

A later implementation must preserve dashboard behavior:

- The cockpit rail still contains the `Live capture` tile.
- The dashboard live-capture control remains present inside the `Live capture`
  tile when route is dashboard.
- The diagnostics link remains present even when start and stop controls are
  unavailable.
- The diagnostics link keeps `href="#diagnostics"`.
- `Capturing` is shown only when the validated status says `capturing` and
  the capture payload says `capture.running`.
- `Ready to start` or `Stopped` controls are shown only when the payload is not
  running and the relevant `start_allowed` value is true.
- `blocked`, `failed`, `crashed`, `stale`, `degraded`, `unknown`,
  `unavailable`, missing, malformed, or contradictory states fail closed to a
  disabled blocked/pending/review state.
- A status of `capturing` with `capture.running: false` must fail closed.
- A status of `ready_to_start` or `stopped` with `capture.running: true` must
  fail closed.
- A stale state must not expose a restart instruction or restart button from
  backend blurb text in the dashboard tile.
- The frontend must not invent score text, current-match score text, exact
  parser truth, or strategic readiness from live-capture diagnostics.

## Preserved Diagnostics Route Invariants

A later implementation must preserve diagnostics behavior:

- The diagnostics route continues to render `Live Capture Control`.
- The diagnostics route continues to render the explicit start/stop controls
  only when current validated payload permissions allow them.
- The diagnostics route must not add reset, delete, wipe, restart, clear,
  repair, or force controls.
- The diagnostics route must not expose raw backend stack traces, raw log
  content, private file paths, or source snippets.
- The read-only live diagnostics summary remains read-only and public-safe.

## Error And Fail-Closed Behavior

Malformed, missing, stale, contradictory, blocked, failed, crashed, degraded,
unknown, unavailable, or ownership-ambiguous live-capture state must fail
closed.

Fail-closed means:

- no start control unless `capture.start_allowed` is true and the current state
  is not submitting;
- no stop control unless `capture.stop_allowed` is true and the current state
  is not submitting;
- no restart/repair/destructive control;
- dashboard links route the operator to diagnostics;
- display text remains symbolic and public-safe;
- no raw private values are echoed;
- no frontend claim says capture is safe, ready, reliable, or parser-truthful.

## ARS And Refactor Evidence Status

```yaml
prior_app_shell_evidence_found: "yes_background_only"
prior_exact_live_capture_controls_evidence_found: "not_verified_in_this_contract"
reviewed_scope: "frontend_live_capture_controls"
reviewed_commit: "10cd9820926786b33a7a64596753001ed303dffb"
evidence_status: "fresh_scoped_evidence_or_owner_exception_required_before_implementation"
fresh_scoped_evidence_needed_before_codex_c: true
owner_exception_allowed_before_codex_c: true
```

Prior app-shell evidence may inform review, but it is not enough by itself to
authorize implementation of this live-capture-controls slice. Before Codex C
may implement this split, one of these must exist:

1. fresh scoped ARS or Refactor Scout evidence for
   `frontend_live_capture_controls` at the exact target commit; or
2. an explicit issue-scoped owner exception that names:
   - issue #708;
   - candidate id `frontend_live_capture_controls`;
   - target commit `10cd9820926786b33a7a64596753001ed303dffb` or a newer exact
     commit;
   - allowed first-pass extraction surface;
   - forbidden behavior changes;
   - required validation commands;
   - false-authority flags.

An owner exception is implementation-routing authority only for the named slice.
It is not ARS clearance, Refactor Scout clearance, readiness, reliability
readiness, parser truth, security assurance, or privacy assurance.

## Decomposition Decision Packet

```yaml
candidate_id: "frontend_live_capture_controls"
candidate_surface_class: "mixed_frontend_runtime_control_surface"
candidate_surface_kind: "frontend_live_capture_controls_surface"
current_path: "frontend/src/App.tsx"
current_target_commit: "10cd9820926786b33a7a64596753001ed303dffb"
truth_or_authority_owner: "Local App / UI owns display and explicit control composition only; backend and parser remain upstream truth or runtime owners."
protected_surface_contact: "mixed_review_required"
proposed_destination: "same_repo_private_frontend_module_behind_frontend_src_App_tsx_facade"
first_pass_allowed_scope_after_review: "pure_components_and_display_helpers_only"
second_pass_requires_new_scope: "async_fetch_effects_start_stop_handlers_or_controller_hook"
why_not_keep_local: "App.tsx still mixes live-capture controls, safe status projection, diagnostics link placement, and dashboard action selection with the broader app shell."
why_not_move_to_existing_repo: "The controls are tightly coupled to Mythic Edge local-app frontend state, route placement, injected API helpers, and App.tsx tests."
why_not_create_new_repo: "No stable independently versioned live-capture UI API exists; cross-repo extraction would increase coordination risk."
new_public_interface_needed: "private_same_repo_only"
new_public_interface_description: "Preserve frontend/src/App.tsx, SetupStatusApp exports, SetupStatusAppProps behavior, route/hash behavior, visible controls, aria labels, diagnostics link, start/stop helper injection, and safe-display semantics."
rollback_plan: "Keep App.tsx as the public facade so a later private-module extraction can be reverted by moving the private code back behind the same exports."
ars_refactor_evidence_status: "fresh_scoped_evidence_or_owner_exception_required_before_implementation"
final_decision: "contract_ready_for_review"
```

## Non-Claims

Required non-claims for later handoff or implementation:

- `not_implementation_authority`
- `not_file_move_authority`
- `not_frontend_behavior_change`
- `not_route_hash_behavior_change`
- `not_visible_control_change`
- `not_api_payload_change`
- `not_api_endpoint_change`
- `not_request_guard_change`
- `not_live_capture_behavior_change`
- `not_backend_route_change`
- `not_parser_behavior_change`
- `not_parser_truth_ownership_change`
- `not_workbook_webhook_change`
- `not_apps_script_change`
- `not_ci_change`
- `not_ars_clearance`
- `not_refactor_scout_clearance`
- `not_readiness`
- `not_reliability_readiness`
- `not_parser_truth`
- `not_analytics_truth`
- `not_ai_truth`
- `not_coaching_truth`
- `not_security_assurance`
- `not_privacy_assurance`

## Tests Required For Later Implementation

Minimum future implementation validation:

```bash
npm --prefix frontend test -- --run src/App.test.tsx
npm --prefix frontend test -- --run src/api.test.ts
npm --prefix frontend run typecheck
printf '%s\n' frontend/src/App.tsx frontend/src/App.test.tsx frontend/src/api.ts frontend/src/types.ts | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' frontend/src/App.tsx frontend/src/App.test.tsx frontend/src/api.ts frontend/src/types.ts | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

Additional validation is required if the later implementation touches backend
routes, live-capture runtime code, parser contact, shared TypeScript types, or
test builders:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_live_app_explicit_start_capture_control.py tests/test_live_app_mtga_process_lifecycle.py tests/test_analytics_local_app_backend.py
```

## Acceptance Criteria

- This packet identifies `frontend_live_capture_controls` as the issue #708
  candidate.
- This packet preserves same-repo-first decomposition and rejects cross-repo
  extraction.
- This packet recommends a first pass limited to pure control components and
  display helpers.
- This packet defers async fetch effects, start/stop handlers, and controller
  hooks unless a later implementation scope explicitly includes them.
- This packet preserves `frontend/src/App.tsx` as the public facade.
- This packet preserves `SetupStatusApp`, `SetupStatusAppProps`, route/hash
  behavior, dashboard placement, diagnostics placement, visible labels, aria
  labels, and injected API helper behavior.
- This packet preserves fail-closed behavior for unavailable, stale,
  malformed, contradictory, blocked, failed, crashed, degraded, unknown, and
  ownership-ambiguous states.
- This packet does not authorize implementation, file movement, behavior
  changes, API payload changes, backend route changes, parser changes,
  workbook/webhook/Apps Script changes, CI changes, ARS/Refactor execution,
  private evidence reads, readiness claims, truth claims, or assurance claims.

## Stop Conditions

Stop and route back to Codex B, Codex A, or the owner if any later request
would:

- change route/hash behavior;
- rename or remove visible live-capture controls;
- change labels, aria labels, disabled states, or diagnostics link behavior;
- add restart, repair, reset, delete, wipe, clear, force, or destructive
  controls;
- call start or stop outside the injected/default API helper boundary;
- change API endpoint paths, request guards, payload validators, or type
  constants;
- change backend route behavior or live-capture runtime semantics;
- change parser behavior, parser truth ownership, parser event classes, match
  identity, game identity, deduplication, or final reconciliation;
- expose raw logs, private paths, source snippets, runtime status files,
  secrets, credentials, tokens, API keys, or webhook URLs;
- run ARS or Refactor Scout without a separate authorized issue;
- claim readiness, reliability readiness, parser truth, security assurance, or
  privacy assurance.

## Recommended Next Role

Recommended next role: Codex E contract reviewer.

Codex E should review whether this packet:

- correctly narrows issue #708 to live-capture controls;
- preserves `frontend/src/App.tsx` as the stable facade;
- keeps async effects and start/stop handlers out of the first-pass extraction
  unless explicitly routed later;
- preserves current UI, accessibility, route, API, and fail-closed invariants;
- requires fresh scoped ARS/Refactor evidence or explicit owner exception
  before implementation;
- avoids false implementation authority and readiness/truth/assurance claims.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Contract Reviewer for Mythic-Edge issue #708.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/708

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Target artifact:
docs/contracts/core_frontend_app_shell_live_capture_controls_decomposition_decision_packet.md

Review goal:
Review the frontend app shell live-capture controls decomposition decision
packet. Confirm whether it preserves same-repo-first decomposition, keeps
frontend/src/App.tsx as the facade, limits the first future split to pure
components/display helpers, preserves visible controls, route/hash behavior,
API helper boundaries, start/stop semantics, fail-closed states, and no-echo
privacy boundaries, and requires fresh scoped ARS/Refactor evidence or an
explicit owner exception before Codex C.

Protected boundaries:
Do not implement code, move files, open a PR, change frontend behavior,
route/hash behavior, visible controls, API payloads, live-capture behavior,
backend routes, parser behavior, workbook/webhook/Apps Script behavior, CI,
readiness claims, parser truth claims, security assurance, or privacy
assurance.

Expected output:
Findings first, verdict, validation run, remaining risks, recommended next
role, and workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/708"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  source_decision_packet: "https://github.com/Tahjali11/Mythic-Edge/issues/697"
  latest_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/706"
  latest_completed_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/707"
  latest_merge_commit: "10cd9820926786b33a7a64596753001ed303dffb"
  completed_thread: "B"
  next_thread: "E"
  verdict: "frontend_live_capture_controls_decomposition_contract_ready_for_review"
  candidate_id: "frontend_live_capture_controls"
  candidate_surface: "frontend/src/App.tsx"
  candidate_surface_class: "mixed_frontend_runtime_control_surface"
  target_artifact: "docs/contracts/core_frontend_app_shell_live_capture_controls_decomposition_decision_packet.md"
  implementation_authorized: false
  file_move_authorized: false
  same_repo_decomposition_authorized: false
  cross_repo_extraction_authorized: false
  frontend_behavior_change_authorized: false
  route_hash_behavior_change_authorized: false
  visible_control_change_authorized: false
  api_payload_change_authorized: false
  live_capture_behavior_change_authorized: false
  backend_route_change_authorized: false
  parser_behavior_change_authorized: false
  workbook_webhook_change_authorized: false
  apps_script_change_authorized: false
  ci_change_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  fresh_scoped_evidence_or_owner_exception_required_before_codex_c: true
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
