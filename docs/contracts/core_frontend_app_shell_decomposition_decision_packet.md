# Core Frontend App Shell Decomposition Decision Packet

Status: Draft contract for review

Role: Codex B - Module Contract Writer

Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/697>

Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>

Source decision issue: <https://github.com/Tahjali11/Mythic-Edge/issues/693>

Latest completed child: <https://github.com/Tahjali11/Mythic-Edge/issues/695>

Latest completed PR: <https://github.com/Tahjali11/Mythic-Edge/pull/696>

Latest merge commit: `19df0d7d5e94cf1f09aaf8ccfe1ceb3a69062548`

Target artifact:
`docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md`

## Module

`core_frontend_app_shell_decomposition_decision_packet`

This contract is the Phase 5 decomposition decision packet for the
`frontend/src/App.tsx` app shell after the frontend API client boundary work
from issue #695.

Plain English: `frontend/src/App.tsx` is the large React app shell. It owns the
visible local app composition, route/hash behavior, dashboard panels,
analytics refresh state, live-capture controls, diagnostics, privacy, manual
import, feedback, and Match Journal UI state. This packet decides what a later
behavior-preserving split may touch and what it must preserve before any
implementation is considered.

This contract is planning-only. It does not implement code, move files, open a
PR, run ARS, run Refactor Scout, read private logs, change frontend behavior,
change route/hash behavior, change API payloads, change live-capture behavior,
change backend routes, change parser behavior or parser truth ownership,
change workbook/webhook/Apps Script behavior, change CI, or claim readiness,
security assurance, privacy assurance, reliability readiness, parser truth,
analytics truth, AI truth, coaching truth, release readiness, deploy readiness,
or production readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: <https://github.com/Tahjali11/Mythic-Edge>
- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/697>
- Project roadmap / tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Broad decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>
- Source API/frontend/live-capture decision packet:
  <https://github.com/Tahjali11/Mythic-Edge/issues/693>
- Source decision packet PR: <https://github.com/Tahjali11/Mythic-Edge/pull/694>
- Latest completed child: <https://github.com/Tahjali11/Mythic-Edge/issues/695>
- Latest completed PR: <https://github.com/Tahjali11/Mythic-Edge/pull/696>
- Latest merge commit: `19df0d7d5e94cf1f09aaf8ccfe1ceb3a69062548`

## Source Artifacts Inspected

- GitHub issue #697
- GitHub PR #696
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
- `docs/contracts/core_api_frontend_live_capture_decomposition_decision_packet.md`
- `docs/implementation_handoffs/core_frontend_api_client_boundary_decomposition_comparison.md`
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

`frontend/src/App.tsx` owns the React app shell and visible local-app
orchestration. It consumes setup, analytics, Match Journal, manual import,
feedback, diagnostics, and live-capture payloads through the frontend API
client. It does not own parser facts, backend route truth, API payload shape,
live-capture runtime behavior, workbook schema, webhook payload shape, Apps
Script behavior, or deployment behavior.

## Internal Project Area

Local App / UI, with read-only contact to parser-owned and backend-owned
facts through the frontend API client.

This contract keeps parser state, backend route binding, live-capture control,
workbook/transport, and Apps Script surfaces out of scope.

## Truth Owner

- Parser and state code own parser-managed match, game, card, event, identity,
  deduplication, and final reconciliation facts.
- Backend/local-app route handlers own backend payload production and local
  live-capture runtime behavior.
- `frontend/src/api.ts` and its private helper modules own browser-side
  endpoint helpers, request guard use, payload validation, and safe API error
  mapping.
- `frontend/src/types.ts` owns TypeScript payload constants and type shapes
  consumed by the frontend.
- `frontend/src/App.tsx` owns React composition, local UI state, route/hash
  behavior, safe display labels, control rendering, and form orchestration.
- Repo governance docs, accepted ADRs, active issues, reviewed contracts,
  reviewed PRs, and deployer-recorded merge evidence own workflow authority.

The app shell must remain a display and explicit-control surface. It must not
become a truth owner for parser facts, API payload schemas, backend route
contracts, live-capture lifecycle semantics, workbook/webhook behavior, or
strategic analytics truth.

## Bridge-Code Status

`bridge_code`

Source internal project area: Local App / UI.

Contacted areas:

- frontend API client, because `SetupStatusApp` receives default API helper
  functions and test-injected replacements;
- local app backend, because the displayed payloads originate from backend
  routes;
