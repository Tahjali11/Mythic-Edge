# Analytics App Frontend Information Architecture Contract

## Module

`analytics_app_frontend_information_architecture`

Plain English: this contract defines the local app frontend shell and first-screen information architecture. The app should feel like a compact competitive cockpit first, with deeper analytics, review, import, feedback, privacy, and diagnostics available through navigation or drawers instead of one long technical page.

This is a contract-writing artifact only. It does not implement code, change backend behavior, change parser behavior, change analytics semantics, create GitHub issues, or enable AI/runtime coaching.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/299
- Branch: `codex/analytics-foundation`
- Risk tier: High overall; recommended first implementation slice is Medium and frontend-only.
- Source artifact: GitHub issue #299

Required repo authorities:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related active or adjacent issues:

- Issue #294: analytics auto-refresh after completed match result
- Issue #297: explicit Start capture control for local SQLite live mode
- Issue #298: submit sanitized error reports to GitHub Issues

Those issues remain separate. This contract may create entry points or placeholders for those surfaces, but it must not implement their behavior.

## Tracker

N/A. Issues #204 and #207 are closed historical context, not active trackers for this work.

## Owning Layer

Primary owning layer: Local App / UI.

Supporting layers:

- Local app backend owns existing API payloads and safe status composition.
- Analytics owns deterministic query outputs and chart-ready dashboard module payloads.
- Match Journal owns human-entered notes and labels.
- Parser/state owns parser-managed facts.

## Internal Project Area

Primary area: Local App / UI.

## Truth Owner

The frontend owns navigation state, visual hierarchy, layout, panel visibility, drawer state, focus behavior, and user-facing status translation.

The frontend does not own parser facts, analytics facts, live capture truth, Match Journal truth, privacy policy authority, GitHub submission authority, or AI/coaching truth.

## Bridge-Code Status

`bridge_code`

Bridge details:

- Source internal project areas: Analytics, Live Player.log Mode, Match Journal, Local App Backend.
- Consuming internal project area: Local App / UI.
- Allowed data flow: existing backend API responses to frontend typed validation to frontend display/navigation.
- Forbidden reverse flow: frontend route state, browser storage, dashboard labels, drawer state, or visual badges must not write back to parser state, analytics tables, live capture state, Match Journal records, external issue trackers, workbook transport, or AI/coaching systems unless a separate contract authorizes that specific behavior.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/analytics_app_frontend_information_architecture.md`

Future Codex C implementation files authorized for the frontend-only first slice:

- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/src/api.ts`, only when route/view wiring requires existing typed API helpers to be passed through unchanged
- `frontend/src/types.ts`, only for frontend route/view state types or already-existing API types used by display
- optional new frontend-only helper/module under `frontend/src/` if it reduces `App.tsx` size without changing backend contracts
- `docs/implementation_handoffs/analytics_app_frontend_information_architecture_comparison.md`

Reference-only surfaces:

- `src/mythic_edge_parser/local_app/backend.py`
- `src/mythic_edge_parser/local_app/error_reports.py`
- existing local app backend tests
- existing analytics, live capture, Match Journal, and feedback contracts

Not owned by this contract:

- parser modules
- local app backend route behavior
- analytics schema, migrations, ingest, or query semantics
- live capture supervisor behavior
- Match Journal repository/service behavior
- GitHub external submission behavior
- workbook/webhook/App Script/Sheets behavior
- OpenAI/model-provider runtime integration
- generated/private/local artifacts

## Observed Current Behavior

Observed on `codex/analytics-foundation` during this contract pass:

- Issue #299 is open.
- The target contract artifact did not exist before this pass.
- The worktree has pre-existing uncommitted local app, live-capture, and error-report files. This contract pass must not revert, stage, or overwrite them.
- `frontend/src/App.tsx` already renders a local app shell with a left rail, dashboard header, cockpit status rail, live capture control panel, Decision Support modules, Coach pending panel, trust/privacy summary, error report panel, analytics review details, Match Journal cockpit, manual import panel, and technical diagnostics disclosure.
- The current app still lays most major surfaces into one long document below the dashboard.
- Current rail links are hash anchors, not a full route-gated information architecture.
- Diagnostics already have a progressive disclosure control.
- Decision Support modules already use the existing analytics dashboard module contract.
- Error reporting is currently copy-first/sanitized under issue #281, while live GitHub submission remains issue #298.
- Explicit live capture control exists as issue #297 and must remain separate from IA work.

## Contract Decision

Issue #299 should authorize a frontend-only first implementation slice.

Approved first slice:

- define a stable hash-route model for app modes;
- turn the left rail into primary mode navigation;
- make Dashboard the first-screen cockpit;
- move or gate deep details behind mode views, drawers, or progressive disclosure;
- keep existing backend API calls and payload contracts unchanged;
- keep existing analytics, live capture, Match Journal, feedback, privacy, and diagnostics data sources unchanged;
- preserve current safe display/redaction behavior;
- add focused frontend tests for navigation, visibility, accessibility, and forbidden claims.

Not approved in this issue:

- backend payload changes;
- new backend routes;
- SQLite schema, migration, or ingest changes;
- analytics auto-refresh from issue #294;
- live capture start/stop semantics from issue #297;
- live GitHub submission from issue #298;
- AI Coach runtime behavior;
- Match Journal write semantics changes;
- arbitrary SQL or database browsing;
- charting library changes;
- destructive controls.

## App-Shell Route Contract

### Route Model

Codex C should implement or refine a frontend-only hash route model. Recommended route ids:

```text
dashboard
coach
analytics
review
privacy
feedback
import
diagnostics
```

Recommended URL shape:

```text
/#dashboard
/#coach
/#analytics
/#review
/#privacy
/#feedback
/#import
/#diagnostics
```

Rules:

- `dashboard` is the default route.
- Unknown routes must fall back to `dashboard` or a safe not-found state that routes back to `dashboard`.
- The route state must be frontend display state only.
- Hash route changes must not trigger backend writes.
- Route state must not become parser, analytics, live capture, Match Journal, GitHub, privacy, or AI truth.

### Left Rail

The left rail should be the primary app navigation. The issue prefers icon-first rail behavior with labels on hover, but the first implementation must preserve discoverability and accessibility.

Required rail behavior:

- stable route links for Dashboard, Coach, Analytics, Review, Privacy, Feedback, Import, and Diagnostics;
- active route state visible in more than color alone;
- keyboard focus visible;
- accessible names for every rail item;
- tooltips or visible labels for icon-first items;
- mobile-friendly layout that does not overlap content;
- no text clipping at supported viewport widths;
- no route item that implies unsupported behavior is live.

Allowed first-slice choice:

- icon-plus-label rail, if that is clearer and safer than icon-only;
- icon-first rail with hover/focus labels, if tests prove labels and focus names remain accessible.

Deferred:

- user-configurable expanded/collapsed rail preference;
- persistent rail layout preference in browser storage;
- command palette;
- global search.

## Mode Responsibility Contract

### Dashboard

Dashboard owns the first 10-second cockpit.

It must prioritize:

- app/backend reachability;
- Player.log monitor state;
- live capture state;
- analytics database/readiness state;
- compact data trust/privacy signal;
- Decision Support with the three existing default modules:
  - `Win Rate By Play/Draw`
  - `Game 1 / Postboard`
  - `Mulligan / Opening Hand Outcomes`
- AI Coach preview marked as pending/deferred;
- quick Match Journal note access or Review route call-to-action;
- feedback access;
- visible route to diagnostics when a serious issue needs attention.

Dashboard must avoid:

- long technical setup grids;
- long history/review tables;
- full manual import forms;
- full Match Journal cockpit forms;
- large privacy explanation blocks;
- raw status dumps;
- generic database browsing;
- first-screen AI/coaching claims.

Dashboard may show compact status cards for surfaces that live elsewhere, but those cards must route the user to the owning mode rather than duplicating the whole workflow.

### Analytics

Analytics owns deeper read-only exploration of stored SQLite analytics:

- match and game history;
- play/draw splits;
- game 1/postboard splits;
- opening hands;
- mulligans;
- gameplay-action review;
- opponent-card-observation review;
- Decision Support module details when expanded.

Analytics must remain read-only in this contract. It must not add arbitrary SQL, table browsing, schema mutation, data export, or analytics truth changes.

### Review

Review owns uneditorialized inspection and Match Journal access:

- Match Journal cockpit;
- journal context summary;
- note entry and readback surfaces already authorized by existing contracts;
- review flags and human labels as human annotations only.

Review must not make Match Journal labels parser truth, archetype truth, hidden-card truth, coaching truth, or gameplay correctness truth.

### Coach

Coach owns a future AI-wrapper placeholder only.

Allowed now:

- pending/deferred panel;
- explanation that AI Coach is not connected;
- links to relevant future routing or issue prompts if already safe.

Forbidden now:

- OpenAI/model-provider calls;
- prompt execution;
- gameplay advice;
- hidden-card inference;
- player-mistake labels;
- best-line recommendations;
- claims that coach output is active or authoritative.

### Import

Import owns manual JSONL import and browser/folder upload workflows.

