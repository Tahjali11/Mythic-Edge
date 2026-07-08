# Core Frontend App Shell Live-Capture Controls Decomposition Comparison

## Role

Codex C - Module Implementer.

## Source Artifacts

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/708>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Decomposition tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/463>
- Contract: `docs/contracts/core_frontend_app_shell_live_capture_controls_decomposition_decision_packet.md`
- Fresh scoped evidence: <https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/153>
- Target commit: `76c1cb499e9ca5b1e74c828ac91d67a5a4b5defe`

## Implementation Summary

Implemented the approved first-pass same-repo decomposition for
`frontend_live_capture_controls`.

The public facade remains `frontend/src/App.tsx`. State ownership, async
effects, injected API helper props, and start/stop handlers remain in
`App.tsx`. Pure live-capture control components, action selection, status
projection helpers, compact display text, and control-message helpers moved to
the private frontend module:

`frontend/src/app_live_capture_controls.tsx`

`LiveCaptureControlPanel` receives the existing `StatusPill` component from
`App.tsx`, so the shared status pill markup and classes remain owned by the
facade and render the same UI.

## Contract Comparison

Implemented:

- Extracted `LiveCaptureControlState` as a private same-repo type imported by
  `App.tsx`.
- Extracted `DashboardLiveCaptureControl`.
- Extracted `LiveCaptureControlPanel`.
- Extracted live-capture action selection and blocked/pending control helpers.
- Extracted `liveCaptureControlPayload`.
- Extracted `liveCaptureDashboardStatus` and `liveCaptureDashboardDetail`.
- Extracted `liveCaptureControlMessage`.
- Extracted compact live-capture display text helper.

Preserved in `App.tsx`:

- `SetupStatusApp` named export and default export.
- `SetupStatusAppProps`, including `fetchLiveDiagnostics`,
  `fetchLiveCapture`, `startCapture`, and `stopCapture`.
- Route/hash behavior.
- Dashboard and diagnostics placement.
- Live diagnostics state.
- Live-capture control state ownership.
- Async fetch effects.
- `handleStartCapture`.
- `handleStopCapture`.
- API helper imports and injected/default helper boundaries.

Not changed:

- visible labels, aria labels, links, hrefs, disabled states, or CSS class
  names;
- route/hash values or fallback behavior;
- API payload shape or endpoint paths;
- backend live-capture runtime behavior;
- parser behavior, workbook/webhook behavior, Apps Script behavior, or CI.

## Behavior Preservation Evidence

The focused App/API test suite passed after extraction:

```text
npm --prefix frontend test -- --run src/App.test.tsx src/api.test.ts

Test Files  2 passed (2)
Tests       96 passed (96)
```

TypeScript typecheck passed:

```text
npm --prefix frontend run typecheck
```

The first focused test attempt failed because local `frontend/node_modules`
was absent and `vitest` was not installed. `npm --prefix frontend ci` restored
dependencies from the committed lockfile; it reported two high-severity audit
findings in the dependency tree. No dependency files were changed by this
implementation.

## Validation Run

- `git status --short --branch`: passed before implementation; primary checkout
  was dirty/detached, so work continued in a clean issue worktree.
- `git fetch --prune`: passed.
- `gh issue view 708 --repo Tahjali11/Mythic-Edge --json number,title,state,url,body`: passed; issue #708 is closed as the contract issue.
- `gh issue view 568 --repo Tahjali11/Mythic-Edge --json number,title,state,url`: passed; tracker #568 is open.
- `npm --prefix frontend ci`: passed; restored local frontend dependencies.
- `npm --prefix frontend test -- --run src/App.test.tsx src/api.test.ts`: passed, 96 tests.
- `npm --prefix frontend run typecheck`: passed.
- `printf '%s\n' frontend/src/App.tsx frontend/src/app_live_capture_controls.tsx | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`: passed.
- `printf '%s\n' frontend/src/App.tsx frontend/src/app_live_capture_controls.tsx | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`: passed.
- `printf '%s\n' frontend/src/App.tsx frontend/src/app_live_capture_controls.tsx docs/implementation_handoffs/core_frontend_app_shell_live_capture_controls_decomposition_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`: passed.
- `printf '%s\n' frontend/src/App.tsx frontend/src/app_live_capture_controls.tsx docs/implementation_handoffs/core_frontend_app_shell_live_capture_controls_decomposition_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`: passed.
- `python3 tools/check_secret_patterns.py --all`: ran and reported existing repo-wide forbidden/warning findings outside this change set.
- `python3 tools/check_protected_surfaces.py --base origin/main`: passed; because this pass has uncommitted work, the path-scoped check above is the changed-file evidence.
- `python3 tools/check_agent_docs.py`: passed.
- `git diff --check`: passed.

## Remaining Risks And Non-Claims

- This is a behavior-preserving same-repo decomposition only.
- Async fetch effects, start/stop handlers, and controller-hook extraction were
  not performed.
- No frontend behavior change, live-capture runtime behavior change, API
  payload change, backend route change, parser behavior change, workbook/webhook
  change, Apps Script change, or CI change is claimed.
- No readiness, reliability-readiness, parser-truth, security-assurance, or
  privacy-assurance claim is made.
- `npm ci` reported existing dependency audit warnings; audit remediation was
  outside this issue.

## Recommended Next Role

Codex E should review the diff against issue #708, the contract, the scoped
owner approval, and this implementation handoff.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge issue #708.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/708

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Contract:
docs/contracts/core_frontend_app_shell_live_capture_controls_decomposition_decision_packet.md

Implementation handoff:
docs/implementation_handoffs/core_frontend_app_shell_live_capture_controls_decomposition_comparison.md

Review goal:
Review the behavior-preserving same-repo extraction of pure live-capture
control components and display helpers from frontend/src/App.tsx into
frontend/src/app_live_capture_controls.tsx.

Protected boundaries:
Do not change code in review mode. Verify no async fetch effects, start/stop
handlers, controller-hook logic, frontend behavior, route/hash behavior,
visible controls, API payloads, backend routes, live-capture runtime behavior,
parser behavior, workbook/webhook/Apps Script behavior, CI behavior,
readiness claims, reliability-readiness claims, parser-truth claims, security
assurance, or privacy assurance were introduced.

Expected output:
Findings first, behavior-preservation verdict, validation review, remaining
risk, recommended next role, and workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/708"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  evidence_issue: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/153"
  completed_thread: "C"
  next_thread: "E"
  verdict: "frontend_live_capture_controls_behavior_preserving_extraction_ready_for_review"
  candidate_id: "frontend_live_capture_controls"
  candidate_surface: "frontend/src/App.tsx"
  target_commit: "76c1cb499e9ca5b1e74c828ac91d67a5a4b5defe"
  branch: "codex/frontend-live-capture-controls-implementation-708"
  contract: "docs/contracts/core_frontend_app_shell_live_capture_controls_decomposition_decision_packet.md"
  implementation_handoff: "docs/implementation_handoffs/core_frontend_app_shell_live_capture_controls_decomposition_comparison.md"
  extracted_module: "frontend/src/app_live_capture_controls.tsx"
  same_repo_decomposition_performed: true
  frontend_behavior_change_authorized: false
  frontend_behavior_changed: false
  async_fetch_effect_extraction_performed: false
  start_stop_handler_extraction_performed: false
  controller_hook_extraction_performed: false
  route_hash_behavior_change_authorized: false
  api_payload_change_authorized: false
  backend_route_change_authorized: false
  live_capture_runtime_behavior_change_authorized: false
  parser_behavior_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