- parser runtime, because live-capture and analytics displays consume
  parser-owned facts;
- local analytics and Match Journal surfaces, because the app shell renders
  read-only local projections and journal interactions.

Allowed data flow:

```text
parser-owned facts and backend-owned local status
  -> backend route payloads
  -> frontend API validators
  -> React app shell display, routing, and explicit operator controls
```

Forbidden reverse flow:

```text
React route state, display labels, control labels, form text, or dashboard
preferences
  -/-> parser truth
  -/-> backend route truth
  -/-> API payload shape
  -/-> live-capture runtime semantics
  -/-> workbook, webhook, or Apps Script truth
```

## Files Owned By This Contract

- `docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md`

Files referenced but not owned:

- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `frontend/src/api.ts`
- `frontend/src/api/*`
- `frontend/src/types.ts`
- `frontend/package.json`

## Authorization State

The following flags are false for this contract:

```yaml
implementation_authorized: false
file_move_authorized: false
same_repo_decomposition_authorized: false
cross_repo_extraction_authorized: false
frontend_behavior_change_authorized: false
route_hash_behavior_change_authorized: false
api_payload_change_authorized: false
api_endpoint_change_authorized: false
request_guard_change_authorized: false
validator_behavior_change_authorized: false
live_capture_behavior_change_authorized: false
live_capture_status_schema_change_authorized: false
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

Any future handoff, review, implementation plan, or validator output that flips
one of these flags without a separate reviewed issue and explicit owner
approval must fail closed.

## Schema Vocabulary Reconciliation

This packet consumes the Phase 5 decision-packet shape from
`docs/contracts/core_governance_report_helper_phase_5_decomposition_decision_packet.md`
where that shared shape applies.

Canonical shared values:

- `packet_schema` remains
  `core_governance_report_helper_phase_5_decomposition_decision_packet.v1`.
- `candidate_surface_class` uses `mixed_governance_runtime_surface` because
  the shared #665 schema does not define a dedicated frontend app shell class.
- `candidate_surface_kind` may use the issue-local value
  `frontend_app_shell_surface`.
- `final_decision` uses the #665 decision vocabulary.
- `ars_refactor_evidence_status` and `non_claims` are required in every
  canonical candidate row.
- Same-repo decomposition may be preferred as a future route, but preference
  is not implementation authority.
- Cross-repo extraction remains rejected for this app shell.

Issue-local `candidate_surface_kind` values allowed by this packet:

- `frontend_app_shell_surface`
- `frontend_route_shell_surface`
- `frontend_dashboard_composition_surface`
- `frontend_live_capture_controls_surface`
- `frontend_manual_import_composition_surface`
- `frontend_feedback_journal_composition_surface`
- `frontend_privacy_diagnostics_composition_surface`

## Packet Envelope

```yaml
packet_schema: "core_governance_report_helper_phase_5_decomposition_decision_packet.v1"
repository: "Tahjali11/Mythic-Edge"
repository_url: "https://github.com/Tahjali11/Mythic-Edge"
issue: "https://github.com/Tahjali11/Mythic-Edge/issues/697"
tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
source_decision_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/693"
latest_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/695"
latest_completed_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/696"
latest_merge_commit: "19df0d7d5e94cf1f09aaf8ccfe1ceb3a69062548"
target_commit: "19df0d7d5e94cf1f09aaf8ccfe1ceb3a69062548"
candidate_scope: "frontend_app_shell"
candidate_id: "frontend_app_shell"
candidate_surface_class: "mixed_governance_runtime_surface"
candidate_surface_kind: "frontend_app_shell_surface"
current_path: "frontend/src/App.tsx"
target_artifact: "docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md"
source_api_client_boundary_completed: true
parser_state_deferred: true
final_decision: "request_fresh_ars_refactor_evidence"
implementation_authorized: false
file_move_authorized: false
same_repo_decomposition_authorized: false
cross_repo_extraction_authorized: false
frontend_behavior_change_authorized: false
api_payload_change_authorized: false
live_capture_behavior_change_authorized: false
parser_behavior_change_authorized: false
workbook_webhook_change_authorized: false
ci_change_authorized: false
readiness_claimed: false
security_assurance_claimed: false
privacy_assurance_claimed: false
parser_truth_claimed: false
```

## Observed Current Behavior

At the reviewed baseline, `frontend/src/App.tsx` is about 5,984 lines. It:

- exports `SetupStatusApp` and default-exports the same component;
- defines `SetupStatusAppProps` for dependency injection in tests and local
  app usage;
- imports API helpers, safe display helpers, and TypeScript payload contracts;
- owns `AppRoute`, route lists, rail items, and `window.location.hash`
  interpretation through `readAppRouteFromHash`;
- owns load states for setup, analytics history, early-game history, action
  review, split review, dashboard modules, analytics auto-refresh, live
  diagnostics, live-capture control, Match Journal, manual import, upload, and
  error-report workflows;
- polls sanitized analytics refresh state and reloads existing analytics views
  when the backend revision changes;
- renders dashboard, coach, analytics, review, feedback, import, privacy, and
  diagnostics routes;
- renders a persistent dashboard live-capture control and a detailed
  diagnostics live-capture control panel;
- calls `startCapture` and `stopCapture` only through injected or default API
  helpers;
- fails closed when live capture is unavailable, stale, malformed,
  ownership-blocked, or contradictory;
- renders safe redacted placeholders and no-echo display labels for private or
  unsafe values;
- stores only local dashboard module view preferences and the synthetic Match
  Journal smoke-note id in browser storage.

`frontend/src/App.test.tsx` is about 3,817 lines and already covers the broad
shell behavior, including dashboard rendering, route fallback, active rail
items, live-capture start/stop UI, stale and blocked capture states, safe
backend blurb display, privacy/no-echo checks, analytics auto-refresh, Match
Journal rendering, manual import behavior, and error-report flows.

## Problem Statement And First Bad Values

The intended behavior is a small, reviewable decision packet before any future
split of the React app shell.

The first bad value is treating this packet as implementation authority.

The second bad value is treating the completed `frontend/src/api.ts` boundary
work as broad clearance to split `frontend/src/App.tsx`. That completed work
reduced API-client risk; it did not prove app-shell safety.

The third bad value is changing route/hash behavior, visible copy, aria labels,
control enablement, storage keys, polling cadence, form submission behavior, or
safe display/no-echo behavior while calling the work a pure decomposition.

The fourth bad value is letting app-shell state become parser truth or backend
payload truth.

The fifth bad value is splitting the whole app shell into many modules in one
implementation issue. Future work should prefer small coherent slices.

The sixth bad value is cross-repo extraction. Local App / UI remains in the
primary repository by ADR-0006 default and depends on repo-local backend,
parser, and frontend contracts.

## Scope Decision

Decision: `request_fresh_ars_refactor_evidence`

Same-repo decomposition is the preferred future direction for
`frontend/src/App.tsx`, but this packet does not authorize implementation or
file movement. Before Codex C may implement a split, one of these must exist:

1. fresh scoped ARS or Refactor Scout evidence for `frontend/src/App.tsx`; or
2. an explicit issue-scoped owner exception that names this candidate, target
   commit, allowed slice, validation plan, and false-authority flags.

If implementation is later authorized, it should keep `frontend/src/App.tsx`
as the stable public facade at first. Private same-repo modules or component
families may sit behind that facade only when they preserve current imports,
props, rendered behavior, route behavior, storage behavior, safe-display
behavior, and tests.

Cross-repo extraction is rejected. A new package or sibling repo would add
versioning and coordination risk without a stable independent public API.

## Candidate Boundary Summary

This table is a planning summary. It is not implementation authority.

| candidate_id | candidate_surface_class | candidate_surface_kind | current_path | final_decision |
| --- | --- | --- | --- | --- |
| `frontend_app_shell` | `mixed_governance_runtime_surface` | `frontend_app_shell_surface` | `frontend/src/App.tsx` | `request_fresh_ars_refactor_evidence` |
| `frontend_route_shell` | `mixed_governance_runtime_surface` | `frontend_route_shell_surface` | `frontend/src/App.tsx` private route/hash logic | `defer` |
| `frontend_dashboard_composition` | `mixed_governance_runtime_surface` | `frontend_dashboard_composition_surface` | `frontend/src/App.tsx` dashboard composition | `defer` |
| `frontend_live_capture_controls` | `mixed_governance_runtime_surface` | `frontend_live_capture_controls_surface` | `frontend/src/App.tsx` live-capture UI controls | `defer` |
| `frontend_manual_import_composition` | `mixed_governance_runtime_surface` | `frontend_manual_import_composition_surface` | `frontend/src/App.tsx` manual import UI | `defer` |
| `frontend_feedback_journal_composition` | `mixed_governance_runtime_surface` | `frontend_feedback_journal_composition_surface` | `frontend/src/App.tsx` feedback and journal UI | `defer` |
| `frontend_privacy_diagnostics_composition` | `mixed_governance_runtime_surface` | `frontend_privacy_diagnostics_composition_surface` | `frontend/src/App.tsx` privacy and diagnostics UI | `defer` |

## Canonical Candidate Row

```yaml
candidate_id: "frontend_app_shell"
candidate_surface_class: "mixed_governance_runtime_surface"
candidate_surface_kind: "frontend_app_shell_surface"
current_path: "frontend/src/App.tsx"
current_behavior: "Owns the React local app shell, SetupStatusApp facade, route/hash handling, dashboard and analytics composition, live-capture UI controls, manual import, Match Journal, feedback, diagnostics, privacy, local UI state, safe labels, and form orchestration."
truth_or_authority_owner: "Local App / UI owns display and explicit control composition only; parser, backend, API client, and type contracts remain upstream truth or payload authorities."
upstream_dependencies:
  - "frontend/src/api.ts"
  - "frontend/src/api/*"
  - "frontend/src/status.ts"
  - "frontend/src/types.ts"
  - "src/mythic_edge_parser/local_app/backend.py"
  - "src/mythic_edge_parser/local_app/live_capture_control.py"
  - "parser-owned facts consumed through backend/API payloads"
