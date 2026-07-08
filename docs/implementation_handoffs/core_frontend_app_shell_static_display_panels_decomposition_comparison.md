# Frontend App Shell Static Display Panels Decomposition Comparison

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/702>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker:
<https://github.com/Tahjali11/Mythic-Edge/issues/463>

Source decision packet:
<https://github.com/Tahjali11/Mythic-Edge/issues/697>

Latest completed frontend app shell child:
<https://github.com/Tahjali11/Mythic-Edge/issues/700>

Latest completed PR:
<https://github.com/Tahjali11/Mythic-Edge/pull/701>

Latest merge commit:
`280671206ffa7b1c53676afec363e00ae9973d0d`

## Contract

`docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md`

## Role Performed

Codex C: Module Implementer.

## Current Behavior Before This Slice

After issue #700, `frontend/src/App.tsx` remained the public app-shell facade
and route-shell metadata already lived in `frontend/src/app_navigation.ts`.
Several pure display panels still lived inline in `App.tsx` even though they
already received complete props and did not call API helpers directly.

## Implementation Comparison

What stayed the same:

- `frontend/src/App.tsx` remains the public facade.
- The named `SetupStatusApp` export is preserved.
- The default `SetupStatusApp` export is preserved.
- `SetupStatusAppProps` dependency-injection behavior is preserved.
- Route/hash behavior and route href generation remain owned by
  `frontend/src/app_navigation.ts`.
- Dashboard, coach, privacy, and diagnostics rendering semantics are preserved.
- Static display copy, headings, aria labels, class names, route-card hrefs,
  status labels, and status tones are preserved.
- No API payload, backend route, live-capture behavior, parser behavior,
  workbook/webhook behavior, Apps Script behavior, storage key, CI behavior, or
  production behavior was intentionally changed.

What changed:

- Added private helper module `frontend/src/app_static_panels.tsx`.
- Moved these pure display panels behind the existing `App.tsx` facade:
  - `CoachBoundaryPanel`
  - `TrustPrivacyLayer`
  - `DashboardTrustPrivacySignal`
  - `DashboardRouteCards`
  - `PrivacyDetailsPanel`
- Added `frontend/src/app_static_panels.test.tsx` to lock the extracted panel
  copy, classes, aria labels, status pills, compact/full trust rendering, and
  route-card hrefs.

## Files Changed

- `frontend/src/App.tsx`
- `frontend/src/app_static_panels.tsx`
- `frontend/src/app_static_panels.test.tsx`
- `docs/implementation_handoffs/core_frontend_app_shell_static_display_panels_decomposition_comparison.md`

## Code Changed

Runtime frontend code changed only to extract private static display panels
behind the existing `frontend/src/App.tsx` facade.

No public frontend interface changed. The new module is private same-repo
support for the approved static display panel slice.

## Tests Added Or Updated

Added `frontend/src/app_static_panels.test.tsx` to verify:

- coach boundary heading, copy, class, and status label/tone;
- full trust/privacy layer headings, item classes, details, and status labels;
- compact dashboard trust/privacy signal copy, labels, and status tones;
- dashboard route-card labels, details, and symbolic hash hrefs;
- privacy details headings and local-only boundary copy.

Existing `frontend/src/App.test.tsx`, `frontend/src/api.test.ts`, and
`frontend/src/app_navigation.test.ts` were rerun for facade, API-boundary, and
route-shell behavior preservation.

## Interface Changes

No public interface changes.

Private same-repo module added:

- `frontend/src/app_static_panels.tsx`

Preserved public interfaces:

- `frontend/src/App.tsx`
- named `SetupStatusApp` export
- default `SetupStatusApp` export
- `SetupStatusAppProps` dependency-injection behavior

## Validation Run

```bash
npm --prefix frontend ci
npm --prefix frontend test -- --run src/app_static_panels.test.tsx
npm --prefix frontend run typecheck
npm --prefix frontend test -- --run src/App.test.tsx src/api.test.ts src/app_navigation.test.ts src/app_static_panels.test.tsx
printf '%s\n' frontend/src/App.tsx frontend/src/app_static_panels.tsx frontend/src/app_static_panels.test.tsx | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' frontend/src/App.tsx frontend/src/app_static_panels.tsx frontend/src/app_static_panels.test.tsx | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main
git diff --check
printf '%s\n' frontend/src/App.tsx frontend/src/app_static_panels.tsx frontend/src/app_static_panels.test.tsx docs/implementation_handoffs/core_frontend_app_shell_static_display_panels_decomposition_comparison.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
python3 tools/check_agent_docs.py
npm --prefix frontend run build
npm --prefix frontend run test -- --run
```

