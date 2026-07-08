# Frontend App Shell Dashboard Module View Preferences Decomposition Comparison

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/704>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker:
<https://github.com/Tahjali11/Mythic-Edge/issues/463>

Source decision packet:
<https://github.com/Tahjali11/Mythic-Edge/issues/697>

Latest completed frontend app shell child:
<https://github.com/Tahjali11/Mythic-Edge/issues/702>

Latest completed PR:
<https://github.com/Tahjali11/Mythic-Edge/pull/703>

Latest merge commit:
`ad9349d3fcba2972aebddf8e540ad9b31330141d`

## Contract

`docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md`

## Role Performed

Codex C: Module Implementer.

## Current Behavior Before This Slice

After issue #702, `frontend/src/App.tsx` remained the public app-shell facade.
Route-shell metadata lived in `frontend/src/app_navigation.ts`, and static
display panels lived in `frontend/src/app_static_panels.tsx`.

`App.tsx` still owned the dashboard module view preference cluster inline:

- `DASHBOARD_MODULE_VIEW_PREFERENCES_KEY`
- accepted dashboard module ids
- accepted dashboard view values
- `readDashboardModuleViewPreferences`
- `writeDashboardModuleViewPreferences`
- selected-view fallback logic

Those helpers are local browser preference behavior only. They do not own
parser facts, backend route contracts, dashboard module payload shape,
analytics truth, live-capture behavior, workbook/webhook behavior, or Apps
Script behavior.

## Implementation Comparison

What stayed the same:

- `frontend/src/App.tsx` remains the public facade.
- The named `SetupStatusApp` export is preserved.
- The default `SetupStatusApp` export is preserved.
- `SetupStatusAppProps` dependency-injection behavior is preserved.
- The storage key remains
  `mythic_edge.analytics.dashboard.module_view_preferences.v1`.
- Accepted module ids remain:
  - `play_draw_win_rate`
  - `game1_postboard`
  - `mulligan_opening_hand_outcomes`
- Accepted view values remain `bar` and `table`.
- Malformed JSON, non-object storage, arrays, unknown module ids, unknown view
  values, and browser storage failures still fail closed.
- Selected-view fallback remains preferred view, then valid module default
  view, then first allowed view, then `table`.
- Visible labels, aria labels, class names, dashboard rendering behavior,
  route/hash behavior, API payloads, backend routes, live-capture behavior,
  parser behavior, workbook/webhook behavior, Apps Script behavior, CI
  behavior, and production behavior were not intentionally changed.

What changed:

- Added private helper module `frontend/src/app_dashboard_preferences.ts`.
- Moved dashboard module preference constants, read/write sanitization helpers,
  and selected-view fallback logic behind the existing `App.tsx` facade.
- Added `frontend/src/app_dashboard_preferences.test.ts` to pin the local
  preference behavior directly.

## Files Changed

- `frontend/src/App.tsx`
- `frontend/src/app_dashboard_preferences.ts`
- `frontend/src/app_dashboard_preferences.test.ts`
- `docs/implementation_handoffs/core_frontend_app_shell_dashboard_module_view_preferences_decomposition_comparison.md`

## Code Changed

Runtime frontend code changed only to extract private dashboard module view
preference helpers behind the existing `frontend/src/App.tsx` facade.

No public frontend interface changed. The new module is private same-repo
support for the approved dashboard module preference slice.

## Tests Added Or Updated

Added `frontend/src/app_dashboard_preferences.test.ts` to verify:

- the storage key is unchanged;
- only supported module ids and view values are read from storage;
- missing, malformed, array, and null storage values fall back to `{}`;
- writes persist only supported module ids and view values;
- browser storage get/set failures do not throw;
- selected-view fallback order remains preferred, valid default, first allowed,
  then `table`.

Existing `frontend/src/App.test.tsx`, `frontend/src/api.test.ts`,
`frontend/src/app_navigation.test.ts`, and `frontend/src/app_static_panels.test.tsx`
were rerun for facade, API-boundary, route-shell, and static-panel behavior
preservation.

## Interface Changes

No public interface changes.

Private same-repo module added:

- `frontend/src/app_dashboard_preferences.ts`

Preserved public interfaces:

- `frontend/src/App.tsx`
- named `SetupStatusApp` export
- default `SetupStatusApp` export
- `SetupStatusAppProps` dependency-injection behavior

## Validation Run