Dashboard may show only compact import readiness and a route/action into Import. The full import forms should not occupy the default dashboard.

Import must preserve all existing private-file and generated-artifact boundaries.

### Feedback

Feedback owns the local report-preparation surface.

First-slice behavior:

- surface may be a route, a right-side drawer, or both;
- report preview remains copy-first and sanitized;
- live GitHub submission is not enabled by this contract;
- any `Submit` wording must not imply external issue creation unless issue #298 is implemented under its own contract.

Recommended wording before #298 implementation:

- `Prepare Report`
- `Preview Report`
- `Copy Report`

Avoid:

- `Submit to GitHub`
- `File Issue`
- `Send Report`

### Privacy

Privacy owns compact trust explanations and redaction summaries.

Dashboard may show a small trust/privacy card. The full detail view belongs under Privacy.

Privacy must explain:

- raw Player.log content is not displayed;
- private local artifacts are excluded;
- generated database files are local-only;
- AI/runtime coaching and external submission are not active unless separately enabled by contract.

Privacy must not expose raw private paths, local file contents, local artifact lists, or sensitive environment details.

### Diagnostics

Diagnostics owns technical setup/status details and live diagnostics.

Diagnostics should be hidden by default unless:

- a serious blocker exists;
- the current route is `diagnostics`;
- the user explicitly expands technical details.

Diagnostics must stay read-only in this contract. It must not expose raw payloads, private local paths, stack traces with sensitive values, arbitrary files, arbitrary SQL, or destructive actions.

## Moved, Hidden, Or Collapsed Section Contract

Codex C may move, hide, or collapse these existing sections as frontend layout work:

- setup/status grids into Diagnostics;
- live diagnostics into Diagnostics;
- long match/game/early-game/action/split tables into Analytics;
- full manual import forms into Import;
- Match Journal cockpit forms into Review;
- full error-report form into Feedback drawer/route;
- full privacy explanation into Privacy.

Codex C must keep the user able to reach every existing major workflow. Moving a section is acceptable; removing an existing workflow is not.

For sections moved away from Dashboard:

- keep a compact Dashboard card or route affordance when the section is operationally important;
- preserve existing loading, empty, degraded, unavailable, and error states;
- preserve existing safe redaction behavior;
- preserve existing form disablement rules;
- preserve existing test coverage or replace it with equivalent route-aware coverage.

## Frontend-Only First-Slice Boundary

Allowed:

- React component restructuring;
- local hash-route state;
- CSS layout changes;
- route-specific conditional rendering;
- frontend-only drawer shell;
- frontend-only status copy refinement that does not alter API interpretation;
- accessible nav labels, focus handling, and active states;
- tests for route navigation, dashboard priority, hidden/moved sections, feedback drawer access, and safety claims.

Allowed browser storage:

- existing dashboard module view preferences;
- optional route preference only if it stores a route id such as `dashboard`.

Forbidden browser storage:

- API payload rows;
- analytics data;
- Player.log values;
- JSONL contents;
- local paths;
- report bodies;
- journal note bodies;
- generated database values;
- secret-like values;
- arbitrary diagnostic dumps.

## Deferred Backend/API/SQLite/GitHub/AI Scope

Backend/API deferred:

- new API routes;
- changed response schemas;
- changed setup/status payloads;
- changed dashboard module payloads;
- changed report preview payloads;
- changed live capture payloads.

SQLite/analytics deferred:

- schema changes;
- migration changes;
- ingest changes;
- query semantics changes;
- auto-refresh after completed match result from issue #294.

External submission deferred:

- GitHub issue creation;
- label management;
- attachments;
- connector authorization;
- OAuth or credential changes.

Live mode deferred:

- live capture start/stop semantics beyond displaying the existing state;
- live Player.log smoke;
- changes to watcher process control;
- changes to live SQLite write behavior.

AI deferred:

- OpenAI/model-provider runtime integration;
- coach prompt execution;
- coaching evaluation;
- strategic advice.

## Accessibility Requirements

Codex C must test or otherwise verify:

- each mode can be reached by keyboard;
- active rail item is visible and programmatically understandable;
- icon-first items have accessible names;
- hover labels are not the only way to understand navigation;
- drawer open/close controls have accessible names and focus behavior;
- route changes do not trap focus;
- status is not communicated by color alone;
- text does not overlap or clip in desktop and mobile layouts.

## Error Behavior

Unknown route:

- route to Dashboard or display a safe route-not-found state with a Dashboard action.

Backend unavailable:

- preserve existing backend-unavailable status behavior;
- do not show raw backend details;
- leave navigation usable.

Malformed API response:

- preserve fail-closed frontend validation;
- show the owning mode as degraded/unavailable;
- do not dump raw response content.

Missing database:

- Dashboard and Analytics should show a safe empty/missing state and route to Import or Diagnostics as appropriate;
- do not create files from the frontend.

Feedback unavailable:

- show copy/preview unavailable state;
- do not expose external submission controls.

AI Coach unavailable:

- show pending/deferred state;
- do not imply runtime support.

## Side Effects

Allowed side effects:

- frontend render state;
- URL hash changes;
- drawer open/close state;
- existing safe form state;
- existing browser storage for dashboard module view preferences;
- optional route preference if introduced safely;
- frontend tests and implementation handoff documentation.

Forbidden side effects:

- backend writes;
- parser behavior changes;
- analytics schema or migration changes;
- analytics ingest changes;
- live capture process changes;
- Match Journal behavior changes;
- external GitHub writes;
- workbook/webhook/App Script/Sheets writes;
- OpenAI/model-provider calls;
- generated database files;
- local runtime artifacts;
- frontend build output committed to Git;
- staging, commit, push, PR, merge, issue closure, or tracker closure unless explicitly requested by a later role.

## Compatibility

The first implementation must preserve:

- current setup/status loading and error behavior;
- current safe redaction behavior;
- current live capture status/control behavior from issue #297 work;
- current Decision Support module API usage;
- current manual refresh controls;
- current manual import workflows;
- current Match Journal workflows;
- current sanitized report preview/copy workflow;
- current diagnostics availability;
- current frontend API base URL safety checks;
- current no-chart-library posture.

## Unknowns

- Whether the best first rail should be icon-only with hover labels or icon-plus-label for discoverability.
- Whether Feedback should be a route, a right-side drawer, or both.
- Whether Privacy should be a rail item, footer utility, or both.
- Whether `Import` and `Diagnostics` should be first-class rail routes long-term or utility routes.
- Whether a visual wireframe artifact is needed before implementation. This contract does not require one, but Codex C may include a short textual layout summary in the implementation handoff.

## Suspected Gaps

- Current hash links do not fully behave like route-gated app modes.
- The current first screen still renders many major workflows below the dashboard in one document.
- Tests may assert global visibility of sections that should become route-specific.
- Feedback and diagnostics may need drawer/modal accessibility tests.
- Mobile rail behavior may need stronger layout constraints.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- Player.log status truth;
- live capture semantics;
- analytics schema, migrations, or ingest behavior;
- backend API contracts;
- Match Journal write semantics;
- SQLite annotation enrichment;
- GitHub external writes;
- privacy/safety display semantics that would weaken redaction;
- AI Coach runtime behavior;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- generated/private/local artifacts;
- secrets, endpoint values, spreadsheet IDs, or environment values.

Do not expose raw Player.log content, private JSONL payloads, generated SQLite contents, full private paths, sensitive local values, screenshots, arbitrary SQL, database browsing, hidden-card inference, archetype truth, player-mistake labels, best-line advice, or coaching claims.

## Tests Required

Codex C must add or update frontend tests proving:

- default route is Dashboard;
- left rail exposes all required modes with accessible names;
- active route state is visible and not color-only;
- Dashboard shows the required first-screen priorities;
- Dashboard does not render long technical setup grids by default;
- Dashboard does not render full manual import forms by default;
- Dashboard does not render full history/review tables by default;
- Dashboard does not render full Match Journal cockpit forms by default;
- Analytics route exposes deeper read-only analytics views;
- Review route exposes Match Journal access without changing write semantics;
- Feedback route or drawer exposes the existing copy-first sanitized report flow without external submission;
- Privacy route/details expose compact trust explanation without private values;
- Diagnostics route/details expose technical status only on demand;
- Coach route is clearly pending/deferred and makes no runtime AI claim;
- unknown route falls back safely;
- mobile or narrow layout does not overlap rail/content text;
- forbidden text/controls are absent: arbitrary SQL, database browsing, destructive controls, external issue submission unless issue #298 is separately implemented, AI coaching claims, hidden-card claims, player-mistake labels, and best-line advice.

Recommended validation:

```powershell
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
git diff --check
py tools\check_agent_docs.py
```

If Codex C touches Python files despite the frontend-only recommendation, it must also run focused backend tests and explain why backend changes were unavoidable.

Codex C and Codex E must run path-scoped protected-surface and secret/private-marker scans over changed files:

```powershell
@'
<changed file paths>
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

@'
<changed file paths>
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

If `npm --prefix frontend run build` creates `frontend/dist`, generated build output must be removed before handoff unless a later contract explicitly authorizes committing it.

## Acceptance Criteria

- `docs/contracts/analytics_app_frontend_information_architecture.md` exists.
- The contract defines the frontend-only first slice.
- The contract defines the route/hash model.
- The contract defines left-rail accessibility and active-state requirements.
- The contract defines Dashboard, Analytics, Review, Coach, Import, Feedback, Privacy, and Diagnostics responsibilities.
- The contract defines which sections move, hide, or collapse.
- The contract preserves existing backend/API contracts.
- The contract defers issue #294, #297, and #298 behavior changes.
- The contract forbids parser, analytics schema/ingest, live capture, Match Journal write, external GitHub submission, workbook/webhook/App Script/Sheets, OpenAI/model-provider, AI/coaching, and production changes.
- The contract requires focused frontend tests and docs-only validation.
- No implementation changes are made in the Codex B pass.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer for issue #299.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/299

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_app_frontend_information_architecture.md

Goal:
Compare the current frontend shell, navigation, dashboard, analytics details, Match Journal, manual import, feedback, privacy, and diagnostics surfaces against the contract. Implement only the frontend information-architecture first slice: hash routes, left-rail navigation, dashboard-first cockpit priorities, progressive disclosure, and route/drawer organization using existing backend APIs.

Before editing:
- Confirm branch and git status.
- Identify unrelated dirty files and do not revert them.
- Read the contract, issue #299, and adjacent issue boundaries for #294, #297, and #298.
- Inspect frontend/src/App.tsx, frontend/src/App.css, frontend/src/api.ts, frontend/src/types.ts, frontend/src/App.test.tsx, and relevant local app backend surfaces as reference only.
- State the minimal implementation plan.

Do:
- Keep the first implementation frontend-only unless an unavoidable blocker is found.
- Implement or refine the route/hash model for Dashboard, Coach, Analytics, Review, Privacy, Feedback, Import, and Diagnostics.
- Make Dashboard the first-screen cockpit.
- Move or gate long details, manual import, Match Journal, feedback, privacy, and diagnostics into their owning modes or drawers.
- Preserve existing API payload contracts and safe redaction behavior.
- Preserve existing workflows by routing them, not deleting them.
- Add or update focused frontend tests for navigation, dashboard priority, moved/hidden sections, accessibility, safe display, and forbidden controls/claims.
- Produce docs/implementation_handoffs/analytics_app_frontend_information_architecture_comparison.md.

Do not:
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, Player.log status truth, live capture semantics, analytics schema/migrations/ingest, backend API contracts, Match Journal write semantics, SQLite annotation enrichment, GitHub external submission, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, Line Tracer, hidden-card inference, archetype truth, player-mistake labels, or gameplay advice;
- implement issue #294 auto-refresh, issue #297 live capture behavior changes, or issue #298 live GitHub submission;
- expose arbitrary SQL, database browsing, destructive controls, raw Player.log content, private JSONL payloads, generated database contents, full private paths, sensitive local values, screenshots, or generated/private/local artifacts;
- add a charting library;
- target main;
- stage, commit, push, open a PR, merge, or close issues unless explicitly asked.

Validation:
- npm --prefix frontend run typecheck
- npm --prefix frontend run test -- --run
- npm --prefix frontend run build
- git diff --check
- py tools/check_agent_docs.py
- path-scoped protected-surface and secret/private-marker scans over changed files
- remove frontend/dist before final handoff if build created it

Final output:
- role performed
- issue and contract used
- files changed
- implementation summary
- validation run
- protected-surface and private-artifact status
- remaining risks
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/299"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #299"
  contract_artifact: "docs/contracts/analytics_app_frontend_information_architecture.md"
  target_artifact: "docs/implementation_handoffs/analytics_app_frontend_information_architecture_comparison.md"
  risk_tier: "High overall; first implementation slice Medium frontend-only"
  branch: "codex/analytics-foundation"
  validation:
    - "Codex B docs-only validation: git diff --check"
    - "Codex B docs-only validation: py tools\\check_agent_docs.py"
    - "Codex B docs-only validation: path-scoped protected-surface scan for the contract"
    - "Codex B docs-only validation: path-scoped secret/private-marker scan for the contract"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not target main."
    - "Do not change backend API contracts in the first slice unless Codex C finds an unavoidable blocker and routes back."
    - "Do not implement issue #294 auto-refresh, issue #297 live capture behavior changes, or issue #298 live GitHub submission."
    - "Do not change parser/runtime/analytics schema/analytics ingest/live capture/Match Journal/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not expose arbitrary SQL, database browsing, destructive controls, raw/private artifacts, generated data, or secrets."
```