downstream_consumers:
  - "frontend/src/main.tsx"
  - "frontend/src/App.test.tsx"
  - "manual local app operator workflow"
  - "local dashboard, analytics, review, feedback, import, diagnostics, and privacy routes"
protected_surface_contact: "mixed_review_required"
proposed_destination: "same_repo_private_modules_behind_frontend_src_App_tsx_facade"
why_not_keep_local: "The app shell is large and mixes route, state loading, display composition, safe labels, live-capture controls, manual import, journal, feedback, privacy, and diagnostics logic; a later same-repo split may reduce review risk."
why_not_move_to_existing_repo: "The app shell is repo-local UI orchestration tied to Mythic Edge backend, parser-owned facts, frontend types, and tests."
why_not_create_new_repo: "No stable independently versioned app-shell API exists; extraction would increase coordination risk and would not improve behavior preservation."
new_public_interface_needed: "private_same_repo"
new_public_interface_description: "Preserve frontend/src/App.tsx, the named SetupStatusApp export, the default export, SetupStatusAppProps behavior, route/hash behavior, visible controls, aria labels, storage keys, and safe-display semantics. Private modules may be introduced only behind the facade after authorization."
behavior_preservation_tests:
  - "npm --prefix frontend test -- --run src/App.test.tsx src/api.test.ts"
  - "npm --prefix frontend run typecheck"
  - "printf '%s\\n' docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
  - "python3 tools/check_protected_surfaces.py --base origin/main"
  - "git diff --check"