```bash
npm --prefix frontend ci
npm --prefix frontend test -- --run src/app_dashboard_preferences.test.ts
npm --prefix frontend test -- --run src/App.test.tsx src/api.test.ts src/app_navigation.test.ts src/app_static_panels.test.tsx src/app_dashboard_preferences.test.ts
npm --prefix frontend run typecheck
printf '%s\n' frontend/src/App.tsx frontend/src/app_dashboard_preferences.ts frontend/src/app_dashboard_preferences.test.ts docs/implementation_handoffs/core_frontend_app_shell_dashboard_module_view_preferences_decomposition_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' frontend/src/App.tsx frontend/src/app_dashboard_preferences.ts frontend/src/app_dashboard_preferences.test.ts docs/implementation_handoffs/core_frontend_app_shell_dashboard_module_view_preferences_decomposition_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main
printf '%s\n' frontend/src/App.tsx frontend/src/app_dashboard_preferences.ts frontend/src/app_dashboard_preferences.test.ts docs/implementation_handoffs/core_frontend_app_shell_dashboard_module_view_preferences_decomposition_comparison.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
python3 tools/check_agent_docs.py
npm --prefix frontend run build
npm --prefix frontend run test -- --run
python3 tools/check_secret_patterns.py --base origin/main
git diff --check
```

Results:

- `npm ci`: passed. It reported two dependency audit findings; dependency
  remediation is outside this decomposition slice.
- New dashboard preference tests: 1 file, 6 tests passed.
- Contracted frontend tests: 5 files, 111 tests passed.
- TypeScript typecheck: passed.
- Path-scoped secret/private marker scan for this changed-file set: 4 scanned
  paths, 0 findings.
- Path-scoped protected-surface gate for this changed-file set: 4 changed
  paths, 0 findings.
- Repo-wide secret/private marker scan: failed on pre-existing legacy findings
  outside this slice. The changed-file scan for this implementation passed.
- Repo-wide protected-surface check: passed, reporting 0 changed committed
  paths because this Codex C work is still uncommitted. The explicit
  changed-file protected-surface scan passed.
- Validation selector for changed paths: passed and selected frontend build,
  frontend tests, frontend typecheck, diff check, protected-surface gate,
  secret/private marker scan, and agent-docs checker.
- Agent docs consistency check: passed with 36 checked files, 0 errors, and
  0 warnings.
- Production frontend build: passed.
- Full frontend test suite: 6 files, 115 tests passed.
- Changed-files secret/private marker scan using the default git diff mode:
  passed, reporting 0 scanned paths because this Codex C work is uncommitted.
- `git diff --check`: passed.

## Still Unverified

- Independent Codex E review.
- Browser visual/manual inspection.
- GitHub CI behavior.
- Later frontend app-shell slices beyond dashboard module view preferences.

## Reviewer Focus

Please verify:

- `frontend/src/App.tsx` remains the public facade;
- the extracted helper preserves the exact storage key and accepted
  module/view vocabulary;
- malformed and unsafe browser storage values still fail closed;
- selected-view fallback order did not change;
- visible copy, controls, aria labels, class names, dashboard rendering,
  route/hash behavior, API payloads, backend routes, live-capture behavior,
  parser behavior, workbook/webhook behavior, Apps Script behavior, and CI
  behavior were not changed.

## Next Workflow Action

Next role: Codex E.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Reviewer for Mythic-Edge issue #704.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/704

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Contract:
docs/contracts/core_frontend_app_shell_decomposition_decision_packet.md

Implementation handoff:
docs/implementation_handoffs/core_frontend_app_shell_dashboard_module_view_preferences_decomposition_comparison.md

Review scope:
Review only the behavior-preserving dashboard module view preference extraction behind the existing frontend/src/App.tsx facade.

Expected files:
- frontend/src/App.tsx
- frontend/src/app_dashboard_preferences.ts
- frontend/src/app_dashboard_preferences.test.ts
- docs/implementation_handoffs/core_frontend_app_shell_dashboard_module_view_preferences_decomposition_comparison.md

Protected boundaries:
Do not change frontend behavior, route/hash behavior, visible copy/control/aria/className behavior, dashboard module rendering behavior, dashboard module payload types, analytics auto-refresh behavior, API payloads, backend routes, live-capture behavior, parser behavior, workbook/webhook/Apps Script behavior, CI, readiness claims, reliability readiness claims, parser truth claims, security assurance, or privacy assurance.

Validation to inspect or rerun:
- npm --prefix frontend test -- --run src/app_dashboard_preferences.test.ts
- npm --prefix frontend test -- --run src/App.test.tsx src/api.test.ts src/app_navigation.test.ts src/app_static_panels.test.tsx src/app_dashboard_preferences.test.ts
- npm --prefix frontend run typecheck
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/704"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  source_decision_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/697"
  latest_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/702"
  latest_completed_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/703"
  latest_merge_commit: "ad9349d3fcba2972aebddf8e540ad9b31330141d"
  completed_thread: "C"
  next_thread: "E"
  verdict: "frontend_dashboard_module_view_preferences_ready_for_review"
  risk_tier: "High"
  candidate_id: "frontend_dashboard_module_view_preferences"
  implementation_scope: "behavior_preserving_dashboard_module_view_preference_helper_extraction_only"
  frontend_behavior_change_authorized: false
  route_hash_behavior_change_authorized: false
  visible_copy_control_aria_classname_change_authorized: false
  dashboard_module_preference_behavior_change_authorized: false
  local_storage_key_change_authorized: false
  dashboard_module_rendering_change_authorized: false
  analytics_auto_refresh_change_authorized: false
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