Results:

- `npm ci`: passed. It reported two dependency audit findings; no dependency
  metadata was changed because audit fixes are outside this slice.
- New static panel tests: 1 file, 5 tests passed.
- TypeScript typecheck: passed.
- Contracted frontend tests: 4 files, 105 tests passed.
- Path-scoped frontend secret/private marker scan: 3 scanned paths, 0 findings.
- Path-scoped frontend protected-surface scan: 3 changed paths, 0 findings.
- Path-scoped scan including this handoff: 4 scanned paths, 0 findings.
- Path-scoped protected-surface gate including this handoff: 4 changed paths,
  0 findings.
- Repo-wide protected-surface check: passed, reporting 0 changed committed
  paths because this Codex C work is still uncommitted.
- Repo-wide secret/private marker scan: failed on pre-existing legacy findings
  outside this slice. Changed-file scans for this implementation passed cleanly.
- `git diff --check`: passed.
- Validation selector for changed paths: passed and selected frontend tests,
  build, typecheck, diff check, protected-surface gate, secret/private marker
  scan, and agent-docs checker.
- Agent docs consistency check: passed with 36 checked files, 0 errors, and
  0 warnings.
- Production frontend build: passed.
- Full frontend test suite: 5 files, 109 tests passed.

## Still Unverified

- Independent Codex E review.
- Browser visual/manual inspection.
- GitHub CI behavior.
- Later frontend app-shell slices beyond static display panels.

## Reviewer Focus

Please verify:

- the extracted panels preserve visible copy, headings, aria labels, class
  names, route-card hrefs, status labels, and status tones;
- `frontend/src/App.tsx` remains the public facade;
- `SetupStatusApp`, the default export, and `SetupStatusAppProps` remain
  intact;
- no route/hash, API, backend, live-capture, parser, storage, CI, workbook,
  webhook, or Apps Script behavior changed;
- the new helper module does not broaden beyond private same-repo static
  display panel support.

## Next Workflow Action

Next role: Codex E.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Reviewer for Mythic-Edge issue #702.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/702

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Contract:
docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md

Implementation handoff:
docs/implementation_handoffs/core_frontend_app_shell_static_display_panels_decomposition_comparison.md

Review scope:
Review only the behavior-preserving static display panel extraction behind the existing frontend/src/App.tsx facade.

Expected files:
- frontend/src/App.tsx
- frontend/src/app_static_panels.tsx
- frontend/src/app_static_panels.test.tsx
- docs/implementation_handoffs/core_frontend_app_shell_static_display_panels_decomposition_comparison.md

Protected boundaries:
Do not change frontend behavior, route/hash behavior, visible copy/control/aria/className behavior, API payloads, backend routes, live-capture behavior, parser behavior, workbook/webhook/Apps Script behavior, CI, readiness claims, reliability readiness claims, parser truth claims, security assurance, or privacy assurance.

Validation to inspect or rerun:
- npm --prefix frontend test -- --run src/app_static_panels.test.tsx
- npm --prefix frontend run typecheck
- npm --prefix frontend test -- --run src/App.test.tsx src/api.test.ts src/app_navigation.test.ts src/app_static_panels.test.tsx
- path-scoped secret/private marker scan for changed files
- path-scoped protected-surface scan for changed files
- git diff --check

End with findings first, validation reviewed, remaining risks, recommended next role, and workflow_handoff.
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/702"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  source_decision_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/697"
  latest_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/700"
  latest_completed_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/701"
  latest_merge_commit: "280671206ffa7b1c53676afec363e00ae9973d0d"
  completed_thread: "C"
  next_thread: "E"
  verdict: "frontend_app_static_display_panels_ready_for_review"
  risk_tier: "High"
  candidate_id: "frontend_app_static_display_panels"
  implementation_scope: "behavior_preserving_static_display_panel_extraction_only"
  frontend_behavior_change_authorized: false
  route_hash_behavior_change_authorized: false
  visible_copy_control_aria_classname_change_authorized: false
  api_payload_change_authorized: false
  live_capture_behavior_change_authorized: false
  backend_route_change_authorized: false
  parser_behavior_change_authorized: false
  workbook_webhook_change_authorized: false
  apps_script_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  reliability_readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
