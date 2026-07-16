# Analytics App Dashboard Status Truthfulness And Action Clarity Fixer Handoff

## Issue

- Original issue: https://github.com/Tahjali11/Mythic-Edge/issues/278
- Original implementation PR: https://github.com/Tahjali11/Mythic-Edge/pull/279
- Closed-issue reentry reason: the user explicitly requested a corrective pass
  for dashboard status truthfulness and action clarity on 2026-07-16.

Issue #278 and PR #279 are closed/merged. This local corrective pass does not
reopen either artifact and does not authorize GitHub lifecycle changes.

## Tracker

- Analytics/local app tracker: https://github.com/Tahjali11/Mythic-Edge/issues/204
  (`CLOSED` when verified)
- Local app umbrella: https://github.com/Tahjali11/Mythic-Edge/issues/207
  (`CLOSED` when verified)
- Release-readiness tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
  (`OPEN` when verified)

## Contract

- [Analytics App First-Screen Competitive Cockpit Contract](../contracts/analytics_app_first_screen_competitive_cockpit.md)
- Relevant contract sections:
  [Compact Health/Status Rail](../contracts/analytics_app_first_screen_competitive_cockpit.md#compact-healthstatus-rail),
  [User-Facing Status Translation Boundary](../contracts/analytics_app_first_screen_competitive_cockpit.md#user-facing-status-translation-boundary),
  and [Error Behavior](../contracts/analytics_app_first_screen_competitive_cockpit.md#error-behavior)
- Original implementation handoff:
  [Analytics App First-Screen Competitive Cockpit Comparison](./analytics_app_first_screen_competitive_cockpit_comparison.md)
- Original independent review:
  [Analytics App First-Screen Competitive Cockpit Contract Test](../contract_test_reports/analytics_app_first_screen_competitive_cockpit.md)
- Governance:
  [Agent Constitution](../agent_constitution.md) and
  [Module Fixer Thread Rules](../agent_threads/module_fixer.md)

## Source Finding

The source finding was the user's explicit request in the current Codex task.
It was reproduced deterministically in the current frontend:

1. `buildCockpitStatusItems` translated a healthy app status to `Connected`
   but tested for the different label `Ready` before choosing its detail text.
   A connected backend therefore displayed `Backend response needs review.`
2. The `Analytics database` tile ignored
   `payload.analytics_database.status`, used only the match/game history state,
   and collapsed every non-`Ready` result into `No history yet.` This could
   describe loading, blocked, unavailable, degraded, missing, or contradictory
   evidence as an empty history.
3. `CockpitStatusRail` supplied an action only for `Live capture`; the app and
   analytics tiles had no direct details or recovery affordance even though the
   contract requires one.

Fault category: frontend presentation/status-translation defect. No backend,
parser, analytics storage, deployment, or contract defect was required to
reproduce the finding.

## Internal Project Area

Local App / UI.

## Truth Owner

- The validated setup response owns the source analytics-database setup
  status.
- The validated match/game history responses own their endpoint statuses and
  returned rows.
- The frontend owns only user-facing translation, evidence precedence, detail
  copy, and navigation affordances.
- Parser/state and Analytics/SQLite truth ownership are unchanged.

## Bridge-Code Status

`bridge_code`

The patch changes only the existing bridge from validated backend status/data
responses to user-facing dashboard status. It does not create a reverse write
path or make frontend labels a source of project truth.

## Role Performed

Codex D: Module Fixer.

Risk tier: Medium-High, inherited from the source contract.

## What Changed

- `App connection` now reports `Connected` only in the ready render path,
  which is reached after a validated setup response succeeds. Aggregate setup
  degradation no longer mislabels backend reachability.
- If setup display values were redacted, the connection remains truthfully
  `Connected`; its detail explains that values were hidden and links to
  Privacy.
- `Analytics database` now combines the source database status with history
  loading/error/status/row evidence instead of treating every non-ready state
  as empty.
- `Empty history` appears only when both history endpoints report empty and
  return no rows.
- Contradictory evidence fails closed. For example, available rows plus a
  missing database setup status remain `Setup needed`, explicitly acknowledge
  the available history, and route to Diagnostics instead of Import.
- Blocking/unavailable/missing endpoint severity takes precedence over a
  simultaneous display-redaction warning, so privacy degradation cannot
  downgrade a more serious source status.
- Ready history reports the visible match/game counts. Degraded history with
  rows says that history is available but needs review.
- App and analytics tiles now expose contextual links to Diagnostics,
  Analytics, Import, or Privacy. The existing live-capture lifecycle control
  remains unchanged.

## Files Changed

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_status_truthfulness_fixer.md`

## Code Changed

Runtime code changed only in the React frontend:

- `CockpitStatusItem` gained a private optional action shape.
- `CockpitStatusRail` renders that action for non-live tiles.
- `buildCockpitStatusItems` now separates successful app reachability from
  aggregate setup health.
- `analyticsDatabaseCockpitSummary` owns the contained precedence rules for
  database status, history availability, row evidence, and redaction state.
- `analyticsHistoryStatus` now evaluates source endpoint severity before the
  frontend redaction warning.
- `analyticsHistoryFallbackDetail` and `countLabel` keep safe copy generation
  explicit.
- `.cockpitActionLink` provides a visible keyboard-focusable action style.

No backend or public API code changed.

## Tests Added Or Updated

`frontend/src/App.test.tsx` now proves:

- a degraded aggregate setup payload can still truthfully show a validated app
  connection as `Connected`;
- a missing analytics database says `Setup needed` and offers Import when no
  history rows are available;
- a ready database with match/game rows says `Ready`, reports the row counts,
  and links to Analytics;
- available history is not called empty when database setup reports missing;
- a database-level empty claim with present history rows fails closed as
  `Needs review`;
- `Empty history` is used only for ready endpoints that both report empty and
  return no rows;
- degraded history with rows remains visibly available while reporting
  `Needs review`;
- a blocked history endpoint remains `Blocked` even when a display value is
  also redacted;
- setup redaction does not turn the connection into a false failure and routes
  the user to Privacy;
- the former generic `No history yet.` copy is absent from the covered status
  states.

## Interface Changes

- Private frontend component shape only: `CockpitStatusItem` now accepts an
  optional `{ href, label }` action.
- No backend payload field, API route, TypeScript API response type, database
  schema, parser interface, environment variable, build contract, or hosting
  contract changed.

## Contracted Area Status

The implementation stayed inside Local App / UI. It consumes already validated
setup and analytics payloads without changing their meaning or producer
contracts. No downstream consumer, persistence layer, protected truth owner,
or external surface was changed.

## Validation Run

```powershell
npm --prefix frontend test -- --run src/App.test.tsx src/status.test.ts
# passed: 2 files, 67 tests

npm --prefix frontend test -- --run
# passed: 4 files, 118 tests

npm --prefix frontend run typecheck
# passed

npm --prefix frontend run build
# passed: TypeScript, Sites TypeScript, server/client build, 5 hosting-shape tests

git diff --check
# passed

py tools\check_agent_docs.py
# passed: 47 files, 0 errors, 0 warnings

# Path-scoped checks over all four files named in this handoff:
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed: forbidden 0, warnings 0

py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed: forbidden 0, warnings 0
```

The build produced only ignored `frontend/dist` output. No build output is
included in the Git diff.

## Still Unverified

- Browser-level visual and responsive behavior was not manually inspected;
  this task did not authorize interactive browser testing.
- Rendering against the user's private live app data was not exercised; tests
  use sanitized synthetic payloads.
- No deployment, Sites publication, backend startup, live capture, external
  write, or production action was attempted.

## Reviewer Focus

The contract-test reviewer should pay special attention to:

- whether successful validated setup fetches are sufficient evidence for the
  `Connected` app label in the ready render path;
- whether database status correctly takes precedence without erasing visible
  history-row evidence;
- whether `Empty history` is restricted to proven empty endpoint results;
- whether unknown, missing, blocked, unavailable, degraded, unsafe, and
  contradictory states still fail closed without implying absence;
- whether each tile's action leads to the most useful existing local route;
- whether the new link remains usable at the existing mobile breakpoint;
- whether any status copy overstates backend, parser, or analytics truth.

## Next Workflow Action

Next role: Codex E, Module Reviewer in contract-test mode.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution and $mythic-edge-workflow.

Act as Codex E: Module Reviewer in contract-test mode for the user-requested dashboard status truthfulness and action-clarity corrective pass against closed issue #278.

Read:
- docs/contracts/analytics_app_first_screen_competitive_cockpit.md
- docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_status_truthfulness_fixer.md
- docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_comparison.md
- docs/contract_test_reports/analytics_app_first_screen_competitive_cockpit.md
- docs/agent_threads/contract_test.md
- docs/templates/contract_test_report.md

Review only the current local diff in:
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx
- docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_status_truthfulness_fixer.md

Verify the first proven failures and the fix independently. Confirm that App connection no longer conflates aggregate setup health with backend reachability; Analytics database does not collapse loading, errors, degradation, missing setup, contradictory row evidence, or redaction into an empty-history claim; Empty history is shown only for proven empty endpoints; every compact rail tile has a meaningful details/action affordance; and frontend copy does not become parser or analytics truth.

Run focused tests first, then the full frontend tests, typecheck, build, diff check, agent-doc check, and path-scoped protected-surface/private-marker scans. Record the review as a followup_after_fixer in docs/contract_test_reports/analytics_app_first_screen_competitive_cockpit.md while preserving the original report evidence.

This is a read-only review except for the contract-test report. Do not edit implementation, stage, commit, push, open or update a PR, reopen or close issues, merge, publish to Sites, deploy, start live capture, or change backend/parser/analytics schema/transport/credentials/external state. Route concrete findings back to Codex D; route contract ambiguity to Codex B.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/278"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/204"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_status_truthfulness_fixer.md"
  target_artifact: "docs/contract_test_reports/analytics_app_first_screen_competitive_cockpit.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  internal_project_area: "Local App / UI"
  truth_owner: "Backend setup/history payload producers own source facts; frontend owns presentation and status translation only"
  bridge_code_status: "bridge_code"
  freshness:
    current_branch: "codex/analytics-foundation"
    intended_branch: "codex/analytics-foundation"
    upstream_branch: "origin/codex/analytics-foundation"
    branch_ahead_behind: "0 ahead, 0 behind before local uncommitted changes"
    issue_state: "#278 CLOSED; explicit user-requested corrective reentry"
    tracker_state: "#204 CLOSED; #207 CLOSED; #136 OPEN"
    source_artifact_status: "new untracked candidate handoff in the current local diff"
    target_artifact_status: "tracked existing report; followup review not yet recorded"
    local_dirty_state: "four intended unstaged files; no unrelated tracked changes observed"
    untracked_artifacts:
      - "docs/implementation_handoffs/analytics_app_first_screen_competitive_cockpit_status_truthfulness_fixer.md"
    related_open_prs: "none for codex/analytics-foundation"
    last_known_merge_or_closeout: "PR #279 merged and issue #278 closed on 2026-06-04"
    worktree_classification: "primary_current_worktree"
    closed_issue_reentry_reason: "explicit user-requested corrective pass for dashboard status truthfulness and action clarity"
    freshness_verdict: "closed_issue_reentry"
    recommended_route: "route_to_codex_e"
    verified_at: "2026-07-16"
  validation:
    - "focused App/status tests -> 67 passed"
    - "full frontend tests -> 118 passed"
    - "frontend typecheck -> passed"
    - "Sites-compatible frontend build and 5 hosting-shape tests -> passed"
    - "git diff --check -> passed"
    - "agent docs consistency -> 47 files, 0 errors, 0 warnings"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
  stop_conditions:
    - "Stop and route to D for a concrete implementation or regression finding."
    - "Stop and route to B if truthful status behavior requires a new backend field, endpoint, or contract change."
    - "Do not infer issue, PR, merge, deployment, Sites publication, or production authority from this handoff."
```