rollback_plan: "A later implementation must keep frontend/src/App.tsx as the facade so private module extraction can be reverted by collapsing the private code back behind the same exports without changing behavior."
ars_refactor_evidence_status: "fresh_scoped_evidence_required_before_implementation"
non_claims:
  - "not_implementation_authority"
  - "not_file_move_authority"
  - "not_frontend_behavior_change"
  - "not_route_hash_behavior_change"
  - "not_api_payload_change"
  - "not_api_endpoint_change"
  - "not_request_guard_change"
  - "not_validator_behavior_change"
  - "not_live_capture_behavior_change"
  - "not_backend_route_change"
  - "not_parser_behavior_change"
  - "not_parser_truth_ownership_change"
  - "not_workbook_webhook_change"
  - "not_apps_script_change"
  - "not_ci_change"
  - "not_ars_clearance"
  - "not_refactor_scout_clearance"
  - "not_readiness"
  - "not_reliability_readiness"
  - "not_parser_truth"
  - "not_analytics_truth"
  - "not_ai_truth"
  - "not_coaching_truth"
  - "not_security_assurance"
  - "not_privacy_assurance"
final_decision: "request_fresh_ars_refactor_evidence"
```

## Future Same-Repo Slice Preferences

If a later issue authorizes implementation, the preferred first slice is the
smallest coherent extraction that reduces app-shell size without changing
behavior. The likely safe order is:

1. route shell and static rail metadata behind the `frontend/src/App.tsx`
   facade;
2. pure display components that already receive complete props and do not call
   API helpers directly;
3. local state hooks for analytics refresh or dashboard module preferences,
   only after route/display extraction is reviewed;
4. live-capture controls last among frontend slices, because they are
   user-facing explicit controls backed by backend runtime state.

This ordering is guidance only. It does not authorize any slice.

## Public Interfaces To Preserve

A later implementation child must preserve:

- `frontend/src/App.tsx` import path;
- named `SetupStatusApp` export;
- default `SetupStatusApp` export;
- `SetupStatusAppProps` dependency-injection behavior used by tests;
- route/hash vocabulary:
  `dashboard`, `coach`, `analytics`, `review`, `privacy`, `feedback`,
  `import`, and `diagnostics`;
- fallback to `dashboard` for unknown hash routes;
- left rail labels and active route semantics;
- dashboard, analytics, review, feedback, import, privacy, diagnostics, and
  coach route visibility semantics;
- dashboard module view preference storage key:
  `mythic_edge.analytics.dashboard.module_view_preferences.v1`;
- Match Journal unattached smoke-note storage key:
  `mythic_edge.match_journal.unattached_smoke_note_id`;
- analytics auto-refresh interval behavior and visibility pause behavior;
- start and stop live-capture calls through injected/default API helpers only;
- fail-closed rendering for stale, blocked, unavailable, malformed, or
  contradictory live-capture states;
- safe display placeholders and no-echo behavior for local paths, raw backend
  details, stack traces, private markers, raw hashes, credentials, tokens, API
  keys, webhook URLs, and raw log content;
- error-report preview-before-submit behavior and privacy guard display;
- manual import safe summaries and raw-path clearing behavior.

## Invariants

- Parser facts remain parser-owned.
- Backend routes and API payload contracts remain upstream of the app shell.
- The app shell may display, hide, downgrade, or label facts; it must not
  invent parser truth or backend payload truth.
- Route/hash behavior is user-visible behavior and must not drift during a
  decomposition.
- Local storage keys and value meanings must not drift during a decomposition.
- API helper calls must remain dependency-injected through `SetupStatusApp`
  props or default helpers from `frontend/src/api.ts`.
- Start and stop remain explicit operator controls.
- Live-capture controls must remain fail-closed for stale, blocked,
  unavailable, malformed, or contradictory states.
- Private and unsafe values must be rendered as public-safe placeholders,
  symbolic categories, or not rendered at all.
- Frontend behavior, API payload shape, backend route behavior, live-capture
  behavior, parser behavior, workbook/webhook behavior, Apps Script behavior,
  CI, deployment, release, and production behavior remain unchanged.

## Error Behavior

Contract ambiguity must fail closed to Codex B or Codex E review.

Future implementation proposals must fail closed if they:

- remove or rename the `frontend/src/App.tsx` public facade;
- remove or rename the named/default `SetupStatusApp` exports;
- change route/hash values, fallback behavior, rail labels, or route
  visibility;
- change visible control enablement, aria labels, or live-capture start/stop
  gating;
- change API endpoint paths, HTTP methods, request guard behavior, schema
  constants, object names, or validators;
- change backend route binding or live-capture runtime behavior;
- weaken safe-display, redaction, no-echo, private-marker, or raw-path
  behavior;
- change browser storage keys or stored value meanings;
- treat tests, owner exception, ARS evidence, Refactor Scout evidence, or
  review acceptance as readiness, truth, security assurance, or privacy
  assurance;
- broaden into parser state, EventBus, backend route, workbook/webhook, Apps
  Script, CI, release, deploy, or production behavior.

## Behavior-Preservation Validation Plan

Docs-only validation for this contract:

```bash
printf '%s\n' docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
git diff --no-index --check -- /dev/null docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md
```

If the contract file is still untracked, `git diff --check` and
`check_protected_surfaces.py --base origin/main` may report no changed paths.
In that state, Codex B must rely on the direct secret-pattern stdin scan and
direct no-index new-file whitespace check for the new file body, and must say
that protected-surface validation becomes fully meaningful only after the file
is tracked or staged by a later submitter role.

Future implementation validation for an app-shell child should include at
minimum:

```bash
npm --prefix frontend test -- --run src/App.test.tsx src/api.test.ts
npm --prefix frontend run typecheck
printf '%s\n' frontend/src/App.tsx frontend/src/App.test.tsx | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --all
printf '%s\n' frontend/src/App.tsx frontend/src/App.test.tsx | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
```

Broader tests are required if a later implementation touches API helpers,
shared TypeScript types, backend route contracts, live-capture control wiring,
parser contacts, local analytics ingest, CSS, build configuration, or package
metadata.

## Acceptance Criteria

- This packet identifies `frontend/src/App.tsx` as the app-shell candidate.
- This packet preserves `frontend/src/App.tsx` as the public facade for any
  first future split.
- This packet records same-repo decomposition as the preferred future route,
  not current implementation authority.
- This packet rejects cross-repo extraction.
- This packet requires fresh scoped ARS/Refactor evidence or explicit
  issue-scoped owner exception before implementation.
- This packet includes a canonical candidate row with
  `ars_refactor_evidence_status` and `non_claims`.
- This packet preserves frontend behavior, route/hash behavior, API payload
  shape, backend route behavior, live-capture behavior, parser behavior,
  parser truth ownership, workbook/webhook behavior, Apps Script behavior, and
  CI boundaries.
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
- change frontend behavior, route/hash behavior, visible controls, storage
  semantics, safe labels, or no-echo behavior;
- change API payloads, endpoint paths, schema constants, object names, local
  request guard behavior, or validators;
- change backend route behavior or live-capture behavior;
- change parser behavior, parser truth ownership, parser event classes, match
  identity, game identity, deduplication, or final reconciliation;
- change workbook schema, webhook payloads, Apps Script behavior, CI,
  deployment, release, or production behavior;
- claim readiness, reliability readiness, parser truth, analytics truth, AI
  truth, coaching truth, security assurance, privacy assurance, release
  readiness, deploy readiness, or production readiness.

## Recommended Next Role

Recommended next role: Codex E contract reviewer for Mythic Edge issue #697.

Codex E should review whether this packet:

- preserves the #693 routing decision and #695 API-client boundary completion;
- correctly scopes `frontend/src/App.tsx` as a Local App / UI bridge surface;
- uses the shared Phase 5 decision vocabulary without inventing schema values;
- includes required `ars_refactor_evidence_status` and `non_claims`;
- keeps `frontend/src/App.tsx` as the stable facade for any first future split;
- requires fresh scoped ARS/Refactor evidence or explicit issue-scoped owner
  exception before implementation;
- preserves frontend/API/live-capture/parser/workbook/webhook/Apps Script/CI
  boundaries and non-claims.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Contract Reviewer for Mythic Edge issue #697.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/697

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Source decision issue:
https://github.com/Tahjali11/Mythic-Edge/issues/693

Latest completed child:
https://github.com/Tahjali11/Mythic-Edge/issues/695

Latest completed PR:
https://github.com/Tahjali11/Mythic-Edge/pull/696

Target artifact:
docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md

Review the frontend app shell Phase 5 decomposition decision packet. Confirm
whether it correctly scopes frontend/src/App.tsx as a high-risk Local App / UI
bridge surface, preserves frontend/src/App.tsx as the public facade, rejects
cross-repo extraction, uses accepted Phase 5 schema vocabulary, includes
ars_refactor_evidence_status and non_claims, requires fresh scoped ARS/Refactor
evidence or explicit issue-scoped owner exception before implementation, and
avoids implementation, file movement, behavior changes, route/hash changes,
API payload changes, live-capture changes, parser changes, private evidence
reads, CI changes, readiness claims, truth claims, and assurance claims.

Expected output:
Findings first, verdict, validation run, remaining risks, recommended next
role, and workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/697"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  source_decision_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/693"
  latest_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/695"
  latest_completed_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/696"
  latest_merge_commit: "19df0d7d5e94cf1f09aaf8ccfe1ceb3a69062548"
  completed_thread: "B"
  next_thread: "E"
  verdict: "frontend_app_shell_decomposition_decision_packet_ready_for_review"
  target_artifact: "docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md"
  decision: "request_fresh_ars_refactor_evidence"
  same_repo_decomposition_preferred_after_review: true
  fresh_scoped_ars_or_refactor_evidence_required_before_implementation: true
  implementation_authorized: false
  file_move_authorized: false
  same_repo_decomposition_authorized: false
  cross_repo_extraction_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  frontend_behavior_change_authorized: false
  route_hash_behavior_change_authorized: false
  api_payload_change_authorized: false
  live_capture_behavior_change_authorized: false
  backend_route_change_authorized: false
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
